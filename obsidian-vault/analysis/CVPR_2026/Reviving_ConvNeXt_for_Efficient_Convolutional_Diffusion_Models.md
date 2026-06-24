---
title: Reviving ConvNeXt for Efficient Convolutional Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Reviving_ConvNeXt_for_Efficient_Convolutional_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- RCECDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 卷积网络固有的局部归纳偏置与参数效率，使其能够在更小的计算开销下学习有效的视觉表示。
primary_logic: 通过复兴并重新设计ConvNeXt架构以整合条件注入、简化的U形设计和有效的通道增强机制（GRN），构建的全卷积扩散模型(FCDM)在计算效率、收敛速度和生成质量上均显著优于基于Transformer的DiT及其他同期的卷积扩散模型。
claims:
- FCDM-XL仅需1M训练步数即达到FID 7.9（无指导），而DiT-XL/2需7M步数达到FID 9.6。
- FCDM-XL在256×256上仅有65 GFLOPs，约是DiT-XL/2 (119 GFLOPs) 的54%，吞吐量达到272.7 it/s，是DiT-XL/2 (80.5 it/s) 的3.4倍。
- 在所有尺度（S、B、L、XL）下，FCDM均比DiT具有更低的FID和更高的吞吐量。
- 消融实验证明，GRN层比DiCo的CCA更有效地增强通道多样性，且无需额外参数。
---

# Reviving ConvNeXt for Efficient Convolutional Diffusion Models

> [!tip] 核心洞察
> 通过复兴并重新设计ConvNeXt架构以整合条件注入、简化的U形设计和有效的通道增强机制（GRN），构建的全卷积扩散模型(FCDM)在计算效率、收敛速度和生成质量上均显著优于基于Transformer的DiT及其他同期的卷积扩散模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 复兴ConvNeXt以实现高效卷积扩散模型 |
| 英文题名 | Reviving ConvNeXt for Efficient Convolutional Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.09408) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | FCDM |
| Dataset | ImageNet 256×256, ImageNet 512×512 |

> [!tip] 效果简介
> - ImageNet 256×256 上，FID (无指导) 7.91 (1M steps) vs DiT-XL/2: 9.62 (7M steps) (-1.71)；FLOPs (G) 64.6 vs DiT-XL/2: 118.6 (-54.0)；Throughput (it/s) 272.7 vs DiT-XL/2: 80.5 (+192.2)。
> - ImageNet 512×512 上，FID (无指导) 7.46 (1M steps) vs DiT-XL/2: 12.03 (3M steps) (-4.57)。

## 概述

扩散模型已成为视觉生成的主流范式，但其骨干网络目前几乎被 Transformer 架构垄断。尽管 Transformer 具备良好的缩放特性，其巨大的计算量与资源需求严重限制了训练与推理效率，构成了当前扩散模型规模化的真实瓶颈。卷积网络天然具备局部归纳偏置与参数效率优势，理论上能够在更小的计算开销下学习有效的视觉表示，但此前卷积扩散模型在生成质量与缩放能力上始终未能与 Transformer 抗衡。

本文提出**全卷积扩散模型（Fully Convolutional Diffusion Model, FCDM）**，通过复兴并重新设计 ConvNeXt 架构，构建了一个专为条件扩散建模优化的纯卷积骨干网络。其核心洞察在于：将卷积固有的效率优势与现代扩散模型所需的条件注入机制、多尺度表示能力相结合，可以在大幅降低计算开销的同时实现更快的收敛和更优的生成质量。

具体而言，FCDM 在 ConvNeXt 基础上做出了四项关键改进：（1）引入**自适应层归一化（AdaLN）**替代标准 LayerNorm，用于注入时间步与类别条件；（2）采用**全局响应归一化（GRN）**替代传统通道注意力，以无额外可学习参数的方式增强通道激活多样性；（3）采用**倒置瓶颈结构**，在深度卷积前进行通道扩张以丰富表示；（4）将上述模块组织为**可缩放的 U 形编码器-解码器架构**，配合跳跃连接实现多尺度特征学习。

