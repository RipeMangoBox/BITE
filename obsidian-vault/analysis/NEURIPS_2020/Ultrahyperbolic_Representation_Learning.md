---
title: "Ultrahyperbolic Representation Learning"
type: paper
paper_level: A
venue: NeurIPS
year: 2020
pdf_ref: paperPDFs/NEURIPS_2020/Ultrahyperbolic_Representation_Learning.pdf
code_link: https://github.com/MarcTLaw/UltrahyperbolicRepresentation
project_link: https://github.com/MarcTLaw/UltrahyperbolicRepresentation
aliases:
- URL
tags:
- NEURIPS_2020
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "将表示空间从正定度量（黎曼）切换为不定度量（伪黎曼）的常曲率伪双曲面，即引入多个时间维度和空间维度，使度量张量同时允许正、负、零内积。"
primary_logic: "伪双曲面上测地线自然融合双曲、平直、球面三种情形，使得单个表示空间可以同时捕捉层次性和循环性关系；并提出一种利用不定度量的非正定性构造保证下降方向的新优化方法。"
claims:
- "在Zachary空手道俱乐部数据集上，超双曲表示（Q_{-1}^{3,1} 和 Q_{-1}^{2,2}）首次领袖排名达到1.2±0.4，显著优于所有基线流形。"
- "在NIPS合著数据集（4维表示）上，Spearman ρ 达到0.667（Q_{-1}^{2,2}），而双曲（Q_{-1}^{4,0}）仅有0.460，提升超过0.2。"
- "在NIPS合著数据集（6维表示）上，Spearman ρ 达到0.688（Q_{-1}^{3,3}），而双曲仅有0.455，提升约0.233。"
- "NIPS co-authorship dataset (4-dim) 上 Spearman's ρ (whole dataset) = 0.667 (Q_{-1}^{2,2})"
---

# Ultrahyperbolic Representation Learning

