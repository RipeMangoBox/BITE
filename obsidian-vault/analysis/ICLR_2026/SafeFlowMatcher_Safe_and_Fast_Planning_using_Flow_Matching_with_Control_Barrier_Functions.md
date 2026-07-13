---
title: "SafeFlowMatcher: Safe and Fast Planning using Flow Matching with Control Barrier Functions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SafeFlowMatcher_Safe_and_Fast_Planning_using_Flow_Matching_with_Control_Barrier_Functions.pdf
project_link: https://takahashi-seiryu.github.io/SafeFlowMatcher/
code_link: null
openreview_forum_id: refcXHU1Nh
aliases:
- SafeFlowMatcher
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "提出一种“预测-校正”（PC）积分器，将路径生成与安全认证解耦：预测阶段在无安全干预下通过流匹配生成候选路径；校正阶段引入消失时间缩放向量场（VTFD）以减少积分误差，并通过基于CBF的二次规划（QP）最小扰动地向候选路径注入安全约束。安全仅在校正阶段作用于接近目标的路径，避免破坏生成动态。"
primary_logic: "通过解耦生成与安全约束，并仅在最终路径上实施最小扰动安全修正，SafeFlowMatcher 保留了流匹配的高效采样特性，同时利用有限时间收敛CBF提供可认证的安全保证，有效抑制分布漂移与局部陷阱问题。"
claims:
- "预测-校正积分器通过仅在最终路径上施加安全约束，防止了分布漂移和局部陷阱。"
- "在 Maze2D 任务中，SafeFlowMatcher 取得最高评分 1.632，陷阱率 0%，而其他安全感知基线存在高陷阱率（如 SafeDiffuser 72%）。"
- "SafeFlowMatcher 在 T^c=4 的封闭解配置下总时间仅 0.023 秒，比 SafeDiffuser 快 50 倍，且路径完整。"
- "能量距离分析表明 SafeFlowMatcher 引起的分布漂移（0.061）显著小于 SafeFM（0.097）和 SafeDiffuser（0.229），说明PC积分器有效抑制了漂移。"
---

# SafeFlowMatcher: Safe and Fast Planning using Flow Matching with Control Barrier Functions

