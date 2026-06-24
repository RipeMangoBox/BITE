---
created: 2026-04-28T20:41
updated: 2026-04-29T14:17
title: MoDebug RL 零基础读本：从 Plan B 到 Event-Level Reward Guidance
status: archived
tags:
  - MoDebug
  - RL
  - reading-guide
  - event-level-reward
  - reward-guidance
  - paper-oriented
related_notes:
  - "[[2026-04-26_modebug-plan-b-core-reading-list]]"
  - "[[2026-04-27_modebug-planb-ordering-omission-manifest]]"
source_papers:
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]"
  - "[[paperAnalysis/Motion_Generation/ICCV_2023/2023_TMR_Text_to_Motion_Retrieval_Using_Contrastive_3D_Human_Motion_Synthesis|TMR]]"
  - "[[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward|AToM]]"
  - "[[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment|ReAlign]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2025/2025_MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions|MotionCritic]]"
  - "[[paperAnalysis/Motion_Generation/NeurIPS_2025/2025_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization|SoPo]]"
  - "[[paperAnalysis/Motion_Generation/ICLR_2026/2026_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Generation|EasyTune]]"
  - "[[paperAnalysis/Motion_Generation/AAAI_2024/2024_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_with_Minimal_Feedback|HuTuDiffusion]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_Perception_Aware_Policy_Optimization_for_Multimodal_Reasoning|PAPO]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/CVPR_2026/2026_APPO_Attention_guided_Perception_Policy_Optimization_for_Video_Reasoning|APPO]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Seeing_with_You_Perception_Reasoning_Coevolution_for_Multimodal_Reasoning|PRCO]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/NeurIPS_2025/2025_Perception_R1_Pioneering_Perception_Policy_with_Reinforcement_Learning|Perception-R1]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/NeurIPS_2025/2025_GVPO_Group_Variance_Policy_Optimization_for_Large_Language_Model_Post_Training|GVPO]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/CVPR_2026/2026_AVATAR_Reinforcement_Learning_to_See_Hear_and_Reason_Over_Video|AVATAR]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_DIVA_GRPO_Enhancing_Multimodal_Reasoning_through_Difficulty_Adaptive_Variant_Advantage|DIVA-GRPO]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_Controllable_Exploration_in_Hybrid_Policy_RLVR_for_Multi_Modal_Reasoning|CalibRL]]"
  - "[[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_VideoZoomer_Reinforcement_Learned_Temporal_Focusing_for_Long_Video_Reasoning|VideoZoomer]]"
---

# MoDebug RL 零基础读本：从 Plan B 到 Event-Level Reward Guidance

> [!abstract] **这份笔记的定位**
> 这不是系统 RL 教程，而是为 `MoDebug Plan B` 定制的零基础读本。目标不是让你会推导 PPO / DPO / GRPO，而是让你能读懂相关论文、分清方法差异，并知道 `MoDebug` 为什么会长成 `Event-T2M + HumanML3D-E + TMR + R_pres / R_ord / R_dur + inference-time guidance` 这条线。

## 0. 先记住 7 句话

1. MoDebug 不是 classic RL control 问题；它更像“用 reward 去校正一个生成过程”。
2. 你当前最需要懂的不是 Bellman equation，而是 `reward`、`scorer/critic`、`preference pair`、`step-aware`、`inference-time guidance`、`credit assignment`。
3. `policy` 在这里可以粗暴理解成“当前生成器/采样过程”；在 diffusion 里更接近 denoising trajectory。
4. `reward model` / `critic` 在这些论文里大多就是“打分器”，不一定意味着完整 actor-critic 训练。
5. AToM 把全局对齐拆成事件级维度；ReAlign 把 reward 放进每个 denoising step；MotionCritic 提醒你“感知质量”和“事件对齐”不是一回事。
6. SoPo / EasyTune 说明“后训练也能做”，但 MoDebug 当前主线优先选 inference-time，因为更 plug-and-play、更贴近现有资产。
7. PAPO / APPO / PRCO 的价值不在于直接照搬 GRPO，而在于教你“单一 reward 会混淆感知与推理，需要拆 reward family”。

## 1. 概念的快速掌握

### 1.1 先把 MoDebug 的 RL 问题写成一句话

MoDebug Plan B 的核心不是“训练一个会控制环境的 agent”，而是：

> 给定多事件文本与当前 denoising 中间态，构造对 `event presence / event ordering / event duration` 敏感的 reward，并在采样过程中用这个 reward 引导 motion 向更正确的事件结构演化。

### 1.2 增量视角：这条技术线是怎么长出来的

```text
经典 RL：定义 reward，更新 policy，让高 reward 行为更常出现
→ 偏好学习：没有精确 reward 也行，用 better / worse pairs 学
→ 生成模型对齐：把“高 reward 输出更常出现”搬到生成模型后训练
→ diffusion 对齐：不只看最终样本，还要考虑整条 denoising trajectory
→ step-aware reward：中间 noisy state 也得能打分，不然梯度不稳
→ event-level reward：全局分数太粗，必须拆成 presence / ordering / duration
→ perception-aware reward：语义事件对齐和整体感知质量要分开
→ MoDebug：inference-time event-level reward guidance
```

### 1.3 `perception` 在本文里的具体含义

这份笔记里的 `perception` 不是泛指“视觉感知”这四个字，而是更具体地指：

> **模型或 scorer 是否真的捕捉到了与任务相关的局部证据，而不是只靠一个全局分数或最终结果做粗判断。**

放到 `MoDebug` 里，`perception` 默认分成两层：

1. **event evidence perception**
   - 是否真的“看见了”某个 event、顺序关系、关键时间段
