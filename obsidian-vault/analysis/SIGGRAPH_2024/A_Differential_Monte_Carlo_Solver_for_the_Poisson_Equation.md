---
title: A Differential Monte Carlo Solver for the Poisson Equation
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/A_Differential_Monte_Carlo_Solver_for_the_Poisson_Equation.pdf
project_link: "https://shuangz.com/projects/diff-wos-sg24/"
code_link: null
aliases:
- DWSW
- DMCSPE
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过物质形式参数化将形状导数转化为参考域上的泊松问题，并导出仅含边界积分的导数公式；同时，利用控制变量与对偶采样大幅降低法向导数的估计方差。
primary_logic: 利用材料导数的链式法则结合Green函数/泊松核的积分表达，将解的导数表达为仅依赖于边界积分的公式，从而可以借助无网格Walk-on-Spheres过程高效估计。
claims:
- 在Wrench、Teapot、Globe、Bunny四个2D/3D示例上，等计算时间下我们的估计结果与有限差分基本一致，而基线方法噪声很大。
- 在旋转角度、姿态和形状优化的逆问题中，只有我们的方法能使优化稳定收敛至目标，基线方法因高方差而失败。
- 消融实验表明全方法在圆盘上可达近零方差，所有变体均优于基线，其中全方法始终最优。
- Wrench (2D Laplace) 上 导数质量（视觉对比） = 与有限差分基本一致
---

# A Differential Monte Carlo Solver for the Poisson Equation

> [!tip] 核心洞察
> 利用材料导数的链式法则结合Green函数/泊松核的积分表达，将解的导数表达为仅依赖于边界积分的公式，从而可以借助无网格Walk-on-Spheres过程高效估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | 一种可微蒙特卡罗泊松方程求解器 |
| 英文题名 | A Differential Monte Carlo Solver for the Poisson Equation |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://shuangz.com/projects/diff-wos-sg24/) · [arXiv](https://arxiv.org/abs/2208.02114) · [Project](https://shuangz.com/projects/diff-wos-sg24/") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Differentiable Walk-on-Spheres (可微WoS) |
| Dataset | Wrench, Teapot, Globe, Bunny |

> [!tip] 效果简介
> - Wrench (2D Laplace) 上，导数质量（视觉对比） 与有限差分基本一致 vs 噪声明显 (显著更平滑)。
> - Teapot (2D Laplace) 上，导数质量（视觉对比） 与有限差分基本一致 vs 噪声明显 (显著更平滑)。
> - Globe (2D Poisson) 上，导数质量（视觉对比） 与有限差分基本一致 vs 噪声明显 (显著更平滑)。

## 概要

当泊松方程的定义域形状随参数变化时，传统离散化方法（如有限元）需要重新剖分网格，计算代价高昂；而直接对积分方程使用Reynolds输运定理求导会引入高方差的边界积分项，导致蒙特卡洛估计不可用。本文提出**可微Walk-on-Spheres（Differentiable WoS）**——一种无网格的蒙特卡洛求解器，能够高效估计泊松方程解对任意参数（包括定义域形状）的导数。

核心思路是：通过物质形式参数化将形状导数转化为参考域上的泊松问题，导出仅含边界积分的导数公式（Eq. 22）；同时利用控制变量与对偶采样大幅降低边界法向导数的估计方差。方法从评估点出发，通过两次WoS过程——第一次采样边界点，第二次在最大内切球内估计法向导数——以低方差获得导数估计。

在Wrench、Teapot、Globe、Bunny等2D/3D示例上，等计算时间下本方法的导数估计与有限差分基本一致，而基线方法噪声显著。在旋转角度优化、姿态优化和形状优化等逆问题中，仅本方法能使优化稳定收敛至目标值，基线方法因高方差而失败。消融实验证实全方法方差最低，在圆盘上可达近零方差。该方法为无网格可微PDE求解提供了首个实用方案，目前支持Dirichlet边界条件的泊松方程。

## 核心方法与创新机理

### 问题瓶颈

当泊松方程的定义域 $\Omega$ 的形状随参数 $\theta$ 变化时，对解 $u$ 求导面临根本性困难。传统方法（如有限元法）需要随形状变化重新剖分网格，计算成本极高。若直接对积分方程使用 Reynolds 输运定理求导，则会在边界上引入高方差项，使蒙特卡洛估计失去实用价值。本文的核心贡献在于：**通过物质形式参数化将形状导数转化为参考域上的泊松问题，并导出一个仅含边界积分的导数公式**，从而使得无网格的 Walk-on-Spheres (WoS) 过程可以高效估计该导数。

