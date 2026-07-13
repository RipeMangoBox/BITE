---
title: "Memorize What Matters: Emergent Scene Decomposition from Multitraversee"
type: paper
paper_level: A
venue: NeurIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/Memorize_What_Matters_Emergent_Scene_Decomposition_from_Multitraversee.pdf
code_link: https://github.com/NVlabs/3DGM
project_link: https://nvlabs.github.io/3DGM/
aliases:
- 3GM3
- MWMESDFM
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "特征残差挖掘策略与鲁棒优化损失函数的引入，使得利用多遍历间的像素一致/不一致性作为自监督信号，能够在3D高斯泼溅框架下实现环境与物体的无监督分解。"
primary_logic: "利用多辆车多次遍历同一区域时，静态环境结构在多视角下保持一致性而动态物体出现不一致性的特点，通过将问题建模为鲁棒可微分渲染（内点/外点），结合去噪DINOv2特征蒸馏和特征残差挖掘，无需人工标注即可同时获得3D环境地图和2D暂时性物体分割。"
claims:
- "将多遍历环境映射制定为鲁棒可微分渲染问题，环境像素为内点，物体像素为外点。"
- "通过蒸馏去噪DINOv2特征并进行特征残差挖掘，无监督生成暂时性物体掩码，显著优于现有无监督方法。"
- "无监督2D分割平均IoU约0.45，相比STEGO提升21.36个百分点（89.8%）。"
- "3D环境重建Chamfer Distance约0.9米，远优于DepthAnything的1.9米。"
---

# Memorize What Matters: Emergent Scene Decomposition from Multitraversee

