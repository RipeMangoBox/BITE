---
title: "EUBRL: Epistemic Uncertainty Directed Bayesian Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EUBRL_Epistemic_Uncertainty_Directed_Bayesian_Reinforcement_Learning.pdf
project_link: null
code_link: null
openreview_forum_id: KASqlcI6Nm
aliases:
- EUBRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/online
core_operator: "认知不确定性引导（epistemic guidance）通过将认知不确定性直接纳入智能体的目标函数，在不确定时强化探索，在确定时侧重利用，实现探索与利用的自适应解耦。"
primary_logic: "利用概率推断将认知不确定性建模为奖励的一部分，通过不确定性概率$P_U$动态调节任务奖励与内在不确定性奖励，使得探索更具原则性，并自适应减少每步遗憾。"
claims:
- "EUBRL 在无限时域折扣 MDP 上同时取得近 minimax 最优的遗憾和样本复杂度。"
- "认知抵抗项$\\Re^t(s)$自适应降低每步遗憾，并通过不确定性概率定量刻画。"
- "EUBRL 在 Chain、Loop、DeepSea、LazyChain 等稀疏/长时程/随机任务上以显著优势超越多种基线。"
- "Chain 上 Average Return = 3473"
---

# EUBRL: Epistemic Uncertainty Directed Bayesian Reinforcement Learning

> [!tip] 核心洞察
> 利用概率推断将认知不确定性建模为奖励的一部分，通过不确定性概率$P_U$动态调节任务奖励与内在不确定性奖励，使得探索更具原则性，并自适应减少每步遗憾。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | EUBRL：认知不确定性引导的贝叶斯强化学习 |
| 英文题名 | EUBRL: Epistemic Uncertainty Directed Bayesian Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KASqlcI6Nm) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/online |
| Method | EUBRL |
| Dataset | Chain, Loop (2 Loops), DeepSea (stochastic), LazyChain |

> [!tip] 效果简介
> - Chain 上，Average Return 为 3473，对比 3465 (VBRB)，变化 +8。
> - Loop (2 Loops) 上，Average Return 为 395，对比 394 (RMAX)，变化 +1。
> - DeepSea (stochastic) 上，Success Rate 为 perfectly solves without failure，对比 其他方法随尺寸增长成功率骤降，变化 显著提升。

## 概要

强化学习中的高效探索是长期存在的核心挑战。现有探索策略——无论是基于乐观主义的频率派方法（如 RMAX、MBIE-EB），还是基于后验采样的贝叶斯方法（如 PSRL、BOSS）——在稀疏奖励、长时程和随机环境中效率低下。根本瓶颈在于不确定性量化不足：这些方法无法精细区分认知不确定性（可通过更多数据减少）与偶然不确定性（环境固有噪声），导致不必要的探索和缓慢收敛。

EUBRL（Epistemic Uncertainty Directed Bayesian Reinforcement Learning）针对这一瓶颈提出了原则性解决方案。其核心机制是将认知不确定性直接纳入智能体的目标函数：通过概率图模型引入“不确定性”隐变量 $U$，将最优性 $O$ 划分为确定与不确定两种情形（Figure 4），并据此动态调节任务奖励与内在不确定性奖励的混合比例。具体而言，EUBRL 的奖励函数为：

$$r_b^{\mathrm{EUBRL}}(s,a) := \left(1 - P(U = 1 | s,a)\right) r_b(s,a) + P(U = 1 | s,a) \mathcal{E}_b(s,a)$$

其中不确定性概率 $P(U = 1 \mid s,a) = \frac{\mathcal{E}_b(s,a)}{\mathcal{E}_{\max}}$ 由归一化的认知不确定性 $\mathcal{E}_b(s,a)$ 定义，而 $\mathcal{E}_b(s,a) = h(\mathcal{E}_T(s,a), \mathcal{E}_R(s,a))$ 整合了转移不确定性与奖励不确定性。当认知不确定性高时，智能体侧重探索（内在奖励主导）；当认知不确定性低时，侧重利用（任务奖励主导），从而实现探索与利用的自适应解耦。

理论上，EUBRL 在无限时域折扣 MDP 上同时取得了近 minimax 最优的遗憾上界和样本复杂度上界。Theorem 2 给出遗憾上界 $\widetilde{\mathcal{O}}\left( \frac{\sqrt{S A T}}{(1-\gamma)^{1.5}} + \frac{S^2 A}{(1-\gamma)^2} \right)$，Theorem 3 给出样本复杂度上界 $\widetilde{\mathcal{O}}\left( \left( \frac{S A}{\epsilon^2 (1-\gamma)^3} + \frac{S^2 A}{\epsilon (1-\gamma)^2} \right) \log \frac{1}{\delta} \right)$，两者均与已知下界匹配。关键技术在于 Theorem 1 中引入的**认知抵抗项** $\Re^t(s) := 2 P_U^t(s, \pi_t(s)) + \frac{9}{7} P_U^t(s, \pi^{\star}(s))$，它自适应地减小每步遗憾上界：当智能体对当前动作或最优动作的认知不确定性较高时，遗憾上界收紧，从而加速收敛。