> [!tip] 核心洞察
> 伪双曲面上测地线自然融合双曲、平直、球面三种情形，使得单个表示空间可以同时捕捉层次性和循环性关系；并提出一种利用不定度量的非正定性构造保证下降方向的新优化方法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 超双曲表示学习 |
| 英文题名 | Ultrahyperbolic Representation Learning |
| 会议/期刊 | NeurIPS 2020 |
| Links | [paper](https://arxiv.org/abs/2007.00211) · [GitHub](https://github.com/MarcTLaw/UltrahyperbolicRepresentation) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | Ultrahyperbolic Representation Learning |
| Dataset | NIPS co-authorship dataset (4-dim), NIPS co-authorship dataset (6-dim) |

> [!tip] 效果简介
> - NIPS co-authorship dataset (4-dim) 上，Spearman's ρ (whole dataset) 为 0.667 (Q_{-1}^{2,2})，对比 0.460 (hyperbolic Q_{-1}^{4,0})，变化 +0.207。
> - NIPS co-authorship dataset (6-dim) 上，Spearman's ρ (whole dataset) 为 0.688 (Q_{-1}^{3,3})，对比 0.455 (hyperbolic Q_{-1}^{6,0})，变化 +0.233。

## 概要

现有主流表示学习范式（欧氏空间、双曲空间、球面流形）均建立在正定度量（黎曼）之上，每种空间只能刻画单一曲率类型的几何结构。然而，现实世界的图数据往往同时包含**层次性树状结构**和**循环结构**，单一正定度量无法统一表示这两种关系模式——这正是本文所识别的核心瓶颈。

为解决该问题，本文提出**超双曲表示学习**，将表示空间从正定度量切换为不定度量（伪黎曼）的**常曲率伪双曲面**。该流形引入多个时间维度和空间维度，其度量张量同时允许正、负、零内积，使得测地线自然融合双曲、平直、球面三种情形，从而在单一表示空间中同时捕捉层次性与循环性关系。在此基础上，作者给出了测地线、指数映射、对数映射的闭式解，并设计了一种利用不定度量非正定性构造保证下降方向的伪黎曼优化方法。

实验验证了该框架的有效性：
- 在Zachary空手道俱乐部数据集上，超双曲表示首次将领袖排名提升至1.2±0.4，显著优于所有基线流形；
- 在NIPS合著数据集的4维表示上，超双曲表示（Q_{-1}^{2,2}）的Spearman ρ达到0.667，相较双曲表示（Q_{-1}^{4,0}）的0.460提升超过0.2；
- 在6维表示上，Spearman ρ进一步提升至0.688（Q_{-1}^{3,3}），而双曲表示仅为0.455。

消融实验表明，当图中存在循环时，具有至少一个时间维度和至少两个空间维度的超双曲流形（q≥1, p≥2）显著优于纯双曲或纯球面流形。此外，所提出的伪黎曼优化器能在低维流形上满足所有约束，而基于欧氏映射的替代方案则无法做到。

该方法的主要局限在于：对数映射在⟨x,y⟩_q ≥ |β|时未定义，论文采用连续线性近似作为替代；测地线预度量d_γ不满足三角不等式，可能影响需要严格度量性质的下游任务；训练时间较长（NIPS数据集4维表示需约10小时），难以直接扩展到大规模图。开放问题包括如何自动确定最优的时间/空间维度配比，以及该框架向度量学习、生成模型等任务的推广。



### 表示学习中的几何空间选择困境

现代表示学习的核心任务之一是将图结构数据嵌入到连续的向量空间中，使得嵌入点之间的几何关系能够反映原始图的结构性质。这一过程中，**嵌入空间的几何类型**直接决定了模型能够捕捉何种结构模式。目前主流的几何空间选择可分为三类：

- **欧氏空间**（ℝᵈ）：平坦、无曲率，是最基础的嵌入空间，但对具有非平凡拓扑结构（如层次化或循环结构）的图数据表达能力有限。
- **双曲空间**（如庞加莱球、洛伦兹双曲面）：具有常负曲率，天然适合建模**树状层次结构**，因为双曲空间中距离沿树根到叶子的方向呈指数增长。然而，双曲空间无法有效表示图中的**循环结构**。
- **球面空间**：具有常正曲率，适合建模**循环或对称关系**，但对层次结构的表达能力不足。

### 核心瓶颈：单一正定度量无法统一层次与循环

上述三类空间的共同特征在于：它们都是**黎曼流形**，其度量张量是**正定**的。正定度量要求所有非零切向量的内积严格大于零，这导致流形上任意两点间的测地线只具有单一的行为模式——在双曲情形下是指数发散，在球面情形下是周期闭合，在欧氏情形下是线性延伸。

然而，真实世界的图数据往往**同时包含层次性和循环性**。例如：
- 社交网络中既存在社区内部的紧密循环连接，也存在跨社区的层级化结构；
- 引文网络中既有论文间的相互引用环，也有领域间的层级包含关系；
- 知识图谱中实体间的关系既可能形成环状依赖，也可能构成分类层次。

当图数据同时具有树状层次和循环结构时，单一曲率类型的正定度量流形必然在某一类结构的表示上产生扭曲。**这一瓶颈的本质在于：正定度量只能刻画一种曲率类型，无法在同一空间中同时容纳双曲、平直和球面三种测地线行为。**

### 本文动机：引入不定度量与伪黎曼流形

针对上述瓶颈，本文提出将表示空间从正定度量的黎曼流形切换为**不定度量（伪黎曼）的常曲率伪双曲面**。具体而言，本文引入伪欧氏空间 ℝ^{p,q+1}（具有 q+1 个时间维度和 p 个空间维度）中的**伪双曲面** 𝒬_β^{p,q}，其定义为：

$$\mathcal{Q}_{\beta}^{p,q} = \left\{ \mathbf{x} \in \mathbb{R}^{p,q+1} : \| \mathbf{x} \|_q^2 = \beta \right\}$$

其中伪欧氏内积为：

$$\langle \mathbf{a}, \mathbf{b} \rangle_q = -\sum_{i=0}^{q} a_i b_i + \sum_{j=q+1}^{p+q} a_j b_j = \mathbf{a}^{\top} \mathbf{G} \mathbf{b}$$

这一空间的关键特性在于：**度量张量 G 具有不定符号（既包含 -1 也包含 +1）**，因此切向量的内积可正、可负、可零。这使得伪双曲面上的测地线能够**统一三种行为模式**（公式 5）：

$$\gamma_{\mathbf{x}\to\pmb{\xi}}(t) = \begin{cases} \cosh(\dots)\mathbf{x} + \dots \sinh(\dots)\pmb{\xi} & \text{if } \langle \pmb{\xi}, \pmb{\xi}\rangle_q > 0 \\ \mathbf{x} + t \pmb{\xi} & \text{if } \langle \pmb{\xi}, \pmb{\xi}\rangle_q = 0 \\ \cos(\dots)\mathbf{x} + \dots \sin(\dots)\pmb{\xi} & \text{if } \langle \pmb{\xi}, \pmb{\xi}\rangle_q < 0 \end{cases}$$

- 当切向量内积为正时，测地线呈**双曲型**（指数发散），适合建模层次关系；
- 当切向量内积为零时，测地线呈**平直型**（线性延伸），对应欧氏行为；
- 当切向量内积为负时，测地线呈**球面型**（周期闭合），适合建模循环关系。

**核心洞察**：通过引入多个时间维度（q+1 ≥ 1）和多个空间维度（p ≥ 2），伪双曲面 𝒬_β^{p,q} 成为一个**超双曲流形**（ultrahyperbolic manifold），它自然地将双曲、平直和球面三种几何融合于单一表示空间之中，从而能够同时捕捉图中的层次性和循环性关系。

### 优化挑战与解决方向

在不定期量流形上进行表示学习面临一个根本性的优化难题：**由于度量张量不定，目标函数的梯度方向不能直接作为下降方向使用**。实验表明，直接使用伪黎曼梯度 -Df(x) 作为搜索方向会导致算法不收敛。为此，本文需要设计一种利用不定度量非正定性来**构造保证下降方向**的伪黎曼优化方法，这是实现超双曲表示学习的关键技术环节。



## 核心方法与创新机理

### 瓶颈与因果开关

现有主流表示学习依赖正定度量（黎曼流形），如欧氏空间、双曲空间和球面空间，它们各自只能刻画单一曲率类型的几何结构。然而，真实世界的图数据往往同时包含层次性（树状）结构和循环结构——例如社交网络中的层级社区与闭合三角关系——单一曲率空间无法统一表示这两种拓扑特征。这一瓶颈的根源在于正定度量张量强制所有方向上的内积符号一致，从而排除了混合曲率行为的可能性。

本工作的因果开关是将表示空间从正定度量切换为**不定度量（伪黎曼度量）**，具体构造为常曲率伪双曲面 $\mathcal{Q}_{\beta}^{p,q}$。该流形嵌入在伪欧氏空间 $\mathbb{R}^{p,q+1}$ 中，其度量张量由伪欧氏内积

$$\langle \mathbf{a}, \mathbf{b} \rangle_q = -\sum_{i=0}^{q} a_i b_i + \sum_{j=q+1}^{p+q} a_j b_j = \mathbf{a}^{\top} \mathbf{G} \mathbf{b}$$

诱导，其中 $q+1$ 个时间维度和 $p$ 个空间维度使得内积可以取正、负或零值。这一设计使得单个表示空间能够同时容纳双曲、平直和球面三种测地线行为，从而统一捕捉层次性与循环性关系。

### 核心洞察：测地线统一与度量泛化

伪双曲面上的测地线 $\gamma_{\mathbf{x}\to\pmb{\xi}}(t)$ 根据切向量 $\pmb{\xi}$ 的伪范数符号自然分化为三种情形：

$$\gamma_{\mathbf{x}\to\pmb{\xi}}(t) = \begin{cases} \cosh(\dots)\mathbf{x} + \dots \sinh(\dots)\pmb{\xi} & \text{if } \langle \pmb{\xi}, \pmb{\xi}\rangle_q > 0 \\ \mathbf{x} + t \pmb{\xi} & \text{if } \langle \pmb{\xi}, \pmb{\xi}\rangle_q = 0 \\ \cos(\dots)\mathbf{x} + \dots \sin(\dots)\pmb{\xi} & \text{if } \langle \pmb{\xi}, \pmb{\xi}\rangle_q < 0 \end{cases}$$

这三种情形分别对应双曲型、平直型和球面型测地线，使得同一流形上的不同区域可以展现截然不同的几何行为。这一统一表达是超双曲表示区别于所有单一曲率黎曼流形的根本数学机制。

基于测地线弧长，论文定义了对称预度量 $\mathsf{d}_{\gamma}$ 作为相似性函数的基础，并在对数映射未定义时（$\langle \mathbf{x},\mathbf{y}\rangle_q \geq |\beta|$）引入连续近似 $\mathsf{D}_{\gamma}$ 以覆盖整个流形。虽然 $\mathsf{d}_{\gamma}$ 不满足三角不等式，但实验表明其足以支撑图嵌入的软最大化排序损失优化。

### 方法槽位变更

| 方法槽位 | 基线方案 | 本文方案 | 变更依据 |
|----------|----------|----------|----------|
| **度量张量** | 正定（黎曼） | 不定（伪黎曼），常非零曲率 | pseudo-Riemannian manifolds of constant nonzero curvature not previously considered in machine learning（Section 1） |
| **相似性/距离函数** | 欧氏距离或双曲距离 | 基于弧长和半径函数的测地线预度量 $\mathsf{d}_{\gamma}$ 及连续近似 $\mathsf{D}_{\gamma}$（公式8, 9） | We define our dissimilarity function based on the general notion of arc length and radius function（Section 3） |
| **优化方法** | 黎曼梯度下降 | 伪黎曼梯度下降，利用不定度量的非正定性构造保证下降方向 | our pseudo-Riemannian optimizer manages to learn representations that satisfy all the constraints（Section 5） |

### 优化方法的非平凡创新

在伪黎曼流形上优化并非平凡推广。伪黎曼梯度定义为环境伪欧氏梯度的正交投影：

$$D f(\mathbf{x}) = \Pi_{\mathbf{x}}(\mathbf{G} \nabla f(\mathbf{x})) = \mathbf{G} \nabla f(\mathbf{x}) - \frac{\langle \mathbf{G} \nabla f(\mathbf{x}), \mathbf{x} \rangle_q}{\langle \mathbf{x}, \mathbf{x} \rangle_q} \mathbf{x}$$

由于度量张量不定，直接使用 $-D f(\mathbf{x})$ 作为搜索方向会导致算法不收敛（Part 009 实验证据）。论文提出了一种在不定内积下仍能保证下降的搜索方向选择策略，结合指数映射 $\exp_{\mathbf{x}}(-\eta \chi)$ 将更新后的点保持在流形上。消融实验表明，该伪黎曼优化器能在低维流形（如 $\mathcal{Q}_{-1}^{4,1}$、$\mathcal{Q}_{-1}^{4,2}$）上成功学习满足所有约束的表示，而基于欧氏映射的替代优化方法（Section 4.1 的微分同胚法）则无法做到。

### 实验验证的核心主张

1. **层次提取能力**：在 Zachary 空手道俱乐部数据集上，超双曲表示（$\mathcal{Q}_{-1}^{3,1}$ 和 $\mathcal{Q}_{-1}^{2,2}$）首次领袖排名达到 $1.2 \pm 0.4$，显著优于所有基线流形（Table 1，置信度 0.95）。

2. **循环图的层次提取**：在 NIPS 合著数据集上，4 维超双曲表示（$\mathcal{Q}_{-1}^{2,2}$）的 Spearman $\rho$ 达到 0.667，而纯双曲（$\mathcal{Q}_{-1}^{4,0}$）仅为 0.460，提升超过 0.2（Table 2，置信度 0.98）。6 维表示（$\mathcal{Q}_{-1}^{3,3}$）进一步提升至 0.688，对比纯双曲（$\mathcal{Q}_{-1}^{6,0}$）的 0.455，提升约 0.233（Table 3，置信度 0.98）。

3. **时间维度的必要性**：消融实验表明，当图中存在循环时，具有至少一个时间维度和至少两个空间维度的超双曲流形（$q \geq 1, p \geq 2$）显著优于纯双曲或纯球面流形，验证了不定度量的核心价值。

### 局限性与开放问题

- 对数映射在 $\langle \mathbf{x},\mathbf{y}\rangle_q \geq |\beta|$ 时未定义，当前线性近似可能非最优；分段测地线（broken geodesic）是潜在改进方向。
- 测地线预度量 $\mathsf{d}_{\gamma}$ 不满足三角不等式，可能影响需要严格度量性质的下游任务。
- 训练时间较长（NIPS 数据集 4 维表示约需 10 小时，12 GB NVIDIA TITAN V），难以直接扩展到大规模图。
- 如何根据数据自动确定最优的时间/空间维度分配（$p, q$）仍是开放问题。



超双曲表示学习（Ultrahyperbolic Representation Learning）的整体流程围绕一个核心范式展开：**将图节点嵌入到具有不定度量（伪黎曼）的常曲率伪双曲面 $\mathcal{Q}_{\beta}^{p,q}$ 上，并通过专门设计的伪黎曼优化算法学习嵌入，使该单一表示空间能够同时捕捉图中的层次性和循环性结构**。整个 pipeline 由三个关键模块串联而成：节点嵌入初始化、软最大化损失计算、伪黎曼优化步。

### 输入输出流

- **输入**：一个图 $\mathcal{G} = (V, E)$，其中节点集合 $V$ 和边集合 $E$ 可蕴含层次树状结构、循环结构或二者的混合。
- **输出**：每个节点 $v_i$ 在伪双曲面 $\mathcal{Q}_{\beta}^{p,q}$ 上的嵌入向量 $\mathbf{x}_i$，其中 $p$ 为空间维度数，$q+1$ 为时间维度数，$\beta < 0$ 为固定曲率参数。这些嵌入满足：高权重边对应的节点对在流形上的相似性值更小（即更“近”）。

### 模块关系与流程

**模块1：节点嵌入初始化**
在伪双曲面的正极点附近生成随机初始点，并将其投影到流形上。具体而言，先在伪欧氏空间 $\mathbb{R}^{p,q+1}$ 中采样随机向量 $\mathbf{z}_i$，然后通过归一化投影得到初始嵌入：
$$\mathbf{x}_i = \frac{\sqrt{|\beta|} \mathbf{z}_i}{\sqrt{|\|\mathbf{z}_i\|_q^2|}} \in \mathcal{Q}_{\beta}^{p,q}$$
这一初始化策略确保所有嵌入点从一开始就严格位于伪双曲面上，且集中在正极点附近，为后续优化提供稳定的起点。

**模块2：软最大化损失计算**
基于所选的相似性函数（测地线预度量 $\mathsf{d}_{\gamma}$ 或其连续近似 $\mathsf{D}_{\gamma}$），构建软最大化（softmax）排序损失：
$$\min_{\mathbf{x}_i \in \mathcal{Q}_{\beta}^{p,q}} \sum_{e_k=(v_i,v_j)\in E} -\log \frac{\exp(-\mathsf{d}(\mathbf{x}_i,\mathbf{x}_j)/\tau)}{\sum_{(v_a,v_b)\in \mathcal{W}(e_k)\cup \{e_k\}} \exp(-\mathsf{d}(\mathbf{x}_a,\mathbf{x}_b)/\tau)}$$
其中 $\mathcal{W}(e_k)$ 为负采样边集合，$\tau$ 为温度参数。该损失函数强制正边对的相似性值小于负边对，从而将图的拓扑结构编码到流形的几何关系中。

**模块3：伪黎曼优化步**
这是整个框架的核心创新之一。由于伪双曲面的度量张量是不定的（非正定），传统的黎曼梯度下降无法直接保证收敛。论文提出了一种**保证下降方向的伪黎曼优化算法**（Algorithm 1），其关键步骤为：
1. 计算环境伪欧氏梯度 $\nabla f(\mathbf{x})$ 并乘以度量矩阵 $\mathbf{G}$ 得到 $\mathbf{G}\nabla f(\mathbf{x})$；
2. 通过正交投影得到流形上的伪黎曼梯度 $D f(\mathbf{x})$：
$$D f(\mathbf{x}) = \Pi_{\mathbf{x}}(\mathbf{G} \nabla f(\mathbf{x})) = \mathbf{G} \nabla f(\mathbf{x}) - \frac{\langle \mathbf{G} \nabla f(\mathbf{x}), \mathbf{x} \rangle_q}{\langle \mathbf{x}, \mathbf{x} \rangle_q} \mathbf{x}$$
3. 沿保证目标函数下降的切方向 $\boldsymbol{\chi}$，以步长 $\eta$ 通过指数映射更新嵌入：
$$\mathbf{x} \leftarrow \exp_{\mathbf{x}}(-\eta \boldsymbol{\chi})$$
指数映射 $\exp_{\mathbf{x}}$ 由测地线 $\gamma_{\mathbf{x}\to\boldsymbol{\xi}}(t)$ 在 $t=1$ 时给出，确保更新后的点始终落在伪双曲面上。

### 关键设计决策

- **相似性函数的选择**：测地线预度量 $\mathsf{d}_{\gamma}$ 基于弧长定义，是对称预度量但不满足三角不等式。当对数映射未定义时（即 $\langle \mathbf{x}, \mathbf{y} \rangle_q \geq |\beta|$），采用连续线性近似 $\mathsf{D}_{\gamma}$ 进行扩展。这一设计使得相似性计算在整个流形上都有定义，但线性近似区域可能引入误差。
- **优化方向的确定**：直接使用 $-D f(\mathbf{x})$ 作为搜索方向在不定度量下不收敛（实验证实），因此需要额外的方向修正策略来保证每次迭代目标函数值下降。论文在 Algorithm 1 中给出了具体的方向选择逻辑。
- **时间与空间维度的配置**：伪双曲面 $\mathcal{Q}_{\beta}^{p,q}$ 的签名 $(p, q+1)$ 决定了流形的几何特性。当 $q \geq 1$ 且 $p \geq 2$ 时，流形上的测地线可同时呈现双曲、平直和球面三种类型，从而统一表达层次性和循环性。维度配置 $(p, q+1)$ 是超参数，需要根据数据特性手动设定。

### 与基线方法的本质差异

| 组件 | 欧氏/双曲/球面基线 | 超双曲方法 |
|------|-------------------|-----------|
| 度量张量 | 正定（黎曼） | 不定（伪黎曼），常曲率 |
| 表示空间 | 单一曲率类型 | 统一融合三种曲率类型 |
| 相似性函数 | 欧氏距离或双曲距离 | 基于弧长和半径函数的测地线预度量及连续近似 |
| 优化方法 | 标准黎曼梯度下降 | 针对不定度量设计的保证下降方向的伪黎曼优化 |

整个框架的输入输出流和模块关系如下图所示（基于论文 Figure 1 和 Figure 2 的几何直觉）：

**图 → 嵌入初始化（正极点附近投影）→ 相似性计算（测地线预度量/连续近似）→ 损失评估（软最大化排序损失）→ 伪黎曼梯度投影 → 指数映射更新 → 收敛后的超双曲嵌入**



### 1. 度量基础：伪欧氏内积与伪双曲面

超双曲表示学习的底层几何空间是伪欧氏空间 ℝ^{p,q+1}，其中包含 q+1 个时间维度和 p 个空间维度。其核心运算为**伪欧氏内积**（标量积），定义为：

$$\langle \mathbf{a}, \mathbf{b} \rangle_q = -\sum_{i=0}^{q} a_i b_i + \sum_{j=q+1}^{p+q} a_j b_j = \mathbf{a}^{\top} \mathbf{G} \mathbf{b}$$

其中度量矩阵 **G** = diag(−1, …, −1, 1, …, 1) 具有不定符号（q+1 个负特征值，p 个正特征值）。这一内积不再正定——同一向量可与自身内积为正、负或零——这是伪黎曼几何区别于黎曼几何的根本特征。

在此空间上，**伪双曲面**（pseudo-hyperboloid）被定义为具有固定伪范数 β 的超曲面：

$$\mathcal{Q}_{\beta}^{p,q} = \{ \mathbf{x} \in \mathbb{R}^{p,q+1} : \| \mathbf{x} \|_q^2 = \beta \}$$

其中 ‖x‖_q^2 = ⟨x, x⟩_q。当 β < 0 时，该流形具有常负截面曲率，且其切空间上的正交投影算子为：

$$\Pi_{\mathbf{x}}(\mathbf{z}) = \mathbf{z} - \frac{\langle \mathbf{z}, \mathbf{x} \rangle_q}{\langle \mathbf{x}, \mathbf{x} \rangle_q} \mathbf{x}$$

该投影将环境空间中的任意向量 **z** 映射到 **x** 点处的切空间 T_x Q_β^{p,q}，是后续梯度计算和优化步的基础。

### 2. 测地线与指数/对数映射

伪双曲面上测地线的核心洞见在于：**切向量的内积符号决定了测地线的几何类型**。给定点 x ∈ Q_β^{p,q} 和切向量 ξ ∈ T_x Q_β^{p,q}，测地线 γ_{x→ξ}(t) 具有统一的分段闭式表达：

$$\gamma_{\mathbf{x}\to\pmb{\xi}}(t) = \begin{cases} \cosh\left(\frac{t \sqrt{|\langle \pmb{\xi}, \pmb{\xi} \rangle_q|}}{\sqrt{|\beta|}}\right)\mathbf{x} + \frac{\sqrt{|\beta|}}{\sqrt{|\langle \pmb{\xi}, \pmb{\xi} \rangle_q|}} \sinh\left(\frac{t \sqrt{|\langle \pmb{\xi}, \pmb{\xi} \rangle_q|}}{\sqrt{|\beta|}}\right)\pmb{\xi} & \text{if } \langle \pmb{\xi}, \pmb{\xi}\rangle_q > 0 \\ \mathbf{x} + t \pmb{\xi} & \text{if } \langle \pmb{\xi}, \pmb{\xi}\rangle_q = 0 \\ \cos\left(\frac{t \sqrt{|\langle \pmb{\xi}, \pmb{\xi} \rangle_q|}}{\sqrt{|\beta|}}\right)\mathbf{x} + \frac{\sqrt{|\beta|}}{\sqrt{|\langle \pmb{\xi}, \pmb{\xi} \rangle_q|}} \sin\left(\frac{t \sqrt{|\langle \pmb{\xi}, \pmb{\xi} \rangle_q|}}{\sqrt{|\beta|}}\right)\pmb{\xi} & \text{if } \langle \pmb{\xi}, \pmb{\xi}\rangle_q < 0 \end{cases}$$

三种情形分别对应双曲型（类时切向量，内积 > 0）、平直型（类光切向量，内积 = 0）和球面型（类空切向量，内积 < 0）测地线。这一统一表达使得单个表示空间可以同时捕捉层次性（双曲分量）和循环性（球面分量）。

基于测地线，**指数映射**将切向量映射回流形上的点：

$$\exp_{\mathbf{x}}(\pmb{\xi}) = \gamma_{\mathbf{x}\to\pmb{\xi}}(1)$$

其逆运算**对数映射**在邻域 U_x 内将流形点映射回切向量：

$$\log_{\mathbf{x}}(\mathbf{y}) = \begin{cases} \frac{\cosh^{-1}\left(\frac{\langle \mathbf{x}, \mathbf{y} \rangle_q}{\beta}\right)}{\sqrt{\left(\frac{\langle \mathbf{x}, \mathbf{y} \rangle_q}{\beta}\right)^2 - 1}} \left(\mathbf{y} - \frac{\langle \mathbf{x}, \mathbf{y} \rangle_q}{\beta} \mathbf{x}\right) & \text{if } \frac{\langle \mathbf{x}, \mathbf{y} \rangle_q}{|\beta|} < -1 \\ \mathbf{y} - \mathbf{x} & \text{if } = -1 \\ \frac{\cos^{-1}\left(\frac{\langle \mathbf{x}, \mathbf{y} \rangle_q}{\beta}\right)}{\sqrt{1 - \left(\frac{\langle \mathbf{x}, \mathbf{y} \rangle_q}{\beta}\right)^2}} \left(\mathbf{y} - \frac{\langle \mathbf{x}, \mathbf{y} \rangle_q}{\beta} \mathbf{x}\right) & \text{if } \in (-1, 1) \end{cases}$$

对数映射的定义域受限于 ⟨x, y⟩_q / β 的取值区间；当该比值 ≥ 1 时（即两点“太远”），对数映射未定义，这构成了后续相似性函数设计的关键约束。

### 3. 相似性函数：从测地线预度量到连续近似

基于弧长，论文首先定义了**测地线预度量** d_γ：

$$\mathsf{d}_{\gamma}(\mathbf{x}, \mathbf{y}) = \sqrt{|\,\|\log_{\mathbf{x}}(\mathbf{y})\|_q^2\,|} = \begin{cases} \sqrt{|\beta|}\cosh^{-1}\left(\frac{\langle \mathbf{x}, \mathbf{y} \rangle_q}{\beta}\right) & \text{if } \frac{\langle \mathbf{x}, \mathbf{y} \rangle_q}{|\beta|} < -1 \\ 0 & \text{if } = -1 \\ \sqrt{|\beta|}\cos^{-1}\left(\frac{\langle \mathbf{x}, \mathbf{y} \rangle_q}{\beta}\right) & \text{if } \in (-1, 1) \end{cases}$$

该函数是对称的，但不满足三角不等式，因此只是预度量（premetric）而非真正的距离度量。其根本局限在于：当 ⟨x, y⟩_q ≥ |β| 时，对数映射未定义，d_γ 因此存在盲区。

为解决这一问题，论文提出了**连续近似相似性函数** D_γ，将对数映射未定义区域的相似性值用线性外推补全：

$$\mathsf{D}_{\gamma}(\mathbf{x}, \mathbf{y}) = \begin{cases} \mathsf{d}_{\gamma}(\mathbf{x}, \mathbf{y}) & \text{if } \langle \mathbf{x}, \mathbf{y} \rangle_q \leq 0 \\ \sqrt{|\beta|}\left(\frac{\pi}{2} + \frac{\langle \mathbf{x}, \mathbf{y} \rangle_q}{|\beta|}\right) & \text{otherwise} \end{cases}$$

当内积 ≤ 0 时，D_γ 退化为 d_γ；当内积 > 0（且可能超过 |β|）时，D_γ 采用线性近似，在 ⟨x, y⟩_q = 0 处与 d_γ 连续拼接。该设计使得相似性函数在整个流形上处处有定义，是后续图嵌入损失计算的基础。

### 4. 伪黎曼优化：下降方向与流形约束

在伪双曲面上优化目标函数 f 时，需要解决两个问题：**如何定义梯度**，以及**如何保证更新后的点仍在流形上**。

**伪黎曼梯度** Df(x) 是环境伪欧氏梯度 G∇f(x) 在切空间上的正交投影：

$$D f(\mathbf{x}) = \Pi_{\mathbf{x}}(\mathbf{G} \nabla f(\mathbf{x})) = \mathbf{G} \nabla f(\mathbf{x}) - \frac{\langle \mathbf{G} \nabla f(\mathbf{x}), \mathbf{x} \rangle_q}{\langle \mathbf{x}, \mathbf{x} \rangle_q} \mathbf{x}$$

这一投影确保梯度位于 T_x Q_β^{p,q} 内。然而，由于内积的不定性，直接使用 −Df(x) 作为搜索方向并不能保证目标函数下降——这是伪黎曼优化与标准黎曼优化的关键区别。论文提出了一种**保证下降的搜索方向选择机制**（Algorithm 1），其核心是根据 ⟨Df(x), ξ⟩_q 的符号自适应调整步长符号，确保每次指数映射更新后损失降低：

$$\mathbf{x} \leftarrow \exp_{\mathbf{x}}(-\eta \, \chi)$$

其中 χ 为经过符号校正的搜索方向，η 为步长。消融实验证实，直接使用 −Df(x) 作为搜索方向时算法不收敛，而该伪黎曼优化器能在低维流形（如 Q_{-1}^{4,1}、Q_{-1}^{4,2}）上成功学习满足所有约束的表示。

### 5. 图嵌入损失函数

给定图 G = (V, E) 和边权重，节点嵌入的学习目标是最小化以下软最大化排序损失：

$$\min_{\mathbf{x}_i \in \mathcal{Q}_{\beta}^{p,q}} \sum_{e_k=(v_i,v_j)\in E} -\log \frac{\exp(-\mathsf{d}(\mathbf{x}_i,\mathbf{x}_j)/\tau)}{\sum_{(v_a,v_b)\in \mathcal{W}(e_k)\cup \{e_k\}} \exp(-\mathsf{d}(\mathbf{x}_a,\mathbf{x}_b)/\tau)}$$

其中 d(·,·) 为所选相似性函数（D_γ 或 d_γ），τ 为温度参数，W(e_k) 为负采样边集合。该损失鼓励高权重边具有较小的相似性值（即节点在流形上更接近），是跨流形表示学习的统一优化目标。



## 实验与关键发现

### 核心实验设计

实验在两个具有不同结构特征的图数据集上评估超双曲表示学习：**Zachary空手道俱乐部**（小规模社交网络，包含层次性与循环结构）和 **NIPS合著数据集**（大规模学术合作网络，具有明显的层次社区结构）。评估指标为 **Spearman ρ** 和 **平均倒数排名（MRR）**，衡量学到的节点嵌入距离与图最短路径距离之间的秩相关性。所有流形使用相同的 softmax 损失函数（公式 17）和相似的随机初始化策略，但相似性函数因流形度量不同而自然差异。

### 主实验结果

#### Zachary空手道俱乐部（Table 1）

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2007_00211/figures/004_Table_1.jpg]]
*Table 1: Evaluation scores for the different learned representations (mean ± standard deviation)*