实验结果表明，FCDM 在效率与性能上均显著超越主流基线。在 ImageNet 256×256 无条件生成任务上，**FCDM-XL 仅需 1M 训练步数即达到 FID 7.91，而 DiT-XL/2 需 7M 步数才达到 FID 9.62**；同时 FCDM-XL 的 FLOPs 仅为 64.6 G，约为 DiT-XL/2（118.6 G）的 54%，吞吐量达到 272.7 it/s，是后者的 3.4 倍。这一效率-性能双重优势在所有模型尺度（S、B、L、XL）下均一致成立，证明卷积架构的缩放能力并不逊于 Transformer。

消融研究进一步验证了各设计选择的有效性：GRN 层相较 DiCo 的 CCA 机制将 FID 从 23.85 降至 19.97，且无需额外参数；7×7 深度卷积在效率与性能间达到最优平衡；全卷积设计在 FID 和吞吐量上均优于局部自注意力替代方案。

## 背景与动机

扩散模型已成为视觉生成领域的主导范式，其核心在于学习一个逐步去噪的过程，将随机噪声映射为高保真图像。然而，当前主流的扩散骨干网络几乎完全被 Transformer 架构所垄断。以 **DiT**（Peebles & Xie, ICCV 2023）为代表的工作将 Vision Transformer 引入扩散模型，证明了 Transformer 在条件图像生成中的强大扩展性，此后一系列后续工作进一步巩固了这一趋势。

**Transformer 的效率瓶颈。** Transformer 的统治地位并非没有代价。其核心操作——多头自注意力——的计算复杂度随序列长度呈二次增长，导致模型在训练和推理阶段的计算量与资源需求极为庞大。以 DiT-XL/2 为例，在 256×256 分辨率下，单次前向传播需要约 119 GFLOPs，吞吐量仅为 80.5 it/s。这种计算开销严重限制了扩散模型的迭代速度与部署可行性，使得高效扩散骨干网络的研究成为亟待解决的问题。

**卷积网络的潜在优势。** 在 Transformer 主导扩散模型之前，卷积神经网络（CNN）曾是视觉生成的主流选择。卷积操作具有天然的局部归纳偏置和参数效率——深度可分离卷积的计算量远低于自注意力，且能够以更少的参数学习有效的视觉表示。然而，早期卷积扩散模型在生成质量上逐渐落后于 Transformer，导致研究重心向后者倾斜。一个关键问题是：**扩展性是否真的是 Transformer 的专属特性？** 卷积网络能否在保持参数效率的同时，实现与 Transformer 相当甚至更优的扩展性与生成质量？

**现有卷积扩散模型的不足。** 近期，一些工作尝试将卷积网络重新引入扩散模型。**DiCo**（Cao et al., NeurIPS 2025）作为当前最先进的卷积扩散模型，虽然证明了全卷积设计的可行性，但其架构仍存在冗余：包含额外的逐点卷积通道注意力模块（CCA）和独立的前馈网络，增加了不必要的计算开销。**DiC**（Wang et al., CVPR 2025）同样探索了卷积扩散方向，但在效率与性能的平衡上仍有改进空间。这些工作表明，简单地复用现有卷积架构不足以充分发挥卷积网络在扩散模型中的潜力，需要针对条件扩散建模进行专门的架构重设计。

**本文动机。** 基于上述观察，本文提出复兴 ConvNeXt 架构，构建一个专为条件扩散建模设计的全卷积扩散模型（Fully Convolutional Diffusion Model, FCDM）。ConvNeXt 通过将现代 Transformer 的设计理念迁移到卷积网络，已在判别任务中证明了其竞争力。本文的核心洞察在于：通过重新设计 ConvNeXt 以整合条件注入机制、简化 U 形多尺度架构，并引入高效的通道增强策略（全局响应归一化 GRN），可以在显著降低计算开销的同时，实现优于 Transformer 的收敛速度与生成质量。这一方向旨在回答一个根本性问题——在扩散模型中，卷积网络能否在效率与扩展性上全面超越 Transformer？

