---
title: "SeaCache: Spectral-Evolution-Aware Cache for Accelerating Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SeaCache_Spectral_Evolution_Aware_Cache_for_Accelerating_Diffusion_Models.pdf
project_link: null
code_link: "https://github.com/jiwoogit/SeaCache"
aliases:
- SeaCache
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入依赖于时间步的频谱演化感知滤波器（SEA filter），通过频率域重加权强调信号成分并抑制噪声，使缓存重用决策更准确反映内容冗余。
primary_logic: 将扩散模型固有的频谱演化先验显式地编码进缓存调度，在频谱对齐的空间中衡量时间步间冗余，避免高频噪声的干扰，从而在不重新训练的情况下显著提升缓存策略的速度-质量权衡。
claims:
- 在Oracle实验中，基于SEA滤波输出距离的缓存调度相比基于原始输出距离的调度，在相同刷新率下实现更高的PSNR，更好跟踪全计算轨迹。
- SEA滤波后的输入距离与SEA滤波后的输出距离高度一致，而原始输入距离或多项式拟合输入距离在早期时间步的对齐较弱。
- 在FLUX.1-dev、HunyuanVideo、Wan2.1 1.3B等多个视觉生成模型上，SeaCache在相似的延迟和计算量下，PSNR、LPIPS、SSIM等全参考指标均显著优于TeaCache、TaylorSeer等基线。
- 消融实验证明SEA滤波器在PSNR-刷新率权衡上优于互补滤波器(1-SEA)、无归一化和低通滤波器，证明频谱选择性的设计是关键。
---

# SeaCache: Spectral-Evolution-Aware Cache for Accelerating Diffusion Models