在 3 维表示空间中，超双曲流形在“第一领袖排名”指标上取得突破性表现：**Q_{-1}^{2,1}** 和 **Q_{-1}^{1,2}** 分别达到 1.2 ± 0.4 和 1.2 ± 0.4，显著优于所有传统黎曼流形（双曲 Q_{-1}^{3,0} 为 2.0 ± 0.0，球面 Q_{-1}^{0,3} 为 2.6 ± 0.5）。该结果表明，超双曲表示能更准确地捕捉图中同时存在的层次性和循环性关系——这是单一正定度量流形无法实现的。

#### NIPS合著数据集 4 维表示（Table 2）

![[assets/figures/papers/paper_list_l41_https_arxiv_org_abs_2007_00211/figures/005_Table_2.jpg]]
*Table 2: Evaluation scores for the different learned representations lying on 4-dimensional manifolds on the NIPS dataset Table 3: Evaluation scores for the different learned representations lying on 6-dimensional manifolds on the NIPS dataset*

超双曲流形 **Q_{-1}^{2,2}** 在全局 Spearman ρ 上达到 **0.667**，相比纯双曲流形 Q_{-1}^{4,0} 的 0.460 提升 **0.207**（相对提升约 45%）。值得注意的是，Q_{-1}^{2,2} 同时超越了球面流形 Q_{-1}^{0,4}（0.591）和欧氏空间（0.586），验证了不定度量在捕捉复杂图结构时的综合优势。

