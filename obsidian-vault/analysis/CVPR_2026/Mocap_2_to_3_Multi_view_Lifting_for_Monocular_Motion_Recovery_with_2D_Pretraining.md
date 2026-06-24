---
title: "Mocap-2-to-3: Multi-view Lifting for Monocular Motion Recovery with 2D Pretraining"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Mocap_2_to_3_Multi_view_Lifting_for_Monocular_Motion_Recovery_with_2D_Pretraining.pdf
project_link: "https://wangzhumei.github.io/mocap-2-to-3/"
code_link: null
aliases:
- M23
- Mocap-2-to-3
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将3D运动恢复重新定义为多视角合成过程，利用大规模2D数据预训练获得强运动先验，再通过3D数据微调实现视角一致性生成；通过解耦局部姿态与全局运动并引入地面平面约束编码，加快收敛并提升绝对位姿精度。
primary_logic: 利用两阶段多视角扩散模型（2D预训练+多视角微调）结合解耦运动表示和地面几何先验，使单目输入能够提升为具有度量尺度的全局一致3D运动，克服了单目升维中的尺度和泛化瓶颈。
claims:
- 在RICH数据集上，我们的方法在没有对齐的世界坐标下W-MPJPE为82.6 mm，显著优于GVHMR+SMPLify的109.4 mm（降低26.8 mm）。
- 消融实验表明解耦局部姿态与全局运动可使PA-MPJPE从65.1 mm降至45.8 mm（无点图），验证了分离表示对动作质量和轨迹估计的关键作用。
- 点图编码使训练所需epoch减少超过50%，在相同训练量下PA-MPJPE从33.4 mm（无点图，8k epoch）降至30.5 mm（有点图，3.5k epoch），证实了显式地面约束对收敛的加速效果。
- RICH 上 PA-MPJPE (mm) = 26.2
---

# Mocap-2-to-3: Multi-view Lifting for Monocular Motion Recovery with 2D Pretraining

