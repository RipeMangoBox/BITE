---
title: "A Scalable Constant-Factor Approximation Algorithm for $W_p$ Optimal Transport"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Scalable_Constant_Factor_Approximation_Algorithm_for_W_p_Optimal_Transport.pdf
project_link: null
code_link: null
aliases:
- SWP
- SCFAAWPOT
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization
core_operator: "通过 Bourgain 多级采样构造有向 spanner，将 $\\mathsf{d}(\\cdot,\\cdot)^p$ 的近似问题转化为有向图中的最短路径问题，从而绕过 $\\mathsf{d}(\\cdot,\\cdot)^p$ 不满足三角不等式的困难。"
primary_logic: "利用多级聚类和精心选择的 Steiner 点构造有向 spanner，使得从任意 $b \\in B$ 到任意 $a \\in A$ 的最短路径距离能常数因子近似 $\\mathsf{d}(a,b)^p$，从而将 $W_p$ 最优传输问题简化为该稀疏有向图上的最小费用流问题。"
claims:
- "对于 $k=2$，有向 spanner 中从 $b$ 到 $a$ 的最短路径距离近似 $\\mathsf{d}(a,b)^p$ 的因子为 $(4+\\varepsilon)^p$。"
- "基于该 spanner 的最小费用流算法可在 $O(n^2 + (n^{3/2} \\varepsilon^{-1} \\log \\Delta \\log n)^{1+o(1)} \\log U)$ 时间内计算 $(4+\\varepsilon)$-近似 $W_p$ 最优传输计划。"
- "对于 $p = \\infty$，若存在 $O(n^2)$ 时间的 $(2-\\varepsilon)$-相对近似算法，则可解决二分图完美匹配的长期开放问题。"
- "合成正态分布数据 上 近似比 = 接近 2（平均）"
---

# A Scalable Constant-Factor Approximation Algorithm for $W_p$ Optimal Transport

> [!tip] 核心洞察
> 利用多级聚类和精心选择的 Steiner 点构造有向 spanner，使得从任意 $b \in B$ 到任意 $a \in A$ 的最短路径距离能常数因子近似 $\mathsf{d}(a,b)^p$，从而将 $W_p$ 最优传输问题简化为该稀疏有向图上的最小费用流问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种可扩展的常数因子近似算法用于 $W_p$ 最优传输 |
| 英文题名 | A Scalable Constant-Factor Approximation Algorithm for $W_p$ Optimal Transport |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=RPQKJxrEPs) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization |
| Method | 基于多级聚类有向 spanner 的 $W_p$ 最优传输近似算法 |
| Dataset | 合成正态分布数据, MNIST 数据集 (p=2), 均匀分布数据 |

> [!tip] 效果简介
> - 合成正态分布数据 上，近似比 为 接近 2（平均），对比 理论最坏情况 (4+ε)，变化 远优于理论界。
> - MNIST 数据集 (p=2) 上，近似比 为 接近 2（平均），对比 理论最坏情况 (4+ε)，变化 远优于理论界。
> - 均匀分布数据 上，近似比 为 接近 2（平均），对比 理论最坏情况 (4+ε)，变化 远优于理论界。

## 概要

本文提出了一种可扩展的常数因子近似算法，用于计算任意有限度量空间上 $W_p$ 最优传输（Optimal Transport, OT）问题。该问题的核心瓶颈在于：现有相对近似算法在任意度量空间下仅能达到 $O(\log n)$ 的近似比，且无法处理 $p = \infty$ 的情况；而精确算法或高精度近似算法（如 Sinkhorn）在 $p$ 较大时效率低下或无法扩展。

**核心方法**：通过 Bourgain 多级采样构造有向 spanner，将 $\mathsf{d}(\cdot,\cdot)^p$ 的近似问题转化为有向图中的最短路径问题，从而绕过 $\mathsf{d}(\cdot,\cdot)^p$ 不满足三角不等式的困难。具体地，对点集进行多级采样和聚类，生成簇集合，并在每个簇中引入 Steiner 点，构造一个稀疏有向图 $G$。该图的关键性质是：从任意 $b \in B$ 到任意 $a \in A$ 的最短路径距离能常数因子近似 $\mathsf{d}(a,b)^p$（Lemma 2.3）。基于此，$W_p$ 最优传输问题被简化为该稀疏有向图上的最小费用流问题。

