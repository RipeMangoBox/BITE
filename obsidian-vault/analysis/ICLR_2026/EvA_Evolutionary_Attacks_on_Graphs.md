---
title: "EvA: Evolutionary Attacks on Graphs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EvA_Evolutionary_Attacks_on_Graphs.pdf
project_link: null
code_link: null
openreview_forum_id: EzXzGRngYb
aliases:
- EEA
- EvA
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/graph_neural_networks
core_operator: "直接求解原始离散组合优化问题，采用精心设计的遗传算法（稀疏编码、自适应目标突变、分治策略）在离散空间中进行无梯度搜索。"
primary_logic: "通过约束搜索空间到攻击节点的感受野、使用准确率作为适应度函数、引入自适应目标突变，遗传算法能够高效探索扰动空间，避免梯度信息带来的误导（非线性、非凸、局部性），从而显著超越当前基于梯度的最强攻击。"
claims:
- "EvA在CoraML等多数据集上使准确率额外下降约11%（与之前最佳攻击PRBCD相比）。"
- "梯度是局部度量，无法正确反映离散边翻转的真实损失变化，且忽略边之间的相互作用（单独翻转与联合翻转效果可能相反）。"
- "自适应目标突变（ATM）和准确率适应度函数从基础遗传算法大幅提升了攻击有效性。"
- "CoraML 上 Classification Accuracy (%) = 52.95"
---

# EvA: Evolutionary Attacks on Graphs

> [!tip] 核心洞察
> 通过约束搜索空间到攻击节点的感受野、使用准确率作为适应度函数、引入自适应目标突变，遗传算法能够高效探索扰动空间，避免梯度信息带来的误导（非线性、非凸、局部性），从而显著超越当前基于梯度的最强攻击。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | EvA：图上的进化攻击 |
| 英文题名 | EvA: Evolutionary Attacks on Graphs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=EzXzGRngYb) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/graph_neural_networks |
| Method | EvA (Evolutionary Attack) |
| Dataset | CoraML, Pubmed, CoraML (Defense: GCN-SVD, ε=0.10), Ogbn-Arxiv (with D&C) |

> [!tip] 效果简介
> - CoraML 上，Classification Accuracy (%) 为 52.95，对比 PRBCD: 66.48，变化 -13.53 (EvA achieves lower accuracy, i.e., stronger attack)。
> - Pubmed 上，Classification Accuracy (%) 为 40.46，对比 PRBCD: 49.32，变化 -8.86 (ε=0.15)。
> - CoraML (Defense: GCN-SVD, ε=0.10) 上，Accuracy 为 0.41，对比 PRBCD: 0.70，变化 -0.29 (EvA breaks defense more effectively)。

## 概要

图上的对抗攻击旨在通过翻转少量边，最大化目标模型在被攻击节点上的分类错误率。现有主流方法（如PRBCD）将这一离散组合优化问题松弛为连续空间，利用梯度信息搜索扰动。然而，梯度是局部度量，无法准确反映离散边翻转的真实损失变化，且边之间的相互作用（单独翻转与联合翻转效果可能相反）进一步导致梯度引导失效。这一瓶颈使得基于梯度的攻击远未达到最优。

EvA（Evolutionary Attack）直接求解原始离散优化问题，采用无梯度的遗传算法在离散空间中搜索扰动。其核心洞察在于：通过将搜索空间约束到攻击节点的感受野、以模型准确率作为适应度函数、引入自适应目标变异（ATM），遗传算法能够高效探索扰动空间，避免梯度信息带来的误导。

在CoraML、Pubmed等多数据集上，EvA相比此前最强的梯度攻击PRBCD平均额外降低约11%的分类准确率，并在对抗训练、图结构防御等鲁棒模型上展现出更强的攻击穿透力。消融实验表明，自适应目标变异和准确率适应度函数是性能提升的关键，分治策略与稀疏编码使方法能够扩展至Ogbn-Arxiv等大规模图。



### 图结构攻击的离散组合优化本质

图对抗攻击的核心是在给定扰动预算下，通过翻转（添加或删除）少量边来最大化被攻击节点的损失函数。其数学形式为：

$$P = \arg \max_P \mathcal{L}(f(\mathcal{G}(X, A \oplus P))_{\mathrm{att}}, y_{\mathrm{att}}) \quad s.t. \quad \mathbf{1}_N P \mathbf{1}_N^\top \leq \epsilon \cdot |\mathcal{E}[\mathcal{V}_{\mathrm{att}} : \mathcal{V}]|$$

