---
title: "FA-VAE: Frequency-Aware Variational Autoencoder"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/FA-VAE_Frequency-Aware_Variational_Autoencoder.pdf
project_link: null
code_link: null
aliases:
- FV
- FA-VAE
tags:
- arxiv_2025
- topic/vision_multimodal_applications
core_operator: 通过离散小波变换将输入图像解耦为低频和高频分量，并对这两个分量使用独立的编码器-解码器分别优化，再通过逆小波变换和潜变量融合重建高保真图像。
primary_logic: 频率感知的变分自编码器（FA-VAE）显式解耦低频和高频子带的学习，使得模型能够同时保留全局结构（低频）和精细纹理（高频），从而在重建和生成任务中均获得更真实的视觉质量。
claims:
- 传统VAE损失函数天然优先优化低频分量，损害高频保真度
- FA-VAE在50k张ImageNet验证集上显著降低了高频区域的残余能量，残余功率谱更低
- FA-VAE的重建损失（0.0044）几乎是VA-VAE（0.0105）的一半，同时在LPIPS、rFID等感知指标上全面领先
- ImageNet 256×256 (reconstruction) 上 Reconstruction Loss (MSE) = 0.0044 (FA-VAE)
---

# FA-VAE: Frequency-Aware Variational Autoencoder

> [!tip] 核心洞察
> 频率感知的变分自编码器（FA-VAE）显式解耦低频和高频子带的学习，使得模型能够同时保留全局结构（低频）和精细纹理（高频），从而在重建和生成任务中均获得更真实的视觉质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 频率感知变分自编码器 |
| 英文题名 | FA-VAE: Frequency-Aware Variational Autoencoder |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2509.05441) |
| Topic | #topic/vision_multimodal_applications |
| Method | FA-VAE |
| Dataset | ImageNet 256×256 |

> [!tip] 效果简介
> - ImageNet 256×256 (reconstruction) 上，Reconstruction Loss (MSE) 0.0044 (FA-VAE) vs 0.0105 (VA-VAE) (-0.0061)；LPIPS 0.0940 (FA-VAE) vs 0.0975 (VA-VAE) (-0.0035)；rFID 0.4156 (FA-VAE) vs 0.4884 (VA-VAE) (-0.0728)。
> - ImageNet 256×256 (generation w/ CFG) 上，gFID 1.32 (LightningDiT + FA-VAE) vs 1.55 (MAR with KL-VAE; no direct LightningDiT+VA-VAE reported) (-0.23)。

## 概要

现有潜变量生成模型（如潜在扩散模型）依赖VAE分词器将图像压缩至低维潜空间。然而，传统VAE的优化目标天然偏向低频信息重建，导致重建图像丢失高频纹理与锐利边缘，视觉上呈现过度平滑。这一瓶颈直接限制了后续生成模型的上限——无论扩散模型或自回归模型如何改进，若潜表示本身缺乏高频保真度，生成结果必然细节模糊。

**FA-VAE**（Frequency-Aware Variational Autoencoder）针对上述瓶颈提出了频率感知的解耦学习框架。其核心思路是：通过离散小波变换将输入图像显式分解为低频子带（LL）和高频子带（LH, HL, HH），分别由独立的编码器-解码器对进行优化，最后通过逆小波变换与潜变量融合重建高保真图像。这一设计使得低频分支专注于全局结构，高频分支专注于纹理细节，从根本上绕开了传统VAE优化偏好的限制。

在ImageNet 256×256验证集上，FA-VAE的重建损失（MSE）仅为0.0044，近乎**VA-VAE**（Yao, Yang, and Wang, CVPR 2025）的0.0105的一半；感知指标LPIPS从0.0975降至0.0940，rFID从0.4884降至0.4156。频域分析进一步证实，FA-VAE在50k张图像上的残余功率谱显著低于VA-VAE，尤其在高频区域。将FA-VAE的融合潜表示接入LightningDiT进行生成时，gFID达到1.32，优于同类配置的基线方法。

在方法谱系上，FA-VAE属于**频率感知潜变量分词器**，与标准VAE（**KL-VAE**, Rombach et al., CVPR 2022）、矢量量化VAE（**VQ-VAE**, Van Den Oord et al., NeurIPS 2017）以及视觉基础模型对齐的VAE（**VA-VAE**）形成对比。其关键差异在于显式的频率解耦与差异化的训练目标：低频分支沿用VA-VAE风格损失（含DINOv2对齐），高频分支仅使用L1重构、KL散度与对抗损失，避免预训练模型监督引入低频偏向。