> [!tip] 核心洞察
> 将扩散模型固有的频谱演化先验显式地编码进缓存调度，在频谱对齐的空间中衡量时间步间冗余，避免高频噪声的干扰，从而在不重新训练的情况下显著提升缓存策略的速度-质量权衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | SeaCache：基于频谱演化感知的缓存加速扩散模型 |
| 英文题名 | SeaCache: Spectral-Evolution-Aware Cache for Accelerating Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.18993) · [Code](https://github.com/jiwoogit/SeaCache) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SeaCache |
| Dataset | FLUX.1-dev, HunyuanVideo, Wan2.1 1.3B |

> [!tip] 效果简介
> - FLUX.1-dev (50步) 上，PSNR↑ / LPIPS↓ / SSIM↑ SeaCache (δ=0.3): 26.285 / 0.106 / 0.893 vs TeaCache (δ=0.3): 20.762 / 0.211 / 0.810; TaylorSeer (S=3): 22.783 / 0.163 / 0.... (PSNR +5.5∼+3.5 dB, LPIPS -0.1∼-0.05)。
> - FLUX.1-dev (50步, 更激进的预算) 上，PSNR↑ / LPIPS↓ / SSIM↑ SeaCache (δ=0.6): 21.332 / 0.226 / 0.798 vs TeaCache (δ=0.6): 17.214 / 0.348 / 0.714; TaylorSeer (S=5): 19.972 / 0.236 / 0.... (PSNR +4.1∼+1.4 dB)。
> - HunyuanVideo (50步) 上，PSNR↑ / LPIPS↓ / SSIM↑ SeaCache (δ=0.19): 32.39 / 0.047 / 0.932 vs TeaCache (δ=0.12): 23.40 / 0.133 / 0.805; TaylorSeer (S=2): 24.14 / 0.152 / 0.8... (PSNR +8.2∼+9.0 dB)。

## 概述

扩散模型与流模型在图像和视频生成中取得了显著进展，但其迭代去噪过程计算开销巨大，严重制约了推理效率。现有缓存加速方法（如 **TeaCache**、**TaylorSeer**、**DiCache**）通过在相邻时间步间重用中间特征来减少计算量，然而它们均基于原始特征空间的距离度量来制定缓存决策。这一策略存在根本性瓶颈：**扩散模型的去噪过程伴随着固有的频谱演化——早期时间步主要恢复低频结构，后期逐步引入高频细节——而原始特征空间的距离度量受高频噪声干扰，难以准确捕捉内容冗余，导致缓存决策在加速与保真度之间无法达到最优平衡。**

**SeaCache** 提出了一种频谱演化感知的缓存策略，核心思想是将扩散模型的时间步相关频谱先验显式编码进缓存调度。具体而言，SeaCache 设计了一个依赖于时间步的 **频谱演化感知滤波器（SEA filter）**，该滤波器基于最优线性去噪器的 Wiener 频率响应导出：在早期时间步强调低频信号，在后期逐步纳入高频成分。通过对中间特征应用快速傅里叶变换（FFT）、与 SEA 滤波器逐元素相乘、再经逆 FFT 获得频谱感知特征，SeaCache 在信号成分增强的表示空间中衡量时间步间冗余，从而避免高频噪声对缓存决策的干扰。

在方法定位上，SeaCache 属于**即插即用的缓存距离度量替换方案**，不改变模型结构或权重，无需重新训练，仅替换缓存调度中的距离计算模块即可与现有动态缓存框架无缝集成。

**核心实验结果**表明，SeaCache 在多个主流视觉生成模型上实现了显著的质量提升：

- 在 **FLUX.1-dev** 上，约50%刷新率下，SeaCache 的 PSNR 达到 26.285 dB，比 TeaCache 高出 5.5 dB，比 TaylorSeer 高出 3.5 dB；LPIPS 降至 0.106。
- 在 **HunyuanVideo** 视频生成模型上，SeaCache 的 PSNR 达到 32.39 dB，领先 TeaCache 约 9.0 dB。
- 在 **Wan2.1 1.3B** 上，SeaCache 的 PSNR 达到 26.60 dB，领先 TeaCache 约 5.8 dB，领先 TaylorSeer 约 10.5 dB。

Oracle 实验和消融研究进一步验证了 SEA 滤波器设计的有效性：基于 SEA 滤波输出距离的缓存调度在相同刷新率下始终优于基于原始输出距离的调度，且频谱选择性滤波（而非简单的低通滤波或互补滤波）是实现这一优势的关键。

## 背景与动机

### 扩散模型加速的缓存范式

扩散模型与整流流模型已成为视觉生成的核心架构，但其迭代去噪过程计算开销巨大。以FLUX、HunyuanVideo、Wan2.1等先进模型为例，单次推理需执行数十步完整前向传播，严重制约了实时应用和资源受限场景的部署。

为缓解这一问题，**特征缓存**（feature caching）作为一类轻量级加速策略受到关注。其核心思想是：相邻时间步的中间特征高度冗余，通过重用已计算的输出来跳过部分去噪器调用，从而降低总计算量。代表性方法包括：

- **TeaCache**：基于相邻时间步输入特征 $I_t$ 和 $I_{t+1}$ 之间的相对L1距离 $\Delta_t$ 进行动态缓存调度，当累积距离超过阈值 $\delta$ 时触发去噪器刷新，否则重用缓存输出。
- **TaylorSeer**：利用泰勒展开预测不同时间步的输出变化，支持静态和动态两种缓存模式。
- **DiCache**：针对DiT架构，在输入侧计算近似距离来决定缓存策略。
- **Δ-DiT**：通过特征差值缓存加速DiT。
- **ToCa**：基于token剪枝的缓存加速方案。
- **MagCache**：基于幅度阈值的固定缓存策略。

这些方法的共同点在于：缓存决策完全依赖**原始特征空间**的距离度量，未考虑扩散模型去噪过程中固有的**频谱演化**特性。

### 被忽视的频谱演化先验

扩散模型的去噪过程遵循从低频到高频的渐进式生成规律：在早期时间步，模型主要恢复图像的粗粒度低频结构（如整体布局、形状）；随着去噪推进，高频细节（如纹理、边缘）逐步涌现。这一频谱演化特性已被多项研究证实，但现有缓存方法在衡量时间步间冗余时，始终在原始特征空间中计算距离，使得高频噪声成分与低频信号成分被**无差别对待**。

这导致一个关键矛盾：在噪声主导的早期时间步，原始特征距离受高频噪声干扰严重，难以准确反映内容层面的真实冗余；而在细节丰富的后期时间步，微小的纹理变化可能被噪声淹没，导致缓存决策错失关键刷新时机。**Oracle实验**直接验证了这一判断：若以去噪器输出（而非输入）的距离作为缓存调度依据，基于SEA滤波输出距离的调度在相同刷新率下实现了显著更高的PSNR，且更紧密地跟踪全计算轨迹（Figure 2, Sec. 4.1）。这表明，原始特征空间的距离度量是缓存性能的瓶颈所在。

### 本文动机与核心思路

基于上述分析，本文提出一个根本性问题：**能否将扩散模型的频谱演化先验显式编码进缓存调度，使缓存决策在频谱对齐的空间中进行？**

SeaCache的回答是：在测量特征距离之前，对中间特征施加一个**依赖于时间步的频谱演化感知滤波器**（Spectral-Evolution-Aware Filter，简称SEA滤波器），通过频率域重加权来强调信号成分并抑制噪声，从而使缓存重用决策更准确地反映内容冗余。这一设计的核心优势在于：

1. **理论驱动**：SEA滤波器从最优线性去噪器（Wiener准则）导出，其频率响应 $G_t(f)$ 自然体现了“低频先恢复、高频后出现”的频谱演化规律，无需额外训练。
2. **即插即用**：SEA滤波作为特征变换模块嵌入现有缓存框架，不改变模型结构或权重，可与TeaCache、DiCache等方案无缝结合。
3. **速度-质量权衡优化**：在频谱感知空间中计算的距离 $\widetilde{\Delta}_t$ 替代原始 $\Delta_t$，使缓存调度在相同计算预算下获得更高的保真度。

Figure 1 直观展示了这一动机：下方面板描绘了一张猫图像的完整去噪轨迹，早期时间步呈现模糊的低频轮廓，后期逐步细化出毛发等高频细节；SeaCache通过SEA滤波器对原始扩散特征进行时间步感知的频谱重加权，使距离度量更好地捕捉时间步间的频谱残差，从而在加速与保真度之间取得更优平衡。

## 核心创新

SeaCache的核心创新在于将扩散模型去噪过程中的**频谱演化先验**显式编码进缓存调度，解决了现有缓存方法在原始特征空间度量距离时受高频噪声干扰的根本缺陷。该创新集中体现在一个关键的**changed slot**上：缓存距离度量的计算空间。

### 从原始特征空间到频谱感知空间

现有动态缓存方法（如**TeaCache**、**TaylorSeer**、**DiCache**）的核心逻辑是：当相邻时间步的输入特征变化足够小时，跳过当前步的去噪计算，直接复用上一步的缓存输出。变化程度的度量通常采用原始特征空间的相对L1距离：

$$\Delta _ { t } = \mathrm { L } 1 _ { \mathrm { r e l } } ( I _ { t } , I _ { t + 1 } ) = \frac { \| I _ { t } - I _ { t + 1 } \| _ { 1 } } { \| I _ { t + 1 } \| _ { 1 } + \xi }$$

这一设计的隐含假设是：特征空间中的距离能够准确反映内容冗余。然而，扩散模型的去噪轨迹具有显著的频谱演化特性——早期时间步主要恢复低频结构，后期逐步引入高频细节（见Figure 4中SEA滤波器随时间的频率响应变化）。在原始特征空间中，高频噪声成分会污染距离度量，导致缓存决策无法准确区分“内容层面的有意义变化”与“噪声层面的无意义波动”。

SeaCache的解决方案是**将距离度量的计算从原始特征空间迁移到频谱感知空间**。具体而言，引入一个依赖于时间步的**频谱演化感知滤波器（SEA Filter）** $G_t^{\mathrm{norm}}(f)$，对输入特征进行频率域重加权：

$$\mathcal { P } ( G _ { t } ^ { \mathrm { n o r m } } , I _ { t } ) = \mathrm { i F F T } \big ( G _ { t } ^ { \mathrm { n o r m } } ( f ) \odot \mathrm { F F T } ( I _ { t } ) \big )$$

滤波后的特征强调与当前时间步信号成分相关的频率，抑制噪声主导的频率分量。缓存距离度量随之变为滤波后特征的相对L1距离：

$$\widetilde { \Delta } _ { t } = \mathrm { L } 1 _ { \mathrm { r e l } } \big ( \mathcal { P } ( G _ { t } ^ { \mathrm { n o r m } } , I _ { t } ) , \mathcal { P } ( G _ { t + 1 } ^ { \mathrm { n o r m } } , I _ { t + 1 } ) \big )$$

累积距离的刷新规则保持不变（Eq. (4)），仅替换了距离度量的计算方式，使SeaCache成为一种**即插即用的缓存策略**——无需重新训练模型，仅替换距离度量即可嵌入现有缓存框架。

### 滤波器设计的理论基础

SEA滤波器的频率响应$G_t(f)$并非启发式设计，而是从最优线性去噪器的Wiener准则导出：

$$G _ { t } ( f ) = \frac { a _ { t } S _ { x } ( f ) } { a _ { t } ^ { 2 } S _ { x } ( f ) + b _ { t } ^ { 2 } }$$

其中$a_t$和$b_t$来自前向加噪过程$x _ { t } = a _ { t } x _ { 0 } + b _ { t } \varepsilon$，$S_x(f)$为自然图像的功率谱（假设遵循幂律分布）。该滤波器自然体现了扩散模型的频谱演化特性：早期时间步（$a_t$大、$b_t$小）主要通过低频成分，后期逐渐开放高频通道。为进一步稳定不同时间步的滤波能量，SeaCache引入密度归一化：

$$\nu _ { t } = \Big ( \frac { 1 } { L } \sum _ { f _ { \ell } \in \mathcal { F } } G _ { t } ( f _ { \ell } ) \Big ) ^ { - 1 } , \quad G _ { t } ^ { \mathrm { n o r m } } ( f ) = \nu _ { t } G _ { t } ( f )$$

归一化确保各时间步滤波后特征的总能量保持恒定，使跨时间步的距离比较具有一致的尺度。

### 创新验证：频谱对齐的有效性

Oracle实验（Figure 2）直接验证了频谱感知距离度量的优势：基于SEA滤波输出距离的缓存调度，在相同刷新率下始终比基于原始输出距离的调度获得更高的PSNR，更紧密地跟踪全计算轨迹。Figure 5进一步揭示了机制层面的证据——SEA滤波后的输入距离与SEA滤波后的输出距离高度一致，而原始输入距离或多项式拟合输入距离在早期时间步的对齐明显较弱。这表明频谱感知空间中的距离度量能够更准确地预测去噪器输出的实际变化，从而做出更合理的缓存决策。

消融实验（Figure 8）排除了其他可能解释：互补滤波器（1−SEA）、无归一化滤波器和低通滤波器在PSNR-刷新率权衡上均显著劣于SEA滤波器，证明频谱选择性的设计——而非简单的滤波操作或能量归一化——是性能提升的关键。此外，将SEA滤波器嵌入DiCache后（DiCache+Ours，Figure 9），在相同刷新率下PSNR始终高于原始DiCache，进一步证实了频谱感知距离度量作为通用模块的有效性。

## 整体框架

SeaCache 是一种**即插即用的缓存策略**，其核心设计理念是将扩散模型去噪过程中的频谱演化先验显式编码进缓存距离度量中，仅替换现有动态缓存方案中的距离计算模块，而保持累积刷新规则不变。

### 方法总览

SeaCache 的整体流水线如 Figure 3 所示，由三个关键模块串联构成：

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/003_Figure_3.jpg]]
*Figure 3: Overview of SeaCache. Given input features*

