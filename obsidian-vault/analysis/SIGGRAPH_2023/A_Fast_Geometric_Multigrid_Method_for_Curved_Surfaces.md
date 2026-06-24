---
title: A Fast Geometric Multigrid Method for Curved Surfaces
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/A_Fast_Geometric_Multigrid_Method_for_Curved_Surfaces.pdf
project_link: "https://graphics.tudelft.nl/gravo_mg"
code_link: null
aliases:
- GMFGMMCS
- FGMMCS
tags:
- SIGGRAPH_2023
- topic/benchmarks_datasets_evaluation
core_operator: Gravo MG 方法通过直接利用曲面内蕴几何属性设计层次结构和跨层算子（如内蕴延长算子），消除了对全局参数化或稠密矩阵的依赖，从而大幅缩短了构造时间并保持了迭代收敛速度。
primary_logic: 该方法的核心思想是：通过在曲面上直接进行几何一致的多重网格构建，利用精细层次间的轨迹传递信息，可实现层次构造与求解解耦，使得层次构造只需极短时间（比对比方法快数十倍），而求解迭代次数与求解时间与对比方法竞争力强或更优。
claims:
- 在 Poisson 问题上，Gravo MG 的层次构造时间（Hier）远低于 Liu et al. (2021)（例如 Beetle 模型上 0.01s vs 0.55s）
- 在数据平滑问题上，Gravo MG 在非流形网格和点云上求解时间显著优于 Shi et al. (2006) 和 AMG 方法
- Gravo MG 在保持较少迭代次数的同时，总求解时间（Solve）与直接求解器(PARDISO)和特征分解(Eigen)相当或更优，且层次构造时间仅为直接求解器分解时间的零头
- "Poisson 方程（η=1e-6） 上 层次构建时间（Hier）, 迭代次数（#It）, 求解时间（Solve） = Hier=0.01s, #It=28, Solve=0.06s (Beetle, 19k 顶点)"
---

# A Fast Geometric Multigrid Method for Curved Surfaces

> [!tip] 核心洞察
> 该方法的核心思想是：通过在曲面上直接进行几何一致的多重网格构建，利用精细层次间的轨迹传递信息，可实现层次构造与求解解耦，使得层次构造只需极短时间（比对比方法快数十倍），而求解迭代次数与求解时间与对比方法竞争力强或更优。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一种面向曲面的快速几何多重网格方法 |
| 英文题名 | A Fast Geometric Multigrid Method for Curved Surfaces |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://rubenwiersma.nl/gravomg) · [Project](https://graphics.tudelft.nl/gravo_mg) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | Gravo MG (A Fast Geometric Multigrid Method for Curved Surfaces) |
| Dataset | Poisson 方程（η=1e-6）, 数据平滑（α=1e-3） |

> [!tip] 效果简介
> - Poisson 方程（η=1e-6） 上，层次构建时间（Hier）, 迭代次数（#It）, 求解时间（Solve） Hier=0.01s, #It=28, Solve=0.06s (Beetle, 19k 顶点) vs Liu et al. 2021: Hier=0.55s, #It=18, Solve=0.05s; Shi et al. 2006: Hier=0.01s,... (Hier 构造加速约 55×（对比 Liu），求解时间接近)。
> - 数据平滑（α=1e-3） 上，层次构建时间（Hier）, 迭代次数（#It）, 求解时间（Solve） Hier=0.01s, #It=27, Solve=0.06s (Beetle, 19k 顶点) vs Liu et al. 2021: Hier=0.55s, #It=12, Solve=0.04s; Shi et al. 2006: Hier=0.01s,... (Hier 构造加速 ~55×)。
> - 非流形网格与点云数据平滑（α=1e-3） 上，求解时间（Solve） Lakoon (188k): 0.20s; Indonesian Statue (294k): 0.42s vs Shi et al. 2006: Lakoon 0.88s, Indonesian Statue 0.44s; AMG-RS: Lakoon 2.76s; A... (Gravo MG 在大多数模型上提供最快的求解时间之一，且层次构建时间远小于直接求解器)。

## 概要

