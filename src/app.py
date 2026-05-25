from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from preprocessing import feature_dict


app = FastAPI(title="MedEase Sample API")


class ExplainRequest(BaseModel):
    text: str


def heuristic_label(features: dict[str, float]) -> str:
    if features["term_density"] > 0.12 or features["info_density"] > 0.18 or features["sentence_len"] > 28:
        return "high"
    if features["term_density"] > 0.05 or features["sentence_len"] > 18:
        return "medium"
    return "low"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/explain")
def explain(request: ExplainRequest) -> dict[str, object]:
    features = feature_dict(request.text)
    label = heuristic_label(features)
    return {
        "cognitive_load_label": label,
        "semantic_complexity_features": features,
        "ui_actions": {
            "show_summary": label in {"medium", "high"},
            "show_inline_terms": label in {"medium", "high"},
            "collapse_technical": label == "high",
            "highlight_risk": "urgent" in request.text.lower() or "emergency" in request.text.lower(),
        },
    }
