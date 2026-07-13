---
title: "Mean Flow Policy with Instantaneous Velocity Constraint for One-step Action Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Mean_Flow_Policy_with_Instantaneous_Velocity_Constraint_for_One_step_Action_Generation.pdf
project_link: null
code_link: null
openreview_forum_id: mIeKe74W43
aliases:
- MVPM
- MFPIVCOSAG
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入瞬时速度约束（IVC）为平均流恒等式提供丢失的边界条件，迫使积分常数为零，消除多解性。"
primary_logic: "用平均速度场替代瞬时速度场实现一步动作生成，并通过IVC解决学习不适定性，在保持生成多样性的同时大幅提升训练与推理效率。"
claims:
- "定理2与定理3证明：IVC显式提供边界条件，消除平均流恒等式的多解性，迫使累积误差为零。"
- "在Robomimic和OGBench共9个任务中，MVP在8个任务上达到或超越最新水平，平均成功率达0.88±0.05。"
- "消融实验表明，IVC系数与成功率正相关，λ=1.0时将Cube-triple-task4的成功率从0.30±0.21提升至0.52±0.11。"
- "一步动作生成使MVP的训练速度（153.6 iter/s）大幅超越多步流基线（如BFN 68.0 iter/s），推理时间（10.93ms）与最快基线相当且远优于多数基线。"
---

# Mean Flow Policy with Instantaneous Velocity Constraint for One-step Action Generation

> [!tip] 核心洞察
> 用平均速度场替代瞬时速度场实现一步动作生成，并通过IVC解决学习不适定性，在保持生成多样性的同时大幅提升训练与推理效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 带瞬时速度约束的平均流策略用于一步动作生成 |
| 英文题名 | Mean Flow Policy with Instantaneous Velocity Constraint for One-step Action Generation |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=mIeKe74W43) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Mean Velocity Policy (MVP) |
| Dataset | Robomimic-lift, Robomimic-can, Robomimic-square, Cube-double-task2 |

> [!tip] 效果简介
> - Robomimic-lift 上，Success Rate 为 1.00 ± 0.00，对比 1.00 ± 0.01 (BFN)，变化 0.00。
> - Robomimic-can 上，Success Rate 为 0.92 ± 0.07，对比 0.94 ± 0.06 (QC)，变化 -0.02。
> - Robomimic-square 上，Success Rate 为 0.93 ± 0.01，对比 0.92 ± 0.01 (QC)，变化 +0.01。

## 概要

机器人操作中的动作生成面临一个核心瓶颈：现有基于流匹配的策略依赖多步迭代采样，导致训练与推理效率低下；同时，在训练平均速度场时缺乏显式边界条件，造成常微分方程（ODE）的多解问题，损害策略的表达能力。

针对上述问题，本文提出**平均速度策略（Mean Velocity Policy, MVP）**。其核心思路是用平均速度场替代瞬时速度场，实现从高斯噪声到动作分布的一步生成，从而大幅提升训练与推理效率。为解决平均流恒等式因缺少边界条件而导致的学习不适定性，进一步引入**瞬时速度约束（Instantaneous Velocity Constraint, IVC）**，显式提供缺失的边界条件，迫使积分常数为零，消除多解性。理论分析表明，IVC 能保证累积误差在理想情况下收敛于零（定理2与定理3，详见第3.2节）。

在实验验证上，MVP 在两个具有挑战性的机器人操作基准——Robomimic 和 OGBench——共9个任务中，于8个任务上达到或超越现有最佳水平，平均成功率达 0.88 ± 0.05（Table 1）。同时，一步生成的设计使 MVP 的在线训练速度达到 153.6 iter/s，大幅领先多步流基线（如 BFN 的 68.0 iter/s）；CPU 推理时间仅需 10.93 ms，与最快的一步基线相当，远优于多数多步基线（Table 2、Table 3）。消融实验证实，IVC 系数与成功率呈正相关，λ = 1.0 时将 Cube-triple-task4 的成功率从 0.30 ± 0.21 提升至 0.52 ± 0.11（Table 4、Figure 4）。

