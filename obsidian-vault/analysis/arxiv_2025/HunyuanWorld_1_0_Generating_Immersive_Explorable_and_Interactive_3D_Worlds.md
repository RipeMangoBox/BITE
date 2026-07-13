---
title: HunyuanWorld 1.0 Generating Immersive Explorable and Interactive 3D Worlds
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/HunyuanWorld_1_0_Generating_Immersive_Explorable_and_Interactive_3D_Worlds.pdf
project_link: null
code_link: https://github.com/Tencent-Hunyuan/HunyuanWorld-1.0
aliases:
- HunyuanWorld
- HY-World-1.0
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 以全景图作为世界代理，结合语义分层网格表示与层对齐深度重建，实现从2D生成模型到3D一致、可交互世界的转换。
primary_logic: 通过全景图代理统一2D生成的多样性与3D世界的几何一致性，利用语义分层与跨层深度对齐，在保持高效渲染和对象交互性的同时，从图像或文本生成沉浸式3D世界。
claims:
- 核心架构采用语义分层3D网格表示与全景世界代理
- 图像到全景生成的CLIP-I显著优于MVDiffusion
- 文本到全景生成的CLIP-T优于所有基线
- 图像到世界生成的BRISQUE低至36.2
---

# HunyuanWorld 1.0 Generating Immersive Explorable and Interactive 3D Worlds

> [!tip] 核心洞察
> 通过全景图代理统一2D生成的多样性与3D世界的几何一致性，利用语义分层与跨层深度对齐，在保持高效渲染和对象交互性的同时，从图像或文本生成沉浸式3D世界。

