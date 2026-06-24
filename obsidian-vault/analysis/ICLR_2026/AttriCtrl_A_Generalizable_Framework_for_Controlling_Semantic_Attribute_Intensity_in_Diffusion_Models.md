---
title: "AttriCtrl: A Generalizable Framework for Controlling Semantic Attribute Intensity in Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AttriCtrl_A_Generalizable_Framework_for_Controlling_Semantic_Attribute_Intensity_in_Diffusion_Models.pdf
aliases:
- AttriCtrl
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "AttriCtrl用属性量化和值编码器把连续美学强度标量注入扩散模型条件序列。"
primary_logic: "属性先归一化到统一标量空间，再编码成可学习词元并与文本嵌入拼接以控制生成强度。"
claims:
- "文本编码器难以稳定表达连续数值化属性强度。"
- "独立训练的值编码器可组合控制亮度、细节、真实感和安全性等属性。"
- "AttriCtrl在控制误差和用户偏好上优于提示增强、嵌入加权和注意力插值基线。"
---

# AttriCtrl: A Generalizable Framework for Controlling Semantic Attribute Intensity in Diffusion Models

> [!tip] 核心洞察
> 通过混合量化策略（直接度量+视觉-语言语义相似度）将主观美学属性（亮度、细节、真实感、安全性）映射到统一的[0,1]标量空间，再利用值编码器将该标量转化为模型可解释的连续嵌入，从而在扩散模型的隐空间中学习到解耦的、可导航的属性控制向量，实现平滑、精确且独立于其他因素的强度调节。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AttriCtrl：扩散模型中语义属性强度的通用控制框架 |
| 英文题名 | AttriCtrl: A Generalizable Framework for Controlling Semantic Attribute Intensity in Diffusion Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=oyDe8cNXt6) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AttriCtrl |
| Dataset | 自定义测试集（基于FLUX模型）, 用户研究（10位专家，100次比较） |

> [!tip] 效果简介
> - 自定义测试集（基于FLUX模型） 上，AvgDiff ↓ 为 0.141，对比 0.257 (Kontext)，变化 -0.116。
> - 自定义测试集（基于FLUX模型） 上，AvgDiff ↓ 为 0.191，对比 0.295 (Kontext)，变化 -0.104。
> - 自定义测试集（基于FLUX模型） 上，AvgDiff ↓ 为 0.192，对比 0.235 (Kontext)，变化 -0.043。

## 概述

AttriCtrl 是一个面向扩散模型的通用控制框架，旨在实现对图像美学属性（如亮度、细节、真实感、安全性）的精确、连续且可组合的强度控制。该框架的核心创新在于引入了一个轻量级、即插即用的值编码器（Value Encoder），将用户指定的归一化连续标量强度值映射为模型可解释的嵌入序列，从而克服了传统文本编码器（如T5、CLIP）无法直接处理数值化指令的根本局限。实验表明，AttriCtrl 在控制精度（AvgDiff）和用户偏好上均显著优于现有基线方法，并能在保持基础模型冻结的前提下，实现多属性的联合调控。

## 背景与动机

现有文本到图像扩散模型（如Stable Diffusion、FLUX）依赖文本编码器（如T5、CLIP）将用户提示转换为条件嵌入。然而，这些编码器设计用于处理离散词元，对连续数值信息（如“亮度0.7”）不敏感，导致用户无法精确指定美学属性的强度。现有方法如“Add to Prompt”（在提示词中添加形容词）和“Control with Kontext”（追加自然语言指令）均无法建立稳定可靠的属性控制（Figure 1）。基于注意力插值的AID方法虽能实现一定程度的属性调节，但缺乏显式数值指导，常产生光晕和鬼影等伪影（Figure 9）。因此，亟需一种能够将连续数值指令无缝注入扩散模型的方法。

## 核心创新

AttriCtrl 的核心创新可概括为三点：

