---
title: "Don't Settle Too Early: Self-Reflective Remasking for Diffusion Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Dont_Settle_Too_Early_Self_Reflective_Remasking_for_Diffusion_Language_Models.pdf
openreview_forum_id: BsZeTuB5fD
aliases:
- RREDLM
- DTSTESRRDLM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入自反思重掩码（remasking）机制，使模型能够在扩散过程中基于令牌置信度主动识别低质量令牌并将其重掩码，从而在后续步骤中利用更丰富上下文重新采样。"
primary_logic: "通过双流架构（TPS+UPS）联合建模令牌分布与置信度评分，并设计两阶段训练流程（Remask SFT 教模型检测和重掩码错误令牌，Remask RL 优化完整生成轨迹），赋予 DLM 自我修正的能力。"
claims:
- "RemeDi 联合预测令牌分布和逐令牌置信度，低置信度令牌会被重掩码以在后续步骤中重新采样。"
- "两阶段训练流水线（Remask SFT + Remask RL）使模型具备自反思式错误修正能力。"
- "RemeDi 在多个基准上刷新开源 DLM 最优结果，例如 GSM8K 89.1%、MATH 52.9%。"
- "Remask SFT 在所有基准上均优于 Vanilla SFT，尤其在 MATH-500（+2.6%）和 HumanEval（+1.8%）上。"
---

# Don't Settle Too Early: Self-Reflective Remasking for Diffusion Language Models

> [!tip] 核心洞察
> 通过双流架构（TPS+UPS）联合建模令牌分布与置信度评分，并设计两阶段训练流程（Remask SFT 教模型检测和重掩码错误令牌，Remask RL 优化完整生成轨迹），赋予 DLM 自我修正的能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 勿过早定局：面向扩散语言模型的自反思重掩码方法 |
| 英文题名 | Don't Settle Too Early: Self-Reflective Remasking for Diffusion Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=BsZeTuB5fD); [GitHub](https://github.com/maple-research-lab/RemeDi) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | RemeDi (Remasking-enabled Diffusion Language Model) |
| Dataset | GSM8K, MATH, HumanEval, ARC-C |

> [!tip] 效果简介
> - GSM8K 上，Accuracy (%) 为 89.1，对比 88.1 (LLaDOU)，变化 +1.0。
> - MATH 上，Accuracy (%) 为 52.9，对比 49.6 (Dream)，变化 +3.3。
> - HumanEval 上，pass@1 (%) 为 73.2，对比 59.8 (Dream)，变化 +13.4。

## 概述

扩散语言模型（DLM）通过逐步去噪生成文本，在数学推理与代码生成等任务上展现出潜力。然而，现有掩码式 DLM 存在一个关键瓶颈：**一旦令牌被解码（unmask），便永久固定，模型缺乏识别并修正早期错误的能力**，导致错误随生成步骤累积，严重制约生成质量。

针对这一问题，本文提出 **RemeDi（Remasking-enabled Diffusion Language Model）**，核心思路是赋予 DLM **自反思重掩码（self-reflective remasking）** 能力。具体而言，RemeDi 在每个扩散步同时预测令牌分布与逐令牌置信度，高置信度令牌被解码，低置信度令牌则被重掩码，以便在后续步骤中利用更丰富的上下文重新采样。为实现这一机制，RemeDi 采用**双流架构**——令牌预测流（TPS）负责预测令牌，解码策略流（UPS）负责估计置信度——并设计**两阶段训练流程**：Remask SFT 教模型检测并重掩码错误令牌，Remask RL 则通过基于结果的强化学习（GRPO）优化完整生成轨迹。

实验结果表明，RemeDi 在多个基准上刷新了开源 DLM 的最优结果：GSM8K 达 89.1%，MATH 达 52.9%，HumanEval pass@1 达 73.2%，较此前最佳 DLM 分别提升 +1.0、+3.3、+13.4 个百分点。在通用任务上，IFEval 和 AlpacaEval 分别取得 85.4% 和 24.8% 的胜率，显著优于 LLaDA 1.5 等基线。消融实验进一步验证：Remask SFT 在所有基准上均优于标准 SFT，Remask RL 收敛更快且最终奖励更高，学习到的重掩码策略也显著优于随机重掩码或预测器-校正器方案。

