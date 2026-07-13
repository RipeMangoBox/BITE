---
title: "Efficient-LVSM: Faster, Cheaper, and Better Large View Synthesis Model via Decoupled Co-Refinement Attention"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Efficient_LVSM_Faster_Cheaper_and_Better_Large_View_Synthesis_Model_via_Decouple_f97270a5835a.pdf
project_link: "https://efficient-lvsm.github.io/"
code_link: null
aliases:
- Efficient-LVSM
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 将输入视图处理与目标视图生成解耦为独立的双流架构，在目标解码器中引入自注意力与交叉注意力交替的共精炼机制，并借助KV缓存实现增量推理。
primary_logic: 通过按视图独立处理输入（视图内自注意力）并让目标令牌交叉注意力查询输入特征，模型实现线性复杂度、异构信息专门化以及KV缓存，显著提升效率与泛化性；层间共精炼进一步融合多层次视觉特征，提高重建质量。
claims:
- Efficient-LVSM在RealEstate10K上以2个输入视图达到29.86 dB PSNR，超过LVSM 0.2 dB。
- 计算复杂度从 O(N²M) 降至 O(NM+N)，推理速度提升4.4倍，训练收敛速度提升2倍。
- 编码器-解码器共精炼结构比仅使用交叉注意力的变体提高1.28 dB PSNR。
- 在64个输入视图下，使用KV缓存的推理延迟加速达66.7倍。
---

# Efficient-LVSM: Faster, Cheaper, and Better Large View Synthesis Model via Decoupled Co-Refinement Attention

