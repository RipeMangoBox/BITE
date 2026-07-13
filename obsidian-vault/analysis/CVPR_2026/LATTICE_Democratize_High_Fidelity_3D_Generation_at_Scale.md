---
title: "LATTICE: Democratize High-Fidelity 3D Generation at Scale"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LATTICE_Democratize_High_Fidelity_3D_Generation_at_Scale.pdf
project_link: "https://lattice3d.github.io"
code_link: null
aliases:
- LATTICE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将VecSet中的点查询（point queries）替换为体素查询（voxel queries），使潜在向量锚定在粗体素网格上，从而在去噪时显式注入空间位置嵌入，实现可定位的结构化生成。
primary_logic: 3D扩散生成器成功的关键在于“可定位性（localizability）”而非单纯的体素结构。通过将“何处放置内容”与“放置什么内容”解耦为粗结构→精细几何两阶段生成，并利用体素坐标提供位置指导，VoxSet实现了简洁的纯Transformer架构、低成本渐进训练和强大的测试时缩放，缩小了与2D生成模型的差距。
claims:
- 模型缩放实验中，VoxSet架构从0.6B扩展到4.5B能持续产生更精细的几何，而VecSet模型则表现饱和。
- 测试时缩放表明，训练时最多使用6144个token的模型，在推理时直接增加到30720个token仍能带来一致性的质量提升。
- 引入体素查询和RoPE位置嵌入后，生成结果的伪影显著减少，细节保真度明显提高。
- Image-to-Geometry (ULIP/Uni3D相似度) 上 ULIP-T (↑) = 0.078
---

# LATTICE: Democratize High-Fidelity 3D Generation at Scale

> [!tip] 核心洞察
> 3D扩散生成器成功的关键在于“可定位性（localizability）”而非单纯的体素结构。通过将“何处放置内容”与“放置什么内容”解耦为粗结构→精细几何两阶段生成，并利用体素坐标提供位置指导，VoxSet实现了简洁的纯Transformer架构、低成本渐进训练和强大的测试时缩放，缩小了与2D生成模型的差距。

