---
title: "LATENT: Learning Athletic Humanoid Tennis Skills from Imperfect Human Motion Data"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/LATENT_Learning_Athletic_Humanoid_Tennis_Skills_from_Imperfect_Human_Motion_Data.pdf
aliases:
- LATENT
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 可校正的潜在动作空间（correctable latent action space），结合基于马氏距离的潜在动作障碍（LAB）和手腕直接校正，使得高层策略能够在约束下组合原始技能并校正手腕。
primary_logic: 尽管收集的人体运动数据仅包含不精确且不完整的网球原始技能片段，但这些准真实数据仍能提供有价值的动作先验；通过设计可校正的潜在空间和适当的探索约束，可以学习出兼具任务性能和自然运动风格的网球技能。
claims:
- LATENT在正手击球任务中成功率达到96.52%，反手82.10%，显著优于所有基线方法（PPO, MotionVAE, AMP, ASE, PULSE）。
- 消融实验表明，移除手腕校正使正手成功率降至82.36%，反手降至68.94%；移除潜在动作障碍（LAB）使正手成功率降至93.12%，反手降至76.96%。
- 在真实世界部署中，LATENT在正手任务上实现90.90%的成功率，并能稳定维持与人类的多回合对打。
- 无动力学随机化时真实世界成功率仅16.67%，无观测噪声时为50.00%，证明了sim-to-real策略的有效性。
---

# LATENT: Learning Athletic Humanoid Tennis Skills from Imperfect Human Motion Data

> [!tip] 核心洞察
> 尽管收集的人体运动数据仅包含不精确且不完整的网球原始技能片段，但这些准真实数据仍能提供有价值的动作先验；通过设计可校正的潜在空间和适当的探索约束，可以学习出兼具任务性能和自然运动风格的网球技能。

