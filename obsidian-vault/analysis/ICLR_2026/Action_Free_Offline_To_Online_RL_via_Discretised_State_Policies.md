---
title: "Action-Free Offline-To-Online RL via Discretised State Policies"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Action_Free_Offline_To_Online_RL_via_Discretised_State_Policies.pdf
aliases:
- ODOSODQN
- AFOORDSP
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/batch_offline
core_operator: "将状态变化离散化为{增大、减小、不变}，利用集成解耦Q学习在此离散动作式空间中学习状态策略，并通过保守正则化约束状态可达性。"
primary_logic: "学习预测离散状态转移而非直接输出动作，使从仅含(s,r,s')的无动作数据中预训练有效状态策略成为可能，再结合在线学习时从头训练的逆动力学模型和策略切换机制，实现离线知识向在线决策的高效迁移。"
claims:
- "OSO-DecQN在离线评估中显著优于BC和DecQN变体，尤其是在低质量数据集上。"
- "消融实验表明离散化和正则化是预训练有效性的关键组件。"
- "引导在线学习机制在多种环境与数据集上均能加速训练并提升最终性能。"
- "Hopper-medium-replay (D4RL) 上 Normalised Average Return = 65.7 ± 2.6 (OSO-DecQN)"
---

# Action-Free Offline-To-Online RL via Discretised State Policies

> [!tip] 核心洞察
> 学习预测离散状态转移而非直接输出动作，使从仅含(s,r,s')的无动作数据中预训练有效状态策略成为可能，再结合在线学习时从头训练的逆动力学模型和策略切换机制，实现离线知识向在线决策的高效迁移。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于离散状态策略的无动作离线到在线强化学习 |
| 英文题名 | Action-Free Offline-To-Online RL via Discretised State Policies |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=TImzB3SxUO) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/batch_offline |
| Method | OSO-DecQN (Offline State-Only Decoupled Q-Network) |
| Dataset | Hopper-medium-replay (D4RL), Walker2D-medium (guided online, 1M steps) |

> [!tip] 效果简介
> - Hopper-medium-replay (D4RL) 上，Normalised Average Return 为 65.7 ± 2.6 (OSO-DecQN)，对比 26.6 (BCa)，变化 +39.1。
> - Walker2D-medium (guided online, 1M steps) 上，Normalised Online Return 为 ~120 (OSO-DecQN)，对比 ~80 (TD3)，变化 +40。

## 概述

