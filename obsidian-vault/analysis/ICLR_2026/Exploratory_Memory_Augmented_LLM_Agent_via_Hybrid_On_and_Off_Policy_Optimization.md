---
title: "Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Exploratory_Memory_Augmented_LLM_Agent_via_Hybrid_On_and_Off_Policy_Optimization.pdf
project_link: https://agent-lightning.github.io/posts/empo2/
code_link: https://github.com/microsoft/agent-lightning/tree/main/contrib/recipes/envs
openreview_forum_id: UOzxviKVFO
aliases:
- EMALAHOPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "EMPO² augments LLM-agent RL with self-generated reflection memory and hybrid on-policy/off-policy optimization."
primary_logic: "The agent stores tips from trajectory reflection, retrieves relevant tips during rollouts, and distills memory-guided high-reward behavior back into the base policy through mixed updates."
claims:
- "Memory retrieval provides structured exploration beyond the current policy sampling distribution."
- "Off-policy updates reinterpret memory-enhanced trajectories without tip conditioning to internalize useful behaviors."
- "The note reports large ScienceWorld and WebShop gains over GRPO, with memory, off-policy updates, and intrinsic reward all important."
---

# Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization

> [!tip] 核心洞察
> Exploratory

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization |
| 英文题名 | Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=UOzxviKVFO) · [GitHub](https://github.com/microsoft/agent-lightning/tree/main/contrib/recipes/envs) · [Project](https://agent-lightning.github.io/posts/empo2/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method |  |
| Dataset | |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

大语言模型（LLM）智能体在复杂交互环境中面临一个根本瓶颈：**探索不足导致策略过早收敛到次优解**。以 GRPO（Group Relative Policy Optimization）为代表的在线强化学习方法，虽然通过组内相对优势比较移除了对价值函数的依赖，但其探索完全由策略自身的随机性驱动，缺乏引导探索的结构化机制。在 ScienceWorld 等需要多步推理与空间导航的任务中，GRPO 训练的策略往往陷入局部最优——例如在“打开红色灯泡”任务中，智能体始终无法找到目标物体，Reward 曲线长期停滞。

针对这一问题，本文提出 **EMPO²（Exploratory Memory-Augmented On- and Off-Policy Optimization）**，一种融合记忆增强探索与混合策略优化的强化学习框架。其核心思路是：**让策略在训练过程中自行生成反思性提示（tips），存入记忆缓冲区，并在后续 rollout 中检索相关提示以引导探索**；同时，通过 on-policy 与 off-policy 更新的混合调度，将记忆引导的探索收益固化为参数化策略的稳定提升。

在 **ScienceWorld** 的 19 个任务上（训练 5 个变体，测试 20 个变体），EMPO² 取得平均 Return **75.9**，相较 GRPO 的 33.2 提升 **42.7 分（相对提升 128.6%）**。在 **WebShop** 上，EMPO² 取得平均得分 88.3，相较 GRPO 提升 11.3%。训练曲线显示，GRPO 在多数任务上收敛到次优性能后不再改进，而 EMPO² 持续探索并最终完成任务。

方法层面，EMPO² 属于**记忆增强的在线 RL + 离线 RL 混合范式**，其关键设计包括：（1）自我生成记忆缓冲区，以余弦相似度检索 top-10 提示；（2）rollout 阶段以概率 $p$ 在无记忆/记忆增强两种模式间采样；（3）update 阶段以概率 $q$ 在 on-policy/off-policy 两种模式间切换，off-policy 更新将存储的 log-probability 替换为仅条件于状态和任务的值，消除记忆条件带来的分布偏移；（4）token 级掩码与内在奖励机制稳定训练并维持策略熵。消融实验表明，记忆模块、off-policy 更新、内在奖励三者缺一不可，且超参数 $p$ 和 $q$ 存在最优区间（$p=0.25$ 稳定收敛，$q=0.85$ 早期探索最快），极端取值会显著损害性能。



### 大语言模型智能体的探索困境

将大语言模型（LLM）作为自主智能体部署于交互式环境时，其核心挑战并非模型缺乏先验知识，而是**探索不足**。以 ScienceWorld 基准中的“打开红色灯泡”任务为例：智能体必须先定位红色灯泡，再执行激活操作。然而，基于 GRPO 训练的智能体在策略初始化阶段（π₀）便反复尝试“聚焦于红色灯泡”并失败，训练至 π₂₀₀ 时行为模式几乎未变——它始终无法发现正确的物体定位路径。学习曲线印证了这一观察：GRPO 在 ScienceWorld 的 power-component 任务上快速收敛至次优性能后便停滞不前，而 EMPO2 则持续改进并最终完成任务（Figure 1a）。

这一困境的根源在于 LLM 智能体的**动作空间与状态空间高度耦合**：模型生成的文本动作直接决定了环境返回的观察状态，而状态分布又反过来塑造策略梯度方向。当早期策略缺乏有效探索时，模型只能反复采样低质量轨迹，形成“差策略→差数据→更差策略”的恶性循环。Figure 3 以漫画式插图直观展示了这一过程——智能体在多个训练步中循环于相同的失败模式，策略熵持续下降而回报毫无提升。

### 现有方法的三条路径及其缺口

当前提升 LLM 智能体探索能力的方法可归为三类，但各自存在结构性缺陷：

**非参数化反思（Non-Parametric Reflexion）** 将失败经验存储为文本记忆，在后续推理时检索并作为提示注入。该方法不更新模型参数，仅依赖上下文学习。其优势在于记忆可跨任务累积，但劣势同样明显：反思内容的质量受限于初始策略的失败模式多样性，且无法将经验内化为参数化能力，导致泛化边界由检索质量决定。

**离线强化学习（Offline RL）** 如 Retrospex，从预收集的静态数据集中学习，避免了在线交互的探索成本。然而，ScienceWorld 等开放式环境中，预收集数据难以覆盖长尾状态分布，模型在分布外（OOD）测试变体上的表现急剧退化。Figure 1(b) 的柱状图显示，Retrospex 在 ScienceWorld 的 ID 设定下表现尚可，但 OOD 性能显著低于在线方法。

**在线强化学习（Online RL）** 以 GRPO 为代表，通过与环境实时交互采样轨迹并更新策略。理论上，在线学习具备最强的适应能力；实践中，GRPO 却因探索不足而收敛至次优解。其症结在于：GRPO 的更新信号完全来自当前策略采样的轨迹，当策略陷入局部最优时，梯度更新无法提供逃离该区域的驱动力。Figure 1(b) 中 GRPO 在 ScienceWorld 上的平均 Return 仅为 33.2，远低于 EMPO2 的 75.9。

### 核心动机：记忆驱动的混合优化

上述三条路径并非互斥，而是互补。非参数化记忆能够存储多样化经验并引导探索，但其本身无法转化为参数化能力；在线策略更新能够内化经验，却受限于当前策略的采样分布；离线更新可以利用历史数据打破采样偏差，但需要高质量的经验来源。

本文的核心动机正是**将这三者耦合为一个闭环**：用非参数化记忆存储并检索探索性经验，以此条件化在线策略的采样过程，提升轨迹多样性；再将记忆中的高质量经验通过离线更新蒸馏为参数化能力，同时离线更新的结果反过来重新评估记忆内容，形成“探索→记忆→蒸馏→再探索”的正反馈循环。Figure 2 的概念图概括了这一思想：非参数化更新鼓励探索，进而引导参数化更新。Figure 4 进一步展示了这一循环的具体实现——当前策略参数 π_θ 被用于回顾历史轨迹，产生的洞察追加至记忆，更新后的记忆再条件化后续采样。

这一设计直接回应了 GRPO 探索不足的根本瓶颈：当策略陷入局部最优时，记忆中的多样化经验为采样提供了额外的状态-动作候选，而离线更新则利用这些经验向策略注入逃离局部最优的梯度信号。



## 核心方法与创新机理

EMPO2（Exploratory Memory-Augmented On- and Off-Policy Optimization）的核心创新在于将**自生成记忆驱动的探索**与**混合在线/离线策略优化**统一到一个框架中，从根本上解决了GRPO等纯在线RL方法在LLM智能体训练中因探索不足而陷入次优解的问题。

### 创新一：自生成记忆驱动的持续探索

传统在线RL（如GRPO）仅依赖标量奖励信号指导策略更新，在稀疏奖励环境中极易收敛至局部最优——智能体反复尝试相似动作而无法发现正确路径。EMPO2通过引入一个非参数记忆缓冲区 $\mathcal{M} = \{\mathrm{tip}_1, \mathrm{tip}_2, \dots\}$ 来打破这一僵局：策略 $\pi_{\boldsymbol{\theta}}$ 在轨迹反思阶段自行生成反思性提示（tips），而非依赖外部模型，这些提示被存入记忆并用于条件化后续rollout的提示构建。

具体而言，记忆增强提示在rollout时通过检索算子 $\mathrm{Retr}(o_t; \mathcal{M})$ 选取与当前状态最相关的提示（上限10条），引导智能体尝试被纯参数策略忽略的动作路径。这一机制使探索不再完全受限于当前策略参数的分布，形成“非参数更新引导探索，探索数据反哺参数更新”的正反馈循环。

### 创新二：混合在线/离线策略优化

EMPO2在rollout阶段采样两种模式——无记忆提示（概率 $1-p$）和记忆增强提示（概率 $p$）——在更新阶段则同时执行在线策略（on-policy）和离线策略（off-policy）更新，构成三种模式组合：

- **在线策略无记忆学习**：标准GRPO式更新，保持参数策略的基础能力。
- **在线策略有记忆学习**：对记忆增强轨迹进行重要性采样更新，将探索成果直接注入参数策略。
- **离线策略学习**：将记忆增强轨迹中存储的log-probability替换为仅条件于状态和任务的log-probability，使同一策略在无记忆条件下重新评估这些轨迹。这实质上是**奖励引导的知识蒸馏**——高奖励的记忆探索轨迹被蒸馏回参数策略，提升其独立执行能力。

这一设计的关键洞察在于：离线策略更新充当了在线策略更新的“引导信号”，将记忆探索中发现的高质量行为模式内化到参数策略中，而在线策略更新则确保策略在无记忆条件下仍能稳定执行。

### 创新三：训练稳定性保障机制

EMPO2引入两项辅助技术确保混合训练过程的稳定性：

1. **Token掩码**：对于概率低于阈值 $\delta$ 的token，在PPO损失中将其更新屏蔽，防止低概率token导致梯度爆炸或NaN发散。
2. **基于状态新颖性的内在奖励**：维护一个状态记忆列表，对每个新状态计算其与已有状态的余弦相似度；若相似度低于阈值，则给予内在奖励 $r_{\mathrm{intrinsic}} = \frac{1}{n}$（$n$ 为相似历史状态数），显式鼓励访问新颖状态，维持策略熵在高位。

### 与基线方法的本质差异

相较于GRPO仅依赖在线策略更新的单一范式，EMPO2的changed slots体现在三个维度：

| 维度 | GRPO | EMPO2 |
|------|------|-------|
| 探索机制 | 仅参数策略采样 | 自生成记忆增强探索 |
| 更新范式 | 纯在线策略 | 在线+离线混合策略 |
| 信号来源 | 仅外部奖励 | 外部奖励+内在新颖性奖励+记忆蒸馏信号 |

这一组合使EMPO2在ScienceWorld上实现平均Return从GRPO的33.2跃升至75.9（+128.6%），且训练曲线持续上升而非过早饱和，验证了混合范式在克服探索瓶颈上的决定性作用。



EMPO² 是一种面向 LLM Agent 的混合强化学习框架，其核心设计围绕**探索性记忆增强**与**混合策略优化**两条主线展开。框架在训练过程中交替运行两种 rollout 模式与两种更新模式，通过非参数记忆模块桥接探索与利用，形成自增强的学习循环。

### 总体流程

EMPO² 的训练循环可分解为四个阶段，构成闭环：

1. **Rollout 采样**：当前策略 $\pi_\theta$ 在环境中执行任务，按概率 $p$ 随机选择两种 rollout 模式之一——「无记忆提示」模式直接依赖策略生成动作，而「记忆增强提示」模式则从记忆缓冲区 $\mathcal{M}$ 中检索与当前状态相关的 tips 作为额外上下文。两种模式下均收集完整的轨迹数据。

2. **轨迹反思与记忆写入**：对于每条完成（无论成功或失败）的轨迹，策略 $\pi_\theta$ 自身被提示进行反思，生成一条反思性 tip：
   $$\mathrm{tip}_i \sim \pi_{\boldsymbol{\theta}}(s_T, \boldsymbol{u}, \text{tip-generation prompt})$$
   该 tip 被存入记忆缓冲区 $\mathcal{M} = \{\mathrm{tip}_1, \mathrm{tip}_2, \dots\}$，形成不断累积的探索知识库。值得注意的是，tips 并非由独立模型生成，而是由持续训练中的策略自身产生，这意味着记忆质量随策略提升而动态改善。

3. **混合策略更新**：框架同时执行两类参数更新：
   - **On-policy 更新**：对记忆增强 rollout 产生的轨迹，使用标准 GRPO 目标进行梯度更新，重要性采样比 $\rho_\theta$ 基于条件于 tips 的 log-probabilities 计算（参见 Table 3）。
   - **Off-policy 更新**：将记忆增强 rollout 中存储的 log-probabilities 替换为策略在仅条件于状态和任务（不含 tips）时分配的概率，重新计算损失。这一机制被作者解释为在线训练过程中的**奖励引导知识蒸馏**——将探索阶段发现的优质行为蒸馏回无条件策略，同时抑制低概率 token 的更新（通过 token masking 机制，见 Figure 6）。

4. **内在奖励注入**：为鼓励状态空间探索，框架引入基于新颖性的内在奖励。维护一个状态记忆列表，对每个新状态计算其与已有状态的余弦相似度；若相似度低于阈值，则赋予内在奖励 $r_{\mathrm{intrinsic}} = 1/n$（$n$ 为相似状态数量），该奖励与外在任务奖励叠加后用于优势函数计算。

### 模块关系与数据流

框架的核心模块及其交互关系如下：

```
┌─────────────────────────────────────────────────────────┐
│                    EMPO² Training Loop                   │
├─────────────────────────────────────────────────────────┤
│  ┌──────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │ Rollout   │───▶│ Trajectory   │───▶│ Memory Buffer │  │
│  │ (π_θ)     │    │ Reflection   │    │ M = {tip_i}   │  │
│  │           │    │ (tip gen)    │    └───────┬───────┘  │
│  │ mode:     │    └──────────────┘            │          │
│  │ · no mem  │                                │ retrieve │
│  │ · w/ mem  │◀───────────────────────────────┘          │
│  └─────┬─────┘                                           │
│        │ trajectories                                    │
│        ▼                                                 │
│  ┌──────────────────────────────────────────┐            │
│  │        Hybrid Policy Update               │            │
│  │  ┌─────────────────┐ ┌─────────────────┐  │            │
│  │  │ On-policy Loss  │ │ Off-policy Loss │  │            │
│  │  │ (w/ tips,       │ │ (w/o tips,      │  │            │
│  │  │  token masking) │ │  token masking) │  │            │
│  │  └────────┬────────┘ └────────┬────────┘  │            │
│  │           └──────────┬────────┘            │            │
│  │                      ▼                     │            │
│  │               π_θ update                  │            │
│  └──────────────────────────────────────────┘            │
│                                                          │
│  Intrinsic Reward: r_int = 1/n (novelty-based)           │
└─────────────────────────────────────────────────────────┘
```

**输入**：任务描述 $u$，初始状态 $s_0$，记忆缓冲区 $\mathcal{M}$（初始为空）。

**输出**：更新后的策略参数 $\theta$，以及持续累积的记忆缓冲区 $\mathcal{M}$。

### 三种模式组合

通过组合两种 rollout 模式与两种更新模式，EMPO² 实际运行三种有效的模式配置（Figure 5）：

| 模式 | Rollout | Update | 功能定位 |
|------|---------|--------|----------|
| On-policy 无记忆 | 无 tips | On-policy | 基础利用，维持策略稳定性 |
| On-policy 有记忆 | 含 tips | On-policy | 记忆引导探索，直接优化带记忆的策略 |
| Off-policy | 含 tips | Off-policy | 将探索发现蒸馏至无条件策略，提升泛化性 |

消融实验（Figure 9）表明，移除任一模式组件均导致次优学习，验证了混合设计的必要性。

### 关键设计决策

- **自生成记忆**：tips 由策略自身生成而非外部模型，确保记忆与当前策略能力对齐，避免分布外知识污染。
- **Token masking**：在 PPO 损失中，对概率低于阈值 $\delta$ 的 token 屏蔽梯度更新，有效防止训练发散至 NaN（Figure 6）。
- **内在奖励**：基于状态新颖性的奖励机制维持策略熵高于无内在奖励的基线（Figure 7），对抗 LLM Agent 在稀疏奖励环境中的探索不足问题。

> **证据强度提示**：上述框架描述基于论文第 4 节方法论及 Figure 4-7 的佐证。Table 3 提供了重要性采样比在不同模式下的精确计算方式，Figure 11 展示了内在奖励配置的敏感性分析。关于 off-policy 更新作为「奖励引导知识蒸馏」的论断来自第 5 节相关工作的定性描述，其机制层面的严格等价性需进一步验证。



### 记忆增强的探索机制

EMPO2 在 rollout 阶段引入两种模式：**无记忆提示**与**记忆增强提示**。记忆缓冲区定义为

$$\mathcal{M} = \{\mathrm{tip}_1, \mathrm{tip}_2, \dots\}$$

其中每个 tip 由策略自身在轨迹反思阶段生成，而非由独立模型产生：

$$\mathrm{tip}_i \sim \pi_{\boldsymbol{\theta}}(s_t, \boldsymbol{u}, \text{tip-generation prompt})$$

在记忆增强模式下，通过检索算子 $\mathrm{Retr}(o_t; \mathcal{M}) \subseteq \mathcal{M}$ 选取与当前状态 $s_t$ 最相关的 tips（上限为 10 条），将其注入后续 rollout 的上下文中，从而促进探索。

### 混合策略优化

EMPO2 在更新阶段同样区分两种模式：**on-policy 更新**与**off-policy 更新**，与 rollout 模式组合形成三种配置（on-policy 无记忆、on-policy 有记忆、off-policy 学习）。

**On-policy 重要性采样比**（记忆增强模式下）：

$$\rho_{\theta}(a_t^{(i)}) = \frac{\pi_{\theta}(a_t^{(i)} \mid s_t^{(i)}, u, \mathrm{tips}_t)}{\pi_{\theta_{\mathrm{old}}}(a_t^{(i)} \mid s_t^{(i)}, u, \mathrm{tips}_t)}$$

**Off-policy 更新**则将存储的 log-probability 替换为仅以 $(s_t, u)$ 为条件的 log-probability，使同一策略在无记忆条件下重新评估历史动作。

### 带 Token Masking 的 PPO 损失

为保证训练稳定性，EMPO2 引入 token 级别的 masking 机制。当某 token 在当前策略下的概率低于阈值 $\delta$ 时，该 token 的更新被抑制。损失函数形式为：

$$\mathbb{E}_{u \sim p(\mathcal{U})} \{ \tau^{(i)} \} \sim \pi_{\theta_{\mathrm{old}}} \left[ \frac{1}{NT} \sum_{i=1}^{N} \sum_{t=1}^{T} \min(\rho_{\theta}^{(i,t)} A(a_t^{(i)}), \mathrm{clip}(\rho_{\theta}^{(i,t)}, 1-\epsilon, 1+\epsilon) A(a_t^{(i)})) \cdot \mathbb{1}[\pi_{\theta}(a_t^{(i)}) > \delta] \right]$$

其中 $\mathbb{1}[\cdot]$ 为指示函数，仅在 token 概率高于 $\delta$ 时参与梯度更新。该设计有效防止训练发散至 NaN。

### 内在奖励

为鼓励状态层面的探索，EMPO2 引入基于新颖性的内在奖励。维护一个状态记忆列表，对每个新状态计算其与已有状态的余弦相似度；若相似度低于阈值，则赋予内在奖励 $r_{\mathrm{intrinsic}} = \frac{1}{n}$，其中 $n$ 为相似历史状态的数量。该奖励作为外在任务奖励的补充，有助于维持更高的策略熵。



## 实验与关键发现

### 主结果：ScienceWorld 与 WebShop 性能对比

EMPO² 在两个具身决策基准上均取得显著提升。在 ScienceWorld 上，EMPO² 的平均 Return 达到 **75.9**，而 GRPO 仅为 33.2，绝对提升 +42.7，相对提升 **128.6%**（Table 1）。这一优势在 19 个任务中具有一致性——EMPO² 在多个任务上取得最佳性能。值得注意的是，非参数方法 Reflexion 仅获得 17.1 的平均 Return，离线 RL 方法 Retrospex 的表现也远低于 EMPO²，表明单纯的记忆反思或离线学习无法替代混合策略带来的增益。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_UOzxviKVFO/figures/009_Table_1.jpg]]
*Table 1: Comparison results of ScienceWorld. Each task in ScienceWorld contains multiple variants. We use the first five variants for training and evaluate on the 20 unseen test variants. Bold shows the best performance per task, while red shading marks cases where parametric updates score lower than non-parametric updates. The EMPO2 performance we evaluate is the performance of the trained model without memory at test time*

