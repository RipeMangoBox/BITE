---
title: "Robot Motion Diffusion Model: Motion Generation for Robotic Characters"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/Robot_Motion_Diffusion_Model_Motion_Generation_for_Robotic_Characters.pdf
aliases:
- RMDMR
- RMDMMGRC
tags:
- SIGGRAPH_ASIA_2024
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "训练一个边缘化奖励代理（Critic），仅基于运动学参考运动预测策略的预期累计回报，从而提供可微分、计算高效的损失函数，用于微调生成式运动学模型，使生成的运动与物理角色能力对齐。"
primary_logic: "通过将运动生成与运动跟踪解耦，利用预训练的运动扩散模型（MDM）提供多样化的运动先验，同时引入边缘化 Critic 作为物理可行性的可微分替身，在微调阶段将物理理解融入采样过程，无需频繁在线仿真即可生成既保持语义多样性又具备物理合理性的运动。"
claims:
- "提出用 reward surrogate（Critic）预测下游跟踪任务的期望回报，作为可微分损失微调生成模型。"
- "RobotMDM 将文本条件的运动扩散模型与基于 RL 的跟踪控制器结合，生成物理合理且可直接部署的运动。"
- "RobotMDM 在 kinematic 评估中实现最高 Realism score（9.562），同时保持与基线相当的生成质量与多样性。"
- "在模拟跟踪评估中，RobotMDM 生成的运动在所有跟踪误差指标上均大幅优于 MDM 基线，例如下体自由度误差降低约 30%。"
---

# Robot Motion Diffusion Model: Motion Generation for Robotic Characters

