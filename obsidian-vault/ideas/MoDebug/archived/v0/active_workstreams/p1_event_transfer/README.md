---
title: "MoDebug 支撑路线：P1 文本单元传播实验"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-20T13:45:48+08:00
status: active
tags:
  - MoDebug
  - P1
  - text_unit_transfer
  - support_route
---

# MoDebug 支撑路线：P1 文本单元传播实验

## 角色

P1 是 MoDebug 的支撑实验，不是独立主线。它提供一批可控样本，用来观察文本单元在三层中的变化：

```text
text embedding
-> generator trace
-> full-motion paired cross-check
```

P1 已有的单元拆分可以继续作为 `text_unit_type=semantic_step` 的来源；后续也可以加入 phrase、attribute、token span 和 planner step。

## 当前证据

| 层级 | 状态 | 入口 | 边界 |
| --- | --- | --- | --- |
| Text embedding | 已有 CLIP / DistilBERT / T5 / Qwen pooled diagnostic | `active/p1_text_pressure_20260516` | 只说明文本侧压力轴 |
| Generator trace | 仍需补齐 | missing_data_report | 不能用旧 proxy 替代 |
| Motion side | 仍需补齐 P1 generated motions | p1_propagation_experiment_queue | 只作为 cross-check |

完整入口：

1. [[ideas/MoDebug/experiments/active/p1_text_pressure_20260516/README|P1 Text-Pressure 实验总览]]
2. [[p1_single_event_similarity_vis|P1 单事件相似度可视化]]
3. [[missing_data_report|missing_data_report]]
4. [[p1_propagation_experiment_queue|p1_propagation_experiment_queue]]

## 下一关口

只补最小集合：

1. 从 P1 样本中筛出 full prompt、phrase、attribute、semantic step 的 perturbation pairs。
2. 先跑 full-text / full-motion paired evaluation，比较 `B` 与 `B+MoDebug`。
3. 对 trace 可用模型补 token logits、confidence、path 或 layer signal。
4. 对 decoded full motion 记录 paired preference、quality guardrail 和必要的可见 cue cross-check。
5. 分析 text embedding 与 generator trace 是否能解释 full-motion paired improvement。

motion-side grounding 不阻塞上述流程。如果 P1 后续加入 grounding-based training，必须额外记录 `start_state_summary`、`end_state_summary`、`core_start / core_end` 与 transition uncertainty。具体风险与增广策略见 [[ideas/MoDebug/active/motion_grounding_state_dependence/README|Motion-Side Grounding 的可靠性与状态依赖风险]]。

## 停止规则

如果 token-level propagation 与 text perturbation 没有稳定关系，不继续扩更多 encoder；先回到文本单元构造、trace 可用性和模型选择。
