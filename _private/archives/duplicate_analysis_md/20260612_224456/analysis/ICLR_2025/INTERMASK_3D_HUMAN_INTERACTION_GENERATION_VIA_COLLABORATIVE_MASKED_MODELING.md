---
title: INTERMASK 3D HUMAN INTERACTION GENERATION VIA COLLABORATIVE MASKED MODELING
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Modelling.pdf
project_link: https://gohar-malik.github.io/intermask
aliases:
- I3HIGCMM
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过引入保留空间维度的2D离散运动令牌图、采用生成式掩码建模框架替代扩散模型，并设计专门的时空注意力和交叉注意力模块，显式捕捉个体内和个体间的时空依赖。
primary_logic: 将运动转化为二维令牌图，并在协同掩码生成过程中同时考虑关节点和时间维度的注意力，能够更有效地建模双人交互中的空间位置精度和反应同步性，从而大幅提升交互生成质量。
claims:
- InterMask 在 InterHuman 数据集上取得 FID 5.154，显著优于先前最佳方法 in2IN 的 5.535。
- InterMask 在 InterX 数据集上取得 FID 0.399，远优于 InterGen 的 5.207。
- 消融实验表明时空注意力模块最为关键，移除后 FID 升至 10.968，R-Precision Top-1 降至 0.350。
- 用户调研显示 69.14% 的被试者偏好 InterMask 而非 InterGen，在交互质量和文本一致性评分上均显著领先。
---

# INTERMASK 3D HUMAN INTERACTION GENERATION VIA COLLABORATIVE MASKED MODELING

