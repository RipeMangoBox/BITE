---
title: A Practical Walk-on-Boundary Method for Boundary Value Problems
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/A_Practical_Walk_on_Boundary_Method_for_Boundary_Value_Problems.pdf
project_link: "https://rsugimoto.net/WoBforBVPsProject/"
code_link: null
aliases:
- WBW
- PWBMBVP
tags:
- SIGGRAPH_2023
- topic/other_unclear
core_operator: 将随机游走从球面改为边界，基于边界积分方程 (BIE) 的第二类 Fredholm 方程，通过光线追踪而非球面采样来进行递归估计。
primary_logic: 边界积分方程与渲染方程在数学上高度相似，使得成熟的光线追踪技术（如 MIS、MCMC）可直接应用于求解 PDE，实现统一的边界值问题求解框架。
claims:
- WoB 无需 ε-shell 近似，可在边界及附近精确求解
- WoB 统一支持 Dirichlet、Neumann、Robin 及混合边界条件，以及内外域问题
- WoB 与光线追踪相似，可轻松集成高级渲染技术
- 内部 Dirichlet 问题在凸/非凸二维域 上 RMSE = WoB (路径长度 M=2~7)
---

# A Practical Walk-on-Boundary Method for Boundary Value Problems

> [!tip] 核心洞察
> 边界积分方程与渲染方程在数学上高度相似，使得成熟的光线追踪技术（如 MIS、MCMC）可直接应用于求解 PDE，实现统一的边界值问题求解框架。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向边界值问题的实用Walk-on-Boundary方法 |
| 英文题名 | A Practical Walk-on-Boundary Method for Boundary Value Problems |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://rsugimoto.net/WoBforBVPsProject/) · [Project](https://rsugimoto.net/WoBforBVPsProject/") |
| Topic | #topic/other_unclear |
| Method | Walk-on-Boundary (WoB) |
| Dataset | 内部 Dirichlet 问题在凸/非凸二维域 |

> [!tip] 效果简介
> - 内部 Dirichlet 问题在凸/非凸二维域 上，RMSE WoB (路径长度 M=2~7) vs WoS (ε-shell 10^{-2}~10^{-7}) (在凸域上相当；在非凸域上 WoS 更高效)。
> - 多种边界条件 (内部 Dirichlet, Neumann, Robin 等) 上，视觉质量 / RMSE WoB (单层/双层势能公式) vs 无直接对比，但展示统一处理能力 (所有问题均收敛至同一真解)。
> - 双向估计器比较 (Dirichlet 问题) 上，等时间噪声水平 MIS 结合后向估计器与下一事件估计 vs 纯后向估计器 (MIS 组合在各设置下均表现鲁棒)。

## 概要

本文针对 Walk-on-Spheres (WoS) 方法的固有缺陷——ε-shell 近似导致边界附近求解存在偏差，且对 Neumann、Robin 等非 Dirichlet 边界条件支持不自然——提出 **Walk-on-Boundary (WoB)** 方法。WoB 将随机游走从球面移至边界表面，基于边界积分方程的第二类 Fredholm 方程，通过光线追踪求交而非球面采样进行递归估计，从而天然避免了 ε-shell 截断误差，并统一支持 Dirichlet、Neumann、Robin 及混合边界条件，适用于内外域问题。该方法与 Monte Carlo 光线追踪在数学形式上高度相似，使多重重要性采样、RIS、MCMC 等成熟渲染技术可直接复用。实验表明，WoB 在边界附近精度显著优于 WoS，在凸域上与 WoS 效率相当，在非凸域上 WoS 更高效；各类边界条件问题均收敛至同一真解。WoB 的路径截断为有偏估计，混合边界问题中的参数选择缺乏理论界限，且多连通域下的收敛性仍有待研究。

## 核心方法与创新机理

### 问题瓶颈：WoS 的 ε-shell 偏差与边界条件局限

