---
title: "Exchangeability of GNN Representations with Applications to Graph Retrieval"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Exchangeability_of_GNN_Representations_with_Applications_to_Graph_Retrieval.pdf
project_link: https://rebrand.ly/graphhash
code_link: null
openreview_forum_id: HQcCd0laFq
aliases:
- EGRAGR
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "训练好的图神经网络（GNN）输出的节点嵌入矩阵，其列（维度方向）是随机初始化诱导的可交换随机变量。"
primary_logic: "利用节点嵌入元素的交换性，将高维运输相似度近似为各维度上排序后嵌入向量差的欧氏相似度，从而可将任意随机超平面LSH直接应用于图，首次为不对称图相似度量（子图匹配、GED等）提供统一的、亚线性检索框架。"
claims:
- "在标准随机初始化、置换不变损失和常规优化器下，训练好的GNN节点嵌入矩阵的列是可交换的随机变量（Theorem 5）。"
- "可交换性使单维度运输相似度可简化为排序后标量的差值（式(4)），且多维度平均集中在真实运输相似度附近（Proposition 7）。"
- "基于交换性的相似度近似允许直接使用随机超平面LSH，并首次证明该哈希方案是原始运输相似度的有效LSH（Theorem 18）。"
- "在四个数据集上，GRAPHHASH在子图匹配和GED两种任务下，MAP/NDCG与检索数量的折衷曲线一致优于FourierHashNet、随机超平面、IVF、DiskANN等基线（Figure 4, Figure 24, Figure 25）。"
---

# Exchangeability of GNN Representations with Applications to Graph Retrieval

