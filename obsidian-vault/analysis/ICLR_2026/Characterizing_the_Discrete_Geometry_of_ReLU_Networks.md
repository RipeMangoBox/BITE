---
title: "Characterizing the Discrete Geometry of ReLU Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Characterizing_the_Discrete_Geometry_of_ReLU_Networks.pdf
project_link: null
code_link: https://github.com/bl-ake/ICLR-2026
openreview_forum_id: TgLW2DiRDG
aliases:
- A1CCGBL
- CDGRN
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "输入维度 d、网络深度 ℓ 和每层最大宽度 m 是决定连通图平均度数与直径的核心架构参数。"
primary_logic: "连通图的平均度严格上界为 2d，与网络宽度和深度无关，并随网络规模增大而单调趋近该上界；连通图的直径上界为 O(m^ℓ) 且与输入维度 d 无关，尽管区域数目随 d 指数增长。"
claims:
- "连通图平均度数上界为 2d，与网络架构无关。"
- "连通图直径上界为 O(m^ℓ) 且与输入维度无关。"
- "平均度数随神经元数量单调递增并趋近 2d。"
- "多面体区域的邻居数分布为单峰右偏，峰值略低于 2d。"
---

# Characterizing the Discrete Geometry of ReLU Networks

> [!tip] 核心洞察
> 连通图的平均度严格上界为 2d，与网络宽度和深度无关，并随网络规模增大而单调趋近该上界；连通图的直径上界为 O(m^ℓ) 且与输入维度 d 无关，尽管区域数目随 d 指数增长。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 刻画ReLU网络的离散几何结构 |
| 英文题名 | Characterizing the Discrete Geometry of ReLU Networks |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=TgLW2DiRDG) · [GitHub](https://github.com/bl-ake/ICLR-2026) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Algorithm 1: Construction of the Connectivity Graph (基于BFS与LP冗余检测的多面体连通图构建) |
| Dataset | Synthetic clustering data with varying d, depth, and width, Synthetic data (d=4,5), MNIST |

> [!tip] 效果简介
> - Synthetic clustering data with varying d, depth, and width 上，Average connectivity graph degree (Avg #Facets) 为 Observed values, e.g., 3.87 for d=2, width=16, depth=4; 7.85 for d=4, width=16, depth=4，对比 2d (theoretical upper bound)，变化 All observed averages ≤ 2d, approaching the bound as network size increases。
> - Synthetic data (d=4,5) 上，Connectivity graph diameter vs theoretical upper bound 为 Estimated actual diameters (midpoint of lower/upper bounds from Magnien et al. 2009)，对比 O(m^ℓ) upper bound，变化 Diameter grows logarithmically with theoretical bound; nearly identical across different input dimensions for fixed architecture。
> - MNIST 上，Classification test accuracy / AUC 为 0.90 / 0.99，对比 N/A (not compared to other methods)。

## 概要

### 问题背景

全连接ReLU网络将输入空间划分为由弯曲超平面（Bent Hyperplane, BH）界定的多面体区域，这些区域构成一个多面体复形（polyhedral complex），其连通图以区域为节点、以共享面为边。现有研究大多聚焦于区域总数的上界，而对区域之间的连接方式——即连通图的拓扑特性——缺乏深入理解。这一盲区限制了我们对ReLU网络几何结构如何影响表示学习、泛化与鲁棒性的认识。

### 核心瓶颈与因果调控变量

**瓶颈**：对全连接ReLU网络多面体复形的连通图拓扑（平均度数、直径）缺乏严格的理论刻画与实证验证。

**因果调控变量**：输入维度 $d$、网络深度 $\ell$ 和每层最大宽度 $m$ 是决定连通图平均度数与直径的核心架构参数。理论分析表明，平均度数仅受 $d$ 约束，与网络规模无关；直径则受 $m$ 和 $\ell$ 控制，与 $d$ 无关。

### 核心发现

1. **平均度数严格上界为 $2d$**（Theorem 3.4）：连通图的平均度数 $\frac{2 N_{d-1}(\mathcal{C})}{N_d(\mathcal{C})} \leq 2d$，与网络宽度和深度无关。
2. **平均度数随网络规模单调趋近 $2d$**（Theorem 3.6, 3.7）：当浅层网络神经元数趋于无穷时，平均面数收敛到 $2d$；实验表明，即使在小规模网络中，平均度数也快速逼近该上界。
3. **直径上界为 $O(m^\ell)$ 且与 $d$ 无关**（Theorem 3.8）：尽管区域数随 $d$ 指数增长，连通图的直径仅由宽度和深度决定，下界为 $\Omega(\ln(N_d(\mathcal{C}))/\ln(n))$。
4. **邻居数分布呈单峰右偏**：多面体区域的邻居数分布为单峰右偏，峰值略低于 $2d$；包含训练数据点的区域平均邻居数显著高于不含数据的区域，且邻居数越高的区域其无界比例越高。

### 方法定位

本文提出 **Algorithm 1**（基于BFS与LP冗余检测的多面体连通图构建方法），通过广度优先搜索遍历符号序列（sign sequence），并利用线性规划（SOLVELP）检测神经元半空间是否为当前多面体的真正面，从而逐步构建完整的连通图。该方法在理论分析上植根于多面体复形的组合拓扑，通过逐层移除神经元的递推关系（Lemma 3.3）建立计数框架，属于ReLU网络几何表征研究中的离散几何分析路线。

### 主要实验结果

- **合成数据**：在输入维度 $d=2$ 至 $5$、宽度 $m \leq 16$、深度 $\ell \leq 4$ 的网络上，所有观测平均度数均 $\leq 2d$，且随神经元数量增加而单调上升并趋近上界（Figure 4, Table 3）；连通图直径随理论上界呈对数增长，且在不同输入维度下几乎一致（Figure 5, Figure 11）。
- **真实数据**：在MNIST（$d=784$ 经PCA降至5维）上，含训练数据的多面体区域平均邻居数显著更高（Figure 6），且训练过程中数据点逐渐被具有更多邻居的区域包围（Figure 14）；邻居数与区域有界性之间存在任务依赖的关联（Figure 7）。

### 局限与开放问题

**主要局限**：连通图枚举算法（Algorithm 1）的计算成本随区域数指数增长，难以直接应用于大型或高维网络；理论结果依赖权重处于一般位置的非退化假设；分析仅覆盖全连接ReLU架构，未扩展到卷积、跳跃连接或其他激活函数。

**开放问题**：训练为何倾向于将数据点置入高邻居数区域？连通图直径等拓扑特性是否与泛化性能、鲁棒性或不确定性量化存在定量关联？能否利用这些几何性质指导架构搜索或数据增强？对于大规模网络，是否存在高效的近似估计算法？

深度神经网络的表达能力与其在输入空间上诱导的几何分割密切相关。对于以ReLU为激活函数的全连接网络，每个神经元对应一个超平面（更准确地说，是弯曲超平面），这些超平面将输入空间 $\mathbb{R}^d$ 划分成若干个凸多面体区域，整体构成一个**多面体复形**（polyhedral complex）。每个区域内的所有点共享相同的激活模式（sign sequence），因此对应一个线性函数。理解这些区域的数目、形状和拓扑连接方式，对于揭示网络的表示能力、优化景观和泛化行为具有根本意义。

### 现有研究的局限

围绕ReLU网络多面体划分的研究已积累了大量成果，但关注点高度集中于一个指标：**区域总数的上下界**。经典结论给出了区域数随深度和宽度增长的最大速率，然而对于区域之间的**连接关系**——即连通图的拓扑特性——理解几乎空白。具体而言，以下问题尚未得到系统回答：

- 一个多面体区域平均有多少个相邻区域（即面数/连通图度数）？
- 连通图的直径（任意两个区域之间所需跨越的最少面数）有多大？
- 这些拓扑量如何受网络架构参数（输入维度 $d$、深度 $\ell$、宽度 $m$）的调控？
- 训练数据在连通图中的位置是否具有特殊的几何特征？

缺乏对这些问题的理解，意味着我们只能描述网络分割的“规模”，却无法刻画其“形状”。

### 核心动机

本文旨在填补上述空白，从拓扑视角系统刻画全连接ReLU网络的离散几何结构。核心动机可归纳为三个层次：

1. **理论层面**：建立连通图平均度数和直径的严格上下界，揭示它们与架构参数 $d$、$m$、$\ell$ 之间的定量依赖关系。
2. **算法层面**：提出一种基于广度优先搜索（BFS）和线性规划（LP）冗余检测的多面体枚举算法，使得对中小规模网络的连通图进行完整构建和统计成为可能。
3. **实证层面**：通过合成数据和真实数据（MNIST、CIFAR10、California Housing）上的实验，验证理论预测并发现训练数据在连通图中的分布规律——例如，包含训练数据的区域平均邻居数显著更高，且训练过程倾向于将数据点推向连通性更强的区域。

### 关键发现预览

本文的理论与实验共同揭示了几个简洁而深刻的规律：

- 连通图的**平均度数严格上界为 $2d$**，与网络的宽度和深度无关；且随着网络规模增大，平均度数单调趋近该上界（Theorem 3.4, 3.6, 3.7）。
- 连通图的**直径上界为 $O(m^\ell)$**，与输入维度 $d$ 无关——尽管区域总数随 $d$ 指数增长，但连通图的“跨度”仅由宽度和深度决定（Theorem 3.8）。
- 区域邻居数的分布呈**单峰右偏**形态，峰值略低于 $2d$；包含训练数据的区域系统性地拥有更多邻居，且更倾向于无界区域（尤其在分类任务中）。

这些发现为理解ReLU网络的几何正则性提供了新的视角，也为后续研究几何特性与泛化性能之间的定量关联奠定了基础。

## 核心方法与创新机理

本工作对全连接ReLU网络所诱导的输入空间多面体剖分进行了拓扑视角下的系统刻画，其核心创新在于将研究焦点从传统的“区域总数上界”转移到**区域之间的连接关系**——即连通图的拓扑特性。这一视角转换揭示了三个此前未被充分理解的几何规律。

### 创新一：连通图平均度数的维度紧确上界

该工作首次给出并证明了连通图平均度数的严格上界为 $2d$（$d$ 为输入维度），且该上界与网络宽度 $m$ 和深度 $\ell$ 无关（**Theorem 3.4**）。这一结果本质上是一个结构性的几何约束：无论网络规模如何膨胀，每个多面体区域平均最多只有 $2d$ 个邻居。更关键的是，该上界是紧的——随着网络神经元数量增加，平均度数单调递增并收敛到 $2d$（**Theorem 3.6, 3.7**），实验观测值也确实验证了这一收敛趋势（Figure 4，右侧面板）。这意味着 $2d$ 不仅是理论上界，更是大规模网络在实际中逼近的渐近极限。

### 创新二：连通图直径与输入维度的解耦

本工作证明了连通图直径的上界为 $O(m^\ell)$，且**与输入维度 $d$ 无关**（**Theorem 3.8**）。这与直觉形成鲜明对比：虽然多面体区域的总数随 $d$ 指数增长，但区域之间的“最远距离”仅由网络架构（宽度和深度）决定。实验进一步表明，在固定宽度和深度的情况下，不同输入维度下的直径增长几乎完全一致（Figure 5），且直径相对于理论上界呈对数增长趋势。这一发现将网络架构参数确立为控制连通图全局拓扑结构的核心因果旋钮。

### 创新三：基于BFS与LP冗余检测的连通图构建算法

为实现上述理论分析的实验验证，该工作提出了**Algorithm 1**——一种基于广度优先搜索（BFS）与线性规划（LP）冗余检测的连通图枚举算法。其核心机制是：通过松弛多面体定义中的单个不等式并求解线性规划（`SOLVELP`），判断该不等式对应的弯曲超平面是否为当前多面体的真正面，从而确定邻居关系。该方法直接操作于符号序列空间，将多面体剖分的组合枚举问题转化为可计算的形式，为后续的几何特性统计分析提供了工具基础。

### 创新四：数据点分布与几何特性的关联发现

在理论结果之外，该工作还揭示了一个具有启发性的经验规律：**包含训练数据点的多面体区域，其平均邻居数显著高于不含数据的区域**（Figure 6，MNIST/CIFAR10/CA Housing）。进一步分析显示，邻居数越高的多面体，其无界比例也越高；且在分类任务中，含数据区域的无界比例更高，而回归任务中则相反（Figure 7）。训练过程中，数据点逐渐被具有更多邻居的多面体所包围（Figure 14）。这些观察将网络的离散几何结构与其学习行为之间建立了初步的关联，为理解ReLU网络的表示偏好提供了新的几何视角。

### 与现有工作的本质差异

现有关于ReLU网络多面体剖分的研究（如区域计数上界的推导）大多停留在“有多少区域”这一静态问题上。本工作的本质突破在于追问“区域之间如何连接”，并将答案提炼为与架构参数直接关联的紧致理论界。这一转变使得连通图的平均度数和直径成为可预测、可验证的几何量，而非仅仅是组合爆炸的副产品。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_TgLW2DiRDG/figures/004_Figure_1.jpg]]
*Figure 1: (a) An example ReLU network with a 2-dimensional input. (b) The corresponding polyhedral complex where region A has neighbors B, C, D, and E. (c) The connectivity graph where nodes represent regions and edges link neighboring regions (so region A has degree 4). (d) A histogram of the number of neighbors for each region, or equivalently the degrees of the connectivity graph*