2. **perceptual quality**
   - motion 整体是否自然、连贯、没有明显崩坏

后文如果不特别说明：

- `perception` 更偏向“证据是否被捕捉到”
- `quality` 更偏向“动作看起来是否自然”
- `event following` 更偏向“文本事件是否被正确执行”

核心名词表：

| 名词 | 在本文里的意思 | 在 MoDebug 里的落点 | 不是指什么 |
| --- | --- | --- | --- |
| `perception` | 对任务相关局部证据的捕捉能力 | event 是否出现、顺序是否对、关键区间在哪 | 不是泛泛“做视觉” |
| `perception-aware` | 在 reward / eval 里显式把“证据是否被看见”单独拿出来 | 不只看最终分数，还看是否抓到关键 event 证据 | 不是一定要上 GRPO |
| `perceptual quality` | 人看上去觉得 motion 是否自然、顺滑、合理 | `quality lane`、`R_qual`、MotionCritic 这一路 | 不是 `event following` |
| `event following` | motion 是否忠实执行文本里的事件结构 | `R_pres / R_ord / R_dur` | 不是整体自然度 |
| `local evidence` | 支撑判断的局部片段或局部信号 | motion window、ordered event pair、attention peak | 不是全局 embedding 分数 |
| `temporal focus` | 对关键时间段赋予更多注意或权重 | ordering-sensitive interval、windowed local score | 不是整段 motion 均匀处理 |
| `quality lane` | 专门约束 motion 质量的一路信号 | 防止只追文本对齐把动作拉崩 | 不是主 event reward 本身 |
| `counterfactual` | 人工构造“改坏一点”的对照样本来测敏感性 | `drop / swap / replace / stretch` corruption | 不是正式生成结果 |
| `critic` | 学出来的打分器 | MotionCritic 式 quality scorer | 不是生成器 |
| `reward family` | 不把所有目标压成一个分数，而是拆成多路 reward | `R_pres / R_ord / R_dur / R_qual` | 不是单一 scalar reward |
| `temporal-aware eval` | 专门测时序局部敏感性的评测层 | presence delta、order delta、windowed evidence | 不是只算 TMR |

### 1.4 只学这些术语就够了

| 概念                        | 你现在可以这样理解                  | 在 MoDebug 里的对应物                                  | 先掌握到什么程度就够                            |
| ------------------------- | -------------------------- | ------------------------------------------------ | ------------------------------------- |
| `policy / generator`      | 产生输出的当前策略                  | `Event-T2M` 的生成与采样过程                             | 知道它是被 reward 影响的对象                    |
| `trajectory`              | 一次生成过程中的状态序列               | `x_T -> ... -> x_0` 的 denoising 轨迹               | 知道 reward 不一定只作用在最终 `x_0`             |
| `reward`                  | 你希望模型偏好的方向                 | `R_pres / R_ord / R_dur`                         | 知道 reward 可以拆分                        |
| `reward model / scorer`   | 给当前样本打分的函数                 | `TMR` 类 scorer、ReAlign reward model、MotionCritic | 知道它不等于生成器                             |
| `critic`                  | 学出来的标量打分器                  | MotionCritic                                     | 知道它常用来做代理监督，不一定是完整 actor-critic       |
| `preference pair`         | “A 比 B 好” 这种成对监督           | AToM / SoPo 的偏好对                                 | 知道它能替代精确标量 reward                     |
| `step-aware`              | 打分时显式考虑当前 step/noise level | ReAlign / EasyTune                               | 知道 noisy motion 和 clean motion 不是一个问题 |
| `inference-time guidance` | 测试时改采样，不改模型参数              | ReAlign 风格 guidance                              | 知道这和后训练不同                             |
| `credit assignment`       | 最终错了，错该归到哪里                | event decomposition、PAPO / APPO / PRCO           | 知道为什么单一全局 reward 不够                   |
| `on-policy`               | 用当前模型自己采出来的样本学习            | SoPo 的在线非偏好样本、MoDebug seed pool                  | 知道它更贴近当前失败模式                          |

### 1.5 哪些 RL base 技术是前身，哪些可以先跳过

**必须知道的前身层：**

1. **MDP / policy / reward / trajectory**
   - 只需语义理解，不必推导。
2. **policy gradient / PPO / actor-critic**
   - 只需知道“参数按高 reward 方向更新”这件事。
   - Motion 领域很多早期 RL 工作都从这条线来，例如物理或节拍对齐。
3. **preference learning / Bradley-Terry / DPO**
   - 只需知道“没精确 reward 时，可以用偏好对学”。
4. **KL-constrained post-training**
   - 只需知道“优化 reward 的同时要别偏离原模型太远”。

**可以先跳过的层：**

1. Bellman equation、TD learning、Q-learning、DQN 细节
2. importance sampling、收敛性证明、variance reduction 推导
3. 连续控制 benchmark
4. 大部分 GRPO / GVPO 的理论证明细节

> [!tip] 为什么可以跳过
> MoDebug 当前主线更接近“生成模型对齐 + diffusion guidance”，不是典型的 value-based RL，也不是重度 online exploration。

### 1.6 技术家族 compare table

