---
title: "Asynchronous Policy Gradient Aggregation for Efficient Distributed Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Asynchronous_Policy_Gradient_Aggregation_for_Efficient_Distributed_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- RNMN
- APGAEDRL
- "Rennala NIGT and Malenia NIGT"
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将异步梯度聚合过程接入NIGT动量归一化策略梯度更新。"
primary_logic: "Rennala按固定梯度数聚合均匀智能体，Malenia按调和均值条件聚合异构智能体，再执行NIGT更新。"
claims:
- "Rennala NIGT通过批量异步聚合和AllReduce把通信复杂度从AFedPG的次优量级降到更优量级。"
- "Malenia NIGT扩展到环境分布和奖励函数异构的分布式策略梯度设置。"
- "在Humanoid和Reacher等异构计算通信场景中，Rennala NIGT比AFedPG和同步NIGT收敛更快。"
- "理论上界与新下界之间仍存在差距，尤其体现在通信复杂度项上。"
---

# Asynchronous Policy Gradient Aggregation for Efficient Distributed Reinforcement Learning

> [!tip] 核心洞察
> 将Rennala SGD的异步聚合思想与NIGT的动量归一化技术结合，在二阶光滑性假设下，通过精心设计的聚合循环条件（Rennala使用固定数量M，Malenia使用调和均值条件）实现最优时间复杂度，同时支持AllReduce操作。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向高效分布式强化学习的异步策略梯度聚合 |
| 英文题名 | Asynchronous Policy Gradient Aggregation for Efficient Distributed Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=SitVEPYv6W) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Rennala NIGT and Malenia NIGT |
| Dataset | Humanoid-v4, Reacher-v4, Walker2d-v4, Hopper-v4 |

> [!tip] 效果简介
> - Humanoid-v4 上，收敛速度（奖励） 为 Rennala NIGT，对比 AFedPG, Synchronized NIGT，变化 在异构计算和通信时间下，Rennala NIGT是唯一鲁棒方法，收敛更快。
> - Reacher-v4 上，收敛速度（奖励） 为 Rennala NIGT，对比 AFedPG, Synchronized NIGT，变化 Rennala NIGT收敛更快。
> - Walker2d-v4 上，收敛速度（奖励） 为 Rennala NIGT，对比 AFedPG, Synchronized NIGT，变化 差距不明显。

## 概要

本文提出两种新的分布式强化学习算法——**Rennala NIGT** 和 **Malenia NIGT**，旨在解决现有异步策略梯度方法（如 AFedPG）在计算与通信效率上的瓶颈。核心创新在于将异步友好的梯度聚合过程（AggregateRennala 和 AggregateMalenia）与 NIGT 动量归一化技术相结合，在二阶光滑性假设下实现了更优的理论时间复杂度，并支持 AllReduce 操作。实验表明，在异构计算和通信环境下，所提方法收敛速度显著优于现有基线。

现有分布式策略梯度方法（如 AFedPG）在异步和异构环境下存在以下瓶颈：
- **不支持异构环境**：AFedPG 无法处理各智能体具有不同环境分布和奖励函数的情况。
- **通信复杂度次优**：AFedPG 的通信复杂度为 $O(\kappa \varepsilon^{-3})$，且在最坏情况下可达 $O(\kappa \varepsilon^{-7/2})$。
- **不支持 AllReduce 操作**：AFedPG 采用贪婪更新策略，每次收到一个梯度就更新，无法利用 AllReduce 实现高效通信。
- **计算复杂度随智能体数量 n 增长而恶化**：AFedPG 的计算复杂度包含 $n^{4/3}$ 项。

本文旨在通过设计异步友好的梯度聚合过程，结合 NIGT 动量归一化技术，同时优化计算和通信复杂度，并支持异构环境。

## 核心方法与创新机理

1. **Rennala NIGT**：针对均匀设置（各智能体环境分布相同），通过 AggregateRennala 过程收集固定数量 M 个梯度后通过 AllReduce 一次性聚合，将通信复杂度从 $O(\kappa \varepsilon^{-3})$ 降低至 $O(\kappa \varepsilon^{-2})$，计算复杂度从 $\tilde{O}((1/n \sum 1/\dot{h}_i)^{-1}(n^{4/3}/\varepsilon^{7/3} + 1/(n\varepsilon^{7/2})))$ 改进为 $\tilde{O}(\min_{m\in[n]}[(1/m \sum 1/\dot{h}_i)^{-1}(1/\varepsilon^2 + 1/(m\varepsilon^{7/2}))])$。

2. **Malenia NIGT**：针对异构设置（各智能体环境分布不同），通过 AggregateMalenia 过程基于调和均值条件收集梯度，首次在支持异步计算的同时支持异构环境，且具有严格更优的理论保证。

