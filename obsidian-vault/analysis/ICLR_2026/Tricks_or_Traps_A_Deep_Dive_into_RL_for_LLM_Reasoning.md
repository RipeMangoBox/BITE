---
title: "Tricks or Traps? A Deep Dive into RL for LLM Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Tricks_or_Traps_A_Deep_Dive_into_RL_for_LLM_Reasoning.pdf
openreview_forum_id: R0JM3BWP7W
aliases:
- LP
- TOTDDIRLR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "优势归一化的组合方式（组均值+批量标准差）与token级损失聚合。"
primary_logic: "通过系统性分析和消融各种RL技术，发现仅需结合两种技术（组均值、批量标准差的优势归一化和token级损失聚合）即可在无critic的PPO损失下释放策略的学习能力，且这种最小组合（Lite PPO）在多个基准上超越更复杂的GRPO和DAPO等方法。"
claims:
- "去除标准差在奖励高度集中时增强训练稳定性与有效性。"
- "局部（组）均值+全局（批量）标准差实现更鲁棒的优势归一化。"
- "仅结合优势归一化（组均值、批量标准差）和token级损失聚合即可最大化无critic PPO策略的潜力，超过GRPO和DAPO。"
- "Token级损失相比序列级损失在基础模型上更有效，能提升收敛速度和峰值准确率。"
---

# Tricks or Traps? A Deep Dive into RL for LLM Reasoning