| 技术家族                           | 代表                   | 奖励作用对象                 | 奖励粒度      | 作用时机      | 是否改主模型 | 对 MoDebug 的意义                                         |
| ------------------------------ | -------------------- | ---------------------- | --------- | --------- | ------ | ----------------------------------------------------- |
| 偏好后训练                          | AToM, SoPo           | 最终生成样本                 | 事件级 / 全局  | 训练期       | 是      | 告诉你 reward 可以来自偏好对，而不是手工公式                            |
| critic-guided 对齐               | MotionCritic         | 最终样本或中间预测              | 全局感知质量    | 训练期       | 是      | 告诉你 1.3 里的 `perceptual quality` 需要单独建模                 |
| few-shot 人类反馈导航                | HuTuDiffusion        | latent prior           | 全局        | 推理前/采样初始  | 否      | 提醒你“不改主模型也能调生成”                                       |
| inference-time reward guidance | ReAlign              | noisy denoising states | 全局        | 推理期       | 否      | MoDebug 当前主线最直接的机械母体                                  |
| step-aware 后训练                 | EasyTune             | 各 denoising step       | 全局        | 训练期       | 是      | 说明 step-aware 不是小 trick，而是 reward 与 denoising 对齐方式的改变 |
| perception-aware RL            | PAPO, APPO, PRCO     | 感知证据 / 推理过程            | 分层 reward | 训练期       | 是      | 告诉你 1.3 里的 `local evidence`、`quality`、`event following` 不该混成一个分数 |
| CoT / agentic motion RL        | Motion-R1, MoRL, IRG | 规划、评估、修正链              | 全局        | 训练期 + 推理期 | 是      | 主要用于“排除性理解”：MoDebug 不该滑到这条线                           |

### 1.7 关键论文 compare table

本节涉及的本地论文入口：

- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]
- [[paperAnalysis/Motion_Generation/ICCV_2023/2023_TMR_Text_to_Motion_Retrieval_Using_Contrastive_3D_Human_Motion_Synthesis|TMR]]
- [[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward|AToM]]
- [[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment|ReAlign]]
- [[paperAnalysis/Motion_Generation/ICLR_2025/2025_MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions|MotionCritic]]
- [[paperAnalysis/Motion_Generation/NeurIPS_2025/2025_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization|SoPo]]
- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Generation|EasyTune]]
- [[paperAnalysis/Motion_Generation/AAAI_2024/2024_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_with_Minimal_Feedback|HuTuDiffusion]]
- [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_Perception_Aware_Policy_Optimization_for_Multimodal_Reasoning|PAPO]]
- [[paperAnalysis/Vision_Language_Reasoning/CVPR_2026/2026_APPO_Attention_guided_Perception_Policy_Optimization_for_Video_Reasoning|APPO]]
- [[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Seeing_with_You_Perception_Reasoning_Coevolution_for_Multimodal_Reasoning|PRCO]]
- [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Motion_R1_Enhancing_Motion_Generation_Decomposed_CoT_RL_Binding|Motion-R1]]
- [[paperAnalysis/Motion_Generation/arXiv_2026/2026_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation|MoRL]]
- [[paperAnalysis/Motion_Generation/arXiv_2025/2025_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_for_Text_to_Motion_Generation|IRG-MotionLLM]]

| 论文 | 它解决的最小问题 | 奖励/信号粒度 | 作用时机 | MoDebug 该拿什么 | MoDebug 该防什么 |
| --- | --- | --- | --- | --- | --- |
| Event-T2M | 多事件文本如何稳定注入生成 | 事件级条件，不是 RL reward | 生成全过程 | “事件是最小语义单元” | 别把事件接口误当 reward 本身 |
| TMR | 文本-动作如何在同一空间里打相似度分数 | 全局语义分数 | 评测/打分 | scorer 基础设施 | 别把它当强时序金标准 |
| AToM | 全局对齐太粗，如何做事件级偏好对齐 | 事件级：完整性/时序/频率 | 后训练 | `R_pres / R_ord / R_dur` 的原型 | 别停在“DPO 微调就够了” |
| ReAlign | 如何在 noisy state 上做 reward guidance | 全局 step-aware reward | 推理期 | gradient injection 机制 | 事件级 reward 稳定性难题 |
| MotionCritic | 人类感知质量如何建模 | 全局感知质量 | 后训练/评测 | 把 `perceptual quality` 从 `event following` 中拆出来 | 别用单标量替代 ordering/duration |
| SoPo | offline DPO 和 online DPO 怎么折中 | 全局偏好 | 后训练 | fallback 路线、on-policy hard negatives 思路 | 训练成本与奖励偏差 |
| EasyTune | 长 denoising 轨迹如何高效做 reward 后训练 | 全局 step-aware reward | 训练期 | step-aware 的训练版理解 | 别把它和 inference-time 混为一谈 |
| HuTuDiffusion | 少量反馈如何不改主模型提升生成 | 全局 prior 导航 | 采样前 | plug-and-play 历史感 | 它不是事件级，也不是 step-aware |
| PAPO | outcome-only reward 为什么会压坏感知 | 分离感知/推理 reward | 训练期 | reward family 拆分思想 | 直接照搬 GRPO 框架 |
| APPO | 关键局部证据怎么自动挖 | 关键帧/关键区间感知 reward | 训练期 | `temporal focus` / interval miner 灵感 | 把 video attention 直接套到 motion |
| PRCO | 感知和推理信用分配如何解耦 | Observer / Solver 双角色 reward | 训练期 | utility reward 思路 | 过早做成双角色主框架 |
| Motion-R1 | 先规划再生成的 motion RL | 全局 reward | 训练期 | 知道近邻长什么样 | 叙事滑向 CoT planning |
| MoRL | 统一理解/生成 + 测试时反思 | 双头 reward | 训练期 + 推理期 | 知道更大统一框架边界 | scope 爆炸 |
| IRG-MotionLLM | 生成-评估-修正交错循环 | 全局 reward | 训练期 + 推理期 | 知道“交错修正”范式 | 把 MoDebug 改成完整 agent pipeline |

### 1.8 增量视角下，MoDebug 为什么最终收口成现在这样

