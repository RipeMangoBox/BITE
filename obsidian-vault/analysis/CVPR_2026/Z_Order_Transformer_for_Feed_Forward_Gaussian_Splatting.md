---
title: Z-Order Transformer for Feed-Forward Gaussian Splatting
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Z_Order_Transformer_for_Feed_Forward_Gaussian_Splatting.pdf
project_link: null
code_link: null
aliases:
- ZOT
- ZOTFFGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用Z-order曲线将非结构化高斯原语组织成保持空间局部性的紧凑序列，并通过分组注意力与top-k注意力协同实现对局部与长程依赖的高效建模。
primary_logic: 将高斯原语按其三维空间位置进行Z-order排序，生成一种既保留空间邻近性又适合Transformer处理的序列化表示，然后引入分组注意力和基于重要性的top-k选择注意力，在控制计算复杂度的同时高效聚合上下文信息，并通过位偏移的Z-order池化自适应地抑制冗余，最终在单次前向传播中实现高质量、少图元的高斯重建。
claims:
- Z-order序列化将像素级高斯转化为空间紧凑的序列，消除了对密集体素网格的依赖，显著减少计算和内存开销。
- 分组注意力捕捉局部空间块，top-k注意力选择关键块，门控融合两者实现稀疏注意力，避免全注意力的高成本。
- 在多个基准数据集上，所有视图配置下均优于现有方法，且高斯图元数量减少2-3倍，推理速度比优化式方法快约1000倍。
- RealEstate10K (360×640) — 2 views 上 PSNR / SSIM / LPIPS = 26.43 / 0.873 / 0.147
---

# Z-Order Transformer for Feed-Forward Gaussian Splatting

> [!tip] 核心洞察
> 将高斯原语按其三维空间位置进行Z-order排序，生成一种既保留空间邻近性又适合Transformer处理的序列化表示，然后引入分组注意力和基于重要性的top-k选择注意力，在控制计算复杂度的同时高效聚合上下文信息，并通过位偏移的Z-order池化自适应地抑制冗余，最终在单次前向传播中实现高质量、少图元的高斯重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向前馈高斯泼溅的Z-Order Transformer |
| 英文题名 | Z-Order Transformer for Feed-Forward Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.13465) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Z-Order Transformer |
| Dataset | RealEstate10K (360×640) — 2 views, RealEstate10K (360×640) — 12 views, DL3DV (256×448) — 12 views, RealEstate10K → ACID |

> [!tip] 效果简介
> - RealEstate10K (360×640) — 2 views 上，PSNR / SSIM / LPIPS 26.43 / 0.873 / 0.147 vs DepthSplat 26.03 / 0.873 / 0.158 (+0.40 / 0.000 / -0.011)。
> - RealEstate10K (360×640) — 12 views 上，PSNR / SSIM / LPIPS 28.56 / 0.901 / 0.110 vs AnySplat 26.94 / 0.892 / 0.122 (+1.62 / +0.009 / -0.012)。
> - DL3DV (256×448) — 12 views 上，PSNR / SSIM / LPIPS 27.09 / 0.892 / 0.124 vs DepthSplat 25.74 / 0.844 / 0.131 (+1.35 / +0.048 / -0.007)。

## 概要

### 问题瓶颈

前馈式3D高斯泼溅（Feed-Forward 3D Gaussian Splatting）旨在从稀疏多视图图像中直接预测3D高斯原语，以实现高效的新视角合成。然而，现有方法面临一个根本性矛盾：逐像素（pixel-wise）生成策略产生海量冗余图元，计算与存储开销巨大；而体素化（voxel-wise）聚合方法虽能压缩图元，却引入量化误差，且固定网格无法自适应场景的稀疏与密集区域，导致细节丢失。如何在保持高重建质量的同时，大幅压缩高斯原语数量并提升推理效率，是该领域尚未解决的核心瓶颈。

### 核心方法

本文提出**Z-Order Transformer**，一种全新的前馈高斯泼溅框架。其核心思路是将非结构化的3D高斯原语按其空间坐标进行Z-order曲线排序，形成一种既保持空间局部性又适配Transformer处理的紧凑2D序列表示。围绕这一表示，方法引入两项关键设计：

- **稀疏注意力机制**：由分组注意力（group attention）捕获局部空间块模式，与top-k选择性注意力（top-k selective attention）聚焦关键块信息，并通过可学习门控网络自适应融合两者，在避免全注意力平方级复杂度的同时高效聚合上下文。
- **Z-order池化**：通过位偏移（bit-shift）操作对序列进行层次化分组池化，自适应地抑制冗余图元，在单次前向传播中逐步压缩高斯表示。

### 主要结果

