---
title: "Relative Value Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Relative_Value_Learning.pdf
project_link: null
code_link: https://github.com/Hauf3n/relative-value-learning
openreview_forum_id: ulTRUwrzt9
aliases:
- RVLR
- RVL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "直接学习状态间的反称值差 Δ(s_i, s_j)=V(s_i)−V(s_j)，以消除绝对价值中的任意常值偏移，从根本上匹配控制问题仅依赖相对差异的不变性。"
primary_logic: "使用反称函数逼近成对值差，将值学习目标从绝对尺度转移到差异空间，天然移除值函数的规范自由度，并与策略梯度基线需求对齐；同时从成对差异重构广义优势估计（R-GAE）仍保持无偏性。"
claims:
- "定理3.1证明成对贝尔曼算子T_π在反称函数空间上为γ-收缩，且唯一不动点等于真实值差。"
- "引理3.2给出R-GAE与标准GAE的关系：Ã_t = A_t + B_t，且推论3.3证明基于R-GAE的策略梯度无偏。"
- "PPO+RV在49个Atari游戏中30个超过PPO，37个超过DAE，并在聚合中位数/IQM/均值上达到更优性能。"
- "Atari 49 games (40M frames) 上 最终平均得分 (mean final score over last 100 episodes) = PPO+RV 在 30/49 游戏中超过 PPO，37/49 游戏中超过 DAE"
---

# Relative Value Learning

> [!tip] 核心洞察
> 使用反称函数逼近成对值差，将值学习目标从绝对尺度转移到差异空间，天然移除值函数的规范自由度，并与策略梯度基线需求对齐；同时从成对差异重构广义优势估计（R-GAE）仍保持无偏性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 相对价值学习 |
| 英文题名 | Relative Value Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ulTRUwrzt9) · [GitHub](https://github.com/Hauf3n/relative-value-learning) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Relative Value Learning (RV) |
| Dataset | Atari 49 games (40M frames), Atari 40M frames (selected game: VideoPinball) |

> [!tip] 效果简介
> - Atari 49 games (40M frames) 上，最终平均得分 (mean final score over last 100 episodes) 为 PPO+RV 在 30/49 游戏中超过 PPO，37/49 游戏中超过 DAE，对比 PPO, DAE，变化 30 vs. 19 (PPO); 37 vs. 12 (DAE)。
> - Atari 49 games (40M frames) 上，Human Normalized Score 聚合指标 (median, IQM, mean, optimality gap) 为 PPO+RV 取得最高中位数、IQM 和均值，以及最低的最优性差距，对比 PPO, DAE，变化 中位数约 0.95 vs. PPO 0.88；最优性差距约 0.44 vs. PPO 0.55。
> - Atari 40M frames (selected game: VideoPinball) 上，最终平均得分 为 138564.8 ± 89747.6，对比 PPO: 37389.0 ± 21539.2; DAE: 23958.8 ± 10071.8，变化 +101175.8 over PPO。

## 概要

标准强化学习中的价值函数估计存在一个根本性问题：绝对状态值 $V(s)$ 包含一个与决策无关的任意常值偏移（gauge freedom）。这一规范自由度在训练中表现为值函数的漂移和不稳定，在隐式反馈或偏好式强化学习等绝对尺度模糊的场景下，更会导致不适定问题。核心症结在于，策略优化实际依赖的只是状态间的**相对差异**，而非绝对尺度。

针对上述瓶颈，本文提出**相对价值学习（Relative Value Learning, RV）**：直接学习一个反称函数 $\Delta_\theta(s_i, s_j) = -\Delta_\theta(s_j, s_i)$ 来逼近真实值差 $V^\pi(s_i) - V^\pi(s_j)$，从根本上消除绝对价值中的任意偏移。该方法将值学习目标从绝对尺度转移到差异空间，天然移除规范自由度，并与策略梯度的基线需求对齐。

理论层面，论文形式化了成对贝尔曼算子 $T_\pi$，并证明其在反称函数空间上为 $\gamma$-收缩，唯一不动点等于真实值差（Theorem 3.1）。基于此，从成对差值沿轨迹伸缩构造相对状态值，进而定义相对广义优势估计（R-GAE）。引理 3.2 揭示 R-GAE 与标准 GAE 仅相差一个轨迹常数基线 $B_t$，推论 3.3 证明基于 R-GAE 的策略梯度仍保持无偏性。

实验层面，将 RV 作为 PPO 的即插即用 critic 在 Atari 49 游戏（40M 帧）上评估。PPO+RV 在 30/49 游戏中超过 PPO，37/49 游戏中超过直接学习优势函数的 DAE 基线；在 Human Normalized Score 的聚合指标上取得最高的中位数、IQM 和均值，以及最低的最优性差距（Figure 3）。典型案例如 VideoPinball，PPO+RV 的最终平均得分达 138564.8，较 PPO 提升约 101175.8 分。

消融实验表明，偏移初始化策略通过轨迹排序减小 $|C|$，有效抑制 R-GAE 方差膨胀（方差与 $C^2$ 成正比），多数游戏中优于零初始化（Figure 4）；配对采样策略中，随机配对通常优于强偏向同幕采样（$p \ge 0.66$）（Table 4）。

当前验证限于离散动作的 Atari 环境，相对价值学习在连续控制、离线强化学习及偏好式学习等场景的有效性仍有待进一步探索。



强化学习中，状态价值函数 $V^\pi(s)$ 是策略评估与优化的核心量，其定义为从状态 $s$ 出发、遵循策略 $\pi$ 的期望折扣回报：

$$V^{\pi}(s) := \mathbb{E}_{\pi, P} \Big[ \sum_{t=0}^{\infty} \gamma^t r(s_t, a_t) \Big| s_0 = s \Big]$$

标准方法通过贝尔曼方程迭代估计 $V^\pi(s)$：

$$V^{\pi}(s) = r_{\pi}(s) + \gamma \mathbb{E}_{s' \sim P^{\pi}(\cdot \vert s)} \big[ V^{\pi}(s') \big]$$

