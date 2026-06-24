---
title: "LSA: Layer-wise Sparsity Allocation for Large Language Model Pruning Based on Minimal Linear Reconstruction Error"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/LSA_Layer_wise_Sparsity_Allocation_for_Large_Language_Model_Pruning_Based_on_Minimal_Linear_Reconstruction_Error.pdf
openreview_forum_id: xq3lza5IjN
aliases:
- LWSAL
- LSA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "使用最小线性重构误差作为层/块/投影冗余度的直接度量，无需权重评分和缩减函数，从而更精确地捕捉移除权重带来的输出扰动。"
primary_logic: "线性重构误差高的层对权重移除更为鲁棒（冗余度高），可分配更高的稀疏度；误差低的层则存在更多离群重要权重（冗余度低），应保留更多参数。该误差天然支持块级和投影级非均匀分配，且对超参数不敏感。"
claims:
- "在70%整体稀疏度下，LSA在语言建模困惑度和七项零样本任务准确率上均显著优于均匀稀疏度以及OWL、DLP等先进逐层分配方法。"
- "LSA支持投影级和块级非均匀稀疏度分配，且不会像OWL和DLP那样引起严重的性能退化，反而在LLaMA3-8B等模型上实现了超越层级的性能。"
- "LSA直接用线性重构误差衡量重要性，其误差度量在均匀剪枝下也比Wanda更有效，并且对计算误差时使用的p值具有较强的鲁棒性。"
- "WikiText 上 Perplexity = 17.57"
---

# LSA: Layer-wise Sparsity Allocation for Large Language Model Pruning Based on Minimal Linear Reconstruction Error