在 WebShop 上，EMPO² 取得 **88.3±2.6** 的平均分数和 **75.6±3.1%** 的成功率，相较于 GRPO（79.3±2.8 / 66.1±3.7%）分别提升 11.3% 和 9.5 个百分点（Table 2）。EMPO² 同样超越了 GiGPO 的两个变体（w/ std: 84.4±2.9 / 72.8±3.2%；w/o std: 86.2±2.6 / 75.2±2.3%），验证了混合 on/off-policy 优化的有效性。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_UOzxviKVFO/figures/013_Table_2.jpg]]
*Table 2: Comparison results of WebShop. Following Feng et al. (2025b), we average results over three random seeds and report both the mean score and the mean success rate (%). $\mathrm { G i G P O } _ { \mathrm { w } / }$ std denotes the use of the normalization factor $F _ { \mathrm { n o r m } } = \mathrm { s t d }$ , whereas $\mathrm { G i G P O _ { w / o \ s t d } }$ uses $F _ { \mathrm { n o r m } }$ = 1 , as specified in Feng et al. (2025b). The $\mathrm { E M P O ^ { 2 } }$ performance we evaluate is the performance of the trained model without memory at test time

### 训练动态：突破 GRPO 的收敛瓶颈

Figure 1(a) 的学习曲线揭示了 GRPO 的核心失败模式：在 ScienceWorld 的 power-component 任务上，GRPO 迅速收敛到次优策略并停滞，而 EMPO² 持续改进并最终完成任务。Figure 3 进一步诊断了这一现象——在 "turn on the red light bulb" 任务中，GRPO 训练的 agent 从 π₀ 到 π₂₀₀ 始终重复 "focus on light bulb" 的失败动作，无法定位红色灯泡。EMPO² 通过记忆增强的提示（memory-augmented prompting）使 agent 能够检索过去的失败经验作为 tips，从而打破重复错误的循环。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_UOzxviKVFO/figures/002_Figure_1.jpg]]
*Figure 1: (a) Comparison of the learning curves of GRPO and EMPO2 (ours) on the Science-World power-component task. While GRPO converges to suboptimal performance, EMPO2 continues to improve and accomplish the task. (b) Comparison of $\mathbf { E M P O ^ { 2 } }$ and other baselines in in-distribution (ID) and out-of-distribution (OOD) settings on and WebShop. In ID experiments, it adapts well to familiar environments, achieving 128.6% on ScienceWorld and 11.3% on Webshop improvements over GRPO. In OOD experiments, it also shows strong performance with few trials and no weight updates, indicating effective use of memory to explore unfamiliar environments. Full results are in Tables 1, 2, and Figure 8*

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_UOzxviKVFO/figures/004_Figure_3.jpg]]
*Figure 3: When training LLM with GRPO in ScienceWorld, the agent struggles because of insufficient exploration. For instance, in the task “turn on the red light bulb,” the agent must first find the red light bulb before activating it. However, the agent fails to locate it and, as a result, cannot complete the task. Rather than analyzing the cause of failure and exploring alternative actions, the agent proceeds unchanged, so its score stagnates even as additional training steps are taken*

