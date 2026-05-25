from __future__ import annotations

import re

from app.config import settings
from app.schemas import (
    ExplainRequest,
    ExplainResponse,
    LLMOutput,
    LocalizedAnnotations,
    LocalizedText,
    MedicalTerm,
    NextStepsPayload,
    RiskPayload,
    TextAnnotation,
)
from app.services.closeai_service import CloseAIService
from app.services.complexity_service import ComplexityService
from app.services.log_service import LogService
from app.services.ui_policy_service import build_ui_actions
from app.services.validation_service import fallback_message, validate_input


DEFAULT_SAFETY = LocalizedText(
    en="This tool helps explain medical information. It does not replace professional medical advice.",
    zh="\u672c\u5de5\u5177\u4ec5\u5e2e\u52a9\u7406\u89e3\u533b\u5b66\u4fe1\u606f\uff0c\u4e0d\u80fd\u66ff\u4ee3\u4e13\u4e1a\u533b\u7597\u5efa\u8bae\u3002",
)

DEFAULT_TRUST = LocalizedText(
    en="AI-generated explanation for understanding only. It may be incomplete or incorrect.",
    zh="\u6b64\u89e3\u91ca\u7531 AI \u751f\u6210\uff0c\u4ec5\u7528\u4e8e\u5e2e\u52a9\u7406\u89e3\uff0c\u53ef\u80fd\u5b58\u5728\u4e0d\u5b8c\u6574\u6216\u4e0d\u51c6\u786e\u4e4b\u5904\u3002",
)


class ExplainService:
    def __init__(self) -> None:
        self.closeai = CloseAIService()
        self.complexity = ComplexityService()
        self.logger = LogService()

    def fallback_response(self, request: ExplainRequest, kind: str) -> ExplainResponse:
        message = fallback_message(kind)
        input_text = LocalizedText(en=request.input_text.strip(), zh=request.input_text.strip())
        empty_output = LLMOutput(summary_en="", explanation_en="", risk_level="low", risk_reason_en="")
        response = ExplainResponse(
            session_id=ExplainResponse.new_session_id(),
            created_at=ExplainResponse.now_iso(),
            input_text=input_text,
            summary=LocalizedText(),
            explanation=LocalizedText(),
            terms=[],
            technical_details=LocalizedText(),
            risk=RiskPayload(level="low", reason=LocalizedText()),
            next_steps=NextStepsPayload(),
            safety_notice=DEFAULT_SAFETY,
            trust_note=DEFAULT_TRUST,
            cognitive_load_label="medium",
            cognitive_load_score=0.5,
            semantic_complexity_features=self.complexity.compute_features("", []),
            ui_actions=build_ui_actions(empty_output, "medium"),
            annotations=LocalizedAnnotations(),
            fallback_type=kind,
            fallback_message=message,
        )
        self.logger.log_explain(request, response, complexity_model_ready=self.complexity.ready)
        return response

    def explain(self, request: ExplainRequest) -> ExplainResponse:
        valid, reason = validate_input(request.input_text)
        if not valid and reason:
            return self.fallback_response(request, reason)

        try:
            output = self.closeai.explain(request)
        except Exception:  # noqa: BLE001
            return self.fallback_response(request, "api_error")

        raw_terms = [build_term_payload(index, term, output) for index, term in enumerate(output.terms, start=1)]
        shared_terms = retain_shared_terms(raw_terms)
        annotations = build_annotations(
            explanation_en=output.explanation_en,
            explanation_zh=output.explanation_zh or output.explanation_en,
            terms=shared_terms,
        )
        complexity_input = build_complexity_input(output, shared_terms)
        complexity = self.complexity.predict(
            complexity_input,
            term_candidates=[
                *[term.term.en for term in shared_terms],
                *[alias for term in shared_terms for alias in term.aliases["en"]],
            ],
        )
        ui_actions = build_ui_actions(output, complexity.label)

        response = ExplainResponse(
            session_id=ExplainResponse.new_session_id(),
            created_at=ExplainResponse.now_iso(),
            input_text=LocalizedText(en=request.input_text.strip(), zh=request.input_text.strip()),
            summary=LocalizedText(en=output.summary_en, zh=output.summary_zh or output.summary_en),
            explanation=LocalizedText(en=output.explanation_en, zh=output.explanation_zh or output.explanation_en),
            terms=shared_terms,
            technical_details=LocalizedText(
                en=output.technical_details_en,
                zh=output.technical_details_zh or output.technical_details_en,
            ),
            risk=RiskPayload(
                level=output.risk_level,
                reason=LocalizedText(en=output.risk_reason_en, zh=output.risk_reason_zh or output.risk_reason_en),
            ),
            next_steps=NextStepsPayload(en=output.next_steps_en, zh=output.next_steps_zh or output.next_steps_en),
            safety_notice=LocalizedText(
                en=output.safety_notice_en or DEFAULT_SAFETY.en,
                zh=output.safety_notice_zh or DEFAULT_SAFETY.zh,
            ),
            trust_note=LocalizedText(
                en=output.trust_note_en or DEFAULT_TRUST.en,
                zh=output.trust_note_zh or DEFAULT_TRUST.zh,
            ),
            cognitive_load_label=complexity.label,
            cognitive_load_score=complexity.score,
            semantic_complexity_features=complexity.features,
            ui_actions=ui_actions,
            annotations=annotations,
            fallback_type="none",
            fallback_message=None,
        )
        self.logger.log_explain(request, response, complexity_model_ready=complexity.ready)
        return response


