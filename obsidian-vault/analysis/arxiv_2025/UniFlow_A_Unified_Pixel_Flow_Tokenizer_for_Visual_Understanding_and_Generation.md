---
title: "UniFlow: A Unified Pixel Flow Tokenizer for Visual Understanding and Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/UniFlow_A_Unified_Pixel_Flow_Tokenizer_for_Visual_Understanding_and_Generation.pdf
aliases:
- UniFlow
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 层级自适应自蒸馏保留预训练编码器的分层语义知识并允许浅层补充细节；轻量级 patch-wise 像素流解码器直接在像素空间建模条件流，将理解与生成解耦。
primary_logic: 通过动态调整蒸馏强度，深层侧重语义稳定、浅层灵活适配重建；流匹配解码器以一步采样实现高保真重建，避免预训练 VAE 的瓶颈，从而在单一 tokenizer 中达成理解与生成的双赢。
claims:
- UniFlow-XL 7B surpasses TokenFlow-XL 14B by 6.05% on average understanding benchmarks.
- UniFlow(InternViT) achieves state-of-the-art reconstruction rFID of 0.26 on ImageNet-1K, outperforming UniTok (0.41).
- UniFlow-LV achieves SOTA multimodal understanding average of 67.87, surpassing TokenFlow-L (62.40).
- UniFlow achieves best rFID (0.28) with significantly less training data and steps compared to TokenFlow, BLIP3-o, and UniTok.
---

# UniFlow: A Unified Pixel Flow Tokenizer for Visual Understanding and Generation

