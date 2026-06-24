---
title: "Cubic Discrete Diffusion: Discrete Visual Generation on High-Dimensional Representation Tokens"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Cubic_Discrete_Diffusion_Discrete_Visual_Generation_on_High_Dimensional_Representation_Tokens.pdf
project_link: null
code_link: "https://github.com/YuqingWang1029/CubiD"
aliases:
- CDDC
- CDDDVGHDRT
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
core_operator: 从“按空间位置或维度分组掩码”转变为“在 h×w×d 三维张量上进行逐元素独立掩码”（立方掩码），使模型能够从部分观测中同时学习空间和维度轴上的依赖关系。
primary_logic: 将高维离散表示视为一个三维张量，通过对其任意子集（任意位置的任意维度）进行掩码并利用双向注意力从可见部分预测被掩码部分，模型能够以固定的 T 步（T ≪ hwd）完成生成，而无需序列化所有维度，从而将复杂依赖建模与计算可行性解耦。
claims:
- 逐元素掩码（per-element）生成质量显著优于按维度或按空间位置掩码：gFID 5.33 vs 120.03 / 22.22。
- 维度级量化（DQ）在理解任务上保持连续特征级别的性能，而向量量化（VQ）严重退化。
- CubiD‑XXL 在 ImageNet 256×256 上达到最优离散生成结果 gFID 1.88，且参数从 9 亿扩展到 37 亿时性能持续提升。
- ImageNet 256×256 Class‑Conditional Generation 上 gFID = 1.88 (CubiD‑XXL w/ classifier‑free guidance)
---

# Cubic Discrete Diffusion: Discrete Visual Generation on High-Dimensional Representation Tokens

> [!tip] 核心洞察
> 将高维离散表示视为一个三维张量，通过对其任意子集（任意位置的任意维度）进行掩码并利用双向注意力从可见部分预测被掩码部分，模型能够以固定的 T 步（T ≪ hwd）完成生成，而无需序列化所有维度，从而将复杂依赖建模与计算可行性解耦。

