---
title: "Relationship Alignment for View-aware Multi-view Clustering"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Relationship_Alignment_for_View_aware_Multi_view_Clustering.pdf
openreview_forum_id: uRA9cT4MK6
aliases:
- RAVAMVC
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "通过全局-局部关系对齐保持邻域结构，并结合基于视图相似度的自适应加权标签对比学习"
primary_logic: "关系对齐提供的稳定邻域结构能够更准确地度量视图差异，进而借助自适应加权对比学习实现可靠的语义对齐"
claims:
- "所提方法在多个基准数据集上达到最优聚类性能"
- "视感知自适应加权机制显著提升了聚类精度"
- "关系对齐模块和标签对比学习模块对性能不可或缺"
- "关系对齐有效保持了样本邻域结构，使全局特征聚类结构随训练逐渐清晰"
---

# Relationship Alignment for View-aware Multi-view Clustering

> [!tip] 核心洞察
> 关系对齐提供的稳定邻域结构能够更准确地度量视图差异，进而借助自适应加权对比学习实现可靠的语义对齐

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 视角感知多视图聚类的关系对齐 |
| 英文题名 | Relationship Alignment for View-aware Multi-view Clustering |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=uRA9cT4MK6); [GitHub](https://github.com/chenzhe207/RAV) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | RAV |
| Dataset | NGs, YoutubeVideo, Cora |

> [!tip] 效果简介
> - NGs 上，ACC 为 0.980，对比 0.936，变化 +0.044。
> - YoutubeVideo 上，ACC 为 0.356，对比 0.318，变化 +0.038。
> - Cora 上，ACC 为 0.592，对比 0.567，变化 +0.025。

## 概述

多视图聚类旨在从多个异构特征表示中挖掘一致的样本分组结构。现有方法普遍面临两个瓶颈：一是忽视跨视图样本邻域结构的一致性，导致不同视图的嵌入空间出现冲突；二是无法自适应地利用视图间的相似性差异，使得语义信息在融合过程中退化。针对这些问题，本文提出视角感知多视图聚类框架 **RAV (Relationship Alignment for View-aware Multi-view Clustering)**，其核心思路是通过**关系对齐**保持稳定的邻域结构，并借助该结构更准确地度量视图差异，进而以**自适应加权标签对比学习**实现可靠的语义对齐。

RAV 包含两个关键模块：**跨视图关系对齐模块**构建各视图特有关系矩阵并与全局关系矩阵对齐，从样本拓扑层面增强视图间一致性；**视感知标签对比学习模块**则基于 Wasserstein 距离动态调制视图对之间的对比强度，使相似度高的视图对贡献更大的语义监督信号。两者协同作用——关系对齐提供的稳定邻域为视图差异度量创造了条件，而自适应加权则据此抑制低质量视图对比带来的语义退化。

在 10 个多视图基准数据集上的实验表明，RAV 在聚类精度（ACC）、归一化互信息（NMI）和纯度（PUR）三项指标上整体优于 MFLVC、MVCAN、DFL-NET 等代表性基线。典型增益包括：NGs 数据集 ACC 从 0.936 提升至 **0.980**（+4.4%），YoutubeVideo 从 0.318 提升至 **0.356**（+3.8%），Cora 从 0.567 提升至 **0.592**（+2.5%）。消融实验进一步验证了关系对齐和自适应加权各自的关键作用——去除任一模块均导致性能显著下降，其中 Caltech-5V 上去除标签对比损失后 ACC 从 0.901 骤降至 0.424。

## 背景与动机

多视图聚类旨在从同一组样本的多个异构表示中挖掘一致的簇结构。其核心挑战在于：不同视图捕捉样本的不同侧面，如何有效融合这些互补信息并消除视图间的语义冲突。近年来，深度多视图聚类方法取得了显著进展，但两个根本性瓶颈仍未解决。

**瓶颈一：跨视图样本邻域结构不一致。** 现有方法通常聚焦于样本特征的直接对齐或聚类分配的一致性约束，却忽视了样本间关系结构在跨视图迁移中的稳定性。具体而言，同一对样本在不同视图中的相似性可能差异显著——若仅对齐特征或标签而放任关系矩阵自由漂移，视图特化编码器将产生相互冲突的嵌入空间，导致语义信息在融合过程中退化。这一问题的本质是缺乏对样本邻域结构的显式保持机制。

**瓶颈二：视间相似性差异被均等化处理。** 以 MFLVC、MVCAN、DFL-NET 和 SEM 为代表的近期方法，在标签对比学习中对所有视图对赋予等权重。然而，不同视图对之间的语义重叠程度天然不同——例如，文本视图与图像视图的相似性通常低于两个图像视图之间的相似性。无视这种差异的均等加权策略，会迫使语义差距大的视图对进行同等强度的对齐，引入表示冲突，反而损害聚类质量。

上述两个瓶颈之间存在深层耦合：缺乏稳定的邻域结构作为参照，视图间相似性的度量本身就不可靠；而缺乏自适应加权机制，即便关系结构被保持，标签对齐过程仍可能因视差过大而失效。

本文提出 **RAV（Relationship Alignment for View-aware Multi-view Clustering）**，核心动机在于：通过全局-局部关系对齐为跨视图比较提供稳定的邻域结构基础，再借助基于 Wasserstein 距离的自适应加权机制，使标签对比学习能够感知视图间的语义亲疏，从而在保持邻域一致性的前提下实现可靠的语义对齐。这一"关系锚定 + 视感知加权"的协同设计，从根本上回应了现有方法的两个结构性缺口。

## 核心创新

RAV 的核心创新并非引入全新的学习范式，而是精准定位了现有深度多视图聚类方法的两个关键瓶颈，并通过两个高度协同的模块予以解决。

**瓶颈一：跨视图样本邻域结构不一致。** 现有方法（MFLVC、MVCAN 等）通常直接对齐样本的深度特征或聚类分配，却忽视了样本间关系结构在不同视图下的一致性。这导致不同视图的表示之间存在结构冲突，难以形成统一的聚类语义。

**瓶颈二：视图间相似度差异被忽视。** 传统标签对比学习方法对所有视图对赋予等权重，未考虑视图间深层特征相似度的差异。当某些视图对语义差异较大时，强制对齐会引入噪声，反而导致表示退化。

针对上述瓶颈，RAV 引入了两个核心 changed slots：

- **样本关系对齐（Cross-View Relation Alignment）：** 为每个视图构建基于高斯核的样本关系矩阵 $s_{ik}^{v}$，并构建一个全局关系矩阵作为"锚点"，通过全局-局部对比损失 $\mathcal{L}_{\mathrm{S}}$ 将各视图的关系结构向全局结构对齐。这一机制显式地保持了跨视图的样本邻域一致性，为后续的语义对齐提供了稳定基础。

- **视感知自适应加权标签对比学习（View-aware Adaptive Weighting）：** 引入基于 Wasserstein 距离的视图相似度度量，动态计算每对视图之间的权重 $w_{(v,u)}$，并以此调制标签对比损失 $\ell_{c}^{(v,u)}$ 的强度。相似度高的视图对获得更大权重以强化一致语义，相似度低的视图对权重降低以抑制冲突，最终形成自适应加权损失 $\mathcal{L}_{\mathsf{Q}}$。

**协同机制**是 RAV 的核心洞察：关系对齐模块提供的稳定邻域结构，使得基于深层特征的视图相似度度量更加准确可靠；而准确的视图相似度又驱动自适应加权机制实现更精准的语义对齐。两者形成正向反馈循环，共同实现鲁棒的多视图聚类。

## 整体框架

![[assets/figures/papers/iclr26_0009_uRA9cT4MK6_Relationship_Alignment_for_View-aware_Multi-view/figures/001_Figure_1.jpg]]
*Figure 1: An illustration of the proposed RAV framework. The model crucially incorporates two modules: cross-view relation alignment to maintain neighborhood structures, and view-aware adaptive weighting in label contrastive learning to counteract representation degradation from view dissimilarity, thereby achieving robust multi-view clustering*

RAV 框架围绕一个核心洞察构建：**稳定的样本邻域结构能够更准确地度量视图间差异，进而支持自适应加权的语义对齐**。为此，框架将四个功能模块串联为统一的端到端优化流程。

### 输入与特征提取

给定 $V$ 个视图的多视图数据集，每个视图的原始特征 $\mathbf{x}^v$ 首先进入**视图特化自编码器**（View-Specific Autoencoder）。每个视图拥有独立的编码器 $f^v$ 和解码器 $g^v$，编码器将输入映射为深度隐特征 $\mathbf{z}^v$，解码器则从隐特征重建输入 $\hat{\mathbf{x}}^v$。所有视图共享同一个多层感知机（MLP）分类头，将各视图的隐特征 $\mathbf{z}^v$ 映射为软聚类分配矩阵 $\mathbf{q}^v \in [0,1]^{N \times K}$，其中 $N$ 为样本数，$K$ 为聚类数。

### 跨视图关系对齐模块

该模块是框架的**结构约束层**。对每个视图的隐特征 $\mathbf{z}^v$，通过高斯核计算视图内样本间的成对相似度，构建视图特有关系矩阵 $\mathbf{s}^v$；同时对所有视图的隐特征求平均后计算全局关系矩阵 $\mathbf{s}$。随后，以全局关系矩阵为监督信号，通过对比损失 $\mathcal{L}_{\mathrm{S}}$ 将每个视图的关系矩阵与全局关系矩阵对齐，强制保持跨视图的样本邻域结构一致性。

### 视感知标签对比学习模块

该模块是框架的**语义对齐层**。在各视图的软分配矩阵 $\mathbf{q}^v$ 之间执行标签级对比学习：同一聚类簇的分配向量在不同视图间构成正样本对，不同簇的分配向量构成负样本对。关键创新在于引入基于 Wasserstein 距离的**自适应加权机制**——根据视图对之间的深度特征相似度动态计算权重 $w_{(v,u)}$，替代传统方法中所有视图对的等权处理。相似度高的视图对获得更大权重，相似度低的视图对则被抑制，从而避免语义退化。加权后的标签对比损失 $\mathcal{L}_{\mathsf{Q}}$ 还包含熵正则项，防止退化解。

### 联合优化与预测

三个损失项——重建损失 $\mathcal{L}_{\mathrm{REC}}$、关系对齐损失 $\mathcal{L}_{\mathrm{S}}$ 和自适应加权标签对比损失 $\mathcal{L}_{\mathsf{Q}}$——通过超参数 $\lambda_1$、$\lambda_2$ 加权求和构成总损失 $\mathcal{L}_{\mathrm{total}}$，进行端到端优化。训练完成后，对所有视图的软分配矩阵取平均，再通过 $\arg\max$ 得到每个样本的最终聚类标签。

### 模块间协同关系

两个核心模块形成因果协同：关系对齐模块提供稳定的邻域结构，使得基于隐特征计算的视图相似度（Wasserstein 距离）能够更准确地反映视图间真实的语义差异；自适应加权模块则利用这一准确度量，动态调制标签对比学习的强度，在抑制低质量视图干扰的同时强化一致性视图的语义信号。消融实验（Table 5）验证了这一协同的必要性：去除关系对齐损失 $\mathcal{L}_{\mathrm{S}}$ 后，Caltech-5V 上的 ACC 从 0.901 骤降至 0.424；去除标签对比损失 $\mathcal{L}_{\mathsf{Q}}$ 同样造成性能崩溃。自适应加权机制的独立贡献在 Table 6 中得到验证：在视图差异较大的 NGs 和 ALOI 数据集上，加权机制分别带来 1.4% 和 2.5% 的 ACC 提升。

## 核心模块与公式推导

RAV 框架由三个核心模块构成：**视图特化自编码器**、**跨视图关系对齐模块**和**视感知标签对比学习模块**。各模块通过联合优化目标协同工作，最终通过融合标签预测获得聚类结果。

### 视图特化自编码器

为每个视图 $v$ 配备独立的编码器 $f^v$ 和解码器 $g^v$，从原始输入 $\mathbf{x}_{i,:}^{v}$ 提取深度特征 $\mathbf{z}_{i,:}^{v}$ 并重建 $\hat{\mathbf{x}}_{i,:}^{v}$。重建损失为所有视图所有样本的均方误差之和：

$$\mathcal{L}_{REC} = \sum_{v=1}^{V} \sum_{i=1}^{N} \| \mathbf{x}_{i,:}^{v} - \hat{\mathbf{x}}_{i,:}^{v} \|_2^2 \tag{3}$$

### 跨视图关系对齐模块

该模块解决现有方法忽视跨视图样本邻域结构一致性的瓶颈。核心思路：**先构建视图特有与全局关系矩阵，再通过对比损失将前者向后者对齐**。

**步骤一：构建关系矩阵。** 对视图 $v$ 中样本 $i$ 与 $k$，用高斯核计算视图内相似度：

$$s_{ik}^{v} = \exp\left( - \frac{ \| \mathbf{z}_{i,:}^{v} - \mathbf{z}_{k,:}^{v} \|^2 }{ \sigma } \right) \tag{4}$$

由此得到视图特有关系向量 $\mathbf{s}_{i,:}^{v}$。对所有视图的相似度求平均，得到全局关系向量 $\mathbf{s}_{i,:}$。

**步骤二：全局监督局部的对比对齐。** 以全局关系向量为锚点，将各视图特有关系向量作为正样本拉近，其他样本的全局关系向量作为负样本推开。跨视图关系对齐损失为：

$$\mathcal{L}_{\mathrm{S}} = - \frac{1}{N} \sum_{v=1}^{V} \sum_{i=1}^{N} \log \frac{ e^{ d( \mathbf{s}_{i,:}^{v}, \mathbf{s}_{i,:} ) / \tau_F } }{ \sum_{k=1}^{N} e^{ d( \mathbf{s}_{i,:}^{v}, \mathbf{s}_{k,:} ) / \tau_F } - e^{ 1/\tau_F } } \tag{6}$$

其中 $d(\cdot,\cdot)$ 为余弦相似度，$\tau_F$ 为温度系数。该损失强制各视图保持一致的邻域结构，为后续模块提供稳定的关系基础。

### 视感知标签对比学习模块

该模块解决现有方法对所有视图对等权重处理、忽视视图间相似度差异的问题。

**步骤一：标签对比损失。** 视图 $v$ 和 $u$ 通过共享 MLP 分别生成聚类软分配矩阵 $\mathbf{q}^v$ 和 $\mathbf{q}^u$。对每一簇 $j$，将两视图中同一簇的分配向量 $(\mathbf{q}_{:,j}^{v}, \mathbf{q}_{:,j}^{u})$ 作为正样本对，进行对比学习：

$$\ell_{c}^{(v,u)} = - \frac{1}{K} \sum_{j=1}^{K} \log \frac{ e^{ d( \mathbf{q}_{:,j}^{v}, \mathbf{q}_{:,j}^{u} ) / \tau_L } }{ \sum_{k=1}^{K} \sum_{m=v,u} e^{ d( \mathbf{q}_{:,j}^{v}, \mathbf{q}_{:,k}^{m} ) / \tau_L } - e^{ 1/\tau_L } } \tag{8}$$

**步骤二：基于 Wasserstein 距离的自适应加权。** 用视图深度特征分布间的 Wasserstein 距离度量视图相似度，导出动态权重 $w_{(v,u)}$。视图越相似，权重越大，对比强度越高；反之则降低冲突视图的影响。最终视感知自适应加权损失为：

$$\mathcal{L}_{\mathsf{Q}} = \frac{1}{2} \sum_{v=1}^{V} \sum_{u \neq v} \frac{1}{2} \big( w_{(v,u)} + w_{(u,v)} \big) \ell_{c}^{(v,u)} + \sum_{v=1}^{V} \sum_{j=1}^{K} r_{j}^{v} \log r_{j}^{v} \tag{12}$$

其中第二项为熵正则，防止分配退化到平凡解。

### 联合优化与标签预测

总体损失函数融合三个模块：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{REC}} + \lambda_{1} \mathcal{L}_{\mathsf{Q}} + \lambda_{2} \mathcal{L}_{\mathrm{S}} \tag{13}$$