1. **SEA 滤波器设计（SEA Filter Design）**：基于最优线性去噪器的 Wiener 准则，导出时间步相关的频率响应 $G_t(f)$，并通过密度归一化得到 $G_t^{\mathrm{norm}}(f)$，确保不同时间步的滤波能量保持恒定，便于跨时间步的距离比较。

2. **频谱特征变换（Feature Transformation）**：对输入特征 $I_t$ 和 $I_{t+1}$ 分别应用快速傅里叶变换（FFT），与对应时间步的归一化 SEA 滤波器 $G_t^{\mathrm{norm}}$ 和 $G_{t+1}^{\mathrm{norm}}$ 逐元素相乘，再通过逆 FFT 获得频谱感知特征 $\mathcal{P}(G_t^{\mathrm{norm}}, I_t)$ 和 $\mathcal{P}(G_{t+1}^{\mathrm{norm}}, I_{t+1})$。该变换在频率域重加权，强调信号成分并抑制噪声。

3. **频谱感知动态缓存（Spectrum-Aware Dynamic Caching）**：在滤波后的特征空间计算相对 L1 距离 $\widetilde{\Delta}_t$，累积相邻时间步的滤波距离，当累积值超过阈值 $\delta$ 时触发去噪器刷新，否则重用缓存的输出。