> [!tip] 核心洞察
> 利用两阶段多视角扩散模型（2D预训练+多视角微调）结合解耦运动表示和地面几何先验，使单目输入能够提升为具有度量尺度的全局一致3D运动，克服了单目升维中的尺度和泛化瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | Mocap-2-to-3: 基于2D预训练的多视角提升单目运动恢复 |
| 英文题名 | Mocap-2-to-3: Multi-view Lifting for Monocular Motion Recovery with 2D Pretraining |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2503.03222) · [Project](https://wangzhumei.github.io/mocap-2-to-3/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Mocap-2-to-3 |
| Dataset | RICH |

> [!tip] 效果简介
> - RICH 上，PA-MPJPE (mm) 26.2 vs 30.7 (-4.5)；W-MPJPE (mm) 82.6 vs 109.4 (-26.8)；Abs-MPJPE (mm) 156.8 vs 430.4 (-273.6)。

## 概述

单目3D人体运动恢复长期受困于两个瓶颈：**3D标注数据的稀缺与场景受限**，导致模型对分布外（OOD）动作的泛化能力不足；以及**单目深度模糊性**，使得估计具有度量尺度的绝对位姿极为困难。现有方法要么仅在根对齐的局部坐标系下评估动作质量，要么在世界坐标系下只能恢复对齐后的全局轨迹，缺乏真正的度量尺度绝对定位能力（如**GVHMR** (Shen et al., SIGGRAPH Asia 2024)、**WHAM** (Shin et al., CVPR 2024) 等）。

本文提出 **Mocap-2-to-3**，一个将单目3D运动恢复**重新定义为多视角合成过程**的框架。其核心洞察是：利用大规模可获取的2D姿态数据进行预训练以习得强运动先验，再在有限3D数据上微调实现视角一致性生成，从而将单目2D输入“提升”为具有度量尺度的全局一致3D运动。方法的关键创新在于三点：

1. **两阶段多视角扩散范式**：先在大量2D数据上预训练任意视角的2D运动扩散模型，再以该权重初始化多视角扩散模型，在3D数据上微调以生成多个虚拟视角的2D姿态，最后通过多视角三角化重建世界坐标系下的3D绝对位姿。
2. **解耦运动表示**：将2D运动分解为局部姿态（根关节中心归一化至[-1,1]）与全局移动（根轨迹+边界框尺度），独立优化后再合并，克服了直接预测全局坐标时位置误差主导损失导致的运动细节退化。
3. **显式地面几何约束**：从相机参数计算地面平面方程并编码为点图（pointmap），通过ResNet-18和交叉注意力层注入扩散模型，提供空间先验以加速收敛并提升绝对位姿精度。

**主要结果**：在RICH数据集上，Mocap-2-to-3在无任何对齐的世界坐标系下W-MPJPE达到82.6 mm，显著优于GVHMR+SMPLify的109.4 mm（降低26.8 mm）；绝对位姿误差Abs-MPJPE从430.4 mm降至156.8 mm。消融实验证实，解耦表示使PA-MPJPE从65.1 mm降至45.8 mm，点图编码使训练所需epoch减少超过50%的同时PA-MPJPE进一步降低2.9 mm。该方法同时支持SMPL和COCO格式输出，展现了良好的格式泛化能力。

**方法定位**：Mocap-2-to-3区别于直接端到端回归（如Ray3D）和仅用2D数据的提升方法（如MVLift），通过“2D预训练+多视角微调”的范式，在仅需单目2D姿态和标定相机参数的条件下，首次实现了具有度量尺度的绝对位姿恢复，同时保持了OOD泛化能力。

## 背景与动机

### 单目3D人体运动恢复的核心瓶颈

从单目视频中恢复具有度量尺度的全局3D人体运动是计算机视觉与图形学中的长期挑战。该任务的核心瓶颈体现在两个层面。其一，**3D训练数据的稀缺与分布受限**：获取带精确3D标注的人体运动数据依赖昂贵的光学动捕系统或IMU设备，导致现有3D数据集在场景多样性、动作类型和相机视角等方面远不及大规模2D姿态数据丰富。这使得直接由单目图像或2D姿态回归3D运动的模型在分布外（OOD）场景下泛化能力显著退化。其二，**单目升维固有的深度模糊性**：从单一视角的2D观测中估计尺度精确的绝对位姿是一个病态问题，缺乏多视角约束或场景几何先验时，模型难以区分由深度变化和由人体尺度变化引起的投影差异。

### 现有方法的局限

当前主流方法可大致分为三类，各自存在结构性缺陷。

**端到端回归方法**（如 **WHAM** (Shin et al., CVPR 2024)、**GVHMR** (Shen et al., SIGGRAPH Asia 2024)）直接从单目图像或2D姿态序列预测3D运动参数。这类方法受限于3D监督数据的规模，在训练分布之外的场景中容易产生不自然的姿态和轨迹漂移。其中GVHMR仅能恢复经初始帧对齐后的世界坐标系轨迹，无法提供度量尺度的绝对定位。

**基于优化的拟合方法**（如 **SMPLify** (Bogo et al., ECCV 2016)）通过迭代优化将参数化人体模型拟合到2D观测，虽不依赖大规模3D训练数据，但优化过程计算代价高、易陷入局部极小，且缺乏时序一致性约束，难以处理快速运动和严重遮挡。

**利用场景几何约束的方法**（如 **Ray3D** (Zhan et al., CVPR 2022)）通过已知的相机参数和地面平面方程提供额外几何先验以缓解深度模糊。然而，这类方法通常需要场景扫描或标定信息作为输入，且未充分利用2D数据中的运动先验来提升动作质量。

近期，**MVLift** (Li et al., CVPR 2025) 尝试仅用2D数据通过扩散模型将单目2D姿态提升至3D全局运动，开创了数据驱动的新范式。但其运动质量仍落后于3D监督方法，说明纯粹的2D训练难以弥补3D几何理解的缺失。

### 本文动机与核心思路

上述分析揭示了一个关键矛盾：**2D数据蕴含丰富的运动先验，但缺乏3D几何约束；3D数据提供精确的几何监督，但规模有限且分布狭窄**。本文的核心动机在于打破这一僵局——能否设计一种框架，既充分利用大规模2D数据学习强运动先验，又通过有限的3D数据注入多视角几何一致性，从而实现从单目2D输入到度量尺度全局3D运动的高质量提升？

为此，本文提出 **Mocap-2-to-3**，将单目3D运动恢复重新定义为**多视角合成过程**：给定主视角的2D姿态序列和相机参数，生成其他虚拟视角的2D姿态，再通过多视角三角化重建世界坐标系下的3D绝对位姿。这一范式的关键优势在于：(1) 2D姿态生成可以在大规模2D数据上预训练，习得覆盖广泛动作和视角的运动先验；(2) 多视角生成在有限3D数据上微调时，显式地引入了视角间几何一致性约束；(3) 三角化步骤将深度模糊问题转化为多视角几何求解，天然具备度量尺度恢复能力。

如图1所示，与传统直接回归框架相比，Mocap-2-to-3通过“2D预训练+多视角微调”的两阶段策略，实现了泛化能力与几何精度的统一。表1系统对比了本文方法与相关工作在输入模态、相机参数需求、2D数据利用方式和度量尺度轨迹恢复能力上的差异，凸显了本框架在仅需单目2D姿态和标定相机参数的条件下，即可输出具有绝对尺度的全局3D运动。

## 核心创新

Mocap-2-to-3 的核心创新在于将单目3D人体运动恢复重新定义为**多视角合成问题**，并通过三个关键设计突破传统方法的瓶颈。

### 1. 两阶段多视角扩散训练范式

传统方法直接由单目图像或2D姿态端到端回归3D运动，受限于稀缺且场景受限的3D训练数据，分布外泛化能力差。Mocap-2-to-3 提出**两阶段训练策略**（Figure 2）：

- **第一阶段**：在大量2D姿态数据上预训练**单视角2D运动扩散模型**，学习任意相机视角下的2D运动生成先验。这使模型从海量2D数据中获取强运动先验，摆脱对昂贵3D标注的依赖。
- **第二阶段**：以预训练权重初始化**多视角扩散模型**，在有限3D数据上微调，以主视角2D姿态序列和相机参数为条件，生成其他虚拟视角的2D姿态。引入 **View Attention 层**显式学习视角间关联，强制几何一致性。

这一范式使单目输入能够“提升”为多视角观察，进而通过三角化重建度量尺度的3D绝对位姿，从根本上克服了单目升维中的尺度模糊性和泛化瓶颈。

### 2. 解耦局部姿态与全局运动

直接预测投影后的全局坐标会导致位置误差主导损失，使运动细节退化（Figure 3b）。Mocap-2-to-3 提出**解耦运动表示**（Figure 3c），将2D运动分解为：

- **局部姿态** $\mathcal{M}_{v}^{l}$：以根关节为中心归一化至 $[-1, 1]$ 的关节点坐标，专注刻画动作细节；
- **全局移动** $(s_v, \tau_v)$：根轨迹 $\tau_v$ 和边界框尺度 $s_v$，描述人体在画面中的整体位移。

推理时通过缩放和平移恢复各视角的全局2D坐标：
$$\mathcal{M}_{v,\{1:J\}}^{g} = \mathcal{M}_{v}^{l} \cdot s_{v} + \tau_{v}, \quad \mathcal{M}_{v}^{g} = [\tau_{v}, \mathcal{M}_{v,\{1:J\}}^{g}]$$

消融实验证实该设计的决定性作用：去除解耦后，PA-MPJPE 从 45.8 mm 升至 65.1 mm（+29.3 mm），验证了分离表示对动作质量和轨迹估计的关键贡献（Table 4）。

### 3. 点图编码的显式地面几何约束

传统方法仅提供相机位姿嵌入，缺乏显式场景几何约束。Mocap-2-to-3 从已知相机参数计算地面平面方程，编码为**点图** $\mathcal{P} \in \mathbb{R}^{W \times H \times 3}$——图像中每个像素 $(u,v)$ 到世界坐标系地面点 $(x_w, y_w, z_w)$ 的映射（Figure 4），提供明确的空间先验。点图通过 ResNet-18 编码器压缩为特征图，经交叉注意力层注入多视角扩散模型。

点图编码带来显著的**收敛加速**效果：在相同训练量下，PA-MPJPE 从 33.4 mm（无点图，8k epoch）降至 30.5 mm（有点图，仅 3.5k epoch），训练所需 epoch 减少超过 50%（Table 4）。这表明显式地面约束为模型提供了有效的空间锚定，大幅降低了优化难度。

### 与代表性方法的差异化对比

Table 1 系统对比了 Mocap-2-to-3 与相关方法的本质差异。**GVHMR**（Shen et al., SIGGRAPH Asia 2024）在世界坐标系下仅恢复对齐后的全局轨迹，缺乏度量尺度绝对定位；**WHAM**（Shin et al., CVPR 2024）虽支持世界坐标系运动恢复，但精度受限于单目深度估计的固有模糊性；**MVLift**（Li et al., CVPR 2025）同样采用2D数据提升至3D，但运动质量落后于3D监督方法。Mocap-2-to-3 是唯一同时具备以下能力的方法：从单目2D输入恢复度量尺度轨迹、利用2D数据增强3D结果、输出SMPL格式的全局运动参数。

## 整体框架

Mocap-2-to-3 将单目3D人体运动恢复重新定义为**多视角合成问题**，其核心思想是：利用大规模2D姿态数据预训练获得强运动先验，再通过有限3D数据微调实现视角一致性生成，从而将单目2D姿态序列“提升”为具有度量尺度的全局一致3D运动。

### 两阶段训练范式

整个框架采用**两阶段训练**策略，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l1070_https_arxiv_org_abs_2503_03222/figures/003_Figure_2.jpg]]
*Figure 2: Pipeline overview. During training: (a) We first train an arbitrary single-view 2D Motion Diffusion Model. (b) Its weights are then used to initialize a Multi-view Diffusion Model, conditioned on 2D pose sequences from V0 and pointmaps. During inference, the Multi-view Model generates motions for other views. (c) We compute local poses and global movement to recover global coordinates for each view. (d) Multi-view triangulation is then used to synthesize 3D absolute poses, (e) resulting in full-body global human motion*

