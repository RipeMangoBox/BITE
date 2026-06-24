---
title: "CARI4D: Category Agnostic 4D Reconstruction of Human-Object Interaction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CARI4D_Category_Agnostic_4D_Reconstruction_of_Human_Object_Interaction.pdf
project_link: "https://nvlabs.github.io/CARI4D/"
code_link: "https://github.com/cmu-perceptual-computinglab/openpose"
aliases:
- CARI4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过粗到细的度量尺度恢复、动态姿态假设选择、类别无关的接触推理网络（CoCoNet）以及接触感知联合优化，有效地对齐了基础模型的预测，恢复了物体度量尺度，并引入了接触约束和时序平滑，从而实现了零样本泛化的4D人-物交互重建。
primary_logic: 核心思路是将多种基础模型的预测进行对齐以获得鲁棒初始化，然后基于渲染-比较范式训练一个类别无关的接触推理模型（CoCoNet）来细化交互并预测接触信息，最后通过接触感知的联合优化满足物理约束，从而实现从单目视频中重建空间和时间一致的4D交互，且不依赖物体模板或固定类别。
claims:
- 在BEHAVE数据集上，CARI4D的联合网格Chamfer距离（CD-c）为9.23 cm，相比VisTracker的14.22 cm降低了35%以上，相比于InterTrack的30.20 cm降低明显更多。
- 在未见过的InterCap数据集上零样本泛化，CD-c为12.88 cm，显著优于所有对比方法（VisTracker 20.17 cm，InterTrack 33.53 cm），相对提升超过36%。
- 消融实验证明，提出的动态姿态假设选择和前向后向估计将物体Chamfer距离从原始FoundationPose的1565.42 cm大幅降至16.85 cm（表3行a vs c），CoCoNet将人体CD-h从7.81降至7.01，接触联合优化将物体加速度误差从3.78降至0.38。
- BEHAVE (分布内) 上 CD-c↓ (cm) = 9.23
---

# CARI4D: Category Agnostic 4D Reconstruction of Human-Object Interaction

> [!tip] 核心洞察
> 核心思路是将多种基础模型的预测进行对齐以获得鲁棒初始化，然后基于渲染-比较范式训练一个类别无关的接触推理模型（CoCoNet）来细化交互并预测接触信息，最后通过接触感知的联合优化满足物理约束，从而实现从单目视频中重建空间和时间一致的4D交互，且不依赖物体模板或固定类别。