**方法定位**：RemeDi 属于掩码式扩散语言模型，以 **LLaDA**（Nie et al., 2025）为骨干，与 **Dream**（Ye et al., 2025）、**LLaDOU**（Huang et al., 2025）、**ReMDM**（Wang et al., 2025a）等同期工作并列，但在生成过程中引入可学习的自反思修正机制，是对 DLM 推理范式的重要改进。

## 背景与动机

扩散语言模型（Diffusion Language Models, DLMs）作为自回归语言模型之外的另一类生成范式，通过迭代去噪过程生成文本，天然支持非自回归的并行解码，在推理效率和可控生成方面展现出潜力。当前主流的掩码式 DLM（如 **LLaDA**、**Dream**）遵循一个基本假设：在生成过程中，一旦某个位置的令牌被解码（unmask），其值便永久固定，不再参与后续的修正。这一设计虽简化了生成流程，却引入了一个根本性缺陷——**模型缺乏识别并修正早期错误的能力**。

在分块逐步生成（block-by-block generation）的典型场景中，模型在早期步骤可用的上下文信息相对稀疏，此时做出的令牌预测可能并非最优。随着后续步骤揭示更丰富的上下文，早期错误会随生成链逐级累积，最终导致输出质量显著下降。这一“错误冻结”问题在数学推理、代码生成等对精度要求极高的任务中尤为突出，成为制约 DLM 性能进一步提升的关键瓶颈。

针对上述问题，已有部分工作尝试引入修正机制。例如 **Seed Diffusion** 通过随机重掩码已解码令牌来实现“修订”，但其重掩码策略是盲目的——不区分令牌质量高低，缺乏对错误位置的主动感知。**ReMDM** 提出了预测-校正（predictor-corrector）的重掩码采样器，但其重掩码决策仍依赖于启发式规则，未能从数据中学习何时以及何处需要修正。

本文的核心动机在于：**赋予扩散语言模型“自反思”（self-reflection）的能力**，使其能够在生成过程中主动评估已解码令牌的置信度，识别低质量令牌并将其重掩码，从而在后续步骤中利用更丰富的上下文重新采样。这一思路将 DLM 的生成过程从单向的“掩码→解码”转变为具备自我纠错能力的“掩码→解码→反思→重掩码→重新解码”循环，有望从根本上缓解错误累积问题。

## 核心创新

### 瓶颈诊断：从“一步定终身”到自我修正

现有掩码式扩散语言模型（如 **LLaDA**、**Dream**）在生成过程中遵循一个刚性规则：一旦某个掩码位置的令牌被解码（unmask），它便永久固定，后续步骤不再允许修改。这一“过早定局”的机制带来了根本性缺陷——模型缺乏识别并修正早期错误的能力。由于扩散生成是一个逐步降噪的过程，早期步骤的上下文信息相对贫乏，模型此时做出的错误预测会随着生成链向后传播并不断积累，最终严重制约输出质量。

RemeDi 的核心突破在于打破这一刚性约束，赋予扩散语言模型**自反思（self-reflective）**的能力。其关键因果旋钮是引入**重掩码（remasking）**机制：在每一步扩散过程中，模型不仅预测哪些掩码位置应该被解码，还同时评估已解码令牌的置信度，主动识别低质量令牌并将其重新置为掩码状态，使其能在后续步骤中利用更丰富的上下文被重新采样。这一机制将扩散生成从单向的“掩码→解码”过程转变为“解码→反思→修正”的闭环。

### 架构变革：双流设计实现联合预测

为实现上述自反思机制，RemeDi 对标准扩散语言模型的架构进行了根本性改造，将单一 Transformer 解码流扩展为**双流架构（dual-stream architecture）**，如图 2 所示：

- **令牌预测流（Token Prediction Stream, TPS）**：继承标准扩散模型的职责，预测掩码位置的令牌概率分布 $p_\theta^i(x_0^i | x_t)$。
- **掩码策略流（Unmasking Policy Stream, UPS）**：这是 RemeDi 的核心新增组件，负责为每个位置预测一个置信度分数 $h_\theta^i$，模型据此决定哪些位置应被解码、哪些应被重掩码。