> [!tip] 核心洞察
> 通过按视图独立处理输入（视图内自注意力）并让目标令牌交叉注意力查询输入特征，模型实现线性复杂度、异构信息专门化以及KV缓存，显著提升效率与泛化性；层间共精炼进一步融合多层次视觉特征，提高重建质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | Efficient-LVSM：基于解耦共精炼注意力的高效大视角合成模型 |
| 英文题名 | Efficient-LVSM: Faster, Cheaper, and Better Large View Synthesis Model via Decoupled Co-Refinement Attention |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=tzBPOXJ3QC) · [Project](https://efficient-lvsm.github.io/) · [paper](https://arxiv.org/abs/2403.14627) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Efficient-LVSM |
| Dataset | RealEstate10K, ABO, GSO |

> [!tip] 效果简介
> - RealEstate10K (场景级) 上，PSNR (res-512) 29.86 vs 29.53 (LVSM Dec-Only) (+0.33 dB)；SSIM (res-512) 0.905 vs 0.904 (LVSM Dec-Only) (+0.001)。
> - ABO (物体级) 上，PSNR (Res-512) 32.65 vs 32.10 (LVSM Dec-Only) (+0.55 dB)。
> - GSO (物体级) 上，PSNR (Res-512) 32.92 vs 32.36 (LVSM Dec-Only) (+0.56 dB)。

## 概要

大视角合成（Large View Synthesis）旨在从稀疏输入视图直接生成任意新视角的图像。现有前馈方法 **LVSM**（Jin et al., 2025）采用全自注意力机制，将所有输入视图令牌与目标视图令牌拼接为单一序列进行统一建模。这一设计带来了两个根本性瓶颈：

1. **计算效率低下**：注意力复杂度随输入视图数量呈二次方增长（$O(N^2)$），严重制约了多视图场景下的训练与推理速度。
2. **表示能力受限**：输入视图（编码已知场景结构）与目标视图（解码未知新视角）的令牌承载着异构信息，却被迫共享相同的注意力参数，导致特征提取与生成的耦合，限制了模型的表达潜力。

针对上述瓶颈，本文提出 **Efficient-LVSM**，一种基于解耦共精炼注意力的高效大视角合成模型。其核心设计包括：

- **解耦双流架构**：将输入视图处理与目标视图生成分离为独立的编码器与解码器。输入编码器对每个视图独立执行视图内自注意力，目标解码器则通过自注意力与交叉注意力交替查询输入特征，实现异构令牌的专门化处理。
- **共精炼机制**：编码器各层特征逐层传递至解码器对应层，使目标令牌能够融合从细粒度细节到高层语义的多层次视觉信息，显著提升重建质量。
- **KV缓存与增量推理**：由于输入视图特征与目标视图生成解耦，模型可缓存输入视图的键值对，在新增输入或目标视图时实现近恒定成本的增量推理。

实验结果表明，Efficient-LVSM 在保持甚至超越现有方法重建质量的同时，大幅提升了效率。在 RealEstate10K 场景级数据集上，以2个输入视图达到 **29.86 dB PSNR**，超过 LVSM 0.2 dB；计算复杂度从 $O(N^2)$ 降至线性 $O(N)$，推理速度提升 **4.4倍**，训练收敛速度提升 **2倍**。在64个输入视图的极端场景下，基于KV缓存的推理延迟加速达 **66.7倍**。此外，该架构在物体级数据集（ABO、GSO）上同样展现出显著的性能优势与泛化能力。

### 大视角合成与潜在空间范式

新视角合成（Novel View Synthesis, NVS）旨在从稀疏的输入视图中生成任意目标视角下的场景渲染。传统方法如基于场景优化的 NeRF 系列虽能生成高质量结果，但推理速度慢、泛化能力弱。近年来，前馈式大视角合成模型（Large View Synthesis Model, LVSM）**LVSM**（Jin et al., 2025）将这一任务重新定义为潜在空间下的图像到图像翻译问题：编码器将输入视图映射为潜在令牌，Transformer 在潜在空间中进行信息融合，解码器再将融合后的潜在表示渲染为目标视图。

这一范式的核心优势在于端到端的前馈推理，无需逐场景优化，且能利用大规模数据训练获得强泛化能力。然而，LVSM 的全自注意力设计在效率与表示能力上存在根本性瓶颈，限制了其向更大规模输入和实际部署的扩展。

### LVSM 的全自注意力瓶颈

LVSM 采用 decoder-only 架构，将所有输入视图令牌与目标视图令牌拼接为一个长序列，通过全自注意力（full self-attention）统一处理。这一设计带来两个关键问题：

**计算复杂度的二次方增长。** 设输入视图数为 $N$，每个视图的令牌数为 $M$，目标视图令牌数为 $1$，则每层注意力的计算复杂度为 $O(M(N+1)^2)$。当输入视图数量增加时，计算量呈二次方膨胀，严重制约了多视图场景下的推理效率。论文明确指出，这一复杂度是“与输入视图数量成二次方”的关系。

**异构令牌的强制参数共享。** 输入视图令牌编码的是场景的几何与内容信息，而目标视图令牌则代表待生成视角的结构先验——两者在语义上本质不同。全自注意力却将它们置于同一参数空间下处理，导致模型无法为异构信息来源学习专门的表示，限制了特征提取的精度与泛化能力。

### 解耦双流的动机与核心洞察

针对上述瓶颈，Efficient-LVSM 的核心洞察是：**将输入视图处理与目标视图生成解耦为独立的双流架构**。具体而言：

- **输入编码器**对每个输入视图独立执行视图内自注意力（intra-view self-attention），复杂度降至 $O(NM)$，且不跨视图交互，天然支持任意数量的输入视图和 KV 缓存。
- **目标解码器**先通过自注意力聚合目标视图内部结构，再通过交叉注意力从编码器特征中查询输入信息，复杂度为 $O(NM+N)$。
- 这一解耦实现了 **线性复杂度**、**异构信息专门化**（编码器与解码器使用独立参数），以及 **KV 缓存驱动的增量推理**——输入视图的键值对可被缓存复用，新增目标视图时无需重新计算输入特征。

此外，论文进一步提出 **双流共精炼（co-refinement）** 机制：将编码器各中间层的特征逐层传递给解码器对应层，使解码器能同时利用浅层的细粒度细节与深层的语义上下文，弥补了普通编码器-解码器结构中中间层特征被浪费的问题。

### 效率与质量的双重目标

Efficient-LVSM 的设计同时追求效率与质量的提升。在效率维度，线性复杂度使推理速度提升 **4.4 倍**，训练收敛速度提升 **2 倍**；在 64 个输入视图下，KV 缓存带来 **66.7 倍**的延迟加速。在质量维度，解耦架构配合共精炼与 REPA 蒸馏，在 RealEstate10K 上以 2 个输入视图达到 **29.86 dB PSNR**，超越 LVSM 0.2 dB，在 ABO 和 GSO 物体级数据集上分别领先 0.55 dB 和 0.56 dB。

### 与现有方法的定位

相较于基于 3D 高斯泼溅的 **pixelSplat** 和 **MVSplat**，Efficient-LVSM 延续了 LVSM 的潜在空间范式，避免显式 3D 重建的几何约束，同时通过架构创新弥补了效率短板。相较于同样采用 Transformer 的 **GS-LRM**（Zhang et al., 2024），Efficient-LVSM 专注于视图合成而非 3D 原语预测，在场景级与物体级任务上展现出更强的泛化性。

## 核心方法与创新机理

Efficient-LVSM 的核心创新在于将 LVSM 的全自注意力范式彻底重构为**解耦双流共精炼架构**，从根本上解决了原有方法在计算效率与表示能力上的双重瓶颈。

### 瓶颈诊断：全自注意力的代价

LVSM 采用 Decoder-Only 架构，将所有输入视图令牌与目标视图令牌拼接为单一序列，施加全自注意力。这一设计带来两个致命缺陷：

1. **计算复杂度与视图数量呈二次方关系**：每层复杂度为 $O(M(N+1)^2)$，其中 $N$ 为输入视图数，$M$ 为目标视图数。当输入视图增多时，计算开销急剧膨胀，严重制约了多视图场景下的可扩展性。
2. **异构令牌强制共享参数**：输入令牌（携带已知视图的几何与纹理信息）与目标令牌（需要合成未知视角）在本质上承载不同的信息类型，但全自注意力迫使它们在同一参数空间中交互，导致表示纠缠，限制了模型对各自信息的专门化建模能力。

### 解耦双流：从二次到线性的复杂度跃迁

针对上述瓶颈，Efficient-LVSM 将单流全自注意力拆分为**输入编码器**与**目标解码器**两个独立模块：

- **输入编码器**对每个输入视图独立执行视图内自注意力（Intra-View Self-Attention），不进行跨视图交互。其更新公式为：

$$\mathbf{S_i}^l = \mathbf{S_i}^{l-1} + \mathrm{Self-Attn}_{\mathrm{input}}^l(\mathbf{S_i}^{l-1}); \quad \mathbf{S_i}^l = \mathbf{S_i}^l + \mathrm{FFN}_{\mathrm{input}}^l(\mathbf{S_i}^l)$$

这一设计将编码器每层复杂度降至 $O(N)$，同时保持了各输入视图的独立性，为后续 KV 缓存与增量推理奠定了基础。

- **目标解码器**通过交叉注意力从编码器输出中查询信息，其基础形式为：

$$\mathbf{T_j}^l = \mathbf{T_j}^l + \mathrm{Cross-Attn}_{\mathrm{target}}^l(\mathbf{T_j}^l, \mathbf{S_1}^L, ..., \mathbf{S}_N^L)$$

解码器每层复杂度为 $O(NM)$，整体架构复杂度从 $O(N^2M)$ 降至 $O(NM + N)$，实现了从二次到线性的根本性转变。

### 共精炼机制：多层特征的深度融合

简单的编码器-解码器结构存在一个隐蔽缺陷：解码器仅能访问编码器末层输出，中间层的细粒度特征被白白浪费。Efficient-LVSM 引入**层间共精炼（Co-Refinement）**机制，将编码器各层特征逐层传递至解码器对应层：

$$\begin{array}{rl} \mathbf{T_j}^l = \mathbf{T_j}^{l-1} + \mathrm{Self-Attn}_{\mathrm{target}}^l(\mathbf{T_j}^{l-1}) \\ \mathbf{T_j}^l = \mathbf{T_j}^l + \mathrm{Cross-Attn}_{\mathrm{target}}^l(\mathbf{T_j}^l, \mathbf{S_1}^l, ..., \mathbf{S}_N^l) \\ \mathbf{T_j}^l = \mathbf{T_j}^l + \mathrm{FFN}_{\mathrm{input}}^l(\mathbf{T_j}^l) \end{array}$$

解码器每层先通过自注意力聚合目标视图内部结构，再以同层编码器特征作为交叉注意力的查询目标。这使得解码器能够同时利用编码器浅层的纹理细节与深层的语义上下文，显著提升了重建质量。消融实验证实，共精炼结构相比仅使用交叉注意力的变体**提升了 1.28 dB PSNR**。

### KV 缓存：增量推理的工程突破

由于输入编码器对每个视图独立处理，输入视图的键值对可在首次计算后缓存。当新增输入视图或生成新目标视图时，模型仅需计算增量部分，实现了**近恒定成本**的增量推理。在 64 个输入视图的场景下，KV 缓存带来 **66.7 倍的推理加速**（延迟从 9231 ms 降至 138.43 ms），使模型在多视图场景中具备实际部署的可行性。

### 辅助创新：REPA 蒸馏

为进一步提升表示质量，Efficient-LVSM 在训练阶段引入 REPA 蒸馏，利用预训练的 DINOv3 视觉编码器作为教师，通过最大化补丁级特征相似度来增强学生模型的隐藏层特征。该蒸馏仅在训练时使用，推理阶段不增加任何开销，为模型带来 **0.8 dB PSNR** 的增益。

综上，Efficient-LVSM 通过解耦双流设计实现了复杂度从二次到线性的跃迁，通过共精炼机制充分挖掘了多层特征潜力，并通过 KV 缓存解锁了高效增量推理能力，构成了一个在速度、质量与可扩展性三个维度上全面超越 LVSM 的统一框架。

Efficient-LVSM 采用**编码器-解码器解耦双流架构**，从根本上改变了此前 LVSM 将输入视图令牌与目标视图令牌拼接后统一送入全自注意力的范式。其核心设计原则是：**输入视图处理与目标视图生成在信息流和参数上完全解耦**，从而消除异构令牌之间的强制共享，并为增量推理提供结构基础。

### 输入表示与令牌化

模型接收两类输入：**带位姿的输入图像**和**目标视图的 Plücker 射线**。两者分别经过图像分词器（image tokenizer）和射线分词器（ray tokenizer）被切分为固定大小的 patch 令牌。具体地，图像以 $8\times8$ 的 patch 大小进行 patchify，每个 patch 被映射为维度为 1024 的隐藏特征向量；Plücker 射线则以相同粒度编码目标视图的空间位置信息。这一阶段为后续的双流处理提供了统一的令牌表示。

### 双流处理管道

Efficient-LVSM 的处理管道由两个功能独立、参数分离的模块组成：

1. **输入编码器**：负责从输入视图令牌中提取内容与几何上下文。每个输入视图的令牌**独立地**通过视图内自注意力进行更新，不同视图之间不存在跨视图的信息交互。这一定位使得编码器复杂度相对于输入视图数量 $N$ 呈线性增长，同时保证了输入视图的独立性，为后续 KV 缓存机制奠定基础。

2. **目标解码器**：负责合成目标视图。解码器对目标令牌依次执行**自注意力**（聚合目标视图内部结构）和**交叉注意力**（从编码器输出中查询输入视图信息）。自注意力使目标令牌之间建立空间一致性，交叉注意力则将输入视图的几何与纹理信息注入目标表示。

### 共精炼连接

与传统的 vanilla 编码器-解码器结构不同，Efficient-LVSM 引入了**逐层共精炼机制**：编码器每一层的输出特征被直接传递至解码器的对应层，而非仅传递末层特征。解码器在每一层都从编码器的同层特征中进行交叉注意力查询。这一设计使解码器能够同时利用编码器浅层的细粒度细节和深层的丰富语义，显著提升了重建质量。

### 辅助模块与推理优化

在训练阶段，模型引入 **REPA 蒸馏**：利用预训练的 DINOv3 视觉编码器作为教师，通过一个 3 层 MLP 投影头将学生模型的隐藏层特征与教师特征对齐。该投影头在推理时被丢弃，不引入额外计算开销。在推理阶段，输入编码器生成的键值对可被**缓存**，当新增输入视图或生成新目标视图时，只需计算增量部分，实现近乎恒定成本的增量推理。

### 复杂度对比

相较于 LVSM 解码器仅用模式（复杂度 $O(M(N+1)^2)$，其中 $M$ 为目标视图数），Efficient-LVSM 的每层复杂度降至 $O(NM+N)$：编码器为 $O(N)$，解码器为 $O(NM)$。这一线性复杂度特性使得模型在输入视图数量增加时仍保持高效，为大规模视图合成场景提供了可扩展的基础。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_tzBPOXJ3QC/figures/001_Figure_1.jpg]]
*Figure 1: Latent Novel View Synthesis Paradigms Comparison. The proposed decoupled architecture disentangles the input and target streams with lower*