> [!tip] 核心洞察
> 通过将运动生成与运动跟踪解耦，利用预训练的运动扩散模型（MDM）提供多样化的运动先验，同时引入边缘化 Critic 作为物理可行性的可微分替身，在微调阶段将物理理解融入采样过程，无需频繁在线仿真即可生成既保持语义多样性又具备物理合理性的运动。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 机器人运动扩散模型：面向机器人角色的运动生成 |
| 英文题名 | Robot Motion Diffusion Model: Motion Generation for Robotic Characters |
| 会议/期刊 | SIGGRAPH Asia 2024 |
| Links | [paper](https://doi.org/10.1145/3680528.3687626) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Robot Motion Diffusion Model (RobotMDM) |
| Dataset | Simulated Tracking (2048 episodes, 30s references), Simulated Tracking |

> [!tip] 效果简介
> - Simulated Tracking (2048 episodes, 30s references) 上，Lower DoFs Tracking Error ↓ 为 11.44，对比 16.11 (MDM)，变化 -4.67。
> - Simulated Tracking 上，Root Rotation Tracking Error ↓ 为 2.34，对比 4.13 (MDM)，变化 -1.79。
> - Simulated Tracking 上，Linear Velocity Tracking Error [m/s] ↓ 为 3.43，对比 4.90 (MDM)，变化 -1.47。

## 概述

现有运动学生成模型（如 **MDM**，Tevet et al., ICLR 2023）虽能产生视觉上吸引人的运动序列，但缺乏物理约束，导致生成的运动包含漂浮、脚底滑动、自碰撞、关节限位违反和动力失衡等瑕疵，无法直接部署于真实物理系统或机器人。核心瓶颈在于：生成的 kinematic 动作缺乏物理可行性，使得下游跟踪控制器无法准确执行。

针对这一问题，本文提出 **Robot Motion Diffusion Model (RobotMDM)**，一个文本条件的运动学扩散模型，可与基于强化学习的跟踪控制器无缝对接，生成物理合理且可直接部署的运动。其核心思路是将运动生成与运动跟踪解耦：利用预训练的运动扩散模型提供多样化的运动先验，同时训练一个**边缘化奖励代理（Critic）**，仅基于运动学参考运动预测策略的预期累计回报，从而提供可微分、计算高效的损失函数，用于微调生成模型，使生成的运动与物理角色能力对齐，而无需频繁在线仿真。

主要结果如下：

- **运动学评估**：RobotMDM 在 Realism score 上达到最高（9.562），同时保持与基线相当的生成质量与多样性。
- **模拟跟踪评估**：在 2048 个 30 秒参考运动的仿真跟踪测试中，RobotMDM 在所有跟踪误差指标上均大幅优于 MDM 基线——下体自由度跟踪误差从 16.11 降至 11.44（降幅约 30%），根旋转误差从 4.13 降至 2.34，线速度误差从 4.90 m/s 降至 3.43 m/s。
- **真实机器人部署**：RobotMDM 生成的运动可在真实机器人上实现更精准的跟踪执行，而 MDM 的运动因缺乏平衡和物理合理性导致目标匹配失败。

方法的局限性在于：Critic 仅提供软性可行性偏好，不包含硬物理约束，无法保证生成的运动绝对安全；数据集与角色高度特定，当文本提示严重超出角色能力时，Critic 可能缺乏有效信号。

## 背景与动机

### 问题背景：运动学生成与物理执行之间的鸿沟

近年来，数据驱动的运动学生成模型取得了显著进展。以**MDM**（Tevet et al., ICLR 2023）为代表的文本条件运动扩散模型，能够根据自然语言描述生成多样化且视觉上富有表现力的人体运动序列。这类模型从大规模运动捕捉数据中学习运动先验，在生成质量、语义匹配度和多样性方面表现优异。

然而，当这些运动学运动被部署到真实物理系统——无论是仿真中的物理角色还是实体机器人——时，一个根本性瓶颈暴露出来：**生成的运动缺乏物理可行性**。运动学生成模型仅关注关节角度的时序变化，完全忽略了质量、惯性、接触力、驱动饱和等物理约束。这导致生成的参考运动中充斥着漂浮、脚底滑动、自碰撞、关节限位违反和动力失衡等瑕疵。下游的跟踪控制器（tracking controller）面对这些物理上不可行的参考运动时，无法准确执行，表现为跟踪误差急剧增大，甚至导致角色摔倒或机器人失控。

这一鸿沟的核心在于：**运动学生成器与物理执行器之间缺乏有效的反馈通道**。生成器不了解下游控制器的能力边界，控制器也无法向生成器传递“哪些运动是可执行的”这一关键信号。

### 现有方法的局限

针对上述问题，已有工作尝试了不同路径，但均存在显著局限：

**推理时物理投影**：以**PhysDiff**（Yuan et al., ICCV 2023）为代表的方法，在扩散模型的推理阶段引入物理仿真与跟踪控制器，对每一步去噪结果进行物理投影，以消除视觉瑕疵。这种方法虽然能改善生成运动的物理合理性，但计算代价高昂——每次推理都需要在线运行完整的物理仿真与控制循环。更重要的是，它仅在推理时“修正”运动，而非从根本上改变生成模型的内部表示，导致生成器本身仍然可能输出物理上不可行的候选运动。

**可微分目标引导**：**DNO**（Karunratanakul et al., CVPR 2024）通过优化扩散噪声来满足可微分目标函数，提供了一种灵活的生成引导框架。然而，该方法缺乏物理可行性信号的注入机制——它没有与物理仿真或控制策略建立联系，因此无法评估生成运动在下游跟踪任务中的实际表现。

**强化学习控制策略**：另一类工作专注于训练高性能的模仿策略，使物理角色能够跟踪给定的运动参考。这些策略虽然具备一定的鲁棒性，但其能力边界受限于训练数据的分布。当参考运动严重偏离训练分布时，跟踪质量急剧下降。然而，这类方法并未向上游的生成模型反馈这一信息，使得生成器与控制器的能力脱节。

### 本文动机：将物理理解注入生成过程

本文的核心动机在于**弥合运动学生成与物理执行之间的鸿沟**。作者观察到，预训练的跟踪控制策略本身蕴含了丰富的物理知识——它隐式地编码了“在当前状态下，哪些运动参考是可执行的、哪些会导致失败”这一关键信息。如果能将这种物理理解以可微分的形式反馈给生成模型，就有可能在保持生成多样性的同时，使生成的运动天然具备物理可行性。

基于这一洞察，本文提出训练一个**边缘化奖励代理（Critic）**，该网络仅基于运动学参考运动预测下游跟踪任务的预期累计回报。这个 Critic 充当了物理可行性的可微分替身，使得生成模型可以在微调阶段直接优化运动的“可执行性”，而无需频繁调用昂贵的物理仿真。最终，这一思路演化为**Robot Motion Diffusion Model（RobotMDM）**——一个文本条件的运动学扩散模型，与基于强化学习的跟踪控制器无缝衔接，能够生成既保持语义多样性又具备物理合理性的运动，并可直接部署于仿真与真实机器人系统。

## 核心创新

RobotMDM 的核心创新在于**将物理可行性偏好注入运动学扩散模型，而不牺牲其语义多样性与生成质量**。该方法并非重新设计生成架构，而是通过一个可微分、计算高效的奖励代理（Critic），在微调阶段将下游跟踪控制器的物理理解“蒸馏”进预训练的运动扩散模型。

### 瓶颈与因果杠杆

现有运动学生成模型（如 **MDM**，Tevet et al., ICLR 2023）虽能产生视觉上吸引人的运动，但缺乏物理约束，导致生成的 kinematic 动作包含漂浮、脚底滑动、自碰撞、关节限位违反和动力失衡等瑕疵。核心瓶颈在于：**这些运动无法被下游的物理跟踪控制器准确执行**，因而不能直接部署于真实机器人系统。

RobotMDM 的因果杠杆是**训练一个边缘化奖励代理（Critic）**。该 Critic 仅基于运动学参考运动 $m$ 预测跟踪策略的预期累计回报 $v(m)$，而无需访问机器人的完整物理状态 $s$。这一设计使其成为一个可微分的物理可行性替身：在微调扩散模型时，Critic 可以直接作为损失项参与梯度反传，无需频繁调用昂贵的物理仿真。

### 关键 changed slots

相较于基线 MDM，RobotMDM 在以下三个维度引入了实质性改变：

**1. 损失函数：从纯运动学重建到物理偏好引导**

基线 MDM 仅使用标准运动学重建损失：
$$\mathcal{L}_{MDM} = \| M_0 - p^{\phi}(M_d, d, c) \|_2^2$$

RobotMDM 在此基础上引入 Critic 估计的期望奖励作为正则项：
$$\mathcal{L}_{RobotMDM} = \mathcal{L}_{MDM} - \beta \sum_{t=0}^{|M|} v^{\theta}(m_t)$$

负的 Critic 值之和鼓励生成模型产生 Critic 评分更高的运动——即那些跟踪控制器能够更准确执行的物理可行运动。权重 $\beta$ 控制物理偏好与运动学保真度之间的平衡。

**2. 物理可行性反馈：从无信号到边缘化 Critic 代理**

基线 MDM 没有任何显式的物理可行性信号。RobotMDM 引入的边缘化 Critic 网络 $v^{\theta}(m)$ 由 PPO 风格的 GAE 训练得到（见 Algorithm 1）。其训练过程如下：

- 价值函数定义（仅依赖运动参考 $m$）：
$$v(m) = \mathbb{E}_{\substack{s_{0:\infty} \\ m_{0:\infty}}} \left[ \sum_{t=0}^{\infty} \gamma^t r_t \middle| m_0 = m, \pi \right]$$

- 使用截断 GAE 计算价值目标：
$$\hat{v}_t = v_t^{\theta} + \sum_{t'=t}^{T-1} (\gamma \lambda)^{(t'-t)} \delta_{t'}, \quad \delta_t = r_t + \gamma v_{t+1}^{\theta} - v_t^{\theta}$$

- 通过均方误差优化 Critic：
$$\min_{\theta} \sum \| \hat{v}_t - v_t^{\theta} \|_2^2$$

关键设计在于 Critic 仅接收运动参考 $m$ 作为输入，而非完整的 $(s, m)$ 对。这种“边缘化”使得 Critic 可以在扩散模型的运动空间上直接提供梯度信号，成为连接运动学生成与物理跟踪的桥梁。

**3. 微调策略：从单阶段预训练到两阶段物理对齐**

基线 MDM 仅进行运动学预训练。RobotMDM 采用两阶段流程：

- **第一阶段（Critic Training）**：利用预训练的模仿策略（Actor）在仿真环境中交互，收集轨迹并训练 Critic 网络。此阶段 Critic 学习评估“给定一段运动参考，Actor 能多好地跟踪它”。
- **第二阶段（Physical Alignment）**：冻结 Critic 网络，使用 $\mathcal{L}_{RobotMDM}$ 对预训练的 MDM 进行额外 400k 步微调。此阶段将物理可行性偏好注入生成模型，使其学会在保持语义多样性的前提下，自动偏向物理上可执行的运动。

### 方法谱系与知识库定位

RobotMDM 处于**运动学运动生成**与**物理角色控制**的交叉点，其方法谱系可定位如下：

- **上游基础**：基于 **MDM**（Tevet et al., ICLR 2023）的文本条件扩散生成框架，提供多样化的运动先验。
- **并行对比**：**PhysDiff**（Yuan et al., ICCV 2023）在推理时使用跟踪控制器与物理仿真投影运动以消除视觉瑕疵，但每次采样需在线仿真；**DNO**（Karunratanakul et al., CVPR 2024）通过优化扩散噪声满足可微分目标，但不涉及物理可行性信号。RobotMDM 与二者的本质区别在于：将物理理解**融入生成模型内部**，而非仅在推理时后处理。
- **独特贡献**：首次将边缘化 Critic 作为奖励代理用于微调运动学扩散模型，实现了物理可行性与语义多样性的联合优化，且推理时无需额外仿真开销。

### 创新边界与局限

需注意该创新的适用范围：

- Critic 提供的是**软性可行性偏好**，而非硬物理约束。生成的运动仍可能违反关节限位或产生不安全动作——Critic 仅使其概率降低，无法保证绝对安全。
- Critic 的训练依赖于预训练的 Actor 策略。若 Actor 本身泛化能力有限，Critic 的指导信号将受限于该策略的能力边界，难以推广至全新运动模式。
- 数据集与角色高度特定：当文本提示严重超出角色能力范围时，Critic 可能缺乏有效信号，此时物理对齐的效果需要手动验证。

## 整体框架

![[assets/figures/papers/paper_list_l50_https_doi_org_10_1145_3680528_3687626/figures/001_Figure_1.jpg]]
*Figure 1: Robot Motion Diffusion Model (RobotMDM) generates motions that are physics-aware and respect character limits. Our method enables the seamless integration of kinematic motion generators with physics-based character control and can be deployed on robots. The example shows a robot performing the prompt "a person who performed a right-handed uppercut."*

RobotMDM 的整体流程围绕三个核心模块展开，形成“评价—对齐—部署”的闭环，如 Figure 2 所示。该框架将运动生成与运动跟踪解耦，利用预训练的运动扩散模型（MDM）提供多样化的运动先验，同时引入一个边缘化 Critic 作为物理可行性的可微分替身，在微调阶段将物理理解注入采样过程。

### 三阶段流程

1. **Critic 训练（Critic Training）**：在预训练的模仿策略（Actor）与环境交互的基础上，训练一个价值网络 $v^\theta(m)$。该 Critic 仅接收当前运动参考 $m_t$ 作为输入，输出对该参考下策略预期累积折扣回报的估计，即 $v(m) = \mathbb{E}_{s_{0:\infty}, m_{0:\infty}}\left[\sum_{t=0}^{\infty} \gamma^t r_t \mid m_0=m, \pi\right]$。训练使用 PPO 风格的截断 GAE（广义优势估计）计算价值目标，并通过均方误差进行优化（Algorithm 1）。这一阶段将 RL 价值函数在状态空间上边缘化，得到仅依赖运动参考的奖励代理。

2. **物理对齐（Physical Alignment）**：冻结 Critic 网络，将其作为可微分的物理可行性评价器，对预训练的 MDM 进行微调。微调损失在标准运动学重建损失 $\mathcal{L}_{MDM}$ 的基础上，加入负的 Critic 值之和作为奖励项：

   $$\mathcal{L}_{RobotMDM} = \mathcal{L}_{MDM} - \beta \sum_{t=0}^{|M|} v^\theta(m_t) \quad \text{(Eq. 7)}$$

   其中 $\beta$ 控制物理可行性偏好的强度。该损失鼓励扩散模型生成 Critic 评价值更高（即更可能被 Actor 成功跟踪）的运动序列。微调持续 400k 步（约 12 小时训练），无需在线仿真即可将物理约束融入生成过程。

3. **部署（Deployment）**：微调后的 RobotMDM 与预训练的 Actor 串联运行——RobotMDM 根据文本提示生成运动学参考运动，Actor 接收该参考并输出物理动作，直接控制仿真或真实机器人。

### 模块间关系

- **MDM（运动扩散模型）** 基于 **Tevet et al., ICLR 2023**，负责文本条件的运动生成，提供多样化的运动候选。
- **Actor（控制策略）** 为预训练的 VMP 模仿策略，在 Critic 训练阶段用于环境交互以生成奖励信号，在部署阶段负责将运动参考转化为物理动作。
- **Critic（奖励代理）** 是连接运动生成与物理跟踪的关键桥梁：它将下游跟踪任务的期望回报转化为仅依赖运动参考的可微分信号，使生成模型在无需频繁仿真的情况下获得物理可行性指导。

### 输入输出流

- **输入**：文本提示（如 “a person who performed a right-handed uppercut”），通过 MDM 的文本编码器转化为条件信号。
- **中间表示**：运动序列编码为 $n \times (7+2j)$ 矩阵，包含根部位高度、线速度、角速度、根姿态及各关节的位置与速度信息。
- **输出**：物理可行的运动学参考运动，可直接馈入 Actor 生成关节扭矩等物理动作，部署于仿真或真实机器人平台。

## 核心模块与公式推导

RobotMDM 的核心架构由三个解耦模块构成，通过两阶段训练将物理可行性注入运动学扩散模型。

### 模块一：Actor（控制策略）

Actor 是一个预训练的模仿策略（VMP policy），接收运动学参考运动 $m$ 并输出物理动作，驱动物理仿真器中的机器人角色。该策略在 Critic 训练阶段负责与环境交互，产生状态转移和奖励信号，但本身在后续物理对齐阶段保持冻结。Actor 的存在使得 Critic 能够以“下游任务执行者”的身份评估任意运动参考的实际可跟踪性。

### 模块二：MDM（运动扩散模型）

MDM 基于 **MDM**（Tevet et al., ICLR 2023）的文本条件运动学扩散模型，负责从文本提示生成多样化的候选运动。其标准训练损失为运动重建损失：

$$\mathcal{L}_{MDM} = \| M_0 - p^{\phi}(M_d, d, c) \|_2^2 \tag{6}$$

其中 $M_0$ 为原始干净运动，$M_d$ 为加噪运动，$d$ 为扩散时间步，$c$ 为文本条件，$p^{\phi}$ 为去噪网络预测。该模块提供丰富的运动先验，但不包含任何物理可行性信息。

### 模块三：Critic（奖励代理）

Critic 是 RobotMDM 的核心创新模块，作为物理可行性的可微分替身。其设计目标是在**不访问当前状态 $s$** 的情况下，仅基于运动参考 $m$ 预测 Actor 执行该参考时的期望累计奖励：

$$v(m) = \mathbb{E}_{\substack{s_{0:\infty} \\ m_{0:\infty}}} \left[ \sum_{t=0}^{\infty} \gamma^t r_t \middle| m_0 = m, \pi \right] \tag{1}$$

与之对比，标准 RL 价值函数同时依赖状态和运动参考：

$$v^{\mathrm{RL}}(s,m) = \mathbb{E}_{\substack{s_{1:\infty} \\ a_{0:\infty} \\ m_{1:\infty}}} \left[ \sum_{t=0}^{\infty} \gamma^t r_t \middle| s_0 = s, m_0 = m, \pi \right] \tag{2}$$

Critic 的关键性质在于：它本质上是 RL 价值函数在运动空间上的**边缘化**，将状态维度的不确定性隐式吸收进期望中。这使得 Critic 可以直接以运动 $m$ 为输入，输出标量可行性评分，从而作为可微分损失函数接入扩散模型的微调。

#### Critic 训练过程

Critic 采用 PPO 风格的 GAE（Generalized Advantage Estimation）进行训练。时序差分误差定义为：

$$\delta_t = r_t + \gamma v_{t+1}^{\theta} - v_t^{\theta} \tag{4}$$

截断 GAE 价值目标为：

$$\hat{v}_t = v_t^{\theta} + \sum_{t'=t}^{T-1} (\gamma \lambda)^{(t'-t)} \delta_{t'} \tag{3}$$

Critic 网络参数 $\theta$ 通过均方误差优化：

$$\min_{\theta} \sum \| \hat{v}_t - v_t^{\theta} \|_2^2 \tag{5}$$

训练数据来自 Actor 在仿真环境中跟踪数据集中运动片段的 rollout，Critic 仅接收运动参考作为输入，学习预测 Actor 的跟踪表现。

### 模块四：Physical Alignment（物理对齐）

物理对齐阶段将冻结的 Critic 接入 MDM 的微调过程。核心操作是在 MDM 标准重建损失上叠加 Critic 估计的负期望奖励，形成 RobotMDM 损失：

$$\mathcal{L}_{RobotMDM} = \mathcal{L}_{MDM} - \beta \sum_{t=0}^{|M|} v^{\theta}(m_t) \tag{7}$$

其中 $\beta$ 为平衡系数，$v^{\theta}(m_t)$ 为 Critic 对运动片段第 $t$ 帧的期望奖励估计。最大化 $\sum_t v^{\theta}(m_t)$ 等价于鼓励生成运动在 Critic 评估下获得更高的物理可行性分数。由于 Critic 完全可微分，该损失可以直接通过梯度反向传播更新 MDM 的去噪网络参数。

微调在 MDM 预训练完成后进行，额外训练 400k 步（约 12 小时），Critic 与 Actor 均保持冻结。这一设计将物理理解注入采样过程，无需在微调期间进行在线仿真，实现了计算效率与物理可行性的解耦。

### 部署流程

部署时将微调后的 RobotMDM 与 Actor 串联：RobotMDM 根据文本提示生成运动参考序列，Actor 逐帧跟踪该参考并输出物理动作，直接在仿真或真实机器人上执行。整个流程无需在线优化或物理投影。

## 实验与分析

### 运动学生成质量与物理可行性

**Table 2** 报告了运动学生成质量、多样性与物理可行性的综合对比。RobotMDM 在 **Realism 分数**上达到 9.562 ± 0.017，显著优于 MDM 基线的 8.782 ± 0.018，同时保持与 MDM 相当的生成质量（FID 0.571 vs 0.544）和多样性（Diversity 9.302 vs 9.316）。这一结果表明，通过 Critic 微调注入的物理可行性偏好并未损害扩散模型的语义多样性与文本匹配能力。值得注意的是，RobotMDM 在 **R-Precision top‑3** 上达到 0.684，为所有方法中最高，说明物理对齐甚至轻微改善了文本‑运动一致性。

![[assets/figures/papers/paper_list_l50_https_doi_org_10_1145_3680528_3687626/figures/004_Table_2.jpg]]
*Table 2: Kinematic Motion Generation. Comparative evaluation of various kinematic motion generation methods across multiple metrics for quality, diversity, and feasibility. Best and second best (excluding the dataset itself ). ± indicates the 95% confidence interval*

**Figure 3** 进一步揭示了可行性提升的统计分布特征。对 10,000 个随机生成的运动样本，RobotMDM 的 Realism 分数分布整体右移，互补累积分布函数（CCDF）显示高可行性区域的概率质量明显增加。这意味着 Critic 微调并非仅提升少数样本的极端值，而是系统性地将生成分布推向物理可行域。

![[assets/figures/papers/paper_list_l50_https_doi_org_10_1145_3680528_3687626/figures/005_Figure_3.jpg]]
*Figure 3: (b) CCDF. Fig. 3. Comparison of MDM and RobotMDM methods for 10000 randomlygenerated motions. (a) Distribution of Realism scores. RobotMDM shows a shift towards higher values, indicating improvements in feasibility. (b) Complementary Cumulative Distribution Function of the motion Realism values shown in (a). RobotMDM motions demonstrate significantly higher values. Anecdotally, values above 9.0 correspond to well-tracked motions*

定性层面，**Figure 4** 展示了“踢腿”和“坐下”两个典型动作。MDM 生成的踢腿动作幅度过大，超出角色平衡极限；坐下动作则出现漂浮和脚底滑动。RobotMDM 在保留语义上下文的前提下，自动将动作幅度收缩至角色物理能力范围内，生成更平衡、可执行的姿态。**Figure 5** 的“手臂抬起”示例表明，RobotMDM 能自然规避自碰撞——因为 Critic 在训练中已将碰撞导致的低跟踪奖励编码为负值信号。

![[assets/figures/papers/paper_list_l50_https_doi_org_10_1145_3680528_3687626/figures/006_Figure_4.jpg]]
*Figure 4: prompt: a worker sits at a circuit board. Fig. 4. Realistic Motion Generation. Aligning the motion diffusion model with physical knowledge results in more realistic motions within the character’s limits while preserving the context. This results in a less extreme kick where the character also remains more balanced, or a sitting motion that is feasible in the absence of a chair*

![[assets/figures/papers/paper_list_l50_https_doi_org_10_1145_3680528_3687626/figures/007_Figure_5.jpg]]
*Figure 5: prompt: a figure raises their right hand in a sweeping motion Fig. 5. Collision Avoidance. Collisions between bodies results in a lower reward, because they are not accurately tracked by the policy. The aligned RobotMDM naturally circumvents collisions*

### 模拟跟踪性能

**Table 3** 在 2,048 个 30 秒仿真片段上定量评估了跟踪精度。RobotMDM 在所有指标上均大幅优于 MDM 基线：

![[assets/figures/papers/paper_list_l50_https_doi_org_10_1145_3680528_3687626/figures/008_Table_3.jpg]]
*Table 3: Motion Tracking. Evaluation of tracking performance across linear and angular root velocity, root rotation, and upper and lower body Degrees of Freedom (DoFs) tracking, measured over 2048 simulations of 30-second references from motions generated by MDM and RobotMDM*

- **下肢自由度跟踪误差**：11.44 vs 16.11（↓ 29.0%），说明物理对齐对腿部姿态的改善最为显著；
- **根旋转误差**：2.34 vs 4.13（↓ 43.3%），几乎减半，验证了 RobotMDM 生成的姿态更平衡；
- **线速度跟踪误差**：3.43 vs 4.90 m/s（↓ 30.0%），角速度误差 0.23 vs 0.29 rad/s（↓ 20.7%）；
- **上肢自由度误差**：5.42 vs 6.02（↓ 10.0%），改善幅度相对较小，这与上肢动作本身物理约束较弱一致。

这些结果表明，Critic 提供的软性可行性偏好虽不包含硬约束，但足以在统计意义上显著提升下游控制器的跟踪精度。下肢和根旋转的突出改善印证了核心瓶颈——平衡相关瑕疵（漂浮、滑动）是导致跟踪失败的主因，而 RobotMDM 有效缓解了这一问题。

### 真实机器人部署

**Figure 6** 和 **Figure 7** 展示了真实机器人上的定性对比。MDM 生成的运动在真实系统中难以跟踪：缺乏平衡导致机器人无法准确匹配目标姿态，出现明显的跟踪漂移。相同文本提示下，RobotMDM 的运动能够被更精准地执行，机器人动作更稳定、更贴合参考轨迹。这验证了在仿真中训练的 Critic 所编码的物理知识可迁移至真实硬件场景。

### 失败模式与局限

尽管整体性能显著提升，方法存在以下已知局限：

1. **软约束的边界失效**：Critic 仅提供可行性偏好而非硬约束，当文本提示严重超出角色能力（如要求机器人执行后空翻）时，生成的运动仍可能包含不可执行的成分。此时 Critic 缺乏有效训练信号，无法提供有意义的梯度指导。

2. **角色‑数据耦合**：Realism 分数的评估依赖于特定角色的 Critic 网络。若角色动力学参数（质量、摩擦系数）发生变化，Critic 需要重新训练，泛化成本较高。

3. **工程部署因素**：真实机器人部署中，通信延迟和执行器带宽限制可能导致仿真中可行的运动在硬件上仍出现跟踪偏差，本文未对此进行系统鲁棒性分析。

4. **Actor 依赖上限**：Critic 的训练依赖于预训练跟踪控制器的性能天花板。若 Actor 本身对某些运动模式的泛化能力有限，Critic 的指导信号将在这些区域变得不可靠，从而限制 RobotMDM 的可行运动空间。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_doi_org_10_1145_3680528_3687626/figures/003_Table_1.jpg]]
*Table 1: Training Parameters*