其中 $P$ 是一个二值扰动矩阵，$\oplus$ 表示异或操作（边翻转），$\epsilon$ 控制扰动预算。这一问题的本质是**离散组合优化**：搜索空间由所有可能的边翻转组合构成，解空间巨大且不可微。

### 梯度攻击的根本缺陷

当前最强的图攻击方法（如 PRBCD、LRBCD）均采用基于梯度的优化范式。这类方法将离散的边翻转问题松弛为连续空间中的梯度下降，存在三个结构性缺陷：

**梯度是局部度量，无法反映离散翻转的真实影响。** 如 Figure 1 所示，损失景观高度非线性且非凸。在边 $(i,j)$ 和 $(u,v)$ 上分别计算梯度，可能指示两者都应翻转；但实际上，单独翻转任一条边会增加损失，而**同时翻转两条边反而可能降低损失**（Figure 1 [Middle]）。梯度无法捕捉这种边之间的相互作用，因为它只度量单一边在当前位置的瞬时变化率。附录 Figure 7 和 Figure 8 进一步验证了这一现象在 Tanh-Margin 损失和交叉熵损失下均普遍存在。

**代理损失与攻击目标不一致。** 梯度方法必须使用可微的代理损失（如交叉熵或 Tanh-Margin），但攻击的最终目标是降低模型准确率——这是一个不可微的离散指标。Figure 2 [Left] 的消融实验表明，直接使用准确率作为优化目标的效果显著优于代理损失，但梯度方法无法直接优化准确率。

**连续松弛引入偏差。** 将二值扰动矩阵松弛为连续值，再通过投影或采样恢复为离散解，这一过程不可避免地引入近似误差。当扰动预算较小（$\epsilon \leq 0.05$）时，这种误差尤为致命，因为每一步的微小偏差都可能导致最终扰动偏离最优解。

### 早期进化攻击的局限

Dai et al. (2018a) 曾尝试使用遗传算法进行图攻击，但效果远不及梯度方法。其失败原因在于搜索空间过于庞大：均匀随机变异在整个图中任意添加边，搜索空间大小为 $\binom{n}{2}^{\delta}$，导致遗传算法在有限计算预算下无法有效收敛。Table 4 显示，该基线在 CoraML 上的攻击效果（$\epsilon=0.15$ 时准确率仍高达 75.08%）远弱于 PRBCD（66.48%）。

### 本文动机

上述分析揭示了一个核心瓶颈：**梯度信息在图离散攻击中具有误导性，而现有无梯度搜索方法又因搜索空间过大而失效。** 这驱动了 EvA 的设计——通过约束搜索空间到攻击节点的感受野、使用准确率作为适应度函数、引入自适应目标变异，使得遗传算法能够在离散空间中高效搜索，从而绕过梯度方法的根本局限。Figure 1 [Right] 初步展示了这一思路的潜力：EvA 在损失优化上同时超越了 PRBCD 和基线遗传算法。



## 核心方法与创新机理

EvA 的核心创新在于**将图对抗攻击从基于梯度的连续松弛优化范式彻底转向无梯度的离散遗传算法搜索**，从而直接求解原始的组合优化问题。这一范式转换由四个关键的 changed slots 支撑，每个 slot 均针对现有梯度攻击的根本性缺陷。

### 1. 优化范式：从梯度松弛到无梯度离散搜索

基于梯度的 SOTA 攻击（如 PRBCD）必须将离散的边翻转问题松弛为连续空间中的优化问题，以便计算梯度。然而，这一松弛过程引入了根本性的误导：**梯度是局部度量，无法准确反映离散边翻转的真实损失变化**。具体而言，梯度刻画的是函数在无穷小变化下的行为，而实际攻击需要的是在 $\{0, 1\}$ 离散空间中翻转整条边的效果。更严重的是，梯度**忽略了边之间的相互作用**——存在这样的情况：单独翻转每条边会暗示损失向某一方向变化，但联合翻转两条边却会逆转这一方向（Figure 1 [Left] 和 [Middle]；§B 提供了详细分析）。这导致损失景观呈现出高度非线性和非凸性，梯度指引的搜索方向可能完全错误。

EvA 直接放弃了梯度信息，采用遗传算法在离散空间中搜索最优扰动矩阵 $P$，直接优化攻击目标：
$$P = \arg \max_P \mathcal{L}(f(\mathcal{G}(X, A \oplus P))_{\mathrm{att}}, y_{\mathrm{att}}) \quad s.t. \quad \mathbf{1}_N P \mathbf{1}_N^\top \leq \epsilon \cdot |\mathcal{E}[\mathcal{V}_{\mathrm{att}} : \mathcal{V}]|$$
这一范式转换使得 EvA 能够规避梯度带来的非线性、非凸和局部性误导，从而显著超越基于梯度的最强攻击。在 CoraML 等多个数据集上，EvA 使准确率额外下降约 11%（与 PRBCD 相比），这一决定性证据直接验证了无梯度搜索范式的优越性。

