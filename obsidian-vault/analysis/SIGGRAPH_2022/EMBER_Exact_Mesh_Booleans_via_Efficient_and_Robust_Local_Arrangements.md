---
title: "EMBER: Exact Mesh Booleans via Efficient and Robust Local Arrangements"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/EMBER_Exact_Mesh_Booleans_via_Efficient_and_Robust_Local_Arrangements.pdf
project_link: "https://graphics.rwth-aachen.de/ember-exact-mesh-booleans"
code_link: "https://github.com/gilbo/cork"
aliases:
- EMBER
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 采用固定宽度整数齐次坐标与平面基元保证精确构造与分类；通过递归自适应kd‑tree细分并传播带已知缠绕数的参考点，将全局分类问题严格局部化，彻底省去全局加速结构的构建与维护；结合多种提前终止条件与局部BSP在多边形级别高效解析交点。
primary_logic: 只要在递归细分过程中跟踪一个带有精确缠绕数向量的参考点，即可在叶节点内仅通过局部BSP和至多三段的分段追踪完成所有多边形的分类，从而将布尔运算完全转化为可高度并行、无全局依赖的局部操作。
claims:
- 在Thingi10K基准（1000对，~20k面）上几何平均仅需1.6 ms，比最快的非精确方法QuickCSG快约一个数量级，比精确方法Mesh Arrangements快数个数量级。
- 对于120万三角形示例，EMBER多线程仅用34 ms，而QuickCSG需1010 ms，Mesh Arrangements需141 s。
- 消融实验表明禁用分类快速路径和提前终止会导致运行时间显著上升，是性能的两大关键来源。
- Thingi10K (随机对，~20k面) 上 几何平均运行时间 (单次布尔运算) = 1.6 ms
---

# EMBER: Exact Mesh Booleans via Efficient and Robust Local Arrangements

> [!tip] 核心洞察
> 只要在递归细分过程中跟踪一个带有精确缠绕数向量的参考点，即可在叶节点内仅通过局部BSP和至多三段的分段追踪完成所有多边形的分类，从而将布尔运算完全转化为可高度并行、无全局依赖的局部操作。

| 字段 | 内容 |
|------|------|
| 中文题名 | EMBER：通过高效且鲁棒的局部排列实现精确网格布尔运算 |
| 英文题名 | EMBER: Exact Mesh Booleans via Efficient and Robust Local Arrangements |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://www.graphics.rwth-aachen.de/publication/03339/) · [Project](https://graphics.rwth-aachen.de/ember-exact-mesh-booleans) · [Code](https://github.com/gilbo/cork) |
| Topic | #topic/other_unclear |
| Method | EMBER |
| Dataset | Thingi10K, 1.2M三角形示例, 20×20梁相交（最坏情况）, 20个重叠立方体 |

> [!tip] 效果简介
> - Thingi10K (随机对，~20k面) 上，几何平均运行时间 (单次布尔运算) 1.6 ms vs 约20 ms (QuickCSG)，>1 s (Mesh Arrangements) (比最快非精确方法快≈12×，比精确方法快>1000×)。
> - 1.2M三角形示例 上，运行时间 34 ms (8核CPU) vs 1010 ms (QuickCSG), 141 s (Mesh Arrangements) (比QuickCSG快≈30×，比Mesh Arrangements快≈4000×)。
> - 20×20梁相交（最坏情况） 上，运行时间 4.5 ms vs 18018 ms (Mesh Arrangements), 1556 ms (浮点排列), 941 ms (CGAL 5.4) (比最快CGAL版本快≈200×)。

## 概要