**主要结果**：
- 对于 $p \in [1, \infty]$，可在 $O(n^2 + (n^{3/2} \varepsilon^{-1} \log \Delta \log n)^{1+o(1)} \log U)$ 时间内计算 $(4+\varepsilon)$-近似 $W_p$ 最优传输计划，成功概率至少 $1 - 1/n$（Theorem 1.1）。
- 对于任意整数 $k > 1$，可在 $O(n^{2+1/k} \log^2 n \log \Delta \log U)$ 时间内计算 $O(k)$-近似 $W_p$ 最优传输成本（Theorem 1.2）。
- 对于 $W_p$ 匹配（$|A|=|B|=n$），可在 $O(n^2 \varepsilon^{-3/2} \log^2 n \log \Delta)$ 时间内计算 $(4+\varepsilon)$-近似匹配（Theorem 1.3）。

**实验验证**：在合成正态分布数据、MNIST 数据集和均匀分布数据上的实验表明，算法的实际近似比远优于理论最坏情况界（通常接近 2），且簇诱导距离的最大失真从未超过理论保证的 $(4+\varepsilon)$ 因子。与基于 HST 嵌入的方法相比，使用簇诱导距离计算的最优匹配成本小 4.5 倍以上。

**局限性**：算法为 Las Vegas 随机化算法，存在小概率失败可能；运行时间依赖于点集 spread $\Delta$ 的对数；对于 $p = \infty$，条件性下界表明近似比 2 以下无法在 $O(n^2)$ 时间内实现（除非解决二分图完美匹配的长期开放问题）。



最优传输（Optimal Transport, OT）问题旨在寻找两个概率分布间的最小成本运输方案。在离散设定下，给定两个大小均为 $n$ 的点集 $A$ 和 $B$（代表支撑集），以及一个度量空间 $(\mathcal{X}, \mathsf{d})$，$W_p$ 最优传输计划 $\sigma$ 的成本定义为：

$$w_p(\sigma) := \left( \sum_{a \in A, b \in B} \sigma(a,b) \times \mathsf{d}(a,b)^p \right)^{1/p}$$

当 $p = \infty$ 时，成本退化为所有正运输质量对应点对的最大距离：$w_\infty(\sigma) := \max_{a,b \in A \times B : \sigma(a,b) > 0} \mathsf{d}(a,b)$。

**现有方法的根本瓶颈**在于：在任意度量空间下，所有已知的相对近似算法（即保证输出成本不超过最优成本的某个倍数）仅能达到 $O(\log n)$ 的近似比。具体而言：
- Charikar (2002) 基于 HST（分层分离树）嵌入的算法仅适用于 $W_1$ 且近似比为 $O(\log n)$。
- Lahn et al. (2025) 的算法虽推广到任意有限 $p$，但近似比仍为 $O(\log n)$，且无法处理 $p = \infty$ 的情形。
- 精确算法和高精度加法近似算法（如 Cuturi 2013 的熵正则化 Sinkhorn 算法）在 $p$ 较大时效率低下或无法扩展到大规模数据，且其误差依赖于数据直径。

**核心因果机制**在于：直接近似 $\mathsf{d}(a,b)^p$ 面临一个根本性困难——当 $p > 1$ 时，$\mathsf{d}(\cdot,\cdot)^p$ 不再满足三角不等式，这使得传统的度量嵌入和近似技术失效。现有方法依赖 HST 嵌入将距离扭曲为树度量，但树度量的固有失真导致 $O(\log n)$ 的近似比下界。

**本文的关键洞察**是：绕过直接近似 $\mathsf{d}(a,b)^p$，转而通过 Bourgain 多级采样构造一个有向 spanner（稀疏子图），将 $\mathsf{d}(a,b)^p$ 的近似问题转化为该有向图中的最短路径问题。具体而言，算法对点集 $P = A \cup B$ 进行多级聚类，在每个聚类中引入 Steiner 点，构造有向边，使得从任意 $b \in B$ 到任意 $a \in A$ 的最短路径距离能常数因子近似 $\mathsf{d}(a,b)^p$。对于 $k=2$ 级聚类，这个近似因子为 $(4+\varepsilon)^p$（Lemma 2.3）。这一转换将 $W_p$ 最优传输问题简化为该稀疏有向图上的最小费用流问题，从而首次实现了常数因子近似。

