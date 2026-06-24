---
title: "Uniform Sampling of Surfaces by Casting Rays"
type: paper
paper_level: A
venue: SGP
year: 2025
pdf_ref: paperPDFs/SGP_2025/Uniform_Sampling_of_Surfaces_by_Casting_Rays.pdf
project_link: https://github.com/iszihan/implicit-uniform-sampler
aliases:
- USSRC
- USSBCR
tags:
- SGP_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "随机射线与曲面相交的交点集合，其中每条射线的所有交点都被保留，且射线采样方式保证了均匀性。"
primary_logic: "基于积分几何的柯西-克罗夫顿公式，通过在包围盒内均匀采样定向射线并将所有交点收集，可以直接在隐式曲面上生成严格均匀分布的白噪声样本，无需显式网格表示或投影步骤。"
claims:
- "通过均匀采样定向射线并收集所有交点，可在曲面上获得均匀分布的点集。"
- "修改后的球体追踪算法能从每条射线找到所有交点，且采样点严格位于曲面上，无需投影。"
- "在114个网格隐式函数数据集上，方法达到平均TV 0.372（与真实网格的0.373相当），且函数评估次数仅为拒绝采样的4.8%，为Marching Cubes的1.8%。"
- "MPZ14 mesh dataset (114 shapes) 上 Total Variation (TV) = 0.372"
---

# Uniform Sampling of Surfaces by Casting Rays

