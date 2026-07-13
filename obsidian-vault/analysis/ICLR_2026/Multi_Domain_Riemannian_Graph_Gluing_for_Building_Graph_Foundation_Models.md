---
title: "Multi-Domain Riemannian Graph Gluing for Building Graph Foundation Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Multi_Domain_Riemannian_Graph_Gluing_for_Building_Graph_Foundation_Models.pdf
project_link: null
code_link: https://github.com/RiemannGraph/GraphGlue
openreview_forum_id: G3uNHQpP7J
aliases:
- MDRGGBGFM
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "通过神经流形胶合理论，将多域图统一到一个光滑的黎曼流形上，并利用度规兼容性、完整性和曲率控制来跟踪和优化知识迁移的几何一致性。"
primary_logic: "将每个图视为局部黎曼流形，通过边的度规传输和三角形完整性条件胶合成全局流形，从而将知识集成与转移转化为几何形变的最小化问题，并据此定义可量化的几何传递度量。"
claims:
- "提出神经流形胶合理论，通过自适应正交帧和(k,M)-稀疏扰动表征局部几何，利用边度规翻译保证全局度量存在，并通过三角形完整性消除胶合偏移。"
- "通过控制体积元变化率（Ricci曲率估计）实现流形光滑，并提出曲率损失函数。"
- "GRAPHGLUE框架在跨域和域内迁移上均超越现有方法，特别是在小样本设定下。"
- "几何传递度量(GTM)与测试损失对齐，证明其能反映迁移难度。"
---

# Multi-Domain Riemannian Graph Gluing for Building Graph Foundation Models

