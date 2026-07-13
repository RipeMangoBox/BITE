---
title: "Unbiased Differential Visibility Using Fixed-Step Walk-on-Spherical-Caps And Closest Silhouettes"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Unbiased_Differential_Visibility_Using_Fixed_Step_Walk_on_Spherical_Caps_And_Closest_Silhouettes.pdf
project_link: null
code_link: null
aliases:
- FSWSCWWAR
- UDVUFSWSCCS
tags:
- SIGGRAPH_2025
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "将速度场构造建模为拉普拉斯方程的Dirichlet边界值问题，并利用Walk-on-Spheres的on-demand Monte Carlo求解特性，结合固定步数终止和球面上最近剪影的锥查询，构建满足连续性和边界条件的速度场。"
primary_logic: "微分可见性所需的速度场本质上可以是调和函数；通过固定步数WoS/WoSC随机游走并抓取最近边界值，得到的非调和场仍满足所需条件，从而避免随机终止的epsilon-shell偏差并提升效率；将问题投影到单位球面上进行随机游走，避开了平面域中复杂遮挡的边界处理。"
claims:
- "方向导数估计器在平面和球面上均与有限差分参考匹配，验证了公式(27)(34)的正确性。"
- "在Voronoi-bunny阴影梯度任务上，本方法的L1误差为0.032，低于WAS的0.053和PSDR-WAS的0.069。"
- "在中心方块场景，本方法的高采样结果与FD参考一致，而WAS和PSDR-WAS噪声更大。"
- "WoSC步数消融实验显示M=1即可达到较好的精度与效率平衡，增加步数收益递减。"
---

# Unbiased Differential Visibility Using Fixed-Step Walk-on-Spherical-Caps And Closest Silhouettes