实验上，EUBRL 在 Chain、Loop、DeepSea 和 LazyChain 四个基准任务上进行了验证（任务规格见 Table 2），这些任务覆盖了稀疏奖励、长时程和随机性等挑战性特征。在 Chain 环境中，EUBRL 取得最高平均回报 3473（Table 1）；在 2 Loops 的 Loop 环境中，EUBRL 以平均回报 395 超越 RMAX 的 394（Table 3）；在 DeepSea 的随机变体上，EUBRL 是唯一能完美解决任务的方法，而其他方法随问题规模增长成功率骤降（Figure 2）；在 LazyChain 上，EUBRL 在成功率和平均解算步数上均一致优于所有基线（Figure 3）。所有结果均在 20 或 500 个随机种子上平均，保证统计可靠性。

EUBRL 的方法定位是**表格型贝叶斯强化学习**，其算法流程（Algorithm 1）包含三个核心模块：信念更新（利用共轭先验在封闭形式下更新后验）、策略求解（构造带认知引导奖励的 MDP 并通过值迭代求解）、以及定时重置与策略更新。当前方法依赖 Dirichlet/Normal 先验组合以取得近 minimax 最优性（Corollary 1），但存在若干已知局限：先验错误指定下可能陷入次优策略（附录 K 给出两臂 Bandit 反例）；Normal-Gamma 先验在确定性 MDP 中可能导致认知不确定性不足（Proposition 1）；认知不确定性估计目前限于表格型表示，扩展至函数逼近和大规模问题仍需进一步研究。



强化学习（RL）的核心挑战之一是在探索与利用之间取得平衡。智能体必须主动探索未知状态-动作对以收集信息，同时利用已有知识最大化累积奖励。这一矛盾在**稀疏奖励、长时程依赖和随机环境**中尤为尖锐——现有探索策略在这些场景下效率低下，往往导致不必要的探索和缓慢收敛。

### 现有方法的瓶颈

当前主流的探索范式可大致分为两类：

**乐观主义方法**（如 RMAX、MBIE-EB、BEB）通过人为抬高未知状态-动作的价值来激励探索。其核心假设是“未知即乐观”，但这一假设在稀疏奖励环境中会导致过度探索：智能体可能花费大量步数在无奖励区域徘徊，因为乐观偏差掩盖了真实的零奖励信号。频率派方法依赖 Hoeffding 不等式等浓度界来构建置信区间，但这些界往往过于保守，无法利用先验知识加速学习。

**贝叶斯方法**（如 PSRL、BOSS）通过维护状态转移和奖励的后验分布来刻画不确定性。后验采样（PSRL）在每个 episode 从后验中采样一个 MDP 并求解最优策略，理论上具有近 minimax 最优的遗憾界。然而，PSRL 的探索完全由采样随机性驱动，缺乏对“哪些状态-动作更需要探索”的细粒度判断。当环境存在长时程依赖时（如 Loop、DeepSea），随机采样可能长期忽略关键的状态-动作对，导致收敛缓慢。Mean-MDP 等方法直接使用后验均值规划，完全放弃了探索加成，在稀疏奖励下几乎无法学习。

**根本瓶颈在于**：现有方法对不确定性的利用不够精细。它们要么将不确定性作为全局探索奖励（缺乏自适应性），要么完全依赖随机采样（缺乏方向性），缺乏一种**将认知不确定性直接纳入决策目标**的机制，使得探索强度能够随不确定性动态调节。

### 认知不确定性引导的动机

人类在学习新任务时，会自然地对不确定的情况投入更多探索精力，而在确定的情况下果断利用。这种“认知不确定性引导”（epistemic guidance）的行为模式启发我们：**智能体应当明确量化“自己对环境知道多少”，并将这一信息注入决策过程**。

具体而言，认知不确定性（epistemic uncertainty）反映的是由于数据不足导致的模型不确定性——它可以通过收集更多数据来减少。这与偶然不确定性（aleatoric uncertainty，环境固有的随机性）不同。在 RL 中，认知不确定性有两个来源：

