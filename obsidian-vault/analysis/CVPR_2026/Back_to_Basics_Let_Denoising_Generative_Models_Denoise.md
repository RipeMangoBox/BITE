---
title: "Back to Basics: Let Denoising Generative Models Denoise"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Back_to_Basics_Let_Denoising_Generative_Models_Denoise.pdf
aliases:
- JJIT
- BBLDGMD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 网络直接预测干净图像（x-prediction）而非噪声或速度，使网络只需关注低维流形信息，从而摆脱高维信息瓶颈。
primary_logic: 基于流形假设，让扩散模型回归“去噪”本意——直接预测干净数据，可使普通ViT在大块高维像素上有效生成，无需额外的潜在空间、预训练或辅助损失。
claims:
- 在ImageNet 256×256（每patch 768维）上仅x-prediction成功，ϵ/v-prediction的FID超过96，完全失败。
- 高维玩具实验（d=2嵌入D=512）中只有x-prediction能生成合理数据，ϵ/v-prediction在模型欠完备时崩溃。
- 调整噪声水平虽然能提升x-prediction，但不能挽救ϵ/v-prediction，说明根本症结在于高维信息传播而非噪声调度。
- ImageNet 256×256 上 FID-50K ↓ = 1.82 (JiT-G/16)
---

# Back to Basics: Let Denoising Generative Models Denoise

> [!tip] 核心洞察
> 基于流形假设，让扩散模型回归“去噪”本意——直接预测干净数据，可使普通ViT在大块高维像素上有效生成，无需额外的潜在空间、预训练或辅助损失。

| 字段 | 内容 |
|------|------|
| 中文题名 | 返璞归真：让去噪生成模型去噪 |
| 英文题名 | Back to Basics: Let Denoising Generative Models Denoise |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.13720) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | JiT (Just image Transformers) |
| Dataset | ImageNet 256×256, ImageNet 512×512 |

> [!tip] 效果简介
> - ImageNet 256×256 上，FID-50K ↓ 1.82 (JiT-G/16) vs 2.27 (DiT-XL/2) (-0.45)。
> - ImageNet 512×512 上，FID-50K ↓ 1.78 (JiT-G/32) vs various models (see Table 8) (competitive)。

## 概述

本文直面扩散模型在高维像素空间中生成质量灾难性下降的根本瓶颈：基于流形假设，干净图像仅占据高维空间中的低维流形，而噪声（ϵ）或流速度（v）则分布在高维空间中。当网络被迫预测ϵ或v时，容量有限的模型必须保留完整的高维信息，导致生成失败。本文的核心洞见是**让扩散模型回归“去噪”本意——直接预测干净图像（x-prediction）**，使网络只需关注低维流形信息，从而摆脱高维信息瓶颈。

基于这一原理，本文提出**JiT（Just image Transformers）**，一种自包含的纯ViT架构，直接作用于原始像素块，无需VAE tokenizer、预训练模型或辅助损失。JiT采用低秩瓶颈嵌入压缩高维像素块，结合adaLN-Zero条件机制、SwiGLU激活、RoPE位置编码等现代Transformer设计，通过x-prediction预测干净图像，再转换为流速度进行流匹配训练，最终以ODE求解器（50步Heun）完成采样。

实验表明，在ImageNet 256×256上，高维patch（768维）条件下仅x-prediction有效，ϵ/v-prediction的FID超过96，完全失败（Table 2a）；而低维patch（48维）下所有预测目标均可行。噪声水平调整虽能改善x-prediction，但无法挽救ϵ/v-prediction，证实根源在于信息容量而非噪声调度（Table 3）。JiT-G/16在ImageNet 256×256上取得FID 1.82，优于DiT-XL/2（2.27）等潜在扩散模型（Table 7）；在512×512分辨率上同样具备竞争力（FID 1.78，Table 8），且计算量随序列长度线性增长，避免了多尺度方法的二次开销。

该方法将扩散生成简化为“ViT + x-prediction”的自包含范式，揭示了预测目标选择对高维生成的决定性作用，为未来生成模型的设计提供了新的方法论视角。

## 背景与动机

### 扩散模型的预测范式

扩散模型和流匹配模型已成为视觉生成的主流方法。这类模型的核心思想是：将数据逐渐加噪至纯噪声，再学习一个神经网络来逆转这一过程。形式上，给定干净图像 $\mathbf{x}$ 和噪声 $\mathbf{\epsilon}$，噪声样本通过线性插值构造：

$$z_t = t \mathbf{x} + (1-t) \mathbf{\epsilon}$$

其中 $t \in [0,1]$，当 $t=1$ 时为纯数据，$t=0$ 时为纯噪声。流速度定义为数据与噪声之差：

$$\mathbf{v} = \mathbf{x} - \mathbf{\epsilon}$$

网络通过最小化预测速度与真实速度的均方误差来训练：

$$\mathcal{L} = \mathbb{E}_{t,\mathbf{x},\mathbf{\epsilon}} \| \mathbf{v}_{\theta}(\mathbf{z}_t, t) - \mathbf{v} \|^2$$