**第一阶段：单视角2D运动扩散模型预训练。** 在大量2D姿态数据上训练一个无条件扩散模型 $D_{2D}$，使其学会在任意相机视角下生成合理的2D人体运动序列 $\mathcal{M} \in \mathbb{R}^{T \times J \times 2}$（$T$ 帧、$J$ 个关键点）。此阶段不依赖3D标注，仅利用易获取的2D运动捕捉或检测数据建立人体运动先验。

**第二阶段：多视角扩散模型微调。** 以第一阶段预训练权重初始化多视角扩散模型 $D_{mv}$，在有限3D数据上进行微调。该模型以主视角（$V_0$）的2D姿态序列、多相机参数（内参 $\mathcal{K}$ 和外参 $\mathcal{RT}$）以及地面点图 $\mathcal{P}$ 作为条件输入，同时生成其他虚拟视角的2D姿态序列。通过引入 **View Attention 层**在多视角特征间传播信息，强制几何一致性。

### 推理流程

推理时，整个pipeline由五个核心模块串联完成从单目2D到全局3D的升维：

1. **多视角2D姿态生成**：将主视角2D姿态序列 $\mathcal{M}_0$、相机参数和点图输入多视角扩散模型 $D_{mv}$，经 $N$ 步去噪生成其余 $V-1$ 个虚拟视角的2D姿态序列。
2. **运动解耦**：将各视角的2D姿态分解为**局部姿态**（以根关节为中心归一化至 $[-1,1]$）和**全局移动**（根轨迹 $\tau_v$ + 边界框尺度 $s_v$），避免直接预测全局坐标时位置误差主导损失、导致运动细节退化的问题（如 Figure 3 所示）。
3. **全局坐标恢复**：通过缩放和平移将局部姿态恢复为各视角的全局2D坐标：
   $$\mathcal{M}_{v,\{1:J\}}^{g} = \mathcal{M}_{v}^{l} \cdot s_{v} + \tau_{v}, \quad \mathcal{M}_{v}^{g} = [\tau_{v}, \mathcal{M}_{v,\{1:J\}}^{g}]$$
