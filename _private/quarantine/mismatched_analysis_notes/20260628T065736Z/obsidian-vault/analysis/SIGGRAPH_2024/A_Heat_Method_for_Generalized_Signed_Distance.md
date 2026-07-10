---
title: A Heat Method for Generalized Signed Distance
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/A_Heat_Method_for_Generalized_Signed_Distance.pdf
project_link: "http://geometry.cs.cmu.edu/intrinsic"
code_link: null
aliases:
- ITF
- HMGSD
tags:
- SIGGRAPH_2024
- topic/other_unclear
core_operator: 将网格几何表示从顶点坐标切换为边长度（edge lengths），并引入保距的内蕴边翻转（intrinsic edge flips）及内蕴重剖分操作，从而在保持原始几何精确性的前提下大幅提升网格单元质量。
primary_logic: 内蕴三角剖分（intrinsic triangulations）通过将形状的离散描述与嵌入空间解耦，实质性地扩大了可用剖分的空间；这一松弛使得可以在不牺牲几何精度的情况下构建具有良好角度界、均匀度以及高数值精度的剖分，并使得诸多原本只能在高质量网格上运行的算法能够直接应用于低质量输入数据。
claims:
- 内蕴 Delaunay 细化可将最小内角提升至不低于30°。
- 在谐波格林函数和短期热核计算中，内蕴自适应细化所需顶点数仅为传统外赋 Delaunay 细化的 1/18 和 1/54。
- 在泊松方程测试中，将内蕴 Delaunay 解直接复制到外赋网格可使平均误差降低约 12.5 倍，而使用 L2 投影传输则降低约 25 倍。
- 随机生成平面域上的泊松方程 (Poisson equation) 上 平均 L2 误差 = 内蕴求解 + 顶点复制：误差降低 12.5x；+ L2 投影：误差降低 25x
---

# A Heat Method for Generalized Signed Distance

> [!tip] 核心洞察
> 内蕴三角剖分（intrinsic triangulations）通过将形状的离散描述与嵌入空间解耦，实质性地扩大了可用剖分的空间；这一松弛使得可以在不牺牲几何精度的情况下构建具有良好角度界、均匀度以及高数值精度的剖分，并使得诸多原本只能在高质量网格上运行的算法能够直接应用于低质量输入数据。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于内蕴三角剖分的几何处理 |
| 英文题名 | A Heat Method for Generalized Signed Distance |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://nzfeng.github.io/research/SignedHeatMethod/index.html) · [Project](http://geometry.cs.cmu.edu/intrinsic) |
| Topic | #topic/other_unclear |
| Method | Intrinsic Triangulation Framework (内蕴三角剖分框架) |
| Dataset | Thingi10k 数据集上的内蕴 Delaunay 翻转 |