传统网格布尔运算面临精确性与性能不可兼得的困境：精确方法依赖全局加速结构与任意精度算术，速度极慢；非精确方法虽快，但在共面、退化等常见配置下极易产生拓扑错误，无法用于自动化流程。EMBER 提出一种基于局部排列的精确网格布尔运算方法，核心思路是将全局分类问题严格局部化——通过自适应递归 kd‑tree 细分空间，并在细分过程中传播带有已知缠绕数向量的参考点，使得每个叶节点内的多边形分类完全独立于全局结构。所有计算采用固定宽度整数齐次坐标与平面基元，保证精确构造与分类。在 Thingi10K 基准（1000 对，约 2 万面）上，EMBER 几何平均仅需 1.6 ms，比最快的非精确方法 QuickCSG 快约一个数量级，比精确方法 Mesh Arrangements 快数个数量级；对于 120 万三角形的示例，多线程仅用 34 ms，而 QuickCSG 需 1010 ms，Mesh Arrangements 需 141 s。该方法同时支持多参数布尔操作、纹理坐标传递，并在各类退化边界条件下保持鲁棒。EMBER 以精确性为前提，实现了与非精确方法相当甚至更优的性能，为自动化几何处理流程提供了可靠且高效的布尔运算基础。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

传统网格布尔运算面临一个根本性二律背反：精确方法（如**Mesh Arrangements**，Zhou et al., TOG 2016；CGAL Nef polyhedra）依赖全局加速结构和任意精度有理算术，虽能保证拓扑正确性，但速度极慢，无法用于交互式或大规模自动化流程；非精确方法（如**QuickCSG**，Douze et al., arXiv 2017；**Cork**，Bernstein 2013）使用浮点数快速计算，却在共面、退化、重叠等常见配置下频繁产生自交、孔洞、法向翻转等拓扑错误，输出不可靠。

EMBER的核心洞察在于：**只要在递归细分过程中跟踪一个带有精确缠绕数向量（Winding Number Vector, WNV）的参考点，即可在叶节点内仅通过局部BSP和至多三段的分段追踪完成所有多边形的分类，从而将布尔运算完全转化为可高度并行、无全局依赖的局部操作。** 这一设计一举解耦了精确性与高性能，使两者不再互斥。

### 数值基底：固定宽度整数齐次坐标与平面基元

EMBER采用**Nehring-Wirxel et al.**（CAD 2021）的固定宽度整数构造，将所有几何计算建立在平面基元之上。每个平面以整数系数 $(a,b,c,d)$ 存储，表示满足 $a x + b y + c z + d = 0$ 的所有点。点由三个平面的交线定义，通过齐次坐标下的行列式计算精确构造：

$$x = \left( \,\left|\begin{array}{lll} d_p & b_p & c_p \\ d_q & b_q & c_q \\ d_r & b_r & c_r \end{array}\right|,\ \left|\begin{array}{lll} a_p & d_p & c_p \\ a_q & d_q & c_q \\ a_r & d_r & c_r \end{array}\right|,\ \left|\begin{array}{lll} a_p & b_p & d_p \\ a_q & b_q & d_q \\ a_r & b_r & d_r \end{array}\right|,\ -\left|\begin{array}{lll} a_p & b_p & c_p \\ a_q & b_q & c_q \\ a_r & b_r & c_r \end{array}\right| \right)^T$$

该构造给出4D整数齐次坐标，当第四分量非零时对应欧氏空间中的精确点。点对平面的分类通过带符号的点积实现：

$$\operatorname{classify}(x,s) = \operatorname{sign}(\langle x,s\rangle) \cdot \operatorname{sign}(x_4)$$

返回 $+1$（正侧）、$-1$（负侧）或 $0$（在平面上）。所有计算在256位整数以内完成，无需任意精度算术，同时严格保证构造与分类的精确性。这一基底是后续所有局部操作——多边形裁剪、交点解析、分段追踪——能够精确执行的先决条件。

### 缠绕数向量与布尔运算的统一框架

EMBER采用缠绕数向量（WNV）作为统一的内部/外部表示。对于 $n$ 个输入网格，空间中任意非表面点 $x$ 的WNV $\mathbf{w}^x \in \mathbb{Z}^n$ 记录该点被每个网格“缠绕”的次数：每穿过一次网格（沿法向正向）加一，反向穿过减一。WNV优雅地处理孔洞、嵌套、非流形等复杂拓扑。

