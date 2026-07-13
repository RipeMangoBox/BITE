---
title: "Splatent: Splatting Diffusion Latents for Novel View Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Splatent_Splatting_Diffusion_Latents_for_Novel_View_Synthesis.pdf
project_link: "https://orhir.github.io/Splatent/"
code_link: null
aliases:
- Splatent
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过扩散模型中的多视图自注意力机制，从参考视图向渲染后的潜在表示注入高频细节，补偿因视角不一致导致的频率衰减。
primary_logic: 保持3D表示在低频域，避免直接优化高频成分，转而通过2D空间的多视图注意力从输入视图中恢复高频细节，从而在不改变预训练VAE的前提下获得高保真重建。
claims:
- VAE潜在空间缺乏多视角一致性，导致3D重建结果模糊。
- 将3D表示保持在低频域，通过2D多视图注意力恢复高频细节，能有效克服上述问题。
- 在多个数据集和指标上，Splatent显著优于基线LRF和Feature-3DGS，结果具有统计显著性。
- DL3DV-10K (dense 30 views) 上 MEt3R↓ = 0.0774
---

# Splatent: Splatting Diffusion Latents for Novel View Synthesis

> [!tip] 核心洞察
> 保持3D表示在低频域，避免直接优化高频成分，转而通过2D空间的多视图注意力从输入视图中恢复高频细节，从而在不改变预训练VAE的前提下获得高保真重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | Splatent：基于扩散潜在空间喷射的新视角合成 |
| 英文题名 | Splatent: Splatting Diffusion Latents for Novel View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Hirschorn_Splatent_Splatting_Diffusion_Latents_for_Novel_View_Synthesis_CVPR_2026_paper.html) · [Project](https://orhir.github.io/Splatent/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Splatent |
| Dataset | DL3DV-10K |

> [!tip] 效果简介
> - DL3DV-10K (dense 30 views) 上，MEt3R↓ 0.0774 vs 0.1106 (Feature-3DGS) / 0.1082 (LRF) (~30% improvement)。
> - DL3DV-10K (sparse 5 views) 上，MEt3R↓ 0.0998 vs 0.1281 (Feature-3DGS) / 0.1272 (LRF) (~22% improvement)。
> - DL3DV-10K (feed-forward 5 views) 上，PSNR↑ 17.976 vs 16.691 (MVSplat360) (+1.285)。

## 概要

基于扩散模型潜在空间的新视角合成面临一个根本性瓶颈：预训练VAE的潜在表示缺乏多视角一致性，导致在3D重建过程中，不同视角的高频信息相互抵消，最终产生模糊纹理和缺失细节。针对这一问题，Splatent提出了一种原则性框架，其核心洞察是将3D表示保持在低频域，避免直接优化高频成分，转而通过2D空间的多视图注意力机制从输入参考视图中恢复高频细节。

具体而言，Splatent冻结预训练VAE以保留其原始重建能力，将新视角合成分为两个阶段：第一阶段在潜在空间优化3D高斯泼溅（3DGS），获取粗粒度的几何与纹理；第二阶段引入基于扩散的增强模块，利用单步扩散模型中的自注意力机制，从邻近参考视图的潜在表示中提取高频信息并注入到渲染结果中。该方法在不改变预训练VAE的前提下，显著提升了重建保真度。

在DL3DV-10K数据集上，Splatent在稠密（30视图）和稀疏（5视图）设置下均显著优于基线方法。以MEt3R指标衡量3D一致性，Splatent在稠密设置下达到0.0774，相比**Feature-3DGS**（Zhou et al., CVPR 2024）的0.1106和**LRF**（Zhou et al., ICLR 2025）的0.1082分别提升约30%和28%。在前馈式框架中，Splatent与**MVSplat360**集成后，PSNR提升1.285 dB，FID降低2.365，同时有效减少了幻觉现象。消融实验表明，使用多张参考图像能显著增强细节并减少幻觉，性能在3张视图时趋于饱和。

新视角合成（Novel View Synthesis, NVS）旨在从一组稀疏的输入图像中重建三维场景，并渲染出任意新视角下的逼真图像。近年来，以3D Gaussian Splatting（3DGS）为代表的显式辐射场方法在渲染质量和效率上取得了显著进展。然而，这些方法通常直接在RGB像素空间进行优化，计算开销大，且对输入视图的覆盖范围高度敏感。

与此同时，扩散模型（Diffusion Models）凭借其强大的生成先验，在图像合成领域展现出卓越的高频细节生成能力。扩散模型的变分自编码器（VAE）能够将高分辨率图像压缩到紧凑的潜在空间，大幅降低计算维度。这一特性催生了一类新范式：**在扩散VAE的潜在空间中构建辐射场**，即潜在辐射场（Latent Radiance Fields）。代表性工作包括**Feature-3DGS**（Zhou et al., CVPR 2024）和**LRF (Latent Radiance Fields)**（Zhou et al., ICLR 2025）。Feature-3DGS直接在冻结的VAE潜在空间上优化3DGS，但渲染结果存在严重的纹理模糊和细节丢失；LRF则通过对VAE进行微调来强制多视角一致性，虽然部分缓解了模糊问题，却不可避免地牺牲了预训练VAE的重建质量。

上述方法的困境源于一个根本性瓶颈：**扩散VAE的潜在空间缺乏多视角一致性**。当从不同视角对同一三维点进行编码时，VAE产生的潜在表示在高频分量上存在显著差异。在3DGS优化过程中，这些不一致的高频信息会相互抵消，导致渲染出的潜在特征仅保留低频成分，解码后表现为模糊的纹理和缺失的细节（见Figure 3的频谱分析）。Feature-3DGS完全受制于此瓶颈；LRF试图通过微调VAE来隐式缓解，但代价是损害了VAE原有的重建能力。

Splatent的核心洞察在于：**将三维表示保持在低频域，避免直接优化高频成分，转而通过二维空间的多视图注意力机制，从输入参考视图中恢复高频细节**。这一策略无需对预训练VAE做任何修改，完整保留了其重建能力，同时从根本上解决了潜在空间不一致导致的细节丢失问题。

## 核心方法与创新机理

Splatent 的核心创新在于**识别并化解了扩散VAE潜在空间的多视角不一致性瓶颈**，通过一种“低频3D + 高频2D恢复”的分离策略，在不牺牲预训练VAE重建能力的前提下获得高保真新视角合成。

### 瓶颈发现：VAE潜在空间的多视角不一致性

扩散模型的标准VAE（如LDM的KL-VAE）虽然具有强大的单图压缩与重建能力，但其潜在空间**并非为多视角一致性而设计**。当从不同视角对同一场景进行编码时，同一3D点的潜在表示在高频分量上存在显著差异。在3DGS优化过程中，这些不一致的高频信息会相互抵消，导致渲染出的潜在特征仅保留低频成分，解码后呈现模糊纹理和缺失细节（参见Figure 3的频谱分析）。这一发现构成了方法设计的因果原点。

### 关键洞察：低频3D + 高频2D恢复

面对上述瓶颈，现有方法采取了两种策略：**Feature-3DGS**（Zhou et al., CVPR 2024）保持VAE冻结但渲染质量差；**LRF**（Zhou et al., ICLR 2025）则对VAE进行微调以强制3D一致性，却牺牲了VAE的原始重建质量。Splatent的**核心洞察**是：将3D表示保持在低频域，避免直接优化高频成分，转而通过2D空间的多视图注意力从输入参考视图中恢复高频细节。这一“分离-恢复”范式无需修改VAE，完整保留了其重建能力。

### Changed Slots：相对于基线的关键设计变化

| 设计维度 | 基线方法 | Splatent方案 | 因果作用 |
|---------|---------|-------------|---------|
| **VAE处理方式** | LRF微调VAE以强制3D一致性；Feature-3DGS保持VAE冻结但渲染质量差 | **VAE完全冻结**，保留其原始重建能力 | 避免微调导致的重建质量退化，维持VAE的泛化性 |
| **高频细节恢复机制** | Feature-3DGS无高频恢复；LRF通过微调VAE隐式缓解 | 在2D空间利用**单步扩散模型与多视图自注意力**，从邻近参考视图中提取高频细节并注入渲染潜在表示 | 将多视角不一致性从“bug”转化为“feature”——利用参考视图的高频信息补偿渲染视图的衰减 |
| **管道阶段性** | 仅优化潜在3DGS（Feature-3DGS）或优化+微调（LRF） | **两阶段解耦**：第一阶段优化潜在3DGS获得粗粒度几何与低频纹理；第二阶段通过扩散增强恢复高频细节 | 阶段解耦使得3DGS专注于几何重建，扩散模块专注于纹理增强，各司其职 |

### 扩散增强模块：2D空间的跨视角信息融合

第二阶段的核心机制是**基于扩散的潜在特征增强**。具体而言，将渲染的潜在表示与选定的参考视图潜在表示拼接为空间网格（渲染视图置于左上角），输入预训练的扩散模型。在单步去噪过程中，扩散模型的自注意力机制在网格内所有视图间聚合信息，使得渲染视图能够从参考视图中“借用”高频细节。这一设计的关键在于：

- **全潜在空间操作**：渲染与增强均在潜在空间完成，避免了解码-编码带来的信息损失和计算开销。
- **多视图注意力作为信息桥**：自注意力机制天然支持跨视图信息传递，无需显式的几何对齐或特征投影。
- **单步扩散**：仅需一次去噪步骤即可完成增强，在效率与质量间取得平衡。

### 与基线方法的本质差异

相比LRF的“强制一致性”思路，Splatent承认VAE潜在空间的多视角不一致性是固有属性，转而通过2D扩散模型在渲染阶段进行补偿。这一范式转变使得方法具有更强的泛化性——模型仅在DL3DV-10K上训练，即可在LLFF和Mip-NeRF360等未见数据集上显著优于基线（参见Table 1）。此外，Splatent的增强模块可**即插即用**地集成到前馈式潜在3DGS框架（如MVSplat360）中，在保持几何精度的同时提升感知质量并减少幻觉（参见Table 4、Figure 5）。

Splatent 的整体 pipeline 采用两阶段设计，将 3D 重建的几何/纹理建模与高频细节恢复解耦为独立的处理阶段，从而在不修改预训练 VAE 的前提下获得高保真新视角合成结果。

**第一阶段：潜在空间 3DGS 优化。** 给定一组已知相机参数的输入视图，首先通过冻结的预训练 VAE 编码器 $\mathcal{E}$ 将每张图像映射到潜在空间，得到潜在码 $z = \mathcal{E}(I) \in \mathbb{R}^{h \times w \times d}$（压缩比 $f=8$）。随后，直接在这些潜在表示上优化 3D Gaussian Splatting（3DGS）模型，重建底层的潜在辐射场。这一阶段的核心目标是获取场景的粗粒度几何结构和低频纹理信息。然而，由于扩散 VAE 的潜在空间缺乏多视角一致性，渲染得到的新视角潜在表示中高频分量显著衰减，导致解码后图像模糊、细节缺失——这是论文识别的核心瓶颈（Figure 3 的频谱分析为此提供了直接证据）。

**第二阶段：扩散增强模块。** 为解决上述高频衰减问题，Splatent 引入基于扩散的精细化机制。具体而言，将第一阶段渲染的目标视角潜在表示与 $V=3$ 张邻近参考视图的潜在表示按空间网格拼接（渲染视图置于左上角），输入到预训练的 Stable Diffusion Turbo 模型中。通过单步扩散过程，利用模型内部的自注意力机制在 2D 空间实现跨视图信息聚合——参考视图中的高频细节被提取并注入到渲染潜在表示中，补偿因 3DGS 优化过程中多视角不一致导致的高频抵消效应。增强后的潜在表示 $\hat{z}_{\text{refined}}$ 最终通过冻结的 VAE 解码器 $\mathcal{D}$ 恢复为高保真 RGB 图像。

**关键设计决策。** 整个 pipeline 完全在潜在空间中运行——渲染与增强均在潜在域完成，仅在最后一步解码到图像空间。VAE 始终保持冻结状态，保留其原始重建能力，这与 **LRF**（Zhou et al., ICLR 2025）通过微调 VAE 强制 3D 一致性但牺牲重建质量的做法形成对比。同时，区别于 **Feature-3DGS**（Zhou et al., CVPR 2024）直接渲染 VAE 特征而无任何细节恢复机制，Splatent 通过 2D 多视图注意力从输入视图中恢复高频信息，实现了“3D 表示保持低频域，高频细节在 2D 空间补偿”的核心洞察。

**训练配置。** 扩散增强模块在 DL3DV-10K 训练集的 400 个场景子集上微调，使用 8 张 NVIDIA H100 GPU 训练约 24 小时。训练损失由三项加权组成：潜在空间 L2 重构损失 $\mathcal{L}_{\text{recon}}$、解码后图像的感知损失 $\mathcal{L}_{\text{LPIPS}}$（权重 $\lambda_{\text{LPIPS}}=2$），以及解码后 RGB 像素的 L2 损失 $\mathcal{L}_{\text{RGB}}$（权重 $\lambda_{\text{RGB}}=1$）。

![[assets/figures/papers/paper_list_l2599_https_openaccess_thecvf_com_content_CVPR2026_html_Hirschorn_Splatent_Spl/figures/002_Figure_2.jpg]]
*Figure 2: Framework Overview. Given a set of input views with known camera parameters, each image is encoded into the VAE latent space of a diffusion model. We then perform 3DGS optimization to reconstruct the underlying latent radiance field. Due to multiview inconsistencies in diffusion VAEs latent space, a rendered novel view latent lacks high frequency details. We tile this rendered view together with reference views into a grid, and leverage a single-step diffusion model with self-attention mechanism that aggregates information across all views. The enhanced latent image is finally decoded to receive the novel view image*

![[assets/figures/papers/paper_list_l2599_https_openaccess_thecvf_com_content_CVPR2026_html_Hirschorn_Splatent_Spl/figures/001_Figure_1.jpg]]
*Figure 1: Novel view synthesis from a latent-space radiance field. Splatent is a principled framework to enhance rendered novel views from a radiance field in the latent space of diffusion VAEs. We demonstrate improvements in image quality in the setting of test-time latent radiance field optimization, compared to LRF [60]. In addition, we show how Splatent can be connected within a latent-based feed-forward model like MVSplat360 [9] to enhance the results and reduce hallucinations*

Splatent 的整个管道由两个核心阶段构成：**潜在空间 3DGS 优化**（低频几何重建）和**扩散增强模块**（高频纹理恢复）。以下逐一拆解关键模块与公式。

### 阶段一：潜在空间 3DGS 优化

给定一组输入视图及其相机参数，首先通过预训练的 VAE 编码器 $\mathcal{E}$ 将每张图像 $I$ 映射到潜在空间：

$$z = \mathcal{E}(I) \in \mathbb{R}^{h \times w \times d}$$

其中 $h = H/f$, $w = W/f$，$f = 8$ 为压缩比，$d$ 为潜在维度。编码器来自 Latent Diffusion Model 的 KL-based VAE，在整个过程中**完全冻结**，以保留其原始重建能力。

随后，在潜在空间中优化一个 3DGS 模型。每个 3D 高斯由以下参数化表示：

$$G = (\mu, \Sigma, \alpha, f_{\mathrm{c}})$$

其中 $\mu$ 为均值（位置），$\Sigma$ 为协方差（形状），$\alpha$ 为不透明度，$f_{\mathrm{c}}$ 为颜色表示。优化目标是最小化渲染潜在表示与输入视图编码之间的差异，从而获得场景的低频几何和纹理结构。

这一阶段的核心问题是：扩散 VAE 的潜在空间**缺乏多视角一致性**。在 3DGS 优化过程中，不同视角下不一致的高频分量会相互抵消，导致渲染出的潜在表示仅保留低频成分，解码后产生模糊纹理和缺失细节（见 Figure 3 的频谱分析）。

![[assets/figures/papers/paper_list_l2599_https_openaccess_thecvf_com_content_CVPR2026_html_Hirschorn_Splatent_Spl/figures/003_Figure_3.jpg]]
*Figure 3: VAE latents spectral analysis. (a) Images in latent space and the corresponding image space (after decoding) (b) Magnitude spectrum of the latent image (Rendered, Ours and Ground Truth), normalized to 1. In both visualizations, VAE latents contain both low- and high-frequency components (green). During 3DGS optimization, inconsistent high frequencies average out, leaving only low-frequency components (blue) and causing blurry decoded images. Our method produces latents whose spectrum closely matches that of the original VAE latents, reconstructing high-frequency details (orange). Graphs show averages over more than 45K latent images from 140 scenes*

### 阶段二：扩散增强模块

为解决上述问题，Splatent 在第二阶段引入基于扩散的增强机制。其核心思想是：**保持 3D 表示在低频域，转而通过 2D 空间的多视图注意力从输入视图中恢复高频细节**。

具体做法是：将渲染的目标视图潜在表示与 $V$ 张参考视图潜在表示拼接成一个空间网格（目标视图置于左上角），输入一个经过微调的单步扩散模型。该模型利用自注意力机制在去噪过程中跨视图聚合信息，从参考视图中提取高频细节并注入到渲染潜在表示中。

增强模块的训练使用以下损失函数。

**潜在重构损失**（L2 距离）：

$$\mathcal{L}_{\mathrm{recon}} = \| \hat{z}_{\mathrm{refined}} - z_{\mathrm{gt}} \|_2^2$$

其中 $\hat{z}_{\mathrm{refined}}$ 为增强后的潜在表示，$z_{\mathrm{gt}}$ 为真实潜在表示。

**感知损失**（LPIPS，在解码后的 RGB 图像上计算）：

$$\mathcal{L}_{\mathrm{LPIPS}} = \mathrm{LPIPS}\big( \mathcal{D}(\hat{z}_{\mathrm{refined}}), \mathcal{D}(z_{\mathrm{gt}}) \big)$$

其中 $\mathcal{D}$ 为 VAE 解码器。

**RGB 重构损失**（解码后像素级 L2）：

$$\mathcal{L}_{\mathrm{RGB}} = \left\| \mathcal{D}(\hat{z}_{\mathrm{refined}}) - \mathcal{D}(z_{\mathrm{gt}}) \right\|_2^2$$

**总损失**为三者的加权和：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{LPIPS}} \mathcal{L}_{\mathrm{LPIPS}} + \lambda_{\mathrm{RGB}} \mathcal{L}_{\mathrm{RGB}}$$

