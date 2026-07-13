---
title: "Understanding The Robustness in Vision Transformers"
type: paper
paper_level: A
venue: ICML
year: 2022
pdf_ref: paperPDFs/ICML_2022/Understanding_The_Robustness_in_Vision_Transformers.pdf
project_link: null
code_link: https://github.com/NVlabs/FAN
aliases:
- FANF
- URVT
tags:
- ICML_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "在ViT中引入通道自注意力（尤其是高效通道注意力ECA）可以增强通道选择与token聚类精度，从而在不显著增加开销的前提下显著提升模型对腐蚀扰动的鲁棒性。"
primary_logic: "自注意力可被解释为信息瓶颈（IB）的迭代优化，自然导致视觉分组并过滤噪声；通过将通道处理也转换为注意力操作，构建完全注意力网络（FAN），进一步强化分组与鲁棒性之间的共生关系，在多个基准上取得最先进的鲁棒性。"
claims:
- "ViT中层数的增加导致显著特征值数量减少，同时输入高斯噪声的幅值快速衰减，表明分组与鲁棒性之间存在共生关系，而ResNet-50中未观测到该现象。"
- "自注意力可以写成信息瓶颈目标的一个迭代优化步骤（Proposition 2.1），建立起SA与IB的理论联系。"
- "在相同训练配方下，ViT的留存率（72%）仍明显高于ResNet-50（65%），说明鲁棒性优势源于架构中的自注意力设计。"
- "引入高效通道注意力（ECA）将FAN-ViT-S在ImageNet-C上的mCE从56.2降至47.7，同时保持与SE注意力相近的GPU内存占用。"
---

# Understanding The Robustness in Vision Transformers

