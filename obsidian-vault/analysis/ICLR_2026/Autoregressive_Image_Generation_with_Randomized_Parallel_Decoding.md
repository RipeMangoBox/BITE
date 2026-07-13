---
title: "Autoregressive Image Generation with Randomized Parallel Decoding"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Autoregressive_Image_Generation_with_Randomized_Parallel_Decoding.pdf
project_link: null
code_link: https://github.com/hp-l33/ARPG
aliases:
- AAIGRPD
- AIGRPD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "ARPG decouples target-position queries from known-content key values in a two-pass autoregressive image decoder."
primary_logic: "Pass 1 encodes known shuffled content into KV caches, while Pass 2 uses position-aware MASK queries to predict one or more target tokens in arbitrary order."
claims:
- "The decoupled formulation supports randomized training order, parallel decoding, and zero-shot infilling or extrapolation."
- "Shared KV projection and RoPE encode known content and target positions efficiently."
- "The note reports FID 1.83 on ImageNet-1K 256 with 32 decoding steps and much lower memory than VAR."
---

# Autoregressive Image Generation with Randomized Parallel Decoding

> [!tip] 核心洞察
> 预测一个标记所需的核心信息是已知标记的集合和目标位置，其他未知位置的状态无关紧要。通过将查询仅从[MASK]标记导出、键值仅从内容标记导出，可以实现完全随机顺序的训练和推理，同时支持并行解码和零样本泛化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于随机并行解码的自回归图像生成 |
| 英文题名 | Autoregressive Image Generation with Randomized Parallel Decoding |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=rJdGst0W8s) · [GitHub](https://github.com/hp-l33/ARPG) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ARPG (Autoregressive Image Generation with Randomized Parallel Decoding) |
| Dataset | ImageNet-1K 256×256 |

> [!tip] 效果简介
> - ImageNet-1K 256×256 上，FID 为 1.83，对比 LlamaGen-XXL: 2.18，变化 -0.35。
> - ImageNet-1K 256×256 上，IS 为 336.1，对比 LlamaGen-XXL: 341.0，变化 -4.9。
> - ImageNet-1K 256×256 上，吞吐量 (img/s) 为 55.28，对比 LlamaGen-XXL: 64.70，变化 -9.42。

## 概要

本文提出ARPG（Autoregressive Image Generation with Randomized Parallel Decoding），一种用于图像合成的高质量高效框架。ARPG通过将位置引导与内容表示解耦，实现了完全随机顺序的训练和推理，同时支持并行解码和零样本泛化。在ImageNet-1K 256×256基准测试上，ARPG仅用32步达到FID 1.83，相比光栅顺序模型实现30倍加速，相比并行AR模型实现3倍加速，内存减少75%。ARPG还支持零样本推理任务，如图像修复、外推和分辨率扩展。



传统自回归图像生成模型受限于固定的光栅扫描顺序，导致推理效率低下且无法进行零样本泛化。掩码建模方法虽支持随机顺序，但存在两个根本性问题：

- **训练效率低下**：掩码建模的损失仅计算在[MASK]标记上，未掩码标记不直接参与损失计算，导致参数更新次优。如公式所示：
  $$\mathcal{L} = -\mathbb{E}\Big[\sum_{m_i=1} \log p(x_i \mid \mathbf{X_M})\Big], \quad \forall i \in \{1,2,\cdots,n\}$$

- **注意力冗余**：如Figure 3所示，RandAR中[MASK]标记的注意力权重极低，注意力主要集中在未掩码标记上，表明[MASK]标记贡献极小。

现有方法（如Table 1总结）在注意力模式、调度灵活性和零样本能力方面各有局限：光栅顺序模型（LlamaGen）使用严格因果注意力但无法并行；块级AR模型（VAR、PAR、SAR、NAR）使用预定义位置但调度器固定；RandAR将位置标记插入序列中，使序列长度加倍且计算成本翻倍。



## 核心方法与创新机理

ARPG的核心洞察是：预测一个标记所需的核心信息是已知标记的集合和目标位置，其他未知位置的状态无关紧要。基于此，论文提出**解耦解码框架**：

- **位置引导与内容表示解耦**：将位置信息编码为查询向量，内容信息编码为键值对，通过交叉注意力机制分离两者。
- **双解码器架构**：第一个解码器（内容精炼）仅处理已知内容标记以生成KV缓存，第二个解码器（位置引导）使用数据无关的[MASK]标记作为查询，通过交叉注意力机制预测目标标记。
- **完全随机顺序训练与推理**：解耦结构使得模型可以在任意排列下进行训练和推理，同时支持并行解码和零样本泛化。



![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_rJdGst0W8s_Autoregressiv/figures/001_Figure_1.jpg]]