### 2. 搜索空间编码：从稠密邻接矩阵到稀疏边索引列表

梯度攻击（如 PRBCD）需要维护稠密的邻接矩阵梯度，空间复杂度为 $O(N^2)$，严重限制了可处理的图规模。EvA 采用**稀疏编码**，将每个候选解表示为长度为 $\delta$（扰动预算的边数）的索引向量：
$$\mathbf{s}_i \in \left[ \frac{n}{2}(n-1) \right]^{\delta}$$
每个索引对应无向图上三角矩阵中的一条边。这一编码将空间复杂度从 $O(N^2)$ 降至 $O(\epsilon \cdot E \cdot P)$，其中 $P$ 为种群大小（通常为常数），因此实际复杂度为 $O(\epsilon \cdot E)$。稀疏编码使 EvA 能够处理大规模图（如 Ogbn-Arxiv），而无需承受稠密矩阵的内存负担。

### 3. 适应度函数：从代理损失到直接优化准确率

梯度攻击受限于可微性要求，只能优化交叉熵或 Tanh-Margin 等代理损失。然而，攻击的最终目标是降低模型准确率——这是一个**不可微的目标**。EvA 利用遗传算法的无梯度特性，直接使用模型准确率作为适应度函数：
$$\mathrm{fit}(\mathbf{s}_i) = \mathcal{L}(\mathbf{X}, \mathbf{A} \oplus \mathbf{P}_i, \mathbf{y})$$
消融实验（Figure 2 [Left]）表明，准确率作为适应度函数优于交叉熵和 margin-based 损失，且对于较大的 $|\mathcal{V}_{\mathrm{att}}|$ 优势更为明显。这一设计使得攻击的优化目标与评估目标完全一致，避免了代理损失带来的优化偏差。

### 4. 变异策略：从均匀随机变异到自适应目标变异

基础的遗传算法在整个图中均匀随机地添加边，搜索空间高达 $\binom{n}{2}^{\delta}$，大量扰动位于攻击节点的感受野之外，几乎无效。EvA 引入**自适应目标变异（ATM）**，将变异操作限制在攻击节点的感受野内：新边至少有一个端点在 $\mathcal{V}_{\mathrm{att}}$ 中，将搜索空间缩减至：
$$\left( \frac{|\mathcal{V}_{\mathrm{att}}| (2n - |\mathcal{V}_{\mathrm{att}}| - 1)}{2} \right)^{\delta}$$
更进一步，ATM 在攻击成功改变某节点的标签后，**将该节点从受限端点中排除**，避免对已成功攻击的节点浪费扰动预算。消融实验（Figure 2 [Middle left] 和 Table 4）表明，ATM 和准确率适应度函数二者均能显著提升攻击效果，其中 ATM 的贡献更大，是 EvA 超越基础遗传算法基线的关键设计。

### 5. 大规模图扩展：分治策略

对于大规模图，搜索空间随节点数平方增长。EvA 引入**分治策略**：将攻击节点集 $\mathcal{V}_{\mathrm{att}}$ 划分为 $k$ 个不相交子集，对每个子集顺序运行攻击，预算按连接边比例分配。这一策略使 EvA 能够扩展到 Ogbn-Arxiv 等大图，并带来约 8% 的额外性能增益（Figure 2 [Middle right]；Table 5）。值得注意的是，分治策略同样适用于现有的梯度攻击，具有一定的通用性。

---

**总结**：EvA 的创新本质在于识别了梯度攻击的根本瓶颈——连续松弛导致的优化偏差——并通过无梯度的遗传算法搜索、稀疏编码、直接优化准确率和自适应目标变异四个 changed slots 系统性地解决了这一问题。实验证据强烈支持这些创新的有效性，使得 EvA 在多个数据集、多种防御模型和不同攻击设定下均显著超越 SOTA 梯度攻击。



EvA 将图对抗攻击形式化为一个离散组合优化问题，并采用遗传算法在二值扰动空间中直接搜索，完全规避了梯度方法所需的连续松弛。其整体 pipeline 由五个核心模块串联构成，输入为原始图（邻接矩阵 $\mathbf{A}$、节点特征 $\mathbf{X}$、标签 $\mathbf{y}$）、攻击节点集 $\mathcal{V}_{\mathrm{att}}$ 和扰动预算 $\epsilon$，输出为满足预算约束的扰动边集。

