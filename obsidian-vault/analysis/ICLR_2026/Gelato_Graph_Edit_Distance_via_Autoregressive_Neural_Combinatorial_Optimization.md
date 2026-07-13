---
title: "Gelato: Graph Edit Distance via Autoregressive Neural Combinatorial Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Gelato_Graph_Edit_Distance_via_Autoregressive_Neural_Combinatorial_Optimization.pdf
project_link: null
code_link: null
aliases:
- Gelato
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/graph_neural_networks
core_operator: "将图编辑距离求解转化为自回归节点匹配序列预测。"
primary_logic: "GELATO逐步预测源图和目标图的节点匹配，每步用已匹配关系更新图表示并通过实例约简压缩子问题。"
claims:
- "自回归匹配能捕捉线性分配方法忽略的匹配间依赖关系。"
- "reduce函数移除已解决局部结构而不丢失最优解，从而压缩状态空间。"
- "自同构类中的等价节点对可作为正样本，缓解监督信号歧义。"
- "GELATO在多个GED数据集上达到或接近最优nMAE和EHR，并保持毫秒级推理。"
---

# Gelato: Graph Edit Distance via Autoregressive Neural Combinatorial Optimization

> [!tip] 核心洞察
> 通过自回归的图神经网络模型，将GED问题转化为一个序列预测任务，每一步预测一对源-目标节点进行匹配，并利用实例约简（reduce）技术压缩状态空间，使得模型能够学习到匹配之间的依赖关系，从而显著提升解的质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Gelato：通过自回归神经组合优化求解图编辑距离 |
| 英文题名 | Gelato: Graph Edit Distance via Autoregressive Neural Combinatorial Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=6ZTcLNmguc) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/graph_neural_networks |
| Method | GELATO |
| Dataset | AIDS, LINUX |

> [!tip] 效果简介
> - AIDS 上，nMAE 为 0.1±0.0，对比 0.8±0.1 (MIP-F2)，变化 -0.7。
> - AIDS 上，EHR 为 99.3±0.3，对比 89.0±1.4 (MIP-F2)，变化 +10.3。
> - LINUX 上，nMAE 为 0.1±0.1，对比 0.1±0.0 (MIP-F2)，变化 0.0。

## 概要

GELATO（Graph Edit distance Learning via Autoregressive neural combinaTorial Optimization）是一种基于图神经网络的自回归模型，用于近似求解图编辑距离（Graph Edit Distance, GED）问题。GED是NP-hard的组合优化问题，传统精确求解器难以处理超过20个节点的图，而经典启发式方法经常产生次优解。GELATO将GED求解建模为顺序决策过程，通过自回归方式逐步构建节点匹配，每一步的预测都基于之前的选择，从而能够捕捉复杂的结构依赖关系。实验结果表明，GELATO在所有数据集上的归一化平均绝对误差（nMAE）和精确命中率（EHR）指标均显著优于所有基线方法，并且能够在训练时未见过的更大图上保持领先性能。



### 2.1 问题定义

图编辑距离（GED）定义为将一个图变换为另一个图所需的最小编辑操作成本。通过匹配公式化，GED可以表示为：

$$GED(G_1, G_2) = \min_{\mu \in \mathcal{M}(G_1, G_2)} c(\mu)$$

其中匹配μ的总成本为节点编辑成本和边编辑成本之和：

$$c(\mu) = \sum_{(u,v) \in \bar{\mu}} c_n(G_1, G_2, u, v) + \sum_{(u,v),(w,z) \in \bar{\mu}} c_e(G_1, G_2, (u,w), (v,z))$$

### 2.2 现有方法的局限性

计算GED是NP-hard问题。精确求解器（如基于A*搜索或整数线性规划的方法）难以处理超过20个节点的图。经典启发式方法（如基于线性分配的方法）虽然速度快，但经常产生次优解。关键问题在于：线性分配方法假设节点匹配决策是独立的，无法捕捉匹配之间的相互依赖关系。如Figure 2所示，两个基于相同替代成本矩阵的匹配可能具有相同的线性分配成本，但由于匹配不一致（如(u₁, v₁)和(u₅, v₆)），其中一个可能是次优的。

### 2.3 核心洞察