> [!tip] 核心洞察
> 利用多辆车多次遍历同一区域时，静态环境结构在多视角下保持一致性而动态物体出现不一致性的特点，通过将问题建模为鲁棒可微分渲染（内点/外点），结合去噪DINOv2特征蒸馏和特征残差挖掘，无需人工标注即可同时获得3D环境地图和2D暂时性物体分割。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 记忆重要之事：从多趟遍历中涌现的场景分解 |
| 英文题名 | Memorize What Matters: Emergent Scene Decomposition from Multitraversee |
| 会议/期刊 | NeurIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2405.17187) · [GitHub](https://github.com/NVlabs/3DGM) · [Project](https://3d-gaussian-mapping.github.io) · [Project](https://nvlabs.github.io/3DGM/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 3D Gaussian Mapping (3DGM) |
| Dataset | Mapverse-Ithaca365 |

> [!tip] 效果简介
> - Mapverse-Ithaca365 上，IoU (2D ephemeral segmentation vs. SegFormer pseudo-GT) 为 45.14% (EmerSeg)，对比 23.78% (STEGO)，变化 +21.36 points (89.8% improvement)。
> - Mapverse-Ithaca365 上，Chamfer Distance (meters, 3D reconstruction) 为 0.9 m (EnvGS)，对比 1.9 m (DepthAnything)，变化 -1.0 m (~52% reduction)。
> - Mapverse-Ithaca365 上，LPIPS (novel view synthesis) 为 0.213 (EnvGS)，对比 0.255 (3DGS)，变化 -0.042 (lower is better)。

## 概要

### 问题背景与核心瓶颈

自动驾驶系统长期面临一个根本性挑战：如何在多次经过同一区域时，让车辆自动“记住”稳定的环境结构（建筑、道路、交通标志），同时“忽略”临时出现的物体（车辆、行人、锥桶）。现有方法要么依赖人工标注的分割模型来过滤动态物体，要么需要昂贵的LiDAR传感器提供几何线索——两者都难以在纯视觉、无标注条件下大规模部署。**核心瓶颈**在于缺乏自监督信号来可靠地区分“持久的环境”与“暂时的物体”。

### 核心思想

3D Gaussian Mapping (3DGM) 的关键洞察简洁而深刻：**多辆车在不同时间经过同一地点时，静态环境结构在多视角下保持一致性，而动态物体则表现出不一致性**。将这一观察转化为技术路径，3DGM将多遍历环境映射形式化为一个**鲁棒可微分渲染问题**——环境像素被视为“内点”（inliers），物体像素被视为“外点”（outliers）。通过蒸馏去噪DINOv2特征到3D高斯中，并设计新颖的**特征残差挖掘策略**充分提取渲染损失图的空间信息，3DGM无需任何人工标注即可同时输出3D环境高斯地图和2D暂时性物体分割掩码。

### 方法定位

在方法谱系上，3DGM处于**3D高斯泼溅（3DGS）**与**自监督视觉基础模型**的交叉点。它继承3DGS的高效可微分渲染框架，但通过三个关键改进实现无监督场景分解：（1）用蒸馏的鲁棒DINOv2特征替代纯RGB监督，使环境高斯学习持久特征表示；（2）用空间特征残差挖掘替代传统的不确定性估计或学习掩码，实现外点识别；（3）用掩码鲁棒损失替代标准L1损失，仅在内点像素上优化环境重建。与依赖LiDAR或预训练分割模型的方法（如3DGS+SegFormer）相比，3DGM是**完全自监督且LiDAR-free**的。

### 主要结果

在Mapverse-Ithaca365基准上，3DGM展现了显著的性能优势：

- **2D暂时性物体分割**：无监督方法EmerSeg达到45.14%的mIoU，相比无监督基线STEGO（23.78%）提升21.36个百分点（89.8%的改善），甚至接近某些监督方法的性能。
- **3D环境重建**：EnvGS的Chamfer Distance约0.9米，远优于DepthAnything的约1.9米（降低约52%），实现了更精确的几何重建。
- **新视角合成**：在移除暂时性物体像素后，EnvGS的LPIPS为0.213，优于标准3DGS的0.255，证明鲁棒优化有效提升了渲染质量。

消融实验进一步揭示：分割性能随遍历次数增加而提升（从1次的15.15% IoU到10次的56.01%），特征维度32是性能阈值，去噪DINOv2作为特征骨干表现最优。这些结果共同验证了“多遍历一致性”作为自监督信号的有效性。

### 局限与展望

尽管效果显著，3DGM仍面临若干挑战：物体阴影的分割不够精确，大面积持久遮挡物可能导致过拟合，远距离小物体的分割精度有限，以及无法处理大幅度的光照和季节变化。这些局限指向了未来的研究方向——阴影感知的环境映射、时序信息整合、自适应阈值设计，以及4D表示对长期一致性的支持。

自动驾驶和移动机器人系统依赖精确的3D环境地图实现定位、规划与导航。传统建图方法通常假设环境是静态的，但真实世界中充斥着行人、车辆等临时性动态物体——这些物体在不同时间遍历同一区域时出现和消失，对构建持久环境表示构成根本性挑战。

现有解决方案存在显著瓶颈。主流方法依赖人工标注的分割模型或LiDAR传感器来过滤动态物体：前者需要昂贵的大规模像素级标注，且跨场景泛化能力有限；后者增加了硬件成本和系统复杂度。在纯视觉、无标注条件下，如何有效分离持久环境结构与临时物体，仍是一个悬而未决的问题。

多趟遍历（multitraverse）数据为此提供了独特的自监督信号。当多辆车在不同时间经过同一区域时，静态环境结构（建筑、道路、交通标志）在多视角下保持一致性，而动态物体（车辆、行人）则在不同遍历间呈现不一致性。这种“共识即环境、不一致即物体”的直觉，构成了无监督场景分解的核心前提。

然而，将这一直觉转化为可操作的计算框架面临多重技术挑战。首先，需要一种能够同时表示3D几何与外观的表示方法，支持可微分渲染以进行端到端优化。其次，需要设计鲁棒的特征表示，使其对光照、天气等环境变化具有不变性，同时能敏锐捕捉临时物体的出现。最后，需要一种机制来挖掘渲染残差中的空间信息，将像素级的不一致性转化为精确的物体分割掩码。

本文提出3D Gaussian Mapping (3DGM)，将多趟遍历环境建图形式化为鲁棒可微分渲染问题——将环境像素视为内点（inliers），物体像素视为外点（outliers）。通过蒸馏去噪DINOv2特征到3D高斯泼溅框架中，并结合新颖的特征残差挖掘策略，3DGM首次在无需LiDAR和人工监督的条件下，同时实现了3D环境高斯地图的构建和2D临时性物体分割。

## 核心方法与创新机理

3DGM的核心创新在于将多遍历环境映射重新定义为**鲁棒可微分渲染问题**，并围绕这一范式设计了三个紧密耦合的机制，实现了纯视觉、无监督的场景分解。其关键创新点可归纳为以下三个“changed slots”：

### 1. 特征监督：从RGB到去噪DINOv2特征的蒸馏

传统3DGS仅依赖RGB像素进行渲染监督，难以区分外观相似的静态环境与动态物体。3DGM将**去噪DINOv2特征**蒸馏到3D高斯中，使每个高斯不仅学习颜色信息，还学习高维语义特征表示（公式2）：

$$\mathcal{L} = \sum_t ( \mathcal{L}_{rgb}(\mathbf{I}_t(\pmb{\xi}_t; \mathbf{G}), \mathbf{I}_t) + \mathcal{L}_{feat}(\mathbf{F}_t(\pmb{\xi}_t; \mathbf{G}), \mathbf{F}_t) )$$

这一设计的因果机制在于：DINOv2特征对光照、视角变化具有天然鲁棒性，但对物体身份变化敏感。当环境高斯被训练去渲染持久结构的特征时，它对临时出现的物体（如车辆、行人）会产生显著的特征渲染残差，从而为后续的物体识别提供了强信号。消融实验证实，去噪DINOv2作为特征骨干达到44.13% IoU，显著优于DINOv1及其他变体（Table 2）。

### 2. 外点识别：特征残差空间挖掘策略

现有鲁棒渲染方法通常依赖不确定性估计或学习的掩码来识别外点，但这些方法在复杂自动驾驶场景中精度不足。3DGM提出**特征残差挖掘（Feature Residuals Mining）**策略，充分利用渲染损失图的空间信息：

- 计算渲染特征与真实特征之间的残差图
- 通过空间轮廓处理（contour processing）从残差图中提取物体级掩码
- 无需任何人工标注或预训练分割模型

该策略的瓶颈突破在于：它不依赖语义先验，而是利用“多遍历间静态结构特征一致、动态物体特征不一致”这一几何-语义联合约束，实现了真正的无监督物体发现。

### 3. 优化损失：鲁棒L1损失与短暂性掩码耦合

标准3DGS使用L1损失对所有像素等权优化，动态物体会“污染”环境高斯的训练。3DGM将EmerSeg提取的**短暂性掩码（ephemerality masks）**作为外点指示器，构建鲁棒优化损失（公式3）：

$$\mathcal{L} = \sum_t \mathcal{L}_{rgb}(\mathbf{M}_t \odot \mathbf{I}_t(\boldsymbol{\xi}_t; \mathbf{G}), \mathbf{M}_t \odot \mathbf{I}_t)$$

该损失仅在环境像素（内点）上计算，使环境高斯专注于学习持久结构。实验表明，这一机制使3D重建的Chamfer Distance从DepthAnything的1.9米降至约0.9米（Figure 5），新视角合成的LPIPS从3DGS的0.255降至0.213（Table 3），甚至在某些场景中超越了使用预训练分割模型的3DGS+SegFormer方法。

### 创新协同效应

上述三个创新并非孤立存在，而是形成了一条**因果链**：特征蒸馏提供判别性信号→残差挖掘定位外点→鲁棒损失保护内点优化。这种协同使得3DGM能够在无LiDAR、无标注的条件下，同时输出高质量的3D环境地图和2D暂时性物体分割，突破了现有方法对人工标注和昂贵传感器的依赖。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2405_17187/figures/001_Figure_1.jpg]]
*Figure 1: A high-level diagram of 3D Gaussian Mapping (3DGM). Given multitraverse RGB videos, 3DGM outputs a Gaussian-based environment map (EnvGS) and 2D ephemerality segmentation (EmerSeg) for the input images. Note that the proposed framework is LiDAR-free and self-supervised*