## 核心创新

### 问题瓶颈与设计动机

当前扩散模型的主流骨干网络依赖 Transformer 架构（如 **DiT**，Peebles & Xie, ICCV 2023），尽管其在模型缩放上表现出色，但计算量与资源需求巨大，严重制约了训练与推理效率。卷积网络固有的局部归纳偏置与参数效率，使其能够在更小的计算开销下学习有效的视觉表示，这构成了复兴卷积架构以构建高效扩散模型的核心动机。

### 关键创新点：从 ConvNeXt 到 FCDM

FCDM 并非简单复用 ConvNeXt，而是围绕条件扩散建模的需求对其进行了系统性重构。相较于基线方法 DiT 和同期最强的卷积扩散模型 **DiCo**（Cao et al., NeurIPS 2025），FCDM 在四个关键设计槽位上做出了针对性改变：

**1. 条件注入机制：AdaLN 替代 LayerNorm**

DiT 使用自适应层归一化（AdaLN）将时间步和类别条件注入 Transformer 块。FCDM 将这一机制迁移至卷积架构中，用 AdaLN 替换 ConvNeXt 原有的 LayerNorm。具体而言，条件嵌入模块（MLP）将条件向量映射为 $(\gamma, \beta, \alpha)$ 三组调制参数，其中最终调制尺度 $\alpha$ 采用零初始化以稳定深层训练。这一设计使全卷积网络能够灵活地融合条件信息，同时保持训练稳定性。

**2. 通道增强机制：GRN 替代 CCA**

DiCo 采用通道注意力（CCA）通过额外的 $1 \times 1$ 逐点卷积学习通道激活权重。FCDM 则引入全局响应归一化（GRN），利用 L2 归一化等无参数操作增强通道激活多样性，完全消除了 CCA 所需的额外可学习参数。这一替换不仅简化了模块结构，还在消融实验中展现出显著优势：在相同训练步数下，GRN 使 FID 从 CCA 的 23.85 降至 19.97。

**3. 瓶颈结构：倒置瓶颈替代标准残差块**

FCDM 采纳 ConvNeXt 的倒置瓶颈设计，在深度卷积之前进行通道扩张，使网络能够在更丰富的通道空间中计算特征表示，而深度卷积的计算开销保持不变。消融实验表明，移除倒置瓶颈或将其替换为标准 ResNet 块会严重损害性能，FID 从 19.97 飙升至 31.14，验证了该设计对表征学习的关键作用。

**4. 架构简化：去除额外前馈模块**

DiCo 在块内包含独立的前馈模块以增强表示能力。FCDM 选择去除这一模块，依赖倒置瓶颈中已扩展的通道计算来提供足够的非线性变换能力，从而得到更简洁高效的块结构。

### 架构组织：可缩放的 U 形设计

除块级创新外，FCDM 将上述 FCDM 块组织为 U 形编码器-解码器架构，并引入跳跃连接以实现多尺度表示学习。该 U 形设计天然支持灵活的深度和宽度缩放，使 FCDM 能够像 DiT 一样在不同参数量级（S、B、L、XL）下进行规模化扩展。

## 整体框架

FCDM 的整体架构遵循“潜空间编码 → 条件化 U 形卷积主干 → 潜空间解码”的流水线。输入图像首先由预训练的变分自编码器（VAE）压缩为低维潜变量 $z_t$，该潜变量与时间步 $t$ 和类别标签 $y$ 共同送入 FCDM 主干网络，预测噪声 $\epsilon_\theta(z_t, t, y)$，再通过 DDPM 调度器逐步去噪还原潜变量，最终由 VAE 解码器生成图像。