其中 $\lambda_{\mathrm{LPIPS}} = 2$, $\lambda_{\mathrm{RGB}} = 1$。

### 关键设计决策

1. **VAE 冻结 vs 微调**：与 **LRF**（Zhou et al., ICLR 2025）微调 VAE 以强制 3D 一致性的策略不同，Splatent 保持 VAE 完全冻结。LRF 的微调虽然改善了多视角一致性，但会牺牲 VAE 的重建质量；Splatent 通过外部扩散增强来补偿一致性损失，从而保留了 VAE 的完整解码能力。

2. **单步扩散 vs 多步扩散**：增强模块采用预训练的 Stable Diffusion Turbo 进行单步去噪，而非标准的多步扩散过程。这大幅降低了推理开销，使其能够嵌入到逐场景优化的管道中。

3. **参考视图数量**：消融实验（Table 3）表明，使用多张参考图像能显著减少幻觉并增强细节。完全不使用参考视图（即无扩散增强）时，FID 从 35.60 急剧上升至 83.66。性能在 3 张参考视图时达到饱和，因此默认配置 $V = 3$。

## 实验与关键发现

### 核心瓶颈的实证验证：VAE潜在空间的多视角不一致性

Splatent的设计根植于一个关键的实证发现：扩散VAE的潜在空间缺乏多视角一致性。这一瓶颈在3D重建过程中表现为高频信息的相互抵消，最终导致模糊纹理和缺失细节。论文通过频谱分析（Figure 3）对这一现象进行了量化验证：对超过140个场景、45K张潜在图像的平均幅度谱显示，渲染后的潜在表示（Rendered）在高频段显著衰减，仅保留低频成分；而Splatent增强后的潜在表示（Ours）的频谱与真实VAE潜在表示（Ground Truth）高度吻合，成功恢复了高频细节。这一分析构成了整个方法论的因果基础——既然直接优化3D表示无法保留高频信息，那么将3D表示维持在低频域、转而在2D空间通过多视图注意力从参考视图中注入高频细节，便成为逻辑上自洽的解决方案。