> [!tip] 核心洞察
> 将运动转化为二维令牌图，并在协同掩码生成过程中同时考虑关节点和时间维度的注意力，能够更有效地建模双人交互中的空间位置精度和反应同步性，从而大幅提升交互生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterMask：基于协同掩码建模的3D人类交互生成 |
| 英文题名 | INTERMASK 3D HUMAN INTERACTION GENERATION VIA COLLABORATIVE MASKED MODELING |
| 会议/期刊 | ICLR 2025 |
| Links |  [Project](https://gohar-malik.github.io/intermask)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | InterMask |
| Dataset | InterHuman, InterX, Computational Cost |

> [!tip] 效果简介
> - InterHuman 上，FID 5.154 vs 5.535 (in2IN) (-0.381)；R-Precision Top-1 0.449 vs 0.425 (in2IN) (+0.024)。
> - InterX 上，FID 0.399 vs 5.207 (InterGen) (-4.808)；R-Precision Top-1 0.403 vs 0.207 (InterGen) (+0.196)。
> - Computational Cost 上，Inference Time (seconds) 0.77 vs 1.63 (InterGen) (-0.86)。

## 概述

### 1. 问题背景与瓶颈

生成逼真且语义一致的3D双人交互动作是计算机视觉与图形学中的核心挑战，其应用涵盖虚拟现实、动画制作与人机交互。现有主流方法多基于扩散模型（如 **InterGen** (Liang et al., 2024)、**in2IN** (Ruiz-Ponce et al., 2024)），然而，这类方法在建模个体间细粒度的空间位置关系和反应时间同步性上存在根本性困难，导致生成的动作在真实感和交互一致性上难以令人满意。

### 2. 核心方法

本文提出 **InterMask**，一种基于协同掩码建模的生成式框架。其核心洞察在于：将运动序列转化为保留空间维度的二维离散令牌图，并在协同掩码生成过程中，通过专门的时空注意力和交叉注意力模块，同时捕捉个体内部（关节-时间）与个体之间（空间-反应）的复杂依赖。该方法以生成式掩码建模替代扩散去噪范式，从根本上改变了交互动作的生成机制。

### 3. 关键结果

InterMask 在双人交互生成任务上取得了显著突破。在 **InterHuman** 数据集上，其 FID 降至 **5.154**，优于先前最佳方法 in2IN 的 5.535；在 **InterX** 数据集上，FID 更是达到 **0.399**，远优于 InterGen 的 5.207。同时，推理速度提升超过一倍（0.77秒 vs. 1.63秒），参数量仅为 InterGen 的约40%（74M vs. 182M）。用户调研进一步证实，69.14% 的被试者偏好 InterMask 生成的交互质量。

### 4. 方法定位

InterMask 属于**生成式掩码建模**与**离散运动表示**的交汇点。其与现有工作的关键差异在于：

- **运动表示**：将传统的1D VQ令牌序列扩展为**2D令牌图**，显式保留空间维度。
- **生成范式**：以**迭代掩码预测**取代扩散去噪，实现高效并行推理。
- **交互建模**：通过**协同掩码**同时预测双人令牌，而非顺序或独立建模。
- **注意力机制**：引入**共享时空注意力**与**共享交叉注意力**，精准捕捉个体内与个体间的时空依赖。
- **条件注入**：采用 **AdaLN-mod** 通过冻结的 CLIP 特征调控归一化参数，实现稳定的文本控制。

## 背景与动机

### 问题背景

生成逼真且语义一致的三维双人交互动作是计算机视觉与图形学中的核心挑战，其应用涵盖动画制作、虚拟现实和具身智能等领域。与单人运动生成不同，双人交互生成要求同时建模两个个体的运动，并精确捕捉个体间细粒度的空间位置关系与时间反应同步性——例如拳击中的攻防节奏、舞蹈中的动作协调以及日常互动中的身体接近度。

从数据表示的角度看，一段个体运动序列可形式化为 $\mathbf{m}_p \in \mathbb{R}^{N \times J \times d}$，其中 $N$ 为时间帧数，$J$ 为关节点数，$d$ 为关节特征维度。双人交互则需联合生成 $\{\mathbf{m}_a, \mathbf{m}_b\}$ 并保持其时空耦合关系。

### 现有方法缺口

近年来，基于扩散模型的运动生成方法在单人场景下取得了显著进展，代表性工作包括 **MDM**（Tevet et al., 2023）和 **T2M**（Guo et al., 2022a）。在此基础上，研究者尝试将扩散框架拓展至双人交互生成，主要形成了三条技术路线：

- **桥接式方法**：如 **ComMDM**（Shafir et al., 2024）将两个独立的 MDM 模型通过通信机制桥接，但缺乏对交互依赖的端到端建模。
- **专用扩散模型**：**InterGen**（Liang et al., 2024）设计了专门的双人交互扩散模型，但扩散模型固有的迭代去噪过程计算开销大，且难以显式捕捉关节点级别的空间精度。
- **检索增强与语言引导**：**MoMat-MoGen**（Cai et al., 2024）引入检索增强机制，**in2IN**（Ruiz-Ponce et al., 2024）利用大语言模型生成个体化描述作为条件，两者虽提升了文本一致性，但均未从根本上解决空间位置精度和反应时间建模不足的问题。

上述方法的共同瓶颈在于：**扩散模型将运动视为一维时序信号处理，丢失了空间维度的结构化信息，导致难以精准建模个体间细粒度的空间位置和反应时间，生成的动作缺乏真实感和交互一致性**。此外，扩散模型推理速度慢、参数量大，限制了其在实际应用中的部署效率。

### 本文动机

针对上述瓶颈，本文提出了一种范式层面的转变：**用生成式掩码建模（Masked Generative Modeling）替代扩散去噪框架，并将运动表示从一维令牌序列升级为保留空间维度的二维离散令牌图**。

这一设计选择基于以下核心洞察：将运动转化为二维令牌图，并在协同掩码生成过程中同时考虑关节点和时间维度的注意力，能够更有效地建模双人交互中的空间位置精度和反应同步性。具体而言：

1. **2D 令牌图**将运动序列从 $(N, J, d)$ 降采样并量化为 $(n, j)$ 的离散网格，显式保留了关节空间结构，使得空间注意力和时间注意力可以分别在关节点维度和时间维度上独立计算。
2. **协同掩码建模**允许两个个体的令牌被同时掩码和预测，迫使模型学习个体间的交叉依赖，而非顺序或独立地处理两个个体。
3. **掩码生成框架**天然支持迭代式并行解码，在推理速度和参数量上相比扩散模型具有显著优势。

基于上述动机，本文提出 **InterMask**——一个基于协同掩码建模的三维人类交互生成框架，旨在以更低的计算成本实现更精准的时空协调和交互一致性。

## 核心创新

InterMask 的核心创新在于从**表示、框架、建模三个层面**对双人交互生成进行了系统性重构，以解决现有扩散模型方法难以精准捕捉个体间细粒度空间位置与反应时间的关键瓶颈。

### 1. 运动表示：从 1D 令牌到 2D 令牌图

现有方法（如 T2M、MDM）通常将运动序列压缩为一维 VQ 令牌序列，仅沿时间维度编码，丢失了关节间的空间结构信息。InterMask 提出**保留空间维度的 2D 离散运动令牌图**：将个体运动序列 $\mathbf{m}_p \in \mathbb{R}^{N \times J \times d}$ 通过 2D 卷积编码器降采样为 $\{t_p\} \in \{0, 1, \cdots, |\mathcal{C}| - 1\}^{n \times j}$，其中 $n$ 和 $j$ 分别对应降采样后的时间帧数和关节点数。这一设计使每个令牌显式对应特定的关节点和时间步，为后续时空注意力建模提供了结构基础。

消融实验（Table 2）验证了这一设计的决定性作用：个体级 2D 令牌图的重建质量（FID 0.970, MPJPE 0.129）远优于 1D 令牌图（FID 3.146, MPJPE 0.354）和交互级 2D 令牌图（FID 1.276, MPJPE 0.198）。

### 2. 生成框架：从扩散去噪到生成式掩码建模

现有交互生成方法（InterGen、in2IN、ComMDM 等）普遍依赖扩散去噪框架，需要多步迭代去噪，推理成本高。InterMask 转而采用**生成式掩码建模（Masked Generative Modeling）**：训练时按余弦调度 $\gamma(\tau_i) = \cos(\frac{\pi \tau_i}{2})$ 随机掩码部分令牌，让 Inter-M Transformer 学习从上下文预测被掩码令牌；推理时从全掩码序列出发，通过迭代预测并重掩码低置信度令牌逐步生成完整运动。

这一框架转换带来显著的效率优势：InterMask 推理仅需 0.77 秒（InterGen 为 1.63 秒），参数量仅 74M（InterGen 为 182M），同时生成质量大幅领先。

### 3. 交互建模：协同掩码与专用注意力模块

这是 InterMask 最核心的机制创新，包含两个紧密耦合的设计：

**协同掩码建模**：将两个个体的 2D 令牌图展平、拼接后统一掩码，由同一个 Transformer 联合预测。这与“逐人交替建模”（Alternative Modeling）形成对比——后者虽然多样性略高，但交互质量显著退化（FID 从 5.154 升至 7.637，Table 3），证明协同建模对于捕捉个体间依赖至关重要。

**三层注意力架构**：每个 Inter-M Transformer Block 包含：
- **自注意力**：对拼接后的令牌序列进行全局建模；
- **共享时空注意力**：分别沿关节点维度（空间注意力）和时间维度（时间注意力）计算注意力，再将两者输出逐项相加融合（Equation 5–6），显式捕捉个体内的时空依赖；
- **共享交叉注意力**：两个个体的嵌入互为查询和键值对（Equation 7），显式建模个体间的交互依赖。

消融实验（Table 3）表明，时空注意力是最关键的模块：移除后 FID 从 5.154 退化至 10.968，R-Precision Top-1 从 0.449 降至 0.350；移除交叉注意力也使 FID 升至 7.306。

### 4. 文本条件注入：AdaLN-mod 调制

区别于标准交叉注意力或特征拼接，InterMask 采用 **AdaLN-mod** 机制：通过冻结的 CLIP 文本特征回归缩放与平移参数，对 Transformer 层的归一化进行条件调制。这一设计使文本条件更平滑地融入生成过程，避免了对令牌序列的显式扰动。

### 创新总结

| 设计维度 | 基线方法 | InterMask 方案 | 关键证据 |
|---------|---------|---------------|---------|
| 运动表示 | 1D VQ 令牌序列 | 2D 令牌图（保留时空结构） | Table 2: FID 0.970 vs 3.146 |
| 生成框架 | 扩散去噪 | 生成式掩码建模 | 推理 0.77s vs 1.63s, 参数 74M vs 182M |
| 交互策略 | 顺序/独立建模 | 协同掩码 + 交叉注意力 | Table 3: FID 5.154 vs 7.637 |
| 注意力机制 | 仅自注意力 | 自注意力 + 时空注意力 + 交叉注意力 | Table 3: 移除时空注意力 FID→10.968 |
| 文本注入 | 交叉注意力/拼接 | AdaLN-mod 调制 | 架构设计（Section 3.2.2） |

这些创新相互依赖、形成闭环：2D 令牌图为时空注意力提供了结构化的操作维度，协同掩码为交叉注意力提供了跨个体信息交换的接口，而掩码建模框架则使整个系统能够以高效率和高质量完成交互生成。

## 整体框架

InterMask 采用两阶段流水线，将文本条件双人交互生成分解为“离散运动表示学习”与“协同掩码生成”两个核心环节（Figure 2）。

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/002_Figure_2.jpg]]
*Figure 2: Overview of InterMask. (a) Individual motions are quantized through vector quantization*