GELATO的核心洞察在于：一旦固定了一个匹配（如(u₁, v₁)）并将其解释为辅助边，原本不可区分的节点对（如(u₅, v₅)和(u₅, v₆)）就变得可区分了。因此，自回归模型可以做出更明智的选择。通过将GED求解建模为顺序决策过程，每一步的预测都基于之前的选择，从而能够捕捉复杂的结构依赖关系。



## 核心方法与创新机理

GELATO的核心创新包括以下四个关键设计变更：

| 变更维度 | 基线方法 | GELATO的改进 | 证据来源 |
|---------|---------|-------------|---------|
| 匹配构建策略 | 一次性求解线性分配问题，所有匹配决策独立进行 | 自回归逐步构建匹配，每一步决策依赖于之前的选择 | Section 1 |
| 状态空间表示 | 使用完整的图表示，不进行约简 | 通过reduce函数移除已匹配且邻居也已匹配的节点，压缩状态空间 | Theorem 1 |
| 训练监督信号处理 | 仅将最优匹配中的节点对作为正样本 | 考虑自同构类，将最优匹配中节点对的自同构类也视为正样本 | Lemma 3 |
| 推理策略 | 单次贪婪选择 | 使用top-k集成策略，从多个起始匹配分支中选取最优解 | Section 4.4 |



![[assets/figures/papers/iclr26_0001_6ZTcLNmguc_Gelato_Graph_Edit_Distance_via_Autoregressive_Ne/figures/001_Figure_1.jpg]]
*Figure 1: Conceptual visualization of GELATO. Graph matchings are generated in a step-by-step manner. In each step, GELATO is fed autoregressively the previous partial matching, and it predicts the next source-target node pair to be matched, until every source node has been mapped.*

GELATO的整体框架包含四个核心模块，形成一个端到端的自回归匹配构建流程：

1. **图编码模块（Graph Encoding）**：将GEDFM（Graph Edit Distance with Fixed Matches）实例编码为图结构，包括源图、目标图和已匹配节点对。

2. **GNN动作预测器（GNN Action Predictor）**：使用GINE消息传递层处理编码后的图，为每对未匹配节点计算匹配分数。

3. **实例约简模块（Instance Reduction）**：在每一步匹配后，移除已匹配且邻居也已匹配的节点，压缩状态空间。

4. **自回归推理模块（Autoregressive Inference）**：逐步选择最高分的节点对进行匹配，并使用top-k集成策略探索多个起始分支。

Figure 1展示了GELATO的自回归逐步匹配过程：在每一步，GELATO自回归地接收之前的局部匹配，并预测下一个要匹配的源-目标节点对，直到所有源节点都被映射。



### 5.1 GEDFM递归定义

GELATO将GED问题形式化为顺序决策过程，其状态空间定义为GEDFM实例的集合：

$$\mathrm{GEDFM}(G_1, G_2, \mu) = \min \Big\{ c(\mu), \min_{(u,v) \in A(G_1, G_2, \mu)} \mathrm{GEDFM}(G_1, G_2, \mu \cup \{(u,v)\}) \Big\}$$

其中动作集A(G₁, G₂, μ)是任何未匹配的源节点和目标节点对。

### 5.2 实例约简（Instance Reduction）

