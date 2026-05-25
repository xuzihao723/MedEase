from __future__ import annotations

import re
from dataclasses import asdict, dataclass


MEDICAL_TERMS = {
    "anemia",
    "ferritin",
    "hemoglobin",
    "pulmonary",
    "nodule",
    "ct",
    "ecg",
    "tachycardia",
    "nt-probnp",
    "diarrhea",
    "rash",
    "ultrasound",
    "blood pressure",
}


@dataclass
class SemanticFeatures:
    readability: float
    term_density: float
    sentence_len: float
    info_density: float


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def split_sentences(text: str) -> list[str]:
    return [part.strip() for part in re.split(r"[.!?;]+", text) if part.strip()]


def token_count(text: str) -> int:
    return max(1, len(re.findall(r"[A-Za-z0-9.\-/%]+", text)))


def count_terms(text: str) -> int:
    lowered = text.lower()
    total = 0
    for term in MEDICAL_TERMS:
        total += len(re.findall(rf"\b{re.escape(term)}\b", lowered))
    return total


def compute_features(text: str) -> SemanticFeatures:
    clean = normalize_text(text)
    sentences = split_sentences(clean) or [clean]
    total_tokens = token_count(clean)
    avg_sentence_len = sum(token_count(sentence) for sentence in sentences) / len(sentences)
    term_density = count_terms(clean) / total_tokens
    info_markers = len(re.findall(r"\d|[%/\-]|[,;:()]", clean))
    info_density = info_markers / total_tokens
    readability = max(0.0, min(100.0, 100.0 - (avg_sentence_len * 2.2 + term_density * 120 + info_density * 40)))
    return SemanticFeatures(
        readability=round(readability, 4),
        term_density=round(term_density, 6),
        sentence_len=round(avg_sentence_len, 4),
        info_density=round(info_density, 6),
    )


def feature_dict(text: str) -> dict[str, float]:
    return asdict(compute_features(text))