> [!tip] 核心洞察
> 通过系统性分析和消融各种RL技术，发现仅需结合两种技术（组均值、批量标准差的优势归一化和token级损失聚合）即可在无critic的PPO损失下释放策略的学习能力，且这种最小组合（Lite PPO）在多个基准上超越更复杂的GRPO和DAPO等方法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 是技巧还是陷阱？深入探究用于LLM推理的强化学习 |
| 英文题名 | Tricks or Traps? A Deep Dive into RL for LLM Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=R0JM3BWP7W) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Lite PPO |
| Dataset | MATH-500 (对齐模型, 简单数据), AMC23 (对齐模型, 困难数据), AIME25 (对齐模型 |

> [!tip] 效果简介
> - MATH-500 (对齐模型, 简单数据) 上，准确率 为 91.43，对比 90.57 (DAPO)，变化 +0.86。
> - AMC23 (对齐模型, 简单数据) 上，准确率 为 81.88，对比 79.69 (DAPO)，变化 +2.19。
> - AMC23 (对齐模型, 困难数据) 上，准确率 为 75.42，对比 68.54 (DAPO)，变化 +6.88。

## 概述

### 问题背景

将强化学习（RL）应用于大语言模型（LLM）的推理能力训练已成为当前研究热点。然而，该领域正面临一个核心瓶颈：**技术碎片化与实验设置不一致导致结论冲突**。不同工作采用了差异巨大的模型初始化策略、训练数据、奖励设计和RL优化技术，使得从业者难以判断哪些技术是真正有效的，哪些仅仅是特定设置下的偶然产物。例如，GRPO（Shao et al., 2024）主张组级归一化以增强稳定性，而REINFORCE++（Hu et al., 2025）则推崇批量级归一化；GRPO在归一化中引入方差，但Dr. GRPO（Liu et al., 2025b）却明确建议移除方差归一化以防止偏差。这种“技巧还是陷阱”的混乱局面，严重阻碍了RL4LLM方法的实际落地。

### 核心发现

本文通过超过160次独立RL训练实验，系统性地消融分析了各类RL优化技术，得出一个简洁而有力的结论：**仅需结合两种技术——优势归一化（组均值 + 批量标准差）和token级损失聚合——即可在无critic的PPO损失下充分释放策略的学习能力**。这一最小组合被命名为 **Lite PPO**。

具体而言，两个关键操作分别是：

- **优势归一化**：采用局部（组）均值减去奖励中心，同时使用全局（批量）标准差进行缩放，即 $A = (r - \text{mean}_{\text{group}}) / \text{std}_{\text{batch}}$。这种组合在奖励分布集中时（如简单数据集）可移除标准差以避免梯度过度放大，同时保留批量级标准差提供的更强梯度幅度约束。
- **Token级损失聚合**：将PPO的clip损失在token粒度上计算，而非传统的序列级均值。这在基础模型上显著提升收敛速度和峰值准确率。

### 方法定位

Lite PPO 位于 critic-free RL 方法谱系中，是对现有方法的极简化重构。与 GRPO（组均值+组标准差+KL惩罚）、DAPO（解耦clip+动态过滤）和 REINFORCE++（批量级归一化）相比，Lite PPO 剥离了KL正则项、解耦clip和复杂过滤机制，仅保留标准PPO损失，证明了**优势归一化的组合方式与损失聚合粒度是影响性能的核心因果杠杆**。

### 主要结果

Lite PPO 在多个基准上超越更复杂的现有方法：

| 基准 | 模型/数据 | Lite PPO | 最佳基线 | 提升 |
|------|-----------|----------|----------|------|
| MATH-500 | 对齐模型/简单数据 | 91.43 | 90.57 (DAPO) | +0.86 |
| AMC23 | 对齐模型/简单数据 | 81.88 | 79.69 (DAPO) | +2.19 |
| AMC23 | 对齐模型/困难数据 | 75.42 | 68.54 (DAPO) | +6.88 |
| AIME25 | 对齐模型/困难数据 | 46.67 | 38.34 (DAPO) | +8.33 |
| MATH-500 | Llama3-8B | 27.3 | 19.8 (GRPO) | +7.5 |
| LCB-v5 | 泛化编码 | 25.08 | 22.94 (GRPO) | +2.14 |
| GPQA | 泛化QA | 46.63 | 42.49 (GRPO) | +4.14 |

在非对齐模型（如Llama3-8B）上，Lite PPO 的优势尤为显著，相比GRPO提升达7.5个百分点。

### 局限与开放问题

研究主要集中在数学推理任务和4B-8B参数规模的模型上，更大模型及更多推理模态的泛化性尚待验证。此外，过length过滤的最优阈值、多轮RL训练的效应，以及Token级损失在所有初始化条件下的普适性，仍是值得进一步探索的开放问题。

## 背景与动机

### 强化学习驱动大语言模型推理的兴起与困境

近年来，强化学习（Reinforcement Learning, RL）已成为提升大语言模型（LLM）推理能力的核心技术路径。以 GRPO（Shao et al., 2024）、DAPO（Yu et al., 2025）和 REINFORCE++（Hu et al., 2025）为代表的一系列无价值函数（critic‑free）RL 方法，在数学推理、代码生成等任务上取得了显著进展。这些方法通过引入多种优化技巧——如优势归一化、裁剪策略、KL 散度正则、过长度过滤等——来稳定训练过程并提升策略的探索能力。

然而，这一快速发展的领域正面临一个核心瓶颈：**现有 RL 技术缺乏标准化的使用指南和对内在机制的深入理解**。不同方法在实验设置上的显著差异——包括模型初始化状态（基座模型 vs. 已对齐模型）、训练数据分布、奖励函数设计、超参数选择等——导致研究结论之间频繁出现冲突。例如，GRPO 主张使用组级归一化来促进样本内竞争，而 REINFORCE++ 则倾向于批量级归一化以缓解过拟合和奖励攻击；GRPO 在归一化中包含方差项，而 Dr. GRPO（Liu et al., 2025b）却明确建议移除方差归一化以防止偏差。这种“技巧扩散”现象使得从业者在实际应用中面临较高的试错成本，难以确定哪些技术是真正必要且通用的。

### 从技巧堆叠到机制理解的研究动机

本文的核心动机在于：**通过系统性的消融分析和机制解构，厘清现有 RL 优化技术各自的作用边界与适用场景，进而提炼出一组最小化但高效的技术组合**。研究团队在统一的实验框架 ROLL 下，进行了超过 160 次独立的 RL 训练运行，覆盖多种模型尺寸（4B、8B）、模型类型（基座模型、已对齐模型）和不同难度的数学推理数据集。

研究的关键发现是：**仅需结合两种技术——优势归一化（组均值 + 批量标准差）和 token 级损失聚合——即可在无 critic 的标准 PPO 损失下充分释放策略的学习能力**。这一极简组合被命名为 Lite PPO，其在多个数学推理基准上不仅超越了采用更多技巧的 GRPO 和 DAPO，还展现出对代码生成、科学问答等非数学推理模态的良好泛化能力。

该发现揭示了一个重要洞察：在 RL4LLM 推理任务中，**技巧的叠加并非总是带来增益，关键在于识别那些直接作用于梯度信号质量和更新粒度控制的核心机制**。通过将优势归一化中的标准差计算从局部（组级）提升到全局（批量级），并采用 token 级别的损失聚合替代传统的序列级损失，Lite PPO 以更简洁的设计实现了更鲁棒和高效的策略优化。

## 核心创新

本工作提出 **Lite PPO**，一种极简的无 critic PPO 变体，其核心创新在于识别出两个关键“控制旋钮”（causal knobs）——**优势归一化**与**损失聚合粒度**——并证明仅需对这两个模块进行特定组合即可释放策略的学习能力，在多个基准上超越更复杂的 GRPO 与 DAPO 等方法。

### 创新点一：混合优势归一化（组均值 + 批量标准差）

现有 critic-free RL 方法在优势归一化上存在分歧：**GRPO**（Shao et al., 2024）采用组级归一化（组均值 + 组标准差）以促进 prompt 内的竞争，而 **REINFORCE++**（Hu et al., 2025）则采用批量级归一化以缓解过拟合。本工作通过系统消融发现，这两种策略各自存在缺陷：

- **纯批量级归一化**对奖励分布偏斜高度敏感，在困难数据集上常导致性能崩溃（Figure 4）。
- **组级归一化中的组标准差**在奖励分布高度集中时（如简单数据集），会因分母趋近于零而过度放大梯度，破坏训练稳定性（Figure 5）。

Lite PPO 的解决方案是将均值与标准差的计算解耦：**均值在局部（组内）计算，标准差在全局（整个批次）计算**。具体而言，对于每个 prompt 的第 $k$ 个回复，其优势值计算为：

$$A_k^{\text{mix}} = \frac{r_k - \text{mean}(\{r_j\}_{j=1}^{K})}{\text{std}(\{r_j\}_{j=1}^{N \times K})}$$

其中 $K$ 为每 prompt 的回复数，$N$ 为批次中的 prompt 数。这一设计的因果机制在于：
1. **组均值**保留了 prompt 内的相对比较信号，使模型能区分同一问题下不同回复的质量差异；
2. **批量标准差**提供了更稳定、更具全局代表性的梯度幅度约束，避免了组标准差在小样本下的噪声放大效应。

消融实验（Figure 6）明确显示，这种“组均值 + 批量标准差”的组合在基础模型上一致优于“组均值 + 组标准差”的纯组级方案，验证了其鲁棒性优势。

### 创新点二：Token 级损失聚合

传统 PPO 及其 critic-free 变体通常采用**序列级损失**：对每条回复的所有 token 取平均后再计算策略损失。Lite PPO 改为**token 级损失聚合**，即逐 token 计算优势加权的 PPO 损失：

$$\mathcal{L}_{\text{PPO}}(\theta) = \mathbb{E}\left[\frac{1}{|o|}\sum_{t=1}^{|o|} \min\left(r_t(\theta) A_t,\ \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t\right)\right]$$

该设计的因果机制在于：序列级损失将整条回复视为一个整体，掩盖了 token 级别的细粒度信号——某些 token 对最终奖励的贡献远大于其他 token，但序列平均会稀释这种差异。Token 级损失使每个 token 的优势信号直接参与梯度计算，从而提供更精确的策略更新方向。

实验证据（Figure 9）表明，token 级损失在基础模型上显著提升了收敛速度和峰值准确率；但在已对齐的指令模型上增益有限，这暗示指令模型的 token 分布已较为均匀，细粒度信号的价值相对降低。

### 创新点三：极简组合的有效性

Lite PPO 的核心洞察在于：**仅需组合上述两个技术——混合优势归一化与 token 级损失聚合——即可在无 critic 的 vanilla PPO 损失下最大化策略的学习能力**。这一结论通过以下证据链得到强支撑：

- 在已对齐 Qwen3-8B 上，Lite PPO 在 MATH-500 上达到 91.43%（超过 DAPO 的 90.57%），在 AMC23 上达到 81.88%（超过 DAPO 的 79.69%）（Table 1）。
- 在困难数据设置下，Lite PPO 在 AMC23 上领先 DAPO 6.88 个百分点，在 AIME25 上领先 8.33 个百分点（Table 2）。
- 在非对齐 Llama3-8B 上，Lite PPO 达到 27.3%（GRPO 为 19.8%，DAPO 为 23.67%），优势显著（Table 3, Figure 12）。
- 在代码（LCB-v5）、科学问答（GPQA）等泛化模态上，Lite PPO 同样一致超越 GRPO（Table 4）。

值得注意的是，Lite PPO **不引入 KL 散度正则项**（与 GRPO 不同）、**不采用解耦 clip**（与 DAPO 不同）、**不使用 critic 网络**，仅通过两个低成本的归一化与聚合策略即实现了更优或相当的性能。这验证了论文的核心主张：当前 RL4LLM 领域的技术扩散中存在大量冗余技巧，真正起决定性作用的只有少数关键组件。

## 整体框架

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_R0JM3BWP7W/figures/003_Figure_1.jpg]]
*Figure 1: Left: The proliferation of RL optimization techniques, coupled with diverse initialized models and data, has raised barriers to practical adoption. Right: We establish detailed application guidelines via dissecting internal mechanisms of widely-used tricks, and introduce Lite PPO, a minimalist two-technique combination that enhances learning capacity in critic-free policies with vanilla PPO loss. The average accuracy is calculated across six mathematical benchmarks*

