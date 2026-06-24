---
title: "Boundary Value Caching for Walk on Spheres"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2023
pdf_ref: paperPDFs/SIGGRAPH_2023/Boundary_Value_Caching_for_Walk_on_Spheres.pdf
project_link: https://imaging.cs.cmu.edu/bvc/
aliases:
- BVCB
- BVCWS
tags:
- SIGGRAPH_2023
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "边界值缓存（BVC）机制——仅在域边界（或感兴趣子域边界）的随机采样点上通过少量随机行走估计未知边界数据（解和法向导数），随后通过边界积分方程（BIE）对内部点进行廉价的无偏蒙特卡洛估计，实现样本复用。"
primary_logic: "通过将随机行走的计算负载从每个内部点转移到少数边界点并缓存结果，再利用边界积分表达式的平滑性在内部点间共享同一组缓存样本，可以大幅降低整体随机行走次数，同时保持无偏性、渐进性、输出敏感性和对低质量几何的鲁棒性。"
claims:
- "方法利用WoS/WoSt仅在边界上估计未知边界值（Dirichlet边界上的法向导数和Neumann边界上的解），然后通过缓存样本和边界积分方程（2）在任意内部点评估解，无需额外随机行走。"
- "缓存方案不引入额外偏差，仅继承点估计器的可控偏差，同时大幅提升效率（图5）并显著压制蒙特卡洛噪声。"
- "针对奇异Green函数引起的边界伪影，提出基于积分分裂的无偏校正策略（式8），并通过重要性采样的残差部分（射线与边界求交）保证低方差。"
- "多个视觉/几何计算测试问题（风洞流线、纹理坐标插值、宇航服温度模型、混合边界条件问题） 上 视觉效果（平滑度、噪声水平）及计算效率（等时间比较） = 在混合边界问题中显著降低噪声，获得全区域平滑的解和梯度，密集评估时效率大幅提升"
---

# Boundary Value Caching for Walk on Spheres

