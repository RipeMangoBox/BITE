---
title: "MM-HELIX: Boosting Multimodal Long-Chain Reflective Reasoning with Holistic Platform and Adaptive Hybrid Policy Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MM_HELIX_Boosting_Multimodal_Long_Chain_Reflective_Reasoning_with_Holistic_Platform_and_Adaptive_Hybrid_Policy_Optimization.pdf
openreview_forum_id: ORCZ0wcPLm
aliases:
- AHPOA
- MM-HELIX
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "AHPO 中的动态自适应系数 ξ，根据在线策略在批次中的成功率决定是否激活基于离线专家数据的监督损失，从而在训练过程中动态调节专家指导与自主探索的平衡。"
primary_logic: "通过单阶段训练框架动态统一离线监督学习和在线策略梯度：在模型探索能力弱时借助专家数据提供密集指导，避免策略陷入困境；当模型熟练后自动关闭专家损失，鼓励独立探索，从而既能高效掌握复杂反思技能，又能将这些技能泛化至数学、逻辑等一般推理领域。"
claims:
- "AHPO 在 MM-HELIX 基准上将基线 Qwen2.5-VL-7B 的准确率提升 18.6%（6.3%→24.9%），并在四个一般数学与逻辑基准上平均提高 5.7%。"
- "仅使用 MM-HELIX 数据集进行 AHPO 训练即可在域内基准上实现 24.4% 的准确率，并且在逻辑基准 LogicVista 上提升至 48.3%，超过使用 MMK12 训练的 GRPO 基线。"
- "SERG 数据生成流水线将推理时间缩短约 90%（~27.8 小时 vs ~311.96 小时），且 Pass@16 达 99.8%；使用 SERG 数据进行 SFT 的整体准确率比纯规则 CoT 提升 4.9%。"
- "AHPO 训练后的 7B 模型在 MM-HELIX 上的表现已超越了多个更大规模的非反思模型，例如 Qwen-2.5-VL-72B（13.9%），说明反思能力的习得弥补了参数量的不足。"
---

# MM-HELIX: Boosting Multimodal Long-Chain Reflective Reasoning with Holistic Platform and Adaptive Hybrid Policy Optimization

