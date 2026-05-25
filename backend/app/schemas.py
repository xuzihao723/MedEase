from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


LanguageCode = Literal["en", "zh"]
RiskLevel = Literal["low", "medium", "high"]
FallbackType = Literal["none", "insufficient_info", "non_medical", "api_error"]


class LocalizedText(BaseModel):
    en: str = ""
    zh: str = ""


class MedicalTerm(BaseModel):
    id: str
    term: LocalizedText
    aliases: dict[Literal["en", "zh"], list[str]] = Field(default_factory=lambda: {"en": [], "zh": []})
    surface_forms: dict[Literal["en", "zh"], list[str]] = Field(default_factory=lambda: {"en": [], "zh": []})
    definition: LocalizedText
    why_it_matters: LocalizedText


class RiskPayload(BaseModel):
    level: RiskLevel
    reason: LocalizedText


class NextStepsPayload(BaseModel):
    en: list[str] = Field(default_factory=list)
    zh: list[str] = Field(default_factory=list)


class UiActions(BaseModel):
    show_summary: bool
    show_inline_terms: bool
    collapse_technical: bool
    highlight_risk: bool


class SemanticComplexityFeatures(BaseModel):
    readability: float = 0.0
    term_density: float = 0.0
    sentence_len: float = 0.0
    info_density: float = 0.0


class TextAnnotation(BaseModel):
    term_id: str
    start: int
    end: int
    surface: str


class LocalizedAnnotations(BaseModel):
    en: list[TextAnnotation] = Field(default_factory=list)
    zh: list[TextAnnotation] = Field(default_factory=list)


class ExplainRequest(BaseModel):
    input_text: str
    language: LanguageCode = "en"
    translate_to_zh: bool = True
    save_session: bool = False


class ExplainResponse(BaseModel):
    session_id: str
    created_at: str
    input_text: LocalizedText
    summary: LocalizedText
    explanation: LocalizedText
    terms: list[MedicalTerm] = Field(default_factory=list)
    technical_details: LocalizedText
    risk: RiskPayload
    next_steps: NextStepsPayload
    safety_notice: LocalizedText
    trust_note: LocalizedText
    cognitive_load_label: RiskLevel = "medium"
    cognitive_load_score: float = 0.5
    semantic_complexity_features: SemanticComplexityFeatures | None = None
    ui_actions: UiActions
    annotations: LocalizedAnnotations = Field(default_factory=LocalizedAnnotations)
    fallback_type: FallbackType = "none"
    fallback_message: LocalizedText | None = None

    @classmethod
    def new_session_id(cls) -> str:
        return f"sess_{uuid4().hex[:12]}"

    @classmethod
    def now_iso(cls) -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class LLMTerm(BaseModel):
    term_en: str
    term_zh: str = ""
    aliases_en: list[str] = Field(default_factory=list)
    aliases_zh: list[str] = Field(default_factory=list)
    definition_en: str
    definition_zh: str = ""
    why_it_matters_en: str
    why_it_matters_zh: str = ""


class LLMOutput(BaseModel):
    summary_en: str
    summary_zh: str = ""
    explanation_en: str
    explanation_zh: str = ""
    terms: list[LLMTerm] = Field(default_factory=list)
    technical_details_en: str = ""
    technical_details_zh: str = ""
    risk_level: RiskLevel
    risk_reason_en: str
    risk_reason_zh: str = ""
    next_steps_en: list[str] = Field(default_factory=list)
    next_steps_zh: list[str] = Field(default_factory=list)
    safety_notice_en: str = "This tool helps explain medical information. It does not replace professional medical advice."
    safety_notice_zh: str = "\u672c\u5de5\u5177\u4ec5\u5e2e\u52a9\u7406\u89e3\u533b\u5b66\u4fe1\u606f\uff0c\u4e0d\u80fd\u66ff\u4ee3\u4e13\u4e1a\u533b\u7597\u5efa\u8bae\u3002"
    trust_note_en: str = "AI-generated explanation for understanding only. It may be incomplete or incorrect."
    trust_note_zh: str = "\u6b64\u89e3\u91ca\u7531 AI \u751f\u6210\uff0c\u4ec5\u7528\u4e8e\u5e2e\u52a9\u7406\u89e3\uff0c\u53ef\u80fd\u5b58\u5728\u4e0d\u5b8c\u6574\u6216\u4e0d\u51c6\u786e\u4e4b\u5904\u3002"