在RealEstate10K和DL3DV等多个基准数据集上，Z-Order Transformer在所有视图配置下均一致优于现有前馈方法。以RealEstate10K 12视图设置为例，PSNR达到28.56 dB，较最优基线**AnySplat**提升1.62 dB，SSIM达0.901，LPIPS降至0.110。跨数据集泛化实验（RealEstate10K→ACID）同样取得1.51 dB的PSNR增益，验证了方法的鲁棒性。效率方面，方法的高斯原语数量较逐像素方法减少约3倍，推理速度比优化式方法**3DGS**快约1000倍，在质量与效率之间取得了突破性平衡。

### 方法谱系与知识库定位

Z-Order Transformer处于前馈式3D高斯泼溅的方法谱系中，其前置基线包括：

- 优化式方法：**3DGS**（per-scene optimization）及其抗锯齿变体**MipSplatting**，质量高但需逐场景迭代优化，推理极慢。
- 前馈逐像素方法：**DepthSplat**等利用深度估计直接为每个像素预测高斯原语，速度快但图元冗余严重。
- 前馈体素方法：**AnySplat**等通过体素网格聚合图元，压缩了数量但受限于固定分辨率的量化误差。

本方法通过Z-order序列化与稀疏注意力，首次在不依赖密集体素网格的前提下，实现了空间自适应的图元压缩与上下文聚合，填补了“保持细节”与“压缩图元”之间的空白。其Z-order表示与分组-选择注意力机制为后续前馈3D重建中的高效空间建模提供了新的技术路径。



### 问题背景：前馈三维高斯泼溅中的表示瓶颈

三维高斯泼溅（3D Gaussian Splatting, 3DGS）作为一种显式辐射场表示，在新视角合成任务中展现出卓越的渲染质量与速度。然而，传统3DGS依赖逐场景的优化过程，无法直接泛化到新场景。前馈（feed-forward）方法试图通过神经网络从多视图图像直接预测高斯原语，从而绕过逐场景优化，但其在表示效率上面临根本性瓶颈。

当前前馈GS方法主要采用两种高斯表示形式（参见Figure 2）：

- **像素级表示（pixel-level）**：为每张输入图像的每个像素生成对应的高斯原语。这种方式虽然保留了细粒度信息，但产生的图元数量巨大（与像素数成正比），导致严重的计算冗余和内存开销。
- **体素级表示（voxel-level）**：将像素级高斯聚合到固定的三维体素网格中。这种策略虽然压缩了图元数量，但引入量化误差，且固定分辨率的网格难以在保持细节的同时实现高效压缩——细网格丢失细节，密网格则计算成本激增。

这一矛盾构成了前馈GS领域的关键瓶颈：**如何在显著压缩高斯原语数量的同时，保留足够的几何与外观细节以实现高质量新视角合成？**

### 现有方法的局限

基于优化的方法如3DGS和MipSplatting虽然渲染质量高，但需要数分钟至数小时的逐场景训练，无法满足实时应用需求。前馈方法中，DepthSplat采用像素级表示，生成大量冗余图元；AnySplat采用体素级表示，受限于固定网格的量化误差。这些方法均未有效解决表示紧凑性与细节保真度之间的权衡。

更根本的问题在于，前馈GS缺乏一种能够**自适应地组织非结构化三维高斯原语**的表示形式。像素级和体素级表示都是对三维空间的刚性划分，无法根据场景内容灵活调整原语分布。Transformer架构具备建模长程依赖的能力，但直接对海量高斯原语应用全注意力（full attention）在计算上不可行。

### 本文动机与核心思路

本文的核心洞察是：**利用Z-order曲线将非结构化高斯原语组织成保持空间局部性的紧凑序列，从而将Transformer高效地引入前馈GS框架**。

Z-order（Morton码）是一种空间填充曲线，通过比特交叉将三维坐标映射为一维编码，使得在原始三维空间中邻近的点在序列中也保持邻近。这一性质恰好满足两个需求：（1）将三维高斯原语序列化为适合Transformer处理的二维序列；（2）序列中的局部块自然对应三维空间中的局部区域，为设计高效的稀疏注意力提供了结构基础。

基于这一表示，本文提出**Z-Order Transformer**，核心组件包括：

- **Z-order序列化**：将像素级高斯按其三维空间位置进行Z-order排序，生成紧凑的二维序列表示，消除对密集体素网格的依赖。
- **稀疏注意力机制**：由分组注意力（group attention）和top-k选择性注意力协同构成。分组注意力捕获局部空间块的上下文，top-k注意力基于重要性得分选择关键块进行精细建模，两者通过可学习门控自适应融合，在控制计算复杂度的同时高效聚合局部与长程信息。
- **自适应Z-order池化**：通过位偏移（bit-shift）的分组池化操作，在保持空间局部性的前提下逐步压缩高斯原语，实现图元数量的自适应缩减。

