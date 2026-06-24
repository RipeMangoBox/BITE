---
title: "DiffusionNFT: Online Diffusion Reinforcement with Forward Process"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DiffusionNFT_Online_Diffusion_Reinforcement_with_Forward_Process.pdf
openreview_forum_id: VJZ477R89F
aliases:
- DNAFD
- DiffusionNFT
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "将在线 RL 的训练目标从反向采样过程转移到正向扩散过程，利用流匹配和负样本感知微调隐式定义改进方向，实现无似然、无求解器约束的策略优化。"
primary_logic: "在正向过程中通过对比正样本和负样本的隐式策略来定义改进方向，并使用双支路流匹配损失直接优化单一目标策略，从而将 RL 信号融入监督学习框架，避免对反向采样轨迹的依赖。"
claims:
- "DiffusionNFT 直接在正向扩散过程中进行策略优化，无需在反向过程上使用策略梯度。"
- "该方法允许使用任意黑盒求解器，且仅需干净图像，无需存储采样轨迹。"
- "隐式参数化技术将改进方向 Δ 直接整合到目标策略中，无需显式训练独立引导模型。"
- "DiffusionNFT 在单奖励任务中效率比 FlowGRPO 高 3× 至 25×，且完全不使用 CFG。"
---

# DiffusionNFT: Online Diffusion Reinforcement with Forward Process