### 输入输出流

给定相邻时间步的特征 $I_t$ 和 $I_{t+1}$，SeaCache 的处理流程为：

- **输入**：扩散模型中间层的输入特征 $I_t$、$I_{t+1}$ 及对应的时间步 $t$、$t+1$。
- **变换**：$I_t \xrightarrow{\text{FFT}} \xrightarrow{\odot G_t^{\mathrm{norm}}} \xrightarrow{\text{iFFT}} \mathcal{P}(G_t^{\mathrm{norm}}, I_t)$，对 $I_{t+1}$ 同理。
- **度量**：计算频谱感知相对距离 $\widetilde{\Delta}_t = \mathrm{L1_{rel}}\big(\mathcal{P}(G_t^{\mathrm{norm}}, I_t), \mathcal{P}(G_{t+1}^{\mathrm{norm}}, I_{t+1})\big)$。
- **决策**：沿用累积距离刷新规则 $\sum_{s=t_a}^{t_b-1} \widetilde{\Delta}_s \leq \delta < \sum_{s=t_a}^{t_b} \widetilde{\Delta}_s$，在 $t_b$ 处刷新，$[t_a, t_b-1]$ 区间复用缓存输出。

### 与基线方法的模块差异

SeaCache 相对于现有缓存方法的**唯一改动**在于距离度量槽位：

| 方法 | 缓存距离度量 |
|------|-------------|
| **TeaCache** | 原始特征空间相对 L1 距离 $\Delta_t = \mathrm{L1_{rel}}(I_t, I_{t+1})$ |
| **TaylorSeer** | 基于泰勒展开预测输出变化 |
| **DiCache** | 输入侧近似距离 |
| **SeaCache** | 频谱感知特征空间相对 L1 距离 $\widetilde{\Delta}_t = \mathrm{L1_{rel}}\big(\mathcal{P}(G_t^{\mathrm{norm}}, I_t), \mathcal{P}(G_{t+1}^{\mathrm{norm}}, I_{t+1})\big)$ |

由于累积刷新规则保持不变，SeaCache 可作为**即插即用模块**嵌入 DiCache 等现有缓存方案。消融实验证实，将 SEA 滤波器嵌入 DiCache 后（DiCache+Ours），在相同刷新率下 PSNR 始终高于原始 DiCache（Figure 9）。

### 频谱演化的直觉

Figure 1 和 Figure 4 揭示了扩散模型去噪过程的频谱特性：早期时间步的滤波器 $G_t(f)$ 主要保留低频成分（粗糙结构），随着去噪推进，滤波器逐渐纳入高频成分（细节纹理）。SeaCache 通过将这一先验编码进距离度量，使缓存决策更准确地反映内容冗余，避免高频噪声对距离计算的干扰。Oracle 实验（Figure 2）表明，基于 SEA 滤波输出距离的缓存调度相比基于原始输出距离的调度，在相同刷新率下实现更高的 PSNR，更好地跟踪全计算轨迹。

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/001_Figure_1.jpg]]
*Figure 1: Conceptual illustration and motivation of the proposed caching scheme (SeaCache) compared with previous caching schemes. The lower panel shows a denoising trajectory of a cat image where coarse low-frequency structure appears at early steps and fine high-frequency details emerge at later steps, illustrating the spectral evolution of iterative generative models. SeaCache applies a Spectral-Evolution-Aware (SEA) Filter to raw diffusion features so that the distance measure better captures timestepaware spectral residuals between timesteps*

