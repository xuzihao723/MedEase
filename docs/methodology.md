# Methodology

## Data

The research version used an OpenMed/MedDialog-based online doctor-patient dialogue corpus. The public repository includes only a small anonymized sample file for demonstration.

## Cognitive Load Labels

Medical advice texts are categorized into:

- `low`: direct advice with limited terminology
- `medium`: moderate terminology, conditions, or follow-up information
- `high`: dense terminology, numerical findings, risk cues, or multiple instructions

## Features

Semantic complexity is represented through:

- Readability
- Terminology density
- Sentence length
- Information density

These features support interpretation and UI policy design. The deployed official classifier uses TF-IDF features with Logistic Regression.

## Model

The official model is a three-class cognitive-load classifier:

```text
TF-IDF (1,2-gram) + Logistic Regression
```

Official evaluation scope:

```text
metric_scope = manual_eval
```

Official results:

```text
accuracy = 0.828125
macro_f1 = 0.800466
```

## Adaptive Interface Policy

Predicted load is mapped to interface behavior:

- Low: minimal restructuring
- Medium: summary and terminology cues
- High: summary-first layout, glossary cues, risk emphasis, and collapsible technical details