该方法在单次前向传播中完成从多视图图像到压缩高斯表示的端到端映射，在多个基准数据集上以2-3倍更少的高斯原语取得优于现有方法的渲染质量，推理速度比优化式方法快约1000倍。



## 核心方法与创新机理

Z-Order Transformer 的核心创新在于重新定义了前馈高斯泼溅（Feed-Forward 3DGS）中高斯原语的表示、聚合与压缩方式，通过三个紧密耦合的“changed slots”构建了一条高效的推理管线。

**瓶颈分析**：现有前馈方法面临两难困境。逐像素（pixel-wise）预测生成大量冗余高斯原语，计算和存储开销巨大；而体素化（voxel-wise）方法虽能压缩图元，却引入量化误差，且固定网格无法自适应场景的稀疏-密集分布，导致细节丢失。Z-Order Transformer 的核心洞察是：**将非结构化的三维高斯原语按其空间位置进行 Z-order 排序，生成一种既保留空间邻近性又适合 Transformer 处理的序列化表示**，从而摆脱对密集体素网格的依赖。

### 1. Z-order 序列化表示：从非结构化到空间紧凑序列

传统方法将高斯原语视为无序点集或规则体素，前者难以高效建模上下文，后者牺牲了空间精度。本工作引入空间填充曲线中的 **Z-order 曲线**，将每个高斯原语的三维坐标 $(x, y, z)$ 通过比特交叉映射为一维编码：

$$\mathbf{Z}(x,y,z) = \sum_{i=0}^{d-1} \left( x_i \cdot 2^{3i} + y_i \cdot 2^{3i+1} + z_i \cdot 2^{3i+2} \right)$$

按此编码排序后，空间邻近的高斯原语在序列中保持邻近——这一性质是后续分组注意力和池化操作有效性的数学基础。与体素网格相比，该序列化表示无需预设网格分辨率，自适应于场景的几何分布，从根本上消除了量化误差与固定网格的效率瓶颈。

### 2. 稀疏注意力机制：分组注意力 + Top-k 选择性注意力

序列化后，如何高效建模原语间的上下文依赖成为关键。全注意力（full attention）的计算复杂度随序列长度平方增长，在数万至数十万量级的高斯原语上不可行。本工作提出一种**双支路稀疏注意力**，由分组注意力和 top-k 选择性注意力组成，并通过可学习门控自适应融合：

$$\mathbf{F}_{\mathrm{gate}} = g_1(\mathbf{F}_{\mathrm{sorted}}) \odot \mathbf{Attn}_{\mathrm{grp}} + g_2(\mathbf{F}_{\mathrm{sorted}}) \odot \mathbf{Attn}_{\mathrm{sel}}$$

- **分组注意力**（Group Attention）：将 Z-order 序列按固定大小分块，对块内平均池化后的 $\hat{\mathbf{Q}}, \hat{\mathbf{K}}, \hat{\mathbf{V}}$ 做缩放点积注意力，捕获块级局部模式：
  $$\mathbf{Attn}_{\mathrm{grp}}(\hat{\mathbf{Q}}, \hat{\mathbf{K}}, \hat{\mathbf{V}}) = \mathrm{softmax}\left( \frac{\hat{\mathbf{Q}}\hat{\mathbf{K}}^{\top}}{\sqrt{d}} \right) \hat{\mathbf{V}}$$

- **Top-k 选择性注意力**（Top-k Selective Attention）：基于块重要性得分选择 top-k 个键值对，保留精细的跨块长程依赖：
  $$\mathbf{Attn}_{\mathrm{sel}} = \mathrm{softmax}\left( \frac{\mathbf{Q}\mathbf{K}_{\mathrm{sel}}^{\top}}{\sqrt{d}} \right) \mathbf{V}_{\mathrm{sel}}$$

- **门控融合**：$g_1, g_2$ 为可学习门控网络，根据输入特征 $\mathbf{F}_{\mathrm{sorted}}$ 动态调节两支路的贡献比例，使模型在局部平滑与长程细节之间自适应平衡。

消融实验证实，去除稀疏注意力（替换为全注意力或纯卷积）均导致 PSNR 显著下降（Table 5, Table S9），验证了分组与 top-k 注意力协同的必要性。

### 3. Z-order 池化：自适应图元压缩

传统方法通过减少像素级预测数量或体素聚合来压缩图元，前者丢失覆盖，后者受限于固定分辨率。本工作利用 Z-order 序列的空间局部性，提出**基于位偏移的分组池化**：将 Z-order 编码右移 $h$ 位（$\mathbf{Z} = \mathbf{Z} \gg h$），等价于在三维空间中按 $2^h$ 倍粗粒度合并相邻原语的特征。该操作在保持空间结构的前提下，自适应地抑制冗余图元——密集区域自然聚合，稀疏区域保留独立表示。