#### NIPS合著数据集 6 维表示（Table 3）

当表示维度提升至 6 维时，超双曲流形 **Q_{-1}^{3,3}** 取得全局最优 Spearman ρ **0.688**，而纯双曲 Q_{-1}^{6,0} 仅为 0.455，差距进一步扩大至 **0.233**（相对提升约 51%）。这一趋势表明，增加时间维度和空间维度的均衡配置能持续增强模型对层次性与循环性的联合建模能力。

### 消融分析：时间维度与空间维度的作用

实验系统性地探索了不同 (p, q) 配置对性能的影响，揭示了关键的结构性规律：

- **循环结构需要时间维度**：当图中存在循环时，至少需要一个时间维度（q ≥ 1）和至少两个空间维度（p ≥ 2）的超双曲流形显著优于纯双曲或纯球面流形。例如，在 NIPS 数据集上，Q_{-1}^{2,2}（Spearman ρ 0.667）远优于 Q_{-1}^{4,0}（0.460）和 Q_{-1}^{0,4}（0.591）。
  
- **维度配置的均衡性**：在总维度固定的情况下，时间维度与空间维度的均衡分配（如 Q_{-1}^{2,2} 优于 Q_{-1}^{3,1} 和 Q_{-1}^{1,3}）通常带来更优性能，这暗示真实世界图数据中的层次性和循环性关系往往需要对称的表示容量。

