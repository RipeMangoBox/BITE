---
title: "Solving partial differential equations in participating media"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Solving_partial_differential_equations_in_participating_media.pdf
code_link: null
project_link: https://imaging.cs.cmu.edu/volumetric_walk_on_spheres/
aliases:
- VWSVVWSV
- SPDEPM
tags:
- SIGGRAPH_2025
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "将微粒几何建模为参与介质（Poisson Boolean 模型），通过条件最近点采样替代确定性几何查询，并引入全记忆随机游走机制，从而能够在随机几何中直接估计 PDE 的期望解。"
primary_logic: "受体积渲染启发，利用 Poisson Boolean 模型的指数性质将距离采样转化为指数随机变量，进而将传统的游走球和游走星算法推广为体积化版本，无需枚举粒子配置即可高效、无偏地求解线性椭圆 PDE。"
claims:
- "体积游走球（VWoS）将确定性最近点查询替换为条件最近点采样，并在随机游走中保留空球和已采样粒子的记忆。"
- "VWoS 的估计结果与总体平均参考解一致，且运行速度提升超过 3 倍。"
- "均化方法在粒子尺寸增大或几何形状较薄的区域产生明显偏差，而 VWoS 保持无偏。"
- "耦合 VWoS 与体积路径追踪时，必须将随机游走的记忆传递到光路估计中，否则会严重影响解的正确性。"
---

# Solving partial differential equations in participating media

