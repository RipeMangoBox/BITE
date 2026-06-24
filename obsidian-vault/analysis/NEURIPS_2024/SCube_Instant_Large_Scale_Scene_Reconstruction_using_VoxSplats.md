---
title: "SCube: Instant Large-Scale Scene Reconstruction using VoxSplats"
type: paper
paper_level: A
venue: NeurIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/SCube_Instant_Large_Scale_Scene_Reconstruction_using_VoxSplats.pdf
aliases:
- SCube
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "使用稀疏体素层级作为几何支架，在其上附着高斯溅射（VoxSplat）表示外观，通过两阶段生成模型（条件扩散模型生成体素几何，前馈网络预测高斯参数）在极稀疏视图下实现前馈重建。"
primary_logic: "将生成式几何重建与前馈外观预测分离，利用高分辨率稀疏卷积网络从数据中学得大规模场景先验，从而在极少输入图像下快速生成几何一致、外观锐利的完整三维场景。"
claims:
- "在Waymo Open Dataset上，SCube在重建帧和未来帧的所有指标上均大幅超越所有基线方法，包含PixelNeRF、PixelSplat、MVSplat等。"
- "图像条件策略（深度分布权重）将细粒度体素IoU从30.33%提升至34.31%，语义mIoU从16.61%提升至20.00%，验证了处理遮挡的有效性。"
- "中位体素Chamfer距离仅为0.26个体素，表明预测的几何非常接近真值。"
- "两阶段模型比单阶段模型在PSNR/LPIPS上有显著提升（19.34/0.48 vs 17.88/0.57）。"
---

# SCube: Instant Large-Scale Scene Reconstruction using VoxSplats

