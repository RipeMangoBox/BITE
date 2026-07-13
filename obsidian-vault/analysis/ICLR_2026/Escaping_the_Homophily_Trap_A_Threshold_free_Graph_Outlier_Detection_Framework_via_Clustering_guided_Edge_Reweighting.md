---
title: "Escaping the Homophily Trap: A Threshold-free Graph Outlier Detection Framework via Clustering-guided Edge Reweighting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Escaping_the_Homophily_Trap_A_Threshold_free_Graph_Outlier_Detection_Framework_via_Clustering_guided_Edge_Reweighting.pdf
project_link: null
code_link: null
aliases:
- CG
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "通过可学习的边权重掩码，选择性削弱异质性邻居的聚合强度，增强正常与异常候选节点在潜空间的可分性。"
primary_logic: "联合优化自判别掩码破坏器与基于聚类的异常检测器，用聚类生成的伪标签引导掩码学习，消除对预定异常阈值的依赖；同时引入多样性损失防止聚类坍缩，实现稳定的无监督端到端检测。"
claims:
- "CER-GOD在Email数据集上AUC达到96.98%，比先前最佳方法AS-GAE提升超过12个百分点。"
- "SD-MS模块通过自适应边重加权显著增强了正常与异常节点嵌入的区分度，t-SNE和距离分布直方图直观显示分离效果提升。"
- "移除SD-MS（w/o SD-MS）后，所有数据集的AUC均大幅下降，例如Email从96.98%降至约50.80%，验证了掩码破坏器的核心作用。"
- "多样性损失有效防止聚类坍缩，是训练过程不可消融的关键组件。"
---

# Escaping the Homophily Trap: A Threshold-free Graph Outlier Detection Framework via Clustering-guided Edge Reweighting

> [!tip] 核心洞察
> 联合优化自判别掩码破坏器与基于聚类的异常检测器，用聚类生成的伪标签引导掩码学习，消除对预定异常阈值的依赖；同时引入多样性损失防止聚类坍缩，实现稳定的无监督端到端检测。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 逃离同质性陷阱：基于聚类引导边重加权的无阈值图异常检测框架 |
| 英文题名 | Escaping the Homophily Trap: A Threshold-free Graph Outlier Detection Framework via Clustering-guided Edge Reweighting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Z8f0whjttd) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | CER-GOD |
| Dataset | Email, Amazon, Disney, OGB-Proteins |

> [!tip] 效果简介
> - Email 上，AUC 为 96.98±0.08，对比 AS-GAE (previous SOTA)，变化 >+12%。
> - Amazon 上，AUC 为 86.24±3.56，对比 Best baseline (e.g., TAM)，变化 排名第一。
> - Disney 上，AUC 为 72.13±3.01，对比 Best baseline，变化 排名第一。

## 概要

图异常检测任务中，图卷积操作容易陷入“同质性陷阱”：异常节点会通过邻域聚合污染邻近正常节点的表示，导致正常与异常节点的嵌入高度重叠，严重损害检测区分度。针对这一核心瓶颈，本文提出一个无阈值图异常检测框架**CER-GOD**，其核心思想是通过**聚类引导的边重加权**机制，自适应地削弱异质性邻居的影响，从而扩大正常与异常节点在潜空间中的分布差异。

CER-GOD 框架由四个关键组件构成：
1. **自判别掩码破坏器 (Self-Discriminative Masking Spoiler, SD-MS)**：学习一个可训练的边权重掩码，以哈达玛积方式调整原始邻接矩阵，选择性抑制携带异质信号的边；
2. **图自编码器 (GAE)**：基于重加权后的图结构学习节点嵌入，并重建节点属性和邻接矩阵；
3. **基于聚类的异常检测器**：通过可学习的聚类层产生软分配，并利用聚类伪标签引导掩码学习，同时输出无需人工指定阈值的异常评分 $s_i = 1 - q_{i, pos}$；
4. **多样性损失 $\ell_{\text{diversity}}$**：强制每个聚类维持最低样本比例，有效防止聚类坍缩。

整个模型通过联合优化重建损失、聚类损失（含多样性正则）和分布推斥损失（最大化正常与异常候选集的最大均值差异）进行端到端训练，实现了无须预设阈值的稳定无监督异常检测。