| 字段 | 内容 |
|------|------|
| 中文题名 | LATENT：从不完美人体运动数据中学习竞技人形机器人网球技能 |
| 英文题名 | LATENT: Learning Athletic Humanoid Tennis Skills from Imperfect Human Motion Data |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.12686) · [Code](https://github.com/GalaxyGeneralRobotics/LATENT) · [Project](https://zzk273.github.io/LATENT/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LATENT |
| Dataset | Real-world tennis rally |

> [!tip] 效果简介
> - Real-world tennis rally (forehand) 上，Success Rate (%) 90.90 vs ours without dynamics randomization (DR) (+74.23)；Success Rate (%) 90.90 vs ours without observation noise (ON) (+40.90)。

## 概述

**核心问题**：如何从不完美的人体运动数据中学习人形机器人的竞技网球技能？真实人体运动捕捉数据通常包含不精确的手腕动作（持拍手）和不完整的技能组合，直接使用此类数据训练策略会导致击球精度低、动作不自然。LATENT 的核心瓶颈在于：**不完美的人体运动数据阻碍了人形机器人直接学习高质量网球技能，需要有效的修正与组合机制**。

**核心结论**：LATENT 通过设计**可校正的潜在动作空间**（correctable latent action space），结合基于马氏距离的**潜在动作障碍**（Latent Action Barrier, LAB）和**手腕直接校正**，使高层策略能够在约束下组合原始技能并校正手腕动作。尽管收集的人体运动数据仅包含不精确且不完整的网球原始技能片段，但这些准真实数据仍能提供有价值的动作先验；通过设计可校正的潜在空间和适当的探索约束，可以学习出兼具任务性能和自然运动风格的网球技能。

**主要结果**：
- 在仿真正手击球任务中成功率达 **96.52%**，反手 **82.10%**，显著优于所有基线方法（vanilla PPO、MotionVAE、AMP、ASE、PULSE）（Table 3）。
- 在真实世界 Unitree G1 机器人部署中，正手任务实现 **90.90%** 成功率，并能稳定维持与人类的多回合对打（Table 5, Figure 1）。
- 消融实验表明，移除手腕校正使正手成功率降至 82.36%，反手降至 68.94%；移除 LAB 使正手降至 93.12%，反手降至 76.96%，验证了两个关键设计的必要性（Table 4）。

**方法定位**：LATENT 基于分层人形机器人控制框架，区别于端到端强化学习（vanilla PPO）、解耦运动生成与跟踪（MotionVAE）、对抗运动先验（AMP）、对抗技能嵌入（ASE）以及无校正机制的潜在动作空间方法（PULSE）。其核心创新在于将**在线蒸馏的条件变分瓶颈**、**状态条件可学习先验**、**手腕直接校正**与**自适应马氏距离约束**统一到同一框架中，实现了从不完美数据到竞技级技能的有效迁移。

## 背景与动机

### 问题背景：人形机器人运动技能的获取瓶颈

使通用人形机器人在动态、高精度的体育任务中达到人类水平的表现，是具身智能领域的长期目标。网球运动对敏捷性、手眼协调和全身运动规划提出了极高要求，成为检验人形机器人运动智能的理想场景。传统的机器人技能获取方法通常依赖于精心设计的运动规划或强化学习，但面临两难困境：纯强化学习（如 vanilla PPO）在稀疏奖励的高维动作空间中难以收敛，而基于运动捕捉数据的模仿学习方法则受限于数据质量。

### 现有方法的缺口：不完美人体运动数据的挑战

近年来，基于运动先验的强化学习方法——如对抗运动先验 **AMP**（Peng et al., TOG 2021）、对抗技能嵌入 **ASE**（Peng et al., TOG 2022）以及潜在动作空间方法 **PULSE**（Luo et al., arXiv 2023）——在利用人体运动数据引导人形机器人学习方面取得了显著进展。然而，这些方法普遍假设运动数据是高质量且完整的。实际采集的人体网球运动数据面临两个根本性缺陷：

1. **手腕动作不精确**：由于运动捕捉系统的精度限制和人体与机器人末端执行器的结构差异，采集到的手腕运动轨迹难以直接转化为精确的球拍控制，导致击球点偏差。
2. **技能组合不完整**：收集的数据通常仅包含孤立的原始技能片段（如正手挥拍、反手挥拍），缺乏将这些片段组合成连续对打策略的完整示范。

这些“不完美”使得现有方法要么生成的运动风格与任务目标冲突，要么无法在保持自然运动风格的同时完成精确的任务操作。核心瓶颈在于：**如何从不精确且不完整的人体运动数据中，提取有价值的运动先验，同时建立有效的修正与组合机制，以学习高质量的网球技能。**

### 本文动机：可校正潜在空间的思路

尽管采集的人体运动数据存在上述缺陷，但这些准真实数据仍蕴含着丰富的运动风格信息——包括自然的重心转移、脚步移动和躯干协调模式。本文的核心洞察是：**通过设计一个可校正的潜在动作空间，使高层策略能够在约束范围内组合原始技能并直接校正关键末端执行器（手腕），可以在任务性能和运动自然度之间取得平衡。**

具体而言，LATENT 系统围绕三个关键机制展开：
- **可学习的条件先验**：替代传统 VAE 的固定单峰高斯先验，使潜在空间能够根据机器人状态自适应地调整动作分布。
- **手腕直接校正**：允许高层策略在潜在动作之外，直接输出右腕关节的控制命令，弥补运动捕捉数据中手腕精度的不足。
- **基于马氏距离的潜在动作障碍（LAB）**：在探索过程中自适应约束残差动作范围，防止策略生成超出运动先验分布的危险动作，从而在保持运动质量的同时完成精确的任务操作。

这一思路使得 LATENT 能够从仅包含不精确原始技能片段的业余球员数据出发，学习出兼具任务成功率（仿真正手 96.52%）和自然运动风格的网球技能，并在 Unitree G1 机器人上实现稳定的多回合真实世界对打。

## 核心创新

LATENT 的核心创新在于构建了一个**可校正的潜在动作空间**（correctable latent action space），使高层策略能够在约束下组合不完美人体数据中的原始技能，并直接校正关键末端执行器。其关键设计围绕以下四个 changed slots 展开。

### 1. 手腕动作直接校正

现有分层潜在动作方法（如 **PULSE**，Luo et al., arXiv 2023）完全依赖潜在空间生成所有关节动作，无法针对不精确的末端执行器（如持拍手腕）进行精确修正。LATENT 将高层策略的输出扩展为 $\boldsymbol{a}_t^{\mathrm{planner}} = [\boldsymbol{a}_t^{\mathrm{latent}}, \boldsymbol{a}_t^{\mathrm{correct}}]$，同时输出潜在动作和右手腕的直接控制命令（Section 3.3.2）。这一设计使得策略在利用潜在空间生成自然身体运动的同时，能够对击球精度至关重要的手腕进行独立校正。消融实验（Table 4）表明，移除手腕校正后，正手成功率从 96.52% 骤降至 82.36%，反手从 82.10% 降至 68.94%，验证了该机制的决定性作用。

### 2. 状态条件的可学习先验

传统 VAE 使用固定单峰高斯先验，无法捕捉不同状态下动作分布的差异性。LATENT 引入可学习的状态条件先验 $\mathcal{P}(z_t^p|s_t) = \mathcal{N}(z_t^p; \mu^p(s_t), \sigma^p(s_t))$（Section 3.2.2），使潜在空间的先验分布随机器人状态自适应变化。这不仅为潜在动作采样提供了更合理的基准，也为后续的潜在动作障碍（LAB）提供了状态依赖的标准差信息，使探索范围能够根据状态不确定性自适应调整。

### 3. 基于马氏距离的潜在动作障碍（LAB）

在潜在空间中无约束采样容易导致策略生成超出训练分布的动作，造成运动抖动甚至失败。LATENT 设计了基于马氏距离的潜在动作障碍（Latent Action Barrier, LAB），将最终 PD 目标动作约束为：

$$\boldsymbol{a}_t^{\mathrm{full}} = [\mathcal{D}(\boldsymbol{s}_t, \boldsymbol{\mu}_t^p + \lambda \boldsymbol{\sigma}_t^p \cdot \mathrm{tanh}(\boldsymbol{a}_t^{\mathrm{latent}})), \boldsymbol{a}_t^{\mathrm{correct}}]$$

与欧氏距离不同，马氏距离利用状态条件标准差 $\boldsymbol{\sigma}_t^p$ 对各维度进行自适应缩放（Section 3.3.3），使探索范围在动作方差大的维度上更宽松，在方差小的维度上更严格。消融实验（Table 4）显示，移除 LAB 后正手成功率降至 93.12%，反手降至 76.96%，且运动出现明显抖动，证明 LAB 对动作质量和任务成功率的双重贡献。

### 4. 在线蒸馏与手腕扰动鲁棒的潜在空间

不同于 PULSE 的离线 VAE 蒸馏，LATENT 采用在线 DAgger 蒸馏结合条件变分瓶颈构建潜在空间（Section 3.2.2）。在运动跟踪器预训练阶段，刻意移除右手腕的控制信号并施加随机扰动（Section 3.2.1），使得后续蒸馏出的潜在空间对腕部扰动具有鲁棒性。这一设计确保了高层策略在输出手腕校正命令时，潜在空间生成的身体动作不会因手腕变化而失真，实现了校正与自然的解耦。

## 整体框架

LATENT 的完整流程遵循“数据收集—先验构建—策略训练—迁移部署”四阶段范式，核心目标是**从不完美的人体运动数据中提取可用的动作先验，并通过可校正的潜在动作空间与探索约束，使高层策略能够在网球任务中组合原始技能并精确控制末端执行器**。

### 数据收集与运动跟踪器预训练

系统首先收集**不完美的人体网球运动数据**，这些数据仅包含原始技能片段（如正手、反手挥拍），缺乏精确的手腕动作和完整的技能组合（Section 3.1）。随后，利用 **Any2Track** 框架（Luo et al., arXiv 2023）预训练一个运动跟踪器，以模仿收集到的运动片段。关键设计在于：训练过程中**移除持拍右手腕的控制信号，并对其施加随机扰动**，使得跟踪器学会对腕部不确定性保持鲁棒，为后续潜在空间的构建奠定基础（Section 3.2.1）。

### 可校正潜在动作空间的构建

在跟踪器预训练完成后，LATENT 通过**在线 DAgger 蒸馏**与**条件变分瓶颈**构建潜在动作空间（Section 3.2.2）。与标准 VAE 使用固定单峰高斯先验不同，LATENT 采用**可学习的状态条件先验** $\mathcal{P}(z_t^p|s_t) = \mathcal{N}(z_t^p; \mu^p(s_t), \sigma^p(s_t))$，以捕捉依赖于状态的动作分布。训练目标为动作重构损失与 KL 散度损失的加权和：

$$\mathcal{L} = \lambda_1 \mathcal{L}_{\mathrm{action}} + \lambda_2 \mathcal{L}_{\mathrm{KL}}$$

其中动作重构损失基于在线聚合数据缓冲区 $\mathcal{D}_{\mathrm{agg}}$ 计算教师动作与学生动作之间的均方误差：

$$\mathcal{L}_{\mathrm{action}} = \mathbb{E}_{(s_t, \hat{a}_t^{\mathrm{body}}) \sim \mathcal{D}_{\mathrm{agg}}} \left[ \lVert \hat{a}_t^{\mathrm{body}} - a_t^{\mathrm{body}} \rVert^2 \right]$$

KL 散度损失鼓励后验编码器分布接近可学习先验：

$$\mathcal{L}_{\mathrm{KL}} = D_{\mathrm{KL}} \big( \mathcal{E}(z_t^q|s_t, \tilde{s}_{t+1}) \,||\, \mathcal{P}(z_t^p|s_t) \big)$$

由于跟踪器已在缺失腕部控制的情况下训练，由此构建的潜在空间对腕部扰动具有天然鲁棒性，为后续**手腕直接校正**提供了操作空间。

### 高层策略训练与动作校正

高层策略的训练是整个系统的核心决策环节。与仅从潜在空间采样的方法（如 PULSE）不同，LATENT 的高层策略**同时输出潜在动作和直接手腕控制命令**：

$$a_t^{\mathrm{planner}} = [a_t^{\mathrm{latent}}, a_t^{\mathrm{correct}}]$$

这一设计使得策略既能利用潜在空间中的自然运动先验，又能对持拍手腕进行精确校正，弥补原始数据中腕部动作不精确的缺陷。

### 潜在动作障碍（LAB）

为确保探索过程中的动作质量，LATENT 引入**基于马氏距离的潜在动作障碍（Latent Action Barrier, LAB）**，自适应约束残差动作范围（Section 3.3.3）。与使用欧氏距离的固定边界不同，LAB 根据状态依赖的标准差自适应缩放约束范围：

$$\boldsymbol{a}_t^{\mathrm{full}} = [ \mathcal{D}(\boldsymbol{s}_t, \boldsymbol{\mu}_t^p + \lambda \boldsymbol{\sigma}_t^p \cdot \tanh(\boldsymbol{a}_t^{\mathrm{latent}})), \boldsymbol{a}_t^{\mathrm{correct}} ]$$

其中 $\mathcal{D}$ 表示基于马氏距离的投影操作，$\lambda$ 控制允许探索的倍数。这一机制在保留动作自然度的同时，防止策略产生超出运动先验支持范围的异常动作。

### Sim-to-Real 迁移

策略从仿真到真实世界的迁移依赖于两方面的域随机化（Table 2）：**机器人动力学随机化**（如关节质量、阻尼、摩擦力）和**网球物理随机化**（如空气阻力系数、反弹系数）。空气阻力模型为 $\pmb{f}_{air} = -k \cdot m \cdot v \cdot ||\pmb{v}||$，与球速和质量成正比。此外，观测噪声的注入进一步提升了策略对真实世界感知误差的鲁棒性。

### 模块间数据流

整个 pipeline 的数据流可概括为：**不完美运动片段 → 运动跟踪器（鲁棒模仿）→ 在线蒸馏（潜在空间构建）→ 高层策略（潜在动作采样 + 手腕校正）→ LAB 约束（动作投影）→ PD 目标（底层执行）→ 域随机化（sim-to-real 桥接）**。这一设计使得 LATENT 能够在仅依赖准真实运动先验的条件下，学习出兼具任务性能和自然运动风格的网球技能。

### 补充图表

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/003_Figure_2.jpg]]
*Figure 2: Overview of LATENT. (a) We pre-train a motion tracker on collected imperfect human motion data. (b) We construct a correctable latent action space via online distillation. (c) We train a high-level policy to correct and compose latent actions for tennis task. (d) We transfer the policy to the real world via dynamics randomization and observation noise*