> [!tip] 核心洞察
> 将每个图视为局部黎曼流形，通过边的度规传输和三角形完整性条件胶合成全局流形，从而将知识集成与转移转化为几何形变的最小化问题，并据此定义可量化的几何传递度量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 多域黎曼图胶合以构建图基础模型 |
| 英文题名 | Multi-Domain Riemannian Graph Gluing for Building Graph Foundation Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=G3uNHQpP7J) · [GitHub](https://github.com/RiemannGraph/GraphGlue) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | GRAPHGLUE |
| Dataset | Arxiv (Node Classification, Intra-domain 5-shot), Reddit (Node Classification, Computers (Node Classification, Cross-domain 1-shot) |

> [!tip] 效果简介
> - Arxiv (Node Classification, Intra-domain 5-shot) 上，Accuracy 为 39.98 ± 1.67，对比 GCOPE 39.45 ± 1.23，变化 +0.53。
> - Reddit (Node Classification, Intra-domain 5-shot) 上，Accuracy 为 84.89 ± 0.68，对比 GCOPE 82.12 ± 0.53，变化 +2.77。
> - Computers (Node Classification, Cross-domain 1-shot) 上，Accuracy 为 59.50 ± 7.05，对比 GCOPE 58.24 ± 7.48，变化 +1.26。

## 概要

图基础模型面临的核心瓶颈在于：**多域图预训练缺乏对知识跨域集成和迁移的一致性理论框架**，现有方法多依赖图码本、图元等离散结构进行知识表征，难以在预训练与领域适应之间建立可量化的迁移性评估。这一问题在少样本跨域迁移场景下尤为突出——当目标域图结构与预训练域差异显著时，模型无法有效判断迁移难度，也难以保证知识传递的几何一致性。

本文提出 **GRAPHGLUE**，其核心洞见是将多域图统一到一个光滑的黎曼流形上：将每个图视为局部黎曼流形，通过边的度规传输和三角形完整性条件胶合成全局流形，从而将知识集成与迁移转化为几何形变的最小化问题。具体而言，该方法通过**神经流形胶合理论**，利用自适应正交帧（AOF）学习节点局部黎曼度量，沿边进行等距变换保证度量兼容性（Theorem 4.5），并通过三角形完整性损失消除胶合偏移（Theorem 4.8），最终以曲率损失控制体积元变化率实现流形光滑（Theorem 4.9）。在此统一流形之上，进一步定义了**几何传递度量**（GTM），由完整性分歧和曲率分歧组成，直接量化目标域融入预训练流形所需的几何形变。

实验表明，GRAPHGLUE 在跨域和域内迁移任务上均超越现有方法：在 Computers 数据集上跨域 1-shot 准确率达 **59.50%**（+1.26% vs GCOPE），Reddit 域内 5-shot 准确率达 **84.89%**（+2.77% vs GCOPE）。消融研究证实，曲率损失和完整性损失是性能的关键支撑——去除曲率损失导致 Arxiv 1-shot 准确率从 28.88 降至 22.33。此外，几何传递度量与测试损失高度对齐，验证了其作为迁移难度指标的有效性；几何缩放律实验进一步揭示，更多预训练域能产生更光滑的流形，从而提升迁移性能。

**方法定位**：GRAPHGLUE 属于多域图预训练方法，区别于 PRODIGY、GCOPE 等基于离散结构的基线，它首次将黎曼几何的胶合理论引入图基础模型构建，为知识跨域集成提供了连续几何框架和可量化的迁移性度量。



### 图基础模型的核心瓶颈

图结构数据广泛存在于社交网络、分子化学、知识图谱等不同领域，但各域图在拓扑模式、特征空间和语义标签上存在显著差异。构建能够跨域泛化的图基础模型面临一个根本性瓶颈：**缺乏对知识跨域集成和迁移的一致理论框架**。现有方法通常将不同域的图视为独立样本，通过离散结构（如图码本、图元、计算树）进行拼接或对齐，但无法在连续几何空间中统一刻画域间知识的传递路径与迁移代价，导致预训练与领域适应之间的迁移性评估缺乏可量化的理论支撑。

### 现有方法的局限

当前多域图预训练方法可大致分为两类。一类以 **GCC**、**DGI**、**GraphMAE** 等自监督方法为代表，它们虽能在单域内学习有效表示，但跨域迁移时缺乏对域间结构差异的显式建模。另一类以 **PRODIGY**、**GFT**、**RAGraph**、**SAMGPT**、**GCOPE**、**MDGFM** 等多域预训练方法为代表，它们试图通过图原型匹配、元学习或提示微调来桥接不同域，但仍存在两个关键缺陷：

1. **知识集成方式离散化**：这些方法依赖图码本、原型向量或计算树等离散结构来组织多域知识，无法捕捉域间知识的连续几何关系，也难以保证知识集成的全局一致性。
2. **迁移难度不可量化**：现有方法仅通过特征相似度或任务性能间接评估迁移效果，缺乏直接量化目标域融入预训练知识体系所需“形变代价”的度量工具。这导致预训练过程中无法主动优化迁移性，也难以预测模型在未见域上的表现。

### 核心动机：从离散集成到连续几何统一

本文的核心动机在于将多域图的知识集成与迁移问题**从离散空间提升到连续黎曼几何空间**。直觉上，每个图可视为一个局部黎曼流形，其节点特征和边结构定义了局部几何度量。不同域的图对应流形上的不同局部区域，知识集成本质上是一个“流形胶合”问题——如何将这些局部流形沿共享结构（边）光滑地拼接成一个全局流形，使得跨域知识传递等价于流形上的几何形变。

这一视角带来了两个关键优势：

- **理论一致性**：通过度规兼容性（metric compatibility）和完整性（holonomy）条件，可以严格定义胶合过程的数学约束，确保知识集成在全局流形上无歧义。
- **可量化的迁移度量**：目标域融入预训练流形所需的几何形变——包括完整性分歧和曲率分歧——可直接量化为**几何传递度量（Geometric Transfer Metric, GTM）**，从而为迁移难度评估和预训练优化提供明确的信号。

### 本文的定位与贡献

基于上述动机，本文提出 **GRAPHGLUE** 框架，其核心是建立**神经流形胶合理论**，将任意图数据集统一到一个光滑的黎曼流形上。与传统方法相比，GRAPHGLUE 从几何层面重新定义了多域图预训练的三大关键环节：局部几何学习（自适应正交帧与稀疏扰动）、流形胶合与光滑化（边度规翻译、完整性损失、曲率损失）、以及领域适应（黎曼混合专家与提示微调）。这一框架不仅为图基础模型的构建提供了理论保证，还通过几何传递度量首次实现了迁移难度的直接量化，为后续的几何缩放律分析和预训练策略优化奠定了基础。



## 核心方法与创新机理

### 问题瓶颈：多域图预训练缺乏一致的几何框架

现有图预训练方法在多域集成上存在根本性瓶颈：它们通常依赖图码本、图元或计算树等离散结构来组织跨域知识，缺乏对知识集成与转移的一致理论框架。这导致两个关键问题难以解决——**如何将不同域的图结构统一到一个连续空间中**，以及**如何量化目标域融入预训练知识所需的迁移难度**。现有方法仅通过相似度等间接指标评估迁移性，无法在预训练与领域适应之间建立一致的几何评估。

### 核心洞察：将知识集成转化为几何形变最小化

GRAPHGLUE的核心洞察是将图预训练重新定义为微分几何问题：**将每个图视为局部黎曼流形，通过边的度规传输和三角形完整性条件胶合成全局光滑流形**。在这一视角下，知识集成与跨域迁移被统一为几何形变的最小化问题——目标域融入预训练流形所需的形变越小，迁移越容易。这使得我们可以定义可量化的几何传递度量（Geometric Transfer Metric, GTM），由完整性分歧和曲率分歧组成，直接量化迁移难度。

### 关键changed slots：三项根本性改变

**1. 多域知识集成方式：从离散结构到连续黎曼流形**

现有方法（如GCOPE、RAGraph等）使用图码本、图元等离散结构组织跨域知识，域之间缺乏连续的几何关系。GRAPHGLUE通过**神经流形胶合理论**，将每个图局部建模为黎曼流形片段，利用自适应正交帧（AOF）学习局部度量张量 $`\pmb{G}_i = \pmb{W}^{(i)\top} \pmb{W}^{(i)}`$（Eq. 1），再通过边度规翻译 $`{\cal P}^{(i,j)}`$（Definition 4.4）保证度量兼容性，最终胶合成统一光滑的全局流形。这一改变使不同域的知识在连续几何空间中自然融合，而非离散堆叠。

**2. 迁移性度量：从间接相似度到几何传递度量（GTM）**

现有方法缺乏可量化的迁移难度指标，仅通过特征相似度间接评估。GRAPHGLUE提出 **GTM = ΔH + ΔC**（Eq. 12），其中完整性分歧 $`\Delta H = \mathcal{L}_{\mathrm{holo}}(\mathcal{G}_0)`$ 衡量目标域融入预训练流形时胶合边界的拓扑偏移，曲率分歧 $`\Delta C = \mathcal{L}_{\mathrm{curv}}(\mathcal{G}_0)`$ 衡量体积元变化率的平滑程度。实验表明，GTM与测试损失高度对齐——曲率损失下降收敛时，测试任务损失呈现相同模式（Figure 3），证明GTM能有效反映迁移难度。

**3. 预训练效率：从全量更新到EMA黎曼原型**

为支持大规模批量预训练，GRAPHGLUE采用指数移动平均（EMA）更新域原型的位置和度量：$`z^{S_k} \gets \beta z^{S_k} + (1-\beta) \frac{1}{|\mathcal{B}_k|} \sum_{\mathcal{G} \in \mathcal{B}_k} z^{\mathcal{G}}`$（Eq. 8），配合对数更新保证度量在正定流形上更新。这替代了传统的全量训练或简单平均原型，在保持几何一致性的同时显著提升预训练效率。

### 理论保证：胶合无偏移与流形光滑

GRAPHGLUE的理论贡献体现在两个核心定理上：**度量兼容性定理**（Theorem 4.5）保证沿边度规翻译能诱导全局度量存在，使局部流形片段在胶合时不产生度量冲突；**三角形平凡完整性定理**（Theorem 4.8）证明当图中所有三角形的完整性映射为单位阵时，胶合边界偏移被消除。基于此，完整性损失 $`\mathcal{L}_{holo}`$（Eq. 5）惩罚非平凡完整性，曲率损失 $`\mathcal{L}_{Curv}`$（Eq. 7）通过对数行列式平滑性控制体积元变化率（Theorem 4.9），共同实现流形胶合的光滑性。消融实验证实，去除曲率损失导致Arxiv 1-shot准确率从28.88降至22.33，去除完整性损失使Reddit 5-shot准确率从85.05降至79.11（Table 22），验证了理论组件的关键作用。

### 局限与开放问题

当前方法假设图中存在足够三角形以保证完整性损失有效，对于稀疏图或缺失三角形的图，近似胶合可能不稳定。几何缩放律的数学形式尚未推导，几何传递度量的泛化性有待在完全未见域上验证。这些开放问题指向未来方向：将GTM扩展为通用图复杂度指标，以及探索不依赖三角完整性的松弛胶合方法。



![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/002_Figure_2.jpg]]
*Figure 2: An Illustration of GRAPHGLUE Framework*

GRAPHGLUE 的核心 pipeline 将多域图预训练与领域适应统一为一个几何连续体：首先将每个图数据集视为局部黎曼流形，然后通过神经流形胶合理论将这些局部片段“粘合”成一个光滑的全局黎曼流形，最后在目标域适应时通过可学习提示和黎曼混合专家将新图胶合到预训练流形上，并用几何传递度量（GTM）量化迁移难度。

### Pipeline 模块与数据流

整个框架由五个关键模块串联构成，输入为多域图数据集，输出为目标域上的任务预测及迁移难度估计。

1. **局部几何学习器（Local Geometry Learner）**
   对每个节点，通过 $(k,M)$-稀疏扰动生成切向量，再经自适应正交帧（AOF）的 QR 分解与长度恢复获得切空间的标准正交基 $\{\pmb{w}_m\}$。局部黎曼度量张量由此直接导出：
   $$\pmb{G}_i = \pmb{W}^{(i)\top} \pmb{W}^{(i)} = \mathrm{diag}(\|\pmb{w}_1\|^2, ..., \|\pmb{w}_M\|^2)$$
   该模块为后续胶合提供每个节点的局部几何描述。

2. **EMA 黎曼原型更新（EMA Riemannian Prototyping）**
   为在流形上区分不同域的语义，框架维护 $K$ 个域原型的位置 $z^{S_k}$ 和度量。采用指数移动平均（EMA）在对数空间更新原型位置：
   $$z^{S_k} \gets \beta z^{S_k} + (1-\beta) \frac{1}{|\mathcal{B}_k|} \sum_{\mathcal{G} \in \mathcal{B}_k} z^{\mathcal{G}}$$
   度量的 EMA 更新同理，保证度量始终保持在正定流形上。该设计支持批量预训练，避免全量计算。

3. **流形胶合与光滑化（Manifold Gluing and Smoothing）**
   这是框架的理论核心。沿图的边执行切向量平移变换 $\mathcal{P}^{(i,j)}$，保证相邻节点的度量兼容性（等距），从而诱导全局度量存在。进一步，对图中每个三角形施加完整性损失 $\mathcal{L}_{\text{holo}}$，消除胶合边界处的偏移；再通过曲率损失 $\mathcal{L}_{\text{Curv}}$ 控制体积元变化率（Ricci 曲率估计），使胶合后的流形达到二阶光滑。同时，样本-原型对比损失 $\mathcal{L}_{\text{proto}}$ 将不同域的原型在流形上推开，强化域间语义分离。

4. **提示适应与黎曼混合专家（Prompt Adaptation and Riemannian MoE）**
   下游适应阶段，通过可学习的提示矩阵 $\pmb{Q}$ 对目标域节点的局部度量进行微调，得到适应后的度量 $\pmb{G}^{\text{adapt}} = \text{diag}(\|\pmb{Q}\pmb{w}_1^\top\|^2, ..., \|\pmb{Q}\pmb{w}_M^\top\|^2)$。黎曼混合专家则从预训练的域原型中集成度量信息，生成几何一致的目标域表示。整体适应损失 $\mathcal{L}_{\text{adap}}$ 平衡任务损失与胶合损失，确保目标域被“粘合”到预训练流形时保持几何连续性。

5. **几何传递度量（Geometric Transfer Metric, GTM）**
   在适应过程中，框架计算目标域融入预训练流形所需的最小几何形变：
   $$\mathbf{GTM}(\mathcal{G}^T; S) = \Delta H + \Delta C, \quad \Delta H = \mathcal{L}_{\text{holo}}(\mathcal{G}_0), \quad \Delta C = \mathcal{L}_{\text{curv}}(\mathcal{G}_0)$$
   其中 $\Delta H$ 为完整性分歧，$\Delta C$ 为曲率分歧。GTM 直接量化迁移难度，且实验表明其与测试损失高度对齐（Figure 3），为迁移性评估提供了可操作的几何指标。

### 框架示意图

Figure 2 展示了 GRAPHGLUE 的整体架构：从左至右依次为局部几何学习、EMA 原型更新、流形胶合与光滑化（预训练阶段），以及下游的提示适应与黎曼 MoE（适应阶段）。不同域的图数据以颜色区分，在胶合过程中逐步融合为统一光滑流形。



GRAPHGLUE 的核心由两个理论模块支撑：**局部几何学习**与**神经流形胶合**。前者为图中每个节点赋予一个局部黎曼度量，后者通过边和三角形将这些局部片断胶合成一个全局光滑流形。

### 局部几何学习：自适应正交帧

每个节点的局部几何由其切空间刻画。GRAPHGLUE 通过以下步骤推断切空间的标准正交基：

1. **$(k,M)$-稀疏扰动**：对节点特征施加稀疏扰动，生成 $M$ 个切向量。
2. **自适应正交帧**：将切向量经图编码器 $f_{\mathrm{GNN}}$ 处理后，通过带长度恢复的 QR 分解得到正交基 $\{\pmb{w}_m\}$。

由此，节点 $i$ 处的局部黎曼度量张量取对角形式：

$$\pmb{G}_i = \pmb{W}^{(i)\top} \pmb{W}^{(i)} = \mathrm{diag}(\|\pmb{w}_1\|^2, ..., \|\pmb{w}_M\|^2) \tag{1}$$

其中 $\pmb{W}^{(i)}$ 的行向量为切空间基，度量张量的对角元即为各基向量的模长平方。该形式保证了度量的正定性，且计算高效。

### 神经流形胶合：边传输与完整性

局部片断通过**边切空间传输**连接。沿边 $(i,j)$ 的传输映射定义为：

$$\mathcal{P}^{(i,j)} = \mathcal{G}_j^{-1/2} \left( \mathcal{G}_j^{1/2} \mathcal{G}_i \mathcal{G}_j^{1/2} \right)^{1/2} \mathcal{G}_j^{-1/2} \tag{2}$$

该映射是一个等距变换，保证了沿边的度量兼容性。定理 4.5 证明，当所有边满足此兼容条件时，可诱导出全局度量。

然而，沿三角形环路传输可能产生偏移。**完整性**刻画了这一现象：对三角形 $\triangle_{ijk}$，完整性映射为三条边传输的复合 $\pmb{H} = \pmb{P}^{(k,i)} \pmb{P}^{(j,k)} \pmb{P}^{(i,j)}$。若该映射为单位阵，则胶合无偏移。为此引入**完整性损失**：

$$\mathcal{L}_{\mathrm{holo}}(\boldsymbol{\mathcal{G}}) = \frac{1}{|\boldsymbol{A}|} \sum_{\boldsymbol{A}_{ijk}} \Vert P^{(k,i)} P^{(j,k)} P^{(i,j)} - \boldsymbol{I} \Vert_F^2 \tag{5}$$

该损失直接惩罚非平凡完整性，迫使所有三角形上的传输环路闭合，消除胶合边界的拓扑偏移。

### 流形光滑化：曲率损失

胶合后的流形仍需保证几何光滑性。利用体积元变化比与 Ricci 曲率的关系：

$$r(z^{(i)}, z^{(j)}) := \frac{\det G_i}{\det G_j} \approx 1 - \frac{1}{3} \mathrm{Ric}(\dot{\gamma}) \tag{6}$$

定义二阶光滑性的**曲率损失**：

$$\mathcal{L}_{\mathrm{Curv}}(\mathcal{G}) = \frac{1}{|A|} \sum_{A_{ijk}} |\log(r_{ij}) - \log(r_{jk})|^2 \tag{7}$$

该损失强制相邻边上对数行列式变化一致，等价于约束 Ricci 曲率在流形上连续变化，从而得到光滑的全局黎曼流形。



## 实验与关键发现

### 主实验结果

GRAPHGLUE在跨域（cross-domain）和域内（intra-domain）的小样本节点分类任务上均展现出显著优势。在跨域1-shot设定下，GRAPHGLUE在Computers数据集上达到59.50%准确率，超出最强基线GCOPE 1.26个百分点（Table 18）；在5-shot设定下，Reddit准确率达84.89%，领先GCOPE 2.77个百分点（Table 21）。域内迁移同样表现稳健：Arxiv 5-shot准确率为39.98%，Reddit 5-shot达84.89%，均优于所有对比方法。值得注意的是，在1-shot极端小样本场景中，GRAPHGLUE的优势更为突出——例如在Computers上领先GCOPE 4.9%（Table 1），表明几何胶合框架在标注极度稀缺时能更有效地复用预训练流形中的知识。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/003_Table_1.jpg]]
*Table 1: Performance of cross-domain transfer on various downstream tasks, reported as mean ± std over 10 runs. The highest result is bolded, and the runner-up is underlined*