> [!tip] 核心洞察
> 通过将随机行走的计算负载从每个内部点转移到少数边界点并缓存结果，再利用边界积分表达式的平滑性在内部点间共享同一组缓存样本，可以大幅降低整体随机行走次数，同时保持无偏性、渐进性、输出敏感性和对低质量几何的鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 球面行走的边界值缓存 |
| 英文题名 | Boundary Value Caching for Walk on Spheres |
| 会议/期刊 | SIGGRAPH 2023 |
| Links | [paper](https://arxiv.org/abs/2302.11825); [Project](https://imaging.cs.cmu.edu/bvc/) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Boundary Value Caching (BVC) |
| Dataset | 多个视觉/几何计算测试问题（风洞流线、纹理坐标插值、宇航服温度模型、混合边界条件问题）, 纯Dirichlet问题, Dirichlet主导的高频边界条件问题 |

> [!tip] 效果简介
> - 多个视觉/几何计算测试问题（风洞流线、纹理坐标插值、宇航服温度模型、混合边界条件问题） 上，视觉效果（平滑度、噪声水平）及计算效率（等时间比较） 为 在混合边界问题中显著降低噪声，获得全区域平滑的解和梯度，密集评估时效率大幅提升，对比 逐点WoSt/WoS估计噪声明显，尤其在Neumann边界主导或远Dirichlet边界区域梯度噪声严重，变化 定性观察：边界值缓存版结果更加平滑，密集网格评估速度远快于点估计器（无具体数值）。
> - 纯Dirichlet问题 上，方差/效率比较（等时间） 为 一般性缓存策略；方差高于Qi et al. 2022专用双向方法，对比 Qi et al. 2022双向WoS，等时间下方差更低，变化 BVC方差偏高，但在混合边界问题中无可比拟。
> - Dirichlet主导的高频边界条件问题 上，效率 为 缓存策略可能效率下降，因随机行走较短、未重要性采样奇异函数以及∂u/∂n估计噪声，对比 逐点WoSt可能在短行走问题上相对效率更高（无数字对比），变化 在Dirichlet主导问题中BVC优势减弱。

## 概述

求解椭圆型偏微分方程（PDE）是计算机图形学与计算物理中的基础任务，其典型形式为带屏蔽项的泊松方程，在域内满足 $\Delta u - \sigma u = f$，并在边界上混合给定 Dirichlet 条件 $u = g$ 和 Neumann 条件 $\partial u / \partial n = h$。传统确定性方法如边界元法（BEM）依赖高质量边界网格和全局稠密线性系统求解，在低质量几何上易产生混叠伪影甚至完全失效（Fig. 2）。网格无关的蒙特卡洛方法——经典球面行走（WoS, Muller 1956）及其扩展星形行走（WoSt, Sawhney et al., ACM Trans. Graph. 2023）——虽然规避了网格依赖，但在每个内部评估点独立执行随机行走，导致大量冗余计算和高方差，尤其当需要密集评估解或梯度时，无法利用椭圆问题解的高空间平滑性。

本文提出**边界值缓存**（Boundary Value Caching, BVC）策略，核心思路是将随机行走的计算负载从每个内部点转移到域边界（或感兴趣子域边界）上的少量随机采样点：仅在边界样本点上通过 WoSt 估计未知边界数据——Dirichlet 边界上的法向导数 $\partial u / \partial n$ 和 Neumann 边界上的解 $u$——并将这些估计值缓存。随后，利用边界积分方程（BIE）对任意内部点进行廉价的蒙特卡洛估计，无需额外随机行走，从而在保持无偏性、渐进性和输出敏感性的同时，大幅降低整体随机行走次数并显著压制蒙特卡洛噪声。

实验表明，在混合边界问题中，BVC 在等时间预算下获得远优于逐点 WoSt 的平滑解和梯度（Fig. 5, Fig. 7），密集网格评估时因样本复用而效率急剧提升。方法对低质量几何具有天然鲁棒性，且支持渐进式评估和输出敏感的子域聚焦计算。在纯 Dirichlet 问题上，BVC 方差高于专用双向方法（Qi et al., Computer Graphics Forum 2022），但在混合边界场景中无可比拟；在 Dirichlet 主导的高频边界条件下，缓存策略效率下降。针对奇异 Green 函数引起的边界伪影，BVC 引入基于积分分裂的无偏校正策略（式 8），在消除伪影的同时避免偏差。

## 背景与动机

偏微分方程（PDE）是计算机图形学与几何处理中描述物理现象的核心工具。许多视觉计算任务——从流体模拟、热传导到曲面参数化——最终都归结为在复杂几何域上求解椭圆型方程。本文关注一类混合边界条件的屏蔽泊松方程：

$$
\begin{array}{rl}
\Delta u - \sigma u = f & \text{on } \Omega \\
u = g & \text{on } \partial\Omega_D \\
\frac{\partial u}{\partial n} = h & \text{on } \partial\Omega_N
\end{array}
$$

其中 $\Omega \subset \mathbb{R}^d$ 为求解域，$\partial\Omega_D$ 和 $\partial\Omega_N$ 分别为 Dirichlet 和 Neumann 边界，$\sigma$ 为常数吸收系数，$f$ 为已知源项，$g$ 和 $h$ 为已知边界数据，$u$ 和法向导数 $\partial u / \partial n$ 在互补边界上未知。

### 现有方法的根本瓶颈

求解上述问题的两类主流范式——确定性边界元方法（BEM）与蒙特卡洛点估计器——各自面临难以调和的矛盾。

**确定性方法的网格依赖困境。** BEM 将 PDE 转化为仅涉及边界的积分方程，通过离散化边界并求解全局稠密线性系统获得解。这一策略天然依赖高质量的边界网格：如图 2 所示，即使对于简单边界条件，网格细化不足会导致边界数据的局部混叠，进而引发全域范围的 PDE 解误差；在包含不规则元素的域上，BEM 甚至可能完全失效。这种对边界表示的强耦合限制了其在低质量几何（如仅为可视化设计的三角网格）上的适用性。

**逐点蒙特卡洛估计器的冗余计算。** 球面行走（Walk on Spheres, WoS; Muller 1956）及其推广星形行走（Walk on Stars, WoSt; Sawhney et al., ACM Trans. Graph. 2023）提供了一条网格无关的替代路径：它们通过模拟布朗运动随机行走，在每个内部评估点独立地获得解的无偏估计。然而，这一独立性恰恰构成了其根本瓶颈——**每个评估点都必须执行完整的随机行走过程，导致大量冗余计算**。当需要密集评估解（如体渲染或流线追踪）或计算梯度场时，总行走次数随评估点数量线性增长，计算代价变得不可接受。更关键的是，这种逐点独立估计完全忽视了椭圆方程解的一个本质特性：**高空间平滑性**。相邻点的解高度相关，但在点估计器框架下，这一相关性无法被利用以共享计算。

### 动机：从“逐点行走”到“边界缓存”

上述困境揭示了一个核心洞察：**随机行走的计算负载应当从每个内部评估点转移到少数边界点，并通过样本复用惠及所有内部点**。这一思想源于边界积分方程（BIE）对解的经典表达：

$$
u(x) = \underbrace{\int_{\partial\Omega} \frac{\partial G}{\partial n}(x,z) u(z) - G(x,z) \frac{\partial u}{\partial n}(z) \,dz}_{=: u_{\partial\Omega}(x)} + \underbrace{\int_{\Omega} G(x,y) f(y) \,dy}_{=: u_{\Omega}(x)}
$$

其中 $G$ 为自由空间 Green 函数。该表达式的关键在于：**一旦边界上的未知量——Dirichlet 边界上的法向导数 $\partial u / \partial n$ 和 Neumann 边界上的解 $u$——被确定，任意内部点 $x$ 的解便可仅通过积分（而非随机行走）计算**。而 WoS/WoSt 恰好能够在单个边界点处估计这些未知量。

由此，本文的核心动机自然浮现：**仅在边界随机采样点上通过少量随机行走估计未知边界数据并缓存，随后利用 BIE 对所有内部评估点进行廉价的蒙特卡洛积分估计。** 这一“边界值缓存”（Boundary Value Caching, BVC）策略将随机行走的次数与内部评估点数量解耦，使密集评估的计算代价大幅降低，同时继承点估计器的无偏性、渐进性、输出敏感性及对低质量几何的鲁棒性。

## 核心创新

BVC的核心创新在于将椭圆型偏微分方程求解的计算范式从“逐点独立估计”转变为“边界采样—缓存复用—积分重建”。这一转变通过以下关键机制实现：

### 从逐点行走到边界复用的估计范式转换

传统蒙特卡洛求解器（如**WoS** (Muller 1956) 和 **WoSt** (Sawhney et al., ACM Trans. Graph. 2023)）对每个内部评估点独立执行随机行走，导致大量冗余计算。BVC将计算负载从内部点转移到边界点：仅在域边界（或感兴趣子域边界）的随机采样点上通过少量随机行走估计未知边界数据——即Neumann边界上的解 $u$ 和Dirichlet边界上的法向导数 $\partial u/\partial n$——然后将这些估计值缓存，随后通过边界积分方程（BIE）对任意内部点进行廉价的蒙特卡洛估计，无需额外随机行走。

这一范式转换的数学基础是解的边界积分表示：

$$u(x) = \int_{\partial\Omega} \frac{\partial G}{\partial n}(x,z) u(z) - G(x,z) \frac{\partial u}{\partial n}(z) \,dz + \int_{\Omega} G(x,y) f(y) \,dy$$

传统方法在每个 $x$ 处独立估计该积分，而BVC将 $u(z)$ 和 $\partial u/\partial n(z)$ 在边界样本 $\{z_i\}$ 上预先估计并缓存，使得对任意评估点 $\{x_k\}$ 的估计退化为对缓存的加权求和：

$$\widehat{u_{\partial\Omega}}(x_k) = \frac{1}{N} \sum_{i=1}^N \frac{\frac{\partial G}{\partial n}(x_k, z_i) \widehat{u}(z_i) - G(x_k, z_i) \widehat{\frac{\partial u}{\partial n}}(z_i)}{p^{\partial\Omega}(z_i)}$$

### 跨评估点的样本共享与相关性引入

逐点估计器各评估点彼此独立，无样本共享。BVC通过同一组边界缓存样本为所有评估点计算BIE贡献，使内部点估计高度相关。这一设计带来两个关键优势：

1. **显著平滑结果**：由于所有内部点共享同一组边界样本的估计误差，空间噪声表现为低频的全局误差而非逐点独立的高频噪声，在视觉效果上产生远为平滑的解和梯度（Fig. 5, Fig. 7）。
2. **密集评估效率大幅提升**：评估更多内部点几乎不影响性能，因为边界样本只需生成一次即可复用。这使得BVC在密集3D网格评估场景下效率远超逐点估计器。

### 输出敏感的子域聚焦计算

传统方法评估任意区域均需从头开始随机行走，无法仅关注局部区域。BVC支持将计算聚焦于用户指定的子域 $R \subset \Omega$：仅需在子域边界 $\partial R$ 上生成并缓存样本，即可在该子域内任意点评估解，而无需涉及全局边界。这一特性使BVC天然支持输出敏感的计算资源分配（Fig. 8）。

### 无偏奇异函数校正策略

缓存方案的一个关键挑战是：BIE中的Green函数及其法向导数在评估点靠近边界时呈奇异性，而缓存方案未对奇异函数进行重要性采样，导致边界附近出现局部伪影。BVC提出基于积分分裂的无偏校正策略：

$$\int_{\partial R} \left.\frac{\partial G}{\partial n}\right|_c (x,z) u(z) \,dz + \int_{\partial R} \left[\frac{\partial G}{\partial n}(x,z) - \left.\frac{\partial G}{\partial n}\right|_c (x,z)\right] u(z) \,dz$$

其中第一项使用钳制（clamped）版本的 $\partial G/\partial n$ 抑制伪影，第二项通过重要性采样残差部分（利用射线与边界求交精确采样 $p^{\partial R} = \partial G/\partial n$）保持整体估计无偏。该策略在消除边界伪影的同时不引入额外偏差（Fig. 11），而单纯的钳制策略会产生明显偏差（Fig. 17 bottom）。

### 对低质量几何的鲁棒性

与**边界元方法（BEM）**需要高质量边界网格和全局密集线性系统求解不同，BVC继承WoS/WoSt的网格无关特性，将问题输入与边界表示解耦，因此对低质量曲面网格具有天然鲁棒性，不会产生混叠伪影（Fig. 2）。

### 方法定位与局限

值得注意的是，BVC作为通用缓存策略，在纯Dirichlet问题上的方差高于专用方法（如**Qi et al. 2022**的双向WoS，Computer Graphics Forum 2022），但在混合边界问题中无可比拟。此外，在Dirichlet主导的高频边界条件问题中，缓存策略效率下降，原因包括随机行走路径变短、未对BIE奇异函数进行重要性采样，以及法向导数估计的噪声影响增大（Fig. 16 bottom row）。

## 整体框架

BVC 的整体工作流围绕“边界采样—点估计—缓存复用—积分求值”四个阶段构建，其核心思想是将随机行走的计算负载从每个内部评估点转移到少数边界样本上，并通过边界积分方程（BIE）实现样本的高效复用。

**输入与预处理。** 方法接受混合边值问题定义（式1），包含 Dirichlet 边界 $\partial\Omega_D$ 上的已知解 $g$、Neumann 边界 $\partial\Omega_N$ 上的已知法向导数 $h$、源项 $f$ 以及常数 $\sigma$。对于内部求解，需构造一个闭合区域，其边界由 Neumann 边界 $\partial\Omega_N$ 和偏移 Dirichlet 边界 $\partial\Omega_D^l$（$l > \varepsilon$）组成（Figure 9），以确保边界样本落在 $\varepsilon$-壳层之外。若仅关注子域 $\mathcal{R} \subset \Omega$，则可仅在 $\partial\mathcal{R}$ 上采样，实现输出敏感计算（Figure 8）。

**缓存生成。** 算法首先生成两类缓存（Algorithm 1 lines 13–16, 24–25）：
- **边界样本缓存** `boundarySamples`：在 $\partial\Omega_N$ 和 $\partial\Omega_D^l$ 上按概率密度 $p^{\partial\Omega}$ 采样位置 $z_i$ 及法向 $n_{z_i}$，随后对每个样本调用 `WalkOnStars`（即 WoSt 点估计器，Section 3.1）估计该点的解 $\widehat{u}(z_i)$ 和法向导数 $\widehat{\partial u/\partial n}(z_i)$。注意在 Dirichlet 边界上仅需估计 $\partial u/\partial n$，在 Neumann 边界上仅需估计 $u$。
- **源样本缓存** `sourceSamples`：在域内按概率密度 $p^{\Omega}$ 采样位置 $y_j$，并记录已知源项值 $f(y_j)$。

**积分求值与样本复用。** 获得缓存后，对任意内部评估点 $x_k \in \texttt{evalPts}$，通过蒙特卡洛估计器直接累加所有边界样本和源样本的贡献（Algorithm 1 lines 18–28）：
- 边界积分贡献 $\widehat{u_{\partial\Omega}}(x_k)$ 由式（3）计算，同时复用同一边界样本集；
- 源积分贡献 $\widehat{u_{\Omega}}(x_k)$ 由式（4）计算；
- 梯度估计 $\widehat{\partial u/\partial x}(x_k)$ 由式（5）和（6）分别计算边界和源积分贡献。

由于所有评估点共享同一组缓存样本，内部点估计高度相关，从而显著平滑结果（Fig. 5）。评估更多内部点几乎不影响性能，因为无需额外随机行走。

**奇异函数校正（可选）。** 当评估点靠近边界时，Green 函数的法向导数 $\partial G/\partial n$ 呈现奇异性，直接使用缓存样本会导致局部伪影。BVC 通过积分分裂策略（式8）将边界积分分解为钳制部分（用 clamped $\partial G/\partial n|_c$ 抑制伪影）和残差部分（用重要性采样 $p^{\partial R} = \partial G/\partial n$ 通过射线-边界求交精确采样，保持无偏）。由于 $\partial G/\partial n$ 随距离快速衰减，仅需对靠近评估点的边界样本运行少量随机行走来估计残差部分，额外开销可控（Fig. 11）。

**渐进式更新。** `UpdateSolution` 函数支持渐进式评估：可随时生成新缓存并将其贡献累加到现有估计中，或利用已有缓存为新增评估点计算估计值，无需重新运行整个流程（Algorithm 1）。这使得方法天然支持渐进式细化和交互式探索。

**输出。** 最终输出为所有评估点上的解 $u(x_k)$ 和梯度 $\partial u/\partial x(x_k)$ 的蒙特卡洛估计值。整个流程不引入除 WoSt 点估计器本身可控偏差（$\varepsilon$-壳终止）之外的任何额外偏差，同时大幅降低了总随机行走次数（Fig. 1）。

### 补充图表

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2302_11825/figures/013_Figure_14.jpg]]
*Figure 14: For Dirichlet problems, our method o en has higher variance than Qi et al. [2022]’s specialized approach for these boundary conditions*