### 主要定量结果

Table 1汇总了Splatent在DL3DV-10K、LLFF和Mip-NeRF360三个数据集上的新视角合成性能，涵盖稠密（30视图）和稀疏（5视图）两种输入配置。所有方法仅在DL3DV-10K上训练，跨数据集评估以验证泛化性；输入视图采用最远点采样策略，确保对比公平。

**稠密设置下**，Splatent在DL3DV-10K上取得PSNR 21.94、SSIM 0.692、LPIPS 0.265、FID 35.60，全面优于**Feature-3DGS**（Zhou et al., CVPR 2024）和**LRF**（Zhou et al., ICLR 2025）。FID指标的优势尤为突出（35.60 vs. LRF的48.05），表明感知质量有实质性的提升。在LLFF和Mip-NeRF360上的跨数据集泛化结果同样保持领先，验证了方法不依赖于特定场景分布。

**稀疏设置下**（5视图），Splatent在DL3DV-10K上仍保持PSNR 20.61、FID 41.01，相比Feature-3DGS（PSNR 19.15, FID 58.17）和LRF（PSNR 19.42, FID 55.84）的优势幅度甚至更大。这表明扩散增强模块在输入信息受限时发挥了更关键的作用——当3DGS优化的潜在辐射场本身信息不足时，多视图注意力机制能够更有效地从有限的参考视图中补偿缺失的细节。