Efficient-LVSM 的核心架构由五个关键模块构成：输入编码器、目标解码器、双流共精炼连接、REPA 蒸馏和 KV 缓存。以下逐一阐述其设计逻辑与数学形式。

### 输入编码器：视图内自注意力

输入编码器的设计目标是**保持不同输入视图的独立性**，同时降低计算复杂度。与 LVSM 将所有输入和目标令牌拼接后执行全自注意力不同（式 1），Efficient-LVSM 将自注意力的范围限制在每个输入视图内部的 patch 之间。

LVSM 的全自注意力操作可形式化为：

$$
\mathbf{V_i}^l = \operatorname{concat}(\mathbf{S_1}^l, ..., \mathbf{S}_N^l, \mathbf{T_j}^l); \quad \mathbf{V_i}^l = \mathbf{V_i}^{l-1} + \operatorname{Self-Attn}_{\mathrm{full}}^l(\mathbf{V_i}^{l-1})
$$

其中 $\mathbf{S_i}$ 表示第 $i$ 个输入视图的令牌序列，$\mathbf{T_j}$ 表示第 $j$ 个目标视图的令牌序列。这种设计导致计算复杂度为 $O(M(N+1)^2)$（$M$ 为每视图 patch 数，$N$ 为输入视图数），且输入与目标令牌共享注意力参数，造成异构信息的纠缠表示。

