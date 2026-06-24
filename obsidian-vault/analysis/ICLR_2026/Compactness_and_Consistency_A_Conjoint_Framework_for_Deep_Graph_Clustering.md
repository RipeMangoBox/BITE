---
title: "Compactness and Consistency: A Conjoint Framework for Deep Graph Clustering"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Compactness_and_Consistency_A_Conjoint_Framework_for_Deep_Graph_Clustering.pdf
aliases:
- CCCFDGC
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "通过图扩散矩阵获得全局视图，引入低秩紧凑嵌入以消除冗余噪声，并利用跨视图一致性学习强制局部与全局表示的对齐。"
primary_logic: "从局部邻接和全局PageRank扩散两个视图提取特征后，利用共享的高斯混合模型子空间对两视图表示进行低秩重建，去除噪声和冗余；同时，通过最小化两视图相似度分布的对称KL散度实现知识传递，获得紧凑、语义丰富且对噪声鲁棒的节点表示，显著提升聚类效果。"
claims:
- "在五个基准数据集上，CoCo在ACC/NMI/ARI/F1等多个指标上均达到最优或次优，例如在Cora上ACC为79.36%。"
- "紧凑性学习（低秩映射）能持续提升性能，移除紧凑性学习（模型变体M5）后各项指标明显下降。"
- "一致性损失（对称KL散度）在所有数据集上均优于MSE和InfoNCE损失，例如Cora上ACC相对MSE提升1.52个百分点。"
- "低秩重建在属性噪声、边噪声和混合噪声设置下均使模型获得更高的准确率，体现出其对噪声的鲁棒性。"
---

# Compactness and Consistency: A Conjoint Framework for Deep Graph Clustering