| 字段 | 内容 |
|------|------|
| 中文题名 | CARI4D：类别无关的人与物体交互4D重建 |
| 英文题名 | CARI4D: Category Agnostic 4D Reconstruction of Human-Object Interaction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.11988) · [Project](https://nvlabs.github.io/CARI4D/) · [Code](https://github.com/cmu-perceptual-computinglab/openpose) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CARI4D |
| Dataset | BEHAVE, InterCap |

> [!tip] 效果简介
> - BEHAVE (分布内) 上，CD-c↓ (cm) 9.23 vs 14.22 (VisTracker) (-5.0 cm (-35%))；Acc-o↓ (cm/s²) 0.35 vs 0.77 (VisTracker) (-0.42 cm/s²)。
> - InterCap (零样本) 上，CD-c↓ (cm) 12.88 vs 20.17 (VisTracker†) (-7.29 cm (-36%))；CD-o↓ (cm) 15.69 vs 27.41 (VisTracker†) (-11.72 cm)。

## 概述

从单目RGB视频中重建人与物体的4D交互（HOI）面临两个根本性瓶颈：**类别依赖**与**度量尺度模糊**。现有方法要么需要已知的物体模板（如VisTracker），要么只能处理预定义类别（如InterTrack），无法泛化到未见物体；同时，单目视频天然缺乏深度信息，导致人、物预测处于不同坐标系且尺度不一致。独立使用基础模型（如FoundationPose、NLF）虽能提供初始化，但预测含噪声、忽略精细接触，难以获得空间-时间一致的度量尺度重建。

CARI4D的核心思路是**将多种基础模型的预测对齐以获得鲁棒初始化，然后基于渲染-比较范式训练一个类别无关的接触推理网络（CoCoNet），最后通过接触感知的联合优化满足物理约束**。这一设计使方法能够从单目视频中重建空间和时间一致的4D交互，且不依赖物体模板或固定类别。

主要结果：在分布内BEHAVE数据集上，CARI4D的联合网格Chamfer距离（CD-c）为**9.23 cm**，相比VisTracker的14.22 cm降低超过35%；在未见InterCap数据集上零样本泛化，CD-c为**12.88 cm**，显著优于VisTracker的20.17 cm（相对提升超36%）。消融实验证实，动态姿态假设选择将物体Chamfer距离从原始FoundationPose的1565.42 cm大幅降至16.85 cm，接触感知联合优化将物体加速度误差从3.78 cm/s²降至0.38 cm/s²。

方法局限在于：严重依赖FoundationPose初始化，当发生严重遮挡或快速运动时可能出现翻转180°的姿态错误且难以纠正；未显式回归手指关节，在精细操控场景中手指姿态可能不真实。

## 背景与动机

### 问题背景

从单目RGB视频中重建人与物体的4D交互，是计算机视觉领域的一项基础性挑战。该任务要求同时恢复人体的三维姿态与形状、物体的几何与六自由度位姿，并在整个视频序列上保持时空一致性。这种重建能力对于具身智能、增强现实、人机协作等应用至关重要，因为智能系统需要理解人与周围物体如何在三维空间中实时交互。

### 现有方法及其缺口

当前的人-物交互重建方法存在三个核心瓶颈，严重制约了其在实际场景中的适用性。

**类别与实例依赖性。** 绝大多数现有方法依赖已知的物体模板或限定在预定义的物体类别内。例如，**InterTrack** 是一种类别特定的视频跟踪方法，仅能处理训练时见过的物体类别；**VisTracker** 则需要已知的实例级物体模板作为输入。这种依赖使得方法无法泛化到未见过的物体，而现实世界中物体的形态千差万别，从椅子、桌子到各种工具，远超出任何有限类别集合的覆盖范围。

**单目深度模糊与尺度不一致。** 单目视频天然缺乏深度信息，导致重建结果存在尺度模糊性。现有方法往往在各自的坐标系中独立预测人体和物体的姿态，未能将它们对齐到统一的度量空间。这意味着即使人体和物体的相对姿态在视觉上看似合理，其绝对尺度和相对距离可能严重偏离物理真实。

**接触交互的忽略与噪声累积。** 直接使用基础模型（如姿态估计器、深度估计器）的预测结果，会面临多源噪声叠加的问题：预测处于不同坐标系、含有随机误差，且完全忽略了精细的接触交互约束。在遮挡或快速运动场景下，这种噪声会迅速累积，导致重建结果出现物体漂浮、穿透等物理上不可能的状态。

### 本文动机与核心思路

针对上述缺口，CARI4D的核心理念是：**将多种基础模型的预测进行对齐以获得鲁棒初始化，然后基于渲染-比较范式训练一个类别无关的接触推理模型来细化交互，最后通过接触感知的联合优化满足物理约束。** 这一思路将问题分解为三个可控的阶段——度量尺度恢复与初始化、接触推理与细化、物理约束优化——每一阶段解决前序阶段的残余误差，最终实现从单目视频中重建空间和时间一致的4D交互，且不依赖任何物体模板或固定类别。

具体而言，CARI4D通过以下机制突破现有瓶颈：

- **粗到细的度量尺度恢复**：利用UniDepth等基础模型估计的深度信息，通过网格搜索和深度对齐策略，将物体重建结果恢复到真实的度量尺度。
- **动态姿态假设选择**：针对FoundationPose在遮挡下可能产生多候选姿态的问题，结合掩码IoU和时序平滑滤波，从候选集中筛选最优姿态，大幅提升初始化的鲁棒性。
- **类别无关的接触推理网络（CoCoNet）**：采用渲染-比较范式，将当前估计的交互状态渲染为RGB、深度和掩码图像，与输入观察进行对比，从而学习预测姿态增量更新和双手接触标签。该网络不依赖物体类别信息，天然支持零样本泛化。
- **接触感知联合优化**：基于CoCoNet预测的接触标签，构建包含接触距离、2D投影、掩码、穿透和加速度损失的多目标优化，在满足视觉约束的同时强制执行物理接触约束，消除漂浮和穿透伪影，并提升运动平滑度。

### 关键证据预览

实验结果表明，这一思路在定量和定性层面均取得了显著提升。在分布内BEHAVE数据集上，CARI4D的联合网格Chamfer距离（CD-c）为9.23 cm，相比VisTracker的14.22 cm降低了35%以上（Table 1）。在未见过的InterCap数据集上零样本泛化时，CD-c为12.88 cm，显著优于VisTracker的20.17 cm，相对提升超过36%（Table 2）。消融实验进一步验证了各模块的独立贡献：动态姿态假设选择将物体Chamfer距离从原始FoundationPose的1565.42 cm大幅降至16.85 cm（Table 3），接触感知联合优化将物体加速度误差从3.78 cm/s²降至0.38 cm/s²，证明了物理约束对时序平滑度的关键作用。

## 核心创新

CARI4D的核心创新在于将类别无关的4D人-物交互重建分解为**度量尺度恢复、鲁棒初始化、接触推理与物理约束优化**四个可解耦的环节，从根本上绕开了现有方法对已知物体模板和固定类别的依赖。其关键技术路径可归纳为以下五个 changed slots。

### 1. 物体姿态初始化：从单帧预测到动态姿态假设选择

现有方法直接使用**FoundationPose**的单帧预测作为物体姿态初始化，在遮挡和深度缺失时极易产生大幅度错误。CARI4D引入**动态姿态假设选择**机制：对FoundationPose输出的多个候选姿态，逐帧计算遮挡感知的掩码IoU（扣除人体掩码后的物体掩码交并比），并结合时序平滑滤波筛选最优姿态；同时采用前向-后向跟踪策略，从置信度最高的帧向两端传播，有效填补遮挡段的姿态缺失。消融实验中，这一改进将物体Chamfer距离（CD-o）从原始FoundationPose的1565.42 cm骤降至16.85 cm（Table 3 row a vs c），证明初始化质量是后续所有模块有效工作的前提。

### 2. 人体-物体空间对齐：融合NLF与UniDepth的度量深度

独立使用**NLF**估计人体姿态时，其预测处于未知尺度空间，与FoundationPose的物体姿态不在同一度量坐标系内。CARI4D将NLF的人体预测与**UniDepth**估计的度量深度进行对齐，使人体和物体统一到同一度量尺度空间。这一对齐操作消除了尺度模糊，为后续CoCoNet的渲染-比较范式提供了几何一致的输入。消融实验表明，仅对齐操作本身即可显著改善初始化质量（Table 3 row a vs c），是后续接触推理的前提条件。

### 3. 交互细化与接触推理：CoCoNet的渲染-比较范式

现有方法缺乏对精细交互的显式建模。CARI4D提出**CoCoNet**——一个类别无关的接触推理网络，采用**渲染-比较范式**：将当前估计的人体与物体姿态渲染为RGB图像、深度图和掩码，与输入观察拼接后送入时空注意力网络，预测姿态增量更新和双手接触标签。该网络不依赖任何物体类别先验，仅通过比较渲染结果与观察来推断交互状态。消融实验中，CoCoNet将人体CD-h从7.81 cm降至7.01 cm，物体CD-o从16.85 cm降至11.59 cm（Table 3 row c vs e），验证了渲染-比较范式对交互细化的有效性。

### 4. 训练时的深度对齐策略：消除分布偏移

CoCoNet训练时直接使用预测深度与GT深度存在系统性分布偏移（绝对平移误差）。CARI4D在训练前利用预测深度与GT深度的中位数及平均绝对偏差计算尺度和偏移参数：

$$s = \frac{\hat{s}^{\mathrm{gt}}}{\hat{s}^{\mathrm{pr}}}, \quad t = m^{\mathrm{gt}} - s \cdot m^{\mathrm{pr}}$$

将预测深度对齐到GT深度空间，消除误差模式偏移。消融实验显示，无此对齐时人体CD-h从7.81 cm恶化至8.01 cm（Table 3 row d vs e），证明该策略对降低CoCoNet学习难度的关键作用。

### 5. 接触感知联合优化：引入物理约束与时序平滑

仅靠CoCoNet的前馈预测无法保证物理合理性，常出现漂浮或穿透现象。CARI4D设计**接触感知联合优化**，以CoCoNet预测的接触标签为引导，联合优化人体和物体姿态参数，最小化加权组合的损失函数：

$$L = \lambda_c L_c + \lambda_{\mathrm{j2d}} L_{\mathrm{j2d}} + \lambda_m L_m + \lambda_{\mathrm{pen}} L_{\mathrm{pen}} + \lambda_{\mathrm{acc}} L_{\mathrm{acc}}$$

其中接触损失 $L_c = \sum_i d(\mathbf{J}_i^h, \mathbf{O}_i') \cdot \mathbf{c}_i$ 惩罚手部关节与物体点云的距离，加速度损失 $L_{\mathrm{acc}} = ||\mathbf{x}_i - 2\mathbf{x}_{i-1} + \mathbf{x}_{i-2}||_2^2$ 抑制时序抖动。消融实验表明，联合优化将物体加速度误差Acc-o从3.78 cm/s²大幅降至0.38 cm/s²（Table 3 row e vs f），显著提升运动平滑度和接触一致性（参见Figure 6的漂浮/穿透对比）。

**因果链路总结**：度量尺度恢复（Slot 1-2）提供几何一致的初始化 → 渲染-比较范式（Slot 3-4）实现类别无关的接触推理 → 物理约束优化（Slot 5）保证时空一致性。五个slot层层递进，共同构成了从单目视频到零样本4D重建的完整技术路径。

## 整体框架

CARI4D 的总体目标是从一段单目 RGB 视频中重建出度量尺度下的人和物体的 4D 交互——即恢复每一帧的人体姿态、物体姿态，并保持时空上一致的接触关系。整个流水线采用**自底向上的初始化 + 数据驱动的交互细化 + 物理约束的联合优化**三步范式，核心设计意图是**将多种基础模型的预测对齐到一个统一的度量空间，再通过渲染-比较范式学习一个类别无关的接触推理网络，最终用接触感知的优化满足物理一致性**。

### 输入与输出

- **输入**：一段单目 RGB 视频 $\{I_i\}_{i=1}^L$，共 $L$ 帧。
- **输出**：
  - 物体的度量尺度网格 $\mathbf{O}$ 及其每帧 6DoF 姿态 $\mathcal{O}_i = (\mathbf{R}^o, \mathbf{t}^o)$；
  - 人体每帧的 SMPL-H 参数 $\mathcal{H}_i = (\boldsymbol{\theta}, \beta, \mathbf{t}^h)$（姿态、体型、全局平移）；
  - 每帧双手与物体的接触标签 $\mathbf{c}_i \in \{0,1\}^2$。

### 流水线模块

Figure 2 给出了完整的流水线概览，四个核心模块依次为：

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/002_Figure_2.jpg]]
*Figure 2: CARI4D method overview. Given a monocular RGB video, we reconstruct the 4D human and object at metric scale with consistent contacts. We start by estimating the metric-scale object mesh (Sec. 3.1), followed by initialization of human and object poses using dynamic pose hypothesis selection (Sec. 3.2). We then train a category agnostic contact reasoning model (CoCoNet) to refine the interaction poses and estimate hand contacts (Sec. 3.3) which are used to perform contact aware joint optimization (Sec. 3.4)*

