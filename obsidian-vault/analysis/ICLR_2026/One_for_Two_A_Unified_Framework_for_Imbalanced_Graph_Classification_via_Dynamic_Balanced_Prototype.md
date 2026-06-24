---
title: "One for Two: A Unified Framework for Imbalanced Graph Classification via Dynamic Balanced Prototype"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/One_for_Two_A_Unified_Framework_for_Imbalanced_Graph_Classification_via_Dynamic_Balanced_Prototype.pdf
openreview_forum_id: MraQM41SNS
aliases:
- OTUFIGCDBP
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "通过信息瓶颈原理驱动的原型负载均衡，强制原型激活分布趋向均匀分布，使尾部图能公平参与原型学习，从而提升其判别性表征。"
primary_logic: "用一组可学习的原型以无偏方式从图实例中提取共享语义特征，并借助基于信息瓶颈的负载均衡约束防止多数类主导，最终利用这些原型增强尾部图的表征能力。"
claims:
- "UniImb 在极端类别不平衡的 PROTEINS 数据集上 Macro‑F1 达到 70.44%，较基础 GIN 提升约 45 个百分点；移除动态平衡原型模块后性能在所有消融变体中最差。"
- "移除原型负载均衡优化（w/o BalOpt）后模型性能明显下降，尤其在类别不平衡数据集上；同时理论推导证明最小化原型‑输入互信息等价于最小化 KL(P||U)，且当 U 为均匀分布时效果最优。"
- "在 6 个常用图分类数据集上，UniImb 在极端类别不平衡和极端拓扑不平衡设定下均取得最高 Macro‑F1 和 Micro‑F1，且通过 Wilcoxon 符号秩检验 (p<0.05) 证明提升显著。"
- "PROTEINS (extreme class imbalance) 上 Macro-F1 = 70.44 ± 4.72"
---

# One for Two: A Unified Framework for Imbalanced Graph Classification via Dynamic Balanced Prototype

