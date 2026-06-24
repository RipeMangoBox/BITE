---
title: "GPG: A Simple and Strong Reinforcement Learning Baseline for Model Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/GPG_A_Simple_and_Strong_Reinforcement_Learning_Baseline_for_Model_Reasoning.pdf
openreview_forum_id: inccdtfx8x
aliases:
- GPGG
- GPG
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过组内奖励均值归一化消除价值模型，使用精确梯度估计（AGE）校正无效样本偏差，并引入有效样本比例阈值与重采样机制以降低梯度估计方差，从而直接优化原始强化学习目标，无需替代损失和分布约束。"
primary_logic: "将组决策动态融入标准策略梯度，去除冗余组件并修正偏差，能够实现比复杂RL方法更简洁、高效且性能更优的推理模型训练。"
claims:
- "GPG直接优化原始RL目标，无需替代损失函数，并消除了批评家模型、参考模型和KL散度约束。"
- "精确梯度估计（AGE）通过重缩放梯度校正了全正确/全错误组带来的偏差，并提出阈值重采样机制以降低方差。"
- "GPG在多个单模态数学推理基准（如AIME24、MATH-500等）以及多模态视觉推理、几何推理、分类和推理定位任务上均一致优于GRPO，且训练资源消耗更低。"
- "Math Reasoning (Qwen2.5-Math-7B) 上 Average score across 5 benchmarks = 48.3 (GPG with F_norm=1, α=B/(B-M), β_th=0.6)"
---

# GPG: A Simple and Strong Reinforcement Learning Baseline for Model Reasoning