> [!tip] 核心洞察
> 基于积分几何的柯西-克罗夫顿公式，通过在包围盒内均匀采样定向射线并将所有交点收集，可以直接在隐式曲面上生成严格均匀分布的白噪声样本，无需显式网格表示或投影步骤。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过射线投射实现曲面均匀采样 |
| 英文题名 | Uniform Sampling of Surfaces by Casting Rays |
| 会议/期刊 | SGP 2025 |
| Links | [paper](https://arxiv.org/abs/2506.05268); [GitHub](https://github.com/iszihan/implicit-uniform-sampler) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Uniform Surface Sampling via Ray Casting |
| Dataset | MPZ14 mesh dataset (114 shapes) |

> [!tip] 效果简介
> - MPZ14 mesh dataset (114 shapes) 上，Total Variation (TV) 为 0.372，对比 0.373 (Rejection Sampling)，变化 -0.001。
> - MPZ14 mesh dataset (114 shapes) 上，Number of Function Evaluations 为 1.92×10^7，对比 3.98×10^8 (Rejection Sampling)，变化 -3.79×10^8。

## 概述

### 问题瓶颈

在隐式曲面（如神经隐式函数）上进行**均匀随机采样**是一个基础但困难的操作。现有方法面临三难困境：
- **拒绝采样**在包围体内随机撒点，仅保留位于曲面上的点，效率极低，大量函数评估被浪费；
- **Marching Cubes网格提取采样**需要将隐式函数转化为显式网格，引入离散化误差和投影步骤，破坏严格均匀性；
- **Hamiltonian Monte Carlo**（Chiu, MIT 2022）等MCMC方法需要额外的非平凡投影步骤才能使采样点精确位于曲面，且可能产生重复样本。

核心瓶颈在于：缺乏一种**无需显式网格表示、无需误差诱导的投影步骤**，即可在连续隐式曲面上生成严格均匀分布白噪声样本的方法。

### 核心思路

本文基于积分几何中的**柯西-克罗夫顿公式**（Cauchy-Crofton formula），提出了一种简洁的解决方案：**在包围盒内均匀采样定向射线，收集每条射线与曲面的所有交点**。理论保证（Theorem 1）表明，当射线均匀分布时，所有交点的集合在曲面上服从均匀分布。

该方法的关键因果调控变量是**交点选择策略**——保留所有交点（而非仅保留一个），这是确保均匀性的决定性因素。采样点通过修改的球体追踪算法直接交于零水平集，严格位于曲面上，无需额外投影。

### 方法定位

该方法属于**基于射线投射的隐式曲面采样**范式，与现有方法的关系如下：
- 相比**拒绝采样**：同为白噪声采样器，但效率提升数十倍；
- 相比**Marching Cubes采样**：无需显式网格中间表示，保持连续曲面的精确性；
- 相比**MCMC方法**：生成独立同分布样本，无需投影，无样本间相关性。

方法仅需**射线-曲面求交**作为唯一子程序，适用于任何具备该能力的隐式表示（有符号距离场、神经隐式函数、解析隐式等）。

### 主要结果

在114个网格隐式函数数据集（MPZ14）上：
- **均匀性**：总变差分数（TV）达到0.372，与真实网格采样的0.373相当；
- **效率**：函数评估次数仅为拒绝采样的**4.8%**，为Marching Cubes（1024³网格）的**1.8%**；
- **通用性**：方法在神经隐式曲面、非流形几何、开放边界、偏移曲面等多种表示上均有效，并可支持蓝噪声采样、曲率重要性重采样、形状量估计等下游应用。

方法的局限性包括：对极薄稀疏特征效率下降；依赖已知的Lipschitz常数；对二值占用场等硬表面表示难以高效追踪。

## 背景与动机

### 隐式曲面的兴起与基本操作的缺失

隐式曲面——将三维形状的几何信息编码为标量函数的零水平集——已成为计算机图形学与视觉中的核心几何表示。从经典的符号距离函数（SDF）到近年兴起的神经隐式场（如SIREN、NeuS），隐式表示因其连续、可微、拓扑灵活的特性，在形状重建、插值与变形等任务中展现出显著优势（Figure 1）。然而，一个看似基础的操作——在隐式曲面上生成**严格均匀分布**的随机采样点——至今仍缺乏高效、准确的通用解决方案。

均匀白噪声采样是众多下游应用的“原材料”：蓝噪声生成、曲率驱动的重要性重采样、神经隐式形变、基于采样的重建正则化，乃至表面积、体积、质心等基本形状量的估计（Figure 1, Figure 2）。当这一基础操作本身存在系统性偏差或效率瓶颈时，整个应用链条的质量都将受到影响。

### 现有方法的根本性困境

当前在隐式曲面上进行均匀采样主要依赖三类策略，每一类都面临难以调和的权衡：

**拒绝采样（Rejection Sampling）**：在包围域内随机生成候选点，仅保留位于曲面上的点。该方法在理论上保证均匀性，但效率极低——对于复杂形状，绝大多数候选点被丢弃，函数评估成本与曲面面积成反比。在114个网格隐式函数数据集上的实验表明，拒绝采样生成50,000个样本需进行约$3.98 \times 10^8$次函数评估（Table 1）。

**网格提取采样（Marching Cubes-based Sampling）**：通过等值面提取算法（如Marching Cubes，Lorensen and Cline, 1998）在规则网格上构建显式网格，再在网格上采样。该方法引入双重误差：网格分辨率受限时，提取的曲面会丢失几何细节（Figure 13）；即便高分辨率网格，提取过程本身也会引入偏离真实曲面的近似误差，且采样点需额外投影步骤才能精确位于隐式曲面上。在$1024^3$网格分辨率下，该方法仍需约$1.07 \times 10^9$次函数评估（Table 1）。

**马尔可夫链蒙特卡洛（MCMC）**：如Chiu（MIT硕士论文，2022）提出的哈密顿蒙特卡洛方法，通过随机游走生成曲面上的样本链。该方法面临三个固有问题：样本间存在相关性，破坏白噪声假设；采样仅能接近曲面，需额外非平凡投影步骤才能获得精确的曲面点（Figure 3）；样本链中会出现重复样本，虽为正确统计所需，但增加了后处理复杂度。

### 核心瓶颈的提炼

上述方法的共同困境可归结为一个根本性瓶颈：**在缺乏显式参数化的隐式曲面上，直接生成严格位于曲面且相互独立的均匀随机点，需要一种既能保证均匀性、又能避免冗余评估的采样机制**。拒绝采样浪费大量评估于空区域，网格方法将连续问题离散化而引入近似误差，MCMC则牺牲了样本独立性。

### 本文的动机与核心洞察

本文的核心动机源于积分几何中一个优雅的经典结果——**柯西-克罗夫顿公式（Cauchy-Crofton formula）**：曲面的面积与随机直线与曲面交点数的期望成正比。这一公式暗示了一条截然不同的技术路径：如果我们能够均匀采样穿过包围盒的随机直线（射线），并收集每条射线与曲面的**所有**交点，那么这些交点集合将自然构成曲面上的均匀分布。

这一洞察的关键在于：它将“在曲面上采样点”的问题转化为“在空间中采样射线并求交”的问题，而后者恰好是隐式曲面渲染中已高度成熟的球体追踪（sphere tracing）算法所能高效完成的任务。换言之，该方法将采样问题重新表述为**射线投射（ray casting）这一唯一必需子程序**，适用于任何具备射线-曲面求交能力的隐式表示。

基于此洞察，本文提出了一套完整的均匀曲面采样框架，其核心创新在于：(1) 保证射线在包围盒内均匀分布的原点采样策略（Figure 5, Figure 6）；(2) 保留每条射线所有交点（而非仅保留一个）的“全交点”策略，这是保证均匀性的关键设计选择（Figure 7）；(3) 可选的稀疏体素分层采样加速机制（Figure 9）。实验表明，该方法在均匀性上可与拒绝采样媲美（TV分数0.372 vs. 0.373），而函数评估次数仅为拒绝采样的4.8%（Table 1）。

## 核心创新

本方法的核心创新在于将**基于积分几何的连续均匀采样理论**转化为一个**纯射线投射的实用算法**，从根本上绕开了隐式曲面采样中长期存在的效率-均匀性困境。其关键设计体现在三个紧密耦合的“变更槽”（changed slots）上。

### 1. 交点选择策略：从“保留一个”到“保留所有”

传统基于射线的采样方法（或直觉做法）通常对每条射线仅保留一个交点（例如随机选取或仅取首个交点），但这会**系统性地破坏均匀性**。本方法的关键洞察是：**必须保留每条射线与曲面的所有交点**。

这一选择直接源于柯西-克罗夫顿公式（Cauchy-Crofton formula）的几何本质——均匀采样定向直线并收集所有交点，等价于在曲面上进行均匀采样。消融实验（Figure 7）明确证实了这一点：在折线上，“保留所有交点”（keep all）策略的TV分数与真实均匀采样相当，而“保留一个交点”（keep one）策略则产生明显更差的TV分数。这一设计是方法均匀性保证的**理论基石**。

### 2. 射线原点采样：从“盒内随机”到“垂直平面均匀采样”

生成均匀分布的射线并非简单地在包围盒内随机选取原点。如图6所示，若直接在包围盒内随机选择原点，射线会**过度集中于包围盒中心区域**，破坏射线分布的均匀性。

本方法采用了一种正确的采样策略：首先在单位球上均匀采样射线方向，然后在**垂直于该方向的平面上**均匀采样原点，并通过拒绝采样仅保留与包围盒相交的射线（Algorithm 1, Figure 5）。这保证了穿过包围盒的射线集合在积分几何意义下是均匀的，从而为后续交点收集提供正确的统计基础。

### 3. 曲面投影：从“需额外投影”到“直接位于曲面”

现有方法（如拒绝采样、Marching Cubes采样、Hamiltonian Monte Carlo采样）生成的采样点通常**仅是近似位于曲面上**，需要额外的投影步骤（如牛顿法）才能精确移动到零水平集。这不仅增加计算开销，还可能引入偏差。

本方法通过**修改后的球体追踪算法**（Algorithm 2）直接找到射线与零水平集的精确交点，采样点**天然位于曲面上**，无需后处理投影。该算法利用隐式函数的Lipschitz条件（$| f ( p _ { 1 } ) - f ( p _ { 2 } ) | \leq \lambda \| p _ { 1 } - p _ { 2 } \| _ { 2 }$）保证步长安全，并从经典“仅找首个交点”扩展为“找到所有交点”。这一设计消除了投影误差源，同时简化了采样管线。

### 创新的协同效应

上述三个变更槽并非孤立存在，而是形成了一个**逻辑闭环**：
- 正确的射线原点采样保证了射线分布的均匀性（积分几何前提）；
- 保留所有交点保证了均匀性从射线传递到曲面样本（理论完备性）；
- 直接在曲面上定位交点消除了投影带来的误差和额外计算（实用可靠性）。

这一协同设计使得方法在114个网格隐式函数数据集上，以**仅拒绝采样4.8%的函数评估次数**（$1.92\times 10^7$ vs $3.98\times 10^8$），达到了**与真实网格采样相当的均匀性**（TV 0.372 vs 0.373，Table 1）。

## 整体框架

本方法的核心流水线由三个关键模块串联构成，将“在隐式曲面上生成均匀白噪声样本”这一目标转化为一个无需显式网格表示、无需投影步骤的纯射线求交过程。

### 模块一：均匀射线生成

给定一个包围隐式曲面的立方体 $[-1,1]^3$，该模块负责生成一组在空间中均匀分布的定向射线。其关键设计在于避免朴素采样导致的射线密度非均匀性——若直接在包围盒内随机选取射线原点，射线会过度集中于包围盒中心区域（见 Figure 6）。为解决此问题，算法采用两步策略：

1. **方向采样**：在单位球面上均匀采样射线方向 $\vec{d}_i$。
2. **原点采样**：在垂直于 $\vec{d}_i$ 的平面上均匀采样原点，并通过拒绝采样仅保留那些与包围盒相交的射线（见 Figure 5 及 Algorithm 1）。具体而言，在由法向 $\vec{n}_i$ 和副法向 $\vec{b}_i$ 张成的平面上，仅接受其发射射线与包围盒相交的点（即该平面上包围盒的正交投影区域）。

该模块的输出是一组在包围盒内均匀分布的射线集合，为后续交点采集提供了严格的均匀性保证。

### 模块二：全交点球体追踪

对于每条生成的射线，本模块使用修改后的球体追踪算法找到其与隐式曲面零水平集的**所有**交点，而非仅第一个交点。这是整个方法均匀性成立的核心操作槽位：若每条射线仅保留一个交点（如随机选取一个），将破坏样本在曲面上的均匀分布，导致总变差（TV）分数显著恶化（见 Figure 7）。

算法依赖于隐式函数 $f$ 满足 Lipschitz 条件 $|f(p_1) - f(p_2)| \leq \lambda \|p_1 - p_2\|_2$（$\lambda > 0$），以确保步长安全。当函数不具备此边界时，需回退到密集步进或专门搜索。修改后的追踪算法从射线进入包围盒处开始，迭代推进直至射线离开包围盒，沿途记录所有与零水平集的穿越点。这些交点**直接位于曲面上**，无需额外的牛顿投影步骤，这与需要投影的基线方法（如拒绝采样、Marching Cubes 采样、Hamiltonian Monte Carlo）形成鲜明对比。

### 模块三：可选稀疏体素分层

为进一步加速采样并降低估计方差，方法可选地引入稀疏体素结构。将包围盒划分为体素网格后，每个体素内的子曲面可视为具有开放边界的独立隐式曲面，方法可在每个体素内独立应用均匀射线采样（见 Figure 9）。这一分层采样策略带来双重收益：

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2506_05268/figures/008_Figure_9.jpg]]
*Figure 9: Sparse voxel structures can accelerate our method and act as a form of stratified sampling which reduces variance for estimations of shape quantities as described in Section 6.2. Here we show one instance of such a voxel structure with a voxel grid resolution of 16, along with a zoom-in view of one voxel, a set of sampled rays (orange) in this voxel, and the resultant samples on the zero level set (white). We plot the variance of a surface area estimate over 30 runs using sparse voxel structures built with different grid resolutions, which demonstrates the variance-reducing benefits of stratified sampling through voxels. We also plot the total time needed (in seconds) for our method across...*