3. **新下界**：建立了 Theorem G.1 中的新下界，量化了与最优性之间的剩余差距。

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_SitVEPYv6W_Asynchronous_Policy_Grad/figures/003_Figure_1.jpg]]
*Figure 1: (a) Equal times*

所提方法由三个核心算法模块组成：

- **Algorithm 1 (Core NIGT step)**：核心动量归一化更新步骤，使用动量 $\eta$ 和步长 $\alpha$，通过外推步利用 Hessian 光滑性改进 oracle 复杂度。
- **Algorithm 2 (AggregateRennala)**：均匀设置下的异步梯度聚合过程：广播参数 $\theta$，等待收集 M 个随机梯度，通过 AllReduce 返回平均梯度。
- **Algorithm 3 (AggregateMalenia)**：异构设置下的异步梯度聚合过程：每个智能体维护自己的计数 $M_i$，当调和均值条件 $(1/n \sum 1/M_i)^{-1} \geq M/n$ 满足时停止，返回加权平均梯度。

**问题形式化**：最大化无限时域上的期望折扣累积奖励：
$$J(\theta) = \mathbb{E}_{(s_t, a_t)_{t \geq 0}} \left[ \sum_{t=0}^{\infty} \gamma^t r(s_t, a_t) \right] \quad \text{(Equation 1)}$$

**截断随机策略梯度**（无偏估计量）：
$$g_H(\tau, \theta) = \sum_{t=0}^{H-1} \left( \sum_{h=t}^{H-1} \gamma^h r(s_h, a_h) \right) \nabla \log \pi_\theta(a_t | s_t) \quad \text{(Equation 3)}$$

**核心收敛分析**：

Lemma D.1 给出归一化梯度更新下的一步下降不等式：
$$-J(\theta_{t+1}) \leq -J(\theta_t) - \alpha \|\nabla J(\theta_t)\| + 2\alpha \|d_t - \nabla J(\theta_t)\| + \frac{L_g \alpha^2}{2}$$

Lemma D.2 给出梯度估计误差期望上界：
$$\mathbb{E}[\|d_t - \nabla J_H(\theta_t)\|] \leq (1-\eta)^t \frac{\sigma}{\sqrt{M_{init}}} + \sqrt{\eta} \frac{\sigma}{\sqrt{M}} + L_h \frac{2\alpha^2}{\eta^2} + \frac{4 D_g \gamma^H}{\eta} + 2 D_h \gamma^H \frac{\alpha}{\eta}$$

**Rennala NIGT 时间复杂度**（Theorem 4.4，含通信时间）：
$$\tilde{\mathcal{O}}\left(\kappa\left(\frac{L_g\Delta}{\varepsilon^2}+\frac{\sqrt{L_h}\Delta}{\varepsilon^{3/2}}\right)+\frac{1}{1-\gamma}\min_{m\in[n]}\left[\left(\frac{1}{m}\sum_{i=1}^m\frac{1}{\hbar_i}\right)^{-1}\left(\frac{L_g\Delta}{\varepsilon^2}+\frac{\sqrt{L_h}\Delta}{\varepsilon^{3/2}}+\frac{\sigma^2}{m\varepsilon^2}+\frac{\sigma^2\sqrt{L_h}\Delta}{m\varepsilon^{7/2}}\right)\right]\right)$$

**Malenia NIGT 时间复杂度**（Theorem 5.1，异构设置）：
$$\tilde{\mathcal{O}}\left(\kappa\left(\frac{L_g\Delta}{\varepsilon^2}+\frac{\sqrt{L_h}\Delta}{\varepsilon^{3/2}}\right)+\frac{1}{1-\gamma}\left[\dot{h}_n\left(\frac{L_g\Delta}{\varepsilon^2}+\frac{\sqrt{L_h}\Delta}{\varepsilon^{3/2}}\right)+\left(\frac{1}{n}\sum_{i=1}^n\dot{h}_i\right)\left(\frac{\sigma^2}{n\varepsilon^2}+\frac{\sigma^2\sqrt{L_h}\Delta}{n\varepsilon^{7/2}}\right)\right]\right)$$

## 实验与关键发现

**主要实验结果**：