实验表明，使用两层 Z-order 块（$h=2$）在压缩率与渲染质量之间达到最佳平衡，高斯原语数量相比逐像素方法减少约 3 倍，同时 PSNR 显著提升（Table 4）。进一步增加块数量虽能继续压缩图元，但会导致渲染退化（Figure 7），揭示了压缩-质量权衡的当前边界。

**总结**：三项创新形成因果闭环——Z-order 序列化提供空间局部性保证，使分组注意力能高效捕获局部模式；top-k 注意力补偿了分组带来的长程信息损失；Z-order 池化则利用同一空间局部性实现无损结构压缩。三者共同支撑了“单次前馈、少图元、高质量”的核心目标。



Z-Order Transformer 的整体 pipeline 以多视图图像为输入，经 Transformer 编码器与深度头提取逐像素几何先验，再通过核心的 ZFormer 模块将非结构化的像素级高斯原语转化为空间紧凑的 Z-order 序列表示，最后由高斯头预测多层级高斯参数并渲染新视图。

**输入到几何先验**：给定 $N$ 个视图的输入图像 $\mathbf{I} = \{\mathbf{I}_i\}_{i=1}^N$，首先采用结构遵循 **DINOv2-Small** 的 Transformer 编码器将每幅图像切分为 token 序列 $\mathbf{t} \in \mathbb{R}^{N \times l \times d}$，并提取全局特征。随后，一个基于 **DPT** 的深度头作用于这些 token，预测各视图的深度图；深度图结合相机参数反投影为三维点云，同时深度头还输出几何特征（Figure 3）。

**ZFormer 块的核心转化**：ZFormer 块是 pipeline 的关键模块（Figure 4），其执行三个有序操作：
1. **Z-order 序列化**：将三维点坐标 $(x,y,z)$ 按比特交叉编码为一维 Z-order 码 $\mathbf{Z}(x,y,z) = \sum_{i=0}^{d-1} \left( x_i \cdot 2^{3i} + y_i \cdot 2^{3i+1} + z_i \cdot 2^{3i+2} \right)$，据此对所有高斯原语排序，形成保持空间局部性的紧凑 2D 序列。
2. **稀疏注意力**：对序列化表示施加分组注意力（捕获局部块级模式）与 top-k 选择性注意力（基于块重要性得分选择关键块），并通过可学习门控网络自适应融合两者输出，避免全注意力的高计算成本。
3. **Z-order 池化**：通过位偏移操作 $\mathbf{Z} = \mathbf{Z} \gg h$ 对序列进行分组聚合，逐步压缩高斯原语数量。

**多层级高斯预测与渲染**：框架堆叠两个 ZFormer 块（$L_1$ 和 $L_2$），分别输出不同压缩程度的表示 $\mathbf{R}_{L1}$ 和 $\mathbf{R}_{L2}$。高斯头是一个两层 MLP 网络 $\mathcal{F}_{\text{head}}$，从各级表示预测完整的高斯参数——均值偏移、尺度、旋转四元数、不透明度以及球谐系数——生成多层级高斯原语 $\{G_{L1}, G_{L2}\}$。渲染时，各级高斯分别通过可微光栅化器生成图像，并与真值计算联合损失。

**训练与推理**：训练损失由深度蒸馏损失 $\mathcal{L}_{\text{depth}}$（预测深度与预训练深度估计器输出的 L1 距离）和颜色重建损失 $\mathcal{L}_{\text{color}}$（各级渲染图像与真值的 MSE + LPIPS 联合损失）组成。推理阶段，采用基于 Z-order 最大覆盖的贪心视角选择算法，在显著减少所需视图数量的同时保持渲染质量。整个前馈过程无需逐场景优化，推理速度较优化式方法（如 3DGS）快约 1000 倍。

### 补充图表

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/003_Figure_3.jpg]]
*Figure 3: Framework. Given multi-view images, our method first utilizes a transformer encoder and a depth head to generate depth maps, which are then projected into a 3D point map based on the camera. Next, global features are extracted from the transformer encoder, and geometry features are derived from the depth head. These features, along with the pixel color and point map, are processed through our ZFormer blocks to generate Z-order-based Gaussian representations. Finally, the Gaussian representations are passed to the Gaussian head, which generates multi-level GS for further rendering*



### 3.1 前馈高斯泼溅的形式化

