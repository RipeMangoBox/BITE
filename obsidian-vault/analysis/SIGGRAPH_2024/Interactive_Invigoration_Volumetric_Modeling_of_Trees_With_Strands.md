---
title: "Interactive Invigoration: Volumetric Modeling of Trees With Strands"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Interactive_Invigoration_Volumetric_Modeling_of_Trees_With_Strands.pdf
project_link: null
code_link: null
aliases:
- II
- IIVMTS
tags:
- SIGGRAPH_2024
- topic/graphics_procedural_modeling
- topic/graphics_animation_interaction
- topic/benchmarks_datasets_evaluation
core_operator: 采用固定直径的束线（strands）作为体积表示基元，结合基于活力的局部生长控制（交互式活力注入）和用户可绘制的横截面轮廓，通过位置动力学（PBD）打包束线位置，从而将二维轮廓转化为三维体积形状。
primary_logic: 将树枝的二维横截面轮廓用一组束线填充，利用树状图发育过程中束线从末梢向根部的投影与打包，实现精细的体积建模；同时允许用户通过绘制轮廓、注入活力、扭转等操作，交互式地控制树枝的侧向和纵向形态。
claims:
- "在相同骨架图上，束线方法生成的树枝形状比Li et al. [2023]的通用圆柱方法更复杂、更自然。"
- 用户绘制的分支轮廓可以控制横截面形状，实现空洞、愈合等效果。
- 交互式活力注入允许用户点击树枝注入活力，驱动局部新生长。
- 束线打包过程中PBD步数可控制分支点的分离时机，产生不同的有机形态。
---

# Interactive Invigoration: Volumetric Modeling of Trees With Strands

> [!tip] 核心洞察
> 将树枝的二维横截面轮廓用一组束线填充，利用树状图发育过程中束线从末梢向根部的投影与打包，实现精细的体积建模；同时允许用户通过绘制轮廓、注入活力、扭转等操作，交互式地控制树枝的侧向和纵向形态。

| 字段 | 内容 |
|------|------|
| 中文题名 | 交互式活力注入：基于束线的树木体积建模 |
| 英文题名 | Interactive Invigoration: Volumetric Modeling of Trees With Strands |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://storage.googleapis.com/pirk.io/projects/invigoration/index.html) |
| Topic | #topic/graphics_procedural_modeling #topic/graphics_animation_interaction #topic/benchmarks_datasets_evaluation |
| Method | Interactive Invigoration |
| Dataset |  |

> [!tip] 效果简介
> - 相同骨架图 上，视觉真实感 更复杂自然的树枝形态 vs 通用圆柱体方法（Li et al.） (定性显著提升)。

## 概要

现有树木建模方法主要依赖骨架图驱动，通过通用圆柱体生成枝干体积，难以高效表现树枝的侧向生长、空洞、愈合组织等复杂有机细节。本文提出 **Interactive Invigoration** 框架，核心思路是以固定直径的**束线（strands）** 作为体积表示基元：束线从末梢沿骨架图延伸至根部，结合基于活力的局部生长控制与用户可绘制的横截面轮廓，经位置动力学（PBD）打包束线位置，将二维轮廓转化为三维体积形状，并采用 Delaunay 三角剖分与边长阈值移除等步骤生成连续网格。方法同时提供交互式活力注入、扭转、不定芽形成等编辑操作符，允许用户实时设计树枝形态。在相同骨架图上，本方法生成的树枝形状相比 Li et al. 的通用圆柱体方法更复杂、更自然；用户绘制的分支轮廓可控制横截面形状，实现空洞、愈合等效果。该方法定位于程序化树木建模与交互式几何编辑的交叉点，以束线体积表示替代传统圆柱体网格生成，填补了侧向生长细节建模的空白。

## 核心方法与创新机理

### 问题瓶颈与核心思路

现有树木建模方法主要关注骨架图（skeletal graph）的生成，采用通用圆柱体（generalized cylinder）沿骨架路径扫掠生成网格，忽略了树枝的**侧向生长**和体积细节。这导致无法高效生成具有空洞、扭曲、愈合组织、树瘤等复杂特征的树木体积模型。真实树木的形态复杂性源于年复一年的次级生长（secondary growth）——形成层向外扩展、枝条相互挤压融合、创伤后形成愈伤组织等过程，而传统圆柱体方法将这些丰富细节简化为单一半径参数。