> [!tip] 核心洞察
> 用一组可学习的原型以无偏方式从图实例中提取共享语义特征，并借助基于信息瓶颈的负载均衡约束防止多数类主导，最终利用这些原型增强尾部图的表征能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一分为二：基于动态平衡原型的统一不平衡图分类框架 |
| 英文题名 | One for Two: A Unified Framework for Imbalanced Graph Classification via Dynamic Balanced Prototype |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=MraQM41SNS); [GitHub](https://github.com/ALWAYS1815/iclr_UniImb) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | UniImb |
| Dataset | PROTEINS (extreme class imbalance), D&D (extreme class imbalance), PROTEINS (extreme topological imbalance) |

> [!tip] 效果简介
> - PROTEINS (extreme class imbalance) 上，Macro-F1 为 70.44 ± 4.72，对比 25.33 ± 7.53 (GIN)，变化 +45.11。
> - D&D (extreme class imbalance) 上，Macro-F1 为 46.63 ± 3.42，对比 9.99 ± 7.44 (GIN)，变化 +36.64。
> - PROTEINS (extreme topological imbalance) 上，Macro-F1 为 71.32 ± 1.88，对比 53.48 ± 2.03 (GIN)，变化 +17.84。

## 概述

图分类任务普遍存在**类别不平衡**（多数类样本远多于少数类）与**拓扑不平衡**（不同类别的图规模差异显著）两种数据偏差。现有方法通常仅针对单一类型的不平衡进行设计，难以应对两者交织的复杂场景。更关键的是，原型学习（prototype learning）在提取共享语义特征时，容易被多数类或大规模图样本主导，导致尾部图（少数类与小规模图）的表征质量严重下降——这是制约不平衡图分类性能的核心瓶颈。

针对上述问题，本文提出 **UniImb**，一个统一处理类别不平衡与拓扑不平衡的图分类框架。其核心思路是：引入一组可学习的**动态平衡原型（Dynamic Balanced Prototype, DBP）**，以无偏方式从图实例中提取共享语义特征；同时，基于**信息瓶颈（Information Bottleneck）原理**推导原型负载均衡正则项，强制原型激活分布趋近均匀分布，从而防止多数类主导，使尾部图能公平参与原型学习，最终提升其判别性表征能力。

在实验层面，UniImb 在 6 个常用图分类数据集上，于极端类别不平衡和极端拓扑不平衡两种设定下均取得最优的 Macro‑F1 与 Micro‑F1，且经 Wilcoxon 符号秩检验（p<0.05）验证提升显著。例如，在极端类别不平衡的 PROTEINS 数据集上，UniImb 的 Macro‑F1 达到 70.44%，较基础 GIN 提升约 45 个百分点；在 D&D 上同样提升超 36 个百分点。消融实验进一步证实，移除动态平衡原型模块或负载均衡优化均会导致性能明显退化，验证了所提机制的关键作用。

### 方法谱系与知识库定位

UniImb 处于图分类、不平衡学习与原型学习的交叉地带。相较于仅关注类别不平衡的方法（如 **G2GNN**、**ImGKB**、**DataDec**）或仅处理拓扑不平衡的方法（如 **SOLT‑GNN**、**ImbGNN**、**TopoImb**），UniImb 首次在统一框架下同时解决两类不平衡。与传统原型方法依赖聚类或静态分配不同，UniImb 通过信息瓶颈引导的原型负载均衡，实现了原型激活的公平分配，这与对比学习中的均匀性假设形成呼应，但将其引入到图级原型学习场景并给出了可微优化方案。在主干网络层面，UniImb 兼容 GIN、GCN、GraphSAGE 等经典 GNN，以及 GraphGPS、Exphormer 等图 Transformer，展现出良好的即插即用特性。

## 背景与动机

图分类是图机器学习的核心任务之一，在药物发现、分子性质预测、社交网络分析等领域具有广泛应用。然而，真实世界图数据普遍存在两类相互交织的不平衡问题：**类别不平衡**（不同类别样本数量悬殊）与**拓扑不平衡**（同一类别内图规模差异巨大）。前者的典型场景如罕见疾病蛋白结构预测，后者则常见于不同分子大小的化合物分类。当类别不平衡与拓扑不平衡同时出现时，少数类中的小规模图（尾部图）面临双重信息匮乏——不仅训练样本稀缺，其自身拓扑结构也过于简单，导致表征质量严重退化。

现有方法对此存在明显缺口。一方面，**G2GNN**、**ImGKB**、**DataDec** 等方法仅针对类别不平衡设计，通过重加权、重采样或合成少数类样本缓解分布偏移，但未考虑图拓扑结构的差异。另一方面，**SOLT‑GNN**、**ImbGNN**、**TopoImb** 等方法专注于拓扑不平衡，通过拓扑增强或迁移学习提升小图表征，却忽视了类别分布的影响。这种“分而治之”的策略无法应对两类不平衡交织的复杂场景。更深层的问题在于，原型学习（prototype learning）作为提取共享语义特征的有效手段，在训练过程中容易被多数类样本主导——原型激活分布向头部类别严重倾斜，尾部图难以公平参与原型学习，其判别性表征因此受损。

针对上述瓶颈，本文提出 **UniImb**，一个统一处理类别不平衡与拓扑不平衡的图分类框架。其核心动机在于：通过一组可学习的原型以无偏方式从图实例中提取共享语义特征，并借助信息瓶颈原理驱动的负载均衡约束，强制原型激活分布趋向均匀，从而确保尾部图获得与头部图同等的原型参与机会，最终提升其表征质量与分类性能。

## 核心创新

UniImb 的核心创新在于构建了一个**统一的不平衡图分类框架**，通过三个关键机制协同解决类别不平衡与拓扑不平衡交织的复杂场景，其设计逻辑围绕一个中心矛盾展开：**如何防止多数类（或大尺度图）在表征学习中系统性压制尾部图**。

### 创新一：动态平衡原型（DBP）——从“被主导”到“公平参与”

现有图分类方法在处理不平衡时，要么依赖重采样/重加权（仅针对类别不平衡），要么通过拓扑增强（仅针对拓扑不平衡），两者均未触及一个深层瓶颈：**图级表征的语义提取过程本身就被头部样本主导**。UniImb 引入一组可学习的原型向量 $\mathbf{S} \in \mathbb{R}^{\mathsf{K} \times d_h}$，通过 top‑k 注意力机制从所有图实例中提取共享语义特征：

$$\widetilde{\mathbf{H}}_{\mathrm{S}} = \mathrm{Softmax}\left(\mathrm{TopK}_1\left(\mathbf{S}\widetilde{\mathbf{H}}^{\top}/\sqrt{d_h}\right)\right)\widetilde{\mathbf{H}}\mathbf{W}_v$$

随后，采用 sigmoid 门控机制将最相关的原型特征注入图表示：

$$\widehat{\mathbf{H}} = \mathrm{Sigmoid}\left(\mathrm{TopK}_2\left(\widetilde{\mathbf{H}}\mathbf{S}^{\top}/\sqrt{d_h}+\eta\right)+\gamma\right)\widetilde{\mathbf{H}}_{\mathrm{s}}$$

其中 $\eta \in \mathbb{R}^{\mathsf{K}}$ 是可学习的调制系数，直接影响原型的激活优先级。**仅靠原型机制本身并不足以保证公平性**——在极端不平衡下，原型仍会被多数类样本“淹没”。因此，UniImb 的关键突破在于为原型学习引入了**基于信息瓶颈的负载均衡约束**。

### 创新二：信息瓶颈驱动的原型负载均衡——从“经验技巧”到“理论保障”

UniImb 将原型学习形式化为信息瓶颈目标：

$$\min \mathrm{I}(\mathbf{S};\mathbf{G}) - \beta \mathrm{I}(\mathbf{S};\mathbf{Y})$$

即最小化原型与输入图的互信息，同时最大化原型与标签的互信息。理论推导（Proposition 1, 2）表明，最小化 $\mathrm{I}(\mathbf{S};\mathbf{G})$ 等价于最小化原型激活分布 $\mathbf{P}$ 与先验分布 $\mathbf{U}$ 的 KL 散度 $\mathrm{KL}(\mathbf{P}\|\mathbf{U})$。当 $\mathbf{U}$ 为均匀分布时，该约束强制每个原型被等频激活，从而**从根本上阻止多数类独占原型资源**。

为实现可微优化，UniImb 设计了基于 stop‑gradient 的约束损失：

$$\mathcal{L}_M = \frac{1}{2}\sum_{k=1}^{\mathsf{K}}\left| \eta + \mathrm{StopGrad}(n_k - \eta) - \frac{2\cdot\mathrm{N}\cdot\mathrm{TopK}_2}{1/u_k} \right|^2$$

其中 $n_k$ 为原型 $k$ 的实际激活次数，$u_k$ 为目标均匀分布。当某原型激活次数超过平均水平时，$\eta$ 会施加惩罚以降低其后续优化中的激活优先级，形成**动态自校正的负载均衡闭环**。消融实验证实，移除该优化（w/o BalOpt）后性能显著下降，尤其在类别不平衡数据集上；且均匀分布先验在所有候选分布（Zipf、Exponential、Poisson、Uniform）中取得最优性能（Table 1）。

### 创新三：个性化图扰动与多尺度拓扑编码——从“统一扰动”到“图自适应增强”

传统图增强方法对所有图施加固定比例的边丢弃或节点掩码，忽略了不同图对扰动的敏感度差异。UniImb 提出**个性化可学习扰动策略**：根据图的平均度 $d^{\mathcal{G}_i}$ 自适应学习边丢弃概率 $a_e^{\mathcal{G}_i} = \sigma(\mathbf{MLP}(d^{\mathcal{G}_i}))$ 和特征掩码概率 $\beta_n^{\mathcal{G}_i}$。这使得稀疏的小规模图（尾部图）获得更温和的增强，而密集的大规模图接受更强的正则化，避免尾部图信息被过度破坏。

同时，UniImb 引入**多尺度拓扑编码**以弥补原始节点特征的拓扑盲区：局部编码采用 $z$ 步随机游走自返回概率 $\mathbf{LE}_j^{\mathcal{G}_i} = [(\mathbf{M}^{\mathcal{G}_i})_{j,j}, \ldots, (\mathbf{M}^{\mathcal{G}_i})_{j,j}^z]$；全局编码通过拉普拉斯特征谱的置换不变映射 $\mathbf{GE}^{\mathcal{G}_i} = \varphi([\ell(h_i, \lambda_i) + \ell(-h_i, \lambda_i)]_{i=1}^z)$ 捕获图级结构签名。消融实验表明，可学习的个性化扰动显著优于静态随机扰动及基于度数的 DoOA 方法。

### 创新总结：从单点修补到系统重构

| 设计维度 | 基线方法 | UniImb 创新 |
|---------|---------|------------|
| 不平衡处理范围 | 仅针对类别或拓扑单一类型 | 统一框架同时处理两类不平衡及其交织场景 |
| 原型学习机制 | 无专用原型，或原型被头部类别主导 | 动态平衡原型 + 信息瓶颈负载均衡，强制均匀激活 |
| 数据增强策略 | 统一随机扰动（固定比例） | 图平均度自适应的可学习个性化扰动 |
| 拓扑信息利用 | 仅原始节点特征或简单位置编码 | 局部随机游走 + 全局拉普拉斯谱的多尺度编码 |

**决定性证据**：在极端类别不平衡的 PROTEINS 数据集上，UniImb 的 Macro‑F1 达到 70.44%，较基础 GIN（25.33%）提升约 45 个百分点（Table 2）；移除 DBP 模块后性能在所有消融变体中最差（Figure 4），直接验证了原型均衡机制的核心地位。

## 整体框架

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/001_Figure_1.jpg]]
*Figure 1: The overall architecture of UniImb which enhances graph representations by extracting prototypical features in an uniform manner*