与多域预训练基线（PRODIGY、GFT、RAGraph、SAMGPT、MDGFM）相比，GRAPHGLUE在所有评估基准上均取得最优或次优结果，且未出现负迁移现象。相比之下，GCOPE在Reddit的1-shot设定下，随预训练域增加反而出现性能下降（Figure 4），暴露了离散结构集成方法在面对域间冲突时的脆弱性。

### 几何传递度量的有效性

Figure 3展示了曲率损失与测试任务损失的同步下降趋势：随着曲率损失收敛，测试交叉熵损失呈现完全一致的模式。这一实证结果直接验证了几何传递度量（GTM）的有效性——GTM由完整性分歧（ΔH）和曲率分歧（ΔC）组成，能够量化目标域融入预训练流形所需的几何形变程度，从而在训练前即可评估迁移难度。该度量解决了多域图预训练中长期缺乏可量化迁移性指标的问题。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/004_Figure_3.jpg]]
*Figure 3: GTM vs Test Task Loss*

### 几何缩放律

Figure 5揭示了GRAPHGLUE的几何缩放律：随着预训练数据集数量的增加，模型在下游任务上的性能持续提升。这一现象在Computers和Reddit数据集上均得到验证，且性能增长呈平滑上升趋势。其理论解释在于：更多样化的域参与预训练，使胶合后的全局流形更加光滑（曲率连续性更好），从而为目标域提供更优的几何初始点。Figure 4进一步显示，GRAPHGLUE在逐步加入新域时性能稳定提升，而GCOPE则可能出现负迁移，表明黎曼流形胶合在知识累积方面具有天然的兼容性优势。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/006_Figure_5.jpg]]
*Figure 5: Geometric scaling law on (a) Computers and (b) Reddit datasets*

