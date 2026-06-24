---
title: "A Graph Meta-Network for Learning on Kolmogorov–Arnold Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Graph_Meta_Network_for_Learning_on_KolmogorovArnold_Networks.pdf
openreview_forum_id: ONpyYavBqR
aliases:
- WK
- GMNLKAN
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/graph_neural_networks
core_operator: "利用KANs与MLPs同构的隐藏神经元置换对称性，将KAN的计算图表示为带属性边的KAN-graph，并采用双向消息传递图神经网络（WS-KAN）进行学习。"
primary_logic: "KANs与MLPs共享相同的隐藏层置换对称性（Proposition 3.1），因此可将KAN的参数表示为图——节点为神经元，边为B-spline函数参数，从而使得GNN能够自然地利用对称性进行权重空间学习。"
claims:
- "KANs exhibit the same permutation symmetries as MLPs."
- "The KAN-graph representation encodes all learnable B-spline parameters as edge features."
- "WS-KAN can simulate the forward pass of the input KAN, confirming its expressive power."
- "WS-KAN consistently outperforms all baseline methods on INR classification, accuracy prediction, and pruning tasks."
---

# A Graph Meta-Network for Learning on Kolmogorov–Arnold Networks

> [!tip] 核心洞察
> KANs与MLPs共享相同的隐藏层置换对称性（Proposition 3.1），因此可将KAN的参数表示为图——节点为神经元，边为B-spline函数参数，从而使得GNN能够自然地利用对称性进行权重空间学习。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种用于Kolmogorov-Arnold网络学习的图元网络 |
| 英文题名 | A Graph Meta-Network for Learning on Kolmogorov–Arnold Networks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ONpyYavBqR); [GitHub](https://github.com/BarSGuy/KAN-Graph-Metanetwork) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/graph_neural_networks |
| Method | WS-KAN |
| Dataset | MNIST INR, Fashion-MNIST INR, CIFAR-10 INR, MNIST Accuracy Prediction |

> [!tip] 效果简介
> - MNIST INR 上，Classification Accuracy (%) 为 94.3±0.5，对比 Best alternative (SetTrans/DS): < 94.3，变化 outperforms all baselines。
> - Fashion-MNIST INR 上，Classification Accuracy (%) 为 84.6±0.6，对比 Best alternative: < 84.6，变化 outperforms all baselines。
> - CIFAR-10 INR 上，Classification Accuracy (%) 为 42.2±0.8，对比 Best alternative: < 42.2，变化 outperforms all baselines。

## 概述

权重空间学习（learning in weight spaces）旨在直接对神经网络的参数进行推理，以预测其下游性能或结构属性。现有方法主要针对多层感知机（MLP）设计，利用其隐藏神经元的置换对称性，将参数表示为图或集合进行处理。然而，Kolmogorov-Arnold网络（KANs）作为一种新兴架构，其参数并非标量权重，而是可学习的单变量函数（通常以B-spline参数化），这给权重空间学习带来了根本性挑战：**如何将对称性感知的架构扩展至函数参数空间，同时保持表达效率？**

本文的核心发现是：KANs与MLPs共享相同的隐藏层置换对称性（Proposition 3.1）。基于这一洞察，作者提出将KAN的计算图转化为一种带属性边的有向图——**KAN-graph**，其中节点对应神经元，边特征编码对应B-spline函数的全部可学习参数。在此基础上，设计了**WS-KAN**——一种双向消息传递图神经网络，通过结合节点与边的位置编码，在尊重置换对称性的同时打破虚假对称性，实现对KAN权重空间的高效学习。

WS-KAN在三个典型任务上一致优于所有基线方法：在MNIST、Fashion-MNIST和CIFAR-10的隐式神经表示（INR）分类中，准确率分别达到94.3%、84.6%和42.2%（Table 1）；在MNIST精度预测任务上，MSE降至3.29×10³，相比朴素MLP基线降低77.4%，R²提升至94.81%（Table 3）；在剪枝掩码预测中，准确率达97.93%，ROC-AUC达99.54%（Table 4）。此外，WS-KAN的计算复杂度与KAN-graph边数线性缩放，具有良好的可扩展性。

该方法的主要局限在于：OOD泛化性能呈现数据集依赖性（MNIST INR在更宽网络上退化严重，而Fashion-MNIST INR保持鲁棒），且仅在特定拓扑上验证，尚未在CNN-KAN等扩展架构上测试。未来方向包括探索更复杂KAN拓扑的适配、非B-spline函数参数化的兼容性，以及利用WS-KAN实现KAN与MLP间的架构转换。

## 背景与动机

### 权重空间学习的兴起与局限

深度学习的成功催生了对神经网络本身进行学习的范式——权重空间学习（weight-space learning）。其核心思想是：将训练好的网络参数视为输入，构建一个元模型来预测网络的性质（如泛化精度、剪枝掩码），或生成新的参数。这一范式在模型选择、超参优化、神经架构搜索等场景中展现出巨大潜力。

然而，权重空间学习面临一个根本性瓶颈：**神经网络参数空间存在固有的置换对称性**。对于多层感知机（MLP），任意隐藏层的神经元可以被重新排列，只要相应地调整相邻层的权重矩阵，网络所表达的函数完全不变。这意味着两个参数向量在欧氏空间中可能相距甚远，却代表完全相同的函数。直接对展平参数向量应用标准架构（如MLP）会忽略这一对称性，导致严重的样本效率低下和泛化能力不足。

为应对这一挑战，研究者提出了多种对称性感知的权重空间架构，如基于深度集（DeepSets）的方法、基于Transformer的集合架构（SetTrans）等。这些方法将网络参数组织为图或集合结构，利用置换等变网络来自然地编码对称性，在MLP的属性预测、精度预测等任务上取得了显著进展。

### Kolmogorov-Arnold网络的兴起与空白

2024年，Kolmogorov-Arnold网络（KAN）作为一种新型神经网络范式引起广泛关注。与MLP在边上使用标量权重、在节点上使用固定激活函数不同，**KAN将可学习的单变量函数置于边上，而节点仅执行求和操作**。具体而言，一个$L$层KAN的前向传播定义为：

$$f(\pmb{x}) = \pmb{x}^L, \quad \mathrm{where} \ {\boldsymbol{x}}_p^l = \sum_{q=1}^{d_{l-1}} \phi_{p,q}^l \big( {\boldsymbol{x}}_q^{l-1} \big), \quad \pmb{x}^0 = \pmb{x}$$

其中每条边上的单变量函数$\phi_{p,q}^l$采用B-spline参数化：

$$\psi ( x ) = w _ { b } b ( x ) + w _ { s } B ( x ) ; \qquad B ( x ) = \langle c , B ( x ) \rangle = \sum _ { i } c _ { i } B _ { i } ( x )$$

即由SiLU基函数$b(x)$与B样条$B(x)$的加权组合构成，其中$B(x)$是基函数$B_i(x)$的线性组合，$c_i$为可学习系数。

KAN在科学发现、偏微分方程求解、时间序列预测等领域展现出优于MLP的表示能力和可解释性。然而，**权重空间学习在KAN上的扩展完全空白**。这一空白源于两个关键挑战：

1. **参数类型的根本差异**：MLP的参数是标量权重矩阵，而KAN的参数是可学习单变量函数（B-spline系数）。如何将权重空间学习框架适配到这种函数型参数空间，尚无现成方案。

2. **对称性结构是否成立**：MLP的置换对称性是其权重空间学习设计的基石。KAN是否具有类似的对称性？如果存在，能否利用它来设计高效的元架构？这些问题在本文之前未被系统研究。

### 本文的核心洞察与贡献

本文的核心洞察是：**KAN与MLP共享相同的隐藏层置换对称性**。如Figure 2所示，在KAN的任意隐藏层中，神经元可以被重新排列，只要相应地调整相邻层的函数矩阵，网络行为完全不变。这一性质被形式化为Proposition 3.1（KAN对称性），为将权重空间学习扩展至KAN奠定了理论基础。

基于这一洞察，本文提出**将KAN的计算图表示为一种带属性边的图——KAN-graph**（Figure 1）。在该图中，节点对应神经元，边则编码了对应的B-spline函数参数：

$$\boldsymbol { e } _ { p , q } ^ { l } = \tilde { \phi } _ { p , q } ^ { l } : = [ w _ { b ; p , q } ^ { l } , ~ w _ { s ; p , q } ^ { l } , ~ \boldsymbol { c } _ { p , q } ^ { l } ]$$

这种表示将KAN的参数自然地组织为图结构，使得图神经网络（GNN）能够利用置换对称性进行学习。

在此基础上，本文开发了**WS-KAN**——一种基于双向消息传递GNN的权重空间学习架构。WS-KAN在KAN-graph上进行前向和后向消息传递，并结合节点与边的位置编码以打破虚假对称性，能够直接对KAN的权重空间进行学习。该架构被证明可以模拟输入KAN的前向传播（Proposition 4.2），确认了其表达能力。

综上，本文填补了权重空间学习在KAN上的空白，为这一新兴网络范式的分析、预测和优化提供了首个专用元学习框架。

## 核心创新

WS-KAN 的核心创新在于将权重空间学习（Weight‑Space Learning）从传统 MLP 扩展至 Kolmogorov–Arnold 网络，其关键突破体现在三个相互关联的维度上。

**参数类型：从标量权重到可学习单变量函数。** 传统权重空间方法操作的对象是 MLP 的标量权重矩阵与偏置。WS‑KAN 首次将学习对象转换为 KAN 中每条边对应的可学习单变量 B‑spline 函数（Eq. (3)、Eq. (5)）。这些函数由 SiLU 基函数 $b(x)$ 与 B‑spline $B(x)$ 的加权组合构成：

$$\psi ( x ) = w _ { b } b ( x ) + w _ { s } B ( x ) ; \qquad B ( x ) = \langle c , B ( x ) \rangle = \sum _ { i } c _ { i } B _ { i } ( x )$$

这使得每条边的参数量从单个标量扩展为包含基函数权重 $w_b, w_s$ 和 B‑spline 系数向量 $\boldsymbol{c}$ 的参数组，本质上改变了权重空间学习的输入粒度。

**输入表示：从展平向量到属性 KAN‑graph。** 朴素基线方法将 KAN 的所有参数展平为单一向量后输入 MLP，这完全忽略了网络内在的结构与对称性。WS‑KAN 则基于一个关键洞察——KAN 与 MLP 共享相同的隐藏神经元置换对称性（Proposition 3.1）——将 KAN 的计算图重构为带属性边的有向图（KAN‑graph）。图中节点对应神经元，边特征编码对应的 B‑spline 参数：

$$\boldsymbol { e } _ { p , q } ^ { l } = \tilde { \phi } _ { p , q } ^ { l } : = [ w _ { b ; p , q } ^ { l } , ~ w _ { s ; p , q } ^ { l } , ~ \boldsymbol { c } _ { p , q } ^ { l } ]$$

这一图表示使得 GNN 能够自然地利用置换对称性进行学习，从根本上解决了展平向量方法对参数排列敏感的问题。

**模型架构：从全连接网络到双向消息传递 GNN。** 与在展平向量上操作的全连接网络不同，WS‑KAN 采用双向消息传递机制，同时沿计算图的前向和后向方向聚合信息：

$$v_i^{\mathrm{F}} = \mathbb{MLP}_v^{(2;\mathrm{F})}\left(v_i, \sum_{j: e(i,j)\in E} \mathbb{MLP}_v^{(1;\mathrm{F})}(v_j,e_{(i,j)})\right)$$

$$v_i^{\mathrm{B}} = \mathbb{MLP}_v^{(2;\mathrm{B})}\left(v_i, \sum_{j: e(i,j)\in E^T} \mathbb{MLP}_v^{(1;\mathrm{B})}(v_j,e_{(i,j)})\right)$$

$$e_{(i,j)} = \mathbb{MLP}_e(v_i, v_j, e_{(i,j)})$$

消融实验证实，双向消息传递在所有任务（INR 分类、精度预测、剪枝）中均至关重要，缺少任一向传递都会导致显著性能下降。此外，WS‑KAN 引入节点与边的位置编码以打破 KAN‑graph 中可能存在的虚假对称性，这在剪枝掩码预测的全部 6/6 个案例中均带来一致提升。

**理论与效率保证。** WS‑KAN 具备模拟输入 KAN 前向传播的表达能力（Proposition 4.2），且其计算复杂度与 KAN‑graph 的边数 $E$ 线性缩放，即 $O(E)$，确保了良好的可扩展性。

## 整体框架

![[assets/figures/papers/iclr26_0012_ONpyYavBqR_A_Graph_Meta-Network_for_Learning_on_KolmogorovA/figures/001_Figure_1.jpg]]
*Figure 1: Constructing the KAN-graph for a given Kolmogorov-Arnold Network (KAN)*

![[assets/figures/papers/iclr26_0012_ONpyYavBqR_A_Graph_Meta-Network_for_Learning_on_KolmogorovA/figures/003_Table_1.jpg]]

WS-KAN 的完整 pipeline 由三个核心模块串联构成：**KAN‑graph 构建器**、**GNN 编码器（WS‑KAN）**和**任务头**。给定一个已训练的 KAN，pipeline 将其参数转化为结构化的图表示，通过对称性感知的消息传递提取权重空间表征，最终适配到下游任务。

### 模块关系与数据流

**1. KAN‑graph 构建器**

输入为一个 $L$ 层 KAN 的完整参数集。构建器将 KAN 的计算图直接映射为带属性边图 $G = (V, E)$（Figure 1）：
- **节点** $V$ 对应所有层的神经元，总节点数 $N = \sum_{l=1}^{L} n_l$。
- **有向边** $E$ 对应层间全连接，总边数 $E = \sum_{l=1}^{L-1} n_l n_{l+1}$。
- **边特征** 编码每条边对应的可学习单变量函数参数：

$$
\boldsymbol{e}_{p,q}^{l} = \tilde{\phi}_{p,q}^{l} := [w_{b;p,q}^{l},\ w_{s;p,q}^{l},\ \boldsymbol{c}_{p,q}^{l}]
$$

其中 $w_b$ 为 SiLU 基函数权重，$w_s$ 为 B‑spline 权重，$\boldsymbol{c}$ 为 B‑spline 系数向量（Eq. (5)）。这一表示将 KAN 的所有可学习参数无损地编码为边属性。

**2. GNN 编码器（WS‑KAN）**

编码器在 KAN‑graph 上执行双向消息传递，提取等变于 KAN 隐藏神经元置换对称性（Proposition 3.1）的权重空间表征。具体更新规则为：

- **前向消息传递**（沿原始边方向）：
  $$v_i^{\mathrm{F}} = \mathbb{MLP}_v^{(2;\mathrm{F})}\left(v_i, \sum_{j: e(i,j)\in E} \mathbb{MLP}_v^{(1;\mathrm{F})}(v_j, e_{(i,j)})\right)$$

- **后向消息传递**（沿转置边方向）：
  $$v_i^{\mathrm{B}} = \mathbb{MLP}_v^{(2;\mathrm{B})}\left(v_i, \sum_{j: e(i,j)\in E^T} \mathbb{MLP}_v^{(1;\mathrm{B})}(v_j, e_{(i,j)})\right)$$

- **边特征更新**：
  $$e_{(i,j)} = \mathbb{MLP}_e(v_i, v_j, e_{(i,j)})$$

节点和边均分配**位置编码**（Figure 3），以打破 KAN‑graph 中因结构对称性导致的虚假对称性，使 GNN 能够区分不同层和位置的神经元。消融实验确认，位置编码在所有 6/6 剪枝掩码预测任务上一致提升性能（Tables 9‑10），而移除双向消息传递导致所有任务（INR 分类、精度预测、剪枝）显著退化（Tables 6‑10）。

**3. 任务头**

编码器输出的图级表征（通过全局池化获得）送入任务特定的线性层或小型 MLP：
- **INR 分类**：输出类别 logits（Table 1）。
- **精度预测**：输出标量精度估计值（Table 3）。
- **剪枝掩码预测**：对每条边输出保留/剪枝的二值决策（Table 4, Figure 11）。

### 效率特性

WS‑KAN 的计算复杂度与 KAN‑graph 的边数 $E$ 线性缩放（$\mathcal{O}(E)$），使其能够高效处理不同拓扑的 KAN。实际运行时间测量（Table 11）显示，MNIST INR 分类任务上每 epoch 训练时间约 10.12 秒，CIFAR‑10 上约 10.88 秒，验证了良好的可扩展性。

### 表达能力保障

Proposition 4.2 证明 WS‑KAN 可以模拟输入 KAN 的前向传播：对任意 $\varepsilon > 0$，存在 WS‑KAN 使得 $\sup_{\boldsymbol{x} \in [a,b]^n} |\text{WS-KAN}(G) - f_\theta(\boldsymbol{x})| < \varepsilon$。这保证了编码器在理论上不会丢失 KAN 的函数信息，为下游任务的性能提供了基础保障。

## 核心模块与公式推导

### KAN的前向传播与B‑spline参数化

KAN的核心计算由L层函数矩阵的复合构成。第l层的前向传播定义为：

$$f(\pmb{x}) = \pmb{x}^L, \quad \mathrm{where} \ {\boldsymbol{x}}_p^l = \sum_{q=1}^{d_{l-1}} \phi_{p,q}^l \big( {\boldsymbol{x}}_q^{l-1} \big), \quad \pmb{x}^0 = \pmb{x}$$

其中 $\phi_{p,q}^l$ 是连接前一层神经元q到当前层神经元p的单变量函数。整个KAN可写为函数矩阵的复合：

$$f(\pmb{x}) = (\phi^L \circ \cdots \circ \phi^1) \pmb{x}$$

每个单变量函数 $\psi(x)$ 采用SiLU基函数与B‑spline的加权组合进行参数化：

$$\psi ( x ) = w _ { b } b ( x ) + w _ { s } B ( x ) ; \qquad B ( x ) = \langle c , B ( x ) \rangle = \sum _ { i } c _ { i } B _ { i } ( x )$$

其中 $b(x)=\text{silu}(x)$ 为基函数，$B(x)$ 为B‑spline函数，由可学习系数向量 $\boldsymbol{c}$ 对B‑spline基函数 $B_i(x)$ 进行线性组合得到。$w_b$ 和 $w_s$ 控制两者的混合权重。这一参数化方式是后续构建KAN‑graph边特征的基础。

### KAN‑graph构建

WS‑KAN方法的核心创新在于将KAN的计算图转化为属性图表示。对于给定的KAN，定义有向图 $G = (V, E)$，其中节点集 $V$ 对应所有神经元，边集 $E$ 对应所有层间的函数连接。每条边 $(p,q)$ 的特征由对应单变量函数的全部可学习参数构成：

$$\boldsymbol { e } _ { p , q } ^ { l } = \tilde { \phi } _ { p , q } ^ { l } : = [ w _ { b ; p , q } ^ { l } , ~ w _ { s ; p , q } ^ { l } , ~ \boldsymbol { c } _ { p , q } ^ { l } ]$$

这里 $w_{b;p,q}^l$ 和 $w_{s;p,q}^l$ 是标量权重，$\boldsymbol{c}_{p,q}^l$ 是B‑spline系数向量。该表示将KAN的所有可学习参数完整编码为边属性，使得GNN能够直接在参数空间上进行学习。

### 置换对称性

KAN与MLP共享相同的隐藏神经元置换对称性（Proposition 3.1）。给定置换矩阵 $P_1$ 和 $P_2$，它们对函数矩阵的作用为：

$$( P _ { 1 } \phi P _ { 2 } ) _ { p , q } = \phi _ { \sigma _ { 1 } ^ { - 1 } ( p ) , \sigma _ { 2 } ( q ) }$$

这意味着对隐藏层神经元进行置换不会改变KAN所表示的函数，从而保证了KAN‑graph表示在置换操作下的等变性。

### WS‑KAN的双向消息传递

WS‑KAN在KAN‑graph上执行双向消息传递以提取权重空间表征。其更新规则包含三个部分：

a) 前向传播：$v_i^{\mathrm{F}} = \mathbb{MLP}_v^{(2;\mathrm{F})}(v_i, \sum_{j: e(i,j)\in E} \mathbb{MLP}_v^{(1;\mathrm{F})}(v_j,e_{(i,j)}))$

