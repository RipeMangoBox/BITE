---
title: "P1 Event Propagation 补实验队列"
created: 2026-05-18T18:16:47+08:00
updated: 2026-05-20T13:45:48+08:00
type: experiment_queue
tags:
  - MoDebug
  - P1
  - event_transfer
  - diagnostic
---

# P1 Event Propagation 补实验队列

## 目标

把“text embedding 在 generation propagation 中是否应该保持某种特性”改写成可证伪的实验问题，并把缺失实验拆成 P0/P1/P2 队列。

## 核心假设

不要把“event embedding 在传播过程中稳定保留”当成必要条件。生成器可能重编码、压缩或重组合文本信息，稳定几何距离不是 motion 满足所有 event 的充分或必要条件。

更稳妥的假设是：

> full prompt 中每个 event 的信息，应当在某些中间表征、注意力路径或输出 motion 中保持可检测、可利用的信号；这些信号是否有价值，必须通过它们和逐事件 motion satisfaction 的相关或因果关系来验证。

当前 CLIP、DistilBERT、T5、Qwen 的 text-side 结果只能说明 event_count 是一个文本侧压力轴；它们不能证明 generator propagation 正确，也不能证明 motion 逐事件满足。

## 当前证据边界

- 已有：CLIP、DistilBERT、T5 base、T5 large、FLAN-T5 base、Qwen3-32B 的 full-vs-single text embedding distance。
- 缺失：P1 full prompt generated motions、P1 single-event generated motions、P1 full/single generator trace、P1 motion-side event satisfaction。
- 禁止：用旧 M0 trace 或 text-side embedding distance 代理填补 P1 generator/motion 结果。

## P0 队列

| 优先级 | 实验 | owner | remote/session/log | 是否先跑 generator | 是否需要 motion satisfaction | 人力/MLLM | 输出路径 | 角色 |
|---|---|---|---|---|---|---|---|---|
| P0-done | 合并 CLIP + DistilBERT/T5/Qwen 多 encoder 文本侧诊断 | local Codex | local only | 否 | 否 | 否 | `results/compact_tables/text_embedding_ext_p1_by_encoder_event_count.tsv`; `results/compact_tables/text_embedding_ext_finite_coverage.tsv` | diagnostic |
| P0-done | P1 generator/motion 缺失清单 | local Codex | local only | 否 | 否 | 否 | `eval/generator_propagation/p1_missing_generator_trace.tsv`; `results/missing_data_report.md` | diagnostic |
| P0-next | 1-event/2-event 最小验证 case plan | local Codex | local only | 否 | 否 | 否 | `results/compact_tables/p1_1e2e_validation_case_plan.tsv` | diagnostic |

P0 的目标是让后续实验不再争论输入单位、已有证据和缺失项。P0 不能回答 propagation 是否正确。

## P1 队列

| 优先级 | 实验 | owner | remote/session/log | 是否先跑 generator | 是否需要 motion satisfaction | 人力/MLLM | 输出路径 | 角色 |
|---|---|---|---|---|---|---|---|---|
| P1-a | 10 full prompts + 30 single-event prompts 的 MoMask/MoGenTS generation run | remote experiment agent | TBD remote host; session/log must be recorded before launch | 是 | 否 | 否 | `eval/motion_side/p1_generated_motion_manifest.tsv`; `motions/p1_full_single/` | diagnostic |
| P1-b | P1 full/single generator trace summary | remote experiment agent | Same run as P1-a if hooks are enabled; otherwise separate trace session | 是 | 否 | 否 | `eval/generator_propagation/p1_full_single_trace_summary.tsv`; `results/p1_generator_trace_summary.md` | diagnostic |
| P1-c | 1-event/2-event full text 最小 motion satisfaction gate | local reviewer + optional MLLM sidecar | local review over P1-a artifacts | 是 | 是 | 建议 1 人快速标注；MLLM 只能做 sidecar | `eval/motion_side/p1_1e2e_event_satisfaction_check.tsv`; `results/p1_1e2e_motion_satisfaction_gate.md` | cross_check |

P1-c 是回答核心假设的最小 gate：对 event_count 1 和 2 的 full text，必须看到生成 motion 是否逐事件满足。没有这一步，任何“embedding 保持/传播”的说法都只能停留在内部诊断。

## P2 队列

| 优先级 | 实验 | owner | remote/session/log | 是否先跑 generator | 是否需要 motion satisfaction | 人力/MLLM | 输出路径 | 角色 |
|---|---|---|---|---|---|---|---|---|
| P2-a | 全 10 full prompts 的逐事件 satisfaction 扩展评估 | evaluator agent | local review over generated artifacts | 是 | 是 | 需要人工或已校准 MLLM | `eval/motion_side/p2_full_event_satisfaction.tsv`; `results/p2_satisfaction_summary.md` | cross_check 或 heldout_final_evaluator |
| P2-b | trace/satisfaction 相关性分析 | analysis agent | local only after P2-a | 是 | 是 | 依赖 P2-a | `eval/generator_propagation/p2_trace_satisfaction_correlation.tsv`; `results/p2_trace_satisfaction_report.md` | diagnostic |
| P2-c | attention/hidden-state intervention 或 event ablation | remote experiment agent | TBD remote host; session/log must be recorded before launch | 是 | 是 | 需要人工或已校准 MLLM | `eval/interventions/p2_event_ablation.tsv`; `results/p2_intervention_report.md` | diagnostic |

只有当 P2-a 使用与开发指标分离的 held-out protocol，并报告 evaluator、n/evaluable、coverage、limitations，才可以把它写成 `heldout_final_evaluator`。否则仍是 `cross_check`。

## 1-event/2-event 最小验证

必须看：

- 每个 generated motion 是否能被逐事件打分，例如 1-event 是 `1/1` 或 `0/1`，2-event 是 `0/2`、`1/2`、`2/2`。
- full prompt embedding 与 single-event embedding 的距离，是否和逐事件 satisfaction 有一致的排序或相关关系。
- 若 2-event motion 只满足一个事件，需要记录满足的是哪一个事件，而不是只记录总分。

不能看：

- 不能只看 text embedding 距离的组间差异。
- 不能用 FID、diversity、latent reconstruction loss 代替逐事件 satisfaction。
- 不能把未校准 MLLM 打分当 final evaluator。
- 不能把 P1 generator trace 的相似度或注意力曲线直接解释为 motion 满足。

## 元数据

- date: `2026-05-18`
- experiment_path: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516`
- evaluator: `DS Max propagation-hypothesis review; Codex experiment queue consolidation`
- protocol: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516/protocols/eval_contract.md`
- data_source: `results/compact_tables/text_embedding_ext_p1_by_encoder_event_count.tsv`, `results/compact_tables/text_embedding_ext_finite_coverage.tsv`, `results/missing_data_report.md`, `eval/generator_propagation/p1_missing_generator_trace.tsv`
- prompt_pair: `full/single_event`
- condition_pair: `not_applicable`
- n/evaluable: `P1 generator trace 0/30 per model at queue creation; text-side diagnostics available for 30 P1 pairs across 6 encoders with Qwen partial finite coverage`
- coverage: `P0/P1/P2 queue for P1 event propagation and motion satisfaction gaps`
- role: `diagnostic`
- used_for: `selection`
- limitations: `This is an experiment management document, not evaluation evidence.`
