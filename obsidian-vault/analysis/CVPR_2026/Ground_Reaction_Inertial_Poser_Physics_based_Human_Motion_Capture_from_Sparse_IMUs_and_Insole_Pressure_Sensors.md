---
title: "Ground Reaction Inertial Poser: Physics-based Human Motion Capture from Sparse IMUs and Insole Pressure Sensors"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Ground_Reaction_Inertial_Poser_Physics_based_Human_Motion_Capture_from_Sparse_IMUs_and_Insole_Pressure_Sensors.pdf
project_link: "https://ryosukehori.github.io/grip-project/"
code_link: null
aliases:
- Ground_Reaction_
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过KinematicsNet估计运动学状态，DynamicsNet在物理模拟器中控制人形机器人，并引入状态差异与摔倒恢复机制，用少量传感器实现物理一致的全身体运动重建。
primary_logic: 融合脚底压力动态线索与惯性信息，借助强化学习驱动的物理仿真，无需绝对位置即可实现高精度且物理合理的人体运动捕捉。
claims:
- GRIP在PRISM、UnderPressure、PSU-TMM100三个数据集上均取得最优全局位置误差（MPJPE）。
- GRIP在所有数据集上脚穿透误差（FP）最低。
- 添加足底压力可将6 IMU配置的MPJPE从160.76 mm降至143.06 mm。
- 状态差异中含速度与相对关节位置差异后，MPJPE从290.71 mm大幅降至182.44 mm。
---

# Ground Reaction Inertial Poser: Physics-based Human Motion Capture from Sparse IMUs and Insole Pressure Sensors

> [!tip] 核心洞察
> 融合脚底压力动态线索与惯性信息，借助强化学习驱动的物理仿真，无需绝对位置即可实现高精度且物理合理的人体运动捕捉。