## 方法谱系与知识库定位

### 方法在谱系中的位置

RobotMDM 处于**运动学生成模型**与**物理角色控制**的交汇地带，其核心贡献在于为二者提供了一种解耦但可微的对齐机制。从谱系上看，该方法继承了三条技术路线：

**运动扩散生成**：RobotMDM 直接构建于 **MDM**（Tevet et al., ICLR 2023）之上，复用其文本条件的扩散框架作为运动先验。与 MDM 的纯运动学训练不同，RobotMDM 在预训练后追加了物理对齐微调阶段，使生成分布从“视觉合理”向“物理可行”偏移。

**物理投影后处理**：**PhysDiff**（Yuan et al., ICCV 2023）在推理时通过跟踪控制器与物理仿真将生成的运动投影到可行域，以消除漂浮、滑动等视觉瑕疵。RobotMDM 与此路线有本质区别：它将物理知识注入生成模型内部（微调阶段），而非作为外部的推理时修正器。这避免了投影步骤可能引入的语义漂移，且不增加推理计算开销。

**扩散噪声优化**：**DNO**（Karunratanakul et al., CVPR 2024）通过优化扩散噪声来满足可微分目标函数，提供了一种在采样过程中注入偏好的通用框架。RobotMDM 的物理对齐可视为 DNO 思路的一个特例，但其关键创新在于使用边缘化 Critic 作为奖励代理——该 Critic 仅依赖运动学参考即可预测下游跟踪的期望回报，无需在线仿真即可提供物理可行性信号。

