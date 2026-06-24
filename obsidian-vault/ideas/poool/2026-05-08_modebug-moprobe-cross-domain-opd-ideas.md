---
created: 2026-05-08T16:39:02+08:00
updated: 2026-05-10T15:05:26+08:00
title: MoDebug / MoProbe 交叉领域 OPD 与能力边界想法整理
status: draft
tags:
  - research-idea
  - MoDebug
  - MoProbe
  - on_policy_distillation
  - reinforcement_learning
  - capability_boundary
  - mechanistic_diagnosis
related_notes:
  - "[[ideas/MoDebug/README]]"
  - "[[paperIDEAs/MoDebug/2026-05-07_modebug-cross-generator-failure-mechanism-plan]]"
  - "[[2026-03-26_moprobe-capability-boundary-probing]]"
  - "[[2026-04-04_tamr-moprobe-mocritique-roadmap]]"
source_papers:
  - "[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Rethinking_On_Policy_Distillation_of_Large_Language_Models_Phenomenology_Mechanism_and_Recipe|Rethinking OPD]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Self_Distilled_Reasoner_On_Policy_Self_Distillation_for_Large_Language_Models|Self-Distilled Reasoner]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_SCOPE_Signal_Calibrated_On_Policy_Distillation_Enhancement_with_Dual_Path_Adaptive_Weighting|SCOPE]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Revisiting_On_Policy_Distillation_Empirical_Failure_Modes_and_Simple_Fixes|Revisiting OPD]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Unifying_Group_Relative_and_Self_Distillation_Policy_Optimization_via_Sample_Routing|SRPO]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_How_Do_Transformers_Learn_to_Associate_Tokens_Gradient_Leading_Terms_Bring_Mechanistic_Interpretability|Transformer Token Association]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling|MoGenTS]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Motion_R1_Enhancing_Motion_Generation_Decomposed_CoT_RL_Binding|Motion-R1]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2026/2026_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation|MoRL]]"
  - "[[paperAnalysis/Motion_Generation/arXiv_2025/2025_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_for_Text_to_Motion_Generation|IRG-MotionLLM]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/Qwen_2025/2025_Qwen3_Technical_Report|Qwen3 Technical Report]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/DeepSeek_2026/2026_DeepSeek_V4_Technical_Report|DeepSeek-V4 Technical Report]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_VideoZoomer_Reinforcement_Learned_Temporal_Focusing_for_Long_Video_Reasoning|VideoZoomer]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Q_Zoom_Query_Aware_Adaptive_Perception_for_Efficient_Multimodal_Large_Language_Models|Q-Zoom]]"
---

# MoDebug / MoProbe 交叉领域 OPD 与能力边界想法整理

> [!abstract] 结论先行
> `## My Note` 里的 OPD / self-distillation / sample routing / active perception 思路有机会服务 MoDebug 和 MoProbe，但不应直接改写成“给 MotionGPT 加 RL”。更稳的路线是先把这些工作抽象成四个可迁移算子：`on-policy state`、`teacher/student overlap`、`按样本状态路由监督`、`query-aware evidence acquisition`。  
> 对 MoDebug，它们最适合作为 failure signature 之后的训练-free reranking、token/mask guidance 或轻量 adapter 设计原则。对 MoProbe，它们更适合扩展 capability boundary：不仅问模型会不会，还问它是否能在更高预算、更强提示、自蒸馏或正确 sibling 条件下被解锁。

## 0. Scope