1. **度量尺度物体重建（Metric-scale Object Reconstruction, Sec. 3.1）**
   从视频首帧出发，利用 Hunyuan3D-2 重建物体的归一化网格，再通过 UniDepth 估计的度量深度图与 FoundationPose 的网格搜索，以粗到细的策略恢复物体的真实物理尺度。这一步解决了“物体长什么样、实际多大”的问题。

2. **人-物姿态初始化（Human and Object Pose Initialization, Sec. 3.2）**
   - **物体姿态**：对每一帧用 FoundationPose 生成多个候选姿态，再通过**动态姿态假设选择**——结合遮挡感知的掩码 IoU 和时序平滑滤波——筛选出最优姿态序列。对于遮挡严重的帧，还引入前向-后向跟踪来填补姿态缺失。
   - **人体姿态**：使用 NLF 估计每帧的 SMPL 参数，然后将其预测的深度与 UniDepth 的度量深度对齐，使人体与物体处于**同一度量空间**。
   
   这一模块的关键作用是提供一个**鲁棒的初始姿态序列**，为后续细化网络提供合理的起点。

3. **CoCoNet：类别无关的接触推理网络（Category-Agnostic Contact Reasoning Network, Sec. 3.3）**
   CoCoNet 是方法的核心学习模块。它采用**渲染-比较范式**：将当前估计的人/物姿态渲染为 RGB 图、深度图和掩码图，与输入观察拼接后送入一个具有时空注意力的网络。网络同时预测：
   - 人体和物体姿态的增量更新；
   - 双手的接触标签。
   
   训练时，一个关键的策略是将预测深度与真值深度按尺度和偏移对齐（见公式 $s = \frac{\hat{s}^{\mathrm{gt}}}{\hat{s}^{\mathrm{pr}}},\; t = m^{\mathrm{gt}} - s \cdot m^{\mathrm{pr}}$），以消除绝对平移误差的分布偏移，降低网络的学习负担。