然而，这一绝对价值估计范式存在一个根本性问题：**绝对价值函数引入了与决策无关的偏移自由度（gauge freedom）**。具体而言，控制问题的决策仅依赖于状态间的相对价值差异，而非绝对尺度——例如，在 $Q$-learning 中，动作选择由 $\arg\max_a Q(s,a)$ 决定，该操作对价值函数的任意常值平移不敏感。但绝对价值学习必须额外学习这个偏移量，导致训练中的不稳定与漂移。在隐式反馈或偏好式强化学习等绝对尺度模糊的场景下，这一问题尤为严重，甚至使学习目标变得不适定。

现有方法对此问题的处理存在局限。标准 PPO 使用绝对价值函数 $V(s)$ 进行值估计和广义优势估计（GAE），无法消除规范自由度带来的噪声。Direct Advantage Estimation (DAE) 虽直接学习优势函数，跳过了绝对价值估计，但其架构设计未能系统性地利用成对值差的数学结构。

本文的**核心动机**在于：**直接学习状态间的反称值差 $\Delta(s_i, s_j) = V(s_i) - V(s_j)$，从根本上消除绝对价值中的任意常值偏移**。这一思路将值学习的目标从绝对尺度转移到差异空间，天然移除值函数的规范自由度，并与策略梯度中仅依赖相对优势的需求对齐。如图 Figure 1 所示，相对价值学习（左）直接建模状态间的价值差异以支持决策，而绝对价值学习（右）则孤立地估计每个状态的价值后再进行决策——前者在概念上更贴近控制问题的本质不变性。

为实现这一目标，本文需要解决三个关键技术挑战：一是如何在反称函数空间上定义收敛的学习算子；二是如何从成对值差重构无偏的策略梯度估计；三是如何在多轨迹训练中处理相对价值的初始化与方差控制问题。



## 核心方法与创新机理

### 瓶颈洞察：绝对价值函数的规范自由度

标准强化学习中的价值函数 $V^\pi(s)$ 定义为从状态 $s$ 出发的期望折扣回报。然而，这个定义隐含了一个与决策无关的自由度——**规范自由度（gauge freedom）**：对同一策略 $\pi$ 下的所有状态值同时加上任意常数 $c$，虽然改变了绝对价值，但状态间的相对差异 $V^\pi(s_i) - V^\pi(s_j)$ 保持不变。由于策略梯度与优势函数 $A(s, a) = Q(s, a) - V(s)$ 仅依赖于值的相对差异，绝对尺度上的偏移对控制问题而言是冗余的。

这一冗余在两类场景下变成实际瓶颈：

1. **训练不稳定与漂移**：绝对价值函数逼近器在拟合 $V(s)$ 时，需要额外“学习”一个与决策无关的全局偏移量。这个偏移量没有来自奖励信号的约束，导致训练中出现慢速漂移和收敛不稳定。
2. **隐式反馈下的不适定性**：在基于偏好的强化学习或仅提供相对反馈（如“轨迹 A 优于轨迹 B”）的场景中，绝对价值尺度本身不可识别，学习 $V(s)$ 成为不适定问题。

### 核心机制：从绝对尺度迁移到差异空间

**Relative Value Learning (RV)** 的核心思想是直接学习状态间的**成对值差**，而非绝对状态值。具体而言，引入一个反称函数：