| 基准任务 | 指标 | 所提方法 | 基线方法 | 结果 | 证据锚点 |
|---------|------|---------|---------|------|---------|
| Humanoid-v4 | 收敛速度 | Rennala NIGT | AFedPG, Synchronized NIGT | 在异构计算和通信时间下，Rennala NIGT 是唯一鲁棒方法，收敛更快 | Figure 2 |
| Reacher-v4 | 收敛速度 | Rennala NIGT | AFedPG, Synchronized NIGT | Rennala NIGT 收敛更快 | Figure 3(a) |
| Walker2d-v4 | 收敛速度 | Rennala NIGT | AFedPG, Synchronized NIGT | 差距不明显 | Figure 3(b) |
| Hopper-v4 | 收敛速度 | Rennala NIGT | AFedPG, Synchronized NIGT | 差距不明显 | Figure 3(c) |
| Humanoid-v4 (异构环境) | 奖励 | Malenia NIGT | AFedPG | Malenia NIGT 获得远高于 AFedPG 的奖励 | Figure 9 |

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_SitVEPYv6W_Asynchronous_Policy_Grad/figures/004_Figure_2.jpg]]
*Figure 2: (b) Heterogeneous times*

**消融实验**：
- 当计算时间相等时，所有方法性能几乎相同（Figure 2(a) and Figure 4）。
- 当计算时间异构且通信时间增加时，Rennala NIGT 的性能差距进一步扩大（Figure 2(c) and Figure 7）。
- 当智能体数量增加到 n=100 时，Rennala NIGT 在异构场景下仍然保持优势（Figures 5-8）。
- 当计算时间递减时，Rennala NIGT 仍然是最快的方法（Figure 8）。

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_SitVEPYv6W_Asynchronous_Policy_Grad/figures/006_Figure_4.jpg]]

**公平性说明**：
- 所有方法从相同的初始点开始，使用相同的随机种子。
- 超参数 $\eta$ 在 Humanoid-v4 任务上统一调优为 0.1，学习率 $\alpha$ 针对每个算法和每个图单独调优。
- Rennala NIGT 的额外参数 M 和 M_init 在 {20, 30, 50} 中调优。
- 实验使用 5 个随机种子，报告 (20%, 80%) 置信区间。

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_SitVEPYv6W_Asynchronous_Policy_Grad/figures/001_Table_1.jpg]]
*Table 1: Homogeneous Setup. The time complexities of distributed methods to find an ε-stationary point in problem (1) up to an error tolerance ε, number of agents n , computation times $\dot { h } _ { i }$ , communication time κ (see Section 4.1), and ignoring logarithmic factors.*

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_SitVEPYv6W_Asynchronous_Policy_Grad/figures/002_Table_2.jpg]]
*Table 2: Heterogeneous Setup. The time complexities of distributed methods to find an ε-stationary point in problem (1) up to an error tolerance ε, computation times $\dot { h } _ { i }$ . , communication time κ (see Section 4.1), and ignoring logarithmic factors.*

![[assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_SitVEPYv6W_Asynchronous_Policy_Grad/figures/005_Figure_1.jpg]]
*Figure 1: (c) Increased communication times Figure 1: Experiments on Humanoid-v4 with increasing heterogeneity of times (from left to right).*

## 定位与知识库关联

本文方法建立在以下工作基础上：
- **Rennala SGD 和 Malenia SGD** (Tyurin & Richtarik, 2023)：提供了异步聚合的基本思想。
- **NIGT** (Fatkhullin et al., 2023)：提供了动量归一化技术，在二阶光滑性下实现 $O(\varepsilon^{-7/2})$ 速率。
- **AFedPG** (Lan et al., 2025)：当前最先进的异步策略梯度方法，本文方法在其基础上改进了计算和通信复杂度，并扩展了异构环境支持。
- **Cutkosky & Mehta (2020)**：提供了核心外推步技术，用于改进 Hessian 光滑性下的 oracle 复杂度。

**局限性**：
1. 理论下界（Theorem G.1）与 Rennala NIGT 上界之间存在间隙，特别是在通信复杂度项上（下界为 $\kappa \varepsilon^{-12/7}$，上界为 $\kappa \varepsilon^{-2}$）。
2. 全局收敛分析需要额外假设（如 Fisher 信息矩阵的正定性），在一般策略参数化下可能不成立。
3. 实验仅在 MuJoCo 连续控制任务上进行，未在更复杂任务中验证。
4. Malenia NIGT 的异构实验仅使用了 n=2 个智能体，环境差异为简单的状态反转。

**开放问题**：
1. 能否缩小 Rennala NIGT 上界与 Theorem G.1 下界之间的间隙？
2. 对于 $(L_g, L_h)$-二阶光滑函数，$\varepsilon^{-12/7}$ 的速率是否可达？
3. STORM/MVR 方法能否适应 RL 中的非平稳分布？
4. 所提方法在大规模语言模型 RLHF 训练中的实际效果如何？

## 原文 PDF

![[paperPDFs/ICLR_2026/Asynchronous_Policy_Gradient_Aggregation_for_Efficient_Distributed_Reinforcement_Learning.pdf]]