| 字段 | 内容 |
|------|------|
| 中文题名 | 立方离散扩散：面向高维表示令牌的离散视觉生成 |
| 英文题名 | Cubic Discrete Diffusion: Discrete Visual Generation on High-Dimensional Representation Tokens |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.19232v1) · [Code](https://github.com/YuqingWang1029/CubiD) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer |
| Method | Cubic Discrete Diffusion (CubiD) |
| Dataset | ImageNet 256×256 Class‑Conditional Generation |

> [!tip] 效果简介
> - ImageNet 256×256 Class‑Conditional Generation 上，gFID 1.88 (CubiD‑XXL w/ classifier‑free guidance) vs — (仅报告自身结果；其他方法因令牌维度不同无法直接对比) (—)。

## 概述

### 问题背景

当前离散视觉生成方法普遍依赖低维潜在令牌（通常 ≤32 维），无法有效利用预训练视觉编码器（如 DINOv2、SigLIP2）产生的高维（768+ 维）特征表示。这些高维特征富含语义信息，在理解任务中表现优异，但将其作为生成目标面临根本性挑战：自回归方法需要逐维度序列化，生成步数达到 $h \times w \times d$ 量级，计算不可行；而标准离散扩散方法以整个空间位置为单元进行掩码与预测，无法捕捉同一位置内部各维度间的复杂依赖关系。

### 核心方法

**CubiD（Cubic Discrete Diffusion）** 提出了一种全新的高维离散生成范式。其核心思想是将高维离散表示视为一个 $h \times w \times d$ 的三维张量，并在此张量上执行**逐元素（per-element）掩码建模**——任意空间位置的任意维度均可被独立掩码，模型通过双向注意力从可见部分预测被掩码的令牌。这一设计同时建模了空间轴和维度轴上的依赖关系，并将生成步数 $T$ 与特征维度 $d$ 解耦（$T \ll h \times w \times d$），实现了高维离散生成的计算可行性。

配合逐元素掩码，CubiD 采用**维度级量化（Dimension-wise Quantization）** 替代传统的向量量化（VQ），对冻结的预训练特征逐维度独立量化，无需重训练编码器，且能保持连续特征级别的语义质量。

### 关键结论

- **掩码粒度的决定性作用**：逐元素掩码在生成质量上大幅优于按维度掩码（gFID 5.33 vs 120.03）和按空间位置掩码（gFID 5.33 vs 22.22），验证了细粒度掩码对高维令牌生成的必要性。
- **维度级量化的语义保持**：在 LLaVA 多模态理解基准上，维度级量化（DQ）保持与连续特征几乎一致的性能，而向量量化（VQ）则出现显著退化。
- **规模化增益**：CubiD 从 9 亿参数扩展至 37 亿参数时性能持续提升，CubiD-XXL 在 ImageNet 256×256 上达到 gFID 1.88，为当前离散生成方法的最优结果。
- **通用性**：CubiD 同样适用于低维令牌和压缩表示令牌，在 ImageNet 512×512 上使用 32 维令牌达到 gFID 1.58，展现出跨令牌维度的泛化能力。

### 局限性

CubiD 的生成质量受限于冻结编码器的重建能力（当前 PSNR 约 18 dB），与连续扩散方法仍存在差距；此外，高质量生成通常需要数百到上千步迭代，推理效率有待提升。

## 背景与动机

### 离散视觉生成的核心瓶颈

离散生成模型因其与统一多模态架构（如多模态大语言模型）的自然兼容性而受到广泛关注。然而，现有方法在生成质量与计算可行性之间存在根本性矛盾，其根源在于**令牌维度**的选择：

- **低维令牌路径**：主流方法（如 MaskGIT 等标准离散扩散模型）将图像压缩为 8–32 维的潜在令牌，在空间维度上进行掩码与生成。这种方式计算可行，但低维潜在空间严重损失了语义丰富性，难以捕捉复杂视觉细节。
- **高维令牌路径**：预训练视觉编码器（如 DINOv2、SigLIP2）能提取 768 维以上的高维语义特征，蕴含丰富的视觉理解信息。然而，直接生成高维离散令牌面临根本性挑战：
  - **自回归方法**需要 $h \times w \times d$ 步（如 16×16×768 ≈ 196,608 步），计算完全不可行。
  - **标准离散扩散方法**以整个空间位置为单元进行掩码——即将某个位置的所有 768 维同时屏蔽或保留。这导致模型无法捕捉同一空间位置内各维度间的复杂依赖关系，因为维度间的交互在训练中从未被部分观测所揭示。

这一困境构成了本文的核心问题：**如何在高维离散令牌上实现既计算可行、又能充分建模维度间依赖的生成？**

### 现有方法的缺口

Figure 1 清晰地对比了现有范式与本文方法的差异：

- **低维生成**（Figure 1a）：自回归需要 $h \times w$ 步，离散扩散可在 $T < h \times w$ 步内并行生成，但两者均受限于低维令牌的表达能力。
- **高维生成**（Figure 1b）：自回归因步数爆炸而不可行；标准离散扩散虽可并行，但其“按空间位置掩码”的策略将整个位置视为原子单元，无法建模同一位置内 768 个维度之间的复杂依赖。这种粗粒度掩码在高维场景下会导致严重的生成质量退化——消融实验证实，按空间位置掩码的 gFID 仅为 22.22，远劣于逐元素掩码的 5.33（Table 4b）。

### 本文动机

本文的核心洞察在于：**将高维离散表示视为一个 $h \times w \times d$ 的三维张量，而非“空间位置上的 $d$ 维向量集合”**。通过在这个三维张量的任意子集（任意位置的任意维度）上进行独立的逐元素掩码，模型能够从部分观测中同时学习空间轴和维度轴上的依赖关系。这一设计将复杂依赖建模与计算可行性解耦——生成步数 $T$ 固定且远小于 $h \times w \times d$，无需序列化所有维度。

基于此洞察，本文提出 **Cubic Discrete Diffusion (CubiD)**，一种面向高维离散令牌的掩码扩散方法，旨在填补离散生成在高维表示空间中的方法空白。

## 核心创新

CubiD 的核心创新在于将高维离散令牌的生成问题从“空间位置或维度分组”的粗粒度掩码范式，转变为**在完整的三维张量上进行逐元素独立掩码**的细粒度建模范式。这一转变通过三个关键设计实现，直接解决了现有方法无法处理高维（768+维）表示令牌的根本瓶颈。

### 1. 维度级量化（Dimension-wise Quantization）

传统离散生成方法依赖向量量化（VQ）将连续特征压缩到低维码本空间，但 VQ 在作用于高维预训练特征时会导致严重的语义退化。CubiD 采用**维度级量化（DQ）**，对每个连续标量独立进行标量量化，映射为 L 个离散级别之一：

$$q_{x,y,i} = \mathrm{Quantize}(z_{x,y,i}; L)$$

这一设计的核心优势在于：**无需重新训练编码器或适配器**，即可将冻结的高维预训练特征（如 DINOv2-B 的 16×16×768 特征图）转换为离散令牌，同时保持连续特征级别的语义质量。Table 3 的验证实验表明，SigLIP2-DQ 在多模态理解任务上（GQA: 63.1 vs 63.2, TextVQA: 59.8 vs 59.6）与连续特征性能几乎一致，而 VQ 则出现显著退化。这为后续在高维语义空间中进行离散生成提供了质量基础。

### 2. 立方掩码策略（Cubic Masking）

这是 CubiD 最关键的范式转变。现有离散扩散方法（如 MaskGIT）以**空间位置**为掩码单元，将整个位置的所有维度同时屏蔽或保留；自回归方法则需要序列化所有 h×w×d 个元素，计算不可行。CubiD 的核心洞察是：**将高维离散表示视为一个统一的 h×w×d 立方空间，对其任意子集——任意位置的任意维度——进行独立掩码**。

训练时，掩码比例 r 从偏向高掩码率的截断高斯分布中采样：

$$r \sim \mathrm{TruncNorm}(\mu=1.0, \sigma, [0, 1.0])$$

模型基于可见部分预测被掩码的令牌，损失函数为：

$$\mathcal{L} = -\mathbb{E}_{\mathbf{q},\mathbf{M}}\left[\sum_{i\in\mathbf{M}} \log p(q_i | \mathbf{q}_{\bar{\mathbf{M}}})\right]$$

推理时，从完全掩码的张量开始，通过固定 T 步（T ≪ h×w×d）迭代去掩码，实现从粗到细的生成。

### 3. 掩码粒度的决定性作用

消融实验（Table 4(b)）提供了因果性证据，验证了逐元素掩码的必要性：

| 掩码策略 | gFID |
|---------|------|
| 按维度掩码（Per-dim） | 120.03 |
| 按空间位置掩码（Per-spatial） | 22.22 |
| **逐元素掩码（Per-element）** | **5.33** |

按维度掩码几乎完全失败，因为模型无法从其他维度的上下文中推断被掩码维度；按空间位置掩码虽优于按维度掩码，但仍无法捕捉同一位置内各维度间的复杂依赖。只有逐元素掩码能够同时从**空间轴和维度轴**学习依赖关系，使模型在部分观测下准确预测缺失元素。Figure 5 的定性对比进一步验证了这一结论：逐元素掩码生成的图像清晰连贯，而其他策略产生严重的纹理伪影或局部不一致。

### 方法谱系与知识库定位

CubiD 属于**掩码离散扩散**（masked discrete diffusion）家族，与 MaskGIT 等方法共享迭代去掩码的生成范式。但其核心差异在于：

- **掩码粒度**：从“空间位置级”升级为“元素级”，这是对离散扩散框架的根本性扩展，使其首次能够处理原生高维表示令牌。
- **令牌表示**：从“低维 VQ 潜在空间”转向“冻结高维预训练特征的维度级量化”，将离散生成与预训练视觉表示的优势打通。
- **生成效率**：通过并行预测所有被掩码元素，将生成步数 T 与特征维度 d 解耦，使高维离散生成在计算上可行。

CubiD 是首个直接在高维（768d）原生表示令牌上进行离散生成的方法，而所有其他方法均使用压缩或低维令牌（通常 ≤32d）。这一差异使得直接数值对比需谨慎，但 CubiD 在 ImageNet 256×256 上达到的 gFID 1.88（CubiD-XXL）以及从 9 亿到 37 亿参数的持续性能提升，表明该范式具有良好的扩展性。

## 整体框架

CubiD 的整体 pipeline 围绕一个核心思想展开：将高维连续表示令牌转化为三维离散张量，并在该张量上执行细粒度的逐元素掩码建模，从而在固定步数内完成高质量生成。整个框架由四个关键模块串联构成，形成“编码→离散化→掩码建模→解码”的端到端流程。

### 从连续特征到离散令牌

给定一张输入图像，**冻结的表示编码器**（Frozen Representation Encoder）首先将其映射为连续特征图。论文默认使用 **DINOv2‑B** 或 **SigLIP2‑B** 作为编码器，二者均输出 $16 \times 16 \times 768$ 的特征张量（Figure 3a）。该编码器在整个训练过程中保持冻结，确保预训练语义空间不被破坏。

随后，**维度级量化器**（Dimension‑wise Quantizer）独立地对特征张量中的每一个标量进行量化，将其映射为 $L$ 个离散级别之一：

$$q_{x,y,i} = \mathrm{Quantize}(z_{x,y,i}; L) \tag{1}$$

其中 $z_{x,y,i}$ 是空间位置 $(x,y)$ 处第 $i$ 维的连续值，$q_{x,y,i} \in \{0, 1, \dots, L-1\}$ 为对应的离散令牌。这一量化方式的关键优势在于**维度独立**——每个维度单独量化，而非对整个向量进行向量量化（VQ），从而最大限度保留预训练特征的语义质量。实验表明，DINOv2‑B 在 $L=8$ 时即可达到与连续特征相当的 rFID（0.57），SigLIP2‑B 在 $L=16$ 时达到同等水平（rFID=0.69，Table 2）；在 LLaVA 多模态理解基准上，维度级量化（DQ）的性能几乎与连续特征持平（GQA: 63.1 vs 63.2; TextVQA: 59.8 vs 59.6），而 VQ 则出现显著退化（Table 3）。

### 立方掩码建模

量化后的离散令牌构成一个 $h \times w \times d$ 的三维张量，这是 CubiD 的核心建模空间。与传统离散扩散方法以空间位置为单元进行掩码不同，CubiD 执行**逐元素掩码**（per‑element masking）：在训练时，从截断高斯分布中采样掩码比例 $r$，

$$r \sim \mathrm{TruncNorm}(\mu=1.0, \sigma, [0, 1.0]) \tag{2}$$

然后在三维张量中**独立地**随机屏蔽任意维度的任意位置（Figure 3b）。这一设计使模型必须从部分观测中同时学习空间轴和维度轴上的复杂依赖关系。

被掩码的令牌送入**双向 Transformer**，其输入处理方式为：将每个空间位置的所有 $d$ 个离散令牌反量化后拼接为一个 $d$ 维向量，通过双向注意力建模空间上下文。Transformer 的每个输出令牌再经过一个 **MLP 预测头**，同时输出该空间位置所有 $d$ 个维度的 $d \times L$ 个 logits，实现对掩码令牌的并行预测。训练目标为掩码位置上的交叉熵损失：

$$\mathcal{L} = -\mathbb{E}_{\mathbf{q},\mathbf{M}}\left[\sum_{i\in\mathbf{M}} \log p(q_i | \mathbf{q}_{\bar{\mathbf{M}}})\right] \tag{3}$$

其中 $\mathbf{M}$ 为被掩码的令牌集合，$\mathbf{q}_{\bar{\mathbf{M}}}$ 为可见令牌。

### 推理与解码

推理过程从全掩码的三维张量开始，按照余弦调度逐步去掩码：每步并行预测所有当前被掩码的令牌，然后随机选择一部分进行去掩码，直至完成全部 $h \times w \times d$ 个令牌的生成（Figure 4）。生成步数 $T$ 固定且远小于 $h \times w \times d$（通常为数百到上千步），使得高维离散生成在计算上可行。

最后，生成的离散令牌通过**预训练的 RAE 解码器**重建为 $256 \times 256$ 像素的图像。该解码器采用噪声增强训练，以提升对生成过程中令牌预测误差的鲁棒性。

### 模块间的数据流

整体数据流可概括为：

1. **输入图像** → 冻结编码器 → $16 \times 16 \times 768$ 连续特征
2. **连续特征** → 维度级量化 → $16 \times 16 \times 768$ 离散令牌（每个维度 $L$ 级）
3. **离散令牌** → 立方掩码（训练时随机掩码，推理时全掩码初始化）→ 双向 Transformer + MLP 预测头 → 预测被掩码令牌
4. **完整离散令牌** → RAE 解码器 → 重建图像

这一 pipeline 的核心瓶颈在于**掩码粒度**的选择：消融实验表明，逐元素掩码（gFID 5.33）大幅优于按维度掩码（gFID 120.03）和按空间位置掩码（gFID 22.22，Table 4b），验证了细粒度掩码对高维令牌生成的必要性。同时，模型展现出良好的规模扩展性——从 CubiD‑L（946M 参数，gFID 5.25）到 CubiD‑XL（1.4B，4.91）再到 CubiD‑XXL（3.7B，4.68），性能持续提升（Table 4e）。

### 补充图表

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of discrete visual generation approaches. (a) Low-dimensional token generation: Both methods operate at the spatial level—autoregressive requires*

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/003_Figure_3.jpg]]
*Figure 3: Overview of Cubic Discrete Diffusion. (a) High-dimensional Token Discretization. Given an input image, a frozen representation encoder extracts continuous tokens, which are then discretized through dimension-wise quantization into h × w × d discrete tokens. (b) Training via Dimension-wise Mask Modeling. During training, we randomly mask tokens across both spatial and dimensional axes of the tensor (white: masked tokens, pink: visible ground truth tokens, other colors: predicted tokens). The transformer learns to predict these masked tokens from the unmasked context, capturing the complex dependencies across both spatial and dimensional axes*