**种群初始化** 模块生成 $P$ 个候选解，每个候选解 $\mathbf{s}_i$ 是一个长度为 $\delta$（即允许翻转的边数）的索引向量，对应无向图上三角矩阵中的边位置。为压缩搜索空间，初始种群的每条边至少有一个端点落在 $\mathcal{V}_{\mathrm{att}}$ 中。这一稀疏编码使空间复杂度降至 $\mathcal{O}(\epsilon \cdot E \cdot P)$，避免了稠密邻接矩阵的 $\mathcal{O}(N^2)$ 存储开销。

**适应度评估** 模块将每个候选解 $\mathbf{s}_i$ 解码为二值扰动矩阵 $\mathbf{P}_i$，构造扰动图并计算模型损失 $\mathrm{fit}(\mathbf{s}_i) = \mathcal{L}(\mathbf{X}, \mathbf{A} \oplus \mathbf{P}_i, \mathbf{y})$。对于全局攻击，EvA 直接使用不可微的准确率作为适应度函数，而非梯度方法常用的交叉熵或 tanh-margin 代理损失——消融实验表明准确率适应度在较大 $\mathcal{V}_{\mathrm{att}}$ 下略优于交叉熵（Figure 2 left）。为提升评估效率，EvA 支持堆叠推理：将 $k$ 个候选解的扰动图拼接为一个大图，在单次前向传播中批量计算所有适应度值。

**锦标赛选择与交叉** 模块通过锦标赛选择（tournament size $n_{\text{tour}}=2$）从当前种群中选出父代，采用单点交叉算子拼接父代片段生成新候选解，维持种群多样性的同时保留优质基因。

**自适应目标变异（ATM）** 是 EvA 区别于基线遗传算法的关键设计。以概率 $p$ 替换候选解中的边索引时，新边至少有一个端点落在 $\mathcal{V}_{\mathrm{att}}$ 中（目标变异，TM），且已成功翻转标签的节点被排除在受限端点之外（自适应，ATM）。这一机制动态收缩搜索空间：当某攻击节点已被攻破，继续扰动其连接不再提升攻击效果，ATM 自动将搜索资源重新分配给尚未攻破的节点。消融实验（Table 4）表明 ATM 是 EvA 性能提升的最大贡献因素。

**局部投影** 模块为可选组件，用于满足每节点度约束的局部攻击场景。EvA 不使用梯度信息，而是基于边在种群中的出现频率分数 $s(e) = \sum_{s \in \mathcal{S}} \mathbb{I}[e \in s] / |\mathcal{S}| + u$（$u$ 为小随机数打破平局）进行贪心筛选，保证扰动满足局部度限制。实验表明 EvA 引入的度约束违反数量少于 PRBCD（Figure 2 right）。

**分治策略** 是面向大规模图的可选扩展。当图规模增大导致搜索空间二次膨胀时，将 $\mathcal{V}_{\mathrm{att}}$ 划分为 $k$ 个不相交子集，对每个子集顺序运行 EvA，扰动预算按子集间连接边比例分配。分治策略使 EvA 能够扩展到 Ogbn-Arxiv 等大图，并带来约 8% 的额外性能增益（Figure 2 middle right），同时该策略对 PRBCD 等梯度攻击同样有效。

整个 pipeline 的核心因果机制在于：通过将搜索空间约束在攻击节点的感受野内、使用准确率作为直接优化目标、引入自适应目标变异动态聚焦未攻破节点，遗传算法能够高效探索离散扰动空间，避免梯度信息因非线性和边间交互效应带来的误导（Figure 1）。



### 攻击优化目标

EvA 直接在离散空间中求解原始组合优化问题，避免了梯度方法所需的连续松弛。其全局攻击目标形式化为：

$$P = \arg \max_P \mathcal{L}(f(\mathcal{G}(X, A \oplus P))_{\mathrm{att}}, y_{\mathrm{att}}) \quad s.t. \quad \mathbf{1}_N P \mathbf{1}_N^\top \leq \epsilon \cdot |\mathcal{E}[\mathcal{V}_{\mathrm{att}} : \mathcal{V}]|$$

