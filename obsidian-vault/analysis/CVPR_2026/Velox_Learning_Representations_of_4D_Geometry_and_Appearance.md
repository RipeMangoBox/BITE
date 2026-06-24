---
title: "Velox: Learning Representations of 4D Geometry and Appearance"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Velox_Learning_Representations_of_4D_Geometry_and_Appearance.pdf
project_link: "https://apple.github.io/ml-velox"
code_link: null
aliases:
- Velox
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 使用Perceiver风格的编码器直接处理无结构的时空彩色点云，无需时间对应关系；并联合训练流匹配的4D表面解码器和高斯解码器，使动态token同时捕获几何和外观。
primary_logic: 通过将时空点云压缩为一组动态token，并用互补的几何和外观解码器进行监督，可以学习到一个紧凑、描述性强且易于访问的4D对象表示，适用于多种下游任务。
claims:
- Velox使用Perceiver编码器从无结构时空彩色点云中学习动态token，无需时间对应。
- 联合4D表面解码器（流匹配）和高斯解码器监督，使token同时捕获几何和外观。
- 在重建、视频到4D生成、3D跟踪和布料模拟等任务上均优于现有方法。
- Objaverse Reconstruction (256 scenes) 上 PSNR↑ = 35.39
---

# Velox: Learning Representations of 4D Geometry and Appearance

