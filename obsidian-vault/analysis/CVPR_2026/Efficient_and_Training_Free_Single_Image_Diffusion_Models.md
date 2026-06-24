---
title: Efficient and Training-Free Single-Image Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Efficient_and_Training_Free_Single_Image_Diffusion_Models.pdf
project_link: "https://haojunqiu.github.io/efficient-SID/"
code_link: null
aliases:
- ETFSIDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 用有限图像块数据集上的封闭形式最优去噪器替代神经网络训练，从而将生成过程简化为无训练的加权平均。
primary_logic: 单张图像的图像块集合是有限且低维的，其分数函数可通过解析的加权高斯核精确计算，无需参数学习，进而将扩散生成还原为高效的非局部均值过程。
claims:
- 方法训练时间为零，而 SinDDM 需 10 小时（TITAN RTX）
- SIFID 指标达到 0.29±0.39，优于 SinDDM 的 0.48±0.62
- 封闭形式去噪器（式 2）在无训练条件下提供最优 MMSE 估计，数学上等价于以每个图像块为中心的 GMM
- 15幅自然图像（约250×250分辨率） 上 SIFID↓ = 0.29±0.39 (T=10, η=0)
---

# Efficient and Training-Free Single-Image Diffusion Models

> [!tip] 核心洞察
> 单张图像的图像块集合是有限且低维的，其分数函数可通过解析的加权高斯核精确计算，无需参数学习，进而将扩散生成还原为高效的非局部均值过程。