其中 $\lambda_1$、$\lambda_2$ 为平衡超参数。最终聚类标签通过对所有视图的软分配取平均后取 argmax 得到：

$$y_{j} = \arg \max_{j} \left( \frac{1}{V} \sum_{v=1}^{V} q_{ij}^{v} \right) \tag{14}$$

**因果机制总结：** 关系对齐模块（$\mathcal{L}_{\mathrm{S}}$）提供稳定的跨视图邻域结构，使视图差异度量更准确；视感知加权模块（$\mathcal{L}_{\mathsf{Q}}$）据此动态调节标签对比强度，避免相似度低的视图对造成语义冲突。两者协同实现了可靠的语义对齐。消融实验验证了这一因果链：去除 $\mathcal{L}_{\mathrm{S}}$ 导致 Caltech-5V 上 ACC 从 0.901 骤降至 0.424（Table 5），去除自适应加权则使 NGs 上 ACC 从 0.980 降至 0.966（Table 6）。

## 实验与分析

### 实验设置

实验在十个多视图基准数据集上进行评估，涵盖不同规模与视图异构程度（Table 1）。模型基于 PyTorch 1.12.1 实现，使用 NVIDIA RTX 4090 D GPU，优化器为 Adam，学习率固定为 $0.0003$，批次大小为 256。预训练与微调阶段均设为 200 个 epoch。高斯核带宽 $\sigma = 1.0$，关系对齐与标签对比的温度系数均固定为 $\tau_F = \tau_L = 0.5$。评估指标采用聚类准确率（ACC）、归一化互信息（NMI）和纯度（PUR）。

