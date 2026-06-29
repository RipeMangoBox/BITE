---
title: Robust Containment Queries Over Collections of Rational Parametric Curves via Generalized Winding Numbers
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Robust_Containment_Queries_Over_Collections_of_Rational_Parametric_Curves_via_Generalized_Winding_Numbers.pdf
project_link: null
code_link: "https://github.com/llnl/axom"
aliases:
- GWNCGAPA
- RCQOCRPCGWN
tags:
- SIGGRAPH_2024
- topic/graphics_geometry_processing
- topic/benchmarks_datasets_evaluation
core_operator: 独立计算每条曲线的广义绕数，利用曲线的线性闭合将广义绕数分解为整数绕数（闭合形状）减去闭合线的绕数；通过自适应构造保持绕数不变的分段线性逼近（折线），仅需几何判断而无需数值积分或求交位置。
primary_logic: 对于任意有理贝塞尔曲线，将其与连接端点的直线闭合。当查询点距离曲线足够远时，曲线可替换为反方向的闭合线（绕数等价于该线段）；否则通过递归二分直到凸包性质保证控制多边形足够简单，此时折线绕数与原始曲线绕数相同，可精确计算广义绕数。
claims:
- 直接对曲线绕数积分使用高斯求积在曲线附近不稳定，产生不可接受的误差（Fig. 6）。
- 所提自适应算法比射线投射基线需要更少的曲线求值次数，最多8次，大多数仅需1-2次（Fig. 15）。
- 自适应折线逼近对任意靠近曲线的点实现完美分类保真度，而固定线性化即使在高细分水平仍存在大量误分类（Fig. 14）。
- 将广义绕数四舍五入到最接近的整数可产生符合设计者直觉的鲁棒包含分类，尽管几何体非水密（Fig. 12）。
---

# Robust Containment Queries Over Collections of Rational Parametric Curves via Generalized Winding Numbers

> [!tip] 核心洞察
> 对于任意有理贝塞尔曲线，将其与连接端点的直线闭合。当查询点距离曲线足够远时，曲线可替换为反方向的闭合线（绕数等价于该线段）；否则通过递归二分直到凸包性质保证控制多边形足够简单，此时折线绕数与原始曲线绕数相同，可精确计算广义绕数。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于广义绕数的有理参数曲线集合鲁棒包含查询 |
| 英文题名 | Robust Containment Queries Over Collections of Rational Parametric Curves via Generalized Winding Numbers |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2403.17371) · [Code](https://github.com/llnl/axom) |
| Topic | #topic/graphics_geometry_processing #topic/benchmarks_datasets_evaluation |
| Method | Generalized Winding Number for Curved Geometry via Adaptive Polyline Approximation |
| Dataset | 非水密非流形形状（自适应 vs 固定线性化） |

> [!tip] 效果简介
> - 自定义非水密形状（如含删除曲线的形状） 上，包含分类正确性（定性） 广义绕数场平滑退化，四舍五入后正确分类 vs 射线投射产生大量误分类 (消除误分类)。
> - 水密模型（用于性能对比） 上，达到完全几何精度所需的曲线求值次数（远离包围盒的点不计） 最多8次，大部分1-2次 vs 几何二分搜索：许多点>15次；贝塞尔裁剪：稍好但仍多于所提方法 (显著减少求值次数)。
> - 非水密非流形形状（自适应 vs 固定线性化） 上，误分类点数 / 总时间 0误分类，运行时间可接受 vs 高细分水平下仍存在大量误分类（图14中数百个） (完美保真度 vs 不可接受的误分类)。

## 概要

CAD模型中普遍存在非水密、非流形间隙与重叠等几何缺陷，传统包含查询方法（如射线投射）对此极为敏感，微小误差即可导致大规模分类错误。本文提出一种基于广义绕数的鲁棒包含查询框架，将广义绕数理论从分段线性形状推广至有理参数曲线集合。核心思路是：独立计算每条曲线的广义绕数贡献，利用曲线的线性闭合将广义绕数分解为闭合形状的整数绕数与闭合线绕数之差；通过自适应构造保持绕数不变的分段线性逼近（折线），仅需几何判断而无需数值积分或求交位置，从而规避了高斯求积在曲线附近的不稳定性。实验表明，所提方法对非水密几何实现平滑退化的绕数场，四舍五入后产生符合设计者直觉的包含分类；相比射线投射基线，曲线求值次数显著减少（最多8次，多数仅1–2次），且自适应折线逼近实现了完美分类保真度，而固定线性化即使在高细分水平仍存在大量误分类。该方法为二维有理参数曲线集合上的包含查询提供了精确、高效且鲁棒的解决方案。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

CAD/CAM 工作流中普遍存在非水密、非流形几何体——曲线间存在微小间隙、重叠或方向不一致。这类几何错误往往肉眼不可见（Fig. 2），却使传统包含查询方法彻底失效：射线投射法要求几何体严格水密，否则射线与边界的交点计数会产生级联错误，导致大量误分类（Fig. 11）。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2403_17371/figures/002_Figure_2.jpg]]
*Figure 2: Geometric errors can be visually imperceptible, but can still cause a shape to have no topological interior*