### 消融实验

Table 22的消融实验揭示了各几何约束的因果贡献：

- **去除曲率损失（L_curv）** 导致所有数据集性能显著下降，尤其在1-shot设定下，Arxiv准确率从28.88%骤降至22.33%。曲率损失通过控制体积元变化率（对数行列式平滑性）实现流形的二阶光滑，其缺失直接破坏了度量连续性。
- **去除完整性损失（L_holo）** 同样造成严重性能退化：5-shot Reddit准确率从85.05%跌至79.11%。完整性损失通过惩罚三角形上的非平凡和乐（holonomy），确保胶合边界无偏移，是维持全局拓扑一致性的关键。
- **完整模型**（含EMA原型更新、原型对比损失、黎曼混合专家）在Table 13中始终表现最优，验证了各模块的协同必要性。

### 失败模式与局限

尽管GRAPHGLUE在多数场景下表现优异，但存在以下已知局限：

1. **稀疏图胶合不稳定**：理论框架依赖图中存在足够的三角形以保证完整性损失有效。对于树状结构或极度稀疏的图，近似胶合可能产生不可控的几何偏移，需手动验证具体退化程度。
2. **超参数敏感性**：Table 14和Table 15显示，性能对扰动参数k、流形维度M和损失权重λ较为敏感，不同数据集需要独立调参（如Arxiv与Computers的最优k值差异明显）。这在实际部署中增加了适配成本。
3. **大规模图效率未验证**：EMA原型更新在批训练中保持度量在正定流形上更新，但其在数十亿节点规模图上的收敛速度与内存开销尚未评估，需注意Table 5中内存成本的线性增长假设可能在高维流形下被打破。
4. **GTM泛化性有限**：几何传递度量仅在相关数据集上验证了与测试损失的对齐关系，其在完全未见域（如化学分子图到社交网络）上的预测能力尚未充分评估。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|---------|
| Table 1/18/19 | GRAPHGLUE在跨域小样本设定下全面超越GCOPE等基线，1-shot优势尤为显著 |
| Table 20/21 | 域内迁移同样取得最优结果，验证框架的通用性 |
| Figure 3 | GTM（曲率损失分量）与测试损失同步收敛，证明几何度量可反映迁移难度 |
| Figure 4 | GRAPHGLUE随预训练域增加稳定提升，GCOPE出现负迁移 |
| Figure 5 | 几何缩放律存在：更多域→更光滑流形→更高下游性能 |
| Table 22 | 曲率损失和完整性损失均为关键组件，去除后性能大幅下降 |
| Table 13 | EMA原型、原型对比损失、黎曼MoE三者协同贡献最优性能 |

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/015_Table_9.jpg]]
*Table 9: Hyper-parameters for 1-shot and 5-shot cross-domain transfer on Reddit. Table 11: Hyper-parameters for 1-shot and 5-shot cross-domain transfer on PROTEINS*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/016_Table_10.jpg]]
*Table 10: Hyper-parameters for 1-shot and 5-shot cross-domain transfer on FB15k 237. Table 12: Hyper-parameters for 1-shot and 5-shot cross-domain transfer on HIV*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/020_Table.jpg]]
*Table: (a) on k (M = 32). (b) Analysis on M (k = 15)*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/008_Table_2.jpg]]
*Table 2: Notation and Description*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/009_Table_3.jpg]]
*Table 3: Computational and memory complexity of each module in GraphGlue*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/010_Table_4.jpg]]
*Table 4: Comparison of computational complexity across graph few-shot learning methods*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/011_Table_5.jpg]]
*Table 5: Memory Cost. Lower values indicate better efficiency*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_G3uNHQpP7J/figures/012_Table_6.jpg]]
*Table 6: Statistics of 12 datasets used in our experiment*



