---
title: "P1 案例卡 p1evt_5_step_bow_turn_bow_turn"
created: 2026-05-16T23:48:32
updated: 2026-05-17T16:36:06+08:00
type: diagnostic_case_card
---

# P1 案例卡 p1evt_5_step_bow_turn_bow_turn

## 目标

查看这个 sample 中每个 decomposed single event 与完整 prompt 的文本相似度，并记录 P1 生成器 trace 缺失状态。

## 数据对象与计算方式

- event_count: `5`
- data_source: `eval/text_embedding/p1_full_single_embedding_similarity.tsv`
- prompt_pair: `full/single_event`
- n/evaluable: `10/10 text rows; 0 generator traces`
- evaluator: `clip_text_similarity_and_trace_availability`
- protocol: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516/protocols/eval_contract.md`
- role: `diagnostic`
- used_for: `observation`
- limitations: `文本相似度不是生成器传递证据；P1 生成器 trace 缺失。`

## 结果

| model | event_order | event_id | target_dimension | cosine_similarity | generator_trace |
|---|---:|---|---|---:|---|
| mogents | 1 | p1evt_5_step_bow_turn_bow_turn__event_01 | direction_path | 0.9274 | 缺失 |
| momask | 1 | p1evt_5_step_bow_turn_bow_turn__event_01 | direction_path | 0.9274 | 缺失 |
| mogents | 2 | p1evt_5_step_bow_turn_bow_turn__event_02 | body_part | 0.8772 | 缺失 |
| momask | 2 | p1evt_5_step_bow_turn_bow_turn__event_02 | body_part | 0.8772 | 缺失 |
| mogents | 3 | p1evt_5_step_bow_turn_bow_turn__event_03 | direction_path | 0.9298 | 缺失 |
| momask | 3 | p1evt_5_step_bow_turn_bow_turn__event_03 | direction_path | 0.9298 | 缺失 |
| mogents | 4 | p1evt_5_step_bow_turn_bow_turn__event_04 | count_duration | 0.9241 | 缺失 |
| momask | 4 | p1evt_5_step_bow_turn_bow_turn__event_04 | count_duration | 0.9241 | 缺失 |
| mogents | 5 | p1evt_5_step_bow_turn_bow_turn__event_05 | count_duration | 0.9346 | 缺失 |
| momask | 5 | p1evt_5_step_bow_turn_bow_turn__event_05 | count_duration | 0.9346 | 缺失 |

## 结论

该案例卡只说明本 sample 内各 single-event prompt 与 full prompt 的文本相似度；P1 生成器 trace 缺失，不能据此判断事件是否被生成器正确传递。