主干网络的核心是 **FCDM 块**，其设计直接继承 ConvNeXt 的倒置瓶颈结构，但针对条件扩散建模进行了三项关键改造：

1. **条件注入**：将 ConvNeXt 中的 LayerNorm 替换为自适应层归一化（AdaLN）。条件嵌入模块（MLP）将时间步和类别条件映射为调制参数 $(\gamma, \beta, \alpha)$，其中 $\gamma$ 和 $\beta$ 分别对归一化特征进行缩放和平移，$\alpha$ 作为最终的残差调制尺度。遵循 DiT 的做法，$\alpha$ 被零初始化以稳定深层训练。
2. **通道正则化**：在倒置瓶颈的末端引入全局响应归一化（GRN），通过 L2 归一化和通道间竞争机制增强激活多样性，替代 DiCo 中需要额外 $1 \times 1$ 卷积的通道注意力模块（CCA），且不引入任何可学习参数。
3. **简化设计**：移除 DiCo 中的前馈模块，仅保留深度可分离卷积（DWConv）和逐点卷积（PWConv）构成的基本残差路径，使块结构更精简高效。

这些 FCDM 块按 **U 形编码器-解码器** 组织。编码器逐级下采样提取多尺度特征，解码器通过跳跃连接融合对应层级的编码器特征后逐级上采样。模型规模通过调整各阶段的块数和通道数进行缩放（S/B/L/XL），所有尺度共享相同的训练超参数。这种设计使 FCDM 在保持卷积网络局部归纳偏置和参数效率的同时，获得了与 Transformer 主干可比拟的扩展能力。

![Figure 3](item_006)

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/006_Figure_3.jpg]]
*Figure 3: The Fully Convolutional Diffusion Model (FCDM) architecture. (a) Details of the ConvNeXt block. (b) Our FCDM block, which incorporates conditioning via adaptive layer normalization. (c) We train conditional latent FCDMs. The input latent is processed by multiple FCDM blocks arranged in an easily scalable U-shaped architecture*

### 补充图表

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/026_Figure_9.jpg]]
*Figure 9: Conditioning modules for class and text in the FCDM architecture. (a) FCDM block with conditioning vector c, (b) Conditioning module for class conditioning, (c) Conditioning module for text conditioning incorporating the CLIP text encoder*

## 核心模块与公式推导

### 3.1 自适应层归一化（AdaLN）

FCDM 沿用 ConvNeXt 的核心设计原则，但为了支持条件扩散建模，将标准 LayerNorm 替换为**自适应层归一化（Adaptive Layer Normalization, AdaLN）**，作为时间步与类别条件注入的机制。

条件向量 $c$ 首先通过一个 MLP 模块映射为三组调制参数——尺度 $\gamma$、偏移 $\beta$ 和门控残差尺度 $\alpha$：

$$(\gamma, \beta, \alpha) = \text{MLP}(c)$$

归一化后的特征 $h$ 按以下方式调制：

$$h' = \gamma \cdot h + \beta$$

最终输出通过 $\alpha$ 进行门控残差连接：

$$\text{output} = \alpha \cdot h' + \text{input}$$

与 DiT（Peebles & Xie, ICCV 2023）一致，最终调制尺度 $\alpha$ 采用**零初始化**策略，以稳定优化过程并支持更深的训练。这一设计使得条件信息能够灵活地注入每个 FCDM 块，而无需引入额外的交叉注意力模块。

### 3.2 倒置瓶颈与全局响应归一化（GRN）

FCDM 块采用 ConvNeXt 的**倒置瓶颈（Inverted Bottleneck）**结构：先通过 $1\times1$ 逐点卷积进行通道扩张，再进行 $7\times7$ 深度卷积，最后用 $1\times1$ 逐点卷积压缩回原通道数。这一设计在保持深度卷积计算量不变的前提下，为块内特征计算提供了更丰富的通道表示。

