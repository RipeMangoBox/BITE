---
title: "Unsupervised Learning of Efficient Exploration: Pre-training Adaptive Policies via Self-Imposed Goals"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Unsupervised_Learning_of_Efficient_Exploration_Pre_training_Adaptive_Policies_via_Self_Imposed_Goals.pdf
project_link: null
code_link: https://github.com/Octavio-Pappalardo/ulee-jax
openreview_forum_id: UmxTIxHWkl
aliases:
- ULEEPTAPSIG
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入基于适应后表现的难度指标（后 K 个回合的成功率），并通过对抗训练的搜索策略生成处于智能体能力前沿的目标，配合难度预测网络构建课程。"
primary_logic: "通过上下文元学习训练无条件策略，并利用自我生成且难度适中的目标课程进行预训练，使智能体习得可跨任务迁移的探索与适应行为。"
claims:
- "ULEE 在探索评估中达到 DIAYN 两倍以上的目标达成率，且适应后收益提升至多 3 倍。"
- "消融实验表明，移除对抗目标搜索或边界采样会显著降低性能，且基于适应后表现的课程在更高难度基准上优势更明显。"
- "ULEE 初始化在长期微调（达 10^9 步）中始终优于从头训练和 DIAYN 预训练，并在监督元学习中提供更强的起点。"
- "4Rooms‑Trivial / 4Rooms‑Small / 6Rooms‑Small 上 探索阶段目标达成率（percentage of μ_eval goals reached） = ULEE (adversarial+bounded)"
---

# Unsupervised Learning of Efficient Exploration: Pre-training Adaptive Policies via Self-Imposed Goals