> [!tip] 核心洞察
> 通过单阶段训练框架动态统一离线监督学习和在线策略梯度：在模型探索能力弱时借助专家数据提供密集指导，避免策略陷入困境；当模型熟练后自动关闭专家损失，鼓励独立探索，从而既能高效掌握复杂反思技能，又能将这些技能泛化至数学、逻辑等一般推理领域。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MM-HELIX：通过整体平台与自适应混合策略优化提升多模态长链反思推理 |
| 英文题名 | MM-HELIX: Boosting Multimodal Long-Chain Reflective Reasoning with Holistic Platform and Adaptive Hybrid Policy Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ORCZ0wcPLm); [Project](https://mm-helix.github.io/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Adaptive Hybrid Policy Optimization (AHPO) |
| Dataset | MM-HELIX, MathVision, MathVerse-V1, LogicVista |

> [!tip] 效果简介
> - MM-HELIX 上，Accuracy (%) 为 24.9，对比 6.3，变化 +18.6。
> - MathVision 上，Accuracy (%) 为 26.6，对比 25.2，变化 +1.4。
> - MathVerse-V1 上，Accuracy (%) 为 47.5，对比 40.5，变化 +7.0。

## 概述

### 问题瓶颈

当前多模态大语言模型（MLLMs）在需要迭代思考、回溯与动态状态跟踪的长链反思推理任务上暴露出系统性缺陷。即使在纯文本输入下，顶尖模型的表现也远未令人满意；而当引入视觉模态时，性能进一步大幅下降，形成显著的模态差距。其根本原因在于：标准的在线强化学习方法（如 **GRPO**，Shao et al., 2024）在这类复杂任务中面临奖励极度稀疏的困境，策略难以获得有效学习信号；而纯监督微调（SFT）虽能借助专家数据掌握域内技能，却会导致对一般数学、逻辑等推理任务的灾难性遗忘。

### 核心思路

本文提出 **MM-HELIX** 整体平台与 **自适应混合策略优化（AHPO）** 方法，通过单阶段训练框架动态统一离线监督学习与在线策略梯度，从根本上化解上述矛盾。其核心调控机制是一个动态自适应系数 $\xi$：

$$\xi = \mathbf{1}\left(\sum_{i=1}^{N_{\mathrm{on}}} \mathbb{I}(R(\tau_i) = 1) < \hat{R}\right)$$

当在线策略在批次中的成功轨迹数低于预设阈值 $\hat{R}$ 时，$\xi=1$ 激活基于离线专家数据的监督损失，为策略提供密集指导，避免探索陷入困境；当模型能力提升、成功轨迹数达标后，$\xi=0$ 自动关闭专家损失，鼓励独立探索。这种“按需辅助”的设计使得模型既能高效习得复杂反思技能，又能将这些技能泛化至一般推理领域。

### 方法定位

AHPO 在方法谱系中处于离线模仿学习与在线策略梯度之间的动态混合地带。与标准 **GRPO** 仅依赖在线采样构造损失不同，AHPO 在总损失中显式引入离线专家轨迹的负对数似然项：

$$\mathcal{L}_{\mathrm{AHPO}}(\theta) = \xi \mathcal{L}_{\mathrm{off-policy}}(\theta) + \mathcal{L}_{\mathrm{on-policy}}(\theta)$$

其中 $\mathcal{L}_{\mathrm{off-policy}}$ 迫使策略模仿专家输出，$\mathcal{L}_{\mathrm{on-policy}}$ 基于组内标准化优势估计进行策略梯度更新。相较于先 SFT 后 GRPO 的两阶段训练，AHPO 在单一阶段内完成监督信号与探索信号的融合；相较于 **LUFFY**（Yan et al., 2025）等基于偏好学习的混合方法，AHPO 通过成功率驱动的开关式 $\xi$ 实现了更简洁、更稳定的动态调节。此外，AHPO 移除了原始 GRPO 中的 KL 散度约束与 CLIP 模块，以降低计算开销并释放策略探索空间。

为支撑 AHPO 训练，本文构建了 **MM-HELIX 基准**（覆盖 42 个任务、5 个难度级别、1,260 个评估实例）与 **MM-HELIX-100K 数据集**（10 万条高质量反思推理轨迹）。数据生成采用 **步骤引导式响应生成流水线（SERG）**：先用规则 CoT 构造函数生成骨架推理路径，再由 Qwen3-235B 细化为自然反思轨迹，最终通过验证器筛选。该流水线将推理生成时间缩短约 90%（~27.8 小时 vs ~311.96 小时），且 Pass@16 达 99.8%。

### 主要结果

- **域内性能**：AHPO 在 MM-HELIX 基准上将基线 Qwen2.5-VL-7B 的准确率从 6.3% 提升至 24.9%（**+18.6 个百分点**），超越了 Qwen2.5-VL-72B（13.9%）等更大规模的非反思模型，表明反思能力的习得可弥补参数量的不足。
- **泛化性能**：在 MathVision、MathVerse-V1、LogicVista、WeMath 四个一般数学与逻辑基准上，AHPO 平均提升 **+5.7 个百分点**，证明域内习得的反思技能可有效迁移。
- **数据效率**：仅使用 MM-HELIX-100K 进行 AHPO 训练，域内准确率即达 24.4%，LogicVista 提升至 48.3%，超过使用数学数据集 MMK12 训练的 GRPO 基线，验证了反思数据本身的迁移价值。
- **消融验证**：动态系数 $\xi$ 是 AHPO 稳定性的关键——静态系数版本（Static-AHPO）虽在训练初期优于 GRPO 与 LUFFY，但后期出现不稳定和性能下降；AHPO 通过自适应开关避免了离线-在线分布冲突，保持稳定提升。

### 局限与开放问题

AHPO 的训练依赖 Qwen3-235B 生成的高质量专家数据，复现门槛较高；MM-HELIX 基准的任务类型集中于图、谜题、算法与游戏等结构化领域，对真实世界多模态场景的覆盖不足；动态系数 $\xi$ 的阈值 $\hat{R}$ 的选取策略及其在不同任务分布下的鲁棒性尚未充分讨论；方法仅在 Qwen2.5-VL-7B 单一架构上验证，跨模型迁移效果待检验。此外，SFT 导致灾难性遗忘而 AHPO 得以避免的内在分布鲁棒性机制，以及反思能力向非结构化多模态任务迁移的深度，仍是值得深入探索的开放问题。

## 背景与动机

多模态大语言模型（MLLMs）在视觉问答、文档理解等任务上已取得显著进展，然而当面对需要**迭代思考、回溯验证和动态状态跟踪**的长链反思推理任务时，现有模型普遍暴露出严重的能力缺陷。以 MM-HELIX 基准的评估结果为例，当前最先进的开源模型 **Qwen2.5-VL-72B** 仅取得 13.9% 的准确率，而规模更大的 **GLM-4.5V-106B** 同样表现不佳（Table 1）。这一现象揭示了一个核心瓶颈：**现有 MLLM 缺乏在复杂推理链中持续反思、自我纠错的内在机制**。

### 现有训练范式的两难困境

针对上述问题，研究者通常诉诸两种训练范式，但二者均存在显著局限：

- **监督微调（SFT）**：通过专家推理轨迹进行模仿学习，能够为模型提供密集的指导信号。然而，SFT 在提升域内反射能力的同时，往往导致对一般推理任务（如数学、逻辑）的**灾难性遗忘**——模型过度拟合专家数据的分布，丧失了泛化所需的探索能力。

- **在线强化学习（如 GRPO）**：通过策略梯度鼓励模型自主探索，理论上可习得可迁移的推理技能。但在复杂的长链反思任务中，奖励信号**极度稀疏**——模型只有在生成完整且正确的推理链时才能获得正向反馈，导致训练初期策略陷入困境，无法有效启动学习过程（Figure 6 中 GRPO 的奖励曲线始终处于低位）。

这种困境的本质在于：**离线监督提供密集指导但扼杀泛化，在线探索追求泛化却受困于稀疏奖励**。现有的混合策略（如先 SFT 后 GRPO 的顺序训练，或基于偏好学习的 **LUFFY** 方法，Yan et al., 2025）试图折中，但均未从根本上解决两个阶段的**分布冲突**——监督阶段习得的策略偏向专家数据分布，而强化学习阶段需要策略偏离该分布以探索更优行为，二者在训练目标上存在内在张力。

### 本文的核心动机

基于上述分析，本文的核心动机可凝练为三个递进的问题：

1. **如何系统评估 MLLM 的反思推理能力？** 现有基准多聚焦于单步或短链推理，缺乏对迭代思考、回溯等长链反思行为的专门度量。

2. **如何高效生成高质量的反思推理训练数据？** 人工标注成本高昂且难以规模化，直接使用大模型进行轨迹采样则面临推理时间长、成功率低的问题（纯模型采样的 Pass@16 仅为 25.0%，推理耗时约 312 小时；Table 3）。

3. **如何在单一训练阶段内动态统一离线监督与在线探索？** 理想的方法应当能够在模型能力不足时借助专家数据提供密集指导，而在模型逐步熟练后自动减弱监督、鼓励独立探索，从而同时实现域内技能的快速掌握与跨域泛化。

针对这些问题，本文提出了 **MM-HELIX 基准**、**SERG 数据生成流水线**以及 **AHPO 自适应混合策略优化**三部分构成的整体框架（Figure 1），旨在系统性地突破 MLLM 在长链反思推理上的能力瓶颈。

## 核心创新

### 问题瓶颈

当前多模态大语言模型（MLLMs）在长链反思推理任务上存在显著性能缺陷。这类任务要求模型进行迭代思考、回溯和动态状态跟踪，而主流模型——即便是具备“思考”能力的先进模型——在此类任务上的准确率极低。例如，**Qwen2.5-VL-72B**（Bai et al., 2025b）在 MM-HELIX 基准上的多模态准确率仅为 13.9%，而最强的闭源模型 GPT-5 也仅达到 58.1%，远未饱和。

这一缺陷的根源在于训练范式的两难困境：标准的在线强化学习方法（如 **GRPO**，Shao et al., 2024）在复杂推理任务中面临奖励极度稀疏的问题，策略难以从零开始探索出正确的长链推理路径；而监督微调（SFT）虽然能通过专家数据快速注入领域技能，却会导致对一般推理任务（如数学、逻辑）的灾难性遗忘。

### 核心洞察

MM-HELIX 的核心洞察在于：**离线专家监督与在线策略探索并非互斥，而是可以通过一个动态门控机制在单阶段训练中实现互补统一。** 在训练初期，模型的自主探索能力极弱，此时需要专家数据提供密集的梯度信号，引导策略走出奖励稀疏的困境；而当模型逐步掌握反思技能后，应逐步减少甚至关闭专家监督，鼓励独立探索，从而将学到的反思能力泛化至更广泛的推理领域。

### 关键创新点：Adaptive Hybrid Policy Optimization (AHPO)

AHPO 围绕上述洞察，对标准 GRPO 框架进行了四个关键改造，形成了一套单阶段自适应混合训练策略。

#### 1. 离线–在线损失统一

标准 GRPO 仅从在线策略采样的轨迹中构造策略梯度损失，不显式利用离线专家数据。AHPO 在总损失中引入了一个基于离线专家轨迹的负对数似然项：

$$\mathcal{L}_{\mathrm{off-policy}}(\theta) = -\frac{1}{|y^*|} \sum_{t=1}^{|y^*|} \log \pi_\theta(y_t^* | x, y_{<t}^*)$$

该损失迫使策略模仿专家输出 $y^*$，提供密集的逐 token 监督信号。在线损失则沿用 GRPO 风格的组内标准化策略梯度：

$$\mathcal{L}_{\mathrm{on-policy}}(\theta) = -\frac{1}{\sum_{i=1}^N |\tau_i|} \sum_{i=1}^N \sum_{t=1}^{|\tau_i|} \mathrm{CLIP}(r_{i,t}(\theta), A_i, \epsilon)$$

其中优势估计 $A_i$ 采用组内均值–标准差归一化：

$$A_i = \frac{R(\tau_i) - \mathrm{mean}(\{R(\tau_i)\})}{\mathrm{std}(\{R(\tau_i)\})}$$

最终统一损失为两者的线性组合：

$$\mathcal{L}_{\mathrm{AHPO}}(\theta) = \xi \mathcal{L}_{\mathrm{off-policy}}(\theta) + \mathcal{L}_{\mathrm{on-policy}}(\theta)$$

#### 2. 动态自适应系数 ξ

这是 AHPO 最关键的创新。若采用固定系数（Static-AHPO），离线专家损失的权重在整个训练过程中保持不变，训练后期会出现离线–在线分布冲突导致的性能不稳定甚至下降。AHPO 通过一个基于实时成功率的指示函数动态控制 ξ：

$$\xi = \mathbf{1}\left(\sum_{i=1}^{N_{\mathrm{on}}} \mathbb{I}(R(\tau_i) = 1) < \hat{R}\right)$$

其逻辑是：当在线策略在批次中产生的成功轨迹数低于预设阈值 $\hat{R}$ 时，激活离线专家损失（$\xi=1$），借助专家数据提供密集指导；一旦模型在该批次中表现出足够的自主求解能力，立即关闭专家损失（$\xi=0$），鼓励独立探索。这一机制使监督信号仅在模型能力不足时介入，避免了不必要的约束。

实验证据直接验证了动态 ξ 的有效性：Static-AHPO 虽然在初期强于 GRPO 与 **LUFFY**（Yan et al., 2025），但在训练后期奖励曲线出现明显波动和下降；而 AHPO 的动态切换策略保持了训练的稳定提升（见 **Figure 7**）。

#### 3. KL 散度移除

原始 GRPO 通常包含一个 KL 散度项，用于约束策略更新不偏离参考策略过远。AHPO 在实现中移除了该 KL 散度项，以降低对策略探索的约束并减少计算开销。这一选择与动态 ξ 的设计理念一致：当模型能力不足时，专家损失本身已提供足够的正则化引导；当模型能力充足时，KL 约束反而会限制其泛化探索。

#### 4. CLIP 模块移除

类似地，AHPO 移除了原始 GRPO 中用于限制策略概率比值更新幅度的 CLIP 操作，以进一步简化训练流程、提高效率。这一简化在动态 ξ 的配合下未损害训练稳定性，反而使整体框架更加轻量。

### 与基线方法的关键差异

| 设计维度 | GRPO (Shao et al., 2024) | LUFFY (Yan et al., 2025) | AHPO (本文) |
|---------|-------------------------|-------------------------|------------|
| 离线数据利用 | 不显式利用 | 基于偏好学习混合 | 负对数似然损失 + 动态门控 |
| 训练阶段 | 单阶段在线 RL | 混合 RL | 单阶段自适应混合 |
| 监督信号介入 | 无 | 固定混合 | 成功率驱动的动态切换 |
| KL 散度 | 包含 | — | 移除 |
| CLIP 操作 | 包含 | — | 移除 |

### 为什么 AHPO 能同时提升域内与泛化性能？

AHPO 的设计直接回应了 SFT 导致灾难性遗忘的机制问题。纯 SFT 在整个训练过程中强制模型模仿专家分布，导致策略过度拟合域内数据模式，丧失在一般推理任务上的生成多样性。AHPO 通过动态 ξ 实现了**渐进式自主**：训练初期模型能力弱，ξ 激活，专家数据提供必要的“脚手架”；随着成功率提升，ξ 关闭，模型在在线 RL 信号的引导下自主探索，从而在掌握反思技能的同时保留了推理多样性。这一机制解释了为何 AHPO 在 MM-HELIX 基准上提升 18.6%（6.3%→24.9%）的同时，在四个通用数学与逻辑基准上平均提升 5.7%（见 **Table 2**），且训练后的 7B 模型在 MM-HELIX 上的表现超越了 Qwen2.5-VL-72B 等更大规模的非反思模型。

## 整体框架

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_ORCZ0wcPLm/figures/001_Figure_1.jpg]]
*Figure 1: Overview of proposed framework. Our framework comprises two core components: (1) MM-HELIX benchmark to evaluate the reflective capabilities of MLLM, and (2) AHPO method to boost reflection capability and transfer enhanced skills to general reasoning tasks*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_ORCZ0wcPLm/figures/005_Figure_5.jpg]]
*Figure 5: Demonstration of Adaptive Hybrid Policy Optimization (AHPO). AHPO dynamically integrates off-policy expert guidance with on-policy exploration, leading to performance generalization*