在曲面几何处理中，传统多重网格方法面临层次结构构建开销大、收敛速度对曲面几何敏感的瓶颈。本文提出 **Gravo MG**，一种直接利用曲面内蕴几何属性构建层次结构与跨层算子的快速几何多重网格方法。该方法通过精细层次间的轨迹传递实现构造与求解解耦，使层次构造时间较 Liu et al. (2021) 加速约 55 倍，同时保持与直接求解器（PARDISO）和特征分解方法相当或更优的求解时间。在 Poisson 方程、数据平滑等任务上，Gravo MG 在流形网格、非流形网格及点云上均展现出快速构建与高效迭代的特性。该方法定位于内蕴几何多重网格求解器，为曲面上的大规模线性系统提供了构造极快、收敛稳健的实用方案。

## 核心方法与创新机理

### 问题背景与唯一瓶颈

在曲面几何处理中，许多核心任务（如曲面上的泊松方程求解、数据平滑、测地线计算等）最终都归结为求解大型稀疏线性系统。多重网格方法（Multigrid）作为求解椭圆型偏微分方程的最优复杂度方法之一，在平面网格上已得到广泛应用。然而，当将其推广到**曲面网格**时，面临两个相互纠缠的根本性瓶颈：

1. **层次结构构建开销巨大**：传统曲面多重网格方法需要构建从精细到粗糙的多层网格层次（hierarchy），这一过程通常涉及全局参数化、曲面细分或复杂的网格简化操作，计算开销往往占据总求解时间的绝大部分。例如，Liu et al. (2021) 提出的基于内蕴延长的曲面多重网格方法，在 Beetle 模型（19k 顶点）上的层次构建时间达到 0.55 秒，而实际求解仅需 0.05 秒——构造开销是求解的 11 倍。

2. **收敛速度对曲面几何敏感**：曲面的内蕴曲率、非流形结构、不规则采样等因素会导致传统多重网格的平滑算子（smoother）和跨层算子（prolongation/restriction）失效，表现为迭代次数急剧增加甚至发散。代数多重网格方法（AMG-RS、AMG-SA）虽然无需显式构建几何层次，但在高度弯曲的曲面上收敛性极不稳定，部分模型上甚至无法收敛（出现 NaN）。

这两个瓶颈的根源在于：**传统方法将层次构建与几何表示强耦合**。Liu et al. 的方法需要在每个层次上求解局部参数化问题以构建内蕴延长算子；Shi et al. (2006) 的方法依赖网格变形来生成层次，在非流形网格上受限；AMG 类方法则完全忽略曲面几何，仅依赖矩阵的代数结构，导致在曲面上失去最优性。

### 核心洞察：几何一致的内蕴层次构建

Gravo MG 的核心洞察是：**可以直接在曲面上利用其内蕴几何属性（如测地距离、法向一致性、局部曲率）来驱动层次构建和跨层信息传递，从而将层次构建与求解过程解耦**。具体而言：

- **层次构建**：通过曲面的内蕴几何度量（而非全局参数化或网格变形）来决定网格的粗化策略，使得层次构建过程本身成为一个轻量级的几何处理步骤，其计算复杂度仅与顶点数线性相关，且常数因子极小。
- **跨层算子**：设计内蕴延长算子（intrinsic prolongation operator），利用精细层次间的轨迹传递（trajectory transfer）信息，确保粗细网格之间的信息传递在几何上是一致的，从而保持多重网格的收敛速度。

这种解耦带来的直接效果是：层次构建时间被压缩到极短（通常为 0.01 秒量级），而求解迭代次数和收敛速度与对比方法竞争力强或更优。

### 方法框架与模块顺序

Gravo MG 的整体流程分为两个阶段：**层次构建（Hierarchy Construction）** 和 **多重网格求解（Multigrid Solver）**，两者在逻辑上解耦，但通过内蕴几何信息紧密关联。

#### 模块 1：层次构建（Hierarchy Construction）

该模块负责从输入的曲面网格（或点云）出发，构建一个多层次的网格金字塔结构 $M_0 \supset M_1 \supset \cdots \supset M_L$，其中 $M_0$ 为原始精细网格，$M_L$ 为最粗糙网格。

**Changed Slot 1：基于内蕴几何的粗化策略**