### 物质形式参数化：将形状导数“拉回”参考域

设 $\Omega$ 随参数 $\theta$ 演化的映射为 $X(\cdot, \theta): \hat{\Omega} \to \Omega$，其中 $\hat{\Omega}$ 是固定的参考域。对任意标量场 $h$，定义**拉回算子**：

$$(X^* h)(p) := h(X(p, \theta)), \quad \forall p \in \hat{\Omega}$$

它将定义在演化域上的场“拉回”到参考域。令 $\hat{u} = X^* u$ 为参考域上的解，$\hat{f}, \hat{g}$ 类似定义。关键的一步是引入**物质导数**（material derivative），它满足链式法则：

$$\left[\frac{d}{d\theta} u(x)\right]_{\theta=0} = (\partial_\theta u)(x) + v(p) \cdot \nabla u(x)$$

其中 $v(p)$ 是速度场，描述域边界的局部运动。**偏导数 $\partial_\theta u$ 正是我们需要的目标**——它衡量当形状“冻结”在当前状态时解对参数的变化率。通过先求物质导数再减去对流项 $v \cdot \nabla u$，即可得到偏导数。

### 核心公式：仅含边界积分的导数表达

经过推导（§4.2），作者得到了本文最核心的公式——**导数边界积分公式**（Eq. 22）：

$$(\partial_{\theta} u)(\rho) = \int_{\partial\hat{\Omega}} P^{\hat{\Omega}}(\rho, s) \big( \partial_{\theta} \hat{g}(s) - v(s) \cdot \nabla_{\hat{\Omega}} \hat{u}(s) \big) \, ds$$

其中 $P^{\hat{\Omega}}(\rho, s)$ 是参考域 $\hat{\Omega}$ 的泊松核密度，$\nabla_{\hat{\Omega}} \hat{u}(s)$ 是参考域解在边界点 $s$ 处的梯度。**这一公式的突破性在于：它将形状导数的计算完全转化为边界上的积分，彻底消除了区域内部积分项**，从而避免了 Reynolds 输运定理中高方差的 $\varepsilon$-壳边界项。

### Changed Slot 1：导数公式形式——从体积-边界混合到纯边界积分

| 维度 | 基线方法 | 本文方法 |
|------|----------|----------|
| **公式来源** | 直接对积分方程（Eq. 5）使用 Reynolds 输运定理 | 物质形式参数化 + 泊松核积分表达 |
| **积分域** | 需同时处理球 $B_x$ 和 $\varepsilon$-壳的导数 | 仅参考域边界 $\partial\hat{\Omega}$ |
| **方差特性** | 边界项方差极高 | 可借助 WoS 自然采样，方差可控 |

这一 changed slot 是整个方法可行性的基石。通过将导数表达为 $P^{\hat{\Omega}}(\rho, s)$ 加权的边界积分，采样过程天然与 WoS 的第一步（从评估点 $p$ 出发采样边界点 $s$）对齐。

### Changed Slot 2：边界法向导数估计——从内点逼近到控制变量+对偶采样

Eq. 22 中的 $\nabla_{\hat{\Omega}} \hat{u}(s)$ 可分解为切向梯度和法向导数：

$$\nabla u(s) = \nabla_{\partial\hat{\Omega}} u(s) + n(s) \partial_{n(s)} u$$

其中切向梯度可直接从边界函数 $g$ 计算：$\nabla_{\partial\hat{\Omega}} u(s) = \nabla g(s) - n(s) \cdot \nabla g(s)$。真正的难点在于**法向导数 $\partial_{n(s)} u$ 的估计**。

基线方法（Sawhney and Crane, SIGGRAPH 2020）使用内点逼近，方差较大。本文提出了**控制变量+对偶采样**的低方差估计量（Eq. 26）：

$$\partial_{n(s)} u = \int_{B_c} (f(y)-f(s)) P^{B_c}(y \to s) \, dy + f(s) \frac{R}{n} + \int_{\partial B_c} (u(z)-g(s)) \partial_{n(s)} P^{B_c}(s \to z) \, dz$$

其中 $B_c$ 是在边界点 $s$ 处沿内法向找到的**最大内切球**（通过二分法搜索，见 Figure 3）。控制变量的核心思想是：减去 $f(s)$ 和 $g(s)$ 使被积函数在 $s$ 附近趋于零，从而大幅降低方差。

![[assets/figures/papers/paper_list_l3_https_shuangz_com_projects_diff_wos_sg24_repair/figures/005_Figure_3.jpg]]
*Figure 3: We search for the largest ball—which is*

