---
title: "Distributional Equivalence in Linear Non-Gaussian Latent-Variable Cyclic Causal Models: Characterization and Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Distributional_Equivalence_in_Linear_Non_Gaussian_Latent_Variable_Cyclic_Causal_Models_Characterization_and_Learning.pdf
project_link: null
code_link: null
openreview_forum_id: b8TlYh6PN6
aliases:
- DELNGLVCCMCL
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "引入边缘秩（edge rank）及其与路径秩的对偶性，将全局的路径秩等价条件分解为局部的子代基（children bases）匹配条件，从而建立首个无需结构假设的分布等价性图形判据。"
primary_logic: "通过边缘秩约束和对偶定理，证明了分布等价性可由潜变量到所有变量的子代基（bases）集合的相等性来刻画，且该条件可进一步简化为对每个观测变量独立检查，使得全局等价性转化为一组局部可操作的组合条件。"
claims:
- "首次在含潜变量和循环的线性非高斯模型中建立了分布等价性的图形刻画。"
- "边缘秩（edge rank）是核心新工具，补全了潜变量因果发现工具箱中缺失的一块。"
- "定理2通过子代基集合给出了分布等价性的图形判据。"
- "等价类可通过可容许的边添加/删除和循环反转遍历，且最多只需一次循环反转。"
---

# Distributional Equivalence in Linear Non-Gaussian Latent-Variable Cyclic Causal Models: Characterization and Learning

> [!tip] 核心洞察
> 通过边缘秩约束和对偶定理，证明了分布等价性可由潜变量到所有变量的子代基（bases）集合的相等性来刻画，且该条件可进一步简化为对每个观测变量独立检查，使得全局等价性转化为一组局部可操作的组合条件。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 线性非高斯潜在变量循环因果模型中的分布等价性：刻画与学习 |
| 英文题名 | Distributional Equivalence in Linear Non-Gaussian Latent-Variable Cyclic Causal Models: Characterization and Learning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=b8TlYh6PN6) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | glvLiNG |
| Dataset | Erdős–Rényi随机图, n=13, ℓ=1, d=3, 高样本量N, n=5, avgdeg=1 (oracle OICA rank) |

> [!tip] 效果简介
> - Erdős–Rényi随机图, n=13, ℓ=1, d=3, 高样本量N 上，SHD (lower is better) 为 33.1，对比 35.3 (PO-LiNGAM)，变化 -2.2。
> - Erdős–Rényi随机图, n=5, ℓ=1, avgdeg=1 (oracle OICA rank) 上，运行时间 (秒) 为 0.015 ± 0.005，对比 0.045 ± 0.013 (MILP)，变化 -0.030。

## 概要

### 问题背景

线性非高斯因果模型（Linear Non-Gaussian, LiNG）在因果发现中占据重要地位，其核心优势在于利用非高斯性实现参数乃至图结构的可识别性。然而，当模型中存在潜在变量（latent variables）时，传统方法普遍依赖强结构假设——例如要求潜变量满足纯测量模型（pure measurement model）、层次结构（hierarchical structure）或三角无环条件——这些假设严重限制了模型在真实场景中的适用性。更根本的障碍在于：在允许任意潜变量结构和循环（cycles）的一般设定下，缺乏对**分布等价性**（distributional equivalence）的完整刻画。也就是说，我们不知道两个具有不同图结构的模型在何种条件下会在观测变量上诱导出完全相同的分布集合，因而无法设计通用的识别与发现算法。

### 核心贡献

本文针对上述空白，在**线性非高斯、含任意潜变量结构和循环**的因果模型中，首次建立了分布等价性的图形判据（graphical criterion）。其核心创新可归纳为三个层面：

1. **新工具：边缘秩（edge rank）**。传统方法依赖路径秩（path rank）来刻画变量间通过有向路径的连通瓶颈，但路径秩是全局量，需要遍历所有观测变量子集才能判定等价性。本文引入边缘秩——定义为二分图中从一组变量到另一组变量通过直接边的最大匹配数——并通过**对偶定理**（Theorem 1）证明路径秩与边缘秩之间存在精确的互补关系。这一工具填补了潜变量因果发现工具箱中长期缺失的一块。

2. **局部化判据**。利用边缘秩的对偶性质，本文将全局的路径秩等价条件分解为对每个观测变量独立检查的局部条件。具体而言，**定理2**表明：两个不可约模型分布等价，当且仅当潜变量到所有变量的**子代基集合**（children bases）在重标号下相等，且该条件可进一步简化为对每个观测变量 $X_i$ 增广后的子代基集合相等。这一分解使得等价性检查从指数级复杂度的子集遍历降为线性复杂度的逐变量检查。

3. **等价类遍历与表示**。**定理3**给出了等价类的变换刻画：任何两个等价图可通过一系列**可容许的边添加/删除**和**至多一次循环反转**相互转换。基于此，本文提出了**glvLiNG**算法，能够从观测数据中恢复完整的分布等价类，并以solid/dashed边的形式（定理4）输出——solid边表示在所有等价图中均出现的边，dashed边表示至少在某一等价图中出现的边。

### 方法定位

