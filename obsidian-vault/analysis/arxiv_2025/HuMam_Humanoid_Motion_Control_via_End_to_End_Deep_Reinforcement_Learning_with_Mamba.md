---
title: "HuMam: Humanoid Motion Control via End-to-End Deep Reinforcement Learning with Mamba"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/HuMam_Humanoid_Motion_Control_via_End_to_End_Deep_Reinforcement_Learning_with_Mamba.pdf
aliases:
- HuMam
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入单层Mamba编码器作为状态空间融合骨干，利用选择性门控动态实现高效特征交互，而无需时间递归或注意力机制。
primary_logic: Mamba的轻量级状态空间动态能够产生更平滑的特征表示，从而减少不必要的力矩波动，显著提升学习速度、训练稳定性和控制能效。
claims:
- HuMam 将峰值性能从 269.85 提升至 285.50（+5.8%），末期平均回报从 263.03 提升至 277.50（+5.5%）。
- HuMam 仅需 15.8M 样本即可达到回报 240，而基线需要 18.2M（减少 13.2%）。
- HuMam 将跨种子的学习曲线标准差从 12.08 降至 7.81（降低 35.4%），后期方差从 102.10 降至 39.87（降低 61.0%）。
- HuMam 将前向行走任务的关节平均力矩降低 9.6%，峰值力矩降低 9.1%。
---

# HuMam: Humanoid Motion Control via End-to-End Deep Reinforcement Learning with Mamba

> [!tip] 核心洞察
> Mamba的轻量级状态空间动态能够产生更平滑的特征表示，从而减少不必要的力矩波动，显著提升学习速度、训练稳定性和控制能效。