### 潜变量生成模型中的重建瓶颈

现代高分辨率图像生成系统普遍采用两阶段范式：先训练一个变分自编码器（VAE）将图像压缩到低维潜空间，再在该潜空间上训练扩散模型或自回归模型。VAE分词器的重建质量直接决定了生成图像的保真度上限——如果分词器在编码-解码过程中丢失了关键的视觉信息，后续生成模型无论如何优化都无法恢复这些细节。

然而，现有VAE分词器面临一个根本性的优化偏向问题：**标准训练目标天然优先优化低频分量，以牺牲高频保真度为代价**。这一现象在频域分析中尤为明显——如Figure 2所示，在50k张ImageNet验证集上的残余功率谱表明，当前性能最强的VA-VAE分词器（Yao, Yang, and Wang, CVPR 2025）在高频区域表现出显著更高的残余能量，意味着重建图像丢失了大量纹理和边缘细节。从视觉上看（Figure 1），这种高频损失导致重建图像呈现过度平滑的外观，在纹理丰富区域、锐利边缘和文字等结构上尤为突出。

### 现有方法的局限性

当前主流的潜变量分词器可以归纳为以下几类，但均未能有效解决频率偏向问题：

- **KL-VAE**（Rombach et al., CVPR 2022）：作为Stable Diffusion的基础分词器，采用标准的VAE架构，其MSE重建损失和KL正则化天然倾向于拟合占据图像能量主体的低频成分，高频细节在优化过程中被系统性忽视。
- **VQ-VAE**（Van Den Oord et al., NeurIPS 2017）：通过向量量化学习离散潜表示，虽然离散编码有助于后续自回归建模，但其重建目标同样未区分频率分量，高频保真度受限。
- **VA-VAE**（Yao, Yang, and Wang, CVPR 2025）：当前最先进的连续潜变量分词器，通过引入视觉基础模型对齐损失（如DINOv2）和感知损失来改善重建质量。尽管在整体指标上表现优异，但从Figure 2的残余功率谱可以清晰看到，其高频区域的残余能量仍然显著，说明仅靠更强的损失函数设计无法从根本上解决优化过程中的频率偏向问题。

### 核心动机：从频域解耦到显式频率感知

本文的核心洞察在于：**与其让单一编码器-解码器在耦合的频率信息上隐式地平衡优化，不如显式地将频率分量解耦，为不同频带设计专门的表示学习路径**。具体而言：

1. **频域解耦的物理基础**：通过离散小波变换（DWT）将输入图像分解为低频子带（LL）和高频子带（LH, HL, HH）。低频子带承载全局结构和色彩分布，高频子带编码纹理、边缘和局部细节——两者在信息特性和优化需求上截然不同。

2. **差异化优化策略**：低频分量适合使用强监督信号（如视觉基础模型对齐、感知损失）来保持语义一致性；而高频分量若同样引入预训练模型监督，反而会引入额外的低频偏向（因为视觉基础模型本身对高频纹理不敏感）。因此，高频分支仅采用L1重建损失和对抗正则化，避免外部模型带来的偏向。

3. **统一潜表示的融合**：解耦学习后，通过逆小波变换恢复完整图像，同时在潜空间层面将低频和高频潜变量拼接融合，为下游扩散模型提供同时包含全局结构和精细细节的统一表示。

这一设计从根本上改变了VAE分词器的优化格局——不再让高频细节在损失函数中"被平均掉"，而是赋予其独立的表示学习通道和定制化的训练目标。



## 核心方法与创新机理

FA-VAE 的核心创新在于**显式解耦并独立优化潜变量嵌入的低频与高频分量**，从而突破传统 VAE 分词器在重建中天然偏向低频信息、导致高频纹理丢失的瓶颈。这一目标通过三个紧密耦合的机制实现：频率分解、分频独立优化、以及潜变量融合。

### 频率分解：从像素域到小波域