### 主实验结果

RAV 在多数数据集上取得了最优或次优的聚类性能。在 NGs 数据集上，ACC 达到 0.980，相较次优方法 MFLVC（0.936）提升 4.4 个百分点；在 YoutubeVideo 上 ACC 为 0.356，领先次优方法 3.8 个百分点；在 Cora 上 ACC 为 0.592，较次优方法提升 2.5 个百分点（Table 2–4）。这些结果表明跨视图关系对齐与视感知自适应加权机制在视图差异显著的场景下能有效提升聚类质量。

![[assets/figures/papers/iclr26_0009_uRA9cT4MK6_Relationship_Alignment_for_View-aware_Multi-view/figures/003_Table_2.jpg]]
*Table 2: Clustering results of all methods on the NGs, Digit-Product, and ALOI datasets*

![[assets/figures/papers/iclr26_0009_uRA9cT4MK6_Relationship_Alignment_for_View-aware_Multi-view/figures/004_Table_3.jpg]]
*Table 3: Clustering results of all methods on the Cora, NUSWIDE, and Caltech-5V datasets*

![[assets/figures/papers/iclr26_0009_uRA9cT4MK6_Relationship_Alignment_for_View-aware_Multi-view/figures/005_Table_4.jpg]]
*Table 4: Clustering results of all methods on the NoisyMNIST, YoutubeVideo, 3Sources, and Fashion datasets*