在通道特征增强方面，FCDM 使用**全局响应归一化（Global Response Normalization, GRN）**替代 DiCo（Cao et al., NeurIPS 2025）的跨通道注意力（CCA）。GRN 的核心操作完全由无参数运算构成：

1. **L2 归一化**：对每个通道的特征图计算全局 L2 范数，得到通道响应向量；
2. **响应归一化**：对通道响应进行归一化，抑制冗余通道、增强弱响应通道；
3. **校准**：将归一化后的响应作为通道权重，对原始特征进行重标定。

与 CCA 需要额外 $1\times1$ 卷积学习通道间激活不同，GRN 不引入任何可学习参数，在促进通道激活多样性的同时保持了模块的简洁性。此外，FCDM 不包含 DiCo 中的前馈模块（Feedforward Module），进一步简化了块结构。

### 3.3 U 形编解码架构

FCDM 的整体架构采用**可扩展的 U 形编解码器设计**，包含多个下采样和上采样阶段，并通过跳跃连接融合多尺度特征。每个阶段由若干 FCDM 块堆叠而成，块的分配策略支持灵活的非对称配置（消融实验验证了编解码器块数可独立调整）。输入潜变量经过编码器逐级压缩后，由解码器逐步恢复分辨率，最终输出预测噪声。

这种全卷积 U 形设计天然保留了卷积网络的局部归纳偏置，同时通过跳跃连接缓解了深层网络中的信息丢失问题，使得 FCDM 在参数效率上显著优于同参数量的 DiT 等 Transformer 架构。

### 补充图表

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/005_Figure_4.jpg]]
*Figure 4: Simple illustration of DiCo and FCDM block. Both architectures share a similar high-level structure, but FCDM adopts an inverted bottleneck that expands channels for richer representations while keeping the computational cost of depthwise convolution unchanged. DiCo employs CCA with an additional 1×1 convolution, whereas FCDM uses GRN, requiring no extra pointwise convolutions. FCDM also does not include DiCo’s feedforward module, resulting in a simpler and more efficient block*

## 实验与分析

### 瓶颈与核心洞察

当前扩散模型的主流骨干网络为Transformer（如 **DiT**，Peebles & Xie, ICCV 2023），其缩放性虽好，但计算量与资源需求巨大，严重限制了训练与推理效率。FCDM的核心洞察在于：**卷积网络固有的局部归纳偏置与参数效率，使其能够在更小的计算开销下学习有效的视觉表示**。通过复兴并重新设计ConvNeXt架构以整合条件注入、简化的U形设计和有效的通道增强机制（GRN），构建的全卷积扩散模型在计算效率、收敛速度和生成质量上均显著优于基于Transformer的DiT及其他同期的卷积扩散模型。

### 主要结果：效率与性能的显著突破

FCDM在所有模型尺度（S、B、L、XL）上均展现出对DiT的压倒性效率优势与更快的收敛速度。

**ImageNet 256×256 无指导生成（Table 3）：**
- **收敛速度**：FCDM-XL仅需1M训练步数即达到FID 7.91，而DiT-XL/2需7M步数才达到FID 9.62——FCDM以**约1/7的训练步数**实现了**1.71的FID绝对优势**。在400K步时，FCDM-XL的FID已达10.72，而DiT-XL/2在同等步数下FID高达19.72。
- **计算效率**：FCDM-XL仅有64.6 GFLOPs，约为DiT-XL/2（118.6 GFLOPs）的**54%**；吞吐量达到272.7 it/s，是DiT-XL/2（80.5 it/s）的**3.4倍**。
- **扩展性**：如图Figure 2所示，FCDM的扩展性曲线始终位于DiT的左下方（更低的FID与更少的FLOPs），证明卷积架构同样具备清晰的扩展性，且效率更优。