3DGM 将多趟遍历的环境映射问题形式化为一个**鲁棒可微分渲染**问题：将持久环境像素视为内点（inlier），将临时物体像素视为外点（outlier），从而在无需人工标注的条件下实现环境与物体的分解。整个框架由三个核心模块串联构成，形成“初始化—分割—优化”的流水线。

**输入与输出。** 系统以多趟遍历的 RGB 视频序列为输入，输出两个协同产物：基于高斯的 3D 环境地图 **EnvGS**，以及对应输入图像的 2D 暂时性物体分割掩码 **EmerSeg**。整个过程不依赖 LiDAR 传感器，也无需任何人工标注。

**模块一：初始化（COLMAP SfM）。** 首先利用经典的运动恢复结构（Structure from Motion, SfM）对多趟遍历图像进行联合重建，获得所有视角的相机位姿以及稀疏的 3D 点云，作为高斯泼溅的初始点。相比单趟遍历 SfM，多趟联合初始化能提供更鲁棒的位姿估计和更完整的初始几何。

**模块二：EmerSeg——无监督暂时性物体分割。** 该模块是 3DGM 实现无监督分解的核心。其关键洞察在于：蒸馏到 3D 高斯中的去噪 DINOv2 特征对光照和外观变化具有鲁棒性，持久环境结构在不同遍历间特征一致，而临时物体则呈现显著的特征残差。EmerSeg 通过以下步骤生成 2D 暂时性掩码：
1. **鲁棒特征蒸馏**：在训练环境高斯时，不仅监督 RGB 渲染，还同时监督特征渲染，损失函数为：
   $$\mathcal{L} = \sum_t \left( \mathcal{L}_{rgb}(\mathbf{I}_t(\pmb{\xi}_t; \mathbf{G}), \mathbf{I}_t) + \mathcal{L}_{feat}(\mathbf{F}_t(\pmb{\xi}_t; \mathbf{G}), \mathbf{F}_t) \right)$$
   这使得高斯学习到的是跨遍历一致的持久特征，而临时物体区域则产生高特征渲染残差。
