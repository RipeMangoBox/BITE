---
title: "ViT$^3$: Unlocking Test-Time Training in Vision"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ViT_3_Unlocking_Test_Time_Training_in_Vision.pdf
project_link: null
code_link: "https://github.com/LeapLabTHU/ViTTT"
aliases:
- V3VTTT
- V3UTTTV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 内部训练配置（损失函数类型、批量大小与训练轮次、学习率）与内部模型设计（宽度、深度、架构类型如卷积或 MLP）的选择直接决定了 TTT 层的性能。
primary_logic: 采用避免混合二阶导数消失的损失函数（如点积损失或 MSE）、单轮全批量内部训练、较大内部学习率（1.0），并增加内部模型宽度（而非深度）且使用卷积架构（特别是深度可分离卷积）作为内部模型，可以显著提升视觉 TTT 模型在图像分类、检测、分割等任务上的性能，使其匹配或超越 Mamba 和线性注意力等线性复杂度方法。
claims:
- MAE (L1) 损失因混合二阶导数几乎处处为零，导致 Top-1 准确率最低（76.5%），验证了 Insight 1
- 全批量训练（B=N）取得最佳 Top-1（78.9%），优于小批量方案，验证了视觉任务中无因果偏好的 Insight 2
- 内部学习率 1.0 达到最高准确率（78.9%）且训练稳定，验证了 Insight 3
- 增加内部模型宽度（从 ratio 1 到 4）持续提升准确率（从 78.9% 到 79.6%），验证了 Insight 4
---

# ViT$^3$: Unlocking Test-Time Training in Vision

> [!tip] 核心洞察
> 采用避免混合二阶导数消失的损失函数（如点积损失或 MSE）、单轮全批量内部训练、较大内部学习率（1.0），并增加内部模型宽度（而非深度）且使用卷积架构（特别是深度可分离卷积）作为内部模型，可以显著提升视觉 TTT 模型在图像分类、检测、分割等任务上的性能，使其匹配或超越 Mamba 和线性注意力等线性复杂度方法。

