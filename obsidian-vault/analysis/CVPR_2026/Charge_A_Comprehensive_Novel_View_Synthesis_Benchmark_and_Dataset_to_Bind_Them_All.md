---
title: "Charge: A Comprehensive Novel View Synthesis Benchmark and Dataset to Bind Them All"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Charge_A_Comprehensive_Novel_View_Synthesis_Benchmark_and_Dataset_to_Bind_Them_All.pdf
project_link: "https://charge-benchmark.github.io/"
code_link: null
aliases:
- CD
- Charge
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 利用Blender制作的高质量动画电影《Charge》生成合成数据，从而获得精确的相机位姿、高帧率捕捉、丰富的多模态标注以及可控的动态和相机设置，构建统一的稠密、稀疏、单目评估基准。
primary_logic: 通过整合稠密、稀疏和单目三种实验设置，提供高分辨率、高帧率、多模态（RGB、深度、法线、分割、光流）的动态数据集，为静态和动态场景重建以及3D基础模型建立了一个更具挑战性和全面性的统一评估平台。
claims:
- Charge数据集的动态像素占比高达25.1%，是现有最好数据集的2倍以上，且光流分布更广，涵盖更多大幅运动。
- Charge提供三种不同稀疏程度的相机设置，测试视图数量远超以往数据集，并能通过FOVo量化任务难度。
- 基线动态重建方法在Charge的稀疏和单目设置下性能显著下降，动态区域PSNR远低于静态区域，揭示了现有方法在场景覆盖不足和大运动下的弱点。
- 静态基准测试揭示了位姿-形状歧义：仅利用源视图通过Umeyama对齐进行新视角合成，性能远低于使用目标视图对齐的方法，且引入光度一致性后各任务相对排名得以保持。
---

# Charge: A Comprehensive Novel View Synthesis Benchmark and Dataset to Bind Them All

> [!tip] 核心洞察
> 通过整合稠密、稀疏和单目三种实验设置，提供高分辨率、高帧率、多模态（RGB、深度、法线、分割、光流）的动态数据集，为静态和动态场景重建以及3D基础模型建立了一个更具挑战性和全面性的统一评估平台。