Walk-on-Spheres (WoS) 方法通过在域内递归采样球面来求解 Laplace 方程，但其路径终止依赖于 ε-shell 近似——当采样点进入距边界 ε 的壳层时，直接取最近边界点的 Dirichlet 值作为估计。这一机制引入两个根本性缺陷：① 边界附近求解存在固有偏差，ε 越小偏差越小但计算代价急剧增大；② 对 Neumann 和 Robin 边界条件缺乏自然支持，因为 ε-shell 截断仅能利用 Dirichlet 值，无法直接融入法向导数信息。

WoB 的核心洞察在于：边界积分方程 (BIE) 的数学结构与渲染方程高度相似，二者同属第二类 Fredholm 积分方程。渲染方程中，出射 radiance 等于自发光加上对入射 radiance 经 BSDF 加权的球面积分；而 BIE 中，边界上的未知量（源密度或解本身）等于边界条件项加上对自身经核函数加权的边界积分。这一结构同源性意味着，成熟的光线追踪技术——多重重要性采样 (MIS)、重采样重要性采样 (RIS)、马尔可夫链蒙特卡洛 (MCMC)——可直接迁移用于 PDE 求解。

### Changed Slots：三个关键替换

**Slot 1：采样域——从球面到边界表面**

WoS 的每一步在当前位置的最大内切球面上均匀采样下一路径点，路径点始终位于域内部。WoB 则从当前边界点沿随机方向发射射线，取射线与边界的最近交点作为下一路径点，使整条路径完全行走在边界上。这一替换消除了对 ε-shell 的依赖，因为路径天然终止于边界而非内部壳层。

**Slot 2：递归方程形式——从 Volterra 到 Fredholm**

WoS 的递归关系依赖于球面半径这一随位置变化的量，本质上是 Volterra 型方程。WoB 基于 BIE 的第二类 Fredholm 方程，核函数和积分域均为固定边界 Γ，方程形式为：
$$\nu(\mathbf{x}) = \int_{\Gamma} 2 \frac{\partial G}{\partial \mathbf{n}_{\mathbf{y}}}(\mathbf{x}, \mathbf{y}) \nu(\mathbf{y}) dA_{\mathbf{y}} + 2 \overline{u}_D(\mathbf{x})$$
其中 $\nu$ 为双层势能源密度，$G$ 为拉普拉斯算子的基本解，$\frac{\partial G}{\partial \mathbf{n}_{\mathbf{y}}}$ 为核函数。Fredholm 形式保证了谱半径小于 1 时的 Neumann 级数收敛性，为路径截断提供理论基础。

**Slot 3：路径终止条件——从 ε-shell 截断到路径长度 M 截断 + 1/2 修正**

WoB 将路径截断为固定长度 M。在最后一步 $i = M-1$ 时，源密度估计不再递归，而是直接取边界条件项的一半：
$$\hat{\nu}(\mathbf{x}_M) := \overline{u}_D(\mathbf{x}_M)$$
这一 1/2 因子源于 Neumann 级数展开的截断修正：将积分算子记为 $\mathrm{H}$，则 $\nu = (\mathrm{I} - \mathrm{H})^{-1} 2\overline{u}_D = (\mathrm{I} + \mathrm{H} + \mathrm{H}^2 + \cdots) 2\overline{u}_D$。截断至 M 项时，末项需乘 1/2 以保证期望收敛至真解。该方法引入的是有偏估计，但偏差随 M 增大指数衰减。

### 模块架构与推理路径

WoB 的完整推理流程由三个级联模块构成：

**模块 1：光线-边界交点采样 (RayIntersectionSampling)**

从当前边界点 $\mathbf{x}_i$ 出发，按采样策略 $p(\mathbf{x}_{i+1}|\mathbf{x}_i)$ 生成下一路径点。采样策略可为：均匀采样出射方向后求射线与边界的交点；或直接按立体角/面积测度在边界上采样。该模块的输出是边界上的路径点序列 $\{\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_M\}$。

**模块 2：递归估计器 (RecursiveEstimator)**