本文整理 [[paperIDEAs/MoDebug/2026-05-07_modebug-cross-generator-failure-mechanism-plan#My Note|MoDebug My Note]] 中若干交叉领域想法，回答三个问题：

1. 是否能服务 [[ideas/MoDebug/README|MoDebug]]。
2. 是否能服务 [[2026-03-26_moprobe-capability-boundary-probing|MoProbe]]。
3. 是否值得产生新的 paper idea。

边界：

1. 本文只做想法分流，不把任何 archived 或 side-signal 结果升级为当前结论。
2. `How_Do_Multimodal...pdf`、`How_does_the_optimizer...pdf`、`RL_Grokking...pdf`、`The_Hot_Mess...pdf` 在当前仓库文件名检索中没有定位到对应本地分析笔记，因此本文只把它们作为 `My Note` 中的启发问题，不作为已验证证据。
3. 表格中不放 aliased wikilinks；完整来源见 frontmatter `source_papers` 和正文列表。

## 1. Idea Decomposition and Association

### 1.1 可迁移算子

| Cross-domain source | 可迁移算子 | 对 motion 的含义 | 适合 MoDebug | 适合 MoProbe | teacher 依赖 |
| --- | --- | --- | --- | --- | --- |
| OPD | on-policy state + overlap region | 不在任意 motion token 上学 teacher，而是在 generator 自己会访问到的 motion-token / mask / candidate 状态上判断能否学 | 强 | 中 | 通常需要 teacher 或 privileged signal |
| Self-Distilled Reasoner | privileged self-teacher | 同一个 generator 在看到 GT event、正确 sibling、judge feedback 后，给自己的失败 rollout 做 dense supervision | 强 | 中 | 可去外部 teacher，但仍要 privileged context |
| SCOPE | 正确 / 错误双路径加权 | 正确但低置信样本强化边界能力；错误样本只在 teacher 低困惑度 / 低熵时蒸馏 | 强 | 强 | 错误支路需要可靠纠错信号 |
| SRPO | 按 rollout 学习状态路由 | 正确 motion 走 reward / preservation，错误且有正确 sibling 的 motion 走 token 级纠错 | 强 | 强 | 可用 sibling/self-teacher 替代外部 teacher |
| Transformer association | token association mechanism | 对 MotionGPT 做 event-token 到 motion-token 的关联扫描，但 attention 不是 judge | 中 | 强 | 不需要 teacher |
| Q-Zoom / VideoZoomer | query-aware evidence acquisition | 只对问题相关时间段 / body part / event 做高成本 judge 或 trace 采集 | 强 | 强 | 可自监督或用强模型蒸馏 |
| Qwen3 / DeepSeek-V4 | OPD 替代部分 RL 合版 | 长轨迹 / 多专家合并时，dense logit distillation 可能比纯 RL 更稳 | 中 | 弱 | 多 teacher 更常见 |
| scenario benchmark | 场景化任务暴露 hidden capability | motion+game / motion+X 可做 benchmark，但必须有真实任务约束，不是只跑模型列表 | 弱 | 强 | 不需要 teacher |
| model merging | skill fusion / adapter soup | 同架构 motion adapters 可合并，跨结构 generator 直接 merge 风险高 | 中 | 弱 | 不需要 teacher，但需要同构参数空间 |

### 1.2 一句话总判断

最有价值的不是“把 OPD 搬到 MotionGPT”，而是把 OPD 系列转成 MoDebug / MoProbe 的状态诊断问题：

```text
当前失败样本是不是模型已经接近正确支持集但没有分配好概率？
如果是，它适合 reranking / OPD / self-distillation / local guidance。
如果不是，它更可能是能力缺失或 teacher 不可靠，不应强行修。
```

这和 MoProbe 的 A/B/C taxonomy 对齐：

| MoProbe root cause | OPD 视角                                                    | MoDebug action                                             |
| ------------------ | --------------------------------------------------------- | ---------------------------------------------------------- |
| capability absence | student 和 teacher / correct sibling overlap 低，teacher 也高熵 | 不修或数据增强，不做 dense distillation                              |
| invocation failure | overlap 中等到高，但 full_text 没激活正确 event                      | prompt routing、candidate reranking、self-teacher correction |
| text ambiguity     | 多个正确支持集并存，teacher / judge 不稳定                             | 标为 ambiguous，不作为训练正负样本                                     |

## 2. Related-Work Support

### 2.1 OPD 系列给出的核心机制

本地 KB 的关键来源：

- [[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Rethinking_On_Policy_Distillation_of_Large_Language_Models_Phenomenology_Mechanism_and_Recipe|Rethinking OPD]]：成功 OPD 主要发生在 student-teacher 的高概率 overlap region；teacher 更强不等于更可蒸馏，teacher 必须在 student 已访问状态上提供新模式。
- [[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Self_Distilled_Reasoner_On_Policy_Self_Distillation_for_Large_Language_Models|Self-Distilled Reasoner]]：外部 teacher 不是 OPD 的本质；本质是在 student 自己 rollout 的 prefix 上得到更 informed 的 dense token distribution。
- [[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_SCOPE_Signal_Calibrated_On_Policy_Distillation_Enhancement_with_Dual_Path_Adaptive_Weighting|SCOPE]]：正确样本和错误样本需要不同监督；正确低置信样本要保留多样性，错误样本要过滤 teacher 不可靠纠错。
- [[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Unifying_Group_Relative_and_Self_Distillation_Policy_Optimization_via_Sample_Routing|SRPO]]：按 rollout 是否正确和是否有正确 sibling 路由到 GRPO 或自蒸馏，避免在所有样本上混合信号。

### 2.2 Motion 领域的可接入面

- [[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]：最像 OPD 的接入对象，因为它把 motion 离散成 token，并接入 T5 式 text-motion 统一词表；可以导出 motion token、logits、entropy、hidden states 后做 overlap / self-distillation 分析。
- [[paperAnalysis/Motion_Generation/CVPR_2024/2024_MoMask_Generative_Masked_Modeling_of_3D_Human_Motions|MoMask]]：适合把 OPD 的 `token prefix` 改写成 `masked token state`；关键证据不是下一 token，而是 masked position 的 top-k confidence、remasking 轨迹和 candidate set。
- [[paperAnalysis/Motion_Generation/NeurIPS_2024/2024_MoGenTS_Motion_Generation_based_on_Spatial_Temporal_Joint_Modeling|MoGenTS]]：适合把 OPD 的 token 支持集改写成 `time x joint` token cell 的局部支持集；天然服务 body part / temporal failure。
- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Motion_R1_Enhancing_Motion_Generation_Decomposed_CoT_RL_Binding|Motion-R1]]、[[paperAnalysis/Motion_Generation/arXiv_2026/2026_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation|MoRL]]、[[paperAnalysis/Motion_Generation/arXiv_2025/2025_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_for_Text_to_Motion_Generation|IRG-MotionLLM]]：证明 motion generation 已经进入 reasoning / reward / self-refinement 竞争区，但它们多是 standalone generator 或 training recipe，不是 MoDebug 的直接插件。

### 2.3 Mechanistic 与 active perception 的启发

- [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_How_Do_Transformers_Learn_to_Associate_Tokens_Gradient_Leading_Terms_Bring_Mechanistic_Interpretability|Transformer Token Association]] 支持一个谨慎观点：attention / association 可以作为候选证据定位器，但不能直接当 event failure judge。MoDebug 需要 counterfactual calibration。
- [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_VideoZoomer_Reinforcement_Learned_Temporal_Focusing_for_Long_Video_Reasoning|VideoZoomer]] 与 [[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Q_Zoom_Query_Aware_Adaptive_Perception_for_Efficient_Multimodal_Large_Language_Models|Q-Zoom]] 给 MoProbe / MoDebug 的最大启发是：不要对整段 motion 平均投入评估预算，而是按 query / event 动态选择时间段、关节或 token 区域。