### 优化方法的必要性验证

消融实验直接对比了两种优化策略：

- **伪黎曼梯度下降**（Section 4.2）：能在低维流形（如 Q_{-1}^{4,1}、Q_{-1}^{4,2}）上成功学习满足所有约束的表示。
- **欧氏映射方法**（Section 4.1）：基于微分同胚将优化映射到欧氏空间，但无法使嵌入点满足流形约束，导致表示质量下降。

此外，实验证实直接使用 **-Df(x)** 作为搜索方向时算法不收敛——这是不定度量的关键特性：伪黎曼梯度的负方向不一定是下降方向。论文提出的保证下降方向选择机制（Algorithm 1）是优化成功的必要条件。

### 计算效率与局限性

尽管超双曲表示在精度上取得显著提升，但训练时间较长：NIPS 数据集上 4 维表示需约 **10 小时**（使用 12 GB NVIDIA TITAN V GPU）。这一开销源于测地线计算和不定度量优化的复杂性，限制了当前方法在大规模图上的直接扩展。

### 关键图表结论

- **Figure 3（左）** 展示了 Zachary 空手道俱乐部的图结构，其包含天然的层次性（俱乐部分裂为两个社区）和循环性（成员间的多重交互），是验证超双曲表示能力的理想测试场景。
- **Figure 3（右）** 的损失曲线显示，具有时间维度的超双曲流形（q ≥ 1）收敛到更低的损失值，且收敛稳定性优于纯双曲或纯球面流形，直接反映了不定度量对图结构建模的适配性。



