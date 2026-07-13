---
title: "Analyzing the Training Dynamics of Image Restoration Transformers: A Revisit to Layer Normalization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Analyzing_the_Training_Dynamics_of_Image_Restoration_Transformers_A_Revisit_to_Layer_Normalization.pdf
project_link: null
code_link: https://github.com/2minkyulee/i-LN
aliases:
- ILIRTTLN
- ATDIRTRLN
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "i-LN用空间整体归一化和输入自适应重缩放替代图像恢复Transformer中的逐token LayerNorm。"
primary_logic: "先用LN*保留token间空间结构，再按输入尺度重缩放注意力或前馈残差以稳定特征统计。"
claims:
- "逐token LayerNorm会破坏图像恢复任务所需的空间关系并引发特征幅度发散。"
- "i-LN将特征幅度稳定在接近标准正态的范围并缓解通道熵崩溃。"
- "在超分辨率、去雨、去噪和JPEG伪影去除任务上，i-LN通常优于传统LN。"
---

# Analyzing the Training Dynamics of Image Restoration Transformers: A Revisit to Layer Normalization

> [!tip] 核心洞察
> 通过整体归一化（LN*）保留空间结构，并通过输入自适应重缩放恢复丢失的全局尺度，i-LN使特征分布稳定在N(0,1)附近（幅度约1.2），从而显著提升训练稳定性和恢复性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 图像恢复Transformer训练动态分析：重新审视层归一化 |
| 英文题名 | Analyzing the Training Dynamics of Image Restoration Transformers: A Revisit to Layer Normalization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=SbLj5hJXh6) · [GitHub](https://github.com/2minkyulee/i-LN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | i-LN (Image Restoration Transformer Tailored Layer Normalization) |
| Dataset | Set14, BSD100 |

> [!tip] 效果简介
> - Set14 上，PSNR 为 29.01，对比 28.79，变化 +0.22。
> - Set14 上，SSIM 为 .7915，对比 .7876，变化 +0.0039。
> - BSD100 上，PSNR 为 27.84，对比 27.68，变化 +0.16。

## 概要

本文系统分析了传统LayerNorm（LN）在图像恢复（Image Restoration, IR）Transformer中导致训练不稳定的根本原因，并提出了一种专门为IR Transformer定制的层归一化方法——i-LN（Image Restoration Transformer Tailored Layer Normalization）。研究发现，传统逐token的LayerNorm与IR任务之间存在两个根本性错配：1）逐token归一化破坏了token间的空间相关性；2）与输入无关的缩放丢弃了输入特定的统计信息。这导致特征幅度发散至百万量级，并造成通道熵急剧下降。i-LN通过空间整体归一化（LN*）保留空间结构，并通过输入自适应重缩放恢复丢失的全局尺度，使特征分布稳定在N(0,1)附近（幅度约1.2），从而显著提升训练稳定性和恢复性能。在×4超分辨率（SR）任务上，i-LN在Set14、BSD100、Urban100、Manga109四个基准上均取得最佳PSNR/SSIM。

图像恢复任务（如超分辨率、去噪、去雨、JPEG伪影去除）要求网络精确保持输入图像的低级特征和空间结构。然而，当前主流的IR Transformer架构（如SwinIR (Liang et al., 2021)、HAT (Chen et al., 2023a)、DRCT (Hsu et al., 2024)）普遍采用从高层视觉任务（如ViT (Dosovitskiy et al., 2020)）继承而来的逐token LayerNorm。

本文通过实验发现，传统LN在IR Transformer中导致两个严重问题（Figure 1）：
- **特征幅度发散**：特征幅度在训练过程中急剧增长，达到百万量级。
- **通道熵崩溃**：通道熵在训练早期急剧下降，表明激活集中在少数通道中。

进一步分析表明（Figure 2），这一发散现象在不同网络深度、宽度以及多种IR任务（SR、DN、DR、CAR）中普遍存在，且随网络规模增大而加剧。完全移除归一化层会导致训练不稳定和无法收敛（Table 1）。

## 核心方法与创新机理

本文的核心创新是提出了i-LN（Image Restoration Transformer Tailored Layer Normalization），作为传统LayerNorm的即插即用替代方案。i-LN包含两个关键组件：

1. **空间整体归一化（LN*）**：在空间-通道维度上进行整体归一化，保留token间的空间结构。
2. **输入自适应重缩放**：在注意力层和前馈层之后，使用LN*计算的标准差进行输入自适应重缩放，恢复丢失的全局尺度信息。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_SbLj5hJXh6_Analyzing_the/figures/001_Figure_1.jpg]]
*Figure 1: (a) Feature Magnitudes*

Figure 3对比了传统LN和i-LN的Transformer块结构。传统LN对每个token独立进行归一化，而i-LN在空间-通道维度上进行整体归一化，并在注意力层和前馈层之后进行输入自适应重缩放。

i-LN的完整块定义如下：