| 字段 | 内容 |
|------|------|
| 中文题名 | ViT^3：解锁视觉测试时训练 |
| 英文题名 | ViT$^3$: Unlocking Test-Time Training in Vision |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.01643) · [Code](https://github.com/LeapLabTHU/ViTTT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ViT^3 (Vision Test-Time Training) |
| Dataset | ImageNet-1K, COCO, ADE20K |

> [!tip] 效果简介
> - ImageNet-1K (非分层模型) 上，Top-1 准确率 76.5 (ViT^3-T) vs 72.2 (DeiT-Ti) (+4.3)。
> - ImageNet-1K (分层模型) 上，Top-1 准确率 84.0 (H-ViT^3-T) vs 82.1 (ConvNeXt-T) (+1.9)。
> - COCO (目标检测, Mask R-CNN 1×) 上，APb (box AP) 48.9 (H-ViT^3-T) vs 47.3 (VMamba-T) (+1.6)。

## 概述

视觉 Transformer 中的 Softmax 注意力机制可被理解为利用未压缩的键值对构建一个隐藏宽度等于序列长度 N 的两层 MLP，这赋予了模型强大的表达能力，但同时也带来了 $O(N^2)$ 的计算复杂度。线性注意力通过将键值对压缩为一个固定的 $d \times d$ 权重矩阵 $W = K^\top V$，将复杂度降至 $O(N)$，然而这种一刀切的压缩方式限制了模型容量。测试时训练（Test-Time Training, TTT）将序列建模重构为在线学习问题——在测试时根据输入的键值对，通过几步自监督训练动态更新一个紧凑的内部模型 $\mathcal{F}_W(\cdot): \mathbb{R}^d \to \mathbb{R}^d$，从而在线性复杂度下实现更灵活的压缩与自适应。

尽管 TTT 在语言建模中展现出潜力，其在视觉任务中的设计空间此前几乎未被探索。本文的核心发现是：**视觉 TTT 的性能高度依赖于内部训练设置与内部模型架构的精心选择**，而此前的默认配置（如 MSE 损失、小批量多轮次训练、简单两层 MLP）远非最优。

具体而言，本文揭示了以下关键瓶颈与对应方案：

- **损失函数选择**：MAE（L1）损失因其混合二阶导数几乎处处为零，导致外部模型参数 $W_V$ 的梯度信号消失，Top-1 准确率仅为 76.5%；而点积损失（Dot Product Loss）与 MSE 损失则能有效传递梯度，准确率提升至约 79.0%（Table 1）。
- **内部训练配置**：与语言任务偏好小批量因果学习不同，视觉任务更适配**单轮次全批量梯度下降**（$B=N$, epochs=1），且内部学习率可大幅提升至 **1.0** 而保持训练稳定，取得 78.9% 的 Top-1 准确率（Table 2, Table 3）。
- **内部模型架构**：增加内部模型宽度（隐藏维度从 $d$ 扩展至 $4d$）可稳定提升性能（78.9% → 79.6%）；而加深内部模型（如三层 MLP）反而导致优化困难、训练损失升高。采用约束设计（如门控线性单元简化版 $\mathrm{FC}(x) \odot \mathrm{SiLU}(\mathrm{FC}(x))$）与引入**深度可分离卷积（DWConv）**可显著改善优化，最终达到 80.1% 的 Top-1 准确率（Table 4, Figure 3）。

基于上述发现，本文构建了 **ViT^3**（Vision Test-Time Training）模型系列。在 ImageNet-1K 分类任务上，非分层 ViT^3-T 以 76.5% 的 Top-1 准确率显著超越 DeiT-Ti 的 72.2%（+4.3%）；分层 H-ViT^3-T 达到 84.0%，优于 ConvNeXt-T 的 82.1%（+1.9%）。在下游任务中，H-ViT^3-T 作为骨干网络在 COCO 目标检测（APb 48.9 vs. VMamba-T 47.3）和 ADE20K 语义分割（mIoU 48.0 vs. ConvNeXt-T 46.8）上均取得领先，证明 TTT 可作为一种通用视觉骨干，在线性复杂度下匹配甚至超越 Mamba、线性注意力等主流高效架构。

**方法定位**：ViT^3 属于线性复杂度视觉架构中的**在线学习压缩范式**，其核心创新在于系统性地探索并优化了 TTT 的内部训练与模型设计空间，而非提出全新的宏观架构。与 Mamba（状态空间压缩）和线性注意力（固定矩阵压缩）相比，TTT 通过可训练的神经网络实现更灵活的键值对压缩，在保持 $O(N)$ 复杂度的同时获得更强的表征能力。

## 背景与动机

### 视觉骨干网络的效率困境

现代视觉骨干网络的核心运算单元是注意力机制。标准 **Softmax 注意力**（Vaswani et al., 2017）可被重新诠释为一个隐层宽度等于序列长度 N 的两层 MLP：

$$O = \sigma(Q K^\top) V \triangleq \sigma(Q W_1) W_2 = \mathrm{MLP}(Q)$$

这一视角揭示了 Softmax 注意力的根本矛盾：它直接在未压缩的键值对上进行操作，隐层宽度随序列长度线性增长，导致计算复杂度为 $O(N^2)$。当处理高分辨率图像或长序列时，该二次复杂度成为严重的效率瓶颈。

为突破这一限制，研究者提出了多种线性复杂度替代方案。**线性注意力**（Katharopoulos et al., ICML 2020）将键值对压缩为一个固定的 $d \times d$ 权重矩阵：

$$O = Q (K^\top V) \triangleq Q W = \mathrm{FC}(Q)$$

这等价于一个单层全连接网络，复杂度降至 $O(N)$。类似地，**状态空间模型**如 **Mamba / VMamba**（Zhu et al., ICML 2024）通过结构化状态空间实现线性复杂度序列建模。然而，这些方法受限于固定的压缩形式——线性注意力仅能表达线性映射，Mamba 依赖预定义的状态转移结构——在面对复杂视觉模式时，其表达能力存在天然上限。

### TTT：将注意力重构为在线学习

**测试时训练（Test-Time Training, TTT）** 提供了一条根本不同的路径。TTT 将注意力操作重新定义为在线学习问题：将键值对视为一个“迷你数据集”，在测试时通过自监督学习训练一个紧凑的内部模型 $\mathcal{F}_W(\cdot): \mathbb{R}^d \to \mathbb{R}^d$，再将该模型应用于查询：

$$\hat{V}_{\mathcal{B}} = \mathcal{F}_W(K_{\mathcal{B}}), \quad W \gets W - \eta \cdot \frac{\partial \mathcal{L}(\hat{V}_{\mathcal{B}}, V_{\mathcal{B}})}{\partial W}$$

TTT 的关键优势在于，内部模型 $\mathcal{F}_W$ 可以是**任意模块**——MLP、卷积网络，甚至微型 Transformer——从而在保持 $O(N)$ 复杂度的同时，获得远超固定压缩方法的表达能力。

### 视觉 TTT 的设计空间空白

尽管 TTT 在语言建模中展现出潜力，其在视觉领域的应用几乎是一片空白。核心瓶颈在于：**视觉 TTT 模型的设计空间缺乏系统性探索**。具体而言，以下关键设计维度尚未被理解：

1. **内部训练设置**：损失函数的选择如何影响梯度信号传播？批量大小、训练轮次、学习率应如何配置？
2. **内部模型架构**：宽度与深度如何权衡？MLP、卷积、门控单元等架构选择对性能有何影响？

缺乏对这些维度的系统性指导，使得视觉 TTT 模型的性能远未达到其理论潜力。本文的工作正是填补这一空白——通过逐项消融研究，揭示视觉 TTT 的关键设计原则，并构建首个在图像分类、目标检测、语义分割和图像生成等任务上全面匹配或超越主流线性复杂度方法的视觉 TTT 架构 **ViT³**。

## 核心创新

ViT^3 的核心创新在于**首次系统性地探索并解锁了视觉测试时训练（TTT）模型的设计空间**。此前的 TTT 工作局限于语言序列建模，视觉领域的 TTT 设计原则几乎为空白。本文通过理论分析与大规模消融实验，揭示了决定 TTT 层性能的六个关键因果旋钮，并将其系统化为一套可复现的设计配方，使 TTT 模型在图像分类、检测、分割和生成任务上首次匹配或超越了 Mamba、线性注意力等主流线性复杂度方法。

### 从 Softmax 注意力到 TTT 层的统一视角

理解创新的起点是统一的计算视角。论文将 Softmax 注意力、线性注意力和 TTT 层统一为“压缩-查询”框架下的不同实例：

- **Softmax 注意力**（**DeiT**，Touvron et al., ICML 2021）等价于构建一个隐藏宽度为序列长度 $N$ 的两层 MLP，直接使用未压缩的键值对 $K, V$ 作为权重：

$$O = \sigma(Q K^\top) V \triangleq \sigma(Q W_1) W_2 = \mathrm{MLP}(Q)$$

- **线性注意力**（Katharopoulos et al., ICML 2020）将键值对压缩为 $d \times d$ 的权重矩阵 $W = K^\top V$，查询时等价于一个线性层：

$$O = Q (K^\top V) \triangleq Q W = \mathrm{FC}(Q)$$

- **TTT 层**则将压缩过程升级为在线学习：在测试时，将键值对视为“迷你数据集”，通过几步自监督梯度下降训练一个紧凑的内部模型 $\mathcal{F}_W(\cdot): \mathbb{R}^d \to \mathbb{R}^d$，然后用训练后的模型处理查询：

$$\hat{V}_{\mathcal{B}} = \mathcal{F}_W(K_{\mathcal{B}}), \quad W \gets W - \eta \cdot \frac{\partial \mathcal{L}(\hat{V}_{\mathcal{B}}, V_{\mathcal{B}})}{\partial W}$$

这一框架下，Softmax 注意力是“无压缩”的特例，线性注意力是“单层线性压缩”的特例，而 TTT 则是“可学习的非线性压缩”的泛化形式。**ViT^3 的贡献不在于提出这一框架本身，而在于首次为视觉任务找到了使其高效工作的具体配置。**

### 六个关键设计旋钮（Changed Slots）

ViT^3 相对于基线 TTT 方法（以及 Softmax/线性注意力）的核心变更体现在以下六个相互关联的设计维度：

#### 1. 内部训练损失函数：避免混合二阶导数消失

**基线值**：先前 TTT 工作默认使用 MSE 损失。
**提出值**：点积损失（Dot Product Loss）或 MSE，明确避免 MAE（L1）损失。

**因果机制**：外循环对值投影矩阵 $W_V$ 的梯度依赖于混合二阶导数：

$$\frac{\partial G}{\partial W_V} = \frac{\partial \hat{V}_{\mathcal{B}}}{\partial W} \cdot \frac{\partial^2 \mathcal{L}(\hat{V}_{\mathcal{B}}, V_{\mathcal{B}})}{\partial \hat{V}_{\mathcal{B}} \partial V_{\mathcal{B}}} \cdot \frac{\partial V_{\mathcal{B}}}{\partial W_V}$$

MAE 损失的混合二阶导数几乎处处为零，导致梯度信号消失。实验验证（Table 1）：MAE 损失仅取得 76.5% Top-1 准确率，而 MSE（79.2%）和 Dot Product（79.0%）表现相当且显著更优。这一发现揭示了损失函数选择的理论约束——必须保证混合 Hessian 非零。

#### 2. 内部训练批量与轮次：单轮全批量

**基线值**：先前 TTT 工作采用小批量、多轮次的内部训练。
**提出值**：单轮次全批量梯度下降（$B=N$, epochs=1）。

**因果机制**：语言任务中，小批量训练有助于捕捉序列的因果依赖；但视觉任务中图像块之间不存在类似的因果结构，全批量训练反而提供了最稳定的梯度估计。Table 2 显示，全批量（B=N）取得最佳 78.9% Top-1，减小批量大小会单调降低准确率。这一发现直接推翻了语言 TTT 的默认配置，确立了视觉 TTT 的独特训练协议。

#### 3. 内部学习率：大胆的固定值 1.0

**基线值**：动态或较小的内部学习率。
**提出值**：固定学习率 $\eta = 1.0$。

**因果机制**：论文证明了在 MSE 损失下，缩放 $K, V$ 等价于改变内部学习率：$\tilde{K} = \sqrt{\eta}K, \tilde{V} = \sqrt{\eta}V$。因此，外循环可以通过调整键值的范数来自动适应内部学习率，使得大胆的 $\eta=1.0$ 成为安全且有效的选择。Table 3 验证：$\eta=1.0$ 达到最高 78.9% 准确率且训练稳定，过低或过高的学习率均导致性能下降。

#### 4. 内部模型宽度：容量是关键

**基线值**：两层 MLP，隐藏维度等于输入维度 $d$。
**提出值**：增加隐藏维度至 $4d$（width ratio = 4）。

**因果机制**：内部模型的表达能力直接决定了键值对压缩的质量。Table 4 显示，将宽度比从 1 增至 4，Top-1 准确率从 78.9% 持续提升至 79.6%，验证了“更宽更好”的缩放规律。

#### 5. 内部模型深度与约束设计：优化优于容量

**基线值**：标准两层 MLP。
**提出值**：门控线性单元的简化变体 $\mathrm{FC}(x) \odot \mathrm{SiLU}(\mathrm{FC}(x))$，并采用约束设计（如固定输出层为恒等映射）。

**因果机制**：直觉上更深的内部模型应提供更强表达能力，但实验揭示了一个反直觉现象——三层 MLP 因优化困难导致训练损失更高、测试准确率更低（Figure 3）。解决方案不是简单地增加深度，而是引入架构约束来改善优化景观：将标准两层 MLP 替换为 $\mathrm{SiLU}(x W_1) (W_2 + I)$ 的约束形式，准确率从 78.9% 提升至 79.4%。进一步移除输出层（即 SwiGLU 的恒等输出版本）将准确率推至 79.7%。这表明，在 TTT 的内部优化中，**易优化性比原始容量更重要**。

#### 6. 卷积内部模型：引入归纳偏置

**基线值**：全连接 MLP 作为内部模型。
**提出值**：深度可分离卷积（DWConv）作为内部模型。

**因果机制**：视觉数据具有强烈的局部空间结构，全连接内部模型缺乏利用这一先验的能力。Table 4 显示，采用 DWConv 作为内部模型将 Top-1 准确率进一步提升至 80.1%，在所有内部模型设计中取得最佳结果。这是首次将卷积结构引入 TTT 内部模型，证明了归纳偏置在在线学习场景中的价值。

### 创新总结

ViT^3 的六项设计变更形成了一个**协同优化的系统**：点积/MSE 损失保证了梯度信号的完整性，全批量单轮次训练提供了最稳定的内部优化，学习率 1.0 简化了超参选择，宽度扩展和卷积结构提升了模型容量与归纳偏置，而约束设计则缓解了深层模型的优化瓶颈。这些变更并非孤立存在——例如，学习率 1.0 的有效性建立在损失函数选择和全批量训练的基础之上，共同构成了视觉 TTT 的完整设计配方。

## 整体框架

ViT³ 的整体架构遵循标准 Transformer 的宏设计范式，其核心创新在于将注意力机制替换为测试时训练（Test-Time Training, TTT）模块。模型由以下主要组件串联构成：

1. **Patch Embedding（块嵌入层）**：将输入图像分割为固定大小的图像块（patch），并通过线性投影映射为嵌入向量序列，形成初始的 token 表示。

2. **Positional Encoding（位置编码）**：采用条件位置编码（Conditional Position Encoding, CPE）为 token 序列注入空间位置信息。

3. **TTT Block（测试时训练块）**：这是架构的核心计算单元，直接替代了标准 Transformer 中的自注意力层。每个 TTT 块内部包含多头 TTT 层，其工作流程如下：
   - **输入**：给定查询（Query, Q）、键（Key, K）、值（Value, V）三组向量，其中 K 和 V 被视为一个“微型数据集”。
   - **内部训练（Inner Training）**：在推理时，TTT 层使用自监督损失函数（如点积损失或 MSE）对内部模型 $\mathcal{F}_W(\cdot): \mathbb{R}^d \to \mathbb{R}^d$ 进行在线梯度下降更新，将键值对 (K, V) 的信息压缩到内部模型的权重 W 中。
   - **推理（Inference）**：更新后的内部模型 $\mathcal{F}_W$ 直接应用于查询 Q，生成输出 O。
   - **多头机制**：每个注意力头可以独立配置不同的内部模型架构（如 MLP、门控线性单元或深度可分离卷积），实现异构的信息压缩。

4. **Inner Model（内部模型 $\mathcal{F}_W$）**：一个紧凑的神经网络模块，在 TTT 层内部根据当前序列的键值对进行在线训练。ViT³ 探索了多种内部模型设计，包括：
   - 两层 MLP（基线）
   - 约束设计的简化门控线性单元：$\mathcal{F}_1 = \mathrm{FC}(x) \odot \mathrm{SiLU}(\mathrm{FC}(x))$
   - 深度可分离卷积（DWConv），这是性能最优的选择

5. **Task-Specific Head（任务特定头）**：根据下游任务（图像分类、目标检测、语义分割或图像生成）附加的线性层或卷积头。

TTT 模块与 Transformer 共享相同的宏架构（Figure 2），这意味着它可以直接嵌入到现有的 Vision Transformer 框架中，无论是非分层架构（如 ViT³）还是分层架构（如 H-ViT³），均保持整体 pipeline 的输入输出流不变。

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the TTT model building block. TTT shares the same macro architecture as Transformer*

### 补充图表

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of Softmax attention [59], linear attention [32], and Test-Time Training (TTT) module [56]. (a) Softmax attention can be viewed as building a two-layer MLP that directly uses the uncompressed keys K and values V , where the hidden width equals the sequence length N and the nonlinearity is Softmax. While effective, this N -width MLP leads to*

## 核心模块与公式推导

### 注意力机制的三种视角

ViT^3 的核心创新在于将序列建模中的注意力操作重新解释为在线学习问题。论文从统一的视角出发，将 Softmax 注意力、线性注意力和 TTT 模块视为对键值对 (K, V) 进行压缩的不同策略。

**Softmax 注意力**可被理解为一个隐式的两层 MLP，其隐藏层宽度等于序列长度 N，非线性为 Softmax：

$$O_i = \sum_{j=1}^N \frac{\exp(Q_i K_j^\top)}{\sum_{j=1}^N \exp(Q_i K_j^\top)} V_j$$

等价地，可重写为 MLP 形式：

$$O = \sigma(Q K^\top) V \triangleq \sigma(Q W_1) W_2 = \mathrm{MLP}(Q)$$

其中 $W_1 = K^\top$，$W_2 = V$，$\sigma$ 为 Softmax 函数。该 MLP 的隐藏宽度为 N，导致 $O(N^2)$ 的计算复杂度。

**线性注意力**将键值对压缩为一个固定的 $d \times d$ 权重矩阵：

$$O = Q (K^\top V) \triangleq Q W = \mathrm{FC}(Q)$$

其中 $W = K^\top V$。这等价于一个线性层，复杂度降为 $O(N)$，但压缩过程不可学习，表达能力受限。

**TTT 模块**将键值对视为一个“迷你数据集”，通过自监督在线训练学习一个紧凑的内部模型 $\mathcal{F}_W(\cdot): \mathbb{R}^d \to \mathbb{R}^d$。其核心更新步骤为：

$$\hat{V}_{\mathcal{B}} = \mathcal{F}_W(K_{\mathcal{B}}), \quad W \gets W - \eta \cdot \frac{\partial \mathcal{L}(\hat{V}_{\mathcal{B}}, V_{\mathcal{B}})}{\partial W}$$

其中 $\mathcal{B}$ 为一个 mini-batch 的键值对索引，$\mathcal{L}$ 为自监督重建损失，$\eta$ 为内部学习率。TTT 通过梯度下降将键值对的信息压缩到内部模型权重 W 中，而后用更新后的 W 对查询 Q 进行前向推理。

### TTT 模块的宏架构

TTT 模块与标准 Transformer 共享相同的宏架构（Figure 2）。一个 TTT Block 包含：
- **多头 TTT 层**：替代自注意力，每个头可独立维护一个内部模型 $\mathcal{F}_W$，实现不同的压缩策略。
- **Patch Embedding**：将输入图像分割为块并映射为嵌入向量。
- **条件位置编码 (CPE)**：引入位置信息。
- **MLP Head / 任务特定头**：根据下游任务（分类、检测、分割、生成）添加线性或卷积头。

### 外循环梯度的关键条件

TTT 层在外循环（主网络训练）中需要对内部模型权重 W 和键值投影参数 $W_V$ 求导。对 $W_V$ 的梯度依赖于混合二阶导数：

$$\frac{\partial G}{\partial W_V} = \frac{\partial \hat{V}_{\mathcal{B}}}{\partial W} \cdot \frac{\partial^2 \mathcal{L}(\hat{V}_{\mathcal{B}}, V_{\mathcal{B}})}{\partial \hat{V}_{\mathcal{B}} \partial V_{\mathcal{B}}} \cdot \frac{\partial V_{\mathcal{B}}}{\partial W_V}$$

若混合二阶导数 $\frac{\partial^2 \mathcal{L}}{\partial \hat{V} \partial V}$ 为零，则外循环对 $W_V$ 的梯度信号消失。这解释了为何 MAE (L1) 损失表现最差——其混合二阶导数几乎处处为零，导致 Top-1 准确率仅 76.5%（Table 1）。而 MSE 和点积损失（Dot Product Loss）因混合二阶导数非零，表现显著更优（约 79.0%），验证了 Insight 1。

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/004_Table_1.jpg]]
*Table 1: Results of different inner training loss functions. Please refer to the Appendix for detailed formulas of each loss function*

