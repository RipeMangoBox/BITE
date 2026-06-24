---
title: "Incentivizing LLM Reasoning via Reinforcement Learning with Functional Monte Carlo Tree Search"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Incentivizing_LLM_Reasoning_via_Reinforcement_Learning_with_Functional_Monte_Carlo_Tree_Search.pdf
openreview_forum_id: lHbhzxiVI9
aliases:
- RRFTT
- ILRRLFMCTS
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "可学习的功能标记与功能树搜索相结合：将功能标记嵌入模型词汇表，使模型能够内化多种人类推理行为（如分析、验证、修正），并在训练中通过标记引导的MCTS实现多样化探索与高效自改进。"
primary_logic: "通过MCTS生成含功能标记的结构化推理数据，为模型提供初始推理能力；随后在强化学习中，模型直接采样功能标记自主构建推理树，利用UCT平衡探索与利用，同时引入过程奖励和KL约束，从而在不依赖外部提示的条件下实现复杂推理路径的探索与强化。"
claims:
- "RFTT通过功能标记引导的MCTS，将推理过程转化为树搜索，大幅提升小模型的数学推理性能，平均超越ReFT 5个百分点。"
- "功能标记消融实验表明，每个标记都有贡献，其中<verify>和<refine>对性能影响最大，缺失时准确率下降约7个百分点。"
- "强化学习中引入功能树搜索比随机采样平均提高1.5%，且结合PRM后进一步带来约2%的提升。"
- "MATH-500 上 Pass@1 准确率 = 79.8"
---

# Incentivizing LLM Reasoning via Reinforcement Learning with Functional Monte Carlo Tree Search

