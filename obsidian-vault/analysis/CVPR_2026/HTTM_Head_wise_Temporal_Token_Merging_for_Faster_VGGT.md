---
title: "HTTM: Head-wise Temporal Token Merging for Faster VGGT"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HTTM_Head_wise_Temporal_Token_Merging_for_Faster_VGGT.pdf
project_link: null
code_link: null
aliases:
- HHWTTM
- HTTM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用每个注意力头独立的令牌合并策略（head-wise merging），结合时空块重组和自适应异常值过滤，通过控制合并率直接调节全局注意力序列长度，从而在推理加速与重建质量之间实现可控权衡。
primary_logic: VGGT中的全局注意力令牌在空间邻近区域和时序相邻帧之间存在显著冗余，该冗余源于旋转位置编码（RoPE）的层间强化与输入图像的视觉相似性。通过对每个注意力头独立进行块内令牌合并，并利用时序重排序将高相似度令牌聚集到同一合并块内，可以在极低计算开销下实现高效率令牌压缩，避免传统多头统一合并导致的表示坍缩，从而在几乎不损失3D重建精度的前提下大幅降低全局注意力延迟。
claims:
- HTTM achieves up to 7× acceleration with negligible performance loss.
- HTTM reduces merging cost by 4.58× under the same merging ratio compared to existing methods.
- Head-wise merging preserves the uniqueness of feature tokens after head concatenation, avoiding feature collapse.
- Temporal reordering shifts high-similarity token pairs inside merging blocks, improving merging quality.
---

# HTTM: Head-wise Temporal Token Merging for Faster VGGT

> [!tip] 核心洞察
> VGGT中的全局注意力令牌在空间邻近区域和时序相邻帧之间存在显著冗余，该冗余源于旋转位置编码（RoPE）的层间强化与输入图像的视觉相似性。通过对每个注意力头独立进行块内令牌合并，并利用时序重排序将高相似度令牌聚集到同一合并块内，可以在极低计算开销下实现高效率令牌压缩，避免传统多头统一合并导致的表示坍缩，从而在几乎不损失3D重建精度的前提下大幅降低全局注意力延迟。

| 字段 | 内容 |
|------|------|
| 中文题名 | HTTM：头级时序令牌合并加速VGGT |
| 英文题名 | HTTM: Head-wise Temporal Token Merging for Faster VGGT |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.21317) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HTTM (Head-wise Temporal Token Merging) |
| Dataset | NRGBD, ScanNet, Global Attention Layers |

> [!tip] 效果简介
> - NRGBD 上，Accuracy (Acc.↓) 0.012 (HTTM) vs 0.016 (FastVGGT) (0.004 更低)；Completeness (Comp.↓) 0.010 (HTTM) vs 0.011 (FastVGGT) (0.001 更低)。
> - ScanNet (1000 frames) 上，Total Latency (s) 102.8 (VGGT*+HTTM) vs 724.6 (VGGT*) (约 7× 加速)。
> - Global Attention Layers (1000 frames) 上，Matching Latency (s) 0.12 (HTTM) vs 2.31 (FastVGGT) (19.25× 更快匹配)。

## 概述

VGGT（Wang et al., CVPR 2025）是一种前馈3D重建模型，其全局注意力层需要对所有输入视图进行完全对完全（all-to-all）的令牌交互。当输入帧数增加时，令牌序列长度急剧膨胀至超过20k，注意力计算的二次复杂度使推理延迟成为主要效率瓶颈。

本文提出**HTTM（Head-wise Temporal Token Merging）**，一种无需训练的3D令牌合并方法，专为加速VGGT的全局注意力层设计。核心洞察是：VGGT中空间邻近区域和时序相邻帧之间存在显著的令牌冗余，该冗余源于旋转位置编码（RoPE）的层间强化与输入图像的视觉相似性。HTTM通过三个关键机制实现高效压缩：

- **头级独立合并**：每个注意力头根据自身的相似性模式独立执行令牌合并，避免传统多头统一合并导致的表示坍缩。
- **时空块重组与时序重排序**：将令牌按空间分块后跨帧堆叠，使高相似度令牌聚集在同一合并块内，以线性成本实现高质量合并。
- **自适应异常值过滤**：跨头识别偏离聚合令牌的异常值并排除合并，防止精度灾难性退化。

实验表明，HTTM在几乎不损失3D重建精度的前提下实现显著加速：在1000帧ScanNet场景下，总延迟从724.6秒降至102.8秒（约7×加速）；合并匹配延迟比FastVGGT快19.25倍；合并成本在同等合并率下降低4.58倍。在NRGBD等细粒度数据集上，HTTM以更短的Q/K/V序列取得了优于FastVGGT的重建质量。

## 背景与动机

### 问题背景：VGGT的全局注意力瓶颈

