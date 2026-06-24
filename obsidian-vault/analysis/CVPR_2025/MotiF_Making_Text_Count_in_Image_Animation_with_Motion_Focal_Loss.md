---
title: "MotiF: Making Text Count in Image Animation with Motion Focal Loss"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MotiF_Making_Text_Count_in_Image_Animation_with_Motion_Focal_Loss.pdf
aliases:
- MMFL
- MotiF
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "利用光流生成运动热力图，对扩散损失进行重新加权，显式地增强模型对高运动区域的关注，从而削弱静态区域的支配地位。"
primary_logic: "运动焦点损失（MotiF）与现有的输入信号增强方法正交：它不是向模型提供额外的运动先验作为输入，而是修改训练目标本身，通过运动热力图加权让模型专注于运动区域，从而在推理时无需任何额外输入，即可显著提高文本对齐和运动生成质量。"
claims:
- "MotiF使用光流生成运动热力图并根据运动强度对损失进行加权。"
- "在TI2V-Bench人类评估中，MotiF相较于九个开源模型的平均偏好率达到72%。"
- "消融实验表明，运动焦点损失显著提升了文本对齐和物体运动，TI2V Score为63.1 vs 36.9。"
- "仅使用图像潜变量拼接（x-cat）作为图像条件，优于使用交叉注意力或两者结合。"
---

# MotiF: Making Text Count in Image Animation with Motion Focal Loss

