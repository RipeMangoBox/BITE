---
title: "MoDebug 当前路线图"
created: 2026-05-20T00:00:00+08:00
updated: 2026-05-23T15:53:56+08:00
status: active
hypothesis: "MoDebug 通过诊断并引导文本条件在预训练动作生成器内部的传播，提高生成动作的质量和文本指令跟随。"
tags:
  - MoDebug
  - roadmap
  - text_condition_propagation
  - guidance
  - diagnostic_protocol
source_papers:
  - "[[paperAnalysis/Motion_Generation/CVPR_2023/2023_T2M_GPT_Generating_Human_Motion_from_Textual_Descriptions_with_Discrete_Representations|T2M-GPT]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling|MoGenTS]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2025/2025_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with_LLMs|Motion-Agent]]"
---

# MoDebug 当前路线图

> [!abstract] 当前方案
> MoDebug 是 **文本条件传播引导插件**：当前先用 HumanML3D Original100 建立诊断失败库，再在 full text / full generated motion 层面做 `baseline` vs `baseline + MoDebug` 的 paired evaluation；内部 trace 用来解释增幅来源，motion-side grounding 并行推进。

## 一句话主张

MoDebug 作为插件追踪并引导文本条件在预训练动作生成器内部的传播，让复杂文本约束更稳定地影响完整 motion 输出，而不需要从零训练一个新的生成器，也不需要等待 motion-side event grounding 完成。

## 核心问题

```text
文本条件如何在 motion generator 内部传播？
哪些语义约束在 condition projection、attention、token prior、confidence trajectory 或 denoising path 中失效？
如何用最小干预让这些约束更稳定地影响最终 motion？
```

文本条件支持多粒度表示：

1. 全句 prompt embedding；
2. token 或 phrase embedding；
3. 方向、计数、速度、身体部位、物体交互等属性 cue；
4. 语义步骤；
5. planner-normalized prompt。

这些表示统一服务 `text condition -> generator internal state -> full motion output` 的传播诊断。

## 当前 MVP

当前可行验证只使用 full text 和 full motion：

```text
full text prompt
-> pretrained baseline B
-> full motion_B

full text prompt
-> pretrained baseline B + MoDebug
-> full motion_B+MoDebug
```

主比较：

```text
motion_B vs motion_B+MoDebug
```

比较条件必须配平：

1. same prompt；
2. same seed 或 same candidate pool；
3. same length / token budget；
4. same sampling budget；
5. same renderer / evaluator protocol。

## Original100 诊断扩展

在正式设计 MoDebug intervention 之前，先扩展 100 条 HumanML3D original text sample：

| bucket | count | role | used_for |
| --- | ---: | --- | --- |
| original100_train_gt | 80 | diagnostic | failure_bank_construction |
| original100_test_gt | 20 | diagnostic | held-out sanity and failure-family cross-check |

记录要求：

1. 每条样本必须标记 `source_split=train/test`、`text_origin=humanml3d_caption`、`text_processing=native_original_caption`、`motion_id`、`caption_idx`、`role=diagnostic`。
2. train-source 样本只支持开发观察和 failure family selection，不支持 held-out generalization claim。
3. test-source 样本可作为更强 sanity check，但在 evaluator、sample selection 和 annotation protocol 锁定前仍不是 final evaluator。
4. 第一轮只使用 original full text；不预生成 decomposed text。
5. decomposed text 只在 full text 结果暴露 event omission、event misbinding、order mismatch 或组合失真后生成，用于区分 atomic event capability failure 与 compositional propagation loss。

完整方案见 [[2026-05-23_modebug_humanml3d_original100_diagnostic_expansion|HumanML3D Original100 Diagnostic Expansion]]。

## 模型家族动机

| 工作 | 家族角色 | 文本条件接口 | MoDebug 抓手 |
| --- | --- | --- | --- |
| T2M-GPT | 最小离散 motion token 生成器 | CLIP feature 条件化 causal GPT | condition projection、next-token logits、结束 token 概率 |
| MotionGPT | motion-language 统一 token 模型 | text tokens 与 motion tokens 共用语言模型框架 | encoder-decoder attention、motion-token logits、prompt 格式敏感性 |
| Motion-Agent / MotionLLM | planner + motion-token translator | planner 先规范化 prompt，再调用 motion translator | planner 改写前后传播差异、调用路径 |
| MoMask | masked-token motion 生成器 | CLIP feature 与目标长度条件化迭代 masked generation | mask confidence、remasking trajectory、residual confidence |
| MoGenTS | time-joint 结构化 token 生成器 | 文本条件控制时空 joint token graph | time/body token response、body-time binding |

这组工作共同说明：motion prior 和动作质量持续增强，但文本条件如何进入并支配生成过程仍缺少可审计机制。

## 传播链

```text
text surface
-> text encoder / prompt adapter
-> condition projection / cross-attention input
-> generator internal propagation
-> motion-token / latent / denoising output
-> decoded motion
```

| 位置 | 诊断信号 | 干预抓手 |
| --- | --- | --- |
| text encoder | full / phrase / attribute embedding sensitivity | prompt packing、phrase weighting、adapter |
| condition projection | condition norm、token separability、layer input delta | projection repair、normalization、gating |
| attention / transformer layers | attention mass、hidden-state delta、entropy curve | attention bias、condition rescaling |
| token prior / denoising path | logits、confidence、token path、remask trajectory | rerank、sampling bias、remask schedule |
| decoded motion | human / VLM / geometry cross-check | quality guardrail、failure labeling |
| motion-side grounding | start/end state、core window、transition uncertainty | state-conditioned training、boundary soft mask、composition stress test |