| 字段 | 内容 |
|------|------|
| 中文题名 | HuMam：基于Mamba的端到端深度强化学习人形运动控制 |
| 英文题名 | HuMam: Humanoid Motion Control via End-to-End Deep Reinforcement Learning with Mamba |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2509.18046) · [Code](https://github.com/allen-legged-robot/humam-rl) · [arXiv](https://arxiv.org/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | HuMam |
| Dataset | JVRC-1 Forward Walking, JVRC-1 Standing, JVRC-1 Lateral Walking, JVRC-1 Backward Walking |

> [!tip] 效果简介
> - JVRC-1 Forward Walking 上，Peak Return 285.50 vs 269.85 (+5.8%)；Final Mean Return (last 10%) 277.50 vs 263.03 (+5.5%)；Samples to Reach 240 Returns (M) 15.8 vs 18.2 (-13.2%)。
> - JVRC-1 Standing 上，Average Power (W) 35.08 vs 57.48 (-39.0%)。
> - JVRC-1 Lateral Walking 上，Energy Efficiency (J/m) 963 vs 1395 (-31.0%)。

## 概述

**核心问题**：人形机器人的运动控制面临异构感知信息融合的挑战——机器人本体状态（关节位置/速度、基座姿态）与外部引导信号（目标脚步、步态时钟）具有不同的物理含义和变化尺度。传统的前馈策略网络（MLP）直接将所有观测拼接输入，缺乏有效的特征交互机制，导致训练不稳定、样本效率低，且学习出的策略往往伴随不必要的力矩波动和较高的驱动能量消耗。

**核心方法**：HuMam 提出以**单层 Mamba 编码器**作为策略网络的特征融合骨干。与传统的全连接 MLP 不同，Mamba 的选择性状态空间动态（selective state-space dynamics）能够在不引入时间递归或注意力机制的前提下，对多模态观测令牌序列进行高效的特征混合，产生更平滑的共享表示，从而减少策略输出的力矩波动。

**核心发现**：Mamba 编码器的轻量级状态空间融合能力，在多个维度上带来了显著收益：
- **性能提升**：前向行走任务的峰值回报从 269.85 提升至 285.50（+5.8%），末期平均回报从 263.03 提升至 277.50（+5.5%）（Table 3）。
- **样本效率**：达到回报 240 所需样本量从 18.2M 降至 15.8M，减少 13.2%（Table 3）。
- **训练稳定性**：跨种子学习曲线标准差从 12.08 降至 7.81（降低 35.4%），后期方差从 102.10 降至 39.87（降低 61.0%）（Table 3）。
- **能效改善**：前向行走任务中关节平均力矩降低 9.6%，峰值力矩降低 9.1%（Table 5）；能量消耗从 673 J/m 降至 421 J/m（降低 37.4%），站立任务平均功耗从 57.48W 降至 35.08W（降低 39%）（Table 6）。

**方法定位**：HuMam 属于**端到端深度强化学习人形运动控制**框架，采用位置级策略输出配合低增益 PD 控制器执行。其核心创新在于用状态空间模型（Mamba）替代传统 MLP 作为观测融合骨干，在不增加计算复杂度的前提下提升了特征表示质量和策略优化效率。该方法在仿真 JVRC-1 平台上进行了五种运动模式的验证（前向、后退、弯道、站立、侧向行走），但尚未进行 sim-to-real 迁移，也未与其他序列模型骨干（如 Transformer、LSTM）进行直接对比。

## 背景与动机

人形机器人因其类人形态，在复杂人类环境中具有天然的操作与导航优势。然而，实现稳定、高效的双足运动控制一直是机器人领域的核心挑战。传统基于模型的控制方法依赖精确的动力学建模与繁琐的手工调参，难以应对多样化的行走模式与环境扰动。近年来，深度强化学习（DRL）为无模型运动控制开辟了新路径，但现有方法在样本效率、训练稳定性和驱动能效方面仍存在显著瓶颈。

### 异构感知融合的瓶颈

在人形运动控制中，策略网络需要同时处理两类性质迥异的感知信息：**机器人中心状态**（关节位置、速度、基座姿态与角速度）和**外部引导信号**（目标脚步位置、步态相位时钟）。前者是高维、连续的物理状态，后者是稀疏、结构化的任务指令。传统的前馈多层感知机（MLP）策略网络将所有观测直接拼接后送入全连接层，缺乏针对异构信息的结构化融合机制。这导致三个关键问题：

1. **训练不稳定**：不同模态的数值尺度与语义差异使得梯度信号相互干扰，学习过程出现剧烈振荡，跨种子的学习曲线标准差高达 12.08。
2. **样本效率低下**：网络需要大量交互样本才能从混合输入中提取有效特征，达到回报 240 需消耗 18.2M 样本。
3. **驱动能量浪费**：粗糙的特征融合导致策略输出包含不必要的力矩波动，前向行走任务中关节平均力矩和峰值力矩均处于较高水平，能量消耗达 673 J/m。

### 现有序列模型的局限

直觉上，Transformer 或 LSTM 等序列建模架构可能改善特征交互质量。但 Transformer 的自注意力机制在低维观测序列上引入过高计算开销与训练不稳定性，LSTM 的时序递归则带来梯度消失和推理延迟问题。人形运动控制对实时性要求极高（策略输出频率 40 Hz，底层控制频率 1000 Hz），且观测本身是即时状态快照而非长序列，因此需要一种**轻量级、非递归、能高效混合异构特征**的融合骨干。

### HuMam 的动机与核心思路

HuMam 的核心动机在于：**用状态空间模型的结构化动态替代简单拼接，以极低的计算代价实现异构特征的深度融合**。具体而言，HuMam 引入单层 Mamba 编码器作为融合骨干。Mamba 的选择性状态空间机制通过输入依赖的门控动态，自适应地调节不同特征通道间的信息流动，无需时间递归或注意力计算即可产生平滑、紧凑的共享表示。这种设计预期带来三重收益：

- **更快的收敛**：高效的特征交互加速策略从奖励信号中提取有效模式；
- **更稳定的训练**：平滑的表示空间减少梯度方差，抑制策略的剧烈振荡；
- **更低的能耗**：紧凑的特征编码消除冗余的力矩指令，使输出动作更加节能。

本文在 JVRC-1 人形机器人平台上，以统一的前馈基线为参照，系统验证了 Mamba 骨干在多种行走模式下的性能增益。

## 核心创新

### 瓶颈分析：前馈策略网络的异构信息融合困境

人形机器人的运动控制需要同时处理两类性质迥异的感知信号：**机器人中心状态**（关节角度、角速度、基座姿态与角速度等本体感受信息）与**外部引导信号**（目标脚步、步态相位时钟等任务指令）。传统的前馈神经网络基线（Feedforward MLP）将所有观测向量直接拼接后送入全连接层，缺乏针对模态差异的结构化归纳偏置。这种粗暴的融合方式导致三个连锁问题：

1. **训练不稳定**：跨随机种子的学习曲线标准差高达 12.08，后期方差达 102.10（Table 3），表明策略对初始化和环境噪声高度敏感；
2. **样本效率低下**：达到回报 240 需要 18.2M 样本，训练成本高昂；
3. **驱动能量浪费**：前向行走任务中平均关节力矩和峰值力矩均处于高位，能量消耗达 673 J/m（Table 6）。

根本原因在于，MLP 骨干缺乏对异构输入之间**选择性交互**的建模能力——它无法动态决定哪些状态维度在当前控制决策中更为关键，导致特征表示中混入大量冗余和噪声，进而产生不必要的力矩波动。

### 核心机制：Mamba 选择性状态空间作为融合骨干

HuMam 的核心创新在于引入**单层 Mamba 编码器**替代传统 MLP，作为异构感知信息的融合骨干（changed slot: backbone）。其关键设计理念是**利用选择性状态空间动态实现高效的特征交互，而无需时间递归或注意力机制**。

具体而言，HuMam 的观测处理流程如下：

1. **观测投影**：将机器人关节状态、目标脚步（$T_i = [x_i, y_i, z_i, \theta_i]$）和步态时钟信号（$\mathrm{Clock}_t = [\sin(2\pi\phi/L), \cos(2\pi\phi/L)]$）分别映射为模态特定的嵌入向量，构成令牌序列；
2. **Mamba 编码**：单层 Mamba 编码器通过选择性状态空间更新方程 $x_{k+1} = \sigma(W_A u_{t,k}) x_k + \sigma(W_B u_{t,k}) u_{t,k}$（Equation 15）对令牌序列进行扫描，其中输入门控 $\sigma(W_B u_{t,k})$ 动态控制新信息的注入强度，状态门控 $\sigma(W_A u_{t,k})$ 选择性保留或遗忘历史上下文；
3. **策略输出**：编码后的紧凑共享表示分别送入策略头（输出 12 个目标关节位置，40 Hz）和价值头，最终通过低增益 PD 控制器转换为执行扭矩（1000 Hz）。

Mamba 的选择性门控机制赋予了网络一种**隐式的注意力能力**：它可以根据当前机器人状态和任务指令，动态调节不同感知通道之间的信息流动。例如，在摆动相期间，脚步目标信号的权重被自动增强以引导足部精准落地；而在支撑相期间，本体感受状态的权重上升以维持全身平衡。这种动态特征混合产生了更平滑的表示空间，从根本上抑制了力矩指令中的高频抖动。

### 创新效果：从性能提升到能效跃迁

HuMam 的创新设计在多个维度上带来了显著且一致的增益：

**学习性能与稳定性**（Table 3）：
- 峰值回报从 269.85 提升至 285.50（+5.8%），末期平均回报从 263.03 提升至 277.50（+5.5%）；
- 达到回报 240 所需样本从 18.2M 降至 15.8M（减少 13.2%），样本效率显著提高；
- 跨种子学习曲线标准差从 12.08 降至 7.81（降低 35.4%），后期方差从 102.10 降至 39.87（降低 61.0%），训练稳定性得到质的改善。

**力矩平滑与能效优化**（Table 5, Table 6）：
- 前向行走任务中，关节平均力矩降低 9.6%，峰值力矩降低 9.1%；
- 站立任务平均功耗从 57.48W 降至 35.08W（降低 39.0%）；
- 前向行走能量消耗从 673 J/m 降至 421 J/m（降低 37.4%），侧向行走从 1395 J/m 降至 963 J/m（降低 31.0%），后退行走从 952 J/m 降至 853 J/m（降低 10.4%）。

这些结果表明，Mamba 编码器带来的平滑特征表示不仅提升了策略的收敛质量，更从根本上降低了执行器的无效做功——机器人学会了用更“经济”的力矩模式完成相同的运动任务。这种能效优势对于人形机器人的实际部署（尤其是电池续航受限的场景）具有重要的工程价值。

### 创新边界与待验证问题

尽管 HuMam 在仿真环境中展现了令人信服的性能优势，其创新主张仍存在以下边界条件需要审慎看待：

1. **骨干对比的单一性**：当前仅与前馈 MLP 基线进行了对比，未涉及 Transformer、LSTM 或 RWKV 等其他序列建模骨干。在相同计算预算下，Mamba 是否具有绝对优势尚待验证。
2. **仿真到现实的鸿沟**：所有实验均在仿真环境中完成，未在物理 JVRC-1 平台上部署。Mamba 编码器产生的平滑力矩在实际硬件延迟、传感器噪声和模型误差下是否仍能保持优势，需要 sim-to-real 迁移实验证实。
3. **任务覆盖的局限性**：仅在平整地面上测试了五种步行模式，未涉及楼梯、斜坡、不平地形等多接触行为。在更复杂的接触动力学场景下，Mamba 的选择性门控是否仍能有效运作，属于开放问题。

## 整体框架

HuMam 将人形运动控制建模为端到端的深度强化学习问题，整体架构由四个核心模块串联构成：**观测投影** → **Mamba 编码器** → **策略/价值头** → **低增益 PD 控制器**，形成从异构感知输入到关节扭矩输出的完整控制链路（Figure 1）。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/001_Figure_1.jpg]]
*Figure 1: Overall architecture of the proposed humanoid locomotion framework. At each time step, robot-centric and external states are collected as observations and projected into a latent embedding. A single-layer Mamba encoder processes these features to produce compact representations for the policy and value heads, which are optimized using PPO. A hierarchical control structure is adopted, where the high-level policy outputs desired joint positions and a low-gain PD controller converts them into executable joint torques. The reward design combines foot-level and body-level objectives to encourage stable and natural gaits*

