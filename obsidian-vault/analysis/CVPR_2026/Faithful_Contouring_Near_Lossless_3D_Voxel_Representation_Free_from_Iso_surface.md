---
title: "Faithful Contouring: Near-Lossless 3D Voxel Representation Free from Iso-surface"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Faithful_Contouring_Near_Lossless_3D_Voxel_Representation_Free_from_Iso_surface.pdf
project_link: null
code_link: "https://github.com/Luo-Yihao/FaithC"
aliases:
- FCF
- FCNL3VRFFIS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: Faithful Contouring绕过距离场，直接从原始网格中为每个活跃体素拟合锚点位置和法向，并记录沿半轴交点的方向编码；这些局部操作完全可并行，无需全局一致性推断，从而在维持体素规整性的同时保留精细几何。
primary_logic: 每个体素与网格的相交片段可以独立地通过二次误差最小化估计出代表局部曲面的锚点位置和法向，半轴交点的符号则提供了确定面片连接的局部信息；这种完全局部的编码方式，配以闭合形式的求解，既避免了传统方法中的信息损失，又支持高分辨率和大规模并行计算。
claims:
- 在1024分辨率下，Faithful Contouring的Hausdorff距离为0.11±0.27×10⁻²，CD_GP为0.01±0.01×10⁻⁴，F₁_0.01为99.71±0.08，均优于对比方法。
- 在2048分辨率下，F₁_0.01达到99.99±0.00，证明了方法的高分辨率扩展能力。
- 在所有体素方法中，Faithful Contouring是唯一能够扩展到2048³的体素表示方法。
- VAE重建结果表明，FaithC在512分辨率下即可超越SparseFlex和Sparc3D在1024分辨率下的表现，CD降低约93%，F-score提升35%。
---

# Faithful Contouring: Near-Lossless 3D Voxel Representation Free from Iso-surface

> [!tip] 核心洞察
> 每个体素与网格的相交片段可以独立地通过二次误差最小化估计出代表局部曲面的锚点位置和法向，半轴交点的符号则提供了确定面片连接的局部信息；这种完全局部的编码方式，配以闭合形式的求解，既避免了传统方法中的信息损失，又支持高分辨率和大规模并行计算。