> [!tip] 核心洞察
> 通过MCTS生成含功能标记的结构化推理数据，为模型提供初始推理能力；随后在强化学习中，模型直接采样功能标记自主构建推理树，利用UCT平衡探索与利用，同时引入过程奖励和KL约束，从而在不依赖外部提示的条件下实现复杂推理路径的探索与强化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于函数蒙特卡洛树搜索的强化学习激励大语言模型推理 |
| 英文题名 | Incentivizing LLM Reasoning via Reinforcement Learning with Functional Monte Carlo Tree Search |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=lHbhzxiVI9); [GitHub](https://github.com/sastpg/RFTT) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | RFTT (Reinforced Functional Token Tuning) |
| Dataset | MATH-500, GSM8K |

> [!tip] 效果简介
> - MATH-500 上，Pass@1 准确率 为 79.8，对比 72.0 (Zero-shot CoT)，变化 +7.8。
> - GSM8K 上，Pass@1 准确率 为 95.2，对比 91.1 (Zero-shot CoT)，变化 +4.1。
> - MATH-500 上，Pass@1 准确率 为 60.2，对比 50.6 (Zero-shot CoT)，变化 +9.6。

## 概述

### 问题瓶颈

纯强化学习（RL）在小型语言模型上训练时，面临双重困境：一方面，小模型缺乏足够的初始推理能力，难以在RL早期产生有效的探索行为；另一方面，直接采用词汇级树搜索（token-level tree search）会因动作空间过大而导致探索效率极低。这两者共同作用，使模型容易收敛到次优的推理模式，无法充分挖掘RL在复杂推理任务上的潜力。

### 核心思路

RFTT（Reinforced Functional Token Tuning）的核心洞察是：**将人类推理行为抽象为可学习的功能标记（functional tokens），嵌入模型词汇表，使模型能够内化“分析→验证→修正”等结构化推理行为**。在训练中，通过功能标记引导的蒙特卡洛树搜索（MCTS）实现多样化探索与高效自改进，从而在不依赖外部提示的条件下，让小模型自主构建并强化复杂推理路径。

### 方法定位

RFTT属于**树搜索增强的强化微调**方法，与现有工作的关键区别在于：

| 维度 | 现有方法 | RFTT |
|------|---------|------|
| 推理引导机制 | 外部提示引导（prompt-guided） | 内部功能标记引导（token-guided） |
| 探索策略 | 随机采样或固定提示 | 功能标记引导的MCTS树搜索 |
| 动作空间 | 词汇级标记采样 | 人类推理行为动作空间（分析、验证、修正等） |

在方法谱系上，RFTT与以下工作形成对比：
- **ReFT**（Trung et al., 2024）：监督微调基线，缺乏RL的探索能力
- **GRPO**（Shao et al., 2024）：RL基线，但未引入树搜索结构
- **MCTS-DPO**（Xie et al., 2024）：偏好优化基线，依赖外部偏好信号
- **TreeRL**（Hou et al., 2025）：树搜索RL，但未使用功能标记
- **rStar**（Qi et al., 2024）、**LLaMA-Berry**（Zhang et al., 2024c）、**ResT-MCTS\***（Zhang et al., 2024a）：推理时树搜索方法，但未将树搜索内化到训练过程中

### 主要结果

在数学推理基准上，RFTT在所有测试的小模型上均取得显著提升：

- **Qwen-2.5-7B-Instruct**：MATH-500准确率从72.0%提升至79.8%（+7.8），GSM8K从91.1%提升至95.2%（+4.1）
- **LLaMA-3.1-8B-Instruct**：MATH-500准确率从50.6%提升至60.2%（+9.6），平均超越ReFT约5个百分点

消融实验表明：
- 功能标记中`<verify>`和`<refine>`对性能影响最大，缺失时准确率下降约7个百分点
- RL中引入功能树搜索比随机采样平均提高1.5%，结合过程奖励模型（PRM）后进一步带来约2%的提升
- 移除SFT预热阶段导致性能下降2.9%–7.7%，验证了初始推理能力对RL探索的关键作用

此外，尽管仅使用数学数据训练，RFTT在MMLU-Pro、GPQA等部分通用基准上展现出跨领域迁移能力。推理时增加搜索rollouts数量可进一步提升性能，表明该方法具有良好的推理时计算扩展性。

> **注意**：当前工作主要聚焦于数学推理领域，在其他复杂领域（如法律、医学诊断）的有效性尚需更多验证。增强的推理能力并不消除LLM固有的偏见、过度自信或生成错误但令人信服的输出等问题。

## 背景与动机

### 大语言模型推理能力提升的范式演进

大语言模型（LLM）在数学推理等复杂任务上的表现，近年来经历了从提示工程到训练干预的范式转变。早期工作依赖链式思考（Chain-of-Thought, CoT）提示，通过外部引导激发模型的逐步推理能力。然而，这类方法本质上受限于模型固有的推理边界——提示只能“唤醒”已有能力，无法从根本上拓展模型的推理深度。

随后的研究转向训练层面的改进。监督微调（SFT）方法利用高质量推理数据训练模型，但其效果高度依赖数据覆盖度，且容易导致模型记忆特定推理模式而非习得通用推理能力。强化学习（RL）方法，如基于结果奖励的ReFT（Trung et al., 2024）和GRPO（Shao et al., 2024），通过奖励信号激励模型探索更优推理路径，在小模型上展现出一定潜力。

### 纯强化学习在小模型上的瓶颈

尽管RL方法取得进展，一个关键瓶颈仍然存在：**小模型缺乏足够的初始推理能力和探索多样性**。当模型本身不具备可靠的推理起点时，RL的探索过程容易收敛到次优推理模式——模型在有限的动作空间内反复尝试，无法跳出局部最优。这一问题的根源在于：

1. **初始推理能力不足**：小模型在未经引导时，难以自发产生结构化的、多分支的推理过程。
2. **探索效率低下**：传统的随机采样或固定提示策略，无法系统性地覆盖复杂推理问题的解空间。
3. **动作空间粒度过细**：直接以词汇级标记（token）为单位进行树搜索，面临动作空间过大、搜索效率极低的问题。

### 树搜索方法的引入与局限

为提升推理探索的系统性，研究者开始将蒙特卡洛树搜索（MCTS）引入LLM推理。MCTS-DPO（Xie et al., 2024）将树搜索与偏好优化结合，TreeRL（Hou et al., 2025）探索树搜索强化学习，ResT-MCTS*（Zhang et al., 2024a）、rStar（Qi et al., 2024）和LLaMA-Berry（Zhang et al., 2024c）等方法则在推理阶段使用树搜索增强模型输出。

然而，这些方法存在一个共同局限：**推理过程始终依赖外部提示引导**。模型本身并未内化树搜索的推理模式，每次推理仍需精心设计的提示模板来触发特定推理行为（如“让我们验证一下”、“请修正错误”等）。这种外部依赖不仅限制了推理的灵活性，也使得训练阶段和推理阶段的行为模式不一致——训练时模型学习模仿提示引导的推理，推理时却需要相同的提示才能复现类似行为。

### 本文的核心动机

针对上述问题，本文提出**将人类推理行为内化为模型的内在能力**，使小模型能够在无需外部提示的条件下，自主进行结构化的树搜索推理。具体而言，需要解决三个核心问题：

1. **如何让模型“学会”多种推理行为**（如分析、验证、修正），而非依赖提示触发？
2. **如何在训练中实现高效、多样化的推理探索**，避免收敛到次优模式？
3. **如何在推理阶段将探索能力转化为性能增益**，使模型能自主扩展推理树？

这些问题的解决，需要在模型架构、训练策略和搜索机制三个层面进行协同设计。本文提出的RFTT方法，通过将功能标记（functional tokens）嵌入模型词汇表，并构建功能标记引导的MCTS训练框架，为上述问题提供了一个统一的解决方案。

## 核心创新

RFTT（Reinforced Functional Token Tuning）的核心创新在于将**可学习的功能标记（functional tokens）** 与**蒙特卡洛树搜索（MCTS）** 深度耦合，构建了一个从“外部提示引导”到“内部标记驱动”的推理能力内化机制。其关键设计围绕三个 changed slots 展开：

### 从外部提示引导到内部功能标记引导

现有推理增强方法（如 ReFT, Trung et al., 2024）依赖外部提示（prompts）来触发模型的逐步推理行为，这本质上是一种脆弱的、依赖上下文窗口的浅层引导。RFTT 将一系列模拟人类推理行为的功能标记——`<analysis>`、`<subquestion>`、`<next_step>`、`<direct_answer>`、`<verify>`、`<refine>`、`<output>`——直接嵌入模型的词汇表中，使其成为模型可自主采样的内部动作。这一转变的因果机制在于：功能标记不再是消耗上下文窗口的外部指令，而是模型策略空间中的原生动作，使模型能够在推理时“自主决定”何时分析、何时验证、何时修正，从而建立起**内部化的标记引导推理模式**（internalized token-guided reasoning patterns）。

### 从随机采样到功能标记引导的 MCTS 树搜索

纯强化学习方法（如 GRPO, Shao et al., 2024）在在线探索阶段通常采用随机采样或固定提示策略，这在小模型上容易因探索多样性不足而收敛到次优推理模式。RFTT 将推理过程形式化为一个树搜索问题，以功能标记作为动作空间，利用 **UCT（Upper Confidence Bound for Trees）** 平衡探索与利用：

$$a_t = \begin{cases} \arg\max_{a \in U(s_t)} \pi_\theta(a|s_{0:t}), & U(s_t) \neq \emptyset \\ \arg\max_{a \in A(s_t)} \mathrm{UCT}(s_t, a), & \text{otherwise} \end{cases}$$

其中 UCT 分数为：

$$\mathrm{UCT}(s_t, a) = \frac{Q(s_t, a)}{N(s_t, a)} + c \cdot \sqrt{\frac{\ln N(s_t)}{N(s_t, a)}}$$

这一设计的核心优势在于：**动作空间被压缩为有限的人类推理行为类别**，而非词汇级别的海量 token 采样空间，从而大幅提升了树搜索的探索效率。消融实验证实，在 RL 采样中使用功能标记引导的 MCTS 比随机采样平均提升 **1.5%**（Table 6）。

### 两阶段训练：SFT 预热 + RL 自改进

RFTT 的两阶段训练框架解决了“冷启动”问题——纯强化学习在小模型上缺乏初始推理能力。第一阶段通过**交叉验证与分支合并**（Cross Verification and Branch Merging）构建结构化 SFT 数据：在正确轨迹 $\tau_c$ 与错误轨迹 $\tau_w$ 的分叉点注入验证节点，生成包含自我验证和自我修正的完整推理路径 $\tau_f = \tau^+ \cup \bar{\tau_w^-} \cup \{s_v\} \cup \tau_c^+$。模型在此阶段学会使用功能标记进行推理。第二阶段，模型直接采样功能标记自主扩展推理树，结合过程奖励模型（PRM）提供中间步骤的细粒度奖励信号，并通过 KL 散度约束防止策略偏离参考模型：

$$R_t(s_{0:t}, a_t, s_{t+1}) = \mathtt{RM}(s_{0:t}, a_t, s_{t+1}) - \beta \cdot \mathtt{KL}(t)$$

消融实验表明，移除 SFT 预热导致 Qwen-2.5-7B-Instruct 平均性能下降 **2.9%**，LLaMA-3.1-8B-Instruct 下降 **7.7%**；加入 PRM 比仅使用结果奖励平均提升约 **2%**（Table 6）。

### 功能标记的差异化贡献

功能标记消融实验（Table 4）揭示了各标记的非对称重要性：掩蔽 `<verify>` 和 `<refine>` 标记导致准确率下降约 **7 个百分点**（从 79.8% 分别降至 72.8% 和 72.6%），表明自我验证与自我修正能力是 RFTT 性能增益的主要来源，而其他标记（如 `<analysis>`、`<subquestion>`）的贡献相对温和。这一发现暗示，**推理能力的提升并非均匀地来自所有推理行为，而是集中在纠正性元认知行为上**。

## 整体框架

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/001_Figure_1.jpg]]
*Figure 1: A conceptual illustration of reasoning path generation based on functional tree search and our training framework. RFTT comprises two phases: supervised fine-tuning warmups the model with initial reasoning capability by functional token-annotated data, while online reinforcement learning allows the model to directly sample functional tokens from its vocabulary to autonomously expand reasoning trees for diverse exploration*