ARPG的整体框架如Figure 4所示，包含两个主要解码器：

1. **Pass-1解码器（内容表示学习）**：通过标准因果自注意力处理已知内容标记序列，生成上下文感知的表示，并投影为键值对。
2. **Pass-2解码器（位置引导解码）**：使用带有位置信息的[MASK]标记作为查询，通过因果交叉注意力从Pass-1的KV缓存中预测目标标记。

训练时，Pass-1从打乱序列中学习因果表示，序列的位置信息右移一位并嵌入到[MASK]标记中作为目标感知查询。推理时，先通过Pass-1计算已知标记的KV缓存，然后选择多个目标感知查询同时访问该缓存，实现单步多标记预测。

Figure 5展示了实现细节：(a) 条件输入提供查询；(b) 零样本修复中已知区域预填充到Pass-1，掩码区域在Pass-2生成。



### 5.1 重表述的自回归分解

论文将标准自回归分解重表述为：
$$\prod_{t=1}^n p(x_{\tau_t} \mid x_{\tau_1}, x_{\tau_2}, \dotsc, x_{\tau_{t-1}}) = f_\theta \big( \{x_{\tau_i}\}_{i=1}^{t-1}, \ \tau_t \big)$$

该公式表明，在任意排列下，序列的联合概率可分解为条件概率的乘积，每个条件概率仅依赖于已知标记和目标位置。

### 5.2 Pass-2注意力机制

Pass-2解码器使用因果交叉注意力，其中查询仅来自数据无关的[MASK]标记，键值仅来自内容标记：

- **查询向量**（带RoPE）：
  $$\pmb{q}_{\tau_t}^{(l)} = \mathrm{RoPE}(\pmb{o}_{\tau_t}^{(l-1)} W_q^{(l)}, \tau_t), \quad \forall \tau_t, \pmb{o}_{\tau_t}^{(0)} = \pmb{m}$$

- **键和值向量**（带RoPE）：
  $$\pmb{k}_{\tau_i}^{(l)} = \mathrm{RoPE}(\pmb{h}_{\tau_i} \pmb{W}_k^{(l)}, \tau_i), ~ \pmb{v}_{\tau_i}^{(l)} = \pmb{h}_{\tau_i} \pmb{W}_v^{(l)}$$

- **注意力输出**：
  $$o_t^{(l)} = \pmb{q}_{\tau_t}^{(l)} + \mathrm{Attention}(\pmb{q}_{\tau_t}^{(l)}, \{\pmb{k}_{\tau_j}^{(l)}\}_{j=1}^{t-1}, \{\pmb{v}_{\tau_j}^{(l)}\}_{j=1}^{t-1})$$

### 5.3 关键设计选择

- **全局键值投影**：Pass-2解码器的所有层共享一个全局键值投影，以提高效率。
- **RoPE位置编码**：使用旋转位置嵌入（RoPE）将位置信息编码到查询和键向量中。
- **块级因果注意力泛化**：推理时可将因果注意力泛化为块级因果注意力，不破坏概率模型且显著提升性能。



## 实验与关键发现

### 6.1 主要结果

**ImageNet-1K 256×256基准测试**（Table 2）：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_rJdGst0W8s_Autoregressiv/figures/015_Table_2.jpg]]
*Table 2: Overall comparisons on ImageNet benchmarks. Arrows indicate whether lower or higher is better. Efficiency was profiled with a batch size of 64 and bfloat16 precision.*

| 模型 | FID↓ | IS↑ | 吞吐量 (img/s)↑ | 内存 (GB)↓ |
|------|------|-----|-----------------|------------|
| ARPG-XXL (32步) | **1.83** | 336.1 | 55.28 | 7.22 |
| LlamaGen-XXL | 2.18 | 341.0 | 64.70 | - |
| VAR-d30 | 2.09 | 356.4 | 1.84 | 28.5 |

**ImageNet-1K 512×512基准测试**（Table 2）：
- ARPG-XL (64步)：FID 2.82，IS 277.5，吞吐量 35.53 img/s，内存 13.98 GB
- VAR-d30：FID 3.30

**文生图**（Table 3）：
- ARPG-XL在GenEval上总体得分0.31，吞吐量30.11 img/s（4M训练数据）

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_rJdGst0W8s_Autoregressiv/figures/026_Table_3.jpg]]
*Table 3: Quantitative evaluation of text-to-image generation at 512×512 resolution.*

**可控生成**（Table 4）：
- ControlARPG (ARPG-L)：Canny条件FID 7.39，Depth条件FID 4.06

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_rJdGst0W8s_Autoregressiv/figures/027_Table_4.jpg]]
*Table 4: Controllable generation on ImageNet.*

### 6.2 消融研究