b) 后向传播：$v_i^{\mathrm{B}} = \mathbb{MLP}_v^{(2;\mathrm{B})}(v_i, \sum_{j: e(i,j)\in E^T} \mathbb{MLP}_v^{(1;\mathrm{B})}(v_j,e_{(i,j)}))$

c) 边更新：$e_{(i,j)} = \mathbb{MLP}_e(v_i, v_j, e_{(i,j)})$

其中 $E^T$ 表示转置边集（即反向连接）。每个节点的表示由其自身特征加上前向及后向邻域聚合信息更新，边特征则基于两端节点和自身进行更新。双向设计使得信息能够沿KAN的计算图在两个方向上流动，消融实验证实缺少任一方向都会导致显著性能下降。

### 位置编码

为打破KAN‑graph中可能存在的虚假对称性，WS‑KAN为节点和边分配位置编码（Figure 3）。位置编码采用简单整数索引，嵌入后与原始特征拼接，使模型能够区分结构上等价但功能不同的神经元和连接。消融实验表明，位置编码在所有6项剪枝掩码预测任务上一致提升性能。

### 表达能力保证

WS‑KAN的表达能力由两个理论结果支撑。首先，MLP可以逼近KAN中的任意单变量函数（Lemma 4.1）：对于任意 $\varepsilon > 0$，存在MLP使得 $\sup_{x \in \mathcal{X}} | MLP(x, w_s, w_b, \pmb{c}) - \psi(x) | < \varepsilon$。在此基础上，WS‑KAN可以模拟输入KAN的前向传播（Proposition 4.2）：对于任意 $\varepsilon > 0$，存在WS‑KAN使得 $\sup_{\pmb{x} \in [a, b]^n} | WS-KAN(G) - f_{\theta}(\pmb{x}) | < \varepsilon$。这保证了GNN架构不会因图表示转换而丢失KAN的函数表达能力。