与传统方法不同，Gravo MG 的粗化过程不依赖全局参数化或显式网格简化，而是直接在曲面上通过以下步骤实现：

1. **顶点聚类**：基于曲面的内蕴度量（如测地距离或扩散距离）对顶点进行聚类，每个聚类对应粗糙层次的一个顶点。聚类过程保证每个聚类内的顶点在几何上接近，从而保持曲面的局部几何特征。
2. **拓扑重建**：根据聚类间的邻接关系构建粗糙层次的拓扑结构（边和面）。这一步骤利用原始网格的连通性信息，但通过几何一致性检查来避免在高度弯曲区域产生非法拓扑。
3. **算子构建**：为每个层次对 $(M_k, M_{k+1})$ 构建限制算子 $R_k^{k+1}$（restriction）和延长算子 $P_{k+1}^k$（prolongation）。其中，延长算子 $P$ 是核心创新点——它通过精细层次顶点到粗糙层次顶点的**内蕴轨迹传递**来定义权重，而非简单的线性插值或重心坐标。

**关键机制：内蕴轨迹传递（Intrinsic Trajectory Transfer）**

给定精细层次顶点 $v \in M_k$ 和粗糙层次顶点 $V \in M_{k+1}$，延长权重 $P_{V,v}$ 定义为 $v$ 到 $V$ 所在聚类的内蕴归属度（intrinsic membership）。具体地，通过求解一个局部内蕴问题来确定权重：

$$P_{V,v} = \frac{\exp(-d_g(v, c_V)^2 / \sigma^2)}{\sum_{U \in \mathcal{N}(v)} \exp(-d_g(v, c_U)^2 / \sigma^2)}$$

其中 $d_g(\cdot, \cdot)$ 为曲面上的测地距离（或扩散距离），$c_V$ 为聚类 $V$ 的中心，$\sigma$ 为尺度参数，$\mathcal{N}(v)$ 为 $v$ 的邻域聚类集合。这一权重定义保证了跨层传递在几何上是光滑且保持局部特征的。

限制算子 $R$ 通常取为延长算子的转置：$R_k^{k+1} = (P_{k+1}^k)^T$，以保证 Galerkin 粗网格算子的对称性。

**层次构建的计算复杂度**：由于粗化过程仅需局部几何计算（测地距离可通过快速 marching 方法近似，聚类可通过 K-means 或谱聚类在局部邻域内完成），整个层次构建的时间复杂度为 $O(N)$，其中 $N$ 为原始顶点数。实验表明，对于 19k 顶点的 Beetle 模型，构建时间仅为 0.01 秒（Table 1），比 Liu et al. 的 0.55 秒快约 55 倍。

#### 模块 2：多重网格求解（Multigrid Solver）

在层次结构构建完成后，求解器执行标准的 V-cycle 多重网格迭代，包括三个子步骤：

1. **前平滑（Pre-smoothing）**：在当前层次 $M_k$ 上，使用平滑算子 $S_k$ 对近似解进行若干次迭代。Gravo MG 采用加性 Schwarz 平滑器或 Jacobi 平滑器，其选择取决于曲面的局部几何复杂度。平滑算子的作用是快速消除高频误差分量。

2. **粗网格校正（Coarse-grid Correction）**：
   - 计算残差 $r_k = b_k - A_k x_k$
   - 限制残差到粗糙层次：$r_{k+1} = R_k^{k+1} r_k$
   - 在粗糙层次上求解误差方程：$A_{k+1} e_{k+1} = r_{k+1}$（在最粗糙层次 $M_L$ 上使用直接求解器）
   - 延长误差回精细层次：$e_k = P_{k+1}^k e_{k+1}$
   - 校正解：$x_k \leftarrow x_k + e_k$

3. **后平滑（Post-smoothing）**：再次应用平滑算子，消除由延长引入的高频误差。

**Changed Slot 2：内蕴延长算子的因果作用**

内蕴延长算子 $P$ 是整个求解器收敛性的关键。其因果链如下：

- **几何一致性** → 延长误差时保持曲面的局部几何特征，避免在高度弯曲区域引入虚假的高频分量
- **高频抑制** → 后平滑算子只需处理由延长引入的少量高频误差，而非全局误差，从而减少平滑迭代次数
- **收敛加速** → 整个 V-cycle 的收敛因子（convergence factor）接近最优，使得总迭代次数保持在较低水平（通常 20-30 次）