本工作构建了一套从**全连接ReLU网络权重**到**输入空间多面体复形连通图**的完整分析管线，包含三个核心模块：多面体枚举与连通图构建（Algorithm 1）、理论性质推导（第3节）、以及实验验证（第5节）。

### 输入输出流

**输入**：一个已训练的 ℓ 层全连接ReLU网络 f，其权重矩阵 W^(j) 与偏置 b^(j) 已知，输入维度为 d，每层最大宽度为 m。

**处理流程**：
1. **符号序列定义**：对任意输入点 x，定义其符号序列 **S**(x) ∈ {−1, 0, 1}^n，每位对应一个神经元在激活函数前的符号。所有弯曲超平面（Bent Hyperplanes, BHs）将输入空间 ℝ^d 划分为互不相交的多面体区域，每个区域对应一个唯一的符号序列。
2. **多面体枚举**（Algorithm 1）：从初始符号序列出发，通过 BFS 遍历所有可能的多面体区域。对每个区域的每个神经元，利用线性规划（SOLVELP 子程序）检测对应不等式是否为当前多面体的真正面——即松弛该不等式后，在法方向最大化目标函数，判断半空间是否冗余。若检测到面，则在连通图中添加边，并将新多面体的符号序列加入队列。
3. **连通图构建**：图的节点为多面体区域（d-细胞），边连接共享一个 (d−1) 维面的相邻区域。连通图的度数即多面体的面数。
4. **理论分析**：基于细胞分类引理（Lemma 3.2）与计数递推（Lemma 3.3），推导连通图平均度数的严格上界 2d（Theorem 3.4）、单调性（Theorem 3.6）、渐近收敛性（Theorem 3.7），以及直径的上下界（Theorem 3.8）。