> [!tip] 核心洞察
> 利用节点嵌入元素的交换性，将高维运输相似度近似为各维度上排序后嵌入向量差的欧氏相似度，从而可将任意随机超平面LSH直接应用于图，首次为不对称图相似度量（子图匹配、GED等）提供统一的、亚线性检索框架。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GNN表示的可交换性及其在图检索中的应用 |
| 英文题名 | Exchangeability of GNN Representations with Applications to Graph Retrieval |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=HQcCd0laFq) · [Project](https://rebrand.ly/graphhash) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | GRAPHHASH |
| Dataset | cox2 (Subgraph Matching), ptc-fm (GED) |

> [!tip] 效果简介
> - cox2 (Subgraph Matching) 上，MAP (vs. #retrieved graphs) 为 GRAPHHASH 在所有检索预算下 MAP 最高，尤其在低检索量时优势显著，对比 FourierHashNet 在大部分选择度区间无法超越50%穷举MAP；RH 方差大；IVF/DiskANN 性能低，变化 GRAPHHASH 的 MAP-检索量曲线全面位于其他方法上方。
> - ptc-fm (GED) 上，NDCG@1000 (vs. #retrieved graphs) 为 GRAPHHASH 的 NDCG 曲线显著高于所有基线，对比 RH 在某些点接近但方差大；FourierHashNet 未能覆盖全选择度，变化 GRAPHHASH 提供了更平滑且完整的精度-效率折衷。

## 概要

**核心问题**：基于最优运输的图相似度量（如子图匹配、图编辑距离 GED）能精确刻画图结构间的非对称关系，但其精确计算复杂度高达 $O(n^3)$，无法直接应用于大规模图检索中的局部敏感哈希（LSH）索引，导致检索效率与精度之间存在根本性矛盾。

**核心发现**：在标准随机初始化、置换不变损失函数和常规优化器（SGD/Adam）下训练得到的图神经网络（GNN）节点嵌入矩阵，其列（嵌入维度方向）是可交换的随机变量（Theorem 5）。这一理论性质将高维节点嵌入集合间的最优运输相似度，近似为各维度内排序后嵌入向量差的欧氏相似度（式(4)），且该近似以高概率集中在真实运输相似度附近（Proposition 7）。

**方法定位**：基于上述交换性，**GRAPHHASH** 首次为子图匹配和 GED 等非对称图相似度量提供了统一的亚线性检索框架。其核心管线为：对 GNN 输出的节点嵌入矩阵逐维排序后应用 Fourier 特征映射，构造结构化哈希向量，再利用随机超平面 LSH 生成二值哈希码（Theorem 18 证明该哈希方案是原始运输相似度的有效 LSH）。该方法将传统图检索从“图级别单一向量+对称相似度”范式，推进到“节点嵌入集合+运输相似度近似”范式。

**主要结果**：在 cox2、ptc-fm 等四个数据集上，GRAPHHASH 在子图匹配和 GED 两种任务下的 MAP/NDCG 与检索数量的折衷曲线一致优于 FourierHashNet、随机超平面 LSH、IVF 和 DiskANN 等基线（Figure 4），尤其在低检索预算下优势显著。百万级语料库的可扩展性实验（Figure 15）验证了方法的实用性。

**方法谱系与知识库定位**：GRAPHHASH 的基线对比包括 **FourierHashNet**（Roy et al., 2023，基于图级别嵌入和 Fourier 特征近似 hinge 距离的非对称哈希）、**Random Hyperplane**（Charikar, 2002，经典余弦相似度 LSH 应用于图级别平均池化向量）、**IVF**（Douze et al., 2024，基于倒排文件的 ANN 索引）和 **DiskANN**（Simhadri et al., 2023，基于图的 ANN 索引）。其中 IVF 和 DiskANN 使用多向量索引但依赖对称相似度（L2/余弦），在非对称任务上表现受限。GRAPHHASH 的核心创新在于将可交换性这一理论性质转化为索引能力，使任意随机超平面 LSH 可直接应用于图，填补了非对称图相似度高效检索的方法空白。

**局限性**：交换性的理论推导依赖于参数层内独立同分布初始化、损失函数对嵌入维度置换不变，以及优化器更新逐元素可分离等假设，超出该设定时仍需验证；当前方法假设查询图和语料图具有相同节点数（通过填充），节点数差异极大时近似质量可能下降；嵌入维度 $D$ 和 Fourier 采样数 $M$ 需充分大以保证近似精度，实际应用中需仔细调节。

图结构数据上的相似度检索是药物发现、分子性质预测、程序分析等领域的核心操作。给定一个查询图，系统需要从大规模语料库中高效地找出与之最相关的图。然而，图之间的相似度往往是非对称的——例如，子图匹配（Subgraph Matching, SM）判定查询图是否为语料图的子结构，图编辑距离（Graph Edit Distance, GED）衡量将一个图转换为另一个图所需的最小编辑代价。这些非对称的、基于最优运输的相似度度量，其精确计算通常涉及求解匹配问题，计算复杂度高达 $O(n^3)$，难以直接应用于大规模检索场景。

现有的大规模近似检索方法，如局部敏感哈希（LSH），通常依赖图级别的单一向量表示（如对节点嵌入做平均池化）来计算余弦相似度。然而，将图压缩为单一向量会丢失细粒度的节点对应信息，导致这些方法无法有效捕获非对称的运输相似度。**FourierHashNet**（Roy et al., 2023）尝试通过 Fourier 特征近似 hinge 距离来处理非对称图相似度，但其基于图级别嵌入的方案在子图匹配任务上表现有限，MAP 曲线常停滞在穷举检索 MAP 的 50% 以下，且无法覆盖完整的检索选择度谱。

核心瓶颈在于：**高维节点嵌入之间的最优运输相似度计算开销大，难以直接与现有的 LSH 索引框架兼容**。若能将运输相似度近似为某种简单的欧氏空间相似度，就可以复用成熟的随机超平面 LSH 方案，从而首次为非对称图相似度量提供统一的亚线性检索框架。

本文的关键洞察源于对训练好的图神经网络（GNN）节点嵌入矩阵的一个结构性质观察：**嵌入矩阵的列（即不同嵌入维度）在随机初始化诱导下，表现为可交换的随机变量**。这一性质意味着，在一维嵌入上，两个节点集合之间的最优运输距离可以通过对各自集合内的标量值排序后直接匹配来精确求解。将这一观察推广到多维嵌入，就可以将高维运输相似度分解为各维度上排序向量差的聚合，从而将其转化为欧氏空间中的近似，使得随机超平面 LSH 可直接应用于图检索。

## 核心方法与创新机理

GRAPHHASH 的核心创新在于**发现并利用了训练好的 GNN 节点嵌入矩阵在维度方向上的可交换性**，从而将高维最优运输相似度近似为各维度内排序后向量的欧氏相似度，使任意随机超平面局部敏感哈希（LSH）可直接应用于图结构数据。这一发现首次为子图匹配、图编辑距离（GED）等非对称图相似度量提供了统一的亚线性检索框架。

### 关键机制：从可交换性到高效哈希

**瓶颈**：基于最优运输的图相似度（如子图匹配的 hinge 距离、GED）计算涉及高维节点嵌入之间的最优匹配，精确算法复杂度为 $O(n^3)$，无法直接用于大规模图检索的 LSH 索引构建。

**因果旋钮**：论文证明，在标准随机初始化、置换不变损失函数和逐元素可分离优化器（如 SGD、Adam）下，训练好的 GNN 输出的节点嵌入矩阵 $X \in \mathbb{R}^{n \times D}$ 的列（即 $X[:,1], \dots, X[:,D]$）是**可交换的随机变量**（Theorem 5）。这意味着各维度的嵌入分布在统计上不可区分，其联合密度满足 $p(X) = p(X\pi)$，其中 $\pi$ 为任意维度置换。

**核心洞察**：可交换性使得单维度上的最优运输问题退化为排序后标量的简单匹配。具体而言，高维运输相似度：

$$\mathrm{sim}(G_c, G_q) = \max_{P \in \mathcal{P}_n} \sum_{u,u'} \sum_{d \in [D]} s\big(x^{(q)}(u)[d] - x^{(c)}(u')[d]\big) \cdot P[u,u']$$

在可交换性假设下，可通过各维度独立近似：

$$\mathrm{sim}_d(G_c, G_q) = s\big(\mathrm{SORT}(X^{(q)}[:,d]) - \mathrm{SORT}(X^{(c)}[:,d])\big)$$

且多维度平均以高概率集中在真实运输相似度附近（Proposition 7）。这一近似将原本不可分解的运输代价转化为各维度上排序向量差的得分，进而通过 Fourier 特征映射构造结构化哈希向量，使其内积近似 $\mathrm{sim}_d$。最终，随机超平面投影可直接应用于这些向量生成二值哈希码，并首次被证明是原始运输相似度的有效 LSH（Theorem 18）。

### 相对基线的 changed slots

| 设计维度 | 基线方法 | GRAPHHASH |
|---------|---------|-----------|
| **图相似度量** | 对称或非对称距离（余弦相似度、hinge 距离）在图级别池化向量上计算 | 基于最优运输的非对称距离通过可交换性近似为各维度排序后向量的得分，转化为欧氏空间中的余弦相似度 |
| **图表示形式** | 图级别单一向量（如 GEN 平均池化） | 节点嵌入集合，经维内排序和 Fourier 变换构造结构化哈希向量 |

**基线方法对比**：
- **FourierHashNet**（Roy et al., 2023）使用图级别嵌入和 Fourier 特征近似 hinge 距离，但依赖对称的图级别表示，无法有效捕获非对称的运输相似度。
- **随机超平面 LSH**（Charikar, 2002）直接应用于图级别平均池化向量，仅能编码对称的余弦相似度。
- **IVF**（Douze et al., 2024）和 **DiskANN**（Simhadri et al., 2023）使用多向量索引（每个图多个节点嵌入），但依赖 L2/余弦等对称距离，在非对称任务上表现不佳。

GRAPHHASH 通过可交换性桥接了“节点级嵌入的运输相似度”与“欧氏空间的哈希索引”之间的鸿沟，使得原本 $O(n^3)$ 的精确运输代价可被 $O(D \cdot n \log n + M)$ 的排序与 Fourier 采样近似，并支持亚线性的哈希桶检索。

### 证据强度

- **可交换性理论**：在 i.i.d. 初始化、置换不变损失和 SGD/Adam 优化器下严格成立（Lemma 2-4, Theorem 5），置信度 0.95。
- **近似集中性**：单维度相似度以高概率集中在真实运输相似度附近（Proposition 7），消融实验显示平均绝对误差随嵌入维度 $D$ 增大而减小（Figure 23），置信度 0.9。
- **哈希有效性**：随机超平面 LSH 被证明是原始运输相似度的有效 LSH（Theorem 18），置信度 0.95。
- **实证验证**：MMD 检验确认节点嵌入的真实分布与置换后分布无统计差异（Table 2），且平均嵌入矩阵坍缩为秩一矩阵（Figure 3），置信度 0.95。

### 局限与待验证点

- 可交换性的理论推导假设参数在层内独立同分布初始化，超出该设定（如预训练模型、自适应优化器）时是否保持交换性仍需验证。
- 当前方法假设查询图和语料图具有相同节点数（通过填充），节点数差异极大时排序相似度的近似质量可能下降。
- 近似质量依赖于嵌入维度 $D$ 和 Fourier 采样数 $M$ 的充分大，实际应用中需仔细调节这些超参数。

GRAPHHASH 的核心目标是为大规模图语料库上的非对称图检索任务（如子图匹配、图编辑距离）提供统一的亚线性检索框架。其整体 pipeline 由五个关键模块串联构成，输入为查询图 $G_q$ 和语料图集 $\{G_c\}$，输出为按运输相似度排序的候选图列表。

### 瓶颈与核心思路

传统基于最优运输的图相似度（式(1)）计算开销极大——精确算法复杂度为 $O(n^3)$，无法直接用于大规模检索的局部敏感哈希（LSH）索引。GRAPHHASH 的核心洞察在于：**训练好的 GNN 输出的节点嵌入矩阵，其列（维度方向）是随机初始化诱导的可交换随机变量**（Theorem 5）。这一性质使得高维运输相似度可被分解为各维度上排序后嵌入向量差的欧氏相似度的均值，且该均值以高概率集中在真实运输相似度附近（Proposition 7）。

### 模块关系与数据流

整个 pipeline 遵循“编码 → 排序 → Fourier 特征映射 → 哈希投影 → 桶检索”的流程：

1. **GNN 编码器（GNN_encoder）**：给定输入图 $G$，GNN 模型 $\text{GNN}_\theta$ 计算所有节点的 $D$ 维嵌入矩阵 $\mathbf{X} = [\mathbf{x}(u)] \in \mathbb{R}^{n \times D}$。该模块的输出是后续所有操作的基础表示，其列的可交换性是整个方法的理论前提。

2. **顺序统计量提取（OrderStat）**：对查询图和语料图的嵌入矩阵，在每一维度 $d$ 内分别进行降序排序，得到排序向量 $\text{SORT}(\mathbf{X}^{(q)}[:,d])$ 和 $\text{SORT}(\mathbf{X}^{(c)}[:,d])$。基于可交换性，单维度运输相似度可精确表示为排序向量差值的得分函数：
   $$\text{sim}_d(G_c, G_q) = s\big(\text{SORT}(\mathbf{X}^{(q)}[:,d]) - \text{SORT}(\mathbf{X}^{(c)}[:,d])\big)$$
   其中 $s(\cdot) = \rho_{\max} - \rho(\cdot)$ 为从运输成本 $\rho$ 导出的得分函数。

3. **Fourier 特征近似（FourierFeatureApprox）**：对每个维度的排序向量应用 Fourier 特征映射并采样 $M$ 个频率，构造结构化向量 $\widehat{\mathbf{T}}_{q,d}$ 和 $\widehat{\mathbf{T}}_{c,d}$，使其内积近似该维度的运输相似度：
   $$\text{sim}_d(G_c, G_q) = \mathbb{E}_{\omega_1,\ldots,\omega_n \sim p(\cdot)}[\mathbf{T}_{q,d}(\omega)^\top \mathbf{T}_{c,d}(\omega)]$$
   通过蒙特卡洛采样，将期望转化为可计算的向量内积。

4. **随机超平面哈希（RandomHyperplaneLSH）**：将各维度的 Fourier 向量拼接为 $\widehat{\mathbf{T}}_{\cdot,d}$，对其应用随机超平面投影生成二值哈希码：
   $$h^{(d)}(G_c) = \text{sign}(\mathbf{W} \widehat{\mathbf{T}}_{c,d})$$
   论文首次证明该哈希方案是原始运输相似度的有效 LSH（Theorem 18）。

5. **索引与检索（IndexRetrieve）**：在索引阶段，将语料图按其哈希码存入对应桶中；查询时，仅检索与查询图落入相同桶的语料图，实现亚线性检索复杂度。

### 关键设计选择

- **非对称相似度支持**：通过运输相似度框架（式(1)），统一了子图匹配（$\rho(\cdot) = [\cdot]_+$）和图编辑距离（$\rho(\cdot) = |\cdot|$）等非对称度量，而传统方法（如 FourierHashNet、随机超平面）依赖图级别的对称相似度。
- **多维度聚合的集中性**：Proposition 7 保证了当嵌入维度 $D$ 足够大时，$\frac{1}{D}\sum_d \text{sim}_d$ 以高概率集中在真实运输相似度附近，这为将高维问题分解为可并行的单维度近似提供了理论保障。
- **超参数依赖**：方法性能依赖于嵌入维度 $D$ 和 Fourier 采样数 $M$ 的充分大（理论上有下界 $D > 1/(\epsilon^2\delta)$），实际应用中这些超参数需要仔细调节以获得最优的精度-效率折衷。

### 整体管线

GRAPHHASH 的核心思路是将图检索问题转化为一个可哈希的向量检索问题。其处理管线由以下模块串联构成：

1. **GNN_encoder**：对查询图 $G_q$ 和语料图 $G_c$ 分别运行训练好的图神经网络 $\text{GNN}_\theta$，输出节点嵌入矩阵 $\mathbf{X}^{(q)}, \mathbf{X}^{(c)} \in \mathbb{R}^{n \times D}$。
2. **OrderStat**：在每一维度 $d \in [D]$ 内，对节点嵌入值进行降序排序，得到排序向量 $\text{SORT}(\mathbf{X}^{(\cdot)}[:,d])$。
3. **FourierFeatureApprox**：对排序向量施加 Fourier 特征映射并采样 $M$ 个频率，构造向量 $\widehat{\mathbf{T}}_{\cdot,d}$，使其内积近似单维度运输相似度。
4. **RandomHyperplaneLSH**：将各维度的 $\widehat{\mathbf{T}}_{\cdot,d}$ 拼接后，通过随机超平面投影生成二值哈希码 $h^{(d)}(G)$。
5. **IndexRetrieve**：将语料图存入哈希桶，查询时仅检索与查询图落入同一桶的候选图。

### 关键公式

#### 基于最优运输的图相关性距离

论文将子图匹配（hinge 损失）和图编辑距离统一为如下运输距离：

$$\Delta(G_c, G_q) = \min_{P \in \mathcal{P}_n} \sum_{u,u'} \sum_{d \in [D]} \rho\big( x^{(q)}(u)[d] - x^{(c)}(u')[d] \big) \cdot P[u,u']$$

其中 $\rho$ 为凸成本函数（子图匹配时取 $\rho(\cdot) = [\cdot]_+$，GED 时取 $\rho(\cdot) = |\cdot|$），$P$ 为置换矩阵，$n$ 为节点数。对应的相似度定义为：

$$\text{sim}(G_c, G_q) = \max_{P \in \mathcal{P}_n} \sum_{u,u'} \sum_{d \in [D]} s\big( x^{(q)}(u)[d] - x^{(c)}(u')[d] \big) \cdot P[u,u']$$

其中 $s(x) = \rho_{\max} - \rho(x)$ 为得分函数。

#### 单维度相似度近似

利用节点嵌入的可交换性（Theorem 5），高维运输相似度可分解为各维度独立贡献之和。在单维度上，最优运输问题退化为排序后逐元素匹配：

$$\text{sim}_d(G_c, G_q) = s\big( \text{SORT}(\mathbf{X}^{(q)}[:,d]) - \text{SORT}(\mathbf{X}^{(c)}[:,d]) \big)$$

这里 $\text{SORT}(\cdot)$ 表示对向量元素降序排列，$s(\cdot)$ 逐元素作用后求和。

#### 集中性保证

单维度相似度 $\text{sim}_d$ 以高概率集中在平均相似度 $\frac{1}{D}\text{sim}(G_c, G_q)$ 附近：

$$\Pr\Big( \big| \frac{1}{D}\text{sim}(G_c, G_q) - \text{sim}_d(G_c, G_q) \big| \leq \epsilon \Big) \geq 1 - \beta_0\delta, \quad D > \frac{1}{\epsilon^2\delta}$$

该结论由 Proposition 7 给出，意味着当嵌入维度 $D$ 充分大时，任一维度的排序相似度都是整体运输相似度的良好近似。

#### Fourier 特征近似

为将排序相似度转化为可哈希的向量内积形式，对排序向量施加 Fourier 变换。令 $\omega_1, \ldots, \omega_n$ 从分布 $p(\cdot)$ 中采样，构造向量 $\mathbf{T}_{\cdot,d}(\omega)$，满足：

$$\text{sim}_d(G_c, G_q) = \mathbb{E}_{\omega_1,\ldots,\omega_n \sim p(\cdot)} \big[ \mathbf{T}_{q,d}(\omega)^\top \mathbf{T}_{c,d}(\omega) \big]$$

实际使用 $M$ 个频率样本的拼接向量 $\widehat{\mathbf{T}}_{\cdot,d}$，使得：

$$\text{sim}_d(G_c, G_q) \propto \cos(\widehat{\mathbf{T}}_{q,d}, \widehat{\mathbf{T}}_{c,d})$$

至此，图间运输相似度被转化为欧氏空间中的余弦相似度，可直接应用随机超平面 LSH（Theorem 18 证明了该哈希方案是原始运输相似度的有效 LSH）。

#### 可交换性的形式化

查询图和语料图的拼接嵌入矩阵 $\mathbf{Y} = [\mathbf{X}^{(q)}; \mathbf{X}^{(c)}]$ 满足维度可交换性：

$$p(\mathbf{Y}) = p(\mathbf{Y}\pi)$$

其中 $\pi$ 为任意维度置换（Proposition 6）。该性质保证了单维度近似在整个嵌入空间中的统计一致性。

## 实验与关键发现

### 核心瓶颈与实验动机

图检索中，基于最优运输的相似度（如子图匹配、图编辑距离）能更准确地刻画图间非对称关系，但精确计算复杂度为 $O(n^3)$，无法直接用于大规模语料库的局部敏感哈希（LSH）索引。现有图检索方法多依赖对称的图级别向量相似度，在非对称任务上存在根本性局限。GRAPHHASH 的核心假设是：训练好的 GNN 节点嵌入矩阵的列（维度方向）是可交换随机变量，这一性质使得高维运输相似度可被分解为各维度排序后向量的欧氏相似度，从而首次将随机超平面 LSH 直接应用于非对称图相似度量。

实验需验证三个递进层次：（1）可交换性是否在真实训练中成立；（2）基于交换性的相似度近似是否准确；（3）整套哈希检索框架是否在精度-效率折衷上超越基线。

### 可交换性的实证验证

**Figure 1** 展示了 cox2 数据集上一个语料图节点嵌入的单维度概率密度，基于 5000 个独立训练的 GNN 实例估计。初始化阶段各维度密度已高度重叠，训练过程中（epoch 8、epoch 20）这种重叠持续保持，表明边际分布的可交换性在训练动力学中是稳定的。

**Table 2** 给出了更严格的统计检验：对原始嵌入分布 $p_X$ 与维度置换后的分布 $p_{X\pi}$ 计算无偏 MMD²。在 cox2 数据集上，子图匹配（SM）任务的 MMD² 为 $-1.18\times10^{-6} \pm 3.28\times10^{-5}$，GED 任务为 $-3.89\times10^{-5} \pm 2.69\times10^{-5}$，均未显著偏离零，确认两个分布在统计上不可区分。

**Figure 3** 进一步揭示了一个更强的结构性质：跨初始化平均后的嵌入矩阵坍缩为秩一矩阵——主导奇异值占比 $\sigma_1^2 / \sum \sigma_i^2$ 收敛到 1。这为交换性提供了几何解释：不同维度承载的是同一潜在表示的随机置换副本。

### 主实验结果

**Figure 4**（正文）和 **Figure 24-25**（附录 H.2.8）展示了 GRAPHHASH 与五个基线在四个数据集上的核心折衷曲线。横轴为检索图数量，纵轴为检索质量（SM 任务用 MAP，GED 任务用 NDCG@1000）。

在 cox2 子图匹配任务上，GRAPHHASH 的 MAP-检索量曲线在所有检索预算下均位于其他方法上方，尤其在低检索量区间优势显著——当仅检索约 10 个图时，GRAPHHASH 的 MAP 已接近穷举检索的 50%，而 **FourierHashNet**（Roy et al., 2023）在大部分选择度区间无法超越该阈值。随机超平面（RH）方法虽然在某些点接近，但方差显著更大。

在 ptc-fm 的 GED 任务上，GRAPHHASH 的 NDCG 曲线同样全面优于所有基线。值得注意的是，**IVF**（Douze et al., 2024）和 **DiskANN**（Simhadri et al., 2023）虽然使用了多向量索引（每个图多个节点嵌入），但它们依赖对称相似度（L2、余弦），在非对称的 GED 任务上表现不佳，这从反面验证了运输相似度对非对称任务的关键作用。

**Figure 15** 将语料库规模扩展到百万级，GRAPHHASH 的精度优势依然保持，证明该方法具备实际可扩展性。

### 消融实验

**哈希码长度**（Figure 5, Figure 16）：哈希码维度 $\text{dim}_h$ 在 10 附近时检索 AUC 最优。过短的哈希码区分能力不足，过长的哈希码导致桶过于稀疏，召回率下降。这一最优值在四个数据集和两种任务上表现一致。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_HQcCd0laFq/figures/022_Figure_5.jpg]]
*Figure 5: Performance of GRAPHHASH across different choices for dimh, the size of the hashcode. We summarize the trade-off plot between MAP and the number of retrieved graphs by computing the area under the curve after normalizing the x-axis. We observe that the optimal size is around dim $\mathrm { l } _ { h }$ = 1 0 across datasets and tasks*

**嵌入维度**（Figure 17）：GNN 输出嵌入维度 $D$ 增加时，穷举检索的 MAP 单调上升，验证了 Proposition 7 的集中性理论——更大的 $D$ 使单维度相似度更准确地集中在真实运输相似度附近。

**哈希表数量**（Figure 18）：从 10 降至 7 时性能下降不显著，降至 5 时明显降低。这表明 GRAPHHASH 对哈希表数量有一定容忍度，但过少会损害召回率。

**随机超平面播种稳定性**（Table 19, Figure 20）：10 次不同随机种子的 AUC 标准差极小，说明随机超平面投影的播种对最终检索性能影响不大，方法具有高稳定性。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_HQcCd0laFq/figures/092_Table_19.jpg]]
*Table 19: Mean and standard deviation of AUC over 10 different random seeds for RH seeding*