> [!tip] 核心洞察
> 线性重构误差高的层对权重移除更为鲁棒（冗余度高），可分配更高的稀疏度；误差低的层则存在更多离群重要权重（冗余度低），应保留更多参数。该误差天然支持块级和投影级非均匀分配，且对超参数不敏感。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LSA：基于最小线性重构误差的大语言模型逐层稀疏度分配剪枝 |
| 英文题名 | LSA: Layer-wise Sparsity Allocation for Large Language Model Pruning Based on Minimal Linear Reconstruction Error |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=xq3lza5IjN); [GitHub](https://github.com/BeiYazi0/LSA) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Layer-wise Sparsity Allocation (LSA) |
| Dataset | WikiText, 7 zero-shot tasks |

> [!tip] 效果简介
> - WikiText 上，Perplexity 为 17.57，对比 27.18 (Uniform)，变化 -9.61。
> - WikiText 上，Perplexity 为 12.45，对比 20.36 (Uniform)，变化 -7.91。
> - 7 zero-shot tasks 上，Mean Accuracy (%) 为 44.77，对比 42.75 (Uniform)，变化 +2.02。

## 概述

大语言模型（LLM）剪枝面临一个核心瓶颈：现有逐层稀疏度分配方法（如 **OWL**（Yin et al., 2024）和 **DLP**（Chen et al., 2025））依赖 Wanda 式权重评分及人工设计的缩减函数来估计层重要性。这不仅需要手动选择评分指标和缩减函数，而且无法在块级或投影级粒度下稳定分配非均匀稀疏度——一旦尝试更细粒度的分配，性能会显著退化。

本文提出 **LSA（Layer-wise Sparsity Allocation）**，核心思路是用**最小线性重构误差**直接度量层/块/投影的冗余度，从而绕开权重评分和缩减函数的设计。其关键洞察是：线性重构误差高的层对权重移除更为鲁棒（冗余度高），可分配更高稀疏度；误差低的层则存在更多离群重要权重（冗余度低），应保留更多参数。该误差天然支持块级和投影级非均匀分配，且对超参数不敏感。

在 70% 整体稀疏度下，LSA 在语言建模困惑度上显著优于均匀稀疏度及 OWL、DLP 等方法（例如 LLaMA1-7B 上 SparseGPT 剪枝后困惑度从 27.18 降至 17.57，LLaMA1-13B 上从 20.36 降至 12.45），在七项零样本任务平均准确率上也取得一致提升。更重要的是，LSA 支持投影级和块级非均匀分配，在 LLaMA3-8B 等模型上实现了超越层级的性能，而 OWL 和 DLP 在相同粒度下则出现严重退化。

## 背景与动机

大语言模型（LLMs）在推理时面临巨大的计算和存储开销，剪枝是缓解这一问题的核心技术之一。非结构化剪枝通过移除单个权重来压缩模型，而逐层剪枝方法（layer-wise pruning）的核心挑战在于如何为不同层分配合适的稀疏度——即确定哪些层可以剪掉更多权重，哪些层需要保留更多参数。

现有逐层稀疏度分配方法存在一个共同瓶颈：它们依赖于**权重评分（weight score）** 和**人工设计的缩减函数（reduce function）** 来估计层重要性。具体而言，**OWL**（Yin et al., 2024）基于权重离群点分布（Layer-wise Outlier Distribution, LOD）来分配稀疏度，其定义为：

$$D ^ { l } = \frac { \sum _ { i = 1 } ^ { c _ { o } } \sum _ { j = 1 } ^ { c _ { i } } \mathbb { I } ( \mathbf { A } _ { i , j } ^ { l } > m \cdot \overline { { \mathbf { A } } } ^ { l } ) } { c _ { i } c _ { o } }$$

**DLP**（Chen et al., 2025）则使用Wanda权重得分的中位数作为层重要性指标。这两种方法都需要手动选择评分指标和缩减函数，且存在两个关键缺陷：

1. **评估粒度受限**：OWL和DLP仅在层级（layer-wise）非均匀分配上有效。当尝试更细粒度的分配——如块级（自注意力块 vs. FFN块）或投影级（q、k、v、o等不同投影矩阵）时，性能会严重退化。例如，在LLaMA1-7B上使用SparseGPT进行70%投影级稀疏度分配时，DLP的困惑度从层级的17.57急剧上升至23.26（Table 1）。

2. **超参数敏感**：OWL和DLP仅在较窄的β范围[0, 0.07]内有效，超出此范围性能迅速恶化（Figure 3）。

这些问题的根源在于：权重评分和缩减函数是对层冗余度的间接度量，无法精确捕捉移除权重后对模型输出的实际扰动。本文提出的核心洞察是：**线性重构误差（Linear Reconstruction Error）** 可以直接作为层/块/投影冗余度的度量——重构误差高的层对权重移除更为鲁棒（冗余度高），可分配更高稀疏度；误差低的层则存在更多离群重要权重（冗余度低），应保留更多参数。

LSA方法通过计算每层在移除50%最不重要权重后的最小线性重构误差，天然支持层、块、投影三级非均匀分配，且对超参数不敏感，从而系统性地解决了上述瓶颈。

## 核心创新

### 问题瓶颈：现有逐层分配依赖间接代理与人工设计

现有逐层剪枝方法（如 **OWL**（Yin et al., 2024）和 **DLP**（Chen et al., 2025））的核心瓶颈在于，它们对层重要性的评估并非直接度量冗余度，而是依赖一条间接、脆弱的因果链：

1. **权重评分**：首先计算每个权重的Wanda得分（权重大小 × 激活范数），形成权重重要性矩阵 $\mathbf{A}^l$。
2. **缩减函数**：然后通过人工设计的缩减函数（如中位数或LOD阈值）将逐权重得分聚合为单一的层重要性指标。OWL使用逐层离群点分布 $D^l$（超过均值 $m$ 倍的权重比例），DLP则直接取 $\mathbf{A}^l$ 的中位数。
3. **稀疏度映射**：最后将该指标映射到各层的稀疏度分配。

这条路径存在两个根本缺陷：**（1）需要手动选择评分指标和缩减函数**，不同的选择可能导致截然不同的分配结果，缺乏理论保证；**（2）该代理指标天然局限于层级粒度**——当试图将其推广到更细的块级（自注意力块 vs. FFN块）或投影级（q, k, v, o等线性投影）时，原有评分和缩减机制失效，导致性能严重退化（见Table 1：OWL和DLP在投影级粒度下困惑度急剧上升）。

### 核心机制：以最小线性重构误差直接度量冗余度

LSA的关键创新在于**绕过权重评分和缩减函数这两个中间环节，直接使用最小线性重构误差（Linear Reconstruction Error, LRE）作为层/块/投影冗余度的原生度量**。

线性重构误差定义为剪枝前后线性层输出的平方L2距离：

$$\mathbf{E} = \left\| \mathbf{W} \mathbf{X}^T - (\mathbf{M} \odot \mathbf{W}) \mathbf{X}^T \right\|_2^2$$

其中 $\mathbf{W}$ 为权重矩阵，$\mathbf{X}$ 为输入激活，$\mathbf{M}$ 为剪枝掩码。该误差直接量化了移除特定权重后对层输出的扰动程度——误差越大，说明被移除的权重对输出的贡献越小，该层/单元越冗余。

LSA的核心洞察在于：**线性重构误差高的层对权重移除更为鲁棒（冗余度高），应分配更高的稀疏度；误差低的层则存在更多离群重要权重（冗余度低），应保留更多参数**。这一关系在Figure 4中得到验证：归一化线性重构误差高的层，其分配的稀疏度也一致偏高，且与OWL中的LOD指标呈负相关。

### 关键改变：从间接代理到直接度量的三个维度

#### 改变一：层重要性评估方式（核心changed slot）

| 维度 | 基线方法（OWL/DLP） | LSA |
|------|---------------------|-----|
| **评估路径** | 权重得分 → 缩减函数 → 层重要性 | 线性重构误差 → 层重要性 |
| **理论基础** | 启发式：离群权重多的层更重要 | 优化驱动：最小化剪枝导致的输出扰动 |
| **超参数依赖** | 需选择评分指标和缩减函数 | 仅需设定内部剪枝比率 $p$（固定为50%，且对结果不敏感） |

具体而言，LSA通过Algorithm 1计算每个Transformer层在假定移除50%最不重要权重后的最小线性重构误差。然后将各层归一化误差通过 $I^l = 1 - \mathbf{E}^l / \sum_i \mathbf{E}^i$ 转换为相对重要性得分。这一过程无需对每个权重进行显式评分，也无需设计聚合函数，从根本上消除了基线方法中人工选择带来的不确定性。

证据强度：在均匀剪枝设置下，直接使用线性重构误差作为权重重要性指标，其困惑度和零样本准确率全面优于Wanda（Table 21, Appendix H），验证了该误差度量本身的有效性。

#### 改变二：稀疏度分配粒度（原生支持多级非均匀分配）

基线方法（OWL、DLP）仅在层级非均匀分配时有效，当扩展到块级或投影级时性能严重下降。LSA则原生支持三级非均匀分配：

- **层级**：每个Transformer层获得不同稀疏度
- **块级**：自注意力块和FFN块各自独立分配
- **投影级**：q, k, v, o等线性投影各自独立分配

这种能力源于线性重构误差的可分解性——误差可以在任意粒度（层、块、投影）上独立计算，无需修改核心算法。Table 1和Table 2显示，LSA在块级粒度下不仅没有性能退化，反而在LLaMA3-8B等使用GQA的模型上实现了超越层级的性能（块级困惑度32.94 vs. 层级39.56），因为GQA中不同投影的冗余度差异较大，更细粒度的分配能更好地匹配这种差异。

#### 改变三：超参数鲁棒性

LSA引入的唯一超参数是稀疏度范围控制参数 $\beta$，用于将重要性得分映射到 $[pr - \beta, pr + \beta]$ 区间。Figure 3的消融实验表明，LSA在 $\beta \in [0, 0.17]$ 范围内困惑度保持稳定，而OWL和DLP仅在 $[0, 0.07]$ 的窄区间内有效。此外，内部剪枝比率 $p$ 在 $\leq 70\%$ 时对最终分配影响极小（Table 22, Appendix I），进一步降低了调参负担。

### 创新总结

LSA的核心创新可概括为**用优化驱动的直接冗余度量替代启发式的间接代理评估**。这一转变使得稀疏度分配不再受限于人工设计的评分函数和缩减策略，同时天然解锁了更细粒度的分配能力，且对超参数具有显著的鲁棒性。实验证据（Table 4, Table 5）表明，在70%整体稀疏度下，LSA在语言建模困惑度和七项零样本任务准确率上均显著优于均匀稀疏度以及OWL、DLP等先进逐层分配方法。

## 整体框架

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/001_Figure_1.jpg]]
*Figure 1: (a) illustrates the weight with minimal linear reconstruction error (LRE) for linear layers within FFN and attention blocks. (b) denotes the layer-wise LRE across all Transformer layers, computed by assuming removing 50% of the weights that contribute least to the reconstruction error in each layer. (c) represents the allocation of different sparsity rates based on the principle that layers with lower reconstruction error should exhibit lower sparsity*

