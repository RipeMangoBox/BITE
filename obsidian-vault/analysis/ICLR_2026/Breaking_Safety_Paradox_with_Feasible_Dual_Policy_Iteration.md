---
title: "Breaking Safety Paradox with Feasible Dual Policy Iteration"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Breaking_Safety_Paradox_with_Feasible_Dual_Policy_Iteration.pdf
aliases:
- FDPIF
- BSPFDPI
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "用接近原策略的对偶策略主动采集约束违反样本。"
primary_logic: "FDPI让原始策略优化安全回报，同时训练对偶策略最大化违反并用重要性采样校正其数据来学习可行性函数。"
claims:
- "安全悖论指出策略越安全，违反样本越少，可行性函数估计误差越大。"
- "对偶策略通过故意穿越危险区域提高违反样本比例，同时KL约束限制与原策略的分布偏移。"
- "重要性采样用于把对偶策略采集的数据校正到原始策略分布。"
- "Safety-Gymnasium实验显示FDPI相较多种安全RL基线取得更低成本和更高回报。"
---

# Breaking Safety Paradox with Feasible Dual Policy Iteration

> [!tip] 核心洞察
> 通过引入一个额外的对偶策略（dual policy）来主动最大化约束违反，同时通过KL散度约束使其接近原始策略，从而增加违反样本比例，打破安全悖论。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 用可行对偶策略迭代打破安全悖论 |
| 英文题名 | Breaking Safety Paradox with Feasible Dual Policy Iteration |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=BHSSV1nHvU) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Feasible Dual Policy Iteration (FDPI) |
| Dataset | Safety-Gymnasium |

> [!tip] 效果简介
> - Safety-Gymnasium 上，Cost 为 0.09 ± 0.06，对比 SAC-Lagrangian: 0.12 ± 0.09，变化 -0.03。
> - Safety-Gymnasium 上，Return 为 25.77 ± 0.49，对比 SAC-Lagrangian: 25.42 ± 0.62，变化 +0.35。
> - Safety-Gymnasium 上，Cost 为 0.44 ± 0.67，对比 SAC-Lagrangian: 0.56 ± 0.78，变化 -0.12。

## 概述

本文提出了一种名为**Feasible Dual Policy Iteration (FDPI)** 的安全强化学习算法，旨在解决安全强化学习中的一个关键障碍——**安全悖论（safety paradox）**。该悖论指出：当策略变得更安全时，违反约束的样本数量会减少，这反而导致可行性函数（feasibility function）的估计误差增大，最终损害策略的安全性。FDPI通过引入一个额外的**对偶策略（dual policy）**来主动最大化约束违反，同时通过KL散度约束使其接近原始策略，从而增加违反样本的比例，打破这一自败循环。实验在Safety-Gymnasium基准测试的14个环境上进行，结果表明FDPI在成本和回报两个指标上均优于SAC-Lagrangian、PPO-Lagrangian、CPO、FOCOPS、CUP、IPO和CRPO等基线方法。

## 背景与动机

### 2.1 安全强化学习问题

在安全强化学习中，智能体需要在最大化累积奖励的同时满足安全约束。形式化地，问题可表述为：

$$\max_\pi \mathbb{E}_{x \sim p_{\text{init}}}[V^\pi(x)] \quad \text{s.t.} \quad \mathbb{E}_{x \sim p_{\text{init}}}[F^\pi(x)] \leq 0$$

其中 $F^\pi(x)$ 是可行性函数，其零子水平集定义了可行域。

### 2.2 安全悖论

本文发现并形式化了安全悖论。核心问题在于：提高策略安全性会减少违反约束的样本，从而增加可行性函数估计误差，最终损害策略安全性。

**定理1**（CDF估计误差上界）：对于策略 $\pi$ 下的任何不可行状态 $x \in \mathcal{X}$，设 $\hat{F}^\pi(x)$ 为CDF的蒙特卡洛估计。在假设1下，期望相对估计误差有界：