> [!tip] 核心洞察
> 通过将时空点云压缩为一组动态token，并用互补的几何和外观解码器进行监督，可以学习到一个紧凑、描述性强且易于访问的4D对象表示，适用于多种下游任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | Velox：学习四维几何与外观表示 |
| 英文题名 | Velox: Learning Representations of 4D Geometry and Appearance |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.04527) · [Project](https://apple.github.io/ml-velox) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Velox |
| Dataset | Objaverse Reconstruction, Objaverse 3D Tracking, Video-to-4D |

> [!tip] 效果简介
> - Objaverse Reconstruction (256 scenes) 上，PSNR↑ 35.39 vs 26.45 (GVF) (+8.94)。
> - Objaverse Reconstruction 上，LPIPS↓ 0.021 vs 0.051 (GVF) (-0.030)。
> - Objaverse 3D Tracking 上，L2_all^3D↓ 0.025 vs 0.068 (SpatialTrackerV2) (-0.043)。

## 概述

### 问题背景

理解动态三维对象——即同时捕捉其几何形状随时间的变化和表面外观——是计算机视觉的核心挑战之一。现有方法通常依赖难以获取的时间对应关系（如逐帧点云配准），或将外观建模与几何建模分离处理，导致表示能力不足或对输入条件要求过高，难以泛化到多样的下游任务。

### 核心方法

Velox 提出了一种紧凑的潜在四维对象表示，称为**动态token（dynamic tokens）**。其核心思路是：

1. **无结构输入**：直接以时空彩色点云 $\mathcal{X} = \{(\mathbf{x}_i \in \mathbb{R}^3, \mathbf{c}_i \in [0,1]^3, \tau_i \in \mathbb{R})\}_{i=1}^N$ 作为输入，无需任何时间对应关系。
2. **Perceiver编码器压缩**：使用 Perceiver IO 风格的编码器将无结构点云压缩为一组动态token，这些token隐式地联合编码了几何和外观信息。
3. **双解码器监督**：通过两个互补的解码器对动态token进行训练——基于流匹配的4D表面解码器建模时变几何分布，高斯解码器则将token映射为3D高斯参数以渲染新视角图像。

最终训练目标为联合损失 $\mathcal{L} = \mathcal{L}_V + \mathcal{L}_{GS} + \gamma\mathcal{L}_C$，其中 $\mathcal{L}_V$ 为流匹配速度监督，$\mathcal{L}_{GS}$ 为图像重建损失，$\mathcal{L}_C$ 为token的KL正则项（$\gamma=10^{-4}$）。

### 方法定位

Velox 在4D对象表示领域填补了一个关键空白：**同时建模几何与外观，且无需时间对应**。与逐帧重建方法（如 LiTo）相比，Velox 通过跨帧联合建模获得更一致的外观；与基于变形的方法（如 GVF）相比，Velox 避免了变形场在大运动区域的失效问题。在生成式建模方面，Velox 在动态token空间上训练 DiT 模型，支持视频到4D生成和布料模拟等任务，而无需依赖像素对齐高斯（如 L4GM）所需的测试时优化。

### 主要结果

在多个任务上，Velox 均显著优于现有方法：

- **4D重建**（Objaverse，256个场景）：PSNR 35.39，较 GVF（26.45）提升 +8.94；LPIPS 0.021，较 GVF（0.051）降低 0.030。
- **3D跟踪**（Objaverse）：$\text{L2}_{\text{all}}^{3D}$ 为 0.025，较 SpatialTrackerV2（0.068）降低 0.043。
- **视频到4D生成**（Objaverse，随机相机）：新视角 PSNR 20.62，较 L4GM（18.30）提升 +2.32；LPIPS 0.104，较 L4GM（0.146）降低 0.042。

消融实验进一步表明，纹理增广（PSNR 从 32.41 提升至 33.93）、增加动态token数量（从4096到16384持续改善Chamfer和LPIPS）以及使用解码器预测体素（接近GT体素性能）均对最终效果有显著贡献。

## 背景与动机

### 四维对象表示的需求与挑战

现实世界中的对象是动态的——它们随时间移动、变形，并呈现出丰富的外观变化。要构建能够理解、重建和生成这类动态对象的智能系统，一个核心前提是学习到有效的**四维（4D）对象表示**，即同时编码三维几何、时间演化和视觉外观的紧凑描述子。然而，现有的4D表示方法在两个关键维度上存在显著不足。

**瓶颈一：对时间对应关系的过度依赖。** 许多现有方法将4D对象建模为逐帧三维表示的序列，或通过变形场连接不同时刻的表面。这类方法通常需要显式的帧间对应关系作为监督信号——例如，需要知道第t帧表面上的某个点在t+1帧中的确切位置。在真实场景中，这类稠密的时间对应关系极难获取，严重限制了方法的可扩展性和泛化能力。

**瓶颈二：几何与外观的分离建模。** 另一类方法虽能处理动态几何，却往往忽略或分离了外观建模。这意味着学到的表示仅描述形状变化，而无法刻画纹理、材质等视觉属性随时间的演变。这种描述性的缺失使得表示难以直接用于需要视觉输出的下游任务，如新视角渲染或视频生成。

### 核心动机与研究问题

上述缺口催生了一个自然的研究问题：**能否学习一种紧凑的4D对象表示，使其同时满足三个条件——（1）无需时间对应关系即可训练；（2）联合捕获几何和外观；（3）易于迁移到多样化的下游任务？**

Velox正是围绕这一核心动机展开。其关键洞察在于：如果将无结构的时空彩色点云直接压缩为一组**动态token**，并用互补的几何解码器和外观解码器联合监督，那么这些token将被迫同时编码形状的时空演化和表面的视觉属性。这种表示不仅规避了时间对应关系的需求，还因其紧凑的隐式形式而天然适用于生成、跟踪等多种任务。

### 方法定位与谱系

在4D表示的方法谱系中，Velox占据了一个独特的位置。与逐帧重建方法（如**LiTo**，每帧独立编码隐变量）相比，Velox通过跨帧共享的动态token实现了时间一致性建模。与基于变形场的方法（如**GVF**，依赖稠密对应关系驱动高斯变形）相比，Velox完全摆脱了对时间对应的依赖，转而使用流匹配解码器直接建模表面分布。与像素对齐的生成方法（如**L4GM**，从视频像素直接回归高斯参数）相比，Velox在紧凑的隐空间中操作，使得生成模型（DiT）能够更高效地学习4D对象的先验分布。

表4（见附录）系统梳理了相关4D表示在几何建模、外观建模、预训练模型使用、隐空间维度、输入形式和训练数据集等维度上的差异，进一步明确了Velox在“无需对应关系的联合几何-外观表示”这一细分方向上的开创性定位。

## 核心创新

Velox 的核心创新在于**将无结构的时空彩色点云压缩为一组联合表示几何与外观的动态 token**，从而绕过了现有 4D 对象表示方法对时间对应关系的依赖，并在单一紧凑表示中同时捕获形状和纹理信息。

### 关键设计转变：Changed Slots 分析

| 设计维度 | 基线方法 | Velox | 机制优势 |
|----------|----------|-------|----------|
| **编码器输入** | 需要时间对应关系或逐帧点云 | 无结构时空彩色点云，无需时间对应 | 降低输入要求，避免昂贵的对应标注 |
| **表示形式** | 逐帧隐变量或变形场 | 联合 4D 动态 token | 跨时间共享信息，避免逐帧独立建模的冗余 |
| **几何建模** | 静态逐帧重建或基于变形 | 条件流匹配解码器 $p(\mathbf{x}|\tau,\mathbf{s})$ | 直接建模时变表面分布，适应大运动和非刚性变形 |
| **外观建模** | 通常省略或与几何分离 | 高斯解码器，基于动态 token 和体素 | 几何与外观联合学习，相互增强 |

### 核心机制

**1. Perceiver IO 编码器：从无结构点云到动态 token**

Velox 采用 Perceiver IO 架构作为编码器，输入为无结构时空彩色点云 $\mathcal{X} = \{(\mathbf{x}_i \in \mathbb{R}^3, \mathbf{c}_i \in [0,1]^3, \tau_i \in \mathbb{R})\}_{i=1}^N$。编码器通过局部交叉注意力机制，将采样点作为查询，仅关注其最近邻的输入点，从而将高维时空点云压缩为一组紧凑的动态 token $\mathbf{s}$。这一设计的关键优势在于：**无需预先建立帧间对应关系**，编码器自动学习跨时间的关联结构。

**2. 互补双解码器：几何与外观的联合学习**

动态 token 通过两个互补的解码器进行监督训练：

- **4D 表面解码器**：基于流匹配范式，以动态 token 和时间戳为条件，估计速度场以将噪声点推向目标表面。损失函数为 $\mathcal{L}_V = \|\mathbf{v} - \dot{\alpha}_t \mathbf{x} - \dot{\sigma}_t \boldsymbol{\epsilon}\|^2$，直接监督时变几何的学习。
- **高斯解码器**：将动态 token 解码为 3D Gaussian 参数，通过可微渲染与新视角图像进行对比，损失为 $\mathcal{L}_{GS} = \|I_{GT} - \mathrm{Render}(G(\mathrm{Vox}, \mathbf{s}, \tau), \mathbf{H}_I)\|^2$。这使得 token 必须同时编码外观信息。

两个解码器的联合训练使得动态 token 成为**几何与外观的统一载体**，这是 Velox 区别于现有方法的核心洞察。

**3. 生成式扩展：在潜在空间直接生成 4D 内容**

基于动态 token 的紧凑性，Velox 进一步训练 DiT 生成模型，直接从输入图像/视频的 DinoV2 特征生成动态 token，实现视频到 4D 生成和布料模拟。这种“在潜在空间生成”的策略避免了直接在高维像素或点云空间建模的困难。

### 与基线方法的本质差异

- **vs. GVF（基于变形的 4D 表示）**：GVF 依赖变形场建模运动，在大运动或关节区域容易出现断裂；Velox 的流匹配解码器直接建模时变表面分布，对复杂变形更鲁棒。
- **vs. LiTo（逐帧 3D 表示）**：LiTo 逐帧独立编码，缺乏跨帧信息共享，导致外观一致性不足；Velox 的动态 token 联合编码整个序列，恢复的外观更忠实。
- **vs. L4GM（像素对齐高斯的视频到 4D）**：L4GM 依赖像素对齐和测试时优化，新视角泛化能力受限；Velox 在潜在空间生成，无需测试时对齐，新视角质量更高。

## 整体框架

Velox 的核心目标是学习一个紧凑、描述性强且易于访问的 4D 对象表示——**动态 token**。整个 pipeline 围绕三个关键环节构建：**编码**、**解码监督**与**下游适配**，如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/002_Figure_2.jpg]]
*Figure 2: Method. (a) We use a Perceiver IO encoder [32, 115] to map dynamic point clouds and queries to dynamic tokens. We train this representation with two decoders: the 4D surface decoder, which maps noisy input surface points to denoised points; and a Gaussian decoder, which maps from voxel centers to 3D Gaussian [37] parameters. (b) To train our models for video-to-4D and cloth simulation, we use a DiT [65] that directly generates 4D representations in the form of dynamic tokens conditioned on input image/video DinoV2 features. We can then use the Gaussian decoder to map the dynamic tokens to 3D Gaussians. (c) Conditioned on dynamic tokens calculated from an input RGBD video, we train a trackin...*

