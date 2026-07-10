---
title: Computing Sparse Integer-constrained Cones for Conformal Parameterizations
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/Computing_Sparse_Integer_constrained_Cones_for_Conformal_Parameterizations.pdf
project_link: "http://staff.ustc.edu.cn/˜fuxm"
code_link: "https://github.com/QingFang1208/IntegerCone"
aliases:
- IFGMC
- CSICCCP
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 维护初始无翻转映射状态（maintenance-based）或将无翻转约束转化为有界共形畸变约束或投影到可行域，是控制翻转的关键手段。
primary_logic: 将无翻转条件与共形畸变界限联系起来，可以将难以直接处理的非凸约束松弛为更易优化的约束，同时利用屏障函数和线搜索保持迭代过程安全。
claims:
- As the inversion-free constraint concerning vertex positions is nonlinear and non-convex, eliminating the inverted simplices is difficult and non-trivial.
- If the initial mapping is not inversion-free, no method has a theoretical guarantee that the result is always inversion-free.
- Accordingly, inversion-free constraints can be converted to bounded conformal distortion constraints.
- 将无翻转条件与共形畸变界限联系起来，可以将难以直接处理的非凸约束松弛为更易优化的约束，同时利用屏障函数和线搜索保持迭代过程安全。
---

# Computing Sparse Integer-constrained Cones for Conformal Parameterizations

> [!tip] 核心洞察
> 将无翻转条件与共形畸变界限联系起来，可以将难以直接处理的非凸约束松弛为更易优化的约束，同时利用屏障函数和线搜索保持迭代过程安全。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无翻转几何映射构造：综述 |
| 英文题名 | Computing Sparse Integer-constrained Cones for Conformal Parameterizations |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://ustc-gcl-f.github.io/) · [Code](https://github.com/QingFang1208/IntegerCone) · [Project](http://staff.ustc.edu.cn/˜fuxm) |
| Topic | #topic/other_unclear |
| Method |  |
| Dataset |  |

> [!tip] 效果简介
> - If the initial mapping is not inversion-free, no method has a theoretical guarantee that the result is always inversion-free.

## 概要

计算几何映射（如参数化、变形、重网格化）常要求映射是**无翻转**的，即局部雅可比行列式处处为正。然而，无翻转约束关于顶点位置是非线性且非凸的，当初始映射包含翻转元素时，消除翻转单元极其困难，且现有方法缺乏理论保证一定能收敛到无翻转解。本文是一篇综述，系统梳理了无翻转映射构造的两类策略：**维护型方法**从无翻转初始状态出发，通过线搜索和屏障函数在迭代中保持无翻转性质；**有界畸变方法**将无翻转条件转化为有界共形畸变约束，将非凸问题松弛为更易优化的形式。综述覆盖了分段线性网格映射、无网格映射、双射映射等不同表示形式，并讨论了参数化、变形、重网格化等应用场景。主要发现是：当前方法在初始映射含翻转时普遍缺乏收敛保障，且3D双射映射计算成本高昂；有界畸变方法中畸变界限的选取仍是一个影响鲁棒性的开放问题。该综述为后续统一算法框架设计和全局收敛性研究提供了知识基础。

## 核心方法与创新机理

### 问题瓶颈：非凸无翻转约束的不可处理性

无翻转几何映射构造的核心瓶颈在于**无翻转约束的非线性与非凸性**。对于分段线性映射 $f(\pmb x) = J_i \pmb x + \pmb t_i$（定义在单纯形网格上），其逐单纯形雅可比矩阵 $\pmb J_i$ 的行列式必须保持严格正定，即 $\det J(\pmb x) > 0$。然而，当这一约束直接施加于顶点位置变量 $\pmb u$ 时，它是高度非线性且非凸的，导致从包含翻转元素的初始映射出发时，**消除翻转单纯形变得极其困难且非平凡**。更根本的是，若初始映射本身并非无翻转，现有所有方法均**缺乏理论保证**能收敛到无翻转解。这一瓶颈构成了整个领域方法设计的核心驱动力。

### 核心机制：从无翻转约束到可优化形式的松弛转化

面对上述瓶颈，该综述揭示了一条贯穿各类方法的**核心因果链路**：将难以直接处理的逐点无翻转约束，通过**等价转化**或**障碍函数松弛**，变为迭代优化过程中可安全处理的约束形式。其关键洞察在于两点：