在方法谱系中，glvLiNG的独特之处在于**完全不依赖结构假设**。与依赖测量模型的PO-LiNGAM（Jin et al., 2024）或基于层次潜变量模型的LaHiCaSl（Xie et al., 2024）不同，glvLiNG允许潜变量之间及潜变量与观测变量之间的任意因果连接和循环。其算法流程分为四个模块：（1）利用过完备独立成分分析（OICA）从观测数据估计宽矩形混合矩阵；（2）Phase 1通过实现横向拟阵的二分图构造恢复潜变量的出边；（3）Phase 2利用定理2的局部分解独立恢复每个观测变量的出边；（4）基于定理3的可容许操作遍历整个等价类并生成solid/dashed边表示。

### 主要结果

在合成数据上的实验表明，当平均入度较高（$d=3$）时，glvLiNG在结构汉明距离（SHD）指标上一致优于PO-LiNGAM和LaHiCaSl，且对潜变量维度的增加表现出更强的鲁棒性——当潜变量数从 $\ell=1$ 增至 $\ell=5$ 时，glvLiNG的SHD仅从33.1微增至35.7，而PO-LiNGAM则从35.3显著恶化至50.7。在运行效率方面，glvLiNG相比基于混合整数线性规划的精确求解基线快出一个数量级以上，且Phase 2（观测变量出边恢复）的运行时间占比在所有实验中均低于总时间的1%，验证了两阶段设计的高效性。在真实股票市场数据上，glvLiNG成功恢复出一个包含19,008个因果图的等价类，并以solid/dashed边形式呈现了各行业板块间的稳健因果连接与可能连接。

### 局限与展望

当前方法依赖OICA估计混合矩阵的精度，在样本量有限或非高斯性较弱时性能可能受限。理论上，边缘秩约束和等价性刻画目前仅适用于线性非高斯模型，向非线性或非参数设定的推广仍是开放问题。此外，等价类在最坏情况下可能包含指数级数量的图，实际应用中需结合稀疏性先验或额外约束来压缩搜索空间。

### 潜变量因果发现的核心瓶颈

从观测数据中恢复因果结构是因果推断的基石问题。当系统中存在未观测的潜在混杂因子时，问题难度急剧上升——我们不仅需要推断观测变量之间的因果关系，还必须同时处理潜变量与观测变量之间、以及潜变量之间的未知结构。现有潜变量因果发现方法普遍依赖强结构假设来使问题可解：**PO-LiNGAM**（Jin et al., 2024）要求潜变量遵循纯测量模型（每个潜变量有一组专属的观测子节点），**LaHiCaSl**（Xie et al., 2024）则依赖层次化的潜变量结构和广义独立噪声（GIN）条件，且这些方法通常假设因果图为有向无环图（DAG）。

然而，现实世界中的潜变量结构往往不满足这些理想化假设——潜变量之间可能存在任意的因果关系，观测变量可能同时受到多个潜变量的直接影响，反馈循环也普遍存在。当这些结构假设被违反时，现有方法面临严重的模型误设问题。**Table 5** 的实验结果表明，在任意的潜变量模型下，PO-LiNGAM 和 LaHiCaSl 均倾向于产生过于稀疏的图，且错误识别超过半数的边（例如在 n=20, ℓ=5, avgdeg=4 的设定下，PO-LiNGAM 的 SHD 高达 167.86 ± 11.28，LaHiCaSl 为 142.76 ± 11.39）。

这一困境的根本障碍在于：**我们缺乏对一般设定下分布等价性的刻画**。在因果发现中，分布等价性刻画了哪些不同的因果图会在观测数据上诱导出相同的分布集合——只有理解了“什么可以被识别”，才能设计出通用的识别方法。在完全观测的线性非高斯设定下，分布等价性已被 LiNGAM 的完全可识别性所解决；在含潜变量的线性高斯设定下，Trek-separation 和 mDAG 提供了有力的刻画工具。但在**含潜变量且允许循环的线性非高斯模型**中，分布等价性此前一直缺乏图形判据。

### 从路径秩到边缘秩：一项缺失的工具

线性非高斯模型的核心可识别性来源于独立成分分析（ICA）的经典结果：在非高斯性假设下，混合矩阵的列秩模式编码了因果图的路径信息。具体而言，从潜变量 L 到观测变量 X 的**路径秩**（path rank）——即 L 到 X 之间顶点不相交有向路径的最大数目——决定了混合矩阵对应子矩阵的秩。因此，两个因果图分布等价，当且仅当它们对所有潜变量子集到观测变量子集产生相同的路径秩（至潜变量重标号）。

但路径秩是全局量：要验证两个图在所有子集上的路径秩是否相等，需要检查指数级数量的子集组合，这在计算上不可行，也无法直接转化为局部的图形判据。

本文的关键创新在于引入**边缘秩**（edge rank）这一新工具。边缘秩定义为从集合 Y 到 Z 通过图中直接边的最大二分匹配的大小（允许自匹配），是一个仅依赖于局部邻接关系的组合量。**Theorem 1** 建立了路径秩与边缘秩之间的精确对偶关系：

$$\min(|Z|,|Y|) - \rho_{\mathcal{G}}(Z,Y) = |V| - \max(|Z|,|Y|) - r_{\mathcal{G}}(V \setminus Y, V \setminus Z)$$