## 实验关口

### 关口 0：Full-Text / Full-Motion 插件评估

目标：先证明 MoDebug 可以增幅一个或多个现有 baseline。

最小输入：

1. full text prompt；
2. baseline full motion；
3. baseline+MoDebug full motion；
4. paired human preference；
5. motion quality guardrail。

通过条件：`baseline+MoDebug` 在 full-text instruction-following paired comparison 中优于原 baseline，且 FID / diversity / geometry / naturalness 等质量护栏没有明显下降。

### 关口 0.5：Original100 Failure Bank

目标：用 100 条 HumanML3D original text sample 观察 baseline artifact 分布，并选择 2-3 个值得进入 trace/intervention 的 failure family。

通过条件：

1. 100 条样本均有 split、caption provenance、GT motion provenance 和 baseline output provenance；
2. human review 区分 `visual_caption`、`problems[]`、`enrichments[]` 和 `ambiguity_flags[]`；
3. 至少形成一组 good / bad comparator；
4. decomposed text 的生成条件被记录，不能把 decomposed prompt 当作默认更正确的监督。

### 关口 1：传播信号可导出

目标：确认至少两个预训练生成器能在 full-text 输入下导出传播 trace。

通过条件：可以记录 condition projection、layer signal、token logits / confidence 或 denoising trajectory 中至少两类信号。

### 关口 2：文本扰动集合

目标：构造不绑定单一标注格式的 perturbation battery。

扰动类型：

1. phrase drop；
2. attribute replacement；
3. order shuffle；
4. count / duration change；
5. body-part swap；
6. prompt compression / expansion。

通过条件：文本扰动能在生成器内部信号中产生可复查差异，而不是只在文本 embedding 层可见。

### 关口 3：传播 signature

目标：发现一类稳定失真模式。

候选 signature：

1. attribute signal 在 condition projection 后消失；
2. later phrase 在 layer depth 中逐步变弱；
3. count / duration cue 提高提前结束或长度偏置；
4. body-part cue 只影响全局 token，不影响对应 body/time region；
5. prompt expansion 改善文本侧可分性，但不改善 generator response。

通过条件：至少一种 signature 在两个模型、两个 prompt bucket 或多个 seed group 中复现。

### 关口 4：引导机制

目标：只针对已发现 signature 做轻量 intervention。

可用干预：

1. text-condition rescaling；
2. phrase / attribute weighting；
3. projection normalization 或 gating；
4. token-level rerank；
5. sampling / remask schedule adjustment；
6. prompt packing / planner-normalized prompt。

通过条件：guided generation 在独立 motion quality / instruction-following cross-check 上优于原生成器，并且不明显牺牲基本动作质量。

### 并行关口：Motion-Side Grounding 可靠性

目标：并行验证 motion-side grounding 是否足够可靠，未来再决定是否用于训练或细粒度解释。

必须记录：

1. grounding coverage；
2. VLM / PoseFix / human agreement；
3. `start_state_summary`；
4. `end_state_summary`；
5. `core_start / core_end`；
6. `transition_before / transition_after`；
7. `grounding_confidence`。

未来进入训练前，额外需要：

1. `start_state_summary`；
2. `end_state_summary`；
3. `core_start / core_end`；
4. `transition_before / transition_after`；
5. `grounding_confidence`；
6. `heldout_start_state` 与 `heldout_composition` 评估。

通过条件：grounding 有足够 coverage、一致性和不确定性记录；进入训练后，同一 text unit 在未见过的 start-state bucket 和前序组合中仍保持语义可见。

## 证据角色

| 证据 | 角色 | 边界 |
| --- | --- | --- |
| full-text / full-motion paired preference | `primary_plugin_evidence` | 当前主 claim：`B+MoDebug` 相对 `B` 的完整输出增幅 |
| embedding distance | `diagnostic` | 只证明文本侧可分 |
| attention / hidden-state / logits | `mechanistic_diagnostic` | 主解释层，但仍需 motion cross-check |
| decoded motion observation | `cross_check` | 不单独当 final evaluator |
| VLM / PoseFix / geometry | `cross_check` | 只验证可见 cue 与 motion quality guardrail |
| motion-side grounding | `parallel_asset` | 可靠性通过前不作为主方法前置条件 |
| human review | `anchor` | 小样本校准，不写总体 failure rate |
| Original100 failure bank | `diagnostic_expansion` | 用于 failure family selection、good/bad pair 和 trace hypothesis，不写成 benchmark |

## 当前入口

1. [[ideas/MoDebug/active/full_text_full_motion_plugin_eval/README|Full-Text / Full-Motion 插件式评估]]
2. [[2026-05-23_modebug_humanml3d_original100_diagnostic_expansion|HumanML3D Original100 Diagnostic Expansion]]
3. [[ideas/MoDebug/active/text_condition_propagation_guidance/README|文本条件传播引导]]
4. [[propagation_schema|传播记录字段]]
5. [[experimental_gates|实验关口]]
6. [[ideas/MoDebug/active/p1_event_transfer/README|P1 文本单元传播支撑实验]]
7. [[ideas/MoDebug/active/vlm_boundary_crosscheck/README|输出交叉检查]]
8. [[ideas/MoDebug/active/motion_grounding_state_dependence/README|Motion-Side Grounding 并行路线]]
9. [[ideas/MoDebug/baselines/README|模型与资产角色登记]]