> [!tip] 核心洞察
> 通过动态调整蒸馏强度，深层侧重语义稳定、浅层灵活适配重建；流匹配解码器以一步采样实现高保真重建，避免预训练 VAE 的瓶颈，从而在单一 tokenizer 中达成理解与生成的双赢。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniFlow：一种面向视觉理解与生成的统一像素流分词器 |
| 英文题名 | UniFlow: A Unified Pixel Flow Tokenizer for Visual Understanding and Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2510.10575) · [arXiv](https://arxiv.org/abs/2310) · [Code](https://github.com/black-forest-labs/flux) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | UniFlow |
| Dataset | ImageNet-1K 256×256 Reconstruction, Multimodal Understanding Average, Text-to-Image Generation, Training Efficiency |

> [!tip] 效果简介
> - ImageNet-1K 256×256 Reconstruction 上，rFID 0.26 (UniFlow(InternViT)) vs 0.41 (UniTok) (-0.15)。
> - Multimodal Understanding Average 上，Avg. score over POPE, GQA, TextVQA, MMVet, MMB, MME-P 67.87 (UniFlow-LV, SigLIP2-SO400M) vs 62.40 (TokenFlow-L) (+5.47)。
> - Text-to-Image Generation (GenEval) 上，Overall score 0.65 (UniFlow 0.6B diffusion) vs 0.57 (SDXL inference from Table 3) (+0.08)。

## 概述

视觉理解与生成任务的统一分词器面临一个根本性瓶颈：高层语义理解所需的抽象特征与低层像素生成所需的细粒度细节之间存在目标冲突，导致优化方向互斥。现有方案或冻结预训练编码器以保留语义但牺牲重建质量，或端到端微调以提升重建却损害语义表征，难以在单一分词器中同时达成两者最优。

**UniFlow** 提出了一套解耦的统一分词框架，核心思路是通过**层级自适应自蒸馏**保留预训练视觉基础模型的层次化语义知识，同时允许浅层灵活补充细粒度细节；并采用**轻量级 patch-wise 像素流解码器**直接在像素空间建模条件流，以一步采样实现高保真重建，从而将理解与生成的能力解耦到编码器与解码器中。

关键实证结论如下：

- **重建质量**：UniFlow（InternViT 编码器）在 ImageNet-1K 256×256 重建上取得 rFID 0.26，显著优于统一分词器基线 UniTok（0.41），且逼近最优生成式分词器水平（Table 1）。
- **多模态理解**：UniFlow-LV 在 POPE、GQA、TextVQA 等 6 项基准上平均得分 67.87，超越 TokenFlow-L（62.40），在统一分词器中达到 SOTA（Table 2）。
- **效率优势**：UniFlow 仅使用 1.2M 训练数据、70k 步即达到 rFID 0.28，而 UniTok 需 1.28B 数据、80k 步才达到 0.38，数据效率提升显著（Table 14）。
- **生成能力**：在 GenEval 文本到图像生成基准上，UniFlow 0.6B 扩散模型取得 0.65 综合分，优于 SDXL 推理的 0.57（Table 3）。

在方法谱系上，UniFlow 区别于 **TokenFlow**（冻结编码器 + 预训练 VAE 解码器）和 **UniTok**（端到端微调 + 多损失像素解码器），通过自蒸馏保留语义、流匹配替代 GAN/L1/L2/LPIPS 等多损失组合，实现了训练目标与架构的双重简化。其定位介于“理解优先”的冻结编码器方案与“生成优先”的专用 VAE 分词器之间，为统一视觉表征提供了一条可扩展的新路径。

## 背景与动机

### 视觉分词器的统一困境

视觉分词器（visual tokenizer）是多模态大模型和视觉生成模型的核心组件，其任务是将图像映射为紧凑的潜在表示，供后续的语言模型或扩散模型使用。然而，当前的分词器设计面临一个根本性的困境：**理解任务**要求编码器提取高层语义抽象特征，而**生成任务**则要求保留低层像素级的细粒度细节。这两类目标在优化方向上存在互斥——强化语义抽象会牺牲空间细节，而保留细节则会稀释语义表征。

这一冲突在现有统一分词器的实践中表现得尤为突出。以 **TokenFlow** 为代表的方案通过冻结预训练编码器来保持语义能力，但受限于其依赖的预训练 VAE 解码器（如 SD-VAE）的瓶颈，重建质量难以突破。以 **UniTok** 为代表的方案则采用端到端训练像素解码器，虽提升了重建保真度，却不可避免地削弱了编码器的语义理解能力。**BLIP3-o** 和 **QLIP** 等方案同样未能从根本上调和这对矛盾，往往在理解与生成之间做出妥协，导致统一分词器在任一维度上都难以匹敌专用方案。

### 现有范式的结构性缺陷

从训练范式来看，现有统一分词器主要沿袭两条路径，但各有结构性缺陷：

1. **冻结编码器 + 预训练 VAE 解码器**（如 TokenFlow）：编码器的语义知识得以完整保留，但预训练 VAE 的解码能力构成硬瓶颈。VAE 通常在与编码器不同的数据分布和目标函数下训练，其潜在空间与编码器特征空间之间存在语义错位，导致重建质量受限于 VAE 的上限，且难以通过端到端优化来弥合。

2. **端到端训练编码器 + 像素解码器**（如 UniTok）：通过联合优化编码器和解码器，重建质量显著提升，但编码器在像素重建损失的驱动下会偏离其预训练的语义空间，导致理解能力退化。这种退化在深层特征中尤为严重，因为深层语义表征对像素级扰动高度敏感。

这两种范式的共同缺陷在于**将理解与生成的目标强耦合在同一优化回路中**，缺乏一个能够动态调节二者权重的机制。

### 本工作的核心动机

UniFlow 的提出正是为了解决上述困境。其核心动机可概括为三个层面：

- **目标解耦**：将语义理解和像素重建的任务分配给不同的模块和损失函数，使编码器专注于语义保持、解码器专注于高保真重建，从而避免优化目标的互斥。
- **知识继承**：设计一种层级自适应自蒸馏策略，使得统一编码器能够从预训练视觉基础模型（Vision Foundation Model, VFM）中继承分层语义知识，深层保持语义稳定，浅层灵活补充细节。
- **高效重建**：摒弃预训练 VAE 的瓶颈，采用基于流匹配（Flow Matching）的轻量级像素解码器，直接在像素空间建模条件流，以一步采样实现高保真重建，同时保持极低的计算开销。

通过上述设计，UniFlow 旨在在单一分词器中同时达成理解与生成的双赢，为统一视觉表示学习提供一条新的技术路径。

## 核心创新

UniFlow 的核心创新在于通过**层级自适应自蒸馏**与**轻量级 patch-wise 像素流解码器**的组合，系统性地解决了统一分词器中语义理解与像素生成之间的根本性冲突。与现有统一分词器（如 TokenFlow、UniTok）相比，UniFlow 在三个关键设计槽位上实现了范式转变。

### 1. 编码器训练策略：从冻结/端到端微调到层级自适应自蒸馏

现有统一分词器通常采用两种策略：TokenFlow 直接冻结预训练编码器以保持语义能力，但牺牲了重建所需的细粒度细节；UniTok 则对编码器进行端到端微调，虽提升了重建质量，却不可避免地破坏了预训练编码器中蕴含的层次化语义知识。

UniFlow 提出的**层级自适应自蒸馏**（Layer-wise Adaptive Self-Distillation）打破了这一僵局。其核心机制是动态调整各层的蒸馏强度：深层特征承载高层语义，需保持稳定；浅层特征则允许灵活适配以补充像素重建所需的细节信息。具体而言，每层的自适应权重由分层先验与对齐惩罚共同决定：

$$w_{l} = \frac{w_{l}^{\mathrm{base}} \cdot \exp(\beta \cdot \alpha_{l})}{\sum_{k=1}^{L} w_{k}^{\mathrm{base}} \cdot \exp(\beta \cdot \alpha_{k})}$$

其中 $w_{l}^{\mathrm{base}}$ 为分层基础权重（深层天然获得更高系数），$\alpha_{l}$ 衡量该层学生特征与冻结教师特征之间的对齐程度，$\beta$ 控制自适应强度。该权重作用于余弦距离损失：

$$\mathcal{L}_{\mathrm{dist}} = \sum_{l=1}^{L} w_{l} \cdot \left(1 - \frac{1}{S} \sum_{i,j} \frac{\langle \mathbf{H}_{\mathrm{U}}^{(l,i,j)}, \mathbf{H}_{\mathrm{T}}^{(l,i,j)} \rangle}{\|\mathbf{H}_{\mathrm{U}}^{(l,i,j)}\| \|\mathbf{H}_{\mathrm{T}}^{(l,i,j)}\|}\right)$$

这一设计的关键洞察在于：与其在全网范围内做语义保持与细节重建的全局折中，不如让不同层各司其职。消融实验证实，$\beta=2$ 时达到最优平衡点——MME-P 得分 1505.1，PSNR 33.23（Table 6a, Figure 5b），验证了自适应机制的因果有效性。

### 2. 解码器架构：从预训练 VAE/像素解码器到 patch-wise 流匹配解码器

传统统一分词器在重建端存在明显的架构瓶颈。TokenFlow 依赖预训练 SD-VAE 解码器，其潜在空间的压缩损失天然限制了重建保真度；UniTok 虽使用像素空间解码器，但需要组合 GAN、L1、L2、LPIPS 等多重损失函数来稳定训练，优化复杂且易产生伪影。

UniFlow 的**轻量级 patch-wise 像素流解码器**从根本上绕开了这些限制。它将图像划分为独立 patch，直接在像素空间建模从噪声到真实像素的直线流轨迹：

$$\mathbf{x}_{t}^{(i,j)} = (1 - t) \mathbf{x}^{(i,j)} + t \cdot \epsilon^{(i,j)}, \quad t \in [0,1]$$

解码器仅需预测速度场 $v_{\boldsymbol{\theta}}(\mathbf{x}_{t}^{(i,j)}, t, \mathbf{c}^{(i,j)})$，训练目标为单一的流匹配均方误差损失：

$$\mathcal{L}_{\mathrm{flow}} = \mathbb{E}_{\mathbf{x}^{(i,j)} \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}, t \sim p_{t}} \left\| v_{\boldsymbol{\theta}}(\mathbf{x}_{t}^{(i,j)}, t, \mathbf{c}^{(i,j)}) - (\epsilon^{(i,j)} - \mathbf{x}^{(i,j)}) \right\|_{2}^{2}$$

