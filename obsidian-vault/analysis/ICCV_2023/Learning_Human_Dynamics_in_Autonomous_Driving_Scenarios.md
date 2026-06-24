---
title: "Learning Human Dynamics in Autonomous Driving Scenarios"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/Learning_Human_Dynamics_in_Autonomous_Driving_Scenarios.pdf
aliases:
- PAMTFHD
- LHDADS
tags:
- ICCV_2023
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "引入物理感知的分层运动控制器，结合强化学习训练的高层控制器和低层运动生成模型，通过预测潜变量和残差，在物理模拟器中逐步生成遮挡帧的运动，并强制符合地形接触，从而填补物理空白。"
primary_logic: "通过将室内训练的运动先验（cVAE）适配到户外不平坦地形，利用地形重建、高度图修复和物理模拟，使分层控制器能够在长时遮挡下生成与视觉证据一致且物理合理的全局人体运动序列。"
claims:
- "与传统方法 GLAMR 相比，本方法在 Waymo Open Dataset 上显著减少了漂浮、滑动和地面穿透伪影"
- "本方法在 FID 指标（所有帧）上达到 1.96，远优于基线"
- "物理感知模仿器有效降低地面穿透、脚滑动和漂浮度"
- "后优化阶段进一步改善了 2D 关键点投影误差和遮挡帧的 PA-MPJPE"
---

# Learning Human Dynamics in Autonomous Driving Scenarios

> [!tip] 核心洞察
> 通过将室内训练的运动先验（cVAE）适配到户外不平坦地形，利用地形重建、高度图修复和物理模拟，使分层控制器能够在长时遮挡下生成与视觉证据一致且物理合理的全局人体运动序列。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 在自动驾驶场景中学习人体动力学 |
| 英文题名 | Learning Human Dynamics in Autonomous Driving Scenarios |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://openaccess.thecvf.com/content/ICCV2023/papers/Wang_Learning_Human_Dynamics_in_Autonomous_Driving_Scenarios_ICCV_2023_paper.pdf) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | Physics-aware motion tracking framework for human dynamics |
| Dataset | Waymo Open Dataset |

> [!tip] 效果简介
> - Waymo Open Dataset 上，FID (All frames) 为 1.96，变化 显著优于 GLAMR 等基线。
> - Waymo Open Dataset 上，Ground Penetration GP (All frames) 为 12.62，变化 显著降低。

## 概述

**核心问题**：从快速移动的车辆摄像头拍摄的单目视频中恢复完整、物理合理的人体三维运动序列。现有最先进方法（如 **GLAMR**，Yuan et al., CVPR 2022）虽然在遮挡感知的全局人体运动恢复上表现突出，但忽略了环境物理约束，导致在遮挡、移动摄像机及复杂地形下产生漂浮、滑动、地面穿透等严重运动伪影，无法恢复物理可信的完整人体动态。

**核心方法**：本文提出一种物理感知的运动跟踪框架，通过三阶段流水线将室内训练的运动先验适配到户外不平坦地形。该方法引入分层运动控制器，结合强化学习训练的高层控制器和低层运动生成模型，在物理模拟器中逐步生成遮挡帧的运动，并强制符合地形接触约束。同时利用 LiDAR 点云重建并修复地形高度图，为物理模拟提供准确的地面几何信息。

**关键发现**：在 Waymo Open Dataset 上的实验表明，该方法显著优于 GLAMR 等基线——在所有帧的 FID 指标上达到 1.96，地面穿透等物理伪影大幅减少。物理感知模仿器和后优化阶段分别对物理合理性和 2D 观测对齐起到关键作用。

**方法定位**：该方法属于物理感知的人体运动捕捉与轨迹填补交叉领域，其核心创新在于将条件变分自编码器（cVAE）运动先验、强化学习控制策略与物理模拟器深度耦合，填补了从纯运动学估计到物理合理动态生成的空白。

## 背景与动机

自动驾驶场景中的人体动力学恢复是理解行人行为、保障安全决策的关键任务。从车载摄像机序列中重建全局一致的人体运动序列，面临移动摄像机视角、严重遮挡和复杂地形等多重挑战。现有最先进的方法，如 **GLAMR**（Yuan et al., CVPR 2022），虽然在遮挡感知的全局人体运动恢复方面取得了显著进展，但其输出普遍存在**物理不合理性**——包括漂浮（floating）、滑动（sliding）和地面穿透（terrain penetration）等伪影（Figure 1）。