> [!tip] 核心洞察
> 微分可见性所需的速度场本质上可以是调和函数；通过固定步数WoS/WoSC随机游走并抓取最近边界值，得到的非调和场仍满足所需条件，从而避免随机终止的epsilon-shell偏差并提升效率；将问题投影到单位球面上进行随机游走，避开了平面域中复杂遮挡的边界处理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于固定步长球冠行走和最近剪影的无偏微分可见性 |
| 英文题名 | Unbiased Differential Visibility Using Fixed-Step Walk-on-Spherical-Caps And Closest Silhouettes |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](https://research.nvidia.com/labs/prl/wu2025diffvisibility/diffvisibility.pdf) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Fixed-Step Walk-on-Spherical-Caps (WoSC) for Warped-Area Reparameterization |
| Dataset | Voronoi-bunny shadows gradient (x-translation), Center box gradient (x-translation), Mirror shadows gradient |

> [!tip] 效果简介
> - Voronoi-bunny shadows gradient (x-translation) 上，Mean L1 error vs FD reference 为 0.032，对比 WAS: 0.053, PSDR-WAS: 0.069，变化 -0.021 / -0.037。
> - Center box gradient (x-translation) 上，Visual match to FD 为 Close match (high spp)，对比 WAS, PSDR-WAS show more noise/bias，变化 N/A。
> - Mirror shadows gradient 上，Visual match to FD 为 Matches FD reference，对比 Projective sampling fails to capture mirrored shadows，变化 N/A。

## 概要

在可微渲染中，微分可见性（differential visibility）是计算场景参数导数时最具挑战性的环节之一。其核心困难在于，可见性变化引入的边界路径积分项需要高效且无偏的估计。现有的**warped-area reparameterization**方法通过散度定理将边界积分转化为面积积分，避免了显式采样不连续边界，但其速度场（velocity field）构造依赖于加权平均插值，存在三个根本缺陷：**估计有偏**（权重函数无界导致的数值不稳定）、**散度支撑窄**（采样效率低）、以及对复杂3D遮挡场景的**鲁棒性不足**。

本文提出了一种基于**固定步数球冠行走（Fixed-Step Walk-on-Spherical-Caps, WoSC）**的无偏微分可见性方法。核心洞察在于：微分可见性所需的速度场本质上可以是**调和函数**——将其建模为拉普拉斯方程的Dirichlet边界值问题，并利用Walk-on-Spheres（WoS）的按需蒙特卡洛求解特性来构造。通过**固定步数终止**随机游走并结合球面上**最近剪影的锥查询**，得到的非调和速度场仍满足warped-area reparameterization所需的连续性和边界条件，从而消除了传统随机终止的epsilon-shell偏差，并显著提升了采样效率。进一步，将问题投影到以着色点为中心的**单位球面**上进行随机游走，避开了平面域中复杂遮挡的边界处理困难。

实验表明，在Voronoi-bunny阴影梯度任务上，本方法的L1误差为**0.032**，显著优于WAS（0.053）和PSDR-WAS（0.069）；方向导数估计器在平面和球面上均与有限差分参考一致；在逆渲染优化中，本方法能从初始圆盘收敛到目标花朵形状，而基线方法因梯度不准确未能收敛。消融实验进一步证实，**M=1步**的WoSC即可达到较好的精度与效率平衡，增加步数收益递减。



### 可微渲染中的微分可见性难题

可微渲染的核心任务之一是计算渲染结果对场景参数（如物体位置、几何形状）的导数。根据微分路径积分理论，该导数可分解为两项：一项是路径内部被积函数的导数，可通过自动微分处理；另一项是**边界项**，源于可见性不连续导致的积分域边界移动效应。边界项的正确估计是实现无偏可微渲染的关键瓶颈。

在路径空间中，边界项表现为对可见性边界上的路径积分：

$$I_{\mathrm{bdr}} = \int_{\partial\Omega} f(\bar{p}) V(\bar{p}) \mathrm{d}\dot{\mu}(\bar{p})$$

直接采样边界路径在3D场景中极其困难，因为可见性边界由复杂的遮挡几何决定，且边界测度为零。

### Warped-Area Reparameterization：思路与缺陷

**Warped-area reparameterization (WAR)** 方法（Bangaru et al., ACM Trans. Graph. 2020; Xu et al., ACM Trans. Graph. 2023）通过散度定理将边界积分转化为面积积分，从而避免直接采样边界：

$$I_{\mathrm{bdr}} = \int_{\Omega} \sum_{K=0}^{N-1} \left[ \nabla \cdot \left( f_K \pmb{v}_K \right) \right] (\pmb{p}_K) \mathrm{d} \mu (\bar{\pmb{p}})$$

这一转换的关键在于构造一个满足特定条件的**速度场** $\pmb{v}$：在可见区域内部连续，在可见性边界处与边界运动向量匹配。然而，现有WAR方法的速度场构造存在三个根本缺陷：

1. **有偏估计**：现有方法（如WAS, Bangaru et al. 2020）通过加权平均插值构造速度场（Eq. 7），其权重函数无界，导致估计存在系统性偏差，在复杂遮挡场景下尤为严重。

2. **数值不稳定**：加权平均插值的权重函数在靠近边界时趋于无穷，使得蒙特卡洛估计的方差急剧增大，产生噪声严重的梯度图像（Fig. 1, Fig. 9）。

3. **采样效率低**：速度场的散度仅在边界附近的狭窄区域内非零，导致大部分采样点的贡献为零，浪费了大量计算资源。

### 核心洞察：从插值到调和函数

本文的核心洞察在于重新审视速度场的数学本质。速度场所需满足的条件——内部连续、边界匹配——本质上是一个**Dirichlet边界值问题**。因此，速度场可以自然地构造为拉普拉斯方程的解：

$$\Delta v(p) = 0 \text{ on } \mathcal{B}^{\mathrm{wa}}, \quad v(p) = v^{\partial}(p) \text{ on } \partial\mathcal{B}^{\mathrm{wa}}$$

这一视角将速度场构造从启发式插值提升为具有坚实数学基础的调和函数求解问题。调和函数具有良好的光滑性和有界性，天然避免了权重函数无界带来的偏差和方差问题。

### 从WoS到固定步数WoSC：技术路径

求解拉普拉斯方程的自然工具是**Walk-on-Spheres (WoS)** 算法——一种按需（on-demand）的蒙特卡洛求解器，通过随机游走从内部点抓取边界值来估计解。然而，原始WoS需要随机步数直到进入边界的ε-shell才终止，这会引入ε-shell偏差。

本文提出**固定步数WoS**：在固定步数M后强制终止随机游走，并直接抓取最近边界点的值。这样得到的场虽然不再严格调和，但仍满足WAR所需的连续性和边界条件（Fig. 3, Fig. 4），同时消除了ε-shell偏差，并使计算代价可控。

进一步，为了处理3D场景中的复杂遮挡，本文将问题**投影到以着色点为中心的单位球面**上进行，提出**固定步数球冠行走（Walk-on-Spherical-Caps, WoSC）**，并设计了高效的**锥查询（cone query）**来寻找球面上的测地线最近剪影点（Fig. 6, Fig. 7）。这一球面投影策略巧妙避开了平面域中复杂遮挡边界的处理难题。

### 方法概览

整体方法流程为：将可见表面区域投影到单位球面 → 通过锥查询高效定位球面边界 → 在球面上执行固定步数WoSC估计速度场 → 利用方向导数将球面速度场映射回平面并计算散度。这一pipeline在Voronoi-bunny阴影梯度任务上实现了L1误差0.032，显著优于WAS的0.053和PSDR-WAS的0.069（Fig. 1），并在逆渲染优化中展现了从初始圆盘收敛到目标花朵形状的能力（Fig. 12），而基线方法因梯度不准确未能收敛。



## 核心方法与创新机理

本方法的核心创新在于将微分可见性中的速度场构造问题重新建模为**拉普拉斯方程的Dirichlet边界值问题**，并利用**固定步数球冠行走（Fixed-Step WoSC）** 在着色点处的单位球面上进行按需Monte Carlo求解。这一范式转换从根本上解决了现有warped-area reparameterization方法的三个瓶颈：

### 1. 速度场构造：从加权平均插值到调和场求解

**Baseline缺陷**：WAS（Bangaru et al., ACM Trans. Graph. 2020）和PSDR-WAS（Xu et al., ACM Trans. Graph. 2023）的速度场构造基于加权平均插值（Eq. 7），其权重函数在边界附近无界，导致估计有偏且数值不稳定；同时，速度场的散度支撑集中在边界附近极窄的区域内，采样效率低下。

**本方法方案**：将速度场$\boldsymbol{v}$定义为满足Dirichlet边界条件的拉普拉斯方程解（Eq. 12）：
$$\Delta v(p) = 0 \text{ on } \mathcal{B}^{\mathrm{wa}}, \quad v(p) = v^{\partial}(p) \text{ on } \partial\mathcal{B}^{\mathrm{wa}}$$

这使得速度场在可见表面区域$\mathcal{B}^{\mathrm{wa}}$内为调和函数，天然满足warped-area reparameterization所需的连续性和边界条件，且散度支撑更广，显著提升了采样效率。

### 2. 随机游走终止策略：从epsilon-shell到固定步数

**Baseline缺陷**：传统WoS算法以随机步数行走，直至进入边界附近的epsilon-shell才终止。这不仅引入epsilon-shell偏差，且终止步数不可控，计算代价难以预测。

**本方法方案**：引入**固定M步终止**策略（Eq. 20）：
$$\boldsymbol{v}^{(M)}(\boldsymbol{p}) = \frac{1}{|B_{\boldsymbol{p}}|} \int_{B_{\boldsymbol{p}}} \boldsymbol{v}^{(M-1)}(\boldsymbol{y}) \mathrm{d}\boldsymbol{y}$$

随机游走在M步后强制终止，并抓取最近边界点的值作为估计。由此得到的场虽非严格调和，但仍满足warped-area reparameterization的所有条件。消融实验（Fig. 10）表明，**M=1即可达到较好的精度-效率平衡**，增加步数收益递减。这一设计消除了epsilon-shell偏差，并使计算代价与速度场平滑度可调控。

### 3. 行走域：从平面到单位球面

**Baseline缺陷**：先前方法在着色点处的切平面（2D切线圆）上进行WoS行走，需要处理复杂的3D遮挡边界投影问题。

**本方法方案**：将可见表面区域投影到以着色点为中心的单位球面上，在球面上执行**球冠行走（WoSC）**（Eq. 32）：
$$\boldsymbol{u}^{(M)}(\boldsymbol{q}) = \frac{1}{|C_{\boldsymbol{q}}|} \int_{C_{\boldsymbol{q}}} \boldsymbol{u}^{(M-1)}(\boldsymbol{y}) \mathrm{d}\boldsymbol{y}$$

这一投影将平面域中复杂的遮挡边界处理转化为球面上的自然边界问题。配合新设计的**锥查询（cone query）** 算法（Algorithm 5），可高效找出球面上测地线距离最近的剪影点，替代了传统的欧氏最近点查询。该方法在镜像阴影等复杂场景中表现出色——投影采样方法（Zhang et al., ACM Trans. Graph. 2023）无法捕获镜面反射的阴影梯度，而本方法的结果与有限差分参考一致（Fig. 11）。

### 创新点总结

| 改进维度 | Baseline | 本方法 | 关键优势 |
|---------|----------|--------|---------|
| 速度场构造 | 加权平均插值（有偏、不稳定） | 拉普拉斯方程求解（无偏、阶跃平滑） | 消除偏差，提升数值稳定性 |
| 行走终止 | 随机步数+epsilon-shell | 固定M步+最近边界点抓取 | 消除epsilon-shell偏差，代价可控 |
| 行走域 | 切平面（2D） | 单位球面（球冠行走） | 简化边界处理，支持复杂遮挡 |
| 最近点查询 | 欧氏距离 | 测地线锥查询 | 适配球面几何，提升查询效率 |

这些创新共同构成了一个**鲁棒、无偏且高效**的微分可见性计算框架，在Voronoi-bunny阴影梯度任务上实现了0.032的L1误差，显著优于WAS的0.053和PSDR-WAS的0.069（Fig. 1），并在逆渲染优化中展现出准确的梯度信息，使遮挡物形状能从初始圆盘收敛到目标花朵形状（Fig. 12）。



本文提出的方法旨在为可微渲染中的微分可见性计算提供一种无偏、鲁棒且高效的warped-area reparameterization方案。其核心流程围绕**固定步数球冠行走（Fixed-Step WoSC）** 构建速度场，并将该速度场嵌入标准的路径空间微分框架中。

### 输入与输出

- **输入**：一条采样的完整光路 $\bar{\pmb{p}} = \pmb{p}_0, \pmb{p}_1, \dots, \pmb{p}_N$，以及待求导的场景参数 $\theta$（如物体的平移向量）。
- **输出**：该光路对参数 $\theta$ 的微分贡献，即微分路径积分 $\partial_\theta I$ 的一个无偏蒙特卡洛估计。

### 核心Pipeline

整体计算流程可分解为以下五个串行模块，对应于路径上每个顶点 $\pmb{p}_K$（$0 \le K \le N-1$）的处理：

**1. 球面投影（Spherical Projection）**
将着色点 $\pmb{p}_{K+1}$ 可见的局部表面区域 $\mathcal{B}^{\mathrm{wa}}$ 投影到以 $\pmb{p}_K$ 为中心的单位球面 $\mathcal{S}^2$ 上。此步骤将平面域中复杂的遮挡边界问题转化为球面上的可见性剪影（silhouette）处理，为后续球面随机游走奠定几何基础（§6.1）。

**2. 锥查询——测地线最近剪影（Cone Query for Geodesic Closest Silhouette）**
在球面上高效寻找当前点到可见性边界 $\partial \mathcal{B}^{\mathrm{wa}}$ 的测地线最近点 $\mathrm{cp}_{\mathcal{S}^2}(\pmb{q})$。该模块使用锥查询（cone query）替代传统的欧氏最近点查询，通过BVH加速结构在球面几何上快速定位最近剪影点，并同时返回该点到边界的测地线距离 $A(\pmb{q})$（Algorithm 5, §6.1）。锥查询是保证速度场边界条件正确赋值的关键，也是当前GPU实现中的主要计算瓶颈。

**3. 固定步数球冠行走（Fixed-Step WoSC）**
在球面上执行固定步数 $M$ 的随机游走，以估计速度场 $\pmb{u}^{(M)}(\pmb{q})$。每一步从当前点 $\pmb{q}$ 出发，在以其到最近剪影的测地线距离 $A(\pmb{q})$ 为半角的球冠 $C_{\pmb{q}}$ 内均匀采样下一个点 $\pmb{y}$；经过 $M$ 步后，抓取终点的最近边界速度值 $\pmb{v}^{\partial}$ 作为估计（Algorithm 6, §6.2）。此模块的核心机制是：通过固定步数终止（而非传统WoS的随机步数进入epsilon-shell）消除了epsilon-shell偏差，同时将计算代价与速度场平滑度解耦——$M$ 越大速度场越平滑，但计算量线性增长。

**4. 速度场与散度计算（Velocity & Divergence Computation）**
利用球面速度场的方向导数公式（Eq. 34），将球面上的速度场 $\pmb{u}^{(M)}$ 映射回平面表面，得到平面速度场 $\pmb{v}^{(M)}$ 及其散度 $\nabla \cdot \pmb{v}^{(M)}$。方向导数的计算依赖于球冠边界上的积分估计，同时包含了球冠半径变化引起的缩放项（Algorithm 7, §5.2, §6.2）。

**5. Warped-Area积分估计**
将散度 $\nabla \cdot \pmb{v}^{(M)}_K(\pmb{p}_K)$ 代入warped-area面积积分公式（Eq. 3），与路径顶点上的被积函数 $f_K$ 相乘，得到该路径段对边界项 $I_{\mathrm{bdr}}$ 的贡献。最终与内部项 $\partial_\theta f$ 的估计相加，形成完整的微分路径积分估计。

### 模块间的因果依赖

上述模块形成一条严格的因果链：
- **模块1→2**：球面投影定义了锥查询的搜索域；
- **模块2→3**：锥查询提供的最近剪影距离 $A(\pmb{q})$ 直接决定了球冠采样的半径，是WoSC随机游走能够正确触及边界的前提；
- **模块3→4**：WoSC估计的速度场 $\pmb{u}^{(M)}$ 是方向导数计算的输入，其统计质量（偏差、方差）决定了散度估计的准确性；
- **模块4→5**：散度是warped-area积分的被积函数，其支撑集宽度和数值稳定性直接影响最终梯度估计的效率与鲁棒性。

### 关键设计决策

本框架的三个关键设计决策直接回应了基线方法（**WAS**, Bangaru et al., 2020; **PSDR-WAS**, Xu et al., 2023）的瓶颈：

| 设计决策 | 解决的瓶颈 | 实现机制 |
|---------|-----------|---------|
| 速度场建模为拉普拉斯方程Dirichlet问题 | 加权平均插值的有偏估计与无界权重 | 利用调和函数的均值性质，通过WoS/WoSC进行无偏Monte Carlo求解 |
| 固定步数终止+最近边界抓取 | 随机终止的epsilon-shell偏差 | 固定$M$步后直接取最近边界值，构建连续非调和但满足边界条件的速度场 |
| 球面域随机游走+锥查询 | 平面域复杂遮挡边界处理 | 将问题投影到单位球面，用测地线最近剪影替代欧氏最近点查询 |

消融实验（Fig. 10）表明，$M=1$ 即可在精度与效率之间达到最佳平衡——增加步数虽可略微降低L1误差，但收益递减，且在等时比较下额外计算成本不划算。这一发现验证了固定步数终止策略的实用价值。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_research_nvidia_com_labs_prl_wu2025diffvisibility_diffvisibility_p/figures/016_Figure_12.jpg]]
*Figure 12: (d) Loss Fig. 12. We present an inverse rendering example that optimizes the occluder’s shape by only looking at shadows. The target shape is shown in (a). Starting from an initial shape in (b), our method can converge to the desired shape in (c). We compare the convergence rates between our method and the baseline method [Bangaru et al. 2020] in (d)*