- **加速**：通过跳过不包含曲面的空体素，减少无效射线求交。
- **降方差**：分层采样降低了表面积等形状量估计的方差（Figure 9 展示了不同体素分辨率下方差与总耗时的变化）。

### 输入输出流

- **输入**：一个隐式曲面表示（零水平集函数 $f$），仅要求能进行射线求交；包围盒通常取 $[-1,1]^3$。
- **输出**：曲面上严格均匀分布的白噪声样本点集，可直接作为下游应用的“原材料”，如蓝噪声生成、曲率重要性重采样、神经隐式变形、形状量估计等（见 Figure 1 概览）。

整个流水线避免了显式网格提取、拒绝采样的大规模浪费或 MCMC 的投影误差，将均匀采样问题归结为“均匀射线 + 全交点收集”这一简洁的积分几何框架。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2506_05268/figures/017_Figure_14.jpg]]
*Figure 14: White noise sampling can be straightforward with mesh surfaces, but offset surface sampling is often non-trivial unless converted to an implicit surface. Our method can easily sample offset surfaces, along both positive and negative directions, in addition to the surface defined at the zero level set*

## 核心模块与公式推导

### 均匀射线生成（Uniform Ray Generation）

该模块的目标是在包围盒内生成均匀分布的定向射线集合。直接采样射线原点容易导致射线密度向包围盒中心聚集（Figure 6），因此方法采用两步策略：