训练完成后，从随机噪声出发，通过求解确定性ODE $dz_t / dt = \mathbf{v}_{\theta}(\mathbf{z}_t, t)$ 逐步生成数据。

在这一框架下，网络可以预测不同的目标：噪声 $\mathbf{\epsilon}$（**ϵ-prediction**）、速度 $\mathbf{v}$（**v-prediction**），或直接预测干净图像 $\mathbf{x}$（**x-prediction**）。损失空间与网络输出空间不必相同——网络输出可以通过简单变换转换到损失空间计算损失。**Table 1** 列举了所有9种可能的组合。

### 主流实践的路径依赖

当前主流的扩散模型几乎都采用 **ϵ-prediction** 或 **v-prediction**。这一选择并非偶然：早期扩散模型（如DDPM）在像素空间使用U-Net架构预测噪声，取得了良好效果。随后，潜在扩散模型（如Stable Diffusion）将这一范式迁移到VAE压缩的潜在空间，进一步提升了效率。代表性工作包括：

- **DiT**（Peebles & Xie, ICCV 2023）：基于Transformer的潜在扩散模型，使用v-prediction，在ImageNet 256×256上取得FID 2.27。
- **SiT**（Ma et al., ECCV 2024）：基于流的可扩展插值Transformer，延续了v-prediction范式。
- **RAE**（Zheng et al., 2025）：使用表征自编码器预训练的扩散Transformer，依赖外部预训练来提升像素空间生成质量。

这些方法的共同特征是：**网络预测的是噪声或速度等“非数据”量**，且通常需要VAE tokenizer将图像压缩到低维潜在空间才能有效工作。

### 被忽视的根本瓶颈

本文揭示了一个被长期忽视的关键问题：**在高维像素空间中，预测噪声或速度存在根本性困难**。

这一困难的根源在于**流形假设**（Manifold Assumption, **Figure 1**）：自然图像虽然存在于高维像素空间（如256×256×3≈197K维），但真实图像仅占据其中的一个极低维流形。干净图像 $\mathbf{x}$ 位于流形之上，而噪声 $\mathbf{\epsilon}$ 和速度 $\mathbf{v} = \mathbf{x} - \mathbf{\epsilon}$ 则天然地“脱离流形”（off-manifold），分布在整个高维空间中。

当网络被要求预测 $\mathbf{\epsilon}$ 或 $\mathbf{v}$ 时，它必须保留完整的高维信息来表征这些遍布全空间的量。然而，网络容量是有限的——在模型“欠完备”（undercomplete）的情况下，它被迫在高维空间中处理大量冗余信息，导致生成质量的灾难性下降。

### 高维玩具实验的启示

为验证这一假设，作者设计了一个简洁的玩具实验（**Figure 2**）：将 $d=2$ 维的真实数据通过随机正交投影矩阵“埋入”$D$ 维空间（$D \gg d$），训练一个5层ReLU MLP（256维隐藏单元）来学习生成。结果显示：

- 当 $D$ 较小时，$\mathbf{\epsilon}$-、$\mathbf{v}$- 和 $\mathbf{x}$-prediction 均能生成合理数据。
- 随着 $D$ 增大（模型相对于数据维度变得“欠完备”），仅 **x-prediction** 能持续生成合理结果，而 $\mathbf{\epsilon}$- 和 $\mathbf{v}$-prediction 完全崩溃。

这一实验清晰地表明：**预测目标的选择并非无关紧要的工程细节，而是在高维设定下决定成败的核心因素**。

### 本文动机：返璞归真

基于上述洞察，本文提出一个朴素而根本的方案：**让去噪生成模型回归“去噪”本意——直接预测干净图像（x-prediction）**。

直觉上，由于干净图像天然位于低维流形上，x-prediction 让网络只需关注流形信息，从而摆脱高维信息瓶颈。这使得一个简单的纯ViT架构（**JiT**, Just image Transformers）直接作用于原始像素大块（如16×16像素，每块768维），无需VAE tokenizer、无需潜在空间、无需预训练或辅助损失，即可在高维像素空间有效生成。

核心主张可概括为三点：
1. **预测目标是关键旋钮**：在高维设定下，x-prediction 是唯一可行的选择。
2. **架构可以极简**：纯ViT + 低秩瓶颈嵌入即可胜任，无需复杂的多尺度U-Net或潜在空间映射。
3. **流形假设是理论根基**：这一设计选择有深刻的几何直觉支撑，而非经验性的技巧堆砌。

## 核心创新

### 1. 预测目标的根本转变：从噪声/速度回归到干净图像直接预测

现有扩散模型（包括基于流的模型）的通用范式是让网络预测噪声 **ϵ** 或流速度 **v**，然后通过迭代去噪间接恢复干净图像。本工作的核心创新在于**回归扩散模型的“去噪”本意**——让网络直接预测干净图像 **x**（x-prediction），从而从根本上改变了生成模型在高维像素空间中的信息处理方式。