> [!tip] 核心洞察
> 将生成式几何重建与前馈外观预测分离，利用高分辨率稀疏卷积网络从数据中学得大规模场景先验，从而在极少输入图像下快速生成几何一致、外观锐利的完整三维场景。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SCube: 基于VoxSplat的大规模场景即时重建 |
| 英文题名 | SCube: Instant Large-Scale Scene Reconstruction using VoxSplats |
| 会议/期刊 | NeurIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2410.20030); [Project](https://research.nvidia.com/labs/toronto-ai/scube/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SCube |
| Dataset | Waymo Open Dataset, Gaussian Splatting Initialization (15 scenes, R=40) |

> [!tip] 效果简介
> - Waymo Open Dataset 上，PSNR (Reconstruction T) 为 25.90，对比 PixelSplat 22.15，变化 +3.75。
> - Waymo Open Dataset 上，LPIPS (Reconstruction T) 为 0.45，对比 PixelSplat 0.61，变化 -0.16。
> - Waymo Open Dataset 上，LPIPS (Prediction T+5) 为 0.47，对比 PixelSplat 0.60，变化 -0.13。

## 概述

从稀疏、无重叠的二维图像中重建大规模三维场景，是自动驾驶、仿真与数字孪生等领域的核心需求。传统方法依赖每场景优化（如NeRF、3D Gaussian Splatting），无法利用数据先验，在极稀疏视角下几何模糊、重建失败；前馈方法虽具备泛化能力，但输出分辨率低、几何不合理或外观模糊。SCube 的核心洞察在于：**将生成式几何重建与前馈外观预测解耦**，利用高分辨率稀疏卷积网络从大规模驾驶数据中学得场景先验，从而在极少输入图像下快速生成几何一致、外观锐利的完整三维场景。

SCube 提出 **VoxSplat** 表示——以稀疏体素层级作为几何支架，在其上附着高斯溅射（3D Gaussians）建模外观。方法分为两阶段：第一阶段的层次化体素潜空间扩散模型以图像特征为条件，渐进生成带语义的稀疏体素几何；第二阶段的前馈网络在此基础上预测每个体素内高斯splats的位置、颜色、不透明度等参数，并合成天空全景背景，实现端到端的前馈新视图合成。

在 Waymo Open Dataset 上，SCube 在重建帧与未来帧的所有指标上均大幅超越 PixelNeRF、PixelSplat、MVSplat、DUSt3R 等基线方法。以重建帧为例，PSNR 达 25.90（PixelSplat 为 22.15），LPIPS 降至 0.45（PixelSplat 为 0.61）；对未来帧的预测同样保持显著优势。几何层面，中位体素 Chamfer 距离仅 0.26 个体素，验证了预测几何与真值的高度吻合。消融实验进一步证实：深度分布加权的图像条件策略将细粒度体素 IoU 从 30.33% 提升至 34.31%，语义 mIoU 从 16.61% 提升至 20.00%；两阶段设计相比单阶段模型在 PSNR/LPIPS 上有质的飞跃（19.34/0.48 vs 17.88/0.57）。

SCube 将方法定位于 **前馈式大规模场景重建** 与 **生成式三维先验学习** 的交叉点。其 VoxSplat 表示继承了体素网格的结构化优势（适合扩散生成与稀疏卷积），又保留了高斯溅射的渲染效率与外观表现力。相比基于 NeRF 的隐式表示，SCube 具备显式、可编辑的几何；相比无结构的 3D Gaussians，SCube 提供了规则化的几何支架，使生成模型能够有效学习场景布局与语义。这一设计使其在重建速度（单场景 < 20 秒）、几何精度与渲染质量三个维度上同时取得突破，并为 LiDAR 仿真、文本到场景生成等下游应用提供了统一的三维基础。

## 背景与动机

大规模场景的三维重建是计算机视觉中的核心问题，在自动驾驶、机器人导航和虚拟现实等应用中至关重要。传统方法依赖运动恢复结构（SfM）和多视图立体（MVS）等几何技术，通过密集的图像重叠区域来恢复场景结构。然而，现实应用中的输入图像往往极为稀疏且几乎没有重叠区域——例如自动驾驶场景中仅使用三个前向摄像头拍摄的图像——这使得基于几何匹配的传统方法难以奏效。

近年来，基于神经网络的三维重建方法取得了显著进展。以NeRF为代表的可微分渲染框架通过每场景优化实现了高质量的新视图合成，但其优化过程耗时且无法利用跨场景的数据先验。前馈式方法（如**PixelNeRF**（Yu et al., CVPR 2021）和**PixelSplat**）试图通过端到端网络直接从稀疏图像预测三维表示，从而避免逐场景优化。然而，这些方法通常面临以下瓶颈：

- **几何质量受限**：前馈方法预测的几何往往模糊、低分辨率或不合理，无法支撑准确的大规模场景重建。
- **外观保真度不足**：在极稀疏视图条件下，现有方法难以生成清晰、细节丰富的新视图。
- **尺度限制**：大多数方法仅适用于小尺度场景或物体，难以扩展到数百米范围的大规模场景。

**DUSt3R**（Wang et al., arXiv 2023）等端到端点云预测方法虽然可以从稀疏视图直接回归三维点云，但其输出缺乏完整的语义信息和外观表示，难以直接用于高质量的新视图合成。**Metric3Dv2**等深度估计方法则通过反投影生成点云，但在稀疏视图下几何完整性不足。**MVSplat**和**MVSGaussian**等方法将高斯溅射与前馈网络结合，但在处理无重叠区域时仍面临挑战。

核心矛盾在于：**如何在极稀疏、低重叠的输入条件下，快速生成几何一致、外观锐利的大规模三维场景？** 这要求模型能够从数据中学得强先验知识，以弥补输入信息的不足。

SCube正是针对这一缺口而提出。其核心思想是将生成式几何重建与前馈外观预测分离：利用稀疏体素层级结构作为几何支架，通过条件扩散模型从数据中学习大规模场景的几何先验，再通过前馈网络在体素支架上附着高斯溅射来预测外观。这种解耦设计使得模型能够从仅有的3张无重叠输入图像中，在20秒内重建出包含数百万个高斯溅射的完整三维场景，同时支持新视图合成和LiDAR仿真等下游任务。

## 核心创新

SCube的核心突破在于将**生成式几何重建**与**前馈外观预测**解耦为两阶段流程，并设计了一种新型混合三维表示——**VoxSplat**（稀疏体素支架上附着的高斯溅射），从而在极稀疏、无重叠的输入视图下实现大规模场景的即时重建。以下从表示、几何、外观三个维度剖析其相对于现有baseline的关键创新。

### 1. 三维表示：从无结构高斯到VoxSplat

现有基于3D Gaussian Splatting的方法（如PixelSplat、MVSplat）直接预测无结构的高斯点云，缺乏显式的几何支架，导致在稀疏视图下容易出现几何模糊或不合理的浮空高斯。SCube提出**VoxSplat**表示（Section 3.2），将高斯溅射锚定在稀疏体素层级结构上：

- **体素作为几何支架**：稀疏体素网格提供了显式的空间占位和语义信息，约束高斯的空间分布，避免几何发散。
- **每体素多高斯**：每个体素内预测M个高斯splats，位置被限制在体素邻域内，实现局部细节建模。
- **高效渲染**：继承高斯溅射的快速光栅化能力，同时获得体素结构的几何一致性。

这一表示将体素的几何规整性与高斯的渲染灵活性结合，是支撑整个方法的核心设计。

### 2. 几何重建：从每场景优化到数据驱动的生成先验

传统方法（如NeRF、3D Gaussian Splatting）依赖每场景迭代优化，无法利用大规模数据中的场景先验，在稀疏视图下几何重建质量急剧下降。SCube在几何阶段引入**分层体素潜空间条件扩散模型**（Section 3.1）：

- **稀疏结构VAE**：首先学习稀疏体素网格的潜在空间，将高维体素几何压缩为低维潜变量，使扩散模型能够高效生成。
- **图像条件策略**：不同于baseline沿射线广播统一特征的做法，SCube利用**深度分布加权特征反投影**（Eq 1）：从DINO-v2+2D CNN提取的图像特征中预测逐像素深度分布 $\theta_{jd}^i$，将特征 $\mathbf{F}_j^i$ 按深度权重反投影到三维体素网格 $\mathbf{C}_v = \sum_{(i,j,d)} \mathbf{F}_{jd}^i$。这一设计显式处理遮挡，使特征精确定位于真实几何表面。
- **扩散生成**：以反投影的图像特征为条件，渐进式去噪生成稀疏体素网格，从数据中学习大规模场景的几何先验。

**关键证据**：消融实验表明，深度分布条件策略将细粒度体素IoU从30.33%提升至34.31%，语义mIoU从16.61%提升至20.00%（Section 4.5），验证了其处理遮挡的有效性。中位体素Chamfer距离仅0.26个体素（Table 9），表明预测几何高度接近真值。

### 3. 外观预测：从优化拟合到前馈推理

传统方法需要每场景优化外观参数，耗时长且难以泛化。SCube的外观阶段采用**前馈3D稀疏UNet**（Section 3.2），以生成的体素几何和图像特征为输入，直接预测每个体素内高斯的参数（位置 $\mu_v$、颜色RGB、不透明度 $\alpha_v$、尺度 $s_v$、旋转 $\mathbf{R}_v$，Eq 4）：

- **几何条件化**：外观网络以已生成的体素几何为条件，避免从零开始预测空间结构，大幅降低学习难度。
- **天空全景模型**：额外构建天空特征全景图，通过Alpha合成（Eq 5）与前景高斯渲染融合，解决远距离天空区域的建模问题。
- **单次前馈**：无需测试时优化，推理速度快（完整场景重建<20秒）。

**关键证据**：两阶段模型相比单阶段模型（直接端到端预测），PSNR从17.88提升至19.34，LPIPS从0.57降至0.48（Table 3），证明了解耦几何与外观的必要性。

### 4. 创新总结

| 维度 | Baseline做法 | SCube创新 | 证据锚点 |
|------|-------------|-----------|----------|
| 三维表示 | 无结构3D Gaussians / NeRF | VoxSplat：稀疏体素支架+附着高斯 | Section 3.2 |
| 几何重建 | SfM或每场景优化 | 分层体素潜空间扩散模型（数据驱动先验） | Section 3.1 |
| 图像条件 | 沿射线广播统一特征 | 深度分布加权反投影（处理遮挡） | Eq 1; Section 4.5 |
| 外观预测 | 每场景优化拟合 | 前馈网络预测高斯参数+天空全景 | Section 3.2 |
| 推理效率 | 分钟至小时级优化 | <20秒前馈重建 | Introduction |

这些创新使SCube在Waymo Open Dataset上全面超越PixelNeRF、PixelSplat、MVSplat等baseline，重建帧PSNR达25.90（+3.75 vs PixelSplat），LPIPS降至0.45（-0.16 vs PixelSplat）（Table 1）。

## 整体框架

SCube 采用“先几何、后外观”的两阶段前馈重建范式，将极稀疏（甚至无重叠）的输入图像转化为以 **VoxSplat** 表示的大规模三维场景。其核心思想是将生成式几何重建与前馈外观预测解耦：第一阶段利用数据驱动的场景先验生成稀疏体素几何支架，第二阶段在该支架上附着高斯溅射并预测天空背景，从而实现几何一致、外观锐利的完整场景重建。

### 概率化流程

整个流程可形式化为从联合分布中采样：

$$p(\mathcal{G}, \hat{A} \mid \mathcal{T}) = p(A \mid \mathcal{G}, \mathcal{T})\, p(\mathcal{G} \mid \mathcal{T})$$

其中 $\mathcal{T}$ 为 $N$ 张稀疏输入图像，$\mathcal{G}$ 为带语义特征的稀疏体素网格（几何），$\hat{A}$ 为包含 VoxSplat 和天空全景的外观表示。该分解将重建任务拆分为两个可独立训练的子问题：几何先验建模 $p(\mathcal{G} \mid \mathcal{T})$ 和外观条件预测 $p(A \mid \mathcal{G}, \mathcal{T})$。

### 两阶段模块架构

**阶段一：生成式几何重建**（§3.1）
- **图像特征编码器**：使用 DINO-v2 结合 2D CNN 从每张输入图像提取特征，同时预测逐像素的深度分布 $\theta_j^i$。
- **深度加权特征反投影**：利用深度分布将图像特征反投影到三维体素网格，处理遮挡并精确定位几何信息：
  $$\mathbf{F}_{jd}^{i} = \theta_{jd}^{i} \cdot \mathbf{F}_{j}^{i}, \quad \mathbf{C}_{v} = \sum_{(i,j,d)} \mathbf{F}_{jd}^{i} \in \mathbb{R}^{C}$$
- **稀疏结构 VAE**：学习稀疏体素层级的潜在空间，将高分辨率体素网格压缩为紧凑的潜变量。
- **分层体素潜空间扩散模型**：基于 XCube 架构，以图像条件特征为引导，渐进生成带语义 logit 的稀疏体素网格 $\mathcal{G}$。训练损失结合扩散损失与深度焦损失：
  $$\mathcal{L} = \mathcal{L}_{\mathrm{Diffusion}} + \lambda \mathcal{L}_{\mathrm{Depth}}, \quad \mathcal{L}_{\mathrm{Depth}} = \mathbb{E}_{\mathbf{X}, i, j} \mathrm{Focal}(\theta_j^i, [\theta_j^i]_{\mathrm{gt}})$$

**阶段二：前馈外观预测**（§3.2）
- **VoxSplat 外观 UNet**：以阶段一生成的体素网格 $\mathcal{G}$ 和图像特征为输入，使用三维稀疏卷积网络预测每个体素内 $M$ 个高斯溅射的参数（位置 $\mu$、颜色 RGB、不透明度 $\alpha$、协方差 $\Sigma$）。高斯位置被约束在其支撑体素的邻域内：
  $$G(\pmb{x}) = \operatorname{RGB} \cdot \alpha \cdot \mathrm{e}^{-\frac{1}{2}(\pmb{x} - \pmb{\mu})^{\top} \pmb{\Sigma}^{-1}(\pmb{x} - \pmb{\mu})}$$
- **天空全景模型**：构建天空特征全景图并解码为背景图像，用于填充远距离/天空区域。
- **前景-背景合成**：将高斯渲染的前景与天空全景进行 Alpha 合成：
  $$\mathbf{I}_{\mathrm{pred}}(u,v) = \mathbf{I}_{\mathrm{GS}}(u,v) + (1 - \mathbf{T}(u,v)) \cdot \mathbf{I}_{\mathrm{bg}}(u,v)$$
- **训练损失**：组合 L1、掩码 L1、SSIM 和 LPIPS 损失：
  $$\mathcal{L} = \lambda_1 \mathcal{L}_1(\mathbf{I}_{\mathrm{pred}}^i, \mathbf{I}_{\mathrm{gt}}^i) + \lambda_2 \mathcal{L}_1(\mathbf{T}^i, \mathbf{M}^i) + \lambda_{\mathrm{SSIM}} \mathcal{L}_{\mathrm{SSIM}} + \lambda_{\mathrm{LPIPS}} \mathcal{L}_{\mathrm{LPIPS}}$$

**可选后处理**（§3.3）：通过 GAN 对渲染图像进行细化，减少体素化伪影，但需每场景约 20 分钟独立训练。

### 输入输出流

- **输入**：3 张（或更多）稀疏、可能无重叠的前向视图图像。
- **中间表示**：$1024^3$ 分辨率的稀疏体素网格，每个体素携带语义 logit。
- **最终输出**：VoxSplat 表示（数百万个高斯溅射附着在稀疏体素支架上）+ 天空全景背景，可直接用于新视图合成或 LiDAR 仿真。
- **推理效率**：从图像到完整场景重建耗时不到 20 秒。

整体框架的端到端流程见 **Figure 2**，该图清晰展示了两阶段的模块关系与数据流向。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/002_Figure_2.jpg]]
*Figure 2: Framework. SCube consists of two stages: (1) We reconstruct a sparse voxel grid with semantic logit conditioned on the input images using a conditional latent diffusion model based on XCube [39]. (2) We predict the appearance of the scene represented as VoxSplats and a sky panorama using a feedforward network. Our method allows us to synthesize novel views in a fast and accurate manner, along with many other applications*