**VGGT**（Wang et al., CVPR 2025）是一种前馈3D重建模型，其核心架构采用交替的帧注意力（Frame Attention）与全局注意力（Global Attention）层。其中，全局注意力层需要跨所有输入视图进行完全对完全（all-to-all）的令牌交互，这使得令牌序列长度随输入帧数急剧增长——当输入超过1000帧时，序列长度可突破20k。由于标准缩放点积注意力的计算复杂度与序列长度的平方成正比，全局注意力层迅速成为整个推理流程的延迟瓶颈。

**关键瓶颈**：VGGT的全局注意力层在长序列输入下，推理延迟主导了端到端耗时，而非模型本身的3D重建计算。论文对VGGT的注意力分数分布分析（Figure 2）显示，与LLaMA 3.1 8B等语言模型不同，VGGT的注意力分数在早期和晚期层中高度集中于低值区域，中层虽略有分散，但整体仍明显偏向低值。这表明VGGT的全局注意力中存在大量冗余交互——许多令牌对之间的注意力权重极低，对最终输出的贡献微乎其微，却仍消耗着昂贵的计算资源。

### 令牌冗余的根源：空间相似性与时序一致性

论文进一步揭示了VGGT中令牌冗余的两个结构来源：

1. **空间冗余**：在同一帧内部，空间邻近区域的令牌具有高度相似的视觉特征。Figure 4展示了单帧重建中第14层全局注意力的查询令牌余弦相似度——高视觉冗余帧（如白墙）表现出强烈的空间相似性，而低冗余帧（杂乱物体）的相似性则较弱。这种空间冗余意味着相邻令牌可以被有效合并而不丢失关键信息。

2. **时序冗余**：在连续帧之间，相同空间位置对应的令牌表现出显著的时序相似性。Figure 3展示了4个相邻帧查询令牌的平均余弦相似度模式——沿块对角线的显著高相似度表明，同一空间区域在连续帧间的令牌特征高度一致。Figure 5进一步证实，当输入帧之间视觉相似度较高时，查询令牌的时序相似度也随之增强，表现为非对角线区域的高分数。

这两种冗余的深层机制与VGGT中使用的旋转位置编码（RoPE）密切相关。RoPE在层间传播过程中强化了空间邻近令牌和时序相邻令牌的表示相似性，使得冗余模式在深层全局注意力层中尤为突出。

### 现有加速方法的缺口

针对VGGT的全局注意力瓶颈，已有两类加速尝试：

- **块稀疏全局注意力**：利用注意力矩阵的稀疏性，仅计算部分令牌对之间的注意力。然而，该方法需要额外的稀疏模式识别开销，且难以保证重建精度的稳定性。

- **FastVGGT**（Shen et al., arXiv 2025）：将2D视觉任务中的令牌合并方法ToMeSD直接迁移到VGGT的全局注意力层。FastVGGT采用**统一的多头合并策略**——所有注意力头共享相同的合并模式。虽然该方法取得了显著的延迟改善，但存在两个根本性缺陷：
  
  1. **表示坍缩风险**：由于不同注意力头捕捉的语义模式各异，统一的合并操作会迫使所有头使用相同的令牌聚合方案，导致头拼接（head concatenation）后输出嵌入的独特性丧失（Figure 7）。这相当于在合并阶段丢弃了多头注意力机制的核心优势——多视角表示能力。
  
  2. **合并成本高昂**：FastVGGT在全局范围内计算令牌相似度以确定合并目标，这一过程本身的计算复杂度与令牌总数呈二次关系，在长序列场景下合并开销甚至可能抵消注意力加速带来的收益。

### 本文动机

基于上述分析，本文的核心动机可概括为三点：

1. **利用而非忽略冗余**：VGGT全局注意力中的空间和时序冗余是结构性的、可预测的，应通过精心设计的令牌压缩策略加以利用，而非简单地将稀疏化方法从其他领域移植过来。

2. **保护多头表示的独特性**：令牌合并必须在每个注意力头内部独立进行，以保留不同头所捕获的差异化特征，避免统一合并导致的表示坍缩。

3. **降低合并本身的开销**：合并操作的成本必须可控——通过将合并范围限制在固定大小的时空块内，使合并成本与序列长度呈线性关系，而非二次关系。

基于这些动机，本文提出**HTTM（Head-wise Temporal Token Merging）**，一种训练无关的3D令牌合并方法，专门针对VGGT的交替注意力架构设计，目标是在几乎不损失3D重建精度的前提下实现显著的推理加速。

## 核心创新

HTTM 的核心创新在于将 VGGT 全局注意力的令牌压缩从“所有头共享合并模式”升级为“每个头独立合并”的细粒度策略，并结合时空块重组与自适应异常值过滤，在几乎不损失 3D 重建精度的前提下实现最高 7× 的推理加速（Table 3）。以下从五个关键维度剖析其相对于现有方法的突破。