> [!tip] 核心洞察
> 将组决策动态融入标准策略梯度，去除冗余组件并修正偏差，能够实现比复杂RL方法更简洁、高效且性能更优的推理模型训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GPG：一种简单且强大的模型推理强化学习基线 |
| 英文题名 | GPG: A Simple and Strong Reinforcement Learning Baseline for Model Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=inccdtfx8x); [GitHub](https://github.com/AMAP-ML/GPG) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Group Policy Gradient (GPG) |
| Dataset | Math Reasoning (Qwen2.5-Math-7B), 1.5B Math Reasoning (DeepSeek-R1-Distill-Qwen-1.5B), 7B Math Reasoning, Geometry Reasoning (GEOQA Test) |

> [!tip] 效果简介
> - Math Reasoning (Qwen2.5-Math-7B) 上，Average score across 5 benchmarks 为 48.3 (GPG with F_norm=1, α=B/(B-M), β_th=0.6)，对比 43.7 (GRPO)，变化 +4.6。
> - 1.5B Math Reasoning (DeepSeek-R1-Distill-Qwen-1.5B) 上，Average pass@1 为 55.7 (GPG-RS1)，对比 53.1 (Open-RS1, GRPO-based)，变化 +2.6。
> - 7B Math Reasoning 上，Average pass@1 为 57.7 (GPG-Zero-7B)，对比 51.4 (Oat-Zero-7B)，变化 +6.3。

## 概述

当前基于强化学习的大语言模型推理训练方法（如 **PPO**、**GRPO**）普遍依赖替代损失函数、参考模型和价值模型，并引入 KL 散度约束以防止策略偏移。这些组件虽然在一定程度上稳定了训练，但也带来了优势估计偏差、梯度估计偏差以及显著的计算开销，限制了模型的可扩展性和性能上限。

**GPG（Group Policy Gradient）** 提出了一种更为简洁且强大的替代方案。其核心思想是：通过组内奖励均值归一化消除价值模型，利用精确梯度估计（AGE）校正无效样本带来的偏差，并引入有效样本比例阈值与重采样机制以控制梯度估计方差。这一设计使得 GPG 能够直接优化原始强化学习目标，完全摒弃替代损失、参考模型和 KL 散度约束，从而在简化训练流程的同时实现了更优的性能。

在多个基准上的实验结果一致表明，GPG 的简化设计并未牺牲性能，反而带来了显著提升：

- **单模态数学推理**：在 Qwen2.5-Math-7B 上，GPG 在五个数学基准上的平均得分达到 **48.3**，显著优于 GRPO 的 43.7（+4.6）。在 7B 规模模型上，GPG-Zero-7B 的平均 pass@1 达到 **57.7**，较 Oat-Zero-7B 的 51.4 提升 6.3 个百分点。
- **多模态推理与定位**：在视觉推理（CV-Bench）上，GPG 的总准确率达到 **76.15**，远高于 GRPO 的 59.47（+16.68）；在推理定位（LISA）上，GPG 的 mIoU 达到 **51.8**，较 GRPO 的 37.6 提升 14.2 个百分点。
- **几何推理与细粒度分类**：GPG 在 GEOQA 上达到 **51.33%**（GRPO 为 47.48%），在四个细粒度分类数据集上的平均准确率达到 **89.0%**（GRPO 为 81.9%）。

消融实验进一步揭示了 GPG 各组件的作用：精确梯度估计（AGE）是性能提升的关键，去除 AGE 后 GPG 仅取得 43.9%，与 GRPO 的 43.7% 基本持平；引入 KL 散度约束反而会损害性能；组内奖励归一化优于批次归一化；适当增大组大小可稳步提升性能，GPG 选定组大小为 8 以平衡成本与效果。

在方法谱系上，GPG 相比 **PPO**（Schulman et al., 2017）、**GRPO**（Shao et al., 2024）、**TRPO**（Schulman et al., 2015）以及 **DAPO**（Yu et al., 2025）等现有方法，移除了价值模型、参考模型、替代损失和策略约束四个组件，在保持训练稳定性的同时实现了最简形式。与 DAPO 的直接对比表明，GPG 在更简单的设计下取得了更强的性能，且资源消耗更低。

值得注意的是，GPG 当前尚未在超大模型（>70B）上进行验证，其长期训练中去除分布约束的稳定性以及 AGE 机制在极端奖励分布下的鲁棒性仍有待进一步探索。

## 背景与动机

### 推理任务中的强化学习范式

大语言模型在数学推理、几何推理、视觉推理等复杂任务上的能力提升，日益依赖于强化学习（RL）驱动的后训练优化。其核心目标可形式化为最大化期望累积奖励：

$$\mathcal{I}(\theta) = \max_\theta \mathbb{E}_{\pi_\theta} \left[ \sum_{t=0}^T r_t \right]$$

根据策略梯度定理，该目标的梯度可表达为：

$$\nabla_\theta \mathcal{I}(\theta) = \mathbb{E}_{\pi_\theta} \left[ \nabla_\theta \log \pi_\theta(a_t|s_t) Q^{\pi_\theta}(s_t,a_t) \right]$$

然而，直接应用策略梯度面临着高方差、不稳定和样本效率低等挑战。为此，主流方法引入了一系列辅助组件来缓解这些问题。

### 现有方法的冗余与偏差

当前广泛应用于推理任务的RL方法——包括 **PPO**（Schulman et al., 2017）、**GRPO**（Shao et al., 2024）及其变体（如 **Dr. GRPO**、**DAPO**）——普遍依赖以下组件：

- **替代损失函数**：PPO通过裁剪机制构造代理目标 $\mathcal{I}^{\text{CLIP}}(\theta) = \mathbb{E}_t \left[ \min \left( r_t(\theta) \hat{A}_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$，而非直接优化原始RL目标。
- **价值模型（Critic）**：用于估计状态价值 $V(s_t)$，以计算优势函数，需额外训练一个与策略模型规模相当的神经网络。
- **参考模型**：保存旧策略参数 $\pi_{\theta_{\text{old}}}$，用于计算概率比 $r_t(\theta) = \pi_\theta(a_t|s_t) / \pi_{\theta_{\text{old}}}(a_t|s_t)$ 和KL散度约束。
- **分布约束**：通过KL散度正则化限制策略更新幅度，防止策略崩溃。

这些组件的叠加带来了三重问题：

1. **训练复杂度高**：需同时维护策略模型、价值模型和参考模型，内存开销和计算成本显著增加。
2. **偏差累积**：优势估计中的奖励标准化（除以组内标准差）和替代损失对梯度的扭曲，导致优化方向偏离真实策略梯度。
3. **无效样本干扰**：在组采样中，当某问题的所有回答均正确或均错误时，该组样本对梯度估计的贡献为零，但标准反向传播仍将其纳入平均，造成梯度估计偏差。

### 核心动机

本文的核心洞察在于：**将组决策动态直接融入标准策略梯度，去除冗余组件并修正偏差，能够实现比复杂RL方法更简洁、高效且性能更优的推理模型训练**。

具体而言，GPG（Group Policy Gradient）的设计围绕三个关键突破：

- **去除冗余**：消除价值模型和参考模型，避免KL散度约束，直接优化原始RL目标，无需替代损失函数。
- **精确梯度估计（AGE）**：识别并排除全正确/全错误组对梯度计算的干扰，通过因子 $\alpha = B/(B-M)$ 对有效样本梯度进行重缩放，修正梯度估计偏差。
- **方差控制**：引入有效样本比例阈值 $\beta_{th}$ 和重采样机制，当有效样本不足时累积并重新采样，确保梯度估计的可靠性。

通过这一设计，GPG在显著降低训练资源消耗的同时，在单模态数学推理、多模态视觉推理、几何推理、细粒度分类和推理定位等广泛任务上一致超越了GRPO等现有方法。

## 核心创新

GPG的核心创新在于对强化学习训练流程的**系统性简化与偏差校正**，而非引入新的复杂组件。相较于当前主流的**GRPO**（Shao et al., 2024）和**PPO**（Schulman et al., 2017），GPG在四个关键维度上实现了结构性改变：

### 1. 损失函数：从替代目标回归原始策略梯度

PPO和GRPO均依赖**替代损失函数**（surrogate loss）来间接优化策略。PPO使用Clipped Surrogate Objective：

$$
\mathcal{I}^{\mathrm{CLIP}}(\theta) = \mathbb{E}_t \left[ \min \left( r_t(\theta) \hat{A}_t, \mathrm{clip} (r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]
$$

GRPO同样采用了基于概率比裁剪的替代损失。而GPG**直接优化原始RL目标**，使用组内优势加权的对数概率损失：

$$
\mathcal{J}_{\mathrm{GPG}}(\theta) = \mathbb{E}_{(q,a)\sim\mathcal{D},\{o_i\}_{i=1}^G} \left[ \frac{1}{\sum_{i=1}^G |o_i|} \sum_{i=1}^G \sum_{t=1}^{|o_i|} \left( -\log \pi_\theta(o_{i,t} | q, o_{i,<t}) \hat{A}_{i,t} \right) \right]
$$

这一改变消除了替代损失引入的优化偏差，使训练目标与真实RL目标完全一致（Table 2, Equation 5）。

### 2. 优势估计：去除价值模型与奖励标准化偏差

GRPO通过组内奖励的均值与标准差进行归一化来计算优势值，这引入了**奖励标准化偏差**——当组内奖励方差较小时，优势估计被不当放大。GPG的优势函数仅使用组内均值归一化，且默认不做标准差缩放（$F_{norm}=1$）：

$$
\hat{A}_{i,t} = \frac{r_i - \mathrm{mean}(\{R_i\}_{i=1}^G)}{F_{norm}}
$$

这一设计使得GPG**完全消除了对价值模型（critic）的依赖**，同时避免了标准化引入的偏差。消融实验证实，组内奖励归一化优于批次归一化（Average 45.3 vs 44.9），而添加KL散度约束则反而损害性能（Table 13）。

### 3. 梯度估计：AGE校正无效样本偏差

这是GPG最关键的创新。在组采样中，当某个问题的所有回答全对或全错时，该组对梯度更新的贡献为零，导致有效样本量减少、梯度估计产生系统性偏差。GPG提出**精确梯度估计**（Accurate Gradient Estimation, AGE），通过重缩放因子 $\alpha = \frac{B}{B-M}$ 校正梯度：

$$
\hat{\bf g} = \frac{\sum_{i=M+1}^B {\bf g_i}}{B-M} = {\bf g} \frac{B}{B-M} = \alpha {\bf g}
$$

其中 $B$ 为总组数，$M$ 为全正确/全错误组数。AGE从数学上修正了无效样本带来的梯度低估问题（Equation 7, Section 2.2）。实验证据表明，AGE是GPG性能提升的决定性因素：无AGE时GPG仅达43.9%，与GRPO的43.7%几乎持平；加入AGE后跃升至47.8%（Table 1）。

### 4. 训练稳定性：以重采样替代分布约束

PPO和GRPO均使用**KL散度约束**或裁剪机制来限制策略更新幅度，防止训练不稳定。GPG则完全移除了参考模型和分布约束，转而通过**有效样本比例阈值与重采样机制**来控制梯度估计方差：当有效样本比例低于阈值 $\beta_{th} = \frac{1}{\alpha_{th}}$ 时，累积有效样本并重新采样，确保每次更新的梯度估计方差可控（Section 2.2）。消融实验表明 $\beta_{th}=0.8$ 时取得最佳平均分48.6（Table 10），验证了该机制的有效性。

### 方法对比总览

| 组件 | PPO | GRPO | TRPO | **GPG** |
|------|-----|------|------|---------|
| 价值模型 | ✓ | ✗ | ✓ | **✗** |
| 参考模型 | ✓ | ✓ | ✗ | **✗** |
| 替代损失 | ✓ | ✓ | ✓ | **✗** |
| 策略约束 | ✓ | ✓ | ✓ | **✗** |

GPG是唯一同时去除全部四个冗余组件的方案（Table 2），在保持训练稳定性的同时实现了显著的性能提升和资源节约。

## 整体框架

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/006_Table_2.jpg]]
*Table 2: Comparison of reinforcement learning algorithms (in reasoning) with various components*

GPG 的整体训练流水线围绕**组采样 → 组内优势计算 → 精确梯度估计 → 策略更新**四个核心阶段展开，其设计哲学是**直接优化原始强化学习目标**，去除替代损失函数、价值模型、参考模型和 KL 散度约束等传统 RL 方法中常见的冗余组件。

### 核心模块与数据流

1. **策略大语言模型（Policy LLM π_θ）**：作为推理生成的主体，对每个输入问题 $q$ 生成回答序列 $o$，并输出每个 token 的对数概率 $\log \pi_\theta(o_{i,t} \mid q, o_{i,<t})$。该模块是唯一需要训练的参数化组件。

2. **组采样与奖励收集**：对每个问题独立采样一组 $G$ 个回答 $\{o_i\}_{i=1}^G$，由奖励模型或基于规则的验证器（如答案匹配）返回**仅有的最终奖励信号** $r_i$。GPG 将问题简化为仅使用最终奖励，不依赖过程奖励或中间步骤的价值估计。

3. **组内优势计算**：利用组内奖励均值进行归一化，计算每个回答的 token 级优势值：
   $$\hat{A}_{i,t} = \frac{r_i - \mathrm{mean}(\{R_i\}_{i=1}^G)}{F_{norm}}$$
   其中 $F_{norm}=1$（即不做标准差归一化），仅通过组内均值中心化来消除对价值模型的依赖，同时有效降低方差。

4. **精确梯度估计（AGE）**：这是 GPG 区别于 GRPO 等方法的**关键校正模块**。当组内所有回答奖励全为 0 或全为 1 时，标准梯度估计会失效（因为这些样本的优势值全为零，对梯度无贡献）。AGE 通过检测并排除这些无效组，对剩余有效样本的梯度进行重缩放：
   $$\hat{\mathbf{g}} = \frac{\sum_{i=M+1}^{B} \mathbf{g}_i}{B-M} = \mathbf{g} \frac{B}{B-M} = \alpha \mathbf{g}, \quad \alpha = \frac{B}{B-M}$$
   其中 $B$ 为总组数，$M$ 为无效组数。

5. **有效样本阈值与重采样**：为控制梯度估计的方差，引入有效样本比例阈值 $\beta_{th} = 1/\alpha_{th}$。当有效组比例低于 $\beta_{th}$ 时，累积有效样本并重新采样，确保每次更新的梯度估计足够可靠。实验表明 $\beta_{th}=0.6$ 时取得最佳平衡。

6. **策略梯度更新**：使用 AGE 校正后的梯度更新策略参数，目标函数为：
   $$\hat{\mathcal{I}}_{\mathrm{GPG}}(\theta) = \alpha \mathcal{I}_{\mathrm{GPG}}(\theta)$$
   其中 $\mathcal{I}_{\mathrm{GPG}}(\theta)$ 为组策略梯度原始目标，$\alpha$ 为 AGE 缩放因子。

### 组件对比：GPG 的极简设计

Table 2 清晰展示了 GPG 与主流 RL 推理方法的架构差异：

| 组件 | PPO | GRPO | TRPO | **GPG** |
|------|-----|------|------|---------|
| 价值模型 | ✓ | ✗ | ✓ | **✗** |
| 参考模型 | ✓ | ✓ | ✗ | **✗** |
| 替代损失 | ✓ | ✓ | ✓ | **✗** |
| 策略约束（KL） | ✓ | ✓ | ✓ | **✗** |

GPG 是唯一**四项全无**的方法。PPO 需要完整的价值模型、参考模型、裁剪替代目标和 KL 约束；GRPO 虽移除了价值模型，但仍保留参考模型和 KL 散度正则化；TRPO 不使用参考模型但依赖价值模型和替代目标。GPG 通过将组决策动态直接融入标准策略梯度，在保持最简形式的同时实现了更优的性能。

### 训练稳定性的内在机制

GPG 不依赖 KL 散度约束来限制策略更新幅度，其训练稳定性来源于两个内在机制：
- **组内奖励归一化**天然提供了相对比较基准，使优势值保持在合理范围内；
- **AGE 的重缩放机制**避免了因无效样本比例波动导致的梯度幅度剧烈变化。

值得注意的是，消融实验表明**引入 KL 散度约束反而会损害 GPG 的性能**，这进一步验证了去除分布约束的合理性——GPG 直接优化原始 RL 目标的设计使其无需额外的策略正则化。

## 核心模块与公式推导

### 问题形式化与策略梯度基础

GPG 直接优化原始强化学习目标，无需替代损失函数。给定问题 $q$ 和提示 $s$，策略 $\pi_\theta$ 采样动作 $a$（即完整推理回答），并获得最终奖励信号 $r$。目标为最大化期望累积奖励：

$$\mathcal{I}(\theta) = \max_\theta \mathbb{E}_{\pi_\theta} \left[ \sum_{t=0}^T r_t \right]$$

根据策略梯度定理，该目标的梯度可表达为：

$$\nabla_\theta \mathcal{I}(\theta) = \mathbb{E}_{\pi_\theta} \left[ \nabla_\theta \log \pi_\theta(a_t|s_t) A^{\pi_\theta}(s_t, a_t) \right]$$

其中 $A^{\pi_\theta}(s_t, a_t)$ 为优势函数，用于降低梯度估计方差。在模型推理场景中，GPG 采用一步优势估计，仅依赖最终奖励信号，避免了广义优势估计（GAE）的复杂性。

### GPG 核心目标函数

GPG 的核心创新在于将组决策动态直接融入标准策略梯度。对每个问题采样一组 $G$ 个回答 $\{o_i\}_{i=1}^G$，目标函数为：

$$\mathcal{J}_{\mathrm{GPG}}(\theta) = \mathbb{E}_{(q,a)\sim\mathcal{D},\{o_i\}_{i=1}^G} \left[ \frac{1}{\sum_{i=1}^G |o_i|} \sum_{i=1}^G \sum_{t=1}^{|o_i|} \left( -\log \pi_\theta(o_{i,t} | q, o_{i,<t}) \hat{A}_{i,t} \right) \right]$$

其中：
- $o_{i,t}$：第 $i$ 个回答的第 $t$ 个 token
- $|o_i|$：第 $i$ 个回答的 token 长度
- $\hat{A}_{i,t}$：组内归一化后的 token 级优势值

### 组内优势估计

GPG 利用组内奖励均值进行归一化以消除价值模型，优势函数定义为：

$$\hat{A}_{i,t} = \frac{r_i - \mathrm{mean}(\{R_i\}_{i=1}^G)}{F_{norm}}$$

其中 $r_i$ 为第 $i$ 个回答的奖励，$F_{norm}$ 为归一化因子。GPG 最终采用 $F_{norm}=1$（即不做标准差归一化），仅通过减去组内均值实现方差缩减。

这一设计的关键因果机制在于：组内均值归一化天然提供了相对比较信号，使得策略梯度更新方向由组内相对优劣决定，无需维护独立的价值模型。

### 精确梯度估计（AGE）

当组内所有回答奖励全为 0 或全为 1 时，组内均值归一化后的优势值全为零，导致该组对梯度更新无贡献，产生梯度估计偏差。AGE 通过排除这些无效组并重缩放梯度来校正该偏差：

$$\hat{\mathbf{g}} = \frac{\sum_{i=M+1}^{B} \mathbf{g_i}}{B-M} = \mathbf{g} \frac{B}{B-M} = \alpha \mathbf{g}, \quad \alpha = \frac{B}{B-M}$$

其中：
- $B$：总组数
- $M$：无效组数（全正确或全错误）
- $\mathbf{g_i}$：第 $i$ 组的梯度
- $\alpha$：梯度缩放因子

最终 GPG 目标函数乘以缩放因子：

$$\hat{\mathcal{I}}_{\mathrm{GPG}}(\theta) = \alpha \mathcal{I}_{\mathrm{GPG}}(\theta)$$

### 有效样本阈值与重采样

为控制梯度估计方差，GPG 引入有效样本比例阈值 $\beta_{th} = 1/\alpha_{th}$。当有效组比例低于 $\beta_{th}$ 时，系统累积有效样本并触发重采样，确保参与梯度更新的样本量充足。实验表明 $\beta_{th}=0.6$ 时取得最佳性能平衡（Table 1）。

### 与 GRPO 优势估计的对比

GRPO 的优势估计为简单的组内差值（原始 GRPO 未除以标准差）：

$$\hat{A}_{i,t}^{\mathrm{GRPO}} = R(o_i) - \frac{1}{G} \sum_{j=1}^G R(o_j)$$

GPG 与之关键区别在于：（1）去除标准差归一化以避免引入偏差；（2）结合 AGE 校正无效样本带来的梯度估计偏差。消融实验证实，无 AGE 的 GPG（$F_{norm}=1, \alpha=1$）平均分仅 43.9%，未显著优于 GRPO 的 43.7%；加入 AGE 后提升至 48.3%（Table 1），说明 AGE 是性能提升的决定性组件。

## 实验与分析

### 一、主实验结果

GPG 在单模态数学推理、几何推理、视觉推理、推理定位及细粒度分类等任务上均一致优于 GRPO，且训练资源消耗更低。

**数学推理（Qwen2.5-Math-7B）。** 在 AIME24、MATH-500、AMC23、Minerva、OlympiadBench 五个基准上，GPG 的最优配置（$F_{\text{norm}}=1$，$\alpha = B/(B-M)$，$\beta_{th}=0.6$）取得平均分 48.3，较 GRPO 的 43.7 提升 +4.6 个百分点（Table 1）。值得注意的是，若仅去除归一化偏差（$F_{\text{norm}}=1$，$\alpha=1$）而不引入精确梯度估计（AGE），GPG 仅得 43.9，未显著超越 GRPO，这表明 AGE 是性能增益的关键来源。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/003_Table_1.jpg]]
*Table 1: We utilize a basic Math Reasoning setting 1 of SimpleRL from open-r1 (Face, 2025), using only the MATH-lighteval dataset to facilitate rapid experimental validation. Specifically, we remove the format reward and only enable the accuracy reward for simplicity. Table 1: Math reasoning results on Qwen2.5-Math-7B model. †: reproduction use the released code*

**1.5B 蒸馏模型。** 在 DeepSeek-R1-Distill-Qwen-1.5B 上，GPG-RS1 取得平均 pass@1 55.7，优于基于 GRPO 的 Open-RS1（53.1），提升 +2.6（Table 3）。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/007_Table_3.jpg]]
*Table 3: The zero-shot pass@1 performance of the 1.5B models distilled by DeepSeek-R1 across five mathematical reasoning benchmarks. †: reproduced results using released codes. ‡: results from (Dang & Ngo, 2025)*