在 ALOI 和 Caltech-5V 上，RAV 略逊于 MVCAN。ALOI 上 RAV 的 ACC/NMI/PUR 分别为 0.826/0.912/0.830，MVCAN 为 0.849/0.929/0.864；Caltech-5V 上 RAV 为 0.901/0.839/0.901，MVCAN 为 0.919/0.856/0.919。这一差距的可能原因在于：ALOI 包含 100 个类别，簇间边界模糊，关系对齐提供的邻域结构可能引入跨簇混淆；Caltech-5V 的视图数较多（5 个），Wasserstein 距离导出的自适应权重在视图差异度量上的精度可能受限于高维特征空间的分布估计质量。此分析需结合 MVCAN 的具体设计进行进一步验证。

### 消融实验

**损失组件消融。** Table 5 报告了在 Caltech-5V、NUSWIDE、ALOI 和 3Sources 上逐步移除各损失项的消融结果。完整模型（$\mathcal{L}_{REC} + \mathcal{L}_Q + \mathcal{L}_S$）在所有数据集上性能最优。移除关系对齐损失 $\mathcal{L}_S$ 后，Caltech-5V 的 ACC 从 0.901 降至 0.899，降幅较小，表明该数据集上视图间邻域结构本身已较为一致。移除标签对比损失 $\mathcal{L}_Q$ 则导致 Caltech-5V 的 ACC 骤降至 0.424，NMI 降至 0.309，说明标签对比学习模块对语义对齐起到决定性作用。单独使用 $\mathcal{L}_Q$（不加入 $\mathcal{L}_S$）时，ALOI 上 ACC 为 0.806，比完整模型低 2 个百分点，验证了关系对齐对标签对比学习的辅助作用——稳定的邻域结构有助于更准确地度量视图差异。