两个流共享底层表示但拥有独立的输出头，通过 bi-residual 连接和 zero-init 桥进行信息交互。消融实验证实，移除这些连接机制会导致性能明显下降（Table 10），验证了双流协同设计的必要性。

### 训练范式的系统性重构

RemeDi 的训练体系从噪声设计、损失函数到后训练阶段进行了全面革新，形成两阶段训练流水线：

**第一阶段：Remask SFT（自反思监督微调）**

传统扩散模型的 SFT 仅对输入施加单一的掩码噪声。RemeDi 引入了**双重噪声机制**：
- **掩码噪声**：随机将令牌替换为 `[M]`，模拟标准扩散过程。
- **错误令牌噪声**：随机将令牌替换为错误的替代词，模拟模型在生成过程中可能产生的错误预测。

关键设计在于噪声比例的单调递减约束（Eq. 3）：
$$\left\lceil \rho_{t,\mathrm{incorrect}} \cdot (1 - \rho_{t,\mathrm{mask}}) \cdot L \right\rceil < \left\lceil \rho_{t,\mathrm{mask}} \cdot L \right\rceil$$

该约束确保经过重掩码后，序列中的掩码令牌总数保持单调递减，符合扩散模型的降噪本质。

训练目标也相应扩展，从单一的扩散损失变为联合优化（Eq. 5）：
$$\mathcal{L}(\theta) = \mathcal{L}_{\mathrm{diffusion}}(\theta) + \lambda_{\mathrm{UPS}} \mathcal{L}_{\mathrm{UPS}}(\theta)$$

其中 $\mathcal{L}_{\mathrm{UPS}}$ 为二元交叉熵损失（Eq. 4），监督信号是软标签 $y^i = p_\theta^i(x_0^i | x_t)$——即当前模型预测真实令牌的概率。这一设计使 UPS 学会判断：高概率对应“应保持 unmask”，低概率对应“应重掩码”。

**第二阶段：Remask RL（自反思强化学习）**

在 Remask SFT 基础上，RemeDi 进一步引入基于结果的强化学习，使用 GRPO 优化完整生成轨迹。其核心创新在于将 unmask 位置的选择建模为可优化的策略：使用 Plackett-Luce 模型依置信度分数顺序采样要解码的位置（Eq. 6），将单步转移概率分解为位置选择策略与令牌预测策略的乘积（Eq. 8）：
$$\pi_{\theta,n}(x_{t_n} | x_{t_{n-1}}) = \pi_{\theta,n}^{\mathrm{unmask}}(\mathcal{U}_n | x_{t_{n-1}}) \cdot \pi_{\theta,n}^{\mathrm{token}}(x_{t_n} | x_{t_{n-1}}, \mathcal{U}_n)$$

### 创新总结：五个关键 changed slots

| 维度 | 基线方法 | RemeDi 方案 | 证据锚点 |
|------|----------|-------------|----------|
| 模型架构 | 单一 Transformer 解码流 | 双流架构（TPS + UPS），UPS 生成逐令牌置信度 | Sec 3.2, Fig. 2 |
| 训练噪声 | 仅掩码噪声 | 掩码噪声 + 随机错误令牌噪声，满足单调递减约束 | Sec 3.2.1, Eq. (3) |
| 损失函数 | 仅掩码位置扩散损失 | 扩散损失 + UPS 二元交叉熵联合优化 | Sec 3.2.1, Eq. (4)-(5) |
| 推理状态更新 | 已解码令牌永久固定 | 每步依置信度决定 unmask 或 remask，低置信度令牌可重新采样 | Sec 3.2, Fig. 1a |
| 后训练阶段 | 无（仅 SFT） | 基于 GRPO 的 Remask RL，优化完整生成轨迹 | Sec 3.2.2, Eq. (6)-(8) |