**7B 模型。** GPG-Zero-7B 在五个数学推理基准上取得平均 pass@1 57.7，大幅领先 Oat-Zero-7B（51.4），提升 +6.3（Table 4），并在 AIME24（36.7）和 MATH-500（82.0）上均取得最优。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/008_Table_4.jpg]]
*Table 4: The zero-shot pass@1 performance of the 7B models across five mathematical reasoning benchmarks. †: reproduced results using the released code. ‡: results from (Dang & Ngo, 2025), ⋆: results from (Liu et al., 2025a)*

**几何推理。** 在 GEOQA 测试集上，GPG 取得准确率 51.33，较 GRPO 的 47.48 提升 +3.85（Table 5）。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/011_Table_5.jpg]]
*Table 5: Geometry reasoning results on GEOQA. GPG is better than GRPO. Table 7: Visual reasoning results on CV-Bench (Tong et al., 2024), which shows GPG training on base model has overall better performance over GRPO and the base model*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/009_Table_5.jpg]]

**视觉推理。** 在 CV-Bench 上，GPG 取得总分 76.15，较 GRPO 的 59.47 提升 +16.68（Table 7），在计数、关系、深度、距离等子维度上全面领先。

**推理定位。** 在 LISA 基准上，GPG 的 mIoU_test 达 51.8，较 GRPO 的 37.6 提升 +14.2（Table 8）。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/012_Table_8.jpg]]
*Table 8: Reasoning grounding results on LISA (Lai et al., 2024). GPG surpasses GRPO in reasoning grounding*

