---
title: "Exploratory Diffusion Model for Unsupervised Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Exploratory_Diffusion_Model_for_Unsupervised_Reinforcement_Learning.pdf
project_link: null
code_link: https://github.com/yingchengyang/ExDM
openreview_forum_id: k0Kb1ynFbt
aliases:
- EDME
- EDMURL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "利用扩散模型的得分函数定义内在奖励 R_score，通过测量模型对回放状态的拟合误差来量化状态的“未访问程度”，引导探索未知区域；同时将预训练扩散模型作为下游微调的先验。"
primary_logic: "扩散模型不仅能生成高质量样本，其密度估计能力可化为探索信号：将扩散模型在回放状态上的预测误差作为内在奖励，驱动智能体向未充分覆盖的区域移动；解耦建模与行动（高斯行为策略采集数据，扩散策略表示分布）兼顾了探索能力和训练效率，且预训练的扩散先验使少样本微调具备理论收敛保证。"
claims:
- "ExDM 在所有 7 个 Maze2d 场景中均取得最高或持平的状态覆盖率，尤其在 Square-bottleneck 上达到 0.75±0.15，远超最强基线 (MEPOL 0.62±0.01)。"
- "ExDM 在 URLB 单实施例和跨实施例设置下的聚合指标 IQM 分别达到 0.80 和 0.80，比第二最优方法高出 13 ‒ 14 个百分点。"
- "ExDM 的预训练仅需 50 万步即可超过所有基线在 200 万步时的微调性能。"
- "定理 4.1 证明了最大熵策略以高概率为非确定性策略，从而要求策略具备足够的表达力，这为使用扩散模型提供了理论支撑。"
---

# Exploratory Diffusion Model for Unsupervised Reinforcement Learning