LSA 的整体 pipeline 围绕一个核心观察展开：**线性重构误差（Linear Reconstruction Error, LRE）高的层对权重移除更为鲁棒，可分配更高稀疏度；误差低的层则包含更多离群重要权重，应保留更多参数**。基于这一观察，LSA 将逐层稀疏度分配问题转化为三个顺序模块，如图 1 所示。

### Pipeline 模块构成

**模块一：线性重构误差计算**

对于每个 Transformer 层（或更细粒度的块/投影），LSA 首先假设移除该单元中 50% 最不重要的权重，然后通过 Algorithm 1 计算在该设定下的最小线性重构误差 $E^l$。该误差定义为剪枝前后线性层输出的平方 L2 范数差：

$$\mathbf { E } = \left\| \mathbf { W } \mathbf { X } ^ { T } - ( \mathbf { M } \odot \mathbf { W } ) \mathbf { X } ^ { T } \right\| _ { 2 } ^ { 2 }$$

其中 $\mathbf{W}$ 为权重矩阵，$\mathbf{X}$ 为输入激活，$\mathbf{M}$ 为二值剪枝掩码。Algorithm 1 通过贪心策略最小化该误差，其核心步骤包括：
- 构建输入激活的 Gram 矩阵 $\mathbf{H} = \mathbf{X}^T \mathbf{X}$；
- 维护每个输出通道的累积误差向量 $\mathbf{e}_{k,:}$；
- 每次迭代选择当前误差最小的权重进行剪枝，并通过 $\mathbf{e}_{k,:} \leftarrow \mathbf{e}_{k,:} + 2\mathbf{W}_{k,i}(\mathbf{W}_{k,:} \odot \mathbf{H}_{i,:})$ 更新误差向量。