**ImageNet 256×256 有指导生成（Table 4）：**
- FCDM-XL在400个训练epoch下达到FID 2.03、IS 285.7，而DiT-XL/2需1400个epoch才达到FID 2.27——FCDM以**更少的训练量实现了更优的生成质量**。在训练成本与吞吐量的Pareto前沿上（Figure 6），FCDM同样占据优势位置。

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/010_Figure_6.jpg]]
*Figure 6: Benchmarking class-conditional image generation performance and efficiency on ImageNet 256×256. Left: FID versus total training cost. Right: FID versus throughput. One zettaFLOP corresponds to*

**ImageNet 512×512 高分辨率生成（Table 5）：**
- FCDM-XL仅用1M步即达到FID 7.46，显著优于DiT-XL/2在3M步下的FID 12.03（**FID降低4.57**），同时吞吐量达129.6 it/s，远超DiT-XL/2的30.7 it/s。

**与同期卷积扩散模型的对比（Table 2, Table 16, Table 17）：**
- FCDM的FLOPs约为 **DiCo**（Cao et al., NeurIPS 2025）的75%，且在FID指标上同样具有竞争力。与 **DiC**（Wang et al., CVPR 2025）相比，FCDM在吞吐量上优势明显。

### 消融实验：设计选择的关键性

消融实验（Table 6，基于FCDM-L，200K训练步）系统验证了各设计组件的贡献：

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/013_Table_6.jpg]]
*Table 6: Ablation study on FCDM design choices. We analyze the effects of kernel size, GRN, DiCo [1] design choices, and the FCDM block. Training iterations are fixed to 200K. ∗ indicates that C is adjusted to match FLOPs to ensure a fair comparison*

| 消融项 | FID (↓) | 关键结论 |
|--------|---------|----------|
| FCDM-L (完整模型) | 19.97 | 基线 |
| 移除GRN | 23.85 | GRN对通道多样性的增强至关重要 |
| 用CCA替换GRN | 23.85 | GRN无额外参数即可达到与CCA相当的效果 |
| 移除倒置瓶颈 | 31.14 | 倒置瓶颈是性能的核心支撑 |
| 替换为ResNet块 | 31.14 | ConvNeXt的现代化设计不可替代 |
| 深度卷积核3×3 | 22.73 | 大核（7×7）对感受野扩展至关重要 |
| 深度卷积核5×5 | 21.07 | 核尺寸减小持续损害性能 |

**GRN的有效性（Figure 7）：** 特征激活可视化显示，GRN层前后的通道激活模式发生显著变化——GRN明显减少了通道冗余，验证了其在增强通道多样性方面的作用。

**深度卷积 vs 局部自注意力（Table 13）：** 将7×7深度卷积替换为邻域注意力（Neighborhood Attention, 7×7窗口）后，FID从19.97升至29.81，吞吐量从381.3 it/s降至122.8 it/s——**全卷积设计在效率与质量上均优于局部自注意力**。

**大核尺寸的进一步探索（Table 10）：** 7×7为最佳核尺寸；减小至5×5或3×3导致FID升高，过度增大至9×9或11×11同样带来性能下降。

**跨潜空间编码器的适应性（Table 11）：** 在SD-VAE和EQ-VAE两种不同潜空间下，FCDM始终优于DiT，表明架构具有广泛的适应性。

**流匹配目标下的扩展性（Table 9）：** FCDM在流匹配（Flow-Matching）训练目标下同样展现出清晰的扩展性，在小尺度（S）上甚至表现更优。

### 失败模式与局限性

1. **生成质量尚未触及SOTA天花板**：尽管FCDM在计算效率上表现优异，但其最终生成质量（如FID 2.03 @ 256×256）尚未超过当前最先进的扩散模型（如EDM-2）或配合更高级训练框架所能达到的水平。
2. **条件类型受限**：目前主要针对类条件和简单的文本条件生成进行验证，尚未扩展至更大规模的多模态或复杂数据集。论文指出，如何将FCDM扩展以支持联合全文本嵌入（如MMDiT）仍是一个重要方向。
3. **频域优势缺乏理论深化**：Figure 8显示FCDM在扩散全过程预测噪声的频谱能量持续高于DiT，暗示其在保持高频信息方面的潜力，但该现象缺乏进一步的理论分析。

