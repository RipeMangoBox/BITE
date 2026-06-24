---
title: "Bayesian Ensemble for Sequential Decision-Making"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Bayesian_Ensemble_for_Sequential_Decision_Making.pdf
aliases:
- BEB
- BESDM
- "Bayesian Ensemble (BE)"
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/bandits_online
core_operator: "将集成成员索引分布视为内部 bandit 后验，并依据奖励反馈动态更新集成采样权重。"
primary_logic: |
  智能体维护集成索引 z 的概率分布，采样索引用于动作选择并用经验风险更新集成参数；随后通过 Beta 或高斯等贝叶斯近似把观测奖励反馈回 index distribution，在 bandit 中形成 BEB，在强化学习中形成 BE-DQN。
claims:
- "动态更新 index distribution 能比固定均匀或标准高斯索引更充分利用集成成员不确定性。"
- "BEB 在 Neural Testbed 和 Mushroom 等 bandit 基准上降低 regret，BE-DQN 在 MiniGrid 等任务上改善集成决策表现。"
---

# Bayesian Ensemble for Sequential Decision-Making

> [!tip] 核心洞察
> 将集成成员的选择视为一个内部的bandit问题，利用贝叶斯推断根据观测到的奖励动态更新成员上的采样分布，而非使用固定的均匀采样。

| 字段 | 内容 |
| ------- | -------------------------------------------------------------------------------- |
| 中文题名 | 用于序列决策的贝叶斯集成 |
| 英文题名 | Bayesian Ensemble for Sequential Decision-Making |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=s2hxd8JghB) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/bandits_online |
| Method | Bayesian Ensemble (BE) |
| Dataset | Neural Testbed d=2, Neural Testbed d=10, Neural Testbed d=50 |

> [!tip] 效果简介
> - Neural Testbed d=2 上，regret improvement 为 ensemble+(BEB)，对比 ensemble+，变化 37.0%。
> - Neural Testbed d=10 上，regret improvement 为 ensemble+(BEB)，对比 ensemble+，变化 12.8%。
> - Neural Testbed d=50 上，regret improvement 为 ensemble+(BEB)，对比 ensemble+，变化 42.2%。

## 概述

本文提出**Bayesian Ensemble (BE)**，一个统一的框架，用于增强基于集成的序列决策方法。核心思想是将集成成员的选择视为一个内部的bandit问题，通过贝叶斯推断根据观测到的奖励动态更新成员上的采样分布（index distribution），而非使用固定的均匀采样。该框架在上下文bandit和强化学习两个领域进行了实例化，分别称为**BEB (Bayesian Ensemble for Bandits)** 和 **BE-DQN (Bayesian Ensemble DQN)**。实验表明，BEB在Neural Testbed和Mushroom等基准上显著降低了累积遗憾，BE-DQN在MiniGrid等部分可观测环境中优于DQN、Ensemble DQN等基线方法。

## 背景与动机

现有基于集成的Thompson采样方法（如ensemble+、hypermodel）在决策过程中保持固定的index distribution（如离散均匀分布或标准高斯分布）。这些方法虽然通过集成成员的不确定性来近似后验分布，但未能充分利用集成成员多样性的不确定性，导致后验分布近似不够精确。具体而言，这些方法维护的采样index distribution在决策过程中保持不变，没有与观测到的奖励反馈建立直接联系。

本文的核心动机是：通过贝叶斯推断动态更新集成成员的index distribution，将index distribution与奖励反馈直接关联，从而更精确地近似后验分布，提升决策性能。

## 核心创新

本文的核心创新在于将集成成员的选择视为一个内部的bandit问题，利用贝叶斯推断根据观测到的奖励动态更新成员上的采样分布，而非使用固定的均匀采样。具体创新点包括：

1. **动态index distribution更新**：通过贝叶斯推断（精确或近似）根据观测到的奖励动态更新index distribution，而非保持固定不变。
2. **index distribution与奖励的直接关联**：直接建立index distribution与奖励分布之间的贝叶斯连接，实现更精确的后验分布近似。
3. **统一框架**：将贝叶斯index distribution更新适配到上下文bandit和强化学习两个领域。

## 整体框架

![[assets/figures/papers/iclr26_0002_s2hxd8JghB_Bayesian_Ensemble_for_Sequential_Decision-Making/figures/001_Figure_1.jpg]]
*Figure 1: The Bayesian Ensemble (BE) framework. The agent maintains a probability distribution $p ^ { ( \bar { t } ) }$ for the index z $\in { \mathcal { Z } }$ and bridges the gap between the index and reward distribution.

Bayesian Ensemble框架的核心流程如下：