$$\Delta_{\theta} : \mathcal{S} \times \mathcal{S} \to \mathbb{R}, \quad \Delta_{\theta}(s_i, s_j) = -\Delta_{\theta}(s_j, s_i)$$

该函数逼近真实值差 $\Delta^\pi(s_i, s_j) = V^\pi(s_i) - V^\pi(s_j)$。通过直接建模差异，天然移除了绝对价值中的任意常值偏移——因为对于任意常数 $c$，有 $\Delta^\pi(s_i, s_j) = (V^\pi(s_i) + c) - (V^\pi(s_j) + c)$，即差异空间对规范自由度具有不变性。

这一迁移由以下理论保证支撑：

- **成对贝尔曼算子与收缩性**（Theorem 3.1）：定义在反称函数空间上的算子 $T_\pi$ 满足 $\|T_\pi \Delta_1 - T_\pi \Delta_2\|_\infty \leq \gamma \|\Delta_1 - \Delta_2\|_\infty$，即以 $\gamma$ 为因子的收缩映射。其唯一不动点等于真实值差 $\Delta^\pi$，从而保证了迭代学习的收敛性和目标的良定性。

- **成对值差恒等式**（Equation 5）：值差满足递归关系：
  $$\Delta^\pi(s_i, s_j) = r_\pi(s_i) - r_\pi(s_j) + \gamma \mathbb{E}_{s_i'\sim P^\pi(\cdot|s_i), s_j'\sim P^\pi(\cdot|s_j)} \left[ \Delta^\pi(s_i', s_j') \right]$$
  该恒等式仅依赖可观测的奖励差和成对后继采样，无需绝对价值锚点，为自举式学习提供了闭合目标。

### 关键设计变更（Changed Slots）

RV 相对于标准 PPO 基线改变了两个核心组件：

| 组件 | 基线（PPO） | RV 方案 | 证据锚点 |
|------|------------|---------|----------|
| **价值估计目标** | 绝对状态值 $V(s)$ | 反称值差函数 $\Delta(s_i, s_j)$ | Equation (1) |
| **优势估计** | GAE 基于绝对价值 $V$ 和 TD 残差 $\delta$ | R-GAE 基于相对价值 $\tilde{V}$ 和相对 TD 残差 $\tilde{\delta}$，与标准 GAE 相差轨迹常数基线 $B_t$ | Lemma 3.2; Equation (9)–(11) |

**R-GAE 的无偏性**（Corollary 3.3）：尽管 R-GAE 与标准 GAE 相差一个轨迹常数基线 $B_t$，但基于 R-GAE 的策略梯度估计保持无偏：
$$\mathbb{E}_t\left[\nabla_\phi \log \pi_\phi(a_t|s_t) \tilde{A}_t\right] = \mathbb{E}_t\left[\nabla_\phi \log \pi_\phi(a_t|s_t) A_t\right]$$
这意味着 RV 作为 PPO 的 drop-in critic 替换时，不影响策略梯度的期望方向，仅改变了方差特性。

### 方差控制：轨迹排序初始化

R-GAE 的无偏性代价是引入了与轨迹初始化偏移 $C$ 平方成正比的方差膨胀项（Lemma C.1）：
$$\text{Var}(g_{\text{rel}}) = \text{Var}(g_{\text{std}}) + \mathbb{E}[\|\nabla_\phi \log \pi_\phi\|^2 B_t^2] + 2\mathbb{E}[A_t B_t \|\nabla_\phi \log \pi_\phi\|^2]$$
其中 $B_t$ 随 $|C|$ 增大而上升（Figure 5 实证验证了 $B_t$ 在轨迹初期较大、随后衰减的模式）。为控制这一方差，RV 引入**轨迹排序（Trajectory Ranking）** 策略：当训练批次包含多条轨迹时，通过成对差值对轨迹的相对价值进行全局排序并注入适当偏移，最小化 $|C|$，从而将 $B_t$ 压缩至接近零。

### 架构实现

反称性通过一个简洁的神经网络头实现：$\Delta_\theta(s_i, s_j) = \Phi(f_{\text{enc}}(s_i) - f_{\text{enc}}(s_j))$，其中 $\Phi$ 为无偏置的线性投影 $w \in \mathbb{R}^d$。该设计天然保证 $\Delta_\theta(s_i, s_j) = -\Delta_\theta(s_j, s_i)$ 且 $\Delta_\theta(s_i, s_i) = 0$，无需额外约束。

> **注意**：RV 目前仅在离散动作的 Atari 环境下验证，其在连续控制、离线强化学习及偏好式学习中的有效性仍属开放问题。



![[assets/figures/papers/iclr26_0009_ulTRUwrzt9_Relative_Value_Learning/figures/001_Figure_1.jpg]]
*Figure 1: Relative Value vs. Absolute Value Learning.. RV (left) learns value differences between states for decision making while AV (right) learns the value for each state in isolation and then decides for the best decision (e.g. by taking maximum in Q-learning)*