**细粒度分类。** 在四个少样本分类数据集上，GPG 平均准确率 89.0，较 GRPO 的 81.9 提升 +7.1（Table 6）。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/010_Table_6.jpg]]
*Table 6: 4-shot Results on Four Fine-grained Classification Datasets. GPG shows consistently better results than GRPO on 4 classification datasets*

**与 DAPO 对比。** 在 Qwen-7B Math 上，GPG 以更简单的架构（无价值模型、无参考模型、无 KL 约束）取得平均分 57.7，优于 DAPO 的 56.0，且训练数据量和计算开销更低（Table 9）。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/013_Table_9.jpg]]
*Table 9: Comparison with DAPO (Qwen-7B Math). Ours is simpler, stronger and resource efficient*

### 二、消融实验

**精确梯度估计（AGE）至关重要。** 在 Qwen2.5-Math-7B 上，无 AGE（$F_{\text{norm}}=1$，$\alpha=1$）时 GPG 仅得 43.9，与 GRPO 的 43.7 几乎持平；引入 AGE 后提升至 47.8，进一步加入阈值重采样（$\beta_{th}=0.6$）后达到 48.3（Table 1）。这验证了 AGE 对校正全正确/全错误组带来的梯度偏差具有决定性作用。

**有效样本阈值 $\beta_{th}$ 的影响。** 在 Qwen2.5-Math-7B 上，$\beta_{th}=0.8$ 时取得最佳平均分 48.6，表明合理的阈值设置能有效降低梯度估计方差（Table 10）。阈值过低会导致有效样本不足，过高则可能引入噪声。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/014_Table_10.jpg]]