UniImb 提出了一种统一的图分类框架，旨在同时应对类别不平衡与拓扑不平衡交织的复杂场景。其核心设计思路是：通过多尺度拓扑编码与个性化图扰动增强单一图实例的表征质量，再借助动态平衡原型（Dynamic Balanced Prototype, DBP）以无偏方式从图实例中提取共享语义特征，最终利用这些原型增强尾部图（少数类与小规模图）的判别能力。

### Pipeline 总览

框架的整体处理流程如图 1 所示，由以下核心模块串联构成：

1. **多尺度拓扑编码**  
   对每个输入图 $\mathcal{G}_i$，分别提取局部与全局拓扑信息。局部编码 $\mathbf{LE}_j^{\mathcal{G}_i}$ 利用 $z$ 步随机游走自返回概率刻画节点的邻域结构；全局编码 $\mathbf{GE}^{\mathcal{G}_i}$ 则基于拉普拉斯矩阵的特征值与特征向量，经置换不变网络映射得到图级拓扑签名。

2. **个性化图扰动**  
   根据图的平均度 $\bar{d}^{\mathcal{G}_i}$ 自适应地学习边丢弃概率 $a_e^{\mathcal{G}_i}$ 与特征掩码概率 $\beta_n^{\mathcal{G}_i}$，通过伯努利采样向图结构与节点特征注入可控随机性。相比固定比例的随机扰动，该策略能根据图自身特性调节增强强度，提升数据多样性。