![[assets/figures/papers/iclr26_0009_ulTRUwrzt9_Relative_Value_Learning/figures/005_Figure_2.jpg]]
*Figure 2: Trajectory Ranking. When training batches contain samples from more than one episode, the initialization $\tilde { V } ( s _ { 0 }$ ) = 0 for each trajectory τi is not correct. The trajectories need to be ranked relative to each other by adding an offset that is calculated with $\Delta ( s _ { i } , \bar { s _ { j } }$ ) . Note that $s _ { 0 } , s _ { 0 } , s _ { 0 }$ are start states of $\tau _ { 1 } , \tau _ { 2 } , \tau _ { 3 }$ indicated by color. For simplicity, assume in this figure that start states are only present at t = 0 for each rollout, so we can think about each τ as one episode

**相对价值学习（Relative Value Learning, RV）** 的核心思路是将价值估计的目标从绝对状态值 $V(s)$ 转移到状态间的**反称值差** $\Delta(s_i, s_j) = V(s_i) - V(s_j)$ 上。这一转移从根本上消除了绝对价值函数中与决策无关的任意常值偏移（gauge freedom），使学习目标与策略优化真正依赖的**相对差异**对齐。

### 整体 Pipeline

RV 作为 on-policy actor-critic 框架中的 **critic 替代模块**，其整体数据流如下：

1. **状态编码**：对任意两个状态 $s_i, s_j$，共享的编码器 $f_{\text{enc}}$ 提取特征表示。
2. **反称差值头**：将两状态编码的差值通过无偏置线性投影 $\Phi$ 输出成对值差：
   $$\Delta_{\theta}(s_i, s_j) = \Phi\big(f_{\text{enc}}(s_i) - f_{\text{enc}}(s_j)\big)$$
   使用单一可学习向量 $w \in \mathbb{R}^d$ 且不含偏置项，天然保证反称性 $\Delta_{\theta}(s_i, s_j) = -\Delta_{\theta}(s_j, s_i)$ 和零自身差 $\Delta_{\theta}(s_i, s_i) = 0$。
3. **相对价值构造**：沿轨迹将成对差值伸缩求和，构造相对状态值，首状态锚定为零：
   $$\tilde{V}_{\theta}(s_0) := 0, \quad \tilde{V}_{\theta}(s_t) := \sum_{k=0}^{t-1} \Delta_{\theta}(s_{k+1}, s_k) \quad (t \geq 1)$$
4. **相对 TD 残差与 R-GAE**：基于相对价值计算时序差分误差 $\tilde{\delta}_t$，进而构造相对广义优势估计 $\tilde{A}_t$。引理 3.2 证明 $\tilde{A}_t = A_t + B_t$，其中 $B_t$ 为仅依赖轨迹初始化偏移的常数基线，推论 3.3 进一步证明基于 R-GAE 的策略梯度**无偏**。
5. **成对值差目标计算**：针对成对采样 $(s_i, s_j)$，提供 1 步、n 步和 λ-回报三种引导目标，仅使用可观测奖励与非终止后继的成对差值，处理终端状态时通过分情况公式保证目标适定性。
6. **轨迹排序初始化**：当训练批次包含多条轨迹时，对轨迹的相对价值进行全局排序并注入偏移，以最小化轨迹常数基线 $B_t$ 带来的方差膨胀（Lemma C.1 表明方差含与初始化偏移 $C^2$ 成正比的噪声项）。

### 模块关系

| 模块 | 输入 | 输出 | 关键属性 |
|------|------|------|----------|
| 状态编码器 $f_{\text{enc}}$ | 原始状态 $s$ | 特征向量 | 与 PPO 共享骨干网络 |
| 反称差值头 $\Phi$ | $f_{\text{enc}}(s_i) - f_{\text{enc}}(s_j)$ | $\Delta_{\theta}(s_i, s_j)$ | 无偏置线性投影，天然反称 |
| 相对价值构造 | 沿轨迹的 $\Delta_{\theta}$ 序列 | $\tilde{V}_{\theta}(s_t)$ | 伸缩求和，$s_0$ 锚定为零 |
| R-GAE 估计器 | $\tilde{V}_{\theta}$ 与即时奖励 | $\tilde{A}_t$ | 等价于 GAE + 轨迹常数基线 |
| 成对目标计算 | 奖励序列与 $\Delta_{\theta}$ | $y_{ij}^{(1)}, y_{ij}^{(n)}, y_{ij}^{(\lambda)}$ | 处理终端状态分情况 |
| 轨迹排序 | 多轨迹的 $\Delta_{\theta}$ | 偏移注入后的 $\tilde{V}$ | 控制 $|C|$ 以减小方差 |