MM-HELIX 框架的核心目标是通过一个完整的“评估—数据生成—训练”闭环，解决当前多模态大语言模型在长链反思推理任务上的性能缺陷。该框架由两大核心组件构成：**MM-HELIX 基准**（用于评估和诊断）与 **AHPO 训练策略**（用于能力习得和泛化），二者通过 **SERG 数据生成流水线** 桥接，形成从问题定义到能力提升的完整路径（Figure 1）。

### 模块关系与数据流

整个 pipeline 遵循“基准构建 → 专家数据合成 → 混合策略训练”的线性推进逻辑：

1.  **MM-HELIX Benchmark Generator**  
    作为框架的起点，该模块通过基于规则的实例生成器、求解器与验证器，构建了一个覆盖 4 大类别（Puzzles、Graphs、Algorithms、Games）、42 个任务、5 个难度级别的多模态反思推理基准（Figure 2）。验证器根据答案复杂度采用精确匹配或程序化验证两种策略，确保评估的可靠性。最终评估集包含 1,260 个实例，每个任务在每个难度级别上采样 6 个实例。该基准的核心作用是**量化诊断当前 MLLMs 的反思推理缺陷**，并为后续数据生成提供任务骨架。

2.  **Step-Elicited Response Generation (SERG) 流水线**  
    该模块是连接基准与训练数据的关键桥梁（Figure 4）。其输入为 MM-HELIX 基准的任务定义与规则 CoT 构造函数生成的骨架推理路径，输出为经过 Qwen3-235B 细化并筛选的高质量反思推理轨迹。具体流程为：先利用规则 CoT 构造函数生成结构正确的推理骨架，再通过大模型将其细化为自然、包含反思步骤的 CoT 轨迹，最后由验证器筛选出正确的高质量数据。这一混合策略将推理时间从纯模型采样的约 311.96 小时大幅缩减至约 27.78 小时（缩减约 90%），同时将 Pass@16 提升至 99.8%（Table 3）。