**3D一致性评估**（Table 2）采用MEt3R指标（越低越好）衡量多视角几何一致性。在DL3DV-10K稠密设置下，Splatent取得0.0774，相比Feature-3DGS的0.1106和LRF的0.1082提升约30%；稀疏设置下为0.0998，相比两个基线的0.1281和0.1272提升约22%。这一结果表明，尽管Splatent的增强过程发生在2D潜在空间，但多视图注意力机制有效地保持了跨视角的几何一致性，并未因引入参考视图信息而破坏3D结构。

### 消融实验：参考视图数量的影响

Table 3系统分析了参考视图数量对增强效果的影响。完全不使用扩散增强（无参考视图）时，FID急剧恶化至83.66，PSNR降至19.47，验证了扩散模块是性能的核心贡献者。使用1张参考视图即可将FID从83.66大幅降至38.04，PSNR提升至21.61；增加到3张视图时性能趋于饱和（FID 35.60, PSNR 21.94），继续增加到5张视图的边际收益极小（FID 35.16, PSNR 21.96）。这一饱和现象表明，3张空间邻近的参考视图已能为多视图注意力提供足够的高频信息源，超过此数量后信息冗余增加但有效增益递减。论文据此将默认参考视图数设为3，在性能与计算开销之间取得平衡。