- **转移不确定性** $\mathcal{E}_T(s,a)$：对状态转移概率 $P(s'|s,a)$ 的估计不准确；
- **奖励不确定性** $\mathcal{E}_R(s,a)$：对奖励函数 $r(s,a)$ 的估计不准确。

当智能体对某个状态-动作对的转移或奖励高度不确定时，它应当倾向于探索该动作以获取信息；当不确定性很低时，它应当信任当前估计并选择最大化期望奖励的动作。这一原则性的探索策略有望在稀疏奖励和长时程环境中显著提升效率。

### 本文的核心思路

EUBRL（Epistemic Uncertainty Directed Bayesian Reinforcement Learning）的核心洞察是：**通过概率推断将认知不确定性建模为奖励的一部分**，利用不确定性概率 $P_U$ 动态调节任务奖励与内在不确定性奖励的混合比例：

$$r_b^{\mathrm{EUBRL}}(s,a) = (1-P_U(s,a))\, r_b(s,a) + P_U(s,a)\, \mathcal{E}_b(s,a)$$

其中 $\mathcal{E}_b(s,a)$ 是统一的认知不确定性度量，$P_U(s,a)$ 是归一化的不确定性概率。这一设计的直观含义是：当不确定性高时（$P_U$ 大），智能体主要追求认知不确定性本身（即探索）；当不确定性低时（$P_U$ 小），智能体回归任务奖励最大化（即利用）。这种**自适应的探索-利用解耦**使得探索更具原则性，并在理论上能够自适应减小每步遗憾。

本文从理论和实验两个层面验证这一思路的有效性：理论上证明 EUBRL 在无限时域折扣 MDP 上同时取得近 minimax 最优的遗憾界和样本复杂度；实验上在 Chain、Loop、DeepSea、LazyChain 等稀疏/长时程/随机任务上以显著优势超越多种贝叶斯和频率派基线。



## 核心方法与创新机理

### 瓶颈：探索-利用的耦合困境

现有探索策略在稀疏奖励、长时程和随机环境中效率低下的根本原因，在于探索与利用的耦合缺乏原则性机制。乐观主义方法（如 RMAX、BEB）通过人为抬高未知状态的价值驱动探索，但其不确定性量化依赖启发式置信区间，导致不必要的探索和缓慢收敛。贝叶斯方法（如 PSRL）虽能通过后验采样平衡探索，但在深度不确定性下仍缺乏自适应的探索强度调节。核心瓶颈在于：**现有方法未将认知不确定性直接纳入智能体的目标函数，导致探索行为与真实认知状态脱节**。

### 因果调节变量：认知引导奖励

EUBRL 的核心创新在于引入**认知引导奖励函数**，将认知不确定性作为奖励的一部分直接写入 MDP 的目标：

$$r_b^{\mathrm{EUBRL}}(s,a) := \left(1 - P(U = 1 | s,a)\right) r_b(s,a) + P(U = 1 | s,a) \mathcal{E}_b(s,a)$$

其中 $\mathcal{E}_b(s,a)$ 为广义认知不确定性，整合了转移不确定性和奖励不确定性：

$$\mathcal{E}_b(s,a) := h(\mathcal{E}_T(s,a), \mathcal{E}_R(s,a))$$

不确定性概率 $P(U = 1 \mid s,a) = \frac{\mathcal{E}_b(s,a)}{\mathcal{E}_{\max}}$ 实现自适应加权：当认知不确定性高时，内在不确定性奖励主导，驱动探索；当认知不确定性低时，任务奖励主导，侧重利用。这一机制实现了**探索与利用的自动解耦**，无需手工设计探索奖励或启发式调度。

### Changed Slot：奖励函数的本质重构

EUBRL 的关键 changed slot 在于**奖励函数的语义重构**（见 Section 3.2）。传统方法使用固定奖励 $r_b(s,a)$，而 EUBRL 将其替换为上述认知引导奖励。这一替换并非简单的奖励塑形，而是通过概率图模型引入隐变量 $U$（不确定性），将最优性 $O$ 划分为“确定”与“不确定”两种情形（见 Figure 4），从而在推断框架下统一了探索与利用。理论分析表明，该设计引入了**认知抵抗项** $\Re^t(s) := 2 P_U^t(s, \pi_t(s)) + \frac{9}{7} P_U^t(s, \pi^{\star}(s))$，可自适应降低每步遗憾上界（Theorem 1），使得 EUBRL 在无限时域折扣 MDP 上同时取得近 minimax 最优的遗憾界 $\widetilde{\mathcal{O}}\left( \frac{\sqrt{S A T}}{(1-\gamma)^{1.5}} + \frac{S^2 A}{(1-\gamma)^2} \right)$（Theorem 2）和样本复杂度界（Theorem 3）。

### 与基线方法的本质区别

| 方法 | 探索机制 | 不确定性使用方式 | 探索-利用耦合 |
|------|----------|------------------|---------------|
| PSRL | 后验采样 | 隐式，通过采样多样性 | 耦合于采样过程 |
| RMAX/BEB | 乐观初始化/奖励加成 | 启发式置信区间 | 固定加成，无自适应 |
| VBRB | 方差奖励 | 方差作为探索奖励 | 方差与任务奖励线性混合 |
| **EUBRL** | **认知引导** | **认知不确定性直接写入目标函数，概率加权** | **自适应解耦** |

VBRB 虽与 EUBRL 思路相近，但使用方差而非互信息形式的认知不确定性，且缺乏不确定性概率 $P_U$ 的动态调节，导致探索效率不足（消融实验证实互信息比方差更具探索性）。EUBRL 通过 Dirichlet/Normal 先验组合实现认知不确定性的封闭形式计算（Corollary 1），在 Chain、Loop、DeepSea、LazyChain 等任务上以显著优势超越所有基线（Tables 1, 3; Figures 1–3），尤其在随机 DeepSea 上实现了零失败率的完美求解。



![[assets/figures/papers/iclr26_0010_KASqlcI6Nm_EUBRL_Epistemic_Uncertainty_Directed_Bayesian_Re/figures/007_Figure_4.jpg]]
*Figure 4: Comparison between standard RL and our formulation as represented by probabilistic graphical models (PGMs). We introduce the variable of “uncertainty” U, which partitions the optimality O into distinct cases: one is when certain, the other is when uncertain*

EUBRL 的核心 pipeline 由三个紧密耦合的模块构成：**信念更新**、**认知不确定性估计**与**认知引导策略求解**。这些模块在智能体与环境交互的每步循环中协同运作，实现探索与利用的自适应解耦。

### 1. 信念更新模块

每次交互后，智能体接收转移 $(s_t, a_t, r_t, s_{t+1})$，并利用共轭先验在封闭形式下更新后验信念 $b_{t+1}$（Algorithm 1）。具体而言，转移模型采用 Dirichlet 分布，奖励模型采用 Normal‑Gamma 分布（Section 5），两者独立更新，使得信念维护在计算上高效且无需采样近似。

### 2. 认知不确定性估计模块

基于当前信念 $b$，该模块计算状态‑动作对 $(s,a)$ 的**广义认知不确定性**（Section 3.1）：

$$
\mathcal{E}_b(s,a) := h\big(\mathcal{E}_T(s,a),\; \mathcal{E}_R(s,a)\big),\quad h(x,y) = \eta(\sqrt{x} + \sqrt{y})
$$

其中 $\mathcal{E}_T$ 为转移不确定性（以互信息或方差度量），$\mathcal{E}_R$ 为奖励不确定性（经下一状态期望聚合：$\mathcal{E}_R(s,a) := \mathbb{E}_{P_b(s'\mid s,a)}[\mathcal{E}_R(s,a,s')]$，见 Appendix B.1）。缩放因子 $\eta$ 控制不确定性奖励的整体幅度。

### 3. 认知引导策略求解模块

认知不确定性被直接注入智能体的目标函数，形成 **EUBRL 奖励**（Section 3.2）：

$$
r_b^{\mathrm{EUBRL}}(s,a) := \big(1 - P_U(s,a)\big)\, r_b(s,a) + P_U(s,a)\, \mathcal{E}_b(s,a)
$$

其中不确定性概率 $P_U(s,a) = \mathcal{E}_b(s,a) / \mathcal{E}_{\max}$ 将认知不确定性归一化后作为混合权重。当 $P_U$ 高时，智能体倾向于追求内在不确定性奖励（探索）；当 $P_U$ 低时，则侧重任务奖励 $r_b(s,a)$（利用）。

随后，利用值迭代在构造的 MDP $\mathcal{M} = (\mathcal{S}, \mathcal{A}, P_b, r_b^{\mathrm{EUBRL}}, \gamma)$ 上求解最优策略 $\pi_{t+1}$（Algorithm 1）。对于无限时域折扣设定，策略定期更新并重置状态；对于有限时域片段式设定，则按幕更新。

### 输入输出流

- **输入**：当前状态 $s_t$、信念 $b_t$、任务奖励函数 $r$。
- **内部流转**：信念更新 → 认知不确定性计算 → EUBRL 奖励构造 → 策略求解。
- **输出**：动作 $a_t \sim \pi_t(\cdot\mid s_t)$，以及更新后的信念 $b_{t+1}$ 和策略 $\pi_{t+1}$。

### 理论支撑的角色定位

认知不确定性估计与奖励混合机制直接支撑了 **认知抵抗项** $\Re^t(s)$（Theorem 1），该抵抗项自适应地减小每步遗憾上界：

$$
\Re^t(s) := 2P_U^t(s,\pi_t(s)) + \frac{9}{7}P_U^t(s,\pi^\star(s))
$$

当当前动作或最优动作的不确定性概率较高时，$\Re^t(s)$ 增大，从而收紧遗憾界——这正是“认知引导”在理论层面的体现。整个 pipeline 因此实现了从不确定性量化到策略优化的闭环，在稀疏奖励、长时程和随机环境中展现出原则性的探索效率。

> **注意**：上述 pipeline 描述基于表格型表示和精确值迭代求解器。在函数逼近或近似求解器下的扩展，其近似误差如何传播至遗憾界，目前仅有初步分解（Appendix B.3），完整的理论分析仍待完善。



### 3.1 认知不确定性建模

EUBRL 的核心在于将认知不确定性（epistemic uncertainty）显式建模并纳入智能体的目标函数。认知不确定性反映的是由于数据不足导致的对环境动态的不完全认知，与环境的固有随机性（aleatoric uncertainty）有本质区别。

**广义认知不确定性。** 为同时捕捉转移和奖励两个维度的不确定性，EUBRL 采用广义组合形式：

$$\mathcal{E}_b(s,a) := h(\mathcal{E}_T(s,a), \mathcal{E}_R(s,a))$$

其中 $\mathcal{E}_T(s,a)$ 和 $\mathcal{E}_R(s,a)$ 分别为转移和奖励的认知不确定性，组合函数取 $h(x,y) = \eta(\sqrt{x} + \sqrt{y})$，$\eta$ 为缩放因子。转移认知不确定性的一般定义为：

$$\mathcal{E}_T(s,a) = f \circ g(P_b(s' | s,a)) - \mathbb{E}_{\mathbf{w} \sim b(\mathbf{w})} \left[ f \circ g(P(s' | s,a, \mathbf{w})) \right]$$