传统 VAE 分词器（如 **KL-VAE** (Rombach et al., CVPR 2022) 和 **VA-VAE** (Yao, Yang, and Wang, CVPR 2025)）直接在原始像素图像上学习潜表示。由于均方误差（MSE）等重构损失天然优先拟合能量占优的低频分量，高频细节在优化过程中被系统性牺牲，导致重建图像过度平滑（Figure 1、Figure 2 提供了视觉和频谱证据）。

FA-VAE 将输入表示从像素域切换至小波域：对输入图像 $\mathbf{x}$ 应用离散小波变换（DWT），采用 Haar 小波将其分解为低频子带 $\mathbf{x}_L$ 和高频子带 $\mathbf{x}_H$（包含 LH、HL、HH 三个方向分量）：

$$\mathcal{W}(\mathbf{x}) = (\mathbf{x}_L, \mathbf{x}_H)$$

这一分解将频率维度的学习从隐式变为显式，为后续的分频独立优化提供了结构基础。

### 分频独立优化：双编码器-解码器架构

FA-VAE 的核心架构变更在于**用两对独立的编码器-解码器替代传统的单对架构**：低频编码器 $E_L$ 与解码器 $D_L$ 处理 $\mathbf{x}_L$，高频编码器 $E_H$ 与解码器 $D_H$ 处理 $\mathbf{x}_H$，分别学习频率特定的潜嵌入 $\mathbf{z}_L$ 和 $\mathbf{z}_H$。

更关键的是，两个分支采用**差异化的训练目标**：

- **低频分支**沿用 VA-VAE 的完整损失体系，包括重构损失、KL 散度、视觉基础模型对齐（VF loss）、对抗损失和感知损失（LPIPS），以保留全局结构和语义一致性：

$$\mathcal{L}_{\mathrm{low}} = \mathcal{L}_{\mathrm{rec}}^L + \beta \cdot \mathcal{L}_{\mathrm{KL}}^L + \lambda_{\mathrm{VF}} \cdot \mathcal{L}_{\mathrm{VF}}^L + \lambda_{\mathrm{GAN}} \cdot \mathcal{L}_{\mathrm{GAN}}^L + \lambda_{\mathrm{LPIPS}} \cdot \mathcal{L}_{\mathrm{LPIPS}}^L$$

- **高频分支**则有意**不引入预训练视觉基础模型的监督**，仅使用 L1 重构损失、KL 散度和对抗损失，以避免预训练模型本身可能存在的低频偏向污染高频学习：

$$\mathcal{L}_{\mathrm{high}} = \mathcal{L}_{\mathrm{rec}}^H + \beta \cdot \mathcal{L}_{\mathrm{KL}}^H + \mathcal{L}_{\mathrm{GAN}}^H$$

这一设计选择体现了方法对因果机制的深刻理解：高频细节的保真度不应被外部语义模型的标准所约束，而应通过直接的重构和对抗信号来驱动。

### 潜变量融合：统一表示供生成模型使用

在推理阶段，低频和高频解码器分别重建 $\hat{\mathbf{x}}_L$ 和 $\hat{\mathbf{x}}_H$，再通过逆小波变换（IDWT）合成完整图像：

$$\hat{\mathbf{x}} = \mathcal{W}^{-1}(\hat{\mathbf{x}}_L, \hat{\mathbf{x}}_H)$$

对于生成任务，FA-VAE 通过简单的拼接操作将 $\mathbf{z}_L$ 和 $\mathbf{z}_H$ 融合为统一的潜表示 $\tilde{\mathbf{z}}$，供下游扩散模型（如 LightningDiT）使用：

$$\tilde{\mathbf{z}} = \mathcal{F}(\mathbf{z}_L, \mathbf{z}_H)$$

这一融合策略保持轻量，避免引入额外的计算开销，同时确保生成模型能够同时访问低频结构信息和高频纹理信息。

### 相对于 baseline 的关键变更总结

| 变更维度 | VA-VAE / KL-VAE（baseline） | FA-VAE（proposed） |
|---------|--------------------------|-------------------|
| 输入表示 | 原始像素图像 | 经 Haar 小波分解的低频（LL）和高频（LH, HL, HH）子带 |
| 编码器-解码器 | 单对编码器-解码器 | 两对独立编码器-解码器，分别处理低频和高频分量 |
| 高频训练目标 | 与低频相同（MSE + 感知 + VF 对齐） | 仅 L1 重构 + KL + 对抗，无预训练模型监督 |
| 潜变量融合 | 无融合，直接使用单一潜变量 | 拼接低频与高频潜变量为统一表示 |

