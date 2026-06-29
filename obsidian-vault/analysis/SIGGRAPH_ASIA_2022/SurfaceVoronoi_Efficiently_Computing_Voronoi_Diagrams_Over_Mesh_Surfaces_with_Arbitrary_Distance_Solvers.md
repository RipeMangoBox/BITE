---
title: "SurfaceVoronoi: Efficiently Computing Voronoi Diagrams Over Mesh Surfaces with Arbitrary Distance Solvers"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/SurfaceVoronoi_Efficiently_Computing_Voronoi_Diagrams_Over_Mesh_Surfaces_with_Arbitrary_Distance_Solvers.pdf
project_link: null
code_link: "https://github.com/sssomeone/SurfaceVoronoi"
aliases:
- SurfaceVoronoi
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_geometry_processing
core_operator: 使用平方距离定义三角形内的线性距离场，并利用过传播策略保留每个三角形的所有贡献源，实现了精确的Voronoi图提取。
primary_logic: 通过将每个三角形的距离场表示为平方距离定义的半平面，并取它们的下包络，该方案在平面退化情况下精确还原2D Voroinoi图，同时能适配任意测地距离求解器。
claims:
- 每个三角形保留一个或多个距离三元组以帮助确定Voronoi分界线。
- 使用平方距离定义三角形内的线性变化，有助于在平面网格上报告精确VD。
- 过传播机制通过比较距离三元组缩小传播区域。
- 平方距离半平面的下包络在平面情形下精确对应2D Voronoi图（定理4.4）。
---

# SurfaceVoronoi: Efficiently Computing Voronoi Diagrams Over Mesh Surfaces with Arbitrary Distance Solvers

> [!tip] 核心洞察
> 通过将每个三角形的距离场表示为平方距离定义的半平面，并取它们的下包络，该方案在平面退化情况下精确还原2D Voroinoi图，同时能适配任意测地距离求解器。