## 核心模块与公式推导

LATENT 的核心架构围绕一个 **可校正的潜在动作空间 (correctable latent action space)** 展开，通过三个关键模块将不完美的人体运动数据转化为可组合、可校正的网球技能。

### 1. 潜在动作空间构建

该模块的目标是从不完美的运动数据中蒸馏出一个紧凑、可采样的动作表示空间，同时使其对手腕扰动具有鲁棒性。

**在线蒸馏与条件瓶颈**：不同于离线 VAE 蒸馏方案（如 **PULSE** (Luo et al., arXiv 2023)），LATENT 采用在线 DAgger 蒸馏框架。在运动跟踪器预训练阶段，系统持续聚合教师动作 $`\hat{a}_t^{\text{body}}`$ 与学生动作 $`a_t^{\text{body}}`$ 的数据对。潜在空间通过一个变分编码器-解码器结构学习，其训练损失为动作重构损失与 KL 散度损失的加权和：

```math
\mathcal{L} = \lambda_1 \mathcal{L}_{\text{action}} + \lambda_2 \mathcal{L}_{\text{KL}}
```

其中，动作重构损失 $`\mathcal{L}_{\text{action}}`$ 定义为聚合缓冲区 $`\mathcal{D}_{\text{agg}}`$ 上教师动作与学生动作之间的均方误差：

