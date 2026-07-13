---
title: "Variable Bitrate Neural Fields"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Variable_Bitrate_Neural_Fields.pdf
code_link: https://github.com/nv-tlabs/vqad
project_link: https://research.nvidia.com/labs/toronto-ai/vqad/
aliases:
- VAVQAD
- VBNF
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将每个网格点的完整特征向量替换为一个低比特整数索引和一个共享码本（codebook），并通过向量量化自解码器（VQ-AD）端到端地学习该压缩表示，从而在维持视觉质量同时大幅降低存储。"
primary_logic: "利用自解码器框架将离散信号压缩与神经场训练统一起来：通过可微分的软化索引（softmax + 直通估计器）使压缩表示能针对下游任务（如新视角合成）进行端到端优化，避免了传统后处理量化带来的质量损失，并天然支持多分辨率渐进式流式传输。"
claims:
- "在 NGLOD-NeRF 基线上，VQ-AD 将特征网格存储从约 20 MB 压缩至 0.33 MB（4bw）或 0.49 MB（6bw），PSNR 仅下降约 2 dB，SSIM 仍超过 0.94"
- "端到端学习式 VQ 相比 k-means 后处理 VQ 在视觉上去除了明显的颜色褪变"
- "学习到的索引码本优于静态随机索引（哈希表），能在相同压缩率下获得更高 PSNR"
- "多分辨率八叉树表示支持渐进式流式传输，仅需约 10 kB 即可显示粗糙 LOD"
---

# Variable Bitrate Neural Fields