本研究构建了一个系统性的分析框架，旨在从当前LLM推理强化学习中繁杂的技术组合中，剥离出真正有效的核心机制。该框架围绕三个层次展开：**问题诊断**、**机制消融**和**简化方案验证**。

### 问题诊断

当前RL4LLM领域面临的核心瓶颈在于**实验设置的高度不一致性**：不同工作采用不同的基模型初始化（Base vs. Instruct）、训练数据难度、奖励设计和超参数配置，导致同一技术在不同上下文下产生相互冲突的结论。例如，GRPO（Shao et al., 2024）主张组级归一化以促进组内竞争，而REINFORCE++（Hu et al., 2025）则采用批量级归一化来缓解过拟合；GRPO在归一化中保留标准差，但Dr. GRPO（Liu et al., 2025b）明确建议移除标准差归一化以防止偏差。这种技术扩散现象（Figure 1）极大提高了从业者的采用门槛。

### 统一实验平台

为消除设置差异带来的混淆，框架将所有方法统一到**ROLL框架**下，固定关键超参数：批次大小1024、每次prompt采样128条回复（rollout）、采样参数top_p=0.99、温度0.99。训练数据采用开源数学推理数据集，按8次采样下的正确响应数划分为Easy、Medium、Hard三个难度等级（Figure 2）。在此平台上，研究完成了**超过160次独立RL训练运行**，覆盖4B和8B参数量的Base与Instruct模型。