2. **特征残差挖掘**：利用渲染损失图的空间信息，通过轮廓处理等后处理步骤，从特征残差中提取精确的暂时性物体掩码。这一策略充分利用了残差图的空间结构，相比简单的阈值分割能获得更完整的物体轮廓。

**模块三：EnvGS——鲁棒环境优化。** 获得暂时性掩码后，EnvGS 利用这些掩码对 3D 高斯进行精调。损失函数被修改为仅在非物体区域（内点）上进行监督：
$$\mathcal{L} = \sum_t \mathcal{L}_{rgb}(\mathbf{M}_t \odot \mathbf{I}_t(\boldsymbol{\xi}_t; \mathbf{G}), \mathbf{M}_t \odot \mathbf{I}_t)$$
其中 $\mathbf{M}_t$ 为 EmerSeg 提取的暂时性掩码。通过屏蔽外点像素，环境高斯得以专注于学习持久场景结构，从而在渲染时自动“擦除”临时物体。

**流水线整体流程**如 Figure 2 所示：多趟遍历 RGB 图像经 COLMAP 初始化后，先通过联合 RGB 与特征渲染训练初始环境高斯；随后利用特征残差挖掘生成暂时性掩码；最后在掩码引导下进行鲁棒优化，产出最终的环境高斯和分割结果。三个模块相互增强——更好的特征蒸馏带来更精确的掩码，更精确的掩码又反哺更干净的环境重建。

### 总体框架

3DGM 包含三个顺序执行的阶段：**Initialization（初始化）**、**EmerSeg（短暂性物体分割）** 和 **EnvGS（环境高斯优化）**。给定多趟遍历的 RGB 视频，框架最终输出基于高斯的 3D 环境地图（EnvGS）和对应的 2D 短暂性物体分割掩码（EmerSeg），整个过程无需 LiDAR 和人工标注。

### 阶段一：多遍历 SfM 初始化

传统 3DGS 依赖单次遍历的 SfM 进行初始化，但单次遍历可能因动态物体遮挡导致稀疏重建不完整。3DGM 将多趟遍历的所有图像联合输入 COLMAP 进行 SfM，同时估计相机位姿 $\boldsymbol{\xi}_t$ 并生成初始稀疏点云，作为后续高斯优化的起点。多视角联合重建有助于在动态物体遮挡区域获得更鲁棒的初始几何。

### 阶段二：EmerSeg——特征蒸馏与残差挖掘

EmerSeg 是无监督 2D 短暂性物体分割的核心模块，其关键洞察在于：**环境结构在多遍历间保持一致性，而短暂性物体在特征空间呈现高残差**。

#### 特征蒸馏

首先，将去噪 DINOv2 特征蒸馏到 3D 高斯中。每个高斯体 $G_i$ 除了原有的位置、协方差、不透明度和球谐系数外，额外学习一个 $d$ 维语义特征向量 $\mathbf{f}_i$。训练时同时优化 RGB 渲染损失和特征渲染损失：

$$
\mathcal{L} = \sum_t \left( \mathcal{L}_{rgb}(\mathbf{I}_t(\boldsymbol{\xi}_t; \mathbf{G}), \mathbf{I}_t) + \mathcal{L}_{feat}(\mathbf{F}_t(\boldsymbol{\xi}_t; \mathbf{G}), \mathbf{F}_t) \right)
$$