> [!tip] 核心洞察
> 运动焦点损失（MotiF）与现有的输入信号增强方法正交：它不是向模型提供额外的运动先验作为输入，而是修改训练目标本身，通过运动热力图加权让模型专注于运动区域，从而在推理时无需任何额外输入，即可显著提高文本对齐和运动生成质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MotiF：用运动焦点损失让文本在图像动画中发挥作用 |
| 英文题名 | MotiF: Making Text Count in Image Animation with Motion Focal Loss |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2412.16153); [Project](https://wang-sj16.github.io/motif/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotiF (Motion Focal Loss) |
| Dataset | TI2V-Bench (human eval), TI2V-Bench (human eval, 仅与无运动焦点损失的基线比较), Animate Bench (自动指标) |

> [!tip] 效果简介
> - TI2V-Bench (human eval) 上，平均偏好率（MotiF vs 基线） 为 72%，对比 28% (平均)，变化 +44%。
> - TI2V-Bench (human eval, 仅与无运动焦点损失的基线比较) 上，TI2V Score 为 63.1，对比 36.9，变化 +26.2。
> - Animate Bench (自动指标) 上，Image Alignment / Text Alignment 为 92.68 / 67.73，对比 DynamiCrafter 92.82 / 58.55, Cinemo 92.11 / 72.10，变化 可比。

## 概述

文本驱动的图像到视频生成（TI2V）的核心瓶颈在于：标准扩散模型采用逐像素均等的 L2 损失进行训练，而自然视频中约 97% 的像素区域是静态的，仅有约 3% 的区域存在有意义的运动。这种严重的类别不平衡导致模型在训练时过度依赖条件图像来降低整体损失——这一现象被称为**条件图像泄漏**——从而难以真正关注文本所描述的运动，造成文本-运动对齐质量低下。

针对上述问题，本文提出 **MotiF（Motion Focal Loss，运动焦点损失）**，一种作用于训练目标层面的简单而有效的解决方案。其核心思想是：利用光流（RAFT）从训练视频中提取帧间运动强度，生成连续的运动热力图，并以此对扩散损失进行逐像素重加权，迫使模型将学习重点集中在高运动区域。与以往向模型注入额外运动信号作为输入的方法不同，MotiF 修改的是训练目标本身，因此在推理阶段无需任何额外输入，且与现有输入增强技术正交互补。

主要结果如下：

- **人类偏好评估**：在自建的 TI2V-Bench 基准上，MotiF 与九个开源模型进行成对比较，取得了平均 **72%** 的偏好率，在文本对齐和物体运动维度上优势尤为显著。
- **消融验证**：相较于无运动焦点损失的基线，MotiF 将 TI2V Score 从 36.9 提升至 **63.1**（+26.2），证实了损失重加权策略的有效性。同时，连续光流热力图优于基于 SAM 的二元掩码热力图；图像条件采用纯潜变量拼接（x-cat）优于交叉注意力或双流注入。
- **自动指标**：在 Animate Bench 上，MotiF 取得了与 DynamiCrafter、Cinemo 等代表性方法可比或更优的文本对齐分数（67.73 vs. 58.55 / 72.10），同时保持了良好的图像一致性。

MotiF 的局限在于：生成视频的运动自然度仍有提升空间；当文本要求在场景中引入新物体或仅针对多物体中的某一个时，运动生成的精确性和连贯性不足。此外，现有自动评估指标普遍偏重相机/背景运动，难以公正反映物体运动质量，评估体系本身仍需完善。

## 背景与动机

文本驱动的图像到视频生成（TI2V）任务要求模型根据一张静态图像和一段描述运动的文本提示，生成一段连贯的动态视频。该任务的核心挑战在于：模型必须同时保持对输入图像的高保真度，并严格遵循文本中指定的运动语义。然而，现有方法在这一平衡点上普遍表现不佳。

### 核心瓶颈：条件图像泄漏与运动区域忽视

标准TI2V训练流程采用L2扩散损失，该损失函数对视频中所有像素一视同仁。但现实视频中存在严重的运动分布不均衡——如Figure 1所示，一个典型视频中约97%的像素是静态的，仅有约3%的区域存在有意义的运动。这种极端的静态占比导致模型在优化L2损失时，倾向于过度依赖条件图像来重建静态背景，从而忽略文本指定的运动。这一现象被先前工作识别为**条件图像泄漏**（conditional image leakage）：模型学会了简单地复制输入图像，而非根据文本指令生成运动。

其因果链条可概括为：标准L2损失平等对待所有像素 → 静态区域在损失中占绝对主导 → 模型的最优策略是复制条件图像以最小化损失 → 文本运动信号被削弱 → 生成的视频缺乏文本指定的物体运动。

### 现有方法的局限：输入信号增强范式

为缓解上述问题，先前工作主要聚焦于**增强模型的输入信号**：通过额外提取运动分数、运动掩码、轨迹等运动先验，将其作为模型的显式输入，期望模型能隐式地利用这些信号来改善运动生成。例如，部分方法引入光流或运动向量作为条件通道，与图像和文本一起送入扩散模型。

这一范式存在两个固有局限：
1. **推理时依赖额外输入**：模型在推理阶段仍需提供运动先验信号，增加了系统的复杂性和应用门槛。
2. **间接引导**：运动先验作为输入信号，模型是否真正利用它、如何利用它，完全取决于模型自身的学习过程，缺乏直接的优化约束。

### MotiF的动机：从训练目标层面直接干预

MotiF提出了一个正交于输入信号增强的新方向：**修改训练目标本身**，而非增加输入信号。核心洞察在于：如果问题根源于L2损失对静态区域的偏向，那么解决方案应当是让损失函数显式地聚焦于运动区域。

具体而言，MotiF利用光流（optical flow）从训练视频中提取运动强度，生成运动热力图（motion heatmap），并将其作为逐像素权重乘到扩散损失上。这使得高运动区域的预测误差被放大，迫使模型在训练中将优化重心从静态背景转移到运动物体上。该方法在推理时**无需任何额外输入**，因为运动焦点信号仅作用于训练阶段，模型在推理时仍仅接收图像和文本，但已通过聚焦训练学会了更好地遵循文本运动指令。

### 与先前工作的关系

如Figure 2所示，MotiF与现有方法并非替代关系，而是互补关系。先前工作关注“给模型什么输入”，MotiF关注“让模型优化什么目标”。两者可以正交叠加：在采用增强运动输入的同时，也可以使用运动焦点损失来强化训练信号。这一设计哲学使MotiF成为一个轻量、即插即用的训练策略，可广泛应用于各类TI2V架构。

## 核心创新

MotiF 的核心创新在于**从训练目标层面解决文本驱动图像到视频（TI2V）生成中的运动生成难题**，而非像以往工作那样向模型提供额外的运动信号作为输入。这一设计选择使得 MotiF 与现有的输入信号增强方法正交且互补，在推理时无需任何额外输入。

### 关键瓶颈：条件图像泄漏与静态区域支配

在标准 TI2V 训练中，扩散模型使用均方误差（L2 损失）平等对待所有像素的预测误差。然而，视频中绝大多数像素（约 97%）是静态的，仅有约 3% 的区域存在有意义的运动（Figure 1a）。这导致模型在优化过程中过度依赖条件图像来降低整体损失——即**条件图像泄漏**（conditional image leakage）——从而难以专注于运动区域，无法忠实地遵循描述运动的文本提示。

### 因果操纵变量：运动焦点损失

MotiF 的核心操作是引入**运动焦点损失（Motion Focal Loss）**，对扩散损失进行运动感知的重新加权。具体而言：

1. **运动热力图生成**：使用 RAFT 光流计算视频帧间的运动强度，并通过类 Sigmoid 函数 $\sigma(x) = 1 / (1 + e^{100(0.05 - x)})$ 将强度图归一化至极化的连续热力图 $\mathbf{m}' \in [0,1]$，下采样至潜变量尺寸。
2. **损失加权**：将运动热力图作为逐像素权重乘到扩散预测的 L2 误差上：

$$\mathcal{L}_{\mathrm{motif}} = \mathbb{E}_{t, \mathbf{x} \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left\| \mathbf{m}' \cdot (\epsilon - \epsilon_{\theta}(\mathbf{z}_t, \mathbf{c}, t)) \right\|_2^2$$

3. **联合训练**：最终损失为扩散损失与运动焦点损失的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \lambda \mathcal{L}_{\mathrm{motif}}$$

这一设计显式地增强了模型对高运动区域的关注，削弱了静态区域的支配地位。损失分析（Figure 6）证实，MotiF 能有效降低高运动区域的相对损失，验证了运动焦点损失的预期效果。

### 与以往方法的根本区别

以往 TI2V 方法（如 **DynamiCrafter**、**Cinemo** 等）主要聚焦于从条件图像中推导额外的运动信号（运动分数、运动掩码等）作为模型的**输入**，让模型隐式地利用这些先验。MotiF 则将运动先验作用于**训练目标层面**——通过运动热力图加权损失来引导模型的学习重点，而非改变模型输入。这一区别使得 MotiF 在推理时无需任何额外输入，且与现有技术互补（Figure 2）。

### 图像条件注入的简化

作为辅助创新，MotiF 发现**仅使用图像潜变量与噪声视频潜变量在通道维拼接（x-cat）**作为图像条件注入方式，优于使用交叉注意力（cx-attn）或两者结合的双流注入。消融实验（Table 3）表明，单独使用交叉注意力会导致所有指标大幅下降（TI2V Score 从 92.2 降至 7.8），而同时使用 x-cat 和 cx-attn 也会损害文本对齐和物体运动。这一发现简化了图像条件的注入设计，使模型能更直接地利用条件图像的像素信息。

### 证据强度

- **运动焦点损失的有效性**：消融实验中，MotiF 相比无运动焦点损失的基线在 TI2V Score 上从 36.9 提升至 63.1（Table 2），文本对齐和物体运动维度提升尤为显著。
- **与输入增强方法的正交性**：MotiF 的训练目标修改与现有输入增强技术不冲突，可叠加使用（论文明确声明互补性）。
- **连续热力图的优势**：使用光流生成的连续热力图在文本对齐和物体运动上优于基于 SAM 的二元掩码热力图（Table A1），表明细粒度的运动强度信息对训练目标加权至关重要。
- **λ 的鲁棒性**：运动焦点损失权重 λ=1 时综合性能最优，但降低 λ 可改善视觉质量（Table A2），提供了实际应用中的调节灵活性。

## 整体框架

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/002_Figure_1.jpg]]
*Figure 1: Motivation and results of MotiF. (a) Example video frames and the corresponding motion heatmaps calculated from optical flow. In this example, 97% of the pixels are static while only 3% has meaningful motion. (b) In standard TI2V training pipeline, the model may learn to over-rely on the conditional image to optimize the L2 loss. This issue has been identified in [53] and termed as conditional image leakage. We propose MotiF to guide the model’s learning to focus on regions with more motion via motion heatmap re-weighting. (c) Qualitative results comparing MotiF to the baseline on examples from our proposed TI2V-Bench evaluation set*