**第一阶段：个体运动的 2D 离散化。**
对于两个个体的运动序列 $\mathbf{m}_a, \mathbf{m}_b \in \mathbb{R}^{N \times J \times d}$（$N$ 帧、$J$ 关节、$d$ 维特征），共享的 VQ-VAE 编码器分别将其下采样并量化为 2D 离散令牌图 $\{t_a, t_b\} \in \{0,1,\cdots,|\mathcal{C}|-1\}^{n \times j}$，其中 $n$ 和 $j$ 分别为降采样后的时间与空间维度，$\mathcal{C}$ 为可学习码本。解码器则将令牌图还原为运动序列。训练目标由 L1 重建损失、承诺损失以及速度、脚部接触、骨骼长度三项几何辅助损失加权构成（Equation 1–2）。

**第二阶段：协同掩码生成。**
两个个体的 2D 令牌图被展平、拼接后，送入 Inter-M Transformer 进行协同掩码建模（Figure 2(b)）。训练时，按余弦调度 $\gamma(\tau)$ 随机掩码部分令牌，Transformer 以文本条件 $c$ 为引导，预测所有被掩码位置的原始令牌，损失为掩码位置上的交叉熵（Equation 8）。推理时，从完全掩码的序列出发，通过多轮迭代逐步预测令牌，每轮对低置信度预测重新掩码，并配合 Classifier-Free Guidance 完成生成（Figure 3），最终由 VQ-VAE 解码器输出双人运动序列。

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/003_Figure_3.jpg]]
*Figure 3: Inference process. Starting from completely masked token sequences of both individuals*