本文的核心洞察在于：将树枝的**二维横截面轮廓**用一组固定直径的束线（strands）填充，利用树状图发育过程中束线从末梢向根部的**投影与打包**，将二维轮廓转化为三维体积形状。束线作为体积表示基元，其空间排列自然编码了树枝的侧向形态信息，使得空洞、劈裂、愈合等复杂特征可以通过用户绘制的轮廓直接表达。

### 核心变更槽位（Changed Slots）

相比基线方法 **Li et al.（2023）** 的通用圆柱体方案，本工作引入了三个关键变更槽位：

1. **分支体积表示方法**：从通用圆柱体沿骨架图生成网格，变更为基于束线的体积表示——束线作为固定直径管道从末梢延伸到根部，通过位置动力学（PBD）打包和B样条生成几何。
2. **次级生长建模**：从仅通过骨架图节点属性定义分支粗细且无侧向细节，变更为通过束线表示侧向生长，支持用户绘制横截面轮廓来控制树枝形状。
3. **网格生成算法**：从在骨架图上直接生成圆柱体网格，变更为基于束线粒子位置的Delaunay三角剖分、边缘长度阈值去除、拉普拉斯平滑的网格生成流程。

### 管线模块与因果链条

整体管线由五个核心模块串联构成，模块之间存在严格的因果依赖关系：

**模块一：树图发育（Tree Graph Development）**
基于活力的骨架图生长模拟，采用 Li et al.（2023）提出的活力信号模型程序化生成PG（plant graph）。PG中的每个节点携带位置、半径、活力值等属性，边表示分支连接关系。该模块输出带有完整属性的骨架图，作为后续所有体积建模操作的结构基础。

**模块二：束线初始化与投影（Strand Initialization and Projection）**
在骨架图每个末端节点的局部坐标系（backplane）上初始化束线粒子。束线粒子初始放置于用户定义或默认的圆形轮廓边界内。随后，系统从末梢向根部逐层投影：对于每个分支节点，将子分支的束线粒子从其“前平面”投影到父分支的“后平面”上。投影过程中，为避免较小分支的束线与较大分支的束线重叠，需要计算位移距离：

$$d_i = D_{\mathrm{large}} + D_{\mathrm{small}}$$

其中 $D_{\mathrm{large}}$ 和 $D_{\mathrm{small}}$ 分别为较大分支和较小分支在投影方向上的最远范围。位移后的粒子位置为：

$$p_i^{\prime} = p_i + d_i \cdot \frac{\mathbf{v}}{\lVert \mathbf{v} \rVert}$$

其中 $\mathbf{v}$ 为投影方向向量。这一投影机制确保了不同分支的束线在汇合平面上空间分离，为后续打包提供合理的初始分布。

**模块三：PBD打包与轮廓拟合（PBD Packing and Profile Fitting）**
投影后的束线粒子在backplane上可能超出用户定义的轮廓边界，或分布不符合期望的横截面形状。本模块通过位置动力学（Position-Based Dynamics, PBD）迭代求解束线粒子的最终位置，核心约束包括：

- **边界约束**：若粒子 $p_i$ 在轮廓边界 $B$ 之外，则向最近边界点 $q_i$ 移动：
  $$p_i \gets p_i + \beta (q_i - p_i)$$
  其中 $\beta$ 为边界修正系数。

- **吸引子约束**：若粒子在轮廓内，则向用户定义的吸引子 $a_k$ 移动：
  $$p_i \gets p_i + \gamma_k (a_k - p_i)$$
  其中 $\gamma_k$ 为吸引子强度系数。

- **中轴约束**：粒子向轮廓中轴最近点 $m_i$ 移动：
  $$p_i \gets p_i + \delta (m_i - p_i)$$
  其中 $\delta$ 为中轴影响系数。

PBD的迭代步数直接影响分支点的分离时机：步数少时束线在分支点早期分离，步数多时束线保持聚合更久才分离，产生不同的有机形态（Fig. 14c-f）。这一机制赋予了用户在分支形态上的精细控制能力。

