---
title: "GlobeDiff: State Diffusion Process for Partial Observability in Multi-Agent System"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/GlobeDiff_State_Diffusion_Process_for_Partial_Observability_in_Multi_Agent_System.pdf
openreview_forum_id: 96g2BRsYZX
aliases:
- GGSDA
- GlobeDiff
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将状态推断转化为条件生成任务：引入潜在变量z作为模态选择器，通过条件扩散模型学习完整分布，并利用变分推断对齐先验与后验，避免确定性假设。"
primary_logic: "将多智能体部分可观测性下的状态推断重新定义为多模态条件生成过程，利用扩散模型的去噪能力隐式捕获一对多映射的复杂性，为去中心化执行提供高保真全局状态。"
claims:
- "在SMAC-v2 (PO) Zerg 5v5上，GlobeDiff推断的全局状态与真实状态的Voronoi多边形结构高度相似，且随着训练进度提升。"
- "GlobeDiff在SMAC-v1 (PO)和SMAC-v2 (PO)多数地图上的胜率显著优于LBS、Dynamic Belief和CommFormer基线。"
- "与CPU等参数量的Vanilla MAPPO (Large)相比，GlobeDiff在所有9个任务中均取得明显更高的胜率，证明单纯增加模型容量无法替代显式生成模块。"
- "移除先验网络和KL约束后，GlobeDiff性能显著下降，验证了变分推断对模态选择的重要性。"
---

# GlobeDiff: State Diffusion Process for Partial Observability in Multi-Agent System

> [!tip] 核心洞察
> 将多智能体部分可观测性下的状态推断重新定义为多模态条件生成过程，利用扩散模型的去噪能力隐式捕获一对多映射的复杂性，为去中心化执行提供高保真全局状态。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GlobeDiff：面向多智能体系统部分可观测性的状态扩散过程 |
| 英文题名 | GlobeDiff: State Diffusion Process for Partial Observability in Multi-Agent System |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=96g2BRsYZX) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | GlobeDiff (Global State Diffusion Algorithm) |
| Dataset | SMAC-v2 PO zerg 5v5, SMAC-v2 PO protoss 5v5, SMAC-v2 PO terran 5v5, SMAC-v2 PO zerg 10v10 |

> [!tip] 效果简介
> - SMAC-v2 PO zerg 5v5 上，Win Rate 为 0.33 ± 0.02，对比 0.22 ± 0.01 (Vanilla MAPPO)，变化 +0.11。
> - SMAC-v2 PO protoss 5v5 上，Win Rate 为 0.38 ± 0.01，对比 0.21 ± 0.02 (Vanilla MAPPO)，变化 +0.17。
> - SMAC-v2 PO terran 5v5 上，Win Rate 为 0.24 ± 0.01，对比 0.16 ± 0.01 (Vanilla MAPPO)，变化 +0.08。

## 概述

多智能体强化学习（MARL）的部分可观测性导致了一个根本性瓶颈：局部观测到全局状态之间存在一对多的映射关系。传统判别式方法（如基于RNN或Transformer的状态推断模块）将这种多模态分布强行坍缩为单点估计，不可避免地造成模态坍塌和信息丢失，限制了去中心化策略的质量。

GlobeDiff 将状态推断重新定义为**条件生成任务**。其核心思路是引入潜在变量 $z$ 作为模态选择器，通过条件扩散模型显式学习从局部观测到全局状态的完整多模态分布，并利用变分推断对齐先验与后验网络，从而在推理时无需访问真实全局状态即可生成高保真的全局状态估计。该方法在理论上有两个支撑：单样本期望误差界（Theorem 1）将推断误差分解为扩散近似误差与条件方差之和；多模态误差界（Theorem 2）进一步刻画了生成样本与最近模态中心之间的期望距离，并给出了指数衰减的模态混淆项。

在实验层面，GlobeDiff 在 SMAC-v1 (PO) 和 SMAC-v2 (PO) 的多数地图上显著优于 LBS、Dynamic Belief 和 CommFormer 等全局状态推断基线。例如，在 SMAC-v1 (PO) 的 6h_vs_8z 任务上，GlobeDiff 的胜率达到 0.47±0.04，而 Vanilla MAPPO 仅为 0.12±0.01。与等参数量的 Vanilla MAPPO (Large) 的对比进一步表明，单纯增加模型容量无法替代显式的生成式建模。消融实验验证了先验网络与 KL 约束对模态选择的关键作用，移除后性能显著下降。状态可视化（Figure 5）则从定性角度展示了 GlobeDiff 推断的全局状态与真实状态在 Voronoi 多边形结构上的高度相似性。

**方法定位**：GlobeDiff 属于 CTDE（集中训练、分散执行）范式下的生成式状态推断方法，通过条件扩散模型桥接局部观测与全局状态之间的信息鸿沟，为下游策略网络提供高保真的全局上下文，而不依赖复杂的显式通信协议。

## 背景与动机

### 多智能体部分可观测性的核心困境