### 分析流水线

框架的分析流水线按以下模块组织：

1. **优势归一化器（Advantage Normalizer）**：将奖励映射为优势值，是策略梯度估计的核心。分析覆盖三种归一化维度——均值计算范围（组级 vs. 批量级）、标准差计算范围（组级 vs. 批量级）以及是否保留标准差。输入为每个prompt的K条回复的奖励向量，输出为归一化后的优势值。

2. **策略损失聚合器（Loss Aggregator）**：决定如何将token级的概率比与优势值聚合成最终的策略损失。对比序列级损失（对每条序列所有token取均值）与token级损失（逐token计算优势加权的损失）。

3. **PPO代理损失（PPO Surrogate Loss）**：采用无critic的标准PPO clipped objective，使用REINFORCE估计优势，并通过裁剪概率比限制策略更新幅度。该模块接收归一化后的优势值和策略概率比，输出最终的优化目标。

4. **辅助技术层**：包括Clip Higher（解耦裁剪上下界以缓解熵崩塌）、过length过滤（掩码超长回复的奖励以保持鲁棒性）等可选组件。

### 简化方案

基于系统性消融的核心发现——**仅需结合两种技术即可最大化无critic PPO策略的学习能力**：① 组均值+批量标准差的优势归一化；② token级损失聚合。这一最小组合被命名为**Lite PPO**，其在多个基准上超越了更复杂的GRPO和DAPO等方法，验证了“少即是多”的设计哲学。

## 核心模块与公式推导

### 1. 优势归一化器 (Advantage Normalizer)

优势归一化是稳定 RL 训练、降低梯度方差的标准技术。在无 critic 的 PPO 框架下，优势值直接由奖励信号构造。本文系统分析了两种主流归一化范式的内在机制：

**组级归一化 (Group‑level Normalization)** 对同一 prompt 的 $K$ 条回复计算局部统计量：

$$A _ { k } ^ { \mathrm { g r o u p } } = \frac { r _ { k } - \mathrm { m e a n } ( \{ r _ { j } \} _ { j = 1 } ^ { K } ) } { \mathrm { s t d } ( \{ r _ { j } \} _ { j = 1 } ^ { K } ) }$$

其中 $r_k$ 为第 $k$ 条回复的奖励，分母为组内标准差。该方法通过组内竞争促进探索，是 GRPO (Shao et al., 2024) 和 RLOO 的核心设计。

**批量级归一化 (Batch‑level Normalization)** 则使用整个批次 $N \times K$ 个奖励的全局统计量：

$$A _ { i } ^ { \mathrm { b a t c h } } = \frac { r _ { i } - \mathrm { m e a n } ( \{ r _ { j } \} _ { j = 1 } ^ { N * K } ) } { \mathrm { s t d } ( \{ r _ { j } \} _ { j = 1 } ^ { N * K } ) }$$

REINFORCE++ (Hu et al., 2025) 采用此范式以缓解过拟合和奖励攻击。

**关键发现：混合归一化。** 实验揭示，两种范式的有效性取决于奖励分布的集中程度。当奖励分布高度集中（如简单训练集）时，标准差会放大微小奖励差异，导致梯度震荡。此时**去除标准差**仅保留均值中心化更为稳定：

$$\boldsymbol { A } _ { k } ^ { \mathrm { s t d } ^ { - } } = \boldsymbol { r } _ { k } - \mathrm { m e a n } ( \{ r _ { j } \} _ { j = 1 } ^ { K } )$$

进一步，**组均值 + 批量标准差**的组合（即均值在组内计算、标准差在全局计算）被证明是最鲁棒的方案：组均值保留了组内竞争信号，而批量标准差提供了更强的梯度幅度约束，避免了局部标准差在奖励稀疏时的估计偏差（见 Figure 6）。这一组合构成了 Lite PPO 的第一个核心模块。