为消除 patch 独立解码可能引入的网格伪影，UniFlow 在潜在空间上投影后引入**全局 Transformer 块**（Global Transformer Blocks, GTB）进行跨 patch 上下文交换：

$$\mathbf{C} = \mathcal{GTB}(\mathcal{P}_{\mathrm{up}}(\mathbf{z}) + \mathbf{PE})$$

消融实验表明，6 层 GTB 即可消除网格伪影，PSNR 达 33.23、rFID 达 0.26；继续增加层数收益递减（Table 6c, Figure 5c）。更重要的是，得益于直线流轨迹的设计，**一步 Euler 推理即可达到最优重建质量**，无需多步迭代（Figure 21）。

### 3. 损失函数：从多重对抗/感知损失到单一流匹配损失

传统生成式分词器（如 SD-VAE）和统一分词器（如 UniTok）通常需要组合 GAN 损失、L1/L2 像素损失和 LPIPS 感知损失，各损失项之间的权重调谐繁琐且对超参数敏感。UniFlow 将重建问题转化为流匹配问题，仅需一个 MSE 损失即可驱动解码器学习像素空间的确定性映射。总训练目标为蒸馏损失与流损失的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{d} \mathcal{L}_{\mathrm{dist}} + \lambda_{f} \mathcal{L}_{\mathrm{flow}}$$

当 $\lambda_d = \lambda_f$ 时达到最优理解-重建平衡，相比纯蒸馏基线在 MME-P 上提升 35.1 分（Table 6b）。

### 创新点的协同效应