这些伪影的根本原因在于，现有方法忽略了**环境的物理约束**。GLAMR 等基于运动学的方法仅考虑关节角度等运动学约束，既不保证脚与地面的接触关系，也不防止身体穿透地形。此外，这些方法通常在室内平坦地面数据上训练，难以适应自动驾驶场景中由 LiDAR 点云重建的不平坦户外地形。当面对长时间遮挡时，基于 transformer 的 cVAE 一次性填补多个缺失帧的策略缺乏逐步的物理反馈，进一步加剧了运动的不真实性。

本文的核心动机正是填补这一**物理空白**：在自动驾驶场景中，仅恢复视觉上一致的运动是不够的，必须保证人体运动在物理世界中是合理且可执行的。为此，本文提出一个物理感知的运动跟踪框架，通过引入强化学习训练的分层运动控制器、物理模拟器中的模仿执行，以及对真实地形的显式建模，系统性地解决上述问题。

## 核心创新

本文的核心创新在于将**物理感知的分层运动控制**引入自动驾驶场景下的人体动态恢复，从根本上解决了现有方法（如 **GLAMR** (Yuan et al., CVPR 2022)）因忽略环境物理约束而产生的漂浮、滑动和地面穿透等伪影。这一创新的因果机制体现在以下四个关键维度：

### 1. 从一次性填补到物理感知的逐步生成

**GLAMR** 采用基于 Transformer 的 cVAE 一次性填补多个缺失帧，仅考虑关节角度等运动学约束，不保证脚部接触和地面穿透的物理合理性。本文提出的分层控制器则采用逐步预测策略：高层控制器 $\pi_C$ 在每个时间步预测运动生成模型所需的潜变量 $z_{t+1}^g$ 和残差 $z_{t+1}^r$，再由物理感知模仿器 $\pi_D$ 在物理模拟器中执行，从而强制每一步生成的运动都符合地形接触和物理定律（Figure 4, Section 3.2.1）。

### 2. 地形适配：从平坦假设到真实地形重建

现有方法普遍忽略真实地形，假设平坦地面，导致户外场景中人体运动与地形严重脱节。本方法首次引入基于 LiDAR 点云的地形重建与高度图修复流程（Figure 3, Section 3.1），通过 Poisson Surface Reconstruction 重建地形网格，并修复无有效 LiDAR 扫描区域的高度图，使物理模拟器能够施加准确的地形接触约束，从而将室内训练的运动先验成功适配到户外不平坦地形。

### 3. 训练数据适应性：合成预训练与真实微调

室内平坦地面数据上训练的运动生成模型 $\pi_M$ 难以直接适应户外复杂地形。本文通过在合成多样地形上预训练高层控制器 $\pi_C$，再在 Waymo Open Dataset 真实数据上微调的策略，显著加快了收敛速度并提升了最终奖励（Figure 6, Section 3.2.2）。这一训练范式的转变使框架能够泛化到未见过的真实驾驶场景地形。

### 4. 后优化阶段：视觉证据与物理约束的联合对齐

在物理感知运动跟踪之后，本文引入第三阶段后优化（Section 3.3），在物理模拟器内基于 2D 关键点投影误差和置信度加权奖励 $r_{proj} = \exp(-\alpha_p \sum(\|\Pi(\overline{j}_t) - \widetilde{j}_t^{2D}\| \times \widetilde{c}_t))$ 进一步优化运动参数。这一阶段显著提升了遮挡帧的 PA-MPJPE 和 2D 关键点投影误差指标（Table 3），使生成的运动在保持物理合理性的同时，与视频视觉证据更加一致（Figure 7）。

**证据强度**：上述创新点的有效性由 Table 1 的 FID 指标（1.96，显著优于基线）、Table 2 的物理指标消融实验（地面穿透、脚滑动、漂浮度均显著降低）以及 Table 3 的后优化消融实验（遮挡帧 PA-MPJPE 和 2D-LE 进一步改善）共同支撑，证据置信度均高于 0.95。

## 整体框架