**输出**：多面体复形的连通图，包含节点数（区域总数）、各节点度数（面数）分布、图直径，以及各多面体的有界性、体积等几何属性。

### 模块间关系

三个模块形成递进依赖：Algorithm 1 为实验提供可计算的连通图实例；理论结果（第3节）为实验观测提供上界与渐近行为预测；实验（第5节）在合成数据与真实数据上验证理论边界，并揭示训练数据分布与几何特性之间的关联（如含数据的区域平均邻居数更高）。管线中的关键计算瓶颈在于 SOLVELP 子程序——每个候选邻居都需求解一次线性规划，且总多面体数随网络规模指数增长，这直接限制了可处理网络的宽度与深度（实验中宽度 ≤ 16，深度 ≤ 4，输入维度 ≤ 5）。

### 多面体连通图的构建算法

本文的核心计算工具是 **Algorithm 1**（连通图构建），其目标是从一个已训练的ReLU网络出发，枚举输入空间被弯曲超平面（Bent Hyperplane, BH）划分出的所有多面体区域，并构建区域之间的邻接关系图。算法由四个关键模块组成：

**1. 初始化模块**
输入训练好的网络 $f$ 和一个初始符号序列 $s$（对应某个输入点的神经元激活符号），初始化队列 $Q$ 和空图 $G$。符号序列 $\pmb{S}(x) \in \{-1,0,1\}^n$ 是长度为 $n$（总神经元数）的向量，每位记录对应神经元在激活函数前的符号——这是贯穿全文的核心表示。