## 定位与知识库关联

### 1. 方法谱系与基线关系

GRAPHGLUE 的提出建立在多域图预训练方法演进的瓶颈之上。早期图神经网络（**GCN** (Kipf & Welling, 2017)、**GraphSAGE**、**GIN**）及自监督预训练方法（**GCC**、**DGI**、**GraphMAE**）主要面向单域场景，缺乏跨域知识集成的显式机制。多域预训练方法（**PRODIGY**、**GFT**、**RAGraph**、**SAMGPT**、**GCOPE**、**MDGFM**）虽尝试融合多源图数据，但其知识集成方式普遍依赖图码本、图元或计算树等离散结构，本质上将不同域视为独立符号空间中的离散对象，缺乏对知识跨域集成和转移的一致理论框架——这正是 GRAPHGLUE 所瞄准的核心瓶颈。

GRAPHGLUE 的关键突破在于将多域知识集成从离散结构迁移到连续几何空间：通过神经流形胶合理论，将每个图视为局部黎曼流形，利用边的度规翻译和三角形完整性条件胶合成全局光滑流形，从而将知识集成与转移转化为几何形变的最小化问题。这一理论转向使得 GRAPHGLUE 具备了两个此前方法所不具备的能力：

1. **可量化的迁移性度量**：此前方法仅通过相似度间接评估迁移难度，而 GRAPHGLUE 提出的几何传递度量（GTM）由完整性分歧和曲率分歧组成，直接量化目标域融入预训练流形所需的几何形变。
2. **几何一致性保证**：通过度规兼容性（Theorem 4.5）和三角形平凡完整性（Theorem 4.8）的严格理论保证，消除了胶合边界的不连续性，这是离散集成方法无法提供的性质。