### 编码：从无结构时空点云到动态 token

给定一段动态对象的观测，输入被组织为无结构的时空彩色点云：

$$\mathcal{X} = \{ (\mathbf{x}_i \in \mathbb{R}^3, \mathbf{c}_i \in [0,1]^3, \tau_i \in \mathbb{R}) \}_{i=1}^N$$

其中 $\mathbf{x}_i$ 为空间坐标，$\mathbf{c}_i$ 为 RGB 颜色，$\tau_i$ 为时间戳。与传统 4D 方法不同，该输入**不要求任何时间对应关系**（如帧间点匹配或变形场标注），这直接消除了现有方法对昂贵标注的依赖。

编码器采用 **Perceiver IO** 架构：从输入点云 $\mathcal{X}$ 中采样 $k$ 个点作为查询（query），每个查询仅与 $\mathcal{X}$ 中距离最近的局部邻域点进行交叉注意力计算。这种局部交叉注意力机制使得编码器能够高效地将大规模时空点云压缩为一组固定大小的**动态 token** $\mathbf{s}$，同时保留时空结构信息。动态 token 的维度不随输入点云规模变化，构成了后续所有下游任务共享的潜在表示。

### 双解码器联合监督

为了确保动态 token 同时捕获几何和外观信息，Velox 使用两个互补的解码器进行联合训练：