> [!tip] 核心洞察
> 通过解耦生成与安全约束，并仅在最终路径上实施最小扰动安全修正，SafeFlowMatcher 保留了流匹配的高效采样特性，同时利用有限时间收敛CBF提供可认证的安全保证，有效抑制分布漂移与局部陷阱问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SafeFlowMatcher：基于流匹配与控制屏障函数的安全快速规划 |
| 英文题名 | SafeFlowMatcher: Safe and Fast Planning using Flow Matching with Control Barrier Functions |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=refcXHU1Nh) · [Project](https://takahashi-seiryu.github.io/SafeFlowMatcher/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | SafeFlowMatcher |
| Dataset | Maze2D (maze-large-v1), Maze2D, Maze2D (Closed-Form CBF, T^c=4), Hopper (locomotion) |

> [!tip] 效果简介
> - Maze2D (maze-large-v1) 上，Score (↑) 为 1.632 ± 0.003，对比 RES-SafeDiffuser: 1.442 ± 0.451，变化 +0.190。
> - Maze2D 上，Trap Rate (↓) 为 0%，对比 RES-SafeDiffuser: 72%，变化 -72%。
> - Maze2D (Closed-Form CBF, T^c=4) 上，T-Time (s) (↓) 为 0.023，对比 RES-SafeDiffuser: 1.208，变化 -1.185 (~50× faster)。

## 概要

**核心瓶颈**：现有基于生成模型的规划器（扩散模型、流匹配）在采样过程中缺乏形式化安全保证。直接将控制屏障函数（CBF）施加于中间潜在状态的认证方法会引起语义错位——安全认证应作用于最终执行的路径，而对未执行的潜变量施加干预会扭曲学习到的流，导致分布漂移和局部陷阱（路径不完整）。

**方法定位**：SafeFlowMatcher 提出一种“预测-校正”（Prediction-Correction, PC）积分器，将路径生成与安全认证解耦。预测阶段在无安全干预下通过流匹配（Flow Matching, FM）生成候选路径；校正阶段引入消失时间缩放向量场（VTFD）以减少积分误差，并通过基于CBF的二次规划（QP）以最小扰动方式向候选路径注入安全约束。安全仅在校正阶段作用于接近目标的路径，避免破坏生成动态。

**核心结论**：
- 在 Maze2D 任务中，SafeFlowMatcher 取得最高评分 1.632，陷阱率 0%，而安全感知基线 SafeDiffuser 陷阱率高达 72%（Table 1）。
- 在封闭解配置（T^c=4）下，SafeFlowMatcher 总时间仅 0.023 秒，比 SafeDiffuser 快约 50 倍（Section 4.1）。
- 能量距离分析表明，SafeFlowMatcher 引起的分布漂移（0.061）显著小于 SafeFM（0.097）和 SafeDiffuser（0.229），验证 PC 积分器有效抑制了漂移（Figure 15）。
- 在高维机器人任务（运动与操控）上，SafeFlowMatcher 持续保持优势（Table 4）。

**方法谱系与知识库定位**：SafeFlowMatcher 处于流匹配规划（Flow Matching for Planning）与安全认证（CBF-based Certification）的交汇点。其基线包括无条件扩散规划器 **Diffuser**、确定性/随机性 **DDIM** 采样器、无条件 **FM** 规划器，以及安全感知变体 **SafeDiffuser**（ROS/RES/TVS）、**SafeDDIM** 和 **SafeFM**。与这些方法在采样过程中全程施加 CBF 约束不同，SafeFlowMatcher 通过解耦生成与安全的时序安排、引入 VTFD 收缩预测误差、以及带松弛项的 CBF-QP 最小扰动机制，在保留流匹配高效采样特性的同时提供可认证的安全保证。

**局限与开放问题**：方法假设预测误差服从对称零均值分布，在复杂环境中可能不成立；屏障函数和松弛权重的选择依赖特定环境；当前依赖预定义 CBF，未涉及从数据学习屏障函数；实验集中在仿真任务，尚未在真实机器人上验证。开放问题包括动态障碍物环境下的表现、CBF 与流匹配的端到端联合优化、极度非凸安全集中的松弛机制鲁棒性等。

### 生成式规划中的安全困境

基于生成模型的轨迹规划方法——特别是扩散模型与流匹配（Flow Matching, FM）——近年来展现出强大的分布建模能力，能够从噪声中生成高质量、多模态的候选路径。然而，当任务引入硬性安全约束（如障碍物规避、关节限位）时，这些方法的采样动态暴露出一个根本性缺陷：**生成过程缺乏形式化的安全保证**。

现有安全感知规划器（如 **SafeDiffuser** 及其变体 ROS/RES/TVS，**SafeDDIM**，**SafeFM**）的通行做法是，在采样的每一步对中间潜在状态施加控制屏障函数（CBF）约束。这一策略看似直接，却引发了两个相互纠缠的失效模式：

1. **分布漂移（Distributional Drift）**：CBF 干预改变了学习到的向量场方向，使采样轨迹偏离流匹配模型所建模的条件概率路径。最终生成的路径不再服从目标分布，路径质量（如平滑性、目标达成度）显著下降。能量距离分析定量印证了这一现象——SafeDiffuser 引入的漂移为 0.229，SafeFM 为 0.097，而 SafeFlowMatcher 仅 0.061（Figure 15）。

2. **局部陷阱（Local Trap）**：对中间潜在状态施加安全约束时，路径可能被“卡”在安全集边界附近，无法抵达目标。在 Maze2D 任务中，RES-SafeDiffuser 的陷阱率高达 72%，而 SafeFlowMatcher 为 0%（Table 1）。

这两个问题的根源在于**语义错位**：安全认证应当作用于最终执行的路径，而不是生成过程中的中间潜变量。对未收敛的中间状态强行施加 CBF，不仅扭曲了流匹配的生成动态，还可能导致优化不可行或振荡。

### 核心瓶颈与解决思路

本文识别出的核心瓶颈可概括为：

> **现有方法将路径生成与安全认证耦合在同一采样循环中，导致安全干预破坏生成动态，引发分布漂移和局部陷阱。**

针对这一瓶颈，SafeFlowMatcher 提出了一种**“预测-校正”（Prediction-Correction, PC）积分器**，其核心洞察是：**将生成与安全约束解耦，仅在最终路径上实施最小扰动安全修正**。具体而言：

- **预测阶段**：在无任何安全干预的条件下，通过流匹配向量场的前向积分生成候选路径。该阶段完整保留了 FM 的高效采样特性，使候选路径接近目标分布。
- **校正阶段**：以候选路径为起点，引入**消失时间缩放向量场（VTFD）**以收缩预测误差，并通过基于 CBF 的二次规划（QP）以最小扰动方式注入安全约束。安全认证仅作用于接近目标的路径，避免了生成过程中的动态破坏。

这一时序解耦策略使得 SafeFlowMatcher 在保留流匹配生成效率的同时，获得了有限时间收敛 CBF 提供的可认证安全保证，有效抑制了分布漂移与局部陷阱。

### 动机与目标

SafeFlowMatcher 的设计动机源于一个实际需求：**在安全至上的规划任务（如机器人导航、运动控制）中，同时实现高效率采样与可认证安全**。现有扩散规划器（如 Diffuser）虽能生成多样路径，但采样速度慢且缺乏安全保证；SafeDiffuser 等安全变体虽引入了 CBF，却牺牲了路径质量和生成效率。SafeFlowMatcher 旨在弥合这一鸿沟，通过 PC 积分器实现：

- **安全可认证**：利用有限时间收敛 CBF 提供形式化安全保证，确保路径在有限时间内进入并保持在安全集内。
- **高效采样**：预测阶段仅需极少的积分步数（T^p=1 即可），校正阶段的 QP 求解可采用封闭解，总时间可比 SafeDiffuser 快约 50 倍（0.023s vs. 1.208s）。
- **路径质量保持**：安全约束以最小扰动方式注入，避免扭曲流匹配学习到的路径分布。

## 核心方法与创新机理

SafeFlowMatcher 的核心创新在于通过**预测-校正（Prediction-Correction, PC）积分器**将路径生成与安全认证在时序上解耦，从根本上解决了现有安全感知生成式规划器的分布漂移与局部陷阱问题。该框架在三个关键维度上改变了 baseline 的设计范式。

### 1. 生成与安全约束的时序解耦

现有安全感知扩散或流匹配规划器（如 SafeDiffuser 的 ROS/RES/TVS 变体、SafeDDIM、SafeFM）在整个生成过程中对中间潜在状态施加控制屏障函数（CBF）约束。这种“边生成边认证”的策略存在根本性缺陷：安全认证应作用于最终执行的路径，而对未收敛的中间潜变量施加干预会扭曲学习到的流匹配（FM）动力学，导致**分布漂移**（distributional drift）和**局部陷阱**（local trap）——路径卡在障碍物附近无法到达目标。

SafeFlowMatcher 将这一过程拆分为两个独立阶段：
- **预测阶段**（Prediction Phase）：从噪声 $\tau_0^p$ 出发，通过 $T^p$ 步 Euler 积分 FM 向量场 $v_t$ 生成候选路径 $\tau_1^p$，全程无任何安全干预，完整保留 FM 的生成动力学。
- **校正阶段**（Correction Phase）：以预测路径 $\tau_0^c = \tau_1^p$ 为起点，在接近目标的路径上通过 CBF 约束的最小扰动修正实现安全认证。

这一时序解耦是 SafeFlowMatcher 所有性能优势的结构性根源：生成动力学不受安全约束干扰，安全约束仅在接近最终解的路径上施加，从而同时保留了 FM 的采样效率和 CBF 的安全保证。

### 2. 消失时间缩放流动力学（VTFD）替代标准积分

在预测阶段，Euler 积分不可避免地引入预测误差 $\varepsilon$，使得 $\tau_1^p = \tau_1^\star + \varepsilon$。若校正阶段直接使用原始 FM 向量场 $v_t$ 进行积分，该误差可能累积甚至放大。

SafeFlowMatcher 在校正阶段引入消失时间缩放流动力学（Vanishing Time-scaled Flow Dynamics, VTFD）：

$$\frac{d \pmb{\tau}_t^c}{d t} = \alpha (1 - t) v_t(\pmb{\tau}_t^c; \theta) \triangleq \tilde{v}_t(\pmb{\tau}_t^c; \theta)$$

缩放因子 $\alpha(1-t)$ 随时间线性衰减至零，使得向量场在早期快速接近目标，在后期趋于稳定。理论分析表明，在此动力学下预测误差以**二次与指数混合方式衰减**：

$$\mathbf{e}_t = O((1-t)^2) + (\varepsilon + O(1)) e^{-\alpha t}$$

这一设计使得校正阶段能够有效收缩预测误差，保证最终路径 $\tau_1^c$ 接近目标解。消融实验证实：关闭消失时间缩放（$\alpha=0$ 或直接使用 $v_t$）时，随着校正步数增加评分反而下降；VTFD 是维持路径质量的关键组件。

### 3. 带松弛机制的有限时间收敛 CBF-QP

Baseline 方法对每个采样步骤的每个路径点施加标准 CBF 约束，在高度非凸安全集（如迷宫）中容易导致数值不可行或振荡。

SafeFlowMatcher 在校正阶段的每个步骤对每个路径点独立求解带松弛项的二次规划（QP）：

$$\mathbf{u}_t^{k*}, r_t^{k*} = \operatorname*{arg min}_{\mathbf{u}_t^k, r_t^k} \| \mathbf{u}_t^k - \tilde{v}_t^k(\tau_t^c; \theta) \|^2 + r_t^{k^2} \quad \mathrm{subject~to} \quad (15)$$

其中约束条件为有限时间收敛 CBF 条件：

$$\operatorname*{sup}_{\mathbf{u}_t \in \mathcal{U}} \left[ L_f b(\mathbf{x}_t) + L_g b(\mathbf{x}_t) \mathbf{u}_t + \epsilon \cdot \mathrm{sgn}(b(\mathbf{x}_t)) |b(\mathbf{x}_t)|^\rho \right] \geq 0$$

该设计的三个关键改进：
- **最小扰动原则**：QP 目标函数最小化控制输入与原始流动力学的偏差，确保安全修正不扭曲路径形状。
- **松弛项** $w_t^k r_t^k$：在校正早期通过递减权重 $w_t^k$ 松弛 CBF 约束，防止数值不可行；当 $t \geq t_w$ 后松弛消失，保证最终路径严格满足安全认证。
- **有限时间收敛保证**：理论证明从初始点到进入鲁棒安全集 $\mathcal{C}_\delta$ 的最大时间有上界：

$$T \leq t_w + \frac{(\delta - b(\pmb{\tau}_{t_w}^{c,k}))^{1-\rho}}{\epsilon (1-\rho)}$$

### 创新点的因果链条

上述三个 changed slots 形成完整的因果链：**时序解耦**（slot 1）使得安全约束不干扰生成动力学，消除分布漂移的结构性根源；**VTFD**（slot 2）保证校正阶段的路径质量不因预测误差而退化；**带松弛的 CBF-QP**（slot 3）在维持安全认证的同时提供数值稳定性。三者共同作用，使 SafeFlowMatcher 在 Maze2D 上取得 0% 陷阱率（对比 SafeDiffuser 的 72%），评分 1.632 的 SOTA 性能，以及在封闭解配置下比 SafeDiffuser 快 50 倍的推理速度（0.023s vs. 1.208s）。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_refcXHU1Nh/figures/001_Figure_1.jpg]]
*Figure 1: Overview of SafeFlowMatcher Versus Existing Certification-Based Methods. Directly constraining intermediate samples during generation (top) can cause paths to be distorted or trapped, whereas Safe-FlowMatcher (bottom) decouples generation and certification, producing a complete and certified-safe path*

