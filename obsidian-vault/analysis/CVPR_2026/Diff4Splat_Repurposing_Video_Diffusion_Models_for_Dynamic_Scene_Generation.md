---
title: "Diff4Splat: Repurposing Video Diffusion Models for Dynamic Scene Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Diff4Splat_Repurposing_Video_Diffusion_Models_for_Dynamic_Scene_Generation.pdf
project_link: "https://paulpanwang.github.io/Diff4Splat"
code_link: "https://github.com/christophschuhmann/improved-aesthetic-predictor"
aliases:
- Diff4Splat
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 将视频扩散模型的生成先验与可变形3D高斯场的显式表示在统一框架内融合，用一次前馈预测直接输出动态4D场景，彻底消除测试时的逐场景优化。
primary_logic: 视频扩散模型的潜变量可以视为具有时空连续性的动态点云，通过条件Transformer将其映射为3D高斯属性和帧间变形，从而在保真度、几何一致性和效率之间取得突破。
claims:
- DIFF4SPLAT 在单次前馈中直接预测可变形3D高斯场，无需测试时优化。
- 核心模块 Video Latent Transformer 弥合了2D时空特征与4D动态场景之间的表示鸿沟。
- 方法将动态场景生成时间缩短至约30秒，相比优化式基线实现60倍加速。
- 统一训练目标整合了流匹配损失、光度损失、几何损失和运动损失，确保外观、几何与动态一致性。
---

# Diff4Splat: Repurposing Video Diffusion Models for Dynamic Scene Generation

> [!tip] 核心洞察
> 视频扩散模型的潜变量可以视为具有时空连续性的动态点云，通过条件Transformer将其映射为3D高斯属性和帧间变形，从而在保真度、几何一致性和效率之间取得突破。