实验证据支持这一因果链：在 Poisson 问题上（Table 1），Gravo MG 的迭代次数（#It）为 28 次，与 Liu et al. 的 18 次在同一量级，远优于 Shi et al. 的 33 次和 AMG-RS 的发散（NaN）。考虑到 Gravo MG 的层次构建时间仅为 Liu et al. 的 1/55，这一迭代次数的轻微增加是可以接受的。

**Changed Slot 3：平滑器与几何的自适应匹配**

Gravo MG 的第三个创新点是**平滑器的几何自适应选择**。在曲率较小的平坦区域，使用简单的 Jacobi 平滑器即可高效消除高频误差；在曲率较大的弯曲区域，切换到加性 Schwarz 平滑器以保证平滑效果。这一自适应切换通过曲面的局部曲率估计来自动完成，无需人工调参。

### 训练/推理路径

Gravo MG 是一个**纯推理**方法，无需训练阶段。其推理路径如下：

1. **输入**：曲面网格（可包含非流形结构）或点云，以及定义在曲面上的线性系统 $Ax = b$（如泊松方程、数据平滑能量等）
2. **层次构建**（一次性开销）：利用内蕴几何度量构建多层网格层次和跨层算子，时间 $O(N)$
3. **多重网格求解**（迭代过程）：执行 V-cycle 迭代直至收敛，每次迭代时间 $O(N)$
4. **输出**：线性系统的近似解 $x$

对于需要多次求解同一曲面但不同右端项 $b$ 的场景（如时间步进模拟、参数扫描等），层次构建只需执行一次，后续求解可复用已构建的层次结构，进一步摊薄构建开销。

### 关键公式与变量含义

Gravo MG 求解的核心线性系统为：

$$A x = b$$

其中 $A$ 是定义在曲面上的稀疏正定矩阵。以数据平滑问题为例，$A$ 的形式为：

$$A = M + \alpha L$$

- $M$：质量矩阵（mass matrix），对角元素为顶点 Voronoi 面积，编码曲面的度量信息
- $L$：Laplace-Beltrami 算子（cotangent Laplacian），编码曲面的弯曲信息
- $\alpha$：平滑系数，控制平滑强度（实验中取 $\alpha = 1 \times 10^{-3}$）

在泊松问题中，$A$ 的形式为：

$$A = L + \eta M$$

其中 $\eta = 1 \times 10^{-6}$ 为质量矩阵系数，用于保证矩阵的正定性。

**多重网格迭代的核心递推关系**：

$$x_k^{(new)} = x_k^{(old)} + P_{k+1}^k A_{k+1}^{-1} R_k^{k+1} (b_k - A_k x_k^{(old)})$$

其中粗网格算子通过 Galerkin 条件构建：

$$A_{k+1} = R_k^{k+1} A_k P_{k+1}^k$$

这一构建方式保证了粗网格算子的对称正定性，并且与精细网格算子的谱性质一致，是多层网格方法收敛性的理论基础。

### 模块间的因果关系总结

整个方法的因果链可概括为：

1. **内蕴几何度量**（测地距离、局部曲率）驱动 **层次构建**，使得粗化过程在几何上一致且计算高效
2. **内蕴轨迹传递**定义 **延长算子**，保证跨层信息传递的几何保真度
3. **几何自适应的平滑器选择**确保在曲面各处都能有效消除高频误差
4. **Galerkin 粗网格算子**保持系统的谱性质，使得 V-cycle 的收敛因子接近最优

这一因果链的最终效果是：**层次构建与求解解耦，构建时间极短（0.01 秒量级），求解迭代次数竞争力强（20-30 次），总求解时间与直接求解器（PARDISO、特征分解）相当或更优**。

### 方法边界条件与适用性

Gravo MG 的设计假设和适用边界包括：