## 实验与分析

### 3.1 INR分类

WS‑KAN在三个INR分类基准上一致超越所有基线方法。表1汇总了在MNIST、Fashion‑MNIST和CIFAR‑10上的分类准确率。WS‑KAN在MNIST上达到94.3±0.5%，在F‑MNIST上达到84.6±0.6%，在CIFAR‑10上达到42.2±0.8%，均显著优于最强基线（包括DeepSets和SetTrans）。这一结果的核心驱动力在于KAN‑graph构建与双向消息传递的结合：KAN‑graph将B‑spline参数编码为边特征，使得GNN能够直接利用KAN的置换对称性进行学习；而双向消息传递则确保了信息沿计算图的前向与后向两个方向流动，完整捕获了参数间的依赖关系。

![[assets/figures/papers/iclr26_0012_ONpyYavBqR_A_Graph_Meta-Network_for_Learning_on_KolmogorovA/figures/007_Table_1.jpg]]
*Table 1: INR classification accuracy*

消融实验（表6）进一步证实了这一判断。移除双向消息传递后，WS‑KAN在所有三个数据集上的准确率均出现显著下降。位置编码的贡献同样关键——在剪枝掩码预测任务中，带位置编码的WS‑KAN在6/6个评估指标上一致优于无位置编码版本（表9、表10），表明位置编码有效打破了KAN‑graph中因同构神经元置换对称性而产生的虚假对称性。