实验表明，CER-GOD 在 8 个公开基准数据集上取得了最优或次优性能。在 **Email** 数据集上 AUC 达到 **96.98%**，比先前最优秀的 AS-GAE 方法提升超过 12 个百分点；在 **Amazon**、**Disney**、**OGB-Proteins** 等数据集上同样名列第一。消融研究证实，移除 SD-MS 模块后 Email 的 AUC 骤降至约 50.80%，而多样性损失对防止聚类坍缩不可或缺。定性分析进一步显示，SD-MS 能够显著拉开正常与异常节点嵌入的距离分布，缓解嵌入重叠问题。总体而言，CER-GOD 为解决图异常检测中的同质性污染提供了一种有效且无阈值的新范式。



图异常检测旨在识别图中显著偏离多数正常模式的节点、边或子结构，在恶意用户检测、系统故障诊断、金融欺诈等多个领域具有关键应用价值。近年来，基于图神经网络（GNN）的方法因能同时利用节点属性与图拓扑信息而成为主流。然而，GNN 的图卷积操作暗含一个严重缺陷——**同质性陷阱（Homophily Trap）**：异常节点的属性通过邻域聚合“污染”其正常邻居的表示，导致正常节点与异常节点在潜空间中嵌入分布高度重叠，使后者难以被检测器有效分离（Figure 2）。具体而言，多层图卷积下节点属性沿着路径传播的影响上界 $|\frac{\partial \mathbf{z}_j^{(r+1)}}{\partial \mathbf{x}_i}| \leq (\alpha\beta)^{r+1} (\mathbf{A}^{r+1})_{ji}$（Eq. 3）表明，异常节点能直接影响位于短距离内的正常节点，使其嵌入被“拖拽”向异常区域。在 Email 数据集上，仅经一层图卷积后，异常节点的 1‑hop 正常邻居与异常节点自身相对于参考高斯分布的 MMD 距离分布已高度纠缠，无法有效区分（Figure 2）；相比之下，远离异常的节点则保持显著差异。这一现象充分暴露了传统图卷积在同质性假设被违反时脆弱性。

现有图异常检测方法未能主动应对上述陷阱。基于图自编码器（GAE）重建的方法（如 DOMINANT、AnomalyDAE、CONAD）使用原始邻接矩阵进行信息聚合，默认所有边都携带同等有用的信息。当图中存在大量异质性边（即连接异常节点与正常节点的边）时，这些方法聚合到正常邻居上的信息被异常特征污染，导致重建误差或对比学习任务难以提供足够的判别性。虽然 AS‑GAE、ADA‑GAD 等近期工作通过对抗训练或数据增强试图减轻噪声影响，但它们仍以原始图的二值邻接关系为基准，缺乏对边传播强度的**自适应加权**能力。此外，绝大多数方法依赖手工设定的异常分数阈值或重建误差阈值来判断异常，这种依赖不仅引入了额外的超参数敏感性，也在完全无监督场景中阻碍了可靠的端到端优化。

上述缺口在 Email 数据集上表现尤为突出：先前最优方法 AS‑GAE 的 AUC 仅约 84%（Table 1），距离理想指标存在巨大差距，表明同质性陷阱是制约检测性能提升的关键瓶颈。因此，迫切需要一种新范式：**有选择地削弱异质性边的影响力，并消除对预定异常阈值的依赖**，以构建更鲁棒的图异常检测器。

本文的核心动机正是针对这两大痛点：① 提出可学习的边权重掩码（Self‑Discriminative Masking Spoiler），通过哈达玛积 $\tilde{\mathbf{A}} = \tilde{\mathbf{M}} \odot \mathbf{A}$（Eq. 5）自适应地重新加权图拓扑，从而主动抑制异常邻居对正常节点的干扰；② 引入聚类引导的无阈值异常评分机制，利用聚类伪标签指导掩码学习，实现完全无监督下的端到端联合优化，彻底脱离手工阈值设定的限制。辅以防止聚类坍缩的多样性损失，该范式有望从根源上打破同质性陷阱，大幅提升图异常检测在复杂真实场景下的区分能力与稳定性。



## 核心方法与创新机理

CER‑GOD 围绕图异常检测的同质性陷阱（Homophily Trap）展开：图卷积操作会将异常节点的特征扩散到正常邻域，导致两类节点在潜空间的嵌入高度重叠，严重削弱区分度（Figure 2）。与其依赖外部规则或硬阈值来绕过该陷阱，该方法引入了一个可端到端学习的**因果操控变量**——通过可训练边权重掩码，选择性抑制异质性邻居的聚合强度，从而增大正常与异常候选集的可分性。

**关键技术变化点（Changed Slots）** 相较于既有基线主要体现在三个维度：