在预训练效率方面，GRAPHGLUE 采用指数移动平均（EMA）原型更新替代全量训练或普通平均原型，支持批量预训练且保持度量在正定流形上更新，在效率与几何一致性之间取得了平衡。

### 2. 适用边界

GRAPHGLUE 的理论框架和实验验证界定了其适用边界：

- **图结构要求**：理论假设图中存在足够的三角形以保证完整性损失有效。对于稀疏图或缺少三角形的图（如二部图、树结构图），近似胶合可能不稳定，完整性损失无法提供有意义的几何约束。
- **域覆盖范围**：实验在 12 个不同域的数据集上进行了综合评估，涵盖引文网络（Arxiv）、社交网络（Reddit）、产品网络（Computers）、知识图谱（FB15k-237）、蛋白质图（PROTEINS）和分子图（HIV）等。在这些域内，GRAPHGLUE 在跨域和域内小样本设定下均展现出优越性。然而，几何传递度量的有效性仅在相关数据集上得到验证，其泛化到完全未见域的能力尚未充分评估。
- **规模限制**：未在大规模图（如数十亿节点）上验证预训练效率，EMA 原型可能在高维流形上收敛较慢，实际部署于工业级大规模图数据时需进一步验证。
- **超参数敏感性**：超参数 $k$（稀疏扰动维度）、$M$（正交帧维度）、$\lambda$（胶合损失权重）对性能敏感，需要针对不同数据集调整。1-shot 和 5-shot 设定下的敏感性分析（Table 14、Table 15）表明，参数选择对最终性能有显著影响。