多智能体强化学习（MARL）在现实场景中面临一个根本性挑战：**部分可观测性**。每个智能体只能通过自身有限的传感器获取局部观测，而无法直接访问环境的完整全局状态。这种信息缺失在合作型多智能体任务中尤为致命——智能体需要在无法感知队友位置、敌方动向和全局态势的条件下做出协调决策。

从信息论角度看，部分可观测性制造了一个**一对多映射问题**：同一个局部观测可能对应多种截然不同的全局状态。例如，在星际争霸微操场景中，一个智能体观测到前方没有敌人，可能意味着敌人确实不存在，也可能意味着敌人正隐藏在视野盲区中准备伏击。这种多模态性要求状态推断模型能够捕捉分布的全部可能性，而非仅输出一个“平均化”的猜测。

### 现有方法的瓶颈：确定性假设与模态坍塌

当前主流方法将状态推断建模为**确定性映射**，试图从历史观测序列中直接回归出单一全局状态。典型做法是使用循环神经网络（RNN）或Transformer编码观测历史，输出一个最大似然估计。这种做法存在两个结构性缺陷：

1. **分布坍缩**：确定性模型将多模态条件分布 $p(s \mid x)$ 压缩为单点估计，丢失了分布中其他可能模态的信息。当真实状态恰好不在主模态时，推断结果会产生系统性偏差。

2. **容量误用**：即使大幅增加模型参数量，RNN/Transformer 的记忆机制本质上是在学习一种隐式平均，而非真正的多模态建模。这意味着模型容量的提升无法根本解决模态坍塌问题——正如本文实验所验证的，与 GlobeDiff 等参数量的 Vanilla MAPPO（Large）在所有9个任务中均未取得显著提升。

现有的改进尝试包括：**LBS**（Learned Belief Search, Hu et al., 2021）使用自回归反事实信念模型近似隐藏信息；**Dynamic Belief**（Zhai et al., 2023）通过预测其他智能体策略进行动态信念推断；**CommFormer**（Hu et al., 2024）设计动态通信图实现消息传递。然而，这些方法要么仍依赖于确定性假设，要么需要复杂的显式通信协议，未能从根本上解决一对多映射带来的分布学习问题。

### 核心动机：将状态推断重新定义为条件生成

本文的核心洞察在于：**部分可观测性下的全局状态推断本质上是一个多模态条件生成任务**，而非确定性回归问题。给定局部观测 $x$，存在多种合理的全局状态假设，每种假设对应分布的一个模态。因此，理想的推断模型应当能够：

- **显式建模多模态分布**：学习 $p(s \mid x)$ 的完整分布结构，而非仅捕捉主模态；
- **可控生成**：在推理时能够根据场景上下文选择合适的模态，生成高保真的全局状态；
- **去中心化执行**：仅依赖局部信息完成推断，不依赖训练时的全局状态访问。

这一重新定义直接指向**条件扩散模型**——扩散过程天然具备建模复杂多模态分布的能力，其逐步去噪机制能够隐式捕获一对多映射的精细结构。GlobeDiff 正是基于这一动机，将扩散模型引入多智能体状态推断，通过潜在变量 $z$ 作为模态选择器，结合变分推断对齐先验与后验分布，为去中心化策略执行提供高保真的全局状态推断。

## 核心创新

GlobeDiff 的核心创新在于将多智能体部分可观测性下的全局状态推断重新定义为一个**多模态条件生成问题**，而非传统的单点回归或确定性映射。这一范式转换直接针对该领域的根本瓶颈：局部观测到全局状态的一对多映射所引发的模态坍塌。

### 问题本质：从判别式坍缩到生成式建模

在部分可观测的多智能体系统中，单个智能体的局部观测 $o_t^i$ 天然对应多个可能的全局状态 $s_t$。传统方法——无论是基于 RNN 的历史编码还是 Transformer 的注意力聚合——本质上学习的是一个从 $x$ 到 $s$ 的确定性映射，输出条件分布的单一最大似然估计。这种判别式范式将多模态分布强行坍缩为点估计，导致信息丢失和次优决策。

GlobeDiff 的因果调控变量是**潜在变量 $z$**，它充当模态选择器：给定局部观测 $x$，不同的 $z$ 对应不同的合理全局状态。通过将状态推断形式化为条件分布 $p_{\theta,\phi}(s \mid x) = \int p_{\theta}(s \mid x, z) p_{\phi}(z \mid x) dz$，模型显式保留了输出空间的多模态结构，从根本上规避了模态坍塌。

### 关键机制：扩散去噪与变分推断的耦合

GlobeDiff 的创新并非简单地将扩散模型套用到 MARL 场景，而在于**扩散过程与变分推断的深度耦合**。具体体现在三个 changed slots 上：

**1. 状态推断方法（判别式 → 生成式扩散）**