### 理论保证

- **收缩性**：定理 3.1 证明成对贝尔曼算子 $\mathcal{T}_{\pi}$ 在反称函数空间上为 $\gamma$-收缩，唯一不动点等于真实值差 $\Delta^{\pi}$。
- **无偏性**：推论 3.3 保证基于 R-GAE 的策略梯度估计与标准 GAE 策略梯度期望一致。

> **注意**：R-GAE 引入的轨迹常数基线 $B_t$ 虽不破坏无偏性，但其平方项会膨胀策略梯度方差。轨迹排序策略通过最小化初始化偏移 $|C|$ 来抑制该方差项，这是 RV 实现中关键的工程决策。



### 反称差值函数

核心建模对象是状态对上的反称函数，直接逼近真实值差：

$$
\Delta_{\theta} : \mathcal{S} \times \mathcal{S} \to \mathbb{R}, \qquad \Delta_{\theta}(s_i, s_j) = -\Delta_{\theta}(s_j, s_i)
$$

该函数天然满足 $\Delta_{\theta}(s_i, s_i) = 0$，消除了绝对价值估计中与决策无关的常值偏移自由度。实现上，通过共享编码器提取状态特征后取差，再经无偏置线性投影输出标量：

$$
\Delta_{\theta}(s_i, s_j) = \Phi\big(f_{\mathrm{enc}}(s_i) - f_{\mathrm{enc}}(s_j)\big)
$$

其中 $\Phi$ 为单个可学习向量 $w \in \mathbb{R}^d$ 且不含偏置项，从结构上保证反称性。

### 成对贝尔曼算子

真实值差满足如下递归恒等式（基于两状态独立后继采样）：

$$
\Delta^{\pi}(s_i, s_j) = r_{\pi}(s_i) - r_{\pi}(s_j) + \gamma \, \mathbb{E}_{s_i' \sim P^{\pi}(\cdot \mid s_i),\, s_j' \sim P^{\pi}(\cdot \mid s_j)} \big[ \Delta^{\pi}(s_i', s_j') \big]
$$

据此定义成对贝尔曼算子：

$$
(T_{\pi} \Delta)(s_i, s_j) := \Delta r^{\pi}(s_i, s_j) + \gamma \, (\widehat{\mathcal{P}}_{\pi} \Delta)(s_i, s_j)
$$

**定理 3.1** 证明该算子在反称函数空间上为 $\gamma$-收缩，唯一不动点等于真实值差，为相对价值学习提供了理论收敛保证。

### 相对价值构造与 R-GAE

沿轨迹将成对差值 telescoping 求和，构造相对状态值（首状态锚定为零）：

$$
\tilde{V}_{\theta}(s_0) := 0, \quad \tilde{V}_{\theta}(s_t) := \sum_{k=0}^{t-1} \Delta_{\theta}(s_{k+1}, s_k) \quad (t \geq 1)
$$

基于相对价值定义相对 TD 残差：

$$
\tilde{\delta}_t := r_t + \gamma \tilde{V}_{\theta}(s_{t+1}) - \tilde{V}_{\theta}(s_t)
$$

进而构造相对广义优势估计 (R-GAE)：

$$
\tilde{A}_t := \sum_{l=0}^{T-t} (\gamma \lambda)^l \, \tilde{\delta}_{t+l}
$$

**引理 3.2** 给出 R-GAE 与标准 GAE 的关系：$\tilde{A}_t = A_t + B_t$，其中 $B_t$ 为仅依赖轨迹初始化偏移 $C$ 的轨迹常数。**推论 3.3** 证明基于 R-GAE 的策略梯度无偏：

$$
\mathbb{E}_t\big[ \nabla_{\phi} \log \pi_{\phi}(a_t \mid s_t) \, \tilde{A}_t \big] = \mathbb{E}_t\big[ \nabla_{\phi} \log \pi_{\phi}(a_t \mid s_t) \, A_t \big]
$$

### 相对价值学习目标

为训练反称差值函数，推导了仅依赖可观测奖励与非终止成对差值的引导目标。

**1 步目标**（含终端状态分情况处理）：

$$
y_{ij}^{(1)} := (r_i - r_j) + \gamma \, \delta_{ij}
$$

其中 $\delta_{ij}$ 根据后继是否终止分三种情况计算（详见附录 A），确保终端状态下的目标适定。

**n 步目标**（折叠非终止后继的成对差异）：

$$
y_{ij}^{(n)} := \sum_{k=0}^{n-1} \gamma^k (r_{i+k} - r_{j+k}) + \gamma^n \Delta_{\theta}(s_{i+n}, s_{j+n})
$$

