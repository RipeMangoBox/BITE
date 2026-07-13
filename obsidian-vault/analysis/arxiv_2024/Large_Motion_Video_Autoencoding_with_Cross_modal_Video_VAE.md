---
title: Large Motion Video Autoencoding with Cross-modal Video VAE
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/Large_Motion_Video_Autoencoding_with_Cross_modal_Video_VAE.pdf
project_link: https://yzxing87.github.io/vae/
code_link: null
aliases:
- CMVV
- LMVACMVV
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过解耦的两阶段时空建模（时间感知空间编码器+轻量级时间压缩模型）并结合跨模态文本引导，有效降低了运动模糊和细节丢失。
primary_logic: 同时压缩模式有利于保持细节和纹理稳定性，顺序压缩模式有利于大运动恢复；将两者优势融合并引入文本语义指导，可在大运动视频上实现更优的重建性能。
claims:
- Cross-modal Video VAE achieves higher PSNR and lower LPIPS than strong baselines (Open-Sora, Open-Sora-Plan, CV-VAE) on WebVid, Inter4K, and large-motion test sets.
- The proposed two-stage spatiotemporal modeling significantly outperforms simultaneous and sequential compression methods on the large-motion test set.
- Video GAN loss and larger temporal convolution kernels improve reconstruction quality over image GAN loss and small kernels.
- Joint image-video training substantially improves both image and video reconstruction performance.
---

# Large Motion Video Autoencoding with Cross-modal Video VAE