| 设计维度 | 基线策略 | CER‑GOD 策略 | 证据 |
|---------|---------|-------------|------|
| **边权重策略** | 使用原始邻接矩阵或等权聚合 | 学习掩码 $\tilde{\mathbf{M}}$，通过 $\tilde{\mathbf{A}}=\tilde{\mathbf{M}}\odot\mathbf{A}$ 削弱异质性边；掩码受聚类伪标签引导优化 | Section 2.2, Eq. (5)；消融移除 SD‑MS 后 Email AUC 从 96.98% 跌至 ≈50.80%（Table 2） |
| **异常判定方式** | 基于预设阈值的评分或重建误差 | 无阈值聚类软分配评分 $s_i = 1 - q_{i,\mathrm{pos}}$，无需手动设定判决边界 | Section 2.3, Eq. (13)；整个框架完全无监督，消除了阈值超参 |
| **聚类稳定性** | 标准聚类损失可能导致类别坍缩 | 引入多样性损失 $\ell_{\mathrm{diversity}} = \sum_k \max(0, \varepsilon - \hat{u}_k)$，强制每个聚类维持至少 $\varepsilon$ 样本比例 | Section 2.3, Eq. (12)；消融实验显示多样性损失是关键稳定剂（Table 2） |

这些变化点共同构成了**自判别掩码破坏器（Self‑Discriminative Masking Spoiler, SD‑MS）** 与**基于聚类的异常检测器**的联合优化闭环。闭环的核心逻辑如下：

1. **图自编码器（GAE）** 通过重建损失 $\ell_{\mathrm{r}}$（Eq. 4）学习基础节点嵌入，保留拓扑和属性信息。
2. **SD‑MS** 在 GAE 前插入可训练的边掩码，将原始图改写为 $\tilde{\mathbf{A}}$，使 GCN 聚合时自动弱化那些可能传播异常特征的边。掩码的优化信号来源于聚类器生成的正常/异常候选集的分布差异最大化——即**分布推斥损失** $\ell_{\mathrm{dr}} = -\mathbf{MMD}^2(\mathcal{D}_{\mathrm{pos}}, \mathcal{D}_{\mathrm{neg}})$（Eq. 6‑8），迫使两类节点的嵌入在潜空间彼此远离。
3. **聚类器** 使用学生‑t 分布计算软分配 $q_{ij}$（Eq. 9），并通过 KL 散度 $\ell_c$（Eq. 11）向锐化的目标分布 $p_{ij}$（Eq. 10）靠拢，从而自动生成用于引导 SD‑MS 的伪标签。异常评分直接取自正常类软分配的补集，无需外部阈值。
4. **多样性损失** 作为正则项防止聚类坍缩，使训练过程稳定。消融实验（Table 2）表明，缺少该损失时模型性能骤降，证实其不可替代性。

与采用 GAT 注意力或者标准聚类的变体（如 GAT+ClusterAD）相比，CER‑GOD 的 SD‑MS 模块带来了**定性可观测的分布分离**：t‑SNE 可视化（Figure 5）和嵌入距离直方图（Figure 7）显示，两类节点的重叠区域显著缩小，分布中心彼此错开。定量上，在 Email 数据集上，CER‑GOD 的 AUC 达到 96.98%，超越先前最优方法 AS‑GAE 超过 12 个百分点（Table 1）；在 OGB‑Proteins 等大规模图上，亦以 74.81% AUC 位列第一（Table 4）。这些结果表明，**基于聚类伪标签的边重加权机制**是实现高区分度无监督图异常检测的关键因果操作，而多样性损失则保证了该机制的优化稳定性。



![[assets/figures/papers/iclr26_0015_Z8f0whjttd_Escaping_the_Homophily_Trap_A_Threshold-free_Gra/figures/001_Figure_1.jpg]]
*Figure 1: The architecture of the proposed CER-GOD framework for graph outlier detection. The model takes an input graph with its topology, applies a learnable mask to suppress noisy or irrelevant connections, and encodes the refined structure using graph convolutional layers. The latent embeddings are then used for graph reconstruction and clustering-based anomaly prediction. Based on these predictions, normal and anomalous candidate groups are generated and optimized through distribution repulsion loss. The framework is jointly optimized with three objectives: reconstruction loss, clustering loss (with a diversity regularization term), and a distribution repulsion loss*

