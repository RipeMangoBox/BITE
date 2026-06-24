---
title: MoDebug Risk Boundary and Claim Control
created: 2026-05-22T00:00:00+08:00
updated: 2026-05-22T00:00:00+08:00
status: active
hypothesis: MoDebug 不需要 pivot；当前核心风险是 nearest-work compression 与 reward/RL 命名混淆，需要用机制对象、证据角色和评估隔离主动管控。
tags:
  - MoDebug
  - risk_control
  - claim_boundary
  - reward_boundary
  - reviewer_risk
source_papers:
  - "[[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment]]"
related_docs:
  - "[[ideas/MoDebug/README]]"
  - "[[core_idea]]"
  - "[[ideas/MoDebug/roadmap]]"
  - "[[ideas/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/README]]"
  - "[[phase1_phase2_eval_data_split_contract]]"
---

# MoDebug Risk Boundary and Claim Control

> [!abstract] 一句话决策
> MoDebug 当前不需要 pivot；但论文写作必须主动管控 **nearest-work compression** 与 **reward/RL naming risk**，把主贡献锁定为 mechanistic text-condition propagation debugging + signature-targeted minimal guidance，而不是泛化的 reward alignment 或新 generator。

## 关联上下文

本文是写作边界控制，不替代路线图或实验协议。对应主文档：

- [[ideas/MoDebug/README|MoDebug README]]
- [[core_idea|MoDebug Core Idea]]
- [[ideas/MoDebug/roadmap|MoDebug 当前路线图]]
- [[ideas/MoDebug/experiments/active/full_text_full_motion_plugin_eval_20260520/README|Full-Text / Full-Motion 插件评估实验骨架]]
- [[phase1_phase2_eval_data_split_contract|Phase1/Phase2 Evaluation Data Split Contract]]
- [[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment|ReAlign]]

## 作者立场

不应把 ReAlign 或其他 reward-guided 方法与 MoDebug 写成 fatal overlap。当前 MoDebug 的核心对象是 **文本条件在预训练动作生成器内部如何传播、在哪里失真、如何对已定位的 signature 做最小干预**。这与方法层面的“用 reward 改善生成结果”不是同一个研究问题。

即使后续 MoDebug 使用 reward、ranking head 或 scorer，也不自动等于 ReAlign、RLHF 或 RL policy optimization。必须拆开说明：

1. reward 信号来源是什么；
2. reward 优化目标是什么；
3. reward 作用在文本侧、内部 trace、candidate rerank、采样步骤、还是模型参数；
4. 是否存在 policy、rollout、credit assignment、return optimization；
5. 是否使用同一 scorer 做 development tuning 与 final evaluation。

用户当前并不特别担心“都用 reward”会成为不可防守的攻击点，因为方法与 RL 范式可以通过 proof、mechanistic evidence 和评估隔离划清。但写作上仍需要预先封住审稿人把 MoDebug 压缩成“another reward-guided alignment method”的路径。

## 不可压缩边界

MoDebug 的不可压缩边界不是“提升 text-to-motion”，而是以下五件事的组合。

| 边界项 | MoDebug 必须保留的含义 | 被压缩后的危险写法 |
| --- | --- | --- |
| 诊断对象 | text condition 在 generator 内部的传播链 | 输出不好，所以加一个 reward 修正 |
| 机制证据 | projection、attention、hidden、logit、confidence、trajectory 等 trace | 只看最终 motion preference |
| signature | 多 prompt、seed、模型或 bucket 中复现的传播失真模式 | 观察到若干失败案例 |
| targeted minimal guidance | 针对 signature 的最小干预，位置和作用必须可解释 | 通用 reward / alignment guidance |
| 插件验证 | 同一 baseline 下比较 B 与 B+MoDebug 的 full-motion paired evaluation | 新 generator 或重新训练模型 |

主 claim 应写成：

```text
MoDebug diagnoses how text conditions propagate inside pretrained text-to-motion generators and applies signature-targeted minimal guidance to improve full-motion outputs.
```

不要写成：

```text
MoDebug proposes a new reward-guided text-to-motion generator.
```

