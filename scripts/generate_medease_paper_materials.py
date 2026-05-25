from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"
CSV_PATH = REPORTS_DIR / "medease_log_events.csv"
METHODS_RESULTS_PATH = REPORTS_DIR / "medease_methods_results_draft.md"
POLISHED_TEXT_PATH = REPORTS_DIR / "medease_methods_results_polished.md"
LOAD_FIG_PATH = REPORTS_DIR / "medease_load_distribution.svg"
UI_FIG_PATH = REPORTS_DIR / "medease_ui_actions.svg"


def load_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_svg_bar_chart(
    output_path: Path,
    title: str,
    labels: list[str],
    values: list[float],
    *,
    width: int = 840,
    height: int = 420,
    bar_color: str = "#0F766E",
    x_label_suffix: str = "",
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    max_value = max(values) if values else 1
    max_value = max(max_value, 1)
    margin_left = 90
    margin_right = 40
    margin_top = 70
    margin_bottom = 90
    chart_width = width - margin_left - margin_right
    chart_height = height - margin_top - margin_bottom
    bar_gap = 24
    bar_width = (chart_width - bar_gap * max(len(values) - 1, 0)) / max(len(values), 1)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#F6F7F8"/>',
        f'<text x="{margin_left}" y="36" font-family="Arial, sans-serif" font-size="26" font-weight="700" fill="#1D1D1F">{escape_xml(title)}</text>',
        f'<line x1="{margin_left}" y1="{margin_top + chart_height}" x2="{margin_left + chart_width}" y2="{margin_top + chart_height}" stroke="#A1A1AA" stroke-width="1"/>',
        f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + chart_height}" stroke="#A1A1AA" stroke-width="1"/>',
    ]

    for tick_index in range(5):
        value = max_value * tick_index / 4
        y = margin_top + chart_height - (chart_height * tick_index / 4)
        parts.append(f'<line x1="{margin_left}" y1="{y}" x2="{margin_left + chart_width}" y2="{y}" stroke="#E4E4E7" stroke-width="1"/>')
        parts.append(
            f'<text x="{margin_left - 12}" y="{y + 5}" text-anchor="end" font-family="Arial, sans-serif" font-size="12" fill="#52525B">{value:.2f}</text>'
        )

    for index, (label, value) in enumerate(zip(labels, values)):
        x = margin_left + index * (bar_width + bar_gap)
        bar_height = 0 if max_value == 0 else (value / max_value) * chart_height
        y = margin_top + chart_height - bar_height
        parts.append(f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_height}" rx="6" fill="{bar_color}"/>')
        parts.append(
            f'<text x="{x + bar_width / 2}" y="{y - 8}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#1D1D1F">{value:.3f}{escape_xml(x_label_suffix)}</text>'
        )
        parts.append(
            f'<text x="{x + bar_width / 2}" y="{margin_top + chart_height + 24}" text-anchor="middle" font-family="Arial, sans-serif" font-size="12" fill="#3F3F46">{escape_xml(label)}</text>'
        )

    parts.append("</svg>")
    output_path.write_text("\n".join(parts), encoding="utf-8")