### 内部模型的具体实现

ViT^3 探索了多种内部模型架构（Table 4），最终采用的两种核心设计为：

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/007_Table_4.jpg]]
*Table 4: Results of different inner model designs. The r and l denote width ratio and layer-wise depth of a MLP. For example, r3, l2 refers to a 2-layer MLP with hidden dimension 3d, where d is the input and output dimension of an inner model*

**门控线性单元简化版**：
$$\mathcal{F}_1 = \mathrm{FC}(x) \odot \mathrm{SiLU}(\mathrm{FC}(x))$$

该设计移除了标准 SwiGLU 的输出线性层（即输出层固定为单位映射），将准确率从 79.0% 提升至 79.7%。

**深度可分离卷积 (DWConv)**：在内部模型中引入卷积结构，利用局部归纳偏置，取得 80.1% 的最佳 Top-1 准确率，验证了 Insight 6。

### 内部训练配置的等价性

论文揭示了一个重要的数学等价关系：在 MSE 损失下，对键值对进行缩放等价于改变内部学习率：

$$\eta \cdot \frac{\partial \mathcal{L}(\hat{V}, V)}{\partial W} = \eta \cdot K^\top(K W - V) = \tilde{K}^\top(\tilde{K} W - \tilde{V})$$

其中 $\tilde{K} = \sqrt{\eta}K$，$\tilde{V} = \sqrt{\eta}V$。这一性质为内部训练的超参数设计提供了理论依据，并解释了为何固定学习率 1.0 配合全批量训练（B=N）即可取得最优效果（Table 2, Table 3）。

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/003_Table_2.jpg]]
*Table 2: Results of various batch sizes and epochs. * refers to the best accuracy before divergence during training*

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/005_Table_3.jpg]]
*Table 3: Results of different inner learning rates. * refers to the best accuracy before divergence during training*