这一对偶性使得原先需要全局检查的路径秩等价条件，可以被转化为局部的边缘秩条件。更重要的是，边缘秩允许将全局等价性**分解为对每个观测变量的独立检查**（Lemma 5 的局部分解）：不再需要检查所有子集 x ⊆ X，只需对每个 X_i ∈ X 单独验证子代基（children bases）的匹配条件即可。这正是 **Theorem 2** 的核心贡献——首次在无需任何结构假设的前提下，给出了含潜变量和循环的线性非高斯模型分布等价性的图形判据。

### 本文的定位与贡献

**Table 2** 将本文的贡献置于更广阔的方法谱系中：在完全观测无环设定下，等价性由 Markov 等价类刻画；在含潜变量的无环设定下，Trek-separation 和 mDAG 提供了高斯情形下的刻画；而本文首次在线性非高斯、含潜变量且允许循环的设定下，建立了基于路径秩/边缘秩的等价性刻画，并给出了等价类的可遍历变换表征（**Theorem 3**：通过可容许的边添加/删除和至多一次循环反转即可遍历整个等价类），以及简洁的 solid/dashed 边表示（**Theorem 4**）。

基于这些理论结果，本文提出了 **glvLiNG** 算法，该算法无需任何结构假设，从 OICA 估计的混合矩阵出发，通过两阶段列增广过程恢复因果图，并输出完整的分布等价类。这填补了潜变量因果发现工具箱中长期缺失的一块：一种通用的、不依赖结构假设的方法，能够处理任意的潜变量结构和反馈循环。

## 核心方法与创新机理

### 瓶颈突破：从结构假设到无假设的分布等价性刻画

现有潜变量因果发现方法的根本瓶颈在于对潜变量结构施加了强假设。**PO-LiNGAM**（Jin et al., 2024）依赖测量模型——潜变量通过纯测量模式连接到观测变量；**LaHiCaSl**（Xie et al., 2024）基于层次潜变量模型和GIN条件，同样预设了特定的潜变量-观测变量拓扑。这些方法不仅限制了可处理的因果结构类型，更关键的是，它们通常假设因果图为有向无环图（DAG），无法应对现实世界中普遍存在的反馈循环。

更深层的问题在于缺乏一般性的分布等价性刻画：当潜变量之间存在任意因果关系、且允许循环时，两个不同的因果图何时会在观测变量上产生无法区分的分布？不知道什么可以被识别，就无法设计通用的识别方法。本文正是在这一根本问题上实现了突破——**首次在含任意潜变量结构和循环的线性非高斯模型中，建立了分布等价性的图形判据**。

### 核心工具：边缘秩及其对偶理论

实现这一突破的关键在于引入了一个新工具——**边缘秩**（edge rank）。传统方法依赖路径秩（path rank）来刻画变量间的因果关系强度，但路径秩本质上是全局量：它衡量从源集合到目标集合的顶点不相交有向路径的最大数目，需要通过最小割计算，且用于等价性检查时需要对所有子集进行指数级验证。

边缘秩则提供了互补的局部视角。其定义为从集合 $Y$ 到 $Z$ 通过直接边的最大二分匹配大小：

$$r_{\mathcal{G}}(Z,Y) := \text{从 }Y\text{ 到 }Z\text{ 通过 }\mathcal{G}\text{ 中边的最大二分匹配的大小（允许自匹配）}$$

这一量度仅依赖图的直接边结构，是局部可算的组合量。**定理1**建立了路径秩与边缘秩之间的精确对偶关系：

$$\operatorname*{min}(|Z|,|Y|) - \rho_{\mathcal{G}}(Z,Y) = |V| - \operatorname*{max}(|Z|,|Y|) - r_{\mathcal{G}}(V \setminus Y, V \setminus Z)$$

这一对偶性意味着，原本需要全局路径计算的秩约束，可以通过局部的边缘匹配条件等价表达。Table 1系统对比了两种秩在直觉、满秩条件、图约束、拟阵表示和对偶性五个维度的差异，边缘秩在“图约束”和“拟阵表示”维度上展现出更强的局部可操作性。

### 方法论跃迁：从全局条件到局部可操作判据

边缘秩的引入带来了方法论上的质变。基于路径秩的等价性条件（Lemma 3）要求对所有观测变量的子集 $x \subseteq X$ 和所有顶点子集 $Y \subseteq V$ 检查秩相等性，复杂度为指数级，无法直接用于算法设计。

边缘秩使得这一条件得以**局部分解**：等价性检查不再需要遍历所有子集，而仅需对每个观测变量 $X_i$ 独立验证。具体而言，**定理2**给出了分布等价性的图形判据——两个不可约模型 $(\mathcal{G}, X)$ 和 $(\mathcal{H}, X)$ 分布等价，当且仅当存在顶点置换 $\pi$，使得：

$$\mathrm{bases}_{\mathcal{G}}(L) = \pi(\mathrm{bases}_{\mathcal{H}}(L)), \quad \text{且}$$

$$\mathrm{bases}_{\mathcal{G}}(L \cup \{X_i\}) = \pi(\mathrm{bases}_{\mathcal{H}}(L \cup \{X_i\})) \quad \text{对每个 } X_i \in X$$

