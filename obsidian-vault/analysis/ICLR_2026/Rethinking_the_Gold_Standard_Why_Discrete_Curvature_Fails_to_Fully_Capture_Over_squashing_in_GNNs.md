---
title: "Rethinking the Gold Standard: Why Discrete Curvature Fails to Fully Capture Over-squashing in GNNs?"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Rethinking_the_Gold_Standard_Why_Discrete_Curvature_Fails_to_Fully_Capture_Over_squashing_in_GNNs.pdf
project_link: null
code_link: null
openreview_forum_id: QYtmqCoilk
aliases:
- WAF3CW
- RGSWDCFFCOSG
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/graph_neural_networks
core_operator: "现有离散曲率的定义只依赖于边两端的一阶邻居关系（如三角形个数、Wasserstein距离），忽略了多跳传播时的度分布不均衡。通过引入度加权函数，可以纠正高度数节点对曲率的过度贡献。"
primary_logic: "高负曲率是过挤压的充分但不必要条件；许多过挤压边拥有较高的正曲率，因此仅依赖高负曲率检测过挤压会系统性地漏掉大量关键边。"
claims:
- "高负曲率是过挤压的充分但不必要条件。"
- "存在反例图族，其中边虽遭受严重过挤压，其离散曲率仍为高度正值。"
- "Ollivier–Ricci 曲率在实践中漏检了 30%～40% 的过挤压边。"
- "Cora (GCN, MOSR) 上 MOSR_10 = 0.000 (WAF3)"
---

# Rethinking the Gold Standard: Why Discrete Curvature Fails to Fully Capture Over-squashing in GNNs?