其中 $\mathbf{I}_t(\boldsymbol{\xi}_t; \mathbf{G})$ 和 $\mathbf{F}_t(\boldsymbol{\xi}_t; \mathbf{G})$ 分别为高斯 $\mathbf{G}$ 在位姿 $\boldsymbol{\xi}_t$ 下渲染的 RGB 图像和特征图，$\mathbf{I}_t$ 和 $\mathbf{F}_t$ 为真实图像和预提取的去噪 DINOv2 特征。为提升效率，特征维度通过 PCA 从 768 压缩至 64。

由于环境结构在多遍历间一致，环境高斯会学习到稳定的特征表示；而短暂性物体在不同遍历中外观不一致，其特征渲染残差显著偏高。

#### 特征残差挖掘

在获得特征渲染残差图后，EmerSeg 不直接使用简单的阈值分割，而是提出**特征残差挖掘策略**：利用残差图的空间信息，通过轮廓处理等后处理步骤，从残差图中提取完整的物体实例掩码 $\mathbf{M}_t$。该策略充分挖掘了渲染损失图的空间结构，相比直接阈值化能更准确地分割完整物体边界。

### 阶段三：EnvGS——鲁棒环境优化

获得短暂性物体掩码 $\mathbf{M}_t$ 后，EnvGS 阶段将多遍历环境映射形式化为**鲁棒可微分渲染**问题：环境像素为内点（inlier），物体像素为外点（outlier）。优化时利用掩码屏蔽外点像素，仅在内点区域监督环境高斯学习：

$$
\mathcal{L} = \sum_t \mathcal{L}_{rgb}(\mathbf{M}_t \odot \mathbf{I}_t(\boldsymbol{\xi}_t; \mathbf{G}), \mathbf{M}_t \odot \mathbf{I}_t)
$$

其中 $\odot$ 表示逐元素乘法。通过这种掩码鲁棒损失，环境高斯仅从一致性的环境结构中学习，短暂性物体被有效排除在优化之外。

### 辅助损失

为提升几何质量，框架引入两项辅助损失（附录 A.3）：

- **逆深度平滑损失**：通过图像梯度加权，鼓励深度在非边缘区域平滑，在边缘处保留不连续性：

  $$
  \mathcal{L}_{depth} = \frac{1}{N} \sum_{i,j} \left( |\nabla D_{i,j}^x| \exp(-\|\nabla I_{i,j}^x\|) + |\nabla D_{i,j}^y| \exp(-\|\nabla I_{i,j}^y\|) \right)
  $$

- **天空遮罩损失**：强制天空区域的渲染不透明度接近 0，非天空区域接近 1：

  $$
  \mathcal{L}_{sky} = \frac{1}{N} \sum_{i,j} \left( |\mathcal{M}_{sky} - (1 - \mathcal{O})| \right)
  $$

### 方法对比：关键改进槽位

| 模块 | 基线方法 | 3DGM 改进 |
|------|---------|----------|
| 特征监督 | 仅 RGB | RGB + 蒸馏去噪 DINOv2 特征 |
| 外点识别 | 不确定性估计或学习掩码 | 空间特征残差挖掘 + 轮廓处理 |
| 优化损失 | 标准 L1 损失 | 短暂性掩码屏蔽的鲁棒 L1 损失 |
| 初始化 | 单遍历 SfM | 多遍历 SfM 联合初始化 |

这些改进槽位共同构成了 3DGM 的技术贡献：通过将鲁棒优化、自监督特征蒸馏和空间残差挖掘有机结合，首次在 3DGS 框架下实现了无需人工标注的多遍历环境与物体分解。

## 实验与关键发现

### 实验设置与基准

3DGM 在 **Mapverse-Ithaca365** 数据集上进行评估，该数据集包含多辆车在纽约 Ithaca 地区 20 个地点多次遍历采集的 RGB 视频，不含 LiDAR 标注。所有实验均在单块 NVIDIA RTX 3090 GPU 上完成。为提升效率，DINOv2 特征维度通过 PCA 从 768 压缩至 64。

