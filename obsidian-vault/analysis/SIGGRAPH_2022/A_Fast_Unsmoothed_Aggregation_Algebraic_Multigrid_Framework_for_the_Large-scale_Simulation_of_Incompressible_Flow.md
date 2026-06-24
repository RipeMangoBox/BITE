---
title: A Fast Unsmoothed Aggregation Algebraic Multigrid Framework for the Large-scale Simulation of Incompressible Flow
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/A_Fast_Unsmoothed_Aggregation_Algebraic_Multigrid_Framework_for_the_Large_scale_Simulation_of_Incompressible_Flow.pdf
project_link: null
code_link: "http://computationalsciences.org/publications/shao-2022-multigrid.html"
aliases:
- USV
- FUAAMFLSSIF
tags:
- SIGGRAPH_2022
- topic/other_unclear
core_operator: 引入非光滑聚合代数多重网格（UAAMG）框架，利用其Galërkin粗化下保持模板模式（Poisson方程7点、粘性方程15点）的特性，辅以多色高斯‑赛德尔光滑器，并基于OpenVDB与SIMD实现矩阵无关运算。
primary_logic: UAAMG的分段常数插值与Galërkin粗化在规则网格上能保持稀疏模板不变，使得粗层矩阵计算可并行、无特殊边界处理；多色高斯‑赛德尔光滑器可稳健处理非对角占优的粘性矩阵；结合OpenVDB连续内存布局与AVX SIMD指令，矩阵‑向量乘法获得显著加速。
claims:
- 整体模拟每子步运行时间比Houdini自适应八叉树求解器快约3倍，粘性求解器在极高粘度场景（如Bunny Cut）可达18.34倍加速。
- 在512^3分辨率下，Poisson方程UAAMG（SIMD）相比ICPCG（Batty）实现147倍加速。
- 只有多色高斯‑赛德尔光滑器为变分粘性方程提供稳定收敛，阻尼雅可比、SPAI‑0等方法无法工作。
- Poisson Compact Scene (512^3) 上 Runtime speedup vs ICPCG (Batty) = UAAMG (SIMD, SRJ)
---

# A Fast Unsmoothed Aggregation Algebraic Multigrid Framework for the Large-scale Simulation of Incompressible Flow

