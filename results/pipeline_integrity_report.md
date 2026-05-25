# Pipeline Integrity Report

## Data Split Checks
- train rows: 48283
- validation rows: 4858
- pair overlap: 0
- doctor_reply overlap: 34
- user_query overlap: 1

## Label Checks
- manual_train labels file: data\annotation\manual_train_labels_combined_batch10_focus_lh.csv
- manual_eval labels file: data\annotation\manual_eval_labels.csv
- manual_train labels total rows: 5482
- manual_train labels valid rows: 5482
- manual_eval labels total rows: 320
- manual_eval labels valid rows: 320
- manual_eval label distribution: {'high': 104, 'medium': 178, 'low': 38}

## Metric Scope
- model_type: text
- eval_label_source: manual
- metric_scope: manual_eval

## Findings
- [PASS] train/val pair overlap = 0
- [PASS] no semantic+weak evaluation leakage detected
- [PASS] current metrics are from manual evaluation
- [PASS] manual eval labels >=200 (320)
- [PASS] manual eval labels contain all classes {'high': 104, 'medium': 178, 'low': 38}