上述三个 changed slots 并非孤立改进，而是形成了因果闭环：层级自适应自蒸馏确保编码器同时保留语义知识与细节表征能力，为解码器提供高质量的条件信号；patch-wise 流匹配解码器则利用这一信号，以极简的损失函数和一步采样实现高保真重建。这种“编码器分层保真、解码器流式重建”的架构分工，使 UniFlow 在数据效率上展现出显著优势——仅使用 120 万张 ImageNet-1K 图像训练 70k 步，即达到 rFID 0.28，优于使用 12.8 亿张图像训练 80k 步的 UniTok（rFID 0.38）（Table 14）。

## 整体框架

UniFlow 的整体设计遵循“统一编码 + 轻量解码”的范式，旨在以单一分词器同时支撑高层语义理解与低层像素重建。如图 2 所示，系统由两条核心通路构成：

1. **统一编码器**（Unified Encoder）以预训练的视觉基础模型（VFM）为骨架，接收输入图像并提取多层特征。这些特征经过**层级自适应自蒸馏**（Layer-wise Adaptive Self-Distillation）与一个冻结的教师编码器对齐，从而在深层保留语义知识的同时，允许浅层灵活补充细粒度细节。编码器的最终输出经下采样投影为紧凑的潜变量 $\mathbf{z}$。

2. **轻量流匹配解码器**（Lightweight Flow-based Decoder）直接在像素空间工作，避免了对预训练 VAE 的依赖。潜变量 $\mathbf{z}$ 先经上采样投影，再通过一组**全局 Transformer 块**（Global Transformer Blocks, GTB）注入跨 patch 的全局上下文，生成条件潜码 $\mathbf{C}$。随后，一个轻量的 MLP 网络以逐 patch 方式预测速度场 $v_{\boldsymbol{\theta}}(\mathbf{x}_t, t, \mathbf{c})$，驱动从噪声到真实像素的直线流轨迹，最终仅需一步 Euler 采样即可完成高保真重建。

整个系统以端到端方式训练，总损失为自蒸馏损失与流匹配损失的加权和：

$$
\mathcal{L}_{\mathrm{total}} = \lambda_{d} \mathcal{L}_{\mathrm{dist}} + \lambda_{f} \mathcal{L}_{\mathrm{flow}}
$$

其中 $\mathcal{L}_{\mathrm{dist}}$ 通过层级自适应权重 $w_l$ 动态调节各层的蒸馏强度，深层侧重语义稳定、浅层灵活适配重建；$\mathcal{L}_{\mathrm{flow}}$ 则驱动解码器学习精确的像素级条件流。这种解耦设计使 UniFlow 在单一框架内实现了理解与生成的双赢。

### 补充图表

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/002_Figure_2.jpg]]
*Figure 2: The framework of UniFlow. Our UniFlow model is trained end-to-end to endow a powerful VFM with both semantic understanding capabilities and high-fidelity pixel reconstruction. ensures that deeper layers receive a higher coefficient, where L is the total number of layers. Second, we introduce an alignment penalty*

## 核心模块与公式推导

UniFlow 由统一编码器 $\mathcal{E}_{\mathrm{U}}$ 与轻量级流匹配解码器 $\mathcal{D}_{\mathtt{flow}}$ 构成（Fig. 2）。其核心矛盾在于：高层语义理解需要抽象特征，而低层像素生成需要细粒度细节，两者的优化目标天然互斥。UniFlow 通过两个关键设计解耦这一冲突——层级自适应自蒸馏保留语义知识，patch-wise 像素流解码器直接在像素空间建模条件流。

### 层级自适应自蒸馏

预训练视觉基础模型（VFM）作为冻结教师 $\mathcal{E}_{\mathrm{T}}$，学生编码器 $\mathcal{E}_{\mathrm{U}}$ 需在保留其分层语义的同时，允许浅层补充细节。为此，UniFlow 引入自适应层权重 $w_l$，动态调节每层的蒸馏强度：

$$w_{l} = \frac{w_{l}^{\mathrm{base}} \cdot \exp(\beta \cdot \alpha_{l})}{\sum_{k=1}^{L} w_{k}^{\mathrm{base}} \cdot \exp(\beta \cdot \alpha_{k})}$$

其中 $w_{l}^{\mathrm{base}}$ 为层级先验（深层天然获得更高基础权重），$\alpha_l$ 为对齐惩罚项——当某层学生-教师特征余弦相似度较低时，该层获得更大权重以加强对齐。$\beta$ 控制先验与惩罚的平衡强度（默认 $\beta=2$）。

基于此权重，自蒸馏损失定义为各层加权余弦距离之和：

$$\mathcal{L}_{\mathrm{dist}} = \sum_{l=1}^{L} w_{l} \cdot \left(1 - \frac{1}{S} \sum_{i,j} \frac{\langle \mathbf{H}_{\mathrm{U}}^{(l,i,j)}, \mathbf{H}_{\mathrm{T}}^{(l,i,j)} \rangle}{\|\mathbf{H}_{\mathrm{U}}^{(l,i,j)}\| \|\mathbf{H}_{\mathrm{T}}^{(l,i,j)}\|}\right)$$