- **4D 表面解码器**：基于条件流匹配（conditional flow matching）框架，以动态 token $\mathbf{s}$ 和时间 $\tau$ 为条件，学习从噪声分布到目标表面点云的条件概率路径。该解码器通过速度场监督损失训练：

  $$\mathcal{L}_V = \|\mathbf{v} - \dot{\alpha}_t \mathbf{x} - \dot{\sigma}_t \epsilon\|^2$$

  其中 $\mathbf{v}$ 为预测的速度向量，$\dot{\alpha}_t$ 和 $\dot{\sigma}_t$ 为流匹配路径的调度参数。该损失驱动动态 token 编码时间变化的表面几何。

- **高斯解码器**：将动态 token 解码为 3D Gaussian Splatting 参数，用于新视角图像渲染。解码过程首先从动态 token 预测**占据体素**（occupancy voxel），然后以体素中心为锚点生成各向异性 3D 高斯的属性（位置、协方差、颜色、不透明度）。图像重建损失为：

  $$\mathcal{L}_{GS} = \|I_{GT} - \mathrm{Render}(G(\mathrm{Vox}, \mathbf{s}, \tau), \mathbf{H}_I)\|^2$$

  其中 $G$ 为高斯参数预测网络，$\mathbf{H}_I$ 为目标视角的相机参数。体素解码器（Voxel decoder）的引入显著加速了高斯解码过程，同时消融实验表明使用解码器预测的体素可接近真实体素的重建性能（PSNR 35.11 vs 35.39）。

最终训练目标为三项损失的加权和：

$$\mathcal{L} = \mathcal{L}_V + \mathcal{L}_{GS} + \gamma \mathcal{L}_C$$

其中 $\mathcal{L}_C = \|\mathbf{s}\|^2$ 为对动态 token 的 KL 正则项（$\gamma = 10^{-4}$），等价于 L2 正则化，防止潜在空间过拟合。

### 下游任务适配

动态 token 作为统一的 4D 对象表示，可通过轻量级任务头适配多种下游任务：

- **视频到 4D 生成**：在动态 token 空间上训练一个 **DiT 扩散模型**，以输入图像/视频的 DinoV2 特征为条件，直接生成动态 token。随后通过高斯解码器将生成的 token 映射为可渲染的 3D 高斯序列。
- **3D 跟踪**：在冻结的动态 token 之上训练一个跟踪网络，给定首帧的 3D 查询点 $\mathbf{x}_0^i$，预测其在后续帧中的 3D 位置 $\mathbf{x}_j^i$。
- **布料模拟**：通过图像到 4D 的生成管线，从单帧初始图像预测布料的完整 4D 运动轨迹。

### 数据增广