给定 $N$ 个视角的输入图像 $\{\mathbf{I}\}_{i=1}^{N}$，前馈高斯泼溅的目标是直接预测一组3D高斯原语 $\{G_k\}_{k=1}^{K}$，每个原语由均值 $\mu_k$、协方差 $\sigma_k$、旋转 $r_k$、尺度 $s_k$ 和颜色 $c_k$ 参数化：

$$\{ G_k : (\mu_k, \sigma_k, r_k, s_k, c_k) \}_{k=1}^{K} = \mathcal{F}(\{\mathbf{I}\}_{i=1}^{N})$$

其中 $\mathcal{F}$ 为待学习的神经网络。现有前馈方法的瓶颈在于：逐像素生成导致图元数量爆炸（每个像素一个高斯），而体素化方法引入量化误差且固定网格效率低下。本文的核心思路是将非结构化的高斯原语通过Z-order曲线组织成空间紧凑的序列化表示，从而在保持细节的同时大幅压缩图元。

### 3.2 Z-order序列化：从三维点到一维紧凑序列

Z-order序列化是整个方法的基础变换。给定三维坐标 $(x, y, z)$，首先将其展开为 $d$ 位二进制表示：

$$x = \sum_{i=0}^{d-1} x_i 2^i, \quad y = \sum_{i=0}^{d-1} y_i 2^i, \quad z = \sum_{i=0}^{d-1} z_i 2^i$$

随后通过比特交叉（bit-interleaving）将三个维度的二进制位交织为一维Z-order编码：

$$\mathbf{Z}(x,y,z) = \sum_{i=0}^{d-1} \left( x_i \cdot 2^{3i} + y_i \cdot 2^{3i+1} + z_i \cdot 2^{3i+2} \right)$$

该编码的核心性质是：三维空间中邻近的点，其Z-order编码在数值上也相近，从而将空间局部性保持在线性序列中。对所有高斯原语按Z-order编码排序后，非结构化的3D点云被转化为一个紧凑的2D序列（序列长度 × 特征维度），消除了对密集体素网格的依赖，显著降低了计算和内存开销。

### 3.3 ZFormer Block：稀疏注意力与自适应池化

ZFormer Block是方法的核心计算单元，其架构如图4所示，由三个关键子模块级联构成。

**分组注意力（Group Attention）**。将Z-order排序后的序列按固定大小划分为 $G$ 个块，对每个块内的查询、键、值进行平均池化得到 $\hat{\mathbf{Q}}, \hat{\mathbf{K}}, \hat{\mathbf{V}}$，然后执行缩放点积注意力：

$$\mathbf{Attn}_{\mathrm{grp}}(\hat{\mathbf{Q}}, \hat{\mathbf{K}}, \hat{\mathbf{V}}) = \mathrm{softmax}\left( \frac{\hat{\mathbf{Q}}\hat{\mathbf{K}}^{\top}}{\sqrt{d}} \right) \hat{\mathbf{V}}$$

该操作在块级别捕获局部空间模式，计算复杂度为 $O(G^2 d)$，远低于全注意力的 $O(L^2 d)$（$L$ 为序列总长度）。

**Top-k选择性注意力（Top-k Selective Attention）**。分组注意力虽高效，但池化操作丢失了块内细粒度信息。为此，引入基于块重要性得分的top-k选择机制：首先计算每个块的重要性分数，选择得分最高的 $k$ 个块的键 $\mathbf{K}_{\mathrm{sel}}$ 和值 $\mathbf{V}_{\mathrm{sel}}$，然后与完整查询 $\mathbf{Q}$ 计算注意力：

$$\mathbf{Attn}_{\mathrm{sel}} = \mathrm{softmax}\left( \frac{\mathbf{Q}\mathbf{K}_{\mathrm{sel}}^{\top}}{\sqrt{d}} \right) \mathbf{V}_{\mathrm{sel}}$$

该操作以 $O(L \cdot k \cdot d)$ 的复杂度保留了关键块的精细信息，$k$ 的选择在计算效率与信息保真度之间取得平衡。

**门控融合（Gated Fusion）**。两种注意力输出通过可学习的门控网络自适应融合：

$$\mathbf{F}_{\mathrm{gate}} = g_1(\mathbf{F}_{\mathrm{sorted}}) \odot \mathbf{Attn}_{\mathrm{grp}} + g_2(\mathbf{F}_{\mathrm{sorted}}) \odot \mathbf{Attn}_{\mathrm{sel}}$$

其中 $g_1, g_2$ 是以排序后特征 $\mathbf{F}_{\mathrm{sorted}}$ 为输入的小型MLP，输出逐元素门控权重。该设计使网络能根据上下文动态调节局部聚合与长程选择性关注的比重。