### 公平性说明

所有模型采用相同的DiT训练与评估框架，统一使用AdamW优化器（学习率 $1 \times 10^{-4}$）、水平翻转增强、EMA衰减和DDPM噪声调度（线性方差 $1 \times 10^{-4}$ 至 $2 \times 10^{-2}$），参数数量对齐以确保公平比较。FCDM的FLOPs远低于DiT，在同等参数数量下计算效率更高。

### 补充图表

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/002_Table_1.jpg]]
*Table 1: FCDM consistently yields lower FLOPs, higher throughput, and converges faster to superior performance compared to DiT across all scales*

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/003_Figure_2.jpg]]
*Figure 2: Is scalability exclusive to transformers? Our Fully Convolutional Diffusion Model (FCDM) exhibits clear scalability: it is more efficient and achieves better convergence than Diffusion Transformers (DiTs). Bubble size indicates the FLOPs of each diffusion model. Across all scales (ordered by parameter count)*

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/008_Table_3.jpg]]
*Table 3: Scalability comparisons on ImageNet 256×256. For each model scale, we report FID, IS, Precision, and Recall (50K samples without guidance), and efficiency metrics (training iterations, FLOPs, throughput). FCDM-XL achieves superior convergence while using 50% fewer FLOPs than DiT-XL/2. The best results are highlighted in bold. Evaluated methods operate in the latent space*

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/009_Table_4.jpg]]
*Table 4: Benchmarking class-conditional image generation on ImageNet 256×256. We compare representative models in terms of FID, IS, Precision, Recall (with guidance), and efficiency metrics (training epochs, FLOPs, throughput). FCDM-XL achieves competitive performance with superior efficiency. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/011_Table_5.jpg]]
*Table 5: Benchmarking class-conditional image generation on ImageNet 512×512. We report FID, IS, Precision, Recall (without guidance), and efficiency metrics for representative models. Even at this resolution, FCDM surpasses models trained for 3M iterations with only 1M iterations and achieves the best efficiency in FLOPs and throughput. The best results are highlighted in bold*

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/012_Figure_7.jpg]]
*Figure 7: Feature activation visualization. We visualize features before and after the GRN layer during sampling for each image on the left. The first 64 channels of the last block in the first stage are shown as 8×8 grids. GRN clearly reduces channel redundancy*

![[assets/figures/papers/paper_list_l927_https_arxiv_org_abs_2603_09408/figures/017_Figure_8.jpg]]
*Figure 8: Spectral energy of predicted noise across diffusion steps. FCDM consistently exhibits higher spectral energy than DiT across the entire diffusion process, suggesting potential for better preservation of high-frequency components*

## 方法谱系与知识库定位

### 1. 与基线方法的关系与边界

**FCDM** 的核心定位是在扩散模型骨干网络领域，以全卷积架构替代当前主流的 Transformer 架构，从而在计算效率、收敛速度和生成质量之间取得更优的帕累托前沿。其设计直接对标并系统性地改进了以下三类基线方法：

- **DiT**（Peebles & Xie, ICCV 2023）：当前扩散模型的事实标准骨干网络，采用纯 Transformer 架构。FCDM 在所有尺度（S/B/L/XL）上均以约 **50% 的 FLOPs** 和 **3.4× 的吞吐量** 超越 DiT，同时仅需 **1/7 的训练步数** 即可达到更优的 FID（Table 1, Table 3）。这一对比直接挑战了“扩散模型的可扩展性为 Transformer 所独有”的假设（Figure 2）。