| 字段 | 内容 |
|------|------|
| 中文题名 | SurfaceVoronoi：使用任意距离求解器在网格曲面上高效计算Voronoi图 |
| 英文题名 | SurfaceVoronoi: Efficiently Computing Voronoi Diagrams Over Mesh Surfaces with Arbitrary Distance Solvers |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2212.09029) · [Code](https://github.com/sssomeone/SurfaceVoronoi) |
| Topic | #topic/graphics_geometry_processing |
| Method | SurfaceVoronoi |
| Dataset | Horse, Dolphin, Bunny |

> [!tip] 效果简介
> - Horse (100K faces) 上，Runtime (seconds, 20K sites) 0.550 (EDBVD) vs 0.718 (RVD) (-23.4%)。
> - Dolphin (180K faces) 上，Runtime (seconds, 20K sites) 0.742 (EDBVD) vs 0.942 (RVD) (-21.2%)。
> - Bunny (70K faces) 上，Runtime (seconds, 20K sites) 0.453 (EDBVD) vs 0.501 (RVD) (-9.6%)。

## 概要

在三维网格曲面上计算 Voronoi 图（VD）的核心瓶颈在于：传统的多点距离传播仅保留每个顶点到最近源的距离，无法重建精确的 Voronoi 分界线；直接使用欧氏距离线性场会导致分界线锯齿化，且在曲面上不满足兼容性——当曲面退化为平面时无法还原标准二维 VD。

本文提出 **SurfaceVoronoi**，关键创新在于：用**平方距离**定义每个三角形内的线性距离场，并将每个三角形的距离场表示为平方距离半平面的下包络，从而在平面退化情况下精确还原二维 VD（定理 4.4）；同时引入**过传播策略**，使每个三角形保留所有贡献源的距离三元组，而非仅保留最近源，确保分界线提取的完整性。

实验表明，SurfaceVoronoi 的 EDBVD 实现比 RVD 和 LRVD 更快（例如在 Horse 模型 100K 面片、20K 站点上，0.550s vs 0.718s，加速 23.4%），且对三角剖分质量不敏感，避免了低质量剖分下分界线缺失的问题。该方法支持任意测地距离求解器作为插件，并可扩展至曲面限定 power diagram 及特征线约束 VD。

## 核心方法与创新机理

### 问题背景与根本瓶颈

在网格曲面上计算Voronoi图（VD）面临一个根本性困难：传统多点距离传播仅保留每个顶点到最近源的距离，构成一个最小距离场 $\mathrm{D}_{\mathrm{min}}$。然而，仅凭这一标量场无法重建精确的Voronoi分界线——分界线本质上是两个或多个距离场相交的轨迹，而最小场在跨越分界线时仅表现出斜率不连续，缺乏显式的源标识信息。如图2(d)所示，直接从多源距离场提取VD会导致分界线模糊或缺失。

更关键的是，即使尝试在每个三角形内用欧氏距离定义线性距离场，也会引入两个致命缺陷：**（1）分界线锯齿化**——由于线性场在三角形边上仅保证$C^0$连续，分界线在跨边处会产生折线伪影（图2(b)）；**（2）兼容性缺失**——当曲面退化为平面时，该方法无法还原精确的2D Voronoi图（图7(a)），说明欧氏距离线性场在曲面上不满足VD的几何本质。

### 核心洞察：平方距离半平面与下包络

SurfaceVoronoi的核心洞察源于对Voronoi图几何本质的重新认识：在2D平面上，Voronoi图等价于一组以源点为顶点的抛物面（平方距离场）的下包络在平面上的投影。将这一观察迁移到曲面网格上，论文提出用**平方距离**而非欧氏距离来定义每个三角形内的距离场变化。

具体而言，对于三角形$f = \triangle v_1 v_2 v_3$和源点$p$，定义提升平面$\Pi_{v_1 v_2 v_3}^{p}$为通过以下三点的平面：
$$(x_1, y_1, \|p - v_1\|^2),\quad (x_2, y_2, \|p - v_2\|^2),\quad (x_3, y_3, \|p - v_3\|^2)$$
其中$(x_i, y_i)$是顶点$v_i$在三角形局部坐标系中的2D坐标。该平面在三角形内部的$z$值定义了源$p$在该三角形内的平方距离场。

当曲面退化为平面时，这一构造具有决定性优势（定理4.4）：所有源点对应的提升平面$\{\Pi_{v_1 v_2 v_3}^{p_i}\}_{i=1}^n$的下包络，精确对应2D Voronoi图在三角形上的限制。这是因为在平面情形下，两个提升平面的高度差等于对应抛物面切平面的高度差（引理4.3），从而下包络的投影边界恰好是Voronoi分界线。

### 三个关键Changed Slots

相较于基线方法RVD（Yan et al., 2009）和LRVD（Yan et al., 2014），SurfaceVoronoi在三个关键维度上做出了根本性改变：

**Slot 1：距离度量——从欧氏距离到平方距离**

- **基线值**：RVD/LRVD使用欧氏距离定义三角形内的线性距离场$d = a_i x + b_i y + c_i$，其中系数由顶点欧氏距离确定。
- **提出值**：SurfaceVoronoi将顶点处的距离值替换为平方距离，即用$\|p - v_k\|^2$替代$d_g(p, v_k)$来构建半平面。这一替换看似简单，却从根本上改变了距离场的几何性质：欧氏距离线性场对应的是圆锥面的分段线性逼近，而平方距离线性场对应的是抛物面的切平面逼近。后者在平面退化情形下能够精确还原VD，赋予算法**兼容性**（compatibility）。
- **因果机制**：平方距离的选择使得三角形内的半平面切割操作等价于2D平面上的抛物面下包络计算，从而消除了分界线锯齿化（图2(e) vs 图2(b)，图7）。

**Slot 2：三角形保留的源信息——从“每顶点最近源”到“每三角形所有贡献源”**

- **基线值**：传统方法在每个顶点仅保留最近源标识，形成单源标签图。
- **提出值**：SurfaceVoronoi为每个三角形维护一个**贡献源列表**（source-point list），包含所有在该三角形内部某处取得最小距离的源点。判断标准是：若源$p_j$在三角形三个顶点上的距离均严格小于$p_i$，即满足$d_j^{(1)} < d_i^{(1)}, d_j^{(2)} < d_i^{(2)}, d_j^{(3)} < d_i^{(3)}$，则$p_i$在该三角形内被“击败”（defeated），不加入列表；否则$p_i$是贡献源。
- **因果机制**：这一设计确保每个三角形保留了足以确定其内部Voronoi结构的全部信息。如图3所示，不同三角形可能由不同数量的源贡献（颜色编码），这反映了VD的局部复杂度。贡献源列表是后续半平面切割的输入，直接决定了分界线的完整性和精度。

**Slot 3：传播策略——从全空间传播到过传播（over-propagation）**

- **基线值**：标准标记-清扫（mark-and-sweep）算法将每个源的距离场传播至整个网格。
- **提出值**：SurfaceVoronoi采用**过传播**策略：每个源的距离场向外传播，直到它不再对任何三角形的VD确定有贡献为止。具体地，在优先队列驱动的传播循环中，每次取出一个传播事件，检查对应源是否能更新当前三角形任一顶点的距离；若能，则将该源加入三角形的贡献源列表，并生成向相邻三角形的传播事件；若一个源在某个三角形中被击败（三个顶点距离均大于另一源），则停止向该方向传播。
- **因果机制**：过传播在不影响VD结果的前提下大幅缩小了每个源的传播区域（图2(f) vs 图2(e)），因为远离源的区域通常由更近的源主导。这一机制是实现高效计算的关键——实验表明，每个三角形的贡献源数量通常远小于总源数（图3右）。

### 算法管线与模块因果关系

SurfaceVoronoi的完整管线包含四个顺序模块，模块间存在严格的因果依赖：

**模块1：初始化**
- 为每个三角形分配空的半平面列表（用于存储贡献源的半平面表示）。
- 初始化空的优先队列$Q$用于距离传播。
- **输出**：就绪的数据结构。

**模块2：源事件入队**
- 对每个源点$p_i \in \{p_i\}_{i=1}^m$，将其初始传播事件推入$Q$。
- 每个事件包含源标识和初始三角形信息。
- **输出**：$Q$中包含$m$个初始事件。

**模块3：过传播循环（核心传播阶段）**
- 当$Q$非空时，取出队首事件，其关联源为$p$，当前三角形为$f$。
- **贡献判断**：检查$p$是否能更新$f$的任一顶点距离。若能，则$p$是$f$的贡献源，将其加入$f$的源列表。
- **事件生成**：若$p$被接受为贡献源，则向$f$的相邻三角形生成新的传播事件（携带更新后的距离信息）；否则，$p$在该方向停止传播。
- **循环终止**：$Q$为空时，每个三角形的贡献源列表已完整。
- **因果依赖**：模块3的输出（每个三角形的贡献源列表）是模块4的输入。过传播的正确性依赖于平方距离定义的击败条件（Slot 1和Slot 2的联合作用）。

**模块4：三角形内下包络计算（VD提取阶段）**
- 对每个三角形$f = \triangle v_1 v_2 v_3$，利用其贡献源列表构建半平面集合$\{\pi_i\}$。
- 每个半平面$\pi_i$编码源$p_i$在$f$内的线性平方距离场：$d = a_i x + b_i y + c_i$，其中系数由三个顶点的平方距离值通过线性方程组求解。
- **增量切割算法**：构造以$\triangle v_1 v_2 v_3$为底的无限三棱柱，然后依次用每个半平面$\pi_i$切割该体积，保留每次切割后的下包络。这一过程等价于在三角形基面上计算所有半平面的下包络。
- **VD追踪**：下包络的投影边界即为三角形内部的Voronoi分线段。将这些分段跨边连接，即得到完整的曲面Voronoi图。
- **因果依赖**：模块4的精度完全取决于模块3提供的贡献源列表是否完整。若某个源在三角形内部某处取得最小距离但未被包含在列表中，则该处的VD将出现错误。

### 关键公式与变量含义

**Voronoi区域定义**（2D欧氏空间）：
$$\Omega_i = \{ x \in \mathbb{R}^d \mid \|x - p_i\| \leq \|x - p_j\|, \forall j \neq i \}$$
该定义为曲面VD提供了理论基准：在平面退化情形下，算法输出应与此一致。

**三角形内源击败条件**：
$$d_j^{(1)} < d_i^{(1)},\ d_j^{(2)} < d_i^{(2)},\ d_j^{(3)} < d_i^{(3)}$$
其中$d_i^{(k)}$表示源$p_i$到三角形第$k$个顶点的距离。该条件是过传播剪枝的核心判据，保证了每个三角形仅保留必要的贡献源。

**半平面线性编码**：
$$d = a_i x + b_i y + c_i$$
其中系数通过两个顶点的距离值和三角形局部坐标求解。该半平面定义了源$p_i$在三角形内部任意点$(x,y)$处的平方距离逼近。

**提升平面定义**（定义4.1）：
$$\Pi_{v_1 v_2 v_3}^{p} \in \mathbb{R}^3$$
通过三个点$(x_k, y_k, \|p - v_k\|^2),\ k=1,2,3$的平面。在平面退化情形下，这些平面的下包络精确对应2D Voronoi图（定理4.4）。

### 扩展能力

SurfaceVoronoi的框架具有高度灵活性，可通过替换距离度量适配多种VD变体：
- **加权VD（power diagram）**：将距离替换为$\|v - p\|^2 - w$，其中$w$为源权重（图14）。
- **密度感知VD**：使用沿路径积分密度场的距离$d_{\rho}(v, p) = d(v, p) \int_0^1 \rho(t) \mathrm{d}t$，处理非均匀密度曲面。
- **断裂线约束VD**：通过修改传播规则阻止Voronoi单元跨越用户指定的断裂线（图13）。
- **曲线段源**：支持以曲线段而非离散点作为源站点（图1(d)）。

这些扩展仅需修改距离求解器插件，核心的过传播和半平面切割框架保持不变，体现了算法“任意距离求解器”驱动VD分割的设计哲学。

## 实验与关键发现

### 主结果：与RVD/LRVD的运行效率对比

SurfaceVoronoi在多个标准网格模型上与两种经典曲面Voronoi图算法——**RVD**（Yan et al., 2009）和**LRVD**（Yan et al., 2014）——进行了系统的运行时间对比。所有测试基于相同的站点数量（20K个源点），使用欧氏距离驱动分区，所得方法记为**EDBVD**。

Table 1给出了核心性能数据。在Horse模型（100K面片）上，EDBVD耗时0.550秒，RVD耗时0.718秒，加速约23.4%；在Dolphin模型（180K面片）上，EDBVD耗时0.742秒，RVD耗时0.942秒，加速约21.2%；在Bunny模型（70K面片）上，EDBVD耗时0.453秒，RVD耗时0.501秒，加速约9.6%。LRVD在多数情况下与RVD性能接近或略优，但EDBVD在所有测试模型上均取得了最短运行时间。

Figure 12进一步展示了不同面片规模下三种方法的运行时间变化趋势。在Vase（30K面片）、Dolphin（30K面片）、Bunny（70K面片）和Horse（100K面片）四个模型上，EDBVD的曲线始终位于RVD和LRVD下方，且随着面片数增加，性能优势保持稳定。

需要指出的是，论文未明确说明运行硬件平台，因此绝对时间数值的跨环境可比性受限，但同一平台上的相对趋势应可靠。

### 关键消融实验

#### 平方距离 vs. 欧氏距离定义半平面

这是SurfaceVoronoi最核心的设计选择。当使用欧氏距离定义三角形内的线性距离场时，分界线呈现明显的锯齿状（Figure 2(b)），且当曲面退化为平面区域时，算法无法还原精确的2D Voronoi图，即缺乏**兼容性**（compatibility）。Figure 7(a)展示了这一失效情形：在凸2D区域上，基于欧氏距离的半平面下包络与标准2D Voronoi图存在偏差。

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2212_09029/figures/002_Figure_2.jpg]]
*Figure 2: The VD based on lifting distance fields. (a) In 2D, the VD can be obtained by finding the lower envelope of a set of distance fields*

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2212_09029/figures/009_Figure_7.jpg]]
*Figure 7: (a) Algorithm 1 cannot report an exact VD when the base surface degenerates to a convex 2D region, thus lacking the property of compatibility. (b) By using squared distance to define half-planes, the resulting VD is the same with the exact 2D Voronoi diagram, endowing Algorithm 1 with the property of compatibility and the ability of dealing with face-interior sites*