3. **GNN 图表示学习**  
   将拓扑编码与扰动后的节点特征输入 GIN 等主干网络，通过 $L$ 层邻域聚合生成图级别表示 $\widetilde{\mathbf{H}}$。在此过程中，局部拓扑编码也通过独立的 GNN 层进行深层更新，以捕获更高阶的拓扑模式。

4. **动态平衡原型 (DBP)**  
   一组可学习的原型嵌入 $\mathbf{S} \in \mathbb{R}^{\mathsf{K} \times d_h}$ 通过 top‑k 注意力机制从图表示中感知原型特征 $\widetilde{\mathbf{H}}_{\mathrm{S}}$，再以 sigmoid 门控方式选择最相关原型增强图表示 $\widehat{\mathbf{H}}$。该模块的核心在于原型负载均衡优化。

5. **原型负载均衡优化**  
   基于信息瓶颈原理，最小化原型与输入图之间的互信息 $\mathrm{I}(\mathbf{S};\mathbf{G})$，同时最大化原型与标签的互信息 $\mathrm{I}(\mathbf{S};\mathbf{Y})$。理论推导表明，最小化 $\mathrm{I}(\mathbf{S};\mathbf{G})$ 等价于最小化原型激活分布与均匀分布 $\mathbf{U}$ 的 KL 散度。为此，引入调制系数 $\eta$ 与 stop‑gradient 技巧，通过约束损失 $\mathcal{L}_M$ 强制每个原型的激活次数逼近均匀目标，防止多数类样本主导原型学习。

6. **特征混合与分类**  
   对增强后的图表示进行随机打乱与线性插值（Feature Mixup），进一步增加尾部图特征多样性。最后，取 $\widehat{\mathbf{H}}$ 的前 $N$ 行（对应 $N$ 个原始输入图）输入双层 MLP 解码器，生成类别预测 $\hat{\mathbf{Y}}$。

### 输入输出流

- **输入**：一批图实例 $\{\mathcal{G}_i\}_{i=1}^N$，每个图包含邻接矩阵与节点特征。
- **输出**：每个图的预测类别标签 $\hat{\mathbf{Y}}$。
- **关键中间表示**：多尺度拓扑编码拼接后的节点特征、GNN 生成的图表示 $\widetilde{\mathbf{H}}$、原型增强后的图表示 $\widehat{\mathbf{H}}$。

### 模块间关系

多尺度拓扑编码与个性化扰动构成“实例增强层”，为后续 GNN 提供更具判别力的输入特征；DBP 模块则作为“无偏语义提取层”，通过负载均衡约束确保头部与尾部图公平参与原型学习；原型增强后的表示经特征混合后送入分类器，形成端到端的统一优化框架。消融实验表明，移除 DBP 模块后性能在所有变体中最差，验证了原型建模在框架中的核心地位。

## 核心模块与公式推导

UniImb 的核心由三个协同模块构成：**多尺度拓扑编码**、**个性化图扰动**，以及**动态平衡原型 (DBP)**。前两者为图实例注入丰富的结构与多样性信息，DBP 则通过信息瓶颈原理驱动的负载均衡机制，确保尾部图公平参与原型学习，从而提升其判别性表征。

### 多尺度拓扑编码