这一转变的动机源于**流形假设**（Manifold Assumption，Figure 1）：自然图像位于高维像素空间中的一个低维流形上，而噪声 ϵ 和流速度 v = x − ϵ 天然处于流形之外，分布在整个高维空间中。当网络被要求预测 ϵ 或 v 时，它必须保留完整的高维信息以精确刻画这些“离流形”的量；而直接预测 x 则允许网络**仅关注低维流形信息**，将容量集中在真正有意义的数据结构上。

**决定性证据**来自 Table 2(a) 的消融实验：在 ImageNet 256×256 上使用 JiT-B/16（每 patch 768 维），所有以 x-prediction 为核心的组合均能正常工作（FID 8.62），而 ϵ-prediction 和 v-prediction 的 FID 分别高达 379–395 和 97–127，呈现灾难性失败。当 patch 维度降至 48 维（ImageNet 64×64，Table 2(b)）时，三种预测目标均能有效生成，这直接证明**预测目标的选择对高维数据至关重要**，且症结在于信息维度而非模型容量。

进一步，Table 3 的噪声水平位移实验表明：适当调整噪声调度可以改善 x-prediction（FID 从 14.44 降至 8.62），但完全无法挽救 ϵ-/v-prediction 的失败（ϵ-prediction 最低仍为 355.25），排除了“噪声调度不当”作为替代解释的可能。

### 2. 架构简化：纯 ViT 直接作用于原始像素块

与主流方法依赖 VAE tokenizer 将图像压缩到潜在空间（如 **DiT-XL/2**，Peebles & Xie, ICCV 2023）或使用 U-Net 卷积骨干不同，JiT 采用**纯 Vision Transformer（ViT）直接作用于原始像素块**（Figure 3），无需任何潜在空间映射或预训练编码器。这一设计使得整个生成管线完全自包含，消除了对外部预训练模型（如 VAE、分类器、自监督特征提取器）的依赖。

架构的核心组件包括：
- **图像分块**：将输入图像划分为大尺寸块（如 16×16 像素），形成固定长度的 token 序列（16×16 = 256 tokens），使计算量与序列长度线性相关，避免了多尺度方法中分辨率翻倍时计算量二次增长的问题。
- **条件注入**：采用 adaLN-Zero 机制同时注入时间步 t 和类别标签条件。
- **高级 Transformer 设计**（Table 4）：集成 SwiGLU 激活、RMSNorm、RoPE 位置编码、qk-norm 等通用改进，逐步累积带来约 1.2 FID 的提升。

### 3. 低秩瓶颈嵌入：显式利用流形低维特性

在标准的 ViT 中，patch 嵌入通常使用全秩线性层，隐藏维度不低于 patch 维度（如 768→768）。JiT 将线性嵌入层替换为**低秩瓶颈结构**：先将 768 维 patch 投影到远低于原始维度的瓶颈空间（d′），再扩展回 Transformer 的隐藏维度。

Figure 4 的实验表明，在较宽的瓶颈范围（32–512 维）内，瓶颈设计可带来最高约 1.3 FID 的提升；即使在极端瓶颈（16 维）下模型仍能生成合理图像。这一结果与流形假设高度一致：瓶颈层强制网络在低维空间中操作，抑制了高维冗余信息的传播，使模型更专注于学习数据流形的本质结构。

### 4. 损失空间的统一与速度转换

尽管网络输出为干净图像 **x_θ**，JiT 并未直接使用 x-loss，而是将预测结果转换为流速度后计算 v-loss：

$$\mathbf{v}_{\theta}(\mathbf{z}_t, t) = (\mathbf{x}_{\theta} - \mathbf{z}_t) / (1-t)$$

$$\mathcal{L} = \mathbb{E}_{t,\mathbf{x},\boldsymbol{\epsilon}} \| \mathbf{v}_{\theta}(\mathbf{z}_t, t) - \mathbf{v} \|^2$$

这一设计利用了 v-loss 的自然重加权特性（等价于带权重 $1/(1-t)^2$ 的 x-loss），在训练过程中自动强调高噪声阶段的信号，同时保持了 x-prediction 的低维信息优势。Table 10 进一步表明，EDM 预条件器或线性预条件器在 x-prediction 下反而导致质量严重下降，说明**避免信息混合、保持预测目标的纯粹性**对高维生成更为关键。

### 与基线方法的 changed slots 总结

| 设计维度 | 基线方法 | JiT 方法 | 证据锚点 |
|---------|---------|---------|---------|
| **预测目标** | ϵ-prediction 或 v-prediction | x-prediction（直接预测干净图像） | Table 2(a); Figure 2 |
| **网络架构** | U-Net 卷积或潜在空间 DiT | 纯 ViT 直接作用于原始像素块 | Figure 3; Section 4.1 |
| **块嵌入策略** | 全秩线性嵌入（d_hidden ≥ d_patch） | 低秩瓶颈嵌入（可降至 16 维） | Figure 4 |
| **外部依赖** | 依赖 VAE tokenizer 或预训练模型 | 完全自包含，无任何外部预训练 | Table 7 公平性说明 |