Efficient-LVSM 的输入编码器则对每个输入视图独立执行自注意力：

$$
\mathbf{S_i}^l = \mathbf{S_i}^{l-1} + \mathrm{Self\text{-}Attn}_{\mathrm{input}}^l(\mathbf{S_i}^{l-1}); \quad \mathbf{S_i}^l = \mathbf{S_i}^l + \mathrm{FFN}_{\mathrm{input}}^l(\mathbf{S_i}^l)
$$

这一设计的直接收益是：编码器每层复杂度降至 $O(N)$（视图间无交互），且为后续 KV 缓存机制提供了天然的结构支持——每个视图的键值对可独立缓存，无需因新增视图而重新计算已有视图的特征。

### 目标解码器：自注意力与交叉注意力交替

目标解码器采用**自注意力-交叉注意力交替**的结构，而非 LVSM 的纯自注意力范式。其基础形式为：目标令牌先通过交叉注意力从编码器末层输出中查询信息：

$$
\mathbf{T_j}^l = \mathbf{T_j}^l + \mathrm{Cross\text{-}Attn}_{\mathrm{target}}^l(\mathbf{T_j}^l, \mathbf{S_1}^L, ..., \mathbf{S}_N^L); \quad \mathbf{T_j}^l = \mathbf{T_j}^l + \mathrm{FFN}_{\mathrm{input}}^l(\mathbf{T_j}^l)
$$