该式度量的是平均转移分布与各可能转移分布之间的偏差，$f \circ g$ 的选择决定了不确定性的具体形式。在实现中，EUBRL 采用互信息（mutual information）形式，其在 Dirichlet 先验下具有闭式解：

$$\mathbf{M}_b(s,a) = \sum_i \frac{\alpha_i}{\alpha_0}[\psi(\alpha_i+1) - \psi(\alpha_0+1) - \log\frac{\alpha_i}{\alpha_0}]$$

消融实验表明，互信息形式的认知不确定性比方差更具探索性。

**奖励不确定性聚合。** 考虑到奖励建模为 $P(r|s,a,s')$，奖励的认知不确定性需在下一状态上聚合：

$$\mathcal{E}_R(s,a) := \mathbb{E}_{P_b(s' \mid s,a)}[\mathcal{E}_R(s,a,s')]$$

### 3.2 认知引导奖励

EUBRL 的关键创新在于通过概率推断将认知不确定性转化为奖励信号的一部分。引入隐变量 $U$ 表示“不确定状态”，将最优性 $O$ 划分为确定与不确定两种情形（见图 4 的概率图模型对比）。

**不确定性概率。** 将认知不确定性归一化为概率：

$$P(U = 1 \mid s,a) = \frac{\mathcal{E}_b(s,a)}{\mathcal{E}_{\max}}$$

**EUBRL 奖励函数。** 以不确定性概率为权重，动态混合任务奖励与内在不确定性奖励：

$$r_b^{\mathrm{EUBRL}}(s,a) := \left(1 - P(U = 1 | s,a)\right) r_b(s,a) + P(U = 1 | s,a) \mathcal{E}_b(s,a)$$

这一设计的因果机制在于：当认知不确定性高时，$P_U$ 接近 1，智能体主要受内在不确定性驱动进行探索；随着数据积累、不确定性降低，$P_U$ 趋近 0，智能体逐渐回归任务奖励驱动的利用。由此实现探索与利用的自适应解耦。

### 3.3 算法流程

EUBRL 的整体流程由三个核心模块构成（见 Algorithm 1）：

1. **信念更新 (Belief Update)**：每次交互后，利用 Dirichlet（转移）和 Normal-Gamma（奖励）共轭先验在封闭形式下更新后验信念 $b_{t+1}$。
2. **策略求解 (Solve MDP)**：构造带认知引导奖励的 MDP $\mathcal{M} = (S, A, P_b, r_b^{\mathrm{EUBRL}}, \gamma)$，利用值迭代求解最优策略 $\pi_{t+1}$。
3. **重置/策略更新 (Reset/Policy Update)**：根据无限期折扣或有限期片段式设定，定时重置状态或更新策略。

### 4.1 每步遗憾分解与认知抵抗

理论分析的核心是将每步遗憾 $\Delta_t := V^{\star}(s_t) - V^{\pi_t}(s_t)$ 分解为三项：

$$V^{\star}(s) - V^{\pi_t}(s) = \underbrace{V^{\star}(s) - \widetilde{V}^t(s)}_{\text{准乐观}} + \underbrace{\widetilde{V}^t(s) - V^t(s)}_{\text{复杂度}} + \underbrace{V^t(s) - V^{\pi_t}}_{\text{准确度}}$$

其中 $\widetilde{V}^t$ 为 EUBRL 奖励下的值函数，$V^t$ 为真实奖励下的值函数。

**认知抵抗。** 定义认知抵抗项（epistemic resistance）：

$$\Re^t(s) := 2 P_U^t(s, \pi_t(s)) + \frac{9}{7} P_U^t(s, \pi^{\star}(s))$$

该量加权了当前策略动作与最优策略动作的不确定性概率，体现认知引导对遗憾的自适应削减。

**Theorem 1（每步遗憾上界）** 给出无限时域折扣 MDP 下的高概率界：

$$V^{\star}(s) - V^{\pi_t}(s) \leq \left(\frac{9}{2} - \Re^t(s)\right) \lambda_t V_{\gamma}^{\uparrow} + 2 J_{\gamma}^t(s) + \mathcal{O}\left(\Phi_t \left(1 + \frac{\Phi_t}{V_{\gamma}^{\uparrow}}\right)\right)$$

其中 $\lambda_t$ 为 Freedman 不等式导出的辅助序列，$\Re^t(s)$ 显式地减小上界——当认知不确定性高时，$\Re^t(s)$ 增大，上界收紧，反映探索带来的信息增益。

### 4.2 频率派遗憾与样本复杂度

将上述每步界累积，得到频率派意义上的全局保证。

**Theorem 2（遗憾上界）** 在无限时域折扣 MDP 下，以高概率成立：

$$\mathrm{Regret}(T) \leq \widetilde{\mathcal{O}}\left( \frac{\sqrt{S A T}}{(1-\gamma)^{1.5}} + \frac{S^2 A}{(1-\gamma)^2} \right)$$

**Theorem 3（样本复杂度上界）** 达到 $\epsilon$ 最优策略所需步数：

$$\widetilde{\mathcal{O}}\left( \left( \frac{S A}{\epsilon^2 (1-\gamma)^3} + \frac{S^2 A}{\epsilon (1-\gamma)^2} \right) \log \frac{1}{\delta} \right) \text{ steps}$$

两者均与已知下界匹配，达到近 minimax 最优。当先验为均匀且有界时（如 Dirichlet + Normal 组合），EUBRL 实例化后直接满足该最优性（Corollary 1）。需注意，若使用 Normal-Gamma 先验且环境（近）确定性，认知不确定性可能不足以保证准乐观性，导致理论退化（Proposition 1 所指）。



## 实验与关键发现

### 核心实验设置

EUBRL 在四个具有代表性的稀疏奖励/长时程环境上进行评估：Chain（5 状态随机任务）、Loop（多环路结构）、DeepSea（$N \times N$ 网格）和 LazyChain（$2N+1$ 状态链）。所有环境均包含确定性和随机性两种变体（Table 2）。对比基线涵盖贝叶斯方法（PSRL、BOSS、BEETLE、Mean‑MDP、BEB、VBRB）和频率派方法（RMAX、MBIE‑EB）。实验结果在 20 或 500 个随机种子上平均，超参数（Dirichlet $\alpha$、Normal‑Gamma $\beta_0$）经过网格搜索。

### 主结果

**Chain 环境**（Table 1）：EUBRL 取得最高平均回报 3473（标准误差 16），略优于 VBRB（3465）和 MBIE‑EB（3462），显著超越 BEETLE（1754）。该环境奖励稀疏且转移随机，EUBRL 的低方差表现表明认知引导在随机性下能稳定聚焦高价值区域。

![[assets/figures/papers/iclr26_0010_KASqlcI6Nm_EUBRL_Epistemic_Uncertainty_Directed_Bayesian_Re/figures/001_Table_1.jpg]]
*Table 1: Results on Chain environment. The average return and standard error are computed across 500 random seeds, with each run consisting of 1000 steps*

**Loop 环境**（Table 3, Figure 1）：在 2 环路设定下，EUBRL 平均回报 395，与 RMAX（394）接近，优于 BEB（386）和 Mean‑MDP（342）。随着环路数增加（Figure 1），任务稀疏度和结构难度上升，EUBRL 的可扩展性优于 RMAX——环路数越多，EUBRL 的相对优势越明显。这验证了认知不确定性在长时程依赖下的有效探索能力。

![[assets/figures/papers/iclr26_0010_KASqlcI6Nm_EUBRL_Epistemic_Uncertainty_Directed_Bayesian_Re/figures/003_Table_3.jpg]]
*Table 3: Results on Loop environment of 2 Loops. The average return and standard error are computed across 500 random seeds, with each run consisting of 1000 steps*

![[assets/figures/papers/iclr26_0010_KASqlcI6Nm_EUBRL_Epistemic_Uncertainty_Directed_Bayesian_Re/figures/004_Figure_1.jpg]]
*Figure 1: Scaling of number of loops, leading to more sparsity and structural difficulty. Averaged over 500 random seeds*

**DeepSea 环境**（Figure 2）：EUBRL+（使用互信息形式认知不确定性）在随机变体上**完美求解，零失败**，而其他方法随网格尺寸 $N$ 增大成功率骤降。在确定性变体上，EUBRL 的成功率和平均解算幕数同样一致领先。该结果直接支撑认知不确定性（特别是互信息形式）比方差更具探索性的消融发现。

![[assets/figures/papers/iclr26_0010_KASqlcI6Nm_EUBRL_Epistemic_Uncertainty_Directed_Bayesian_Re/figures/005_Figure_2.jpg]]
*Figure 2: Success rate and average episodes to solve task, reported for both deterministic and stochastic variants over different problem sizes ( S = N $\times$ N ) . Averaged over 20 random seeds*

**LazyChain 环境**（Figure 3）：EUBRL 在确定性和随机性两种变体上，成功率和平均解算步数均一致优于其他贝叶斯和频率派方法。LazyChain 的特点是 agent 需抵抗“懒惰”动作的诱惑以到达远端高奖励状态，认知引导在此类延迟奖励场景下展现出原则性优势。

![[assets/figures/papers/iclr26_0010_KASqlcI6Nm_EUBRL_Epistemic_Uncertainty_Directed_Bayesian_Re/figures/006_Figure_3.jpg]]
*Figure 3: Success rate and average steps to solve task, reported for both deterministic and stochastic variants over different problem sizes (S = 2N + 1). Averaged over 20 random seeds*

### 消融与关键发现

**互信息 vs 方差**：实验发现，基于互信息的认知不确定性比基于方差的度量更具探索性（Section 5）。这一差异在 DeepSea 随机变体上尤为显著——互信息形式的 EUBRL+ 完美求解，而方差形式可能探索不足。

**先验选择的影响**：理论分析（Corollary 1, Proposition 1）和实验共同表明，Dirichlet + Normal 先验组合使 EUBRL 达到近 minimax 最优。若使用 Normal‑Gamma 先验，在（近）确定性 MDP 中认知不确定性可能不足以保证准乐观性，导致理论退化。这一发现对实际部署中的先验选择具有指导意义。

**认知抵抗的实证体现**：理论上的认知抵抗项 $\Re^t(s)$（当前策略与最优策略动作的不确定性概率加权和）在实验中表现为：当 agent 对环境充分确定时，EUBRL 自动降低探索强度、侧重利用；当遇到陌生状态-动作对时，认知不确定性升高，驱动定向探索。这种自适应解耦是 EUBRL 在稀疏奖励任务上样本效率优势的核心机制。

### 失败模式与局限

1. **先验错误指定**：当先验分布与真实环境严重不匹配时，EUBRL 可能陷入次优策略。两臂 Bandit 反例表明，错误的先验会导致认知不确定性估计失真，使 agent 过早放弃有潜力的动作。

2. **Normal‑Gamma 先验退化**：在确定性或近确定性环境中，Normal‑Gamma 先验产生的认知不确定性可能过小，不足以维持准乐观性，导致探索不足。

3. **表格型表示限制**：当前认知不确定性估计依赖表格型表示，扩展到函数逼近（深度网络）时，如何构建校准良好的不确定性估计仍是开放问题。

4. **超参数敏感性**：缩放因子 $\eta$ 和先验参数对性能影响显著，目前依赖网格搜索，缺乏自动化选择机制。

### 理论-实验一致性

实验趋势与理论界高度一致：Theorem 2 和 Theorem 3 证明 EUBRL 在无限时域折扣 MDP 上取得近 minimax 最优的 $\widetilde{\mathcal{O}}(\sqrt{SAT}/(1-\gamma)^{1.5} + S^2A/(1-\gamma)^2)$ 遗憾界和样本复杂度界。实验中的样本效率优势（尤其在 DeepSea 和 LazyChain 上随规模增大而扩大的差距）为上述理论提供了实证支撑。Theorem 1 中认知抵抗项 $\Re^t(s)$ 自适应减小每步遗憾的机制，在实验中体现为 EUBRL 在探索-利用切换上的平滑性和低方差特性。



## 定位与知识库关联

### 与基线方法的关系

EUBRL 的核心创新在于将认知不确定性直接植入智能体的奖励目标，而非仅作为外部探索奖励或置信区间。这一设计使其与现有方法在探索机制上形成本质差异。

**乐观主义谱系**：RMAX、MBIE-EB、BEB 等方法通过向未知状态-动作对注入乐观奖励来驱动探索。EUBRL 的认知引导奖励在形式上类似，但关键区别在于其自适应混合机制：当认知不确定性高时，$P_U$ 接近 1，奖励退化为纯粹的认知不确定性项 $\mathcal{E}_b(s,a)$；当不确定性消退时，$P_U$ 接近 0，奖励回归任务奖励 $r_b(s,a)$。这种"软切换"避免了乐观主义方法中硬编码的探索奖励衰减问题。实验证据表明，在 Chain 环境上 EUBRL 的平均回报（3473）略高于基于方差的 VBRB（3465）和基于置信区间的 MBIE-EB（3462），差距虽小但统计显著（500 随机种子）。在 Loop 环境上，EUBRL（395）同样以微弱优势超越 RMAX（394）。

**贝叶斯后验采样谱系**：PSRL 和 BOSS 通过从后验中采样 MDP 来自然平衡探索与利用，但其探索行为受先验和后验耦合的隐性控制，缺乏显式的认知引导信号。EUBRL 则通过概率图形模型显式引入不确定性变量 $U$，将认知状态作为可观测信号纳入决策。这种显式建模使得探索行为更具可解释性：不确定性概率 $P_U$ 直接量化了智能体对当前状态-动作对的"无知程度"。

**贝叶斯自适应 MDP 谱系**：BEETLE 追求贝叶斯最优解，但计算代价随状态空间指数增长。Mean-MDP 则完全放弃探索，仅使用后验均值进行规划。EUBRL 位于两者之间：通过认知引导奖励的巧妙构造，以接近 Mean-MDP 的计算代价获得了接近贝叶斯最优的探索效率。在 Chain 环境上，BEETLE 的平均回报仅为 1754，远低于 EUBRL 的 3473，这印证了精确贝叶斯自适应方法在表格型稀疏奖励任务上的计算瓶颈。

### 适用边界与先验敏感性

EUBRL 的理论保证和实证性能依赖于先验的合理指定。分析揭示了以下适用条件：

**先验充分性要求**：Theorem 4 和 Corollary 1 表明，当先验 $b_0$ 属于"充分表达类"（包含均匀且有界先验）时，EUBRL 可达到近 minimax 最优的遗憾和样本复杂度。具体而言，Dirichlet 先验（用于转移）与 Normal 先验（用于奖励）的组合满足这一条件。然而，当使用 Normal-Gamma 先验时，若环境接近确定性，认知不确定性可能不足以维持准乐观性，导致理论退化。这一发现具有实际指导意义：在已知环境具有显著随机性的场景下，Dirichlet/Normal 组合是安全选择；而在高度确定性的环境中，需谨慎评估 Normal-Gamma 先验的适用性。

**先验错误指定的脆弱性**：两臂 Bandit 反例表明，当先验与真实环境严重不匹配时，EUBRL 可能陷入次优策略。这是贝叶斯方法的共性局限，但 EUBRL 的认知引导机制放大了这一风险——错误先验下的认知不确定性估计会系统性偏差，进而误导探索方向。该问题目前缺乏自动化检测和修正机制。

**超参数敏感性**：缩放因子 $\eta$ 控制认知不确定性在奖励中的绝对尺度，直接影响 $P_U$ 的饱和速度。论文通过网格搜索确定 $\eta$，但未提供自适应调节方案。在实际部署中，$\eta$ 的选择可能因任务稀疏性和时程长度而异，需要手动调参。

### 局限性与开放问题

**表格型表示的扩展瓶颈**：当前 EUBRL 的认知不确定性估计依赖于 Dirichlet 分布的闭式互信息公式或方差公式，这要求对每个状态-动作对维护独立的计数统计。在连续状态空间或大规模离散空间中，这种表格型表示不可行。虽然论文讨论了函数逼近下的误差分解框架，将近似误差作为遗憾的附加项，但尚未给出可操作的深度网络实现方案。如何构建校准良好的认知不确定性估计器（如基于贝叶斯神经网络的互信息近似）仍是开放问题。

**认知不确定性度量的通用性**：当前 $\mathcal{E}_b(s,a)$ 采用 $h(x,y) = \eta(\sqrt{x} + \sqrt{y})$ 的特定组合形式，并通过互信息或方差实例化。消融分析表明互信息比方差更具探索性，但这是否为最优选择尚不清楚。是否存在无需手工设计 $h$ 函数的更通用认知不确定性度量——例如直接从贝叶斯遗憾中推导出的内在奖励——是值得探索的方向。

**近似求解器的理论缺口**：论文在 Appendix B.3 中给出了近似求解器下的遗憾分解，将近似误差 $V^{\pi_t}(s) - V^{\hat{\pi}_t}(s)$ 作为附加项。然而，该分解未给出近似误差与认知不确定性之间的联合界。在实际中，当认知不确定性较高时，值函数估计本身可能更不准确，近似误差与认知不确定性存在耦合。完整的近似理论分析仍待完善。

**多层级认知不确定性的建模**：当前框架将转移不确定性和奖励不确定性通过单一函数 $h$ 聚合为标量。在复杂环境中，不同来源的不确定性可能具有不同的时间尺度和结构特性。如何在多层级（如状态抽象、选项、子目标）上捕获和利用认知不确定性，以最小化手工设计奖励的需求，是更具雄心的研究方向。



## 原文 PDF

![[paperPDFs/ICLR_2026/EUBRL_Epistemic_Uncertainty_Directed_Bayesian_Reinforcement_Learning.pdf]]