## 与 ReAlign 的边界

[[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment|ReAlign]] 的核心是 **step-aware reward model + diffusion noisy motion reward-gradient guidance**：它训练一个能处理 noisy motion 的 reward model，在扩散每个 denoising step 中加入 reward gradient，使采样朝文本语义对齐和 motion realism 更高的方向移动。

MoDebug 不能被写成同类的全局 reward guidance。需要明确：

| 维度 | ReAlign | MoDebug 写作边界 |
| --- | --- | --- |
| 主对象 | noisy motion 上的 reward-guided sampling | text condition 在 generator 内部的传播与失真 |
| reward 位置 | denoising step 中对 noisy motion 求梯度 | 若使用 scorer，也应绑定 diagnostic、ranking、rerank 或 signature target |
| 方法形态 | 推理期全局 reward-gradient guidance | 机制诊断协议 + signature-targeted minimal guidance |
| 主要证据 | R-Precision、FID、MM Dist 等生成质量与对齐指标 | trace signature、paired B vs B+MoDebug、quality guardrail、cross-check |
| 可插拔含义 | diffusion sampler 外挂 reward gradient | 预训练生成器内部传播链上的最小插件干预 |

推荐相关工作写法：

```text
Reward-guided approaches such as ReAlign improve diffusion sampling by learning step-aware rewards over noisy motions. MoDebug addresses a different problem: it audits where textual conditions are weakened or misbound inside pretrained generators, then applies minimal interventions targeted to the diagnosed propagation signature.
```

禁止把二者边界写成“ReAlign 做 reward，MoDebug 不做 reward”。正确边界是：

```text
ReAlign globally guides noisy motion samples with reward gradients during diffusion; MoDebug localizes text-condition propagation failures and intervenes at the corresponding internal or sampling interface only after a signature is identified.
```

## Reward / RL 命名边界

写作中必须区分四类东西。

| 名称 | 可否叫 reward | 可否叫 RL | MoDebug 中的安全用途 | 必须说明的边界 |
| --- | --- | --- | --- | --- |
| diagnostic scorer | 可以叫 score，少用 reward | 不能 | 检查 trace、文本单元、motion cue 是否可分 | 不优化 policy，不作为 final evaluator |
| supervised reward / ranking head | 可以叫 supervised reward 或 preference/ranking scorer | 通常不能 | 学一个候选排序或质量估计器 | 数据来源、训练 split、held-out evaluator separation |
| inference-time reward guidance | 可以，但需限定作用位置 | 不能自动叫 RL | candidate rerank、sampling bias、局部 schedule 调整 | 是否求梯度、是否全局作用、是否影响 diversity |
| RL policy optimization | 可以 | 必须有 policy/rollout/return/credit assignment | 只有真的优化生成 policy 时才使用 | policy、rollout、credit assignment、train-test separation、evaluator separation |

### 什么时候不能叫 RL

以下情况不能写成 RL：

1. 只训练一个 supervised scorer 或 ranking head；
2. 只在 inference 时用 score 做 candidate rerank；
3. 只用 reward-like signal 选择 guidance strength；
4. 只把 human preference 当作 paired evaluator；
5. 只对 trace signature 做 deterministic 或 heuristic intervention。

这些最多叫 `reward-scored`、`reward-informed`、`preference-ranked`、`score-guided` 或 `inference-time reranking`，不能写成 policy optimization。

### 什么时候必须补充 RL 细节

如果论文中出现以下设计，就必须说明 policy / rollout / credit assignment / train-test separation / evaluator separation：

1. 用 reward 对 generator 参数做优化；
2. 用 sampling trajectory 当 rollout；
3. 对多步 generation 分配 credit；
4. 用同一 reward 同时训练、选择 checkpoint 和报告最终结果；
5. 声称 learning from preference 或 reinforcement learning 提升 instruction following。

最低记录字段：

```text
reward_source
reward_target
optimization_target
policy_definition
rollout_unit
credit_assignment
train_split
dev_split
test_split
final_evaluator
evaluator_overlap_check
limitations
```