| 字段 | 内容 |
|------|------|
| 中文题名 | LATTICE：实现大规模高保真3D生成的民主化 |
| 英文题名 | LATTICE: Democratize High-Fidelity 3D Generation at Scale |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.03052) · [Project](https://lattice3d.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LATTICE |
| Dataset | Image-to-Geometry |

> [!tip] 效果简介
> - Image-to-Geometry (ULIP/Uni3D相似度) 上，ULIP-T (↑) 0.078 vs 所有开源方法最佳 (新基准最优)；Uni3D-Fine (↑) 0.315 vs 所有开源方法最佳 (新基准最优)。
> - 几何重建 (LATTICE-Bench(R)) 上，Chamfer Distance (↓) / F-score (↑) 多尺度最优（详细数值见论文） vs 现有VAE方法。

## 概要

**问题瓶颈**：现有基于VecSet的高效3D生成方法在压缩与重建上表现优异，但其潜在表示完全无结构——潜在向量是无序集合，扩散生成过程中无法利用空间位置信息。这导致模型在提升几何细节质量和扩大规模时遭遇严重瓶颈，与2D扩散模型之间的可扩展性差距持续存在。

**核心洞察**：3D扩散生成器成功的关键不在于“局部性”（locality），而在于测试时是否具备已知的空间结构——即可定位性（localizability）。将“何处放置内容”与“放置什么内容”解耦，是缩小与2D生成模型差距的根本路径。

**提出方法**：LATTICE围绕**VoxSet**这一半结构化潜在表示构建。VoxSet将VecSet中的点查询替换为锚定在粗体素网格中心的体素查询，使潜在向量获得显式的空间坐标。在此基础上，LATTICE采用两阶段粗到细流水线：第一阶段利用现成模型生成粗体素结构作为空间锚点，第二阶段通过带旋转位置嵌入（RoPE）的整流流扩散变换器（DiT）生成VoxSet细节几何。该设计实现了简洁的纯Transformer架构、低训练成本（2B模型在64 GPU上训练不足24小时）以及从0.6B到4.5B参数的平滑缩放能力。

**关键结果**：
- **模型缩放**：VoxSet架构从0.6B扩展到4.5B持续产生更精细的几何，而VecSet模型表现饱和（Figure 12）。
- **测试时缩放**：训练时最多使用6,144个token的模型，在推理时直接增加到30,720个token仍带来一致性质量提升（Figure 2, Figure 13）——这是VecSet方法无法实现的。
- **生成质量**：在图像到几何生成的ULIP和Uni3D相似度指标上达到开源方法最优（Table 2），几何重建在LATTICE-Bench(R)上取得多尺度最优（Table 1）。

**方法定位**：LATTICE在方法谱系上属于**半结构化潜在扩散生成**，连接了VecSet的高效压缩与结构化体素的空间感知。与Trellis (SLAT)等稀疏体素方法不同，VoxSet保留VecSet的交叉注意力压缩机制，仅通过体素查询注入结构；与CLAY、Michelangelo、TripoSG、Step1X-3D等VecSet基线相比，核心差异在于将无结构序列转化为可定位的半结构化序列。



### 3D生成模型的规模化困境

近年来，大规模2D图像与视频扩散模型取得了令人瞩目的进展，其成功很大程度上得益于潜在空间的结构化特性——潜在向量与像素/体素网格保持空间对应关系，使得扩散生成器能够利用位置信息进行高效的去噪建模。然而，3D生成领域在追求规模化时却面临一个根本性瓶颈：**高效率的潜在表示与可定位的结构信息之间存在尖锐矛盾**。

当前主流的3D生成方法可分为两条技术路线。一条路线采用稠密体素（dense voxel）或三平面（tri-plane）等结构化表示，这些表示天然携带空间位置信息，但计算和存储开销随分辨率呈立方增长，难以扩展到大规模训练。另一条路线采用基于集合的潜在表示（VecSet），如 **Hunyuan3D-2**、**CLAY**、**Michelangelo**、**TripoSG** 和 **Step1X-3D** 等方法，通过交叉注意力将3D资产压缩为一组无序的潜在向量。VecSet在压缩效率和重建质量上表现优异，但其潜在空间完全无结构——向量之间没有空间位置关系，扩散生成器在去噪时无法获知“内容应放置在何处”，这严重限制了模型提升细节质量和扩大规模的能力。

### 核心瓶颈：可定位性的缺失

本文识别出这一困境的本质原因：**3D扩散生成器成功的关键不在于“局部性”（locality），而在于“可定位性”（localizability）——即测试时潜在向量与空间位置的对应关系是否已知且可利用**。

在VecSet框架下，潜在向量通过点查询（point queries）从物体表面采样得到。训练时，这些查询点的位置是已知的；但在生成阶段，扩散器需要同时预测“何处放置内容”和“放置什么内容”，这构成了一个高度不适定的联合优化问题。实验证据表明，即使将VecSet模型参数从0.6B扩展到4.5B，其生成质量也趋于饱和（Figure 12），说明单纯增加模型容量无法弥补结构信息的缺失。

### 从“体素化”到“可定位”：VoxSet的动机

直观上，体素网格似乎能解决上述问题——体素天然提供规则的空间结构。但传统体素表示的高计算成本使其不适合大规模生成。本文提出一个关键洞察：**生成器所需的并非完整的稠密体素，而仅仅是测试时可用的粗粒度空间锚点**。这一观察催生了VoxSet表示：将VecSet中的点查询替换为体素查询（voxel queries），使每个潜在向量锚定在一个粗体素网格的中心。这样，VoxSet既保留了VecSet的压缩效率，又为扩散生成器提供了显式的空间位置指导，实现了“半结构化”的潜在空间。

基于VoxSet，LATTICE采用两阶段流水线：第一阶段利用现成模型生成粗体素结构锚点，第二阶段在该结构引导下生成精细几何细节。这种“结构→细节”的解耦策略，使得扩散器只需专注于“放置什么内容”，而“何处放置”由已知的体素坐标提供，从而显著降低了生成难度，并展现出VecSet所不具备的**测试时缩放能力**——训练时使用6144个token的模型，在推理时可直接扩展到30720个token并持续获得质量提升（Figure 2）。



## 核心方法与创新机理

LATTICE的核心创新在于对3D扩散生成中“表示”这一根本问题的重新审视。现有基于VecSet的高效3D生成方法（如**Hunyuan3D-2**、**CLAY**、**Michelangelo**、**TripoSG**、**Step1X-3D**）在压缩与重建上表现优异，但其潜在表示是无结构的——潜在向量构成一个无序集合，扩散变换器在去噪时无法获得任何空间位置信息。这导致模型在提升细节质量和扩大规模时遭遇瓶颈：生成器不知道“在哪里放置内容”，只能依赖隐式的统计关联，伪影难以消除，模型缩放也迅速饱和。

LATTICE的核心洞察是：**3D扩散生成器成功的关键在于“可定位性（localizability）”，而非单纯的体素结构或局部性。** 只要在测试时能够为每个潜在向量提供确定的空间坐标，生成器就能学会将“何处放置内容”与“放置什么内容”解耦，从而在简洁的架构下实现强大的缩放能力。

### 关键机制变更（Changed Slots）

| 组件 | 基线方案（VecSet类方法） | LATTICE方案（VoxSet） |
|------|------------------------|----------------------|
| **潜在表示查询类型** | 点查询（Point Queries）：在物体表面采样，测试时位置未知 | 体素查询（Voxel Queries）：锚定在粗体素网格中心，测试时位置已知 |
| **扩散变换器位置编码** | 无位置编码（非结构化序列） | 基于体素坐标的旋转位置嵌入（RoPE） |
| **多分辨率训练策略** | 固定分辨率训练 | 查询抖动训练（添加均匀随机偏移），支持推理时任意分辨率 |
| **生成流水线** | 单阶段VecSet扩散生成 | 两阶段：粗体素结构→VoxSet细节生成 |

### 从“无结构”到“半结构化”的表示跃迁

VecSet将3D资产压缩为一组无位置锚定的潜在向量，训练时通过交叉注意力在物体表面采样查询点，但测试时这些点的位置无从得知。LATTICE的VoxSet将查询点替换为**体素查询**——每个潜在向量锚定在一个粗体素网格的活跃体素中心。这一改动看似微小，却带来了根本性的变化：扩散变换器在去噪时，可以通过体素坐标获得显式的空间位置指导，从而在生成过程中实现“可定位”的结构化建模。

为支持灵活的多分辨率推理，LATTICE引入了**查询抖动训练**策略：训练时对点查询添加均匀随机偏移 $\epsilon \sim U \left[ \frac{-1}{2R}, \frac{1}{2R} \right]$，使VAE学会处理任意分辨率的查询位置。这使得模型在推理时可以使用远超训练分辨率的token数量（从6144增至30720），持续获得质量提升。

### 两阶段粗到细生成流水线

LATTICE将生成过程解耦为两个阶段：
1. **粗体素结构生成**：利用现成模型（如Hunyuan3D-2或**Trellis (SLAT)**）生成粗网格并体素化，获得测试时可用的体素结构锚点。这一阶段确定“何处放置内容”。
2. **VoxSet细节生成**：在粗体素结构指导下，使用整流流扩散变换器（DiT）配合RoPE位置嵌入，去噪生成VoxSet潜在向量，再通过SDF解码器重建高保真几何。这一阶段决定“放置什么内容”。

这种解耦设计使得LATTICE能够以纯Transformer架构、低成本渐进训练实现强大的测试时缩放，缩小了3D生成与2D扩散模型在质量和可扩展性上的差距。消融实验（Figure 10, Section 4.3）表明，体素查询替代点查询显著减少伪影，查询抖动训练优于固定分辨率训练（Table 3），向DiT添加RoPE位置嵌入加速收敛并提升生成质量。模型缩放实验（Figure 12）进一步证实：VoxSet架构从0.6B扩展到4.5B持续产生更精细的几何，而VecSet模型则表现饱和——这直接验证了“可定位性”是3D扩散生成规模化的关键瓶颈。



LATTICE 采用**两阶段粗到细（coarse-to-fine）生成流水线**，其核心是将“何处放置内容”与“放置什么内容”解耦：第一阶段生成稀疏的粗体素结构锚点，第二阶段在该结构引导下生成高保真几何细节。整个系统围绕一种新的半结构化潜在表示 **VoxSet** 构建，该表示将 3D 资产压缩为一组锚定在粗体素网格上的潜在向量，从而在扩散生成过程中显式注入空间位置信息。

### 流水线模块与数据流

**第一阶段：粗体素结构生成器**
- 输入：单张图像（或文本等多模态条件）。
- 处理：利用现成的 3D 生成模型（如 Hunyuan3D-2 或 Trellis）从输入图像生成粗网格，随后对该粗网格进行体素化（voxelization），得到一个稀疏的体素网格。
- 输出：测试时已知的**稀疏体素结构锚点**，明确了后续细节生成中“何处放置内容”的空间框架。

**第二阶段：VoxSet VAE 编码器**
- 输入：原始 3D 资产的点云表示 $P \in \mathbb{R}^{N \times 7}$，其中每个点编码 3D 坐标、表面法线和锐利边缘二值指示符。
- 处理：通过交叉注意力（cross-attention）机制将输入点云压缩为一组固定数量的潜在向量（latent tokens）。每个潜在向量对应一个**体素查询（Voxel Query）**，该查询锚定在粗体素网格中与物体表面相交的活跃体素中心。
- 关键设计：训练时对查询位置添加均匀随机抖动 $\epsilon \sim U \left[ \frac{-1}{2R}, \frac{1}{2R} \right]$，使模型在推理时能支持任意大于训练分辨率 $R$ 的体素分辨率。
- 输出：**VoxSet 潜在表示**——一组空间锚定的潜在向量序列。

**第二阶段：整流流扩散变换器（DiT）+ RoPE**
- 输入：第一阶段生成的粗体素结构（作为条件），以及噪声化的 VoxSet 潜在向量。
- 处理：基于体素坐标的**旋转位置嵌入（RoPE）**被注入扩散变换器，使去噪过程具备显式的空间感知能力。模型采用整流流（rectified flow）目标进行去噪生成。
- 关键能力：由于潜在向量锚定在已知体素网格上，模型在推理时可以将 token 数量从训练时的最多 6,144 个扩展到 30,720 个，实现**测试时缩放（test-time scaling）**并持续获得质量提升。
- 输出：去噪后的 VoxSet 潜在向量。

**第二阶段：SDF 解码器**
- 输入：去噪后的 VoxSet 潜在向量。
- 处理：通过交叉注意力从潜在向量重建有向距离场（SDF），随后使用 Marching Cubes 算法提取多边形网格。
- 输出：高保真 3D 几何网格。

### 架构核心：VoxSet 表示

VoxSet 是 LATTICE 的核心创新，其设计动机源于对现有 VecSet 方法瓶颈的洞察：VecSet 的潜在向量是无结构的点查询（point queries），测试时位置未知，导致扩散生成器无法有效利用空间位置信息。VoxSet 将点查询替换为**体素查询**，使潜在向量锚定在粗体素网格中心，从而在保持 VecSet 压缩效率和简洁性的同时，为扩散生成器提供了关键的**可定位性（localizability）**。这使得整个流水线可以采用纯 Transformer 架构、低成本渐进训练，并具备强大的测试时缩放能力。

### 输入输出流总览

单张图像 → **[第一阶段]** 粗体素结构 → **[第二阶段 DiT + RoPE]** 去噪生成 VoxSet 潜在向量 → **[SDF 解码器]** 高保真 3D 网格

> **注意**：当前流水线专注于几何生成，未包含纹理或材质生成模块。完整的 PBR 资产创建需额外步骤。

### 补充图表

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/003_Figure_3.jpg]]
*Figure 3: LATTICE system: At its core is a novel VoxSet representation, enabling scalable 3D modeling from 0.6B to 4.5B*

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/005_Figure_5.jpg]]
*Figure 5: LATTICE Model Architecture: it features a two-stage coarse-to-fine pipeline and a novel VoxSet VAE and DiT*