> [!tip] 核心洞察
> 自注意力可被解释为信息瓶颈（IB）的迭代优化，自然导致视觉分组并过滤噪声；通过将通道处理也转换为注意力操作，构建完全注意力网络（FAN），进一步强化分组与鲁棒性之间的共生关系，在多个基准上取得最先进的鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 理解视觉Transformer的鲁棒性 |
| 英文题名 | Understanding The Robustness in Vision Transformers |
| 会议/期刊 | ICML 2022 |
| Links | [paper](https://arxiv.org/abs/2204.12451) · [GitHub](https://github.com/NVlabs/FAN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Fully Attentional Networks (FANs) |
| Dataset | ImageNet-C, ImageNet-1K, Cityscapes-C, COCO-C |

> [!tip] 效果简介
> - ImageNet-C 上，mCE (lower is better) 为 47.7，对比 76.7，变化 -29.0。
> - ImageNet-1K 上，Top-1 Accuracy 为 87.1。
> - Cityscapes-C 上，mIoU (average over corruptions) 为 66.4，对比 55.8，变化 +10.6。

## 概要

视觉Transformer（ViT）在图像分类任务中展现出优于传统卷积神经网络（CNN）的鲁棒性，但其背后的机制尚不清晰。一个关键瓶颈在于：自注意力（Self-Attention）对鲁棒性的贡献机制未被充分理解，且现代无注意力CNN（如ConvNeXt）也能取得相近的鲁棒性，表明仅靠自注意力并非鲁棒性的唯一来源。

本文的核心洞察是：自注意力可被解释为信息瓶颈（Information Bottleneck, IB）的迭代优化过程，这一过程自然诱导视觉分组（visual grouping）并过滤噪声。基于此，作者提出**完全注意力网络（Fully Attentional Networks, FAN）**，通过将通道处理也转换为注意力操作，强化了分组与鲁棒性之间的共生关系。

FAN的设计要点在于：在标准ViT块的基础上，引入高效通道注意力（Efficient Channel Attention, ECA）替代原有的MLP通道处理，使整个网络实现“完全注意力化”。这一改动在不显著增加计算开销的前提下，显著提升了通道选择与token聚类精度。

在ImageNet-C基准上，FAN-S模型以28M参数量取得47.7%的mCE，大幅优于ResNet-50（76.7%）、Swin-T和ConvNeXt-T等基线。放大至76.8M参数时，mCE进一步降至35.8%，达到监督训练下的最先进水平。同时，FAN在ImageNet-1K上取得87.1%的干净精度。在语义分割（Cityscapes-C）和目标检测（COCO-C）的下游任务中，FAN同样展现出显著优于CNN和Transformer基线的鲁棒性，验证了该设计的通用性。

### 视觉Transformer的鲁棒性之谜

深度神经网络在干净数据上表现优异，但在面对图像腐蚀、天气变化等分布偏移时性能急剧下降，这一鲁棒性缺口严重制约了其在安全关键场景中的部署。视觉Transformer（ViT）的出现为这一问题带来了新的转机：相比传统CNN，ViT在ImageNet-C等鲁棒性基准上展现出显著优势，但其背后的机制一直缺乏清晰解释。

一个直观的假设是，自注意力（Self-Attention, SA）模块赋予了ViT更强的鲁棒性。然而，**ConvNeXt**（Liu et al., 2022）等现代CNN在完全摒弃自注意力的情况下，同样取得了与ViT相近的鲁棒性表现。这一现象揭示了一个关键瓶颈：**自注意力对鲁棒性的贡献机制尚不清晰，仅靠自注意力并非鲁棒性的唯一来源，而当前ViT的设计可能并未充分利用自注意力的潜力来增强鲁棒性。**

### 自注意力的隐藏能力：视觉分组

本文的核心洞察在于重新审视自注意力的本质功能。作者发现，自注意力可以被解释为**信息瓶颈（Information Bottleneck, IB）目标的迭代优化步骤**（Proposition 2.1）。从IB的视角看，自注意力在压缩输入token信息的同时，保留与“干净信号”最相关的特征，这一过程自然导致token的**视觉分组**——相似的token被聚合为语义上有意义的簇，而噪声token则被逐步过滤。

这一分组效应在ViT的深层表现尤为明显。如Figure 3所示，随着层数加深，ViT特征矩阵中显著特征值的数量持续减少（零特征值增多），同时输入高斯噪声的幅值快速衰减。这种**分组与去噪的共生关系**在ResNet-50中未被观察到，暗示自注意力架构天然具备CNN所缺乏的鲁棒性构建机制。

### 从通道处理到完全注意力：FAN的设计动机

尽管自注意力在token维度上实现了有效的分组与噪声过滤，标准ViT的通道处理模块仍采用简单的MLP（两层线性层 + GELU激活）。这种设计存在两个关键缺陷：

1. **通道特征变换缺乏选择性**：MLP对所有通道一视同仁，无法动态筛选与任务相关的通道特征，限制了分组精度的进一步提升。
2. **注意力聚合能力不足**：多头自注意力后的聚合方式依赖固定线性投影，缺乏内容自适应的动态聚合机制。

基于上述分析，本文提出一个自然的改进方向：**将通道处理也转换为注意力操作**，构建**完全注意力网络（Fully Attentional Networks, FAN）**。具体而言，FAN在token自注意力之后引入**高效通道注意力（Efficient Channel Attention, ECA）**，通过通道重标定促进通道选择，从而强化token聚类精度。这一设计以极小的额外开销，将自注意力诱导的视觉分组能力推向极致，在图像分类、语义分割和物体检测三大任务上均取得了最先进的鲁棒性。

### 关键证据预览

- **理论联系**：自注意力可严格写为IB目标的迭代优化步骤（Eqn. 4–5），为分组-鲁棒性共生关系提供理论支撑。
- **实验验证**：在完全相同训练配方下，ViT-S的留存率（72%）仍显著高于ResNet-50（65%），证明架构层面的自注意力设计是鲁棒性优势的独立来源（Table 4）。
- **性能突破**：引入ECA后，FAN-ViT-S在ImageNet-C上的mCE从56.2降至47.7，同时GPU内存占用与SE注意力相当（Table 6）。

## 核心方法与创新机理

### 问题瓶颈：自注意力与鲁棒性的因果断裂

视觉Transformer（ViT）在多种腐蚀扰动下展现出优于传统CNN的鲁棒性，但其核心机制——自注意力（Self-Attention, SA）——究竟如何贡献于鲁棒性，在本文之前仍不清晰。两个关键观察揭示了这一认知断裂：

1. **无注意力的现代CNN同样鲁棒**：ConvNeXt等纯卷积架构在不使用任何自注意力的情况下，也能取得与ViT相近的腐蚀鲁棒性，表明自注意力并非鲁棒性的唯一来源。
2. **分组与鲁棒性的共生关系未被充分利用**：分析发现，随着ViT层数加深，token特征矩阵的显著特征值数量持续减少，同时输入高斯噪声的幅值快速衰减（Figure 3）。这一现象在ResNet-50中完全未观测到，暗示自注意力在深层网络中自然诱导了视觉分组（visual grouping），从而过滤噪声、增强鲁棒性。然而，标准ViT设计并未显式利用这一分组机制，其通道处理仍依赖简单的MLP（两层线性层+GELU），缺乏对通道维度的选择性关注。

### 理论重构：自注意力即信息瓶颈的迭代优化

本文的核心理论贡献在于建立了自注意力与信息瓶颈（Information Bottleneck, IB）之间的形式化联系。具体而言，IB目标旨在将输入 $X$ 压缩为表示 $Z$ 的同时，最大化 $Z$ 与干净信号 $X'$ 之间的互信息：

$$f_{\mathrm{IB}}^{*}(Z|X) = \arg\min_{f(Z|X)} I(X,Z) - I(Z,X')$$

在温和假设下，该目标的迭代优化步骤可精确写为softmax注意力的形式（Proposition 2.1）：

$$\mathbf{z}_c = \sum_{i=1}^{n} \frac{\log[n_c/n]}{n \det \Sigma} \frac{\exp[\mu_c^\top \Sigma^{-1} \mathbf{x}_i / (1/2)]}{\sum_{c=1}^{n} \exp[\mu_c^\top \Sigma^{-1} \mathbf{x}_i / (1/2)]} \mathbf{x}_i$$

其中键矩阵 $K$ 存储临时聚类中心特征，查询矩阵 $Q$ 编码当前token特征。这一等价性揭示了自注意力的本质：**通过softmax竞争机制，自注意力在每一层执行隐式的token聚类与选择，自然形成视觉分组并抑制噪声token的干扰**。

### 架构改造：三个关键changed slots

基于上述理论洞察，本文提出**完全注意力网络（Fully Attentional Networks, FANs）**，对标准ViT块进行了三处关键修改（Figure 2）：

**Slot 1: 通道处理模块 —— MLP → 高效通道注意力（ECA）**

标准ViT的通道处理使用简单的MLP（两层线性层+GELU），对所有通道一视同仁。FAN将其替换为高效通道注意力（Efficient Channel Attention, ECA），通过token原型平均和sigmoid门控实现轻量级通道重标定：

$$\mathrm{ECA}(Z) = \mathrm{Norm}\left(\frac{(W_Q' \sigma(Z)) \sigma(\overline{Z})^\top}{\sqrt{n}}\right) \odot \mathrm{MLP}(Z)$$

其中 $\overline{Z}$ 为沿通道维度平均得到的token原型，$\sigma$ 为sigmoid函数。ECA使模型能够动态选择信息量丰富的通道，过滤不相关特征，从而形成更精确的前景/背景token聚类（Figure 4）。消融实验表明，ECA在鲁棒性（ImageNet-C mCE 47.7）上显著优于标准通道自注意力CA（mCE 51.4）和SE注意力（mCE 50.0），且GPU内存占用与SE相当（Table 6）。

**Slot 2: 注意力聚合方式 —— 仅token自注意力 → token自注意力 + 通道自注意力**

标准ViT仅使用多头自注意力进行token混合，随后用MLP聚合多头输出。FAN在token自注意力之后引入通道自注意力（Channel Attention, CA），沿通道维度计算注意力矩阵以利用特征协方差进行动态特征变换：

$$\operatorname{CA}(Z) = \operatorname{Softmax}\left(\frac{(W_Q' Z)(W_K' Z)^\top}{\sqrt{n}}\right) \operatorname{MLP}(Z)$$

这一设计使整个网络成为“完全注意力”架构——token维度和通道维度均由注意力操作驱动，强化了分组与鲁棒性之间的共生关系。

**Slot 3: 通道处理后的线性投影 —— 保留 → 移除**

标准ViT在MLP后设有一个线性投影层。FAN块中，该线性投影层被移除（Figure 2 caption），简化了信息流并减少了冗余参数。

### 创新本质：从隐式分组到显式共生

FAN的核心创新不在于引入全新的操作原语，而在于**将自注意力诱导的隐式视觉分组显式化为架构设计原则**。通过将通道处理也转换为注意力操作，FAN在token和通道两个维度上同时执行选择性信息聚合，使分组过程更加精确、噪声抑制更加彻底。这一设计在多个基准上得到验证：FAN系列模型在图像分类（ImageNet-C mCE 47.7）、语义分割（Cityscapes-C mIoU 66.4）和物体检测（COCO-C mAP 35.5）三个任务上均大幅超越CNN和Transformer基线，取得最先进的鲁棒性。

FAN（Fully Attentional Networks）的整体设计围绕一个核心洞察展开：自注意力（Self-Attention, SA）可被解释为信息瓶颈（Information Bottleneck, IB）目标的迭代优化步骤，该过程自然诱导视觉分组（visual grouping）并过滤噪声。为充分利用这一机制，FAN 将标准 ViT 块中的 MLP 通道处理替换为通道注意力，构建了一个完全由注意力操作驱动的网络。

### Pipeline 总览

FAN 的基本计算单元是 **FAN block**，它由两个串联的注意力模块构成：

1. **Token Self-Attention（Token SA）**：负责 token 间的信息混合，沿序列维度计算注意力，聚合上下文特征。
2. **Channel Attention（CA）**：负责通道维度的特征变换与动态选择，利用特征协方差进行通道重标定。

输入图像首先被切分为 patch 并线性投影为 token 序列 $X \in \mathbb{R}^{n \times d}$（$n$ 为 token 数，$d$ 为通道数），随后依次通过多个 FAN block。每个 FAN block 的前向流程为：

$$
Z^\top = \mathrm{SA}(X) = \mathrm{Softmax}\left(\frac{Q^\top K}{\sqrt{d}}\right) V^\top W_L \quad \text{(Token 混合)}
$$

$$
Z' = \mathrm{CA}(Z) \quad \text{或} \quad Z' = \mathrm{ECA}(Z) \quad \text{(通道注意力特征变换)}
$$

其中，**Efficient Channel Attention（ECA）** 是实际部署中采用的轻量级通道注意力设计，旨在以极低的计算开销实现通道选择。

### 模块关系与设计逻辑

FAN block 的设计遵循“先 token 混合，后通道选择”的范式，其关键改动体现在两个层面：

- **通道处理模块的替换**：标准 ViT 块在 SA 之后使用两层 Linear + GELU 的 MLP 进行通道特征变换。FAN 将其替换为通道自注意力（CA）或高效通道注意力（ECA），使通道维度的信息聚合也由注意力机制驱动，从而形成“完全注意力”网络。
- **线性投影层的移除**：在标准 ViT 中，SA 输出后跟随一个线性投影层 $W_L$ 用于多头聚合。FAN block 中，通道注意力直接作用于 SA 的多头输出，该线性投影层被移除，由通道注意力承担动态、内容依赖的聚合功能。

FAN 提供了三种模型变体以适应不同场景：

- **FAN-ViT**：将标准 ViT 的 transformer block 全部替换为 FAN block，保持各向同性结构。
- **FAN-Hybrid**：在底层两个阶段使用卷积块（基于 ConvNeXt 设计）进行下采样和局部特征提取，顶层使用 FAN block，兼顾大分辨率输入的效率与注意力带来的鲁棒性。
- **FAN-SWIN**：在 Swin Transformer 的特征变换部分引入 ECA，弥补窗口自注意力在 token 选择上的局限性。

### 输入输出流

以图像分类为例，输入图像经 patch embedding 后得到 token 序列，依次通过多个 FAN block。每个 block 内，token SA 利用 softmax 归一化促进 token 间的竞争性选择，形成初步的视觉分组；随后的通道注意力（ECA）通过 token 原型平均和 sigmoid 门控对通道进行重标定，过滤无关特征，强化分组精度。最终输出的 [CLS] token 或全局平均池化特征用于分类。

在下游密集预测任务（语义分割、目标检测）中，FAN-Hybrid 或 FAN-SWIN 作为骨干网络，其多尺度特征图被送入任务特定的解码器（如 DeepLabv3+、Mask R-CNN），整个流程无需腐蚀相关的微调或对抗训练。

### 2.1 标准ViT块：Token混合与通道处理

FAN模型的构建起点是标准Vision Transformer（ViT）块。每个Transformer块包含两个核心操作：

**Token自注意力（Token Self-Attention）** 负责token间的信息混合。给定输入token序列 $X$，通过线性投影得到查询 $Q = W_Q X$、键 $K = W_K X$ 和值 $V = W_V X$，自注意力的计算为：

$$Z^{\top} = \mathrm{SA}(X) = \mathrm{Softmax}\left(\frac{Q^{\top}K}{\sqrt{d}}\right)V^{\top}W_L$$

其中 $d$ 为键的维度，$W_L$ 为输出投影矩阵。Softmax归一化促使不同token之间产生竞争，从而实现对特定token的选择性聚合。

**通道处理** 由两层全连接网络和GELU激活函数组成的MLP实现：$Z' = \mathrm{MLP}(Z)$。该MLP沿通道维度独立作用于每个token，完成特征变换。

### 2.2 自注意力与信息瓶颈的理论联系

论文的核心理论贡献在于建立了自注意力与信息瓶颈（Information Bottleneck, IB）之间的形式化联系。信息瓶颈的目标是在压缩输入 $X$ 到表示 $Z$ 的同时，最大化保留关于干净信号 $X'$ 的信息：

$$f_{\mathrm{IB}}^{*}(Z|X) = \arg\min_{f(Z|X)} I(X,Z) - I(Z,X')$$

**Proposition 2.1** 指出，在温和假设下，优化上述IB目标的迭代步骤可写为：

$$\mathbf{z}_c = \sum_{i=1}^{n} \frac{\log[n_c/n]}{n \det \Sigma} \frac{\exp[\mu_c^{\top} \Sigma^{-1} \mathbf{x}_i / (1/2)]}{\sum_{c=1}^{n} \exp[\mu_c^{\top} \Sigma^{-1} \mathbf{x}_i / (1/2)]} \mathbf{x}_i$$

这一形式等价于softmax注意力机制，其中键矩阵 $K$ 存储了可学习的临时聚类中心特征 $\mu_c$。该理论联系揭示了自注意力的本质：它隐式地执行视觉分组（visual grouping），将相似token聚合为簇，同时过滤噪声信息。

### 2.3 通道自注意力（Channel Attention, CA）

基于上述洞察，FAN块在token自注意力之后引入通道维度的自注意力，替代原有的MLP通道处理。通道自注意力的设计利用了特征协方差进行特征变换：

$$\operatorname{CA}(Z) = \operatorname{Softmax}\left(\frac{(W_Q' Z)(W_K' Z)^{\top}}{\sqrt{n}}\right) \operatorname{MLP}(Z)$$

与token自注意力不同，CA沿通道维度而非token维度计算注意力矩阵。这使得模型能够动态地选择和重标定通道特征，过滤不相关特征，进而形成更精确的前景/背景token聚类。

### 2.4 高效通道注意力（Efficient Channel Attention, ECA）

为降低标准通道自注意力的计算开销，论文进一步提出高效通道注意力（ECA）。ECA包含两个关键改进：

1. **Token原型生成**：通过对通道维度求平均得到token原型 $\overline{Z}$，避免计算完整的 $n \times n$ 注意力矩阵。
2. **Sigmoid门控归一化**：使用Sigmoid函数替代Softmax进行注意力权重归一化，实现更灵活的通道重标定。

ECA的完整计算为：

$$\mathrm{ECA}(Z) = \mathrm{Norm}\left(\frac{(W_Q' \sigma(Z)) \sigma(\overline{Z})^{\top}}{\sqrt{n}}\right) \odot \mathrm{MLP}(Z)$$

其中 $\sigma$ 为Sigmoid函数，$\odot$ 表示逐元素乘法。与标准CA（mCE 51.4）和SE注意力（mCE 50.0）相比，ECA在ImageNet-C上取得了最优鲁棒性（mCE 47.7），同时GPU内存占用与SE注意力相当（Table 6）。

### 2.5 FAN块整体架构

FAN块将上述模块整合为一个完全注意力化的处理单元：输入token首先经过多头token自注意力进行token混合，随后通过高效通道注意力（ECA）完成通道特征变换与动态选择。与标准ViT块相比，FAN块移除了通道注意力之后的线性投影层，使整个网络完全由注意力操作构成（Figure 2）。这种设计强化了自注意力诱导的视觉分组与鲁棒性之间的共生关系。

## 实验与关键发现

### 训练配方与架构优势的解耦

为区分训练技巧与架构本身对鲁棒性的贡献，作者在完全相同的DeiT训练配方（含CutMix、RandAugmentation等）下复现了ResNet-50*和ViT-S*。结果（Table 4）表明，即使训练配方完全相同，ViT-S*的留存率（72%）仍显著高于ResNet-50*（65%），说明自注意力架构对鲁棒性的优势独立于训练技巧。Table 2进一步显示，知识蒸馏和ImageNet-22K预训练等高级技巧虽能提升ViT-S的绝对精度，但未能显著缩小干净精度与腐蚀精度之间的差距——留存率始终维持在72%–73%区间，mCE在54.0–56.2之间波动。这意味着**主要鲁棒性改进源于架构本身，而非训练技巧的堆叠**。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2204_12451/figures/007_Table_4.jpg]]
*Table 4: Robustness comparison between ResNet-50 and ViT-S (%)*

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2204_12451/figures/008_Table_2.jpg]]
*Table 2: Impacts of various performance improvement tricks on model robustness (%)*

值得注意的是，为ResNet-50添加SE注意力模块后，其留存率从60%提升至63%（Table 3），说明通道重标定机制对CNN同样有益，但提升幅度远不及ViT架构的固有优势。这一发现直接支持了论文的核心论点：自注意力中的softmax归一化促进了token间的竞争与选择，从而自然形成视觉分组并过滤噪声。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2204_12451/figures/010_Table_3.jpg]]
*Table 3: Robustness of ResNet-50 with various performance improvement tricks (%)*

### 消融研究：通道注意力设计与架构变化

作者在FAN-ViT-S框架下系统消融了通道注意力设计的影响（Table 6）。标准通道自注意力（CA）将mCE从基线ViT-S的56.2降至51.4，但GPU内存消耗高达21.2 GB。SE注意力以较低内存（12.6 GB）将mCE降至50.0。**提出的高效通道注意力（ECA）以与SE相当的内存（12.8 GB）将mCE进一步降至47.7**，留存率提升至78%，在所有设计中取得最优权衡。ECA的核心优势在于：通过token原型平均和sigmoid门控替代softmax归一化，既保留了通道选择能力，又大幅降低了计算开销。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2204_12451/figures/011_Table_6.jpg]]
*Table 6: Effects of different channel attentions on model robustness (%)*

将FAN块移植到Swin Transformer进一步验证了设计的通用性（Table 7）。在Swin-T中添加ECA后，ImageNet-C准确率从55.4%提升至59.4%，有效弥补了窗口自注意力带来的鲁棒性损失。这一结果表明，**通道注意力机制可以作为独立模块增强不同Transformer变体的鲁棒性**。

关于多头数量的分析（Figure 7）揭示了表达能力与鲁棒性之间的权衡：增加头数可提升鲁棒性，但每头通道数过少会导致干净精度下降，最佳权衡点为每头32通道。

### 图像分类鲁棒性主结果

Table 8汇总了ImageNet-C上的分类鲁棒性对比。FAN系列模型在不同规模下均大幅超越CNN和Transformer基线：

- **FAN-S-ViT**（28.3M参数）在ImageNet-C上达到64.5%准确率，mCE为47.7，留存率78%，显著优于同规模的DeiT-S（55.4% / 50.2 / 70%）和ConvNeXt-T（57.8% / 51.2 / 70%）。
- **FAN-B-ViT**（54.0M参数）进一步将ImageNet-C提升至67.0%，留存率79%。
- 缩放至76.8M参数的**FAN-L-Hybrid**达到35.8% mCE，在监督训练设置下取得当时最先进的鲁棒性，同时保持87.1%的ImageNet-1K干净精度。

Table 12的逐类腐蚀细分显示，FAN在所有19种ImageNet-C腐蚀类型下均优于对比模型，尤其在“雪”“霜冻”“雾”等高频纹理破坏场景下优势更为突出。

### 下游任务鲁棒性

**语义分割**（Table 9）：在Cityscapes-C上，FAN-B-Hybrid以66.4% mIoU显著超越SegFormer-B2（55.8% mIoU），提升达10.6个百分点，留存率高达81.5%。即使在脉冲噪声（severity 3）和雪（severity 3）等极端腐蚀下，FAN-Hybrid仍能保持清晰的分割边界（Figure 6），而SegFormer出现大面积误分割。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2204_12451/figures/013_Figure_6.jpg]]
*Figure 6: Segmentation visualization on corrupted images with impulse noise (severity 3) and snow (severity 3). We select the recent state-of-the-art SegFormer model (Xie et al., 2021) as a strong baseline. FAN-S-H denotes our hybrid model. Under comparable model size and computation, FAN achieve significantly improved segmentation results over ResNet-50 and SegFormer-B2 model. A video demo is available via external players*