**组大小的影响。** 在不使用 AGE 的条件下，组大小从 2 增加到 16 可稳步提升平均性能（Table 11），但考虑到计算成本，论文选定组大小为 8 作为平衡点。

**KL 散度约束有害。** 在 GPG 中引入 KL 散度正则化会导致性能下降（Table 13），这支持了 GPG 的核心设计理念——直接优化原始 RL 目标无需分布约束。

**组内奖励归一化优于批次归一化。** 组内归一化取得平均分 45.3，优于批次归一化的 44.9（Table 13），表明组级别的相对比较能更有效地稳定训练。

### 三、训练动态分析

**奖励分布与梯度校正的必要性。** 随着训练推进，组内全正确（奖励全为 1）和全错误（奖励全为 0）的问题比例显著上升（Figure 2 左），这些无效样本组对梯度估计的贡献为零，直接平均会导致梯度被稀释。AGE 通过因子 $\alpha = B/(B-M)$ 对有效样本梯度进行重缩放，恰好补偿了这一偏差（Figure 2 右展示了 $\alpha$ 随训练步数的变化）。

**GPG 与 GRPO 的训练指标对比。** 在 DeepSeek-R1-Distill-Qwen-1.5B 上，GPG 的训练损失更低、奖励曲线更高、生成长度更稳定（Figure 3），表明 GPG 不仅最终性能更优，训练过程也更为高效平稳。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/024_Figure_3.jpg]]
*Figure 3: Comparison of GPG(blue curves) and GRPO(gray curves) in terms of training loss, rewards and completion length. Experiments are based on DeepSeek-R1-Distill-Qwen-1.5B, same as Table 3*