LATTICE的核心在于将3D潜在表示从无结构的**VecSet**升级为半结构化的**VoxSet**，并围绕这一表示构建了可定位的扩散生成流水线。以下逐一拆解关键模块及其公式。

### 1. VoxSet VAE：体素查询驱动的压缩与重建

VoxSet VAE负责将任意3D资产压缩为一组锚定在粗体素网格上的潜在向量。其输入为点云 $P \in \mathbb{R}^{N \times 7}$，其中 $N$ 为点数，每个点编码其3D坐标、表面法线和一个二值锐利边缘指示符。编码器通过交叉注意力（cross-attention）将点云信息聚合到一组体素查询（Voxel Queries）上，生成潜在向量序列。解码器则从这些潜在向量出发，同样通过交叉注意力重建有向距离场（SDF），最终使用Marching Cubes提取多边形网格。

与VecSet的核心差异在于查询类型：VecSet使用在物体表面采样的**点查询**（point queries），其在测试时位置未知；VoxSet则使用锚定在粗体素网格中心的**体素查询**（voxel queries），测试时位置已知。这一替换使得潜在空间具备了显式的空间结构，为后续扩散生成提供了可定位性基础。

### 2. 查询抖动训练：支持多分辨率推理

为使VAE在推理时能灵活适配任意体素分辨率 $R$，训练阶段对点查询施加随机偏移：