### 消融分析：三种模式组合的贡献

EMPO² 包含三种模式组合：无记忆的 on-policy 学习、有记忆的 on-policy 学习、以及 off-policy 学习。Figure 9 的消融实验表明，移除任一组件都会导致次优学习——单独移除 off-policy 学习或移除有记忆的 on-policy 学习均使训练曲线显著下降。这证实了混合优化的必要性：on-policy 更新提供稳定的梯度信号，off-policy 更新则充当 reward-guided knowledge distillation，在在线训练中引导策略向高回报区域靠拢。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_UOzxviKVFO/figures/015_Figure_9.jpg]]
*Figure 9: Comparison of training curves between $\mathrm { E M P O ^ { 2 } }$ and variants that exclude either off-policy learning or on-policy learning with memory*

### 训练稳定性与探索机制

Token masking 机制对训练稳定性至关重要。Figure 6 显示，对概率低于阈值 δ 的 token 进行 masking 可有效防止训练发散至 NaN。在探索方面，Figure 7 对比了有无 intrinsic reward 时的策略熵——引入基于状态新颖性的 intrinsic reward 使策略保持更高的熵值，避免过早坍缩到确定性策略。Figure 11 进一步考察 intrinsic reward 的配置敏感性：标准配置（scale=1.0）优于 0.5× 和 2.0× 缩放变体，也优于用 RND 替代的变体和完全移除 intrinsic reward 的配置，表明适度且基于余弦相似度的 novelty 奖励设计是有效的。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_UOzxviKVFO/figures/023_Figure_11.jpg]]
*Figure 11: $\mathrm { E M P O ^ { 2 } }$ learning curves with different intrinsic reward configurations on ScienceWorld chemistry-mix-paint-secondary-color task. We compare our full method against four variants: scaling the intrinsic reward coefficient by 0.5× and 2 $\times$ , substituting it with a Random Network Distillation (RND) bonus, and its complete removal (w/o Intrinsic Reward)