基线方法（如 LBS、Dynamic Belief、CommFormer）均依赖循环网络或 Transformer 输出单一状态估计。GlobeDiff 转而使用 U-Net 结构的一维时序卷积扩散模型 $\epsilon_\theta$，条件于辅助观测 $x$、潜在变量 $z$ 和扩散步 $k$，通过 $K$ 步迭代去噪恢复全局状态 $\hat{s}^0$。训练损失函数将扩散噪声预测误差与 KL 正则项联合优化：

$$\mathcal{L}(\theta, \phi, \psi) = \mathbb{E}_{k \sim \mathcal{U}, \epsilon \sim \mathcal{N}(\mathbf{0},\mathbf{I}), (s,x) \sim \mathcal{D}, z \sim q_\psi} \left[ \| \epsilon - \epsilon_\theta \left( \sqrt{\overline{\alpha}^k} s + \sqrt{1-\overline{\alpha}^k} \epsilon, x, z, k \right) \|^2 \right] + \beta_{\mathrm{KL}} \mathbf{KL}(q_\psi(z \mid x, s) \| p_\phi(z \mid x))$$

**2. 一对多映射的处理机制（无显式机制 → 潜在变量模态选择）**

这是 GlobeDiff 最本质的 changed slot。基线方法缺乏对多模态分布的显式建模，仅依赖模型容量隐式记忆。GlobeDiff 通过后验网络 $q_\psi(z \mid x, s)$（训练时访问真实状态）和先验网络 $p_\phi(z \mid x)$（推理时仅依赖局部观测）的对齐，实现模态选择。消融实验证实：移除先验网络和 KL 约束后，性能显著下降，验证了变分推断对模态选择的关键作用。

**3. 通信利用方式（显式协议 → 灵活场景适配）**

与 CommFormer 等需要设计复杂通信图的方法不同，GlobeDiff 根据信息丰度灵活选择辅助观测构建方式：信息丰富时堆叠自身历史观测 $x_t = \{ o_{t-m}^i, \ldots, o_t^i \}$；信息匮乏时拼接联合观测 $x_t = \{ o_t^1, \ldots, o_t^n \}$。这种设计将通信降级为可选的辅助输入，而非必需组件。

### 理论支撑：误差界的双模态分析

GlobeDiff 提供了两个理论结果来刻画生成质量。单模态误差界（Theorem 1）表明，生成状态与真实样本的期望平方误差受限于扩散模型的 Wasserstein 距离和条件方差：

$$\mathbb{E} \left[ \| \hat{s} - s \|^2 \right] \leq 2 W_2^2 (p_{\theta, \phi}(s \mid x), p(s \mid x)) + 4 \operatorname{Var}(s \mid x)$$

多模态误差界（Theorem 2）进一步将误差分解为与最近模态中心的距离，包含扩散步长 $\delta$、KL 误差 $\varepsilon_{KL}$ 和协方差迹的贡献，为扩散步数 $K$ 的选择提供了理论指导。

### 与等容量基线的决定性对比

一个关键的公平性验证来自 Table 1：在 SMAC-v2 (PO) 的 zerg 5v5、protoss 5v5、terran 5v5 等九个任务上，GlobeDiff 的胜率均显著高于参数量匹配的 Vanilla MAPPO (Large)（约 13.5–14M 参数）。这排除了“性能提升仅来自更大模型容量”的替代解释，证明**显式生成式建模本身**——而非参数预算——是性能增益的根本来源。

## 整体框架

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_96g2BRsYZX/figures/001_Figure_1.jpg]]
*Figure 1: The overall framework of GlobeDiff. During the execution phase, we first construct auxiliary local observations x and then infer the global state sˆ using GlobeDiff. Agents make decisions based on the inferred global state sˆ*

GlobeDiff 的整体流程围绕一个核心洞察展开：将多智能体部分可观测性下的全局状态推断重新定义为**多模态条件生成任务**。其 pipeline 由四个关键模块串联构成，形成“观测构建 → 模态选择 → 扩散去噪 → 策略决策”的闭环。

### 辅助观测构建

在进入生成模块之前，系统首先根据场景的信息丰裕度构建辅助观测 $x$。这一设计避免了显式通信协议的复杂性，而是灵活选择输入来源：

- **信息丰富时**：仅使用智能体 $i$ 自身过去 $m$ 步的观测堆叠，即 $x_t = \{ o_{t-m}^i, o_{t-m+1}^i, ..., o_t^i \}$（Eq.1）。
- **信息匮乏时**：通过通信获取所有智能体的联合观测拼接，即 $x_t = \{ o_t^1, o_t^2, ..., o_t^n \}$（Eq.2）。

### 潜在变量作为模态选择器

部分可观测性的核心瓶颈在于：同一局部观测 $x$ 可能对应多种合理的全局状态 $s$（一对多映射）。传统判别式模型（RNN/Transformer）将这种多模态分布坍缩为单点估计，导致模态坍塌。GlobeDiff 的因果调节旋钮是引入**潜在变量 $z$** 作为模态选择器，将状态推断转化为条件生成 $p_{\theta,\phi}(s \mid x) = \int p_{\theta}(s \mid x, z) p_{\phi}(z \mid x) dz$（Eq.3）。