这些变更共同构成了 FA-VAE 的“因果旋钮”：通过在小波域显式分离频率分量，并为高频学习设计不受低频偏向污染的训练目标，模型得以在保留全局结构的同时显著提升纹理和边缘的保真度。Table 1 的定量结果表明，FA-VAE 的重建损失（0.0044）几乎是 VA-VAE（0.0105）的一半，LPIPS 和 rFID 也全面领先，验证了频率感知解耦设计的有效性。



FA-VAE 的整体设计遵循“频率解耦—独立编码—融合重建”的流水线。其核心动机来自一个被实验验证的观察：标准 VAE 的优化目标天然偏向低频分量，导致重建图像丢失高频纹理与锐利边缘。为解决这一问题，FA-VAE 显式地将输入图像的低频与高频子带分离，并分别为其分配独立的编码器-解码器对，从而阻断低频对高频学习的压制。

### 流水线模块与数据流

1. **离散小波变换（DWT）**  
   输入图像 $\mathbf{x}$ 首先通过一级 Haar 小波变换分解为四个子带：
   $$ \mathcal{W}(\mathbf{x}) = (\mathbf{x}_L, \mathbf{x}_H) $$
   其中 $\mathbf{x}_L$ 为低频子带（LL），承载全局结构与主体色调；$\mathbf{x}_H$ 为三个高频子带（LH, HL, HH）的组合，承载边缘、纹理等细节信息。

2. **低频编码器-解码器**  
   低频子带 $\mathbf{x}_L$ 送入低频编码器 $E_L$，得到低频潜变量 $\mathbf{z}_L = E_L(\mathbf{x}_L)$；随后低频解码器 $D_L$ 从中重建低频分量 $\hat{\mathbf{x}}_L = D_L(\mathbf{z}_L)$。该分支采用 VA-VAE 风格的复合损失，包含重建损失、KL 散度、视觉基础模型对齐（如 DINOv2）、对抗损失与感知损失（LPIPS），以充分保留全局语义与结构。

3. **高频编码器-解码器**  
   高频子带 $\mathbf{x}_H$ 送入高频编码器 $E_H$，得到高频潜变量 $\mathbf{z}_H = E_H(\mathbf{x}_H)$；高频解码器 $D_H$ 从中重建高频分量 $\hat{\mathbf{x}}_H = D_H(\mathbf{z}_H)$。高频分支的训练目标被有意简化，仅使用 L1 重构损失、KL 散度与对抗损失，**不引入预训练模型监督**，以避免低频偏向再次渗透到高频学习中。

4. **逆小波变换（IDWT）**  
   将解码后的低频与高频子带通过逆小波变换合成为完整重建图像：
   $$ \hat{\mathbf{x}} = \mathcal{W}^{-1}(\hat{\mathbf{x}}_L, \hat{\mathbf{x}}_H) $$

5. **潜变量融合**  
   为适配下游生成模型，低频潜变量 $\mathbf{z}_L$ 与高频潜变量 $\mathbf{z}_H$ 通过简单的拼接操作融合为统一的生成用潜表示：
   $$ \tilde{\mathbf{z}} = \mathcal{F}(\mathbf{z}_L, \mathbf{z}_H) $$
   融合后的 $\tilde{\mathbf{z}}$ 直接输入 LightningDiT 等潜在扩散模型进行高分辨率图像生成。

### 模块间关系

整个框架中，低频与高频分支在训练阶段完全解耦，各自优化频率特定的潜嵌入；仅在推理阶段通过逆小波变换在像素空间汇合，或在生成阶段通过潜变量拼接在潜空间汇合。这种设计使得模型能够同时保留全局结构（低频）与精细纹理（高频），从根源上缓解了标准 VAE 分词器因频率偏向导致的过度平滑问题。

**关键证据**：在 50k 张 ImageNet 验证集上的残余功率谱分析（Figure 2）显示，FA-VAE 的残余能量在全频段均显著低于 VA-VAE，尤其在高频区域的降低更为明显，直接验证了频率解耦策略对高频保真度的提升效果。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our proposed frequency-aware VAE framework (FA-VAE). An input image is decomposed into low- and highfrequency representations using a wavelet transform. Each frequency band is decoupled, encoded and decoded separately to learn dedicated latent embeddings, which are then coupled and passed through an inverse wavelet transform to reconstruct the image. These enriched embeddings are subsequently used in a latent diffusion model to improve generation fidelity, particularly preserving fine details*