3.  **MM-HELIX-100K Dataset**  
    SERG 流水线的输出产物，包含 10 万条高质量反思推理轨迹，覆盖全部 42 个任务。该数据集在 SFT 阶段的训练效果显著优于纯规则 CoT 数据（总体准确率 23.8% vs 18.9%，Table 4），并作为 AHPO 训练中的**离线专家数据源**，为策略提供密集的监督信号。

4.  **AHPO Trainer**  
    框架的核心训练模块（Figure 5），接收 MM-HELIX-100K（离线专家数据）和 MMK12（在线探索数据）作为输入，通过单阶段训练动态统一离线监督与在线策略梯度。其关键机制是通过**自适应系数 ξ** 实时调控离线损失的激活状态：

    $$ \mathcal{L}_{\mathrm{AHPO}}(\theta) = \xi \mathcal{L}_{\mathrm{off-policy}}(\theta) + \mathcal{L}_{\mathrm{on-policy}}(\theta) $$

    其中离线损失为专家轨迹的负对数似然：

    $$ \mathcal{L}_{\mathrm{off-policy}}(\theta) = -\frac{1}{|y^*|} \sum_{t=1}^{|y^*|} \log \pi_\theta(y_t^* | x, y_{<t}^*) $$

    在线损失为基于组内标准化优势估计的裁剪策略梯度（实际实现中移除了 KL 散度和 CLIP 模块以简化训练）。自适应系数 ξ 由指示函数动态确定：

    $$ \xi = \mathbf{1}\left(\sum_{i=1}^{N_{\mathrm{on}}} \mathbb{I}(R(\tau_i) = 1) < \hat{R}\right) $$

    当批次中成功轨迹数低于预设阈值 R̂ 时，ξ=1 激活离线专家损失，迫使策略模仿专家行为；当模型能力足够时，ξ=0 关闭监督信号，鼓励独立探索。这一“按需辅助”的设计是框架能够**同时提升域内反思能力与泛化至通用推理任务**的核心因果机制。