其中 $\mathrm{bases}_{\mathcal{G}}(Y)$ 是 $Y$ 的**子代基**（children bases）集合，定义为能够与 $Y$ 形成完美边缘匹配的顶点子集。这一判据将全局等价性转化为对潜变量和每个观测变量的独立局部条件检查，使得算法设计成为可能。

### 等价类的可遍历性：变换刻画

进一步，**定理3**给出了等价类的变换刻画：两个不可约模型分布等价，当且仅当一个图可以通过一系列**可容许操作**变换为另一个图（至潜变量重标号）。这些可容许操作包括：
- **边添加/删除**：当目标边满足余环条件（Lemma 7）时，添加或删除该边不改变分布等价性；
- **循环反转**：不相交的循环可自由反转（Lemma 6），且整个等价类中**最多只需一次循环反转**即可遍历所有图。

这一定理将抽象的等价类概念转化为可操作的图变换空间，直接支撑了算法的等价类遍历模块。

### Changed Slots：与基线方法的结构性差异

| 维度 | 基线方法（PO-LiNGAM, LaHiCaSl等） | 本文方法（glvLiNG） |
|------|----------------------------------|---------------------|
| **结构假设** | 依赖潜变量的指示模式（测量模型、层次结构），通常假设无环 | 无任何结构假设，允许潜变量间及潜变量-观测变量间的任意因果结构和循环 |
| **等价性输出** | 仅输出单个点估计（因果图），不考虑等价类 | 输出完整的分布等价类（以solid/dashed边表示），并可遍历等价类中所有图 |

这两个changed slots直接源于前述理论突破：无结构假设之所以可能，是因为边缘秩判据不预设任何潜变量拓扑；等价类输出之所以可行，是因为定理3提供了遍历等价类的可容许操作集合。glvLiNG算法通过两阶段设计——Phase 1恢复潜变量出边、Phase 2独立恢复每个观测变量的出边——将理论判据转化为可扩展的计算流程，并在等价类遍历中利用定理3的变换操作生成完整的solid/dashed边表示。

### 证据强度与边界

上述核心创新的证据链坚实：定理2和定理3提供了严格的数学证明（confidence 0.98），边缘秩与路径秩的对偶性（定理1）在理论上完整（confidence 0.95）。仿真实验中，glvLiNG在无结构假设下仍能与依赖强假设的基线方法竞争（SHD 33.1 vs PO-LiNGAM 35.3），且在稠密图中因无假设优势表现更优。运行时间上，glvLiNG比精确MILP基线快数个数量级（n=5时0.015s vs 0.045s），验证了局部判据的计算效率。

需注意的边界：当前理论仅适用于线性非高斯模型，向非线性或高斯系统的推广仍是开放问题；等价类遍历在最坏情况下可能包含指数级数量的图，实际应用需结合稀疏性先验。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_b8TlYh6PN6/figures/005_Table_1.jpg]]
*Table 1: A side-by-side comparison between path ranks and edge ranks*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_b8TlYh6PN6/figures/014_Table_2.jpg]]
*Table 2: A side-by-side overview of representative works on equivalence characterizations across different settings using different approaches. The final column summarizes this work’s contributions*


本节给出 glvLiNG 算法的整体 pipeline 及其背后的设计逻辑。算法将分布等价类的恢复分解为三个顺序步骤，每个步骤对应一个核心理论结果，形成从数据到等价类表征的完整通路。

### 输入输出流

- **输入**：观测变量 $X$ 的独立同分布样本。
- **输出**：以 solid/dashed 边形式呈现的分布等价类表征，其中 solid 边表示等价类中所有图均存在的边，dashed 边表示至少存在一个等价图包含该边。等价类内部可通过边添加/删除和循环反转遍历。

### 三阶段 Pipeline

**阶段 0：OICA 估计混合矩阵**

利用过完备独立成分分析（OICA）从观测数据中估计宽矩形混合矩阵 $\tilde{A}_{X,:}$，得到其秩模式（rank pattern）。实现上采用 SDP-ICA（Podosinnikova et al., 2019），因其在实验中倾向于提供最优的混合矩阵估计。该阶段是整个 pipeline 的瓶颈——OICA 的精度受样本量及实际非高斯性程度影响，可能限制小样本或弱非高斯场景下的性能。

**阶段 1：潜变量出边恢复**

从混合矩阵中恢复潜变量 $L$ 到所有变量 $V$ 的边。核心操作是通过构造实现横向拟阵（transversal matroid）的二分图，将混合矩阵的列增广以满足拟阵基约束。该阶段利用了边缘秩约束在潜变量到全体变量子集上的全局匹配性质。

**阶段 2：观测变量出边恢复**

利用定理 2 的局部分解性质，独立地为每个观测变量 $X_i$ 增广对应的列，恢复观测变量 $X$ 到所有变量 $V$ 的边。这一设计的关键洞察是：边缘秩允许将原本需要对 $X$ 的所有子集进行指数级检查的全局等价性条件，简化为仅需对每个 $X_i$ 独立检查的局部条件。实验消融表明，Phase 2 的运行时间占比在所有实验中均低于总时间的 1%，验证了两阶段设计的高效性。

**等价类遍历**