**目标检测**（Table 10）：在COCO-C上，FAN-S-Hybrid以35.5% mAP超越Swin-T（29.3% mAP），提升6.2个百分点，留存率72.3%。Table 14的逐类分析确认FAN在所有腐蚀类型下均保持优势。

**分布外泛化**（Table 11）：FAN在ImageNet-A和ImageNet-R上同样展现更强的泛化能力，表明完全注意力设计不仅提升对合成腐蚀的鲁棒性，也增强了对自然分布偏移的适应能力。

### 失败模式与局限性

尽管FAN在腐蚀鲁棒性上表现突出，以下局限性值得关注：

1. **理论假设的边界**：信息瓶颈与自注意力的理论联系建立在若干温和假设之上（Proposition 2.1），可能无法完整刻画自注意力在深层网络中的所有行为。当数据分布严重偏离假设时，分组与鲁棒性的共生关系是否仍然成立尚需验证。

2. **混合模型的归因困难**：FAN-Hybrid使用了ConvNeXt的卷积阶段进行下采样，因此完全注意力设计的独立贡献在混合模型中并非完全可分离。ConvNeXt-T本身已展现强鲁棒性（留存率70%），FAN-Hybrid-S的提升（留存率78%）中，卷积阶段与注意力阶段各自的贡献权重难以精确量化。