## 3. For MoDebug

### 3.1 MoDebug-OPD：event-overlap routed self-distillation

核心假设：

```text
部分 event-level failure 不是能力缺失，而是 student 已经接近正确 motion-token 支持集，
但在 full/drop/replace/shuffle 条件下把概率质量分配错了。
```

对应 OPD 映射：

| OPD 概念               | MotionGPT 映射                                        | MoMask 映射                                             | MoGenTS 映射                              |
| -------------------- | --------------------------------------------------- | ----------------------------------------------------- | --------------------------------------- |
| student rollout      | base generator under full_text                      | iterative masked generation trajectory                | joint-time generation trajectory        |
| token prefix         | generated motion token prefix                       | current masked/unmasked token state                   | current time x joint token grid         |
| teacher distribution | privileged-context logits or correct sibling logits | correct candidate / lower-mask reference distribution | local joint-time reference distribution |
| overlap ratio        | student top-k motion tokens vs teacher top-k        | masked position top-k overlap                         | cell-wise top-k overlap                 |
| teacher entropy      | privileged teacher uncertainty                      | candidate / mask confidence                           | cell-wise uncertainty                   |
| correctness          | human / side-signal / paired prompt label           | same                                                  | same                                    |

最小实验不是训练，而是先做诊断：

1. 对 MotionGPT 跑 `full_text / drop_text / replace_text / shuffle_text` paired prompts，生成 `G=4` 到 `G=8` candidates。
2. 导出每步 motion token logits、top-k、entropy、sequence score。
3. 用 side signals 和少量人审标出：correct、omission、wrong-event、order failure、ambiguous。
4. 构造三种 teacher 候选：
   - external teacher：更强 motion LLM / MLLM judge / human label 只提供 label 或 preferred candidate；
   - self teacher：同一 MotionGPT 在 `prompt + event list + judge feedback / GT motion caption` privileged context 下重打分 student trajectory；
   - sibling teacher：同组候选中被 judge 认为正确或更好的 sibling。
5. 计算 overlap ratio、teacher entropy、student entropy、correctness 的相关性。

通过条件：

```text
正确或可修失败样本的 overlap 明显高于不可修失败；
teacher / self-teacher 在可修失败上的 entropy 更低；
overlap / entropy 能预测 reranking 或 guidance 是否有效。
```

如果这个条件不成立，不应进入 OPD 训练。那说明 motion-token dense supervision 的局部几何还没有被证实。

### 3.2 是否需要 teacher

需要区分三层：

| 用途                             | 是否需要 teacher                      | 可替代来源                                                                      |
| ------------------------------ | --------------------------------- | -------------------------------------------------------------------------- |
| MoDebug failure diagnosis      | 不一定                               | paired prompts、side signals、人审、trace contrast                              |
| candidate reranking / guidance | 不一定                               | TMR / ChronAccRet side signal、human calibration、小规模 judge                  |
| OPD / self-distillation 训练     | 需要广义 teacher signal               | external teacher、privileged self-teacher、correct sibling、GT motion context |
| 完全 teacher-free RL             | 不需要 teacher，但需要 reliable verifier | 仅当 reward / verifier 足够可信时可尝试                                              |

结论：外部 teacher 可以剔除，但 teacher signal 不能凭空消失。Self-Distilled Reasoner 和 SRPO 的启发是把外部 teacher 替换成 `privileged context` 或 `correct sibling`，不是让错误 rollout 自己无监督变好。

### 3.3 MotionGPT + RL 是否值得做

短期不建议直接做 `MotionGPT + GRPO` 主线。原因：

1. MoDebug 当前首要门槛是 M1 trace instrumentation 和 M2 failure family，不是训练 recipe。
2. Motion-R1 / MoRL / IRG-MotionLLM 已经把 motion LLM + CoT / GRPO / self-refinement 做成显性竞争线，直接跟随会失去 MoDebug 的机制诊断差异化。
3. 如果 verifier 不可靠，GRPO 会把 side signal 噪声强化成模型偏差。

更稳的路径：

```text
M1 trace -> M2 failure family -> M5a reranking -> M5b token/mask guidance
-> only if overlap diagnostic passes -> M5d lightweight adapter / OPD / routed RL
```

如果后续一定要引入 RL，建议采用 sample routing 而不是全样本 GRPO：

| Sample state                   | 监督方式                            | MoDebug 理由                |
| ------------------------------ | ------------------------------- | ------------------------- |
| correct + low entropy          | preserve / no update            | 已掌握，不要压缩多样性               |
| correct + high student entropy | weighted MLE / self-consistency | 边界正确样本，值得保留               |
| wrong + low teacher entropy    | OPD / token-level correction    | teacher 仍能纠错              |
| wrong + high teacher entropy   | reject / human / more evidence  | flawed-prefix trap，避免蒸馏噪声 |
| ambiguous                      | exclude from training           | 不把文本歧义当模型错误               |

