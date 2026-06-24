---
title: "P1 单事件相似度可视化"
created: 2026-05-17T16:34:36+08:00
updated: 2026-05-20T13:45:48+08:00
type: diagnostic_summary
---

# P1 文本侧单事件相似度可视化

## 目标

展示 P1 decomposed single event prompt 与所属 full prompt 的文本侧相似度，让读者能直接看到每个 sample 内各事件在完整文本中的嵌入接近程度。

## 数据对象

- P1 sample：`10` 个。
- source rows：`60` 行 MoMask/MoGenTS 文本侧重复记录。
- unique events：按 `(sample_id, event_id)` 折叠后得到 `30` 个 decomposed single events。
- prompt_pair：`full/single_event`。

## 计算方式

读取 `p1_full_single_embedding_similarity.tsv`，按 `(sample_id, event_id)` 折叠重复模型行，使用 `cosine_distance` 作为热力图颜色，格内显示 `cosine_similarity` 和 `cosine_distance`。

## 来源与边界

- date: `2026-05-17`
- experiment_path: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516`
- evaluator: `clip/ViT-B/32_text_embedding_similarity_collapsed_by_sample_event`
- protocol: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516/protocols/eval_contract.md`
- data_source: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516/eval/text_embedding/p1_full_single_embedding_similarity.tsv`
- prompt_pair: `full/single_event`
- n/evaluable: `30/30 unique decomposed events`
- coverage: `10/10 samples；从 60 条模型标签重复行 折叠为 30 个 unique events；模型标签为 mogents,momask。`
- role: `diagnostic`
- used_for: `observation`
- limitations: `仅为 CLIP 文本嵌入相似度；MoMask/MoGenTS 重复文本侧行按 (sample_id, event_id) 折叠；不是生成器传递、运动正确性或最终评估器证据。`

## 输出

- SVG：`vis/summary/p1_single_event_full_text_similarity_heatmap.svg`
- 小型表：`results/compact_tables/p1_single_event_similarity_sample_order.tsv`

![[p1_single_event_full_text_similarity_heatmap.svg]]

## 读图说明

每行对应一个 `sample_id`，每列对应 `event_order`。颜色使用 `cosine_distance`，红色更高表示 decomposed single event prompt 与 full prompt 的文本嵌入距离更大；格内保留 `target_dimension` 的中文短标签，并显示 `cosine_similarity` 与 `cosine_distance`。

本图从 `p1_full_single_embedding_similarity.tsv` 的 60 行中，按 `(sample_id, event_id)` 折叠 MoMask/MoGenTS 重复文本侧记录，得到 30 个 unique decomposed single events，覆盖 10 个 samples。重复记录检查：无；重复行的 similarity/distance 与首个文本侧记录一致。

## 数值范围

- min_cosine_similarity: `0.754820`
- max_cosine_similarity: `1.000000`
- min_cosine_distance: `-0.000000`
- max_cosine_distance: `0.245180`

## 结论

- 该图覆盖 30/30 个 P1 decomposed single events。
- 颜色最深的格子表示该 single-event prompt 与 full prompt 的文本嵌入距离更大，适合作为后续 generator trace 检查的定位入口。
- 这仍然只是文本侧诊断，不说明生成器已经传递了该事件。

## 使用边界

这个结果只用于观察文本侧 decomposition 与 full prompt 的嵌入接近程度。它不包含 generator trace、motion-side event satisfaction 或人类偏好判断，因此 `role` 保持为 `diagnostic`，`used_for` 保持为 `observation`。