## 核心模块与公式推导

SeaCache 的核心设计是将扩散模型去噪轨迹中的频谱演化先验显式编码进缓存调度，通过三个紧密协作的模块实现：**SEA 滤波器设计**、**频谱特征变换**和**频谱感知动态缓存**。整个流程作为即插即用的缓存策略，仅替换距离度量，不改变去噪器结构或训练过程。

### SEA 滤波器设计

扩散模型的前向加噪过程可统一表示为：

$$x_{t} = a_{t} x_{0} + b_{t} \varepsilon, \qquad \varepsilon \sim \mathcal{N}(0, \mathbf{I})$$

其中 $a_t$ 和 $b_t$ 由具体调度决定。在该框架下，最优线性去噪器在 Wiener 准则下的频率响应为：

$$G_{t}(f) = \frac{a_{t} S_{x}(f)}{a_{t}^{2} S_{x}(f) + b_{t}^{2}}$$

这里 $S_{x}(f)$ 表示干净信号 $x_0$ 的功率谱密度，假设遵循自然图像的幂律谱 $S_{x}(f) \propto 1/f^{\alpha}$。该响应具有明确的时间步依赖性：早期时间步 $a_t$ 较大而 $b_t$ 较小，$G_t(f)$ 主要保留低频成分；随着去噪推进，高频响应逐渐增强（见 Figure 4a）。这精确刻画了“粗粒度结构先恢复、高频细节后出现”的频谱演化规律。

为使不同时间步的滤波能量可比，引入密度归一化：

$$\nu_{t} = \Big( \frac{1}{L} \sum_{f_{\ell} \in \mathcal{F}} G_{t}(f_{\ell}) \Big)^{-1}, \quad G_{t}^{\mathrm{norm}}(f) = \nu_{t} G_{t}(f)$$

归一化后的滤波器 $G_t^{\mathrm{norm}}(f)$ 在所有时间步保持恒定平均增益（见 Figure 4b），确保后续距离度量不受滤波能量尺度差异的干扰。

### 频谱特征变换

对每个时间步的输入特征 $I_t$，应用快速傅里叶变换后与归一化 SEA 滤波器逐元素相乘，再通过逆变换获得频谱感知特征：

$$\mathcal{P}(G_{t}^{\mathrm{norm}}, I_{t}) = \mathrm{iFFT}\big(G_{t}^{\mathrm{norm}}(f) \odot \mathrm{FFT}(I_{t})\big)$$

该操作在频率域选择性增强信号成分、抑制噪声成分，使特征表示更突出内容冗余而非噪声波动。

### 频谱感知动态缓存

在滤波后的特征空间计算相对 L1 距离，替代传统缓存方法中直接在原始特征空间度量的 $\Delta_t$：

$$\widetilde{\Delta}_{t} = \mathrm{L1_{rel}}\big( \mathcal{P}(G_{t}^{\mathrm{norm}}, I_{t}), \mathcal{P}(G_{t+1}^{\mathrm{norm}}, I_{t+1}) \big)$$

其中原始相对 L1 距离定义为：

$$\Delta_{t} = \mathrm{L1_{rel}}(I_{t}, I_{t+1}) = \frac{\| I_{t} - I_{t+1} \|_{1}}{\| I_{t+1} \|_{1} + \xi}$$

缓存刷新决策沿用累积距离规则：当自上次刷新 $t_a$ 起的累积 $\widetilde{\Delta}$ 超过阈值 $\delta$ 时触发新的去噪器计算，否则重用缓存输出：

$$\sum_{s=t_a}^{t_b-1} \widetilde{\Delta}_{s} \leq \delta < \sum_{s=t_a}^{t_b} \widetilde{\Delta}_{s}$$

### 设计逻辑的实证支撑

Oracle 实验（Figure 2）表明，基于 SEA 滤波输出距离的缓存调度在相同刷新率下 PSNR 显著高于基于原始输出距离的调度，验证了频谱感知度量能更准确跟踪全计算轨迹。Figure 5 进一步显示，SEA 滤波后的输入距离与输出距离高度一致，而原始输入距离或多项式拟合输入距离在早期时间步的对齐较弱——这正是噪声干扰缓存决策的直接证据。消融实验（Figure 8）证明，SEA 滤波器在 PSNR-刷新率权衡上优于互补滤波器（1-SEA）、无归一化滤波和低通滤波器，确认了频谱选择性设计的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of timestep-dependent denoising filters. (a) Optimal linear denoising responses*

## 实验与分析

### 核心实验设置

所有对比方法使用相同的初始随机种子，生成结果统一保存为PNG（图像）或MP4（视频）格式。全参考指标（PSNR、LPIPS、SSIM）均以**原始未缓存模型的完整计算输出**作为参考真值。缓存预算通过调整阈值δ（TeaCache/SeaCache）或步长S（TaylorSeer）对齐至约50%和30%刷新率两档，在相同GPU（Blackwell Pro 6000 / A100）上测量延迟与TFLOPs。VBench评估涵盖16个维度，各缓存方案使用相同设置以进行公平排名。