为提升外观建模的泛化能力，Velox 在训练中对动态序列施加**随机纹理替换增广**（Figure 3），将原始纹理替换为随机纹理贴图。消融实验表明，该增广对重建外观质量有显著贡献（Ours-S w/o aug. PSNR 32.41 vs w/ aug. 33.93），因为未增广的动态数据集中纹理多样性不足以捕获高频细节。

## 核心模块与公式推导

Velox 的核心架构由三个紧密协作的模块构成：**Perceiver IO 编码器**、**4D 表面解码器**和**高斯解码器**，三者通过一组**动态 token** 实现信息压缩与传递。

### 编码器：从无结构点云到动态 token

编码器接收的输入是无结构的时空彩色点云，形式化为：

$$
\mathcal{X} = \{ (\mathbf{x}_i \in \mathbb{R}^3, \mathbf{c}_i \in [0,1]^3, \tau_i \in \mathbb{R}) \}_{i=1}^{N}
$$

其中 $\mathbf{x}_i$ 为空间坐标，$\mathbf{c}_i$ 为 RGB 颜色，$\tau_i$ 为时间戳。编码器采用 **Perceiver IO** 架构，从输入点云中采样 $k$ 个点作为查询（queries），这些查询仅与 $\mathcal{X}$ 中空间距离最近的邻域点进行局部交叉注意力计算，从而将高维时空点云压缩为一组紧凑的**动态 token** $\mathbf{s}$。这一设计的关键优势在于：无需预先建立帧间的时间对应关系，编码器直接从原始时空数据中学习联合表示。

### 4D 表面解码器：流匹配驱动的几何建模

4D 表面解码器以动态 token $\mathbf{s}$ 和时间 $\tau$ 为条件，通过**条件流匹配**框架建模时变表面分布。给定带噪表面点 $\mathbf{x}$ 和噪声 $\epsilon$，解码器预测速度向量 $\mathbf{v}$，其监督损失为：

$$
\mathcal{L}_{V} = \| \mathbf{v} - \dot{\alpha}_t \mathbf{x} - \dot{\sigma}_t \epsilon \|^2
$$

其中 $\dot{\alpha}_t$ 和 $\dot{\sigma}_t$ 为流匹配路径的系数导数。该损失驱动解码器学习从噪声分布到目标表面几何的条件概率路径，使动态 token 必须编码精确的时空几何信息。

### 高斯解码器：基于体素的外观建模

高斯解码器将动态 token 解码为 3D Gaussian 参数，用于新视角图像渲染。为加速解码，模型首先从动态 token 预测**占据体素**（voxel），再以体素中心为锚点生成各高斯原语的属性（位置、协方差、颜色、不透明度）。渲染损失为：

$$
\mathcal{L}_{GS} = \| I_{GT} - \mathrm{Render}(G(\mathrm{Vox}, \mathbf{s}, \tau), \mathbf{H}_I) \|^2
$$

其中 $G(\cdot)$ 为高斯参数预测函数，$\mathbf{H}_I$ 为目标视角的相机参数。该损失强制动态 token 同时捕获外观信息，与表面解码器形成互补监督。

### 联合训练目标

最终训练损失为三项的加权组合：

$$
\mathcal{L} = \mathcal{L}_{V} + \mathcal{L}_{GS} + \gamma \mathcal{L}_{C}
$$

其中正则项 $\mathcal{L}_{C} = \|\mathbf{s}\|^2$ 为动态 token 的 L2 正则（等价于 KL 散度正则），权重 $\gamma = 10^{-4}$。这一联合目标使得同一组动态 token 能够同时支撑几何重建与外观渲染，形成紧凑且描述性强的 4D 对象表示。

**需要人工核实**：公式中流匹配路径的具体形式（$\alpha_t$、$\sigma_t$ 的定义）在提供的分析材料中未完整展开，建议查阅原文 Section 3 确认其与标准 Flow Matching 框架的对应关系。

### 补充图表

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/021_Figure_11.jpg]]
*Figure 11: Real-world generation. We mask out real-world videos for the object of interest, and generate video-conditioned 4D objects*

## 实验与分析

### 核心实验设置