沿路径反向递归计算边界未知量。以 Dirichlet 问题的源密度 $\nu$ 为例，单步估计为：
$$\hat{\nu}(\mathbf{x}_i) := \frac{2 \frac{\partial G}{\partial \mathbf{n}_{\mathbf{y}}}(\mathbf{x}_i, \mathbf{x}_{i+1})}{\hat{p}(\mathbf{x}_{i+1}|\mathbf{x}_i)} \hat{\nu}(\mathbf{x}_{i+1}) + 2 \overline{u}_D(\mathbf{x}_i)$$
其中分子为核函数值，分母为采样概率密度，二者之比构成重要性权重。递归从 $i=M-1$ 开始，以 $\hat{\nu}(\mathbf{x}_M) = \overline{u}_D(\mathbf{x}_M)$ 初始化，逐步向前传播至 $i=0$ 得到 $\hat{\nu}(\mathbf{x}_0)$。这一递归结构与路径追踪中的递归 radiance 估计完全对应：核函数类比 BSDF，边界条件项类比自发光。

**模块 3：内部/外部解估计**

获得边界源密度估计后，域内任意点 $\mathbf{x} \in \Omega$ 的解通过双层势能积分求得：
$$u(\mathbf{x}) = \int_{\Gamma} \frac{\partial G}{\partial \mathbf{n}_{\mathbf{y}}}(\mathbf{x}, \mathbf{y}) \nu(\mathbf{y}) dA_{\mathbf{y}}$$
在蒙特卡洛框架下，此积分通过从 $\mathbf{x}$ 向边界发射射线采样 $\mathbf{y}$ 来估计，与模块 1 共享光线追踪基础设施。

### 统一边界条件框架的机制

WoB 的统一性源于 BIE 对不同边界条件的表达均归结为第二类 Fredholm 方程（或经变换的第一类方程）。Table 1 总结了各类问题的估计器公式：

- **Dirichlet 问题**：使用双层势能间接 BIE，求解源密度 $\nu$，核函数为 $\partial G/\partial \mathbf{n}_{\mathbf{y}}$。
- **Neumann 问题**：使用单层势能间接 BIE，求解源密度 $\mu$，核函数为 $G$（弱奇异，但可通过变量替换正则化）。
- **Robin 问题**：混合 Dirichlet 和 Neumann 算子，仍可写成第二类 Fredholm 形式。
- **混合边界问题**：在 Dirichlet 边界段，将第一类方程乘以常数 $k$ 转化为第二类形式，保证迭代收敛。

这种统一性使得同一套光线追踪代码可处理所有常见边界条件，无需为每种条件编写独立的采样和求解逻辑。

### 高级采样技术的集成

WoB 与渲染方程的相似性使得三类高级采样技术可即插即用：

1. **多重重要性采样 (MIS)**：同时使用前向估计器（核为 $\partial G/\partial \mathbf{n}_{\mathbf{x}}$）和后向估计器（核为 $\partial G/\partial \mathbf{n}_{\mathbf{y}}$），按平衡启发式组合，降低单一采样策略在特定几何配置下的高方差。
2. **重采样重要性采样 (RIS)**：在混合边界问题中，先用简单分布生成候选边界点，再按目标核函数重采样，有效捕获非零贡献区域。
3. **下一事件估计**：从当前边界点直接采样 Dirichlet 边界段，无递归地累积边界条件贡献，减少随机游走步数带来的方差。

这些技术的因果链为：BIE 与渲染方程的结构同源性 → 核函数类比 BSDF → 采样策略可复用渲染领域的成熟方案 → 方差降低、鲁棒性提升。

### 关键公式的变量含义与因果关系

核心递归式（Eq. 17）中各变量的物理和几何含义：

- $\mathbf{x}_i$：路径上第 $i$ 个边界点，$\mathbf{x}_0$ 为评估点（可在边界或域内）。
- $\mathbf{n}_{\mathbf{y}}$：点 $\mathbf{x}_{i+1}$ 处指向域外的单位法向量。
- $G(\mathbf{x}, \mathbf{y}) = 1/(4\pi r)$：三维拉普拉斯算子的基本解，$r = \|\mathbf{x} - \mathbf{y}\|$。
- $\frac{\partial G}{\partial \mathbf{n}_{\mathbf{y}}} = \frac{(\mathbf{x} - \mathbf{y}) \cdot \mathbf{n}_{\mathbf{y}}}{4\pi r^3}$：核函数，表征 $\mathbf{x}_{i+1}$ 处的源对 $\mathbf{x}_i$ 处场的贡献强度，几何上正比于视线方向与法向夹角的余弦。
- $\hat{p}(\mathbf{x}_{i+1}|\mathbf{x}_i)$：从 $\mathbf{x}_i$ 采样到 $\mathbf{x}_{i+1}$ 的概率密度，用于重要性加权以保持无偏性。
- $\overline{u}_D(\mathbf{x}_i)$：$\mathbf{x}_i$ 处给定的 Dirichlet 边界值。