其中 $\mathbf{H}_{\mathrm{U}}^{(l,i,j)}$ 与 $\mathbf{H}_{\mathrm{T}}^{(l,i,j)}$ 分别为学生和教师在第 $l$ 层空间位置 $(i,j)$ 的特征向量，$S$ 为空间位置总数。该设计使深层侧重语义稳定，浅层灵活适配重建，避免端到端微调对预训练知识的破坏。

### Patch-wise 像素流解码器

编码器输出的最终特征经下采样投影为紧凑潜码 $\mathbf{z}$（维度 $\hat{d}=64$），再通过上采样投影恢复空间维度，并与位置编码相加后送入全局 Transformer 块（GTB）以注入跨 patch 的全局上下文：

$$\mathbf{C} = \mathcal{GTB}(\mathcal{P}_{\mathrm{up}}(\mathbf{z}) + \mathbf{PE})$$

GTB 通过自注意力机制消除 patch 间的网格伪影，产生全局一致的潜码条件 $\mathbf{C}$，随后拆分为逐 patch 条件 $\mathbf{c}^{(i,j)}$。

流匹配解码器 $v_{\boldsymbol{\theta}}$ 是一个轻量级 MLP 网络，在像素空间学习连续速度场。对每个 patch，定义从真值 $\mathbf{x}^{(i,j)}$ 到高斯噪声 $\epsilon^{(i,j)}$ 的直线轨迹：

$$\mathbf{x}_{t}^{(i,j)} = (1 - t) \mathbf{x}^{(i,j)} + t \cdot \epsilon^{(i,j)}, \quad t \in [0,1]$$

训练目标为最小化预测速度与真值速度 $(\epsilon^{(i,j)} - \mathbf{x}^{(i,j)})$ 之间的均方误差：

$$\mathcal{L}_{\mathrm{flow}} = \mathbb{E}_{\mathbf{x}^{(i,j)} \sim p_{\mathrm{data}}, \epsilon \sim \mathcal{N}, t \sim p_{t}} \left\| v_{\boldsymbol{\theta}}(\mathbf{x}_{t}^{(i,j)}, t, \mathbf{c}^{(i,j)}) - (\epsilon^{(i,j)} - \mathbf{x}^{(i,j)}) \right\|_{2}^{2}$$

该设计的关键优势在于：解码器直接在像素空间建模，避免了预训练 VAE 潜空间的瓶颈；直线轨迹使推理时仅需一步 Euler 采样即可获得高保真重建（Fig. 21 验证额外步骤无质量增益）。

### 联合训练目标

最终训练损失为自蒸馏损失与流匹配损失的加权组合：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{d} \mathcal{L}_{\mathrm{dist}} + \lambda_{f} \mathcal{L}_{\mathrm{flow}}$$

消融实验（Table 6b）表明，平衡权重 $\lambda_d = \lambda_f$ 提供最优的语义保持与重建质量权衡，相比纯蒸馏基线在 MME-P 上提升 35.1 分。

### 补充图表

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/040_Figure_19.jpg]]
*Figure 19: Visualization of Global Transformer Block (GTB) Impact on Flow Loss and Reconstruction Quality. The figure shows flow loss curves (left) and corresponding reconstructed images (right) for models with 0, 3, and 6 GTB layers during training. As GTB layers increase, flow loss converges faster and to a lower value, with reconstructed images exhibiting reduced grid artifacts and higher visual fidelity*

## 实验与分析

### 核心瓶颈验证：理解与生成的优化冲突

UniFlow 的设计动机源于统一分词器中的一个根本性冲突：高层语义理解所需的抽象特征与低层像素生成所需的细粒度细节在优化目标上互斥。传统方法或冻结预训练编码器以保语义（如 TokenFlow），或端到端微调以追求重建质量（如 UniTok），难以兼得。UniFlow 通过**层级自适应自蒸馏**与**轻量级 patch-wise 像素流解码器**将两者解耦，在单一分词器中实现双赢。