### 3.2 分布外泛化

WS‑KAN展现出数据集依赖的OOD泛化行为（表2）。当在隐藏层宽度h=32的KAN上训练，并在h∈{48,64,80,96}的未见宽度上测试时，MNIST INR的准确率从94.3%急剧下降至57.1%（h=96），而F‑MNIST INR则表现出显著鲁棒性，准确率仅从84.6%小幅下降至82.2%。这种差异可能源于两个数据集的INR所编码的函数复杂性不同，但具体机制尚待进一步分析。

### 3.3 精度预测

在精度预测任务中，WS‑KAN以大幅优势领先所有基线（表3）。以MNIST为例，WS‑KAN的MSE为3.29±0.17（×10³），相较于朴素MLP基线（14.58）降低了77.4%；R²达到94.81±0.27，较MLP（76.99）提升了17.82个百分点。在F‑MNIST和K‑MNIST上，WS‑KAN同样取得最低MSE和最高R²。这些结果表明，WS‑KAN能够从KAN的参数空间中提取出对泛化性能高度敏感的表示，而展平参数向量则完全丢失了这种结构性信息。

![[assets/figures/papers/iclr26_0012_ONpyYavBqR_A_Graph_Meta-Network_for_Learning_on_KolmogorovA/figures/010_Table_3.jpg]]
*Table 3: Accuracy prediction. Comparison of MSE and R ^ { 2 } across datasets*