在方法谱系上，MVP 位于离线到在线强化学习与流基策略的交汇点。相比基于行为克隆后蒸馏的 **FQL**（Park et al., 2025）、Best-of-N 采样的 **BFN**（Ghasemipour et al., 2021）以及引入动作分块的 **QC**（Li et al., 2025）等多步流基线，MVP 的关键差异在于：生成步数从多步压缩为单步，速度场类型从瞬时速度场改为平均速度场，并通过 IVC 损失提供显式边界条件。策略改进则采用 Best-of-N 生成与基于 Q 值的选择机制，与模仿训练解耦。

当前工作的主要局限在于仅在仿真基准上验证，尚未在真实机器人平台部署；训练中计算 Jacobian-vector product（JVP）可能增加 GPU 内存开销；IVC 系数虽不敏感，但仍需手动设定。未来方向包括扩展到更高维动作空间、探索避免 JVP 计算的近似方案，以及在真实环境中验证性能。



### 机器人操作中的策略学习困境

在长周期、稀疏奖励的机器人操作任务中，学习表达能力强且采样效率高的策略函数是核心挑战。当前主流方法可分为两大范式：**行为克隆（BC）** 直接从专家演示中学习确定性映射，但难以捕获多模态动作分布；**扩散/流基策略**通过迭代去噪过程建模复杂的动作分布，在多模态任务上表现优异，却面临严重的效率瓶颈。

### 流基策略的效率瓶颈

现有流基策略（如 **FQL**、**BFN**、**QC**）依赖多步迭代采样生成动作。具体而言，这些方法需要从噪声分布出发，通过求解常微分方程（ODE）逐步演化至目标动作分布，通常需要10步甚至更多的网络前向传播。这导致两个关键问题：

1. **训练效率低下**：每次策略更新都需要完整的迭代采样过程，在线训练速度受限于采样步数。例如，BFN 的在线训练速度仅为 68.0 iter/s，QC 进一步降至约 41 iter/s。
2. **推理延迟高**：实际部署时，多步采样造成显著的推理延迟。BFN 和 QC 的 CPU 推理时间分别高达 117.3ms 和 113.2ms，难以满足实时控制需求。

### 平均流匹配的学习不适定性

一个直觉的加速思路是直接学习**平均速度场**（mean velocity field），实现从噪声到动作的一步映射。然而，这一思路面临深层理论障碍：从平均速度的定义出发，可以推导出**平均流恒等式**（mean flow identity）：

$$-u(a(t), t, r, s) + (r-t) \frac{d}{dt} u(a(t), t, r, s) = -v(a(t), t, s)$$

该恒等式将平均速度场 $u$ 与瞬时速度场 $v$ 关联，是训练监督信号的基础。但问题在于：**该恒等式缺乏显式边界条件，存在无穷多解**。具体而言，任何满足该恒等式的 $u$ 加上一个任意常数 $C$ 仍然是有效解，这导致学习目标不适定，累积误差无法被有效约束，严重损害策略的表达能力。

### 本文动机

针对上述问题，本文提出 **Mean Velocity Policy（MVP）**，核心动机是：

- **效率侧**：用平均速度场替代瞬时速度场，实现单步动作生成，从根本上消除迭代采样开销；
- **表达力侧**：引入**瞬时速度约束（IVC）**，为平均流恒等式显式提供边界条件，迫使积分常数为零，消除多解性，确保策略保持强表达力。

这一设计使得 MVP 在保持流基策略多模态建模能力的同时，大幅提升训练与推理效率，为机器人操作中的策略学习提供了一种高效且表达力强的替代方案。



## 核心方法与创新机理

MVP 的核心创新在于用**平均速度场**替代传统流策略的**瞬时速度场**，实现一步动作生成，并通过**瞬时速度约束（IVC）**解决平均流恒等式的多解性问题，从而在保持高表达力的同时大幅提升训练与推理效率。

### 从瞬时速度到平均速度：一步生成的数学基础