```math
\mathcal{L}_{\text{action}} = \mathbb{E}_{(s_t, \hat{a}_t^{\text{body}}) \sim \mathcal{D}_{\text{agg}}} \left[ \lVert \hat{a}_t^{\text{body}} - a_t^{\text{body}} \rVert^2 \right]
```

KL 散度损失 $`\mathcal{L}_{\text{KL}}`$ 用于规范潜在空间的结构，迫使后验编码器分布 $`\mathcal{E}(z_t^q|s_t, \tilde{s}_{t+1})`$ 逼近一个可学习的条件先验 $`\mathcal{P}(z_t^p|s_t)`$：

```math
\mathcal{L}_{\text{KL}} = D_{\text{KL}} \big( \mathcal{E}(z_t^q|s_t, \tilde{s}_{t+1}) \ || \ \mathcal{P}(z_t^p|s_t) \big)
```

**可学习条件先验**：与标准 VAE 使用的固定单峰高斯先验不同，LATENT 采用状态条件先验 $`\mathcal{P}(z_t^p|s_t) = \mathcal{N}(z_t^p; \mu^p(s_t), \sigma^p(s_t))`$。该设计使先验能够根据当前状态 $`s_t`$ 自适应地预测合理的动作分布，为后续高层策略的探索提供了更精准的约束基础。