> [!tip] 核心洞察
> 利用自解码器框架将离散信号压缩与神经场训练统一起来：通过可微分的软化索引（softmax + 直通估计器）使压缩表示能针对下游任务（如新视角合成）进行端到端优化，避免了传统后处理量化带来的质量损失，并天然支持多分辨率渐进式流式传输。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 可变比特率神经场 |
| 英文题名 | Variable Bitrate Neural Fields |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2206.07707) · [GitHub](https://github.com/nv-tlabs/vqad) · [Project](https://research.nvidia.com/labs/toronto-ai/vqad/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | VQ-AD (Vector-Quantized Auto-Decoder) |
| Dataset | RTMV (Night Fury) |

> [!tip] 效果简介
> - RTMV (Night Fury) 上，PSNR 为 30.09 (4bw)，对比 32.72 (NGLOD-NeRF)，变化 -2.63 dB。
> - RTMV (Night Fury) 上，SSIM 为 0.9482 (4bw)，对比 0.9700 (NGLOD-NeRF)，变化 -0.0218。
> - RTMV (Night Fury) 上，Storage 为 0.33 MB (4bw, 61.3x compression)，对比 ~20 MB (NGLOD-NeRF)，变化 61.3x smaller。

## 概要

神经场（neural fields）在高质量三维信号重建与新视角合成中展现出强大能力，但其主流实现——基于特征网格（feature grid）的方法——面临一个根本瓶颈：每个网格顶点需存储完整的浮点特征向量（例如16维×float32 = 64 bytes/顶点），在包含数百万顶点的场景中，存储需求可达数十MB，严重制约了内存和带宽受限的图形应用中的实用性。

针对这一问题，本文提出了**向量量化自解码器（VQ-AD, Vector-Quantized Auto-Decoder）**，核心思路是将每个顶点的完整特征向量替换为一个低比特整数索引和一个共享码本（codebook），并通过端到端训练联合优化压缩表示与下游任务目标。该方法的关键洞察在于：利用自解码器框架将离散信号压缩与神经场训练统一起来，通过可微分的软化索引（softmax + 直通估计器）使压缩表示能针对渲染质量进行端到端优化，避免了传统后处理量化（如k-means VQ）带来的质量损失，并天然支持多分辨率渐进式流式传输。

在方法谱系上，VQ-AD 以 **NGLOD-NeRF**（Takikawa et al., CVPR 2021）的稀疏八叉树特征网格为基线架构，将每顶点存储从浮点特征向量替换为b-bit索引+尺寸为2^b×k的码本，训练时通过软化矩阵C∈R^{m×2^b}和softmax实现可微索引。相比 **NeRF**（Mildenhall et al., ECCV 2020）和 **mip-NeRF**（Barron et al., ICCV 2021）等全局方法，VQ-AD继承了特征网格方法的高质量重建能力；相比 **Instant NGP**（Müller et al., 2022）的哈希索引方案，VQ-AD通过学习索引而非静态随机映射，在相同压缩率下获得更高PSNR（+2.94 dB, Table 3）；相比k-means后处理VQ和低秩近似（LRA），端到端学习显著减少了颜色褪变等视觉伪影（Fig. 4）。

主要实验结果（Table 2）表明：在RTMV（Night Fury）场景上，VQ-AD将NGLOD-NeRF约20 MB的特征网格压缩至0.33 MB（4-bit，61.3×压缩）或0.49 MB（6-bit，40.9×压缩），PSNR分别仅下降2.63 dB和1.96 dB，SSIM仍超过0.94。同时，多分辨率八叉树表示支持渐进式流式传输，仅需约10 kB即可显示粗糙细节层次（Fig. 2），而NeRF等全局方法需传输约2.5 MB才能开始绘制（Fig. 1）。

方法的局限性包括：训练时软化索引矩阵在6-bit位宽下导致峰值内存高达18 GB；压缩后的几何表示（SDF）会在法线方向引入可见伪影（Fig. 5）；未采用熵编码以保持流式传输兼容性。



### 神经场与特征网格的兴起

神经场（Neural Fields）已成为三维场景表示的核心范式。以 **NeRF**（Mildenhall et al., ECCV 2020）为代表的全局方法将整个场景编码进一个多层感知机（MLP）的权重中，通过可微体积渲染实现高质量的新视角合成。然而，这类方法的表达能力受限于 MLP 容量，且查询效率较低。

为突破这一瓶颈，**特征网格方法**（feature-grid methods）应运而生。其核心思路是在空间域中引入一个显式的、可优化的特征网格 $Z \in \mathbb{R}^{m \times k}$（其中 $m$ 为网格顶点数，$k$ 为每顶点特征维度），通过插值获取局部特征向量后馈入一个轻量 MLP 解码器。这种设计将场景的“记忆”从 MLP 权重中剥离，交由特征网格承担，从而显著提升了重建质量和训练速度。代表性工作包括 **NGLOD-NeRF**（Takikawa et al., CVPR 2021）和 **Plenoxels**（Yu et al., CVPR 2022），它们在多项基准上达到或超越了纯 MLP 方法的水平（见 Table 1）。

### 核心瓶颈：特征网格的存储爆炸

特征网格的性能提升并非没有代价。一个典型场景的特征网格可能包含数百万个顶点，每个顶点存储一个 $k$ 维浮点特征向量（如 $k=16$，半精度浮点）。以 NGLOD-NeRF 为例，其未压缩的特征网格存储量高达约 **20 MB**（约 15,207 kB，见 Fig. 2）。这一数字在内存和带宽受限的图形应用中——如移动端渲染、Web 端流式传输、AR/VR 设备——构成了严重的实用障碍。

更关键的是，这种存储开销与场景复杂度呈正相关，且无法通过简单的后处理压缩（如低秩近似或 k-means 量化）来有效削减而不引入明显的视觉退化。这构成了本文的核心问题：**如何在不牺牲视觉质量的前提下，将特征网格的存储需求压缩一至两个数量级？**

### 现有压缩方案的局限

针对特征网格的压缩，已有若干直观方案，但它们各自存在根本性缺陷：

- **低秩近似（Low-Rank Approximation, LRA）**：将特征矩阵 $Z$ 分解为两个小矩阵的乘积。然而，特征网格的行（顶点）和列（特征维度）之间缺乏天然的低秩结构，强制低秩分解会导致显著的 PSNR 下降（见 Table 2）。
- **后处理向量量化（k-means VQ, kmVQ）**：在训练完成后对特征向量进行 k-means 聚类，将每个顶点替换为聚类中心索引。这种方式与训练过程解耦，量化误差无法被下游任务（如可微渲染）感知和补偿，导致渲染结果出现明显的颜色褪变（见 Fig. 4）。
- **静态随机索引（哈希表）**：如 **Instant NGP**（Müller et al., 2022）使用哈希函数将顶点映射到固定码本中的条目。这种方法虽然简单，但哈希冲突不受任务目标约束，在相同压缩率下重建质量显著低于学习式索引（见 Table 3, Fig. 6）。

这些方法的共同缺陷在于：**压缩操作与神经场的端到端训练是分离的**。压缩被视为一个独立的后处理步骤，而非训练目标的一部分，因此无法利用可微渲染的梯度信号来引导压缩表示的学习。

### 本文动机与核心思路

本文的动机源于一个关键洞察：**将离散信号压缩与神经场训练统一到同一个自解码器框架中**。具体而言，我们提出 **VQ-AD（Vector-Quantized Auto-Decoder）**，将每个网格顶点的完整特征向量替换为一个低比特整数索引和一个共享的码本（codebook）$D \in \mathbb{R}^{2^b \times k}$。训练时，通过可微分的软化索引操作（softmax + 直通估计器）使整个压缩表示能够针对下游任务（如新视角合成）进行端到端优化；推理时，则直接使用硬索引进行高效查表。

这种设计带来了三重优势：
1. **端到端优化**：码本和索引的更新直接由渲染损失驱动，避免了后处理量化与任务目标之间的失配。
2. **天然的多分辨率支持**：利用稀疏八叉树组织索引，不同层级的细节层次（LOD）可独立传输和渲染，仅需约 **10 kB** 即可显示粗糙 LOD（见 Fig. 2）。
3. **渐进式流式传输**：数据可按广度优先顺序从粗到细流式传输，使接收端能根据可用带宽动态调整渲染质量（见 Fig. 1）。

在 NGLOD-NeRF 基线上，VQ-AD 将特征网格存储从约 20 MB 压缩至 **0.33 MB**（4-bit 索引，61.3 倍压缩），PSNR 仅下降约 2.6 dB，SSIM 仍超过 0.94；若使用 6-bit 索引，存储为 0.49 MB（40.9 倍压缩），PSNR 下降仅约 1.96 dB（见 Table 2）。这一结果首次证明了：**特征网格可以在保持实用视觉质量的同时，被压缩到适合流式传输的量级**。



## 核心方法与创新机理

VQ-AD 的核心创新在于将神经场的特征网格压缩问题转化为一个**端到端可学习的向量量化自解码器**框架。其关键洞察是：通过将每个网格顶点的完整浮点特征向量替换为一个低比特整数索引和一个共享码本，并利用可微分的软化索引机制，使压缩表示能够针对下游任务（如新视角合成）进行联合优化，从而在维持视觉质量的同时实现两个数量级的存储压缩。

### 关键改变槽位

VQ-AD 相对于未压缩特征网格基线（NGLOD-NeRF，Takikawa et al., CVPR 2021）引入了两个核心结构改变：

**1. 网格顶点存储内容：从浮点特征向量到整数索引+码本**

在基线方法中，每个网格顶点存储一个 $k$ 维浮点特征向量（如 $k=16$，每顶点 $16 \times 32$ 位 = 64 字节），整个特征网格的存储需求可达数百万个浮点数。VQ-AD 将其替换为一个 $b$ 比特的整数索引，该索引指向一个共享码本矩阵 $D \in \mathbb{R}^{2^b \times k}$。例如，当 $b=4$ 时，每顶点仅需 4 比特存储，码本仅包含 16 个 $k$ 维特征向量。这一替换在 RTMV 场景上实现了 61.3 倍压缩（从约 20 MB 降至 0.33 MB），PSNR 仅下降约 2.6 dB，SSIM 仍超过 0.94（Table 2）。

**2. 训练时索引操作：从直接优化到软化可微索引**

硬索引操作 $D[V]$ 是不可微的，无法通过梯度反向传播直接优化码本和索引。VQ-AD 在训练时引入一个软化矩阵 $C \in \mathbb{R}^{m \times 2^b}$，通过 softmax 函数 $\sigma(C)$ 生成软索引权重，再与整个码本相乘得到可微的加权特征向量。训练目标变为：

$$\underset{D, C, \theta}{\arg\min} \ \mathbb{E}_{x, y} \left\| \psi_{\theta}\left(x, \mathrm{interp}(x, \sigma(C) D)\right) - y \right\|$$

同时采用直通估计器（straight-through estimator）在反向传播时传递梯度。推理时则通过 argmax 从 $C$ 中提取硬索引，恢复为紧凑的整数表示。这一设计使得压缩表示能够针对渲染损失进行端到端优化，而非在训练后进行后处理量化。

### 为什么这构成了突破性创新

**瓶颈定位精准**：特征网格方法虽然重建质量优异，但其庞大的存储需求（数百万个浮点特征向量）严重制约了在内存和带宽受限的图形应用中的实用性。VQ-AD 直接针对这一存储瓶颈进行压缩，而非在渲染质量上妥协。

**端到端优化避免质量损失**：传统后处理压缩方法（如 k-means 向量量化，kmVQ）在训练完成后对特征网格进行独立聚类，导致明显的颜色褪变伪影（Fig. 4）。VQ-AD 将压缩融入训练过程，使码本和索引能够适应渲染任务的需求，在相同压缩率下显著提升了视觉质量。

**学习索引优于静态随机索引**：与基于哈希的静态随机索引方法（Müller et al., 2022, Instant NGP）相比，VQ-AD 通过学习索引实现了自适应碰撞解决，使得在更小码本尺寸下仍能获得更高重建质量。在近似压缩率下，4 比特学习索引（29.60 PSNR）显著优于 12 比特哈希索引（26.66 PSNR）（Table 3, Fig. 6）。

**天然支持渐进式流式传输**：由于压缩后的多分辨率八叉树在所有层级都存储了数据，VQ-AD 天然支持按广度优先顺序流式传输，仅需约 10 kB 数据即可显示粗糙细节层次（Fig. 2），实现了可变比特率的细节层次渲染。



VQ-AD 的核心思路是将特征网格的压缩问题转化为一个**端到端可学习的向量量化自解码器**。整个 pipeline 围绕一个关键替换展开：将每个网格顶点存储的完整浮点特征向量（例如 16 维 × float32 = 64 bytes/顶点）替换为一个低比特整数索引和一个共享的码本（codebook），从而将存储需求压缩两个数量级，同时保持可微渲染下的重建质量。

### 模块构成与数据流

系统由五个核心模块串联而成，形成“索引查找 → 特征插值 → MLP 解码 → 体积渲染 → 可微训练”的闭环：

1. **多分辨率稀疏八叉树 (Sparse Octree Grid)**  
   负责组织空间网格结构。八叉树的每个顶点存储一个 $b$-bit 整数索引（如 $b=4$ 或 $b=6$），而非完整的特征向量。多分辨率层级天然支持渐进式流式传输：从最粗糙的 LOD 开始，仅需约 10 kB 即可显示场景轮廓（Fig. 2），后续层级逐步细化。

2. **码本与索引查找 (Codebook & Index Lookup)**  
   这是压缩的核心机制。码本 $D \in \mathbb{R}^{2^b \times k}$ 包含 $2^b$ 个 $k$ 维特征向量。给定顶点索引 $V_i$，通过查表 $D[V_i]$ 直接取回对应的特征向量。推理时使用硬索引（hard indexing），存储代价从 $m \times k \times \text{float32}$ 降至 $m \times b\text{ bits} + 2^b \times k \times \text{float32}$。

3. **MLP 解码器 (MLP Decoder)**  
   接收插值后的局部特征向量与视线方向，映射为体积密度 $\sigma$ 和视角相关的颜色 $\mathbf{c}$。解码器结构与 NGLOD-NeRF（Takikawa et al., CVPR 2021）保持一致，保证压缩前后架构的可比性。

4. **可微体积渲染 (Volumetric Renderer)**  
   沿光线采样点累积密度和颜色，生成像素级 RGB 输出，与训练图像计算光度损失。此模块提供间接监督信号，驱动整个压缩表示的学习。

5. **软化索引训练模块 (Soft-Indexing Trainer)**  
   硬索引操作 $\text{interp}(x, D[V])$ 不可微，因此训练时引入软化矩阵 $C \in \mathbb{R}^{m \times 2^b}$，通过 softmax 生成软索引权重：
   $$\underset{D, C, \theta}{\arg\min} \; \mathbb{E}_{x, y} \left\| \psi_{\theta}\left(x, \mathrm{interp}\left(x, \sigma(C) D\right)\right) - y \right\|$$
   训练完成后通过 argmax 将 $C$ 转换为硬索引 $V$，用于推理。这一设计使得压缩表示能针对下游渲染任务进行端到端优化，避免了后处理量化（如 k-means VQ）带来的颜色褪变（Fig. 4）。

### 关键设计决策

- **自解码器框架**：不依赖编码器网络，而是直接在间接监督（可微渲染）下优化压缩系数 $V$ 和码本 $D$。这避免了“先训练后压缩”两阶段流程中的信息损失。
- **学习式索引 vs. 静态哈希**：与 Instant NGP（Müller et al., 2022）的随机哈希索引不同，VQ-AD 学习索引分配，允许自适应碰撞解决。在相近压缩率下，4-bit 学习索引的 PSNR 比 12-bit 哈希索引高约 3 dB（Table 3, Fig. 6）。
- **无熵编码设计**：所有报告结果均未使用熵编码，因为熵编码会破坏流式传输的渐进性。若采用 gzip 可额外压缩 4–7%，但这是以牺牲流式能力为代价的（Section 8.2）。

### 训练与推理的分离

训练时使用软化索引（softmax + 直通估计器）保证梯度流动，但软化矩阵 $C$ 的尺寸为 $m \times 2^b$，在 $b=6$ 时导致训练峰值内存高达 18 GB，限制了更高比特宽度的实验。推理时切换为硬索引，速度与未压缩基线相当（约 15 FPS），且可通过缓存优化进一步提升。

### 补充图表

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2206_07707/figures/008_Figure_5.jpg]]
*Figure 5: Ours (72 kB) Fig. 5. Compressing geometry. We show how VQ-AD can compress signed distance functions as in NGLOD. Our method introduces visible artifacts in the normals, however it does result in a significant bitrate reduction. We also compare against a quantized Draco mesh which has similar bitrates when entropy coded (2 MB as the decompressed binary .ply mesh)*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2206_07707/figures/001_Figure_1.jpg]]
*Figure 1: Compressed streaming level of detail. Using our vector-quantized auto-decoder (VQ-AD) method, we compactly encode a 3D signal in a hierarchical representation which can be used for progressive streaming and level of detail (LOD). Two example neural radiance fields are shown after streaming from 5 to 8 levels of their underlying octrees. The sizes shown are the total bytes streamed; that is, the finer LODs include the cost of the coarser ones. Prior work such as NeRF [Mildenhall et al. 2020] requires ≈ 2.5 MB to be transferred before anything can be drawn*