## 核心模块与公式推导

SCube 将稀疏视图重建分解为两个解耦阶段：**几何重建**与**外观预测**，对应概率分解 $p(\mathcal{G}, \hat{A} | \mathcal{T}) = p(A | \mathcal{G}, \mathcal{T}) \, p(\mathcal{G} | \mathcal{T})$。以下逐一拆解各核心模块及其关键公式。

### 3.1 图像特征编码与深度感知反投影

输入 $N$ 张稀疏图像 $\{I^i\}_{i=1}^N$，首先通过 **DINO-v2** 与 **2D CNN** 组成的特征编码器提取多尺度图像特征，同时预测每像素的深度分布 $\theta_j^i$（其中 $j$ 为像素索引，$d$ 为深度离散化索引）。

**核心创新**在于深度分布加权的特征反投影（Eq 1），以解决稀疏无重叠视图下的遮挡歧义：

$$
\mathbf{F}_{jd}^{i} = \theta_{jd}^{i} \cdot \mathbf{F}_{j}^{i}, \quad \mathbf{C}_{v} = \sum_{(i,j,d)} \mathbf{F}_{jd}^{i} \in \mathbb{R}^{C}
$$

**变量含义**：$\mathbf{F}_j^i$ 为图像 $i$ 在像素 $j$ 处的特征向量；$\theta_{jd}^i$ 为该像素在深度 $d$ 处的预测概率权重；$\mathbf{F}_{jd}^i$ 为深度加权后的特征；$\mathbf{C}_v$ 为体素 $v$ 处聚合得到的条件特征。该机制使特征沿射线按深度分布“投票”到三维体素网格，而非简单广播，从而有效抑制遮挡区域的错误特征注入。消融实验证实，该策略将细粒度体素 IoU 从 30.33% 提升至 34.31%，语义 mIoU 从 16.61% 提升至 20.00%（§4.5）。

