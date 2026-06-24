---
title: "P1 Text-Pressure 缺失数据报告"
created: 2026-05-16T23:48:32
updated: 2026-05-20T13:45:48+08:00
type: diagnostic_report
---

# P1 Text-Pressure 缺失数据报告

## 目标

明确记录 P1 MoMask/MoGenTS 生成器 trace 和运动侧输出缺失，避免用旧 M0 数据硬补。

## 数据对象

- P1 sample：10 条。
- P1 single-event prompt：30 条。
- 模型：MoMask、MoGenTS。

## 计算方式

只做产物可用性检查：检查当前 experiment 目录中是否存在 P1 生成输出、text embedding snapshot、full-prompt generator trace summary 和 motion-side satisfaction / visualization artifacts。

## 结论

- P1 没有 MoMask/MoGenTS generated motion outputs。
- P1 没有 MoMask/MoGenTS full-prompt generator trace summary。
- P1 没有 P1 motion-side satisfaction、geometry audit 或 visualization artifacts。
- 因此 P1 目前只能做文本侧 full-vs-single similarity；生成器传播和运动侧可视化仍缺失。
- 缺失项状态：禁止用 M0 代理填补 P1 generator/motion；补实验队列已经拆到 `results/p1_propagation_experiment_queue.md`。
- 核心假设边界：不能把“event embedding 在传播中稳定保留”当成已验证的必要条件；下一步必须用 P1 generation trace 和 1-event/2-event motion satisfaction gate 检查中间信号是否和逐事件 motion 满足有关。

## 补实验队列摘要

| priority | next action | owner | remote/session/log | generator required | motion satisfaction required | expected output | role |
|---|---|---|---|---|---|---|---|
| P0 | 1-event/2-event validation case plan | local Codex | local only | no | no | `results/compact_tables/p1_1e2e_validation_case_plan.tsv` | diagnostic |
| P1-a | P1 full/single generation run | remote experiment agent | TBD before launch | yes | no | `eval/motion_side/p1_generated_motion_manifest.tsv` | diagnostic |
| P1-b | P1 full/single generator trace summary | remote experiment agent | same as P1-a if hooks are enabled | yes | no | `eval/generator_propagation/p1_full_single_trace_summary.tsv` | diagnostic |
| P1-c | 1-event/2-event motion satisfaction gate | local reviewer | local review over generated artifacts | yes | yes | `eval/motion_side/p1_1e2e_event_satisfaction_check.tsv` | cross_check |

## 元数据

- date: `2026-05-20`
- experiment_path: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516`
- evaluator: `p1_artifact_availability_check`
- protocol: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516/protocols/eval_contract.md`
- data_source: `inputs/sample_manifest.tsv`, `inputs/single_event_prompt_manifest.tsv`, `inputs/event_decomposition.tsv`
- prompt_pair: `full/single_event`
- n/evaluable: `0/30 full-prompt generator traces per model; missing table rows 60`
- coverage: `10 samples, 30 single-event prompts, 2 models`
- role: `diagnostic`
- used_for: `observation`
- limitations: `缺失报告不是评估器；没有 proxy trace、attention、geometry 或 embedding 被当成 final evaluator；补实验队列只是 selection/management，不是新证据。`
