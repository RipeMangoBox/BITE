---
title: MoDebug HumanML3D Original100 Diagnostic Expansion
created: 2026-05-23T15:53:56+08:00
updated: 2026-05-23T15:53:56+08:00
status: active
hypothesis: 先用 100 条 HumanML3D original text sample 建立诊断失败库，再按结果决定是否生成 decomposed text，用 full-vs-decomposed 对照区分单事件能力缺失与组合传播丢失。
tags:
  - MoDebug
  - diagnostic_expansion
  - HumanML3D
  - failure_bank
  - decomposed_text
related_docs:
  - "[[ideas/MoDebug/README]]"
  - "[[ideas/MoDebug/roadmap]]"
  - "[[ideas/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/README]]"
  - "[[phase1_phase2_eval_data_split_contract]]"
---

# MoDebug HumanML3D Original100 Diagnostic Expansion

> [!abstract] 当前决策
> 采纳“数据不是论文贡献，而是诊断工作台”的定位。下一步先扩到 100 条 HumanML3D original text sample，其中 80 条来自 train source split，20 条来自 test source split；第一轮只跑 original full text。decomposed text 不预先生成为主数据集，而是在 original text 结果暴露出 event omission、event misbinding 或组合失真后，再作为归因对照生成。

## 一句话定位

Original100 是 MoDebug 的 `failure_bank_v1`，不是 benchmark、不是数据集贡献，也不是最终评价器。它服务于这条链：

```text
original full text sample
-> baseline generated full motion
-> human / geometry / side-signal observation
-> failure family selection
-> trace hypothesis
-> targeted MoDebug intervention
```

它的目标是帮助选择值得进入机制分析的 failure family，而不是用人工标注规模证明总体 failure rate。

## 为什么先扩 original text

当前 18 条 P1 样本已经能暴露若干现象，但样本太小，且包含 manual event decomposition，容易把问题混成“拆分文本任务”而不是真实 HumanML3D original text 生成问题。

先扩到 original text 的好处：

1. 保留 HumanML3D 原始 caption 分布，减少手工拆分带来的 prompt artifact。
2. 先观察 baseline 在真实 full text 上的失败分布，避免提前假设所有问题都来自 event composition。
3. 让后续 decomposed text 成为有触发条件的归因工具，而不是额外数据集。
4. 为 trace 分析选择稳定 failure family，例如 `motion_in_place`、方向/转身错配、event omission、order mismatch 或 count ambiguity。

## 样本合同

目标规模：

| bucket | count | source_split | role |
| --- | ---: | --- | --- |
| original_train_source | 80 | train | diagnostic |
| original_test_source | 20 | test | diagnostic |
| total | 100 | mixed | diagnostic |

必须记录的字段：

| 字段 | 取值或说明 |
| --- | --- |
| `sample_id` | 建议使用 `hml_orig100_train_000` / `hml_orig100_test_000` |
| `phase` | `phase1_original100_gt` |
| `split_bucket` | `original100_train_gt` 或 `original100_test_gt` |
| `source_split` | HumanML3D source motion split: `train` / `test` |
| `text_origin` | `humanml3d_caption` |
| `text_processing` | `native_original_caption` |
| `caption_idx` | HumanML3D 原始 text 文件中的 caption index |
| `motion_id` | HumanML3D motion id |
| `has_gt_motion` | `yes` |
| `role` | `diagnostic` |
| `used_for` | `failure_bank_construction;baseline_artifact_observation;failure_family_selection;trace_hypothesis_prep` |
| `limitations` | 说明 train-source 不支持泛化 claim；test-source 也不是 final held-out evaluator |

选择策略应尽量分层，但不需要过度设计：

1. 覆盖 locomotion、turning、stopping、sitting/squatting、body-part action、count/duration、direction/path、multi-action composition。
2. 避免只挑 hard case；需要保留 easy / normal generation 作为 good comparator。
3. 每条记录保留原始 caption，不在第一轮改写、补全或拆分。
4. 若同一 motion 有多条 caption，可以选择其中一条作为主样本，但必须保留 `caption_idx` 和原始 caption 列表路径。

## 第一轮生成与标注

第一轮只使用 original full text：

```text
HumanML3D original caption
-> baseline generators
-> full generated motion
-> visual review / geometry side check
-> structured diagnostic record
```

标注结构建议保留两层，而不是把所有内容塞进一个 caption：

| 字段 | 含义 |
| --- | --- |
| `visual_caption` | 人看到 motion 后的中性描述，可以补充 GT caption 的多样化表达 |
| `problems[]` | caption 与 original text 的冲突、缺失或错绑，必须尽量 event-level 对齐 |
| `enrichments[]` | 不与 text 冲突、只是更细的可视化补充 |
| `ambiguity_flags[]` | 步数、边界、最后并步是否计步等数据 scope ambiguity |
| `severity_overall` | 只用于排序和选 case，不作为最终 evaluator |
| `review_status` | `raw` / `cleaned` / `needs_second_pass` |

注意：GT caption 可以作为多样化描述补充；baseline 的问题描述必须可回连到原始 text。若 `visual_caption` 与 text 都合理，只记为 enrichment，不记 problem。

## Decomposed Text 的触发条件

decomposed text 不在 original100 创建时一次性生成。只有当 original full text 结果满足以下任一条件时才生成：

1. full motion 明显遗漏某个 event；
2. full motion 中 event 顺序、方向、步数或身体部位发生错绑；
3. full text 的多个 event 在 motion 中互相覆盖或被 dominant prior 吞掉；
4. 人工或几何 side check 无法判断是单事件不会做，还是组合时丢失。