> [!tip] 核心洞察
> 扩散模型不仅能生成高质量样本，其密度估计能力可化为探索信号：将扩散模型在回放状态上的预测误差作为内在奖励，驱动智能体向未充分覆盖的区域移动；解耦建模与行动（高斯行为策略采集数据，扩散策略表示分布）兼顾了探索能力和训练效率，且预训练的扩散先验使少样本微调具备理论收敛保证。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 探索性扩散模型用于无监督强化学习 |
| 英文题名 | Exploratory Diffusion Model for Unsupervised Reinforcement Learning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=k0Kb1ynFbt) · [GitHub](https://github.com/yingchengyang/ExDM) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Exploratory Diffusion Model (ExDM) |
| Dataset | Maze2d, URLB Single-Embodiment, URLB Cross-Embodiment |

> [!tip] 效果简介
> - Maze2d 上，State Coverage (均值 ± 标准差) 为 ExDM: 0.75±0.15，对比 MEPOL: 0.62±0.01 (Square-bottleneck)，变化 ↓ 0.13 绝对提升。
> - Maze2d 上，State Coverage (均值 ± 标准差) 为 ExDM: 0.71±0.07，对比 MEPOL: 0.59±0.04 (Square-large)，变化 ↓ 0.12 绝对提升。
> - URLB Single-Embodiment 上，Aggregate IQM (置信区间) 为 ExDM: 0.80 [0.76, 0.84]，对比 CeSD: 0.71 [0.67, 0.76]，变化 提升 13%。

## 概要

无监督强化学习（URL）的核心瓶颈在于：预训练探索产生的回放数据高度异构且非平稳，现有策略（如单一高斯策略或离散技能策略）的表达能力不足以准确建模状态分布，导致内在奖励信号失真，并严重限制了下游任务微调的泛化能力。

本文提出 **Exploratory Diffusion Model (ExDM)**，首次将扩散模型引入无监督 RL。其核心机制是：在回放缓冲区上在线训练状态扩散模型，利用其得分函数的预测误差定义内在奖励 $\mathcal{R}_{\mathrm{score}}$——误差越大，表明状态越“陌生”，从而驱动智能体向未充分探索的区域移动。同时，ExDM 采用**解耦架构**：以轻量高斯行为策略负责高效在线采样，以扩散策略负责建模多样化行为模式，兼顾了探索能力与训练效率。预训练完成后，扩散模型直接作为下游微调的强先验，通过交替优化 Q 函数与扩散策略蒸馏实现少样本适应，并具备理论上的单调改进与最优收敛保证。

实验表明，ExDM 在 Maze2d 所有 7 个场景中均取得最高或持平的状态覆盖率，尤其在最具挑战性的 Square-bottleneck 迷宫上达到 0.75±0.15，远超最强基线 MEPOL（0.62±0.01）。在 URLB 基准上，ExDM 的单实施例与跨实施例聚合指标 IQM 均达到 0.80，比第二优方法高出 13–14 个百分点。消融研究进一步验证了预训练扩散先验的样本效率：仅需 50 万预训练步，ExDM 的微调性能即超过所有基线在 200 万步时的表现。

ExDM 的局限性在于扩散策略在极低交互量下的采样效率仍不及高斯策略，且在线训练扩散模型带来额外计算开销（Maze2d 约 0.5 天/种子，URLB 约 2 天/种子）。当前方法面向完全可观测的单任务连续控制，其在部分观测、多智能体或图像输入场景下的有效性仍有待验证。

### 无监督强化学习的核心挑战

无监督强化学习（Unsupervised RL, URL）旨在让智能体在无奖励环境中自主探索，获取可泛化的行为先验，再通过少量交互快速适应下游任务。其核心瓶颈在于：**探索阶段产生的回放数据高度异构且非平稳**。智能体在无外在奖励引导下自由探索，采集到的状态-动作分布随探索进程不断漂移，呈现出多模态、长尾等复杂特性。

这一数据特性对策略表达能力提出了严峻要求。现有主流方法存在明显缺口：

- **高斯策略**（如 DDPG、PPO 中常用的单峰高斯分布）表达能力有限，无法准确覆盖回放缓冲区中的多模态状态分布，导致内在奖励估计偏差，探索不充分。
- **技能基策略**（如 **DIAYN** (Eysenbach et al., 2018)、**SMM** (Lee et al., 2019)、**CIC** (Laskin et al., 2022) 等）通过离散隐变量或互信息最大化学习多样化行为，但其技能空间通常是离散且有限的，难以精细建模连续状态空间中的复杂分布结构。

论文通过定理 4.1 从理论上证明了：**最大熵策略以高概率为非确定性策略**，这要求策略必须具备足够的表达力来捕捉环境中的多模态行为。这一理论结果直接指明了现有方法的根本局限——简单分布族无法胜任无监督探索的建模需求。

### 扩散模型的潜力与直接应用的障碍

扩散模型近年来在连续控制中展现出强大的异构行为建模能力，通过逐步去噪过程可以表示任意复杂的动作分布。这恰好回应了 URL 对高表达力策略的需求。然而，将扩散模型直接引入无监督 RL 面临两个关键障碍：

1. **采样效率瓶颈**：扩散策略的多步去噪采样（通常需 5-20 步）远慢于高斯策略的单步前向传播，在需要大量在线交互的探索阶段会严重拖慢数据采集速度。
2. **非平稳数据流的适配**：扩散模型通常针对固定数据集训练，而 URL 的回放分布随探索不断演化，如何在非平稳数据流上稳定训练扩散模型并提取有效的探索信号，尚无成熟方案。

### 本文动机与核心思路

针对上述缺口，本文提出 **探索性扩散模型（Exploratory Diffusion Model, ExDM）**，核心动机是**将扩散模型的密度估计能力转化为探索驱动力**，同时通过架构解耦规避采样效率问题。

具体而言，ExDM 沿着两条主线展开：

- **探索阶段**：在回放数据上在线训练状态扩散模型，将其预测误差（即得分函数对当前状态的拟合质量）定义为内在奖励 $\mathcal{R}_{\mathrm{score}}$。该奖励直接量化状态的“未访问程度”——模型对某状态预测误差越大，说明该状态在回放分布中越罕见，智能体应优先探索。同时，采用**解耦架构**：用轻量高斯行为策略 $\pi_g$ 负责高效采样交互，扩散模型仅负责分布建模与奖励计算，兼顾了表达力与采样效率。

- **微调阶段**：预训练的动作扩散模型 $\pi_d$ 作为强行为先验，通过交替优化 Q 函数（基于 IQL 的 expectile 回归）与扩散策略蒸馏（基于对比能量预测 CEP 的 guided sampling），在少量在线交互下将任务奖励注入扩散策略，理论保证单调改进与最优收敛（定理 4.2）。

这一设计将扩散模型从单纯的“生成器”角色提升为“探索信号源”与“微调先验”的双重枢纽，为无监督 RL 提供了新的技术范式。

## 核心方法与创新机理

ExDM 针对无监督强化学习（URL）中“探索回放数据高度异构、传统策略表达能力不足”这一瓶颈，提出了三个层面的关键创新，其核心机制可概括为**扩散建模驱动探索、解耦架构保障效率、扩散先验赋能微调**。

### 创新一：基于扩散模型预测误差的得分内在奖励

传统 URL 方法的内在奖励通常依赖手工设计的不确定性度量（如 RND 的预测误差、Disagreement 的集成分歧）或状态熵的近似估计（如 RE3 的 k-NN 熵、MEPOL 的粒子熵）。这些方法在面对 Maze2d 等复杂环境中产生的多模态、非平稳回放分布时，密度估计精度不足，导致探索信号失真。

ExDM 的核心突破在于**将扩散模型的密度估计能力转化为探索信号**。具体而言，ExDM 在回放缓冲区上在线训练一个状态扩散模型 $\epsilon_{\theta'}$，该模型学习回放状态分布 $p(s)$ 的得分函数。对于任意状态 $s$，其得分内在奖励定义为扩散模型在该状态上的预测误差：

$$\mathcal{R}_{\mathrm{score}}(s) = \mathbb{E}_{\epsilon, t} \left[ \| \epsilon_{\theta'}(s_t | t) - \epsilon \|^2 \right]$$

这一设计的理论依据在于：扩散模型的去噪得分匹配损失与状态负对数似然 $-\log p_{\theta'}(s)$ 通过证据下界（ELBO）相关联——预测误差越大，表明该状态在当前回放分布下的似然越低，即“未被充分访问”。因此，$\mathcal{R}_{\mathrm{score}}$ 直接量化了状态的新颖程度，引导智能体向模型尚未覆盖的区域移动。

**证据强度**：Table 1 显示，ExDM 在 Maze2d 的 7 个场景中均取得最高或持平的状态覆盖率，尤其在 Square-bottleneck 上达到 $0.75 \pm 0.15$，远超最强基线 MEPOL 的 $0.62 \pm 0.01$，验证了得分内在奖励对异构状态分布建模的显著优势。

### 创新二：建模与行动解耦的架构设计

扩散策略虽表达力强，但其多步采样过程（通常需 5–100 步去噪）在在线交互中效率极低，直接用于探索将严重拖慢数据收集速度。ExDM 通过**解耦架构**解决了这一矛盾：

- **高斯行为策略 $\pi_g$**：一个轻量级的对角高斯策略，由 DDPG 以 $\mathcal{R}_{\mathrm{score}}$ 为奖励训练，负责高效的在线动作采样与数据收集。
- **扩散策略 $\pi_d$**：在回放数据上离线训练，精确建模状态-动作分布，为下游微调提供强先验，但不参与在线交互。

这种设计使得 ExDM 在预训练阶段的计算开销与标准高斯策略方法相当（Maze2d 约 0.5 天/种子），同时保留了扩散模型对异构行为的高保真建模能力。Theorem 4.1 进一步从理论上证明了最大熵策略以高概率为非确定性策略，从而要求策略具备足够的表达力——这为使用扩散模型而非单一高斯策略提供了理论支撑。

### 创新三：基于扩散先验的交替优化微调框架

传统 URL 方法在预训练后通常直接使用 DDPG 或 PPO 在下游任务上微调高斯策略，丢弃了预训练阶段学到的行为先验。ExDM 则**将预训练的扩散策略作为下游微调的强先验**，通过交替优化实现高效适应。

微调目标在最大化任务回报 $J(\pi)$ 的同时，惩罚当前策略与预训练扩散策略 $\pi_d$ 之间的 KL 散度：

$$\max_{\pi} J_{\mathrm{f}}(\pi) \triangleq J(\pi) - \frac{\beta}{(1-\gamma)} \mathbb{E}_{s \sim d_{\pi}} \left[ D_{\mathrm{KL}}(\pi(\cdot|s) \| \pi_{\mathrm{d}}(\cdot|s)) \right]$$

ExDM 将优化解耦为两个交替执行的步骤：
1. **Q 函数优化**：采用 IQL 的 expectile 回归学习 Q 函数，隐式惩罚与 $\pi_d$ 偏差过大的动作，避免灾难性遗忘。
2. **扩散策略蒸馏**：通过对比能量预测（CEP）训练能量引导网络 $f_\phi$，使其近似 Q 值加权的采样梯度，再将基础扩散得分与能量引导蒸馏为新的扩散策略 $\epsilon_\psi$。

Theorem 4.2 证明了该交替优化过程保证策略单调改进并收敛到最优解。Figure 4(a) 的消融实验表明，ExDM 仅需 50 万预训练步即可超过所有基线在 200 万步时的微调性能，验证了扩散先验对少样本适应的关键作用。

### 方法谱系与知识库定位

ExDM 在 URL 方法谱系中占据独特位置，其设计融合了多个研究脉络的要素：

| 设计维度 | 传统方法 | ExDM 的差异化 |
|---------|---------|-------------|
| **内在奖励** | RND（Burda et al., 2018）的随机网络预测误差；RE3（Seo et al., 2021）的 k-NN 熵估计 | 扩散模型得分误差，直接关联状态负对数似然，密度估计更精确 |
| **状态分布建模** | MEPOL（Mutti et al., 2021）的粒子熵最大化；CIC（Laskin et al., 2022）的对比学习 | 在线训练扩散模型，可精确建模多模态、非平稳分布 |
| **策略结构** | DIAYN（Eysenbach et al., 2018）的离散技能；SMM（Lee et al., 2019）的混合技能 | 高斯行为策略 + 扩散策略解耦，兼顾效率与表达力 |
| **下游微调** | PEAC（Ying et al., 2024）的策略蒸馏；DQL（Wang et al., 2023）的离线扩散 Q 学习 | 交替优化 Q 函数与扩散策略蒸馏，理论保证单调改进 |

在 URLB 单实施例和跨实施例设置下，ExDM 的聚合指标 IQM 分别达到 0.80 和 0.80，比第二最优方法（CeSD 和 PEAC）高出 13–14 个百分点（Table 4, Table 6），确立了其在无监督 RL 预训练-微调范式中的领先地位。

**需人工验证**：ExDM 在极低数据量下扩散策略微调性能仍低于高斯策略微调（Figure 3(c)），表明扩散采样效率仍是瓶颈，论文将此列为开放问题。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_k0Kb1ynFbt/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Exploratory Diffusion Model (ExDM). Different from standard RL, URL aims to explore in reward-free environments, requiring expressive policies and models to fit heterogeneous data (Theorem 4.1). During pre-training, ExDM employs the diffusion model to model the heterogeneous exploration data and calculate score-based intrinsic rewards to encourage exploration. Moreover, we adopt a Gaussian behavior policy to collect data that avoids the inefficiency caused by the multi-step sampling of the diffusion policy*

ExDM 的整体设计围绕一个核心矛盾展开：无监督探索产生的回放数据高度异构且非平稳，传统高斯策略或技能基策略的表达能力不足，难以准确建模状态分布，进而限制了内在奖励的有效性和下游适应的泛化能力。为此，ExDM 构建了一个**建模与行动解耦**的两阶段流水线，其架构如 **Figure 1** 所示。

### 预训练阶段：扩散建模 + 高斯采样

预训练阶段包含三条并行的数据流，共同完成“探索—建模—奖励”的闭环。

**扩散模型双通道训练。** ExDM 在回放缓冲区 $\mathcal{D}$ 上同时训练两个扩散模型：状态扩散模型 $\epsilon_{\theta'}$ 和状态-条件动作扩散模型 $\epsilon_{\theta}$。二者的训练目标均为最小化噪声预测的均方误差（公式 6），分别学习状态分布 $p(s)$ 和条件动作分布 $p(a|s)$ 的得分函数。这一设计使得扩散模型能够精确捕捉异构回放数据中的多模态行为模式，为后续的内在奖励计算和下游微调提供密度估计基础。

**得分内在奖励驱动探索。** 状态扩散模型的预测误差被直接转化为探索信号。具体而言，对于任意状态 $s$，得分内在奖励定义为：
$$\mathcal{R}_{\mathrm{score}}(s) = \mathbb{E}_{\epsilon, t}\left[\|\epsilon_{\theta'}(s_t|t) - \epsilon\|^2\right]$$
该奖励与状态的负对数似然通过 ELBO 相关联——扩散模型对某状态的预测误差越大，意味着该状态在回放分布中的密度越低，即越“陌生”。因此，最大化 $\mathcal{R}_{\mathrm{score}}$ 等价于引导智能体向尚未充分覆盖的区域移动。相比手工设计的不确定性度量或状态熵近似，这一奖励信号直接依赖扩散模型对回放分布的拟合质量，具有明确的理论依据。

**高斯行为策略高效采样。** 扩散策略的多步采样在在线交互中计算开销巨大。ExDM 通过引入一个轻量级的高斯行为策略 $\pi_g$ 来规避这一瓶颈：$\pi_g$ 由任意离线 RL 算法（实践中采用 DDPG）以 $\mathcal{R}_{\mathrm{score}}$ 为奖励进行训练，负责与环境交互并采集数据。扩散模型仅承担分布建模的角色，不参与在线动作生成。这种解耦在保持建模表达力的同时，将采样效率提升至与传统高斯策略相当的水平。

**数据闭环。** $\pi_g$ 采集的交互数据被存入回放缓冲区 $\mathcal{D}$，用于更新两个扩散模型；扩散模型的预测误差又反过来构成 $\pi_g$ 的内在奖励。这一循环持续推动探索边界的扩展，直至预训练步数耗尽。

### 微调阶段：交替优化 + 扩散蒸馏

下游任务微调的目标是在最大化任务回报的同时，避免对预训练先验的灾难性遗忘。ExDM 将这一目标形式化为带 KL 惩罚的优化问题（公式 9），并通过交替优化 Q 函数与扩散策略来求解。

**Q 函数优化。** 采用 Implicit Q-Learning (IQL) 的 expectile 回归框架，隐式地惩罚与预训练扩散策略 $\pi_d$ 偏差过大的动作，从而在不显式计算 KL 散度的情况下实现分布约束。

**扩散策略蒸馏。** 给定优化后的 Q 函数 $Q_{n-1}$，目标策略的理论最优形式为 $\pi_n \propto \pi_d \cdot e^{Q_{n-1}/\beta}$（公式 12）。ExDM 通过对比能量预测（CEP）训练一个能量引导网络 $f_\phi$ 来近似这一加权分布的得分梯度（公式 13），随后将基础扩散得分与能量引导相加，通过得分蒸馏训练微调后的扩散策略 $\epsilon_\psi$（公式 14）。这一过程可迭代多轮，理论保证策略单调改进并收敛至最优解（定理 4.2）。

### 模块关系总结

ExDM 的六个核心模块及其数据流关系如下：

| 模块 | 阶段 | 输入 | 输出 | 作用 |
|------|------|------|------|------|
| 高斯行为策略 $\pi_g$ | 预训练 | 状态 $s$，$\mathcal{R}_{\mathrm{score}}$ | 动作 $a$，交互数据 | 高效在线采样，驱动探索 |
| 状态扩散模型 $\epsilon_{\theta'}$ | 预训练 | 回放状态 $s$ | $\mathcal{R}_{\mathrm{score}}(s)$ | 建模状态分布，生成内在奖励 |
| 动作扩散模型 $\epsilon_\theta$ | 预训练 | 回放状态-动作对 $(s,a)$ | 预训练扩散策略 $\pi_d$ | 建模行为分布，提供微调先验 |
| IQL Q 函数优化 | 微调 | 任务奖励 $\mathcal{R}$，$\pi_d$ | Q 函数 $Q$ | 学习任务相关的值函数，约束策略偏移 |
| CEP 能量引导 $f_\phi$ | 微调 | $Q$，$\pi_d$ 采样动作 | 能量梯度 | 近似 Q 值加权的扩散采样方向 |
| 蒸馏扩散策略 $\epsilon_\psi$ | 微调 | $\epsilon_\theta$，$f_\phi$ | 微调后策略 | 融合任务知识与探索先验，生成最终动作 |

该流水线的关键设计决策在于**预训练阶段建模与行动的彻底解耦**：扩散模型专注于精确密度估计，高斯策略专注于高效采样，二者各司其职，避免了扩散采样效率低与高斯策略表达弱的两难困境。这一解耦范式也为将其他生成模型（如流模型、变分自编码器）引入无监督 RL 提供了可复用的架构模板。

ExDM 的核心架构由三个解耦模块构成，分别负责分布建模、探索采样与下游微调。其公式体系围绕扩散模型的噪声预测误差展开，将密度估计能力转化为探索信号与策略先验。

### 4.1 扩散模型训练与得分内在奖励

ExDM 在回放缓冲区 $\mathcal{D}$ 上同时训练两个扩散模型：状态扩散模型 $\epsilon_{\theta'}$ 和状态条件动作扩散模型 $\epsilon_\theta$。训练目标为联合噪声预测均方误差：

$$
\operatorname*{min} \mathbb{E}_{s, a \sim \mathcal{D}} \left[ \mathbb{E}_{t, \epsilon} \| \epsilon_{\theta'}(s_t | t) - \epsilon \|^2 + \mathbb{E}_{t, \epsilon} \| \epsilon_{\theta}(a_t | s, t) - \epsilon \|^2 \right]
$$

其中 $s_t = \alpha_t s + \sigma_t \epsilon$ 为前向扩散过程（$\mathbf{a}_t = \alpha_t \mathbf{a} + \sigma_t \mathbf{\epsilon}, t \in [0,1]$）注入噪声后的状态。该损失通过证据下界（ELBO）与状态的负对数似然相关联：

$$
-\log p_{\theta'}(s) \leq \mathbb{E}_{\epsilon, t} [ w_t \| \epsilon_{\theta'}(s_t | t) - \epsilon \|^2 ] + C
$$

基于此关系，ExDM 直接将状态扩散模型的预测误差定义为**得分内在奖励** $\mathcal{R}_{\mathrm{score}}$：

$$
\mathcal{R}_{\mathrm{score}}(s) = \mathbb{E}_{\epsilon, t} \left[ \| \epsilon_{\theta'}(s | t) - \epsilon \|^2 \right]
$$

**因果机制**：扩散模型在频繁访问的状态上预测误差低，在未充分探索的状态上预测误差高。因此 $\mathcal{R}_{\mathrm{score}}$ 天然量化了状态的“陌生程度”——误差越大，说明该状态越偏离回放分布，智能体应被引导前往。这一设计将密度估计能力直接转化为探索驱动力，无需手工设计不确定性度量。

### 4.2 解耦采样架构

扩散策略的多步采样在在线交互中效率过低。ExDM 引入**高斯行为策略** $\pi_g$ 负责实际动作采样，仅需单步前向传播；扩散模型 $\epsilon_\theta$ 专注于建模回放数据中的异构行为分布，不参与实时决策。$\pi_g$ 由任意离线 RL 算法（如 DDPG）结合 $\mathcal{R}_{\mathrm{score}}$ 训练，确保探索效率与表达能力解耦。

### 4.3 下游微调目标

微调阶段，ExDM 将预训练的扩散策略 $\pi_d$（由 $\epsilon_\theta$ 参数化）作为强先验，优化带 KL 正则化的目标：

$$
\max_{\pi} J_f(\pi) \triangleq J(\pi) - \frac{\beta}{(1-\gamma)} \mathbb{E}_{s \sim d_\pi} \left[ D_{\mathrm{KL}}(\pi(\cdot|s) \| \pi_d(\cdot|s)) \right]
$$

其中 $J(\pi) = \frac{1}{1-\gamma} \mathbb{E}_{s \sim d_\pi, a \sim \pi} [\mathcal{R}(s, a)]$ 为任务回报。KL 惩罚项防止策略在少量交互下灾难性遗忘预训练获得的多样化行为先验。

### 4.4 交替优化与扩散策略蒸馏

ExDM 通过交替优化求解 $J_f$。第 $n$ 次迭代的策略提升步具有闭式解：

$$
\pi_n(\cdot|s) = \frac{\pi_d(a|s) e^{Q_{n-1}(s, a)/\beta}}{Z(s)}
$$

其中 $Q_{n-1}$ 由 IQL（隐式 Q 学习）通过 expectile 回归优化，隐式惩罚与 $\pi_d$ 偏差过大的动作。为从 $\pi_n$ 采样，ExDM 使用**对比能量预测（CEP）**训练能量引导网络 $f_{\phi_{n-1}}$：

$$
\operatorname*{min}_{\phi_{n-1}} \mathbb{E}_{t,s} \mathbb{E}_{a^1,\ldots,a^K \sim \pi_d(\cdot|s)} \left[ -\sum_{i=1}^K \frac{e^{Q_{n-1}(s,a^i)/\beta}}{\sum_{j=1}^K e^{Q_{n-1}(s,a^j)/\beta}} \log \frac{f_{\phi_{n-1}}(s, a_t^i, t)}{\sum_{j=1}^K f_{\phi_{n-1}}(s, a_t^j, t)} \right]
$$

该对比损失使 $f_{\phi_{n-1}}$ 近似 Q 值加权的中间能量梯度。最终通过得分蒸馏将基础扩散得分与能量引导合并为微调后的扩散策略 $\epsilon_\psi$：

$$
\operatorname*{min}_{\psi} \mathbb{E}_{s, a, t} \| \epsilon_{\psi}(a_t | s, t) - \epsilon_{\theta}(a_t | s, t) - f_{\phi_{n-1}}(s, a_t, t) \|^2
$$

这一蒸馏过程将交替优化的理论收敛保证（定理 4.2）转化为可高效采样的单一扩散策略，实现少样本微调下的单调改进。

## 实验与关键发现

### 核心发现

ExDM 在两个标准无监督强化学习基准——Maze2d 和 URLB——上均展现出显著优于现有方法的探索能力与下游适应效率。其实验优势可归纳为三个层面：**状态覆盖率**、**下游微调性能**和**样本效率**。

#### Maze2d 探索覆盖率

在 Maze2d 的 7 个迷宫场景中，ExDM 在所有场景下均取得最高或持平的状态覆盖率。关键瓶颈场景的结果如下：

- **Square-bottleneck** 迷宫：ExDM 达到 0.75±0.15，最强基线 MEPOL（Mutti et al., 2021）为 0.62±0.01，绝对提升 0.13。
- **Square-large** 迷宫：ExDM 达到 0.71±0.07，MEPOL 为 0.59±0.04，绝对提升 0.12。
- 简单迷宫 **Square-a** 上 ExDM 达到 0.99±0.02，接近完全覆盖。

定性热图（Figure 2）显示，ExDM 在复杂分支路径和瓶颈区域的探索轨迹密度明显高于其他方法，表明基于扩散模型预测误差的内在奖励能有效引导智能体进入其他方法难以到达的区域。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_k0Kb1ynFbt/figures/003_Figure_2.jpg]]
*Figure 2: Heatmap of explored regions by URL methods in the most complicated mazes. Table 1: State coverage in Maze. We report the mean and std of 10 seeds for each algorithm*

#### URLB 下游微调性能

在 URLB 的两个主要设置下，ExDM 的聚合指标 IQM 均大幅领先：

- **单实施例设置**：ExDM IQM 达 0.80 [0.76, 0.84]，比第二优方法 CeSD（Bai et al., 2024）的 0.71 [0.67, 0.76] 提升约 13%。
- **跨实施例设置**：ExDM IQM 达 0.80 [0.75, 0.83]，比第二优方法 PEAC（Ying et al., 2024）的 0.70 [0.64, 0.76] 提升约 14%。

在扩散策略微调对比中，ExDM 同样显著优于现有扩散在线微调基线（DQL、QSM、DIPO、IDQL），验证了其交替优化 Q 函数与蒸馏扩散策略的有效性。

#### 样本效率

消融实验揭示了 ExDM 的极高样本效率：在仅 50 万预训练步后，ExDM 的微调性能即超过所有基线方法在 200 万步时的性能（Figure 4(a)）。这表明预训练扩散模型为下游任务提供了强先验，使少样本微调具备理论收敛保证。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_k0Kb1ynFbt/figures/005_Figure_4.jpg]]
*Figure 4: Ablation studies*

### 消融研究

**Q 函数优化方法**：ExDM 显著优于其移除 IQL 的变体（ExDM w/o IQL），验证了 IQL 的 expectile 回归在惩罚分布外动作方面的关键作用（Figure 4(b)）。

**扩散采样步数**：微调性能随扩散采样步数增加而提升，当步数超过 5 后趋于稳定（Figure 4(c)）。这表明仅需少量采样步骤即可逼近高质量行为，DPM-Solver 加速采样进一步降低了推理开销。

**正则化系数 β**：ExDM 对 β 不敏感，在较宽的取值范围内表现稳定（Figure 4(d)），说明方法对超参数选择具有鲁棒性。

### 计算开销与局限

ExDM 的预训练需在线训练扩散模型，Maze2d 约需 0.5 天/种子，URLB 约需 2 天/种子。通过解耦高斯行为策略进行采样，避免了扩散策略多步采样的低效问题，使计算开销保持在可接受范围。然而，扩散策略微调的性能在当前有限交互步数下仍低于高斯策略微调，表明极低数据量下扩散采样效率仍是瓶颈，需要进一步研究更高效的单步或蒸馏微调方法。

### 公平性说明

所有基线方法均采用官方实现（URLBench 或对应开源代码库）和相同的 DDPG 主干，预训练步数与微调步数保持一致，使用相同的环境和 10 个随机种子进行重复实验，确保比较公平。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_k0Kb1ynFbt/figures/007_Table_2.jpg]]
*Table 2: Details of hyperparameters used for Maze2d and state-based URLB*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_k0Kb1ynFbt/figures/011_Table_3.jpg]]
*Table 3: Detailed results in URLB of different pre-trained methods that fine-tune Gaussian policies with DDPG. Average cumulative reward (mean of 10 seeds) of the best policy*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_k0Kb1ynFbt/figures/013_Table_5.jpg]]
*Table 5: In Table 5, we further report the detailed results of all methods in the 4 downstream tasks of 2 domains in cross-embodiment URLB, which is much more challenging as the algorithms require handling various embodiments. In both the Walker-mass and Quadruped-mass domains, ExDM obtains state-of-the-art performance in downstream tasks. Overall, there are the most number of downstream tasks that ExDM performs the best, and ExDM significantly outperforms existing exploration algorithms. Table 5: Detailed results in cross-embodiment state-based DMC. Average cumulative reward (mean of 10 seeds) of the best policy*

## 定位与知识库关联

### 1. 方法定位与核心贡献

ExDM 的核心贡献在于将扩散模型首次引入无监督强化学习（URL），解决探索数据高度异构导致现有策略表达能力不足的瓶颈。其方法谱系可从三个维度定位：

- **探索范式**：ExDM 属于**基于预测误差的内在奖励探索**家族，但将误差来源从环境动力学模型（如 **ICM** (Pathak et al., 2017)、**RND** (Burda et al., 2018)）或集成模型分歧（**Disagreement** (Pathak et al., 2019)）迁移到**回放状态分布的扩散模型拟合质量**上。这一设计使内在奖励直接量化状态的“未访问程度”，而非间接的不确定性或新颖性度量。

- **策略表达力**：ExDM 的解耦架构——高斯行为策略 $\pi_g$ 负责高效采样，扩散策略 $\pi_d$ 负责建模多样化行为——是对技能基方法（**DIAYN** (Eysenbach et al., 2018)、**SMM** (Lee et al., 2019)、**CIC** (Laskin et al., 2022)）和状态熵最大化方法（**MEPOL** (Mutti et al., 2021)、**RE3** (Seo et al., 2021)）的互补性改进。定理 4.1 从理论上证明最大熵策略以高概率为非确定性策略，为扩散模型替代单一高斯策略或离散技能策略提供了形式化支撑。

- **下游适应**：ExDM 的微调方案将预训练扩散策略作为强先验，通过 IQL 优化 Q 函数并交替蒸馏扩散策略，区别于直接在线微调高斯策略（DDPG/PPO）的常见做法。在扩散策略微调基线中，ExDM 与 **DQL** (Wang et al., 2023)、**QSM** (Psenka et al., 2023)、**DIPO** (Yang et al., 2023a)、**IDQL** (Hansen-Estruch et al., 2023) 等方法形成直接对比，实验表明 ExDM 在聚合指标上“substantially outperforms”这些基线（Figure 3(c)）。

### 2. 与关键基线的关系

| 基线方法 | 关系定位 | 关键差异 |
|---|---|---|
| **MEPOL** (Mutti et al., 2021) | 直接竞争——状态熵最大化 | ExDM 用扩散模型密度估计替代 MEPOL 的粒子基熵近似，在 Square-bottleneck 上覆盖率从 0.62 提升至 0.75 |
| **RE3** (Seo et al., 2021) | 同属熵估计探索 | RE3 使用随机编码器的 k-NN 熵估计；ExDM 使用扩散模型得分函数，密度估计更精确 |
| **CeSD** (Bai et al., 2024) | URLB 单实施例 SOTA 基线 | ExDM 在聚合 IQM 上领先 13%（0.80 vs 0.71） |
| **PEAC** (Ying et al., 2024) | 跨实施例 URL 基线 | ExDM 在跨实施例 IQM 上领先 14%（0.80 vs 0.70） |
| **CIC** (Laskin et al., 2022) / **BeCL** (Yang et al., 2023b) | 技能发现/对比学习探索 | ExDM 不使用互信息或对比目标，而是直接建模状态分布 |
| **DQL / QSM / DIPO / IDQL** | 扩散策略微调基线 | ExDM 采用交替优化 + CEP 引导蒸馏，理论保证单调改进（定理 4.2） |

### 3. 适用边界

ExDM 的设计适用于以下场景：

- **完全可观测的连续控制任务**：当前方法面向状态基（state-based）URL，未在部分可观测或图像基设定下验证。
- **单任务无监督预训练 + 少样本微调**：预训练阶段无任务奖励，微调阶段交互步数有限。
- **异构探索数据**：当探索策略产生高度多样化的回放数据时，扩散模型的表达能力优势得以体现；若数据分布简单（如单峰高斯），扩散模型的额外计算开销可能不划算。

### 4. 局限性与开放问题

#### 已识别的局限性

1. **扩散策略微调效率瓶颈**：在有限交互步数下，扩散策略微调的性能仍低于高斯策略微调，说明极低数据量下扩散采样效率仍是瓶颈。
2. **在线训练扩散模型的计算开销**：预训练需在线训练扩散模型，Maze2d 约 0.5 天/种子，URLB 约 2 天/种子（通过解耦高斯采样得以部分缓解）。
3. **内在奖励对回放缓冲区质量的依赖**：若缓冲区大小或数据多样性不足，状态分布建模可能不准确，影响探索质量。
4. **环境假设限制**：未验证在部分观测、离线设定或多智能体系统下的效果。

#### 开放问题

1. **高效单步扩散微调**：如何设计更高效的单步或蒸馏扩散策略微调方法，以在极少量在线交互下超越高斯策略？
2. **跨模态扩展**：ExDM 的探索机制能否扩展到部分可观测环境、多智能体系统或基于图像的 URL？
3. **非平稳数据流上的扩散模型稳定性**：当回放分布与真实环境分布差距较大时，扩散模型在非平稳数据流上的学习稳定性理论有待深入研究。
4. **定向探索合成**：是否可以利用扩散模型的生成能力直接合成“困难”状态，以进一步引导定向探索？
5. **通用生成模型范式**：ExDM 的模块化解耦是否可作为一种通用范式，将其他生成模型（如流模型、一致性模型）引入无监督 RL？

## 原文 PDF

![[paperPDFs/ICLR_2026/Exploratory_Diffusion_Model_for_Unsupervised_Reinforcement_Learning.pdf]]