## 核心模块与公式推导

### 3.1 维度级量化（Dimension-wise Quantization）

CubiD 的核心前提是将冻结预训练编码器（如 DINOv2‑B 或 SigLIP2‑B）提取的连续特征图 $\mathbf{z} \in \mathbb{R}^{h \times w \times d}$ 转化为离散令牌张量，同时尽可能保留原始语义质量。与现有方法普遍采用的向量量化（VQ）不同，CubiD 采用**维度级量化**：对每个空间位置 $(x,y)$ 的每个维度 $i$ 独立执行标量量化。

设连续特征值为 $z_{x,y,i}$，量化级别数为 $L$，则离散令牌为：

$$q_{x,y,i} = \mathrm{Quantize}(z_{x,y,i}; L) \tag{1}$$

其中 $\mathrm{Quantize}(\cdot; L)$ 将连续标量映射到 $\{0, 1, \dots, L-1\}$ 的离散索引。这一设计的因果机制在于：高维预训练特征（768 维）的各维度在训练过程中已自然解耦为有意义的语义方向，维度级量化仅引入轻微的标量舍入误差，而 VQ 将整个向量替换为码本中最近邻，会破坏维度间的精细语义结构。实验证据（Table 3）表明，SigLIP2 特征的维度级量化在 GQA 上得分 63.1，与连续特征 63.2 几乎一致；而 VQ 导致显著退化。Table 2 进一步显示，DINOv2‑B 在 $L=8$ 时即可达到连续特征级别的重建质量（rFID 0.57），SigLIP2‑B 则需要 $L=16$。