为进一步降低边界积分方差，引入**对偶采样**（Eq. 27）：对 $\partial B_c$ 上的采样点 $z$，构造其对偶点

$$z^* = s + 2( n(s) \cdot \Delta z ) n(s) - \Delta z$$

其中 $\Delta z = z - s$。$z$ 和 $z^*$ 关于法线对称，其泊松核导数的贡献倾向于相互抵消，从而进一步压缩方差。

### 推理路径：双 WoS 流程

整个导数估计的推理路径由两个嵌套的 WoS 过程组成（Figure 2, Algorithm 1 & 2）：

![[assets/figures/papers/paper_list_l3_https_shuangz_com_projects_diff_wos_sg24_repair/figures/004_Figure_2.jpg]]
*Figure 2: Our estimator: To estimate*

**模块 1：主 WoS 采样边界点。** 从评估点 $p \in \hat{\Omega}$ 出发，以泊松核密度 $P^{\hat{\Omega}}(p, s)$ 为目标分布，执行标准 WoS 过程采样一个边界点 $s$。这一步天然实现了 Eq. 22 中对 $\partial\hat{\Omega}$ 的蒙特卡洛积分。

**模块 2：最大内切球搜索。** 在采样到的边界点 $s$ 处，沿内法向 $n(s)$ 用二分法找到最大包含球 $B_c \subseteq \hat{\Omega}$（Figure 3, Eq. 28）。该球的大小直接决定了法向导数估计的方差——球越大，控制变量效果越好。

**模块 3：法向导数估计 WoS。** 在 $B_c$ 内部均匀采样 $y$ 以估计源项贡献；在 $\partial B_c$ 上对偶采样 $z$ 和 $z^*$，从这两点分别启动第二次 WoS 过程估计解值 $u(z)$ 和 $u(z^*)$，最后组合得到 $\partial_{n(s)} u$。

**模块间的因果关系链：** 模块 1 的输出 $s$ 是模块 2 和 3 的输入；模块 2 的输出 $B_c$ 决定了模块 3 的采样域；模块 3 的输出 $\partial_{n(s)} u$ 与切向梯度组合后代入 Eq. 22，乘以 $\partial_\theta \hat{g}(s) - v(s) \cdot \nabla_{\hat{\Omega}} \hat{u}(s)$，最终得到 $(\partial_\theta u)(\rho)$ 的无偏估计。

### 关键公式变量含义速查

| 符号 | 含义 | 锚点 |
|------|------|------|
| $\hat{\Omega}$ | 固定参考域 | §4.1 |
| $P^{\hat{\Omega}}(\rho, s)$ | 参考域的泊松核密度 | Eq. 2 |
| $v(s)$ | 边界速度场，描述形状变化方向 | §4.2 |
| $\partial_{n(s)} u$ | 解在边界点 $s$ 处沿内法向的方向导数 | Eq. 23 |
| $B_c$ | 在 $s$ 处与边界相切的最大内切球 | Figure 3 |
| $z, z^*$ | $\partial B_c$ 上的对偶采样点对 | Eq. 27 |

### 方差控制的因果机制

整个方法的方差控制存在清晰的因果链：**物质形式参数化 → 纯边界积分公式 → WoS 天然采样泊松核 → 控制变量压缩内部积分方差 → 对偶采样压缩边界积分方差 → 最大内切球最大化控制变量效果**。消融实验（Figure 4）验证了这一链条：在圆盘上，内切球等于整个域，全方法达到近零方差；在三叶草域上，去掉对偶采样仅略微增加方差，但仍远优于基线；使用小球替代最大球则方差显著上升。

![[assets/figures/papers/paper_list_l3_https_shuangz_com_projects_diff_wos_sg24_repair/figures/008_Figure_4.jpg]]
*Figure 4: Ablation: We compare the performance of four normal-derivative estimators: the baseline method by Sawhney and Crane [2020], ours without antithetic sampling, ours using a small ball*

## 实验与关键发现

### 导数估计质量：与有限差分的视觉对比

论文在四个具有不同几何复杂度的域上评估了可微WoS的导数估计质量，并与基线方法（直接对积分方程使用Reynolds输运定理求导）进行等计算时间比较。

在**Wrench（2D Laplace）**、**Teapot（2D Laplace）**、**Globe（2D Poisson）**和**Bunny（3D Laplace）**四个示例上，本文方法的导数估计结果与有限差分（FD）参考解基本一致，呈现出平滑的导数场分布。相比之下，基线方法在相同计算时间内产生显著噪声，导数场中出现大量高频伪影，无法可靠地反映真实的导数结构（Figure 5）。