为监督深度分布学习，几何阶段训练损失（Eq 2）在扩散损失基础上加入焦损失项：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{Diffusion}} + \lambda \mathcal{L}_{\mathrm{Depth}}, \quad \mathcal{L}_{\mathrm{Depth}} = \mathbb{E}_{\mathbf{X}, i, j} \mathrm{Focal}(\theta_{j}^{i}, [\theta_{j}^{i}]_{\mathrm{gt}})
$$

其中 $\mathcal{L}_{\mathrm{Depth}}$ 以 LiDAR 投影得到的真实深度分布为监督信号，$\lambda$ 为平衡系数。

### 3.2 稀疏结构 VAE 与分层体素潜空间扩散模型

几何重建采用基于 **XCube** 的条件潜空间扩散模型，在稀疏体素层级上渐进生成场景几何。首先通过 **Sparse Structure VAE** 将稀疏体素网格编码为紧凑潜表示，扩散模型在该潜空间中执行去噪过程。扩散损失采用 v-参数化形式（Eq 7，详见附录 A）：

$$
\mathcal{L}_{\mathrm{Diffusion}} = \mathbb{E}_{t, \mathbf{X}, \epsilon \sim \mathcal{N}(0, I)} \left[ \left\| v( \sqrt{\bar{\alpha}_t} \mathbf{X} + \sqrt{1 - \bar{\alpha}_t} \epsilon, t ) - ( \sqrt{\bar{\alpha}_t} \epsilon - \sqrt{1 - \bar{\alpha}_t} \mathbf{X} ) \right\|_2^2 \right]
$$

