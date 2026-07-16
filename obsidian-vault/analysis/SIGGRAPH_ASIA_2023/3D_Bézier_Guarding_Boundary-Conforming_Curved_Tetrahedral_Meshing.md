---
title: "3D Bézier Guarding: Boundary-Conforming Curved Tetrahedral Meshing"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2023/3D_B_zier_Guarding_Boundary_Conforming_Curved_Tetrahedral_Meshing.pdf
project_link: null
code_link: null
aliases:
- 3BZG
- 3BZGBCCTM
tags:
- SIGGRAPH_ASIA_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用先验（a priori）的Bézier守护策略，通过定义并检测正交可保卫性（guardability）条件，在必要时递归细分面片，直接构造贴合输入曲面的正则面元和边元，从而将剩余空间转化为纯平面边界，将问题降维为经典线性网格生成。
primary_logic: 核心洞察在于通过分层构造（面元覆盖曲面片、边元填充边间隙）将复杂的曲面边界完全封装，使得暴露的边界变为平面。这样，高阶曲面网格生成问题被系统性地简化为一个已知可解的线性网格问题，同时通过构造数学保证所有元素的正则性和不相交性。
claims:
- 算法在所有随机化数据集和示例模型上成功生成了所有所需的面元和边元，且这些元素均被验证为正则和无相交。
- 利用精确有理算术实施所有谓词和中间构造，完全避免了浮点精度导致的收敛性证明失效。
- 递归细分过程能被证明终止：通过构造使面元高度与子三角形边长成正比，随着细分逐步收敛，最终每个子面片均可守护。
- Set A (随机生成中度曲面) 上 曲面元素生成成功率 = 100%
---

# 3D Bézier Guarding: Boundary-Conforming Curved Tetrahedral Meshing