RFTT（Reinforced Functional Token Tuning）是一个两阶段训练框架，旨在让小模型通过功能标记引导的树搜索，内化复杂推理行为（如分析、验证、修正），从而在不依赖外部提示的条件下实现多样化的推理探索与强化。其核心瓶颈在于：纯强化学习在小模型上缺乏足够的初始推理能力与探索多样性，容易收敛到次优推理模式；同时，直接采用词汇级树搜索面临动作空间过大、探索效率低下的问题。RFTT通过将人类推理行为抽象为可学习的功能标记，并将这些标记嵌入模型词汇表，使模型能够自主构建和搜索推理树，从而系统性地解决上述问题。

### 训练流程

RFTT的训练分为两个阶段，如图1所示：

1. **监督微调预热阶段（SFT Warmup）**：利用功能提示（functional prompts）引导的MCTS，在数学问题集上生成结构化的推理树。通过交叉验证与分支合并机制，将正确轨迹与错误轨迹融合，构造含有自我验证和自我修正步骤的推理路径数据。这些数据被用于对基座模型进行SFT，使模型初步学会使用功能标记进行推理，为后续强化学习提供初始推理能力。

2. **在线强化学习阶段（Online RL）**：模型不再依赖外部提示，而是直接从自身词汇表中采样功能标记，自主扩展推理节点，构建功能标记引导的MCTS推理树。在搜索过程中，利用UCT（Upper Confidence Bound for Trees）分数平衡探索与利用，同时引入过程奖励模型（PRM）和KL散度约束来指导策略更新。策略优化采用Reinforce++算法（即带裁剪的PPO式目标），使模型在稳定更新的同时持续提升推理能力。