### 2. Token 级损失聚合器 (Token‑level Loss Aggregator)

传统 PPO 采用**序列级损失**：对一条完整回复的所有 token 取平均后再计算策略损失。标准 PPO 裁剪代理目标为：

$$\mathcal { T } _ { \mathrm { P P O } } ( \theta ) = \mathbb { E } _ { [ q \sim P ( Q ) , \ o \sim \pi _ { \theta _ { \mathrm { o l d } } } ( O \mid q ) ] } \frac { 1 } { | \boldsymbol { o } | } \sum _ { t = 1 } ^ { | o | } \operatorname* { m i n } \left( \frac { \pi _ { \theta } \left( o _ { t } | q , o _ { < t } \right) } { \pi _ { \theta _ { \mathrm { o l d } } } \left( o _ { t } | q , o _ { < t } \right) } A _ { t } , \mathrm { c l i p } \left( \frac { \pi _ { \theta } \left( o _ { t } | q , o _ { < t } \right) } { \pi _ { \theta _ { \mathrm { o l d } } } \left( o _ { t } | q , o _ { < t } \right) } , 1 - \epsilon , 1 + \epsilon \right) A _ { t } \right)$$

其中 $\frac{1}{|o|}$ 即为序列级平均。

**Token 级损失**则逐 token 计算优势加权的策略损失后再聚合，使每个 token 的贡献按其重要性（优势值）独立加权。消融实验（Figure 9）表明：在 Base 模型上，token 级损失显著提升收敛速度和峰值准确率；但在已对齐的 Instruct 模型上增益有限。这一差异的因果机制在于，Base 模型的 token 级奖励信号更稀疏，序列级平均会稀释关键 token 的学习信号。

### 3. PPO 代理损失 (Critic‑Free Surrogate Loss)

Lite PPO 直接使用无 critic 的标准 PPO 损失，以 REINFORCE 方式从组内奖励估计优势，无需额外训练价值网络。这避免了 critic 网络引入的偏差和计算开销，同时通过上述两个模块（混合优势归一化 + token 级损失聚合）充分释放了无 critic 策略的学习潜力。

**与 GRPO/DAPO 的差异。** GRPO 在 PPO 损失中额外引入 KL 散度正则项：

$$\mathcal { I } _ { \mathrm { G R P O } } ( \theta ) = \mathbb { E } \left[ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \frac { 1 } { | \omega _ { i } | } \sum _ { t = 1 } ^ { | \omega _ { i } | } \left\{ \operatorname* { m i n } ( r _ { i , t } ( \theta ) \hat { A } _ { i , t } , \exp ( r _ { i , t } ( \theta ) , 1 - \epsilon , 1 + \epsilon ) \hat { A } _ { i , t } ) - \beta D _ { \mathrm { K L } } [ \pi _ { \theta } \| \pi _ { \mathrm { r e f } } ] \right\} \right]$$

DAPO 则使用解耦的上下界裁剪和 token 级聚合：

$$\mathcal { I } _ { \mathrm { D A P O } } ( \theta ) = \mathbb { E } \frac { 1 } { \sum _ { i = 1 } ^ { G } \left. o _ { i } \right. } \sum _ { i = 1 } ^ { G } \sum _ { t = 1 } ^ { \left. o _ { i } \right. } \left\{ \operatorname* { m i n } \left( r _ { i , t } ( \theta ) \hat { A } _ { i , t } , \ \mathrm { c l i p } \left( r _ { i , t } ( \theta ) , 1 - \epsilon _ { \mathrm { l o w } } , 1 + \epsilon _ { \mathrm { h i g h } } \right) \hat { A } _ { i , t } \right) \right\}$$

Lite PPO 的极简设计表明，这些额外的 KL 正则和解耦裁剪并非必需——仅需两个核心模块即可在多个基准上超越 GRPO 和 DAPO。

## 实验与分析

### 实验设置概览

为隔离各RL技术组件的因果效应，作者在统一框架ROLL下进行了超过160次独立训练运行。所有实验采用一致的超参数：批次大小1024，rollout数量128，采样参数top_p=0.99、温度0.99，使用开源数学数据集训练。实验覆盖4B和8B两种参数规模，包含Qwen3-4B/8B的Base和Aligned（指令微调后）两类模型，以及Llama3-8B。根据8次rollout采样下的正确响应数，训练数据被划分为Easy、Medium、Hard三个难度等级（Figure 2）。

训练动态的初步观察（Figure 3）揭示了关键瓶颈：**Base模型从零开始学习推理能力，提升显著但伴随较大波动；Aligned模型初始准确率已较高，额外RL训练仅带来约2%的微弱增益**。这一差异直接影响了后续各技术在不同模型类型上的效果分化。

### 主实验结果