Table 1 的主结果直接验证了这一主张。UniFlow(InternViT) 在 ImageNet-1K 256×256 重建上取得 rFID 0.26，显著优于统一分词器基线 UniTok（0.41）和 SD-VAE（0.67），且与纯生成式分词器（如 Cosmos-Tokenizer 的 0.20）差距极小。同时，UniFlow-LV（SigLIP2-SO400M）在 Table 2 的多模态理解基准上取得平均分 67.87，超过 TokenFlow-L（62.40）达 5.47 分。**以 7B 语言模型超越 14B 的 TokenFlow-XL 达 6.05%（Figure 1），证明语义保留策略的有效性。**

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of different training paradigms for unified tokenizers. All multimodal large language models are trained on LLaVA-v1.5 data with Vicuna-7B, except that TokenFlow uses Vicuna-13B. UniFlow simultaneously improves performance and training efficiency*

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/004_Table_1.jpg]]
*Table 1: Comparison of reconstruction quality on the 256 × 256 ImageNet-1K and MS-COCO 2017 validation sets. “Ratio” denotes downsampling ratio; “Type” indicates tokenizer traits (VQ usage and decoder type). UniFlow achieves state-of-the-art (SOTA) performance in unified tokenizers while also being competitive with the best generative tokenizers. See Appendix B.1 for data details*

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/005_Table_2.jpg]]
*Table 2: Evaluation on multimodal understanding benchmarks. UniFlow-LV indicates training in the LLaVA-v1.5 setting, as marked by †. Our UniFlow-LV achieves SOTA in unified tokenizers. MME is divided by 20 for the Avg*

### 主结果分析

**重建质量（Table 1）**：UniFlow 在四个编码器初始化（DFN-CLIP、SigLIP2、DINOv2、InternViT）下均取得统一分词器的 SOTA。InternViT 变体以 rFID 0.26 领先，DINOv2 变体以 PSNR 31.01 和 SSIM 0.87 在像素级指标上表现最佳。值得注意的是，UniFlow 的下采样比仅为 14×–28×，远低于 Cosmos-Tokenizer 的 64×，在压缩率与重建质量之间取得了更优的平衡。

**多模态理解（Table 2）**：UniFlow-LV 在 LLaVA-v1.5 训练范式下，以 SigLIP2-SO400M 编码器取得平均 67.87，涵盖 POPE、GQA、TextVQA、MMVet、MMB、MME-P 六项基准。相比同样使用统一分词器的 TokenFlow-L（62.40）和 QLIP（59.22），UniFlow 在所有子项上均有提升，尤其在需要细粒度视觉定位的 TextVQA（+3.1）和 MMVet（+4.8）上优势明显。

**文本到图像生成（Table 3）**：UniFlow 0.6B 扩散模型在 GenEval 上取得 0.65 的综合分，超过 SDXL 的 0.57，验证了 UniFlow tokenizer 在生成任务中的潜力。在 DPG-Bench 上，UniFlow 同样以 78.54 领先多个基线，表明流匹配解码器学到的像素空间表示对扩散生成是有效的条件信号。

**训练效率（Table 14）**：UniFlow 仅用 1.2M 数据、70k 步即达到 rFID 0.28，而 UniTok 需要 1.28B 数据、80k 步才达到 0.38。数据效率提升约三个数量级，归因于预训练编码器提供的强语义先验与流匹配损失的简洁性——无需 GAN、LPIPS 等复杂损失组合。

### 消融实验

消融实验围绕三个核心设计展开（Table 6，Figure 5）：

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/010_Table_6.jpg]]
*Table 6: Ablation studies of UniFlow training. We highlight the default setting. (a) Distillation strategy (b) Loss balance (c) Decoder design*

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/013_Figure_5.jpg]]
*Figure 5: Ablation studies on training comparison and hyperparameters*

**1. 层级自适应自蒸馏策略（Table 6a，Figure 5b）**

对比四种蒸馏策略：无蒸馏（仅重建损失）、均匀蒸馏、固定层级权重蒸馏、自适应蒸馏（β=2）。自适应蒸馏在 MME-P 上取得 1505.1，显著高于无蒸馏（1411.0）和均匀蒸馏（1470.0），同时 PSNR 保持在 33.23 的强水平。β 控制自适应强度：β=0 退化为固定权重，β 过大则过度惩罚未对齐层导致语义漂移。β=2 在语义保留与重建灵活性之间达到最优。

**2. 损失平衡（Table 6b）**

蒸馏损失与流匹配损失的权重比是关键。仅蒸馏（λ_d=1, λ_f=0）导致 MME-P 仅 1470.0，重建能力缺失；仅流匹配（λ_d=0, λ_f=1）使 MME-P 降至 1411.0，语义退化。等权重（λ_d=λ_f）在 MME-P 上获得 35.1 的提升，验证了两者协同的必要性。

**3. 解码器设计（Table 6c，Figure 5c）**

全局 Transformer 块（GTB）是消除网格伪影的关键。无 GTB 时，PSNR 仅 31.50，rFID 高达 0.42；加入 6 层 GTB 后，PSNR 提升至 33.23，rFID 降至 0.26。进一步增加层数收益递减（12 层 PSNR 33.25），表明 6 层已足够建模 patch 间全局上下文。

