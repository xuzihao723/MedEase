import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

from baseline_common import (
    DEFAULT_EVAL_LABELS_CSV,
    DEFAULT_EVAL_TEXT_CSV,
    DEFAULT_OUTPUT_ROOT,
    DEFAULT_TRAIN_LABELS_CSV,
    DEFAULT_TRAIN_TEXT_CSV,
    LABELS,
    load_official_manual_datasets,
)
from common import compute_features, difficulty_score, mean, read_csv, split_sentences, token_count, write_csv


MEDICAL_KEYWORDS_EN = {
    "mg",
    "ml",
    "tablet",
    "dose",
    "ecg",
    "mri",
    "ct",
    "xray",
    "ultrasound",
    "bilirubin",
    "sgpt",
    "sgot",
    "hba1c",
    "blood pressure",
    "hypertension",
    "diabetes",
    "tumor",
    "cancer",
    "infection",
    "antibiotic",
    "surgery",
    "diagnosis",
    "differential",
    "ovulation",
    "pregnancy",
    "renal",
    "liver",
    "cardiac",
    "neurolog",
    "rheumat",
}

UNCERTAINTY_KEYWORDS = {
    "could",
    "might",
    "may",
    "possible",
    "likely",
    "probably",
    "suggest",
    "consider",
    "rule out",
}

URGENCY_KEYWORDS = {
    "emergency",
    "urgent",
    "immediately",
    "as soon as possible",
    "er",
    "fatal",
    "severe",
    "dangerous",
    "hospitalized",
}


def safe_float(v, default=0.0):
    try:
        return float(v)
    except Exception:
        return default


def parse_float(raw):
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def predict_with_thresholds(model, x_eval, decision):
    if not hasattr(model, "predict_proba"):
        preds = list(model.predict(x_eval))
        return preds, None

    probs = model.predict_proba(x_eval)
    classes = list(model.classes_)
    idx = {c: i for i, c in enumerate(classes)}
    low_th = decision.get("low")
    high_th = decision.get("high")

    preds = []
    for p in probs:
        p_high = float(p[idx["high"]]) if "high" in idx else 0.0
        p_low = float(p[idx["low"]]) if "low" in idx else 0.0

        if high_th is not None and p_high >= high_th:
            preds.append("high")
            continue
        if low_th is not None and p_low >= low_th:
            preds.append("low")
            continue
        best_i = max(range(len(p)), key=lambda i: p[i])
        preds.append(classes[best_i])

    return preds, (probs, classes)


def classify_reply_type(text, feat):
    lower = (text or "").lower()
    tokens = token_count(text or "")
    sent_count = len(split_sentences(text or ""))
    digit_count = len(re.findall(r"\d", text or ""))
    keyword_hits = sum(1 for kw in MEDICAL_KEYWORDS_EN if kw in lower)

    if tokens <= 22:
        return "short_directive"
    if digit_count >= 10:
        return "numeric_lab_heavy"
    if any(kw in lower for kw in URGENCY_KEYWORDS):
        return "urgency_or_risk"
    if sent_count >= 6 or tokens >= 170:
        return "long_multistep_explanation"
    if any(kw in lower for kw in UNCERTAINTY_KEYWORDS):
        return "differential_uncertainty"
    if keyword_hits >= 3 or safe_float(feat.get("term_density"), 0.0) >= 0.02:
        return "term_dense_education"
    return "general_advice"