> [!tip] 核心洞察
> 核心洞察在于通过分层构造（面元覆盖曲面片、边元填充边间隙）将复杂的曲面边界完全封装，使得暴露的边界变为平面。这样，高阶曲面网格生成问题被系统性地简化为一个已知可解的线性网格问题，同时通过构造数学保证所有元素的正则性和不相交性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 3D Bézier 守护：边界贴合曲面四面体网格生成 |
| 英文题名 | 3D Bézier Guarding: Boundary-Conforming Curved Tetrahedral Meshing |
| 会议/期刊 | SIGGRAPH ASIA 2023 |
| Links | [paper](https://doi.org/10.1145/3618332) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 3D Bézier Guarding |
| Dataset | Set A, Set B, Set C, Set D |

> [!tip] 效果简介
> - Set A（单个随机多项式曲面片）上，曲面元素生成成功率为 100%，整体流程成功率（含直线网格）为 99.5%。
> - Set B（10 个随机曲面片）上，曲面元素生成成功率为 100%，整体流程成功率为 92%。
> - 论文没有可直接量化对比的既有方法；核心证据是构造所得曲面元素在全部测试实例中均保持正则且无相交。

## 概要

现有三维高阶四面体网格生成方法几乎都采用后验变形策略：先生成线性网格，再通过优化或投影使元素曲面贴合边界。这一范式存在根本性瓶颈——正则性（无退化、无反转）与边界精确贴合往往不可兼得。本文提出 **3D Bézier 守护**（3D Bézier Guarding），一种先验构造方法：直接从输入的多项式曲面出发，通过构造数学保证生成的高阶 Bézier 四面体既严格贴合边界，又绝对无反转。

核心思路是将复杂曲面边界分层封装：首先在每个可守护的曲面三角面片上构造一个底面贴合曲面、其余面为平面的正则“面元”；继而在相邻面元之间的边隙中填入“边元”，使暴露边界全部变为平面；剩余空间退化为经典线性多面体网格问题，可由标准工具填充。整个构造过程由正交可保卫性条件驱动自适应细分，并以精确有理算术实现所有谓词，确保收敛性和正确性。

在四组随机化数据集和多个示例模型上，曲面元素生成成功率达 **100%**，且所有面元与边元均被验证为正则、无相交。整体流程成功率在中等曲率场景下为 99.5%，极端高曲率场景下约 70%（失败源于第三方直网格工具的浮点精度限制，非本方法缺陷）。方法支持任意多项式阶数，为高阶仿真提供了可证明正确的曲面网格生成基础。

## 核心方法与创新机理

### 问题瓶颈与范式转换

现有三维高阶四面体网格生成方法几乎全部采用**后验变形（a posteriori curving）**范式：先生成线性网格，再通过节点移动、投影或优化使元素贴合曲面边界。这一范式的根本困境在于，**正则性（无退化或反转）与边界精确贴合（conformance）往往不可兼得**——优化过程可能陷入无保证状态，投影操作极易导致元素反转，且现有方法通常仅支持低阶曲面（如二次），难以推广到任意多项式阶数。

本文提出的 **3D Bézier Guarding** 方法从根本上改变了这一范式，采用**先验构造（a priori construction）**策略：直接在曲面状态下生成四面体，通过构造数学保证每一个元素既正则又精确贴合边界。这一范式转换构成了方法的核心创新。

### 核心洞察：分层封装与降维

方法的核心洞察在于**通过分层构造将复杂的曲面边界完全封装，使暴露的剩余边界变为纯平面**，从而将高阶曲面网格生成问题系统性地降维为经典线性网格生成问题。具体而言：

- **面元（Face Elements）**：在每个输入曲面三角形上直接构造一个正则 Bézier 四面体，其底面精确贴合曲面片，其余控制点位于由曲面几何导出的“共同守卫区域”内。
- **边元（Edge Elements）**：在相邻面元之间的边隙中构造第二类四面体（半曲面半平面），填满曲面边周围的空隙，并保证暴露面为平面。
- **直元（Straight Elements）**：剩余的多面体区域边界已全部为平面，可直接调用标准线性约束四面体化方法（如 TetGen）填充。

这一分层策略将“在整个体积内同时处理曲面边界”这一难题，分解为三个可独立求解且数学上可保证的子问题。

### 关键技术模块与因果链路

方法由以下六个核心模块构成，模块之间存在严格的因果依赖关系：

**模块一：输入预处理与 Bézier 三角形转换**
输入为分片多项式曲面（Bézier 三角形面片或可精确转换的张量积 B-spline/NURBS 面片）。对于张量积形式的矩形 Bézier 面片，通过精确的升阶与三角剖分公式转换为 Bézier 三角形面片 $P_i$。输入面片需满足正则性、仅在边界相交、无退化角等条件。

**模块二：可守卫性检测与自适应细分**
这是方法的核心理论模块。对每个面片 $P$，检测其是否满足**正交可守卫性（Orthogonal Guardability）**条件。该条件要求存在一对正交于底面平面的平面——支撑平面与分离平面——使得面片的所有控制向量（蓝向量 $\Gamma^0$ 和红向量 $\Gamma^1$）满足特定的几何约束。若面片不可守卫，则采用红-绿细分策略递归细分，直至所有子面片均可守卫。细分终止性由构造保证：随着细分进行，面元高度与子三角形边长成正比收敛，最终每个子面片必然可守卫。

**模块三：面元构造**
对于每个正交可守卫的面片 $P$，构造一个正则 Bézier 四面体 $H$ 作为面元。其底面控制点直接取自 $P$，其余层控制点放置于**共同守卫区域** $G_P$ 内。$G_P$ 定义为所有控制点各自守卫区域 $g(p_{ij})$ 的交集：
$$G_{\mathbf{P}} = \bigcap_{ij} g(\mathbf{p}_{ij})$$
其中每个 $g(p_{ij})$ 由四个切平面（外切平面 $T_{++}$、$T_{--}$ 和内切平面 $T_{-+}$、$T_{+-}$）界定，这些切平面从蓝锥和红锥的几何关系导出。通过将高层控制点沿特定方向置于 $G_P$ 内，可构造保证 Jacobian 行列式恒正的面元。

**模块四：边元构造（内部边与边界边）**
面元构造完成后，相邻面元之间沿曲面边存在空隙。边元构造分为两种情况：对于内部边，可构造单个四面体或两个四面体组成的扇；对于边界边，需引入辅助三角形 $S$ 并施加内角约束以避免与相邻元素相交。边元的关键性质是：其暴露于剩余空间的侧面为平面面片（由蓝、红向量共面保证），从而为后续直网格生成提供纯平面边界。

**模块五：直网格生成**
剩余待填充区域的所有边界面均为平面，构成一个多面体区域。调用标准约束四面体化方法生成直四面体，并在与边元/面元的接缝处调整控制点以保持 $C^0$ 连续性。

**模块六：正则性验证**
所有构造的面元和边元需通过严格的 Jacobian 行列式正性验证。将行列式表达为次数 $3(n-1)$ 的 Bernstein 多项式：
$$\operatorname{det}(J_{\mathrm{H}}) = \sum_{i+j+k \leq \hat{n}} d_{ijk} B_{ijk}^{\hat{n}}(u,v,w)$$
利用 Bernstein 基的凸包性质，通过系数 $d_{ijk}$ 的下界判定正性。若下界非正，则递归细分元素并重新验证，直至可严格判定正则性。

### 关键公式与变量含义

Bézier 三角形与四面体的参数化定义为方法提供了统一的数学语言：

- **Bézier 三角形**（次数 $n$）：$\mathbf{P}(u,v) = \sum_{i+j \leq n} \mathbf{P}_{ij} B_{ij}^n(u,v)$，其中 $\mathbf{P}_{ij}$ 为控制点，$B_{ij}^n$ 为三角域上的 Bernstein 多项式。
- **Bézier 四面体**（次数 $n$）：$\mathbf{H}(u,v,w) = \sum_{i+j+k \leq n} p_{ijk} B_{ijk}^n(u,v,w)$，定义在四面体参数域上。
- **控制向量**：对四面体的控制网格分层定义蓝向量 $\Gamma^0$、红向量 $\Gamma^1$、绿向量 $\Gamma^2$，分别对应参数域中三个方向的差分。Jacobian 行列式可表达为这些向量的混合积：
$$\operatorname{det}(J_{\mathrm{H}}) = n^3 \left( \left( \sum \Delta_{ijk}^0 B_{ijk}^{n-1} \right) \times \left( \sum \Delta_{ijk}^1 B_{ijk}^{n-1} \right) \right) \cdot \left( \sum \Delta_{ijk}^2 B_{ijk}^{n-1} \right)$$

### 与基线方法的关键差异

| 维度 | 后验变形方法 | 3D Bézier Guarding |
|------|-------------|-------------------|
| 构造范式 | 先生成线性网格，后变形贴合 | 直接生成曲面四面体 |
| 正则性保证 | 优化过程无保证，可能反转 | 构造数学保证 Jacobian > 0 |
| 边界贴合 | 投影或拟合，存在误差 | 精确贴合多项式边界 |
| 多项式阶数 | 通常限于低阶（二次） | 支持任意多项式阶数 |
| 数值实现 | 双精度浮点，可能失败 | 精确有理算术，避免精度问题 |

### 数值实现的关键决策

方法的所有谓词和中间构造均采用**精确有理算术**实现。这一决策并非简单的工程选择，而是保证收敛性证明有效性的理论需求：浮点舍入误差可能导致守卫区域计算错误、面元相交判定失败，从而使构造的数学保证失效。实验证实，使用精确有理算术时，所有随机化数据集上的曲面元素生成成功率为 100%，且所有元素均被验证为正则且无相交。

![[assets/figures/papers/v6_refresh_p4300/figures/008_Figure_8.jpg]]
*Figure 8: Illustration of inner edge elements construction. Top: a case where a single tetrahedron is sufficient. Bottom: a case where a fan of two tetrahedra is constructed. Note that a case of straight edge ?? is shown here for clarity; in general*

![[assets/figures/papers/v6_refresh_p4300/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our 3D Bézier Guarding approach, from input surface triangles (a) to output volume tetrahedral mesh (g). See Section 3 for an explanation. Note that here both sides of the input are treated (blue and green), whereas in Fig. 1 meshing was restricted to the interior of a closed object. For visual clarity, triangles and tetrahedra are shown slightly shrunken*

![[assets/figures/papers/v6_refresh_p4300/figures/009_Figure_9.jpg]]
*Figure 9: Top: Illustration of boundary edge elements construction. Middle: Bottom left: Control point positioning to make S conform to the boundary edge ??. Bottom right: Inner angle restriction for S, to avoid intersection with other incident elements*

![[assets/figures/papers/v6_refresh_p4300/figures/011_Figure_11.jpg]]
*Figure 11: Illustration of red-green refinement for subdivision of the input*

## 实验与关键发现

### 总体成功率与鲁棒性

该方法的核心优势在于曲面元素（面元与边元）的构造成功率。在所有随机化数据集（Set A–D）及示例模型上，算法**始终 100% 成功生成所有所需的曲面元素，且这些元素均被验证为正则（无退化或反转）**（Table 1）。这是一个定性突破：现有后验变形方法无法同时保证正则性与边界贴合，而本方法通过构造数学提供了这一保证。

![[assets/figures/papers/v6_refresh_p4300/figures/013_Table_1.jpg]]
*Table 1: Result statistics for the various randomized datasets and the example models. Reported are the numbers of input triangles and their number after subdivision, the numbers of generated face, (inner and boundary) edge, and straight elements, the run time (in exact numerics mode) to perform the construction of all face and edge elements, to adaptively subdivide the patches, to test elements for intersection, and to generate the straight mesh part. As can be seen, the algorithm always succeeds in generating all the required curved elements and they are always regular. Only the final straight mesh generation part (delegated to TetGen in our implementation) can fail in extreme scenarios (e.g. 8 in...*

整体流程的成功率则受限于最后的直线网格生成步骤。该步骤委托给第三方工具 TetGen，其浮点精度在极端场景下会导致失败：
- **Set A**（中度曲面）：整体成功率 99.5%（仅 1 例因 TetGen 失败）
- **Set B**（较高曲率）：整体成功率 92%（8 例失败）
- **Set C**（高度弯曲）：整体成功率 70%（3 例失败）
- **Set D**（光滑模板扰动）：整体成功率 100%

失败案例均发生在 TetGen 的约束四面体化阶段，而非本方法的曲面元素构造阶段。在 16 个实例中，精确有理算术构造的曲面元素在转换为浮点表示时引入了近乎退化的网格，导致 TetGen 无法保持边界完整性。这揭示了**精确算术到浮点转换的鲁棒性问题**，而非构造逻辑本身的缺陷。

### 元素质量分析

Table 2 报告了面元和边元的形状质量统计，采用 scaled Jacobian 和 mean ratio 两个指标（理想值均为 1.0，0.0 表示退化）：

![[assets/figures/papers/v6_refresh_p4300/figures/024_Table_2.jpg]]
*Table 2: Quality statistics over the face and edge elements, averaged over all output meshes of each dataset. The scaled Jacobian and mean ratio shape quality measure [Gargallo-Peiró et al. 2015a] are reported; for both the ideal value is 1.0, while 0.0 would indicate degenerate elements. Let us remark that the choice of a higher parameter value ?? would lead to higher quality; for ?? = 3 the scaled Jacobians increase by around an order of magnitude*

| 数据集 | Shape Quality (均值) | Scaled Jacobian (均值) |
|--------|---------------------:|------------------------:|
| Set A  | 0.247 | 0.037 |
| Set B  | 0.223 | 0.038 |
| Set C  | 0.201 | 0.038 |
| Set D  | 0.156 | 0.076 |

**关键发现**：元素可能高度扭曲。Set C 的 scaled Jacobian 均值仅为 0.038，且最小值为 0.000016。这意味着本方法生成的网格**不能直接视为理想的仿真网格，通常需要后处理优化**。作者明确指出，这些元素仅保证正则性（Jacobian > 0），不保证形状质量下界。

### 参数 μ 的消融效果

面元高度参数 μ 是影响网格质量的关键控制量。μ 控制面元控制点向守卫区域内部的退缩距离：μ 越大，控制点越深入守卫区域内部，远离边界约束。在 RoundedCube 模型上的对比实验（Fig. 20）显示：
- 当 μ 从 0.1 增加到 1.0 时，面元形状明显改善
- 当 μ = 3 时，scaled Jacobian 约**增大一个数量级**（Table 2 caption）

这表明通过调节 μ 可以在正则性保证与形状质量之间取得权衡。但 μ 过大可能导致面元之间或面元与边元之间的空间冲突，因此存在实际上限。

### 精确算术的必要性

所有谓词和中间构造均使用**精确有理算术**实现，这是避免构造失败和保证收敛性证明成立的关键因素。Section 6.2 明确指出："This is due to our implementation making use of exact rational arithmetic to avoid any numerical issues"。若使用双精度浮点，守卫性测试和面元控制点放置中的舍入误差可能导致：
1. 守卫性条件的误判（将可守卫面片判为不可守卫，或反之）
2. 控制点放置超出守卫区域，导致元素反转
3. 递归细分终止性证明失效

代价是运行时间显著增加：Set C 平均约 **2.3 小时**。作者指出，使用双精度控制点（仅谓词保留精确算术）可提速约 **6 倍**，但会重新引入数值风险。

### 递归细分的终止性与代价

守卫性仅是充分条件而非必要条件，这导致**过度细分**问题。不少面片实际上可以被守卫，但因不满足正交可守卫性的充分条件而被递归细分。Table 1 显示，细分后面片数量显著膨胀：
- Set A：平均 1 个输入面片细分为 116.5 个输出面片
- Set B：平均 10 个输入面片细分为 1,741.9 个输出面片
- Set C：平均 100 个输入面片细分为 18,139.2 个输出面片

细分过程本身被证明终止：随着细分进行，面元高度与子三角形边长成正比收敛，最终每个子面片均可守卫。红-绿细分策略（red-green refinement）保证了细分不会引入退化面片。

### 适用边界与失败模式

1. **仅支持多项式边界**：不能直接处理有理多项式（NURBS），需预先转换为多项式 Bézier 面片，限制了与主流工程造型系统的直接兼容性。

2. **裁剪面片的高次代价**：裁剪的张量积面片需通过 2D Bézier Guarding 进行三角剖分，最终面片次数可能极高（例如三次裁剪曲线在双三次面片上可达 18 次），实用性受限。

3. **非流形支持**：方法可处理非流形输入（Fig. 21 展示了非流形模型的剖切视图），但需满足输入面片间无零角退化等条件。

4. **直网格依赖**：剩余空间的直网格生成完全依赖 TetGen，在极端几何条件下鲁棒性有限，成为整体流程的最薄弱环节。

5. **无直接比较基线**：由于已有方法均无法同时提供正则性与贴合性保证，本文未与其他 3D 高阶四面体网格生成方法进行定量比较。实验评估本质上是**可行性验证**而非性能对比。

## 定位与知识库关联

### 改变的核心范式槽位：从“后验变形”到“先验构造”

3D Bézier Guarding 对高阶四面体网格生成领域最根本的改变，在于将**网格生成范式**从“后验变形”（a posteriori curving）切换为“先验构造”（a priori construction）。在已有方法中，标准流程是先生成线性四面体网格，再通过节点位移、投影或优化将边界贴合到曲面——这一范式在几何保真度与单元正则性之间存在根本性张力：边界贴合越精确，单元越容易发生反转或退化；而维持正则性则往往意味着牺牲边界精度。3D Bézier Guarding 通过**直接生成已处于曲面状态的四面体**，将正则性与贴合性同时纳入构造保证，从而避开了这一两难困境。这一范式切换意味着方法不再依赖于优化收敛性或启发式投影的数值稳定性，而是将正确性建立在可证明的几何条件之上。

### 知识库挂载点：Bézier 几何处理与计算几何的交叉

本工作在知识库中的核心挂载位置是 **Bézier 几何处理** 与 **计算几何网格生成** 的交叉地带。具体而言：

- **Bernstein-Bézier 表示理论**：方法深度依赖 Bézier 三角形和四面体的控制点结构，利用控制向量（蓝、红、绿向量）的凸包性质来定义“可守卫性”（guardability）条件。这一条件本质上是将控制点集合的几何关系转化为对支撑平面和分离平面的存在性判定，从而在不显式计算 Jacobian 的情况下保证构造的正则性。这是对 Bernstein 基函数保形性质的创造性利用。

- **精确几何计算**：方法在实现层面采用了精确有理算术（exact rational arithmetic），这使得所有几何谓词（如平面存在性判定、控制点位置计算）的结论具有数学严格性。这对于“先验构造”范式的可信度至关重要——如果构造过程本身依赖浮点近似，则“通过构造保证正则性”的论断将失去根基。这一选择将本工作与精确计算几何（Exact Geometric Computation）传统相连接。

- **约束网格生成**：方法的最后一步将剩余多面体区域委托给标准约束四面体化工具（如 TetGen），这暴露了本工作与经典线性网格生成之间的依赖关系。值得注意的是，这一依赖也是当前方法的主要鲁棒性瓶颈：在 Set C（高度弯曲曲面）上，约 30% 的实例因 TetGen 的浮点精度限制而整体失败，而非曲面元素构造本身失败。

### 与已有方法的本质差异

由于论文未提供直接的定量基线比较，以下差异基于方法学层面的分析：

1. **正则性保证的强度**：已有后验方法（如基于弹性变形或优化的 curving 方法）通常只能提供“优化目标”而非“正则性保证”——在极端曲面或粗网格下，优化可能收敛到无效解。3D Bézier Guarding 通过构造提供 **严格的数学保证**：所有面元和边元在构造完成时即被证明为正则（Jacobian 行列式 > 0），这一保证由精确有理算术支撑，不依赖数值收敛。

2. **多项式阶数的通用性**：方法支持**任意多项式阶数**，而非仅限于低阶（如二次或三次）。这一特性源于 guardability 条件的定义仅依赖于控制向量的几何关系，与阶数无关——只要面片可守卫，即可用同一套构造逻辑生成对应阶数的四面体。这对高阶有限元方法（如 p-FEM）具有直接价值。

3. **边界贴合的精确性**：面元底面**精确贴合**输入 Bézier 三角形面片，而非通过投影或插值近似。这意味着边界几何在网格转换过程中无信息损失，对于需要精确边界表示的应用（如流体-结构耦合界面）至关重要。

### 适用边界与限制

本方法的适用边界由以下因素界定：

- **输入必须是多项式曲面**：方法要求输入为 Bézier 三角形面片集合，不能直接处理有理多项式（NURBS）。这限制了与主流 CAD 系统的直接兼容性——NURBS 需要先经过多项式近似或升阶转换才能输入。论文指出裁剪张量积面片可通过 2D Bézier Guarding 间接三角剖分，但会导致面片次数显著升高（例如三次裁剪曲线在双三次面片上可达 18 次），实用性受限。

- **单元质量不保证**：虽然正则性（无反转）得到保证，但单元形状质量（scaled Jacobian, mean ratio）可能极低。Set C 的面元平均 scaled Jacobian 仅 0.038（理想值为 1.0），这意味着单元可能高度扭曲，不能直接用于仿真，必须经过后处理优化。这是“保证正则性”与“保证质量”之间的根本差距。

- **Guardability 是充分非必要条件**：算法仅当 patch 满足正交可守卫条件时才构造面元，否则递归细分。由于 guardability 是充分条件而非必要条件，许多实际上可构造正则面元的面片被不必要地细分，导致网格密度偏高。这是当前方法效率的主要瓶颈。

- **直网格步骤的外部依赖**：剩余区域的线性网格生成依赖 TetGen 等外部工具，这些工具的浮点精度问题成为整体鲁棒性的薄弱环节。论文报告了 16 个实例中因浮点转换引入的近乎退化网格导致 TetGen 失败。

### 后续启发与开放方向

本工作对后续研究提供了以下启发：

1. **质量下界的构造性引入**：当前方法仅保证正则性，不保证质量。一个直接方向是在构造规则中嵌入单元质量下界——例如通过约束 guard region 的形状或面元高度参数 μ 的自适应选择，使得面元和边元在构造时即满足最低质量阈值，减少后处理负担。论文的消融实验已表明 μ 对质量有显著影响（μ = 3 时 scaled Jacobian 约增大一个数量级），但当前 μ 为全局固定参数。

2. **更紧的可构造性条件**：寻找比正交可守卫性更紧的充分条件（甚至充要条件），以减少冗余细分和最终网格密度。这可能涉及对控制向量集合的更精细几何分析，或引入局部自适应而非全局统一的守卫区域。

3. **直网格步骤的先验化**：当前方法在曲面元素构造完成后，将剩余问题降维为经典线性网格生成。能否将直网格生成也纳入先验构造框架，从而消除对外部网格器的依赖并进一步提高鲁棒性？这将使整个流程获得端到端的数学保证。

4. **向有理多项式的推广**：将方法从 Bézier 四面体推广到有理 Bézier 四面体，从而原生支持 NURBS 输入，是连接本方法与工业造型流程的关键一步。这需要重新审视 guardability 条件在有理控制点（带权）下的几何意义。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2023/3D_B_zier_Guarding_Boundary_Conforming_Curved_Tetrahedral_Meshing.pdf]]