现有广义绕数方法（Jacobson et al., 2013）虽能通过绕数场的平滑退化处理非水密几何，但其理论和实现仅适用于分段线性形状。直接推广到参数曲线面临根本性困难：对曲线绕数积分使用高斯求积在曲线附近数值不稳定，即使采用 50 个节点仍产生不可接受的误差（Fig. 6），导致包含分类在近边界区域完全不可靠。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2403_17371/figures/005_Figure_6.jpg]]
*Figure 6: (top) The absolute error (log scale) in Gaussian quadrature used to compute the generalized winding number on a cubic Bézier curve with Equation 5, evaluated with 15-, 30- and 50-nodes. (middle) Using Guassian quadrature to compute generalized winding numbers over a shape leads to unacceptable errors. (bottom) Close-up of highlighted region*

本文的核心洞察在于：**对于任意有理贝塞尔曲线，可以通过自适应构造保持绕数不变的分段线性逼近（折线），将曲线绕数计算转化为纯几何判断，完全避免数值积分和求交位置计算。** 这一洞察建立在两个关键观察之上：（1）开曲线的广义绕数等于其闭合形状的整数绕数减去闭合线的绕数；（2）只要逼近折线闭合后的整数绕数与原始闭合形状相同，其广义绕数就必然相等。

### Changed Slot 1：绕数计算方法——从数值积分到自适应折线逼近

**基线方法**直接对曲线进行高斯求积计算绕数积分，在曲线附近产生不可接受的误差。**所提方法**将曲线绕数计算替换为自适应折线逼近，利用角度求和精确计算绕数，无需任何数值积分。

核心机制分为三层：

**第一层：绕数分解与闭合。** 对于任意开曲线 $\Gamma$ 和查询点 $q$，引入连接曲线两端点的直线段 $C$ 作为闭合线。根据绕数的可加性：

$$w_{\Gamma}(q) + w_{C}(q) = w_{\Gamma \cup C}(q) \in \mathbb{Z}$$

其中 $w_{\Gamma \cup C}(q)$ 是闭合形状的整数绕数，$w_C(q)$ 是直线段的绕数（可直接解析计算）。因此，计算开曲线的广义绕数等价于计算闭合形状的整数绕数并减去闭合线的贡献（Fig. 7）。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2403_17371/figures/007_Figure_7.jpg]]
*Figure 7: The unknown winding number with respect to a curved shape (left) can be computed by finding the integer winding number of the closed figure (center) and subtracting away the contribution of its closure (right)*

**第二层：远点快速判定。** 若查询点位于曲线的包围盒之外，则该点必然位于闭合形状 $\Gamma \cup C$ 的外部，其整数绕数为零。此时可直接将曲线替换为反向闭合线 $-C$，绕数计算退化为单条线段的绕数（Algorithm 1 中的远点检查）。若查询点位于凸包之外但可能在包围盒内，同样可保证其在闭合形状外部，采用相同替换策略（Fig. 9a）。

**第三层：自适应二分与折线构造（Algorithm 2）。** 当查询点靠近曲线时，递归二分曲线并检查控制多边形的几何性质。对于有理贝塞尔曲线，其控制多边形提供了曲线的凸包边界。当某子曲线的控制多边形满足“简单且凸”的条件时，该子曲线闭合后的整数绕数与其控制多边形闭合后的整数绕数相同。此时可用控制多边形作为逼近折线 $\widetilde{\Gamma}$，满足：

$$w_{\Gamma \cup C}(q) = w_{\widetilde{\Gamma} \cup C}(q) \Rightarrow w_{\Gamma}(q) = w_{\widetilde{\Gamma}}(q)$$