**手腕扰动鲁棒性**：在运动跟踪器训练期间，系统刻意移除持拍右手腕的控制信号，并对其关节施加随机扰动。这一设计迫使潜在空间学会在手腕信息缺失或不可靠的情况下仍能生成合理的全身动作，从而为高层策略的直接手腕校正预留了空间。

### 2. 手腕动作校正

该模块解决了不完美人体数据中手腕动作不精确的核心瓶颈。高层策略 $`\pi_{\text{high}}`$ 的输出被设计为一个拼接向量：

```math
a_t^{\text{planner}} = [a_t^{\text{latent}}, a_t^{\text{correct}}]
```

其中 $`a_t^{\text{latent}}`$ 是在潜在空间中的采样动作，$`a_t^{\text{correct}}`$ 是直接作用于右手腕关节的 PD 目标校正命令。这种设计使高层策略能够同时进行全身动作的隐式选择（通过潜在动作）和手腕动作的显式精细控制（通过直接校正），从而在不破坏整体运动风格的前提下精确调整击球姿态。

### 3. 潜在动作障碍（LAB）

该模块是约束高层策略探索行为的关键机制。若不加约束，策略可能在潜在空间中采样到远离训练分布的动作，导致运动失真或控制不稳定。

LAB 基于 **马氏距离 (Mahalanobis distance)** 而非欧氏距离来定义探索边界。其核心动机在于：状态条件先验的标准差 $`\sigma_t^p`$ 反映了该状态下动作的合理变化范围——在动作多样性高的状态下应允许更大的探索，而在动作精确性要求高的状态下应施加更紧的约束。

最终输出的完整 PD 控制目标 $`a_t^{\text{full}}`$ 由经过 LAB 约束的潜在动作和直接手腕校正拼接而成：

```math
\boldsymbol{a}_t^{\text{full}} = [ \mathcal{D}(\boldsymbol{s}_t, \boldsymbol{\mu}_t^p + \lambda \boldsymbol{\sigma}_t^p \cdot \tanh(\boldsymbol{a}_t^{\text{latent}})), \boldsymbol{a}_t^{\text{correct}} ]
```

其中 $`\mathcal{D}(\cdot)`$ 表示基于马氏距离的障碍函数，$`\lambda`$ 控制约束的松紧程度，$`\tanh`$ 将潜在动作限制在 $`[-1, 1]`$ 范围内。该公式的自适应缩放特性——通过 $`\sigma_t^p`$ 调整有效探索半径——是 LAB 区别于简单残差约束的核心创新。

### 4. 仿真物理建模

为支持 sim-to-real 迁移，仿真环境对网球空气阻力进行了建模：

```math
\pmb{f}_{air} = -k \cdot m \cdot v \cdot ||\pmb{v}||
```

其中 $`m`$ 为网球质量，$`v`$ 为速度矢量，$`k`$ 为阻力系数。该力与速度大小的平方成正比，方向与速度相反，是动力学随机化（Table 2）中的关键随机化参数之一。

### 补充图表

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/005_Figure_4.jpg]]
*Figure 4: The motivation of Latent Action Barrier (LAB)*

## 实验与分析

### 仿真环境下的主实验结果

LATENT 在四项网球返回子任务（正手、反手、前场、后场）上进行了系统评估，使用成功率（SR↑）和距离误差（DE↓）作为核心指标。Table 3 给出了与五种基线方法的全面对比。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/008_Table_3.jpg]]
*Table 3: Comparison with baseline methods. Bold numbers indicate the best performance*

**与端到端 RL 基线的对比（vanilla PPO）**：无任何运动先验的 vanilla PPO 在所有任务上几乎完全失败。这验证了一个关键结论：从零开始学习人形机器人网球技能极其困难，纯粹的任务奖励信号不足以诱导出协调的全身运动与精确的击球动作。