1. [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]] 证明了 **event 是合理的最小语义单元**，并给了 `HumanML3D-E` 这种可直接消费的结构。
2. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward|AToM]] 证明了 **全局 reward 太粗，需要拆成事件级维度**。
3. [[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment|ReAlign]] 证明了 **reward 不一定要靠后训练，也可以在每个 denoising step 做 inference-time guidance**。
4. [[paperAnalysis/Motion_Generation/ICLR_2025/2025_MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions|MotionCritic]] 说明 1.3 里的 **`perceptual quality` 与 `event following` 不是同一维度**。
5. [[paperAnalysis/Motion_Generation/NeurIPS_2025/2025_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization|SoPo]] 与 [[paperAnalysis/Motion_Generation/ICLR_2026/2026_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Generation|EasyTune]] 说明 **后训练是存在的 fallback**，但 MoDebug 当前为了 plug-and-play 和资产复用，先不走这条主线。
6. [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_Perception_Aware_Policy_Optimization_for_Multimodal_Reasoning|PAPO]] / [[paperAnalysis/Vision_Language_Reasoning/CVPR_2026/2026_APPO_Attention_guided_Perception_Policy_Optimization_for_Video_Reasoning|APPO]] / [[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Seeing_with_You_Perception_Reasoning_Coevolution_for_Multimodal_Reasoning|PRCO]] 进一步提醒：1.3 里的 **`local evidence`、`temporal focus`、`perceptual quality`** 应该分开处理，而不是混成一个 reward。
7. 所以当前 Plan B 的最小闭环是：

```text
Event-T2M backbone
+ HumanML3D-E ordered events
+ TMR-style scorer as current practical starting point
+ R_pres / R_ord / R_dur reward family
+ inference-time event-level reward guidance
```

## 2. 更深入掌握所需的学习资料

### 2.1 论文导向的最小学习路径

**Phase A：先把词认全，不求推导**

1. `Sutton & Barto, Reinforcement Learning: An Introduction`
   - 只看：Chapter 1, 3, 13
   - 目标：知道 `agent / reward / policy / trajectory / policy gradient` 是什么意思
   - 不用看：大量 Bellman / TD / control 细节
2. `Direct Preference Optimization: Your Language Model is Secretly a Reward Model`
   - 目标：知道为什么“偏好对”可以代替显式 reward model
   - 读到能说清 DPO 与 SFT 的区别就够
3. 一份 PPO / actor-critic 短教程
   - 目标：只搞懂“actor 负责生成，critic 负责打分/估优势”这层直觉
   - 不必推公式

**Phase B：先补 diffusion 背景，否则 ReAlign / EasyTune 看不动**

1. [[paperAnalysis/Motion_Generation/ICLR_2023/2023_MDM_Human_Motion_Diffusion_Model|MDM]]
2. [[paperAnalysis/Motion_Generation/CVPR_2023/2023_MLD_Executing_your_Commands_via_Motion_Diffusion_in_Latent_Space|MLD]]

读到的最低要求：

- 知道什么是 denoising step
- 知道 `x_t` 是 noisy motion state
- 知道 inference-time guidance 是往采样更新里加额外方向

### 2.2 MoDebug 必读层

1. [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]
   - 为什么读：它定义了 `event` 这个接口，给了 `HumanML3D-E`
   - 读到什么程度：读懂“一个文本 -> 多个事件 -> 多个条件 -> 一个 motion”
   - 读完应能回答：为什么 event 是 `MoDebug` 的最小单位
2. [[paperAnalysis/Motion_Generation/ICCV_2023/2023_TMR_Text_to_Motion_Retrieval_Using_Contrastive_3D_Human_Motion_Synthesis|TMR]]
   - 为什么读：这是当前 `R_pres`/semantic scorer 的现实起点
   - 读到什么程度：知道它是共享 embedding scorer，不是生成器
   - 读完应能回答：为什么它能给“语义 sanity score”，但不是 ordering 金标准
3. [[paperAnalysis/Motion_Generation/CVPR_2025/2025_AToM_Aligning_Text_to_Motion_Model_Event_Level_GPT4Vision_Reward|AToM]]
   - 为什么读：它给出事件级 reward decomposition 原型
   - 读到什么程度：抓住 `完整性 / 时序 / 频率`
   - 读完应能回答：`R_pres / R_ord / R_dur` 分别最像它的哪一部分
4. [[paperAnalysis/Motion_Generation/AAAI_2026/2026_ReAlign_Bilingual_Text_to_Motion_Generation_via_Step_Aware_Reward_Guided_Alignment|ReAlign]]
   - 为什么读：它给出 step-aware inference-time guidance 的最直接机械模板
   - 读到什么程度：抓住 reward model 为何必须处理 noisy motion，以及 `∇R(x_t, c)` 怎么进采样更新
   - 读完应能回答：MoDebug 的 guidance 最像它的哪一步
5. [[paperAnalysis/Motion_Generation/ICLR_2025/2025_MotionCritic_Aligning_Human_Motion_Generation_with_Human_Perceptions|MotionCritic]]
   - 为什么读：它让你从一开始就避免“把语义对齐和自然度混成一个标量”
   - 读到什么程度：抓住 critic 是学 human perception 的，不是 event alignment 的充分替代
   - 读完应能回答：为什么 `R_pres / R_ord / R_dur` 之外还可能需要 perceptual sidecar

### 2.3 第二层：理解 fallback 与边界

1. [[paperAnalysis/Motion_Generation/NeurIPS_2025/2025_SoPo_Text_to_Motion_Generation_Using_Semi_Online_Preference_Optimization|SoPo]]
   - 看点：offline DPO、online DPO、semi-online 的区别
   - 作用：帮你理解为什么 Plan B 现在不优先走后训练
