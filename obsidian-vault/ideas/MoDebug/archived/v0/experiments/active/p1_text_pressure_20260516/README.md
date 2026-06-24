---
title: "MoDebug P1 Text-Pressure 实验总览"
created: 2026-05-16T21:45:00+08:00
updated: 2026-05-20T13:45:48+08:00
tags:
  - MoDebug
  - P1
  - text_pressure
  - diagnostic
---

# MoDebug P1 Text-Pressure 实验总览

## 当前角色

本实验现在只保留为 **P1 文本侧压力轴**。它回答的问题是：在 10 个多事件/组合 prompt 中，完整文本与 decomposed single-event prompt 在不同 text encoder 下是否仍可分，以及哪些样本适合后续 generator trace 和 full-motion paired evaluation。

它不再承载旧 M0 generator proxy、motion geometry/static panel 或混合 summary 结论。

## 数据对象

- P1 正式输入：`10` 个 sample，覆盖事件数 1-5，每档 2 条。
- P1 事件分解：`30` 个 decomposed event。
- P1 单事件 prompt：`30` 条。
- 文本编码器：CLIP ViT-B/32、DistilBERT、T5 base、T5 large、FLAN-T5 base、Qwen3-32B mean pooling。

## 当前可用证据

| 层级 | 状态 | 入口 | 角色 |
|---|---|---|---|
| P1 输入设计 | 可用 | `inputs/`、`docs/selection_notes.md` | `diagnostic_design` |
| CLIP full-vs-single similarity | 可用 | `eval/text_embedding/`、`results/p1_single_event_similarity_vis.md` | `diagnostic` |
| 多 encoder text-side 复查 | 可用但只限文本侧 | `eval/text_embedding_ext/`、`results/compact_tables/`、`provenance/l40_text_encoder_status.md` | `diagnostic` |
| P1 generator trace | 缺失 | `eval/generator_propagation/p1_missing_generator_trace.tsv`、`results/missing_data_report.md` | `missing_report` |
| P1 generated motion / satisfaction | 缺失 | `results/p1_propagation_experiment_queue.md` | `experiment_queue` |

## 当前结论

1. P1 文本侧 full-vs-single similarity 可作为后续实验的压力轴和样本定位入口。
2. event decomposition 是诊断单元，不是 motion-side temporal boundary。
3. Qwen3-32B mean pooling finite coverage 不足，只保留为失败/诊断信号，不参与主排序。
4. P1 当前没有 generator trace、generated motion、motion-side event satisfaction，因此不能支持 propagation 或 instruction-following 结论。
5. 后续如果要进入方法 claim，必须转到 full-text / full-motion paired evaluation，而不是继续扩 text embedding encoder。

## 推荐阅读入口

1. `results/file_map.md`：清理后的文件地图。
2. `results/p1_single_event_similarity_vis.md`：CLIP 文本侧 full-vs-single 可视化说明。
3. `results/compact_tables/p1_text_similarity_by_event_count_order.tsv`：P1 文本相似度紧凑表。
4. `results/compact_tables/text_embedding_ext_p1_by_encoder_event_count.tsv`：多 encoder P1 event_count 统计。
5. `results/compact_tables/text_embedding_ext_finite_coverage.tsv`：多 encoder finite coverage。
6. `results/missing_data_report.md`：P1 generator/motion 缺失报告。
7. `results/p1_propagation_experiment_queue.md`：后续补实验队列。

## 保留边界

- raw TSV 中可能仍保留旧 `experiment_path` 字段，这是移动目录前的 provenance，不代表当前 active 结论仍使用旧路径。
- 旧 M0 rows、旧 M0 trace、旧 M0 geometry/static panel 不作为当前 P1 active evidence。
- 本目录所有现有正向结果的 `role` 都保持为 `diagnostic` 或 `missing_report`；没有任何 `formal_ordering_evidence` 或 `heldout_final_evaluator`。

## 下一步

1. 停止扩展纯 text embedding encoder。
2. 在 `active/full_text_full_motion_plugin_eval_20260520/` 中建立 `B` vs `B+MoDebug` full-motion paired run。
3. 如果复用 P1，先选 1-event/2-event 最小样本进入 generated motion 与 human/cross-check gate。
4. 若要补 trace，必须记录真实 P1 full/single generation trace，不能用旧 proxy 替代。
