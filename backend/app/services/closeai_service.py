from __future__ import annotations

import json

import httpx
from openai import OpenAI

from app.config import settings
from app.schemas import ExplainRequest, LLMOutput


SYSTEM_PROMPT = """You are a medical text explanation assistant.

Your role is to help ordinary users understand medical text. You are not a diagnosis assistant.

Return JSON only. Do not return Markdown. Do not include any text outside JSON.

Requirements:
1. Explain the medical text in plain English.
2. Also provide Chinese display translations for all user-facing content.
3. Do not make certain diagnoses.
4. Do not exaggerate risk.
5. Do not invent test results, patient history, or treatment plans.
6. If information is limited, stay cautious and say so.
7. If red-flag symptoms are implied, advise prompt clinical evaluation.
8. Use the same core medical concepts in both explanation_en and explanation_zh.
9. Every listed term should appear explicitly in both language explanations, either as the canonical term or a listed alias.

Return this exact JSON shape:
{
  "summary_en": "string",
  "summary_zh": "string",
  "explanation_en": "string",
  "explanation_zh": "string",
  "terms": [
    {
      "term_en": "string",
      "term_zh": "string",
      "aliases_en": ["string"],
      "aliases_zh": ["string"],
      "definition_en": "string",
      "definition_zh": "string",
      "why_it_matters_en": "string",
      "why_it_matters_zh": "string"
    }
  ],
  "technical_details_en": "string",
  "technical_details_zh": "string",
  "risk_level": "low | medium | high",
  "risk_reason_en": "string",
  "risk_reason_zh": "string",
  "next_steps_en": ["string"],
  "next_steps_zh": ["string"],
  "safety_notice_en": "string",
  "safety_notice_zh": "string",
  "trust_note_en": "string",
  "trust_note_zh": "string"
}
"""


class CloseAIService:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=settings.closeai_api_key,
            base_url=settings.closeai_base_url,
            timeout=settings.request_timeout_seconds,
            http_client=httpx.Client(
                timeout=settings.request_timeout_seconds,
                trust_env=False,
            ),
        )

    def _call_model(self, request: ExplainRequest, model_name: str) -> LLMOutput:
        response = self.client.chat.completions.create(
            model=model_name,
            temperature=settings.closeai_temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Explain this medical text as JSON only.\n\n"
                        f"Input text:\n{request.input_text.strip()}\n\n"
                        f"Primary language: {request.language}\n"
                        f"Return Chinese translation fields: {'yes' if request.translate_to_zh else 'no'}\n"
                        "For aliases_en and aliases_zh, include exact surface forms that appear in the explanation text when possible.\n"
                        "If the explanation uses a shorter form, include that shorter form in aliases."
                    ),
                },
            ],
        )
        content = response.choices[0].message.content or "{}"
        return LLMOutput.model_validate(json.loads(content))

    def explain(self, request: ExplainRequest) -> LLMOutput:
        if not settings.closeai_ready:
            raise RuntimeError("CloseAI API key is not configured.")

        attempts: list[str] = [settings.closeai_model]
        if settings.closeai_fallback_model and settings.closeai_fallback_model != settings.closeai_model:
            attempts.append(settings.closeai_fallback_model)

        last_error: Exception | None = None
        for model_name in attempts:
            try:
                return self._call_model(request, model_name)
            except Exception as exc:  # noqa: BLE001
                last_error = exc

        assert last_error is not None
        raise last_error