### 四、失败模式与局限性

1. **未在超大模型上验证。** 受计算资源限制，GPG 仅在 ≤7B 参数规模的模型上进行了评估，其在 70B 及以上模型上的可扩展性尚待验证。
2. **长期训练中缺乏策略约束的风险。** GPG 完全移除了参考模型和 KL 散度约束，尽管当前实验未观察到训练不稳定，但在更复杂任务或更长训练周期中，缺失分布约束可能导致模型遗忘预训练知识。
3. **AGE 对奖励分布的依赖。** AGE 和阈值重采样机制依赖有效样本比例，当问题难度极端不平衡时，可能需要更精细的自适应策略。
4. **多模态任务中的奖励敏感性。** 在视觉推理和推理定位等任务中，奖励设计（如 IoU 阈值、格式奖励）对性能影响较大，GPG 的通用性可能受限于具体奖励函数的选择。

### 五、关键图表结论

- **Figure 1**：GPG 在单模态数学推理和多模态推理任务上均大幅领先 GRPO 及其他基线，验证了方法的通用性和有效性。
- **Table 2**：GPG 是唯一同时去除价值模型、参考模型、替代损失和策略约束的方法，实现了 RL 训练流程的最大简化。
- **Figure 4**：在 AIME24 案例中，GPG 生成的推理过程比 GRPO 更全面、准确，定性展示了方法对推理质量的提升。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_inccdtfx8x/figures/002_Figure_1.jpg]]
*Figure 1: Performance comparison on unimodal reasoning tasks, with extended validation on multimodal reasoning. (Top) GPG achieves substantial performance gains over state-of-the-art (SOTA) baselines across diverse mathematical benchmarks, demonstrating its core effectiveness for linguistic reasoning. (Bottom) The method also generalizes robustly to multi-modal settings, outperforming other RL methods and further validating its broad applicability*