**Inter-M Transformer 的核心设计。**
每个 Transformer 块包含三个注意力模块（Figure 2(c)）：
- **自注意力**：对拼接后的令牌序列进行全局依赖建模；
- **共享时空注意力**：在同一时间步内对所有关节点做空间注意力，并在同一关节点沿时间步做时间注意力，二者输出逐项相加（Equation 5–6），显式捕捉个体内部的时空结构；
- **共享交叉注意力**：两个个体的令牌互为查询与键值对（Equation 7），建模个体间的交互依赖。

文本条件通过冻结的 CLIP 特征经 AdaLN-mod 注入，以缩放与平移的方式调制归一化层。

**关键设计选择。**
消融实验（Table 3）证实，时空注意力是最关键的模块——移除后 FID 从 5.154 退化至 10.968。交叉注意力同样重要，移除后 FID 升至 7.306。此外，协同掩码策略（同时掩码并预测两个个体）优于逐人交替建模（FID 7.637 vs 5.154），说明同步推理对于交互一致性至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/017_Figure_10.jpg]]
*Figure 10: Overview of the Alternative Modeling approach, where we predict the tokens of one person at a time. (a) During training, only the embeddings of one individual*

## 核心模块与公式推导

InterMask 的核心由两个级联模块构成：**2D 运动 VQ-VAE**（将个体运动序列压缩为离散令牌图）和 **Inter-M Transformer**（在令牌空间内协同掩码建模双人交互）。以下仅展开关键公式与变量含义。

### 2D 运动 VQ-VAE

给定个体 $p$ 的运动序列 $\mathbf{m}_p \in \mathbb{R}^{N \times J \times d}$（$N$ 帧，$J$ 个关节，$d$ 维特征），2D 编码器通过卷积降采样得到潜在表示，再经向量量化映射为 2D 令牌图 $\{t_p\} \in \{0, 1, \cdots, |\mathcal{C}| - 1\}^{n \times j}$，其中 $n$、$j$ 分别为降采样后的时间与空间维度，$|\mathcal{C}|$ 为码本大小。

VQ-VAE 的基础训练目标为：

$$
\mathcal { L } _ { v q } = \| \mathbf { m } _ { p } - \hat { \mathbf { m } } _ { p } \| _ { 1 } + \beta \| \tilde { \mathbf { t } } _ { p } - \mathrm { s g } ( \mathbf { t } _ { p } ) \| _ { 2 } ^ { 2 }
$$

- $\hat{\mathbf{m}}_p$：解码器重建的运动序列。
- $\tilde{\mathbf{t}}_p$：编码器输出的连续潜在向量。
- $\mathbf{t}_p$：量化后的码本向量。
- $\mathrm{sg}(\cdot)$：停止梯度算子，防止承诺损失反向传播至编码器。
- $\beta$：承诺损失权重。

为提升重建的物理合理性，额外引入速度损失 $\mathcal{L}_{vel}$、脚部接触损失 $\mathcal{L}_{fc}$、骨骼长度损失 $\mathcal{L}_{bl}$ 三项几何约束，总体损失为：

$$
\mathcal { L } _ { v q v a e } = \mathcal { L } _ { v q } + \lambda _ { v e l } \mathcal { L } _ { v e l } + \lambda _ { f c } \mathcal { L } _ { f c } + \lambda _ { b l } \mathcal { L } _ { b l }
$$

其中三个几何辅助损失定义为：