传统流基策略（如 **FQL** (Park et al., 2025)、**BFN** (Ghasemipour et al., 2021)）建模瞬时速度场 $v(a(t), t, s)$，需要沿时间轴进行多步迭代采样（通常10步）才能从噪声生成动作。MVP 转而建模平均速度场：

$$u(a(t), t, r, s) \triangleq \frac{1}{r-t} \int_t^r v(a(\tau), \tau, s) d\tau$$

这一设计使得策略推理只需单步完成：$a(1) = a(0) + u(a(0), 0, 1, s)$，其中 $a(0) \sim \mathcal{N}(0, I)$。生成步数从多步缩减为单步（**changed slot：生成步数**），消除了昂贵的迭代采样过程。

### IVC：为平均流恒等式提供缺失的边界条件

平均速度场的训练依赖从定义导出的**平均流恒等式**：

$$-u(a(t), t, r, s) + (r-t) \frac{d}{dt} u(a(t), t, r, s) = -v(a(t), t, s)$$

然而，该恒等式本身缺乏显式边界条件，导致训练时存在多解问题——不同的 $u$ 函数可能满足相同的恒等式，损害策略表达力。这是 MVP 方法设计的核心瓶颈。

**IVC 的因果作用**：在 $t=r$ 的边界上，平均速度应退化为瞬时速度，即 $u(a(t), t, t) = v$。IVC 将这一物理约束显式化为训练目标：

$$\mathcal{L}_{\mathrm{IVC}}(\theta) = \mathbb{E}_{t, a(t)} \left\| u_\theta(a(t), t, t) - v \right\|_2^2$$

定理2和定理3（Section 3.2）证明：IVC 显式提供边界条件，迫使积分常数为零，消除平均流恒等式的多解性（**changed slot：边界条件**）。最终策略损失为：

$$\mathcal{L}_{\mathrm{policy}}(\theta) = \mathcal{L}_{\mathrm{MF}}(\theta) + \lambda \mathcal{L}_{\mathrm{IVC}}(\theta)$$

### 策略改进的解耦：Best-of-N 与 Q 值引导

传统离线到在线 RL 方法直接最大化 Q 值或依赖行为克隆进行策略改进。MVP 采用 Best-of-N 机制：从策略采样 $N$ 个候选动作，用 Critic $Q_\phi$ 选择 Q 值最高的动作执行（**changed slot：策略改进机制**）。定理1（Eq. 13）将性能提升分解为 Best-of-N 改进项 $\Delta_1$ 与拟合误差项 $\Delta_2$，为解耦模仿训练与策略改进提供了理论保证。

### 创新点的证据强度

| 创新点 | 关键证据 | 置信度 |
|--------|----------|--------|
| 平均速度场实现一步生成 | Eq. (6-7)；训练速度 153.6 iter/s vs BFN 68.0 iter/s（Table 2） | 0.98 |
| IVC 消除多解性 | 定理2/3（Section 3.2）；消融实验 $\lambda=1.0$ 将 Cube-triple-task4 成功率从 0.30 提升至 0.52（Table 4） | 0.97 |
| Best-of-N 策略改进 | 定理1（Eq. 13）；9 任务中 8 个达到或超越 SOTA（Table 1） | 0.95 |

**需人工验证**：IVC 系数 $\lambda$ 虽不敏感，但默认值 1.0 为手动选择，缺乏自适应机制。训练中 JVP 计算可能增加 GPU 内存消耗，在资源受限环境下需额外评估。



MVP（Mean Velocity Policy）的整体框架围绕**平均速度场建模**与**Best-of-N策略改进**两条主线展开，包含离线预训练与在线微调两个阶段，核心模块及其交互关系如下。

### 模块构成与职责

- **平均速度模型 $u_\theta$**：建模平均速度场 $u(a(t), t, r, s)$，实现从基高斯噪声到动作的**单步生成**。给定状态 $s$，采样 $a(0) \sim \mathcal{N}(0, I)$，一步映射得到动作 $a(1) = a(0) + u_\theta(a(0), 0, 1, s)$。训练时通过最小化平均流恒等式残差 $\mathcal{L}_{\mathrm{MF}}(\theta)$（Eq. 9）和瞬时速度约束 $\mathcal{L}_{\mathrm{IVC}}(\theta)$（Eq. 15）的联合损失 $\mathcal{L}_{\mathrm{policy}}(\theta)$（Eq. 19）来学习。