这些变革并非孤立的技术叠加，而是围绕“自反思修正”这一核心洞察的系统性重构：双流架构提供了置信度评估的硬件基础，双重噪声和联合损失教会模型识别错误，RL 阶段则优化了修正策略的全局效果。消融实验有力支撑了这一设计的有效性——Remask SFT 在所有基准上均优于 Vanilla SFT，尤其在 MATH-500（+2.6%）和 HumanEval（+1.8%）上（Table 4）；Remask RL 相比 LLaDOU RL 收敛更快且最终奖励更高（Table 5, Fig. 15）。

## 整体框架

RemeDi 的核心设计围绕一个双流 Transformer 架构展开，该架构由**令牌预测流（Token Prediction Stream, TPS）**和**去掩码策略流（Unmasking Policy Stream, UPS）**组成（Fig. 2）。TPS 负责在每一个扩散步中预测掩码位置的令牌概率分布，而 UPS 则独立地生成每个位置的置信度分数 $h_{\theta}^i$，用于决定哪些位置应当被去掩码（unmask），哪些位置应当被重掩码（remask），从而赋予模型在生成过程中主动识别并修正早期错误的能力。

整个训练与推理流程可概括为以下阶段：

1.  **基础模型适配**：以 **LLaDA-8B-Instruct**（Nie et al., 2025）为骨干，将其改造为支持可变长度分块生成（block-by-block generation）的扩散语言模型，作为重掩码机制的运行基础。
2.  **Remask SFT（监督微调）**：在此阶段，模型输入被同时注入两种噪声——标准的掩码噪声（mask noise）和随机替换的错误令牌噪声（incorrect token noise）。模型被联合训练以完成两个目标：
    *   TPS 恢复被掩码的令牌（标准扩散损失 $\mathcal{L}_{\mathrm{diffusion}}$）。
    *   UPS 判断每个已去掩码的令牌是否应被重掩码（二元交叉熵损失 $\mathcal{L}_{\mathrm{UPS}}$）。
    总损失函数为 $\mathcal{L}(\theta) = \mathcal{L}_{\mathrm{diffusion}}(\theta) + \lambda_{\mathrm{UPS}} \mathcal{L}_{\mathrm{UPS}}(\theta)$。通过这一阶段，模型学会了检测并重掩码低质量令牌。
3.  **Remask RL（强化学习）**：在 SFT 基础上，采用基于结果的强化学习（GRPO）对整个生成轨迹进行优化。该阶段使用 Plackett-Luce 模型依据 UPS 的置信度分数来采样去掩码位置，直接以最终生成质量（如数学答案的正确性）作为奖励信号，进一步提升模型的自修正能力。

在推理时，RemeDi 的每一步生成均遵循“预测-评估-重掩码”循环：TPS 为所有掩码位置预测候选令牌，UPS 为序列中所有位置（包括已去掩码的）计算置信度。高置信度的掩码位置被去掩码，而低置信度的已去掩码令牌则被重新置为掩码状态，使其能在后续步骤中利用更丰富的上下文信息被重新采样，从而打破传统扩散语言模型“一旦解码便永久固定”的限制（Fig. 1a）。

## 核心模块与公式推导

### 双流架构：TPS 与 UPS

RemeDi 将标准 Transformer 扩展为双流架构（Fig. 2），包含两个并行流：

- **TPS（Token Prediction Stream）**：标准扩散语言模型的解码流，在每步预测掩码位置的令牌概率分布 $p_\theta^i(x_0^i \mid x_t)$，决定被 unmask 的令牌应取何值。
- **UPS（Unmasking Policy Stream）**：新增的置信度预测流，为每个位置 $i$ 输出标量隐藏状态 $h_{\theta,n}^i$，经 sigmoid 后得到逐令牌置信度分数 $\sigma(h_\theta^i)$，用于决定哪些位置应被 unmask 或 remask。

两流共享底层表示，但 UPS 通过 bi-residual 连接和 zero-init 桥与 TPS 交互，消融实验（Table 10）表明移除这些连接会明显降低性能。

---

### Remask SFT 训练

#### 噪声构造

Remask SFT 的核心创新在于引入两种噪声模拟扩散中间状态：