每个输入多边形 $t$ 关联一个WNTV（Winding Number Transition Vector）$\Delta\mathbf{w}^t$，表示穿过该多边形时WNV的变化量。沿线段从点 $x$ 行进至 $y$，$y$ 处的WNV可通过累加所有相交多边形的带符号WNTV得到：

$$\mathbf{w}^y = \mathbf{w}^x + \sum_{t\in T} \operatorname{sign}\langle n_t, x-y\rangle \cdot \Delta\mathbf{w}^t$$

布尔运算通过指示函数将WNV映射到IN/OUT。例如并集运算：

$$f_{\mathrm{union}}(\mathbf{w}) = \begin{cases} \mathrm{IN}, & \text{if any } w_i \neq 0 \\ \mathrm{OUT}, & \text{otherwise} \end{cases}$$

输出多边形依据其前后WNV决定保留或丢弃：$(OUT, IN)$ 保留原序，$(IN, OUT)$ 反转序以保证法向正确，$(IN, IN)$ 和 $(OUT, OUT)$ 丢弃。

### Changed Slot 1：全局加速结构 → 自适应递归细分与参考点传播

传统精确方法需预先构建全局八叉树、BSP或使用光线投射进行全局分类，这一全局结构与全局依赖是性能瓶颈的核心来源。EMBER**彻底取消了全局加速结构**，代之以单次自适应递归kd-tree风格的空间细分，并在细分过程中传播带有已知WNV的参考点，使叶节点分类完全局部化。

细分过程如下：给定初始场景包围盒和已知WNV的参考点（例如场景外任意点，其WNV为零向量），在每个细分步骤中，沿点云重心处、方差最大的坐标轴方向放置轴对齐分割平面。将当前子问题的所有多边形对分割平面进行裁剪（Fig. 6），分配到两个子AABB中。若参考点落在某一侧，则另一侧通过从原参考点出发的分段追踪计算新参考点及其WNV。这一传播机制是**局部性的关键保障**——每个叶节点都拥有一个位于其AABB内的参考点及其精确WNV，后续所有分类操作无需访问任何全局信息。

![[assets/figures/papers/paper_list_l32_https_www_graphics_rwth_aachen_de_publication_03339/figures/008_Figure_6.jpg]]
*Figure 6: Clipping a convex polygon against a plane using classify is straightforward. Each vertex is classified as −1, 0, or 1. Edges from −1 to 1 are split. The result can be assembled from all non-positive vertices on the one side and all non-negative ones on the other side. Clipping requires creating 0, 1, or 2 new vertices via intersect. An example of each case is shown*

细分终止条件为叶节点内多边形数量低于阈值（通常为数十个），此时进入叶节点局部计算。

### Changed Slot 2：全局分类 → 局部BSP + 分段追踪分类

叶节点内的计算完全局部化（Fig. 5），分为三个级联步骤：

![[assets/figures/papers/paper_list_l32_https_www_graphics_rwth_aachen_de_publication_03339/figures/007_Figure_5.jpg]]
*Figure 5: The computation at the leaves of our subdivision is completely local. We start by computing pairwise intersections and build per-polygon BSPs (new edges in yellow, only intersecting polygons are opaque). Each leaf BSP polygon is then classified by tracing a segment path towards the local reference point*

**步骤一：局部BSP构建与交点解析。** 对叶节点内的每对多边形进行精确交线计算，将交集线段作为新的分割边插入各自的局部BSP树中（Fig. 7）。对于重叠多边形，通过总序（如输入索引）禁用被“较低”多边形覆盖的BSP叶子，保证重叠区域至多贡献一次（Fig. 8）。此步骤将叶内所有多边形剖分为互不相交的凸多边形片。