> [!tip] 核心洞察
> 同时压缩模式有利于保持细节和纹理稳定性，顺序压缩模式有利于大运动恢复；将两者优势融合并引入文本语义指导，可在大运动视频上实现更优的重建性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于跨模态视频VAE的大运动视频自编码 |
| 英文题名 | Large Motion Video Autoencoding with Cross-modal Video VAE |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2412.17805) · [Project](https://yzxing87.github.io/vae/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Cross-modal Video VAE |
| Dataset | WebVid test set |

> [!tip] 效果简介
> - WebVid test set 上，PSNR (dB) ↑ 30.11 (Cross-modal VAE) vs 29.38 (Open-Sora) (+0.73)；LPIPS ↓ 0.0544 (Cross-modal VAE) vs 0.1240 (Open-Sora) (-0.0696)。

## 概要

**核心问题**：现有视频VAE大多将图像VAE的2D卷积直接膨胀为3D卷积，形成时空耦合压缩。这种“同时压缩”模式在大运动场景下会引发运动模糊、细节失真和时序闪烁；而“先空间后时间”的顺序压缩虽有利于大运动恢复，却容易丢失纹理细节。此外，现有方法普遍缺乏对跨模态文本信息的利用，限制了重建质量的上限。

**核心结论**：本文提出**Cross-modal Video VAE**，通过解耦的两阶段时空建模（时间感知空间编码器 + 轻量级时间压缩模型）融合同时压缩与顺序压缩的优势，并引入跨模态文本引导，在大运动视频重建上显著超越现有方法。在WebVid测试集上，该方法相较Open-Sora VAE将PSNR从29.38 dB提升至30.11 dB，LPIPS从0.1240降至0.0544；在大运动专项测试集上的消融实验进一步验证了两阶段建模（Table 3）和视频GAN损失（Table 4）的关键作用。

**方法定位**：本文方法属于视频自编码器（Video VAE）范畴，直接对标Open-Sora VAE、Open-Sora-Plan OD VAE、CV-VAE等主流视频VAE，同时也可作为CogVideoX、Cosmos Tokenizer等潜空间视频扩散模型的tokenizer替代方案。其核心改进在于将时空压缩从单一策略升级为两阶段混合策略，并首次在视频VAE中引入Flan-T5文本嵌入的交叉注意力机制。

**主要结果速览**：
- 在WebVid、Inter4K及大运动测试集上，PSNR、SSIM、LPIPS全面优于Open-Sora、Open-Sora-Plan和CV-VAE（Table 1）。
- 联合图像-视频训练策略使图像和视频重建性能同时获得显著提升（Table 2）。
- 视频3D GAN损失和更大的时序卷积核（如(7,3,3)）对重建质量有正向贡献（Table 4）。



视频生成模型（如视频扩散模型）的快速发展对视频压缩与重建提出了更高要求。视频自编码器（Video VAE）作为这类模型的核心组件，负责将高维视频数据压缩到低维潜空间，再从潜空间重建视频。其重建质量直接影响下游生成模型的性能上限。

当前主流的视频VAE方案大多是将图像VAE直接扩展到三维。这种扩展路径主要存在两种范式：**同时压缩**（simultaneous compression）与**顺序压缩**（sequential compression）。同时压缩通过将预训练的2D卷积膨胀为3D卷积，在单个阶段内同时压缩空间与时间维度；顺序压缩则先用空间编码器压缩空间信息，再用时间编码器压缩时序冗余。然而，这两种范式各自存在结构性缺陷：

- **同时压缩**将空间与时间维度耦合处理，虽然有利于保持纹理细节和时序稳定性，但在大运动场景下容易产生运动模糊和细节失真。
- **顺序压缩**将空间与时间解耦，有利于恢复大运动，但由于空间编码阶段缺乏时序感知，容易丢失跨帧的动态信息，导致重建出现时序闪烁和纹理断裂。

更为关键的是，现有视频VAE方法普遍忽略了**跨模态文本信息**的利用。视频数据天然携带文本描述（如字幕、标签），这些语义信息可以为编码器提供场景内容先验，指导解码器更准确地恢复细节。然而，已有的视频VAE均未将文本条件引入压缩-重建流程，这在大运动、复杂场景下进一步限制了重建质量的提升空间。

上述问题的根源在于：**单一压缩范式无法同时兼顾纹理保真度与大运动恢复能力，且缺乏语义引导机制来弥补压缩过程中的信息损失**。因此，如何设计一种能够融合同时压缩与顺序压缩优势、并有效利用文本语义的视频VAE架构，成为提升大运动视频重建质量的关键挑战。



## 核心方法与创新机理

本工作提出的 **Cross-modal Video VAE** 围绕现有视频 VAE 在大运动场景下的根本瓶颈——时空压缩耦合与跨模态信息缺失——进行了三项关键创新，形成一条从压缩策略到训练范式的完整改进链路。

### 创新一：解耦的两阶段时空压缩建模

现有视频 VAE 普遍采用两种时空压缩策略：**同时压缩**（将预训练 2D 空间 VAE 直接膨胀为 3D VAE，时空维度一并压缩）与**顺序压缩**（先压缩空间、再压缩时间）。前者有利于保持细节和纹理稳定性，但在大运动下易产生模糊和重影；后者对大运动恢复更友好，但空间细节容易丢失。本工作识别出这两种策略的互补特性，提出**两阶段时空建模**（Figure 2）：

- **第一阶段**：时间感知空间自编码器（temporal-aware spatial autoencoder），仅压缩空间维度（8× 下采样），同时通过膨胀的 3D 卷积捕获跨帧运动信息，输出中间潜变量 $\mathbf{Z}_1 = \mathcal{E}_1(\mathbf{X})$。
- **第二阶段**：轻量级时间自编码器，对 $\mathbf{Z}_1$ 进一步压缩时间冗余，得到最终潜变量 $\mathbf{Z}_2 = \mathcal{E}_2(\mathbf{Z}_1)$。

这一设计融合了同时压缩的细节保持能力与顺序压缩的运动恢复优势。消融实验（Table 3）在大运动测试集上验证了该策略显著优于单一的同时或顺序压缩方案（PSNR/SSIM/LPIPS 均有明显提升）。

### 创新二：跨模态文本引导

现有视频 VAE 仅依赖视觉信号，缺乏对场景语义的先验理解，导致在复杂纹理和大运动遮挡区域的细节恢复不足。本工作首次将文本信息引入视频 VAE 的编解码过程：在时间感知空间编码器和解码器的每个 ResNet 块之后，插入交叉注意力层，以视觉 token 作为 Query 和 Value，以 **Flan-T5** 文本嵌入作为 Key，将语义先验注入特征重建（Figure 3）。定性结果（Figure 5）表明，跨模态文本引导有效改善了细节恢复，减少了运动模糊和伪影。

### 创新三：联合图像-视频训练与视频 GAN 损失

为在保持图像重建能力的同时学习视频时序动态，本工作采用**联合图像-视频训练**策略：以 8:2 的视频-图像比例采样，对图像批次屏蔽时序模块。Table 2 显示该策略使图像和视频重建性能同时获得显著提升。此外，将传统图像 GAN 损失替换为**视频 3D GAN 损失**，并增大时序卷积核尺寸（如 (7,3,3)），进一步抑制时序闪烁和运动模糊（Table 4）。

---

**创新总结**：Cross-modal Video VAE 的核心贡献在于通过解耦的两阶段压缩策略解决了时空耦合难题，并通过跨模态文本引导和联合训练范式填补了视频 VAE 在语义利用与训练数据方面的空白，在大运动视频重建上实现了对 **Open-Sora**、**Open-Sora-Plan**、**CV-VAE** 等强基线的显著超越（Table 1）。



Cross‑modal Video VAE 的整体 pipeline 遵循一个解耦的两阶段时空压缩范式：**时间感知的空间编码 → 轻量时间压缩 → 时间解码 → 空间解码**，并在编解码过程中注入文本语义信息以增强细节恢复。其核心思想是将“同时压缩”和“顺序压缩”的优势融合——同时压缩有利于保持细节与纹理稳定性，顺序压缩有利于大运动恢复——从而在大运动视频上获得更优的重建质量。

### 输入输出定义

给定输入视频张量 $\mathbf{X} \in \mathbb{R}^{C \times T \times H \times W}$（$C$ 为通道数，$T$ 为帧数，$H,W$ 为空间分辨率），目标是学习编码器 $\mathcal{E}$ 和解码器 $\mathcal{D}$，使得：

$$\mathbf{Z} = \mathcal{E}(\mathbf{X}), \quad \hat{\mathbf{X}} = \mathcal{D}(\mathbf{Z})$$

潜变量 $\mathbf{Z}$ 在空间和时间维度上均被压缩，解码器则需以高时空保真度重建视频，尤其在大运动场景下避免运动模糊、细节失真和时序闪烁。

### 两阶段编码流程

**第一阶段：时间感知的空间编码器（Temporal‑aware Spatial Encoder）**

第一阶段仅压缩空间维度，不压缩时间维度，输出中间潜变量 $\mathbf{Z}_1$：

$$\mathbf{Z}_1 = \mathcal{E}_1(\mathbf{X})$$

该编码器以 Stable Diffusion VAE 的 2D 卷积为基础，将其膨胀为 3D 卷积，并在其后追加一个额外的 3D 卷积作为时间卷积，构成 **STBlock3D**（Figure 3）。STBlock3D 使编码器在压缩空间的同时捕获跨帧运动信息，为后续时间压缩提供高质量的特征表示。同时，在每个 ResNet 块之后注入交叉注意力层，以视觉 token 作为 Query/Value、文本嵌入作为 Key，实现跨模态文本引导。

**第二阶段：轻量时间编码器（Temporal Encoder）**

第二阶段对 $\mathbf{Z}_1$ 进一步压缩时间冗余，得到最终潜变量 $\mathbf{Z}_2$：

$$\mathbf{Z}_2 = \mathcal{E}_2(\mathbf{Z}_1)$$

该时间编码器由 3D ResNet 块构成，结构轻量，仅负责时序维度的压缩，避免了对空间细节的干扰。

### 两阶段解码流程

解码过程是编码的逆过程，先由时间解码器 $\mathcal{D}_2$ 处理 $\mathbf{Z}_2$ 恢复时间维度，再由空间解码器 $\mathcal{D}_1$ 重建视频：

$$\hat{\mathbf{X}} = \mathcal{D}_1(\mathcal{D}_2(\mathbf{Z}_2)) = \mathcal{D}_1(\mathbf{Z}_1)$$

空间解码器同样采用 STBlock3D 结构和交叉注意力文本引导，确保重建视频在空间细节和时序一致性上均达到高质量。

### 跨模态文本注入机制

文本信息通过 Flan‑T5 编码为嵌入向量，在空间编码器和空间解码器的每个 ResNet 块后以交叉注意力的形式注入：视觉特征图被切分为 patch token（各层 patch size 分别为 $8\times8$、$4\times4$、$2\times2$、$1\times1$），作为交叉注意力的 Query 和 Value，文本嵌入作为 Key。这一设计使模型能够利用文本语义指导细节恢复，减少重建伪影。

### 训练策略与损失函数

模型采用**联合图像‑视频训练**策略，以 8:2 的视频‑图像比例采样数据。对于图像批次，时间模块被屏蔽，使模型同时保持强大的图像重建能力。总损失函数为三项的加权和：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{GAN}} \mathcal{L}_{\mathrm{GAN}}$$