2. [[paperAnalysis/Motion_Generation/ICLR_2026/2026_EasyTune_Efficient_Step_Aware_Fine_Tuning_for_Diffusion_Based_Motion_Generation|EasyTune]]
   - 看点：step-aware 在训练期如何缓解长轨迹梯度稀疏
   - 作用：帮你理解“step-aware 不是工程偶然”
3. [[paperAnalysis/Motion_Generation/AAAI_2024/2024_HuTuDiffusion_Human_Tuned_Navigation_of_Latent_Motion_Diffusion_Models_with_Minimal_Feedback|HuTuDiffusion]]
   - 看点：不改主模型，只改 prior / sampling 也能带来收益
   - 作用：帮你建立 plug-and-play 路线的历史感

### 2.4 第三层：迁移灵感层

1. [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_Perception_Aware_Policy_Optimization_for_Multimodal_Reasoning|PAPO]]
   - 看点：单一 outcome reward 会压坏感知
   - 对 MoDebug：支持把单一 `R_k` 拆成 reward family
2. [[paperAnalysis/Vision_Language_Reasoning/CVPR_2026/2026_APPO_Attention_guided_Perception_Policy_Optimization_for_Video_Reasoning|APPO]]
   - 看点：如何自动找关键局部证据
   - 对 MoDebug：未来 `interval miner` 的灵感来源
3. [[paperAnalysis/Vision_Language_Reasoning/arXiv_2026/2026_Seeing_with_You_Perception_Reasoning_Coevolution_for_Multimodal_Reasoning|PRCO]]
   - 看点：Observer / Solver 分离与 utility reward
   - 对 MoDebug：future sidecar，不是 MVP 依赖

### 2.5 排除性阅读层

1. [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Motion_R1_Enhancing_Motion_Generation_Decomposed_CoT_RL_Binding|Motion-R1]]
2. [[paperAnalysis/Motion_Generation/arXiv_2026/2026_MoRL_Reinforced_Reasoning_for_Unified_Motion_Understanding_and_Generation|MoRL]]
3. [[paperAnalysis/Motion_Generation/arXiv_2025/2025_IRG_MotionLLM_Interleaving_Motion_Generation_Assessment_and_Refinement_for_Text_to_Motion_Generation|IRG-MotionLLM]]

这三篇的读法都一样：

- 只看摘要、方法图、奖励设计、推理流程
- 目的不是学实现
- 目的是确认 `MoDebug` 不该滑向 `CoT planning`、`统一理解/生成框架`、`生成后交错修正 pipeline`

### 2.6 每篇论文的最小读法模板

每读完一篇，强制只写下面 5 行：

1. 它解决的最小问题是什么
2. 它的 reward / critic / scorer 粒度是什么
3. 它在训练期还是推理期起作用
4. 它能被 MoDebug 继承的 1 个机制是什么
5. 它最容易把 MoDebug 带偏的 1 个方向是什么

> [!note] 这是最适合你当前阶段的读法
> 你是“论文导向但不追求全部细节和推导”，所以最重要的是建立**方法差异的判别力**，不是背公式。

### 2.7 2025/2026 顶会扩展搜索结果（联网补充）

> [!note] 检索说明
> 本节在本地 `paperAnalysis` 之外，额外联网核对了 2025/2026 的顶会相关论文。当前最稳定的公开入口主要是 `OpenReview`、`CVPR OpenAccess / project page`、`NeurIPS schedule / poster / arXiv`、`AAAI abstract / arXiv`。截至 `2026-04-28`，少数 `CVPR 2026` 工作的主公开入口仍以 preprint / project 为主，本文沿本地知识库的 venue 标注整理。

本节新增关注的本地论文入口：

- [[paperAnalysis/Vision_Language_Reasoning/NeurIPS_2025/2025_Perception_R1_Pioneering_Perception_Policy_with_Reinforcement_Learning|Perception-R1]]
- [[paperAnalysis/Vision_Language_Reasoning/NeurIPS_2025/2025_GVPO_Group_Variance_Policy_Optimization_for_Large_Language_Model_Post_Training|GVPO]]
- [[paperAnalysis/Vision_Language_Reasoning/CVPR_2026/2026_AVATAR_Reinforcement_Learning_to_See_Hear_and_Reason_Over_Video|AVATAR]]
- [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_DIVA_GRPO_Enhancing_Multimodal_Reasoning_through_Difficulty_Adaptive_Variant_Advantage|DIVA-GRPO]]
- [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_Controllable_Exploration_in_Hybrid_Policy_RLVR_for_Multi_Modal_Reasoning|CalibRL]]
- [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_VideoZoomer_Reinforcement_Learned_Temporal_Focusing_for_Long_Video_Reasoning|VideoZoomer]]

#### A. 与 MoDebug 最直接相关的 motion / alignment 线

| 论文 | Venue | 核心 RL/对齐思想 | 对 MoDebug 的直接价值 | 建议优先级 |
| --- | --- | --- | --- | --- |
| AToM | CVPR 2025 | 事件级偏好分解 + DPO/SLiC | `R_pres / R_ord / R_dur` 的最直接前身 | 必读 |
| MotionCritic | ICLR 2025 | 人类感知 critic | 建立“quality != text following”的分层意识 | 必读 |
| SoPo | NeurIPS 2025 | semi-online preference optimization | 提供后训练 fallback 与 on-policy negatives 思路 | 次必读 |
| Event-T2M | ICLR 2026 | event-level conditioning | 提供事件接口与 `HumanML3D-E` 主数据形态 | 必读 |
| ReAlign | AAAI 2026 | step-aware inference-time reward guidance | 提供推理期 guidance 机械模板 | 必读 |
| EasyTune | ICLR 2026 | step-aware reward post-training | 解释 step-aware 的训练版意义 | 次必读 |
| Motion-R1 | ICLR 2026 | CoT + GRPO for motion | 帮你界定 MoDebug 不该滑向什么 | 排除性阅读 |