1. **约束等价转化**：无翻转条件 $\det J_i > 0$ 可等价表达为基于雅可比矩阵元素的不等式。在二维情形下，该条件等价于 $\sqrt{a_i^2 + b_i^2} > \sqrt{c_i^2 + d_i^2}$，其中 $a_i, b_i, c_i, d_i$ 为 $\pmb J_i$ 的元素。进一步，这一不等式可被推广为**有界共形畸变约束**：
   $$\frac{k_i - 1}{k_i + 1} \sqrt{a_i^2 + b_i^2} > \sqrt{c_i^2 + d_i^2}$$
   其中 $k_i$ 为预设的共形畸变上界。这种转化将原本的非凸可行域嵌入到一个更易于优化的约束形式中，使得投影到可行域的方法成为可能。

2. **障碍函数与线搜索保护**：维护型方法（maintenance-based methods）采用**障碍能量函数**（如 AMIPS 能量）来替代硬约束。这类能量在行列式趋近于零时趋向无穷大，形成“屏障”阻止优化轨迹穿越翻转边界。具体而言，AMIPS 能量定义为：
   $$\frac{1}{d} \left( \frac{\sum_{j=1}^d \sigma_{i,j}^2}{(\prod_{j=1}^d \sigma_{i,j})^{2/d}} \right) + \frac{1}{2} \left( \prod_{j=1}^d \sigma_{i,j} + \frac{1}{\prod_{j=1}^d \sigma_{i,j}} \right)$$
   其中 $\sigma_{i,j}$ 为 $\pmb J_i$ 的奇异值。该能量线性组合了 MIPS 共形畸变项 $\frac{\sum_{j=1}^d \sigma_{i,j}^2}{d(\prod_{j=1}^d \sigma_{i,j})^{2/d}}$ 与面积畸变比率项，使得优化过程在保持局部单射性的同时，兼顾共形与面积保持。配合**回溯线搜索**（backtracking line search）控制步长，确保每一步迭代均不跨越翻转边界。

### 方法分类体系：三种策略路径

基于上述核心机制，该综述将现有方法归纳为三类策略，每类对应不同的约束处理方式：

**路径一：维护型方法（Maintenance-based）**  
从无翻转初始映射出发，通过最小化自带屏障性质的畸变能量（如 AMIPS、对称 Dirichlet 能量 $\sum_{j=1}^d (\sigma_{i,j}^2 + \sigma_{i,j}^{-2})$），配合线搜索保持迭代全程的无翻转性质。其通用框架如 Algorithm 1 所示：计算下降方向 → 线搜索确定安全步长 → 更新变量 → 检查收敛。这类方法的**关键前提**是初始映射必须无翻转，否则屏障能量在翻转区域无定义或梯度异常。

**路径二：投影型方法（Projection-based）**  
将无翻转约束转化为有界共形畸变约束或直接定义无翻转可行域，在每次迭代中将中间解**投影**回可行域。这类方法可处理翻转初始化，因为投影操作本身不依赖初始状态。但其**核心难点**在于投影算子的计算效率与精度，以及畸变界限 $k_i$ 的选择——过紧的界限可能导致可行域过小，过松则无法有效防止翻转。

**路径三：变量替换方法（Variable-substitution）**  
将优化变量从顶点位置 $\pmb u$ 替换为逐单纯形的雅可比矩阵 $\pmb J_i$，在雅可比空间直接施加无翻转约束（此时约束变为对矩阵元素的简单不等式），求解后再通过**最小二乘组装**恢复顶点位置。组装问题的形式为：
$$\min_{\widehat{\pmb v}_1, \cdots, \widehat{\pmb v}_n} \sum_{k=1}^{N_e} \left( \| \pmb J_i (\pmb v_a - \pmb v_b) - (\widehat{\pmb v}_a - \widehat{\pmb v}_b) \|_2^2 + \| \pmb J_j (\pmb v_a - \pmb v_b) - (\widehat{\pmb v}_a - \widehat{\pmb v}_b) \|_2^2 \right)$$
该方法将非线性非凸约束**解耦**为两个较易处理的子问题：在雅可比空间优化畸变能量（约束简单），以及求解线性最小二乘恢复顶点（无翻转约束）。这一策略的关键在于组装约束的满足程度直接影响最终映射质量。