![[assets/figures/papers/paper_list_l4_https_research_nvidia_com_labs_prl_wu2025diffvisibility_diffvisibility_p/figures/001_Figure_1.jpg]]
*Figure 1: We introduce a robust method to compute warped-area reparameterization for differential visibility. The key ingredient is a novel velocity construction using fixed-step walk-on-spherical-caps (WoSC) accelerated by cone queries (illustrated in the left image) that find the geodesic closest distance to the boundaries on a unit sphere. In this example, we show derivatives of the shadows, cast by a Voronoi-bunny model [Mehta et al. 2022] with 168k triangles under an area light source, with respect to the ??-translation of the bunny. In (a), we present the gradient image computed by our method with a high sample count. In (b)–(d), we show equal-sample comparisons with the baseline methods (WAS [...*



### 问题建模：速度场作为拉普拉斯方程的边值问题

warped-area reparameterization的核心是将边界路径积分转化为面积积分。对于路径段 $\overline{\mathbf{P}_K \mathbf{P}_{K+1}}$，需要在可见表面区域 $\mathcal{B}^{\mathrm{wa}}$ 上构造一个连续速度场 $\boldsymbol{v}: \mathcal{B}^{\mathrm{wa}} \to T_{\mathbf{p}_K}(\mathcal{B})$，满足两个条件：(1) 在可见区域内部连续可微；(2) 在可见性边界 $\partial\mathcal{B}^{\mathrm{wa}}$ 上取特定的边界值 $\boldsymbol{v}^{\partial}$。

先前方法（**WAS**, Bangaru et al., ACM Trans. Graph. 2020）通过加权平均插值构造速度场（Eq. 7），其权重函数无界，导致估计有偏且数值不稳定。本文的关键洞察是：**速度场本质上可以是调和函数**，因此将其构造建模为拉普拉斯方程的Dirichlet边值问题：

$$\Delta \boldsymbol{v}(\mathbf{p}) = 0 \quad \text{on } \mathcal{B}^{\mathrm{wa}}, \qquad \boldsymbol{v}(\mathbf{p}) = \boldsymbol{v}^{\partial}(\mathbf{p}) \quad \text{on } \partial\mathcal{B}^{\mathrm{wa}}$$

其中 $\boldsymbol{v}^{\partial}$ 是边界运动向量，描述当场景参数 $\theta$ 沿方向 $d$ 变化时，可见性边界点的运动速度。其计算分两步（Fig. 5）：先将整个圆沿 $d$ 方向平移，再缩放使圆仍与边界相切。

### 固定步数WoS：消除epsilon-shell偏差

经典Walk-on-Spheres算法利用调和函数的均值性质：

$$\boldsymbol{v}(\mathbf{p}) = \frac{1}{|\partial B(\mathbf{p}, r)|} \int_{\partial B(\mathbf{p}, r)} \boldsymbol{v}(\mathbf{z}) \, \mathrm{d}\mathbf{z}$$

通过递归采样直至进入边界的epsilon-shell。这引入两个问题：(1) epsilon-shell偏差；(2) 随机步数导致计算代价不可控。

本文提出**固定步数WoS**：在 $M$ 步后强制终止，抓取最近边界点的值作为估计。速度场的递推定义为：

$$\boldsymbol{v}^{(M)}(\mathbf{p}) = \frac{1}{|B_{\mathbf{p}}|} \int_{B_{\mathbf{p}}} \boldsymbol{v}^{(M-1)}(\mathbf{y}) \, \mathrm{d}\mathbf{y}$$

其中 $\boldsymbol{v}^{(0)}(\mathbf{p}) = \boldsymbol{v}^{\partial}(\text{cp}(\mathbf{p}))$，$\text{cp}(\mathbf{p})$ 返回 $\mathbf{p}$ 在边界上的最近点。$M$ 步后的速度场 $\boldsymbol{v}^{(M)}$ 不再是调和函数，但仍是连续的，且满足warped-area reparameterization所需条件。消融实验（Fig. 10）表明 $M=1$ 即可达到较好的精度与效率平衡。

### 方向导数与散度估计

为计算面积积分中的散度项 $\nabla \cdot \boldsymbol{v}$，需要速度场沿任意方向 $d$ 的方向导数。对于 $M$ 步固定步WoS，方向导数估计器为：

$$\partial_d \boldsymbol{v}^{(M)}(\mathbf{p}) = -\frac{2}{D} \partial_d D(\mathbf{p}) \cdot \boldsymbol{v}^{(M)}(\mathbf{p}) + \frac{1}{\pi D^2} \int_{\partial B_{\mathbf{p}}} \boldsymbol{v}^{(M-1)}(\mathbf{z}) \left( \mathbf{d} \cdot (\mathbf{g}_D + \mathbf{n}^{\partial}(\mathbf{z})) \right) \mathrm{d}\mathbf{z}$$

其中 $D$ 是 $\mathbf{p}$ 到边界的距离，$\mathbf{g}_D$ 是距离梯度，$\mathbf{n}^{\partial}$ 是边界法向。该估计器在平面场景上与有限差分参考一致（Fig. 8 上行）。

### 球面投影与WoSC

平面上的WoS在处理复杂3D遮挡时，可见区域的边界几何复杂。本文的核心创新是将问题**投影到以着色点为中心的单位球面**上，在球面上执行随机游走。

球面上 $M$ 步WoSC的速度场递推定义为：

$$\boldsymbol{u}^{(M)}(\mathbf{q}) = \frac{1}{|C_{\mathbf{q}}|} \int_{C_{\mathbf{q}}} \boldsymbol{u}^{(M-1)}(\mathbf{y}) \, \mathrm{d}\mathbf{y}$$

其中 $C_{\mathbf{q}}$ 是以 $\mathbf{q}$ 为中心的球冠区域。球面上的方向导数估计器为：

$$\partial_d \boldsymbol{u}^{(M)}(\mathbf{q}) = -\frac{\sin A}{1 - \cos A} \partial_d A(\mathbf{q}) \cdot \boldsymbol{u}^{(M)}(\mathbf{q}) + \frac{1}{|C_{\mathbf{q}}|} \int_{\partial C_{\mathbf{q}}} \boldsymbol{u}^{(M-1)}(\mathbf{z}) \left( \hat{V}_d^{\partial}(\mathbf{z}) \cdot \hat{\mathbf{n}}^{\partial}(\mathbf{z}) \right) \mathrm{d}\mathbf{z}$$

其中 $A$ 是球冠的半角，$\hat{V}_d^{\partial}$ 是球面边界运动向量，$\hat{\mathbf{n}}^{\partial}$ 是球冠边界法向。该估计器在球面上同样与有限差分参考匹配（Fig. 8 下行）。

### 锥查询加速最近剪影点

球面上需要高效查找测地线最近剪影点 $\text{cp}_{S^2}$。本文提出**锥查询**（Algorithm 5）：从查询点出发，沿测地线方向发射一个锥体，通过BVH遍历快速定位球面边界上的最近点。锥查询的初始半角参数在查询速度与速度场平滑度之间权衡，是当前未完全解决的开放问题。



## 实验与关键发现

### 核心验证：方向导数估计器

方法正确性的基础在于平面与球面上的方向导数估计器。论文通过有限差分（FD）参考图像对两者进行了严格验证（Fig. 8）。在平面表面（上排）和球面表面（下排）上，由公式(27)和(34)给出的估计方向导数均与FD参考高度一致，确认了从球面速度场映射回平面并计算散度这一关键步骤的数学正确性。该验证构成了后续所有微分可见性实验的理论可信度基础。

![[assets/figures/papers/paper_list_l4_https_research_nvidia_com_labs_prl_wu2025diffvisibility_diffvisibility_p/figures/011_Figure_8.jpg]]
*Figure 8: (c) FD ref. Fig. 8. Validation of our directional derivative estimators on flat surfaces (top row) and spherical surfaces (bottom row; visualized by projecting the hemisphere onto a disk). (a) Given values at the boundaries (shown in blue segments) as input, we compute the interior values using our fixed-step estimators with ?? = 1. The estimated derivatives with respect to a direction ?? in (b) using Eqs. (27) and (34) match the references in (c) computed by finite differences*

### 主结果：阴影梯度精度

**Voronoi-bunny阴影梯度（x方向平移）** 是最核心的定量基准。如Fig. 1所示，本方法在高采样数下产出的梯度图像与FD参考高度吻合。在等样本数比较中，本方法的平均L1误差为**0.032**，显著优于WAS（Bangaru et al., 2020）的0.053和PSDR-WAS（Xu et al., 2023）的0.069，相对误差降低约40%–54%。该场景包含大量细碎遮挡边界，对速度场的连续性和散度支撑宽度构成严峻考验，本方法的优势直接源于固定步数WoSC构造的非调和但连续的速度场，以及球面上测地线最近剪影锥查询对边界值的准确抓取。

**中心方块场景（Fig. 9）** 进一步验证了warped-area reparameterization算法本身。在高采样数下，本方法的结果与FD参考几乎无法区分；而在等样本数比较中，WAS和PSDR-WAS均表现出更明显的噪声或偏差。这表明固定步数终止消除了原始WoS中epsilon-shell引入的偏差，并使估计器的方差特性更优。

**镜面阴影场景（Fig. 11下排）** 测试了方法在复杂间接可见性下的鲁棒性。本方法成功捕获了经镜面反射的阴影梯度，与FD参考一致；而基于显式不连续采样的Projective Sampling方法（Zhang et al., 2023）完全无法处理此类间接可见性边界。这归因于本方法将问题投影到单位球面上进行随机游走，天然地将直接与间接遮挡统一处理为球面上的剪影边界，无需显式枚举所有可见性事件。

### 消融研究：WoSC步数M的影响

Fig. 10展示了等时间预算下不同WoSC步数M的消融结果。核心发现是：**M=1即可达到最佳的代价–精度平衡**。增加步数M虽能略微降低L1误差，但收益递减明显——额外的球冠行走步骤带来的计算成本线性增长，而速度场平滑度的提升对最终散度估计的改善有限。这一结论具有重要实践意义：单步WoSC既避免了随机终止的epsilon-shell偏差，又将计算代价控制在最低水平，是该方法的推荐配置。

固定步数终止的另一优势在于使计算代价与速度场平滑度可调控。当场景遮挡极为复杂时，可适度增加M以换取更平滑的速度场，但这种需求在论文测试的场景中并未出现。

### 逆渲染应用验证

Fig. 12展示了将本方法用于遮挡物形状优化的逆渲染任务。从初始圆盘形状出发，仅通过观察阴影梯度，本方法能够收敛到目标花朵形状；而WAS和PSDR-WAS基线方法因梯度估计不准确，无法有效收敛。收敛速率曲线（Fig. 12d）定量地展示了本方法的优势。这一应用验证了微分可见性估计的无偏性和低方差对下游优化任务的关键影响——有偏或高方差的梯度会直接导致优化发散或停滞。

### 失败模式与局限性

尽管整体表现优异，论文明确指出了若干局限：

1. **锥查询的计算开销**：在GPU上，基于BVH遍历的锥查询约为光线相交查询的10倍开销（龙模型上1M查询约30ms），成为性能瓶颈。这限制了方法在实时或交互式应用中的直接部署。

2. **初始半角参数的选择**：锥查询中用于平衡查询速度与速度场平滑度的初始半角参数，其最优选择依赖于场景几何复杂度，目前缺乏自动化选取机制。

3. **几何表示的局限性**：当前方法专注于三角网格场景，向符号距离函数（SDF）等其他几何表示的扩展尚未探索。

4. **高M步数的收益递减**：虽然固定步数终止消除了epsilon-shell偏差，但当M>1时额外计算成本线性增长而精度收益递减，在极端复杂遮挡场景下可能需要更高M，但论文未给出此类场景的明确证据。

### 公平性说明

与基线的所有比较均采用等样本数（Figs. 1, 9, 11）或等时间（Fig. 10）设置，基线方法实现均依据原论文描述，比较条件公平可信。

![[assets/figures/papers/paper_list_l4_https_research_nvidia_com_labs_prl_wu2025diffvisibility_diffvisibility_p/figures/013_Figure_10.jpg]]
*Figure 10: An equal-time ablation study on the number of WoSC steps ??. In practice, we do not observe significant benefits from using more than one step, due to the linearly increasing computational cost. (a) Configuration*

### 补充图表

![[assets/figures/papers/paper_list_l4_https_research_nvidia_com_labs_prl_wu2025diffvisibility_diffvisibility_p/figures/004_Figure_3.jpg]]
*Figure 3: (c) Our fixed-step WoS Fig. 3. A 1D toy example. (a) We want to use warped-area reparameterization to compute the derivative of the integral ?? defined in Eq. (10) (the area of the blue region) with respect to the changing discontinuity ?? . (b) Plots of the velocity functions and their divergences constructed by the prior method (Eq. (7)) and solving Laplace’s equation. (c) Plots of the velocity functions and their divergences constructed by our ??-step WoS method with M = 1 , 4 , and 16*

![[assets/figures/papers/paper_list_l4_https_research_nvidia_com_labs_prl_wu2025diffvisibility_diffvisibility_p/figures/010_Figure_9.jpg]]
*Figure 9: (c) Ours (high spp) (e) PSDR-WAS (f ) Ours Fig. 9. In this example, we compute derivatives with respect to the ??- translation of the center box. We first validate our warped-area reparameterization algorithm by comparing our result in (c) with the reference gradient image computed by finite differences in (b). In (d)–(f ), we show equal-sample comparisons with the baseline methods, WAS [Bangaru et al. 2020] and PSDR-WAS [Xu et al. 2023]*

![[assets/figures/papers/paper_list_l4_https_research_nvidia_com_labs_prl_wu2025diffvisibility_diffvisibility_p/figures/012_Figure.jpg]]
*Figure: (b) FD ref. Mean L1 error*

![[assets/figures/papers/paper_list_l4_https_research_nvidia_com_labs_prl_wu2025diffvisibility_diffvisibility_p/figures/014_Figure_11.jpg]]
*Figure 11: (e) Projective sampling Fig. 11. Comparison with projective sampling [Zhang et al. 2023]. The example on the top row computes derivatives of the shadows cast by the Voronoi-bunny model, and the example on the bottom row computes derivatives of the shadows seen through a mirror. Our results closely match the FD reference images, showing the robustness of our method under complicated light transport configurations. On the other hand, the results of projective sampling deviate from the reference images*



## 定位与知识库关联

### 1. 问题谱系：微分可见性与Warped-Area重参数化

本工作处于可微渲染中**微分可见性**（differential visibility）这一子领域，其核心挑战在于：当场景参数变化引起遮挡边界移动时，路径积分中由阶跃可见性函数产生的Dirac-delta类边界项必须被正确估计，否则梯度将是有偏的。

早期方法通过显式采样不连续边界来处理这一问题（如 **Projective Sampling**, Zhang et al., ACM Trans. Graph. 2023），但其在复杂遮挡和镜面反射等场景中鲁棒性不足。**Warped-area reparameterization**（WAR）范式由Bangaru等人（ACM Trans. Graph. 2020）提出，通过散度定理将边界路径积分转化为可见表面区域上的面积积分，从而将边界运动的采样问题转化为速度场散度的采样问题。Xu等人（ACM Trans. Graph. 2023）进一步将WAR推广到路径空间（PSDR-WAS）。

然而，上述WAR方法的瓶颈在于**速度场构造**：它们基于加权平均插值（Eq. 7），其权重函数无界，导致估计有偏且数值不稳定；同时，散度的支撑域仅局限于边界附近极窄的带状区域，采样效率低下。这些缺陷使得现有WAR方法在复杂3D场景中难以鲁棒、高效地工作。

### 2. 核心方法创新：从WoS到固定步WoSC

本工作的核心贡献是将速度场构造重新建模为**拉普拉斯方程的Dirichlet边界值问题**，并利用Walk-on-Spheres（WoS）的Monte Carlo求解特性来构建满足连续性、平滑性和边界条件的速度场。这一思路的关键洞察在于：微分可见性所需的速度场本质上可以是调和函数（harmonic function），而WoS天然适合按需（on-demand）求解此类问题。

在此基础上，本文做出了三项关键改进，构成了与先前WAR方法的本质区别：

| 设计维度 | 先前方法（WAS/PSDR-WAS） | 本方法（Fixed-Step WoSC） |
|---------|------------------------|------------------------|
| 速度场构造 | 加权平均插值，权重无界，估计有偏 | 固定步数WoS/WoSC求解拉普拉斯方程，无偏估计 |
| 随机游走终止 | 随机步数，直至进入epsilon-shell（引入偏差） | 固定M步终止，抓取最近边界点值（消除epsilon-shell偏差） |
| 游走域 | 平面表面（2D切线圆） | 以着色点为中心的单位球面（球冠行走） |

**固定步数终止**（fixed-step termination）是本方法的关键设计选择。原始WoS需随机步数直至进入边界的epsilon-shell，这不仅引入偏差，且计算代价不可预测。固定步数WoS在M步后强制终止，并通过抓取最近边界点的值来近似，得到的场虽非严格调和，但仍满足WAR所需的连续性和边界条件。消融实验（Fig. 10）表明，M=1即可达到较好的精度与效率平衡，增加步数收益递减。

**球面投影与WoSC**是另一项重要创新。将可见表面区域投影到着色点处的单位球面上进行随机游走，避开了平面域中复杂遮挡边界的处理。配合**锥查询**（cone query）高效寻找球面上测地线最近的剪影点，构成了完整的球面速度场求解管线。

### 3. 与相关方法的横向对比

- **vs. WAS** (Bangaru et al., 2020)：本方法在速度场构造上从插值范式转向PDE求解范式，消除了有偏估计的根源。在Voronoi-bunny阴影梯度任务上，本方法的L1误差为0.032，显著低于WAS的0.053（Fig. 1）。
- **vs. PSDR-WAS** (Xu et al., 2023)：PSDR-WAS将WAR推广到路径空间，但速度场构造仍沿用加权平均插值，继承了偏差和数值不稳定问题。本方法在相同任务上L1误差为0.032，低于PSDR-WAS的0.069。
- **vs. Projective Sampling** (Zhang et al., 2023)：投影采样显式处理不连续边界，但在镜面反射阴影等场景中失效。本方法在镜面阴影梯度任务中与有限差分参考匹配，而投影采样无法捕捉镜面反射的阴影（Fig. 11）。

### 4. 适用边界与局限

**适用场景**：
- 三角网格表示的几何体上的微分可见性计算
- 需要无偏梯度估计的可微渲染与逆渲染任务
- 复杂遮挡、镜面反射等对边界采样方法不友好的场景

**已知局限**：
1. **锥查询开销**：GPU上的锥查询（BVH遍历）约为光线相交查询的10倍开销（龙模型上1M查询约30ms），仍有优化空间。
2. **初始半角参数**：在BVH遍历中平衡查询速度与速度场平滑度的最优半角选择问题尚未解决。
3. **几何表示限制**：当前方法专注于三角网格，未探索向符号距离函数（SDF）等其他几何表示的扩展。
4. **步数M的收益递减**：固定步数终止虽然高效，但M>1时额外计算成本线性增长而收益递减，极端场景下可能需要更高M。

### 5. 开放问题与未来方向

1. **实时性能优化**：如何在GPU上进一步优化锥查询，以实现实时或交互式的微分可见性计算？
2. **流形WoS方法的结合**：最近的基于流形的WoS方法（如Projected WoS）是否可以应用于本方法的球面设定，以进一步提升效率？
3. **几何表示的泛化**：本方法是否可推广到SDF、神经隐式表面等其他几何表示？这将显著扩展其应用范围。
4. **自适应步数选择**：对于不同复杂度和光照传输配置的场景，如何自动选择最优步数M？这需要建立场景特征与步数需求之间的预测模型。
5. **与其他可微渲染组件的集成**：本方法专注于可见性梯度，如何与材质、几何等梯度的其他估计器协同优化，构建端到端的高效可微渲染系统？



## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Unbiased_Differential_Visibility_Using_Fixed_Step_Walk_on_Spherical_Caps_And_Closest_Silhouettes.pdf]]