### 频率感知变分自编码器（FA-VAE）框架

FA-VAE 的核心设计在于将标准 VAE 的优化过程从耦合的像素空间解耦为独立的频率子带学习。给定输入图像 $\mathbf{x} \in \mathcal{X}$，首先通过离散小波变换（Discrete Wavelet Transform, DWT）将其分解为低频和高频分量：

$$\mathcal{W}(\mathbf{x}) = (\mathbf{x}_L, \mathbf{x}_H)$$

其中 $\mathbf{x}_L$ 为低频子带（LL），$\mathbf{x}_H$ 为高频子带集合（LH, HL, HH），使用 Haar 小波滤波器实现。随后，这两类分量分别由独立的编码器-解码器对处理：

$$\mathbf{z}_L = E_L(\mathbf{x}_L), \quad \mathbf{z}_H = E_H(\mathbf{x}_H)$$

$$\hat{\mathbf{x}}_L = D_L(\mathbf{z}_L), \quad \hat{\mathbf{x}}_H = D_H(\mathbf{z}_H)$$

最终通过逆小波变换（IDWT）将解码后的子带恢复为完整重建图像：

$$\hat{\mathbf{x}} = \mathcal{W}^{-1}(\hat{\mathbf{x}}_L, \hat{\mathbf{x}}_H)$$

### 低频分支训练目标

低频分支负责保留图像的全局结构和语义信息，采用与 VA-VAE（Yao, Yang, and Wang, CVPR 2025）一致的多目标损失函数：

$$\mathcal{L}_{\mathrm{low}} = \mathcal{L}_{\mathrm{rec}}^L + \beta \cdot \mathcal{L}_{\mathrm{KL}}^L + \lambda_{\mathrm{VF}} \cdot \mathcal{L}_{\mathrm{VF}}^L + \lambda_{\mathrm{GAN}} \cdot \mathcal{L}_{\mathrm{GAN}}^L + \lambda_{\mathrm{LPIPS}} \cdot \mathcal{L}_{\mathrm{LPIPS}}^L$$

其中：
- $\mathcal{L}_{\mathrm{rec}}^L$ 为低频子带的重构损失（MSE）
- $\mathcal{L}_{\mathrm{KL}}^L$ 为 KL 散度正则项，约束潜变量分布接近标准正态分布
- $\mathcal{L}_{\mathrm{VF}}^L$ 为视觉基础模型对齐损失，利用预训练模型（如 DINOv2）监督语义一致性
- $\mathcal{L}_{\mathrm{GAN}}^L$ 为对抗损失，提升重建图像的逼真度
- $\mathcal{L}_{\mathrm{LPIPS}}^L$ 为感知损失，衡量高层特征差异
- $\beta, \lambda_{\mathrm{VF}}, \lambda_{\mathrm{GAN}}, \lambda_{\mathrm{LPIPS}}$ 为各损失项的权重系数

### 高频分支训练目标

高频分支专注于纹理、边缘等细节信息的重建。为避免预训练模型监督引入低频偏向，高频分支仅使用轻量级损失组合：

$$\mathcal{L}_{\mathrm{high}} = \mathcal{L}_{\mathrm{rec}}^H + \beta \cdot \mathcal{L}_{\mathrm{KL}}^H + \mathcal{L}_{\mathrm{GAN}}^H$$

其中 $\mathcal{L}_{\mathrm{rec}}^H$ 采用 L1 重构损失，配合对抗损失 $\mathcal{L}_{\mathrm{GAN}}^H$ 增强高频细节的真实性，不引入 $\mathcal{L}_{\mathrm{VF}}$ 或 $\mathcal{L}_{\mathrm{LPIPS}}$ 等依赖预训练模型的监督信号。

### 潜变量融合模块

为将频率解耦的潜变量统一用于下游生成任务，FA-VAE 采用拼接（concatenation）操作作为融合函数：

$$\tilde{\mathbf{z}} = \mathcal{F}(\mathbf{z}_L, \mathbf{z}_H)$$