3. **评估覆盖范围有限**：鲁棒性评估集中在ImageNet-C等常见腐蚀基准，对对抗攻击、背景剧烈变化、跨域迁移等更广泛的分布外场景的覆盖有限。尽管Table 11展示了在ImageNet-A和ImageNet-R上的初步结果，但缺乏与对抗训练方法的直接对比。

4. **大规模部署的计算瓶颈**：尽管ECA显著降低了通道注意力的开销（Table 6），但在超大模型尺度下，额外的通道计算仍可能成为瓶颈。FAN-L-Hybrid的15.8G FLOPs相比同规模纯CNN或纯ViT有所增加，需要进一步优化以实现实际部署中的效率-鲁棒性平衡。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2204_12451/figures/022_Figure_8.jpg]]
*Figure 8: Visualization on Cityscapes. A video demonstration is available with external player*

## 定位与知识库关联

### 核心基线谱系

FAN 的提出建立在对以下基线的系统消融与对比之上：

| 基线模型 | 角色定位 | 关键引用 |
|---------|---------|---------|
| **ResNet-50** | 标准CNN鲁棒性基线 | He et al., CVPR 2016 |
| **ViT-S** | 标准ViT基线，含自注意力但无通道注意力 | Dosovitskiy et al., ICLR 2021 |
| **DeiT-S** | 使用高级训练配方（蒸馏、数据增强）的ViT | Touvron et al., ICML 2021 |
| **Swin-T** | 层级Transformer基线，采用窗口自注意力 | Liu et al., ICCV 2021 |
| **ConvNeXt-T** | 现代CNN基线，无自注意力但鲁棒性接近ViT | Liu et al., CVPR 2022 |
| **SegFormer-B2** | 分割任务Transformer基线 | Xie et al., NeurIPS 2021 |