### 核心模块与数据流

整个框架由以下关键模块串联：

- **功能标记动作空间**：定义了七种人类推理行为作为树搜索的动作空间——`<analysis>`（分析）、`<subquestion>`（子问题分解）、`<next_step>`（下一步推理）、`<direct_answer>`（直接回答）、`<verify>`（验证）、`<refine>`（修正）和`<output>`（输出）。这些标记在SFT阶段以提示形式引导模型，在RL阶段则被嵌入模型词汇表，成为模型可自主调用的内部推理原语。

- **交叉验证与分支合并（SFT数据构建）**：对于每个问题，先用功能提示引导的MCTS生成多条推理轨迹。从正确轨迹集合$\mathcal{T}_c$中选择平均过程奖励最高的轨迹$\tau_c$，从与之有共同前缀的错误轨迹集合$\mathcal{T}_w$中选择平均奖励最低的轨迹$\tau_w$。然后，在分叉节点处生成验证步骤$s_v$，解释错误原因，最终合并为一条包含自我验证和自我修正的完整推理路径$\tau_f = \tau^+ \cup \bar{\tau_w^-} \cup \{s_v\} \cup \tau_c^+$（见图2）。该模块解决了纯RL初期模型缺乏自我纠错能力的问题。

- **功能标记引导的MCTS（RL阶段）**：在RL的每次前向推理中，模型从当前状态$s_t$出发，按以下策略选择动作$a_t$（即功能标记）：若存在未被探索的动作$U(s_t)$，则按模型对数似然$\pi_\theta(a|s_{0:t})$采样；否则按UCT分数$\mathrm{UCT}(s_t, a) = \frac{Q(s_t, a)}{N(s_t, a)} + c \cdot \sqrt{\frac{\ln N(s_t)}{N(s_t, a)}}$选择。该模块将词汇级采样的问题转化为在有限的人类推理行为空间中进行树搜索，大幅降低了探索难度。

- **过程奖励与KL约束**：每一步的即时奖励定义为$R_t = \mathtt{RM}(s_{0:t}, a_t, s_{t+1}) - \beta \cdot \mathtt{KL}(t)$。其中结果奖励$\mathtt{RM}$根据最终答案的正确性给出：正确为1，错误为0.1，若推理未完成则返回过程奖励模型给出的中间分数$\sigma$。KL惩罚项约束策略不偏离参考模型过远，防止训练不稳定。

- **策略更新（Reinforce++）**：使用剪切式策略梯度目标$\mathcal{L}_{RL}(\theta) = -\mathbb{E}_t\left[\min\left(\frac{\pi_\theta}{\pi_{\theta_{\mathrm{old}}}}\hat{A}_t, \mathrm{clip}(\frac{\pi_\theta}{\pi_{\theta_{\mathrm{old}}}}, 1-\epsilon, 1+\epsilon)\hat{A}_t\right)\right]$进行参数更新，在保证探索效率的同时维持训练稳定性。