SafeFlowMatcher 的整体 pipeline 围绕一个核心设计原则展开：**将路径生成与安全认证在时序上彻底解耦**。现有安全感知生成式规划器（如 SafeDiffuser、SafeFM）在采样的每一步都对中间潜在状态施加控制屏障函数（CBF）约束，这种“边生成边认证”的策略会导致两个严重后果——**分布漂移**（生成的路径分布偏离原始流匹配学到的目标分布）和**局部陷阱**（路径因过早的安全干预而卡在障碍物附近，无法抵达目标）。SafeFlowMatcher 通过“预测-校正”（Prediction-Correction, PC）积分器将这一耦合打破，使安全约束仅在接近最终路径时才被注入，从而保留了流匹配的高效采样特性。

### 两阶段流水线

整个框架由三个关键模块串联而成，形成清晰的前向数据流：

| 阶段 | 输入 | 核心操作 | 输出 | 安全干预 |
|------|------|----------|------|----------|
| **预测阶段** | 噪声样本 $\tau_0^p \sim p_0$ | $T^p$ 步 Euler 积分 FM 向量场 $v_t$ | 候选路径 $\tau_1^p \approx \tau_1^* + \varepsilon$ | 无 |
| **校正阶段** | 预测路径 $\tau_0^c = \tau_1^p$ | $T^c$ 步 VTFD 积分 + CBF-QP 修正 | 安全最终路径 $\tau_1^c$ | 有（最小扰动） |
| **CBF-QP 求解器** | 每步每点的 $\tilde{v}_t^k$ 与屏障值 | 求解二次规划 (17) | 修正控制量 $\mathbf{u}_t^{k*}$ | 核心安全机制 |