**无监督 2D 分割评估**采用五个顶级监督模型生成的伪真值作为参考（PSPNet、SegViT、Mask2Former、SegFormer、InternImage），其中带 `*` 号的模型未在该数据集上训练。**3D 重建评估**以 LiDAR 点云为参考，计算 Chamfer Distance。**新视角合成评估**将测试/训练视图比例设为 1/8，移除暂时性物体像素后计算 LPIPS 和 SSIM。

---

### 2D 暂时性物体分割：EmerSeg 性能

**Table 1** 展示了 EmerSeg 与五种监督方法及两种无监督方法（STEGO、CAUSE）的对比结果。EmerSeg 以 **45.14% 的平均 IoU** 显著优于现有无监督方法，相比 STEGO 提升 **21.36 个百分点（89.8% 提升）**，相比 CAUSE 提升 18.81 个百分点（71.4% 提升）。在 20 个地点中，有 7 个地点 IoU 超过 50%，最高达到 56%（**Figure 3**）。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2405_17187/figures/004_Table_1.jpg]]
*Table 1: Mean IoU of unsupervised vs. five supervised methods in Mapverse-Ithaca365. ∗ indicates the model without training on our dataset*

定性结果（**Figure 4** 及附录 Figure V）显示，EmerSeg 在多种光照和天气条件下均能有效分割汽车、公交车和行人，展现了良好的鲁棒性。

---

### 消融实验：EmerSeg 关键设计选择

**Table 2** 系统消融了遍历次数、特征维度、特征分辨率和特征骨干网络的影响：

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2405_17187/figures/006_Table_2.jpg]]
*Table 2: Ablation Study Results of EmerSeg in Mapverse-Ithaca365*

| 消融维度 | 关键发现 | 最优配置 |
|----------|----------|----------|
| **遍历次数** | IoU 从 1 次遍历的 15.15% 提升至 10 次遍历的 56.01%，2 次遍历后提升最为显著 | 10 次遍历 |
| **特征维度** | 32 维是近似阈值，低于此值 IoU 急剧下降 10%~25%，64 维达到最佳性能 | 64 维 |
| **特征分辨率** | 110×180 分辨率获得 44.13% IoU，更高分辨率反而轻微下降 | 110×180 |
| **特征骨干** | 去噪 DINOv2 表现最佳（44.13% IoU），优于 DINOv1 和 DINOv2 其他变体 | 去噪 DINOv2 |

这些结果表明：**多遍历提供的时序不一致性信号**是 EmerSeg 的核心驱动因素，而**去噪 DINOv2 特征的鲁棒表示**和**适中的特征分辨率**在精度与效率间取得了最优平衡。附录 Figure VII 进一步展示了不同迭代次数下 IoU 的收敛过程及相应特征残差图的可视化演变。

---

### 3D 环境重建：EnvGS 几何质量

**Figure 5** 展示了 EnvGS 与 DepthAnything 在 3D 几何重建上的定性与定量对比。EnvGS 的平均 Chamfer Distance 约为 **0.9 米**，远优于 DepthAnything 的约 1.9 米（降低约 52%）。定性可视化显示，EnvGS 生成的深度图具有平滑过渡和清晰边缘，在路面等区域也保持了较好的几何一致性。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2405_17187/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative and quantitative evaluation of 3D geometry in Mapverse-Ithaca365*

值得注意的是，EnvGS 完全基于相机输入，**无需 LiDAR 传感器参与训练**，即可在有效忽略暂时性物体的同时重建 3D 环境结构。

---

### 新视角合成与环境渲染

**Table 3** 比较了不同方法在新视角合成任务上的表现。EnvGS 的 LPIPS 为 **0.213**，优于 VanillaNeRF（0.423）、RobustNeRF（0.266）和原始 3DGS（0.255）。在 SSIM 指标上，EnvGS（0.806）与使用预训练 SegFormer 掩码的 3DGS+SegFormer（0.806）持平，表明无监督掩码质量已接近监督模型的水平。

**Figure 6** 的定性渲染对比进一步证实：EnvGS 能有效移除暂时性物体及其阴影，在某些情况下甚至优于配备预训练模型的 3DGS+SegFormer。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2405_17187/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative evaluations of the environment rendering. Our method demonstrates robust performance against transient objects, and can even outperform the method equipped with a pretrained model in some cases. Notably, this includes the effective removal of object shadows*

---

### 失败模式与局限性

尽管 3DGM 在多数场景下表现鲁棒，论文明确指出以下失败模式：