CER-GOD 是一个端到端的无监督图异常检测框架，其核心目标是通过可学习的边重加权机制打破图中同质性陷阱（homophily trap）——即异常节点通过消息传递污染相邻正常节点表示，导致两类嵌入在潜空间高度重叠、检测区分度严重下降。框架以原始属性图 $(\mathbf{A}, \mathbf{X})$ 为输入，输出每个节点的无阈值异常评分 $s_i$，整体流水线如下：

1. **自判别掩码破坏器（SD-MS）**  
   学习一个实值掩码 $\tilde{\mathbf{M}} \in [0,1]^{N \times N}$，通过哈达玛积对邻接矩阵进行自适应重加权：$\tilde{\mathbf{A}} = \tilde{\mathbf{M}} \odot \mathbf{A}$（Eq. 5）。掩码的优化目标并非直接由标签监督，而是由后续聚类检测器生成的正常/异常候选伪标签间接引导——即 **“自判别”** 的含义。掩码放大了正常子图内部的同质性连接，同时削弱异质性邻居的聚合强度，为下游嵌入学习提供净化后的拓扑。

2. **图自编码器（GAE）**  
   以重加权邻接矩阵 $\tilde{\mathbf{A}}$ 和节点属性 $\mathbf{X}$ 为输入，经多层图卷积编码器生成潜变量 $\mathbf{Z}$，再由解码器重建属性 $\hat{\mathbf{X}}$ 和邻接矩阵 $\hat{\mathbf{A}}$，计算重建损失 $\ell_{\mathrm{r}}$（Eq. 4）。GAE 负责将图结构和属性压缩为判别性嵌入，是整个框架的基础表示层。

3. **基于聚类的异常检测器**  
   在编码器输出的嵌入 $\mathbf{Z}$ 上部署一个可学习聚类层。采用学生 t-分布计算软分配 $q_{ij}$（Eq. 9），进而构造锐化的目标分布 $p_{ij}$（Eq. 10），并以 KL 散度 $\ell_c = \mathrm{KL}(P \| Q)$（Eq. 11）优化聚类。聚类结果同时提供两个关键信号：
   - **正常/异常候选组划分**：根据软分配将节点分为正常候选集 $\mathcal{D}_{\mathrm{pos}}$ 和异常候选集 $\mathcal{D}_{\mathrm{neg}}$，用于指导 SD‑MS 的掩码学习以及分布推斥损失；
   - **无阈值异常评分**：直接取正常类软分配的补集 $s_i = 1 - q_{i,\mathrm{pos}}$（Eq. 13），彻底消除对手工阈值的依赖。

4. **分布推斥损失（DR Loss）**  
   计算两组候选嵌入集合之间的最大均值差异（MMD）：$\mathbf{MMD}^2(\mathcal{D}_{\mathrm{pos}}, \mathcal{D}_{\mathrm{neg}})$（Eq. 6），并取其负值 $\ell_{\mathrm{dr}} = -\mathbf{MMD}^2$（Eq. 8），迫使正常与异常节点在潜空间中的分布尽可能远离。该损失直接作用于嵌入学习，是逃脱同质性陷阱的关键驱动——消融实验表明，移除 SD‑MS 后 Email 数据集 AUC 从 96.98% 骤降至约 50.80%（Table 2），且正常/异常嵌入的距离分布重叠大幅增加（Figure 7）。

5. **多样性损失（Diversity Loss）**  
   为防止聚类过程中出现类别坍缩（所有样本被划入同一簇），引入正则项 $\ell_{\mathrm{diversity}} = \sum_k \max(0, \varepsilon - \hat{u}_k)$（Eq. 12），强制每个聚类的样本比例不低于 $\varepsilon$。该模块是训练稳定性的必要保障（Table 2 的消融结论）。

**联合优化与数据流**  
各模块彼此依赖、协同更新：GAE 提供嵌入 $\mathbf{Z}$，聚类检测器从 $\mathbf{Z}$ 中获得伪标签与异常评分，SD‑MS 利用伪标签以最大化候选集分布差异为目标调整边权重，而分布推斥损失则反向迫使 GAE 学习更具区分度的嵌入。三个核心损失加权组合共同构成优化目标：
$$\ell = \ell_{\mathrm{r}} + \alpha \ell_c + \beta \ell_{\mathrm{dr}} + \gamma \ell_{\mathrm{diversity}}$$
超参数 $\alpha, \beta, \gamma$ 在较宽范围内保持性能稳定（Figure 3）。整个流水线无需任何标签或预定阈值，在完全无监督的条件下实现了鲁棒的图异常检测。框架的直观结构如 Figure 1 所示。