4. **接触感知联合优化（Contact-Aware Joint Optimization, Sec. 3.4）**
   以 CoCoNet 的预测为初始化，对每帧的人体和物体姿态参数进行优化，最小化一个组合损失函数：
   $$L = \lambda_c L_c + \lambda_{\mathrm{j2d}} L_{\mathrm{j2d}} + \lambda_m L_m + \lambda_{\mathrm{pen}} L_{\mathrm{pen}} + \lambda_{\mathrm{acc}} L_{\mathrm{acc}}$$
   其中：
   - $L_c$：接触损失，当 CoCoNet 预测手与物体接触时，惩罚手关节到物体点云的最小距离；
   - $L_{\mathrm{j2d}}$ 和 $L_m$：2D 投影损失和遮挡感知掩码损失，保持视觉一致性；
   - $L_{\mathrm{pen}}$：穿透损失，防止人-物几何穿插；
   - $L_{\mathrm{acc}}$：加速度损失 $||\mathbf{x}_i - 2\mathbf{x}_{i-1} + \mathbf{x}_{i-2}||_2^2$，抑制关节和物体姿态的抖动，提升时序平滑度。

### 设计逻辑与因果链

整个流水线的设计遵循一条清晰的因果链：**基础模型的原始预测处于不同坐标系、含有噪声且忽略接触交互 → 通过度量尺度对齐和动态姿态选择获得鲁棒初始化 → CoCoNet 学习类别无关的交互细化与接触推理 → 接触感知优化施加物理约束和时序平滑 → 得到空间和时间一致的 4D 重建**。这一链条使得方法能够在**不依赖物体模板和固定类别**的前提下，实现零样本泛化。

## 核心模块与公式推导

CARI4D 的核心流水线由四个关键模块串联而成，每个模块解决一个特定的子问题，最终实现从单目 RGB 视频到度量尺度 4D 人-物交互重建的端到端流程（Figure 2）。

### 1. 度量尺度物体重建（Metric-scale Object Reconstruction）

给定视频的首帧，该模块负责重建物体的三维网格并恢复其真实物理尺度。流程采用由粗到细的策略：首先利用 **Hunyuan3D-2** 从 RGB 图像生成物体网格，但此时网格处于未知的归一化尺度空间。为恢复度量尺度，模块通过网格搜索的方式，将不同缩放系数的物体网格渲染后与 **UniDepth** 估计的度量深度图进行对齐，选择最优缩放因子，从而得到具有真实尺度的物体网格。这一步骤使得后续的人体与物体能够处于统一的度量坐标空间中。

### 2. 动态姿态假设选择（Dynamic Pose Hypothesis Selection）

物体姿态的初始化是后续跟踪与细化的基础。直接使用 **FoundationPose** 的单帧预测在遮挡和深度缺失场景下极易产生大幅误差。为此，该模块设计了两个筛选准则：

- **掩码 IoU 筛选**：对 FoundationPose 输出的多个候选姿态，将渲染的物体掩码与输入物体掩码计算交并比。为处理遮挡，输入掩码需先减去人体掩码：