**2. BFS队列处理模块**
算法以广度优先方式遍历队列中的符号序列。对每个出队序列 $s$，逐一检查所有 $n$ 个神经元。核心思想是：邻居多面体可通过“跨越单个BH”到达，即其符号序列仅在位置 $i$ 处与原序列相反，记为 $s_{-i}$。

**3. SOLVELP线性规划检测模块**
这是算法的计算瓶颈。对候选邻居序列 $s_{-i}$，需判断第 $i$ 个神经元的半空间约束是否为当前多面体的**真正面**（即该不等式是否冗余）。判断方法为求解以下线性规划：

$$
\begin{array}{ll}
\text{maximize} & -\Phi_{s_i}^T x \\
\text{subject to} & \Phi_{s} x \leq -\beta_{s} + e_i
\end{array}
$$

其中 $\Phi_s$ 和 $\beta_s$ 是定义当前多面体的线性不等式系数矩阵和偏置向量（见下文公式推导），$e_i$ 是第 $i$ 位为1的单位向量。该LP松弛了第 $i$ 个不等式，并在其法方向 $-\Phi_{s_i}^T$ 上最大化目标函数。若最优值大于 $-(\beta_s)_i$，则该不等式非冗余，即第 $i$ 个神经元的BH确实构成当前多面体的一个面，$s_{-i}$ 是有效邻居。

**4. 图更新模块**
若SOLVELP确认面存在，则在连通图中添加边 $(s, s_{-i})$，并将新符号序列 $s_{-i}$ 加入队列和顶点集。

### 多面体线性不等式系统的逐层构造

给定一个符号序列 $s$，对应多面体区域的线性不等式系统 $\Phi x \leq -\beta$ 可通过逐层递推构造。设网络有 $\ell$ 层，第 $j$ 层的权重矩阵为 $W^{(j)}$，偏置为 $b^{(j)}$，符号向量为 $s^{(j)}$。则：

**系数矩阵递推**（Equation (2)）：
$$
\Phi^{(j)} = \mathrm{diag}(s^{(j)}) W^{(j)} \mathrm{diag}(\mathrm{ReLU}(s^{(j-1)})) \Phi^{(j-1)}
$$

**偏置向量递推**（Equation (3)）：
$$
\beta^{(j)} = \mathrm{diag}(s^{(j)}) \left( W^{(j)} \mathrm{diag}(\mathrm{ReLU}(s^{(j-1)})) \beta^{(j-1)} + b^{(j)} \right)
$$