### 3.4 剪枝掩码预测与下游剪枝

WS‑KAN在剪枝掩码预测任务上达到97.93±0.19%的准确率和99.54±0.01的ROC‑AUC（表4），均优于所有基线。更重要的是，下游剪枝性能（图5）揭示了WS‑KAN的实际价值：在MNIST上，WS‑KAN预测的剪枝掩码在保持高测试精度的同时，实现了与Oracle prune（基于真实激活值阈值）相当甚至更优的精度‑稀疏性权衡，而推理时间仅为1.6×10⁻⁴秒，比Oracle prune（7.20秒）快约四个数量级。在F‑MNIST（图12）上，WS‑KAN同样取得最佳的精度‑稀疏性折衷；在K‑MNIST（图13）上，DeepSets与WS‑KAN表现相当，但WS‑KAN在保留权重比例上略有优势。

![[assets/figures/papers/iclr26_0012_ONpyYavBqR_A_Graph_Meta-Network_for_Learning_on_KolmogorovA/figures/011_Table_4.jpg]]
*Table 4: Pruning mask prediction*

![[assets/figures/papers/iclr26_0012_ONpyYavBqR_A_Graph_Meta-Network_for_Learning_on_KolmogorovA/figures/014_Figure_5.jpg]]
*Figure 5: Downstream pruning performance across methods over KANs trained on MNIST. We report: (i) Test accuracy: the downstream accuracy of pruned networks, averaged over nonoverlapping bins of 20%, to highlight the relative effectiveness of pruning strategies under varying noise levels – Figure 5a; (ii) Kept weights: the percentage of weights retained after pruning, averaged over the same bins as in (i) – Figure 5b; and (iii) Pruning time (↓): the computational cost comparison (log scale) in seconds, between WS-KAN and Oracle prune – Figure 5c, low is better*