扩散模型以图像条件特征 $\mathbf{C}_v$ 为引导，分层生成从粗到细的稀疏体素网格 $\mathcal{G}$，每个体素携带语义 logit。定量评估显示中位体素 Chamfer 距离仅为 0.26 个体素（Table 9），表明预测几何与真值高度吻合。

### 3.3 VoxSplat 外观表示与前馈预测

外观阶段采用 **VoxSplat** 表示：在几何阶段输出的稀疏体素支架上，每个体素内附着 $M$ 个高斯溅射（Gaussian Splats）。高斯函数定义为（Eq 3）：

$$
G(\pmb{x}) = \operatorname{RGB} \cdot \alpha \cdot \mathrm{e}^{-\frac{1}{2}(\pmb{x} - \pmb{\mu})^{\top} \pmb{\Sigma}^{-1}(\pmb{x} - \pmb{\mu})}
$$

其中 $\pmb{\mu}$ 为高斯中心，$\pmb{\Sigma}$ 为协方差矩阵，$\alpha$ 为不透明度，RGB 为颜色值。高斯中心被约束在支撑体素的邻域范围内，确保外观与几何的对齐。

**3D 稀疏卷积 UNet** 以前馈方式预测每个体素内高斯的原始参数 $(\bar{\mu}_v, \bar{\alpha}_v, \bar{s}_v, \bar{\mathbf{q}}_v, \mathrm{RGB}_v)$，随后通过激活函数转换为实际渲染参数（Eq 4）：

$$
\mu_v = r \cdot \tanh{\bar{\mu}}_v + \mathrm{Center}_v, \quad \alpha_v = \mathrm{sigmoid}({\bar{\alpha}}_v), \quad s_v = \exp{\bar{s}}_v, \quad \mathbf{R}_v = \mathrm{quat2rot}({\bar{\mathbf{q}}}_v)
$$

其中 $r$ 为邻域半径，$\mathrm{Center}_v$ 为体素中心坐标，$s_v$ 为尺度，$\mathbf{R}_v$ 为由四元数转换的旋转矩阵。颜色目前仅使用 0 阶球谐系数（DC 分量），不支持视角相关效果。

### 3.4 天空全景背景与前景-背景合成

为处理无几何覆盖的远距离天空区域，引入 **Sky Panorama Model**：将图像特征沿极坐标投影构建天空特征全景图，解码为背景图像 $\mathbf{I}_{\mathrm{bg}}$。最终渲染图像由高斯溅射前景与天空背景通过 alpha 合成得到（Eq 5）：