## 定位与知识库关联

### 1. 对现有表示空间的突破

现有图表示学习方法主要依赖三类几何空间：欧氏空间（ℝ^d）、双曲空间（如庞加莱球、洛伦兹模型）和球面空间。这些空间的共同特征是**度量张量均为正定（黎曼）**，因此只能刻画单一曲率类型的结构。具体而言：
- **双曲空间**（如 Q_{-1}^{p,0}）适合建模树状层次结构，但无法表示循环关系；
- **球面空间**（如 Q_{-1}^{0,q}）适合建模循环结构，但难以捕捉层次性；
- **欧氏空间**作为平直基线，对两类结构的表达能力均有限。

现实世界的图数据（如社交网络、合著网络）往往**同时包含层次化社区结构和局部循环**（如三元闭包、派系），单一正定度量空间无法统一表示这种混合拓扑。本文的核心突破在于将表示空间从黎曼流形切换为**伪黎曼流形**，具体采用常曲率伪双曲面 Q_β^{p,q}（β < 0），其度量张量是不定的，同时包含 q+1 个时间维度和 p 个空间维度。这使得测地线自然融合双曲、平直、球面三种情形（公式 5），单个表示空间即可同时捕捉层次性和循环性。

### 2. 与相关工作的关系

#### 2.1 双曲表示学习