- **DiCo**（Cao et al., NeurIPS 2025）：同期最先进的卷积扩散模型。FCDM 在架构层面做出了关键差异化设计：用 **GRN（全局响应归一化）** 替代 DiCo 的 **CCA（通道交叉注意力）**，消除了额外的 1×1 卷积参数开销；采用 **倒置瓶颈** 结构替代 DiCo 的无通道扩张设计，在深度卷积计算量不变的前提下实现更丰富的通道表示；同时 **移除了 DiCo 的前馈模块**，使整体架构更简洁高效。消融实验表明，GRN 相比 CCA 将 FID 从 23.85 降至 19.97（Table 6），且 FLOPs 仅约为 DiCo 的 75%（Table 2）。

- **DiC**（Wang et al., CVPR 2025）：另一卷积扩散模型，在吞吐量对比中作为参照。FCDM 在同等参数规模下展现出显著的吞吐量优势。

**适用边界**：FCDM 目前验证的主要场景是类条件图像生成（ImageNet 256×256 和 512×512）以及简单的文本条件生成。其设计假设条件信号可通过 AdaLN 的调制参数（γ, β, α）有效注入，对于需要复杂交叉注意力的多模态条件（如密集文本描述）尚未充分验证。

### 2. 在知识库中的定位与贡献

FCDM 的方法贡献可定位于以下三条技术脉络的交汇点：

1. **卷积架构复兴脉络**：继承 ConvNeXt 的现代化卷积设计理念（倒置瓶颈、大核深度卷积、归一化层选择），将其从判别式视觉任务迁移至生成式扩散建模。FCDM 证明了卷积网络的局部归纳偏置在扩散生成任务中依然具有竞争力，且参数效率显著优于 Transformer。

2. **扩散模型骨干网络演进脉络**：从 U-Net 到 DiT 的骨干网络变迁中，FCDM 提供了一条“卷积替代路径”。其 U 形编解码器设计保留了多尺度特征学习的优势，同时通过 AdaLN 实现了与 DiT 同等的条件注入能力。Table 12 的等构架构消融进一步表明，即使在不使用 U 形结构的情况下，FCDM 的纯卷积块仍优于 DiT。

3. **通道增强机制脉络**：GRN 层的引入为通道多样性增强提供了一种无参数方案。Figure 7 的特征可视化直接证实了 GRN 能有效减少通道冗余，这一机制在扩散模型的采样过程中尤为重要——高频信息的保留依赖于通道的差异化激活（Figure 8 的频域能量分析提供了佐证）。

### 3. 局限与开放问题

**已知局限**：

- **生成质量天花板**：尽管 FCDM 在效率上大幅领先，其最终生成质量尚未超过配合高级训练框架（如 EDM-2）或流匹配目标的最先进扩散模型。Table 9 表明 FCDM 在流匹配下同样展现扩展性，但未报告与 SOTA 的直接对比。
- **条件类型受限**：当前主要验证类条件和简单文本条件，尚未扩展至联合全文本嵌入（如 MMDiT）以学习更丰富的多模态表示。
- **分辨率泛化**：512×512 实验（Table 5）虽已展示优势，但更高分辨率下的卷积网络效率优势是否持续，缺乏实验支撑。

**开放问题**：

- **频域优势的理论解释**：Figure 8 显示 FCDM 在整个扩散过程中预测噪声的频谱能量始终高于 DiT，暗示卷积网络在保持高频信息方面具有内在优势。这一现象缺乏严格的理论分析，理解其成因可能为扩散模型骨干设计提供新的指导原则。
- **与全文本嵌入的融合**：如何将 FCDM 的卷积骨干与联合全文本嵌入机制（如 MMDiT）结合，是扩展至复杂文本到图像生成任务的关键方向。
- **更大规模下的行为**：当前最大模型为 698.8M 参数的 FCDM-XL，在十亿参数规模下卷积网络的训练稳定性和扩展规律是否仍优于 Transformer，有待验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Reviving_ConvNeXt_for_Efficient_Convolutional_Diffusion_Models.pdf]]