为捕获图的结构信息，UniImb 同时建模局部与全局拓扑特征。

**局部拓扑编码** 基于随机游走矩阵的自返回概率。对于图 $\mathcal{G}_i$ 中的节点 $v_j$，定义 $z$ 步随机游走矩阵 $\mathbf{M}^{\mathcal{G}_i}$，其局部编码为各步自返回概率的拼接：

$$
\mathbf{LE}_j^{\mathcal{G}_i} = [(\mathbf{M}^{\mathcal{G}_i})_{j,j}, (\mathbf{M}^{\mathcal{G}_i})_{j,j}^2, \ldots, (\mathbf{M}^{\mathcal{G}_i})_{j,j}^z] \in \mathbb{R}^z
$$

该向量刻画了节点邻域的局部连通性，计算复杂度低，仅需关注对角元素。

**全局拓扑编码** 利用图拉普拉斯矩阵的特征值与特征向量。取前 $z$ 个特征对 $(h_i, \lambda_i)$，经置换不变网络 $\varphi$ 映射：

$$
\mathbf{GE}^{\mathcal{G}_i} = \varphi\left([\ell(h_i, \lambda_i) + \ell(-h_i, \lambda_i)]_{i=1}^z\right)
$$

其中 $\ell(\cdot)$ 为可学习的特征变换函数。该编码对节点重编号具有不变性，为图表示提供全局结构先验。

### 个性化图扰动

传统数据增强采用固定概率的随机边丢弃或节点掩码，忽略了图实例间的拓扑差异。UniImb 提出**自适应扰动策略**：根据图的平均度 $\bar{d}^{\mathcal{G}_i}$，通过 MLP 学习个性化的边丢弃概率 $a_e^{\mathcal{G}_i}$ 和特征掩码概率 $\beta_n^{\mathcal{G}_i}$：

$$
a_e^{\mathcal{G}_i} = \sigma(\mathbf{MLP}(\bar{d}^{\mathcal{G}_i})), \quad m_e \sim \mathcal{B}(a_e^{\mathcal{G}_i})
$$
$$
\beta_n^{\mathcal{G}_i} = \sigma(\mathbf{MLP}(\bar{d}^{\mathcal{G}_i})), \quad m_n \sim \mathcal{B}(\beta_n^{\mathcal{G}_i})
$$

边丢弃掩码 $m_e$ 控制每条边的保留概率，特征掩码 $m_n$ 控制节点特征维度的置零概率。该策略使稀疏图与密集图采用不同强度的扰动，增强数据多样性的同时避免破坏关键结构。

### 动态平衡原型 (DBP)

DBP 是 UniImb 的核心创新，包含原型感知、原型增强与负载均衡三个子机制。

**原型感知**：设可学习原型矩阵 $\mathbf{S} \in \mathbb{R}^{\mathsf{K} \times d_h}$，图表示矩阵为 $\widetilde{\mathbf{H}}$。通过 top‑k 注意力从图表示中提取原型特征：

$$
\widetilde{\mathbf{H}}_{\mathrm{S}} = \mathrm{Softmax}\left(\mathrm{TopK}_1\left(\mathbf{S}\widetilde{\mathbf{H}}^{\top}/\sqrt{d_h}\right)\right)\widetilde{\mathbf{H}}\mathbf{W}_v
$$

其中 $\mathrm{TopK}_1$ 仅保留注意力矩阵每列的前 $k_1$ 个最大值，强制每个原型仅关注最相关的图实例。

**原型增强**：采用 sigmoid 门控机制，选择与每个图最相关的原型来增强其表示：

$$
\widehat{\mathbf{H}} = \mathrm{Sigmoid}\left(\mathrm{TopK}_2\left(\widetilde{\mathbf{H}}\mathbf{S}^{\top}/\sqrt{d_h} + \eta\right) + \gamma\right)\widetilde{\mathbf{H}}_{\mathrm{S}}
$$

其中 $\eta \in \mathbb{R}^{\mathsf{K}}$ 为可学习的调制系数，直接影响注意力的生成过程；$\gamma$ 为偏置项。

**原型负载均衡优化**：核心挑战在于避免多数类图主导原型学习。UniImb 从信息瓶颈原理出发，最小化原型与输入图的互信息 $\mathrm{I}(\mathbf{S};\mathbf{G})$，同时最大化原型与标签的互信息 $\mathrm{I}(\mathbf{S};\mathbf{Y})$：

$$
\min \mathrm{I}(\mathbf{S};\mathbf{G}) - \beta \mathrm{I}(\mathbf{S};\mathbf{Y})
$$