**证据强度**：Lemma 2.3 的证明在数学上严格，置信度为 1.0。Theorem 1.1 声明基于该 spanner 的最小费用流算法可在 $O(n^2 + (n^{3/2} \varepsilon^{-1} \log \Delta \log n)^{1+o(1)} \log U)$ 时间内计算 $(4+\varepsilon)$-近似 $W_p$ 最优传输计划。实验部分（Figure 1a, 1b, 2）显示实际近似比通常接近 2，远优于理论最坏情况，但实验仅基于合成数据和 MNIST 数据集，未在真实大规模应用中验证，置信度为 0.8。

**与现有方法的对比**：本文在三个关键维度上改变了算法设计空间：
1. **距离近似方式**：从 HST 嵌入或直接计算 $\mathsf{d}(a,b)^p$ 变为使用多级聚类构造有向 spanner，通过最短路径近似。
2. **近似比**：从 $O(\log n)$ 降低到常数 $(4+\varepsilon)$（$k=2$ 时）或 $O(k)$（一般 $k$）。
3. **适用范围**：从仅适用于有限 $p$ 扩展到所有 $p \in [1, \infty]$。

**一个重要的条件性下界**：Theorem 1.4 指出，若存在 $O(n^2)$ 时间的 $(2-\varepsilon)$-相对近似算法用于 $W_\infty$ 匹配，则可解决二分图完美匹配的长期开放问题（即是否存在 $O(n^2)$ 时间的完美匹配算法）。这暗示了本文的近似比在 $p = \infty$ 时可能接近最优。



## 核心方法与创新机理

本文的核心瓶颈在于：现有 $W_p$ 最优传输算法在任意度量空间下仅能达到 $O(\log n)$ 近似比，且无法处理 $p = \infty$ 的情况；同时，精确算法或高精度近似算法（如 Sinkhorn）在 $p$ 较大时效率低下或无法扩展。针对这一瓶颈，本文的关键因果旋钮是通过 Bourgain 多级采样构造有向 spanner，将 $\mathsf{d}(\cdot,\cdot)^p$ 的近似问题转化为有向图中的最短路径问题，从而绕过 $\mathsf{d}(\cdot,\cdot)^p$ 不满足三角不等式的困难。

**核心洞察**在于利用多级聚类和精心选择的 Steiner 点构造有向 spanner，使得从任意 $b \in B$ 到任意 $a \in A$ 的最短路径距离能常数因子近似 $\mathsf{d}(a,b)^p$，从而将 $W_p$ 最优传输问题简化为该稀疏有向图上的最小费用流问题。

**与 baseline 的关键差异**体现在三个 changed slots 上：

1. **距离近似方式**：Baseline（Charikar 2002, Lahn et al. 2025）使用 HST 嵌入或直接计算 $\mathsf{d}(a,b)^p$；本文使用多级聚类构造有向 spanner，通过最短路径近似 $\mathsf{d}(a,b)^p$。这一改变的支撑证据来自 Lemma 2.3，其证明了对于 $k=2$，有向 spanner 中从 $b$ 到 $a$ 的最短路径距离近似 $\mathsf{d}(a,b)^p$ 的因子为 $(4+\varepsilon)^p$。

2. **近似比**：Baseline 的近似比为 $O(\log n)$；本文将其改进为常数 $(4+\varepsilon)$（$k=2$ 时）或 $O(k)$（一般 $k$）。这一改进的代价是运行时间，但 Theorem 1.1 和 Theorem 1.2 分别给出了具体的时间复杂度上界。

3. **适用范围**：Baseline 仅适用于有限 $p$；本文适用于所有 $p \in [1, \infty]$。Theorem 1.1 明确给出了 $p = \infty$ 时的处理策略：通过二分搜索簇半径并计算最大流序列。

**证据强度评估**：Lemma 2.3 和 Theorem 1.1 的置信度为 1.0，是本文最核心的理论贡献。实验证据（Figure 1a, 1b, 2）显示实际近似比接近 2，远优于理论最坏情况 $(4+\varepsilon)$，但置信度仅为 0.8，因为实验仅在合成数据和 MNIST 上进行，未在真实大规模应用中验证。