### 关键公式与因果关系

上述三类方法共享一个统一的数学基础——**分段线性映射的雅可比参数化**。给定源网格的单纯形 $s_i$，其上的映射雅可比 $\pmb J_i$ 为常数矩阵，可表达为顶点位置的线性函数。这一离散化使得连续的无翻转条件 $\det J(\pmb x) > 0$ 退化为有限个单纯形上的行列式正定条件。

在能量设计层面，**比率形式的畸变度量**（如 $\prod_{j=1}^d \sigma_{i,j} + 1/\prod_{j=1}^d \sigma_{i,j}$）因其在行列式趋于零时发散的特性，天然构成障碍函数，是维护型方法的核心工具。而**基于角度的展平能量** $\sum_{s_i} \sum_{j=1}^3 \frac{1}{\omega_{i,j}} (\widehat{\alpha}_{i,j} - \alpha_{i,j}^\star)^2$ 则通过三角形内角一致性、顶点周角和为 $2\pi$、以及轮状一致性条件，间接保证无翻转性质，适用于共形参数化的特殊场景。

### 无网格变体：解耦映射与网格

除基于网格的分段线性映射外，无网格映射 $f(\pmb x) = \sum_{j=1}^m c_j B_j(\pmb x)$ 将映射表达为基函数的线性组合，其雅可比 $\pmb J_x = \sum_{j=1}^m c_j \nabla_x B_j(\pmb x)$ 是系数 $\pmb c$ 的线性函数。这一参数化**消除了网格拓扑对映射质量的限制**，使得变形结果更加光滑（如 Figure 5A 所示），但其代价是需要在连续域上采样或积分以满足无翻转约束，计算复杂度显著增加。

![[assets/figures/papers/paper_list_l10_https_ustc_gcl_f_github_io/figures/005_Figure_5A.jpg]]
*Figure 5A: 3D meshless deformation of a spherical tet mesh using Fig. 5AMIPS. Deformed meshes and their cut-views are shown. The meshless deformation generates smooth results. Reproduced with permission from Ref. [14], -c ACM 2015*

### 方法边界与未解决问题

尽管上述策略在大量应用中取得了成功，综述明确指出：**当初始映射包含翻转时，没有任何方法具备理论上的全局收敛保证**。此外，有界畸变方法中畸变界限 $k_i$ 的设置仍是一个开放问题，直接影响算法的鲁棒性与结果质量。三维双射映射的计算成本亦居高不下，缺乏高效方法。这些边界条件构成了未来研究的关键方向。

![[assets/figures/papers/paper_list_l10_https_ustc_gcl_f_github_io/figures/002_Figure.jpg]]
*Figure: Illustration for the piecewise linear mapping*

![[assets/figures/papers/paper_list_l10_https_ustc_gcl_f_github_io/figures/001_Figure.jpg]]
*Figure: Illustration for the geometric mapping f*

![[assets/figures/papers/paper_list_l10_https_ustc_gcl_f_github_io/figures/004_Figure.jpg]]
*Figure: Illustration for the symbols*

![[assets/figures/papers/paper_list_l10_https_ustc_gcl_f_github_io/figures/006_Figure.jpg]]
*Figure: Illustration for the SVD*

## 实验与关键发现

本综述并未提出新方法，而是对数十种已有无翻转映射构造方法进行了系统分类与定性比较，因此不涉及传统意义上的定量主结果表格或消融实验。其核心实验贡献在于通过统一视角揭示各类方法的性能瓶颈、适用边界与失败模式。

### 核心瓶颈：翻转初始化的理论保证缺失

综述明确指出，当前所有方法面临的最根本挑战是**当初始映射包含翻转元素时，没有任何方法能从理论上保证最终结果一定无翻转**。这一论断来自对维护型方法（maintenance-based）、投影型方法（projection-based）与有界畸变方法（bounded distortion-based）三大类方法的全面审视。维护型方法（Algorithm 1）要求从无翻转初始状态出发，通过屏障函数和线搜索保持迭代过程中的无翻转性质；一旦初始映射含有翻转，该方法便无法直接应用。投影型方法试图将翻转的中间解投影回可行域，但由于无翻转约束关于顶点位置是非线性非凸的，投影操作本身缺乏闭式解且计算代价高昂。有界畸变方法通过将无翻转约束转化为有界共形畸变约束来规避直接处理非凸性，但其有效性依赖于**畸变上界 $k_i$ 的合理设置**——这一参数选择至今仍是开放问题，设置过松则无法消除翻转，设置过紧则导致优化不收敛或结果质量下降。