双曲表示学习（如 Nickel & Kiela, NIPS 2017 的庞加莱嵌入；Chami et al., ICML 2019 的洛伦兹图卷积网络）是本文最直接的前驱。这些方法在常负曲率黎曼流形上建模层次关系，在无循环的树状图（如 WordNet 上位词图）上表现优异。本文的超双曲流形可视为双曲流形的**严格推广**：当时间维度 q = 0 时，Q_β^{p,0} 退化为标准双曲面（洛伦兹模型）。因此，双曲表示学习是本文框架的特例。

#### 2.2 球面与欧氏表示学习

球面表示学习（如 Wilson et al., ICML 2014 的球面嵌入）在正曲率空间建模循环结构。欧氏空间（ℝ^d）作为最广泛使用的表示空间，是本文的平直基线。本文的实验系统对比了 Q_{-1}^{p,q} 与 Q_{-1}^{p+q,0}（双曲）、Q_{-1}^{0,p+q}（球面）及 ℝ^{p+q}（欧氏），证实了不定度量的优势。

#### 2.3 伪黎曼优化

伪黎曼流形上的优化在机器学习中几乎未被探索。本文的方法学贡献之一是**构造了保证下降的搜索方向**：由于不定度量的存在，直接使用负伪黎曼梯度 -Df(x) 作为搜索方向时不收敛（见消融实验），需要根据目标函数梯度与搜索方向的内积符号自适应调整步长符号。这一优化方法填补了伪黎曼流形上表示学习的技术空白。