### 3.2 立方掩码扩散（Cubic Masked Diffusion）

#### 3.2.1 逐元素掩码策略

给定离散令牌张量 $\mathbf{q} \in \{0,\dots,L-1\}^{h \times w \times d}$，CubiD 将其视为统一的**立方建模空间**。训练时，从截断高斯分布采样掩码比例 $r$：

$$r \sim \mathrm{TruncNorm}(\mu=1.0, \sigma, [0, 1.0]) \tag{2}$$

其中 $\mu=1.0$ 使分布偏向高掩码率，强制模型从极少上下文中学习；$\sigma$ 控制分布的集中程度。根据该比例，在 $h \times w \times d$ 张量的所有元素中**独立随机**选择被掩码的令牌——任意空间位置的任意维度都可能被屏蔽，而同一位置的其他维度可能保持可见。

这与标准离散扩散（如 MaskGIT）的根本区别在于**掩码粒度**：标准方法以整个空间位置为单元（per-spatial），将该位置的所有 $d$ 个维度同时掩码或保留；CubiD 的逐元素（per-element）掩码将决策粒度细化到单个维度，使模型必须从部分观测中同时推断空间关系和维度间依赖。消融实验（Table 4b）提供了决定性证据：逐元素掩码达到 gFID 5.33，而按维度掩码（per-dim）为 120.03，按空间位置掩码（per-spatial）为 22.22，验证了细粒度掩码在高维令牌生成中的必要性。