其中 $\mathcal{F}$ 表示简单的拼接操作，将低频潜变量 $\mathbf{z}_L$ 和高频潜变量 $\mathbf{z}_H$ 在通道维度拼接，形成统一的生成用潜表示 $\tilde{\mathbf{z}}$。该融合表示随后被送入 LightningDiT 等潜在扩散模型进行高分辨率图像生成。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/002_Figure_2.jpg]]
*Figure 2: Residual power spectra averaged over 50k ImageNet validation images, comparing reconstruction errors (input minus reconstruction) of VAVAE and our method. The log-scaled spectra show that VAVAE exhibits higher residual energy across the frequency spectrum, particularly in high-frequency regions. In contrast, our method significantly reduces reconstruction residual energy, indicating better preservation of fine details and textures*



## 实验与关键发现

### 核心发现：频率感知解耦带来的重建质量跃升

FA-VAE 在 ImageNet 256×256 验证集上的重建性能全面超越现有最优分词器。**Table 1** 汇总了与多种潜变量分词器的定量对比，FA-VAE 在全部指标上取得最佳结果。最关键的数据是：FA-VAE 的重建损失（MSE）为 0.0044，几乎是此前最强的 **VA-VAE**（Yao, Yang, and Wang, CVPR 2025）的 0.0105 的一半。这一大幅降幅直接验证了论文的核心假设——传统 VAE 损失函数天然偏向低频优化，而显式解耦频率分量能够从根本上缓解高频细节的丢失。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison of various latent tokenizers based on their reconstruction quality across multiple metrics. Tokenizer configurations are denoted as: f : latent spatial resolution, c: latent dimensionality, and v: vocabulary size in case of quantized models. Lower values indicate better performance*

在感知质量指标上，FA-VAE 同样领先：LPIPS 降至 0.0940（VA-VAE 为 0.0975），rFID 降至 0.4156（VA-VAE 为 0.4884，降幅达 0.0728）。rFID 的显著改善尤为值得关注，因为它衡量的是重建图像与原始图像在特征空间中的分布差异，说明频率感知建模不仅提升了像素级精度，更带来了整体视觉真实感的增强。

**Figure 2** 从频域角度提供了机制层面的证据。该图展示了在 50k 张 ImageNet 验证图像上平均的残差功率谱（输入减重建的对数尺度频谱）。VA-VAE 在整个频谱上表现出更高的残差能量，尤其在高频区域更为突出；而 FA-VAE 显著降低了残差能量，特别是在高频部分。这一频域分析直接证实了方法设计的有效性：独立的低频和高频编码器-解码器对确实让模型能够分别优化不同频率分量的重建。

### 生成任务中的迁移效果

将 FA-VAE 作为分词器集成到 **LightningDiT**（Yao, Yang, and Wang, CVPR 2025）扩散模型中，在 ImageNet 256×256 的类别条件生成任务上同样展现出竞争力。**Table 2** 显示，LightningDiT + FA-VAE 在使用无分类器引导（CFG）时，gFID 达到 1.32。作为参考，MAR 搭配 KL-VAE 的 gFID 为 1.55。需要注意的是，原文并未直接报告 LightningDiT + VA-VAE 的 gFID，因此无法进行严格的同架构对比，但 FA-VAE 在该生成框架下的表现仍具参考价值。**Figure 4** 展示了生成样本的可视化效果。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/006_Table_2.jpg]]
*Table 2: Comparision of generation performance of autoregressive and latent diffusion models with and without classifier-free guidance (CFG) vs LightningDiT with our FA-VAE tokenizer. Missing values are indicated by -. We report metrics only available in the respective works*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/005_Figure_4.jpg]]
*Figure 4: Generated Visualization of our proposed FA-VAE together with LightningDiT-XL trained on ImageNet 256 × 256 resolution*

### 消融实验：小波表示本身不足以解释全部增益