其中 $P$ 为二值扰动矩阵，$A \oplus P$ 表示对邻接矩阵的边翻转操作，$\mathcal{L}$ 为损失函数，$\mathcal{V}_{\mathrm{att}}$ 为攻击目标节点集，$\epsilon$ 为扰动预算。EvA 的关键创新在于直接以不可微的模型准确率作为 $\mathcal{L}$，而非依赖交叉熵或 Tanh-Margin 等代理损失。

### 稀疏编码与个体表示

为降低空间复杂度，EvA 采用稀疏编码，将每个候选解表示为一个长度为 $\delta$（扰动边数）的索引向量：

$$\mathbf{s}_i \in \left[ \frac{n}{2}(n-1) \right]^{\delta}$$

每个索引对应无向图上三角矩阵中的一条边，避免了稠密邻接矩阵 $\mathcal{O}(N^2)$ 的存储开销。整体记忆复杂度为 $\mathcal{O}(\epsilon \cdot E \cdot P)$，其中 $E$ 为边数，$P$ 为种群大小。由于种群大小通常为常数，实际复杂度简化为 $\mathcal{O}(\epsilon \cdot E)$。

### 适应度评估

个体 $\mathbf{s}_i$ 的适应度直接定义为扰动后图上的模型损失：

$$\mathrm{fit}(\mathbf{s}_i) = \mathcal{L}(\mathbf{X}, \mathbf{A} \oplus \mathbf{P}_i, \mathbf{y})$$

实验证据表明，以准确率（而非交叉熵或 Margin 损失）作为适应度函数能显著提升攻击效果（Figure 2 left）。为加速评估，EvA 支持堆叠推理：将 $k$ 个候选解组合成一个大图，在单次前向传播中批量评估所有个体。

### 自适应目标变异（ATM）

变异策略是 EvA 区别于基线遗传算法的核心。标准均匀变异在整个图中随机添加边，搜索空间为 $\binom{n}{2}^{\delta}$。EvA 引入目标变异（TM），限制新边至少有一个端点在 $\mathcal{V}_{\mathrm{att}}$ 中，将搜索空间压缩至：

$$\left( \frac{|\mathcal{V}_{\mathrm{att}}| (2n - |\mathcal{V}_{\mathrm{att}}| - 1)}{2} \right)^{\delta}$$

在此基础上，自适应目标变异（ATM）进一步排除已被成功攻击的节点：当攻击已改变某节点的预测标签后，继续扰动其连接不再提升攻击效果，因此将这些节点从受限端点中移除。消融实验表明，ATM 在所有种群规模下均能持续提升性能（Figure 3 Middle），且其贡献大于适应度函数选择（Table 4）。

### 局部投影的频率分数

在处理局部度约束攻击时，EvA 无法使用梯度信息进行投影。替代方案是基于种群边频率的贪心筛选，频率分数定义为：

$$s(e) = \sum_{s \in \mathcal{S}} \mathbb{I}[e \in s] / |\mathcal{S}| + u$$

其中 $\mathcal{S}$ 为当前种群，$u$ 为小的均匀随机数以打破平局。该分数反映边在当前种群中的共识程度，用于指导满足每节点度约束的贪心投影（§4 LOCAL AND TARGETED ATTACKS）。实验表明，EvA 引入的度约束违反数量少于 PRBCD（Figure 2 right）。

### 分治策略

针对大图场景，EvA 采用分治策略：将 $\mathcal{V}_{\mathrm{att}}$ 划分为 $k$ 个不相交子集，对每个子集顺序运行攻击，预算按连接边比例分配。该策略使 EvA 能够扩展到 Ogbn-Arxiv 等大图，并带来至少约 8% 的性能增益（Figure 2 right），同时也可应用于现有梯度攻击方法。



## 实验与关键发现

### 核心瓶颈：梯度为何在离散图攻击中失效

基于梯度的图攻击方法（如 PRBCD、LRBCD）将离散的边翻转问题松弛为连续优化，但这一松弛引入了根本性缺陷。**梯度是一个局部度量**，它量化的是函数在无穷小变化下的行为，而边翻转是 {0,1} 空间中的离散跳变，梯度无法准确反映这种离散变化对损失的真正影响。更关键的是，梯度完全忽略了边之间的交互效应：存在这样的情况——单独翻转每条边时梯度提示某个损失变化方向，但同时翻转两条边时损失变化方向完全相反（见 Figure 1 [Left] 和 [Middle]，以及 §B 中的详细分析）。这种非线性与非凸性使得梯度引导的搜索在离散组合空间中极易陷入误导。

