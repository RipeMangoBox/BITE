---
title: "VLM-Pruner: Buffering for Spatial Sparsity in an Efficient VLM Centrifugal Token Pruning Paradigm"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VLM_Pruner_Buffering_for_Spatial_Sparsity_in_an_Efficient_VLM_Centrifugal_Token_Pruning_Paradigm.pdf
project_link: null
code_link: "https://github.com/Casey-bit/VLMPruner"
aliases:
- VP
- VLM-Pruner
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: BSS准则通过调节候选token与已选集合的最小空间距离来调制特征相似度（λ>0），从而控制选择过程由近及远，实现离心式增长。
primary_logic: 在贪婪去冗余选择中引入空间邻近性先验，使算法优先密实局部邻域细节再向外扩张，既避免重复又保持物体细节完整性。
claims:
- VLM-Pruner在5个VLM、88.9%剪枝率下一致优于FastV、DART、DivPrune等强基线（Figure 1）。
- 去除BSS中的归一化最近距离项后，平均性能下降1.11%（Table 6 / Section 4.5）。
- 与冗余去除方法（DART、DivPrune）相比，VLM-Pruner选择的token分布更集中，边缘token数量更少，且能保留更多精细细节（Figure 2, Figure 5）。
- 仅前两阶段（无Stage 3）仍超过其他方法约5%绝对点（Qwen2-VL-7B, Table 13）。
---

# VLM-Pruner: Buffering for Spatial Sparsity in an Efficient VLM Centrifugal Token Pruning Paradigm

> [!tip] 核心洞察
> 在贪婪去冗余选择中引入空间邻近性先验，使算法优先密实局部邻域细节再向外扩张，既避免重复又保持物体细节完整性。