def provider_status(complexity_model_ready: bool) -> dict[str, str | bool]:
    return {
        "status": "ok",
        "provider": "closeai",
        "model": settings.closeai_model,
        "ready": settings.closeai_ready,
        "complexity_model_ready": complexity_model_ready,
    }


def build_complexity_input(output: LLMOutput, terms: list[MedicalTerm]) -> str:
    return "\n".join(
        part.strip()
        for part in [
            output.explanation_en,
            output.technical_details_en,
            " ".join(term.term.en for term in terms),
            " ".join(alias for term in terms for alias in term.aliases["en"]),
        ]
        if part and part.strip()
    )


def build_term_payload(index: int, term, output: LLMOutput) -> MedicalTerm:
    aliases = build_aliases(term)
    return MedicalTerm(
        id=f"term_{index}",
        term=LocalizedText(en=term.term_en, zh=term.term_zh or term.term_en),
        aliases=aliases,
        surface_forms=build_surface_forms(
            aliases=aliases,
            explanation_en=output.explanation_en,
            explanation_zh=output.explanation_zh or output.explanation_en,
        ),
        definition=LocalizedText(en=term.definition_en, zh=term.definition_zh or term.definition_en),
        why_it_matters=LocalizedText(
            en=term.why_it_matters_en,
            zh=term.why_it_matters_zh or term.why_it_matters_en,
        ),
    )


def build_aliases(term) -> dict[str, list[str]]:
    en: list[str] = []
    zh: list[str] = []

    def push(bucket: list[str], value: str) -> None:
        cleaned = (value or "").strip()
        if cleaned and cleaned not in bucket:
            bucket.append(cleaned)

    push(en, term.term_en)
    push(zh, term.term_zh)

    for value in term.aliases_en:
        push(en, value)
    for value in term.aliases_zh:
        push(zh, value)

    if "(" in term.term_en and ")" in term.term_en:
        main = term.term_en.split("(", 1)[0].strip()
        inside = term.term_en.split("(", 1)[1].split(")", 1)[0].strip()
        push(en, main)
        push(en, inside)

    if term.term_zh.endswith("\u68c0\u67e5"):
        push(zh, term.term_zh[:-2])

    return {"en": en, "zh": zh}


def build_surface_forms(aliases: dict[str, list[str]], explanation_en: str, explanation_zh: str) -> dict[str, list[str]]:
    return {
        "en": find_surface_forms(explanation_en, aliases.get("en", []), ascii_mode=True),
        "zh": find_surface_forms(explanation_zh, aliases.get("zh", []), ascii_mode=False),
    }


def find_surface_forms(text: str, candidates: list[str], ascii_mode: bool) -> list[str]:
    if not text.strip():
        return []

    found: list[str] = []
    lower_text = text.lower()

    for candidate in sorted({item.strip() for item in candidates if item and item.strip()}, key=len, reverse=True):
        if ascii_mode:
            pattern = re.compile(rf"\b{re.escape(candidate.lower())}\b")
            match = pattern.search(lower_text)
            if match:
                snippet = text[match.start():match.end()]
                if snippet and snippet not in found:
                    found.append(snippet)
                continue
        else:
            start = text.find(candidate)
            if start != -1:
                snippet = text[start:start + len(candidate)]
                if snippet and snippet not in found:
                    found.append(snippet)

    return found


def build_annotations(explanation_en: str, explanation_zh: str, terms: list[MedicalTerm]) -> LocalizedAnnotations:
    return LocalizedAnnotations(
        en=find_annotations(explanation_en, terms, "en"),
        zh=find_annotations(explanation_zh, terms, "zh"),
    )


def find_annotations(text: str, terms: list[MedicalTerm], language: str) -> list[TextAnnotation]:
    candidates: list[tuple[str, str]] = []
    for term in terms:
        for value in term.surface_forms.get(language, []):
            cleaned = (value or "").strip()
            if cleaned:
                candidates.append((term.id, cleaned))

    matches: list[TextAnnotation] = []
    occupied: list[tuple[int, int]] = []
    seen_term_ids: set[str] = set()
    search_text = text.lower() if language == "en" else text

    for term_id, surface in sorted(candidates, key=lambda item: len(item[1]), reverse=True):
        if term_id in seen_term_ids:
            continue
        search_value = surface.lower() if language == "en" else surface
        cursor = 0
        while cursor < len(text):
            start = search_text.find(search_value, cursor)
            if start == -1:
                break
            end = start + len(surface)
            if all(end <= left or start >= right for left, right in occupied):
                occupied.append((start, end))
                matches.append(TextAnnotation(term_id=term_id, start=start, end=end, surface=text[start:end]))
                seen_term_ids.add(term_id)
                break
            cursor = end

    matches.sort(key=lambda item: item.start)
    return matches


def retain_shared_terms(terms: list[MedicalTerm]) -> list[MedicalTerm]:
    return [
        term
        for term in terms
        if bool(term.surface_forms.get("en")) and bool(term.surface_forms.get("zh"))
    ]