1. **方向采样**：在单位球面上均匀采样射线方向 $\vec{d}_i$。
2. **原点采样**：在垂直于 $\vec{d}_i$ 的平面上，通过拒绝采样选择那些发出的射线与包围盒相交的原点。具体而言，在由法向 $\vec{n}_i$ 和副法向 $\vec{b}_i$ 张成的平面上的一个边长为 $2\sqrt{3}$ 的正方形区域内均匀采样，仅保留其射线与包围盒相交的点（Figure 5 绿色区域）。

这一过程保证射线在包围盒内均匀分布，是后续均匀曲面采样的理论基础（Algorithm 1）。

### 全交点球体追踪（All-Intersections Sphere Tracing）

传统球体追踪（sphere tracing）仅寻找射线的第一个交点。本方法对其进行了关键修改（Algorithm 2），以找到射线与零水平集的**所有交点**：

- **核心前提**：隐式函数 $f$ 满足 Lipschitz 条件，即存在常数 $\lambda > 0$，使得：
  $$| f(p_1) - f(p_2) | \leq \lambda \| p_1 - p_2 \|_2$$
  该条件保证了以 $|f(p)|/\lambda$ 为步长沿射线前进时不会穿透曲面。

- **全交点策略**：在找到第一个交点后，算法继续沿射线方向以微小步长推进，越过当前交点后重新启动球体追踪，从而依次发现所有后续交点。所有交点被直接保留，采样点严格位于曲面上，无需额外的投影步骤（如牛顿法）。