## 核心模块与公式推导

### 边界积分表示与缓存估计框架

BVC的核心思想源于椭圆型偏微分方程解的边界积分表示。对于定义在域 $\Omega$ 上的混合边界值问题：

$$
\begin{array}{rl}
\Delta u - \sigma u = f & \text{on } \Omega \\
u = g & \text{on } \partial\Omega_D \\
\frac{\partial u}{\partial n} = h & \text{on } \partial\Omega_N
\end{array}
$$

其解可借助自由空间Green函数 $G$ 及其法向导数表示为边界积分与源积分的叠加（式2）：

$$
u(x) = \int_{\partial\Omega} \frac{\partial G}{\partial n}(x,z) u(z) - G(x,z) \frac{\partial u}{\partial n}(z) \,dz + \int_{\Omega} G(x,y) f(y) \,dy
$$

其中 $u_{\partial\Omega}(x)$ 为边界积分贡献，$u_{\Omega}(x)$ 为源积分贡献。该表示的关键洞察在于：一旦获得了边界上各点的 $u(z)$ 和 $\frac{\partial u}{\partial n}(z)$，任意内部点的解即可通过积分直接计算，无需额外随机行走。BVC正是利用这一性质，将计算负载从逐点随机行走转移到边界样本的估计与缓存上。