### 1. 头级合并粒度：从统一合并到独立合并

**Baseline（FastVGGT）**：所有注意力头共享相同的令牌合并模式。该方法直接将 ToMeSD 的 2D 视觉任务合并策略迁移到 VGGT，未考虑多头注意力中不同头对令牌相似性模式的差异化响应。

**HTTM 的改进**：每个注意力头独立执行令牌合并（Section 3.2, Figure 7）。具体而言，对于每个头 $i$，分别计算源令牌集与目标令牌集之间的行归一化余弦相似度矩阵：

$$\mathbf{Sim}^{(i)} = \mathrm{RowNorm}\Big(\mathbf{S}^{(i)}\Big) \cdot \mathrm{RowNorm}\Big(\mathbf{D}^{(i)}\Big)^{\top}$$

然后独立选择 top-r 最相似令牌进行合并，生成压缩后的 Q/K/V：

$$\tilde{\mathbf{Q}}^{(i)} = \mathcal{M}_i^q(\mathbf{Q}^{(i)}), \quad \tilde{\mathbf{K}}^{(i)} = \mathcal{M}_i^k(\mathbf{K}^{(i)})$$

**关键机理**：多头统一合并会导致头拼接后的特征表示坍缩——不同头捕获的差异性信息被强制统一合并，丢失了表示的多样性。头级合并保留了每个头独特的相似性模式，使合并后的输出嵌入保持独特性（Figure 7）。这一设计的证据强度高（confidence 0.95），是 HTTM 相对于 FastVGGT 在细粒度数据集 NRGBD 上取得更优重建精度（Acc.↓: 0.012 vs 0.016, Table 1）的核心原因。

### 2. 合并范围：从全局匹配到分块匹配

**Baseline（ToMeSD 风格合并）**：在全局范围内计算所有令牌对之间的相似度并执行合并，合并成本随令牌数 $N$ 呈二次增长。

**HTTM 的改进**：将令牌序列分割为固定大小 $n_b$ 的合并块，仅在块内进行令牌匹配与合并（Section 3.3）。合并块大小定义为：

$$n_b = n_s \times n_t$$

其中 $n_s$ 为空间块大小，$n_t$ 为时序帧数。这使得合并成本随 $N$ 线性增长，而非二次增长。在相同合并率下，HTTM 的合并成本降低 4.58×（Figure 1, confidence 0.9）。

### 3. 时序重排序：将高相似度令牌聚集到同一合并块

**Baseline**：令牌按帧的空间顺序排列，跨帧的高相似度令牌对分散在不同合并块中，无法被块内合并捕获。

**HTTM 的改进**：执行时序重排序——将不同帧中相同空间位置的块堆叠形成时序合并块（Section 3.3, Figure 8）。例如，从 $n_t = 8$ 帧中各取空间块大小 $n_s = 128$ 的令牌堆叠，形成 $n_b = 1024$ 的合并块。

**关键机理**：VGGT 中旋转位置编码（RoPE）的层间强化与连续帧的视觉相似性，导致同一空间区域跨帧的令牌具有高余弦相似度（Figure 3, Figure 5）。时序重排序将这些高相似度令牌对从块外“转移”到块内（Figure 8），使块内合并能捕获原本需要全局匹配才能发现的高质量匹配对，从而在低计算开销下实现高效令牌压缩（confidence 0.95）。

### 4. 自适应异常值过滤：防止灾难性精度退化

**Baseline**：所有令牌均参与合并，无异常值处理机制。当某些令牌与合并目标偏差过大时，强制合并会引入显著表示误差。

**HTTM 的改进**：跨所有注意力头识别偏离聚合令牌最大的 top d% 令牌，将其标记为异常值并排除合并（Section 3.4）。异常值令牌的输出直接保留原始值，同时修正受异常值影响的合并结果。该模块通过自定义 CUDA 核实现高效计算。

**证据强度**：消融实验（Table 5, confidence 0.98）表明，移除异常值过滤后，NRGBD 上的 Accuracy 从 0.012 急剧退化至 0.240，证实了该模块对维持重建精度的关键作用。

### 5. 第一帧锚定：抑制歧义与稳定位姿估计

**Baseline**：无显式的目标令牌选择策略，合并过程中源-目标令牌的角色分配可能引入歧义。

**HTTM 的改进**：显式将所有第一帧令牌作为目标（dst）令牌（Section 4.4, Figure 10）。这一设计使第一帧成为合并的“锚定参考”，抑制了合并过程中的歧义性，同时保持了参考帧的稳定性，对相机位姿估计质量有正向影响（confidence 0.9）。

### 创新总结