本文提出一个三阶段物理感知运动跟踪框架，从快速移动车载摄像机拍摄的单目视频中恢复行人的物理合理人体动力学。输入为包含 $M$ 帧的单目视频序列 $\boldsymbol{I} = (I_1, ..., I_M)$，输出为目标行人 $N$ 个完整运动序列在世界坐标系下的物理合理运动 $\{Q^i\}_{i=1}^N$，其中每个运动序列 $Q = (T, R, \Theta)$ 由根平移 $T$、根旋转 $R$ 和身体姿态 $\Theta$ 组成（Figure 2）。

**核心瓶颈**：现有方法（如 **GLAMR**，Yuan et al., CVPR 2022）在遮挡、移动摄像机及复杂地形下产生漂浮、滑动、地面穿透等物理伪影，根源在于其忽略环境物理约束，仅依赖运动学信息一次性填补缺失帧。

**核心思路**：引入物理感知的分层运动控制器，结合强化学习训练的高层控制器和低层运动生成模型，在物理模拟器中逐步生成遮挡帧运动并强制符合地形接触，从而填补物理空白。

### 阶段一：运动与地形准备

首先利用现成的运动捕捉方法（如 KAMA）估计可见帧的人体姿态序列 $\widetilde{Q}$，同时基于 LiDAR 点云使用泊松表面重建获取场景地形网格。为适配后续物理模拟，将重建网格转换为高度图并进行修复扩展，以覆盖行人运动范围（Figure 3）。

### 阶段二：物理感知运动跟踪

这是框架的核心。由三个关键组件协同工作（Figure 4）：

- **运动生成模型 $\pi_M$**：基于条件变分自编码器（cVAE）的生成式转移模型，在室内平坦地面数据上预训练，根据前一姿态和潜变量生成下一帧运动状态。
- **物理感知模仿器 $\pi_D$**：在物理模拟器中执行 PD 控制器，将生成的目标姿态转化为符合物理约束的关节角度。
- **高层控制器 $\pi_C$**：基于强化学习训练的策略网络，输入当前生成状态 $\widehat{S}_t^g$、模拟状态 $\widehat{S}_t$、未来轨迹 $x$、地形 $G$ 及目标姿态 $\widetilde{Q}_{t_2}$，输出潜变量 $z_{t+1}^g$ 和残差 $z_{t+1}^r$，以补偿 $\pi_M$ 在户外不平坦地形上的不适配：

$$z_{t+1}^g, z_{t+1}^r = \pi_C(\widehat{S}_t^g, \widehat{S}_t, x, G, \widetilde{Q}_{t_2})$$

随后生成运动状态并计算关节目标：

$$\widehat{S}_{t+1}^g = \pi_M(\widehat{S}_t^g, z_{t+1}^g) + z_{t+1}^r, \quad \widehat{a}_{t+1} = \pi_D(\widehat{S}_t, \widehat{S}_{t+1}^g)$$

为加速训练，高层控制器先在合成多样地形上预训练，再在真实数据上微调（Figure 6 显示预训练显著加快收敛并提升最终奖励）。训练奖励由轨迹跟随奖励 $r_p$ 和填补奖励 $r_i$ 加权求和：$r = w_p \cdot r_p + w_i \cdot r_i$。

### 阶段三：后优化

在物理模拟器中，基于 2D 关键点投影误差对全局运动进行微调，投影奖励定义为：

$$r_{proj} = \exp(-\alpha_p \sum(\|\Pi(\overline{j}_t) - \widetilde{j}_t^{2D}\| \times \widetilde{c}_t))$$

其中 $\widetilde{c}_t$ 为关键点置信度，用于加权投影误差。最终奖励结合投影奖励与运动模仿奖励：$r = r_{proj} \cdot w_p + r_{im} \cdot w_{im}$。此阶段显著提升了遮挡帧的 PA-MPJPE 和 2D 关键点对齐精度（Table 3, Figure 7）。

### 关键改进槽位

与基线 **GLAMR** 相比，本框架在四个关键维度做了替换：