- **Critic $Q_\phi$**：估计动作值函数 $Q(s, a)$，为候选动作的Best-of-N选择提供打分依据。训练采用标准TD-error（Eq. 20），从回放缓冲区的转移样本 $(s_k, a_k, r_k, s_{k+1})$ 上优化。

- **瞬时速度约束（IVC）**：作为边界条件嵌入策略训练损失中，约束在区间端点 $t$ 处平均速度等于已知瞬时速度，即 $\mathcal{L}_{\mathrm{IVC}}(\theta) = \mathbb{E}_{t, a(t)} \| u_\theta(a(t), t, t) - v \|_2^2$。IVC显式提供平均流恒等式（Eq. 8）缺失的边界条件，迫使积分常数为零，消除ODE多解问题，是保障策略表达力的关键机制。

### 输入输出流

1. **离线预训练阶段**：利用离线数据集预训练平均速度模型 $u_\theta$ 和Critic $Q_\phi$。策略通过 $\mathcal{L}_{\mathrm{policy}}$ 学习平均速度场，Critic通过TD-error学习值函数。

2. **在线交互与微调阶段**：在每个决策步，策略从噪声采样 $N$ 个候选动作 $\{a_i\}_{i=1}^N$，经Critic打分后选择 $Q$ 值最高的动作执行，实现Best-of-N策略改进。交互数据存入回放缓冲区，交替优化策略和Critic。

### 效率优势的根源

传统流基策略依赖多步迭代采样（如10步），训练中每步需反复调用速度模型，推理时同样需要多步积分。MVP用平均速度场替代瞬时速度场，将动作生成压缩为**单步映射**，从根源上消除了迭代采样的计算开销。这一设计使在线训练速度达到153.6 iter/s，较BFN（68.0 iter/s）提升2.2倍以上；CPU推理时间仅10.93ms，与最快的单步基线相当，远低于BFN（117.3ms）和QC（113.2ms）。



### 3.1 平均速度策略（Mean Velocity Policy, MVP）

现有流基策略的核心瓶颈在于依赖多步迭代采样：从噪声分布逐步演化到动作分布需要反复调用速度网络，训练和推理效率均受拖累。MVP 的根本改造是将建模对象从**瞬时速度场** $v(a(t), t, s)$ 切换为**平均速度场** $u(a(t), t, r, s)$，定义为瞬时速度在区间 $[t, r]$ 上的均值：

$$u(a(t), t, r, s) \triangleq \frac{1}{r-t} \int_t^r v(a(\tau), \tau, s) d\tau \quad \text{(Eq. 6)}$$

这一替换使策略推理退化为单步映射：给定基高斯噪声 $a(0) \sim \mathcal{N}(0, I)$，最终动作直接由 $a(1) = a(0) + u_\theta(a(0), 0, 1, s)$ 生成，彻底消除迭代采样开销。

训练 $u_\theta$ 不能直接使用流匹配损失，因为没有现成的平均速度真值。作者从 Eq. 6 对 $t$ 求导，导出**平均流恒等式**（Mean Flow Identity）：

$$-u(a(t), t, r, s) + (r-t) \frac{d}{dt} u(a(t), t, r, s) = -v(a(t), t, s) \quad \text{(Eq. 8)}$$

该恒等式将未知的平均速度 $u$ 与已知的瞬时速度 $v$ 联系起来，为训练提供监督信号。据此构造平均流匹配损失：

$$\mathcal{L}_{\mathrm{MF}}(\theta) = \mathbb{E}_{t, r<t, a(t)} \bigg\| u_\theta(a(t), t, r, s) - \mathrm{sg}\left( v - (t-r) \frac{d}{dt} u_\theta(a(t), t, r, s) \right) \bigg\|_2^2 \quad \text{(Eq. 9)}$$