HTTM 的五个 changed slots 构成了一条完整的效率-质量优化链路：**头级合并**保护表示多样性 → **分块合并**控制计算成本 → **时序重排序**提升块内匹配质量 → **异常值过滤**防止精度崩塌 → **第一帧锚定**稳定位姿估计。这些创新相互协同，使 HTTM 在 1000 帧输入下实现 7× 加速的同时，重建质量与原始 VGGT 几乎持平（Table 3, Table 2）。

## 整体框架

HTTM 是一个**训练无关**的令牌压缩加速框架，专为 VGGT（Wang et al., CVPR 2025）的交替注意力架构设计。其核心目标是在全局注意力层进入注意力核之前，通过对 Q/K/V 令牌进行压缩，大幅降低二次复杂度的计算开销，同时在注意力计算完成后将令牌恢复至原始序列长度，保证下游模块不受影响。

### Pipeline 总览

HTTM 的整体流程由五个顺序模块构成，形成“重排序—合并—计算—反合并—过滤”的闭环：

1. **时序重排序（Temporal Reordering）**  
   将输入令牌按空间位置分块，并跨帧堆叠对应块，形成包含时序信息的合并块（merging block）。每个合并块大小为 $n_b = n_s \times n_t$，其中 $n_s$ 为空间块大小，$n_t$ 为时序帧数。这一步骤将高相似度令牌集中到同一块内，为后续块内合并奠定基础（Section 3.3, Figure 8）。

2. **头级令牌合并（Head-wise Token Merging）**  
   在每个注意力头内，独立计算源令牌集 $\mathbf{S}^{(i)}$ 与目标令牌集 $\mathbf{D}^{(i)}$ 之间的行归一化余弦相似度矩阵：
   $$\mathbf{Sim}^{(i)} = \mathrm{RowNorm}\Big(\mathbf{S}^{(i)}\Big) \cdot \mathrm{RowNorm}\Big(\mathbf{D}^{(i)}\Big)^{\top}$$
   基于相似度矩阵，在每个合并块内选取 top-$r$ 最相似令牌进行合并，生成压缩后的查询和键：
   $$\tilde{\mathbf{Q}}^{(i)} = \mathcal{M}_i^q(\mathbf{Q}^{(i)}), \quad \tilde{\mathbf{K}}^{(i)} = \mathcal{M}_i^k(\mathbf{K}^{(i)})$$
   值令牌 $\mathbf{V}^{(i)}$ 遵循键的合并模式进行压缩（Section 3.2）。

3. **压缩注意力计算（Reduced Attention Computation）**  
   在压缩后的令牌上执行标准缩放点积注意力：
   $$\mathbf{A}^{(i)} = \mathrm{softmax}\left(\frac{\tilde{\mathbf{Q}}^{(i)}(\tilde{\mathbf{K}}^{(i)})^{\top}}{\sqrt{d_\mathrm{head}}}\right), \quad \tilde{\mathbf{O}}^{(i)} = \mathbf{A}^{(i)} \tilde{\mathbf{V}}^{(i)}$$
   由于序列长度大幅缩减，注意力计算延迟显著降低（Section 3.2）。

4. **头级令牌反合并（Head-wise Token Unmerging）**  
   通过逆映射 $\mathcal{U}_i$ 将合并输出恢复至原始序列长度。未参与合并的令牌直接保留其输出，被合并的令牌则将合并输出复制到所有参与合并的原始令牌位置：
   $$\mathbf{o}_n^{(i)} := \tilde{\mathbf{o}}_m^{(i)}, \quad \mathbf{O}^{(i)} = \mathcal{U}_i(\tilde{\mathbf{O}}^{(i)})$$
   最后将所有注意力头的输出在通道维度拼接，送入后续层（Section 3.2）。

5. **自适应异常值过滤（Adaptive Outlier Filtering）**  
   在所有头中识别偏离聚合令牌较大的异常值（top $d\%$），将其排除在合并之外，并修正合并结果。该模块通过自定义 CUDA 核实现高效过滤，防止异常令牌导致的精度灾难性退化（Section 3.4, Table 5）。

### 关键设计决策

与基线方法 **FastVGGT**（Shen et al., arXiv 2025）的关键区别在于，HTTM 在以下维度进行了系统性改进：

| 设计维度 | FastVGGT | HTTM |
|---------|----------|------|
| 合并粒度 | 所有头共享统一合并模式 | 每个头独立执行合并 |
| 合并范围 | 全局全对全相似度计算 | 固定大小时空块内合并 |
| 令牌排序 | 按帧的空间顺序排列 | 时序重排序，跨帧堆叠对应块 |
| 异常值处理 | 无 | 自适应跨头识别与过滤 |
| 目标令牌锚定 | 无显式策略 | 第一帧锚定（可选） |