4. **点图几何约束**：地面点图 $\mathcal{P} \in \mathbb{R}^{W \times H \times 3}$ 编码每个像素 $(u,v)$ 到世界坐标系地面点 $(x_w, y_w, z_w)$ 的映射，经 ResNet-18 压缩为特征图后通过交叉注意力层注入扩散模型，提供显式的地面平面先验（Figure 4）。
5. **多视角三角化**：利用多视角2D全局坐标和已知相机参数，通过三角化重建世界坐标系下的3D绝对位姿，输出 SMPL 格式的全局人体运动。

![[assets/figures/papers/paper_list_l1070_https_arxiv_org_abs_2503_03222/figures/004_Figure_3.jpg]]
*Figure 3: (a) 2D projection coordinates, (b) direct prediction results (failure case). (c) Our decoupled representation separating local pose and global movement*

### 输入输出与关键设计

- **输入**：单目2D姿态序列 + 标定相机参数 + 地面点图
- **输出**：具有度量尺度的世界坐标系3D绝对位姿（支持 SMPL 和 COCO 格式）
- **关键设计**：运动解耦表示分离了动作质量与轨迹精度两个优化目标，点图编码提供显式空间先验加速收敛（训练所需 epoch 减少超过 50%），View Attention 机制确保多视角生成的一致性。