| 字段 | 内容 |
|------|------|
| 中文题名 | VLM-Pruner：一种平衡冗余与空间稀疏性的高效VLM离心式Token剪枝方法 |
| 英文题名 | VLM-Pruner: Buffering for Spatial Sparsity in an Efficient VLM Centrifugal Token Pruning Paradigm |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.02700) · [Code](https://github.com/Casey-bit/VLMPruner) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VLM-Pruner |
| Dataset | LLaVA-1.5-7B, LLaVA-1.5-13B, LLaVA-Next-7B, Qwen2-VL-7B |

> [!tip] 效果简介
> - LLaVA-1.5-7B (64 tokens, ↓88.9%) 上，Avg. 相对上界保留率 95.61% vs FastV 84.60%, DART 92.71%, DivPrune 93.68% (+1.93% vs DivPrune)。
> - LLaVA-1.5-13B (64 tokens, ↓88.9%) 上，Avg. 92.68% vs FastV 84.75%, DART 88.12%, DivPrune 90.20% (+2.48% vs DivPrune)。
> - LLaVA-Next-7B (dynamic resolution, 11.1% tokens) 上，Avg. 91.60% vs FastV 84.02%, DART 90.35%, DivPrune 89.02% (+1.25% vs DART)。

## 概要

视觉语言模型（VLM）在推理时需处理大量视觉token，导致计算开销急剧膨胀。现有训练无关的token剪枝方法可归为两类：**重要性驱动方法**（如**FastV**, ECCV 2024；**SparseVLM**, ICML 2025）倾向于保留语义相似的高分token，造成冗余累积；**冗余去除方法**（如**DART**, EMNLP 2025；**DivPrune**, CVPR 2025）虽能提升多样性，却使token分布过于分散，丢失物体局部精细细节。这一“冗余-稀疏性”失衡构成了当前VLM高效推理的核心瓶颈。

**VLM-Pruner**提出了一种**离心式token剪枝范式**，核心创新在于引入**缓冲空间稀疏性（Buffering for Spatial Sparsity, BSS）准则**：在贪婪去冗余选择过程中，通过候选token与已选集合的最小空间距离动态调制特征相似度，强制算法优先密实局部邻域细节，再由近及远向外扩张。该方法遵循三阶段流水线——（i）在token key空间以max-min策略初始化少量多样化枢轴；（ii）在BSS调制下并行批次贪婪选择，阈值退火，实现离心式增长；（iii）通过相似性加权聚合（SWA）将丢弃token的信息回注到保留token中，恢复外围信息。整个过程无需训练，仅依赖前一层LLM解码器的token特征。

在5个VLM、13个评测基准上，VLM-Pruner以88.9%的剪枝率一致优于所有强基线：在LLaVA-1.5-7B上平均相对上界保留率达95.61%（较DivPrune提升+1.93%），在Qwen2-VL-7B上达92.58%（+3.65%），在LLaVA-Video-7B上达90.55%（+5.48%），同时实现端到端推理加速。消融实验证实，移除BSS中的归一化距离项导致平均性能下降1.11%，验证了空间邻近性先验在平衡冗余与细节完整性中的关键作用。

视觉语言模型（VLM）将视觉编码器与大型语言模型（LLM）级联，在图像/视频理解任务上取得了显著进展。然而，视觉编码器产生的视觉token数量通常远超文本token——例如LLaVA-1.5对每张图像提取576个视觉token——导致LLM解码器的自注意力计算开销随token数量平方增长，严重制约了推理效率。

**核心瓶颈**：现有训练无关（training-free）的token剪枝方法可归为两类，但均存在结构性缺陷。**重要性驱动方法**（如**FastV**, ECCV 2024; **SparseVLM**, ICML 2025; **PDrop**, CVPR 2025）依据注意力分数等重要性指标保留token，倾向选择特征相似的冗余token，造成信息重复。**冗余去除方法**（如**DART**, EMNLP 2025; **DivPrune**, CVPR 2025）通过最大化token间多样性来避免冗余，但生成的保留token分布过于分散，丢失了物体内部的精细细节。两类方法都无法同时兼顾**多样性**与**局部细节完整性**：前者冗余过多，后者细节缺失。

**因果机制**：这一困境的根源在于，现有方法在选择token时缺乏**空间邻近性先验**。重要性方法忽略空间分布，冗余去除方法则过度追求全局分散，均未利用“物体细节集中在局部邻域”这一视觉信号的基本结构属性。

**本文动机**：基于上述分析，本文提出VLM-Pruner，一种训练无关的**离心式token剪枝范式**。其核心思想是：在贪婪去冗余选择中引入空间邻近性先验，使算法优先密实局部邻域细节，再逐步向外扩张，从而在避免冗余的同时保持物体细节完整性。该方法通过**BSS（Buffered Spatial Sparsity）准则**调节候选token与已选集合的最小空间距离来调制特征相似度，实现由近及远的离心式增长，显式平衡冗余去除与空间稀疏性。

## 核心方法与创新机理

VLM-Pruner的核心创新在于提出了一种**离心式Token剪枝范式（Centrifugal Token Pruning）**，通过在贪婪去冗余选择中引入空间邻近性先验，使算法优先密实局部邻域细节再向外扩张，从根本上解决了既有方法无法同时兼顾多样性与局部细节完整性的瓶颈。

### 问题诊断：冗余去除与细节保留的内在冲突

现有训练无关的token剪枝方法可归为两类，但各自存在结构性缺陷：

- **重要性驱动方法**（如**FastV**, ECCV 2024；**SparseVLM**, ICML 2025；**PDrop**, CVPR 2025）倾向于保留注意力权重高的token，但这些高重要性token在特征空间中往往高度相似，导致保留集合存在大量冗余，浪费了有限的token预算。
- **冗余去除方法**（如**DART**, EMNLP 2025；**DivPrune**, CVPR 2025）通过最大化保留token间的多样性来避免冗余，但生成的token分布过于分散，丢失了物体边界的精细细节，在需要细粒度视觉理解的任务（如OCR）上表现不佳。

这一瓶颈的本质在于：**多样性与局部完整性是一对需要显式平衡的目标**，而既有方法仅优化其中一端。

### 核心机制：BSS准则与离心式增长

VLM-Pruner的关键创新是通过**缓冲空间稀疏性准则（Buffering for Spatial Sparsity, BSS）**来调制token间的特征相似度，从而实现由近及远的有序选择。具体而言，BSS在候选token与已选集合的余弦相似度上施加一个空间距离调制因子：

$$\widetilde{M}_{ij} = M_{ij} (1 + \lambda \bar{\delta}_i(S))$$

其中 $M_{ij}$ 为降维后的余弦相似度，$\bar{\delta}_i(S)$ 为候选token $i$ 到已选集合 $S$ 的归一化最近空间距离，$\lambda > 0$ 为调制强度。该设计的因果逻辑是：**空间距离越远的候选token，其相似度被人工放大，从而在贪婪选择中降低被选中的概率**。这迫使算法优先在已选token的空间邻域内进行密集覆盖，待局部细节充分保留后，选择才逐步向外扩张——形成“离心式”增长模式。

消融实验为BSS的有效性提供了决定性证据：移除BSS中的归一化最近距离项（即仅使用原始余弦相似度）后，平均性能下降**1.11%**（Table 6），证实空间邻近性先验是性能增益的核心来源。

### 三阶段流水线的协同设计

VLM-Pruner将离心式剪枝范式落实为三个互补阶段，每个阶段对应一个changed slot：

1. **枢轴初始化（Stage 1）**：采用max-min策略在token key空间选取 $\kappa$ 个多样化枢轴（$\kappa=4$），粗覆盖不同语义区域。相比传统的top-k重要性初始化或随机初始化，该策略确保选择起点在特征空间中充分分散，为后续离心扩张提供稳健锚点。消融表明，用Top-4 L1距离取代max-min枢轴初始化会导致性能下降**1.27%**（Table 6）。

2. **带BSS准则的并行贪婪选择（Stage 2）**：在BSS调制下按非冗余分数 $r_i = 1 - \max_{j \in \mathcal{S}} \widetilde{M}_{ij}$ 排序，通过并行批次选择和阈值退火机制，由近及远扩展保留集。该阶段是离心式增长的核心执行环节。

3. **相似性加权聚合（SWA, Stage 3）**：将丢弃token按最大相似度分配给保留token，通过归一化加权聚合恢复外围信息，弥补远端token被丢弃造成的信息损失。聚合权重 $\beta=0.3$ 在OCRBench上取得最优结果（279），而去掉Stage 3后平均性能从**95.30%**降至**95.07%**（LLaVA-1.5-7B, Table 12），验证了信息恢复的必要性。

仅前两阶段（无Stage 3）在Qwen2-VL-7B上仍超过FastV、DART、DivPrune等强基线约**5个绝对百分点**（Table 13），表明BSS驱动的离心选择本身已具备显著优势。

### 与基线方法的本质差异

| 维度 | 重要性驱动方法 | 冗余去除方法 | VLM-Pruner |
|------|---------------|-------------|------------|
| 选择策略 | 纯重要性排序 | 纯多样性最大化 | BSS调制的离心式选择 |
| 空间先验 | 无 | 无 | 归一化最近空间距离调制 |
| 枢轴初始化 | top-k重要性 | 随机/启发式 | max-min多样化选择 |
| 丢弃token处理 | 直接丢弃 | 直接丢弃 | SWA加权聚合恢复 |
| 特征通道 | 全通道 | 全通道 | top-q高方差通道筛选 |

定性可视化（Figure 2, Figure 5）进一步印证了机制差异：VLM-Pruner选择的token分布更集中，边缘token数量更少，且能保留更多精细细节；而DART和DivPrune的token分布明显更分散，在物体边界处容易丢失关键信息。

VLM-Pruner 提出一种**训练无关的离心式Token剪枝范式**，在LLM解码器的单层内完成视觉token的选择与压缩。其核心设计理念是：在贪婪去冗余选择中引入空间邻近性先验，使算法优先密实局部邻域细节再向外扩张，从而同时避免token冗余并保持物体细节完整性。

### 三阶段流水线

整个方法由三个串行阶段构成，对应 Figure 3 所示的由近及远的离心式扩展过程：

![[assets/figures/papers/paper_list_l2244_https_arxiv_org_abs_2512_02700/figures/003_Figure_3.jpg]]
*Figure 3: Centrifugal token pruning paradigm of VLM-Pruner. (a) Pipeline: In the i-th decoder layer of the LLM, VLM-Pruner follows a near-to-far selection order, (b) starting with pivot tokens, (c) gradually expanding outward from neighborhoods, and (d) ultimately recovering the outermost information from the discarded tokens via SWA. The similarity computed under BSS criterion makes candidate tokens spatially closer to selected ones more likely to be chosen. Color transition from green to red indicates decreasing selection probability. C and S denote candidate and selected tokens, respectively. After applying BSS, the closer candidate C2 is prioritized over C1*

1. **Pivot初始化（Stage 1）**：在token key空间通过max-min策略选取κ个多样化枢轴，粗粒度覆盖不同语义区域，为后续扩展提供空间上分散的锚点。
2. **带BSS准则的并行贪婪选择（Stage 2）**：在BSS调制下按非冗余分数排序，并行批次选择，阈值退火，由近及远地将候选token纳入保留集。
3. **相似性加权聚合（SWA, Stage 3）**：将丢弃token按最大相似度分配给保留token，通过归一化加权聚合恢复外围信息，弥补剪枝造成的信息损失。

### 模块关系与数据流

给定LLM解码器第i层的视觉token集合，VLM-Pruner的完整处理流程如下：

- **输入**：来自前一层解码器的视觉token隐藏状态 $\mathbf{H} \in \mathbb{R}^{N \times d}$ 及对应的token key $\mathbf{K} \in \mathbb{R}^{N \times d}$，其中N为视觉token总数（如576）。
- **通道筛选**：对隐藏状态按通道方差排序，仅保留top-q个高方差通道（默认q=256），得到降维特征 $\tilde{\mathbf{H}} \in \mathbb{R}^{N \times q}$，以减少后续相似度计算开销。
- **空间坐标映射**：将token索引映射到二维特征图空间坐标，用于计算token间的欧氏距离及归一化最近距离。
- **Stage 1 → Stage 2**：以κ个枢轴为初始保留集，在BSS调制相似度下并行贪婪扩展，通过阈值τ的指数衰减控制选择终止，最终得到保留token集合。
- **Stage 2 → Stage 3**：将丢弃token按与保留token的最大余弦相似度进行分配，通过SWA以权重β=0.3将丢弃token的信息聚合到对应的保留token中，输出最终的压缩token表示。

### 关键控制参数

| 参数 | 默认值 | 作用 |
|------|--------|------|
| κ | 4 | 枢轴数量，控制初始语义覆盖范围 |
| q | 256 | 高方差通道数，平衡计算效率与特征保真度 |
| λ | 0.5 | BSS空间距离调制强度，控制离心扩展的紧密度 |
| τ(0) | 0.8 | 初始选择阈值，控制保留token的筛选严格度 |
| B | 16 | 并行批次大小，影响选择速度与性能平衡 |
| β | 0.3 | SWA聚合权重，控制丢弃token信息的回注比例 |

### 离心式选择的核心机制

BSS准则通过调节候选token与已选集合的最小空间距离来调制特征相似度：距离越远的候选token，其相似度被放大越多，从而降低被选中的概率。这一机制使选择过程天然遵循由近及远的顺序——优先填充已选token的邻域，再逐步向外扩张，最终形成**密实局部、稀疏外围**的token分布格局。Figure 3直观展示了这一过程：候选token C2因空间上更接近已选集合而被优先选择，而非距离更远但特征相似度相当的C1。

### 3.1 空间坐标与特征预处理

VLM-Pruner 的离心式剪枝建立在视觉 token 的二维空间结构之上。对于大小为 $H \times W$ 的特征图，每个 token 的索引 $i$ 被映射为空间坐标：

$$x_i = i \bmod W, \quad y_i = \lfloor i / W \rfloor$$

基于此坐标，任意两个 token $i$ 与 $j$ 之间的欧氏距离定义为 $D_{ij}^{(\mathrm{sp})} = \| \mathbf{p}_i - \mathbf{p}_j \|_2$，网格上的最大可能距离为 $D_{\mathrm{max}} = \sqrt{H^2 + W^2}$，用于后续距离归一化。

为降低计算开销，VLM-Pruner 对 token 特征进行通道筛选：仅保留方差最大的 top-$q$ 个通道（默认 $q=256$），得到降维特征 $\tilde{\mathbf{H}}$。在此降维空间上计算 token 间的余弦相似度：

$$M_{ij} = \frac{\tilde{\mathbf{H}}_i^\top \tilde{\mathbf{H}}_j}{\|\tilde{\mathbf{H}}_i\|_2 \|\tilde{\mathbf{H}}_j\|_2}$$

该相似度矩阵 $M$ 是后续贪婪选择的基础，但未经调制的原始相似度无法体现空间邻近性先验。

### 3.2 BSS 准则：空间邻近性调制的相似度

**核心瓶颈**在于：纯重要性驱动的方法倾向于选择相似冗余 token，而纯冗余去除方法则使 token 分布过于分散，丢失物体精细细节。VLM-Pruner 的因果调控机制是 **BSS（Buffering for Spatial Sparsity）准则**，它通过在相似度中引入空间距离项来调制选择行为。

具体而言，对于候选 token $i$ 和当前已选集合 $\mathcal{S}$，计算 $i$ 到 $\mathcal{S}$ 中最近 token 的归一化空间距离：

$$\bar{\delta}_i(\mathcal{S}) = \frac{\min_{j \in \mathcal{S}} D_{ij}^{(\mathrm{sp})}}{D_{\mathrm{max}}}$$

BSS 调制后的相似度为：

$$\widetilde{M}_{ij} = M_{ij} (1 + \lambda \bar{\delta}_i(\mathcal{S}))$$

其中 $\lambda = 0.5$ 为调制强度。**关键机制**：当候选 token 与已选集合空间距离较近时，$\bar{\delta}_i(\mathcal{S})$ 较小，调制因子接近 1，相似度几乎不变，token 容易被选中；随着已选集合向外扩张，远处 token 的 $\bar{\delta}_i(\mathcal{S})$ 增大，调制因子放大其等效相似度，从而降低被选概率。这实现了**由近及远的离心式增长**，优先密实局部邻域细节，再逐步向外扩张。

**消融证据**：移除 BSS 中的归一化距离项（即 $\bar{\delta}_i(\mathcal{S})$）后，平均性能下降 1.11%（Table 6），验证了空间邻近性先验的关键作用。

### 3.3 三阶段离心式剪枝流程

VLM-Pruner 在 LLM 解码器的第 2 层执行，遵循三阶段范式（Figure 3）：

**Stage 1 — Pivot 初始化**：在 token key 空间 $\mathbf{K}$ 中，通过 max-min 策略选取 $\kappa = 4$ 个多样化枢轴 token：

$$j_1 = \arg \max_{j \in V} \| \mathbf{K}_j \|_1, \quad j_t = \arg \max_{j \in \mathcal{C}} \min_{j' \in \mathcal{S}_{t-1}} \| \mathbf{K}_j - \mathbf{K}_{j'} \|_2$$

第一个枢轴选 L1 范数最大的 token，后续枢轴选与已选集合最小距离最大的候选 token，从而粗覆盖不同语义区域。

**Stage 2 — 带 BSS 的并行贪婪选择**：基于 BSS 调制相似度，为每个候选 token $i$ 计算非冗余分数：

$$r_i = 1 - \max_{j \in \mathcal{S}} \widetilde{M}_{ij}$$

分数越高表示 token $i$ 与已选集合的冗余度越低。选择过程以并行批次（batch size $B=16$）进行，配合阈值退火（初始 $\tau^{(0)} = 0.8$），由近及远逐步扩展保留集。

**Stage 3 — 相似性加权聚合（SWA）**：将丢弃 token 的信息回注到保留 token 中。对于每个保留 token $j$，找到与其最相似的丢弃 token 集合 $\mathcal{D}_j$，计算聚合权重：

$$\alpha_{uj} = \frac{M_{uj}}{\sum_{u' \in \mathcal{D}_j} M_{u'j} + \varepsilon}, \quad \varepsilon = 10^{-8}$$

最终通过加权融合恢复外围信息：

$$\mathbf{H}_j = \beta \mathbf{H}_j + (1-\beta) \mathbf{E}_j, \quad \mathbf{E}_j = \sum_{u \in \mathcal{D}_j} \alpha_{uj} \mathbf{H}_u$$

其中 $\beta = 0.3$，表示 70% 的聚合信息被注入保留 token 的最终表示。消融实验表明，去除 Stage 3 后平均性能从 95.30% 降至 95.07%（LLaVA-1.5-7B, Table 12），验证了 SWA 对恢复外围细节的贡献。

### 3.4 复杂度分析

整个流程的计算开销可控：通道筛选与相似度构建分别为 $O(Nd)$ 和 $O(N^2q)$，空间距离计算为一次性 $O(N^2)$。在 88.9% 剪枝率下，VLM-Pruner 实现了端到端推理加速（Table 5），同时保持了与上界接近的性能。

## 实验与关键发现

### 主实验结果

VLM-Pruner 在 5 个 VLM、13 个基准上的主实验结果一致表明，离心式剪枝范式在极高剪枝率下显著优于现有训练无关的 token 剪枝方法。实验统一采用批大小为 1 的官方评测协议，所有对比方法（包括 **FastV** (ECCV 2024)、**SparseVLM** (ICML 2025)、**PDrop** (CVPR 2025)、**MustDrop** (arXiv 2024)、**DART** (EMNLP 2025)、**DivPrune** (CVPR 2025) 等）均在同一评测框架下运行，确保公平性。

**LLaVA-1.5-7B 上的图像理解**（Table 1）：在仅保留 64 个 token（剪枝率 88.9%）的设置下，VLM-Pruner 达到平均相对上界保留率 95.61%，显著优于重要性驱动方法 FastV（84.60%）和冗余去除方法 DART（92.71%）、DivPrune（93.68%），领先 DivPrune 约 1.93 个百分点。在保留 128 个 token（剪枝率 77.8%）时，VLM-Pruner 保留率高达 98.07%；保留 192 个 token（剪枝率 66.7%）时达到 98.85%，几乎无损。这一趋势在 **LLaVA-1.5-13B** 上同样成立：64 token 设置下 VLM-Pruner 达到 92.68%，领先 DivPrune 2.48 个百分点（Table 2）。

**动态分辨率模型的泛化**（Table 2）：在支持动态分辨率的 **LLaVA-Next-7B** 上，VLM-Pruner 以约 11.1% 的 token 保留率取得 91.60% 的平均保留率，优于 DART（90.35%）和 DivPrune（89.02%），证明离心式剪枝对非固定 token 数量场景具有良好的适应性。

**跨架构验证**（Table 3-4）：在 **Qwen2-VL-7B-Instruct** 上，VLM-Pruner 以 150 个保留 token（剪枝率 88.9%）达到 92.58%，领先 DivPrune 3.65 个百分点。在视频理解模型 **LLaVA-Video-7B-Qwen2** 上，以 88.9% 剪枝率取得 90.55%，领先 DivPrune 5.48 个百分点，表明离心式剪枝对视觉 token 密集的视频场景尤为有效。

**推理效率**（Table 5）：VLM-Pruner 在 8 块 32GB VRAM GPU 上实测端到端推理速度。在 LLaVA-1.5-7B 上，64 token 设置相比无剪枝上界实现了显著加速，总时间和 FLOPs 均大幅降低。与其他剪枝方法相比，VLM-Pruner 在相似 token 数量下保持了竞争力推理开销，同时获得更高性能。

**Qwen3-VL-4B 验证**（Table 7）：在 Qwen3-VL-4B-Instruct 上，VLM-Pruner 保持优势，MME 达 2129、SQA 达 85.23、OCRBench 达 573，进一步验证了方法的跨模型鲁棒性。

### 消融实验

#### 三阶段结构分解

VLM-Pruner 的三阶段设计各自贡献显著（Table 6 / Section 4.5）。移除 BSS 准则中的归一化最近距离项（即仅使用原始余弦相似度进行选择）导致平均性能下降 1.11%，直接验证了空间邻近性先验对离心式增长的核心作用。将 max-min 枢轴初始化替换为 Top-4 L1 距离选择，性能下降 1.27%，表明多样化枢轴对覆盖不同语义区域至关重要。去除 Stage 3（SWA 聚合）后，LLaVA-1.5-7B 平均性能从 95.30% 降至 95.07%（Table 12），虽降幅不大但在 OCRBench 上影响更为明显（从 279 降至更低值）。值得注意的是，仅保留前两个阶段（无 Stage 3）的 VLM-Pruner 仍超过其他方法约 5 个绝对百分点（Qwen2-VL-7B, Table 13），说明 BSS 调制下的离心式选择本身已具备强竞争力。

![[assets/figures/papers/paper_list_l2244_https_arxiv_org_abs_2512_02700/figures/009_Table_6.jpg]]
*Table 6: Structural decomposition analysis in three stages*

#### 关键超参数

**枢轴数量 κ**（Table 8）：κ=4 时平均性能最优（95.30%）。过少的枢轴无法充分覆盖语义区域，过多则引入冗余，降低后续选择的效率。

**高方差通道 top-q**（Table 9）：q=256 时取得最优性能（95.30%）。通道筛选在降低计算开销（相似度矩阵构建复杂度从 O(N²d) 降至 O(N²q)）的同时，通过聚焦高方差通道提升了特征判别力。

**选择阈值 τ(0)**（Table 10）：τ(0)=0.8 为最优设定。阈值控制并行贪婪选择的严格程度，过高会导致选择不足，过低则引入过多冗余 token。

**Token 批次大小 B**（Table 11）：B=16 在速度与性能间取得最佳平衡（总时间 91 分钟，平均 95.30%）。并行批次选择是 VLM-Pruner 实现高效推理的关键设计，过大的批次会降低选择精度，过小则增加迭代开销。

**聚合权重 β**（Table 12）：β=0.3 取得最佳 OCRBench（279）且整体平均 95.30%。该设定意味着 70% 的丢弃 token 信息通过相似性加权聚合注入保留 token，有效恢复外围细节。

**剪枝层选择**（Table 14）：在 LLM 解码器的第 2 层执行剪枝取得最优性能（95.30%）。VLM-Pruner 无法在第 0 层剪枝，因为需要前一层的 token key 进行粗语义抽象；过深的剪枝层则导致冗余 token 在前期层中浪费计算。

### 定性分析与失败模式

**Figure 2** 展示了 VLM-Pruner 与基线方法的剪枝效果定性对比。在视觉问答案例中，VLM-Pruner 的选择顺序（数字 1 到 64）呈现明显的离心式增长模式：优先密实局部邻域细节，再向外扩张。相比之下，重要性驱动方法（如 FastV）倾向于保留相似冗余 token，而冗余去除方法（如 DART、DivPrune）生成的 token 分布过于分散，丢失物体精细细节。**Figure 5** 进一步量化了这一差异：VLM-Pruner 选择的边缘 token 数量更少，token 分布更集中，同时保留了更多精细细节。这解释了 VLM-Pruner 在 OCRBench 等细节敏感基准上的显著优势。

**方法局限性**：首先，VLM-Pruner 无法在第 0 层剪枝，限制了下游微调场景的灵活性。其次，SWA 聚合引入额外计算开销，在极低 token 数量下可能抵消部分加速收益。此外，方法依赖空间坐标结构，对于非网格布局的 token（如稀疏注意力）需要重新设计距离度量。超参数（κ, q, τ(0), β, B）基于经验设定，虽表现稳健但缺乏自适应性。

![[assets/figures/papers/paper_list_l2244_https_arxiv_org_abs_2512_02700/figures/002_Figure_2.jpg]]
*Figure 2: Comparisons of the actual pruning effects between baselines and VLM-Pruner. Visual question answering cases with correct (green) and incorrect (red) responses; numbers (from 1 to 64) denote selection order*

![[assets/figures/papers/paper_list_l2244_https_arxiv_org_abs_2512_02700/figures/010_Figure_4.jpg]]
*Figure 4: Ablation studies on hyperparameters on LLaVA-1.5- 7B. (a) Number of pivots κ, (b) Top-q highest variance channels*

![[assets/figures/papers/paper_list_l2244_https_arxiv_org_abs_2512_02700/figures/011_Figure_5.jpg]]
*Figure 5: More visualizations of the actual pruning effects between baselines and VLM-Pruner. From left to right are VLM-Pruner, DivPrune, and DART. (a) The average number of edge tokens in VLM-Pruner is lower. (b) The token distribution in the VLM-Pruner model is more concentrated*

![[assets/figures/papers/paper_list_l2244_https_arxiv_org_abs_2512_02700/figures/013_Table_8.jpg]]
*Table 8: Ablation study on the number of pivots κ*

## 定位与知识库关联

### 1. 与现有工作的关系

VLM-Pruner 位于训练无关（training‑free）视觉‑语言模型 token 剪枝方法的交汇点，其设计直接回应了该领域两大主流路线的结构性缺陷。

**重要性驱动剪枝（importance‑driven pruning）** 以 **FastV**（ECCV 2024）、**SparseVLM**（ICML 2025）、**PDrop**（CVPR 2025）和 **MustDrop**（arXiv 2024）为代表。这类方法依据 token 的注意力分数或梯度重要性进行选择，计算开销低，但存在一个被反复验证的瓶颈：高重要性 token 在特征空间中往往高度相似，导致保留集合冗余严重，浪费了有限的 token 预算。VLM‑Pruner 在实验中与 FastV 和 MustDrop 的直接对比（Table 1, Table 2）表明，仅靠重要性信号无法在极端剪枝率下维持多样化的视觉覆盖。

**冗余去除剪枝（redundancy‑reduction pruning）** 以 **DART**（EMNLP 2025）、**DivPrune**（CVPR 2025）、**SAINT** 和 **BTP** 为代表。它们通过最大化保留 token 之间的特征差异性来缓解冗余，但走向了另一个极端：差异性最大化使得 token 分布过于分散，丢失了物体内部的局部精细细节。VLM‑Pruner 的定性可视化（Figure 2, Figure 5）直接展示了这一现象——DART 和 DivPrune 选择的 token 散布在图像各处，边缘 token 数量显著多于 VLM‑Pruner，而 VLM‑Pruner 的 token 分布更集中，能够保留更多物体细节。

VLM‑Pruner 的关键创新在于通过 **BSS（Balancing Spatial Sparsity）准则** 在两者之间建立了可控的权衡。该准则在贪婪去冗余选择中引入空间邻近性先验：候选 token 与已选集合的最小空间距离越近，其被选中的概率越高。这一机制使算法优先在局部邻域内密实覆盖细节，再逐步向外扩张，既避免了重要性驱动方法的冗余问题，又克服了冗余去除方法的空间碎片化缺陷。

### 2. 方法谱系中的定位

从技术组件的角度，VLM‑Pruner 可被解构为三个相互耦合的模块，每个模块都对应着对现有范式的改进：

| 技术槽位 | 基线方法的主流做法 | VLM‑Pruner 的做法 | 支撑证据 |
|---------|-------------------|-------------------|---------|
| Token 选择策略 | 纯重要性或纯多样性 | 离心式剪枝：BSS 调制相似度，强制由近及远的选择顺序 | Eq. (5), Section 3.2 |
| 空间距离项 | 无 | 候选 token 到已选集合的最小欧氏距离，经归一化并以 λ=0.5 缩放后调制相似度 | Eq. (5), Section 3.2 |
| 枢轴初始化 | 随机选取 / 重要性 top‑k | max‑min 多样化枢轴选取（在 token key 空间） | Eq. (6), Section 3.3.1 |
| 丢弃 token 处理 | 直接丢弃 | 相似性加权聚合（SWA），以 β=0.3 将丢弃 token 信息重新注入最相似的保留 token | Eq. (10), Section 3.3.3 |
| 特征通道筛选 | 使用全部通道 | 仅保留方差最高的 top‑q（q=256）通道以降低计算量 | Section 3.2, Table 9 |

消融实验为这些设计选择提供了因果证据：
- 移除 BSS 中的归一化最近距离项后，平均性能下降 **1.11%**（Table 6 / Section 4.5），直接证明了空间调制项的必要性。
- 用 Top‑4 L1 距离取代 max‑min 枢轴初始化，性能下降 **1.27%**（Table 6 / Section 4.5），验证了多样化枢轴覆盖不同语义区域的价值。
- 去掉 Stage 3（SWA 聚合）后，LLaVA‑1.5‑7B 上的平均性能从 95.30% 降至 95.07%（Table 12），表明外围信息的恢复对极端剪枝率下的细节保留有贡献。

### 3. 适用边界

VLM‑Pruner 的适用性受到以下结构性约束：

1. **剪枝层位置限制**：方法无法在第 0 层剪枝，因为需要前一层的 token key 进行粗语义抽象。这意味着在需要对底层视觉特征进行微调的下游场景中，VLM‑Pruner 的灵活性受限。

2. **空间坐标依赖性**：BSS 准则依赖 token 在二维特征图上的网格坐标。对于非网格布局的 token 序列（如稀疏注意力机制或非均匀采样的视觉 backbone），需要重新设计距离度量函数。

3. **SWA 聚合的计算开销**：在极低 token 数量下，SWA 聚合引入的额外计算可能部分抵消剪枝带来的加速收益。Table 5 的推理成本分析提供了端到端加速比数据，但在 token 数极少的极端情况下，这一权衡需要更细致的评估。

4. **超参数的经验性**：κ（枢轴数量）、q（高方差通道数）、τ(0)（选择阈值）、β（聚合权重）和 B（批次大小）均基于经验设定。尽管消融实验（Table 8–12, Figure 4）表明这些参数在较宽范围内表现稳健，但缺乏对任务或数据集特征的自适应调节能力。

### 4. 局限与开放问题

基于上述分析，VLM‑Pruner 留下了若干值得进一步探索的方向：

- **自适应 λ 学习**：BSS 准则中的 λ 参数控制空间邻近性先验的强度。当前 λ=0.5 为固定值，能否设计一种机制使其根据输入图像的特征冗余程度动态调整，是一个有实际价值的问题。

- **跨任务泛化**：离心式剪枝范式目前仅在图像和视频理解的 VQA 任务上得到验证。将其推广到更广泛的视觉任务（如视频理解中的长时依赖建模、多帧时序推理）需要验证 BSS 准则在时间维度上的适用性。

- **SWA 与注意力机制的深度融合**：当前 SWA 通过简单的相似性加权将丢弃 token 信息聚合到保留 token 的隐状态中。是否可以将这一聚合过程与 LLM decoder 的注意力计算更紧密地结合，以实现更高效的信息融合，值得进一步研究。

- **更大规模 VLM 上的验证**：现有实验覆盖了 7B 和 13B 规模的 VLM。在更大规模的模型（如 34B 以上）上，VLM‑Pruner 是否仍能保持高效的端到端加速比，以及超参数是否需要重新调优，目前尚无实验数据支撑。

- **与训练方法的互补性**：VLM‑Pruner 是训练无关方法，与需要微调的剪枝方法（如结构化剪枝）在技术路线上互补。两者是否可以结合——例如用 VLM‑Pruner 的离心式选择策略指导结构化剪枝的 mask 学习——是一个开放的研究方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/VLM_Pruner_Buffering_for_Spatial_Sparsity_in_an_Efficient_VLM_Centrifugal_Token_Pruning_Paradigm.pdf]]