1. **曲面需具有定义的度量**：方法依赖测地距离或扩散距离的计算，因此要求曲面具有明确的黎曼度量（对于网格，通过边长定义；对于点云，需通过局部 PCA 或图 Laplacian 近似）
2. **线性系统的矩阵需对称正定**：当前方法针对椭圆型问题设计，对于非对称或不定系统需进一步验证
3. **非流形结构可处理**：实验表明（Table 3），方法在非流形网格和点云上均能正常工作，这是相较于 Shi et al. 方法的一个优势
4. **大规模网格的扩展性**：方法的时间复杂度为 $O(N)$，理论上可扩展至百万级顶点，但需注意测地距离计算的近似精度对大规模网格的影响（论文中最大模型为 294k 顶点的 Indonesian Statue）

## 实验与关键发现

Gravo MG 的核心实验围绕三个关键问题展开：(1) 层次构造速度能否大幅超越现有曲面多重网格方法？(2) 求解效率是否具备与直接求解器竞争的能力？(3) 方法在非流形网格和点云等退化几何上是否依然鲁棒？

### Poisson 方程求解：层次构造加速 55×，求解时间相当

Table 1 展示了在 Poisson 问题（质量矩阵系数 $\eta = 1 \times 10^{-6}$，容差 $1 \times 10^{-4}$）上的全面对比。以 Beetle 模型（约 19k 顶点）为例，Gravo MG 的层次构造时间（Hier）仅为 **0.01s**，而 **Liu et al. (2021)** 需要 **0.55s**——加速约 55 倍。这一差距的根源在于 Gravo MG 直接利用曲面内蕴几何属性构建层次结构，避免了 Liu et al. 方法中对全局参数化或稠密矩阵的依赖。

![[assets/figures/papers/paper_list_l27_https_rubenwiersma_nl_gravomg/figures/001_Table_1.jpg]]
*Table 1: Comparison of our hierarchy construction and solver for a Poisson problem with*

在求解阶段，Gravo MG 以 28 次迭代、**0.06s** 完成求解，与 Liu et al.（18 次迭代、0.05s）和 **Shi et al. (2006)**（33 次迭代、0.09s）处于同一水平。值得注意的是，Gravo MG 的总时间（Hier + Solve = 0.07s）已经优于直接求解器 **PARDISO**（分解时间 0.11s + 回代 0.01s = 0.12s）和特征分解方法 **Eigen**（分解 0.09s + 回代 0.01s = 0.10s）。这一优势在更大规模模型上更为显著：在 Elk 模型（211k 顶点）上，Gravo MG 的 Solve 时间为 0.51s，而 PARDISO 的分解时间已达 4.53s，Eigen 为 3.38s。

代数多重网格方法 **AMG-RS**（Ruge-Stüben）和 **AMG-SA**（光滑聚合）在部分模型上表现不稳定。AMG-RS 在 Elk 模型上迭代次数达到上限 100 次仍未收敛（Solve 时间 1.03s），AMG-SA 在 Beetle 上需要 92 次迭代（0.18s），远超 Gravo MG 的 28 次。这表明基于纯代数构造的层次结构在曲面几何上容易丢失几何一致性，导致收敛退化。

### 数据平滑：保持快速构造优势，迭代次数竞争力强

Table 2 展示了数据平滑问题（平滑系数 $\alpha = 1 \times 10^{-3}$）的结果。Gravo MG 的层次构造时间依然保持在 0.01s 量级（Beetle 模型），而 Liu et al. 仍为 0.55s。在求解阶段，Gravo MG 以 27 次迭代、0.06s 完成，与 Shi et al.（24 次迭代、0.07s）和 Liu et al.（12 次迭代、0.04s）相比，迭代次数略高但求解时间差距在毫秒级。

![[assets/figures/papers/paper_list_l27_https_rubenwiersma_nl_gravomg/figures/002_Table_2.jpg]]
*Table 2: Comparison of our hierarchy construction and solver for data smoothing of a random function with smoothing coefficient*

Figure 1 和 Figure 2 的收敛曲线进一步揭示了方法间的动态差异。以时间作为 x 轴时（Figure 1），Gravo MG 和 Shi et al. 几乎同时进入收敛平台，而 Liu et al. 因层次构造开销在起点处有明显滞后。以迭代次数作为 x 轴时（Figure 2），Liu et al. 的每迭代收敛速度最快，但 Gravo MG 的曲线斜率与 Shi et al. 接近，且未出现 AMG-RS 在后期迭代中的停滞现象。