因果链路：$\mathbf{x}_i$ 处的源密度 $\nu(\mathbf{x}_i)$ 由两部分驱动——来自 $\mathbf{x}_{i+1}$ 的“散射”贡献（核函数加权 × $\nu(\mathbf{x}_{i+1})$）加上本地“自发光”（边界条件 $2\overline{u}_D$）。这一“散射 + 自发光”结构与渲染方程中“反射 radiance + 自发光”完全同构，解释了为何光线追踪技术可无缝迁移。

### 方法边界与未解决问题

当前 WoB 框架存在以下理论和技术边界：

1. **有偏截断**：路径长度 M 截断引入有偏估计，虽可通过增大 M 指数衰减偏差，但缺乏无偏的俄罗斯轮盘赌截断方案。这是 WoB 与成熟路径追踪之间的关键差距。
2. **混合边界参数 $k$**：将第一类方程乘以常数 $k$ 转化为第二类形式时，$k$ 的理论最优值未知，仅通过实验调节，缺乏收敛性保证。
3. **非凸域效率**：在包含细小结构的非凸域上，WoB 的边界行走路径可能需更多步数才能充分探索边界，效率低于 WoS 的球面跳跃。
4. **超奇异核**：求解边界附近梯度时涉及核函数的二阶导数（超奇异），当前估计器噪声较大，需进一步正则化。

![[assets/figures/papers/paper_list_l39_https_rsugimoto_net_WoBforBVPsProject/figures/001_Figure_1.jpg]]
*Figure 1: The walk-on-boundary (WoB) method can handle various boundary value problems including Dirichlet, Robin, Neumann, and mixed for both interior and exterior problems under the same framework based on boundary integral equations. In this experiment, each problem is configured to have the same ground-truth solution (middle), and this figure shows that our WoB estimators all converge to that same solution (left and right)*

![[assets/figures/papers/paper_list_l39_https_rsugimoto_net_WoBforBVPsProject/figures/009_Figure_7.jpg]]
*Figure 7: Results of a WoB solver implemented on top of an MC ray tracing system. WoB’s strong similarity to MC ray tracing makes such an implementation easy to carry out. The images show the estimated solution for interior (top) and exterior (bottom) Dirichlet problems on a cutting plane. WoB can solve both problems efficiently with a unified MC ray tracing solver. Ambient occlusion was computed at the same time as the solution using the same rendering system*

## 实验与关键发现

### 核心实验设计思路

WoB 的实验评估围绕三个核心问题展开：**边界精度**（能否消除 WoS 的 ε-shell 偏差）、**边界条件通用性**（能否在同一框架下处理 Dirichlet、Neumann、Robin 及混合边界条件）、以及**与光线追踪技术的集成能力**（MIS、RIS、MCMC 等是否可自然嫁接）。实验覆盖二维和三维域，包括凸/非凸几何、内外域问题，并与 **WoS**（Sawhney and Crane, 2020）进行直接对比。

### 边界精度：消除 ε-shell 偏差

WoB 最关键的实验证据来自与 WoS 在边界附近的精度对比（Fig. 2）。WoS 依赖 ε-shell 截断，当路径进入距边界 ε 距离的壳层时即终止，这导致解在边界附近产生系统性偏差——图中可见明显的条带伪影（banding artifacts）。WoB 通过直接在边界上采样和递归估计，完全绕开了 ε-shell 近似，在同一区域无此类误差。这一结果直接验证了 WoB 的核心优势：**无需引入与路径终止相关的近似误差**。