#### 预测阶段：无干预生成候选路径

预测阶段从先验噪声分布中采样 $\tau_0^p$，通过 $T^p$ 步标准 Euler 积分沿流匹配向量场 $v_t(\tau_t;\theta)$ 前向传播，得到候选路径 $\tau_1^p$。这一阶段**完全不涉及任何安全约束**，因此流匹配学到的原生动力学得以完整保留。由于 Euler 积分的数值误差，$\tau_1^p$ 与精确解 $\tau_1^*$ 之间存在预测误差 $\varepsilon$，但实验表明即使 $T^p=1$（单步预测），该误差也足够小，使候选路径已接近目标分布。

#### 校正阶段：安全约束的最小扰动注入

校正阶段以预测路径为起点（$\tau_0^c = \tau_1^p$），通过两个机制协同工作：

1. **消失时间缩放流动力学（VTFD）**：将原始向量场乘以衰减因子 $\alpha(1-t)$，形成 $\tilde{v}_t = \alpha(1-t)v_t$。这一缩放在校正早期（$t$ 接近 0 时）保持较大的积分步长以快速接近目标，在校正后期（$t \to 1$）则趋于零，使路径稳定收敛。理论分析表明，在此动力学下预测误差以 $O((1-t)^2) + (\varepsilon + O(1))e^{-\alpha t}$ 的速度衰减，即同时具备二次衰减和指数衰减特性。

2. **CBF-QP 安全修正**：在每个校正步骤 $t$ 和每个路径点 $k$ 上，独立求解一个二次规划问题：
   $$\mathbf{u}_t^{k*}, r_t^{k*} = \operatorname*{arg min}_{\mathbf{u}_t^k, r_t^k} \| \mathbf{u}_t^k - \tilde{v}_t^k(\tau_t^c; \theta) \|^2 + r_t^{k^2} \quad \mathrm{subject~to} \quad (15)$$
   该 QP 以最小化对 VTFD 向量场的偏离为目标，同时满足带松弛项的有限时间收敛 CBF 条件。松弛变量 $r_t^k$ 与递减权重 $w_t^k$ 配合，在校正早期提供数值稳定性（防止因路径点远离安全集导致 QP 不可行），当 $t \geq t_w$ 后松弛项消失，确保最终路径满足严格的安全认证。

### 关键设计决策与因果机制

**为什么解耦是有效的？** 现有方法在生成过程中对中间潜变量施加 CBF 约束，本质上是让安全认证作用于一个尚未收敛到目标分布的中间表示。这导致两个问题：(1) 安全干预扭曲了学习到的向量场，使最终路径偏离训练分布（分布漂移）；(2) 在非凸安全集（如迷宫）中，早期干预可能将路径推入无法逃脱的“死胡同”（局部陷阱）。SafeFlowMatcher 将安全约束推迟到校正阶段——此时路径已接近目标，安全修正只需做微小调整即可满足约束，既保留了路径质量，又避免了漂移和陷阱。

**VTFD 的双重作用**：VTFD 不仅是误差收缩工具，还间接服务于安全目标。通过在校正早期保持较大的向量场幅值，它使路径快速脱离预测误差的影响区域；在校正后期向量场趋于零，则使 CBF-QP 的修正成为主导力，平滑地将路径推入安全集内部。

**松弛项的必要性**：在高度非凸的安全集（如 Maze2D）中，预测路径的某些点可能初始时远离安全集，此时严格的 CBF 条件会导致 QP 不可行或产生极端修正量。松弛项 $w_t^k r_t^k$ 在校正早期允许暂时违反 CBF 条件，随着 $t$ 增大和 $w_t^k$ 衰减，约束逐渐收紧，最终在 $t \geq t_w$ 时恢复为严格安全认证。这一机制在 Maze2D 实验中至关重要——关闭松弛项会导致 SafeFlowMatcher 也出现局部陷阱。

### 输入输出规范