**与解耦式运动生成基线的对比（MotionVAE）**：MotionVAE 采用“先离线学习运动生成，再在线跟踪”的解耦策略，其性能显著优于 vanilla PPO，但仍远低于 LATENT。以正手任务为例，LATENT 的成功率（96.52%）比 MotionVAE 高出约 20 个百分点。这揭示了离线运动生成器与在线任务策略之间的分布偏移是解耦方法的核心瓶颈——离线学到的运动分布无法覆盖任务策略实际需要的动作区域。

**与对抗式运动先验基线的对比（AMP, ASE）**：AMP 和 ASE 使用对抗式判别器来鼓励策略模仿运动数据中的风格，但它们在成功率上仍明显落后于 LATENT（正手任务差距约 15–20 个百分点）。原因在于，这些方法缺乏对不完美数据的显式修正机制：当参考运动中的手腕动作不精确时，对抗式先验反而会“固化”这些错误，而非修正它们。

**与潜在动作空间基线的对比（PULSE）**：PULSE 是与 LATENT 最接近的基线，同样采用潜在动作空间进行高层控制，但缺少手腕校正和潜在动作障碍（LAB）两个关键组件。LATENT 在正手成功率上领先 PULSE 约 3.4 个百分点，在反手上领先约 5.1 个百分点。这一差距在反手任务上更大，因为反手击球对手腕精度的要求更高，恰好放大了手腕校正机制的价值。

**距离误差指标**：LATENT 在距离误差上也全面领先——正手仅 1.32，反手 1.89，显著低于所有基线。低距离误差意味着击球点更接近球拍甜区，直接关系到回球质量和后续对打的可持续性。

### 消融实验

Table 4 报告了两个关键组件的消融结果。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/009_Table_4.jpg]]
*Table 4: Ablation study. Bold numbers indicate the best performance*

**移除手腕校正（w/o Corr.）**：正手成功率从 96.52% 骤降至 82.36%，反手从 82.10% 降至 68.94%。反手任务的降幅（约 13 个百分点）远大于正手（约 14 个百分点），这与直觉一致：反手击球时手腕处于更不自然的姿态，对精确控制的依赖更强。这一结果直接验证了核心设计动机——不完美人体运动数据中手腕动作的不精确性，必须通过直接校正机制来弥补。

**移除潜在动作障碍（w/o LAB）**：正手成功率降至 93.12%，反手降至 76.96%。除成功率下降外，论文还报告了运动质量的明显退化——机器人出现抖动。LAB 的机理在于：基于马氏距离的自适应约束使得探索范围随状态条件标准差动态缩放，在动作分布不确定性高的状态区域收紧约束，防止策略采样到不可行的动作；移除 LAB 后，策略可能探索到潜在空间中远离训练分布的区域，导致解码器生成的 PD 目标不稳定，表现为关节抖动。

**两个组件同时移除**：等同于退化为 PULSE 基线，性能进一步下降，验证了两者的互补性——手腕校正解决末端执行器精度问题，LAB 保证全身运动的稳定性和自然度。

### 真实世界部署与 Sim-to-Real 分析

Table 5 报告了在 Unitree G1 机器人上的真实世界评估结果。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/010_Table_5.jpg]]
*Table 5: Real-world performance. Bold numbers indicate the best*

**完整系统的真实世界表现**：LATENT 在正手任务上实现 90.90% 的成功率，并能稳定维持与人类的多回合对打（Figure 1）。从仿真到真实的成功率仅下降约 5.6 个百分点（96.52% → 90.90%），展现了良好的迁移能力。

**动力学随机化（DR）的关键性**：移除动力学随机化后，真实世界成功率暴跌至 16.67%。Table 2 列出了详细的随机化范围，涵盖机器人动力学（关节质量、阻尼、摩擦力等）和网球物理（空气阻力系数、恢复系数等）。这一极端对比表明，仿真中训练的策略对物理参数高度敏感，DR 是弥合 sim-to-real 鸿沟的不可或缺组件。

**观测噪声（ON）的关键性**：移除观测噪声后，成功率降至 50.00%。真实世界的感知系统（光学动作捕捉）不可避免地引入测量误差，在训练中注入观测噪声使策略学会了对抗状态估计的不确定性，而非过度拟合精确的仿真状态。

**需要手动验证的点**：论文未报告真实世界的反手任务成功率，也未提供真实世界消融的完整数据（仅对比了 DR 和 ON 的移除效果）。这些缺失数据可能反映了反手任务在真实世界部署中面临额外困难，需要进一步验证。

### 主要失败模式

基于实验结果和论文描述，可归纳以下失败模式：