**模型设计消融**（Table 5，ARPG-L，150 epoch，64步）：

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_rJdGst0W8s_Autoregressiv/figures/030_Table_5.jpg]]
*Table 5: Ablation study of model design. The baseline model is ARPG-L, trained for 150 epochs with 64 sampling steps. “Rand. & Parall.” denotes support for randomized parallel generation.*

| 配置 | FID↓ | IS↑ | 吞吐量 (img/s)↑ | 内存 (GB)↓ |
|------|------|-----|-----------------|------------|
| 基线 (12+12层) | 3.51 | 282.7 | 67.47 | 2.64 |
| 无共享KV | 3.46 | 283.5 | 48.02 | 3.83 |
| 全Pass-2 (0+24层) | 4.57 | 268.9 | 72.26 | 0.91 |
| 无Pass-2 (24+0层) | >90 | <50 | 11.70 | 4.96 |
| 余弦位置编码 | 3.68 | 280.1 | 67.47 | 2.64 |

关键发现：
- 减少Pass-2解码器比例会降低推理效率和生成质量；完全移除Pass-2解码器导致模型退化为标准AR模型，失去随机并行解码能力。
- 不使用共享KV投影会略微提升生成质量，但显著影响推理速度和内存消耗。
- 将RoPE替换为余弦位置编码会导致性能下降。

**生成顺序影响**（Table 7）：
- 随机顺序（FID 2.44，64步）优于光栅顺序（FID 2.49，256步），表明随机顺序建模虽更具挑战性，但性能更优。

**并行解码消融**（Table 8，Figure 9）：
- ARPG-XXL在256步下FID 1.90（因果注意力）和1.88（块级注意力），吞吐量8.41 img/s
- 泛化注意力模式（因果→块级）在更少解码步数下提升质量

### 6.3 注意力分布分析

Figure 11显示，ARPG的解耦结构导致两个解码器的注意力分数分布更均匀，避免了RandAR（Figure 3）中大量标记被分配极低权重的问题。

### 6.4 训练损失曲线

Figure 10显示，最大模型（1.3B参数）在1M迭代后达到最低损失约7.03，719M参数模型收敛到7.29，320M参数模型最高损失7.50。

### 6.5 零样本推理

Figure 8展示了ARPG在零样本推理任务中的定性结果，包括图像修复、编辑和外推（从256×256到1024×256）。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_rJdGst0W8s_Autoregressiv/figures/014_Table_1.jpg]]
*Table 1: Summary of existing methods.*



## 定位与知识库关联

ARPG在自回归图像生成方法谱系中占据独特位置：

- **与光栅顺序AR模型（LlamaGen）的区别**：ARPG通过解耦结构实现随机顺序训练和并行解码，克服了固定顺序的推理效率瓶颈。
- **与掩码建模（MaskGIT、MAR）的区别**：ARPG使用因果注意力而非双向注意力，所有标记参与损失计算，避免了掩码建模的训练效率低下问题。
- **与随机顺序AR模型（RandAR）的区别**：ARPG将位置信息作为查询而非插入序列，避免了序列长度加倍和注意力冗余问题。
- **与块级AR模型（VAR、PAR、SAR、NAR）的区别**：ARPG支持完全灵活的随机顺序，而非预定义的块级顺序。

**知识库定位**：ARPG属于视觉自回归建模领域，核心贡献在于提出了一种新的解码范式——将位置引导与内容表示解耦，通过双解码器架构实现高效并行解码和零样本泛化。该方法在效率（30倍加速、75%内存减少）和质量（FID 1.83）之间取得了优异平衡，并为自回归模型在可控生成和零样本任务中的应用开辟了新途径。

**局限性**：
- 文生图模型仅在4M数据子集上训练50个epoch，数据量和训练步数有限。
- 可控生成任务（Canny、Depth）上的FID与ControlAR持平，未显示出显著优势。
- 零样本推理任务仅展示了定性结果，缺乏定量评估。
- 高分辨率（512×512）生成质量（FID 2.82）仍低于256×256（FID 1.83）。
- GenEval总体得分（0.31）与LlamaGen（0.32）相当，但低于DALL-E 3（0.67）等先进模型。

**开放问题**：
- ARPG在更大规模数据和更多训练步数下的性能如何？
- ARPG能否扩展到更高分辨率（如1024×1024）的图像生成？
- ARPG的零样本泛化能力的定量指标（如FID、LPIPS）是多少？
- ARPG架构是否可以推广到视频生成或3D生成任务？
- ARPG与扩散模型结合能否进一步提升效率？



## 原文 PDF

![[paperPDFs/ICLR_2026/Autoregressive_Image_Generation_with_Randomized_Parallel_Decoding.pdf]]