> [!tip] 效果简介
> - 随机生成平面域上的泊松方程 (Poisson equation) 上，平均 L2 误差 内蕴求解 + 顶点复制：误差降低 12.5x；+ L2 投影：误差降低 25x vs 直接在外赋网格上求解 (12.5x / 25x 改善)。
> - 谐波格林函数 (harmonic Green's function) 上，顶点数 3029 (Intrinsic AMR) vs 54916 (Extrinsic Delaunay Refinement) (18x 减少)。
> - 短期热核 (short time heat kernel) 上，顶点数 1551 (Intrinsic AMR) vs 81702 (Extrinsic Delaunay Refinement) (54x 减少)。

## 概要

传统外赋网格处理面临一个根本瓶颈：输入网格常含有狭长三角形与非 Delaunay 边，导致离散拉普拉斯算子构建及 PDE 求解数值不稳定、精度差，而外赋重剖分方案要么改变几何，要么需要插入大量顶点。本课程系统阐述**内蕴三角剖分框架**，将网格几何表示从顶点坐标切换为边长度，并引入保距的内蕴边翻转与重剖分操作，在严格保持原始表面度量的前提下大幅提升单元质量。核心洞察在于：将形状的离散描述与嵌入空间解耦，实质性地扩大了可用剖分空间，使得最小内角可提升至不低于 30°，且内蕴自适应细化在谐波格林函数和短期热核计算中所需顶点数仅为传统外赋 Delaunay 细化的 1/18 和 1/54。该框架作为一座“桥梁”，允许现有几何处理算法直接运行于低质量输入数据，并将高精度解传回原网格，无需终端用户感知底层变换。

## 核心方法与创新机理

### 一、问题瓶颈：外赋网格的单元质量困境

传统几何处理算法（如有限元求解、测地线计算、参数化等）对输入网格的质量有隐性假设：三角形应接近等边，角度不宜过小，边应满足 Delaunay 条件。然而，实际应用中获取的网格——无论是三维扫描、CAD 导出还是用户建模——普遍存在大量狭长三角形、极小内角和非 Delaunay 边。直接在这些低质量外赋网格上构造 cotan-Laplacian 或求解 PDE，会导致刚度矩阵条件数恶化、数值解精度严重下降甚至完全失效。

问题的根源在于：**传统外赋网格将几何表示与嵌入空间绑定**——三角形被定义为三维空间中由顶点坐标 $f_i \in \mathbb{R}^3$ 决定的平面片。要改善单元质量，就必须移动顶点或插入新顶点（如外赋 Delaunay 细化），这不可避免地改变了原始几何。换言之，在传统范式下，**几何精确性与单元质量是一对不可调和的矛盾**。

### 二、核心洞察：将几何表示从嵌入空间解耦

本课程的核心创新在于提出**内蕴三角剖分（Intrinsic Triangulations）**框架，其根本性的思想转变是：将网格的几何表示从顶点坐标切换为边长度。

**Changed Slot 1：几何表示（geometry representation）**
- 基线（外赋网格）：几何由顶点坐标 $f_i \in \mathbb{R}^3$ 编码，三角形是三维空间中的平面片。
- 内蕴方案：几何由边长度 $\ell_{ij} \in \mathbb{R}_{>0}$ 编码（见 Section 2.3.3）。三角形仅由三条边长定义，不再需要嵌入坐标即可计算面积（Heron 公式）、角度（余弦定律）和 cotan 权重等所有内蕴几何量。

这一松弛的深远意义在于：**只要保持边长度不变，任何共享相同拓扑的三角剖分都描述完全相同的离散度量**。这极大地扩展了可用剖分的空间——内蕴三角形可以“弯折”在底层多面体表面上，而不必是三维空间中的平面三角形（Fig. 3）。由此，我们可以自由地改变网格的连通性（重剖分）以改善单元质量，同时**精确保持原始几何**。

![[assets/figures/papers/paper_list_l20_https_nzfeng_github_io_research_SignedHeatMethod_index_html/figures/004_Figure_3.jpg]]
*Figure 3: Conceptually, intrinsic triangles can “bend” across an underlying polyhedron, yet still flatten out into standard triangles described by three ordinary edge lengths (left). This flexibility enables things that are impossible with standard, extrinsic algorithms—here, a mesh with tiny input angles becomes a geometrically identical Delaunay triangulation with angles no smaller than 30◦ (right). Since the output is described by conventional data (connectivity + edge lengths) it can still be used directly by many standard simulation and mesh processing algorithms*

### 三、关键使能操作：内蕴边翻转

**Changed Slot 2：边翻转（edge flip）的性质**
- 基线（外赋翻转）：翻转一条边会改变网格在三维空间中的几何形状。
- 内蕴方案：内蕴边翻转**精确保持表面度量**（Section 2.3.4）。翻转仅改变两个相邻三角形的对角连接方式，但由于新边长度可通过余弦定律从旧边长度计算得出，整个离散度量完全不变。

这一性质是内蕴重剖分的基石。它使得我们可以在不损失几何信息的前提下，执行经典的 Delaunay 翻转算法：对内蕴三角剖分中的每条非 Delaunay 边（即对边两侧三角形对角之和 $\alpha + \beta > \pi$），执行边翻转以恢复局部 Delaunay 条件。翻转过程仅需边长信息，无需顶点嵌入，最终收敛于唯一的**内蕴 Delaunay 剖分**。

### 四、框架模块与因果链路

内蕴三角剖分框架包含三个顺序模块，形成完整的“重剖分→求解→回传”管线：

**模块 1：内蕴重剖分（Intrinsic Retriangulation）**

该模块将输入外赋网格转换为高质量的内蕴剖分，包含三个层次的算法：

1. **内蕴 Delaunay 翻转**（Section 4.2）：从外赋网格提取初始边长度，执行贪婪边翻转直至所有边满足 Delaunay 条件。算法保证收敛到唯一的内蕴 Delaunay 剖分，且实践中翻转次数与网格规模呈线性关系（Fig. 23, Thingi10k 数据集验证）。

![[assets/figures/papers/paper_list_l20_https_nzfeng_github_io_research_SignedHeatMethod_index_html/figures/070_Figure_23.jpg]]
*Figure 23: An empirical study of the number of edge flips to produce an intrinsic Delaunay triangulation [Sharp et al. 2019b]. Each point is a 3D model from the Thingi10k dataset [Zhou and Jacobson 2016]. The observed complexity trend is linear, even on these difficult models*

2. **内蕴 Delaunay 细化**（Section 4.3, Algorithm 5 DelaunayRefine）：在翻转基础上，对仍存在小角度的三角形插入新顶点并重新翻转。可保证最小内角提升至不低于 30°（Fig. 24），且新增顶点仅增加内蕴剖分的自由度，不改变底层几何。

![[assets/figures/papers/paper_list_l20_https_nzfeng_github_io_research_SignedHeatMethod_index_html/figures/073_Figure_24.jpg]]
*Figure 24: Left: Rich data structures enable intrinsic Delaunay refinement, generating triangulations with good angle bounds. The black wireframe denotes the extrinsic mesh, while colored triangles give the intrinsic triangulation. Right: Signposts further enable vector field processing; the Laplacian of the intrinsic Delaunay triangulation offers a maximum principle for tangent vector fields, which here avoids unexpected flipped vectors when generating a smooth field*

3. **内蕴自适应细化**（Section 4.6）：根据解的局部特征（如格林函数的奇异性）进行选择性细化，在精度与计算成本间取得最优平衡。

**模块 2：内蕴计算（Intrinsic Computation）**

在获得高质量内蕴剖分后，在其上执行几何处理算法。核心是构造**内蕴 Delaunay Laplacian**（Changed Slot 3）：

- 基线（外赋 cotan-Laplacian）：依赖顶点坐标计算 cotan 权重，在低质量网格上可出现负权重，导致矩阵非正定。
- 内蕴方案：cotan 权重仅依赖边长度（见 Appendix A, Eq. (21)）：

$$\cot\theta_k^{ij} := \frac{\ell_{jk}^2 + \ell_{ki}^2 - \ell_{ij}^2}{4A_{ijk}}$$

其中 $A_{ijk}$ 由 Heron 公式给出：

$$A_{ijk} = \sqrt{s(s-\ell_{ij})(s-\ell_{jk})(s-\ell_{ki})}, \quad s := \frac{\ell_{ij}+\ell_{jk}+\ell_{ki}}{2}$$

由于内蕴 Delaunay 条件保证所有对角之和不大于 $\pi$，该 Laplacian 的所有 off-diagonal 权重非负，矩阵为 M-矩阵，满足离散极大值原理，且**对任意多面体唯一确定**（Section 4.1）。

**模块 3：解传输（Solution Transfer）**

内蕴剖分上计算得到的解（标量函数、向量场等）需要传回原始外赋网格。课程提供两种策略（Section 4.11）：

- **顶点值复制**：直接按顶点对应关系拷贝解值。简单高效，但引入近似误差。
- **$L^2$ 最优传输**：通过在两个剖分的公共细分上求解 $L^2$ 投影问题，实现最优逼近。

消融实验表明，在泊松方程测试中，顶点复制方案将平均误差降低约 12.5 倍，而 $L^2$ 投影方案降低约 25 倍（Section 4.11.1, inset figure），验证了高质量传输的必要性。

### 五、因果机制总结

整个框架的因果链条可概括为：

**边长度表示 → 内蕴边翻转（保距） → 内蕴 Delaunay 剖分（正定 Laplacian） → 高精度内蕴求解 → 解传输回外赋网格**

核心突破在于：通过将几何表示从嵌入空间解耦，打破了“改善单元质量必然改变几何”的固有约束，使得大量原本只能在高质量网格上运行的算法能够直接应用于低质量输入数据，且最终结果可以无损地传回原始表示。这一框架对用户透明——输入和输出均为标准外赋网格，所有内蕴操作均在“引擎盖下”完成。

### 六、边界条件与限制

需明确的是，内蕴框架**不提高几何逼近质量**：若输入网格本身是对光滑曲面的粗糙近似，内蕴处理不会改善逼近精度。框架假设输入网格的边长度精确描述了目标几何；拓扑缺陷（孔洞、非流形边）需预先修复。此外，框架主要针对多面体表面设计，对非平面多边形面的几何解释尚不完善。部分操作要求网格为流形且可定向，通过 tufted cover 可扩展至非流形网格，但顶点处仍存在限制。

![[assets/figures/papers/paper_list_l20_https_nzfeng_github_io_research_SignedHeatMethod_index_html/figures/027_Figure_14.jpg]]
*Figure 14: Local coordinate system for tangent vectors at vertices*

![[assets/figures/papers/paper_list_l20_https_nzfeng_github_io_research_SignedHeatMethod_index_html/figures/100_Figure_41.jpg]]
*Figure 41: Robustness in the context of differential surface editing [Lipman et al. 2004; Sorkine et al. 2004; Yu et al. 2004], where a system of equations involving a Laplacian is solved to deform a 3D model. Applying these techniques naively in the extrinsic mesh, which is nonmanifold and has many low-quality triangles, yields only numerical noise. Substituting the nonmanifold IDT Laplacian constructed on the tufted cover generates the expected smooth deformation*

## 实验与关键发现

内蕴三角剖分框架的实验验证围绕一个核心主张展开：**在不改变原始几何的前提下，通过内蕴重剖分大幅提升网格单元质量，从而显著改善几何处理算法的数值精度与计算效率**。以下从精度提升、效率增益、关键消融和适用边界四个维度组织证据。

### 精度提升：从泊松方程到热方法

最直接的精度证据来自**泊松方程求解**。在随机生成的平面域上，直接在外赋网格上构建标准 cotan-Laplacian 并求解，与内蕴 Delaunay 剖分上的求解结果进行对比。将内蕴解通过顶点值直接复制回外赋网格，平均 L2 误差降低约 **12.5 倍**；若采用 L2 最优投影进行解传输，误差进一步降低至约 **25 倍**（Section 4.11.1 插图）。这一结果揭示了两个层次的信息：内蕴 Delaunay Laplacian 本身的数值质量远优于低质量外赋网格上的 cotan-Laplacian；而解传输方式的选择对最终精度有显著影响。

在更复杂的几何处理任务中，精度优势同样显著。**热方法**（heat method）作为测地线计算的经典 PDE 方法，在低质量网格上运行时精度严重退化；替换为内蕴 Delaunay 剖分后，解的质量得到“戏剧性改善”（Fig. 29）。类似地，在**微分曲面编辑**任务中，原始外赋网格因存在非流形结构和大量低质量三角形，直接求解 Laplacian 方程组仅产生数值噪声；而基于 tufted cover 构造的非流形内蕴 Delaunay Laplacian 则生成了预期的光滑变形结果（Fig. 41）。

### 效率增益：内蕴自适应细化的顶点数优势

内蕴三角剖分的另一关键优势在于**计算效率**——通过内蕴自适应网格细化（Intrinsic AMR），可在远少于外赋 Delaunay 细化的顶点数下达到同等精度。在**谐波格林函数**计算中，内蕴 AMR 仅需 **3,029 个顶点**，而传统外赋 Delaunay 细化需要 **54,916 个顶点**，顶点数减少约 **18 倍**（Fig. 26）。在**短期热核**计算中，差距更为悬殊：内蕴 AMR 仅需 **1,551 个顶点**，外赋细化则需 **81,702 个顶点**，减少约 **54 倍**（Fig. 26）。

![[assets/figures/papers/paper_list_l20_https_nzfeng_github_io_research_SignedHeatMethod_index_html/figures/079_Figure_26.jpg]]
*Figure 26: Intrinsic AMR allows one to efficiently compute standard geometric kernels to high accuracy. Performing ordinary Delaunay refinement to the same accuracy requires 18x and 54x as many vertices on the harmonic Green’s function and short time heat kernel resp. [Sharp et al. 2019b]*

这一效率增益的根源在于：外赋 Delaunay 细化必须通过插入大量新顶点来同时满足 Delaunay 条件和保持几何形状，往往在狭长区域产生大量冗余三角形；而内蕴细化仅需在度量意义上进行局部加密，无需为维持嵌入几何而付出额外顶点代价（Fig. 28）。

### 翻转行为与角度界保障

内蕴 Delaunay 翻转算法的实际行为在 **Thingi10k 数据集**上得到了大规模验证。该数据集包含大量来自真实建模场景的困难模型，实验表明翻转次数与网格边数呈**线性关系**（Fig. 23），尽管理论上的最坏情况复杂度尚未得到严格证明。这一线性趋势对于工程应用至关重要，意味着内蕴 Delaunay 化的计算成本是可预测的。

在角度质量方面，**内蕴 Delaunay 细化**（Algorithm 5）可将最小内角提升至不低于 **30°**（Fig. 24），这一角度界对于有限元方法的数值稳定性具有重要意义。值得注意的是，这一改善是在完全保持原始几何度量的前提下实现的——外赋方法若要达到同样的角度界，要么需要插入大量顶点，要么必须移动顶点从而改变几何。

### 关键消融：解传输方式与路径变直早期停止

两项消融实验揭示了方法设计中的关键选择。

**解传输方式消融**（Section 4.11.1）：将内蕴解传回外赋网格时，简单的顶点值复制（12.5x 误差降低）与 L2 最优投影（25x 误差降低）之间存在约 2 倍的精度差距。这说明当外赋网格质量极差时，顶点位置本身可能并非解的最佳采样点，通过最小二乘投影将解重新拟合到外赋网格上可进一步补偿表示误差。

**路径变直早期停止消融**（Fig. 37）：在 FlipOut 算法（Algorithm 7）中，通过长度阈值或角度阈值提前终止翻转过程，可产生类似**离散曲线缩短流**的效果——在不过分偏离初始化路径的前提下生成更直的曲线，而非收缩为一个点。这一消融验证了算法作为连续曲线缩短流的离散模拟的有效性，并为实际应用中的参数调节提供了指导。

### 适用边界与已知局限

内蕴三角剖分框架的能力边界在课程笔记中有明确界定，这些边界对于正确使用该方法至关重要：

1. **几何逼近质量不改善**：内蕴三角剖分精确保持输入网格的离散度量。若输入网格本身是对光滑曲面的粗糙逼近（如稀疏采样或含噪声），内蕴处理不会提高逼近精度。框架的“精度提升”仅针对在给定离散几何上的数值计算精度。

2. **拓扑缺陷不修复**：孔洞、小柄、非流形边等拓扑问题需预先处理。tufted cover 构造可将框架扩展到非流形网格（Fig. 41），但顶点处的非流形性仍然存在，且 tangent 数据结构尚未完全适配。

3. **非平面多边形面的限制**：框架的几何解释（面积、离散曲率等）建立在平面多面体假设上。对于具有非平面多边形面的网格，缺乏统一的几何定义，内蕴“平面化”是否可作为全局优化的替代方案仍是开放问题。

4. **内蕴 Delaunay 细化的终止性**：全局终止性的理论证明尚不完整，尤其对于带边界的通用网格。实践中虽未观察到不终止的情况，但这一理论缺口意味着在某些极端输入上可能需要额外的保护机制。

5. **翻转复杂度**：尽管 Thingi10k 实验显示线性趋势，但渐近复杂度的严格最坏情况界尚未建立。在需要严格性能保证的场景中，这一不确定性需要关注。

## 定位与知识库关联

### 相对于已有方法的本质差异

本课程所构建的内蕴三角剖分框架，相对于传统外赋网格处理，改变的核心 **slot** 是 **几何表示**：将网格几何从顶点坐标 $f_i \in \mathbb{R}^3$ 切换为边长度 $\ell_{ij} \in \mathbb{R}_{>0}$。这一切换不是简单的数据格式转换，而是将形状的离散描述与嵌入空间解耦，从而实质性地扩大了可用剖分的空间。传统外赋网格处理直接使用输入网格进行 Laplace 算子构建和 PDE 求解，其数值精度受制于网格单元质量（狭长三角形、非 Delaunay 边等），而任何通过移动或插入顶点来改善质量的外赋重剖分方案（如 **Shewchuk 2002b** 的 Delaunay 细化）都会改变几何或需要大量顶点。内蕴框架的关键突破在于：**保距的内蕴边翻转**（intrinsic edge flips）可以在精确保持表面度量的前提下，将任意输入网格转换为内蕴 Delaunay 剖分，从而在不牺牲几何精度的条件下获得高质量的数值求解环境。

第二个被改变的 **slot** 是 **Laplacian 构造方式**。传统 cotan-Laplacian 依赖于顶点坐标嵌入，而内蕴 Delaunay Laplacian 仅依赖于边长度且具有唯一性——对任意多面体，其内蕴 Delaunay Laplace 矩阵是唯一确定的。这一性质使得原本只能在高质量网格上运行的算法（如热方法、有限元求解器）可以直接应用于低质量输入数据。

### 知识库挂载点

本工作可挂载于以下几个知识库节点：

1. **离散微分几何（DDG）——离散 Laplace-Beltrami 算子**：内蕴框架为 cotan-Laplacian 提供了不依赖嵌入的定义方式，将算子构建完全建立在边长度和三角形面积（Heron 公式）之上。余切权重可直接由边长度计算：$\cot\theta_k^{ij} := \frac{\ell_{jk}^2 + \ell_{ki}^2 - \ell_{ij}^2}{4A_{ijk}}$，避免了反三角函数的数值不稳定性。这为 DDG 中“离散算子应仅依赖于内蕴度量”的原则提供了完整实现。

2. **网格处理——重剖分与网格质量优化**：传统重剖分（remeshing）需要在几何保真度和单元质量之间权衡。内蕴重剖分将这一权衡彻底消除：通过内蕴 Delaunay 细化（Algorithm 5, DelaunayRefine）可将最小内角提升至不低于 30°，同时几何完全不变。这为重剖分领域提供了一个全新的范式。

3. **PDE 几何处理——解的质量与传输**：内蕴框架引入了解传输机制。实验表明，将内蕴 Delaunay 解直接复制到外赋网格可使泊松方程的平均 L2 误差降低约 12.5 倍，而使用 L2 最优传输则降低约 25 倍。这为“求解-传输”两阶段范式提供了量化证据。

4. **测地线与最短路径**：通过 FlipOut 算法（路径变直），内蕴边翻转可用于将任意初始路径精确缩短为多面体测地线，且早期停止可产生类似曲线缩短流的效果。这连接了离散测地线计算与内蕴重剖分两个方向。

### 适用边界

内蕴三角剖分框架的适用性受以下边界条件约束：

- **几何精度假设**：框架假设输入网格几何是精确的，不提高几何逼近质量。若输入存在噪声或逼近误差，内蕴处理不会改善。
- **拓扑完整性要求**：不修复拓扑缺陷（孔洞、小柄等），需预先进行拓扑修复。
- **多面体表面限制**：框架主要针对多面体表面（平面多边形）设计，非平面多边形缺乏统一的几何解释和离散曲率定义。
- **流形与可定向性**：部分操作要求网格是流形且可定向；通过 tufted cover 可扩展到非流形网格，但顶点处仍非流形，且 tangent 数据结构尚未完全适配。
- **理论完备性缺口**：内蕴 Delaunay 细化的全局终止性理论证明尚不完整（尤其对于带边界的通用网格），翻转算法的渐近复杂度也缺乏严格最坏情况界（尽管在 Thingi10k 数据集上表现为线性）。

### 后续启发与开放问题

本课程在结尾明确列出了若干开放问题，为后续研究提供了直接方向：

1. **嵌入问题**：给定连通性和边长度，能否嵌入为欧氏多面体？需要何种剖分？能否在无嵌入的前提下判定可嵌入性？这是内蕴框架的理论根基问题。

2. **非平面面的几何解释**：如何为含有非平面多边形的网格定义面积和离散曲率？内蕴“平面化”是否可作为全局优化的替代方案？

3. **高维推广**：如何将内蕴 Delaunay 及其性质（边翻转、曲率等）推广到四面体剖分？局部 cavity 操作是否可以替代四面体翻转？

4. **数据结构优化**：能否为 signpost 数据结构增加正常坐标以可证明地保证对应关系，同时比纯整数坐标更快？

对于后续研究者，本课程提供的代码示例、交互式演示和完整算法伪代码（Algorithm 1–7）构成了可直接复用的工程基础。内蕴三角剖分作为“桥梁”技术，其价值在于使得大量现有几何处理算法无需修改即可应用于低质量数据——这一“即插即用”特性使其具有广泛的后续应用潜力，包括物理模拟、几何深度学习的数据预处理等方向。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/A_Heat_Method_for_Generalized_Signed_Distance.pdf]]