其中 $\mathrm{sg}(\cdot)$ 为停止梯度操作，避免训练不稳定。右侧目标项本质是 Eq. 8 移项后的结果，用当前 $u_\theta$ 的雅可比-向量积（JVP）近似 $\frac{d}{dt}u_\theta$。

### 3.2 瞬时速度约束（Instantaneous Velocity Constraint, IVC）

Eq. 8 作为微分方程存在多解问题：若某个 $u$ 满足该恒等式，则 $u + C/(r-t)$（$C$ 为任意常数）同样满足。这意味着仅靠 $\mathcal{L}_{\mathrm{MF}}$ 无法唯一确定 $u_\theta$，导致学习不适定，损害策略表达力。

**定理 2** 与**定理 3**（Section 3.2）证明：在 $t = r$ 处施加边界条件 $u(a(t), t, t) = v(a(t), t, s)$ 可迫使积分常数 $C = 0$，消除多解性。这正是 IVC 的理论动机——为平均流恒等式提供缺失的边界条件。

IVC 损失定义为在 $t$ 处预测的平均速度与已知瞬时速度的 L2 距离：

$$\mathcal{L}_{\mathrm{IVC}}(\theta) = \mathbb{E}_{t, a(t)} \left\| u_\theta(a(t), t, t) - v \right\|_2^2 \quad \text{(Eq. 15)}$$

该约束迫使模型在区间端点处精确匹配瞬时速度，从而在整个区间上逼近唯一解。

### 3.3 策略改进与整体损失

策略改进采用 Best-of-N 机制：从当前策略 $\pi_{\text{old}}$ 采样 $N$ 个候选动作，由 Critic $Q_\phi$ 选择 Q 值最高的动作构成新策略 $\pi_{\text{new}}$。**定理 1** 将新旧策略的性能差分解为两项下界：

$$V^{\pi_{new}}(s) - V^{\pi_{old}}(s) \ge \underbrace{\mathbb{E}_{\tau \sim \pi_{new}} \left[ \sum_{t=0}^{\infty} \gamma^t \Delta_N^{\pi_{old}}(s_t) \right]}_{\Delta_1} - \underbrace{\frac{2\epsilon_Q + L_Q \epsilon_A}{1-\gamma}}_{\Delta_2} \quad \text{(Eq. 13)}$$

其中 $\Delta_N^{\pi_{old}}(s) := \mathbb{E}_{a_1, \ldots, a_N \sim \pi_{old}} [\max_i Q^{\pi_{old}}(s, a_i)] - V^{\pi_{old}}(s) \ge 0$ 为 Best-of-N 优势增益，$\Delta_2$ 为 Critic 拟合误差与策略近似误差的惩罚项。该分解表明：只要 $u_\theta$ 足够逼近真实平均速度场（控制 $\epsilon_A$），Best-of-N 即可保证策略单调改进。

策略训练总损失结合平均流匹配与 IVC 正则：

$$\mathcal{L}_{\mathrm{policy}}(\theta) = \mathcal{L}_{\mathrm{MF}}(\theta) + \lambda \mathcal{L}_{\mathrm{IVC}}(\theta) \quad \text{(Eq. 19)}$$

Critic $Q_\phi$ 以标准 TD 误差训练：

$$\mathcal{L}_{Q}(\phi) = \mathbb{E}\left[\left(Q_{\phi}(s_k, a_k) - \left(r_k + \gamma Q_{\phi}(s_{k+1}, a_{k+1}^{\star})\right)\right)^{2}\right] \quad \text{(Eq. 20)}$$

整体流程如 Algorithm 1 所示：先在离线数据集上预训练策略和 Critic，再进入在线交互与微调阶段，交替优化两者。



## 实验与关键发现

### 主实验结果

MVP在Robomimic和OGBench共9个长时域、稀疏奖励的机器人操作任务上与三个强基线进行了对比：**FQL**（Park et al., 2025，先训练多步流策略再蒸馏为单步策略）、**BFN**（Ghasemipour et al., 2021，Best-of-N采样结合多步流策略）和**QC**（Li et al., 2025，在BFN基础上加入动作分块）。所有方法使用相同的离线数据集、评估环境和超参数，每个任务使用5个随机种子重复实验，报告均值和标准差。