#### 3.2.2 训练目标

令 $\mathbf{M}$ 为被掩码令牌的索引集合，$\mathbf{q}_{\bar{\mathbf{M}}}$ 为可见令牌。训练损失为掩码位置的标准交叉熵：

$$\mathcal{L} = -\mathbb{E}_{\mathbf{q},\mathbf{M}}\left[\sum_{i \in \mathbf{M}} \log p(q_i \mid \mathbf{q}_{\bar{\mathbf{M}}})\right] \tag{3}$$

其中 $p(q_i \mid \mathbf{q}_{\bar{\mathbf{M}}})$ 由双向 Transformer 和 MLP 预测头给出（见 §3.3）。该目标迫使模型从任意部分观测中重建完整张量，隐式学习空间轴与维度轴的联合分布。

#### 3.2.3 推理过程

推理从全掩码张量开始，采用余弦调度逐步去掩码。每步中，模型并行预测所有当前被掩码令牌的 logits，并按调度比例随机选择一部分令牌解除掩码，保留其预测值。生成总步数 $T$ 固定且远小于 $h \times w \times d$（典型值 256–1024 步），解决了自回归方法需要 $O(hwd)$ 步的计算不可行问题。Figure 4 可视化了从全掩码到完整图像的渐进生成过程，呈现出由粗到细的结构涌现。

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/004_Figure_4.jpg]]
*Figure 4: Inference process of CubiD. Top row shows the latent token state (white: masked, pink: unmasked), bottom row shows corresponding decoded images. During generation, CubiD starts from a fully masked tensor (0%) and progressively unmasks tokens until reaching a complete image (100%). At each iteration, the model predicts all masked tokens in parallel and randomly unmasks a subset. The percentages show the progress through generation steps. Generation takes hundreds of iterations regardless of feature dimensionality, making high-dimensional discrete generation computationally feasible. The visualization demonstrates a coarse-to-fine generation process, where early iterations establish overall s...*

### 3.3 架构组件

CubiD 的生成模型由以下模块组成：

1. **令牌反量化与嵌入**：将每个空间位置的 $d$ 个离散索引反量化回连续值，拼接为 $d$ 维向量，作为该位置的输入嵌入。

2. **双向 Transformer**：在 $h \times w$ 的空间网格上应用双向自注意力，建模空间位置间的全局依赖。被掩码位置使用可学习的掩码令牌（learned mask token）填充，消融实验（Table 4c）表明学习型令牌（gFID 5.33）优于固定值（5.56）和随机值（56.38）。

3. **MLP 预测头**：每个 Transformer 输出令牌通过共享的 MLP 映射为 $d \times L$ 维 logits，同时预测该空间位置所有 $d$ 个维度的离散分布。这一设计使模型在一次前向传播中完成对任意掩码子集的预测，无需按维度或空间位置串行解码。

4. **冻结解码器**：生成的离散令牌通过预训练的 RAE 解码器（来自文献 ）重建为图像。解码器采用噪声增强训练以提高对生成误差的鲁棒性，但其重建质量（PSNR ~18 dB）构成当前生成质量的上限。

### 补充图表

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/012_Figure_5.jpg]]
*Figure 5: Qualitative comparison of different masking strategies. Top row: Per-dim masking completely fails, producing severe texture-like artifacts. Middle row: Per-spatial masking generates images with significant local inconsistencies and blurry details. Bottom row: Our per-element masking produces clear, coherent images with fine details. The dramatic quality difference validates that high-dimensional tokens require fine-grained masking across both spatial and dimensional axes*

## 实验与分析

### 核心实验设计

CubiD 的实验体系围绕一个中心论题展开：**逐元素立方掩码是高维离散生成可行的关键**。实验设计从离散化质量验证开始，逐步递进至掩码策略消融、模型规模扩展和最终生成质量评估，形成一条完整的证据链。

#### 实验配置与基础组件

所有实验基于冻结的预训练表示编码器（DINOv2‑B 或 SigLIP2‑B），两者均输出 $16 \times 16 \times 768$ 的特征图。离散化采用维度级量化（DQ），将每个连续标量独立映射为 $L$ 个离散级别。训练时掩码比例 $r$ 从截断高斯分布中采样：

$$r \sim \mathrm{TruncNorm}(\mu=1.0, \sigma, [0, 1.0])$$

该分布偏向高掩码率，迫使模型从极少量可见上下文中学习全局依赖。训练损失为标准交叉熵，仅对被掩码位置计算：

$$\mathcal{L} = -\mathbb{E}_{\mathbf{q},\mathbf{M}}\left[\sum_{i\in\mathbf{M}} \log p(q_i | \mathbf{q}_{\bar{\mathbf{M}}})\right]$$