> [!tip] 核心洞察
> 从局部邻接和全局PageRank扩散两个视图提取特征后，利用共享的高斯混合模型子空间对两视图表示进行低秩重建，去除噪声和冗余；同时，通过最小化两视图相似度分布的对称KL散度实现知识传递，获得紧凑、语义丰富且对噪声鲁棒的节点表示，显著提升聚类效果。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 紧凑性与一致性：深度图聚类的联合框架 |
| 英文题名 | Compactness and Consistency: A Conjoint Framework for Deep Graph Clustering |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=9jdQLmPUHW); [GitHub](https://github.com/juweipku/CoCo) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | CoCo |
| Dataset | Cora, AMAP, BAT |

> [!tip] 效果简介
> - Cora 上，ACC 为 79.36±0.69，对比 MAGI 76.21±0.50，变化 +3.15。
> - Cora 上，NMI 为 60.71±0.59，对比 MAGI 59.84±0.43，变化 +0.87。
> - AMAP 上，ACC 为 79.27±0.70，对比 CCGC 77.25±0.41，变化 +2.02。

## 概述

基于GNN的图聚类方法受限于局部消息传递，难以捕获节点间的全局依赖关系；同时，图数据固有的冗余与噪声使节点表示缺乏紧凑性和鲁棒性，制约聚类性能。针对上述瓶颈，本文提出**CoCo**（**Co**mpactness and **Co**nsistency），一个联合紧凑性学习与跨视图一致性学习的深度图聚类框架。其核心思路为：从标准邻接矩阵和个性化PageRank扩散矩阵分别构建局部与全局视图，通过解耦的图卷积滤波器与MLP编码器提取两视图特征；随后利用共享GMM子空间对拼接嵌入进行低秩重建，得到去除噪声和冗余的紧凑表示；再以锚点相似度分布的对称KL散度对齐局部与全局视图的知识，实现跨视图一致性学习；最终平均两视图的紧凑嵌入并执行K-means获得聚类结果。

该方法在五个基准数据集上展现出显著优势：CoCo在ACC、NMI、ARI、F1等指标上均达到最优或次优水平，明显超越现有GNN聚类和深度聚类基线。消除紧凑性学习或一致性损失的消融实验证实了各模块的必要性；在属性噪声、边噪声及混合噪声设置下，CoCo仍保持较高准确率，体现出良好的鲁棒性。上述结果验证了“双视图+低秩紧凑性+一致性对齐”这一联合范式对提升图聚类质量的有效性，并为后续图表示学习与聚类方法的设计提供了新的视角。

## 背景与动机

图聚类旨在以无监督方式将节点聚合成内聚性子图，在社交网络分析、推荐系统、生物信息学等领域具有广泛应用。随着图神经网络（GNN）的发展，大量深度图聚类方法（如基于自编码器的 SDCN、基于对比学习的 MAGI 与 GraphLearner 等）被提出，它们通过将局部邻接关系编码到节点表示中，显著超越了传统方法。然而，这些方法面临两个根本性瓶颈：

**局部感受野限制**：GNN 的消息传递机制天然偏向节点的直接邻居，导致模型难以捕获远距离节点间的依赖关系。图聚类中的社区结构往往由非直接相连但语义相似的节点构成，纯粹的局部编码会丧失对全局结构的感知，使簇分配缺乏宏观一致性。

**冗余与噪声干扰**：真实图数据（尤其是属性图）包含大量与聚类无关的冗余特征和噪声（如属性噪声、边噪声）。多数现有方法直接对原始特征进行变换，未显式压缩冗余或抑制噪声，导致节点嵌入不紧凑、聚类边界模糊，鲁棒性严重不足。即使表现较好的方法（如 MAGI、GraphLearner），其嵌入在高噪声场景下仍会出现显著的性能退化。

上述问题交互叠加：局部表示因感受野不足而丢失的全局信息，无法通过含有噪声和冗余的高维特征来弥补；同时，噪声破坏了跨节点的相似度度量，进一步放大了局部与全局视角之间的不一致。

为此，本文提出 **CoCo（Compactness and Consistency）** 联合框架，其设计动机是：

- **引入全局视图**：通过个性化 PageRank 扩散矩阵建模节点间的长程依赖，赋予模型全局感受野，从根本上弥补局部邻接的视野缺失。
- **学习紧凑表示**：利用低秩子空间学习对节点嵌入进行重建，主动消除冗余特征和噪声成分，使簇结构在低维空间中更清晰、更鲁棒。
- **强制跨视图一致性**：设计对称 KL 散度对齐局部视图与全局视图的锚点相似度分布，使两个视角的信息相互增强、语义对齐，从而充分利用互补特征。

综上，CoCo 通过协同解决“全局缺失”与“噪声冗余”两个瓶颈，旨在得到紧凑、鉴别力强且对噪声鲁棒的节点表示，从而在无需标签的前提下显著提升图聚类性能。

## 核心创新

现有基于GNN的深度图聚类方法面临两个紧密相关的瓶颈：**局部消息传递机制难以捕获节点间的全局依赖**；同时，图数据中固有的属性冗余和结构噪声使得节点表示缺乏紧凑性，直接削弱聚类性能。CoCo 以“双视图全局扩散 → 低秩紧凑嵌入 → 跨视图一致性学习”的联合设计，系统地破解这一困局。其相对于强基线（如 MAGI、GraphLearner、Dink‑Net 等）的关键创新，集中体现在四个 **changed slots** 及其因果关联。

### 2.1 局部‑全局双视图特征提取（槽位：Graph views for encoding）
基线普遍仅基于归一化邻接矩阵进行特征传播，编码范围局限于局部邻域。CoCo 同时引入 **个性化 PageRank 扩散矩阵** 
$$\mathbf{S} = \alpha ( \mathbf{I}_N - (1 - \alpha) \tilde{\mathbf{A}} )^{-1}$$
作为全局视图，有效捕捉长程依赖。局部与全局视图采用 **解耦的图卷积架构**：先用广义拉普拉斯平滑滤波去除高频噪声并融合属性与结构（Eq. 1），再经由独立 MLP 编码为可训练表示（Eq. 2），彻底替代传统的端到端纠缠式 GCN。这一解耦设计在不同层数下均使性能更稳定、更高（见图 7，附录 J）。实验上，仅依靠局部视图的 SDCN 在 Cora 上 ACC 为 69.69%，而 CoCo 借助双视图达到 79.36%（Table 1），提升幅度非常显著；消融实验也直接印证双视图的有效性。

### 2.2 基于 GMM 的低秩紧凑性学习（槽位：Redundancy elimination）
多数基线缺乏显式的去冗余机制，导致表示空间被噪声维度污染。CoCo 创新性地将局部与全局嵌入拼接后，输入 **共享的高斯混合模型（GMM）**，通过 EM 算法学习一个 K 维低秩子空间，并对嵌入进行 **低秩重构**（Eq. 4）
$$\hat{z}_{ij} = \sum_{k=1}^{K} \hat{\lambda}_{ik} \hat{\gamma}(y_{jk})$$
该重构剔除冗余与噪声，仅保留数据的主要变异方向。定理 2（附录 B.3）从理论上保证其保持个体信息守恒且最大化总变异。引入的 **残差连接**（Eq. 5）则确保紧凑嵌入不会丢失局部细节并保持梯度流畅通。因果证据十分明确：移除整个紧凑性模块（模型变体 M5）后，所有聚类指标均显著下降（Figure 2）；在属性噪声、边噪声和混合噪声设置下，低秩重建使 CoCo 准确率始终最高（Table 3），充分展现其去冗余带来的鲁棒性提升。

### 2.3 对称 KL 驱动的跨视图一致性学习（槽位：Cross‑view interaction）
以往方法对多视图信息或简单拼接，或采用未对齐的对比损失，难以实现互补知识的有效传递。CoCo 通过构造锚点集，计算两视图下节点‑锚点的相似度分布 $\mathbf{p}^i$ 与 $\mathbf{q}^i$，并以 **对称 KL 散度**
$$\mathcal{L} = \frac{1}{2N} \sum_{i=1}^{N} \left( \mathrm{KL}(\mathbf{p}^i || \mathbf{q}^i) + \mathrm{KL}(\mathbf{q}^i || \mathbf{p}^i) \right)$$
强制分布对齐，实现跨视图的知识传递。对称 KL 能够容忍视图间的分布差异并避免塌缩，优于传统 MSE 和 InfoNCE（Table 2）：在 Cora 上 ACC 相较 MSE 提升 1.52 个百分点；在所有测试数据集上，该损失一致带来 ACC、NMI、ARI、F1 的全面改进。一致性损失与紧凑性学习形成闭环：低秩嵌入先去除噪声，一致性学习再对齐语义，最终使融合后的表示 $\mathbf{Z}^{\mathrm{F}}$（Eq. 7）兼具全局趋势与局部细节，直接支撑聚类性能。

### 2.4 槽位变更的协同效应与边界
上述 three changed slots 并非独立：双视图提供互补信息源，低秩紧凑性从表示空间剔除冗余，一致性学习则充当跨视图的知识传输纽带。三者协同产生的增益在五个基准数据集上得到系统验证，CoCo 在 ACC、NMI、ARI、F1 四项指标上经常占据最优或次优（Table 1），尤其对噪声和异配图的鲁棒性远超同类方法（Table 3、Table 4）。然而，该方法仍需 **预先指定聚类数 K**，低秩子空间维度和锚点数量也依赖人工调节，缺乏自动推断机制；当前实验尚未覆盖百万级节点的大规模图与动态图，其可扩展性有待进一步验证。这些限制指向下一个创新方向：自动确定 K 和子空间参数，并将框架推广至时间图、异质图乃至单细胞基因组学聚类等场景。

## 整体框架

![[assets/figures/papers/iclr26_0015_9jdQLmPUHW_Compactness_and_Consistency_A_Conjoint_Framework/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the proposed framework CoCo*

CoCo 框架旨在解决深度图聚类中两个核心瓶颈：局部消息传递机制难以捕获全局节点依赖，以及属性与拓扑结构中的冗余噪声导致表示缺乏紧凑性和鲁棒性。其设计思路是构造局部与全局双视图，通过低秩子空间学习消除冗余并提取紧凑表示，再利用跨视图一致性学习融合互补知识，最终得到兼具区分性与鲁棒性的节点嵌入用于聚类。图 1 展示了整体架构。

整个流水线以原始属性图（邻接矩阵 $\mathbf{A}$，节点特征 $\mathbf{X}$）为输入，依次经过以下关键模块：

1. **双视图特征提取**  
   局部视图基于对称归一化邻接矩阵 $\tilde{\mathbf{A}}$；全局视图则采用个性化 PageRank 扩散矩阵 $\mathbf{S} = \alpha (\mathbf{I}_N - (1 - \alpha) \tilde{\mathbf{A}})^{-1}$，以捕捉长程依赖。两种视图各自经过解耦的广义拉普拉斯平滑滤波（式 1）和独立 MLP（式 2），分别输出局部嵌入 $\mathbf{Z}^{\mathrm{l}}$ 和全局嵌入 $\mathbf{Z}^{\mathrm{g}}$。这一设计使得滤波与特征变换分离，避免了传统 GCN 的深层性能衰退（附录 J）。

2. **紧凑性学习（低秩子空间重建）**  
   将 $\mathbf{Z}^{\mathrm{l}}$ 和 $\mathbf{Z}^{\mathrm{g}}$ 纵向拼接后，送入一个共享的 GMM。通过 EM 算法迭代更新子空间基底 $\lambda_{ik}$ 与聚类后验概率 $\gamma(y_{jk})$（式 3），进而将原始嵌入投影到 $K$ 维子空间进行重构：$\hat{z}_{ij} = \sum_{k=1}^K \hat{\lambda}_{ik} \hat{\gamma}(y_{jk})$（式 4），得到低秩紧凑嵌入 $\hat{\mathbf{Z}}$。该过程在保持个体信息与总变异的前提下最大程度地消除噪声和冗余（定理 2）。消融实验（图 2）表明，移除紧凑性学习模块后，各项聚类指标大幅下降，证实了该模块的必要性。

3. **残差连接**  
   为避免低秩重建丢失局部细节，CoCo 将重构嵌入与原始嵌入相加：$\tilde{\mathbf{Z}} = \hat{\mathbf{Z}} + \mathbf{Z}$（式 5），以此维持梯度流动并混合局部与全局尺度信息。

4. **跨视图一致性学习**  
   通过一个锚点集合计算节点在两个视图下的相似度分布 $\mathbf{p}^i$ 和 $\mathbf{q}^i$，并以对称 KL 散度作为损失函数：$\mathcal{L} = \frac{1}{2N} \sum_{i=1}^N (\mathrm{KL}(\mathbf{p}^i || \mathbf{q}^i) + \mathrm{KL}(\mathbf{q}^i || \mathbf{p}^i))$（式 6）。该损失强制局部与全局视图的相互对齐，实现知识传递。对比实验（表 2）显示，对称 KL 散度在所有数据集上均优于 MSE 和 InfoNCE 损失，带来了更丰富的语义表示和更强的噪声鲁棒性。

5. **融合与聚类**  
   训练完成后，对局部和全局视图的紧凑嵌入取平均，得到最终融合表示 $\mathbf{Z}^{\mathrm{F}} = (\tilde{\mathbf{Z}}^{\mathrm{l}} + \tilde{\mathbf{Z}}^{\mathrm{g}}) / 2$（式 7），再输入 K-means 输出聚类结果。融合表示同时继承了局部邻域细节与全局长程信息，且经过低秩去噪和一致性对齐，从而显著提升聚类性能。

## 核心模块与公式推导

CoCo 框架由局部与全局双视图特征提取、紧凑性学习（低秩子空间重建）、残差连接、跨视图一致性对齐以及最终融合聚类四个核心阶段构成。下面依次阐述各模块的数学形式与变量含义。

### 2.1 局部与全局视图特征提取

首先定义带自环的归一化邻接矩阵

$$\tilde{\mathbf{A}} = \hat{\mathbf{D}}^{-1/2} \hat{\mathbf{A}} \hat{\mathbf{D}}^{-1/2},\quad \hat{\mathbf{A}} = \mathbf{A} + \mathbf{I}_N,$$

其中 $\mathbf{A}$ 为原始邻接矩阵，$\hat{\mathbf{D}}$ 为 $\hat{\mathbf{A}}$ 的度矩阵，$\mathbf{I}_N$ 为 $N$ 阶单位阵。

**全局视图** 由个性化 PageRank 图扩散矩阵给出，用于捕获节点间的长程依赖：

$$\mathbf{S} = \alpha \big( \mathbf{I}_N - (1 - \alpha) \tilde{\mathbf{A}} \big)^{-1}.$$

$\alpha \in (0,1]$ 为 teleport 概率，$\mathbf{S}$ 编码了节点在全局拓扑中的扩散关系。

**特征滤波**：对原始属性矩阵 $\mathbf{X}$，分别构造局部拉普拉斯矩阵 $\tilde{\mathbf{L}}^{\mathrm{l}} = \mathbf{I}_N - \tilde{\mathbf{A}}$ 和全局拉普拉斯矩阵 $\tilde{\mathbf{L}}^{\mathrm{g}} = \mathbf{I}_N - \mathbf{S}$，利用广义拉普拉斯平滑去除高频噪声：

$$
\tilde{\mathbf{X}}^{\mathrm{l}} = \big( \mathbf{I}_N - \tilde{\mathbf{L}}^{\mathrm{l}} / k^{\mathrm{l}} \big)^t \mathbf{X},\qquad
\tilde{\mathbf{X}}^{\mathrm{g}} = \big( \mathbf{I}_N - \tilde{\mathbf{L}}^{\mathrm{g}} / k^{\mathrm{g}} \big)^t \mathbf{X}. \tag{1}
$$

$k^{\mathrm{l}}, k^{\mathrm{g}}$ 分别为对应拉普拉斯矩阵的最大特征值上界，$t$ 为平滑阶数，控制滤波强度。

**非线性编码**：平滑后的特征各自经过独立的 MLP 得到局部与全局的初始嵌入：

$$
\mathbf{Z}^{\mathrm{l}} = \mathrm{MLP}_1(\tilde{\mathbf{X}}^{\mathrm{l}}),\qquad
\mathbf{Z}^{\mathrm{g}} = \mathrm{MLP}_2(\tilde{\mathbf{X}}^{\mathrm{g}}). \tag{2}
$$

### 2.2 紧凑性学习：低秩子空间重建

将两视图嵌入按行拼接，形成联合特征矩阵 $\mathbf{Z} = [\mathbf{Z}^{\mathrm{l}}; \mathbf{Z}^{\mathrm{g}}] \in \mathbb{R}^{N \times 2D}$。为消除冗余与噪声，CoCo 假设每个特征维度 $j$ 由一个潜在变量 $y_{jk}$ 决定其所属的隐藏聚类（共享的高斯混合模型子空间），通过期望最大化（EM）算法迭代优化。

- **E‑step**：计算特征维度 $j$ 属于第 $k$ 个成分的后验概率 $\gamma(y_{jk})$（具体算式略，见原文附录 A）。
- **M‑step**：更新节点 $i$ 在第 $k$ 个基上的表示系数 $\lambda_{ik}$：

$$
\lambda_{ik}^{\mathrm{new}} = \frac{1}{\sum_{j=1}^{2D} \gamma(y_{jk})} \sum_{j=1}^{2D} \gamma(y_{jk}) \, z_{ij}. \tag{3}
$$

收敛后得到子空间系数矩阵 $\boldsymbol{\Lambda} \in \mathbb{R}^{N \times K}$ 和成分分配概率矩阵 $\boldsymbol{\Gamma} \in \mathbb{R}^{2D \times K}$。低秩重建的紧凑嵌入为

$$
\hat{\mathbf{Z}} = \boldsymbol{\Lambda} \boldsymbol{\Gamma}^{\top},\quad \text{即}\quad \hat{z}_{ij} = \sum_{k=1}^{K} \hat{\lambda}_{ik} \hat{\gamma}(y_{jk}). \tag{4}
$$

$K$ 既为混合模型成分数，也是低秩子空间的维度（通常与聚类数一致）。该低秩投影在理论上被证明保持个体信息量的同时最大化总体变异，从而保留判别性结构并滤除噪声（见原文 Theorem 2）。

### 2.3 残差连接

为防止梯度阻断并保留原始局部细节，将重构的紧凑嵌入与初始嵌入相加：

$$
\tilde{\mathbf{Z}} = [\tilde{\mathbf{Z}}^{\mathrm{l}}; \tilde{\mathbf{Z}}^{\mathrm{g}}] = \hat{\mathbf{Z}} + \mathbf{Z}. \tag{5}
$$

$\tilde{\mathbf{Z}}^{\mathrm{l}}, \tilde{\mathbf{Z}}^{\mathrm{g}}$ 分别为局部与全局视图的残差增强表示，供后续一致性学习与聚类使用。

### 2.4 跨视图一致性学习

从两视图的紧凑表示中分别计算节点 $i$ 与一组锚点（取自记忆库）的相似度分布 $\mathbf{p}^i$（局部视图）和 $\mathbf{q}^i$（全局视图）。CoCo 采用对称 KL 散度强制两视图分布对齐，实现知识迁移：

$$
\mathcal{L} = \frac{1}{2N} \sum_{i=1}^{N} \Big( \mathrm{KL}(\mathbf{p}^i \,\|\, \mathbf{q}^i) + \mathrm{KL}(\mathbf{q}^i \,\|\, \mathbf{p}^i) \Big). \tag{6}
$$

该损失使模型在训练过程中学得视图一致、语义鲁棒的节点表示。

### 2.5 融合与聚类

最终，将两视图残差嵌入进行平均得到统一表示，并输入 $K$‑means 完成聚类：

$$
\mathbf{Z}^{\mathrm{F}} = \frac{\tilde{\mathbf{Z}}^{\mathrm{l}} + \tilde{\mathbf{Z}}^{\mathrm{g}}}{2}. \tag{7}
$$

整个框架在优化损失 $\mathcal{L}$ 的过程中同时实现了紧凑特征学习与跨视图一致性对齐，直接输出高质量的聚类结果。

## 实验与分析

**瓶颈与因果验证**  
CoCo 针对基于局部消息传递的 GNN 图聚类方法难以捕获全局依赖、且节点表示易受冗余与噪声影响这两个核心瓶颈，通过三项机制联合提升聚类质量：  
（1）引入个性化 PageRank 扩散矩阵 $\mathbf{S}$ 提取全局视图，弥补局部邻接 $\tilde{\mathbf{A}}$ 的长程依赖缺失；  
（2）在局部与全局双视图编码后，利用共享高斯混合模型（GMM）的 EM 算法将拼接表示投影至低秩子空间，并重构紧凑嵌入 $ \hat{\mathbf{Z}} $，去除属性冗余与噪声；  
（3）以锚点相似度分布的对称 KL 散度作为一致性损失 $ \mathcal{L} $，强制局部与全局视图的分布对齐，实现知识互传。  
接下来的实验围绕这三个因果 knob 展开，系统验证其独立与联合效用。

### 1. 主聚类结果  
在 Cora、AMAP、BAT、EAT、UAT 五个公开基准上，CoCo 与 10 种基线（包括 SDCN、MAGI、GraphLearner、Dink‑Net、RGC 等）全面比较 ACC、NMI、ARI、F1。Table 1 显示，CoCo 在绝大多数数据集上取得最优或次优成绩，且提升幅度显著：  
- **Cora**：ACC 79.36%±0.69，较第二名 MAGI（76.21%）提升 3.15 个百分点；NMI 60.71%±0.59，ARI 58.76%±1.47，F1 亦有类似优势。  
- **AMAP**：ACC 79.27%±0.70，较 CCGC（77.25%）高出 2.02 个百分点。  
- **BAT**：ACC 78.85%±0.91，较 GraphLearner（75.50%）提升 3.35 个百分点；NMI 相对提升更达 8.74 个百分点。  
- **UAT**：ACC 59.68%±0.36，仍以约 2.15 个百分点的优势领先最强基线。  
所有对比方法采用相同的数据划分与评估协议，结果均附带标准差，保证了比较的公平性。

![[assets/figures/papers/iclr26_0015_9jdQLmPUHW_Compactness_and_Consistency_A_Conjoint_Framework/figures/002_Table_1.jpg]]
*Table 1: Clustering performance on five benchmark datasets (mean ± standard deviation). The top two results for each method are marked in bold and underline, respectively*

### 2. 消融实验  
**（1）紧凑性学习的贡献**  
Figure 2 展示了不同变体的消融结果。移除紧凑性学习模块（即去掉低秩重建与残差连接，变体 M5）后，所有数据集上的 ACC、NMI、ARI、F1 均出现明显下降，证明低秩子空间重建是性能的关键支撑。进一步比较 M3（原始嵌入 + 低秩）与 M1（仅原始嵌入），以及 M4 与 M2，均显示引入低秩映射后性能稳定提升，表明紧凑性学习能有效消除冗余、提取判别性结构。

![[assets/figures/papers/iclr26_0015_9jdQLmPUHW_Compactness_and_Consistency_A_Conjoint_Framework/figures/006_Figure_2.jpg]]
*Figure 2: The ablation experimental results*

**（2）一致性损失的选择**  
Table 2 对比了对称 KL 散度（一致性损失）、MSE 和 InfoNCE 三种跨视图交互损失。在 Cora、AMAP、UAT 三个数据集上，一致性损失一致且显著地优于替代方案：例如 Cora 上 ACC 达到 79.36%（一致性），而 MSE 为 77.84%（提升 1.52 个百分点），InfoNCE 仅 75.57%。对称 KL 散度不仅在准确率上领先，在 NMI、ARI 和 F1 上也保持优势，说明其能更有效地对齐局部与全局视图的分布，促进语义一致的知识传递。

![[assets/figures/papers/iclr26_0015_9jdQLmPUHW_Compactness_and_Consistency_A_Conjoint_Framework/figures/007_Table_2.jpg]]

**（3）解耦架构的优势**  
附录 J 中的 Figure 7 比较了 GCF+MLP（解耦滤波加独立 MLP）与端到端 GCN 在不同层数下的表现。GCF+MLP 在层数增加时性能下降更缓、绝对精度更高，表明去纠缠的图卷积滤波能够减轻过平滑，增强模型鲁棒性。

**（4）EM 迭代次数与效率**  
Table 6 展示了 EM 算法迭代次数（1–30）对 NMI 的影响。在 Cora 和 AMAP 上，NMI 在 10 次迭代后已接近饱和，继续增加迭代几乎没有额外收益；而 EM 过程的耗时仅占整体训练时间的约 4%，体现了极低的计算开销与高效率。

### 3. 鲁棒性分析  
为验证紧凑性学习的去噪能力，Table 3 在 BAT 数据集上注入了三种类型的噪声：属性噪声（随机掩盖 30% 属性）、边噪声（随机删减 30% 边）以及混合噪声（属性+边）。CoCo 在所有噪声设置下均取得最高 ACC，尤其在属性噪声下领先第二名约 11.60 个百分点。该结果表明，低秩重建能够压制属性与结构中的随机扰动，结合一致性学习提供的跨视图语义互补，使模型对噪声高度鲁棒。

![[assets/figures/papers/iclr26_0015_9jdQLmPUHW_Compactness_and_Consistency_A_Conjoint_Framework/figures/016_Table_3.jpg]]
*Table 3: Comparison of accuracy on noisy BAT*

### 4. 异配图与同配图的扩展  
Table 4 报告了在异配图 Cornell 和 Wisconsin 上的聚类结果。CoCo 在 ACC 上优于 GraphLearner 和 MAGI，但在 NMI 上 GraphLearner 仍占优，说明方法在异配场景下对部分指标提升有限，存在改进空间。  
此外，Table 5 给出了与专门同配图方法 DGCN 的对比，CoCo 在 Cora 和 AMAP 上的 ACC 与 NMI 均领先约 5–7 个百分点，显示出在同配图上明显的性能优势。

### 5. 可视化与图表结论  
Figure 3 展示了 CoCo 与若干强基线在 Cora 和 AMAP 上的 t‑SNE 投影。CoCo 形成的簇内聚度更高、类间边界更清晰，直观反映了紧凑性与一致性学习共同作用下的判别表示质量。综合图表可得出以下核心结论：  
- **Table 1** 确立了 CoCo 在多数据集上的整体领先地位；  
- **Figure 2** 与 **Table 2** 分别证明了紧凑性模块和对称 KL 散度损失的关键性；  
- **Table 3** 证实了低秩重建赋予的强抗噪能力；  
- **Figure 3** 提供了表示质量的定性佐证。

![[assets/figures/papers/iclr26_0015_9jdQLmPUHW_Compactness_and_Consistency_A_Conjoint_Framework/figures/008_Figure_3.jpg]]
*Figure 3: The t-SNE results comparing our CoCo with competitive baselines on two datasets. The first row and second row correspond to Cora and AMAP, respectively*

### 6. 失败模式与局限  
尽管 CoCo 表现突出，仍然存在若干限制：  
- 聚类数目 $K$ 以及低秩子空间维度 $K$ 均需事先指定，缺乏自动推断机制；  
- 锚点数量 $M$ 仅通过实验调参确定，尚无理论指导其最优选择；  
- 实际扩展性仅通过复杂度分析示意，未在百万级节点规模图上进行验证；  
- 模型设计主要面向属性图，对纯拓扑图或动态图聚类未做专门适配；  
- 在异配图上，部分指标（如 NMI）的提升幅度较小，对高度异配环境的适应性仍需加强。  
这些局限指出了未来可探索的方向，如自动推断聚类数、理论指导锚点选择以及在大规模动态图上的落地应用。

## 方法谱系与知识库定位

本方法在深度图聚类的研究链条中处于从局部结构信息引入到全局依赖建模与去冗余表示的转折点。早期的代表性工作 SDCN 率先将图结构信息通过自编码器框架融入深度聚类，克服了仅依赖节点属性的局限，但其使用的是原始邻接矩阵，感知范围受限于局部消息传递机制，难以捕获长程的节点关系。随后的 MAGI 和 GraphLearner 等以对比学习为核心的方法，分别通过模块度最大化和结构学习来强化图结构信息，但它们仍以邻接矩阵为主要输入，缺乏显式的全局视图，且未针对图数据内在的冗余与噪声进行系统化处理。Dink‑Net 和 RGC 分别从可扩展架构和强化学习自动确定聚类数量等角度扩展了图聚类的设计空间，但同样未将紧凑性作为学习目标（分析依据： baseline_methods 与 changed_slots 的对比）。

CoCo 相对于上述基线的关键变化体现在四个互相关联的设计维度上：
1. **局部‑全局双视图编码**：基线方法仅依赖局部邻接矩阵，而 CoCo 同时使用归一化邻接矩阵和基于个性化 PageRank 的图扩散矩阵 $\mathbf{S}$，以相对稠密的全局视图捕获节点间的长程依赖，弥补局部消息传递的固有局限。
2. **基于 GMM 的低秩紧凑学习**：基线方法没有明确的冗余消除机制；CoCo 则引入共享的高斯混合模型，在拼接的双视图表示上执行 EM 迭代，学得低秩子空间并重构紧凑嵌入（式 3–4）。这一设计通过定理 2 保证个体信息守恒和总变异最大化，从理论上支撑了去噪与去冗余的能力。
3. **跨视图一致性学习**：不同于简单的特征融合或常用的一致性损失（MSE、InfoNCE），CoCo 通过锚点相似度分布的对称 KL 散度（式 6）强制局部视图与全局视图在语义分布上对齐，实现知识迁移。实验表明，该损失在 Cora、AMAP、UAT 上一致优于 MSE 和 InfoNCE，其中 Cora ACC 相对 MSE 提升 1.52 个百分点（Table 2）。
4. **解耦的卷积滤波设计**：将图卷积滤波（广义拉普拉斯平滑）与 MLP 编码解耦，替代端到端纠缠的 GCN 层，使得不同层数下性能更稳定且更优（Appendix J, Figure 7），增强了鲁棒性。

这些变化的综合效果在五个基准数据集上得到验证：CoCo 在 ACC/NMI/ARI/F1 上取得最优或次优，例如 Cora ACC 达到 79.36%，高出 runner‑up MAGI 3.15 个百分点（Table 1）。消融实验进一步证实，移除紧凑性学习模块（模型变体 M5）会导致所有指标显著下降，而低秩投影本身（M3 vs M1、M4 vs M2）均能持续提升性能（Figure 2）。噪声鲁棒性实验显示，在属性噪声、边噪声及混合噪声三种设定下，CoCo 的准确率均明显高于 GraphLearner 和 MAGI，尤其在属性噪声下领先幅度达 11.60 个百分点（Table 3）。

**适用边界**：当前 CoCo 面向属性图聚类，实验覆盖 Cora、AMAP、BAT、EAT、UAT 等中规模同配图以及 Cornell、Wisconsin 等异配图，且在噪声场景下表现稳健。但模型假设聚类数 K 和低秩子空间维度需预先指定，且锚点数 M 通过实验确定而无理论指导。在异配图上，部分指标提升幅度较小（如 Wisconsin 的 NMI 仍低于 GraphLearner），说明紧凑性与一致性机制在极低同配性条件下的边际增益有限。此外，复杂度分析仅通过理论示意，缺乏百万级节点规模的实际验证，大规模图上的扩展性仍待检验。该方法也未专门处理纯拓扑图（无属性）或动态图。

**局限与开放问题**：以下问题为本文直接指出或从实验边界中明确推知。需手动指定聚类数 K 和子空间维度，限制了对未知数据的全自动适配。锚点数量 M 的选取缺乏理论指导，其与记忆库多样性及最终性能的关系尚未阐明。此外，作者提出了若干开放方向：探索更优的低秩空间训练方法；将模型扩展至时间图聚类和单细胞基因组学聚类；研究自动推断最优 K 的策略；在更广泛的图类型（异质图、有向图）上验证方法的普适性。这些方向也折射出现有框架的结构假设过强、动态适应性不足等潜在瓶颈。

## 原文 PDF

![[paperPDFs/ICLR_2026/Compactness_and_Consistency_A_Conjoint_Framework_for_Deep_Graph_Clustering.pdf]]