| 改进维度 | GLAMR | 本文方法 |
|---------|-------|---------|
| 遮挡轨迹填补 | Transformer cVAE 一次性填补多帧 | 分层控制器逐步预测潜变量+残差，物理模拟器执行 |
| 物理约束 | 仅运动学约束 | 物理模拟器中强制执行，PD 控制器+地形适配 |
| 地形处理 | 忽略真实地形，假设平坦地面 | LiDAR 点云重建地形，高度图修复，模拟中施加接触 |
| 训练数据适应性 | 室内平坦地面训练 | 合成多样地形预训练+真实数据微调 |

### 局限性

当前框架主要处理静态地形，对动态障碍物（如车辆）交互未深入探讨；身体形状参数由离线 MoCap 估计，未在物理感知框架内优化；高度图到网格转换误差及 SMPL 模型精度限制导致脚部穿透等微小伪影未完全消除；高层控制器训练需大量计算资源（单 V100 GPU >12 小时），且对每个视频需微调。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_openaccess_thecvf_com_content_ICCV2023_papers_Wang_Learning_Human/figures/001_Figure_1.jpg]]
*Figure 1: We compare our method against GLAMR [67], the state-of-the-art method for global human motion mesh recovery. The output of GLAMR (left) suffers from various physical implausibilities, such as floating, sliding, or terrain penetration. Our method (right) yields a clear improvement*

## 核心模块与公式推导

### 人体运动表示

本框架将人体动态统一表示为一组运动序列。对于单个行人，其运动序列 $Q$ 定义为：

$$Q = (T, R, \Theta)$$

其中 $T$ 表示根关节的全局平移，$R$ 表示根关节的全局旋转，$\Theta$ 表示身体各关节的姿态参数。这一表示覆盖了从可见帧到遮挡帧的完整人体动态，是世界坐标系下的全局描述。

### 三阶段流水线架构

框架采用分阶段处理策略，核心模块分布在三个阶段中（Figure 2）：

**阶段一：运动与地形准备。** 利用现成的运动捕捉方法（如 KAMA）估计可见帧的人体姿态，同时通过泊松表面重建从 LiDAR 点云中恢复地形网格，并将其转换为高度图进行修复与扩展，为后续物理模拟提供准确的地面接触约束（Figure 3）。

**阶段二：物理感知运动跟踪。** 这是方法的核心创新模块，由三个子组件协同工作——高层次控制器 $\pi_C$、运动生成模型 $\pi_M$ 和物理感知模仿器 $\pi_D$（Figure 4）。该阶段负责填补遮挡帧的运动序列，并强制运动与重建地形之间的物理合理性。

**阶段三：后优化。** 在物理模拟器中，基于 2D 关键点投影误差对完整运动序列进行微调，进一步提升与视频证据的一致性。

### 物理感知运动跟踪核心公式

运动跟踪框架的核心在于逐步生成遮挡帧的运动状态。在时间步 $t$，高层次控制器 $\pi_C$ 根据当前生成状态 $\widehat{S}_t^g$、模拟状态 $\widehat{S}_t$、未来轨迹 $x$、地形 $G$ 以及目标姿态 $\widetilde{Q}_{t_2}$，预测下一帧的潜变量 $z_{t+1}^g$ 和残差 $z_{t+1}^r$：

$$z_{t+1}^g, z_{t+1}^r = \pi_C(\widehat{S}_t^g, \widehat{S}_t, x, G, \widetilde{Q}_{t_2})$$

随后，运动生成模型 $\pi_M$ 基于上一帧生成状态和潜变量生成初步运动，并与残差相加得到目标生成状态；物理感知模仿器 $\pi_D$ 则将该目标状态转换为可执行的关节角度目标 $\widehat{a}_{t+1}$：

$$\widehat{S}_{t+1}^g = \pi_M(\widehat{S}_t^g, z_{t+1}^g) + z_{t+1}^r, \quad \widehat{a}_{t+1} = \pi_D(\widehat{S}_t, \widehat{S}_{t+1}^g)$$

**关键设计动机：** 运动生成模型 $\pi_M$ 仅在室内平坦地面数据上训练，难以直接适应户外不平坦地形。高层次控制器通过预测残差 $z_{t+1}^r$ 来修正生成运动的偏差，而 $\pi_D$ 作为 PD 控制器在物理模拟器中强制执行地面接触约束，从而消除漂浮、滑动和地面穿透等伪影。

### 训练奖励设计