解码器采用基于 RAE 的重建框架，并引入噪声增强训练以提升对生成误差的鲁棒性。模型规模从 CubiD‑B（~300M）到 CubiD‑XXL（3.7B）共五个配置（Table 1），每个输出 token 经 MLP 预测头产生 $d \times L$ 个 logits，实现单次前向预测该空间位置所有维度的离散分布。

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/005_Table_1.jpg]]
*Table 1: Model sizes and architecture configurations of CubiD*

### 离散化质量验证：维度级量化的语义保真度

在进入生成任务之前，实验首先验证了维度级量化能否保留预训练特征的语义质量。这是整个方法可行性的前提——如果量化本身严重损害表示能力，后续生成就失去了意义。

**Table 2** 展示了量化级别 $L$ 对重建质量（rFID）的影响。DINOv2‑B 在 $L=8$ 时即达到连续特征基线（rFID=0.57），SigLIP2‑B 则在 $L=16$ 时收敛至基线（rFID=0.69）。这一结果表明，高维特征的每个维度仅需极少量离散级别即可保留足够信息，为后续的逐元素掩码提供了离散搜索空间可控的基础。

**Table 3** 进一步验证了量化方法的语义保真度。在 LLaVA 多模态理解基准上，维度级量化（DQ）的 SigLIP2 特征几乎完全保持了连续特征的性能（GQA: 63.1 vs 63.2；TextVQA: 59.8 vs 59.6），而向量量化（VQ）则出现显著退化。这一对比揭示了关键因果机制：VQ 在低维空间中进行全局码本匹配，破坏了高维特征的细粒度语义结构；DQ 的逐维度独立量化则保留了各维度的语义完整性，使得离散令牌仍可用于理解任务。这为“生成与理解可共享同一离散表示”的愿景提供了实证支撑。

### 消融实验：掩码粒度的决定性作用

消融实验的核心发现集中在 **Table 4**，其中掩码粒度的对比结果构成了全文最强的因果证据。

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/006_Table_4.jpg]]
*Table 4: Ablation studies on CubiD design choices. Gray rows indicate best results*

**掩码比例分布**（Table 4a）：标准差 $\sigma=0.10$ 时 gFID 达到最优 5.33。较小的 $\sigma$ 使分布更集中于高掩码率区域，迫使模型从极少上下文中学习；过大的 $\sigma$ 则使掩码率分布趋于均匀，削弱了“从部分观测推断整体”的训练压力。这一结果验证了截断高斯分布设计的合理性。

**掩码粒度**（Table 4b）是本工作的决定性消融：

| 掩码策略 | gFID |
|---------|------|
| 按维度掩码 (per-dim) | 120.03 |
| 按空间位置掩码 (per-spatial) | 22.22 |
| 逐元素掩码 (per-element, CubiD) | **5.33** |

三种策略的 gFID 跨越两个数量级，差距远超一般消融实验的效应量。按维度掩码完全失败（gFID=120.03），因为模型只能从其他维度的空间结构中推断被掩码维度，而维度间缺乏直接的空间对应关系。按空间位置掩码（gFID=22.22）优于按维度掩码但仍远逊于逐元素掩码，因为将整个空间位置的所有维度同时掩码，模型无法学习同一位置内各维度间的依赖关系。逐元素掩码允许模型同时从空间邻居和维度邻居获取上下文，实现了对三维张量中复杂依赖的完整建模。**Figure 5** 的定性对比直观展示了这一差异：按维度掩码产生严重纹理伪影，按空间位置掩码存在局部不一致和模糊细节，逐元素掩码则生成清晰连贯的图像。

**掩码令牌类型**（Table 4c）：可学习掩码令牌（gFID=5.33）优于固定值（5.56）和随机值（56.38），表明模型能够学习到表示“缺失信息”的最优嵌入。

**推理步数**（Table 4d）：gFID 随推理步数增加持续改善，在 512 步后趋于饱和。这表明立方掩码的迭代去掩码过程具有稳定的收敛特性，且实际部署时可在质量与速度间灵活权衡。

**模型规模扩展**（Table 4e）：从 CubiD‑L（946M, gFID=5.25）到 CubiD‑XL（1.4B, 4.91）再到 CubiD‑XXL（3.7B, 4.68），性能持续提升，未观察到饱和迹象。这一扩展行为与大型语言模型的经验一致，暗示高维离散生成可能受益于进一步的规模扩展。

### 主要结果：高维离散生成的最优性能

**Table 5** 报告了 ImageNet 256×256 类条件生成的主要结果。CubiD‑XXL 配合无分类器引导达到 gFID=1.88，是当前离散生成方法中的最优结果。

然而，直接与其他方法进行数值比较需要审慎。CubiD 的潜在维度为 768，而表中其他方法（如 MaskGIT 系列）通常使用 ≤32 维的压缩令牌。高维令牌本身携带更丰富的语义信息，但也意味着更大的生成空间和更高的建模难度。此外，CubiD 的解码器基于 RAE 重建框架，其重建质量（PSNR ~18 dB）构成生成质量的理论上限，与其他使用高保真自编码器的方法相比存在先天劣势。因此，CubiD 的 1.88 gFID 应在“首个直接生成原生高维离散令牌”这一技术定位下理解，而非简单地进行数值排名。