其中，**头级合并**是防止表示坍缩的核心机制——不同注意力头捕捉不同的相似性模式，统一合并会抹杀这种多样性，而独立合并能保留头拼接后特征令牌的唯一性（Figure 7, Section 3.2）。**时序重排序**则将原本分散在不同合并块的高相似度令牌对集中到同一块内，在相同合并率下使合并质量显著提升，同时将合并成本从全局的二次复杂度降至线性复杂度（Figure 8, Section 3.3）。

### 数据流与模块关系

输入令牌序列首先经过时序重排序形成时空合并块，随后在每个注意力头内独立执行“合并—注意力计算—反合并”的子流程，最后经异常值过滤修正输出。整个流程插入在全局注意力层的 Q/K/V 投影之后、注意力核计算之前，以及注意力核输出之后、后续线性投影之前，对 VGGT 的其他组件（帧注意力层、交替 Transformer 块等）完全透明，无需重新训练或微调。

### 补充图表

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/006_Figure_6.jpg]]
*Figure 6: Overview of how HTTM accelerates attention layers by merging QKV tokens. HTTM merges and unmerges Q/K/V tokens before and after entering the attention kernel. Using temporal reordering 3.3, HTTM forms temporal blocks that consist of similar tokens (denoted with colors) and performs merging and unmerging within these blocks*

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/001_Figure_1.jpg]]
*Figure 1: HTTM forms spatio-temporal merging blocks that jointly consider neighboring tokens across consecutive frames. This design exploits temporal coherence and spatial redundancy to merge tokens efficiently. With the same merging ratio, HTTM reduces the merging cost by 4.58×*

## 核心模块与公式推导

HTTM 的核心管线由四个模块构成：时序重排序（Temporal Reordering）、头级令牌合并（Head-wise Token Merging）、压缩注意力计算（Reduced Attention）和头级令牌反合并（Head-wise Token Unmerging），并辅以自适应异常值过滤（Adaptive Outlier Filtering）。以下逐一展开各模块的机制与关键公式。

### 时序重排序

VGGT 的全局注意力层接收来自所有帧的令牌序列。若直接按帧的空间顺序排列令牌，则高相似度的跨帧对应令牌会分散在序列的不同位置，导致固定大小的合并块无法捕获这些匹配对（见 Figure 8a）。

HTTM 的解决方案是**时序重排序**：首先将每帧的令牌按空间位置划分为大小为 $n_s$ 的空间块，然后将连续 $n_t$ 帧中相同空间位置的块堆叠在一起，形成一个大小为 $n_b = n_s \times n_t$ 的**时空合并块**。这一重排序操作将跨帧的高相似度令牌对集中到同一合并块内部（见 Figure 8b），使得后续的块内合并能够高效捕获时序冗余，而无需执行昂贵的全局相似度计算。合并成本因此从与序列长度 $N$ 的二次关系降为线性关系。

### 头级令牌合并

传统令牌合并方法（如 ToMeSD）对所有注意力头使用统一的合并模式，这在 VGGT 中会导致**特征表示坍缩**：不同头学习到的不同相似性模式被强制统一，头拼接后输出嵌入的独特性丧失（见 Figure 7）。

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/007_Figure_7.jpg]]
*Figure 7: Head-wise merging can better keep the uniqueness of the output embedding. Different shades of the same color represent similar token chunks*

HTTM 的核心设计是**每个注意力头独立执行令牌合并**。对于多头注意力层的第 $i$ 个头，其查询（Query）和键（Key）令牌分别通过独立的合并模块 $\mathcal{M}_i^q$ 和 $\mathcal{M}_i^k$ 进行处理，值（Value）令牌则跟随键令牌的合并模式。

合并过程的第一步是计算源令牌集 $\mathbf{S}^{(i)}$ 与目标令牌集 $\mathbf{D}^{(i)}$ 之间的余弦相似度矩阵：

$$\mathbf{Sim}^{(i)} = \mathrm{RowNorm}\Big(\mathbf{S}^{(i)}\Big) \cdot \mathrm{RowNorm}\Big(\mathbf{D}^{(i)}\Big)^{\top} \tag{1}$$

其中 $\mathrm{RowNorm}(\cdot)$ 表示行归一化操作。基于该相似度矩阵，每个目标令牌选择与其最相似的 top-$r$ 个源令牌进行合并，得到压缩后的查询和键：

$$\tilde{\mathbf{Q}}^{(i)} = \mathcal{M}_i^q(\mathbf{Q}^{(i)}), \quad \tilde{\mathbf{K}}^{(i)} = \mathcal{M}_i^k(\mathbf{K}^{(i)}) \tag{2}$$

### 压缩注意力计算

合并后的令牌进入标准的缩放点积注意力计算。由于序列长度显著缩短，注意力矩阵的计算复杂度大幅降低：

