from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = PROJECT_ROOT / "backend" / "logs" / "explain-events.jsonl"
REPORTS_DIR = PROJECT_ROOT / "reports"
CSV_PATH = REPORTS_DIR / "medease_log_events.csv"
MD_PATH = REPORTS_DIR / "medease_log_summary.md"


def load_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if not stripped:
                continue
            events.append(json.loads(stripped))
    return events


def flatten_event(event: dict) -> dict[str, object]:
    request = event.get("request", {})
    response = event.get("response", {})
    features = response.get("semantic_complexity_features") or {}
    ui = response.get("ui_actions") or {}

    return {
        "logged_at": event.get("logged_at", ""),
        "provider": event.get("provider", ""),
        "model": event.get("model", ""),
        "complexity_model_ready": event.get("complexity_model_ready", False),
        "session_id": event.get("session_id", ""),
        "language": request.get("language", ""),
        "translate_to_zh": request.get("translate_to_zh", False),
        "save_session": request.get("save_session", False),
        "input_length": request.get("input_length", 0),
        "contains_cjk": request.get("contains_cjk", False),
        "fallback_type": response.get("fallback_type", ""),
        "risk_level": response.get("risk_level", ""),
        "terms_count": response.get("terms_count", 0),
        "annotation_count_en": response.get("annotation_count_en", 0),
        "annotation_count_zh": response.get("annotation_count_zh", 0),
        "summary_length_en": response.get("summary_length_en", 0),
        "summary_length_zh": response.get("summary_length_zh", 0),
        "explanation_length_en": response.get("explanation_length_en", 0),
        "explanation_length_zh": response.get("explanation_length_zh", 0),
        "technical_details_length_en": response.get("technical_details_length_en", 0),
        "technical_details_length_zh": response.get("technical_details_length_zh", 0),
        "next_steps_count_en": response.get("next_steps_count_en", 0),
        "next_steps_count_zh": response.get("next_steps_count_zh", 0),
        "cognitive_load_label": response.get("cognitive_load_label", ""),
        "cognitive_load_score": response.get("cognitive_load_score", 0.0),
        "readability": features.get("readability", 0.0),
        "term_density": features.get("term_density", 0.0),
        "sentence_len": features.get("sentence_len", 0.0),
        "info_density": features.get("info_density", 0.0),
        "show_summary": ui.get("show_summary", False),
        "show_inline_terms": ui.get("show_inline_terms", False),
        "collapse_technical": ui.get("collapse_technical", False),
        "highlight_risk": ui.get("highlight_risk", False),
    }


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def mean(values: list[float]) -> float:
    return round(sum(values) / len(values), 6) if values else 0.0


def ratio(rows: list[dict[str, object]], key: str) -> float:
    if not rows:
        return 0.0
    return round(sum(1 for row in rows if row.get(key)) / len(rows), 4)


def build_summary(rows: list[dict[str, object]]) -> str:
    total = len(rows)
    fallback_counter = Counter(row["fallback_type"] for row in rows)
    load_counter = Counter(row["cognitive_load_label"] for row in rows)
    risk_counter = Counter(row["risk_level"] for row in rows)
    lang_counter = Counter(row["language"] for row in rows)

    lines = [
        "# MedEase Log Summary",
        "",
        f"- Total logged explanation events: **{total}**",
        f"- Language distribution: {format_counter(lang_counter)}",
        f"- Fallback distribution: {format_counter(fallback_counter)}",
        f"- Cognitive load distribution: {format_counter(load_counter)}",
        f"- Risk level distribution: {format_counter(risk_counter)}",
        "",
        "## Aggregate metrics",
        "",
        f"- Mean cognitive load score: **{mean([float(row['cognitive_load_score']) for row in rows])}**",
        f"- Mean readability: **{mean([float(row['readability']) for row in rows])}**",
        f"- Mean term density: **{mean([float(row['term_density']) for row in rows])}**",
        f"- Mean sentence length: **{mean([float(row['sentence_len']) for row in rows])}**",
        f"- Mean info density: **{mean([float(row['info_density']) for row in rows])}**",
        f"- Mean terms count: **{mean([float(row['terms_count']) for row in rows])}**",
        f"- Mean English annotation count: **{mean([float(row['annotation_count_en']) for row in rows])}**",
        f"- Mean Chinese annotation count: **{mean([float(row['annotation_count_zh']) for row in rows])}**",
        "",
        "## UI action trigger rates",
        "",
        f"- `show_summary`: **{ratio(rows, 'show_summary')}**",
        f"- `show_inline_terms`: **{ratio(rows, 'show_inline_terms')}**",
        f"- `collapse_technical`: **{ratio(rows, 'collapse_technical')}**",
        f"- `highlight_risk`: **{ratio(rows, 'highlight_risk')}**",
        "",
        "## Notes",
        "",
        "- These logs describe system behavior and internal adaptive policy activation.",
        "- They are appropriate for system-trace analysis, implementation validation, and appendix tables.",
        "- They should not be presented as direct user-benefit evidence without accompanying human-subject evaluation.",
    ]

    return "\n".join(lines) + "\n"


def format_counter(counter: Counter) -> str:
    if not counter:
        return "none"
    return ", ".join(f"`{key}`={value}" for key, value in sorted(counter.items()))


def main() -> None:
    events = load_events(LOG_PATH)
    rows = [flatten_event(event) for event in events]
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    if rows:
        write_csv(rows, CSV_PATH)
    summary = build_summary(rows)
    MD_PATH.write_text(summary, encoding="utf-8")

    print(f"Loaded {len(rows)} events from {LOG_PATH}")
    if rows:
        print(f"Wrote event CSV to {CSV_PATH}")
    else:
        print("No rows found; CSV was not written.")
    print(f"Wrote markdown summary to {MD_PATH}")


if __name__ == "__main__":
    main()