MotiF 的整体框架围绕一个核心洞察构建：**标准扩散损失对所有像素一视同仁，而视频中约 97% 的区域是静态的**，导致模型在训练中过度依赖条件图像（即“条件图像泄漏”），难以专注于真正需要生成运动的区域并遵循文本提示。MotiF 的解决方案不是向模型注入额外的运动信号作为输入，而是**修改训练目标本身**——通过运动热力图对扩散损失进行重加权，迫使模型将学习重心放在高运动区域。这一设计与现有输入增强方法正交，推理时无需任何额外输入。

### 管道模块与数据流

MotiF 基于预训练的文本到视频扩散模型 **VideoCrafter2** 构建，在潜空间中进行扩散与去噪。整体管道包含以下关键模块，数据流从输入到输出依次为：

1. **图像条件注入（x-cat）**：将第一帧图像的潜变量与带噪声的视频潜变量沿通道维直接拼接，作为去噪 U-Net 的输入。消融实验表明，仅使用这种拼接方式（x-cat）优于使用交叉注意力（cx-attn）或两者组合的方案——后者会显著损害文本对齐和物体运动质量。

2. **文本条件注入**：使用 CLIP 文本编码器提取文本嵌入，通过 U-Net 中的交叉注意力层注入，为模型提供运动描述的语义引导。