Fig. 8 说明了这一不变性原理：三条不同曲线由同一虚线闭合，在阴影区域内（所有闭合形状的外部），三条曲线产生的绕数场完全相同（仅方向可能相反）。这意味着只要保证闭合形状的整数绕数不变，折线逼近就是精确的。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2403_17371/figures/008_Figure_8.jpg]]
*Figure 8: (left) All three curves are closed by the same dashed line, and the shaded region is exterior to all three closed shapes. (right) This means that the winding number field generated by each curve (and the closure, up to orientation) is identical in the shaded region*

对于不满足条件的子曲线，继续递归二分。由于贝塞尔曲线的变差缩减性质，二分后的控制多边形会逐渐逼近曲线，最终必然满足简单凸条件。Fig. 9 展示了三次迭代过程：初始三个查询点中，一个在包围盒外直接替换为闭合线（a），一个在二分后满足条件（b），最后一个需要再次二分（c）。

### Changed Slot 2：包含查询决策规则——从交叉数到广义绕数四舍五入

**基线方法**依赖射线投射的交叉数奇偶性或整数绕数（仅适用于水密形状）。**所提方法**独立计算每条曲线的广义绕数贡献并求和，对总和四舍五入到最接近的整数后应用非零规则判定包含。

这一设计的关键优势在于**错误局部化**。由于每条曲线的绕数独立计算，单条曲线的几何缺陷（如间隙、删除、方向反转）仅影响该曲线附近的局部绕数场，而不会像射线投射那样产生全局性级联错误。Fig. 12 展示了这一性质：删除一条曲线后，广义绕数场在缺口附近平滑退化（从整数逐渐过渡），四舍五入后产生的包含分类更符合设计者直觉，而射线投射在同一区域产生大量误分类（Fig. 11）。

### Changed Slot 3：对非水密几何的处理——从无法处理到平滑退化

传统方法要求几何体严格水密，否则包含查询结果无意义。所提方法天然支持非水密、非流形曲线集合，绕数场在几何错误处平滑退化。Fig. 13 展示了故意分离相邻曲线的变形形状：广义绕数场在间隙处产生不确定性区域（绕数与最近整数的差值大于 0.25），但这些区域极为稀疏，整体分类仍然鲁棒。

### 完整推理路径与模块因果关系

整个包含查询的推理路径如下：

1. **逐曲线绕数计算（Algorithm 1）**：对曲线集合中的每条有理贝塞尔曲线 $\Gamma_i$，独立计算其对查询点 $q$ 的广义绕数贡献 $w_{\Gamma_i}(q)$。各曲线贡献求和得到总广义绕数 $w_{\Gamma}(q) = \sum_i w_{\Gamma_i}(q)$（Eq. 3）。

2. **远点过滤**：对每条曲线，首先检查 $q$ 是否在其包围盒外。若在外部，直接取闭合线的负绕数 $-w_{C_i}(q)$ 作为该曲线贡献，跳过后续自适应细分。

3. **自适应折线构造（Algorithm 2）**：对靠近曲线的查询点，递归二分曲线。每次二分后检查子曲线的控制多边形是否简单且凸。满足条件时，用控制多边形作为逼近折线，计算闭合多边形的整数绕数（使用 Hormann & Agathos 2001 的无三角函数算法）并减去闭合线绕数，得到该子曲线贡献。不满足条件则继续二分。

4. **重合点处理（Algorithm 5）**：当查询点恰好落在曲线端点上时，绕数定义需要特殊处理。通过计算非重合端点与切线向量之间的夹角来定义绕数（Fig. 10），保证边界情况的良定义性。

5. **包含决策**：将总广义绕数四舍五入到最接近的整数。若非零，则判定点在形状内部；否则在外部。

模块间的因果关系清晰：**远点过滤**减少了需要自适应细分的曲线数量（大部分查询点只需 1-2 次曲线求值，Fig. 15）；**自适应折线构造**保证了近曲线区域的几何保真度（零误分类，Fig. 14）；**逐曲线独立计算**实现了错误局部化和平滑退化；**绕数分解**将开曲线问题转化为闭合形状问题，使得整数绕数的不变性可用于指导折线逼近。

### 关键公式与变量含义

绕数分解的核心公式为：

