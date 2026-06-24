---
title: "Autoregressive-based Progressive Coding for Ultra-Low Bitrate Image Compression"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Autoregressive_based_Progressive_Coding_for_Ultra_Low_Bitrate_Image_Compression.pdf
aliases:
- ABPCA
- ABPCULBIC
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "用VAR下一尺度预测和分组掩码残差量化实现渐进式超低码率压缩。"
primary_logic: "ARPC先传输粗尺度离散token和图像描述，再由VAR预测未接收尺度并用概率估计支持无损熵重编码。"
claims:
- "VAR从粗到细的下一尺度预测天然适合按尺度渐进传输图像信息。"
- "单个ARPC模型可通过选择传输尺度数量支持多码率压缩。"
- "基于VAR概率的无损熵重编码在不损害质量的情况下降低约30%比特率。"
- "ARPC在超低码率下取得强感知质量，解码速度比扩散压缩方法快2到6倍。"
---

# Autoregressive-based Progressive Coding for Ultra-Low Bitrate Image Compression

> [!tip] 核心洞察
> 核心洞察是：VAR的从粗到细（coarse-to-fine）生成范式天然契合渐进式压缩——先传输包含布局等关键信息的粗尺度，再逐步添加细粒度纹理细节以提升图像质量。同时，VAR相比扩散模型具有更快的生成速度，且无需发送端和接收端共享随机性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于自回归的渐进式超低比特率图像压缩编码 |
| 英文题名 | Autoregressive-based Progressive Coding for Ultra-Low Bitrate Image Compression |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=FXu4G5T5QZ); [GitHub](https://github.com/Joanna-0421/ARPC) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | AutoRegressive-based Progressive Coding (ARPC) |
| Dataset | CLIC2020 (1024×1024) |

> [!tip] 效果简介
> - CLIC2020 (1024×1024) 上，BD-rate (FID) 为 0，对比 ARPC作为基线，变化 N/A。
> - CLIC2020 (1024×1024) 上，BD-rate (DISTS) 为 0，对比 ARPC作为基线，变化 N/A。
> - CLIC2020 (1024×1024) 上，BD-rate (PIEAPP) 为 0，对比 ARPC作为基线，变化 N/A。

## 概述

本文提出了一种基于自回归的渐进式图像压缩编码方法（AutoRegressive-based Progressive Coding, ARPC），旨在解决超低比特率（ultra-low bitrate）下图像压缩的感知保真度与解码效率问题。ARPC 利用视觉自回归模型（Visual AutoRegressive model, VAR）的下一尺度预测（next-scale prediction）范式，通过多尺度残差向量量化器将图像编码为离散的分层视觉token，并仅选择前k个尺度进行传输，利用VAR的自回归生成能力预测未接收的尺度，从而实现渐进式编码。实验表明，ARPC在超低比特率下实现了最先进的感知保真度，且解压效率比现有基于扩散模型的方法高2-6倍。

## 背景与动机

现有基于扩散模型的超低比特率图像压缩方法面临三大瓶颈：

1.  **比特率适应性有限**：通常采用每速率单模型训练范式，难以适应动态传输环境。
2.  **编解码计算复杂度高**：扩散模型的迭代去噪本质引入不可避免的复杂性。
3.  **需要发送端和接收端共享随机性**：这在许多实际场景中不可用。

核心洞察是：VAR的从粗到细（coarse-to-fine）生成范式天然契合渐进式压缩——先传输包含布局等关键信息的粗尺度，再逐步添加细粒度纹理细节以提升图像质量。同时，VAR相比扩散模型具有更快的生成速度，且无需发送端和接收端共享随机性。

## 核心创新

ARPC 的核心创新在于将视觉自回归模型（VAR）的下一尺度预测范式引入图像压缩领域，具体包括：

1.  **渐进式编码框架**：利用多尺度残差向量量化器将图像编码为K个尺度的离散token图，通过选择不同传输尺度控制比特率，单模型支持多速率。
2.  **基于VAR的解码生成**：利用VAR的下一尺度预测能力，以自回归方式从粗到细生成未接收的尺度，无需共享随机性，解码速度提升2-6倍。
3.  **基于VAR概率估计的无损熵重编码（LRE）**：将VAR作为概率估计器，利用其c个二元分类器预测每个token的分布，用于算术编码，实现约30%的比特率降低。
4.  **分组掩码bitwise多尺度残差量化器（GM-BMSRQ）**：对前几个尺度的通道进行掩码（第一组掩码后c/2通道，第二组掩码后c/4通道），实现更紧凑的表示。

## 整体框架

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_FXu4G5T5QZ_Autoregr/figures/001_Figure_1.jpg]]
*Figure 1: Qualitative comparison between ARPC and diffusion-based methods. ARPC effectively reconstructs fine-grained textural details, while other methods exhibit noticeable texture loss.*