Velox 的训练数据基于 Objaverse 动态序列，每条序列包含 25 帧时空彩色点云。编码器采用 Perceiver IO 架构，以局部交叉注意力将输入压缩为一组动态 token。训练目标由三部分构成：4D 表面解码器的流匹配速度监督损失 $\mathcal{L}_V$、高斯解码器的图像重建损失 $\mathcal{L}_{GS}$，以及动态 token 的 L2 正则项 $\mathcal{L}_C$（权重 $\gamma = 10^{-4}$）。纹理增广策略（Figure 3）通过随机替换物体纹理显著提升了外观多样性，是获得高质量外观重建的关键因素。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/003_Figure_3.jpg]]
*Figure 3: Texture augmentations. We augment training sequences with random textures, increasing appearance diversity. Asset credit: [87]*

### 4D 重建评估

Table 1 报告了在 Objaverse 256 个场景上的重建质量对比。Velox 在使用 GT 体素时取得 **PSNR 35.39、SSIM 0.984、LPIPS 0.021、FVD 48.99**，全面超越基线方法：GVF 的 PSNR 仅为 26.45，LiTo 为 32.55。即使使用解码器预测的体素（dec. vox.），Velox 仍达到 PSNR 35.11，接近 GT 体素性能，且推理速度远快于点采样法。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/005_Table_1.jpg]]
*Table 1: Reconstruction evaluation. Reconstruction quality across methods, including different voxelization methods for our Gaussian decoder. Chamfer values are multiplied by 105*

定性对比（Figure 4）揭示了两项关键优势：在大运动区域，GVF 基于变形的高斯方法难以准确建模，而 Velox 的流匹配解码器能稳定恢复几何；在关节建模区域，LiTo 逐帧独立处理导致外观不一致，Velox 通过跨时间联合建模保持了外观的时空连贯性。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/004_Figure_4.jpg]]
*Figure 4: Reconstruction results. Black inset: Our approach outperforms GVF [117], especially on areas with bigger movements, where deforming Gaussians proves challenging. Blue inset: Furthermore, due to jointly modeling the object across time, we recover more faithful appearance than the single frame-based LiTo [11]. Asset credit [58]*

消融实验（Table 1）进一步表明：去除纹理增广后，Ours-S 的 PSNR 从 33.93 降至 32.41，外观重建明显退化，说明增广策略对学习高频纹理至关重要。动态 token 数量消融（Table 10）显示，token 数从 4096 增至 16384 时，Chamfer 距离和 LPIPS 持续改善，但推理时间相应增加，呈现质量-效率的权衡。

### 3D 跟踪评估

在 Objaverse 3D 跟踪任务上（Table 2），Velox 取得了 $L_{2,\text{all}}^{3D}$ 为 **0.025**，显著优于 SpatialTrackerV2（0.068）和 CoTracker3（0.097）。值得注意的是，基线方法在过滤场景边界外点后指标大幅改善，而 Velox 在过滤前后均保持稳定优势，表明其跟踪结果更少依赖后处理修正。在真实数据 TAPVid-Panoptic 上（Table 9），Velox 同样取得最佳综合性能，验证了动态 token 表示在真实场景下的泛化能力。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/006_Table_2.jpg]]
*Table 2: Objaverse 3D tracking evaluation. For*

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/018_Table_9.jpg]]
*Table 9: 3D tracking metrics on real data from TAPVid-Panoptic [39]. Our method achieves the best overall performance across all reported metrics*

### 视频到 4D 生成评估

Table 3 报告了在 Objaverse 和 Consistent4D 两个数据集上的视频到 4D 生成指标。在随机相机距离设置下，Velox 的新视角 PSNR 达到 **20.62 ± 6.04**，LPIPS 为 **0.104 ± 0.052**，均优于 L4GM（PSNR 18.30，LPIPS 0.146）。L4GM 虽能忠实重建输入视图（得益于其像素对齐高斯和测试时对齐），但在新视角下出现明显的漂浮伪影（Figure 5）。GVF 则在复杂形变区域泛化失败，无法同时保持输入与新视角的保真度。Velox 通过直接在动态 token 空间生成，避免了逐帧对齐的局限，在输入视图和新视角上均取得更平衡的质量。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/008_Table_3.jpg]]
*Table 3: Video-to-4D generation evaluation. For quantitative metrics, we render the generated 4D objects from 10 viewpoints. We report separate metrics for the input and 9 novel viewpoints on Consistent4D [33] (C4D) and 128 test objects in Objaverse [17] (Obj). The input video is rendered from random distance to the origin (r ∈ [2, 5]) with a paired field of view to cover the entire object*

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/007_Figure_5.jpg]]
*Figure 5: Video-to-4D results. 2nd row: GVF [117] fails to generalize across complex shape deformations, and does not faithfully reproduce both input and novel views. 3rd row: L4GM renders the input view faithfully due to its pixel-based Gaussian formulation and test-time alignment. However, it fails to generate realistic novel views, with visible floaters around the object. Bottom row: Our method recovers both accurate input views and novel view generations, even for complex structures like the bird (RHS). Asset credit [64, 111]*