理论推导表明（Proposition 1, 2），最小化 $\mathrm{I}(\mathbf{S};\mathbf{G})$ 等价于最小化原型激活分布 $\mathbf{P}$ 与先验分布 $\mathbf{U}$ 的 KL 散度 $\mathrm{KL}(\mathbf{P}\|\mathbf{U})$。当 $\mathbf{U}$ 为均匀分布时，该约束强制每个原型被等概率激活，从而防止头部类主导。

为实现可微优化，引入 stop‑gradient 技巧构造负载均衡损失 $\mathcal{L}_M$：

$$
\mathcal{L}_M = \frac{1}{2}\sum_{k=1}^{\mathsf{K}}\left| \eta_k + \mathrm{StopGrad}(n_k - \eta_k) - \frac{2 \cdot \mathrm{N} \cdot \mathrm{TopK}_2}{1/u_k} \right|^2
$$

其中 $n_k$ 为第 $k$ 个原型的实际激活次数，$u_k$ 为目标分布（均匀分布时 $u_k = 1/\mathsf{K}$）。$\eta_k$ 的更新规则为 $\eta_k \leftarrow \eta_k - \phi \cdot \mathrm{sgn}(n_k - 2 \cdot \mathrm{N} \cdot \mathrm{TopK}_2 \cdot u_k)$，当某原型激活次数超出平均水平时，$\eta_k$ 被惩罚以降低其后续激活优先级。

消融实验证实，均匀分布先验在所有候选分布（Zipf、Exponential、Poisson、Uniform）中取得最佳性能（Table 1），移除负载均衡优化（w/o BalOpt）后模型性能显著下降（Figure 4），验证了该机制的有效性。

## 实验与分析

### 核心性能验证

#### 极端类别不平衡

在六个常用图分类数据集上，UniImb 在极端类别不平衡设定下全面超越现有方法。Table 2 的结果显示，以 GIN 为骨干时，UniImb 在 PROTEINS 上的 Macro‑F1 达到 **70.44%**，较基础 GIN（25.33%）提升约 45 个百分点；在 D&D 上达到 **46.63%**，较 GIN（9.99%）提升超过 36 个百分点。这一提升幅度表明，仅靠 GNN 骨干本身几乎无法从严重倾斜的标签分布中学习尾部类别的判别特征，而 UniImb 的原型均衡机制有效逆转了该趋势。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/003_Table_2.jpg]]
*Table 2: Performance on class imbalance datasets with extreme imbalance degree. The best results are marked and the runner-ups are underlined . We report the average and standard deviation over 20 runs. Numbers marked with * indicate that the improvement is statistically significant compared with the best baseline (Wilcoxon Signed-Rank Test with p-value \< 0.05)*

与专门处理类别不平衡的方法相比，UniImb 同样保持显著优势：在 PROTEINS 上较 **ImGKB** 和 **G2GNN** 分别高出约 10–30 个 Macro‑F1 百分点。值得注意的是，UniImb 在提升尾部类别性能的同时并未牺牲头部类别——Micro‑F1 在 REDDIT‑B 上达到 **88.82%**，说明整体分类质量同步改善。所有结果均经过 20 次独立运行，并通过 Wilcoxon 符号秩检验（p<0.05）确认统计显著性。

#### 极端拓扑不平衡

在拓扑不平衡场景下（Table 3），UniImb 同样取得最优性能。以 PROTEINS 为例，Macro‑F1 达到 **71.32%**，较 GIN（53.48%）提升约 18 个百分点，且优于 **SOLT‑GNN**、**ImbGNN** 和 **TopoImb** 等专为拓扑不平衡设计的方法。这验证了动态平衡原型模块对不同不平衡类型的统一适应能力——原型负载均衡不仅对类别分布敏感，也能有效缓解图规模差异带来的表征偏差。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/004_Table_3.jpg]]
*Table 3: Performance comparison on topological imbalance datasets with extreme imbalance degree*

#### 交织不平衡与大规模场景

在同时存在类别与拓扑不平衡的交织场景下，UniImb 的优势进一步扩大（Table 5），表明两类不平衡并非独立问题，而 UniImb 的统一框架能从机制层面协同处理。在大规模真实数据集 AirGraph 上（Figure 2），UniImb 在性能与效率之间取得最佳折衷：其 Macro‑F1 显著高于 **GraphGPS**、**Exphormer** 和 **Graph‑Mamba** 等先进架构，同时推理时间仅略高于轻量级 GIN，验证了原型机制的计算效率优势。

### 消融实验与机制验证

Figure 4 的消融实验揭示了各模块的因果贡献：