## 方法谱系与知识库定位

### 与现有RL方法的谱系关系

GPG的核心贡献在于将组决策动态直接融入标准策略梯度（Policy Gradient, PG）框架，从而在推理任务中实现了对现有强化学习方法的系统性简化。该简化并非凭空产生，而是通过对PPO–GRPO谱系中冗余组件的逐层剥离和偏差修正完成的。

**PPO**（Schulman et al., 2017）是该谱系的起点，其完整架构包含四个核心组件：价值模型（Critic）、参考模型（Reference Model）、替代损失函数（Surrogate Loss）和KL散度策略约束。PPO通过裁剪替代目标 $\mathcal{I}^{\mathrm{CLIP}}(\theta) = \mathbb{E}_t [\min(r_t(\theta) \hat{A}_t, \mathrm{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t)]$ 限制策略更新幅度，同时依赖价值模型估计优势函数，并使用参考模型计算概率比 $r_t(\theta)$。**TRPO**（Schulman et al., 2015）则移除了参考模型，但仍保留价值模型和替代损失。

**GRPO**（Shao et al., 2024）是GPG最直接的对比基线，其关键突破在于通过组内奖励均值归一化移除了价值模型，将优势估计简化为 $\hat{A}_{i,t} = R(o_i) - \frac{1}{G}\sum_{j=1}^G R(o_j)$。然而，GRPO仍保留了参考模型用于计算KL散度约束，且其奖励标准化（除以标准差）引入了额外的估计偏差。**Dr. GRPO**（Liu et al., 2025a）进一步研究了奖励和损失归一化的细节，但未触及根本架构简化。

GPG的定位是这一简化过程的终点：它同时移除了价值模型、参考模型、替代损失和KL散度约束，仅保留组内奖励均值归一化作为方差缩减手段（Table 2）。与同样追求简化的**ReMax**（Li et al., 2024）相比，GPG通过AGE梯度校正机制解决了无效样本偏差问题，这是ReMax未涉及的维度。

**DAPO**（Yu et al., 2025）是另一条并行路线，采用动态采样和全有效批次策略，但保留了更多训练组件（如CLIP项和KL散度）。Table 9的直接对比表明，在Qwen-7B Math设定下，GPG以更简单的架构（无CLIP、无KL）实现了57.7%的平均得分，优于DAPO的56.0%，同时消耗更少的训练资源和数据。

### 适用边界与局限性

**模型规模的可扩展性**：GPG当前验证集中于7B及以下参数规模的模型（Qwen2.5-Math-7B、DeepSeek-R1-Distill-Qwen-1.5B/7B），在更大规模模型（>70B）上的表现尚待验证。论文明确指出这一局限源于计算资源约束。

**训练稳定性的隐忧**：尽管实验表明GPG在去除KL散度约束后未出现训练不稳定，甚至添加KL约束反而损害性能（Table 13），但这并不意味着分布约束在所有场景下都可有可无。在更复杂的任务或更长训练周期中，完全缺失策略约束可能导致模型遗忘预训练知识或策略崩溃，这一风险需要进一步评估。

**AGE机制对奖励分布的敏感性**：精确梯度估计（AGE）通过因子 $\alpha = B/(B-M)$ 校正全正确/全错误组的梯度偏差，并引入有效样本比例阈值 $\beta_{th}$ 触发重采样以控制方差。该机制的有效性依赖于组内奖励存在一定区分度——当问题难度极端不平衡（大量组内全正确或全错误）时，$\alpha$ 值可能过大，导致梯度估计方差激增。Figure 2展示了训练过程中全正确/全错误组比例和奖励标准差的变化，证实了这一现象的存在，但论文未提供极端分布下的自适应策略。

**奖励函数设计的耦合性**：在多模态任务（视觉推理、推理定位）中，GPG的性能增益显著（CV-Bench上+16.68%，LISA上+14.2% mIoU），但这些任务依赖特定的奖励设计（如IoU、格式奖励）。GPG对奖励函数选择的敏感性尚未被系统消融，其通用性可能受到奖励设计质量的影响。

### 开放问题

1. **大规模模型扩展性**：GPG在70B+参数模型上的性能与稳定性如何？AGE机制在更大batch size下的方差特性是否保持不变？

2. **长期训练中的分布漂移**：去除KL散度约束后，策略在长期训练中是否会逐渐偏离初始分布，导致预训练知识遗忘？现有的训练步数（通常数千步）可能不足以暴露这一问题。

3. **AGE的自适应阈值策略**：当前 $\beta_{th}$ 为固定值（最优0.8，Table 10），能否根据训练进度或奖励分布动态调整阈值，以更好地平衡偏差-方差权衡？

4. **多任务与多模态泛化**：GPG的组内归一化假设奖励信号具有可比性，在奖励尺度差异巨大的多任务场景下，是否需要引入任务特定的归一化策略？

5. **与过程奖励的兼容性**：当前GPG仅使用最终奖励信号（one-step estimation），能否扩展到使用过程奖励模型（PRM）的场景，以提供更细粒度的优势估计？

## 原文 PDF

![[paperPDFs/ICLR_2026/GPG_A_Simple_and_Strong_Reinforcement_Learning_Baseline_for_Model_Reasoning.pdf]]