生成 decomposed text 时，每个 full text 对应一组 semantic event prompts，并保留原文和拆分依据：

```text
full_original_text
-> event_text_1
-> event_text_2
-> ...
```

decomposed prompt 必须标记：

| 字段 | 含义 |
| --- | --- |
| `decomposition_source` | `manual_from_original_caption` / `automatic_pending_review` / `manual_cleaned` |
| `event_idx` | 从 1 开始 |
| `event_text` | 子事件文本 |
| `event_relation_to_full` | `literal_span` / `paraphrase` / `implicit_completion` |
| `boundary_confidence` | 文本事件边界置信度，不等于 motion temporal boundary |
| `limitations` | 拆分歧义，例如最后一步并步、计数模糊、转身是否独立事件 |

## Full-vs-Decomposed 归因矩阵

decomposed text 的唯一主要用途是归因，而不是单独扩大训练数据。

| full text 结果 | decomposed event 结果 | 暂定解释 | 后续动作 |
| --- | --- | --- | --- |
| full 失败 | 单 event 也失败 | baseline 缺少该 atomic event 能力，或动作定义/数据存在歧义 | 不优先作为 composition-propagation claim；可作为模型能力边界 |
| full 失败 | 单 event 成功 | 组合生成中发生 event 信息丢失、错绑或优先级覆盖 | 进入 MoDebug trace 和 targeted guidance |
| full 成功 | 单 event 失败 | full context 反而提供必要上下文，拆分破坏语义 | 不把 decomposed 作为更强监督 |
| full 成功 | 单 event 成功 | 正常样本，可作为 good comparator | 用于 trace 对照 |
| full 模糊 | 单 event 模糊 | 多半是 text/data scope ambiguity | 标记 ambiguity，不作为核心 claim |

这张矩阵是 MoDebug 论文中更有价值的证据入口：它把“模型不会做单个动作”和“full text 组合时丢 event”区分开，后者才直接对应 text-condition propagation 失真。

## 步数与边界歧义

步数不稳定不是当前 MoDebug 要主动解决的核心问题。Original100 中应将其作为数据 scope ambiguity 管控：

1. 若 text 明确要求 count，而 motion 明显不同，可记 `problem.attribute=steps/count`，但要附 `ambiguity_flags`。
2. 若 text 是 `a few steps`、`several steps` 等弱约束，caption 给出具体步数通常是 enrichment，不是 problem。
3. “最后一步并步是否算一步”这类边界必须写入 `ambiguity_flags`，不用于严格 final metric。
4. 若 count ambiguity 是某个 family 的主现象，需要单独定义计步协议和 held-out evaluator；在此之前只作为 diagnostic side analysis。

## 与机制路线的连接

Original100 结束后不要直接扩大人工标注，而应做选择：

1. 汇总 failure family，优先选择能用几何或结构化指标交叉检查的类别。
2. 为每个候选 family 建立 good / bad pair。
3. 检查该 family 是否能导出 generator trace，例如 projection、attention、logit、confidence 或 remask trajectory。
4. 只有 trace hypothesis 成立时，才设计 MoDebug intervention。
5. intervention 后回到 full-text / full-motion paired evaluation，而不是只报告 failure tag 改善。

优先进入机制分析的候选 family：

| family | 自动化潜力 | MoDebug 相关性 | 备注 |
| --- | --- | --- | --- |
| `motion_in_place` / `weak_translation` | 高 | 中到高 | root planar span 可作 side check；需要区分 locomotion 能力与 text propagation |
| direction / turn mismatch | 中 | 高 | 与 path/direction cue 传播相关 |
| event omission | 中 | 高 | 最适合 full-vs-decomposed 对照 |
| order mismatch | 中 | 高 | 需要较可靠的人类或结构化检查 |
| steps/count ambiguity | 低到中 | 条件性相关 | 先作为 ambiguity 管控，不作为核心 evaluator |

## 证据边界

允许 claim：

1. Original100 用于构建 MoDebug 的 failure bank 和 trace hypothesis。
2. 80 train-source 与 20 test-source 均带 split 标记，train-source 只用于诊断和开发观察。
3. decomposed text 是按 original full-text 失败结果触发的归因对照。
4. full-vs-decomposed 对照可以帮助区分 atomic event capability 与 compositional propagation loss。

禁止 claim：

1. Original100 是新的 benchmark 或数据集贡献。
2. 100 条人工标注能证明模型总体 failure rate。
3. train-source 结果支持 held-out generalization。
4. decomposed text 天然比 original text 更正确或更强监督。
5. VLM、geometry 或人工 problem tag 可以直接作为最终 evaluator。

## Drift Note

```text
old_plan: 18 条 P1 样本 + baseline/GT human eval，倾向讨论 structured dataset 或 failure caption 数据构造
new_plan: 100 条 HumanML3D original text diagnostic expansion，先观察 full-text 失败分布，再按触发条件生成 decomposed text 做归因对照
evidence: 18 条样本已暴露 motion_in_place、walk translation、GT step-count ambiguity 和 caption/problem 混合问题；小样本不适合作为数据集贡献
affected_docs: MoDebug README；MoDebug roadmap；full_text_full_motion_plugin_eval experiment scaffold；phase1/phase2 split contract
next_action: 构造 original100 sample manifest，运行 baseline full-motion generation，清洗 human eval schema，再选择 2-3 个 failure family 进入 trace/intervention
```