$$\mathbf{A}^{(i)} = \mathrm{softmax}\left(\frac{\tilde{\mathbf{Q}}^{(i)}(\tilde{\mathbf{K}}^{(i)})^{\top}}{\sqrt{d_{\mathrm{head}}}}\right) \tag{3}$$

$$\tilde{\mathbf{O}}^{(i)} = \mathbf{A}^{(i)} \tilde{\mathbf{V}}^{(i)} \tag{4}$$

其中 $d_{\mathrm{head}}$ 为每个注意力头的维度，$\tilde{\mathbf{V}}^{(i)}$ 为合并后的值令牌。

### 头级令牌反合并

注意力计算完成后，需要将压缩输出恢复到原始序列长度，以便后续层处理。对于每个头 $i$，未参与合并的令牌直接保留其原始输出；被合并的令牌则通过反合并映射 $\mathcal{U}_i$ 将合并令牌的输出复制到所有参与合并的原始令牌位置：

$$\mathbf{o}_n^{(i)} := \tilde{\mathbf{o}}_m^{(i)} \tag{5}$$

$$\mathbf{O}^{(i)} = \mathcal{U}_i(\tilde{\mathbf{O}}^{(i)}) \in \mathbb{R}^{N \times d_{\mathrm{head}}} \tag{6}$$

最后，将所有注意力头的输出在通道维度上拼接，得到完整的输出嵌入。

### 自适应异常值过滤

令牌合并的潜在风险是**异常值令牌**被强制合并到与其差异较大的聚合令牌中，导致信息严重失真。HTTM 采用自适应异常值过滤来应对这一问题。

具体机制为：在所有注意力头完成合并后，跨头识别与各自聚合令牌之间 L2 偏差最大的 top $d\%$ 令牌，将其标记为异常值。这些异常值令牌被排除在合并之外，保留其原始特征，同时对合并结果进行修正以补偿异常值的移除。该过滤策略通过**自定义 CUDA 核**实现高效执行。消融实验（Table 5）表明，移除异常值过滤会导致 NRGBD 数据集上的 Accuracy 指标从 0.012 急剧恶化至 0.240，验证了该模块的关键作用。

### 第一帧锚定策略

在目标令牌的选择上，HTTM 显式地将**第一帧的所有令牌作为目标（dst）令牌**，后续帧的令牌仅作为源（src）令牌向第一帧合并。这一设计抑制了合并方向上的歧义，使参考帧保持稳定，从而有利于相机位姿估计的稳定性（见 Figure 10）。

### 补充图表

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/008_Figure_8.jpg]]
*Figure 8: Token similarity in merging blocks of size 1024. (a) Without temporal reordering, many highly similar matches lie outside of merging blocks. We can’t capture those matches unless we use a global merging block that is very costly. (b) Through temporal reordering, high-similarity matches shift inside merging blocks, leading to better merging quality*

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/003_Figure_3.jpg]]
*Figure 3: Cosine similarity patterns averaged across all heads between query tokens of 4 adjacent frames. High similarities observed along the block diagonals indicate that tokens within the same spatial region (local areas) and corresponding locations across consecutive frames share highly similar features*

## 实验与分析

HTTM 的评估围绕两个核心维度展开：**3D 重建精度保持**与**全局注意力推理加速**。实验在 7Scenes、NRGBD 和 ScanNet 三个基准上进行，所有测试均在相同 NVIDIA GPU 环境下使用 FlashAttention 和 BFloat16 精度执行，确保比较基准一致。

### 主要定量结果

**重建精度**：在细粒度数据集 NRGBD 上，HTTM 在更短的 Q/K/V 序列长度下实现了优于 FastVGGT 的重建质量。具体而言，HTTM 的 Accuracy（Acc.↓）达到 0.012，优于 FastVGGT 的 0.016；Completeness（Comp.↓）为 0.010，同样优于 FastVGGT 的 0.011（Table 1）。这表明头级合并策略在压缩令牌的同时更有效地保留了 3D 重建所需的空间细节。

**推理加速**：在 1000 帧 ScanNet 输入下，VGGT*+HTTM 的总延迟为 102.8 秒，而原始 VGGT* 为 724.6 秒，实现了约 **7× 加速**（Table 3）。在更长序列场景中，HTTM 持续保持与原始 VGGT 相近的重建性能，同时大幅缩短延迟（Table 2）。

**合并效率**：在 1000 帧输入下，HTTM 的全局注意力层匹配延迟仅为 0.12 秒，而 FastVGGT 为 2.31 秒，匹配阶段加速达 **19.25×**（Table 4）。在相同合并率下，HTTM 的合并成本相比现有方法降低 **4.58×**（Figure 1）。这一效率优势源于时空块内合并将相似度计算复杂度从全局二次降为块内线性。