**LN*（空间整体归一化）**：
$$\operatorname{LN}^{*}(x) = \gamma \frac{1}{\sqrt{\sigma^{2} + \epsilon}} (x - \mu) + \beta, \quad \mu = \mathbb{E}_{\ell,c}[x_{\ell,c}], \quad \sigma^{2} = \mathbb{E}_{\ell,c}[(x_{\ell,c} - \mu)^{2}]$$

**i-LN块**：
$$B(x; f, i\text{-}\mathrm{LN}) = x + \sqrt{\sigma^{2} + \epsilon} \cdot f(\mathrm{LN}^{*}(x))$$

其中$f$表示注意力层或前馈层。

### 5.1 逐token LayerNorm的问题

标准逐token LayerNorm定义为：
$$\mathrm{LN}(x_{\ell}) = \gamma \frac{1}{\sqrt{\sigma_{\ell}^{2} + \epsilon}} (x_{\ell} - \mu_{\ell}) + \beta, \qquad \mu_{\ell} = \mathbb{E}_{c}[x_{\ell,c}], \qquad \sigma_{\ell}^{2} = \mathbb{E}_{c}[(x_{\ell,c} - \mu_{\ell})^{2}]$$

**Proposition 1**（LN不保结构）：逐token LN在token集上甚至不是共形映射，因此不保结构。对于两个token $\ell, k$，LN后的差分为：
$$T_{\mathrm{LN}}(x_{\ell}) - T_{\mathrm{LN}}(x_{k}) = a Q(x_{\ell} - x_{k}) \quad \text{for all } x_{\ell}, x_{k}$$

其中$Q$不是恒等缩放，因此LN破坏了token间的空间关系。

### 5.2 LN*的保结构性质

**Proposition 2**（LN*保结构）：LN*是homothety（均匀缩放），保结构至全局尺度：
$$T_{\mathrm{LN}^{*}}(x_{\ell}) - T_{\mathrm{LN}^{*}}(x_{k}) = (1/\sigma)(x_{\ell} - x_{k})$$

这意味着LN*保留了token间的相对空间关系，仅进行全局缩放。

### 5.3 输入自适应重缩放

i-LN在注意力层和前馈层之后，使用LN*计算的标准差进行重缩放：
$$B(x; f, i\text{-}\mathrm{LN}) = x + \sqrt{\sigma^{2} + \epsilon} \cdot f(\mathrm{LN}^{*}(x))$$

这一策略使网络能够保留输入特定的统计信息，并允许中间特征具有范围灵活性。

## 实验与关键发现

### 6.1 主要结果

**Table 1**：不同归一化方案在×4 SR（HAT1骨干）上的定量比较。i-LN在所有四个基准上均取得最佳PSNR/SSIM：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_SbLj5hJXh6_Analyzing_the/figures/009_Table_1.jpg]]
*Table 1: Comparison between various normalization schemes. † indicates that BatchNorm is evaluated in train-mode. SH indicates the spatial holisticness of the normalization scheme, including the setting without any normalization (None). Experiments are performed for ×4 SR with HAT1. The best result for each setting is highlighted in bold.*

| 基准 | 指标 | LN（基线） | i-LN（本文） | 提升 |
|------|------|-----------|-------------|------|
| Set14 | PSNR | 28.79 | **29.01** | +0.22 |
| Set14 | SSIM | .7876 | **.7915** | +0.0039 |
| BSD100 | PSNR | 27.68 | **27.84** | +0.16 |
| BSD100 | SSIM | .7411 | **.7456** | +0.0045 |
| Urban100 | PSNR | 26.55 | **27.17** | +0.62 |
| Urban100 | SSIM | .8015 | **.8167** | +0.0152 |
| Manga109 | PSNR | 31.01 | **31.82** | +0.81 |
| Manga109 | SSIM | .9150 | **.9228** | +0.0078 |

**Table 2**：i-LN在多种IR任务上的定量比较：
- **去雨（Rain100L, HAT1）**：PSNR 36.20 vs 34.35（+1.85），SSIM .9641 vs .9471
- **去雨（Test100, SwinIR1）**：PSNR 29.87 vs 27.45（+2.42），SSIM .8982 vs .8766
- **去噪（σ=15, Urban100, HAT1）**：PSNR 35.558 vs 35.489（+0.069）
- **JPEG伪影去除（q=10, Urban100, HAT1）**：PSNR 28.52 vs 28.45（+0.07），SSIM .8530 vs .8514
- **JPEG伪影去除（q=40, Urban100, HAT1）**：PSNR 33.36 vs 33.26（+0.10），SSIM .9312 vs .9302

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_SbLj5hJXh6_Analyzing_the/figures/011_Table_2.jpg]]
*Table 2: Quantitative comparison between the conventional LayerNorm (LN) and our proposed i-LN across diverse IR tasks. The best result for each setting is highlighted in bold.*

### 6.2 消融研究

