# Baseline Leaderboard (manual_eval)

> Only rows with `eval_samples=320` and `comparable_eval320=yes` should be directly compared with official manual_eval scores.

| baseline_name | model_id | metric_scope | eval_samples | comparable_eval320 | accuracy | macro_f1 | confusion_matrix |
|---|---|---:|---:|---:|---:|---:|---|
| official_lr_reference | tfidf_lr_manual_only | manual_eval | 320 | yes | 0.828125 | 0.800466 | `[[29, 9, 0], [15, 147, 16], [0, 15, 89]]` |
| rule_baseline | semantic_linear_threshold_rule | manual_eval | 320 | yes | 0.45 | 0.35472 | `[[36, 2, 0], [68, 107, 3], [5, 98, 1]]` |
| transformer_baseline | bert-base-uncased | manual_eval | 320 | yes | 0.88125 | 0.866722 | `[[30, 8, 0], [3, 173, 2], [0, 25, 79]]` |
| transformer_baseline | roberta-base | manual_eval | 320 | yes | 0.85 | 0.837872 | `[[31, 7, 0], [4, 173, 1], [0, 36, 68]]` |
| llm_fewshot_baseline | llama-3.1-8b-instant | manual_eval | 320 | yes | 0.26875 | 0.229533 | `[[36, 2, 0], [132, 46, 0], [38, 62, 4]]` |