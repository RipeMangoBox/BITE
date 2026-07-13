---
title: Structured 3D Latents for Scalable and Versatile 3D Generation
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Structured_3D_Latents_for_Scalable_and_Versatile_3D_Generation.pdf
project_link: null
code_link: https://github.com/Microsoft/TRELLIS
aliases:
- TRELLIS
- SLAT
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用结构化稀疏潜在表示（SLAT），将粗粒度的几何结构（活跃体素）与细粒度的视觉特征（DINOv2多视图特征）解耦，并采用两阶段修正流变换器生成流程，从而在多种输出格式下实现高保真3D生成。
primary_logic: 通过将稀疏体素结构所携带的显式几何位置与预训练视觉编码器提取的稠密多视图特征相结合，SLAT以表征无关的方式同时捕捉几何和外观信息，使得统一生成框架能够通过不同解码器输出多种高质量3D表示，并支持灵活编辑。
claims:
- SLAT在重建保真度上全面超越所有基线方法，其PSNR达到32.74，CD仅0.0083，F-score达0.9999，表明该潜在表示能同时保留高质量外观和几何。
- 在Toys4k上的生成评估中，本文方法在文本到3D和图像到3D任务的所有指标（CLIP, FD, KD）上均显著优于现有方法，特别是FD_dinov2较最佳基线降低约48%。
- 消融实验证实，将潜在空间从32³升级到64³带来重建PSNR的明显跃升（31.85→32.74），验证了高分辨率结构对细节捕捉的重要性。
- 替换扩散模型为修正流模型可在两个生成阶段独立提升CLIP和FD指标，证明了修正流模型在3D生成任务中的优越性。
---

# Structured 3D Latents for Scalable and Versatile 3D Generation