**模块四：束线几何生成（Strand Geometry Generation）**
以打包后的束线粒子位置为控制点，生成B样条曲线作为广义圆柱的轨迹。每条束线对应一根固定直径的管道，从末梢连续延伸到根部。B样条保证了束线几何的光滑性，同时保留了粒子级别的位置信息用于后续网格构建。

**模块五：网格生成（Mesh Generation）**
本模块利用束线粒子的空间信息构建连续网格，流程为：
1. 在相邻分支段之间进行束线粒子位置的线性插值；
2. 对插值后的粒子位置进行Delaunay三角剖分；
3. 基于边缘长度阈值 $\epsilon$ 移除过长三角形，从而实现分支分离控制——较小的 $\epsilon$ 导致早期分离，较大的 $\epsilon$ 导致晚期分离（Fig. 8）；
4. 应用拉普拉斯平滑消除网格锯齿。

该网格生成策略与传统圆柱体方法的本质区别在于：它不是沿单一骨架路径扫掠，而是基于多束线的空间分布构建网格，因此能自然表达分支汇合处的复杂几何。

### 交互式操作符

在上述自动管线之上，系统提供了一组交互式操作符，允许用户实时干预树木形态：

- **交互式活力注入（Interactive Invigoration）**：用户点击树枝任意位置，系统向对应节点注入活力，驱动局部新生长（Fig. 5）。点击持续时间控制注入活力的大小。
- **不定芽形成（Adventitious Bud Formation）**：模拟创伤重发——用户修剪枝条后，在修剪位置注入活力可诱导不定芽发育，形成新的分支（Fig. 7）。
- **分支扭转（Branch Twisting）**：对选定分支施加螺旋生长效果，模拟某些树种的天然扭转形态（Fig. 6）。
- **轮廓绘制（Profile Sketching）**：用户可在任意节间绘制自定义横截面轮廓，实现空洞、劈裂、愈合等效果（Fig. 13）。

### 关键公式变量含义汇总

| 符号 | 含义 | 所在模块 |
|------|------|----------|
| $d_i$ | 束线粒子 $i$ 的位移距离 | 模块二 |
| $D_{\mathrm{large}}$, $D_{\mathrm{small}}$ | 大小分支在投影方向的最远范围 | 模块二 |
| $\mathbf{v}$ | 投影方向向量 | 模块二 |
| $\beta$ | PBD边界修正系数 | 模块三 |
| $\gamma_k$ | 吸引子 $k$ 的强度系数 | 模块三 |
| $\delta$ | 中轴影响系数 | 模块三 |
| $\epsilon$ | Delaunay三角剖分后三角形移除的边缘长度阈值 | 模块五 |

### 因果机制总结

整个方法的因果链条可概括为：**活力驱动的骨架发育** → **束线初始化与空间投影** → **PBD约束求解实现轮廓拟合** → **B样条生成束线几何** → **Delaunay三角剖分与阈值过滤构建网格**。其中，PBD打包步数和边缘长度阈值 $\epsilon$ 是两个关键的形态控制旋钮，分别影响分支分离的时序和空间程度。用户通过交互式操作符在骨架发育和轮廓定义层面注入设计意图，系统自动将高层编辑传播到底层束线表示和网格生成，实现了从粗略骨架到精细体积的完整建模闭环。

![[assets/figures/papers/paper_list_l20_https_storage_googleapis_com_pirk_io_projects_invigoration_index_html/figures/001_Figure_1.jpg]]
*Figure 1: The intricate branching structure of a mature acacia tree model created with our framework Interactive Invigoration*

![[assets/figures/papers/paper_list_l20_https_storage_googleapis_com_pirk_io_projects_invigoration_index_html/figures/004_Figure_3.jpg]]
*Figure 3: Overview of the strand particle placement and dynamics in tree branch modeling: (a) Initial placement of strand particles on the 2D local coordinate system at the end nodes of the branch graph. Strand particles are placed within the circular profile boundary. (b) Projection process of strand particles from the ’front planes’ of smaller branches onto the ’backplane’ of the main branch, with vector v illustrating the direction of displacement. (c) Integration and packing of strand particles on the backplane. Strand particles from different branches are merged onto a single plane, followed by a PBD process to resolve collisions and enforce packing constraints within the profile boundary on the...*