1. **手腕精度不足导致的击球失败**：消融实验中移除手腕校正后成功率大幅下降，表明手腕控制是任务的关键瓶颈。在真实世界中，这一问题的严重程度可能因机械间隙和关节柔性而被放大。

2. **探索越界导致的运动不稳定**：移除 LAB 后出现的抖动现象，揭示了潜在空间探索中的核心风险——当策略采样到远离训练分布的区域时，变分解码器无法可靠地映射到有效的 PD 目标。

3. **sim-to-real 迁移中的物理参数失配**：无 DR 时 16.67% 的成功率表明，策略对质量、摩擦、恢复系数等物理参数高度敏感，任何未覆盖的参数偏移都可能导致灾难性失败。

4. **感知精度依赖**：系统依赖外部光学动作捕捉系统获取球状态，当感知信息不准确时（无 ON 训练时成功率仅 50%），策略无法有效应对。这限制了系统在非结构化环境中的自主部署能力。

### 场地覆盖与持续对打能力

Figure 5 的热力图展示了机器人在连续回球过程中的场地覆盖模式。随着连续回球次数增加（从 8 次到 400 次），机器人展现出有效的场地覆盖和自适应重新定位能力——策略学会了在每次回球后回到合理位置，为下一次击球做准备。Figure 6 的机器人自对弈评估进一步显示，在 50 局随机比赛中，连续回合数的分布表明策略能够维持多回合对打，而非仅完成单次击球。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/011_Figure_5.jpg]]
*Figure 5: Robot movement coverage during consecutive ball returns. Heatmaps of the robot’s global positions accumulated over different numbers of consecutive ball returns (8, 16, 80, and 400). The learned policy enables effective court coverage and adaptive repositioning during consecutive rallies*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/013_Figure_6.jpg]]
*Figure 6: Robot-robot self-play evaluation in simulation. (a) Visualization of two robots performing self-play on opposite sides of the court. (b) Distribution of number of consecutive rallies over 50 random games*

### 实验局限性与公平性考量

1. **部署基础设施依赖**：真实世界实验使用光学动作捕捉系统感知球状态，部署成本高且依赖外部基础设施，限制了户外和移动场景的扩展。

2. **任务设计的简化性**：评估局限于从固定位置发射球的单回合返回模式，未涵盖完整网球比赛中的发球、截击、对手行为预测和策略博弈。

3. **随机化参数的平台特异性**：sim-to-real 策略的成功严重依赖于精心调校的动力学随机化范围（Table 2），这些参数可能在其他机器人平台或任务上需要重新调整，泛化性有待验证。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/007_Table_2.jpg]]
*Table 2: Dynamics randomization used in LATENT. We randomize robot dynamics and tennis ball physics*

4. **数据来源的局限性**：训练数据仅来自业余球员，可能限制了动作的专业性和多样性，对于更高水平的竞技表现可能存在天花板效应。

### 补充图表

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/002_Figure_1.jpg]]
*Figure 1: (a) The humanoid performs multi-shot rallies with a human player using different stroke types across various court regions. (b) The humanoid performs athletic tennis skills to strike an incoming ball traveling at high speed (peak velocities > 15 m/s)*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/014_Figure_7.jpg]]
*Figure 7: Different hitting events in simulation. The red curves denote incoming ball trajectories, the robot posture corresponds to the moment of ball contact, and the green curves indicate the trajectories of the returned balls*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/015_Figure_8.jpg]]
*Figure 8: Close-up real-world examples. Representative frames from real-world rallies showing diverse tennis return behaviors, including forehand and backhand strokes, dynamic footwork, and coordinated whole-body motion*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2603_12686/figures/004_Table_1.jpg]]
*Table 1: Reward terms used in LATENT. The reward terms are divided into three types: Task, Regularization, and Termination*

## 方法谱系与知识库定位

### 1. 在具身技能学习谱系中的位置

LATENT 处于**分层人形机器人控制**与**运动先验引导强化学习**的交叉点。其核心思路——先构建潜在动作空间以表征自然运动，再训练高层策略在该空间中采样完成任务——继承自 PULSE（Luo et al., arXiv 2023）的潜在动作空间框架，但针对“不完美运动数据”这一现实约束做出了关键推进。

与现有工作的关系可从三个维度定位：

**（1）端到端无先验 RL（vanilla PPO）**
直接从头训练网球技能被证明“极其困难”（extremely difficult），因为网球任务的高维动作空间和稀疏奖励使得探索几乎不可能收敛。LATENT 通过引入运动先验绕过了这一瓶颈。