> 注：本方法假设训练和推理时已知相机内参与外参，不适用于未标定的在野视频；且以2D姿态为输入，对上游2D检测器精度敏感。

### 补充图表

![[assets/figures/papers/paper_list_l1070_https_arxiv_org_abs_2503_03222/figures/001_Figure_1.jpg]]
*Figure 1: (a) Traditional framework for direct 3D motion regression. (b) Mocap-2-to-3: our multi-view lifting framework from monocular input which leverages 2D pretraining to enhance 3D motion capture. (c) The model outputs SMPL-format global motions with absolute position from monocular 2D pose input while maintaining out-of-distribution generalization capability. (d) Our model also supports outputs in the COCO-format keypoint*

## 核心模块与公式推导

### 3.1 两阶段多视角扩散框架

Mocap-2-to-3 将单目3D运动恢复重新定义为**多视角合成过程**，训练分为两个阶段（Fig. 2）：

- **第一阶段：单视角2D运动扩散模型预训练**。在大规模2D姿态数据上训练一个面向任意相机视角的2D运动生成器，学习强运动先验。输入为2D运动序列 $\mathcal{M} \in \mathbb{R}^{T \times J \times 2}$（$T$ 帧、$J$ 个关键点），模型学习在任意相机参数下的2D姿态分布。

- **第二阶段：多视角扩散模型微调**。以预训练权重初始化，接收主视角（$V_0$）的2D姿态序列 $\mathcal{M}_0 \in \mathbb{R}^{T \times J \times 2}$、相机参数（内参 $\mathcal{K} \in \mathbb{R}^{V \times 4}$ 和外参 $\mathcal{RT} \in \mathbb{R}^{V \times 3}$）以及点图 $\mathcal{P}$ 作为条件输入，生成其他虚拟视角的2D姿态。通过引入**View Attention层**在多视角特征间传播信息，强制几何一致性。

### 3.2 运动解耦表示

直接预测投影后的全局2D坐标会导致位置误差主导损失，使运动细节退化（Fig. 3b）。为此，提出将2D运动**解耦为局部姿态与全局移动**（Fig. 3c）：

- **局部姿态** $\mathcal{M}_v^l$：以根关节为中心归一化至 $[-1, 1]$ 区间，保留精细动作信息。
- **全局移动**：由根轨迹 $\tau_v$ 和边界框尺度 $s_v$ 组成，描述人体在图像平面内的整体位移和大小变化。

推理时通过缩放和平移恢复各视角的全局2D坐标：

$$\mathcal{M}_{v,\{1:J\}}^{g} = \mathcal{M}_{v}^{l} \cdot s_{v} + \tau_{v}, \quad \mathcal{M}_{v}^{g} = [\tau_{v}, \mathcal{M}_{v,\{1:J\}}^{g}]$$

其中 $\mathcal{M}_{v,\{1:J\}}^{g}$ 为除根关节外的全局坐标，$\mathcal{M}_{v}^{g}$ 为拼接根轨迹后的完整全局2D姿态序列。该解耦使局部动作优化与全局轨迹估计相互独立，消融实验证实去除解耦后 PA-MPJPE 从 45.8 mm 上升至 65.1 mm（Table 4）。

### 3.3 点图编码与地面几何约束

为提供显式的空间先验，从已知相机参数计算地面平面方程，编码为**点图** $\mathcal{P} \in \mathbb{R}^{W \times H \times 3}$——图像中每个像素 $(u, v)$ 到世界坐标系下地面点 $(x_w, y_w, z_w)$ 的映射（Fig. 4）。点图通过 **ResNet-18** 编码器压缩为特征图，再通过交叉注意力层注入多视角扩散模型，提供明确的地面几何约束。消融实验表明，点图编码使训练所需 epoch 减少超过 50%，在相同训练量下 PA-MPJPE 从 33.4 mm（无点图，8k epoch）降至 30.5 mm（有点图，3.5k epoch），证实了显式地面约束对收敛的加速效果（Table 4）。

![[assets/figures/papers/paper_list_l1070_https_arxiv_org_abs_2503_03222/figures/005_Figure_4.jpg]]
*Figure 4: (a) Pointmaps representing pixel-to-world coordinate*