方法维护两类缓存：**边界样本缓存**（boundarySamples），包含边界采样点位置 $z_i$、该点解估计 $\widehat{u}(z_i)$ 和法向导数估计 $\widehat{\frac{\partial u}{\partial n}}(z_i)$；**源样本缓存**（sourceSamples），包含域内采样点位置 $y_j$ 和已知源项值 $f(y_j)$。对任意评估点 $x_k$，边界积分贡献的蒙特卡洛估计为（式3）：

$$
\widehat{u_{\partial\Omega}}(x_k) = \frac{1}{N} \sum_{i=1}^N \frac{\frac{\partial G}{\partial n}(x_k, z_i) \widehat{u}(z_i) - G(x_k, z_i) \widehat{\frac{\partial u}{\partial n}}(z_i)}{p^{\partial\Omega}(z_i)}
$$

源积分贡献的蒙特卡洛估计为（式4）：

$$
\widehat{u_{\Omega}}(x_k) = \frac{1}{M} \sum_{j=1}^M \frac{G(x_k, y_j) f(y_j)}{p^{\Omega}(y_j)}
$$

梯度估计遵循相同的缓存复用逻辑。边界积分对梯度的贡献估计为（式5）：

$$
\widehat{\frac{\partial u_{\partial\Omega}}{\partial x}}(x_k) = \frac{1}{N} \sum_{i=1}^N \frac{\frac{\partial^2 G}{\partial x\partial n}(x_k, z_i) \widehat{u}(z_i) - \frac{\partial G}{\partial x}(x_k, z_i) \widehat{\frac{\partial u}{\partial n}}(z_i)}{p^{\partial\Omega}(z_i)}
$$