- **输入**：从先验分布 $p_0$ 采样的噪声 $\tau_0^p$（与训练时一致的噪声分布）；预训练的流匹配向量场参数 $\theta$；CBF 参数 $(\delta, \epsilon, \rho)$ 及松弛权重调度 $\{w_t^k\}$。
- **输出**：满足 $b(\tau_1^{c,k}) \geq \delta$（鲁棒安全边界）的完整路径 $\tau_1^c$，其中每个路径点均通过有限时间收敛 CBF 认证。
- **可配置项**：预测步数 $T^p$（默认 1）、校正步数 $T^c$（默认 256）、缩放常数 $\alpha$（默认 2.0）、松弛消失时间 $t_w$。

SafeFlowMatcher 的核心架构是一个**预测-校正（Prediction-Correction, PC）积分器**，它将路径生成与安全认证在时序上完全解耦。该方法包含四个关键模块：预测阶段、校正阶段（含消失时间缩放流动力学）、CBF-QP 求解器，以及松弛项与权重机制。

### 预测阶段

预测阶段的目标是在**无任何安全干预**的条件下，通过流匹配（Flow Matching, FM）的向量场生成一条候选路径。该阶段从噪声样本 $ \tau_0^p $ 出发，经 $ T^p $ 步 Euler 积分得到预测路径：

$$ \tau_1^p = \Psi_{0 \to 1}^{(T^p)}(\tau_0^p) = \tau_1^\star + \varepsilon \tag{9} $$

其中 $ \tau_1^\star $ 是流匹配 ODE 的精确解，$ \varepsilon $ 为 Euler 积分引入的预测误差。该误差是后续校正阶段需要处理的核心对象。实验表明，$ T^p=1 $ 即足以获得高质量候选路径（Score 1.632），进一步增大 $ T^p $ 仅增加计算时间而不显著提升路径质量（Table 2）。

### 校正阶段与消失时间缩放流动力学

校正阶段以预测路径为起点 $ \tau_0^c = \tau_1^p $，通过 $ T^c $ 步积分同时完成两项任务：**收缩预测误差**和**注入安全约束**。为收缩误差，该阶段引入**消失时间缩放流动力学（Vanishing Time-Scaled Flow Dynamics, VTFD）**：

$$ \frac{d \pmb{\tau}_t^c}{d t} = \alpha (1 - t) v_t(\pmb{\tau}_t^c; \theta) \triangleq \tilde{v}_t(\pmb{\tau}_t^c; \theta) \tag{10} $$

其中 $ \alpha $ 为缩放常数，$ 1-t $ 因子使向量场随时间衰减。VTFD 的关键性质是使预测误差呈**二次与指数混合衰减**：

$$ \mathbf{e}_t = O((1-t)^2) + (\varepsilon + O(1)) e^{-\alpha t} \tag{12} $$

这意味着校正初期向量场较强，可快速接近目标路径；校正后期向量场趋零，保证数值稳定性。消融实验证实，关闭消失时间缩放（$ \alpha=0 $ 或直接使用 $ v_t $）时，随着 $ T^c $ 增加评分反而下降（Figure 7）；$ \alpha=2.0 $ 时评分最优（Table 3）。

### CBF-QP 求解器

安全约束通过在校正阶段的流动力学上叠加最小扰动控制量来实现：

$$ \frac{d \pmb{\tau}_t^{c,k}}{dt} = \tilde{v}_t^k(\pmb{\tau}_t^c; \theta) + \Delta \mathbf{u}_t^k \triangleq \mathbf{u}_t^k \tag{13} $$

其中 $ k $ 为路径点索引。每个校正步的每个路径点独立求解如下二次规划（QP）以获得最优控制量：

$$ \mathbf{u}_t^{k*}, r_t^{k*} = \operatorname*{arg min}_{\mathbf{u}_t^k, r_t^k} \| \mathbf{u}_t^k - \tilde{v}_t^k(\tau_t^c; \theta) \|^2 + r_t^{k^2} \quad \mathrm{subject~to} \quad (15) \tag{17} $$

约束条件 (15) 为**有限时间收敛 CBF 条件**：

$$ \operatorname*{sup}_{\mathbf{u}_t \in \mathcal{U}} \left[ L_f b(\mathbf{x}_t) + L_g b(\mathbf{x}_t) \mathbf{u}_t + \epsilon \cdot \mathrm{sgn}(b(\mathbf{x}_t)) |b(\mathbf{x}_t)|^\rho \right] \geq 0 \tag{7} $$

该条件保证系统状态在有限时间内进入并保持在安全集 $ \mathcal{C} \triangleq \{ \mathbf{x}_t \in \mathcal{D} \mid b(\mathbf{x}_t) \geq 0 \} $ 内。有限收敛时间的理论上界为：

$$ T \leq t_w + \frac{(\delta - b(\pmb{\tau}_{t_w}^{c,k}))^{1-\rho}}{\epsilon (1-\rho)} \tag{16} $$

由 CBF 参数 $ (\rho, \epsilon) $ 和初始屏障值决定。在 Maze2D 任务中，QP 求解采用闭式解时平均耗时仅 1.14 ms（Table 1 caption），使 SafeFlowMatcher 在 $ T^c=4 $ 配置下总时间仅 0.023 秒，比 SafeDiffuser 快约 50 倍（Section 4.1）。

### 松弛项与权重机制

为增强数值稳定性，CBF-QP 在校正早期引入松弛变量 $ r_t^k $ 和递减权重 $ w_t^k $。当 $ t < t_w $ 时，松弛项允许路径点暂时偏离安全集，防止在高度非凸安全集（如 Maze2D）中出现不可行或振荡；当 $ t \geq t_w $ 时，$ w_t^k $ 消失，松弛项失效，确保最终路径严格满足 $ b(\tau) \geq \delta $（$ \delta=0.01 $ 为鲁棒性边界）。该机制在非凸环境中尤为关键（Remark 2）。