### 定性结果

Figure 9 的定性对比显示，HTTM 相比 FastVGGT 保留了更多来自原始 VGGT 的高保真细节。在细粒度几何结构（如物体边缘和表面纹理）上，HTTM 的重建结果更接近原始 VGGT 输出，验证了头级独立合并在避免表示坍缩方面的有效性。

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/011_Figure_9.jpg]]
*Figure 9: Qualitative results. Compared to FastVGGT, HTTM preserves more high-fidelity details of VGGT*

### 消融分析

**自适应异常值过滤**：Table 5 的消融实验表明，移除异常值过滤后，NRGBD 上的 Accuracy 从 0.012 急剧恶化至 0.240，精度退化幅度超过一个数量级。这证实了异常令牌对合并质量的灾难性影响，以及跨头自适应过滤机制的关键作用。

**时序重排序**：Figure 8 的相似度矩阵对比显示，不使用时序重排序时，大量高相似度令牌对落在固定大小的合并块之外，无法被捕获；而通过跨帧堆叠空间块形成时序合并块，高相似度匹配被集中到块内，显著提升了合并质量。这一机制在连续帧场景中尤其有效。

**第一帧锚定**：Section 4.4 和 Figure 10 的分析表明，显式将所有第一帧令牌作为目标（dst）令牌，抑制了合并过程中的歧义性，稳定了相机位姿估计。第一帧作为参考帧的稳定性对整体重建质量至关重要。

**时空合并权衡**：Figure 11 的帕累托前沿展示了合并成本与合并质量之间的权衡关系。对于连续帧输入，沿时序维度合并更多帧可获得更优的质量/速度折衷；对于稀疏视角场景，沿空间维度合并更多令牌更为有效。这一发现为不同应用场景下的合并策略选择提供了指导。

### 失败模式与局限

HTTM 的有效性高度依赖输入帧的时间连续性。在稀疏视角或低重叠场景下，时序重排序的优势显著减弱，方法退化为主要依赖空间合并，加速效果受限。此外，自适应异常值过滤依赖自定义 CUDA 核实现，增加了部署复杂度和跨平台兼容性要求。该方法针对 VGGT 的交替帧注意力/全局注意力架构设计，无法直接迁移至其他 3D 重建模型或通用视觉 Transformer。

### 补充图表

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/009_Table_1.jpg]]
*Table 1: Comparison of 3D reconstruction performance in accuracy (Acc) and completeness (Comp). HTTM achieves better reconstruction quality on fine-grained datasets like NRGBD than FastVGGT using a shorter Q/K/V sequence*

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/013_Table_3.jpg]]
*Table 3: Latency Comparison. At 1000 frames, we are 7× faster than the baseline VGGT with FlashAttention in Bfloat16*

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/012_Table_4.jpg]]
*Table 4: Averaged latency composition of Global Attention layers in HTTM and FastVGGT using comparable merging ratios over 1000 frames*

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/015_Table_5.jpg]]
*Table 5: Accuracy and completeness on NRGBD with and without outlier filtering using the same token sequence length*

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/014_Figure_11.jpg]]
*Figure 11: The Pareto front illustrates the trade-off between merging cost and merging quality, with color indicating the composition of the cost. Greenish points merge more frames along the temporal dimension, while redish points merge more tokens along the spatial dimension*

![[assets/figures/papers/paper_list_l2104_https_arxiv_org_abs_2511_21317/figures/002_Figure_2.jpg]]
*Figure 2: Attention score distribution comparison between VGGT and Llama 3.1 8B[12]. The distribution of attention scores in VGGT is heavily concentrated around low values in both its early and late layers. In the middle layers, attention distribution is still more skewed towards lower values compared to Llama*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

HTTM 的核心定位是**训练无关的推理加速插件**，专为 VGGT（Wang et al., CVPR 2025）的交替注意力架构设计。VGGT 的全局注意力层需要跨所有视图进行完全对完全的令牌交互，随着输入帧数增加，令牌序列长度急剧增长（超过 20k），二次复杂度的注意力计算成为主要效率瓶颈。HTTM 通过在注意力计算前压缩 Q/K/V 令牌序列长度来直接缓解这一瓶颈。

**与 FastVGGT 的关系**：FastVGGT（Shen et al., arXiv 2025）是基于 ToMeSD 的训练无关加速方法，同样通过令牌合并来缩短全局注意力序列。然而，FastVGGT 直接将 2D 视觉任务中的合并策略移植到 VGGT，存在三个关键局限：（1）所有注意力头共享相同的合并模式，导致头拼接后特征表示的独特性丧失（特征坍缩）；（2）合并范围采用全局全对全相似度计算，合并成本本身随序列长度二次增长；（3）未考虑 VGGT 中旋转位置编码（RoPE）层间强化和时序相邻帧视觉相似性所导致的特殊冗余模式。