从恢复的单个图出发，依据定理 3 的可容许操作（边添加/删除、循环反转）进行 BFS/DFS 遍历整个等价类，并生成定理 4 的 solid/dashed 边表示。定理 3 保证任意两个等价图可通过一系列可容许操作相互转换，且最多只需一次循环反转。

### 设计逻辑：从路径秩到边缘秩的简化

整个 pipeline 的可行性建立在边缘秩（edge rank）替代路径秩（path rank）这一核心转折点上。路径秩等价条件（Lemma 3）虽然给出了分布等价性的纯图形刻画，但需要对 $X$ 的所有子集进行指数级检查，无法直接用于算法设计。边缘秩通过定理 1 的对偶关系与路径秩等价，但具有局部可算的组合性质——它衡量从集合 $Y$ 到 $Z$ 通过直接边可实现的最大二分匹配数。这一性质使得 Lemma 5 的全局条件被分解为定理 2 中的子代基（children bases）匹配条件，进而使 Phase 2 的逐变量独立恢复成为可能。

### 与现有方法的根本差异

现有潜变量因果发现方法（如 PO-LiNGAM、LaHiCaSl）普遍依赖强结构假设：PO-LiNGAM 基于测量模型假设潜变量仅通过观测变量的指示模式体现，LaHiCaSl 依赖层次潜变量结构和 GIN 条件，且通常假设无环。这些方法仅输出单个点估计（因果图），不考虑等价类。glvLiNG 则无任何结构假设，允许潜变量之间及潜变量与观测变量之间的任意因果结构和循环，并输出完整的分布等价类表征。这一能力来源于对分布等价性本身的完整刻画——知道什么可以被识别，才能设计通用的识别方法。

### 关键公式与变量含义

本节聚焦于分布等价性刻画与算法构造所依赖的核心公式，按其在理论链条中的角色分层呈现。

**线性非高斯结构方程与混合形式**

模型的基础是线性非高斯结构方程模型：

$$V = B V + E$$

其中 $V$ 为全体变量（观测变量 $X$ 与潜变量 $L$ 的并集），$B$ 为加权邻接矩阵（$B_{V_j, V_i} \neq 0$ 当且仅当 $V_i \to V_j \in \mathcal{G}$），$E$ 为相互独立的非高斯外生噪声。假设 $I - B$ 可逆，模型可等价地写为混合形式：

$$V = (I - B)^{-1} E =: A E$$

其中 $A$ 为总因果效应矩阵。这一混合形式是将因果图结构约束转化为矩阵秩约束的桥梁。

**路径秩定义**

路径秩是刻画分布等价性的第一代工具，定义为从集合 $Y$ 到 $Z$ 的顶点不相交有向路径的最大数目，等价于最小割：

$$\rho_{\mathcal{G}}(Z,Y) := \min_{\mathbf{c} \subseteq V(\mathcal{G})} \{ |\mathbf{c}| : \mathbf{c}\text{ 的移除使 }\mathcal{G}\text{ 中不存在从 }Y \setminus \mathbf{c}\text{ 到 }Z \setminus \mathbf{c}\text{ 的路径}\}$$

在泛型参数下，混合矩阵的子矩阵秩等于对应的路径秩：$\operatorname{rank}(A_{Z,Y}) = \rho_{\mathcal{G}}(Z,Y)$。由此，分布等价性可转化为路径秩的等式约束（引理3）：存在顶点置换 $\pi$ 使得对所有 $Z \subseteq X$ 和 $Y \subseteq V(\mathcal{G})$ 有 $\rho_{\mathcal{G}}(Z,Y) = \rho_{\mathcal{H}}(Z, \pi(Y))$。

**边缘秩定义——核心新工具**

路径秩虽精确，但涉及全局路径结构，难以局部操作。边缘秩作为本文的核心新工具，定义为从 $Y$ 到 $Z$ 通过图中直接边的最大二分匹配的大小：

$$r_{\mathcal{G}}(Z,Y) := \text{从 }Y\text{ 到 }Z\text{ 通过 }\mathcal{G}\text{ 中边的最大二分匹配的大小（允许自匹配）}$$

等价的最小割形式为：

$$r_{\mathcal{G}}(Z,Y) := \min_{z \subseteq Z,\; y \subseteq Y,\; z \cup y \supseteq Z \cap Y} \{ |z| + |y| : \text{不存在从 }Y \setminus y\text{ 到 }Z \setminus z\text{ 的边}\}$$

在支持矩阵（二元邻接矩阵的闭包）上，边缘秩等于矩阵的匹配秩（matching rank），即通过列置换可使对角线上非零元最大化的数量：

$$\operatorname{mrank}(M) := \max_{P \in \operatorname{Perm}(n)} \sum_{i=1}^{\min(m,n)} \mathbb{1}((MP)_{i,i} \neq 0)$$

**路径秩与边缘秩的对偶定理**

定理1建立了两种秩之间的精确对偶关系，是理论框架的基石：

$$\min(|Z|,|Y|) - \rho_{\mathcal{G}}(Z,Y) = |V| - \max(|Z|,|Y|) - r_{\mathcal{G}}(V \setminus Y, V \setminus Z)$$

该对偶性表明：路径秩衡量“瓶颈”的大小，边缘秩衡量“非瓶颈”的容量，二者提供关于图中连通结构的互补视角（参见 Table 1 的并排对比）。