> [!tip] 核心洞察
> 受体积渲染启发，利用 Poisson Boolean 模型的指数性质将距离采样转化为指数随机变量，进而将传统的游走球和游走星算法推广为体积化版本，无需枚举粒子配置即可高效、无偏地求解线性椭圆 PDE。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 参与介质中偏微分方程的求解 |
| 英文题名 | Solving partial differential equations in participating media |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](https://arxiv.org/abs/2506.08237) · [Project](https://imaging.cs.cmu.edu/volumetric_walk_on_spheres/) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Volumetric walk on spheres (VWoS) and volumetric walk on stars (VWoSt) |
| Dataset | Mushroom domain, Connector domain, Bilipid membrane electrostatics |

> [!tip] 效果简介
> - Mushroom domain 上，Speedup vs ensemble averaging 为 >3× faster for same number of walks，对比 ensemble averaging，变化 >3×。
> - Connector domain 上，Speedup vs ensemble averaging 为 nearly 5× faster，对比 ensemble averaging，变化 ~5×。
> - Bilipid membrane electrostatics 上，Runtime for slice plane 为 1 sec (VWoS)，对比 11 sec (ensemble averaging)，变化 11× speedup。

## 概要

在众多物理系统中——例如生物膜的静电屏蔽、云层中的光化学臭氧生成——求解偏微分方程（PDE）时，域内往往包含大量微小粒子（离子、气溶胶等）。这些微粒几何极其复杂，使得传统 PDE 求解方法陷入两难：**总体平均法**通过对大量随机粒子配置逐一求解再取平均来估计期望解，计算成本极高；**均化法**则将微粒介质替换为等效连续介质，虽计算高效，但在粒子尺寸与几何特征尺度可比时引入显著偏差（Figure 9）。

本文的核心贡献在于提出了一类**体积化蒙特卡洛算法**，将参与介质中的 PDE 求解问题转化为对随机几何中期望解的直接估计，从根本上规避了上述两难。其核心洞察受体积渲染启发：利用 **Poisson Boolean 模型**（PBM）的指数性质，将距离采样转化为指数随机变量，从而将经典的**游走球**（walk on spheres, WoS）和**游走星**（walk on stars, WoSt）算法推广为**体积游走球**（volumetric walk on spheres, VWoS）和**体积游走星**（volumetric walk on stars, VWoSt）。

具体而言，VWoS 用**条件最近点采样**替代确定性几何查询，并在随机游走中维护**全记忆**——记录已走过的空球和已采样的粒子——以保证估计的无偏性。该方法的关键因果机制在于：PBM 的独立散射性质使得最近点距离的条件分布可解析采样，而全记忆机制则确保后续游走步骤不会与已探索区域产生虚假交互。

实验结果表明，VWoS 在 Dirichlet 边界条件下与总体平均参考解一致，且运行速度提升超过 3 倍（Figure 9）；在混合 Dirichlet-Neumann 边界条件下，VWoSt 达到近 5 倍加速（Figure 10），而在生物膜静电学场景中，线估计的加速比更超过 10,000 倍。相比之下，均化法在粒子尺寸增大或几何较薄区域出现明显偏差。消融实验进一步证实，有限记忆会导致显著偏差，全记忆是保证估计精度的关键（Figure 12）。

本文方法目前受限于线性椭圆 PDE（Laplace、Poisson、screened Poisson）、球形粒子及独立 PBM 假设，但其体积化范式为参与介质中 PDE 的无网格、无偏求解开辟了新方向。



### 问题背景：复杂微粒几何中的 PDE 求解

许多物理系统的模拟依赖于在包含大量微粒的几何域上求解偏微分方程。典型的例子包括生物膜中的静电屏蔽、大气云层中的光化学扩散过程，以及复合材料中的热传导与弹性问题。在这些系统中，域的定义为确定体积 $V$ 与随机粒子配置 $O$ 的差：

$$\Omega := V \setminus O$$

其中粒子配置 $O$ 遵循 **Poisson Boolean 模型**（Poisson Boolean model, PBM），由空间变化的密度函数 $\lambda(x)$ 控制粒子的中心分布，每个粒子为半径 $R$ 的球体（Figure 2）。研究者关心的核心量是 PDE 解关于所有可能粒子配置的期望——即**均值解**（mean solution）：

$$\overline{u}(x) := \mathbb{E}_O[u(x)] = \int_{\mathcal{P}(V)} p(O) u(x) \mathrm{d}O$$

该均值解刻画了在微粒几何随机变化下物理场的平均行为，是理解此类系统的关键。

### 现有方法的瓶颈

在本文工作之前，求解上述均值解的主流方法存在根本性的精度-效率权衡困境。

**总体平均法**（Ensemble averaging）是直接而昂贵的方法：首先采样大量随机粒子配置，然后在每个采样域上独立求解 PDE，最后对所有解取平均（Figure 3）。该方法理论上无偏，但其计算成本随配置采样数量线性增长——对于每个粒子配置都需要重新构建几何并执行完整的 PDE 求解，在高密度或大域场景下几乎不可行。

**均化法**（Homogenization）则走向另一极端。该方法将微粒几何的微观效应通过极限过程“抹平”为等效的宏观 PDE。在粒子尺寸趋于零、密度趋于无穷的极限下，原 Laplace 方程转化为 screened Poisson 方程：

$$\Delta u_{\mathrm{h}}(x) - 4\pi \lambda R u_{\mathrm{h}}(x) = 0 \ \mathrm{in} \ V, \quad u_{\mathrm{h}}(x) = \mathrm{g}(x) \ \mathrm{on} \ \partial V$$

然而，这一渐近假设在真实物理系统中常常不成立。如 Figure 1 所展示的生物膜系统，微粒的尺度往往与几何特征尺寸相当，此时均化法会引入显著偏差——尤其在粒子尺寸增大或几何形状较薄的区域，偏差尤为明显（Figure 9）。

### 核心动机：借鉴体积渲染的随机化思路

本文的核心洞察来自体积渲染（volume rendering）领域：在渲染中，指数型参与介质的透射率可以通过沿光线采样距离来无偏估计，而无需显式枚举介质中的微粒。这一思想与 Poisson Boolean 模型的指数性质高度契合——点 $x$ 到最近 Poisson 中心距离的概率密度函数具有简洁的指数形式：

$$\mathrm{p}_x^{\mathrm{dc}}(r) := \exp(-\Lambda(x,r)) \int_{\partial \mathrm{B}(x,r)} \lambda(y) \mathrm{d}A(y)$$

这意味着，传统 PDE 蒙特卡洛求解器（如游走球算法 WoS）中依赖确定性几何的**最近点查询**（closest point query），可以被替换为从 PBM 中**采样**最近边界点的随机过程。这一替换使得算法无需枚举粒子配置，即可直接在随机几何上估计均值解，从而在保持无偏性的同时大幅提升效率。

论文据此提出两个核心算法——**体积游走球**（Volumetric Walk on Spheres, VWoS）和**体积游走星**（Volumetric Walk on Stars, VWoSt）——分别针对纯 Dirichlet 边界条件和混合 Dirichlet-Neumann 边界条件，实现了参与介质中线性椭圆 PDE 的高效、无离散化求解。



## 核心方法与创新机理

本文的核心创新在于将**体积渲染的指数介质采样思想**引入 PDE 随机游走求解器，从而在无需枚举粒子配置的前提下，直接、无偏地估计参与介质中线性椭圆 PDE 的期望解。这一创新的关键因果杠杆是：将传统的**确定性几何查询**替换为基于 Poisson Boolean 模型（PBM）的**条件最近点采样**，并引入**全记忆随机游走机制**以保持估计的无偏性。

### 创新一：从确定性最近点查询到条件最近点采样

传统 Walk on Spheres（WoS）算法的每一步跳跃半径由当前点到确定性域边界的**最近点查询**决定。当域边界由随机微粒几何定义时，这一查询必须针对每一个采样的粒子配置执行，这正是总体平均法（ensemble averaging）计算代价高昂的根源。

本文的关键替换（changed slot）在于：
- **Baseline（总体平均 / 标准 WoS）**：对每个采样的粒子配置，使用 BVH 等加速结构执行确定性最近点查询。
- **Proposed（VWoS）**：利用 PBM 的指数性质，通过 **Algorithm 1** 直接从随机过程中**采样**最近点，无需实例化具体的粒子配置。

这一替换的数学基础来自 PBM 的极分解性质（Proposition 1）：在均匀 PBM 中，某点到最近粒子中心的立方距离服从指数分布，而中心位置在给定距离的球面上均匀分布。这使得最近点采样可以分解为两步：先采样距离，再采样方向（Figure 5）。在异质 PBM 中，则通过细化（thinning）策略实现（Algorithm 1）。由此，VWoS 的每一步跳跃半径由采样得到的随机最近距离决定（Figure 6 右），而非依赖确定性几何。

### 创新二：全记忆随机游走机制

直接将标准 WoS 的“无记忆”跳跃策略应用于条件最近点采样会导致严重偏差。这是因为随机游走的每一步采样会“遗忘”之前步骤已探索过的空球区域和已采样到的粒子，从而破坏估计的无偏性。

本文的第二个关键替换在于：
- **Baseline（标准 WoS）**：每步独立，无记忆。
- **Proposed（VWoS）**：维护**全记忆数据结构** $M_k$（Algorithm 3），包含：
  - **空球集合** $E(M_k)$：游走历史上所有以采样点为中心、以跳跃半径为半径的球体，这些区域内不可能存在粒子中心。
  - **已采样粒子集合** $C(M_k)$：游走历史上已采样到的粒子球体。

在每一步的**条件最近点采样**（Algorithm 4）中，PBM 的密度在空球集合内部被置零，同时已采样粒子被视为确定性边界的一部分。这确保了采样过程与游走历史一致，从而保证了估计器的无偏性（Equation 19）。

### 创新三：体积游走星（VWoSt）对混合边界条件的推广

在纯 Dirichlet 边界的 VWoS 基础上，本文进一步提出了**体积游走星（VWoSt）**，以支持微粒几何上的 Neumann 边界条件。VWoSt 将传统的游走星算法推广到体积化版本：通过采样构建星形区域（Figure 8），在该区域内利用 Green 函数进行积分估计，从而处理混合 Dirichlet-Neumann 边界条件。这一推广保持了与 VWoS 相同的记忆机制和条件采样框架。

### 与体积渲染的深层联系

本文的方法论发展明确借鉴了体积渲染中指数介质的采样技术（如 Woodcock tracking）。附录 B 揭示了 Monte Carlo PDE 求解与体积渲染之间的形式对应：WoS 的球面采样对应于表面渲染的路径追踪，而 VWoS 的条件最近点采样对应于体积路径追踪中的自由程采样。这一洞察是促成上述创新的思想源泉。



本文提出的体积化蒙特卡洛求解框架，旨在以“参与介质”的视角统一处理含随机微粒几何的线性椭圆 PDE 求解问题。其核心 pipeline 由三个逻辑阶段构成：**域建模与随机几何表征 → 条件最近点采样 → 记忆化随机游走估计**，并在需要时耦合体积路径追踪以处理非平凡边界条件。

### 域建模与随机几何表征

框架的输入是一个确定性的宏观体积 $V \subset \mathbb{R}^3$ 和一个定义于其上的 **Poisson Boolean 模型（PBM）**。PBM 由空间变化的密度函数 $\lambda(x)$ 和统一的粒子半径 $R$ 参数化，随机微粒几何 $O$ 被建模为以 Poisson 点过程为中心、半径为 $R$ 的球之并集。求解域则定义为 $\Omega := V \setminus O$（Figure 2）。这一建模选择的根本动机在于：PBM 的指数性质使得距离采样可以被高效地转化为指数随机变量的采样，从而绕过了对显式粒子配置的枚举需求。

### 条件最近点采样模块

框架的第一个核心模块是 **条件最近点采样（Algorithm 1）**。与传统游走球算法中确定性的最近点查询不同，该模块从 PBM 中采样点 $x$ 到随机边界 $\partial O$ 的最近点 $y^{\partial O}(x)$。其实现遵循两步策略（Figure 4）：
1. 先采样最近粒子中心 $c(x)$ 的距离 $r^c(x)$，其 PDF 由 PBM 的指数结构给出（Equation 8）；
2. 再由 $c(x)$ 计算最近边界点 $y^{\partial O}(x) = x + (r^c(x) - R) \cdot \mathrm{dir}(x, c(x))$。

在均匀密度情形下，最近中心距离的立方服从指数分布，中心方向在球面上均匀采样（Figure 5 左）；在异质密度情形下，通过细化（thinning）策略从增广的均匀泊松过程中按距离递增顺序采样并接受/拒绝（Figure 5 右）。这一模块是连接随机几何与 PDE 求解器的关键适配层。

### 记忆化随机游走估计模块

框架的第二个核心模块是 **体积游走球（VWoS, Algorithm 2）** 和 **体积游走星（VWoSt）** 估计器。两者均采用递归单样本蒙特卡洛积分的形式（Equation 19），但其跳跃半径不再由确定性边界决定，而是由条件最近点采样模块对随机微粒几何的采样结果确定（Figure 6 右）。

与标准游走球的关键区别在于 **全记忆机制（Algorithm 3）**：每次跳跃后，游走器维护两个累积集合（Equation 20）——
- **空球集合** $E(\mathrm{M}_k)$：所有历史跳跃球 $\mathrm{B}(x_l, r_l)$ 的并集；
- **已采样粒子集合** $C(\mathrm{M}_k)$：所有已触及的粒子球 $\mathrm{B}(c_l, R)$ 的并集。

这些记忆被馈入 **带记忆的条件最近点采样（Algorithm 4）**，确保后续跳跃不会“穿透”已知的微粒几何（Figure 7）。游走终止于到达 $\varepsilon$-壳层内的确定性边界 $\partial V$ 或已采样粒子边界时，此时以 Dirichlet 边界数据 $\mathrm{g}(x)$ 作为估计值。

VWoSt 是对 VWoS 的扩展（Section 6），通过额外采样构建星形区域（Figure 8），以处理微粒几何上的混合 Dirichlet-Neumann 边界条件。

### 输入输出流与耦合

**输入**：确定体积 $V$、PBM 参数 $(\lambda(x), R)$、边界条件 $\mathrm{g}(x)$、评估点 $x$。
**输出**：期望解 $\overline{u}(x) = \mathbb{E}_O[u(x)]$ 的无偏蒙特卡洛估计。

当边界条件本身依赖于光传输（如大气光化学示例）时，框架支持 **VWoS 与体积路径追踪（VPT）的耦合**（Figure 13）：VWoS 游走终止时的记忆集合必须传递到 VPT 光路估计中，否则会破坏估计的正确性。这一耦合揭示了随机游走记忆在跨物理过程联合仿真中的非平凡作用。

### 与基线方法的架构对比

| 方法 | 几何查询 | 记忆 | 估计目标 |
|------|---------|------|---------|
| 总体平均法 | 确定性最近点（对每个采样配置） | 无 | 先采样配置，再求解 PDE，后取平均 |
| 均化法 | 无微粒几何（以有效系数替代） | 无 | 直接求解均化 PDE |
| **VWoS/VWoSt** | 条件最近点采样（从 PBM） | 全记忆（空球 + 已采样粒子） | 直接估计期望解 |

总体平均法需要在每个采样配置上运行完整的确定性求解器，计算成本随配置数线性增长；均化法用一个等效 PDE 替代随机几何，在粒子尺寸与几何特征可比时引入显著偏差。本文框架通过条件采样与记忆机制的协同，实现了对期望解的直接、无偏估计，且无需枚举粒子配置。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_08237/figures/003_Figure_3.jpg]]
*Figure 3: Ensemble averaging is a simple but expensive method to estimate the mean solution of a PDE in a participating medium, by first sampling many random particle configurations (top row), then solving the PDE on each sampled domain (bo om row), and finally averaging the computed solutions. Our volumetric walk on spheres algorithm directly estimates the mean solution without expensive ensemble averaging*