$$\epsilon \sim U\left[-\frac{1}{2R}, \frac{1}{2R}\right]$$

该偏移服从均匀分布，范围由目标分辨率 $R$ 决定。查询抖动（Query Jitter）策略使模型在训练时即见过不同位置的查询，从而在推理时可直接增加体素分辨率（即增加token数量）而无需重新训练。消融实验（Table 3）证实该策略优于固定分辨率训练，并为测试时缩放奠定了基础。

### 3. 整流流扩散变换器 + RoPE位置嵌入

扩散生成器采用整流流（rectified flow）目标训练的DiT架构，对VoxSet潜在向量进行去噪。关键创新在于向DiT注入基于体素坐标的旋转位置嵌入（RoPE），使模型在去噪过程中显式感知每个潜在向量对应的空间位置。

这一设计的因果逻辑是：**“可定位性（localizability）”是3D扩散生成器成功的关键**。VecSet的潜在向量是无结构序列，DiT无法获知“何处放置内容”；VoxSet通过体素坐标提供位置指导，将“放置位置”与“放置内容”解耦，使纯Transformer架构即可高效利用空间信息，无需引入稀疏卷积等复杂结构。

### 4. 两阶段粗到细生成流水线

完整生成流水线分为两阶段：

- **第一阶段：粗体素结构生成。** 利用现成模型（如Hunyuan3D-2或Trellis）生成粗网格并体素化，得到测试时可用的体素结构锚点。该阶段确定“何处放置内容”。
- **第二阶段：VoxSet细节生成。** 在粗体素网格约束下，DiT+RoPE去噪生成VoxSet潜在向量，再由SDF解码器重建精细几何。该阶段确定“放置什么内容”。