其中 $\mathbf{S_1}^L, ..., \mathbf{S}_N^L$ 为编码器末层（第 $L$ 层）的输出。解码器每层复杂度为 $O(NM)$，整体复杂度从 LVSM 的二次方 $O(N^2M)$ 降至线性 $O(NM+N)$。

### 双流共精炼连接

上述基础编码器-解码器结构存在一个关键缺陷：编码器中间层的隐藏特征被浪费，解码器仅能访问末层的压缩表示。双流共精炼机制通过**层对层连接**解决此问题——将编码器第 $l$ 层的输出直接传递给解码器第 $l$ 层的交叉注意力模块：

$$
\begin{array}{rl}
\mathbf{T_j}^l = \mathbf{T_j}^{l-1} + \mathrm{Self\text{-}Attn}_{\mathrm{target}}^l(\mathbf{T_j}^{l-1}) \\
\mathbf{T_j}^l = \mathbf{T_j}^l + \mathrm{Cross\text{-}Attn}_{\mathrm{target}}^l(\mathbf{T_j}^l, \mathbf{S_1}^l, ..., \mathbf{S}_N^l) \\
\mathbf{T_j}^l = \mathbf{T_j}^l + \mathrm{FFN}_{\mathrm{input}}^l(\mathbf{T_j}^l)
\end{array}
$$