**步骤二：分段追踪分类。** 对每个BSP多边形，需确定其前后WNV以决定保留/丢弃。EMBER通过从叶参考点出发、追踪至多边形内部任意点的路径来累积WNV变化。由于齐次坐标下两点间无法直接构造单一线段（受限于精度边界），EMBER采用**至多三段**的路径构造策略（Fig. 9）：两点各由三个平面定义，每次仅改变一个平面即可构造一条有效线段。当路径可能超出叶AABB时，额外进行AABB裁剪（Fig. 10）。沿路径累加相交多边形的带符号WNTV，即得多边形处的WNV。

**步骤三：输出生成。** 依据前后WNV和布尔指示函数，决定每个多边形片的保留/丢弃/反转。

### Changed Slot 3：全量计算 → 多层提前终止与优化

EMBER在多个层级嵌入提前终止条件，大幅减少无效计算：

- **WNTV类型快速路径**（Fig. 11）：若输入网格各自无自交，则叶内仅含单一WNTV类型的多边形时，可跳过局部BSP构建，直接进行整体分类。
- **布尔运算符提前丢弃**（Fig. 12）：根据参考WNV、叶内多边形的WNTV类型和布尔运算符，可判定整个子空间不可能产生输出面时，直接丢弃该子问题。例如，差集运算中参考WNV为 $(0,0)$ 且叶内仅含 $(0,1)$ 类型多边形时，任何路径追踪结果均不满足差集的IN条件，该叶可整枝剪除。
- **无嵌套组件优化**：若输入无嵌套，则单一分类结果对所有包含表面有效，避免逐多边形追踪。

消融实验（Fig. 17）证实，禁用分类快速路径和禁用细分提前终止是性能下降的两大主因，验证了这些优化是EMBER高性能的关键支柱。

### 并行化架构

EMBER的递归细分天然适合并行化：每个细分步骤为纯函数，无副作用，通过任务队列和工作窃取（work-stealing）实现多线程调度（Fig. 18）。细分任务（绿色）和叶任务（红色）交错执行，在8核CPU上实现显著加速，尽管初始阶段存在“预热”效应——前几次细分任务数不足以充分利用所有核心，且内存带宽最终成为瓶颈。

### 方法边界条件

EMBER的精确性保证严格限定在输入/输出均处于固定宽度整数齐次坐标的前提下。与浮点格式互转时可能引入微小的自交或精度损失。输出为凸多边形汤（polygon soup），未三角化且包含T-交界，若下游需要规范拓扑需后处理。当前实现未利用持久化加速结构，迭代CSG场景中每步均需重建细分树。极度重叠（如20面共面）或特定提前终止失效场景下，优化效果减弱。

![[assets/figures/papers/paper_list_l32_https_www_graphics_rwth_aachen_de_publication_03339/figures/003_Figure_1.jpg]]
*Figure 1: High-level overview of our approach to mesh Booleans. Our method, łEMBERž, performs a single pass of adaptive recursive kd-tree type spatial subdivision while exploiting various early-out pruning criteria. In the leaf nodes, all faces are split into disjoint polygons by pairwise intersection using local BSP trees. These polygons are classified according to their winding numbers via segment traces. Our key contribution towards maximum efficiency is that these winding numbers can be computed locally for each leaf node since we propagate reference points with known winding numbers through the recursive subdivision. All computations are exact due to the use of a plane-based mesh representation...*

![[assets/figures/papers/paper_list_l32_https_www_graphics_rwth_aachen_de_publication_03339/figures/009_Figure_7.jpg]]
*Figure 7: Construction of the local BSPs is done via adding intersection segments. Each leaf node that contains a non-trivial part of the segment is split. The image shows a triangle with three intersection segments (red) that are added to the BSP (with existing splitting planes in green). Numbers indicate the result of classifying the segment vertices against the current BSP node plane. Note that while each intersection segment eventually lies on a green BSP splitting plane, the converse is not true: In this example, the first intersection segment causes a split that is longer than strictly necessary. This conservative splitting keeps each cell convex, leading to a simple and fast method*