### 问题设定与均值解定义

本文求解的核心问题是定义在随机域上的 Laplace 边值问题。域 $\Omega$ 被建模为确定体积 $V$ 与随机粒子几何 $O$ 的差：

$$\Omega := V \setminus O$$

其中粒子配置 $O$ 遵循 **Poisson Boolean 模型（PBM）**：粒子为半径 $R$ 的球，其中心集合 $\{c_n\}$ 服从密度为 $\lambda(x)$ 的非齐次 Poisson 点过程（Figure 2）。在此随机域上，Laplace 方程的 Dirichlet 边值问题为：

$$
\begin{array}{rcllcl}
\Delta u(x) &=& 0 & \mathrm{in} & \Omega, \\
u(x) &=& \mathrm{g}(x) & \mathrm{on} & \partial\Omega.
\end{array}
$$

由于域是随机的，解 $u(x)$ 本身也是随机变量。本文的目标是直接估计 **均值解（mean solution）**：

$$\overline{u}(x) := \mathbb{E}_O[u(x)] = \int_{\mathcal{P}(V)} p(O) \, u(x) \, \mathrm{d}O$$

传统方法（总体平均法）需要先采样大量粒子配置，在每个配置上独立求解 PDE，再取平均——这一流程计算成本极高（Figure 3）。