高层次控制器的训练采用标准强化学习算法，$\pi_M$ 预训练后冻结。总奖励由轨迹跟随奖励 $r_p$ 和填补奖励 $r_i$ 加权求和：

$$r = w_p \cdot r_p + w_i \cdot r_i$$

在后优化阶段，引入基于 2D 关键点投影的奖励项，以置信度 $\widetilde{c}_t$ 加权投影误差：

$$r_{proj} = \exp(-\alpha_p \sum(\|\Pi(\overline{j}_t) - \widetilde{j}_t^{2D}\| \times \widetilde{c}_t))$$

最终优化目标为投影奖励与运动模仿奖励的加权组合：$r = r_{proj} \cdot w_p + r_{im} \cdot w_{im}$。

### 地形适配策略

为将室内训练的运动先验迁移到户外场景，框架在合成多样化地形上预训练高层次控制器，再在 Waymo Open Dataset 的真实数据上微调。这一策略显著加快了收敛速度并提升了最终奖励（Figure 6），验证了合成数据预训练对真实场景泛化的有效性。

## 实验与分析

### 主实验结果

在 Waymo Open Dataset 上，本文方法在运动生成质量与物理合理性两个维度均显著超越现有基线。Table 1 汇总了与多种方法的定量对比，其中 **GLAMR***（Yuan et al., CVPR 2022）表示在 GLAMR 输出后接入了与本文相同的物理感知模仿器，以保证比较的公平性。

![[assets/figures/papers/paper_list_l37_https_openaccess_thecvf_com_content_ICCV2023_papers_Wang_Learning_Human/figures/006_Table_1.jpg]]
*Table 1: Baseline Comparison. We compare against several different baselines on the following metrics. GLAMR∗ means use the same physics-aware imitator as our framework after GLAMR. Our method achieves the significantly better result on FID, PAM-PJPE on frames with occlusion (Occ), and physics-based metrics (GP, FS, FL)*

核心指标表现如下：
- **FID（全部帧）**：本文方法达到 **1.96**，远优于包括 GLAMR 在内的所有基线方法，表明生成运动的分布与真实运动高度一致。
- **PA-MPJPE（遮挡帧）**：在仅考虑被遮挡帧的姿态估计误差时，本文方法同样取得显著优势，说明分层控制器对缺失帧的填补不仅物理合理，而且与真实姿态接近。
- **物理合理性指标**：地面穿透（GP）降至 **12.62**，脚滑动（FS）和漂浮度（FL）也大幅降低。相比之下，原始 GLAMR 存在严重的漂浮、滑动和地面穿透伪影（Figure 1 和 Figure 5 提供了直观的定性对比）。

这些结果表明，引入物理感知的分层运动控制器和地形适配机制，是解决遮挡下人体运动恢复中物理伪影问题的关键。

### 消融实验

#### 物理感知模仿器的作用

Table 2 考察了物理感知模仿器 $π_D$ 的独立贡献。实验设置中，高层次控制器在训练时已将生成运动适配到地形，但消融结果显示：即使在此前提下，物理感知模仿器仍能进一步改善 GP、FS、FL 三项物理指标（标注 Our* 的结果不含后优化）。这说明 $π_D$ 提供的物理模拟强制执行并非冗余——它能在控制器预测的基础上，修正关节级别的微小不合理性，从而提升整体运动质量。

![[assets/figures/papers/paper_list_l37_https_openaccess_thecvf_com_content_ICCV2023_papers_Wang_Learning_Human/figures/007_Table_2.jpg]]
*Table 2: Ablation studies on the physics-aware imitator. Although we have adapted the generated motion to the ground during training, the physics-aware motion imitator still can improve the motion quality on these physics attributes. Our∗ means the result without post-optimization*

#### 后优化阶段的作用

Table 3 对比了有无后优化阶段的填补结果。数据显示，后优化显著提升了 **2D 关键点投影误差（2D-LE）** 和遮挡帧的 **PA-MPJPE**，同时进一步增强了物理属性。Figure 7 的定性结果也佐证了这一点：经过后优化，前两阶段生成的运动会更好地与视频中的 2D 关键点证据对齐，减少视觉上的偏移和不一致。