### 问题形式化：将压缩纳入特征网格学习

VQ-AD 的核心目标是将神经场的特征网格从“存储完整浮点向量”转变为“存储低比特索引 + 共享码本”，并在端到端训练中联合优化压缩表示与下游任务质量。

设未压缩的特征网格为矩阵 $Z \in \mathbb{R}^{m \times k}$，其中 $m$ 为网格顶点数，$k$ 为每顶点特征向量维度。标准特征网格方法（如 NGLOD-NeRF, Takikawa et al., CVPR 2021）直接优化 $Z$ 和 MLP 解码器参数 $\theta$：

$$
\underset{Z, \theta}{\arg\min} \; \mathbb{E}_{\boldsymbol{x}, \boldsymbol{y}} \left\| \psi_{\theta}\big(\boldsymbol{x}, \mathrm{interp}(\boldsymbol{x}, Z)\big) - \boldsymbol{y} \right\|
$$

其中 $\mathrm{interp}(\boldsymbol{x}, Z)$ 表示在查询点 $\boldsymbol{x}$ 处对网格 $Z$ 进行多分辨率插值，$\psi_\theta$ 为 MLP 解码器，$\boldsymbol{y}$ 为监督信号（如像素颜色）。

VQ-AD 的压缩方案将 $Z$ 替换为一个整数索引向量 $V \in \{0, \dots, 2^b - 1\}^m$ 和一个码本矩阵 $D \in \mathbb{R}^{2^b \times k}$，其中 $b$ 为每顶点的比特位宽。推理时，通过硬索引 $D[V]$ 从码本中取回特征向量，优化目标变为：