def load_official_eval_predictions(dataset, model_path: Path):
    try:
        import joblib
    except Exception as e:
        raise RuntimeError("joblib is required for error analysis") from e

    bundle = joblib.load(model_path)
    model = bundle["model"]
    model_type = bundle.get("model_type", "text")
    decision = bundle.get("decision_thresholds") or {}

    if model_type == "semantic":
        x_eval = []
        for row in dataset.eval_rows:
            f = compute_features(row["text"])
            x_eval.append(
                [
                    safe_float(f.get("readability")),
                    safe_float(f.get("term_density")),
                    safe_float(f.get("sentence_len")),
                    safe_float(f.get("info_density")),
                ]
            )
    else:
        x_eval = [r["text"] for r in dataset.eval_rows]

    y_pred, proba_bundle = predict_with_thresholds(model, x_eval, decision)
    out = {}
    for i, row in enumerate(dataset.eval_rows):
        rec = {
            "sample_id": row["sample_id"],
            "true_label": row["label"],
            "pred_label": y_pred[i],
        }
        if proba_bundle is not None:
            probs, classes = proba_bundle
            p = probs[i]
            idx = {c: j for j, c in enumerate(classes)}
            rec["p_low"] = float(p[idx["low"]]) if "low" in idx else 0.0
            rec["p_medium"] = float(p[idx["medium"]]) if "medium" in idx else 0.0
            rec["p_high"] = float(p[idx["high"]]) if "high" in idx else 0.0
        out[row["sample_id"]] = rec

    return out, decision


def discover_baseline_prediction_maps(output_root: Path):
    pred_maps = {}
    summary_paths = sorted(output_root.rglob("summary.json"))
    for sp in summary_paths:
        try:
            summary = json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            continue

        if summary.get("metric_scope") != "manual_eval":
            continue
        if int(summary.get("eval_samples", 0) or 0) != 320:
            continue

        pred_csv = summary.get("prediction_csv")
        if pred_csv:
            pp = Path(pred_csv)
        else:
            pp = sp.parent / "predictions.csv"
        if not pp.exists():
            continue

        rows = read_csv(pp)
        model_id = str(summary.get("model_id") or "unknown")
        baseline_name = str(summary.get("baseline_name") or "baseline")
        key = f"{baseline_name}:{model_id}"

        m = {}
        for r in rows:
            sid = (r.get("sample_id") or "").strip()
            pred = (r.get("pred_label") or "").strip().lower()
            if sid and pred in set(LABELS):
                m[sid] = pred
        if len(m) >= 300:
            pred_maps[key] = m

    return pred_maps


def build_sample_meta(eval_rows, official_pred_map):
    out = {}
    for row in eval_rows:
        sid = row["sample_id"]
        text = row["text"]
        feat = compute_features(text)
        score = difficulty_score(
            readability=safe_float(feat.get("readability")),
            term_density=safe_float(feat.get("term_density")),
            sentence_len=safe_float(feat.get("sentence_len")),
            info_density=safe_float(feat.get("info_density")),
        )
        reply_type = classify_reply_type(text, feat)
        off_pred = official_pred_map[sid]["pred_label"]
        out[sid] = {
            "sample_id": sid,
            "true_label": row["label"],
            "official_pred_label": off_pred,
            "official_error": int(off_pred != row["label"]),
            "reply_type": reply_type,
            "token_count": token_count(text),
            "sentence_count": len(split_sentences(text)),
            "difficulty_score": score,
            "readability": safe_float(feat.get("readability")),
            "term_density": safe_float(feat.get("term_density")),
            "sentence_len": safe_float(feat.get("sentence_len")),
            "info_density": safe_float(feat.get("info_density")),
            "text_preview": text[:220].replace("\n", " "),
        }
    return out