#### B. 对时序感知 / 局部证据 / reward family 最有启发的顶会线

| 论文 | Venue | 核心思想 | 对 MoDebug 的启发 | 建议优先级 |
| --- | --- | --- | --- | --- |
| Perception-R1 | NeurIPS 2025 | perceptual perplexity 决定 RL 是否有效 | 可迁移成“事件困惑度 / temporal uncertainty”诊断 | 高 |
| PAPO | ICLR 2026 | 分离 perception reward 与 reasoning reward | 支持把 `text following` 与 `high quality` 分 lane | 高 |
| APPO | CVPR 2026 | attention-guided 关键局部感知优化 | 适合作为 future interval miner 母版 | 高 |
| VideoZoomer | ICLR 2026 | RL 学 temporal zoom / 动态时段聚焦 | 适合迁移成时序证据定位 / local eval 设计 | 高 |
| AVATAR | CVPR 2026 | temporal advantage shaping + off-policy replay | 适合迁移成“关键时间段更重”的 eval / guidance 调度 | 中高 |

#### C. 对 RL 稳定性 / 组内方差 / 探索策略有启发的顶会线

| 论文 | Venue | 核心思想 | 对 MoDebug 的意义 | 建议优先级 |
| --- | --- | --- | --- | --- |
| GVPO | NeurIPS 2025 | 比 GRPO 更稳的 group-wise optimization 视角 | 帮你统一理解 DPO / GRPO / group reward 关系 | 中 |
| DIVA-GRPO | ICLR 2026 | 通过难度变体制造有效方差 | 可迁移成 event corruption / hard-negative 设计 | 高 |
| CalibRL | ICLR 2026 | 稀有度加权探索 + 非对称校准 | 可迁移成“稀有但关键事件错误更高权重” | 中高 |

#### D. 这批新增论文里，哪些最值得真加进你的阅读主线

如果只补 6 篇，建议按这个顺序：

1. [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_Perception_Aware_Policy_Optimization_for_Multimodal_Reasoning|PAPO]]
2. [[paperAnalysis/Vision_Language_Reasoning/NeurIPS_2025/2025_Perception_R1_Pioneering_Perception_Policy_with_Reinforcement_Learning|Perception-R1]]
3. [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_VideoZoomer_Reinforcement_Learned_Temporal_Focusing_for_Long_Video_Reasoning|VideoZoomer]]
4. [[paperAnalysis/Vision_Language_Reasoning/CVPR_2026/2026_AVATAR_Reinforcement_Learning_to_See_Hear_and_Reason_Over_Video|AVATAR]]
5. [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_DIVA_GRPO_Enhancing_Multimodal_Reasoning_through_Difficulty_Adaptive_Variant_Advantage|DIVA-GRPO]]
6. [[paperAnalysis/Vision_Language_Reasoning/ICLR_2026/2026_Controllable_Exploration_in_Hybrid_Policy_RLVR_for_Multi_Modal_Reasoning|CalibRL]]

原因很简单：

- `PAPO` 解决 reward family 分层
- `Perception-R1` 解决“什么时候 RL/额外感知 supervision 值得做”
- `VideoZoomer` / `AVATAR` 解决“时序关键区间如何被更强地看见 / 加权”
- `DIVA-GRPO` / `CalibRL` 解决“hard cases、稀有 cases、组内方差和探索权重怎么设计”

## 3. 为了更好掌握 RL 核心，你还需要的其他信息和资料

### 3.1 三个非 RL 但必须懂的支撑件

1. [[paperAnalysis/Motion_Generation/ICLR_2026/2026_Event_T2M_Event_Level_Conditioning_Complex_Text_to_Motion_Synthesis|Event-T2M]]
   - 它决定 `MoDebug` 的条件接口长什么样
   - 没它，你不知道 event reward 到底挂在哪里
2. [[paperAnalysis/Motion_Generation/ICCV_2023/2023_TMR_Text_to_Motion_Retrieval_Using_Contrastive_3D_Human_Motion_Synthesis|TMR]]
   - 它决定当前 scorer 从哪里来
   - 没它，你不知道 `R_pres` 的现实起点是什么
3. `HumanML3D-E`
   - 它决定当前 ordered events 从哪里来
   - 没它，`R_ord` 只能停留在概念上

### 3.2 一个很重要的历史判断

如果把 motion 里的 RL 路线粗分一下，前身大概有三类：

1. **控制/物理 RL**
   - 代表直觉：PPO、actor-critic、物理奖励、模仿策略
   - 典型目的是“动作更物理合理”
   - 和 MoDebug 的差别：这不是当前主问题，当前主问题是多事件语义对齐
2. **偏好/对齐 RL**
   - 代表直觉：DPO、critic、reward model、KL-regularized post-training
   - 典型目的是“输出更符合偏好/语义”
   - 这是 MoDebug 更直接的前身
3. **推理/agentic RL**
   - 代表直觉：GRPO、CoT、生成-评估-修正
   - 典型目的是“让模型会规划、会反思”
   - 对 MoDebug 目前主要是排除项，而不是主继承项

### 3.3 如果你还想补一点“RL 核心”但不想掉进大坑

**推荐顺序：**

1. 先补 `reward / policy / preference / KL regularization`
2. 再补 `diffusion denoising step` 和 `guidance`
3. 最后才看 `GRPO / GVPO / actor-critic` 这些方法名之间的关系

