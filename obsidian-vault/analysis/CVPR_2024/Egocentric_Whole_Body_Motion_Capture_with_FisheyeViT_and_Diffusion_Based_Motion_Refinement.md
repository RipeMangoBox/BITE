---
title: "Egocentric Whole-Body Motion Capture with FisheyeViT and Diffusion-Based Motion Refinement"
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/Egocentric_Whole_Body_Motion_Capture_with_FisheyeViT_and_Diffusion_Based_Motion_Refinement.pdf
aliases:
- FPA3HDBMR
- EWBMCFDBMR
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过FisheyeViT将鱼眼图像划分为等FOV的未畸变小块作为ViT令牌，使用像素对齐的3D热图回归器在uvd空间中预测关节位置并保留不确定性，再结合基于不确定性的扩散模型对全身运动进行细化，有效缓解了畸变和遮挡问题。"
primary_logic: "将鱼眼相机畸变校正嵌入Vision Transformer框架，并通过在图像uv空间回归3D热图实现像素级对齐，使得预测的关节可以无缝衔接到鱼眼重投影。同时，引入不确定性引导的全身运动扩散先验，能够在保留高置信关节的同时生成遮挡区域的合理运动，显著提高了时序一致性和精度。"
claims:
- "在SceneEgo测试集上，单帧方法Ours-Single的MPJPE达到64.19 mm，比之前最好的SceneEgo (118.5 mm) 提高了45.7%，扩散精炼后进一步降至57.59 mm。"
- "消融研究显示，移除FisheyeViT会导致MPJPE从64.19上升到67.36，证明其缓解鱼眼畸变的有效性。"
- "移除不确定性引导后，精炼方法MPJPE从57.59上升到62.16，证实不确定性信息对扩散细化的关键作用。"
- "使用基于MLP的直接回归替换像素对齐的3D热图，MPJPE剧增至130.7 mm，说明该热图表示对准确度至关重要。"
---

# Egocentric Whole-Body Motion Capture with FisheyeViT and Diffusion-Based Motion Refinement