### 主实验结果

**FLUX.1-dev 文生图。** 在50步生成设置下，SeaCache在两个预算档位上均显著超越所有基线（Table 1）。在约50%刷新率（δ=0.3）时，SeaCache的PSNR达到26.285 dB，相比TeaCache（20.762 dB）提升**5.5 dB**，相比TaylorSeer（S=3, 22.783 dB）提升**3.5 dB**；LPIPS从TeaCache的0.211降至0.106，SSIM从0.810升至0.893。在更激进的约30%刷新率（δ=0.6）下，SeaCache仍保持21.332 dB PSNR，领先TeaCache（17.214 dB）**4.1 dB**，领先TaylorSeer（S=5, 19.972 dB）**1.4 dB**。

**HunyuanVideo 文生视频。** 在50步设置下，SeaCache的优势进一步扩大（Table 3）。δ=0.19时PSNR达32.39 dB，较TeaCache（23.40 dB）提升**9.0 dB**，较TaylorSeer（24.14 dB）提升**8.2 dB**；LPIPS仅为0.047，SSIM达0.932。这一差距表明视频生成中时间步间的频谱冗余更为显著，频谱感知缓存策略的收益更大。

**Wan2.1 1.3B 文生视频。** SeaCache同样表现突出（Table 4）。δ=0.2时PSNR为26.60 dB，领先TeaCache（20.84 dB）**5.8 dB**，领先TaylorSeer（16.15 dB）**10.5 dB**。TaylorSeer在视频模型上退化严重，可能因其泰勒展开假设在视频潜在空间中不再成立。

**VBench 综合质量评估。** 在HunyuanVideo和Wan2.1 1.3B的VBench 16维评估中，SeaCache在两个预算档位上均取得最低平均排名（Table 9, Table 10），表明频谱感知缓存不仅保护像素级保真度，也更好地维持了语义一致性、运动平滑性等感知质量维度。

**CycleReward 偏好排名。** 在FLUX.1-dev上使用CycleReward进行偏好排序（Table 2），SeaCache在δ=0.3和δ=0.6时分别取得1.91和1.96的平均排名（越低越好），显著优于TeaCache和TaylorSeer，进一步验证了其输出在感知偏好上的优势。

### 消融实验

**频谱选择性滤波的关键作用。** 在FLUX和HunyuanVideo上，将SEA滤波器替换为互补滤波器（1−SEA）、无密度归一化的原始滤波器、或30%截止频率的低通滤波器，绘制PSNR-刷新率权衡曲线（Figure 8，Sec. 5.4）。结果表明：SEA滤波器在所有刷新率下均取得最优PSNR，互补滤波器表现最差（因其放大噪声而非信号），低通滤波器次之，无归一化滤波器在低刷新率下退化明显。这证实了**频谱选择性**（而非简单滤波）和**密度归一化**是SeaCache设计的两个关键要素。

**即插即用的模块化验证。** 将SEA滤波度量嵌入DiCache后（DiCache+Ours），在FLUX上绘制PSNR-刷新率曲线（Figure 9，Sec. 5.4）。在相同刷新率下，DiCache+Ours的PSNR始终高于原始DiCache，证明SEA滤波可作为**独立于缓存策略的即插即用模块**，改善现有基于特征距离的缓存方案。

**刷新分布模式分析。** 在30%刷新率预算下，SeaCache自动将大部分刷新集中在早期时间步（Figure 10，Sec. 5.4），与频谱演化中早期低频结构更重要的先验一致。相比之下，TeaCache的刷新分布更为均匀，未能有效利用频谱演化的时序特性。

### 运行时开销分析

SEA滤波的额外计算主要来自FFT/iFFT操作。在FLUX.1-dev上，单样本过滤开销约**0.8 ms**（Table 5），在Wan2.1-14B-T2V上，从480p到720p分辨率，开销从**1.2 ms到2.5 ms**（Table 6）。考虑到缓存策略节省的完整去噪器前向计算（通常数十至数百毫秒），这一开销可忽略不计，保证了SeaCache的实用加速比。

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/015_Table_5.jpg]]
*Table 5: Runtime overhead of SEA filtering per sample, averaged over 10 runs*

### 与蒸馏/高效注意力方案的兼容性

SeaCache与LightX2V、Jenga等快速推理方案可叠加使用（Table 12），在已加速的基线上进一步降低延迟，且质量退化保持在可控范围。这表明频谱感知缓存与模型压缩/高效计算方案是正交的加速维度。

### 失败模式与局限性

1. **谱先验假设偏差。** 推导最优线性滤波器时假设信号服从幂律谱、宽平稳且与噪声独立。当生成内容高度合成、背景无显著物体或纹理异常时，功率谱可能偏离自然图像先验，导致滤波偏差和缓存决策准确性下降。
2. **潜在空间近似误差。** 滤波器设计在图像/视频域进行，而现代扩散模型工作在潜在空间。编码器可能改变频谱分布，因此所得滤波器仅为潜在空间响应的近似，在潜在空间频谱与像素域差异较大时可能引入额外误差。
3. **极端低预算下的退化。** 当刷新率降至约20%以下时，即使SEA滤波也难以准确捕捉所有关键时间步的残差，质量退化加速。这是所有缓存方法的共性瓶颈，源于去噪轨迹中不可压缩的信息增量。