改用平方距离定义半平面后，锯齿现象消失（Figure 2(e)），且在平面退化情形下能够精确还原2D Voronoi图（Figure 7(b)）。论文通过Theorem 4.4给出了严格证明：三角形提升平面$\Pi_{v_1 v_2 v_3}^{p_i}$的下包络配置恰好定义了关于源点集$\{p_i\}$的2D Voronoi图。这一理论保证使得EDBVD在任意平面区域上都能输出与标准Voronoi图一致的结果。

#### 过传播机制的有效性

过传播（over-propagation）是SurfaceVoronoi的另一关键技术。传统的多点距离传播通常仅保留每个顶点的最近源信息，这不足以重建三角形内部的精确Voronoi分界线。过传播策略改为为每个三角形保留所有贡献源的距离三元组，传播条件为：仅当源点$p_j$在当前三角形的三个顶点上的距离均小于$p_i$时，$p_i$才被判定为“被击败”并停止传播。

Figure 2(f)与Figure 2(e)的对比表明，过传播在不影响最终VD结果的前提下，大幅缩小了每个源的传播区域。Figure 3以颜色编码方式可视化每个三角形实际保留的贡献源数量：大部分三角形仅需保留1-2个源的距离场，仅靠近Voronoi分界线的三角形需要保留更多源信息。这种按需传播策略有效避免了全空间传播的计算浪费。