### 3.4 OPD-style MoDebug 的潜在贡献句

可写方向：

```text
We show that event-level motion failures are not uniformly repairable:
only failures with high event-token / motion-token support overlap admit reliable process-time correction.
We therefore route candidate reranking, self-distillation, and adapter updates by failure state and teacher reliability.
```

不可写方向：

```text
We simply apply OPD / GRPO to MotionGPT and improve metrics.
```

## 4. For MoProbe

### 4.1 从“会不会”升级为“能否被解锁”

MoProbe 原始问题是 capability boundary：模型在哪里失败，为什么失败。OPD / RL grokking 的启发是把边界细分成四层：

| Boundary layer               | 判定问题                               | Probe protocol                     | 对 MoDebug 的意义      |
| ---------------------------- | ---------------------------------- | ---------------------------------- | ------------------ |
| raw capability               | base prompt 能否生成                   | normal prompt                      | 成功则无需修             |
| invocation capability        | 换词 / event list / CoT 后能否生成        | prompt rewrite / structured prompt | 适合 prompt routing  |
| budget-unlocked capability   | 多采样 / reranking / reflection 后能否生成 | G candidates + judge               | 适合 reranking       |
| training-unlocked capability | self-distillation / adapter 后能否生成  | small finetune / OPD diagnostic    | 适合训练型 intervention |
| absent capability            | 上述都失败                              | data / architecture audit          | 不适合 MoDebug 修复     |

这能让 MoProbe 不只是输出 `success rate`，而是输出 `unlockability map`：

```text
concept -> raw success -> prompt success -> rerank success -> self-distill success -> absence
```

这个 map 比普通 benchmark 更有下游价值，因为它直接告诉 MoDebug 哪些 failure 该修、该怎么修、哪些不该修。

### 4.2 Motion+Game / Motion+X benchmark 的机会

`My Note` 对 MLLM 场景 benchmark 的疑问是合理的：如果只是设计一个场景然后跑模型，很容易显得创新不足。它能被认可通常不是因为“场景新”本身，而是因为满足至少三个条件：

1. 场景暴露了通用 benchmark 看不到的能力缺口。
2. 任务协议能系统分解能力，而不是堆 case。
3. 结果能反推模型设计、训练数据或评估方法的改进。

Motion 领域中，`motion+game` 有机会，但要避开“游戏化展示”的浅层路线。它应该测的是可执行约束：

| Dimension | Game / interactive motion constraint | Why standard T2M misses it |
| --- | --- | --- |
| affordance | move, dodge, attack, interact with prop | HumanML3D caption 不要求动作对环境可执行 |
| timing | react within a window, hit after wind-up | FID / R-Precision 不测反应时序 |
| contact | foot/hand/object contact correctness | 文本相似不等于物理可用 |
| controllability | preserve style while changing target | 普通生成不测局部可控编辑 |
| failure recovery | after a bad partial motion, correct without whole regeneration | 普通 benchmark 不测修复性 |
| policy compatibility | motion can be consumed by downstream controller / game engine | 离线动画好看不等于可玩 |

适合落在 MoProbe，而不是 MoDebug：

```text
MoProbe-GameBench: probing whether motion generators understand executable action constraints in interactive scenes.
```

只有当该 benchmark 输出 repairability prior 后，才把它交给 MoDebug。

### 4.3 Mechanistic association probe

Transformer token association 工作给 MoProbe 一个新的诊断维度：

```text
event words 是否在 MotionGPT 内部关联到对应 motion token / time span？
```

可做黑盒到灰盒两级：

1. 黑盒：`full/drop/replace/shuffle` prompt 下输出是否变化。
2. 灰盒：MotionGPT trace 中 event token 与 motion token 的 attention / hidden-state / logit delta 是否变化。
3. 校准：只有当 trace delta 能预测人工或 side-signal failure，才把它记作 useful probe。

注意：attention 只说明 learned association，不说明 correctness。必须做 counterfactual calibration。

## 5. New Idea Candidates

### 5.1 Candidate A: MoRoute

工作名：

```text
MoRoute: Sample-Routed Self-Distillation for Event-Level Motion Generation Failures
```

核心：

```text
用 MoProbe / MoDebug 的 failure label 路由训练信号：
correct-boundary 样本保留多样性，wrong-but-repairable 样本做 token/mask correction，
ambiguous 或 non-repairable 样本不训练。
```

适合对象：

1. MotionGPT：motion-token logits。
2. MoMask：masked-token confidence 和 remasking。
3. MoGenTS：time-joint token cell。

最小贡献：

1. 将 OPD / SCOPE / SRPO 的 sample routing 迁移到 motion generation。
2. 明确 event-level failure 的 repairability boundary。
3. 避免把所有错误样本都当可蒸馏样本。

风险：

1. 需要可靠 correctness / failure labels。
2. 需要能导出 token logits 或 masked-token distributions。
3. 如果 overlap diagnostic 不成立，训练信号可能只是噪声。

优先级：中高。它是 MoDebug 后续方法层的自然候选，但必须在 M1/M2 后再启动。

### 5.2 Candidate B: MotionOPD without External Teacher

工作名：