这些创新共同构成了一个**极简但高效的生成范式**：通过回归“去噪”本意（x-prediction）并配合低秩瓶颈设计，使普通 ViT 能够在大块高维像素上有效生成，无需潜在空间、预训练或辅助损失，在 ImageNet 256×256 上以 JiT-G/16 取得 FID 1.82，优于 DiT-XL/2 的 2.27（Table 7）。

## 整体框架

JiT（Just image Transformers）的整体设计遵循一个核心原则：**让扩散模型回归“去噪”本意**，即网络直接预测干净图像（x-prediction），而非噪声或速度。基于流形假设——自然图像仅占据高维像素空间中的一个低维流形——该方法使网络只需关注低维流形上的信息，从而摆脱高维信息瓶颈的束缚。

### Pipeline 总览

JiT 的生成 pipeline 由五个核心模块串联而成，形成从原始像素到生成图像的端到端流程：

1. **图像分块与低秩瓶颈嵌入**：将输入图像划分为大块（如 16×16 像素的 patch），通过低秩线性层嵌入至 Transformer 维度。该瓶颈设计允许嵌入维度远低于 patch 的原始维度（甚至降至 16 维），以主动丢弃高维空间中的冗余信息，使网络更专注于流形上的有效特征。

2. **Transformer 编码器**：采用标准 ViT 架构处理 patch token 序列，集成 adaLN-Zero 时间/类别条件注入、SwiGLU 激活函数、RMSNorm 归一化、RoPE 位置编码以及 qk-norm 等通用高级组件。所有 token 在 Transformer 层中通过自注意力进行全局交互，序列长度始终保持为 patch 数量（如 16×16 tokens），不随分辨率变化而改变。

3. **x 预测头**：每个 token 经线性层映射回对应的干净图像块 $\mathbf{x}_\theta$。这是网络的核心输出——直接对干净数据的估计，而非对噪声 $\epsilon$ 或速度 $\mathbf{v}$ 的预测。

4. **速度转换与 v-loss 计算**：将预测的干净图像 $\mathbf{x}_\theta$ 转换为预测速度 $\mathbf{v}_\theta$：
   $$\mathbf{v}_\theta(\mathbf{z}_t, t) = (\mathbf{x}_\theta - \mathbf{z}_t) / (1 - t)$$
   随后与真实速度 $\mathbf{v} = \mathbf{x} - \epsilon$ 计算 L2 损失：
   $$\mathcal{L} = \mathbb{E}_{t,\mathbf{x},\epsilon} \| \mathbf{v}_\theta(\mathbf{z}_t, t) - \mathbf{v} \|^2$$
   该损失等价于重加权的 x-loss：$\mathcal{L} = \mathbb{E} \frac{1}{(1-t)^2} \| \mathbf{x}_\theta - \mathbf{x} \|^2$。选择在速度空间计算损失（而非直接使用 x-loss）是因为 v-loss 在实践中提供了更稳定的训练动态。

5. **ODE 求解器采样**：从随机噪声 $\mathbf{z}_0 = \epsilon$ 开始，通过求解确定性 ODE $d\mathbf{z}_t / dt = \mathbf{v}_\theta(\mathbf{z}_t, t)$ 逐步生成图像。采样采用 50 步 Heun 求解器，将噪声沿流轨迹逐步推向干净数据 $\mathbf{x} = \mathbf{z}_1$。

### 关键设计决策

**预测目标的选择**是 JiT 区别于主流扩散模型（如 DiT、SiT）的根本差异点。传统方法预测噪声（ϵ-prediction）或速度（v-prediction），要求网络在高维像素空间中保留完整信息；而 JiT 的 x-prediction 使网络输出直接锚定在低维数据流形上。这一选择在高维 patch（如 768 维）场景下是决定性的：Table 2(a) 显示，在 ImageNet 256×256 上，ϵ-prediction 和 v-prediction 的 FID 分别高达 379.21 和 96.53，完全失败；而 x-prediction 的 FID 仅为 8.62。

**低秩瓶颈嵌入**进一步强化了这一设计哲学。Figure 4 的消融表明，将 patch 嵌入维度从全秩 768 维压缩至 32~512 维的瓶颈，可提升 FID 约 1.3；即使极端压缩至 16 维，模型仍能生成合理图像。这印证了流形假设——高维像素空间中绝大部分维度是冗余的，瓶颈设计主动丢弃这些信息，反而帮助网络聚焦于流形上的本质结构。

**纯 ViT 架构**使 JiT 无需依赖 VAE tokenizer 或潜在空间，直接在原始像素块上操作。计算量与序列长度（patch 数量）线性相关，避免了多尺度方法中分辨率翻倍时的二次增长，使得跨分辨率扩展（256→512→1024）自然高效。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/004_Figure_3.jpg]]
*Figure 3: The “Just image Transformer” (JiT) architecture: simply a plain ViT [13] on patches of pixels for x-prediction*

## 核心模块与公式推导

### 预测空间与损失空间的解耦