1. **掩码噪声**：以比例 $\rho_{t,\text{mask}}$ 将令牌替换为 $[\mathbf{M}]$。
2. **错误令牌噪声**：以比例 $\rho_{t,\text{incorrect}}$ 将令牌替换为随机错误令牌，模拟模型早期生成的错误。

两种噪声比例需满足单调递减约束，确保经 remask 后掩码总数减少：

$$\left\lceil \rho_{t,\text{incorrect}} \cdot (1 - \rho_{t,\text{mask}}) \cdot L \right\rceil < \left\lceil \rho_{t,\text{mask}} \cdot L \right\rceil \tag{Eq. 3}$$

其中 $L$ 为序列长度。该约束保证扩散过程的降噪单调性。

#### 损失函数

**扩散损失**（仅计算掩码位置）：

$$\mathcal{L}_{\text{diffusion}}(\theta) = \mathbb{E}_{t,x_0,x_t} \bigg[ -\frac{1}{t} \sum_{i=1}^{L} \mathbf{1}(x_t^i = [\mathbf{M}]) \log p_\theta^i(x_0^i \mid x_t) \bigg] \tag{Eq. 2}$$

**UPS 损失**：对每个位置，UPS 需判断该令牌应保持 unmask（$y^i=1$）还是应 remask（$y^i=0$）。标签 $y^i$ 为软标签，取值为 TPS 对真值令牌的预测概率 $p_\theta^i(x_0^i \mid x_t)$：

$$\mathcal{L}_{\text{UPS}}(\theta) = \sum_i \text{BCE}\big(\sigma(h_\theta^i), y^i\big) \tag{Eq. 4}$$

**总损失**：

$$\mathcal{L}(\theta) = \mathcal{L}_{\text{diffusion}}(\theta) + \lambda_{\text{UPS}} \mathcal{L}_{\text{UPS}}(\theta) \tag{Eq. 5}$$

联合优化使模型同时学会预测掩码令牌和识别应被重掩码的错误令牌。

---

### Remask RL 训练

在 Remask SFT 后，使用基于结果的强化学习（GRPO）优化完整生成轨迹。

**Unmasking 位置采样**：采用 Plackett-Luce 模型，依 UPS 置信度分数 $h_{\theta,n}^j$ 顺序采样要 unmask 的位置子集 $\mathcal{U}_n$：

$$\pi_{\theta,n}^{\text{unmask}}(\mathcal{U}_n \mid x_{t_{n-1}}) = \prod_{k=1}^{K_n} \frac{\exp(h_{\theta,n}^{u_n(k)})}{\sum_{j \notin \{u_n(1),\dots,u_n(k-1)\}} \exp(h_{\theta,n}^j)} \tag{Eq. 6}$$

**联合转移概率**：单步扩散状态转移由位置选择和令牌预测共同决定：

$$\pi_{\theta,n}(x_{t_n} \mid x_{t_{n-1}}) = \pi_{\theta,n}^{\text{unmask}}(\mathcal{U}_n \mid x_{t_{n-1}}) \cdot \pi_{\theta,n}^{\text{token}}(x_{t_n} \mid x_{t_{n-1}}, \mathcal{U}_n) \tag{Eq. 8}$$

RL 阶段使模型在 GSM8K 上收敛更快且最终奖励高于 LLaDOU RL（Fig. 15, Table 5），验证了联合优化生成轨迹的有效性。

## 实验与分析

### 核心结果：RemeDi 在数学、代码与通用任务上全面刷新开源 DLM 最优水平

RemeDi 在数学推理、代码生成和通用任务基准上均取得开源扩散语言模型（DLM）中的最优结果，且两阶段训练（Remask SFT → Remask RL）带来的提升具有一致性与累积性。

**数学与代码生成**（Table 1）：经过 Remask RL 后，RemeDi 在 GSM8K 上达到 **89.1%**，在 MATH 上达到 **52.9%**，分别超出此前最优 DLM **LLaDOU**（88.1%）和 **Dream**（49.6%）1.0 和 3.3 个百分点。在代码生成任务上，HumanEval pass@1 达到 **73.2%**，较 Dream（59.8%）提升 13.4 个百分点；MBPP 达到 59.4%，同样显著领先。值得注意的是，仅经过 Remask SFT（未做 RL）的模型已在 GSM8K（86.3%）和 MATH（51.4%）上超越多数 DLM 基线，表明重掩码机制本身已带来实质性增益。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/004_Table_1.jpg]]
*Table 1: Model performance on math and code generation benchmarks. We highlight the bestperforming model among compared DLMs in bold. “-” indicates unknown cases not mentioned in original papers*