![[assets/figures/papers/iclr26_0009_uRA9cT4MK6_Relationship_Alignment_for_View-aware_Multi-view/figures/018_Table_5.jpg]]
*Table 5: Ablation studies on different loss components on the Caltech-5V, NUSWIDE, ALOI, and 3Sources datasets*

**自适应加权机制消融。** Table 6 比较了有无视感知自适应加权机制（W）的性能差异。引入该机制后，NGs 的 ACC 从 0.966 提升至 0.980（+1.4%），ALOI 从 0.801 提升至 0.826（+2.5%），Cora 从 0.585 提升至 0.592（+0.7%）。增益在视图差异较大的数据集（如 ALOI 的 4 个异构视图）上更为显著，证实了基于 Wasserstein 距离的自适应权重能有效抑制低相似度视图对的负面影响。

![[assets/figures/papers/iclr26_0009_uRA9cT4MK6_Relationship_Alignment_for_View-aware_Multi-view/figures/019_Table_6.jpg]]
*Table 6: Ablation study on the view-aware adaptive weighting mechanism for NGs, Digit-Product, ALOI and Cora datasets*

### 参数敏感性

Figure 2 展示了 $\lambda_1$（标签对比损失权重）和 $\lambda_2$（关系对齐损失权重）在 NUSWIDE、Caltech-5V、NoisyMNIST 和 3Sources 上的敏感性分析。在较宽的参数范围内（$\lambda_1 \in [10^{-3}, 10^2]$，$\lambda_2 \in [10^{-3}, 10^1]$），聚类性能仅呈现小幅波动，表明模型对超参数选择不敏感，具备良好的训练稳定性。