#### 对三角剖分质量的鲁棒性

Figure 9展示了EDBVD与LRVD在低质量三角剖分上的对比。LRVD依赖沿网格边的Dijkstra扫描来推断站点间的邻近关系，当三角剖分质量较差时，沿边传播可能无法可靠地报告邻近关系，导致部分Voronoi分界线缺失。相比之下，EDBVD通过三角形内部的半平面下包络计算直接确定分界线，不依赖边传播的拓扑正确性，因此在低质量剖分上仍能输出完整的Voronoi图结构。这一特性使得SurfaceVoronoi对输入网格的三角剖分质量具有更强的容忍度。

### 不同距离求解器的适配验证

SurfaceVoronoi的核心优势之一是可以适配任意距离求解器。Figure 8在Leaf模型上系统对比了多种距离度量驱动下的曲面Voronoi图结果：

- **VTP算法**（精确测地距离）：输出高质量曲面VD（Figure 8(b)），作为参考标准。
- **RVD**（欧氏距离）：可能产生无主区域（ownerless regions，Figure 8(c)中浅蓝色高亮部分）。
- **LRVD**（欧氏距离）：在公平剖分下与EDBVD结果一致（Figure 8(d) vs. Figure 8(e)）。
- **扩散距离**（diffusion distance）：除非输入网格具有很高的剖分质量，否则结果不精确（Figure 8(f)）。
- **快速行进法**（fast marching method）：结果与VTP相似但不完全精确（Figure 8(g)）。
- **通勤时间距离**（commute-time distance）和**双调和距离**（biharmonic distance）：与测地距离相差甚远，产生的VD与参考标准显著不同（Figure 8(h)-(i)）。

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2212_09029/figures/010_Figure_8.jpg]]
*Figure 8: Taking the Leaf model as the input (a), we visually compare the results produced by various approaches. We use the VTP algorithm to feed exact distances into our algorithm, yielding a high-quality surface VD (b). Both RVD (c) and LRVD (d) use the Euclidean distance to drive the surface partition, but RVD may produce ownerless regions (highlighted in light blue). If we takes Euclidean distance to drive the partition, the result (e) is the same as LRVD on this model (fair triangulation). Diffusion diagram (f ) is inaccurate except that the input mesh is with a high triangulation quality. If we take the fast marching method (g) as the plugin, the results are similar to (b) but not accurate. Co...*