**推荐补充材料：**

1. [[paperAnalysis/Vision_Language_Reasoning/NeurIPS_2025/2025_GVPO_Group_Variance_Policy_Optimization_for_Large_Language_Model_Post_Training|GVPO]]
   - 用于建立 SFT / Reject Sampling / DPO / GRPO 的统一视角
   - 不是必读，但很适合“看清关系图”
2. [[paperAnalysis/Motion_Generation/ICCV_2023/2023_PhysDiff_Physics_Guided_Human_Motion_Diffusion_Model|PhysDiff]]
   - 如果你想看一个更早的 motion-domain RL 祖先样例
   - 价值在于理解“RL 曾经怎样进入 motion”
3. [[paperAnalysis/Motion_Generation/TPAMI_2023/2023_Bailando_3D_Dance_Generation_by_Actor_Critic_GPT_with_Choreographic_Memory|Bailando]]
   - 如果你想看 actor-critic 在 motion 中的另一种老路线
   - 价值在于理解“早期 RL 更常服务于节拍/控制，不是事件语义 alignment”

### 3.4 当前阶段最容易混淆的 8 个点

1. `TMR` 是 scorer，不是 reward theorem，也不是时序金标准
2. `critic` 不等于必须有 actor-critic 训练闭环
3. `event-level conditioning` 不等于 `event-level reward`
4. `step-aware` 不等于“每步都更新参数”；ReAlign 是推理期，EasyTune 是训练期
5. `preference optimization` 不等于“真正 online RL”；DPO/SoPo 常常是偏好后训练
6. `perception-aware` 不等于一定要上 GRPO；按 1.3，它首先是把 `local evidence`、`temporal focus`、`perceptual quality` 从单一路 reward 中拆出来
7. `R_pres / R_ord / R_dur` 是 reward family，不是三篇独立方法
8. 当前 `R_dur` 还是接口，不该在入门阶段抢占主注意力

### 3.5 你现在真正需要会回答的 5 个问题

1. 为什么全局 reward 不足以解决 `ordering / omission`
2. 为什么 `noisy motion` 上的 reward 比 final motion reward 更难
3. 为什么 `inference-time guidance` 和 `post-training` 是两条不同路线
4. 为什么 “感知自然度” 不能替代 “事件顺序/存在性”
5. 为什么 `MoDebug` 当前主线比 `Motion-R1 / MoRL / IRG` 更窄但也更稳

## 4. 这些新增 RL 技术如何服务 MoDebug 的 contribution 构建

### 4.1 对 `MoDebug` 当前 challenge 的直接判断

当前 Plan B 最卡的不是“有没有更多 RL 名词”，而是下面 4 个真实缺口：

1. **时序感知 eval 还不够强**
   - `TMR` 更像 global semantic sanity check
   - `MotionPatches temporal probe` 又不够强，难以支撑 ordering 级 claim
2. **`R_ord` 的稳定性证据仍偏弱**
   - 当前主要靠 corruption / proxy gate
   - 但还缺一个更系统的 temporal sensitivity 叙事
3. **单纯追 `event following` 可能伤 `perceptual quality`**
   - 如果没有 1.3 里的 `quality lane`，reviewer 很容易质疑你是在拿自然度换文本对齐
4. **reviewer 容易说你只是 AToM + ReAlign**
   - 如果没有新的 eval / diagnostic / reward decomposition 叙事，这个风险很高

### 4.2 如何服务 `MoDebug` 的时序感知 eval

最值得补的不是再找一个更大的全局 scorer，而是构建一个围绕 1.3 中 `temporal focus` 和 `local evidence` 的 **temporal-aware event sensitivity eval stack**。

建议写成三层：

1. **Global semantic sanity**
   - 继续保留 `TMR`
   - 角色：确认 motion 没彻底跑偏
2. **Counterfactual event sensitivity**
   - 用 `drop / swap / replace / stretch` 四类 corruption
   - 分别测：
     - `Presence Sensitivity Delta`
     - `Order Swap Delta`
     - `Distractor Rejection Delta`
     - `Duration Stretch Delta`
3. **Temporal focus evidence**
   - 不要求一开始就做 full localizer
   - 但至少做：
     - windowed local score
     - attention peak / interval overlap
     - on-policy hard-negative bank 的局部对比

这套 eval stack 的论文来源可以这样借：

- `Perception-R1`：告诉你先做“任务是否值得更细 supervision”的困惑度诊断
- `VideoZoomer`：告诉你时间段本身可以是需要主动聚焦的对象
- `AVATAR`：告诉你关键时间位置不该被均匀看待
- `APPO`：告诉你关键局部证据可以由模型自身信号辅助挖出
- `DIVA-GRPO`：告诉你要主动制造有信息量的 counterfactual variant，而不是被动等失败样本出现

也就是说，你未来最有 paper 味道的 eval 贡献，不是“我们也算了 TMR / MP temporal”，而是：

> **我们系统性测量 event-level reward / scorer 对 presence、ordering、duration corruption 的敏感性，并把 temporal focus 证据纳入评测闭环。**

### 4.3 如何服务 event-level `high-quality + text following` 增强

按 1.3 的定义，这里最值得补的是把当前主线从“单路 event reward”升级成 **`event following` / `perceptual quality` 双路 guidance**：

```text
Lane A: event following
  R_pres + R_ord + optional R_dur

Lane B: motion quality / perceptual plausibility
  R_qual
```

来源关系很简单：`AToM` 给 `event following` 的拆法，`MotionCritic` 给 `perceptual quality` 的独立性，`PAPO` 给 reward-family 的分 lane 思想，`ReAlign` 给这两路信号进入 step-aware guidance 的位置。