**Table 3**：消融研究验证了i-LN两个组件的必要性：
- 移除重缩放策略（Rs）或空间整体性（SH）均会降低恢复质量
- 完整i-LN取得最佳结果：BSD100 27.9206, Urban100 27.5849, Manga109 32.1694
- 基线LN：BSD100 27.7897, Urban100 26.8779, Manga109 31.5444

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_SbLj5hJXh6_Analyzing_the/figures/012_Table_3.jpg]]
*Table 3: (a) Single image super-resolution (SR)*

**Figure 7**：通道熵随i-LN组件的移除呈指数级下降，表明每个组件都对维持跨通道的均匀激活分布有贡献。

### 6.3 与其他稳定化方法的对比

**Table 8**：与梯度裁剪（GC）和KLD正则化的对比：
- GC无法阻止极端特征幅度（最大5.6e6 vs 基线5.8e6）
- KLD正则化稳定了特征统计量，但导致显著的性能下降
- i-LN将特征幅度稳定在约1.2（接近N(0,1)分布），同时持续优于所有替代方案

### 6.4 计算密集型设置下的结果

**Table 6**：在计算密集型设置（HAT†）下，i-LN仍优于LN：
- ×2 SR Set5：38.65/.9631 vs 38.63/.9630
- ×4 SR Set5：33.12/.9064 vs 33.04/.9056

### 6.5 低精度推理

**Table 4**和**Figure 10**：i-LN在低精度推理（int8, int4, fp16）下表现出色，而LN导致严重性能下降：
- fp16：i-LN Urban100 27.5849, Manga109 32.1693；LN Urban100 7.4640, Manga109 5.0736

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_SbLj5hJXh6_Analyzing_the/figures/013_Table_4.jpg]]
*Table 4: (b) Image deraining (DR)*

### 6.6 鲁棒性分析

**Figure 11**：i-LN在多个随机种子下保持稳定一致的结果，而LN表现出显著波动。

**Figure 14**：i-LN在不同批量大小（2, 4, 8）下均优于LN。

### 6.7 定性分析

**Figure 6**：在四个代表性IR任务上，i-LN产生更清晰、更真实的恢复结果。

**Figure 9**和**Figure 12**：i-LN产生结构良好的相对位置嵌入（RPE），表明其更好地理解了像素间的空间关系。

**Figure 8**：LN中仿射偏置参数与通道幅度精确对齐，揭示了补偿机制。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_SbLj5hJXh6_Analyzing_the/figures/014_Table_5.jpg]]
*Table 5: (c) Color image denoising (DN) (d) Image JPEG compression artifact removal (CAR)*

## 定位与知识库关联

### 7.1 与现有归一化方法的关系

本文系统比较了多种归一化方案（Table 1）：
- **逐token归一化**（LN、RMSNorm (Zhang & Sennrich, 2019)、LayerScale (Touvron et al., 2021)）：均导致特征发散
- **空间一致性归一化**（i-LN、BN (Ioffe & Szegedy, 2015)、IN (Ulyanov et al., 2016)、ReZero (Bachlechner et al., 2021)）：不出现发散
- BN在评估模式下性能显著下降，表明IR任务需要基于每张图像统计的归一化
- IN丢弃了关键的通道信息，性能受限
- 完全移除归一化（None）导致训练不稳定和无法收敛

### 7.2 与现有工作的联系

本文建立在以下工作的基础上：
- **IR Transformer架构**：SwinIR (Liang et al., 2021)、HAT (Chen et al., 2023a)、DRCT (Hsu et al., 2024)、SRFormer (Zhou et al., 2023)
- **训练动态分析**：Karras et al. (2024) 在扩散模型中观察到类似的特征幅度发散现象
- **归一化在SR中的作用**：Lim et al. (2017b) 和 Wang et al. (2018) 指出移除BN可提升SR性能

### 7.3 局限性

1. i-LN在去噪（DN）和JPEG伪影去除（CAR）任务上的改进幅度小于超分辨率（SR）和去雨（DR），表明这些任务对归一化错配的敏感性较低。
2. i-LN在计算密集型设置（HAT†）下的改进幅度小于轻量级设置，可能表明更大模型具有更强的鲁棒性。
3. i-LN的输入自适应重缩放策略增加了少量计算开销（乘以标量标准差）。
4. i-LN在真实世界退化场景下的评估仅基于合成数据（Real-ESRGAN管线），在真实退化图像上的泛化能力有待进一步验证。

### 7.4 开放问题

1. i-LN在视频恢复、多帧超分辨率等时间序列IR任务上的表现如何？
2. i-LN是否可以推广到其他需要保空间结构的视觉任务（如图像分割、深度估计）？
3. i-LN中空间整体归一化和输入自适应重缩放两个组件的相对重要性是否随任务和骨干网络变化？
4. i-LN在更大规模模型（如ViT-G）和更极端低精度（如int2）下的表现如何？
5. i-LN与通道注意力机制（如HAT中的通道注意力）之间的相互作用机制是什么？

## 原文 PDF

![[paperPDFs/ICLR_2026/Analyzing_the_Training_Dynamics_of_Image_Restoration_Transformers_A_Revisit_to_Layer_Normalization.pdf]]