| 字段 | 内容 |
|------|------|
| 中文题名 | Diff4Splat：将视频扩散模型重用于动态场景生成 |
| 英文题名 | Diff4Splat: Repurposing Video Diffusion Models for Dynamic Scene Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Pan_Diff4Splat_Repurposing_Video_Diffusion_Models_for_Dynamic_Scene_Generation_CVPR_2026_paper.html) · [Project](https://paulpanwang.github.io/Diff4Splat) · [Code](https://github.com/christophschuhmann/improved-aesthetic-predictor) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DIFF4SPLAT |
| Dataset | RealEstate10K, Stereo4D, TartanAir, MatrixCity, PointOdyssey, DynamicReplica, Spring, VKITTI2, MultiCamVideo |
> [!tip] 效果简介
> - 动态视频生成质量 (VBench-2.0 / 4D基准) 上，FVD ↓ / Reconstruction Time FVD 210.15, Rec.Time 30s vs 优化方法 (Mosca ~30 min, DimensionX 数小时) (生成速度提升60倍以上，生成质量达到或超过优化方法)。
> - 几何完整性评估 上，Avg. Matches / Subj. Consist. / Bg. Consist. 5114.22 / 88.32 / 89.89 vs 隐式表示/优化方法 (几何匹配数和一致性指标优于对比方法，同时保持30s推理时间)。
> - 相机位姿精度 (相对位姿误差) 上，Avg.RPE Translation / Rotation 0.012 / 0.008 vs 隐式表示方法 (如Aether) (平移和旋转误差显著降低，验证了显式几何表示的优势)。

## 概要

### 问题瓶颈

动态4D场景生成（从单张图像生成具有时空一致性的可渲染动态场景）长期受困于一个根本性瓶颈：现有方法普遍采用“先生成2D视频，再逐场景优化升维为3D/4D表示”的两阶段流水线。无论是**Mosca**的约半小时优化，还是**DimensionX**（Sun et al., arXiv 2024）的数小时多阶段处理，测试时优化（test-time optimization）的昂贵计算代价使得这类方法无法满足实时或交互式应用需求。**Aether**（Zhu et al., arXiv 2025）虽然尝试了前馈生成，但其隐式表示在渲染时仍存在空洞和伪影问题。核心矛盾在于：2D视频生成先验与4D场景表示之间存在巨大的表示鸿沟（representational gap），现有方案缺乏一个统一的框架来弥合这一鸿沟。

### 核心方法

**DIFF4SPLAT** 提出了一种范式转换：将视频扩散模型的生成先验与可变形3D高斯场的显式表示融合，在单次前馈推理中直接输出动态4D场景，彻底消除测试时优化。其核心洞察在于——视频扩散模型的潜变量可被解释为具有时空连续性的动态点云，通过专门设计的**Video Latent Transformer**将其映射为3D高斯属性（均值、旋转、尺度、不透明度、颜色）及其帧间变形，从而在保真度、几何一致性和效率之间取得突破。

方法架构（Figure 2）包含四大创新模块：（1）以预训练视频扩散模型**CogVideoX**为基础，输入单图、文本和相机位姿（Plücker嵌入），生成时空一致的潜在张量；（2）**Latent Dynamic Reconstruction Model (LDRM)**，由16个标准Transformer块构成，将潜变量解码为高斯特征图与变形图；（3）**可变形高斯场**，通过可学习的帧间变形（均值位移、旋转四元数乘法、尺度加性调整）实现动态场景的显式表示；（4）**统一训练目标**，整合流匹配损失、光度损失、几何损失和运动损失，确保外观、几何与动态的一致性监督。

### 关键结果

DIFF4SPLAT将动态场景生成时间压缩至约**30秒**，相比优化式基线实现**60倍加速**（Table 2）。在动态视频生成质量（VBench-2.0/4D基准）上，FVD达到**210.15**，与需要逐场景优化的方法相当或更优（Table 1）。几何完整性方面，平均匹配数达**5114.22**，主体一致性**88.32**，背景一致性**89.89**，均优于隐式表示方法（Table 2）。相机位姿精度上，平均相对位姿误差（RPE）的平移误差仅**0.012**、旋转误差**0.008**，显著低于隐式方法如Aether（Table 3），验证了显式几何表示在空间精度上的优势。消融实验进一步证实：移除运动损失导致FVD从210.15恶化至**351.38**（Table 4）；移除可变形高斯场模块在大运动区域出现重影和撕裂伪影（Figure 6）；渐进式训练策略（先静后动）比直接从动态数据训练获得更高的视觉质量（Figure 7）。

### 方法谱系与知识库定位

DIFF4SPLAT定位于**前馈动态4D场景生成**这一新兴方向，与以下工作形成对比与互补：

- **优化式4D生成**：Mosca、DimensionX等依赖逐场景优化，生成质量高但耗时巨大；DIFF4SPLAT以约30秒的前馈推理实现了可比的质量，填补了效率缺口。
- **前馈动态生成**：Aether（Zhu et al., arXiv 2025）同样采用前馈方式，但使用隐式表示，渲染存在空洞和伪影；DIFF4SPLAT通过显式可变形3D高斯场获得了更优的几何完整性和相机位姿精度。
- **视频扩散模型蒸馏**：Lyra等基于视频扩散模型与3DGS蒸馏进行动态生成；DIFF4SPLAT的Video Latent Transformer提供了一种更直接的潜变量到4D表示的映射机制。
- **静态3D生成**：DIFF4SPLAT的可变形高斯场扩展了3D Gaussian Splatting（Kerbl et al., SIGGRAPH 2023）的静态表示，将其推广至动态场景，同时保留了显式表示的可微渲染和实时渲染优势。

方法的局限性在于依赖大规模带标注的4D数据集进行训练，对极小或极快运动场景的生成效果可能仍有不足。开放问题包括：如何进一步压缩模型体积以支持移动端部署，能否扩展到更长时序或开放域的动态场景生成，以及在完全无标注的真实世界视频上的泛化能力。



### 动态4D场景生成的现实需求

从单张图像重建可交互的动态三维场景，是计算机视觉与图形学中长期存在的核心挑战。该能力一旦成熟，将直接赋能增强现实、虚拟制作、沉浸式视频会议等应用场景——用户仅需提供一张照片和一段相机轨迹，即可获得一个可自由漫游、实时渲染的动态4D世界。然而，这一目标的实现面临双重困难：既要保证多视角下的外观真实感，又要维持跨帧的几何与运动一致性。

### 现有方法的瓶颈：多阶段流程与昂贵的测试时优化

当前主流的动态场景生成方法普遍采用“先生成2D视频，再将其升维为4D表示”的两阶段范式。具体而言，这类方法首先利用视频扩散模型或图像到视频模型生成一段多视角视频序列，随后通过逐场景的优化过程，将视频帧拟合为某种3D表示（如神经辐射场、隐式表面或动态点图）。代表性工作包括 **Mosca**（优化式动态4D场景生成，单场景耗时约半小时）和 **DimensionX**（Sun et al., arXiv 2024，多阶段流程，耗时数小时）。这类方案的根本缺陷在于：

- **计算代价极高**：测试时优化需要为每个新场景重新执行完整的梯度下降过程，通常耗费数GPU小时，完全无法满足实时或交互式应用的需求。
- **表示能力受限**：隐式表示（如NeRF）虽能产生连续表面，但缺乏显式几何结构，导致渲染存在空洞和伪影；而动态点图等方法则难以保持精细的外观细节。例如，**Aether**（Zhu et al., arXiv 2025）作为前馈动态点图生成方法，虽避免了逐场景优化，但其隐式表示在渲染时仍会出现明显的几何不完整性问题。

### 核心洞察：视频扩散潜变量即动态点云

DIFF4SPLAT 的出发点建立在一个关键的观察之上：**预训练视频扩散模型在潜空间中编码的时空特征，本质上已经蕴含了场景的三维结构和运动信息**。这些潜变量可以被重新解释为一组具有时空连续性的动态点云——它们不仅描述了场景的外观，还隐式地捕捉了帧间的几何变形。然而，现有方法仅将视频扩散模型用作2D像素生成器，完全忽略了潜空间中这些可贵的3D-4D线索。

### 本文动机：统一前馈框架

基于上述洞察，DIFF4SPLAT 提出了一种全新的范式：**将视频扩散模型的生成先验与可变形3D高斯场的显式表示在单一前馈框架内深度融合，直接预测动态4D场景，彻底消除测试时的逐场景优化**。这一设计在三个维度上实现了突破：

1. **效率**：将动态场景生成时间压缩至约30秒，相比优化式基线实现60倍加速。
2. **保真度**：显式高斯表示保证了高分辨率的外观质量和清晰的几何结构。
3. **一致性**：通过统一的光度、几何和运动损失联合监督，确保多视角渲染与动态演化的时空一致性。

为实现这一目标，DIFF4SPLAT 设计了 Video Latent Transformer 作为核心桥梁，将2D时空潜特征映射为结构化的可变形3D高斯场参数，并引入可学习的帧间变形机制来显式建模动态场景的演化。后续章节将详细展开这一方法论的技术细节与实验验证。



## 核心方法与创新机理

DIFF4SPLAT 的核心创新在于**将视频扩散模型的生成先验与可变形3D高斯场的显式表示在统一框架内融合**，通过一次前馈预测直接输出动态4D场景，彻底消除测试时的逐场景优化。这一范式转变由以下关键模块和设计选择共同支撑。

### 关键创新模块

**视频潜变量Transformer（Video Latent Transformer）** 是弥合2D时空特征与4D动态场景之间表示鸿沟的核心架构。传统方法将视频扩散模型仅用于生成2D帧序列，而DIFF4SPLAT通过Latent Dynamic Reconstruction Model（LDRM）将扩散模型产生的潜变量重新解释为具有时空连续性的动态点云。LDRM由16个标准Transformer块组成，以预训练视频扩散模型CogVideoX生成的潜在张量和相机位姿（Plücker嵌入）为输入，直接回归3D高斯原语的属性参数。这一设计使得2D外观先验、几何线索与运动信息得以在潜空间中协同融合，为下游的显式4D表示提供了结构化特征基础。

**可变形3D高斯场（Deformable Gaussian Field）** 是DIFF4SPLAT提出的显式动态场景表示。与隐式表示或静态点图不同，该表示在标准3D高斯溅射的基础上引入了高效的帧间变形机制：每个高斯原语在时间 $t$ 的均值、旋转和尺度分别通过可学习的位移向量 $\Delta\pmb{\mu}_p^t$、四元数乘法 $\pmb{q}_p^0 \otimes \Delta\pmb{q}_p^t$ 和加性调整 $\pmb{s}_p^0 + \Delta\pmb{s}_p^t$ 从初始状态演化而来。这种显式变形建模使得场景的动态演化可以被前馈网络直接预测，同时保持了渲染的几何一致性和计算效率。

**统一监督范式** 将流匹配损失、光度损失、几何损失和运动损失整合为单一训练目标：

$$\mathcal{L} = \mathcal{L}_{\mathrm{FM}} + \lambda_{photo}\mathcal{L}_{\mathrm{photo}} + \lambda_{geo}\mathcal{L}_{\mathrm{geo}} + \lambda_{motion}\mathcal{L}_{\mathrm{motion}}$$

其中 $\lambda_{photo}=1.0$，$\lambda_{geo}=0.5$，$\lambda_{motion}=2.0$。流匹配损失 $\mathcal{L}_{\mathrm{FM}}$ 确保扩散模型生成时序一致的潜变量序列；光度损失结合MSE和LPIPS约束新视角合成质量；几何损失通过预测深度与真实深度的余弦相似度惩罚几何不一致；运动损失基于3D点追踪，鼓励预测位移与真实位移一致。消融实验表明，移除运动损失导致FVD从210.15恶化至351.38（Table 4），验证了运动监督对动态视频质量的关键作用。

**渐进式训练策略** 进一步稳定了4D表示的学习过程：模型先在静态数据上预训练以获得稳健的3D几何先验，再引入动态数据进行联合训练。消融实验（Figure 7）显示，直接从动态数据训练会导致视觉质量下降，而渐进式策略在100K次迭代后产出更高的渲染质量。

### 相对于基线方法的范式转变

DIFF4SPLAT 在以下维度实现了对现有方法的根本性改进：

| 维度 | 优化式方法（Mosca、DimensionX） | 前馈隐式方法（Aether） | **DIFF4SPLAT** |
|------|-------------------------------|----------------------|----------------|
| **场景生成流程** | 两阶段：视频生成 → 逐场景4D优化 | 单阶段前馈，但使用隐式表示 | **单阶段前馈生成可变形3D高斯场** |
| **3D场景表示** | 隐式表示或静态高斯场 | 动态点图（隐式） | **显式可变形3D高斯表示** |
| **潜特征利用** | 仅用于2D帧生成 | 直接解码为点图 | **通过Video Latent Transformer解释为动态点云并回归高斯参数** |
| **运动建模** | 无显式帧间变形模块 | 隐式时序建模 | **可学习帧间变形（均值位移、旋转四元数、尺度调整）** |
| **监督范式** | 逐场景优化损失 | 前馈损失 | **统一前馈训练损失：流匹配+光度+几何+运动** |

这一范式转变带来了显著的效率提升：DIFF4SPLAT将动态场景生成时间压缩至约30秒，相较于优化式基线（Mosca约30分钟，DimensionX数小时）实现了60倍以上的加速。同时，显式几何表示使得相机位姿精度（平均相对位姿误差：平移0.012，旋转0.008）显著优于隐式表示方法（Table 3），验证了可变形高斯场在几何一致性上的优势。



DIFF4SPLAT 将动态 4D 场景生成重塑为一个**单阶段前馈过程**：给定一张单目图像、一条指定的相机轨迹，以及可选的文本提示，模型在一次前向传播中直接输出一个**可变形 3D 高斯场**，彻底消除了传统方法中耗时的测试时逐场景优化。

### 框架总览

整个 pipeline 由四个核心模块串联构成，如 Figure 1 和 Figure 2 所示：

![[assets/figures/papers/paper_list_l2462_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Diff4Splat_Repurpo/figures/001_Figure_1.jpg]]
*Figure 1: Given a single image, a specified camera trajectory, and an optional text prompt, our diffusion-based framework directly generates a deformable 3D Gaussian field without test-time optimization. The resulting representation supports diverse applications, including video generation, depth rendering, and novel view synthesis, enabling real-time rendering of dynamic scenes and interactive virtual exploration*

1. **预训练视频扩散模型（CogVideoX）**：以输入图像、文本和相机位姿（Plücker 嵌入）为条件，生成具有时空一致性的潜在张量 $\mathbf{z}$。该模型运行于 3D Causal VAE 的潜在空间，压缩方案为 $32 \times 4 \times 8 \times 8$。
2. **Latent Dynamic Reconstruction Model（LDRM）**：由 16 个标准 Transformer 块组成，将潜在张量和相机位姿编码拼接后，解码为高斯特征图与变形图。这是整个框架的**核心创新**——它桥接了 2D 时空特征与 4D 显式场景表示之间的鸿沟。
3. **可变形高斯场**：将 LDRM 的输出实例化为显式的 3D 高斯原语集合，每个原语包含均值 $\pmb{\mu}_p^0$、旋转 $\pmb{q}_p^0$、尺度 $\pmb{s}_p^0$、不透明度和颜色，并附加帧间变形参数（均值位移 $\Delta \pmb{\mu}_p^t$、旋转四元数增量 $\Delta \pmb{q}_p^t$、尺度调整 $\Delta \pmb{s}_p^t$）。
4. **可微光栅化器**：将变形后的高斯原语渲染为多视角 RGB 图像和深度图，用于损失计算与下游应用。

### 输入输出流

- **输入**：单张 RGB 图像 $\mathbf{I}_0 \in \mathbb{R}^{H \times W \times 3}$，相机位姿序列（以 Plücker 嵌入表示 $\mathcal{P} \in \bar{\mathbb{R}}^{T \times H \times W \times 6}$），可选文本提示。
- **输出**：可变形 3D 高斯场，支持实时渲染动态视频、新视角合成、深度图提取等应用（Figure 5）。
- **生成速度**：整个流程压缩至约 **30 秒**，相比优化式基线（如 Mosca 约 30 分钟、DimensionX 数小时）实现 **60 倍加速**。

### 训练范式

DIFF4SPLAT 采用**渐进式训练策略**：先在静态数据上预训练 3D 高斯场的几何与外观基础，再引入动态数据训练变形机制。消融实验（Figure 7）表明，直接从动态数据训练会导致几何初始化失败，而渐进式策略能显著提升视觉质量。训练目标由四项损失联合监督（详见 3.4 节）：流匹配损失 $\mathcal{L}_{\mathrm{FM}}$、光度损失 $\mathcal{L}_{\mathrm{photo}}$、几何损失 $\mathcal{L}_{\mathrm{geo}}$ 和运动损失 $\mathcal{L}_{\mathrm{motion}}$，权重分别为 $\lambda_{photo}=1.0$、$\lambda_{geo}=0.5$、$\lambda_{motion}=2.0$。

### 数据预处理

为获得带度量深度的 4D 训练数据，方法对 RealEstate10K 等仅提供相对位姿的数据集进行了**深度与位姿重估计**：利用 Video Depth Anything 和 MegaSaM 等基础模型恢复对齐的度量深度图与相机外参（Algorithm 1），最终积累了约 **13 万**高质量 4D 训练场景。



DIFF4SPLAT 的核心架构由四大模块构成：预训练视频扩散模型、Latent Dynamic Reconstruction Model (LDRM)、可变形高斯场，以及统一多损失监督。以下逐一剖析其设计逻辑与关键公式。

### 1. 视频扩散先验与条件嵌入

框架以 **CogVideoX** 作为预训练视频扩散 Transformer 主干，该模型在 3D Causal VAE 的潜空间中运行，压缩模式为 $32\times 4\times 8\times 8$。输入条件包括：单张图像 $\mathbf{I}_0 \in \mathbb{R}^{H \times W \times 3}$、文本提示（可选），以及相机位姿的 **Plücker 嵌入** $\mathcal{P} \in \bar{\mathbb{R}}^{T \times H \times W \times 6}$。扩散模型在前向过程中生成具有时空一致性的潜张量 $\mathbf{z}$，为下游的 3D 结构化预测提供紧凑的 2D 时空特征基。

### 2. Latent Dynamic Reconstruction Model (LDRM)

LDRM 是整个框架的表示转换枢纽，由 **16 个标准 Transformer 块** 构成。其核心任务是将扩散模型输出的潜变量 $\mathbf{z}$ 与相机位姿编码拼接后，解码为结构化的 3D 高斯属性。具体而言，LDRM 将潜特征解释为**动态点云**，并直接回归每个高斯原语在首帧的静态参数（均值 $\pmb{\mu}_p^0$、旋转四元数 $\pmb{q}_p^0$、尺度 $\pmb{s}_p^0$、不透明度与颜色），以及后续各帧的变形量。这一设计弥合了 2D 时空特征与 4D 动态场景之间的表示鸿沟，使单次前馈即可输出完整的可变形场景表示。

### 3. 可变形高斯场

为表征动态场景，DIFF4SPLAT 在静态 3D Gaussian Splatting 基础上引入帧间变形机制。每个高斯原语 $p$ 在空间点 $\mathbf{x}$ 处的响应由均值与协方差矩阵定义：

$$
\pmb{G}_p(\mathbf{x}) := \exp\left(-\frac{1}{2}(\mathbf{x} - \pmb{\mu}_p)^\top \pmb{\Sigma}_p^{-1}(\mathbf{x} - \pmb{\mu}_p)\right)
$$

在时间 $t$，原语的几何属性通过可学习的变形量从首帧状态更新：

- **均值位移**：$\pmb{\mu}_p^t := \pmb{\mu}_p^0 + \Delta\pmb{\mu}_p^t$
- **旋转更新**（四元数乘法）：$\pmb{q}_p^t := \pmb{q}_p^0 \otimes \Delta\pmb{q}_p^t$
- **尺度调整**（加性）：$\pmb{s}_p^t := \pmb{s}_p^0 + \Delta\pmb{s}_p^t$

变形后的高斯原语通过可微光栅化器渲染为多视角 RGB 图像与深度图，供后续损失计算使用。

### 4. 统一训练目标

总损失由四项加权组成，平衡系数为 $\lambda_{photo}=1.0$、$\lambda_{geo}=0.5$、$\lambda_{motion}=2.0$：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{FM}} + \lambda_{photo}\mathcal{L}_{\mathrm{photo}} + \lambda_{geo}\mathcal{L}_{\mathrm{geo}} + \lambda_{motion}\mathcal{L}_{\mathrm{motion}}
$$