$$
\tilde{\mathbf{M}}_{i}^{o} = \mathbf{M}_{i}^{o} \cap (\sim \mathbf{M}_{i}^{h})
$$

$$
\mathrm{IoU}_{i}^{j} = \sum \tilde{\mathbf{M}}_{i}^{j} \cap \tilde{\mathbf{M}}_{i}^{o}
$$

- **时序平滑筛选**：在掩码 IoU 基础上，进一步选择与前一帧姿态差异最小的候选，抑制帧间抖动。

此外，模块引入前向-后向跟踪策略：分别从视频首帧正向跟踪和末帧反向跟踪，融合两方向的估计以提升鲁棒性。消融实验（Table 3，行 a vs c）表明，该模块将物体 Chamfer 距离从原始 FoundationPose 的 1565.42 cm 大幅降至 16.85 cm。

### 3. CoCoNet：类别无关的接触推理网络

CoCoNet 是方法的核心学习模块，负责细化人/物姿态并预测双手接触标签。其设计遵循 **渲染-比较范式**（render-and-compare），结合时空注意力机制：

- **输入**：将当前帧的 RGB 观察、深度图、掩码与基于当前姿态渲染的 RGB、深度、掩码拼接，形成“比较”输入；同时输入带彩色纹理的 SMPL 人体网格，以增强语义推理。
- **输出**：人体姿态增量 $\{\mathcal{H}_i\}$、物体姿态增量 $\{\mathcal{O}_i\}$，以及二值接触标签 $\{\mathbf{c}_i\}$，指示左右手是否与物体接触。
- **训练策略**：使用 L1 损失监督姿态增量，二值交叉熵损失监督接触标签。关键创新在于训练前对深度进行对齐——将预测深度与真值深度通过尺度和偏移对齐，消除分布偏移：

$$
s = \frac{\hat{s}^{\mathrm{gt}}}{\hat{s}^{\mathrm{pr}}}, \quad t = m^{\mathrm{gt}} - s \cdot m^{\mathrm{pr}}
$$

其中 $\hat{s}^{\mathrm{pr}}$ 和 $\hat{s}^{\mathrm{gt}}$ 分别为预测深度与真值深度的中位数绝对偏差，$m^{\mathrm{pr}}$ 和 $m^{\mathrm{gt}}$ 为各自的中位数。消融实验（Table 3，行 d vs e）证实，无此对齐时人体 CD-h 从 7.81 cm 恶化至 8.01 cm，验证了该策略的有效性。

### 4. 接触感知联合优化（Contact-aware Joint Optimization）

CoCoNet 的前馈预测虽已较好，但仍可能违反物理约束（如漂浮、穿透）。该模块利用 CoCoNet 预测的接触标签 $\mathbf{c}_i$，对人/物姿态参数进行后优化，目标函数为五项损失的线性组合：

$$
L = \lambda_{c} L_{c} + \lambda_{\mathrm{j2d}} L_{\mathrm{j2d}} + \lambda_{m} L_{m} + \lambda_{\mathrm{pen}} L_{\mathrm{pen}} + \lambda_{\mathrm{acc}} L_{\mathrm{acc}}
$$

各损失项含义如下：

- **接触损失 $L_c$**：当 $\mathbf{c}_i = 1$ 时，惩罚双手关节与变形后物体点云之间的最小距离：

$$
L_{c} = \sum_{i} d(\mathbf{J}_{i}^{h}, \mathbf{O}_{i}^{\prime}) \cdot \mathbf{c}_{i}
$$

- **2D 投影损失 $L_{\mathrm{j2d}}$**：约束三维关节的二维投影与观测一致。
- **遮挡感知掩码损失 $L_m$**：约束渲染掩码与输入掩码的差异。
- **穿透损失 $L_{\mathrm{pen}}$**：惩罚人体网格与物体网格的相互穿透。
- **加速度损失 $L_{\mathrm{acc}}$**：抑制帧间抖动，提升运动平滑度：

$$
L_{\mathrm{acc}} = ||\mathbf{x}_{i} - 2\mathbf{x}_{i-1} + \mathbf{x}_{i-2}||_{2}^{2}
$$

消融实验（Table 3，行 e vs f）表明，联合优化将物体加速度误差从 3.78 cm/s² 降至 0.38 cm/s²，显著提升了时序一致性。Figure 6 的定性对比进一步展示了有无接触优化时的差异：无优化时出现物体漂浮或穿透，优化后手-物交互贴合自然。

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/007_Figure_6.jpg]]
*Figure 6: Importance of contacts. Without our contact-aware optimization, the model does not properly handle the fine-grained hand-object interaction, leading to floating object or penetration errors. (Purple balls indicate contact predictions.)*

### 补充图表

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/011_Figure_7.jpg]]
*Figure 7: CoCoNet architecture. Here b, t, h, w denote batch size, temporal window size, image height and width respectively. We follow a render-and-compare paradigm, hence RGB a and RGB b denote the image from input observation and rendering respectively, same for xyz map and mask (human and object stacked together)*

## 实验与分析

### 核心性能：分布内与零样本泛化