扩散生成模型可在三种空间之一定义其损失与网络输出：干净数据空间 **x**、噪声空间 **ϵ**、或流速度空间 **v**。关键洞察在于，损失空间与网络输出空间不必相同——网络可直接预测一种量，再通过插值关系转换为损失所需的另一种量（Table 1 展示了全部 9 种组合）。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/002_Table_1.jpg]]
*Table 1: All possible combinations of defining the loss and network prediction in x, v, or ϵ spaces. The direct network outputs are highlighted in colors. For any off-diagonal entry where the network output space differs from the loss space, a transformation on the network output is applied*

这一解耦的核心是线性插值过程。给定干净图像 $\mathbf{x}$ 与高斯噪声 $\mathbf{\epsilon}$，噪声样本 $\mathbf{z}_t$ 定义为：

$$\mathbf{z}_t = t \mathbf{x} + (1-t) \mathbf{\epsilon}$$

其中 $t \in [0,1]$ 是时间参数：$t=1$ 时 $\mathbf{z}_1 = \mathbf{x}$（纯数据），$t=0$ 时 $\mathbf{z}_0 = \mathbf{\epsilon}$（纯噪声）。流速度 $\mathbf{v}$ 定义为数据与噪声之差，亦等于 $\mathbf{z}_t$ 对 $t$ 的导数：

$$\mathbf{v} = \mathbf{x} - \mathbf{\epsilon} = \frac{d\mathbf{z}_t}{dt}$$

当网络输出 $\mathbf{x}_\theta$、$\mathbf{\epsilon}_\theta$ 或 $\mathbf{v}_\theta$ 中的任意一个时，其余两个可通过式 (1)(2) 互相推导。以 **x-prediction** 为例，网络直接输出 $\mathbf{x}_\theta = \text{net}_\theta(\mathbf{z}_t, t)$，则对应的噪声估计与速度估计为：

$$\mathbf{\epsilon}_\theta = \frac{\mathbf{z}_t - t \mathbf{x}_\theta}{1-t}, \quad \mathbf{v}_\theta = \frac{\mathbf{x}_\theta - \mathbf{z}_t}{1-t}$$

### 流匹配损失与 x-prediction 的等价性

JiT 采用 **v-loss**（流匹配损失）作为训练目标。该损失在速度空间中定义为预测速度 $\mathbf{v}_\theta$ 与真实速度 $\mathbf{v}$ 的均方误差：

$$\mathcal{L} = \mathbb{E}_{t,\mathbf{x},\mathbf{\epsilon}} \| \mathbf{v}_\theta(\mathbf{z}_t, t) - \mathbf{v} \|^2$$

将 x-prediction 下的 $\mathbf{v}_\theta$ 表达式代入，v-loss 可重写为带时间权重的 x-loss 形式：

$$\mathcal{L} = \mathbb{E} \frac{1}{(1-t)^2} \| \mathbf{x}_\theta(\mathbf{z}_t, t) - \mathbf{x} \|^2$$

这表明 x-prediction + v-loss 的组合等价于一个自适应加权的去噪自编码器——在 $t$ 接近 1（低噪声）时权重极大，迫使网络在高信噪比区域精确重建干净图像。这一推导来自 Section 3.2，是 JiT 方法有效性的理论基石。

### 确定性采样 ODE

训练完成后，生成过程通过求解以下常微分方程完成：

$$\frac{d\mathbf{z}_t}{dt} = \mathbf{v}_\theta(\mathbf{z}_t, t)$$

从 $t=0$（纯噪声 $\mathbf{z}_0 = \mathbf{\epsilon}$）积分至 $t=1$（生成图像 $\mathbf{z}_1 = \mathbf{x}$）。JiT 采用 50 步 Heun 二阶求解器完成采样，无需随机噪声注入。

### 核心流水线模块

JiT 的完整生成流水线由以下模块串联构成：

1. **图像分块与低秩瓶颈嵌入**：将输入图像划分为大块（如 $16 \times 16$ 像素，每块 768 维），通过两级线性层嵌入至 Transformer 维度。第一级将 768 维压缩至瓶颈维度 $d'$（如 128 维），第二级扩展至隐藏维度。这一低秩设计符合流形假设——自然图像仅占据高维像素空间中的低维流形，瓶颈迫使网络丢弃冗余信息。消融实验（Figure 4）表明，$d'$ 在 32 至 512 范围内均可提升 FID 约 1.3，即使极端瓶颈（16 维）仍能生成合理图像。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/007_Figure_4.jpg]]
*Figure 4: Bottleneck linear embedding. Results are for JiT-B/16 on ImageNet 256×256. A raw patch is 768-dim (16×16×3) and is embedded by two sequential linear layers with an intermediate bottleneck dimension d′*

2. **Transformer 编码器**：标准 ViT 架构，集成 adaLN-Zero 时间/类别条件注入、SwiGLU 激活函数、RMSNorm 归一化、RoPE 位置编码及 qk-norm 注意力归一化。所有 JiT 模型保持相同的序列长度（$16 \times 16$ tokens），使计算量与分辨率解耦。