---

### 核心洞察：从确定性查询到条件采样

将传统 WoS 推广到随机几何的关键瓶颈在于：**如何在不显式枚举粒子配置的情况下，确定随机游走每一步的跳跃半径**。传统 WoS 依赖确定性最近点查询 $r^{\partial\Omega}(x)$，而本文的核心创新是将这一几何查询替换为**条件最近点采样**。

这一替换之所以可行，源于 Poisson Boolean 模型的指数性质：在均匀介质中，点 $x$ 到最近粒子中心的立方距离服从指数分布。具体而言，最短中心距离 $r^c(x)$ 的概率密度函数为：

$$\mathrm{p}_x^{\mathrm{dc}}(r) := \exp(-\Lambda(x,r)) \int_{\partial \mathrm{B}(x,r)} \lambda(y) \, \mathrm{d}A(y)$$

在均匀情况（$\lambda$ 为常数）下，该式简化为 $\mathrm{p}_x^{\mathrm{dc}}(r) = \exp(-\frac{4}{3}\pi r^3 \lambda) \, 4\pi r^2 \lambda$，即 $r^3 \sim \mathrm{Exp}(\frac{4}{3}\pi\lambda)$。采样最近中心后，最近边界点由几何关系直接计算（Figure 4）：

$$r^{\partial O}(x) = \|x - c(x)\| - R, \quad y^{\partial O}(x) = x + r^{\partial O}(x) \, \mathrm{dir}(x, c(x))$$

在异质介质中，则通过细化（thinning）策略处理：先引入虚构密度将介质均化，按距离递增顺序采样候选中心，再根据真实密度随机接受或拒绝，取首个被接受的候选中心（Figure 5）。