其中 $\mathcal{L}_{\mathrm{recon}}$ 为重建损失，$\mathcal{L}_{\mathrm{KL}}$ 为 KL 散度损失以正则化潜空间，$\mathcal{L}_{\mathrm{GAN}}$ 为视频 3D GAN 损失以提升感知质量。消融实验表明，视频 3D GAN 损失相比图像 GAN 损失能显著改善重建质量（Table 4）。

### 与基线方法的架构差异

现有视频 VAE（如 Open‑Sora 的 OPS VAE、Open‑Sora‑Plan 的 OD VAE、CV‑VAE）通常直接将图像 VAE 的 2D 卷积膨胀为 3D 卷积进行同时空压缩，或采用先空间后时间的纯顺序压缩。前者在大运动下产生运动模糊和细节失真，后者则容易丢失纹理稳定性。Cross‑modal Video VAE 通过两阶段解耦设计同时规避了这两类问题，并引入文本跨模态信息作为额外引导，在 WebVid、Inter4K 及大运动测试集上均取得了显著优于基线的 PSNR/LPIPS 指标（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2412_17805/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of our optimal spatiotemporal modeling and the two other options. Simultaneous modeling is achieved by inflating pre-trained 2D spatial VAE to 3D VAE. Sequential modeling indicates first compressing the spatial dimension with a spatial encoder and then compressing the temporal information with a temporal encoder. We identify the issues of these two options and propose to combine both advantages and achieve a much better video reconstruction quality. Our VAE also benefits from cross-modality, i.e., text information*