**Fourier 频率数**（Figure 21）：频率采样数 $M$ 低于 10 时 AUC 急剧下降，超过 10 后收益递减。这与理论分析一致——需要足够的频率采样来准确近似运输相似度的期望形式。

**集中性验证**（Figure 23）：单维度相似度 $\text{sim}_d$ 与真实运输相似度 $\text{sim}$ 之间的平均绝对误差随 $D$ 增大而显著减小，直接验证了 Proposition 7 的集中不等式。

### 失败模式与局限

1. **节点数差异敏感性**：当前方法假设查询图和语料图具有相同节点数（通过填充实现）。对于节点数差异极大的图对，排序相似度的近似质量可能下降，因为填充节点会引入虚假的排序匹配。

2. **超参数依赖**：运输相似度的近似质量依赖于嵌入维度 $D$ 和 Fourier 采样数 $M$ 的充分大（理论上有下界 $D > 1/(\epsilon^2\delta)$）。在实际部署中，这些超参数需要在精度和计算开销之间仔细调节。

3. **初始化假设的边界**：可交换性的理论推导假设参数在层内独立同分布初始化、损失函数对嵌入维度置换不变，且优化器更新是逐元素可分离的（如 SGD/Adam）。尽管论文声称可扩展到更宽范围，但在预训练模型或自适应优化器下的行为仍需验证。