$$w_{\Gamma}(q) = w_{\Gamma \cup C}(q) - w_C(q)$$

其中 $w_{\Gamma \cup C}(q) \in \mathbb{Z}$ 是闭合形状的整数绕数，$w_C(q) = \frac{1}{2\pi}\theta_C$ 是闭合线 $C$ 的绕数（$\theta_C$ 为 $C$ 两端点相对于 $q$ 的夹角）。折线逼近的不变性条件为：

$$w_{\Gamma \cup C}(q) = w_{\widetilde{\Gamma} \cup C}(q)$$

当控制多边形 $\widetilde{\Gamma}$ 满足简单凸条件时，该等式自动成立，从而保证 $w_{\Gamma}(q) = w_{\widetilde{\Gamma}}(q)$。这一条件将连续曲线的绕数计算转化为离散多边形的整数绕数计算，完全避免了数值积分的不稳定性。

## 实验与关键发现

### 核心实验设计

实验围绕三个关键维度展开：**几何保真度**（包含分类正确性）、**计算效率**（曲线求值次数）和**鲁棒性**（对非水密几何的容错能力）。所有方法在相同硬件上评估，使用相同的曲线求值操作计数，未利用预计算缓存。基线方法包括几何二分射线投射（Farin, 2001）、贝塞尔裁剪（Nishita et al., 1990; Sederberg and Nishita, 1990）以及固定细分水平的均匀折线逼近。

### 主结果一：非水密几何的包含分类正确性

在含有删除曲线的非水密形状上，传统射线投射产生大量误分类（Fig. 11）。当几何体缺失一条曲线时，射线投射的交叉计数规则将导致级联错误——大量本应在形状内部的点被错误分类为外部（粉色为内部，绿色为外部）。

所提方法通过独立计算每条曲线的广义绕数并求和，绕数场在几何错误附近**平滑退化**（Fig. 12 center）。将广义绕数四舍五入到最接近的整数后，产生的包含分类更符合设计者直觉，消除了射线投射的灾难性误分类（Fig. 12 right）。这一结果验证了核心设计决策：**每条曲线独立计算绕数，错误局部化而非传播**。

对于故意变形使相邻曲线轻微分离的形状，广义绕数场仍然保持良好行为（Fig. 13 top）。通过计算绕数与其四舍五入值之间的绝对差（对数尺度），可以发现分类不确定性区域（差值 > 0.25 的点）在整个域中极为稀疏地分布（Fig. 13 bottom），说明所提方法在非水密条件下仍能提供高置信度的包含判断。

### 主结果二：自适应折线逼近 vs 固定线性化的精度对比

这是最具决定性的消融实验（Fig. 14）。在非水密、非流形形状上，对 $10^5$ 个均匀随机采样点评估广义绕数，对比自适应策略与固定细分水平的均匀折线线性化。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2403_17371/figures/014_Figure_14.jpg]]
*Figure 14: Given a non-watertight, non-manifold shape, we observe the practical effect of curve linearization on geometric accuracy and runtime. We compare our adaptive strategy to those that uses a uniform, piecewise linearization of the curve at fixed levels of refinement. We record the total time spent to evaluate the generalized winding number for 105 points randomly sampled from a uniform distribution, and the number of these points which are ultimately misclassified. We see that a fixed linearization can offer better computational performance, as subdivisions of the curve can be efficiently precomputed. However, we note that even at high levels of refinement there are still a considerable number...*

| 方法 | 误分类点数 | 总运行时间 |
|------|-----------|-----------|
| 自适应折线逼近 | **0** | 可接受 |
| 固定线性化（低细分） | 大量 | 快（可预计算） |
| 固定线性化（高细分） | 仍有数百个 | 显著增加 |

关键发现：固定线性化即使在高细分水平下仍存在大量误分类，这在许多下游应用中不可接受。固定线性化可通过预计算曲线细分获得更好的计算性能，但牺牲了几何精度。自适应策略实现了**完美分类保真度**（零误分类），证明仅需几何判断而无需数值积分或精确求交位置即可保证绕数计算正确性。

### 主结果三：曲线求值效率对比

在水密模型上均匀采样 250,000 个点，测量达到完全几何精度所需的曲线求值次数（Fig. 15）。直方图省略了需要零次求值的点（查询点在曲线包围盒外，对所有方法频率相同）。