![[assets/figures/papers/paper_list_l32_https_www_graphics_rwth_aachen_de_publication_03339/figures/010_Figure_8.jpg]]
*Figure 8: Top-down view of three overlapping triangles. Overlapping polygons are gracefully handled during BSP construction. Given a total order of input polygons (e.g. indices), BSP leaves are disabled if they are overlapped by a łlowerž polygon. This guarantees that overlap regions contribute to the result at most once. In this example, the current triangle ?? is cut up by two overlapping ones. However, only the light blue parts of ?? are further classified and might contribute to the result as*

![[assets/figures/papers/paper_list_l32_https_www_graphics_rwth_aachen_de_publication_03339/figures/011_Figure_9.jpg]]
*Figure 9: Given two points in homogeneous coordinates, we cannot, in general, form a segment directly between the points while staying within our precision bounds. However, for classification, we only need a path between them. Each point is defined by the intersection of three planes and by changing one plane at a time, it is always possible to construct a path between two such points with at most three segments*

## 实验与关键发现

EMBER 的实验评估围绕三个核心维度展开：与精确/非精确基线的整体性能对比、各优化模块的消融贡献，以及极端配置下的鲁棒性边界。所有实验均在同一台 8 核消费级 CPU 上执行，对比方法均使用其支持的多线程设置（若具备），以保证公平性。

### 主基准：Thingi10K 随机对

实验从 Thingi10K 数据集中随机抽取 1000 对面片数在 1000 至 100,000 之间的网格对，并施加随机刚体变换以确保重叠区域具有代表性。图 13 的直方图与几何平均线给出了核心结论：

- **EMBER 的几何平均运行时间仅为 1.6 ms**，比最快的非精确方法 **QuickCSG**（约 20 ms）快约一个数量级（≈12×），比精确方法 **Mesh Arrangements**（>1 s）快超过 1000 倍。
- 非精确方法 **Cork** 和 QuickCSG 虽然速度尚可，但在共面、退化等常见配置下频繁产生拓扑错误，无法保证输出为有效流形；而 EMBER 与 Mesh Arrangements 始终输出正确结果。
- EMBER 的性能优势在面片数增加时更为显著：对于 120 万三角形的示例（图 1），EMBER 多线程仅需 **34 ms**，QuickCSG 需 1010 ms（≈30×），Mesh Arrangements 需 141 s（≈4000×）。

这一差距的根源在于 EMBER 将全局分类问题完全局部化——无需构建全局八叉树或 BSP，也无需逐像素光线投射，仅通过递归细分中传播带已知缠绕数向量（WNV）的参考点，使叶节点内的分类成为纯局部操作。

### 迭代 CSG 场景：铣削仿真

图 14 展示了 Nehring-Wirxel et al.（CAD 2021）提出的迭代 CSG 基准，模拟钻头反复从工件中减去的铣削过程。EMBER 在整个迭代序列中保持稳定且极低的单步耗时，而精确排列方法随迭代次数增加迅速膨胀。值得注意的是，EMBER 当前实现并未利用持久化加速结构——每步均重建细分树——即便如此，其性能仍远超所有精确基线，表明局部化策略本身已大幅降低了迭代 CSG 的计算冗余。

### 极端配置与最坏情况

为探测方法边界，实验设计了两种极端挑战：

**20×20 梁相交（图 24）**：100 根梁的交点产生 100 个立方体，是典型的二次交点爆炸场景。EMBER 仅需 **4.5 ms**；Mesh Arrangements 需 18018 ms（≈4000×），浮点网格排列需 1556 ms（≈346×），CGAL 5.4 需 941 ms（≈209×）。非精确方法在此配置下输出严重损坏。

**20 个重叠立方体（图 25）**：所有立方体共享顶面和底面，形成最多 20 层共面重叠区域。尽管输入仅 240 个三角形，EMBER 仍仅需 **5.9 ms**；Mesh Arrangements 需 58280 ms（≈10000×），浮点排列需 5620 ms（≈953×）。该配置对局部 BSP 构建和重叠处理（基于总序禁用叶子，图 8）构成极限压力，EMBER 的精确整数基元与局部 BSP 策略在此展现出极强的鲁棒性。