### 输入输出流总结

| 模块 | 输入 | 输出 | 作用 |
|------|------|------|------|
| Benchmark Generator | 任务定义、难度参数 | MM-HELIX 基准（1,260 实例） | 评估诊断 |
| SERG Pipeline | 任务定义、规则 CoT 骨架 | MM-HELIX-100K 数据集 | 专家数据合成 |
| AHPO Trainer | MM-HELIX-100K + MMK12 | 经 AHPO 训练的 Qwen2.5-VL-7B 模型 | 能力习得与泛化 |

整个框架的设计哲学在于：**通过合成基准暴露缺陷，通过混合生成高效构建专家数据，通过动态混合策略在探索与监督之间取得平衡**，最终使 7B 规模的模型在 MM-HELIX 上的表现（24.9%）超越多个更大规模的非反思模型（如 Qwen2.5-VL-72B 的 13.9%），并在通用数学与逻辑基准上平均提升 5.7 个百分点。

## 核心模块与公式推导

### 整体框架概览

MM-HELIX 框架包含两个核心组件（Figure 1）：(1) **MM-HELIX 基准**，用于评估多模态大语言模型（MLLM）的反思推理能力；(2) **AHPO 方法**，用于增强反思能力并将所学技能迁移至通用推理任务。整体流程为：首先通过规则生成器构建 MM-HELIX 基准，随后利用步骤引导式响应生成流水线（SERG）从基准中生成高质量反思推理轨迹数据集 MM-HELIX-100K，最后通过 AHPO 训练器在单阶段内动态统一离线监督与在线策略优化。

### 关键模块

#### MM-HELIX 基准生成器

该模块基于规则构造 42 个多模态任务，覆盖 **Puzzles**（18 个任务，如数独、Nonogram、Kakuro）、**Graphs**（8 个任务，如欧拉回路/路径、最大流、拓扑排序）、**Algorithms** 和 **Games** 四个类别（Figure 2）。每个任务配备实例生成器、求解器与验证器。难度通过程序化调整推理所需步数来控制，共分为 5 个渐进级别。最终评估集包含 1,260 个实例，每个任务在各难度级别上均匀采样 6 个实例，共 30 个。

验证器根据答案复杂度采用两种验证策略：对于简单离散答案（如布尔值或数值），执行直接精确匹配；对于复杂答案，则通过求解器进行结构化验证。

#### 步骤引导式响应生成流水线（SERG）

SERG 流水线（Figure 4）旨在高效生成高质量的反思型思维链（CoT）轨迹。其核心设计为：

1. **规则骨架构造**：利用基准内置的规则 CoT 构造函数生成结构化的推理路径骨架。
2. **大模型精炼**：通过 Qwen3-235B 将骨架细化为自然语言形式、包含反思步骤的完整 CoT 轨迹。
3. **验证筛选**：通过验证器过滤低质量数据，确保最终数据集的可靠性。

该流水线生成的数据集 **MM-HELIX-100K** 包含 100k 条高质量反思推理轨迹，覆盖全部 42 个任务，用作 AHPO 的离线专家数据。SERG 相比纯模型采样的推理时间缩短约 90%（~27.8 小时 vs ~311.96 小时），且 Pass@16 达到 99.8%。

#### AHPO 训练器

AHPO 训练器（Figure 5）实现单阶段动态混合优化，其架构包含两条并行路径：

- **在线策略路径**：策略模型对输入（如扫雷谜题）生成响应，通过组奖励计算产生逐样本优势估计 $A_1, \dots, A_N$，用于在线策略损失。
- **离线策略路径**：从 MM-HELIX-100K 中采样专家轨迹，计算负对数似然损失，并通过动态系数 $\xi$ 控制其对总损失的贡献。

### 核心公式

AHPO 的统一损失函数由离线损失与在线损失通过自适应系数 $\xi$ 动态组合而成。

**离线策略损失**（负对数似然，迫使策略模仿专家输出）：

$$\mathcal{L}_{\mathrm{off-policy}}(\theta) = -\frac{1}{|y^*|} \sum_{t=1}^{|y^*|} \log \pi_\theta(y_t^* \mid x, y_{<t}^*)$$

其中 $y^*$ 为离线专家轨迹，$|y^*|$ 为其长度，$\pi_\theta$ 为当前策略。

**在线策略损失**（裁剪策略梯度，使用组内优势估计）：

$$\mathcal{L}_{\mathrm{on-policy}}(\theta) = -\frac{1}{\sum_{i=1}^N |\tau_i|} \sum_{i=1}^N \sum_{t=1}^{|\tau_i|} \mathrm{CLIP}(r_{i,t}(\theta), A_i, \epsilon)$$

其中 $\tau_i$ 为在线采样的第 $i$ 条轨迹，$r_{i,t}(\theta)$ 为概率比值，$A_i$ 为轨迹级优势估计，$\epsilon$ 为裁剪阈值。值得注意的是，AHPO 在实现中移除了 KL 散度项（减少对策略探索的约束）和 CLIP 模块（简化训练、提高效率）。

**优势估计**（组内均值-标准差归一化）：