ODE 积分步数消融（Table 8）表明，即使使用较少步数，Velox 仍优于 L4GM 和 GVF，说明动态 token 空间本身具有更好的生成效率。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/015_Table_8.jpg]]
*Table 8: Video-to-4D generation evaluation. For quantitative metrics, we render the generated 4D objects from 10 viewpoints. We report separate metrics for the input and 9 novel viewpoints on Consistent4D [33] (C4D) and 128 test objects in Objaverse [17] (Obj). The input video is rendered from random distance to the origin (r ∈ [2, 5]) with a paired field of view to cover the entire object*

### 布料模拟评估

在布料模拟任务上（Figure 7），Velox 的图像到 4D 管线能够从单帧初始图像生成完整的 4D 轨迹。对质心点的位置、速度和加速度分析显示，生成轨迹呈现出符合物理规律的加速下落和触地反弹行为（$\tau \approx 0.5$ 时刻），与参考轨迹的动力学特征高度一致。Table 12 报告了生成指标评估，但作者跳过了 FVD，因为数据分布与 InceptionI3D 特征模型的训练分布差异过大。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/010_Figure_7.jpg]]
*Figure 7: Cloth simulation results. (b) Our generative model predicts the full 4D trajectory of a cloth from an initial position (Top right: input frame). (c) Position, velocity, and acceleration (acc) of the center-of-mass point (marked in (a) and (b)) along the negative y axis, plotted against time. Both the generated and reference trajectories show an initial acceleration toward the ground followed by an upward rebound after impact at τ ≈ 0.5*

### 失败模式分析

尽管 Velox 在多项任务上取得领先，论文明确指出了以下局限：

1. **时间不一致性闪烁**：高斯解码器逐帧独立运行，缺乏跨帧约束，导致在复杂纹理或大运动区域可能出现残余闪烁。这源于解码器架构的内存限制，无法同时处理多帧高斯参数。

2. **高频纹理退化**：在视频到 4D 生成中，当输入视频包含高频细节时，生成纹理质量可能下降。这受限于 DiT 生成模型的容量，且缺乏大规模 4D 基础模型初始化进一步加剧了该问题。

3. **计算开销**：训练动态 token 需要大量计算资源（Table 6 列出了各模型规模与训练细节），目前缺乏可用的 4D 预训练权重来降低训练成本。

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2605_04527/figures/013_Table_6.jpg]]
*Table 6: Model size and training details. The table overviews architecture and training details about individual models*

### 跨数据集泛化

Table 11 展示了 Velox（仅在 Objaverse 上训练）在 PokeFlex 数据集上的重建性能，初步验证了动态 token 的跨数据集迁移能力。值得注意的是，GVF 因缺少时间对应关系而无法应用于 PokeFlex，凸显了 Velox 无需时间对应的输入灵活性优势。

## 方法谱系与知识库定位

### 与现有方法的谱系关系

Velox 的提出直接回应了当前 4D 对象表示领域的两类核心瓶颈：**基于变形的方法**需要难以获取的时间对应关系，而**逐帧 3D 表示方法**则忽略时间维度的联合建模，导致外观描述不足或下游任务泛化受限。

**与基于变形的方法对比。** **GVF** 等变形场方法在 4D 重建中依赖显式的帧间对应关系来驱动高斯变形，这在大运动或关节区域（如鸟类展翅、人物奔跑）容易出现几何撕裂和外观模糊。Velox 通过 Perceiver IO 编码器直接处理无结构时空彩色点云（式 $\mathcal{X} = \{ (\mathbf{x}_i \in \mathbb{R}^3, \mathbf{c}_i \in [0,1]^3, \tau_i \in \mathbb{R}) \}_{i=1}^N$），将跨帧信息压缩为一组动态 token，从根本上规避了时间对应关系的依赖。定量上，在 Objaverse 重建任务中，Velox 的 PSNR 达到 35.39，比 GVF 的 26.45 高出 8.94 dB（Table 1）；定性上，在大运动区域的优势尤为显著（Figure 4 黑色标注）。