**分布等价性的图形判据——子代基条件**

利用边缘秩的局部可操作性，定理2将全局的分布等价性刻画分解为子代基（children bases）的匹配条件。定义子代基集合为：

$$\operatorname{bases}_{\mathcal{G}}(Y) := \{ Z \subseteq \operatorname{ch}_{\mathcal{G}}(Y) \cup Y : r_{\mathcal{G}}(Z, Y) = |Z| = |Y| \}$$

即从 $Y$ 出发存在完美边缘匹配的那些顶点集。定理2断言：两个不可约模型 $(\mathcal{G}, X)$ 与 $(\mathcal{H}, X)$ 分布等价，当且仅当存在顶点置换 $\pi$ 使得：

$$\operatorname{bases}_{\mathcal{G}}(L) = \pi(\operatorname{bases}_{\mathcal{H}}(L))$$

且对每个观测变量 $X_i \in X$ 有：

$$\operatorname{bases}_{\mathcal{G}}(L \cup \{X_i\}) = \pi(\operatorname{bases}_{\mathcal{H}}(L \cup \{X_i\}))$$

这一判据的关键突破在于：原本需要对所有 $X$ 的子集检查路径秩（指数级复杂度），现在只需独立检查每个 $X_i$ 的局部子代基条件（引理5的局部分解）。

**可容许边添加条件**

引理7给出了在不改变分布等价性的前提下可添加边 $V_i \to V_j$ 的充要条件：

$$r_{\mathcal{G}}(V_i\text{的非子节点}\setminus \{V_j\}, L \setminus \{V_i\}) < r_{\mathcal{G}}(V_i\text{的非子节点}, L \setminus \{V_i\})$$

即 $V_j$ 在潜变量到 $V_i$ 非子节点的二分图中是一个余环（cocircuit）元素。这一条件为等价类遍历中的边添加/删除操作提供了精确的局部判据。

---

### 算法管线核心模块

glvLiNG 算法由四个核心模块串联而成，每个模块对应上述理论链条的一个环节。

**模块一：OICA 估计**

利用过完备独立成分分析（SDP-ICA，Podosinnikova et al., 2019）从观测数据中估计宽矩形混合矩阵 $A_{X,:}$，得到秩模式。该模块是算法与数据的接口，其精度直接影响后续步骤。实践中，SDP-ICA 的 MATLAB 实现提供了最佳的估计质量。

**模块二：Phase 1——潜变量出边恢复**

从混合矩阵的秩模式出发，通过实现横向拟阵（transversal matroid）的二分图构造，恢复潜变量 $L$ 到所有变量 $V$ 的边。具体而言，该模块构造一个二分图，使其匹配结构满足拟阵的基约束，从而将代数秩约束转化为具体的图边。

**模块三：Phase 2——观测变量出边恢复**

利用定理2的局部分解性质，独立地为每个观测变量 $X_i$ 增广对应的列，恢复观测变量 $X$ 到所有变量 $V$ 的边。由于每个 $X_i$ 可独立处理，该阶段的计算开销极低——消融实验表明 Phase 2 的运行时间在所有实验中均低于总时间的 1%（Table 4）。

**模块四：等价类遍历**

从恢复的单个图出发，依据定理3的可容许操作（边添加/删除、循环反转）通过 BFS/DFS 遍历整个等价类。定理3保证：任意两个等价图可通过一系列可容许的边添加/删除和至多一次循环反转相互转换。最终输出定理4定义的 solid/dashed 边表示：solid 边在所有等价图中均出现，dashed 边在至少一个等价图中出现。

## 实验与关键发现

### 主结果

#### 结构误设下的鲁棒性优势

现有潜变量因果发现方法普遍依赖强结构假设，例如 **PO-LiNGAM**（Jin et al., 2024）基于测量模型，**LaHiCaSl**（Xie et al., 2024）基于层次潜变量模型和GIN条件，二者均假设图无环。当真实模型违反这些假设时，两类基线方法均倾向于产生过度稀疏的图，并错误识别超过一半的边（Table 5）。相比之下，glvLiNG 无需任何结构假设，允许潜变量之间及潜变量与观测变量之间的任意因果结构和循环，因而在结构误设场景下展现出根本性的鲁棒性优势。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_b8TlYh6PN6/figures/017_Table_5.jpg]]
*Table 5: Algorithms are provided with their oracle tests, that is, for them to directly query oracle generalized independent noise (GIN) conditions from the digraph. When the number of their identified latent variables is fewer than truth, we simply add isolated latent variables into the result. When the identified number of latents is larger (which seems not happened), we planned to choose the removal that leads to best result. Finally, the best possible result is reported, i.e., we choose the digraph in the ground-truth equivalence class that is closer to their output as the truth. The latent variables are viewed as unlabeled*

#### SHD 对比

在 Erdős–Rényi 随机图生成的真实模型上（n=13, ℓ=1, 平均入度 d=3），glvLiNG 在高样本量下的平均 SHD 为 33.1，显著优于 PO-LiNGAM 的 35.3（差距 -2.2）。需注意，所有方法的 SHD 度量均取相对于真实等价类中所有图的最小距离，这一度量对输出等价类的方法与输出单图的方法均是公平的。