**密集交互场景（图 22）**：约 35 万输入三角形、大量交错重叠的配置下，EMBER 仅需 43 ms，表明方法在复杂交互下仍保持高性能。

### 运行时剖分

图 16 揭示了 EMBER 各阶段的耗时分布：在大多数配置下，叶节点耗时约为细分阶段的两倍。细分本身以多边形裁剪为主导；叶节点中，分段追踪分类的代价几乎是交点计算与解析的两倍。这一定量剖分直接解释了消融实验中各优化的贡献权重。

### 消融实验

图 17 的消融研究逐一禁用了 EMBER 的关键优化，以量化其贡献：

- **禁用分类快速路径**（即从图 5 的局部 BSP 分段追踪回退到图 10 的通用三线段路径）导致总运行时间显著上升，是**最大的单一优化收益来源**。快速路径利用叶节点内 BSP 多边形与参考点的几何关系，大幅缩短了追踪路径长度。
- **禁用细分中的提前终止**（图 11、图 12）是**第二大优化贡献**。提前终止利用参考 WNV、WNTV 类型和布尔运算符指示函数，在细分阶段即丢弃不可能产生输出面的子空间，避免无效的叶节点计算。
- 两项优化叠加构成了 EMBER 性能优势的主体，验证了“局部化+提前丢弃”的设计哲学。

### 多线程可扩展性

图 18(a) 显示 EMBER 在 8 物理核上的加速比：虽然未达到完全线性（内存带宽饱和及初始“预热”阶段限制了前期并行度），但整体加速效果显著。图 18(b) 的性能剖线展示了工作窃取调度下细分任务（绿色）与叶任务（红色）的交错执行模式，验证了任务队列设计的有效性。

### 方法与边界条件

EMBER 的精确性保证建立在**输入/输出均处于固定宽度整数齐次坐标**的前提之上。与浮点数格式互转时，可能引入微小的自交或精度损失。输出为凸多边形汤（非三角化），包含 T-交界，若下游需要规范拓扑需后处理。在极度重叠（如 20 面共面）或提前终止完全失效的退化配置下，优化效果会减弱，但方法的核心局部化机制仍保证正确性。

综合来看，EMBER 在 Thingi10K 规模网格上以几何平均 1.6 ms 的速度、比最快非精确方法快约 12 倍、比精确排列快超过三个数量级的性能，确立了精确网格布尔运算的新基准。消融实验证实分类快速路径和提前终止是两大性能支柱，而极端配置测试表明方法在共面重叠、二次交点爆炸等经典难题下仍保持鲁棒且高效。

## 定位与知识库关联

### 相对已有方法的本质差异：改变的“Slot”

EMBER 在网格布尔运算这一经典问题上的核心贡献，并非提出新的数学理论，而是通过**改变“全局依赖”这一架构性 slot**，实现了精确性与高性能的首次统一。具体而言，传统精确布尔方法（如 **Mesh Arrangements**（Zhou et al., TOG 2016）、**CGAL Nef polyhedra**（Hachenberger et al., 2007））依赖预先构建的全局加速结构（全局八叉树、全局 BSP 或全局网格单元传播）来对多边形进行分类。这一全局依赖导致了两个根本性瓶颈：其一，全局结构的构建与维护本身开销巨大；其二，任意精度有理数算术在全局范围内累积的精度代价极高。

EMBER 将这一 slot 从“全局结构 + 全局分类”替换为“**自适应递归细分 + 带已知缠绕数向量的参考点传播**”。这一替换的因果机制在于：只要在递归细分过程中始终跟踪一个带有精确缠绕数向量（WNV）的参考点，那么每个叶节点的多边形分类就完全不需要访问全局信息——只需通过至多三段的分段追踪，从参考点走到多边形内部点，即可局部计算出该多边形的 WNV，进而由布尔运算符的指示函数决定其取舍。这一“全局问题局部化”的策略，使得 EMBER 能够彻底省去全局加速结构的构建与维护，同时将精确计算限制在固定宽度整数（256 位以内）的范围内，避免了任意精度算术的膨胀。