## 实验与关键发现

### 核心瓶颈与因果机制验证

SafeFlowMatcher 的设计围绕一个关键因果旋钮展开：**将路径生成与安全认证在时序上解耦**。现有安全感知规划器（如 SafeDiffuser、SafeFM）在整个生成过程中持续对中间潜在状态施加 CBF 约束，这会导致两个相互关联的失败模式——分布漂移和局部陷阱。因果链条如下：对尚未收敛的中间样本施加安全干预会扭曲流匹配（flow matching）学习到的向量场，使生成分布偏离目标分布（分布漂移）；同时，在复杂障碍环境中，中间样本可能被“推入”障碍物死角，由于缺乏全局视野而无法逃逸（局部陷阱，Figure 2）。

SafeFlowMatcher 通过预测-校正（PC）积分器切断这一因果链：预测阶段在不施加任何安全约束的条件下，利用流匹配向量场将噪声样本传播至接近目标路径的候选解；校正阶段才以最小扰动方式注入 CBF 安全约束，且仅作用于已接近目标路径的样本。这一时序解耦策略从根本上防止了安全干预对生成动力学的破坏。

**证据强度**：能量距离分析（Figure 15）直接量化了分布漂移——SafeFlowMatcher 引起的漂移（0.061）显著低于 SafeFM（0.097）和 SafeDiffuser（0.229），证实 PC 积分器有效抑制了漂移。Table 9 的消融实验进一步表明，无 PC 积分器的 SafeFM 在广泛的 CBF 超参数范围内陷阱率高达 100%，而 SafeFlowMatcher 保持 0% 陷阱率，直接验证了“解耦生成与安全”这一因果机制的有效性。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_refcXHU1Nh/figures/043_Table_9.jpg]]
*Table 9: Comparison between SafeFlowMatcher and SafeFM on CBF hyperparameters. Subset of the (ρ, ϵ) hyperparameter grid in Maze2D, comparing SafeFlowMatcher (ours) and SafeFM (w/o PC). Each entry reports mean ± std over 100 rollouts for Score, Trap Rate, curvature (κ), acceleration (a), and minimum barrier values (BS1, BS2)*

### 主实验结果

#### Maze2D 导航任务

Table 1 汇总了 Maze2D 环境下的主实验结果。SafeFlowMatcher 在所有方法中取得最高评分（Score = 1.632 ± 0.003），且陷阱率（Trap Rate）为 0%。相比之下，最强的安全感知基线 RES-SafeDiffuser 的陷阱率高达 72%，评分仅为 1.442 ± 0.451（方差大，表明性能不稳定）。


**安全指标**：SafeFlowMatcher 的两个屏障安全指标 BS1 和 BS2 均为 0.010，满足鲁棒安全阈值 δ = 0.01 的要求，且无安全违规。这表明校正阶段的 CBF-QP 能够可靠地将路径约束在安全集内。

**效率指标**：在闭式解配置下（T^c = 4），SafeFlowMatcher 的总时间（T-Time）仅为 0.023 秒，比 SafeDiffuser（1.208 秒）快约 50 倍（Table 10）。即使使用通用 QP 求解器（T^c = 256），SafeFlowMatcher 的 0.157 秒也比 SafeDiffuser 快约 8 倍（Table 11）。效率优势源于两个因素：（1）流匹配本身比扩散模型需要更少的采样步数；（2）预测阶段已将样本推至目标附近，校正阶段的 CBF-QP 仅需微调，计算量远小于对全空间随机样本施加约束。

**路径质量**：SafeFlowMatcher 的路径曲率（κ = 69.19）和加速度（a = 91.90）均处于合理范围，表明路径在保证安全的同时维持了平滑性。

#### 采样步数鲁棒性

Figure 4 展示了不同采样步数（sampling horizon T）下的评分变化。SafeFlowMatcher 在所有采样步数下均保持最高评分，且性能稳定。值得注意的是，即使在极低采样步数（T = 16）下，SafeFlowMatcher 的评分仍显著优于其他方法在高步数下的表现。当关闭安全约束时（Figure 4 右），FlowMatcher（FM + PC 积分器）同样优于其他无条件方法，表明 PC 积分器本身对路径质量有正向贡献。

#### 高维机器人任务

Table 4 展示了 SafeFlowMatcher 在运动（locomotion）和操控（manipulation）任务上的表现。在 Hopper 任务上，SafeFlowMatcher 取得 0.917 ± 0.026 的评分，优于 SafeDiffuser（约 0.883）和 SafeFM（约 0.868）。在 Walker2D 和 Block Stacking 任务上，SafeFlowMatcher 同样保持领先。这表明 PC 积分器的解耦策略在高维连续控制场景中同样有效，安全约束的注入未显著破坏生成路径的物理合理性。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_refcXHU1Nh/figures/018_Table_4.jpg]]
*Table 4: Performance on high-dimensional robotic tasks. SafeFlowMatcher maintains its advantages in both locomotion and robot manipulation settings*

### 消融实验

#### PC 积分器的核心作用

Table 9 直接对比了 SafeFlowMatcher 与 SafeFM（无 PC 积分器）在不同 CBF 超参数 (ρ, ε) 下的表现。SafeFM 在大多数参数组合下陷阱率达到 100%，评分剧烈下降至 0.45–1.42 区间。而 SafeFlowMatcher 在所有参数组合下保持 0% 陷阱率，评分稳定在约 1.63。这一对比强有力地证明：**PC 积分器的解耦设计是实现鲁棒安全的关键，而非 CBF 参数的选择**。

