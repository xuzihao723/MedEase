from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import joblib

from app.schemas import SemanticComplexityFeatures


MODEL_PATH = Path(__file__).resolve().parents[3] / "models" / "cognitive_load_classifier.joblib"


@dataclass
class ComplexityResult:
    label: str
    score: float
    features: SemanticComplexityFeatures
    ready: bool


class ComplexityService:
    def __init__(self) -> None:
        self._bundle = None
        self._pipeline = None
        self._labels: list[str] = []
        self._decision_thresholds: dict[str, float] = {}
        self.ready = False
        self._load()

    def _load(self) -> None:
        if not MODEL_PATH.exists():
            return
        try:
            bundle = joblib.load(MODEL_PATH)
        except Exception:  # noqa: BLE001
            return
        self._bundle = bundle
        self._pipeline = bundle.get("model") if isinstance(bundle, dict) else bundle
        self._labels = list(bundle.get("labels", [])) if isinstance(bundle, dict) else []
        self._decision_thresholds = dict(bundle.get("decision_thresholds", {})) if isinstance(bundle, dict) else {}
        self.ready = self._pipeline is not None

    def predict(self, text: str, term_candidates: list[str] | None = None) -> ComplexityResult:
        features = self.compute_features(text, term_candidates or [])

        if not self.ready or not text.strip():
            return ComplexityResult(label="medium", score=0.5, features=features, ready=False)

        model = self._pipeline
        label = str(model.predict([text])[0]).lower().strip()
        score = 0.5

        if hasattr(model, "predict_proba"):
            try:
                probs = model.predict_proba([text])[0]
                classes = [str(item).lower() for item in getattr(model, "classes_", self._labels)]
                if classes:
                    idx = {name: i for i, name in enumerate(classes)}
                    score = float(probs[idx.get(label, 0)])
                    high_threshold = self._decision_thresholds.get("high")
                    low_threshold = self._decision_thresholds.get("low")

                    if high_threshold is not None and "high" in idx and float(probs[idx["high"]]) >= float(high_threshold):
                        label = "high"
                        score = float(probs[idx["high"]])
                    elif low_threshold is not None and "low" in idx and float(probs[idx["low"]]) >= float(low_threshold):
                        label = "low"
                        score = float(probs[idx["low"]])
            except Exception:  # noqa: BLE001
                score = 0.5

        if label not in {"low", "medium", "high"}:
            label = "medium"

        return ComplexityResult(label=label, score=round(float(score), 6), features=features, ready=True)

    def compute_features(self, text: str, term_candidates: list[str]) -> SemanticComplexityFeatures:
        clean = normalize_text(text)
        sentences = split_sentences(clean)
        if not sentences:
            sentences = [clean] if clean else [""]

        total_tokens = max(token_count(clean), 1)
        sentence_lens = [max(token_count(sentence), 1) for sentence in sentences]
        avg_sentence_len = sum(sentence_lens) / len(sentence_lens)

        med_terms = count_candidate_terms(clean, term_candidates)
        term_density = med_terms / total_tokens

        numeric_markers = len(re.findall(r"\d", clean)) + len(re.findall(r"[%/\-]", clean))
        punct_markers = len(re.findall(r"[，,：:；;（）（)\(、]", clean))
        info_density = (numeric_markers + punct_markers) / total_tokens

        raw_readability_penalty = avg_sentence_len * 2.2 + term_density * 120 + info_density * 40
        readability = max(0.0, min(100.0, 100.0 - raw_readability_penalty))

        return SemanticComplexityFeatures(
            readability=round(readability, 4),
            term_density=round(term_density, 6),
            sentence_len=round(avg_sentence_len, 4),
            info_density=round(info_density, 6),
        )


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"[。！？!?;；\n]+", text)
    return [part.strip() for part in parts if part.strip()]


def token_count(text: str) -> int:
    zh_chars = re.findall(r"[\u4e00-\u9fff]", text)
    en_words = re.findall(r"[A-Za-z0-9.\-/%]+", text)
    return len(zh_chars) + len(en_words)


def count_candidate_terms(text: str, term_candidates: list[str]) -> int:
    total = 0
    normalized = []
    for candidate in term_candidates:
        cleaned = (candidate or "").strip()
        if cleaned and cleaned not in normalized:
            normalized.append(cleaned)

    for term in normalized:
        if re.search(r"[A-Za-z]", term):
            total += len(re.findall(rf"\b{re.escape(term)}\b", text, flags=re.IGNORECASE))
        else:
            total += text.count(term)
    return total