1. **维护index distribution**：智能体维护索引z的概率分布p^{(t)}。
2. **采样集成成员**：从p^{(t)}中采样索引z^{(t)}。
3. **动作选择**：根据采样的集成成员选择最大化期望奖励的动作。
4. **参数更新**：使用经验风险最小化更新集成参数θ。
5. **index distribution更新**：使用贝叶斯推断（精确或近似）更新index distributionp。

Figure 1展示了Bayesian Ensemble框架，智能体维护索引z的概率分布p^{(t)}，并桥接索引与奖励分布之间的差距。

## 核心模块与公式推导

### 5.1 集成奖励分布模型

神经网络集成将上下文x和索引z映射到N个奖励值上的概率分布，由θ参数化：

$$f(x \in \cdot ; z \in \cdot , \theta \in \cdot) : \mathcal{X} \times \mathcal{Z} \times \Theta \to \Delta^N \quad \text{(Equation 1)}$$

集成输出的第i个坐标给出了奖励等于R_i的估计概率：

$$\hat{\mathrm{Pr}}\{r = R_i\} = f(r; z, \theta)_i, \forall i \in [N] \quad \text{(Equation 2)}$$

### 5.2 动作选择规则

根据采样的集成成员选择最大化期望奖励的动作：

$$\mathbf{x}^{(t)} \gets \arg\max_{\mathbf{x} \in \mathcal{X}^{(t)}} \sum_{i=1}^N R_i \cdot f(\mathbf{x}; \mathbf{z}^{(t)}, \mathbf{\theta}^{(t)})_i \quad \text{(Equation 3)}$$

### 5.3 参数更新

通过最小化index distributionp上的期望损失来优化集成参数θ：

$$\min_{\mathbf{\theta} \in \Theta} \sum_{(\mathbf{x}, r) \in \mathcal{D}} \mathbb{E}_{z \sim p} \left[ \ell(r, f(\mathbf{x}; z, \mathbf{\theta})) \right] \quad \text{(Equation 4)}$$

### 5.4 BEB的具体实例化

**ensemble+的增强**：将离散均匀index distribution替换为Beta分布权重：z = argmax_i w_i, w_i ∼ Beta(α_i, β_i)。

**hypermodel的增强**：将多元标准高斯分布替换为具有可学习均值和方差的多元高斯分布：z_i ∼ N(μ_i, σ_i^2)。

### 5.5 BE-DQN

BE-DQN维护K个独立的Q网络，每个网络具有Beta分布权重。动作选择使用具有最大采样权重的Q网络，然后更新该网络的Beta参数：(α_j, β_j) ← (α_j, β_j) + (r^{(t)}, 1 - r^{(t)})。

BE-DQN的目标Q值使用所有集成Q网络的加权平均：