#### 运行时间对比

在 oracle OICA 秩模式下，glvLiNG 的图构造速度远超精确求解基线 MILP。以 n=5, ℓ=1, avgdeg=1 为例，glvLiNG 的运行时间仅为 0.015 ± 0.005 秒，而 MILP 需要 0.045 ± 0.013 秒（差距约 3 倍）。当问题规模增大至 n=10 时，glvLiNG 可在 5 秒内完成求解，而 MILP 在 n>5 后即需要数小时，差距呈指数级扩大（Table 4）。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_b8TlYh6PN6/figures/016_Table_4.jpg]]
*Table 4: Running time comparison between our glvLiNG algorithm and a mixed integer linear programming (MILP) baseline for constructing digraphs that satisfy the rank constraints of oracle OICA mixing matrices. Ground-truth graphs are generated from the Erdos–Rényi model with total ˝ number of vertices n and average in-degree avgdeg, with ℓ vertices randomly designated as latent. Each entry reports the mean and standard deviation over 50 models (when completed); empty entries indicate runs that did not finish within 10 minutes. All times are reported in seconds. Experiments were run on an Apple M4 chip*

#### 等价类规模量化

Table 3 给出了不同规模下分布等价类的统计。以 n=5、前 2 个顶点为潜变量为例，在 480,640 个不可约模型中，仅存在 783 个分布等价类，表明等价类具有显著的压缩效应——大量看似不同的图结构实际上在观测分布上不可区分。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_b8TlYh6PN6/figures/015_Table_3.jpg]]
*Table 3: For different numbers of vertices n and latent vertices l, we report the total number of weakly connected digraphs with n vertices, the subset that are irreducible when the first l vertices are latent (both with and without L-isomorphic variants), and the corresponding numbers of distributional equivalence classes they fall into. The final two columns present statistics on how irreducible digraphs (both ut L-isomorphic variants) are distributed among those equiv*

### 消融分析

#### 两阶段设计的效率验证

glvLiNG 的 Phase 1（潜变量出边恢复）承担了主要的计算负载，而 Phase 2（观测变量出边恢复）的运行时间占比极低。Table 4 数据显示，在 n=5, avgdeg=1 的设置下，Phase 1 耗时 0.014 ± 0.005 秒，Phase 2 仅耗时 0.001 ± 0.000 秒，后者的占比在所有实验中均低于总时间的 1%。这一消融结果直接验证了定理 2 的核心价值：通过边缘秩约束，原先需要指数级子集检查的全局等价性条件被简化为仅需对每个观测变量独立检查的局部条件，使得 Phase 2 的计算代价几乎可忽略。

#### OICA 估计质量的影响

glvLiNG 的性能依赖于过完备独立成分分析（OICA）对混合矩阵的估计精度。在稀疏图中（低平均入度），OICA 估计误差可能导致 glvLiNG 的 SHD 略逊于利用结构假设的基线方法；但在稠密图中，glvLiNG 因其无结构假设的优势表现更优。这一现象在 Figure 7 中随样本量变化的曲线上清晰可见：当样本量不足时，OICA 的估计噪声成为性能瓶颈。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_b8TlYh6PN6/figures/018_Figure_7.jpg]]
*Figure 7: Simulation results comparing glvLiNG with existing methods with varying sample size N (the global x-axis), and each subplot shows a setting under a specific number of total variables n, number of latent variables $\ell$ , and the average in-degree d. Mean and standard deviation of SHD are calculated from 25 random irreducible models*

### 失败模式与局限

1. **小样本/弱非高斯场景**：当前方法依赖 OICA 估计混合矩阵，其精度受样本量及实际非高斯性程度影响。在小样本或噪声接近高斯的场景下，OICA 的秩模式估计可能不可靠，进而导致后续图恢复失败。

2. **潜变量数量需预先指定**：尽管理论上潜变量数量可从混合矩阵的秩信息中识别，实践中仍需预先指定潜变量数量 ℓ，并通过验证集选择最优值。错误的 ℓ 设定将直接导致恢复的图结构偏离真实等价类。

3. **等价类遍历的规模瓶颈**：尽管理论上等价类可通过可容许的边添加/删除和至多一次循环反转遍历（定理 3），但在最坏情况下等价类可能包含指数级数量的图。当前实现对于大规模图的遍历可能需要结合额外的稀疏性或先验约束才能实际可行。

4. **线性非高斯假设的边界**：边缘秩约束和等价性理论仅适用于线性非高斯模型。向非线性或非参数模型的推广仍是开放问题，当前框架无法处理此类设定。

### 关键图表结论

- **Table 1**：系统对比了路径秩与边缘秩在直觉、满秩条件、图约束、拟阵表示和对偶性五个维度上的差异，确立了边缘秩作为局部可算组合工具的理论地位。
- **Table 2**：将本文贡献置于跨设定的等价性刻画谱系中，表明本文首次在含潜变量和循环的线性非高斯模型中建立了完整的分布等价性图形判据。
- **Figure 7**：随样本量变化的 SHD 曲线揭示了 glvLiNG 与基线方法的交叉现象——稀疏图中基线方法在小样本下占优，稠密图中 glvLiNG 始终领先，反映了结构假设与数据效率之间的权衡。
- **Figure 8**：在股票市场真实数据上，glvLiNG 输出的等价类以 solid/dashed 边的形式呈现，solid 边表示在所有等价图中必然出现的边，dashed 边表示至少在一个等价图中存在的边，为实际应用中的因果解释提供了可操作的确定性/不确定性区分。