def write_error_by_class(official_pred_map, out_csv: Path):
    rows = []
    for true_label in LABELS:
        subset = [r for r in official_pred_map.values() if r["true_label"] == true_label]
        support = len(subset)
        pred_counter = Counter(r["pred_label"] for r in subset)
        correct = pred_counter.get(true_label, 0)
        error = support - correct
        wrong_counter = {k: v for k, v in pred_counter.items() if k != true_label}
        most_confused = max(wrong_counter.items(), key=lambda x: x[1])[0] if wrong_counter else ""

        rows.append(
            {
                "row_type": "class_summary",
                "true_label": true_label,
                "pred_label": "",
                "support": support,
                "count": support,
                "ratio": 1.0,
                "correct": correct,
                "error": error,
                "error_rate": round(error / support, 6) if support else 0.0,
                "pred_low": pred_counter.get("low", 0),
                "pred_medium": pred_counter.get("medium", 0),
                "pred_high": pred_counter.get("high", 0),
                "most_confused_with": most_confused,
            }
        )

        for pred_label in LABELS:
            if pred_label == true_label:
                continue
            c = pred_counter.get(pred_label, 0)
            if c <= 0:
                continue
            rows.append(
                {
                    "row_type": "confusion_pair",
                    "true_label": true_label,
                    "pred_label": pred_label,
                    "support": support,
                    "count": c,
                    "ratio": round(c / support, 6) if support else 0.0,
                    "correct": "",
                    "error": "",
                    "error_rate": "",
                    "pred_low": "",
                    "pred_medium": "",
                    "pred_high": "",
                    "most_confused_with": "",
                }
            )

    write_csv(
        out_csv,
        [
            "row_type",
            "true_label",
            "pred_label",
            "support",
            "count",
            "ratio",
            "correct",
            "error",
            "error_rate",
            "pred_low",
            "pred_medium",
            "pred_high",
            "most_confused_with",
        ],
        rows,
    )


def write_hard_reply_types(sample_meta, all_pred_maps, out_md: Path):
    rows = list(sample_meta.values())
    n_models = len(all_pred_maps)

    for r in rows:
        sid = r["sample_id"]
        votes = 0
        for _, pmap in all_pred_maps.items():
            pred = pmap.get(sid)
            if pred and pred != r["true_label"]:
                votes += 1
        r["error_votes"] = votes
        r["error_vote_rate"] = votes / n_models if n_models else 0.0

    by_type = defaultdict(list)
    for r in rows:
        by_type[r["reply_type"]].append(r)

    summary_rows = []
    for reply_type, items in by_type.items():
        n = len(items)
        err = sum(i["official_error"] for i in items)
        summary_rows.append(
            {
                "reply_type": reply_type,
                "n_samples": n,
                "official_error_count": err,
                "official_error_rate": err / n if n else 0.0,
                "avg_difficulty_score": mean([i["difficulty_score"] for i in items]),
                "avg_sentence_len": mean([i["sentence_len"] for i in items]),
                "avg_token_count": mean([i["token_count"] for i in items]),
                "avg_error_votes": mean([i["error_votes"] for i in items]),
                "avg_error_vote_rate": mean([i["error_vote_rate"] for i in items]),
            }
        )

    summary_rows.sort(key=lambda x: (x["official_error_rate"], x["n_samples"]), reverse=True)

    md = []
    md.append("# Hard Reply Types")
    md.append("")
    md.append("- metric_scope: `manual_eval`")
    md.append("- model_focus: `official_lr_reference`")
    md.append(f"- compared_models_for_error_votes: `{n_models}`")
    md.append("")
    md.append(
        "| reply_type | n_samples | official_error_rate | avg_difficulty | avg_sentence_len | avg_error_vote_rate |"
    )
    md.append("|---|---:|---:|---:|---:|---:|")
    for r in summary_rows:
        md.append(
            f"| {r['reply_type']} | {r['n_samples']} | {r['official_error_rate']:.4f} | "
            f"{r['avg_difficulty_score']:.4f} | {r['avg_sentence_len']:.2f} | {r['avg_error_vote_rate']:.4f} |"
        )

    md.append("")
    md.append("## Representative Hard Cases (Official Wrong)")
    md.append("")
    for r in summary_rows[:5]:
        rt = r["reply_type"]
        wrong = [x for x in by_type[rt] if x["official_error"] == 1]
        wrong = sorted(wrong, key=lambda x: x["error_vote_rate"], reverse=True)[:5]
        if not wrong:
            continue
        md.append(f"### {rt}")
        for w in wrong:
            md.append(
                f"- {w['sample_id']} | true={w['true_label']} pred={w['official_pred_label']} | "
                f"vote_rate={w['error_vote_rate']:.2f} | text={w['text_preview']}"
            )
        md.append("")

    out_md.write_text("\n".join(md), encoding="utf-8")