### 3.5 计算效率

复杂度分析（附录C.5）表明，WS‑KAN的消息传递复杂度为O(E)，其中E为KAN‑graph的边数，即随网络宽度二次增长。实际运行时间测量（表11）显示，在INR分类任务中，WS‑KAN每epoch训练时间约为10‑11秒（MNIST: 10.12±0.06s, F‑MNIST: 10.18±0.05s, CIFAR‑10: 10.88±0.10s），具有良好的可扩展性。

**需要人工核实的问题**：OOD泛化的退化机制（MNIST INR vs. F‑MNIST INR）在原文中未给出因果解释；WS‑KAN仅在[2‑h‑h‑10]拓扑上进行了验证，对更深或跳跃连接等拓扑变体的泛化能力尚未测试；边特征仅利用了B‑spline的显式参数，其他函数基（如小波）的兼容性需进一步实验确认。

## 方法谱系与知识库定位

### 权重空间学习谱系中的位置

WS-KAN 处于权重空间学习（Weight-Space Learning）与 Kolmogorov-Arnold 网络两条研究线的交汇处。在权重空间学习领域，已有工作主要聚焦于 MLP 和 CNN：DeepSets（DS）和 SetTransformer（SetTrans）通过集合视角利用置换对称性处理展平的参数向量；DWSNets 和其 GNN 变体将 MLP 的计算图表示为图，利用消息传递捕获权重空间结构。WS-KAN 将这一范式从标量权重矩阵扩展至函数矩阵——每条边不再是标量，而是由 B-spline 参数化的单变量函数。