### 关键设计决策

RFTT相较于现有工作的三个核心设计转变在于：

1. **推理引导机制**：从外部提示引导（如ReFT的零样本CoT提示）转变为内部功能标记引导。模型在RL阶段直接从词汇表中采样功能标记来驱动推理树的自主扩展，实现了推理行为的内部化。

2. **探索策略**：从随机采样或固定提示转变为功能标记引导的MCTS树搜索。UCT机制在有限的动作空间内高效平衡探索与利用，使小模型也能发现高质量的推理路径。

3. **动作空间**：从词汇级标记采样（动作空间为整个词表）转变为人类推理行为动作空间（仅7种功能标记）。这一设计从根本上解决了词汇级树搜索动作空间过大、探索效率低下的问题。

### 训练与推理配置

在SFT阶段，使用约1.2k道MATH题目通过64个并发进程进行MCTS搜索，生成约1k条SFT数据；训练batch size为128，学习率为$7\times10^{-6}$，截断长度为8192。在RL阶段，每步训练对16个不同问题各搜索16条推理路径；策略模型学习率为$5\times10^{-7}$，温度为0.95，KL系数为0.01。过程奖励模型采用mathshepherd-mistral-7b-prm。推理时，RFTT可利用MCTS进一步扩展搜索，以推理时计算换取性能提升（见图3），且无需额外奖励模型引导。

## 核心模块与公式推导

### 功能标记动作空间

RFTT 将人类复杂推理行为抽象为可学习的**功能标记**（functional tokens），嵌入模型词汇表，作为树搜索的动作空间。这些标记包括：`<analysis>`（分析，a2）、`<subquestion>`（子问题，a3）、`<next_step>`（下一步，a4）、`<direct_answer>`（直接回答，a5）、`<verify>`（验证，a6）、`<refine>`（修正，a7）和 `<output>`（输出）。在 SFT 预热阶段，使用功能提示引导 MCTS 生成结构化推理树；在 RL 阶段，模型直接从自身词汇表中采样功能标记，自主扩展推理节点。

### 交叉验证与分支合并（SFT 数据构建）

该模块负责生成含自验证和自修正的结构化推理数据。给定问题 $x$，通过功能提示引导的 MCTS 生成正确轨迹集合 $\mathcal{T}_c$ 和错误轨迹集合 $\mathcal{T}_w$。选择策略如下：

- **正确轨迹选择**：选择平均过程奖励最高的正确轨迹：
  $$\tau_c = \arg\max_{\tau_i \in \mathcal{T}_c} \bar{R}(\tau_i)$$

- **错误轨迹选择**：在与正确轨迹存在公共前缀的错误轨迹中，选择平均奖励最低者：
  $$\tau_w = \arg\min_{\tau_i \in \mathcal{T}_w} \bar{R}(\tau_i)$$

随后，在分叉节点处生成验证节点 $s_v$，解释错误原因，并将轨迹合并为最终推理路径：
$$\tau_f = \tau^+ \cup \bar{\tau_w^-} \cup \{s_v\} \cup \tau_c^+$$
其中 $\tau^+$ 为公共前缀，$\bar{\tau_w^-}$ 为错误轨迹的独有步骤，$\tau_c^+$ 为正确轨迹的独有步骤。该合并路径作为 SFT 训练数据，使模型内化功能标记引导的推理模式。

### 功能标记引导的 MCTS（RL 阶段）

在在线 RL 阶段，模型通过功能标记引导的树搜索实现多样化探索。每个推理步骤的动作选择遵循两级策略：

$$a_t = \begin{cases} \arg\max_{a \in U(s_t)} \pi_\theta(a|s_{0:t}), & U(s_t) \neq \emptyset \\ \arg\max_{a \in A(s_t)} \mathrm{UCT}(s_t, a), & \text{otherwise} \end{cases}$$

其中 $U(s_t)$ 为当前状态下未被探索的动作集合，$A(s_t)$ 为全部可用动作。优先按模型对数似然选择未探索动作；当所有动作均被探索后，按 UCT 分数平衡探索与利用：

$$\mathrm{UCT}(s_t, a) = \frac{Q(s_t, a)}{N(s_t, a)} + c \cdot \sqrt{\frac{\ln N(s_t)}{N(s_t, a)}}$$

其中 $Q(s_t, a)$ 为动作 $a$ 的累积奖励，$N(s_t, a)$ 为动作被访问次数，$c$ 为探索系数。