def write_boundary_cases(sample_meta, official_pred_map, decision, out_csv: Path):
    low_th = decision.get("low")
    high_th = decision.get("high")

    rows = []
    for sid, p in official_pred_map.items():
        if "p_low" not in p:
            continue
        probs = {"low": p["p_low"], "medium": p["p_medium"], "high": p["p_high"]}
        ordered = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        top1_label, top1_prob = ordered[0]
        top2_label, top2_prob = ordered[1]
        margin = top1_prob - top2_prob

        pair = "-".join(sorted([top1_label, top2_label], key=lambda x: LABELS.index(x)))

        threshold_dists = [margin]
        low_dist = ""
        high_dist = ""
        if low_th is not None:
            low_dist = abs(probs["low"] - float(low_th))
            threshold_dists.append(low_dist)
        if high_th is not None:
            high_dist = abs(probs["high"] - float(high_th))
            threshold_dists.append(high_dist)
        decision_edge_distance = min(threshold_dists)

        is_boundary = int(margin <= 0.08 or decision_edge_distance <= 0.03)

        m = sample_meta[sid]
        rows.append(
            {
                "sample_id": sid,
                "true_label": p["true_label"],
                "pred_label": p["pred_label"],
                "is_error": int(p["true_label"] != p["pred_label"]),
                "boundary_pair": pair,
                "top1_label": top1_label,
                "top1_prob": round(top1_prob, 6),
                "top2_label": top2_label,
                "top2_prob": round(top2_prob, 6),
                "margin_top1_top2": round(margin, 6),
                "p_low": round(probs["low"], 6),
                "p_medium": round(probs["medium"], 6),
                "p_high": round(probs["high"], 6),
                "decision_low_threshold": low_th if low_th is not None else "",
                "decision_high_threshold": high_th if high_th is not None else "",
                "dist_to_low_threshold": round(low_dist, 6) if low_dist != "" else "",
                "dist_to_high_threshold": round(high_dist, 6) if high_dist != "" else "",
                "decision_edge_distance": round(decision_edge_distance, 6),
                "is_boundary_case": is_boundary,
                "reply_type": m["reply_type"],
                "difficulty_score": round(m["difficulty_score"], 6),
                "sentence_len": round(m["sentence_len"], 4),
                "term_density": round(m["term_density"], 6),
                "info_density": round(m["info_density"], 6),
                "text_preview": m["text_preview"],
            }
        )

    rows.sort(key=lambda x: (x["margin_top1_top2"], x["decision_edge_distance"]))
    write_csv(
        out_csv,
        [
            "sample_id",
            "true_label",
            "pred_label",
            "is_error",
            "boundary_pair",
            "top1_label",
            "top1_prob",
            "top2_label",
            "top2_prob",
            "margin_top1_top2",
            "p_low",
            "p_medium",
            "p_high",
            "decision_low_threshold",
            "decision_high_threshold",
            "dist_to_low_threshold",
            "dist_to_high_threshold",
            "decision_edge_distance",
            "is_boundary_case",
            "reply_type",
            "difficulty_score",
            "sentence_len",
            "term_density",
            "info_density",
            "text_preview",
        ],
        rows,
    )


def build_paired_participants(study_rows):
    by_pid = {}
    for r in study_rows:
        pid = (r.get("participant_id") or "").strip()
        if not pid:
            continue
        cond = (r.get("condition") or "").strip().upper()
        if cond not in {"A", "B"}:
            continue
        acc = parse_float(r.get("accuracy"))
        tsec = parse_float(r.get("time_sec"))
        nasa = parse_float(r.get("nasa_tlx_total"))
        if acc is None or tsec is None or nasa is None:
            continue
        slot = by_pid.setdefault(
            pid,
            {
                "A": None,
                "B": None,
                "order_group": (r.get("order_group") or "").strip().upper(),
            },
        )
        slot[cond] = {"accuracy": acc, "time_sec": tsec, "nasa": nasa}

    paired = []
    for pid, d in by_pid.items():
        if d["A"] is None or d["B"] is None:
            continue
        paired.append(
            {
                "participant_id": pid,
                "order_group": d.get("order_group") or "UNK",
                "A": d["A"],
                "B": d["B"],
            }
        )
    return paired