**变量含义**：
- $\Phi^{(j)}$：第 $j$ 层输出的线性不等式系数矩阵，最终 $\Phi = \Phi^{(\ell)}$ 定义了多面体
- $\beta^{(j)}$：第 $j$ 层输出的偏置向量，最终 $\beta = \beta^{(\ell)}$
- $\mathrm{diag}(s^{(j)})$：以第 $j$ 层符号为对角元素的对角矩阵，将神经元激活状态编码为符号翻转
- $\mathrm{diag}(\mathrm{ReLU}(s^{(j-1)}))$：前一层符号的ReLU对角矩阵，仅保留正激活神经元的贡献

这两个递推公式将网络的前向传播转化为线性约束的累积，是多面体枚举和SOLVELP求解的基础。

### 细胞计数的递推关系

理论分析的核心工具是 **Lemma 3.3** 给出的细胞计数递推公式。设 $\mathcal{C}$ 为ReLU复形，$h_i$ 为移除神经元 $i$ 的弯曲超平面后的子复形，则 $k$-细胞的数量满足：

$$
N_k(\mathcal{C}) = N_k(h_i) + N_k(\mathcal{C} - h_i) + N_{k-1}(h_i)
$$

**含义**：总 $k$-细胞数 = 位于 $h_i$ 上的 $k$-细胞数 + 不在 $h_i$ 上的 $k$-细胞数 + 被 $h_i$ 分割产生的 $k$-细胞数（每个被分割的 $(k-1)$-细胞产生一个新的 $k$-细胞）。

该递推关系是证明平均度数上界（Theorem 3.4）和单调收敛性（Theorem 3.6, 3.7）的基石。通过逐层移除神经元并追踪各类细胞的消长，可以导出连通图平均度数的严格上界 $2d$，并证明随着神经元数量增加，平均度数单调趋近该上界。

## 实验与关键发现

### 5.1 理论边界的实证验证

本节通过合成数据实验，系统验证了第3节提出的连通图平均度数与直径的理论边界，并揭示了这些几何量随网络架构参数（输入维度 $d$、深度 $\ell$、宽度 $m$）的变化规律。

**实验设置**：在合成聚类数据上训练不同架构的全连接ReLU网络（$d \in \{2,3,4,5\}$，$\ell \in \{1,2,3,4\}$，$m \in \{4,8,16\}$），每组配置使用5种不同权重初始化，每种初始化对应5个不同的训练数据集。使用Algorithm 1枚举多面体区域并构建连通图。对于直径估计，由于精确计算在大图上不可行，采用Magnien et al. (2009)的上下界算法，取中点作为实际直径的估计值。

#### 5.1.1 平均度数的上界验证与收敛行为

**核心发现**：所有实验观测到的平均度数均严格小于理论上界 $2d$，且随网络规模增大单调趋近该上界。

Figure 4（左）展示了不同架构下多面体面数（即连通图度数）的分布直方图。以 $d=2$、宽度16、深度4的网络为例，其平均度数为3.87，而理论上界为4。当 $d=4$、宽度16、深度4时，平均度数上升至7.85，理论上界为8。所有分布均呈现**单峰右偏**形态，峰值略低于 $2d$，与引言中的经验观察一致。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_TgLW2DiRDG/figures/010_Figure_4.jpg]]
*Figure 4: (Left) Distributions for the number of faces of polyhedra in ReLU networks trained on synthetic data. Each colored bar shows the number of polyhedra with a given number of faces in complexes of networks with a specifc width, depth, and input dimension, averaged across 5 initializations of network weights for 5 different training datasets with standard deviation shown by the black bars. (Right) The mean of each distribution versus the number of neurons in the network, colored by dimension. Dotted lines represent upper bounds for the networks with different d*

Figure 4（右）和Table 1、Table 3进一步量化了这一趋势。平均度数随神经元总数单调递增，且增长曲线在不同输入维度下呈现清晰的分离——维度越高，收敛目标值 $2d$ 越大。这一现象由Theorem 3.6和Theorem 3.7严格保证：平均面数关于神经元数量单调递增，且当浅层网络神经元数趋于无穷时收敛到 $2d$。实验表明，即使在有限宽度的深层网络中，这一收敛趋势依然成立。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_TgLW2DiRDG/figures/030_Table_3.jpg]]
*Table 3: Summary statistics for the distributions in Fig. 12. Diameter for each complex is estimated as described in Section 5.1*

**Table 1 关键数据**（$d=4$，深度4，宽度16）：平均度数为7.85 ± 0.15，而理论上界为8；多面体总数约 $2.7 \times 10^6$。$d=5$ 时对应平均度数为9.82，理论上界为10。这些结果确证了Theorem 3.4的紧致性：$2d$ 不仅是上界，更是网络容量增大时的渐近极限。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_TgLW2DiRDG/figures/014_Table_1.jpg]]
*Table 1: Summary statistics for the distributions in Fig. 4 with four dimensions (left) and fve dimensions (right). Diameter for each complex is estimated as described in Section 5.1. Non-degenerate depth-1 networks always have the same number of polyhedra because their BHs are all just hyperplanes (Buck, 1943)*