> [!tip] 核心洞察
> 通过将稀疏体素结构所携带的显式几何位置与预训练视觉编码器提取的稠密多视图特征相结合，SLAT以表征无关的方式同时捕捉几何和外观信息，使得统一生成框架能够通过不同解码器输出多种高质量3D表示，并支持灵活编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向可扩展且多功能3D生成的结构化3D潜变量 |
| 英文题名 | Structured 3D Latents for Scalable and Versatile 3D Generation |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2412.01506) · [Code](https://github.com/Microsoft/TRELLIS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TRELLIS (Structured 3D Latents aka SLAT) |
| Dataset | Toys4k reconstruction subset, Toys4k text-to-3D generation, Toys4k image-to-3D generation |

> [!tip] 效果简介
> - Toys4k reconstruction subset (500 instances) 上，PSNR 32.74 (GS) / 32.19 (RF) vs LN3Diff 26.44; CLAY N/A (geometry-only) (>6 dB improvement)。
> - Toys4k reconstruction subset 上，CD 0.0083 vs CLAY 0.0124 (0.0041 lower (better))。
> - Toys4k text-to-3D generation (1250 prompts) 上，CLIP score 26.70 (Ours XL) vs InstantMesh 25.56 (1.14 improvement)。

## 概要

3D内容生成领域长期受到**缺乏统一潜在表示**的困扰：现有方法难以在单一框架下同时处理高质量的几何与外观，且输出格式固定，无法在网格、辐射场与3D高斯溅射等表示之间灵活切换。这导致通用3D生成范式的发展受限——不同方法各自为战，缺乏可复用的表征基础。

本文提出**TRELLIS**，其核心是**结构化稀疏潜在表示SLAT**（Structured Latents）。SLAT将粗粒度的几何结构（活跃体素网格）与细粒度的视觉特征（从DINOv2多视图特征聚合而来）解耦，以表征无关的方式同时捕捉几何和外观信息。这一设计使得统一的生成框架能够通过不同解码器输出多种高质量3D表示，并支持灵活的3D编辑。

在生成范式上，TRELLIS采用**两阶段修正流变换器**：首先生成稀疏体素结构，再在其上生成局部潜变量，最终由特定解码器转换为目标3D表示。该方法在重建保真度上全面超越基线——PSNR达32.74，倒角距离（CD）仅0.0083，F-score达0.9999（Table 1）。在Toys4k基准上，文本到3D和图像到3D生成任务的所有指标均显著优于现有方法，其中FD_dinov2较最佳基线降低约48%（Table 2）。用户研究进一步验证了其优势：文本到3D和图像到3D任务分别获得67.1%和94.5%的优选率（Table 9）。

**方法定位：** TRELLIS属于3D生成式模型中的**潜在表示方法**，但其结构化稀疏设计区别于LN3Diff的潜在三平面、3DTopia-XL的潜在点云和CLAY的潜在向量集。它通过引入预训练视觉特征与修正流生成范式，在表征通用性和生成质量之间建立了新的平衡点。

高质量3D资产的自动生成是计算机图形学与视觉领域的核心挑战之一，其应用覆盖虚拟现实、游戏开发、影视制作和具身智能等多个领域。近年来，随着扩散模型和可微渲染技术的进步，3D生成取得了显著进展，但现有方法仍面临一个根本性瓶颈：**缺乏统一的潜在表示**，难以同时处理高质量的几何和外观，并且无法在不同输出格式（如网格、辐射场、3D高斯）间灵活切换。

具体而言，当前主流方法在潜在空间设计上存在以下结构性缺口：

- **表示割裂**：基于隐式三平面（triplane）的 **LN3Diff**、基于潜在点云的 **3DTopia-XL**、以及基于潜在向量集的 **CLAY** 等方法，分别针对特定输出格式优化，其潜在空间无法在不同3D表示间迁移。**CLAY** 仅支持几何生成，不包含外观信息。
- **直接生成方法的局限**：**Shap-E** 等端到端方法直接生成3D表示，但生成质量受限于模型容量和训练数据规模；**LGM**、**InstantMesh** 等基于2D提升（2D-lifting）的方法依赖多视图扩散模型，难以保证3D一致性。
- **统一范式的缺失**：现有方法无法在单一框架内同时输出3D高斯、辐射场和网格等多种表示，限制了通用3D生成范式的发展。

上述问题的根源在于：**几何结构（占据空间的位置信息）与视觉外观（多视图一致的纹理和光照特征）在现有潜在空间中被耦合或丢失**。粗粒度的几何先验（如稀疏体素）能提供显式的位置约束，而预训练视觉编码器（如DINOv2）提取的稠密多视图特征则携带丰富的语义和纹理信息——如何将二者解耦并有效融合，是构建统一3D潜在表示的关键。

本文提出 **TRELLIS**，其核心动机是设计一种**结构化稀疏潜在表示（Structured Latents, SLAT）**，将粗粒度几何结构（活跃体素）与细粒度视觉特征（DINOv2多视图特征）解耦，并采用两阶段修正流变换器生成流程，从而在多种输出格式下实现高保真3D生成。该方法以表征无关的方式同时捕捉几何和外观信息，使得统一生成框架能够通过不同解码器输出多种高质量3D表示，并支持灵活编辑。

## 核心方法与创新机理

本工作提出了 **TRELLIS**，其核心创新在于引入一种名为 **SLAT (Structured Latents)** 的统一结构化稀疏潜在表示，并配套设计了一套两阶段修正流变换器生成流程，从而在单一框架内实现了高质量、多格式、可编辑的3D资产生成。

### 1. 结构化稀疏潜在表示 (SLAT)

现有3D生成方法通常依赖于特定的潜在表示，如 **LN3Diff** 的潜在三平面、**3DTopia-XL** 的潜在点云或 **CLAY** 的潜在向量集，这些表示在几何与外观的联合建模以及输出格式的灵活性上存在固有局限。SLAT 通过将粗粒度几何结构与细粒度视觉特征解耦，打破了这一瓶颈。

具体而言，SLAT 将3D资产表示为一组定义在稀疏3D网格活跃体素上的局部潜变量：
$$z = \{ (z_i, p_i) \}_{i=1}^{L}, \quad z_i \in \mathbb{R}^C, p_i \in \{0,1,\dots,N-1\}^3$$
其中，活跃体素位置 $p_i$ 勾勒出物体的粗略几何结构，而局部潜变量 $z_i$ 则编码了该位置周边的细粒度外观与形状信息。这些潜变量是通过聚合并处理预训练 **DINOv2** 编码器从稠密多视图渲染中提取的视觉特征而获得的，从而以表征无关的方式同时捕捉了几何和外观。

### 2. 表征无关的多格式解码

与只能输出单一格式（如仅网格或仅辐射场）的先前方法不同，SLAT 作为一种通用潜在表示，可以通过不同的解码器头部分别解码为多种主流3D表征，实现了“一次编码，多种输出”的灵活性：
- **3D高斯 (3D Gaussians)**：每个潜变量解码为 $K$ 个带有位置偏移、颜色、尺度、不透明度和旋转参数的3D高斯。
  $$\mathcal{D}_{\mathrm{GS}} : \{ (z_i, p_i) \}_{i=1}^{L} \to \{ \{ (o_i^k, c_i^k, s_i^k, \alpha_i^k, r_i^k) \}_{k=1}^{K} \}_{i=1}^{L}$$
- **辐射场 (Radiance Fields)**：解码为局部辐射体素的CP分解向量，用于重构 $8^3$ 的辐射场体积。
  $$\mathcal{D}_{\mathrm{RF}} : \{ (z_i, p_i) \}_{i=1}^{L} \to \{ (v_i^{\mathrm{x}}, v_i^{\mathrm{y}}, v_i^{\mathrm{z}}, v_i^{\mathrm{c}}) \}_{i=1}^{L}$$
- **网格 (Meshes)**：解码为 **Flexi-Cubes** 参数和有符号距离值，随后上采样并提取网格。
  $$\mathcal{D}_{\mathrm{M}} : \{ (z_i, p_i) \}_{i=1}^{L} \to \{ \{ (w_i^j, d_i^j) \}_{j=1}^{64} \}_{i=1}^{L}$$

### 3. 两阶段修正流生成范式

在生成范式上，本工作摒弃了主流的扩散模型（Diffusion）或GAN，转而采用**修正流变换器 (Rectified Flow Transformers)** 并设计了专门的两阶段生成流程：
1. **稀疏结构生成 (Stage 1)**：首先生成由VAE压缩的稠密二值网格所表示的粗粒度活跃体素结构，该阶段使用一个以文本/图像为条件的变换器。
2. **结构化潜变量生成 (Stage 2)**：在已生成的稀疏结构基础上，利用一个结合稀疏卷积的变换器，以结构和提示词为条件，生成附着于活跃体素的局部潜变量。

修正流模型的训练目标为匹配从噪声指向数据的直线路径：
$$\mathcal{L}_{CFM}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \epsilon} \lVert \mathbf{v}_{\theta}(\mathbf{x}, t) - (\epsilon - \mathbf{x}_0) \rVert_2^2$$

