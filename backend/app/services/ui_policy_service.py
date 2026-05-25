from __future__ import annotations

from app.schemas import LLMOutput, UiActions


def build_ui_actions(output: LLMOutput, complexity_label: str | None = None) -> UiActions:
    explanation_len = len(output.explanation_en.strip())
    detail_len = len(output.technical_details_en.strip())
    term_count = len(output.terms)

    label = complexity_label or "medium"

    highlight_risk = output.risk_level in {"medium", "high"}
    show_summary = (
        output.risk_level == "high"
        or label in {"medium", "high"}
        or explanation_len >= 280
        or detail_len >= 180
    )
    show_inline_terms = (
        output.risk_level == "high"
        or label in {"medium", "high"}
        or term_count >= 2
        or explanation_len >= 220
    )
    collapse_technical = (
        output.risk_level == "high"
        or label == "high"
        or detail_len >= 160
        or explanation_len >= 360
    )

    return UiActions(
        show_summary=show_summary,
        show_inline_terms=show_inline_terms,
        collapse_technical=collapse_technical,
        highlight_risk=highlight_risk,
    )