如果写成方法，最像下面这种：

1. **Event-following lane**
   - 主打 `R_pres`
   - `R_ord` 只在 separability gate 过后再开
   - `R_dur` 继续留接口，不抢 MVP
2. **Quality lane**
   - 先用轻量 perceptual proxy
   - 目标不是证明“绝对真实”，而是防止文本跟随增强把 motion quality 拉崩
3. **Step schedule**
   - 早期 denoising step：以 quality / global coherence 为主
   - 中后期 denoising step：逐步加大 event-following lane
4. **Interval-aware weighting**
   - 对 ordering-sensitive interval 权重更高
   - 对明显不相关区间少施压，减少 guidance 噪声

这会比“AToM 的事件分解 + ReAlign 的 guidance”更完整，因为你多了两件 reviewer 很难忽略的东西：

1. **quality-preserving 叙事**
2. **temporal focus / interval weighting 叙事**

### 4.4 如何服务 MoDebug 的 contribution 写法

如果收敛成 paper-safe 版本，我建议未来 contribution package 写成 3 件事，而不是 1 件事：

1. **Temporal-aware event sensitivity evaluation**
   - 解决“现有 global metrics 看不见 ordering / omission”的问题
2. **Quality-preserving event-level guidance**
   - 解决“文本跟随增强容易伤自然度”的问题
3. **Counterfactual diagnostic for event reward validity**
   - 解决“为什么这不是简单拼接”的问题

这样一来，你的方法贡献就不再只是：

> event-level reward + step-aware guidance

而会变成：

> event-level reward guidance + temporal-aware eval + quality-preserving decomposition + counterfactual validation

这个组合明显更像一个完整 contribution，而不是一条机械桥接。

### 4.5 具体优先级建议

**P0：立刻该补的**

1. `event corruption eval stack`
2. `R_pres / R_ord` 的 delta 指标体系
3. quality lane 的最小 proxy

**P1：在 P0 稳后再补的**

1. interval-aware weighting
2. windowed local score / temporal focus probe
3. on-policy hard-negative bank 的系统化

**P2：明确属于 later extension 的**

1. APPO-style interval miner
2. PRCO-style observer branch
3. full RL post-training（SoPo / EasyTune / GRPO family）

## 5. 新构建的 contribution，是否真的补强当前 MoDebug Plan？

### 5.1 短答案

**能补强，而且是实质性补强；但前提是 scope 控制住。**

### 5.2 它具体补强了什么

| 当前薄弱点 | 新 contribution 是否补到 | 为什么 |
| --- | --- | --- |
| ordering / omission 的评测抓手不足 | 是 | temporal-aware event sensitivity eval 直接补评测口 |
| reviewer 质疑简单拼接 | 是 | 多了 eval、quality lane、counterfactual diagnostic 三重差异 |
| 只追 text following 可能伤 naturalness | 是 | dual-lane guidance 明确把 quality 拉进主方法叙事 |
| `R_ord` 证据弱 | 部分补强 | corruption + interval weighting + focus probe 能补证据，但未必立即解决 scorer 上限 |
| `R_dur` 太早做会爆 scope | 是 | 新框架允许它继续只当接口，不妨碍主线成立 |

### 5.3 它没有自动解决什么

1. **它没有自动提供一个强时序 scorer**
   - `TMR` 仍然不是 ordering 金标准
2. **它没有自动保证 noisy state 上 event reward 稳定**
   - 这仍然是 ReAlign-style guidance 最难的核心问题
3. **它没有让 `R_dur` 瞬间变简单**
   - duration 仍然应是 sidecar
4. **它没有替代 HumanML3D-E 的结构优势**
   - 你仍然高度依赖 ordered-event cache

### 5.4 对 `paperIDEAs/MoDebug/archived/related_work_and_backbone_comparison/2026-04-26_modebug-plan-b-core-reading-list.md` 的补强建议

不要推翻那份 reading list，而是给它加一个 **Supplement Track** 会更合理。

建议补一个新层：

1. **Temporal / Perception Supplement**
   - `PAPO`
   - `Perception-R1`
   - `VideoZoomer`
   - `AVATAR`
   - `APPO`
2. **RL Mechanics Supplement**
   - `DIVA-GRPO`
   - `CalibRL`
   - `GVPO`

对应角色：

- `PAPO / Perception-R1`：解释为什么要拆 reward family、什么时候细粒度感知 supervision 值得做
- `VideoZoomer / AVATAR / APPO`：解释为什么 temporal focus 和关键区间加权值得进入 eval / guidance
- `DIVA-GRPO / CalibRL / GVPO`：解释怎么设计 hard negatives、方差、权重与探索策略

### 5.5 对当前 Plan B 最稳的建议

如果只允许你在现有 Plan B 上加 1 层，而不改主骨架，我建议加的是：

> **把 Plan B 从“event-level inference-time guidance”升级成“event-level guidance + temporal-aware eval + minimal quality lane”。**

这一步最划算，因为：

1. 不需要立刻改成 full RL pipeline
2. 不需要立刻训练 observer / miner
3. 却能显著增强 contribution 的完整度和 reviewer defensibility

## 6. 一句话收口

如果只用一句话记住这份笔记，那就是：

> `MoDebug Plan B` 真正需要的 RL 核心，不是把整套经典 RL 都学完，而是看懂这条递进链：**reward 最大化 → 偏好学习 → diffusion alignment → step-aware guidance → event-level reward decomposition → perception-aware reward family**；只要这条链打通，你就已经具备读懂当前 reading list 和参与方案判断的能力了。