**通用任务**（Table 2）：RemeDi 在 ARC-C（87.7%）、IFEval（85.4%）和 AlpacaEval（胜率 24.8%）上均大幅领先已有 DLM。与 LLaDA 1.5 相比，IFEval 提升 11.9 个百分点，AlpacaEval 胜率提升 10.9 个百分点，说明自反思重掩码对指令遵循和开放生成质量同样有效。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/005_Table_2.jpg]]
*Table 2: Model performance on general tasks. We highlight the best-performing model among compared DLMs in bold. “-” indicates unknown cases not mentioned in original papers*

**推理效率与精度的平滑权衡**（Figure 14）：通过调节每步解码令牌数（1/2/4 tok/step），RemeDi 在 GSM8K 精度与吞吐量之间形成帕累托前沿——在吞吐量远超自回归模型（如 DeepSeekMath、MetaMath）的同时，精度仍保持领先。这一特性使 RemeDi 在实际部署中可按需配置延迟-质量平衡点。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/028_Figure_14.jpg]]
*Figure 14: Throughput–performance trade-off of RemeDi compared with other AR and DLM models. By increasing the number of denoised tokens per step, RemeDi provides a smooth quality–latency trade-off. All results are measured with batch size 1 and sequence length 1024 on a single H800 GPU*

### 消融实验：重掩码机制与两阶段训练各自贡献明确

消融实验从训练策略、采样器选择、架构设计三个维度验证了 RemeDi 各组件的必要性。

**Remask SFT vs. Vanilla SFT**（Table 4）：在统一的基础模型上，Remask SFT 在所有基准上均优于标准 SFT，尤其在 MATH-500（+2.6%）和 HumanEval（+1.8%）上。这表明让模型显式学习识别和重掩码错误令牌，比单纯扩大 SFT 数据量更有效。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/010_Table_4.jpg]]
*Table 4: Experiment results after supervised tuning with different algorithms. The baseline model is already tuned to be a variable-length block-wise generation DLM (see Appendix B.2.2)*

**Remask RL vs. LLaDOU RL**（Table 5, Figure 15）：在完全相同的 RL 超参数和基础模型下，Remask RL 在 GSM8K 上收敛更快且最终奖励更高。Figure 15 的奖励曲线显示，Remask RL 在约第 20 步即超越 LLaDOU RL，并持续保持优势，最终 pass@1 精度也相应更高。匹配计算量消融（Table 9）进一步证明，Remask RL 优于将同等算力投入额外 SFT 训练，排除了“RL 增益仅来自更多训练”的替代解释。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/011_Table_5.jpg]]
*Table 5: GSM8K pass@1 accuracy comparison between Remask and LLaDOU RL*

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/022_Table_9.jpg]]
*Table 9: Matched-compute ablation between extra SFT training and Remask RL*

**Remask 采样器的关键作用**（Table 8）：在相同 Remask SFT 模型上，Remask 采样器在 MATH-500、HumanEval、IFEval 上显著优于传统半自回归采样器和自适应采样器。这说明推理时的自反思重掩码策略——而非仅训练阶段的改进——是性能提升的直接原因。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/021_Table_8.jpg]]
*Table 8: Effect of different samplers under the same Remask SFT model*

**UPS 架构设计**（Table 10）：移除 UPS 的 bi-residual 连接或 zero-init 桥均导致 GSM8K 精度大幅下降（分别降至 78.6% 和 79.7%，对比基线 83.6%），验证了双流架构中信息融合设计对置信度预测质量的关键影响。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/023_Table_10.jpg]]
*Table 10: UPS structure ablations. Removing either the bi-residual connections or the zero-init bridge degrades performance*