这一设计将问题解耦为两个子任务：
1. **先验网络 $p_\phi(z \mid x)$**：仅从局部观测 $x$ 预测 $z$ 的分布（均值和方差），用于推理时采样模态。
2. **扩散模型 $\epsilon_\theta$**：条件于 $x$、$z$ 和扩散步 $k$，学习从噪声中恢复全局状态。

训练阶段额外引入**后验网络 $q_\psi(z \mid x, s)$**，利用真实全局状态 $s$ 提供的信息来指导 $z$ 的学习，并通过 KL 散度约束 $\mathbf{KL}(q_\psi(z \mid x, s) \| p_\phi(z \mid x))$ 使先验与后验对齐（Eq.4）。消融实验表明，移除先验网络和 KL 约束后性能显著下降，验证了变分推断对模态选择的关键作用（Figure 9）。

### 扩散去噪过程

扩散模型采用一维时序卷积的 U-Net 架构（Figure 12），将二维空间卷积替换为一维时序卷积，使其天然适配序列化的状态数据。训练时，模型联合优化两项损失（Eq.10）：

$$\mathcal{L}(\theta, \phi, \psi) = \mathbb{E}_{k \sim \mathcal{U}, \epsilon \sim \mathcal{N}(\mathbf{0},\mathbf{I}), (s,x) \sim \mathcal{D}, z \sim q_\psi} \left[ \| \epsilon - \epsilon_\theta \left( \sqrt{\overline{\alpha}^k} s + \sqrt{1-\overline{\alpha}^k} \epsilon, x, z, k \right) \|^2 \right] + \beta_{\mathrm{KL}} \mathbf{KL}(q_\psi(z \mid x, s) \| p_\phi(z \mid x))$$

推理时，从高斯噪声出发，通过 $K$ 步迭代去噪恢复全局状态 $\hat{s}^0$（Eq.11）：

$$s^{k-1} = \frac{1}{\sqrt{\alpha^k}} \left( s^k - \frac{\beta^k}{\sqrt{1 - \overline{\alpha}^k}} \epsilon_{\theta}(s^k, x, z, k) \right) + \sqrt{\beta^k} \epsilon$$

扩散步数 $K$ 的消融显示，$K=5$ 相比 $K=3$ 可提升推断准确度，但步数过大收益递减（Figure 10左）。

### 策略学习与训练流程

推断出的全局状态 $\hat{s}$ 被送入标准的 MAPPO 策略网络进行决策。训练遵循 CTDE 范式——训练阶段可访问真实全局状态以加速收敛，但推理阶段完全去中心化，仅依赖局部观测和扩散模型推断。

为缓解离线数据与在线分布的偏差，训练采用两阶段策略：先用离线数据集预训练扩散模型，再在在线执行中持续用收集的数据更新模型。整体算法流程见 Algorithm 1。

### 输入输出流总结

| 阶段 | 输入 | 核心模块 | 输出 |
|------|------|----------|------|
| 观测构建 | 局部观测 $o_t^i$ 或联合观测 $\{o_t^j\}$ | 辅助观测构造（Eq.1/2） | 辅助观测 $x_t$ |
| 模态选择 | $x_t$ | 先验网络 $p_\phi(z \mid x)$ | 潜在变量 $z$ |
| 状态推断 | $x_t$, $z$, 高斯噪声 | 扩散模型 $\epsilon_\theta$（U-Net） | 推断全局状态 $\hat{s}^0$ |
| 策略决策 | $\hat{s}^0$ | MAPPO 策略网络 $\pi_i$ | 动作 $a_t^i$ |

等参数实验（Table 1）提供了决定性证据：与参数量匹配的 Vanilla MAPPO (Large)（约 13.5–14M）相比，GlobeDiff 在所有 9 个测试任务上均取得显著更高的胜率，证明单纯增加模型容量无法替代显式生成模块。可视化结果（Figure 5）进一步显示，GlobeDiff 推断的全局状态与真实状态的 Voronoi 多边形结构高度相似，且随训练推进持续改善。

## 核心模块与公式推导

GlobeDiff 将部分可观测条件下的全局状态推断重新定义为条件生成问题，其核心架构由四个功能模块构成，通过潜在变量 $z$ 和扩散过程显式建模从局部观测到全局状态的一对多映射。

### 辅助观测构建

在推理阶段，智能体首先根据场景构建辅助观测 $x_t$，作为扩散模型的条件输入。该模块提供两种策略：

- **信息丰富场景**：堆叠智能体 $i$ 过去 $m$ 步的自身观测，$x_t = \{ o_{t-m}^i, o_{t-m+1}^i, \cdots, o_t^i \}$，无需通信。
- **信息匮乏场景**：通过通信获取所有智能体的联合观测并拼接，$x_t = \{ o_t^1, o_t^2, \cdots, o_t^n \}$。

这一设计使 GlobeDiff 可根据任务特性灵活选择输入模式，避免依赖复杂的通信协议设计。