**Table 1**展示了各方法的成功率对比。MVP在9个任务中的8个上达到或超越当前最优水平，平均成功率达到0.88±0.05，优于QC的0.86±0.05。具体而言：

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/004_Table_1.jpg]]
*Table 1: Success rates. Mean ± Std over 5 seeds. Bold = best, underlined = 2nd-best*

- 在Robomimic-lift任务上，MVP与BFN均达到1.00的完美成功率。
- 在Robomimic-can任务上，MVP取得0.92±0.07，略低于QC的0.94±0.06。
- 在Robomimic-square任务上，MVP以0.93±0.01超越QC的0.92±0.01。
- 在Cube-double-task2和task3上，MVP与QC均达到1.00。
- 在Cube-double-task4上，MVP以0.95±0.04超越QC的0.93±0.08。
- 在Cube-triple-task2/3/4三个最具挑战性的任务上，MVP分别取得0.88±0.03、0.71±0.06、0.52±0.11，均超越QC（分别为0.82±0.10、0.69±0.05、0.46±0.13），其中Cube-triple-task4上的提升幅度最大（+0.06）。

**Figure 1**展示了9个任务上的平均成功率与在线训练速度的散点图，MVP位于图的右上角区域，表明其在性能和效率两个维度上均占据优势地位。**Figure 3**的训练曲线进一步显示，MVP在离线预训练阶段即展现出快速的收敛趋势，进入在线微调阶段后能够持续稳定提升，而多步流基线在部分任务上波动较大。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/003_Figure_3.jpg]]
*Figure 3: Training curves on benchmarks. The solid lines correspond to mean and shaded regions correspond to 95% confidence interval over five runs. The shadow background indicates the offline training phase, while the white background indicates the online training phase*

### 效率分析

一步动作生成是MVP高效性的根本来源。**Table 2**对比了各方法的在线训练速度：MVP达到153.6±11.5 iter/s，是BFN（68.0 iter/s）的2.2倍以上，也显著快于QC（79.2 iter/s）和FQL（105.3 iter/s）。这种优势源于MVP仅需单步前向传播即可生成动作，避免了多步流策略所需的迭代采样过程。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/007_Table_2.jpg]]
*Table 2: Comparison of online training speed*

在推理效率方面，**Table 3**显示MVP在CPU环境下的平均推理时间为10.93±0.95 ms，与最快的单步基线FQL（9.87 ms）相当，而远优于BFN（117.3 ms）和QC（113.2 ms）。这表明MVP在部署场景中同样具有显著优势。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/008_Table_3.jpg]]
*Table 3: Comparison of inference time*

### 消融实验

#### IVC的有效性

瞬时速度约束（IVC）是MVP方法的核心组件。**Figure 4**和**Table 4**展示了不同IVC系数λ对Cube-triple-task3和task4性能的影响。实验结果表明，IVC权重与性能呈正相关：当λ从0.0升至1.0时，Cube-triple-task4的成功率从0.30±0.21显著提升至0.52±0.11。值得注意的是，MVP对λ的取值并不敏感，λ=1.0被选为默认值即可获得稳定表现。这验证了IVC通过提供显式边界条件，有效消除了平均流恒等式的多解性，从而提升了策略的表达力。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/005_Figure_4.jpg]]
*Figure 4: Training curves of ablation on the IVC*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/009_Table_4.jpg]]
*Table 4: Ablation on the impact of IVC*

#### 与单步基线的对比

为验证MVP的优势并非单纯来自“一步生成”，**Figure 5**和**Table 5**将MVP与各基线的单步变体（如FQL-Onestep等）进行了对比。结果显示，这些单步基线在困难任务（如Cube-triple-task4）上成功率几乎为零，而MVP凭借平均速度场建模和IVC约束保持了强大的表达力，取得了0.52以上的成功率。这证明单纯的一步生成不足以解决复杂操作任务，MVP的建模设计是关键。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/006_Figure_5.jpg]]
*Figure 5: Training curves of comparison with one-step flow*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/010_Table_5.jpg]]
*Table 5: Comparison with one-step variants of the aforementioned baselines*