### 观测投影

每个时间步，系统收集两类异构观测信号：**机器人中心状态**（关节位置与速度、基座姿态与角速度）和**外部引导状态**（目标脚步、步态时钟、期望朝向）。这些多模态信号通过独立的投影层映射为统一维度的令牌嵌入，构成一个令牌序列作为 Mamba 编码器的输入。

### Mamba 编码器

核心瓶颈在于传统前馈 MLP 难以有效融合上述异构信息，导致特征表示不够平滑、训练不稳定。HuMam 引入**单层 Mamba 编码器**作为状态空间融合骨干（Table 1：隐藏维度 128）。Mamba 利用选择性门控的状态空间动态对令牌序列进行特征编码，无需时间递归或注意力机制即可实现高效的跨模态特征交互。其状态更新遵循：

$$x_{k+1} = \sigma( W_A u_{t,k} ) x_k + \sigma( W_B u_{t,k} ) u_{t,k}$$

该机制产生的特征表示更为平滑，直接减少了后续策略输出的力矩波动。

### 策略与价值头

编码后的共享表示分别送入**策略头**和**价值头**。策略头输出 12 个目标关节位置（频率 40 Hz），价值头估计状态价值函数用于 PPO 的优势计算。两者通过同一 PPO 训练损失联合优化：