3. **FPS 嵌入**：将帧率信号嵌入为类似时间步嵌入的表示，为模型提供时间动态的先验信息。

4. **运动热力图生成**：在训练阶段，使用 RAFT 光流模型计算视频帧间的运动强度，经 sigmoid-like 函数 $ \sigma(x) = 1 / (1 + e^{100(0.05 - x)}) $ 归一化至极化范围 $[0, 1]$，再下采样至潜变量尺寸，得到逐像素的运动权重图 $\mathbf{m}'$。

5. **运动焦点损失（MotiF Loss）**：将下采样后的运动热力图 $\mathbf{m}'$ 作为逐像素权重，乘到扩散模型预测噪声的 L2 误差上：

   $$ \mathcal{L}_{\mathrm{motif}} = \mathbb{E}_{t, \mathbf{x} \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left\| \mathbf{m}' \cdot (\epsilon - \epsilon_{\theta}(\mathbf{z}_t, \mathbf{c}, t)) \right\|_2^2 $$

   该损失与标准扩散损失联合训练：

   $$ \mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \lambda \mathcal{L}_{\mathrm{motif}} $$

   其中 $\lambda=1$ 时综合性能最优。降低 $\lambda$ 会改善视觉质量，但会损害文本对齐和物体运动。

训练配置为 8 张 A100-80G GPU、batch size 64，共训练 32K 步。推理时使用 DDIM 采样器，50 步，引导尺度 7.5，**无需任何额外的运动信号输入**。

### 与先前工作的关键差异

先前方法（如 DynamiCrafter、Cinemo 等）主要致力于从输入图像中提取额外的运动先验（运动分数、运动掩码等）作为模型的附加输入信号，让模型隐式地学习利用这些信息。MotiF 则从**学习目标层面**利用运动先验——运动热力图仅用于训练阶段的损失加权，推理时完全不需要。这一设计使得 MotiF 与现有技术互补：理论上可以将运动焦点损失应用于任何 TI2V 模型的训练中，而无需改变其推理管道。

## 核心模块与公式推导

MotiF 的核心设计思路是：**不修改模型架构或增加推理时的额外输入，而是改造训练目标本身**。其方法由三个关键模块构成：运动热力图生成、运动焦点损失计算，以及图像条件注入方式的选择。

### 3.1 运动热力图生成

给定一段训练视频，首先使用 **RAFT** 光流估计器计算相邻帧之间的光流强度。对于第 $l$ 帧 $x_l$ 与其后续帧 $x_{l+1}$，得到逐像素的运动强度图 $f_l$。随后，通过一个类 sigmoid 函数将强度图归一化并极化为 $[0, 1]$ 范围内的连续热力图：

$$\sigma(x) = 1 / (1 + e^{100(0.05 - x)})$$

该函数的设计意图是增强对比度：将大部分低运动区域推向接近 0，高运动区域推向接近 1，从而形成清晰的运动焦点图。最后，将热力图下采样至扩散模型潜空间的尺寸，得到用于损失加权的 $\mathbf{m}'$。

### 3.2 运动焦点损失

标准的扩散模型训练目标是最小化预测噪声与真实噪声之间的均方误差：

$$\mathcal{L}_{\mathrm{diffusion}} = \mathbb{E}_{t, \mathbf{x} \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \| \epsilon - \epsilon_{\theta}(\mathbf{z}_t, \mathbf{c}, t) \|_2^2$$

其中 $\mathbf{z}_t$ 为加噪后的潜变量，$\mathbf{c}$ 为条件信号（文本嵌入与图像条件），$\epsilon_{\theta}$ 为去噪网络。

MotiF 在此基础上引入**运动焦点损失**，将下采样后的运动热力图 $\mathbf{m}'$ 作为逐像素权重，乘到扩散预测的 L2 误差上：

$$\mathcal{L}_{\mathrm{motif}} = \mathbb{E}_{t, \mathbf{x} \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left\| \mathbf{m}' \cdot (\epsilon - \epsilon_{\theta}(\mathbf{z}_t, \mathbf{c}, t)) \right\|_2^2$$

其因果机制是：热力图在高运动区域取值接近 1，在静态区域接近 0，因此模型在高运动区域的预测误差会被放大，迫使优化过程将更多容量分配给运动区域的建模，从而削弱静态区域对损失的支配地位。

最终训练损失为两者的加权组合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \lambda \mathcal{L}_{\mathrm{motif}}$$

其中 $\lambda$ 控制运动焦点损失的相对强度。消融实验表明，简单地设置 $\lambda = 1$ 即可取得最佳综合性能（Table A2）。

### 3.3 图像条件注入方式

与许多先前工作采用双流注入（通道拼接 + 交叉注意力）不同，MotiF **仅使用通道维拼接**将条件图像注入去噪模型。具体而言，将第一帧图像的潜变量与带噪声的视频潜变量沿通道维拼接（记为 x-cat），作为 U-Net 的输入。文本条件则通过 CLIP 文本编码器提取嵌入，经交叉注意力层注入。

消融实验（Table 3）提供了该设计选择的证据：
- 仅使用交叉注意力（cx-attn）会导致所有指标大幅下降（TI2V Score 从 92.2 降至 7.8）；
- 同时使用 x-cat 和 cx-attn 也会在文本对齐和物体运动上造成明显退化。

这表明，在 TI2V 任务中，简洁的通道拼接方式比引入额外的交叉注意力路径更能保持图像-文本-运动三者之间的平衡。

### 3.4 与先前工作的本质区别

此前的 TI2V 方法主要聚焦于**输入信号增强**——从条件图像中提取额外的运动分数或运动掩码，作为模型的附加输入信号。MotiF 则选择了一条正交路径：**在训练目标层面利用运动先验**。运动热力图仅用于训练阶段的损失加权，推理时无需任何额外输入，因此与现有的输入增强技术天然互补。

## 实验与分析

### 核心实验设置

MotiF 基于预训练的 T2V 扩散模型 **VideoCrafter2** 构建，在 512×512 分辨率下训练。训练使用 8 块 A100-80G GPU，总 batch size 为 64，训练 32K 步。联合训练损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \lambda \mathcal{L}_{\mathrm{motif}}$，其中运动焦点损失权重 $\lambda$ 默认设为 1。推理时采用 DDIM 采样器，50 步去噪，引导尺度为 7.5。

人类评估通过 Amazon Mechanical Turk 进行，每个比较对由 5 名标注者独立评判，最终采用多数投票制。评估维度包括整体偏好、文本对齐、图像对齐、物体运动和整体质量五个方面。

### 主实验结果

#### 人类评估：TI2V-Bench

在自建的 TI2V-Bench 基准上（覆盖 22 个场景、88 张独特图像、133 条不同提示），MotiF 与九个开源模型进行了全面的人类评估比较，包括 **DynamiCrafter**、**Cinemo** 等代表性方法。结果如图 4 所示，MotiF 在所有五个评估维度上均取得显著优势，平均偏好率达到 **72%**。特别值得注意的是，在“文本对齐”和“物体运动”这两个直接反映运动生成质量的关键维度上，MotiF 的优势尤为突出——这正是运动焦点损失设计目标的直接体现。

#### 自动指标：Animate Bench

在 Animate Bench 上的自动指标评估中（表 4），MotiF 取得了与已有方法可比的结果：图像对齐 92.68，文本对齐 67.73。对比来看，DynamiCrafter 为 92.82/58.55，Cinemo 为 92.11/72.10。一个值得关注的发现是，简单的“静态视频基线”（仅重复第一帧）就能获得最高的图像对齐分数和合理的文本对齐分数，这进一步揭示了现有自动指标在评估 TI2V 生成质量时的局限性——它们往往无法有效区分真实的物体运动与静态场景或相机运动，这也是 MotiF 主要依赖人类评估而非自动指标的原因。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/011_Table_4.jpg]]
*Table 4: Automatic metrics on Animate Bench [51]. A simple static video baseline (repeating the first frame) can generate the best image alignment score and reasonable text alignment score (first row). MotiF achieved comparable results to prior works*

### 消融实验

#### 运动焦点损失的有效性

表 2 的核心消融直接对比了有无运动焦点损失的模型表现。结果显示，引入运动焦点损失后，TI2V Score 从基线的 36.9 跃升至 **63.1**（+26.2），文本对齐和物体运动维度改善最为显著。这验证了核心假设：标准的 L2 扩散损失平等对待所有像素，导致模型被约 97% 的静态区域主导，而运动焦点损失通过运动热力图加权，迫使模型将学习重心转移到真正有意义的运动区域。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/009_Table_2.jpg]]
*Table 2: Ablation studies on different design choices. The numbers on the left is for MotiF and the right is for the baseline. Similarly to the comparisons to prior works, MotiF mostly excel in improving the text alignment and object motion. Table 3. Ablation study on the image conditioning methods. Compared to our choice (x-cat), cx-attn alone leads to much worse results and using both is also sub-optimal. Here we train the models without motion focal loss to simplify the setting*