---

### 体积游走球（VWoS）估计器

VWoS 将传统 WoS 的递归单样本蒙特卡洛框架推广到随机几何。其核心估计器为（Equation 19）：

$$\langle \overline{u}(x_k \mid \mathrm{M}_k) \rangle := \begin{cases} \mathrm{g}(x_k), & r_k < \varepsilon, \\ \frac{\mathrm{P}(r_k)}{\mathrm{p}(r_k)} \langle \overline{u}(x_{k+1} \mid \mathrm{M}_{k+1}) \rangle, & \text{otherwise}. \end{cases}$$

其中：
- $r_k$ 是当前点 $x_k$ 到域边界 $\partial\Omega$ 的采样最短距离（综合考虑随机粒子边界 $\partial O$ 和确定边界 $\partial V$）；
- $\mathrm{P}(r_k)$ 是均匀球面上的积分核（与标准 WoS 一致）；
- $\mathrm{p}(r_k)$ 是采样 $r_k$ 时使用的概率密度；
- $\varepsilon$ 是终止阈值（$\varepsilon$-shell 近似）。

与标准 WoS 的关键区别在于跳跃半径的确定方式：VWoS 同时对随机微粒几何和确定域边界进行最近点采样，以两者中较近者作为跳跃半径（Figure 6）。

---

### 全记忆机制

VWoS 区别于无记忆传统 WoS 的关键设计是**全记忆（full memory）**数据结构 $\mathrm{M}_k$。在随机游走第 $k$ 步时，记忆包含两个集合（Equation 20）：

$$E(\mathrm{M}_k) := \bigcup_{l=0}^{k-1} \mathrm{B}(x_l, r_l), \quad C(\mathrm{M}_k) := \bigcup_{l: y_l \notin \partial V} \mathrm{B}(c_l, R)$$

- **空球集合** $E(\mathrm{M}_k)$：游走历史中所有以采样点为球心、以采样距离为半径的球。这些球内部已被验证不包含粒子中心，因此后续采样必须将 PBM 密度在这些区域内置零。
- **已采样粒子集合** $C(\mathrm{M}_k)$：游走历史中已发现并记录的所有粒子。这些粒子成为确定边界的一部分，后续步骤需对其进行确定性最近点查询。

在带记忆的条件下进行最近点采样时（Figure 7），需要分别处理两部分：
1. 对随机微粒几何采样最近点 $y^{\partial O}$，但 PBM 密度在 $E(\mathrm{M}_k)$ 内被置零；
2. 对确定边界 $\partial V$ 和已采样粒子 $C(\mathrm{M}_k)$ 查询最近点 $y^{\partial V}$。

最终取两者中距 $x_k$ 更近者作为边界点，并将新生成的空球和（如适用）新发现的粒子加入记忆。

---

### 体积游走星（VWoSt）扩展

对于微粒几何上施加 Neumann 边界条件的混合边值问题，VWoS 不再适用。VWoSt 将游走星（walk on stars）算法推广到随机几何：在每一步，首先生成一个以当前点为中心的**星形区域**（Figure 8），该区域完全包含于域内且边界由随机微粒几何和确定边界共同界定；然后在此星形区域边界上采样下一个游走点。这一扩展需要额外的采样步骤来构建星形区域，计算开销高于纯 Dirichlet 情况。

---

### 均化极限

作为理论参照，论文给出了在粒子半径 $R \to 0$、密度 $\lambda \to \infty$ 且 $4\pi\lambda R$ 保持常数的极限下，均值解收敛到的均化 PDE（Equation 25）：

$$\Delta u_{\mathrm{h}}(x) - 4\pi \lambda R \, u_{\mathrm{h}}(x) = 0 \ \mathrm{in} \ V, \quad u_{\mathrm{h}}(x) = \mathrm{g}(x) \ \mathrm{on} \ \partial V$$

这是一个 screened Poisson 方程。然而实验表明，当粒子尺寸不可忽略或几何存在薄结构时，均化解会引入显著偏差（Figure 9），这正是 VWoS/VWoSt 方法所要克服的问题。



## 实验与关键发现

### 核心结果：VWoS 与 VWoSt 的精度-效率权衡

本节报告体积游走球（VWoS）和体积游走星（VWoSt）在多个基准场景下的主实验结果。所有实验均在统一框架（Zombie）中实现，总体平均法使用共享 BVH 加速最近点查询以保证公平比较，时间测量包含粒子配置采样和 PDE 求解的完整运行时间。实验场景参数汇总于 Table 1，Dirichlet 边界条件定义见表 Table 2。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_08237/figures/014_Table_1.jpg]]
*Table 1: Scene parameters for experiments in Sections 7 and 8. We report the maximum density and corresponding mean free ball radius (average shortest distance to particle centers) of the participating media. We also report the maximum extent (maximum length across all dimensions) of the scenes. Table 2. Dirichlet boundary data g on the medium boundary $\partial$ V and particle boundary 𝜕𝑂, for experiments in Sections 7 and 8. $x _ { i }$ is the 𝑖-th coordinate of the point 𝑥 ∈ R3. 𝑦𝜕𝑉 (𝑥 ) and $r ^ { \partial \stackrel { \smile } { V } }$ ( x ) are the closest point and shortest distance (resp.) between 𝑥 and $\partial$ V