$$y_{s,a}^i = \mathbb{E}_{\mathcal{B}} [r + \gamma \max_{a'} \sum_{k=1}^K p_k Q(s', a', \theta_{i-1}^k) | s, a] \quad \text{(Equation 5)}$$

最终Q值为集成成员的加权平均：

$$Q_i^{\mathrm{BE-DQN}}(s, a) = \sum_{k=1}^K p_k^i Q(s, a; \theta_i^k) \quad \text{(Algorithm 2 output)}$$

### 5.6 方差分析

Theorem 1证明：BE-DQN的variance upper bound为DQN方差，下界为Ensemble DQN方差，保证了训练稳定性。

在单向MDP（Figure 2）中，各方法的Q值方差分别为：

- DQN: $\mathrm{Var}[Q_i^{\mathrm{DQN}}(s_0, a)] = \sum_{m=0}^{M-1} \gamma^{2m} \sigma_{s_m}^2$
- Ensemble DQN: $\mathrm{Var}[Q_i^{\mathrm{E-DQN}}(s_0, a)] = \frac{1}{K} \sum_{m=0}^{M-1} \gamma^{2m} \sigma_{s_m}^2$
- BE-DQN: $\mathrm{Var}[Q_i^{\mathrm{BE-DQN}}(s_0, a)] = \sum_{k=1}^K p_k^2 \sum_{m=0}^{M-1} \gamma^{2m} \sigma_{s_m}^2$

## 实验与分析

### 6.1 主要结果

**Neural Testbed和Mushroom上的遗憾比较（Figure 3）**：

| 基准 | 方法 | regret improvement |
|------|------|----------|
| Neural Testbed d=2 | ensemble+(BEB) vs ensemble+ | 37.0% |
| Neural Testbed d=10 | ensemble+(BEB) vs ensemble+ | 12.8% |
| Neural Testbed d=50 | ensemble+(BEB) vs ensemble+ | 42.2% |
| Neural Testbed d=2 | hypermodel(BEB) vs hypermodel | 69.8% |
| Neural Testbed d=10 | hypermodel(BEB) vs hypermodel | 22.8% |
| Neural Testbed d=50 | hypermodel(BEB) vs hypermodel | 30.3% |
| Mushroom | ensemble+(BEB) vs ensemble+ | 8.7% |
| Mushroom | hypermodel(BEB) vs hypermodel | 4.8% |

**Yahoo!R6B上的累积奖励（Table 5）**：在Yahoo!R6B子集（前1M事件）上，ensemble+(BEB)相比ensemble+的clicks提升了3.2%。

![[assets/figures/papers/iclr26_0002_s2hxd8JghB_Bayesian_Ensemble_for_Sequential_Decision-Making/figures/019_Table_5.jpg]]
*Table 5: Cumulative rewards on the Yahoo!R6B subset (first 1M events)*

**MiniGrid上的性能（Figure 4）**：在MiniGrid的五个环境中，BE-DQN在大多数任务上优于DQN、E-DQN、RE-DQN和UAAC。

### 6.2 消融实验

**集成规模的影响（Table 6）**：随着集成成员数量从25增加到100，ensemble+(BEB)的相对regret improvement从28.23%增长到47.97%。

**计算效率（Table 7, Table 8）**：将索引更新频率降低到原来的1/3，计算成本显著降低，同时仍能保持有竞争力的regret improvement。

### 6.3 公平性说明

- 所有实验在相同硬件（四核Intel Core i5, 16GB RAM）上运行，每个实验重复20次（bandit）或5次（RL）不同随机种子。
- 超参数调优在验证集上进行，最终结果在测试集上报告。
- 计算开销分析显示，BEB框架允许通过调整更新频率来平衡性能和效率。

### 补充图表

![[assets/figures/papers/iclr26_0002_s2hxd8JghB_Bayesian_Ensemble_for_Sequential_Decision-Making/figures/007_Table_1.jpg]]
*Table 1: Elapsed wall time(s) on Neural Testbed*

![[assets/figures/papers/iclr26_0002_s2hxd8JghB_Bayesian_Ensemble_for_Sequential_Decision-Making/figures/008_Table_2.jpg]]
*Table 2: Cumulative rewards on Yahoo!R6B*

![[assets/figures/papers/iclr26_0002_s2hxd8JghB_Bayesian_Ensemble_for_Sequential_Decision-Making/figures/009_Table_3.jpg]]
*Table 3: Performance of agents on MiniGrid after 1e5 frames training. We report the average rewards and standard error for each method. All results are averaged over 5 random seeds, with each seed tested for 100 episodes.*

![[assets/figures/papers/iclr26_0002_s2hxd8JghB_Bayesian_Ensemble_for_Sequential_Decision-Making/figures/016_Table_4.jpg]]
*Table 4: Hyperparameters used in BE-DQN.*

## 方法谱系与知识库定位

Bayesian Ensemble属于基于集成的贝叶斯近似方法谱系。它与以下方法密切相关：

- **Thompson Sampling (Thompson, 1933)**：原始Thompson采样方法，通过采样后验分布进行决策。
- **Ensemble Sampling (Lu & Roy, 2017)**：使用集成近似后验分布进行采样。
- **Deep Thompson Sampling (Riquelme et al., 2018)**：将深度集成与Thompson采样结合。
- **ensemble+ (Osband et al., 2018)**：使用随机先验函数的深度集成方法。
- **hypermodel (Dwaracherla et al., 2020)**：使用超网络将索引映射到模型参数。
- **Ensemble DQN (Anschel et al., 2017)**：使用多个Q网络的平均值来降低方差。
- **Random Ensemble DQN (Agarwal et al., 2020)**：使用随机加权组合多个Q网络。

BE的核心区别在于：现有方法保持固定的index distribution，而BE通过贝叶斯推断动态更新index distribution，直接建立index distribution与奖励反馈之间的连接，从而实现更精确的后验分布近似。

**局限性**：
- 理论分析假设零奖励环境，方差作为策略稳定性的代理指标。
- 当奖励本身是随机的（如Beta分布），1/K下界不再成立，尽管BE-DQN方差仍低于标准DQN。
- 计算开销方面，BEB的索引更新（尤其是hypermodel的变分推断）增加了额外计算成本，但可通过调整更新频率来缓解。

**开放问题**：
- 如何将BEB框架扩展到更复杂的RL算法（如PPO、SAC）？
- 在奖励随机性较强的环境中，如何显式建模并界定环境奖励的方差？
- index distributionp的通用结构是什么？除了Beta分布和高斯分布，是否还有其他有效的参数化形式？
- BEB框架在离线RL或模仿学习场景中的表现如何？
- 如何进一步降低BEB的计算开销，使其适用于超大规模集成？

## 原文 PDF

![[paperPDFs/ICLR_2026/Bayesian_Ensemble_for_Sequential_Decision_Making.pdf]]