#### 5.1.2 连通图直径的维度无关性

**核心发现**：连通图直径的上界为 $O(m^\ell)$ 且与输入维度 $d$ 无关；实验证实，固定架构下不同 $d$ 的直径增长几乎一致。

Figure 5以对数尺度展示了直径估计值随理论上界 $O(m^\ell)$ 的变化关系。三个子图分别对应宽度 $m=4,8,16$，每个子图包含深度 $\ell=1$ 至 $4$ 的曲线。关键观察：


1. **固定宽度下直径呈对数增长**：当 $m$ 固定时，实际直径随深度增加而增长，但增速远低于理论上界的指数增长，在对数尺度上近似线性。
2. **维度无关性验证**：Figure 11将横轴替换为Theorem 3.8的下界 $\Omega(\ln(N_d)/\ln(n))$ 后，不同输入维度的数据点几乎完全重叠。这直观地证明了直径由网络架构（宽度和深度）主导，而非输入维度——尽管区域总数 $N_d$ 随 $d$ 指数增长。

**Table 1 直径数据**（$d=4$，深度4，宽度8）：估计直径约120；而 $d=5$ 相同架构下直径约118，差异在估计误差范围内。Table 3中 $d=2$ 至 $d=5$ 的对应行进一步证实了这一模式。

Theorem 3.8提供了理论解释：直径上界 $O(m^\ell)$ 仅依赖最大宽度和深度，下界 $\Omega(\ln(N_d)/\ln(n))$ 虽涉及区域总数，但实验表明实际直径更贴近上界的增长模式。这意味着**网络的拓扑连通性主要由架构决定，而非输入空间的分片复杂度**。

### 5.2 真实数据上的几何特性

本节在MNIST、CIFAR10和California Housing三个真实数据集上训练网络（架构与性能见Table 2），分析多面体区域的连通性、有界性及其与训练数据的关系。Table 2显示，MNIST网络测试准确率为0.90，AUC为0.99；CIFAR10准确率为0.52，AUC为0.91；CA Housing的 $R^2$ 为0.65，MSE为0.34。

#### 5.2.1 数据点倾向于高连通区域

**核心发现**：包含训练数据点的多面体区域，其平均邻居数显著高于不含数据的区域。

Figure 6展示了三个数据集的邻居数分布直方图。灰色柱表示不含训练数据的多面体，彩色柱表示含数据的多面体（颜色深浅表示所含数据点数量）。在所有数据集中，含数据区域的分布明显右移——其邻居数普遍高于整体平均。以MNIST为例，含数据区域的平均邻居数约为6-8，而不含数据区域集中在3-5。CIFAR10和CA Housing呈现相同的定性模式。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_TgLW2DiRDG/figures/018_Figure_6.jpg]]
*Figure 6: Histograms of polyhedron neighbor counts (i.e., the number of polyhedra that have a specifc number of neighbors) for polyhedra that do not contain training data (gray) and ones that do (colored by total number of data points contained in those polyhedra)*

这一现象在训练动态中进一步得到证实。Figure 14展示了MNIST网络在不同训练epoch下的面计数分布：随着训练进行，数据点逐渐从低连通区域迁移到高连通区域。这暗示**SGD优化过程可能内生地偏好将决策边界塑造成使数据点位于拓扑上更“中心”的区域**，其优化机理或表示学习层面的原因尚待阐明。

#### 5.2.2 连通性与有界性的关联

**核心发现**：邻居数越高的多面体，其无界比例越高；分类与回归任务在有界性模式上呈现相反趋势。

Figure 7将多面体按是否包含数据点分为上下两行，每行柱状图按邻居数排列，颜色表示该邻居数下**有界多面体的比例**（越深表示有界比例越低，即无界比例越高）。关键观察：

1. **高连通区域更可能是无界的**：在所有子图中，右侧（高邻居数）的柱颜色更深，表明随着邻居数增加，多面体为无界的概率单调上升。这符合直觉：位于复形边缘的区域通常邻居较少，而内部区域（可能延伸至无穷）有更多相邻区域。
2. **分类与回归的差异**：在分类任务（MNIST、CIFAR10）中，含数据区域的无界比例**高于**不含数据区域；而在回归任务（CA Housing）中，含数据区域的无界比例**低于**不含数据区域。这一反转可能源于两类任务的目标函数形态差异——分类的决策边界倾向于在类别间形成延伸至无穷的分割面，而回归的连续输出曲面可能在数据区域周围形成更多有界“盆地”。这一假说需要进一步验证。

#### 5.2.3 枚举的扩展性限制