### 未解决的问题

- 能否放松幂律谱和平稳性假设，设计内容自适应的时变滤波器，以处理合成场景和异常纹理？
- 是否可以直接在潜在空间估计频谱并设计滤波器，避免像素域先验与潜在空间的分布偏移？
- 在保持即插即用特性的前提下，可否引入轻量级非线性校正（如小型可学习残差模块）来进一步提升缓存保真度？

### 补充图表

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison in FLUX.1-dev [28, 29]*

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/007_Table_3.jpg]]
*Table 3: Quantitative comparison in HunyuanVideo [27]*

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/011_Table_4.jpg]]
*Table 4: Quantitative comparison in Wan2.1 1.3B [63]*

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/013_Figure_8.jpg]]
*Figure 8: Ablation on spectrum-aware filtering. Trade-offs for different cache metrics on FLUX and HunyuanVideo. Results are averaged over 200 prompts for FLUX and 20 randomly selected from VBench for HunyuanVideo, with the other settings fixed*

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/014_Figure_9.jpg]]
*Figure 9: Plug-and-play adaptation to DiCache. PSNR-refresh ratio trade-off on FLUX when applying the SEA-based cache metric to DiCache [6]. “DiCache+Ours” denotes DiCache combined with our SEA filter, while “DiCache” uses the original metric*

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/012_Figure_10.jpg]]
*Figure 10: Refresh pattern across timesteps on FLUX. Pertimestep refresh ratio at a 30% budget. (a) SeaCache automatically concentrates refreshes on early timesteps, whereas (b) Tea-Cache spreads refreshes more uniformly over the trajectory*

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/008_Table_2.jpg]]
*Table 2: Comparison of average rank on CycleReward [4]*

![[assets/figures/papers/paper_list_l2053_https_arxiv_org_abs_2602_18993/figures/002_Figure_2.jpg]]
*Figure 2: Latency-quality trade-off in oracle experiments. We compare cache decisions based on raw output differences and SEA-filtered output differences (Sec. 4.1) on FLUX [28, 29] and Wan2.1 1.3B [63]. The refresh ratio is the fraction of timesteps that run a full denoiser evaluation instead of reusing cached features. For each criterion, PSNR is computed between the cached sample and the corresponding full timestep (no-cache) sample, averaged over each prompt set [23, 49]. At matched refresh ratios, the filtered criterion consistently achieves higher PSNR with respect to the full-compute trajectory, validating the effectiveness of a spectrum-aware distance for cache scheduling*

## 方法谱系与知识库定位

### 与现有缓存加速方法的关系

扩散/流模型推理加速领域已涌现多种缓存策略，SeaCache 在**缓存距离度量**这一关键环节进行了根本性改进，与现有工作形成互补而非替代关系。

**动态缓存方法的共同框架。** 当前主流的动态缓存方案——包括 **TeaCache**、**TaylorSeer** 和 **DiCache**——共享一个核心范式：在相邻时间步之间比较中间特征的变化程度，当累积变化超过阈值时触发去噪器刷新，否则复用缓存输出。这一范式的缓存调度质量完全取决于所选距离度量能否准确反映内容冗余。SeaCache 正是在这一框架下，将距离计算从原始特征空间迁移到频谱演化感知的特征空间，而不改变累积规则（Eq. (4)）或缓存架构本身。

**与 TeaCache 的关系。** TeaCache 直接计算相邻时间步输入特征 $I_t$ 和 $I_{t+1}$ 之间的相对 L1 距离作为缓存决策依据。SeaCache 保留了 TeaCache 的动态阈值调度机制，但将距离度量替换为经 SEA 滤波器与密度归一化后的频谱感知特征之间的相对 L1 距离 $\widetilde{\Delta}_t$（Eq. (8)）。这一替换的动机在于：原始特征空间包含大量高频噪声，这些噪声在早期时间步尚未被去噪器有效抑制，导致原始距离无法准确反映信号层面的内容变化。实验表明，在相同刷新率预算下，SeaCache 在 FLUX.1-dev 上将 PSNR 提升 3.5–5.5 dB（Table 1），在 HunyuanVideo 上提升 8.2–9.0 dB（Table 3），证实了频谱感知度量对缓存决策质量的系统性改善。

**与 TaylorSeer 的关系。** TaylorSeer 利用泰勒展开预测不同时间步的输出变化，是一种基于多项式外推的缓存策略。该方法在数学形式上与 SeaCache 正交：TaylorSeer 关注输出侧的预测精度，而 SeaCache 关注输入侧特征空间的频谱对齐。两者的互补性体现在：TaylorSeer 在输出变化平滑的区间表现良好，但在频谱快速演化的早期时间步容易出现外推偏差；SeaCache 通过显式编码频谱先验，在早期时间步实现了更准确的冗余判断（Figure 5 显示 SEA 滤波后的输入距离与输出距离高度对齐，而多项式拟合输入距离在早期步的对齐较弱）。