**算法流水线**包含四个模块：多级聚类构造（对点集 $P$ 进行多级采样和聚类，生成簇集合 $\mathcal{C}$）、有向 spanner 构造（基于簇集合 $\mathcal{C}$ 构造有向图 $G$，包含 Steiner 点 $a_C, b_C$ 和相应边）、动态加权双色最近对 (BCP) 数据结构（维护每个簇中 $A$ 和 $B$ 点的最大堆，支持快速查询加权最近对）、以及最小费用流求解器或组合算法（在稀疏有向图 $G$ 上运行最小费用流算法或基于 BCP 的匈牙利搜索+DFS 增广的组合算法）。

**条件性下界**（Theorem 1.4）表明：对于 $p = \infty$，若存在 $O(n^2)$ 时间的 $(2-\varepsilon)$-相对近似算法，则可解决二分图完美匹配的长期开放问题。这一结果将本文的近似比改进空间与一个公开难题联系起来。



该算法的核心 pipeline 围绕“构造有向 spanner → 稀疏图上的最小费用流（或组合匹配）求解”展开，旨在将 $W_p$ 最优传输问题转化为一个可在近线性时间内求解的图问题。整个流程的瓶颈在于如何绕过 $\\mathsf{d}(\\cdot,\\cdot)^p$ 不满足三角不等式的困难，从而获得常数因子近似。

**输入与输出流：**
- **输入**：两个大小均为 $n$ 的离散概率分布（支撑集 $A$ 和 $B$），定义在度量空间 $(P, \\mathsf{d})$ 上，以及参数 $p \\in [1, \\infty]$ 和精度参数 $\\varepsilon$。
- **输出**：一个 $(4+\\varepsilon)$-近似 $W_p$ 最优传输计划（或匹配）。

**核心 Pipeline 模块及其关系：**

1.  **多级聚类构造**：对点集 $P = A \\cup B$ 进行多级采样和聚类。以论文中详细阐述的两层级为例：首先以概率 $n^{-1/2}$ 采样得到子集 $P_1$；然后，对于每个 $q \\in P_1$，以其为中心、按几何级数增长的半径 $r_i$ 构造簇 $C_q[i]$（包含其 Voronoi 区域内的点）；对于 $q \\notin P_1$ 的点，同样构造以 $q$ 为中心的簇。此模块的输出是簇集合 $\\mathcal{C}$，它定义了簇诱导距离 $d_\\mathcal{C}(x,y)$，该距离能常数因子近似真实距离 $\\mathsf{d}(x,y)$（Lemma 2.2）。该模块是后续所有步骤的基础，其计算复杂度为 $O(n^2 + n^{3/2} \\varepsilon^{-1} \\log \\Delta)$。

2.  **有向 Spanner 构造**：基于簇集合 $\\mathcal{C}$ 构造一个有向图 $G = (V, E)$。关键操作是为每个簇 $C \\in \\mathcal{C}$ 引入两个 Steiner 点 $a_C$ 和 $b_C$。图 $G$ 的顶点集 $V = A \\cup B \\cup \\{a_C, b_C \\mid C \\in \\mathcal{C}\\}$。边集 $E$ 的设计使得从任意 $b \\in B$ 到任意 $a \\in A$ 的最短路径距离能常数因子（如 $(4+\\varepsilon)^p$）近似 $\\mathsf{d}(a,b)^p$（Lemma 2.3）。这个模块将原始度量空间中的距离近似问题，转化为一个稀疏有向图中的最短路径问题，从而绕过了 $\\mathsf{d}(\\cdot,\\cdot)^p$ 不满足三角不等式的核心障碍。该图的稀疏性（平均度数 $O(n^{1/2} \\varepsilon^{-1} \\log \\Delta)$）是保证后续算法效率的关键。

3.  **动态加权双色最近对（BCP）数据结构**：该数据结构是连接 Spanner 构造与后续求解器的桥梁。它维护每个簇中 $A$ 和 $B$ 点的最大堆，支持快速查询具有最小加权距离 $d_w(a,b) = d_\\mathcal{C}^p(a,b) - w(a) - w(b)$ 的“最紧”边对。该模块负责在算法运行过程中，高效地找到需要松弛或增广的边，其更新操作的时间复杂度为 $O(n^{1/2} \\varepsilon^{-1} \\log n \\log \\Delta)$（Lemma 2.5）。