```text
MotionOPD-ST: Privileged Self-Distillation for Motion Token Generators
```

核心：

```text
同一个 motion generator 扮演 student 与 privileged teacher。
student 只看原 prompt 生成失败 rollout；
teacher 看 event decomposition、GT motion context、judge feedback 或 correct sibling，
在 student rollout 上提供 dense token / mask supervision。
```

teacher 去除方式：

| External teacher version | Teacher-free / self-teacher version |
| --- | --- |
| stronger LLM gives CoT / token distribution | same MotionGPT with event list / GT caption context |
| MLLM judge gives correction | same model conditioned on judge feedback text |
| expert generator gives preferred motion | same-group correct sibling gives privileged context |
| human labels every case | human labels only calibrate small set, model self-distills remaining cases |

成立条件：

1. 模型在 privileged context 下真的更懂当前失败。
2. teacher distribution entropy 较低。
3. self-teacher 不只是复述错误 prefix。

优先级：中。适合作为去 teacher 的研究点，但需要先证明 privileged context 对 MotionGPT 有效。

### 5.3 Candidate C: MoProbe Unlockability Map

工作名：

```text
MoProbe-UL: Capability Boundary as Unlockability, Not Binary Success
```

核心：

```text
每个 motion concept 不只标记 success/fail，而是标记它在哪种预算下被解锁：
prompt rewrite、多采样、reranking、reflection、自蒸馏、小 adapter。
```

贡献：

1. 让 MoProbe 从 benchmark 变成 diagnostic protocol。
2. 直接服务 MoDebug 的 repairability prior。
3. 可以吸收 RL grokking / capability boundary 的思想：能力可能已潜伏但需要 post-training 或 test-time compute 解锁。

优先级：高。它不依赖复杂训练，最适合作为 MoProbe 的增强方向。

### 5.4 Candidate D: Motion+Game Capability Benchmark

工作名：

```text
MoActBench: Probing Executable Action Understanding in Text-to-Motion Generators
```

核心：

```text
把 motion generation 放进可执行交互场景，测试模型是否理解动作 affordance、时序窗口、接触、目标约束和 failure recovery。
```

关键不是做漂亮游戏 demo，而是让 game / simulator 提供标准 HumanML3D 不具备的可验证约束。

最小版本：

1. `20` 个原子场景：dodge、hit、pick、kick、jump-over、turn-react。
2. 每个场景构造 `full/drop/replace/shuffle/negation/count` variants。
3. 输出 motion 后用规则 + MLLM / human 做双层评估。
4. 报告 failure taxonomy、capability map、unlockability map。

优先级：中。适合另开 benchmark 线，但成本和资产建设高于 MoProbe-UL。

### 5.5 Candidate E: Motion Adapter Merging

工作名：

```text
MoMerge: Skill Adapter Merging for Motion Token Generators
```

核心：

```text
不是跨架构 merge MotionGPT / MoMask / MoGenTS，而是在同一 backbone 上训练多个 small adapters，
例如 locomotion、hand interaction、temporal ordering、style，再做 adapter merge / routing。
```

判断：

1. 直接跨模型、跨数据集、跨架构 merge 风险很高，当前不适合作为 MoDebug / MoProbe 主线。
2. 同架构 LoRA / adapter merging 有机会作为 MoDebug 的后续 intervention 层。
3. 它更像工程补强，不像当前最高价值研究问题。

优先级：低到中。除非已经有同 backbone 多 adapter 资产，否则不建议近期推进。

## 6. Priority Recommendation

| Priority | Direction | Why now | Minimal next action |
| --- | --- | --- | --- |
| P0 | MoProbe Unlockability Map | 直接增强 MoProbe，不依赖训练，能服务 MoDebug repairability | 在 MoMask 或 MotionGPT 上做 50 到 100 条 prompt 的 raw / rewrite / rerank / reflection 对比 |
| P0 | MotionGPT OPD diagnostic | 决定 OPD / self-distillation 是否有局部几何基础 | 导出 logits/top-k/entropy，计算 full/drop/shuffle/replace 的 overlap 与 failure label 相关性 |
| P1 | MoRoute sample routing | 如果 P0 成立，可自然变成 MoDebug 方法层 | 先做 candidate reranking routing，不直接 finetune |
| P1 | Query-aware temporal / body-part evidence | 能同时服务 MoProbe judge 和 MoDebug localization | 设计 event query -> suspicious interval/body-part 的 sidecar，不作为 final judge |
| P2 | Motion+Game benchmark | 可能形成新 benchmark，但资产成本高 | 先写 20 场景 spec，验证是否真的超出 HumanML3D 常规评估 |
| P3 | adapter / model merging | 需要同构 adapter 资产，短期不清楚收益 | 暂存，不进入当前 MoDebug 主线 |

## 7. Concrete Next Experiments

### 7.1 MotionGPT OPD diagnostic pilot

目标：判断 OPD 系列是否真能迁移到 MotionGPT。

数据：

1. `30` 个 HumanML3D-E 多事件 prompts。
2. 每个 prompt 构造 `full_text / drop_text / replace_text / shuffle_text`。
3. 每个 condition 采样 `G=4` 到 `G=8`。

记录：

1. generated motion tokens；
2. per-step top-k logits；
3. token entropy；
4. sequence score；
5. static skeleton / video；
6. side-signal score；
7. 小样本人审 label。

输出指标：

