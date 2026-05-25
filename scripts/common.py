import csv
import math
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
REPORTS_DIR = PROJECT_ROOT / "reports"
LOGS_DIR = PROJECT_ROOT / "logs"

MEDICAL_TERMS = [
    "高血压", "甘油三酯", "血脂", "胸片", "糖化血红蛋白", "OGTT", "甲状腺", "窦性心动过速",
    "脂肪肝", "痛风", "eGFR", "咽鼓管", "中耳炎", "CBT-I", "TI-RADS", "FNA", "铁蛋白",
    "转铁蛋白", "靶器官", "门诊", "认知负荷", "胃食管反流", "PPI", "HbA1c", "FPG",
    "分层", "影像学", "代谢", "干预", "病因学"
]


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def normalize_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def split_sentences(text: str):
    parts = re.split(r"[。！？!?;；\n]+", text)
    return [p.strip() for p in parts if p.strip()]


def token_count(text: str) -> int:
    zh_chars = re.findall(r"[\u4e00-\u9fff]", text)
    en_words = re.findall(r"[A-Za-z0-9\.\-/%]+", text)
    return len(zh_chars) + len(en_words)


def count_med_terms(text: str) -> int:
    total = 0
    for term in MEDICAL_TERMS:
        total += len(re.findall(re.escape(term), text, flags=re.IGNORECASE))
    return total


def compute_features(text: str):
    clean = normalize_text(text)
    sentences = split_sentences(clean)
    if not sentences:
        sentences = [clean] if clean else [""]

    total_tokens = max(token_count(clean), 1)
    sentence_lens = [max(token_count(s), 1) for s in sentences]
    avg_sentence_len = sum(sentence_lens) / len(sentence_lens)

    med_terms = count_med_terms(clean)
    term_density = med_terms / total_tokens

    numeric_markers = len(re.findall(r"\d", clean)) + len(re.findall(r"[%/\-]", clean))
    punct_markers = len(re.findall(r"[，,：:；;（）（)\(、]", clean))
    info_density = (numeric_markers + punct_markers) / total_tokens

    raw_readability_penalty = avg_sentence_len * 2.2 + term_density * 120 + info_density * 40
    readability = max(0.0, min(100.0, 100.0 - raw_readability_penalty))

    return {
        "readability": round(readability, 4),
        "term_density": round(term_density, 6),
        "sentence_len": round(avg_sentence_len, 4),
        "info_density": round(info_density, 6),
    }


def difficulty_score(readability: float, term_density: float, sentence_len: float, info_density: float):
    readability_component = 1.0 - max(0.0, min(readability / 100.0, 1.0))
    term_component = min(term_density / 0.25, 1.0)
    sentence_component = min(sentence_len / 60.0, 1.0)
    info_component = min(info_density / 0.40, 1.0)

    score = (
        0.15 * readability_component
        + 0.35 * term_component
        + 0.25 * sentence_component
        + 0.25 * info_component
    )
    return round(max(0.0, min(score, 1.0)), 6)


def ensure_dirs():
    for p in (REPORTS_DIR, LOGS_DIR):
        p.mkdir(parents=True, exist_ok=True)


def mean(values):
    return sum(values) / len(values) if values else 0.0


def std(values):
    if len(values) < 2:
        return 0.0
    mu = mean(values)
    var = sum((x - mu) ** 2 for x in values) / (len(values) - 1)
    return math.sqrt(var)


def normal_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0