### 收敛性与特征可视化

Figure 3 的收敛曲线显示，在 Caltech-5V、Digit-Product、NGs 和 NoisyMNIST 上，总损失随训练 epoch 增加而平稳下降，ACC 和 NMI 同步上升并在约 150 epoch 后趋于稳定，验证了联合优化目标的有效收敛性。

Figure 4 展示了 Digit-Product 上全局特征 $\mathbf{Z}$ 在训练过程中的 t-SNE 可视化。Epoch 0 时各类别特征高度混杂；至 Epoch 200 时，同簇特征紧密聚集、异簇特征高度分离。该结果表明，关系对齐提供的稳定邻域结构使全局特征在训练中逐步形成清晰的聚类结构，与定量结果相互印证。

### 失败模式与局限

当前方法存在以下已知局限：第一，对不完整视图和噪声数据的鲁棒性尚未验证，实际部署中可能面临视图缺失或特征扰动场景；第二，关系结构依赖高斯核相似度度量，缺乏对最优相似性度量的理论分析；第三，在类别数极多（如 ALOI 的 100 类）且视图差异度量精度受限时，性能可能被 MVCAN 超越。这些局限需在实际应用中审慎评估。

## 方法谱系与知识库定位

### 与现有基线的结构性差异

RAV 与当前多视图聚类前沿方法的核心差异体现在两个维度：**邻域结构保持**与**视图差异感知**。