$$
\underset{D, V, \theta}{\arg\min} \; \mathbb{E}_{\boldsymbol{x}, \boldsymbol{y}} \left\| \psi_{\theta}\big(\boldsymbol{x}, \mathrm{interp}(\boldsymbol{x}, D[V])\big) - \boldsymbol{y} \right\|
$$

该目标不可微，因为 $V$ 是离散整数。为此，VQ-AD 引入软化索引机制。

### 软化索引：可微训练的核心模块

训练时，将每个顶点的离散索引替换为一个软化矩阵 $C \in \mathbb{R}^{m \times 2^b}$，通过 softmax 函数 $\sigma(\cdot)$ 生成软分配权重，再与整个码本相乘得到“软特征向量”：

$$
\underset{D, C, \theta}{\arg\min} \; \mathbb{E}_{\boldsymbol{x}, \boldsymbol{y}} \left\| \psi_{\theta}\big(\boldsymbol{x}, \mathrm{interp}(\boldsymbol{x}, \sigma(C) D)\big) - \boldsymbol{y} \right\|
$$

其中 $\sigma(C)$ 在每一行上计算 softmax，输出一个 $m \times 2^b$ 的软分配矩阵。该操作完全可微，允许梯度通过码本 $D$ 和软化矩阵 $C$ 反向传播。