这一修改是方法均匀性的关键：**保留所有交点**（keep all）而非仅保留一个交点（keep one），是保证采样点集在曲面上均匀分布的核心操作（Figure 7 消融实验证实，keep one 策略的 TV 分数显著劣于 keep all）。

### 可选稀疏体素分层（Sparse Voxel Stratification）

为进一步降低估计方差并加速采样，方法引入了稀疏体素结构（Figure 9）：

- 将包围盒划分为稀疏体素网格（如分辨率 $16^3$），仅对包含曲面的体素进行射线采样。
- 每个体素内的子曲面具有开放边界，方法可独立应用于每个体素，天然形成分层采样（stratified sampling）。
- 分层采样显著降低了表面积等形状量估计的方差，同时避免了在空白区域浪费函数评估。

### 核心公式：均匀性度量与形状量估计

**总变差（Total Variation, TV）分数**用于量化采样点集的均匀性。将曲面划分为离散面片（如网格三角形），TV 定义为：
$$\mathrm{TV} = \frac{1}{2} \sum_i \left| \frac{n_i}{N} - \frac{A_i}{A_{\mathrm{total}}} \right|$$
其中 $n_i$ 为落在面片 $i$ 上的样本数，$N$ 为总样本数，$A_i$ 为面片 $i$ 的面积，$A_{\mathrm{total}}$ 为曲面总面积。TV 值越低表示样本分布越均匀。

**表面积估计**基于柯西-克罗夫顿公式的蒙特卡洛积分。当射线数量 $M \to \infty$ 时：
$$A = \lim_{M \to \infty} \frac{12K}{M}$$
其中 $K$ 为所有射线与曲面交点的总数。Figure 11 的实验验证了平均每条射线的交点数与真实表面积之间的线性关系，为该公式提供了实证支持。

**体积与质心估计**同样基于射线弦长。体积的蒙特卡洛估计为：
$$V = \lim_{M \to \infty} \frac{6}{M} \sum_{i=1}^{M} \sigma_i$$
其中 $\sigma_i$ 为第 $i$ 条射线在物体内部的弦长总和。体积质心则通过弦的中点加权弦长进行估计：
$$\mathbf{c}_{\mathrm{solid}} = \frac{1}{V} \int \mathbf{x} d\mathbf{x} = \frac{\displaystyle \sum_{i=1}^{M} \sum_{j \in \mathcal{C}_i} \frac{\sigma_{ij}}{2} (\mathbf{a}_{ij} + \mathbf{b}_{ij})}{\displaystyle \sum_{i=1}^{M} \sum_{j \in \mathcal{C}_i} \sigma_{ij}}$$
其中 $\mathcal{C}_i$ 为射线 $i$ 在物体内部的弦段集合，$\mathbf{a}_{ij}$ 和 $\mathbf{b}_{ij}$ 为弦段的两个端点，$\sigma_{ij}$ 为弦长。

**收敛性改进**：使用低差异序列（low-discrepancy sequence）替代均匀随机采样射线，可使表面积估计误差的收敛速度从 $O(N^{-1/2})$ 提升至 $O(N^{-2/3})$（Figure 16）。

## 实验与分析

### 核心定量结果

实验在 **MPZ14 网格数据集**（114 个形状）上系统评估了所提方法与三种基线方法的均匀性与效率。评估指标为 **总变差分数**（Total Variation, TV）和 **隐式函数评估次数**。TV 分数定义如下：

$$\mathrm { T V } = \frac { 1 } { 2 } \sum _ { i } \left| \frac { n _ { i } } { N } - \frac { A _ { i } } { A _ { \mathrm { t o t a l } } } \right|$$

该指标衡量样本集在网格各三角形上的分布与真实面积分布的偏差，值越低表示均匀性越好。效率指标统一采用函数评估次数而非运行时间，以消除实现差异和并行化影响。

**Table 1** 汇总了在 114 个形状上采样 50,000 个点的平均表现：