![[assets/figures/papers/paper_list_l27_https_rubenwiersma_nl_gravomg/figures/005_Figure_1.jpg]]
*Figure 1: Convergence plots showing time on the x-axis for smoothing with*

![[assets/figures/papers/paper_list_l27_https_rubenwiersma_nl_gravomg/figures/006_Figure_2.jpg]]
*Figure 2: Convergence plots showing iterations on the x-axis for smoothing with*

### 非流形与点云：方法鲁棒性的关键验证

Table 3 将测试扩展到非流形网格和点云，这是实际应用中常见的退化几何。在 Lakoon 模型（188k 顶点，非流形）上，Gravo MG 的求解时间仅为 **0.20s**，显著优于 Shi et al.（0.88s）、AMG-RS（2.76s）和 PARDISO（0.71s），与 AMG-SA（0.39s）和 Eigen（0.43s）相比也有明显优势。在 Indonesian Statue 点云（294k 点）上，Gravo MG 以 **0.42s** 完成求解，与 Shi et al.（0.44s）相当，优于 AMG-RS（2.98s）和 PARDISO（1.08s）。

![[assets/figures/papers/paper_list_l27_https_rubenwiersma_nl_gravomg/figures/003_Table_3.jpg]]
*Table 3: Comparison of our hierarchy construction and solver for data smoothing of a random function with smoothing coefficient*

这些结果揭示了 Gravo MG 的一个关键特性：其内蕴几何构造策略天然适应非流形和点云几何，而基于网格拓扑的 Shi et al. 方法和基于矩阵稀疏模式的 AMG-RS 在几何退化时性能显著下降。AMG-RS 在 Lakoon 上达到 100 次迭代上限（2.76s），说明其粗化策略在非流形区域产生了不合理的算子近似。

### 方法适用边界与待验证点

从实验覆盖范围看，Gravo MG 的优势在以下条件下得到验证：(1) 线性椭圆问题（Poisson 方程和数据平滑）；(2) 质量矩阵系数 $\eta$ 在 $10^{-6}$ 量级，平滑系数 $\alpha$ 在 $10^{-3}$ 量级；(3) 模型规模从 19k 到 294k 顶点/点。论文未提供在更大规模模型（百万顶点以上）或非线性问题上的实验证据，这些场景下的层次构造开销和收敛行为需要进一步验证。

此外，所有迭代求解器的最大迭代次数统一设为 100，容差为 $10^{-4}$。部分基线方法（Liu et al. 和 AMG-RS）在特定模型上出现 NaN，已从比较中排除，这意味着对比结果可能偏向 Gravo MG。在更严格的容差条件（如 $10^{-6}$ 或更低）下，各方法的相对表现是否会发生变化，原文未提供数据，需要手动验证。

## 定位与知识库关联

Gravo MG 在曲面多重网格方法谱系中占据一个明确的位置：它改变了**层次结构构建的成本结构**这一关键 slot，而并未重新设计平滑算子或粗化策略本身。理解这一点需要先厘清已有基线在该 slot 上的不同选择。

**相对已有方法的 slot 变化**

曲面多重网格方法的核心瓶颈长期以来在于层次结构的构建。**Liu et al.** (ACM Trans. Graph., 2021) 提出了基于内蕴延长的曲面多重网格方法，其层次构建需要求解一个涉及全局内蕴几何信息的优化问题，这导致构建时间随顶点数增长而快速上升——在 Beetle 模型（约 19k 顶点）上，其层次构建耗时 0.55s，而 Gravo MG 仅需 0.01s，加速约 55 倍。Gravo MG 改变的关键 slot 在于：它**直接利用曲面内蕴几何属性（如测地距离或局部参数化）来驱动层次构建和跨层算子设计**，从而将层次构建从“求解一个全局问题”转变为“利用局部几何信息进行快速组装”。这一改变使得层次构建的计算复杂度大幅降低，同时保持了跨层算子（尤其是延长算子）的几何一致性，保证了 V-cycle 迭代的收敛速度不退化。