### 奖励函数与 KL 约束

即时奖励由结果/过程奖励减去 KL 散度惩罚构成，防止策略偏离参考模型：

$$R_t(s_{0:t}, a_t, s_{t+1}) = \mathtt{RM}(s_{0:t}, a_t, s_{t+1}) - \beta \cdot \mathtt{KL}(t)$$

其中 $\beta$ 为 KL 系数（设为 0.01），$\mathtt{KL}(t)$ 为当前策略与参考模型在第 $t$ 步的 KL 散度。结果奖励函数为：

$$\mathtt{RM}(s_{0:t}, a_t, s_{t+1}) = \begin{cases} 1, & \mathtt{ANS}(s_{t+1}) = y \\ 0.1, & \mathtt{ANS}(s_{t+1}) \neq \text{null}, \neq y \\ \sigma, & \mathtt{ANS}(s_{t+1}) = \text{null} \end{cases}$$

其中 $\mathtt{ANS}(s_{t+1})$ 为从生成内容中提取的答案，$y$ 为标准答案，$\sigma$ 为过程奖励模型（PRM）给出的中间步骤奖励。答案正确得 1 分，错误得 0.1 分，未完成则返回 PRM 的过程奖励。

### 策略更新（Reinforce++）

使用剪切式 PPO 目标稳定更新策略模型：

$$\mathcal{L}_{RL}(\theta) = -\mathbb{E}_t\left[\min\left(\frac{\pi_\theta(a_t|s_{0:t})}{\pi_{\theta_{\mathrm{old}}}(a_t|s_{0:t})}\hat{A}_t, \mathrm{clip}\left(\frac{\pi_\theta(a_t|s_{0:t})}{\pi_{\theta_{\mathrm{old}}}(a_t|s_{0:t})}, 1-\epsilon, 1+\epsilon\right)\hat{A}_t\right)\right]$$

其中 $\hat{A}_t$ 为优势估计，$\epsilon$ 为剪切范围。该目标通过限制策略更新幅度，在提升推理能力的同时保持训练稳定性。

## 实验与分析

### 主实验结果

RFTT在多个数学推理基准上显著提升了小模型的性能。Table 1展示了三个基础模型在MATH-500、GSM8K、SVAMP、Olympiad Bench和AMC上的Pass@1准确率。以Qwen-2.5-7B-Instruct为例，RFTT在MATH-500上达到79.8%，相比Zero-shot CoT基线（72.0%）提升7.8个百分点；在GSM8K上达到95.2%，提升4.1个百分点。对于LLaMA-3.1-8B-Instruct，MATH-500从50.6%提升至60.2%，增幅达9.6个百分点。与监督微调基线**ReFT**（Trung et al., 2024）相比，RFTT平均领先约5个百分点，表明功能标记引导的树搜索强化学习比单纯的行为克隆更有效。


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/003_Table_1.jpg]]
*Table 1: Accuracy of our proposed RFTT and baselines across different mathematical reasoning benchmarks. The best results in each box are highlighted in bold. The proposed RFTT significantly boosts the performance of smaller LLMs across all datasets*

跨领域泛化实验（Table 2）显示，仅在MATH数据集上训练的RFTT在MMLU-Pro、GPQA、CommonsenseQA、FOLIO、TableBench和CRUXEval等非数学基准上同样取得一致提升。例如Qwen-2.5-7B-Instruct在MMLU-Pro上从52.4%提升至57.2%，在FOLIO上从68.5%提升至73.9%。这表明功能标记内化的推理行为（分析、验证、修正）具有一定的领域迁移能力。


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/004_Table_2.jpg]]
*Table 2: Performance of RFTT on out-of-domain benchmarks. Despite being trained only on math datasets, RFTT exhibits strong transferability*

与其他树搜索方法的对比（Table 3）进一步验证了效率优势：RFTT在GSM8K上以95.2%的准确率和每题81秒的耗时，优于**rStar**（Qi et al., 2024）的92.1%/162秒和**LLaMA-Berry**（Zhang et al., 2024c）的94.9%/128秒；在MATH-500上以72.0%/131秒显著领先于rStar的61.0%/344秒。


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/009_Table_3.jpg]]
*Table 3: Comparison of different tree search methods*

### 消融实验

**功能标记消融**（Table 4）：逐一掩蔽各功能标记的实验表明，所有标记均有正向贡献。其中`<verify>`和`<refine>`的影响最大：掩蔽`<verify>`（a6）后准确率从79.8%降至72.8%，掩蔽`<refine>`（a7）后降至72.6%，降幅约7个百分点。这印证了自我验证与自我修正在复杂推理中的核心作用。

