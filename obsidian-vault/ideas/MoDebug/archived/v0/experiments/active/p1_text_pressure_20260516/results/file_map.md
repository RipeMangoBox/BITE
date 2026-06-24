---
title: "MoDebug P1 Text-Pressure 文件地图"
created: 2026-05-17T15:18:13+08:00
updated: 2026-05-20T13:45:48+08:00
type: diagnostic_file_map
tags:
  - MoDebug
  - diagnostic
  - text_pressure
---

# MoDebug P1 Text-Pressure 文件地图

## 目标

解释清理后的 P1 text-pressure 目录中每个文件夹和关键文件的作用。这个文件地图只服务阅读和追溯，不重新计算指标。

## 数据对象

- P1：10 个 sample。
- decomposed event：30 个。
- single-event prompt：30 条。
- 当前 active 证据：文本侧 full-vs-single diagnostic 与缺失报告。

## 先读这里

1. `README.md`：当前角色和边界。
2. `results/p1_single_event_similarity_vis.md`：CLIP 文本侧可视化说明。
3. `results/compact_tables/p1_text_similarity_by_event_count_order.tsv`：event_count / event_order 紧凑表。
4. `results/compact_tables/text_embedding_ext_p1_by_encoder_event_count.tsv`：多 encoder P1 统计。
5. `results/compact_tables/text_embedding_ext_finite_coverage.tsv`：多 encoder finite coverage。
6. `results/missing_data_report.md`：P1 generator/motion 缺失报告。
7. `results/p1_propagation_experiment_queue.md`：补实验队列。

## 文件夹作用

| 路径 | 作用 | 阅读方式 |
|---|---|---|
| `inputs/` | P1 sample、event decomposition、single-event prompt 输入清单 | 作为诊断单位来源 |
| `docs/selection_notes.md` | 样本选择和计划漂移记录 | 检查为什么保留这些 P1 单位 |
| `protocols/eval_contract.md` | P1 text-pressure 诊断协议 | 确认所有指标不是 final evaluator |
| `eval/text_embedding/` | CLIP full-vs-single 文本侧原始指标 | 只在复查数字时读 |
| `eval/text_embedding_ext/` | L40 多 encoder P1 文本侧诊断 | 先看 compact table 和 finite coverage |
| `eval/generator_propagation/` | 当前只保留 P1 generator trace 缺失表 | 不包含真实 P1 trace |
| `eval/motion_side/` | 当前为空，留给后续 P1 generated motion / satisfaction | 不含现有运动侧证据 |
| `results/compact_tables/` | 面向阅读的小型聚合 TSV | 支撑 text-pressure 观察 |
| `vis/case_cards/` | 每个 P1 sample 的文本侧 case card | 看单例细节 |
| `vis/summary/` | P1 文本侧热力图 | 首选视觉入口 |
| `provenance/` | L40 text encoder 环境和 run 状态 | 追溯远程环境、权重和 coverage |
| `logs/` | 当前无有效 active run log | 后续复现实验再填 |

## 问题到文件的映射

| 问题 | 先读 | 原始证据 |
|---|---|---|
| 单事件 prompt 与完整文本有多相似？ | `results/p1_single_event_similarity_vis.md` | `eval/text_embedding/p1_full_single_embedding_similarity.tsv` |
| event_count / event_order 是否形成文本压力轴？ | `results/compact_tables/p1_text_similarity_by_event_count_order.tsv` | `eval/text_embedding/p1_full_single_embedding_similarity.tsv` |
| 不同 text encoder 是否有完整 finite coverage？ | `results/compact_tables/text_embedding_ext_finite_coverage.tsv` | `eval/text_embedding_ext/run_20260517_l40_multiscale/` |
| P1 generator trace 是否存在？ | `results/missing_data_report.md` | `eval/generator_propagation/p1_missing_generator_trace.tsv` |
| 后续要补什么实验？ | `results/p1_propagation_experiment_queue.md` | 本目录输入表和缺失报告 |

## 已移出 Active 结论的内容

以下内容不再作为当前 P1 active evidence：

1. 旧 M0 condition set 的 generator trace summary delta；
2. 旧 M0 motion geometry / static panel cross-check；
3. 混合 P1/M0 的 summary、图表和结论；
4. 任何把 text embedding distance 直接升级为 motion satisfaction 的解释。

## 元数据

- date: `2026-05-20`
- experiment_path: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516`
- evaluator: `modebug_p1_text_pressure_file_map_cleanup`
- protocol: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516/protocols/eval_contract.md`
- data_source: 当前 experiment 下已有 `inputs/`、`eval/text_embedding/`、`eval/text_embedding_ext/`、`results/compact_tables/`、`vis/summary/`
- prompt_pair: `full/single_event`
- n/evaluable: 见各结果文件
- coverage: P1 文本侧和缺失报告
- role: `diagnostic`
- used_for: `observation`
- limitations: 文件地图不是评估器，只是阅读索引。