**Z-order池化（Z-order Pooling）**。在注意力操作后，通过位偏移实现自适应下采样：将Z-order编码右移 $h$ 位（$\mathbf{Z} = \mathbf{Z} \gg h$），空间上邻近的点被映射到相同的低分辨率编码，随后对这些点进行特征聚合。该方法利用Z-order的局部保持性质，在不引入额外参数的情况下压缩图元数量。论文中设置池化深度 $h=2$。

### 3.4 高斯参数预测

经过一个或多个ZFormer Block处理后，得到不同压缩层级的表示 $\mathbf{R}_{L1}, \mathbf{R}_{L2}$。高斯头 $\mathcal{F}_{\mathrm{head}}$ 为一个两层MLP，从这些表示中预测所有高斯参数：

$$G_{L1}, G_{L2} = \mathcal{F}_{\mathrm{head}}(\mathbf{R}_{L1}), \mathcal{F}_{\mathrm{head}}(\mathbf{R}_{L2})$$

多层级输出的设计使得网络能同时生成不同粒度的3D高斯，在训练时对各层均施加渲染损失（见式12），从而在不同压缩率下均保持渲染质量。

### 3.5 训练损失函数

训练使用深度蒸馏损失与颜色重建损失的联合优化。

**深度蒸馏损失**：将深度头预测的深度图与预训练深度估计器（如Depth Anything v2）的输出进行L1对齐：

$$\mathcal{L}_{\mathrm{depth}} = \left| \mathcal{F}_{\mathrm{depth}}(\mathbf{I}) - \hat{\mathcal{F}}_{\mathrm{depth}}(\mathbf{I}) \right|$$

该损失使模型继承大规模预训练深度先验，同时通过联合训练允许对不准确的深度估计进行补偿（消融实验证实固定深度估计会导致局部细节丢失）。

**颜色重建损失**：对各层级高斯渲染图像与真值之间同时施加MSE和LPIPS损失：

$$\mathcal{L}_{\mathrm{color}} = \sum_{i=1}^{M} \left[ \mathbf{MSE}( \mathcal{R}(G_{Li}, \mathbf{c}), \mathbf{I}_{\mathrm{gt}} ) + \mathbf{LPIPS}( \mathcal{R}(G_{Li}, \mathbf{c}), \mathbf{I}_{\mathrm{gt}} ) \right]$$

其中 $\mathcal{R}$ 为可微高斯泼溅渲染器，$\mathbf{c}$ 为相机参数，$M$ 为层级数。多层级监督确保了从粗到细的渲染质量一致性。

### 补充图表

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/004_Figure_4.jpg]]
*Figure 4: ZFormer Block. The ZFormer block begins by serializing and ordering the 3D points, features, and pixel colors using Z-order. The serialized data is then passed through a sparse attention mechanism, including group attention, and top-K attention. After the attention steps, Z-order pooling is applied to further aggregate the features*

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/002_Figure_2.jpg]]
*Figure 2: Gaussian representations in feed-forward GS*



## 实验与关键发现

### 主要定量结果

**Z-Order Transformer** 在多个基准数据集和视图配置下均取得最优性能，同时显著降低了高斯原语数量与推理延迟。Table 1 汇总了在 RealEstate10K 和 DL3DV 两个数据集上，使用 2 至 12 个输入视图的定量对比。方法以单层 Z-order 块配置（Ours#L1）在所有指标上均超越现有前馈方法：

- **RealEstate10K（360×640，2 视图）**：PSNR 达到 26.43 dB，SSIM 0.873，LPIPS 0.147，比 DepthSplat 提升 0.40 dB，LPIPS 降低 0.011。
- **RealEstate10K（12 视图）**：PSNR 28.56 dB，SSIM 0.901，LPIPS 0.110，较 AnySplat 提升 1.62 dB，SSIM 提升 0.009，LPIPS 降低 0.012。
- **DL3DV（256×448，12 视图）**：PSNR 27.09 dB，SSIM 0.892，LPIPS 0.124，比 DepthSplat 提升 1.35 dB，SSIM 大幅提升 0.048。

Table 2 进一步展示了在可变视图输入（训练与推理均使用 2–12 视图）下的性能，Ours#L1 取得 PSNR 28.07 dB、SSIM 0.890、LPIPS 0.125，表明方法对视图数量变化具有鲁棒性。

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/007_Table_2.jpg]]
*Table 2: Comparison on Variable Input. We train and evaluate the performance across various view inputs (2 to 12 views)*

### 跨数据集泛化

Table 3 报告了跨数据集泛化评估：将在 RealEstate10K 和 DL3DV 上预训练的模型直接应用于 ACID 数据集。在 RealEstate10K → ACID 设置下，PSNR 达 27.56 dB，SSIM 0.853，LPIPS 0.172，比 DepthSplat 提升 1.51 dB，SSIM 提升 0.043。这表明 Z-order 序列化与稀疏注意力机制学到的表示具有较好的场景迁移能力。

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/011_Table_3.jpg]]
*Table 3: Cross-Dataset Evaluation. We assess the crossdataset generalization capability by testing the RealEstate10K and DL3DV pre-trained models on the ACID dataset*