![[assets/figures/papers/paper_list_l20_https_storage_googleapis_com_pirk_io_projects_invigoration_index_html/figures/013_Figure_11.jpg]]
*Figure 11: An array of complex tree structures generated by our interactive tree modeling framework. (a) Shows user-guided branch growth through the Interactive Invigoration operator. (b) and (c) features the dynamic forms achievable with the Branch Twisting Operator. (d) Highlights the intricate branching structure of a mature tree model. (e) Features an unusual tree form achievable through user-defined profiles. (f ) Captures the stark silhouette of a Joshua tree. (g) represents a result achieved using the Adventitious Bud Formation and Twisting operator to generate a Juniper tree model. (h) Illustrates the application of both the invigoration and user-defined profiles to model a tree with a split t...*

## 实验与关键发现

本文的实验验证主要围绕三个方面展开：与基线方法的视觉对比、关键参数消融分析，以及交互式操作符的定性效果展示。由于缺乏定量用户研究，所有结论均基于视觉质量判断，需读者结合自身需求审慎参考。

### 与通用圆柱体方法的对比

论文将所提束线方法与 **Li et al.（2023）** 的通用圆柱体方法进行了对比。两种方法使用**完全相同的骨架图**和基于活力的生长模型，唯一差异在于体积表示和网格生成方式。如 **Fig. 10** 所示，束线方法生成的树枝形状“更复杂、更自然”，尤其在分支弯曲处和分叉区域展现出通用圆柱体无法捕捉的有机细节。这一差异的因果根源在于：通用圆柱体仅沿骨架轴生成固定截面网格，而束线方法通过粒子级投影、PBD打包和基于Delaunay三角剖分的网格生成，能够自然地塑造分支间的分离、融合与侧向形态变化。

**证据强度**：该对比仅提供单组视觉样例，未报告定量指标（如网格复杂度、用户偏好评分），因此“显著提升”的结论需谨慎对待，更宜视为定性趋势。

### 关键参数消融实验

论文通过三项消融实验揭示了核心参数对输出形态的因果控制作用：

**1. 每末端束线数量（Fig. 9）**

在固定节点数（21K）的条件下，将每末端束线数量从1条增加到4条，树干外观显著变化：4条束线产生的枝干表面更平滑，分支间分离更清晰。其机制在于，更多束线提供了更密集的粒子采样，使PBD打包和后续网格生成能更精细地逼近用户定义的轮廓边界，同时增强了分支交界处的几何分辨率。

**2. PBD打包步数（Fig. 14c-f）**

PBD迭代次数直接控制分支点的分离时机。步数较少时，粒子尚未充分向吸引子/中轴收敛，分支在早期即呈现分离状态；步数较多时，粒子被更紧密地拉向轮廓内部，分支在更晚阶段才分离。这一发现为艺术家提供了直观的形态控制手段：通过调整PBD超时步数（默认300-6000步，用户轮廓下1500-10000步），可在“早期分离”与“后期融合”之间连续调节。

**3. 网格生成中的边长阈值参数 ε（Fig. 8）**

在Delaunay三角剖分后，系统依据参数 ε 设定的边长阈值移除过长的三角形边，从而控制分支分离程度。较小的 ε 值导致早期分离（分支间连接更少），较大的 ε 值则产生后期分离（分支保持更长的融合状态）。该参数与PBD步数形成互补控制：PBD步数影响粒子在二维平面上的分布，ε 则在三维网格生成阶段决定哪些粒子群被识别为独立分支。

### 交互式操作符的定性效果

论文展示了一系列交互式操作符的生成结果，验证了框架的表达能力：

- **交互式活力注入（Fig. 5）**：用户点击树枝后，系统向对应骨架节点注入活力，驱动局部新生长。该操作符将程序化生长与用户意图实时结合，使非专业用户也能引导树木发育方向。
- **分支扭转（Fig. 6）**：通过扭转操作符可生成螺旋状分支生长效果，模拟某些树种的自然扭转形态。
- **不定芽形成（Fig. 7）**：模拟创伤性复生现象——用户剪除树枝后，在旧枝上注入活力可诱导不定芽发育为新枝，逐步形成复杂树冠结构。
- **轮廓绘制（Fig. 13）**：用户可为任意节间绘制自定义横截面轮廓，实现空洞、愈合组织、分裂枝干等效果。轮廓通过PBD约束束线粒子的分布，最终转化为三维体积形状。