> [!tip] 核心洞察
> 将鱼眼相机畸变校正嵌入Vision Transformer框架，并通过在图像uv空间回归3D热图实现像素级对齐，使得预测的关节可以无缝衔接到鱼眼重投影。同时，引入不确定性引导的全身运动扩散先验，能够在保留高置信关节的同时生成遮挡区域的合理运动，显著提高了时序一致性和精度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于FisheyeViT和扩散运动精炼的以自我为中心全身运动捕捉 |
| 英文题名 | Egocentric Whole-Body Motion Capture with FisheyeViT and Diffusion-Based Motion Refinement |
| 会议/期刊 | CVPR 2024 |
| Links | [paper](https://arxiv.org/abs/2311.16495) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FisheyeViT with Pixel-Aligned 3D Heatmap and Diffusion-Based Motion Refinement |
| Dataset | SceneEgo test dataset, GlobalEgoMocap test dataset, Mo²Cap² test dataset, SceneEgo test dataset (hands) |

> [!tip] 效果简介
> - SceneEgo test dataset 上，MPJPE (body, mm) 为 57.59 (Ours-Refined†)，对比 118.5 (SceneEgo)，变化 -60.91。
> - GlobalEgoMocap test dataset 上，PA-MPJPE (body, mm) 为 65.83 (Ours-Refined†)，对比 76.50 (SceneEgo)，变化 -10.67。
> - Mo²Cap² test dataset 上，PA-MPJPE (body, mm) 为 72.63 (Ours-Refined†)，对比 79.65 (SceneEgo)，变化 -7.02。

## 概述

从单视角头戴鱼眼相机捕捉全身运动是一项极具挑战的任务。核心瓶颈在于三点：鱼眼镜头引入的严重畸变使传统卷积或Transformer网络难以提取有效特征；以自我为中心的视角导致身体末端（脚、手）频繁发生自遮挡；以及缺乏同时标注身体与手部的大规模训练数据。现有方法或依赖场景几何先验，或直接作用于畸变图像，精度与鲁棒性均受限制。

本文提出了一套完整的以自我为中心全身运动捕捉框架，其核心洞察在于将鱼眼畸变校正嵌入Vision Transformer的特征提取过程，并通过在图像uv空间回归像素对齐的3D热图实现关节预测与鱼眼重投影的无缝衔接。具体而言，**FisheyeViT**通过球面投影将鱼眼图像划分为等视场角的未畸变小块作为ViT令牌，从源头缓解畸变；**像素对齐3D热图回归器**在uvd空间预测关节位置并保留热图最大值作为不确定性估计；在此基础上，**不确定性引导的全身运动扩散先验**对整段运动序列进行时序精炼——高置信关节得以保留，遮挡区域的运动则由扩散模型生成合理补全。

在SceneEgo测试集上，单帧方法Ours-Single的MPJPE达到64.19 mm，比此前最优的SceneEgo（118.5 mm）降低45.7%；经扩散精炼后进一步降至57.59 mm。手部姿态方面，MPJPE从Hand4Whole的49.66 mm降至19.37 mm。消融实验证实，移除FisheyeViT导致MPJPE上升至67.36 mm，移除不确定性引导则使精炼后MPJPE从57.59回升至62.16 mm，验证了各模块的关键作用。

## 背景与动机

从单视角头戴鱼眼相机捕捉全身运动是计算机视觉领域一项极具挑战性的任务。鱼眼相机因其超宽视场角（FOV）能够覆盖佩戴者身体的大部分区域，使其成为以自我为中心（egocentric）运动捕捉的理想传感器。然而，这一技术路线面临三大核心瓶颈，严重制约了现有方法的精度与鲁棒性。

**第一重瓶颈：鱼眼畸变与特征提取的失配。** 鱼眼镜头产生的严重几何畸变使得标准卷积神经网络（CNN）或视觉Transformer（ViT）难以提取有效的图像特征。传统网络假设图像遵循透视投影，其平移不变性等归纳偏置在鱼眼图像上不再成立。现有工作要么忽略畸变直接输入网络，要么采用全局畸变校正后再处理，但全局校正往往导致图像边缘信息的大量丢失或重采样伪影，无法从根本上解决特征提取的失配问题。

**第二重瓶颈：以自我为中心视角下的自遮挡。** 头戴相机的位置决定了身体部位——尤其是脚部和手部——频繁经历自遮挡。当佩戴者进行日常活动时，双手和双脚经常处于相机视野之外或被躯干遮挡。单帧方法缺乏时序上下文，在遮挡区域只能依赖模糊的视觉线索进行猜测，导致预测结果抖动剧烈、时序一致性差。

**第三重瓶颈：大规模标注数据的匮乏。** 以自我为中心的全身运动捕捉需要同时标注身体和手部的精确3D关节位置，而真实场景下获取此类标注极其困难。现有数据集要么仅包含身体关节，要么手部标注稀疏，难以支撑全身模型的充分训练。

面对上述瓶颈，本文的核心动机在于：**能否将鱼眼畸变校正嵌入到特征提取网络内部，而非作为预处理步骤？能否利用运动时序先验来填补遮挡区域的推理空白？** 这促使作者提出了两个关键设计——FisheyeViT和不确定性引导的扩散运动精炼——分别从单帧特征质量和时序运动合理性两个维度突破现有方法的性能上限。

## 核心创新

本工作针对单视角头戴鱼眼相机全身运动捕捉，提出了三项关键创新，分别对应特征提取、姿态回归表示和时序精炼三个核心环节。

### 创新一：FisheyeViT — 鱼眼畸变感知的特征提取

鱼眼镜头引入的严重畸变是传统视觉主干网络（如标准ViT或CNN）失效的根本原因。现有方案通常先对整个图像进行畸变校正再提取特征，但全局校正会引入插值伪影并破坏原始像素对应关系。FisheyeViT的核心思路是将畸变校正嵌入Vision Transformer的令牌化过程：通过球面投影在鱼眼图像上提取一系列等FOV（视场角）的未畸变小块，每个小块作为ViT的一个令牌输入。

具体而言，对于每个预设的切平面中心$\mathbf{P}_{ij}^{c}$，通过计算交点$\mathbf{P}_{ij}^{x}$确定切平面上的局部坐标系（公式1），然后在切平面上以$l \times l$正方形内生成$M \times M$的规则网格点（公式2），最后通过逆投影得到鱼眼图像上的采样坐标。由于给定固定鱼眼相机模型后，所有采样坐标$\mathbf{C}_{ij}^{mn}$均可预计算，训练和推理速度不受影响。

这一设计的因果机制在于：每个图像小块对应相同的FOV范围，使得ViT的注意力机制可以在语义一致、无畸变的局部区域上进行计算，从而有效缓解了鱼眼畸变对特征提取的干扰。消融实验证实，将FisheyeViT替换为普通ViT后，MPJPE从64.19 mm上升至67.36 mm（Table 3），验证了该模块的有效性。

### 创新二：像素对齐的3D热图回归 — uvd空间中的姿态表示

传统3D姿态回归通常采用两种范式：MLP直接回归xyz坐标，或通过V2V（volume-to-volume）在xyz空间中预测3D热图。前者缺乏空间对齐性，后者计算量大且与鱼眼投影无直接对应关系。

本工作提出在uvd空间（图像uv坐标+深度d）中回归像素对齐的3D热图。其核心洞察是：热图的voxel与2D特征图的像素直接对应，使得预测的关节uv坐标可以无缝衔接到鱼眼相机的重投影函数$\mathcal{P}^{-1}$，从而恢复准确的xyz坐标。这种表示同时保留了像素级空间对齐性和鱼眼投影的几何一致性。

该方法的关键优势在于：1）利用soft-argmax从热图中提取关节位置，同时获得热图最大值作为置信度，直接导出关节不确定性（公式9：$\mathbf{u} = 0.05 \times (1 - \mathbf{HM})$）；2）不确定性信息为后续扩散精炼提供了关键的引导信号。消融实验显示，用MLP直接回归替换该热图表示后，MPJPE剧增至130.7 mm（Supplementary Section 16），证明像素对齐的uvd热图对准确度至关重要。

### 创新三：不确定性引导的全身运动扩散精炼

单帧预测存在时序不一致性和遮挡区域的估计偏差。本工作引入基于扩散模型的运动先验，通过对全身运动序列进行时序精炼来纠正这些问题。核心创新在于将关节不确定性显式嵌入扩散采样过程。

去噪网络采用EDGE的Transformer框架，训练目标为预测原始信号$\mathbf{x}_0$（公式4）。在采样阶段，通过不确定性引导的采样步骤（公式5）混合预测运动$\hat{\mathbf{x}}_0$和初始估计运动$\mathbf{x}_e$：
$$\mathbf{x}_{t-1} \sim \mathcal{N}(\hat{\mathbf{x}}_0 + \mathbf{w}(\mathbf{x}_e - \hat{\mathbf{x}}_0), \boldsymbol{\Sigma}_t)$$

其中权重$\mathbf{w}$依赖于扩散步$t$和关节不确定性$\mathbf{u}$（公式6）：
$$\mathbf{w} = 1 / \left(1 + e^{-k(t - T \mathbf{u})}\right)$$

该函数的设计机制是：高不确定性关节（如被遮挡的脚部）在扩散早期就趋近初始估计，利用运动先验进行合理生成；低不确定性关节（如清晰可见的躯干）则在扩散后期才受初始估计影响，保留单帧预测的高精度。移除不确定性引导后，精炼方法MPJPE从57.59 mm升至62.16 mm（Table 3），证实了关节不确定性对运动先验引导的关键作用。此外，仅训练身体运动先验（不含手部）会导致手部MPJPE退化，说明全身运动先验能够捕获身体与手部的运动关联。

### 方法谱系与知识库定位

本工作在以下三个维度上推进了以自我为中心的运动捕捉前沿：

- **特征提取**：相比**EgoPW**和**SceneEgo**等使用标准CNN/ViT处理畸变图像的方法，FisheyeViT首次将鱼眼畸变校正嵌入ViT令牌化过程，实现了畸变感知的特征学习。
- **姿态回归**：不同于**EgoHMR**的MLP直接回归或**Mo²Cap²**的xyz空间热图，uvd空间像素对齐热图建立了图像像素与3D关节的直接几何对应，同时天然输出不确定性估计。
- **时序精炼**：相比**Ego-STAN**的时序编码或**EgoHMR**的扩散姿态估计，本工作首次将关节不确定性显式引入扩散采样，实现了选择性精炼——保留高置信预测、生成遮挡区域合理运动。

## 整体框架

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/001_Figure_1.jpg]]
*Figure 1: From an image sequence captured by a single head-mounted fisheye camera, our method can predict accurate and temporally coherent whole-body motion, including human body and hand poses. The SMPL-X parameters are obtained using inverse kinematics*