### 补充图表

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/006_Figure_3.jpg]]
*Figure 3: Results of TTT models with inner modules of 1, 2, 3 layers (FC, two-layer and three-layer MLP). Deeper inner models lead to higher training loss, and thus lower test accuracy*

## 实验与分析

### 内部训练配置的消融研究

作者围绕 TTT 层的内部训练配置进行了系统消融，揭示了对视觉任务至关重要的设计选择。

**损失函数的选择（Insight 1）。** 内部训练损失函数直接影响外循环梯度的有效性。核心机制在于：外循环对值投影矩阵 $W_V$ 的梯度依赖于损失函数对预测值 $\hat{V}$ 和真实值 $V$ 的**混合二阶导数**（见 Eq. 6）。若该导数消失，梯度信号将无法回传。实验验证了这一理论：MAE（L1）损失因其混合二阶导数几乎处处为零，导致 Top-1 准确率仅 76.5%，为所有损失中最差；MSE 损失和点积损失（Dot Product）表现相当，均达到约 79.0% 的准确率（Table 1）。这一结论与 NLP 领域的先前发现形成鲜明对比——视觉任务中 MSE 与点积损失均可有效工作，而 MAE 则完全失效。

**批量大小与训练轮次（Insight 2）。** 内部训练的批量大小和轮次对性能有显著影响。全批量训练（$B=N$，即单轮次批梯度下降）取得最佳 Top-1 准确率 78.9%。减小批量大小（如 $B=128, 256$）会导致准确率下降，而增加训练轮次（如 epochs=2）几乎不带来收益（Table 2）。这表明视觉序列建模任务**偏好非因果的单轮次全批量学习**，与 NLP 中需要 mini-batch 多轮次训练的因果偏好形成对比。