### 3. 局限与开放问题

**已识别的局限**：

1. **三角完整性依赖**：完整性损失的有效性依赖于图中存在足够数量的三角形。当图结构稀疏或缺少闭合环时，胶合边界的几何一致性无法得到充分约束，可能导致流形局部形变不协调。
2. **跨域泛化未充分验证**：GTM 的预测能力仅在实验涉及的 12 个数据集域内得到验证，对于分布差异极大的全新图域，GTM 与迁移性能的相关性尚不明确。
3. **大规模可扩展性未知**：EMA 原型更新在黎曼流形上的收敛速度与流形维度和域数量相关，在高维流形或大量域的场景下可能收敛缓慢。
4. **超参数调优成本**：$k$、$M$、$\lambda$ 等关键参数需要针对每个目标域进行调优，增加了实际部署的工程成本。

**开放问题**：

1. **通用图复杂度度量**：如何将几何传递度量扩展为通用的图复杂度或迁移性指标，以指导基础模型的构建？若 GTM 能够脱离特定预训练流形而独立评估任意图的迁移难度，将极大提升图基础模型的设计效率。
2. **与大语言模型的融合**：能否将本框架与大型语言模型结合，用于文本属性图的跨域预训练？文本属性图同时包含结构信息和语义信息，黎曼流形胶合理论为两者的统一建模提供了几何框架。
3. **松弛胶合方法**：在不满足三角完整性条件时，是否存在更有效的松弛胶合方法？例如，对于二部图或长程依赖图，能否通过路径完整性或谱方法近似胶合一致性？
4. **几何缩放律的理论推导**：实验已观察到几何缩放律（Figure 5），即预训练域数量增加带来性能的稳定提升。其数学形式是否可推导，从而无需大量实验即可预测性能增长？这直接关系到图基础模型的规模化策略设计。
5. **负迁移的几何解释**：实验显示 GCOPE 在加入某些域后出现负迁移（Figure 4），而 GRAPHGLUE 避免了这一问题。这是否可以从曲率分歧或完整性分歧的角度给出几何解释，从而建立负迁移的预警机制？



## 原文 PDF

![[paperPDFs/ICLR_2026/Multi_Domain_Riemannian_Graph_Gluing_for_Building_Graph_Foundation_Models.pdf]]