一个自然的问题是：FA-VAE 的性能提升是否仅仅源于在小波域而非像素域进行操作？**Table 3** 的消融实验回答了这个问题。实验对比了多种分词器在输入小波表示（而非原始像素）下的重建性能，涵盖 Rec（总重建损失）、LF（低频损失）和 HF（高频损失）三个指标。结果显示，FA-VAE 在全部指标上均优于耦合频率的变体。这表明，单纯的频率变换不足以带来实质性改进，关键在于 FA-VAE 对低频和高频子带的**独立编码-解码与差异化训练目标**：低频分支采用包含视觉基础模型对齐的完整损失函数，而高频分支仅使用 L1 重建损失、KL 散度和对抗损失，刻意避免预训练模型监督可能引入的低频偏向。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/007_Table_3.jpg]]
*Table 3: Reconstruction comparison of tokenizers with input wavelet representation instead of input pixel representation. Rec.: Reconstruction Loss, LF: Low Frequency Loss, HF: High Frequency Loss. Lower is better*

### 公平性分析：复杂类别上的稳健性

**Figure 5** 展示了 ImageNet 中重建误差最高的 100 个类别上的类别级对比。这些类别通常包含复杂的纹理、边缘或文字等高频信息。FA-VAE 在这些挑战性类别上的归一化均方误差（NMSE）持续低于 VA-VAE。这一结果表明，频率感知建模不仅提升了平均性能，还为结构复杂的图像提供了更公平、更稳健的潜表示——传统分词器在这些类别上往往表现最差，而 FA-VAE 有效缩小了这一差距。

### 局限性与待验证问题

尽管实验结果令人信服，但以下方面仍需注意或进一步验证：

1. **数据集规模有限**：全部实验在 ImageNet 上完成。论文自身指出在更大规模、更多样化的数据集上可能表现更优，但这一假设尚未得到验证。
2. **低频分支的外部依赖**：低频训练目标依赖预训练视觉基础模型（如 DINOv2）的对齐损失，这引入了外部偏差，并限制了在缺乏此类模型的场景中的直接适用性。
3. **频率分解策略固定**：当前采用 1 级 Haar 小波分解，可能并非所有场景下的最优选择。可学习的多级小波分解或自适应频率选择是值得探索的方向。
4. **生成模型的迁移范围有限**：生成实验仅在 LightningDiT 上进行，在其他扩散模型或自回归模型上的迁移效果尚待考察。
5. **融合策略简单**：潜变量融合采用直接拼接，交叉注意力等更具表现力的融合机制是否能进一步提升生成质量，仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/001_Figure_1.jpg]]
*Figure 1: Visual comparison of reconstructions. From left to right: original image, VAVAE reconstruction, and our approach. The highlighted regions emphasize areas rich in textures, edges, and text. Our method better preserves high-frequency details and sharp structures, resulting in reconstructions visually closer to the input*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/008_Figure_5.jpg]]
*Figure 5: Top-100 classes by reconstruction error. Our model shows consistently lower MSE across challenging categories*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/009_Table_4.jpg]]
*Table 4: Comparison of tokenizers on the ImageNet validation set across frequency-aware and perceptual metrics. Lower values indicate better performance. f denotes the latent spatial downsampling factor (e.g., f=16 implies 16× downsampling in width and height), and c denotes the number of latent channels. For VQ models, v indicates the vocabulary size. ∗ Models trained on ImageNet, SAM, FFHQ, and Mapillary Vistas. † Models trained on OpenImages. ‡ Models fine-tuned on OpenImages and LAION*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/012_Figure_8.jpg]]
*Figure 8: Qualitative reconstructions using our proposed FA-VAE on ImageNet 256×256*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/010_Figure_6.jpg]]
*Figure 6: Qualitative reconstructions using KL-VAE on ImageNet 256×256*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2509_05441/figures/011_Figure_7.jpg]]
*Figure 7: Qualitative reconstructions using VA-VAE on ImageNet 256×256*



## 定位与知识库关联

### 与基线方法的关系

FA-VAE 直接构建在 **VA-VAE**（Yao, Yang, and Wang, CVPR 2025）的框架之上，后者是当前潜变量分词器的 state-of-the-art，通过视觉基础模型对齐来提升潜表示质量。FA-VAE 的核心改进在于引入频率感知的显式解耦：将输入图像经离散小波变换（Haar 小波）分解为低频子带（LL）和高频子带（LH, HL, HH），并为两个频段分别配备独立的编码器-解码器对。低频分支保留了 VA-VAE 的完整训练目标（含 DINOv2 等视觉基础模型对齐损失），而高频分支则采用更轻量的 L1 重构损失加对抗正则化，刻意避免预训练模型的监督以规避低频偏向。