### 先验网络 $p_\phi(z \mid x)$

先验网络仅以辅助观测 $x$ 为输入，输出潜在变量 $z$ 的分布参数（均值与方差）。其作用是在推理时（无法访问真实全局状态）为扩散模型提供模态选择信号。训练阶段，先验网络通过 KL 散度约束与后验网络对齐：

$$\text{KL}(q_\psi(z \mid x, s) \parallel p_\phi(z \mid x))$$

消融实验表明，移除先验网络和 KL 约束后，GlobeDiff 在 SMAC-v1 (PO) 上的性能显著下降，验证了变分推断对模态选择的关键作用。

### 扩散模型 $\epsilon_\theta$

扩散模型是状态推断的核心计算单元，采用 U-Net 架构，将二维空间卷积替换为一维时序卷积，以适应状态序列的时序结构。该模型是**全卷积**的，推理的时间范围由输入维度而非模型架构决定。

扩散模型以当前噪声状态 $s^k$、辅助观测 $x$、潜在变量 $z$ 和扩散步 $k$ 为条件，预测添加的噪声 $\epsilon_\theta(s^k, x, z, k)$。训练目标为最小化噪声预测误差与 KL 正则项的联合损失：

$$\mathcal{L}(\theta, \phi, \psi) = \mathbb{E}_{k \sim \mathcal{U}, \epsilon \sim \mathcal{N}(\mathbf{0},\mathbf{I}), (s,x) \sim \mathcal{D}, z \sim q_\psi} \left[ \| \epsilon - \epsilon_\theta \left( \sqrt{\bar{\alpha}^k} s + \sqrt{1-\bar{\alpha}^k} \epsilon, x, z, k \right) \|^2 \right] + \beta_{\mathrm{KL}} \text{KL}(q_\psi(z \mid x, s) \parallel p_\phi(z \mid x))$$

### 去噪采样过程

推理时，从高斯噪声 $s^K \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 出发，通过 $K$ 步迭代去噪恢复全局状态 $\hat{s}^0$。单步更新公式为：

$$s^{k-1} = \frac{1}{\sqrt{\alpha^k}} \left( s^k - \frac{\beta^k}{\sqrt{1 - \bar{\alpha}^k}} \epsilon_{\theta}(s^k, x, z, k) \right) + \sqrt{\beta^k} \epsilon$$

其中 $\alpha^k$、$\beta^k$、$\bar{\alpha}^k$ 为扩散过程的标准噪声调度参数。消融实验显示，增加扩散步数（$K=5$ 对比 $K=3$）可提升状态推断准确度，但步数过大时收益递减；扩散模型的残差块数量对最终性能影响较小，表明模型容量已足够。

### 理论保障

GlobeDiff 提供了两个理论结果来刻画推断误差。在观测函数为单射的假设下，单样本期望误差上界为：

$$\mathbb{E} \left[ \| \hat{s} - s \|^2 \right] \leq 2 W_2^2 (p_{\theta, \phi}(s \mid x), p(s \mid x)) + 4 \text{Var}(s \mid x)$$

该界表明推断误差受扩散模型的分布逼近质量（Wasserstein 距离）和条件方差共同约束。针对多模态分布，进一步给出了生成样本与最近模态中心的期望误差上界：

$$\mathbb{E} \left[ \| \hat{s} - \mu_j(x) \|^2 \right] \leq C_1 K \delta^2 + C_2 \varepsilon_{KL} + 2 \max_i \text{Tr}(\Sigma_i(x)) + \mathcal{O} \left( e^{-D^2 / (8 \sigma_{max}^2)} \right)$$

该界将误差分解为扩散步数 $K$、KL 逼近误差 $\varepsilon_{KL}$、模态内协方差迹以及模态间分离度 $D$ 的函数，为扩散步数和先验网络训练质量提供了理论指导。

## 实验与分析

### 主实验结果

#### 与全局状态推断基线的对比

GlobeDiff 在 SMAC-v1 (PO) 和 SMAC-v2 (PO) 两个基准上与三类全局状态推断方法进行了对比：**LBS**（Hu et al., 2021）基于自回归反事实信念模型近似隐藏信息，**Dynamic Belief**（Zhai et al., 2023）预测其他智能体策略，**CommFormer**（Hu et al., 2024）通过学习动态通信图进行消息传递。所有方法均集成在 MAPPO 的 CTDE 框架下，确保 RL 算法一致。

在 SMAC-v1 (PO) 的 9 个地图中，GlobeDiff 在 7 个地图上取得最优胜率，尤其在 MMM2（0.49 vs 次优 0.27）和 6h_vs_8z（0.47 vs 次优约 0.15）等超难地图上优势显著（Figure 3）。在 SMAC-v2 (PO) 的 9 个地图中，GlobeDiff 在 8 个地图上显著优于所有基线（Figure 4）。这些结果表明，基于扩散模型的生成式状态推断相比判别式信念建模和通信机制，能更有效地处理部分可观测性带来的信息缺失。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_96g2BRsYZX/figures/005_Figure_3.jpg]]
*Figure 3: Comparison results with global state inference baselines in SMAC-v1 (PO) tasks with win rate over three random seeds*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_96g2BRsYZX/figures/011_Figure_4.jpg]]
*Figure 4: Comparison results with global state inference baselines in SMAC-v2 (PO) tasks with win rate over three random seeds*