def build_methods_results(rows: list[dict[str, str]]) -> str:
    total = len(rows)
    load_counter = Counter(row.get("cognitive_load_label", "unknown") for row in rows)
    risk_counter = Counter(row.get("risk_level", "unknown") for row in rows)

    mean_score = mean(float(row.get("cognitive_load_score", 0.0)) for row in rows)
    mean_terms = mean(float(row.get("terms_count", 0.0)) for row in rows)
    mean_annotation_en = mean(float(row.get("annotation_count_en", 0.0)) for row in rows)
    mean_annotation_zh = mean(float(row.get("annotation_count_zh", 0.0)) for row in rows)
    summary_rate = ratio(rows, "show_summary")
    inline_rate = ratio(rows, "show_inline_terms")
    collapse_rate = ratio(rows, "collapse_technical")
    risk_rate = ratio(rows, "highlight_risk")

    return f"""# Draft Text for Methods and Results

## Methods: System Logging and Internal Trace

To support system-level analysis, the MedEase prototype recorded internal traces for each explanation request. The logging layer did not store raw medical text. Instead, it recorded a hashed identifier of the input, the input length, the detected language, the cognitive load label, the cognitive load score, semantic complexity features, term counts, annotation counts, and the UI actions triggered for the final presentation. These logs were used to verify that the adaptive interface was driven by the estimated complexity of the generated explanation rather than fixed display rules.

The backend generated a structured explanation with plain-language summaries, term annotations, risk information, and next-step advice. The English explanation was then passed to the cognitive load classifier, which returned a load label and score together with semantic complexity features. Based on these outputs, the frontend selectively activated presentation strategies such as summary display, inline term explanation, and collapsing technical details.

## Results: System Trace Analysis

Across **{total}** logged explanation events, the system consistently returned structured outputs that included summaries, term explanations, risk information, and recommended next steps. The internal trace data showed the following cognitive load distribution: {format_counter(load_counter)}. Risk levels were distributed as follows: {format_counter(risk_counter)}.

The mean cognitive load score was **{mean_score:.6f}**. On average, each explanation produced **{mean_terms:.3f}** extracted terms, with **{mean_annotation_en:.3f}** English inline annotations and **{mean_annotation_zh:.3f}** Chinese inline annotations. The adaptive interface triggered `show_summary` in **{summary_rate:.3f}** of logged sessions, `show_inline_terms` in **{inline_rate:.3f}**, `collapse_technical` in **{collapse_rate:.3f}**, and `highlight_risk` in **{risk_rate:.3f}**.

These internal results indicate that the adaptive pipeline was functioning as intended at the system level: the LLM generated explanation content, the cognitive load model estimated explanation difficulty, and the frontend responded by adjusting the amount and form of explanation shown to the user. These logs should be interpreted as system-behavior evidence rather than direct end-user benefit evidence, which still requires human-subject evaluation.
"""


def build_polished_methods_results(rows: list[dict[str, str]]) -> str:
    total = len(rows)
    load_counter = Counter(row.get("cognitive_load_label", "unknown") for row in rows)
    risk_counter = Counter(row.get("risk_level", "unknown") for row in rows)
    fallback_counter = Counter(row.get("fallback_type", "unknown") for row in rows)

    mean_score = mean(float(row.get("cognitive_load_score", 0.0)) for row in rows)
    mean_readability = mean(float(row.get("readability", 0.0)) for row in rows)
    mean_term_density = mean(float(row.get("term_density", 0.0)) for row in rows)
    mean_sentence_len = mean(float(row.get("sentence_len", 0.0)) for row in rows)
    mean_info_density = mean(float(row.get("info_density", 0.0)) for row in rows)
    mean_terms = mean(float(row.get("terms_count", 0.0)) for row in rows)
    mean_annotation_en = mean(float(row.get("annotation_count_en", 0.0)) for row in rows)
    mean_annotation_zh = mean(float(row.get("annotation_count_zh", 0.0)) for row in rows)
    summary_rate = ratio(rows, "show_summary")
    inline_rate = ratio(rows, "show_inline_terms")
    collapse_rate = ratio(rows, "collapse_technical")
    risk_rate = ratio(rows, "highlight_risk")

    sample_note = (
        "Because the current trace set is small, these descriptive statistics are reported as an implementation check rather than as evidence of end-user benefit."
        if total < 30
        else "These descriptive statistics summarize the behavior of the deployed prototype over the logged trace set."
    )

    return f"""# Polished Methods and Results Text

## Methods: System Trace Logging

To examine whether the adaptive explanation pipeline operated as intended, MedEase recorded a lightweight internal trace for each explanation request. The trace was designed for system-level analysis rather than user surveillance: it did not store the raw medical text or the full generated explanation. Instead, each record contained a hashed input identifier, input length, language indicators, model provider metadata, the predicted cognitive load label and score, semantic complexity features, term and annotation counts, risk level, and the user-interface actions selected for the final presentation.

For each request, the backend first generated a structured plain-language medical explanation using an external LLM service. The English explanation, technical details, and extracted terminology were then passed to the cognitive load classifier. The classifier produced a categorical cognitive load estimate (`low`, `medium`, or `high`), a confidence-like score, and semantic complexity features including readability, term density, sentence length, and information density. These outputs were subsequently mapped to adaptive presentation actions, including whether to show a plain-language summary, activate inline term explanations, collapse technical details, and highlight risk-related guidance. The frontend used these actions to adjust the presentation, but the internal model outputs were not shown to users.

## Results: System Trace Analysis

The current trace file contained **{total}** logged explanation event(s). The fallback distribution was {format_counter(fallback_counter)}, indicating how often the system returned a normal explanation versus a fallback state. The cognitive load distribution was {format_counter(load_counter)}, and the risk-level distribution was {format_counter(risk_counter)}.

Across the logged events, the mean cognitive load score was **{mean_score:.6f}**. The corresponding semantic complexity profile showed a mean readability of **{mean_readability:.6f}**, mean term density of **{mean_term_density:.6f}**, mean sentence length of **{mean_sentence_len:.6f}**, and mean information density of **{mean_info_density:.6f}**. Each explanation contained an average of **{mean_terms:.3f}** extracted terms, with **{mean_annotation_en:.3f}** English inline annotations and **{mean_annotation_zh:.3f}** Chinese inline annotations.

The adaptive presentation policy was also observable in the trace data. The system triggered `show_summary` in **{summary_rate:.3f}** of sessions, `show_inline_terms` in **{inline_rate:.3f}**, `collapse_technical` in **{collapse_rate:.3f}**, and `highlight_risk` in **{risk_rate:.3f}**. These results indicate that the interface behavior was linked to the output of the complexity-estimation module rather than being rendered as a fixed static explanation.

Overall, the trace analysis provides system-behavior evidence that the prototype implemented the intended pipeline: the LLM generated explanation content, the cognitive load model estimated explanation difficulty from the generated text, and the frontend adapted the explanation format accordingly. {sample_note} Direct claims about reduced user cognitive load should be supported by human-subject evaluation rather than by internal traces alone.
"""