4. **公平性说明**：所有基线方法均在其原生评分函数下评估——FourierHashNet 使用基于 hinge 损失的图级别嵌入，随机超平面使用余弦相似度训练的图级别嵌入，GRAPHHASH 使用运输距离训练的节点级嵌入。这种设置保证了各方法在其设计假设下的最优表现，但也意味着性能差异部分源于相似度定义本身的不同。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_HQcCd0laFq/figures/023_Table_6.jpg]]
*Table 6: Graph statistics for each dataset generated for Subgraph Matching (SM)*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_HQcCd0laFq/figures/024_Table_7.jpg]]
*Table 7: Graph statistics for each dataset generated for GED*

## 定位与知识库关联

### 核心方法定位

GRAPHHASH 的核心贡献在于首次为**非对称图相似度量**（子图匹配、图编辑距离等）提供了统一的局部敏感哈希（LSH）框架。传统图检索方法依赖图级别池化向量（如平均池化）上的对称相似度（余弦、L2），而 GRAPHHASH 通过揭示训练后 GNN 节点嵌入的**可交换性**，将高维最优运输相似度近似为各维度排序后向量的欧氏相似度，从而将经典随机超平面 LSH 直接应用于图结构数据。

### 与基线方法的关系

#### 基于图级别嵌入的哈希方法