源积分对梯度的贡献估计为（式6）：

$$
\widehat{\frac{\partial u_{\Omega}}{\partial x}}(x_k) = \frac{1}{M} \sum_{j=1}^M \frac{\frac{\partial G}{\partial x}(x_k, y_j) \, f(y_j)}{p^{\Omega}(y_j)}
$$

由于所有评估点共享同一组边界和源缓存样本，上述估计器在评估点之间高度相关，从而产生显著平滑的解和梯度。**缓存方案不引入额外偏差，仅继承底层点估计器（WoS/WoSt）的可控偏差**（Section 3）。

### 边界样本生成与点估计

边界样本需要在指定边界上按概率密度 $p^{\partial\Omega}$ 生成，随后通过点估计器获取该点的解和法向导数。对于混合边界问题，边界样本生成在由Neumann边界 $\partial\Omega_N$ 和偏移Dirichlet边界 $\partial\Omega_D^l$（$l > \varepsilon$）围成的闭合区域上进行（Figure 9）。偏移量 $l$ 设置为 $5\varepsilon$ 可有效缓解Dirichlet边界附近法向导数估计的偏差——过小的 $l$ 会使球完全包含在 $\varepsilon$-壳层内，导致法向导数估计趋近于零而产生系统性偏差（Figure 17 top）。