### 失败模式与局限性

尽管MVP在多数任务上表现优异，但以下局限性值得关注：

1. **困难任务的绝对成功率仍有提升空间**：在Cube-triple-task4上，MVP的成功率仅为0.52±0.11，标准差较大，表明在某些初始状态或操作序列下策略仍不稳定。
2. **训练中JVP计算引入额外开销**：平均流匹配损失需要计算Jacobian-vector product，可能增加GPU内存消耗，对资源受限环境不够友好。论文指出这是未来优化的方向之一。
3. **真实机器人部署尚未验证**：当前实验全部基于仿真基准（Robomimic和OGBench），在真实机器人平台上的迁移性能有待检验。
4. **IVC系数需手动设置**：尽管λ=1.0表现稳健，但缺乏自适应调节机制，在不同任务特性下可能需要调整。

### 关键图表总结

| 图表 | 核心结论 |
|------|---------|
| **Table 1** | MVP在9个任务中8个达到或超越SOTA，平均成功率0.88±0.05 |
| **Table 2** | 在线训练速度153.6 iter/s，为BFN的2.2倍以上 |
| **Table 3** | CPU推理时间10.93 ms，与最快单步基线相当 |
| **Figure 4 / Table 4** | IVC权重与成功率正相关，λ=1.0将Cube-triple-task4成功率从0.30提升至0.52 |
| **Figure 5 / Table 5** | 单步基线在困难任务上几乎为零，MVP的表达力优势来自建模设计而非仅一步生成 |

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/011_Figure_6.jpg]]
*Figure 6: Snapshots of the 9 challenging long-horizon, sparse-reward manipulation tasks*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/012_Figure_7.jpg]]
*Figure 7: Visualizations of typical success episodes: Robomimic-lift, Robomimic-can, Robomimic-square, Cube-double-task2, and Cube-double-task3*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/013_Figure.jpg]]
*Figure: (a) Double-task4 (b) step = 40*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_mIeKe74W43/figures/014_Figure_8.jpg]]
*Figure 8: Visualizations of typical success episodes: Cube-double-task4, Cube-triple-task2, Cube-tripletask3, and Cube-triple-task4*



## 定位与知识库关联

### 问题瓶颈与动机

现有基于流匹配（Flow Matching）的策略学习方法面临两个核心瓶颈。其一，**多步迭代采样**：传统流基策略（如 **FQL** (Park et al., 2025)、**BFN** (Ghasemipour et al., 2021)、**QC** (Li et al., 2025)）依赖从噪声到动作的逐步积分过程（通常需10步以上），导致训练与推理效率低下。其二，**平均流恒等式的多解性**：当从瞬时速度场转向平均速度场以实现单步生成时，平均流恒等式（Eq. 8）缺乏显式边界条件，造成训练目标存在无穷多解，积分常数可任意取值，严重损害策略表达力。这两个问题构成了“效率-表达力”的权衡困境：多步流表达力强但效率低，直接单步化则因学习不适定性导致性能崩溃。

### 核心因果机制

MVP 通过两个相互耦合的设计打破上述困境：

1. **平均速度场替代瞬时速度场**：将建模对象从瞬时速度 $v(a(t), t, s)$ 替换为区间 $[t, r]$ 上的平均速度 $u(a(t), t, r, s)$（Eq. 6），使得策略推理可由单步欧拉积分完成：$a(1) = a(0) + u(a(0), 0, 1, s)$，其中 $a(0) \sim \mathcal{N}(0, I)$。这从根本上消除了迭代采样过程。