4.  **最小费用流求解器（或组合算法）**：这是最终的求解模块，在稀疏有向图 $G$ 上运行。论文提供了两种实现路径：
    - **基于最小费用流**：在 $G$ 上添加源点 $s$ 和汇点 $t$，设置边容量（$A$ 点质量、$B$ 点需求），并运行 Chen et al. (2022) 的最小费用流算法。得到的流 $f^*$ 可直接分解为传输计划 $\\sigma$，其 $W_p$ 成本满足 $(4+\\varepsilon)$-近似界（Theorem 1.1）。此路径理论效率高，但实现复杂。
    - **基于组合算法（用于匹配）**：采用匈牙利搜索 + DFS 增广的经典框架。利用 BCP 数据结构高效找到最小松弛量边（即“最紧”边），然后进行 DFS 寻找增广路。对偶权重的更新和增广操作交替进行，直到所有点都被匹配。此路径在 $W_p$ 匹配问题上实现了 $O(n^2 \\varepsilon^{-3/2} \\log^2 n \\log \\Delta)$ 的时间复杂度（Theorem 1.3），且更易于实现。

**模块间数据流总结：**
`点集 P` → (1) `多级聚类` → `簇集合 C` → (2) `Spanner构造` → `稀疏有向图 G` → (3) `BCP 数据结构`（辅助查询） → (4) `最小费用流/组合算法` → `近似最优传输计划 σ`

**失败模式与注意事项：**
- 算法为 Las Vegas 随机化算法，成功概率为 $1 - 1/n$，存在小概率失败可能。
- 运行时间依赖于点集 spread $\\Delta$ 的对数，当 $\\Delta$ 极大时（如指数级），$\\log \\Delta$ 项可能成为瓶颈。
- 对于 $p = \\infty$，论文证明了在 $O(n^2)$ 时间内实现 $(2-\\varepsilon)$-相对近似会解决一个长期开放的二分图完美匹配问题（Theorem 1.4），这构成了该问题在二次时间内的近似下界。



### 问题形式化与瓶颈

给定度量空间 $(P, \mathsf{d})$ 上的两个离散概率分布 $\mu$ 和 $\nu$，支撑集大小 $|A| = |B| = n$，$W_p$ 最优传输的目标是找到一个传输计划 $\sigma: A \times B \to \mathbb{R}_{\ge 0}$，最小化 $p$ 阶 Wasserstein 成本：

$$w_p(\sigma) := \left( \sum_{a \in A, b \in B} \sigma(a,b) \times \mathsf{d}(a,b)^p \right)^{1/p}$$

对于 $p = \infty$，成本退化为：

$$w_\infty(\sigma) := \lim_{p \to \infty} w_p(\sigma) = \max_{a,b \in A \times B : \sigma(a,b) > 0} \mathsf{d}(a,b)$$

核心瓶颈在于：$p \ge 1$ 时，$\mathsf{d}(\cdot,\cdot)^p$ 通常不满足三角不等式（除非 $p=1$），导致无法直接应用经典最短路径或嵌入技术。此前最优的相对近似算法（Lahn et al. 2025）仅能达到 $O(\log n)$ 近似比，且无法处理 $p = \infty$。

### 多级聚类构造

算法的核心模块是**多级聚类**，用于构造一个能常数因子近似 $\mathsf{d}(a,b)^p$ 的**有向 spanner**。

对于 $k=2$ 层聚类（两层级），构造过程如下：

1.  **采样**：设 $P_0 = P$。以概率 $n^{-1/2}$ 独立采样每个点，得到子集 $P_1 \subseteq P_0$。
2.  **Voronoi 划分**：对每个 $q \in P_1$，定义其 Voronoi 集：
    $$V(q, P_1) := \{ y \in P \mid \mathsf{d}(y, q) < \mathsf{d}(y, P_1) \}$$
3.  **簇生成**：对每个 $q \in P_1$ 和每个索引 $i$（对应半径 $r_i$），生成簇：
    - 若 $q \notin P_1$（即 $q$ 是二级中心）：$C_q[i] = \{ x \in V(q, P_1) \mid \mathsf{d}(x, q) \le r_i \}$
    - 若 $q \in P_1$（即 $q$ 是一级中心）：$C_q[i] = \{ x \in P_0 \mid \mathsf{d}(x, q) \le r_i \}$