Lite PPO在多个基准上一致超越GRPO（Shao et al., 2024）和DAPO（Yu et al., 2025）。

**对齐模型 + 简单数据**（Table 1）：在Qwen3-8B上，Lite PPO平均准确率达62.17，超过DAPO的60.66。具体基准上，MATH-500达91.43（+0.86），AMC23达81.88（+2.19），AIME24达49.17（+1.25）。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_R0JM3BWP7W/figures/032_Table_1.jpg]]
*Table 1: Results using Qwen3-8B (aligned model) trained on the Easy dataset*

**对齐模型 + 困难数据**（Table 2）：差距进一步扩大。Lite PPO平均准确率66.96 vs DAPO 64.17。在AMC23上领先+6.88，在AIME25上领先+8.33，表明困难数据场景下Lite PPO的优势更显著。但需注意AIME24上DAPO反超+2.92，说明Lite PPO并非在所有子集上都占优。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_R0JM3BWP7W/figures/033_Table_2.jpg]]
*Table 2: Results using Qwen3-8B (aligned model) trained on the Hard dataset*

**非对齐Llama3-8B**（Table 3）：Lite PPO平均准确率25.53，远超GRPO的22.63和DAPO的23.67。MATH-500上达27.3（GRPO仅19.8，+7.5），验证了最小技术组合在Base模型上的有效性。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_R0JM3BWP7W/figures/034_Table_3.jpg]]
*Table 3: Results on Llama3-8B*

**泛化至其他推理模态**（Table 4）：在编码（LCB-v5: 25.08）、科学问答（GPQA: 46.63）、语言理解（MMLU-Pro: 62.38）上，Lite PPO的Pass@1均领先GRPO和DAPO，表明其泛化能力不限于数学推理。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_R0JM3BWP7W/figures/035_Table_4.jpg]]
*Table 4: Pass@1 score on other reasoning modalities*

### 消融分析

#### 优势归一化：均值与标准差的解耦

Figure 4对比了无归一化、批量归一化、组归一化在Easy和Hard数据集上的表现。**组级均值归一化（减去组均值）是实现稳定训练的核心**，批量级归一化在奖励分布偏斜时容易性能崩溃。

进一步消融标准差的作用（Figure 5）：在Easy数据集上，训练过程中标准差维持在极低水平（约0.05），此时除以标准差会过度放大小奖励差异的梯度，导致训练不稳定。**去除标准差后（仅用组均值偏移），训练稳定性和最终准确率均提升**。Takeaway 1明确指出：当奖励分布高度集中时，去除标准差增强训练稳定性与有效性。

#### 标准差计算粒度：组级 vs 批量级

Figure 6展示了关键发现：**组均值 + 批量标准差（而非组标准差）实现最优归一化**。仅使用组均值+组标准差（GRPO标准做法）时，由于每组内K个回复的标准差估计噪声大，归一化不稳定。改用批量级（N×K个回复）标准差计算后，梯度幅度得到更有效的约束，准确率明显提升。这构成Takeaway 2的核心主张。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_R0JM3BWP7W/figures/013_Figure_6.jpg]]
*Figure 6: Accuracy comparison of base models with different standard deviation calculation*

#### Clip Higher：缓解已对齐模型的熵崩塌

Figure 7揭示了模型类型的分化效应：Base模型的熵值在训练中自然下降但保持合理水平，Clip Higher对其影响有限；**Aligned模型的熵值急剧崩塌（从约2.0降至0.5以下），提高clip上界（ε_high从0.2增至0.28-0.32）能显著减缓这一崩塌**。Figure 8进一步显示，4B模型在ε_high=0.32时准确率峰值最高，8B模型在0.28时最优，表明最优clip上界与模型规模相关。

#### Token级损失聚合 vs 序列级损失

Figure 9的消融揭示了模型类型的又一次分化：**Token级损失在Base模型上显著提升收敛速度和峰值准确率，但在Aligned模型上增益有限**。这一发现直接指导了Lite PPO的设计——将token级损失聚合作为Base模型训练的核心组件。

#### 过length过滤的阈值效应

Figure 10展示了最大生成长度约束的影响：8k长度阈值配合过length过滤能提升学习效果，但将阈值放宽至20k后收益递减。Figure 11揭示了机制：错误生成（reward=0）的重复率远高于正确生成，过length过滤通过屏蔽截断样本中的重复模式来维持训练鲁棒性。但阈值的自适应选择仍是开放问题。

### 失败模式与局限