#### 与生成式基线的对比

为验证扩散模型在生成式状态推断中的优势，GlobeDiff 与两类生成式基线进行了对比：**MAPPO (VAE)** 使用条件 VAE 替代扩散模型，**MAPPO (MLP)** 使用多层感知机直接映射局部观测到状态预测。在 SMAC-v1 (PO) 和 SMAC-v2 (PO) 的超难地图上，GlobeDiff 均显著优于 VAE 和 MLP（Figure 6, Figure 7）。VAE 和 MLP 在多数困难任务上几乎无法学习有效策略，而 GlobeDiff 能稳定获得非零胜率，表明扩散模型的迭代去噪过程比单步前向映射或 VAE 的隐变量建模更能捕获一对多映射的复杂性。

#### 与增大参数量的 MAPPO 对比

为排除性能提升仅来自参数增加的假设，实验对比了等参数预算下的 **Vanilla MAPPO (Large)**——将其网络容量扩大至与 GlobeDiff 总参数量匹配（约 13.5–14M）。Table 1 显示，Vanilla MAPPO (Large) 在 9 个任务中均未取得显著提升，甚至在 MMM2 和 6h_vs_8z 上胜率降至约 0.01，远低于标准 MAPPO。而 GlobeDiff 在所有任务上均明显优于两者。这一结果直接验证了显式生成建模的必要性：单纯增加判别式模型的容量无法解决部分可观测性下的模态坍塌问题。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_96g2BRsYZX/figures/025_Table_1.jpg]]
*Table 1: Comparison results between Vanilla MAPPO, Vanilla MAPPO (Large), and GlobeDiff*

#### 状态推断质量可视化

Figure 5 展示了 GlobeDiff、VAE 和 MLP 推断的全局状态与真实状态的对比。通过 t-SNE 降维和 Voronoi 多边形可视化，GlobeDiff 生成的状态多边形结构与真实状态高度相似，且随着训练进度（颜色从浅绿到紫色）逐步提升。相比之下，VAE 和 MLP 的推断结果与真实状态结构差异明显。这一可视化直接验证了扩散模型在高维状态空间中恢复细粒度空间结构的能力。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_96g2BRsYZX/figures/013_Figure_5.jpg]]
*Figure 5: Visualization of global states generated by GlobeDiff, VAE and MLP. The first plot displays true states and subsequent plots show inferred states per agent. White points denote individual states with polygons highlighting local neighborhoods. Gradient shading (light green to purple) indicates training progression. The similarity between the polygon structures of the inferred and true states reflects the predicted quality*

### 消融实验

#### 先验网络与变分推断的必要性

移除先验网络 $p_\phi(z|x)$ 及对应的 KL 约束后，GlobeDiff 在 SMAC-v1 (PO) 上的性能显著下降（Figure 9）。这一消融验证了变分推断框架对模态选择的关键作用：后验网络 $q_\psi(z|x,s)$ 在训练时提供模态监督信号，先验网络在推理时替代后验进行模态采样，两者通过 KL 散度对齐是保证推理质量的核心机制。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_96g2BRsYZX/figures/018_Figure_9.jpg]]
*Figure 9: Ablation of prior network*

#### 扩散步数与模型容量的影响

在 SMAC-v2 (PO) zerg 5v5 任务上，扩散步数从 3 步增加到 5 步可提升状态推断准确度和最终胜率，但继续增加步数收益递减（Figure 10 左）。扩散模型的残差块数量对最终性能影响较小（Figure 10 右），表明默认的模型容量已足以捕获状态分布。

#### 视野范围的影响

在原始 SMAC 环境中，随着智能体视野范围减小（模拟更强的部分可观测性），GlobeDiff 相对于 MAPPO 的优势更加明显（Figure 8），进一步验证了该方法在信息匮乏场景下的鲁棒性。

### 关键实验结论

1. **一对多映射的显式建模是核心增益来源**：VAE 和 MLP 的失败表明，简单的隐变量模型或确定性映射无法有效处理部分可观测性下的多模态状态分布，扩散模型的迭代去噪过程隐式学习了复杂分布结构。

2. **变分推断框架不可替代**：先验-后验对齐机制为扩散模型提供了有效的模态选择能力，移除后性能急剧下降。

3. **参数增加不等于能力提升**：等参数实验排除了模型容量混淆因素，确认性能增益来自生成式建模本身而非参数量。

### 失败模式与局限

1. **训练依赖全局状态**：GlobeDiff 的训练需要访问真实全局状态（CTDE 范式），在完全去中心化环境中不可得。虽然论文使用离线数据集初始化缓解了冷启动问题，但离线数据与在线分布的偏差可能影响早期训练稳定性。