本文提出一种从单视角头戴鱼眼相机捕获全身运动的端到端流水线，其核心设计围绕三个瓶颈展开：鱼眼畸变、自遮挡导致的部位不可见、以及单帧估计的时序不一致性。流水线由两个阶段串联而成——**单帧全身姿态估计**与**基于扩散模型的时序运动精炼**——整体结构如 Figure 2 所示。

### 单帧估计阶段

输入为一帧头戴鱼眼相机图像。首先由 **FisheyeViT** 提取畸变感知的图像特征令牌：该模块不直接对整幅畸变图像进行全局校正，而是通过球面投影在切平面上采样等视场角（FOV）的未畸变小块，将其作为 Vision Transformer 的令牌输入，从而在保留鱼眼光学几何的前提下实现 patch 级去畸变（Section 3.1.1）。这一设计使得特征提取与鱼眼投影模型深度耦合，避免了传统 CNN/ViT 在严重畸变区域的感受野失真。

FisheyeViT 输出的图像特征令牌随后进入**身体姿态回归器**。该回归器采用像素对齐的 3D 热图表示：通过 1D 卷积网络将 2D 特征图上采样为 uvd 空间中的 3D 热图，其中每个体素直接对应 2D 特征的像素位置。利用 soft-argmax 从热图中提取关节的 uvd 坐标，再通过鱼眼重投影函数 $\mathcal{P}^{-1}$ 恢复为相机坐标系下的 3D 身体关节 $\hat{\mathbf{J}}_b$（Section 3.1.2）。与传统的 xyz 空间直接回归相比，uvd 空间的热图表征天然对齐鱼眼成像模型，使得预测关节可无缝衔接到鱼眼重投影，避免了坐标空间转换引入的精度损失。同时，热图的最大值被用于计算每个关节的不确定性 $\mathbf{u}$，供后续扩散精炼使用。