CARI4D在分布内数据集BEHAVE和未见数据集InterCap上均表现出显著优势，其核心指标**联合网格Chamfer距离（CD-c）**全面超越现有方法。

**BEHAVE（分布内）**：CARI4D的CD-c达到**9.23 cm**，相比VisTracker的14.22 cm降低约**35%**，相比InterTrack的30.20 cm降幅更为显著（Table 1）。在物体Chamfer距离（CD-o）上，CARI4D为12.05 cm，VisTracker为14.34 cm；在人体Chamfer距离（CD-h）上，CARI4D为7.74 cm，VisTracker为12.84 cm。时序平滑性方面，CARI4D的物体加速度误差（Acc-o）仅为**0.35 cm/s²**，远低于VisTracker的0.77 cm/s²和InterTrack的2.53 cm/s²。值得注意的是，VisTracker需要已知物体模板作为输入，为公平对比，作者将其增强为使用CARI4D重建的物体模板（表中标记为†）。

**InterCap（零样本泛化）**：在完全未见的InterCap数据集上，CARI4D的CD-c为**12.88 cm**，显著优于VisTracker†的20.17 cm（相对提升**36%**）和InterTrack的33.53 cm（Table 2）。物体CD-o从VisTracker†的27.41 cm降至15.69 cm，人体CD-h从15.67 cm降至11.40 cm。这表明CARI4D的类别无关设计使其能够泛化到训练时未见的物体类别和交互场景。

**评估公平性说明**：评估采用首帧对齐到真值并将同一刚性变换应用于全视频的方式，衡量全局平移一致性，而非逐帧对齐。InterTrack是类别特定方法，在未见类别上测试并非其设计目标，但其结果仍列出以供参考。

### 消融实验：各模块贡献

Table 3的消融实验系统验证了CARI4D流水线中每个关键模块的贡献：

**初始化策略（行a→c）**：原始FoundationPose（FP）的单帧预测（行b）物体CD-o高达1565.42 cm，完全不可用。加入NLF人体预测与UniDepth深度对齐后（行c），物体CD-o骤降至**16.85 cm**，人体CD-h从9.56 cm降至7.81 cm。这证明**动态姿态假设选择**（掩码IoU + 时序平滑滤波 + 前向后向跟踪）和**人体深度对齐**是获得可用初始化的决定性步骤。

**CoCoNet细化（行c→e）**：加入CoCoNet后，人体CD-h从7.81 cm进一步降至**7.01 cm**，物体CD-o从16.85 cm降至**11.59 cm**。行d与行e的对比揭示了一个关键训练策略：**训练时对预测深度与GT深度进行尺度和偏移对齐**（式(1)）至关重要——无对齐时人体CD-h反而恶化至8.01 cm，因为预测深度与GT深度之间的分布偏移增加了CoCoNet的学习难度。

**接触感知联合优化（行e→f）**：最终优化阶段对时序平滑性贡献最大——物体加速度误差Acc-o从3.78 cm/s²骤降至**0.38 cm/s²**，人体加速度Acc-h从1.41 cm/s²降至1.14 cm/s²。这验证了式(2)中加速度损失$L_{\mathrm{acc}}$和接触损失$L_c$的有效性。

### 鲁棒性与敏感性分析

**对基础模型误差的鲁棒性**（Figure 8）：在UniDepth和FoundationPose注入不同程度噪声的条件下，CARI4D的最终性能保持稳定且始终优于VisTracker。这表明CoCoNet的渲染-比较范式和后续联合优化能够有效补偿上游基础模型的预测误差，而非简单依赖其精度。

**Oracle研究**（Table 4）：当提供真实深度或真实物体网格时，CARI4D性能仅小幅提升（CD-c从9.23 cm降至约8.6 cm），说明在仅使用估计深度训练的条件下，模型已接近性能上界，进一步验证了所提深度对齐策略的有效性。

### 效率分析

Table 5显示，处理一段300帧视频，CARI4D平均耗时约**15分钟**，显著快于VisTracker（约25分钟）和InterTrack（约50分钟），同时精度更高。效率优势源于CoCoNet的前馈推理与轻量级联合优化的组合设计。

### 按交互类型分析

Table 6将BEHAVE数据集的性能按交互类型细分：手动交互（如抓握）、坐姿、肩部接触、倚靠等。CARI4D在所有类型上均保持较低的Chamfer距离，但在涉及精细手指操作的场景（如抓取小物体）中误差相对较高，这与方法的已知局限一致——CARI4D主要关注全身层面交互，未显式回归手指关节。

### 失败模式

Figure 11揭示了两个典型失败场景：
1. **精细手指操作**：当任务需要精确的手指姿态（如端盘子），CARI4D无法重建真实的手指姿态，因为CoCoNet仅预测双手接触标签，不回归手指关节细节。
2. **初始化翻转**：在高度动态运动和极端遮挡下，FoundationPose可能输出翻转180°的错误姿态。该旋转误差过大，后续CoCoNet细化和联合优化均无法纠正，导致最终重建失败。这表明方法对FoundationPose初始化质量存在硬性依赖。

### 定性结果