### 前馈式框架集成

Splatent不仅适用于测试时优化的场景，还可作为即插即用的增强模块集成到前馈式潜在3DGS方法中。Table 4展示了在DL3DV-10K上使用5张输入视图时，将Splatent接入**MVSplat360**后的性能变化：PSNR从16.691提升至17.976（+1.285），SSIM从0.514提升至0.531（+0.017），LPIPS从0.431降至0.378（-0.053），FID从13.462降至11.097（-2.365）。定性结果（Figure 5）进一步显示，MVSplat360在前馈推理中容易产生幻觉（如凭空生成窗户或树木），而Splatent增强后的输出更忠实于场景的真实结构，同时保留了更丰富的纹理细节。这表明扩散增强模块的多视图注意力机制不仅能恢复高频纹理，还能在一定程度上纠正前馈模型的几何幻觉。

![[assets/figures/papers/paper_list_l2599_https_openaccess_thecvf_com_content_CVPR2026_html_Hirschorn_Splatent_Spl/figures/006_Figure_5.jpg]]
*Figure 5: Feed-Forward Qualitative comparison. We demonstrate how Splatent can enhance feed-forward latent radiance field methods such as MVSplat360 [9]. While MVSplat360 often hallucinates (e.g., the window in the first example or the tree in the last example) and lacks fine details, Splatent yields sharper and more faithful reconstructions*