1. **批量归一化的脆弱性**（Figure 4）：当批次内奖励分布偏斜时，批量级归一化会导致性能崩溃，这是其被组级归一化取代的根本原因。
2. **Aligned模型的学习饱和**（Figure 3）：已对齐模型从RL训练中获益有限（约2%增益），Lite PPO在此场景下虽仍优于DAPO，但绝对提升幅度不大。引入Clip Higher可提供额外帮助，但未纳入Lite PPO的最小组合。
3. **AIME24上的反例**（Table 2）：困难数据上DAPO在AIME24子集反超Lite PPO，提示特定任务分布下更复杂的DAPO机制仍有优势。
4. **规模未充分验证**：所有实验限于4B和8B模型，更大规模模型上的结论需进一步验证。
5. **多轮RL与SFT联合优化**：未探索Lite PPO在迭代RL或与SFT损失联合训练下的表现。

### 关键图表结论速查

| 图表 | 核心结论 |
|------|---------|
| Figure 4 | 组均值归一化是实现稳定训练的基石；批量归一化易崩溃 |
| Figure 5 | 奖励分布集中时去除标准差增强稳定性 |
| Figure 6 | 组均值+批量标准差优于组均值+组标准差 |
| Figure 7 | Clip Higher减缓Aligned模型的熵崩塌 |
| Figure 9 | Token级损失在Base模型上有效，Aligned模型上增益有限 |
| Table 3 | Lite PPO在Llama3-8B上大幅领先GRPO（+7.5 on MATH-500） |
| Table 4 | Lite PPO泛化至编码、QA、语言理解基准 |

## 方法谱系与知识库定位

### 1. 问题定位：RL4LLM 的技术碎片化

当前将强化学习用于大语言模型推理（RL4LLM）的研究面临一个核心瓶颈：**缺乏标准化的使用指南和机制理解**。不同工作（如 GRPO、DAPO、REINFORCE++ 等）在模型初始化、训练数据、奖励设计、优势归一化策略、损失聚合方式等维度上各自采用不同配置，导致实验结论相互冲突，严重阻碍了从业者的实际应用。Figure 1 直观地展示了这种技术扩散现象：左侧是层出不穷的 RL 优化技巧与多样化的初始模型/数据组合，右侧则是本文通过机制剖析建立的系统化应用指南。

### 2. 方法谱系：从 Vanilla PPO 到 Lite PPO 的简化路径

#### 2.1 基线方法定位

本文的方法谱系围绕 **无 critic 的 PPO 策略优化**展开，核心基线包括：

- **Vanilla PPO (critic-free)**（Schulman et al., 2017）：标准 PPO 裁剪代理目标，去除价值函数后使用 REINFORCE 估计优势。其损失函数为：
  $$\mathcal{T}_{\mathrm{PPO}}(\theta) = \mathbb{E}_{[q \sim P(Q), o \sim \pi_{\theta_{\mathrm{old}}}(O \mid q)]} \frac{1}{|o|} \sum_{t=1}^{|o|} \min\left(\frac{\pi_{\theta}(o_t | q, o_{<t})}{\pi_{\theta_{\mathrm{old}}}(o_t | q, o_{<t})} A_t, \mathrm{clip}\left(\frac{\pi_{\theta}(o_t | q, o_{<t})}{\pi_{\theta_{\mathrm{old}}}(o_t | q, o_{<t})}, 1-\epsilon, 1+\epsilon\right) A_t\right)$$