1. **阴影分割困难**：物体阴影有时被误分为短暂性物体或完全遗漏，难以准确处理。
2. **大面积持久遮挡**：面对长时间存在的遮挡物，模型可能过拟合导致分割失败。
3. **远距离小物体**：受限于特征图分辨率，对远处小物体的分割精度有限。
4. **反射表面**：不同遍历间反射外观变化大，易导致错误分割。
5. **光照与季节变化**：当前方法无法处理大幅度的光照和季节变化，限制了实际部署。
6. **无纹理区域几何**：路面等无纹理区域的 3D 重建质量有待提升，深度估计缺乏约束。

附录 Figure V 中标注了部分失败案例，包括阴影误分割和远距离物体遗漏等典型问题。

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2405_17187/figures/021_Figure.jpg]]
*Figure: XI: Comparison of ephemerality masks and feature residuals using different versions of the DINO model. The figure includes raw and denoised versions of DINOv1 and DINOv2, as well as raw and denoised versions of DINOv2 with a registration module (DINOv2-Register). Denoising enhances the quality of feature residuals, while registration does not yield notable gains*

## 定位与知识库关联

### 1. 问题定位：3D 映射中的“持久/临时”分解瓶颈

自动驾驶场景的长期 3D 环境建图面临一个核心瓶颈：**如何在无人工标注、无 LiDAR 的条件下，从纯视觉多趟遍历数据中分离出持久的环境结构与临时的动态物体**。现有方法对此存在两类典型不足：

- **监督式分割依赖**：传统 3D 映射管线通常需要预先训练的分割模型（如 PSPNet、SegViT、Mask2Former、SegFormer、InternImage）或 LiDAR 点云来识别并过滤动态物体。这类方法不仅依赖昂贵的人工标注，且分割模型在跨域泛化时性能退化严重。
- **无监督方法的特征脆弱性**：现有无监督分割方法（如 STEGO、CAUSE）在自动驾驶场景中对光照变化、视角差异敏感，难以可靠地区分“外观变化但结构持久”的区域与“真正临时”的物体。

3DGM 将多趟遍历环境建图**重新建模为鲁棒可微分渲染问题**，将环境像素视为内点（inlier）、物体像素视为外点（outlier），从而绕过了对显式语义标注的依赖。这一建模思路与 RobustNeRF 等鲁棒 NeRF 方法有思想上的延续性，但 3DGM 的关键创新在于引入了**去噪 DINOv2 特征蒸馏**与**特征残差空间挖掘**，使得外点识别不再依赖简单的 RGB 残差或不确定性估计，而是在高维鲁棒特征空间中利用多遍历间的“共识-不一致”信号进行无监督掩码生成。

### 2. 技术谱系：从 NeRF 鲁棒渲染到 3DGS 特征蒸馏

3DGM 的技术架构处于三条研究线索的交汇处：

**（1）3D 高斯泼溅（3D Gaussian Splatting）渲染管线**

3DGM 选择 3DGS 而非传统 NeRF（如 VanillaNeRF）作为底层表示，主要考量在于 3DGS 的显式点云结构更便于提取 3D 几何信息，且渲染效率更高。实验表明，在相同的新视角合成任务上，3DGS 基方法在 LPIPS 指标上显著优于 NeRF 基方法（EnvGS 0.213 vs. VanillaNeRF 0.423）。这一选择也使得后续的 3D 环境重建（Chamfer Distance 约 0.9 m）能够直接从优化后的高斯中提取点云，无需额外的后处理步骤。

**（2）视觉基础模型特征蒸馏**

3DGM 在每个 3D 高斯上附加一个可学习的语义特征向量 $\mathbf{f}_i \in \mathbb{R}^d$，并通过可微分渲染将其投影到 2D 特征图。该方法的关键设计选择是采用**去噪 DINOv2** 作为教师特征——消融实验证实，去噪 DINOv2 的 IoU 达 44.13%，优于 DINOv1 及 DINOv2 的其他变体。特征维度的消融进一步揭示了一个有趣的现象：**32 维是一个近似阈值**，低于该维度时 IoU 显著下降（约 10%-25%），而 64 维达到最佳性能。为平衡效率与精度，3DGM 通过 PCA 将 768 维压缩至 64 维，特征图分辨率优化为 110×180（IoU 44.13%，存储 5.0 MB），更高分辨率反而导致性能轻微下降。

**（3）鲁棒优化与外点掩码**