![[assets/figures/papers/iclr26_0012_EzXzGRngYb_EvA_Evolutionary_Attacks_on_Graphs/figures/001_Figure_1.jpg]]
*Figure 1: We compute $\mathcal { L } _ { \mathrm { m a r g i n } }$ ( A + $\Delta$ A ) where $\Delta$ A = $e _ { i } e _ { i } ^ { \top } \Delta _ { i j } + e _ { u } e _ { v } ^ { \top } \Delta _ { u v }$ and $e _ { i }$ is the i-the cannonical vector. [Left] The loss landscape is non-linear, and the gradient does not always indicate the loss direction when we flip an edge (e.g. gradient suggests decrease, but loss increases). [Middle] Due to non-convexity, the effect of flipping each edge separately (e.g. loss decreases) can differ from flipping both edges simultaneously (e.g. loss increases). This happens for many edges (§ B). [Right] EvA does not suffer from this issue and outperforms both PRBCD and search...

EvA 直接求解原始离散组合优化问题，采用遗传算法在无梯度条件下搜索扰动空间。通过约束搜索空间到攻击节点的感受野、使用模型准确率作为适应度函数、引入自适应目标突变，EvA 避免了梯度信息带来的系统性偏差，从而显著超越当前最强的梯度攻击方法。

### 主实验结果

**Table 1** 展示了 CoraML 数据集上不同攻击方法在不同扰动预算下的分类准确率。EvA 在所有预算水平下均显著优于 SOTA 方法 PRBCD：在 ε=0.05 时，EvA 将准确率压至 52.95%，而 PRBCD 为 66.48%，额外下降约 13.5 个百分点；在 ε=0.10 时，EvA 达到 41.99%，PRBCD 为 53.42%。随着预算增大，EvA 的优势持续扩大，在 ε=0.15 时准确率降至 37.65%，几乎将 GCN 的性能压缩至随机猜测水平。其他梯度/启发式攻击（DICE、PGA、PGD、GRPCD）的性能下降幅度远小于 EvA。

![[assets/figures/papers/iclr26_0012_EzXzGRngYb_EvA_Evolutionary_Attacks_on_Graphs/figures/005_Table_1.jpg]]
*Table 1: Performance of different attack methods under varying budgets on CoraML dataset*

**Table 2** 展示了防御模型下的攻击效果。在 GCN-SVD 防御下，ε=0.10 时 EvA 将准确率从 PRBCD 的 0.70 压至 0.41，降幅达 29 个百分点，表明 EvA 能够有效击穿基于 SVD 预处理的防御。对于 GNNGuard、GNNJaccard、Robust-GCN 和 Soft-Median 等防御机制，EvA 同样持续优于 PRBCD。值得注意的是，在 Soft-Median-GDC 这一较强防御下，EvA 在 ε=0.10 时仍将准确率压至 0.55，而 PRBCD 为 0.68。

![[assets/figures/papers/iclr26_0012_EzXzGRngYb_EvA_Evolutionary_Attacks_on_Graphs/figures/006_Table_2.jpg]]
*Table 2: Performance of different defense models under various attack strengths on CoraML*

**Figure 5** 进一步展示了跨模型和跨数据集的性能对比。在 CoraML 的 vanilla GCN 上，EvA 在极小预算（ε≈0.01-0.02）下即开始显著拉开与 PRBCD 的差距；在经 PRBCD 对抗训练的 GCN 上，EvA 同样保持优势。在 Ogbn-Arxiv 大图上，结合分治策略的 EvA 在 ε=5% 时准确率为 53.92%，略优于 PRBCD 的 54.7%（见 Table 17 及 Figure 5 右）。

![[assets/figures/papers/iclr26_0012_EzXzGRngYb_EvA_Evolutionary_Attacks_on_Graphs/figures/007_Figure_5.jpg]]
*Figure 5: (Left to right) Performance on CoraML on Vanilla GCN, adversarially trained GCN using PRBCD, Soft-Median-GDC model. The right-most figure is GCN on Ogbn-Arxiv*

**Table 3** 展示了非引文网络数据集（Amazon-Photo、Amazon-Computers）上的结果。在 ε=0.05 的 Photo 数据集上，EvA 准确率为 72.73%，PRBCD 约为 75.40%，EvA 额外压低了约 2.67 个百分点，验证了方法的跨域泛化能力。

### 消融实验：关键设计组件的贡献