两阶段设计将结构定位与细节生成解耦，使得第二阶段可专注于高保真几何建模，同时支持测试时通过增加体素分辨率（token数量）来持续提升细节质量。

### 补充图表

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/004_Figure_4.jpg]]
*Figure 4: Illustrations of different latent representations and different query types*

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of test-time scaling in our model. The model is trained with up to 6,144 tokens, but is evaluated under different token counts at test time, showing notable improvements*

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/006_Figure_6.jpg]]
*Figure 6: Illustration of model/training and test scaling effects*



## 实验与关键发现

### 几何重建能力验证

LATTICE的VoxSet VAE首先在几何重建任务上进行验证。Table 1报告了在LATTICE-Bench(R)上与其他VAE方法的定量对比，采用Chamfer Distance（↓）和F-score（↑）作为指标。VoxSet VAE在多尺度设置下均取得了最优的重建精度，验证了体素查询（voxel queries）相较于点查询（point queries）在压缩-重建任务上的优势。这一优势的因果机制在于：体素查询锚定在已知的粗体素网格中心，编码器和解码器共享明确的空间对应关系，从而减小了潜在空间的域差距。

### 图像到几何生成主结果

Table 2给出了图像到几何生成任务在ULIP和Uni3D相似度指标上的全面对比。LATTICE-1.9B在所有开源方法中取得了最优性能：