推理时，通过 $\arg\max$ 将软索引转换为硬索引：$V = \arg\max(C)$，恢复为图 3(b) 所示的紧凑表示。训练过程中使用直通估计器（straight-through estimator, Bengio et al., 2013）：前向传播使用 $\arg\max$ 的硬索引结果，反向传播时梯度直接传递给 softmax 输出，从而弥合训练与推理的分布差异。

### 自解码器框架：无编码器的压缩学习

VQ-AD 采用自解码器（auto-decoder, Park et al., 2019）框架，不构建显式编码器，而是将压缩系数（索引 $V$ 或软化矩阵 $C$）视为可优化变量，通过解码器（MLP $\psi_\theta$ 和可微渲染器）的间接监督进行学习。其一般形式为：

$$
\underset{\mathbf{v}_x, \gamma}{\arg\min} \left\| F\big(f_{\gamma}^{-1}(\mathbf{v}_x)\big) - F(\mathbf{u}_x) \right\|
$$

其中 $\mathbf{v}_x$ 为压缩系数，$f_{\gamma}^{-1}$ 为解码器，$F$ 为前向映射（如体积渲染），$\mathbf{u}_x$ 为原始信号。在 VQ-AD 中，该框架将离散信号压缩与神经场训练统一：码本和索引直接针对渲染损失进行优化，避免了传统后处理量化（如 k-means VQ）带来的质量损失。

### 多分辨率八叉树与渐进式流式传输

压缩表示被组织在稀疏八叉树中，所有细节层次的数据同时存储。查询点 $\boldsymbol{x}$ 的特征通过多分辨率插值获得。由于码本和索引天然支持不同 LOD 的独立解码，该结构支持渐进式流式传输：仅需传输约 10 kB 的粗糙层级数据即可显示初始结果（Fig. 2），随后逐步加载更精细层级。