- **移除动态平衡原型模块（w/o DBP）**：性能在所有消融变体中最差，尤其在类别不平衡数据集上下降最为剧烈。这直接证明了原型建模是不可替代的核心组件——缺乏原型时，模型退化为普通 GNN，完全丧失对尾部图的增强能力。
- **移除原型负载均衡优化（w/o BalOpt）**：性能明显下降，且下降幅度在类别不平衡场景下更为显著。这说明仅引入原型而不施加均衡约束，原型仍会被多数类样本主导，无法实现公平表征。
- **移除可学习扰动策略（w/o Perturb）**：性能亦有下降，但幅度小于前两者，表明个性化数据增强是有效的辅助手段，但非决定性因素。

Table 1 进一步验证了负载均衡先验分布的选择：均匀分布（Uniform）在所有四种候选分布（Zipf、Exponential、Poisson）中取得最优性能。这与论文的理论推导一致——最小化原型‑输入互信息等价于最小化 KL(P‖U)，当 U 为均匀分布时，强制原型激活趋向等概率，最大程度抑制多数类主导。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/002_Table_1.jpg]]
*Table 1: Macro-F1 and Micro-F1 scores on class imbalance datasets with extreme imbalance degree under different U distributions. The best results are marked and the runner-ups are underlined*

扰动策略的细化消融（Figures 9, 10）表明，基于图平均度自适应的可学习边丢弃与特征掩码策略，优于固定比例的随机扰动和基于度数的 DoOA 方法，验证了个性化扰动设计的必要性。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/030_Figure_9.jpg]]
*Figure 9: Ablation experiments on class-imbalance (upper half) and topological-imbalance (lower half), evaluated by Macro-F1 score. Figure 10: Ablation experiments on class-imbalance (upper half) and topological-imbalance (lower half), evaluated by Micro-F1 score*

### 泛化性与鲁棒性

UniImb 具备良好的骨干网络泛化性（Table 4）：当 GIN 替换为 GCN 或 GraphSAGE 时，UniImb 仍能带来一致的性能增益，说明原型均衡机制独立于具体 GNN 架构。原型数量 K 的敏感性分析（Figure 5）显示，性能在较宽的 K 值范围内保持稳定，表明方法对超参数不敏感，易于实际部署。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/009_Figure_5.jpg]]
*Figure 5: Sensitivity study on class imbalance (upper) and topological imbalance (lower). (d) After DBP Figure 6: Representation visualization on the PROTEINS dataset with extreme imbalance degree*

### 局限与待验证问题

尽管实验覆盖了 19 个数据集和三种不平衡设定，以下局限仍需注意：

1. **异质图泛化**：所有实验均在同质图上进行，方法在包含多种节点/边类型的异质图上的有效性未经检验。
2. **任务范围**：当前仅评估图分类任务，尚未扩展到节点级不平衡学习、少样本图学习或动态图场景。
3. **真实世界多样性**：大规模验证仅依赖 AirGraph 的污染预测任务，更多样化的真实分布（如社交网络、生物网络）有待覆盖。
4. **原型数量极端情况**：当 K 极大时，信息瓶颈近似的保真度与计算效率之间的平衡尚未系统研究。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/010_Figure.jpg]]

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/021_Table_14.jpg]]
*Table 14: Macro-F1 and Micro-F1 score on class imbalance datasets with extreme imbalance degree. The best results are marked and the runner-ups are underlined . We report the average and standard deviation over 20 runs*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/022_Table_15.jpg]]
*Table 15: Macro-F1 and Micro-F1 score on class imbalance datasets with medium imbalance degree*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/031_Figure_11.jpg]]
*Figure 11: Sensitivity study of TopK1 on class-imbalance (upper half) and topological-imbalance (lower half). Figure 12: Sensitivity study of $\mathrm { T o p K } _ { 2 }$ on class-imbalance (upper half) and topological-imbalance (lower half)*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/037_Figure_15.jpg]]
*Figure 15: Visualization analysis of prototype effects*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_MraQM41SNS/figures/015_Figure_7.jpg]]
*Figure 7: Distribution of Pollution Levels in the AirGraph Dataset: High (6.86%), Medium (42.84%), and Low (50.30%)*

## 方法谱系与知识库定位

### 1. 问题定位：从单一不平衡到交织不平衡

现有图分类研究在处理数据不平衡时，通常将**类别不平衡**与**拓扑不平衡**视为两个独立问题。类别不平衡方法（如 **G2GNN**、**ImGKB**、**DataDec**）聚焦于少数类样本的过采样或重加权，而拓扑不平衡方法（如 **SOLT-GNN**、**ImbGNN**、**TopoImb**）则关注图规模差异导致的表征偏差。然而，真实场景中这两类不平衡往往**交织出现**——少数类图通常同时具有较小的节点/边规模，使得单一策略难以奏效。