**4. 推理步数（Figure 21）**

流匹配解码器支持多步 Euler 采样，但一步推理即达到最优重建质量。增加步数不提升 rFID 或 PSNR，仅增加延迟。这与 rectified flow 的直线轨迹特性一致——模型已学会从噪声到像素的直线映射，无需迭代修正。

### 失败模式与局限性

**1. 商用模型视觉质量差距**：尽管 UniFlow 在学术基准上取得 SOTA，与基于大规模专有数据（如数亿图文对）训练的商用模型相比，在极端细节纹理和复杂场景下的视觉质量仍存在微小差距。这是数据规模限制的直接结果，而非方法缺陷。

**2. 固定分辨率依赖**：UniFlow 的分词器继承预训练编码器的固定输入分辨率（如 InternViT 的 448×448），缺乏对可变分辨率的原生支持。在多分辨率应用场景中，需要额外的插值或裁剪操作，可能引入信息损失。

**3. 编码器耦合性**：UniFlow 的性能与选定的视觉基础模型强相关。Table 1 显示不同编码器初始化导致 PSNR 在 28.56–31.01 间波动，rFID 在 0.26–0.42 间变化。更换编码器需重新训练整个分词器，缺乏即插即用的灵活性。

### 重要图表结论

- **Figure 1**：UniFlow 以更小的模型（7B vs 14B）和更少的训练数据，在理解与重建两个维度上同时超越 TokenFlow，验证了训练范式的根本性优势。
- **Table 1**：UniFlow 在统一分词器中首次将 rFID 降至 0.26，逼近纯生成式分词器水平，打破了“统一分词器必须牺牲重建质量”的固有认知。
- **Table 2**：UniFlow-LV 在六项多模态理解基准上全面超越 TokenFlow-L，尤其在需要细粒度视觉感知的任务上优势显著。
- **Figure 5 + Table 6**：自适应蒸馏、等权重损失平衡、6 层 GTB 是 UniFlow 高性能的三个关键设计，缺一不可。
- **Table 14**：UniFlow 以千分之一的数据量达到优于 UniTok 的重建质量，展示了预训练先验与流匹配损失的强大组合效应。

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/036_Table_14.jpg]]
*Table 14: Comparison of Training Efficiency Across Different Unified Tokenizer Paradigms. The table presents rFID scores, with results for each model measured at its respective training resolution*

### 补充图表

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/006_Table_3.jpg]]
*Table 3: Evaluation of text-to-image generation ability on GenEval (Ghosh et al., 2023) and DPG-Bench (Hu et al., 2024) benchmark*

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/042_Figure_21.jpg]]
*Figure 21: Impact of sampling steps on reconstruction*

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/022_Figure_7.jpg]]
*Figure 7: Visualization of image reconstruction. All models are inferred on 448 × 448, except for BLIP3-o, TokenFlow, and QLIP, which are inferred on 512, 384, and 392 respectively*

![[assets/figures/papers/paper_list_l82_https_arxiv_org_abs_2510_10575/figures/014_Figure_6.jpg]]
*Figure 6: Qualitative analysis of representations. (a) VQA: demonstrates UniFlow’s superior understanding of detailed concepts. (b) t-SNE: UniFlow generates more semantically coherent clusters than InternViT and SD-VAE XL. (c) PCA: UniFlow maintains richer spatial information with clearer object contours*

## 方法谱系与知识库定位

### 统一分词器的瓶颈与UniFlow的定位

视觉分词器（visual tokenizer）是将连续图像信号转换为离散或连续编码的核心组件。近年来，两条技术路线并行发展：**生成式分词器**（如 **SD‑VAE**）专注于高保真像素重建，但其编码器缺乏高层语义理解能力；**语义分词器**（如 CLIP、SigLIP）在理解任务上表现优异，却无法直接支持像素生成。**统一分词器**试图弥合这一鸿沟，但面临一个根本性冲突：高层语义理解所需的抽象特征与低层像素生成所需的细粒度细节之间存在优化目标互斥。

现有统一分词器采用了不同的策略来缓解这一冲突：
- **TokenFlow** 冻结预训练语义编码器（如 EMU2），仅训练一个像素解码器，但冻结编码器限制了细节补偿能力。
- **UniTok** 对编码器进行端到端微调并引入像素重建损失，但语义能力在微调过程中容易退化。
- **BLIP3‑o** 和 **QLIP** 也尝试在统一框架中平衡理解与生成，但通常依赖预训练 VAE 作为解码器，引入了解码端的性能瓶颈。