> [!tip] 核心洞察
> 通过上下文元学习训练无条件策略，并利用自我生成且难度适中的目标课程进行预训练，使智能体习得可跨任务迁移的探索与适应行为。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 无监督高效探索：基于自我目标的自适应策略预训练 |
| 英文题名 | Unsupervised Learning of Efficient Exploration: Pre-training Adaptive Policies via Self-Imposed Goals |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=UmxTIxHWkl) · [GitHub](https://github.com/Octavio-Pappalardo/ulee-jax) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | ULEE |
| Dataset | 4Rooms‑Trivial / 4Rooms‑Small / 6Rooms‑Small, 4Rooms‑Small（少样本适应）, 固定 μ_eval 任务（长期微调）, μ_train 上的监督元学习 |

> [!tip] 效果简介
> - 4Rooms‑Trivial / 4Rooms‑Small / 6Rooms‑Small 上，探索阶段目标达成率（percentage of μ_eval goals reached） 为 ULEE (adversarial+bounded)，对比 DIAYN / Random，变化 达成率提升超过一倍（20 回合时达两倍以上）。
> - 4Rooms‑Small（少样本适应） 上，第 30 回合平均收益（mean return） 为 ULEE，对比 DIAYN / Random，变化 收益提升至多 3 倍（由 ~0.2 至 ~0.6）。
> - 固定 μ_eval 任务（长期微调） 上，平均收益、第 40 和第 20 百分位收益 为 ULEE 初始化 + 微调，对比 从头训练 / DIAYN 预训练后微调，变化 所有百分位收益持续更高（微调至 10^9 步均保持优势）。

## 概要

现有无监督探索预训练方法面临一个关键瓶颈：它们仅依赖即时表现来衡量目标难度，却忽略了任务特定适应过程的动态变化，导致习得的策略难以泛化到分布外或未知目标上。本文提出 **ULEE（Unsupervised Learning of Efficient Exploration）**，一种无监督元学习方法，其核心思路是将**上下文自适应策略**与**对抗性目标生成机制**相结合，通过自我设定的目标课程来预训练智能体的探索与适应能力。

ULEE 的关键创新在于引入**基于适应后表现的难度指标**——即策略在多个回合交互后（而非首回合）的成功率补数——来指导目标生成。这一指标与**对抗训练的目标搜索策略**配合，使系统能够持续生成处于智能体能力前沿的挑战性目标，并通过难度预测网络高效构建课程，避免对每个候选目标进行昂贵的经验评估。

实验在多个网格世界基准上验证了 ULEE 的有效性：

- **探索能力**：ULEE 预训练策略在 20 回合探索预算下，目标达成率达到 DIAYN 的两倍以上（Figure 2）。
- **少样本适应**：在有限交互回合内，ULEE 策略的收益提升至多 3 倍（Figure 3a），且基于适应后表现的课程在更高难度基准上优势愈加显著。
- **长期微调**：ULEE 初始化在高达 10 亿步的微调预算中始终优于从头训练和 DIAYN 预训练（Figure 4）。
- **监督元学习**：ULEE 初始化作为元学习的起点，在 μ_eval 任务上获得更高的平均收益和分位数收益（Figure 5）。
- **零样本泛化**：在 MiniGrid 的 14 个任务中，ULEE 在 7 个任务上取得最优表现，尤其在操控类任务上优势明显（Table 1）。

消融实验进一步确认，移除对抗目标搜索或边界采样机制会显著降低性能，验证了 ULEE 各组件在构建有效探索课程中的必要性。



强化学习（RL）智能体在面对未知任务时，通常需要大量交互才能学会有效行为。无监督预训练旨在利用无任务标签的环境交互，提前习得可迁移的探索与适应能力，从而在下游任务上降低样本需求。然而，现有无监督探索预训练方法存在一个根本性瓶颈：**它们仅依赖即时表现来衡量目标难度，缺少对任务特定适应的考量**，导致习得的策略难以在分布外或未见过的目标上泛化。

以代表性方法 DIAYN 为例，其通过互信息最大化发现可区分的技能，并在下游用技能判别器作为奖励进行条件策略微调。这类方法的核心缺陷在于，目标难度的定义忽略了智能体在多个回合中逐步适应的能力——一个目标可能在首回合失败，但在经过若干回合的试探后变得可解。若课程仅根据即时成功与否生成目标，预训练策略便无法获得足够的“挣扎”经验，从而限制了其面对新任务时的适应潜力。

本文的动机正是填补这一缺口：**设计一种能够感知适应后表现的目标难度指标，并围绕该指标构建自监督课程，使预训练策略在无外界奖励的情况下学会探索、适应与泛化**。为此，作者提出 ULEE（Unsupervised Learning of Efficient Exploration），一种无监督元学习方法，其核心思路是将上下文自适应策略与对抗目标生成机制相结合，让智能体在与环境的多回合交互中自我驱动地成长。



## 核心方法与创新机理

ULEE 的核心创新在于重构了无监督探索预训练的三个关键环节，使其从“学习可区分的技能”转向“学习可迁移的探索与适应行为”。具体而言，该方法在以下五个维度上相对于现有基线（以 DIAYN 为代表）进行了系统性改进。

### 从目标条件策略到上下文自适应策略

传统无监督预训练方法（如 DIAYN）训练的是**目标条件策略（goal-conditioned policy）**，下游使用时需要显式提供目标编码作为输入。ULEE 则采用**无条件的上下文自适应策略（in-context meta-learner）**，其输入仅为完整的历史交互序列，通过黑盒元学习在多回合交互中学会探索和适应（Section 3.1）。这一架构变更的因果意义在于：预训练策略不再依赖外显的目标信号，而是将“理解当前任务”内化为一种从交互历史中涌现的能力，从而在分布外或未知目标上具备更强的泛化潜力。

### 从即时表现到适应后表现的难度度量

现有方法通常以首回合成功与否衡量目标难度，这忽略了智能体在多个回合中逐步适应任务的能力。ULEE 重新定义了**目标难度**：对于策略 $\pi$ 和环境 $M$，目标 $g$ 的难度是后 $K$ 个回合的期望成功率的补数（Eq. 2）：

$$d(g; \pi, M) = 1 - \mathbb{E}_{\rho_M, P_M, \pi} \left[ \frac{1}{K} \sum_{j=H-K+1}^{H} \mathbf{1}\{\exists t \in \{0,\dots,T-1\} : f(s_{t+1}^{(j)}) = g\} \right]$$

这一度量直接锚定在“适应后表现”上，而非即时表现。消融实验证实，基于适应后表现的课程在更高难度基准上优势愈发明显——这表明当任务空间复杂度上升时，仅凭即时成功与否筛选目标会导致课程过于简单，而适应后难度能更准确地识别处于智能体能力前沿的目标。

### 从随机采样到对抗目标搜索

基线方法通常从固定目标集或随机采样中获取训练目标。ULEE 引入了一个**对抗训练的 Goal-search Policy $\pi_{gs}$**，以目标难度作为奖励信号，主动搜索环境中困难的目标（Eq. 3）：

$$r_t^{gs} = r^{gs}(s_t; \pi, M) = d(f(s_t); \pi, M)$$

该搜索策略与预训练策略形成对抗关系：$\pi_{gs}$ 寻找 $\pi$ 难以适应的目标，而 $\pi$ 则在这些目标上训练以提升适应能力。消融实验表明，移除对抗搜索（改用随机搜索）会显著降低性能，而边界采样在随机搜索时尤为有效——这验证了对抗机制在生成“恰到好处”的挑战性目标上的关键作用。

### 从均匀采样到边界采样

在获得候选目标后，ULEE 并非对所有候选目标均匀采样，而是在难度区间 $[LB, UB]$ 内进行**边界采样（bounded sampling）**（Eq. 4）：

$$g_M \sim \operatorname{Unif}(S), \quad S = \{g \in GC_M : LB \leq d(g; \pi, M) \leq UB\}$$

这一设计确保训练目标始终处于中等难度——既不过于简单（无法推动能力增长），也不过于困难（导致无学习信号）。消融结果显示，边界采样在目标搜索为随机时效果尤为突出，说明它在一定程度上补偿了目标提议质量的不足。

### 从经验估计到难度预测网络

直接通过运行策略多个回合来估计目标难度成本高昂。ULEE 引入了**Difficulty Predictor 网络**，从近期目标缓冲区 $B_g$ 中学习预测目标难度，通过 L2 回归损失进行监督训练（Eq. 5）：

$$\mathcal{L}_{\mathrm{DP}}(\phi) = \frac{1}{|B_g|} \sum_{(g,\xi,\tilde{d}) \in B_g} \big( \hat{d}_\phi(g,\xi) - \tilde{d}(g) \big)^2$$

该预测器使目标搜索和选择无需额外的环境交互即可进行，大幅降低了课程构建的计算开销。缓冲区仅保存最近训练过的目标，确保预测器始终与智能体当前能力同步。

### 创新点的协同效应

上述五个 changed slots 并非孤立改进，而是形成了一条完整的因果链条：**适应后难度度量**定义了什么是“合适的目标”，**对抗目标搜索**生成处于能力前沿的候选目标，**边界采样**从中筛选中等难度的训练样本，**难度预测网络**使这一过程可规模化运行，而**上下文自适应策略**则在这些目标构成的课程上习得可迁移的探索与适应行为。这一链条的核心洞察在于：预训练的目标不应是学会特定技能，而是学会“如何快速学会”——这正是 ULEE 在探索评估中达到 DIAYN 两倍以上目标达成率、在少样本适应中收益提升至多 3 倍的根本原因。



ULEE 的整体设计围绕一个核心矛盾展开：**如何在不依赖人工标注的情况下，为自适应策略生成难度适中且能推动泛化的训练目标**。现有无监督探索预训练方法仅依赖即时表现衡量目标难度，缺少对任务特定适应的考量，导致习得的策略难以在分布外或未知目标上泛化。ULEE 通过引入基于适应后表现的难度指标，并构建一个由对抗目标搜索、难度预测和边界采样组成的闭环课程生成系统，从根本上改变了这一局面。

### 核心模块与数据流

ULEE 的训练管线由五个相互耦合的模块构成，其关系可概括为“一个策略、一个搜索器、一个预测器、一个采样器、一个缓冲区”：

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **Pre-trained Policy π** | 核心自适应策略，通过上下文元学习在多个回合的交互中学会探索和适应 | 历史交互序列（状态、动作、奖励） | 动作分布 |
| **Goal-search Policy π_gs** | 对抗训练的搜索策略，以目标难度为奖励，发现环境中困难的候选目标 | 环境状态 | 候选目标集合 |
| **Difficulty Predictor** | 从目标和环境上下文预测适应后难度，避免昂贵的在线估计 | 目标编码、环境上下文 | 难度预测值 |
| **Goal Selection Strategy** | 在难度区间 [LB, UB] 内均匀采样，提供中等难度的训练目标 | 候选目标及其预测难度 | 选中的训练目标 |
| **Goal Buffer B_g** | 保存近期训练目标及其经验难度估计，用于训练难度预测器 | 已训练目标、经验难度 | 监督信号 |

数据流形成一个闭环：Goal-search Policy 探索环境并收集候选目标 → Difficulty Predictor 估计每个候选目标的适应后难度 → Goal Selection Strategy 从中筛选中等难度的目标 → Pre-trained Policy π 在这些目标上执行多回合交互并记录经验难度 → 经验难度存入 Goal Buffer 用于更新 Difficulty Predictor。这一闭环确保课程始终与策略当前能力前沿保持同步。

### 关键设计决策

**无条件策略架构**：与传统的目标条件策略不同，ULEE 的 Pre-trained Policy π 不接收显式的目标编码输入，而是采用黑盒元学习方式，仅基于完整的历史交互序列选择动作。这使得策略在下游部署时无需额外的目标推断模块，可直接适应任意任务。

**适应后难度度量**：目标 $g$ 对策略 $\pi$ 的难度定义为后 $K$ 个回合的期望成功率的补数：

$$d(g; \pi, M) = 1 - \mathbb{E}_{\rho_M, P_M, \pi} \left[ \frac{1}{K} \sum_{j=H-K+1}^{H} \mathbf{1}\{\exists t \in \{0,\dots,T-1\} : f(s_{t+1}^{(j)}) = g\} \right]$$

该定义的前 $H-K$ 个回合作为适应期被忽略，仅关注策略适应后的表现。这一设计与传统基于即时成功的度量形成鲜明对比，是 ULEE 课程质量提升的核心因果杠杆。

**对抗目标搜索**：Goal-search Policy π_gs 以目标难度作为奖励进行训练：

$$r_t^{gs} = r^{gs}(s_t; \pi, M) = d(f(s_t); \pi, M)$$

搜索策略被激励去到达高难度状态，从而持续为 Pre-trained Policy 提供处于能力前沿的候选目标。消融实验证实，移除对抗搜索（改用随机搜索）会显著降低性能，验证了这一设计的必要性。

**难度预测器**：由于在线估计每个候选目标的难度需要运行策略多个回合，成本高昂，ULEE 引入 Difficulty Predictor 网络，通过 L2 回归从 Goal Buffer 中学习预测难度：

$$\mathcal{L}_{\mathrm{DP}}(\phi) = \frac{1}{|B_g|} \sum_{(g,\xi,\tilde{d}) \in B_g} \big( \hat{d}_\phi(g,\xi) - \tilde{d}(g) \big)^2$$

Goal Buffer 仅保留最近训练过的目标，确保预测器跟踪策略能力的变化。

### 预训练目标

整个系统的优化目标为最大化策略在 $H$ 个回合的终身期望折扣累积收益：

$$\mathcal{I}(\pi) = \mathbb{E}_{M \sim \mu^{\mathrm{msup}},\, g \sim p(g|M)} \left[ \mathbb{E}_{\rho_M, P_M, \pi} \left[ \sum_{j=1}^{H} \sum_{t=0}^{T-1} \gamma^{(j-1)T + t} r_t^{(j)} \right] \right]$$

其中目标分布 $p(g|M)$ 由上述课程生成系统动态决定。预训练完成后，仅 Pre-trained Policy π 被保留和部署，其余模块均为训练辅助组件。

### 需要人工验证的设计点

目标映射函数 $f$（如 $f_\text{counts}$ 或 $f_\text{grid}$）需针对环境手动设计，这限制了方法在不同领域间的直接迁移。论文在 MiniGrid 实验中对比了两种映射函数的效果差异，但未提供自动学习 $f$ 的机制。



ULEE 的核心架构围绕一个**无条件上下文自适应策略**展开，通过自我生成的目标课程进行预训练。整个系统由四个关键模块协同工作：预训练策略、目标搜索策略、难度预测器及目标选择机制。

### 预训练策略 π

与传统的目标条件策略不同，ULEE 预训练一个**无条件策略**，该策略采用黑箱元学习方法（Duan et al., 2016; Wang et al., 2016），仅基于完整的交互历史选择动作，无需显式目标编码输入。策略在多个连续回合（称为一个"生命周期"）中与环境交互，其优化目标为最大化终身期望折扣收益：

$$
\mathcal{I}(\pi) = \mathbb{E}_{M \sim \mu^{\mathrm{msup}},\, g \sim p(g|M)} \left[ \mathbb{E}_{\rho_M, P_M, \pi} \left[ \sum_{j=1}^{H} \sum_{t=0}^{T-1} \gamma^{(j-1)T + t} r_t^{(j)} \right] \right]
$$

其中 $M$ 为从无监督任务分布 $\mu^{\mathrm{msup}}$ 采样的环境，$g$ 为从动态目标分布 $p(g|M)$ 采样的目标，$H$ 为生命周期包含的总回合数，$T$ 为每回合步数。该公式使策略学会在多个回合的交互中逐步适应目标任务——这正是 ULEE 区别于仅关注单回合即时表现的方法的核心机制。

### 目标难度定义

ULEE 的关键创新在于引入**基于适应后表现的难度指标**，而非传统的即时成功率。对于目标 $g$、策略 $\pi$ 和环境 $M$，难度定义为后 $K$ 个回合期望成功率的补数：

$$
d(g; \pi, M) = 1 - \mathbb{E}_{\rho_M, P_M, \pi} \left[ \frac{1}{K} \sum_{j=H-K+1}^{H} \mathbf{1}\{\exists t \in \{0,\dots,T-1\} : f(s_{t+1}^{(j)}) = g\} \right]
$$

这里 $f$ 为目标映射函数（如 $f_\text{counts}$ 或 $f_\text{grid}$），将状态映射到目标空间。该定义忽略前 $H-K$ 个适应回合，仅衡量策略经过充分适应后的表现。消融实验证实，基于适应后表现的课程在更高难度基准上优势愈发显著，而基于即时表现的课程则倾向于生成过于简单的目标。

### 对抗目标搜索策略 π_gs

为生成处于智能体能力前沿的目标，ULEE 引入一个**对抗训练的目标搜索策略** $\pi_{gs}$。该策略以目标难度作为奖励进行训练：

$$
r_t^{gs} = r^{gs}(s_t; \pi, M) = d(f(s_t); \pi, M)
$$

即搜索策略在时刻 $t$ 获得的奖励等于当前状态对应目标的难度。通过最大化该奖励，$\pi_{gs}$ 被驱动去发现 $\pi$ 难以完成的目标候选。实际实现中，搜索策略使用难度预测器的估计值 $\hat{d}_\phi(f(s_t), \xi_{M_i})$ 作为奖励信号，避免额外环境交互。

### 边界目标采样

从搜索策略收集的候选目标集 $GC_M$ 中，ULEE 并非均匀采样，而是在难度区间 $[LB, UB]$ 内进行均匀采样：

$$
g_M \sim \operatorname{Unif}(S), \quad S = \{g \in GC_M : LB \leq d(g; \pi, M) \leq UB\}
$$

这一机制确保训练目标保持在中等难度——既不过于简单（无法提供学习信号），也不过于困难（策略无法取得进展）。消融实验表明，当目标搜索为随机时，边界采样尤为有效。

### 难度预测器

直接通过运行策略多个回合来估计目标难度成本高昂。ULEE 引入一个**难度预测器网络** $\hat{d}_\phi$，从近期目标缓冲区 $B_g$ 中学习：

$$
\mathcal{L}_{\mathrm{DP}}(\phi) = \frac{1}{|B_g|} \sum_{(g,\xi,\tilde{d}) \in B_g} \big( \hat{d}_\phi(g,\xi) - \tilde{d}(g) \big)^2
$$

其中 $B_g$ 保存三元组 $(g, \xi, \tilde{d})$，$\xi$ 为环境上下文，$\tilde{d}$ 为经验难度估计。缓冲区仅保留最近训练过的目标，确保预测器与策略当前能力保持同步。该模块使系统能够高效评估大量候选目标的难度，支撑目标搜索与选择的高效运行。



## 实验与关键发现

### 核心瓶颈与实验设计逻辑

ULEE 的设计动机源于一个关键瓶颈：现有无监督探索预训练方法仅依赖即时表现衡量目标难度，缺少对任务特定适应的考量，导致习得的策略难以在分布外或未知目标上泛化。因此，实验围绕三个核心问题展开：(1) 预训练策略的纯探索能力如何？(2) 策略在有限经验下的适应能力如何？(3) 预训练策略是否为长期微调或元学习提供了更强的初始化？

实验在 XLand-MiniGrid 派生的三个基准上进行：4Rooms-Trivial、4Rooms-Small 和 6Rooms-Small（见 Figure 1），任务空间包含 13 种目标类型和 10 种规则类型。所有方法使用相同的 PPO 超参数与网络容量（见 Table 2），ULEE 的预训练步数中来自目标搜索策略的部分（约增加 25% 步数）已在报告中排除以保证比较公平。

![[assets/figures/papers/iclr26_0010_UmxTIxHWkl_Unsupervised_Learning_of_Efficient_Exploration_P/figures/004_Figure_1.jpg]]
*Figure 1: Panel (a), reproduced from Nikulin et al. (2024) (CC BY 4.0), shows a goal and the rules that must be triggered to achieve $\mathrm { i t }$ , represented as a tree of depth 2. Analogously, tasks from the trivial and small benchmarks correspond to depth-0 and depth-1 trees. Panels (b)-(d) show example environments from the three benchmarks: 4Rooms-Trivial, 4Rooms-Small, and 6Rooms-Small*

### 探索评估

Figure 2 展示了不同探索预算下 μ_eval 中目标的达成百分比。ULEE 的预训练策略在所有基准上均显著优于随机策略和 DIAYN 预训练：在 20 回合标记处，ULEE 达成的目标数量超过 DIAYN 的两倍。这一优势源于 ULEE 的无条件上下文自适应架构——策略无需显式目标编码输入，仅通过历史交互序列即可推断当前任务目标并执行有效探索。

![[assets/figures/papers/iclr26_0010_UmxTIxHWkl_Unsupervised_Learning_of_Efficient_Exploration_P/figures/008_Figure_2.jpg]]
*Figure 2: DIAYN Random ULEE (random+bounded) ULEE (random+uniform) ULEE (adversarial+uniform) ULEE (SED) ULEE Figure 2: Percentage of $\mu ^ { \mathrm { { e v a l } } }$ goals reached under different exploration budgets. A goal is considered reached at episode j if it was achieved in any episode ≤ j. Results are averaged across 4 seeds, with individual seeds overlaid as faint thin lines

值得注意的是，DIAYN 预训练策略在探索阶段的表现接近随机策略。这是因为 DIAYN 学到的技能判别器需要在下游任务中作为奖励信号进行条件微调，其预训练阶段并未针对零样本探索进行优化。相比之下，ULEE 的预训练目标直接对齐于终身探索收益（Equation 1），使策略在无任何微调的情况下即可展现结构化探索行为。

### 少样本适应评估

Figure 3a 展示了策略在任务特定适应过程中的收益变化。ULEE 的预训练策略能够有效利用交互历史持续改进：到第 30 回合时，平均收益提升至多 3 倍（在 4Rooms-Small 上从约 0.2 提升至约 0.6）。这一适应能力来源于预训练阶段通过上下文元学习习得的探索与适应行为——策略学会在多个回合的交互中推断目标并调整行为，而非依赖固定的目标条件输入。

![[assets/figures/papers/iclr26_0010_UmxTIxHWkl_Unsupervised_Learning_of_Efficient_Exploration_P/figures/021_Figure_3.jpg]]
*Figure 3: Evaluations on $\mu ^ { \mathrm { { e v a l } } }$ tasks: (a) performance across episodes during task-specific adaptation, (b) few-shot performance by task percentile, (c) few-shot performance as pre-training on $\mu ^ { \mathrm { u n s u p } }$ progresses. ULEE pre-training improves over baselines and ablations across all views. The legend in (c) applies to all panels. Reported steps for ULEE variants in (c) omit those from the Goal-search Policy, which adds 25%. Results are averaged over 4 seeds, with shaded regions indicating standard deviation

Figure 3b 按任务分位数展示了少样本适应后的表现。ULEE 在所有分位数上均优于基线，但在最困难的分布外任务上（6Rooms-Small 的前 60% 任务），预训练策略仍未获得任何收益。这表明 ULEE 的适应能力存在上限：当任务复杂度远超预训练分布时，策略的上下文推断能力不足以弥合差距。

Figure 3c 追踪了预训练进行过程中少样本表现的变化。ULEE 的性能随预训练步数增加而持续提升，而 DIAYN 预训练的性能则停滞甚至下降。这一对比揭示了基于适应后表现的课程设计的关键作用：DIAYN 的互信息最大化目标可能使策略陷入简单技能的局部最优，而 ULEE 的难度预测器（Equation 5）和对抗目标搜索（Equation 3）持续将训练目标推向能力前沿。

### 长期微调与监督元学习

Figure 4 展示了在固定 μ_eval 任务上进行长期微调的结果。ULEE 初始化在所有微调预算下（直至 10^9 步）始终优于从头训练和 DIAYN 预训练后微调，且优势在平均收益、第 40 百分位和第 20 百分位收益上均保持一致。这表明 ULEE 预训练不仅提供了更好的初始策略，还使策略处于更有利于后续优化的参数空间区域。

![[assets/figures/papers/iclr26_0010_UmxTIxHWkl_Unsupervised_Learning_of_Efficient_Exploration_P/figures/024_Figure_4.jpg]]
*Figure 4: Mean, 40th, and 20th percentile returns on a fixed set of $\mu ^ { \mathrm { { e v a l } } }$ tasks as learning on them progresses. Results are averaged over 4 seeds, with shaded regions indicating standard deviation

Figure 5 展示了在 μ_train 上进行监督元学习过程中 μ_eval 上的收益变化。ULEE 初始化在所有百分位收益上均优于从零开始的 RL^2 元学习。使用 f_counts 作为目标映射的版本在早期优势明显，但到 50 亿步时与 f_grid 版本的差异变得可忽略。这一结果表明，ULEE 预训练习得的探索与适应行为可作为监督元学习的有效起点，且对目标表示的选择具有一定鲁棒性。

![[assets/figures/papers/iclr26_0010_UmxTIxHWkl_Unsupervised_Learning_of_Efficient_Exploration_P/figures/028_Figure_5.jpg]]
*Figure 5: Mean, 40th, and 20th percentile returns on $\mu ^ { \mathrm { { e v a l } } }$ tasks as meta-learning on $\mu ^ { \mathrm { t r a i n } }$ progresses. Results are averaged over 4 seeds, with shaded regions indicating standard deviation

### MiniGrid 零样本泛化

Table 1 展示了预训练于 4Rooms-Small 后在 14 个 MiniGrid 任务上 20 适应回合的平均收益。ULEE 在 7 个任务上取得最优结果，尤其在 BlockedUnlockPickUp（0.43）、Unlock（0.47）和 UnlockPickUp（0.40）等操控任务上明显超越 DIAYN。这些任务需要序列化的物体交互，与预训练环境中的规则触发结构相似，验证了 ULEE 习得的探索行为具有跨任务迁移能力。

![[assets/figures/papers/iclr26_0010_UmxTIxHWkl_Unsupervised_Learning_of_Efficient_Exploration_P/figures/029_Table_1.jpg]]
*Table 1: Mean return on MiniGrid tasks. ULEE and DIAYN methods were pre-trained on 4Rooms-Small and their performance is evaluated after 20 adaptation episodes. Results are averaged over 4 seeds, with standard deviations reported. The best-performing method is highlighted in bold*

然而，在 LockedRoom 等需要特定钥匙-门匹配的任务上，所有方法的表现均接近零。这一失败模式揭示了当前方法的局限：目标映射函数 f（如 f_counts 或 f_grid）需针对环境手动设计，无法自动捕获任务间的细粒度语义差异。

### 消融实验

消融实验（Section 4.3.1）揭示了两个关键设计选择的因果作用：

**对抗目标搜索 vs. 随机搜索**：使用对抗训练的 Goal-search Policy 的变体在所有基准上取得最佳结果。当目标搜索退化为随机采样时，性能显著下降。这是因为随机搜索无法系统性地发现处于能力前沿的困难目标，导致课程中充斥过于简单或过于困难的目标。

**边界采样与基于适应后表现的课程**：在目标搜索为随机的情况下，边界采样（在 [LB, UB] 区间内均匀采样，Equation 4）尤为有效，因为它至少能过滤掉极端难度的目标。更重要的是，基于适应后表现（后 K 个回合的成功率，Equation 2）的课程相比基于即时表现的课程，在更高难度基准上优势更加明显。这验证了核心设计假设：衡量目标难度时，必须考虑策略的适应潜力，而非仅看首次尝试的表现。

### 失败模式与局限

1. **分布外困难任务上的零收益**：在 6Rooms-Small 的前 60% 任务上，ULEE 预训练策略在少样本适应后仍未获得任何收益。这暴露出上下文元学习的泛化边界——当任务结构与预训练分布差异过大时，策略的历史推断机制失效。

2. **目标映射函数的手动设计需求**：f_counts 和 f_grid 需要针对环境手动定义，这限制了方法在视觉复杂或连续控制环境中的直接应用。尽管 f_counts 版本在部分任务上表现更好，但其设计依赖于对任务空间的先验知识。

3. **缺少层次化结构**：当前策略在单层上下文中进行适应，面对更长时序或更复杂指令的任务时可能表现不足。论文明确指出，引入层次化结构是未来工作的重要方向。

4. **单一环境域验证**：所有实验在网格世界环境中进行，尚未在连续控制或视觉复杂环境中验证框架的有效性。这留下了开放问题：难度预测器和对抗目标搜索在高维状态空间中是否同样稳定？



## 定位与知识库关联

### 与基线方法的关系

ULEE 的核心设计建立在对现有无监督探索预训练范式的两个关键诊断之上：其一，仅依赖即时表现衡量目标难度会导致课程退化，无法为智能体提供合适的泛化压力；其二，目标条件策略在下游需要额外的适应机制才能处理分布外目标。基于此，ULEE 在以下维度上区别于基线方法。

**相对于 DIAYN（无监督技能发现）**：DIAYN 通过最大化技能-状态互信息学到一组可区分的技能，下游利用技能 discriminator 的输出作为奖励进行条件策略微调。这一范式的瓶颈在于：技能发现阶段的难度信号完全来自即时判别能力，忽略了任务特定的适应过程。ULEE 则以适应后表现作为难度度量（公式 $d(g; \pi, M)$ 取后 $K$ 个回合的期望成功率补数），并采用无条件上下文自适应策略，使预训练目标直接对齐于下游的适应过程。实验证据表明，这一差异在探索评估中转化为显著差距——ULEE 在 20 回合时达到 DIAYN 两倍以上的目标达成率（Figure 2），且在少样本适应中实现至多 3 倍的收益提升（Figure 3a）。

**相对于 PPO（从零训练）和 RND（好奇心驱动探索）**：PPO 从零训练缺乏任何预训练先验，RND 虽提供内在激励但未构建目标导向的课程。ULEE 的预训练策略在长期微调中始终优于这两者，且在高达 $10^9$ 步的微调预算下保持优势（Figure 4），表明预训练习得的探索与适应行为具有持久的迁移价值。

**相对于 RL²（监督元学习从零开始）**：RL² 同样采用黑盒上下文元学习，但完全依赖任务特定的监督奖励进行训练。ULEE 的无监督预训练为后续监督元学习提供了更强的初始化，在 $\mu^{\mathrm{train}}$ 上元学习过程中，$\mu^{\mathrm{eval}}$ 上的各分位数收益均高于从零开始的 RL²（Figure 5）。这说明自我生成的目标课程能够有效替代监督信号，预训练出可迁移的元探索能力。

### 适用边界与泛化能力

ULEE 在网格世界任务上展现出跨任务泛化能力：预训练于 4Rooms-Small 后，在 MiniGrid 的 14 个任务中，有 7 个任务在 20 适应回合后取得最优性能（Table 1），尤其在 BlockedUnlockPickUp、Unlock、UnlockPickUp 等需要序列操控的任务上明显超越 DIAYN 和随机策略。这表明预训练策略习得了结构化的探索与工具使用行为，而非简单的环境记忆。

然而，适用边界同样清晰。在最困难的分布外任务上（如 6Rooms-Small 的前 60% 任务），预训练策略仍未获得任何收益（Figure 3b），说明当目标复杂度远超预训练分布时，适应能力有限。此外，目标映射函数 $f$（如 $f_{\mathrm{counts}}$ 或 $f_{\mathrm{grid}}$）需针对环境手动设计，这构成方法向新领域迁移的关键约束——在视觉复杂或连续控制环境中，如何自动构建有意义的目标空间仍是开放问题。

### 局限与开放问题

**结构层面**：当前策略采用扁平的黑盒元学习架构，未引入层次化结构。面对更长时序或需要多级子目标规划的任务时，单一序列模型可能难以有效分解和协调子任务。论文明确指出，引入层次化结构是未来的重要方向。

**目标空间设计**：目标映射函数 $f$ 的手动设计限制了方法的普适性。一个互补方向是将视觉-语言模型集成到目标提议或奖励定义中，使预训练更贴近人类相关任务，并提升向真实场景的迁移潜力。

**课程机制**：论文在附录中提出了适应后学习进度指标 $LP_{\mathrm{post}}$（Appendix A.3），衡量适应后表现的变化量，但未将其纳入主课程。该指标与适应后难度课程结合后能否进一步提升课程质量，尚待验证。

**环境验证**：所有实验均在单一的网格世界环境（XLand-MiniGrid 变体）中进行，尚未在高维视觉输入和连续动作空间中验证框架的有效性。这一局限性需要在未来的工作中通过更广泛的环境测试来弥合。



## 原文 PDF

![[paperPDFs/ICLR_2026/Unsupervised_Learning_of_Efficient_Exploration_Pre_training_Adaptive_Policies_via_Self_Imposed_Goals.pdf]]