$$
\mathbf{I}_{\mathrm{pred}}(u,v) = \mathbf{I}_{\mathrm{GS}}(u,v) + (1 - \mathbf{T}(u,v)) \cdot \mathbf{I}_{\mathrm{bg}}(u,v)
$$

其中 $\mathbf{T}(u,v)$ 为沿像素 $(u,v)$ 光线的累积透射率，$\mathbf{I}_{\mathrm{GS}}$ 为高斯溅射渲染的前景。

### 3.5 外观阶段训练损失

外观模型训练采用组合损失（Eq 6），同时约束渲染图像质量和前景掩码：

$$
\mathcal{L} = \lambda_1 \mathcal{L}_1(\mathbf{I}_{\mathrm{pred}}^i, \mathbf{I}_{\mathrm{gt}}^i) + \lambda_2 \mathcal{L}_1(\mathbf{T}^i, \mathbf{M}^i) + \lambda_{\mathrm{SSIM}} \mathcal{L}_{\mathrm{SSIM}}(\mathbf{I}_{\mathrm{pred}}^i, \mathbf{I}_{\mathrm{gt}}^i) + \lambda_{\mathrm{LPIPS}} \mathcal{L}_{\mathrm{LPIPS}}(\mathbf{I}_{\mathrm{pred}}^i, \mathbf{I}_{\mathrm{gt}}^i)
$$

其中 $\mathbf{M}^i$ 为真实前景掩码，训练视图从输入图像的邻近 10 帧中采样。消融实验表明，两阶段模型（体素几何 + 外观）相比单阶段模型，PSNR 从 17.88 提升至 19.34，LPIPS 从 0.57 降至 0.48（Table 3），验证了分解设计的有效性。

### 3.6 可选 GAN 后处理

为减少体素化伪影，可附加一个轻量 GAN 对渲染图像进行细化（§3.3），但需每场景约 20 分钟独立训练，影响推理效率。该模块为可选组件，SCube 基础版本不依赖此后处理即可取得有竞争力的结果。

## 实验与分析

### 实验设置

SCube在**Waymo Open Dataset**上进行了系统评估，所有对比方法均在该数据集上重新训练，统一使用**三个前向视图**作为输入，以保证公平比较。评估时排除移动物体区域，仅计算前三个视角的重叠区域。输入图像分辨率为$640 \times 960$，体素网格分辨率默认采用$1024^3$，每个体素预测4个高斯溅射体。

#### 基准线方法

实验涵盖了多种主流重建范式：
- **PixelNeRF**（Yu et al., CVPR 2021）：基于NeRF的稀疏视图重建
- **PixelSplat**：基于3D高斯溅射的稀疏视图重建
- **MVSplat**：多视图立体高斯溅射方法
- **MVSGaussian**：多视图高斯溅射方法
- **DUSt3R**（Wang et al., arXiv 2023）：端到端点云预测
- **Metric3Dv2**：单目深度估计+反投影重建

### 新视图合成主结果

Table 1展示了SCube与各基准线在Waymo Open Dataset上的定量对比。SCube在**重建帧（T）和未来帧（T+5, T+10）**的所有指标上均大幅超越所有基线方法：

**重建帧（T）表现：**
- SCube达到**PSNR 25.90**，相比最强基线PixelSplat（22.15）提升**+3.75 dB**
- LPIPS降至**0.45**，相比PixelSplat（0.61）降低**0.16**
- SSIM达到**0.77**，显著优于其他方法

**未来帧预测表现：**
- T+5帧：PSNR 19.90，LPIPS 0.47（PixelSplat为0.60）
- T+10帧：PSNR 18.78，LPIPS 0.49（PixelSplat为0.60）

SCube在未来帧上的优势尤为突出，说明其重建的几何结构具有较好的时序一致性，而PixelSplat等方法的性能随视角外推快速衰减。

Figure 4的定性对比进一步验证：SCube能够重建完整的场景几何，包括远距离区域，而基线方法在稀疏输入下往往产生模糊、不完整或几何不合理的重建结果。俯视图可视化显示SCube的体素几何支架提供了清晰的结构先验。

### 几何重建质量

SCube的核心优势在于其**生成式几何重建**能力。Table 9报告了体素Chamfer距离：SCube的中位Chamfer距离仅为**0.26个体素**，表明预测的稀疏体素几何与真值高度吻合。单阶段非扩散模型的Chamfer距离显著更高，验证了扩散模型在几何生成中的关键作用。

Figure 5展示了与Metric3Dv2的几何重建对比。Metric3Dv2通过逐帧深度估计+反投影的方式，在稀疏视角下产生大量空洞和不一致，而SCube利用数据先验生成完整的语义几何结构。

### 高斯溅射初始化

Table 2展示了SCube作为3D Gaussian Splatting初始化的能力。在15个场景上，使用SCube初始化的3DGS训练（R=40帧）达到**PSNR 26.07**，相比随机初始化（24.93）提升**+1.14 dB**。这验证了SCube的前馈几何预测为后续优化提供了优质的起点。