```text
motiongpt_full_drop_overlap_ratio
motiongpt_failure_teacher_entropy
motiongpt_correct_low_confidence_rate
motiongpt_wrong_low_teacher_entropy_rate
motiongpt_overlap_vs_repairability_auc
```

注意：所有指标必须记录 evaluator、protocol、n、coverage、role 和 limitations，不能写裸 `drop=` 或 `full>drop=`。

### 7.2 MoProbe unlockability pilot

目标：把 MoProbe 从 success/fail 扩展为 unlockability。

每个 probe concept 跑四种预算：

1. raw prompt；
2. structured event prompt；
3. multi-sample reranking；
4. self-reflection / privileged feedback prompt。

标签：

```text
raw_success
prompt_unlocked
rerank_unlocked
reflection_unlocked
still_failed
ambiguous
```

解释：

1. `prompt_unlocked` 更像 invocation failure。
2. `rerank_unlocked` 更像 latent capability。
3. `still_failed` 更像 capability absence 或数据缺失。
4. `ambiguous` 不能进入 MoDebug 训练。

### 7.3 Teacher ablation

同一批 MotionGPT failures 比较四种 teacher signal：

| Signal | Purpose |
| --- | --- |
| no teacher, side-signal reranking only | 训练-free 下限 |
| external judge preference | 强 teacher 上限 |
| same-model privileged context | 去外部 teacher 的关键 |
| correct sibling self-teacher | SRPO-style 最贴近 on-policy |

通过标准：

```text
self-teacher 接近 external judge 的 reranking / correction 效果，
且 teacher entropy 能过滤失败纠错信号。
```

## 8. Risks

| Risk | Severity | Mitigation |
| --- | --- | --- |
| motion token 没有清晰 event semantics | high | 先做 overlap / trace diagnostic，不先训练 |
| teacher 在坏 motion prefix 上高熵 | high | SCOPE/SRPO 式 entropy / PPL filtering |
| MLLM judge 不可靠 | high | 小样本人审 anchor，automatic scorer 只作 side signal |
| benchmark 场景只是包装 | medium | 必须有 executable constraints 和 failure taxonomy |
| OPD 压缩多样性 | medium | 正确低置信样本走 diversity-preserving route |
| model merging 跨架构不可行 | medium | 只考虑同 backbone adapter merge |
| MoDebug 滑向 Motion-R1 / MoRL 竞争正面战场 | high | 保持机制诊断 + cross-generator plugin 定位 |

## 9. Working Decision

短期建议：

1. **MoProbe 先做 unlockability map**：这是最容易从 `My Note` 中形成独立价值的方向。
2. **MoDebug 先做 OPD diagnostic，不做 OPD training**：先证明 overlap / entropy / repairability 的关系，再考虑 MoRoute。
3. **teacher 不必是外部大模型，但必须有 privileged signal**：可用 GT event、correct sibling、judge feedback 或同模型 privileged context 替代。
4. **Motion+Game 是潜在新 benchmark，不是当前 MoDebug 的必需模块**：除非能定义可执行约束和可复现实验，否则先不投入主线。
5. **model merging 暂不作为核心**：仅保留为同 backbone adapter 层的后续可能。

最强的下一篇 idea 形态可能不是“MotionGPT + RL”，而是：

```text
MoProbe-UL -> identifies unlockable failures.
MoDebug/MoRoute -> routes only unlockable failures into reranking, self-distillation, or lightweight intervention.
```

这条线保留了 MoProbe 的诊断价值，也给 MoDebug 一个比直接套 GRPO 更清晰的机制贡献。

---

## 10. 2026-05-10 Addendum: MotionGPT T5, Qwen, and MLLM Decision

> [!abstract] 结论先行
> 不建议把 MotionGPT 的 Flan-T5 直接平替成同参数量的 Qwen decoder-only LLM。MotionGPT 当前的核心不是普通文本编码器，而是一个 T5-style text-motion seq2seq translator：统一文本词表和 motion token 词表，并用 encoder-decoder 结构覆盖 text-to-motion、motion-to-text、prediction、inbetweening 与 span corruption 式预训练。更有价值的路线是保留可检查的 motion-token translator，把 Qwen / MLLM 放在 prompt rewrite、duration planning、condition variant generation、trace explanation、active perception sidecar 或视觉化 motion understanding 中。

### 10.1 Scope

本节回答三个问题：

1. MotionGPT 的 Flan-T5 是否可以直接替换为 Qwen 0.5B / 0.8B 这类 decoder-only LLM。
2. 如果引入 MLLM 视觉能力，哪些是真问题，哪些只是概念拼装。
3. 当前 MoDebug / MoProbe 最小可执行验证应该怎么做，且不训练新的 Qwen-motion 大模型。

边界：

1. 本节不把 TMR、ChronAccRet、MLLM sidecar、人审以外的自动信号写成 final evaluator。
2. 本节不声称 Qwen 或 MLLM 不能用于 motion；只否定“直接替换 MotionGPT 的 T5 translator 会自然提升”这个假设。
3. 本节使用 DeepSeek 多轮讨论作为设计压力测试，但结论以本地 `paperAnalysis` 证据和当前 MoDebug 资产为准。

### 10.2 Architecture Decision

短期决策：

```text
Do not directly replace MotionGPT's Flan-T5 with a Qwen decoder-only LLM.
Treat Qwen / MLLM as a planner, condition augmenter, sidecar, or later adapter candidate.
```