该设计的核心洞察在于：编码器浅层保留细粒度细节，深层富含语义上下文，解码器通过逐层查询可同时融合多粒度视觉特征。消融实验证实，共精炼结构相较仅使用交叉注意力的变体提升 **1.28 dB PSNR**（Table 6(a)），特征图可视化也表明共精炼能捕获更多目标视图的细节（Figure 3）。

### REPA 蒸馏

REPA（Representation Alignment）蒸馏在训练阶段引入预训练视觉编码器（DINOv3）作为教师，通过最大化教师特征与学生隐藏层投影特征之间的 patch 级相似度来增强表示学习：

$$
\mathcal{L}_{REPA} = \frac{1}{N} \sum_{i=1}^{N} \sin(f(\mathbf{I}), h_{\phi}(\mathbf{X_k}))
$$

其中 $f(\mathbf{I})$ 为教师编码器对输入图像 $\mathbf{I}$ 提取的特征，$h_{\phi}$ 为可训练的 MLP 投影层（3 层），$\mathbf{X_k}$ 为学生模型第 $k$ 层的隐藏特征。该模块**仅在训练时使用**，推理时投影层和教师编码器均被丢弃，不引入额外计算开销。消融实验表明 REPA 为 Efficient-LVSM 带来 **0.8 dB PSNR** 增益（Table 6(b)）。

### KV 缓存与增量推理

解耦架构使得输入视图的键值对可被缓存复用。当新增输入视图或生成新目标视图时，只需计算增量部分的注意力，已有视图的 KV 对直接从缓存读取。实验数据显示，在 64 个输入视图下，KV 缓存带来 **66.7 倍**的推理加速（延迟从 9231 ms 降至 138.43 ms，Table 8），实现了近恒定成本的增量推理。

## 实验与关键发现

### 核心性能对比

Efficient-LVSM 在场景级和物体级基准上均以显著更低的计算开销超越了前馈大视角合成方法 LVSM。在 RealEstate10K 场景级测试中，以 2 个输入视图、512 分辨率评估，Efficient-LVSM 达到 **29.86 dB PSNR**，超过 LVSM Decoder-Only 约 0.33 dB（Table 2）；在 ABO 和 GSO 物体级数据集上，PSNR 分别达到 **32.65 dB** 和 **32.92 dB**，较 LVSM Decoder-Only 分别高出 0.55 dB 和 0.56 dB（Table 3）。值得注意的是，这些质量增益是在训练时间减半（仅需 3 天 / 64 张 A100 GPU）的前提下实现的。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_tzBPOXJ3QC/figures/006_Table_2.jpg]]
*Table 2: Scene-level View Synthesis Quality. We test on the same validation set proposed in pixelSplat*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_tzBPOXJ3QC/figures/007_Table_3.jpg]]
*Table 3: Object-level View Synthesis Quality. We test at 512 and 256 resolution on both input and rendering. ”Enc” means encoder and ”Dec” means decoder*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_tzBPOXJ3QC/figures/003_Table.jpg]]
*Table: 2.2 ANALYSIS OF LVSM’S FULL SELF-ATTENTION PARADIGM*

效率方面的优势更为突出。Efficient-LVSM 将每层计算复杂度从 LVSM 的 $O(M(N+1)^2)$ 降至 $O(NM+N)$，其中 $N$ 为输入视图数，$M$ 为每视图令牌数。在 64 个输入视图的推理场景下，借助 KV 缓存机制，延迟从 LVSM Decoder-Only 的 9231 ms 降至 **138.43 ms**，加速比约 **66.7 倍**（Table 8）；整体推理速度提升约 4.4 倍，训练收敛速度提升约 2 倍。