半径 $r_i$ 以 $\varepsilon^{-1} \log \Delta$ 量级的数量呈几何级数增长，覆盖所有可能的距离尺度。

**簇诱导距离** $d_{\mathcal{C}}$ 定义为：对同时属于某个簇 $C$（索引为 $i$）的点 $x,y$，有 $d_{\mathcal{C}}(x,y) = 2 r_i$。该距离满足关键近似界（Lemma 2.2）：

$$d(x,y) \le d_{\mathcal{C}}(x,y) \le (4+\varepsilon) \cdot d(x,y)$$

对于一般 $k$ 级聚类，近似因子为 $2k(1+\varepsilon)$（Lemma B.3）。

### 有向 Spanner 构造

基于簇集合 $\mathcal{C}$，构造有向图 $G = (V, E)$：

- **顶点集**：$V = A \cup B \cup \{a_C, b_C \mid C \in \mathcal{C}\}$，其中 $a_C, b_C$ 是引入的 Steiner 点。
- **边集**：包含三类边：
    1.  从源点 $s$ 到每个 $a \in A$ 的边（容量为 $\mu(a)$，费用为 0）。
    2.  从每个 $b \in B$ 到汇点 $t$ 的边（容量为 $\nu(b)$，费用为 0）。
    3.  连接簇内点的边：对每个簇 $C$，所有 $a \in A \cap C$ 连向 Steiner 点 $a_C$（费用 0），$b_C$ 连向所有 $b \in B \cap C$（费用 0），且 $a_C$ 到 $b_C$ 的边费用为 $(2r_i)^p$。

**关键性质**：在 $G$ 中，从任意 $b \in B$ 到任意 $a \in A$ 的最短路径距离能常数因子近似 $\mathsf{d}(a,b)^p$。具体地，对于 $k=2$，近似因子为 $(4+\varepsilon)^p$（Lemma 2.3）。这通过将 $\mathsf{d}(a,b)^p$ 的近似问题转化为有向图中的最短路径问题，绕过了 $\mathsf{d}(\cdot,\cdot)^p$ 不满足三角不等式的困难。

### 最小费用流与组合算法

**最小费用流算法**：在稀疏有向图 $G$ 上运行最小费用流算法（Chen et al. 2022），得到流 $f^*$。通过路径分解，可从 $f^*$ 构造传输计划 $\sigma$，其成本满足：

$$w_p(\sigma) \le (4+\varepsilon) \cdot W_p(\mu, \nu)$$

对于 $p = \infty$，通过二分搜索簇半径并计算最大流序列实现。

**组合算法**：为提升实用性，论文设计了基于**动态加权双色最近对（BCP）** 数据结构的组合算法。该算法维护匹配 $M$ 和对偶变量 $y$，满足 **1-可行性条件**：

$$
\begin{array} { l l } 
{ y(a) + y(b) \le \hat{c}(a,b) + 1 } & { \qquad \mathrm{for~all} \ (a,b) \in A \times B, } \\
{ y(a) + y(b) = \hat{c}(a,b) } & { \qquad \mathrm{for~all} \ (a,b) \in M. }
\end{array}
$$

其中 $\hat{c}(a,b) = \lceil d_{\mathcal{C}}^p(a,b) / \delta \rceil$ 是缩放后的整数费用，$\delta$ 是缩放因子。边的**松弛量**定义为：

$$s(a,b) = \begin{cases} 0, & \mathrm{if~} (a,b) \in M, \\ \widehat{c}(a,b) - y(a) - y(b) + 1, & \mathrm{if~} (a,b) \notin M. \end{cases}$$

组合算法的核心循环包括：
1.  **匈牙利搜索**：使用 BCP 数据结构（维护有效权重 $w(b) = \delta(y(b) - \ell_b)$ 和 $w(a) = \delta y(a)$）找到最小松弛边。
2.  **对偶更新**：根据搜索树更新对偶变量：
    $$y(a) \gets y(a) - \ell_{a^\star} + \ell_a \quad \mathrm{for~all~} a \in S, \qquad y(b) \gets y(b) + \ell_{a^\star} - \ell_b \quad \mathrm{for~all~} b \in T$$