与传统的 **KL-VAE**（Rombach et al., CVPR 2022）和 **VQ-VAE**（Van Den Oord et al., NeurIPS 2017）相比，FA-VAE 在方法层面的关键差异在于：
- **频率解耦**：传统 VAE 分词器使用单对编码器-解码器处理整幅图像，其 MSE 驱动的优化天然偏向低频分量，导致高频纹理和锐利边缘丢失。FA-VAE 通过小波分解将这一隐式偏向转化为显式的双分支架构，使高频信息获得独立的优化通道。
- **潜变量融合**：FA-VAE 将低频潜变量 $\mathbf{z}_L$ 和高频潜变量 $\mathbf{z}_H$ 通过拼接操作 $\tilde{\mathbf{z}} = \mathcal{F}(\mathbf{z}_L, \mathbf{z}_H)$ 融合为统一的潜表示，供下游扩散模型使用。这一设计使生成模型能够同时访问全局结构信息和精细纹理信息。

在生成实验方面，FA-VAE 作为分词器被集成到 **LightningDiT**（Yao, Yang, and Wang, CVPR 2025）这一快速收敛的潜扩散模型中。Table 2 显示，LightningDiT + FA-VAE 在 ImageNet 256×256 上的 gFID 达到 1.32（with CFG），优于 MAR + KL-VAE 的 1.55。但需要注意的是，原文未直接报告 LightningDiT + VA-VAE 的生成指标，因此 FA-VAE 相对于 VA-VAE 在生成任务上的增益尚需进一步验证。

### 适用边界

FA-VAE 的适用边界由以下几个设计选择所界定：

**数据域边界**：所有实验均在 ImageNet 256×256 上完成。虽然原文推测在更大规模、更多样化的数据集上可能表现更优，但这一断言缺乏实验支撑，需要手动验证。在分布外场景（如医学影像、遥感图像、高压缩率文本图像）上的泛化能力尚不明确。

**架构依赖边界**：
- 低频分支依赖预训练视觉基础模型（如 DINOv2）的对齐损失 $\mathcal{L}_{\mathrm{VF}}^L$，这引入了外部模型偏差，并且限制了在没有合适预训练模型时的直接适用性。
- 小波分解固定为 1 级 Haar 小波。Haar 小波具有计算高效的优势，但其频率选择性有限，可能不是纹理复杂场景下的最优分解方式。原文未探索其他小波基（如 Daubechies）或多级分解。
- 潜变量融合策略采用简单的拼接操作，未引入交叉注意力等更具表现力的融合机制。这限制了高低频潜变量之间交互建模的能力。

**生成框架边界**：生成实验仅在 LightningDiT 这一优化的 DiT 架构上进行了验证。FA-VAE 的融合潜表示在其他扩散模型（如标准 DiT、U-Net 类扩散模型）或自回归模型上的迁移性和收益尚未被验证，这一结论点需要读者自行评估。

### 局限与开放问题

**已明确的局限**：
1. **数据集规模局限**：仅在 ImageNet 上验证了频率感知嵌入的有效性，缺乏更大规模、更多样化数据集上的实验证据。
2. **预训练模型依赖**：低频分支的对齐损失依赖外部视觉基础模型，增加了训练复杂度和外部偏差风险。
3. **固定频率分解**：1 级 Haar 小波可能不是最优的频率分解策略，限制了方法在更复杂纹理场景下的表现上限。
4. **生成模型泛化性未验证**：仅在 LightningDiT 上测试了生成性能，在其他生成范式下的收益未知。

**开放问题**：
1. **自适应频率分解**：能否学习或自适应选择最优的小波类型、分解级数和频带划分策略？可学习的小波变换或频域注意力机制可能是值得探索的方向。
2. **跨模态扩展**：频率感知的潜表示学习框架能否推广到视频生成（时空频率解耦）、3D 内容生成（几何与纹理频率解耦）等多模态任务？
3. **融合策略改进**：拼接操作是否能被交叉注意力或频域门控机制所替代，以实现高低频潜变量之间更丰富的交互？
4. **高频分支增强**：高频分支目前仅使用 L1 + 对抗损失，是否可以与边缘检测、纹理描述符等显式感知线索结合，进一步提升细节生成质量？



## 原文 PDF

![[paperPDFs/arxiv_2025/FA-VAE_Frequency-Aware_Variational_Autoencoder.pdf]]
