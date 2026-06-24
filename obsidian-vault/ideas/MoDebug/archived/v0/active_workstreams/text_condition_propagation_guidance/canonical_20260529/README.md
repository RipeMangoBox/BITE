---
title: "MoDebug canonical 2026-05-29 阅读入口"
created: 2026-05-29
status: active
role: index
tags:
  - MoDebug
  - text_condition_propagation
  - canonical_audit
---

# MoDebug canonical 2026-05-29 阅读入口

本目录是 MoDebug 文本条件传播诊断审计的当前 canonical evidence bundle。当前结论是：审计部分有效，但旧 `null_text="This is a null prompt with no semantic meaning."` 的 semantic-null delta 已标为 `blocked / historical diagnostic only`，只能保留为诊断记录，不能支持稳健主结论、因果或机制 claim。

## 从这里开始

1. 先读 `canonical_audit_report.md`：正式报告。
2. 再读 `THIRD_PARTY_REVIEW_PROMPT.md`：第三方复核任务书。
3. 需要复算时只使用正式数据表：`canonical_trace_dedup_400.csv`、`dedup_400_mannwhitney_holm.csv`、`covariate_sensitivity.csv`、`valid_ratio_partial_corr.csv`、`annotation_join_quality.csv`、`failure_factor_structured_70.csv`。

## 正式文件

- `canonical_trace_dedup_400.csv`
- `dedup_400_mannwhitney_holm.csv`
- `covariate_sensitivity.csv`
- `valid_ratio_partial_corr.csv`
- `annotation_join_quality.csv`
- `failure_factor_structured_70.csv`
- `failure_factor_distribution.csv`
- `failure_factor_by_model.csv`
- `prompt_delta_correlations.csv`

## 当前可引用口径

- `canonical_trace_dedup_400.csv` 是唯一统计主表，包含 400 个唯一 `(model, sample_id)`。
- 结构化 `failure_factor` 已完成 70 / 70。
- 16 个模型 × 指标 Mann-Whitney 检验经 Holm 校正后，只有 MoLingo `metric_value` 存活。
- MoLingo `metric_value` 只能称为旧 semantic-null historical diagnostic marker；它对 MoLingo-only `valid_ratio` 和 prompt length 调整不稳健。
- MotionGPT 没有 Holm 后稳健信号。
- 跨 baseline shared propagation pattern 不成立。
- `failure_factor` 只能作为 post-hoc 人工/agent 诊断分类，不能升级为机制因果证据。

## 下一步 gate

- 必须补 `standing` 与 `zero_text` null ablation，并与旧 semantic-null delta 对比。
- `valid_ratio` 只能作为 MoLingo-only mask/valid diagnostic，不得写成跨 baseline confound/mediator 或 final evaluator。