$$A_i = \frac{R(\tau_i) - \mathrm{mean}(\{R(\tau_i) \mid \tau_i \sim \pi_{\theta_{\mathrm{old}}}(\tau), i=1,2,\dots,N\})}{\mathrm{std}(\{R(\tau_i) \mid \tau_i \sim \pi_{\theta_{\mathrm{old}}}(\tau), i=1,2,\dots,N\})}$$

**AHPO 统一损失**：

$$\mathcal{L}_{\mathrm{AHPO}}(\theta) = \xi \mathcal{L}_{\mathrm{off-policy}}(\theta) + \mathcal{L}_{\mathrm{on-policy}}(\theta)$$

**自适应离线系数**（核心调控机制）：

$$\xi = \mathbf{1}\left(\sum_{i=1}^{N_{\mathrm{on}}} \mathbb{I}(R(\tau_i) = 1) < \hat{R}\right)$$

其中 $N_{\mathrm{on}}$ 为在线采样轨迹数，$\mathbb{I}(R(\tau_i) = 1)$ 指示轨迹是否完全正确（奖励为 1），$\hat{R}$ 为预设的成功轨迹数阈值。该指示函数的核心逻辑为：**当批次内成功轨迹数低于阈值时，激活离线专家损失（$\xi=1$），为策略提供密集监督信号；当模型自主探索能力足够时，关闭专家损失（$\xi=0$），鼓励独立探索**。

这一动态切换机制是 AHPO 区别于静态混合方法（Static-AHPO，$\xi$ 固定）的关键设计。实验表明，Static-AHPO 虽在训练初期强于 GRPO 与 LUFFY，但在后期出现不稳定和性能下降；而动态 $\xi$ 的 AHPO 能有效避免离线-在线分布冲突，保持训练的稳定提升（Figure 7）。

## 实验与分析

### 核心实验结果

AHPO 在 MM-HELIX 基准上实现了显著的性能突破。基于 Qwen2.5-VL-7B 基座模型，AHPO 取得了 **24.9%** 的准确率，相较于未训练的基座模型（6.3%）提升了 **+18.6 个百分点**（Table 2）。这一结果不仅远超所有对比训练策略——GRPO（7.7%）、SFT（12.2%）、SFT+GRPO（21.1%）以及基于偏好学习的 LUFFY（Yan et al., 2025）（7.9%）——更值得关注的是，经过 AHPO 训练的 7B 模型在 MM-HELIX 上的表现已经超越了多个更大规模的非反思模型，例如 Qwen2.5-VL-72B（13.9%）和 GLM-4.5V-106B。这表明，**反思能力的习得有效弥补了参数量的不足**，AHPO 并非单纯依赖模型容量扩张，而是通过训练策略本身赋予了小模型处理长链反思推理的能力。


![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_ORCZ0wcPLm/figures/009_Table_2.jpg]]
*Table 2: Comparison of AHPO and other training strategies. AHPO achieves significant improvement on MM-HELIX while also showing great performance transfer to general mathematics and logic tasks, indicating a robust enhancement of both specialized and generalized reasoning abilities*

在泛化性能方面，AHPO 在四个通用数学与逻辑推理基准上取得了平均 **+5.7 个百分点**的提升（从基线的 36.5% 提升至 42.2%）。具体而言：MathVision 从 25.2% 提升至 26.6%（+1.4%），MathVerse-V1 从 40.5% 提升至 47.5%（+7.0%），LogicVista 从 45.6% 提升至 53.5%（+7.9%），WeMath 从 34.5% 提升至 41.1%（+6.6%）。这一结果验证了 AHPO 的核心设计目标：**在域内掌握复杂反思技能的同时，将这些技能有效迁移至一般推理领域**，避免了标准 SFT 常见的灾难性遗忘问题。

### 消融实验：数据组成的影响

为分析训练数据构成对性能的贡献，实验对比了三种数据配置下的 AHPO 训练效果（Table 5）：


![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_ORCZ0wcPLm/figures/012_Table_5.jpg]]
*Table 5: Performance of each data component in training data. By utilizing AHPO with MM-HELIX dataset which has no overlap with the mathematical content MMK12, the model achieves much better performance on both in-domain and general benchmark*

- **仅用 MMK12**：该数据集仅包含问题-答案对，缺乏思维链轨迹。在此配置下，MM-HELIX 基准准确率仅为 5.5%，与基座模型（6.3%）几乎持平，说明纯答案监督的强化学习无法激发反思能力。
- **仅用 MM-HELIX-100K**：单独使用包含专家反思轨迹的 MM-HELIX 数据集进行 AHPO 训练，将 MM-HELIX 基准准确率从 6.3% 大幅提升至 **24.4%**，并在 LogicVista 上达到了 48.3%——甚至超过了仅用 MMK12 训练的 GRPO 基线。然而，MathVerse-V 准确率从基线的 40.5% 略微下降至 39.9%，表明**纯域内数据虽能有效掌握反思技能，但在部分泛化任务上仍需辅助数据支撑**。
- **混合数据（MM-HELIX-100K + MMK12）**：在所有基准上均取得最优结果，MM-HELIX 达到 24.9%，WeMath 达到 41.1%。混合策略同时利用了专家反思轨迹的技能引导和数学数据的泛化支撑，实现了域内与域外性能的最佳平衡。

### SERG 数据生成流水线的效率与质量

SERG（Step-Elicited Response Generation）流水线在数据生成效率上展现出压倒性优势（Table 3）。相较于传统的 Model Rollout 方法（直接调用大模型生成 CoT），SERG 将推理生成时间从约 **311.96 小时**缩减至约 **27.78 小时**，缩短约 **90%**，同时平均生成长度从 7140.59 tokens 降至 5500.53 tokens，减少了冗余。更关键的是，SERG 的 Pass@16 达到了 **99.8%**，远超 Model Rollout 的 25.0%，表明其生成的高质量轨迹几乎无需人工后处理。