#### 预测步数 T^p 的影响

Table 2 展示了预测步数 T^p 对路径质量和计算时间的影响。T^p = 1 时即可获得最高评分（1.632），进一步增大 T^p 至 16 仅使总时间从 1.209 秒微增至 1.287 秒，评分不变。这表明流匹配的预测阶段效率极高，单步积分即可将样本推至目标路径附近，验证了 Lemma 3 中预测误差 ε 的有限性。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_refcXHU1Nh/figures/007_Table_2.jpg]]
*Table 2: Effect of prediction horizon T p. We compare path quality metrics (score, curvature, and acceleration) and the total computation time, measured after one full path generation*

#### 消失时间缩放常数 α 的影响

Table 3 和 Figure 6 展示了缩放常数 α 对路径质量的影响。α = 2.0 时评分最优（1.632）。增大 α 会持续降低路径曲率（κ 从 α=1.0 时的 85.10 降至 α=3.0 时的 44.08）和加速度（a 从 173.22 降至 58.05），使路径更平滑，但过大的 α 可能扭曲路径形状（偏离目标分布）。VTFD 中的 (1 − t) 因子使向量场在 t → 1 时自然衰减，α 控制衰减速率：过小则误差收缩不足，过大则过度平滑。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_refcXHU1Nh/figures/009_Table_3.jpg]]
*Table 3: Effect of scaling constant α. Path qualities are measured after full generation*

#### 消失时间缩放的必要性

Figure 7 的消融显示，当关闭消失时间缩放（α = 0，直接使用原始 v_t）时，随着校正步数 T^c 增加，评分反而下降。这是因为缺乏衰减机制的向量场在接近目标时会引入额外积分误差，累积的扰动使路径偏离最优解。VTFD 通过 (1 − t) 因子使向量场在校正后期自然归零，保证了误差的二次方与指数衰减（Eq. 12），从而在更多校正步数下维持路径质量。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_refcXHU1Nh/figures/015_Figure_7.jpg]]
*Figure 7: Score with and without a vanishing time-scale. When T ^ { p } = 1 , as the correction horizon T ^ { c } increases, we see that the score decreases in the absence of vanishing time-scale*

### 失败模式与局限性

尽管 SafeFlowMatcher 在实验中表现优异，但存在以下已知局限：

1. **预测误差对称假设**：Lemma 3 的误差衰减分析假设预测误差 ε 服从对称零均值分布。在高度复杂或非凸的安全集环境中，该假设可能不成立，导致误差衰减速率低于理论预期。当前实验未系统验证重尾分布下的鲁棒性。

2. **屏障函数依赖**：SafeFlowMatcher 依赖预定义的已知 CBF。在 Maze2D 中，屏障函数由障碍物几何直接导出；在机器人任务中，CBF 由任务约束定义。对于未知或动态变化的环境，需要从数据中学习屏障函数，而当前框架未涉及 CBF 学习。

3. **松弛项权重调参**：在高度非凸安全集（如 Maze2D）中，松弛项权重 w_t^k 的衰减策略对数值稳定性至关重要。Remark 2 明确指出松弛项在 Maze2D 中“必不可少”，暗示在更复杂的约束拓扑中可能需要仔细调参。

4. **仿真验证局限**：所有实验均在仿真环境（Maze2D、Gym-Mujoco、机器人操控仿真）中完成，尚未在真实机器人上验证。仿真到现实的迁移中，模型误差和感知噪声可能影响 CBF 条件的满足。

### 关键图表结论汇总

- **Figure 3**：直观对比了 SafeDiffuser 与 SafeFlowMatcher 的路径生成过程。SafeDiffuser 从全空间随机初始化样本，在收敛过程中部分样本陷入局部陷阱；SafeFlowMatcher 从预测阶段开始样本已聚集在目标路径附近，校正阶段仅微调，无局部陷阱。
- **Figure 15**：能量距离分析量化了分布漂移，SafeFlowMatcher（0.061）显著优于 SafeFM（0.097）和 SafeDiffuser（0.229），直接验证 PC 积分器的解耦效果。
- **Table 9**：SafeFM 在无 PC 积分器时陷阱率 100%，SafeFlowMatcher 保持 0%，证明 PC 积分器是安全鲁棒性的必要条件。
- **Table 10–11**：闭式解和 QP 求解器两种配置下，SafeFlowMatcher 均比 SafeDiffuser 快 8–50 倍，验证了流匹配 + 解耦策略的效率优势。

## 定位与知识库关联

### 核心瓶颈与设计动机

SafeFlowMatcher 的方法设计围绕一个明确的因果瓶颈展开：**现有基于生成模型的规划器（扩散模型、流匹配）在采样动态中缺乏形式化安全保证，而直接将控制屏障函数施加于中间潜在状态的认证方法会引起语义错位**。具体而言，安全认证应作用于最终执行的路径，对未收敛的中间潜变量施加 CBF 干预会扭曲学习到的流分布，导致分布漂移和局部陷阱——即路径在障碍物前停滞不完整。

这一洞察将 SafeFlowMatcher 与两类基线区分开来：

- **无条件生成规划器**：如 **Diffuser**、**DDIM**（确定性/随机性采样器）、**FM**（流匹配）和 **FlowMatcher**（带 PC 积分器但无安全约束），它们不提供安全保证。
- **安全感知扩散/流匹配变体**：如 **SafeDiffuser**（ROS、RES、TVS 三种变体）、**SafeDDIM** 和 **SafeFM**，它们在采样过程中对中间潜在状态施加 CBF 约束，导致分布漂移和局部陷阱（SafeDiffuser 陷阱率高达 72%）。