这一对比验证了SurfaceVoronoi框架的距离求解器无关性：只要提供每个顶点到源点的距离值（或平方距离值），算法即可正常工作，而VD的质量直接取决于所采用距离度量的准确性。

### 扩展功能验证

论文还展示了SurfaceVoronoi的灵活扩展能力。Figure 13展示了带特征线约束的曲面Voronoi图，通过在传播过程中阻止距离场跨越用户指定的断裂线（breaklines），实现了受控分区。Figure 14展示了曲面限定power diagram，通过将距离替换为加权平方距离$\|\mathbf{v} - \mathbf{p}\|^2 - \mathbf{w}$，算法可直接支持带权重的Voronoi图划分。Figure 1(d)进一步展示了以曲线段而非离散点为源点的分区能力。

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2212_09029/figures/001_Figure_1.jpg]]
*Figure 1: We propose a novel algorithm for computing surface-based Voronoi diagrams, without the need of an off-the-shelf Voronoi/Delaunay solver. Our algorithm supports an arbitrary geodesic algorithm to drive the partition; Specially, it also supports Euclidean distance (a). Our algorithm is flexible enough to handle various versions of surface-based Voronoi diagrams. For example, it can be used to compute the surface-based power diagram (b). Furthermore, it enables users to draw breaklines to prevent any Voronoi cell from crossing the breaklines (c), and naturally supports curve segments as the source sites (d)*