**Table 6** 和 **Table 7** 分别验证了 CubiD 在低维令牌和压缩表示令牌上的表现。在 DC‑AE‑f32c32 的 32 维令牌上（Table 6），CubiD 同样展现出竞争力，表明立方掩码框架具有通用性，不局限于高维场景。在将 768 维特征压缩至 32 维后（Table 7），CubiD 仍能保持合理的生成质量，进一步验证了框架的灵活性。

### 失败模式与局限性

**Figure 5** 的定性对比揭示了逐元素掩码的失败模式边界：当掩码粒度不足以捕捉维度间依赖时（按维度掩码），模型输出退化为无结构的纹理噪声；当掩码粒度过粗而忽略空间上下文时（按空间位置掩码），局部一致性丧失。这些失败模式从反面验证了立方掩码设计的必要性。

更根本的局限性来自表示编码器的重建瓶颈。当前 RAE 解码器的 PSNR 约 18 dB，意味着即使离散令牌完美生成，重建图像仍存在信息损失。这一上限直接限制了 CubiD 与连续扩散方法在极端细节还原上的竞争力。此外，高质量生成需要 512 步以上的迭代推理，相比连续扩散模型的少步采样方案（如蒸馏）存在效率差距。

### 证据强度评估

- **掩码粒度消融**（Table 4b）：效应量极大（gFID 5.33 vs 120.03），实验设计干净，是全文最有力的因果证据。
- **维度级量化语义保真度**（Table 3）：对比清晰，但仅在 LLaVA 基准上验证，对其他理解任务的泛化性需进一步确认。
- **模型扩展行为**（Table 4e）：趋势一致，但最大模型仅 3.7B 参数，是否在更大规模上持续有效尚待验证。
- **主结果对比**（Table 5）：因令牌维度和解码器差异，与其他方法的直接数值比较需谨慎解读。

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/011_Table_3.jpg]]
*Table 3: Understanding performance on LLaVA benchmarks with different quantization methods. Evaluation using SigLIP2 features. VQ: vector quantization, DQ: dimension-wise quantization. DQ maintains continuous-level performance while VQ shows significant degradation*

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/013_Table_5.jpg]]
*Table 5: Discrete generation methods on ImageNet [8] 256×256. Latent Dim denotes the original dimensionality of the latent space (features before vector quantization for low-dimensional methods, before and after dimension-wise quantization for CubiD). Results with superscript ”re” denote rejection sampling. CubiD is the first and only discrete method to directly generate with native high-dimensional representation tokens (768d), while all other methods use compressed or low-dimensional tokens (mostly below 32)*

### 补充图表

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/007_Table.jpg]]
*Table: (b) Masking granularity. Perdim: mask all spatial positions per dimension. Per-spatial: mask all dimensions per position. Perelement: mask independently across all axes*

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/008_Table_2.jpg]]
*Table 2: Effect of quantization levels on reconstruction quality. Both encoders achieve continuous-level performance with appropriate quantization levels (L=8 for DINOv2, L=16 for SigLIP2)*

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/014_Table_6.jpg]]
*Table 6: CubiD on low-dimensional tokens on ImageNet 512×512. Results using DC-AE-f32c32 tokenizer producing 32- dimensional tokens*

![[assets/figures/papers/arxiv_2603_19232_cubid/figures/015_Table_7.jpg]]
*Table 7: CubiD with compressed representation tokens on ImageNet 256×256. Features compressed from 768d to 32d*

## 方法谱系与知识库定位

### 离散生成范式的演进与CubiD的定位

离散视觉生成方法的历史可大致划分为两条技术路线：**自回归生成**与**离散扩散生成**。自回归方法将图像生成建模为序列预测问题，以光栅扫描顺序逐令牌生成，代表工作包括 VQGAN、DALL·E、LlamaGen 等。这类方法的根本瓶颈在于生成步数与令牌总数线性相关——对于低维令牌（如 16×16 空间网格），需要 256 步；一旦扩展到高维令牌（16×16×768 三维张量），所需步数膨胀至约 20 万步，计算上完全不可行。

离散扩散方法（如 **MaskGIT**）通过并行迭代去掩码的方式，将生成步数 T 压缩至远小于令牌总数。然而，现有离散扩散方法均以**空间位置为掩码单元**——将整个空间位置的所有维度同时屏蔽或保留。这在低维令牌场景下是合理的，因为每个空间位置的维度数很少（通常 ≤32），维度间依赖可通过简单的全连接预测头捕获。但当令牌维度扩展至 768 维时，这种粗粒度掩码策略暴露出结构性缺陷：模型无法从部分维度观测中学习同一位置内各维度间的复杂依赖关系，导致生成质量急剧退化（gFID 从 5.33 升至 22.22，见 Table 4b）。

**CubiD 的核心定位**在于填补了“高维离散令牌生成”这一方法空白。其关键创新是将掩码粒度从“按空间位置”下沉至“逐元素”（per-element）——在 h×w×d 三维张量上独立地屏蔽任意维度的任意位置。这一设计使模型能够从任意子集的观测中同时学习空间轴和维度轴上的依赖关系，从而将复杂依赖建模与计算可行性解耦：生成步数 T 固定（通常 256–1024 步），与令牌维度 d 无关。

### 与相关工作的关系网络