Figure 3和Figure 4分别展示了BEHAVE和InterCap上的定性对比。CARI4D重建的物体网格形状完整、姿态准确，而InterTrack仅输出噪声点云，VisTracker†虽使用重建网格但跟踪精度不足。Figure 5展示了在野生互联网视频上的泛化能力，CARI4D在物体姿态、接触预测和整体一致性方面均优于PICO、InterTrack和VisTracker。Figure 6通过消融可视化证明了接触感知优化的重要性：无优化时手与物体之间出现漂浮或穿透，优化后交互贴合自然。

### 补充图表

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/006_Table_1.jpg]]
*Table 1: Evaluation results on BEHAVE [3] dataset (unit: cm). Our method significantly outperforms previous instance-specific VisTracker [57] and category-specific InterTrack [11]*

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/005_Table_2.jpg]]
*Table 2: Zero-shot generalization to unseen InterCap [18] dataset (unit: cm). ∗Denotes key-frames only, where acceleration metrics do not apply. Our method outperforms both image based method PICO [10] and video based tracking methods [57, 59]*

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/010_Table_3.jpg]]
*Table 3: Ablation studies. Our proposed initialization (c) is better than running vanilla (a, b) NLF [37] and FoundationPose (FP [52]). Our contact reasoning model trained with the proposed alignment (e) further improves the accuracy. Joint optimization (f) improves smoothness and contact consistency (see Fig. 6)*

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/012_Figure_8.jpg]]
*Figure 8: Sensitivity analysis of UniDepth and FoundationPose errors on the final performance*

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/009_Table_4.jpg]]
*Table 4: Oracle study. Trained on estimated depth, our model also allows input with ground truth depth or object mesh and achieves slightly better results*

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/013_Table_5.jpg]]
*Table 5: Average runtime (minutes) to process one video of 300 frames. Our method is much faster than baselines while being more accurate*

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/015_Table_6.jpg]]
*Table 6: Performance of our method per interaction type*

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/008_Figure_5.jpg]]
*Figure 5: Generalization to in-the-wild videos. Prior methods predict noisy shape (InterTrack [59]), flipped object pose (Vis-Tracker [57], † with our object reconstruction) or wrong contacts and object position (PICO [10]). Our method generalizes better overall. (Purple balls indicate contact predictions.)*

![[assets/figures/papers/paper_list_l1010_https_arxiv_org_abs_2512_11988/figures/017_Figure_11.jpg]]
*Figure 11: Failure case examples. Our method focuses on full body interaction and the detailed hand poses are not handled, which can be important for fine-grained object manipulation task (top row). Our method thus failed to reconstruct realistic finger poses for holding the plate. Under highly dynamic motion and extreme occlusion (bottom row), FoundationPose predicts flipped object pose for initialization. Such large rotation error is not able to be corrected by our refinement process in subsequent steps, leading to inaccurate reconstruction in the end*

## 方法谱系与知识库定位

### 问题域定位：从类别依赖到零样本泛化

CARI4D 试图解决的核心问题是单目 RGB 视频中人与任意物体交互的 4D 重建。此前的代表性方法可大致分为两条技术路线：

- **类别特定（category-specific）的跟踪方法**：以 **InterTrack** 为代表，通过在特定物体类别（如椅子、桌子）上训练，从视频中同时重建人体和物体点云并跟踪姿态。其根本局限在于无法泛化到训练时未见过的物体类别，重建的几何形状为噪声点云而非高质量网格。
- **实例特定（instance-specific）的跟踪方法**：以 **VisTracker** 为代表，要求预先提供被测物体的已知 3D 模板，通过视频跟踪恢复物体姿态。这种依赖使其无法处理“在野外”任意物体——因为模板本身不可得。为公平对比，CARI4D 将 VisTracker 增强为使用自身重建的物体网格（表中标记为 †），即便如此，其重建精度仍显著落后。

此外，基于单帧图像的优化方法如 **PICO** 虽然不依赖视频时序，但缺乏时序一致性约束，在零样本场景下物体定位和接触预测均不可靠（见 Figure 5 定性对比）。

CARI4D 在这两条路线之外开辟了第三条路径：**类别无关（category-agnostic）的零样本 4D 重建**。其关键区别在于：既不依赖已知物体模板，也不限制物体类别，而是通过组合多个基础模型的预测并进行对齐、细化和联合优化，实现对任意物体的度量尺度重建与跟踪。

### 核心方法谱系：基础模型组合与接触感知优化

CARI4D 的方法架构由五个顺序模块构成，每个模块对应一个已识别的瓶颈：

| 模块 | 解决的瓶颈 | 核心机制 |
|------|-----------|---------|
| 度量尺度物体重建（Sec. 3.1） | 单目视频缺乏深度信息，物体尺度模糊 | 使用 Hunyuan3D-2 重建物体网格，通过 UniDepth 估计度量深度，结合 FoundationPose 的网格搜索粗到细恢复尺度 |
| 物体姿态假设选择（Sec. 3.2） | 基础模型预测含噪声，遮挡下 FoundationPose 易输出错误姿态 | 动态姿态假设选择：基于掩码 IoU（去除人体掩码后计算）和时序平滑滤波，从前向后向估计中筛选最优姿态 |
| 人体姿态估计与深度对齐（Sec. 3.2） | NLF 人体预测与物体处于不同坐标系 | 将 NLF 预测与 UniDepth 度量深度对齐，使人、物统一到同一度量空间 |
| CoCoNet 接触推理网络（Sec. 3.3） | 独立基础模型忽略精细接触交互 | 类别无关的渲染-比较范式，结合时空注意力，预测姿态增量更新和双手接触标签 |
| 接触感知联合优化（Sec. 3.4） | 前馈预测缺乏物理约束和时序一致性 | 基于 CoCoNet 预测的接触标签，联合优化人/物姿态，最小化接触距离、重投影误差、穿透和加速度 |