**流匹配损失**（仅作用于扩散模型参数 $\theta$）训练向量场 $v_\theta$ 逼近真实向量场 $u_t$：

$$
\mathcal{L}_{\mathrm{FM}}(\theta) = \mathbb{E}_{t,p_t(\mathbf{z}^{(t)})} \left[ \| v_\theta(\mathbf{z}^{(t)},t) - u_t(\mathbf{z}^{(t)}) \|_2^2 \right]
$$

**光度损失**结合像素级 MSE 与感知相似度 LPIPS（$\lambda_p=0.5$），约束新视图合成质量：

$$
\mathcal{L}_{\mathrm{photo}} = \mathtt{MSE}(\hat{\mathbf{I}}^k, \mathbf{I}^k) + \lambda_p \cdot \mathtt{LPIPS}(\hat{\mathbf{I}}^k, \mathbf{I}^k)
$$

**几何损失**通过预测深度 $\hat{D}_k$ 与真实深度 $D_k^*$ 的归一化协方差（余弦相似度）惩罚几何不一致，并配合总变分正则项：

$$
\mathcal{L}_{\mathrm{geo}}(\hat{D}_k, D_k^*) = 1 - \frac{\operatorname{Cov}(\hat{D}_k, D_k^*)}{\sqrt{\operatorname{Var}(\hat{D}_k)\operatorname{Var}(D_k^*)}}
$$

