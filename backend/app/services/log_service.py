from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import settings
from app.schemas import ExplainRequest, ExplainResponse


class LogService:
    def __init__(self) -> None:
        self.enabled = settings.logging_enabled
        self.logs_dir = settings.logs_dir

    def log_explain(self, request: ExplainRequest, response: ExplainResponse, *, complexity_model_ready: bool) -> None:
        if not self.enabled:
            return

        self.logs_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "event": "explain",
            "logged_at": self._utc_now(),
            "provider": "closeai",
            "model": settings.closeai_model,
            "complexity_model_ready": complexity_model_ready,
            "session_id": response.session_id,
            "request": {
                "language": request.language,
                "translate_to_zh": request.translate_to_zh,
                "save_session": request.save_session,
                "input_length": len(request.input_text or ""),
                "input_sha256": self._sha256(request.input_text or ""),
                "contains_cjk": bool(any("\u4e00" <= ch <= "\u9fff" for ch in (request.input_text or ""))),
            },
            "response": {
                "created_at": response.created_at,
                "fallback_type": response.fallback_type,
                "risk_level": response.risk.level,
                "terms_count": len(response.terms),
                "annotation_count_en": len(response.annotations.en),
                "annotation_count_zh": len(response.annotations.zh),
                "summary_length_en": len(response.summary.en or ""),
                "summary_length_zh": len(response.summary.zh or ""),
                "explanation_length_en": len(response.explanation.en or ""),
                "explanation_length_zh": len(response.explanation.zh or ""),
                "technical_details_length_en": len(response.technical_details.en or ""),
                "technical_details_length_zh": len(response.technical_details.zh or ""),
                "next_steps_count_en": len(response.next_steps.en),
                "next_steps_count_zh": len(response.next_steps.zh),
                "cognitive_load_label": response.cognitive_load_label,
                "cognitive_load_score": response.cognitive_load_score,
                "semantic_complexity_features": (
                    response.semantic_complexity_features.model_dump()
                    if response.semantic_complexity_features is not None
                    else None
                ),
                "ui_actions": response.ui_actions.model_dump(),
            },
        }
        self._append_jsonl(self.logs_dir / "explain-events.jsonl", payload)

    def _append_jsonl(self, path: Path, payload: dict[str, Any]) -> None:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")

    @staticmethod
    def _sha256(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
