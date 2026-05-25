from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def train(input_csv: Path, output_model: Path) -> None:
    data = pd.read_csv(input_csv)
    required = {"text", "label"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    model = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(lowercase=True, ngram_range=(1, 2), min_df=1)),
            ("clf", LogisticRegression(max_iter=300, class_weight="balanced")),
        ]
    )
    model.fit(data["text"].astype(str), data["label"].astype(str))
    output_model.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_model)
    print(f"saved model: {output_model}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a lightweight cognitive-load classifier on sample data.")
    parser.add_argument("--input", default="data/sample_anonymized_data.csv")
    parser.add_argument("--out", default="results/sample_model.joblib")
    args = parser.parse_args()
    train(Path(args.input), Path(args.out))


if __name__ == "__main__":
    main()