**（2）对抗式运动先验方法（AMP / ASE）**
AMP（Peng et al., TOG 2021）通过对抗式判别器鼓励策略模仿参考运动分布；ASE（Peng et al., TOG 2022）进一步将运动嵌入到可组合的技能潜在空间。然而，这些方法假设参考运动数据是精确且完整的。当面对不精确的手腕动作和不完整的技能片段时，对抗式先验会放大数据中的噪声，导致运动质量下降。LATENT 用**可校正的潜在空间**替代了对抗式先验的角色，使高层策略能够主动修正数据缺陷。

**（3）解耦式运动生成与跟踪（MotionVAE）**
MotionVAE 先离线生成运动序列，再通过跟踪控制器执行。这种两阶段方案缺乏闭环反馈，无法根据球状态实时调整动作。LATENT 的在线蒸馏和端到端高层策略训练保证了感知-动作闭环。

### 2. 关键设计决策与基线差异

LATENT 相对于最接近的前身 PULSE 做出了四项核心改动，每一项都针对“不完美数据”这一瓶颈：

| 设计槽位 | PULSE / 基线做法 | LATENT 做法 | 改动动机 |
|---|---|---|---|
| 手腕动作校正 | 无直接校正，完全依赖潜在空间生成 | 高层策略同时输出潜在动作和直接手腕 PD 目标 $a_t^{\text{planner}} = [a_t^{\text{latent}}, a_t^{\text{correct}}]$ | 业余数据中手腕动作不精确，直接校正使末端执行器能精准击球 |
| 潜在空间先验 | 固定单峰高斯先验 | 可学习的状态条件先验 $\mathcal{P}(z_t^p|s_t) = \mathcal{N}(z_t^p; \mu^p(s_t), \sigma^p(s_t))$ | 不同状态下的合理动作分布差异巨大，条件先验提供了更紧致的探索约束 |
| 探索约束 | 无约束或简单残差空间 | 基于马氏距离的潜在动作障碍（LAB），自适应缩放约束范围 | 欧氏距离无法反映各维度的状态依赖方差，LAB 允许在“安全”方向更多探索，在“危险”方向更保守 |
| 潜在空间构建 | 离线 VAE 蒸馏 | 在线 DAgger 蒸馏 + 条件变分瓶颈，且对右腕扰动鲁棒 | 离线蒸馏无法适应策略探索中的分布漂移；在线聚合缓冲区 $\mathcal{D}_{\text{agg}}$ 持续更新教师信号 |

### 3. 适用边界与局限

**数据依赖边界**：LATENT 的有效性建立在“准真实数据仍能提供有价值的运动先验”这一假设之上。当人类数据与机器人运动学差异过大（如关节限位、质量分布严重不匹配）时，运动跟踪器的模仿误差将传导至潜在空间，削弱先验质量。论文仅使用业余球员数据，专业级动作的覆盖度存疑。

**任务边界**：当前系统设计为从固定位置发射球的单回合返回任务，而非完整比赛。这意味着：
- 没有对手行为建模与博弈策略；
- 没有发球、截击、高压球等多样化技能；
- 没有比赛级别的连续决策与体能管理。

**部署边界**：真实世界部署依赖外部光学动作捕捉系统感知球状态，限制了自主性和户外场景扩展。消融实验（Table 5）显示，移除动力学随机化后成功率从 90.90% 骤降至 16.67%，移除观测噪声后降至 50.00%，表明 sim-to-real 转移对随机化参数极为敏感，迁移到其他机器人平台可能需要重新调校。

**评估边界**：当前评估仅覆盖成功率（SR）和距离误差（DE），缺少运动自然度、能量效率、对打持续性等细粒度指标。50 局自对弈的连续回合分布（Figure 6b）提供了初步的对打持续性证据，但未与人类对打数据对比。

### 4. 开放问题

1. **主动视觉替代动作捕捉**：如何用机载相机实现端到端的球跟踪与击球决策，使系统摆脱外部基础设施依赖？

2. **完整比赛扩展**：如何将框架从单回合返回扩展至包含发球、截击、对手行为预测的完整网球比赛？这可能需要引入多智能体强化学习（如 NFSP）进行自我博弈训练。

3. **自我博弈提升**：当前自对弈评估（Figure 6）仅为验证性实验。能否通过持续自我博弈使对打持续时间和技能水平自动提升，类似于 AlphaGo 的自我对弈进化？

4. **专业数据融合**：如何结合专业运动员数据以提升动作质量和赛事级表现？这可能需要处理专业数据与业余数据之间的分布差异。

5. **多平台泛化**：LAB 的马氏距离约束和 sim-to-real 随机化范围如何自动化适配不同的人形机器人平台，减少人工调校成本？

## 原文 PDF

![[paperPDFs/arxiv_2026/LATENT_Learning_Athletic_Humanoid_Tennis_Skills_from_Imperfect_Human_Motion_Data.pdf]]