> [!tip] 核心洞察
> 在正向过程中通过对比正样本和负样本的隐式策略来定义改进方向，并使用双支路流匹配损失直接优化单一目标策略，从而将 RL 信号融入监督学习框架，避免对反向采样轨迹的依赖。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DiffusionNFT：基于前向过程的在线扩散强化学习 |
| 英文题名 | DiffusionNFT: Online Diffusion Reinforcement with Forward Process |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=VJZ477R89F); [Project](https://research.nvidia.com/labs/dir/DiffusionNFT) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Diffusion Negative-aware FineTuning (DiffusionNFT) |
| Dataset | GenEval, GenEval (head‑to‑head single reward), OCR, PickScore |

> [!tip] 效果简介
> - GenEval 上，GenEval score 为 0.94 (1.7k iterations, multi‑reward)，对比 SD3.5‑M (w/o CFG): 0.24; FLUX.1‑Dev: 0.68; FlowGRPO: 0.95 (5k+ iterations with CFG)，变化 +0.70 (vs. base); matches FlowGRPO in 1/3 iterations。
> - GenEval (head‑to‑head single reward) 上，GenEval score 为 0.98 (1k steps)，对比 FlowGRPO: 0.95 (5k+ steps with CFG)，变化 +0.03, while using 5× fewer steps。
> - OCR 上，OCR score 为 0.91 (multi‑reward)，对比 SD3.5‑M (w/o CFG): 0.12; FLUX.1‑Dev: 0.84; FlowGRPO: 0.92 (2k single‑reward)，变化 +0.79 (vs. base)。

## 概述

基于反向过程的扩散强化学习（RL）方法——如 FlowGRPO——存在结构性缺陷：它们依赖对反向 SDE 的离散化与似然估计，这限制了可用求解器的类型（仅一阶 SDE），并导致正向-反向过程的不一致性；同时，无分类器引导（CFG）的集成要求同时训练条件与无条件模型，使优化变得复杂。这些瓶颈制约了在线扩散 RL 的效率与灵活性。

DiffusionNFT 将在线 RL 的训练目标从反向采样过程转移到正向扩散过程。其核心思路是：在正向过程中，利用奖励信号将生成样本划分为正、负两类，并通过隐式参数化构造两条对比支路——正支路与负支路——来定义改进方向 Δ；随后，使用双支路流匹配损失直接优化单一目标策略，将 RL 信号融入监督学习框架，从而避免对反向采样轨迹的依赖。该方法无似然、无 CFG，且允许使用任意黑盒求解器（包括 ODE 和高阶求解器）进行数据收集，训练与采样完全解耦。

实验表明，DiffusionNFT 在单奖励任务上的效率比 FlowGRPO 高 3× 至 25×（GenEval 得分从 0.24 提升至 0.98，仅需约 1k 步，而 FlowGRPO 需超过 5k 步并配合 CFG 才达到 0.95）。在多奖励训练中，DiffusionNFT 以 CFG‑free 的方式将基模型 SD3.5‑Medium 的 GenEval 得分从 0.24 提升至 0.94，OCR 得分从 0.12 提升至 0.91，并在 PickScore、HPSv2.1、Aesthetic、ImageReward 等指标上全面超越基模型与 FlowGRPO。消融实验确认了负样本感知微调的必要性（移除负支路损失会导致奖励瞬时崩溃），并验证了 ODE 采样器优于 SDE 采样器、自适应时间加权与软更新策略对训练稳定性的关键作用。

## 背景与动机

### 扩散模型与流匹配

扩散模型通过逐步向数据添加噪声并学习反向去噪过程来生成高质量样本。在流匹配框架下，模型被训练为预测速度场 $\boldsymbol{v}_\theta(\boldsymbol{x}_t, t)$，其训练目标为：

$$\mathbb{E}_{t, \boldsymbol{x}_0 \sim \pi_0, \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} [ w(t) \| \boldsymbol{v}_\theta(\boldsymbol{x}_t, t) - \boldsymbol{v} \|_2^2 ]$$

其中目标速度 $\boldsymbol{v} = \dot{\alpha}_t \boldsymbol{x}_0 + \dot{\sigma}_t \boldsymbol{\epsilon}$，正向加噪过程具有闭合形式 $\boldsymbol{x}_t = \alpha_t \boldsymbol{x}_0 + \sigma_t \boldsymbol{\epsilon}$。反向采样可通过求解 ODE $\frac{\mathrm{d}\boldsymbol{x}_t}{\mathrm{d}t} = \boldsymbol{v}_\theta(\boldsymbol{x}_t, t)$ 实现，这为后续的强化学习优化提供了基础。

### 现有在线扩散 RL 方法的瓶颈

以 FlowGRPO 为代表的基于反向过程的在线扩散 RL 方法，通过在反向 SDE 采样轨迹上计算策略梯度来优化扩散模型。然而，这类方法存在三个根本性缺陷：

1. **求解器受限**：策略梯度计算依赖于一阶 SDE 采样器，无法使用 ODE 或高阶求解器。这既限制了采样效率，也使得训练与采样过程深度耦合。

2. **正向-反向不一致性**：训练目标定义在反向采样轨迹上，但实际生成过程的正向扩散分布与反向采样分布之间存在固有偏差，导致优化信号与真实生成行为脱节。

3. **CFG 集成复杂**：无分类器引导（CFG）需要同时训练条件模型和无条件模型，实现在线 RL 时需维护双模型架构，增加了训练复杂性和计算开销。

此外，这类方法需要存储完整的采样轨迹（包含中间时间步）用于策略梯度计算，进一步加重了内存和计算负担。

### 本文动机

上述瓶颈的核心在于：**将在线 RL 的训练目标绑定在反向采样过程上**。本文提出一个根本性的视角转换——将策略优化从反向过程转移到正向扩散过程。通过在正向过程中利用流匹配目标直接优化速度预测器，可以天然规避对反向采样轨迹的依赖，实现无似然、无求解器约束的策略优化。

具体而言，DiffusionNFT 的核心思路是：在正向过程中通过对比正样本（高奖励）和负样本（低奖励）的隐式策略来定义改进方向 $\Delta$，并使用双支路流匹配损失直接优化单一目标策略，从而将 RL 信号融入监督学习框架。这一设计使得方法允许使用任意黑盒求解器进行数据收集，仅需干净图像与对应的奖励信号，无需存储采样轨迹，且全程 CFG-free。

## 核心创新

### 1. 训练范式转移：从反向过程策略梯度到正向过程流匹配

现有基于扩散模型的在线 RL 方法（以 FlowGRPO 为代表）的核心瓶颈在于**依赖反向采样过程进行策略优化**。这类方法需要在离散化的反向 SDE 上估计似然并计算策略梯度，由此引入三个结构性缺陷：

- **求解器受限**：数据采样必须使用一阶 SDE 采样器，无法利用 ODE 或高阶求解器，限制了生成质量和采样效率。
- **正向-反向不一致性**：训练目标基于反向轨迹，而实际生成过程涉及正向扩散，两者之间的分布偏移未得到显式处理。
- **CFG 集成复杂**：后训练中需同时维护条件模型和无条件模型，实现双模型优化，增加了训练开销和调参难度。

DiffusionNFT 的**核心范式转移**在于将在线 RL 的训练目标从反向采样过程转移到**正向扩散过程**。具体而言，方法直接在正向流匹配目标上进行策略优化，无需在反向过程上使用策略梯度。这一转变的因果机制如下：

1. **无似然优化**：正向流匹配损失天然不依赖似然估计，避免了反向过程 RL 中因离散化 SDE 和近似似然引入的偏差。
2. **求解器完全解耦**：数据收集阶段允许使用任意黑盒求解器（包括 ODE 和高阶求解器），训练与采样完全解耦，无需存储完整采样轨迹，仅需干净图像与对应的奖励信号。
3. **CFG-free 设计**：全程不使用无分类器引导，避免了条件/无条件双模型训练的复杂性和潜在偏见。

> **证据强度**：该范式转移是方法的核心主张，在 Section 1 和 Figure 2 中有明确的概念对比和说明，置信度 0.95。

### 2. 隐式策略优化：对比正负样本的单一模型更新

DiffusionNFT 的第二个关键创新在于**隐式参数化技术**，它使得强化引导信号可以直接整合到单一目标策略模型中，而无需显式训练独立的引导模型。

**改进方向的定义。** 方法首先根据奖励信号将生成样本划分为"正样本"和"负样本"，并分别定义两个隐式策略：

- **隐式正策略**：$\boldsymbol{v}_\theta^+(\boldsymbol{x}_t, \boldsymbol{c}, t) := (1 - \beta) \boldsymbol{v}^{\mathrm{old}}(\boldsymbol{x}_t, \boldsymbol{c}, t) + \beta \boldsymbol{v}_\theta(\boldsymbol{x}_t, \boldsymbol{c}, t)$
- **隐式负策略**：$\boldsymbol{v}_\theta^-(\boldsymbol{x}_t, \boldsymbol{c}, t) := (1 + \beta) \boldsymbol{v}^{\mathrm{old}} - \beta \boldsymbol{v}_\theta$

正策略是旧策略与当前策略的凸组合，负策略则是反向插值。两者之间的速度差定义了一个**改进方向 Δ**：

$$\Delta := [1-\alpha(\boldsymbol{x}_t)] [\boldsymbol{v}^{\mathrm{old}} - \boldsymbol{v}^-] = \alpha(\boldsymbol{x}_t) [\boldsymbol{v}^+ - \boldsymbol{v}^{\mathrm{old}}]$$

该方向表示从旧策略向更优分布移动的矢量，其几何意义在 Figure 3 中示意。

**双支路流匹配损失。** 基于上述隐式策略，DiffusionNFT 构造了一个统一的双支路训练目标：

$$\mathcal{L}(\theta) = \mathbb{E}_{c, \pi^{\mathrm{old}}(\boldsymbol{x}_0 \mid c), t} \; r \| \boldsymbol{v}_\theta^+(\boldsymbol{x}_t, \boldsymbol{c}, t) - \boldsymbol{v} \|_2^2 + (1 - r) \| \boldsymbol{v}_\theta^-(\boldsymbol{x}_t, \boldsymbol{c}, t) - \boldsymbol{v} \|_2^2$$

其中 $r \in [0,1]$ 是由原始奖励映射得到的最优性概率，用于正/负样本的软划分。该损失同时优化正负两个分支，但**仅更新单一速度预测器 $\boldsymbol{v}_\theta$**（正负策略均通过 $\boldsymbol{v}_\theta$ 与 $\boldsymbol{v}^{\mathrm{old}}$ 的插值隐式构造）。在无限数据和容量下，最优解收敛到：

$$\boldsymbol{v}_{\theta^*}(\boldsymbol{x}_t, \boldsymbol{c}, t) = \boldsymbol{v}^{\mathrm{old}} + \frac{2}{\beta} \Delta$$

这表明优化目标能够将 RL 信号融入监督学习框架，实现对策略的隐式改进。

> **证据强度**：隐式参数化的理论推导在 Theorem 3.1 和 Theorem 3.2 中给出，消融实验（Section 4.4）证实移除负分支损失会导致奖励瞬时崩溃，置信度 0.95。

### 3. 与 Baseline 的关键差异对比

下表总结了 DiffusionNFT 相对于 FlowGRPO 等反向过程 RL 方法的核心 changed slots：

| 维度 | 反向过程 RL（FlowGRPO） | DiffusionNFT（正向过程 RL） |
|------|------------------------|---------------------------|
| **训练范式** | 反向过程的策略梯度，需离散化反向 SDE 并估计似然 | 正向过程的流匹配目标与负样本感知微调，直接优化速度预测器 |
| **CFG 集成** | 需同时训练条件/无条件模型，实现双模型优化 | 隐式引导集成：单模型上直接融合强化引导，全程 CFG-free |
| **求解器灵活性** | 依赖一阶 SDE 采样器，无法使用 ODE 或高阶求解器 | 允许任意黑盒求解器（ODE、高阶），训练与采样完全解耦 |
| **训练数据需求** | 需存储完整采样轨迹（含中间时间步） | 仅需干净图像与对应奖励信号 |

这些差异直接转化为实际效率提升：在单奖励任务的 GenEval 头对头对比中，DiffusionNFT 以 1k 步达到 0.98 分，而 FlowGRPO 需 5k+ 步且额外使用 CFG 才达到 0.95 分，效率提升达 3× 至 25×（Figure 1(a), Figure 6）。

### 4. 辅助创新：稳定训练的技术组件

除上述核心创新外，DiffusionNFT 还引入了几项对训练稳定性至关重要的技术组件：

- **自适应时间加权**：将标准流匹配损失中的 $w(t)$ 替换为自归一化 $x_0$ 回归损失 $\frac{\|x_\theta - x_0\|_2^2}{\mathrm{sg}(\mathrm{mean}(\mathrm{abs}(x_\theta - x_0)))}$，在较大时间步 $t$ 给予更高权重，提升训练稳定性（Section 4.4 消融证实）。
- **EMA 软更新**：$\theta^{\mathrm{old}} \leftarrow \eta_i \theta^{\mathrm{old}} + (1 - \eta_i) \theta$，解耦采样策略与训练策略。从小 $\eta$ 开始并逐渐增大至最大值的调度策略在收敛速度和稳定性之间取得最佳平衡。
- **最优性概率映射**：$r(\boldsymbol{x}_0, \boldsymbol{c}) := \frac{1}{2} + \frac{1}{2} \mathrm{clip}\left[ \frac{r^{\mathrm{raw}} - \mathbb{E}[r^{\mathrm{raw}}]}{Z_c}, -1, 1 \right]$，将原始奖励归一化并映射到 $[0,1]$，实现正负样本软划分，避免硬阈值带来的信息损失。

> **证据强度**：上述组件的消融实验在 Section 4.4 中系统验证，置信度 0.9。

## 整体框架

![[assets/figures/papers/iclr26_0012_VJZ477R89F_DiffusionNFT_Online_Diffusion_Reinforcement_with/figures/003_Figure_2.jpg]]
*Figure 2: Comparison between Forward-Process RL (NFT) and Reverse-Process RL (GRPO). NFT allows using any solvers and does not require storing the whole sampling trajectory for optimization*

![[assets/figures/papers/iclr26_0012_VJZ477R89F_DiffusionNFT_Online_Diffusion_Reinforcement_with/figures/005_Figure_4.jpg]]
*Figure 4: DiffusionNFT jointly optimizes two dual diffusion objectives, on both positive ( r = 1 ) and negative ( r = 0 ) branches. Rather than training two independent models ${ \boldsymbol { v } } _ { \theta } ^ { + }$ and ${ \boldsymbol$ v $} _ { \boldsymbol { \theta } _ { } } ^ { - }$ , it adopts an implicit parameterization technique that directly optimizes a single target policy ${ \pmb$ v $} _ { \theta }$

DiffusionNFT 的整体设计围绕一个核心洞察展开：**将在线强化学习的训练目标从反向采样过程转移到正向扩散过程**。这一转移使得方法能够完全规避传统扩散 RL 对似然估计和特定求解器的依赖，同时通过对比正负样本的隐式策略来定义改进方向。整个 pipeline 由五个紧密耦合的模块构成，形成“采样—评估—优化—更新”的闭环。

### 数据收集（Rollout）

在每轮在线训练开始时，系统使用**任意黑盒求解器**从当前采样策略 $\\pi^{\\mathrm{old}}$ 生成 $K$ 张干净图像 $\\{\\boldsymbol{x}_0^{(i)}\\}_{i=1}^K$。与 FlowGRPO 等依赖一阶 SDE 采样器的方法不同，DiffusionNFT 的求解器选择完全灵活——可使用 ODE 求解器、高阶求解器或任何黑盒采样器，训练与采样过程完全解耦。消融实验（Figure 7）表明，ODE 采样器在数据收集上优于 SDE 采样器，尤其在 PickScore 指标上提升明显。

这一设计带来的另一个关键优势是：**仅需存储最终的干净图像**，无需保留完整的采样轨迹（包含中间时间步 $\\boldsymbol{x}_t$），大幅降低了存储开销和工程复杂度。

### 最优性概率分配

收集到的图像通过外部奖励模型获得原始奖励 $r^{\\mathrm{raw}}(\\boldsymbol{x}_0, \\boldsymbol{c})$。为将奖励信号转化为可微调的软标签，DiffusionNFT 将原始奖励归一化并映射为 $[0,1]$ 范围内的**最优性概率** $r(\\boldsymbol{x}_0, \\boldsymbol{c})$：

$$r(\\boldsymbol{x}_0, \\boldsymbol{c}) := \\frac{1}{2} + \\frac{1}{2} \\mathrm{clip}\\left[ \\frac{r^{\\mathrm{raw}}(\\boldsymbol{x}_0, \\boldsymbol{c}) - \\mathbb{E}[r^{\\mathrm{raw}}]}{Z_c}, -1, 1 \\right]$$

这一设计实现了正/负样本的**软划分**：$r$ 接近 1 表示正样本（高奖励），$r$ 接近 0 表示负样本（低奖励），而非硬阈值二分类。这为后续的双支路损失提供了平滑的权重信号。

### 正向流匹配损失（正/负双支路）

这是 DiffusionNFT 的核心优化模块。对每条数据，系统同时计算两条支路的速度预测损失，隐式定义改进方向：

$$\\mathcal{L}(\\theta) = \\mathbb{E}_{c, \\pi^{\\mathrm{old}}(\\boldsymbol{x}_0 \\mid c), t}\\ r \\| \\boldsymbol{v}_\\theta^+(\\boldsymbol{x}_t, \\boldsymbol{c}, t) - \\boldsymbol{v} \\|_2^2 + (1 - r) \\| \\boldsymbol{v}_\\theta^-(\\boldsymbol{x}_t, \\boldsymbol{c}, t) - \\boldsymbol{v} \\|_2^2$$

其中，正/负支路的速度目标通过**隐式参数化**构造，无需训练独立的引导模型：

$$\\boldsymbol{v}_\\theta^+(\\boldsymbol{x}_t, \\boldsymbol{c}, t) := (1 - \\beta) \\boldsymbol{v}^{\\mathrm{old}} + \\beta \\boldsymbol{v}_\\theta$$
$$\\boldsymbol{v}_\\theta^-(\\boldsymbol{x}_t, \\boldsymbol{c}, t) := (1 + \\beta) \\boldsymbol{v}^{\\mathrm{old}} - \\beta \\boldsymbol{v}_\\theta$$

正支路将旧策略速度 $\\boldsymbol{v}^{\\mathrm{old}}$ 向当前模型 $\\boldsymbol{v}_\\theta$ 插值，负支路则反向插值，两者间的速度差 $\Delta$ 即为改进方向（Theorem 3.1）。在无限数据和容量假设下，该目标的最优解收敛于 $\\boldsymbol{v}_{\\theta^*} = \\boldsymbol{v}^{\\mathrm{old}} + \\frac{2}{\\beta} \\Delta$（Theorem 3.2），实现了对单一目标策略的直接优化。

消融实验证实，**移除负分支损失会导致奖励瞬时崩溃**，证明负样本感知微调对训练稳定性至关重要。

### 隐式参数化策略更新

上述双支路设计的关键在于隐式参数化技术：通过 $\beta$ 插值构造隐式正/负策略，将强化引导信号直接整合到单一速度预测器 $\\boldsymbol{v}_\\theta$ 中。这意味着 DiffusionNFT 全程 **CFG-free**——无需同时训练条件模型和无条件模型，避免了传统 CFG 带来的双模型优化复杂性和潜在偏见。引导强度 $\beta$ 在 1 附近表现稳定，实验中选用 $\beta=1$ 或 $0.1$。

### EMA 软更新与自适应时间加权

在线 RL 中，采样策略与训练策略的同步是关键挑战。DiffusionNFT 使用**指数移动平均（EMA）** 将两者解耦：

$$\\theta^{\\mathrm{old}} \\leftarrow \\eta_i \\theta^{\\mathrm{old}} + (1 - \\eta_i) \\theta$$

消融实验（Figure 8）表明，从小 $\eta$ 开始并逐渐增加至最大值的软更新策略在收敛速度和稳定性之间取得最佳平衡。

此外，为改善训练稳定性，DiffusionNFT 采用**自适应时间加权**替换原始的 $w(t)$ 加权：

$$w(t) \\|\\boldsymbol{v}_\\theta - \\boldsymbol{v}\\|_2^2 \\to \\frac{\\|\\boldsymbol{x}_\\theta - \\boldsymbol{x}_0\\|_2^2}{\\mathrm{sg}(\\mathrm{mean}(\\mathrm{abs}(\\boldsymbol{x}_\\theta - \\boldsymbol{x}_0)))}$$

该设计在较大时间步 $t$ 给予更高权重，进一步提升了训练稳定性（Figure 9）。

### 整体数据流

整个 pipeline 的数据流可概括为：**当前策略 → 黑盒采样 → 干净图像 → 奖励评估 → 最优性概率 → 双支路流匹配损失 → 隐式策略更新 → EMA 软更新采样策略**。这一闭环将 RL 信号无缝融入监督学习框架，避免了反向过程策略梯度对采样轨迹和特定求解器的依赖，实现了无似然、无求解器约束的高效在线扩散强化学习。

## 核心模块与公式推导

### 瓶颈与设计动机

现有基于反向过程的扩散 RL 方法（如 FlowGRPO）存在三个固有缺陷：**求解器受限**（必须使用一阶 SDE 采样器，无法使用 ODE 或高阶求解器）、**正向-反向不一致性**（训练依赖反向采样轨迹，与正向扩散过程存在分布偏差）、**CFG 集成复杂**（需要同时训练条件模型和无条件模型，实现双模型优化）。这些缺陷制约了在线 RL 在扩散模型中的效率与灵活性。

DiffusionNFT 的核心思路是将在线 RL 的训练目标从反向采样过程**转移到正向扩散过程**，利用流匹配（flow matching）目标直接优化速度预测器 $v_\theta$，实现**无似然（likelihood-free）、无求解器约束**的策略优化。

### 正向流匹配基础

扩散模型的速度参数化训练目标为：

$$
\mathbb{E}_{t, \boldsymbol{x}_0 \sim \pi_0, \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left[ w(t) \| \boldsymbol{v}_\theta(\boldsymbol{x}_t, t) - \boldsymbol{v} \|_2^2 \right]
$$

其中目标速度 $\boldsymbol{v} = \dot{\alpha}_t \boldsymbol{x}_0 + \dot{\sigma}_t \boldsymbol{\epsilon}$，正向加噪过程通过重参数化 $\boldsymbol{x}_t = \alpha_t \boldsymbol{x}_0 + \sigma_t \boldsymbol{\epsilon}$ 实现。该框架允许在任意时间步采样噪声状态，为后续的在线 RL 优化提供基础。

### 改进方向 Δ 的定义

DiffusionNFT 的核心洞察在于：**通过对比正样本和负样本的隐式策略来定义改进方向**。给定旧策略 $v^{\text{old}}$，将数据分布按奖励信号拆分为正分布 $\pi^+$ 和负分布 $\pi^-$，则改进方向 $\Delta$ 定义为：

$$
\Delta := [1-\alpha(\boldsymbol{x}_t)] [\boldsymbol{v}^{\text{old}} - \boldsymbol{v}^-] = \alpha(\boldsymbol{x}_t) [\boldsymbol{v}^+ - \boldsymbol{v}^{\text{old}}]
$$

其中 $\alpha(\boldsymbol{x}_t)$ 是后验拆分系数，$\boldsymbol{v}^+$ 和 $\boldsymbol{v}^-$ 分别为正、负分布下的最优速度预测器。该方向表示从旧策略向正策略移动的矢量，是后续优化的理论依据。

### 隐式参数化与双支路损失

为避免显式训练独立的引导模型，DiffusionNFT 采用**隐式参数化技术**，将改进方向直接整合到单一目标策略中：

$$
\boldsymbol{v}_\theta^+(\boldsymbol{x}_t, \boldsymbol{c}, t) := (1 - \beta) \boldsymbol{v}^{\text{old}}(\boldsymbol{x}_t, \boldsymbol{c}, t) + \beta \boldsymbol{v}_\theta(\boldsymbol{x}_t, \boldsymbol{c}, t)
$$

$$
\boldsymbol{v}_\theta^-(\boldsymbol{x}_t, \boldsymbol{c}, t) := (1 + \beta) \boldsymbol{v}^{\text{old}} - \beta \boldsymbol{v}_\theta
$$

其中 $\beta$ 为引导强度（实验中 $\beta=1$ 或 $0.1$ 表现稳定）。正策略由旧策略与当前策略的凸组合得到，负策略由反向插值得到，二者提供对比信号。

基于此，DiffusionNFT 的优化目标为**双支路流匹配损失**：

$$
\mathcal{L}(\theta) = \mathbb{E}_{c, \pi^{\text{old}}(\boldsymbol{x}_0 \mid c), t} \; r \| \boldsymbol{v}_\theta^+(\boldsymbol{x}_t, \boldsymbol{c}, t) - \boldsymbol{v} \|_2^2 + (1 - r) \| \boldsymbol{v}_\theta^-(\boldsymbol{x}_t, \boldsymbol{c}, t) - \boldsymbol{v} \|_2^2
$$

其中 $r \in [0,1]$ 为最优性概率（见下文）。该损失同时训练正、负两个分支，隐式地将 RL 信号融入监督学习框架。在无限数据和容量下，最优解收敛为：

$$
\boldsymbol{v}_{\theta^*}(\boldsymbol{x}_t, \boldsymbol{c}, t) = \boldsymbol{v}^{\text{old}} + \frac{2}{\beta} \Delta
$$

即旧策略加上两倍缩放的改进方向。

### 最优性概率与软划分

原始奖励需要转换为 $[0,1]$ 范围内的最优性概率 $r$，实现正/负样本的**软划分**：

$$
r(\boldsymbol{x}_0, \boldsymbol{c}) := \frac{1}{2} + \frac{1}{2} \mathrm{clip}\left[ \frac{r^{\text{raw}}(\boldsymbol{x}_0, \boldsymbol{c}) - \mathbb{E}[r^{\text{raw}}]}{Z_c}, -1, 1 \right]
$$

该映射将高于均值的样本推向 $r \to 1$（正样本），低于均值的推向 $r \to 0$（负样本），避免硬阈值划分带来的信息损失。

### 训练稳定性机制

**EMA 软更新**：采样策略 $\theta^{\text{old}}$ 通过指数移动平均与训练策略 $\theta$ 解耦：

$$
\theta^{\text{old}} \leftarrow \eta_i \theta^{\text{old}} + (1 - \eta_i) \theta
$$

从小 $\eta$ 开始并逐渐增大至最大值，在收敛速度和稳定性之间取得平衡。

**自适应时间加权**：将原始加权 $w(t) \|\boldsymbol{v}_\theta - \boldsymbol{v}\|_2^2$ 替换为自归一化的 $x_0$ 回归损失：

$$
\frac{\|\boldsymbol{x}_\theta(\boldsymbol{x}_t, \boldsymbol{c}, t) - \boldsymbol{x}_0\|_2^2}{\mathrm{sg}(\mathrm{mean}(\mathrm{abs}(\boldsymbol{x}_\theta - \boldsymbol{x}_0)))}
$$

该设计在较大 $t$ 时给予更高权重，改善训练稳定性。

### 关键消融证据

- **负分支损失不可移除**：移除 $\boldsymbol{v}_\theta^-$ 的损失会导致奖励**瞬时崩溃**，证明负样本感知微调对在线 RL 至关重要。
- **引导强度 $\beta$**：在 $1$ 附近表现稳定，实验中选用 $\beta=1$ 或 $0.1$。
- **ODE 求解器优势**：数据收集使用 ODE 采样器优于 SDE 采样器，尤其在 PickScore 上提升明显。

## 实验与分析

### 主要定量结果

DiffusionNFT 在多个规则型与模型型奖励指标上均展现出显著提升，且全程无需 CFG。Table 1 汇总了以 SD3.5-Medium（w/o CFG）为基模型、经过 1.7k 次迭代多奖励训练后的评估结果：

![[assets/figures/papers/iclr26_0012_VJZ477R89F_DiffusionNFT_Online_Diffusion_Reinforcement_with/figures/006_Table_1.jpg]]
*Table 1: Evaluation Results. Gray-colored: In-domain reward. † Evaluated on official checkpoints. ‡Evaluated under 1024×1024 resolution. Bold: best; Underline: second best*

- **GenEval**：从基模型的 0.24 提升至 **0.94**，接近 FlowGRPO（0.95，需 5k+ 迭代与 CFG），但仅用约 1/3 的训练步数。
- **OCR**：从 0.12 提升至 **0.91**，逼近 FlowGRPO（0.92，单奖励训练）。
- **PickScore**：达到 **23.80**，显著高于基模型（20.51）和 CFG 增强版（22.34），也优于 FlowGRPO（21.91）。
- **HPSv2.1**：达到 **0.331**，较基模型（0.204）提升 62%，超越 CFG 增强版（0.279）和 FlowGRPO（0.256）。
- **Aesthetic**：从 5.13 提升至 **6.01**。
- **ImageReward**：从 -0.58 提升至 **1.49**。

在单奖励头对头对比中（Figure 1(a)、Figure 6），DiffusionNFT 在 GenEval 上达到 **0.98**（约 1k 步），而 FlowGRPO 在 5k+ 步且启用 CFG 后仅为 0.95。整体效率优势达到 **3× 至 25×**（wall-clock time）。

![[assets/figures/papers/iclr26_0012_VJZ477R89F_DiffusionNFT_Online_Diffusion_Reinforcement_with/figures/002_Figure_1.jpg]]
*Figure 1: Performance of DiffusionNFT. (a) Head-to-head comparison with FlowGRPO on the GenEval task. (b) By employing multiple reward models, DiffusionNFT significantly boosts the performance of SD3.5-Medium in every benchmark tested, while being fully CFG-free*

![[assets/figures/papers/iclr26_0012_VJZ477R89F_DiffusionNFT_Online_Diffusion_Reinforcement_with/figures/024_Figure_6.jpg]]
*Figure 6: Head-to-head comparison between DiffusionNFT with FlowGRPO on single rewards*

**Table 2** 揭示了单奖励训练的泛化局限：仅在 OCR 奖励上训练时，DiffusionNFT 的 OCR 得分可达 0.92，但其他指标（如 GenEval、PickScore）出现退化，需额外启用 CFG 进行评估。这表明单一奖励信号的过拟合风险仍然存在，多奖励联合训练是维持泛化能力的关键。

![[assets/figures/papers/iclr26_0012_VJZ477R89F_DiffusionNFT_Online_Diffusion_Reinforcement_with/figures/031_Table_2.jpg]]
*Table 2: Evaluation results of FlowGRPO and DiffusionNFT trained on single rewards, both initialized from CFG-free base model. Gray-colored: In-domain reward. We observe that training exclusively on the OCR reward impairs generalization to other metrics; to compensate this, we enable CFG when evaluating non-OCR rewards for OCR-trained models. We provide more qualitative comparison between the base model, FlowGRPO and our multi-reward optimized model in Figure 11, Figure 12 and Figure 13*

### 消融实验

消融实验系统验证了 DiffusionNFT 各设计组件的必要性：

- **负样本感知微调（Negative-aware FineTuning）**：移除负分支损失 $v_\theta^-$ 后，奖励在在线训练中几乎瞬间崩溃。这直接证明了仅靠正样本微调（即 RFT 范式）无法维持策略改进的稳定性，负样本提供的对比信号是方法的核心驱动力。
- **求解器选择**：Figure 7 显示，在数据收集阶段使用 ODE 采样器优于 SDE 采样器，尤其在 PickScore 上提升明显。这验证了方法对任意黑盒求解器的兼容性，并表明 ODE 采样器在在线 RL 场景下可能提供更稳定的 rollout 质量。
- **自适应时间加权**：将标准流匹配损失替换为自归一化 $x_0$ 回归损失（在较大 $t$ 给予更高权重）后，训练稳定性显著改善。这表明在正向过程早期（高噪声阶段）施加更强的优化信号有助于策略收敛。
- **EMA 软更新策略**：从小 $\eta$ 开始并逐渐增大至最大值的调度策略，在收敛速度与训练稳定性之间取得最佳平衡（Figure 8）。
- **引导强度 $\beta$**：$\beta$ 在 1 附近表现稳定，实验中选用 $\beta=1$ 或 $0.1$ 均可获得良好效果，表明方法对引导强度不敏感。

### 定性结果

Figure 5 展示了 SD3.5-M、FlowGRPO 与 DiffusionNFT 在 GenEval、OCR、DrawBench 上的生成样例对比。DiffusionNFT 在文本渲染准确性（OCR）、物体计数与空间关系（GenEval）以及复杂场景构图（DrawBench）上均表现出明显改善，且未使用 CFG 即可达到与 FlowGRPO 相当的视觉质量。更多定性对比见 Figure 11–13。

### 失败模式与局限性

1. **奖励模型依赖**：整个在线 RL 过程依赖于外部奖励模型的质量。若奖励模型存在偏差（如对特定风格或内容的偏好），最终策略将继承这些偏差。论文未对不同人群或属性上的公平性进行评估。
2. **单奖励过拟合**：如 Table 2 所示，仅在 OCR 奖励上训练会导致其他指标泛化能力下降，需额外启用 CFG 补偿。这表明单目标优化存在“奖励黑客”风险。
3. **多阶段训练调度**：多奖励训练需要分阶段调度不同奖励模型，自动化程度仍有提升空间，可能增加实际部署的工程复杂度。

## 方法谱系与知识库定位

### 与基线方法的本质差异

DiffusionNFT 的核心创新在于将在线强化学习的优化目标从**反向采样过程**转移到**正向扩散过程**，这与以 FlowGRPO 为代表的反向过程 RL 方法形成了根本性的范式差异。

**瓶颈根源：反向过程 RL 的固有缺陷。** FlowGRPO 等方法在反向 SDE 上应用策略梯度（如 GRPO），需要离散化反向 SDE 并估计似然。这一范式带来了三个连锁限制：（1）**求解器受限**——数据采样必须依赖一阶 SDE 采样器，无法使用 ODE 或高阶求解器；（2）**正向-反向不一致性**——训练阶段的正向加噪与采样阶段的反向去噪之间存在分布错配；（3）**CFG 集成复杂**——需要同时训练条件模型和无条件模型，实现双模型优化。这些限制构成了扩散 RL 领域的真实瓶颈。

**因果旋钮：从反向到正向的范式转移。** DiffusionNFT 将训练目标重新锚定在正向扩散过程上，利用流匹配（flow matching）目标直接优化速度预测器 $v_\theta$。具体而言，该方法通过以下机制实现了无似然、无求解器约束的策略优化：

| 设计维度 | 反向过程 RL（FlowGRPO） | 正向过程 RL（DiffusionNFT） |
|---------|----------------------|--------------------------|
| 训练范式 | 反向 SDE 上的策略梯度 | 正向过程的流匹配目标 + 负样本感知微调 |
| 求解器灵活性 | 仅支持一阶 SDE 采样器 | 任意黑盒求解器（ODE/高阶） |
| 训练数据需求 | 需存储完整采样轨迹 | 仅需干净图像与奖励信号 |
| CFG 集成 | 双模型（条件/无条件）训练 | 隐式引导集成，全程 CFG-free |

**证据强度：** 上述差异在论文中得到了明确锚定（Section 1），置信度达 0.95。DiffusionNFT 允许使用任意黑盒求解器进行数据收集，且无需存储整个采样轨迹，仅需干净图像即可进行策略优化——这是其相对于 FlowGRPO 效率提升 3× 至 25× 的结构性原因（Figure 1）。

### 与 Rejection FineTuning (RFT) 的关系

RFT 是一种仅利用正样本进行微调的基线方法，可视为 DiffusionNFT 的退化版本。DiffusionNFT 通过引入**负样本感知微调**（negative-aware fine-tuning），在 RFT 的基础上增加了对比信号：利用奖励信号将生成样本划分为正样本和负样本，并通过双支路流匹配损失同时优化正策略和负策略。消融实验表明，移除负分支损失 $v_\theta^-$ 会导致奖励在在线训练中几乎瞬时崩溃（Section 4.4），这证明负样本感知机制是该方法有效性的必要条件。

### 适用边界与限制

**1. 奖励模型依赖。** DiffusionNFT 的在线 RL 过程依赖于外部奖励模型的质量。最优性概率 $r(x_0, c)$ 将原始奖励归一化并映射到 $[0,1]$ 区间，用于正/负样本的软划分。奖励模型的偏差会直接影响策略的改进方向 $\Delta$，进而影响最终生成质量。论文未对不同奖励模型质量下的鲁棒性进行系统性评估。

**2. 单奖励训练的泛化衰退。** 在 OCR 等任务上单独训练时，DiffusionNFT 会导致其他指标的泛化能力下降，需额外启用 CFG 进行评估（Table 2）。这表明单一奖励信号可能诱导策略过度专业化，在多目标权衡上存在不足。

**3. 多奖励训练的调度复杂性。** 多奖励训练需要分阶段调度不同的奖励模型，自动化程度仍有提升空间。论文未提供自适应的多奖励融合策略。

**4. 隐式参数化的适用范围。** 隐式参数化技术通过 $\beta$ 插值构造正/负策略（$v_\theta^+ := (1-\beta)v^{old} + \beta v_\theta$, $v_\theta^- := (1+\beta)v^{old} - \beta v_\theta$），直接优化单一目标速度模型。这一技术目前仅在流匹配框架下得到验证，其在其他类型扩散模型（如 DDPM、EDM 等非流匹配模型）上的适用性有待验证。

### 开放问题

**1. Off-policy 训练的分布漂移。** DiffusionNFT 使用 EMA 软更新（$\theta^{old} \leftarrow \eta_i \theta^{old} + (1-\eta_i) \theta$）解耦采样策略与训练策略，本质上是一种 off-policy 训练。论文未讨论如何在不使用重要性采样的前提下处理分布漂移问题。随着训练进行，采样策略与训练策略之间的差异累积可能影响优化稳定性。

**2. 隐式参数化的扩展性。** 该方法能否扩展到更大的模型（如 FLUX.1-Pro 级别）或零样本引导场景而不引入额外的训练开销？当前的实验基于 SD3.5-Medium（约 2.5B 参数），更大规模下的收敛行为尚不明确。

**3. 理论收敛性。** 论文在 Theorem 3.2 中给出了无限数据和容量下的最优解 $v_{\theta^*}(x_t, c, t) = v^{old} + \frac{2}{\beta} \Delta$，但有限样本和有限模型容量下的收敛速率和误差界尚未建立。

**4. 公平性评估缺失。** 尽管该方法完全 CFG-free，避免了条件/无条件双模型训练带来的潜在偏见，但论文未报告不同人群或属性上的公平性评估。CFG-free 设计是否确实带来了更公平的生成分布，需要进一步的实证检验。

## 原文 PDF

![[paperPDFs/ICLR_2026/DiffusionNFT_Online_Diffusion_Reinforcement_with_Forward_Process.pdf]]