- **均匀性**：所提方法平均 TV 为 **0.372**，与真实网格直接采样的 0.373 几乎一致，证明其生成的样本集具有严格的均匀分布特性。拒绝采样虽也达到 0.373，但代价极高。
- **效率**：所提方法平均函数评估次数为 **1.92×10⁷**，仅为拒绝采样（3.98×10⁸）的 **4.8%**，为 Marching Cubes 网格采样（1024³ 分辨率下约 1.07×10⁹）的 **1.8%**。这意味着在同等均匀性下，所提方法将计算成本降低了一到两个数量级。
- **Hamiltonian Monte Carlo**（Chiu 2022）在均匀性和效率上均显著劣于所提方法，且需要额外的牛顿投影步骤才能将采样点精确置于曲面上。

**Figure 10** 进一步展示了在 8 个形状子集上，随着采样点数从 5,000 增加到 50,000，所提方法在 TV 距离和函数评估次数两个维度上均一致优于 HMC 和拒绝采样，且优势随样本量增大而保持稳定。

### 消融实验

**保留所有交点 vs. 保留单个交点**（Figure 7）：若每条射线仅保留一个交点（“keep one”策略），TV 分数显著恶化。这是因为单交点策略破坏了射线采样与曲面面积之间的比例关系，导致密度较高的曲面区域被欠采样。保留所有交点（“keep all”）是保证均匀性的关键设计选择。

**稀疏体素分层采样**（Figure 9）：引入稀疏体素结构后，方法获得两重收益：
1. **方差降低**：在相同射线数量下，表面积估计的方差随体素分辨率提高而下降，验证了分层采样的方差缩减效果。
2. **加速**：总运行时间随体素分辨率提高而缩短，因为体素结构减少了无效的射线-空区域求交计算。

**低差异序列采样**（Figure 16）：将均匀随机射线替换为低差异序列后，表面积估计误差的收敛速度从 $O(N^{1/2})$ 提升至约 $O(N^{2/3})$，与理论预期一致。这为需要高精度几何量估计的应用提供了进一步优化的路径。

### 方法适用性与边界

**非流形与开放边界**（Figure 8）：方法仅要求隐式函数定义余维数为 1 的曲面，对非流形连接处和开放边界无需特殊处理。在由无符号距离函数级联构成的帆船模型上，白噪声采样自然覆盖了所有几何特征。

**偏移曲面采样**（Figure 14）：通过修改零水平集的值，方法可直接在正/负偏移曲面上生成均匀样本，无需额外算法改动。

**多种隐式函数验证**（Figure 12）：方法在神经隐式曲面（NeuS、SIREN）、解析隐式曲面（Möbius 变换、旋转曲面）、插值隐式曲面（不同椅子间的平滑过渡）以及初步的高斯泼溅场景上均展示了稳定的采样质量。

### 形状量估计

基于射线-曲面相交的积分几何原理，方法可自然地估计表面积、体积、曲面质心和体积质心（Figure 15）。**Figure 11** 验证了每射线平均交点数与真实表面积之间的线性关系，为表面积估计公式提供了实证支持：

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2506_05268/figures/018_Figure_15.jpg]]
*Figure 15: Our method can estimate various shape quantities like surface area, volume, surface centroids, and volumetric centroids, as demonstrated here for this PseudoSDF ShaderToy example of a burger as seen in Figure . ShaderToy PseudoSDF credit to ©Xor (CC BY-NC-SA 3.0)*

$$A = \operatorname* { l i m } _ { M \to \infty } \frac { 1 2 K } { M }$$

其中 $K$ 为总交点数，$M$ 为射线数。体积估计则利用射线在物体内部的弦长：

$$V = \operatorname* { l i m } _ { M \to \infty } \frac { 6 } { M } \sum _ { i = 1 } ^ { M } \sigma _ { i }$$

### 失败模式与局限

**极薄稀疏特征**：当形状包含大量细薄结构时，大多数射线不与几何体相交，导致采样效率下降。**Figure 17** 揭示了总函数评估次数与表面积的正相关关系，表面积越小的形状，无效射线比例越高。

**Lipschitz 常数依赖**：修改的球体追踪算法依赖已知或可估计的 Lipschitz 常数 $\lambda$ 来保证步长安全。对于不满足 Lipschitz 条件的隐式函数，必须回退到密集步进或专门搜索策略，这会增加计算成本。