## 定位与知识库关联

### 1. 与现有方法的根本差异

现有线性非高斯潜变量因果发现方法普遍依赖强结构假设，这些假设从根本上限制了其适用范围。**PO-LiNGAM**（Jin et al., 2024）要求潜变量遵循纯测量模型（pure measurement model），即潜变量仅通过其子观测变量间接被测量，且模型通常假设无环。**LaHiCaSl**（Xie et al., 2024）则依赖层次化的潜变量结构，并利用GIN（Generalized Independent Noise）条件进行因果方向识别。这些方法在结构假设成立时表现良好，但一旦面对任意的潜变量间因果结构或循环，就会因模型误设而失效——Table 5的实验证据表明，在任意潜变量模型下，这些方法倾向于产生过度稀疏的图，并错误识别超过一半的边。

本文的核心突破在于**完全放弃结构假设**。glvLiNG方法允许潜变量之间、潜变量与观测变量之间存在任意的因果结构和循环，无需测量模型、层次结构或三角无环等前提。这一突破的关键在于引入了一个新工具——**边缘秩（edge rank）**，它补全了潜变量因果发现工具箱中长期缺失的一块：一个无需结构假设即可操作的局部图形约束。

### 2. 在等价性刻画谱系中的位置

Table 2系统性地梳理了等价性刻画工作在不同设定下的进展，本文的贡献可沿该谱系定位：

- **结构约束方法**（如Tian & Pearl, UAI 2002）：通过semi-Markov模型中的c-component等结构分解来刻画等价性，但要求无环且依赖特定结构假设。
- **代数方法**（如van Ommen & Mooij, UAI 2017）：利用线性高斯模型中协方差矩阵的代数约束刻画等价性，但同样受限于无环设定。
- **本文贡献**：首次在**含潜变量和循环**的线性非高斯模型中建立了分布等价性的图形刻画（Theorem 2），且该刻画**不依赖任何结构假设**。这一结果填补了等价性理论在一般潜变量循环模型中的空白。

从技术路径看，本文的方法论创新在于：将传统的**路径秩（path rank）**等价条件（Lemma 3）——该条件需要对所有观测变量子集进行指数级检查——通过**路径秩与边缘秩的对偶定理**（Theorem 1）转化为局部的**子代基（children bases）**匹配条件。这使得全局等价性被分解为对每个观测变量 $X_i$ 的独立局部检查（Lemma 5的局部分解），从而使得等价类的可操作遍历成为可能。

### 3. 适用边界

本方法的理论框架和算法具有明确的适用边界：

- **模型类限制**：边缘秩约束和等价性理论严格适用于线性非高斯模型。向非线性或非参数模型的推广仍是开放问题。
- **数据预处理依赖**：glvLiNG算法依赖过完备独立成分分析（OICA）来估计混合矩阵 $\tilde{A}$。OICA的精度受样本量和实际非高斯性程度影响，在小样本或弱非高斯场景下可能成为性能瓶颈。在稀疏图中，OICA估计误差可能导致glvLiNG逊于利用结构假设的基线方法（如PO-LiNGAM）；而在稠密图中，glvLiNG因其无结构假设的优势表现更优。
- **潜变量数量需预设**：尽管理论上潜变量数量可识别，实践中仍需预先指定 $\ell$，并通过验证集选择最优值。
- **等价类规模**：在最坏情况下，等价类可能包含指数级数量的图（Table 3提供了小规模图的统计数据），实际应用中对大规模图的遍历可能需要结合稀疏性或先验约束。

### 4. 局限与开放问题

**已识别的局限**：

1. **OICA依赖**：当前算法管线以OICA估计为起点，尚未实现直接在数据上估计边缘秩并构建等价类的端到端方法。
2. **表示完备性**：当前的等价类表示（solid/dashed边，Theorem 4）虽简洁，但无法编码某些更精细的代数约束（如hyperedge或mDAG结构），表示的完备性仍有提升空间。
3. **线性非高斯假设**：理论框架尚未推广到线性高斯系统或非线性设定。

**开放问题**：

1. **秩基因果发现**：能否设计无需OICA预处理的算法，直接在数据上估计边缘秩并构建等价类？
2. **统一线性模型**：边缘秩约束及对偶理论能否推广到线性高斯系统，从而统一两类模型的等价性刻画？
3. **非线性推广**：在非线性/非参数设定下，如何可靠地检验和利用秩约束（或更广义的约束）进行潜变量因果发现？
4. **表示增强**：能否在等价类表示中融入类似Meek规则的额外约束，以进一步压缩表示的冗余并增强可解释性？
5. **干预扩展**：如何将本框架扩展到干预分布等价类和参数的可识别性，从而指导实验设计？

## 原文 PDF

![[paperPDFs/ICLR_2026/Distributional_Equivalence_in_Linear_Non_Gaussian_Latent_Variable_Cyclic_Causal_Models_Characterization_and_Learning.pdf]]