手部姿态估计与身体姿态并行进行：从输入图像中检测手部区域后，独立回归左右手的 3D 关节 $\hat{\mathbf{J}}_{lh}$、$\hat{\mathbf{J}}_{rh}$，再变换到身体坐标系下与身体关节合并，形成完整的全身关节 $\hat{\mathbf{J}}$（Section 3.1.3）。

### 时序精炼阶段

单帧估计虽精度较高，但存在时序抖动和遮挡区域的预测错误。为此，第二阶段引入**不确定性感知的扩散运动精炼**。该模块基于 EDGE 的 Transformer 去噪网络，在全身运动序列上训练一个无条件扩散模型，学习人体运动的时序先验（Section 3.2.1）。精炼采样时，在每一去噪步中，根据关节不确定性权重 $\mathbf{w}$ 混合扩散模型预测的运动 $\hat{\mathbf{x}}_0$ 与单帧估计的运动 $\mathbf{x}_e$：

$$\mathbf{x}_{t-1} \sim \mathcal{N}(\hat{\mathbf{x}}_0 + \mathbf{w}(\mathbf{x}_e - \hat{\mathbf{x}}_0), \boldsymbol{\Sigma}_t)$$

权重函数 $\mathbf{w} = 1 / (1 + e^{-k(t - T\mathbf{u})})$ 使得高不确定性关节（如被遮挡的脚部）在扩散早期就趋近单帧估计值，而低不确定性关节则主要依赖扩散先验进行平滑（Section 3.2.2）。这一机制在保留高置信关节精度的同时，利用全身运动先验生成遮挡区域的合理运动，显著提升时序一致性和整体精度。

### 输入输出与模块关系总结

- **输入**：单视角头戴鱼眼相机图像序列。
- **输出**：时序一致的全身 3D 关节位置（身体 + 左右手），可进一步通过逆运动学拟合 SMPL-X 参数。
- **模块串联**：FisheyeViT → 身体姿态回归器 + 手部姿态估计 → 身体-手部合并 → 不确定性感知扩散精炼。
- **关键数据流**：图像 → 去畸变特征令牌 → uvd 热图 → 3D 关节 + 不确定性 → 精炼后的全身运动序列。

## 核心模块与公式推导

### 3.1 FisheyeViT：鱼眼畸变感知的特征提取

FisheyeViT 的核心思想是**不对整幅鱼眼图像进行全局畸变校正，而是将其划分为若干等视场角（FOV）的未畸变小块，作为 Vision Transformer 的输入令牌**。这一设计使网络能够直接在原始鱼眼图像上提取特征，同时避免全局校正带来的插值误差和计算冗余。

具体而言，FisheyeViT 采用**球面投影（gnomonic projection）** 在小块级别进行畸变校正。对于每个小块中心 $\mathbf{P}_{ij}^{c}$，首先构建其切平面，并确定平面上的坐标轴方向。x 轴方向 $\mathbf{v}_{ij}^{x}$ 通过计算从原点出发、经过右移图像点的向量与切平面的交点获得：

$$
\mathbf{P}_{ij}^{x} = \frac{\langle \mathbf{P}_{ij}^{c}, \mathbf{v}_{ij}^{c} \rangle}{\langle \mathbf{v}_{ij}^{u}, \mathbf{v}_{ij}^{c} \rangle} \mathbf{v}_{ij}^{u} = \frac{1}{\langle \mathbf{v}_{ij}^{u}, \mathbf{v}_{ij}^{c} \rangle} \mathbf{v}_{ij}^{u}
$$