### 消融实验

#### 两阶段 vs 单阶段

Table 3的核心消融对比了两阶段模型（体素几何扩散+外观前馈）与单阶段模型（直接端到端预测）。两阶段模型实现**PSNR 19.34, LPIPS 0.48**，相比单阶段模型（PSNR 17.88, LPIPS 0.57）有显著提升。Figure 10的视觉消融直观展示了单阶段模型产生模糊几何和外观伪影，而两阶段模型保持了清晰的几何结构和锐利外观。

#### 图像条件策略

深度分布加权条件（Eq 1）是处理遮挡的关键设计。消融实验表明，该策略将**细粒度体素IoU从30.33%提升至34.31%**，语义mIoU从16.61%提升至20.00%。移除深度分布监督后，模型无法有效区分遮挡和非遮挡区域，导致几何定位精度下降。

#### 体素分辨率与高斯数量

Table 3还探索了体素分辨率和高斯数量的影响：
- $1024^3$体素+每体素4个高斯：PSNR 19.34, LPIPS 0.48（最优）
- $256^3$体素：PSNR显著下降，几何细节丢失（Figure 10c）
- 每体素1个高斯：PSNR 19.16, LPIPS 0.49，略低于4个高斯配置

#### PixelSplat深度监督

Table 4显示，为PixelSplat添加深度监督后性能反而下降，说明直接为前馈高斯方法添加深度约束可能与其隐式几何学习机制冲突，而SCube的显式体素几何支架天然支持深度监督。

### 失败模式与局限性

1. **视角相关效果缺失**：外观模型当前仅使用0阶球谐系数，不支持镜面反射等视角相关颜色效果，在包含车辆玻璃、湿润路面等场景中表现受限。

2. **GAN后处理效率**：可选的GAN后处理（SCube+）可进一步减少体素化伪影（Figure 8），但需要每场景约20分钟独立训练，影响推理效率。

3. **数据依赖性**：训练依赖LiDAR+COLMAP融合的高质量三维真值（Figure 3），在缺少精确几何数据的域中泛化能力未经验证。

4. **极端条件未验证**：在极端光照、雨雪天气条件下的重建质量缺乏系统评估。

5. **动态物体**：当前仅支持单个时间戳的静态场景重建，未建模移动物体和时变外观。

### 关键图表索引

- **Table 1**：新视图合成主结果，SCube在所有指标上大幅领先
- **Table 2**：高斯溅射初始化对比，SCube初始化优于随机初始化
- **Table 3**：外观重建消融，两阶段模型和$1024^3$分辨率最优
- **Table 4**：PixelSplat深度监督消融，深度监督对基线无效
- **Table 9**：几何质量对比，中位Chamfer距离仅0.26体素
- **Figure 4**：新视图合成定性对比
- **Figure 5**：几何重建对比
- **Figure 10**：视觉消融实验

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/020_Figure_10.jpg]]
*Figure 10: Visual Ablation Study. (a) SCube+ (b) SCube (c) SCube with a 2 5 6 ^ { 3 } resolution input grid (d) Single-stage model. Zoom in for a better view*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/006_Table_1.jpg]]
*Table 1: Quantitative Comparisons on 3D Reconstruction. The metrics are computed both at the input frame T and future frames. ↑: higher is better, ↓: lower is better*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/008_Table_2.jpg]]
*Table 2: Initializations for Gaussian Splatting training. We train 3D Gaussians with different initialization for R frames. We report the test-set metrics. ↑: higher is better, ↓: lower is better*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/012_Table_3.jpg]]
*Table 3: Ablation Study for Appearance Reconstruction*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/013_Table_4.jpg]]
*Table 4: Comparison of PixelSplat and PixelSplat with Depth Supervision*

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/022_Figure_11.jpg]]
*Figure 11: More Text-2-Scene Generation. The generated multi-view images may contain flaws, while SCube is still able to reconstruct the 3D scenes*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/023_Figure_12.jpg]]
*Figure 12: A suburban neighborhood features a park with green trees, residential houses with red-tiled roofs, streets with bike lane signs and white markings, well-maintained lawns, and sidewalks. Figure 12: More Text-2-Scene Generation*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/014_Table_5.jpg]]
*Table 5: Hyperparameters for VAE*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/015_Table_6.jpg]]
*Table 6: Hyperparameters for voxel latent diffusion models*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/016_Table_7.jpg]]
*Table 7: Hyperparameters for 3D sparse UNet in appearance reconstruction stage*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2410_20030/figures/017_Table.jpg]]

## 方法谱系与知识库定位

### 核心差异与因果机制