作为对照，论文还实验了“反向运动损失”（对低运动区域加权），结果如预期般损害了运动生成质量，进一步从反面印证了运动感知加权机制的必要性。

#### 运动热力图类型的影响

附录表 A1 比较了两种热力图生成方式：基于光流的连续热力图（MotiF 默认方案）与基于 SAM 的二元分割掩码。结果表明，光流生成的连续热力图在文本对齐和物体运动上均优于二元掩码方案。连续热力图能更精细地刻画运动强度的空间分布，而二元掩码丢失了运动幅度的梯度信息，导致模型无法区分剧烈运动与微弱运动。

#### 运动焦点损失权重 λ 的选择

附录表 A2 探索了 λ 的不同取值。λ=1 时综合性能最优。降低 λ 会改善视觉质量，但代价是文本对齐和物体运动指标的下降。这揭示了一个固有的权衡：更强的运动焦点损失迫使模型更激进地生成运动，但可能引入不自然的运动伪影；而较弱的权重则趋向于保守的静态生成。

#### 图像条件注入方式的消融

表 3 系统比较了三种图像条件注入策略：
- **仅拼接（x-cat）**：MotiF 的默认方案，将图像潜变量与噪声视频潜变量沿通道维拼接。
- **仅交叉注意力（cx-attn）**：通过交叉注意力层注入图像特征。
- **双流（x-cat + cx-attn）**：同时使用两种注入方式，类似于 DynamiCrafter 的设计。

