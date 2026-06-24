---
title: "StereoWorld: Geometry-Aware Monocular-to-Stereo Video Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/StereoWorld_Geometry_Aware_Monocular_to_Stereo_Video_Generation.pdf
project_link: "https://ke-xing.github.io/StereoWorld/"
code_link: null
aliases:
- StereoWorld
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将预训练单目视频扩散模型改造为端到端立体生成器，通过帧维度拼接左右视图潜在表示并联合使用视差与深度监督（几何感知正则化），使模型显式学习立体几何。
primary_logic: 预训练视频扩散模型的 3D 时空注意力能够自然地融合帧维度拼接的左右视图信息；配合显式的视差监督（强制立体对应）和深度监督（补偿非重叠区域的几何缺失），模型能端到端地生成具有高几何一致性和视觉保真度的右眼视图。
claims:
- 定量结果表明，在视觉质量与几何精度指标上全面超越现有方法 GenStereo、SVG 和 StereoCrafter（PSNR 25.98、LPIPS 0.095、EPE 17.45 等）。
- 消融实验证实，视差监督和深度监督各自都有正向贡献，完整模型（同时使用视差和深度）获得最佳整体性能。
- 人工评估显示，受试者在立体效果（SE 4.8/5）、视觉质量（VQ 4.7/5）、双目一致性（BC 4.9/5）和时间一致性（TC 4.8/5）上均给出最高评分。
- StereoWorld-11M Test Set 上 PSNR = 25.9794
---

# StereoWorld: Geometry-Aware Monocular-to-Stereo Video Generation

> [!tip] 核心洞察
> 预训练视频扩散模型的 3D 时空注意力能够自然地融合帧维度拼接的左右视图信息；配合显式的视差监督（强制立体对应）和深度监督（补偿非重叠区域的几何缺失），模型能端到端地生成具有高几何一致性和视觉保真度的右眼视图。