**内部学习率（Insight 3）。** 内部学习率 $\eta$ 的最优值确定为 1.0，此时达到最高准确率 78.9% 且训练稳定。过低的学习率（如 0.1）或过高的学习率（如 10.0）均会损害性能（Table 3）。值得注意的是，作者从理论上证明了缩放键值对 $K, V$ 在数学上等价于改变内部学习率（Remark 3），这为理解 TTT 层的优化行为提供了统一视角。

### 内部模型架构的消融研究

内部模型 $\mathcal{F}_W(\cdot): \mathbb{R}^d \to \mathbb{R}^d$ 的设计是 TTT 层的核心自由度。作者从宽度、深度和架构类型三个维度进行了深入探索（Table 4）。

**宽度扩展持续有效（Insight 4）。** 将内部模型的隐藏维度从 $d$（ratio 1）逐步增加到 $4d$（ratio 4），Top-1 准确率从 78.9% 单调提升至 79.6%。这表明增加内部模型容量是提升 TTT 性能的可靠路径。

**深度扩展面临优化困难（Insight 5）。** 与宽度扩展的稳定收益不同，增加内部模型深度（从单层 FC 到三层 MLP）会导致**训练损失升高、测试准确率下降**（Figure 3）。三层 MLP 的内部训练损失明显高于两层 MLP，表明深层内部模型在单轮次全批量训练下存在优化困难。为解决这一问题，作者探索了约束设计：采用简化的门控线性单元 $\mathrm{FC}(x) \odot \mathrm{SiLU}(\mathrm{FC}(x))$ 替代完整的两层 MLP，将准确率从 78.9% 提升至 79.4%；进一步移除输出层（即恒等输出层的 SwiGLU），准确率进一步提升至 79.7%。