方法谱系上，WS-KAN 与以下基线构成递进关系：

- **朴素 MLP（展平参数）**：完全忽略置换对称性，在所有任务中表现最差。在 MNIST 精度预测任务上，其 MSE（14.58×10³）是 WS-KAN（3.29×10³）的 4.4 倍。
- **MLP + Aug. / MLP + Align.**：通过数据增强或参数对齐引入对称性先验，性能排序为 MLP + Align. > MLP + Aug. > MLP，但仍显著弱于原生对称性感知架构。
- **DeepSets / SetTransformer**：作为基于集合的对称性感知架构，在多个任务上表现强劲（通常第二优），验证了置换等变性是权重空间学习的关键归纳偏置。WS-KAN 在此基础上进一步利用 KAN 的计算图拓扑，通过双向消息传递捕获层间依赖。
- **DMC（深度元分类）**：作为另一类权重空间方法，在 INR 分类任务上表现不如 DS/SetTrans/WS-KAN。

### 适用边界

**支持的 KAN 拓扑**：WS-KAN 天然支持全连接 KAN 层（任意宽度），因为 KAN-graph 构建仅依赖层间全连接假设。实验验证的拓扑为 [2-h-h-10]（h=32），其泛化至未见宽度（h=48/64/80/96）的 OOD 性能因数据集而异：Fashion-MNIST INR 保持鲁棒（h=96 时准确率 82.2±0.7 vs. ID 84.6±0.6），而 MNIST INR 退化严重（h=96 时准确率降至 57.1±6.1）。这表明 WS-KAN 的 OOD 泛化能力不具有数据集无关的保证，需针对具体任务评估。