## 当前 Claim 分级

### 当前安全 claim

这些 claim 可以进入 proposal、roadmap 或 related-work positioning：

1. MoDebug 的研究对象是 text condition 在预训练 text-to-motion generator 内部的传播。
2. MoDebug 当前 MVP 是插件式 paired evaluation：同一 baseline 下比较 `B` 与 `B+MoDebug` 的 full motion。
3. trace signal、embedding distance、VLM、PoseFix、geometry 和 human review 当前各有证据角色，不能互相替代。
4. motion-side grounding 是并行资产路线，不是 MVP 前置条件。
5. ReAlign 与 MoDebug 的直接重合不足以构成 pivot 理由；需要管控的是审稿人对 reward/alignment 方向的压缩。

### 需要证据后才能 claim

这些 claim 只有在对应证据齐全后才能写：

| Claim | 需要的最小证据 | 当前状态 |
| --- | --- | --- |
| B+MoDebug 优于 B | same prompt、same seed/candidate pool、same length/sampling budget、blind paired preference、quality guardrail | 需要正式 plugin eval |
| 某个 signature 稳定存在 | 至少跨两个模型、prompt bucket 或 seed group 复现 | 待 trace schema 与实验确认 |
| guidance 是 signature-targeted | 干预位置与 signature 一一对应，并有 ablation | 待 intervention artifact |
| instruction following 提升 | 独立 motion-side check 或 held-out evaluator，不与 dev scorer 重合 | 待 held-out evaluator |
| motion-side grounding 可用于训练 | coverage、一致性、start/end state、transition uncertainty、heldout start-state/composition 评估 | 并行验证中 |

### 禁止 claim

以下写法当前禁止：

1. MoDebug 是新的 text-to-motion generator。
2. MoDebug 是 ReAlign 式全局 reward-gradient guidance。
3. 当前 P1 diagnostic visualization 证明 `B+MoDebug` 优于 `B`。
4. train-source HumanML3D rows 支持 held-out generalization。
5. embedding distance 证明 motion instruction following 提升。
6. VLM / PoseFix / geometry 是最终 evaluator。
7. 同一个 scorer/protocol 既做 tuning 又做 final evaluator。
8. motion-side event grounding 可靠性通过前，把 grounded event 训练写成主方法依赖。
9. released pretrained checkpoints 已经是完全可信 foundation，除非有 clean upstream retrain sanity comparison。

## 风险登记表

表内只写简称；完整文档链接见上方“关联上下文”。

| 风险 | 触发方式 | 影响 | Mitigation | Proof artifact |
| --- | --- | --- | --- | --- |
| nearest-work compression | 审稿人把 MoDebug 压缩成 ReAlign/泛 reward alignment | novelty 被低估 | Related Work 明确“global reward-gradient sampling”与“mechanistic propagation debugging”的对象差异 | related-work boundary paragraph；ReAlign 对照表 |
| method ambiguity | guidance、reward、plugin、debugging 混用 | 方法像 post-hoc repair | 每个 intervention 记录 signature、target、作用位置、是否改参数 | intervention manifest；signature-to-target mapping |
| reward/RL naming | 写成 reward 后被追问是否 RL | 被要求 policy optimization 细节或 evaluator 隔离 | 统一用 scorer/ranking/guidance/RL 四分法 | reward_boundary section；reward_source/target schema |
| evaluator leakage | dev scorer 与 final evaluator 重合 | final claim 不可信 | dev scorer、selection scorer、final evaluator 分离 | evaluator_overlap_check；held-out evaluator protocol |
| phase1 train/test leakage | Phase1 train-source rows 被写成 generalization | 实验 claim 失真 | 每行保留 split_bucket/source_split/role/used_for | phase1_gt_sample_manifest；split contract |
| motion-side grounding overclaim | grounded event 被当作可靠训练标签 | 方法依赖不稳 | grounding 通过 coverage、一致性、start/end state、transition 后再进入训练 | grounding coverage report；state/composition heldout test |
| renderer/source-generation confound | 不同模型视频来自不同 runner、renderer、长度估计 | visual comparison 被误读 | 同 renderer 只控制可视化变量，source generation 差异单独记录 | unified-renderer run_record；source generation provenance |
| annotation cleaning | 人工标注重复、空描述或旧版本混入 | human eval 统计污染 | latest annotation table 为主，raw events 作 audit log | phase1_clean_human_annotations；annotation cleaning run_record |