def load_order_group_map(randomization_csv: Path):
    if not randomization_csv.exists():
        return {}
    rows = read_csv(randomization_csv)
    out = {}
    for r in rows:
        pid = (r.get("participant_id") or "").strip()
        og = (r.get("order_group") or "").strip().upper()
        if pid and og:
            out[pid] = og
    return out


def summarize_pair_group(items, group_type, group_value):
    if not items:
        return None
    a_acc = [x["A"]["accuracy"] for x in items]
    b_acc = [x["B"]["accuracy"] for x in items]
    a_nasa = [x["A"]["nasa"] for x in items]
    b_nasa = [x["B"]["nasa"] for x in items]
    a_time = [x["A"]["time_sec"] for x in items]
    b_time = [x["B"]["time_sec"] for x in items]

    ma_a = mean(a_acc)
    ma_b = mean(b_acc)
    mn_a = mean(a_nasa)
    mn_b = mean(b_nasa)
    mt_a = mean(a_time)
    mt_b = mean(b_time)

    return {
        "analysis_scope": "participant_level",
        "group_type": group_type,
        "group_value": group_value,
        "n_participants": len(items),
        "n_rows": len(items) * 2,
        "mean_A_accuracy": round(ma_a, 6),
        "mean_B_accuracy": round(ma_b, 6),
        "accuracy_gain_abs": round(ma_b - ma_a, 6),
        "accuracy_gain_pct": round(((ma_b - ma_a) / ma_a * 100.0) if ma_a else 0.0, 6),
        "mean_A_nasa": round(mn_a, 6),
        "mean_B_nasa": round(mn_b, 6),
        "nasa_reduction_abs": round(mn_a - mn_b, 6),
        "nasa_reduction_pct": round(((mn_a - mn_b) / mn_a * 100.0) if mn_a else 0.0, 6),
        "mean_A_time_sec": round(mt_a, 6),
        "mean_B_time_sec": round(mt_b, 6),
        "time_increase_abs": round(mt_b - mt_a, 6),
        "time_increase_pct": round(((mt_b - mt_a) / mt_a * 100.0) if mt_a else 0.0, 6),
        "status": "ok",
        "note": "",
    }