这一过程直接量化了移除权重对层输出的扰动程度，无需依赖 Wanda 式的权重评分（权重大小 × 激活范数）或人工设计的缩减函数。

**模块二：重要性转换**

获得各单元的归一化误差后，LSA 将其转换为相对重要性得分：

$$I^{l} = 1 - \frac{\mathbf{E}^{l}}{\sum_{i} \mathbf{E}^{i}}$$

该公式的逻辑是：重构误差越大的层，其重要性得分越低（即越冗余），应被分配更高的稀疏度。这种转换天然适用于层、块（自注意力/FFN）、投影（q, k, v, o 等）三级粒度。

**模块三：稀疏度映射与分配**

给定目标整体稀疏度 $pr$ 和超参数 $\beta$，LSA 将重要性得分压缩到 $[0, 2\beta]$ 区间，使各单元的稀疏度 $s^l$ 被约束在 $[pr - \beta, pr + \beta]$ 范围内。对于块级或投影级分配，LSA 通过 $s = (pr \times N + (\mathrm{mean}(d) - d) \times \mathrm{mean}(N)) / N$ 计算各子单元的具体稀疏度，同时保证整体稀疏度不变。

### 输入输出流

- **输入**：预训练 LLM 的权重矩阵、校准数据集（从 C4 中随机抽取 128 个样本，每个 2048 token）产生的激活值、目标整体稀疏度 $pr$、超参数 $\beta$。
- **中间产物**：各层/块/投影的线性重构误差 $E^l$ 及对应的重要性得分 $I^l$。
- **输出**：各单元的非均匀稀疏度分配方案，可直接与 SparseGPT、Wanda、ADMM-Grad 等底层剪枝方法结合使用。

### 与基线方法的关键差异

| 设计维度 | OWL / DLP | LSA |
|---------|-----------|-----|
| 层重要性评估 | 基于 Wanda 权重得分 + 缩减函数（LOD 阈值或中位数） | 直接计算最小线性重构误差 |
| 支持粒度 | 仅层级，块级/投影级分配导致性能退化 | 原生支持层、块、投影三级分配 |
| 超参数敏感性 | 仅 $\beta \in [0, 0.07]$ 内有效 | $\beta \in [0, 0.17]$ 内保持稳定（Figure 3） |

这一框架的核心优势在于：线性重构误差作为冗余度的直接度量，避免了权重评分和缩减函数选择带来的不确定性，且对内部剪枝比率 $p$（≤70% 时）和 $\beta$ 超参数均表现出较强的鲁棒性。

## 核心模块与公式推导

LSA 的方法核心在于**用最小线性重构误差（Linear Reconstruction Error, LRE）直接量化各计算单元的冗余度**，从而绕过现有逐层分配方法对权重评分和人工缩减函数的依赖。整个流程由三个关键模块串联构成。

---

### 模块一：线性重构误差计算

对于 Transformer 中的任意线性层（权重矩阵 $\mathbf{W} \in \mathbb{R}^{c_o \times c_i}$，输入激活 $\mathbf{X}$），剪枝引入的二进制掩码 $\mathbf{M}$ 造成的输出扰动由线性重构误差定义：

$$
\mathbf{E} = \left\| \mathbf{W} \mathbf{X}^T - (\mathbf{M} \odot \mathbf{W}) \mathbf{X}^T \right\|_2^2
$$

其中 $\odot$ 表示逐元素乘积。该误差直接度量了移除特定权重后层输出的平方 L2 偏差，是 LSA 冗余度评估的唯一信号来源。