### 失败模式与适用边界

论文明确指出了SurfaceVoronoi的若干局限性：

1. **半平面裁剪操作未经优化**：当前实现中，三角形内的增量半平面裁剪是计算瓶颈之一，作者指出该操作可进一步加速，但未给出具体的优化方案或加速比预期。

2. **高精度测地距离求解器下的效率问题**：当使用VTP等高精度精确测地距离求解器，且模型面片数很大而站点数很少时，总体运行时间较长。这是因为精确测地距离的计算本身开销较大，此时距离求解成为性能瓶颈而非VD提取过程。

3. **极细长三角形的数值稳定性**：论文提及极细长三角形可能导致数值问题，但未给出具体的退化阈值或定量分析。这一点的证据强度较弱，需要在实际应用中根据网格质量进行验证。

4. **非流形或破损网格的适用性未验证**：当前算法假设输入为流形三角网格，对于非流形、破损或自相交网格的扩展仍是一个开放问题。

总体而言，SurfaceVoronoi在标准三角网格上展示了优于RVD/LRVD的运行效率、对低质量剖分的鲁棒性，以及与任意距离求解器的适配灵活性。其核心创新——平方距离半平面与过传播机制——通过理论证明和实验验证得到了充分支撑。

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2212_09029/figures/011_Figure_9.jpg]]
*Figure 9: Comparison between EDBVD and LRVD on a poorly triangulated surface. Since the Dijkstra-sweep along mesh edges may fail to report reliable neighboring relationship between sites, LRVD may miss some bisectors but EDBVD cannot*

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2212_09029/figures/004_Figure_3.jpg]]
*Figure 3: Left: a planar mesh and the VD w.r.t. four sites. Right: for each triangle, we visualize how many distance fields (sources) really contribute to the triangle in a color-coding style*

## 定位与知识库关联

SurfaceVoronoi 的核心定位在于**改变网格曲面 Voronoi 图（VD）计算中的“距离场编码方式”和“源点信息保留策略”两个关键 slot**，从而在保持与任意测地距离求解器兼容的前提下，实现精确、无锯齿的曲面 VD 提取。

### 相对已有方法的本质差异

传统曲面 VD 方法如 **RVD**（Yan et al., 2009）和 **LRVD**（Yan et al., 2014）均基于欧氏距离驱动划分。RVD 采用全空间传播，在每个网格顶点仅保留到最近源的距离值，然后通过插值近似 Voronoi 分界线。这一策略存在两个根本性问题：（1）仅保留最近源信息不足以重建三角形内部的精确分界线，因为分界线可能穿过某个三角形而该三角形的三个顶点恰好被同一源点“统治”；（2）欧氏距离在三角形内线性变化，但不同源点的线性距离场相交时，其下包络在平面情况下并不等价于精确的 2D Voronoi 图，导致分界线出现锯齿状伪影（见 Fig. 2(b) 和 Fig. 7(a)）。

SurfaceVoronoi 改变了三个关键 slot：

1. **距离度量 slot**：从欧氏距离（线性）改为**平方距离（线性）**。这一改变的深层机理在于：在二维平面上，Voronoi 图等价于一组以源点为顶点的抛物面（由平方距离定义）的下包络在平面上的投影。当曲面退化为平面三角形网格时，使用平方距离定义的半平面进行增量切割，可以精确还原 2D Voronoi 图（定理 4.4 给出严格证明）。这一性质被称为“兼容性”（compatibility），是欧氏距离线性场所不具备的。