def write_ui_effect_subgroup(study_csv: Path, sample_meta, out_csv: Path, order_group_map=None):
    study_rows = read_csv(study_csv)
    paired = build_paired_participants(study_rows)
    order_group_map = order_group_map or {}
    for p in paired:
        if p.get("order_group") and p["order_group"] != "UNK":
            continue
        fallback = (order_group_map.get(p["participant_id"]) or "").strip().upper()
        if fallback:
            p["order_group"] = fallback

    rows = []
    all_row = summarize_pair_group(paired, "all_participants", "all")
    if all_row:
        rows.append(all_row)

    by_order = defaultdict(list)
    for p in paired:
        by_order[p["order_group"]].append(p)
    for og, items in sorted(by_order.items()):
        r = summarize_pair_group(items, "order_group", og)
        if r:
            rows.append(r)

    if paired:
        med = sorted([p["A"]["accuracy"] for p in paired])[len(paired) // 2]
        low_group = [p for p in paired if p["A"]["accuracy"] <= med]
        high_group = [p for p in paired if p["A"]["accuracy"] > med]
        r1 = summarize_pair_group(low_group, "baseline_A_accuracy_bin", f"<=median({med:.3f})")
        r2 = summarize_pair_group(high_group, "baseline_A_accuracy_bin", f">median({med:.3f})")
        if r1:
            rows.append(r1)
        if r2:
            rows.append(r2)

    has_sample_id = any((r.get("sample_id") or "").strip() for r in study_rows)
    if not has_sample_id:
        rows.append(
            {
                "analysis_scope": "text_type_level",
                "group_type": "reply_type",
                "group_value": "N/A",
                "n_participants": 0,
                "n_rows": len(study_rows),
                "mean_A_accuracy": "",
                "mean_B_accuracy": "",
                "accuracy_gain_abs": "",
                "accuracy_gain_pct": "",
                "mean_A_nasa": "",
                "mean_B_nasa": "",
                "nasa_reduction_abs": "",
                "nasa_reduction_pct": "",
                "mean_A_time_sec": "",
                "mean_B_time_sec": "",
                "time_increase_abs": "",
                "time_increase_pct": "",
                "status": "missing_sample_level_fields",
                "note": "study_results.csv currently has no sample_id per trial; cannot compute true text-type UI effect. Add sample_id and per-trial rows for A/B.",
            }
        )
    else:
        typed = []
        for r in study_rows:
            sid = (r.get("sample_id") or "").strip()
            cond = (r.get("condition") or "").strip().upper()
            if sid not in sample_meta or cond not in {"A", "B"}:
                continue
            acc = parse_float(r.get("accuracy"))
            tsec = parse_float(r.get("time_sec"))
            nasa = parse_float(r.get("nasa_tlx_total"))
            if acc is None or tsec is None or nasa is None:
                continue
            typed.append(
                {
                    "reply_type": sample_meta[sid]["reply_type"],
                    "condition": cond,
                    "accuracy": acc,
                    "time_sec": tsec,
                    "nasa": nasa,
                }
            )

        if typed:
            by_type = defaultdict(list)
            for t in typed:
                by_type[t["reply_type"]].append(t)
            for rt, items in sorted(by_type.items()):
                a = [x for x in items if x["condition"] == "A"]
                b = [x for x in items if x["condition"] == "B"]
                if not a or not b:
                    continue
                ma_a = mean([x["accuracy"] for x in a])
                ma_b = mean([x["accuracy"] for x in b])
                mn_a = mean([x["nasa"] for x in a])
                mn_b = mean([x["nasa"] for x in b])
                mt_a = mean([x["time_sec"] for x in a])
                mt_b = mean([x["time_sec"] for x in b])
                rows.append(
                    {
                        "analysis_scope": "text_type_level",
                        "group_type": "reply_type",
                        "group_value": rt,
                        "n_participants": "",
                        "n_rows": len(items),
                        "mean_A_accuracy": round(ma_a, 6),
                        "mean_B_accuracy": round(ma_b, 6),
                        "accuracy_gain_abs": round(ma_b - ma_a, 6),
                        "accuracy_gain_pct": round(((ma_b - ma_a) / ma_a * 100.0) if ma_a else 0.0, 6),
                        "mean_A_nasa": round(mn_a, 6),
                        "mean_B_nasa": round(mn_b, 6),
                        "nasa_reduction_abs": round(mn_a - mn_b, 6),
                        "nasa_reduction_pct": round(((mn_a - mn_b) / mn_a * 100.0) if mn_a else 0.0, 6),
                        "mean_A_time_sec": round(mt_a, 6),
                        "mean_B_time_sec": round(mt_b, 6),
                        "time_increase_abs": round(mt_b - mt_a, 6),
                        "time_increase_pct": round(((mt_b - mt_a) / mt_a * 100.0) if mt_a else 0.0, 6),
                        "status": "ok",
                        "note": "",
                    }
                )

    write_csv(
        out_csv,
        [
            "analysis_scope",
            "group_type",
            "group_value",
            "n_participants",
            "n_rows",
            "mean_A_accuracy",
            "mean_B_accuracy",
            "accuracy_gain_abs",
            "accuracy_gain_pct",
            "mean_A_nasa",
            "mean_B_nasa",
            "nasa_reduction_abs",
            "nasa_reduction_pct",
            "mean_A_time_sec",
            "mean_B_time_sec",
            "time_increase_abs",
            "time_increase_pct",
            "status",
            "note",
        ],
        rows,
    )


def write_summary_md(out_md: Path, outputs: dict, n_models: int):
    lines = []
    lines.append("# Error Analysis Summary")
    lines.append("")
    lines.append(f"- generated_at: {datetime.now().isoformat(timespec='seconds')}")
    lines.append("- metric_scope: manual_eval")
    lines.append("- focus_model: official_lr_reference")
    lines.append(f"- compared_prediction_models: {n_models}")
    lines.append("")
    lines.append("## Outputs")
    lines.append("")
    for k, v in outputs.items():
        lines.append(f"- {k}: `{v}`")
    out_md.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Run model error analysis and UI subgroup analysis")
    parser.add_argument("--train-text-csv", default=str(DEFAULT_TRAIN_TEXT_CSV))
    parser.add_argument("--eval-text-csv", default=str(DEFAULT_EVAL_TEXT_CSV))
    parser.add_argument("--train-labels-csv", default=str(DEFAULT_TRAIN_LABELS_CSV))
    parser.add_argument("--eval-labels-csv", default=str(DEFAULT_EVAL_LABELS_CSV))
    parser.add_argument("--official-model", default="models/cognitive_load_classifier.joblib")
    parser.add_argument("--study-csv", default="data/study_results.csv")
    parser.add_argument("--study-randomization-csv", default="data/study_randomization_n30.csv")
    parser.add_argument("--baseline-output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--output-dir", default="reports/error_analysis")
    args = parser.parse_args()

    dataset = load_official_manual_datasets(
        train_text_csv=Path(args.train_text_csv),
        eval_text_csv=Path(args.eval_text_csv),
        train_labels_csv=Path(args.train_labels_csv),
        eval_labels_csv=Path(args.eval_labels_csv),
    )
    if len(dataset.eval_rows) != 320:
        raise RuntimeError(f"Expected 320 eval rows, got {len(dataset.eval_rows)}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    official_pred_map, decision = load_official_eval_predictions(dataset, Path(args.official_model))
    sample_meta = build_sample_meta(dataset.eval_rows, official_pred_map)

    model_pred_maps = discover_baseline_prediction_maps(Path(args.baseline_output_root))
    model_pred_maps["official_lr_reference:tfidf_lr_manual_only"] = {
        sid: rec["pred_label"] for sid, rec in official_pred_map.items()
    }

    error_by_class_csv = output_dir / "error_by_class.csv"
    hard_reply_types_md = output_dir / "hard_reply_types.md"
    boundary_cases_csv = output_dir / "boundary_cases.csv"
    ui_effect_subgroup_csv = output_dir / "ui_effect_subgroup.csv"
    summary_md = output_dir / "summary.md"

    write_error_by_class(official_pred_map, error_by_class_csv)
    write_hard_reply_types(sample_meta, model_pred_maps, hard_reply_types_md)
    write_boundary_cases(sample_meta, official_pred_map, decision, boundary_cases_csv)
    order_group_map = load_order_group_map(Path(args.study_randomization_csv))
    write_ui_effect_subgroup(Path(args.study_csv), sample_meta, ui_effect_subgroup_csv, order_group_map=order_group_map)

    outputs = {
        "error_by_class_csv": str(error_by_class_csv.resolve()),
        "hard_reply_types_md": str(hard_reply_types_md.resolve()),
        "boundary_cases_csv": str(boundary_cases_csv.resolve()),
        "ui_effect_subgroup_csv": str(ui_effect_subgroup_csv.resolve()),
    }
    write_summary_md(summary_md, outputs, len(model_pred_maps))

    print("[OK] error analysis done")
    print(f"[OK] {error_by_class_csv}")
    print(f"[OK] {hard_reply_types_md}")
    print(f"[OK] {boundary_cases_csv}")
    print(f"[OK] {ui_effect_subgroup_csv}")
    print(f"[OK] {summary_md}")


if __name__ == "__main__":
    main()
