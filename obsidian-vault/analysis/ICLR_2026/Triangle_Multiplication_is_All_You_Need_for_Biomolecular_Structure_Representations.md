---
title: "Triangle Multiplication is All You Need for Biomolecular Structure Representations"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Triangle_Multiplication_is_All_You_Need_for_Biomolecular_Structure_Representations.pdf
project_link: null
code_link: https://github.com/genesistherapeutics/pairmixer
openreview_forum_id: CrXcfMLR9q
aliases:
- TMIAYNBSR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/chemistry_and_drug_discovery
core_operator: "Pairmixer replaces Pairformer attention updates with incoming and outgoing triangle multiplication plus FFN over 2-D pair representations."
primary_logic: "It keeps pair representations explicit, removes sequence update and triangle attention, and uses matrix-multiplication-based triangle mixing before the structure module."
claims:
- "Triangle multiplication alone preserves high-order geometric reasoning while lowering Pairformer training and inference cost."
- "Pairmixer matches Pairformer mean lDDT on RCSB while using about 66% of the training time."
- "Low-norm dropout analysis suggests triangle multiplication relies on sparse high-norm residue-pair interactions."
---

# Triangle Multiplication is All You Need for Biomolecular Structure Representations

> [!tip] 核心洞察
> 三角乘法本身已经能够聚合残基三元组几何关系；Pairmixer 将 Pairformer 简化为 incoming/outgoing triangle multiplication 加 FFN，以更低常数开销保留二维 pair representation 的几何推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Triangle Multiplication is All You Need for Biomolecular Structure Representations |
| 英文题名 | Triangle Multiplication is All You Need for Biomolecular Structure Representations |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=CrXcfMLR9q) · [GitHub](https://github.com/genesistherapeutics/pairmixer) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/chemistry_and_drug_discovery |
| Method |  |
| Dataset | |

> [!tip] 效果简介
> 结果与证据沿用下文“实验与关键发现”中的现有记录；本轮不新增或外推论文事实。

## 概要

生物分子结构预测与设计领域长期依赖基于注意力机制的 Pairformer 架构，该架构通过序列更新、三角注意力和三角乘法等模块捕获残基对之间的复杂几何关系。然而，注意力机制带来的二次计算复杂度严重制约了训练与推理效率，尤其在大规模序列场景下成为瓶颈。

本文提出 **Pairmixer**，一种完全移除注意力的高效特征提取器。核心思路是显式维护二维对表示（pair representation），仅通过三角乘法（triangle multiplication）和前馈网络进行更新，彻底去除序列更新和三角注意力两个模块。三角乘法通过矩阵乘法密集聚合全序列特征，同时能有效捕获残基三元组之间的稀疏几何关系，在保持几何推理能力的前提下显著降低计算开销。

在 RCSB（Boltz）测试集上，Pairmixer 的 mean lDDT 达到 0.78，与 Pairformer 持平（Figure 4）。训练效率方面，Pairmixer 仅需 Pairformer 约 66% 的训练时间即可达到同等精度，训练成本降低约 34%。推理速度在 512 token 序列上实现 1.6 倍加速（21 秒 vs 34 秒），长序列场景下加速可达 4 倍。在 BoltzDesign 蛋白质设计框架中，采样速度提升超过 2 倍。

消融实验表明，三角乘法对稀疏几何关系的捕获具有鲁棒性：在低范数 dropout 高达 75% 时性能保持稳定，而随机 dropout 超过 25% 时性能急剧下降，说明模型依赖少数关键残基对的强交互。与纯 Transformer 架构的对比中，Pairmixer 在 lDDT 指标上以 93.7% 的胜率显著领先，验证了二维对表示在捕获成对交互方面的优势。



生物分子结构预测（蛋白质、核酸、小分子及其复合物）是计算结构生物学的核心问题。近年来，以 AlphaFold 系列为代表的深度学习方案取得了突破性进展，其主干网络普遍采用基于成对表征（pair representation）的架构来捕获残基/原子间的几何关系。当前事实上的标准主干是 **Pairformer**，它组合了三角形注意力（triangle attention）、三角形乘法（triangle multiplication）和序列注意力（sequence attention）等模块，通过迭代更新成对表征来实现高精度结构预测。

然而，这一范式存在显著的效率瓶颈。三角形注意力需要对成对表征的 $N \\times N$ 矩阵沿两个维度分别执行轴向注意力，其计算复杂度与序列长度 $N$ 呈平方关系，且实际运行中内存占用和推理延迟随序列增长急剧膨胀。在长序列场景（如大型蛋白质复合物）下，这直接限制了模型的吞吐量和实际部署可行性。

本文的核心动机源于一个关键观察：**三角形乘法本身已经隐式地编码了高阶几何约束**，而三角形注意力是否不可或缺，此前并无系统性的消融证据。作者提出，通过移除三角形注意力和序列注意力，仅保留三角形乘法与前馈网络，并引入一种新的矩阵乘法驱动的 token 混合机制，即可在保持几何推理能力的同时大幅提升计算效率。这一设计催生了 **Pairmixer**——一个完全摒弃注意力机制、以矩阵乘法实现 token 混合的高效主干架构。

需要指出的是，关于“三角形乘法足以替代注意力”这一核心假设的因果机制和理论分析，论文中并未给出严格的形式化证明，仅通过实验验证了其经验有效性。后续章节将详细展开架构设计和实验支撑。



## 核心方法与创新机理

Pairmixer 的核心创新在于**以纯矩阵乘法替代注意力机制，同时保留高阶几何推理能力**。具体而言，该方法识别并移除了 Pairformer 主干网络中的两个冗余模块——序列更新（sequence updates）和三角注意力（triangle attention），仅保留入向三角乘法（incoming triangle multiplication）、出向三角乘法（outgoing triangle multiplication）以及前馈网络（FFN），构成一个完全无注意力的特征提取器。

这一设计的理论依据在于：三角乘法通过残基三元组（residue triplets）的聚合机制，能够等效地捕获几何一致的配对表示，但计算代价显著低于三角注意力。三角乘法密集地聚合全序列特征，同时通过调整特征范数的大小来有效地捕捉稀疏的几何关系。

在架构层面，Pairmixer 仅更新配对表示 $z^{\text{msa}}$，而保持单序列表示 $s^{\text{init}}$ 不变。其主干网络严格遵循 Algorithm 1 的简单结构：

$$z_l \leftarrow z_l + \text{TriMulIncoming}(z_l)$$
$$z_l \leftarrow z_l + \text{TriMulOutgoing}(z_l)$$
$$z_{l+1} \leftarrow z_l + \text{FFN}(z_l)$$

这一简化带来了显著的效率增益：训练成本降低 34%，长序列推理速度最高提升 4 倍，同时在 RCSB 测试集上保持了与 Pairformer 相当的 mean lDDT（0.78）。



![[assets/figures/papers/iclr26_0009_CrXcfMLR9q_Triangle_Multiplication_is_All_You_Need_for_Biom/figures/004_Figure_4.jpg]]
*Figure 4: (a) Pairformer architecture. The de facto biomolecular structure prediction backbone. (b) Pairmixer architecture. An efficient yet effective biomolecular structure prediction backbone*

Pairmixer 是一个面向生物分子结构预测与设计的注意力无关特征提取器，它直接替换 AlphaFold3 体系中的 Pairformer 骨干网络，同时保持管道其余模块不变。整体管道遵循生物分子结构预测的标准流程：给定一组序列，模型预测所有序列在单一复合物中的三维折叠结构（Figure 2）。

### 输入表示与初始化

管道的输入是序列列表。每条序列首先通过序列嵌入和模板模块处理，生成单序列表示 $s^{\text{init}}$ 和初始多序列比对表示 $z^{\text{msa}}$。初始的 pair 表示由单序列表示与位置编码组合而成：

$$z_{ij} = s_i + s_j + \mathbf{PE}(i, j)$$

这个 2-D pair 表示是整个 Pairmixer 骨干网络唯一处理和更新的对象——单序列表示 $s^{\text{init}}$ 在 Pairmixer 中保持不变。

### 骨干网络：从 Pairformer 到 Pairmixer

Pairformer 骨干网络包含两个并行的更新路径：pair 表示路径和单序列表示路径。pair 表示路径由三角形自注意力（Triangle Attention）和三角形乘法（Triangle Multiplication）交替组成，单序列路径则使用带 pair bias 的序列注意力。Pairmixer 的设计核心是识别并移除 Pairformer 中的两个冗余模块：**序列更新**和**三角形注意力**。

Pairmixer 骨干网络仅保留三个操作，按顺序执行（Algorithm 1）：

1. **Incoming Triangle Multiplication**：沿行方向聚合特征
2. **Outgoing Triangle Multiplication**：沿列方向聚合特征
3. **Feed-Forward Network (FFN)**：逐位置非线性变换

形式化地，三角形乘法的核心运算为：

$$\mathrm{TriMul}(z)_{ij} = \sum_{k=1}^{L} (W_a z_{ik}) \odot (W_b z_{jk})$$

该操作通过矩阵乘法将 pair 表示中不同行/列的特征进行密集聚合，从而隐式地捕获残基三元组之间的几何关系。与三角形注意力不同，三角形乘法不依赖 softmax 归一化的注意力权重，而是通过可学习的线性投影和逐元素乘积来混合信息。

### 与上下游模块的连接

Pairmixer 作为特征提取器，位于 MSA 模块与结构模块之间。具体集成方式为：

- **上游**：MSA 模块输出的 pair 表示 $z^{\text{msa}}$ 直接输入 Pairmixer 骨干网络。在 Pairmixer 版本中，MSA 模块中的三角形注意力也被移除，仅保留三角形乘法。
- **下游**：Pairmixer 更新后的 pair 表示 $z^{\text{backbone}}$ 与单序列表示 $s^{\text{init}}$ 一同输入结构模块（扩散模块），用于预测最终的三维坐标。

在 Transformer 基线中，pair 表示的更新方式不同：它不经过独立的 pair 更新路径，而是通过单序列表示的外和来间接更新：

$$z_{ij}^{\text{backbone}} = z_{ij}^{\text{msa}} + W_{sz} s_i^{\text{backbone}} + W_{sz} s_j^{\text{backbone}}$$

### 架构对比

Figure 3 和 Figure 10 给出了 Pairformer、Pairmixer 和 Transformer 三种骨干架构的并排对比。核心差异在于：

- **Pairformer**：包含序列更新 + pair 更新（三角形注意力 + 三角形乘法 + FFN）
- **Pairmixer**：无序列更新，pair 更新仅含三角形乘法 + FFN，完全移除注意力机制
- **Transformer**：仅保留序列更新（标准注意力），pair 表示通过序列外和被动更新

Pairmixer 的设计理念是：三角形乘法本身已具备捕获几何一致性 pair 表示的能力，且计算成本显著低于三角形注意力。通过显式物化 2-D pair 表示并用三角形乘法更新，Pairmixer 在保持几何推理能力的同时，大幅简化了架构。



### Pairmixer 骨干架构

Pairmixer 是一个**无注意力特征提取器**，仅更新对表示 $z^{\text{msa}}$，而不改变单序列表示 $s^{\text{init}}$。其核心设计原则是：在 Pairformer 基础上移除两个冗余模块——序列更新（sequence updates）和三角注意力（triangle attention），仅保留三角乘法（triangle multiplication）和前馈网络（FFN）。

如 Algorithm 1 所示，Pairmixer 骨干的每一层仅包含三个操作：

1. **入边三角乘法**（TriMulIncoming）
2. **出边三角乘法**（TriMulOutgoing）
3. **前馈网络**（FFN）

更新过程为：
$$z_l \leftarrow z_l + \text{TriMulIncoming}(z_l)$$
$$z_l \leftarrow z_l + \text{TriMulOutgoing}(z_l)$$
$$z_{l+1} \leftarrow z_l + \text{FFN}(z_l)$$

这种极简设计使得 Pairmixer 完全移除了骨干中的注意力机制，转而通过矩阵乘法实现 token 间的混合。

### 关键公式

#### 对表示初始化

对表示 $z$ 的初始值由单表示和位置编码组合而成：

$$z_{ij} = s_i + s_j + \mathbf{PE}(i, j)$$

其中 $s_i$、$s_j$ 为残基 $i$ 和 $j$ 的单表示，$\mathbf{PE}(i,j)$ 为相对位置编码。

#### 三角乘法

三角乘法是对表示更新的核心操作，通过对第三维求和来整合不同行/列的特征：

$$\mathrm{TriMul}(z)_{ij} = \sum_{k=1}^{L} (W_a z_{ik}) \odot (W_b z_{jk})$$

其中 $W_a$、$W_b$ 为可学习的投影矩阵，$\odot$ 表示逐元素乘积，$L$ 为序列长度。该操作通过遍历所有 $k$，密集聚合整条序列的特征，但通过调整特征幅值来高效捕获残基三元组之间的稀疏几何关系。

#### 三角注意力（被移除的模块）

作为对比，Pairformer 中的三角注意力公式为：

$$\mathbf{TriAtt}(z)_i = \mathrm{softmax}\left( (W_Q z_i)(W_K z_i)^\top + W_B z \right) W_V z_i$$

该操作将对表示的每一行视为独立序列，施加带对偏置的序列注意力。Pairmixer 的消融实验表明，三角注意力和三角乘法对 Pairformer 性能均至关重要（移除任一模块均导致 IDDT 从 0.74 降至 0.70），但三角乘法能以更低的计算成本提供等价的三元组几何推理能力，因此 Pairmixer 选择保留三角乘法而舍弃三角注意力。

#### 稀疏三角乘法（分析用）

为分析三角乘法的工作机制，论文引入了带 dropout 的变体：

$$\mathrm{TriMulWithDropout}(z)_{ij} = \sum_{k=1}^{L} (W_a z_{ik}) \odot (W_b z_{jk}) \cdot M(z_{ik}) M(z_{jk})$$

其中低范数 dropout 掩码定义为：

$$M(z_{ik}) = \begin{cases} 1, & \text{if } k \in \text{Top}_{1-\gamma}(\{\|z_{il}\|\}_{l=1}^{L}) \\ 0, & \text{otherwise} \end{cases}$$

该掩码保留对表示范数最大的前 $1-\gamma$ 比例的交互，用于验证三角乘法对稀疏几何关系的捕获能力。



## 实验与关键发现

### 训练效率与精度权衡

Pairmixer 的核心主张是在不牺牲预测精度的前提下大幅提升训练与推理效率。Figure 4 的训练曲线直接验证了这一点：在 RCSB 测试集上，Pairmixer（Large Phase2）达到与 Pairformer 基线相同的 mean lDDT 0.78，但训练时间仅需后者的 66%（约 34% 的训练成本节省）。这一效率优势在 Small、Medium、Large 三个模型规模上均一致成立——Pairmixer 的橙色虚线始终位于 Pairformer 的青色虚线左侧，意味着达到同等精度所需的 GPU 天数更少。

![[assets/figures/papers/iclr26_0009_CrXcfMLR9q_Triangle_Multiplication_is_All_You_Need_for_Biom/figures/005_Figure_4.jpg]]
*Figure 4: Performance curves on RCSB test set across model sizes. We compare three backbone architectures across three model sizes over training. Pairmixer matches or surpasses the Pairformer baseline while training more efficiently*

Table 4 的完整指标矩阵进一步确认了系统级性能：在 Boltz RCSB 测试集上，Pairmixer 的 DOCKQ>0.23 为 0.63（Pairformer 为 0.64），lDDT_PLI 为 0.73（持平），ligand RMSD<2 为 0.55（略优于 Pairformer 的 0.54）。在 CASP15 测试集（Table 5）上，Pairmixer 的 IDDT 为 0.39，与 Pairformer 持平。这些结果表明，移除 triangle attention 和 sequence update 后，triangle multiplication 与 feed-forward network 的组合足以维持几何一致性推理能力。

![[assets/figures/papers/iclr26_0009_CrXcfMLR9q_Triangle_Multiplication_is_All_You_Need_for_Biom/figures/033_Table_4.jpg]]
*Table 4: Model Performance on the Boltz RCSB test set. The metric is computed on the bestperforming protein out of five samples (oracle)*

### 推理速度与下游应用加速

推理速度是 Pairmixer 的另一关键优势。Figure 5 显示，在 512 tokens 输入下，Pairmixer 完成推理仅需 21 秒，而 Boltz-1 需要 34 秒，加速比 1.6×。随着序列长度增长至 1024 tokens，Pairmixer 的优势进一步扩大，达到约 4× 的推理加速。这一加速来源于 triangle attention 的完全移除——triangle attention 的复杂度为 $O(L^3 C_z)$，而 triangle multiplication 虽同为 $O(L^3 C_z)$，但常数因子显著更小（Table 3 的 FLOPs 分解显示 Pairformer 的 $12L^3 C_z$ 项主要来自 triangle attention）。

![[assets/figures/papers/iclr26_0009_CrXcfMLR9q_Triangle_Multiplication_is_All_You_Need_for_Biom/figures/009_Figure_5.jpg]]
*Figure 5: Inference speed analysis. We measure runtime across architectures and input sizes. While the Transformer is the fastest overall, Pairmixer achieves substantially lower inference times than Pairformer, particularly on longer sequences*

在下游 binder 设计任务中，效率优势同样显著。Table 2 显示，BindFast（基于 Pairmixer 的 BoltzDesign 变体）在生成 110 残基 binder 时，相比原版 BoltzDesign 实现 2×–2.6× 加速，且将目标蛋白的尺寸上限从 500 残基扩展至 650 残基，同时避免了原版在长序列上的 OOM 问题。

![[assets/figures/papers/iclr26_0009_CrXcfMLR9q_Triangle_Multiplication_is_All_You_Need_for_Biom/figures/014_Table_2.jpg]]
*Table 2: Runtime comparison of generating proteins with Pairmixer and Pairformer in the BoltzDesign framework. For biologically relevant targets of various sequence lengths, we generate three 110-residue binders using 160 iterations in all settings and report the average running time*

### 消融实验：哪些模块真正必要？

Table 6 的 Pairformer 消融实验揭示了各模块的重要性排序。移除 triangle multiplication 或 triangle attention 均导致 IDDT 从 0.74 降至约 0.70，表明两者对性能均有显著贡献。相比之下，移除 sequence update 对性能影响极小。这一发现直接支撑了 Pairmixer 的设计决策：保留 triangle multiplication，移除 triangle attention 和 sequence update。Table 7 的 Pairmixer 消融进一步验证了架构选择的合理性——默认配置（triangle multiplication + FFN）在各项指标上均达到最优。

Table 11 的 mixing method 消融对比了四种替代方案：FFT、AvgPool、TriMul-rows（仅行方向）、TriMul-both（行列双方向）。TriMul-both 在 lDDT（0.71）、DOCKQ>0.49（0.42）、lDDT_PLI（0.50）和 RMSD<1（0.33）四项指标上全面领先，证明行列双向的 triangle multiplication 是最有效的 token mixing 策略。

![[assets/figures/papers/iclr26_0009_CrXcfMLR9q_Triangle_Multiplication_is_All_You_Need_for_Biom/figures/039_Table_11.jpg]]
*Table 11: (c) Mixing Method*

### Triangle Multiplication 的工作机制分析

Figure 8 的稀疏化实验揭示了 triangle multiplication 如何高效捕获几何关系。在随机 dropout 下，性能在 dropout 率超过 25% 后迅速下降；但在 low-norm dropout（按 pair representation 范数保留 top-$(1-\gamma)$ 交互）下，即使 dropout 率达到 75%，性能仍保持稳定。这表明 triangle multiplication 虽然形式上密集聚合所有 token 对，但其有效信息主要集中于少数高范数交互——模型通过调整 pair representation 的幅值自然地实现了稀疏化。

Figure 9 的 blockwise dropout 实验进一步表明，triangle multiplication 严重依赖长程交互。当仅保留局部 block 内的交互时，即使对于局部度量 lDDT，性能也快速退化。这解释了为何简单的局部聚合方法（如 AvgPool）无法替代 triangle multiplication。

### 与 Transformer 基线的对比

Figure 7 的头对头比较显示，Pairmixer 在 lDDT 上以 93.7% 的胜率超越 Transformer 基线，在 RMSD 上以 74.7% 的胜率领先。这表明 2-D pair representation 配合 triangle multiplication 的 triplet 推理机制，比单纯的序列级 attention 更擅长捕获残基对之间的几何约束。Transformer 基线虽然在训练 FLOPs 上更轻量（Figure 1），但其精度天花板明显低于 Pairmixer——在 Figure 4 中，Transformer（紫色）的训练曲线在所有模型规模上均低于 Pairmixer 和 Pairformer。

### 局限性与待验证点

PoseBusters 蛋白-配体复合物基准（Table 1）上，Pairmixer 的 RMSD<2 为 0.67，略低于 Pairformer 的 0.68；IDDT_PLI 为 0.73，略低于 Pairformer 的 0.74。这一微小差距提示，在蛋白-配体相互作用这类需要精细几何建模的任务上，triangle attention 可能仍提供了一定的边际收益，尽管在主要蛋白质结构预测指标上该差距不可见。此外，所有实验均基于 Boltz-1 框架，Pairmixer 在其他结构预测框架（如 AlphaFold3 原版）上的迁移效果需要手动验证。



## 定位与知识库关联

### 与 AlphaFold3 / Boltz-1 谱系的关系

Pairmixer 直接构建在 Boltz-1（AlphaFold3 的后继实现）之上，核心改动是**替换 Pairformer 骨干网络并移除 MSA Module 中的 triangle attention**[part_003]。它保留了 Boltz-1 的其他所有模块（MSA 处理、Structure Module、扩散解码等），仅对特征提取器的 pair representation 更新路径进行简化。

具体而言，Pairmixer 从 Pairformer 中**识别并移除了两个被判定为冗余的模块**：sequence updates（序列更新）和 triangle attention（三角注意力）[part_002]。保留下来的组件是 incoming triangle multiplication、outgoing triangle multiplication 和 feed-forward network，这三者构成 Pairmixer 骨干的全部操作[part_002, Algorithm 1]。

从架构谱系看，该工作定义了一条清晰的简化路径：
- **Pairformer**：sequence attention with pair bias + triangle attention + triangle multiplication + FFN（双路径更新 single 和 pair representation）
- **Pairmixer**：仅 triangle multiplication + FFN（单路径，仅更新 pair representation $z^\text{msa}$，不更新 $s^\text{init}$）[part_002]
- **Transformer baseline**：仅 sequence attention with pair bias + FFN（移除 pair update，MSA 模块额外输出 $s^\text{msa}$）[part_006, A.2]

这一谱系表明，**triangle multiplication 是 Pairformer 性能的核心来源**，而 triangle attention 和 sequence updates 可以被移除而不损害精度，前提是保留 triangle multiplication 的 triplet reasoning 能力[part_002, part_003]。

### 与 Transformer 基线的对比定位

论文设置了 Transformer 基线来验证 pair representation 的必要性。Transformer 基线完全移除 pair update，仅通过 outer sum $z_{ij}^\text{backbone} = z_{ij}^\text{msa} + W_{sz} s_i^\text{backbone} + W_{sz} s_j^\text{backbone}$ 从序列表示间接构建 pair 特征[part_006, A.2]。

Head-to-head 对比显示，Pairmixer 在 lDDT 上以 **93.7% 的胜率**超越 Transformer，在 RMSD 上以 **74.7% 的胜率**超越[part_004, Figure 7]。这从实验上确立了 **显式 pair representation + triangle multiplication** 相对于纯序列注意力的优势，也为理解 Pairmixer 的能力边界提供了参照：当 pair 更新被完全移除时，模型对 pairwise interaction 的捕捉能力显著下降。

### 适用边界

**已验证的适用场景：**

1. **蛋白质结构预测**：在 RCSB (Boltz) 测试集上，Pairmixer Large Phase2 达到 mean lDDT 0.78，与 Pairformer 持平[part_003, Figure 4]。在 CASP15 测试集上（Medium, 68 epochs），lDDT 为 0.39[part_007, Table 5]。

2. **蛋白质-配体复合物**：在 PoseBusters 基准（298 样本）上，Pairmixer 的 ligand RMSD < 2Å 为 0.55（vs Boltz-1 的 0.54），略有改善；lDDT-PLI 为 0.73（vs 0.75），略低[part_003, Figure 6; part_008 提及 Table 1]。

3. **抗体-抗原复合物**：DockQ > 0.23 指标上 Pairmixer 为 0.63，略低于 Boltz-1 的 0.64[part_003, Figure 6; part_007, Table 4]。

4. **蛋白质 binder 设计**：在 BoltzDesign 框架中替换为 Pairmixer 后（称为 BindFast），采样速度提升 **2× 至 2.6×**，目标蛋白长度上限从 500 残基扩展到 **650 残基**，且避免了大序列长度下的 OOM 问题[part_008, C.4; Table 2]。

**效率边界：**

- 训练成本降低 **34%**（Abstract 声明）
- 推理速度：512 tokens 时 21 秒 vs Boltz-1 的 34 秒（**1.6× 加速**）；长序列上可达 **4× 加速**[part_001, part_003, Figure 5]
- 速度优势随序列长度增长而扩大[part_003, Figure 5]

### 局限与待验证问题

**1. 蛋白质-蛋白质相互作用指标的轻微退化**

在 DockQ > 0.23 指标上，Pairmixer（0.63）略低于 Pairformer（0.64），表明在蛋白质复合物界面预测的某些方面可能存在细微差距[part_003, Figure 6]。这一退化幅度很小（约 1.6%），但方向一致，需要更大规模评估来确认是否具有统计显著性。

**2. 稀疏化鲁棒性的非对称特征**

Pairmixer 对不同类型的稀疏化表现出截然不同的鲁棒性[part_004, Figure 8, Figure 9]：
- **随机 dropout**：dropout 率超过 25% 时性能快速下降
- **低范数 dropout**（保留高范数交互）：可容忍高达 75% 的 dropout 率
- **块状 dropout**（仅保留局部交互）：即使仅评估局部度量，性能也快速下降

这表明 triangle multiplication 虽然形式上密集聚合全序列特征，但实际**依赖长程交互和少数关键残基对**。这一特性既是效率优势的来源（可以通过范数引导的稀疏化进一步压缩），也暴露了潜在脆弱性：当关键的长程交互被破坏时，模型缺乏 triangle attention 那样的显式注意力权重来灵活重分配计算资源。

**3. 需要额外训练来恢复性能**

Pairmixer 的消融实验显示，直接移除 triangle attention 或 triangle multiplication 会导致 lDDT 从 0.74 降至 0.70[part_008, Table 6]。论文明确指出 Pairmixer “通过额外训练恢复性能”[part_008, D.1]。这意味着 Pairmixer 不是一个即插即用的零成本替换——从 Pairformer 迁移到 Pairmixer 需要重新训练，而非仅加载预训练权重。

**4. 开放问题**

- **其他生物分子模态的验证**：当前验证集中在蛋白质、蛋白质-配体、抗体-抗原和 RNA（Table 3, 27 样本）。对 DNA、共价修饰、翻译后修饰等场景的适用性尚未系统评估。
- **更大规模下的 scaling 行为**：论文测试了 Small / Medium / Large 三种规模，但未探索与 AlphaFold3 原始规模（~93M 参数）相当的配置下 Pairmixer 是否仍能保持精度持平。
- **triangle multiplication 的理论表达力上界**：论文通过实验论证了 triangle multiplication 足以替代 triangle attention，但未从理论上证明两者的表达力等价性。低范数 dropout 的鲁棒性暗示 triangle multiplication 可能隐式学习了稀疏的几何约束，其理论机制值得深入分析。



## 原文 PDF

![[paperPDFs/ICLR_2026/Triangle_Multiplication_is_All_You_Need_for_Biomolecular_Structure_Representations.pdf]]