| 字段 | 内容 |
|------|------|
| 中文题名 | Charge：一个综合性的新型视图合成基准与数据集 |
| 英文题名 | Charge: A Comprehensive Novel View Synthesis Benchmark and Dataset to Bind Them All |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.13639) · [Project](https://charge-benchmark.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Charge (Dataset) |
| Dataset | Charge Dense Setup, Charge Sparse Setup, Charge Mono Setup, Charge Static Benchmark |

> [!tip] 效果简介
> - Charge Dense Setup (25 views) 上，PSNR Ex4DGS 29.75 vs 4DGS 28.94 (+0.81)。
> - Charge Sparse Setup (9 views) 上，PSNR 4DGS 26.67 vs STG 24.52 (+2.15)。
> - Charge Mono Setup (Random Walk Slow) 上，PSNR MoSca 24.29 vs 4DGS 23.38 (+0.91)。

## 概述

### 问题与瓶颈
现有的动态新视角合成数据集普遍存在**动态内容占比低**（最高仅12.6%）、**标注模态单一**（通常仅RGB或部分深度）、**相机设置与现实应用不匹配**（仅稠密或仅单目）、以及**测试视角覆盖不足**等问题。这些局限使得现有基准难以全面评测下一代重建方法和3D基础模型在真实复杂场景下的能力边界。

### 核心思路
本文提出**Charge**——一个基于Blender高质量动画电影《Charge》构建的综合新视角合成数据集。其核心洞察在于：通过利用生产级动画资源，可同时获得精确的相机位姿、96 fps高帧率捕捉、丰富的多模态标注（RGB、深度、法线、分割、光流、UV贴图、动态掩码），以及可控的动态与相机设置。Charge整合**稠密**（25训练+16测试视角）、**稀疏**（3/6/9训练+10测试视角）和**单目**（4种轨迹×4+16测试视角）三种实验设置，为静态与动态场景重建以及3D基础模型建立了一个更具挑战性和全面性的统一评估平台。

### 关键发现
- **动态挑战显著**：Charge的动态像素占比高达25.1%，是现有最佳数据集（DyCheck 12.6%）的两倍以上，且光流分布覆盖更大范围的运动幅度（见Figure 3）。基线动态重建方法在稀疏和单目设置下PSNR大幅下降，动态区域PSNR始终低于静态区域，揭示了现有方法在场景覆盖不足和大运动下的明显弱点。
- **难度可控量化**：通过定义视场重叠指标 $FOV_O$ 量化任务难度，实验表明降低相机移动速度或改变轨迹类型会减小视场重叠，导致各方法性能相应下降。
- **位姿-形状歧义**：静态基准测试中，仅用源视图通过Umeyama对齐进行新视角合成，性能远低于使用目标视图对齐的方法，揭示了位姿估计与几何重建之间的深层歧义；引入光度一致性后各方法相对排名得以保持。

### 方法谱系与知识库定位
Charge本身是一个**数据集与基准**，而非重建算法。它面向三类方法的评估：
- **多视图动态重建**：评估方法包括**4DGS**（Wu et al., CVPR 2024）、**STG**（Li et al., CVPR 2024）、**Ex4DGS**（Lee et al., NeurIPS 2024）。
- **单目动态重建**：评估方法包括**D-3DGS**（Yang et al., CVPR 2024）、**SC-GS**（Huang et al., CVPR 2023）、**MoSca**（Lei et al., CVPR 2025）。
- **3D基础模型**：评估**VGGT**（Wang et al., CVPR 2025）、**π³**（Wang et al., arXiv 2025）、**AnySplat**（Jiang et al., SIGGRAPH Asia 2025）、**WorldMirror**（Liu et al., arXiv 2025）在相机位姿估计、深度估计和新视角合成上的表现。

### 局限与展望
Charge完全由合成动画生成，与真实场景存在领域差距；仅包含单部电影的8个场景，多样性受限；静态基准仅选取部分静止帧，未评估基础模型在动态序列上的表现。未来需在真实动态数据上验证模型泛化能力，并探索更有效的位姿-形状解耦策略。

## 背景与动机

新视角合成（Novel View Synthesis, NVS）旨在从一组已知视角的图像中恢复场景的三维表示，并渲染出任意新视角下的逼真图像。近年来，以NeRF和3D Gaussian Splatting为代表的神经渲染方法在该领域取得了显著进展，推动了静态场景重建的成熟。然而，现实世界本质上是动态的，动态场景的重建与渲染——即动态新视角合成——正成为下一阶段的核心挑战。

### 现有数据集的瓶颈

当前动态新视角合成研究面临的一个关键制约在于**评估数据集的局限性**。现有数据集普遍存在以下结构性缺陷：

1. **动态内容占比过低**：多数动态数据集中，实际发生运动的像素比例有限。如表2所示，广泛使用的DyCheck数据集动态像素占比仅为12.6%，Neural 3D为10.9%，Technicolor为9.7%。低动态占比意味着评估结果可能被大量静态区域所主导，无法真实反映方法对动态内容的建模能力。

2. **标注模态单一**：大多数现有数据集仅提供RGB图像，缺少深度、法线、光流、语义分割等多模态真值标注。这种单一性限制了对重建方法进行多维度诊断分析的可能性，也难以支撑需要多模态监督的下一代方法。

3. **相机设置与现实场景不匹配**：现有数据集通常采用单一相机配置——要么是稠密多视角捕获，要么是单目视频，缺乏在统一场景下对比不同稀疏程度相机设置的能力。这导致评估无法系统性地揭示方法在输入视角减少时的性能退化规律。

4. **测试视角覆盖不足**：许多数据集仅提供单一或少数几个测试视角，难以全面评估新视角合成方法在未见视角上的泛化能力。

5. **帧率与运动捕捉能力有限**：真实场景的采集帧率通常较低（5–60 fps），对于快速运动的场景，难以提供足够的时间分辨率来准确建模动态过程。

### 本文动机

上述瓶颈的存在，使得现有基准难以全面评测下一代动态重建方法——尤其是那些旨在从稀疏甚至单目输入中恢复完整4D表示的方法，以及正在兴起的3D基础模型——的真实能力。为此，本文提出**Charge数据集**，旨在通过一个**高动态含量、高帧率、多模态、多相机设置**的统一评估平台，填补这一空白。Charge的核心设计理念是：利用Blender制作的电影级动画《Charge》生成合成数据，从而获得精确的相机位姿、高帧率（96 fps）的时间采样、丰富的逐像素真值标注，以及可控的稠密、稀疏和单目三种相机配置，为静态和动态场景重建建立一个更具挑战性和全面性的统一基准。

## 核心创新

Charge 数据集的核心创新并非提出新的重建算法，而是通过系统性地重新设计数据集的**内容构成、相机配置和多模态标注**，构建了一个更具挑战性且统一的评估平台，直击现有动态新视角合成基准的瓶颈。

### 1. 显著提升的动态内容与运动覆盖

现有动态数据集的根本缺陷在于动态像素占比过低，导致评估难以真实反映方法对场景运动的建模能力。Charge 从根本上改变了这一局面：
- **动态像素占比跃升**：Charge 的动态像素占比达到 **25.1%**，是此前最佳数据集 DyCheck（12.6%）的约 2 倍，远超 Neural 3D（10.9%）和 Technicolor（9.7%）（Table 2）。
- **更广的光流分布**：与 DyCheck 相比，Charge 的光流幅度直方图展现出更高的密度和更宽的覆盖范围，尤其在**大幅度运动**区间具有明显优势（Figure 3）。这意味着 Charge 能够更有效地检验方法对复杂运动的鲁棒性。

### 2. 统一的稠密-稀疏-单目相机设置

以往数据集通常仅提供单一相机配置（如仅稠密多视角或仅单目视频），迫使研究者使用不同基准评估不同方法，难以进行公平比较。Charge 在同一批场景上设计了三种标准化的相机设置（Figure 2），并提供了远超以往数据集的测试视角数量：
- **稠密设置**：25 个训练相机 + 16 个测试相机，球面均匀分布。
- **稀疏设置**：提供 3/6/9 个训练相机 + 10 个测试相机，模拟有限视角的挑战。
- **单目设置**：4 种不同速度和轨迹类型（Spline Fast/Slow, Random Walk Fast/Slow）的视频序列，各含 4 个训练视角 + 16 个测试视角。

这一设计使得同一方法可以在不同输入稀疏度下被系统性评估，揭示了方法对视角覆盖的敏感程度。

### 3. 可量化的任务难度指标：FOVo

Charge 引入了**视场重叠度**（Field of View Overlap, FOVo）作为任务难度的量化指标：

$$FOV_{O} = \frac{1}{n_{test}} \left( \frac{\sum_{n_{train}} m_i}{n_{train} \cdot H W} \right)$$

该指标计算测试视角与所有训练视角的平均视场重叠比例。FOVo 越低，表示测试视角越远离训练视角的覆盖区域，任务难度越高。实验表明，FOVo 的下降（如单目设置中从 Fast 到 Slow，或轨迹从 Spline 变为 Random Walk）与各方法 PSNR 的下降高度相关（Table 3），为评估任务难度提供了可解释的参考。

### 4. 丰富的多模态真值标注

Charge 不仅提供高分辨率 RGB 图像（2048×858），还以 **96 fps** 的高帧率渲染了完整的像素级真值标注，包括：深度、法线、光流、实例分割、UV 贴图和动态掩码。这种多模态数据的同步提供，使其不仅能评估新视角合成的视觉质量，还能直接衡量几何重建、运动估计和语义理解的准确性，为 3D 基础模型的多任务评估提供了可能。

### 5. 揭示位姿-形状歧义的静态基准

Charge 还从动态序列中抽取静态帧构建了静态基准，用于评估 3D 基础模型。通过对比仅使用源视图进行 Umeyama 对齐（NVS）与使用目标视图进行相机对齐（NVS†）的新视角合成结果，Charge 揭示了**位姿-形状歧义**（pose-shape ambiguity）对重建性能的显著影响：仅依赖源视图对齐的方法性能远低于引入目标视图的方法（Table 5）。同时，实验表明当在流程中引入光度一致性后，各方法的相对排名得以保持，为后续研究解耦位姿估计与形状重建提供了明确的实验证据。

## 整体框架

Charge 是一个以生产级动画电影《Charge》为核心数据源，通过重构渲染管线、设计多层级相机配置并生成丰富多模态标注，构建的统一静态与动态新视角合成基准。其整体框架由四个核心模块串联而成：**场景处理与渲染管线重构**、**多层级相机设置设计**、**多模态数据生成**以及**基准组织与评估协议**。

### 场景处理与渲染管线重构

数据集的原始素材取自《Charge》电影的 8 个完整生产镜头。每个镜头包含完整的动画、光照和资产库。为消除原始渲染管线中后期处理效果（如色彩分级、晕影、运动模糊等）对三维一致性的破坏，Charge 移除了原有管线，替换为从相机直接渲染的方式，并额外添加深度、法线等模态输出。这一重构确保了所有渲染帧在几何和外观上的严格一致性，为多视角重建提供了无噪声、无失真的理想合成环境。

### 多层级相机设置设计

为覆盖从稠密多视角到极稀疏单目的完整评测谱系，Charge 在场景球面上布置相机，构建了三种标准配置（Figure 2 右侧）：

![[assets/figures/papers/paper_list_l2232_https_arxiv_org_abs_2512_13639/figures/003_Figure_2.jpg]]
*Figure 2: An overview of the Charge dataset. The left side presents a selection of frames from all the animations. On the right side, a 3 setups included in the dataset are presented: Dense, Sparse, and Mono. Cameras allocation and sample movement path for monocular trajectory are overlayed on the section of the point cloud corresponding to scene 040 0040*

- **稠密设置 (Dense)**：25 个训练相机 + 16 个测试相机，提供最丰富的视角覆盖。
- **稀疏设置 (Sparse)**：分别提供 3、6、9 个训练相机 + 10 个测试相机，通过递减训练视角数量梯度式增加任务难度。
- **单目设置 (Mono)**：4 种轨迹类型（Spline Fast / Spline Slow / Random Walk Fast / Random Walk Slow），每种轨迹提供 4 个训练视角 + 16 个测试视角，模拟真实手持拍摄的连续运动。

所有设置的测试视角数量均远超以往数据集（如 DyCheck 仅提供单测试视角或双视角），且通过 **视场重叠度 (FOVₒ)** 量化每个测试视角与训练视角的平均重叠比例，作为任务难度的客观指标：

$$FOV_{O} = \frac{1}{n_{test}} \left( \frac{\sum_{n_{train}} m_i}{n_{train} \cdot H W} \right)$$

FOVₒ 越低，表示测试视角越远离训练视角覆盖区域，重建难度越高。

### 多模态数据生成

在重构的渲染管线上，Charge 以 2048×858 分辨率和 96 fps 的高帧率输出多模态数据，包括：RGB、深度、法线、光流、语义分割、UV 贴图以及动态掩码。这一模态丰富度远超仅提供 RGB 或部分深度的现有数据集（Table 1）。其中，动态掩码和光流标注直接支持对动态区域重建质量的精细评估，而 UV 贴图则为未来基于纹理的建模方法提供了可能。

### 基准组织与评估协议

Charge 将数据划分为两大基准：

- **动态基准 (Dynamic Benchmark)**：覆盖全部三种相机设置，评估多视角和单目动态重建方法。评测指标包括全图 PSNR/SSIM/LPIPS，以及按动态掩码分离的**动态区域指标 (PSNR-D、SSIM-D、LPIPS-D)** 和**静态区域指标 (PSNR-S、SSIM-S、LPIPS-S)**，以区分方法对运动和静态内容的建模能力。
- **静态基准 (Static Benchmark)**：从各场景中抽取部分静态帧，评估当前仅支持静态场景的 3D 基础模型，涵盖相机位姿估计、深度估计和新视角合成三个任务。通过对比仅使用源视图的 Umeyama 对齐 (NVS) 与引入目标视图对齐 (NVS†) 的结果，揭示位姿-形状歧义对几何重建的影响。

整个框架的输入为 Blender 生产场景文件，输出为标准化的训练/测试图像及多模态标注，供下游方法统一评测。

## 核心模块与公式推导

### 数据集构建管线

Charge数据集的构建围绕三个核心模块展开，形成从动画资产到多模态基准的完整流水线。

**场景处理与渲染管线** 从Blender制作的动画电影《Charge》中选取全部8个可用的生产级镜头。原始渲染管线包含后期处理效果，可能破坏3D一致性，因此将其替换为直接相机渲染，并添加深度、法线等额外模态输出（Section 3.1）。这一替换是确保合成数据几何精确性的关键步骤。

**相机设置设计** 在场景点云周围的球面上布置相机，创建三种标准化的评估配置（Section 3.2，见Figure 2）：
- **稠密设置**：25个训练视角 + 16个测试视角
- **稀疏设置**：3/6/9个训练视角 + 10个测试视角（三种稀疏程度）
- **单目设置**：4种轨迹类型（Spline Fast、Spline Slow、Random Walk Fast、Random Walk Slow），每种4个训练视角 + 16个测试视角

**多模态数据生成** 以2048×858分辨率、96 fps帧率渲染输出七种模态：RGB、深度、法线、光流、语义分割、UV贴图和动态掩码（Section 3.3）。96 fps的高帧率使得Charge在捕捉快速运动方面显著优于现有数据集（如DyCheck的5–60 fps，见Table 1）。

### 任务难度量化公式

为量化不同相机设置下的任务难度，Charge引入了**视场重叠度**指标：

$$FOV_{O} = \frac{1}{n_{test}} \left( \frac{\sum_{n_{train}} m_i}{n_{train} \cdot H W} \right)$$

其中：
- $n_{test}$ 为测试视角数量
- $n_{train}$ 为训练视角数量
- $H$ 和 $W$ 分别为图像高度和宽度
- $m_i$ 为第 $i$ 个训练视角中与测试视角视场重叠的像素数

$FOV_O$ 值越低，表示测试视角越远离训练视角的覆盖范围，任务难度越高。该指标在Table 3和Table 4中作为难度参考列出现，例如稠密设置下 $FOV_O$ 约为0.57，而单目Random Walk Slow设置下仅为0.38，直观反映了视角覆盖的递减。

### 基准组织逻辑

数据集被划分为两个评估基准（Section 4）：

- **动态基准**（Section 4.1）：涵盖所有三种相机设置，评估多视图和单目动态重建方法。动态区域与静态区域的分离评估通过动态掩码实现，指标后缀 `-D` 和 `-S` 分别表示仅动态区域和仅静态区域的度量。
- **静态基准**（Section 4.2）：从每个场景中选取静态帧子集，评估当前仅支持静态场景的基础模型（如VGGT、π3、AnySplat、WorldMirror），涵盖相机位姿估计、深度估计和新视角合成三项任务。

## 实验与分析

### 动态基准：稠密、稀疏与单目设置下的重建性能

Charge数据集在三种相机设置下对当前主流的动态高斯泼溅（Gaussian Splatting）方法进行了系统评估。Table 3和Table 4汇总了稠密（25训练视角）、稀疏（3/6/9训练视角）与单目（4种轨迹×4训练视角）设置下的量化结果，所有方法均按统一协议在8个场景上训练和测试。

在稠密设置下，**Ex4DGS**（Lee et al., NeurIPS 2024）以PSNR 29.75取得最佳性能，略优于**4DGS**（Wu et al., CVPR 2024）的28.94和**STG**（Li et al., CVPR 2024）的29.29（Table 3）。然而，当训练视角从25个骤降至稀疏设置时，所有方法的性能均出现显著滑坡：9视角下最优方法**4DGS**的PSNR仅为26.67，较稠密设置下降超过3 dB；3视角下PSNR进一步降至24.72（Table 4）。这一退化幅度揭示了现有方法对训练视角覆盖密度的强依赖性。

![[assets/figures/papers/paper_list_l2232_https_arxiv_org_abs_2512_13639/figures/006_Table_3.jpg]]
*Table 3: Quantitative evaluation results of Charge dataset - Dense and Mono setups, -D denotes metrics on dynamic-only areas, -S static only and F OVO quantifies the field-of-view overlap between testing and training views (i.e. harder when lower). Best performer*

![[assets/figures/papers/paper_list_l2232_https_arxiv_org_abs_2512_13639/figures/007_Table_4.jpg]]
*Table 4: Quantitative evaluation results of Charge dataset - Sparse setup, -D denotes metrics on dynamic-only areas, -S static only and F OVO quantifies the field-of-view overlap between testing and training views (i.e. harder when lower). Best performer*

单目设置进一步暴露了方法的脆弱性。在四种单目轨迹中，性能最优的**MoSca**（Lei et al., CVPR 2025）在Random Walk Slow轨迹下仅取得PSNR 24.29，而**4DGS**在相同条件下为23.38（Table 3）。值得注意的是，单目设置下所有方法的PSNR均低于稀疏9视角的结果，说明单目视频中有限的空间覆盖比稀疏多视角带来了更大的重建挑战。

### 动态区域与静态区域的性能鸿沟

一个贯穿所有设置的关键发现是**动态区域的重建质量始终且显著低于静态区域**。Table 3和Table 4中，PSNR-D（仅动态区域）持续低于PSNR-S（仅静态区域），差距在稠密设置下约为3–5 dB，在稀疏和单目设置下进一步扩大。例如，4DGS在稠密设置下PSNR-S为31.52而PSNR-D为28.94（差2.58 dB），在单目Random Walk Slow下PSNR-S为26.25而PSNR-D为23.38（差2.87 dB）。SSIM-D和LPIPS-D呈现相同的趋势，证实动态内容——尤其是Charge数据集中占比高达25.1%的大幅运动——对现有方法构成了核心瓶颈。

### 任务难度量化：视场重叠指标FOVo

为量化不同设置的固有难度，论文引入了**视场重叠指标**（Field of View Overlap, FOVo）：

$$FOV_{O} = \frac{1}{n_{test}} \left( \frac{\sum_{n_{train}} m_i}{n_{train} \cdot H W} \right)$$

该指标计算测试视角与所有训练视角的平均视场重叠比例，数值越低表示测试视角越远离训练覆盖区域，任务难度越高。Table 3和Table 4中的FOVo值与性能变化高度一致：稠密设置FOVo约为0.55，稀疏9/6/3视角分别降至约0.38/0.30/0.22，单目设置进一步降至0.38–0.42区间。FOVo的下降与PSNR的退化呈单调关系，验证了该指标作为任务难度代理的有效性。

### 单目轨迹类型与速度的影响

单目设置下的消融分析揭示了相机运动模式对重建难度的调制作用。对比四种轨迹（Spline Fast、Spline Slow、Random Walk Fast、Random Walk Slow），两个趋势清晰可见：（1）降低相机移动速度（Fast → Slow）会减小FOVo，从而增加重建难度；（2）将轨迹类型从Spline改为Random Walk同样降低FOVo。例如，**D-3DGS**（Yang et al., CVPR 2024）在Spline Fast下PSNR为24.88，在Random Walk Slow下降至23.73（Table 3）。这表明更慢、更不规则的相机运动导致训练视角覆盖范围缩小，使新视角合成任务更加困难。

### 静态基准：基础模型的位姿-形状歧义

Charge的静态基准（Table 5）从动态序列中抽取静态帧，评估了四类基础模型在相机位姿估计、深度估计和新视角合成上的表现。核心发现围绕**位姿-形状歧义**（pose-shape ambiguity）展开。

![[assets/figures/papers/paper_list_l2232_https_arxiv_org_abs_2512_13639/figures/011_Table_5.jpg]]
*Table 5: A static benchmark of next generation foundational models on Charge, including camera pose estimation, depth estimation and novel view synthesis, † denotes target views used for camera alignment. Best performer*

在新视角合成任务中，当仅利用源视图通过Umeyama对齐进行相机位姿估计时（NVS列），所有方法的性能均显著低于将目标视图纳入对齐流程的方法（NVS†列）。例如，**WorldMirror**（Liu et al., arXiv 2025）在m-aseds子集上NVS为17.54而NVS†为20.94，**AnySplat**（Jiang et al., SIGGRAPH Asia 2025）在9-sseds子集上NVS为12.15而NVS†为13.27（Table 5）。这一差距表明，不准确的位姿估计会严重损害几何重建质量，位姿误差与形状误差之间存在耦合——这正是位姿-形状歧义的核心表现。

值得注意的是，当在流程中引入光度一致性后，各方法在所有任务上的相对排名得以保持。这说明虽然绝对性能受位姿质量影响，但方法的相对优劣具有鲁棒性，Charge基准能够稳定区分不同方法的能力层级。

在深度估计任务上，**π³**（Wang et al., arXiv 2025）在所有子集上均取得最优AbsRel（9-sseds上0.0896，6-sssedg上0.0909），优于**VGGT**（Wang et al., CVPR 2025），确立了其在静态场景几何估计上的领先地位。

### 定性分析：失败模式的可视化

Figure 4、Figure 5和Figure 6分别展示了稠密、稀疏和单目设置下的定性渲染结果。在稠密设置下（Figure 4），各方法均能生成视觉上合理的新视角，但在动态区域（如人物手部、快速移动的衣物）仍可见模糊和伪影。稀疏设置下（Figure 5，场景050_0160），视角覆盖不足导致大面积区域出现几何坍塌和纹理模糊，尤其在远离训练视角的测试视角上。单目设置下（Figure 6），由于空间覆盖极度有限，方法在未见过的视角上产生严重的几何畸变和外观失真，动态物体的重建尤为困难。这些定性观察与定量指标一致，共同指向现有方法在稀疏和单目条件下对场景覆盖的强依赖性。

![[assets/figures/papers/paper_list_l2232_https_arxiv_org_abs_2512_13639/figures/008_Figure_4.jpg]]
*Figure 4: Example results of rendering in Charge dataset evaluation - Dense setup. Best viewed zoomed in*

![[assets/figures/papers/paper_list_l2232_https_arxiv_org_abs_2512_13639/figures/009_Figure_5.jpg]]
*Figure 5: Example results of rendering in Charge dataset evaluation - Sparse setup, scene 050 0160. Best viewed zoomed in*

![[assets/figures/papers/paper_list_l2232_https_arxiv_org_abs_2512_13639/figures/010_Figure_6.jpg]]
*Figure 6: Example results of rendering in Charge dataset evaluation - Mono setup. Best viewed zoomed in*

### 数据集特性对评估结果的影响

Charge数据集的高动态内容占比（25.1%，Table 2）和广泛的光流分布（Figure 3）是导致上述性能退化的关键因素。与DyCheck（12.6%）、Neural 3D（10.9%）和Technicolor（9.7%）相比，Charge的动态像素占比超过2倍，且光流直方图显示其涵盖更多大幅运动。这一特性使得Charge能够更有效地暴露方法在动态场景下的弱点，而此前数据集因动态内容不足而难以区分方法间的细微差异。

![[assets/figures/papers/paper_list_l2232_https_arxiv_org_abs_2512_13639/figures/004_Table_2.jpg]]
*Table 2: Percentage of dynamic content in various datasets*

![[assets/figures/papers/paper_list_l2232_https_arxiv_org_abs_2512_13639/figures/005_Figure_3.jpg]]
*Figure 3: Optical flow histogram for DyCheck and Charge*

### 公平性与局限性说明

需注意以下影响结论普适性的因素：Charge完全由合成动画生成，与真实世界捕捉的噪声、光照和动态复杂性存在领域差异，迁移至真实场景时可能需额外适应。静态基准仅选取部分静止帧，未评估基础模型在动态序列上的表现，留下评估空白。此外，基准未涵盖最新的4D重建方法（如HexPlane、K-Planes等），评估范围仍可扩展。

### 补充图表

![[assets/figures/papers/paper_list_l2232_https_arxiv_org_abs_2512_13639/figures/002_Table_1.jpg]]
*Table 1: A summary and comparison of datasets used in dynamic novel view synthesis. The top section includes datasets used for multiview evaluation whereas the middle section focuses on monocular evaluation data. † - 2 camera rig with alternating frames assigned to training and test trajectory*

## 方法谱系与知识库定位

### 数据集设计的核心定位

Charge数据集的根本定位是一个**面向下一代动态与静态重建方法的统一评估平台**。其设计出发点是弥补现有动态新视角合成数据集在动态内容占比、标注模态丰富度、相机设置多样性及测试视角覆盖上的系统性不足。与现有数据集（如DyCheck、Neural 3D、Technicolor）相比，Charge将动态像素占比提升至25.1%（Table 2），约为最好现有数据集的两倍，同时提供96 fps的高帧率捕捉和2048×858的高分辨率渲染，为评估方法在快速、大范围运动下的表现提供了更具挑战性的测试场景。

### 与现有动态重建方法的接口

Charge的基准评估覆盖了当前动态重建领域的主流方法谱系。在**多视角稠密重建**方向上，基准测试了**4DGS**（Wu et al., CVPR 2024）、**STG**（Li et al., CVPR 2024）和**Ex4DGS**（Lee et al., NeurIPS 2024）三种基于4D高斯泼溅的代表性方法。在**单目动态重建**方向上，评估了**D-3DGS**（Yang et al., CVPR 2024）、**SC-GS**（Huang et al., CVPR 2023）和**MoSca**（Lei et al., CVPR 2025）。这些方法代表了当前4D高斯泼溅框架下的不同技术路线——从多视角联合优化到单目先验引导重建，Charge通过统一的相机设置和评估协议，首次在同一数据集上对这些方法进行了系统性的横向对比。

### 与3D基础模型的接口

Charge的静态基准（Static Benchmark）面向当前快速发展的**3D基础模型**生态。评估涵盖了**VGGT**（Wang et al., CVPR 2025）和**π³**（Wang et al., arXiv 2025）等纯几何推理模型，以及**AnySplat**（Jiang et al., SIGGRAPH Asia 2025）和**WorldMirror**（Liu et al., arXiv 2025）等具备新视角合成能力的高斯泼溅生成模型。这一设计使得Charge成为连接传统重建方法与新兴基础模型的桥梁——前者依赖已知相机位姿进行场景优化，后者则从稀疏视图直接预测3D表示。

### 方法适用边界与关键发现

Charge的实验揭示了现有方法的几个关键适用边界：

**稀疏设置下的性能退化**：当训练视角从稠密（25视角）降至稀疏（9、6、3视角）时，所有动态重建方法的PSNR均出现显著下降。Table 4显示，4DGS在9视角下的PSNR为26.67，较稠密设置（28.94）下降超过2 dB，而STG和Ex4DGS的下降幅度更大。这一退化趋势与视场重叠度（FOVₒ）的降低高度相关，表明现有方法对训练视角覆盖的依赖性仍然很强。

**动态区域的系统性弱点**：在所有设置下，动态区域的PSNR（PSNR-D）始终低于静态区域（PSNR-S），且SSIM-D和LPIPS-D呈现相同趋势。这一定量证据确认了动态内容重建仍是当前方法的核心瓶颈，尤其是在稀疏和单目设置下，动态区域的视觉质量下降更为显著。

**单目设置中的轨迹敏感性**：通过设计不同的单目相机轨迹（Spline Fast/Slow, Random Walk Fast/Slow），Charge揭示了现有方法对相机运动模式的敏感性。降低移动速度或改变轨迹类型会减小FOVₒ，导致各方法PSNR随之下降，说明单目重建方法对输入视频的视场覆盖范围高度依赖。

### 位姿-形状歧义的揭示

静态基准的一个关键贡献是系统性地揭示了**位姿-形状歧义**（pose-shape ambiguity）问题。Table 5中，当仅通过源视图的Umeyama对齐进行新视角合成（NVS列）时，所有方法的性能显著低于将目标视图纳入相机对齐的方法（NVS†列）。例如，WorldMirror在m-aseds子集上NVS为17.54，而NVS†可达20.94。这一发现表明，在缺乏目标视图位姿信息时，仅从源视图推断的相机位姿与场景几何之间存在难以解耦的歧义，这为未来基础模型的设计提供了明确的改进方向。

### 局限与开放问题

Charge作为合成数据集，其核心局限在于**领域差距**——完全由Blender渲染的动画场景与真实世界捕捉在光照、噪声、运动模式上存在本质差异。现有方法在Charge上的表现能否迁移至真实场景，仍需在真实采集的动态数据上进行验证。此外，数据集仅包含单部电影的8个场景，场景多样性受限于该作品的艺术风格，可能无法代表室外场景、多人交互等更复杂的动态情境。

从评估完整性角度看，当前基准存在两个空白：一是未涵盖HexPlane、K-Planes等非高斯泼溅框架的4D重建方法；二是静态基准仅选取部分静止帧，未评估基础模型在动态序列上的表现。未来工作需扩展方法覆盖范围，并设计能够同时衡量时序一致性和运动准确性的综合评估指标。

在知识库定位上，Charge适合作为动态重建研究的**标准化压力测试集**——其高动态占比、多模态标注和可控难度梯度使其能够有效区分方法的鲁棒性差异，但其合成属性决定了它应作为真实数据集的补充而非替代。建议研究者将Charge与真实动态数据集（如DyCheck）联合使用，以全面评估方法的泛化能力。

## 原文 PDF

![[paperPDFs/CVPR_2026/Charge_A_Comprehensive_Novel_View_Synthesis_Benchmark_and_Dataset_to_Bind_Them_All.pdf]]