![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_ORCZ0wcPLm/figures/010_Table_3.jpg]]
*Table 3: Comparison of CoT generation methods cost. Our hybrid approach significantly save the generation cost and make less redundancy. Table 4: Efficiency of our dataset in SFT stage. Our method outperforms Rule-Based CoT, indicates great quality of our generation method*

在 SFT 阶段的数据质量验证中（Table 4），使用 SERG 数据训练的模型在 MM-HELIX 上取得了 **23.8%** 的整体准确率，相较于使用纯规则 CoT 数据训练的基线（18.9%）提升了 **+4.9 个百分点**。这证实了 SERG 生成的包含自然反思步骤的 CoT 轨迹比机械化的规则推导序列更有利于模型学习反思推理能力。

### 自适应系数 ξ 的关键作用

AHPO 与 Static-AHPO 的训练曲线对比（Figure 6, Figure 7）揭示了动态系数 ξ 的核心价值。Static-AHPO 采用固定系数，在训练初期虽优于 GRPO 和 LUFFY，但在训练后期出现明显的性能不稳定和下降趋势。这是因为固定的离线损失权重导致离线专家数据与在线探索分布之间产生持续冲突，阻碍了策略的自主进化。


![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_ORCZ0wcPLm/figures/007_Figure_7.jpg]]
*Figure 7: Comparison of Static-AHPO and AHPO. AHPO dynamically integrates expert data to ensure a robust training*

AHPO 通过动态系数 ξ 的指示函数机制——当组内成功轨迹数低于预设阈值 R̂ 时激活离线专家损失（ξ=1），否则关闭（ξ=0）——实现了**监督信号仅在模型能力不足时介入**。这一设计使得训练后期模型能够摆脱对专家数据的依赖，充分进行自主探索，从而获得更稳定且更高的最终性能。

### 失败模式与局限性

尽管 AHPO 取得了显著成效，但实验分析揭示了若干值得关注的局限：

1. **泛化的非对称性**：仅用 MM-HELIX-100K 训练时，MathVerse-V 性能出现轻微下降（-0.6%），而 LogicVista 却大幅提升（+2.7% vs 基线）。这表明反思技能的迁移具有任务选择性，可能与目标任务的推理结构与训练数据中反思模式的相似度有关，具体机制尚待进一步分析。

2. **SFT 的灾难性遗忘**：标准 SFT 训练在 MM-HELIX 上仅达到 12.2%，且其泛化性能未在 Table 2 中单独报告。AHPO 通过单阶段动态混合损失有效避免了这一问题，但其内在的分布鲁棒性机制——即为何离线-在线动态切换能同时保留域内技能和泛化能力——仍需更深入的理论解释。

3. **数据依赖性**：AHPO 的性能高度依赖于 MM-HELIX-100K 中专家轨迹的质量，而该数据集的生成需要 Qwen3-235B 等大规模模型和 SERG 流水线的支持，可能限制小规模团队的直接复现。

4. **超参数敏感性**：动态系数 ξ 依赖于预设的成功阈值 R̂，原文未系统讨论该阈值在不同任务难度或训练阶段下的选择策略及其鲁棒性，这在实际部署中可能需要额外的调参工作。

## 方法谱系与知识库定位

### 1. 核心方法定位

MM-HELIX 提出的 **Adaptive Hybrid Policy Optimization (AHPO)** 是一种单阶段训练策略，旨在解决多模态大语言模型（MLLMs）在长链反思推理任务上的学习难题。其核心创新在于通过动态系数 $\xi$ 将离线专家监督与在线策略探索统一于同一训练阶段，打破了传统“先监督微调（SFT）后强化学习（GRPO）”的两阶段范式。

AHPO 在方法谱系中处于 **离线模仿学习** 与 **在线策略梯度** 的交汇点。与纯离线方法（如行为克隆）不同，AHPO 保留了在线探索能力；与纯在线方法（如 GRPO, Shao et al., 2024）不同，AHPO 在策略能力不足时主动引入专家轨迹的负对数似然损失作为密集指导信号。这种设计直接回应了长链推理任务中奖励极度稀疏的瓶颈：当模型尚未掌握回溯与迭代思考技能时，仅依赖稀疏的最终答案奖励无法产生有效的梯度信号。

### 2. 与基线方法的本质差异

| 方法 | 训练阶段 | 数据利用 | 核心机制 | 关键局限 |
|------|---------|---------|---------|---------|
| **GRPO** (Shao et al., 2024) | 单阶段在线 | 仅在线采样轨迹 | 组内标准化优势估计 + 裁剪策略梯度 | 稀疏奖励下训练停滞 |
| **SFT** | 单阶段离线 | 仅专家轨迹 | 负对数似然损失 | 灾难性遗忘，泛化能力退化 |
| **SFT → GRPO** | 两阶段顺序 | 先专家后在线 | 先模仿再探索 | 两阶段分布偏移，SFT 阶段遗忘不可逆 |
| **LUFFY** (Yan et al., 2025) | 单阶段混合 | 偏好对数据 | 基于偏好学习的混合 RL | 依赖偏好标注，训练后期不稳定（Figure 6） |
| **AHPO (本文)** | 单阶段自适应 | 专家 + 在线采样 | 动态系数 $\xi$ 门控离线损失 | 依赖高质量专家数据，阈值 $\hat{R}$ 需预设 |

**关键区分点**：

