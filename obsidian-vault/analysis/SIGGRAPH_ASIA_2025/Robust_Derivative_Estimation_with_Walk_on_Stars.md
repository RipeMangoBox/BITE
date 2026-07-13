---
title: "Robust Derivative Estimation with Walk on Stars"
type: paper
paper_level: A
venue: "SIGGRAPH Asia"
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2025/Robust_Derivative_Estimation_with_Walk_on_Stars.pdf
project_link: null
code_link: null
aliases:
- RDEWS
tags:
- SIGGRAPH_ASIA_2025
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "引入向量值反射函数 ρ_v 控制星形区域半径并实现无偏俄罗斯轮盘赌终止，将方向导数 BIE 转化为单一未知函数的递归估计。"
primary_logic: "调和函数的导数仍为调和的，借此构建方向导数的边界积分方程 (BIE)，通过反射函数自适应调整步长并实现无偏早期终止，从而在边界附近获得有界方差。"
claims:
- "导数本身是调和函数，可为 Poisson 方程的一阶和二阶空间导数构造边界积分方程。"
- "通过处理奇异核并引入控制变量，估计器在边界和内部均保持有界方差。"
- "在 Neumann 主导问题中通过无偏早期终止显著降低方差。"
- "纯 Neumann 导数估计中，我们方法在同等计算预算下比基线误差更低、噪声更小 (图 6)。"
---

# Robust Derivative Estimation with Walk on Stars