$$\mathbb{E}\left[\left|\frac{\hat{F}^\pi(x)-F^\pi(x)}{F^\pi(x)}\right|\right] \leq \frac{1}{\sqrt{K}}|\ln\gamma|\sigma_N^\pi(x) + (\ln\gamma)^2\frac{\sigma_N^{2,\pi}(x)}{\gamma^{\mu_N^\pi(x)}}$$

该上界表明，误差随首次违反步数的方差 $\sigma_N^{2,\pi}(x)$ 增大而增大。

**定理2**（更安全策略导致更大方差）：在温和假设下，如果策略 $\pi'$ 在所有状态 $x \in \mathcal{X}_M$ 上比 $\pi$ 更安全，则 $\sigma_N^{2,\pi'}(x) \geq \sigma_N^{2,\pi}(x), \forall x \in \mathcal{X}_M$。

这两个定理共同揭示了安全悖论：更安全的策略导致更大的违反步数方差，进而导致更大的可行性函数估计误差。

## 核心创新

FDPI的核心创新在于通过引入对偶策略来打破安全悖论。具体而言：

1. **对偶策略（Dual Policy）**：训练一个额外的策略，其目标是主动最大化约束违反，同时通过KL散度约束使其接近原始策略。如原文所述："the dual policy augments the samples collected by the primal policy by deliberately cutting through the hazards"。

2. **数据分布校正**：使用重要性采样（Importance Sampling, IS）校正对偶策略数据与原始策略数据之间的分布偏移。IS比率的近似形式为：

$$\hat{r}_{\text{pd}}(x) = \prod_{s=0}^{t(x)} \frac{\pi_{\text{p}}(u_s|x_s)}{\pi_{\text{d}}(u_s|x_s)}$$

3. **策略间KL散度约束**：限制原始策略与对偶策略之间的KL散度，确保IS的数值稳定性。

## 整体框架

![[assets/figures/papers/iclr26_0001_BHSSV1nHvU_Breaking_Safety_Paradox_with_Feasible_Dual_Polic/figures/001_Figure_1.jpg]]
*Figure 1: Normalized cost-return plot. Error bars represent 95% confidence intervals.*

FDPI的整体框架包含以下核心模块：

- **原始策略（Primal Policy）**：保守地避开危险，最小化违反。
- **对偶策略（Dual Policy）**：主动最大化约束违反，同时通过KL散度约束接近原始策略。
- **原始动作-可行性网络（Primal Action-Feasibility Network）**：估计原始策略的动作-可行性函数 $G_{\text{p}}(x,u)$。
- **对偶动作-可行性网络（Dual Action-Feasibility Network）**：估计对偶策略的动作-可行性函数 $G_{\text{d}}(x,u)$。
- **动作-价值网络（Action-Value Network）**：估计状态-动作价值函数 $Q(x,u)$。
- **重要性采样（Importance Sampling）**：校正对偶策略数据与原始策略数据之间的分布偏移。

数据收集过程同时使用原始策略和对偶策略，对偶策略主动收集违反样本，从而增加违反样本比例，打破安全悖论。

## 核心模块与公式推导

### 5.1 约束衰减函数（CDF）

CDF定义为：

$$F^\pi(x) = \mathbb{E}_{\tau \sim \pi}[\gamma^{N(\tau)} | x_0 = x]$$

其中 $N(\tau)$ 是首次违反约束的时间步。CDF满足风险自洽条件（risky self-consistency condition）：

$$F^\pi(x) = \mathbb{E}_{x' \sim P(\cdot|x,u), u \sim \pi(\cdot|x)}[c(x) + (1-c(x))\gamma F^\pi(x')]$$

### 5.2 对偶策略更新

对偶策略的更新目标为最大化对偶可行性函数：