#### Dirichlet 边界条件：VWoS vs 总体平均与均化

在仅含 Dirichlet 边界的蘑菇域（mushroom domain）中，VWoS 在相同随机游走次数下运行速度比总体平均法快 **3 倍以上**，且估计结果与总体平均参考解一致（Figure 9, Section 7.1）。在连接器域（connector domain）中，加速比接近 **5 倍**（Figure 10, Section 7.1）。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_08237/figures/011_Figure_11.jpg]]
*Figure 11: Statistics for walk length (first row) and memory size (second row) for the mushroom (Figure 9(a–c), Dirichlet boundary conditions) and connector (Figure 10(a–b), Neumann boundary conditions) domains. Though the size of the empty-ball memory always equals walk length, the size of the sampled-particle memory can grow slower (in the Dirichlet case) or faster (in the Neumann case) than walk length. In both cases, increased density leads to longer walks and faster growth of sampled-particle memory*

均化方法（Marchenko and Khruslov 2008）的偏差随粒子尺寸增大而显著增长。Figure 9(a, b) 显示，当粒子半径 R 增大时，均化解与参考解之间出现肉眼可见的偏差，而 VWoS 在所有尺度下均保持无偏。在几何形状较薄的区域（Figure 9(d, e)），均化方法同样引入明显偏差，VWoS 则准确捕捉了薄区内的解变化。

#### 混合 Dirichlet-Neumann 边界条件：VWoSt 的验证

在连接器域上施加 Neumann 边界条件于微粒几何表面时，VWoSt 的估计结果与总体平均参考解一致，运行速度提升近 **5 倍**（Figure 10, Section 7.1）。误差图像（Figure 10 第三列）表明 VWoSt 正确估计了均值解，无明显系统性偏差。实验覆盖了不同粒子密度（Figure 10 第二行与第三行），VWoSt 在稀疏和密集介质中均保持稳定精度。

#### 生物膜静电学：极端加速场景

在双脂膜（bilipid membrane）静电学应用中（Section 8.1），VWoS 展现出极端加速能力：
- 切片平面估计：VWoS 耗时 **1 秒**，总体平均法耗时 **11 秒**（11 倍加速）。
- 线估计：VWoS 比总体平均法快 **超过 10,000 倍**。

这一极端加速源于总体平均法在线估计场景下需要对每个粒子配置分别求解 PDE 并沿指定线段采样，计算量随配置数线性增长；而 VWoS 直接在随机游走过程中估计线段上的均值解，避免了重复求解。

### 消融实验：记忆机制的关键作用

VWoS/VWoSt 的核心创新之一是**全记忆随机游走**——在游走过程中维护空球集合 $E(\mathrm{M}_k)$ 和已采样粒子集合 $C(\mathrm{M}_k)$（Equation (20)）。消融实验（Section 7.3, Figure 12）系统评估了记忆机制对精度和效率的影响。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_08237/figures/012_Figure_12.jpg]]
*Figure 12: We compare the bias-performance trade-of of finite memory of size one (third column) versus full memory (second column) using ensemble averaging (first column) for reference. We show error images and report runtimes for each method (the + numbers are the time to sample particle configurations for ensemble averaging). Using finite memory improves runtime only marginally (a, c) or not at all (b), yet always introduces significant bias in solution estimates. These results suggest that memory is crucial for estimation accuracy, and finite memory does not offer a favorable biasperformance trade-off for either VWoS (a, b) or VWoSt (c)*

**无记忆 VWoS**（memoryless）导致估计结果高度不准确，且运行时间反而更差。原因在于：无记忆时，随机游走可能重复进入已被探索过的空球区域或穿透已采样粒子，导致估计偏差增大且游走步数增加。

**有限记忆（size 1）**仅保留最近一步的空球和粒子信息。Figure 12 显示：
- 在蘑菇域 Dirichlet 场景（Figure 12(a, b)）中，有限记忆的运行时间改善微乎其微，却引入显著偏差。
- 在连接器域 Neumann 场景（Figure 12(c)）中，有限记忆同样无法在偏差-性能之间取得有利权衡。

这些结果表明，**全记忆对于估计精度至关重要**，有限记忆无法提供可接受的偏差-性能权衡。这一发现与直觉相符：Poisson Boolean 模型中的粒子位置在空间上独立，因此遗忘已访问区域的信息会直接破坏条件采样的正确性。

### 随机游走统计特性

Figure 11 报告了蘑菇域（Dirichlet）和连接器域（Neumann）中随机游走长度和记忆大小的统计分布。

- **空球记忆大小始终等于游走长度**：每一步都会添加一个新的空球到记忆中。
- **已采样粒子记忆的增长模式因边界条件而异**：
  - Dirichlet 情况下，粒子记忆增长慢于游走长度，因为游走倾向于在触及微粒边界后终止。
  - Neumann 情况下，粒子记忆增长可能快于游走长度，因为游走星算法会在微粒表面反射而非终止，累积更多已采样粒子。