与传统 3DGS 的标准 L1 损失不同，3DGM 在 EnvGS 阶段采用**被暂时性掩码 $\mathbf{M}_t$ 屏蔽的鲁棒 L1 损失**：

$$\mathcal{L} = \sum_t \mathcal{L}_{rgb}(\mathbf{M}_t \odot \mathbf{I}_t(\boldsymbol{\xi}_t; \mathbf{G}), \mathbf{M}_t \odot \mathbf{I}_t)$$

这一设计使得环境高斯仅在“内点像素”上接收梯度信号，从而避免将临时物体的外观“烧录”进环境表示。与 3DGS+SegFormer（使用预言机级别的监督分割掩码）的对比显示，EnvGS 在 SSIM 指标上达到同等水平（0.806 vs. 0.806），说明无监督掩码的质量已接近监督方法的水平。

### 3. 适用边界与关键约束

3DGM 的设计隐含了若干适用前提，理解这些边界对于正确使用该方法至关重要：

- **多遍历数据依赖**：方法的核心自监督信号来自多趟遍历间的像素一致性/不一致性。消融实验表明，分割 IoU 从 1 次遍历的 15.15% 提升至 10 次遍历的 56.01%，其中 **2 次遍历后的提升最为显著**。这意味着该方法在仅有单次遍历的场景下性能有限，需要至少 2 次以上、覆盖同一区域的多次采集。
- **光照与季节稳定性假设**：去噪 DINOv2 特征虽然比 RGB 更鲁棒，但论文明确指出当前方法**无法处理大幅度的光照和季节变化**。反射表面在不同遍历中的外观变化也容易导致错误分割。
- **物体尺度与距离敏感性**：由于特征图分辨率有限（最优为 110×180），对远距离小物体的分割精度受限。论文将此列为已知局限，并提出了自适应阈值挖掘的开放问题。
- **阴影处理的模糊性**：模型难以准确区分物体阴影——有时将阴影误分为短暂性物体，有时又遗漏。这一问题的根源在于阴影在特征空间中可能同时表现出“持久”（随光照变化而移动）和“临时”（与物体共现）的双重特性。

### 4. 局限与开放问题

论文明确列出了以下局限，并对应提出了值得探索的方向：

| 局限 | 开放问题 |
|------|----------|
| 物体阴影分割不准确，易误分或遗漏 | 如何实现阴影感知的环境映射？是否需要在特征空间中显式建模光照不变性？ |
| 大面积、长时间存在的遮挡物可能导致模型过拟合 | 能否利用时间维度的多帧一致性或运动信息来处理持久遮挡？ |
| 远距离小物体分割精度有限 | 如何设计自适应阈值，根据物体距离动态调整特征残差的挖掘策略？ |
| 反射表面外观变化大，易导致错误分割 | 能否通过大规模野外数据训练视觉基础模型，进一步提升特征对反射的鲁棒性？ |
| 路面等无纹理区域 3D 重建质量不足 | 能否整合网格重建或 2D 高斯泼溅来增强无纹理区域的几何约束？ |
| 无法处理大幅度光照和季节变化 | 如何引入 4D 表示（时间作为第四维度）来建模长期环境变化，提升跨季节一致性？ |

此外，从评估方法的角度，需要注意当前无监督分割的评估使用监督模型生成的伪真值作为参考，这可能引入系统性偏差。渲染评估中移除暂时性物体像素的做法虽然合理，但不同方法对掩码边界的处理差异可能影响可比性。

### 5. 在知识库中的定位

3DGM 在自动驾驶建图领域的方法谱系中占据了一个独特位置：它**首次在纯视觉、无 LiDAR、无人工标注的条件下，实现了 3D 环境高斯与 2D 暂时性物体掩码的联合无监督生成**。相较于依赖 LiDAR 的建图方法，3DGM 降低了传感器成本；相较于依赖监督分割的方法，它消除了标注负担和跨域泛化问题；相较于现有无监督分割方法（STEGO、CAUSE），它在自动驾驶场景中取得了显著的性能提升（IoU 提升 21.36 个百分点，89.8% 相对改进）。其核心贡献——特征残差挖掘策略与鲁棒优化损失的结合——为后续研究提供了一个可扩展的自监督框架，但面向大规模、跨季节、全天候的实际部署，仍需解决上述开放问题。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/Memorize_What_Matters_Emergent_Scene_Decomposition_from_Multitraversee.pdf]]