![[assets/figures/papers/paper_list_l39_https_rsugimoto_net_WoBforBVPsProject/figures/002_Figure_2.jpg]]
*Figure 2: Unlike WoS, WoB does not introduce any errors associated with the ??-shell path termination. The indicated region (left) displays visible banding artifacts with WoS (middle), where WoB presents no such error (right)*

### 边界条件统一性验证

Fig. 1 是 WoB 通用性的核心视觉证据。实验将同一真解配置为六种不同问题：内部 Dirichlet、内部 Robin、内部 Neumann、混合边界条件、外部 Dirichlet、外部 Robin。所有 WoB 估计器均收敛至该真解，证明了基于边界积分方程（BIE）的框架可统一处理各类边界值问题。这一能力是 WoS 所不具备的——WoS 对 Neumann 和 Robin 条件的支持需要额外处理，且不够自然。

### 定量效率对比：WoB vs. WoS

在凸域和非凸域的 Dirichlet 问题上，论文进行了等时间 RMSE 对比（Fig. 12）。在凸域上，WoB（路径长度 M=2~7）与 WoS（ε-shell 10⁻²~10⁻⁷）的性能相当；但在非凸域上，WoS 的效率更高。这一差异的根源在于：非凸域中光线从内部点出发可能与边界多次相交，WoB 的路径生成效率下降，而 WoS 的球面采样不受几何复杂度同等程度的影响。**这构成了 WoB 的主要适用边界：在非凸或具有细小结构的复杂域中，WoS 仍是更高效的求解器。**

### 路径截断的偏差-方差权衡

WoB 使用固定路径长度 M 截断（末项乘 1/2 修正），而非无偏的 Russian roulette 截断。Fig. 6 的消融实验表明：增加 M 可降低截断误差（偏差减小），但会增加方差。这一权衡是 WoB 实际应用中的关键调参点——M 过小则偏差显著，M 过大则噪声放大。论文指出当前未提供无偏截断方案，这是方法的一个已知局限。

### 双向估计器与 MIS 组合

对于 Dirichlet 问题，WoB 可构建后向估计器（backward estimator）和下一事件估计器（next-event estimator），并通过多重重要性采样（MIS）组合两者。Fig. 10 的等时间对比显示：纯后向估计器在边界值非零区域集中时表现良好，但在边界值分布于中心区域时噪声较大；下一事件估计器则相反。MIS 组合在所有设置下均表现鲁棒，验证了将渲染中的 MIS 技术直接应用于 PDE 求解的有效性。

![[assets/figures/papers/paper_list_l39_https_rsugimoto_net_WoBforBVPsProject/figures/012_Figure_10.jpg]]
*Figure 10: Equal-time comparison of bidirectional WoB estimators. Left to right: purely backward estimator, next-event estimation, and the MIS combination of the two. Top row: non-zero boundary values on each side. Bottom row: non-zero boundary values around the center of each side. Either the backward estimator or next-event estimation is more efficient than the other in each setting. WoB allows us to trivially combine the two estimators via MIS, and the combined estimator is robust across different settings (right)*

### 前向与后向估计器的方差特性

在核函数为 ∂G/∂n_x 的场景下，前向估计器的方差低于后向估计器（Section 4.4.3）。这一发现对实际选择估计器方向具有指导意义：当问题允许使用前向估计器时，应优先考虑以降低方差。

### 混合边界问题的采样挑战与 RIS 解决

混合边界问题（如部分 Dirichlet、部分 Robin）中，纯光线采样策略可能完全错过非零贡献的边界区域。论文采用重采样重要性采样（RIS）对边界进行采样，有效捕获了非零贡献（Section 5）。这一消融实验表明：**WoB 的性能高度依赖边界采样策略的质量**，简单的均匀方向采样在混合边界条件下可能失效，需要引入高级采样技术。

### Poisson 方程的扩展能力

Fig. 4 展示了 WoB 对 Poisson 方程（非零源项）的处理能力。通过将 Poisson 方程转化为 Laplace 方程加体积分项，WoB 可处理 Dirichlet 和 Neumann 条件下的非齐次问题。每条采样路径使用 16 个体积样本来估计域积分，结果收敛至真解。这表明 WoB 框架具有向非齐次 PDE 扩展的潜力，但体积采样的引入增加了计算开销。