ARPC的整体框架如Figure 2所示，包含以下主要模块：

1.  **图像编码器（Image Encoder E）**：将输入图像x编码为特征图F。
2.  **分组掩码bitwise多尺度残差量化器（GM-BMSRQ）**：将特征图F量化为K个尺度的残差token图(R_1,...,R_K)，对前几个尺度进行通道掩码以减少比特数。
3.  **BLIP2图像描述生成器**：生成图像描述t作为全局语义上下文，与token一起传输。
4.  **算术编解码器（Arithmetic Codec A）**：基于VAR预测的概率分布对token索引进行无损熵编码/解码。
5.  **视觉自回归模型（VAR）**：作为概率估计器用于熵编码，并作为生成器预测未接收的尺度token。
6.  **图像解码器（Image Decoder D）**：将完整的K个尺度token上采样并拼接后重建为图像。

## 核心模块与公式推导

### 5.1 尺度token概率的自回归分解

所有尺度token的联合概率被分解为条件概率的乘积：

$$p(R_1, R_2, ..., R_K) = \prod_{i=1}^{K} p(R_k | R_1, ..., R_{k-1}, C)$$

其中每个尺度token R_k 基于之前尺度和文本嵌入C进行预测。

### 5.2 Bitwise多尺度残差量化器

每个c维向量被映射为一个c-bit二进制码：

$$r_{i,j} = R_k^{(i,j)} = \frac{1}{\sqrt{c}} sign(\frac{r_{i,j}}{|r_{i,j}|})$$

尺度k的累积特征图定义为：

$$F_k = \sum_{i=1}^{k} \text{upsample}(R_i, (h, w))$$

### 5.3 渐进编码的失真上界

Theorem 3.1 提供了传输前k个尺度时的期望失真上界：

$$\mathbb{E}[D_k] \leq \mathbb{E}[D_K] + C \cdot \mathbb{E}_{R_{\leq k}}[D_{KL}(p(R_{>k}|R_{\leq k}) \| p_\theta(R_{>k}|R_{\leq k}))]$$

该上界表明，期望失真受限于真实token重建的期望失真加上真实分布与预测分布之间KL散度的常数倍。

### 5.4 训练损失

第一阶段训练编码器、解码器和量化器：

$$\mathcal{L}_{first} = \mathcal{L}_{rec} + \mathcal{L}_{per} + \mathcal{L}_{dis} + \mathcal{L}_{commit} + \mathcal{L}_{entropy}$$

第二阶段训练VAR：

$$\mathcal{L}_{VAR} = -\sum_{i=1}^{K} \log p_\theta(R_i | R_{<i})$$

### 5.5 二进制索引编码

将bitwise量化器的输出转换为每个token的整数索引：

$$y_k(i,j) = \sum_{n=0}^{c-1} \mathbb{1}_{R_k(i,j,n) > 0} 2^n$$

## 实验与分析

### 6.1 主要结果

ARPC在CLIC2020和DIV2K两个标准测试集上进行了评估，与13个最先进的基线方法进行了比较，包括ELIC、MS-ILLM、DiffEIC、DiffPC、RDEIC、ResULIC、StableCodec、OSCAR、DiffC、VQGAN、GLC、DLF等。

**Table 1: Inference efficiency and BD-rate (%) comparison on CLIC2020 dataset (1024×1024).**

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_FXu4G5T5QZ_Autoregr/figures/006_Table_1.jpg]]
*Table 1: Inference efficiency and BD-rate (%) comparison on CLIC2020 dataset (1024×1024).*

| 方法 | 编码时间 (s) | 解码时间 (s) | BD-rate (FID) | BD-rate (DISTS) | BD-rate (PIEAPP) |
|------|-------------|-------------|---------------|----------------|------------------|
| ARPC (w/ LRE) | 6.21 | 5.39 | 0 | 0 | 0 |
| ARPC (w/o LRE) | 0.20 | 5.39 | 34.64 | 34.58 | 34.38 |

**关键发现：**
- ARPC在FID、DISTS、PIEAPP指标上的BD-rate均为0（作为基线）。
- ARPC的解码时间为5.39秒，比扩散方法快2-6倍。
- 基于VAR预测概率的无损熵重编码（LRE）可在不影响图像质量的情况下降低约30%的比特率。

**Figure 3: Quantitative comparisons with SOTA methods on the DIV2K and CLIC2020 datasets.**

**Figure 4: Visual comparison of generative compression methods at ultra-low bitrates (<0.01bpp). SC denotes the StableCodec.**