![[assets/figures/papers/paper_list_l20_https_storage_googleapis_com_pirk_io_projects_invigoration_index_html/figures/008_Figure_6.jpg]]
*Figure 6: Twisting operator: branches can be generated mimicking spiral branch growth (right) and for comparison without twisting applied (left)*

### 性能数据与适用边界

**Table 1** 报告了不同复杂度模型的性能特征。束线数量从2K到12K的模型中，轮廓计算时间（PC）和网格生成时间（M）随复杂度增长。具体数值需查阅原表，但论文未提供与基线方法的运行时间对比，因此无法评估计算开销的相对竞争力。

**适用边界与失败模式**：

1. **计算密集性**：束线方法比基于网格细化的方法计算成本更高，当前未针对大规模森林场景进行扩展验证。
2. **骨架图依赖**：当骨架图发生变化时，所有束线需重新计算投影和打包，限制了实时编辑场景下的响应速度（论文指出可通过代码优化解决，但未实现）。
3. **生物精确性牺牲**：采用轮廓驱动而非模拟形成层年度生长，牺牲了时间一致性和生物精确性，不适合需要严格植物学准确度的应用。
4. **环境因素集成困难**：动态环境因素（天气、季节、土壤）的集成被列为开放问题，当前框架仅关注形态生成。
5. **参数语义模糊**：部分参数（如 ε 和中轴影响系数）的具体含义和推荐取值范围未充分说明，增加了用户调参负担。

### 实验验证的不足

论文的实验部分存在以下明显局限，读者在参考时需注意：

- **无定量用户研究**：所有效果评估均基于视觉质量的主观判断，缺乏用户偏好评分、任务完成时间或识别准确率等定量指标。
- **单一基线对比**：仅与Li et al.（2023）一种基线方法对比，未涉及其他树木建模方法（如基于L-system、粒子流或隐式曲面的方法）。
- **消融实验的定性性质**：参数消融仅展示视觉差异，未量化参数变化对网格质量、计算时间或用户满意度的影响。
- **泛化性未验证**：尽管展示了多种树种的结果（Fig. 16），但未系统评估方法在不同树形拓扑、分支密度或轮廓复杂度下的鲁棒性。

综上，本文的核心实验贡献在于**定性证明了束线表示相较于通用圆柱体在树枝形态表达上的优势**，并通过参数消融揭示了PBD步数、束线数量和边长阈值对分支形态的因果控制关系。然而，定量验证的缺失和适用边界的模糊性，使得该方法在实际生产流程中的可靠性仍需进一步检验。

![[assets/figures/papers/paper_list_l20_https_storage_googleapis_com_pirk_io_projects_invigoration_index_html/figures/015_Table_1.jpg]]
*Table 1: Performance characteristics of tree models with different levels of complexity. PC = Profile calculation time in seconds; M = time in seconds for computing a surface mesh*

![[assets/figures/papers/paper_list_l20_https_storage_googleapis_com_pirk_io_projects_invigoration_index_html/figures/010_Figure_8.jpg]]
*Figure 8: Having a single skeletal graph strand representation (a), the user can control the separation of branches at bifurcation points using small values for ?? resulting in early separation (b), medium values for medium separation (c), and high values for ?? resulting in late separation (d)*

## 定位与知识库关联

本文提出的 **Interactive Invigoration** 框架在树木建模知识库中的核心定位是：**将树木体积表示从“骨架驱动的通用圆柱体”推进到“束线驱动的可编辑体积模型”**。相对于已有工作，其改变的关键 slot 是**分支体积表示方法**——从 **Li et al. (2023)** 采用的沿骨架图直接生成通用圆柱体网格，转变为以固定直径束线（strands）作为体积基元，通过从末梢向根部的投影、位置动力学（PBD）打包、以及 B 样条曲线生成几何的方式构造树枝体积。这一改变使得树木建模首次能够在保持骨架图发育逻辑的同时，表达树枝的侧向生长细节（空洞、扭曲、愈合组织、分叉形态等）。