**与 Seed Diffusion 的对比**（Table 6）：RemeDi 的显式重掩码策略始终优于 Seed Diffusion 的隐式修正方法，证明学习明确的“检测-重掩码-重采样”策略优于依赖扩散过程本身的随机修正。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/019_Table_6.jpg]]
*Table 6: Unified head-to-head comparison with other training algorithms under identical settings*

### 重掩码行为的任务依赖性分析

重掩码频率在不同任务间呈现显著差异（Figure 4, Table 3）。代码生成（HumanEval）中每个令牌平均被重掩码次数最高，数学推理（GSM8K、MATH-500）次之，开放式问答（AlpacaEval）最低。在 MATH-500 内部，随着题目难度从 Level 1 升至 Level 5，平均重掩码频率单调递增（Table 3），表明模型自适应地在更复杂问题上进行更多自我修正。这一行为模式与重掩码机制的设计直觉一致：当生成任务需要更精细的推理时，早期错误更可能被后续上下文暴露，触发更多的重掩码操作。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/009_Table_3.jpg]]
*Table 3: Statistics of the remasking frequencies per block (block size is fixed to 32) when generating responses to questions with different difficulty levels in MATH-500*

经过 Remask RL 后，重掩码频率进一步上升（Table 11），同时精度同步提升——RL 训练使模型在 GSM8K 上重掩码频率从 0.45 升至 0.78，HumanEval 从 0.82 升至 1.15。这说明 RL 优化了“何时重掩码”的决策质量，而非简单地减少修正次数。

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/024_Table_11.jpg]]
*Table 11: Average remask frequency (ARF) and performance across tasks. ARF measures how many times each token is remasked on average during decoding*

### 局限与待验证问题

论文未设专门局限性章节，但从实验设置和结果可推断以下边界：

1. **训练成本与模型复杂度**：双流架构（TPS + UPS）和额外的 Remask RL 阶段增加了训练开销。当前实验基于 LLaDA-8B，在更大规模模型（如 70B+）上的扩展性尚未验证。
2. **任务适用性边界**：重掩码在代码和数学任务上收益最大，在开放式文本生成上频率较低，暗示该方法对需要精确推理的任务更有效，对自由文本生成的增益可能有限。
3. **多语言与低资源场景**：所有实验均在英文基准上进行，未讨论跨语言迁移能力。
4. **生成多样性与事实一致性**：重掩码机制对生成多样性和幻觉率的影响缺乏系统评估，需后续研究补充。

### 补充图表

![[assets/figures/papers/paper_list_l48_https_openreview_net_forum_id_BsZeTuB5fD/figures/020_Table_7.jpg]]
*Table 7: Comparison between our learned remask policy in RemeDi and the ReMDM predictorcorrector, both evaluated with RemeDi-Instruct*

## 方法谱系与知识库定位

### 1. 方法在现有 DLM 谱系中的位置

RemeDi 的核心贡献在于为掩码式扩散语言模型（DLM）引入**自反思式错误修正能力**，其技术路线与现有工作形成以下关系：

**与基础 DLM 的关系**：RemeDi 直接构建在 **LLaDA**（Nie et al., 2025）之上，将其改造为支持可变长度逐块生成的骨干模型。与 **Dream**（Ye et al., 2025）和 **LLaDA 1.5**（Zhu et al., 2025）等后续改进版 DLM 相比，RemeDi 的根本区别不在于基础扩散框架，而在于**生成过程中的令牌状态管理机制**——传统 DLM 中令牌一旦解码（unmask）便永久固定，RemeDi 则允许模型根据置信度主动回退并修正早期错误。

**与 DLM + RL 方法的关系**：**LLaDOU**（Huang et al., 2025）同样在 DLM 上引入强化学习优化生成质量，但其 RL 阶段作用于标准的固定令牌生成过程。RemeDi 的 Remask RL 在两点上形成差异：（1）RL 优化的是包含重掩码动作的完整生成轨迹，而非简单的逐步解码链；（2）消融实验（Table 5, Figure 15）表明，在相同 RL 超参数和基础模型下，Remask RL 收敛更快且最终奖励更高，说明重掩码机制本身为 RL 提供了更丰富的优化空间。