### 方法间定性比较：收敛性与鲁棒性

Figure 7P 展示了四种代表性竞争方法——**CM**（复合主方向混合法）、**PP**（投影型参数化）、**AKVF**（几乎 Killing 向量场法）与 **SLIM**（可扩展局部单射映射）——在相同输入上的收敛行为比较。该图揭示了两类典型失败模式：

![[assets/figures/papers/paper_list_l10_https_ustc_gcl_f_github_io/figures/007_Figure_7P.jpg]]
*Figure 7P: Comparison for four competing methods, including CM [37], Fig. 7PP [35], AKVF [36], and SLIM [43]. Reproduced with permission from Ref. [35], -c ACM 2018*

1. **收敛速度差异显著**：基于逐顶点非线性求解的方法（如 CM）在早期迭代中能量下降较快，但后期容易陷入局部极小值；而基于重参数化与全局线性求解交替的方法（如 SLIM）通常具有更稳定的全局收敛趋势，但单步计算成本更高。
2. **翻转消除能力不均**：部分方法（如 PP）在初始映射含有严重翻转时无法有效恢复，表现为能量曲线发散或震荡；而 AKVF 通过引入矢量场正则化能在一定程度上缓解此问题，但其有效性高度依赖于输入网格的拓扑质量。

### 畸变度量的隐性权衡

综述汇总了多种畸变能量函数，包括 MIPS 能量、AMIPS 能量、对称 Dirichlet 能量等，并指出它们之间存在隐性的**共形保持 vs. 面积保持**权衡。Figure 11 展示了纯共形参数化在具有显著几何特征区域产生大面积畸变的典型案例——虽然局部角度得以保持，但面积缩放因子可跨越数个数量级，导致纹理映射或重网格化应用中的严重失真。AMIPS 能量通过线性组合 MIPS 项与面积畸变比率项来平衡这一矛盾，但其权重选择无理论指导，实际应用中需根据任务手动调节。

### 双射约束的计算成本瓶颈

当映射不仅要求无翻转、还要求全局双射（即无自交）时，问题复杂度急剧上升。Figure 8W 对比了有无双射约束的参数化结果：无双射约束时，二维参数域中的同一点可能对应曲面上的多个不同位置，导致纹理映射中出现错误。然而，综述明确指出**3D 双射映射的计算成本极高且缺乏高效方法**，这构成了当前方法在六面体网格生成（Figure 9c 的 PolyCube 流程）等应用中的主要瓶颈。在 PolyCube 全六面体重网格化流程中，第三步将六面体网格映射回输入模型时，若映射出现翻转或自交，将直接导致体网格质量不合格，而现有方法难以在可接受时间内保证大规模网格的双射性。

### 有界畸变方法的参数敏感性

有界畸变方法通过将无翻转条件松弛为有界共形畸变约束，形式上等价于：

$${ \frac { k _ { i } - 1 } { k _ { i } + 1 } } { \sqrt { a _ { i } ^ { 2 } + b _ { i } ^ { 2 } } } > { \sqrt { c _ { i } ^ { 2 } + d _ { i } ^ { 2 } } }$$

其中 $k_i$ 为逐单纯形的畸变上界。综述指出，**设置合适的 $k_i$ 值仍是一个开放问题**：过大的 $k_i$ 使约束过松，无法有效消除翻转；过小的 $k_i$ 则过度限制映射的自由度，导致优化问题不可行或结果畸变过大。这一参数敏感性使得不同有界畸变方法之间的公平比较极为困难，因为性能差异可能源自参数选择而非算法本身。

### 割缝长度与畸变质量的权衡

Figure 12 揭示了参数化中割缝长度与畸变之间的基本权衡关系：一般而言，割缝越长，参数化畸变越小。这一经验规律对闭合曲面参数化具有重要意义——追求低畸变必然导致更长的割缝，进而影响后续应用（如纹理映射中的接缝可见性）。综述未提供定量数据支撑这一关系，因此该结论需要结合具体方法进行验证。

### 适用边界总结