**自适应目标变异（ATM）与适应度函数。** Table 4 系统消融了 ATM 和适应度函数对 EvA 性能的影响。以 Dai et al. (2018a) 的基础 GA 为起点（CoraML ε=0.15 时准确率 75.08%），引入准确率适应度（Lacc）后降至 55.38%，进一步加入 ATM 后降至 37.65%。ATM 的贡献尤为显著：它将变异操作约束到攻击节点感受野内，并动态排除已被成功攻击的节点，有效缩小搜索空间并提升搜索效率。Figure 2（左和中左）进一步可视化显示，准确率作为适应度函数优于交叉熵和 margin-based 损失，而 ATM 在所有变异策略中表现最佳。

![[assets/figures/papers/iclr26_0012_EzXzGRngYb_EvA_Evolutionary_Attacks_on_Graphs/figures/002_Figure_2.jpg]]
*Figure 2: [Left] EvA’s performance with different objective functions and [Middle left] mutation strategies. [Middle right] Effect of D&C on the performance of EvA for different datasets. [Right] The number of violations from local constraints by EvA, and PRBCD ( $\epsilon _ { \mathrm { l o c } }$ = 0 . 5 )

![[assets/figures/papers/iclr26_0012_EzXzGRngYb_EvA_Evolutionary_Attacks_on_Graphs/figures/010_Table_4.jpg]]
*Table 4: The effect of our adaptive targeted mutation (ATM) and the fitness function on CoraML*

**稀疏编码与分治策略。** Table 5 展示了在大图 Ogbn-Arxiv 上的消融结果。基础 GA 因内存溢出无法直接运行；加入稀疏编码（SE）后 EvA 可运行但性能有限（ε=0.10 时准确率 63.51%）；进一步加入分治策略（D&C）后，准确率降至 47.56%。Figure 2（中右）显示，D&C 在大图和大预算下带来约 8% 的额外性能增益，而在小图上效果不明显——这与分治策略作为近似优化的本质一致。

**可扩展性分析。** Figure 3 对比了 PRBCD 和 EvA 在不同计算资源下的性能变化。增加种群大小和迭代次数能够稳定提升 EvA 的性能，而 PRBCD 在增加步数或块大小时提升有限。此外，ATM 在不同种群大小下均一致增强性能，表明该方法对资源配置具有鲁棒性。Figure 3 右还展示了前向传播次数与性能的关系，EvA 在给定查询预算下效率优于 PRBCD。

### 失败模式与局限性

尽管 EvA 在全局攻击场景下表现卓越，但在**单节点目标攻击**等信号极稀疏的场景中，准确率适应度函数失效，仍需退回到代理损失（如 tanh-margin），无法发挥无梯度直接优化的全部优势。

**计算开销**是 EvA 的主要代价：每代需评估整个种群的前向传播，查询成本高于部分梯度攻击。分治策略虽能缓解大图的内存压力，但作为一种近似优化，可能丢失跨子集的全局最优扰动组合。

**超参数敏感性**也不容忽视。种群多样性对搜索效率至关重要，种群大小、变异率、锦标赛规模等需要针对具体数据集调节。Figure 2（右）显示 EvA 在局部度约束下的违规数量少于 PRBCD，但并未完全消除违规，表明局部投影机制仍有改进空间。

### 新颖攻击目标

Figure 6 展示了 EvA 对非传统攻击目标的优化能力。由于无需梯度信息，EvA 可直接优化 conformal 预测的覆盖率和集合大小：在 vanilla 和对抗训练的 GCN 上，EvA 均能有效降低 conformal 覆盖率并增大预测集合。此外，EvA 还能攻击认证鲁棒性指标（certified ratio），在经 PRBCD 对抗训练的 GPRGNN 上同时扰动图结构 A 和节点特征 X，显著降低认证比率。这验证了 EvA 作为通用攻击框架的灵活性——只要目标函数对搜索空间中的小变化敏感，即可被直接优化。

### 公平性说明

所有实验均在相同的归纳学习设定下进行，使用五次不同数据划分取平均，并以相同的攻击预算和评估协议对比。与 PRBCD 比较时，严格控制了时间、内存与前向/反向传播次数等计算资源，确保对比的公平性。



## 定位与知识库关联

### 与基线方法的关系

EvA 的核心定位是对基于梯度的图对抗攻击范式的根本性替代。当前 SOTA 攻击 PRBCD 及其变体 LRBCD 将离散的边翻转问题松弛为连续优化，利用块坐标梯度下降搜索扰动。这一范式的根本瓶颈在于：**梯度是局部度量，无法准确反映离散边翻转的真实损失变化，且忽略边之间的相互作用**——单独翻转两条边可能暗示损失朝某一方向变化，但联合翻转时效果可能完全相反（Figure 1 [Left] 和 [Middle]，以及 §B 的详细分析）。EvA 通过直接求解原始离散组合优化问题，绕开了这一瓶颈。