- **ULIP-T（↑）**：0.078
- **ULIP-I（↑）**：0.130
- **Uni3D-Fine（↑）**：0.315

这些指标衡量生成几何与输入图像在跨模态嵌入空间中的语义一致性。值得注意的是，LATTICE在ULIP和Uni3D两个互补的评估维度上均超越了现有开源基线，包括Hunyuan3D-2、Trellis (SLAT)、CLAY、Michelangelo、TripoSG和Step1X-3D。Figure 8提供了与这些方法的可视化对比，LATTICE生成的几何在细节保真度和结构完整性上表现出一致的优势。

Figure 9进一步展示了与商业模型（如Meshy-5.0、Rodin-2.0）的视觉对比。LATTICE在保持开源可复现性的前提下，生成了具有竞争力的高保真几何结果。

### 用户研究

Figure 11报告了用户研究结果，以获胜率（%）衡量。LATTICE在Overall、Subject和Scene三个类别上均显著优于对比方法。这一主观评估与Table 2的客观指标相互印证，表明VoxSet生成的几何在人类感知层面同样具有更高的质量。

### 消融实验

#### 体素查询与VoxSet VAE的增量贡献

Figure 10通过逐步添加各个组件，消融了体素查询和VoxSet VAE的贡献。核心发现是：

- **体素查询替代点查询**显著减少了生成伪影。这是因为体素查询在测试时具有已知的空间位置，扩散变换器可以依赖这一结构化信息进行去噪，而非像VecSet那样处理无结构序列。
- **VoxSet VAE**凭借更强的重建能力引入了更多细节。两个组件的叠加带来了生成质量的飞跃。

#### 查询抖动训练策略

Table 3消融了查询抖动（Query Jitter）训练策略。结果表明，使用抖动训练（在训练时对查询添加均匀随机偏移 $\epsilon \sim U \left[ \frac { - 1 } { 2 R } , \frac { 1 } { 2 R } \right]$）的VAE优于固定分辨率训练的VAE，并且在应用于不同分辨率时提供了更大的灵活性。这一策略是实现测试时缩放的关键使能技术。

#### 位置嵌入的贡献

向扩散变换器（DiT）添加基于体素坐标的旋转位置嵌入（RoPE）加速了模型收敛并提升了生成质量（Section 3.2, Figure 6）。RoPE为原本无结构的潜在向量序列注入了空间感知能力，使去噪网络能够利用“何处放置内容”的位置信息，从而更有效地分配建模容量。

### 模型缩放实验

Figure 12展示了模型参数缩放对性能的影响，这是验证VoxSet架构可扩展性的决定性证据。**VecSet模型**随着参数量增加（0.6B→4.5B）表现出明显的性能饱和，细节提升有限；而**VoxSet模型**在相同参数量增长范围内持续产生更精细的几何细节。这一对比揭示了核心洞察：结构化潜在表示（VoxSet）是3D扩散生成器实现模型缩放的瓶颈突破点——无结构的VecSet无法有效利用额外参数，而VoxSet通过体素坐标锚定提供了可定位性，使更大模型能够学习更丰富的局部几何先验。

### 测试时缩放实验

Figure 13展示了测试时形状token数量缩放的效果，这是VoxSet区别于VecSet的另一关键优势。训练时最多使用6,144个token的模型，在推理时直接增加到30,720个token（约5倍于训练设置）仍能带来一致性的质量提升。相比之下，VecSet模型在token数增加时收益有限，较早出现饱和。这一现象的根本原因在于：VoxSet的体素查询具有明确的空间坐标，增加token数量等价于提高体素网格分辨率，扩散变换器可以自然地利用RoPE位置嵌入将去噪推广到更密集的空间采样；而VecSet的无结构序列缺乏这种空间泛化能力。

### 失败模式与局限

尽管LATTICE在多项指标上取得了最优结果，仍存在以下局限：

