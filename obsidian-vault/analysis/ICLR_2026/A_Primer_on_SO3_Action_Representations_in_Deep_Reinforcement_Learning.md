---
title: "A Primer on SO(3) Action Representations in Deep Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Primer_on_SO3_Action_Representations_in_Deep_Reinforcement_Learning.pdf
project_link: https://amacati.github.io/so3_primer
code_link: null
aliases:
- LTVDAR
- PS3ARDRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "动作表示的选择（特别是局部切空间增量 vs 全局矩阵/四元数）以及是否对网络输出进行单位旋转居中（unit-rotation centering）和缩放（scaling）。"
primary_logic: "将动作表示为局部坐标系中的切向量（tangent vectors in the local frame）能提供最可靠的结果，因为它天然居中于单位旋转、便于缩放以避开切空间的割迹（cut locus），且在小角度下近似于delta欧拉角但无奇异性。"
claims:
- "Delta tangent vector representation almost always results in the best final policy with minor variances between runs."
- "Global matrix representations achieve the second-best performance, except for SAC with sparse rewards, where they exhibit poor performance."
- "Projecting actions leads to significant performance loss in PPO because probability ratios no longer match."
- "Scaling tangent vectors to the range of permissible angles improves performance and stability."
---

# A Primer on SO(3) Action Representations in Deep Reinforcement Learning