每个边界样本的 $\widehat{u}(z_i)$ 和 $\widehat{\frac{\partial u}{\partial n}}(z_i)$ 通过 **Walk on Stars (WoSt)** 算法估计（Algorithm 1 line 16）。法向导数通过 $\mathbf{n}_x \cdot \widehat{\frac{\partial u}{\partial x}}(x)$ 计算，其中梯度估计可递归使用WoSt（式7），利用WoSt在混合边界上同时估计解和梯度的能力。

### 奇异函数处理与无偏校正

边界积分表示中的Green函数 $\frac{\partial G}{\partial n}(x,z)$ 在 $x \to z$ 时具有奇异性。由于缓存方案未对该奇异函数进行重要性采样，当评估点靠近边界样本时会产生明显的局部伪影。为解决这一问题，BVC采用基于积分分裂的无偏校正策略（式8）：

$$
\int_{\partial R} \left.\frac{\partial G}{\partial n}\right|_c (x,z) u(z) \,dz + \int_{\partial R} \left[\frac{\partial G}{\partial n}(x,z) - \left.\frac{\partial G}{\partial n}\right|_c (x,z)\right] u(z) \,dz
$$

其中 $\left.\frac{\partial G}{\partial n}\right|_c \equiv \max(-c, \min(c, \frac{\partial G}{\partial n}))$ 为钳制后的法向导数。第一项（钳制部分）使用缓存样本计算，有效抑制奇异伪影；第二项（残差部分）仅在评估点靠近边界样本时非零，通过重要性采样 $p^{\partial R} = \frac{\partial G}{\partial n}$ 进行估计——该采样可通过射线与边界求交精确实现，仅需少量额外随机行走。**该校正策略在消除伪影的同时保持估计的无偏性**（Figure 11, Figure 17 bottom）。钳制界 $c$ 根据场景尺度设置，过小的 $c$ 虽能更强地抑制伪影但会引入偏差，而积分分裂校正正是为了消除这一偏差。

### 渐进式评估与输出敏感性

BVC支持渐进式评估：通过生成新的缓存并将贡献累加到现有估计中（Algorithm 1函数UpdateSolution），用户可在任意时刻获得当前最佳估计。更重要的是，方法天然支持**输出敏感**的局部评估——用户可定义感兴趣的子域 $R \subset \Omega$，仅在其边界 $\partial R$ 上生成和缓存样本，从而将计算聚焦于特定区域（Figure 8），无需像传统边界元方法（BEM）那样进行全局求解。

## 实验与分析

### 主要结果

BVC 在混合边界条件问题上的核心优势体现在**样本复用带来的全局平滑性**与**密集评估时的大幅效率提升**。图5展示的定性对比中，在相同计算时间内，BVC 产生的解场在整个域内显著平滑于逐点 WoSt 估计器——后者在 Neumann 边界主导区域和远离 Dirichlet 边界的区域噪声明显。这种平滑性源于所有内部评估点共享同一组边界缓存样本，使得点估计之间高度相关，从而压制了蒙特卡洛噪声。

梯度估计的改善更为突出（图7）。BVC 在计算梯度时直接使用 Neumann 边界上已知的 $\partial u/\partial n$ 值代入式(5)，而 WoSt 的梯度估计在远离 Dirichlet 边界时需要更长的随机行走，噪声随距离累积。这一差异在风洞流线可视化（图1）和宇航服温度模型等应用中直接转化为视觉质量的显著提升。

在纯 Dirichlet 问题上，BVC 作为通用方法并未针对该特定设定优化。图14显示，与 **Qi et al. 2022 双向 WoS**（Computer Graphics Forum 2022）相比，BVC 在等时间下方差更高。该专用方法利用 Dirichlet 问题的结构特征实现了更低的方差，但无法处理混合边界条件——而这正是 BVC 无可比拟的场景。

在 Dirichlet 主导的高频边界条件问题中，BVC 的效率优势减弱（图16底部行）。原因有三：(1) 随机行走路径变短，缓存策略摊销长行走成本的核心优势被削弱；(2) BVC 未对边界积分方程中的奇异 Green 函数进行重要性采样；(3) Dirichlet 边界上 $\partial u/\partial n$ 的估计噪声对最终解的影响增大。这一失败模式提示：当问题中 Dirichlet 边界占主导且边界条件频率较高时，逐点 WoSt 可能是更优选择。