#### 2.4 产品空间方法

近期工作（如 Gu et al., NeurIPS 2019）提出将双曲空间和球面空间的笛卡尔积作为表示空间，以分别捕捉层次和循环结构。本文的伪双曲面方法与之不同：**混合曲率行为内嵌于单个流形的测地线结构中**，而非通过乘积构造外在地组合不同空间。这避免了产品空间中各分量维度分配的超参数选择问题。

### 3. 适用边界与局限

#### 3.1 测地线“距离”的度量缺陷

本文定义的测地线预度量 d_γ（公式 8）是对称的，但**不满足三角不等式**，因此不是严格的度量。对于需要度量性质的下游任务（如基于距离的分类器、度量学习损失），这可能引入理论上的不一致性。论文未讨论这一缺陷对实际性能的影响。

#### 3.2 对数映射的未定义区域

当两点内积 ⟨x, y⟩_q ≥ |β| 时，对数映射未定义，论文采用连续线性近似 D_γ（公式 9）作为替代。这种近似在几何上并非最优——论文自身指出“broken geodesic”（分段测地线，经由 -x 中转）是可能的备选方案，但未实验验证。在表示学习中，若大量节点对落入该区域，近似误差可能累积。

#### 3.3 计算开销

NIPS 合著数据集上 4 维表示的训练时间约 10 小时（12 GB NVIDIA TITAN V），显著高于欧氏或双曲基线。这限制了该方法在大规模图（百万级节点）上的直接应用。计算瓶颈主要来自：
- 每次迭代需计算所有节点对的相似性（softmax 损失的分母）；
- 伪黎曼优化中步长符号的自适应选择增加了每次迭代的计算量。

#### 3.4 时间/空间维度的选择

论文未提供自动确定最优 (p, q) 的方法。实验中通过网格搜索（q = 0, 1, 2, 3）选择最佳配置，但这一过程依赖下游任务评估，缺乏先验指导原则。对于结构未知的真实图数据，如何高效选择维度分配仍是开放问题。

### 4. 开放问题

1. **自动维度分配**：能否从图的拓扑特征（如树宽、环的基序分布）推导最优的时间/空间维度比？这需要建立图结构与伪双曲面曲率之间的理论联系。

2. **分段测地线替代方案**：当对数映射未定义时，采用 broken geodesic（d_γ(x, -x) + d_γ(-x, y)）是否比线性近似更优？其计算开销与表示质量的权衡需实验验证。

3. **任务泛化性**：本文仅验证了图嵌入的层次提取任务。超双曲表示能否推广到节点分类、链接预测、图分类等标准图学习任务？在度量学习、生成模型（如 VAE 的潜在空间）中，不定度量的非正定性是否带来新的表达能力？

4. **可扩展优化**：能否借鉴双曲表示学习中的加速技术（如黎曼 Adam、负采样）来降低超双曲优化的计算成本？伪黎曼流形上的自适应优化器设计是一个待探索的方向。

5. **理论性质**：测地线预度量不满足三角不等式，这对表示学习的收敛性和泛化性有何理论影响？是否可以在伪双曲面上定义满足三角不等式的真度量？



## 原文 PDF

![[paperPDFs/NEURIPS_2020/Ultrahyperbolic_Representation_Learning.pdf]]
