---
created: 2026-04-29T23:40
updated: 2026-04-29T23:40
title: MoDebug Plan B 核心参考工作阅读清单（归档）
status: archived
tags:
  - MoDebug
  - reading-list
  - plan-b
  - event-level-reward
  - reward-guidance
related_notes:
  - "[[2026-04-29_modebug-roadmap]]"
  - "[[2026-04-29_modebug-exec-plan]]"
  - "[[2026-04-29_modebug-full-vs-event-level-alignment-analysis]]"
  - "[[2026-04-29_modebug-evaluator-status-summary]]"
  - "[[2026-04-29_modebug-attention-filter-evaluator-pipeline-update]]"
  - "[[2026-04-26_modebug-plan-b-core-reading-list]]"
---

# MoDebug Plan B 核心参考工作阅读清单（归档）

> [!abstract] **TL;DR**
> - 这份 note 是 archived reading-list 草稿，不作为当前 MoDebug roadmap / exec 的权威入口。
> - 当前 active 入口以 `2026-04-29_modebug-roadmap`、`2026-04-29_modebug-exec-plan`、`2026-04-29_modebug-attention-filter-evaluator-pipeline-update` 为准。
> - 当前最核心的机制阅读顺序：`AToM -> ReAlign -> MotionCritic -> PAPO -> EasyTune`。
> - 当前上调为**高参考补充层**的工作：`APPO / PRCO / VideoZoomer / Perception-R1`。
> - 当前保留但降权为**背景 / fallback / 历史线**的工作：`SoPo / HuTuDiffusion`。
> - 当前只在需要补 RL mechanics 时再读：`AVATAR / DIVA-GRPO / GVPO`。
> - 继续保留**排除性阅读**：`Motion-R1 / MoRL / IRG-MotionLLM`，用于防止主线滑向 CoT-RL 或交错修正 pipeline。

## 0. 这份清单服务于哪个 Plan B

当前 `MoDebug` 正式主线以 [[2026-04-29_modebug-roadmap|Roadmap]] 为准：

> `Event-T2M + HumanML3D-E + inference-time event-level reward guidance`

当前固定问题与边界：

1. 主问题是 `ordering / omission`，`duration` 仍然是 later，不抢 MVP。
2. 当前正式 evaluator 栈是 `Event-T2M self eval + native TMR omission side signal + ChronAccRet ordering evidence / omission cross-check`。
3. attention filter 现在已经是 active 支线，因此“关键区间 / temporal focus / evaluator routing”相关论文的参考权重需要上调。
4. 当前不是后训练主线，不是 PRCO 式双角色主框架，也不是 Motion-R1 / MoRL 那种 CoT-RL 主体。

所以这份清单不是泛泛的 “motion RL papers list”，而是只围绕下面五个问题服务：

1. **事件级 reward 到底该怎么定义？**
2. **推理期 guidance 在 noisy denoising states 上到底怎么落地？**
3. **为什么 reward 不能只给单一总分，而要拆成 family？**
4. **关键区间 / temporal focus / evaluator routing 到底该从哪些工作借逻辑？**
5. **怎样避免方案被 reviewer 误判成 AToM + ReAlign 拼接，或滑向完整 RL/agentic pipeline？**

### 0.1 和归档清单的关系

`[[paperIDEAs/MoDebug/archived/related_work_and_backbone_comparison/2026-04-26_modebug-plan-b-core-reading-list|2026-04-26 归档阅读清单]]` 保留为历史快照，不再修改。

这份 active 更新版相对旧清单的变化是：

1. **保留原清单有效骨架**：
   - `AToM / ReAlign / MotionCritic / SoPo / HuTuDiffusion / EasyTune / PAPO / APPO / PRCO / Motion-R1 / MoRL / IRG-MotionLLM` 继续保留
2. **上调参考权重**：
   - `PAPO` 从“迁移创新来源”上调到“直接影响机制设计”
   - `EasyTune` 从“第二层补充”上调到“核心 step-aware 对照”
   - `APPO / PRCO` 从“以后再看”上调到“当前高参考补充”
3. **新增当前更值得同步的工作**：
   - `VideoZoomer`
   - `Perception-R1`
   - `AVATAR`
   - `DIVA-GRPO`
   - `GVPO`
4. **降权但不删除**：
   - `SoPo / HuTuDiffusion` 仍保留，但当前主要承担背景比较、fallback 与历史线作用

## 1. 最短阅读路线

### 1.1 如果时间只够读 4 篇

按这个顺序：

1. `AToM`
2. `ReAlign`
3. `MotionCritic`
4. `PAPO`

读完这 4 篇，基本就能回答：