![[assets/figures/papers/paper_list_l37_https_openaccess_thecvf_com_content_ICCV2023_papers_Wang_Learning_Human/figures/005_Table_3.jpg]]
*Table 3: Ablation studies on post optimization. We compare the infilling results with and without the post-optimization after physics-aware motion tracking*

后优化的有效性源于其奖励设计——投影奖励 $r_{proj} = \exp(-\alpha_p \sum(\|\Pi(\overline{j}_t) - \widetilde{j}_t^{2D}\| \times \widetilde{c}_t))$ 显式地将 2D 观测置信度纳入优化，使物理模拟器在保持物理约束的前提下，向视觉证据靠拢。

#### 预训练策略的效果

Figure 6 展示了高层次控制器在合成数据上预训练对收敛速度的影响。在 Waymo Open Dataset 上微调时，经过合成地形预训练的控制器收敛速度显著加快，且最终奖励更高。这与直觉一致：合成数据提供了多样化的地形条件，使控制器在接触真实数据前已习得基本的地形适应能力，从而减少了在真实场景中的探索成本。值得注意的是，从零开始在单张 V100 GPU 上训练控制器需超过 12 小时（1000 次迭代），预训练策略有效缓解了这一计算瓶颈。

![[assets/figures/papers/paper_list_l37_https_openaccess_thecvf_com_content_ICCV2023_papers_Wang_Learning_Human/figures/008_Figure_6.jpg]]
*Figure 6: Convergence Results. We compare the time cost of training the high-level controller on the Waymo Open Dataset with and without the pre-training on synthetic data. We show that the high-level controller converges much faster and achieves a better reward with the pre-training*

### 失败模式与局限性

尽管本文方法在整体指标上表现优异，但分析中仍暴露出若干局限：

1. **微小穿透伪影残留**：由于高度图到网格转换的误差以及 SMPL 人体模型的精度限制，脚部与地面的微小穿透并未完全消除。这提示物理模拟的精度受限于上游地形重建和人体模型的保真度。

2. **动态障碍物未建模**：当前框架假设地形为静态，未考虑车辆等动态移动障碍物对人体的交互影响。在真实驾驶场景中，行人可能与车辆近距离交互，忽略这一点可能导致运动预测的偏差。

3. **身体形状未优化**：身体形状参数由离线运动捕捉方法（如 KAMA）估计，未在物理感知框架内联合优化，可能导致与真实人体模型的偏差，进而影响物理模拟的准确性。

4. **计算开销**：高层次控制器需对每个视频序列进行微调，且训练耗时较长，限制了方法的实时应用潜力。

### 重要图表结论

- **Figure 1 和 Figure 5**：定性对比直观展示了本文方法相较 GLAMR 的物理合理性提升——漂浮、滑动和地面穿透等伪影得到显著抑制。
- **Table 1**：定量证据的核心载体，FID 1.96 和 GP 12.62 构成方法优势的主要支撑。
- **Table 2 和 Table 3**：分别验证了物理感知模仿器和后优化阶段的独立贡献，强化了“物理模拟 + 视觉对齐”协同设计的合理性。
- **Figure 6**：为预训练策略的必要性提供了实验依据，同时揭示了训练效率的瓶颈。
- **Figure 7**：后优化的定性效果展示，说明优化后运动与视频证据的对齐程度明显改善。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_openaccess_thecvf_com_content_ICCV2023_papers_Wang_Learning_Human/figures/002_Figure_2.jpg]]
*Figure 2: System Overview. Our approach processes each pedestrian mesh sequence in a stage-wise fashion. We first estimate motions for visible frames $\widetilde { Q }$ using an off-the-shelf motion capture method. We also reconstruct the ground terrain G in preparation for the physicsbased stages (Details in Section 3.1). The physics-aware motion tracking (Section 3.2) infills the motion Q for the occluded frames, as well as adapts the previously reconstructed motion to the reconstructed ground. In the last stage (Section 3.3), we optimize the entire motion $\widehat { Q }$ to closely match the evidence from a 2D keypoint-based system to produce the final motion Q

## 方法谱系与知识库定位

### 与基线方法的关系