关键理由：

1. MotionGPT 的 Flan-T5 是 task translator，不只是 text encoder。它把 motion token 并入 T5 词表，用 encoder-decoder 统一 text-to-motion、motion-to-text、motion prediction、motion inbetweening。
2. Qwen 0.5B / 0.8B 是 decoder-only。直接加入 motion token 后，需要重做 tokenizer embedding 初始化、position / modality boundary、causal mask、训练目标和 decoding protocol；这不是平替。
3. 相近参数量不等于相近归纳偏置。Flan-T5-base 约 220M，但 encoder-decoder 对双向文本理解和条件生成更经济；Qwen 小模型参数更大也不保证 motion-token alignment 更稳。
4. 现有强工作不是简单换 backbone。MG-MotionLLM 仍走 T5-based 统一框架；ScaMo 是冻结 T5-XL 词级前缀 + AR motion transformer；MoLingo 证明 multi-token cross-attention 条件注入显著影响结果；HY-Motion 把 Qwen3 用作 token-level semantic、prompt rewrite 和 duration prediction，而不是替换成统一 motion translator。
5. MECo 是支持 Qwen 小模型接 motion token 的重要正例，但它的关键不是“Qwen 天然更强”，而是三阶段 token embedding 初始化和知识保护。该文反而提醒：直接把新 token 塞进 LLM 会带来知识遗忘和训练不稳定。

### 10.3 Related-Work Support

T5 / T5-conditioned 路线：

1. [[paperAnalysis/Motion_Generation/NeurIPS_2023/2023_MotionGPT_Human_Motion_as_Foreign_Language|MotionGPT]]：`core_operator` 是运动词表扩展 + T5 预训练；`primary_logic` 是 VQ-VAE motion token、文本 token、统一词表、Flan-T5 encoder-decoder。
2. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_MG_MotionLLM_A_Unified_Framework_for_Motion_Comprehension_and_Generation_across_Multiple_Granularities|MG-MotionLLM]]：用 T5-based 运动感知语言模型做粗/细粒度任务协同，说明 T5 仍是 motion language 的强基线。
3. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_ScaMo_Exploring_the_Scaling_Law_in_Autoregressive_Motion_Generation_Model|ScaMo]]：冻结 T5-XL 词级前缀，再接 AR motion transformer；它支持 scaling，但不是 decoder-only LLM 平替。
4. [[paperAnalysis/Motion_Generation/CVPR_2026/2026_MoLingo_Motion_Language_Alignment_for_Text_to_Motion_Generation|MoLingo]]：T5-Large + 多 token cross-attention 显著优于单 token 条件注入，提示瓶颈在 condition interface，而不是“文本模型名字”。

Qwen / MLLM 的有效接入面：

1. [[paperAnalysis/Motion_Generation/Tencent_HY/2025_HY_Motion_1_0_Scaling_Flow_Matching_Text_to_Motion|HY-Motion 1.0]]：Qwen3-8B 提供 token-level semantic，CLIP-L 提供 global semantic，Qwen3-30B-A3B 做 prompt rewrite / duration prediction；这是 planner / conditioner 模式。
2. [[paperAnalysis/Motion_Generation/SIGGRAPH_2025/2025_MECo_Motion_example_controlled_Co_speech_Gesture_Generation_Leveraging_Large_Language_Models|MECo]]：Qwen2.5-0.5B 可接运动和音频 token，但依赖三阶段初始化，且核心贡献之一是避免新增 token 破坏 LLM 原有能力。
3. [[paperAnalysis/Motion_Generation/ECCV_2024/2024_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts|MotionChain]]：把文本、图像、历史 motion VQ token 统一到 MLLM 对话序列中，适合 multi-turn / history-conditioned motion control。
4. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_LLaMo_Human_Motion_Instruction_Tuning|LLaMo]]：对 motion understanding，连续 motion 表示 + 视觉特征融合能避免离散 token 损失。
5. [[paperAnalysis/Motion_Generation/CVPR_2024/2024_MotionPatch_Exploring_Vision_Transformers_3D_Human_Motion_Language_Models_Motion_Patches|MotionPatches]]：motion patch pseudo-image + ImageNet ViT 预训练支持数据稀缺下的 motion-language retrieval，但它是 global representation，不提供 MotionGPT 式 token-level generation trace。
6. [[paperAnalysis/Motion_Generation/arXiv_2026/2026_SkeletonLLM_Universal_Skeleton_Understanding_via_Differentiable_Rendering_and_MLLMs|SkeletonLLM]]：DrAction 可微渲染把 skeleton 接到 MLLM 视觉通道，适合理解与跨格式迁移，不直接解决 text-to-motion generation。

### 10.4 Candidate Ideas

**MoDebug: No-New-Model T5-vs-Qwen Decision Probe**

目标：

```text
不训练新的 Qwen-motion 模型，也能给出“是否值得直接替换”的可复查证据。
```

现有资产：

1. MotionGPT / MoMask / MoGenTS 的 M0_v2 battery 已闭合。
2. MotionGPT stage2 retrain 正在 remote4090 跑，作为训练链 sanity，不作为方法效果。
3. MoMask / MoGenTS fullvis 正在或已完成，服务 renderer stability 和 artifact readiness。
4. M1 trace instrumentation 是下一步，用于导出 logits、entropy、hidden states、mask confidence、joint-time evidence。