### 6.2 消融研究

**Table 2: The effect of GM-BMSRQ and SRD on visual tokenizer.**

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_FXu4G5T5QZ_Autoregr/figures/010_Table_2.jpg]]
*Table 2: The effect of GM-BMSRQ and SRD on visual tokenizer.*

| 配置 | rFID | PSNR |
|------|------|------|
| Original | 0.31 | 22.6 |
| W/ GM-BMSRQ | 0.56 | 22.12 |
| W/ GM-BMSRQ W/ SRD | 0.67 | 21.5 |

**Table 3: BD-rate of different mask configuration for GM-BMSRQ.**

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_FXu4G5T5QZ_Autoregr/figures/012_Table_3.jpg]]
*Table 3: BD-rate of different mask configuration for GM-BMSRQ.*

| 配置 | BD-rate (DISTS) | BD-rate (FID) |
|------|-----------------|---------------|
| (5,6,2) | 25.69 | 64.19 |
| (2,2,9) | 17.29 | 29.87 |

**Table 4: BD-rate comparison with vanilla VAR.**

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_FXu4G5T5QZ_Autoregr/figures/013_Table_4.jpg]]
*Table 4: BD-rate comparison with vanilla VAR.*

| 方法 | BD-rate (DISTS) | BD-rate (FID) |
|------|-----------------|---------------|
| Vanilla VAR | 63.32 | 79.51 |
| StableCodec | 10.78 | 22.47 |
| ARPC | 0 | 0 |

**消融研究结论：**
- 分组掩码（GM-BMSRQ）有效提升了压缩比，尤其在超低比特率下。
- 尺度随机丢弃（SRD）策略增强了早期尺度的表示能力，提升了低比特率下的重建保真度。
- GM-BMSRQ和SRD策略对VAE的整体重建能力有轻微影响（rFID从0.31升至0.67，PSNR从22.6降至21.5）。
- 图像描述在超低比特率下对解压质量至关重要；没有描述时质量严重下降。

### 6.3 效率分析

**Table 5: The encoding time and bitrate when selecting different k.**

![[assets/figures/papers/iclr26_generative_models_diffusion__generative_models_and_autoencoders__b001_FXu4G5T5QZ_Autoregr/figures/014_Table_5.jpg]]
*Table 5: The encoding time and bitrate when selecting different k.*

| k | 编码时间 (s) | 比特率 (bpp) |
|---|-------------|-------------|
| 1-10 | <3 | <0.025 |
| 11 | 2.77 | - |
| 12 | 4.09 | - |
| 13 | 6.21 | - |

**Table 6: Inference efficiency with different input image size.**

### 6.4 轻量化部署

**Table 7: Model parameters for lightweight deployment using BLIP and w/o LRE.**

| 组件 | 参数量 |
|------|--------|
| BLIP | 223.9M |
| VAR (w/o VAE) | 2.2B |
| VAE | 44.9M |
| Total w/ LRE | 2.2B |
| Total w/o LRE | 268.8M |

**Table 8: BD-rate comparison for lightweight deployment using BLIP and w/o LRE. The BD-rate is calculated on DIV2K dataset with using BLIP-2 caption model and LRE as the baseline.**

| 配置 | BD-rate (DISTS) | BD-rate (FID) |
|------|-----------------|---------------|
| BLIP + w/ LRE | 0.12 | 0.08 |
| BLIP + w/o LRE | 25.93 | 25.56 |

## 方法谱系与知识库定位

ARPC 属于生成式图像压缩（generative image compression）领域，具体位于以下方法谱系中：

1.  **VAE-based 方法**：如 ELIC、MS-ILLM，侧重于率失真优化，但在超低比特率下感知质量有限。
2.  **Diffusion-based 方法**：如 DiffEIC、DiffPC、RDEIC、ResULIC、StableCodec、OSCAR、DiffC，通过迭代去噪实现高感知质量，但计算复杂度高且需要共享随机性。
3.  **GAN-based 方法**：如 VQGAN、GLC、DLF，通过对抗训练提升感知质量，但训练不稳定。
4.  **ARPC**：首次将视觉自回归模型（VAR）的下一尺度预测范式引入图像压缩，实现了渐进式编码、高感知保真度和高效解码的平衡。

ARPC 的核心贡献在于证明了视觉自回归模型不仅可以用于图像生成，还可以作为高效的图像压缩框架，为超低比特率图像压缩提供了新的技术路径。

## 原文 PDF

![[paperPDFs/ICLR_2026/Autoregressive_based_Progressive_Coding_for_Ultra_Low_Bitrate_Image_Compression.pdf]]