UniImb 的核心定位在于**首次将两类不平衡纳入统一框架**处理。其设计的动态平衡原型（DBP）模块不依赖类别标签先验，而是通过信息瓶颈原理强制原型激活分布趋向均匀，从而在机制层面同时缓解类别主导与规模主导的表征偏差。

### 2. 与现有方法的关键差异

#### 2.1 原型学习机制的革新

传统原型学习方法（如原型网络在少样本学习中的应用）通常直接基于样本特征计算原型，容易在类别不平衡场景下被头部类样本主导。UniImb 的 DBP 模块引入了两个关键改进：

- **Top-K 注意力感知**：通过 $\mathrm{TopK}_1$ 和 $\mathrm{TopK}_2$ 操作，从图表示中稀疏地提取原型特征并选择性增强，避免全局平均导致的特征稀释。
- **负载均衡正则化**：基于信息瓶颈理论推导出原型激活的均匀分布约束，通过可微的 stop-gradient 技术实现负载均衡，确保尾部图也能公平参与原型学习。

消融实验（Figure 4）表明，移除 DBP 模块后性能在所有变体中最差，移除负载均衡优化（w/o BalOpt）也在类别不平衡数据集上造成显著性能下降，验证了这两项设计的必要性。

#### 2.2 数据增强策略的差异化

现有图数据增强方法多采用**固定比例**的随机边丢弃或节点掩码（如 **GraphCL** 中的统一扰动）。UniImb 的个性化图扰动策略则根据图的**平均度**自适应学习边丢弃概率 $a_e^{\mathcal{G}_i} = \sigma(\mathbf{MLP}(d^{\mathcal{G}_i}))$ 和特征掩码概率，使增强强度与图自身拓扑特性匹配。消融实验（Figures 9, 10）显示该策略优于静态随机扰动及基于度数的 DoOA 方法。

#### 2.3 拓扑编码的互补性

UniImb 同时编码**局部**（随机游走自回归概率）与**全局**（拉普拉斯谱特征）拓扑信息，这与仅使用节点原始特征或简单位置编码的基线（如 **GIN**、**GraphGPS**）形成互补。多尺度拓扑编码为后续原型学习提供了更丰富的结构语义基础。

### 3. 方法适用边界与局限

#### 3.1 已验证的适用范围

- **同质图分类**：当前实验覆盖了 6 个常用基准数据集（PROTEINS、D&D、NCI1、REDDIT-B、COLLAB、IMDB-B）及大规模实际场景数据集 AirGraph，均属于同质图。
- **极端不平衡设定**：在类别不平衡（不平衡比 $\rho$ 达极端水平）和拓扑不平衡（训练集仅占 10%）下均取得最优性能，且通过 Wilcoxon 符号秩检验（$p<0.05$）验证提升显著。
- **主干网络兼容性**：与 GIN、GCN、GraphSAGE 等多种 GNN 主干结合均表现稳定（Table 4）。

#### 3.2 已知局限

1. **异质图泛化性未验证**：当前方法假设所有节点和边属于同一类型，未涉及包含多种节点/边类型的异质图场景。如何在异质图中定义与平衡原型仍需探索。
2. **任务类型受限**：仅在图分类任务上评估，尚未扩展到节点级不平衡学习、少样本图学习、动态图学习或图异常检测等场景。
3. **大规模原型效率**：原型数量 $K$ 的敏感性分析（Figure 5）显示性能对 $K$ 在合理范围内鲁棒，但当 $K$ 极大时，信息瓶颈近似的保真度与计算效率之间的平衡缺乏理论保证。

### 4. 开放问题

1. **跨任务迁移**：所提出的负载均衡策略能否直接推广到节点级或边级的不平衡学习任务？原型机制在非分类任务（如链接预测、图生成）中如何适配？
2. **异质图原型定义**：在包含多种节点/边类型的异质图中，如何定义具有语义意义的原型并保持公平性？是否需要为不同类型设计独立的原型空间？
3. **理论边界**：信息瓶颈目标 $\min I(\mathbf{S};\mathbf{G}) - \beta I(\mathbf{S};\mathbf{Y})$ 中，$\beta$ 的选取与原型数量 $K$、数据集规模之间存在怎样的理论关系？当 $K$ 趋近于样本数时，均匀分布约束是否仍能保持有效性？
4. **实际部署**：AirGraph 数据集上的性能与效率对比（Figure 2）初步展示了实际应用潜力，但在更多样化的真实世界分布（如社交网络、生物分子网络）中的表现有待进一步验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/One_for_Two_A_Unified_Framework_for_Imbalanced_Graph_Classification_via_Dynamic_Balanced_Prototype.pdf]]