综合全文证据，当前无翻转映射构造方法的适用边界可归纳为：
- **初始映射无翻转**：维护型方法可稳定工作，通过屏障函数保证迭代过程安全；
- **初始映射含翻转**：需借助雅可比矩阵作为中间变量（投影型）或将约束转化为有界畸变形式（有界畸变法），但均无理论收敛保证；
- **要求全局双射**：2D 场景已有可行方案但计算成本较高，3D 场景仍缺乏高效方法；
- **对畸变有严格上界要求**：有界畸变方法可满足，但参数选择依赖经验且可能牺牲结果质量。

这些边界条件直接指向综述末尾列出的开放问题：能否为任意输入提供全局收敛的无翻转映射算法？如何降低 3D 双射映射的计算成本？这些问题至今仍是该领域的核心挑战。

## 定位与知识库关联

本综述并非提出一种新的映射构造算法，而是对“无翻转几何映射构造”这一子领域进行系统化梳理与分类。其核心学术贡献在于**将现有方法按处理翻转约束的策略划分为维护型（maintenance-based）与消除型（elimination-based）两大类**，从而揭示出该领域方法设计的根本分岔点：**初始映射是否无翻转**决定了可用的算法路径。

### 改变的Slot：翻转约束的处理范式

传统几何映射方法通常将无翻转视为一个“事后修复”问题——先允许翻转产生，再通过重网格化或局部调整消除翻转。本综述所归纳的维护型方法改变了这一范式：**将无翻转约束从“修复目标”提升为“迭代不变量”**。具体而言，维护型方法要求初始映射本身无翻转（如Tutte嵌入提供的凸组合映射），然后在每次迭代中通过屏障函数（barrier function）和线搜索（line search）确保下降步长不会引入翻转（见Algorithm 1）。这一slot的变化直接导致了**理论保证的差异**：维护型方法可以保证迭代全程无翻转，而消除型方法在初始映射含翻转时，没有任何方法能提供收敛到无翻转解的理论保证（原文明确指出的开放问题）。

### 知识库挂载点

本综述可挂载到计算几何与图形学知识库的以下节点：

1. **网格参数化（Mesh Parameterization）**：综述将无翻转参数化与有界共形畸变理论建立了等价性桥梁——无翻转约束可转化为有界共形畸变约束 $ \frac{k_i - 1}{k_i + 1}\sqrt{a_i^2 + b_i^2} > \sqrt{c_i^2 + d_i^2} $，其中 $k_i$ 为畸变上界。这一连接使得基于奇异值的畸变度量（如MIPS能量、AMIPS能量）可以直接用于构造无翻转映射，将非凸的翻转约束松弛为更易优化的凸约束。

2. **无网格变形（Meshless Deformation）**：综述覆盖了基于无网格基函数的映射表示 $f(\pmb{x}) = \sum_{j=1}^{m} c_j B_j(\pmb{x})$，其雅可比矩阵是系数 $c_j$ 的线性函数。这一表示将翻转约束从顶点位置的非线性非凸约束转化为对系数向量的约束，为3D无网格变形提供了新的优化视角。

3. **体网格生成（Volume Mesh Generation）**：PolyCube全六面体重网格化流程（Figure 9c）展示了无翻转映射在下游应用中的关键角色——将六面体网格从PolyCube域映射回输入模型时，必须保持无翻转以保证网格有效性。

### 适用边界与局限性

本综述揭示的适用边界是明确的：**维护型方法依赖无翻转的初始映射，而消除型方法缺乏理论收敛保证**。对于任意输入的全局收敛算法仍是开放问题。此外，有界畸变方法中畸变界限 $k_i$ 的设置直接影响算法鲁棒性与结果质量，但如何自动确定合适的界限值仍无系统性方案，这使得不同方法间的公平比较存在困难。3D双射映射的计算成本显著高于2D情形，目前缺乏高效方法，这限制了无翻转映射在三维体网格处理中的实际部署。

### 后续启发

综述提出的分类框架为后续研究指明了方向：能否将维护型与消除型方法统一到同一框架下（如通过调整TLC中的参数 $\alpha$）？如何降低3D双射映射的计算成本？时间序列数据上的无翻转优化算法（用于动态场景重建）是另一个待探索的开放问题。这些问题的解决将直接推动几何处理、物理仿真和计算机动画等下游应用。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/Computing_Sparse_Integer_constrained_Cones_for_Conformal_Parameterizations.pdf]]