**UniFlow** 的核心创新在于**将理解与生成的解耦从编码器-解码器架构层面推进到训练策略和生成范式层面**：通过层级自适应自蒸馏保留预训练编码器的分层语义知识，同时用轻量级 patch‑wise 像素流解码器直接在像素空间建模条件流，避免了预训练 VAE 的瓶颈。

### 关键设计决策与对比

#### 编码器训练策略：从冻结/端到端到层级自适应自蒸馏

| 方法 | 编码器策略 | 语义保留机制 | 细节补充能力 |
|------|-----------|-------------|-------------|
| TokenFlow | 冻结预训练编码器 | 完全保留 | 无 |
| UniTok | 端到端微调 | 依赖损失平衡 | 有限 |
| **UniFlow** | **层级自适应自蒸馏** | **深层强约束，浅层灵活** | **浅层可补充细节** |

UniFlow 的自蒸馏机制通过公式 $w_{l} = \frac{w_{l}^{\mathrm{base}} \cdot \exp(\beta \cdot \alpha_{l})}{\sum_{k=1}^{L} w_{k}^{\mathrm{base}} \cdot \exp(\beta \cdot \alpha_{k})}$ 动态调整每层蒸馏强度：深层（语义层）获得更高的基础权重以稳定语义表征，浅层（细节层）在蒸馏约束较弱的条件下可灵活适配重建需求。消融实验（Table 6a）证实，β=2 时达到最优平衡，MME‑P 达 1505.1 且 PSNR 为 33.23。

#### 解码器架构：从预训练 VAE 到轻量级像素流解码器

| 方法 | 解码器类型 | 重建空间 | 训练损失 |
|------|-----------|---------|---------|
| SD‑VAE | 预训练 VAE + 扩散解码器 | 潜空间 | GAN + L1 + LPIPS |
| TokenFlow | 像素解码器 | 像素空间 | 多损失组合 |
| **UniFlow** | **Patch‑wise 流匹配解码器** | **像素空间** | **单一流匹配 MSE** |

UniFlow 的解码器是一个轻量级 MLP 网络，在全局 Transformer 块（GTB）提供上下文信息后，直接预测每个 patch 的速度场 $v_{\boldsymbol{\theta}}(\mathbf{x}_{t}^{(i,j)}, t, \mathbf{c}^{(i,j)})$。训练目标为流匹配损失 $\mathcal{L}_{\mathrm{flow}} = \mathbb{E} \| v_{\boldsymbol{\theta}}(\mathbf{x}_{t}^{(i,j)}, t, \mathbf{c}^{(i,j)}) - (\epsilon^{(i,j)} - \mathbf{x}^{(i,j)}) \|_{2}^{2}$，仅需一步 Euler 推理即可完成重建，无需多步扩散采样。消融实验（Figure 5c, Table 6c）表明，6 层 GTB 即可消除网格伪影，PSNR 达 33.23、rFID 达 0.26，更多层数收益递减。

### 适用边界与局限

1. **数据规模与视觉质量**：UniFlow 主要在 ImageNet‑1K（1.2M 图像）上验证，而 UniTok 使用了 1.28B 图像。尽管 UniFlow 在数据效率上显著领先（rFID 0.28 vs 0.38，仅用约千分之一的数据量），但与基于大规模专有数据训练的商用模型相比，在视觉质量上可能存在微小差距。这一结论需要手动验证，论文未提供与商用闭源模型的直接对比。

2. **固定分辨率依赖**：框架依赖于选定预训练编码器的固定输入分辨率（如 InternViT 的 448×448），处理可变分辨率能力受限。论文将此列为开放问题，需进一步开发分辨率无关的扩展。

3. **编码器选择的影响**：不同 VFM 编码器（DFN‑CLIP、SigLIP2、DINOv2、InternViT）在重建和理解任务上表现各异（如 InternViT 重建最优 rFID 0.26，DINOv2 在某些理解任务上有优势），UniFlow 的性能上限仍受限于所选教师编码器的能力。

### 开放问题

1. **大规模数据扩展**：如何利用更大规模、更多样化的数据集来进一步缩小与商用模型的视觉质量差距？论文指出当前数据规模仅为 1.2M，远小于部分基线方法。

2. **分辨率无关扩展**：如何将 UniFlow 扩展为分辨率无关的统一分词器，以适应更广泛的真实场景？当前设计受限于编码器的固定输入分辨率。

3. **生成能力的深度挖掘**：UniFlow 在文本到图像生成任务上展示了初步能力（GenEval 0.65），但与专用生成模型仍有差距。流匹配解码器在生成任务中的潜力尚待进一步探索。

## 原文 PDF

![[paperPDFs/arxiv_2025/UniFlow_A_Unified_Pixel_Flow_Tokenizer_for_Visual_Understanding_and_Generation.pdf]]