第二个被改变的 slot 是**次级生长建模**。基线方法（Li et al. 2023 的活力模型）仅通过骨架图节点属性定义分支粗细，缺乏对横截面形状和侧向不规则性的控制。本文引入用户可绘制的分支横截面轮廓（branch profiles），结合束线在轮廓内的 PBD 打包，将二维轮廓转化为三维体积形状，从而实现了对次级生长的显式建模。

第三个被改变的 slot 是**交互控制机制**。从程序化参数调整升级为交互式操作符集合，包括：交互式活力注入（点击树枝注入新生长）、不定芽形成（模拟创伤性重复生长）、分支扭转（螺旋生长效果）等，使用户能够实时、直观地编辑树木形态。

### 知识库挂载点

本工作可挂载到以下知识库节点：

1. **树木骨架建模（Tree Skeleton Modeling）**  
   继承自 Li et al. (2023) 提出的基于活力的信号模型来程序化生成骨架图（PG），但将其输出从“通用圆柱体的轨迹”重新定义为“束线投影与打包的空间参考”。该挂载点表明：本文的贡献不在于骨架发育算法本身，而在于骨架与体积表示之间的接口重构。

2. **基于粒子的体积表示（Particle-Based Volume Representation）**  
   束线粒子的投影、碰撞解决、吸引子/中轴约束等机制，与位置动力学（PBD）领域的粒子打包方法形成连接。本文的 PBD 打包算法（Algorithm 1）可视为 PBD 在树木体积建模中的特定实例化。

3. **交互式植物建模（Interactive Plant Modeling）**  
   交互式活力注入、轮廓绘制、扭转等操作符，将树木建模从“一次性生成”转变为“迭代式设计”，与交互式建模工具（如 Sketch-based modeling）的知识线对接。

4. **程序化网格生成（Procedural Mesh Generation）**  
   基于束线粒子位置的 Delaunay 三角剖分、边缘长度阈值移除（参数 $\epsilon$）、拉普拉斯平滑的网格生成管线，构成了从粒子集到连续网格的完整通路，可挂载到点云网格化方法的知识节点。

### 适用边界与限制

- **计算密集性**：束线方法比基于网格细化的方法计算成本更高。性能数据（Table 1）显示，轮廓计算时间（PC）和网格生成时间（M）随束线数量增长显著，对大规模森林场景的扩展存在挑战。
- **骨架图依赖性**：当用户修改骨架图时，所有束线需要重新计算投影与打包，目前尚未实现增量更新。
- **生物学精确性的取舍**：本文采用轮廓驱动方法定义次级生长，未模拟形成层年度生长的时间一致性，牺牲了年轮等时间维度的生物精确性以换取交互灵活性和视觉控制力。
- **环境因素集成困难**：动态环境因素（天气、季节、土壤）的集成被作者列为复杂且可能不产生真实结果的开放问题。

### 后续启发与开放问题

1. **定量验证的缺失**：本文的实验证据均为定性视觉比较（Fig. 10 与 Li et al. 的对比），缺乏用户研究或与真实树木观测（如伤口愈合、树瘤形成）的定量吻合度验证。后续工作可建立基准数据集进行系统评估。

2. **参数语义化**：控制分支分离的 $\epsilon$ 参数和中轴影响系数等关键参数的具体含义在论文中未完全明确（原文存在“??”占位），需要进一步澄清其几何或物理语义，以降低用户调参门槛。

3. **与生态模拟工具的集成**：如何将束线体积模型与动态环境模拟工具对接，实现更真实的生态交互（如风致变形、光照竞争下的形态适应），是一个有潜力的扩展方向。

4. **数据驱动的参数学习**：可否利用机器学习技术从真实树木扫描数据中自动推断特定物种的束线数量、轮廓形状、活力参数等，是提升方法自动化程度的关键开放问题。

5. **增量更新机制**：实现骨架图局部修改时的束线增量重计算，是提升交互响应速度和扩展到大尺度场景的必要工程优化。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Interactive_Invigoration_Volumetric_Modeling_of_Trees_With_Strands.pdf]]