为了在分配稀疏度之前获得各层的冗余度量，LSA 采用 **Algorithm 1** 所示的贪心最小化过程：对每个层，假设移除 $p=50\%$ 最不重要的权重，通过迭代选择对当前重构误差贡献最小的权重进行掩码，最终得到该层在 50% 稀疏度下的最小线性重构误差 $\mathbf{E}^l$。这一过程的关键性质是：

- **$p$ 值不敏感**：实验表明，计算误差时使用的内部剪枝比率 $p \leq 70\%$ 时，最终稀疏度分配几乎不变（Table 22），因此固定 $p=50\%$ 即可。
- **误差度量本身优于 Wanda**：在均匀剪枝设置下，直接用线性重构误差作为权重重要性指标，其困惑度和零样本准确率全面优于 Wanda 权重得分（Table 21）。

---

### 模块二：重要性转换

获得各计算单元（层/块/投影）的归一化线性重构误差后，LSA 将其转换为相对重要性得分：

$$
I^{l} = 1 - \frac{\mathbf{E}^{l}}{\sum_{i} \mathbf{E}^{i}}
$$

该公式的因果逻辑是：**线性重构误差越高的层，对权重移除越鲁棒（冗余度高），因此重要性越低**，应分配更高稀疏度；反之，误差低的层存在更多离群重要权重，需保留更多参数。这一转换天然支持层、块（自注意力/FFN）和投影（q, k, v, o 等）三级粒度的非均匀分配，无需额外设计。

---

### 模块三：稀疏度映射与分配

给定目标整体稀疏度 $pr$ 和超参数 $\beta$，LSA 将重要性得分线性映射到 $[pr - \beta, pr + \beta]$ 区间，生成各单元的具体稀疏度 $s^l$。$\beta$ 控制分配的非均匀程度：

- **$\beta=0$ 退化为均匀稀疏度**。
- **$\beta$ 增大允许更极端的层间差异**。

实验表明 LSA 对 $\beta$ 具有极强的鲁棒性：在块级分配下，$\beta \in [0, 0.17]$ 范围内困惑度保持稳定，而 OWL 和 DLP 仅在 $[0, 0.07]$ 内有效（Figure 3）。这一性质源于线性重构误差本身对冗余度的准确刻画，而非对超参数的精细调参。

---

### 关键公式汇总

| 公式 | LaTeX | 变量含义 |
|------|-------|----------|
| 线性重构误差 | $\mathbf{E} = \|\mathbf{W}\mathbf{X}^T - (\mathbf{M} \odot \mathbf{W})\mathbf{X}^T\|_2^2$ | $\mathbf{W}$: 权重矩阵; $\mathbf{X}$: 输入激活; $\mathbf{M}$: 二进制掩码 |
| 层重要性得分 | $I^{l} = 1 - \frac{\mathbf{E}^{l}}{\sum_{i} \mathbf{E}^{i}}$ | $\mathbf{E}^{l}$: 第 $l$ 层的最小线性重构误差 |
| 贪心通道剪枝误差更新 | $\mathbf{e}_{k,:} \leftarrow \mathbf{e}_{k,:} + 2\mathbf{W}_{k,i}(\mathbf{W}_{k,:} \odot \mathbf{H}_{i,:})$ | 用于结构化剪枝中更新每个输出通道的累积误差向量（Eq 4） |

> **注意**：结构化剪枝场景下，线性重构误差等价于矩阵 $\mathbf{S}$ 中被剪枝通道索引子矩阵的元素之和（Eq 3），这是 Algorithm 1 贪心选择子矩阵的理论基础（Figure 2 展示了 25% 结构化稀疏度下的子矩阵选择过程）。

## 实验与分析

### 核心问题与实验设计逻辑

现有逐层剪枝方法（如 **OWL** (Yin et al., 2024) 和 **DLP** (Chen et al., 2025)）面临两个瓶颈：一是依赖 Wanda 式权重评分和人工设计的缩减函数来估计层重要性，需要手动选择评分指标和缩减函数；二是无法在更细粒度（块级、投影级）下稳定分配非均匀稀疏度，导致性能显著下降。LSA 的核心假设是：**线性重构误差高的层对权重移除更为鲁棒（冗余度高），可分配更高的稀疏度；误差低的层则存在更多离群重要权重（冗余度低），应保留更多参数**。基于此，实验设计围绕三个层次展开：(1) 验证 LSA 在层级非均匀分配上的有效性；(2) 检验其在块级和投影级的泛化能力；(3) 通过消融实验确认各设计选择的必要性。