HTTM 在 FastVGGT 的基础上进行了四项关键改进，构成了方法谱系中的**结构性升级**：

| 改进维度 | FastVGGT | HTTM |
|---------|----------|------|
| 合并粒度 | 所有头共享合并模式 | 每个头独立执行合并 |
| 合并范围 | 全局全对全相似度 | 固定大小时空块内 |
| 令牌排序 | 按帧空间顺序 | 时序重排序（跨帧堆叠对应块） |
| 异常值处理 | 无 | 自适应异常值过滤 |

**与块稀疏全局注意力的关系**：另一种 VGGT 加速思路是利用注意力矩阵的稀疏性进行块稀疏全局注意力计算。HTTM 与该方法正交——前者通过令牌压缩减少序列长度，后者通过稀疏化减少注意力计算量。两者在原理上可以叠加，但 HTTM 的优势在于其合并成本本身是线性的（块内合并），且不依赖注意力模式的先验假设。

### 2. 适用边界与前提条件

HTTM 的有效性建立在以下前提之上：

- **输入帧的时间连续性**：时序重排序的核心机制依赖于相邻帧中相同空间位置的令牌具有高相似度。对于稀疏视角或低重叠场景，时间维度的冗余减弱，HTTM 退化为主要依赖空间合并，加速效果受限。实验表明，对于连续帧，沿时间维度合并更多帧可获得更好的质量/速度权衡；对于稀疏视角，沿空间维度合并更有效（Figure 11）。

- **VGGT 的交替注意力架构**：HTTM 针对 VGGT 的“帧注意力 + 全局注意力”交替结构设计，其中全局注意力层的令牌冗余最为显著。该方法无法直接应用于其他 3D 重建模型（如 DUSt3R 系列）或通用视觉 Transformer，因为其合并策略依赖 VGGT 中 RoPE 强化的时序相似性模式。

- **推理阶段的令牌冗余假设**：HTTM 假设全局注意力层的令牌在空间邻近区域和时序相邻帧之间存在显著冗余。这一假设在 VGGT 的深层全局注意力层中得到验证（Figure 4, Figure 5），但在模型的早期层或帧注意力层中冗余程度不同，因此 HTTM 仅应用于全局注意力层。

### 3. 已知局限

1. **场景依赖性**：HTTM 的加速效果与输入场景的视觉冗余度相关。高视觉冗余场景（如白墙）的空间相似性更强，合并质量更高；低视觉冗余场景（如杂乱物体）的合并收益下降（Figure 4）。

2. **部署复杂度**：自适应异常值过滤依赖自定义 CUDA 核实现，增加了部署复杂度和平台兼容性要求。虽然合并成本相比 FastVGGT 降低了 4.58×（Figure 1），但异常值过滤引入了额外的聚合延迟开销。

3. **训练无关的固有限制**：作为训练无关方法，HTTM 的合并策略基于启发式相似度度量（余弦相似度），无法像训练感知方法那样通过端到端优化来学习最优合并模式。在极端压缩率下，重建精度仍会出现退化。

4. **单 GPU 推理假设**：当前设计未考虑多 GPU 分布式推理场景。在多 GPU 环境下，时间重排序和块内合并可能引入跨设备通信开销，需要额外的手动验证。

### 4. 开放问题

1. **跨架构泛化**：HTTM 的头级合并策略能否推广到其他使用全局注意力的前馈 3D 重建模型（如 DUSt3R 系列、MASt3R 等）？这些模型的令牌冗余模式可能与 VGGT 不同，需要重新验证时序重排序和异常值过滤的有效性。

2. **与其他加速技术的叠加**：HTTM 与模型量化、知识蒸馏、注意力稀疏化等技术在原理上正交，但实际叠加时能否产生累积加速效果？是否存在精度损失的叠加风险？目前缺乏系统性的组合实验。

3. **异常值过滤的自适应优化**：当前的自适应异常值过滤使用固定的百分比阈值 d% 来识别异常令牌。该阈值是否可通过学习或基于输入特征的动态调整来进一步优化，是一个值得探索的方向。

4. **分布式推理的适配**：在多 GPU 推理场景下，时间重排序需要跨设备重新组织令牌，块内合并可能破坏原有的数据并行划分。如何设计通信高效的分布式 HTTM 仍是一个开放问题。

5. **训练感知合并的可能性**：虽然 HTTM 强调训练无关的优势，但若允许轻量级微调（如合并模块的参数学习），是否能进一步提升压缩率与精度的 Pareto 前沿？这需要在部署灵活性和性能上限之间做出权衡。

## 原文 PDF

![[paperPDFs/CVPR_2026/HTTM_Head_wise_Temporal_Token_Merging_for_Faster_VGGT.pdf]]