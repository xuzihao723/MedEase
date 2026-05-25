# Limitations and Ethics

## Scope Limitations

MedEase is not a diagnosis system. It is a comprehension-support prototype for medical advice text.

The system should not be used to make clinical decisions without professional medical review.

## Data Limitations

The public repository includes only anonymized sample data. The full research dataset and manual labels are not included in this public version.

## Model Limitations

The deployed classifier estimates cognitive load from text. It does not verify clinical correctness, factuality, or safety of the advice.

Transformer baselines achieved higher offline scores, while the deployed Logistic Regression model was selected for interpretability and lightweight integration.

## User Study Limitations

The A/B study was conducted with 30 participants. Larger and more diverse studies are needed before making broad general claims.

## Responsible AI Position

The goal is to make medical AI outputs easier to understand, not to replace clinicians. The interface includes safety and trust notes to reduce overreliance.