**组件消融**（Table 6）揭示了三个关键设计的作用机制：


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/010_Table_6.jpg]]
*Table 6: Ablation study on different components of RFTT. We additionally perform an analysis using Deepseek-R1 on 1,000 randomly selected questions from MMLU-Pro (a dataset that spans STEM, social sciences, law, and health). The sampled reasoning trajectories are broken down into discrete steps using predefined rules (e.g., newline delimiters). We then employ GPT-4o to assess whether each step could be mapped to one of our functional tokens. As presented in Table 5, approximately 98.4% of the steps aligned with the intended semantic coverage of our token set, which demonstrates the generation of our functional tokens across diverse tasks*


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/011_Table_5.jpg]]

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/012_Table_6.jpg]]

- **SFT预热**：移除SFT阶段直接进行RL训练，Qwen-2.5-7B-Instruct平均性能下降2.9%，LLaMA-3.1-8B-Instruct下降7.7%。这验证了核心瓶颈——小模型缺乏足够的初始推理能力，纯RL难以有效探索。SFT阶段通过MCTS生成的结构化推理数据为模型提供了必要的“冷启动”。

- **MCTS引导采样**：在RL阶段将功能标记引导的MCTS替换为随机采样，平均性能下降1.5%（从73.92%降至72.34%）。MCTS通过UCT分数（公式见方法部分）平衡探索与利用，使模型能更高效地发现高质量推理路径，而非依赖随机扰动。

- **过程奖励模型**：仅使用结果奖励（ORM）而非过程奖励（PRM）时，平均性能下降约2%。PRM为中间推理步骤提供细粒度反馈，有效缓解了长推理链中的误差累积问题。论文使用的PRM为mathshepherd-mistral-7b-prm（Wang et al., 2024b）。

### 推理时计算量扩展

Figure 3展示了推理时增加搜索rollout数量对性能的影响。随着rollout数从1增至20，所有方法（基础模型、SFT、RL+MCTS+ORM、RL+MCTS+PRM）的准确率均持续提升，但RFTT（RL+MCTS+PRM）的增益最为显著，在Qwen-2.5-7B-Instruct上最终达到约88%，接近o1-preview的水平。这一结果表明，功能标记内化的树搜索能力使模型在推理时能够有效利用额外计算资源进行更深度的探索。


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/008_Figure_3.jpg]]
*Figure 3: Performance gains under scaling up the inference-time computation*

### 训练动态

Figure 5展示了RL阶段的训练曲线。随着训练推进，模型在MATH-500上的准确率稳步上升，同时KL散度保持在可控范围内，表明KL约束（系数0.01）有效防止了策略偏离参考模型过远。训练中每步对16个不同问题各搜索16条推理路径，在探索多样性与计算效率之间取得了平衡。

### 失败模式与局限性

尽管RFTT取得了显著性能提升，仍需注意以下局限：

1. **数学领域过度优化风险**：训练数据仅来自MATH数据集，虽然在部分通用基准上展示了迁移能力，但在法律、医学诊断等更广泛推理领域的有效性尚需验证。

2. **固有偏见未消除**：增强的推理能力并不消除LLM固有的偏见、过度自信或生成看似合理但错误的输出。功能标记引导的自我验证机制可能产生“自信的错误”。

3. **安全风险**：功能标记作为特殊控制标记，可能被用于标记注入攻击以操纵模型行为，这是实际部署中需要防御的威胁向量。

4. **训练稳定性**：基于自我改进的RL循环可能导致能力意外放大或训练不稳定，需要持续监控奖励破解行为。

### 计算成本

Table 7对比了不同方法的计算开销。RFTT的SFT数据构建阶段使用64个并发进程对1200个问题进行约一天的MCTS搜索，生成1000条SFT训练数据。RL阶段每步采样256条路径（16问题×16路径），在计算效率与探索充分性之间取得折中。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/019_Table_9.jpg]]
*Table 9: Accuracy of our proposed RFTT and baselines across different mathematical reasoning benchmarks. The best results in each box are highlighted in bold. The proposed RFTT significantly boosts the performance of smaller LLMs across all datasets*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/017_Table_7.jpg]]
*Table 7: Comparison of computational cost*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/018_Table_8.jpg]]
*Table 8: Performance of RFTT on wider reasoning domains*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_lHbhzxiVI9/figures/020_Table_10.jpg]]
*Table 10: Comparison with entropy-based RL methods for promoting exploration. The best results in each box are highlighted in bold*


## 方法谱系与知识库定位

### 1. 方法演进定位

RFTT 处于**推理时搜索**与**强化微调**两条技术路线的交叉点，其核心创新在于将可学习的功能标记嵌入模型词汇表，使模型从“外部提示引导”转向“内部标记引导”的推理范式。