$$
\begin{aligned}
\mathcal { L } _ { v e l } &= \frac { 1 } { N - 1 } \sum _ { i _ { n } = 1 } ^ { N } \| ( m _ { i _ { n } + 1 } - m _ { i _ { n } } ) - ( \hat { m } _ { i _ { n } + 1 } - \hat { m } _ { i _ { n } } ) \| _ { 1 } \\
\mathcal { L } _ { f c } &= \frac { 1 } { N - 1 } \sum _ { i _ { n } = 1 } ^ { N } \| ( \hat { m } _ { i _ { n } + 1 } - \hat { m } _ { i _ { n } } ) \cdot f _ { i _ { n } } \| _ { 1 } \\
\mathcal { L } _ { b l } &= \frac { 1 } { N - 1 } \sum _ { i _ { n } = 1 } ^ { N } \| B ( m _ { i _ { n } } ) - B ( \hat { m } _ { i _ { n } } ) \| _ { 1 }
\end{aligned}
$$

- $f_{i_n}$：第 $i_n$ 帧的脚部接触标签。
- $B(\cdot)$：骨骼长度计算函数。

消融实验证实，对个体运动使用 2D 令牌图的重建质量（FID 0.970, MPJPE 0.129）远优于 1D 令牌图（FID 3.146, MPJPE 0.354）和交互级别 2D 令牌图（FID 1.276, MPJPE 0.198），见 **Table 2**。

### Inter-M Transformer

两个个体的 2D 令牌图被展平、拼接后送入 Inter-M Transformer 进行协同掩码建模。每个 Inter-M 块依次包含三个注意力模块：

**自注意力**：标准缩放点积注意力，捕获全局令牌依赖。

$$
\mathrm { A t t n } ( \mathbf { Q } , \mathbf { K } , \mathbf { V } ) = \mathrm { s o f t m a x } ( \mathbf { Q } \mathbf { K } ^ { \top } / \sqrt { \tilde { d } } ) \mathbf { V }
$$

**共享时空注意力**：在同一时间步内对所有关节点做空间注意力，再对同一关节点沿时间步做时间注意力，二者输出逐项相加。

$$
\begin{aligned}
\mathbf { e } _ { p } ^ { \prime } ( i _ { n } ) &= \mathrm { A t t n } ( \mathbf { Q } _ { j } , \mathbf { K } _ { j } , \mathbf { V } _ { j } ) \\
\mathbf { e } _ { p } ^ { \prime \prime } ( i _ { j } ) &= \mathrm { A t t n } ( \mathbf { Q } _ { n } , \mathbf { K } _ { n } , \mathbf { V } _ { n } ) \\
\mathbf { e } _ { p } &= \mathbf { e } _ { p } ^ { \prime } ( i _ { n } ) + \mathbf { e } _ { p } ^ { \prime \prime } ( i _ { j } ) \quad \forall \; 0 < i _ { n } < n , 0 < i _ { j } < j
\end{aligned}
$$

**共享交叉注意力**：个体 $a$ 的查询关注个体 $b$ 的键与值，反之亦然，显式建模个体间依赖。

$$
\mathbf { e } _ { a } ^ { \prime } = \mathrm { A t t n } ( \mathbf { Q } _ { a } , \mathbf { K } _ { b } , \mathbf { V } _ { b } ) \quad \mathbf { e } _ { b } ^ { \prime } = \mathrm { A t t n } ( \mathbf { Q } _ { b } , \mathbf { K } _ { a } , \mathbf { V } _ { a } )
$$

文本条件通过 AdaLN-mod 注入：冻结的 CLIP 文本特征控制归一化层的缩放与平移参数。

### 训练与推理目标

训练时，采用余弦调度控制掩码比例：

$$
\gamma ( \tau _ { i } ) = \cos \left( \frac { \pi \tau _ { i } } { 2 } \right) \in [ 0 , 1 ] \quad \tau _ { i } \sim \mathcal { U } ( 0 , 1 )
$$

掩码位置的训练损失为负对数似然（交叉熵）：

$$
\mathcal { L } _ { m a s k } = \sum _ { \tilde { t } _ { k } = [ \mathrm { M A S K } ] } - \log p _ { \theta } ( t _ { k } | \tilde { t } , c )
$$

推理时，从全掩码序列出发，迭代预测令牌并重掩码低置信度令牌，配合 Classifier-Free Guidance 完成采样。

### 消融关键结论

**Table 3** 的消融实验揭示了各注意力模块的因果作用：移除时空注意力后 FID 从 5.154 退化至 10.968，R-Precision Top-1 从 0.449 降至 0.350；移除交叉注意力使 FID 升至 7.306，R-Precision Top-1 降至 0.392。这表明时空注意力与交叉注意力是交互建模质量的决定性因素。

### 补充图表

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/012_Figure_8.jpg]]
*Figure 8: Illustration of the two-stage masking technique used during training of the Inter-M Transformer. For stage 1, we either apply Random Masking with a probability of*

## 实验与分析

### 主要结果与定量对比