2. **推理计算开销**：K 步去噪过程增加了推理延迟，在实时决策场景中可能成为瓶颈。消融显示 K=5 是较好的平衡点，但自适应选择 K 的机制尚未探索。

3. **智能体数量扩展性**：当智能体数量增大时，联合观测维度线性增长，扩散模型的输入维度膨胀可能影响效率。论文仅在最多 10–11 个智能体的场景中验证，更大规模场景下的可扩展性未知。

4. **环境泛化性未验证**：所有实验均在修改后的 SMAC 环境（移除敌方类型和生命值信息）上进行，对真实世界部分可观测任务（如自动驾驶、机器人集群）的泛化能力缺乏实证。

### 补充图表

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_96g2BRsYZX/figures/027_Table_2.jpg]]
*Table 2: Hyper-parameters for MAPPO*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_96g2BRsYZX/figures/028_Table_3.jpg]]
*Table 3: Hyper-parameters for prior network $p _ { \phi }$ and posterior network $q _ { \psi }$

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_96g2BRsYZX/figures/029_Table_4.jpg]]
*Table 4: Hyper-parameters for Generative methods*

## 方法谱系与知识库定位

### 问题定位：部分可观测性中的一对多映射

多智能体系统在部分可观测条件下，每个智能体仅能获取局部观测，而决策需要全局状态。传统判别式方法（如基于RNN或Transformer的历史编码器）将局部观测到全局状态的映射建模为确定性函数，输出单一最大似然估计。这一假设在本质上忽略了问题的核心难点：**单个局部观测可能对应多种合理的全局状态配置**（一对多映射）。判别式模型将多模态分布坍缩为点估计，导致模态坍塌和信息丢失——模型只能“记住”训练集中最常见的配置，无法应对推理时的不确定性。

GlobeDiff的出发点是**将状态推断重新定义为条件生成任务**：给定局部观测 $x$，从条件分布 $p(s|x)$ 中采样全局状态，而非预测单一值。这一视角转变使得模型能够显式地捕获一对多映射的复杂性。

### 与现有状态推断方法的对比

**LBS**（Learned Belief Search; Hu et al., 2021）通过自回归反事实信念模型近似隐藏信息，其核心是学习一个信念分布，但本质上仍依赖确定性映射来产生信念表征。**Dynamic Belief**（Zhai et al., 2023）通过预测其他智能体的策略来推断动态信念，将部分可观测性转化为对其他智能体行为的预测问题，但未显式建模全局状态的多模态性。**CommFormer**（Hu et al., 2024）通过学习动态通信图进行消息传递，试图通过显式通信协议弥补信息缺失，但这引入了额外的通信架构设计和带宽约束。

GlobeDiff与上述方法的本质区别在于**不依赖复杂的显式通信协议**，而是通过生成建模直接填补信息缺口。在信息丰富的场景中，GlobeDiff仅使用智能体自身的历史观测堆叠 $x_t = \{o_{t-m}^i, ..., o_t^i\}$ 作为条件输入；在信息匮乏时，通过共享联合观测 $x_t = \{o_t^1, ..., o_t^n\}$ 作为辅助，避免设计复杂的消息聚合机制。这种“按需通信”的设计使其在不同信息条件下具有灵活的适用性。

### 与生成式基线的对比

GlobeDiff在生成式方法谱系中的定位通过对比实验得以明确。**MAPPO (VAE)** 使用条件VAE替代扩散模型作为状态推断模块，**MAPPO (MLP)** 则直接使用多层感知机进行确定性映射。Figure 5的可视化结果揭示了关键差异：MLP生成的状态与真实状态的Voronoi多边形结构几乎无关，VAE能产生一定程度的多样性但保真度不足，而GlobeDiff推断的全局状态与真实状态的多边形结构高度相似，且随着训练进度（从浅绿到紫色渐变）持续改善。

这一差异的根源在于扩散模型的去噪过程隐式地学习分布，而非像VAE那样显式参数化分布形式。VAE的生成质量受限于先验分布的形式（通常为高斯）和近似后验的表达能力，而扩散模型通过多步去噪逐步精化，能够捕获更复杂的多模态结构。Table 1的等参数实验进一步验证了这一优势：在总参数量匹配（约13.5-14M）的条件下，**Vanilla MAPPO (Large)** 在所有9个任务中均未能显著提升性能，说明单纯增加模型容量无法替代显式的生成建模。

### 核心机制：潜在变量与变分推断

GlobeDiff处理一对多映射的关键机制是引入**潜在变量 $z$ 作为模态选择器**。生成分布被形式化为 $p_{\theta,\phi}(s|x) = \int p_\theta(s|x,z) p_\phi(z|x) dz$，其中 $z$ 捕获了给定局部观测下不同全局状态配置的模态信息。训练时，后验网络 $q_\psi(z|x,s)$ 利用真实全局状态 $s$ 的信息来指导 $z$ 的学习；推理时，先验网络 $p_\phi(z|x)$ 仅从局部观测采样 $z$，弥合训练与推理的信息不对称。