**与逐帧表示方法的对比。** **LiTo** 作为逐帧 3D 表示方法，每帧独立编码隐变量，缺乏跨帧信息交互，导致外观重建的时序一致性不足。Velox 通过联合训练 4D 表面解码器（流匹配）和高斯解码器，使动态 token 同时捕获几何和外观的时序演化，从而在重建外观上更忠实于原始序列（Figure 4 蓝色标注）。为公平比较，作者对 LiTo 进行了微调，使其每帧隐变量总数与 Velox 匹配。

**与像素对齐生成方法的对比。** 在视频到 4D 生成任务中，**L4GM** 采用像素对齐的高斯表示，能够忠实渲染输入视图，但在新视角生成时容易出现“漂浮物”（floaters）伪影，且需要测试时方位角搜索优化。Velox 则直接在动态 token 空间进行扩散生成（使用 DiT 架构），无需测试时优化，在新视角 PSNR 上达到 20.62 ± 6.04，优于 L4GM 的 18.30 ± 4.85（Table 3）。

**与 3D 跟踪方法的对比。** 在 3D 跟踪任务中，**SpatialTrackerV2** 和 **CoTracker3**（2D 跟踪投影到 3D）在场景边界外点较多时性能下降明显。Velox 的跟踪网络以动态 token 为条件，直接预测查询点在后续帧的 3D 位置，在 $L_{2, \text{all}}^{3D}$ 指标上达到 0.025，远低于 SpatialTrackerV2 的 0.068（Table 2）。即使对基线进行边界过滤后处理，Velox 仍保持优势。

### 适用边界与局限

尽管 Velox 在多个任务上展现了统一的表示能力，其适用边界和局限值得明确：

1. **时序闪烁问题。** 高斯解码器逐帧独立运行，缺乏跨帧约束，在复杂纹理或大运动区域可能存在残余闪烁。这是当前解码器架构的固有局限，而非动态 token 表示本身的问题。

2. **高频纹理生成的退化。** 在视频到 4D 生成中，当输入视频包含高频细节时，生成纹理质量可能下降。这受限于 DiT 生成模型的容量和训练数据规模，而非表示框架的理论上限。

3. **训练计算开销。** 动态 token 的训练需要大量计算资源和时间，目前缺乏大规模 4D 基础模型初始化，增加了训练成本。消融实验表明，增加 token 数量（从 4096 到 16384）持续改善 Chamfer 和 LPIPS，但推理时间相应增加（Table 10）。

4. **真实场景泛化。** 尽管在 PokeFlex 数据集上展示了跨数据集的重建能力（Table 11），且 GVF 因缺少时间对应关系无法应用于该数据集，但更广泛的真实场景测试仍有待探索。真实世界视频到 4D 生成的初步结果见 Figure 11，但系统性的真实数据评估尚不充分。

### 开放问题

1. **内存高效的多帧解码器。** 如何设计能够同时处理多帧高斯参数的解码器，以引入跨帧一致性约束，减少时序闪烁？

2. **高频纹理生成的改进。** 能否通过更大的生成模型、多阶段细化或超分辨率策略来改进视频到 4D 生成中的高频纹理细节？

3. **大规模预训练与训练效率。** 如何降低训练计算成本？能否利用大规模 4D 预训练模型进行初始化，类似 2D 基础模型在视觉任务中的作用？

4. **复杂场景扩展。** 动态 token 目前针对单个对象设计，能否扩展用于多对象交互场景或更大规模的环境表示？这需要解决 token 分配、对象间交互建模和计算可扩展性等挑战。

5. **真实场景鲁棒性验证。** 在更广泛的真实数据（如野外视频、遮挡场景、光照变化）上的泛化能力需要系统评估，以确定动态 token 表示在实际部署中的可靠性边界。

## 原文 PDF

![[paperPDFs/CVPR_2026/Velox_Learning_Representations_of_4D_Geometry_and_Appearance.pdf]]