### 效率与图元压缩

Table 4 比较了推理时间与高斯原语数量。在 360×640 分辨率下，2 视图推理仅需约 0.123 秒，12 视图约 0.5 秒，比优化式方法 3DGS 快约 1000 倍。高斯原语数量约为 1.7×10⁵，比 DepthSplat 减少约 2–3 倍。效率提升的核心在于：Z-order 序列化消除了密集体素网格的存储与计算开销，而 Z-order 池化通过位偏移分组（$Z = Z \gg h$）自适应地抑制冗余图元。

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/009_Table_4.jpg]]
*Table 4: Comparison of Runtime and the Number of Gaussian Primitives. Values are reported in milliseconds (ms) for 2 and 12 views, with a resolution of 360×640. #GS denotes the number of Gaussian primitives (×105)*

### 消融实验

**Table 5** 系统消融了各核心组件（RealEstate10K，2 视图设置）：

- **移除 ZFormer（替换为卷积）**：PSNR 从 26.43 dB 骤降至 24.86 dB，降幅达 1.57 dB，证实 Z-order 序列化与注意力机制是方法的核心贡献。
- **去除稀疏注意力（使用全注意力）**：性能同样显著下降，说明分组注意力与 top-k 选择性注意力的门控融合（Eq. 9）在建模局部与长程依赖的同时有效控制了计算复杂度。Table S9 进一步拆分了分组注意力和 top-k 注意力的各自贡献，两者共同作用才能达到最优性能。
- **不固定深度估计（Ours-Fix-Depth）**：联合训练深度头与高斯头比固定预训练深度更优，Figure 6 显示固定深度会导致局部细节模糊，证实深度先验的不准确性需要通过端到端优化来补偿。
- **SH 参数初始化**：用输入像素颜色初始化球谐系数有助于训练稳定性和最终收敛质量（Table 5: Ours w/o SH）。

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/013_Table_5.jpg]]
*Table 5: Ablation Study. We have conducted ablations on different components of our method*

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/008_Figure_6.jpg]]
*Figure 6: Visual Ablation Study. Results of ablations on different components of our method*

**Table 6 与 Table S7** 消融了视图选择策略。在 16 个视图中，Z-order 最大覆盖贪心选择（ZS.16）取得 PSNR 28.73 dB，显著优于随机选择（RS.16，27.97 dB），且接近全视图（NA.32，29.01 dB）。这验证了 Z-order 编码的空间覆盖信息能有效指导稠密视图的稀疏化。

**Figure 7** 消融了 Z-order 块数量。使用两个块在压缩率与渲染质量之间取得最佳平衡；进一步增加块数虽能继续压缩高斯原语数量，但会导致渲染退化，表明过度池化会丢失必要的空间细节。

### 可视化分析

Figure 5 展示了新视图合成的可视化对比。Z-Order Transformer 在锐利边缘和复杂纹理区域（如家具轮廓、文字标识）的保真度明显优于 DepthSplat 和 AnySplat，这与 LPIPS 指标的显著降低一致，归因于稀疏注意力机制对局部与关键块信息的有效聚合。

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/006_Figure_5.jpg]]
*Figure 5: Visual Comparison. Our method achieves better performance in capturing sharp edges and intricate details*

### 失败模式与局限

尽管方法在常规分辨率下表现优异，论文明确指出以下局限：

1. **极高分辨率场景**（>1K）：模型复杂度与内存限制可能导致细粒度细节捕捉不足，需要进一步验证。
2. **Z-order 块数量增加**：虽然能进一步压缩高斯原语，但会带来渲染质量的明显退化，当前未找到有效缓解方案。
3. **复杂场景泛化**：在非朗伯表面、动态场景或大规模室外环境下的适应性尚未验证，属于开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/005_Table_1.jpg]]
*Table 1: Quantitative Comparison with Varying Numbers of Views. We highlight the best results in red and the second-best in yellow*

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/012_Figure_7.jpg]]
*Figure 7: Ablation Study on Layer Selection. We use two Z-order blocks in our framework to prevent degradation while achieving a lower number of GS primitives*

![[assets/figures/papers/paper_list_l2096_https_arxiv_org_abs_2605_13465/figures/010_Table_6.jpg]]
*Table 6: Ablation Study with Different Selection Strategies. NA. indicates that all views will be used during inference, RS. refers to random selection, while ZS. denotes our Z-order-based view selection method. The input resolution is 360×640*