对于CIFAR10和California Housing，完全枚举多面体复形在计算上不可行。Algorithm 1的BFS搜索在遍历800万区域后被终止，随后通过随机采样10,000个训练点来发现额外的多面体并补全连通图。这意味着**报告的高连通区域统计数据可能存在采样偏差**——采样策略更可能遗漏低连通或无界的孤立区域，从而导致平均度数的估计偏高。对于MNIST，由于输入维度较低（$d=784$ 经预处理）且网络较小，成功完成了完全枚举。

### 5.3 几何特性的架构依赖性

Figure 12和Table 3提供了更全面的架构扫描结果（$d \in \{2,3,4,5\}$，$\ell \in \{1,2,3,4\}$，$m \in \{4,8,16\}$ 的全组合）。

**平均度数**：在所有配置中，平均度数严格小于 $2d$，且随宽度和深度增加而单调上升。例如，$d=3$ 时，宽度4深度1的平均度数为4.12，宽度16深度4升至5.89（理论上界为6）。Table 3显示，深度从1增至4时，平均度数的增幅在0.5-1.5之间，宽度加倍带来的增幅约为0.3-0.8。

**区域数量**：深度1的非退化网络具有固定的区域数（Buck, 1943），而深层网络的区域数随深度指数增长。Table 3中，$d=4$、宽度16的网络从深度1的约 $1.1 \times 10^4$ 区域增至深度4的约 $2.7 \times 10^6$ 区域。

**有界区域比例**：Table 3的“% Finite”列显示，有界区域的比例通常随深度增加而下降。$d=2$ 时，深度1的有界比例接近100%，深度4降至约40-60%。高维输入下这一比例更低，$d=5$ 深度4时仅约10-20%的区域是有界的。

**体积分布**：Figure 13展示了MNIST网络中有界d-cell的体积和内径分布。高连通区域倾向于具有更大的体积和内径，这与Figure 7的有界性模式形成互补——无界区域（体积无穷大）在邻居数分布中占据高连通端，而有界区域中体积较大者也倾向于有更多邻居。

### 5.4 失败模式与局限

1. **枚举的可扩展性瓶颈**：Algorithm 1的BFS-LP组合策略的计算代价随区域数指数增长。对于CIFAR10（$d=3072$）和CA Housing（$d=8$，但网络较宽），搜索被迫在800万区域后终止。这使得大规模网络的完全几何表征在当前方法下不可行，限制了结论向实际规模网络的推广。

2. **一般位置假设的未验证性**：所有理论结果均假设网络权重处于一般位置（非退化），即弯曲超平面的交集不会出现退化情况。实际训练权重的退化程度未被系统评估，这可能导致理论边界在某些情况下不严格成立。

3. **架构覆盖的局限性**：分析仅针对全连接ReLU网络，未涉及卷积层、跳跃连接、批归一化或Dropout等实际广泛使用的组件。这些结构对多面体复形拓扑的影响是开放问题。

4. **网络规模的实验限制**：合成实验的最大宽度为16、最大深度为4、最大输入维度为5。对于更大规模的网络（如宽度数百、深度数十的现代架构），几何特性的外推行为尚待验证。特别是，直径 $O(m^\ell)$ 的上界在 $m=100$、$\ell=10$ 时已极其宽松，实际直径的增长率可能远低于此。

5. **几何特性与泛化的关联缺失**：尽管揭示了数据点倾向于高连通区域等有趣现象，但未建立平均度数、直径等几何指标与测试泛化性能之间的定量关系。Table 2中的性能数据仅用于说明网络训练质量，未与几何特性做相关性分析。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_TgLW2DiRDG/figures/027_Table_2.jpg]]
*Table 2: Architecture, training hyperparameters, and performance of networks trained on real-world data. For the regression task, we report coeffcient of determination R ^ { 2 } and Mean Squared Error (MSE), while for the classifcation tasks, we report accuracy and Receiver Operating Characteristic Area Under the Curve (AUC) on the test set*

## 定位与知识库关联

### 问题背景与核心瓶颈

对于全连接ReLU网络，输入空间被神经元的**弯曲超平面（Bent Hyperplane, BH）**剖分为多面体区域构成的复形。现有研究大多聚焦于区域总数的上界（如Montúfar et al., 2014; Serra et al., 2018），而对区域之间的**连接方式**——即连通图的拓扑特性——缺乏深入理解。本工作的核心瓶颈在于：区域数量随输入维度指数增长，但区域间的邻接关系（面数、连通图直径）是否也遵循类似的指数增长规律，此前并无严格刻画。

### 方法定位与理论谱系

本工作沿袭Masden (2025)的拓扑视角，将ReLU网络的输入空间剖分视为一个**多面体复形（polyhedral complex）**，并以**符号序列（sign sequence）**作为区域和细胞（cell）的唯一标识。在此基础上，作者构建了连通图（connectivity graph），其中节点为d-维多面体区域，边表示两区域共享一个(d-1)-维面。