结果清晰表明，仅使用交叉注意力会导致所有指标的严重退化（TI2V Score 从 92.2 骤降至 7.8）。同时使用两种方式（双流）也会在文本对齐和物体运动上出现明显下降。这一发现具有重要的工程指导意义：在 TI2V 任务中，简单直接的潜变量拼接比复杂的交叉注意力机制更有效，可能因为拼接保留了更完整的空间对应关系，而交叉注意力引入了额外的信息瓶颈。

### 损失分析

图 6 的损失分析从另一个角度验证了运动焦点损失的机制：MotiF 相比基线模型，能够有效降低高运动区域的相对损失。这意味着运动焦点损失确实将模型的优化重心从静态区域转移到了运动区域，使模型在训练过程中“被迫”学习更准确的动作生成，而非简单地复制条件图像。

### 失败模式与局限性

尽管 MotiF 在整体上取得了显著提升，论文也坦诚指出了若干失败模式：
- 生成的视频有时会出现**不自然的运动**，这是运动焦点损失激进加权带来的副作用。
- 当文本提示要求**在场景中引入新物体**，或需要对**多个物体中的某一个**进行精确运动控制时，模型难以生成连贯且准确的运动。这反映了当前方法在细粒度空间-语义对齐上的根本性局限。
- 运动热力图的质量直接影响训练效果——光流在遮挡、大位移等场景下的估计误差会传播到损失加权中。
- 现有评估基准（如 VBench-I2V）往往偏向相机/背景运动而非物体运动，导致自动指标无法完全反映真实质量，这一点在表 4 的静态基线实验中得到了充分暴露。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Figure 4 | MotiF 在人类评估中以 72% 平均偏好率显著优于九个基线模型 |
| Table 2 | 运动焦点损失使 TI2V Score 从 36.9 提升至 63.1，文本对齐和物体运动改善最大 |
| Table 3 | 仅使用潜变量拼接（x-cat）作为图像条件最优；交叉注意力单独或双流使用均会损害性能 |
| Figure 6 | MotiF 有效降低了高运动区域的相对损失，验证了损失重加权的机制 |
| Table A1 | 光流连续热力图优于 SAM 二元掩码，尤其在文本对齐和物体运动维度 |
| Table A2 | λ=1 综合最优；降低 λ 改善视觉质量但损害运动生成 |