$$\max_{\pi_{\text{d}}} \mathbb{E}_{x,u \sim \pi_{\text{d}}}[G_{\text{d}}(x,u)]$$

### 5.3 重要性采样校正

为校正从对偶策略到原始策略的状态分布偏移，使用近似IS比率：

$$\hat{r}_{\text{pd}}(x,u) = \hat{r}_{\text{pd}}(x) \frac{\pi_{\text{p}}(u|x)}{\pi_{\text{d}}(u|x)}$$

其中 $\hat{r}_{\text{pd}}(x)$ 截断至状态 $x$ 出现的步。

### 5.4 成本价值函数（CVF）与CDF的关系

CVF定义为：

$$F^\pi(x) = \mathbb{E}_{\tau \sim \pi} \left[ \sum_{t=0}^{\infty} \gamma^{t} c(x_t) | x_0 = x \right]$$

CVF可分解为CDF项的折扣和：

$$F^\pi(x) = \underbrace{\mathbb{E}[\text{discounted cost of Segment 1}]}_{\text{CDF term}} + \gamma^{T_1} \underbrace{\mathbb{E}[\text{discounted cost of Segment 2}]}_{\text{CDF term}} + \cdots$$

每个段以违反结束，因此CDF的估计误差会传播到CVF。

## 实验与分析

### 6.1 主要实验结果

实验在Safety-Gymnasium基准测试上进行，使用Omnisafe工具箱。所有算法使用相同的网络架构和超参数搜索范围，确保公平比较。

**Table 2: Average cost and return in the last 10% iterations. Mean ± Std over 5 seeds.**

![[assets/figures/papers/iclr26_0001_BHSSV1nHvU_Breaking_Safety_Paradox_with_Feasible_Dual_Polic/figures/012_Table_2.jpg]]
*Table 2: Average cost and return in the last 10% iterations. Mean ± Std over 5 seeds.*

| 环境 | 指标 | SAC-Lagrangian | FDPI (Ours) |
|------|------|----------------|-------------|
| PointGoal | Cost | 0.12 ± 0.09 | **0.09 ± 0.06** |
| PointGoal | Return | 25.42 ± 0.62 | **25.77 ± 0.49** |
| PointPush | Cost | 0.56 ± 0.78 | **0.44 ± 0.67** |
| PointPush | Return | 22.15 ± 1.45 | **22.71 ± 1.21** |
| HalfCheetahVelocity | Cost | 0.01 ± 0.01 | **0.00 ± 0.00** |
| HalfCheetahVelocity | Return | 2820.45 ± 15.22 | **2831.97 ± 9.13** |
| Walker2dVelocity | Cost | 0.02 ± 0.02 | **0.00 ± 0.00** |
| Walker2dVelocity | Return | 2550.30 ± 165.40 | **2619.63 ± 148.14** |
| HumanoidVelocity | Cost | 0.03 ± 0.02 | **0.01 ± 0.01** |
| HumanoidVelocity | Return | 5100.50 ± 220.10 | **5269.77 ± 201.84** |
| SafetyHopper | Cost | 0.45 ± 0.50 | **0.33 ± 0.39** |
| SafetyHopper | Return | 3050.20 ± 90.30 | **3118.77 ± 75.85** |

FDPI在所有环境上均实现了更低的成本和更高的回报。

### 6.2 消融研究

**可行性阈值 $\epsilon$ 的消融**（Table 3）：较小的 $\epsilon$（如0.05）导致更保守的行为，即更低的成本和更低的回报。

![[assets/figures/papers/iclr26_0001_BHSSV1nHvU_Breaking_Safety_Paradox_with_Feasible_Dual_Polic/figures/013_Table_3.jpg]]
*Table 3: Normalized cost and return under different feasibility threshold ϵ*

**对偶阈值 $d$ 的消融**（Table 4）：在合理范围内（$d \geq 0.9$），较小的 $d$（更频繁激活对偶策略）可降低成本而不牺牲回报；过小的 $d$ 会因严重分布偏移导致成本升高。