| 方法 | 曲线求值次数 |
|------|------------|
| 所提自适应方法 | 最多 **8 次**，大部分 **1-2 次** |
| 几何二分搜索 | 许多点 **> 15 次** |
| 贝塞尔裁剪 | 稍好于几何二分，但仍多于所提方法 |

性能优势的来源：所提方法将远点直接替换为闭合线段（零求值），近点通过自适应二分构建折线，仅需验证控制多边形的简单性和凸性，无需计算精确交点位置。对于高阶曲线（Fig. 16），虽然需要更多曲线细分以达到完美几何保真度，但所提算法仍保持性能优势，因为无需直接计算各交点位置。

![[assets/figures/papers/paper_list_l33_https_arxiv_org_abs_2403_17371/figures/016_Figure_16.jpg]]
*Figure 16: For higher-order curves, additional curve subdivisions are necessary to reach perfect geometric fidelity. The proposed algorithm still has superior performance in such cases, as the location of the various intersections need not be computed directly*

### 数值积分不稳定性的直接证据

直接对曲线绕数积分使用高斯求积在曲线附近产生不可接受的误差（Fig. 6）。在三次贝塞尔曲线上使用 15、30、50 节点的高斯求积计算广义绕数，绝对误差（对数尺度）在求积节点附近达到无意义的值。将高斯求积应用于整个形状的绕数计算导致不可接受的误差（Fig. 6 middle），这直接证明了数值积分路径不可行，必须采用所提的几何分解方法。

### 关键消融实验

**数值容差的影响**（Fig. 17）：Algorithm 3 中的数值容差超过一定阈值后，由于算法的自适应性质，性能对其不敏感。实践中将容差设为零可确保精确几何保真度，且仅略微增加计算负担。这一消融验证了自适应策略的鲁棒性——算法本身的结构保证了精度，而非依赖精细调参。

**曲线方向错误的影响**（Fig. 18）：在 Fig. 12 的形状中，将高亮曲线的方向反转而非删除。反转导致周围局部区域的包含分类发生交换，但错误仍局限于该曲线附近。这揭示了方法的一个边界条件：假设曲线方向基本一致；单个反向曲线不会导致全局分类崩溃，错误保持局部性——这与射线投射在几何错误时产生全局级联错误形成鲜明对比。

### 失败模式与适用边界

1. **方向不一致的累积效应**：当模型中存在大量方向不一致的曲线时，局部错误可能累积，但论文未给出定量评估，需要手动验证。
2. **三维推广的障碍**：当前方法仅适用于二维参数曲线。三维曲面广义绕数面临缺乏简单闭合原语（相当于二维中闭合线段的曲面类比）的挑战，这是方法的内在边界。
3. **远距离查询的优化空间**：算法尚未集成空间索引以加速远距离查询。当前对每个查询点遍历所有曲线检查包围盒，存在通过哈希映射缓存曲线细分结果、多线程或 GPU 并行化的优化机会（Algorithm 1 具有内在并行性）。
4. **预计算与自适应的权衡**：固定线性化可通过预计算获得更好的计算性能，但牺牲精度。自适应方法在需要完美几何保真度的场景中不可替代，但在精度要求可放松的应用中可能过度计算。

## 定位与知识库关联

本文的核心贡献在于将**广义绕数（generalized winding number）**的理论框架从分段线性几何推广到**二维有理参数曲线集合**，并配套提出了一种无需数值积分、仅依赖几何判断的自适应折线逼近算法。这一定位在知识库中的挂载点及其与已有工作的本质差异可从以下几个维度理解。

### 相对于已有方法的 slot 改变

与现有包含查询方法相比，本文改变了三个关键 slot：

1. **绕数计算方式**：已有方法对参数曲线绕数采用直接数值积分（如高斯求积），但 Fig. 6 明确显示该方法在曲线附近产生不可接受的误差，即使使用 50 个节点仍无法保证精度。本文将其替换为**自适应折线逼近 + 整数绕数精确计算**的组合：当查询点远离曲线时直接替换为闭合线段，否则递归二分直到控制多边形足够简单，此时折线绕数与原始曲线绕数等价。这一替换的因果机制在于利用了绕数在保闭合整数绕数的折线逼近下的不变性，从而绕开了数值积分的不稳定性。