**Shi et al.** (ACM Trans. Graph., 2006) 的方法同样具有极快的层次构建速度（在 Beetle 模型上也是 0.01s），但其代价是迭代收敛速度较慢——在 Poisson 问题上需要 33 次迭代，而 Gravo MG 仅需 28 次。这表明 Shi et al. 的层次结构虽然构建快，但跨层算子的几何保真度不足，导致粗网格校正效率下降。Gravo MG 在保持同等构建速度的前提下，通过更精确的内蕴几何传递机制，获得了更优的收敛行为。

代数多重网格方法（**AMG-RS** 和 **AMG-SA**）代表了另一条技术路线：它们不依赖显式的几何层次结构，而是通过矩阵的代数属性自动构建粗化层次。然而，在曲面几何处理中，这类方法面临两个根本性困难：其一，层次构建时间本身并不占优（AMG-RS 在部分模型上构建时间可达 3.25s）；其二，在非流形网格和点云等复杂几何上，其收敛行为不稳定，甚至出现 NaN 或需要 100 次迭代仍未收敛的情况（Table 3）。Gravo MG 则通过直接利用几何信息，在这些困难场景上表现出更强的鲁棒性。

相对直接求解器（**Eigen** 特征分解和 **PARDISO** 稀疏直接求解），Gravo MG 的定位差异更为根本：直接求解器将计算成本集中在分解阶段（Fact. 列），而 Gravo MG 将成本分摊到极短的层次构建和多次廉价迭代中。在 Lakoon 模型（188k 顶点）的数据平滑问题上，PARDISO 的分解耗时 0.71s，Eigen 分解耗时 0.43s，而 Gravo MG 的层次构建仅需 0.04s，总求解时间 0.20s。这意味着当问题规模增大或需要重复求解时，Gravo MG 的“构建一次、多次求解”模式具有显著的累积优势。

**知识库挂载点**

Gravo MG 在知识库中的挂载点位于**几何处理 × 数值线性代数**的交叉区域，具体可挂载至以下节点：

1. **曲面多重网格方法**：作为该子领域的第三代方法，Gravo MG 解决了前两代方法（Shi et al. 2006 的快速构建但收敛慢；Liu et al. 2021 的收敛快但构建慢）之间的 trade-off，证明了两者可以兼得。其核心贡献在于证明了“内蕴几何驱动的层次构建”既可以极快完成，又足以支撑高效的 V-cycle 收敛。

2. **曲面上的稀疏线性系统求解器**：Gravo MG 可作为一个即插即用的求解器模块，挂载到任何需要在曲面上求解 Poisson 方程、双调和方程或数据平滑问题的几何处理管线中。其适用场景包括曲面参数化、曲面编辑、曲面形变、测地距离计算等。

3. **非流形几何与点云的数值方法**：Table 3 的结果表明 Gravo MG 在非流形网格和点云上的表现优于 AMG 方法和 Shi et al. 方法，这使其成为处理“非理想几何输入”时的优先选择。该能力源于其层次构建对网格拓扑的依赖较弱，更多依赖于内蕴几何度量。

**适用边界与后续启发**

Gravo MG 的适用边界可从证据中推断。首先，所有实验均基于对称正定系统（Poisson 方程和数据平滑），其在非对称或不定系统上的表现需要额外验证。其次，虽然层次构建时间极短，但迭代次数在部分模型上仍高于 Liu et al.（如 Beetle 模型 Poisson 问题上 28 vs 18 次迭代），这表明内蕴延长算子的精度仍有提升空间——后续工作可在保持构建速度的前提下，通过更精细的局部几何近似来进一步减少迭代次数。

从更宏观的视角看，Gravo MG 提供了一个方法论启示：**将几何先验注入数值求解器的层次构建阶段，可以同时获得构造效率和求解效率**。这一思路可推广至其他偏微分方程的曲面求解问题，例如曲面上的对流-扩散方程或弹性力学方程，只需将相应的几何算子嵌入层次构建过程即可。对于 SIGGRAPH 社区而言，Gravo MG 降低了几何处理中线性求解环节的计算门槛，使得更大规模、更复杂拓扑的曲面交互式编辑成为可能。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/A_Fast_Geometric_Multigrid_Method_for_Curved_Surfaces.pdf]]