3.  **DFS 增广**：沿可容许边（满足 $\lceil (2r_i)^p / \delta \rceil - y(u) - y(v) + 1 = 0$）进行深度优先搜索，寻找增广路径。

### 时间复杂度与近似保证

- **两层级（$k=2$）**：时间复杂度 $O(n^2 + (n^{3/2} \varepsilon^{-1} \log \Delta \log n)^{1+o(1)} \log U)$，近似比 $(4+\varepsilon)$（Theorem 1.1）。
- **一般 $k$ 级**：时间复杂度 $O(n^{2+1/k} \log^2 n \log \Delta \log U)$，近似比 $O(k)$（Theorem 1.2）。
- **匹配版本**：时间复杂度 $O(n^2 \varepsilon^{-3/2} \log^2 n \log \Delta)$，近似比 $(4+\varepsilon)$（Theorem 1.3）。
- **$p = \infty$ 条件性下界**：若存在 $O(n^2)$ 时间的 $(2-\varepsilon)$-相对近似算法，则可解决二分图完美匹配的长期开放问题（Theorem 1.4）。



## 实验与关键发现

### 主结果与近似比验证

实验在合成正态分布、MNIST 数据集 (p=2) 和均匀分布上评估了双层聚类算法的近似比。三个基准测试一致显示，算法在实际中的平均近似比接近 **2**（参见 Figure 1a, 1b, Figure 2），远优于理论最坏情况保证的 $(4+\varepsilon)$ 因子。这一结果说明，理论分析中的常数因子由多级聚类构造中的最坏情况距离失真驱动，而实际数据中簇诱导距离 $d_{\mathcal{C}}$ 的失真通常远小于上界。

### 关键消融与机制验证

**距离失真分析**（Figure 1e）是理解近似比的核心消融实验：
- **最大失真**（worst-case distortion）从未超过 Lemma 2.2 的 $(4+\varepsilon)$ 理论保证，验证了构造的正确性。
- **平均失真**（average distortion）通常接近因子 **2**，解释了实验近似比远优于理论界的原因：大多数点对的距离近似误差远小于最坏情况。

**与 HST 嵌入的对比**（Figure 1f）进一步凸显了有向 spanner 的优势：使用 $d_{\mathcal{C}}$ 计算的最优匹配成本比使用 HST 距离的成本小 **4.5 倍以上**。这直接验证了核心洞察——绕过 $\mathsf{d}(\cdot,\cdot)^p$ 非三角不等式的有向 spanner 构造比基于 HST 的 O(log n) 近似算法在经验上更高效。

**图结构验证**：观察到的平均度数在维度 $d \leq 10$ 时紧密跟随理论界（Figure 1d），BCP 查询次数按理论预测增长且对所有 $p$ 几乎相同（Figure 1c），表明算法效率的理论分析在实验中成立。

### 失败模式与局限性

1. **理论最坏情况未在实验中复现**：实验数据（合成正态、MNIST、均匀分布）均具有相对规则的结构，未测试极端度量空间（如高维稀疏点集或 spread $\Delta$ 极大的情况）。在这些场景下，最大失真可能接近 $(4+\varepsilon)$，近似比劣化至理论界。
2. **$p=\infty$ 的硬性下界**：Theorem 1.4 表明，若存在 $O(n^2)$ 时间的 $(2-\varepsilon)$-相对近似算法，则可解决二分图完美匹配的长期开放问题。这意味着在 $p=\infty$ 时，近似比 2 以下在二次时间内几乎不可能实现，算法在此场景下存在固有限制。
3. **随机化失败概率**：算法为 Las Vegas 随机化算法，成功概率为 $1-1/n$。在极低概率的失败事件中，近似保证不成立，但实验未报告此类失败的发生频率。
4. **实验覆盖范围有限**：仅在合成数据和 MNIST 上验证，未在文档分类、拓扑数据分析等真实大规模应用中测试。对于长尾分布或非均匀质量分布，算法行为尚未验证。

### 重要图表结论