- **密度增加导致游走变长、记忆增长加速**：在高密度介质中，平均自由球半径减小，游走需要更多步数才能到达边界，同时遇到微粒的概率增大。

### 耦合 VWoS 与体积路径追踪：记忆传递的必要性

在大气光化学概念验证系统（Figure 13, Section 8.2）中，VWoS 与体积路径追踪（VPT）耦合以模拟云层中臭氧的扩散与光化学生成。VWoS 游走终止时使用 VPT 路径估计 Dirichlet 边界条件（等于 fluence）。

**关键发现**：由于 VWoS 游走和 VPT 路径与**同一微粒几何**交互，游走过程中累积的记忆必须传递到光路估计中。Figure 13 第五列显示，正确耦合记忆对臭氧浓度估计有**非平凡的影响**——忽略记忆传递会导致解的空间分布出现显著偏差。这一发现揭示了体积模拟与体积渲染耦合时的深层一致性要求：随机游走的条件采样状态必须与光路追踪的几何查询状态保持同步。

### 失败模式与局限性的实验证据

1. **高密度场景下的效率下降**：Table 1 报告了各场景的最大密度和平均自由球半径。当密度增大时，游走长度和记忆大小均增长（Figure 11），导致单次游走的计算开销增加。虽然 VWoS 仍比总体平均法快数倍，但绝对运行时间随密度上升。

2. **VWoSt 的额外计算开销**：体积游走星算法需要额外采样步骤来构建星形区域（Figure 8），在 Neumann 边界条件下计算开销高于纯 Dirichlet 的 VWoS。Figure 10 的运行时间对比显示 VWoSt 的加速比（~5×）略低于 VWoS 在 Dirichlet 场景中的表现（3×–5×），部分原因即在于此。

3. **均化方法的系统性偏差**：Figure 9 系统展示了均化方法在以下条件下的失效模式：
   - 粒子尺寸增大时（Figure 9(a, b)）：均化假设粒子趋于零尺寸极限（Equation (25)），该渐近假设在大粒子场景下不再成立。
   - 几何薄区（Figure 9(d, e)）：均化 PDE 在薄区无法分辨微粒尺度的几何特征，导致解平滑过度。
   
   这些失效模式直接验证了论文的核心动机——均化方法在微粒尺度与几何特征尺度可比时高度不准确（Figure 1）。

### 重要图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| Figure 9 | VWoS 在所有尺度和几何条件下保持无偏；均化方法在粒子增大或薄区时偏差显著 |
| Figure 10 | VWoSt 正确估计混合边界条件下的均值解，加速比近 5 倍 |
| Figure 11 | 游走长度和记忆大小随密度增长；Neumann 条件下粒子记忆增长更快 |
| Figure 12 | 全记忆对精度至关重要；有限记忆（size 1）无法提供可接受的偏差-性能权衡 |
| Figure 13 | VWoS-VPT 耦合中记忆传递对正确估计有非平凡影响，忽略记忆导致显著偏差 |
| Table 1 | 实验覆盖从稀疏到密集的多种介质参数，最大密度场景下平均自由球半径显著减小 |

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_08237/figures/007_Figure_7.jpg]]
*Figure 7: (a) To sample the closest point $y ^ { \partial \varOmega }$ at 𝑥 conditionally on the memory M accumulated during a walk, we determine two points: First, we sample the random closest point $y ^ { \partial O }$ on the stochastic microparticle geometry, but with the PBM density zeroed out inside the spheres formed during the walk. Second, we query the closest point $y ^ { \partial V }$ on the deterministic boundary of the medium and previously sampled particles. Then, we select the closest of these two points to 𝑥, $y ^ { \partial \dot { \Omega } }$ : = $\mathrm { ~ }$ closest 𝑥, $\{ y ^ { \partial O } , y ^ { \partial V } \}$ ) . A er sampling, we add to M a new empty sphere (b), and a new particle if...

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2506_08237/figures/015_Table.jpg]]



## 定位与知识库关联

### 与现有方法的谱系关系

本文提出的体积游走球（VWoS）和体积游走星（VWoSt）算法，处于蒙特卡洛 PDE 求解与体积渲染的交叉地带，其谱系可沿两条主线追溯。

**第一条主线：游走球（Walk on Spheres, WoS）家族。** WoS 是一类经典的网格无关蒙特卡洛方法，通过在球面上递归采样来求解线性椭圆 PDE 的边值问题。其核心操作是确定点 $x$ 到域边界 $\partial\Omega$ 的最近距离 $r^{\partial\Omega}(x)$，然后在以 $x$ 为心、$r^{\partial\Omega}(x)$ 为半径的球面上均匀采样下一个游走点。本文的关键洞察在于：当域 $\Omega = V \setminus O$ 包含随机微粒几何 $O$ 时，传统的确定性最近点查询不再可行——因为 $O$ 本身是随机的。作者受体积渲染中指数介质的采样机制启发，将最近点查询替换为从 Poisson Boolean 模型（PBM）中的条件最近点采样（Algorithm 1），从而将 WoS 推广为体积化版本。这一推广的深层逻辑是：PBM 的指数性质使得距离采样可转化为指数随机变量的生成，与体积渲染中自由程采样在数学上同构（详见附录 B）。