消融实验证实，将扩散模型替换为修正流模型可在两个生成阶段独立提升CLIP和FD指标，验证了这一范式转变的优越性（Table 4）。此外，这一两阶段设计天然支持灵活的3D编辑，例如通过固定结构生成资产变体，或通过适配 **Repaint** 策略实现无微调的区域特定编辑。

TRELLIS 的整体 pipeline 围绕 **结构化稀疏潜在表示（SLAT）** 构建，形成“编码—生成—解码”三阶段流程。其核心设计思想是将粗粒度的几何结构（活跃体素）与细粒度的视觉特征（局部潜变量）解耦，使统一的生成框架能够通过不同解码器输出多种 3D 表示。

### 模块关系与数据流

**1. 编码阶段（Encoding）**

给定一个 3D 资产 $O$，首先从球面上随机采样相机视角进行稠密多视图渲染，并利用预训练的 DINOv2 编码器提取特征图。随后，通过特征聚合与稀疏 VAE 编码器，将多视图视觉特征融合并映射为一组定义在稀疏 3D 网格活跃体素上的局部潜变量：

$$z = \{ (z_i, p_i) \}_{i=1}^{L}, \quad z_i \in \mathbb{R}^C, p_i \in \{0,1,\dots,N-1\}^3$$

其中 $p_i$ 表示活跃体素的位置（粗粒度几何结构），$z_i$ 为附着于该位置的局部潜变量（细粒度外观与形状细节）。编码器采用带有移位窗口注意力（Shifted Window Attention）的变换器架构，端到端地使用 3D Gaussians 进行训练，以保证高保真度和计算效率。