最小闭环：

1. 选 30 条 complex event prompts，覆盖顺序、否定、duration、body part、方向反转、并行事件。
2. 为每条 prompt 构造 3 类 condition variants：original full text；MLLM / Qwen text-only rewrite；causal-prefix shadow，只给前 30%、60%、100% token。
3. 用现有 MotionGPT、MoMask、MoGenTS 推理，不训练新模型。
4. 记录 event-level output、M1 trace、candidate score、side signals。
5. 只回答一个二元问题：T5 当前结构是否已经在 surface-form robustness 和 event consistency 上足够稳定；若是，直接换 Qwen 没有证据收益。

**MoProbe: Unlockability Map for Motion-Language Interfaces**

MoProbe 可以把“模型会不会”升级为“能力能否被条件接口解锁”：

```text
raw prompt -> structured event prompt -> rewritten prompt -> multi-sample rerank
-> trace-guided condition -> adapter / distillation candidate
```

这比直接比较 T5/Qwen 更有价值，因为它输出的是 repairability prior：哪些 failure 属于 prompt / condition interface，哪些属于 motion representation 或 generator backbone。

**New Direction: Motion-to-Vision Sidecar for Evidence Acquisition**

把 MotionPatches 与 SkeletonLLM 的思路合并成一个 sidecar：

```text
generated skeleton -> pseudo-image / differentiable render -> MLLM / ViT evidence
-> event span proposal / body-part proposal / ambiguity flag
```

用途：

1. 给 MoDebug 提供高成本评估预算的 routing。
2. 给人审界面提供候选 event spans。
3. 为 MoProbe 标注哪些 prompt 需要视觉 grounding。

硬约束：

1. Sidecar 不做 final judge。
2. Sidecar 输出必须带 coverage、uncertainty、failure mode。
3. Sidecar 不能替代 MotionGPT / MoMask / MoGenTS 的 native trace。

**New Direction: Hybrid Planner-Generator Motion LLM**

如果未来要真正用 Qwen，建议不要平替 MotionGPT，而是做 hybrid：

```text
Qwen planner: event list + duration + body-part constraints
native generator: MotionGPT / MoMask / MoGenTS generation
trace monitor: detects event omission / order failure
repair controller: rerank or condition edit
```

这条路线比“Qwen 直接吐 motion token”更稳，因为 Qwen 做它擅长的语言规划，motion generator 做它擅长的低维运动生成。

### 10.5 Recommended Next Experiment

Name:

```text
EXP-CLINCH: No-New-Model Verification for T5-vs-Qwen Decoder-Only
```

Protocol:

1. Build a 30-prompt `T5_Qwen_decision_probe` from existing M0_v2 dimensions plus new negation/duration/body-part cases.
2. Generate original and 3 text-only variants per prompt.
3. Run MotionGPT / MoMask / MoGenTS with 1-3 seeds each.
4. Export native outputs and M1 trace if available.
5. Compute event count consistency, order consistency, variant divergence, trace entropy / confidence shift, and small human spot-check on high-divergence cases.
6. Write a decision memo: keep T5 translator; use Qwen / MLLM as condition-side planner and sidecar; postpone Qwen-motion training unless the probe reveals a condition interface bottleneck that T5 cannot resolve.

Success criteria:

| Outcome | Decision |
| --- | --- |
| low variant divergence, low full-mode failure | do not replace; T5 is sufficient for current MoDebug |
| high variant divergence across all generators | focus on prompt/condition robustness, not Qwen replacement |
| high MotionGPT-specific divergence with trace evidence | improve MotionGPT condition interface or adapter; still not direct Qwen replacement |
| sidecar detects useful spans but disagrees with human often | use sidecar only for routing and UI, not scoring |

Revisit Qwen-motion training only if all conditions hold:

1. Current T5-based translator fails on complex event prompts even after structured event input.
2. Failure is not explained by motion tokenizer quality or decoder limitation.
3. There is a reliable training signal beyond weak MLLM judgment.
4. A MECo-style token initialization and knowledge-preservation plan is available.
5. The target task needs Qwen-specific language or reasoning capability, not merely a larger text model.

### 10.6 Drift Note

old_plan: consider replacing MotionGPT's T5 translator with same-scale Qwen or adding MLLM visual ability as a likely capability upgrade

new_plan: keep MotionGPT's T5 translator as the mechanism-probe backbone for now; evaluate Qwen / MLLM as condition planner, variant generator, active perception sidecar, or future adapter candidate only after M1 trace and event-level robustness probes

evidence: MotionGPT / MG-MotionLLM / ScaMo / MoLingo preserve T5-style or T5-conditioned interfaces; HY-Motion uses Qwen as semantic conditioner and prompt planner; MECo shows Qwen small LLM can work only with careful token initialization; MotionPatches and SkeletonLLM support visual/MLLM sidecars for representation and understanding, not direct MotionGPT translator replacement

affected_docs: [[ideas/MoDebug/README]], [[paperIDEAs/MoDebug/2026-05-07_modebug-cross-generator-failure-mechanism-plan]], future M1 trace instrumentation notes

next_action: create `T5_Qwen_decision_probe` prompt set after M1 trace export path is stable; keep MLLM outputs labeled as `side_signal` or `condition_variant`, never `formal_ordering_evidence` or `heldout_final_evaluator`