1. **混合量化策略**：针对不同美学属性，采用直接度量（如HSV亮度均值、香农熵）与视觉-语言语义相似度（CLIP余弦相似度）相结合的混合方法，将主观美学属性映射到统一的[0,1]标量空间。
2. **值编码器（Value Encoder）**：设计一个轻量级神经网络，将归一化标量强度值编码为固定长度的可学习词元序列（默认32个词元），并与文本嵌入拼接后注入扩散模型的注意力层，实现精确的连续控制。
3. **模块化多属性组合**：每个属性独立训练值编码器，推理时按序列拼接各属性嵌入，实现即插即用的多属性联合控制，无需联合训练。

## 整体框架

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_oyDe8cNXt6_AttriCtrl_A_G/figures/001_Figure_1.jpg]]
*Figure 1: Effects of Add to Prompt and Control with Kontext Figure 1: Overview. Methods such as ‘Add to Prompt’ and ‘Control with Kontext’ fail to establish stable or reliable attribute control. In contrast, our proposed AttriCtrl enables fine-grained control over aesthetic attributes by modulating their intensity in the generated image.*

AttriCtrl 的整体框架如 Figure 3 所示，包含三个主要模块：

1. **属性量化模块（Attribute Quantification）**：将输入图像的美学属性量化为[0,1]范围内的归一化标量值。
2. **值编码器（Value Encoder）**：将归一化标量值映射为多尺度表示（词元序列）。
3. **扩散模型主干（DiT Backbone）**：接收文本嵌入和值编码器输出的联合嵌入，执行去噪过程生成最终图像。基础模型保持冻结。

## 核心模块与公式推导

### 5.1 属性量化

**亮度强度**：在HSV颜色空间中提取V通道，计算像素均值并归一化至[0,1]。
$$x_I^{Brightness} = \frac{1}{H \cdot W} \sum_{i=1}^{h} \sum_{j=1}^{w} \frac{v_{i,j}}{255}$$

**细节强度**：采用灰度图像直方图的香农熵，度量纹理丰富度。
$$x_I^{Detail} = \mathrm{Entropy}(\mathrm{Hist}(I)) = -\sum_{k=1}^{256} p_k \log(p_k)$$

**真实感强度**：利用CLIP模型计算图像嵌入与正向提示（如“真实照片”）和负向提示（如“卡通”）的余弦相似度之差。
$$x_I^{Realism} = sim(e_I, e_{\mathrm{pos}}) - sim(e_I, e_{\mathrm{neg}})$$

**安全性强度**：基于Stable Diffusion内置安全检查器的嵌入，计算与不安全概念嵌入的相似度减去阈值t=0.19后取负。
$$x_I^{Safety} = -(sim(e_I, e_s) - t)$$

**排名归一化**：将所有原始值通过其在n个样本中的平均排名映射到[0,1]。
$$x_i^{\mathrm{norm}} = \frac{\mathrm{rank}(x_i) - 0.5}{n} \in [0, 1]$$

### 5.2 值编码器

值编码器首先通过正弦位置编码将归一化标量值映射为初始嵌入，再经过一个两层MLP（含SiLU激活函数）处理，最后复制扩展为固定长度的词元序列（默认32个词元），并添加可学习的位置编码。该序列与文本嵌入沿序列维度拼接，形成联合表示注入扩散模型。

### 5.3 训练目标

值编码器通过标准的扩散噪声预测损失进行训练，保持基础扩散模型冻结：
$$\mathcal{L}(\theta) = \mathbb{E}_{z_t, \varepsilon, c, t} \left[ \|\varepsilon - \hat{\varepsilon}_\theta(z_t, c, v, t)\|_2^2 \right]$$

## 实验与分析

### 6.1 主要定量结果

**控制精度（AvgDiff ↓）**：AttriCtrl 在亮度、细节、真实感三个属性上的平均AvgDiff为0.175，显著低于所有基线方法（最佳基线AID-in为0.262）。具体而言，亮度0.141、细节0.191、真实感0.192（Table 1）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_oyDe8cNXt6_AttriCtrl_A_G/figures/004_Table_1.jpg]]
*Table 1: Left: We measure control accuracy using the average absolute difference (AvgDiff ↓) between the target and result attribute intensity values. Right: User preference study. Participants were shown sequences of images with increasing attribute intensity from each method and asked to select the one demonstrating the most accurate, smooth, and high-quality progression (N=10 participants, 100 comparisons).*