### 定性分析与失败模式

Figure 4的定性对比直观展示了三种方法的差异：Feature-3DGS的重建结果存在显著的细节丢失，纹理区域呈现模糊块状；LRF通过微调VAE在一定程度上改善了这一问题，但仍无法恢复精细结构（如细密的栅栏、文字标识等）；Splatent则产生了更锐利、更逼真的重建，高频细节（如叶片纹理、建筑装饰线条）得到了有效保留。

**需要注意的局限性**：论文未系统报告失败案例。从方法设计推断，Splatent的性能依赖于参考视图与目标视图之间的空间邻近性和视觉重叠度——当目标视角与所有参考视图的重叠区域极小时，多视图注意力可能无法获取足够的相关信息，增强效果预计会退化。此外，扩散模型的微调仅在DL3DV-10K的400个场景子集上进行（8×H100 GPU，约24小时），对于与训练分布差异极大的场景类型，增强质量可能下降。这些推断需要在实际应用中手动验证。

![[assets/figures/papers/paper_list_l2599_https_openaccess_thecvf_com_content_CVPR2026_html_Hirschorn_Splatent_Spl/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison. We compare our method using DL3DV-10K, LLFF and Mip-NeRF360 datasets. In the dense setting, we use 30 input views (except for the LLFF dataset, for which we use 1/8 of views in each scene). In the sparse setting, we use 5 input views. The rest of the views in each scene are used for evaluation. LRF and Splatent are trained only on DL3DV-10K. Best results in bold*

![[assets/figures/papers/paper_list_l2599_https_openaccess_thecvf_com_content_CVPR2026_html_Hirschorn_Splatent_Spl/figures/008_Table_3.jpg]]
*Table 3: Components ablation. Impact of reference image count. Multiple references reduce hallucinations and enhance details, with performance saturating at 3 views*

## 定位与知识库关联

### 问题定位：扩散VAE潜在空间的多视角不一致瓶颈

Splatent 的核心动机源于一个被先前工作忽视的关键瓶颈：预训练扩散模型（如 Stable Diffusion）的 VAE 潜在空间**缺乏多视角一致性**。当从不同视角编码同一场景时，VAE 产生的潜在表示在纹理、光照等高频细节上存在系统性偏移。在 3D 重建过程中，这些不一致的高频信号在优化时相互抵消，导致渲染结果仅保留低频成分，表现为模糊纹理和缺失细节（见 Figure 3 的频谱分析）。这一问题直接制约了潜在空间辐射场在新视角合成中的保真度。

### 与基线工作的关系：冻结 VAE 与 2D 细节恢复的双重策略

Splatent 的方法设计围绕两个关键选择展开，每个选择都直接回应了现有基线的不足：

**1. VAE 处理方式：冻结 vs. 微调**

- **Feature-3DGS**（Zhou et al., CVPR 2024）保持 VAE 冻结，直接在潜在空间优化 3DGS，但缺乏任何细节恢复机制，渲染结果细节损失严重。
- **LRF**（Latent Radiance Fields, Zhou et al., ICLR 2025）通过对 VAE 进行微调来强制多视角一致性，但这会牺牲 VAE 的原始重建质量——微调后的 VAE 解码器无法再准确恢复预训练模型所学的丰富纹理先验。
- **Splatent 的选择**：VAE **完全冻结**，保留其原始重建能力。这一选择的关键在于认识到 VAE 的不一致性是高频域的问题，而非低频几何——因此无需修改 VAE 本身，而是将恢复任务转移到下游的扩散增强模块。

**2. 高频细节恢复机制：2D 多视图注意力 vs. 隐式缓解**

- Feature-3DGS 无高频恢复机制。
- LRF 通过微调 VAE 隐式缓解不一致性，但效果有限，仍无法恢复精细纹理（见 Figure 4 定性对比）。
- **Splatent 的机制**：在 2D 空间利用**单步扩散模型与多视图自注意力**，将渲染后的低频潜在表示与邻近参考视图的潜在表示拼接为空间网格，通过扩散去噪过程中的注意力机制从参考视图中提取高频细节并注入到目标视图中。这一设计的核心洞察是：**将 3D 表示保持在低频域，避免直接优化高频成分，转而通过 2D 空间的多视图注意力从输入视图中恢复高频细节**。

### 管道架构：两阶段解耦设计

Splatent 采用明确的两阶段管道，与端到端优化的基线形成对比：

- **第一阶段（潜在空间 3DGS 优化）**：从输入视图的 VAE 潜在表示重建粗糙的潜在辐射场，获得低频几何和纹理。此阶段仅关注结构一致性。
- **第二阶段（扩散增强）**：接收第一阶段渲染的潜在表示和选定的参考视图，通过单步扩散与自注意力恢复高频细节。两阶段解耦使得几何优化和纹理增强可以独立进行，避免了联合优化中的梯度冲突。

### 与前馈式方法的集成

Splatent 不仅适用于逐场景优化的潜在辐射场，还可以作为增强模块集成到前馈式框架中。论文以 **MVSplat360** 为基线，展示了 Splatent 在该框架下的增强能力：MVSplat360 在前馈推理中常产生幻觉（如虚构窗户、树木），而 Splatent 通过多视图注意力机制显著减少了这些伪影，同时提升了感知质量（Table 4：FID 从 13.462 降至 11.097）。

### 适用边界与局限

基于论文提供的证据，Splatent 的适用边界可从以下维度界定：

1. **扩散模型依赖性**：方法依赖预训练扩散模型（Stable Diffusion Turbo）的 VAE 和去噪网络。在扩散模型覆盖域之外的场景（如特殊成像模态），方法的适用性需要手动验证。
2. **参考视图质量与数量**：消融实验（Table 3）表明，完全不使用参考视图会导致性能急剧下降（FID 从 35.60 升至 83.66），而性能在 3 张参考视图时达到饱和。这说明方法对参考视图的可用性有基本要求。
3. **跨数据集泛化**：模型仅在 DL3DV-10K 上训练，但在 LLFF 和 Mip-NeRF360 上评估时仍表现出一致的性能提升（Table 1），表明方法具有一定的泛化能力。然而，论文未提供在更大域偏移（如室外航拍、医学影像）下的测试结果。
4. **计算开销**：扩散增强阶段引入了额外的前向传播成本（使用 8 张 NVIDIA H100 GPU 微调约 24 小时），相比纯潜在 3DGS 方法增加了推理时间。论文未提供详细的推理延迟对比，该点需要手动验证。

### 开放问题

1. **VAE 不一致性的理论刻画**：论文通过频谱分析（Figure 3）实证了 VAE 潜在空间的高频不一致性，但未从理论上分析这种不一致性的来源（是训练数据的视角偏差，还是 VAE 架构的固有属性）。理解这一机制可能指导未来设计更本质的解决方案。
2. **扩散增强的几何保真度**：虽然 Table 2 的 MEt3R 指标表明 Splatent 提升了 3D 一致性，但扩散模型在恢复纹理时是否可能引入几何层面的细微扭曲，论文未深入探讨。
3. **与 NeRF 类方法的对比**：论文仅与潜在空间 3DGS 方法（Feature-3DGS、LRF）和 MVSplat360 进行了对比，未涉及基于 NeRF 的潜在辐射场方法（如 Latent-NeRF），后者可能在几何表示上有不同特性。
4. **实时应用的可能性**：两阶段管道和扩散推理的计算成本限制了实时应用。是否可以通过蒸馏或更高效的注意力机制降低推理开销，是工程化部署的关键问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/Splatent_Splatting_Diffusion_Latents_for_Novel_View_Synthesis.pdf]]