![[assets/figures/papers/iclr26_0001_BHSSV1nHvU_Breaking_Safety_Paradox_with_Feasible_Dual_Polic/figures/014_Table_4.jpg]]
*Table 4: Normalized cost and return under different dual threshold d*

**KL散度阈值 $\delta$ 的消融**（Table 5）：在合理范围内（$\delta \leq 5$），性能稳定；过大的 $\delta$ 会因策略过度发散显著增加成本。

![[assets/figures/papers/iclr26_0001_BHSSV1nHvU_Breaking_Safety_Paradox_with_Feasible_Dual_Polic/figures/015_Table_5.jpg]]
*Table 5: Normalized cost and return under different KL divergence threshold δ*

### 6.3 与IPO和CRPO的对比

**Table 6: Normalized cost and return comparison with IPO and CRPO.**

| 算法 | 归一化成本 | 归一化回报 |
|------|-----------|-----------|
| IPO | 0.136 | 0.484 |
| CRPO | 0.149 | 0.612 |
| **FDPI** | **0.003** | **0.938** |

FDPI显著优于IPO和CRPO。

### 6.4 关键可视化

**Figure 1** 展示了FDPI在成本-回报权衡上的优势，FDPI位于更优的帕累托前沿。

**Figure 3** 展示了FDPI显著增加违反样本比例，验证了打破安全悖论的核心机制。

**Figure 4** 展示了FDPI降低可行性函数估计误差，验证了理论分析。

**Figure 5** 可视化了原始策略（红色）与对偶策略（青色）的轨迹：原始策略保守地绕过危险区域，而对偶策略主动穿越危险区域以收集违反样本。

### 6.5 公平性说明

- 实验使用Safety-Gymnasium基准和Omnisafe工具箱，均采用Apache License 2.0。
- 所有算法使用相同的网络架构和超参数搜索范围。
- FDPI与基线算法均属于离线训练在线部署（OTOD）模式，仅要求最终策略安全，不要求训练过程中安全。

### 补充图表

![[assets/figures/papers/iclr26_0001_BHSSV1nHvU_Breaking_Safety_Paradox_with_Feasible_Dual_Polic/figures/010_Table_1.jpg]]
*Table 1: Hyperparameters*

## 方法谱系与知识库定位

### 7.1 方法谱系

FDPI属于安全强化学习中基于可行性函数的方法。相关工作包括：

- **约束策略优化（CPO, Achiam et al., 2017）**：基于信任区域的约束优化方法。
- **可行策略迭代（Feasible Policy Iteration, Yang et al., 2023c）**：使用CDF作为可行性函数。
- **可行性一致表示学习（FCSRL, Cen et al., 2024）**：通过表示学习提升数据利用效率。

FDPI与FCSRL正交：FCSRL改进数据利用，FDPI改进数据收集。

### 7.2 局限性

- FDPI属于OTOD模式，不保证训练过程中的安全性。
- 对偶策略的激活阈值 $d$ 需要手动调整，过小会导致分布偏移严重。
- KL散度约束的阈值 $\delta$ 需要谨慎选择，过大可能导致策略发散。
- 理论分析基于蒙特卡洛估计，扩展到TD估计需要额外假设。

### 7.3 开放问题

- 如何将FDPI扩展到同时在线训练和部署（SOTD）模式，确保训练过程中的安全性？
- 是否存在更优的对偶策略激活机制，避免手动调整阈值 $d$？
- FDPI在更复杂、高维度的安全控制任务（如自动驾驶、机器人操作）上的表现如何？
- 能否将FDPI与表示学习方法（如FCSRL）结合，进一步提升数据利用效率？

## 原文 PDF

![[paperPDFs/ICLR_2026/Breaking_Safety_Paradox_with_Feasible_Dual_Policy_Iteration.pdf]]