| 字段 | 内容 |
|------|------|
| 中文题名 | 稀疏IMU与足底压力驱动的物理仿真人体运动捕捉 |
| 英文题名 | Ground Reaction Inertial Poser: Physics-based Human Motion Capture from Sparse IMUs and Insole Pressure Sensors |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.16233) · [Project](https://ryosukehori.github.io/grip-project/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | GRIP |
| Dataset | PRISM, UnderPressure, PSU-TMM100 |

> [!tip] 效果简介
> - PRISM 上，MPJPE (mm) ↓ 182.44 vs 198.30 (GlobalPose) (-15.86)。
> - UnderPressure 上，MPJPE (mm) ↓ 218.09 vs 301.12 (GlobalPose) (-83.03)。
> - PSU-TMM100 上，MPJPE (mm) ↓ 118.60 vs 175.96 (GlobalPose) (-57.36)。

## 概述

**核心问题**：基于稀疏惯性测量单元（IMU）的人体运动捕捉系统缺乏绝对位置信息，导致估计的全局轨迹随时间漂移，且常出现脚部滑动、穿地等物理不合理现象。仅靠足底压力传感器同样难以重建全身运动与全局位移，而现有物理优化方法多采用后处理接触约束，无法在推理过程中自然产生物理一致的足-地交互。

**核心方法**：本文提出**GRIP（Ground Reaction Inertial Poser）**——一种融合稀疏IMU与足底压力信号的物理仿真人体运动捕捉框架。GRIP仅需四个可穿戴设备（双腕智能手表与鞋垫内嵌传感器），通过观测器-控制器架构实现物理一致的全身体运动重建：**KinematicsNet**从传感器数据估计运动学状态（关节位置、旋转、速度），**DynamicsNet**基于强化学习在物理模拟器中控制人形机器人，并引入**状态差异**机制与**摔倒恢复**策略，避免传统速度积分漂移，保证推理的物理合理性与连续性。

**核心结论**：
- GRIP在PRISM、UnderPressure、PSU-TMM100三个数据集上均取得**最优全局位置误差（MPJPE）**，较最强基线GlobalPose分别降低15.86 mm、83.03 mm和57.36 mm（Table 1）。
- 在所有数据集上，GRIP的**脚穿透误差（FP）最低**，脚滑动指标与物理优化方法相当，显著优于纯运动学方法FoRM（Table 1）。
- 消融实验证实，足底压力信息可将6 IMU配置的MPJPE从160.76 mm降至143.06 mm（Table 3）；状态差异中引入速度与相对关节位置差异后，MPJPE从290.71 mm大幅降至182.44 mm（Table 4）。

**方法定位**：GRIP区别于现有基于后处理物理优化的方法（如PIP、GlobalPose、MobilePoser），将物理仿真直接嵌入推理循环，通过强化学习控制的PD力矩驱动人形机器人，实现自然的足-地接触与全局位移估计。与仅依赖足底IMU+压力的SolePoser和FoRM相比，GRIP同时利用腕部IMU的运动学线索，实现了更完整的全身体姿态重建。

## 背景与动机

人体运动捕捉是计算机视觉与图形学中的基础问题，广泛应用于虚拟现实、具身智能与运动分析。传统光学动捕系统依赖多相机、标记点与受控环境，成本高昂且难以部署于日常场景。近年来，基于惯性测量单元（IMU）的稀疏传感器方案因其便携性和环境无关性受到关注，仅需数个穿戴式传感器即可估计全身运动。

然而，稀疏IMU系统面临一个根本性瓶颈：**缺乏绝对位置信息**。现有方法通常依赖速度积分来恢复全局位移，但IMU加速度的双重积分会累积显著漂移，导致轨迹偏离真实路径。同时，纯运动学方法缺乏物理约束，重建结果常出现**脚部滑动、地面穿透**等物理不真实现象，严重损害运动自然度。另一方面，仅依赖足底压力传感器的方法（如SolePoser）虽能捕获足-地接触动态，却难以重建上肢姿态与全局位移。

现有物理优化方法（如PIP、GlobalPose、MobilePoser）尝试在后处理阶段引入接触约束以缓解上述问题，但它们通常采用**固定接触假设**，无法模拟自然的足-地交互动力学，且仍依赖速度积分，漂移问题未从根源解决。FoRM虽融合足底IMU与压力信号，但完全放弃物理建模，运动合理性无法保证。

本文的核心动机在于：**脚底压力信号蕴含丰富的动态线索**，可反映足部是否触地、承重分布及运动相位。若能将这些动态线索与IMU惯性信息深度融合，并借助物理仿真器强制执行物理定律，则有望在无需绝对位置传感的条件下，实现**高精度且物理一致的全身体运动重建**。为此，本文提出**GRIP（Ground Reaction Inertial Poser）**，通过“运动学观测—物理控制”的双模块架构，用强化学习驱动仿真人形机器人，从根本上解决漂移与物理不真实问题。

## 核心创新

GRIP的核心创新在于将**足底压力动态线索**与**强化学习驱动的物理仿真**深度融合，以极少量传感器（4个IMU+鞋垫压力）实现物理一致的全身体运动捕捉，解决了稀疏IMU系统长期面临的轨迹漂移与物理不真实（脚滑动、穿地）瓶颈。

### 创新一：足底压力作为动态约束

传统稀疏IMU方法仅依赖惯性信息，缺乏绝对位置参考，导致全局轨迹漂移。GRIP首次将足底压力传感器与IMU协同使用，将压力信号作为足-地接触的动态线索。消融实验证实，在6 IMU配置中增加足底压力后，MPJPE从160.76 mm降至143.06 mm（Table 3），表明压力信息为系统提供了关键的接地约束，有效抑制了漂移。

### 创新二：强化学习物理仿真替代后处理优化

现有方法（如PIP、GlobalPose、MobilePoser）普遍采用**后处理物理优化**，通过固定接触约束修正运动学结果，缺乏真实的足-地交互建模。GRIP改用**基于PPO的DynamicsNet**在物理模拟器中直接控制人形机器人，通过PD控制器将目标关节角转化为关节力矩，实现自然的足-地交互。这一设计使GRIP在所有数据集上取得最低的脚穿透误差（FP），在UnderPressure数据集上FP降至0.00 mm，显著优于物理优化方法（Table 1）。

### 创新三：状态差异机制规避积分漂移

传统方法通过速度积分估计全局位置，误差随时间累积。GRIP引入**状态差异（State Difference）**机制，计算KinematicsNet估计状态与仿真人形状态的差异，包括关键关节运动差异$D_t^{\text{key}}$与全关节位置差异$D_t^{\text{full}}$。消融实验表明，仅使用方向和加速度差异时MPJPE高达290.71 mm，加入速度与根相对关节位置差异后大幅降至182.44 mm（Table 4），证明了该机制在避免积分漂移中的关键作用。

### 创新四：摔倒恢复机制保障推理连续性

物理仿真在高动量运动中可能发生摔倒，传统方法缺乏有效的恢复策略。GRIP设计了**摔倒恢复机制**：检测摔倒后利用历史缓冲中的KinematicsNet预测替换摔倒段运动输出，并通过运动学根位移$\Delta p_{t-N:t}^{\text{kin,root}}$重置仿真根位置$p_t^{\text{sim,root}} = p_{t-N}^{\text{sim,root}} + \Delta p_{t-N:t}^{\text{kin,root}}$。该机制仅在推理时使用，训练时不引入，定性地保障了运动连续性（补充视频验证）。

### 方法谱系与知识库定位

| 维度 | 现有方法 | GRIP |
|------|---------|------|
| 传感器 | 仅IMU（6或更少） | 4 IMU + 鞋垫压力 |
| 物理建模 | 后处理物理优化（固定接触约束） | 强化学习控制的物理仿真（自然足-地交互） |
| 全局位置 | 速度积分导致漂移 | 状态差异避免积分漂移 |
| 摔倒处理 | 无恢复或依赖外力 | 基于历史缓冲的运动学重置与恢复 |

GRIP在方法谱系中属于**物理仿真驱动的人体运动捕捉**，区别于纯运动学方法（如FoRM、SolePoser）和后处理物理优化方法（如PIP、GlobalPose）。其核心贡献在于将足底压力作为动态先验引入强化学习控制框架，实现了传感器稀疏性与物理真实性的统一。

## 整体框架

GRIP 采用“观测器–控制器”架构，将稀疏可穿戴传感与物理仿真人体运动重建解耦为两个核心阶段：**运动学状态估计**与**物理仿真控制**。整体流程（图2）从四枚IMU与鞋垫压力信号出发，依次经过 KinematicsNet 估计全身运动学状态、状态差异计算模块将估计状态与仿真人形状态对齐，最终由 DynamicsNet 在物理模拟器中以关节力矩驱动人形机器人，实现物理一致的全身体运动重建。

**输入模态**：系统接收四枚IMU信号——两枚位于手腕（如智能手表），两枚嵌入鞋垫——以及鞋垫压力数据。每帧输入包括加速度张量 $\boldsymbol{A}_t \in \mathbb{R}^{4 \times 3}$、方向张量 $\pmb{R}_t \in \mathbb{R}^{4 \times 3 \times 3}$ 和压力值，所有信号经时间同步与坐标系对齐后送入网络。

**KinematicsNet（运动学网络）**：该模块从传感器数据中逐步估计运动学信息，输出四类状态：末端关节位置（leaf-joint positions, LP）、全身关节位置（full-joint positions, FP）、全身关节角（full-body joint angles, FA）和关键关节速度（key-joint velocities, KV）。训练时以MSE损失监督全部四类输出与真值之间的差异：

$$
\mathcal{L}_{\mathrm{Kin}} = \| p^{\mathrm{leaf}} - \hat{p}^{\mathrm{leaf}} \|^2 + \| p - \hat{p} \|^2 + \| \pmb{\theta} - \hat{\pmb{\theta}} \|^2 + \| \pmb{v}^{\mathrm{key}} - \hat{\pmb{v}}^{\mathrm{key}} \|^2
$$

**状态差异（State Difference）**：为避免传统速度积分导致的全局位置漂移，GRIP 不直接将 KinematicsNet 的绝对位置估计送入控制器，而是计算估计状态与当前仿真人形状态之间的差异向量 $D_t = [D_t^{\mathrm{key}}, D_t^{\mathrm{full}}]$，其中 $D_t^{\mathrm{key}}$ 编码关键关节的运动差异（含速度方向差），$D_t^{\mathrm{full}}$ 编码全身关节的相对位置差异。这一设计使得控制器仅需关注“如何纠正当前仿真状态以逼近运动学参考”，而非从零重建全局轨迹——消融实验（Table 4）证实，加入速度与相对关节位置差异后，MPJPE 从 290.71 mm 大幅降至 182.44 mm。

**DynamicsNet（动力学网络）**：该模块将整体框架形式化为马尔可夫决策过程 $\mathcal{M} = \langle \mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \gamma \rangle$，基于 PPO 强化学习训练策略网络。网络以状态差异、仿真人形本体感知（关节角、速度等）和足部压力为观测，输出目标关节角 $\theta_t^*$，再经比例-微分（PD）控制器转化为关节力矩：

$$
\tau_t = k_p (\theta_t^* - \theta_t) - k_d \dot{\theta}_t
$$

奖励函数综合了对抗运动先验（AMP）奖励、模仿奖励和能量惩罚，驱动人形机器人在物理模拟器中产生自然且贴合参考运动的足-地交互。与依赖后处理物理优化的基线方法不同，GRIP 的人形模型**无浮动基座、无残余外力**，完全通过关节力矩与环境交互维持平衡与运动。

**摔倒恢复机制**：高动量或复杂运动中可能发生仿真摔倒。GRIP 在推理时检测摔倒后，利用历史缓冲中的 KinematicsNet 预测替换摔倒段运动输出以保持运动学连续性，并通过缓冲的运动学根位移重置仿真根位置：

$$
p_t^{\mathrm{sim,root}} = p_{t-N}^{\mathrm{sim,root}} + \Delta p_{t-N:t}^{\mathrm{kin,root}}
$$

该机制仅在推理时使用，训练中未引入，定性上可在摔倒后恢复运动连续性（参见补充视频），但可能引入短暂姿态跳变。

### 补充图表

![[assets/figures/papers/paper_list_l1063_https_arxiv_org_abs_2603_16233/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the GRIP framework. Input Data (Sec. 3.1) consists of IMU and insole measurements. KinematicsNet (Sec. 3.2) estimates kinematic states, and the State Difference (Sec. 3.3) compares them with the simulated humanoid. DynamicsNet (Sec. 3.4) drives the humanoid through physics simulation-based control. The PRISM dataset (Sec. 3.5) provides diverse multi-modal data*

![[assets/figures/papers/paper_list_l1063_https_arxiv_org_abs_2603_16233/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed Ground Reaction Inertial Poser (GRIP). (a) GRIP observes motion using four IMUs and foot pressure data from smartwatches and smart insoles. (b) Full-body motion is reconstructed by driving a humanoid with joint torques in a physics simulator. (c) The PRISM dataset offers multimodal measurements, including IMUs, foot pressure, motion data, and environmental data*

## 核心模块与公式推导

GRIP 采用“观测器–控制器”架构，由两个核心网络与状态差异计算模块串联构成（图2）。系统从四枚IMU（双腕、双足）及鞋垫压力传感器获取稀疏观测，最终在物理模拟器中以关节力矩驱动物理一致的全身体人形机器人。

### KinematicsNet：运动学状态估计器

KinematicsNet 从输入传感器数据中递进估计运动学信息，输出四类状态：叶节点位置（LP）、全关节位置（FP）、全身体关节角（FA）和关键关节速度（KV）。叶节点位置指四肢末端在根坐标系下的坐标，为后续状态差异计算提供关键参照。

网络训练采用均方误差损失，同时监督上述四类输出与真值之间的差异：

$$
\mathcal{L}_{\mathrm{Kin}} = \| p^{\mathrm{leaf}} - \hat{p}^{\mathrm{leaf}} \|^2 + \| p - \hat{p} \|^2 + \| \pmb{\theta} - \hat{\pmb{\theta}} \|^2 + \| \pmb{v}^{\mathrm{key}} - \hat{\pmb{v}}^{\mathrm{key}} \|^2 \tag{1}
$$

其中 $p^{\mathrm{leaf}}$ 为叶节点位置，$p$ 为全关节位置，$\pmb{\theta}$ 为关节角，$\pmb{v}^{\mathrm{key}}$ 为关键关节速度，带帽变量表示网络预测值。

### 状态差异：桥接运动学估计与物理仿真

状态差异模块将 KinematicsNet 的估计状态与物理模拟器中的仿真人形状态进行比较，生成差异向量 $D_t$，作为 DynamicsNet 的核心观测输入。差异向量由两部分拼接而成：

$$
D_t = [D_t^{\mathrm{key}}, D_t^{\mathrm{full}}]
$$

- $D_t^{\mathrm{key}}$：关键关节的运动差异，包含速度方向差和相对根关节的位置差；
- $D_t^{\mathrm{full}}$：全关节位置差异。

消融实验（Table 4）表明，仅包含方向和加速度差异时 MPJPE 高达 290.71 mm，加入速度和根相对关节位置差异后大幅降至 182.44 mm，验证了速度方向差对抑制积分漂移的关键作用。

### DynamicsNet：物理仿真控制器

DynamicsNet 基于 PPO 强化学习策略网络，在物理模拟器中驱动无浮动基座、无残余力的人形机器人。整体框架建模为马尔可夫决策过程 $\mathcal{M} = \langle \mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \gamma \rangle$，其中状态空间 $\mathcal{S}$ 包含状态差异 $D_t$、仿真人形本体感受信息及 KinematicsNet 估计的目标姿态。

策略网络输出目标关节角 $\theta_t^*$，通过比例-微分（PD）控制器转化为关节力矩：

$$
\tau_t = k_p (\theta_t^* - \theta_t) - k_d \dot{\theta}_t
$$

其中 $k_p$、$k_d$ 分别为比例和微分增益，$\theta_t$ 和 $\dot{\theta}_t$ 为当前仿真关节角与角速度。

训练奖励函数综合三类信号：

$$
r_t = 0.5 r_t^{\mathrm{amp}} + 0.5 r_t^{\mathrm{imit}} + r_t^{\mathrm{energy}}
$$

- **对抗运动先验奖励** $r_t^{\mathrm{amp}}$：基于判别器 $D$ 的奖励，鼓励生成逼真运动：

  $$
  r_t^{\mathrm{amp}} = -\log\left(1 - \sigma\big(D(O_t^{\mathrm{self}})\big)\right) \tag{8}
  $$

- **模仿奖励** $r_t^{\mathrm{imit}}$：衡量仿真运动与 KinematicsNet 参考运动在位置、姿态、线速度、角速度上的差异：

  $$
  r_t^{\mathrm{imit}} = w_p e^{-100\|\hat{p}_t - p_t\|} + w_\theta e^{-100\|\hat{\theta}_t \ominus \theta_t\|} + w_v e^{-10\|\hat{\boldsymbol{v}}_t - \boldsymbol{v}_t\|} + w_\omega e^{-0.1\|\hat{\omega}_t - \omega_t\|} \tag{10}
  $$

  其中 $\ominus$ 表示旋转空间中的差异运算，$w_p, w_\theta, w_v, w_\omega$ 为各分量权重。

- **能量惩罚** $r_t^{\mathrm{energy}}$：抑制过大的关节力矩，提升运动自然度。

### 摔倒恢复机制

当仿真人形摔倒（如躯干高度或朝向异常）时，系统利用历史缓冲中的 KinematicsNet 预测替换摔倒阶段的运动输出，维持运动学连续性。仿真根位置按以下规则重置：

$$
p_t^{\mathrm{sim,root}} = p_{t-N}^{\mathrm{sim,root}} + \Delta p_{t-N:t}^{\mathrm{kin,root}}
$$

即取摔倒前 $N$ 帧的仿真根位置，叠加对应时段内 KinematicsNet 估计的根位移量，实现无缝恢复。该机制仅在推理时启用，训练阶段不引入（见补充视频定性验证）。

## 实验与分析

### 主结果量化对比

GRIP在三个公开数据集上均取得最优全局位置精度，同时实现了最低的物理穿透误差，验证了物理仿真与足底压力融合的有效性。Table 1报告了各方法在PRISM、UnderPressure和PSU-TMM100上的多指标对比。

**全局位置精度（MPJPE）**：GRIP在PRISM上达到182.44 mm，相比最优运动学基线**GlobalPose**（198.30 mm）降低15.86 mm；在UnderPressure上为218.09 mm，较GlobalPose（301.12 mm）大幅降低83.03 mm；在PSU-TMM100上为118.60 mm，较GlobalPose（175.96 mm）降低57.36 mm。UnderPressure上的显著提升表明，在缺乏绝对位置参考的长时间行走场景中，物理仿真对抑制轨迹漂移的作用尤为突出。

**物理合理性指标**：GRIP在所有数据集上取得最低的脚穿透误差（FP）。在UnderPressure上FP为0.00 mm，而物理优化方法**PIP**为1.43 mm；在PRISM上FP为5.77 mm，GlobalPose为9.72 mm。脚滑动（FS）指标方面，GRIP与物理优化方法（PIP、GlobalPose、MobilePoser）处于同一水平，显著优于纯运动学方法**FoRM**，说明物理仿真对足-地接触建模是减少滑动的关键，而GRIP通过强化学习控制的自然交互进一步消除了穿透。

**定性分析**：Figure 3展示了三个数据集上的姿态重建对比。在PRISM的物体踩踏场景中，GRIP准确重建了脚在物体上的放置位置；在UnderPressure的长距离行走中，GRIP的轨迹漂移明显小于基线方法（Figure 5）；在PSU-TMM100的慢速重心转移动作中，GRIP捕捉到了细微的姿态变化。Figure 4的足部接触时序对比表明，GRIP估计的接触标签与真实值高度一致，进一步验证了物理仿真的接触建模能力。

### 传感器配置消融

Table 3对比了不同传感器组合对性能的影响。核心发现：**足底压力的引入在IMU数量减少时补偿效果显著**。6个IMU配置（无压力）的MPJPE为160.76 mm，加入足底压力后降至143.06 mm，降幅约11%。当IMU数量从6个减至4个（GRIP默认配置）时，无压力配置的MPJPE升至178.58 mm，而加入压力后恢复至182.44 mm，接近6 IMU无压力水平。这表明足底压力提供的动态线索（接触状态与地面反作用力）有效弥补了上肢IMU减少带来的运动学信息损失。

### 观测设计消融

Table 4消融了状态差异（State Difference）中不同成分的贡献。**速度差异与根相对关节位置差异是性能的关键驱动因素**。仅使用方向差异和加速度差异时，MPJPE高达290.71 mm；加入关键关节速度差异和全关节位置差异后，MPJPE骤降至182.44 mm，降幅达37%。这一结果表明，KinematicsNet估计的速度信息为DynamicsNet提供了关键的全局运动线索，避免了纯方向信息导致的积分漂移问题；而全关节位置差异则确保了仿真人形与运动学估计在姿态层面的对齐。

### 摔倒恢复机制

摔倒恢复机制仅在推理时使用，训练阶段未引入。该机制通过检测仿真人形摔倒状态，利用历史缓冲中的KinematicsNet预测替换摔倒期间的输出，并在恢复后以运动学根位移重置仿真根位置（公式 $p_t^{\mathrm{sim,root}} = p_{t-N}^{\mathrm{sim,root}} + \Delta p_{t-N:t}^{\mathrm{kin,root}}$）。补充视频定性地展示了该机制在摔倒后恢复运动连续性的效果，但论文未提供定量的恢复成功率或姿态跳变幅度指标，该机制的鲁棒性需要进一步验证。

### 基线与方法特性对比

Table 2从输入模态、输出表示和物理建模三个维度对比了各方法。GRIP的差异化优势在于：(1) 同时使用IMU和足底压力，而**SolePoser**和**FoRM**仅依赖足底传感器；(2) 通过强化学习控制的物理仿真实现自然足-地交互，区别于PIP、GlobalPose等后处理物理优化方法；(3) 输出全局位置，而SolePoser仅输出根相对姿态。Table 5进一步对比了现有含足底压力的人体运动数据集，PRISM在模态丰富度（IMU+压力+动捕+环境数据）上具有独特优势。

### 失败模式与局限

论文明确指出的失败模式包括：(1) 在高动量或复杂运动中可能发生摔倒，摔倒恢复机制依赖历史缓冲，可能引入短暂姿态跳变，该问题在补充视频中有定性展示；(2) 当前仅支持单人运动重建，未扩展到多人交互场景；(3) 训练计算开销大，KinematicsNet约需24小时，DynamicsNet约需48小时，推理速度约28 ms/帧，尚未达到实时；(4) 依赖物理模拟器中的平面地面假设，若真实环境几何复杂，性能可能下降。

### 补充图表

![[assets/figures/papers/paper_list_l1063_https_arxiv_org_abs_2603_16233/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of our method with baseline methods across the three datasets. Lower values indicate better performance for all metrics. Bold numbers denote the best performance for each metric, and underlined numbers denote the second best*

![[assets/figures/papers/paper_list_l1063_https_arxiv_org_abs_2603_16233/figures/004_Table_2.jpg]]
*Table 2: Comparison of input modalities, output representations, and physical modeling across baseline methods*

![[assets/figures/papers/paper_list_l1063_https_arxiv_org_abs_2603_16233/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison of pose estimation results across the three datasets. Our method accurately reconstructs foot placementeq000_008 on objects (PRISM), exhibits less position drift (UnderPressure), and captures slow weight-shifting motions (PSU-TMM100)*

![[assets/figures/papers/paper_list_l1063_https_arxiv_org_abs_2603_16233/figures/006_Figure_4.jpg]]
*Figure 4: Comparison of foot contact timing. Right-foot contact labels during low-speed motions in PSU-TMM100, computed from the estimated GRF of the physics-based methods*

![[assets/figures/papers/paper_list_l1063_https_arxiv_org_abs_2603_16233/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison of estimated poses and root trajectories for a walking sequence from the UnderPressure dataset. Colors correspond to the same methods shown in Fig. 3*

![[assets/figures/papers/paper_list_l1063_https_arxiv_org_abs_2603_16233/figures/008_Table_3.jpg]]
*Table 3: Comparison across different sensor configurations*

![[assets/figures/papers/paper_list_l1063_https_arxiv_org_abs_2603_16233/figures/009_Table_4.jpg]]
*Table 4: Ablation study on observation configuration*

![[assets/figures/papers/paper_list_l1063_https_arxiv_org_abs_2603_16233/figures/014_Table_5.jpg]]
*Table 5: Comparison of human motion datasets utilizing insole-type foot pressure sensors*

![[assets/figures/papers/paper_list_l1063_https_arxiv_org_abs_2603_16233/figures/015_Figure_10.jpg]]
*Figure 10: Comparison between SolePoser and our method using the same 17 joint locations extracted from the SMPL model*

## 方法谱系与知识库定位

### 1. 问题定位：稀疏可穿戴传感的物理合理性瓶颈

现有基于稀疏IMU的人体运动捕捉方法面临两个根本性瓶颈：**绝对位置信息的缺失**导致轨迹漂移，以及**缺乏物理约束**导致重建结果违反物理定律（如脚部滑动、地面穿透）。传统方案通常采用后处理物理优化来缓解这些问题，但其固定接触约束无法模拟自然的足地交互，且依赖速度积分来恢复全局位移，漂移问题仍未解决。

GRIP的切入点在于：将**足底压力**作为动态线索引入，与惯性信息融合，并通过**强化学习驱动的物理仿真**替代后处理优化，使人体模型在仿真器中自然地“行走”，而非通过规则约束来“修正”运动。

### 2. 方法谱系中的位置

#### 2.1 与纯运动学方法的区别

**FoRM** 和 **SolePoser** 代表了仅依赖运动学估计的方案。FoRM使用足底IMU和压力传感器进行姿态估计，但完全不引入物理建模；SolePoser同样使用足底IMU和压力，但仅输出根相对姿态，无法恢复全局位移。这两类方法在脚滑动（FS）指标上表现显著差于物理方法（Table 1），验证了纯运动学方法在物理合理性上的固有缺陷。

GRIP与这些方法的本质区别在于：运动学估计（KinematicsNet）仅作为“观察器”提供参考状态，最终运动由物理仿真器中的PD控制器驱动人形机器人产生，从而天然满足物理约束。

#### 2.2 与后处理物理优化方法的区别

**PIP**（6个IMU + 后处理物理优化）、**GlobalPose**（6个IMU + 物理优化 + 骨盆IMU校正）和**MobilePoser**（3个IMU + 物理优化）代表了当前主流的物理辅助方案。这些方法在运动学估计之后施加物理优化，通过固定接触约束来减少脚滑动和地面穿透。

GRIP与它们的关键差异体现在两个维度：

| 维度 | 后处理物理优化方法 | GRIP |
|------|-------------------|------|
| 物理建模方式 | 后处理阶段施加固定接触约束 | 强化学习控制器在仿真器中实时驱动人形机器人 |
| 足地交互 | 硬约束，无法模拟自然接触动态 | 通过PD控制力矩和奖励函数实现自然交互 |
| 全局位置恢复 | 依赖速度积分，存在漂移 | 通过状态差异（速度方向差）避免积分漂移 |
| 传感器配置 | 6个或更少IMU | 4个IMU + 足底压力 |

定量上，GRIP在三个数据集上均取得了最优的全局位置误差（MPJPE）：PRISM上182.44 mm（GlobalPose为198.30 mm），UnderPressure上218.09 mm（GlobalPose为301.12 mm），PSU-TMM100上118.60 mm（GlobalPose为175.96 mm）（Table 1）。在脚穿透误差（FP）上，GRIP同样在所有数据集上取得最低值（Table 1）。

#### 2.3 技术路线的继承与创新

GRIP的技术架构继承了**AMP（Adversarial Motion Priors）** 的对抗运动先验框架，通过判别器奖励鼓励生成逼真运动。其创新在于：

1. **多模态观测融合**：将足底压力显式编码为输入特征，而非仅依赖IMU信号。消融实验（Table 3）表明，在6个IMU配置下增加足底压力可将MPJPE从160.76 mm降至143.06 mm。

2. **状态差异机制**：不直接将运动学估计作为目标姿态，而是计算估计状态与仿真状态的差异向量 $D_t = [D_t^{\mathrm{key}}, D_t^{\mathrm{full}}]$ 作为控制器的观测。消融实验（Table 4）显示，仅包含方向和加速度差异时MPJPE高达290.71 mm，加入速度和根相对关节位置差异后降至182.44 mm，证明该设计的必要性。

3. **摔倒恢复机制**：在检测到摔倒后，利用历史缓冲中的运动学预测替换摔倒段输出，并通过 $p_t^{\mathrm{sim,root}} = p_{t-N}^{\mathrm{sim,root}} + \Delta p_{t-N:t}^{\mathrm{kin,root}}$ 重置仿真根位置，保证推理连续性。该机制仅在推理时使用，训练时未引入（Sec. 4.1）。

### 3. 适用边界

#### 3.1 传感器假设

GRIP假设使用4个IMU（双腕和双足鞋垫内嵌）和足底压力传感器。这一配置在消费级设备上具有可行性（如Apple Watch配合智能鞋垫），但要求传感器能够提供可靠的姿态和压力读数。对于UnderPressure和PSU-TMM100数据集，由于缺少真实IMU数据，采用从SMPL网格差分合成的IMU信号进行训练和评估，可能高估了IMU信号质量（公平性说明）。

#### 3.2 运动类型限制

当前方法在复杂或高动量运动（如快速转身、跳跃、跌倒后起身）中可能发生摔倒。摔倒恢复机制依赖历史缓冲，可能引入短暂的姿态跳变（论文自述限制）。在PSU-TMM100的低速重心转移动作上，GRIP展现了良好的接触时序估计能力（Figure 4），但在高动态场景下的鲁棒性仍需验证。

#### 3.3 计算资源需求

训练计算资源需求较高：KinematicsNet约需24小时，DynamicsNet约需48小时。推理速度约28 ms/帧，未达到实时（< 16.7 ms/帧），限制了在线应用场景。

### 4. 开放问题

1. **高动量运动的稳定性**：如何设计控制器以更好地估计不稳定或高动量条件下的稳定运动，是当前物理仿真方法的共性问题。可能的改进方向包括引入更丰富的环境交互奖励或采用模型预测控制。

2. **多传感器融合扩展**：如何集成额外传感器（如头戴相机或UWB定位传感器）以进一步减少全局漂移，同时保持系统在消费级设备上的可部署性。

3. **多人场景与动态交互**：当前方法仅支持单人运动重建。扩展到多人场景需要解决人-人遮挡、交互力传递和共享物理空间中的碰撞避免等问题。

4. **环境几何信息的利用**：GRIP依赖物理模拟器，若环境几何信息（如地面高度、障碍物）不准确，可能影响性能。如何从传感器数据中在线估计环境几何，或设计对环境误差鲁棒的控制器，是实用化部署的关键挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/Ground_Reaction_Inertial_Poser_Physics_based_Human_Motion_Capture_from_Sparse_IMUs_and_Insole_Pressure_Sensors.pdf]]