1. **两阶段依赖**：第一阶段粗体素结构的质量直接影响最终细节。若现成模型（如Hunyuan3D-2或Trellis）生成的粗网格存在缺失或错误体素，第二阶段无法弥补这些结构性缺陷。
2. **几何专精**：当前模型仅生成几何，未包含纹理或材质生成，完整的PBR资产创建需要额外的纹理合成步骤。
3. **推理资源需求**：尽管训练成本已大幅降低（2B模型在64 GPU上训练不到24小时），4.5B参数模型的推理仍需高端GPU，限制了在消费级设备上的部署。

### 关键图表索引

- **Table 1**：几何重建定量对比，验证VoxSet VAE的压缩-重建能力。
- **Table 2**：图像到几何生成的ULIP/Uni3D相似度数值对比，LATTICE在所有开源方法中取得最优。
- **Figure 10**：体素查询与VoxSet VAE的增量消融，揭示各组件的独立贡献。
- **Figure 11**：用户研究获胜率，主观评估与客观指标一致。
- **Figure 12**：模型参数缩放实验，证明VoxSet的可扩展性优于VecSet。
- **Figure 13**：测试时token数量缩放实验，证明VoxSet的测试时缩放能力。

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/009_Table_1.jpg]]
*Table 1: Quantitative comparisons of geometry reconstruction*

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/011_Table_2.jpg]]
*Table 2: Numerical comparison of geometry generation performance on ULIP [49] and Uni3D [61] similarities.LATTICMeshy-5.0 Rodin-2.0*

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/014_Figure_10.jpg]]
*Figure 10: Ablation study on the proposed voxel query and VoxSet VAE, by incrementally adding each component*

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/015_Figure_12.jpg]]
*Figure 12: Illustration of the effect of model scaling (in parameters) on performance. VecSet models show limited improvement as parameters increase, whereas larger VoxSet models produce finer and more detailed results*

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/016_Figure_13.jpg]]
*Figure 13: Illustration of the effect of test-time scaling (in shape tokens) on model performance. VecSet models exhibit limited gains as the number of tokens increases, showing early saturation. In contrast, VoxSet models consistently benefit from higher token counts, producing finer details and demonstrating stronger scaling capability. * indicates the token count used during training*

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/012_Figure_11.jpg]]
*Figure 11: User study of our method against competitors showing win rate (%) across Overall, Subject, and Scene categories*

### 补充图表

![[assets/figures/papers/paper_list_l2533_https_arxiv_org_abs_2512_03052/figures/008_Figure_8.jpg]]
*Figure 8: Visual comparison of geometry generation against several state-of-the-art open-source methods*



## 定位与知识库关联

### 1. 核心瓶颈与因果机制

现有基于VecSet的高效3D生成方法（如**3DShape2VecSet**、**CLAY**、**Michelangelo**、**TripoSG**、**Step1X-3D**）在压缩与重建上表现优异，但其潜在表示本质上是**无结构的**——潜在向量是一组无序集合，在扩散生成过程中无法利用空间位置信息。这一结构性缺陷构成了关键瓶颈：扩散变换器在去噪时缺乏“何处放置内容”的位置指导，严重限制了模型提升细节质量和扩大规模的能力。

LATTICE的因果调节变量是**将点查询替换为体素查询**，使潜在向量锚定在粗体素网格中心。这一改动引入了测试时已知的空间位置信息，使扩散生成器获得了**可定位性**——这是3D扩散生成器成功的关键，而非单纯的体素结构本身。通过将“何处放置内容”与“放置什么内容”解耦为粗结构→精细几何两阶段生成，VoxSet实现了简洁的纯Transformer架构、低成本渐进训练和强大的测试时缩放能力。

### 2. 方法谱系定位

#### 2.1 与VecSet系方法的关系

LATTICE直接继承自**3DShape2VecSet**的VecSet压缩范式，但对其核心缺陷进行了针对性修正：

- **3DShape2VecSet**（Zhang et al.）：奠定了通过交叉注意力将3D资产压缩为潜在向量集合的基础框架，但潜在向量是无序、无结构的集合，扩散生成时缺乏空间感知。
- **CLAY**：大规模VecSet扩散生成基线，受限于无结构表示，模型缩放时性能饱和。
- **Michelangelo**：在VecSet框架下实现形状-图像-文本对齐，但同样面临无结构表示带来的生成质量瓶颈。
- **TripoSG**、**Step1X-3D**：基于整流流的高保真VecSet生成方法，在细节表现上优于早期工作，但仍无法突破无结构表示的根本限制。