- **GRPO**（Shao et al., 2024）：采用组级（group-level）优势归一化，对每个 prompt 的 K 个回复用组内均值和标准差归一化，并引入 KL 散度正则项以约束策略偏离参考模型。其损失形式为：
  $$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{[q \sim P(Q), \{\alpha_i\}_{i=1}^{\infty} \sim \pi_{\theta_{\mathrm{old}}}(O | q)]} \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|\omega_i|} \sum_{t=1}^{|\omega_i|} \{\min(r_{i,t}(\theta) \hat{A}_{i,t}, \exp(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_{i,t}) - \beta D_{\mathrm{KL}}[\pi_{\theta} \| \pi_{\mathrm{ref}}]\}$$

- **DAPO**（Yu et al., 2025）：引入解耦的上下界 clip（$\epsilon_{\mathrm{low}}$ 和 $\epsilon_{\mathrm{high}}$）和 token 级损失聚合，以鼓励探索。其目标为：
  $$\mathcal{I}_{\mathrm{DAPO}}(\theta) = \mathbb{E}_{[(q,a) \sim \mathcal{D}, \{o_i\}_{i=1}^{G} \sim \pi_{\theta_{\mathrm{old}}}(\cdot | q)]} \frac{1}{\sum_{i=1}^{G} |o_i|} \sum_{i=1}^{G} \sum_{t=1}^{|o_i|} \{\min(r_{i,t}(\theta) \hat{A}_{i,t}, \mathrm{clip}(r_{i,t}(\theta), 1-\epsilon_{\mathrm{low}}, 1+\epsilon_{\mathrm{high}}) \hat{A}_{i,t})\}$$

- **REINFORCE++**（Hu et al., 2025）：采用批量级（batch-level）优势归一化，用整个批次的均值和标准差进行归一化。

#### 2.2 关键技术分歧与消融发现

本文通过超过 160 次独立训练运行的系统性消融，揭示了现有技术之间的关键分歧及其实际效果：

**优势归一化策略的分歧**：GRPO 和 RLOO 主张组级归一化以促进组内竞争，而 REINFORCE++ 则采用批量级归一化以缓解过拟合和奖励黑客（reward hacking）。此外，GRPO 在归一化中保留了标准差，但 Dr. GRPO（Liu et al., 2025b）明确建议去除标准差归一化以防止偏差。本文的消融实验（Figure 4-6）表明：
- 组级均值计算在训练稳定性和最终性能上一致优于批量级均值（批量级对奖励分布偏斜高度敏感，常导致性能崩溃）
- 去除标准差在奖励分布高度集中的简单数据集上显著增强训练稳定性（Takeaway 1）
- 批量级标准差计算优于组级标准差，提供更强的梯度幅度约束（Takeaway 2）

**损失聚合粒度的选择**：序列级损失（每条序列所有 token 取均值）与 token 级损失（逐 token 计算优势加权损失）之间存在显著差异。实验表明，token 级损失在基础模型上能提升收敛速度和峰值准确率，但在指令模型上增益有限（Figure 9）。

#### 2.3 Lite PPO：最小有效组合

基于上述消融发现，本文提出 **Lite PPO**，仅需结合两种技术即可最大化无 critic PPO 策略的学习能力：
1. **优势归一化**：使用组均值 + 批量标准差，即 $A_k^{\mathrm{mixed}} = \frac{r_k - \mathrm{mean}(\{r_j\}_{j=1}^{K})}{\mathrm{std}(\{r_j\}_{j=1}^{N \times K})}$
2. **Token 级损失聚合**：逐 token 计算优势加权的 PPO 裁剪损失

这一最小组合在多个基准上超越了更复杂的 GRPO 和 DAPO 等方法：在 MATH-500 上达 91.43%（vs DAPO 90.57%），在 AMC23 困难数据上达 75.42%（vs DAPO 68.54%），在 AIME25 上达 46.67%（vs DAPO 38.34%）。

### 3. 适用边界与局限

#### 3.1 已验证的适用范围

- **模型规模**：实验覆盖 4B 和 8B 参数量的模型（Qwen3 系列、Llama3-8B），更大规模模型上的结论尚未验证
- **模型类型**：基础模型（Base）和对齐模型（Aligned）均有覆盖，但 Lite PPO 在非对齐模型上的增益更为显著（Figure 12）
- **任务领域**：主要集中在数学推理任务（MATH-500、AMC23、AIME25），对编码（LCB-v5）、科学问答（GPQA）等其他推理模态的泛化性仅通过少量基准验证
- **数据难度**：覆盖简单、中等、困难三个难度级别的训练数据

#### 3.2 已知局限

1. **奖励设计依赖性**：Lite PPO 的增益可能依赖于所用的奖励设计和训练数据分布，在不同奖励机制下的鲁棒性有待进一步验证
2. **过长度过滤阈值**：8k 长度阈值的过长度过滤能提升学习，但 20k 阈值收益减少（Figure 10），最优阈值如何根据任务长度分布自适应调整尚未充分探索
3. **多轮训练效应**：未深入分析多轮 RL 训练或与 SFT 损失联合优化的效应
4. **Clip Higher 的补充作用**：虽然 Lite PPO 本身不包含 Clip Higher，但实验表明 Clip Higher 能减缓已对齐模型的熵崩塌（Figure 7），其与 Lite PPO 的组合在已对齐模型上可能带来额外增益

### 4. 开放问题

1. **场景适配性**：现有众多 RL 技术（组级/批量级归一化、有/无标准差、序列级/token 级损失、Clip Higher 等）各自最适用于哪些具体场景（模型类型、数据难度、奖励机制）？
2. **自适应 clip 上界**：如何针对不同模型尺寸和架构自动选择最优的 clip 上界？实验表明 4B 模型在 clip 上界 0.32 时最优，而 8B 模型在 0.28 时最优（Figure 8）
3. **Token 级损失的边界条件**：Token 级损失聚合是否在所有初始化条件下都优于序列级损失，或者存在特定反例（如在高度对齐的指令模型上）？
4. **过长度过滤的自适应阈值**：掩码阈值应如何根据任务长度分布自适应调整，以在长链推理任务中平衡探索与效率？
5. **Lite PPO 的扩展性**：在更大规模模型（>8B）和更多样化的推理任务上，Lite PPO 的最小组合是否仍然足够，还是需要引入其他轻量级技术？

## 原文 PDF

![[paperPDFs/ICLR_2026/Tricks_or_Traps_A_Deep_Dive_into_RL_for_LLM_Reasoning.pdf]]