**λ-回报目标**（指数加权平均 n 步目标，用于 TD(λ) 风格学习）：

$$
y_{ij}^{(\lambda)} := (1-\lambda) \sum_{n=1}^{\infty} \lambda^{n-1} \, y_{ij}^{(n)}
$$

### 轨迹排序初始化

当训练批次包含多条轨迹时，各轨迹独立锚定 $\tilde{V}(s_0)=0$ 会产生不一致的相对尺度。轨迹排序策略通过成对差值计算轨迹间的全局偏移，注入后使相对价值在跨轨迹间可比。该策略的核心动机来自方差分析——**引理 C.1** 给出相对策略梯度估计的方差分解：

$$
\operatorname{Var}(g_{\mathrm{rel}}) = \operatorname{Var}(g_{\mathrm{std}}) + \mathbb{E}\big[ \|\nabla_{\phi} \log \pi_{\phi}\|^2 B_t^2 \big] + 2\mathbb{E}\big[ A_t B_t \|\nabla_{\phi} \log \pi_{\phi}\|^2 \big]
$$

其中 $B_t^2$ 项与轨迹偏移 $C^2$ 成正比。轨迹排序通过最小化 $|C|$ 使 $B_t \approx 0$，从而抑制方差膨胀。



## 实验与关键发现

### 主实验：Atari 49 游戏基准

PPO+RV 作为 PPO 的即插即用型 critic 替代，在 Arcade Learning Environment（ALE）的 49 款 Atari 游戏上以 40M 帧训练后进行评估。核心结果如下：

**逐游戏对比**：在 49 款游戏中，PPO+RV 在 30 款上超越标准 PPO，在 37 款上超越直接优势估计基线 DAE。表 1 给出了所有游戏的最终平均得分（最后 100 个 episode 的均值）及标准差。以 VideoPinball 为例，PPO+RV 达到 138564.8±89747.6，而 PPO 为 37389.0±21539.2，DAE 仅为 23958.8±10071.8，相对 PPO 提升超过 10 万分。


![[assets/figures/papers/iclr26_0009_ulTRUwrzt9_Relative_Value_Learning/figures/006_Table_1.jpg]]
*Table 1: PPO+RV (ours) is competitive with PPO and DAE. Mean final scores (last 100 episodes) with standard deviation of PPO, DAE and our method (PPO+RV) after 40 M game frames*

**聚合指标**：图 3 展示了基于 Human Normalized Score 的聚合性能对比（采用 95% 分层自助置信区间）。PPO+RV 在所有四个指标上均取得最优：

![[assets/figures/papers/iclr26_0009_ulTRUwrzt9_Relative_Value_Learning/figures/007_Figure_3.jpg]]
*Figure 3: Compute Resources. Each 40M-frame run completes in approximately 65 minutes on a single A100 GPU with 12 CPU cores. Across all 49 games and 10 seeds (490 runs total), this corresponds to 530 GPU-hours or 22.10 A100-days. Figure 3: Comparison between Methods. Aggregate metrics with 95% stratified bootstrap confidence intervals (Agarwal et al., 2021). Higher median, interquartile mean (IQM), and mean, but lower optimality gap indicate better performance*

- 中位数约 0.95（PPO 约 0.88，DAE 约 0.82）
- IQM（四分位均值）约 0.93（PPO 约 0.83，DAE 约 0.72）
- 均值约 5.8（PPO 约 4.8，DAE 约 3.2）
- 最优性差距约 0.44（PPO 约 0.55，DAE 约 0.68）

DAE 在聚合指标上显著弱于 PPO 和 PPO+RV，表明直接学习优势函数在 Atari 大规模场景下不如相对价值学习稳定。

### 消融实验

**价值初始化策略**：图 4 对比了零初始化（公式 9 的默认构造 $\tilde{V}_{\theta}(s_0) := 0$）与偏移初始化（公式 26 的轨迹排序策略）在 49 款游戏上的学习曲线。偏移初始化在多数游戏中改善信用分配，表现优于或持平零初始化；部分游戏（如 BattleZone）对初始化不敏感。这一结果与方差分析一致——偏移初始化通过最小化轨迹常数基线 $B_t$ 的幅度来降低 R-GAE 估计方差。


![[assets/figures/papers/iclr26_0009_ulTRUwrzt9_Relative_Value_Learning/figures/008_Figure_4.jpg]]
*Figure 4: Ablation for Value Initialization. This figure compares the performance difference between zero (see Equation 9) and offset initialization (see Equation 26) for relative values. Usually the proposed offset initialization is needed to improve credit assignment, but for some games the algorithm can handle zero initialization as well*

**配对采样策略**：表 4 在 22 款游戏上对比了三种配对采样策略：完全随机、偏向同幕采样概率 p=0.33、以及 p=0.66。结果表明：