这一设计与条件VAE的框架相似，但GlobeDiff将VAE的解码器替换为条件扩散模型 $p_\theta(s|x,z)$，从而获得更强的生成能力。训练目标联合优化扩散噪声预测误差和KL正则项：

$$\mathcal{L}(\theta, \phi, \psi) = \mathbb{E}_{k\sim\mathcal{U}, \epsilon\sim\mathcal{N}(0,I), (s,x)\sim\mathcal{D}, z\sim q_\psi} \left[ \|\epsilon - \epsilon_\theta(\sqrt{\bar{\alpha}^k} s + \sqrt{1-\bar{\alpha}^k} \epsilon, x, z, k)\|^2 \right] + \beta_{KL} \text{KL}(q_\psi(z|x,s) \| p_\phi(z|x))$$

消融实验（Figure 9）表明，移除先验网络和KL约束后性能显著下降，验证了变分推断对模态选择的重要性——没有KL约束，潜在变量 $z$ 将退化为无信息的随机噪声，无法有效区分不同模态。

### 理论保证

GlobeDiff提供了两个误差界来刻画生成质量。**Theorem 1**给出单样本期望误差上界：

$$\mathbb{E}[\|\hat{s} - s\|^2] \leq 2 W_2^2(p_{\theta,\phi}(s|x), p(s|x)) + 4 \text{Var}(s|x)$$

该界表明生成误差由两部分控制：生成分布与真实分布的2-Wasserstein距离（反映扩散模型的拟合质量），以及给定观测下真实状态的条件方差（反映问题本身的不确定性）。**Theorem 2**进一步针对多模态分布，给出了生成状态与最近模态中心的期望误差上界，其中包含扩散步数 $K$、KL误差 $\varepsilon_{KL}$ 和模态间分离度 $D$ 的显式依赖关系，为扩散步数的选择提供了理论指导。

### 适用边界与局限

**训练依赖全局状态**。GlobeDiff遵循CTDE（集中训练、分散执行）范式，训练阶段需要访问真实全局状态来构建后验分布和计算扩散损失。在完全去中心化且无法获取全局信息的场景中，该方法不可直接适用。

**推理计算开销**。$K$ 步去噪采样过程引入了额外的推理延迟。消融实验（Figure 10左）显示，增加扩散步数（$K=5$ vs $K=3$）可提升推断准确度，但步数过大收益递减。在实时性要求高的场景中，需要在推断精度和计算开销之间权衡。目前尚缺乏自适应选择 $K$ 的机制。

**智能体数量可扩展性**。当智能体数量增大时，联合观测的维度呈线性增长，扩散模型的输入维度随之膨胀。虽然GlobeDiff采用了一维时序卷积的U-Net架构（Figure 12），理论上对输入维度具有一定的灵活性，但大规模多智能体场景下的计算效率和推断质量仍需验证。

**环境泛化性**。所有实验均在修改后的SMAC环境（SMAC-v1/v2 (PO)，移除了敌方单位类型和生命值以强化部分可观测性）上进行。在真实世界的部分可观测任务（如自动驾驶、机器人集群）中，状态空间的结构和噪声特性与SMAC显著不同，GlobeDiff的推断质量能否保持尚属未知。

**离线-在线分布偏移**。GlobeDiff采用先离线预训练、再在线更新的策略来缓解分布偏移，但初始离线数据集可能与在线交互分布存在偏差，影响早期训练的稳定性。论文未详细讨论这一偏移的量化分析和缓解策略。

### 开放问题

1. **真实多智能体系统的迁移**：在自动驾驶、无人机编队等真实场景中，GlobeDiff的状态推断质量如何？真实传感器噪声、通信延迟和非平稳动态对扩散模型的去噪过程有何影响？

2. **自适应扩散步数**：能否根据当前的不确定性或任务紧急程度动态调整扩散步数 $K$，在计算预算和推断精度之间实现自适应平衡？

3. **大规模系统的可扩展性**：当智能体数量增至数十或上百时，联合观测维度爆炸如何应对？是否可以通过稀疏注意力或分层聚合来保持扩散模型的效率？

4. **潜在变量的语义可解释性**：Figure 11对潜在变量 $z$ 进行了初步的定性分析，但其语义含义仍不清晰。能否通过解耦表示学习或监督信号注入，使 $z$ 的不同维度对应可解释的全局状态模态（如“进攻阵型”vs“防守阵型”）？

5. **与通信方法的融合**：GlobeDiff目前仅将通信作为辅助输入的拼接，未充分利用通信的结构化信息。能否将扩散模型的去噪过程与图神经网络通信机制结合，在推断全局状态的同时优化通信效率？

## 原文 PDF

![[paperPDFs/ICLR_2026/GlobeDiff_State_Diffusion_Process_for_Partial_Observability_in_Multi_Agent_System.pdf]]