$$\mathcal{I}(\theta, \phi) = -\mathcal{L}_{\mathrm{clip}}(\theta) + \beta_V \mathcal{L}_V(\phi) - \beta_H \mathbb{E}[\mathcal{H}_t]$$

其中裁剪代理目标约束策略更新幅度，广义优势估计（GAE）降低优势方差，熵正则项鼓励探索。

### 低增益 PD 控制器

策略输出的目标关节位置并非直接作为力矩指令，而是通过**低增益 PD 控制器**转换为执行扭矩（频率 1000 Hz）。这种分层控制结构使得高层策略只需关注位置层面的运动规划，底层 PD 控制器保证平滑的力矩输出，从而让学习过程保持良好条件化。

## 核心模块与公式推导

### 3.1 问题形式化与观测空间

HuMam 将人形运动控制建模为马尔可夫决策过程（MDP），其优化目标为最大化累积折扣回报：

$$J(\pi) = \mathbb{E}_{\pi}\left[\sum_{t=0}^{T-1} \gamma^t r(s_t, a_t)\right]$$

其中策略 $\pi$ 输出目标关节位置 $a_t$，低增益 PD 控制器以 1000 Hz 频率将其转化为执行扭矩，形成层次化控制架构。

观测向量由机器人中心状态与外部引导状态拼接而成：

$$s_t = \{ s_t^{\mathrm{robot}}, s_t^{\mathrm{external}} \}$$

**机器人中心状态**包括腿部关节位置与速度、基座姿态四元数及角速度。**外部引导状态**则引入两类关键信号：

- **目标脚步**：以机器人坐标系中的下一步及再下一步脚步位姿表示：

$$T_i = [x_i, y_i, z_i, \theta_i], \quad i \in \{1, 2\}$$