![[assets/figures/papers/paper_list_l39_https_rsugimoto_net_WoBforBVPsProject/figures/005_Figure_4.jpg]]
*Figure 4: Estimates for Poisson’s equation for Dirichlet (top) and Neumann (bottom) problems. WoB can handle the non-zero source term. For each sample path, we used 16 volume samples to estimate all domain integrals*

### 方法局限与待解决问题

实验揭示了 WoB 的若干边界条件：

1. **非凸域效率劣势**：如前所述，在复杂非凸域中 WoS 更高效。
2. **有偏截断**：当前 length-M 截断引入偏差，无偏的 Russian roulette 截断尚未实现。
3. **混合边界参数敏感性**：第一类方程变换中的参数 k 缺乏理论界限，仅通过实验选取，在未知问题上可能需要反复调试。
4. **多连通域与特定 Robin 条件**：部分公式在多连通域或某些 Robin 边界条件下可能失效或效率低下，论文未提供系统的实验验证。
5. **超奇异核问题**：在边界附近估计解的梯度时，涉及超奇异核（hypersingular kernel），噪声显著增大，这是未来需要解决的问题。

### 实验证据强度总结

| 核心主张 | 证据类型 | 强度 |
|---------|---------|------|
| WoB 消除 ε-shell 边界偏差 | 视觉对比（Fig. 2） | 强 |
| 统一支持多种边界条件 | 六种配置收敛验证（Fig. 1） | 强 |
| MIS 组合估计器鲁棒性 | 等时间对比（Fig. 10） | 较强 |
| 凸域效率与 WoS 相当 | RMSE 对比（Fig. 12） | 较强 |
| 非凸域效率低于 WoS | RMSE 对比（Fig. 12） | 较强 |
| RIS 改善混合边界采样 | 消融实验（Section 5） | 中等（需更多定量数据） |
| 路径截断偏差-方差权衡 | 参数扫描（Fig. 6） | 中等 |

总体而言，WoB 的实验评估充分验证了其在边界精度和边界条件通用性上的核心优势，但也诚实地揭示了在复杂几何上的效率劣势和若干未解决的理论问题。对于需要精确边界解或多边界条件混合的问题，WoB 提供了 WoS 无法替代的能力；对于复杂非凸域内的快速求解，WoS 仍是更实用的选择。

![[assets/figures/papers/paper_list_l39_https_rsugimoto_net_WoBforBVPsProject/figures/004_Table_1.jpg]]
*Table 1: List of equations for WoB estimators. The highlighted equations are the second kind Fredholm equations (or the modified first-kind equation for mixed boundary problems at Dirichlet boundaries) we use to get the unknown direct or indirect quantities on the boundary. It can be combined with other equations to find the unknown quantities of interest in the interior (or exterior) or on the boundary. It is assumed that the left hand side unknowns are functions of x, and the integrals are taken over boundary points y. The explicit dependencies on variables are omitted for brevity when it is not confusing. For interior problems*

## 定位与知识库关联

### 相对已有方法的本质差异

WoB 的核心变革在于将蒙特卡洛 PDE 求解的**采样域**从球面/体积转移到边界表面。以 **Walk-on-Spheres (WoS)**（Sawhney and Crane, ACM Trans. Graph. 2020）为基线，WoB 改变了三个关键 slot：

1. **采样域**：WoS 在域内进行球面随机游走，每一步采样下一个球面点，最终在 ε-shell 内截断。WoB 则通过光线追踪直接采样边界交点，每一步都落在边界上。这一改变消除了 WoS 中 ε-shell 近似带来的固有偏差（Fig. 2 显示 WoS 在边界附近产生可见条带伪影，而 WoB 无此问题）。

2. **递归方程的数学结构**：WoS 基于 Volterra 型方程（球面半径依赖于当前点到边界的距离），而 WoB 基于第二类 Fredholm 方程——积分域固定在边界 Γ 上，与当前点位置无关。这一转变使得 WoB 的估计器结构与渲染方程高度相似：两者都是固定积分域上的递归路径积分。