### 补充图表

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/001_Figure.jpg]]
*Figure: (a) A bear jumping high on a meadow. A bear running to the left on a meadow*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/004_Figure.jpg]]

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/016_Figure.jpg]]
*Figure: The bear peeks out from behind the tree*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/017_Figure.jpg]]
*Figure: A2. Results on complex scenarios. MotiF generates faithful videos for (1) object occlusion and (b) multiple object interaction*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/018_Figure.jpg]]
*Figure: A3. Typical failure and challenging cases of MotiF on TI2V-Bench. We observe two typical cases that the model fail: 1) the generated videos may have unnatural motion ((a)); 2) the generated videos do not align well with the prompts ((b), (c), (d)). For 2), there are two specific scenarios when following the text is challenging including novel object ((c)) or multiple objects ((d)). We also include more video samples in the project website*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/019_Figure.jpg]]
*Figure: Starting Image: Video 1*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/005_Figure_3.jpg]]
*Figure 3: Example image-text pairs in TI2V-Bench. For each scenario (column), we first think of a scene that could be potentially animated to generate different types of motion. We include challenging scenarios when there are multiple objects (yellow/blue/red balloon) in the initial image for fine-grained control or the text prompt describes a new object (frisbee, bubbles) to enter the scene. Then we come up with different prompts and use the publicly available meta.ai tool to generate diverse sets of images. Images of low quality or those not in the appropriate initial state are removed. Table 1. Recent TI2V evaluation benchmarks. We believe the key for TI2V generation is that the text should descri...*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/008_Table.jpg]]

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2412_16153/figures/012_Table.jpg]]
*Table: A2. Ablation studies on the motion focal loss weight λ. The numbers on the left is for MotiF and the right is for the comparing setting*

## 方法谱系与知识库定位

MotiF 的核心贡献在于将运动先验从**输入信号增强**转移到**训练目标重加权**，这一思路与现有 TI2V 方法构成正交关系。理解这一谱系定位，需要先厘清当前 TI2V 研究的两条主要技术路线。

### 输入增强路线：向模型“告诉”运动信息

此前绝大多数 TI2V 方法聚焦于从条件图像或文本中**提取额外的运动信号，作为模型的显式输入**。典型做法包括：

- **运动分数/运动掩码注入**：从文本或图像中推导运动强度或运动区域，以额外条件的形式送入扩散模型。这些方法试图让模型在推理时“看到”运动提示，从而生成更符合文本描述的动态视频。
- **双流图像注入**：如 **DynamiCrafter** 等模型采用图像潜变量拼接（x-cat）与交叉注意力（cx-attn）相结合的方式注入条件图像，试图同时保留空间细节和语义对齐。

这类方法的共同假设是：**模型需要额外的运动信号作为输入，才能生成符合文本的运动**。其瓶颈在于，推理时依赖的额外输入（如运动掩码）本身可能不准确，且增加了推理复杂度和对外部模块的依赖。

### MotiF 的正交定位：修改训练目标本身

MotiF 选择了截然不同的切入点：**不改变模型输入，而是改变模型“学什么”**。其核心洞察是：标准 L2 扩散损失平等对待所有像素，而视频中约 97% 的区域是静态的（见 Figure 1），这导致模型过度依赖条件图像来最小化损失——即“条件图像泄漏”问题。模型学会了复制背景，却忽略了文本指定的运动。

运动焦点损失（Motion Focal Loss）通过以下机制解决这一问题：

1. **运动热力图生成**：使用 RAFT 光流计算帧间运动强度，经 sigmoid-like 函数 $ \sigma(x) = 1 / (1 + e^{100(0.05 - x)}) $ 极化为接近 0 或 1 的连续热力图，下采样至潜变量尺寸。
2. **损失重加权**：将热力图作为逐像素权重乘到扩散预测的 L2 误差上，使高运动区域的损失贡献被放大，静态区域的贡献被压制。联合训练损失为 $ \mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \lambda \mathcal{L}_{\mathrm{motif}} $，其中 $ \lambda=1 $ 时综合性能最优。