所有实验均使用从 C4 中随机抽取的 128 个样本（每个样本 2048 token）作为校准数据，每个实验配置重复至少 5 次并报告平均结果。对比方法均与相同的底层剪枝方法（SparseGPT、Wanda）结合，保持其他设置一致。

### 主实验结果

#### 语言建模困惑度

在 70% 整体非结构化稀疏度下，LSA 在 WikiText 困惑度上显著优于均匀稀疏度及 OWL、DLP 等逐层分配方法。以 SparseGPT 为底层剪枝器时，LLaMA1-7B 的困惑度从均匀方法的 27.18 降至 **17.57**（降低 9.61），LLaMA1-13B 从 20.36 降至 **12.45**（降低 7.91）（Table 4）。这一优势在 LLaMA2 系列和 Wanda 剪枝器下同样保持。在更大规模的 LLaMA1-30B 上，LSA 仍持续优于所有基线，表明方法具有良好的模型规模可扩展性。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/010_Table_4.jpg]]
*Table 4: Perplexity results on WikiText dataset Table 5: Comparison of mean zero-shot accurawith 70% unstructured sparsity across the cies (%) for pruned LLaMA1 and LLaMA2 mod-LLaMA1 and LLaMA2 models. The best per- els at 70% unstructured sparsity. The best perforformance result is indicated in bold. mance result is indicated in bold*

#### 零样本任务准确率

在七项零样本任务（WinoGrande、HellaSwag、BoolQ、PIQA、OBQA、ARC-e、ARC-c）的平均准确率上，LSA 同样表现最优。LLaMA1-7B 在 70% 稀疏度下，LSA 的平均准确率为 **44.77%**，高于均匀方法的 42.75%（Table 5）。在更先进的模型上（LLaMA3-8B、Qwen2.5-7B、Qwen3-8B），LSA 继续保持优势，Qwen2.5-7B 上 LSA 的平均准确率达到 **49.66%**（Table 10）。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/011_Table_5.jpg]]

#### 推理加速

结合 DeepSparse 推理引擎，LSA 在 70% 稀疏度下实现了超过 **3.0 倍**的端到端解码加速（Table 6），验证了非均匀稀疏度分配在实际部署中的有效性。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/012_Table_6.jpg]]
*Table 6: End-to-end decoding latency and throughput of the LLaMA2-7B-chat-hf model using the DeepSparse inference engine with LSA*

### 细粒度分配：块级与投影级

LSA 的关键优势在于原生支持块级（自注意力/FFN）和投影级（q、k、v、o 等）非均匀分配，而 OWL 和 DLP 在这些粒度下性能严重退化。

**块级分配**：在 LLaMA3-8B 上，LSA 块级分配的困惑度为 **32.94**，显著优于其层级分配的 39.56（Table 2）。这是因为 LLaMA3 采用 GQA（分组查询注意力），不同投影间的冗余度差异较大，块级分配能更精细地捕捉这种差异。在 Qwen2.5-7B 上，块级 LSA 的零样本平均准确率进一步提升至 **51.82%**（Table 10）。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/004_Table_2.jpg]]
*Table 2: Results of block-wise (B) granularity on perplexity using the LLaMA3 model with the WikiText dataset at 70% sparsity. The best performance results are highlighted in bold*

**投影级分配**：在投影级粒度下，OWL 和 DLP 均出现严重性能退化，而 LSA 的退化幅度远小于 DLP。例如 LLaMA1-7B 上，LSA 投影级困惑度为 19.46，而 DLP 为 23.26；LLaMA2-7B 上 LSA 为 21.15，DLP 则高达 28.05（Table 1）。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/003_Table_1.jpg]]
*Table 1: Comparison of sparsity allocation tech- Table 3: Comparison of LOD and Perplexity on niques across three types of granularity on Wiki- the WikiText dataset at 70% sparsity. The best Text dataset: layer-, block-, and projection-wise. performance result is indicated in bold*

### 消融实验

#### 超参数 β 的鲁棒性

LSA 对超参数 β 不敏感。在块级剪枝设置下，LSA 在 β ∈ [0, 0.17] 范围内困惑度保持稳定，而 OWL 和 DLP 仅在 [0, 0.07] 的窄区间内有效（Figure 3）。这一特性使得 LSA 在实际应用中几乎不需要调参。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/006_Figure_3.jpg]]
*Figure 3: Perplexity of the LLaMA3-8B model on the WikiText dataset, pruned using various $\beta$ at 70% sparsity in block-wise (B)*

#### 内部剪枝比率 p 的影响