**MFLVC** 作为代表性多级特征对比学习方法，通过实例级和聚类级对比学习实现多视图一致性，但其对比损失对所有视图对赋予相等权重，忽视了视图间固有相似度差异带来的表示退化风险。**MVCAN** 引入了注意力机制聚合视图特征，但在跨视图样本关系建模上缺乏显式约束。**DFL-NET** 专注于解耦特征学习，**SEM** 则依赖自监督语义软标签，两者均未对视图间邻域结构一致性进行显式建模。

RAV 的关键突破在于识别并填补了这一空白：通过全局-局部关系对齐（$L_S$）构建了跨视图的样本邻域结构约束，使各视图的局部关系矩阵与全局关系矩阵保持一致。在此基础上，基于 Wasserstein 距离的自适应加权机制（$L_Q$）利用关系对齐提供的稳定邻域结构，更准确地度量视图间相似度，从而动态调制标签对比学习的强度。这一"先对齐结构，再度量差异，后加权对比"的级联设计，是 RAV 区别于所有基线方法的根本特征。

消融实验直接验证了这一差异的重要性：在 Caltech-5V 数据集上，去除关系对齐损失 $L_S$ 后 ACC 仅从 0.901 降至 0.899，表明视图自适应加权机制可部分弥补结构约束的缺失；但去除标签对比损失 $L_Q$ 后 ACC 骤降至 0.424，说明在失去语义对齐能力后，仅靠关系对齐无法完成聚类任务。两者协同工作才能达到最优性能。

### 适用边界与局限

**适用场景**：RAV 在视图数量适中（2-5 个）、视图间存在互补信息且样本量从数百到数万规模的数据集上表现突出。在 NGs（3 视图，500 样本）、YoutubeVideo（4 视图，101,499 样本）、Cora（4 视图，2,708 样本）等差异较大的数据集上均取得最优或接近最优结果，表明方法对不同数据规模具有较好的适应性。

**性能边界**：RAV 并非在所有场景下均占优。在 ALOI（4 视图，100 类）和 Caltech-5V（5 视图，7 类）上，RAV 略低于 MVCAN（ALOI ACC 0.826 vs 0.849，Caltech-5V ACC 0.901 vs 0.919）。这可能表明当视图间差异较小或类别数较多时，基于注意力机制的视图聚合策略（MVCAN）比基于对比学习的语义对齐策略更具优势。此点需结合具体数据集特征进一步验证。

**已知局限**：论文明确指出的局限包括两方面。其一，当前方法对不完整视图（部分视图缺失）和噪声数据的鲁棒性尚未验证，这限制了方法在真实世界数据采集不完善场景下的直接应用。其二，关系结构的构建和视图相似性度量缺乏理论支撑——高斯核带宽 $\sigma$ 固定为 1.0，Wasserstein 距离作为视图差异度量的最优性未得到理论证明。

### 开放问题与后续方向

论文提出的开放问题指向三个方向：

1. **理论深化**：探索理论上更鲁棒的关系结构（替代高斯核相似度）和通用的视图相似性度量（替代 Wasserstein 距离）。当前关系对齐损失 $L_S$ 和自适应权重 $w_{(v,u)}$ 均依赖启发式设计，其理论性质（如收敛性保证、最优性条件）有待建立。

2. **场景扩展**：将方法扩展到不完整视图和噪声数据等复杂实际场景。这涉及对缺失视图的插补策略、噪声鲁棒的关系矩阵构建，以及在此条件下自适应加权机制的有效性保持。

3. **度量的自适应选择**：如何自动确定最优的视图权重度量方式？当前 Wasserstein 距离是固定选择，但在不同数据集上可能存在更优的差异度量（如最大均值差异 MMD、互信息等），自动选择或学习该度量是一个开放问题。

这些方向共同指向一个核心挑战：在保持 RAV 现有"关系对齐-差异度量-加权对比"框架优势的前提下，提升其理论完备性和实际部署鲁棒性。

## 原文 PDF

![[paperPDFs/ICLR_2026/Relationship_Alignment_for_View_aware_Multi_view_Clustering.pdf]]