关键优势在于：**运动热力图仅在训练时使用，推理时无需任何额外输入**。这与输入增强路线形成根本性差异——MotiF 是“训练时聚焦运动”，而非“推理时注入运动”。

### 与具体基线的关系

在人类评估中，MotiF 与九个开源模型进行了对比，包括 **DynamiCrafter**（双流图像注入）、**Cinemo**（运动残差学习）等。MotiF 取得了平均 72% 的偏好率（Figure 4），且在文本对齐和物体运动维度上优势尤为显著。

消融实验进一步揭示了 MotiF 与现有设计选择的关系：

- **图像条件注入方式**：实验表明，仅使用 x-cat（图像潜变量拼接）优于双流注入（x-cat + cx-attn）或纯交叉注意力。使用 cx-attn 单独作为图像条件时，所有指标大幅下降（TI2V Score 从 92.2 降至 7.8，Table 3）；同时使用两者也会损害文本对齐和物体运动。这说明**过于复杂的图像注入机制可能引入额外的条件泄漏**，与运动焦点损失的目标相悖。
- **运动热力图类型**：基于光流的连续热力图在文本对齐和物体运动上优于基于 SAM 的二元掩码（Table A1），表明**连续的运动强度信息比硬性分割更有利于模型学习**。
- **损失权重**：$ \lambda=1 $ 时综合性能最优；降低 $ \lambda $ 会改善视觉质量但损害文本对齐和物体运动（Table A2），揭示了**运动聚焦与视觉质量之间的权衡**。

### 适用边界与局限

MotiF 的有效性建立在以下前提之上：

- **训练数据需包含足够的运动多样性**：运动焦点损失依赖光流生成的热力图质量，若训练数据中运动模式单一或光流估计不准确，重加权可能引入偏差。
- **文本提示需明确描述运动**：MotiF 的设计目标是让模型更好地遵循文本中的运动描述；若提示本身不包含运动信息（如仅描述静态场景），运动焦点损失的优势无法体现。

论文明确指出的局限包括：

- 生成的视频有时会出现**不自然的运动**，说明仅靠损失重加权还不足以完全解决运动质量的问题。
- 当文本提示要求在场景中**引入新物体**，或**只针对多个物体中的一个**指定运动时，模型难以生成精确且连贯的运动。这表明运动焦点损失在细粒度物体级别的运动控制上仍有不足。
- 当前评估基准（如 VBench-I2V）往往**偏重相机/背景运动而非物体运动**，自动指标不能完全反映 MotiF 的真实优势（Table A3）。

### 开放问题

从 MotiF 的定位和局限出发，以下问题值得进一步探索：

1. **运动自然度的进一步提升**：损失重加权解决了“是否运动”的问题，但“运动是否自然”可能需要更精细的运动先验或对抗训练策略。
2. **多物体场景的精细控制**：当前运动热力图是帧级别的全局权重，缺乏物体级别的区分能力。结合实例分割或开放词汇检测生成物体级运动热力图，可能是直接扩展方向。
3. **运动热力图质量的提升**：光流在遮挡、大位移等场景下存在误差，更鲁棒的运动估计方法（如基于深度学习的运动分割）可能进一步提升性能。
4. **向纯文本到视频生成（T2V）的迁移**：MotiF 当前在 TI2V 场景下验证，其核心思想——用运动热力图重加权扩散损失——理论上同样适用于 T2V，但需要解决无条件图像时运动热力图的来源问题。
5. **更全面的自动评价指标**：现有指标难以区分物体运动与相机运动，设计能解耦这两类运动的自动指标，对推动 TI2V 研究至关重要。

### 知识库定位总结

MotiF 在 TI2V 方法谱系中占据**训练目标优化**这一独特节点。它与输入增强方法（运动信号注入、双流图像条件）正交且互补——理论上可以将运动焦点损失应用于任何现有的 TI2V 架构。其方法论简洁性（仅修改损失函数，无需额外推理输入）使其具有较强的可迁移性，但当前在运动自然度和细粒度控制上的局限也指明了后续工作的方向。

## 原文 PDF

![[paperPDFs/CVPR_2025/MotiF_Making_Text_Count_in_Image_Animation_with_Motion_Focal_Loss.pdf]]