![[assets/figures/papers/paper_list_l3_https_shuangz_com_projects_diff_wos_sg24_repair/figures/007_Figure_5.jpg]]
*Figure 5: Differentiable PDE solve results: (a) Solutions to Poisson equations with Dirichlet boundary conditions*

这一结果验证了核心方法设计的有效性：通过将形状导数转化为仅含边界积分的公式（Eq. 22），并利用控制变量与对偶采样降低法向导数估计方差，可微WoS成功规避了Reynolds输运定理直接求导引入的高方差边界项问题。

### 逆问题优化：收敛能力的决定性优势

论文在四类逆问题上验证了可微WoS的实用价值，所有实验均使用相同的Adam优化器配置（相同初始化、学习率等），确保比较的公平性。

**2D旋转角度优化**（Figure 6）：在Wrench和Globe两个域上，优化目标为基于边界附近解场$u$推断域的旋转角度。本文方法的损失函数迅速下降，参数误差趋近于零；而基线方法由于导数估计的高方差，损失函数不降或剧烈震荡，无法实现有效收敛。

**3D姿态优化**（Figure 7）：在Bunny模型上，基于包围立方体表面采样的解值推断Bunny的三维姿态。本文方法再次表现出稳定收敛，参数误差快速趋零；基线方法则完全失败。

**2D扩散曲线形状优化**（Figure 8）：优化域边界的逐顶点位置，使解场匹配目标颜色场。本文方法是唯一能使损失和形状误差稳定下降至接近零的方案。

这些逆问题实验构成了本文最有力的证据：可微WoS是唯一能在形状参数优化场景中提供可用梯度信号的方法，基线方法因方差过大而完全失效。

### 消融实验：各组件贡献的定量分析

论文通过消融实验系统评估了法向导数估计器中各组件的贡献（Figure 4），使用高样本数（2000和100000）以准确评估方差特性。

**圆盘域上的极限情况**：在圆盘上求解Laplace问题并估计法向导数时，全方法达到近零方差。这是因为圆盘本身即为最大内切球（$B_c = \Omega$），控制变量项精确抵消，对偶采样进一步消除边界积分方差。这一结果验证了方法在理想几何条件下的理论最优性。

**三叶草域上的综合比较**：在更复杂的三叶草域上求解Poisson问题，比较了四种估计器：
- 基线方法（Sawhney and Crane 2020的内点近似）：方差最高
- 本文方法（无对偶采样）：方差显著降低，远优于基线
- 本文方法（小球变体）：性能介于无对偶和全方法之间
- 本文全方法：方差最低，表现最优

去掉对偶采样仅略微增加方差，但仍远优于基线，说明控制变量是降低方差的主要贡献因素，而对偶采样提供了进一步的方差缩减。所有变体均显著优于基线，验证了基于最大内切球的控制变量策略的核心有效性。

### 方法的适用边界与限制

尽管可微WoS在实验设定下表现出色，论文明确指出了若干限制：

1. **前向求解器的局限**：前向WoS过程采用基础实现，未整合双向采样、路径缓存等更先进的变体技术，在复杂几何或高精度需求场景下可能存在效率瓶颈。

2. **采样策略的优化空间**：法向导数估计中对球内源项积分和边界积分均采用均匀采样，未针对被积函数的局部特性设计重要性采样策略，在源项$f$或解$u$变化剧烈的区域可能产生较高方差。

3. **问题类型的限制**：当前方法仅支持Dirichlet边界条件的泊松方程，尚未推广至屏蔽泊松方程（screened Poisson）或Neumann边界条件等更一般的二阶椭圆型偏微分方程。

4. **几何表示的依赖**：最大内切球搜索（Figure 3, Eq. 28）依赖于沿内法向的二分查找，需要域边界的光滑性或至少局部可查询的距离信息，对于具有尖锐特征或非流形边界的域可能需要额外处理。

![[assets/figures/papers/paper_list_l3_https_shuangz_com_projects_diff_wos_sg24_repair/figures/010_Figure_6.jpg]]
*Figure 6: Solving 2D inverse problems: For both examples, we optimize the rotation angle of the domain boundary based on the solution field ?? near the boundary (both interior and exterior). All images in this example use the same color map as Figure 1. The parameter error in (f) is used only for evaluation (and not for optimization)*

![[assets/figures/papers/paper_list_l3_https_shuangz_com_projects_diff_wos_sg24_repair/figures/011_Figure_7.jpg]]
*Figure 7: Solving 3D inverse problem: In this example, we infer the pose of a 3D bunny (with fixed Dirichlet boundary conditions over the surface) based on the solution ?? sampled on the surface of a cube surrounding the bunny. All images in the top row use the same color map as Figure 1. The parameter error in (f) is used only for evaluation (and not for optimization)*