- 为什么 Plan B 需要“事件级”而不是只有全局 reward
- 为什么 Plan B 应该优先是 inference-time，而不是先走后训练
- 为什么 `R_k` 不能停留在单一标量，而需要继续拆成 `R_pres / R_ord / R_dur`
- 为什么“感知增强”不能只停留在 slogan，必须和 reward family 绑定

### 1.2 如果可以读到 6 篇

在上面 4 篇后面补：

5. `EasyTune`
6. `APPO`

这样你会多回答两件事：

- `step-aware` 到底改变了什么，而不只是一个 engineering trick
- “关键局部 / 关键区间”为什么值得进入 evaluator routing 或 interval mining

### 1.3 如果你要直接对接当前 active root notes

再补：

7. `PRCO`
8. `VideoZoomer`

这样你就能更直接读懂：

- observer-style evidence 是否值得以后引入
- temporal zoom / focus / query-aware routing 对当前 attention filter 支线意味着什么

### 1.4 如果你在评估 fallback 或历史对照

再补：

9. `SoPo`
10. `HuTuDiffusion`

这样你会更清楚：

- 为什么当前不先押 post-training preference optimization
- 为什么“不改主模型参数也能提升生成”这条历史线早已有先例

## 2. 更新后的推荐阅读顺序

| 顺序  | 论文            | 当前角色                    | 思考                                                                                                                                       |
| --- | ------------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | AToM          | 核心机制层                   |                                                                                                                                          |
| 2   | ReAlign       | 核心机制层                   | MoDebug是否可以同时提供推理和训练阶段的reward设置？但这算不上独立贡献，只是两种适配而已                                                                                       |
| 3   | MotionCritic  | 核心机制层                   |                                                                                                                                          |
| 4   | PAPO          | 核心机制层                   | MoDebug的reward可以在哪些维度细分：1. temporal：output/event/frame；2. token级别，spatio-temporal具体而定；3. diffusion step；4. net layer；5. sampling的CFG或许也行 |
| 5   | EasyTune      | 核心机制层                   |                                                                                                                                          |
| 6   | APPO          | 高参考补充层                  |                                                                                                                                          |
| 7   | PRCO          | 高参考补充层                  |                                                                                                                                          |
| 8   | VideoZoomer   | 高参考补充层                  |                                                                                                                                          |
| 9   | Perception-R1 | 高参考补充层                  |                                                                                                                                          |
| 10  | SoPo          | 背景 / fallback           | 现有alignment/preference RL工作的奖励是整个模型级别的（train、单步采样），但没有探索模型参数分层级别的，==这就是机会==                                                              |
| 11  | HuTuDiffusion | 背景 / 历史线                |                                                                                                                                          |
| 12  | AVATAR        | RL mechanics supplement |                                                                                                                                          |
| 13  | DIVA-GRPO     | RL mechanics supplement | advantage vanishing 与难度自适应                                                                                                               |
| 14  | GVPO          | RL mechanics supplement | GRPO 类方法为何持续被改                                                                                                                           |
| 15  | Motion-R1     | 排除性阅读                   | 不要滑向 LLM-CoT-RL motion 主框架                                                                                                               |
| 16  | MoRL          | 排除性阅读                   | 不要扩成统一 motion reasoning framework                                                                                                        |
| 17  | IRG-MotionLLM | 排除性阅读                   | 不要滑向生成-评估-修正 agent pipeline                                                                                                              |

## 3. 核心机制层：直接决定当前 Plan B 设计

对应笔记：

- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward|AToM]]
- [[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment|ReAlign]]
- [[paperAnalysis/Motion_Generation/ICLR_2025/2025_MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions|MotionCritic]]
- [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_Perception_Aware_Policy_Optimization_for_Multimodal_Reasoning|PAPO]]
- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Generation|EasyTune]]

### 3.1 AToM

阅读重心：

- 它怎样把事件级对齐拆成 `完整性 / 时序 / 频率`
- 它的“事件级 reward”是 unary event 分数，还是已经带 relation
- GPT-4V 标注链路里，哪些部分是 Plan B 能继承的，哪些部分太贵

你读完后要得到的结论：

- `R_pres / R_ord / R_dur` 里，哪些维度已经在 AToM 有原型
- 如果不用 GPT-4V，Plan B 失去了哪一层 guarantee

### 3.2 ReAlign

阅读重心：

- reward model 为什么必须 `step-aware`
- reward gradient 是怎么插进每个 denoising step 的
- noisy motion 上 reward 的稳定性和 sampling dynamics 是怎么处理的

你读完后要得到的结论：

- Plan B 的 inference-time guidance 最接近哪一段 ReAlign 公式 / 实现逻辑
- 如果从全局 reward 切到事件级 reward，最先会在哪个环节失稳

### 3.3 MotionCritic

阅读重心：

- “感知质量”与“文本事件对齐”为什么不是一回事
- critic 型 reward 适合做什么，不适合做什么
- 为什么不能拿一个全局 critic 同时证明 ordering / duration