3. **路径终止机制**：WoS 依赖 ε-shell 截断（距离边界小于 ε 时终止），截断误差与 ε 相关。WoB 采用固定路径长度 M 截断，并在末项乘以 1/2 因子以保证收敛（Eq. (22) 的 Neumann 级数变换），这是一种有偏但可控的截断策略。

### 知识库挂载点

WoB 的核心洞察——边界积分方程与渲染方程的数学同构——使其可以直接挂载到成熟的**蒙特卡洛光线追踪**知识体系中：

- **积分方程形式**：渲染方程 $L = L_e + \mathcal{T}L$ 与 WoB 的 Fredholm 方程 $\nu = 2\overline{u}_D + \mathrm{H}\nu$ 具有相同的第二类 Fredholm 结构，只是积分核从 BSDF 替换为基本解的核函数（如双层势能核 $2\partial G/\partial \mathbf{n}_{\mathbf{y}}$）。

- **采样技术迁移**：由于方程结构一致，渲染领域的先进采样技术可直接应用于 WoB：
  - **多重重要性采样 (MIS)**：用于结合前向和后向估计器，在不同边界条件下保持鲁棒性（Fig. 10）。
  - **重采样重要性采样 (RIS)**：用于混合边界问题中有效捕获非零贡献区域（Section 5）。
  - **MCMC**：作者指出可应用 MCMC 方法处理复杂边界条件（Section 4.4.4），这是渲染中成熟的技术栈。

- **实现基础设施**：WoB 可直接构建在现有 MC 光线追踪系统之上（Fig. 7 展示了基于 Mitsuba 的实现），利用其光线求交、材质采样等基础设施，大幅降低实现门槛。

这一挂载点将 PDE 求解问题转化为渲染社区熟悉的路径积分估计问题，使得两个领域的技术可以双向流动。

### 适用边界

1. **优势场景**：
   - 需要边界及附近精确解的问题（WoS 的 ε-shell 近似不可接受时）。
   - 涉及 Neumann、Robin 或混合边界条件的问题（WoS 对这些条件支持不自然，需额外处理）。
   - 外域问题（WoS 难以处理无界域，WoB 通过边界积分自然支持）。
   - 需要与渲染管线集成的应用（如基于物理的可视化中的 PDE 求解）。

2. **劣势场景**：
   - 复杂非凸域（尤其含细小结构时）：WoS 的球面游走可快速“跳过”复杂几何，而 WoB 的边界游走需要更多步数才能遍历域内信息（Fig. 12 定量比较显示非凸域上 WoS 更高效）。
   - 需要域内体积项的问题（如泊松方程）：WoB 需要额外采样域内源项（Fig. 4，每条路径需 16 个体积样本），增加了实现复杂度。
   - 多连通域：部分公式可能失效或效率降低，需进一步研究。

3. **当前限制**：
   - 路径截断为有偏估计，尚未提供无偏的 Russian roulette 截断方案。
   - 混合边界问题中第一类方程变换参数 $k$ 的理论最优值未知，依赖实验调节。
   - 边界附近梯度估计（涉及超奇异核）噪声较大，未提供有效降噪方案。

### 后续启发

WoB 为 PDE 求解与渲染的交叉研究打开了多个方向：

1. **无偏路径截断**：将渲染中的 Russian roulette 和路径空间滤波技术引入 WoB，实现无偏估计，是最直接的改进方向。

2. **降噪与重建**：渲染中的降噪器（如基于神经网络的降噪）可直接应用于 WoB 的噪声输出，尤其在边界附近梯度估计场景中。

3. **扩展到其他 PDE**：作者指出 WoB 框架可扩展到泊松方程（Section 3.1 已给出转换关系）、弹性方程等。关键在于找到对应 PDE 的基本解和合适的边界积分方程形式。

4. **逆问题与可微渲染**：由于 WoB 与渲染管线深度集成，可微渲染技术可用于 PDE 约束的逆问题（如从边界观测反演域内参数），这是 WoS 难以实现的。

5. **混合 WoS-WoB 策略**：在域内使用 WoS 快速传播、在边界附近切换为 WoB 精确求解的混合策略，可能结合两者优势。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/A_Practical_Walk_on_Boundary_Method_for_Boundary_Value_Problems.pdf]]