LATTICE的VoxSet通过将潜在向量锚定在体素网格上，**在保持VecSet压缩效率的同时注入了空间结构**，使扩散变换器能够利用位置嵌入进行空间感知的去噪生成。消融实验（Figure 10）表明，Voxel Queries替代Point Queries显著减少伪影，得益于更小的域差距。

#### 2.2 与结构化体素方法的关系

**Trellis (SLAT)** 采用结构化稀疏体素进行3D生成，证明了体素结构对生成质量的价值。但Trellis的体素表示是显式的、稠密的几何载体，而VoxSet的体素查询是**半结构化的潜在表示**——体素网格仅作为潜在向量的空间锚点，实际几何细节由潜在向量通过交叉注意力解码生成。这种设计既保留了体素结构的空间可定位性，又继承了VecSet的压缩效率和表达能力。

#### 2.3 与两阶段生成范式的关系

LATTICE的两阶段流水线（先粗结构后精细几何）与**Hunyuan3D-2**等现成模型形成互补：第一阶段可直接利用Hunyuan3D-2或Trellis生成的粗网格进行体素化，获得测试时可用的体素结构锚点；第二阶段在此结构指导下生成VoxSet细节。这种设计使LATTICE能够灵活接入不同的粗结构生成器，同时将自身聚焦于精细几何生成这一核心能力。

### 3. 技术贡献的适用边界

#### 3.1 有效范围

- **几何生成**：VoxSet专注于几何表示与生成，在ULIP/Uni3D相似度指标上达到开源方法最优（Table 2），在LATTICE-Bench(R)重建基准上多尺度最优（Table 1）。
- **模型缩放**：从0.6B到4.5B参数，VoxSet架构持续产生更精细的几何，而VecSet模型则表现饱和（Figure 12）。
- **测试时缩放**：训练时最多使用6144个token的模型，推理时直接增加到30720个token仍能带来一致性的质量提升（Figure 2, Figure 13）。

#### 3.2 已知局限

- **第一阶段依赖**：两阶段流水线依赖现成的第一阶段模型生成粗体素结构，粗结构中的错误或缺失体素无法在第二阶段弥补，形成质量上限。
- **无纹理/材质生成**：当前模型专注于几何生成，未包含纹理或材质生成，完整的PBR资产创建尚需额外步骤。
- **推理成本**：尽管训练成本已大幅降低（2B模型可在64块GPU上24小时内完成训练），但4.5B参数模型的推理仍需要高端GPU，限制了在消费级设备上的部署。

### 4. 开放问题与未来方向

1. **与2D生成模型的差距**：如何进一步缩小3D生成模型与2D图像/视频扩散模型在质量和可扩展性上的差距？VoxSet已证明结构注入是关键方向，但更本质的位置信息编码方式仍有探索空间。

2. **多模态条件扩展**：VoxSet表示能否直接扩展到多模态条件（如文本、多视角输入）而无需复杂的结构适应？当前设计以图像条件为主，向其他模态的泛化能力尚待验证。

3. **更高分辨率体素网格**：如何在保持VoxSet效率的同时，支持更高分辨率的体素网格以捕捉微米级细节？查询抖动训练策略已提供了一定的分辨率灵活性，但体素网格的稀疏性假设在极高分辨率下可能面临挑战。

4. **更本质的结构注入方式**：除RoPE位置嵌入外，是否有更本质的方法将局部结构信息注入生成过程，以进一步提升测试时缩放效果？这一问题指向3D生成表示理论的深层突破。

5. **端到端一体化**：当前两阶段设计存在级联误差风险，能否将粗结构生成与精细几何生成统一为端到端的单阶段模型，同时保持VoxSet的可定位性优势？



## 原文 PDF

![[paperPDFs/CVPR_2026/LATTICE_Democratize_High_Fidelity_3D_Generation_at_Scale.pdf]]