**卷积架构带来显著增益（Insight 6）。** 在内部模型中引入卷积结构可大幅提升性能。使用深度可分离卷积（DWConv）作为内部模型取得了 **80.1% 的 Top-1 准确率**，为所有内部模型设计中的最佳结果。这表明卷积的归纳偏置（局部连接、空间共享权重）与 TTT 的在线学习机制高度互补，能够更有效地从键值对中提取结构化信息。

### 主实验结果

#### 图像分类

**分层架构（Table 5）。** H-ViT^3-T 在 ImageNet-1K 上达到 84.0% 的 Top-1 准确率，超越 ConvNeXt-T（82.1%）、VMamba-T（82.5%）和 Swin-T（81.3%）等代表性基线，增益为 +1.5% 至 +2.7%。H-ViT^3-S 进一步达到 84.9%，与更大规模的模型相比仍具竞争力。所有模型均使用标准 300 epoch 训练设置，标注 ‡ 的模型使用了 MESA 正则化以防止过拟合，比较是公平的。

**非分层架构（Table 7）。** ViT^3-T 在 ImageNet-1K 上取得 76.5% 的 Top-1 准确率，相比 DeiT-Ti 基线（72.2%）提升 **+4.3 个百分点**。这一增益完全来自将 Softmax 注意力替换为 TTT 层，验证了 TTT 机制本身的有效性。

#### 下游任务泛化

**目标检测（Table 8）。** 在 COCO 数据集上使用 Mask R-CNN 1× 框架，H-ViT^3-T 骨干网络达到 48.9 APb（box AP），超越 VMamba-T（47.3 APb）和 ConvNeXt-T（46.2 APb），增益分别为 +1.6 和 +2.7。在实例分割任务上（APm），H-ViT^3-T 同样表现出优势。