CER‑GOD 由四个关键组件协同构成：**图自编码器 (GAE)** 负责生成基础节点嵌入，**自判别掩码破坏器 (SD‑MS)** 自适应削弱异质性边，**基于聚类的异常检测器** 提供无阈值异常评分，**多样性损失** 防止聚类坍缩。各模块的核心公式及变量含义梳理如下。

### 1. 图自编码器 (GAE) 与重建损失
GAE 通过编码器‑解码器结构将节点映射为低维嵌入 $\mathbf{z}_i$，并强迫嵌入保留图的结构与属性信息。其重建损失定义为：
$$
\ell_{\mathrm{r}} = \frac{1}{N} \sum_{i=1}^{N} \left( \| \hat{\mathbf{x}}_i - \mathbf{x}_i \|^2 + \| \hat{\mathbf{A}}_i - \mathbf{A}_i \|^2 \right) \tag{4}
$$
其中 $N$ 为节点总数，$\hat{\mathbf{x}}_i$、$\mathbf{x}_i$ 分别是节点 $i$ 的重构与原始属性向量，$\hat{\mathbf{A}}_i$、$\mathbf{A}_i$ 是重构与原始邻接矩阵的第 $i$ 行。该损失确保嵌入 $\mathbf{z}_i$ 能较好地恢复输入特征和邻接关系。

### 2. 自判别掩码破坏器 (SD‑MS)
SD‑MS 的核心是可学习的边权重掩码 $\tilde{\mathbf{M}} \in [0,1]^{N\times N}$，通过哈达玛积调整原始邻接矩阵：
$$
\tilde{\mathbf{A}} = \tilde{\mathbf{M}} \odot \mathbf{A} \tag{5}
$$
掩码的优化目标是**最大化正常候选节点与异常候选节点在潜空间的可分性**。首先计算两集合嵌入的经验最大均值差异 (MMD)：
$$
\begin{aligned}
\mathbf{MMD}^2[\mathcal{F},\mathcal{D}_{\mathrm{pos}},\mathcal{D}_{\mathrm{neg}}] 
= &\frac{1}{m(m-1)} \sum_{i=1}^{m} \sum_{j\neq i} \kappa(\mathbf{z}_i^{\mathrm{pos}},\mathbf{z}_j^{\mathrm{pos}}) \\
+ &\frac{1}{n(n-1)} \sum_{i=1}^{n} \sum_{j\neq i} \kappa(\mathbf{z}_i^{\mathrm{neg}},\mathbf{z}_j^{\mathrm{neg}}) 
- \frac{2}{mn} \sum_{i=1}^{m} \sum_{j=1}^{n} \kappa(\mathbf{z}_i^{\mathrm{pos}},\mathbf{z}_j^{\mathrm{neg}}) \tag{6}
\end{aligned}
$$
其中 $\mathcal{D}_{\mathrm{pos}}$、$\mathcal{D}_{\mathrm{neg}}$ 分别为根据当前聚类伪标签划分的正常与异常候选节点嵌入集合，$m$、$n$ 是各自集合大小，$\kappa(\cdot,\cdot)$ 为核函数（实践中常用 Chebyshev 核以突出单维度最大差异）。分布推斥损失直接取 MMD 的相反数：
$$
\ell_{\mathrm{dr}} = -\mathbf{MMD}^2(\mathcal{D}_{\mathrm{pos}},\mathcal{D}_{\mathrm{neg}}) \tag{8}
$$
通过最小化 $\ell_{\mathrm{dr}}$，掩码将被“推斥”以筛选掉那些导致两类分布重叠的异质性边，从而增强正常与异常节点的嵌入区分度。