- **Figure 1e** 是最关键的消融图：它同时验证了理论正确性（最大失真不越界）和实际优越性（平均失真接近 2），直接支撑了“理论界保守而实际性能更好”的核心结论。
- **Figure 1f** 提供了与先前最优基线（HST 嵌入）的直接对比，定量展示了有向 spanner 在成本近似上的显著优势。
- **Figure 1a/b 和 Figure 2** 共同构成主结果验证，三个不同分布上的一致表现增强了结论的稳健性。



## 定位与知识库关联

### 与 Baseline / Follow-up 的关系

本文提出的基于多级聚类有向 spanner 的 $W_p$ 最优传输近似算法，在方法谱系中实现了两个关键突破：**将近似比从对数级压缩至常数级**，并**首次将适用范围扩展至 $p = \infty$**。

在基线方法方面，该算法直接针对两个先验工作的瓶颈进行改进。Charikar (2002) 基于 HST 嵌入的算法仅适用于 $W_1$ 且近似比为 $O(\log n)$，而 Lahn et al. (2025) 虽将适用范围扩展至任意有限 $p$，但近似比仍为 $O(\log n)$。本文通过构造有向 spanner 而非使用 HST 嵌入，将近似比降至常数 $(4+\varepsilon)$（$k=2$ 时）。实验证据（Figure 1f）表明，使用簇诱导距离 $d_{\mathcal{C}}$ 计算的最优匹配成本比使用 HST 距离的成本小 4.5 倍以上，实证验证了理论改进的有效性。

与熵正则化方法（Cuturi 2013）相比，本文算法属于相对近似而非加法近似。Sinkhorn 算法的误差依赖于直径，且无法处理 $p = \infty$；本文算法则对所有 $p \in [1, \infty]$ 均适用，且近似比与直径无关。这是该方法在适用性上的核心优势。

### 适用边界

该算法适用于**任意度量空间**中的离散 $W_p$ 最优传输问题，支持所有 $p \in [1, \infty]$。其核心机制——通过 Bourgain 多级采样构造有向 spanner，将 $\mathsf{d}(\cdot,\cdot)^p$ 的近似问题转化为有向图中的最短路径问题——绕过了 $\mathsf{d}(\cdot,\cdot)^p$ 不满足三角不等式的根本困难。这一设计使得算法在理论上适用于任何度量空间，无需特殊结构假设。

算法的边界条件体现在三方面：
1. **随机化依赖**：算法为 Las Vegas 随机化，成功概率为 $1 - 1/n$，存在小概率失败可能。
2. **数据规模依赖**：运行时间依赖于点集 spread $\Delta$ 的对数，当 $\Delta$ 呈指数级增长时，$\log \Delta$ 项可能显著增大。
3. **实现复杂度**：最小费用流求解器（Chen et al. 2022）理论上高效但实现复杂，实际中组合算法可能更实用。

### 局限与开放问题

**核心局限**：
- 实验验证范围有限：仅在合成正态分布、均匀分布和 MNIST 数据集上进行，未在真实大规模应用（如文档分类、拓扑数据分析）中验证。
- 实验仅报告了近似比和效率指标，未讨论算法对不同分布类型（如长尾分布）的公平性。
- 对于 $p = \infty$，条件性下界（Theorem 1.4）表明，若存在 $O(n^2)$ 时间的 $(2-\varepsilon)$-相对近似算法，则可解决二分图完美匹配的长期开放问题，暗示该近似比可能已接近理论极限。

**开放问题**：
1. **近似比下界**：能否将近似比从 $(4+\varepsilon)$ 进一步降低到 $2$ 或更小，同时保持 $O(n^2)$ 或更优的时间复杂度？
2. **$W_\infty$ 的精细复杂度**：是否存在 $O(n^2)$ 时间的 $(2-\varepsilon)$-相对近似算法用于 $W_\infty$ 匹配？这等价于解决二分图完美匹配的长期开放问题。
3. **连续分布扩展**：能否将算法扩展到连续分布或非离散支撑集？
4. **亚二次时间可行性**：能否在更弱的假设（如低倍率 doubling 度量空间）下实现亚二次时间？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Scalable_Constant_Factor_Approximation_Algorithm_for_W_p_Optimal_Transport.pdf

![[paperPDFs/ICLR_2026/A_Scalable_Constant_Factor_Approximation_Algorithm_for_W_p_Optimal_Transport.pdf]]