**语义分割（Table 9）。** 在 ADE20K 数据集上使用 UperNet 框架，H-ViT^3-T 达到 48.0 mIoU，超过 ConvNeXt-T（46.8 mIoU）和 Swin-T（44.5 mIoU）。这表明 TTT 层学习到的压缩表示具有良好的空间理解能力。

**图像生成（Table 10）。** 在 ImageNet-1K 类别条件图像生成任务上，基于 TTT 的扩散 Transformer（DiT^3）在 FID 指标上取得了有竞争力的结果，验证了 TTT 机制在生成任务中的适用性。

### 失败模式与局限

1. **深层内部模型的优化困难。** 三层及更深的 MLP 内部模型在单轮次全批量训练下出现训练损失升高、测试准确率下降的问题（Figure 3），限制了通过增加深度来扩展容量的路径。当前最佳方案是通过架构约束（如简化的门控单元）来缓解，但根本性的解决方案（如残差连接或结构化初始化）尚未被探索。

2. **MAE 损失的彻底失效。** MAE（L1）损失因混合二阶导数消失导致性能最差（76.5%），验证了理论分析的正确性，但也意味着某些在 NLP 中可行的损失函数在视觉 TTT 中完全不可用。

3. **计算开销。** TTT 层的前向传播包含内部训练步骤，相比标准注意力存在约 4× 的前向-反向计算开销（Figure 4 的效率对比），在资源受限场景下可能成为瓶颈。

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/013_Figure_4.jpg]]
*Figure 4: Comparisons between DeiT and*

4. **未探索的设计空间。** 内部优化器（如 Adam 替代 SGD）、内部数据增强、Transformer 作为内部模型等设计选择未被研究，研究并非穷尽。

### 补充图表

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/008_Table_5.jpg]]
*Table 5: Comparison with hierarchical architectures on ImageNet-1K. We focus on representative ConvNet, Transformer, Mamba, and Linear attention methods. ‡ indicates the model is trained with MESA [14], a strategy that can alleviate overfitting at little cost*

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/009_Table_7.jpg]]
*Table 7: Comparison with non-hierarchical designs on ImageNet*

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/010_Table_8.jpg]]
*Table 8: Results on COCO dataset. C, T, M, L represent ConvNet, Transformer, Mamba, and Linear attention, respectively. The FLOPs are computed with an input resolution of 1280×800*

![[assets/figures/papers/paper_list_l2146_https_arxiv_org_abs_2512_01643/figures/011_Table_9.jpg]]
*Table 9: Results of semantic segmentation. FLOPs are calculated with an input resolution of 512×2048*

## 方法谱系与知识库定位

### 1. 方法脉络：从 Softmax 注意力到测试时训练

ViT^3 的核心贡献在于将**测试时训练（Test-Time Training, TTT）** 范式从语言序列建模成功迁移到视觉主干网络，并首次系统性地揭示了视觉 TTT 的设计空间。为理解这一贡献，需先梳理注意力机制的演化脉络。

**Softmax 注意力**（Vaswani et al., NeurIPS 2017）可被重新诠释为一种特殊的"在线学习"过程：对每个查询 $Q_i$，它隐式地构建了一个隐藏宽度等于序列长度 $N$ 的两层 MLP：
$$O_i = \sum_{j=1}^N \frac{\exp(Q_i K_j^\top)}{\sum_{j=1}^N \exp(Q_i K_j^\top)} V_j$$
该 MLP 的第一层权重由键 $K$ 构成，第二层权重由值 $V$ 构成，非线性为 Softmax。这种视角揭示了 Softmax 注意力的本质缺陷：**内部模型容量随序列长度线性增长**，导致 $O(N^2)$ 的计算复杂度。

**线性注意力**（**Linear Attention**, Katharopoulos et al., ICML 2020）通过改变键-值对的结合顺序，将复杂度降至 $O(N)$：
$$O = Q (K^\top V) \triangleq Q W = \mathrm{FC}(Q)$$
这等价于将 $K$ 和 $V$ 压缩为一个固定的 $d \times d$ 权重矩阵 $W$，然后对查询 $Q$ 执行线性变换。然而，这种"一次性压缩"策略丧失了 Softmax 注意力的非线性表达能力和对序列内容的适应性。

**TTT 层**（Sun et al., 2024）在线性注意力与 Softmax 注意力之间建立了连续的谱系。它保留了线性注意力的压缩思想，但将压缩过程升级为**在线梯度下降**：
$$\hat{V}_{\mathcal{B}} = \mathcal{F}_W(K_{\mathcal{B}}), \quad W \gets W - \eta \cdot \frac{\partial \mathcal{L}(\hat{V}_{\mathcal{B}}, V_{\mathcal{B}})}{\partial W}$$
内部模型 $\mathcal{F}_W(\cdot): \mathbb{R}^d \to \mathbb{R}^d$ 可以是任意神经网络模块，通过自监督重建损失 $\mathcal{L}$ 在键值对上实时更新权重 $W$。这使得 TTT 既具备线性复杂度，又保留了非线性适应能力。