def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


def ratio(rows: list[dict[str, str]], key: str) -> float:
    if not rows:
        return 0.0
    return sum(1 for row in rows if str(row.get(key, "")).lower() == "true") / len(rows)


def format_counter(counter: Counter) -> str:
    if not counter:
        return "none"
    return ", ".join(f"`{key}`={value}" for key, value in sorted(counter.items()))


def escape_xml(value: str) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def main() -> None:
    rows = load_rows(CSV_PATH)
    if not rows:
        print(f"No CSV rows found at {CSV_PATH}. Run summarize_medease_logs.py first.")
        return

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    load_counter = Counter(row.get("cognitive_load_label", "unknown") for row in rows)
    ui_rates = {
        "show_summary": ratio(rows, "show_summary"),
        "show_inline_terms": ratio(rows, "show_inline_terms"),
        "collapse_technical": ratio(rows, "collapse_technical"),
        "highlight_risk": ratio(rows, "highlight_risk"),
    }

    write_svg_bar_chart(
        LOAD_FIG_PATH,
        "MedEase Cognitive Load Distribution",
        ["low", "medium", "high"],
        [float(load_counter.get("low", 0)), float(load_counter.get("medium", 0)), float(load_counter.get("high", 0))],
        bar_color="#0F766E",
    )
    write_svg_bar_chart(
        UI_FIG_PATH,
        "MedEase UI Action Trigger Rates",
        list(ui_rates.keys()),
        list(ui_rates.values()),
        bar_color="#2563EB",
    )

    METHODS_RESULTS_PATH.write_text(build_methods_results(rows), encoding="utf-8")
    POLISHED_TEXT_PATH.write_text(build_polished_methods_results(rows), encoding="utf-8")

    print(f"Wrote methods/results draft to {METHODS_RESULTS_PATH}")
    print(f"Wrote polished methods/results text to {POLISHED_TEXT_PATH}")
    print(f"Wrote load distribution figure to {LOAD_FIG_PATH}")
    print(f"Wrote UI action figure to {UI_FIG_PATH}")


if __name__ == "__main__":
    main()
