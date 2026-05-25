from __future__ import annotations

import re

from app.schemas import LocalizedText


MEDICAL_HINTS = [
    "blood",
    "test",
    "doctor",
    "note",
    "pain",
    "fever",
    "dose",
    "tablet",
    "mg",
    "g/dl",
    "ct",
    "mri",
    "scan",
    "report",
    "symptom",
    "hemoglobin",
    "anemia",
    "infection",
    "surgery",
    "wound",
    "urine",
    "nodule",
    "diagnosis",
    "treatment",
    "patient",
    "clinic",
    "clinician",
    "medication",
    "antibiotic",
    "follow-up",
    "follow up",
    "cholesterol",
    "glucose",
    "biopsy",
    "x-ray",
]

MEDICAL_HINTS_ZH = [
    "\u5fc3\u529f\u80fd",
    "\u5fc3\u5f8b",
    "\u51a0\u5fc3\u75c5",
    "\u80ba\u90e8",
    "\u7532\u72b6\u817a",
    "\u6c14\u77ed",
    "\u4e0b\u80a2\u6c34\u80bf",
    "\u6c34\u80bf",
    "\u5fc3\u810f",
    "\u6cf5\u8840",
    "\u8840\u538b",
    "\u8840\u7cd6",
    "\u8840\u7ea2\u86cb\u767d",
    "\u8d2b\u8840",
    "\u7ea2\u7ec6\u80de",
    "\u767d\u7ec6\u80de",
    "\u62a5\u544a",
    "\u68c0\u67e5",
    "\u5f71\u50cf",
    "ct",
    "mri",
    "\u7528\u836f",
    "\u836f\u7269",
    "\u5242\u91cf",
    "\u53d1\u70ed",
    "\u80f8\u75db",
    "\u547c\u5438\u56f0\u96be",
    "\u95e8\u8bca",
    "\u533b\u751f",
    "\u672f\u540e",
    "\u5207\u53e3",
    "\u6e17\u6db2",
]


def validate_input(input_text: str) -> tuple[bool, str | None]:
    stripped = input_text.strip()
    if not stripped:
        return False, "insufficient_info"
    if len(stripped) < 24:
        return False, "insufficient_info"

    lower = stripped.lower()
    if any(hint in lower for hint in MEDICAL_HINTS):
        return True, None
    if any(hint in stripped for hint in MEDICAL_HINTS_ZH):
        return True, None

    has_medical_shape = bool(re.search(r"\b(?:mg|ml|cm|mm|bp|hr|wbc|rbc|hgb|mcv)\b", lower))
    if has_medical_shape:
        return True, None

    return False, "non_medical"


def fallback_message(kind: str) -> LocalizedText:
    if kind == "insufficient_info":
        return LocalizedText(
            en="This is too brief to generate a structured medical explanation. Please add more context, such as symptoms, test results, duration, or a doctor's note.",
            zh="\u8fd9\u6bb5\u5185\u5bb9\u592a\u77ed\uff0c\u65e0\u6cd5\u751f\u6210\u7ed3\u6784\u5316\u533b\u5b66\u89e3\u91ca\u3002\u8bf7\u8865\u5145\u75c7\u72b6\u3001\u68c0\u67e5\u7ed3\u679c\u3001\u6301\u7eed\u65f6\u95f4\u6216\u533b\u751f\u8bf4\u660e\u7b49\u4fe1\u606f\u3002",
        )
    if kind == "non_medical":
        return LocalizedText(
            en="This does not look like medical text. Please paste a test result, doctor's note, medication instruction, or medical AI response.",
            zh="\u8fd9\u770b\u8d77\u6765\u4e0d\u50cf\u533b\u5b66\u6587\u672c\u3002\u8bf7\u7c98\u8d34\u68c0\u67e5\u62a5\u544a\u3001\u533b\u751f\u56de\u590d\u3001\u7528\u836f\u8bf4\u660e\u6216\u533b\u5b66 AI \u56de\u590d\u3002",
        )
    return LocalizedText(
        en="We could not generate an explanation right now. Please try again later.",
        zh="\u6682\u65f6\u65e0\u6cd5\u751f\u6210\u89e3\u91ca\uff0c\u8bf7\u7a0d\u540e\u91cd\u8bd5\u3002",
    )