其中 $\mathbf{v}_{ij}^{c}$ 为中心点方向向量，$\mathbf{v}_{ij}^{u}$ 为右移图像点的方向向量。随后，在切平面上以 $\mathbf{P}_{ij}^{c}$ 为中心、$l \times l$ 的正方形区域内生成 $M \times M$ 的规则网格采样点：

$$
\{ \mathbf{P}_{ij}^{mn} = \mathbf{P}_{ij}^{c} + (l \frac{m}{M} \mathbf{v}_{ij}^{x}, l \frac{n}{M} \mathbf{v}_{ij}^{y}) \}
$$

这些采样点通过逆投影映射回鱼眼图像坐标，提取像素值形成未畸变小块。关键工程优化在于：对于固定的鱼眼相机模型，所有采样坐标 $\mathbf{C}_{ij}^{mn}$ 可**预先计算并缓存**，显著加速训练和推理过程。

### 3.2 像素对齐的 3D 热图回归器

传统方法通常在 xyz 空间回归 3D 热图（如 V2V 网络），但与鱼眼图像的像素空间不对齐，导致精度损失。本方法创新性地在 **uvd 空间**回归像素对齐的 3D 热图——热图的每个体素直接对应 2D 特征图的像素位置，深度维度 d 则编码该像素处关节存在的概率。

3D 身体关节 $\hat{\mathbf{J}}_b = \{ (x_i, y_i, z_i) \mid i \in 0, 1, 2, ..., J \}$ 通过鱼眼重投影函数从 uvd 坐标恢复：

$$(x_i, y_i, z_i) = \mathcal{P}^{-1}(u_i, v_i, d_i)$$

其中 $\mathcal{P}^{-1}$ 为鱼眼相机的逆投影函数，$(u_i, v_i)$ 由 soft-argmax 在热图的 uv 平面上定位，$d_i$ 由深度维度的 soft-argmax 确定。这一设计使预测关节与鱼眼投影几何无缝衔接，避免了坐标系转换带来的累积误差。

### 3.3 不确定性感知的扩散运动精炼

单帧估计存在时序不一致和遮挡区域的精度退化问题。为此，引入基于扩散模型的全身运动先验进行序列级精炼。

**正向扩散过程**定义为一个马尔可夫链，逐步向原始运动序列 $\mathbf{x}_0$ 添加高斯噪声：

$$q(\mathbf{x}_t|\mathbf{x}_{t-1}) = \mathcal{N}(\sqrt{\alpha_t} \mathbf{x}_{t-1}, (1-\alpha_t)I)$$

去噪网络 $D(\cdot)$ 采用 **EDGE** 的 Transformer 架构，训练目标为直接预测原始信号：

$$\mathcal{L}_{\mathrm{simple}} = E_{\mathbf{x}_0 \sim q(\mathbf{x}_0), t \sim [1,T]}\left[||\mathbf{x}_0 - D(\mathbf{x}_t, t)||_2^2\right]$$

**不确定性引导的采样**是精炼的核心机制。在去噪步骤 $t-1$，采样分布为：

$$\mathbf{x}_{t-1} \sim \mathcal{N}(\hat{\mathbf{x}}_0 + \mathbf{w}(\mathbf{x}_e - \hat{\mathbf{x}}_0), \boldsymbol{\Sigma}_t)$$

其中 $\hat{\mathbf{x}}_0$ 为去噪网络预测的运动，$\mathbf{x}_e$ 为单帧估计的运动，$\mathbf{w}$ 为关节级不确定性权重。权重函数设计为：

$$\mathbf{w} = 1 / \left(1 + e^{-k(t - T \mathbf{u})}\right)$$

其中 $k=0.1$，$T$ 为总扩散步数，$\mathbf{u}$ 为关节不确定性。**该函数的物理意义**：高不确定性关节（$\mathbf{u}$ 大）在扩散早期就趋近初始估计 $\mathbf{x}_e$，充分利用观测信息；低不确定性关节（$\mathbf{u}$ 小）则在后期才受其影响，更多依赖运动先验生成。不确定性值由归一化热图最大值计算：

$$\mathbf{u} = 0.05 \times (1 - \mathbf{HM})$$

缩放因子 0.05 用于限制扩散过程的随机影响幅度。

### 3.4 全身关节集成

身体关节 $\hat{\mathbf{J}}_b$、左手关节 $\hat{\mathbf{J}}_{lh}$ 和右手关节 $\hat{\mathbf{J}}_{rh}$ 分别估计后，合并为全身关节 $\hat{\mathbf{J}}$，作为扩散精炼模块的输入。手部姿态先通过手部检测器定位区域，再独立回归 3D 手部关节，最终变换到身体坐标系下完成集成。

## 实验与分析