- **步态相位时钟**：采用正弦/余弦对连续编码步态相位，避免循环计数的不连续性：

$$\mathrm{Clock}_t = [\sin(2\pi\phi/L), \cos(2\pi\phi/L)]$$

### 3.2 奖励函数设计

奖励函数由六项加权组合而成，兼顾足部精度与全身稳定性：

$$R_t = \alpha_{\mathrm{force}} R_t^{\mathrm{force}} + \alpha_{\mathrm{vel}} R_t^{\mathrm{vel}} + \alpha_{\mathrm{step}} R_t^{\mathrm{step}} + \alpha_{\mathrm{orient}} R_t^{\mathrm{orient}} + \alpha_{\mathrm{height}} R_t^{\mathrm{height}} + \alpha_{\mathrm{upper}} R_t^{\mathrm{upper}}$$

其中步伐精度奖励鼓励摆动脚准确落在目标脚步上：

$$R_t^{\mathrm{step}} = \exp\big( - \| p_t^{\mathrm{foot}} - T_1 \|^2 \big)$$

姿态奖励惩罚根四元数偏离参考姿态：

$$R_t^{\mathrm{orient}} = \exp\big( -10 \cdot (1 - \langle q_t, \hat{q}_t \rangle^2) \big)$$

身高奖励维持标称根高度：

$$R_t^{\mathrm{height}} = \exp\big( -40 \cdot ( h_t^{\mathrm{root}} - \hat{h}^{\mathrm{root}} )^2 \big)$$

其余三项分别约束足部接触力、摆动速度及上体角速度，共同构成紧凑且可泛化的奖励结构。

### 3.3 Mamba 编码器：选择性状态空间融合骨干

HuMam 的核心创新在于用**单层 Mamba 编码器**替代传统前馈 MLP 作为策略网络的特征融合骨干。其处理流程如下：

1. **观测投影**：将异构输入（关节状态、脚步目标、时钟信号）映射为模态特定嵌入，生成令牌序列。
2. **Mamba 编码**：通过选择性状态空间动态对令牌序列进行特征编码，核心更新方程为：

$$x_{k+1} = \sigma( W_A u_{t,k} ) x_k + \sigma( W_B u_{t,k} ) u_{t,k}$$

其中 $u_{t,k}$ 为第 $k$ 个令牌，$\sigma$ 为选择性门控函数。该机制使模型能够根据输入内容动态调整状态转移，实现高效的特征交互，而无需时间递归或注意力机制。

3. **策略头与价值头**：从编码后的紧凑共享表示分别输出 12 个目标关节位置（40 Hz）和状态价值估计。

网络架构配置见 Table 1：令牌宽度 $d=41$，Mamba 隐藏尺寸 $d=128$，投影头为单层 MLP + ReLU。

### 3.4 PPO 优化目标

策略与价值函数通过 PPO 联合优化。优势估计采用广义优势估计（GAE）降低方差：

$$\delta_t = r_t + \gamma V_{\phi}(s_{t+1}) - V_{\phi}(s_t), \qquad \hat{A}_t = \sum_{l=0}^{T-t-1} (\gamma\lambda)^l \delta_{t+l}$$

策略更新采用裁剪代理目标约束更新幅度：

$$\pi^{*} = \arg\max_{\pi} \mathbb{E}_t \Big[ \min\big( \rho_t(\theta) \hat{A}_t,\ \mathrm{clip}(\rho_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \big) \Big]$$

总体训练损失函数联合优化策略、价值函数及熵正则项：

$$\mathcal{I}(\theta, \phi) = -\mathcal{L}_{\mathrm{clip}}(\theta) + \beta_V \mathcal{L}_V(\phi) - \beta_H \mathbb{E}[\mathcal{H}_t]$$

其中熵奖励定义为：

$$\mathcal{H}_t = -\sum_a \pi_{\theta}(a \mid s_t) \log \pi_{\theta}(a \mid s_t)$$

该设计在保持训练稳定性的同时鼓励探索，所有实验均使用相同的 PPO 超参数（见 Table 2）以确保公平对比。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/002_Table.jpg]]
*Table: Network architecture settings*

## 实验与分析

### 实验设置