**硬表面表示**：对于二值占用场等缺乏距离信息的表示，球体追踪无法高效进行，方法适用性受限。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2506_05268/figures/015_Table_1.jpg]]
*Table 1: We compute the average total number of function evaluations to sample 50,000 points on a dataset of surfaces [MPZ14], as well as the total variation (TV) score measuring the uniformity of the samples. Although our method is generally aimed at implicit surfaces, we use meshes here for the sake of known geometry to evaluate against. For marching cubes, the grid size is 10243. The total variation “Ground truth” refers to uniform sampling using the ground truth mesh, for which we use the average score across 10 sampling runs for each shape*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2506_05268/figures/020_Figure_16.jpg]]
*Figure 16: We plot the absolute surface area estimation error with samples acquired from sampled rays using a low-discrepancy sequence as proposed in [LYZ∗06, LYZ∗10], as well as uniformly sampled rays, as described in Section 4.1. We also plot asymptotes O ( $N ^ { \frac { 2 } { 3 } }$ ) and O ( $N ^ { \frac { 1 } { 2 } }$ ) , and observe that using the low-discrepancy sequence results in faster convergence, as pointed out in [LYZ∗06]

## 方法谱系与知识库定位

### 1. 方法谱系：从拒绝采样到积分几何

隐式曲面上的均匀采样问题长期受困于一个根本性的效率-精度权衡。传统方法谱系可沿两条轴线梳理：**基于域内采样的方法**与**基于显式中介表示的方法**。

**拒绝采样（Rejection Sampling）** 是最朴素的基线：在包围盒内随机生成候选点，仅保留满足 $|f(x)| < \epsilon$ 的样本。这一方法在理论上可保证均匀性（当 $\epsilon \to 0$ 时收敛至曲面的白噪声采样），但其致命缺陷在于**采样效率与表面积/体积比成正比**——对于稀疏或薄片几何体，绝大多数候选点被拒绝，函数评估成本急剧膨胀。在 MPZ14 数据集的 114 个网格隐式函数上，拒绝采样为获得 50,000 个曲面样本平均需要 $3.98 \times 10^8$ 次函数评估（Table 1），这使其在神经隐式等评估昂贵的场景中几乎不可用。

**基于 Marching Cubes 的采样**（Lorensen and Cline, 1998）代表了另一条路径：先在规则网格上提取显式三角网格，再在网格上均匀采样。该方法的采样效率高（网格采样本身是 $O(1)$ 的），但存在两个结构性缺陷。其一，**网格分辨率决定了几何保真度的上限**——即使在 $1024^3$ 的高分辨率下，提取的网格仍可能遗漏细薄结构（Figure 13），从而破坏采样的均匀性。其二，**网格提取本身极其昂贵**：在 $1024^3$ 网格上执行 Marching Cubes 需要 $1.07 \times 10^9$ 次函数评估（Table 1），远超本文方法。

**哈密顿蒙特卡洛方法**（Chiu, Master's thesis, MIT 2022）代表了一类基于动力系统的采样尝试。该方法通过在曲面附近构造保测度的哈密顿动力学来生成样本，但其内在局限在于**样本仅分布在曲面附近而非严格在曲面上**（Figure 3 左切片），需要额外的牛顿投影步骤才能获得曲面上的点集。这一投影不仅引入误差，还破坏了均匀性保证。

本文方法的关键突破在于**绕过上述权衡**：基于积分几何中的柯西-克罗夫顿公式（Cauchy-Crofton formula），将曲面均匀采样问题转化为**均匀定向射线与曲面求交**的问题。这一理论框架使得方法天然具备以下优势：
- **无需投影**：球体追踪直接交于零水平集，采样点严格位于曲面（Section 4.2, Algorithm 2）；
- **无需显式网格**：直接操作隐式函数，几何保真度仅受限于函数本身的精度；
- **效率与表面积成正比**：函数评估次数与表面积线性相关（Figure 11），而非与体积相关。

### 2. 关键设计决策的消融证据

方法的核心设计决策围绕两个“槽位”展开，消融实验提供了清晰的因果证据。

**槽位一：交点选择策略——“保留所有交点” vs “保留一个交点”**

这是决定均匀性的关键设计。直觉上，每条射线保留一个随机交点似乎更高效，但 Figure 7 的消融实验表明：在折线（polyline）上，“keep one”策略产生的 TV 分数显著劣于“keep all”策略。原因在于，**射线与曲面的交点数与曲面的局部几何复杂度相关**——仅保留一个交点会系统性地欠采样复杂区域、过采样简单区域，破坏均匀性。保留所有交点是保证样本集为白噪声（即 $k$-等分布序列，Section 3.1）的必要条件。

**槽位二：射线原点采样——“垂直平面均匀采样” vs “包围盒内随机采样”**