**函数参数化的依赖**：边特征定义（Eq. 5）直接收集 B-spline 的显式参数 $[w_{b;p,q}^l, w_{s;p,q}^l, \boldsymbol{c}_{p,q}^l]$。这意味着 WS-KAN 当前仅兼容使用 B-spline 参数化的 KAN 变体，对其他函数基（如小波、傅里叶基、径向基函数）的兼容性尚未验证。

**计算效率边界**：WS-KAN 的消息传递复杂度为 $O(E)$，其中 $E = \sum_{l=1}^{L-1} n_l n_{l+1}$ 为 KAN-graph 的边数。在 MNIST INR 分类任务上，每 epoch 训练时间约 10.12 秒，与问题规模线性缩放。但边特征维度随 B-spline 网格点数 G 线性增长（$\boldsymbol{c}_{p,q}^l$ 为 G+k 维向量），当 G 较大时，MLP 编码器的输入维度可能成为瓶颈。

### 已知局限

1. **拓扑泛化受限**：仅在简单全连接 KAN 上验证，未测试跳跃连接、CNN-KAN 等扩展架构。深层 KAN（L>3）的适用性未经实验证实。

2. **OOD 不稳定性**：MNIST INR 的 OOD 退化（h=96 时准确率下降 37.2 个百分点）与 Fashion-MNIST INR 的鲁棒性形成鲜明对比，其根本原因尚不明确。可能涉及 INR 任务特性与 KAN 宽度交互的复杂机制。

3. **函数表示单一**：边特征仅利用 B-spline 参数，未探索对其他可学习函数基的泛化。这限制了 WS-KAN 在更广泛 KAN 变体上的应用。

4. **对齐方法的次优性**：通道级对齐采用等权重的 L2 距离求和（$\arg \min_{\pi} \sum_{c} \| \mathrm{vec}(\Theta_A^c) - \mathrm{vec}(\pi(\Theta_B^c)) \|_2$），加权方案存在改进空间。

### 开放问题

- **架构扩展**：如何将 WS-KAN 的图表示和消息传递机制适配至 CNN-KAN 或带跳跃连接的 KAN 拓扑？这可能需要引入新的边类型或图构建规则。
- **跨范式迁移**：能否利用 WS-KAN 实现 KAN 到 MLP 的变换，以结合 KAN 的可解释性和 MLP 的推理效率？Proposition 4.2 表明 WS-KAN 可模拟 KAN 前向传播，这为跨架构知识迁移提供了理论基础。
- **函数基泛化**：B-spline 以外的函数参数化（如小波、傅里叶基）能否与 WS-KAN 无缝集成？这需要重新设计边特征提取器，但图结构本身可能保持不变。
- **OOD 鲁棒性机制**：MNIST 与 Fashion-MNIST 的 OOD 行为差异揭示了哪些影响泛化的隐藏因素？系统研究此问题可能揭示权重空间学习的根本泛化边界。

## 原文 PDF

![[paperPDFs/ICLR_2026/A_Graph_Meta_Network_for_Learning_on_KolmogorovArnold_Networks.pdf]]