实验在 Isaac Gym 仿真环境中进行，机器人模型为 JVRC-1 人形机器人。所有策略均使用相同 PPO 超参数（Table 2）、网络容量和训练步数进行训练，采用 on-policy 轨迹采样、小批量更新、优势归一化和梯度裁剪。每个实验使用多个随机种子重复运行，报告均值和标准差以验证稳定性。Baseline 与 HuMam 在完全相同的仿真环境与奖励函数下训练和评估，确保对比公平性。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/004_Table_2.jpg]]

评估涵盖五种运动场景：前向行走、后退行走、弯道路径行走、原地站立和侧向行走（Figure 2）。网络架构配置如 Table 1 所示，Mamba 编码器采用单层结构，隐藏维度为 128。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/003_Figure_2.jpg]]
*Figure 2: Simulated environments that the robot is trained and evaluated. Panels (a)–(e): (a) Walking straight forward; (b) Walking straight backward; (c) Walking on a curved path; (d) Standing in place; (e) Lateral Walking*

### 主要结果

**性能与样本效率。** Table 3 汇总了 JVRC-1 前向行走任务的核心指标。HuMam 将峰值回报从 Baseline 的 269.85 提升至 285.50（+5.8%），末期平均回报（最后 10% 训练阶段）从 263.03 提升至 277.50（+5.5%）。在样本效率方面，HuMam 仅需 15.8M 样本即可达到回报 240，而 Baseline 需要 18.2M，样本消耗减少 13.2%。

**训练稳定性。** 跨种子的学习曲线标准差从 12.08 降至 7.81（降低 35.4%），后期训练方差从 102.10 降至 39.87（降低 61.0%），表明 Mamba 编码器产生的平滑特征表示显著抑制了训练过程中的策略震荡。Figure 3 的训练曲线直观展示了这一差异：HuMam 的阴影区域（标准差）明显更窄，回报增长更为平稳。

**奖励组成分析。** Table 4 展示了各项奖励分项的平均值对比。HuMam 在步伐精度、姿态保持和上体稳定性等关键子项上均取得提升，整体每步平均总奖励从 0.728 提高至 0.737。

### 关节力矩与能量效率

**力矩降低。** Table 5 和 Figure 8 给出了前向行走任务的关节力矩对比。HuMam 将各关节平均力矩降低 9.6%，峰值力矩降低 9.1%。这一改善源于 Mamba 的选择性状态空间动态能够产生更平滑的特征表示，从而减少不必要的力矩波动。

**能耗优化。** Table 6 汇总了各任务下的能量效率与功耗对比。在前向行走任务中，HuMam 将能量消耗从 673 J/m 降至 421 J/m（降低 37.4%）；侧向行走从 1395 J/m 降至 963 J/m（降低 31.0%）；后退行走从 952 J/m 降至 853 J/m（降低 10.4%）。在站立任务中，平均功耗从 57.48W 降至 35.08W（降低 39%）。这些结果表明，Mamba 编码器在无需时间递归或注意力机制的前提下，通过轻量级状态空间动态实现了控制信号的平滑化，从而大幅降低了驱动能量消耗。

### 足部轨迹分析

Figure 4–7 展示了各行走任务的足部轨迹。HuMam 生成的足部轨迹更加规整、对称，摆动相与支撑相的过渡更为平滑，这与力矩和能耗的改善趋势一致。在弯道路径行走（Figure 7）中，HuMam 的步态适应性优于 Baseline，轨迹偏差更小。

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/006_Figure_4.jpg]]
*Figure 4: Foot trajectory of lateral walking*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/011_Figure_7.jpg]]
*Figure 7: Foot trajectory of curved path walking*

### 局限性与失败模式

当前工作存在以下局限，需在后续研究中解决：

1. **仅仿真验证**：所有实验均在 Isaac Gym 仿真环境中完成，未在实际 JVRC-1 物理机器人上进行 sim-to-real 迁移部署，物理环境下的鲁棒性尚待验证。
2. **骨干对比不足**：仅与前馈 MLP 基线进行了对比，未与 Transformer、LSTM 等其他序列模型骨干在相同计算预算下进行系统比较。
3. **地形单一**：仅在平整地面上测试了五种步行模式，未涉及楼梯、不平地形等多接触行为，泛化能力有限。
4. **实时性分析缺失**：未提供推理延迟和计算资源占用的详细分析，这对实际部署至关重要。

### 开放问题

基于上述局限，以下问题值得进一步探索：