2. **源信息保留 slot**：从“每个顶点仅保留最近源”改为**每个三角形保留所有贡献源的 distance triples**。贡献源的判定基于“击败条件”：若源 $p_j$ 在三角形三个顶点上的距离均严格小于源 $p_i$，则 $p_i$ 在该三角形内被击败（$d_j^{(1)} < d_i^{(1)}, d_j^{(2)} < d_i^{(2)}, d_j^{(3)} < d_i^{(3)}$）。这一策略确保每个三角形内部的分界线计算拥有完整的候选源信息，而非仅依赖顶点处的局部最优。

3. **传播策略 slot**：从全空间传播改为**过传播（over-propagation）**。距离场从源点向外扫描，直到该源在所有三角形中均被击败、不再对 VD 有贡献为止。这在不影响最终 VD 结果的前提下大幅缩小了每个源的传播区域（Fig. 2(f) vs Fig. 2(e)，Fig. 3），是算法效率的关键保障。

### 知识库挂载点

SurfaceVoronoi 可挂载到以下知识库节点：

- **计算几何·Voronoi 图**：将经典 2D Voronoi 图的下包络/提升（lifting）理论（通过抛物面 $\Pi_{v_1 v_2 v_3}^{p}$ 的构造）推广到曲面网格，建立了“三角形内平方距离半平面下包络 ⇔ 曲面 VD”的桥梁。定理 4.4 和 Lemma 4.3 构成了这一推广的理论核心。

- **几何处理·测地距离**：算法与具体距离求解器解耦，支持 VTP 精确测地距离、快速行进法（FMM）、通勤时间距离、双调和距离等多种求解器即插即用（Fig. 8）。这使其成为一个通用框架，而非绑定特定距离度量。

- **几何处理·曲面重网格化与分区**：曲面 VD 是曲面重网格化、纹理图集生成、曲面分割等任务的基础算子。SurfaceVoronoi 支持受限 power diagram（通过加权距离 $\|\boldsymbol{v} - \boldsymbol{p}\|^2 - \boldsymbol{w}$）、特征线约束（breaklines，Fig. 13）、密度感知距离（$d_{\rho}(v, p) = d(v, p) \int_{0}^{1} \rho(t) \mathrm{d}t$）等扩展，覆盖了实际应用中的多种需求。

### 适用边界

1. **输入假设**：算法假设输入为流形三角形网格。对于非流形或破损网格的扩展是开放问题。
2. **数值稳定性**：极细长三角形可能导致半平面系数计算中的数值问题，这是因为系数求解涉及矩阵求逆（$\binom{a_i}{b_i} = \binom{x_1 \; y_1 \; 1 \atop x_2 \; y_2 \; 1}^{-1} \binom{d_i^{(1)}}{d_i^{(2)}}$）。
3. **性能边界**：当使用高精度精确测地距离求解器（如 VTP）且模型面片数很大而站点很少时，过传播的剪枝效果有限，总体运行时间可能较长。此外，三角形内的半平面裁剪操作未经深度优化，存在进一步加速空间。
4. **对比 LRVD 的优势场景**：在低质量三角剖分上，LRVD 可能因 Dijkstra 沿边扫描无法可靠报告站点邻接关系而缺失分界线，而 SurfaceVoronoi 对剖分质量不敏感（Fig. 9）。

### 后续启发

SurfaceVoronoi 的“过传播+平方距离半平面下包络”框架为曲面域上的几何划分问题提供了一个新范式。后续工作可从以下方向展开：（1）将半平面裁剪操作替换为更高效的凸多边形求交算法，以支持大规模实时应用；（2）探索将框架扩展到体网格或点云曲面；（3）借鉴 power diagram 的加权机制，发展更丰富的曲面分区控制手段。在知识库中，该工作可作为连接“经典 2D Voronoi 理论”与“曲面几何处理”的桥梁节点，为后续曲面采样、重网格化、各向异性分区等任务提供理论支撑和算法基线。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/SurfaceVoronoi_Efficiently_Computing_Voronoi_Diagrams_Over_Mesh_Surfaces_with_Arbitrary_Distance_Solvers.pdf]]