**与 DiCache 的关系。** DiCache 是针对 DiT 架构设计的输入侧近似距离缓存策略。SeaCache 的即插即用特性使其可以直接嵌入 DiCache 框架：消融实验（Figure 9）表明，将 SEA 滤波器嵌入 DiCache 后（DiCache+Ours），在相同刷新率下 PSNR 始终高于原始 DiCache，验证了频谱感知度量作为通用模块改善现有缓存方案的潜力。

**与固定缓存方案的关系。** **MagCache** 采用基于幅度阈值的固定缓存策略，不根据内容动态调整刷新位置。SeaCache 在相同刷新率下与 MagCache 的对比（Table 13, Figure 11）显示动态频谱感知调度在质量保持上的优势。**ToCa** 基于 token 剪枝实现加速，与特征缓存属于不同的加速范式，但两者可正交叠加。

### 适用边界与关键假设

SeaCache 的滤波器设计基于三个核心假设，这些假设定义了方法的适用边界：

1. **信号功率律谱假设。** 推导最优线性去噪滤波器 $G_t(f)$（Eq. (5)）时，假设自然图像的功率谱 $S_x(f)$ 遵循 $1/f$ 衰减规律。这一假设在自然场景图像/视频中广泛成立，但当生成内容高度合成（如抽象纹理、纯色背景、无显著物体的场景）时，实际功率谱可能偏离自然图像先验，导致滤波器频率选择性失配，缓存决策准确性可能下降。

2. **宽平稳性与独立性假设。** Wiener 滤波推导要求信号与噪声相互独立且信号宽平稳。实际扩散模型的潜在空间特征可能不严格满足这些条件，尤其是在模型架构引入空间相关性的情况下。论文明确承认这一局限，指出所得滤波器仅为潜在空间响应的近似。

3. **像素域先验在潜在空间的适用性。** 现代扩散模型（如 FLUX、HunyuanVideo、Wan2.1）工作在 VAE 编码的潜在空间，而 SEA 滤波器基于像素域的自然图像统计推导。编码器可能改变频谱分布（例如通过下采样压缩高频），因此滤波器在潜在空间的频率选择性可能与理论设计存在偏差。论文将此列为开放问题，建议未来直接在潜在空间估计频谱并设计内容自适应滤波器。

### 方法局限与失效模式

除上述假设带来的理论局限外，实验和分析揭示了以下实际约束：

**滤波器设计的近似性质。** Figure 4 可视化了不同时间步的 $G_t(f)$ 和 $G_t^{\text{norm}}(f)$：早期时间步滤波器主要保留低频成分，后期逐步纳入高频。这一演化模式与扩散模型的粗到细生成特性一致，但滤波器的具体形状依赖于功率谱假设的准确性。当实际生成内容偏离假设时，滤波器可能过度抑制或过度保留某些频率分量，影响距离度量的保真度。

**计算开销与分辨率的关系。** SEA 滤波涉及 FFT/iFFT 操作，其开销随分辨率增长。Table 5 和 Table 6 报告了不同设置下的运行时开销：在标准分辨率下，滤波开销相对于去噪器前向传播可忽略；但在高分辨率视频生成（如 Wan2.1-14B-T2V）中，FFT 开销可能成为需要考虑的因素。这限制了方法在极高分辨率场景下的效率优势。

**极端缓存预算下的退化。** 当刷新率极低（如 30% 以下）时，即使频谱感知度量也无法完全补偿信息损失。Table 1 显示 SeaCache 在 δ=0.6（约 30% 刷新率）下的 PSNR 为 21.332 dB，虽显著优于基线（TeaCache 17.214 dB），但与全计算轨迹仍有差距。这表明缓存策略存在信息论下界，频谱先验的注入可以提升效率边界但无法突破。

### 开放问题与未来方向

论文明确指出了三个值得探索的方向：

1. **放松谱先验假设。** 当前滤波器设计依赖功率律谱、平稳性和独立性假设。如何设计更精确的时变滤波器，使其能适应多样化的生成内容和模型架构，是一个重要的理论问题。可能的方向包括：从数据中学习时间步相关的滤波器参数，或引入轻量级自适应机制在线调整频率响应。

2. **潜在空间原生频谱建模。** 直接在潜在空间估计频谱分布并设计内容自适应滤波器，可避免像素域先验与潜在空间之间的分布偏移。这需要研究 VAE 编码器对频谱的变换特性，并设计相应的校正机制。

3. **非线性校正与即插即用性的平衡。** 在保持即插即用特性的前提下，引入轻量级非线性校正（如小型可学习网络调整滤波器响应）可能进一步提升缓存保真度。Figure 9 的 DiCache 嵌入实验已初步验证了模块化设计的可行性，未来可探索更丰富的适配形式。

此外，Figure 10 揭示的刷新模式（SeaCache 自动将大部分刷新集中在早期时间步）暗示频谱感知度量隐式编码了生成过程的时间重要性先验，这为理解扩散模型去噪轨迹的信息动态提供了新的分析视角。

## 原文 PDF

![[paperPDFs/CVPR_2026/SeaCache_Spectral_Evolution_Aware_Cache_for_Accelerating_Diffusion_Models.pdf]]