Theorem 1保证了reduce函数的正确性：设(G₁, G₂, μ)是一个GEDFM实例，μ* ⊇ μ是该实例的最优匹配。那么，约简后的实例(G₁', G₂', μ') = reduce(G₁, G₂, μ)具有最优匹配μ* ∩ (V₁' × V₂')。这意味着约简操作不会丢失最优解，同时可以显著压缩状态空间。Figure 3展示了两个不同的GEDFM实例如何通过reduce映射到相同的更小子问题。

### 5.3 GINE消息传递层

GELATO使用GINE消息传递层进行节点表示学习，其更新公式为：

$$h_u^{\ell+1} = h_u^{\ell} + \mathrm{ReLU}\bigg(\mathrm{BatchNorm}\bigg(\mathrm{MLP}\Big(h_u^{\ell} + \sum_{v \in \mathcal{N}(u)} \mathrm{ReLU}(h_v^{\ell} + e_{v,u})\Big)\bigg)\bigg) \in \mathbb{R}^d$$

该层通过结合自身嵌入、邻居嵌入和边特征，并添加残差连接和批归一化，更新节点表示。

### 5.4 节点对匹配分数计算

对于每对未匹配节点(u, v)，通过拼接它们的最终层表示并输入MLP计算匹配分数：

$$o_{u,v} = \mathrm{MLP}\left(h_u^{\mathcal{L}} \| h_v^{\mathcal{L}}\right)$$

### 5.5 训练策略

训练采用链接预测任务的形式，其中正链接是最优匹配中尚未包含的节点对。关键创新在于处理自同构匹配：如果一对节点(u, v) ∉ μ*与一对(w, z) ∈ μ*是自同构的，那么存在另一个最优解ν*使得(u, v) ∈ ν*，因此(u, v)应被视为正链接。Figure 4展示了自同构匹配的概念。

### 5.6 推理策略

推理时采用贪婪顺序过程，并使用top-k集成策略：选择top-k个得分最高的起始节点对，每个起始对初始化一个独立的搜索分支，最终选取最优解。



## 实验与关键发现

### 6.1 主要结果

Table 1展示了GELATO与所有基线方法在六个数据集上的nMAE和EHR指标比较：

![[assets/figures/papers/iclr26_0001_6ZTcLNmguc_Gelato_Graph_Edit_Distance_via_Autoregressive_Ne/figures/009_Table_1.jpg]]
*Table 1: Overall solution quality of methods in terms of nMAE (↓) and EHR (↑) in %.*

| 数据集 | 指标 | GELATO | 最佳基线 | 改进幅度 |
|-------|------|--------|---------|---------|
| AIDS | nMAE | 0.1±0.0 | 0.8±0.1 (MIP-F2) | -0.7 |
| AIDS | EHR | 99.3±0.3 | 89.0±1.4 (MIP-F2) | +10.3 |
| LINUX | nMAE | 0.1±0.1 | 0.1±0.0 (MIP-F2) | 0.0 |
| LINUX | EHR | 99.9±0.1 | 99.9±0.1 (MIP-F2) | 0.0 |
| IMDB-16 | nMAE | 0.1±0.3 | 0.1±0.0 (MIP-F2) | 0.0 |
| IMDB-16 | EHR | 99.9±0.1 | 99.9±0.1 (MIP-F2) | 0.0 |
| ZINC-16 | nMAE | 0.7±0.1 | 1.4±0.1 (GREED) | -0.7 |
| ZINC-16 | EHR | 91.1±1.1 | 68.4±1.3 (GREED) | +22.7 |
| molhiv-16 | nMAE | 0.5±0.4 | 1.1±0.1 (GREED) | -0.6 |
| molhiv-16 | EHR | 95.3±0.8 | 72.4±1.2 (GREED) | +22.9 |
| code2-22 | nMAE | 0.6±0.4 | 1.2±0.1 (GREED) | -0.6 |
| code2-22 | EHR | 95.7±0.8 | 72.4±1.2 (GREED) | +22.9 |

GELATO在所有数据集上均达到或接近最优性能，在ZINC-16、molhiv-16和code2-22等更具挑战性的数据集上，EHR指标提升超过20个百分点。

### 6.2 泛化性能

Figure 5展示了GELATO在不同图大小上的泛化性能。训练仅在不超过16或22个节点的图上进行，但GELATO在更大图上仍能保持领先性能，且性能下降是渐进的，而非加速恶化。这表明GELATO具有良好的分布外泛化能力。

### 6.3 消融研究

Table 4的消融研究揭示了各关键组件的贡献：

![[assets/figures/papers/iclr26_0001_6ZTcLNmguc_Gelato_Graph_Edit_Distance_via_Autoregressive_Ne/figures/015_Table_4.jpg]]
*Table 4: Ablation studies of key components of GELATO. Solution quality metrics reported in %.*

- **自回归过程**：去除自回归过程（一次性预测所有匹配）导致性能显著下降，证明自回归方法是GELATO性能的关键。
- **实例约简**：去除实例约简对性能有轻微的负面影响，表明约简有助于提升预测性能。
- **自同构匹配处理**：处理自同构匹配的策略在不同数据集上效果不一，有时提升有时下降。
- **批归一化和残差连接**：Figure 7显示去除批归一化或残差连接会降低解的质量。

### 6.4 超参数研究

Figure 6（包含Figures 8-10）的超参数研究表明：
- 增大嵌入维度d、层数L和集成大小k均能提升性能，但会增加计算开销。
- 在ZINC上，将集成大小k从32增加到128，EHR从91%提升到97%。
- 在AIDS上，使用L=1（一跳邻域）时EHR仅13%，说明多跳消息传递至关重要。

### 6.5 有限监督下的性能

Table 5显示GELATO在有限或带噪声的监督下仍然有效，即使只使用10³个训练样本也能达到最优性能。这大大降低了对精确求解器生成大量训练数据的依赖。

![[assets/figures/papers/iclr26_0001_6ZTcLNmguc_Gelato_Graph_Edit_Distance_via_Autoregressive_Ne/figures/022_Table_5.jpg]]
*Table 5: Solution quality with limited supervision*

### 6.6 推理效率

Table 3显示GELATO的推理时间极短（每对图3-5毫秒），比GEDGNN、GEDHOT和MATA*等基于学习的方法快两个数量级，这得益于其GPU友好的实现。

### 6.7 实验公平性说明

- 数据集划分时确保训练集、验证集和测试集中不包含同构的图，以避免数据泄露。
- 所有ML方法的训练和评估均使用相同的训练/验证/测试划分。
- 对于每个数据集，所有方法使用相同的编辑成本函数。
- 实验结果报告了五次独立运行的平均值和标准差，以确保统计可靠性。

### 补充图表

![[assets/figures/papers/iclr26_0001_6ZTcLNmguc_Gelato_Graph_Edit_Distance_via_Autoregressive_Ne/figures/010_Table_2.jpg]]

![[assets/figures/papers/iclr26_0001_6ZTcLNmguc_Gelato_Graph_Edit_Distance_via_Autoregressive_Ne/figures/011_Table_2.jpg]]
*Table 2: Solution quality on edgeunlabeled graphs. Eval. metrics in %. Table 3: Average inference runtime per graph pair (ms).*



## 定位与知识库关联

### 7.1 与现有方法的关系

GELATO属于神经组合优化（Neural Combinatorial Optimization）领域，具体针对图编辑距离问题。与现有方法相比：

- **与线性分配方法（如GEDGNN、GEDHOT）的区别**：这些方法假设匹配决策独立，无法捕捉依赖关系。GELATO通过自回归过程克服了这一限制。
- **与基于A*搜索的方法（如MATA*）的区别**：这些方法需要启发式函数指导搜索，GELATO直接构建完整匹配。
- **与RGM（Liu et al., 2023a）的区别**：RGM也顺序预测节点匹配，但使用更昂贵的乘积图，且不利用Theorem 1的搜索空间约简。此外，RGM使用强化学习训练，而GELATO使用监督学习。

### 7.2 局限性

1. GELATO依赖于从精确求解器（如MIP-F2）获得的最优匹配进行监督训练，这本身是NP-hard的，限制了其在更大图上的应用。
2. 自回归推理过程是顺序的，无法像线性分配方法那样完全并行化，尽管GPU友好的实现使其仍然很快。
3. 当前的集成策略（top-k）是简单的，更复杂的推理策略（如beam search）可能进一步提升性能。
4. 模型在具有不同特征空间的标签图之间进行迁移学习时，性能下降显著，表明其泛化能力受限于特征空间的一致性。
5. 对于无标签图（如LINUX和IMDB-16），GELATO的性能提升相对较小，因为拓扑结构信息有限。

### 7.3 开放问题

1. 能否使用强化学习来消除对最优匹配监督的依赖，从而扩展到更大规模的图？
2. GELATO能否被集成到分支定界方法中，以加速精确GED求解？
3. 更复杂的推理策略（如beam search）能否进一步提升GELATO的性能？
4. GELATO在具有不同特征空间的图之间进行迁移学习时，如何更好地泛化？
5. GELATO的架构能否扩展到其他组合优化问题，如旅行商问题（TSP）或车辆路径问题（VRP）？



## 原文 PDF

![[paperPDFs/ICLR_2026/Gelato_Graph_Edit_Distance_via_Autoregressive_Neural_Combinatorial_Optimization.pdf]]