**边缘化 Critic 的谱系渊源**：在 RL 中，边缘化价值函数曾被用于课程学习（curriculum learning），通过仅依赖上下文预测期望回报来塑造训练分布。RobotMDM 将这一思想迁移到生成模型的微调场景：Critic 在运动空间上对状态进行边缘化，输出 $v^{\theta}(m)$，从而为扩散模型提供逐帧的可微分物理评分。

### 适用边界

- **角色特定性**：整个管线——包括 Actor、Critic 和微调后的 RobotMDM——均针对特定双足机器人角色的动力学参数和运动数据集训练。更换角色（如不同质量分布、关节构型）需要重新训练 Critic 和微调。
- **运动覆盖依赖**：Critic 的训练信号来自 Actor 在数据集运动上的跟踪表现。当文本提示严重超出数据集的运动覆盖范围时，Critic 的评估可能缺乏有效指导，导致微调效果退化。
- **软约束本质**：Critic 提供的是期望奖励的连续偏好信号，而非硬物理约束。这意味着生成的运动仍可能违反关节限位、产生自碰撞或动力失衡——只是概率显著降低。在安全关键场景中，该方法不能替代显式约束。
- **Actor 能力上限**：Critic 的指导质量受限于预训练 Actor 的泛化能力。若控制策略本身无法跟踪某类运动模式，Critic 将学会对其赋予低值，从而抑制生成模型探索该区域——这既是物理对齐的机制，也是多样性的潜在天花板。

