from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score


LABELS = ["low", "medium", "high"]


def evaluate(input_csv: Path, model_path: Path, output_json: Path) -> None:
    data = pd.read_csv(input_csv)
    model = joblib.load(model_path)
    y_true = data["label"].astype(str).tolist()
    y_pred = model.predict(data["text"].astype(str)).tolist()

    metrics = {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 6),
        "macro_f1": round(float(f1_score(y_true, y_pred, average="macro", zero_division=0)), 6),
        "labels": LABELS,
        "confusion_matrix": confusion_matrix(y_true, y_pred, labels=LABELS).tolist(),
        "note": "Sample-data demo metrics only. Official paper metrics are in results/metrics.json.",
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(json.dumps(metrics, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the sample cognitive-load classifier.")
    parser.add_argument("--input", default="data/sample_anonymized_data.csv")
    parser.add_argument("--model", default="results/sample_model.joblib")
    parser.add_argument("--out", default="results/sample_metrics.json")
    args = parser.parse_args()
    evaluate(Path(args.input), Path(args.model), Path(args.out))


if __name__ == "__main__":
    main()