2. **包含查询决策规则**：传统射线投射（ray casting）依赖交叉计数或整数绕数，要求几何体水密（watertight）。本文将其替换为**广义绕数四舍五入后应用非零规则**，且每条曲线独立计算贡献后求和。这一改变使得包含查询对非水密、非流形几何具有天然的鲁棒性——间隙和重叠不会导致级联错误，而是使绕数场平滑退化。

3. **对非水密几何的处理范式**：已有方法要么无法处理非水密几何，要么产生大规模误分类（Fig. 11 中射线投射在删除单条曲线后产生大量错误）。本文通过**逐曲线独立计算绕数**实现了错误的局部化：单条曲线的缺失或方向反转仅影响其局部区域的绕数场，而不会污染整体分类结果（Fig. 18）。

### 知识库挂载点

本文直接继承并扩展了 **Jacobson et al. (2013)** 提出的广义绕数框架。Jacobson 等人的工作建立了广义绕数在分段线性形状上的理论基础，证明了绕数场在几何错误周围的平滑退化特性，但其方法仅限于三角形网格等分段线性表示。本文的挂载点在于：将广义绕数的定义域从分段线性曲线扩展到**有理 Bézier 曲线**，并解决了这一扩展中的两个核心障碍——（1）参数曲线上绕数积分的数值不稳定性；（2）如何在保证几何保真度的前提下高效计算。

在绕数计算的技术路径上，本文继承了 **Hormann & Agathos (2001)** 的闭合多边形整数绕数算法（无需三角函数，仅通过有理运算），将其作为自适应折线逼近后的计算后端。同时，本文的闭合-分解策略（将开曲线绕数表达为闭合形状整数绕数减去闭合线绕数）与 **Barill et al. (2018)** 在三维广义绕数中的“Stokes 定理分解”思路在精神上相似，但本文在二维参数曲线场景下给出了更简洁的闭合原语（直线段）和更直接的几何判断条件。

### 适用边界

本文方法的适用边界明确：

- **几何维度**：当前仅适用于**二维参数曲线**。三维曲面（如 NURBS 曲面）的广义绕数计算面临缺乏简单闭合原语的挑战——三维中不存在类似于二维直线段那样绕数可精确计算的简单闭合形状。这是方法向三维推广的主要障碍。
- **曲线方向假设**：算法假设曲线方向基本一致。当存在方向反转的曲线时，局部包含分类会交换（Fig. 18），但错误仍保持局部性，整体鲁棒性优于射线投射。论文未提供自动检测或补偿方向错误的机制。
- **性能优化空间**：当前实现未集成空间索引（如包围盒层次结构）来加速远距离查询的快速剔除，也未利用多线程或 GPU 并行化 Algorithm 1 的内在并行性。这些是工程优化而非方法本身的限制。

### 后续启发与开放问题

本文为以下研究方向提供了出发点：

1. **三维推广**：如何将自适应折线逼近的思路推广到三维有理曲面？可能的路径包括寻找三维中的简单闭合原语（如平面多边形），或探索基于曲面边界的 Stokes 定理分解（沿 **Barill et al., 2018** 的方向但面向参数曲面）。

2. **缓存与重用**：由于自适应细分的结果仅依赖于曲线本身和查询点的相对位置关系，可以利用哈希映射缓存曲线细分结果，在大量查询点共享同一曲线集合时进一步提升性能。

3. **方向一致性检测**：当模型中存在大量方向不一致的曲线时，能否通过分析绕数场的局部符号模式自动检测并补偿方向错误？这将进一步提升方法在实际 CAD 工作流中的鲁棒性。

4. **与等几何分析的集成**：广义绕数提供的平滑内外分类场可能作为等几何分析（IGA）中施加边界条件的软约束，尤其适用于包含微小间隙或重叠的 CAD 装配体模型。

### 与基线的本质差异总结

与 **Geometric Bisection Ray Casting**（Farin, 2001）和 **Bézier Clipping**（Nishita et al., 1990; Sederberg and Nishita, 1990）相比，本文方法的本质差异不在于计算效率的常数倍提升，而在于**问题建模层面的根本转变**：将包含查询从“判断点是否在闭合形状内部”重新定义为“计算广义绕数场并四舍五入”。这一转变使方法对几何错误的响应从“灾难性失败”变为“平滑退化”，而自适应折线逼近则是使这一理论框架在参数曲线上可高效实现的关键技术手段。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Robust_Containment_Queries_Over_Collections_of_Rational_Parametric_Curves_via_Generalized_Winding_Numbers.pdf]]