## 实验与关键发现

### 核心结果：压缩率与重建质量的权衡

VQ-AD 在 RTMV 场景（Night Fury）上以 **NGLOD-NeRF**（Takikawa et al., CVPR 2021）为未压缩基线，展示了极致的存储压缩能力。基线特征网格占用约 20 MB，PSNR 达 32.72 dB，SSIM 为 0.9700（Table 1）。VQ-AD 在 4 比特位宽（4bw）下将存储压缩至 **0.33 MB（61.3× 压缩）**，PSNR 为 30.09 dB（下降 2.63 dB），SSIM 仍保持 0.9482；在 6 比特位宽（6bw）下存储为 **0.49 MB（40.9× 压缩）**，PSNR 为 30.76 dB（下降 1.96 dB），SSIM 为 0.9567（Table 2）。这表明端到端学习式向量量化在牺牲约 2 dB PSNR 的代价下，实现了两个数量级的存储缩减。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2206_07707/figures/005_Table_1.jpg]]
*Table 1: Baseline References. This table shows the baseline feature-grid method (NGLOD-NeRF) in comparison to NeRF and mip-NeRF which are state-of-the-art global-methods, and Plenoxels which is also a feature-grid method. We see from the results that NGLOD-NeRF is a strong baseline with similar quality to both. All floats are half precision*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2206_07707/figures/006_Table_2.jpg]]
*Table 2: LRA, VQ vs loss-aware VQ (ours). This table shows the comparison between low-rank approximation (LRA), vector quantization (kmVQ) and learned vector quantization (ours) at different truncation sizes (for LRA) and different quantization bitwidths (for kmVQ and ours). We see that across all metrics we see a significant improvement by learning vector quantization. The bitrate is data dependent, so we report average bitrate*

### 消融实验：端到端学习 vs. 后处理压缩

**与 k-means 后处理 VQ（kmVQ）对比。** 在相同码本条目数下，训练后对特征网格施加 k-means 向量量化的方案会导致明显的颜色褪变（Fig. 4），而 VQ-AD 的端到端学习式 VQ 能保持视觉质量。定量上，kmVQ 在相近比特率下的 PSNR 和 SSIM 均显著低于 VQ-AD（Table 2），验证了将量化过程纳入训练循环的必要性——压缩表示通过可微渲染的梯度直接针对下游任务优化，避免了后处理量化与任务目标之间的失配。

**与低秩近似（LRA）对比。** LRA 通过对特征网格矩阵进行截断 SVD 实现压缩，但在相同或更大的存储开销下，其 PSNR 和 SSIM 均不及 VQ-AD（Table 2）。这说明向量量化在特征网格压缩场景中比线性低秩分解更具表达能力。

**学习索引 vs. 静态随机索引。** 与基于哈希的静态随机索引方案（如 Instant NGP 中的哈希表，Müller et al., 2022）相比，VQ-AD 的学习索引展现出显著优势。在近似压缩率下，4 比特学习索引（332 kB）达到 29.60 dB PSNR，而 12 比特哈希索引（536 kB）仅获得 26.66 dB PSNR（Table 3）。视觉上，学习索引重建结果的噪声明显更少（Fig. 6）。其机理在于：学习索引能够自适应地解决“碰撞”问题——多个网格顶点可通过优化分配到不同码本条目，从而在更小的码本尺寸下实现更高的表示精度。

### 渐进式流式传输与细节层次

VQ-AD 的多分辨率八叉树结构天然支持渐进式流式传输。如 Fig. 2 所示，仅需接收约 **10 kB** 的数据即可显示粗糙的细节层次（LOD），随后可逐层细化。Fig. 1 展示了从 5 层到 8 层八叉树的流式加载过程，总传输字节数随 LOD 提升而累积。相比之下，传统 NeRF（Mildenhall et al., ECCV 2020）需要传输约 2.5 MB 才能开始渲染任何内容。Fig. 7 进一步对比了 VQ-AD 与 mip-NeRF（Barron et al., ICCV 2021）的细节层次行为：mip-NeRF 虽然能产生滤波结果，但其比特率是恒定的；VQ-AD 则同时实现了滤波与可变比特率，比特率可随 LOD 动态缩放。率失真曲线（Fig. 8）直观展示了这一优势——VQ-AD 的曲线在比特率轴上可水平移动，而单比特率架构仅为一个固定点。

### 几何压缩的局限

