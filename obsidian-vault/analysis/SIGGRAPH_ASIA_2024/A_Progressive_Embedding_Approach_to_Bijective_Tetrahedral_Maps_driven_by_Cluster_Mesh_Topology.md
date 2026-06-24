---
title: A Progressive Embedding Approach to Bijective Tetrahedral Maps driven by Cluster Mesh Topology
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/A_Progressive_Embedding_Approach_to_Bijective_Tetrahedral_Maps_driven_by_Cluster_Mesh_Topology.pdf
project_link: "https://www.algohex.eu/publications/cluster-mesh-sae"
code_link: "https://www.algohex.eu/publications/cluster-mesh-sae"
aliases:
- CMEC
- PEABTMDBCMT
tags:
- SIGGRAPH_ASIA_2024
- topic/representation_self_supervised_transfer
core_operator: 簇网格(cluster mesh)中未扩展链接(Lk^•)的拓扑性质——具体而言，其第0贝蒂数b₀(Lk^•)=1且欧拉示性数χ(Lk^•)=1——直接决定了对应顶点的可扩展性，而无需依赖扩展锥的几何分析。
primary_logic: 簇网格的局部连接信息已包含确定可行扩展序列所需的全部拓扑信息：对于可壳化(shellable)的四面体网格，总能仅通过检查未扩展链接是否单连通(即b₀=1且χ=1)来贪心地找到可行的扩展序列，从而消除了原始SaE方法中对扩展锥的昂贵分析和对所有2ⁿ子集组合探索的需求。
claims:
- 命题1-3及推论1证明：顶点的未扩展链接单连通当且仅当其扩展锥基底单连通，因此可仅通过簇网格的局部拓扑判定可扩展性
- CM在6小时内的成功率为95.8%，相比原始SaE的76.3%有显著提升，且运行时间约为SaE的一半，网格增长率显著降低
- CM算法对可壳化网格具有理论完备性保证，仅在遇到NOBUENOSS(罕见病理情况)时可能失败
- Nigolian et al. 2023数据集(2846个网格) 上 6小时内成功率 = 95.8%
---

# A Progressive Embedding Approach to Bijective Tetrahedral Maps driven by Cluster Mesh Topology