![[assets/figures/papers/iclr26_0009_ulTRUwrzt9_Relative_Value_Learning/figures/012_Table_4.jpg]]
*Table 4: Ablation of Pair Sampling. Mean final scores (last 100 episodes) with standard deviation of our method PPO+RV with different pair sampling strategies after 40 M game frames. The results average over five seeds*

- 随机配对策略通常优于强偏向同幕采样（p=0.66）
- 适度同幕采样（p=0.33）与随机策略各有胜负，差异不显著
- 过度偏向同幕（p≥0.66）可能降低性能，例如在 Alien 上从随机策略的 2123.4±346.0 降至 1802.0±600.5

这一消融说明相对价值学习对配对采样策略有一定敏感性，但默认配置（随机采样为主，33% 概率同幕）已足够稳健。

**轨迹常数基线的实证验证**：表 2 在一个小规模轨迹上验证了轨迹常数基线 $B_t$ 的存在性。设定 $\gamma=0.9$、$\lambda=0.8$、$C=2$，真实 GAE $A_t$ 与相对 GAE $\tilde{A}_t$ 的差值精确匹配预测的 $B_t$（例如 t=0 时差值为 0.61，与预测一致）。图 5 可视化了 $B_t$ 在 T=128 步 rollout 上的衰减：$|C|$ 越大，$B_t$ 的初始幅度越大，但随轨迹推进逐渐衰减至接近零。这印证了引理 C.1 的方差膨胀分析——相对梯度估计的方差包含与 $C^2$ 成正比的噪声项，因此轨迹排序策略对控制方差至关重要。

### 失败模式与局限性

1. **方差膨胀风险**：R-GAE 引入的轨迹常数基线 $B_t$ 在初始化偏移 $C$ 较大时会导致策略梯度估计方差显著增加。轨迹排序策略可缓解此问题，但在极端情况下（如轨迹间真实价值差异极大时）可能仍不足以完全抑制方差膨胀。

2. **验证范围有限**：当前实验仅覆盖离散动作的 Atari 环境。相对价值学习在连续控制、离线强化学习（off-policy）以及基于偏好的强化学习场景中的有效性尚未验证，这些场景下绝对尺度的模糊性可能更为突出，但成对采样的工程实现也面临不同挑战。

3. **DAE 性能显著弱于预期**：DAE 作为直接学习优势函数的基线，在 Atari 上表现明显逊于 PPO 和 PPO+RV。这一结果暗示直接优势估计在该规模下存在稳定性问题，但论文未深入分析其具体失败机制，需要进一步验证。



## 定位与知识库关联

### 与标准 Actor-Critic 的关系

相对价值学习（RV）直接回应了标准 actor-critic 框架中一个长期存在却常被忽略的结构性问题：**绝对价值函数估计引入了与决策无关的偏移自由度（gauge freedom）**。在 PPO 等 on-policy 算法中，价值网络 $V_\phi(s)$ 需要逼近 $V^\pi(s)$，但控制问题真正依赖的只是状态间的相对差异——优势函数 $A(s,a)$ 和策略梯度仅对 $V$ 的任意常数偏移不敏感。这一“规范自由度”导致：

- **训练不稳定与漂移**：绝对价值目标在隐式反馈或偏好式强化学习等绝对尺度模糊的场景下成为不适定问题。
- **冗余的学习负担**：价值网络必须同时学习决策无关的绝对尺度，增加了优化难度。

RV 将值学习目标从绝对尺度转移到差异空间，通过学习反称差值函数 $\Delta_\theta(s_i,s_j) = V^\pi(s_i) - V^\pi(s_j)$，天然移除了规范自由度。这一设计使 RV 成为 PPO 的 **drop-in critic 替代方案**：仅需替换价值网络头，保留策略网络和 PPO-clip 目标不变。

**与 Direct Advantage Estimation (DAE) 的对比**：DAE 直接学习优势函数 $A(s,a)$，同样试图绕过绝对价值估计。但 DAE 在 Atari 49 游戏上仅 12/49 超过 PPO（Table 1），而 PPO+RV 在 37/49 游戏中超过 DAE。RV 的优势在于保留了与 GAE 的理论兼容性——通过 R-GAE 构建优势估计，仅引入轨迹常数基线 $B_t$（Lemma 3.2），而策略梯度保持无偏（Corollary 3.3）。DAE 缺乏这种与广义优势估计的直接对应关系。

### 理论根基与适用边界

RV 的理论支柱是**成对贝尔曼算子** $T_\pi$ 在反称函数空间上的 $\gamma$-收缩性（Theorem 3.1），其唯一不动点等于真实值差。这为基于 TD 目标的学习提供了收敛保证。从成对差值出发，RV 构建了完整的学习管线：