InterMask 在双人交互生成任务的两个主流基准上均取得了最优性能，验证了协同掩码建模框架与 2D 令牌图表示的有效性。

**Table 1** 报告了在 InterHuman 与 InterX 测试集上的全面对比。在 InterHuman 数据集上，InterMask 的 **FID 达到 5.154**，优于先前最佳方法 in2IN（Ruiz-Ponce et al., 2024）的 5.535；R-Precision Top-1 为 0.449，同样领先于 in2IN 的 0.425。在更具挑战性的 InterX 数据集上，InterMask 的优势更为显著：**FID 低至 0.399**，而 InterGen（Liang et al., 2024）为 5.207，降幅达 4.808；R-Precision Top-1 为 0.403，较 InterGen 的 0.207 提升了近一倍。这表明 InterMask 不仅在运动质量上显著提升，在文本-动作对齐方面也有实质性突破。

除生成质量外，InterMask 在计算效率上也具备优势。推理阶段仅需 **0.77 秒**，参数量为 **74M**，而 InterGen 分别需要 1.63 秒和 182M 参数——InterMask 以不到一半的参数量实现了近一倍的推理加速。这一效率优势源于生成式掩码建模框架的迭代解码机制，相较于扩散模型的逐步去噪过程更为高效。

**Figure 4** 的定性对比进一步佐证了定量结果。在“拳击对打”场景中，InterGen 生成的两个人物动作缺乏实时反应，表现为机械的交替出拳；而 InterMask 能够生成具有真实反应时间的躲闪与反击动作。在“双人舞蹈”场景中，InterMask 生成的舞者动作保持了精确的空间协调与节奏同步，避免了 InterGen 中出现的肢体穿透与动作脱节问题。

### 用户调研

**Figure 5** 展示了在 Amazon Mechanical Turk 上进行的用户调研结果。在交互质量（Interaction Quality）和文本一致性（Text Alignment）两个维度上，InterMask 均显著优于 InterGen：**69.14% 的被试者偏好 InterMask** 生成的交互动画。调研中动画呈现顺序随机，并筛选了高信誉评分者以消除偏见，结果具有统计可靠性。

### 消融实验

消融实验系统性地验证了 InterMask 各核心组件的贡献，所有实验均在 InterHuman 测试集上进行，报告 95% 置信区间。

#### 2D 令牌图的有效性

**Table 2** 对比了三种运动离散表示方案对 VQ-VAE 重建质量的影响：
- **1D 令牌图**（仅沿时间维度压缩）：FID 3.146，MPJPE 0.354
- **交互级 2D 令牌图**（将双人运动拼接后一起编码）：FID 1.276，MPJPE 0.198
- **个体级 2D 令牌图**（InterMask 采用的方案）：**FID 0.970，MPJPE 0.129**

个体级 2D 令牌图在重建精度上远超 1D 方案（MPJPE 降低约 64%），也优于交互级方案。其优势在于保留了空间（关节点）维度的结构信息，使得后续的时空注意力能够分别对关节间和时间步间的依赖进行建模。**Figure 11** 的定性消融显示，1D 令牌图重建的动作存在明显的抖动和关节错位，而 2D 令牌图能够更准确地还原精细的手部与足部动作。

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/018_Figure_11.jpg]]
*Figure 11: Qualitative results for the ablation study on Motion VQ-VAE to verify the proposed 2D token map*

#### 注意力模块的贡献

**Table 3** 对 Inter-M Transformer 的各注意力模块进行了消融：
- **完整模型**：FID 5.154，R-Precision Top-1 0.449
- **移除时空注意力**：FID 升至 **10.968**（退化约 113%），R-Precision Top-1 降至 0.350
- **移除交叉注意力**：FID 升至 7.306，R-Precision Top-1 降至 0.392
- **仅保留自注意力**：FID 进一步退化为 11.765

时空注意力模块的移除导致性能退化最为严重，验证了其对个体内时空依赖建模的核心作用。交叉注意力的移除则主要损害了个体间的交互协调，表现为 R-Precision 的显著下降。**Figure 12** 的定性结果表明，移除时空注意力后生成的动作出现明显的时序不连贯，移除交叉注意力则导致双人动作失去互动性（如一人出拳时另一人无反应）。

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/019_Figure_12.jpg]]
*Figure 12: Qualitative results for the ablation study on Inter-M Transformer to verify contributions of the proposed Attention modules*

#### 协同建模 vs. 交替建模