**2. 生成阶段（Generation）**

生成过程采用**两阶段修正流变换器**流水线：

- **第一阶段：稀疏结构生成（Sparse Structure Generation）**。将稠密二值体素网格经 VAE 压缩后，利用条件修正流变换器生成粗粒度的活跃体素布局。该变换器以文本或图像提示为条件，输出物体的宏观几何占位结构。

- **第二阶段：结构化潜变量生成（Structured Latents Generation）**。在第一阶段生成的稀疏结构基础上，利用带稀疏卷积的变换器为每个活跃体素生成对应的局部潜变量 $z_i$。该阶段同样以提示和已生成的结构为条件，填充细粒度的外观与几何信息。

两阶段均采用修正流（Rectified Flow）模型，其训练目标为：

$$\mathcal{L}_{CFM}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \epsilon} \lVert \mathbf{v}_{\theta}(\mathbf{x}, t) - (\epsilon - \mathbf{x}_0) \rVert_2^2$$

即让模型预测的向量场匹配从噪声 $\epsilon$ 指向数据 $\mathbf{x}_0$ 的直线路径。

**3. 解码阶段（Decoding）**

生成的 SLAT 可通过三种专用解码器转换为不同的 3D 表示，解码器共享主干架构，仅在输出层有所差异：

- **3D Gaussians 解码器**：将每个潜变量 $z_i$ 解码为 $K$ 个 3D 高斯，包含位置偏移、颜色、尺度、不透明度和旋转参数：
  $$\mathcal{D}_{\mathrm{GS}} : \{ (z_i, p_i) \}_{i=1}^{L} \to \{ \{ (o_i^k, c_i^k, s_i^k, \alpha_i^k, r_i^k) \}_{k=1}^{K} \}_{i=1}^{L}$$

- **辐射场（Radiance Fields）解码器**：解码为局部辐射体素的 CP 分解向量，用于重构 $8^3$ 的辐射场体积：
  $$\mathcal{D}_{\mathrm{RF}} : \{ (z_i, p_i) \}_{i=1}^{L} \to \{ (v_i^{\mathrm{x}}, v_i^{\mathrm{y}}, v_i^{\mathrm{z}}, v_i^{\mathrm{c}}) \}_{i=1}^{L}$$

- **网格（Meshes）解码器**：解码为 Flexi-Cubes 参数和有符号距离值，随后上采样至 $256^3$ 并通过 Marching Cubes 提取网格：
  $$\mathcal{D}_{\mathrm{M}} : \{ (z_i, p_i) \}_{i=1}^{L} \to \{ \{ (w_i^j, d_i^j) \}_{j=1}^{64} \}_{i=1}^{L}$$

### 关键设计决策

默认 SLAT 分辨率设为 $64^3$。消融实验证实，将分辨率从 $32^3$ 提升至 $64^3$ 使重建 PSNR 从 31.85 跃升至 32.74（Table 3），表明更高空间分辨率对细节捕捉至关重要。此外，用修正流模型替换扩散模型可在两个生成阶段独立提升 CLIP 和 FD_dinov2 指标（Table 4），验证了修正流在 3D 生成任务中的优越性。

整个框架的输入为文本提示或单张图像，输出可在约 10 秒内生成高质量的 3D Gaussians、辐射场或网格表示，并支持区域特定的无调参编辑（基于 Repaint 方法适配到两阶段流水线）。

### 3.1 结构化潜在表示 (SLAT)

TRELLIS 的核心在于提出一种统一的**结构化稀疏潜在表示**（Structured Latents, SLAT），将3D资产的几何与外观信息编码为一组定义在稀疏3D网格上的局部潜变量。其形式化定义为：

