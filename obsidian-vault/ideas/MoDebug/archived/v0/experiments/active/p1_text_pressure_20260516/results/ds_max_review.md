---
title: "DS Max 审查 MoDebug 任务一诊断总结"
created: 2026-05-17T15:16:00+08:00
updated: 2026-05-20T13:45:48+08:00
type: diagnostic_review
tags:
  - MoDebug
  - diagnostic
  - ds_max
---

# DS Max 审查 MoDebug 任务一诊断总结

## 目标

独立检查 P1 text-pressure 诊断结论是否过度推断，是否遵守 diagnostic/cross_check 边界。

## 数据对象

- P1 文本侧 full-vs-single similarity。
- P1 generator/motion 缺失报告。

## 审查结论

**通过，但需要轻微降级措辞。**

DS Max 认为 P1 text-side 结果不能写成最终评估器，也不能用旧 proxy 填补 P1 生成器/运动侧缺失。

## 计算方式

DS Max 读取 P1 聚合数字和图形说明，重点检查小样本过度推断、文本侧指标与生成器指标混用、以及 diagnostic/cross_check 是否被写成 final evaluator。

## 已支持的结论

- P1 文本距离随 event_count 增加，但必须标注小样本限制。
- P1 generator/motion 缺失必须单独记录，不能用旧 proxy 或文本侧距离填补。

## 已执行的修改

- 把 P1 event_count 趋势写成“有限样本下的诊断趋势”。
- 把 P1 event_order/order5 写成“n=2 不稳定”，不写成因果解释。
- 把 P1 当前状态收缩为 text-pressure diagnostic 与 missing report，不做全局模型排名。
- 从 active 结论入口移除旧 M0 proxy、motion geometry/static panel 和混合 summary。

## 2026-05-18 二轮：propagation 假设审查

DS Max 对“为了最终 motion 满足所有 event，text embedding 在 propagation 中是否应该保持某种特性”给出的审查结论是：不能把“稳定保留 event embedding 几何关系”写成必要条件。生成器可能重编码或重组合文本信息；真正需要验证的是中间信号是否仍然可检测、可利用，并且是否和逐事件 motion satisfaction 有相关或因果关系。

建议使用以下重述：

> full prompt 中每个 event 的信息，应当在某些中间表征、注意力路径或输出 motion 中保持可检测、可利用的信号；这些信号是否有价值，必须通过它们和逐事件 motion satisfaction 的相关或因果关系来验证。

二轮审查的最小执行结论：

- P0 只整理 text-side 压力轴和缺失项，不需要新 generator，不需要 motion satisfaction。
- P1 必须补 P1 full/single generation 和 generator trace；否则不能讨论 P1 propagation。
- 1-event/2-event full text 是最小 motion gate：需要真实 generated motion 和逐事件 satisfaction check，人工标注优先，MLLM 只能作为 sidecar 或校准后 evaluator。
- text embedding distance、Qwen finite coverage failure、旧 proxy、P1 trace similarity 都不能直接升级为 final evaluator。

详细队列见 `results/p1_propagation_experiment_queue.md`。

## 元数据

- date: `2026-05-18`
- experiment_path: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516`
- evaluator: `DS Max independent diagnostic-methodology review`
- protocol: `paperIDEAs/MoDebug/experiments/active/p1_text_pressure_20260516/protocols/eval_contract.md`
- data_source: `results/compact_tables/`, `vis/summary/`, `results/missing_data_report.md`
- condition_pair or prompt_pair: `full/single_event`
- n/evaluable: 见 compact TSV
- coverage: P1 文本侧、P1 缺失数据声明，以及 propagation 假设审查
- role: `diagnostic`
- used_for: `observation`
- limitations: DS Max 审查不是 held-out 最终评估器；二轮审查只给出实验设计 gate，不提供 motion satisfaction 证据。