### 主结果：身体姿态估计

在三个公开测试集上，本文方法在身体姿态估计任务中全面超越已有方法。Table 1 汇总了 SceneEgo、GlobalEgoMocap 和 Mo²Cap² 上的 MPJPE、PA-MPJPE 和 BA-MPJPE 指标。单帧版本 Ours-Single 在 SceneEgo 上达到 64.19 mm MPJPE，相比此前最优的 SceneEgo（118.5 mm）降低 45.7%，相对提升幅度显著。引入时序扩散精炼后，Ours-Refined 进一步将 MPJPE 压缩至 57.59 mm。在 GlobalEgoMocap 上，Ours-Refined 的 PA-MPJPE 为 65.83 mm，较 SceneEgo 的 76.50 mm 下降 10.67 mm；在 Mo²Cap² 上则为 72.63 mm，较 SceneEgo 的 79.65 mm 下降 7.02 mm。上述结果表明，FisheyeViT 与像素对齐 3D 热图的组合在单帧精度上已具压倒性优势，而扩散精炼在时序维度上进一步压缩了误差。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/007_Table_1.jpg]]
*Table 1: Egocentric human body pose accuracy of our method on three test datasets. Our method outperforms all previous state-ofthe-art methods. † denotes the temporal-based methods*

Figure 4 的定性对比直观展示了优势：在室内（左列）和室外（右列）场景中，Ours-Single 和 Ours-Refined 的绿色骨架与红色真值骨架高度重合，而 EgoPW 和 SceneEgo 在四肢末端及自遮挡区域出现明显偏离。这验证了 FisheyeViT 对鱼眼畸变的校正能力以及像素对齐热图对关节定位的精确性。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison on human body pose estimations between our methods and the state-of-the-art egocentric pose estimation methods on in-the-studio (left column) and in-the-wild scenes (right column). The red skeleton is the ground truth while the green skeleton is the predicted pose. Our methods predict more accurate body poses compared with EgoPW [49] and SceneEgo [50]*

### 主结果：手部姿态估计

手部姿态的定量结果见 Table 2。在 SceneEgo 测试集上，Ours-Single 的手部 MPJPE 已显著低于 Hand4Whole，Ours-Refined 进一步将 MPJPE 降至 19.37 mm，而 Hand4Whole 为 49.66 mm，降幅达 30.29 mm。Figure 5 的定性对比中，Hand4Whole 在手指关节处出现明显错位，本文方法则更贴近真值。值得注意的是，扩散精炼使用全身运动先验（包含身体与手部关节），消融实验证实仅训练身体先验会导致手部 MPJPE 退化，说明身体-手部运动关联被扩散模型有效捕获。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/009_Table_2.jpg]]
*Table 2: Egocentric hand pose accuracy of our method on SceneEgo test dataset. Our method outperforms the state-of-the-art Hand4Whole method [32]. Table 3. Ablation Study on SceneEgo test dataset [50]. † denotes the temporal-based method*

### 消融实验

Table 3 在 SceneEgo 测试集上系统拆解了各组件的贡献。

**FisheyeViT 的必要性**：将 FisheyeViT 替换为普通 ViT（w/o FisheyeViT），MPJPE 从 64.19 mm 升至 67.36 mm，增幅约 3.2 mm。这表明在鱼眼图像上直接应用标准 ViT 会因畸变导致特征提取质量下降，FisheyeViT 的等 FOV 分块去畸变策略有效缓解了这一问题。

**像素对齐 3D 热图的关键作用**：使用基于 MLP 的直接回归替换像素对齐 3D 热图后，MPJPE 剧增至 130.7 mm（补充材料 Section 16），精度几乎崩溃。这揭示了在 uvd 空间中回归热图并通过鱼眼重投影恢复 xyz 坐标的设计是准确度的核心保障——该表示使预测与像素空间严格对齐，避免了直接回归 xyz 时因畸变非线性导致的严重误差。

**EgoWholeBody 数据集的贡献**：移除该合成数据集（w/o EgoWholeBody），仅用 EgoPW 等真实数据训练，MPJPE 升至 75.10 mm，劣化约 10.9 mm。该数据集包含超 87 万帧（70 万帧 Renderpeople + 17 万帧 SMPL-X），覆盖多样人体形状与运动，为网络提供了关键的姿态先验和畸变-姿态映射知识。