### 局限与开放问题

**已确认的局限**：
1. 无硬约束保证：Critic 仅提供软性可行性偏好，无法确保生成的运动绝对安全或不违反物理限制。
2. 角色与数据集绑定：生成质量依赖于特定角色的运动数据覆盖，泛化至新角色需重新训练。
3. 真实部署的工程差距：真实机器人部署受通信延迟、执行器带宽等因素影响，本文未进行系统鲁棒性分析。
4. Actor 依赖瓶颈：Critic 训练依赖固定 Actor，若 Actor 泛化有限，则 Critic 的指导无法推广至全新运动模式。

**开放问题**：
- **硬约束嵌入**：能否将接触力约束、驱动饱和等硬物理条件显式嵌入扩散模型（如通过约束采样或投影层），以实现更严格的可行性保证？
- **联合训练范式**：当前 Critic 与生成模型分阶段训练，Actor 保持冻结。能否设计联合优化框架，使 Critic 和生成模型协同进化，突破固定 Actor 带来的上限？
- **动力学自适应**：当角色动力学参数（质量、摩擦系数等）发生变化时，Critic 需要多快重新适应？是否可能训练一个以动力学参数为条件的 Critic，实现跨角色的零样本迁移？
- **可扩展性**：该方法在更复杂的形态（如四足机器人、带手爪的移动操作平台）或更大规模运动数据集上的表现尚待验证。Critic 的边缘化假设在更高维运动空间中是否仍然有效，值得进一步研究。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/Robot_Motion_Diffusion_Model_Motion_Generation_for_Robotic_Characters.pdf]]