Table 3 还对比了协同掩码建模（Collaborative Modeling）与逐人交替建模（Alternative Modeling，见 **Figure 10**）。交替建模方案在训练时一次只更新一个人的嵌入，推理时交替预测两个个体的令牌。结果显示，交替建模虽然多样性（MModality）略高，但交互质量明显下降：FID 从 5.154 升至 7.637，R-Precision Top-1 从 0.449 降至 0.393。这表明同时预测两个个体的令牌对于捕捉实时交互中的时空耦合至关重要。

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/008_Table_3.jpg]]
*Table 3: Ablation Study results on the InterHuman test set to verify key components of the proposed Inter-M Transformer. Bold face indicates the best result*

#### 掩码策略的影响

**Table 4** 探索了随机掩码概率 $p_r$ 对交互生成与反应生成任务的影响。$p_r=0.8$ 在两个任务间取得了最佳平衡：交互 FID 5.154，反应 FID 2.991。过低的 $p_r$ 会减少交互掩码（同时掩码两个个体对应位置的令牌）的比例，削弱协同建模能力；过高的 $p_r$ 则不利于反应生成任务中对参考动作的条件建模。

### 失败模式与局限性

**Figure 14** 展示了 InterMask 的两类典型失败案例：

1. **身体穿透问题**：将输出骨架转换为 SMPL 网格时，可能出现双人身体部位的相互穿透（如手臂穿过对方躯干）。这是因为训练阶段仅在骨架层面施加了几何约束（速度损失、脚部接触损失、骨骼长度损失），未包含网格级的抗穿透损失。

2. **数据隐含偏见**：模型可能受到训练数据分布的影响，在文本未明确提及舞蹈时仍倾向于生成舞蹈类动作。例如，对于“两人面对面站立交谈”的提示，生成的动画可能不自觉地加入律动感。这一问题源于 InterHuman 数据集中舞蹈类交互占比较高的分布偏差。

此外，当前 InterMask 仅支持固定长度的运动序列（约 10 秒），尚未验证对更长或不定长序列的扩展性。在 MModality 指标上略低于部分方法（如 InterGen），表明生成多样性仍有提升空间。

### 补充图表

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation on the InterHuman and InterX test sets. ± indicates a 95% confidence interval and → means the closer to ground truth the better. Bold face indicates the best result, while underscore refers to the second best*

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison between InterMask and InterGen (Liang et al., 2024), highlighting InterMask’s superior interaction quality, text adherence and avoidance of implicit biases*

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/006_Figure_5.jpg]]
*Figure 5: User Study comparing our Inter-Mask and InterGen (Liang et al., 2024)*

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/007_Table_2.jpg]]
*Table 2: Ablation Study results on InterHuman test set to verify key components of the proposed Motion VQ-VAE. Bold face indicates the best result*

![[assets/figures/papers/paper_list_l1781_INTERMASK_3D_HUMAN_INTERACTION_GENERATION_VIA_COLLABORATIVE_MASKED_MODEL/figures/021_Figure_14.jpg]]
*Figure 14: Examples of Limitations of our method. The first row shows body penetration when converted from output skeleton to SMPL mesh. The second row shows implicit bias towards dancing*

## 方法谱系与知识库定位

### 从扩散模型到生成式掩码建模的范式迁移

InterMask 的核心突破在于将双人交互生成从**扩散去噪范式**迁移至**生成式掩码建模（Masked Generative Modeling）**框架。此前主流方法——从单人到双人的演进——几乎全部依赖扩散模型：

- **单人扩散基线**：**MDM**（Tevet et al., 2023）以扩散框架实现文本条件的单人运动生成，成为后续双人方法的基石。
- **桥接式双人扩展**：**ComMDM**（Shafir et al., 2024）通过将两个预训练的 MDM 模型进行通信桥接来实现交互生成，本质上是对独立模型的后期缝合。
- **专用双人扩散模型**：**InterGen**（Liang et al., 2024）是首个专为双人交互设计的扩散模型，在 InterHuman 和 InterX 数据集上建立了强基线（FID 分别为 5.918 和 5.207）。**in2IN**（Ruiz-Ponce et al., 2024）进一步引入 LLM 生成的个体化文本描述作为条件，将 InterHuman FID 推至 5.535。
- **检索增强方法**：**MoMat-MoGen**（Cai et al., 2024）引入检索增强机制来辅助交互扩散生成。

InterMask 选择**放弃扩散框架**，转而采用生成式掩码建模。这一设计选择的关键动因在于：扩散模型的迭代去噪过程难以显式建模个体间细粒度的空间位置精度和反应时间同步性。掩码建模通过直接预测被遮蔽的令牌，配合逐步重掩码低置信度令牌的迭代推理策略，在推理效率（0.77 秒 vs InterGen 的 1.63 秒）和参数量（74M vs 182M）上均实现显著压缩，同时取得了更优的生成质量。

### 运动表示的关键创新：2D 令牌图