| 字段 | 内容 |
|------|------|
| 中文题名 | StereoWorld：几何感知的单目到立体视频生成 |
| 英文题名 | StereoWorld: Geometry-Aware Monocular-to-Stereo Video Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.09363) · [Project](https://ke-xing.github.io/StereoWorld/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | StereoWorld |
| Dataset | StereoWorld-11M Test Set, Human Evaluation |

> [!tip] 效果简介
> - StereoWorld-11M Test Set 上，PSNR 25.9794 vs GenStereo, SVG, StereoCrafter (all lower) (显著优于所有基线)；EPE (End-Point Error) 17.4527 vs baselines have higher EPE (几何误差最低)。
> - Human Evaluation 上，Stereo Effect (SE) 4.8 out of 5 vs GenStereo, SVG, StereoCrafter (lower scores) (主观评分最高)。

## 概述

**核心问题**：将普通单目视频转换为具有立体视觉效果的 3D 内容，是扩展 XR 内容生态的关键需求。现有主流方法（如 **GenStereo** (Qiao et al., arXiv 2025)、**StereoCrafter** (Zhao et al., arXiv 2024)）普遍采用“深度估计—视点扭曲—空洞修补”的多阶段管道，这不仅破坏了视频的自然分布，还难以保证端到端的几何一致性与视觉保真度，常导致纹理失真、色彩偏移和立体伪影。

**核心方法**：本文提出 **StereoWorld**，一种端到端的扩散模型框架。其核心思路是将预训练的单目视频扩散模型改造为立体生成器：在潜在空间中将左右视图沿帧维度拼接，利用预训练模型的 3D 时空注意力自然融合跨视角信息；同时引入视差与深度双重几何监督，强制模型显式学习立体对应关系，并补偿非重叠区域的几何缺失。

**关键结果**：在自建的 StereoWorld-11M 测试集上，StereoWorld 全面超越现有方法——PSNR 达 25.98、LPIPS 低至 0.095、EPE 仅 17.45（Table 2）。人工评估中，受试者在立体效果（4.8/5）、视觉质量（4.7/5）、双目一致性（4.9/5）和时序一致性（4.8/5）上均给出最高评分（Table 4）。消融实验证实，视差监督与深度监督各自均有正向贡献，且二者互补，完整模型取得最佳性能（Table 3, Figure 8）。

**方法定位**：StereoWorld 属于“基于扩散模型的端到端立体视频生成”范式，区别于传统的多阶段扭曲-修补路线。它通过改造预训练视频 DiT（Diffusion Transformer）架构，在 Rectified Flow 框架下联合优化 RGB 与深度速度场，实现了从单目视频到高质量立体视频的直接映射。

## 背景与动机

立体视频（Stereoscopic video）是沉浸式视觉体验的核心载体，广泛应用于 3D 电影、扩展现实（XR）头显及各类立体显示设备。然而，立体内容的制作长期受限于高昂的专业拍摄成本与复杂的后期处理流程——传统方案需要双摄像机精确同步、严格的基线校准（IPD 对齐）以及繁重的后期立体校正。将海量的单目视频自动转换为高质量立体视频，因此成为一个兼具学术价值与产业需求的关键问题。

现有的单目转立体视频方法主要遵循一条**多阶段管道**：首先利用单目深度估计模型预测场景深度，继而通过图像扭曲（warping）生成右眼视图，最后依赖修补（inpainting）网络填充扭曲产生的空洞与遮挡区域。**GenStereo**（Qiao et al., arXiv 2025）与 **SVG** 等无需训练的基线方法，以及经微调的 **StereoCrafter**（Zhao et al., arXiv 2024），均属于这一范式。然而，这一管道存在根本性瓶颈：**深度估计、扭曲与修补三个阶段各自独立优化，破坏了视频数据的自然分布，缺乏端到端的几何与视觉一致性约束**，导致生成的右眼视图普遍存在纹理失真、色彩偏移和立体伪影。尤其在非重叠区域——水平相机平移引入的左右视图不可见部分——扭曲-修补策略几乎无法产生可信的内容，因为仅靠视差信息无法约束这些区域的生成。

从数据层面看，现有公开立体视频数据集（如 Spring、VKITTI2）普遍**未进行 IPD 对齐**，而已对齐的数据集（如 3D Movies）又不公开，这一数据缺口严重制约了端到端学习方法的训练。**StereoWorld-11M** 是首个大规模、IPD 对齐的立体视频数据集（Table 1），为突破上述瓶颈提供了数据基础。

上述分析指向一个明确的因果调控点：**将单目视频扩散模型改造为端到端的立体生成器，使其在统一的生成框架内显式学习立体几何对应关系**。本文的核心洞察在于：预训练视频扩散模型的 3D 时空注意力机制天然具备融合多视角信息的能力——若将左右视图的潜在表示沿帧维度拼接，模型便能在去噪过程中自动建立跨视角的时空关联。在此基础上，引入视差监督（强制像素级立体对应）与深度监督（补偿非重叠区域的几何缺失），可形成完整的几何感知正则化，使模型端到端地生成具有高几何一致性和视觉保真度的右眼视图。

> **需人工验证**：关于 GenStereo、SVG 和 StereoCrafter 的具体技术细节（如深度估计主干网络、修补策略等），本文未提供详细对比分析，上述总结基于论文对“多阶段管道”的概括性描述，建议查阅原始文献以确认各方法的精确差异。

## 核心创新

StereoWorld 的核心贡献在于**将预训练的单目视频扩散模型改造为端到端的立体视频生成器**，从根本上改变了现有方法“深度估计→扭曲→修补”的多阶段范式。其关键创新可归纳为以下三个维度。

### 1. 端到端扩散生成范式

现有主流方法（如 **GenStereo** (Qiao et al., arXiv 2025)、**SVG**、**StereoCrafter** (Zhao et al., arXiv 2024)）普遍采用多阶段管道：先估计左视图深度，再通过视差扭曲生成右视图，最后用修补网络填充空洞。这一范式破坏了视频的自然分布，导致纹理失真、色彩偏移和立体伪影。

StereoWorld 的解决方案是**将左右视图的 VAE 潜在表示沿帧维度拼接**（$z_i = [z_l, z_r]_{\mathrm{frame-dim}}$），直接输入基于 DiT 架构的预训练视频扩散模型。预训练模型的 3D 时空注意力机制能够自然地融合拼接后的左右视图信息，使模型端到端地学习从单目到立体的映射。这一设计的关键洞察在于：**帧维度拼接使得时空注意力块可以同时关注左右视图的对应区域，隐式地建立跨视角关联**，而无需显式的视差估计或扭曲操作。

### 2. 几何感知正则化策略

仅靠 RGB 重建损失无法保证立体几何的准确性，尤其是左右视图非重叠区域（由水平相机平移引入）缺乏直接的像素对应约束。StereoWorld 引入了一套**视差监督 + 深度监督**的双重几何正则化机制：

- **视差监督**：通过一个轻量级可微立体投影器 $\kappa$ 从左右潜在表示估算视差图 $\hat{b}_{\mathrm{pred}}$，并与伪真值视差 $\hat{b}_{\mathrm{gt}}$ 计算损失。视差损失 $\mathcal{L}_{\mathrm{dis}}$ 由对数损失项 $\mathcal{L}_{\log} = \mathbb{E}[d^2] - \lambda_1 (\mathbb{E}[d])^2$（惩罚对数视差差异的统计量，加强全局几何一致性）和 L1 损失项 $\mathcal{L}_{\mathrm{l1}} = \mathbb{E}[|\hat{b}_{\mathrm{pred}} - \hat{b}_{\mathrm{gt}}|]$（像素级视差一致性）加权组合而成。

- **深度监督**：针对非重叠区域（Figure 3 所示）视差监督无法覆盖的问题，模型额外预测右视图深度图，并通过深度速度场损失 $\mathcal{L}_{\mathrm{dep}}$ 进行约束。这为 RGB 生成提供了补充的几何线索，补偿了视差监督的盲区。

这两种监督通过**双分支 DiT 架构**实现解耦：初始 DiT 模块共享，提取 RGB 和深度的联合时空几何表示；最后的若干 DiT 模块权重复制为两个专用分支——RGB 分支预测 RGB 速度场，深度分支预测深度速度场。总训练目标为 $\mathcal{L} = \mathcal{L}_{\mathrm{rgb}} + \mathcal{L}_{\mathrm{dep}} + \lambda_{\mathrm{dis}} \mathcal{L}_{\mathrm{dis}}$。

### 3. 高分辨率长视频的时空拼接策略

预训练视频扩散模型通常受限于生成分辨率和时长的内存瓶颈。StereoWorld 提出了**时空拼接策略**以高效生成高分辨率、长时长的立体视频：

- **时间拼接**：训练时以概率 $p$ 用真实帧替换噪声潜在的前几帧，使模型学会以前段视频为条件生成后续帧；推理时将长视频分割为有时间重叠的段，前一段的末尾帧用于引导下一段生成，确保时序一致性。

- **空间拼接**：推理时将高分辨率潜在表示分割为空间重叠的瓦片，各瓦片独立去噪后，在重叠区域融合并拼接回原始尺寸。

这一策略使 StereoWorld 能够突破单次推理的内存限制，同时保持全局的时空一致性。

### 创新总结

| 创新维度 | 现有方法 | StereoWorld |
|---------|---------|-------------|
| 生成范式 | 多阶段深度估计-扭曲-修补 | 端到端扩散框架，帧维度拼接左右潜在表示 |
| 几何监督 | 仅 RGB 重建损失 | 视差监督 + 深度监督，双分支 DiT 解耦 |
| 高分辨率长视频 | 通常受限于低分辨率 | 时空拼接策略（时间分段 + 空间瓦片） |

消融实验（Table 3, Figure 8）证实：去除视差监督后几何精度大幅下降（EPE 和 D1-all 均变差），去除深度监督则降低非重叠区域的生成质量；完整模型在所有指标上取得最佳性能，验证了视差与深度监督的互补性。

## 整体框架

StereoWorld 旨在将预训练的单目视频扩散模型改造为一个端到端的立体视频生成器。其核心设计思路是：**将左右视图的潜在表示沿帧维度拼接，使预训练模型的 3D 时空注意力能够自然地融合跨视角信息，同时引入几何感知的正则化策略来显式约束立体几何的一致性。**

### 框架总览

如图 2 所示，整个框架围绕一个基于 DiT（Diffusion Transformer）架构的预训练文本到视频扩散模型（具体为 Wan2.1-T2V-1.3B）构建，并在 Rectified Flow 框架下进行训练。其前向过程定义了一条从数据分布到标准正态噪声的线性轨迹：

$$z _ { t } = ( 1 - t ) z _ { 0 } + t \epsilon$$

模型通过条件流匹配损失来回归目标向量场 $u_t$：

$$\mathbb { E } _ { t , p _ { t } ( z , \epsilon ) , p ( \epsilon ) } | | v _ { \Theta } ( z _ { t } , t ) - u _ { t } ( z _ { 0 } | \epsilon ) | | _ { 2 } ^ { 2 }$$

StereoWorld 在此基础架构上进行了三个关键改造：

1. **单目条件注入（Monocular Conditioning）**：将左视图视频和待生成的右视图视频分别编码到潜在空间后，沿帧维度拼接为联合输入 $z _ { i } = [ z _ { l } , z _ { r } ] _ { \mathrm { f r a m e - d i m } }$。这种帧维度的拼接使得模型内部的时空注意力层能够自然地建立左右视图之间的对应关系，无需额外的跨视角注意力模块。

2. **双分支 DiT 架构**：在共享若干初始 DiT 模块以提取联合的纹理与几何表示后，将最后几层 DiT 模块的权重复制为两个专用分支——一个专注于预测 RGB 速度场，另一个专注于预测深度速度场。这种设计使得模型能够解耦 RGB 生成与几何推理，同时保持两者之间的信息交互。

3. **几何感知正则化**：通过一个轻量级可微立体投影器 $\kappa$，从左右潜在表示中估计预测视差 $\hat { b } _ { \mathrm { p r e d } }$，并与伪真值视差进行监督。同时，深度分支预测右视图深度图，为 RGB 生成提供补充的几何约束。

### 训练与推理流程

**训练阶段**，系统首先利用外部模型（Video Depth Anything 和 Stereo Any Video）为所有训练视频预计算右视图深度图 $D_r$ 和视差图 $Disp_{gt}$ 作为伪真值。左视图视频与右视图视频及其深度图在潜在空间中沿帧维度拼接后，作为联合条件输入。训练时的总损失函数为：

$$\mathcal { L } = \mathcal { L } _ { \mathrm { r g b } } + \mathcal { L } _ { \mathrm { d e p } } + \lambda _ { \mathrm { d i s } } \mathcal { L } _ { \mathrm { d i s } }$$

其中 $\mathcal { L } _ { \mathrm { r g b } }$ 和 $\mathcal { L } _ { \mathrm { d e p } }$ 分别为 RGB 和深度潜在变量的条件流匹配损失，$\mathcal { L } _ { \mathrm { d i s } }$ 为视差损失。

**推理阶段**，仅使用共享 DiT 模块和 RGB 专用分支，以单目视频作为唯一输入，直接生成对应的右眼视图，无需任何额外的深度估计或视差计算步骤。

### 高分辨率长视频的时空拼接策略

为突破单次生成的内存限制，StereoWorld 引入了时空拼接策略：

- **时间拼接（Temporal Tiling）**：将长视频分割为具有时间重叠的片段，前一个片段的最后若干帧用作下一个片段的引导帧，确保段间时序一致性。训练时，以概率 $p$ 将噪声潜在的前几帧替换为真实帧，使模型学会利用上下文帧进行条件生成。
- **空间拼接（Spatial Tiling）**：将高分辨率潜在表示分割为具有空间重叠的瓦片，各瓦片独立去噪后，在重叠区域进行融合再解码回像素空间，实现高效的高分辨率生成。

### 与现有范式的本质区别

现有主流方法（如 **GenStereo**（Qiao et al., arXiv 2025）、**SVG**、**StereoCrafter**（Zhao et al., arXiv 2024））普遍采用多阶段管道：先估计深度图，再通过扭曲（warping）生成右视图，最后用修补（inpainting）填充空洞。这种范式破坏了视频的自然分布，容易引入纹理失真、色彩偏移和立体伪影。StereoWorld 的端到端扩散框架则从根本上避免了这一问题——模型直接学习从单目视频到立体视频的条件分布，无需显式的深度估计或扭曲操作，从而在视觉质量和几何一致性上取得了显著提升。

### 补充图表

![[assets/figures/papers/paper_list_l2604_https_arxiv_org_abs_2512_09363/figures/003_Figure_2.jpg]]
*Figure 2: Overall framework of StereoWorld. Before training, we use Video Depth Anything [9] and Stereo Any Video [24] to obtain the depth maps*

## 核心模块与公式推导

### 3.1 基础扩散框架

StereoWorld 构建在预训练的文本到视频扩散模型 **Wan2.1-T2V-1.3B** 之上，该模型基于 Diffusion Transformer (DiT) 架构，并在 Rectified Flow 框架下训练。Rectified Flow 定义了一条从数据分布到标准正态分布的线性轨迹：

$$z _ { t } = ( 1 - t ) z _ { 0 } + t \epsilon$$

其中 $z_0$ 为干净数据，$\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声，$t \in [0, 1]$ 为时间步。模型通过条件流匹配损失来回归目标向量场 $u_t(z_0|\epsilon) = \epsilon - z_0$：

$$\mathbb { E } _ { t , p _ { t } ( z , \epsilon ) , p ( \epsilon ) } || v _ { \Theta } ( z _ { t } , t ) - u _ { t } ( z _ { 0 } | \epsilon ) || _ { 2 } ^ { 2 }$$

该框架为后续的立体生成改造提供了统一的概率建模基础。

### 3.2 单目条件化：帧维度潜在拼接

StereoWorld 的核心创新在于将单目视频扩散模型改造为端到端立体生成器，而非沿用传统的“深度估计→扭曲→修补”多阶段管道。具体而言，给定左视图视频 $V_l$ 和右视图视频 $V_r$，首先通过 VAE 将其编码到潜在空间，得到 $z_l$ 和 $z_r$，随后沿帧维度拼接为联合输入：

$$z _ { i } = [ z _ { l } , z _ { r } ] _ { \mathrm { f r a m e - d i m } }$$

这一设计的因果机制在于：预训练 DiT 的 3D 时空注意力天然具备跨帧信息融合能力，将左右视图视为同一视频序列的连续帧，即可隐式地建立跨视角对应关系。训练时，模型以拼接后的联合潜在变量为输入，同时预测左右视图的去噪方向；推理时，仅需输入左视图视频，模型即可端到端地生成对应的右视图。

### 3.3 几何感知正则化

仅依赖 RGB 重建损失无法保证立体几何精度。StereoWorld 引入了由视差监督和深度监督组成的几何感知正则化策略。

#### 3.3.1 视差监督

视差监督强制左右视图之间的像素级对应关系。首先通过轻量级可微立体投影器 $\kappa$ 从左右潜在表示估算预测视差 $\hat{b}_{\mathrm{pred}}$，然后与伪真值视差 $\hat{b}_{\mathrm{gt}}$（由 **Stereo Any Video** 预提取）进行对比。视差损失由对数损失项和 L1 损失项加权组合：

$$\mathcal { L } _ { \mathrm { d i s } } = \mathcal { L } _ { \mathrm { l o g } } + \lambda _ { \mathrm { l l } } \mathcal { L } _ { \mathrm { l l } }$$

其中，对数视差损失通过惩罚对数视差差异 $d = \log \hat{b}_{\mathrm{pred}} - \log \hat{b}_{\mathrm{gt}}$ 的统计量来加强全局几何一致性：

$${ \mathcal { L } } _ { \log } = \mathbb { E } \left[ d ^ { 2 } \right] - \lambda _ { 1 } \left( \mathbb { E } [ d ] \right) ^ { 2 }$$

L1 损失则提供像素级别的稠密监督：

$$\mathcal { L } _ { \mathrm { 1 1 } } = \mathbb { E } [ | \hat { b } _ { \mathrm { p r e d } } - \hat { b } _ { \mathrm { g t } } | ]$$

#### 3.3.2 深度监督的必要性

水平相机平移会引入左右视图之间的非重叠区域（如前景物体边缘的遮挡区域），视差监督对此类区域完全失效（参见 Figure 3）。为补偿这一几何缺失，StereoWorld 额外引入深度监督：利用 **Video Depth Anything** 预提取右视图深度图 $D_r$ 作为伪真值，约束模型在生成 RGB 的同时预测一致的深度信息。

![[assets/figures/papers/paper_list_l2604_https_arxiv_org_abs_2512_09363/figures/004_Figure_3.jpg]]
*Figure 3: Non-overlapping regions between stereo views. Horizontal camera translation introduces non-overlapping content, which disparity supervision alone cannot constrain, motivating the use of depth-based supervision*

#### 3.3.3 双分支 DiT 架构

为实现 RGB 与深度的解耦学习，StereoWorld 复制了最后若干层 DiT 模块的权重，形成两个专用分支：

- **RGB 分支**：预测右视图 RGB 速度场，对应损失函数为：

$$\mathcal { L } _ { \mathrm { r g b } } = \mathbb { E } _ { t , p _ { t } ( z , \epsilon ) , p ( \epsilon ) } || v _ { \Theta ^ { \prime } } ( z _ { t } , t ) - u _ { t } ( z _ { 0 } | \epsilon ) || _ { 2 } ^ { 2 }$$

- **深度分支**：预测右视图深度速度场，对应损失函数为：

$$\mathcal { L } _ { \mathrm { d e p } } = \mathbb { E } _ { t , p _ { t } ( d , \epsilon ) , p ( \epsilon ) } || v _ { \Theta ^ { \prime } } ( d _ { t } , t ) - u _ { t } ( d _ { 0 } | \epsilon ) || _ { 2 } ^ { 2 }$$

初始的共享 DiT 模块则负责提取 RGB 和深度的联合时空几何表示。推理时仅使用共享模块和 RGB 分支，深度分支不参与前向计算。

#### 3.3.4 总训练目标

联合优化 RGB 生成、深度预测和视差约束的总损失函数为：

$$\mathcal { L } = \mathcal { L } _ { \mathrm { r g b } } + \mathcal { L } _ { \mathrm { d e p } } + \lambda _ { \mathrm { d i s } } \mathcal { L } _ { \mathrm { d i s } }$$

其中 $\lambda_{\mathrm{dis}}$ 为视差损失的平衡权重。消融实验（Table 3, Figure 8）证实：视差监督和深度监督各自均有正向贡献，完整模型在所有指标上取得最佳性能，验证了两者的互补性——视差约束确保重叠区域的精确对应，深度监督补偿非重叠区域的几何缺失。

### 3.4 时空拼接策略

为支持高分辨率长视频的立体生成，StereoWorld 采用了时空拼接策略：

- **时间分段**（Figure 4）：训练时以概率 $p$ 将噪声潜在变量的前若干帧替换为真值帧，模拟推理时的分段引导；推理时将长视频分割为有时间重叠的段，前一段的最后若干帧用于引导下一段，确保时序一致性。

![[assets/figures/papers/paper_list_l2604_https_arxiv_org_abs_2512_09363/figures/005_Figure_4.jpg]]
*Figure 4: Temporal tiling strategy. During training, the first few frames of noisy latents are replaced with ground-truth frames with a probability p. During inference, long videos are split into overlapping segments, with the last frames of the previous segment used to guide the next, ensuring temporal consistency*

- **空间瓦片**（Figure 5）：推理时将高分辨率潜在表示分割为空间重叠的瓦片，各瓦片独立去噪后，在重叠区域融合拼接回原始尺寸，有效缓解显存压力。

![[assets/figures/papers/paper_list_l2604_https_arxiv_org_abs_2512_09363/figures/006_Figure_5.jpg]]
*Figure 5: Spatial tiling strategy. During inference, highresolution videos are encoded into latents, which are split into overlapping tiles. Each tile is denoised independently, and then the tiles are stitched back to the original size with overlapping regions fused before decoding*

> **注意**：论文未详细公开时空拼接策略中超参数（如重叠比例、瓦片尺寸）的具体取值，也未讨论段间过渡在极端运动场景下的平滑性量化评估，该部分细节需手动验证。

## 实验与分析

### 定量对比：全面超越现有方法

StereoWorld 在 StereoWorld-11M 测试集上与三类代表性基线进行了全面对比：无需训练的立体生成方法 **GenStereo**（Qiao et al., arXiv 2025）和 SVG，以及经微调的 **StereoCrafter**（Zhao et al., arXiv 2024）。表 2 汇总了视觉质量与几何精度两个维度的定量结果。

在视觉质量指标上，StereoWorld 取得了 **PSNR 25.98**、**SSIM 0.7964** 和 **LPIPS 0.095** 的最佳成绩，显著优于所有基线。同时，VBench 的图像质量评分（IQ-Score）和时序闪烁评分（TF-Score）也表明，本方法在保持高画质的同时有效抑制了帧间抖动。

在几何精度指标上，StereoWorld 的 **EPE（端点误差）为 17.45**，**D1-all 为 0.48**，均为所有方法中最低，说明生成的右视图与左视图之间的像素级对应关系最为准确。多阶段管道方法（如 GenStereo、SVG）因深度估计-扭曲-修补的级联误差，在纹理细节和立体对应上均明显劣化；StereoCrafter 虽经微调，但其几何一致性仍不及本方法的端到端学习范式。

### 消融实验：几何感知正则化的必要性

为验证视差监督与深度监督各自的贡献，研究者在完整模型基础上分别移除各损失项进行消融（表 3）。

**去除视差监督（w/o L_dis）** 导致几何精度大幅下降：EPE 和 D1-all 均显著恶化，表明模型失去了强制立体对应的关键约束，右视图的像素偏移出现系统性偏差。定性结果（图 8）也显示，缺少视差监督时，生成的立体效果明显减弱，物体的水平位移不符合立体几何预期。

**去除深度监督（w/o L_dep）** 主要损害非重叠区域的生成质量。由于水平相机平移会引入左右视图间无法通过视差约束的非重叠内容（图 3），仅靠视差损失无法为这些区域提供几何引导。消融实验中，去除深度监督后，非重叠区域的纹理细节和结构连贯性明显变差，整体视觉一致性下降。

**完整模型（同时使用视差和深度监督）** 在所有指标上取得最佳性能，证实了两者的互补性：视差监督负责重叠区域的精确立体对应，深度监督弥补非重叠区域的几何缺失，二者协同实现了端到端的高保真立体生成。

### 人工评估：主观体验全面领先

除自动指标外，研究还进行了人工评估（表 4），邀请受试者从四个维度对生成结果进行 1-5 分评分：

- **立体效果（SE）**：4.8 / 5
- **视觉质量（VQ）**：4.7 / 5
- **双目一致性（BC）**：4.9 / 5
- **时间一致性（TC）**：4.8 / 5

StereoWorld 在所有主观维度上均获得最高评分，尤其在双目一致性和立体效果上优势明显，表明生成的立体视频在佩戴 3D 眼镜或 XR 头显观看时能提供自然、舒适的深度感知。

### 定性分析：细节保真与文本渲染

图 6 展示了与现有方法的静态帧定性对比。StereoWorld 在保持与左视图高度视觉一致的同时，能更好地保留细粒度纹理细节（如毛发、织物纹理）。尤其值得注意的是，**本方法在文本渲染质量上远超所有基线**：多阶段管道方法在扭曲和修补过程中常导致文字扭曲、模糊或残缺，而端到端扩散框架能更完整地保留文字的形状和清晰度。

图 7 从时间维度进一步验证了时序一致性。StereoWorld 生成的连续帧之间过渡平滑，无明显闪烁或伪影，而基线方法在运动区域常出现纹理抖动或几何跳变。

### 失败模式与局限性

尽管整体表现优异，StereoWorld 仍存在若干已知局限：

1. **外部模型依赖**：方法依赖预训练的深度估计模型（Video Depth Anything）和立体匹配模型（Stereo Any Video）提供伪真值。这些模型的估计误差可能向下游传播，在遮挡边界、透明物体或弱纹理区域尤为明显。
2. **场景泛化**：训练数据集 StereoWorld-11M 主要来源于 Blu-ray 影视内容，场景类型偏向室内对话和中等运动幅度。对户外高速运动、极端光照或非自然场景的泛化能力尚需进一步验证。
3. **时空拼接的过渡平滑性**：虽然时空拼接策略有效缓解了长视频和高分辨率生成的内存压力，但在极端运动或快速场景切换下，段间过渡仍可能出现轻微的不连贯。
4. **计算与版权**：论文未详细公开基于 Wan2.1-T2V-1.3B 的大规模训练计算开销，也未讨论所收集电影数据的版权合规性问题。

### 关键图表索引

- **表 2**：与现有方法的全面定量对比，覆盖视觉质量（PSNR、SSIM、LPIPS、IQ-Score、TF-Score）和几何精度（EPE、D1-all）两类指标。
- **表 3**：几何感知正则化的消融实验，验证视差监督和深度监督各自的贡献及互补性。
- **表 4**：人工评估结果，从立体效果、视觉质量、双目一致性和时间一致性四个维度进行主观评分。
- **图 6**：与现有方法的静态帧定性对比，突出细节保真和文本渲染质量。
- **图 7**：时间维度的定性对比，展示时序一致性优势。
- **图 8**：消融实验的定性对比，直观展示视差偏移和结构感知的差异。

### 补充图表

![[assets/figures/papers/paper_list_l2604_https_arxiv_org_abs_2512_09363/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparisons with state-of-the-art methods. It shows that our method achieves the best generation quality, preserving fine details while maintaining strong visual consistency with the left view. Crucially, our method achieves far better text rendering quality than all baselines*

![[assets/figures/papers/paper_list_l2604_https_arxiv_org_abs_2512_09363/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative comparisons with state-of-the-art methods in the temporal dimension. Our method maintains superior temporal consistency while preserving high visual quality and fine-grained detail fidelity compared to other methods*

![[assets/figures/papers/paper_list_l2604_https_arxiv_org_abs_2512_09363/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative comparison results of ablation study. Our full model exhibits better disparity shifts and structural perception*

![[assets/figures/papers/paper_list_l2604_https_arxiv_org_abs_2512_09363/figures/011_Table_3.jpg]]
*Table 3: Ablation on geometry-aware regularization. The full model achieves the best overall performance*

![[assets/figures/papers/paper_list_l2604_https_arxiv_org_abs_2512_09363/figures/012_Table_4.jpg]]
*Table 4: Results of Human evaluation with metrics: Stereo Effect (SE), Visual Quality (VQ), Binocular Consistency (BC), and Temporal Consistency (TC)*

![[assets/figures/papers/paper_list_l2604_https_arxiv_org_abs_2512_09363/figures/002_Table_1.jpg]]
*Table 1: Comparison of the stereo datasets. Existing datasets are generally not IPD-aligned (e.g., Spring, VKITTI2), while datasets that are IPD-aligned are not publicly available (e.g., 3D Movies). Our StereoWorld is the first large-scale, IPD-aligned dataset*

## 方法谱系与知识库定位

### 1. 从多阶段管道到端到端生成：范式迁移的因果瓶颈

单目到立体视频生成任务长期被多阶段管道主导：先通过单目深度估计获得视差/深度图，再基于扭曲（warping）生成右视图，最后利用修补（inpainting）填充空洞区域。这一范式存在根本性瓶颈——各阶段独立优化，破坏了视频的自然分布，导致纹理失真、色彩偏移和立体伪影。本文提出的 **StereoWorld** 将预训练单目视频扩散模型改造为端到端立体生成器，核心因果调节旋钮在于**帧维度拼接左右视图潜在表示**，并联合施加**视差与深度监督**，使模型显式学习立体几何对应关系。

与现有方法的本质差异体现在生成范式、几何监督和高分辨率处理三个维度：

| 维度 | 基线方法 | StereoWorld |
|------|----------|-------------|
| 生成范式 | 多阶段深度估计-扭曲-修补 | 端到端扩散框架，帧维度拼接左右视图潜在表示 |
| 几何监督 | 仅 RGB 重建损失 | 视差监督 + 深度监督，双分支 DiT 解耦 RGB 与深度学习 |
| 高分辨率长视频 | 通常受限于低分辨率 | 时空拼接策略（时间分段 + 空间瓦片） |

### 2. 与基线工作的关系定位

本文的对比基线覆盖了两类代表性方法：

- **无需训练的立体生成方法**：**GenStereo**（Qiao et al., arXiv 2025）和 **SVG** 均属于推理时即插即用的方案，不涉及模型微调。这类方法虽然部署便捷，但缺乏对立体几何的显式建模，在几何精度和视觉一致性上存在天然劣势。定量结果表明，StereoWorld 在 PSNR（25.98）和 EPE（17.45）上显著优于这些方法（Table 2）。

- **经微调的立体生成基线**：**StereoCrafter**（Zhao et al., arXiv 2024）对预训练模型进行了微调，但其监督信号仍以 RGB 重建为主，未引入显式的几何正则化。StereoWorld 在此基础上引入了视差监督（强制立体对应）和深度监督（补偿非重叠区域的几何缺失），消融实验证实这两项监督各自均有正向贡献，完整模型取得最佳整体性能（Table 3, Figure 8）。

方法的核心洞察在于：预训练视频扩散模型的 3D 时空注意力能够自然地融合帧维度拼接的左右视图信息；配合显式的几何正则化，模型能端到端地生成具有高几何一致性和视觉保真度的右眼视图。

### 3. 适用边界与局限

尽管 StereoWorld 在定量和定性评估中均表现出色，其适用边界和潜在局限值得关注：

**数据依赖与外部模型偏差**。该方法依赖预训练的深度估计模型（Video Depth Anything）和立体匹配模型（Stereo Any Video）提供伪真值监督。这些外部模型的预测误差可能向下游传播，影响最终生成质量。论文未分析当伪真值质量下降时（如极端光照、透明物体、重复纹理场景）生成结果的退化程度。

**训练数据场景覆盖**。StereoWorld-11M 数据集主要来源于 Blu-ray 影视内容，场景类型以叙事性室内外场景为主。对于户外高速运动、无人机航拍、体育赛事等具有剧烈视差变化和快速场景切换的领域，模型的泛化能力尚需验证。此外，论文未讨论所收集电影数据的版权合规性。

**时空拼接的过渡平滑性**。时空拼接策略（Figure 4, Figure 5）通过时间分段和空间瓦片缓解了长视频高分辨率生成的内存压力，但在极端运动或快速场景切换下，段间过渡的平滑性仍有提升空间。论文未提供拼接边界伪影的定量分析。

**计算开销未公开**。该方法基于 Wan2.1-T2V-1.3B 构建，双分支 DiT 架构和几何感知正则化引入了额外计算量，但论文未详细公开大规模训练的计算开销和推理延迟。

### 4. 开放问题

基于当前工作的技术路线和局限，以下开放问题值得后续研究关注：

1. **非 IPD 对齐基线的泛化**：StereoWorld 训练数据经过 IPD 对齐处理，如何将端到端立体生成框架推广到任意基线配置（如用户自定义瞳距或非水平相机排列）？

2. **几何感知正则化的多视角扩展**：当前的视差和深度监督针对双目立体设计，该正则化策略能否扩展到多视角（如自由视点视频）或 3D 一致的视频生成任务？

3. **轻量化伪真值估计**：是否存在更轻量的深度/视差估计器可以替代当前的外部模型，从而降低训练成本并减少误差累积？自监督或弱监督的几何信号是否可行？

4. **生成深度的下游可用性**：该方法同步生成了右视图深度图，其质量如何？是否可直接用于下游 3D 重建、新视点合成或场景理解任务？

5. **运动遮挡鲁棒性**：当左右视图存在显著运动遮挡（如前景物体快速横穿画面）时，当前框架的几何推理能力如何？是否需要引入显式的遮挡推理模块？

6. **版权与伦理合规**：大规模影视数据的收集和使用涉及版权问题，如何在保证训练数据规模的同时建立合规的数据获取和授权机制，是推动该技术走向实际应用的重要前提。

## 原文 PDF

![[paperPDFs/CVPR_2026/StereoWorld_Geometry_Aware_Monocular_to_Stereo_Video_Generation.pdf]]