| 字段 | 内容 |
|------|------|
| 中文题名 | 高效且无需训练的单图像扩散模型 |
| 英文题名 | Efficient and Training-Free Single-Image Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Qiu_Efficient_and_Training-Free_Single-Image_Diffusion_Models_CVPR_2026_paper.html) · [Project](https://haojunqiu.github.io/efficient-SID/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Efficient and Training-Free Single-Image Diffusion Model |
| Dataset | 15幅自然图像（约250×250分辨率）, 推理时间（A6000, 186×248图像）, 高分辨率生成（308 MP 输入 → 1 GP 输出） |

> [!tip] 效果简介
> - 15幅自然图像（约250×250分辨率） 上，SIFID↓ 0.29±0.39 (T=10, η=0) vs 0.48±0.62 (SinDDM) (-0.19)。
> - 同上 上，LPIPS Div.↑ 0.49±0.07 (T=10, η=0) vs 0.38±0.07 (SinFusion) (+0.11)；训练时间（TITAN RTX）↓ 0.0 小时 vs 10.0 小时 (SinDDM) (-10.0 小时)。
> - 推理时间（A6000, 186×248图像） 上，推理时间↓ 3.09±0.02 秒 (T=10, η=0) vs 1.25±0.05 秒 (SinDDM) (+1.84 秒 (但无训练；加速版 k=5 仅 0.88s))。

## 概述

现有单图像生成模型（如 **SinGAN** (Shaham et al., ICCV 2019)、**SinDDM** (Kulikov et al., ICML 2023)）虽然能够从单张图像学习内部统计结构并生成新样本，但普遍依赖数小时的神经网络训练，计算成本极高，严重阻碍了实际部署与快速迭代。本文的核心发现是：单张图像的图像块集合是有限且低维的，其分数函数可以通过解析的加权高斯核精确计算，无需任何参数学习。基于这一洞察，作者提出一种**高效且无需训练的单图像扩散模型**，用封闭形式最优去噪器替代神经网络训练，将扩散生成还原为高效的非局部均值过程。

该方法的决定性优势体现在三个层面：**（1）训练时间为零**——与 SinDDM 需要 10 小时（TITAN RTX）形成鲜明对比（Table 1）；**（2）生成质量更优**——SIFID 指标达到 0.29±0.39，优于 SinDDM 的 0.48±0.62（Table 1）；**（3）数学上可解释**——封闭形式去噪器（式 2）等价于以每个图像块为中心的高斯混合模型，提供最优 MMSE 估计。

在方法谱系上，该工作属于单图像生成模型中的免训练分支，与基于最近邻图像块的 **GPNN** (Granot et al., CVPR 2022) 和基于 Wasserstein 距离的 **GPDM** (Elnekave & Weiss, ECCV 2022) 共享“免训练”理念，但首次将扩散框架与封闭形式去噪器结合。相较于需要训练的 **SinDDM**、**SinDiffusion** (Wang et al., TPAMI 2025) 和 **SinFusion** (Nikankin et al., ICML 2023)，本文方法在保持或超越生成质量的同时，完全消除了训练开销。

主要实验结果（15 幅自然图像，约 250×250 分辨率）表明：该方法在 SIFID（0.29 vs. 0.48）和多样性指标 LPIPS Div.（0.49 vs. 0.38）上均优于训练型扩散方法；通过融合注意力核、潜在空间扩散和近似最近邻等加速技术，推理速度可提升超过 1000 倍，并支持高达 1 GP 的超高分辨率生成（13.9 分钟，A6000）。然而，生成质量依赖图像内部的自相似性，对于缺乏重复结构的图像可能表现不佳，且超参数需根据输入图像手动调整。

## 背景与动机

单张图像生成（single-image generation）旨在从仅一幅输入图像中学习其内部统计结构，并合成新的、视觉上合理的变体。这一任务在纹理扩展、图像编辑、超分辨率和艺术创作等场景中具有广泛应用。传统方法依赖生成对抗网络（GAN），例如 **SinGAN**（Shaham et al., ICCV 2019），通过多尺度金字塔逐步生成新图像，但训练过程需要数小时且易受模式坍塌影响。

近年来，扩散模型在图像生成领域展现出卓越的质量与多样性，自然也被引入到单图像场景中。**SinDDM**（Kulikov et al., ICML 2023）、**SinDiffusion**（Wang et al., TPAMI 2025）和 **SinFusion**（Nikankin et al., ICML 2023）等工作将去噪扩散概率模型（DDPM）应用于单张图像，通过训练一个神经网络（通常是 U‑Net）来学习图像内部的块分布。这些方法在生成质量上显著优于 GAN 基线，但引入了一个关键瓶颈：**训练成本极高**。例如，SinDDM 在单张 TITAN RTX 上需要约 **10 小时**的训练时间（Table 1），这严重阻碍了实际部署与快速迭代。

与此同时，另一条技术路线试图完全避免训练。**GPNN**（Granot et al., CVPR 2022）和 **GPDM**（Elnekave & Weiss, ECCV 2022）分别基于最近邻图像块检索和 Wasserstein 距离的块分布匹配进行生成，在单图像 Fréchet Inception Distance（SIFID）指标上甚至优于训练型方法。然而，这些免训练方法存在一个根本缺陷：它们以极高概率生成输入图像的近乎重复副本（见原文 Sec. S5），本质上并未实现有意义的“生成”。

上述现状揭示了一个结构性矛盾：**训练型方法质量尚可但耗时巨大，免训练方法速度快却缺乏多样性**。是否存在一条路径，能够在不牺牲生成多样性的前提下，彻底消除训练开销？

本文的核心洞察源于对扩散模型去噪过程本质的重新审视。在标准扩散模型中，去噪器 $D(\mathbf{x}_t, t)$ 通过最小化对所有干净信号 $\mathbf{y}$ 的加权均方误差来训练：

$$\mathbb{E}_{\mathbf{y}\sim\mathcal{Y}, t, \epsilon}\left[w(t)\|D(\mathbf{x}_t, t) - \mathbf{y}\|_2^2\right]$$

当信号集 $\mathcal{V}$ 是**有限且离散**的——正如从单张图像中提取的重叠图像块集合——该优化问题存在一个**封闭形式的最优解**（Sec 3.1, Eq 2）：

$$D(\mathbf{x}_t, \mathcal{V}, t) = \frac{\sum_{\mathbf{y}\in\mathcal{V}} p_{\mathcal{N}}(\mathbf{x}_t; \alpha\mathbf{y}, \sigma^2\mathbf{I}) \mathbf{y}}{\sum_{\mathbf{y}\in\mathcal{V}} p_{\mathcal{N}}(\mathbf{x}_t; \alpha\mathbf{y}, \sigma^2\mathbf{I})}$$

这一去噪器在数学上等价于以每个干净图像块为中心的高斯混合模型（GMM）下的最小均方误差（MMSE）估计，其形式与非局部均值（non-local means）去噪高度相似。**这意味着，对于单图像生成任务，神经网络训练并非必要——最优去噪可以通过对整个干净块集合的解析加权平均直接计算。**

基于这一洞察，本文提出了一种**高效且无需训练的单图像扩散模型**（Efficient and Training-Free Single-Image Diffusion Model），将扩散生成过程还原为三个核心步骤：(1) 从输入图像提取多尺度重叠图像块构成有限数据集；(2) 用封闭形式去噪器对每个噪声块进行最优 MMSE 去噪；(3) 通过从粗到细的多尺度采样策略保持全局结构一致性。该方法在训练时间为零的前提下，实现了与训练型方法相当甚至更优的生成质量（SIFID 0.29 vs. SinDDM 0.48），同时保持了有意义的生成多样性（LPIPS Div. 0.49 vs. SinFusion 0.38）。

## 核心创新

本文的核心创新在于将单图像扩散生成从**需要数小时网络训练**的范式，彻底重构为**完全无训练的封闭形式推理**。这一转变源于一个关键洞察：单张图像的图像块集合是有限且低维的，其分数函数可通过解析的加权高斯核精确计算，无需参数学习。基于此，作者将扩散生成还原为高效的非局部均值过程，并围绕三个关键模块（changed slots）实现了系统性改进。

### 1. 从神经网络去噪器到封闭形式最优去噪器

传统单图像扩散模型（如 **SinDDM** (Kulikov et al., ICML 2023)）依赖 U‑Net 等神经网络作为去噪器，需要在每张输入图像上从头训练数小时。本文的核心突破是推导出**封闭形式的最优去噪器**（式 2）：

$$D(\mathbf{x}_t, \mathcal{V}, t) = \frac{\sum_{\mathbf{y}\in\mathcal{V}} p_{\mathcal{N}}(\mathbf{x}_t; \alpha\mathbf{y}, \sigma^2\mathbf{I}) \mathbf{y}}{\sum_{\mathbf{y}\in\mathcal{V}} p_{\mathcal{N}}(\mathbf{x}_t; \alpha\mathbf{y}, \sigma^2\mathbf{I})}$$

该去噪器在数学上等价于以每个图像块为中心的高斯混合模型（GMM），输出为所有干净图像块在给定噪声下的加权平均。这一设计直接消除了训练需求——训练时间从 SinDDM 的 10 小时（TITAN RTX）降至 0（Table 1），同时提供最优的最小均方误差（MMSE）估计。

### 2. 从单尺度隐式捕捉到显式从粗到细多尺度采样

已有方法（如 SinDiffusion）或在单一尺度上扩散，或依赖网络隐式学习多尺度信息。本文提出**显式的从粗到细多尺度采样策略**（Algorithm 2）：先在最粗尺度上运行单尺度采样，再通过拉普拉斯金字塔混合将粗尺度输出注入细尺度生成。具体而言，两尺度混合公式为：

$$\tilde{\mathbf{x}}_{s,t} \gets \hat{\mathbf{x}}_{s,t} - \mathbf{BLUR}(\hat{\mathbf{x}}_{s,t}) + \mathbf{UPSAMPLE}(\mathbf{x}_{s+1,t=0})$$

即对当前尺度去噪图像施加高通滤波，并叠加上采样后的粗尺度结果，以此保持全局结构。Figure 3 直观展示了单尺度采样无法捕获全局结构的局限性，而 Figure 4 的定性结果表明，从粗到细策略使生成质量与需要数小时训练的方法相当。

### 3. 从纯像素空间到融合加速组件的可扩展推理

封闭形式去噪器的计算复杂度为 $O(N^2)$，直接应用于高分辨率图像时推理成本高昂。为此，本文引入了三项加速技术（Sec 3.5），构成可组合的加速体系：

- **融合注意力核**：将图像块去噪器重构为缩放点积注意力，利用 FlashAttention 加速计算。
- **潜在空间扩散**：通过预训练 VAE（FLUX VAE）将图像压缩到潜在空间进行扩散，空间压缩比 8×。
- **近似最近邻（ANN）**：通过聚类将复杂度从 $O(N^2)$ 降至 $O(N^{3/2})$。

Table 2 显示，三项技术联合使 16 MP 图像的生成速度提升超过 1000 倍。在 308 MP 输入 → 1 GP 输出的极端高分辨率场景中，生成仅需 13.9 分钟（Figure 5）。

### 创新本质总结

上述三个 changed slots 共同构成了从“训练依赖”到“免训练推理”的范式转换。其本质是将扩散模型的学习问题重新表述为一个**基于有限图像块集合的解析概率推理问题**，从而在保持生成质量（SIFID: 0.29 vs SinDDM 0.48）和多样性（LPIPS Div.: 0.49 vs SinFusion 0.38）的同时，彻底消除了训练成本。

## 整体框架

该方法以单张自然图像为输入，**无需任何训练**，通过扩散模型生成保持输入图像内部统计结构的新图像。整个 pipeline 围绕一个核心观察构建：单张图像的图像块集合是有限且低维的，其分数函数可通过解析的加权高斯核精确计算，从而将扩散生成还原为高效的非局部均值过程。

### 输入与预处理

1. **输入**：单张自然图像（典型分辨率约 250×250，高分辨率实验可达 308 MP）。
2. **多尺度图像块提取**：在多个空间尺度上，从输入图像中提取重叠的图像块（默认尺寸 15×15 像素，步长 1），构成干净图像块数据集 $\mathcal{V}$。这些图像块是后续所有去噪操作的基础。

### 核心 Pipeline 模块

整个生成过程由以下模块串联构成，如 Figure 2 所示：

![[assets/figures/papers/paper_list_l865_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Efficient_and_Trai/figures/002_Figure_2.jpg]]
*Figure 2: Method overview. Our approach takes a single image as input, extracts patches, and uses the patches to generate new images using denoising diffusion. (top) We illustrate a single step of the reverse diffusion process: (blue) patches from the noisy image are denoised and used to reconstruct an image; (green) the denoised image is blended with the output of the reverse diffusion process at a coarser scale*

| 模块 | 功能 | 关键公式/算法 |
|------|------|---------------|
| 封闭形式图像块去噪 | 对每个噪声图像块，以整个干净图像块数据集为参考，计算加权平均得到去噪结果 | Eq. 2：$D(\mathbf{x}_t, \mathcal{V}, t) = \frac{\sum_{\mathbf{y}\in\mathcal{V}} p_{\mathcal{N}}(\mathbf{x}_t; \alpha\mathbf{y}, \sigma^2\mathbf{I}) \mathbf{y}}{\sum_{\mathbf{y}\in\mathcal{V}} p_{\mathcal{N}}(\mathbf{x}_t; \alpha\mathbf{y}, \sigma^2\mathbf{I})}$ |
| 图像重建 | 通过高斯权重拷贝矩阵 $\mathbf{R}_{\rho}$（$\rho=0.2$）将去噪后的图像块拼回完整图像 | $\hat{\mathbf{x}}_t \gets \sum_{i=1}^{N} \mathbf{R}_{\rho}^{(i)} \hat{\mathbf{x}}_t^{(i)}$ |
| 反向扩散更新 | 依次计算去噪信号、估计噪声，并采样前一扩散步的加噪图像 | Eqs. 3–6 |
| 两尺度混合 | 在从粗到细生成中，将粗尺度输出上采样后与当前尺度去噪图像的高通分量相加 | $\tilde{\mathbf{x}}_{s,t} \gets \hat{\mathbf{x}}_{s,t} - \mathbf{BLUR}(\hat{\mathbf{x}}_{s,t}) + \mathbf{UPSAMPLE}(\mathbf{x}_{s+1,t=0})$ |

### 从粗到细的生成流程

单尺度采样仅能捕获图像块尺度的统计信息，无法保持全局结构（Figure 3）。为此，该方法采用**从粗到细的多尺度采样策略**：

1. 在最粗尺度上执行完整的单尺度反向扩散（Algorithm 1），生成粗尺度输出 $\mathbf{x}_{s+1, t=0}$。
2. 在下一个更细尺度上，每一步反向扩散中，先将当前噪声图像块去噪并重建为 $\hat{\mathbf{x}}_{s,t}$，然后通过**两尺度混合**注入粗尺度的全局结构信息：对 $\hat{\mathbf{x}}_{s,t}$ 施加高通滤波（减去模糊版本），再加上上采样后的粗尺度输出。
3. 逐尺度递进，直至达到原始分辨率。

这一设计使生成图像既保留了图像块级别的纹理细节，又维持了全局的布局与结构。

### 加速组件

针对封闭形式去噪器 $O(N^2)$ 的计算复杂度，该方法集成了三个可选加速模块：

- **融合注意力核**：将图像块去噪器重构为缩放点积注意力，利用 FlashAttention 加速。
- **潜在空间扩散**：通过预训练 VAE（FLUX VAE，8× 空间压缩）将扩散过程迁移到压缩潜在空间。
- **近似最近邻（ANN）**：以聚类近似最近邻搜索，将复杂度降至 $O(N^{3/2})$。

三者联合可使 16 MP 图像的生成速度提升超过 1000 倍（Table 2），且仅带来轻微的 SIFID 上升（0.29→0.38，Table 1）。

### 输入输出流总结

```
单张输入图像
    │
    ▼
多尺度图像块提取 ──► 干净图像块数据集 V
    │
    ▼
从粗到细多尺度反向扩散循环：
    粗尺度：单尺度采样 ──► 粗尺度输出
    细尺度：图像块去噪 → 重建 → 两尺度混合 → 反向扩散更新
    │
    ▼
生成图像（保持输入图像的内部统计结构）
```

整个流程**完全无训练**，所有计算基于输入的图像块数据集闭合形式完成，从根本上消除了传统单图像扩散模型数小时的网络训练需求。

## 核心模块与公式推导

### 3.1 封闭形式最优去噪器

本方法的核心洞察在于：单张图像的图像块集合是有限且低维的，其分数函数可通过解析的加权高斯核精确计算，无需参数学习。传统扩散模型通过最小化去噪损失来训练神经网络：

$$
\mathbb{E}_{\mathbf{y}\sim\mathcal{Y}, t\sim\mathcal{U}[0,T], \epsilon\sim\mathcal{N}(\mathbf{0},\mathbf{I})} \left[ w(t) \| D(\mathbf{x}_t, t) - \mathbf{y} \|_2^2 \right]
$$

当干净数据集 $\mathcal{V}$ 为有限离散集合时，该损失的最优最小均方误差（MMSE）解具有封闭形式：

$$
D(\mathbf{x}_t, \mathcal{V}, t) = \frac{\sum_{\mathbf{y}\in\mathcal{V}} p_{\mathcal{N}}(\mathbf{x}_t; \alpha\mathbf{y}, \sigma^2\mathbf{I}) \mathbf{y}}{\sum_{\mathbf{y}\in\mathcal{V}} p_{\mathcal{N}}(\mathbf{x}_t; \alpha\mathbf{y}, \sigma^2\mathbf{I})}
$$

**公式含义**：对任意噪声图像块 $\mathbf{x}_t$，去噪输出为所有干净图像块 $\mathbf{y}\in\mathcal{V}$ 的加权平均，权重为 $\mathbf{x}_t$ 在以 $\alpha\mathbf{y}$ 为中心、$\sigma^2\mathbf{I}$ 为协方差的高斯分布下的似然概率。这一形式在数学上等价于以每个图像块为中心的**高斯混合模型（GMM）**下的最优估计，本质上是一个非局部均值（non-local-means）去噪器。

### 3.2 反向扩散更新

基于封闭形式去噪器，单步反向扩散过程依次执行以下计算（式 3–6）：

1. **去噪信号估计**：$\hat{\mathbf{x}}_t \gets D(\mathbf{x}_t, \mathcal{V}, t)$
2. **噪声估计**：$\hat{\boldsymbol{\epsilon}}_t \gets (\mathbf{x}_t - \alpha(t)\hat{\mathbf{x}}_t)/\sigma(t)$
3. **前一步加噪图像采样**：

$$
\mathbf{x}_{t-1} \gets \alpha(t-1)\hat{\mathbf{x}}_t + \sqrt{\sigma(t-1)^2 - c(t-1)^2}\hat{\epsilon}_t + c(t-1)\epsilon_t
$$

其中 $c(t-1) \in [0, \sigma(t-1)]$ 控制采样随机性，$\epsilon_t \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 为注入的随机噪声。当 $\eta(t)=0$ 时，该更新退化为确定性 **DDIM** 采样。

### 3.3 图像块提取与重建

**图像块提取**：从输入图像按多个尺度提取重叠图像块（典型尺寸 15×15，步长 1），构成干净数据集 $\mathcal{V}$。

**图像重建**：对所有噪声图像块分别去噪后，通过加权拷贝算子 $\mathbf{R}_{\rho}^{(i)}$ 将去噪块拼回完整图像：

$$
\hat{\mathbf{x}}_t \gets \sum_{i=1}^{N} \mathbf{R}_{\rho}^{(i)} \hat{\mathbf{x}}_t^{(i)}
$$

其中 $\mathbf{R}_{\rho}^{(i)}$ 使用标准差 $\rho=0.2$ 的高斯权重将第 $i$ 个图像块放置回其原始位置，重叠区域通过权重归一化实现平滑融合。

### 3.4 从粗到细多尺度采样

单尺度采样仅捕获图像块尺度的统计信息，无法保持全局结构（Figure 3）。为此，方法引入显式的从粗到细多尺度生成策略。在相邻两尺度间，通过拉普拉斯金字塔混合注入粗尺度全局结构：

![[assets/figures/papers/paper_list_l865_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Efficient_and_Trai/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of single-scale sampling. This procedure (detailed in Algorithm 1) captures image statistics at the scale of an individual patch (white squares), but fails to capture the coarse structure of the image. We address this issue using coarse-to-fine image sampling (Algorithm 2, Figure 4)*

$$
\tilde{\mathbf{x}}_{s,t} \gets \hat{\mathbf{x}}_{s,t} - \mathbf{BLUR}(\hat{\mathbf{x}}_{s,t}) + \mathbf{UPSAMPLE}(\mathbf{x}_{s+1,t=0})
$$

**公式含义**：当前尺度 $s$ 的去噪图像 $\hat{\mathbf{x}}_{s,t}$ 经高通滤波（减去模糊版本）提取细节分量，再与上采样后的粗尺度输出 $\mathbf{x}_{s+1,t=0}$ 相加。粗尺度输出提供全局布局约束，细尺度去噪补充局部纹理，二者协同实现结构一致的高质量生成。

### 3.5 加速组件

为应对封闭形式去噪器 $O(N^2)$ 的计算复杂度，方法引入三项加速技术：

- **融合注意力核**：将图像块去噪器重构为缩放点积注意力，利用 PyTorch 的 FlashAttention 后端加速。
- **潜在空间扩散**：通过预训练 VAE（FLUX VAE，8× 空间压缩）将扩散过程迁移到低维潜在空间。
- **近似最近邻（ANN）**：对图像块数据集进行聚类，将去噪搜索复杂度降至 $O(N^{3/2})$。

### 3.6 关键超参数与调度

- **噪声调度**：采用 flow matching 调度 $\alpha(t) = 1 - t/T$，$\sigma(t) = t/T$。
- **图像块尺寸**：消融实验表明 11–15 像素的图像块可获得最低 SIFID（Table 3）。
- **重建权重**：$\rho=0.2$ 在图像块拼合中取得最优质量（Table 3）。
- **扩散步数**：SIFID 在约 10 步后趋于收敛，更多步数改善有限（Figure 8）。

## 实验与分析

### 核心定量结果

**Table 1** 汇总了无条件生成的主实验。在 15 幅自然图像（约 250×250 分辨率）上，本文方法以 **零训练时间** 取得与需要数小时训练的扩散模型相当甚至更优的生成质量：

- **SIFID ↓**：0.29±0.39（T=10, η=0），优于 SinDDM 的 0.48±0.62，差距 −0.19，表明生成的图像块分布更接近原图。
- **LPIPS Div. ↑**：0.49±0.07，高于 SinFusion 的 0.38±0.07，说明生成样本的多样性显著提升。
- **训练时间**：0.0 小时，对比 SinDDM 的 10.0 小时（TITAN RTX），完全消除训练成本。
- **推理时间**：3.09±0.02 秒（A6000, 186×248 图像, T=10），慢于 SinDDM 的 1.25 秒，但加速版（k=5 ANN）降至 0.88 秒，兼顾效率。

需注意：GPNN 和 GPDM 在 SIFID 上最优，但原文指出它们高概率生成近乎重复的图像（Sec. S5），因此本文方法在质量-多样性权衡上更具优势。无参考图像质量指标（NIQE、NIMA、MUSIQ）上，本文方法也与训练型方法持平。

### 加速策略的消融

**Table 2** 展示了三种加速组件在不同分辨率下的推理时间（RTX 6000 Ada, T=10）：

- **融合注意力（FlashAttention）**：将图像块去噪器重写为缩放点积注意力，利用 PyTorch 融合注意力后端，显著降低显存和计算开销。
- **潜在空间扩散**：使用 FLUX VAE（8× 空间压缩）在潜在空间执行去噪，图像块尺寸从 15×15 降至 7×7（16 通道），大幅减少计算量。
- **近似最近邻（ANN）**：通过聚类将去噪器的复杂度从 O(N²) 降至 O(N^{3/2})。

三种技术联合使 16 MP 图像的生成速度提升超过 **1000 倍**。在 308 MP 输入 → 1 GP 输出的极端高分辨率场景下（Figure 5），仅需 **13.9 分钟**（T=20, η=1, ANN k=5, RTX A6000 PRO），证明了方法的可扩展性。

![[assets/figures/papers/paper_list_l865_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Efficient_and_Trai/figures/007_Figure_5.jpg]]
*Figure 5: High-resolution generation. The input image is 308 MP, and we generate an image of size 14336 × 70080 (1 GP) in only 13.9 minutes (NVIDIA RTX A6000 PRO) by incorporating the three proposed acceleration techniques (see Sec. S3.5). Specifically, we use T = 20 sampling steps with η = 1 and ANN with k = 5. Image: Duncan Rawlinson, CC BY-NC 2.0*

### 超参数敏感性

**Figure 8** 显示 SIFID 随扩散步数 T 的变化曲线：约 **10 步** 后 SIFID 趋于稳定，更多步数改善有限。随机性参数 η 增大时 SIFID 略有上升，但生成多样性增加。

**Table 3** 分析了单尺度采样下图像块尺寸与重建权重 ρ 的影响：
- 较小 ρ（0.2）和 11–15 像素的图像块尺寸取得最低 SIFID。
- ρ 过大会引入过度平滑，图像块尺寸过大则无法捕获细粒度纹理，过小则丢失结构信息。

### 加速版的质量-效率权衡

使用近似最近邻（k=5）时，SIFID 从 0.29 轻微升至 0.38，但推理时间从 3.09 秒降至 0.88 秒（Table 1, proposed (k=5) 列）。这表明 ANN 近似以可接受的质量代价换取了显著的加速，适合对实时性要求高的场景。

### 失败模式与局限

1. **自相似性依赖**：方法的核心假设是图像内部存在丰富的重复结构。对于缺乏自相似性的图像（如纯色区域、随机纹理），图像块数据集无法提供有效的生成先验，生成质量会下降。
2. **超参数手动调整**：扩散步数 T、图像块尺寸、ρ、η 等超参数需要针对输入图像调整，缺乏自动化最优选择机制。
3. **图像块重建伪影**：当图像块尺寸选择不当或 ρ 设置不合理时，重建图像可能出现模糊或块状伪影。
4. **计算复杂度瓶颈**：封闭形式去噪器的原始复杂度为 O(N²)，对于大尺寸图像或密集采样的图像块数据集，无加速时推理速度显著慢于训练型方法。ANN 近似缓解了此问题，但引入了近似误差。

### 图表结论摘要

- **Figure 4**：定性对比表明，本文免训练方法生成的图像在纹理保持和结构合理性上与 SinDDM、SinDiffusion 等训练型方法相当，且多样性更丰富。
- **Figure 5**：验证了方法在超高分辨率场景（308 MP → 1 GP）下的可行性，13.9 分钟完成生成。
- **Figure 8 + Table 3**：为实际部署提供了超参数选择指导——T≈10、图像块尺寸 11–15、ρ=0.2 是质量-效率的较优平衡点。

![[assets/figures/papers/paper_list_l865_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Efficient_and_Trai/figures/005_Figure_4.jpg]]
*Figure 4: Unconditional single-image generation results. Our training-free, coarse-to-fine image sampling procedure based on closed-form denoising diffusion (right) produces results of the same quality as other state-of-the-art methods that require hours of training time*

![[assets/figures/papers/paper_list_l865_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Efficient_and_Trai/figures/010_Figure_8.jpg]]
*Figure 8: Plot of SIFID vs diffusion timesteps T for coarse-to-fine image sampling across different η values. The SIFID converges in roughly 10 timesteps*

![[assets/figures/papers/paper_list_l865_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Efficient_and_Trai/figures/011_Table_3.jpg]]
*Table 3: Analysis of the single-scale image sampling SIFID versus different patch sizes and values of*

### 补充图表

![[assets/figures/papers/paper_list_l865_https_openaccess_thecvf_com_content_CVPR2026_html_Qiu_Efficient_and_Trai/figures/006_Table.jpg]]

## 方法谱系与知识库定位

### 单图像生成模型谱系

本文方法处于单图像生成模型（single-image generative models）这一研究脉络中。该领域的目标是从单张输入图像学习其内部统计结构，并生成保留该结构特征的新图像。早期工作以 **SinGAN**（Shaham et al., ICCV 2019）为代表，采用多尺度 GAN 金字塔逐级生成，训练时间通常在数十分钟到数小时级别。后续基于扩散的方法如 **SinDDM**（Kulikov et al., ICML 2023）、**SinDiffusion**（Wang et al., TPAMI 2025）和 **SinFusion**（Nikankin et al., ICML 2023）将扩散生成范式引入单图像场景，通过训练 U‑Net 等神经网络去噪器来捕获图像内部分布，但训练成本显著增加——SinDDM 在 TITAN RTX 上需约 10 小时（Table 1）。

与上述训练型方法不同，**GPNN**（Granot et al., CVPR 2022）和 **GPDM**（Elnekave and Weiss, ECCV 2022）探索了免训练路线：GPNN 基于最近邻图像块检索与拼接，GPDM 则通过 Wasserstein 距离匹配图像块分布。二者在 SIFID 指标上表现最优，但原文指出它们高概率生成近乎重复的图像（Sec. S5），多样性不足。

本文的**关键转折点**在于：将扩散模型的分数函数与经典图像块先验（patch prior）建立等价关系，从而将去噪过程转化为无需训练的加权平均。这一思路在理论上可追溯至非局部均值去噪（non-local means）和基于图像块的 GMM 先验，但本文首次将其系统性地嵌入完整的多尺度扩散生成框架中，实现了训练时间为零且质量与训练型方法可比的结果。

### 核心知识贡献

本工作的核心知识贡献可归纳为三个层次：

**1. 扩散生成与图像块先验的等价性桥梁。** 本文证明了：当数据集为有限图像块集合时，扩散模型的最优去噪器存在封闭形式解（式 2），其输出等价于以各干净图像块为中心的高斯混合模型下的 MMSE 估计。这一发现将扩散生成从“神经网络参数学习”还原为“非局部加权平均”，在概念上连接了扩散模型与经典图像复原中的图像块方法。

**2. 从粗到细多尺度扩散采样。** 单尺度图像块扩散仅能捕获局部统计，无法保持全局结构（Figure 3）。本文通过拉普拉斯金字塔式的高频注入（式 TwoScaleBlend）将粗尺度输出与细尺度去噪结果融合，实现了全局结构保持的多尺度生成，这是对纯图像块方法的必要补充。

**3. 计算加速策略。** 封闭形式去噪器的朴素实现复杂度为 $O(N^2)$（$N$ 为图像块数量），在高分辨率下不可行。本文通过融合注意力核（FlashAttention）、潜在空间扩散（FLUX VAE 8× 压缩）和近似最近邻（ANN, $k=5$）三个组件，将 16 MP 图像的生成速度提升超过 1000 倍（Table 2），使该方法可扩展至 308 MP 到 1 GP 的超高分辨率生成（Figure 5）。

### 适用边界与局限

**依赖图像内部自相似性。** 该方法的核心假设是输入图像包含丰富的重复或相似结构（即图像块数据集具有足够的统计代表性）。对于缺乏自相似性的图像（如高度非平稳纹理、信息稀疏的场景），图像块先验的表达能力有限，生成质量可能显著下降。这一局限在原文中作为首要限制条件被明确指出。

**超参数敏感性。** 扩散步数 $T$、图像块尺寸、重建权重 $\rho$ 等超参数需要根据输入图像调整，缺乏自动化最优选择机制。消融实验表明：$\rho=0.2$ 和 11–15 像素的图像块尺寸可获得最低 SIFID（Table 3），SIFID 在约 10 个扩散步后趋于稳定（Figure 8），但这些结论基于 15 幅自然图像的统计，未必适用于所有图像类型。

**推理速度的权衡。** 在无加速条件下，推理时间（3.09s, A6000, 186×248 图像, $T=10$）慢于 SinDDM（1.25s），尽管训练时间为零。加速版（$k=5$ ANN）可将推理降至 0.88s，但 SIFID 从 0.29 升至 0.38（Table 1），存在质量-速度权衡。

**图像块重建伪影。** 图像块提取和加权重建过程可能引入模糊或块状伪影，尤其当图像块尺寸选择不当或 $\rho$ 过大时。原文未对伪影类型进行系统分类，该点需在实际应用中手动验证。

**计算复杂度的理论瓶颈。** 即使采用 ANN 近似，复杂度仍为 $O(N^{3/2})$，对于超大图像块数据集（如高分辨率多尺度提取）仍构成挑战。该方法目前依赖 GPU 并行和注意力融合来弥补，但未触及算法复杂度的根本性降低。

### 开放问题

**通用单图像先验的构建。** 当前方法将图像块先验仅用于生成任务。一个自然的问题是：能否基于该封闭形式构建通用的单图像先验，用于图像复原（去噪、超分辨率、修复）等逆问题？这需要将扩散采样框架适配为条件生成或后验采样，同时保持封闭形式去噪器的最优性。

**多图像扩散先验的扩展。** 该方法目前仅利用单张图像的内部统计。若能同时利用多张相关图像（如同场景不同视角、同类别不同实例）的图像块集合，可构建更丰富的多图像扩散先验，这可能提升对缺乏自相似性图像的泛化能力。

**文本引导编辑中的理论一致性。** 在文本引导生成中，CLIP 梯度的引入（通过预训练视觉-语言模型引导扩散过程）是否破坏了封闭形式去噪器的最优性？当前方法将 CLIP 梯度作为外部力项加入采样过程，但未分析其对最优 MMSE 估计性质的影响，这需要进一步的理论分析。

**非自然图像的泛化验证。** 所有实验均在自然图像上进行。对于医学图像、遥感图像、工业检测图像等具有不同统计特性的非自然图像，图像块先验的适用性和超参数选择策略尚未验证。

**实时部署的可行性。** 尽管加速版在 A6000 上可达 0.88s（186×248），但距离实时生成（<100ms）仍有差距。移动端部署面临更严峻的算力限制，需要模型压缩、量化或更高效的近似算法。

## 原文 PDF

![[paperPDFs/CVPR_2026/Efficient_and_Training_Free_Single_Image_Diffusion_Models.pdf]]