**与其他修正型 DLM 的关系**：**Seed Diffusion**（Song et al., 2025）和 **ReMDM**（Wang et al., 2025a）也探索了 DLM 中的修正能力。Seed Diffusion 采用替代性的修正策略，而 RemeDi 的 Remask SFT 在所有基准上始终优于 Seed Diffusion（Table 6），验证了**显式学习重掩码策略**相比隐式修正的优势。ReMDM 提出的 predictor-corrector 采样器与 RemeDi 的重掩码采样器思路相近，但 RemeDi 将重掩码判断内化为模型自身的 UPS 流输出，而非外部采样器规则。

### 2. 技术瓶颈与因果机制

**核心瓶颈**：现有掩码式 DLM 的生成过程存在**错误不可逆**问题——早期步骤中基于不完整上下文作出的令牌预测，即使后续步骤获得更丰富信息后被发现是错误的，也无法修正。这导致错误沿生成链累积，严重制约最终输出质量。

**因果调节变量**：RemeDi 通过引入**逐令牌置信度评分**作为可操作的调节变量，使模型能够在每一步主动识别"低质量令牌"并触发重掩码。这一机制的关键在于：

1. **双流架构（TPS + UPS）** 将令牌预测与置信度评估解耦，UPS 专门学习判断令牌在当前上下文下的可靠性，而非简单地复用 TPS 的预测概率。
2. **两阶段训练** 赋予模型完整的自反思能力：Remask SFT 教模型"检测并重掩码错误"，Remask RL 教模型"优化包含修正的完整生成策略"。
3. **噪声设计** 中的单调递减约束（Eq. 3）确保重掩码后的序列仍符合扩散模型的降噪特性，避免破坏生成过程的数学基础。

### 3. 适用边界与局限性

**任务依赖性**：重掩码的有效性与任务类型显著相关。实验数据（Figure 4）显示，代码生成（HumanEval）中每块平均重掩码频率最高（28.52 ± 12.04），数学推理（MATH-500）次之（11.81 ± 10.23），开放式问答（AlpacaEval）最低（2.78 ± 5.33）。这表明该方法在**结构化推理任务**（数学、代码）上优势更明显，而在自由文本生成上的增益可能有限。难度分层分析（Table 3）进一步显示，MATH-500 中高难度问题的重掩码频率更高，暗示模型在面临更大不确定性时更依赖修正机制。

**计算成本**：论文未设专门局限性章节，但可从方法设计推断以下约束：
- 双流架构增加了模型参数和推理时的计算开销。
- Remask RL 阶段需要采样完整生成轨迹并计算奖励，训练成本高于标准 SFT。
- 当前实现基于 LLaDA-8B，尚未在更大规模模型（如 70B+）上验证扩展性。

**未覆盖场景**：论文未讨论多语言生成、低资源领域适配、以及重掩码对生成多样性和事实一致性的系统影响。这些方面需要进一步验证。

### 4. 开放问题

1. **效率优化**：如何在不显著增加计算开销的前提下实施重掩码？可能的路径包括稀疏激活策略（仅对低置信度区域触发 UPS）、缓存 UPS 中间表示、或设计更轻量的置信度估计模块。

2. **跨范式迁移**：重掩码策略是否可以迁移到自回归模型或其他非扩散生成范式？自回归模型的顺序生成特性使得"回退修正"更为复杂，但置信度引导的重生成机制在原则上具有通用性。

3. **多样性与事实一致性**：重掩码本质上是一种"纠错"机制，其对生成多样性的影响（是否导致过度保守的输出）以及对事实一致性的系统影响尚待探索。

4. **大规模扩展**：该方法在 70B+ 规模模型上的扩展性和稳定性如何？双流架构在大模型下的训练稳定性和通信开销需要实证验证。

5. **更细粒度的重掩码策略**：当前重掩码基于逐令牌置信度，是否可以利用令牌间的结构依赖（如语法树、推理步骤间的逻辑关系）设计更智能的重掩码策略，进一步提升修正效率？

## 原文 PDF

![[paperPDFs/ICLR_2026/Dont_Settle_Too_Early_Self_Reflective_Remasking_for_Diffusion_Language_Models.pdf]]