### 快速适应与定性案例

Figure 8 展示了 EMPO² 的快速适应能力：在三个新任务场景中，EMPO² 在 10 步内平均提升 **136%**，而 GRPO 几乎无法从零开始学习。Figure 17 的定性案例对比了有无记忆的 agent 行为——在 ScienceWorld 的化学混合颜料任务中，无记忆 agent 重复在走廊倾倒黄色颜料而失败；有记忆 agent 则检索到 "不要在走廊混合颜料，去有工作台的地方" 等 tips，成功调整行为并完成任务。这一案例直观展示了记忆增强提示如何将过去的失败转化为可操作的探索引导。



## 定位与知识库关联

### 在LLM智能体强化学习中的位置

EMPO²处于**在线强化学习（online RL）与记忆增强（memory-augmented）智能体**的交叉点。在LLM智能体训练的谱系中，现有方法大致可分为三类基线：

- **非参数化反思方法**：如 **Reflexion**（Shinn et al., NeurIPS 2023），通过语言化的失败反思来改进后续尝试，但不进行参数更新。在ScienceWorld上平均Return仅为17.1（Table 1），验证了纯非参数化方法的性能上限有限。
- **离线RL方法**：如 **Retrospex**（Feng et al., 2025b），从静态数据集中学习，在ScienceWorld上平均Return为23.0，在WebShop上得分为73.1±4.1。离线方法受限于数据分布，难以应对OOD场景。
- **在线RL方法**：以 **GRPO**（Shao et al., 2024）为代表，通过组内相对优势进行策略优化，在ScienceWorld上平均Return为33.2，在WebShop上得分为79.3±2.8。GRPO的核心瓶颈在于**探索不足导致策略早熟收敛**——Figure 3展示了GRPO在ScienceWorld中反复陷入同一失败模式（如找不到红色灯泡），策略熵随训练持续下降而无法跳出局部最优。