### 视频自编码问题定义

给定输入视频张量 $\mathbf{X} \in \mathbb{R}^{C \times T \times H \times W}$（$C$ 为通道数，$T$ 为帧数，$H \times W$ 为空间分辨率），视频自编码的目标是学习编码器 $\mathcal{E}$ 和解码器 $\mathcal{D}$，使得：

$$\mathbf{Z} = \mathcal{E}(\mathbf{X}), \quad \hat{\mathbf{X}} = \mathcal{D}(\mathbf{Z}) \tag{1}$$

其中 $\mathbf{Z}$ 为压缩后的潜变量，$\hat{\mathbf{X}}$ 为重建视频。核心挑战在于同时压缩空间和时间维度，并在大运动场景下保持高保真重建。

### 两阶段时空建模

本文的核心创新在于提出**两阶段时空压缩策略**，融合“同时压缩”与“顺序压缩”各自的优势。如 Figure 2 所示，同时压缩（将 2D VAE 膨胀为 3D VAE）有利于保持细节和纹理稳定性，但大运动下容易产生模糊；顺序压缩（先空间后时间）有利于大运动恢复，但细节容易丢失。两阶段建模将二者结合：

**第一阶段：时间感知空间编码**。空间编码器 $\mathcal{E}_1$ 仅压缩空间维度（$H \times W$），不压缩时间维度，同时通过 3D 卷积捕获跨帧运动信息：

$$\mathbf{Z}_1 = \mathcal{E}_1(\mathbf{X}) \tag{2}$$

**第二阶段：轻量级时间压缩**。时间编码器 $\mathcal{E}_2$ 对中间潜变量 $\mathbf{Z}_1$ 进一步压缩时间冗余：

$$\mathbf{Z}_2 = \mathcal{E}_2(\mathbf{Z}_1) \tag{3}$$

**解码过程**。先由时间解码器 $\mathcal{D}_2$ 恢复时序维度，再由空间解码器 $\mathcal{D}_1$ 重建完整视频：