**第二条主线：体积渲染与参与介质。** 体积路径追踪（VPT）等渲染算法通过自由程采样处理指数型参与介质，无需显式枚举散射体。本文明确指出其方法论与体积渲染的相似性，并将这一思想迁移到 PDE 求解领域。值得注意的是，这种迁移并非简单类比：PDE 求解中的随机游走需要维护对已访问区域的记忆（空球集合 $E(\mathrm{M}_k)$ 和已采样粒子集合 $C(\mathrm{M}_k)$），以确保估计的无偏性——这是体积渲染中通常不需要的机制（尽管论文在开放问题中提出了反向迁移的可能性）。

### 与基线方法的对比定位

**总体平均法（Ensemble Averaging）。** 这是最直接的基线：对 PBM 多次采样生成具体的微粒配置，在每个配置上独立求解 PDE（例如用标准 WoS），然后对解取平均。该方法在理论上无偏，但计算成本极高——每次配置采样都需要重新构建加速结构并进行完整的 PDE 求解。本文的 VWoS/VWoSt 通过直接在随机几何上进行单次随机游走来估计期望解 $\overline{u}(x) := \mathbb{E}_O[u(x)]$，避免了配置枚举。实验证据表明，在相同精度下，VWoS 的速度提升从 3 倍（Mushroom 域，Figure 9）到超过 10,000 倍（Bilipid membrane 线估计，Section 8.1）不等。这一加速的关键在于：VWoS 的每次游走同时探索了配置空间和解空间，而总体平均法则将两者分离。

**均化方法（Homogenization）。** 均化方法（Marchenko and Khruslov, 2008）在粒子尺寸趋于零、密度趋于无穷的渐近极限下，将随机几何 PDE 近似为一个确定性的 screened Poisson 方程（Equation 25）。该方法计算成本极低，但引入了系统性偏差。Figure 9 的实验清晰展示了均化的失效模式：（a, b）当粒子尺寸增大时偏差显著增加；（d, e）在几何形状较薄的区域（如连接通道），均化无法捕捉微粒几何对解的局部阻塞效应。相比之下，VWoS 在所有测试场景下保持无偏。这一对比揭示了本文方法的核心价值：在均化的渐近假设不成立的中尺度场景（微粒尺寸与几何特征尺度可比）中，VWoS 提供了精确且高效的替代方案。

### 适用边界与局限

**方程类型限制。** 当前算法仅适用于 Laplace、Poisson 和 screened Poisson 等线性椭圆 PDE。这些方程的共同特征是解满足均值性质（mean value property），这是 WoS 类算法成立的基础。论文未将方法推广到更复杂的 PDE（如线性弹性、Stokes 流、热传导方程），这些方程需要不同的随机表示。

**粒子几何限制。** 算法假设所有粒子为等半径球体（PBM 的 Boolean 模型），且粒子间满足独立 Poisson 点过程假设。这意味着以下场景不在适用范围内：
- 非球形粒子（如椭球、多面体）；
- 多尺寸粒子分布；
- 具有排斥或吸引作用的相关粒子系统（如硬核 Gibbs 过程）。

**高密度场景的效率退化。** 随机游走的记忆大小随游走长度增长（Figure 11），在高密度介质中，游走步数增加，记忆维护开销变大。虽然完整记忆对无偏性至关重要（Figure 12 的消融实验表明，有限记忆引入显著偏差），但在极高密度下可能导致效率下降。论文未提供记忆压缩或近似策略。

**混合边界条件的额外开销。** VWoSt 算法在处理 Neumann 边界条件时，需要额外采样步骤构建星形区域（Figure 8），其计算开销高于纯 Dirichlet 情况下的 VWoS。

### 开放问题

论文明确提出了若干开放方向：

1. **PDE 类型扩展。** 能否将体积化算法推广到线性弹性、热传导、Stokes 流等具有不同随机表示的其他 PDE？这需要为每类方程设计相应的随机游走机制和边界条件处理。

2. **粒子模型泛化。** 能否支持非球形、多尺寸或相关粒子的布尔模型？对于非球形粒子，最近点采样将不再能简单地从最近中心推导（Figure 4 的几何关系仅对球体成立）。

3. **记忆机制的反向迁移。** 体积渲染算法（如 VPT）是否可以借鉴本文的记忆机制以提高估计精度？这一方向暗示了 PDE 求解与渲染之间可能存在更深层的双向方法论交换。

4. **无记忆变体的可能性。** 是否可能开发仅依赖距离采样而不需要记忆的 VWoS 变体？这需要重新设计估计器以保证无偏性，目前尚不清楚是否可行。

5. **有限记忆的潜在优势。** 尽管 Figure 12 显示有限记忆在单点估计中表现不佳，但论文指出在利用空间连续性或 GPU 并行性时，有限记忆可能展现优势——这是一个需要进一步探索的工程方向。

6. **非指数介质的处理。** 当前方法依赖 PBM 的指数性质进行距离采样。如何处理非独立散射或非指数型参与介质（如具有空间相关性的微粒分布）仍是一个开放问题。



## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Solving_partial_differential_equations_in_participating_media.pdf]]