与确定性方法 BEM 的对比（图2）揭示了 BVC 的另一结构性优势：BVC 将问题输入与边界表示解耦，因此对低质量网格和不规则单元具有天然的鲁棒性，不会出现 BEM 因网格混叠导致的全局误差。但这也意味着 BVC 的误差呈现全局特性（图12），随边界样本数增加而消失——收敛行为更接近传统确定性求解器，而非点估计器的局部噪声模式。

### 消融实验

**偏移参数 $l$ 的选取**（图17顶部）：当 $l$ 设置为 $0.1 \times \varepsilon$ 时，每个 Dirichlet 边界样本处的球完全包含在 epsilon 壳层内，导致 $\partial u/\partial n$ 的估计趋近于零，在域内引入显著偏差。随 $l$ 增大，偏差逐渐消失。论文最终设置 $l = 5\varepsilon$，在偏差抑制与边界采样灵活性之间取得平衡。

**钳位参数 $c$ 与奇异校正策略**（图17底部，图11）：直接钳制 $\partial G/\partial n$ 的幅度（$c$ 取较小值）虽然能抑制近边界处的奇异伪影，但会引入明显偏差。BVC 提出的积分分裂校正策略（式8）将边界积分分解为钳制部分与残差部分，对残差部分通过射线与边界求交进行重要性采样，在消除局部伪影的同时保持无偏性——图11底部右图验证了该策略的有效性。

### 公平性说明

所有与逐点估计器的比较均在等时间预算下进行，确保计算资源公平分配。与 BEM 的比较侧重于网格质量对求解精度的影响。与 Qi et al. 2022 的比较限定于纯 Dirichlet 问题，BVC 在该设定下并非最优，但其通用性使其在混合边界问题中无可替代。需注意，主要结果的评估依赖定性视觉质量而非定量误差指标，原因在于测试场景缺少解析解或高精度参考解。

### 补充图表

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2302_11825/figures/007_Figure_7.jpg]]
*Figure 7: Our gradients have considerably less noise compared to pointwise estimates as they use known values for 𝜕𝑢/𝜕𝑛 on the Neumann boundary to evaluate Equation (5). In contrast, WoSt gradients become noisier away from the Dirichlet boundary as estimation requires longer random walks*

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2302_11825/figures/005_Figure_5.jpg]]
*Figure 5: We obtain far smoother results across the domain compared to directly using pointwise estimators like WoSt at equal time. Evaluating the BIE at more points inside the domain has li le impact on performance, as the same boundary samples are used to determine the PDE solution*

![[assets/figures/papers/paper_list_l51_https_arxiv_org_abs_2302_11825/figures/016_Figure_17.jpg]]
*Figure 17: Top: Se ing the 𝑙 ofset parameter to 0.1 × 𝜀 efectively sets each Dirichlet boundary sample’s 𝜕𝑢/𝜕𝑛 estimate to zero, as balls centered at each sample point are contained entirely inside the epislon shell—this biases the solution estimate inside the domain. Bias diminishes with increasing ofset values. Bo om: Smaller values of the bound 𝑐 for 𝜕𝐺/𝜕𝑛 in Equation (8) suppress singular artifacts near the boundary but biases interior estimates without our correction strategy, shown here on a model scaled to fit inside a unit sphere*

## 方法谱系与知识库定位

### 1. 基线方法谱系

**BVC** 位于网格无关蒙特卡洛 PDE 求解器与边界积分方程（BIE）方法的交叉点上，其设计同时回应了两类基线的核心瓶颈。

#### 1.1 点估计蒙特卡洛方法

- **Walk on Spheres (WoS)**（Muller 1956）：经典网格无关方法，通过模拟布朗运动随机行走求解纯 Dirichlet 椭圆问题。其根本局限在于每个内部评估点需要独立执行完整随机行走，无法在密集评估网格中复用计算。
- **Walk on Stars (WoSt)**（Sawhney et al., *ACM Trans. Graph.* 2023）：将 WoS 扩展至混合 Dirichlet-Neumann 边界条件。继承了点估计的独立行走范式，在 Neumann 边界主导或远离 Dirichlet 边界的区域梯度噪声显著增加（Fig. 7）。
- **双向 WoS**（Qi et al., *Computer Graphics Forum* 2022）：针对纯 Dirichlet 问题的专用方法，在等时间计算预算下方差通常低于 BVC（Fig. 14）。但其适用范围受限，无法处理混合边界条件。