### 消融研究

消融实验系统性地验证了各设计组件的贡献（Table 6）：

- **共精炼架构**：将纯交叉注意力解码器替换为自注意力-交叉注意力交替的共精炼结构，带来 **1.28 dB PSNR** 的显著增益（26.25 dB vs. 24.18 dB）。这表明解码器内部的视图内自注意力与跨层特征融合对重建质量至关重要。
- **REPA 蒸馏**：引入 DINOv3 特征蒸馏后，PSNR 进一步提升 **0.8 dB**（26.81 dB vs. 26.01 dB）。蒸馏仅在训练时使用，推理时无额外开销。Smooth L1 损失在实验中表现优于其他损失函数。
- **模型规模**：将编码器和解码器各扩展至 12 层时，PSNR 达到 28.32 dB，验证了架构的可扩展性。

在架构变体对比中（Table 7），完整双流共精炼设计在 PSNR（26.02 dB）、延迟（17.58 ms）和显存占用三个维度上均优于注意力掩码方案和 MMDiT 风格变体。LVSM w/ Mask 变体虽在理论上可复现解耦数据流，但需定制 CUDA 内核才能实现实际加速，目前缺乏工程支持。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_tzBPOXJ3QC/figures/016_Table_7.jpg]]
*Table 7: Comparison of Different Architectures*

### 效率与泛化性分析

Efficient-LVSM 的效率优势源于两个关键机制。其一，输入编码器对每个视图独立执行视图内自注意力，复杂度与输入视图数呈线性关系，且天然支持 KV 缓存——输入视图的特征键值对可被缓存，后续目标视图生成仅需计算交叉注意力部分。其二，目标解码器无需重复处理输入令牌，避免了 LVSM 中因新目标视图加入而重算全部令牌的冗余。

在泛化性方面，Efficient-LVSM 对输入视图数量的变化表现出良好的零样本鲁棒性（Figure 7c）。当输入视图数偏离训练设置时，性能下降幅度明显小于 LVSM，这归因于解耦架构中编码器对每个视图的独立处理——新增或移除输入视图不会破坏已编码视图的特征表示。

### 失败模式与局限

尽管 Efficient-LVSM 在效率和质量上取得了显著进步，论文明确指出以下局限：

1. **工业部署差距**：大型 Transformer 架构在产业级应用中的延迟和内存约束依然严峻。当前模型仍属学术概念验证，需通过模型压缩、量化或知识蒸馏等手段进一步小型化。
2. **定制内核缺失**：LVSM w/ Mask 等竞争性变体虽在理论上可行，但因缺乏定制 CUDA 内核而无法实现实际加速，这限制了架构比较的工程公平性。
3. **大规模泛化未验证**：现有实验集中在 RealEstate10K、ABO、GSO 等受控数据集上，解耦共精炼架构在更大规模、更多样化的真实场景数据上的泛化能力尚待检验。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_tzBPOXJ3QC/figures/014_Table_5.jpg]]
*Table 5: Ablation Study of REPA Distillation*

## 定位与知识库关联

### 与LVSM的继承与突破

Efficient-LVSM 直接继承自 **LVSM**（Jin et al., 2025）的大视角合成范式，后者首次将前馈潜在空间视图合成推至场景级与物体级多视图生成。然而，LVSM 的 decoder-only 架构采用全自注意力（full self-attention），将所有输入视图令牌与目标视图令牌拼接为单一序列处理，导致两大瓶颈：

1. **表征纠缠**：输入视图的内容/几何特征与目标视图的待合成特征共享同一组注意力参数，迫使异构信息通过统一变换，限制了模型对两类令牌的专门化建模能力。
2. **计算与存储代价**：每层复杂度为 $O(M(N+1)^2)$（$N$ 为输入视图数，$M$ 为目标视图数），随输入视图数量呈二次方增长，且每次生成新目标视图均需重新计算所有令牌，无法支持增量推理。