$$z = \{ (z_i, p_i) \}_{i=1}^{L}, \quad z_i \in \mathbb{R}^C, p_i \in \{0,1,\dots,N-1\}^3$$

其中 $p_i$ 表示活跃体素在 $N^3$ 网格中的整数坐标，勾勒出物体的粗粒度几何结构；$z_i$ 是附着在该位置上的 $C$ 维局部潜变量，承载细粒度的外观与形状信息。这种将**显式几何位置**与**稠密视觉特征**解耦的设计，使得同一潜在表示可被不同解码器转换为多种3D输出格式（3D高斯、辐射场、网格），构成了表征无关的生成基础。

### 3.2 编码器：多视图特征聚合与稀疏VAE

编码器将3D资产转化为SLAT的关键流程包含两个阶段：

1. **多视图特征提取与聚合**：对每个3D资产，从球面上随机采样相机视角渲染密集多视图图像，使用预训练的DINOv2编码器提取特征图。对于每个活跃体素 $p_i$，通过反投影将其映射到各视图的特征图上，聚合得到该体素的初始视觉特征 $f_i$。

2. **稀疏Transformer处理**：将聚合后的体素特征序列 $\{f_i\}$ 送入一个采用**移位窗口注意力**（Shifted Window Attention）的Transformer进行上下文增强，最终输出压缩后的局部潜变量 $z_i$。这一过程通过端到端训练完成，训练时使用3D高斯表示以获得高保真度和高效率。

### 3.3 解码器：多表示输出

SLAT通过三个独立解码器支持多种3D表示的无缝切换：

- **3D高斯解码**：每个潜变量 $z_i$ 被解码为 $K$ 个3D高斯原语，包含位置偏移、颜色、尺度、不透明度和旋转参数：
  $$\mathcal{D}_{\mathrm{GS}} : \{ (z_i, p_i) \}_{i=1}^{L} \to \{ \{ (o_i^k, c_i^k, s_i^k, \alpha_i^k, r_i^k) \}_{k=1}^{K} \}_{i=1}^{L}$$

- **辐射场解码**：将潜变量解码为局部辐射体素的CP分解向量，重构 $8^3$ 的辐射场体积：
  $$\mathcal{D}_{\mathrm{RF}} : \{ (z_i, p_i) \}_{i=1}^{L} \to \{ (v_i^{\mathrm{x}}, v_i^{\mathrm{y}}, v_i^{\mathrm{z}}, v_i^{\mathrm{c}}) \}_{i=1}^{L}$$

- **网格解码**：解码为Flexi-Cubes参数和有符号距离值，随后上采样至 $256^3$ 并通过Marching Cubes提取网格：
  $$\mathcal{D}_{\mathrm{M}} : \{ (z_i, p_i) \}_{i=1}^{L} \to \{ \{ (w_i^j, d_i^j) \}_{j=1}^{64} \}_{i=1}^{L}$$
  网格解码器的训练损失由几何损失、颜色损失和正则化项组合而成：
  $$\mathcal{L}_{\mathrm{M}} = \mathcal{L}_{\mathrm{geo}} + 0.1\mathcal{L}_{\mathrm{color}} + \mathcal{L}_{\mathrm{reg}}$$

### 3.4 两阶段修正流生成

生成过程采用两阶段修正流变换器（Rectified Flow Transformers），将生成任务分解为从粗到细的级联过程：

- **阶段一：稀疏结构生成**。首先生成表示粗粒度几何的稀疏体素网格。该阶段使用VAE压缩的稠密二值网格作为训练目标，通过一个条件于文本/图像提示的变换器进行生成。

- **阶段二：结构化潜变量生成**。在已生成的稀疏结构基础上，为每个活跃体素生成对应的局部潜变量 $z_i$。该阶段使用结合稀疏卷积的变换器，同时条件于结构信息和输入提示。

两阶段均采用**条件流匹配**（Conditional Flow Matching）目标进行训练，使模型预测的向量场匹配从噪声 $\epsilon$ 指向数据 $\mathbf{x}_0$ 的直线路径：