BVC 相对于上述方法的**核心因果操作**是：将随机行走的计算负载从每个内部评估点转移到少数边界采样点，通过缓存机制实现跨评估点的样本复用。这直接回应了逐点估计器“独立行走导致冗余计算”的根本瓶颈。

#### 1.2 确定性边界元方法

- **Boundary Element Method (BEM)**：传统边界元方法需构建高质量边界网格并求解全局稠密线性系统。其在低质量网格上产生严重的混叠伪影，且无法处理不规则单元（Fig. 2）。BVC 通过解耦问题输入与边界表示，从根本上避免了对网格质量的依赖。

BVC 与 BEM 的**关键分水岭**在于：BEM 将计算负载集中于全局线性系统求解，而 BVC 将负载转移至边界样本的随机行走估计，继承了蒙特卡洛方法的渐进性、输出敏感性和对低质量几何的鲁棒性。

### 2. 方法适用边界

#### 2.1 优势场景

- **混合边界条件问题**：BVC 在 Neumann 边界主导的问题中效率优势最为显著，因为缓存策略将长距离随机行走的成本摊销到大量内部评估点上（Fig. 16 top two rows）。
- **密集评估网格**：当需要在域内大量点处评估解或梯度时，样本复用带来的效率提升急剧增大——评估更多内部点几乎不影响性能，因为同一组边界样本被共享（Fig. 5）。
- **低质量几何**：BVC 不依赖边界网格质量，可直接在可视化网格上求解 PDE（Fig. 1 风洞流线示例），而 BEM 在类似条件下会产生混叠误差甚至完全失败（Fig. 2）。
- **局部感兴趣区域**：BVC 支持输出敏感的局部评估——可仅在子域边界 ∂R 上缓存样本，聚焦计算于感兴趣区域，而 BEM 必须执行涉及整个边界的全局求解（Fig. 8）。

#### 2.2 劣势场景

- **Dirichlet 主导的高频边界条件问题**：效率下降，原因有三：（1）随机行走路径变短，缓存摊销效益减弱；（2）未对 BIE 中的奇异 Green 函数进行重要性采样；（3）Dirichlet 边界上法向导数估计的噪声影响增大（Fig. 16 bottom row）。
- **纯 Dirichlet 问题**：BVC 作为通用方法，在等时间下方差高于 Qi et al. (2022) 的专用双向 WoS 方法（Fig. 14）。此时 BVC 的通用性成为负担而非优势。

### 3. 方法局限

1. **继承的偏差**：BVC 继承 WoS/WoSt 点估计器中的可控偏差（epsilon-壳终止），且未提供直接在 Dirichlet 边界上无偏估计法向导数的方案。偏移参数 *l* 需手动设置为 5ε 以缓解偏差（Fig. 17 top），缺乏自适应性。
2. **边界伪影与校正复杂性**：缓存方案因未对奇异 Green 函数进行重要性采样而产生边界伪影。所提出的积分分裂校正策略（Equation 8）虽保持无偏，但增加了实现复杂性，且钳位参数 *c* 需根据场景尺度手动设置（Fig. 17 bottom）。
3. **大规模评估的扩展性瓶颈**：当前实现未集成快速多极、Barnes-Hut 或 lightcuts 等加速结构。当评估点数量极大时，边界积分的直接求和评估可能成为瓶颈。
4. **全局误差特性**：与 BEM 类似，BVC 的误差呈现全局特性（Fig. 12），而非点估计器的局部噪声。这意味着收敛行为更接近传统确定性求解器，可能在某些场景下不如逐点估计器的局部误差分布可预测。
5. **梯度校正缺失**：奇异函数校正策略当前仅适用于解估计，向梯度估计器的扩展仍为未来工作（Fig. 10 展示了朴素钳制在梯度估计中引入偏差的问题）。

### 4. 开放问题

1. **加速结构集成**：如何将快速多极、Barnes-Hut 或 lightcuts 等聚类加速技术融入缓存策略，以支持大规模评估点集的高效边界积分计算？
2. **无偏法向导数估计**：是否存在无需偏移壳层的、直接在 Dirichlet 边界上进行无偏法向导数估计的方法？
3. **混合策略**：是否可将双向 WoS（Qi et al. 2022）整合到缓存框架中，在纯 Dirichlet 区域自动切换至更高效的专用估计器？
4. **自适应参数调节**：如何自动设置钳位参数 *c*，以及如何借鉴虚拟点光源（VPL）文献中的技术自适应调节奇异函数校正？
5. **域分解与复杂拓扑**：如何在蒙特卡洛框架下设计域分解策略，有效处理薄特征和复杂拓扑域？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2023/Boundary_Value_Caching_for_Walk_on_Spheres.pdf]]