## 定位与知识库关联

### 与前馈高斯泼溅方法的关系

本文的**Z-Order Transformer**处于前馈（feed-forward）3D高斯泼溅（3DGS）重建这一研究脉络中，其核心贡献在于对高斯原语的表示形式和聚合机制进行了根本性重构。现有前馈方法可大致分为两类：

**像素级方法**（如 **DepthSplat**）将每个输入像素直接映射为一个高斯原语，导致原语数量随分辨率线性增长，产生大量冗余图元。**体素级方法**（如 **AnySplat**）则通过将点云量化为密集体素网格来聚合信息，但固定分辨率的体素网格引入了量化误差，且均匀网格无法自适应场景的稀疏性，效率低下。

Z-Order Transformer的关键突破在于**用Z-order序列化替代了像素级或体素级的中间表示**。通过将三维点按其Z-order编码排序，该方法将非结构化的高斯原语组织成一个紧凑的二维序列，同时保留了空间局部性——这是后续稀疏注意力机制得以高效运作的前提。这一设计消除了对密集体素网格的依赖，从根本上改变了前馈3DGS的表示瓶颈。

与基于优化的方法（如 **3DGS** 和 **MipSplatting**）相比，Z-Order Transformer属于前馈范式，无需逐场景迭代优化，推理速度提升约三个数量级（约1000倍），同时将高斯原语数量压缩了2–3倍。

### 方法谱系中的关键设计选择

**注意力机制的演进**：传统前馈方法依赖卷积或全注意力进行特征聚合。卷积的感受野受限于局部邻域，难以建模长程依赖；全注意力虽能捕捉全局上下文，但其 $O(N^2)$ 的计算复杂度在高分辨率场景下不可承受。本文提出的**分组注意力+top-k选择性注意力**的门控融合机制，是一种介于局部和全局之间的稀疏注意力方案——分组注意力在Z-order序列的局部块内建模空间邻近性，top-k注意力则基于块重要性得分选择关键块进行跨块交互，两者通过可学习门控自适应融合。这一设计在控制计算成本的同时，有效利用了Z-order序列的局部性先验。

**图元压缩策略**：不同于像素级方法的“一对一”映射或体素方法的均匀聚合，Z-Order Transformer采用**基于位偏移的Z-order池化**（$Z = Z \gg h$）进行层次化压缩。这种池化方式天然地与Z-order序列的空间局部性对齐——相邻的Z-order编码在池化后仍保持相邻，从而在压缩过程中保留了空间结构信息。实验表明，使用两个Z-order块在压缩率与渲染质量之间取得最佳平衡，更多块会导致渲染退化。

**多视图选择**：提出的**基于Z-order最大覆盖的贪心视角选择算法**，利用Z-order编码的空间覆盖特性进行视点筛选，在显著减少视点数量时优于随机选择，且接近全视点性能。

### 适用边界与局限

尽管在RealEstate10K和DL3DV等室内外静态场景基准上取得了显著提升，该方法存在以下适用边界：

1. **分辨率限制**：当前框架在极高分辨率（>1K）数据集上，模型复杂度与内存限制可能导致细粒度细节捕捉不足，这是Transformer架构在处理长序列时的固有瓶颈。
2. **压缩-质量权衡**：增加Z-order块数量虽能进一步压缩高斯原语，但会带来渲染质量的明显退化，表明当前层次化压缩策略存在上限。
3. **场景泛化性未验证**：当前评估集中在静态、朗伯场景，在更复杂的非朗伯表面、动态场景或大规模室外场景下的泛化能力尚未得到验证。跨数据集实验（RealEstate10K→ACID）虽显示了初步的泛化能力，但测试域仍属相似类型。

### 开放问题

1. **深层压缩与质量保持**：如何在使用更多Z-order块实现更高压缩率的同时，保持甚至提升渲染质量？这可能需要更精细的层次化特征传播机制或渐进式重建策略。
2. **高分辨率细节保持**：层次化或多尺度特征表示能否在不显著增加计算量的前提下，提升对高分辨率细节的保持？混合神经渲染（如NeRF-based模块）可能是一个值得探索的方向。
3. **动态与大规模场景适应性**：Z-order序列化与稀疏注意力机制在非刚体动态场景或大规模室外场景中的适应性如何？Z-order编码本身对空间变换敏感，动态场景可能需要时序一致的序列化策略。
4. **跨域泛化机制**：当前跨数据集泛化虽有效果，但其泛化能力的来源（是深度先验的鲁棒性还是Z-order表示的结构不变性）尚不明确，需要更系统的分析。



## 原文 PDF

![[paperPDFs/CVPR_2026/Z_Order_Transformer_for_Feed_Forward_Gaussian_Splatting.pdf]]