3. **x 预测头**：线性层将每个 token 映射回干净图像块 $\mathbf{x}_\theta$。

4. **速度转换与 v-loss 计算**：由 $\mathbf{x}_\theta$ 通过式 (6) 转换为 $\mathbf{v}_\theta$，与真实速度 $\mathbf{v}$ 计算 L2 损失。

5. **ODE 求解器采样**：从随机噪声出发，通过 50 步 Heun 方法求解 $d\mathbf{z}_t/dt = \mathbf{v}_\theta$ 生成最终图像。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/001_Figure_1.jpg]]
*Figure 1: The Manifold Assumption [4] hypothesizes that natural images lie on a low-dimensional manifold within the highdimensional pixel space. While a clean image x can be modeled as on-manifold, the noise ϵ or flow velocity v (e.g., v = x − ϵ) is inherently off-manifold. Training a neural network to predict a clean image (i.e., x-prediction) is fundamentally different from training it to predict noise or a noised quantity (i.e., ϵ/v-prediction)*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/003_Figure_2.jpg]]
*Figure 2: Toy Experiment: d-dimensional (d = 2) underlying data is “buried” in a D-dimensional space, by a fixed, random, column-orthogonal projection matrix. In the D-dim space, we train a simple generative model (5-layer ReLU MLP with 256-dim hidden units). The projection matrix is unknown to the model, and we only use it for visualizing the output. In this toy experiment, with the observed dimension D increasing, only x-prediction can produce reasonable results*

## 实验与分析

### 核心发现：预测目标决定高维生成的成败

实验的核心结论是：**在高维像素空间中，只有直接预测干净图像（x-prediction）才能使扩散模型有效生成，而传统的噪声预测（ϵ-prediction）和速度预测（v-prediction）会灾难性失败**。

Table 2 展示了这一关键消融实验。在 ImageNet 256×256 上使用 JiT-B/16（每 patch 768 维），x-prediction 结合 v-loss 取得 FID-50K 为 8.62；而 ϵ-prediction 的 FID 高达 379.21–394.58，v-prediction 为 96.53–126.88，完全无法生成合理图像。作为对比，在 ImageNet 64×64 上使用 JiT-B/4（每 patch 仅 48 维），三种预测目标均表现良好（FID 在 3.46–3.63 之间）。这一对比直接揭示：**问题症结在于高维信息传播，而非预测目标本身**。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/005_Table_2.jpg]]
*Table 2: Results of all combinations of loss space and network space (see Tab. 1), evaluated by FID-50K on ImageNet: (a) JiT-B/16 at 256 resolution, 768-d per patch; (b) JiT-B/4 at 64 resolution, 48-d per patch. We annotate catastrophic failures in red and reasonable results by green. Settings: 200 epochs, with CFG [22]*

玩具实验（Figure 2）进一步验证了这一机制：将 d=2 的低维数据嵌入 D 维空间，当 D 增大至 512 时，只有 x-prediction 能生成合理数据，ϵ/v-prediction 在模型欠完备时崩溃。这符合流形假设——干净数据位于低维流形上，而噪声和速度分布在高维空间中，要求网络保留完整的高维信息。

### 噪声调度不足以挽救 ϵ/v-prediction

Table 3 的噪声水平位移实验排除了噪声调度作为根本原因的可能性。通过调整 logit-normal t-采样器的 μ 参数，x-prediction 的 FID 从 μ=0.0 时的 14.44 优化至 μ=-0.8 时的 8.62，说明适当的高噪声对 x-prediction 有益。然而，ϵ-prediction 和 v-prediction 在所有噪声水平下均保持灾难性失败（FID 最低分别为 355.25 和 96.53），证明**信息容量瓶颈而非噪声调度是失败的根源**。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/006_Table_3.jpg]]
*Table 3: Noise-level shift (JiT-B/16, ImageNet 256×256, FID-50K). We shift the noise level by adjusting µ in the logit-normal t-sampler [15]. An appropriate noise level is useful, but is not sufficient for addressing the catastrophic failure in ϵ-/v-prediction. Settings (the same as Tab. 2): 200 epochs, with CFG*

### 瓶颈嵌入：流形假设的架构印证

Figure 4 展示了在 patch 嵌入中引入低秩瓶颈的效果。原始 patch 为 768 维（16×16×3），通过两个连续线性层嵌入，中间瓶颈维度 d′ 可调。实验表明，瓶颈维度在 32–512 范围内均可提升 FID 约 1.3，即使极端瓶颈（16 维）仍能生成图像。这从架构层面印证了流形假设：**自然图像 patch 的内在维度远低于像素维度，低秩嵌入帮助网络聚焦于低维流形信息**。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/008_Table_4.jpg]]
*Table 4: “Just Advanced” Transformers with general-purpose designs. All are JiT/16 for ImageNet 256×256, with bottleneck patch embedding (128-d, Fig. 4), evaluated by FID-50K. Settings: 200 epochs, with CFG (and with CFG interval [33] in brackets)*

### 高级 Transformer 组件的累积收益