SafeFlowMatcher 的核心创新在于**将安全约束的时序从生成过程解耦**：先完成无干预的路径预测，再在接近目标的路径上实施最小扰动安全修正。这一“预测-校正”框架保留了流匹配的高效采样特性，同时利用有限时间收敛 CBF 提供可认证的安全保证。

### 方法变体谱系中的定位

从生成模型规划器的方法谱系来看，SafeFlowMatcher 处于以下交叉点：

| 维度 | 基线方法 | SafeFlowMatcher |
|------|---------|-----------------|
| 生成模型 | 扩散模型（Diffuser, SafeDiffuser） | 流匹配（FM） |
| 安全约束介入时机 | 生成过程中全程介入（SafeDiffuser, SafeFM） | 仅在校正阶段介入 |
| 积分向量场 | 标准 Euler 积分 | 消失时间缩放向量场（VTFD） |
| 安全约束形式 | 标准 CBF 约束（无可松弛项） | 带松弛项的有限时间收敛 CBF-QP |
| 分类器/引导 | CG、CG-e（分类器引导） | 无需额外引导网络 |

具体而言，SafeFlowMatcher 相对于各基线的方法差异体现在三个关键“槽位”上：

**槽位 1：生成与安全约束的时序安排。** SafeDiffuser 和 SafeFM 在整个生成过程中对中间潜在状态施加 CBF 安全约束，这导致分布漂移与局部陷阱。SafeFlowMatcher 则先进行无安全干预的预测阶段生成候选路径，然后在校正阶段对接近目标的路径施加 CBF 安全约束，解耦二者的时序（证据锚点：Introduction 中明确说明“SafeFlowMatcher enforces safety only in the correction phase”）。

**槽位 2：积分向量场的结构。** 基线方法直接使用 FM 向量场 $v_t$ 进行 Euler 积分。SafeFlowMatcher 在校正阶段引入消失时间缩放向量场 $\alpha(1-t)v_t$，使预测误差呈二次方与指数衰减（Lemma 3），从而在校正步数增加时仍保持路径质量。

**槽位 3：安全约束实施机制。** SafeDiffuser 对每个采样步骤的每个路径点施加标准 CBF 约束（无松弛项），可能引起不可行与振荡。SafeFlowMatcher 在校正阶段通过 QP 最小扰动地满足带松弛项 $w_t^k r_t^k$ 的有限时间收敛 CBF 条件，增强数值稳定性并保证有限时间流入安全集（Theorem 1 和 Proposition 1 提供理论保证）。

### 适用边界与局限

SafeFlowMatcher 的有效性依赖于以下边界条件：

1. **预测误差分布假设**：方法假设预测误差服从对称零均值分布，该假设在更复杂环境中可能不成立，影响误差衰减速率。当环境高度非结构化或流匹配模型训练不充分时，预测误差可能呈现重尾分布，此时 VTFD 的误差收缩效果可能减弱。

2. **屏障函数需预定义**：当前框架依赖预定义的已知 CBF，未涉及从数据中学习屏障函数。这意味着在未知环境或动态变化的安全集中，方法的适用性受到限制。对于高度非凸安全集（如 Maze2D），松弛项权重的选择需要仔细调参——论文明确指出“松弛项主要在非凸环境中必要”。

3. **仿真验证为主**：实验集中在仿真任务（迷宫导航、Hopper 运动、机器人操控），尚未在真实机器人上验证。从仿真到现实的迁移中，CBF 的建模误差和传感器噪声可能影响安全认证的可靠性。

4. **CBF 超参数敏感性**：消融实验（Table 9）表明，无 PC 积分器的 SafeFM 在参数变化下陷阱率高达 100%，而 SafeFlowMatcher 在广泛的 $(\rho, \epsilon)$ 范围内保持 0% 陷阱率。但缩放常数 $\alpha$ 的最优值（2.0）需要针对环境调整——过大的 $\alpha$ 虽使路径更平滑但可能扭曲路径形状。

### 开放问题

1. **动态环境扩展**：SafeFlowMatcher 在动态障碍物和时变约束环境中的表现如何？当前框架假设安全集是静态的，而真实场景中障碍物可能移动，CBF 需要实时更新。

2. **端到端联合优化**：能否将 CBF 的学习与流匹配模型联合优化，以端到端方式同时提升生成质量与安全性？当前方法中屏障函数是外生给定的，限制了在未知环境中的泛化能力。

3. **极端非凸安全集的松弛机制**：当安全集极度非凸或高维时，松弛机制如何保证不牺牲安全认证？论文指出松弛项主要在早期校正阶段起作用（$t \geq t_w$ 后消失），但 $t_w$ 的选择缺乏理论指导。

4. **重尾误差分布的鲁棒性**：VTFD 的误差衰减分析基于对称零均值假设，当预测误差呈现重尾分布时，是否需要自适应调整收缩参数 $\alpha$ 或引入鲁棒估计？

5. **多智能体与交互场景**：SafeFlowMatcher 的 CBF-QP 框架是否可扩展到多智能体安全规划，其中每个智能体的安全集依赖于其他智能体的行为？

## 原文 PDF

![[paperPDFs/ICLR_2026/SafeFlowMatcher_Safe_and_Fast_Planning_using_Flow_Matching_with_Control_Barrier_Functions.pdf]]