你读完后要得到的结论：

- Plan B 至少要拆成“事件语义对齐”和“整体感知质量”两层
- `R_pres / R_ord / R_dur` 不能被一个单标量 perceptual score 替代

### 3.4 PAPO

阅读重心：

- 为什么 outcome-only reward 会压坏感知
- 感知奖励和推理奖励怎样分离
- “67% 错误来自感知”这类诊断式论证怎么组织

你读完后要得到的结论：

- 为什么单一 `R_k` 继续细分是合理的，不是 overdesign
- 为什么 reward family 的拆分本身就是重要机制，不只是评估附属品

### 3.5 EasyTune

阅读重心：

- step-aware 为什么能缓解全轨迹优化的梯度稀疏
- 每步更新和最终 reward 的关系
- 它和 ReAlign 的最大边界：一个是 post-training，一个是 inference-time

你读完后要得到的结论：

- `step-aware` 改变的是 reward 与 denoising 的对齐方式，不只是节省显存
- Plan B 可以引用它解释“为什么我们也要 step-aware”，但主线仍应保留在 plug-and-play guidance

## 4. 高参考补充层：当前比旧清单更值得同步的工作

对应笔记：

- [[paperAnalysis/Vision_Language_Reasoning/CVPR_2026/2026_APPO_Attention_guided_Perception_Policy_Optimization_for_Video_Reasoning|APPO]]
- [[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Seeing_with_You_Perception_Reasoning_Coevolution_for_Multimodal_Reasoning|PRCO]]
- [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_VideoZoomer_Reinforcement_Learned_Temporal_Focusing_for_Long_Video_Reasoning|VideoZoomer]]
- [[paperAnalysis/Vision_Language_Reasoning/NeurIPS_2025/2025_Perception_R1_Pioneering_Perception_Policy_with_Reinforcement_Learning|Perception-R1]]

### 4.1 APPO

阅读重心：

- attention map 怎样变成关键帧 / 关键局部弱监督
- 感知奖励如何只针对“关键局部”而非整个输入

当前为什么上调：

- `MoDebug` 已经有 active 的 attention filter / interval miner 支线
- APPO 不再只是 future idea，而是当前 query-aware routing 与 temporal interval mining 的直接参考

你读完后要得到的结论：

- 如果要做 `Motion-APPO`，最该继承的是“关键局部信号怎么进入 reward / routing”
- 你要盯的是机制，不是视频 benchmark 本身

### 4.2 PRCO

阅读重心：

- Observer / Solver 分离怎样解决感知与推理的 credit assignment
- utility reward 怎样从下游成功率反推上游证据质量
- caption-first warmup 为什么关键

当前为什么上调：

- 旧清单里它更像 extension inspiration
- 现在 MoDebug 已经出现 evaluator router / evidence lane，所以 PRCO 对“证据层”和“决策层”的拆分更值得提前理解

你读完后要得到的结论：

- 如果以后把 reward model 升级成 evidence-producing observer，这篇是路线图
- 但当前它仍不该进入 MVP 主闭环

### 4.3 VideoZoomer

阅读重心：

- temporal zoom / active focusing 是怎么作为可学习 action 进入系统的
- static frame selection 为什么不够，为什么推理中需要动态补证据

当前为什么新增：

- 它直接补上了“关键时段 focus”这条逻辑线
- 对当前 attention filter / temporal routing 支线的参考价值，高于一般的泛泛 video-RL 论文

你读完后要得到的结论：

- 如果未来要把 interval miner 往 active temporal zoom 发展，这篇是直接母版之一
- 当前先借它的 temporal focus 逻辑，不借它的完整 agentic 主框架

### 4.4 Perception-R1

阅读重心：

- 什么样的感知任务适合 RL 式增强，什么样的不适合
- `perceptual perplexity` 这种“先判断值不值得做”的视角

当前为什么新增：

- 它能帮助你避免把所有细粒度感知增强都一股脑塞进主线
- 对 `R_dur`、局部 temporal supervision、interval judge 值不值得做，能提供一个“先看不确定性”的判断框架

你读完后要得到的结论：

- 当前哪些 reward / evaluator 细化可能值得做，哪些可能收益很低
- 为什么“细分更多 supervision”不自动等于“更值得做”

## 5. 背景 / fallback / 历史线：保留但降权

对应笔记：

- [[paperAnalysis/Motion_Generation/NeurIPS_2025/2025_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization|SoPo]]
- [[paperAnalysis/Motion_Generation/AAAI_2024/2024_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_with_Minimal_Feedback|HuTuDiffusion]]

### 5.1 SoPo

阅读重心：

- 离线 DPO、在线 DPO、半在线 DPO 各自的偏差
- 为什么偏好后训练容易学到“更像好样本”，但不一定学到“哪里错了”
- SoPo 对 MoDebug 的启发该停在背景比较，还是可做 fallback 路线