$$\hat{\mathbf{X}} = \mathcal{D}_1(\mathcal{D}_2(\mathbf{Z}_2)) = \mathcal{D}_1(\mathbf{Z}_1) \tag{4}$$

### 时间感知空间自编码器结构

Figure 3 展示了空间自编码器的具体架构。其核心构建块为 **STBlock3D**：将预训练 SD VAE 的 2D 卷积膨胀为 3D 卷积后，再追加一个额外的 3D 卷积作为时序卷积，形成时空联合感知能力。该模块在压缩空间信息的同时保留帧间运动特征，为大运动场景下的后续时间压缩提供高质量中间表示。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2412_17805/figures/003_Figure_3.jpg]]
*Figure 3: The architecture of our temporal-aware spatial autoencoder. We expand the 2D convolution of SD VAE [25] to 3D convolution and append one additional 3D convolution as temporal convolution after the expanded 3D convolution, which forms the STBlock3D. We also inject the cross-attention layers for crossmodal learning with textual conditions*

### 跨模态文本引导

在每个 ResNet 块之后，将视觉特征图切分为 patch token 作为 Query (Q) 和 Value (V)，以 Flan-T5 文本嵌入作为 Key (K)，通过交叉注意力注入语义信息。各层 patch 大小分别为 $8 \times 8$、$4 \times 4$、$2 \times 2$ 和 $1 \times 1$。文本引导帮助模型在重建时恢复更丰富的细节，如 Figure 5 所示。

### 训练损失函数

总损失为三项的加权和：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{KL}} \mathcal{L}_{\mathrm{KL}} + \lambda_{\mathrm{GAN}} \mathcal{L}_{\mathrm{GAN}} \tag{5}$$

其中 $\mathcal{L}_{\mathrm{recon}}$ 为重建损失，$\mathcal{L}_{\mathrm{KL}}$ 为潜变量分布的 KL 散度正则项，$\mathcal{L}_{\mathrm{GAN}}$ 为**视频 3D GAN 损失**（在时空维度上判别，优于图像 GAN 损失，如 Table 4 消融所示）。联合图像-视频训练时，视频与图像按 8:2 比例混合，图像批次通过屏蔽时序模块处理。



## 实验与关键发现

### 主实验结果

**Cross-modal Video VAE** 在 WebVid 测试集、Inter4K 测试集以及专门构建的大运动测试集上与多个强基线方法进行了全面对比，包括 **Open-Sora (OPS VAE)**、**Open-Sora-Plan (OD VAE)**、**CV-VAE** 以及 **CogVideoX**、**Cosmos Tokenizer** 等。Table 1 汇总了定量结果。

在 WebVid 测试集上，4 通道版本的 Cross-modal VAE 取得了 **PSNR 30.31 dB**、**SSIM 0.8676**、**LPIPS 0.0538**；16 通道版本进一步提升至 **PSNR 34.16 dB**、**SSIM 0.9362**、**LPIPS 0.0271**。相比 Open-Sora 的 PSNR 29.38 dB 和 LPIPS 0.1240，4 通道版本即实现了 **+0.73 dB** 的 PSNR 提升和 **-0.0696** 的 LPIPS 降低。在 Inter4K 和大运动测试集上，该方法同样保持了显著优势，表明解耦的时空建模策略对高动态场景具有更强的鲁棒性。

定性结果（Figure 1）进一步印证了定量结论：在体育动作等大运动场景下，基线方法普遍出现运动模糊、重影伪影和细节丢失，而 Cross-modal VAE 显著改善了运动恢复质量，大幅减少了鬼影效应。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2412_17805/figures/001_Figure_1.jpg]]
*Figure 1: Our reconstruction results compared with a line of three recent strong baseline approaches. The ground truth frame is (0). Our model significantly outperforms previous methods, especially under large motion scenarios such as people doing sports*

### 消融研究

#### 1. 时空压缩策略对比（Table 3, Figure 4）

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2412_17805/figures/007_Table_3.jpg]]
*Table 3: Ablation study comparing simultaneous modeling, sequential modeling, and ours on the large-motion test set*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2412_17805/figures/004_Figure_4.jpg]]
*Figure 4: Comparisons among simultaneous spatiotemporal modeling, sequential spatiotemporal modeling and our proposed solution*