**不确定性引导的有效性**：去除不确定性引导后（w/o uncert. guidance），精炼方法 MPJPE 从 57.59 mm 升至 62.16 mm，退化 4.57 mm。不确定性权重 w 由关节热图最大值推导（$ \mathbf{u} = 0.05 \times (1 - \mathbf{HM}) $），在扩散采样中控制估计运动与预测运动的混合比例：高不确定关节（如被遮挡的脚部）在早期扩散步就趋近初始估计 $ \mathbf{x}_e $，低不确定关节则保留更多扩散先验生成的运动。去除该机制后，扩散模型对所有关节施加均等修正，反而损害了高置信关节的精度。

### 与全景图像处理方法的对比

Table 7（原文标注为 Table 8）将 FisheyeViT 与 SphereNet、Panoformer 等全景图像处理网络进行了对比。FisheyeViT 在鱼眼姿态估计任务上表现更优，原因在于其分块去畸变策略专为鱼眼相机的大畸变特性设计，而全景网络假设等距或柱面投影，无法直接适配鱼眼镜头的非线性畸变模型。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/015_Table_7.jpg]]
*Table 7: Comparison with Spherenet and Panoformer*

### 失败模式与局限性

尽管整体精度领先，方法仍存在以下可辨识的失败模式：

1. **严重自遮挡下的物理不合理性**：当手脚被身体完全遮挡时，扩散模型生成的姿态可能出现穿模或违反运动学约束。这是因为扩散先验仅从运动数据中学习统计规律，缺乏物理模拟器的硬约束。
2. **域差导致的泛化衰退**：EgoWholeBody 为合成数据集，真实场景中光照、衣物纹理、背景复杂度与合成域存在差异。在极端野外场景下，单帧估计的置信度可能下降，进而影响不确定性估计和精炼效果。
3. **扩散精炼的计算开销**：扩散采样需多步迭代，增加了推理延迟，限制了在实时 VR/AR 场景中的直接部署。
4. **相机内参依赖**：FisheyeViT 的采样坐标 $ \mathbf{C}_{ij}^{mn} $ 需基于预校准的鱼眼相机模型预计算，无法处理未知或动态变化的相机内参。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|---------|
| Table 1 | 单帧方法在三个测试集上全面超越现有方法，扩散精炼进一步压缩误差 6–10 mm |
| Table 2 | 手部 MPJPE 从 49.66 mm 降至 19.37 mm，全身先验捕获身体-手部关联 |
| Table 3 | FisheyeViT（+3.2 mm）、像素对齐热图（+66.5 mm）、EgoWholeBody（+10.9 mm）、不确定性引导（+4.6 mm）各自贡献显著 |
| Figure 4 | 定性展示身体姿态在室内外场景中均更贴合真值，尤其在四肢末端 |
| Figure 5 | 手部姿态定性对比，手指关节定位明显优于 Hand4Whole |

**证据强度说明**：主结果和消融实验均基于公开测试集的标准指标，且所有对比方法使用相同训练数据重新训练（Table 1 中 * 标记），公平性得到控制。补充材料中 MLP 替代热图的 130.7 mm 结果置信度略低（0.9），因该实验仅在补充材料中报告，但量级差异足以支撑结论。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/006_Figure.jpg]]

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/016_Figure_8.jpg]]
*Figure 8: The setup of the egocentric fisheye camera and one example of the egocentric image*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/019_Figure.jpg]]

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/020_Figure.jpg]]

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/021_Figure.jpg]]

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/008_Table.jpg]]

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2311_16495/figures/011_Table_4.jpg]]
*Table 4: Comparison between different training datasets for egocentric body pose estimation*

## 方法谱系与知识库定位

### 与现有基线方法的关系

本文提出的以自我为中心全身运动捕捉方法，在三个层面与现有工作形成显著差异：

**特征提取层面**：现有以自我为中心姿态估计方法普遍采用标准ViT或CNN直接处理畸变鱼眼图像，例如 **EgoPW**、**SceneEgo**、**EgoHMR** 等基线均未对鱼眼畸变进行显式建模。本文提出的FisheyeViT将球面投影嵌入Vision Transformer框架，将鱼眼图像划分为等FOV的未畸变小块作为令牌输入，从根本上改变了畸变图像的特征提取范式。消融实验中，将FisheyeViT替换为普通ViT导致MPJPE从64.19 mm上升至67.36 mm，证实了该模块对缓解鱼眼畸变的实际贡献。

**姿态回归层面**：主流方法如 **EgoPW** 采用MLP直接回归xyz关节坐标，或使用V2V在xyz空间进行体素预测。本文提出在图像uvd空间回归像素对齐的3D热图，通过soft-argmax和鱼眼重投影函数恢复3D关节位置。这一设计使得每个体素直接对应2D特征图中的像素，实现了像素级对齐。消融实验表明，用MLP直接回归替换该热图表示后，MPJPE剧增至130.7 mm，说明该表示对准确度的关键作用。