Table 4 展示了在 JiT/16 上逐步叠加通用 Transformer 设计的效果。以基础 ViT 为起点（FID 10.08），依次加入 SwiGLU 激活（9.38）、RoPE 位置编码（8.82）、qk-norm（8.31）、RMSNorm（8.22）和 adaLN-Zero 条件化（7.34），最终结合 CFG 间隔后处理可降至 5.63。所有组件均为即插即用的通用设计，无需针对扩散模型定制。

### 主结果：自包含范式达到竞争性能

**ImageNet 256×256**（Table 7）：JiT-G/16 取得 FID 1.82，优于 DiT-XL/2（FID 2.27）和 SiT-XL/2（FID 2.06）。值得注意的是，JiT 未使用任何外部预训练模型（VAE tokenizer、分类器、自监督特征），而 RAE 等基线依赖表征自编码器预训练，PixNerd 使用感知损失（依赖预训练 VGG）。

**ImageNet 512×512**（Table 8）：JiT-G/32 以 1.78 FID 取得竞争结果，且计算量显著低于多尺度方法。由于 JiT 采用大步长 patch（32×32 像素），序列长度保持 16×16 tokens，避免了分辨率翻倍时计算量的二次增长。

### 预条件器的失败模式

Table 10 的消融揭示了预条件器在高维生成中的危害。EDM 预条件器（Karras et al.）和线性预条件器在 x-prediction 下分别导致 FID 升至 31.65 和 18.64（基线 8.62）。原因是预条件器通过混合不同噪声水平的信息来稳定训练，但在高维场景下，这种信息混合反而干扰了网络对低维流形的聚焦，印证了**直接预测避免信息混合更利于高维生成**的论断。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/017_Table_10.jpg]]
*Table 10: Comparisons with pre-conditioners (FID-50K, ImageNet 256, JiT-B/16). The settings are the same as Tab. 2 (a)*

### 可扩展性与跨分辨率能力

Table 6 展示了 JiT 从 B 到 G 规模的扩展性：在 256×256 上，FID 从 JiT-B/16 的 8.62 单调降至 JiT-G/16 的 1.82；在 512×512 上，JiT-H/32 取得 1.71 FID。Table 12 的跨分辨率实验表明，在 512 分辨率训练的模型下采样到 256 分辨率仍具竞争力，体现了该范式的灵活性。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/010_Table_6.jpg]]
*Table 6: Scalability on ImageNet 256×256 and 512×512, evaluated by FID-50K. All models have the same sequence length of 16×16, and thus the models at 512 resolution have nearly the same compute as their 256 counterparts. Settings: the same as Tab. 5*

### 公平性说明

JiT 的对比遵循严格的自包含原则：不使用 VAE tokenizer、分类器引导外的预训练网络、感知损失或对抗损失。部分结果使用 CFG 间隔（Kynkäänniemi et al.）改善 FID，但主表同时提供直接 CFG 结果作为参考。所有模型保持相同的 16×16 序列长度和相似参数量，确保跨分辨率对比的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/011_Table_7.jpg]]
*Table 7: Reference results on ImageNet 256×256. FID [21] and IS [53] of 50K samples are evaluated. The “pre-training” columns list the external models required to obtain the results (note that the perceptual loss [77] uses a pre-trained VGG classifier [56]). The parameters include the generator and tokenizer decoder (used at inference-time), but exclude other pre-trained components. The Giga-flops are measured for a single forward pass (not counting the tokenizer) and are roughly proportional to the computational cost of an iteration during both training and inference (for the multi-scale method [6], we measure the finest level)*

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2511_13720/figures/013_Table_8.jpg]]
*Table 8: Reference results on ImageNet 512×512. JiT has an aggressive patch size and can use small compute to achieve strong results. Notations are similar to Tab. 7*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

JiT 的核心主张——在高维像素空间直接预测干净图像（x-prediction）——使其与当前主流的扩散模型范式形成了根本性分歧。理解这一分歧，需要回溯到生成模型在“预测空间”选择上的演化脉络。

**主流范式：潜在空间中的噪声/速度预测。** 自 DDPM 以来，扩散模型的默认选择是预测噪声 ϵ 或流速度 v。这一范式在像素空间应用时面临严重的计算与质量挑战，因此后来的工作普遍转向两个方向：一是引入 VAE tokenizer 将图像压缩到低维潜在空间后再进行 ϵ/v-prediction，如 **DiT-XL/2**（Peebles & Xie, ICCV 2023）和 **SiT-XL/2**（Ma et al., ECCV 2024）；二是通过多尺度架构或预训练来缓解像素空间的建模难度，如 **RAE**（Zheng et al., 2025）使用表征自编码器进行预训练。这些方法的共同前提是：高维像素空间对 ϵ/v-prediction 不友好，必须通过降维或强先验来回避。