2. **瞬时速度约束（IVC）提供边界条件**：平均流恒等式 $-u + (r-t)\frac{d}{dt}u = -v$ 本身不唯一确定 $u$。IVC 损失 $\mathcal{L}_{\text{IVC}}(\theta) = \mathbb{E}_{t, a(t)} \| u_\theta(a(t), t, t) - v \|_2^2$（Eq. 15）显式强制 $t=r$ 时平均速度等于已知瞬时速度，为恒等式提供缺失的边界条件，迫使积分常数为零，消除多解性。定理2与定理3从理论上证明了这一设计的必要性。

两者的协同效应在于：平均速度场带来单步生成的高效率，IVC 则确保该单步映射具有足够的表达力以捕获多模态动作分布。

### 与基线方法的关系

MVP 在方法谱系中处于“流基策略”与“单步生成”的交汇点，与主要基线的关系如下：

| 方法 | 生成步数 | 速度场类型 | 边界条件 | 策略改进机制 |
|------|----------|------------|----------|-------------|
| **FQL** (Park et al., 2025) | 多步（后蒸馏为单步） | 瞬时速度 | 无 | 行为克隆 + 蒸馏 |
| **BFN** (Ghasemipour et al., 2021) | 多步（约10步） | 瞬时速度 | 无 | Best-of-N + Q值选择 |
| **QC** (Li et al., 2025) | 多步 + 动作分块 | 瞬时速度 | 无 | Best-of-N + Q值选择 + 分块探索 |
| **MVP** (本文) | **单步** | **平均速度** | **IVC** | Best-of-N + Q值选择 |

关键区分点：
- **相对于 FQL**：FQL 采用“先训练多步流策略再蒸馏为单步”的两阶段方案，蒸馏过程引入额外拟合误差。MVP 直接端到端学习单步策略，避免了蒸馏损失。
- **相对于 BFN/QC**：BFN 和 QC 均使用多步瞬时速度场，推理需迭代采样。QC 额外引入动作分块以提升探索效率，但未改变多步本质。MVP 通过平均速度场实现原生单步生成，训练速度（153.6 iter/s）较 BFN（68.0 iter/s）提升约2.3倍，推理时间（10.93 ms）远低于 BFN（117.3 ms）和 QC（113.2 ms）。
- **单步变体的失败**：FQL-Onestep 等直接单步化的基线在困难任务（如 Cube-triple-task4）上成功率近乎为零（Table 5），而 MVP 达到 0.52，证明单纯减少步数不足以维持表达力，IVC 提供的边界条件是关键使能因素。

### 适用边界与局限

**适用场景**：
- 离线预训练 + 在线微调的 RL 范式，适用于长时域、稀疏奖励的机器人操作任务。
- 在 Robomimic 和 OGBench 共9个任务中，MVP 在8个任务上达到或超越当前最优水平，平均成功率达 $0.88 \pm 0.05$，在 Cube-triple 等困难任务上优势尤为明显（较 QC 提升 $+0.06$）。

**已知局限**：
1. **仿真验证局限**：目前仅在仿真基准上验证，尚未在真实机器人平台上部署，Sim-to-Real 迁移性能未知。
2. **GPU 内存开销**：训练中计算 JVP（Jacobian-vector product）以获取平均流恒等式的监督信号，可能增加 GPU 内存消耗，对资源受限环境不够友好。
3. **超参数敏感性**：IVC 系数 $\lambda$ 虽在 $[0.1, 1.0]$ 范围内不敏感，但仍需手动设置默认值 1.0，缺乏自适应调节机制。

### 开放问题

1. **高维动作空间扩展**：当前验证集中于机械臂操作（6-7维动作空间），方法能否扩展到更复杂的高维动作空间（如灵巧手操作、全身控制）尚待验证。
2. **JVP 计算替代方案**：能否通过近似方法（如有限差分）或对抗训练框架避免 JVP 计算，以降低训练时的 GPU 内存开销，是提升方法实用性的重要方向。
3. **真实机器人部署**：在真实环境中，观测噪声、动力学不确定性等因素对单步生成策略的鲁棒性影响需要进一步研究。



## 原文 PDF

![[paperPDFs/ICLR_2026/Mean_Flow_Policy_with_Instantaneous_Velocity_Constraint_for_One_step_Action_Generation.pdf]]