- 如何将当前框架成功实现 sim-to-real 迁移并部署在真实 JVRC 平台上？
- 在完全相同的计算预算下，Mamba 与其他轻量级骨干（如 Linformer、RWKV）相比表现如何？
- 能否在不显著增加样本复杂度的前提下，将观测空间扩展至视觉或事件相机等机载感知信号？
- 如何整合在线脚步规划与可行性检查，以应对动态环境中的实时行走策略？
- 在更严格的能量预算下，能否学习出更为复杂的多接触行为（如上下楼梯）？

### 补充图表

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/005_Figure_3.jpg]]
*Figure 3: Training curves of HuMam and Baseline across scenarios. Solid lines denote the mean episode return across seeds, while shaded regions indicate the standard deviation*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/007_Table_3.jpg]]

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/010_Table.jpg]]
*Table: Comprehensive Reward Components Comparison*

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/012_Table_5.jpg]]

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/013_Table_6.jpg]]

![[assets/figures/papers/paper_list_l27_https_arxiv_org_abs_2509_18046/figures/014_Figure_8.jpg]]
*Figure 8: Joint Torques of Forward Walking Task*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

HuMam 的核心技术路径是在标准 PPO 强化学习框架内，将策略网络中的**特征融合骨干**从前馈 MLP 替换为**单层 Mamba 编码器**。这一替换的直接比较对象是论文中构建的 **Baseline** 方法——一个使用全连接 MLP 直接融合所有观测输入（机器人状态、步态时钟、目标脚步）的前馈策略网络，两者共享完全相同的奖励函数、PPO 超参数（Table 2）和训练环境。

从方法谱系上看，HuMam 属于**状态空间模型（SSM）驱动的端到端强化学习**范式，区别于以下几条主流路线：

- **基于模型的控制（Model-Based Control）**：传统人形机器人运动控制依赖全身动力学模型和轨迹优化（如模型预测控制 MPC），这些方法需要精确的系统辨识，计算负担重，且在接触丰富的非结构化环境中泛化能力有限。HuMam 的端到端无模型路线绕过了显式建模，直接通过仿真交互学习策略。
- **Transformer / LSTM 序列策略**：近年来有工作将 Transformer 或 LSTM 引入策略网络以捕捉时序依赖，但这些方法要么计算开销大，要么面临梯度消失/爆炸问题。HuMam 选择 Mamba 的动机在于其**选择性状态空间动态**可以在不引入时间递归或注意力机制的前提下实现高效的特征交互，从而避免上述问题。但需注意，论文**未直接与 Transformer 或 LSTM 骨干进行实验对比**，这一比较的缺失是需要手动验证的薄弱环节。
- **分层控制策略（Hierarchical Control）**：HuMam 采用高层策略输出目标关节位置、低层低增益 PD 控制器执行力矩的分层结构。这一设计在机器人学习中并不新颖（例如 引用的相关工作），其作用是将学习问题约束在位置层面，使优化更稳定。HuMam 的贡献不在于分层结构本身，而在于**高层策略内部的特征融合机制**。

### 2. 核心机制差异与因果归因

Baseline 与 HuMam 之间的性能差距可归因于以下因果链条：

1. **异构信息融合瓶颈**：Baseline 将机器人本体状态（关节位置/速度、基座姿态/角速度）与外部引导信号（目标脚步、步态时钟）直接拼接后送入 MLP。由于这些信号在物理意义、量纲和变化频率上高度异构，前馈 MLP 的静态权重难以自适应地调节各模态间的信息流动，导致特征表示不够平滑。

2. **Mamba 的选择性门控机制**：HuMam 通过 Mamba 编码器的选择性状态空间更新方程（Equation 15）：
   $$x_{k+1} = \sigma( W_A u_{t,k} ) x_k + \sigma( W_B u_{t,k} ) u_{t,k}$$
   实现了对输入序列的动态特征混合。其中门控函数 $\sigma(W_A u_{t,k})$ 和 $\sigma(W_B u_{t,k})$ 根据当前输入内容自适应地决定保留多少历史状态和注入多少新信息，这使得编码器能够产生更紧凑、更平滑的共享表示。