> [!tip] 核心洞察
> 簇网格的局部连接信息已包含确定可行扩展序列所需的全部拓扑信息：对于可壳化(shellable)的四面体网格，总能仅通过检查未扩展链接是否单连通(即b₀=1且χ=1)来贪心地找到可行的扩展序列，从而消除了原始SaE方法中对扩展锥的昂贵分析和对所有2ⁿ子集组合探索的需求。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于簇网格拓扑驱动的渐进嵌入双射四面体映射方法 |
| 英文题名 | A Progressive Embedding Approach to Bijective Tetrahedral Maps driven by Cluster Mesh Topology |
| 会议/期刊 | SIGGRAPH ASIA 2024 |
| Links | [paper](https://www.algohex.eu/publications/cluster-mesh-sae/) · [Code](https://www.algohex.eu/publications/cluster-mesh-sae) |
| Topic | #topic/representation_self_supervised_transfer |
| Method | Cluster Mesh Expansion (CM) |
| Dataset | Nigolian et al. 2023数据集 |

> [!tip] 效果简介
> - Nigolian et al. 2023数据集(2846个网格) 上，6小时内成功率 95.8% vs 76.3% (SaE) (+19.5个百分点)。
> - Nigolian et al. 2023数据集 上，每输入四面体的平均运行时间(s) 6.36×10⁻³ vs 2.31×10⁻² (SaE) (约快3.6倍)；最大网格增长率 34.2 vs 459 (SaE) (降低约13.4倍)。
> - 子集数据集(与FOL对比) 上，6小时内成功率 99.5% vs 99.4% (FOL) (+0.1个百分点)。

## 概要

本文针对球拓扑四面体网格到星形边界约束的双射映射问题，提出**簇网格扩展（Cluster Mesh Expansion, CM）**方法。该方法改进自Nigolian等人2023年的Shrink-and-Expand（SaE）框架，核心洞察在于：**簇网格中未扩展链接的局部拓扑**——具体而言，其第0贝蒂数 $b_0=1$ 且欧拉示性数 $\chi=1$——**即可判定顶点的可扩展性**，无需依赖扩展锥的昂贵几何分析。CM引入膨胀操作以扩大可扩展候选顶点范围，并辅以即时精度截断和Chebyshev中心优化。在2846个网格数据集上，CM将6小时内成功率从SaE的76.3%提升至**95.8%**，平均运行时间加快约3.6倍，最大网格增长率降低约13.4倍。该方法为可壳化网格提供理论完备性保证，可作为六面体网格生成等应用中的映射组件。

## 核心方法与创新机理

### 问题背景：Shrink-and-Expand 框架的瓶颈

本文改进的基线方法是 **Shrink-and-Expand (SaE)**（Nigolian et al., ACM Trans. Graph. 2023），其核心思想分两步：首先将所有内部顶点收缩至同一焦点，形成几何退化的初始构型（Shrink）；然后依次将顶点从退化簇中分离，移动至非退化位置，逐步扩展其入射四面体（Expand），全程保证不产生反转或新的退化。

原始 SaE 的根本瓶颈在于**可扩展性判定依赖于扩展锥的几何分析**，而非纯拓扑信息。具体而言，SaE 需要：
1. 检查扩展锥基底是否具有圆盘拓扑（ball-topology）；
2. 当扩展锥非星形时，执行**星形化（star-shapification）**操作——通过反复分裂边使非星形区域适应某个星形子区域。

星形化是导致网格细化和数值精度膨胀的主要根源：每次分裂都产生新增顶点，网格规模随扩展过程持续增长。此外，当单个顶点不可扩展时，SaE 需枚举所有可能的子簇组合来寻找可扩展子集，其搜索复杂度为 $O(n^k)$，成为超时案例的主要耗时来源。

### 核心洞察：簇网格的拓扑判定能力

本文的关键发现是：**簇网格（cluster mesh）的局部连接信息已包含确定可行扩展序列所需的全部拓扑信息**。

簇网格 $M^\bullet$ 定义为仅由未扩展顶点构成的子网格。在扩展过程的任意时刻，顶点分为已扩展集 $V^\circ$（初始为边界顶点）和未扩展集 $V^\bullet$（初始为所有内部顶点，几何上重合于焦点）。对于任意未扩展顶点 $v$，其**未扩展链接** $\mathrm{Lk}^\bullet(v)$ 是簇网格中 $v$ 的 1 环邻域中属于 $M^\bullet$ 的部分。

核心定理（命题 1-3 及推论 1）建立了以下等价关系：
$$v \in M^{\bullet} \text{ is expandable } \Leftrightarrow b_0(\mathrm{Lk}^{\bullet}(v)) = 1 \text{ and } \chi(\mathrm{Lk}^{\bullet}(v)) = 1$$

即：**簇网格顶点 $v$ 可扩展当且仅当其未扩展链接是单连通（第 0 贝蒂数 $b_0=1$）且欧拉示性数 $\chi=1$**。这一判定准则仅依赖簇网格的局部拓扑，计算成本仅取决于输入网格的最大价数，不随扩展过程中的网格细化而增长，从根本上消除了原始 SaE 中对扩展锥的昂贵几何分析需求。

该定理的理论基础在于未扩展链接与扩展锥基底之间的内在拓扑对应关系：$v$ 的扩展锥基底单连通当且仅当 $\mathrm{Lk}^\bullet(v)$ 单连通。因此，通过检查簇网格中 $v$ 的 1 环邻域连通性，即可判定扩展的拓扑可行性，无需访问扩展锥的几何信息。

### 方法框架：Cluster Mesh Expansion (CM)

CM 方法的完整流水线包含以下模块，按执行顺序展开：

#### 1. 簇网格构建与初始化
将所有内部顶点收缩至同一焦点，形成退化簇网格 $M^\bullet$。边界顶点构成初始已扩展集 $V^\circ$，其位置由星形边界约束确定。此时所有内部四面体几何退化（边长为零），但拓扑结构完整保留。

#### 2. 可扩展性判定（Changed Slot 1）
对簇网格中每个未扩展顶点 $v$，计算其未扩展链接 $\mathrm{Lk}^\bullet(v)$ 的 $b_0$ 和 $\chi$。若满足 $b_0=1$ 且 $\chi=1$，则 $v$ 被标记为拓扑可扩展。此步骤替代了原始 SaE 中基于扩展锥几何分析的判定逻辑，是该工作的核心创新点。

#### 3. 膨胀操作（Inflation）（Changed Slot 2）
当扩展锥基底单连通但非圆盘拓扑时（即基底为带割顶点的非流形曲面），原始 SaE 无法直接扩展。CM 引入**膨胀操作**：对于扩展锥基底 $\mathrm{Lk}^\circ(v)$ 中的每个割顶点 $b$，分裂所有连接 $b$ 与未扩展顶点 $c_i \in M^\bullet$（$c_i \neq v$）的边。该操作通过引入新顶点将基底增广为圆盘拓扑，从而扩大可扩展候选顶点的范围。膨胀的触发条件完全由拓扑判定，无需几何分析。

#### 4. 星形化（Star-shapification）
当顶点拓扑可扩展但扩展锥非星形时，仍需借助原始 SaE 的星形化操作。该操作通过边分裂将非星形区域弯曲以适应某个星形子区域。CM 将其作为最后手段使用，并配合拉普拉斯平滑（仅平滑簇网格的直接已扩展邻居）以促进星形扩展锥的形成，从而减少星形化的触发频率。

#### 5. 扩展执行
对可扩展顶点 $v$，采用二分搜索策略确定其有效位置：从 $v$ 与目标域中对应点 $p_c$ 的中点出发，寻找使所有入射四面体保持正定向（无反转）的合法坐标。扩展后，$v$ 从 $V^\bullet$ 移至 $V^\circ$，簇网格相应更新。

#### 6. 子簇扩展
当单个顶点不可扩展时，CM 尝试同时扩展最多 4 个顶点的子集。子簇扩展通过枚举未扩展顶点的组合来寻找可联合扩展的子集，以此规避对星形化的需求。消融实验表明，子簇大小上限为 4 时达到性能最佳平衡点；使用更大子簇会因 $O(n^k)$ 复杂度的搜索而导致性能下降，且不再提升成功率。

#### 7. 数值精度管理（Changed Slot 3）
CM 采用**即时精度截断启发式**：在扩展过程中主动降低数值精度，避免原始 SaE 使用精确有理数（GMPQ）导致的位数膨胀问题。这一策略在保持双射性保证的同时，显著控制了内存和计算开销。

#### 8. Chebyshev 中心优化（Changed Slot 4）
作为后处理步骤，CM 迭代地将每个顶点移动至其 1 环邻域的 **Chebyshev 中心**（即包含所有邻接顶点的最小包围球的球心）。该优化在 IEEE 754 双精度下确保映射的双射性，同时改善单元质量。优化后可进一步应用对称 Dirichlet 能量进行畸变最小化。

### 模块间的因果关系

上述模块形成一条因果链：**簇网格拓扑判定**（模块 2）是核心使能器，它消除了对扩展锥几何分析的依赖，使得**膨胀操作**（模块 3）和**子簇扩展**（模块 6）成为可能——前者利用拓扑信息增广可扩展性，后者通过组合搜索规避星形化。**星形化**（模块 4）被降级为最后手段，其触发频率因前序模块而大幅降低，从而抑制了网格细化和精度膨胀。**精度管理**（模块 7）和**Chebyshev 优化**（模块 8）则分别从数值表示和几何质量两个维度保障最终结果的双射性和实用性。

### 理论完备性边界

CM 为**可壳化（shellable）四面体网格**提供理论完备性保证：对于此类网格，总能仅通过贪心地检查未扩展链接是否单连通来找到可行的扩展序列。唯一的理论失败模式是簇网格在扩展过程中退化为 **NOBUENOSS**（无边界的单连通非流形表面，欧拉示性数为 1 但不分隔空间），此时算法无法继续。然而在实际测试中，尚未遇到非壳化网格导致的失败案例。

![[assets/figures/papers/paper_list_l35_https_www_algohex_eu_publications_cluster_mesh_sae/figures/003_Figure_2.jpg]]
*Figure 2: A 2D overview of the core concept of the SaE framework that our work improves upon. (??) a ball-topology mesh with three interior vertices. (?? ) boundary vertices’ prescribed positions (blue) give a star-shaped target domain. Interior vertices are initially coincident, degenerating some of the elements. In (?? ) and (?? ) interior vertices are sequentially detached to positions yielding non-degenerate elements*

![[assets/figures/papers/paper_list_l35_https_www_algohex_eu_publications_cluster_mesh_sae/figures/021_Figure_12.jpg]]
*Figure 12: Each dot of this scatter plot represents a single mesh. Blue dots are cases where a bijective map was obtained within the 6h time limit, while the red dots exceeded the time limit. Aside from the lower number of red dots, this clearly suggests that our method shows polynomial dependence on the input size on average rather than exponential dependence as the original SaE implementation. However, a significant portion of test cases still show exponential behavior, as we discuss further in Sec. 5.4*

## 实验与关键发现

### 主结果：成功率、效率与网格增长的全面提升

本文在 Nigolian et al. (2023) 提供的 2846 个球拓扑四面体网格数据集上，以 6 小时为统一时间上限，对 Cluster Mesh Expansion (CM) 与原始 Shrink-and-Expand (SaE) 进行了系统对比。**Table 1** 汇总了关键性能指标，其核心发现如下：

![[assets/figures/papers/paper_list_l35_https_www_algohex_eu_publications_cluster_mesh_sae/figures/019_Table_1.jpg]]
*Table 1: The table below summarizes key metrics for our comparison with the original SaE implementation. Perhaps the most important one is the success rate, showing the percentage of meshes for which a bijective map could be obtained within the 6h time limit, in exact representation. Our algorithm here performs significantly better, even though the time limit is still exceeded for 4.2% of cases. Another important metric for practical uses is the rate at which maps can be converted to floating-point*

- **成功率**：CM 在 6 小时内成功率为 **95.8%**，相比 SaE 的 **76.3%** 提升了 **19.5 个百分点**。这意味着失败率从近四分之一降至 4.2%，大幅扩展了可处理网格的范围。
- **运行效率**：CM 的每输入四面体平均运行时间为 **6.36 × 10⁻³ 秒**，仅为 SaE（2.31 × 10⁻² 秒）的约 **1/3.6**。**Fig. 11** 的逐网格比率分析进一步显示，CM 在 **98%** 的案例中运行速度快于 SaE。
- **网格增长率**：CM 的最大网格增长率仅为 **34.2**，而 SaE 高达 **459**，降低了约 **13.4 倍**。在 86.6% 的案例中，CM 产生的网格细化程度更低。

![[assets/figures/papers/paper_list_l35_https_www_algohex_eu_publications_cluster_mesh_sae/figures/018_Figure_11.jpg]]
*Figure 11: We measure our performance compared to the original SaE implementation by computing the per-mesh ratio for the run time and growth ratio. CM performs significantly better in both metrics, being faster than SaE in 98% of cases and growing less in 86.6%. We note, however, that in some relatively rare cases, our implementation can be significantly slower than the original SaE*

**Table 2** 的逐网格交叉对比揭示了更细致的模式：在 SaE 成功而 CM 失败的 7 个网格中，CM 的失败源于不同的技术路径选择；而在 SaE 失败但 CM 成功的 560 个网格中，CM 展现了其拓扑驱动策略对困难案例的显著优势。

### 与 Foliation 方法的对比

为评估 CM 相对其他有理论保证方法的竞争力，本文在子集数据集上与 **Foliation maps (FOL)**（Campen et al., ACM Trans. Graph. 2016）进行了对比（**Table 3**）。由于 FOL 不适用于大规模网格且目标域类型不同，该对比使用了较小规模的网格子集。结果显示：

- 成功率相当：CM 为 **99.5%**，FOL 为 99.4%，差异仅 0.1 个百分点。
- 效率优势显著：CM 的每四面体平均运行时间为 **4.90 × 10⁻⁴ 秒**，比 FOL（1.56 × 10⁻² 秒）快约 **30 倍**。
- 网格细化程度更低：CM 所需的网格细化远少于 FOL。

**Fig. 13** 的散点图进一步揭示了两种方法随输入规模增长的趋势差异：FOL 在小规模网格上表现稳定，但当网格超过数千个四面体后变得极不实用；CM 在效率上始终占优，且对输入规模呈现多项式依赖（**Fig. 12**），而非 SaE 的指数增长趋势。

### 消融实验：子簇大小的关键作用

子簇扩展（subcluster expansion）是 CM 规避星形化操作的核心机制——当单个顶点不可扩展时，算法尝试同时扩展最多 k 个顶点的子集。**Fig. 16** 展示了子簇大小上限从 1 到 8 变化时三项关键指标的演化：

![[assets/figures/papers/paper_list_l35_https_www_algohex_eu_publications_cluster_mesh_sae/figures/027_Figure_16.jpg]]
*Figure 16: Evolution of three key performance metrics, depending on the maximum number of vertices that can be expanded at once (“subcluster”, see Sec. 4.2.5). Using larger subclusters is clearly advantageous in terms of success rate (both in exact and floating-point representation) and refinement, while not meaningfully impacting run time. We do note, however, that using subclusters of size larger than 4 actually has a negative impact on performance, while not improving success rate. This can simply be explained by the fact that exploring ??-subclusters is a component with*

- **成功率**：从单顶点扩展（k=1）的约 85% 显著提升至 k=4 时的 95.8%，但继续增大 k 不再带来成功率提升。
- **运行时间**：k=4 时达到最优平衡点；使用更大子簇（k>4）反而因 O(nᵏ) 复杂度的子簇探索导致性能下降。
- **网格增长率**：随 k 增大略有上升，但幅度有限。

该消融实验确认了 k=4 是性能与成功率的最佳折衷点，也揭示了子簇搜索的组合复杂度是算法的主要计算瓶颈之一。

### 失败模式与瓶颈分析

尽管 CM 显著提升了整体性能，但仍有 **4.2%** 的网格在 6 小时内无法完成映射。**Fig. 15** 对成功案例和超时案例的运行时间构成进行了剖析：

- **成功案例的瓶颈**：最耗时的部分通常是**子簇探索**，而非星形化操作。这说明即使对于可成功处理的网格，候选子集的枚举搜索仍是主要开销。
- **超时案例的瓶颈**：大量时间消耗在**无效的子簇搜索**上——算法反复尝试不同的顶点组合却无法找到可行扩展序列，最终耗尽时间预算。
- **星形化的残余影响**：星形化操作虽然在 CM 中被推迟为最后手段，但它仍是网格细化和数值精度膨胀的主要根源。当星形化被触发时，边分裂操作会引入大量新增顶点，导致后续扩展的几何计算成本急剧上升。

从理论角度看，CM 的完备性保证仅适用于**可壳化（shellable）**的四面体网格。对于非壳化网格，簇网格可能在扩展过程中退化为 **NOBUENOSS**（无边界的单连通非流形表面，欧拉示性数为 1 但不分隔空间），此时算法无法继续。不过，在实际测试中尚未观察到因非壳化导致的失败案例，说明该病理情况在真实数据中极为罕见。

### 数值精度与后处理优化

CM 引入了**即时精度截断启发式**（on-the-fly precision truncation）来抑制精确有理数运算中的位数膨胀问题。实验表明，该启发式在保持双射性的前提下有效控制了数值精度的增长。

后处理阶段的 **Chebyshev 中心优化**将每个顶点迭代移动至其 1 环邻域的 Chebyshev 中心，以确保在 IEEE 754 双精度下维持双射性。然而，**Fig. 17** 的畸变分布直方图揭示了一个重要限制：在 2846 个生成的双射映射中，仅约 **50%**（1430 个）可通过对称 Dirichlet 能量进行后续畸变优化，其余案例包含在双精度下 Jacobian 行列式为零或负的数值无效单元。这表明虽然 CM 在精确有理数表示下保证了双射性，但向浮点表示的转换仍可能引入数值退化。

### 适用边界总结

CM 在以下条件下展现了可靠性能：球拓扑输入网格、星形边界约束、可壳化网格结构。其核心优势——基于簇网格局部拓扑的可扩展性判定——使运行时间对输入规模呈多项式依赖，在绝大多数实际案例中避免了指数级复杂度。然而，约 4% 的顽固案例仍受困于子簇搜索的组合爆炸，且浮点精度下的畸变优化仅对约半数输出有效，这些构成了当前方法的实用边界。

![[assets/figures/papers/paper_list_l35_https_www_algohex_eu_publications_cluster_mesh_sae/figures/024_Figure_13.jpg]]
*Figure 13: Looking at the relation between mesh size and performance, it is apparent that our method performs better than the foliation method. Although FOL is more consistent in its trend, it becomes highly impractical for meshes (or star cavities) larger than a few thousand tetrahedra*

## 定位与知识库关联

本文的核心贡献在于改变了 Shrink-and-Expand（SaE）框架中**可扩展性判定的信息源**这一关键 slot：将判定依据从扩展锥（expansion cone）的几何分析替换为簇网格（cluster mesh）的局部拓扑信息。这一改变使扩展序列的可行性判定不再依赖于网格细化过程中不断膨胀的几何数据，而是仅取决于输入网格的固定组合结构，从而在理论保证和实用效率两个维度上实现了对基线方法的系统性提升。

### 相对基线的本质差异

与直接基线 **SaE**（Nigolian et al., *ACM Trans. Graph.* 2023）相比，CM 方法在以下四个 slot 上做出了实质性改变：

1. **可扩展性判定准则**（最核心的改变）：SaE 需要分析扩展锥的拓扑和星形性（star-shapedness），其计算成本随网格细化而增长，且当扩展锥基底非圆盘拓扑时直接判定为不可扩展。CM 将判定准则替换为对簇网格中未扩展链接 Lk^•(v) 的简单拓扑检查——仅需验证 $b_0(\mathrm{Lk}^{\bullet}(v)) = 1$ 且 $\chi(\mathrm{Lk}^{\bullet}(v)) = 1$，计算成本仅取决于输入网格的最大顶点价数，不随细化增长。这一替换的数学基础由命题 1–3 及推论 1 严格证明：未扩展链接单连通当且仅当扩展锥基底单连通。该准则对可壳化（shellable）四面体网格具有理论完备性保证——总能仅通过贪心策略找到可行扩展序列，从而消除了 SaE 中对所有 $2^n$ 子集进行组合探索的需求。

2. **扩展候选顶点范围**：SaE 仅在扩展锥基底为圆盘拓扑时方可扩展。CM 引入膨胀（inflation）操作，通过分裂连接割顶点的边，将基底单连通但非圆盘拓扑的扩展锥增广为可扩展状态，显著扩大了可扩展顶点的候选池。

3. **顶点最终位置优化**：SaE 无后处理优化步骤。CM 增加 Chebyshev 中心驱动的几何位置优化，迭代将每个顶点移至其 1 环邻域的 Chebyshev 中心，以确保在 IEEE 754 双精度下保持双射性。

4. **数值精度管理**：SaE 使用精确有理数（GMPQ）表示，可能导致位数膨胀。CM 采用即时精度截断启发式（on-the-fly precision truncation heuristic），在扩展过程中主动降低数值精度以控制计算开销。

与另一同类有理论保证的映射方法 **Foliation maps (FOL)**（Campen et al., *ACM Trans. Graph.* 2016）相比，CM 在可比成功率（99.5% vs 99.4%）下实现了约 30 倍的加速（每输入四面体平均运行时间 $4.90 \times 10^{-4}$ s vs $1.56 \times 10^{-2}$ s），且网格细化程度显著更低。这一差异源于 FOL 依赖全局叶状结构构造，而 CM 仅需局部拓扑信息进行贪心扩展。

### 知识库挂载点

本文在知识库中的挂载位置为：**Computer Graphics → Geometry Processing → Mesh Parameterization → Bijective Mapping → Shrink-and-Expand Framework**。具体而言，该方法可挂载于以下知识节点：

- **SaE 框架的拓扑加速变体**：作为 SaE 框架（Nigolian et al., 2023）的直接改进，CM 将扩展判定的信息源从几何域迁移到拓扑域，属于“用拓扑信息替代几何分析以加速几何算法”这一经典研究范式的成功实践。
- **壳化（shellability）理论在网格处理中的应用**：CM 的理论完备性依赖于四面体网格的壳化性质，为壳化理论在双射映射生成中的应用提供了首个系统性的算法实现。
- **局部拓扑判据用于全局映射保证**：CM 证明了仅通过检查每个顶点的 1 环邻域拓扑即可贪心地保证全局双射映射的存在性，这一“局部判全局”的范式可启发其他几何处理任务。

### 适用边界

CM 方法的理论完备性保证仅适用于**可壳化的球拓扑四面体网格**，且要求目标边界为星形（star-shaped）。对于非壳化网格，簇网格可能在扩展过程中退化为 NOBUENOSS（无边界的单连通非流形表面，欧拉示性数为 1 但不分隔空间），此时算法无法继续。不过，作者指出在实际数据集中尚未遇到非壳化网格导致的失败案例，该拓扑限制在实践中的影响极为有限。

此外，CM 仍依赖继承自 SaE 的星形化（star-shapification）操作作为最后手段，该操作是网格细化和数值精度膨胀的主要瓶颈。在困难案例中，子簇枚举搜索具有 $O(n^k)$ 的组合复杂度，是超时案例的主要耗时来源。尽管 CM 将 6 小时内失败率从 SaE 的 23.7% 降至 4.2%，仍有少量顽固案例无法在规定时间内完成。

### 后续研究启发

1. **星形化操作的改进空间**：论文明确指出，如何更好地利用星形化操作中的几何自由度（例如结合变形和选择性分裂来替代保守分裂方案），以避免细化和精度膨胀，是一个重要的开放问题。这为后续研究提供了直接的改进方向。

2. **NOBUENOSS 的直接处理方法**：当前对 NOBUENOSS 簇网格的处理仅提供了理论绕行方案（Sec. 5.1），如何直接高效地处理此类拓扑退化情况仍需探索。虽然在实际网格中极为罕见，但对某些对拓扑完备性要求严格的应用可能仍有价值。

3. **边界约束的泛化**：当前方法仅适用于星形边界约束，能否扩展至任意边界约束（如任意多边形或多面体边界）是自然的研究延伸。这需要重新审视可扩展性准则在非星形边界下的适用性。

4. **作为子模块嵌入更大系统**：如论文所述，CM 可作为 drop-in 替换用于 **Hinderink 和 Campen（2023）** 方法中的单个星形处理步骤，也可通过摩托车复形（motorcycle complex）将高亏格网格分解为球拓扑块后分别映射（Fig. 18），这为六面体网格生成等下游应用提供了更高效的参数化工具链。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/A_Progressive_Embedding_Approach_to_Bijective_Tetrahedral_Maps_driven_by_Cluster_Mesh_Topology.pdf]]