> [!tip] 核心洞察
> 将动作表示为局部坐标系中的切向量（tangent vectors in the local frame）能提供最可靠的结果，因为它天然居中于单位旋转、便于缩放以避开切空间的割迹（cut locus），且在小角度下近似于delta欧拉角但无奇异性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 深度强化学习中SO(3)动作表示入门 |
| 英文题名 | A Primer on SO(3) Action Representations in Deep Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=g4ZrpMQL1Z) · [Project](https://amacati.github.io/so3_primer) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | 局部切空间增量动作表示（Local Tangent Vector Delta Action Representation） |
| Dataset | Idealized Rotation Environment |

> [!tip] 效果简介
> - Idealized Rotation Environment 上，PPO dense reward 为 -5.4 ± 0.2 (s_tau)，对比 -5.4 ± 0.2 (R), -8.4 ± 0.5 (ε_τ)，变化 tied with R, better than ε_τ。
> - Idealized Rotation Environment 上，SAC dense reward 为 -2.9 ± 0.3 (s_tau)，对比 -4.7 ± 0.3 (R), -7.1 ± 1.5 (ε_τ)，变化 best。
> - Idealized Rotation Environment 上，SAC sparse reward 为 -7.9 ± 0.8 (s_tau)，对比 -29.4 ± 0.7 (R), -33.5 ± 1.8 (ε_τ)，变化 best。

## 概要

本文系统性地研究了SO(3)旋转群的不同动作表示在深度强化学习连续控制任务中的影响。核心瓶颈在于：SO(3)流形不存在全局光滑、无奇点的最小参数化，导致常见的欧拉角、四元数、旋转矩阵、李代数等表示在强化学习动作空间中会引入不同的探索偏差、熵正则化失效和训练不稳定问题。

**核心结论**：将动作表示为局部坐标系中的切向量增量（delta tangent vector in local frame）在几乎所有测试场景下都取得了最佳最终策略性能，且运行间方差最小。全局旋转矩阵表示整体表现次之，但在SAC稀疏奖励场景下性能显著下降。论文明确指出，动作表示的选择（特别是局部切空间增量 vs 全局矩阵/四元数）以及对网络输出是否进行单位旋转居中（unit-rotation centering）和缩放（scaling）是影响训练稳定性和最终性能的关键因果变量。

**方法定位**：论文并未提出新的强化学习算法，而是在标准PPO、SAC、TD3算法的框架下，系统比较了6类动作表示（旋转矩阵、四元数、欧拉角、李代数切向量、6D表示、局部切空间增量）在理想化旋转环境、无人机轨迹跟踪、无人机竞速、RoboSuite机器人操作基准上的表现。关键设计变化包括：在策略网络输出中添加单位旋转偏置、将切向量范数限制到最大允许角度α_max、以及在策略网络内部投影均值而非采样后投影。

**主要结果**：在理想化旋转环境中，局部切空间增量表示在PPO密集奖励下与旋转矩阵持平（-5.4 ± 0.2），在SAC密集奖励（-2.9 ± 0.3 vs 全局矩阵-4.7 ± 0.3）、SAC稀疏奖励（-7.9 ± 0.8 vs 全局矩阵-29.4 ± 0.7）、TD3密集奖励（-3.5 ± 0.3 vs 全局矩阵-4.7 ± 0.2）和TD3稀疏奖励（-6.9 ± 0.5 vs 全局矩阵-6.4 ± 0.5）下均显著优于其他表示。在PickAndPlaceOrient任务中，局部切空间表示的成功率达到69.8%，显著高于旋转矩阵的54.1%、四元数的46.7%和欧拉角的32.3%。缩放切向量至最大允许角度可将最终平均奖励提升1.5至2倍并降低方差。需要指出的是，本文仅研究了连续动作空间的on-policy和off-policy算法，未涉及离散动作空间或扩散策略等更复杂的策略参数化，且PickAndPlaceOrient任务的成功率仍较低（最高69.8%），表明全姿态控制仍具挑战性。

在深度强化学习中，将连续动作空间扩展到SO(3)旋转群面临一个根本性的拓扑障碍：SO(3)流形不存在全局光滑、无奇点的最小参数化。这意味着任何将$\mathbb{R}^3$映射到SO(3)的参数化都必然在某些点附近出现奇异性或非双射性。常见的SO(3)动作表示——欧拉角、四元数、旋转矩阵、李代数坐标——各自引入了不同的几何偏差，而这些偏差在强化学习的随机策略和探索噪声下被放大，直接影响探索动力学、熵正则化的有效性以及训练稳定性。

现有方法的缺口在于，尽管SO(3)表示在机器人学和控制理论中已有深入研究，但它们在深度强化学习中的系统比较和设计原则仍然缺失。具体而言，动作表示的选择不仅决定了策略网络输出的维度、约束类型和奇异性位置，还通过以下因果机制影响学习效果：**表示的选择（特别是全局 vs 增量、是否投影、是否居中）决定了高斯采样或探索噪声在流形上的分布形态，进而影响策略梯度的方差和熵奖励项的计算正确性。** 例如，欧拉角的万向锁导致某些方向上的探索被压缩；四元数的双覆盖导致SAC和TD3的评论家学习到双峰Q值；全局旋转矩阵的投影操作在PPO中导致概率比不匹配，造成显著性能损失。

本文的动机是填补这一系统性研究的空白，核心洞察是：**将动作表示为局部坐标系中的切向量（delta tangent vector in local frame）能够天然解决多个关键问题。** 这种表示天然居中于单位旋转（即网络输出零向量对应无动作），便于通过缩放限制动作幅度以避开切空间的割迹（cut locus），在小角度下近似于delta欧拉角但无奇异性。实验证据表明，局部切空间增量表示在理想化旋转环境、无人机轨迹跟踪与竞速、以及RoboSuite机械臂基准上几乎总是取得最佳最终策略，且运行间方差最小。此外，密集奖励可以缓解表示特定的失败模式，而稀疏奖励则会放大这些差异。

## 核心方法与创新机理

本文的核心创新不在于提出全新的深度强化学习算法，而在于对**SO(3)动作表示**进行了系统性的实证比较与分析，揭示了不同表示在强化学习探索动力学、熵正则化及训练稳定性中的因果机制，并提炼出一套实用的设计原则。其核心洞察在于：**动作表示的选择是一个关键的因果旋钮（causal knob），它直接决定了探索偏差、熵正则化的有效性以及训练的稳定性，而不仅仅是后处理问题。**

### 关键瓶颈与因果机制

文章识别的根本瓶颈是：**SO(3)流形不存在全局光滑、无奇点的最小参数化**。这意味着所有常见表示（欧拉角、四元数、旋转矩阵、李代数）在作为强化学习动作空间时，都会引入不同的病态特性：
- **欧拉角**：存在万向锁（gimbal lock）和奇异性，导致在奇点附近动作空间“缠绕”，产生非各向同性的探索偏差，且熵正则化失效。
- **四元数**：存在双覆盖（double-cover）问题，即`q`和`-q`代表同一旋转。这导致评论家（critic）学习到双模态Q值分布，破坏值函数估计的稳定性。
- **全局旋转矩阵**：虽然光滑且唯一，但其9维输出空间包含严格的约束（正交性和单位行列式），强制投影会改变动作概率分布，尤其对PPO这类依赖概率比（probability ratio）的on-policy算法造成严重破坏。
- **李代数坐标（ε_τ）**：作为全局切向量，在远离单位旋转时存在割迹（cut locus），导致大角度动作的表示不连续。

### 核心创新：局部切空间增量动作表示

针对上述瓶颈，文章提出的核心方案是**局部切空间增量动作表示（Local Tangent Vector Delta Action Representation, 记为 $^s \tau$）**。其核心思想是：将动作表示为**当前姿态局部坐标系下的切向量**，而非全局旋转参数。这带来了四个关键改变（changed slots）：

1.  **动作表示类型**：从全局参数（旋转矩阵、四元数等）改为局部增量切向量。这天然地将动作空间“居中”于单位旋转，避免了全局参数化的奇异性问题。在小角度下，它近似于delta欧拉角，但无奇异性。
2.  **单位旋转居中（Unit-Rotation Centering）**：在策略网络输出中显式添加单位旋转偏置（即 `action_mean = network_output + identity_rotation`）。这确保了策略初始时输出零均值动作对应于“不旋转”，而非一个随机旋转，极大地改善了初始探索效率。实验表明，这对PPO的delta四元数和矩阵表示有显著提升。
3.  **动作缩放（Action Scaling）**：将切向量的范数限制在最大允许角度 $\alpha_{max}$ 内。这避免了切空间在远离原点处的割迹问题，将动作空间限制在一个无奇点的局部区域。实验证明，缩放可将最终平均奖励提升1.5到2，并显著降低方差。
4.  **投影策略（Projection Strategy）**：针对投影破坏概率比的问题，文章提出**在策略网络内部投影均值**，而在**环境端投影采样动作**。这样在计算对数概率时，使用的是投影前的分布，避免了PPO中概率比不匹配导致的性能损失。SAC不受此影响，因为其动作概率是实时重算的。

### 实验证据与性能优势

文章在理想化旋转环境、无人机轨迹跟踪/竞速、以及RoboSuite机器人操作基准上进行了广泛验证。决定性证据表明：
- **$^s \tau$ 几乎在所有设置下都取得了最佳策略**，且运行间方差最小（Table 2, Figure 4, 6）。在理想化环境中，$^s \tau$ 在SAC和TD3的密集/稀疏奖励下均显著优于其他表示（如SAC稀疏奖励下，$^s \tau$ 的奖励为-7.9，而全局矩阵为-29.4）。
- **全局矩阵表示（R）** 在多数情况下表现次优，但**在SAC与稀疏奖励的组合下严重失效**（Table 2），这归因于其投影操作与稀疏奖励的交互放大了探索困难。
- **缩放是性能的关键**：未缩放的 $^s \tau$ 在少数运行中会因大角度动作而失败，缩放则消除了这一问题（Figures 10-12）。
- **PPO对投影敏感**：投影采样动作会显著损害PPO性能，但对SAC无影响（Figure 8）。

### 局限性

- 研究仅限于连续动作空间的on-policy（PPO）和off-policy（SAC, TD3）算法，未涉及离散动作空间或扩散策略。
- 在复杂的全姿态控制任务（PickAndPlaceOrient）中，即使最佳表示的成功率也仅为69.8%，表明该问题仍具挑战性。
- 单位旋转居中在SAC和TD3上的效果不一致，其背后的原因尚待进一步研究。

该论文的核心贡献在于系统性地揭示了深度强化学习中 SO(3) 动作表示选择与算法性能之间的因果机制。其整体框架并非提出一个全新的算法，而是构建了一个用于诊断和比较不同 SO(3) 动作表示的实验与分析方法论。

**核心瓶颈与因果旋钮**

论文的底层逻辑建立在 SO(3) 流形的一个基础性数学事实之上：**不存在一个全局光滑、无奇异点的最小参数化**。这意味着所有常见的动作表示（欧拉角、四元数、旋转矩阵、李代数）都不可避免地引入某种形式的偏差或奇异性。这个瓶颈是理解所有后续实验结果的出发点。

由此，论文将问题简化为几个关键的 **因果旋钮**：
1.  **动作表示类型**：选择全局（直接输出旋转）还是增量（输出相对于当前姿态的变化）表示。
2.  **策略输出与流形的交互方式**：网络输出是欧几里得空间中的向量，必须通过投影（Projection）映射到 SO(3) 流形上。这个投影过程会如何影响强化学习的核心机制（如 PPO 的概率比、SAC 的熵正则化）？
3.  **动作缩放与居中**：对于切空间表示，是否对网络输出的切向量进行缩放（限制最大旋转角度）和居中（使零输出对应单位旋转）？

**Pipeline 与模块关系**

整个框架的流程可以抽象为以下模块：

1.  **策略网络 (Actor Network)**：这是一个标准的深度神经网络（如前馈网络），其输出是欧几里得空间中的一个向量。这是所有动作表示的共同起点。论文明确指出：“Feedforward policies produce Euclidean outputs that do not satisfy manifold constraints by construction.”

2.  **投影层 (Projection Layer)**：这是框架的核心模块，负责将网络的原生输出转换为合法的 SO(3) 元素。不同的动作表示对应不同的投影策略：
    *   **旋转矩阵**：通过 SVD 分解将 3x3 矩阵投影到最近的旋转矩阵：`R = U diag(1, 1, det(UV^T)) V^T`。
    *   **四元数**：通过 L2 归一化使四元数模长为 1。
    *   **欧拉角**：通过 `tanh` 函数将角度限制在特定范围内。
    *   **切向量**：直接作为 SO(3) 李代数 $\mathfrak{so}(3)$ 中的元素，通过指数映射 `Exp` 转换为旋转。

    论文的关键发现之一在于，**投影的位置**至关重要。对于 PPO，如果对采样后的动作进行投影，会导致用于计算重要性采样权重的概率比不匹配，从而造成严重的性能损失。因此，推荐在**网络内部对均值进行投影**，而在**环境端对采样后的动作进行投影**，以保证对数概率的可计算性。

3.  **环境动力学 (Environment Dynamics)**：该模块根据动作类型应用环境状态更新：
    *   **全局动作**：策略直接输出一个目标姿态 $R_a$，环境以最大步长 $\alpha_{max}$ 沿测地线朝向该姿态旋转。
    *   **增量动作**：策略输出一个相对于当前姿态的旋转变化量 $\Delta R_{\Delta a}$，环境更新为 $R_{t+1} = R_t \Delta R_{\Delta a}$。

4.  **奖励函数 (Reward Function)**：论文使用了两种奖励设置来放大不同表示间的差异：
    *   **密集奖励**：`r_t = -d(R_t, R_g)`，其中 $d(R_1, R_2) = \operatorname{arccos}\left( \frac{\operatorname{tr}(R_1^\top R_2) - 1}{2} \right)$ 是测地距离。密集奖励能提供连续的梯度信号，可以缓解某些表示带来的问题。
    *   **稀疏奖励**：当姿态误差小于 0.1 弧度时奖励为 0，否则为 -1。稀疏奖励会放大表示缺陷导致的探索失败，使不同表示的性能差异更加显著。

**输入输出流**

*   **输入**：观测空间 $s$，包含当前姿态 $R_t$ 和/或目标姿态 $R_g$ 的表示。
*   **输出**：动作 $a$，经过投影层和环境动力学后，驱动环境状态转移。
*   **反馈**：奖励 $r_t$ 和新状态 $s_{t+1}$，用于更新策略网络和值函数网络。

**证据强度与失败模式**

论文通过一系列精心设计的消融实验（Ablation Studies）来验证其因果假设，这些实验构成了框架的关键证据：
*   **动作缩放**：限制切向量范数至 $\alpha_{max}$ 能显著提升性能和稳定性，将最终平均奖励提升 1.5 到 2 倍，并降低方差（见 Figures 10, 11, 12）。这直接验证了避免切空间割迹（cut locus）的重要性。
*   **单位旋转居中**：在策略网络输出中添加单位旋转偏置，对 PPO 的 delta 四元数和矩阵表示有显著提升，但对 SAC 和 TD3 效果不一。这个结果需要手动验证其背后的原因，论文本身也未完全解释。
*   **投影策略**：对 PPO 而言，对采样动作进行投影是灾难性的（Figure 8）。而对 SAC 则影响不大，因为其动作概率是实时重新计算的。
*   **四元数双覆盖**：SAC 和 TD3 的评论家网络会学到因四元数 $q$ 和 $-q$ 表示同一旋转而产生的双峰 Q 值（Figure 13），这解释了为何基于四元数的全局表示在这些算法中表现不佳。

**核心洞察**

综合所有证据，论文得出的最可靠结论是：**将动作表示为局部坐标系中的切向量（Local Tangent Vector Delta Action Representation）** 能提供最稳定和最优的性能。其优势在于：
1.  **天然居中**：网络输出零自然对应单位旋转，避免了额外的偏置处理。
2.  **便于缩放**：可以方便地限制切向量范数，从而避开切空间的割迹，避免大角度跳跃。
3.  **无奇异性**：在小角度下近似于 delta 欧拉角，但避免了欧拉角的万向锁问题。

然而，该框架也存在局限性。在更复杂的机器人任务（如 PickAndPlaceOrient）中，即使使用最佳表示，成功率也仅为 69.8%，表明全姿态控制仍具挑战性。此外，论文未涉及离散动作空间或扩散策略等更复杂的策略参数化，这些是重要的开放问题。

### 1. SO(3)流形与动作表示的基本约束

旋转动作的本质约束源于SO(3)流形的拓扑结构。SO(3)定义为所有满足正交性和单位行列式的3×3旋转矩阵的集合：

$$\mathrm{SO(3)} = \{ R \in \mathbb{R}^{3 \times 3} \mid R^{\top} R = I, \det R = 1 \}$$

该流形的一个核心瓶颈在于：**不存在从 $\mathbb{R}^3$ 到 $\mathrm{SO(3)}$ 的全局光滑、双射且无奇点的最小参数化**。这意味着所有常见的动作表示（欧拉角、四元数、旋转矩阵、李代数坐标）都会在全局范围内引入某种形式的奇异性、非唯一性或冗余约束。Table 1总结了这些性质：欧拉角存在万向锁（gimbal lock），四元数具有双覆盖（double cover，即q与-q表示同一旋转），旋转矩阵是唯一且光滑的但维度冗余（9维），李代数切向量在小角度下光滑但在大角度下存在割迹（cut locus）。

### 2. 核心公式：环境动力学与奖励

论文在理想化旋转环境中定义了统一的动力学和奖励函数，以隔离动作表示的影响。

**测地距离**：两个旋转之间的角度距离由下式计算：

$$d(R_1, R_2) = \operatorname{arccos}\left( \frac{\operatorname{tr}(R_1^{\top} R_2) - 1}{2} \right)$$

**密集奖励**：当前姿态 $R_t$ 与目标姿态 $R_g$ 之间的负角度：

$$r_t^{\mathrm{dense}} = -d(R_t, R_g)$$

稀疏奖励则在 $d(R_t, R_g) \leq 0.1$ 时为零，否则为-1。

**全局动作的动力学**：对于全局动作（网络直接输出目标旋转 $R_a$），环境以最大步长 $\alpha_{max}$ 沿最短路径更新姿态：

$$R_{t+1} = \left\{ \begin{array}{ll} R_a, & \mathrm{if~} d(R_t, R_a) < \alpha_{max} \\ R_t \mathrm{Exp}\left( \frac{\alpha_{max}}{d(R_t, R_a)} \mathrm{Log}\left( R_t^{-1} R_a \right) \right), & \mathrm{otherwise} \end{array} \right.$$

对于delta动作（网络输出增量旋转 $\Delta R$），动力学简化为 $R_{t+1} = R_t \Delta R$。

### 3. 投影层与概率比不匹配

由于策略网络输出欧几里得空间中的原始向量，必须将其投影到SO(3)流形上。对于旋转矩阵，使用SVD投影到最近的旋转矩阵：

$$R = U \mathrm{diag}\big(1, 1, \mathrm{det}(U V^{\top})\big) V^{\top}$$

该投影是可微的，可作为网络层插入。然而，**在PPO中对采样动作进行投影会导致严重性能损失**，因为PPO的裁剪替代目标中使用的概率比 $\frac{\pi_\theta(\mathbf{a}|\mathbf{s})}{\pi_{\theta_{old}}(\mathbf{a}|\mathbf{s})}$ 不再匹配未投影动作的概率比。SAC则不受影响，因为动作概率在策略更新时在线重新计算。

### 4. 局部切空间增量表示

论文推荐的局部切空间增量动作（delta tangent vector in local frame）的核心设计包含三个关键机制：

1. **单位旋转居中（Unit-Rotation Centering）**：在策略网络输出中添加单位旋转偏置，使网络输出的零向量天然映射到无动作（单位旋转），避免探索初期产生随机大角度跳跃。

2. **动作缩放（Action Scaling）**：将切向量范数限制在最大允许角度 $\alpha_{max}$ 范围内。缩放避免了切空间在大角度下的割迹问题，实验表明缩放可将最终平均奖励提升1.5到2，并显著降低方差。

3. **投影策略**：在策略网络内部投影均值，在环境端投影采样动作。这保持了PPO的对数概率可计算性，同时确保动作始终在流形上。

### 5. 策略参数化与熵正则化

PPO和SAC使用squashed高斯策略：

$$\pi_\theta(\mathbf{s}) = \tanh(\mathbf{u} \sim \mathcal{N}(\mu_\theta(\mathbf{s}), \sigma_\theta(\mathbf{s})))$$

标准熵奖励项为：

$$\mathcal{H}(\pi_\theta(\cdot|s) = \frac{1}{2} \sum_{i=1}^4 \log(2\pi e \sigma_i^2(s))$$

这里的关键因果机制是：**熵正则化假设动作空间是欧几里得的**，而SO(3)流形上的实际分布熵（需要在球面 $S(3)$ 上积分）与高斯熵不同。这导致不同表示下熵正则化的实际效果产生偏差，尤其当切向量未缩放时，网络可能通过增大方差来"欺骗"熵奖励，产生超出物理允许范围的大角度动作。

### 6. 关键公式变量含义汇总

| 符号 | 含义 |
|------|------|
| $R \in \mathrm{SO(3)}$ | 3×3旋转矩阵 |
| $d(R_1, R_2)$ | 测地距离（弧度） |
| $\alpha_{max}$ | 最大允许旋转步长 |
| $R_a$ | 网络输出的目标旋转（全局动作） |
| $\Delta R$ | 增量旋转（delta动作） |
| $\mathrm{Exp}(\cdot)$ | 指数映射：李代数→李群 |
| $\mathrm{Log}(\cdot)$ | 对数映射：李群→李代数 |
| $\mu_\theta(s), \sigma_\theta(s)$ | 高斯策略的均值和标准差 |
| $q_I, I$ | 单位四元数和单位矩阵（用于居中偏置） |

## 实验与关键发现

### 主结果：局部切空间增量动作表示在几乎所有设置中表现最佳

本文在理想化旋转环境、无人机轨迹跟踪/竞速以及RoboSuite机器人基准上系统评估了多种SO(3)动作表示。**核心结论明确且一致：局部切空间增量动作表示（delta tangent vector in local frame，记为 $^s\tau$）在几乎所有算法和奖励设置中均取得最佳或次优的最终策略性能，且运行间方差最小**（Table 2, Figure 4, Figure 6, 置信度0.95）。

![[assets/figures/papers/iclr26_0003_g4ZrpMQL1Z_A_Primer_on_SO3_Action_Representations_in_Deep_R/figures/003_Table_2.jpg]]
*Table 2: Results for the idealized rotation environment*

在理想化旋转环境中（Table 2），局部切向量表示在SAC密集奖励（-2.9 ± 0.3）、SAC稀疏奖励（-7.9 ± 0.8）、TD3密集奖励（-3.5 ± 0.3）和TD3稀疏奖励（-6.9 ± 0.5）下均为最佳。PPO密集奖励下与全局矩阵表示持平（-5.4 ± 0.2）。**稀疏奖励场景下优势尤为突出**：SAC稀疏奖励中，全局旋转矩阵（R）仅达到-29.4 ± 0.7，而局部切向量为-7.9 ± 0.8，差距超过20分；TD3稀疏奖励中，全局矩阵为-6.4 ± 0.5，切向量为-6.9 ± 0.5，差距较小但切向量方差更低。

在更复杂的机器人基准中（Figure 4），无人机轨迹跟踪和竞速任务上局部切向量表示同样获得最高奖励。在PickAndPlaceOrient任务（Figure 6）中，局部切空间表示的成功率达到69.8%，显著优于旋转矩阵（54.1%）、四元数（46.7%）和欧拉角（32.3%），且收敛速度更快。

**全局旋转矩阵表示通常位列第二**，但在SAC稀疏奖励中表现极差（-29.4 ± 0.7），表明其与off-policy算法在稀疏奖励下的交互存在根本性问题。四元数表示在RoboSuite部分任务中（Figure 5）优于矩阵表示，但在理想化环境中表现不佳。欧拉角在几乎所有设置中表现最差，仅在PPO密集奖励下例外（置信度0.9）。

![[assets/figures/papers/iclr26_0003_g4ZrpMQL1Z_A_Primer_on_SO3_Action_Representations_in_Deep_R/figures/008_Figure_5.jpg]]
*Figure 5: Achieved reward across the RoboSuite benchmark as a fraction of the maximum possible reward. Error bars denote the standard deviation across five seeds*

### 消融研究：缩放、居中与投影的影响

**切向量缩放（Scaling）** 是局部切空间表示的关键改进。将切向量范数限制在最大允许角度 $\alpha_{\text{max}}$ 内，可使最终平均奖励提升1.5到2，并显著降低方差（Figures 10, 11, 12，置信度1.0）。缩放的核心机制是避免切空间的割迹（cut locus）：当动作范数接近 $\pi$ 时，指数映射的逆映射不唯一，导致梯度不稳定。缩放确保动作始终位于指数映射的双射区域内。

**单位旋转居中（Unit-rotation centering）** 的效果因算法而异。在PPO中，对delta四元数和矩阵表示添加单位旋转偏置（即网络输出加上恒等旋转）能显著提升性能（Figure 3，置信度0.9）。但在SAC和TD3上效果不一致（Figures 22-27），部分设置甚至出现退化。这种差异的成因尚未完全明确，可能与off-policy算法中Q函数对居中偏置的响应不同有关。

**动作投影（Projection）** 对PPO和SAC的影响截然不同（Figure 8，置信度0.95）。在PPO中，投影采样动作会导致显著的性能损失，根本原因是投影改变了动作的概率密度，使得PPO的截断代理目标中的概率比 $\frac{\pi_\theta(\mathbf{a}|\mathbf{s})}{\pi_{\theta_{\text{old}}}(\mathbf{a}|\mathbf{s})}$ 不再匹配实际采样分布。SAC则不受影响，因为其动作概率在策略更新时在线重新计算，投影在计算之后应用。这一发现表明，对于PPO，应在策略网络内部投影均值，在环境端投影采样动作，以保持对数概率的可计算性。

### 失败模式与机制分析

**四元数双覆盖导致Q值双峰分布**（Figure 13，置信度1.0）：由于 $q$ 和 $-q$ 表示同一旋转，SAC和TD3的评论家学习到的Q值在四元数空间中出现对称双峰。这导致Q函数的多模态性，增加了评论家估计的不确定性，进而影响策略优化。这是四元数表示在off-policy算法中表现不佳的核心机制。

**欧拉角的奇异性与缠绕效应**（Figure 9，置信度1.0）：在奇点（如俯仰角 $\pm\pi/2$）附近，高斯采样的分布被"缠绕"到流形上，导致实际探索方向与期望方向严重偏离。HER回放缓冲区中存储的目标姿态分布进一步放大了这种偏差，形成恶性循环。

**投影动作的分布畸变**（Figure 7，置信度0.9）：不同表示的投影操作产生截然不同的噪声分布。旋转矩阵的SVD投影产生接近均匀的分布；切向量投影集中在边界；四元数投影在小噪声下均匀；欧拉角投影则集中在奇点附近。这些畸变直接影响探索效率和策略学习。

**全局矩阵在SAC稀疏奖励中的失效**：尽管全局矩阵表示光滑且唯一，但在SAC稀疏奖励下表现极差（Table 2）。这可能与SAC的熵正则化机制有关：在稀疏奖励下，策略倾向于保持高熵，而全局矩阵表示的高维输出空间（9维）使得熵正则化难以有效引导探索，导致策略在无效区域徘徊。

### 6D表示与其它变体

6D表示（Zhou et al., 2019）在理想化环境中的表现与标准旋转矩阵相似，差异较小（Figures 28-31，置信度1.0）。在PPO中使用绝对动作时，6D表示略微优于矩阵表示；但在delta动作下表现逊色。在TD3中，标准矩阵表示通常更优。这种差异可能源于6D表示的Gram-Schmidt过程对噪声的敏感性，但需要进一步验证。

**Delta vs 全局动作**：在理想化环境中，delta矩阵表示始终低于全局矩阵表示（Table 2的详细数据），尽管两者都是光滑且唯一的。这一反直觉的结果表明，增量动作的局部性优势（避免全局奇异性）在某些情况下被增量更新带来的误差累积所抵消。

![[assets/figures/papers/iclr26_0003_g4ZrpMQL1Z_A_Primer_on_SO3_Action_Representations_in_Deep_R/figures/001_Table_1.jpg]]
*Table 1: Properties of common $\mathrm { S O ( 3 ) }$ representations used for actions*

![[assets/figures/papers/iclr26_0003_g4ZrpMQL1Z_A_Primer_on_SO3_Action_Representations_in_Deep_R/figures/067_Table_3.jpg]]
*Table 3: Number of runs per environment for hyperparameter optimization*

## 定位与知识库关联

本文系统性地将SO(3)流形上的动作表示问题纳入深度强化学习的设计空间，填补了此前动作表示选择缺乏系统性指导的空白。其核心贡献在于揭示了不同表示方式如何通过探索偏差、熵正则化失效和训练不稳定这三个机制影响策略学习，并给出了明确的实用建议。

**与baseline/follow-up的关系**：本文直接对比了五种主流SO(3)表示——旋转矩阵、四元数、欧拉角、李代数坐标和6D表示（Zhou et al., 2019），覆盖了全局动作和增量动作两种模式。实验设计的关键公平性在于：所有表示共享相同的网络架构、训练预算和超参数调优流程（贝叶斯优化），仅改变动作表示。这使得结果能够归因于表示本身的属性，而非实现差异。值得注意的是，6D表示（Zhou et al., 2019）的表现与标准旋转矩阵高度相似，差异小于算法间的方差，说明该表示并未带来实质性改善。这一发现对后续研究者有警示意义：不应默认更复杂的参数化必然带来性能提升。

**适用边界**：本文的结论在以下范围内成立——连续动作空间、标准on-policy（PPO）和off-policy（SAC、TD3）算法、最大步长受限（α_max）的旋转控制任务。核心推荐（局部切空间增量向量）的优越性在三个基准上得到验证：理想化旋转环境（控制变量）、无人机轨迹跟踪/竞速（动态环境）、RoboSuite操作任务（高维接触动力学）。特别是PickAndPlaceOrient任务中，局部切空间表示的成功率（69.8%）显著优于旋转矩阵（54.1%）和四元数（46.7%），表明在需要完整姿态控制的任务中，表示选择的影响被放大。

**关键局限**：
1. **离散动作空间未覆盖**：本文明确将离散动作算法（如DQN）排除在外，而SO(3)的离散化方案（如均匀采样、球面编码）本身就是一个开放问题，可能改变表示之间的相对优劣。
2. **策略参数化局限**：仅研究了高斯策略和squashed高斯策略（tanh）。扩散策略等具有多模态输出能力的策略，其噪声过程和分布特性可能使不同表示的差距缩小或反转。
3. **机器人基准的成功率天花板**：即使使用最佳表示，PickAndPlaceOrient任务的成功率仍低于70%，说明全姿态控制本身仍是挑战性问题，表示优化只是解决方案的一部分。
4. **单位旋转居中的不一致性**：该技巧在PPO上显著改善delta四元数和矩阵的性能，但在SAC和TD3上效果混合。这一现象的原因尚未被解释，可能与off-policy算法的经验回放分布特性有关。

**开放问题**：
- **delta矩阵vs全局矩阵的悖论**：在理想化环境中，delta矩阵（增量旋转矩阵）始终低于全局矩阵，尽管两者都是光滑且唯一的。这与“局部表示优于全局表示”的整体结论矛盾，暗示可能存在未被识别的交互机制（如累积误差或梯度路径长度）。
- **投影策略的算法依赖性**：投影动作样本对PPO造成显著性能损失（概率比不匹配），但对SAC无影响。这一差异的深层原因——PPO的clipped surrogate objective对分布偏移更敏感——已被识别，但缺乏理论分析。
- **标准化基准缺失**：目前缺乏一个被广泛接受的、需要完整SO(3)控制的基准套件。本文使用的理想化环境和RoboSuite任务各有局限，前者过于简化，后者任务难度天花板低。一个标准化的基准将极大促进该方向的系统比较。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Primer_on_SO3_Action_Representations_in_Deep_Reinforcement_Learning.pdf

![[paperPDFs/ICLR_2026/A_Primer_on_SO3_Action_Representations_in_Deep_Reinforcement_Learning.pdf]]