当前角色变化：

- 旧清单里它更接近“直接机制参考”
- 现在保留，但主要承担 **为什么不先押后训练** 与 **pilot 失败后的备选** 两个作用

你读完后要得到的结论：

- 为什么当前优先押 inference-time，而不是先走 preference optimization
- 如果 inference-time pilot 卡死，SoPo 是否是最自然的 fallback 之一

### 5.2 HuTuDiffusion

阅读重心：

- 不改主模型参数，单靠 sampling / prior 导航能提升到什么程度
- “轻量 plug-and-play 调整”在 motion 里有哪些历史先例

当前角色变化：

- 保留它不是为了直接复用方法细节
- 而是为了补一条历史线：Plan B 不是第一篇“无需重训主体模型也可改善生成”的 motion work

## 6. RL mechanics supplement：只在你真的要补 RL 机制时再读

对应笔记：

- [[paperAnalysis/Vision_Language_Reasoning/CVPR_2026/2026_AVATAR_Reinforcement_Learning_to_See_Hear_and_Reason_Over_Video|AVATAR]]
- [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_DIVA_GRPO_Enhancing_Multimodal_Reasoning_through_Difficulty_Adaptive_Variant_Advantage|DIVA-GRPO]]
- [[paperAnalysis/Vision_Language_Reasoning/NeurIPS_2025/2025_GVPO_Group_Variance_Policy_Optimization_for_Large_Language_Model_Post_Training|GVPO]]

### 6.1 AVATAR

它回答的问题：

- 为什么纯 on-policy GRPO 数据效率低
- 为什么 group 内奖励方差消失会让训练停掉
- 为什么 temporal weighting 会成为一个单独议题

对 MoDebug 的价值：

- 当前不是主方法参考
- 但如果以后进入 learned guidance / on-policy hard negatives / group rollout 训练，这篇会迅速变得重要

### 6.2 DIVA-GRPO

它回答的问题：

- 为什么极易 / 极难样本会让 advantage vanish
- 如何通过难度自适应变体增强保持组内奖励分布有方差

对 MoDebug 的价值：

- 当前更适合当 diagnostic 思路库
- 如果以后要做 hard negative / corruption curriculum / sample difficulty 分层，这篇很有用

### 6.3 GVPO

它回答的问题：

- 为什么 GRPO 一直被继续改
- 为什么 group-wise policy optimization 的权重设计会直接影响稳定性与最优性

对 MoDebug 的价值：

- 当前不是你必须掌握的主机制
- 但它能帮你把 `GRPO / DPO / SFT / reject sampling` 看成统一后训练视角的一组变体

## 7. 排除性阅读：知道哪些路不要滑过去

对应笔记：

- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Motion_R1_Enhancing_Motion_Generation_Decomposed_CoT_RL_Binding|Motion-R1]]
- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation|MoRL]]
- [[paperAnalysis/Motion_Generation/arXiv_2025/2025_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_for_Text_to_Motion_Generation|IRG-MotionLLM]]

### 7.1 Motion-R1

读它的目标：

- 不是学做法，而是确认 Plan B 不要变成 LLM-CoT-RL 路线

### 7.2 MoRL

读它的目标：

- 确认 Plan B 不要扩成统一 motion reasoning framework

### 7.3 IRG-MotionLLM

读它的目标：

- 确认 Plan B 不要滑向生成-评估-修正交错 pipeline

## 8. 建议的阅读产出

每读完一篇，建议固定只记录 4 行：

1. **它解决的最小问题是什么**
2. **它的 reward / critic / guidance 粒度是什么**
3. **它最能被 Plan B 继承的 1 个机制是什么**
4. **它最容易把 Plan B 带偏的 1 个方向是什么**

如果你希望把阅读结果直接服务于当前 active root notes，那么读完前 5 篇后，应该强制输出一版：

- `R_pres` 候选定义
- `R_ord` 候选定义
- `R_dur` 候选定义
- 哪些信号来自 event decomposition
- 哪些信号来自 step-aware noisy-state guidance
- 哪些信号来自 reward family split，而不是单一总分

如果你继续读到 `APPO / PRCO / VideoZoomer / Perception-R1`，则还要额外强制输出：

- 哪些信号适合做 `interval miner`
- 哪些信号适合做 `evaluator router`
- 哪些细粒度 supervision 值得进入当前 scope，哪些应该删掉
- 哪些 claim 如果做不到，就必须从主叙事里主动删掉

如果你真的进入 RL mechanics supplement，再补一份：

- on-policy / off-policy 是否已经成为真实瓶颈
- group variance / advantage vanishing 是否已经成为真实瓶颈
- 是否有必要把当前 inference-time 主线扩成 train-time policy optimization