在运动离散表示层面，InterMask 提出了**保留空间维度的 2D 离散运动令牌图**，这是区别于所有先前工作的核心设计。传统方法（如 T2M、MDM 系列）通常将运动序列压缩为仅沿时间维度的 1D VQ 令牌序列，丢失了关节点之间的空间结构信息。

InterMask 的 2D 令牌图将运动序列 $\mathbf{m}_p \in \mathbb{R}^{N \times J \times d}$ 降采样并量化为 $\{t_p\} \in \{0, 1, \cdots, |\mathcal{C}| - 1\}^{n \times j}$，其中 $n$ 为降采样后的时间维度，$j$ 为空间（关节点）维度。消融实验（Table 2）提供了决定性证据：

- **个体级 2D 令牌图**：重建 FID 0.970，MPJPE 0.129
- **1D 令牌图**：重建 FID 3.146，MPJPE 0.354（质量退化约 3.2 倍）
- **交互级 2D 令牌图**（将两人拼接为一张图）：重建 FID 1.276，MPJPE 0.198

这表明在个体级别保留空间维度的 2D 令牌图设计，既能保留关节间的空间拓扑关系，又避免交互级拼接带来的信息混淆。

### 交互建模策略的谱系定位

双人交互生成的核心挑战在于如何建模个体间的时空依赖。现有方法沿两条路径演进：

1. **独立建模 + 后融合**：ComMDM 为代表，两个模型独立运行，仅在特定层进行通信。这类方法难以捕捉精细的实时交互同步。
2. **联合建模**：InterGen 和 in2IN 将两人运动拼接后统一输入扩散模型，但缺乏显式的个体间注意力机制。

InterMask 的**协同掩码建模**策略在此基础上引入了三项关键设计：

- **共享时空注意力**：在同一时间步内对所有关节点计算空间注意力，同时对同一关节点沿时间步计算时间注意力，二者输出逐项相加（Equation 5-6）。消融实验（Table 3）表明，移除此模块导致 FID 从 5.154 退化至 10.968，R-Precision Top-1 从 0.449 降至 0.350——这是所有消融中退化最剧烈的项，确证了时空注意力是系统最关键组件。
- **共享交叉注意力**：每个个体的查询关注另一个个体的键和值（Equation 7），显式建模个体间信息交换。移除后 FID 升至 7.306，R-Precision Top-1 降至 0.392。
- **协同掩码与交替建模对比**：逐人交替建模（Alternative Modeling）虽然多样性略高，但交互质量显著下降（FID 7.637 vs 5.154），验证了同时掩码并预测两人令牌的必要性。

### 适用边界与局限

InterMask 的当前能力边界明确：

1. **序列长度固定**：目前仅支持约 10 秒的固定长度运动序列，尚未验证对更长或不定长序列的扩展性。这一限制源于 VQ-VAE 的固定降采样结构和 Transformer 的位置编码设计。

2. **身体穿透问题**：将输出骨架转换为 SMPL 网格时可能出现身体穿透（Figure 14 第一行）。当前框架未集成网格转换与抗穿透损失，需要额外的后处理或训练约束。

3. **数据集隐含偏见**：模型可能受到训练数据中动作分布的影响，例如在未明确提及跳舞时将动作倾向跳舞（Figure 14 第二行）。这反映了生成模型对数据分布偏差的敏感性，而非方法本身的架构缺陷。

4. **多样性权衡**：在 MModality 指标上略低于部分扩散方法，表明掩码建模在生成多样性上存在提升空间。随机掩码概率 $p_r=0.8$ 被证明是交互质量与反应多样性之间的最佳平衡点（Table 4）。

### 开放问题与扩展方向

1. **多人扩展**：协同掩码框架理论上可扩展至三人及以上个体的交互生成，但交叉注意力的计算复杂度将随人数平方增长，需要设计更高效的注意力机制或分组策略。

2. **抗穿透集成**：如何在训练中端到端地集成网格转换与抗穿透损失，避免两阶段处理带来的误差累积，是提升物理合理性的关键方向。

3. **偏见缓解**：通过数据增强、平衡采样或在文本条件中引入更细粒度的动作类型约束，减少数据集固有偏见对生成结果的影响。

4. **长序列生成**：突破当前固定长度限制的可能路径包括：引入层级化令牌图（多尺度时间降采样）、采用滑动窗口生成策略，或结合自回归与掩码建模的混合框架。

5. **多样性-一致性平衡**：在保持交互一致性的前提下提升生成多样性，可能需要探索温度调节采样、引导强度动态调整或引入隐变量建模等技术。

## 原文 PDF

![[paperPDFs/ICLR_2025/InterMask_3D_Human_Interaction_Generation_via_Collaborative_Masked_Modelling.pdf]]