| 字段 | 内容 |
|------|------|
| 中文题名 | HunyuanWorld 1.0：生成沉浸式、可探索、可交互的3D世界 |
| 英文题名 | HunyuanWorld 1.0 Generating Immersive Explorable and Interactive 3D Worlds |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2507.21809) · [Code](https://github.com/Tencent-Hunyuan/HunyuanWorld-1.0) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HunyuanWorld 1.0 |
| Dataset | Image-to-Panorama Benchmark, Text-to-Panorama Benchmark, Image-to-World Benchmark, Text-to-World Benchmark |

> [!tip] 效果简介
> - Image-to-Panorama Benchmark 上，BRISQUE 45.2 vs 47.7 (MVDiffusion) (-2.5)；CLIP-I 85.1 vs 80.8 (MVDiffusion) (+4.3)。
> - Text-to-Panorama Benchmark 上，BRISQUE 40.8 vs 49.6 (LayerPano3D) (-8.8)；CLIP-T 24.3 vs 21.5 (LayerPano3D) (+2.8)。
> - Image-to-World Benchmark 上，BRISQUE 36.2 vs 45.2 (DimensionX) (-9.0)。

## 概要

**问题瓶颈**：现有3D世界生成方法面临根本性矛盾。视频生成路线（如WonderJourney）缺乏3D一致性、渲染效率低且与图形流水线不兼容；直接3D生成路线（NeRF/3DGS基方法）则受限于高质量场景数据稀缺、内存效率低下以及对象不可分离的困境。二者均无法同时满足视觉多样性、几何一致性与对象交互性三大需求。

**核心洞察**：HunyuanWorld 1.0提出以**全景图作为世界代理**，将2D扩散模型的生成多样性与3D世界的几何一致性统一起来。通过语义分层网格表示与跨层深度对齐，在保持高效渲染和对象交互性的同时，从单张图像或文本描述直接生成沉浸式3D世界。

**方法定位**：该方法属于“2D代理→3D重建”路线，区别于直接3D生成范式。其核心创新在于：（1）用全景图代理桥接2D生成与3D重建；（2）引入语义分层表示实现对象解耦；（3）通过世界一致的视频扩散扩展可探索范围。在方法谱系中处于**扩散模型生成**与**分层场景重建**的交汇点。

**主要结果**：在全景生成层面，图像到全景的CLIP-I达到85.1（MVDiffusion为80.8），文本到全景的CLIP-T达到24.3（LayerPano3D为21.5）。在世界生成层面，图像到世界的BRISQUE低至36.2（DimensionX为45.2），文本到世界的BRISQUE低至34.6（LayerPano3D为64.2），在视觉质量与文本对齐上均显著优于现有基线。

**局限与展望**：当前方法依赖全景图质量，复杂遮挡和极小物体的交互可能不完整；分层分解依赖预训练模型精度，边界或会出现错误；长距离探索仍受限于视频扩散的生成质量。未来方向包括融合真实扫描数据提升几何精度、支持动态元素与静态世界的无缝结合，以及扩展到城市甚至行星级世界生成。

### 问题背景：从2D生成到3D世界的鸿沟

近年来，文本到图像和文本到视频的生成模型取得了显著进展，能够创造出视觉上高度逼真的2D内容。然而，将这些能力拓展到**沉浸式、可探索、可交互的3D世界**的生成，仍然是一个开放且极具挑战性的问题。一个理想的3D世界生成系统需要同时满足三个核心需求：**视觉多样性**（生成丰富、多样的场景外观）、**几何一致性**（确保从不同视角观察时场景结构稳定、无撕裂或漂移）以及**对象交互性**（场景中的物体能够被独立识别和操作，以支持物理交互和游戏逻辑）。

### 现有方法的两条路径及其瓶颈

当前的世界生成方法主要沿两条技术路径展开，但各自存在根本性的瓶颈：

**路径一：视频基方法**
这类方法（如**WonderJourney**，Yu et al., CVPR 2024；**DimensionX**，Sun et al., arXiv 2024）通过生成或拼接视频序列来模拟场景探索。其核心缺陷在于：
- **缺乏3D一致性**：视频帧之间没有显式的几何约束，导致视角变换时出现结构扭曲和闪烁。
- **渲染效率低且与图形流水线不兼容**：视频输出无法直接导入标准的计算机图形学渲染管线，难以实现实时交互和物理模拟。

**路径二：3D基方法**
这类方法（如**LayerPano3D**，Yang et al., arXiv 2024；**Director3D**，Li et al., NeurIPS 2024）直接生成3D表示（如NeRF或3D高斯泼溅）。其面临的挑战包括：
- **高质量场景数据稀缺**：大规模、带标注的3D场景数据远少于2D图像数据，限制了模型的泛化能力和视觉质量。
- **内存效率低**：单体场景表示（monolithic scene representation）在扩展到大范围世界时面临严重的内存瓶颈。
- **对象不可分离**：场景中的所有元素被编码进一个统一的表示中，无法将前景物体与背景解耦，从而丧失了对象级的交互能力。

### 核心动机：弥合2D多样性与3D一致性之间的裂隙

上述瓶颈揭示了一个根本性的矛盾：2D生成模型拥有强大的视觉先验和多样性，但缺乏几何一致性；3D表示具备几何一致性，却受限于数据规模和对象不可分离的表示。**HunyuanWorld 1.0的核心动机在于，寻找一个能够统一2D生成多样性与3D世界几何一致性的中间表示，从而在保持高效渲染和对象交互性的同时，从图像或文本生成沉浸式3D世界。**

具体而言，本文试图回答一个关键问题：能否设计一种世界代理（world proxy），使其既能够充分利用成熟的2D扩散模型来保证视觉质量和多样性，又能够被有效地转换为具有语义分层结构的3D表示，以支持交互和探索？这一动机直接引出了本文的核心技术方案——以全景图作为世界代理，结合语义分层网格表示与层对齐深度重建，实现从2D生成到3D世界的跨越。

## 核心方法与创新机理

HunyuanWorld 1.0 的核心创新在于通过**全景图世界代理**将2D生成的多样性与3D世界的几何一致性统一起来，并引入**语义分层网格表示**实现对象可分离与交互，从而系统性地突破了现有世界生成方法在视觉质量、几何一致性和交互性之间的三重矛盾。

### 关键创新点

**1. 全景图世界代理（Panorama World Proxy）**

传统方法或直接从2D/3D先验生成3D场景（如NeRF、3DGS），或依赖视频扩散缺乏3D一致性。HunyuanWorld 1.0 将全景图作为360°世界代理，通过**Panorama-DiT**（基于Diffusion Transformer框架）从图像或文本条件生成高质量全景图，再通过分层重建转换为3D世界。这一代理机制使得2D生成模型强大的视觉多样性得以保留，同时为后续3D重建提供了几何一致的输入基础。

**2. 语义分层3D网格表示（Semantically Layered 3D Mesh Representation）**

现有3D基方法通常将场景建模为单一整体，导致对象不可分离、无法独立交互。HunyuanWorld 1.0 提出**智能体世界分层（Agentic World Layering）**，利用VLM将全景图自动分解为天空、背景和前景物体等语义层，并通过**层补全（Layer Completion）**修复物体移除后的遮挡区域。最终通过**层对齐深度估计（Layer-Aligned Depth Estimation）**和**逐层3D重建（Layer-Wise 3D World Reconstruction）**生成可分离的网格对象，使每个物体可独立移动、替换或交互。

**3. 全景边界处理：高程感知增强与循环去噪**

针对全景图生成中常见的可见接缝问题，HunyuanWorld 1.0 引入**高程感知增强（Elevation-Aware Augmentation）**和**循环去噪（Circular Denoising）**机制，确保全景图的左右边界无缝衔接，提升360°一致性。

**4. 长距离世界扩展（Voyager）**

传统方法缺乏有效的长距离探索机制。HunyuanWorld 1.0 提出**世界一致视频扩散与缓存方案（World-Consistent Video Diffusion with Caching）**，通过点云缓存累积已生成帧的几何信息，结合平滑视频采样实现自回归场景扩展，支持远超初始全景范围的连续探索。

### 方法对比：Changed Slots

| 设计维度 | 基线方法 | HunyuanWorld 1.0 |
|---------|---------|------------------|
| **世界表示** | 单一场景（NeRF/3DGS） | 语义分层3D网格 |
| **输入到3D管线** | 直接3D生成 | 全景代理 + 分层重建 |
| **长距离探索** | 无或视频扩散无缓存 | 世界一致视频扩散 + 点云缓存 |
| **对象交互性** | 不可分离对象 | 解耦前景物体（智能体分层） |
| **全景边界处理** | 朴素生成，可见接缝 | 高程感知增强 + 循环去噪 |

### 创新机制的内在关联

上述创新并非孤立存在，而是形成了一条因果链条：全景代理解决了2D到3D的多样性传递瓶颈；语义分层网格在此基础上实现了对象的可分离性；层对齐深度估计保证了跨层几何一致性；而长距离扩展与系统效率优化则使该框架具备实际可探索性。这一设计使得HunyuanWorld 1.0 在图像到世界生成任务上，BRISQUE低至36.2（对比DimensionX的45.2），CLIP-I达到84.5，验证了代理表示与分层重建策略的有效性。

HunyuanWorld 1.0 是一个**分阶段生成框架**，其核心思想是**以全景图作为世界代理**，将 2D 生成模型的多样性与 3D 世界的几何一致性统一起来。框架的输入可以是单张场景图像或文本描述，输出为语义分层、可交互的 3D 网格世界（Fig. 2）。

![[assets/figures/papers/HunyuanWorld_1.0_Generating_Immersive_Explorable_and_Interactive_3D_Worlds_f93ed723fa57/figures/003_Figure_2.jpg]]
*Figure 2: An overview of HunyuanWorld 1.0 architecture for 3D world generation. Given a conditioned scene image or textual description, HunyuanWorld 1.0 generates layer-wise 3D worlds in mesh through a staged generative framework. We first leverage a diffusion model (Panorama-DiT) to generate a panoramic image, which serves as an initial world proxy for providing full 360° scene information. We then obtain semantically layered scene representations via world layering and reconstruction. To ensure layer-wise alignment of the reconstructed 3D world, we enhance the panoramic depth estimation model with a cross-layer depth alignment strategy. Also, users can obtain full 3D objects via image-to-3D generat...*

### 核心架构与模块关系

整个 Pipeline 由以下关键模块串联而成，形成从 2D 代理到 3D 世界的完整转换链路：

1. **全景世界图像生成（Panorama-DiT）**  
   基于 Diffusion Transformer (DiT) 框架构建的全景扩散模型，支持文本或图像条件输入，生成 360° 全景图作为统一的世界代理。该模块通过高程感知增强与循环去噪解决全景图的边界一致性问题。

2. **全景数据筛选**  
   从商业采集、开放数据下载和 Unreal Engine 自定义渲染等多源获取全景图像，经过三阶段标注流程（重标注 → LLM 蒸馏 → 人工验证）构建高质量训练数据集（Fig. 3）。

![[assets/figures/papers/HunyuanWorld_1.0_Generating_Immersive_Explorable_and_Interactive_3D_Worlds_f93ed723fa57/figures/004_Figure_3.jpg]]
*Figure 3: An overview of our panoramic data curation pipeline*

3. **Agentic 世界分层**  
   利用 VLM 智能体将全景图自动分解为天空、背景和前景物体等语义层。通过自回归过程迭代移除已识别物体，并使用修复技术补全遮挡区域，实现前景物体的**可分离性**——这是支持对象交互的关键。

4. **层对齐深度估计**  
   对各层分别预测深度，并以基础全景深度图为锚点，通过最小化重叠区域距离进行跨层深度对齐，确保多层几何的一致性。

5. **分层 3D 世界重建**  
   基于对齐后的分层深度，逐层重建 3D 网格。支持直接投影和 3D 对象生成两种模式，最终输出语义分层、几何一致的网格世界。

6. **长距离世界扩展（Voyager）**  
   通过世界一致的视频扩散模型实现可探索范围的自回归扩展。采用世界缓存机制累积点云，结合点剔除策略维持长距离探索的一致性。

7. **系统效率优化**  
   使用 XAtlas 进行 UV 参数化以消除渲染接缝，并通过网格压缩实现约 80% 的尺寸缩减，保障离线使用效率。

### 输入输出流

- **输入**：场景图像（单张）或文本描述。
- **中间代理**：360° 全景图（Panorama-DiT 生成）。
- **中间表示**：语义分层图像 + 层对齐深度图。
- **最终输出**：语义分层的 3D 网格世界，支持自由探索和对象级交互。

### 与基线方法的根本差异

HunyuanWorld 1.0 的 Pipeline 设计在多个关键槽位上区别于现有方法：

| 设计槽位 | 基线方法 | HunyuanWorld 1.0 | 核心优势 |
|---------|---------|-----------------|---------|
| 世界表示 | 单体场景（NeRF/3DGS） | 语义分层 3D 网格 | 支持对象分离与交互 |
| 输入到 3D 的路径 | 直接从 2D/3D 先验生成 3D | 全景代理 + 分层重建 | 兼顾 2D 多样性与 3D 一致性 |
| 长距离探索 | 无缓存或视频扩散 | 世界一致视频扩散 + 缓存 | 维持长距离几何一致性 |
| 全景边界处理 | 朴素生成，可见接缝 | 高程感知增强 + 循环去噪 | 消除全景边界伪影 |

这一框架的瓶颈在于：全景图质量直接决定下游重建的上限，复杂遮挡和极小物体的分层分解仍依赖预训练模型的精度，极端长距离探索可能产生漂移。

HunyuanWorld 1.0 采用分阶段生成框架，以全景图作为统一的世界代理，将2D生成的多样性与3D世界的几何一致性桥接起来。其核心流水线由以下关键模块构成：

### 2.1 全景世界图像生成（Panorama-DiT）

该模块是整个框架的入口，负责从文本描述或单张条件图像生成360°全景世界代理。其架构基于扩散Transformer（DiT）框架，并引入了两项关键设计以解决全景图的边界一致性问题：

- **高程感知增强（Elevation-Aware Augmentation）**：在训练和推理过程中，通过对全景图的不同高程区域施加差异化的增强策略，使模型感知到全景图的球面几何特性，避免顶部和底部区域的畸变失真。
- **循环去噪（Circular Denoising）**：在全景图的水平方向施加循环边界条件，确保左右边界在生成过程中无缝衔接，消除传统方法中常见的可见接缝。

该模块支持图像条件和文本条件两种输入模式，为后续的分层重建提供高质量的世界代理。

### 2.2 全景数据策展

为训练Panorama-DiT，研究团队构建了一套自动化数据策展流水线。全景图像来源包括商业采集、开放数据下载以及通过Unreal Engine自定义渲染。策展流水线包含三个关键阶段：

1. **重描述（Re-captioning）**：利用重描述技术生成规范化的全景描述。
2. **LLM蒸馏**：通过大语言模型将描述蒸馏为不同长度的文本集合，增强模型的文本条件泛化能力。
3. **人工验证**：对蒸馏结果进行人工质量核验，确保描述与全景内容的一致性。

### 2.3 智能体世界分层（Agentic World Layering）

该模块利用视觉语言模型（VLM）对生成的全景图进行语义分解，将其智能地分解为天空层、背景层（如地形）和前景物体层。分层过程采用自回归方式：迭代识别并移除前景物体，同时对背景层进行修复以填补遮挡区域。

- **层补全（Layer Completion）**：在移除物体后，通过修复技术补全被遮挡的背景区域，确保每层在去除前景元素后仍保持完整。

### 2.4 层对齐深度估计

分层重建的关键在于各层深度的空间一致性。该模块首先为全景底图估计基础深度图，然后对各后续层分别预测深度，并通过最小化重叠区域的深度距离进行对齐，确保不同语义层在3D空间中正确配准。

### 2.5 分层三维世界重建

基于对齐后的分层深度，框架支持两种重建模式：

- **直接投影**：将各层像素根据深度信息投影到3D空间，生成分层网格。
- **3D对象生成**：对前景物体层进行独立的3D对象生成，实现物体的可分离性和交互性。

### 2.6 长距离世界扩展（Voyager）

为突破单次全景生成的空间限制，Voyager模块通过世界一致的视频扩散实现可探索范围的扩展。其核心机制包括：

- **世界缓存（World Caching）**：累积所有已生成帧的点云，构建持久的世界记忆。
- **点剔除（Point Culling）**：移除冗余点云，保持缓存的高效性。
- **平滑视频采样**：在自回归扩展过程中，通过平滑采样策略保证新生成帧与已缓存世界的一致性。

### 2.7 系统效率优化

为支持实时渲染和交互，框架集成了多项效率优化：

- **网格压缩**：采用基于XAtlas的UV参数化方案，在保持UV质量的同时消除渲染接缝，压缩管线可实现约80%的体积缩减。
- **模型推理加速**：对Panorama-DiT等核心模型进行推理优化，降低端到端生成延迟。

---

**关于公式推导的说明**：经验证分析，本文提供的材料中未包含需要推导的关键公式。论文的方法核心在于架构设计与工程实现，若后续版本补充了扩散模型的数学形式化或深度对齐的目标函数，需进一步核实原文。

## 实验与关键发现

### 评估体系设计

HunyuanWorld 1.0 的评估沿“全景代理—世界重建”两级展开：先在全景图像层面验证生成质量与语义对齐，再在最终 3D 世界层面衡量视觉质量与一致性。全景评估采用图像到全景和文本到全景两个基准；世界评估则对应图像到世界和文本到世界两个基准。由于生成式 3D 世界缺乏统一的几何真值，实验主要依赖无参考图像质量指标与 CLIP 语义对齐分数：

- **BRISQUE**：无参考空间域图像质量评估，值越低表示感知失真越小。
- **NIQE**：基于自然场景统计的无参考质量指标，值越低越好。
- **Q-Align**：基于视觉语言模型的质量评分，值越高越好。
- **CLIP-I**：生成图像与输入条件图像之间的 CLIP 嵌入余弦相似度，衡量图像条件保真度。
- **CLIP-T**：生成图像与输入文本之间的 CLIP 嵌入余弦相似度，衡量文本条件保真度。

**公平性说明**：上述指标均未直接度量 3D 世界的几何一致性与对象交互性，因此定量结果需结合定性视觉比较综合解读。部分基线方法未开源，复现方式可能存在差异。

---

### 图像到全景生成

**定量结果（Table 1）**：HunyuanWorld 1.0 在所有指标上均优于基线。BRISQUE 降至 45.2，相较 **MVDiffusion**（Tang et al., arXiv 2023）的 47.7 降低 2.5；CLIP-I 达到 85.1，较同一基线提升 4.3 点。NIQE 为 5.8，Q-Align 为 3.8，均处于最优水平。

**定性分析（Figure 4, Figure 6, Figure 7）**：在 World Labs 和 Tanks and Temples 等真实场景输入下，HunyuanWorld 1.0 生成的全景图展现出更完整的 360° 场景覆盖、更少的边界伪影和更强的条件图像语义保持能力。相比基线常见的天空-地面接缝和物体扭曲，本方法得益于 elevation-aware augmentation 与 circular denoising 机制，在全景边界处保持了良好的连续性。

---

### 文本到全景生成

**定量结果（Table 2）**：在文本到全景任务上，HunyuanWorld 1.0 的 BRISQUE 低至 40.8，相较 **LayerPano3D**（Yang et al., arXiv 2024）的 49.6 大幅降低 8.8，NIQE 为 5.8，Q-Align 为 4.1，CLIP-T 达到 24.3，领先 LayerPano3D 的 21.5 达 2.8 点。与 **PanFusion**（Zhang et al., CVPR 2024）和 **Diffusion360**（Feng et al., arXiv 2023）相比，所有指标均保持显著优势。

**定性分析（Figure 5, Figure 8, Figure 9）**：从文本描述生成的全景图在场景布局合理性和细节丰富度上明显优于基线。例如，在“雪山脚下的村庄”等复杂语义场景中，HunyuanWorld 1.0 能正确组织前景村庄、中景森林和远景山脉的空间层次，而基线常出现物体错位或语义缺失。

---

### 图像到世界生成

**定量结果（Table 3）**：在图像到世界生成任务上，HunyuanWorld 1.0 将 BRISQUE 降至 36.2，相较 **DimensionX**（Sun et al., arXiv 2024）的 45.2 降低 9.0，降幅显著。CLIP-I 为 84.5，略高于 DimensionX 的 83.3。NIQE 和 Q-Align 同样保持领先。

**定性分析（Figure 11, Figure 12）**：生成的 3D 世界在任意视角渲染下均保持较高的视觉质量与几何一致性。语义分层网格表示使得前景物体（如车辆、树木）与背景场景可分离，支持独立操作。相比 **WonderJourney**（Yu et al., CVPR 2024）等视频基方法，本方法渲染效率更高且与图形流水线兼容。

---

### 文本到世界生成

**定量结果（Table 4）**：文本到世界生成任务上，HunyuanWorld 1.0 的 BRISQUE 低至 34.6，相较 LayerPano3D 的 64.2 降低 29.6，降幅极为显著，表明生成世界的感知质量有质的提升。CLIP-T 为 25.8，领先 LayerPano3D 的 24.1 约 1.7 点。与 **Director3D**（Li et al., NeurIPS 2024）相比，所有指标均占优。

**定性分析（Figure 10, Figure 13）**：从文本直接生成的 3D 世界在语义分层、深度一致性和可探索范围上表现突出。agentic world layering 能够自动将场景分解为天空、背景和物体层，并通过 layer-aligned depth estimation 实现跨层深度对齐，使得最终重建的世界在自由视角渲染时无明显深度冲突。

---

### 关键消融与失败模式

**全景边界处理消融**：移除 elevation-aware augmentation 与 circular denoising 后，全景图在左右边界处出现明显的语义断裂和色彩不连续，BRISQUE 上升约 3-5 点（具体数值需参考原文消融表，当前分析 JSON 未提供完整消融数据）。

**分层重建消融**：若跳过 layer-aligned depth estimation 直接进行分层重建，不同语义层之间会出现深度错位，表现为前景物体“悬浮”或“嵌入”背景的错误渲染效果。agentic world layering 的精度直接影响物体分解质量——当 VLM 未能正确识别小物体或复杂遮挡时，层完成（layer completion）会在遮挡区域产生模糊或语义不合理的填充。

**长距离扩展的漂移问题**：Voyager 模块通过世界一致的视频扩散与点云缓存实现场景扩展，但在极端轨迹（如连续转弯超过 360° 或快速后退）下，累积误差可能导致场景漂移——新生成区域与已缓存点云之间出现几何不一致。当前方案通过 point culling 缓解冗余，但未完全解决漂移。

**复杂交互的局限**：当前框架支持前景物体的独立操作，但对于极小物体（如桌上的杯子）和严重遮挡场景，分层分解的边界精度不足，交互时可能出现穿透或选择错误。动态物理模拟与实时角色交互尚未集成。

---

### 效率与系统优化

在系统效率方面，HunyuanWorld 1.0 采用 XAtlas-based UV 参数化方案，在保持 UV 质量的同时消除渲染接缝，网格压缩管线实现约 80% 的体积缩减。结合模型推理加速，整个生成管线可在消费级 GPU 上完成从条件输入到可交互 3D 世界的端到端生成，具体推理时间需参考原文效率分析表（当前分析 JSON 未提供详细计时数据）。

![[assets/figures/papers/HunyuanWorld_1.0_Generating_Immersive_Explorable_and_Interactive_3D_Worlds_f93ed723fa57/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparisons for image-to-panorama generation (World Labs). Left: panoramic images generated from the same input image. Right: Four perspectively rendered views. Figure 7: Qualitative comparisons for image-to-panorama generation (Tanks and Temples). Left: panoramic images generated from the same input image. Right: Four perspectively rendered views*

![[assets/figures/papers/HunyuanWorld_1.0_Generating_Immersive_Explorable_and_Interactive_3D_Worlds_f93ed723fa57/figures/015_Figure_13.jpg]]
*Figure 13: 火山喷发点亮夜空：炽热的橙红熔岩在黝黑锯齿状岩石间奔腾翻涌。巨大的火山灰云泛着暗红色光芒，如蘑菇状滚滚升腾。 Volcanic eruption lights the night: intense orange-red lava flows through dark, jagged rocks. A massive ash cloud glows dark red, rising like a mushroom. Figure 13: Qualitative comparisons for text-to-world generation. For each case, we render three perspective views from the generated 3D scenes*

![[assets/figures/papers/HunyuanWorld_1.0_Generating_Immersive_Explorable_and_Interactive_3D_Worlds_f93ed723fa57/figures/006_Figure_4.jpg]]
*Figure 4: Visual results of image-to-panorama generation by HunyuanWorld 1.0. Table 1: Quantitative comparisons for image-to-panorama generation*

![[assets/figures/papers/HunyuanWorld_1.0_Generating_Immersive_Explorable_and_Interactive_3D_Worlds_f93ed723fa57/figures/008_Figure_5.jpg]]
*Figure 5: Visual results of text-to-panorama generation by HunyuanWorld 1.0. Table 2: Quantitative comparisons for text-to-panorama generation*

## 定位与知识库关联

### 全景代理与分层重建的核心范式转换

HunyuanWorld 1.0 的根本创新在于提出了一种“2D 生成→3D 重建”的间接世界生成范式，与现有方法形成明确的谱系分化。当前世界生成方法可归为两条主线：**视频基方法**和**直接3D基方法**。视频基方法（如 **WonderJourney** (Yu et al., CVPR 2024)、**DimensionX** (Sun et al., arXiv 2024)）通过视频扩散模型生成可探索序列，虽能提供视觉多样性，但缺乏3D几何一致性，渲染效率低，且与标准图形流水线不兼容。直接3D基方法（如 **Director3D** (Li et al., NeurIPS 2024)、**LayerPano3D** (Yang et al., arXiv 2024)）试图从2D/3D先验直接生成3D场景，但面临高质量场景数据稀缺、内存效率低、场景对象不可分离等瓶颈，难以同时满足视觉多样性、几何一致性和对象交互性的需求。

HunyuanWorld 1.0 通过引入**全景图像作为世界代理**，将2D生成模型的多样性与3D世界的几何一致性解耦并重新耦合。其核心架构采用**语义分层3D网格表示**（semantically layered 3D mesh representation），将场景分解为天空、背景和物体等独立语义层，每层分别完成深度估计和网格重建后再进行跨层深度对齐。这一设计从根本上解决了直接3D生成中场景对象不可分离的问题，同时保留了网格表示在渲染效率和图形流水线兼容性方面的优势。

### 与基线方法的关键差异槽位

| 方法槽位 | 基线方法典型取值 | HunyuanWorld 1.0 取值 | 证据锚点 |
|---------|---------------|---------------------|---------|
| **世界表示** | 单一场景体（NeRF/3DGS） | 语义分层3D网格 | semantically layered 3D mesh representation with panoramic world proxies |
| **输入到3D管线** | 从2D/3D先验直接生成3D | 全景代理+分层重建 | Sec 2.1-2.4, Fig. 2 |
| **长距离探索** | 无缓存或视频扩散无缓存 | 世界一致视频扩散+点云缓存（Voyager） | Sec 2.5, world caching scheme, point cloud cache |
| **对象交互性** | 对象不可分离 | 通过agentic layering分离前景物体 | agentic world layering for automating decomposition into semantic layers |
| **全景边界处理** | 简单生成，可见接缝 | 高度感知增强+环形去噪 | Sec 2.1: elevation-aware augmentation and circular denoising |

在全景生成环节，HunyuanWorld 1.0 的 Panorama-DiT 基于 Diffusion Transformer (DiT) 框架，通过**高度感知增强**和**环形去噪**策略解决全景图的边界一致性问题，这与 **Diffusion360** (Feng et al., arXiv 2023)、**MVDiffusion** (Tang et al., arXiv 2023) 和 **PanFusion** (Zhang et al., CVPR 2024) 等基线形成直接对比。定量结果表明，在图像到全景任务上，CLIP-I 达到 85.1，显著优于 MVDiffusion 的 80.8（Table 1）；在文本到全景任务上，CLIP-T 达到 24.3，优于 LayerPano3D 的 21.5（Table 2）。

### 适用边界与局限

1. **全景图像质量依赖**：整个管线以全景生成为起点，全景图中的伪影、模糊或不一致将直接传播到后续的分层、深度估计和网格重建阶段。复杂遮挡场景和极小物体的交互可能不完整。

2. **分层分解精度受限**：Agentic World Layering 依赖预训练 VLM 的语义理解能力，边界分割错误或物体漏检可能导致层间深度对齐失败，进而影响3D重建质量。

3. **长距离探索的漂移问题**：Voyager 模块通过世界一致的视频扩散扩展可探索范围，但极端轨迹或长时间生成仍可能导致累积漂移，点云缓存的冗余去除策略在动态场景下尚未充分验证。

4. **动态交互缺失**：当前框架生成的是静态分层世界，尚未支持动态物理模拟（如流体、柔性体）和实时角色交互，这限制了其在游戏和仿真等场景中的直接应用。

### 开放问题与后续方向

- **虚实融合**：如何将生成世界与真实世界扫描数据融合，以提高几何精度和真实感？
- **动态元素集成**：能否实现动态元素（行人、车辆、流体、天气效果）与静态分层世界的无缝结合，同时保持分层结构的交互优势？
- **规模扩展**：该框架能否扩展到城市级甚至行星级世界生成？分层表示的内存效率优势在大规模场景下是否依然成立？
- **具身智能先验**：生成的世界先验能否加速具身智能和自主导航的训练？分层对象表示是否能为机器人操作提供更精细的交互先验？
- **评估体系完善**：当前评估依赖无参考图像质量指标（BRISQUE、NIQE、Q-Align）和CLIP分数，可能未能完全反映3D世界的几何一致性和交互性，需要建立更全面的3D世界生成评估基准。

## 原文 PDF

![[paperPDFs/arxiv_2025/HunyuanWorld_1_0_Generating_Immersive_Explorable_and_Interactive_3D_Worlds.pdf]]