1. **反称差值头**：$\Delta_\theta(s_i,s_j) = \Phi(f_{\text{enc}}(s_i) - f_{\text{enc}}(s_j))$，通过无偏置线性投影天然满足反称性与零自身差。
2. **相对价值伸缩构造**：$\tilde{V}_\theta(s_0) := 0,\ \tilde{V}_\theta(s_t) := \sum_{k=0}^{t-1} \Delta_\theta(s_{k+1}, s_k)$，从成对差值沿轨迹重构相对状态值。
3. **R-GAE 优势估计**：使用相对 TD 残差 $\tilde{\delta}_t$ 构造广义优势估计，等价于标准 GAE 加上轨迹常数基线 $B_t$。
4. **多步成对目标**：1步/n步/λ-回报目标仅使用可观测奖励与非终止成对差值，处理终端状态时通过分情况推导保证目标良定性。

**当前已验证的适用边界**：
- **环境类型**：仅在高维离散动作空间（Atari 49 游戏，40M 帧）上验证。
- **算法范式**：作为 on-policy PPO 的 critic 替代，未扩展到 off-policy 方法（如 DQN、SAC）。
- **反馈类型**：使用标准奖励信号，未在偏好反馈或隐式反馈的 RLHF 场景下测试。

### 关键局限与失效模式

**1. R-GAE 的方差膨胀问题**

相对策略梯度估计的方差分解（Lemma C.1）揭示了核心脆弱性：

$$\operatorname{Var}(g_{\text{rel}}) = \operatorname{Var}(g_{\text{std}}) + \mathbb{E}[\|\nabla_\phi \log \pi_\phi\|^2 B_t^2] + 2\mathbb{E}[A_t B_t \|\nabla_\phi \log \pi_\phi\|^2]$$

其中 $B_t$ 与轨迹初始化偏移 $C$ 成正比。当 $|C|$ 较大时，方差中的 $\mathbb{E}[\|\nabla_\phi \log \pi_\phi\|^2 B_t^2]$ 项呈二次增长，可能严重降低样本效率。Figure 5 可视化显示 $B_t$ 在轨迹起始步较大，随 $\gamma^t$ 衰减但未完全消失。

**缓解策略**：轨迹排序初始化（Trajectory Ranking）通过成对差值对多轨迹的相对价值进行全局排序并注入偏移，最小化 $|C|$。Figure 4 的消融实验表明，偏移初始化在多数游戏中优于零初始化，但部分游戏（如 BattleZone）对初始化不敏感——说明该方法并非对所有环境都有效。

**2. 配对采样策略的敏感性**

RV 的训练依赖状态对的采样策略。Table 4 的消融显示：
- 随机配对策略通常优于强偏向同幕采样（$p=0.66$）。
- 适度同幕采样（$p=0.33$）与随机策略各有胜负。
- 过度偏向同幕可能降低性能，因为减少了跨轨迹的对比学习信号。

这一敏感性意味着 RV 的性能对采样策略超参数有一定依赖，需要针对具体环境调优。

**3. 未验证的场景**

以下场景中 RV 的有效性尚待验证（论文明确列为开放问题）：
- **连续控制任务**（如 MuJoCo、DeepMind Control Suite）：状态空间的连续性可能影响成对差值的泛化特性。
- **离线强化学习**：RV 依赖在线 rollout 的成对采样和轨迹排序，离线设置下的采样策略需要重新设计。
- **基于偏好的强化学习**：这是 RV 理论上最有前景的场景（绝对尺度模糊正是其核心假设），但缺乏实验验证。
- **与 Q-learning 的集成**：RV 目前仅作为 critic 用于 actor-critic 框架，如何扩展到值迭代方法尚不明确。

### 知识库中的定位

RV 在强化学习值估计方法谱系中的位置可以概括为：

- **上游基础**：标准 actor-critic（PPO）、广义优势估计（GAE）、TD(λ) 方法。
- **并行方法**：Direct Advantage Estimation（直接学习优势函数）、Distributional RL（学习值分布而非标量值）。
- **下游延伸潜力**：偏好式 RL 的奖励建模、多任务迁移中的值差共享、元学习中的相对值先验。

RV 的核心贡献在于**识别并解决了绝对价值学习中的规范自由度问题**，将值函数学习从“估计绝对尺度”重新定义为“学习相对差异”。这一视角转换在理论上是优雅的（通过反称函数空间上的收缩算子保证收敛），在实践上是有效的（Atari 聚合指标全面优于 PPO 和 DAE），但其方差膨胀问题和未验证的应用场景构成了当前的主要边界。



## 原文 PDF

![[paperPDFs/ICLR_2026/Relative_Value_Learning.pdf]]