EMPO²的核心突破在于将**非参数化记忆更新**与**参数化策略优化**融合为统一的混合框架。其方法定位可以理解为：以GRPO的在线RL为基础，引入自生成记忆缓冲区（self-generated memory buffer）来驱动探索，并通过on-policy/off-policy双模式更新来同时利用记忆增强轨迹和无记忆轨迹。这种设计使EMPO²在ScienceWorld上达到75.9的平均Return（相对GRPO提升128.6%），在WebShop上达到88.3±2.6的得分（相对GRPO提升11.3%）。

### 与后续工作的关系与适用边界

EMPO²的方法架构包含三个可组合的模式：**无记忆on-policy学习**、**记忆增强on-policy学习**、以及**off-policy学习**。Figure 9的消融表明，移除任一组分均导致次优学习——这暗示该方法在**需要持续探索的长程任务**中最为关键，而在简单或短视任务上，纯GRPO可能已足够。

论文明确指出的适用边界和开放方向包括：

- **检索机制的改进空间**：当前使用余弦相似度进行记忆检索，且检索数量限制为10条。更先进的检索机制可能进一步提升性能。
- **模型泛化性待验证**：当前实验主要在特定模型上进行，扩展到更广泛的模型家族和规模可能揭示方法的鲁棒性边界。
- **领域迁移潜力**：论文提出将EMPO²应用于数学推理、代码生成、多跳问答和多模态RL等新领域，这些场景中的记忆结构和探索需求可能与当前环境存在本质差异。