## 定位与知识库关联

本文在可微物理模拟与无网格蒙特卡洛方法的交叉点上开辟了一个新方向。其核心贡献在于**将泊松方程解的导数计算从依赖网格的离散化框架中解放出来**，使形状导数可以在无网格的Walk-on-Spheres过程中以低方差估计。

### 改变的Slot：从域内体积分到纯边界积分

与直接对积分方程使用Reynolds输运定理求导的基线方法相比，本文改变的关键slot是**导数公式的积分域结构**。基线方法对球域$B_x$和$\epsilon$-壳同时求导，得到的估计量包含高方差的边界项，在蒙特卡洛采样中极不稳定。本文通过**物质形式参数化**（material-form parameterization），利用拉回算子将形状演化问题转化为参考域上的泊松问题，最终导出一个仅依赖于参考域边界$\partial\hat{\Omega}$积分的公式（Eq. 22）：

$$(\partial_{\theta} u)(\rho) = \int_{\partial\hat{\Omega}} P^{\hat{\Omega}}(\rho, s) \big( \partial_{\theta} \hat{g}(s) - v(s) \cdot \nabla_{\hat{\Omega}} \hat{u}(s) \big) \, ds$$

这一形式将方差源从“域内+边界”压缩为“仅边界”，并使得采样过程可以完全复用前向WoS的泊松核$P^{\hat{\Omega}}(\rho \to s)$进行边界点采样，无需对域内几何变化做额外处理。

### 知识库挂载点

**1. 挂载于Walk-on-Spheres求解器（Sawhney and Crane, SIGGRAPH 2020）**

前向WoS求解器是本文的基础设施。本文的方法可视为在该求解器上附加了一个“微分通道”：主WoS过程（Algorithm 1）采样边界点$s$，第二次WoS过程（Algorithm 2）估计该点处的法向导数$\partial_{n(s)}u$。这一设计保持了与现有WoS框架的兼容性——任何WoS的改进（如双向采样、缓存策略）都可以直接提升本文方法的效率，这是论文明确指出的一个未来方向。

**2. 挂载于形状优化与可微模拟**

在可微模拟的知识谱系中，本文填补了“无网格泊松求解器+形状导数”的空白。传统方法（如有限元法）在形状优化中需要每次迭代重新剖分网格，计算成本随几何复杂度急剧上升。本文的方法天然免网格，只需评估点处的蒙特卡洛采样，特别适合边界几何频繁变化的场景（如图8的扩散曲线形状优化）。与基于神经网络的PDE求解器（如PINN）相比，本文方法不需要训练过程，且导数估计具有无偏性保证。

**3. 挂载于控制变量与对偶采样技术**

法向导数估计（Eq. 26）的核心技巧——减去$f(s)$和$g(s)$作为控制变量，以及利用内切球边界上的对偶采样点$z$和$z^*$（Eq. 27）——源自蒙特卡洛积分的经典降方差技术。在圆盘这一特殊情形下，内切球等于整个域，控制变量完全抵消积分方差，达到近零方差（Figure 4 top c），这为理论最优性提供了实证锚点。

### 适用边界与局限

本文方法的适用边界清晰且务实：

- **方程类型**：仅支持带有Dirichlet边界条件的泊松方程（$\Delta u = -f$ on $\Omega$, $u = g$ on $\partial\Omega$）。论文明确指出尚未推广至屏蔽泊松方程（screened Poisson）或Neumann边界条件，这是最直接的扩展方向。
- **采样策略**：法向导数估计中的内部积分和边界积分均采用均匀采样，未针对源项$f$的分布做重要性采样优化，在$f$变化剧烈的区域可能存在方差偏高的问题。
- **前向求解器**：使用基础WoS，未整合更先进的变体（如Walk-on-Boundary），在狭窄区域可能存在收敛慢的问题。

### 后续启发价值

本文的方法论框架——通过物质导数链式法则将形状导数转化为参考域上的边界积分——具有超越泊松方程的潜力。对于更一般的二阶椭圆型算子，只要其Green函数和泊松核具有可采样的形式，类似的推导路径可能成立。此外，法向导数估计中“最大内切球+控制变量+对偶采样”的组合策略，为其他边界积分型蒙特卡洛估计器提供了可复用的降方差模板。与Walk-on-Boundary等替代无网格方法的结合，有望在保持无网格优势的同时进一步提升采样效率。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/A_Differential_Monte_Carlo_Solver_for_the_Poisson_Equation.pdf]]