> [!tip] 核心洞察
> 高负曲率是过挤压的充分但不必要条件；许多过挤压边拥有较高的正曲率，因此仅依赖高负曲率检测过挤压会系统性地漏掉大量关键边。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 重新审视“黄金标准”：为何离散曲率无法完全捕捉GNN中的过挤压？ |
| 英文题名 | Rethinking the Gold Standard: Why Discrete Curvature Fails to Fully Capture Over-squashing in GNNs? |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=QYtmqCoilk) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/graph_neural_networks |
| Method | Weighted Augmented Forman-3 Curvature (WAF3) |
| Dataset | Cora (GCN, MOSR), Average over 21 datasets (GCN, SDRF rewiring (Texas), GNRF end-to-end (Texas) |

> [!tip] 效果简介
> - Cora (GCN, MOSR) 上，MOSR_10 为 0.000 (WAF3)，对比 0.030 (Ollivier Ricci)，变化 -0.030。
> - Average over 21 datasets (GCN, MOSR) 上，MOSR_10 mean 为 0.036 (WAF3)，对比 0.067 (Augmented Forman-3) / 0.271 (Ollivier Ricci)，变化 -0.031 / -0.235。
> - SDRF rewiring (Texas) 上，Accuracy 为 73.62±0.62 (WAF3)，对比 70.35±0.60 (Balanced Forman)，变化 +3.27。

## 概要

图神经网络（GNN）中的**过挤压（over‑squashing）**现象会严重损害信息在图中长距离传播的效率。离散曲率——尤其是 Ollivier‑Ricci 曲率——被广泛视为检测过挤压边的“黄金标准”，其核心直觉是：负曲率越高的边越容易发生信息瓶颈。然而，本文通过严格的理论分析与大规模实验，揭示了这一直觉的根本缺陷：**高负曲率是过挤压的充分条件，但并非必要条件**。换言之，大量遭受严重过挤压的边实际上拥有高度正曲率，仅依赖高负曲率进行检测会系统性地漏掉这些关键边。

这一核心洞察的因果机制在于：现有离散曲率定义（Ollivier‑Ricci、Balanced Forman、Augmented Forman‑3 等）仅考虑边两端节点的**一阶邻居紧密程度**（如共同邻居数、Wasserstein 距离），却忽略了多跳传播中因**度分布不均衡**导致的信息“稀释”效应。当高度数节点参与消息聚合时，来自远距离源节点的信号被大量邻居的噪声淹没，即使该边局部结构紧密、曲率为正，过挤压依然发生。

为量化曲率漏检的严重性，本文提出了 **Missed Over‑Squashing Ratio（MOSR）** 指标，用于衡量被曲率忽略的过挤压边比例。在 21 个真实数据集上的实验表明：Ollivier‑Ricci 曲率平均漏检了 **27%–40%** 的过挤压边，而表现最好的 Augmented Forman‑3 曲率也漏检了约 **7%–16%**。这些被忽略的边并非位于图的外围，而是大量集中在**集群内部**，承担着重要的桥接角色。

针对上述瓶颈，本文提出 **Weighted Augmented Forman‑3 Curvature（WAF3）**，其核心改动在于引入**度依赖权重函数** $f(d) = 1/(1+d)$，抑制高度数节点对曲率的过度贡献，从而更准确地反映多跳传播中的信息稀释。WAF3 在保持最低计算复杂度的同时，将平均 MOSR 降至 **0.036**，显著优于所有基线曲率。此外，通过将 WAF3 重写为加权 Jaccard 相似度的函数，并借助加权 MinHash 采样，本文设计了线性时间近似算法，可在 **23.8 秒**内完成 500 万边图的曲率计算，实现 **133.7 倍**加速。

在下游任务验证中，WAF3 驱动的图重连（SDRF）和端到端重连（GNRF）在多个数据集上均取得最优分类准确率，例如在 Texas 数据集上分别达到 **73.62%** 和 **87.11%**，较 Balanced Forman 曲率提升约 3–4 个百分点。

综上，本文的核心贡献可概括为三点：
1. **理论反例**：构造反例图族，严格证明离散曲率不是过挤压的必要条件；
2. **量化工具**：提出 MOSR 指标，首次系统量化曲率漏检的严重程度与漏检边的结构特征；
3. **实用方案**：提出 WAF3 及其高效近似算法，在检测精度与计算效率上均取得显著提升。



### 过挤压：GNN 信息传播的结构性瓶颈

消息传递神经网络（MPNN）已成为图表示学习的主流范式。其第 $l$ 层的更新规则为：

$$\mathbf { H } ^ { ( l + 1 ) } = \mathsf { R e L U } \left( \widetilde { \mathbf { A } } \mathbf { H } ^ { ( l ) } \mathbf { W } ^ { ( l ) } \right)$$

然而，当图中存在拓扑瓶颈时，来自远距离节点的信息在传播过程中会被指数级压缩，这种现象被称为**过挤压（over-squashing）**。从雅可比矩阵的角度看，过挤压表现为源节点 $s$ 到目标节点 $t$ 的雅可比范数 $\left\| \frac{\partial \mathbf{h}_t^{(L)}}{\partial \mathbf{h}_s^{(0)}} \right\|$ 过小，其下界由两端节点的度数 $a, b$ 决定：

$$\operatorname*{inf}_{N \in \mathbb{Z}^+} \left\| \frac{\partial \mathbf{h}_t^{(L)}}{\partial \mathbf{h}_s^{(0)}} \right\| = \phi_L(a, b)$$

其中 $\phi_L(a, b) = \prod_{l=0}^{L-1} \mathbf{W}^{(l)} \left( \frac{1}{a+1} + \frac{1}{b+1} \right)^{L-1} \frac{\rho}{\sqrt{(a+1)(b+1)}}$。这一下界揭示了过挤压与图拓扑之间的内在关联：度数不均衡的节点对会加剧信息流的衰减。

### 离散曲率作为“黄金标准”的局限

为检测和缓解过挤压，离散曲率（discrete curvature）被广泛用作拓扑瓶颈的代理指标。其核心直觉是：具有高负曲率的边连接着图的不同集群，构成信息传播的瓶颈。主流离散曲率包括：

- **Ollivier–Ricci 曲率**：基于最优传输理论，计算复杂度最高，但被认为是检测过挤压最精确的指标。
- **Balanced Forman 曲率**（Topping et al., 2021）：复杂度较低，计算效率优于 Ollivier–Ricci。
- **Augmented Forman-3 曲率（AF3）**：基于三角形计数，复杂度最低，定义为构成三角形的邻居数减去剩余一阶邻居数之差。

然而，本文的核心发现是：**高负曲率是过挤压的充分条件，但并非必要条件**。这意味着大量遭受严重过挤压的边可能拥有正值甚至高正值的离散曲率，从而被系统性漏检。

### 反例图族：正曲率下的严重过挤压

为证明上述论断，作者构造了一族反例图 $\mathcal{G}_{2,4}^{\mathtt{c}}$（Figure 1）。在该图族中，存在一些边虽然遭受严重的过挤压，其离散曲率却呈现高度正值。这一理论构造从根本上动摇了“高负曲率等价于过挤压”的直觉——离散曲率仅能反映一阶邻居的紧密程度，无法捕捉多跳传播中因度数分布不均衡导致的“信息稀释”效应。

### MOSR：量化曲率的漏检程度

为系统评估离散曲率的漏检问题，作者提出了**漏检过挤压比率（Missed Over-Squashing Ratio, MOSR）**：

$$\mathsf{MOSR}_q := \frac{\sum_{(u,v) \in \mathcal{E}} \mathbf{1}_{\mathsf{Curv}(u,v) \geq 0} \cdot \mathbf{1}_{\mathsf{JacoNorm}(u,v) \leq J_q}}{\sum_{(u',v') \in \mathcal{E}} \mathbf{1}_{\mathsf{JacoNorm}(u',v') \leq J_q}}$$

其中 $J_q$ 是雅可比范数的第 $q$ 百分位数。MOSR 直接量化了“被曲率判定为非负（即非瓶颈）的边中，有多少比例实际上是过挤压边”。

实验揭示了一个严峻的现实：**Ollivier–Ricci 曲率在实践中漏检了 30%～40% 的过挤压边**。在 21 个数据集上，当 $q=10$ 时，离散曲率漏检的过挤压边比例在 6.7% 到 38.6% 之间；$q=25$ 时，这一比例升至 7.9% 到 39.8%（Table 2）。值得注意的是，Augmented Forman-3 曲率虽然计算复杂度最低，其平均 MOSR（0.067）却显著优于 Ollivier–Ricci（0.271），说明更高阶的曲率定义并不必然带来更好的过挤压检测能力。

### 漏检的根源：集群内部 vs. 集群间边

通过引入边介数（edge betweenness）分析，作者进一步揭示了漏检的结构性原因。定义：

$$\mathsf{Between}(e) = \sum_{u \neq v \in \mathcal{V}} \frac{\sigma_{uv}(e)}{\sigma_{uv}}$$

并基于此定义 $\mathsf{BetwIden}_q$（被曲率识别的过挤压边的平均介数）、$\mathsf{BetwAll}$（所有边的平均介数）和 $\mathsf{BetwIgno}_q$（被曲率忽略的过挤压边的平均介数）。Table 3 的结果表明：

- 在大多数情况下，$\mathsf{BetwAll} > \mathsf{BetwIgno}$，说明被曲率忽略的过挤压边主要位于集群内部，而非连接不同集群的桥边。
- $\mathsf{BetwIden} > \mathsf{BetwAll}$，说明离散曲率仅能识别集群间的桥边，对集群内部的过挤压边几乎完全失效。

这一发现揭示了离散曲率的根本局限：它仅依赖一阶邻居的紧密程度（如三角形个数、Wasserstein 距离），无法反映多跳传播中因高度数节点导致的“信息稀释”效应。因此，大量处于集群内部的过挤压边因拥有较高的正曲率而被系统性忽略。

### 本文动机与贡献

基于上述分析，本文的动机明确：**需要一种既能保持计算高效性、又能更全面捕获过挤压边的离散曲率定义**。具体而言，本文的贡献包括：

1. 从理论上证明高负曲率是过挤压的充分而非必要条件，并构造反例图族加以验证。
2. 提出 MOSR 指标，首次系统量化离散曲率的漏检程度。
3. 通过边介数分析揭示漏检的结构性根源：集群内部边被忽略。
4. 提出加权扩展 Forman-3 曲率（WAF3），通过度依赖权重函数纠正高度数节点对曲率的不当贡献，并设计基于加权 MinHash 的线性时间近似算法。



## 核心方法与创新机理

### 问题重定义：曲率并非过挤压的必要条件

现有工作将离散曲率（尤其是高负曲率）视为检测消息传递神经网络中“过挤压”现象的“黄金标准”。本文通过理论分析和实证度量，系统性地挑战了这一假设，提出核心洞察：**高负曲率是过挤压的充分但不必要条件**。

这一洞察的因果瓶颈在于：现有离散曲率（Ollivier–Ricci、Balanced Forman、Augmented Forman‑3 等）的定义仅依赖于边两端的一阶邻居关系——如三角形个数或概率测度间的 Wasserstein 距离。这些定义天然倾向于将**连接不同集群的“桥边”**识别为高负曲率边，却无法反映多跳信息传播中的“稀释”效应。当一条边处于集群内部，两端节点的度分布严重不均衡时，信息流仍然可能因高度数节点的“吸收”效应而衰减，但该边的离散曲率却保持高度正值。

为严格证明这一缺陷，作者构造了一族反例图 $\mathcal{G}_{n,m}^c$（Definition 3），并证明其中存在边虽遭受严重过挤压，其离散曲率仍为高度正值。这一理论发现直接催生了新的评估视角：需要量化离散曲率究竟漏检了多少过挤压边。

### 关键度量：漏检过挤压比率（MOSR）

基于上述洞察，本文提出**Missed Over‑Squashing Ratio（MOSR）**作为评估离散曲率检测能力的新度量。MOSR 的定义直接锚定在雅可比范数（信息流强度的代理）与曲率符号的交叉统计上：

$$\mathsf{MOSR}_q := \frac{\sum_{(u,v) \in \mathcal{E}} \mathbf{1}_{\mathsf{Curv}(u,v) \geq 0} \cdot \mathbf{1}_{\mathsf{JacoNorm}(u,v) \leq J_q}}{\sum_{(u',v') \in \mathcal{E}} \mathbf{1}_{\mathsf{JacoNorm}(u',v') \leq J_q}}$$

其中 $J_q$ 为雅可比范数的第 $q$ 百分位数。MOSR 直接回答：在所有遭受过挤压的边中，有多少比例的边被离散曲率赋予了非负值（即被“忽略”）。

MOSR 的引入将曲率评估从间接的下游任务准确率提升，转变为**对曲率检测能力本身的直接量化**。实验表明，Ollivier–Ricci 曲率在 21 个数据集上的平均 MOSR₁₀ 高达 0.271，意味着超过四分之一的过挤压边被其忽略。

### 方法改进：加权扩展 Forman‑3 曲率（WAF3）

针对 MOSR 揭示的漏检问题，本文提出 **Weighted Augmented Forman‑3 Curvature（WAF3）**。其核心改进在于引入**度依赖权重函数**，修正高度数节点对曲率的不当贡献。

**Changed Slot：邻居节点贡献权重**

- **Baseline（AF3）**：所有一阶邻居等权贡献，即 $f(d) \equiv 1$。AF3 的计算本质上是“构成三角形的节点数”减去“剩余一阶邻居数”，高度数节点的贡献与低度数节点完全相同。
- **Proposed（WAF3）**：引入度依赖权重 $f(d) = 1/(1+d)$，抑制高度数节点的贡献。WAF3 的定义为：

$$\mathsf{WAF3}_f(u,v) := \sum_{i \in \mathcal{B}(u) \cap \mathcal{B}(v)} f(d_i) - \left( \sum_{i \in \mathcal{N}(u) \setminus \mathcal{B}(v)} f(d_i) + \sum_{i \in \mathcal{N}(v) \setminus \mathcal{B}(u)} f(d_i) \right)$$

其中 $\mathcal{B}(\cdot)$ 表示构成三角形的邻居集合。这一修正的动机源于理论分析：高度数节点在消息传递中会“稀释”信息流，但传统曲率却将其视为正面贡献。通过令 $f(+\infty) = 0^+$，WAF3 自动抑制了这种不当贡献。

**效果**：在 21 个数据集上，WAF3 的平均 MOSR₁₀ 降至 0.036，相比 AF3 的 0.067 降低了约 46%，相比 Ollivier–Ricci 的 0.271 降低了约 87%。

### 算法加速：基于加权 MinHash 的线性时间近似

WAF3 的另一个关键创新在于**可扩展性**。通过将 WAF3 重写为加权 Jaccard 相似度的函数（Theorem 6）：

$$\mathsf{WAF3}_f(u,v) = \frac{2}{f(u) + f(v)} \left( 2 - \frac{3}{1 + \mathrm{Jaccard}_f(\mathcal{N}(u), \mathcal{N}(v))} \right) \left( \sum_{i \in \mathcal{N}(u)} f(d_i) + \sum_{i \in \mathcal{N}(v)} f(d_i) \right)$$

其中 $\mathrm{Jaccard}_f(\mathcal{N}(u), \mathcal{N}(v)) := \frac{\sum_{i \in \mathcal{N}(u) \cap \mathcal{N}(v)} f(d_i)}{\sum_{i \in \mathcal{N}(u) \cup \mathcal{N}(v)} f(d_i)}$。

**Changed Slot：曲率计算的可扩展性**

- **Baseline**：精确计算复杂度为 $O(|E| d_{\max})$ 或更高，Ollivier–Ricci 甚至需要线性规划。
- **Proposed**：基于加权 MinHash 采样的近似算法（Algorithm 1），复杂度降至 $O(H|E|)$，其中 $H$ 为哈希函数数量。在 $H=100$ 时，近似 WAF3 与精确值之间的 Kendall Tau‑b 相似度约 95%，同时实现 **133.7 倍加速**。在 500 万边图上，计算仅需 23.8 秒。

这一加速使得 WAF3 成为第一个**可实际部署于大规模图**的过挤压检测曲率。

### 局限与待验证点

- WAF3 仍仅依赖一阶邻居局部结构，理论上不能保证完全检测所有过挤压边（曲率不是过挤压的必要条件）。
- 权重函数 $f(d)=1/(1+d)$ 为启发式选择，消融实验（Table 9）表明它优于 $(1+d)^{-2}$ 和 $(1+d)^{-1/2}$，但尚未证明其最优性。
- 近似算法引入了约 5% 的排序相似度损失，在精度敏感任务中需手动验证影响。
- 实验仅在同质无向图上进行，且限于 GCN、GAT、GraphSAGE 三种架构，普适性有待扩展。



![[assets/figures/papers/iclr26_0012_QYtmqCoilk_Rethinking_the_Gold_Standard_Why_Discrete_Curvat/figures/001_Table_1.jpg]]
*Table 1: We summarize all discrete curvatures defined on edges here. Curvatures defined on nodes (such as Bakry-Emery-Ricci ( ´ Mondal et al., 2024), combination (Kamtue, 2018), and node resistance (Devriendt & Lambiotte, 2022)) are not included. $\mu _ { u } ^ { \alpha }$ is the uniform distribution of the first-order neighbors of u with restart probability α. $W _ { 1 }$ is the 1-Wasserstein distance. $\{ w _ { u v } \}$ is the pseudoinverse of the weighted Laplacian matrix. $d _ { u }$ is the degree of node u , and $d _ { u } \vee d _ { v }$ : = $\operatorname$* { m a x } ( $d _ { u } , d _ { v } ) d _ { u } \wedge d _ { v }$ : = $\operatorname$* { m i n } ( $\bar { d } _ { u } , d _ { v }$ ) . $\bar { \bigtriangle...$

本文围绕“离散曲率作为过挤压检测工具”这一核心假设，构建了一个从理论质疑、量化评估到方法改进的完整分析流程。整体 pipeline 由四个关键模块串联而成：

### 1. 问题形式化：过挤压的雅可比刻画

首先将 MPNN 的信息流形式化为节点对之间的雅可比范数。给定 $L$ 层 MPNN：

$$\mathbf { H } ^ { ( l + 1 ) } = \mathsf { R e L U } \left( \widetilde { \mathbf { A } } \mathbf { H } ^ { ( l ) } \mathbf { W } ^ { ( l ) } \right)$$

在路径激活概率均匀的假设下，源节点 $\mathrm{s}$ 与目标节点 $\mathrm{t}$ 之间的雅可比下界可显式表达为：

$$\operatorname* { i n f } _ { N \in \mathbb { Z } ^ { + } } \bigg \vert \bigg \vert \frac { \partial \mathbf { h } _ { \mathrm { t } } ^ { ( L ) } } { \partial \mathbf { h } _ { \mathrm { s } } ^ { ( 0 ) } } \bigg \vert \bigg \vert = \phi _ { L } ( a , b )$$

其中 $\phi_L(a,b)$ 仅依赖于两端点度数 $a, b$、网络深度 $L$ 和权重范数。该下界揭示了过挤压的本质：信息在多跳传播中因高度数节点的“稀释”效应而衰减——这一衰减机制仅取决于端点度数，而与边的局部聚类结构（即离散曲率所捕捉的三角形密度）无必然联系。

### 2. 理论质疑：反例图族与 MOSR 度量

为证明离散曲率并非过挤压的必要条件，文章构造了反例图族 $\mathcal{G}_{n,m}^c$（Figure 1），并从理论上证明：在该图族中存在边，尽管遭受严重过挤压（雅可比范数极低），其离散曲率仍为高度正值。

在此基础上，提出 **Missed Over-Squashing Ratio (MOSR)** 作为核心评估指标：

$$\mathsf { M O S R } _ { q } : = \frac { \sum _ { ( u , v ) \in \mathcal { E } } \mathbf { 1 } _ { \mathsf { C u r v } ( u , v ) \geq 0 } \cdot \mathbf { 1 } _ { \mathsf { J a c o N o r m } ( u , v ) \leq J _ { q } } } { \sum _ { ( u ^ { \prime } , v ^ { \prime } ) \in \mathcal { E } } \mathbf { 1 } _ { \mathsf { J a c o N o r m } ( u ^ { \prime } , v ^ { \prime } ) \leq J _ { q } } }$$

其中 $J_q$ 为所有边雅可比范数的第 $q$ 百分位数。MOSR 量化了“被曲率误判为安全（非负曲率）但实际遭受过挤压”的边占真实过挤压边的比例。该指标将曲率检测能力与雅可比范数这一 ground-truth 信号直接对标，构成了整个评估框架的量化基础。

### 3. 曲率评估与诊断：从 MOSR 到边介数分析

基于 21 个数据集、3 种 GNN（GCN、GAT、GraphSAGE）和 3 种离散曲率（Ollivier–Ricci、Balanced Forman、Augmented Forman-3），系统计算 MOSR（Table 2）。核心发现：

- **Ollivier–Ricci 漏检最严重**：平均 MOSR₁₀ 达 0.271，在部分数据集上漏检 30%–40% 的过挤压边。
- **Augmented Forman-3 表现最优**：平均 MOSR₁₀ 为 0.067，但仍存在系统性漏检。
- **GCN 的 MOSR 最低**：相比 GAT 和 GraphSAGE，GCN 的雅可比范数分布与曲率判断的一致性更好。

为诊断漏检边的结构特征，引入 **边介数（Edge Betweenness）** 分析（Table 3）：

$$\mathsf{Between}(e) = \sum_{u \neq v \in \mathcal{V}} \frac{\sigma_{uv}(e)}{\sigma_{uv}}$$

定义三组统计量：$\mathsf{BetwIden}_q$（曲率识别边的平均介数）、$\mathsf{BetwAll}$（所有边的平均介数）、$\mathsf{BetwIgno}_q$（曲率忽略的过挤压边的平均介数）。结果表明：$\mathsf{BetwIden} > \mathsf{BetwAll} > \mathsf{BetwIgno}$ 在多数数据集中成立，揭示出离散曲率仅能识别**集群间桥接边**（高介数），而系统性地忽略**集群内部边**（低介数但同样遭受过挤压）。

### 4. 方法改进：WAF3 曲率与可扩展近似

基于上述诊断——高度数节点对曲率贡献不当是漏检的根源——提出 **Weighted Augmented Forman-3 (WAF3)** 曲率：

$$\mathsf { W A F 3 } _ { f } ( u , v ) : = \sum _ { i \in \mathcal { B } ( u ) \cap \mathcal { B } ( v ) } f ( d _ { i } ) - \left( \sum _ { i \in \mathcal { N } ( u ) / \mathcal { B } ( v ) } f ( d _ { i } ) + \sum _ { i \in \mathcal { N } ( v ) / \mathcal { B } ( u ) } f ( d _ { i } ) \right)$$

其中权重函数 $f(d) = 1/(1+d)$ 抑制高度数节点的贡献。AF3 是 $f \equiv 1$ 的特例。WAF3 将平均 MOSR₁₀ 从 AF3 的 0.067 降至 0.036（Table 4），在 Cora 上甚至达到 0.000。

为解决精确计算的复杂度瓶颈，利用 **Theorem 6** 将 WAF3 重写为加权 Jaccard 相似度的函数，进而通过 **加权 MinHash 采样**（Algorithm 1）实现 $O(H|E|)$ 的近似计算。在 $10^5$ 节点图上，$H=100$ 时加速 133.7 倍（Figure 3），Kendall Tau‑b 相似度维持在约 95%（Figure 4）。

最终，WAF3 被集成到两种图重连框架中验证下游效果：SDRF 重连下 Texas 准确率提升 3.27%（Table 10），GNRF 端到端模型中提升 3.96%（Table 11）。

### 输入输出流总结

```
原始图 → [雅可比范数计算] → 过挤压 ground-truth (J_q)
         → [离散曲率计算] → 曲率判断 (正/负)
              ↓
         MOSR 量化漏检比例
              ↓
         边介数诊断漏检边结构位置
              ↓
         WAF3 曲率 (加权抑制高度数节点)
              ↓
         MinHash 近似加速 (可选)
              ↓
         图重连 / 端到端训练
```

整个框架的瓶颈在于：现有离散曲率仅依赖一阶邻居的局部三角形结构，无法反映多跳传播中的度数稀释效应。WAF3 通过度加权部分缓解该问题，但本质上仍受限于一阶局部性——这是该 pipeline 的结构性局限，也是未来工作的开放方向。



### 过挤压的雅可比下界

MPNN 的第 $l$ 层消息传递定义为：

$$
\mathbf{H}^{(l+1)} = \mathsf{ReLU}\left( \widetilde{\mathbf{A}} \mathbf{H}^{(l)} \mathbf{W}^{(l)} \right) \tag{1}
$$

其中 $\widetilde{\mathbf{A}}$ 为归一化邻接矩阵，$\mathbf{W}^{(l)}$ 为可学习权重。在假设所有计算路径以相同概率 $\rho$ 被激活的前提下（Assumption 1），源节点 $\mathrm{s}$ 与目标节点 $\mathrm{t}$ 之间信息流的雅可比范数下界为：

$$
\inf_{N \in \mathbb{Z}^+} \left\| \frac{\partial \mathbf{h}_{\mathrm{t}}^{(L)}}{\partial \mathbf{h}_{\mathrm{s}}^{(0)}} \right\| = \phi_L(a, b) \tag{Lemma 2}
$$

其中 $a, b$ 分别为源、目标节点的度数，$\phi_L$ 的显式形式为：

$$
\phi_L(a, b) := \prod_{l=0}^{L-1} \mathbf{W}^{(l)} \left( \frac{1}{a+1} + \frac{1}{b+1} \right)^{L-1} \frac{\rho}{\sqrt{(a+1)(b+1)}} \tag{2}
$$

该下界揭示了过挤压的核心机制：当端点度数 $a, b$ 增大时，因子 $\frac{1}{\sqrt{(a+1)(b+1)}}$ 和 $\left(\frac{1}{a+1} + \frac{1}{b+1}\right)^{L-1}$ 共同导致雅可比范数指数级衰减，信息在多跳传播中被“稀释”。

### 漏检过挤压比率（MOSR）

为量化离散曲率对过挤压边的漏检程度，定义 MOSR 指标。首先，给定分位数 $q$，令 $J_q$ 为所有边雅可比范数的第 $q$ 百分位数，则被曲率识别为过挤压的边集为：

$$
\mathcal{E}_q := \{ e \in \mathcal{E} \mid \mathsf{Curv}(e) \leq \mathsf{Percentile}(\mathcal{C}_-, q) \}
$$

MOSR 定义为曲率非负但雅可比范数已处于低分位的边占所有过挤压边的比例：

$$
\mathsf{MOSR}_q := \frac{\sum_{(u,v)\in\mathcal{E}} \mathbf{1}_{\mathsf{Curv}(u,v) \geq 0} \cdot \mathbf{1}_{\mathsf{JacoNorm}(u,v) \leq J_q}}{\sum_{(u',v')\in\mathcal{E}} \mathbf{1}_{\mathsf{JacoNorm}(u',v') \leq J_q}} \tag{3}
$$

MOSR 越高，表明曲率漏检越严重。实验表明（Table 2），Ollivier–Ricci 曲率在 $q=10$ 时漏检 6.7%–38.6% 的过挤压边，在 $q=25$ 时漏检 7.9%–39.8%。

### 加权扩展 Forman-3 曲率（WAF3）

Augmented Forman-3（AF3）曲率计算边两端共同构成三角形的邻居数与剩余一阶邻居数之差：

$$
\mathsf{AF3}(u, v) = |\mathcal{B}(u) \cap \mathcal{B}(v)| - \left( |\mathcal{N}(u) \setminus \mathcal{B}(v)| + |\mathcal{N}(v) \setminus \mathcal{B}(u)| \right)
$$

其中 $\mathcal{N}(u)$ 为 $u$ 的一阶邻居集，$\mathcal{B}(u) = \mathcal{N}(u) \cup \{u\}$。AF3 对所有邻居等权贡献（$f \equiv 1$），导致高度数节点对曲率的贡献被过度放大。

WAF3 引入度依赖权重函数 $f: \mathbb{R} \to \mathbb{R}$ 来抑制高度数节点的贡献：

$$
\mathsf{WAF3}_f(u, v) := \sum_{i \in \mathcal{B}(u) \cap \mathcal{B}(v)} f(d_i) - \left( \sum_{i \in \mathcal{N}(u) \setminus \mathcal{B}(v)} f(d_i) + \sum_{i \in \mathcal{N}(v) \setminus \mathcal{B}(u)} f(d_i) \right) \tag{Section 5}
$$

其中 $d_i$ 为节点 $i$ 的度数。AF3 是 WAF3 在 $f \equiv 1$ 时的特例。实验采用 $f(d) = 1/(1+d)$，该选择在消融实验中优于 $f(d) = (1+d)^{-2}$ 和 $f(d) = (1+d)^{-1/2}$（Table 9）。

### 基于加权 Jaccard 相似度的等价形式与加速

WAF3 可重写为加权 Jaccard 相似度的函数。定义加权 Jaccard 相似度：

$$
\mathrm{Jaccard}_f(\mathcal{N}(u), \mathcal{N}(v)) := \frac{\sum_{i \in \mathcal{N}(u) \cap \mathcal{N}(v)} f(d_i)}{\sum_{i \in \mathcal{N}(u) \cup \mathcal{N}(v)} f(d_i)}
$$

则 WAF3 的等价形式为（Theorem 6）：

$$
\mathsf{WAF3}_f(u, v) = \frac{2}{f(u) + f(v)} \left( 2 - \frac{3}{1 + \mathrm{Jaccard}_f(\mathcal{N}(u), \mathcal{N}(v))} \right) \left( \sum_{i \in \mathcal{N}(u)} f(d_i) + \sum_{i \in \mathcal{N}(v)} f(d_i) \right)
$$

该等价形式将曲率计算转化为加权 Jaccard 相似度的估计问题。通过加权 MinHash 采样 $H$ 个哈希函数，可将 Jaccard 相似度计算复杂度降至 $O(H)$，从而使 WAF3 的整体计算复杂度降为 $O(H|\mathcal{E}|)$（Algorithm 1）。在 $10^5$ 节点图上，$H=100$ 的近似 WAF3 相比精确计算实现 133.7 倍加速（Figure 3），且 Kendall Tau-b 排序相似度维持在约 95%（Figure 4）。

### 边介数分析

为刻画被曲率识别与忽略的边的结构位置，引入边介数：

$$
\mathsf{Between}(e) = \sum_{u \neq v \in \mathcal{V}} \frac{\sigma_{uv}(e)}{\sigma_{uv}} \tag{4}
$$

其中 $\sigma_{uv}$ 为 $u$ 到 $v$ 的最短路径总数，$\sigma_{uv}(e)$ 为其中经过边 $e$ 的路径数。定义三个统计量：
- $\mathsf{BetwIden}_q$：被曲率识别为过挤压的边的平均介数；
- $\mathsf{BetwAll}$：所有边的平均介数；
- $\mathsf{BetwIgno}_q$：被曲率忽略（曲率 $\geq 0$ 但雅可比范数 $\leq J_q$）的边的平均介数。

实验发现（Table 3），在绝大多数数据集上 $\mathsf{BetwIden} > \mathsf{BetwAll} > \mathsf{BetwIgno}$，表明离散曲率倾向于仅识别连接集群的“桥梁边”，而系统性地忽略位于集群内部、介数较低但同样遭受严重过挤压的边。



## 实验与关键发现

### 核心评价指标：遗漏过挤压比率 (MOSR)

为量化离散曲率对过挤压边的漏检程度，本文定义了遗漏过挤压比率 (Missed Over-Squashing Ratio, MOSR)：

$$
\mathsf{MOSR}_q := \frac{\sum_{(u,v) \in \mathcal{E}} \mathbf{1}_{\mathsf{Curv}(u,v) \geq 0} \cdot \mathbf{1}_{\mathsf{JacoNorm}(u,v) \leq J_q}}{\sum_{(u',v') \in \mathcal{E}} \mathbf{1}_{\mathsf{JacoNorm}(u',v') \leq J_q}}
$$

其中 $J_q$ 表示雅可比范数（JacoNorm）的第 $q$ 百分位数。MOSR 衡量的是：在所有被雅可比范数判定为过挤压的边（JacoNorm $\leq J_q$）中，被曲率判定为“非过挤压”（曲率 $\geq 0$）的比例。MOSR 值越低，说明曲率对过挤压边的漏检越少。

### 主结果一：现有离散曲率存在系统性漏检

在 21 个数据集、3 种 GNN 架构（GCN、GAT、GraphSAGE）上的实验揭示了现有离散曲率的显著缺陷。

**Table 2** 报告了三种离散曲率的 MOSR 值。核心发现如下：

![[assets/figures/papers/iclr26_0012_QYtmqCoilk_Rethinking_the_Gold_Standard_Why_Discrete_Curvat/figures/003_Table_2.jpg]]
*Table 2: The values of ${ \mathsf { M O S R } } _ { 1 0 }$ and ${ \mathsf { M O S R } } _ { 2 5 }$ across different GNNs, curvatures, and datasets. Among these, the entr$y ^ { 6 6 }$ . 0 3 0 / . 1 0 $3 ^ { \cdots }$ in the first row and first column indicates that for Ollivier Ricci curvature, GCN, and Cora dataset, $\mathsf { M O S R } _ { 1 0 }$ = 0 . 0 3 0 and $\mathsf { M O S R } _ { 2 5 }$ = 0 . 1 0 3 . OOR denotes “Out of Resources”, meaning the GPU memory consumption exceeds 24 GB or the running time surpasses 12 hours. NNE (No Negative-curvature Edge) indicates that | $\mathcal { E } _ { q }$ | = 0 in this scenario

- **Ollivier–Ricci 曲率漏检最为严重**。在 $q=10$ 时，其 MOSR 范围高达 6.7%–38.6%；$q=25$ 时升至 7.9%–39.8%。在 Cora 数据集上，GCN 搭配 Ollivier–Ricci 的 MOSR$_{10}$ 为 0.030，意味着 3% 的过挤压边被忽略。在 21 个数据集上的平均 MOSR$_{10}$ 达到 0.271，即超过四分之一的过挤压边被漏检。
- **Balanced Forman 曲率表现居中**，平均 MOSR$_{10}$ 为 0.108–0.205，但仍存在不可忽视的漏检。
- **Augmented Forman-3 (AF3) 曲率在现有方法中表现最优**，平均 MOSR$_{10}$ 为 0.067–0.161，且计算复杂度最低（$O(|E| d_{\max})$）。这表明基于三角形计数的简单曲率反而比复杂的 Ollivier–Ricci 曲率更有效地关联过挤压。

> **需要手动验证**：Table 2 中部分数据集的 MOSR 值以科学计数法报告，具体数值需查阅原文确认。

### 主结果二：漏检边的结构特征——边介数分析

为理解曲率为何漏检，本文引入边介数（Edge Betweenness）指标：

$$
\mathsf{Between}(e) = \sum_{u \neq v \in \mathcal{V}} \frac{\sigma_{uv}(e)}{\sigma_{uv}}
$$

并定义了三个统计量：**BetwIden**（被曲率识别的边的平均介数）、**BetwAll**（所有边的平均介数）、**BetwIgno**（被曲率忽略的过挤压边的平均介数）。

**Table 3** 在 GCN 模型、$q=25$ 设定下的结果显示：

![[assets/figures/papers/iclr26_0012_QYtmqCoilk_Rethinking_the_Gold_Standard_Why_Discrete_Curvat/figures/004_Table_3.jpg]]
*Table 3: The model is fixed as GCN, q is set to 25, and we report BetwIden, BetwAll, and BetwIgno on three curvature definitions and 21 datasets, respectively. NIE (No Ignored Edge) means no edges are ignored by curvature, so BetwIgno cannot be calculated*

- 在绝大多数数据集中，**BetwIden > BetwAll**，表明离散曲率主要识别位于集群之间的“桥接边”（高介数边）。
- 同时，**BetwAll > BetwIgno**，说明被曲率忽略的过挤压边具有较低的边介数，即这些边位于集群内部而非集群之间。

这一发现揭示了现有离散曲率的根本局限：它们仅依赖于一阶邻居的紧密程度（如三角形个数），因此天然倾向于将集群间的稀疏连接判定为高负曲率（过挤压），而忽略了集群内部因高度数节点导致的“信息稀释”效应。

### 消融实验一：WAF3 的权重函数选择

WAF3 的核心创新在于引入度依赖权重函数 $f(d)$ 来抑制高度数节点的过度贡献。**Table 9** 考察了三种衰减函数对 MOSR 的影响：

- $f(d) = (1+d)^{-1}$：MOSR$_{10}$ 平均 0.036，MOSR$_{25}$ 平均 0.045
- $f(d) = (1+d)^{-2}$：过强衰减，性能略差
- $f(d) = (1+d)^{-1/2}$：过弱衰减，性能介于两者之间

实验表明 $f(d) = 1/(1+d)$ 在平均 MOSR 上表现最优，但该选择仍是启发式的，尚未证明其最优性。

### 消融实验二：MOSR 随训练动态变化

附录 D.1 中的 **Figure 5–11** 展示了 MOSR 随训练轮次的变化趋势。关键观察：

- MOSR 随训练轮次增加而缓慢上升，最终趋于稳定。
- 未训练模型的 MOSR 值实际上是各曲率漏检概率的**下界**。这意味着即使在不考虑模型参数影响的情况下，曲率的漏检问题已然存在；训练过程会进一步暴露这一问题。

### 主结果三：WAF3 显著降低 MOSR

**Table 4** 报告了 WAF3（$f(x) = 1/(1+x)$）在 17 个数据集上的 MOSR 表现：

![[assets/figures/papers/iclr26_0012_QYtmqCoilk_Rethinking_the_Gold_Standard_Why_Discrete_Curvat/figures/006_Table_4.jpg]]
*Table 4: The values of ${ \mathsf { M O S R } } _ { 1 0 }$ and ${ \mathsf { M O S R } } _ { 2 5 }$ across different GNNs and datasets when the discrete curvature si set to WAF3 and f ( x ) $\equiv$ 1 / ( 1 + x )

- WAF3 的 MOSR$_{10}$ 范围为 0.000–0.123，MOSR$_{25}$ 范围为 0.000–0.134。
- 在 21 个数据集上的平均 MOSR$_{10}$ 降至 **0.036**，相比 AF3 的 0.067 降低了约 46%，相比 Ollivier–Ricci 的 0.271 降低了约 87%。
- 在 Cora 数据集上，GCN + WAF3 的 MOSR$_{10}$ 降至 **0.000**，即理论上的零漏检。

### 加速算法评估

WAF3 通过等价变换为加权 Jaccard 相似度，并利用加权 MinHash 实现近似计算（Algorithm 1）。

**Figure 3** 展示了不同曲率的计算时间对比。在 $10^5$ 节点规模下，近似 WAF3（$H=100$）相比精确 WAF3 实现了 **133.7 倍**加速；在 500 万边图上仅需 **23.8 秒**，而 Ollivier–Ricci 曲率在 24GB GPU 限制下无法完成计算。

**Figure 4** 评估了近似质量。使用 $H=100$ 个哈希函数时，精确与近似 WAF3 之间的 Kendall Tau-b 相似度约为 **95%**；$H=1000$ 时超过 **98%**。这表明近似算法在维持排序一致性的同时大幅降低了计算开销。

### 下游任务验证：图重连与端到端学习

为验证 WAF3 在实际应用中的有效性，本文在两个图重连框架下进行了测试。

**SDRF 图重连（Table 10）**：在 Texas 数据集上，以 WAF3 为曲率定义的 SDRF 重连后分类准确率达到 **73.62±0.62**，相比 Balanced Forman 的 70.35±0.60 提升了 **+3.27 个百分点**。

![[assets/figures/papers/iclr26_0012_QYtmqCoilk_Rethinking_the_Gold_Standard_Why_Discrete_Curvat/figures/021_Table_10.jpg]]
*Table 10: Accuracy on downstream classification tasks after graph rewiring using SDRF (Topping et al., 2021) with different curvature definitions. The experimental setup for this experiment remains identical to the original paper. *Indicates data referenced from Topping et al. (2021)*

**GNRF 端到端学习（Table 11）**：在 Texas 数据集上，WAF3 驱动的 GNRF 准确率达到 **87.11±1.03**，相比 Balanced Forman 的 83.15±6.25 提升了 **+3.96 个百分点**。近似 WAF3（$H=100$）也达到了 86.11±0.96，在精度损失极小的情况下保持了竞争力。

![[assets/figures/papers/iclr26_0012_QYtmqCoilk_Rethinking_the_Gold_Standard_Why_Discrete_Curvat/figures/022_Table_11.jpg]]
*Table 11: The accuracy of end-to-end model GNRF (Chen et al., 2025) on downstream classification tasks using different curvature definitions. The experimental setup for this experiment remains exactly the same as the original GNRF paper*

### 失败模式与局限

1. **理论上的不完整性**：WAF3 仍仅依赖一阶邻居的局部结构，离散曲率本质上不是过挤压的必要条件，因此无法从理论上保证完全检测所有过挤压边。
2. **权重函数的启发式性质**：$f(d)=1/(1+d)$ 的选择基于经验，缺乏严格的最优性证明。
3. **近似引入的误差**：虽然 $H=100$ 时 Kendall Tau-b 相似度约 95%，但在精度敏感场景中，这一近似损失可能影响过挤压边检测的准确性。
4. **实验范围的限制**：所有实验限于同质无向图及 GCN/GAT/GraphSAGE 三种架构，在有向图、异构图、时序图上的有效性有待验证。
5. **MOSR 的计算开销**：MOSR 依赖雅可比范数的计算，在大规模图中仍较昂贵，限制了其在超大图上的实时使用。



## 定位与知识库关联

### 与现有离散曲率的关系

本文提出的加权扩展 Forman-3 曲率（Weighted Augmented Forman-3 Curvature, WAF3）直接继承自 Augmented Forman-3（AF3）的定义框架，但引入了一个关键的修正项：**度依赖权重函数** $f(d) = 1/(1+d)$，用于抑制高度数节点对曲率的过度贡献。AF3 可视为 WAF3 在 $f \equiv 1$ 时的特例。

在更广的方法谱系中，离散曲率用于检测 GNN 过挤压的工作可大致分为三类：

1. **Ollivier–Ricci 曲率及其变体**：基于最优传输距离定义，计算复杂度最高（精确计算为 $O(|E| d_{\max}^3)$），在 MOSR 指标上表现最差（平均漏检 27.1%–39.8% 的过挤压边）。
2. **Balanced Forman 曲率**（Topping et al., 2021）：复杂度较低（$O(|E| d_{\max}^2)$），MOSR 表现中等，但仍存在显著漏检。
3. **Augmented Forman-3 曲率**：基于三角形计数的纯组合定义，复杂度最低（$O(|E| d_{\max})$），MOSR 表现优于前两者，但平均仍有 6.7%–16.1% 的漏检率。

WAF3 在 AF3 的基础上，通过加权函数修正了高度数节点的贡献偏差，将平均 MOSR₁₀ 从 0.067 进一步降至 0.036，MOSR₂₅ 从 0.161 降至 0.123。这一改进的**因果机制**在于：AF3 对一阶邻居等权求和，导致高度数节点（如 hub 节点）在曲率计算中占据主导地位，使得曲率值主要反映 hub 周围的局部紧密程度，而非边在多跳传播中的信息瓶颈程度。

### 适用边界

WAF3 的适用性受以下条件约束：

1. **图结构类型**：当前实验仅在同质无向图上验证（21 个标准引文网络和社交网络数据集），未涉及异构图、有向图或时序图。在这些更复杂的图结构上，WAF3 的定义和 MOSR 评估框架的有效性需要手动验证。
2. **模型架构**：MOSR 实验覆盖 GCN、GAT、GraphSAGE 三种经典 MPNN，其中 GCN 始终取得最低的 MOSR 值。对于使用注意力机制或跳跃连接的更复杂架构，MOSR 的行为模式可能不同。
3. **任务类型**：MOSR 基于节点分类任务中的雅可比范数定义，其结论向图分类、链接预测等任务的迁移需要额外验证。
4. **图规模**：精确 WAF3 的计算复杂度为 $O(|E| d_{\max})$，近似算法通过加权 MinHash 将复杂度降至 $O(H|E|)$（$H$ 为哈希函数数量）。在 500 万边图上，近似 WAF3（$H=100$）仅需 23.8 秒，实现 133.7 倍加速，Kendall Tau‑b 相似度约 95%。但对于十亿级边的工业图，$O(H|E|)$ 的线性复杂度仍可能成为瓶颈。

### 局限与开放问题

**已知局限**：

1. **曲率不是过挤压的必要条件**：WAF3 仍仅依赖于一阶邻居的局部结构，理论上不能保证完全检测所有过挤压边。这是离散曲率方法的根本性局限——高负曲率是过挤压的充分但不必要条件，但反之不成立。
2. **权重函数的启发式选择**：$f(d) = 1/(1+d)$ 的选择基于直觉（抑制高度数节点），消融实验表明它在平均 MOSR 上优于 $(1+d)^{-2}$ 和 $(1+d)^{-1/2}$，但其最优性尚未得到理论证明。
3. **近似损失**：加权 MinHash 近似引入了随机误差。当 $H=100$ 时，Kendall Tau‑b 相似度约 95%；$H=1000$ 时超过 98%。在精度敏感的下游任务（如 SDRF 图重连）中，近似损失可能累积影响最终性能。
4. **MOSR 的计算成本**：MOSR 依赖于雅可比范数的计算，在大规模图上仍较昂贵，限制了其在超大图上的实时使用。文中报告的未训练模型 MOSR 值实际上是各曲率漏检概率的下界，MOSR 随训练轮次增加而缓慢上升并趋于稳定。

**开放问题**：

1. **充分必要条件**：能否设计一种既充分又必要地捕获过挤压的离散曲率？这需要超越一阶邻居的局部信息，可能涉及高阶邻域结构或多跳路径特征。
2. **自适应权重**：WAF3 的权重函数 $f(d)$ 是否有自适应的学习策略？例如通过注意力机制动态获得，或根据下游任务端到端优化。
3. **内部集群过挤压的影响**：被曲率忽略的内部集群过挤压边（BetwIgno < BetwAll）对下游任务性能的实际影响有多大？这些边虽然介数较低，但在密集集群内部的信息稀释效应可能对特定任务产生非平凡的影响。
4. **更大规模的可扩展性**：加权 MinHash 近似算法能否进一步降低复杂度，以支持十亿级边的工业图？可能的路径包括分布式哈希计算或基于采样的近似策略。
5. **异构图和有向图的扩展**：在有向图、异构图和时序图上，离散曲率的概念和 MOSR 检测框架是否依然有效？这需要重新审视曲率的几何意义和过挤压的数学定义。



## 原文 PDF

![[paperPDFs/ICLR_2026/Rethinking_the_Gold_Standard_Why_Discrete_Curvature_Fails_to_Fully_Capture_Over_squashing_in_GNNs.pdf]]