与现有工作的关键区别在于：
- **从计数到连接**：前人工作（如Hanin & Rolnick, 2019a; Masden, 2025）主要关注区域数量的上界或精确计数，本工作首次系统分析了区域间的邻接拓扑。
- **维度无关的直径上界**：定理3.8给出了连通图直径的上界$O(m^\ell)$（$m$为最大层宽，$\ell$为深度），该上界**与输入维度$d$无关**——尽管区域总数随$d$指数增长，直径却不受此影响。
- **平均度数的普适上界**：定理3.4证明连通图平均度数严格上界为$2d$，与网络宽度和深度无关；定理3.6和3.7进一步证明该平均度数随神经元数量单调递增并趋近$2d$。

该方法可定位于**神经网络几何理论**与**计算拓扑**的交叉地带，属于理论分析型工作，不提出新的训练或推理算法。

### 算法工具：基于BFS与LP冗余检测的连通图构建

为实证验证理论结论，作者提出了Algorithm 1（连通图构建算法），其核心流程为：
1. **初始化**：输入训练好的网络$f$及一个初始符号序列$s$，初始化BFS队列和图结构。
2. **BFS遍历**：对队列中每个符号序列，逐一检查所有神经元。
3. **SOLVELP子程序**：对第$i$个神经元，松弛其对应的不等式约束，求解线性规划以判断该半空间是否为当前多面体的**真正面**（即不等式是否冗余）。LP形式为：
   $$\begin{array}{ll} \text{maximize} & -\Phi_{s_i}^T x \\ \text{subject to} & \Phi_{s} x \leq -\beta_{s} + e_i \end{array}$$
4. **图更新**：若检测到面，则在连通图中添加边，并将新多面体的符号序列加入队列。

该算法本质上是一种**基于约束冗余检测的BFS枚举**，其正确性依赖于符号序列到多面体的单射性和SOLVELP对冗余不等式的精确判定。

### 适用边界与局限

本工作的理论结果和实验结论受以下边界条件约束：

1. **架构假设**：分析仅针对**全连接ReLU网络**，未扩展到卷积层、跳跃连接、归一化层或其他激活函数（如Leaky ReLU、GELU）。作者明确指出这是后续工作的开放方向。

2. **一般位置假设**：理论结果假定网络权重处于**一般位置（非退化）**，即不存在恰好使多个弯曲超平面在非平凡交集上重合的退化配置。实际训练得到的权重在多大程度上满足此假设，本文未做定量评估。

3. **计算可扩展性**：Algorithm 1的计算成本随区域数指数增长。对于CIFAR10和California Housing数据集，搜索被迫在遍历800万区域后终止，仅通过对10000个训练点采样来补全部分区域。这限制了该方法在大型网络或高维输入上的直接应用。

4. **网络规模有限**：实验所用的网络规模较小（宽度$\leq 16$，深度$\leq 4$，输入维度$\leq 5$），更大网络中的几何行为尚待验证。定理3.7的渐近收敛结论在这些有限规模实验中仅观察到趋势，远未达到收敛。

5. **与实际性能的关联缺失**：本文未建立所计算的几何特性（平均度数、直径、有界性比例）与网络泛化性能、鲁棒性或不确定性量化之间的**定量关系**。这是连接理论与应用的关键缺口。

### 开放问题

基于本工作的发现与局限，作者及分析中识别出以下待解决问题：

1. **训练动力学机理**：实验观察到训练倾向于将数据点置入拥有更多邻居的多面体区域（Figure 6, Figure 14），且训练过程中数据点逐渐被高连通性区域包围。这一现象背后的优化或表示学习机理尚不清楚。

2. **架构推广**：如何将多面体复形和连通图的分析框架推广到包含卷积、归一化、跳跃连接等结构的网络，或使用其他分段线性激活函数（如Leaky ReLU、GELU）的网络？

3. **拓扑特性与泛化的关联**：连通图直径、平均度数等拓扑特性是否与网络的泛化性能、对抗鲁棒性或校准误差存在定量关联？这需要在大规模真实数据集上进行系统实验。

4. **高效近似算法**：鉴于完全枚举的计算不可扩展性，是否存在高效近似算法来估计连通图的平均度数和直径，而无需遍历整个复形？这对高维实际应用至关重要。

5. **架构设计指导**：能否利用平均度数的$2d$上界和直径的$O(m^\ell)$上界来指导神经架构搜索、网络剪枝或数据增强策略？例如，直径上界与深度$\ell$的指数依赖关系是否暗示深层网络在表示拓扑上存在根本性约束？

6. **有界性与任务类型的关系**：Figure 7显示分类任务中含数据区域的无界比例更高，而回归任务中更低——这一差异是否反映了不同任务类型对决策边界几何的根本性不同需求？

## 原文 PDF

![[paperPDFs/ICLR_2026/Characterizing_the_Discrete_Geometry_of_ReLU_Networks.pdf]]