实际离线强化学习面临一个致命瓶颈：大量离线数据集由于隐私、存储或传感器限制而缺失动作标签，仅包含 $(s, r, s')$ 三元组，导致传统离线 RL 方法无法直接应用。本文针对这一"无动作"离线到在线 RL 设定，提出一种基于离散状态策略的方法 **OSO‑DecQN (Offline State-Only Decoupled Q-Network)**。

**核心思路** 是将状态变化方向离散化为 $\{-1,0,1\}$（分别对应减小、不变、增大），在离散状态差异空间上学习状态策略，从而无需访问任何动作信息即可完成离线预训练。该离散化方案通过 z-score 归一化实现尺度不变性，并配合集成解耦 Q 网络与**保守正则化**，使预训练策略能够从仅含状态-奖励-下一状态的数据中安全地学习。在线阶段，则通过从头训练的**逆动力学模型（IDM）**将离散状态建议转化为可执行动作，并采用概率混合（策略切换）机制，将离线知识高效注入在线学习。

**主要结果**显示，OSO‑DecQN 在离线评估中显著优于行为克隆和 DecQN 变体，尤其在低质量数据集上优势突出；在线引导学习能一致地加速收敛并提升终局性能，超越 TD3 以及已有的无动作引导方法。消融实验进一步证实离散化粒度和保守正则化是取得这些效果的关键组件。

## 背景与动机

在连续控制任务中，离线强化学习（Offline RL）允许智能体从预先收集的静态数据集中学习策略，而无需与环境进行在线交互。这避免了在线探索带来的安全风险和采集成本，因此在实际部署中具有重要价值。然而，标准离线 RL 方法普遍要求数据集以四元组形式组织：$(\text{状态}, \text{动作}, \text{奖励}, \text{下一状态})$，即必须包含明确的动作标签。

**动作缺失瓶颈**：在许多现实场景中，这一要求往往难以满足。动作标签可能因以下原因缺失或被刻意移除——

- **隐私与合规限制**：医疗、教育等领域的交互数据可能涉及个人行为细节，只允许保留状态层面的观测记录。
- **存储与传输带宽约束**：传感器节点或边缘设备可能仅上传状态快照，丢弃高频动作日志以降低存储和通信开销。
- **传感器限制**：仅能观测系统状态而无法记录控制指令，例如从视频重建的轨迹数据。

**由此产生的是"无动作离线 RL"（action-free offline RL）的核心难题**：如何在只有 $(s, r, s')$ 三元组的条件下，学习一个有效的策略？传统行为克隆（如 BCa）需要动作标签进行拟合，因此无法直接迁移到此类数据集上。这一缺口催生了对全新学习范式的需求——策略必须仅从状态转移规律和奖励信号中推导出决策逻辑，而不依赖已标注的动作示例。

现有的无动作方法（如 Zhu 等人提出的 AF-Guide）尝试利用决策变换器（Decision Transformer）和内在奖励引导机制来桥接离线知识与在线微调。但此类方法的预训练阶段计算开销较大，且完全回避在离线阶段建模可执行的动作语义，导致其在引导在线学习时的效果不稳定（图2显示 AF-Guide 在多项任务中甚至弱于基线 TD3）。

**本文的核心动机**正是填补这一空白：设计一种无需动作标签即可高效预训练的状态策略，并构建一套从离线知识向在线决策迁移的完整机制。与直接预测连续动作或下一状态不同，本文的关键直觉在于——**策略只需学会预测状态的离散变化方向**（各维度是增大、减小还是不变）。这一视角将连续动作空间中的高维回归问题转化为低维分类问题，使其既能从稀疏的状态差异中提取有效信号，又能通过推理原始状态转移中的因果关系来推导所需动作，从而在无动作的离线数据集上开辟出一条可行的学习路径。

## 核心创新

OSO-DecQN 的核心创新围绕一个核心瓶颈展开：**实际离线数据集常缺失动作标签**（因隐私、存储或传感器限制），使传统离线RL方法无法直接应用。该方法通过四个紧密耦合的模块将"无动作离线数据"转化为可用的强先验，显著提升了离线预训练与在线微调的性能。

**瓶颈与因果链条：**
缺失动作标签意味着无法直接学习状态-动作值函数 $Q(s,a)$。OSO-DecQN 的关键洞察是将优化目标从"直接预测动作"转换为"预测离散状态转移方向"。它首先将状态变化通过 z-score 归一化后离散化为三元向量 $\Delta s \in \{-1,0,1\}^M$（参见公式 $\delta_i^{\epsilon}(s, s')$），以便从纯净的 $(s,r,s')$ 元组中学习 $Q(s,\Delta s)$，从根本上规避了对动作标签的依赖。

**关键创新点**（changed slots vs. baselines）：

1.  **动作空间重构为离散状态差：**
    与 BCa 等基线使用原始连续动作 $a$ 不同，OSO-DecQN 将动作定义为"状态维度的增减方向" $\Delta s$。这一离散化表示具有 z-score 归一化带来的**尺度不变性**，使模型能跨任务泛化；同时也降低了策略搜索空间的复杂度（置信度1.0，锚点 Sec 4.1）。消融实验证实，离散化粒度与容忍阈值 $\epsilon$ 是预训练有效性的关键组件：用 3 类离散化（增/减/不变）优于 2 类，且设置 $\epsilon=0$（消除"不变"区域）会损害性能（置信度0.9-0.95，锚点 Table 9, Table 10）。

2.  **解耦式状态Q函数与保守正则项：**
    Q 网络从 $Q(s,a)$ 的分解形式（$Q_{\theta}(s, \mathbf{a}) = \frac{1}{N} \sum_{j=1}^{N} U_{\theta_j}^j(s, a_j)$）迁移至 $Q(s, \Delta s)$ 的独立维度分解（置信度1.0，锚点 Sec 4.2）。同时，引入了一项适配离散域的**保守正则化损失** $\mathcal{R}_{\theta} = \sum_{(s,\Delta s)\sim\mathcal{D}} \log\|\exp(Q_{\theta}(s,\cdot))\|_1 - Q_{\theta}(s,\Delta s)$，其等价于行为克隆的负对数似然，强制约束 Q 值估计在离线数据的支持范围内，**有效抑制了对分布外状态的过估计**（置信度1.0，锚点 Sec 4.3）。消融显示，缺少该正则项会导致回报急剧下降与严重过估计（置信度0.85，锚点 Table 1 与 Sec 6 讨论）。

3.  **基于"翻译器"的离线-在线引导机制：**
    离线预训练的状态策略无法直接输出可执行动作。OSO-DecQN 设计了一个**轻量级逆动力学模型（IDM）** $I_{\phi}(s, \Delta s)$，仅在在线阶段从零训练，充当从状态建议到连续动作的"翻译器"。在线决策通过一个**概率切换策略** $\beta$ 进行控制：以概率 $\beta$ 使用 IDM 翻译的离线建议动作，否则执行在线策略的动作（置信度1.0，锚点 Sec 4.4）。实验证据表明，这一引导机制不仅加速了训练，更提升了最终性能。例如，在 Walker2D-medium 任务上，OSO-DecQN 引导的在线学习回报比 TD3 基线高出约 40 分（置信度0.9，锚点 Figure 7）。进一步消融发现，**线性衰减的 $\beta$ 调度**优于任何固定 $\beta$ 值，说明早期大量使用离线先验、后期逐步放权给在线学习是最优策略（置信度0.9，锚点 Figure 3, Sec D.3）。

**创新有效性总结：**
上述创新共同实现了"从无动作状态数据预训练有效策略，再高效迁移至在线决策"的完整闭环。在离线评估中，OSO-DecQN 在 Hopper-medium-replay 上获得 65.7 的归一化平均回报，远超行为克隆基线 BCa 的 26.6（置信度0.95，锚点 Table 1）。其核心性能提升来自**离线状态策略本身**，而非 IDM 的具体架构；IDM 的自举训练项对整体平均回报有正向贡献（115.8 vs. 112.7），但并非性能主因（置信度0.95，锚点 Table 14, Sec E 讨论）。需要手动验证的是：该方法在高维复杂动态系统（如灵巧手操作）上的效果尚未被充分检验。

## 整体框架

OSO‑DecQN 由离线预训练与在线引导两个阶段构成，整体输入为一个 **无动作标签** 的离线数据集
$\mathcal{D}_{\text{off}} = \{(s, r, s')\}$，输出是能够直接用于在线交互的策略。其核心洞察在于：
将状态转移离散化为 $\{-1,0,1\}^M$，使强化学习可以在纯粹的状态变化空间中进行，从而绕过缺失动作标签的限制；
在线阶段再经由一个轻量的逆动力学模型和策略切换机制，将离线学到的状态变化建议翻译成可执行动作。

### 1. 状态差异离散化

对离线数据中的每一对 $(s, s')$，先对每个状态维度进行 z-score 归一化以消除量纲影响，
再将原始差分按阈值 $\epsilon$ 映射为三元离散值 $\Delta s \in \{-1,0,1\}^M$：

$$
\delta_i^{\epsilon}(s, s') = \begin{cases}
-1 & \text{if } s_i' - s_i < -\epsilon \\
 1 & \text{if } s_i' - s_i >  \epsilon \\
 0 & \text{otherwise.}
\end{cases}
$$

该步骤将无动作数据转化为"状态变化类别"标签，为后续在离散动作空间上的 Q 学习提供了监督信号。
（对应模块：状态差异离散化模块，Section 4.1。）

### 2. 状态策略离线预训练（OSO‑DecQN）

将离散化后的 $(s,\Delta s, r, s')$ 作为训练数据，OSO‑DecQN 在离散状态差异空间上训练一个
**集成解耦 Q 网络**。网络输出拆分为每个状态维度的独立效用函数 $U_{\theta}^j(s,\Delta s_j)$，
最终 $Q(s,\Delta s) = \frac{1}{N}\sum_{j=1}^{N} U_{\theta_j}^j(s,\Delta s_j)$，
采用 n 步 TD 误差：

$$
\mathcal{L}(\theta) = \frac{1}{|B|}\sum_{(s_0,\Delta s_0, r_{0:n-1}, s_n)\in B} L\big(y^n - Q_\theta(s_0,\Delta s_0)\big).
$$

为缓解离线数据分布外（OOD）的过估计，引入一个适应离散域的保守正则项，等价于行为克隆的负对数似然：

$$
\mathcal{R}_\theta = \sum_{(s,\Delta s)\sim\mathcal{D}} \log\|\exp(Q_\theta(s,\cdot))\|_1 - Q_\theta(s,\Delta s).
$$

最终目标函数为 $\mathcal{L}(\theta) + \alpha \mathcal{R}_\theta$。预训练完成后，策略通过
$\arg\max_{\Delta s} Q(s,\Delta s)$ 输出下一步的状态变化建议。
（对应模块：离线状态策略预训练，Section 4.2–4.3，Algorithm 1。）

### 3. 逆动力学模型与在线引导

在线阶段并不直接使用离线训练出的 Q 网络执行动作，因为真实环境期望的是连续动作 a。为此引入一个
**逆动力学模型（IDM）** $I_\phi$，它从 $(s,\Delta s)$ 映射到动作 a，并随在线交互持续学习。
IDM 本身是轻量的：在文献的消融实验（Table 12）中，其网络层数和小批次大小对最终性能影响不敏感，
且损失曲线（Figure 4）快速收敛至与专家模型相近的水平，表明翻译任务并非性能瓶颈。

动作选择由策略切换机制决定：以概率 $\beta$ 使用 IDM 翻译离线策略的建议，
否则执行在线算法自身的策略 $\pi_{\text{on}}$：

$$
\mathbf{a} = \begin{cases}
I_\phi\big(s, \arg\max_{\Delta s} Q(s,\Delta s)\big) & \text{if } \zeta < \beta,\\
\pi_{\text{on}}(s) & \text{otherwise.}
\end{cases}
$$

其中 $\beta$ 可以是固定值或线性衰减至零（图 3 及 Section D.3 中显示退火 $\beta$ 可获得更好的最终回报）。
在线算法可对接任意 model‑free 算法（如 TD3、SAC 或 DecQN_N），形成统一的离线到在线迁移框架。
（对应模块：逆动力学模型、策略切换引导，Section 4.4。）

综上，OSO‑DecQN 的数据流为：
离线 $\{(s,r,s')\}$ → 离散化 $\rightarrow (s,\Delta s,r,s')$ → 预训练 Q 网络 → 离线状态策略
→ 在线阶段：IDM 翻译 + $\beta$‑混合 → 最终执行动作。整套 pipeline 不依赖动作标签，使无动作的离线数据可直接驱动后续的强化学习。

## 核心模块与公式推导

OSO‑DecQN 的整体流程可拆解为四个顺序耦合的模块：① 状态差异离散化，将原始转移数据转化为可学习的离散动作；② 离线状态策略预训练，在离散空间上学习保守的 Q 函数；③ 在线逆动力学建模，将状态差异建议翻译为可执行动作；④ 策略切换引导，通过概率衰减将离线知识足量注入在线训练。

### 状态差异离散化

实际数据集仅提供三元组 $(s, r, s')$，缺少动作 $a$。为了构造可优化的离散动作空间，对每一个状态维度 $i$ 先应用 z‑score 标准化（使变化量尺度无关），再引入容忍阈值 $\epsilon$，将相邻状态之差映射为三元指示量：

$$
\delta_i^\epsilon(s, s') =
\begin{cases}
-1 & \text{if } s_i' - s_i < -\epsilon \\
 1 & \text{if } s_i' - s_i > \epsilon \\
 0 & \text{otherwise}.
\end{cases}
$$

**变量含义**：$s, s'$ 为已标准化的一对状态；$\epsilon$ 是"无变化区域"的宽度，避免微小涨落产生虚假符号翻转；输出 $\Delta s \in \{-1,0,1\}^M$，其中 $M$ 为状态维度。  
该模块是动作标签缺失下可学习性的核心：定理 1 证明，将连续增量按 $k$ 个均匀区间离散化后，最优值函数误差上界满足 $\|V^* - V_D^*\|_\infty = \mathcal{O}\!\left(\frac{H\sqrt{M}}{k}\right)$，随维度 $M$ 和规划步长 $H$ 增大而上升，随格点数 $k$ 增大而下降。

### 离线状态策略预训练

预训练模块学习形如 $Q(s, \Delta s)$ 的集成解耦 Q 网络。借鉴 DecQN 的分解思想，将联合 Q 值表达为各维度效用函数的均值：

$$
Q_\theta(s, \Delta s) = \frac{1}{N} \sum_{j=1}^{N} U_{\theta_j}^j(s, \Delta s_j),
$$

其中每个效用分支 $U_{\theta_j}^j$ 只负责预测第 $j$ 维的离散值 $(-1,0,1)$ 的偏好。采用 n 步时间差分损失更新（与标准 DQN 类似，仅将动作 $a$ 替换为 $\Delta s$），目标形式为：

$$
y^n = r + \gamma r_{t+1} + \cdots + \gamma^{n-1} r_{t+n-1} + \gamma^n \max_{\Delta s'} Q_{\theta^-}(s_{t+n}, \Delta s').
$$

**关键创新**：为防止在离线数据覆盖不足的 $\Delta s$ 区域出现过估计，加入**保守正则项**，显式约束策略只停留在数据支撑集内：

$$
\mathcal{R}_\theta = \sum_{(s,\Delta s)\sim\mathcal{D}} \log\!\left\| \exp\!\big(Q_\theta(s,\cdot)\big) \right\|_1 - Q_\theta(s, \Delta s).
$$

该正则项等价于在软最大策略下的负对数似然，迫使对观测到的 $\Delta s$ 赋予更高 Q 值而对其他组合压低。完整的预训练损失为 TD 误差与 $\alpha \mathcal{R}_\theta$ 的加权和（$\alpha$ 为超参数）。消融实验（Table 1 无正则化行）证实，缺少 $\mathcal{R}_\theta$ 会导致性能急剧恶化。

### 逆动力学模型

离线学到的状态策略直接给出的是目标状态差异 $\Delta s^*$，而非实际环境可执行的动作。因此在线阶段引入一个小型逆动力学模型（IDM） $I_\phi(s, \Delta s)$，通过监督回归预测从 $s$ 过渡到 $s'$ 所需的动作 $a$。IDM 以轻量网络实现，训练数据来自在线交互中实际观察到的 $(s, a, s')$ 三元组，损失为均方误差。IDM 本身不是 OSO‑DecQN 的核心性能来源，其引导效果通过表 14 的消融得到确认：加入 IDM 自举项仅能带来约 3 个点的全领域平均收益提升。

### 策略切换引导

在线训练时，以概率 $\beta$ 调用离线策略建议（IDM 翻译后负责）与从零训练的在线策略 $\pi_{\mathrm{on}}$，执行方式为：

$$
\mathbf{a} =
\begin{cases}
I_\phi\big(s, \arg\max_{\Delta s} Q(s,\Delta s)\big) & \text{if } \zeta < \beta \\
\pi_{\mathrm{on}}(s) & \text{otherwise},
\end{cases}
$$

其中 $\zeta \sim \mathcal{U}(0,1)$，$\beta$ 可采用固定值或线性退火（Figure 3 显示退火策略在"Walker2d"和"Hopper"上均优于固定 $\beta$）。随着在线策略逐步成熟，$\beta$ 衰减便实现了离线知识到自主决策的平滑移交。

## 实验与分析

### 离线预训练效果
OSO‑DecQN 在仅使用无动作 $(s,r,s')$ 数据离线训练后，已能获得远超行为克隆的回报。以 Hopper‑medium‑replay 为例，OSO‑DecQN 归一化平均回报达到 65.7±2.6，而 BCa（使用动作的行为克隆）仅为 26.6，提升 39.1 分（Table 1）。该方法在 HalfCheetah‑medium 和 Walker2D‑medium‑replay 等任务上也一致地超越 BCΔs（状态差异克隆）和不带保守正则化的 DecQN 变体，证实直接预测离散状态变化方向可以从无动作数据中提取出有效策略。

![[assets/figures/papers/iclr26_0006_TImzB3SxUO_Action-Free_Offline-To-Online_RL_via_Discretised/figures/009_Table_1.jpg]]
*Table 1: Normalised average returns on D4RL and Factorised action tasks. Scores are averaged across 5 seeds with 10 episodes per seed. Ensemble-based methods use N = 5 . Where relevant, we report the mean ± standard error*

状态策略的预测能力在 Table 2 中得到量化：在 Hopper‑medium‑expert 上平均离散差异误差仅 0.16，接近专家水平，而随机策略的预期误差为 0.76。这表明离散化后的 Q 学习能够准确捕捉状态转移的结构，并为后续在线引导提供可靠的建议信号。

### 在线引导学习性能
将离线预训练的 OSO‑DecQN 集成到在线训练中，通过逆动力学模型将建议的状态差翻译为可执行动作，显著加速了学习并提升了最终性能。Figure 1 展示了在 Cheetah‑Run 等任务上的在线学习曲线：无论预训练数据质量是 random‑medium‑expert、medium‑expert 还是 expert，OSO‑DecQN 引导的训练在 1M 步内均快于仅使用在线算法（DecQN\_N），且最终回报更高。在 Walker2D‑medium 任务上，OSO‑DecQN 引导的在线算法达到约 120 的归一化回报，而纯 TD3 约为 80（Figure 7），表明从离线数据中提炼的知识对在线探索有实质性帮助。

![[assets/figures/papers/iclr26_0006_TImzB3SxUO_Action-Free_Offline-To-Online_RL_via_Discretised/figures/005_Figure_1.jpg]]
*Figure 1: Online learning curves comparing the performance of guided online learning with state policies pre-trained on datasets of different qualities against baselines over 1M timesteps. The solid line corresponds to the mean normalised return across 5 seeds with the shaded area corresponding to 1 standard deviation away from the mean*

![[assets/figures/papers/iclr26_0006_TImzB3SxUO_Action-Free_Offline-To-Online_RL_via_Discretised/figures/037_Figure_7.jpg]]
*Figure 7: Normalised online returns (mean ± s.e. over 5 seeds) for Hopper, HalfCheetah and Walker2D across different dataset qualities. We plot AF-Guide, TD3 and OSO-DecQN on the same axes. OSO-DecQN consistently achieves comparable or higher final performance than AF-Guide*

与另一无动作方法 AF‑Guide 的直接对比显示 OSO‑DecQN 的优越性：在同一组 D4RL 环境中，OSO‑DecQN 引导一致地取得与或高于 TD3 的最终性能，而 AF‑Guide 的表现经常低于 TD3 基线（Figure 2, Figure 7）。这表明基于 Q 学习的离散状态策略比基于决策变压器的方案更适合此类引导任务。

### 关键组件消融

**离散化粒度与 ε 容忍区。**  
状态差的离散化方式对性能至关重要。Table 10 对比了 2 区间（仅在增大/减小二分类）与 3 区间（{−1,0,1}）的表现，发现 3‑bin 离散化在次优数据集（如 medium‑replay）上始终持平或更优。进一步地，ε 参数决定了声明"无变化"的容忍区间：当 ε=0（无容忍）时，离散化对归一化后的微小波动过于敏感，导致性能显著恶化（Table 9）。这说明合理的"不变"区间是维持状态预测稳定性和策略泛化的必要条件。

![[assets/figures/papers/iclr26_0006_TImzB3SxUO_Action-Free_Offline-To-Online_RL_via_Discretised/figures/018_Table_10.jpg]]
*Table 10: Comparing the performance of our algorithm when discretising ∆s using two and three bins*

![[assets/figures/papers/iclr26_0006_TImzB3SxUO_Action-Free_Offline-To-Online_RL_via_Discretised/figures/017_Table_9.jpg]]
*Table 9: Ablation studying the effects of varying ϵ. Results averaged across 3 seeds ± 1 s.e*

**保守正则化。**  
Table 1 中移除保守正则项 $\mathcal{R}_{\theta}$ 的 DecQN 变体会出现严重的回报下降和过估计，直接证明了该正则项对约束状态预测在数据支撑内的关键作用。正则项的形式

$$
\mathcal{R}_{\theta} = \sum_{(s,\Delta s)\sim\mathcal{D}} \log\|\exp(Q_{\theta}(s,\cdot))\|_1 - Q_{\theta}(s,\Delta s)
$$

相当于对每个样本约束 Q 值的分布集中到数据中的 $\Delta s$ 上，从而抑制对分布外状态差的错误高估。

**逆动力学模型与引导机制。**  
IDM 作为轻量翻译器，其引导项在在线阶段带来正向收益：在所有域上的全模型平均回报为 115.8，而去除 IDM 引导项的消融版本为 112.7（Table 14）。IDM 本身的架构（2–4 层网络）和批大小对最终性能影响不大，且 IDM 损失在线训练过程中快速收敛（Figure 4），收敛后的损失与在专家数据上训练的 IDM 损失处于同一水平（Table 13），说明 IDM 不是性能瓶颈，主要增益来源于离线预训练的状态策略。

引导时的策略切换概率 β 的调度方式也经过消融检验：线性退火的 β 在 Walker2D 和 Hopper 上最终性能均优于固定 β 值（Figure 3）。随着在线策略逐步改进，逐渐减少对离线建议的依赖可以更好地平衡早期引导与后期自主探索。

![[assets/figures/papers/iclr26_0006_TImzB3SxUO_Action-Free_Offline-To-Online_RL_via_Discretised/figures/022_Figure_3.jpg]]
*Figure 3: Comparison of fixed versus linearly annealed β in guided online learning for Walker2D and Hopper*

### 值得注意的不足与待验证点
论文未系统报告失败模式，但从消融实验可提取以下需要留意的方面：
- 当 ε 设置不当（如 0）时性能坍塌，表明方法对离散化阈值极为敏感，在实际部署前需根据环境调试。
- 离散化仅为 3 个区间，对上界定理 ($\| V^* - V_D^* \|_{\infty} = \mathcal{O}(H\sqrt{M}/k)$）的更细粒度收益未能充分探索；在精细控制要求极高的任务中可能不够。
- 所有实验在 MuJoCo/DMControl 运动类任务上完成，未涉及图像输入或稀疏奖励场景，因此其在视觉或高维观测任务中的有效性仍需手动验证。

## 方法谱系与知识库定位

OSO‑DecQN 定位在"无动作标签的离线到在线强化学习"这一新兴子方向。不同于依赖动作数据的行为克隆（BC）或保守 Q 学习，它通过离散化状态转移方向来构造可 Q 评价的离散动作空间，从而在仅含 (s, r, s′) 的离线数据集上预训练有用的状态策略，并借助轻量逆动力学模型（IDM）将状态策略的建议翻译为在线可执行的动作，实现离线知识的快速迁移。

### 与现有工作的关系

OSO‑DecQN 的核心架构继承自 DecQN 体系，但对其三个关键设计槽位进行了"无动作化"替换，由此发展出与先前方法不同的能力（参见 changed_slots）：

- **相对于行为克隆变体**：BCa 在无动作数据上不可用；BCΔs 虽可直接拟合连续状态变化，却缺乏价值引导与保守性约束，在低质量数据集（如 Hopper‑medium‑replay）上性能远低于 OSO‑DecQN（BCa: 26.6 vs OSO‑DecQN: 65.7±2.6，见 Table 1）。OSO‑DecQN 通过将状态差离散化为 {−1,0,1}，结合集成解耦 Q 网络与保守正则化，在无动作的条件下实现了对状态轨迹的有效价值评估与约束。
- **相对于 AF‑Guide**：Zhu et al. (2023) 提出的 AF‑Guide 使用决策 Transformer 和内在奖励引导进行无动作离线学习，但其结构复杂且训练慢。在与 TD3 基线的对比中（Figure 2），AF‑Guide 的引导在线学习反而劣于纯 TD3，而 OSO‑DecQN 则稳定地提升样本效率和最终性能（如在 Walker2D‑medium 上提升约 +40 归一化回报，见 Figure 7）。同时，OSO‑DecQN 不使用 Transformer，预训练耗时大幅减少，说明在无动作约束下，基于离散化状态差异的 Q 学习方法比序列生成模型更精简有效。
- **相对于有动作的离线到在线方法**：OSO‑DecQN 不属于策略蒸馏或保守更新框架，而是通过"状态建议 → IDM 翻译 → 动作执行"的路径，将离线学到的状态层面偏好注入在线策略。这一准则与 AWAC、IQL 等离线到在线算法形成互补，且在 Walker2d 任务上已展现与这些强基线可比的表现（Figure 6），证明了无动作转移的可能性和竞争力。

因此，OSO‑DecQN 在方法树上可视作 DecQN 的"离散状态策略"变体，并在无动作离线预训练和轻量在线引导两个层面，构成了独立且优于现有无动作基线的新分支。

### 适用边界

从实验覆盖范围与理论分析看，OSO‑DecQN 的有效性成立需要满足以下条件：

- **任务形态**：主要适用于连续控制中的运动任务（MuJoCo、DMControl），尤其是在动作空间可因子化（各维度独立）且状态变化方向与动作方向之间存在相对平滑映射的环境。离散化带来的值函数误差由 Theorem 1 给出界 $\mathcal{O}(H\sqrt{M}/k)$，当状态维度 $M$ 较小或离散化箱数 $k$ 足够时，误差可控。
- **数据要求**：离线数据必须包含奖励信号（r），暂不能仅从纯状态序列（如视频）中学习；数据质量可以从随机到专家不均，甚至在次优数据（如 medium‑replay 子集）上，OSO‑DecQN 仍保持显著优势。但如果数据集中大量轨迹的动力学特性高度随机或不可逆，离散化方向可能掩盖细节，导致状态预测误差扩大（如 Cheetah‑Run medium‑expert 上误差达 1.6，见 Table 2），此时的引导效果可能衰减。
- **状态表示**：离散化依赖各维度独立且经 z‑score 归一化后可有效区分变化方向。对耦合剧烈或非欧几里得状态空间（如图像嵌入），现有离散化范式需要扩展，这是该方法向视觉‑运动领域转移的瓶颈。

### 局限与开放问题

尽管性能显著，该方法仍存在几个固有局限，且对应着值得深入探究的方向。

**当前已知局限：**
1. **离散化粒度的固定性**：始终采用 3 箱 {−1,0,1} 的离散化方案。消融已经表明 3 箱优于 2 箱（Table 10），且引入 ε 容忍区有利于抗噪，但不能自适应任务需求。对于需要精细幅度控制的场景，固定粗粒度离散化会带来不可忽略的价值误差。
2. **IDM 性能的依赖性**：在线阶段 IDM 负责将离散状态建议翻译为动作。虽然该模块轻量且训练收敛快（Figure 4），但如果环境动态高度非线性或动作与状态差之间存在多模态映射，IDM 误差可能积累，降低引导收益。消融实验（Table 14）也显示加入 IDM 自举项能提升平均回报，表明翻译精度对整体性能有可度量的影响。
3. **额外的计算开销**：OSO‑DecQN 需要完整的离线预训练环节，相较纯在线方法增加了一轮计算成本（Table 8 展示 Hopper 上预训练 + 在线共约 4.7 小时），对于计算敏感的应用场景不够经济。
4. **奖励信号的硬性需求**：方法无法从无奖励的 (s,s′) 对中学习价值函数，限制了对纯状态序列日志或视频的应用鸿沟。

**开放研究问题：**
- 能否引入**自适应离散化**机制，根据上下文或值函数精度动态调节箱数和 ε 阈值，以平衡学习精度与计算复杂性？
- 若将离散状态策略与**价值函数分类框架**（如 cross‑entropy 值支撑）结合，能否进一步提高评论家训练的稳定性和可扩展性（见 Part 004 的讨论）？
- 如何从**视觉观测**中提取有意义的状态差表示，使该方法可服务于端到端的无动作视觉 RL 管道？
- 面对环境动态随机性较高的任务，是否可用**概率离散表示**（例如预测 Δs 属于各类的概率分布）替代确定性分类，以增强策略鲁棒性？
- 在线引导中 β 的手工衰减方案虽优于固定 β（Figure 3），但其**自动化调节**（如基于 IDM 损失或策略分歧）是否能进一步提升最终性能和通用性？

综合来看，OSO‑DecQN 为无动作离线到在线 RL 开辟了一个基于离散状态策略的轻量范式，但在复杂感知与更精细的动作控制方面，仍有广阔的拓展空间。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Action_Free_Offline_To_Online_RL_via_Discretised_State_Policies.pdf

![[paperPDFs/ICLR_2026/Action_Free_Offline_To_Online_RL_via_Discretised_State_Policies.pdf]]
