# AI Medical Advice Comprehensibility

This repository contains a research prototype for improving the comprehensibility of AI-mediated medical advice. The project connects text complexity analysis, cognitive-load classification, and an adaptive explanation interface for non-expert users.

## Problem

LLM-generated medical explanations can sound fluent and professional while remaining difficult for non-expert users to understand. Dense terminology, compressed reasoning, numerical thresholds, and risk cues can increase cognitive load and make follow-up actions harder to identify.

## Goal

Build a cognitive-load-aware explanation system that classifies the complexity of medical advice and adapts the interface accordingly.

## What This Project Demonstrates

- A medical-advice cognitive-load classifier using TF-IDF and Logistic Regression.
- Semantic complexity features: readability, terminology density, sentence length, and information density.
- A frontend interface that adapts presentation with plain-language summaries, inline term explanations, risk cues, and collapsible technical details.
- A FastAPI backend that connects LLM-generated explanation content with cognitive-load estimation and UI policy actions.
- A human-subject A/B evaluation showing improved comprehension, lower workload, and shorter task time.

## Key Results

| Component | Result |
|---|---:|
| Official classifier accuracy | 0.828125 |
| Official classifier macro-F1 | 0.800466 |
| Manual evaluation set | 320 samples |
| A/B study participants | 30 |
| Comprehension accuracy | 0.7600 to 0.8845 |
| NASA-TLX workload | 70.306 to 48.945 |
| Task completion time | 293.967 s to 257.233 s |

The official classifier results use `manual_eval`. The A/B study was conducted as a within-subject comparison between a conventional display and an adaptive explanation interface.

## Repository Structure

```text
backend/      FastAPI backend for explanation, complexity estimation, and UI policy
frontend/     Static MedEase interface
src/          Lightweight reproducible preprocessing/training/evaluation scripts
scripts/      Research analysis utilities
data/         Small anonymized sample data only
results/      Metrics, summaries, and exported result tables
docs/         Project overview, methodology, study design, limitations and ethics
paper/        Abstract and project summary material
notebooks/    Notebook placeholders and analysis guide
demo/         Screenshots folder for GitHub display
models/       Trained cognitive-load classifier artifact
```

## Quick Start

### Frontend

Open:

```text
frontend/index.html
```

The frontend can run as a static file. By default, it is configured for the local API endpoint:

```text
http://127.0.0.1:8000/api/explain
```

### Backend

Create a local environment file from the template:

```powershell
copy backend\.env.example backend\.env
```

Install backend dependencies:

```powershell
pip install -r backend\requirements-backend.txt
```

Run the backend:

```powershell
powershell -ExecutionPolicy Bypass -File backend\run_backend.ps1
```

Health check:

```text
http://127.0.0.1:8000/api/health
```

## Reproduce the Lightweight Classifier Demo

The public repository includes a small anonymized sample dataset for demonstration. It is not the full research dataset.

```powershell
python src\train_classifier.py --input data\sample_anonymized_data.csv --out results\sample_model.joblib
python src\evaluate.py --input data\sample_anonymized_data.csv --model results\sample_model.joblib --out results\sample_metrics.json
```

## Research Scope

This is a comprehensibility and HCI research prototype. It is not a clinical diagnosis system and does not replace professional medical judgment.

## Responsible AI Notes

- Raw medical text and API keys are not included.
- The public dataset is a small anonymized demonstration sample.
- The system is designed to support understanding, not to make clinical decisions.
- Internal trace logs should be treated as system-behavior evidence, not direct evidence of user benefit.

## Suggested Citation

If referencing this project:

```text
Xu, Z. MedEase: From Semantic Complexity to Adaptive Explanation for AI-Mediated Medical Advice Comprehensibility. Research prototype, 2026.
```
