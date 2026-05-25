import argparse
import json
import math
from datetime import datetime
from pathlib import Path

from common import DATA_DIR, REPORTS_DIR, mean, normal_cdf, read_csv, std


STUDY_PATH = DATA_DIR / "study_results.csv"
OUT_MD = REPORTS_DIR / "study_analysis_report.md"
OUT_JSON = REPORTS_DIR / "study_summary.json"


def paired_ttest(diffs):
    n = len(diffs)
    if n < 2:
        return 0.0, 1.0

    mu = mean(diffs)
    sd = std(diffs)
    if sd == 0:
        return 0.0, 1.0

    t = mu / (sd / math.sqrt(n))
    p = 2 * (1 - normal_cdf(abs(t)))
    return t, p


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


def main():
    parser = argparse.ArgumentParser(description="Analyze within-subject A/B user study results")
    parser.add_argument("--study-csv", default=str(STUDY_PATH))
    parser.add_argument("--out-md", default=str(OUT_MD))
    parser.add_argument("--out-json", default=str(OUT_JSON))
    args = parser.parse_args()

    study_path = Path(args.study_csv)
    out_md = Path(args.out_md)
    out_json = Path(args.out_json)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = read_csv(study_path)

    by_pid = {}
    skipped_missing_pid = 0
    skipped_invalid_condition = 0
    skipped_incomplete_or_non_numeric = 0
    duplicate_condition_rows_overwritten = 0
    parsed_rows = 0

    for r in rows:
        pid = (r.get("participant_id") or "").strip()
        if not pid:
            skipped_missing_pid += 1
            continue

        cond = (r.get("condition") or "").strip().upper()
        if cond not in {"A", "B"}:
            skipped_invalid_condition += 1
            continue

        accuracy = parse_float(r.get("accuracy"))
        time_sec = parse_float(r.get("time_sec"))
        nasa = parse_float(r.get("nasa_tlx_total"))
        if accuracy is None or time_sec is None or nasa is None:
            skipped_incomplete_or_non_numeric += 1
            continue

        slot = by_pid.setdefault(pid, {})
        if cond in slot:
            duplicate_condition_rows_overwritten += 1
        slot[cond] = {
            "accuracy": accuracy,
            "time_sec": time_sec,
            "nasa": nasa,
        }
        parsed_rows += 1

    paired = []
    for pid, data in by_pid.items():
        if "A" in data and "B" in data:
            paired.append((pid, data["A"], data["B"]))

    a_acc = [a["accuracy"] for _, a, _ in paired]
    b_acc = [b["accuracy"] for _, _, b in paired]
    a_time = [a["time_sec"] for _, a, _ in paired]
    b_time = [b["time_sec"] for _, _, b in paired]
    a_nasa = [a["nasa"] for _, a, _ in paired]
    b_nasa = [b["nasa"] for _, _, b in paired]

    mean_a_acc, mean_b_acc = mean(a_acc), mean(b_acc)
    mean_a_time, mean_b_time = mean(a_time), mean(b_time)
    mean_a_nasa, mean_b_nasa = mean(a_nasa), mean(b_nasa)

    nasa_reduction_pct = ((mean_a_nasa - mean_b_nasa) / mean_a_nasa * 100) if mean_a_nasa else 0
    acc_improve_pct = ((mean_b_acc - mean_a_acc) / mean_a_acc * 100) if mean_a_acc else 0
    time_increase_pct = ((mean_b_time - mean_a_time) / mean_a_time * 100) if mean_a_time else 0

    nasa_diff = [b - a for a, b in zip(a_nasa, b_nasa)]
    acc_diff = [b - a for a, b in zip(a_acc, b_acc)]
    time_diff = [b - a for a, b in zip(a_time, b_time)]

    t_nasa, p_nasa = paired_ttest(nasa_diff)
    t_acc, p_acc = paired_ttest(acc_diff)
    t_time, p_time = paired_ttest(time_diff)

    c1 = nasa_reduction_pct >= 10
    c2 = acc_improve_pct >= 15 and mean_b_acc >= mean_a_acc
    c3 = time_increase_pct <= 10

    summary = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "study_csv": str(study_path),
        "n_participants": len(paired),
        "data_quality": {
            "rows_total": len(rows),
            "rows_parsed": parsed_rows,
            "rows_skipped_missing_pid": skipped_missing_pid,
            "rows_skipped_invalid_condition": skipped_invalid_condition,
            "rows_skipped_incomplete_or_non_numeric": skipped_incomplete_or_non_numeric,
            "duplicate_condition_rows_overwritten": duplicate_condition_rows_overwritten,
            "participants_with_any_valid_row": len(by_pid),
            "participants_with_A_and_B": len(paired),
        },
        "mean": {
            "A_accuracy": round(mean_a_acc, 4),
            "B_accuracy": round(mean_b_acc, 4),
            "A_time_sec": round(mean_a_time, 3),
            "B_time_sec": round(mean_b_time, 3),
            "A_nasa": round(mean_a_nasa, 3),
            "B_nasa": round(mean_b_nasa, 3),
        },
        "delta_pct": {
            "nasa_reduction_pct": round(nasa_reduction_pct, 3),
            "accuracy_improve_pct": round(acc_improve_pct, 3),
            "time_increase_pct": round(time_increase_pct, 3),
        },
        "paired_ttest": {
            "nasa": {"t": round(t_nasa, 4), "p_approx": round(p_nasa, 6)},
            "accuracy": {"t": round(t_acc, 4), "p_approx": round(p_acc, 6)},
            "time": {"t": round(t_time, 4), "p_approx": round(p_time, 6)},
        },
        "acceptance": {
            "criterion_1_nasa_reduction": c1,
            "criterion_2_accuracy_gain": c2,
            "criterion_3_time_non_significant_increase": c3,
            "overall": c1 and c2 and c3,
        },
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    md = []
    md.append("# 用户实验分析报告")
    md.append("")
    md.append(f"- 生成时间: {summary['generated_at']}")
    md.append(f"- 数据文件: {summary['study_csv']}")
    md.append(f"- 被试数: {summary['n_participants']}")
    md.append("")
    md.append("## 数据质量")
    md.append("")
    md.append(f"- 原始行数: {summary['data_quality']['rows_total']}")
    md.append(f"- 有效行数: {summary['data_quality']['rows_parsed']}")
    md.append(f"- 跳过（缺少 participant_id）: {summary['data_quality']['rows_skipped_missing_pid']}")
    md.append(f"- 跳过（condition 非 A/B）: {summary['data_quality']['rows_skipped_invalid_condition']}")
    md.append(f"- 跳过（未填或非数字）: {summary['data_quality']['rows_skipped_incomplete_or_non_numeric']}")
    md.append(f"- 覆盖（同被试同条件重复）: {summary['data_quality']['duplicate_condition_rows_overwritten']}")
    md.append(f"- 有任一有效记录的被试数: {summary['data_quality']['participants_with_any_valid_row']}")
    md.append(f"- A/B 配对完整被试数: {summary['data_quality']['participants_with_A_and_B']}")
    md.append("")
    md.append("## 均值结果")
    md.append("")
    md.append(f"- Accuracy: A={mean_a_acc:.3f}, B={mean_b_acc:.3f}, 提升={acc_improve_pct:.2f}%")
    md.append(f"- NASA-TLX: A={mean_a_nasa:.3f}, B={mean_b_nasa:.3f}, 下降={nasa_reduction_pct:.2f}%")
    md.append(f"- Time: A={mean_a_time:.2f}s, B={mean_b_time:.2f}s, 变化={time_increase_pct:.2f}%")
    md.append("")
    md.append("## 近似配对t检验（正态近似）")
    md.append("")
    md.append(f"- NASA: t={t_nasa:.3f}, p≈{p_nasa:.6f}")
    md.append(f"- Accuracy: t={t_acc:.3f}, p≈{p_acc:.6f}")
    md.append(f"- Time: t={t_time:.3f}, p≈{p_time:.6f}")
    md.append("")
    md.append("## 验收结论")
    md.append("")
    md.append(f"- 场景1（NASA下降>=10%）: {'通过' if c1 else '未通过'}")
    md.append(f"- 场景2（准确率提升>=15%）: {'通过' if c2 else '未通过'}")
    md.append(f"- 场景3（时长增幅<=10%）: {'通过' if c3 else '未通过'}")
    md.append(f"- 总体: {'通过' if (c1 and c2 and c3) else '未通过'}")

    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(md), encoding="utf-8")

    print(f"[OK] 输入: {study_path}")
    print(f"[OK] 输出: {out_md}")
    print(f"[OK] 输出: {out_json}")


if __name__ == "__main__":
    main()