SCube 与现有方法的关键分水岭在于**是否利用数据驱动的三维先验**。传统方法如 **PixelNeRF**（Yu et al., CVPR 2021）和 **DUSt3R**（Wang et al., arXiv 2023）依赖逐场景优化或端到端回归，但缺乏从大规模数据中学习的场景级几何先验，导致在稀疏、无重叠视图下产生模糊或不合理的几何。SCube 通过两阶段生成式框架解决了这一问题：

1. **几何阶段**：使用基于 XCube 的分层体素潜空间扩散模型，以输入图像的深度分布加权特征为条件，生成稀疏体素网格几何。这一步的核心是将几何重建转化为从数据中学得的先验采样问题，而非从零开始的优化。
2. **外观阶段**：在固定几何支架上，使用前馈 3D 稀疏卷积网络直接预测每个体素内高斯溅射的参数（VoxSplat），实现快速、锐利的外观重建。

因果链条为：**数据驱动的体素几何先验 → 即使在极稀疏输入下也能生成完整、几何一致的三维结构 → 前馈外观网络在此结构上生成高质量纹理**。消融实验（Table 3）证实了这一分离的必要性：两阶段模型相比单阶段模型，PSNR 从 17.88 提升至 19.34，LPIPS 从 0.57 降至 0.48。

### 相对于基线的改进槽位

| 改进维度 | 基线方法 | 基线缺陷 | SCube 方案 | 证据强度 |
|---------|---------|---------|-----------|---------|
| **三维表示** | NeRF（PixelNeRF）或无结构 3D Gaussians（PixelSplat、MVSplat） | NeRF 渲染慢；无结构 Gaussians 缺乏几何约束，易产生漂浮物 | VoxSplat：稀疏体素支架上附着高斯溅射，兼顾几何约束与渲染效率 | 强（Table 1：PSNR +3.75 vs PixelSplat） |
| **几何重建方式** | SfM + 逐场景优化（3DGS）或端到端点云回归（DUSt3R） | 需要足够重叠视图；稀疏视图下失效 | 分层体素潜空间扩散模型，利用数据先验补全缺失几何 | 强（Table 9：中位体素 Chamfer 距离仅 0.26 个体素） |
| **图像条件策略** | 沿射线广播统一特征（PixelNeRF） | 无法处理遮挡，特征错误分配到空白区域 | 深度分布加权特征反投影（Eq 1），利用预测的逐像素深度分布精确定位三维特征 | 强（消融：细粒度体素 IoU 从 30.33% 提升至 34.31%） |
| **外观预测** | 逐场景优化拟合（3DGS） | 耗时长，无法前馈推理 | 前馈网络直接预测高斯参数 + 天空全景背景 | 强（推理时间 < 20 秒） |

### 适用边界与局限

**适用场景**：
- 大规模户外场景的稀疏视图重建（Waymo Open Dataset 验证）
- 需要快速推理的场景（单次前馈 < 20 秒）
- 几何一致性要求高的应用（如 LiDAR 仿真、新视图合成）
- 可作为 3D Gaussian Splatting 的初始化，提升逐场景优化起点（Table 2：PSNR 从 24.93 提升至 26.07）

**已知局限**（需在应用中注意）：
1. **视角相关效果缺失**：外观模型仅使用 0 阶球谐系数，不支持高光等视角相关颜色效果。这意味着在金属表面、湿润路面等场景下可能产生不真实渲染。
2. **GAN 后处理效率低**：可选的 GAN 细化步骤需要每场景约 20 分钟独立训练，破坏了前馈推理的实时性优势。
3. **训练数据依赖**：依赖高质量三维真值（LiDAR + COLMAP 融合），在缺少精确几何数据的域中（如室内、非结构化自然场景）泛化能力未经验证。
4. **动态场景未建模**：当前仅支持单个时间戳的静态场景，移动物体需在数据预处理阶段通过边界框补偿（Figure 3），无法处理时变外观。
5. **极端条件未验证**：在极端光照、雨雪天气等条件下的表现缺乏实验支持。

### 开放问题与未来方向

1. **动态场景建模**：如何将 VoxSplat 框架扩展到包含移动物体和时变外观的动态场景？可能的路径包括引入 4D 体素表示或分离静态背景与动态前景。
2. **跨域泛化**：能否通过域适应或自监督学习，在无需大规模 3D 真值的情况下将模型泛化到一般户外场景？这需要解决几何真值获取的瓶颈。
3. **遮挡区域外观补全**：当前方法对严重遮挡区域的外观预测质量有限。引入更强的生成先验（如视频扩散模型）可能是一个方向。
4. **端到端可控生成**：Figure 7 展示了文本到场景的初步能力，但流程是分离的（先生成多视图图像，再重建）。实现端到端的可控生成需要将文本条件直接注入几何和外观两个阶段。
5. **高阶外观建模**：引入更高阶球谐系数或小型 MLP 解码器来支持视角相关效果，同时保持前馈推理效率，是一个工程上可行的改进方向。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/SCube_Instant_Large_Scale_Scene_Reconstruction_using_VoxSplats.pdf]]