> [!tip] 核心洞察
> 调和函数的导数仍为调和的，借此构建方向导数的边界积分方程 (BIE)，通过反射函数自适应调整步长并实现无偏早期终止，从而在边界附近获得有界方差。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于星星行走的鲁棒导数估计 |
| 英文题名 | Robust Derivative Estimation with Walk on Stars |
| 会议/期刊 | SIGGRAPH Asia 2025 |
| Links | [paper](https://projects.shuangz.com/grad-wost-sa25/grad-wost-sa25.pdf) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Robust Derivative Estimation with Walk on Stars |
| Dataset | 解析纯 Neumann 问题, 混合 Dirichlet-Neumann 问题, 纯 Neumann 问题解重建, 二阶法向导数估计 |

> [!tip] 效果简介
> - 解析纯 Neumann 问题 上，方向导数误差/方差 为 使用 ρ_max=1 时误差低、噪声小，对比 Eq.6 的 WoSt 基线 (截断 128 步)，变化 显著更低误差，质量更优。
> - 混合 Dirichlet-Neumann 问题 上，方向导数方差 为 靠近 Neumann 边界处方差更低，对比 Eq.6 的 WoSt 基线，变化 同等计算预算下方差更小。
> - 纯 Neumann 问题解重建 上，重建精度、噪声、偏差 为 通过梯度积分重建，噪声低、偏差小，对比 Tikhonov 正则化 (小/大吸收系数)，变化 噪声显著低于小吸收系数 Tikhonov，偏差显著低于大吸收系数 Tikhonov。

## 概要

### 问题背景

蒙特卡洛方法在求解偏微分方程（PDE）时，天然支持无网格、局部求值与大规模并行计算，近年来在计算机图形学中重新受到关注。Walk on Stars（WoSt）方法将 Walk on Spheres 推广至混合 Dirichlet-Neumann 边界条件的 Poisson 方程，但**现有 WoSt 导数估计器面临一个根本瓶颈**：在边界附近——尤其是 Neumann 主导问题中——因奇异核和长随机游走导致高方差与偏差；纯 Neumann 问题甚至无法实现无偏终止，只能依赖有偏截断或 Tikhonov 正则化。

### 核心贡献

本文提出了一种**基于星星行走的鲁棒导数估计**方法，其核心数学洞察是：**调和函数的导数本身仍是调和的**。利用这一性质，作者为 Poisson 方程的一阶和二阶空间导数构造了边界积分方程（BIE），并引入**向量值反射函数 $\rho_v$** 作为关键控制变量。该反射函数同时实现两个目标：自适应调整星形区域的半径以保持反射率有界，以及通过俄罗斯轮盘赌实现无偏早期终止。整套方法将方向导数 BIE 转化为仅含单一未知函数的递归估计，从根本上解决了边界附近方差爆炸的问题。

### 方法定位

本工作在方法谱系中处于 Walk on Spheres / Walk on Stars 系列与边界积分方程蒙特卡洛求解器的交叉点。其直接前身包括：

- **Walk on Spheres 梯度估计器**（Sawhney and Crane, SIGGRAPH 2020）：基于球上积分的原始梯度估计。
- **Walk on Stars 导数估计器**（Sawhney et al., SIGGRAPH 2023; Miller et al., SIGGRAPH Asia 2024）：基于梯度球积分（Eq. 6）的 WoSt 基线，在纯 Neumann 问题中需截断或 Tikhonov 正则化。

本方法的关键改进在于：将估计目标从梯度本身转化为方向导数的递归 BIE，用反射函数替代固定半径选择，并引入无偏俄罗斯轮盘赌终止，从而在保持无偏性的同时显著压缩方差。

### 主要结果

实验覆盖纯 Neumann、混合边界、解重建、二阶法向导数和形状优化等场景，核心发现如下：

- **纯 Neumann 方向导数估计**：在同等计算预算下，本方法（$\rho_{\max}=1$）相比 WoSt 基线（截断 128 步）误差显著更低、噪声更小（Fig. 6）。
- **混合边界条件**：靠近 Neumann 边界处，本方法方差明显低于基线（Fig. 7）。
- **纯 Neumann 解重建**：通过梯度积分重建的解，噪声低于小吸收系数 Tikhonov 正则化，偏差低于大吸收系数 Tikhonov（Fig. 9）。
- **二阶法向导数**：估计量随样本数增加收敛至真值（Fig. 11）。
- **形状优化**：使用 100 次/迭代的导数估计可成功收敛至目标；1 次/迭代则发散（Fig. 12）。

### 局限与展望

本方法目前假设边界光滑，尖凹角处导数估计存在偏差（Fig. 13）；仅处理 Poisson 方程，尚未扩展至一般线性椭圆方程或 Robin 边界条件；反射率阈值 $\rho_{\max}$ 需手工设定；解重建的路径积分依赖人工选择参考点和连接路径。这些方向构成了后续工作的自然延伸空间。



### Poisson 方程的蒙特卡洛求解范式

本文关注一类核心计算问题：在复杂几何域上求解 Poisson 方程及其空间导数。给定域 $\Omega \subset \mathbb{R}^3$ 及其边界 $\partial\Omega = \partial\Omega_D \cup \partial\Omega_N$（Dirichlet 与 Neumann 分区），目标方程为：

$$
\begin{array}{rcl}
\Delta u &=& -f \quad \text{on } \Omega, \\
u &=& g \quad \text{on } \partial\Omega_D, \\
\partial_n u &=& h \quad \text{on } \partial\Omega_N.
\end{array}
$$

蒙特卡洛方法通过随机游走求解此类边值问题，其核心优势在于**无需全局网格**，可在任意空间点独立求值，天然适合局部高分辨率查询、域内稀疏采样等场景。其中，**Walk on Stars (WoSt)**（Sawhney et al., SIGGRAPH 2023; Miller et al., SIGGRAPH Asia 2024）是当前最先进的蒙特卡洛 PDE 求解器，能够处理混合 Dirichlet-Neumann 边界条件。其基本机制如 Fig. 2 所示：随机游走在域内以星形区域步进，在 Neumann 边界上反射，到达 Dirichlet 边界时终止。

然而，WoSt 的行为高度依赖边界条件类型：
- **纯 Dirichlet 问题**：退化为经典的 Walk on Spheres（Muller 1956），漫步总能终止。
- **纯 Neumann 问题**：漫步在 Neumann 边界间无限反射，**无法自然终止**（Fig. 2 左下），需借助截断或 Tikhonov 正则化等有偏策略。
- **混合边界问题**：漫步在 Dirichlet 边界终止，但在 Neumann 边界附近仍需大量反射步骤。

### 现有导数估计的瓶颈

对于形状优化、势流模拟、物理仿真等应用，**空间导数**（梯度 $\nabla u$、方向导数 $\partial_v u$、二阶法向导数 $\partial_n^2 u$）往往比解 $u$ 本身更为关键。现有 WoSt 导数估计器基于梯度球积分（Eq. 6）：

$$
\nabla u(x) = \int_{\partial \mathrm{B}(c,R)} \nabla P^{\mathrm{B}}(x,z) \, u(z) \, \mathrm{d}z + \int_{\mathrm{B}(c,R)} \nabla G^{\mathrm{B}}(x,y) \, f(y) \, \mathrm{d}y,
$$

该估计器存在两个根本性缺陷：

1. **奇异核问题**：当求值点 $x$ 靠近域边界时，积分核 $\nabla P^{\mathrm{B}}$ 呈现径向奇异性，导致方差急剧增大。这在 Neumann 主导问题中尤为严重，因为漫步长期滞留在边界附近。

2. **长随机游走与有偏终止**：纯 Neumann 问题中，解估计器必须持续反射，而导数估计器继承这一特性——漫步要么被强制截断（引入偏差），要么运行极长步数（引入高方差）。Tikhonov 正则化通过引入人工吸收项提供终止机制，但本质上在噪声与偏差之间做权衡（Fig. 9 b-c）。

### 核心洞察与本文动机

本文方法的数学基石是一条关键观察：**调和函数的导数仍为调和函数**。对于 Poisson 方程，这意味着方向导数 $\partial_v u$ 本身也满足 Poisson 方程，因而可为其构建边界积分方程（BIE）。这一洞察打开了全新的设计空间：

- 可以为**一阶和二阶空间导数**直接建立 BIE，而非通过对解 $u$ 的估计间接求导。
- 新 BIE 可引入**向量值反射函数** $\rho_v$，控制星形区域半径，使导数估计器拥有与解估计器完全不同的步进策略。
- 导数漫步可在 Neumann 边界上**无偏提前终止**，从根本上规避纯 Neumann 问题的终止困境。

基于此，本文提出 **Robust Derivative Estimation with Walk on Stars**，目标是以有界方差在边界和域内任意点鲁棒估计空间导数，尤其针对现有方法失效的 Neumann 主导场景。方法首先在纯 Neumann 问题上建立方向导数 BIE（第 4.1–4.2 节），随后扩展至混合 Dirichlet-Neumann 问题（第 4.3 节），并进一步支持二阶法向导数估计（第 4.4 节）和形状优化中的参数导数计算（第 6.4 节）。



## 核心方法与创新机理

### 问题瓶颈

现有 Walk on Stars (WoSt) 及其变体的导数估计器面临两个根本性困难。其一，基线梯度球积分估计器 (Eq. 6) 的核函数在边界附近呈现奇异性，导致高方差与偏差。其二，在纯 Neumann 问题中，WoSt 解估计器的随机游走会无限反射而无法终止；即便采用固定步数截断或 Tikhonov 正则化 (Sawhney et al., SIGGRAPH 2023)，前者引入截断偏差，后者则在小吸收系数下噪声过大、大吸收系数下偏差过高。这一瓶颈在 Neumann 主导的混合边界问题中同样存在——靠近 Neumann 边界处，基线估计器效率急剧下降。

### 核心洞察：导数的调和性

本文的关键数学洞察是：**调和函数的导数本身仍是调和函数**。对于 Poisson 方程 $\Delta u = -f$，其方向导数 $\partial_v u$ 同样满足一个 Poisson 方程。这一性质使得作者能够为方向导数构造一个与解估计器结构平行的边界积分方程 (BIE)，从而将导数估计转化为一个自洽的递归蒙特卡洛问题。

### 关键创新：三个 changed slots

**1. 方向导数 BIE 与向量值反射函数 $\rho_v$**

基线 WoSt 导数估计器直接对梯度球积分 (Eq. 6) 进行蒙特卡洛采样，该积分同时依赖 $u$ 和 $\partial_n u$ 两个未知函数。本文提出全新的方向导数 BIE (Eq. 9)：

$$
\alpha(x) \partial_v u(x) = \int_{\partial \mathrm{St}} P^{\mathrm{B}}(x,z) \left( |\rho_v(x,z)| \partial_\rho u(z) + \mu_v(z) \right) \mathrm{d}z - \int_{\partial \mathrm{St}_N} G^{\mathrm{B}}(x,z) \eta_v(z) \mathrm{d}z + \int_{\mathrm{St}} G^{\mathrm{B}}(x,y) \partial_v f(y) \mathrm{d}y
$$

其中 $\rho_v$ 是一个**向量值反射函数** (Eq. 10)，在球边界上等于 $v$，在 Neumann 边界上则结合了切向分量与法向反射：

$$
\rho_v(x,z) = \begin{cases} v & \text{if } z \in \partial \mathrm{St}_B \\ v_\Gamma - v \cdot n \frac{\nabla_\Gamma G^{\mathrm{B}}(x,z)}{P^{\mathrm{B}}(x,z)} & \text{if } z \in \partial \mathrm{St}_N \end{cases}
$$

这一重构的关键效果是：方程右侧仅含一个未知函数 $\partial_\rho u$（沿反射方向的导数），从而将问题转化为类似 WoSt 解估计器的单变量递归形式 (Eq. 13)。

**2. 反射率控制的星形区域半径**

基线 WoSt 解估计器将星形区域半径 $R$ 设为当前点到 $\partial\Omega_N$ 最近轮廓点的距离。本文的导数估计器则根据反射率幅值上限 $\rho_{\max}$ 来选择半径 (Eq. 15)：

$$
R = \min\{ \|x - z\| : z \in \partial\Omega_N, |\rho_v(x, z)| \geq \rho_{\max} \}
$$

这一设计保证了每一步的反射率幅值 $|\rho_v|$ 有界，从而控制了递归估计中乘性因子的增长，是方差有界性的核心机制 (Fig. 3 展示了两种半径选择策略的对比)。

**3. 无偏俄罗斯轮盘赌早期终止**

在纯 Neumann 问题中，解估计器的游走必须永远反射。本文利用反射率幅值 $|\rho_v|$ 作为生存概率：当 $|\rho_v| < 1$ 时，以概率 $1 - |\rho_v|$ 进行俄罗斯轮盘赌终止 (Algorithm 1, line 10)。由于 $|\rho_v|$ 在 Neumann 边界上通常小于 1，游走可以在 Neumann 边界上无偏终止，从根本上避免了基线方法的截断偏差或 Tikhonov 正则化的偏差-方差权衡。

### 创新链条的因果逻辑

上述三个 changed slots 形成一条因果链：**方向导数 BIE** 将问题转化为单变量递归 → **反射函数 $\rho_v$** 提供了控制递归幅度的数学把手 → **反射率控制半径** 保证了 $|\rho_v|$ 有界 → **俄罗斯轮盘赌终止** 利用有界的 $|\rho_v|$ 实现无偏早期终止。这条链条共同解决了基线方法在边界附近的高方差问题和纯 Neumann 问题的终止困难。

### 配套创新模块

在核心 BIE 框架之上，论文还引入了若干配套模块以扩展适用范围：

- **Dirichlet 边界法向导数**：通过从偏离球心且切于边界的球启动次级漫步来估计 $\partial_n u$ (Section 4.3, Fig. 4)，延续了 Yu et al. (2024) 的策略。
- **二阶法向导数**：递归应用方向导数估计器计算 $\partial_n^2 u$ (Eq. 16)，用于形状优化中的参数导数 PDE。
- **多面体域边积分**：通过线积分处理 Neumann 边界边缘处的 Dirac delta 贡献 (Eq. 22-23)，将方法推广至三角网格表示的几何体。

### 创新边界

需注意，该方法的适用域明确限定于 **Poisson 方程** 且假设 **光滑边界**。尖凹角处的角奇异性会导致导数估计偏差 (Fig. 13)，且尚未集成 Robin 边界条件。反射率阈值 $\rho_{\max}$ 需手工设定（消融实验表明 $\rho_{\max}=1$ 为推荐值，过大会增加噪声）。



![[assets/figures/papers/paper_list_l23_https_projects_shuangz_com_grad_wost_sa25_grad_wost_sa25_pdf/figures/001_Figure_1.jpg]]
*Figure 1: Streamlines from a potential flow simulation around marine life of vastly different scales, computed using our Monte Carlo walk on stars solver for spatial derivatives. Unlike traditional solvers, our method can compute flow gradients at arbitrary resolutions for streamline tracing in local regions of interest–whether around a single fin (a), multiple dolphins (b), or a full blue whale (c)–without requiring a background grid or a volumetric mesh adapted to the boundary geometry. Compared to prior walk on stars estimators (bottom right), our method achieves significantly lower error at equal computation time*

本文提出的鲁棒导数估计方法以**Walk on Stars (WoSt)** 随机游走求解器为基础，构建了一套针对 Poisson 方程一阶与二阶空间导数的蒙特卡洛估计流水线。其核心思想源于一个关键的数学洞察：**调和函数的导数本身仍是调和函数**。这一性质使得我们可以为 Poisson 方程的空间导数建立边界积分方程 (BIE)，从而将导数估计转化为一个仅含单一未知函数的递归估计问题。

### 流水线总览

整个方法由以下主要模块串联构成，形成从输入到输出的完整估计链路：

1. **方向导数 BIE 估计器**
   将任意方向 $v$ 上的方向导数 $\partial_v u(x)$ 表示为一个边界积分方程 (Eq. 9)。该方程将导数估计分解为三个组成部分：星形区域边界 $\partial \mathrm{St}$ 上的反射项（含未知函数 $\partial_\rho u$）、Neumann 边界 $\partial \mathrm{St}_N$ 上的已知源项 $\eta_v$、以及星形区域内部 $\mathrm{St}$ 上的体积分项。与基线 WoSt 导数估计器 (Eq. 6) 不同，该 BIE **避免了奇异核**，且可以在域边界上直接求值。

2. **反射率控制的星形区域选择**
   在每一步随机游走中，星形区域的半径 $R$ 不再简单地取为到最近 Neumann 边界轮廓点的距离（如 WoSt 解估计器所做），而是由**向量值反射函数** $\rho_v$ 的幅值上限 $\rho_{\max}$ 约束 (Eq. 15)：
   $$R = \min\{ \|x - z\| : z \in \partial\Omega_N,\ |\rho_v(x, z)| \geq \rho_{\max} \}$$
   这一设计确保了反射率幅值 $|\rho_v|$ 在游走过程中保持有界，是控制方差的关键机制。

3. **俄罗斯轮盘赌早期终止**
   当 $|\rho_v| < 1$ 时，游走以概率 $1 - |\rho_v|$ 无偏终止 (Algorithm 1, line 10)。该机制从根本上解决了纯 Neumann 问题中游走无法自然终止的瓶颈——基线 WoSt 在纯 Neumann 边界上必须无限反射，而本方法通过反射率幅值作为生存概率，实现了**无偏早期终止**，显著降低了 Neumann 主导问题中的方差。

4. **Dirichlet 边界上的法向导数估计**
   当游走到达 Dirichlet 边界 $\partial \Omega_D$ 时，需要估计该处的法向导数 $\partial_n u$。方法采用 Yu et al. (2024) 的策略：从一个**偏离球心、切于边界的球**启动次级 WoSt 游走 (Fig. 4)，从而在 Dirichlet 边界上获得法向导数估计值。

5. **二阶法向导数估计器**
   对于 Neumann 边界上的二阶法向导数 $\partial_n^2 u$，方法通过递归应用方向导数估计器来实现 (Eq. 16)。具体而言，将 $\partial_n^2 u(x)$ 表示为切于边界点的球面上的积分，其中被积函数包含一阶法向导数 $\partial_n u(z)$，后者再由方向导数估计器递归估计。

6. **多面体域边积分处理**
   在由三角形网格表示的多面体域中，Neumann 边界边缘处的几何不连续性会引入 Dirac delta 贡献。方法通过**线积分** (Eq. 22-23) 显式处理这些贡献，确保估计的无偏性。

7. **双通道形状优化**
   在 PDE 约束的形状优化应用中，方法采用**双通道策略**：首先预计算空间导数并缓存，然后在微分漫步中复用这些缓存值，从而避免嵌套漫步带来的高昂计算开销。

### 输入输出流

- **输入**：Poisson 方程的定义域 $\Omega$（含 Dirichlet 边界 $\partial \Omega_D$ 和 Neumann 边界 $\partial \Omega_N$）、源项 $f$、边界数据 $g$（Dirichlet）和 $h$（Neumann）、查询点 $x$ 及待估方向 $v$、反射率阈值 $\rho_{\max}$。
- **内部状态传递**：每一步游走从当前点 $x_k$ 出发，根据 $\rho_v$ 计算星形区域半径 $R$，在 $\partial \mathrm{St}$ 上采样下一点 $x_{k+1}$，同时传递更新后的方向 $\rho_v$ 和累积权重。
- **输出**：方向导数 $\partial_v u(x)$ 的无偏蒙特卡洛估计值。通过组合不同方向的估计，可进一步获得梯度 $\nabla u(x)$、法向导数 $\partial_n u$、二阶法向导数 $\partial_n^2 u$，乃至通过路径积分重建纯 Neumann 问题的解 (Eq. 25)。

整个流水线的设计使得估计器在**域内和边界附近均保持有界方差**，且在 Neumann 主导问题中通过早期终止显著优于基线方法。



### 3.1 核心洞察：导数的调和性

本方法的数学基础是一个关键洞察：**调和函数的导数本身仍是调和函数**。对于 Poisson 方程 $\Delta u = -f$，其方向导数 $\partial_v u$ 同样满足一个 Poisson 方程，因此可为其构造与解类似的边界积分方程 (BIE)。这一性质使得导数估计不再依赖对解 BIE 的数值微分，而是直接建立导数的边界积分表示。

### 3.2 方向导数边界积分方程 (Eq. 9)

核心 BIE 将方向导数 $\partial_v u(x)$ 表达为仅含**单一未知函数** $\partial_\rho u$ 的积分形式：

$$
\alpha(x) \partial_v u(x) = \int_{\partial \mathrm{St}} P^{\mathrm{B}}(x,z) \left( |\rho_v(x,z)| \partial_\rho u(z) + \mu_v(z) \right) \mathrm{d}z - \int_{\partial \mathrm{St}_N} G^{\mathrm{B}}(x,z) \eta_v(z) \mathrm{d}z + \int_{\mathrm{St}} G^{\mathrm{B}}(x,y) \partial_v f(y) \mathrm{d}y
$$

**变量含义**：
- $\partial \mathrm{St}$：星形区域边界，分为球面部分 $\partial \mathrm{St}_B$ 和 Neumann 边界部分 $\partial \mathrm{St}_N$
- $P^{\mathrm{B}}$、$G^{\mathrm{B}}$：球的 Poisson 核与 Green 函数
- $\rho_v(x,z)$：**向量值反射函数** (Eq. 10)，定义下一漫步步骤中导数估计的方向
- $\partial_\rho u(z)$：沿反射方向 $\rho_v$ 的方向导数，是方程中唯一的未知量
- $\mu_v(z)$：来自 Neumann 边界数据 $h$ 的已知附加项 (Eq. 11)
- $\eta_v(z)$：综合源项，包含切向导数、平均曲率贡献及源项 $f$ (Eq. 12)

与 WoSt 解估计器 (Eq. 3) 的结构对比，Eq. 9 的关键差异在于：
1. 未知函数从 $u$ 变为 $\partial_\rho u$，且被乘以反射率幅值 $|\rho_v|$
2. 新增 $\mu_v$ 和 $\eta_v$ 两项已知源项
3. 方向向量在漫步过程中动态演化，而非固定

### 3.3 反射函数与星形区域半径控制

**反射向量** $\rho_v$ 的显式表达式为 (Eq. 14)：

$$
\rho_v = v - v \cdot n \frac{z - x}{(z - x) \cdot n}
$$

其中 $v$ 为当前估计的方向向量，$n$ 为 Neumann 边界法向量，$z$ 为边界采样点。该向量位于由 $v$ 和 $n$ 张成的平面内，其幅值 $|\rho_v|$ 决定了漫步的收缩/扩张行为。

**星形区域半径选择** (Eq. 15)：

$$
R = \min\{ \|x - z\| : z \in \partial\Omega_N, |\rho_v(x, z)| \geq \rho_{\max} \}
$$

与 WoSt 解估计器以到最近轮廓点距离为半径不同，导数估计器以**反射率幅值上限** $\rho_{\max}$ 为约束选择半径。当 $|\rho_v| < 1$ 时，漫步的乘法因子收缩，使估计器在 Neumann 边界附近保持有界方差（Fig. 3 对比）。

### 3.4 递归单样本估计器与无偏终止

每步漫步的递归估计器为 (Eq. 13)：

$$
\widehat{\partial_v u}(x_k) = \frac{P^{\mathrm{B}}(x_k, x_{k+1}) \left( |\rho_v(x_k, x_{k+1})| \widehat{\partial_\rho u}(x_{k+1}) + \mu_v(x_{k+1}) \right)}{\alpha(x_k) p^{\partial \mathrm{St}}(x_k, R)(x_{k+1})}
$$

其中 $p^{\partial \mathrm{St}}$ 为方向采样下的边界采样概率密度。

**俄罗斯轮盘赌无偏终止**：当 $|\rho_v| < 1$ 时，以概率 $1 - |\rho_v|$ 终止漫步。这一机制的关键在于：
- 纯 Neumann 问题中，解估计器的漫步**必须始终反射**，永不终止（Fig. 2 左下）
- 导数估计器因 $|\rho_v|$ 可小于 1，能在 Neumann 边界附近**无偏提前终止**，避免解估计所需的长轨迹
- 终止概率与乘法因子 $|\rho_v|$ 互补，保证估计的无偏性

### 3.5 Dirichlet 边界的法向导数估计

在 Dirichlet 边界 $\partial \Omega_D$ 上，法向导数 $\partial_n u$ 通过**次级 WoSt 过程**估计：从偏离球心、切于边界的球启动漫步（Fig. 4）。该策略沿用 Yu et al. (2024) 的方法，将边界上的法向导数转化为域内导数的积分。

### 3.6 二阶法向导数估计 (Eq. 16)

Neumann 边界上的二阶法向导数 $\partial_n^2 u$ 通过递归应用方向导数估计器计算：

$$
\partial_n^2 u(x) = \int_{\partial \mathrm{B}(c,R)} \partial_{n_x} P^{\mathrm{B}}(x,z) \partial_n u(z) \mathrm{d}z + \int_{\mathrm{B}(c,R)} \partial_{n_x} G^{\mathrm{B}}(x,y) \partial_n f(y) \mathrm{d}y
$$

其中球 $\mathrm{B}(c,R)$ 切于边界点 $x$。该公式将 $\partial_n^2 u$ 表达为边界上 $\partial_n u$ 的积分，而 $\partial_n u$ 本身可通过方向导数估计器获得，形成递归结构。



## 实验与关键发现

### 核心实验结果

#### 纯 Neumann 问题方向导数估计

本文在一个具有解析解的纯 Neumann 问题上系统评估了方向导数估计的质量。基线 **WoSt 导数估计器**（基于 Eq. 6 的梯度球积分，Sawhney et al., SIGGRAPH 2023）在边界附近表现出显著的高方差和偏差，其随机游走被截断在固定步数（128 步）后终止（Fig. 6b）。相比之下，本文方法在反射率阈值 $\rho_{\max}=1$ 的设置下，于同等计算预算内获得了更准确、噪声更低的结果（Fig. 6c）。这一优势源于两个关键机制：其一，方向导数边界积分方程（Eq. 9）将未知函数缩减为单一 $\partial_\rho u$，避免了基线方法中奇异核导致的方差放大；其二，当 $|\rho_v|<1$ 时以概率 $1-|\rho_v|$ 执行俄罗斯轮盘赌无偏终止（Algorithm 1 line 10），使游走在 Neumann 边界附近能够提前结束，而非像解估计器那样必须持续反射。

![[assets/figures/papers/paper_list_l23_https_projects_shuangz_com_grad_wost_sa25_grad_wost_sa25_pdf/figures/009_Figure_6.jpg]]
*Figure 6: timetime (s) Fig. 6. Estimation of directional derivatives for an analytically defined pure Neumann problem. The baseline WoSt estimator (Section 3.3) in column (b) exhibits high variance and bias, especially near the boundary, with walks truncated after a fixed number of steps (here, 128). In contrast, using our method with the reflectance threshold $\rho _ { \mathrm { m a x } }$ = 1 in column (c) yields more accurate results for the same compute budget. Larger thresholds values, such as $\rho _ { \mathrm { m a x } }$ = 1 0 0 in column (d), lead to higher noise

消融实验揭示了反射率阈值的关键作用：当 $\rho_{\max}$ 增大至 100 时，噪声显著增加（Fig. 6d），验证了约束反射率幅值对控制方差的必要性。

#### 混合 Dirichlet-Neumann 问题方向导数估计

在混合边界条件下，随机游走到达 Dirichlet 边界即终止，轨迹长度较纯 Neumann 情形更短。即便如此，基线估计器在 Neumann 边界附近仍效率低下。本文方法在同等计算预算下于这些区域实现了更低的方差（Fig. 7），表明反射率控制的星形区域半径选择（Eq. 15）和无偏早期终止策略在混合边界场景中同样有效。

![[assets/figures/papers/paper_list_l23_https_projects_shuangz_com_grad_wost_sa25_grad_wost_sa25_pdf/figures/011_Figure_7.jpg]]
*Figure 7: Directional derivative estimation under mixed boundary conditions. Walks terminate upon reaching the Dirichlet boundary, resulting in shorter trajectories than in the pure Neumann case. Nonetheless, the baseline estimator remains inefficient near the Neumann boundary, where our method yields lower variance for the same compute budget*

#### 纯 Neumann 问题解重建

对于纯 Neumann 问题，本文通过对估计梯度进行路径积分来重建解（Eq. 25）。与 **Tikhonov 正则化**（Sawhney et al., SIGGRAPH 2023）相比，本文重建结果展现出双重优势：噪声显著低于使用小吸收系数的 Tikhonov 正则化，同时偏差显著低于使用大吸收系数的 Tikhonov 正则化（Fig. 9）。这一结果表明，通过方向导数估计器获得的高质量梯度信息能够有效支撑解的重建，避免了正则化方法中偏差-方差权衡的困境。

#### 二阶法向导数估计

本文进一步评估了二阶法向导数 $\partial_n^2 u$ 的估计器（Eq. 16），该估计器递归地应用方向导数估计器于 $\partial_n u$。在具有解析解的 PDE 上，随着样本数增加，估计均值收敛至真值，置信区间逐步收窄（Fig. 11），验证了递归估计策略的无偏性和一致性。

![[assets/figures/papers/paper_list_l23_https_projects_shuangz_com_grad_wost_sa25_grad_wost_sa25_pdf/figures/016_Figure_11.jpg]]
*Figure 11: We evaluate our estimator for the second-order normal derivative $\partial _ { n } ^ { 2 }$ u on a PDE with a known analytical solution. The plot shows the estimated mean and confidence interval for a fixed evaluation point as the number of samples increases*

#### 形状优化应用

在 PDE 约束的形状优化任务中，本文采用双通道策略：预计算空间导数并缓存，随后在微分漫步中复用。消融实验表明，每轮迭代至少需要 10 次导数估计才能实现稳定收敛；使用 1 次估计会导致优化发散，而 10 次或 100 次估计均可成功收敛至目标（Fig. 12 bottom row）。这一发现揭示了导数估计精度对优化收敛性的门槛效应。

![[assets/figures/papers/paper_list_l23_https_projects_shuangz_com_grad_wost_sa25_grad_wost_sa25_pdf/figures/017_Figure_12.jpg]]
*Figure 12: Top row: We optimize the position and scale of a fish-shaped Neumann boundary by minimizing an L ^ { 2 } loss between the solution ?? to a Poisson equation and target values specified at a sparse set of points in the domain (red dots). The optimized result, obtained using 100 walks per iteration to estimate the spatial derivatives of ??, is shown on the top right (c). Bottom row: Ablation study on the number of walks used per iteration to estimate spatial derivatives of ??. We plot the optimization loss and parameter error for 1, 10, and 100 such walks, while keeping the number of walks for the parameter derivatives ??¤ fixed*

### 失败模式与局限性

#### 尖角奇异性

本文方法假设边界光滑，在尖锐凹角处导数估计存在偏差。如 Fig. 13 所示，在势流模拟中，当边界存在尖角时，流线未能正确绕边界弯曲；而将尖角圆化后，估计梯度产生的流线与预期流动高度吻合。这一局限性源于角点处方向导数的奇异性，反射函数在该处的行为偏离了光滑边界的理论假设。

#### 解重建的路径依赖

纯 Neumann 问题的解重建依赖人工选择参考点和连接路径（Fig. 8）。在无法从参考点直接通过直线路径到达的查询点，需要链接多段线积分（如从 $p$ 到 $q$，再从 $q$ 到其他点）。这一过程目前缺乏自动化方案，影响了方法的易用性。

![[assets/figures/papers/paper_list_l23_https_projects_shuangz_com_grad_wost_sa25_grad_wost_sa25_pdf/figures/010_Figure_8.jpg]]
*Figure 8: Top row: To reconstruct the solution to a pure Neumann problem, we first fix its value at a single point in the domain. The estimated results then match the analytical reference pointwise, up to an additive constant anywhere in the domain (inset). Bottom row: In regions not directly reachable from the pinned point ??, we can recover the solution by chaining multiple line integrals, e . g . , from ?? to ??, then from ?? to all other points*

#### 反射率阈值的手工设定

反射率阈值 $\rho_{\max}$ 需要用户手工指定。虽然 $\rho_{\max}=1$ 在多数场景下表现良好，但缺乏自适应选择机制可能限制方法在极端几何或边界条件下的鲁棒性。

### 公平性说明

所有对比实验均在相同计算预算或相同时间下进行（Fig. 6, Fig. 7）。需要指出的是，反射率计算和边积分（Eq. 22-23）增加了单步计算开销，但通过更早的随机游走终止和更低的方差，整体效率仍优于基线。当前方法仅适用于 Poisson 方程，且假设边界光滑，这些前提条件在解读实验结果时需予以考虑。

### 补充图表

![[assets/figures/papers/paper_list_l23_https_projects_shuangz_com_grad_wost_sa25_grad_wost_sa25_pdf/figures/013_Figure.jpg]]
*Figure: (a) Halbach Array (c) B (reference) (b) M (input) (d) B (ours)*

![[assets/figures/papers/paper_list_l23_https_projects_shuangz_com_grad_wost_sa25_grad_wost_sa25_pdf/figures/014_Figure.jpg]]
*Figure: (b) 2nd order normal derivative*



## 定位与知识库关联

### 前置工作与基线

本方法建立在 **Walk on Stars (WoSt)** 框架之上。WoSt 由 Sawhney et al. (SIGGRAPH 2023) 提出，并由 Miller et al. (SIGGRAPH Asia 2024) 进一步扩展，其核心是利用星形区域上的边界积分方程 (BIE) 以蒙特卡洛随机游走求解具有混合 Dirichlet–Neumann 边界条件的 Poisson 方程。在 WoSt 中，解的递归单样本估计器为：

$$\widehat{u}(x_k) = \frac{P^{\mathrm{B}}(x_k, x_{k+1}) \widehat{u}(x_{k+1})}{\alpha(x_k) p^{\partial \mathrm{St}(x_k,R)}(x_{k+1})}$$

其中星形区域半径 $R$ 取为当前漫步位置到最近 Neumann 边界轮廓点及 Dirichlet 边界点的最小距离。该框架在纯 Dirichlet 问题上退化为经典的 **Walk on Spheres (WoS)** (Muller 1956)，但在纯 Neumann 问题中，由于漫步始终在 Neumann 边界上反射而永不终止，必须依赖截断或有偏的 Tikhonov 正则化 (Sawhney et al., SIGGRAPH 2023) 来强制终止。

在导数估计方面，Sawhney & Crane (SIGGRAPH 2020) 提出了基于球上梯度积分的 WoS 梯度估计器，随后 Sawhney et al. (SIGGRAPH 2023) 和 Miller et al. (SIGGRAPH Asia 2024) 将其推广至 WoSt 框架，形成基线导数估计器：

$$\nabla u(x) = \int_{\partial \mathrm{B}(c,R)} \nabla P^{\mathrm{B}}(x,z) u(z) \mathrm{d}z + \int_{\mathrm{B}(c,R)} \nabla G^{\mathrm{B}}(x,y) f(y) \mathrm{d}y$$

该基线存在两个关键瓶颈：(1) 核函数 $\nabla P^{\mathrm{B}}$ 在边界附近具有径向奇异性，导致高方差；(2) 纯 Neumann 问题中随机游走路径过长，方差和偏差随边界接近而急剧增大。

### 核心改进与因果机制

本文的核心洞察是：**调和函数的导数本身仍是调和函数**。这一数学性质使得可以为 Poisson 方程的一阶和二阶空间导数构造与解 BIE 形式平行的边界积分方程，从而将导数估计转化为一个仅含单一未知函数 $\partial_\rho u$ 的递归估计问题。

具体而言，本文引入三个关键机制，构成因果链：

1. **向量值反射函数 $\rho_v$**：将方向导数 BIE 中原本涉及两个未知函数 ($u$ 和 $\partial_n u$) 的积分重新参数化，使得右侧仅出现沿反射方向 $\rho$ 的方向导数 $\partial_\rho u$。反射函数在球边界和 Neumann 边界上分段定义 (Eq. 10)，其显式表达式为 Eq. 14：

   $$\rho_v = v - v \cdot n \frac{z - x}{(z - x) \cdot n}$$

2. **反射率控制的自适应半径选择**：不同于 WoSt 解估计器以最近轮廓点距离为半径，导数估计器以反射率幅值上限 $\rho_{\max}$ 为约束选择半径 (Eq. 15)：

   $$R = \min\{ \|x - z\| : z \in \partial\Omega_N, |\rho_v(x, z)| \geq \rho_{\max} \}$$

   这确保在每一步漫步中 $|\rho_v|$ 保持有界，从而控制估计器方差。

3. **无偏俄罗斯轮盘赌早期终止**：当 $|\rho_v| < 1$ 时，以概率 $1 - |\rho_v|$ 终止漫步。这使得在 Neumann 主导问题中漫步可以提前结束，避免解估计器所需的长程反射路径，从而在边界附近获得有界方差。

以上机制将方向导数估计转化为递归形式 (Eq. 13)：

$$\widehat{\partial_v u}(x_k) = \frac{P^{\mathrm{B}}(x_k, x_{k+1}) \left( |\rho_v(x_k, x_{k+1})| \widehat{\partial_\rho u}(x_{k+1}) + \mu_v(x_{k+1}) \right)}{\alpha(x_k) p^{\partial \mathrm{St}}(x_k, R)(x_{k+1})}$$

### 适用边界与约束条件

本方法的设计空间受以下边界约束：

- **PDE 类型**：仅限 Poisson 方程 $\Delta u = -f$，尚未扩展至一般线性椭圆方程。
- **几何光滑性假设**：方法假设边界光滑。在尖凹角处，导数估计存在角奇异性偏差 (Fig. 13 显示流线在尖角处错误弯曲，圆化角后恢复正常)。
- **边界条件类型**：目前支持 Dirichlet、Neumann 及混合边界条件，尚未集成 Robin 边界条件。
- **反射率阈值**：$\rho_{\max}$ 需手工设定。消融实验表明 $\rho_{\max}=1$ 得到准确结果，过大阈值 (如 100) 导致噪声增加 (Fig. 6c vs 6d)。
- **解重建路径依赖**：纯 Neumann 问题的解重建 (Eq. 25) 需人工指定参考点 $p_0$ 和连接路径，路径规划尚未自动化。

### 局限与开放问题

**已确认的局限**：

1. 尖凹角处导数估计存在偏差，源于角奇异性问题。
2. 仅处理 Poisson 方程，未扩展至更广泛 PDE 类。
3. 尚未集成 Robin 边界条件的导数估计。
4. 反射率阈值 $\rho_{\max}$ 需手工设定，缺乏自适应选择策略。
5. 解重建的路径积分依赖人工选择参考点和连接路径。

**开放问题**：

1. **非光滑几何扩展**：如何将方法推广至具有尖凹角的非光滑域，特别是在 concave 角附近实现稳健的导数估计？
2. **Robin 边界条件集成**：能否将反射函数框架扩展以处理 Robin 边界条件，实现统一的三类边界条件导数估计？
3. **PDE 类型推广**：能否将核心洞察 ("导数的导数仍为调和的") 推广至 Poisson 以外的更广泛 PDE 类？
4. **路径规划自动化**：如何设计自动连接查询点与参考点的路径规划方案，以消除解重建中的人工干预？
5. **凹边界加速**：如何加速 concave 边界附近漫步的收敛速度，降低该区域的方差？



## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2025/Robust_Derivative_Estimation_with_Walk_on_Stars.pdf]]