**相对于纯强化学习方法**：GRPO（Shao et al., 2024）等纯 RL 方法直接对模型进行策略优化，但在小模型上缺乏足够的初始推理能力与探索多样性，容易收敛到次优推理模式。RFTT 通过 SFT 预热阶段注入结构化推理数据，为后续 RL 提供了初始推理能力，消融实验表明移除 SFT 预热导致 Qwen-2.5-7B-Instruct 平均性能下降 2.9%，LLaMA-3.1-8B-Instruct 下降 7.7%（Table 6），验证了 SFT 预热对小模型的关键作用。

**相对于监督微调方法**：ReFT（Trung et al., 2024）通过监督微调提升推理能力，但缺乏在线探索机制。RFTT 在此基础上引入功能标记引导的 MCTS，在 RL 阶段实现自主树搜索探索，平均超越 ReFT 约 5 个百分点（Table 1）。

**相对于偏好优化方法**：MCTS-DPO（Xie et al., 2024）利用 MCTS 生成偏好对进行 DPO 训练，但训练与推理阶段搜索策略分离。RFTT 将树搜索直接嵌入 RL 训练循环，使模型在线采样功能标记自主构建推理树，训练与推理行为一致。

**相对于树搜索推理方法**：ResT-MCTS*（Zhang et al., 2024a）、rStar（Qi et al., 2024）、LLaMA-Berry（Zhang et al., 2024c）等方法在推理时使用 MCTS 增强性能，但依赖外部奖励模型引导搜索，且未将搜索过程内化到模型参数中。RFTT 通过功能标记将搜索行为编码进模型词汇表，使模型自身具备树搜索能力，在推理效率上显著优于同类方法——在 GSM8K 上达到 95.2% 准确率仅需 81 秒/题，而 rStar 需 203 秒/题（Table 3）。

**相对于树搜索 RL 方法**：TreeRL（Hou et al., 2025）同样结合树搜索与 RL，但 RFTT 的关键差异在于动作空间设计——将词汇级标记采样替换为人类推理行为动作空间（分析、验证、修正等），大幅降低了搜索复杂度。

### 2. 适用边界

**已验证的适用场景**：
- 数学推理任务（MATH-500、GSM8K、SVAMP、Olympiad Bench、AMC），训练数据仅来自 MATH 数据集
- 小规模模型（7B-8B 参数级别），包括 LLaMA-3.1-8B-Instruct、Qwen-2.5-7B-Instruct、Qwen-3-4B-Base
- 跨领域迁移：在 MMLU-Pro、GPQA、CommonsenseQA、FOLIO、TableBench、CRUXEval 等基准上展现出一定的泛化能力（Table 2），Qwen-2.5-7B-Instruct 在 MMLU-Pro 上达到 57.2%，GPQA 上达到 35.6%

**需要谨慎推广的场景**：
- 非数学推理领域（如法律、医学诊断）的有效性尚需验证
- 更大规模模型（>70B）上的表现未知
- 训练数据仅来自 MATH 数据集，可能存在对数学领域的过度优化

### 3. 局限与风险

**技术局限**：
- 功能标记可能被用于标记注入攻击，从而操纵模型行为
- 基于自我改进的 RL 循环可能导致能力意外放大或训练不稳定
- 增强的推理能力并未消除 LLM 固有的偏见、过度自信或生成错误但令人信服的输出等问题
- 小模型经过 RFTT 训练后仍可能产生错误但看起来合理的输出

**计算成本**：SFT 数据构建阶段需对 1.2k 问题使用 64 并发进程进行约一天的 MCTS 搜索，RL 阶段每步需为每个问题搜索 16 条推理路径，整体训练开销显著高于标准 SFT 或 RL 方法。

### 4. 开放问题

1. **领域泛化**：RFTT 能否有效扩展到更广泛的非数学推理领域（如法律、医学诊断、科学推理）？
2. **安全性**：如何进一步防御利用功能标记的恶意注入攻击？功能标记机制本身是否引入了新的攻击面？
3. **规模扩展**：能否在不显著增加计算成本的前提下，将功能标记引导的树搜索与更大规模模型（如 70B+）集成？
4. **训练稳定性**：在持续的自我改进循环中，如何避免模型遗忘原有能力或产生奖励破解（reward hacking）行为？
5. **功能标记语义**：功能标记的语义与行为之间的关系（Figure 4）是否具有跨模型、跨任务的稳定性？能否设计更优的功能标记集合？

## 原文 PDF

![[paperPDFs/ICLR_2026/Incentivizing_LLM_Reasoning_via_Reinforcement_Learning_with_Functional_Monte_Carlo_Tree_Search.pdf]]