**关键设计决策的因果链路**：

1. **初始化质量决定了后续细化的上限**：消融实验（Table 3）表明，原始 FoundationPose 的物体 Chamfer 距离高达 1565.42 cm（行 a），经动态姿态假设选择和前向后向估计后骤降至 16.85 cm（行 c），降幅超过 98%。这一初始化策略是后续 CoCoNet 能够有效工作的前提——如果初始姿态翻转 180°，CoCoNet 的细化能力不足以纠正如此大的旋转误差（见 Figure 11 失败案例）。

2. **深度对齐消除分布偏移**：训练 CoCoNet 时，若直接将预测深度作为输入而不与 GT 深度对齐，人体 CD-h 从 7.81 cm 恶化至 8.01 cm（Table 3 行 d vs e）。对齐策略通过计算尺度 $s$ 和偏移 $t$（使用中位数和平均绝对偏差，见 Eq. 1），将预测深度的误差模式校正到与 GT 一致，降低了网络的学习负担。

3. **接触约束是物理合理性的关键**：消融实验显示，接触感知联合优化将物体加速度误差从 3.78 cm/s² 降至 0.38 cm/s²（Table 3 行 e vs f），降幅达 90%。定性结果（Figure 6）进一步表明，无接触优化时出现物体漂浮或穿透，而加入接触损失后交互变得贴合。

### 知识库定位：基础模型的编排者而非替代者

CARI4D 的独特定位在于它**不试图替代任何基础模型**，而是作为一个“编排层”（orchestration layer），将多个现成模型的预测对齐、细化并施加物理约束。这种设计使其天然具备以下特性：

- **可升级性**：Oracle 研究（Table 4）表明，当提供真实深度或物体网格时，模型性能进一步提升，说明各基础模型可被更优版本替换而无需改变整体架构。
- **鲁棒性**：敏感性分析（Figure 8）显示，即使在 UniDepth 和 FoundationPose 注入噪声的条件下，CARI4D 最终性能仍保持稳定且始终优于 VisTracker，表明编排层对底层模型误差具有一定容忍度。
- **效率优势**：Table 5 显示，处理 300 帧视频的平均运行时间显著低于对比方法，同时精度更高。

### 适用边界与局限

CARI4D 的适用边界由其设计选择直接决定：

1. **全身交互 vs. 精细手指操作**：方法显式建模的是双手关节与物体的接触（通过 CoCoNet 预测接触标签），但未回归手指关节姿态。在涉及小物体或精细操控的场景（如捏住盘子边缘），手指姿态可能不真实，接触细节不准确（见 Figure 11 上行失败案例）。这一局限源于 SMPL-H 模型本身对手指的简化表示，以及训练数据中缺乏细粒度手指接触标注。

2. **对 FoundationPose 初始化的强依赖**：当发生严重遮挡或快速运动时，FoundationPose 可能输出翻转 180° 的错误姿态。由于 CoCoNet 的细化能力受限于局部搜索范围，如此大的旋转误差无法被纠正，导致最终重建失败（见 Figure 11 下行失败案例）。这是当前流水线的单点故障源。

3. **双手接触 vs. 躯干/多人接触**：当前 CoCoNet 仅预测双手接触标签，联合优化中的接触损失也仅作用于手部关节。对于躯干倚靠、肩部接触等交互类型，方法虽能通过整体姿态优化间接改善，但缺乏显式的接触建模（Table 6 按交互类型划分的性能可进一步验证此点，需手动确认具体数值）。

### 开放问题

1. **集成手部姿态估计器**：能否将专用手部姿态估计器（如 HaMeR、Hawor）作为额外的基础模型纳入编排层，在保持全身一致性的同时捕获精细手指运动？这需要在 CoCoNet 的输入表示和损失函数中增加手部关节的显式建模。

2. **运动填充与时间先验**：能否引入类似 GLAMR 或 VisTracker 中的运动填充机制，从可见帧外推遮挡段的运动？这将是解决 FoundationPose 初始化失败的关键——即使初始帧姿态错误，强时间先验可能帮助从后续帧恢复正确姿态。

3. **更复杂的交互推理**：在训练数据更加多样化的条件下，CoCoNet 能否学习躯干接触、多人协作等更复杂的交互模式？当前的双接触标签输出可扩展为多部位接触预测，但需要相应的标注数据支持。

4. **端到端训练的可能性**：当前流水线是模块化的，各基础模型独立运行。能否将部分模块（如深度对齐、姿态选择）纳入可微分框架，实现端到端的联合训练，进一步提升整体性能？

## 原文 PDF

![[paperPDFs/CVPR_2026/CARI4D_Category_Agnostic_4D_Reconstruction_of_Human_Object_Interaction.pdf]]