为验证两阶段时空建模的有效性，论文在大运动测试集上对比了三种压缩范式：

- **同时压缩（Simultaneous）**：直接将预训练 2D VAE 膨胀为 3D VAE，空间和时间维度被耦合压缩。
- **顺序压缩（Sequential）**：先压缩空间维度，再压缩时间维度。
- **本文方案（Ours）**：时间感知空间编码 + 轻量级时间压缩模型。

定量结果表明，同时压缩在保持纹理稳定性方面有优势，但大运动恢复能力差；顺序压缩对运动恢复有利，但细节和纹理稳定性下降。本文方案结合两者优势，在 PSNR、SSIM 和 LPIPS 三项指标上均取得最优（Table 3）。Figure 4 的定性对比展示了这一优势：同时压缩产生运动模糊，顺序压缩出现纹理闪烁，而本文方案在运动清晰度和纹理一致性之间取得了更好的平衡。

#### 2. 联合图像-视频训练（Table 2, Figure 6）

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2412_17805/figures/006_Table_2.jpg]]
*Table 2: JT∗ means joint training. We evaluate image reconstruction performance w/ or w/o our joint image-video training strategy*

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2412_17805/figures/010_Figure_6.jpg]]
*Figure 6: The effectiveness of joint image and video training*

为验证联合训练策略的效果，论文对比了仅视频训练与联合图像-视频训练（视频:图像 = 8:2）下的图像重建性能。Table 2 显示，联合训练不仅在视频重建上表现更优，同时显著提升了图像重建的 PSNR 和 SSIM。这表明联合训练使模型在习得视频时序建模能力的同时，保留并增强了空间细节重建能力。Figure 6 的定性对比也显示，联合训练后的重建结果在纹理细节上明显优于仅视频训练的版本。

#### 3. GAN 损失与时间卷积核设计（Table 4）

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2412_17805/figures/009_Table_4.jpg]]
*Table 4: Ablation study comparing temporal-aware spatial autoencoder with image/video GAN loss, and different kernel sizes*

论文进一步消融了 GAN 损失类型和时间卷积核大小对重建质量的影响。Table 4 的结果表明：

- **视频 3D GAN 损失** 相比图像 GAN 损失在视频重建指标上有明显提升，验证了在时序维度上施加对抗训练的必要性。
- **更大的时间卷积核**（如 (7,3,3)）相比小核设计能更有效地捕获跨帧运动信息，进一步提升重建质量。

#### 4. 跨模态文本引导（Figure 5）

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2412_17805/figures/008_Figure_5.jpg]]
*Figure 5: The effectiveness of the cross-modal learning for our video VAE. The introduction of textural information improves the detail recovery. We visualize the learned attention map using keywords of the input prompts*

Figure 5 展示了跨模态文本条件对细节恢复的影响。引入 Flan-T5 文本嵌入后，模型在细节区域（如人脸、文字、纹理）的重建质量明显优于无文本条件的版本。论文还可视化了注意力图，显示模型能够准确关注到文本提示中的关键词所对应的视觉区域，验证了跨模态注意力机制的有效性。

### 失败模式与局限

论文未在原文中明确报告失败模式或系统性的局限性分析。从方法设计推断，两阶段时空建模在极端运动幅度或长视频序列下可能面临时间压缩瓶颈，且跨模态文本引导的效果依赖于文本标注质量。这些方面需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2412_17805/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with state-of-the-art methods*



## 定位与知识库关联

### 问题定位：从耦合时空压缩到解耦两阶段建模

现有视频VAE的核心瓶颈在于将图像VAE直接“膨胀”到3D所导致的时空压缩耦合。当视频包含大幅度运动时，同时压缩空间与时间维度会引入三类典型退化：运动模糊、细节失真和时序闪烁。本文提出的**Cross-modal Video VAE**将这一耦合拆解为两个阶段——时间感知的空间编码与轻量级时序压缩——并引入文本语义作为跨模态引导，从而在大运动场景下取得显著优于强基线（如Open-Sora、Open-Sora-Plan、CV-VAE）的重建质量。