**用户偏好研究**：在10位专家参与的100次比较中，AttriCtrl被选中的比例平均为84.2%，远超次优方法AID-in的7.2%（Table 1）。

**安全性控制**：在I2P数据集上，AttriCtrl的安全性移除率（RR）达到57.7%，优于ESD（53.9%）、SLD（32.6%）和NP（11.6%）（Figure 5）。

### 6.2 消融实验

**词元数量**：值编码器的词元数量从1增加到32时，控制精度持续提升；32词元达到最佳平衡，64词元时部分属性精度下降（Table 2）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_oyDe8cNXt6_AttriCtrl_A_G/figures/010_Table_2.jpg]]
*Table 2: Ablation on the number of tokens evaluated by AvgDiff ↓.*

**位置编码**：引入位置编码可进一步提升控制精度，在亮度、细节、真实感上AvgDiff分别从0.181、0.213、0.228降至0.141、0.191、0.192（Table 3）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_oyDe8cNXt6_AttriCtrl_A_G/figures/011_Table_3.jpg]]
*Table 3: Ablation on the use of positional encoding evaluated by AvgDiff ↓.*

**细节量化指标**：香农熵在人类专家评估中一致优于频域分析和局部对比度指标，被一致认为是最可靠的细节指示器（Figure 8）。

### 6.3 兼容性与泛化性

AttriCtrl 可与ControlNet、EliGen等主流控制框架无缝集成（Figure 7），并在不同扩散架构（SD v1.4, SDXL, SD v3.0）上均能实现有效的属性控制（Figure 13）。在COCO数据集上的评估表明，AttriCtrl 不会损害无关概念的生成质量（FID: 29.963, CLIP Score: 0.317）（Table 4）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_oyDe8cNXt6_AttriCtrl_A_G/figures/017_Table_4.jpg]]
*Table 4: Evaluation on unrelated concepts using FID ↓ and CLIP Score ↑.*

### 6.4 局限性

- 当提示词本身已包含属性相关修饰词（如“hyper-realistic hyperlapse lighting”）时，控制精度会下降，模型倾向于优先保证语义一致性。
- 安全性维度是相对于Stable Diffusion内置安全检查器的标准定义的，其有效性受限于该参考模型的覆盖范围和偏差。
- 实验基于FLUX模型（DiT架构），在U-Net架构上的适应性有待未来探索。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_oyDe8cNXt6_AttriCtrl_A_G/figures/002_Figure_2.jpg]]
*Figure 2: Examples of aesthetic attribute intensities in the training dataset. We show the raw values computed via quantitative metrics and the normalized values after value mapping, scaled to the [0, 1].*

## 方法谱系与知识库定位

AttriCtrl 属于扩散模型条件控制领域的方法，其核心思想——将归一化标量值通过值编码器映射为可学习的词元序列——建立了一种通用且强大的细粒度条件控制范式。与现有方法相比：

- **与基于文本指令的方法（Kontext）**：AttriCtrl 通过显式数值编码避免了自然语言对数值的不敏感性。
- **与基于嵌入加权的方法（W-Emb）**：AttriCtrl 的值编码器学习连续的控制轨迹，而非简单的线性加权。
- **与基于注意力插值的方法（AID-in/out）**：AttriCtrl 提供显式的数值指导，避免了插值过程中的伪影。
- **与概念擦除方法（ESD, SLD, NP）**：AttriCtrl 的安全性控制是可调节的连续强度，而非二值化的概念移除。

该框架为扩散模型的美学属性控制提供了一种可解释、可组合且与现有框架兼容的解决方案，为未来探索更复杂概念（如创意构图、情感基调）的量化与控制奠定了基础。

## 原文 PDF

![[paperPDFs/ICLR_2026/AttriCtrl_A_Generalizable_Framework_for_Controlling_Semantic_Attribute_Intensity_in_Diffusion_Models.pdf]]