**JiT 的定位：回归像素空间的 x-prediction。** JiT 的立场恰恰相反——问题不在于像素空间本身，而在于预测目标的选择。论文的核心洞察是：ϵ 和 v 天然位于数据流形之外（off-manifold），要求网络在高维空间中保留完整信息；而 x 位于低维流形之上（on-manifold），网络只需关注流形附近的信息。这一洞察直接挑战了“潜在空间是必需品”的共识，证明一个纯 ViT 在原始像素块上配合 x-prediction，不仅可行，而且能与最优的潜在扩散模型竞争（ImageNet 256×256 上 JiT-G/16 的 FID 为 1.82，优于 DiT-XL/2 的 2.27）。

**与去噪自编码器的深层联系。** 论文明确指出，x-prediction 使扩散模型回归到“去噪自编码器”的本源——网络的任务就是“去噪”，即从噪声样本中恢复干净图像。这与流形假设（Figure 1）一脉相承：去噪自编码器之所以能学习有意义的表征，正是因为它迫使网络将输入映射到数据流形上。JiT 将这一思想从表征学习迁移到生成任务，揭示了两者在预测目标选择上的统一性。

**与流匹配框架的兼容性。** 值得注意的是，JiT 并未抛弃流匹配的损失框架——它仍然使用 v-loss（Eq. 3），只是网络直接输出 x_θ，再通过 $ \mathbf{v}_{\theta}(\mathbf{z}_t, t) = (\mathbf{x}_{\theta} - \mathbf{z}_t) / (1-t) $ 转换为速度。这意味着 JiT 可以无缝嵌入现有的流匹配采样器（如 50 步 Heun ODE 求解器），在推理效率上与主流方法持平。

### 2. 适用边界

**已验证的适用场景。** 当前证据集中在自然图像的类别条件生成任务上：ImageNet 256×256、512×512 和 1024×1024 分辨率下，JiT 均展现出竞争力或优越性。其架构的简洁性（纯 ViT，无 VAE tokenizer，无多尺度设计）意味着部署门槛低，且序列长度恒定（16×16 tokens）使计算量随分辨率线性增长，避免了多尺度方法中分辨率翻倍时的二次增长。

**需要谨慎对待的场景。**
- **高频细节的保真度。** 大步长块（如 16×16 像素）可能丢失部分高频纹理。虽然瓶颈嵌入和 x-prediction 在一定程度上弥补了这一缺陷，但在极端纹理丰富的场景（如毛发、织物特写）中，其表现尚未得到专门验证。
- **非自然图像域。** 流形假设的有效性依赖于数据本身具有低维流形结构。对于蛋白质结构、天气预测、医学影像等模态，该假设是否成立、x-prediction 是否同样优于 ϵ/v-prediction，目前缺乏实验证据。
- **小规模数据集。** 所有实验均在 ImageNet 规模上进行。在小数据集上，ViT 的归纳偏置较弱可能成为劣势，x-prediction 的优势是否依然存在需要进一步验证。

### 3. 局限性与开放问题

**已知局限。**
1. **未探索辅助损失与预训练的潜力。** 论文坦承，JiT 目前未使用感知损失、对抗损失或任何形式的预训练（VAE tokenizer、分类器、自监督特征）。这些技术已被证明能提升生成质量，与 x-prediction 的结合可能带来进一步的增益。
2. **数据集单一。** 仅在 ImageNet 上验证，缺乏跨域泛化证据。
3. **大步长块的固有局限。** 虽然瓶颈设计缓解了信息冗余问题，但块内的高频细节建模能力天然受限。

**核心开放问题。**
1. **瓶颈维度的选择准则。** Figure 4 显示瓶颈维度在 32–512 范围内均可工作，甚至极端瓶颈（16 维）仍能生成合理图像。但最优维度的选择是否具有一般性准则？能否在不同任务中自动确定？这一问题触及流形假设的可操作化——瓶颈维度本质上是对数据流形本征维度的隐式估计。
2. **与高效采样策略的协同。** 当前使用 50 步 Heun ODE 求解器。能否将 x-prediction 与更激进的少步采样策略（如一致性模型、对抗扩散蒸馏）结合，在保持质量的同时将步数降至 1–4 步？
3. **扩展到其他数据模态。** 流形假设的普适性意味着 x-prediction 的范式可能适用于文本、音频、蛋白质结构等“自然数据”。但不同模态的流形结构差异巨大，ViT 架构也需要相应调整。
4. **计算效率的进一步优化。** 虽然 JiT 避免了 VAE tokenizer 的额外开销，但纯 ViT 在原始像素上的自注意力计算仍随序列长度二次增长。结合稀疏注意力或线性注意力机制能否在保持质量的前提下降低计算成本？
5. **预条件器的失效原因。** Table 10 显示 EDM 和线性预条件器在 x-prediction 下导致严重质量下降。论文将此归因于预条件器混合了不同噪声水平的信息，破坏了 x-prediction 的“去噪”本质。但这一解释尚停留在直觉层面，更深入的理论分析——例如从优化景观或梯度方差的角度——仍有待展开。

## 原文 PDF

![[paperPDFs/CVPR_2026/Back_to_Basics_Let_Denoising_Generative_Models_Denoise.pdf]]