### 3.4 多视角三角化与绝对位姿恢复

推理阶段，去噪过程共 $N$ 步。每步模型 $\mathcal{D}_{mv}$ 以 $[\epsilon, \mathcal{M}_0, \mathcal{K}, \mathcal{RT}, \mathcal{P}]$ 为输入，预测各视角的2D运动序列 $\mathcal{M}_v^n$。对每个去噪步，通过运动解耦模块从生成结果中分离局部姿态和全局移动，重新计算各视角的全局2D坐标。最终利用多视角2D全局坐标和已知相机参数，通过**多视角三角化**重建世界坐标系下的3D绝对位姿，得到具有度量尺度的全局一致人体运动（Fig. 2d-e）。

## 实验与分析

### 主实验结果

Mocap-2-to-3 在两个标准基准上进行了评估：RICH（室内多视角捕捉）和 AIST++（舞蹈动作数据集）。所有实验均假设已知相机内参和外参（通过校准获得），输入为单目 2D 姿态序列。

**RICH 数据集。** 如表 2 所示，Mocap-2-to-3 在三种评估协议下均显著优于现有方法：

- **相机坐标系根对齐（PA-MPJPE）：** 达到 26.2 mm，比 **GVHMR + SMPLify**（Shen et al., SIGGRAPH Asia 2024；Bogo et al., ECCV 2016）的 30.7 mm 降低 4.5 mm。这表明解耦运动表示有效保留了细粒度动作细节。
- **世界坐标系首帧对齐（W-MPJPE）：** 达到 82.6 mm，比 **GVHMR + SMPLify** 的 109.4 mm 降低 26.8 mm，验证了多视角提升框架对全局轨迹估计的显著改进。
- **世界坐标系无对齐（Abs-MPJPE）：** 达到 156.8 mm，而 **GVHMR + SMPLify** 为 430.4 mm，**Ray3D**（Zhan et al., CVPR 2022）为 395.1 mm。Mocap-2-to-3 的绝对定位误差仅为基线方法的约三分之一，证明其在不依赖额外设备的情况下实现了度量尺度的精确定位。

**AIST++ 数据集。** 如表 3 所示，Mocap-2-to-3 在 PA-MPJPE 上达到 60.1 mm，优于 **MVLift**（Li et al., CVPR 2025）和 **GVHMR + SMPLify**。值得注意的是，该方法在 COCO 格式骨架上的泛化表现同样稳健（见图 7），验证了 2D 预训练赋予的分布外泛化能力。

### 消融实验

表 4 系统消融了三个核心设计选择：

**1. 运动解耦的有效性。** 移除局部姿态与全局运动的解耦表示（即直接预测投影坐标），PA-MPJPE 从 45.8 mm 上升至 65.1 mm（上升 19.3 mm），W-MPJPE 从 82.6 mm 上升至 103.9 mm。这证实分离表示使模型能够独立优化动作质量和轨迹估计，避免了位置误差主导损失导致的运动细节退化。

**2. 点图编码的收敛加速。** 在相同训练量（3.5k epoch）下，引入点图编码使 PA-MPJPE 从 33.4 mm 降至 30.5 mm。更重要的是，无点图配置需要训练至 8k epoch 才能达到 33.4 mm，而有点图配置在 3.5k epoch 即达到更优性能——训练所需 epoch 减少超过 50%。这表明显式地面平面约束为模型提供了强空间先验，大幅加速收敛。

**3. 2D 预训练的数据域适配。** 在预训练阶段加入少量与测试域同分布的 2D 数据（175 个 RICH 序列），PA-MPJPE 和 MPJPE 均有进一步下降。这揭示了 2D 预训练的运动先验对数据分布存在一定敏感性，域内数据的少量注入即可带来可观的性能增益。

### 失败模式与局限性

尽管 Mocap-2-to-3 在定量指标上表现优异，以下失败模式需要在实际部署中关注：

- **上游 2D 检测器敏感性。** 模型以 2D 姿态为输入，不直接处理原始图像，因此对前级检测器的精度高度敏感。当输入骨架存在遮挡或噪声时（如原始视频中低置信度关节点），当前方法未利用检测置信度进行过滤或加权，可能导致生成的 3D 运动出现异常。
- **校准依赖。** 训练和推理均依赖校准后的多视角相机系统（已知内参和外参），这限制了在未标定在野视频上的直接应用。
- **物理约束缺失。** 当前框架未整合足部滑动减少或地面接触约束，在某些动作下可能产生不真实的地面交互（如滑步）。
- **格式迁移灵活性。** 2D 预训练采用 SMPL 格式，推理时若需输出 COCO 等格式，仍需目标格式的微调或重新训练，格式间的零样本迁移能力有限。