- **与 GRPO 的本质差异**：AHPO 在 GRPO 的在线策略梯度框架上增加了两个关键修改：(1) 引入基于离线专家轨迹的监督损失 $\mathcal{L}_{\mathrm{off-policy}}$；(2) 移除 KL 散度约束和 CLIP 模块以降低对策略探索的限制。这两个修改使得模型在探索初期能够从专家数据中获得密集的学习信号，而非在稀疏奖励空间中盲目搜索。

- **与 SFT+GRPO 两阶段范式的本质差异**：两阶段训练存在不可逆的分布偏移——SFT 阶段将策略强制拉向专家分布，可能导致对一般推理能力的灾难性遗忘；随后的 GRPO 阶段从已偏移的策略出发，难以恢复已丧失的能力。AHPO 通过动态系数 $\xi = \mathbf{1}\left(\sum_{i=1}^{N_{\mathrm{on}}} \mathbb{I}(R(\tau_i) = 1) < \hat{R}\right)$ 实现了单阶段的平滑过渡：当在线策略的成功轨迹数低于阈值 $\hat{R}$ 时激活专家损失（$\xi=1$），否则关闭（$\xi=0$），使模型在能力不足时获得指导，在能力充足时自主探索。

- **与 LUFFY 的本质差异**：LUFFY 基于偏好学习构造混合损失，但其固定权重的设计在训练后期出现不稳定和性能下降（Figure 6）。AHPO 的自适应门控机制在训练后期自动关闭离线损失，避免了离线-在线分布冲突导致的性能退化（Figure 7）。

### 3. 适用边界

**有效适用场景**：
- 需要长链推理、迭代回溯和动态状态跟踪的结构化任务（如图搜索、谜题求解、算法模拟）
- 奖励函数可被明确定义为二值成功/失败（$R(\tau) \in \{0, 1\}$）的任务
- 存在高质量专家轨迹数据，且专家数据与目标任务的推理模式一致

**能力边界**：
- AHPO 的有效性依赖于专家数据的质量与覆盖度。当专家轨迹无法覆盖任务空间的关键区域时，离线损失可能引入偏差
- 动态系数 $\xi$ 的门控逻辑基于批次内成功轨迹的计数，在批次规模较小或任务难度分布不均时，阈值 $\hat{R}$ 的选择可能影响训练的稳定性
- 当前验证仅基于 Qwen2.5-VL-7B 单一架构，方法在其他基座模型（如不同规模、不同视觉编码器）上的迁移效果尚不明确

### 4. 局限与开放问题

**已知局限**（原文明确讨论或可从实验中推断）：

1. **专家数据依赖**：AHPO 的训练需要 MM-HELIX-100K 数据集，该数据集通过 SERG 流水线（规则骨架 + Qwen3-235B 精炼 + 验证器筛选）生成，涉及额外的计算资源（约 27.8 小时推理时间）和复杂的多阶段生成流程，可能限制小规模团队的复现性。

2. **任务覆盖范围**：MM-HELIX 基准的 42 个任务集中于图、谜题、算法和游戏等结构化领域，对真实世界多模态场景（如自然图像理解、开放域视觉对话、视频推理）的反思能力评估尚不充分。从 Table 1 的模态差距（纯文本性能显著优于多模态性能）来看，视觉编码与推理模块的协同仍有较大提升空间。

3. **超参数敏感性**：自适应系数 $\xi$ 依赖于预设的成功阈值 $\hat{R}$，原文未详细讨论该阈值的选择策略及其在不同任务难度分布下的鲁棒性。消融实验（Table 5）显示，仅使用 MM-HELIX 数据训练时，MathVerse-V 性能相比基线略有下降，表明域内-域外数据混合比例对泛化性能存在影响，但未系统研究。

4. **架构验证单一**：所有实验基于 Qwen2.5-VL-7B，未验证方法在更大规模模型（如 72B）、不同视觉编码器架构或纯文本 LLM 上的效果。

**开放问题**（从实验现象中提炼，原文未给出答案）：

1. **灾难性遗忘的避免机制**：SFT 阶段导致对一般推理任务的性能退化，而 AHPO 仅通过动态混合损失就有效避免了这一现象。其内在机制是什么？是离线损失的动态关闭保护了策略的探索多样性，还是在线策略梯度本身具有对分布偏移的鲁棒性？

2. **表示层面的技能泛化**：AHPO 中探索与监督的动态切换究竟以何种方式塑造了策略的表示空间？模型从 MM-HELIX 的结构化反思任务中学到的“回溯”与“迭代验证”能力，如何在表示层面迁移到数学证明（WeMath）或逻辑推理（LogicVista）等不同格式的任务？

3. **模态差距的根源**：MM-HELIX 基准中纯文本与多模态输入之间存在显著的性能差距（如 GPT-5 从 58.1% 跃升至 84.5%）。这一差距的根本原因是视觉编码的信息损失、跨模态注意力对齐不足，还是多模态输入增加了推理链的长度与复杂度？

4. **自适应阈值的优化**：$\hat{R}$ 的固定设定是否最优？能否根据训练进度或任务难度自适应调整阈值，例如从保守（低阈值，频繁激活专家）逐渐过渡到激进（高阈值，鼓励自主探索），以进一步提升训练效率与最终性能？

5. **更广泛任务的迁移深度**：从 MM-HELIX 学得的反思能力能否迁移到非结构化的多模态任务（如自然图像问答、视频时序推理）？如何设计评估协议来度量这种迁移的深度——是表面格式的模仿，还是深层推理模式的泛化？

## 原文 PDF

![[paperPDFs/ICLR_2026/MM_HELIX_Boosting_Multimodal_Long_Chain_Reflective_Reasoning_with_Holistic_Platform_and_Adaptive_Hybrid_Policy_Optimization.pdf]]