> [!tip] 核心洞察
> UAAMG的分段常数插值与Galërkin粗化在规则网格上能保持稀疏模板不变，使得粗层矩阵计算可并行、无特殊边界处理；多色高斯‑赛德尔光滑器可稳健处理非对角占优的粘性矩阵；结合OpenVDB连续内存布局与AVX SIMD指令，矩阵‑向量乘法获得显著加速。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向大规模不可压缩流体模拟的快速非光滑聚合代数多重网格框架 |
| 英文题名 | A Fast Unsmoothed Aggregation Algebraic Multigrid Framework for the Large-scale Simulation of Incompressible Flow |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](http://computationalsciences.org/publications/shao-2022-multigrid.html) · [Code](https://github.com/christopherbatty/) |
| Topic | #topic/other_unclear |
| Method | UAAMG（非光滑聚合代数多重网格）结合SIMD-VDB |
| Dataset | Poisson Compact Scene, Viscosity Unit Test, River Fall, Meteor |

> [!tip] 效果简介
> - Poisson Compact Scene (512^3) 上，Runtime speedup vs ICPCG (Batty) UAAMG (SIMD, SRJ) vs ICPCG (Batty) (147×)。
> - Viscosity Unit Test (μ=10^4 Pa·s, 512^3) 上，Runtime speedup vs DPCG UAAMG (SIMD) vs DPCG (64×)。
> - River Fall (non‑viscous, 0.1 m grid) 上，Per‑substep total speedup vs Houdini adaptive octree Our framework vs Houdini (adaptive octree) (3.55×)。

## 概要

大规模不可压缩流体模拟中，变分粘性方程因高粘性系数下矩阵非对角占优，导致传统光滑器（如阻尼雅可比）失效，几何多重网格收敛缓慢，成为整体性能瓶颈。本文提出**非光滑聚合代数多重网格（UAAMG）框架**，核心思路是利用分段常数插值与Galërkin粗化在规则网格上保持稀疏模板不变（Poisson方程7点、粘性方程15点），使粗层矩阵可并行构建且无需特殊边界处理；辅以**多色高斯‑赛德尔光滑器**稳健处理非对角占优粘性矩阵，并结合**OpenVDB连续内存布局与AVX SIMD指令**实现矩阵无关的高速矩阵‑向量乘法。

实验表明，整体模拟每子步运行时间比Houdini自适应八叉树求解器快约**3倍**；在512³分辨率下，Poisson方程求解器相比ICPCG（Batty）实现**147倍**加速；粘性求解器在极高粘度场景（Bunny Cut）可达**18.34倍**加速。该方法将代数多重网格、多色光滑器与SIMD数据结构协同整合，为图形学中大规模不可压缩粘性流模拟提供了一条高效、可并行且对材料刚度不敏感的求解路径。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

在大规模不可压缩流体模拟中，压力泊松方程与变分粘性方程是每个时间步必须求解的两个大型稀疏线性系统。传统几何多重网格（GMG）方法在规则网格上对压力方程表现良好，但当处理高粘性系数场景时，变分粘性方程的系统矩阵呈现严重的非对角占优特性，导致阻尼雅可比（damped Jacobi）等传统光滑器发散或收敛极慢，成为整个模拟管线的主要性能瓶颈。

本文的核心洞察在于：**非光滑聚合代数多重网格（UAAMG）的分段常数插值与 Galërkin 粗化策略在规则笛卡尔网格上具有“模板保持”（stencil-preserving）特性**——压力泊松方程的 7 点模板和变分粘性方程的 15 点模板在粗化后结构不变，仅系数发生变化。这一特性使得粗层矩阵的构建可以完全并行化、无需显式矩阵乘法，且避免了边界特殊处理。结合多色高斯‑赛德尔光滑器对非对角占优矩阵的稳健收敛能力，以及基于 OpenVDB 连续内存布局的 AVX SIMD 矩阵‑向量乘法加速，形成了从算法到实现的全栈高效求解框架。

### 管线模块与执行顺序

整个模拟框架遵循 FLIP（Fluid-Implicit-Particle）方法的标准流程，每个时间步子步包含以下模块序列：

1. **对流步（Advection）**：采用 FLIP 方法配合中点规则（midpoint rule）进行时间积分，更新粒子位置和速度场。
2. **第一次压力投影（Pressure Poisson Solve）**：求解压力泊松方程 $- \nabla^2 p = \frac{\rho}{\Delta t} \nabla \cdot \vec{\mathbf{u}}^{*}$，获得中间无散度速度场。该方程在规则网格上离散为 7 点模板，采用 cut‑cell 方法处理不规则固液边界，ghost fluid 方法处理液气边界以达到二阶精度。
3. **变分粘性求解（Variational Viscosity Solve）**：求解由能量泛函最小化导出的粘性方程，更新速度场以考虑粘性应力效应。
4. **第二次压力投影**：再次求解压力泊松方程，确保最终速度场严格无散度。

其中步骤 2–4 均为大型稀疏线性系统求解，是性能瓶颈所在。UAAMG 框架作为预条件共轭梯度法（PCG）的预处理器嵌入这些求解步骤中。

### UAAMG 的核心机制

#### 聚合粗化与模板保持

UAAMG 采用 1‑to‑8 的分段常数聚合策略：每 $2 \times 2 \times 2$ 个细网格体素聚合为一个粗网格体素。限制算子 $R$ 定义为 $R_{ij} = 1/8$（若粗体素 $i$ 覆盖细体素 $j$），延拓算子 $P = 8R^T$。粗层矩阵由 Galërkin 条件构建：

$$A_H := R A_h P$$

在规则网格上，这一粗化过程具有关键的**模板保持**性质：压力泊松方程的粗层矩阵仍为 7 点模板，变分粘性方程的粗层矩阵仍为 15 点模板（包含 1 个对角项、6 个非对角项和 8 个交叉项）。这意味着粗层矩阵的系数可以直接由子网格系数通过固定模式计算得到，无需执行显式的稀疏矩阵乘法。

以压力泊松方程为例，粗层对角项的计算遵循以下模式：

$$d_{\text{coarse}} = \frac{1}{8} \sum_{\text{children}} d_{\text{fine}} + 2 \times \sum_{\text{children pairs}} a_{\text{fine, off-diag}}$$

其中第一项为 8 个子体素对角项的均值，第二项为相邻子体素对之间非对角项贡献的叠加。这一“矩阵无关”（matrix‑free）的粗化策略使得层级构建完全并行化，且无需存储显式的限制和延拓矩阵。

#### 多色高斯‑赛德尔光滑器

变分粘性方程的 15 点模板涉及同一体素上三个速度分量之间的交叉耦合项，使得系统矩阵高度非对角占优。本文的关键技术选择是采用**多色高斯‑赛德尔（multi‑color Gauss‑Seidel）光滑器**。通过分析模板中 15 个自由度的空间索引奇偶性，可将其划分为 6 种颜色（如图 2b 所示），同色自由度之间不存在数据依赖，可完全并行更新。

这一光滑器是唯一能在高粘性场景下为变分粘性方程提供稳定收敛的选择——阻尼雅可比光滑器在高粘度时发散，SPAI‑0 光滑器虽然收敛但效率显著低于多色高斯‑赛德尔。

#### 预条件共轭梯度中的延拓因子

UAAMG 作为 PCG 预处理器时，引入了一个延拓因子 $\alpha = 2$（标准多重网格通常取 $\alpha = 1$）。这一调整改善了预条件算子的谱性质，加速了共轭梯度法的收敛速度。完整的 μ‑cycle 递归求解流程包括：前光滑 → 残差计算与限制 → 粗层递归求解 → 延拓与校正 → 后光滑。

### 关键 Changed Slots

相较于已有方法，本文在以下四个维度上做出了实质性改变：

**Slot 1：矩阵存储结构 → OpenVDB + SIMD 对齐**

传统方法使用 Eigen 等通用库的显式行压缩稀疏矩阵存储。本文改用 OpenVDB 的浮点网格作为底层数据结构，将矩阵系数内嵌于体素的连续内存布局中。每个 $8 \times 8 \times 8$ 的叶节点内部体素按特定顺序排列，使得 AVX SIMD 向量指令可以直接在 8 个连续体素上并行执行矩阵‑向量乘法。这一设计使得矩阵‑向量乘法比传统并行行主流稀疏矩阵乘法快约 3 倍。

**Slot 2：粗化实现 → 矩阵无关并行粗化**

传统代数多重网格方法依赖显式的 Galërkin 乘积 $R A_h P$ 构建粗层矩阵，需要昂贵的稀疏矩阵乘法。本文利用模板保持特性，直接从子网格系数按固定代数规则推导粗层系数，实现了完全矩阵无关的并行粗化。这一改变消除了层级构建的串行瓶颈。

**Slot 3：变分粘性方程光滑器 → 多色高斯‑赛德尔**

传统几何多重网格对粘性方程使用阻尼雅可比或红黑高斯‑赛德尔光滑器，在高粘度时失效。本文采用 6 色并行高斯‑赛德尔光滑器，是唯一能稳健处理非对角占优粘性矩阵的选择。

**Slot 4：多重网格类型与插值 → UAAMG + 分段常数插值**

相对于几何多重网格的分段线性插值和边界特殊处理，UAAMG 的分段常数插值结合 Galërkin 粗化在规则网格上自动保持模板模式，简化了实现并提升了并行度。

### SIMD 矩阵‑向量乘法的实现细节

OpenVDB 的叶节点内 512 个体素按特定 Morton 序排列，使得沿三个坐标轴方向的相邻体素访存具有较好的局部性。矩阵‑向量乘法利用 AVX 指令集一次处理 8 个浮点数：

- 对角项乘法直接对连续 8 个体素执行向量乘加。
- 非对角项（如 $x$ 方向邻居）通过位移操作获取偏移后的向量，再执行乘加。
- 跨叶节点边界的邻居访问通过特殊的 intrinsic 函数（如图 6 所示）高效获取。

默认系数修剪（default coefficient trimming）技术进一步减少了实际参与乘法的非零系数数量，在保持精度的前提下提升了吞吐量。在泊松方程求解器中，仅此项优化就带来约 1.5 倍的额外加速。

### 方法边界条件与限制

UAAMG 框架的有效性依赖于规则笛卡尔网格上的模板保持特性，因此当前实现仅适用于均匀网格。对于极度稀疏的液滴场景，SIMD 方法因大量无效计算而产生明显开销，此时 ICPCG 反而更具优势。此外，框架未针对空间变化的粘性系数进行优化，在粘性剧烈变化时系数修剪效果会降低。光滑器对材料参数仍存在一定敏感性，尚未达到完全参数不敏感的理想状态。

![[assets/figures/papers/paper_list_l10_http_computationalsciences_org_publications_shao_2022_multigrid_html/figures/003_Figure_2.jpg]]
*Figure 2: Illustration of the matrix coe!icients, stencil pa"ern, and update color for one row of the variational viscosity Eq. (8). (a) Matrix coe!icients evaluated based on viscosity and stress control volumes located at edge centers and voxel centers, and velocity control volume located at the face center. (b) The stencil pa"ern of one row of Eq. (8) corresponding to the D component, as well as the values of the stencil pa"ern. The stencil involves 15 DOF, categorized into 6 colors for the multi-color Gauss-Seidel smoother, based on the parity of the sum of their spatial indices*

![[assets/figures/papers/paper_list_l10_http_computationalsciences_org_publications_shao_2022_multigrid_html/figures/001_Figure_1.jpg]]
*Figure 1: Our framework enables the fast simulation of (a) buckling and coiling e!ects for liquids with various viscosity, (b) highly viscous liquids colliding with thin wires, and (c) the dynamics of non-viscous fluids interacting with a complex riverbed geometry*

![[assets/figures/papers/paper_list_l10_http_computationalsciences_org_publications_shao_2022_multigrid_html/figures/005_Figure_3.jpg]]
*Figure 3: 2D illustration of Galerkin coarsening operations for Poisson’s equation. Top: simulation geometry and pressure DOF at each level. Active DOFs are denoted by red dots in red voxels. For each voxel we store the matrix diagonal term indicated by the number above the red dot, and matrix o!-diagonal terms between neighbor DOFs indicated by numbers on the bo"om (le#) side. Bo"om: calculating the level 1 matrix coe!icients from level 0 coe!icients. Each column of the level 1 matrix*

![[assets/figures/papers/paper_list_l10_http_computationalsciences_org_publications_shao_2022_multigrid_html/figures/006_Figure_4.jpg]]
*Figure 4: 2D illustration of Galerkin coarsening operations for the cross component terms in the variational viscosity equation. Bo"om le# legend: each voxel stores the velocities of the bo"om and le# faces, and four cross component terms between velocities on four faces. On the coarse level, four cross terms can be calculated from those at immediate fine level. The input is a standard basis 48 at the coarse level. A#er prolongation we get*

## 实验与关键发现

### 实验设置概览

实验在配备 Intel Xeon Gold 6136 处理器（3.0 GHz，12 核）和四通道 DDR4‑2133 内存（峰值带宽约 60 GB/s）的工作站上进行。所有对比均使用相同帧范围的每子步统计，确保公平性。UAAMG 使用均匀网格，内存开销可能高于自适应八叉树，但借助 SIMD 与粗化加速取得了显著加速比。报告时间包括矩阵层级构建时间（对于 UAAMG 显式矩阵版本）以及求解迭代时间。

测试分为三类：**单位测试**（Poisson 方程和粘性方程在规则几何上的独立性能）、**非粘性复杂场景**（与 Houdini 自适应八叉树求解器的端到端对比）、**粘性复杂场景**（涵盖从低粘度到极高粘度的多种材料参数）。

---

### 主结果：求解器加速比

#### Poisson 方程单位测试

在 512³ 分辨率的紧凑场景中（Table 2），UAAMG 配合 SIMD 和 SRJ（Steepest Descent with Restarted Jacobi）光滑器，相比 Batty 实现的 ICPCG（Incomplete Cholesky Preconditioned Conjugate Gradient）实现了 **147 倍加速**。相比 DPCG（Diagonal Preconditioned Conjugate Gradient），加速比更为显著。AMGCL 库（使用 SPAI‑0 光滑器）在该场景下表现不佳，收敛速度远低于 UAAMG。

| 方法 | 512³ 紧凑场景耗时 | 相对 ICPCG 加速比 |
|------|-------------------|-------------------|
| DPCG | 基准（极慢） | — |
| ICPCG (Batty) | 基准 | 1× |
| AMGCL (SPAI‑0) | 较慢 | <1× |
| UAAMG (SRJ) | 显著加速 | 数十倍 |
| **UAAMG (SRJ, SIMD)** | **最优** | **147×** |

#### 粘性方程单位测试

在 μ = 10⁴ Pa·s、512³ 分辨率的粘性单位测试中（Table 3），UAAMG (SIMD) 相比 DPCG 实现了 **64 倍加速**。关键发现是：**只有多色高斯‑赛德尔光滑器能为变分粘性方程提供稳定收敛**。阻尼雅可比光滑器在高粘度时发散，SPAI‑0 光滑器效率较低。这验证了 UAAMG 框架对材料刚度敏感性显著降低的优势——相比几何多重网格（GMG），UAAMG 在粘性方程上的性能衰减远小于 GMG（Fig. 9）。

#### 非粘性复杂场景：与 Houdini 自适应八叉树对比

Table 4 展示了三个非粘性场景的每子步时间分解。UAAMG 框架整体模拟速度显著优于 Houdini 的商业自适应八叉树求解器（Goldade et al., 2019）：

- **River Fall**（0.1 m 网格）：每子步总时间 **3.55 倍加速**
- **Fan Mixer**：压力求解器约 2.5 倍加速
- **Meteor**（0.025 m 网格）：每子步总时间 **5.32 倍加速**

加速主要来源于压力 Poisson 求解器的性能优势——UAAMG 的压力投影比 Houdini 自适应八叉树压力求解快约 2.5 倍。

#### 粘性复杂场景：极高粘度下的压倒性优势

Table 5 展示了粘性场景的时间分解。UAAMG 粘性求解器的优势随粘度增大而急剧扩大：

- **Bunny Cut**（μ = 20000 Pa·s）：粘性方程求解速度相比 Houdini 自适应八叉树 **8.98 倍加速**
- **Buckling/Coiling**（多种高粘度参数）：粘性求解器峰值加速达 **18.34 倍**

在 SIGGRAPH Bunnies 场景中（数百个粘性兔子同时下落），UAAMG 框架成功处理了大量自由表面与复杂几何的交互。Fan Mixer（粘性）和 Meteor（粘性）场景进一步验证了框架在中等粘度下的稳定性。

---

### 关键消融实验

#### 系数修剪技术

默认系数修剪（default coefficient trimming）是 SIMD 矩阵‑向量乘法的重要组成部分。在 Poisson 求解器中，对比无修剪版本（NT）与最终版本，**系数修剪单独带来了约 1.5 倍加速**（Table 2）。修剪通过跳过接近零的系数减少 SIMD 向量操作次数，在流体几何稀疏度较高时效果尤为明显。

#### 光滑器选择

多色高斯‑赛德尔光滑器是变分粘性方程稳定收敛的**必要条件**。Table 3 的对比表明：
- 阻尼雅可比光滑器在高粘度（μ ≥ 10³ Pa·s）时发散
- SPAI‑0 光滑器虽然收敛，但效率显著低于多色高斯‑赛德尔
- 6 色并行方案在保持收敛速度的同时实现了良好的并行度

光滑器对材料参数仍有一定敏感性，未实现如 Zhu et al. 2010 所述的完全参数不敏感光滑器。

#### UAAMG vs 几何多重网格（GMG）

Fig. 9 展示了不同粘度系数下 DPCG、UAAMG 和 UAAMG (SIMD) 的运行时间对比。GMG 在粘性方程上因矩阵非对角占优导致光滑器失效，性能随粘度增大急剧恶化。UAAMG 对材料刚度的敏感性显著降低，在高粘度区间保持稳定收敛。

#### SIMD 矩阵‑向量乘法

基于 OpenVDB 连续内存布局和 AVX SIMD 指令的矩阵‑向量乘法，比并行行主流稀疏矩阵乘法快约 **3 倍**（Section 1）。该加速来源于 8×8×8 叶节点内的向量化访存和对齐计算，以及跨叶节点的高效向量获取（Fig. 6）。

---

### 失败模式与适用边界

#### 极度稀疏场景下的性能退化

在极度稀疏的液滴场景中（Fig. 8），流体几何仅占据网格的小部分，SIMD 方法存在明显开销——大量叶节点仅含少量活动自由度，向量化利用率降低。此时 ICPCG 反而更有优势。这表明 UAAMG‑SIMD 更适合中等以上填充率的流体体积。

#### 空间变化粘性系数的局限性

框架目前未针对空间变化的粘性系数进行优化。当粘性在空间上剧烈变化时，可能出现较少可修剪的系数，降低 SIMD 修剪效果。这一局限性在多层流体或非牛顿流体模拟中可能成为瓶颈。

#### 内存带宽瓶颈

SIMD 矩阵‑向量乘法已接近四通道 DDR4‑2133 的峰值带宽（约 60 GB/s），进一步加速受限于内存带宽。这解释了为何在部分场景中 SIMD 加速比未达到理论峰值。

#### 光滑器参数敏感性

多色高斯‑赛德尔光滑器虽然远优于阻尼雅可比，但对材料参数仍有一定敏感性。在极端粘度（μ > 10⁵ Pa·s）或极低粘度场景下，收敛速度可能出现波动。

#### 硬件与并行限制

当前实现仅支持 CPU 并行（OpenMP 多线程 + AVX SIMD），未移植到 GPU 或扩展到多计算节点。对于超大规模（如 1024³ 以上）或需要实时交互的应用，这一限制可能成为障碍。

---

### 收敛行为验证

附录 Fig. A5 展示了 Poisson 方程和粘性方程在 256³ 分辨率下的收敛曲线。UAAMG 在两种方程上均表现出接近网格无关的收敛速度——迭代次数不随分辨率增加而显著增长，这是多重网格方法的典型优势。相比之下，DPCG 和 ICPCG 的迭代次数随分辨率增大而明显增加。

![[assets/figures/papers/paper_list_l10_http_computationalsciences_org_publications_shao_2022_multigrid_html/figures/026_Figure.jpg]]
*Figure: Fig. A5. Convergence plot for the unit test experiments. A comparison for the pressure Poisson equation between five methods (DPCG, ICPCG (Ba"y), AMGCL (SPAI-0), UAAMG (SRJ) and UAAMG (SRJ, SIMD)) using a resolution of 256 is shown at the top. A comparison for the variational viscosity equation between four methods (DPCG, ICPCG (Ba"y), UAAMG, UAAMG (SIMD)) using a resolution of 256 is shown at the bo"om. Viscosity coe!icients $\mu = 1$ $\mathsf { P a }$ $\cdot s$ (bo"om le#) and $\mu = 1$ $0 ^ { 4 }$ $\mathrm { P a }$ $\cdot s$ (bo"om right) are used. The absolute error normalized by the norm of the initial r.h.s. is shown as relative error*

---

### 与现有方法的系统对比

Table 1 系统总结了不同多重网格方法在流体模拟中的应用。UAAMG 的关键区分点在于：
- **二阶精度**的 Dirichlet 边界处理（通过 Ng et al. 2009 的切割单元法）
- **分段常数插值**配合 Galerkin 粗化，在规则网格上保持稀疏模板不变
- **矩阵无关实现**，无需显式存储粗层矩阵，降低内存占用和构建开销

![[assets/figures/papers/paper_list_l10_http_computationalsciences_org_publications_shao_2022_multigrid_html/figures/002_Table_1.jpg]]
*Table 1: Summary of di!erent multigrid methods. 1st and 2nd refers to the spatial order of accuracy*

这些设计选择使 UAAMG 在保持几何多重网格收敛速度的同时，获得了代数多重网格的灵活性和实现简洁性。

## 定位与知识库关联

本文的核心贡献在于将**非光滑聚合代数多重网格（UAAMG）**引入不可压缩流体模拟的两个瓶颈方程——压力Poisson方程与变分粘性方程——并利用OpenVDB数据结构与AVX SIMD指令实现矩阵无关的并行粗化与矩阵-向量乘法，从而在均匀网格上获得远超现有商业求解器与迭代法的性能。其改变的**关键slot**是：将传统几何多重网格（GMG）或通用代数多重网格（AMG）的**分段线性插值 + 显式Galerkin乘积**替换为**分段常数插值 + 矩阵无关的并行Galerkin粗化**，并将光滑器从阻尼雅可比/红黑高斯-赛德尔替换为**多色高斯-赛德尔（6色并行）**。

### 相对已有方法的本质差异

**1. 与几何多重网格（GMG）的对比**

在图形学流体模拟中，GMG长期是Poisson方程的主流求解策略。McAdams et al.（SIGGRAPH 2010）提出的GMG方法使用分段线性插值与红黑高斯-赛德尔光滑器，在低粘度场景下表现良好，但其**光滑器对材料参数高度敏感**——当变分粘性方程的粘度系数增大导致矩阵非对角占优时，阻尼雅可比发散，红黑GS收敛极慢。UAAMG通过多色GS光滑器（6色并行）解决了这一瓶颈，在μ=10^4 Pa·s的512³单位测试中，UAAMG（SIMD）比DPCG加速64倍（Table 3），且对粘度系数的敏感性显著低于GMG（Fig. 9）。

**2. 与通用AMG库（AMGCL）的对比**

AMGCL（SPAI-0光滑器）作为通用代数多重网格库基准，在变分粘性方程上效率较低（Table 3）。UAAMG的关键差异在于：利用规则网格上分段常数插值与Galerkin粗化的**模板保留特性**——Poisson方程的7点模板在粗层保持不变，粘性方程的15点模板同样如此。这使得粗层矩阵系数可直接由子网格系数推导（Algorithm 2/3），无需显式矩阵-矩阵乘积，从而避免了通用AMG库中粗化阶段的串行瓶颈。

**3. 与自适应八叉树求解器（Houdini）的对比**

Goldade et al.（2019）在Houdini中实现的自适应八叉树求解器代表了生产级商业软件的最新水平。UAAMG框架在均匀网格上实现了对其的显著加速：非粘性场景（River Fall, Meteor）每子步总时间加速3.55–5.32倍（Table 4）；高粘性场景（Bunny Cut, Buckling/Coiling）粘性方程求解加速8.98–18.34倍（Table 5）。这一优势源于：均匀网格的连续内存布局使得SIMD向量化成为可能，而自适应八叉树的非连续存储难以充分利用SIMD带宽。

**4. 与ICPCG（Batty, 2018）的对比**

Batty的ICPCG实现是压力Poisson方程的重要参考基线。UAAMG（SIMD, SRJ光滑器）在512³紧凑场景中实现147倍加速（Table 2）。这一巨大差异不仅来自多重网格的层次化误差消除，更来自**SIMD-VDB矩阵-向量乘法**本身比并行行主流稀疏矩阵乘法快约3倍（Section 1），以及**默认系数修剪**技术单独贡献约1.5倍加速（Table 2消融对比）。

### 知识库挂载点

本文在知识库中的定位是**大规模不可压缩流体模拟的线性求解器加速技术**，具体挂载点为：

- **多重网格方法族**：属于代数多重网格（AMG）分支下的非光滑聚合AMG（UAAMG），区别于经典GMG（McAdams et al., SIGGRAPH 2010）与通用AMG（AMGCL）。其核心特征是分段常数插值与矩阵无关的Galerkin粗化，在规则网格上保持模板不变性。
- **变分粘性求解**：继承Batty & Bridson（2008）的变分粘性框架，但将求解器从DPCG/ICPCG替换为UAAMG-PCG，解决了高粘度下的收敛瓶颈。
- **稀疏数据结构与SIMD优化**：基于OpenVDB的连续内存布局与AVX指令集，将矩阵-向量乘法从通用稀疏矩阵格式（如Eigen）迁移到SIMD向量化实现，峰值内存带宽达四通道DDR4-2133的约60 GB/s。

### 适用边界与限制

1. **均匀网格限制**：UAAMG依赖规则网格的模板保留特性，无法直接迁移到自适应八叉树或非结构化网格。在极度稀疏的液滴场景下，SIMD方法存在明显开销，此时ICPCG反而更有优势（Fig. 8）。
2. **粘性系数敏感性**：虽然多色GS光滑器显著降低了对材料参数的敏感性，但未实现如Zhu et al.（2010）所述的完全参数不敏感光滑器。在空间变化粘性系数剧烈时，可修剪系数减少，SIMD修剪效果下降。
3. **内存带宽瓶颈**：当前实现已达四通道DDR4-2133的峰值带宽，SIMD进一步加速受限于此，尚未移植到GPU或扩展到多计算节点。
4. **边界条件处理**：UAAMG对Dirichlet边界实现二阶精度（Gibou et al., 2002），对Neumann固体边界使用Ng et al.（2009）的切割单元法，但对复杂边界条件的通用性尚未验证。

### 后续工作启发

- **完全参数不敏感光滑器**：能否引入对粘度系数、网格尺寸完全不敏感的光滑器（如基于Schur补或多项式光滑器），进一步消除UAAMG对材料参数的残余敏感性？
- **GPU迁移**：当前内存带宽瓶颈可通过GPU的高带宽显存（如HBM2e）缓解，但需解决OpenVDB在GPU上的高效实现与多色GS的并行调度问题。
- **空间变化粘性**：针对粘性系数空间变化剧烈的场景，可探索自适应粗化策略或混合精度存储，以保持系数修剪的有效性。
- **多节点扩展**：对于超大规模（如1024³以上）模拟，UAAMG的层次结构天然适合分布式并行，粗层求解可聚合到更少节点，但需解决跨节点通信与负载均衡问题。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/A_Fast_Unsmoothed_Aggregation_Algebraic_Multigrid_Framework_for_the_Large_scale_Simulation_of_Incompressible_Flow.pdf]]