**时序精炼层面**：现有单帧方法（如 **SceneEgo**、**EgoHMR**）缺乏时序先验，预测结果存在时间不稳定性。时序方法如 **Ego-STAN** 虽引入了时序建模，但未利用运动先验进行全局优化。本文基于 **EDGE** 的Transformer去噪架构，构建了不确定性引导的全身运动扩散先验。与标准扩散采样不同，本文利用从3D热图提取的关节不确定性值，在采样过程中选择性混合预测运动与初始估计运动——高不确定关节（如被遮挡的脚部）在扩散早期即受初始估计引导，低不确定关节则保持扩散模型的生成自由度。移除不确定性引导后，精炼方法MPJPE从57.59 mm上升至62.16 mm，验证了该机制对运动先验引导的重要性。

**手部姿态层面**：与 **Hand4Whole** 等第三方视角手部估计方法相比，本文方法在SceneEgo测试集上将手部MPJPE从49.66 mm降至19.37 mm（精炼后），降幅达61%。全身运动扩散先验能捕获身体与手部运动的关联，仅训练身体运动先验（不含手部）会导致手部MPJPE退化，进一步证实了全身联合建模的必要性。

### 适用边界

**相机条件**：方法依赖预校准的鱼眼相机模型，采样坐标 $C_{ij}^{mn}$ 需基于固定相机参数预计算。对于未知或变化的相机内参，方法无法直接适用，需补充在线标定模块。

**数据依赖**：方法依赖大规模合成数据集EgoWholeBody（超过87万帧）进行训练。该数据集使用Renderpeople模型和SMPL-X模型渲染，虽覆盖多种人体形状和运动，但合成数据与真实场景之间的域差可能影响泛化能力。消融实验显示，移除EgoWholeBody后MPJPE从64.19 mm升至75.10 mm，表明当前方法对合成数据的强依赖。

**遮挡处理**：扩散精炼能在一定程度上生成遮挡区域的合理运动，但在严重自遮挡情况下（如俯身时手部完全被躯干遮挡），生成的姿态可能不符合物理约束，出现穿模或力学不合理现象。方法未引入物理模拟器或接触约束来保证生成结果的物理合理性。

**实时性**：扩散精炼增加了推理耗时，当前设计难以满足实时VR/AR应用需求。单帧方法虽可实时运行，但精度和时序一致性不及精炼后结果。

**面部捕捉**：当前方法仅覆盖身体和手部姿态，未包含面部表情捕捉，因此输出的SMPL-X参数不完整，无法实现真正完整的全身动捕。

### 局限与开放问题

**方法内在局限**：

1. **物理不合理性**：扩散模型生成的遮挡区域运动缺乏物理约束，可能出现穿模、关节超限旋转等问题。未来可探索将物理模拟器嵌入扩散采样过程，或引入接触约束损失进行引导。

2. **计算开销**：扩散精炼的迭代采样过程显著增加了推理时间。如何通过蒸馏、步数缩减或高效采样策略降低耗时，是走向实时应用的关键瓶颈。

3. **相机标定依赖**：FisheyeViT的采样坐标预计算依赖已知相机模型，限制了其在非标定场景的部署。自标定或无标定鱼眼姿态估计是值得探索的方向。

**领域开放问题**：

1. **FisheyeViT架构泛化**：当前FisheyeViT专为姿态估计设计，其等FOV分块策略是否可扩展到其他鱼眼视觉任务（如深度估计、语义分割、SLAM）？这需要验证该特征表示在不同下游任务中的迁移能力。

2. **完整SMPL-X估计**：如何在现有身体+手部框架中融入面部表情捕捉，实现完整的SMPL-X参数估计？面部区域在以自我为中心视角中通常不可见或严重畸变，需要新的传感器布局或跨模态融合策略。

3. **减少合成数据依赖**：能否通过无监督域适应、自监督预训练或神经渲染技术，降低对大规模合成数据的依赖，使模型能在少量真实标注或纯真实数据下有效训练？

4. **物理感知扩散模型**：如何将物理模拟器或运动学约束嵌入扩散去噪过程，从根本上解决自遮挡导致的物理不合理性？这需要设计可微的物理约束项并融入采样引导。

5. **多任务联合优化**：FisheyeViT提取的特征是否可同时服务于姿态估计、场景理解和动作识别？多任务联合训练可能提升特征表示的鲁棒性，同时降低整体系统开销。

## 原文 PDF

![[paperPDFs/CVPR_2024/Egocentric_Whole_Body_Motion_Capture_with_FisheyeViT_and_Diffusion_Based_Motion_Refinement.pdf]]