VQ-AD 在符号距离函数（SDF）压缩上也能显著降低比特率（Fig. 5），例如将 NGLOD 的 TSDF 表示压缩至约 72 kB。然而，压缩后的几何在法线方向会引入可见伪影，表现为表面法线的不连续或噪声。与量化 Draco 网格的对比显示，后者在熵编码后具有相似的比特率（解压后为 2 MB 的 .ply 文件），但 VQ-AD 的法线质量仍有差距。这表明当前方法在几何信号的保真度上存在改进空间。

### 公平性与实验设置说明

所有对比实验均采用相同的 NGLOD-NeRF 架构和超参数，确保压缩方案是唯一变量。报告结果均未使用熵编码——若采用 gzip 可额外压缩 4-7%，但熵编码会破坏流式传输能力（Section 8.2）。训练时软化索引矩阵 $C \in \mathbb{R}^{m \times 2^b}$ 的尺寸随比特位宽指数增长，6 比特时训练峰值内存高达 18 GB（Section 8.1.2），这限制了更高位宽（如 8-bit）的实验。压缩模型的推理速度与未压缩基线相当（约 15 FPS），预估可通过缓存优化进一步提升（Section 8.1.1）。

### 补充图表

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2206_07707/figures/007_Figure_4.jpg]]
*Figure 4: Ours (bw-4) Fig. 4. Post-Process vs. Learned Vector Quantization. We compare applying k-means vector quantization on the feature grid as a post-processing after training, vs. learning vector quantization end-to-end with the same number of codebook entries. We see the k-means quantization has visible discoloration, whereas ours preserves the visual quality*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2206_07707/figures/009_Figure_6.jpg]]
*Figure 6: Ours (learned,4 bitwidth) Fig. 6. Qualitative comparison of static and learned indices. We qualitatively compare a hash approach with 12 bitwidth codebooks and our learned indices with 4 bitwidth codebooks which have similar compression rates. We see that our learned indices are able to reconstruct with less noise*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2206_07707/figures/010_Table_3.jpg]]
*Table 3: Comparison between random indices and learned indices. This table shows the effects of learning codebook indices with VQAD at 120 epochs with different quantization bitwidths (bw). To highlight the tradeoff, we list the size of the indices ?? and codebook ?? separately. We see that even when storing indices, we are able to achieve higher quality than the hash-based approach*



## 定位与知识库关联

### 一、问题定位：特征网格的存储瓶颈

神经场（Neural Fields）在三维场景表示中取得了显著进展，但特征网格方法面临一个核心矛盾：**高质量重建依赖于密集的浮点特征向量，而数百万个顶点的存储需求严重制约了内存和带宽受限应用中的实用性**。以 **NGLOD-NeRF**（Takikawa et al., CVPR 2021）为代表的特征网格基线，每个顶点存储 $k$ 维浮点特征向量（如 $k=16$，每顶点 64 bytes），总存储量可达约 20 MB 甚至更高（Table 2）。这种“笨重”的表示方式使得渐进式流式传输和细节层次（LOD）控制几乎不可能——如 Fig. 1 所示，传统方法如 **NeRF**（Mildenhall et al., ECCV 2020）需要传输约 2.5 MB 数据才能开始渲染任何内容。

VQ-AD 正是瞄准这一瓶颈：**将每个网格顶点的完整特征向量替换为一个低比特整数索引和一个共享码本（codebook）**，通过端到端学习实现 40-60 倍的存储压缩，同时维持视觉质量。

### 二、核心机制：向量量化自解码器（VQ-AD）

VQ-AD 的方法论贡献可分解为三个相互耦合的创新点：

#### 2.1 压缩表示的结构性替换

在未压缩的特征网格中，每个顶点存储 $k$ 维浮点向量 $Z \in \mathbb{R}^{m \times k}$（$m$ 为顶点数）。VQ-AD 将其替换为：
- **整数索引向量** $V \in \mathbb{Z}^m$，取值范围 $[0, 2^b - 1]$，每个顶点仅需 $b$ bits；
- **共享码本** $D \in \mathbb{R}^{2^b \times k}$，包含 $2^b$ 个可学习的特征向量。

推理时，通过硬索引 $D[V]$ 从码本中取回特征向量（Fig. 3b）。这一替换将存储从 $\mathcal{O}(m \cdot k \cdot 32)$ bits 降至 $\mathcal{O}(m \cdot b + 2^b \cdot k \cdot 32)$ bits，其中 $b \in \{4, 6\}$ 是关键的压缩控制旋钮。

#### 2.2 可微软化索引训练

硬索引操作 $D[V]$ 不可微，无法直接端到端优化。VQ-AD 的关键洞察是引入**软化索引矩阵** $C \in \mathbb{R}^{m \times 2^b}$，训练时通过 softmax 生成软索引：

$$\underset{D, C, \theta}{\arg\min} \ \mathbb{E}_{x, y} \left\| \psi_{\theta}\left(x, \mathrm{interp}(x, \sigma(C) D)\right) - y \right\|$$

