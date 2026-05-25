# MedDialog 模型训练报告

- 时间: 2026-04-12T15:39:57
- 模型类型: **text**
- 指标范围: **manual_eval**
- 类别权重: **balanced**
- 数据源: https://huggingface.co/datasets/OpenMed/MedDialog
- 训练样本: 5482
- 评估样本: 320
- Accuracy: **0.8281**
- Macro-F1: **0.8005**
- LR C: **2.3**
- min_df: **1**
- Manual train labels loaded(rows): **5482**
- Manual eval labels loaded(rows): **320**
- 训练标签来源: **manual_only**
- 评估标签来源: **manual**
- High boost factor: **1**
- 决策阈值: high>=0.42, low>=0.45

## Classification Report
```text
              precision    recall  f1-score   support

        high     0.8476    0.8558    0.8517       104
         low     0.6591    0.7632    0.7073        38
      medium     0.8596    0.8258    0.8424       178

    accuracy                         0.8281       320
   macro avg     0.7888    0.8149    0.8005       320
weighted avg     0.8319    0.8281    0.8294       320
```

## Confusion Matrix (rows=true, cols=pred)
```text
labels: ['low', 'medium', 'high']
[[ 29   9   0]
 [ 15 147  16]
 [  0  15  89]]
```