计算线性重构误差时使用的内部剪枝比率 p（默认为 50%）对最终稀疏度分配影响极小。实验表明，当 p ≤ 70% 时，稀疏度分配结果几乎不变（Table 22, Appendix I），说明该超参数不敏感，进一步降低了方法的使用门槛。

#### 线性重构误差作为权重重要性指标

在均匀剪枝设置下，直接使用线性重构误差作为权重重要性指标，其性能（困惑度和准确率）全面优于 Wanda（Table 21, Appendix H）。这验证了线性重构误差本身就是一个更有效的冗余度量，无需依赖 Wanda 式的权重×激活范数评分。

#### 权重离群点保存能力

LSA 在 70% 稀疏度下实现了最高的 LOD（层离群点分布）和最低的困惑度（Table 3），表明其稀疏度分配策略能更有效地保留关键权重离群点。这一结果与 Figure 4 的发现一致：线性重构误差高的层恰好也是 LOD 低的层，LSA 对这些层分配更高稀疏度，从而在整体上更好地保护了重要权重。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/009_Figure_4.jpg]]
*Figure 4: Comparison of layer-wise sparsity distributions. The background bar chart illustrates the normalized linear reconstruction error. In each subplot, the horizontal axis represents the layer index, the left vertical axis denotes the error, and the right vertical axis indicates the layer-wise sparsity*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/005_Table_3.jpg]]

### 与其他压缩方法的集成

LSA 作为稀疏度分配策略具有良好的可组合性。实验表明，LSA 可与结构化剪枝（LLM-Pruner，Table 12）、N:M 混合稀疏度（Table 13）、量化（Table 14）以及 ADMM-Grad 剪枝（Table 11）等方法结合，均能带来一致的性能提升。在 ADMM-Grad 剪枝下，LSA 在 LLaMA3-8B 上的 C4 困惑度为 **30.09**，并在 7 项零样本任务中的 5 项上取得最高准确率。

### 计算效率

LSA 的剪枝度量计算时间与均匀基线相当甚至更低。在 LLaMA1-30B 上，LSA 的计算时间为 1285.27 秒，低于均匀方法的 1359.40 秒（Table 7）。这说明 LSA 在提升性能的同时未引入显著的计算开销。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/013_Table_7.jpg]]
*Table 7: Comparison of time on LLaMA1 for computing the pruning metric (seconds)*

### 微调恢复

经 LoRA 微调后，LSA 剪枝模型的性能可大幅恢复。LLaMA1-7B 在 70% 稀疏度下的困惑度从未微调的 20.66 降至微调后的 **12.27**（Table 8），表明 LSA 保留的权重结构有利于后续微调恢复。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/014_Table_8.jpg]]

### 补充图表

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_xq3lza5IjN/figures/015_Table_9.jpg]]
*Table 9: WikiText perplexity of various LLMs pruned by Uniform and Ours using Wanda*

## 方法谱系与知识库定位

### 1 问题定位：逐层剪枝中的冗余度量瓶颈

现有逐层剪枝方法的核心瓶颈在于**层重要性评估依赖间接代理指标**。主流方法遵循两阶段范式：(1) 计算逐权重的重要性得分（如Wanda的权重大小×激活范数）；(2) 通过人工设计的缩减函数（reduce function）将得分聚合为层级标量。**OWL** (Yin et al., 2024) 使用层内权重离群点比例（Layer-wise Outlier Distribution, LOD）作为冗余度量——离群点越少则该层越可剪；**DLP** (Chen et al., 2025) 则将Wanda得分的中位数直接作为层冗余指标。这两种方法均需手动选择评分指标和缩减函数，且其层重要性估计与剪枝后模型的实际输出误差之间缺乏直接对应关系。

LSA的关键突破在于**绕过代理指标，直接以最小线性重构误差作为冗余度量**。其核心逻辑链为：对每层假设移除50%最不重要权重，计算该操作引起的输出扰动（即线性重构误差）；误差高的层对权重移除更为鲁棒（冗余度高），应分配更高稀疏度；误差低的层则存在更多离群重要权重（冗余度低），应保留更多参数。这一设计消除了权重评分和缩减函数两个人工设计环节，使重要性评估直接锚定于剪枝对模型输出的因果影响。

### 2 粒度扩展：从层级到投影级的原生支持

现有方法的另一结构性局限在于**仅支持层级非均匀分配**。当OWL和DLP被直接应用于更细粒度（块级或投影级）时，性能会出现严重退化——Table 1显示DLP在投影级分配下，LLaMA2-7B的困惑度从层级的21.15飙升至28.05。这是因为基于Wanda得分中位数或LOD阈值的缩减函数在细粒度下丧失了统计稳定性：块或投影内的权重数量远少于整层，离群点比例或中位数的估计方差急剧增大。