### 关键图表解读

- **图 5（RICH 定性比较）：** 首帧对齐后的全局运动可视化显示，Mocap-2-to-3 生成的分布外动作具有准确的身体朝向和空间定位，而基线方法（红色圆圈标注）出现不自然的姿态扭曲。
- **图 6（绝对位姿定性比较）：** 在共享世界坐标系下的无对齐对比中，基线方法随时间累积出现明显的定位漂移，Mocap-2-to-3 始终保持精确的绝对定位，无需额外设备辅助。
- **图 7（AIST++ 定性比较）：** 在 COCO 格式骨架上的泛化结果表明，多视角提升框架对不同骨架拓扑具有鲁棒性，这得益于 2D 预训练阶段学习到的视角无关运动先验。

### 补充图表

![[assets/figures/papers/paper_list_l1070_https_arxiv_org_abs_2503_03222/figures/002_Table_1.jpg]]
*Table 1: Comparison with related methods. Unlike methods limited to canonical/root-aligned trajectories, Mocap2-to-3 recovers metric-scale trajectories from monocular 2D input and can further leverage 2D data to enhance 3D results*

![[assets/figures/papers/paper_list_l1070_https_arxiv_org_abs_2503_03222/figures/006_Table_2.jpg]]
*Table 2: Quantitative results on RICH in: (1) Root-aligned in Camera Coordinates, (2) World Coordinates with initial-frame alignment, (3) World Coordinates without any alignment. The symbols ∗, ‡, and † denote the inclusion of images, scene scans, and calibrated camera poses as inputs, respectively. The best and second-best results are highlighted green and yellow*