其中 $\sigma(\cdot)$ 为 softmax 函数，$\psi_\theta$ 为 MLP 解码器。训练完成后，通过 $\arg\max$ 将 $C$ 转换为硬索引 $V$ 用于推理（Fig. 3c）。这一设计允许压缩表示直接针对下游任务（如新视角合成的可微渲染损失）进行优化，避免了传统后处理量化带来的质量损失。

#### 2.3 自解码器框架的统一

VQ-AD 采用自解码器（Auto-Decoder）框架（Park et al., 2019），仅显式构建解码器 $f_\gamma^{-1}$，直接优化压缩系数：

$$\underset{v_x, \gamma}{\arg\min} \left\| F(f_{\gamma}^{-1}(v_x)) - F(u_x) \right\|$$

这种设计将离散信号压缩与神经场训练统一在同一优化循环中，使得压缩表示能够“感知”下游任务损失，形成**损失感知压缩**（loss-aware compression）。

### 三、在方法谱系中的位置

VQ-AD 位于以下方法线的交汇处：

| 方法线 | 代表工作 | VQ-AD 的继承与突破 |
|--------|----------|-------------------|
| **特征网格神经场** | NGLOD-NeRF (Takikawa et al., CVPR 2021), Plenoxels (Yu et al., CVPR 2022) | 继承多分辨率八叉树结构和特征插值机制，但将存储从 $\mathcal{O}(m \cdot k)$ 压缩至 $\mathcal{O}(m \cdot b)$ |
| **向量量化压缩** | k-means VQ (后处理) | 将离线 k-means 升级为端到端学习式 VQ，避免了颜色褪变等后处理伪影（Fig. 4） |
| **哈希索引方法** | Instant NGP (Müller et al., 2022) | 用可学习索引替代静态哈希函数，在相同压缩率下获得更高 PSNR（Table 3: +2.94 dB） |
| **低秩近似压缩** | LRA (矩阵分解) | 在相同或更小存储下，VQ 的 PSNR 和 SSIM 均优于 LRA（Table 2） |
| **渐进式流式传输** | 传统 LOD 方法 (Crassin et al., 2009) | 将多分辨率八叉树与压缩表示结合，实现仅需约 10 kB 即可显示粗糙 LOD（Fig. 2） |

**与 Instant NGP 的关键区别**：Müller et al. (2022) 使用多分辨率哈希表来避免存储特征网格，但哈希冲突导致质量损失。VQ-AD 通过学习索引实现自适应冲突解决，允许使用更小的码本，代价是需要存储索引本身（Table 3 显示，4-bit 学习索引的 PSNR 为 29.60，优于 12-bit 哈希索引的 26.66）。

### 四、适用边界与局限

VQ-AD 的适用性受以下因素制约：

1. **训练内存瓶颈**：软化索引矩阵 $C \in \mathbb{R}^{m \times 2^b}$ 的尺寸随比特宽度指数增长。当 $b=6$ 时，训练峰值内存高达 18 GB（Section 8.1.2），限制了更高比特宽度（如 8-bit）的实验。

2. **几何表示质量**：当应用于符号距离函数（SDF）压缩时，VQ-AD 会在法线方向引入可见伪影（Fig. 5），表明该方法对几何细节的保真度不如对辐射场的颜色信息。

3. **流式传输与熵编码的互斥**：VQ-AD 未采用熵编码（如 gzip），因为熵编码的变长特性与渐进式流式传输不兼容（Section 8.2）。实验表明 gzip 可额外压缩 4-7%，但会破坏流式能力。

4. **深度监督依赖**：当前方法依赖深度监督来初始化八叉树结构（Section 5），对无深度监督的场景（如稀疏视角输入、单张图像）适用性未知。

5. **推理速度**：压缩模型的推理速度与未压缩基线相当（约 15 FPS），但预估可通过缓存优化进一步提升（Section 8.1.1）。

### 五、开放问题

VQ-AD 留下的研究缺口包括：

- **训练内存优化**：能否设计更高效的软化索引机制（如 Gumbel-Softmax 或分块训练），以支持更高比特宽度？
- **混合索引方案**：能否结合学习索引和哈希函数，在保持质量的同时降低存储索引的代价？
- **熵编码与流式传输共存**：是否可能通过分块熵编码或熵最小化正则化（尽管当前实验显示后者会大幅降低重建质量）实现部分流式？
- **稀疏输入扩展**：从单张图像或稀疏视角输入中学习压缩特征网格的可行性如何？
- **码本优化替代方案**：能否利用可微渲染的梯度直接优化码本，而无需软化索引，例如使用直通估计器的变体？

这些问题的解决将推动压缩神经场从“演示级”走向“实用级”，特别是在移动设备、Web 端和带宽受限的流式应用中。



## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Variable_Bitrate_Neural_Fields.pdf]]