3. **从平滑表示到高效控制**：更平滑的特征表示直接导致策略输出的目标关节位置序列波动更小，进而通过低增益 PD 控制器产生**更低的关节力矩振荡**。这解释了 Table 5 中 HuMam 将前向行走任务的平均关节力矩降低 9.6%、峰值力矩降低 9.1% 的现象，以及 Table 6 中站立任务功耗降低 39%、前向行走能量消耗从 673 J/m 降至 421 J/m（降低 37.4%）的显著节能效果。

4. **训练稳定性提升**：平滑的特征空间也稳定了 PPO 的策略梯度更新。Table 3 显示，HuMam 将跨种子的学习曲线标准差从 12.08 降至 7.81（降低 35.4%），后期训练方差从 102.10 降至 39.87（降低 61.0%）。这表明 Mamba 编码器有效抑制了异构输入引起的梯度噪声，使优化过程更加鲁棒。

### 3. 适用边界与约束条件

HuMam 的当前设计存在明确的适用边界：

- **任务空间**：仅在平整地面上验证了五种步行模式（前向、后退、弯道、侧向行走和站立），未涉及楼梯、斜坡、不平地形等多接触/欠约束行为。在这些场景下，脚步目标的设计和奖励函数的适应性需要重新评估。
- **感知模态**：观测空间仅包含本体感知和预定义的外部引导（目标脚步、步态时钟），未整合视觉、深度或触觉等机载感知信号。将观测空间扩展到高维感知输入时，Mamba 编码器的令牌序列处理能力是否仍然高效，是一个待验证的开放问题。
- **仿真到现实的迁移**：所有实验均在仿真环境中完成，未在真实 JVRC-1 物理机器人上部署。低增益 PD 控制器产生的平滑力矩在仿真中表现良好，但真实世界的执行器延迟、关节摩擦和接触动力学不确定性可能削弱这一优势。
- **计算实时性**：论文未提供推理延迟和计算资源分析。虽然单层 Mamba 在理论上是轻量级的，但在嵌入式平台上的实际运行频率（目标为 40 Hz 策略输出）仍需验证。

### 4. 局限性与开放问题

基于论文验证分析中提取的局限性和开放问题：

**已验证的局限性：**
- 仅进行仿真验证，缺乏 sim-to-real 迁移实验。
- 未与其他序列模型骨干（Transformer、LSTM、RWKV、Linformer 等）在相同计算预算下进行对比。
- 仅在平整地面测试五种步行模式，任务多样性有限。
- 缺乏推理延迟和实时性资源分析。

**开放问题：**
1. 如何将当前框架成功实现 sim-to-real 迁移并部署在真实 JVRC-1 平台上？这需要解决域随机化、系统辨识和在线自适应等工程挑战。
2. 在完全相同的计算预算下，Mamba 与其他轻量级骨干（如 Linformer、RWKV）相比表现如何？这一对比对于确立 Mamba 在人形控制中的独特优势至关重要。
3. 能否在不显著增加样本复杂度的前提下，将观测空间扩展至视觉或事件相机等机载感知信号？这需要重新设计观测投影模块，并可能引入视觉编码器的预训练。
4. 如何整合在线脚步规划与可行性检查，以应对动态环境中的实时行走策略？当前脚步目标来自预定义的开环模式，缺乏对障碍物或地形变化的在线适应能力。
5. 在更严格的能量预算下，能否学习出更为复杂的多接触行为（如上下楼梯）？这需要奖励函数和脚步目标设计的根本性扩展。

### 5. 知识库定位

HuMam 在人形机器人运动控制的知识体系中占据以下位置：

- **方法论贡献**：首次将 Mamba 状态空间模型作为端到端强化学习策略的特征融合骨干应用于人形运动控制，证明了选择性状态空间动态在该领域的有效性。
- **经验性发现**：揭示了平滑特征表示与低能耗控制之间的因果关联，为后续工作提供了"通过特征融合设计提升能效"的研究方向。
- **基准价值**：提供了在 JVRC-1 仿真平台上使用 PPO 训练人形步态的完整基准（Baseline 性能、奖励分解、力矩分布、能耗指标），可作为后续方法比较的参考点。

需要注意的是，由于论文未提供会议/期刊发表信息（venue 和 year 均为 null），在引用和定位其学术影响力时需要谨慎，建议确认正式发表版本后再进行学术引用。

## 原文 PDF

![[paperPDFs/arxiv_2025/HuMam_Humanoid_Motion_Control_via_End_to_End_Deep_Reinforcement_Learning_with_Mamba.pdf]]