![[assets/figures/papers/paper_list_l1070_https_arxiv_org_abs_2503_03222/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison on RICH. Global motions are compared after first-frame alignment. Our method generates more realistic OOD motions with accurate body orientation and positioning, while red circles mark unnatural baseline poses*

![[assets/figures/papers/paper_list_l1070_https_arxiv_org_abs_2503_03222/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparison on RICH. Unaligned absolute pose comparison in shared world coordinates. Unlike baseline methods that exhibit positional drift, our solution maintains accurate localization without requiring additional equipment*

![[assets/figures/papers/paper_list_l1070_https_arxiv_org_abs_2503_03222/figures/009_Table_3.jpg]]
*Table 3: Quantitative results on AIST++. Symbols ∗ or † indicate the use of images or calibrated camera poses as inputs*

![[assets/figures/papers/paper_list_l1070_https_arxiv_org_abs_2503_03222/figures/010_Table_4.jpg]]
*Table 4: Ablation study on RICH: Pointmaps boost convergence; 2D pretraining increases motion accuracy*

![[assets/figures/papers/paper_list_l1070_https_arxiv_org_abs_2503_03222/figures/011_Figure_7.jpg]]
*Figure 7: Qualitative comparison on AIST++. Our method generalizes well to COCO-format skeletons as well*

## 方法谱系与知识库定位

### 1. 与现有方法的谱系关系

Mocap-2-to-3 处于单目3D人体运动恢复这一活跃研究脉络中，其核心贡献在于将**2D数据驱动的生成先验**与**多视角几何一致性**相结合，突破了该领域长期存在的两个瓶颈：3D训练数据稀缺导致的分布外泛化能力差，以及单目升维中固有的尺度模糊性。

**与直接回归方法的对比。** 传统单目3D运动恢复方法（如 **GVHMR** (Shen et al., SIGGRAPH Asia 2024)、**WHAM** (Shin et al., CVPR 2024)）采用端到端回归范式，直接从单目图像或2D姿态预测3D运动参数。这类方法受限于3D标注数据的规模和场景多样性，在分布外动作上的泛化能力显著下降。Mocap-2-to-3 通过引入两阶段训练范式——先在大规模2D姿态数据上预训练单视角扩散模型，再在有限3D数据上微调多视角扩散模型——将3D运动恢复重新定义为多视角合成过程，从而将2D数据中蕴含的丰富运动先验迁移至3D任务。Table 1 明确对比了各方法在输入模态、相机参数需求、2D数据利用能力和度量尺度轨迹恢复等方面的差异，Mocap-2-to-3 是唯一能从单目2D输入恢复度量尺度绝对轨迹、且能进一步利用2D数据增强3D结果的方法。

**与扩散模型方法的对比。** **MVLift** (Li et al., CVPR 2025) 同样采用扩散模型将2D姿态提升至3D全局运动，但其仅使用2D数据进行训练，缺乏3D监督信号，导致运动质量落后于3D监督方法。Mocap-2-to-3 在保留2D预训练优势的同时，通过多视角微调阶段引入3D监督和View Attention层强制视角间一致性，在RICH数据集上PA-MPJPE达到26.2 mm，显著优于MVLift的30.7 mm（Table 2）。这一差距验证了“2D预训练+3D微调”混合范式的有效性。

**与几何约束方法的对比。** **Ray3D** (Zhan et al., CVPR 2022) 利用射线投影和校准相机进行单目绝对3D定位，但缺乏对场景几何的显式建模。Mocap-2-to-3 通过点图编码器（ResNet-18 + 交叉注意力层）将地面平面方程编码为空间先验，为扩散模型提供了明确的地面几何约束。这一设计的直接效果是训练收敛加速超过50%（Table 4：无点图需8k epoch达到PA-MPJPE 33.4 mm，有点图仅需3.5k epoch即达到30.5 mm），且在世界坐标系无对齐评估中W-MPJPE降至82.6 mm，远超GVHMR+SMPLify的109.4 mm。

**与优化方法的对比。** 经典的 **SMPLify** (Bogo et al., ECCV 2016) 通过优化拟合SMPL参数实现单目姿态估计，但缺乏对全局运动和绝对尺度的约束。当GVHMR的预测结果经SMPLify后处理时，Abs-MPJPE高达430.4 mm，而Mocap-2-to-3仅156.8 mm（Table 2），降幅达273.6 mm，充分说明多视角三角化结合解耦运动表示对绝对位姿精度的决定性作用。

### 2. 适用边界与局限

尽管Mocap-2-to-3在多个基准上取得了显著提升，其适用边界受以下因素制约：

**相机标定依赖。** 方法假设训练和推理时已知相机内参与外参（或可通过校准获得），多视角三角化步骤依赖精确的相机参数。这使其不适用于未标定的在野视频，限制了在移动拍摄、用户生成内容等场景下的直接部署。

**上游检测器敏感性。** 模型以2D姿态序列为输入，不直接处理原始图像，因此对前级2D检测器的精度高度敏感。当前实现未利用检测置信度进行加权或过滤，在遮挡、运动模糊等导致低质量骨架输入的场景下，误差会向下游传播并放大。

**物理约束缺失。** 方法缺乏足部滑动减少、地面接触一致性等物理约束，可能在某些动作下产生不真实的地面交互效果。这在与物理仿真或具身智能等下游任务对接时可能成为瓶颈。

**数据格式迁移成本。** 2D预训练采用特定骨架格式（如SM），推理时若需输出不同格式（如COCO-format），仍需目标格式的微调或重新训练，格式迁移灵活性有待提升。

### 3. 开放问题

基于上述局限和该方向的整体发展趋势，以下开放问题值得进一步探索：

1. **鲁棒性增强**：如何将2D检测置信度作为条件信号融入扩散模型的去噪过程，使模型能够自适应地处理遮挡和噪声输入？这可能需要修改条件注入机制，使低置信度关节点对生成过程的约束强度相应降低。

2. **弱监督标定**：能否在不依赖校准多视角系统的前提下，通过自监督（如利用场景中的几何线索）或弱监督（如单目深度估计）方式实现类似的绝对位姿估计精度？这将显著扩展方法的适用范围。

3. **物理一致性**：如何整合足部滑动减少、接触力约束或物理仿真反馈，以提升生成运动的物理真实感？这可能需要在扩散模型输出后增加一个物理优化后处理步骤。

4. **任务泛化**：该多视角提升框架的核心思想——利用2D预训练获得强先验，再通过多视角一致性实现3D升维——能否扩展到多人交互、手物交互、具身智能等需要精确3D空间推理的下游任务？这需要重新设计运动表示和条件信号以适应更复杂的交互场景。

## 原文 PDF

![[paperPDFs/CVPR_2026/Mocap_2_to_3_Multi_view_Lifting_for_Monocular_Motion_Recovery_with_2D_Pretraining.pdf]]