射线原点的采样方式直接影响射线在包围盒内的分布密度。若直接在包围盒内随机选择原点，射线会过度集中穿过包围盒中心区域（Figure 6 中左），导致曲面采样不均匀。本文采用的方法（Algorithm 1, Figure 5）是：先均匀采样方向 $\vec{d}_i$，再在垂直于 $\vec{d}_i$ 的平面上均匀采样原点，并通过拒绝采样仅保留与包围盒相交的射线。这一设计保证了**射线在包围盒内的密度是均匀的**（Figure 6 右），从而保证了曲面采样的均匀性。

**槽位三：投影需求——“直接位于曲面” vs “需要投影”**

拒绝采样和 Marching Cubes 方法均需额外的投影步骤（如牛顿法 $x \leftarrow x - f(x) \frac{\nabla f(x)}{\|\nabla f(x)\|^2}$）将样本精确移至曲面。本文方法通过修改的球体追踪算法（Algorithm 2）直接找到射线与零水平集的所有交点，采样点天然位于曲面上，消除了投影误差。

### 3. 适用边界与局限

**已知的 Lipschitz 常数依赖**。球体追踪的安全步长依赖于隐式函数的 Lipschitz 边界 $|f(p_1) - f(p_2)| \leq \lambda \|p_1 - p_2\|_2$（Section 4.2）。对于具有已知或可估计 $\lambda$ 的隐式函数（如有符号距离函数、神经隐式等），方法可直接应用。但对于**没有 Lipschitz 边界的隐式函数**，必须回退到密集步进（dense stepping）或专门搜索策略，效率将显著下降。

**稀疏几何体的效率退化**。方法的核心效率指标——函数评估次数——与表面积成正比（Figure 11），这意味着对于**具有极薄稀疏特征的形状**，大多数射线不与几何体相交，导致有效采样率降低。Figure 17（附录 B）展示了这一关系：表面积越小的形状，每射线平均交点数越低，浪费的评估成本越高。

**硬表面表示的挑战**。对于**二值占用场（binary occupancy fields）** 等缺乏邻近信息的表示，球体追踪无法利用距离信息加速，方法需要回退到密集光线步进（ray marching），效率大幅下降。这是方法在更广泛隐式表示上的一个开放问题。

**非流形与开放边界的自然兼容**。值得强调的是，方法对非流形连接处和开放边界天然免疫（Figure 8）——仅要求曲面是余维数为 1 的隐式函数水平集，无需任何拓扑假设。

### 4. 开放问题与扩展方向

论文明确指出了若干未解决的问题：

- **高维扩展**。将方法推广到 4D 及以上维度的曲面采样是理论可行的，但平均弦长公式表明采样效率随维度升高而下降——高维空间中随机射线与曲面相交的概率更低。

- **更紧密的包围体**。当前方法使用轴对齐包围盒进行射线采样，使用更紧密的包围体（如球体、凸包）或支持更快射线采样的基元可进一步提高效率。

- **曲线采样（1D 采样）**。通过随机平面相交来采样曲线是方法的自然对偶问题，尚未被探索。

- **二值场与密度场的适配**。将方法扩展到二值占用场或连续密度表示（如 NeRF 的体积密度）的曲面采样，需要根本性地重新设计求交策略。

- **相交体积估计**。方法在模拟中的相交体积估计等应用场景有待进一步验证。

### 5. 知识库定位

本文方法在计算机图形学与几何处理的工具链中占据一个**基础算子**的位置。它不替代任何下游应用，而是为一系列任务提供高质量的“原材料”（Figure 1）：

- **蓝噪声采样**（Figure 2）：白噪声样本可作为蓝噪声生成器的输入；
- **曲率重要性重采样**：均匀样本可通过重要性重采样转化为曲率自适应的分布；
- **神经隐式变形**（Figure 4）：在插值隐式序列的每一帧上均匀采样；
- **形状量估计**（Figure 15）：表面积、体积、质心等基本几何量的蒙特卡洛估计；
- **重建正则化**：采样点可作为基于采样的正则化项。

与现有方法相比，本文方法在**均匀性-效率 Pareto 前沿**上实现了显著推进：在 MPZ14 数据集上，TV 分数（0.372）与拒绝采样（0.373）相当，但函数评估次数仅为后者的 4.8%（$1.92 \times 10^7$ vs $3.98 \times 10^8$），为 Marching Cubes 的 1.8%（Table 1）。这一效率优势在神经隐式等评估昂贵的场景中尤为关键。

## 原文 PDF

![[paperPDFs/SGP_2025/Uniform_Sampling_of_Surfaces_by_Casting_Rays.pdf]]