与之相比，非精确方法（如 **QuickCSG**（Douze et al., arXiv 2017）、**Cork**（Bernstein, 2013））虽然也避免了全局结构，但它们通过浮点数运算换取速度，在共面、退化等常见配置下极易产生拓扑错误。EMBER 通过固定宽度整数齐次坐标与平面基元（继承自 **Nehring-Wirxel et al., CAD 2021** 的精确构造）保证了所有计算的精确性，从而填补了“快但不准”与“准但极慢”之间的鸿沟。

另一重要差异在于**多边形分类机制**：**浮点排列方法**（Cherchi et al., TOG 2020）虽使用精确断言，但仍依赖全局网格单元传播进行分类；EMBER 则在叶节点内先通过局部 BSP 解析交点，再对每个 BSP 多边形进行分段追踪分类，使得分类操作同样完全局部化且可并行。

### 知识库挂载点

EMBER 在知识库中的挂载点可定位为：

1. **精确计算几何的工程化突破**：将平面基元与固定宽度整数齐次坐标的精确构造（Nehring-Wirxel et al., 2021 的理论框架）从概念验证推进到高性能工程系统，证明了精确计算在合理精度约束下可以比浮点近似方法更快。

2. **空间细分与局部化策略**：递归自适应 kd-tree 细分本身是经典技术，但 EMBER 的创新在于将其与“参考点 WNV 传播”耦合，使得细分不仅是空间划分工具，更是全局信息局部化的载体。这一思路可推广至其他需要全局一致分类的几何处理任务。

3. **缠绕数向量的工程应用**：缠绕数作为鲁棒的内部/外部判定工具已有悠久历史（Jacobson et al., 2013），但 EMBER 首次将其向量形式（WNV）与局部追踪、提前终止条件深度结合，使其成为高性能布尔运算的核心数据结构，而非仅仅作为理论工具。

### 适用边界

EMBER 的精确性保证严格依赖于**输入/输出均处于固定宽度整数齐次坐标范围内**。当输入网格来自浮点数格式时，转换过程可能引入微小的自交或精度损失，此时精确性不再严格成立。此外，输出为无三角化的凸多边形集合（含 T-交界），若下游管线要求规范拓扑（如流形网格），需额外后处理步骤。

在极度重叠场景（如 20 个面共面）或特定提前终止条件失效时，EMBER 的优化效果会减弱，但即便如此，其性能仍远超传统精确方法。当前实现未利用持久化加速结构，在迭代 CSG（如铣削仿真）中每步均需重建细分树，这在高步数场景下可能成为瓶颈。

### 后续启发与开放问题

EMBER 的成功揭示了几个值得探索的方向：

1. **全局信息局部化的通用范式**：参考点传播的策略是否可推广至其他需要全局一致性的几何处理任务（如全局参数化、重新网格化）？关键在于能否为这些任务定义合适的“局部可传播不变量”。

2. **并行化预热问题的解决**：EMBER 的初始细分阶段难以充分利用多核（Fig. 18），如何通过静态预分割任务或持久化加速结构消除这一“预热”效应，是进一步提升多线程利用率的关键。

3. **分段追踪的进一步压缩**：当前每个多边形均需独立分段追踪至参考点，能否通过重用相邻多边形的分类结果来减少追踪次数？这需要在不破坏局部性的前提下引入适度的局部共享。

4. **高层语义信息的利用**：针对大型 CSG 树或铣削仿真等特殊场景，能否利用操作序列的高层语义信息（如刀具扫掠体）实现更激进的提前丢弃？这需要将布尔运算从“几何层面”提升到“语义层面”进行优化。

5. **高维缠绕数向量的可扩展性**：当输入网格数量极大（缠绕数向量维度极高）时，当前方案是否仍能维持效率？是否需要压缩或分层策略来管理 WNV 的维度增长？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/EMBER_Exact_Mesh_Booleans_via_Efficient_and_Robust_Local_Arrangements.pdf]]