Efficient-LVSM 的核心突破在于将全自注意力范式**解耦为双流架构**：输入编码器仅执行视图内自注意力（$O(N)$ 复杂度），目标解码器通过自注意力与交叉注意力的交替机制查询输入特征（$O(NM)$ 复杂度，见表1）。这一解耦不仅将复杂度从二次降至线性，更使得输入视图的键/值对可被缓存（KV-Cache），实现近恒定成本的增量推理——在64个输入视图下加速达66.7倍（Table 8）。

### 与其他视图合成方法的定位

在场景级视图合成领域，Efficient-LVSM 与以下代表性工作形成差异化竞争：

- **pixelSplat** 与 **MVSplat**：基于显式几何（3D高斯泼溅）的场景级方法，依赖多视图立体匹配构建显式场景表示，在稀疏视图下表现受限。Efficient-LVSM 则通过潜在空间的前馈生成绕开显式几何重建，在仅2个输入视图的条件下即可达到29.86 dB PSNR（RealEstate10K，Table 2），展现了稀疏输入下的强鲁棒性。

- **GS-LRM**（Zhang et al., 2024）：基于Transformer的大型重建模型，预测3D高斯原语以实现新视图合成。Efficient-LVSM 在RealEstate10K上以1.7 dB PSNR的优势显著超越该方法（参见分析中的实验证据），且不依赖显式3D表示，避免了高斯原语优化中的几何伪影。

在物体级视图合成上，Efficient-LVSM 在ABO和GSO数据集上分别达到32.65 dB和32.92 dB PSNR（Table 3），均超越LVSM decoder-only基线0.5 dB以上，验证了双流解耦架构在跨场景与跨物体级别的泛化能力。

### 适用边界与局限

尽管 Efficient-LVSM 在效率与质量上取得了显著突破，其适用边界与局限仍值得审慎评估：

1. **产业部署的延迟与内存约束**：模型基于24层Transformer（12层编码器+12层解码器），隐藏维度1024，在A100 80G GPU上训练需3天（64卡）。尽管推理速度已大幅优化，将此类大规模Transformer架构部署至边缘设备或实时应用仍面临严格的延迟与内存限制，需要模型压缩、量化或知识蒸馏等进一步创新。

2. **学术验证与工业落地的距离**：当前实验主要基于RealEstate10K（室内场景）、ABO与GSO（物体）等相对受控的数据集，模型在更大规模、更多样化的真实场景（如室外驾驶、动态场景）中的泛化能力尚未充分验证。论文本身亦明确指出该工作仍是面向学术的概念验证，离广泛的工业落地尚有距离。

3. **KV缓存的硬件适配**：尽管KV-Cache在理论上实现了显著的增量推理加速，但论文中未详细讨论缓存管理策略在长序列或多轮交互场景下的内存占用峰值。此外，LVSM w/ Mask变体理论上可复现解耦数据流，但需定制CUDA内核才能实现实际加速，这一工程挑战尚未解决。

### 开放问题

基于当前工作的边界，以下开放问题值得后续研究关注：

- **小型化与部署**：如何通过模型压缩、网络量化和知识蒸馏将Efficient-LVSM转化为适合工业部署的轻量版本，同时保持解耦共精炼带来的质量优势？
- **定制化高效算子**：LVSM w/ Mask等变体在理论上可模拟解耦数据流，但实际加速依赖定制CUDA内核。如何设计此类内核以释放解耦架构的全部潜力？
- **大规模真实场景泛化**：在更大规模、更多样化的真实场景数据（如自动驾驶、AR/VR环境）上，解耦共精炼架构的泛化能力是否依然稳健？输入视图数量与场景复杂度的关系如何影响模型性能？
- **多模态扩展**：当前模型仅依赖RGB图像与Plücker射线作为输入，未来是否可将深度、语义或文本等多模态信息融入双流架构，以进一步提升稀疏视图下的合成质量？

## 原文 PDF

![[paperPDFs/ICLR_2026/Efficient_LVSM_Faster_Cheaper_and_Better_Large_View_Synthesis_Model_via_Decouple_f97270a5835a.pdf]]