### 方法谱系：与关键基线的结构性差异

#### 1. 相对同时压缩方法（Simultaneous Modeling）

同时压缩方法（如Open-Sora-Plan的OD VAE、Open-Sora的OPS VAE）将预训练2D VAE的卷积核直接膨胀为3D，同时对空间和时间维度进行下采样。这类方法在静态或小运动场景下表现尚可，但在大运动场景下会因运动模糊和鬼影伪影而严重退化（见Table 3和Figure 4）。其根本原因在于：空间细节的保持需要高分辨率特征，而时序压缩需要跨帧信息聚合，两者在同一卷积层中相互干扰。

Cross-modal Video VAE通过**时间感知空间编码器**（Temporal-aware Spatial Encoder）在第一阶段仅压缩空间维度，利用膨胀的3D卷积和STBlock3D捕获跨帧信息但不降低时间分辨率。这保留了空间细节的稳定性，避免了同时压缩带来的纹理损失。随后由轻量级**时间自编码器**（Temporal Autoencoder）独立处理时序冗余，实现解耦压缩。

#### 2. 相对顺序压缩方法（Sequential Modeling）

顺序压缩方法先用2D空间编码器逐帧压缩空间维度，再用时间编码器压缩时序。该方法对大运动恢复有一定优势，但逐帧独立编码忽略了帧间的空间关联，导致细节丢失和纹理不稳定（见Figure 4）。

Cross-modal Video VAE的“时间感知”设计弥补了这一缺陷：空间编码器中的3D卷积在压缩空间的同时感知跨帧运动信息，使得输出到时间编码器的中间潜变量Z₁已经携带了时序上下文。这融合了同时压缩的细节保持优势和顺序压缩的大运动恢复优势。

#### 3. 相对CV-VAE与Cosmos Tokenizer

CV-VAE和Cosmos Tokenizer代表了近期视频tokenizer的改进方向，但均未引入文本信息作为重建引导。Cross-modal Video VAE在空间编码器和解码器的每个ResNet块后注入**交叉注意力层**，以视觉token作为Q/V、Flan-T5文本嵌入作为K，使文本语义直接参与潜变量编码。这在大运动场景下显著改善了细节恢复（Figure 5），并减少了仅依赖视觉信号时的模糊和伪影。

#### 4. 训练策略的差异化贡献

Cross-modal Video VAE采用**联合图像-视频训练**（8:2的视频-图像比例），图像批次通过mask时序模块处理。Table 2表明，该策略使模型在保持强图像重建能力的同时学会处理视频数据，避免了纯视频训练导致的图像重建退化。这一设计在现有视频VAE工作中并不常见，多数方法（如Open-Sora系列）仅使用视频数据进行训练。

### 知识库定位与适用边界

**核心贡献**：将视频VAE的时空压缩从“耦合”推进到“解耦+跨模态”范式，证明了在大运动场景下，时间感知的空间编码与文本引导是两个正交且互补的改进维度。

**适用边界**：
- 该方法在包含大幅度运动（如体育场景）的视频上优势最为显著，在静态或小运动场景下相对基线的增益可能缩小（需人工验证，原文未提供按运动幅度分层的细粒度分析）。
- 跨模态文本引导的有效性依赖于输入视频配有准确描述文本；在无文本或文本质量差的场景下，该模块的贡献将减弱。
- 联合训练策略需要同时维护图像和视频数据集，对数据工程有一定要求。

**局限与开放问题**：
- 原文未报告推理延迟和显存占用的系统级对比，两阶段架构和交叉注意力模块的计算开销需人工评估。
- 时间编码器的压缩比和潜变量通道数（4通道 vs 16通道）对下游生成任务（如视频扩散模型）的影响未在本文中充分探讨。
- 文本引导的注意力机制在大运动模糊帧上的鲁棒性（如文本描述与实际视觉内容不匹配时）未经验证。



## 原文 PDF

![[paperPDFs/arxiv_2024/Large_Motion_Video_Autoencoding_with_Cross_modal_Video_VAE.pdf]]