| 字段 | 内容 |
|------|------|
| 中文题名 | Faithful Contouring：免等值面的近无损三维体素表示 |
| 英文题名 | Faithful Contouring: Near-Lossless 3D Voxel Representation Free from Iso-surface |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.04029) · [Code](https://github.com/Luo-Yihao/FaithC) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | Faithful Contouring (FaithC) |
| Dataset | Representation fidelity benchmark, Mesh reconstruction (VAE) on Dora benchmark |

> [!tip] 效果简介
> - Representation fidelity benchmark (ABO, Objaverse, in-the-wild) 上，Hausdorff Distance (HD↓ ×10⁻²) Ours 1024: 0.11±0.27 vs SparC 1024 (次优，具体数值未提供)，其他方法更低 (达到所有方法中最低的HD)。
> - Representation fidelity benchmark 上，CD_GP↓ (×10⁻⁴) Ours 1024: 0.01±0.01 vs 对比方法（SparC等） (最小CD_GP，反映对细粒度结构的准确恢复)；F₁_0.01↑ Ours 1024: 99.71±0.08; Ours 2048: 99.99±0.00 vs SparC及其他方法（较低） (大幅提升，2048分辨率下几乎完美)。
> - Mesh reconstruction (VAE) on Dora benchmark 上，Chamfer Distance (CD↓) FaithC 1024: 0.06 / 0.05 vs SparseFlex 1024, Sparc3D 1024 (~93% CD reduction, F-score 35% improvement)。

## 概要

传统三维体素化流程依赖“网格 → 水密化 → 有符号距离场（SDF）/占用场 → Marching Cubes 等值面提取”这一管线，在预处理（水密化）、符号分配和曲面提取三个阶段均引入几何误差，导致尖锐特征丢失、内部结构消失和表面加厚。该管线对非水密、开放或复杂拓扑的网格尤为脆弱，且全局操作（如绕数、洪水填充）限制了分辨率扩展能力。

**Faithful Contouring (FaithC)** 提出了一条根本性不同的技术路线：**绕过距离场，直接从原始网格中为每个活跃体素独立拟合锚点位置与法向，并沿半轴交点记录方向编码**。其核心洞察是：每个体素与网格的相交片段可以通过二次误差最小化（QEF）以闭合形式局部估计出代表曲面的锚点，半轴交点的符号则提供确定面片连接的局部信息。这种完全局部的编码方式无需全局一致性推断，天然支持大规模并行计算，且避免了传统方法中的信息损失。

**主要结果**：在 1024³ 分辨率下，FaithC 的 Hausdorff 距离为 0.11±0.27×10⁻²，CD_GP 为 0.01±0.01×10⁻⁴，F₁_0.01 达 99.71±0.08，全面优于对比方法；在 2048³ 分辨率下 F₁_0.01 进一步提升至 99.99±0.00，且 FaithC 是目前唯一能扩展到 2048³ 的体素表示方法。在 VAE 重建任务中，FaithC 在 512³ 分辨率下即可超越 SparseFlex 和 Sparc3D 在 1024³ 下的表现，Chamfer Distance 降低约 93%，F-score 提升 35%。

三维几何的体素化表示是计算机图形学与三维视觉中的基础问题，其核心挑战在于：如何将连续的三角网格离散化为规整的体素结构，同时最大程度保留原始几何的精细细节与内部结构。这一问题的困难源于传统表示管线中固有的信息损失机制。

### 传统体素化管线的结构性缺陷

当前主流的体素化流程遵循一条“网格→场函数→等值面”的间接路径。首先，原始网格需要被转换为连续场表示，如无向距离场（UDF）或有符号距离场（SDF）；随后，通过Marching Cubes或其变体从场函数中提取等值面，重建出离散化后的曲面。这条管线在三个关键阶段系统性地引入几何误差（见图2）：

1. **预处理阶段的水密化**：将任意拓扑的开放网格转换为水密网格时，往往需要填充孔洞或加厚表面，导致原始几何被不可逆地修改。
2. **符号分配阶段的内/外推断**：SDF的构建依赖全局操作（如绕数法或洪水填充）来确定空间点的内/外符号。这类操作在非水密、非流形或复杂拓扑的网格上极易产生歧义，导致内部结构丢失或双层伪影。
3. **等值面提取阶段的阶梯状伪影**：Marching Cubes在体素棱上线性插值零等值点，其精度受限于体素分辨率，且无法恢复尖锐特征和薄层结构，最终产生阶梯状表面。

这些缺陷的根源在于：**传统管线将“体素化”视为一个场函数采样与重建的问题，而非直接对网格-体素相交关系进行编码的问题**。每一次中间表示的转换都意味着信息的一次有损压缩，而最终的等值面提取又将累积误差固化为几何伪影。

### 现有方法的瓶颈与空白

近年来，基于学习的体素表示方法（如**SparseFlex**（He et al., 2025）、**Sparc3D**（Li et al., 2025）、**XCube**（Ren et al., CVPR 2024）等）在三维生成和重建任务上取得了显著进展。然而，这些方法仍深度依赖上述传统管线：它们或隐或显地使用SDF/Occupancy作为监督信号，通过可微渲染或场回归来优化体素特征，再经Marching Cubes解码为网格。这一范式存在两个根本性瓶颈：

- **分辨率受限**：全局场函数的计算与存储开销随分辨率立方增长，使得现有方法通常难以超越1024³的体素分辨率。
- **几何保真度不足**：即使在1024分辨率下，等值面提取仍会产生可感知的细节损失和伪影，尤其对于开放曲面、薄壳结构和尖锐边缘。

### Faithful Contouring的动机与核心思路

Faithful Contouring的提出源于一个关键的观察：**体素与网格的相交关系本身携带了足够的局部几何信息，无需借助全局场函数即可实现高保真重建**。每个活跃体素内的网格片段可以通过局部二次误差最小化（QEF）估计出代表局部曲面的锚点位置和法向，而沿体素半轴的相交检测则提供了确定面片连接方向的局部编码。

基于这一洞察，Faithful Contouring完全绕开了距离场和等值面提取，直接从原始网格中为每个活跃体素拟合锚点并编码连接关系，形成“忠实轮廓令牌”（Faithful Contour Token, FCT）。这种**完全局部、可并行**的编码方式带来了三重优势：

1. **近乎无损的表示精度**：避免了场转换和等值面提取的累积误差，在1024分辨率下即可达到10⁻⁵量级的距离误差。
2. **高分辨率可扩展性**：局部操作无需全局状态，支持在单GPU上扩展至2048³分辨率，是目前唯一具备此能力的体素方法。
3. **对任意拓扑的鲁棒性**：无需水密化或内/外符号推断，天然支持开放曲面、非流形元素和多组件装配体。

简言之，Faithful Contouring将体素化从“场重建”范式转变为“局部几何编码”范式，为高保真三维表示开辟了新的技术路径。

## 核心方法与创新机理

Faithful Contouring 的核心创新在于**彻底绕过了传统体素化流程中“网格→距离场→等值面提取”的信息损失链**，转而采用一套完全局部、可并行、且具有闭合解的几何编码方案。这一设计改变了三个关键环节（changed slots），从根本上解决了传统方法在尖锐特征保留、内部结构维持和分辨率扩展上的长期瓶颈。

### 1. 表示管线的根本重构

传统管线（Figure 2）遵循“Mesh → 水密化 → SDF/占用场 → Marching Cubes 重网格化”的路径，每个步骤都是信息损失源：水密化强行闭合开放曲面、SDF 符号分配引入全局推断误差、Marching Cubes 等值面提取产生阶梯状伪影和表面加厚。

Faithful Contouring 的管线则完全不同：

```
Mesh → 活跃体素检测 → 锚点拟合 (QEF) → 半轴交点编码 → 基于令牌的解码重建
```

这一管线**直接从原始网格中提取体素化特征**，无需任何距离场转换或等值面提取。具体而言：
- **活跃体素检测**：使用分离轴定理（SAT）精确判定体素与三角形的相交关系，仅标记真正包含几何的体素，天然支持稀疏表示。
- **锚点拟合**：对每个活跃体素，通过二次误差最小化（QEF）联合估计代表局部曲面的锚点位置和法向，而非从距离场中插值出等值面顶点。
- **半轴交点编码**：沿体素半轴检测网格相交并记录方向符号，提供确定面片连接的局部信息，无需全局一致性推断。

### 2. 计算模式从全局到完全局部的转变

传统方法依赖全局操作来推断符号和提取曲面：基于无向距离场（UDF）的方法需要绕数（winding number）或洪水填充（flood-fill）来确定内/外，这些操作不仅计算昂贵，而且在非水密、开放或复杂拓扑网格上容易出错。

Faithful Contouring 的**所有核心操作均是完全局部的**：
- SAT 体素-三角形相交检测仅涉及单个三角形与单个体素；
- QEF 锚点拟合仅使用当前体素内的裁剪多边形质心作为样本；
- 半轴射线检测仅沿三个局部方向进行 Möller–Trumbore 线段-三角形测试。

这种完全局部的设计意味着**无需任何全局符号分配或渲染优化**，天然适合 GPU 大规模并行计算。所有编码（Alg. 1）和解码（Alg. 2）核心算子均实现为自定义 PyTorch 和 CUDA 内核。

### 3. 分辨率扩展能力的突破

传统体素方法受限于计算开销，通常难以超过 $1024^3$ 分辨率。Faithful Contouring 是**唯一能够扩展到 $2048^3$ 分辨率的体素表示方法**，且可在单 GPU 上运行。

这一能力源于两个设计选择：
- **稀疏性**：仅对与网格相交的活跃体素进行编码和存储，避免稠密体素网格的 $O(n^3)$ 存储和计算开销。
- **闭合解**：锚点位置通过法方程 $\left( M^{\top} M + \lambda I \right) \mathbf{x}^{*} = M^{\top} \mathbf{d} + \lambda \bar{\mathbf{c}}$ 直接求解，法向通过 Tikhonov 正则化的闭合解 $\tilde{\mathbf{n}} = (C + \mu I)^{-1} (\mu \bar{\mathbf{n}})$ 获得，无需迭代优化。

### 4. 与基线方法的关键差异

| 维度 | 传统方法 (UDF/SDF + MC) | Faithful Contouring |
|------|------------------------|---------------------|
| 前置条件 | 需要水密化预处理 | 直接处理任意网格（开放、非流形、多组件） |
| 中间表示 | 距离场（有信息损失） | 无中间表示，直接编码 |
| 曲面提取 | Marching Cubes 等值面（阶梯伪影） | QEF 锚点拟合（保留尖锐特征） |
| 符号推断 | 全局操作（绕数/洪水填充） | 完全局部（半轴交点编码） |
| 分辨率上限 | 通常 ≤ $1024^3$ | $2048^3+$ |
| 内部结构 | 易丢失（双层伪影） | 忠实保留 |

这些差异的因果机制在于：**Faithful Contouring 将每个体素视为独立的局部几何估计问题**，通过 QEF 最小化直接拟合最优锚点，而非从全局距离场中插值。这避免了距离场转换中的信息损失和等值面提取中的离散化误差，使得即使在 $8^3$ 的极低分辨率下（Figure 4），仍能保持整体形状和尖锐几何特征。

> **注意**：上述关于传统方法分辨率上限的断言基于论文中的对比实验设置（所有基线均在 ≤1024 分辨率下评估），具体各基线方法的最大可运行分辨率需查阅原始文献确认。

Faithful Contouring (FaithC) 提出了一条**免距离场、免等值面**的体素化表示管线，将任意三角网格直接编码为稀疏的 Faithful Contour Token (FCT)，并在解码时通过局部二次误差最小化（QEF）与半轴方向编码实现高保真重网格化。图3展示了该管线的完整流程。

### 编码器：从网格到 FCT

编码器以原始三角网格为输入，依次执行四个完全局部的并行操作，无需全局符号推断或水密化预处理：

1. **活跃体素检测（Active Voxel Detection）**：利用分离轴定理（SAT）判定每个体素与三角面片是否相交，标记所有活跃体素。此步骤直接处理非水密、开放或复杂拓扑的网格，避免了传统 UDF→SDF 管线中水密化和符号分配引入的误差。
2. **交点质心计算（Intersection Centroid Computation）**：对每个活跃体素内的裁剪多边形，通过分割三角形计算其质心 $\mathbf{c}_{v,f}$，作为后续锚点拟合的样本点。
3. **锚点拟合（Anchor Fitting）**：对每个活跃体素，通过带 Tikhonov 正则化的二次误差最小化，联合估计锚点位置 $\mathbf{x}^*$ 和法向 $\mathbf{n}^*$。位置与法向均存在闭合形式解，避免了 Marching Cubes 等值面提取产生的阶梯状伪影。
4. **半轴交点编码（Semi-axis Intersection Encoding）**：沿体素三个半轴方向进行 Möller–Trumbore 线段-三角形相交检测，记录方向编码 $\mathrm{orient} = \mathrm{sign}(\mathbf{n}^*, \hat{\mathbf{e}}) \in \{-1, 0, 1\}$，为后续面片定向与连接提供局部信息。

以上操作完全可并行，编码结果存储为 FCT——每个活跃体素包含锚点位置、法向及半轴编码，构成稀疏体素表示。

### 解码器：从 FCT 到网格

解码过程将 FCT 重建成高保真三角网格，同样由局部操作驱动：

1. **全局聚合（Global Gather）**：合并相邻体素共享的 dual 锚点，构建统一的顶点集。
2. **四边形面片定向与三角剖分**：根据半轴编码确定面片方向，对每个四边形面片选择使法向偏差最小的对角线进行三角剖分，确保重建曲面在尖锐特征处的连续性。

### 关键设计选择

- **完全局部操作**：编码与解码均不依赖全局一致性推断（如绕数、洪水填充），天然适合 GPU 大规模并行计算。
- **闭合形式求解**：锚点位置与法向的估计均通过法方程或 Tikhonov 正则化获得闭合解，避免了迭代优化的计算开销。
- **分辨率可扩展性**：得益于稀疏表示与局部操作，FaithC 是唯一能扩展到 $2048^3$ 分辨率的体素方法，且单 GPU 即可运行。

### 与 VAE 的集成

FaithC 进一步构建了基于 FCT 的 VAE 框架：编码器采用级联稀疏 3D 卷积残差块与轻量局部注意力层，支持 FCT 或点云输入；解码器通过分层上采样从潜码重建 FCT。训练损失函数加权组合锚点位置 MSE、法向余弦相似度、轴/掩码/占用二值交叉熵及 KL 散度，确保重建 FCT 的几何保真度。

图3 直观展示了上述编码-解码流程中数据形态的转换：输入网格 → 活跃体素 → 交点质心 → 锚点拟合 → 半轴编码 → FCT → 聚合 → 定向 → 重网格化输出。

### 补充图表

![[assets/figures/papers/paper_list_l2079_https_arxiv_org_abs_2511_04029/figures/003_Figure_3.jpg]]
*Figure 3: Faithful Contour pipeline. Encoder voxelizes the input mesh, then computes centroids, anchors, and semi-axis intersections, and stores them in the Faithful Contour Token (FCT) on K active voxels. Decoder gathers anchors, resolves orientations, and remeshes the tokens into highfidelity surfaces*

![[assets/figures/papers/paper_list_l2079_https_arxiv_org_abs_2511_04029/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of representing pipelines. Traditional UDF → water-tightening → SDF → iso-surface pipelines, relying on Marching Cubes and its variants, introduce artifacts at each lossy step, including artificial surface thickening, loss of internal structures, and jagged iso-surface extraction. In contrast, FAITHFUL CONTOURING directly obtains voxelized features, including fitted anchors and connections, from raw meshes with a highly accurate remeshing algorithm*

### 3.1 编码器：从网格到忠实轮廓令牌（FCT）

FaithC 的编码器将原始三角网格直接转化为稀疏体素表示，完全绕过距离场转换。其核心由四个局部可并行的模块串联构成。

**（i）活跃体素检测**
采用分离轴定理（SAT）检测每个体素 $v$ 与三角形 $f$ 的相交关系，标记所有存在交集的体素为“活跃体素”。这一步完全局部，无需全局符号推断。

**（ii）相交质心计算**
对每个活跃体素 $v$ 内的每个相交三角形 $f$，计算裁剪多边形 $Q_{v,f} = v \cap f$ 的质心 $\mathbf{c}_{v,f}$，作为后续锚点拟合的样本点。质心通过面积加权公式计算：

$$
\mathbf { c } _ { v , f } = \frac { 1 } { 3 A } \sum _ { k = 2 } ^ { m - 1 } A _ { k } ( \mathbf { q } _ { 1 } + \mathbf { q } _ { k } + \mathbf { q } _ { k + 1 } ) , \quad A _ { k } = \frac { 1 } { 2 } \| ( \mathbf { q } _ { k } - \mathbf { q } _ { 1 } ) \times ( \mathbf { q } _ { k + 1 } - \mathbf { q } _ { 1 } ) \|
$$

其中 $\mathbf{q}_1, \dots, \mathbf{q}_m$ 为裁剪多边形的顶点序列，$A_k$ 为子三角形面积，$A = \sum A_k$ 为总面积。

**（iii）锚点拟合（QEF）**
这是 FaithC 的核心创新模块：对每个活跃体素，通过二次误差最小化（Quadratic Error Minimization）联合估计代表局部曲面的锚点位置 $\mathbf{x}^*$ 和法向 $\mathbf{n}^*$。位置目标函数为：

$$
\mathbf { x } ^ { * } = \arg \operatorname* { m i n } _ { \mathbf { x } } \sum _ { i } ( \mathbf { n } _ { i } ^ { \top } ( \mathbf { x } - \mathbf { c } _ { i } ) ) ^ { 2 } + \lambda \| \mathbf { x } - \bar { \mathbf { c } } \| ^ { 2 }
$$

其中 $\mathbf{c}_i$ 和 $\mathbf{n}_i$ 为体素内第 $i$ 个相交片段的质心和法向，$\bar{\mathbf{c}}$ 为所有质心的均值，$\lambda$ 为正则化系数。法向目标函数为：

$$
\mathbf { n } ^ { * } = \arg \operatorname* { m i n } _ { \| \mathbf { n } \| = 1 } \sum _ { i } ( \mathbf { n } ^ { \top } ( \mathbf { x } ^ { * } - \mathbf { c } _ { i } ) ) ^ { 2 } + \mu \| \mathbf { n } - \bar { \mathbf { n } } \| ^ { 2 }
$$

两者均具有闭合形式解。位置的法方程为：

$$
\left( M ^ { \top } M + \lambda I \right) \mathbf { x } ^ { * } = M ^ { \top } \mathbf { d } + \lambda \bar { \mathbf { c } }
$$

法向的 Tikhonov 正则化解为：

$$
\tilde { \mathbf { n } } = ( C + \mu I ) ^ { - 1 } ( \mu \bar { \mathbf { n } } ) , \qquad \mathbf { n } ^ { * } = \frac { \tilde { \mathbf { n } } } { \| \tilde { \mathbf { n } } \| _ { 2 } }
$$

其中 $M$ 由各片段的法向堆叠而成，$\mathbf{d}$ 为 $M\bar{\mathbf{c}}$ 的对应项，$C$ 为协方差矩阵。这种局部 QEF 求解使 FaithC 能够绕过 Marching Cubes 的等值面提取，从根本上避免了体素网格的阶梯状伪影。

**（iv）半轴交点编码**
沿体素的三个半轴方向进行 Möller–Trumbore 线段-三角形相交检测，记录方向编码：

$$
\mathrm { o r i e n t } = \mathrm { s i g n } ( \mathbf { n } ^ { * } , \hat { \mathbf { e } } ) \in \{ - 1 , 0 , 1 \}
$$

该编码为后续解码阶段确定面片连接方向提供了局部信息，无需全局一致性推断。

### 3.2 解码器：从 FCT 到高保真曲面

解码过程将 $K$ 个活跃体素的 FCT 令牌重建为网格曲面。

**全局汇聚**：合并共享的 dual 锚点，消除冗余，构建统一的顶点集。

**四边形面片定向与三角剖分**：根据半轴编码确定每个四边形面片的方向。三角剖分时，选择使法向偏差最小的对角线：

$$
\{ d _ { i } , d _ { j } \} = \arg \operatorname* { m i n } _ { ( 1 , 3 ) , ( 2 , 4 ) } \sum _ { t \in T _ { i j } } \big ( 1 - \langle \mathbf { n } ( t ) , \mathbf { n } _ { \mathrm { a v g } } \rangle \big )
$$

其中 $T_{ij}$ 为对角线 $(i,j)$ 对应的两个三角形，$\mathbf{n}(t)$ 为三角形法向，$\mathbf{n}_{\mathrm{avg}}$ 为四边形顶点法向的均值。

### 3.3 VAE 训练损失

FaithC VAE 的总损失为多任务加权组合：

$$
{ \mathcal { L } } = \lambda _ { \mathrm { { x } } } { \mathcal { L } } _ { \mathrm { { x } } } + \lambda _ { \mathrm { { n } } } { \mathcal { L } } _ { \mathrm { { n } } } + \lambda _ { \mathrm { { a x i s } } } { \mathcal { L } } _ { \mathrm { { a x i s } } } + \lambda _ { \mathrm { { m a s k } } } { \mathcal { L } } _ { \mathrm { { m a s k } } } + \lambda _ { \mathrm { { o c c } } } { \mathcal { L } } _ { \mathrm { { o c c } } } + \lambda _ { \mathrm { { K L } } } { \mathcal { L } } _ { \mathrm { { K L } } }
$$

其中 $\mathcal{L}_{\mathrm{x}}$ 为锚点位置的 MSE 损失，$\mathcal{L}_{\mathrm{n}}$ 为法向的余弦相似度损失，$\mathcal{L}_{\mathrm{axis}}$、$\mathcal{L}_{\mathrm{mask}}$、$\mathcal{L}_{\mathrm{occ}}$ 分别为半轴编码、体素掩码和占用的二值交叉熵损失，$\mathcal{L}_{\mathrm{KL}}$ 为潜在空间的 KL 散度正则项。

## 实验与关键发现

### 表示保真度对比

Faithful Contouring 在直接表示质量上全面超越现有体素方法。Table 1 汇总了在 ABO、Objaverse 及 in‑the‑wild 网格上的定量结果。在 1024 分辨率下，FaithC 取得最低的 Hausdorff 距离 **0.11±0.27×10⁻²** 和最小的 Chamfer Distance (CD_GP) **0.01±0.01×10⁻⁴**，同时 F₁_0.01 达到 **99.71±0.08**。当分辨率提升至 2048 时，F₁_0.01 进一步攀升至 **99.99±0.00**，HD 保持 0.11±0.18，CD_GP 低于 0.01×10⁻⁴，证明方法具有极强的高分辨率扩展能力——FaithC 是目前唯一可扩展至 2048³ 的体素表示方法。

![[assets/figures/papers/paper_list_l2079_https_arxiv_org_abs_2511_04029/figures/007_Table_1.jpg]]
*Table 1: Quantitative comparison of different voxel representation. All HD values are scaled by*

Figure 6 的定性对比揭示了传统管线（UDF 水密化、Flood‑Fill SDF、SparC）的典型失效模式：双层伪影、内部结构丢失、表面加厚以及体素阶梯状凹凸。FaithC 通过局部 QEF 锚点拟合绕过了 Marching Cubes 等值面提取，从根本上消除了这些伪影，能够以单层表面表示开放曲面，并忠实保留精细细节与内部几何，2048 分辨率下细节进一步增强。

![[assets/figures/papers/paper_list_l2079_https_arxiv_org_abs_2511_04029/figures/006_Figure_6.jpg]]
*Figure 6: Comparison of representations. From top to bottom: Ground Truth, UDF (1024), Flood-Fill (1024), SparC [28] (1024), and our method (FAITHFUL CONTOURING) at 1024 and 2048. Competing methods often suffer from double-layer artifacts, loss of internal structures, or surface thickening (red circles) and voxel-lattice artifacts or bumping on reconstructed faces. In contrast, FAITHFUL CONTOURING generates clean, high-fidelity surfaces; represents open surfaces with single-layers; and faithfully preserves fine details and internal geometries across diverse categories, with higher resolution further improving details*

### VAE 重建质量

在 3D 生成任务的 VAE 重建基准（Dora benchmark）上，FaithC 同样展现出显著优势。Table 2 显示，FaithC 在 1024 分辨率下的 Chamfer Distance 低至 **0.06/0.05**（全量/水密子集），相比 SparseFlex 和 Sparc3D 在同等 1024 分辨率下的表现，CD 降低约 **93%**，F‑score 提升约 **35%**。值得注意的是，即使在 **512** 的低分辨率下，FaithC VAE 的重建质量仍明显优于 SparseFlex 和 Sparc3D 在 1024 分辨率下的结果，这直接证明了 FCT 表示本身的高容量与保真性。Figure 7 的可视化进一步印证了 FaithC 在复杂形状、开放曲面和内部结构重建上的优越能力。

![[assets/figures/papers/paper_list_l2079_https_arxiv_org_abs_2511_04029/figures/008_Table_2.jpg]]
*Table 2: Quantitative results of VAE reconstruction quality. The “/” separates results over the full dataset vs. the watertight subset. † indicates our re-implementation. We specify the compression schemes for different VAEs, where “Vec.” indicates compression using vecset [66], and “Vox*

![[assets/figures/papers/paper_list_l2079_https_arxiv_org_abs_2511_04029/figures/009_Figure_7.jpg]]
*Figure 7: Comparison of VAE reconstructions. Our method demonstrates superior performance in reconstructing complex shapes, open surfaces, and interior structures, compared to existing VAEs*

### 消融与关键机制分析

**局部 QEF 锚点拟合的有效性**：传统体素化方法在低分辨率下会产生严重的阶梯状伪影，而 FaithC 通过在每个活跃体素内求解带正则化的二次误差最小化（QEF）来联合估计锚点位置与法向，即使在 8³、16³、32³、64³ 等极低分辨率下，重建结果仍能保持整体形状并捕获尖锐几何特征（Figure 4）。这一完全局部的操作无需全局符号推断，从根本上避免了传统管线中信息损失累积的问题。

**表示容量与压缩效率**：FaithC VAE 在 512 分辨率下即可超越 SparseFlex 和 Sparc3D 在 1024 下的表现，说明 FCT 的锚点‑半轴编码方式在同等体素预算下携带了更丰富的几何信息。稀疏体素结构配合自定义 CUDA 内核，使编码和解码均可在单 GPU 上高效并行执行，支撑 2048+ 分辨率。

### 局限与失效模式

尽管 FaithC 在绝大多数场景下表现优异，验证分析揭示了以下边界情况：
- **歧义锚点**：在严重自交或紧密薄层等复杂拓扑处，局部 QEF 可能产生歧义锚点，导致局部微小漂移，这一问题在极端薄壁结构中尤为明显。
- **VAE 未充分利用表示能力**：当前 VAE 在高度不规则结构上的重建质量仍有提升空间，解码后 FCT 的平滑度和锐度相比原始拟合略有下降，表明生成模型的架构设计尚未完全匹配 FCT 的表达潜力。

### 公平性说明

所有基线方法均基于公开可用代码实现或重新实现，评估指标直接根据各方法输出结果计算，未经过任何后处理，确保了对比的公平性。

## 定位与知识库关联

### 1. 与基线方法的关系

**Faithful Contouring (FaithC)** 的核心突破在于对传统体素化管线的根本性重构。传统方法——无论是基于无向距离场（UDF）的水密化重建（如 **Dora**，Chen et al., CVPR 2025），还是基于洪水填充（Flood-fill）符号分配的SDF重建——均遵循“Mesh → Watertightening → SDF/Occupancy → Marching Cubes remeshing”的管线。这一管线在三个环节系统性地引入误差：水密化预处理改变原始拓扑、符号分配产生内外歧义、等值面提取丢失尖锐特征并造成表面加厚。FaithC完全绕过距离场和等值面提取，直接从原始网格中为每个活跃体素拟合锚点位置与法向，并通过半轴交点编码方向信息，将管线重构为“Mesh → Active Voxel Detection → Anchor Fitting (QEF) → Semi-axis Intersection Coding → Token-based Decoding”。

在计算模式上，传统方法依赖全局操作（如绕数计算、洪水填充）推断体素的内/外属性，这些操作难以并行化且对非水密网格脆弱。FaithC的所有核心操作——包括分离轴定理（SAT）的体素-三角形相交检测、裁剪多边形质心计算、二次误差最小化（QEF）锚点拟合、以及Möller–Trumbore半轴射线检测——均为完全局部的并行操作，无需全局一致性推断。所有编码（Alg. 1）和解码（Alg. 2）核心算子均以自定义PyTorch和CUDA内核实现，这使其成为**唯一能够扩展到2048³分辨率的体素表示方法**，而其他方法通常受限于≤1024分辨率。

与最新的稀疏体素方法相比：**SparC (Sparc3D)**（Li et al., 2025）和 **SparseFlex (TripoSF)**（He et al., 2025）均基于变形的稀疏体素SDF框架，本质上仍依赖距离场和等值面提取。FaithC在1024分辨率下的Hausdorff距离（0.11±0.27×10⁻²）和CD_GP（0.01±0.01×10⁻⁴）均显著优于这些方法；更关键的是，即使在512的低分辨率下，FaithC VAE的重建质量仍明显优于SparseFlex和Sparc3D在1024分辨率下的结果，CD降低约93%，F-score提升35%。这表明FaithC的表示本身具有更高的信息容量，而非单纯依赖分辨率提升。

在3D生成VAE领域，FaithC与 **Craftsman**（Li et al., 2024）、**Dora**（Chen et al., CVPR 2025）、**Trellis**（Xiang et al., CVPR 2025）、**XCube**（Ren et al., CVPR 2024）等形成对比。这些方法或依赖向量集压缩、或采用降采样体素压缩，而FaithC的FCT（Faithful Contour Token）直接在体素级编码锚点位置、法向和半轴方向，提供了结构化的高保真潜在表示。

### 2. 适用边界与局限

FaithC的设计使其天然适用于传统方法难以处理的场景：

- **非水密与开放曲面**：无需水密化预处理，可直接表示开放边界和单层表面，避免了UDF方法的双层伪影。
- **复杂拓扑与内部结构**：无需全局符号分配，可保留内部几何结构（如嵌套壳体），这是SDF方法因符号二义性而丢失的信息。
- **多组件装配**：FCT支持组件级编辑，包括装配、变换/姿态调整和纹理恢复（Figure 5）。

然而，方法存在以下明确局限：

1. **歧义锚点问题**：在严重自交或紧密薄层等复杂情况下，局部QEF拟合可能产生歧义锚点，导致局部微小漂移。这是完全局部方法的内在代价——缺乏全局一致性约束时，极端几何配置下的局部最优可能偏离真实曲面。

2. **VAE未充分利用表示能力**：当前VAE在高度不规则结构上的重建质量仍有提升空间，解码后的FCT在平滑度和锐度上相较于原始拟合略有下降。这表明VAE架构尚未完全释放FCT的表达潜力。

3. **缺乏可微分性**：当前编码和解码流程为非可微分操作，限制了其直接集成到基于梯度的学习框架中的能力。

### 3. 开放问题

论文明确提出了四个开放方向：

1. **锚点鲁棒性增强**：如何在紧密薄层等挑战性场景下提高锚点估计的鲁棒性？可能的路径包括引入轻量级局部一致性约束或自适应正则化策略。

2. **可微分轮廓化与渲染**：开发可微分版本的轮廓化和渲染操作，以使FCT能够集成到基于梯度的优化和端到端学习框架中。这将大幅扩展其在逆向渲染、3D生成等任务中的适用性。

3. **动态分辨率分配**：当前方法采用均匀体素网格，在薄结构周围可能浪费容量，而在平坦区域可能分辨率不足。实现动态分辨率以更好地分配薄结构周围的表示容量是一个自然延伸。

4. **结构化潜在表示**：将轮廓令牌（FCT）用作高精度3D生成的结构化潜在表示，探索其在扩散模型、自回归模型等生成范式中的应用。FaithC在2048分辨率下F₁_0.01达到99.99±0.00的近乎完美重建，表明FCT有潜力成为高保真生成任务的理想中间表示。

### 4. 知识库定位

FaithC在3D表示知识谱系中占据了一个独特位置：它桥接了传统显式表示（网格）与隐式表示（距离场/占用场）之间的鸿沟。与显式网格相比，它提供了规整的体素结构，支持卷积和注意力操作；与隐式场相比，它避免了信息损失和昂贵的等值面提取。其核心贡献在于证明：**通过完全局部的几何操作（QEF锚点拟合+半轴方向编码），可以在维持体素规整性的同时实现近无损的几何保持**。这一洞察为高分辨率3D深度学习提供了新的表示范式选择。

## 原文 PDF

![[paperPDFs/CVPR_2026/Faithful_Contouring_Near_Lossless_3D_Voxel_Representation_Free_from_Iso_surface.pdf]]