### 局限与待验证问题

从实验设置可识别的关键局限：

1. **ScienceWorld的变体分布**：训练使用每任务的前5个变体，测试使用20个未见变体。虽然这构成了OOD评估，但变体之间的差异程度未被量化——如果变体间差异较小，则OOD泛化能力的宣称需要谨慎解读。

2. **内在奖励的通用性**：基于状态新颖性的内在奖励（$r_{\mathrm{intrinsic}} = 1/n$）在ScienceWorld中有效，但其依赖于状态表示的余弦相似度计算。在离散动作空间或高维文本状态空间中，该机制的适用性需要进一步验证。Figure 7仅展示了策略熵的比较，未提供内在奖励在不同任务类型上的敏感性分析。

3. **训练稳定性机制**：Token masking被证明能稳定训练（Figure 6），但该机制引入的概率阈值δ是一个关键超参数，论文未讨论其对不同任务的敏感性。

4. **记忆质量的自反馈循环**：由于记忆提示（tips）由策略自身生成，低质量策略可能产生误导性记忆，形成负反馈循环。论文未分析记忆质量随训练进程的演化规律，这是实际部署中需要关注的风险点。



## 原文 PDF

![[paperPDFs/ICLR_2026/Exploratory_Memory_Augmented_LLM_Agent_via_Hybrid_On_and_Off_Policy_Optimization.pdf]]