在方法谱系上，EvA 并非首个将遗传算法引入图攻击的工作。Dai et al. (2018a) 曾提出基于 GA 的图攻击基线，但其采用均匀随机变异（在整个图中随机添加边）和交叉熵代理损失，搜索效率低下，攻击效果远逊于梯度方法。EvA 在此基础上进行了三项关键改造：

1. **搜索空间约束**：将变异操作限制在攻击节点感受野内（targeted mutation, TM），并进一步排除已成功攻击的节点（adaptive targeted mutation, ATM），将搜索空间从 $\binom{n}{2}^{\delta}$ 压缩至 $\left( \frac{|\mathcal{V}_{\mathrm{att}}| (2n - |\mathcal{V}_{\mathrm{att}}| - 1)}{2} \right)^{\delta}$。
2. **适应度函数替换**：用模型准确率直接作为适应度（$L_{acc}$），替代交叉熵或 tanh-margin 等代理损失，使优化目标与攻击目标完全对齐。
3. **稀疏编码**：用边索引列表（空间 $\mathcal{O}(\delta)$）替代稠密邻接矩阵梯度（空间 $\mathcal{O}(N^2)$），大幅降低内存需求。

消融实验（Table 4）表明，ATM 和 $L_{acc}$ 二者均能显著提升攻击效果，其中 ATM 的贡献更大。基础 GA 基线（Dai et al.）在 CoraML 上仅能将准确率从 80.71%（$\epsilon=0.01$）降至 75.08%（$\epsilon=0.15$），而 EvA（+ both）可降至 37.65%。

### 适用边界

**优势场景**：

- **全局扰动攻击**：EvA 在 CoraML、Pubmed、AMAZON-PHOTO 等多个数据集上一致超越 PRBCD，在 CoraML 上额外降低准确率约 11%（Table 1）。
- **防御突破**：EvA 能有效攻破 GCN-SVD、GNNGuard、Robust-GCN、Soft-Median-GDC 等多种防御机制，在 GCN-SVD 上准确率从 PRBCD 的 0.70 降至 0.41（$\epsilon=0.10$, Table 2）。
- **不可微目标攻击**：EvA 可优化认证比率（certified ratio）和 conformal 预测覆盖等梯度方法无法处理的目标（Figure 6）。
- **大图扩展**：结合分治策略（D&C）和稀疏编码（SE），EvA 可处理 Ogbn-Arxiv 规模的数据集，且 D&C 带来约 8% 的性能增益（Figure 2 [Middle right], Table 5）。

**受限场景**：

- **单节点目标攻击**：当攻击节点数极少时，准确率适应度信号过于稀疏，需退化为 tanh-margin 等代理损失（§4）。
- **计算预算敏感场景**：EvA 每代需评估整个种群，前向传播次数显著高于梯度攻击。PRBCD 在额外计算资源下提升有限，而 EvA 可通过增加种群大小和迭代次数持续提升性能（Figure 3），但这也意味着更高的查询成本。

### 局限与开放问题

**已知局限**：

1. **查询效率**：EvA 需要大量前向传播，计算开销高于部分梯度攻击，在查询预算严格受限的场景下可能不适用。
2. **分治近似的次优性**：D&C 策略将攻击节点子集划分并顺序攻击，是一种近似优化，可能丢失全局最优解，在小图上可能无效甚至有害。
3. **超参数敏感性**：攻击性能依赖种群多样性和超参数（种群大小、变异率等）的仔细调节，缺乏自适应的参数选择机制。
4. **目标攻击的适应度退化**：对于信号极稀疏的单节点目标攻击，准确率适应度失效，需依赖代理损失。

**开放问题**：

1. **专用搜索算法设计**：当前 EvA 直接使用通用遗传算法框架。能否设计专为图对抗攻击定制的搜索算法，利用图结构先验进一步压缩搜索空间或引导变异方向？
2. **梯度-进化混合策略**：梯度信息虽不完美，但在局部仍有一定指导意义。将梯度作为变异引导或种群初始化的一部分，是否能结合二者优势？
3. **查询高效变体**：如何通过代理模型、主动学习或贝叶斯优化等手段降低 EvA 的查询成本，使其适用于更严格的查询预算约束？
4. **理论收敛性**：EvA 在经验上表现优异，但其在离散组合空间中的收敛性质和近似比尚缺乏理论分析，这是理解其优势边界的关键。



## 原文 PDF

![[paperPDFs/ICLR_2026/EvA_Evolutionary_Attacks_on_Graphs.pdf]]