### 3. 基于聚类的异常检测器
该检测器通过可学习的聚类层生成伪标签，并实现无阈值评分。对于嵌入 $\mathbf{z}_i$，其属于聚类 $j$ 的软分配概率基于 Student‑t 分布：
$$
q_{ij} = \frac{ (1 + \| \mathbf{z}_i - \pmb{\mu}_j \|^2)^{-1} }{ \sum_{j'=1}^{c} (1 + \| \mathbf{z}_i - \pmb{\mu}_{j'} \|^2)^{-1} } \tag{9}
$$
式中 $\pmb{\mu}_j$ 为第 $j$ 个聚类中心，$c$ 为聚类个数（异常检测常设 $c=2$）。为提升簇内紧凑性，进一步构造锐化后的目标分布 $p_{ij}$：
$$
p_{ij} = \frac{ q_{ij}^2 / \sum_{i=1}^N q_{ij} }{ \sum_{j'=1}^c q_{ij'}^2 / \sum_{i=1}^N q_{ij'} } \tag{10}
$$
聚类损失是最小化当前分布 $Q$ 与目标分布 $P$ 之间的 KL 散度：
$$
\ell_c = \mathrm{KL}(P \| Q) = \sum_{i=1}^N \sum_{j=1}^c p_{ij} \log \frac{p_{ij}}{q_{ij}} \tag{11}
$$
最终，节点 $i$ 的异常分数直接由其不属于“正常”聚类的概率给出，无需人为设定阈值：
$$
s_i = 1 - q_{i,\mathrm{pos}} \tag{13}
$$
其中 $q_{i,\mathrm{pos}}$ 是将节点 $i$ 分配给正常聚类（通常指样本量较大的类）的软概率。

### 4. 多样性损失
标准聚类损失易导致类别坍缩（所有样本被归入同一类）。为此引入多样性损失，强制每个聚类至少维持一定比例的样本：
$$
\ell_{\mathrm{diversity}} = \sum_{k=1}^c \max(0, \varepsilon - \hat{u}_k) \tag{12}
$$
其中 $\hat{u}_k$ 为聚类 $k$ 中样本的经验比例，$\varepsilon$ 为允许的最小比例阈值（文内固定为 $\varepsilon=1$）。该损失有效防止了训练过程中某一聚类被清空。

最终，CER‑GOD 以权重 $\alpha,\beta,\gamma$ 联合最小化以上四项损失：  
$\ell_{\mathrm{total}} = \ell_{\mathrm{r}} + \alpha \ell_c + \beta \ell_{\mathrm{dr}} + \gamma \ell_{\mathrm{diversity}}$，使掩码学习与异常检测在统一无监督框架下协同进化。



## 实验与关键发现

### 主实验结果

CER-GOD在8个基准数据集上系统性地评估，包括Email、Cora、Disney、Flickr、CiteSeer、Enron、Reddit与Amazon（表Table 1）。为了公平比较，所有基线方法均采用相同GCN主干、公开代码和默认参数设置。结果上，CER-GOD在所有数据集上均取得最优或次优AUC，尤其是：

![[assets/figures/papers/iclr26_0015_Z8f0whjttd_Escaping_the_Homophily_Trap_A_Threshold-free_Gra/figures/004_Table_1.jpg]]
*Table 1: Average AUCs with standard deviation (10 trials) of different graph anomaly detection algorithms. The best and second-best results are bolded and underlined, respectively*

- **Email**：AUC达到96.98%±0.08，相较先前SOTA方法AS-GAE提升超过12个百分点，体现模型在捕获异常模式上的显著优势。
- **Amazon**：AUC为86.24%±3.56，稳居第一。
- **Disney**：AUC为72.13%±3.01，同样领跑所有对比方法。

大规模图上的泛化能力在OGB-Proteins数据集得到验证：CER-GOD取得74.81% AUC，超过TAM（74.49%）等基线（表Table 4），证明其可扩展性。

![[assets/figures/papers/iclr26_0015_Z8f0whjttd_Escaping_the_Homophily_Trap_A_Threshold-free_Gra/figures/030_Table_4.jpg]]
*Table 4: AUCs (%) of different graph anomaly detection algorithms on large-scale dataset OGB-Proteins. The best result is bolded*

### 消融研究

为揭示各模块的因果贡献，我们在Email、Cora、Flickr上进行消融（表Table 2）：

![[assets/figures/papers/iclr26_0015_Z8f0whjttd_Escaping_the_Homophily_Trap_A_Threshold-free_Gra/figures/028_Table_2.jpg]]
*Table 2: Ablation Study on Email, Cora, and Flickr (mean (%)±std (%))*

- **移除SD-MS模块**（w/o SD-MS）导致AUC崩塌式下降——Email上从96.98%暴跌至约50.80%，说明自判别掩码破坏器是逃离同质性陷阱的核心机制。
- **移除图重建损失**（w/o Reconstruction）使得性能大幅下滑，验证了图自编码器在提供可判别嵌入方面的必要角色。
- 仅使用重建的异常检测器（Reconstruction OD）亦远逊于完整模型，表明聚类引导的边重加权与分布推斥损失缺一不可。

此外，即便将GCN替换为GAT并在其上加聚类检测器（GAT+ClusterAD），性能仍远低于CER-GOD，原因是通用注意力机制无法像SD-MS那样针对性地削弱异质性边。多样性损失ℓ_diversity的作用同样不可消融：移除该正则项后，聚类极易坍缩，训练不稳定。

### 参数敏感性

超参数α、β、γ（分别控制聚类损失、分布推斥损失和多样性损失权重）在较宽范围（如[0.01, 1]）内模型性能保持稳定（图Figure 3），说明框架具有较好的鲁棒性。关键部件级分析（图Figure 4）揭示了以下趋势：

- **MMD核函数**：Chebyshev核在所有数据集上一致优于RBF核，因其能捕捉单个维度上的最大差异，更有效地识别异常模式。
- **多样性阈值ε**：ε固定为1时性能良好；若ε过小，则聚类坍缩风险升高，过大则会轻微损害AUC。
- **分布推斥层位置**：将ℓ_dr作用于第一层GCN效果最佳，随着层数加深性能逐渐衰减（图Figure 4(c)），表明早期层次的结构扰动对表示分离影响更关键。

### 效率分析

运行时间对比（表Table 3）显示，CER-GOD在200个epoch内的计算开销处于competitive水平：远低于AD-GCL（>2000s），与DOMINANT等高效方法接近，在保持高精度的同时未引入过重计算负担。

### 定性可视化与机制验证

t-SNE可视化（图Figure 5）直观揭示了基线方法的同质性陷阱：DOMINANT、AnomalyDAE、CONAD等方法的正常（蓝色）与异常（红色）节点嵌入高度重叠。而CER-GOD通过SD-MS重加权边拓扑，使异常节点形成紧凑、分离良好的簇，从而大幅提升检测区分度。

![[assets/figures/papers/iclr26_0015_Z8f0whjttd_Escaping_the_Homophily_Trap_A_Threshold-free_Gra/figures/022_Figure_5.jpg]]
*Figure 5: The comparison of t-SNE visualizations on the Email dataset for all baseline methods and(a) Flickr (b) Cora the proposed model. Normal nodes are depicted in blue, while anomalous nodes are shown in red*

进一步的距离分布分析（图Figure 7）量化了该效果：以标准高斯分布为参考计算嵌入距离时，移除SD-MS后正常与异常节点的直方图严重混叠；引入SD-MS后，正常节点集中在较低距离区间，异常节点明显外推至高距离区域，两类重叠大幅减少。这印证了SD-MS通过打压异质性邻居，成功净化了正常节点表示，从而放大了异常性。

![[assets/figures/papers/iclr26_0015_Z8f0whjttd_Escaping_the_Homophily_Trap_A_Threshold-free_Gra/figures/027_Figure_7.jpg]]
*Figure 7: Distribution histograms of embedding distances with or w/o SD-MS on Cora. The distance is computed between learned embeddings and vectors sampled from a standard Gaussian distribution $\mathcal { N } ( \mathbf { 0 } , \mathbf { I } _ { k }$ ) through $L _ { \mathrm { { 2 } } } \mathrm { { - n o r m } }$

### 局限性与失败模式

1. **多数类假设**：CER-GOD的性能依赖正常节点在图中占多数的先验，在高度不平衡或异常占主导的场景中，伪标签质量和模型稳定性可能劣化。
2. **二元聚类到多类扩展**：当前检测器使用c=2进行二元正常/异常分离，如何自动将更多聚类映射到真实标签，或直接支持多类异常判定，需要进一步研究。
3. **复杂度瓶颈**：分布推斥损失在最坏情况下的复杂度为O(N^2)，图重建损失也具有较高计算开销，这限制了在超大规模图（例如千万级节点）上的可扩展性。
4. **超参数适配**：α、β需针对每个数据集手动调节，增加了应用成本；尽管存在稳定区间，但最佳设置仍需少量调参。
5. **固定多样性阈值**：ε固定为1，在某些数据集上可能不是最理想的样本比例约束，未来可设计自适应阈值或动态合并机制来增强对不同异常模式的覆盖。
6. **动态图与流式数据**：当前模型假定静态拓扑，难以直接适用于随时间演化的图，如何增量式学习边掩码和聚类结构是一个待解决问题。



## 定位与知识库关联

### 与基线方法的关系

CER-GOD 延续了基于图自编码器（GAE）的异常检测范式，但其核心创新在于对聚合过程的主动干预与异常判定的无阈值化。与重构系列方法（DOMINANT、AnomalyDAE）仅依赖重建误差区分异常不同，CER-GOD 引入 **自判别掩码破坏器（SD-MS）**，通过可学习的边掩码 $\tilde{\mathbf{A}} = \tilde{\mathbf{M}} \odot \mathbf{A}$ 选择性削弱异质性邻居的影响，从根本上缓解了“同质性陷阱”导致的嵌入重叠问题。这一改变体现在关键机制差异上：从 **原始图结构或无差别邻域聚合** 变为 **聚类伪标签引导的边重加权**。消融实验表明，移除 SD‑MS 后，Email 数据集上的 AUC 由 96.98% 骤降至约 50.80%（Table 2），直接验证了该模块的决定性作用。

在异常判定方式上，CER-GOD 颠覆了基于预定阈值的重构误差比较（如 AS‑GAE 使用的对抗性评分）和对比学习中的启发式匹配（如 AD‑GCL、ADA‑GAD），转而采用 **基于聚类软分配的无阈值评分** $s_i = 1 - q_{i,\mathrm{pos}}$。该设计使模型能够通过可学习的聚类层（Eq. 9–11）自动产生正常/异常伪标签，消除了对手工阈值的依赖。同时引入的 **多样性损失** $\ell_{\mathrm{diversity}}$ 强制每个聚类至少维持最低比例样本，解决了传统聚类损失可能导致的类别坍缩问题（Table 2 中移除此项性能下降，证实其必要性）。

从对抗与对比两大技术流派看，CER-GOD 以 **分布推斥损失** $\ell_{\mathrm{dr}} = -\mathbf{MMD}^2(\mathcal{D}_{\mathrm{pos}},\mathcal{D}_{\mathrm{neg}})$ 替代对抗训练的博弈过程，通过最大化正常候选集与异常候选集在潜在空间的 MMD 距离实现分布分离，避免了对抗训练的不稳定性；Chebyshev 核在 MMD 计算中的使用进一步提升了异常模式捕获能力（Figure 4a）。相较于对比方法，CER-GOD 无需设计复杂的正负采样和视图增广，而是依托聚类生成的软标签进行自监督引导，在简单高效的同时取得了超越 SOTA 的性能（Email 上领先 AS‑GAE 超 12 个百分点，Table 1）。

### 适用边界

CER-GOD 的设计建立在 **正常节点占多数的假设** 之上（聚类分配中倾向于将大簇标记为正常类），因此在高度不平衡或异常节点比例接近 50% 的场景下可能退化。模型适用于 **静态属性图** 上的二元异常检测，尚未扩展至动态图、流式图或多类异常情形；其聚类层默认采用二类分离（$c=2$），多类映射机制仍属开放问题。此外，模型性能受数据集超参数调节的影响：α 和 β 虽在较宽范围保持稳定（Figure 3），但仍需针对具体任务进行微调；多样性损失中的 ε 固定为 1，在部分数据集上可能并非最优（Figure 4b）。在计算规模上，分布推斥损失的最坏复杂度达到 $O(N^2)$，虽在 OGB‑Proteins 等较大图上仍以 74.81% AUC 胜过 TAM（Table 4），但极端规模的图（千万节点级）的可扩展性尚未验证。

### 局限与开放问题

1. **多类异常与标签映射的不稳定性**：当前二元聚类需将多个学习到的簇映射为正常/异常标签，完全无监督设置下如何避免映射动荡是待解难题；多类异常检测的框架扩展也未实现。
2. **超大规模图的可扩展性**：分布推斥损失和图重构的计算代价阻碍了在数千万节点图上的应用，设计 O(N) 或 O(N log N) 的近似机制是潜在研究方向。
3. **动态与流式图异常检测**：CER‑GOD 假设图结构固定，未涉及随时间演化的拓扑；将其扩展至动态图需要重新考虑掩码更新和增量聚类。
4. **聚类组件的自适应性**：当前聚类数目固定为 2，且难以自动合并不同异常模式对应的簇；自动化确定聚类数目或开发自适应合并策略可提升对复杂异常模式的捕获能力。
5. **多样性损失的通用性**：ε 的固定值在某些数据集上可能过强或过弱，学习自适应的 ε 或设计新的防坍缩机制可能进一步稳定训练。
6. **超参数调节的自动化**：α、β 仍需人工设定，如何在无验证集的情况下自动平衡重建、聚类和推斥损失，是提升易用性的关键方向。



## 原文 PDF

![[paperPDFs/ICLR_2026/Escaping_the_Homophily_Trap_A_Threshold_free_Graph_Outlier_Detection_Framework_via_Clustering_guided_Edge_Reweighting.pdf]]