**运动损失**基于 3D 点追踪，鼓励预测位移 $\Delta\hat{\mathbf{x}}_j$ 与真实位移 $\Delta\mathbf{x}_j$ 一致（$\lambda_m=2.0$），同时对预测位移施加 L1 稀疏正则：

$$
\mathcal{L}_{\mathrm{motion}} = \frac{1}{|\mathcal{O}|} \sum_{j\in\mathcal{O}} \left( \lambda_m \| \Delta\hat{\mathbf{x}}_j - \Delta\mathbf{x}_j \|_2 + \| \Delta\hat{\mathbf{x}}_j \|_1 \right)
$$

### 5. 渐进式训练策略

训练采用“先静后动”的课程式策略：首先在静态数据上预训练 3DGS 的几何与纹理基础，随后引入动态数据联合训练。消融实验（Figure 7）表明，直接从动态数据训练会导致几何初始化失败，而渐进式策略能稳定学习 4D 表示并获得更高的视觉质量。

### 补充图表

![[assets/figures/papers/paper_list_l2462_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Diff4Splat_Repurpo/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of DIFF4SPLAT. We present a high-fidelity dynamic 3DGS generation method from a single image through four key innovations: (1) video diffusion latents processed by our novel Transformer (Sec. 3.2), (2) a dynamic 3DGS deformation mechanism (Sec. 3.3), (3) unified supervision with photometric, geometric, and motion losses (Sec. 3.4), and (4) a progressive training scheme for robust geometry and texture*



## 实验与关键发现

### 主要结果

DIFF4SPLAT 在多个维度上展现出显著优势，其核心突破在于将动态4D场景生成从“优化式多阶段流程”转变为“单次前馈预测”，从而在保真度、几何一致性和效率之间取得突破。

**外观保真度与美学质量。** 如表1所示，DIFF4SPLAT 在 FVD（210.15）、KVD（2.316）、CLIP-Score（23.123）和 CLIP-Aesthetic（5.231）等指标上均达到或超越现有优化式方法。更重要的是，它将重建时间从优化式基线（Mosca 约30分钟，DimensionX 数小时）压缩至约30秒，实现60倍以上的加速。这一结果直接验证了核心因果机制——将视频扩散模型的生成先验与显式可变形3D高斯表示融合，彻底消除测试时逐场景优化。

**几何完整性与相机控制精度。** 表2显示，DIFF4SPLAT 在平均匹配数（5114.22）、主体一致性（88.32）和背景一致性（89.89）上均优于对比方法，同时保持30秒推理时间。表3进一步揭示，其平均相对位姿误差（RPE）在平移上仅0.012、旋转上仅0.008，显著低于隐式表示方法（如Aether）。这种几何精度的提升源于显式可变形高斯场——每个高斯原语在帧间通过均值位移、旋转四元数乘法和尺度加性调整进行连续演化，为相机位姿估计提供了可靠的3D对应点。

**定性对比。** 图3的定性对比显示，DIFF4SPLAT 生成的动态场景在视觉吸引力、时间一致性和几何保真度上均优于基线方法。图4进一步展示了极端视角下的鲁棒渲染结果，验证了显式几何表示在处理大视角变化时的优势。

### 消融实验

**运动损失的定量影响。** 表4的消融实验表明，移除运动损失（Motion Loss）后，FVD 从 210.15 急剧恶化至 351.38。运动损失基于3D点追踪，鼓励预测位移与真实位移一致（公式5），其权重 λ_motion=2.0 在总损失中占据主导地位。这一结果证明，运动监督对动态视频质量至关重要——仅靠光度损失和几何损失无法有效约束帧间变形的一致性。

**可变形高斯场的定性验证。** 图6显示，移除可变形高斯场模块（即仅使用静态场景表示）后，大运动区域出现明显的重影和撕裂伪影。这验证了变形机制的必要性：静态高斯场无法建模场景的动态演化，而帧间变形（均值位移 Δμ、旋转四元数更新 Δq、尺度调整 Δs）为每个高斯原语提供了灵活的运动表达能力。

**渐进式训练策略。** 图7的消融对比表明，采用“先静后动”的渐进式训练策略比直接从动态数据训练获得更高的视觉质量。这是因为静态预训练为3D高斯场提供了稳定的几何初始化，使后续的动态训练能够在可靠的几何先验上学习帧间变形，避免因同时学习几何和运动而陷入局部最优。

### 失败模式与局限性

尽管 DIFF4SPLAT 取得了显著进展，其性能仍受限于训练数据的覆盖范围。方法依赖大规模带标注的4D数据集（约13万个高质量4D训练场景），对极小物体或极快运动场景的生成效果可能不足。此外，当前框架基于 CogVideoX 预训练模型，其潜空间的压缩率（32×4×8×8）可能限制了对高频细节的保留能力。在完全无标注的真实世界视频上的泛化能力也尚未得到充分验证。

### 补充图表

![[assets/figures/papers/paper_list_l2462_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Diff4Splat_Repurpo/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of appearance fidelity and aesthetic quality. † denotes methods requiring per-scene optimization. We highlight first-place and second-place results*

![[assets/figures/papers/paper_list_l2462_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Diff4Splat_Repurpo/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparison with state-of-the-art methods. DIFF4SPLAT (last column) generates more visually appealing and temporally consistent 4D scenes with superior geometric fidelity compared to baselines. Kindly zoom in for details*

![[assets/figures/papers/paper_list_l2462_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Diff4Splat_Repurpo/figures/005_Table_4.jpg]]
*Table 4: Ablation Study on Motion Loss. We evaluate the impact of our proposed motion loss on dynamic video generation*

![[assets/figures/papers/paper_list_l2462_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Diff4Splat_Repurpo/figures/006_Table_2.jpg]]
*Table 2: Geometric integrity and reconstruction time. † denotes optimization-based methods. Best results are in bold, second best are underlined*

![[assets/figures/papers/paper_list_l2462_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Diff4Splat_Repurpo/figures/007_Table_3.jpg]]
*Table 3: Comparison of Average Relative Pose Error (RPE), highlighting our explicit model’s superior accuracy in translation and rotation, alongside its additional capabilities*

![[assets/figures/papers/paper_list_l2462_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Diff4Splat_Repurpo/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative results under extreme viewpoints*

![[assets/figures/papers/paper_list_l2462_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Diff4Splat_Repurpo/figures/009_Figure_5.jpg]]
*Figure 5: Applications of DIFF4SPLAT. Our method supports applications such as novel view synthesis and depth map extraction from the generated 4D representation*

![[assets/figures/papers/paper_list_l2462_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Diff4Splat_Repurpo/figures/010_Figure_6.jpg]]
*Figure 6: Ablation of the Deformation Gaussian Field. Removing this module (the red bounding boxes) results in ghosting artifacts, particularly in frames with large motion*

![[assets/figures/papers/paper_list_l2462_https_openaccess_thecvf_com_content_CVPR2026_html_Pan_Diff4Splat_Repurpo/figures/011_Figure_7.jpg]]
*Figure 7: Ablation on the progressive training strategy. Our approach (left) yields higher visual quality than direct dynamic training (right) after 100K iterations*



## 定位与知识库关联

### 1. 问题瓶颈与范式转换

现有动态4D场景生成方法普遍遵循“2D视频生成 → 逐场景4D优化”的两阶段范式。其核心瓶颈在于：**测试时逐场景优化**（per-scene optimization）过程极其昂贵——典型方法如 **Mosca** 需约30分钟，**DimensionX**（Sun et al., arXiv 2024）则需数小时，整个流程无法满足实时或交互式应用需求。

DIFF4SPLAT 通过**因果旋钮**（causal knob）实现范式转换：将视频扩散模型的生成先验与可变形3D高斯场的显式表示在统一框架内融合，用单次前馈预测直接输出动态4D场景，彻底消除测试时的逐场景优化。其核心洞察在于：视频扩散模型的潜变量可视为具有时空连续性的动态点云，通过条件Transformer将其映射为3D高斯属性和帧间变形，从而在保真度、几何一致性和效率之间取得突破。

### 2. 关键改进槽位对比

下表从五个关键维度对比DIFF4SPLAT与基线方法的差异：

| 改进槽位 | 基线方法取值 | DIFF4SPLAT取值 |
|---------|------------|---------------|
| 场景生成流程 | 两阶段：视频生成 → 逐场景4D优化 | 单阶段前馈生成可变形3D高斯场 |
| 3D场景表示 | 隐式表示或动态点图 | 显式可变形3D高斯表示（含均值、旋转、尺度的帧间变形） |
| 潜特征利用 | 视频扩散模型仅用于2D帧生成 | 通过Video Latent Transformer将潜变量解释为动态点云并回归3D高斯参数 |
| 运动建模 | 无显式帧间变形模块 | 可学习帧间变形（均值位移、旋转四元数乘法、尺度加性调整） |
| 监督范式 | 逐场景优化损失 | 统一前馈训练损失：Flow Matching + 光度 + 几何 + 运动损失 |

### 3. 与相关工作的关系定位

**优化式动态4D生成方法**：**Mosca** 和 **DimensionX** 代表基于逐场景优化的路线，虽能生成较高质量结果，但推理时间在半小时至数小时量级。DIFF4SPLAT 以约30秒的推理时间实现60倍加速，且生成质量达到或超过优化方法（FVD 210.15，Table 1），证明前馈范式可替代昂贵的测试时优化。

**前馈动态点图方法**：**Aether**（Zhu et al., arXiv 2025）采用前馈动态点图生成，但使用隐式表示，渲染存在空洞和伪影。DIFF4SPLAT 改用显式可变形3D高斯表示，在几何完整性（Avg. Matches 5114.22，Table 2）和相机位姿精度（Avg.RPE Translation 0.012 / Rotation 0.008，Table 3）上显著优于隐式表示方法。

**视频扩散模型蒸馏路线**：**Lyra** 探索了基于视频扩散模型与3DGS蒸馏的动态生成，DIFF4SPLAT 在此基础上进一步引入Video Latent Transformer，弥合2D时空特征与4D动态场景之间的表示鸿沟，并设计了包含运动损失的统一监督方案。

### 4. 适用边界与局限

- **数据依赖性**：方法依赖大规模带标注的4D数据集（约130,000个高质量训练场景），对极小或极快运动场景的生成效果可能仍有不足。
- **模型体量**：基于CogVideoX预训练视频扩散模型和16个标准Transformer块的LDRM模块，模型体积较大，尚未针对移动端或实时交互场景进行压缩优化。
- **时序长度**：当前框架主要针对固定长度的动态场景生成，扩展到更长时序或开放域动态场景的能力有待验证。
- **真实场景泛化**：在完全无标注的真实世界视频上，模型的泛化能力尚未得到系统性评估。

### 5. 开放问题

1. **模型压缩与加速**：如何进一步压缩模型体积与推理时间，以支持移动端或实时交互应用？
2. **长时序扩展**：能否将框架扩展到更长时序或开放域的动态场景生成，例如分钟级或无限时长场景？
3. **无监督/自监督泛化**：在完全无标注的真实世界视频上，模型能否通过自监督或弱监督方式学习动态场景先验？
4. **多模态条件融合**：当前支持单图、文本和相机位姿作为条件输入，能否融合更多模态（如音频、草图）以实现更灵活的场景控制？



## 原文 PDF

![[paperPDFs/CVPR_2026/Diff4Splat_Repurposing_Video_Diffusion_Models_for_Dynamic_Scene_Generation.pdf]]