- **Random Hyperplane (RH)**（Charikar, 2002; Indyk et al., 1997）：经典余弦相似度 LSH，直接应用于图级别平均池化向量。RH 在对称相似度任务上有效，但无法处理子图匹配和 GED 等非对称度量。实验显示 RH 在某些检索预算点接近 GRAPHHASH，但方差显著更大。

- **FourierHashNet**（Roy et al., 2023）：基于图级别嵌入的非对称哈希方法，使用 Fourier 特征近似 hinge 距离。这是与 GRAPHHASH 最直接相关的基线，两者都使用 Fourier 变换构造哈希向量。关键差异在于：FourierHashNet 操作在图级别单一向量上，而 GRAPHHASH 操作在节点嵌入集合的排序统计量上，后者由可交换性理论保证其近似质量。实验表明 FourierHashNet 在大部分选择度区间无法超越 50% 穷举 MAP，而 GRAPHHASH 在所有检索预算下均表现最优。

#### 基于多向量索引的 ANN 方法

- **IVF**（Douze et al., 2024）：基于倒排文件索引的近似最近邻方法，使用节点级嵌入的 L2 距离。

- **DiskANN**（Simhadri et al., 2023）：基于图的 ANN 索引，使用节点级嵌入的 L2/余弦距离。

IVF 和 DiskANN 虽能利用多向量表示（每个图多个节点嵌入），但依赖对称相似度，因此在非对称任务上性能显著低于 GRAPHHASH。这从反面验证了 GRAPHHASH 的核心洞察：**非对称检索需要非对称的索引机制**。