## 论文写作边界句

### 可以写

```text
MoDebug studies text-condition propagation inside pretrained text-to-motion generators and uses the diagnosed propagation signatures to determine minimal guidance targets.
```

```text
Our current evidence separates diagnostic traces, side signals, quality guardrails, and final paired evaluation, so trace improvements are not reported as final motion-generation gains unless paired output evidence is available.
```

```text
Reward-guided diffusion methods such as ReAlign optimize sampling with reward gradients over noisy motions; MoDebug instead asks where textual constraints are lost or misbound inside the generator and intervenes only at the diagnosed interface.
```

```text
When a score or reward-like head is used, we treat it as a diagnostic, ranking, or inference-time guidance signal unless the method explicitly optimizes a policy with rollouts and credit assignment.
```

```text
Motion-side grounding is maintained as a parallel reliability asset and is not assumed to be a clean training signal before coverage, transition uncertainty, and state-conditioned held-out checks are reported.
```

### 不能写

```text
MoDebug is a reward-guided alignment method similar to ReAlign.
```

```text
MoDebug uses reinforcement learning to improve text-to-motion generation.
```

```text
The diagnostic P1 visualizations prove that MoDebug improves the baseline.
```

```text
Event-level motion grounding provides clean independent training samples.
```

```text
VLM/PoseFix scores are the final evaluator for instruction following.
```

```text
HumanML3D train-source Phase1 examples demonstrate held-out generalization.
```

## 最小后续动作清单

| 动作 | 对应文档/实验 | 完成后允许提升的 claim |
| --- | --- | --- |
| 固定 paired eval contract：blind pairwise、quality guardrail、side signal、same prompt/seed/length/sampling budget | Full-Text / Full-Motion 插件评估实验骨架 | 可以正式报告 B vs B+MoDebug 的实验入口 |
| 建立 intervention manifest：signature、target、作用位置、是否改参数、scorer 使用方式 | MoDebug 当前路线图；MoDebug Core Idea | 可以说 guidance 是 signature-targeted，而不是泛 reward guidance |
| 固定 trace schema：projection、attention、hidden、logit、confidence、trajectory 的字段和 role | MoDebug README；MoDebug Core Idea | 可以报告 mechanistic diagnostic evidence |
| 为 reward-like 组件补充四分法标签：diagnostic scorer、ranking head、inference guidance、RL policy optimization | 本文 Reward / RL 命名边界 | 可以降低 reward/RL naming risk |
| 把 Phase1 rows 的 split_bucket、source_split、text_origin、role、used_for 写入所有分析表 | Phase1/Phase2 Evaluation Data Split Contract | 可以防止 train/test leakage 与 annotation cleaning 混淆 |
| 对 unified renderer 结果保留 source generation provenance 和 renderer provenance | Full-Text / Full-Motion 插件评估实验骨架 | 可以说明 renderer 被控制，但 source generation confound 仍存在 |
| motion-side grounding 单独出 coverage、agreement、start/end state、transition uncertainty 报告 | MoDebug README；MoDebug 当前路线图 | 只有通过后才考虑训练依赖或细粒度解释 claim |
| Related Work 中加入 ReAlign boundary paragraph 与对照表 | ReAlign；本文与 ReAlign 的边界 | 可以主动处理 nearest-work compression |

## 写作总原则

MoDebug 的论文叙事要从“为什么文本条件在生成器内部失效”出发，而不是从“我们也有一个 reward 可以提升生成”出发。reward、scorer、ranking 或 guidance 都只能作为定位后的工具；主贡献必须落在可审计传播链、可复现 signature、signature-targeted minimal guidance，以及与最终 full-motion 输出的 paired evidence 之间的闭环。