**与离散扩散方法的继承与突破**：CubiD 继承了 MaskGIT 等工作的掩码扩散框架（双向注意力 + 迭代去掩码），但在掩码粒度上做出了根本性改变。Figure 1 清晰展示了这一差异：低维令牌生成中，自回归和离散扩散均在空间层面操作；而 CubiD 将操作空间扩展至完整的三维张量。Table 4b 的消融实验提供了决定性证据：逐元素掩码（gFID 5.33）大幅优于按维度掩码（120.03）和按空间位置掩码（22.22），验证了细粒度掩码是解锁高维离散生成的关键。

**与表示学习方法的关系**：CubiD 的方法论建立在预训练视觉表示的基础上，使用冻结的 DINOv2-B 或 SigLIP2-B 作为特征提取器。这使其区别于需要端到端训练自编码器的方法（如 VQGAN、SD-VAE）。维度级量化（Dimension-wise Quantization, DQ）是连接连续表示与离散生成的关键桥梁——与向量量化（VQ）不同，DQ 独立地对每个维度的每个标量进行量化，无需学习码本或训练适配器。Table 3 的证据表明，DQ 在多模态理解任务上保持连续特征级别的性能（GQA: 63.1 vs 63.2），而 VQ 则出现显著退化，这验证了 DQ 在语义保持上的优势。

**与连续扩散方法的关系**：CubiD 的生成质量受限于其解码器（RAE Decoder）的重建能力。当前 RAE 重建的 PSNR 约 18 dB，这构成了生成质量的上限。相比之下，连续扩散方法（如 Stable Diffusion 3、DiT）使用高保真自编码器（如 SD-VAE），重建质量更高，因此生成质量的上限也更高。这是 CubiD 在 gFID 上与连续方法存在差距的结构性原因，而非生成模型本身的能力限制。Table 5 中 CubiD-XXL 达到 gFID 1.88，但需注意这一数值与使用低维令牌的方法不可直接比较——令牌维度的差异直接影响生成难度和表示能力。

### 适用边界

CubiD 的方法设计决定了其适用场景和边界条件：

1. **表示编码器的依赖**：CubiD 的生成质量严格受限于冻结编码器的重建能力。当前 DINOv2-B 和 SigLIP2-B 的重建质量（PSNR ~18 dB）限制了细节还原的上限。若未来出现重建质量更高的表示编码器，CubiD 的生成质量有望直接受益，无需修改生成框架。

2. **令牌维度的下限**：CubiD 的设计优势在高维令牌场景下最为显著。当令牌维度较低（如 32 维）时，逐元素掩码与按空间位置掩码的差异缩小，CubiD 的优势不再突出。Table 6 和 Table 7 分别展示了 CubiD 在低维令牌和压缩表示令牌上的表现，可作为适用性参考。

3. **推理效率的权衡**：高质量生成通常需要 512–1024 步迭代（Table 4d 显示 512 步后性能趋于饱和），相比连续扩散模型（通常 20–50 步）推理更慢。这使 CubiD 更适合对生成质量要求高、对推理延迟容忍度较大的场景。

4. **多模态统一的潜力**：CubiD 的离散令牌天然适合与语言模型集成，这是连续扩散方法难以实现的。维度级量化保持了语义质量（Table 3），使得生成的离散令牌可直接用于下游理解任务，为统一多模态架构提供了技术基础。

### 局限与开放问题

**当前局限**：

1. **重建质量瓶颈**：RAE 解码器的重建质量（PSNR ~18 dB）是生成质量的结构性上限。提升表示自编码器的重建质量是突破这一瓶颈的关键方向，但需注意更高保真的解码器可能引入更多计算开销。

2. **推理步数**：尽管 T ≪ hwd，但 512–1024 步的推理成本仍显著高于连续扩散模型。当前尚未探索蒸馏或渐进式去掩码等加速技术在该框架下的适用性。

3. **条件生成能力**：当前 CubiD 主要验证了类别条件生成，在文本条件生成、图像编辑等更复杂的条件任务上的表现尚未充分探索。

**开放问题**：

1. **解码器改进**：能否设计专门针对高维离散令牌的解码器，在保持语义一致性的同时提升重建质量？例如，在解码器中引入生成式先验或对抗训练。

2. **加速技术迁移**：连续扩散模型的加速技术（如一致性蒸馏、渐进式蒸馏）能否适配离散扩散框架？由于离散令牌的去掩码过程与连续去噪过程存在本质差异，直接迁移可能面临挑战。

3. **多模态扩展**：CubiD 能否有效扩展到文本条件生成或其他多模态任务？其离散令牌与语言模型的天然兼容性为这一方向提供了基础，但需要验证跨模态条件下的生成质量和可控性。

4. **表示编码器的选择**：Table 4f 显示 DINOv2 和 SigLIP2 在生成质量上存在差异，但未深入分析不同表示编码器对生成特性的影响。未来可探索更适合生成任务的表示学习方法，或将表示学习与生成训练进行弱耦合联合优化。

5. **掩码策略的理论分析**：当前掩码比例分布（截断高斯分布）的选择基于经验消融（Table 4a），缺乏理论层面的分析。理解掩码比例与学习难度、生成质量之间的理论关系，可能指导更优的掩码调度策略设计。

## 原文 PDF

![[paperPDFs/arxiv_2026/Cubic_Discrete_Diffusion_Discrete_Visual_Generation_on_High_Dimensional_Representation_Tokens.pdf]]