**ViT^3 的突破**在于：此前 TTT 仅在小规模语言任务上验证，其设计空间（损失函数、训练配置、内部模型架构）在视觉领域几乎未被探索。ViT^3 通过系统消融，找到了使 TTT 在 ImageNet 分类、COCO 检测、ADE20K 分割等任务上匹配甚至超越 **Mamba**（Zhu et al., ICML 2024）和线性注意力等线性复杂度方法的关键配置。

### 2. 与基线方法的关系定位

ViT^3 在实验中与四类代表性方法进行了系统对比：

| 方法类别 | 代表工作 | 核心机制 | 复杂度 | ViT^3 的优势 |
|---------|---------|---------|--------|-------------|
| 标准 ViT | **DeiT** (Touvron et al., ICML 2021) | Softmax 注意力 | $O(N^2)$ | 非分层模型 +4.3% Top-1 (76.5 vs 72.2) |
| 现代卷积 | **ConvNeXt** (Liu et al., CVPR 2022) | 深度可分离卷积 | $O(N)$ | 分层模型 +1.9% Top-1 (84.0 vs 82.1) |
| 状态空间 | **VMamba** (Zhu et al., ICML 2024) | 选择性状态空间 | $O(N)$ | COCO 检测 +1.6 APb (48.9 vs 47.3) |
| 线性注意力 | **Linear Attention** (Katharopoulos et al., ICML 2020) | 核技巧线性化 | $O(N)$ | 同复杂度下更强的非线性表达能力 |

**关键区分点**：ViT^3 并非简单的"又一个线性复杂度替代方案"。其本质优势在于**在线适应性**——内部模型权重随输入动态更新，使得每一层都能根据当前样本的键值对分布调整其变换。这与 Mamba 的固定状态转移和线性注意力的静态压缩形成根本差异。

### 3. 适用边界与设计约束

基于消融实验揭示的因果机制，ViT^3 的适用边界可归纳如下：

**必须满足的条件**：
- **损失函数需避免混合二阶导数消失**。MAE（L1）损失因 $\frac{\partial^2 \mathcal{L}}{\partial \hat{V} \partial V}$ 几乎处处为零，导致外循环梯度信号断裂（Top-1 仅 76.5%）。MSE 和点积损失均能维持梯度流动（约 79.0%）。
- **内部训练需采用全批量单轮次**。视觉任务缺乏语言中的因果偏好，小批量训练会损害准确率（Table 2 显示批量减小导致性能下降）。
- **内部学习率需固定为 1.0**。过低的学习率限制适应能力，过高则导致训练发散（Table 3）。

**推荐的设计选择**：
- **内部模型应宽而非深**。将隐藏维度从 $d$ 扩展到 $4d$，准确率从 78.9% 持续提升至 79.6%。但加深至三层 MLP 反而因优化困难导致性能下降（Figure 3）。
- **卷积内部模型显著优于全连接**。深度可分离卷积（DWConv）作为内部模型取得 80.1% 的最佳 Top-1，验证了归纳偏置在 TTT 内部模型中的价值。
- **门控机制有效但需简化**。SiLU(FC(x)) 的约束设计（移除输出层）将准确率从 78.9% 提升至 79.4%，但完整的 SwiGLU 反而略低（79.0%）。

**当前不适用或需谨慎的场景**：
- **极小模型容量**：TTT 层的 4× 前向-反向计算开销使其在极致轻量场景下不如线性注意力高效。
- **需要多轮内部训练的任务**：当前设计仅支持单轮全批量训练，可能限制在需要因果建模的序列任务上的表现。

### 4. 已知局限与开放问题

**已确认的局限**（论文明确承认）：
1. **设计空间探索非穷尽**：内部优化器（如 Adam）、内部数据增强、Transformer 作为内部模型等方向未涉及。
2. **深层内部模型的优化困难**：三层 MLP 的训练损失高于两层，测试准确率反而下降，限制了通过深度扩展容量的路径。
3. **计算开销**：TTT 层的前向过程包含内部训练的反向传播，相比标准注意力有约 4× 的理论开销（实际吞吐量对比见 Figure 4）。

**开放问题**（需进一步研究）：
- **视觉专用的小批量内部训练算法**：能否设计结合因果与非因果建模的 mini-batch 策略，既保持全批量的优化稳定性，又引入序列偏好的灵活性？
- **深层内部模型的初始化与训练策略**：残差连接或结构化初始化能否缓解三层及以上 MLP 的优化困难，释放更大容量？
- **卷积内部模型的深度扩展**：DWConv 在单层/两层表现优异，能否构建更深的卷积内部模型（>3 层）并保持有效训练？
- **轻量化内部模型设计**：如何利用 TTT 的在线学习特性，设计参数更少但表达力足够的内部模型，降低前向-反向的计算开销？
- **内部优化器的选择**：当前仅使用 SGD，Adam 等自适应优化器能否在内部训练中带来增益？

**需要人工验证的点**：论文未提供 ViT^3 在视频理解、多模态等更复杂视觉任务上的实验结果，其在时序建模场景中的表现是否仍能匹配 Mamba 等时序原生架构，尚待第三方验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/ViT_3_Unlocking_Test_Time_Training_in_Vision.pdf]]