### 适用边界与局限

1. **初始化假设的约束**：可交换性的理论推导假设 GNN 参数在层内独立同分布初始化，损失函数对嵌入维度置换不变，且优化器更新是逐元素可分离的（如 SGD、Adam）。论文声称可扩展到更宽范围，但超出该设定时交换性是否保持仍待验证。

2. **节点数差异的敏感性**：当前方法假设查询图和语料图具有相同节点数（通过填充实现）。当节点数差异极大时，排序相似度的近似质量可能下降——填充引入的零值会扭曲排序统计量的分布。

3. **超参数依赖**：运输相似度的近似质量依赖嵌入维度 $D$ 和 Fourier 采样数 $M$ 的充分大。理论上有下界约束（Proposition 7 给出 $D > 1/(\epsilon^2\delta)$），实际应用中这些超参数需要仔细调节。消融实验显示 $M$ 低于 10 时检索 AUC 急剧下降，哈希码长度在 10 附近最优。

4. **损失函数的不变性假设**：可交换性证明依赖损失函数对嵌入维度置换的不变性。论文指出即使损失本身非置换不变，若在中间表示置换和参数变换的联合作用下保持不变，结论仍成立，但这一扩展的适用范围未经验证。

### 开放问题

1. **可交换性对 GNN 学习动力学的深层影响**：可交换性是否会影响表征多样性、灾难性遗忘或模式坍缩？当前工作仅将交换性用作检索工具，未探索其对模型训练本身的反馈效应。

2. **向三维结构数据的扩展**：该方法能否扩展到三维分子结构或 3D 物体的图表示？这需要重新审视节点嵌入的几何语义与排序操作之间的兼容性。

3. **预训练模型与自适应优化器下的保持性**：在不依赖 i.i.d. 初始化假设的预训练模型（如大规模分子预训练 GNN）或自适应优化器（如 LAMB）中，交换性是否仍然保持？这直接决定了 GRAPHHASH 能否融入现有模型生态。

4. **更广泛的不对称相似度函数**：当前框架统一了子图匹配（hinge 损失）和 GED，但理论上任何凸成本函数 $\rho$ 均可纳入。对其他非对称图核（如 Weisfeiler-Lehman 子树核的非对称变体）的适用性值得探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/Exchangeability_of_GNN_Representations_with_Applications_to_Graph_Retrieval.pdf]]