LSA的线性重构误差天然支持细粒度分配。由于误差计算（Algorithm 1）对任意线性层子单元均适用，只需将计算单元从层替换为块（自注意力块/FFN块）或投影（q, k, v, o等），即可获得对应粒度的冗余度量。实验表明，在LLaMA3-8B等使用GQA的模型上，块级分配的困惑度（32.94）显著优于层级分配（39.56）（Table 2），原因在于GQA中不同投影的冗余度差异较大，层级聚合会掩盖这种异质性。

### 3 与底层剪枝方法的解耦关系

LSA属于**稀疏度分配策略**，而非权重选择策略。它可与任意底层剪枝方法（SparseGPT、Wanda、Magnitude、ADMM-Grad）组合使用。其工作流为：先通过LSA确定每层/块/投影的目标稀疏度，再由底层剪枝方法在该稀疏度约束下选择具体权重进行移除。这种解耦设计使LSA具有广泛的兼容性——Table 4和Table 5分别验证了其与SparseGPT和Wanda组合在LLaMA1/2系列上的有效性；Table 11进一步展示了与ADMM-Grad的组合效果。

值得注意的是，LSA的误差度量本身在均匀剪枝设置下也比Wanda更有效。Appendix H（Table 21）表明，使用线性重构误差作为权重重要性指标进行均匀剪枝，其在困惑度和零样本准确率上全面优于Wanda。这意味着LSA的冗余度量不仅服务于稀疏度分配，也揭示了更本质的权重重要性排序。

### 4 超参数鲁棒性与适用边界

LSA引入两个超参数：误差计算时的内部剪枝比率p（Algorithm 1中固定为50%）和稀疏度映射时的范围控制参数β（Section 4.2）。消融实验表明两者均具有强鲁棒性：

- **p值不敏感**：Table 22（Appendix I）显示，p在≤70%范围内变化时，最终稀疏度分配几乎不变，因为不同p值下的相对误差排序保持稳定。
- **β值鲁棒性强**：Figure 3表明，LSA在β∈[0, 0.17]范围内困惑度保持稳定，而OWL和DLP仅在[0, 0.07]内有效。更宽的β容忍区间意味着LSA在实际部署中无需精细调参。

适用边界方面，LSA的当前验证集中在70%整体稀疏度下的非结构化剪枝场景，且主要基于LLaMA系列模型。虽然Table 9和Table 10展示了在Qwen2.5-7B、Qwen3-8B等更先进模型上的泛化能力，但缺乏对更高稀疏度（>80%）或结构化剪枝场景下的系统评估。此外，LSA的误差计算基于校准数据集（C4中128个样本），其对不同领域数据的敏感性尚未被充分探索。

### 5 在知识库中的定位

LSA在LLM剪枝方法谱系中占据**稀疏度分配策略**这一细分位置，与以下工作形成直接对比或互补关系：

- **vs. OWL / DLP**：同属逐层非均匀分配方法，但LSA以直接误差度量替代代理指标+缩减函数的范式，在精度、粒度和鲁棒性三个维度上均形成优势。
- **vs. Uniform Sparsity**：作为非均匀分配方法的统一对比基线，LSA在70%稀疏度下实现了显著且一致的性能提升（Table 4：LLaMA1-7B困惑度从27.18降至17.57）。
- **vs. 结构化剪枝方法**：LSA的误差计算框架（Algorithm 1）本身支持结构化剪枝（通过子矩阵选择，见Figure 2和Eq (3)），但在正文实验中主要验证非结构化场景，结构化扩展仅见于Appendix C。
- **与微调恢复的关系**：Table 8显示LSA剪枝后的模型经LoRA微调可大幅恢复性能（LLaMA1-7B困惑度从20.66降至12.27），表明LSA保留的权重结构对后续恢复训练友好。

**开放问题**：当前分析中未发现论文明确指出的局限性声明或未来工作方向。需要进一步验证的问题包括：(1) LSA在更高稀疏度（>80%）下的性能退化模式；(2) 误差计算对校准数据分布的敏感性；(3) 与量化、N:M稀疏等压缩技术的组合效果（文中提及Appendix C有相关实验，但本部分未覆盖其具体结果，需手动核实）。

## 原文 PDF

![[paperPDFs/ICLR_2026/LSA_Layer_wise_Sparsity_Allocation_for_Large_Language_Model_Pruning_Based_on_Minimal_Linear_Reconstruction_Error.pdf]]