本工作最直接的对比对象是 **GLAMR**（Yuan et al., CVPR 2022），该方法代表了当时遮挡感知全局人体运动恢复的最高水平。GLAMR 的核心策略是利用基于 Transformer 的条件变分自编码器（cVAE）一次性填补多个缺失帧的运动，但其在物理合理性上存在系统性缺陷：它仅考虑关节角度等运动学约束，忽略真实地形接触，且其运动先验在室内平坦地面数据上训练，难以适配户外复杂地形。这导致 GLAMR 的输出普遍存在漂浮、滑动、地面穿透等伪影（Figure 1）。

本文的方法在四个关键维度上对 GLAMR 的范式进行了根本性改造：

1.  **遮挡轨迹填补方式**：从 cVAE 的一次性全局填补，转变为分层控制器逐步预测潜变量并结合残差，通过物理感知模仿器逐帧执行。这一改变使运动生成过程具备了因果时序一致性，而非对缺失段的整体猜测。
2.  **物理约束引入**：从纯运动学约束升级为在物理模拟器中强制执行物理合理性，引入 PD 控制器和地形适配机制，从根本上消除了脚滑动和地面穿透的物理矛盾。
3.  **地形处理**：从忽略真实地形（假设平坦地面）转变为利用 LiDAR 点云重建地形并修复高度图，在模拟中施加准确的地形接触约束。这是实现户外场景物理合理运动的关键前提。
4.  **训练数据适应性**：从仅在室内数据上训练，转变为在合成多样地形上预训练高层控制器，再在真实数据上微调。这一策略显著加速了收敛并提升了最终奖励（Figure 6）。

为了公平对比，论文还引入了 **GLAMR\*** 变体——在 GLAMR 的输出上额外施加与本文相同的物理感知模仿器。即便如此，本文方法在 FID、遮挡帧 PA-MPJPE 以及物理指标（GP、FS、FL）上仍全面领先（Table 1），证明改进并非单纯来自物理后处理，而是源于分层控制架构与地形感知的协同设计。

### 方法适用边界

本框架的设计假设和实验设置定义了其当前的适用边界：

-   **场景类型**：主要面向自动驾驶场景中车载单目视频的行人动态恢复，摄像机处于快速移动状态，行人存在频繁且长时的遮挡。
-   **地形假设**：当前方法主要处理静态地形。论文明确指出，对动态移动障碍物（如车辆）的交互未深入探讨，这意味着在行人与移动车辆发生复杂交互的场景中，方法的物理合理性可能下降。
-   **人体模型**：身体形状参数由离线运动捕捉方法（如 KAMA）估计，未在物理感知框架内联合优化。这可能导致恢复的人体形状与真实个体存在偏差，进而影响接触约束的精度。
-   **输入依赖**：框架依赖现成的运动捕捉和场景重建模块作为前置输入，其性能上限受这些模块精度的制约。

### 局限与开放问题

论文坦诚了若干现存局限，这些局限同时指向了未来的研究方向：

-   **微小物理伪影残留**：由于高度图到网格转换的误差及 SMPL 模型本身的精度限制，脚部穿透等微小伪影仍未完全消除。这表明单纯依赖几何重建和刚体物理模拟可能不足以解决所有接触层面的精细问题。
-   **计算资源需求**：高层次控制器的训练需要大量计算资源（单张 V100 GPU 超过 12 小时），且对每个视频序列需要微调。这限制了方法在实时或大规模部署场景中的可行性。
-   **动态交互空白**：如何将框架扩展到处理动态障碍物或多人交互场景，是一个明确但未解决的开放问题。这需要超越静态地形约束，引入对移动物体的感知与响应机制。
-   **端到端可微分性**：当前框架为模块化级联设计，身体形状优化与物理模拟分离。能否将身体形状优化集成到物理感知框架中，实现端到端的可微分动态，是提升整体一致性的潜在路径。
-   **泛化能力验证**：论文仅在 Waymo Open Dataset 上进行了验证。在更多样化的真实驾驶场景（如不同城市、天气条件、交通密度）中，该框架的泛化能力尚待检验。
-   **感知一致性**：定性指标（如 FID）的改进是否与人类感知的物理真实性完全一致，仍是一个值得追问的问题。物理指标的降低不一定线性对应感知质量的提升，需要用户研究等进一步验证。

## 原文 PDF

![[paperPDFs/ICCV_2023/Learning_Human_Dynamics_in_Autonomous_Driving_Scenarios.pdf]]