FAN 在方法上同时借鉴了 **XCiT**（El-Nouby et al., 2021）的通道自注意力设计思路，但将其应用位置从MLP输入改为MLP输出，并进一步简化为高效通道注意力（ECA）。

### 方法演进路径

FAN 的设计遵循一条清晰的因果链：

1. **诊断瓶颈**：观察到 ViT 中层数增加时，特征矩阵的显著特征值数量减少、输入高斯噪声幅值快速衰减（Figure 3），而 ResNet-50 中不存在该现象。这表明自注意力诱导的**视觉分组**与鲁棒性之间存在共生关系，但标准 ViT 仅将自注意力用于 token 混合，通道处理仍依赖 MLP，未能充分利用这一机制。

2. **理论桥接**：将自注意力解释为信息瓶颈（IB）目标的一个迭代优化步骤（Proposition 2.1），建立 SA 与 IB 的理论联系。IB 目标 $\min I(X,Z) - I(Z,X')$ 本质是压缩输入 $X$ 到表示 $Z$ 的同时保留关于干净信号 $X'$ 的信息，而 softmax 注意力恰好实现了对 token 的竞争性选择与聚类中心更新。

3. **架构补全**：在 token 自注意力之后引入**通道自注意力**（CA），使通道维度的特征变换也从静态 MLP 变为动态的、内容依赖的注意力聚合。这一改动将整个 block 变为“完全注意力”（Fully Attentional），强化了分组与噪声过滤的共生关系。

4. **效率优化**：标准 CA 的注意力矩阵尺寸为 $C \times C$（$C$ 为通道数），计算开销较大。ECA 通过 token 原型平均和 sigmoid 门控，将注意力计算简化为查询向量与原型向量的点积，在保持鲁棒性优势的同时将 GPU 内存消耗降至与 SE 注意力相当（Table 6）。

### 与同期工作的关系

- **与 ConvNeXt 的对比**：ConvNeXt 证明了无自注意力的纯 CNN 也能取得接近 ViT 的鲁棒性，这表明自注意力并非鲁棒性的唯一来源。FAN 的回应是：自注意力驱动的分组机制确实有效，但标准 ViT 未充分利用它；通过将通道处理也转为注意力操作，FAN 在 ConvNeXt 之上进一步提升了鲁棒性（FAN-Hybrid 的早期阶段直接使用 ConvNeXt 的卷积块）。

- **与 Swin Transformer 的对比**：Swin 的窗口自注意力限制了 token 混合的感受野，当窗口内缺乏关键信息时可能选择无关 token。FAN-SWIN 实验（Table 7）表明，仅将 Swin 的 MLP 替换为 ECA，ImageNet-C 准确率即从 55.4% 提升至 59.4%，说明通道注意力可部分弥补局部自注意力的鲁棒性损失。

- **与 SE/SENet 的对比**：SE 注意力通过全局平均池化生成通道权重，是一种静态的通道重标定。ECA 则通过 token 原型与查询的交互实现动态的、内容依赖的通道选择，在 mCE 上优于 SE（47.7 vs 50.0），且内存消耗相当（Table 6）。

### 适用边界与局限

**适用场景**：
- 图像分类、语义分割、目标检测等标准视觉任务，在常见腐蚀（ImageNet-C、Cityscapes-C、COCO-C）下表现出强鲁棒性。
- 分布外泛化（ImageNet-A、ImageNet-R）同样有效（Table 11）。
- 支持从 Tiny（7.3M 参数）到 Large（80.5M）的多尺度部署。

**已知局限**：
1. **理论假设的温和性**：IB 与 SA 的理论等价建立在若干温和假设之上（如高斯先验、聚类结构），可能无法完整刻画自注意力的所有行为，尤其是深层网络中的非线性交互。
2. **混合模型的归因困难**：FAN-Hybrid 使用了 ConvNeXt 的卷积阶段，因此完全注意力设计的独立贡献在混合模型中并非完全可分离。
3. **腐蚀类型覆盖有限**：鲁棒性评估集中在常见腐蚀（噪声、模糊、天气、数字变换），对对抗攻击、背景域偏移等更广泛的分布外场景的覆盖有限。
4. **超大模型的扩展性**：尽管 ECA 显著降低了通道注意力的开销，但在超大模型尺度下，额外的通道计算仍可能成为瓶颈，需进一步优化或与稀疏注意力结合。

### 开放问题

1. **跨任务泛化**：自注意力驱动的视觉分组现象在视频理解、3D 视觉、多模态任务中是否同样存在并有利于鲁棒性？FAN 的完全注意力设计能否直接迁移？

2. **跨模态推广**：IB-SA 理论联系和完全注意力设计是否适用于自然语言处理或其他序列建模任务，以提升对输入噪声的鲁棒性？

3. **归纳偏置的精确隔离**：ConvNeXt 等无注意力 CNN 展现的强鲁棒性表明，卷积的局部性、平移等变性等归纳偏置也能发挥作用。如何设计更干净的对照实验，精确量化自注意力的独立贡献？

4. **分组-鲁棒性的定量理论**：目前仅观察到分组程度与鲁棒性之间的定性共生关系（特征值稀疏化 ↔ 噪声衰减），能否建立定量的理论关系（如分组纯度与 mCE 的函数形式），从而指导架构的超参数设计（如头数、层数）？

5. **与对抗训练的协同**：FAN 目前仅评估了未经腐蚀微调的标准训练模型。完全注意力设计与对抗训练、腐蚀数据增强等鲁棒训练范式之间是否存在协同效应或冲突？

## 原文 PDF

![[paperPDFs/ICML_2022/Understanding_The_Robustness_in_Vision_Transformers.pdf]]