$$\mathcal{L}_{CFM}(\theta) = \mathbb{E}_{t, \mathbf{x}_0, \epsilon} \lVert \mathbf{v}_{\theta}(\mathbf{x}, t) - (\epsilon - \mathbf{x}_0) \rVert_2^2$$

消融实验证实，将扩散模型替换为修正流模型可在两个阶段独立提升CLIP和FD_dinov2指标（Table 4），验证了修正流在3D生成任务中的优越性。

![[assets/figures/papers/Structured_3D_Latents_for_Scalable_and_Versatile_3D_Generation_9feedf5ea34b/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. Encoding & Decoding: We adopt a structured latent representation (SLAT) for 3D assets encoding, which defines local latents on a sparse 3D grid to represent both geometry and appearance information. It is encoded from the 3D assets by fusing and processing dense multiview visual features extracted from a DINOv2 encoder, and can be decoded into versatile output representations with different decoders. Generation: Two specialized rectified flow transformers are utilized to generate SLAT, one for the sparse structure and the other for local latents attached to it*

![[assets/figures/papers/Structured_3D_Latents_for_Scalable_and_Versatile_3D_Generation_9feedf5ea34b/figures/006_Figure_5.jpg]]
*Figure 5: Visual comparisons of generated 3D assets between our method and previous approaches, given AI-generated prompts*

## 实验与关键发现

### 核心实验设置

实验基于约50万个高质量3D资产进行训练，数据源自Objaverse-XL、ABO、3D-FUTURE和HSSD四个公开数据集。每个资产渲染150张多视图图像，并使用GPT-4o生成文本描述。评估采用Toys4k基准，该数据集完全未在训练集中出现，且所有基线方法也未使用该数据训练，保证了评估的独立性。

### 重建保真度：潜在表示质量验证

Table 1呈现了不同潜在表示的重建保真度对比。SLAT在64³分辨率下实现了PSNR 32.74（3D Gaussians输出）和32.19（Radiance Fields输出），较LN3Diff的26.44提升超过6 dB，验证了结构化稀疏表示对几何和外观信息的强保留能力。在几何指标上，SLAT的Chamfer Distance仅为0.0083，显著优于CLAY的0.0124；F-score达到0.9999，近乎完美重建。值得注意的是，CLAY仅支持几何重建，无法评估外观指标，而SLAT同时覆盖几何和外观，展现出表征通用性。

### 生成质量：文本/图像到3D的主结果

Table 2汇总了Toys4k上的生成对比。在文本到3D任务中，TRELLIS-XL的CLIP score达到26.70，FD_dinov2仅237.48，较最佳基线GaussianCube的460.07降低约48%，表明生成分布与真实分布的高度一致。在图像到3D任务中，TRELLIS-L的CLIP score为85.77，FD_dinov2为67.21，均优于InstantMesh等2D辅助方法。Figure 5的视觉对比进一步印证了定量优势：基线方法常出现几何残缺或纹理模糊，而TRELLIS在复杂结构和材质细节上表现更为完整。

### 消融实验：关键设计选择

**潜在空间分辨率**（Table 3）：将SLAT从32³升级至64³，重建PSNR从31.85跃升至32.74，Chamfer Distance从0.0092降至0.0083。这一跃升验证了高分辨率稀疏结构对捕捉细粒度几何和纹理细节的决定性作用，是性能提升的核心杠杆。

**生成范式**（Table 4）：将两阶段的扩散模型替换为修正流模型，Stage 1的CLIP从25.86升至26.37，FD_dinov2从342.47降至295.89；Stage 2同样观察到一致改善。这证明修正流模型在3D生成任务中具有独立且叠加的增益效果。

**模型规模**（Table 5）：从Basic（342M）到XL（2B），CLIP从25.41持续提升至25.71，FD_dinov2从121.45降至93.96。规模扩展带来单调但递减的收益，表明更大模型有助于捕获更丰富的生成分布。

**时间步采样**（Table 7）：采用logitNorm(1,1)采样相比logitNorm(0,1)，在Stage 1中CLIP从26.03升至26.37，FD_dinov2从316.24降至295.89，验证了修正流模型中时间步分布对训练质量的影响。

### 用户研究：感知质量验证

Figure 6和Table 9展示了用户研究结果。在文本到3D任务中，TRELLIS获得67.1%的优选率；在图像到3D任务中，优选率高达94.5%。候选资产未经筛选，每个提示仅采样一次，避免了选择偏差；试验顺序随机化，增强了结果可信度。高优选率表明SLAT生成的资产在视觉质量和提示一致性上显著优于现有方法。

### 局限性与失败模式

尽管整体表现优异，方法存在以下局限：
- **两阶段流水线效率**：首先生成稀疏结构再生成细节，相比单阶段端到端方法增加了推理步骤。
- **光照烘焙问题**：图像到3D模型未分离光照效果，生成的3D资产包含输入图像的烘焙阴影和高光，影响在新环境中的重光照应用。
- **数据分布限制**：仅在开源数据集上训练，可能对真实世界复杂光照材质场景的泛化存在差距。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|---------|
| Table 1 | SLAT在重建PSNR（32.74）和CD（0.0083）上全面超越LN3Diff和CLAY，验证表示保真度 |
| Table 2 | 文本/图像到3D生成所有指标显著优于基线，FD_dinov2较最佳基线降低约48% |
| Table 3 | 64³分辨率是性能跃升的关键杠杆，PSNR提升0.89 |
| Table 4 | 修正流模型在两阶段独立提升生成质量，验证范式优越性 |
| Table 5 | 模型规模扩展持续改善分布质量，但收益递减 |
| Table 9 | 用户优选率67.1%（文本）和94.5%（图像），感知质量显著领先 |

![[assets/figures/papers/Structured_3D_Latents_for_Scalable_and_Versatile_3D_Generation_9feedf5ea34b/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparisons using Toys4k [80]. (KD is reported ×100. †: evaluated using shaded images of PBR meshes.)*

![[assets/figures/papers/Structured_3D_Latents_for_Scalable_and_Versatile_3D_Generation_9feedf5ea34b/figures/010_Table_3.jpg]]
*Table 3: Ablation study on the size of SLAT*

![[assets/figures/papers/Structured_3D_Latents_for_Scalable_and_Versatile_3D_Generation_9feedf5ea34b/figures/011_Table_4.jpg]]
*Table 4: Ablation study on different generation paradigms*

![[assets/figures/papers/Structured_3D_Latents_for_Scalable_and_Versatile_3D_Generation_9feedf5ea34b/figures/012_Table_5.jpg]]
*Table 5: Ablation study on model size*

## 定位与知识库关联

### 1. 核心基线对比与谱系定位

TRELLIS 的核心创新在于提出了一种统一的、表征无关的结构化稀疏潜在表示 **SLAT**，并配合两阶段修正流变换器进行生成。这使其在方法谱系中处于一个独特的位置，既不同于传统的单一表征生成方法，也不同于现有的潜在空间生成方法。

#### 1.1 潜在空间生成方法

现有方法通常将3D资产压缩到某种连续的潜在空间中，然后在该空间进行生成。TRELLIS 与这些方法的根本区别在于潜在表示的结构和编码信息。

-   **LN3Diff**：采用潜在三平面（latent triplanes）表示。三平面是一种紧凑的隐式表示，但其对几何和外观的耦合是隐式的。SLAT 通过将显式的稀疏几何结构（活跃体素 $p_i$）与局部外观特征（$z_i$）解耦，实现了更精细的控制和更高的重建保真度。如表1所示，SLAT在重建PSNR上达到32.74，远超LN3Diff的26.44，证明了结构化稀疏表示在保真度上的优势。

-   **3DTopia-XL**：采用潜在点云表示。点云天然具有稀疏性，但缺乏对体积外观信息的直接编码能力。SLAT 的稀疏体素结构可以视为一种“体积化”的点云，每个体素不仅包含位置信息，还携带了通过DINOv2聚合的多视图视觉特征，从而同时捕捉几何细节和复杂外观。

-   **CLAY**：采用潜在向量集（latent vector set）进行仅几何的网格生成。CLAY 的表示缺乏对颜色和纹理等外观信息的编码，这限制了其生成资产的丰富度。SLAT 通过将稠密的多视图DINOv2特征聚合到每个活跃体素上，统一了几何与外观的编码，使得单一表示可以解码为包含生动外观的3D高斯或辐射场，或具有精细几何的网格。

#### 1.2 直接生成与2D提升方法

除了潜在空间方法，TRELLIS 也显著区别于直接生成或依赖2D先验提升的方法。

-   **Shap-E**：作为一种直接3D生成基线，其生成质量和多样性受限于其隐式神经表示和扩散模型架构。TRELLIS 的两阶段修正流变换器，首先生成稀疏结构再生成细节，在生成质量上实现了质的飞跃，在Toys4k文本到3D任务上，其CLIP得分（26.70）和FD_dinov2（237.48）均大幅领先。

-   **LGM, InstantMesh**：这些方法利用2D扩散模型作为先验来生成或提升3D表示（如3D高斯或网格）。它们通常面临多视图一致性和生成速度的挑战。TRELLIS 直接在3D潜在空间进行生成，天然保证了3D一致性，且生成速度极快（约10秒），在图像到3D任务上，其CLIP得分（85.77）同样超越了InstantMesh（84.43），证明了原生3D生成范式的潜力。

-   **GaussianCube**：作为3D高斯的生成模型，GaussianCube 直接在结构化的高斯参数网格上进行扩散。TRELLIS 与之相比，其SLAT表示更为紧凑和抽象，将生成过程从高维的高斯参数空间转移到低维的、语义丰富的潜在空间，从而在生成质量上取得了显著提升，其FD_dinov2指标（237.48）相比GaussianCube（460.07）降低了约48%。

### 2. 适用边界与局限性

TRELLIS 的设计带来了显著优势，但也划定了其适用边界和当前局限。

-   **两阶段生成的低效性**：生成过程被分解为稀疏结构生成和结构化潜变量生成两个阶段。这种解耦虽然提升了质量和可控性，但相比单阶段端到端方法，流水线更为复杂，效率存在上限。这是一个架构层面的权衡，而非单纯的工程问题。

-   **烘焙光照问题**：图像到3D的生成过程中，模型未能将光照效果与材质属性分离。这导致生成的3D资产会“烘焙”进输入参考图像中的阴影和高光，而非生成具有物理渲染（PBR）材质的、可重新打光的资产。这限制了生成资产在真实感渲染管线中的直接使用。

-   **数据驱动的泛化边界**：模型在约50万个来自Objaverse-XL、ABO、3D-FUTURE、HSSD等开源数据集的高质量3D资产上训练。尽管其生成质量已超越部分商业模型，但在面对数据集中未覆盖的极端复杂光照、特殊材质或高度精细的结构时，其泛化能力可能存在上限。模型对训练数据分布的依赖是固有的局限性。

### 3. 开放问题

论文的贡献和局限性共同指向了以下值得探索的开放问题：

1.  **单阶段高效生成架构**：能否设计一个单阶段的生成模型，在保持或提升SLAT生成质量的同时，消除两阶段流水线的效率瓶颈？这可能需要新的生成范式或更高效的稀疏注意力机制。
2.  **内蕴材质与光照解耦**：如何在训练过程中引入光照增强和物理渲染损失，迫使模型学习将外观解耦为PBR材质参数（如反照率、粗糙度、金属度）和环境光照，从而生成可重新打光的3D资产？
3.  **大规模场景组合与内存效率**：当前方法主要针对单个物体生成。当用于组合大规模场景时，其稀疏体素结构的泛化能力和显存占用如何？是否需要设计层级化的稀疏策略或自适应的空间分辨率来支持场景级生成？
4.  **精细编辑的潜力**：论文展示了区域级的几何编辑和资产变体生成。SLAT表示是否具备更细粒度的编辑能力，例如独立编辑物体的材质属性或局部光照效果？这可能需要将潜在空间进一步结构化或引入解耦表示学习技术。

## 原文 PDF

![[paperPDFs/arxiv_2024/Structured_3D_Latents_for_Scalable_and_Versatile_3D_Generation.pdf]]
