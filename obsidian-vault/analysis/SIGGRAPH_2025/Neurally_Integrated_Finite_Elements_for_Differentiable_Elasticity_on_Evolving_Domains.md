---
title: "Neurally Integrated Finite Elements for Differentiable Elasticity on Evolving Domains"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/Neurally_Integrated_Finite_Elements_for_Differentiable_Elasticity_on_Evolving_Domains.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/flexisim/
aliases:
- NIMF
- NIFEDEED
tags:
- SIGGRAPH_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过小型神经网络从局部SDF值学习可微的求积点位置与权重，实现平滑且高质量的数值积分，从而打通从物理响应到隐式表面的梯度通道。"
primary_logic: "将求积规则预测转化为小型MLP的学习任务，既保证了积分精度，又天然输出连续可微的映射，使得在粗网格上也能有效模拟演化隐式域的弹性行为，并支持在循环中同时优化形状、拓扑和材料。"
claims:
- "神经求积在边界移动时平滑更新求积点，而Clip和Full方案出现跳变（Figure 2）。"
- "移除神经求积后梯度完全消失，优化无法收敛（Figure 17消融）。"
- "神经求积结合混合FEM在粗网格下仍能获得接近高分辨率的平衡形状，明显优于Clip/Full配方及线性四面体网格（Figure 5）。"
- "神经求积能正确捕获亚像素异质性，而Full/Clip求积在相同网格下失败（Figure 8）。"
---

# Neurally Integrated Finite Elements for Differentiable Elasticity on Evolving Domains

> [!tip] 核心洞察
> 将求积规则预测转化为小型MLP的学习任务，既保证了积分精度，又天然输出连续可微的映射，使得在粗网格上也能有效模拟演化隐式域的弹性行为，并支持在循环中同时优化形状、拓扑和材料。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向演化域可微弹性的神经集成有限元方法 |
| 英文题名 | Neurally Integrated Finite Elements for Differentiable Elasticity on Evolving Domains |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [paper](https://arxiv.org/abs/2410.09417); [Project](https://research.nvidia.com/labs/toronto-ai/flexisim/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Neurally Integrated Mixed FEM |
| Dataset | Dumbbell equilibrium (Section 5.1, Figure 5), Dumbbell with large stiffness ratios (Figure 6, 24), Dumbbell buckling (Figure 7), Stress minimization on bracket (Figure 10) |

> [!tip] 效果简介
> - Dumbbell equilibrium (Section 5.1, Figure 5) 上，Equilibrium shape accuracy (qualitative) 为 Neural quadrature + Mixed FEM yields accurate shape even at 16^3 resolution，对比 Full quadrature underestimates deformation; Clip quadrature unstable; linear tetrahedral mesh inaccurate，变化 Closer to high-resolution reference。
> - Dumbbell with large stiffness ratios (Figure 6, 24) 上，Convergence after 250 Newton iterations 为 Mixed FEM converges to correct equilibrium，对比 Displacement-only FEM stagnates far from equilibrium at ratios up to 10^9，变化 Qualitative improvement in convergence。
> - Dumbbell buckling (Figure 7) 上，Buckling shape fidelity 为 Tri-quadratic Neural quadrature captures high-resolution behavior well，对比 Tri-linear Full/Clip quadrature deviates strongly at coarse resolution，变化 Closer to 64^3 reference。

## 概述

**核心问题**：在隐式表面表示的演化域上进行可微弹性模拟时，传统固定求积方案（如Full、Clip）在边界移动时会产生积分跳变或不可微，导致物理损失对几何参数的梯度消失，切断了端到端形状与拓扑优化的梯度通道。

**核心方法**：本文提出**神经集成混合有限元方法（Neurally Integrated Mixed FEM）**，包含两个关键创新：
1. **神经求积网络（QuadNet）**：用小型MLP从局部SDF值预测每个单元的求积点位置与权重，实现平滑、可微的高阶数值积分，打通从物理响应到隐式表面的梯度通路。
2. **四场旋转感知混合FEM**：将Trusty et al.（2022）的混合公式推广到任意有限元，支持宽范围材料刚度比（高达10⁹），避免纯位移FEM在高刚度比下的收敛停滞。

**方法定位**：该方法位于可微物理模拟与隐式几何优化的交叉点。与基于密度场的拓扑优化（如SIMP）不同，它直接在演化隐式表面上操作；与纯网格方法不同，它通过规则网格上的神经求积实现亚像素分辨率的物理感知。结合FlexiCubes（Shen et al., SIGGRAPH 2023）重建，形成从隐式SDF到物理模拟再到显式网格的完全可微管线。

**关键发现**：
- 神经求积在边界移动时平滑更新求积点，而Clip和Full方案出现跳变（Figure 2）。
- 移除神经求积后梯度完全消失，优化无法收敛（Figure 17消融实验）。
- 神经求积结合混合FEM在粗网格（如16³）下仍能获得接近高分辨率（64³）的平衡形状，明显优于Clip/Full方案及线性四面体网格（Figure 5）。
- 混合FEM在高刚度比下正确收敛，而位移-仅FEM在250次牛顿迭代后仍远离平衡（Figure 6）。
- 物理感知损失驱动形状与材料优化，使椅子在2.5kN负载下抵抗坍塌，而纯几何重建严重坍塌（Figure 11）。

**主要局限**：位移自由度受限于底层形函数，无法正确模拟断开连接的浮动材料；物理感知重建缺乏全局收敛性，对初始SDF和损失函数敏感；混合FEM依赖经验性惩罚参数ε；神经求积网络需针对特定阶数和单元类型训练。

## 背景与动机

### 隐式表面弹性模拟的核心瓶颈

在计算机图形学与计算力学中，基于隐式表面（如符号距离函数 SDF）表示几何形状的方法因其天然的拓扑灵活性而备受青睐。然而，当几何形状在优化过程中不断演化时，如何对定义在隐式域上的弹性行为进行可微的数值积分，成为一个长期悬置的关键难题。

传统的有限元方法依赖固定的求积方案来计算单元内的积分。在隐式表面上，两种常见策略均存在根本性缺陷：

- **Full quadrature**（标准 Gauss-Legendre 求积）：在穿越边界的单元中，积分点固定不变，导致积分不连续——当边界移动时，求积点突然“跳入”或“跳出”材料域，使积分值产生阶跃。
- **Clip quadrature**（基于指示函数的裁剪求积）：虽然通过权重裁剪来近似材料域，但其权重更新同样是不连续的，且积分精度在粗网格下严重退化。

这两种方案的核心问题在于：**积分过程对几何参数不可微**。当边界在单元内平滑移动时，Full 和 Clip 方案的求积点位置和权重发生跳变（见 Figure 2），导致物理响应相对于隐式表面参数的梯度为零或不可靠。这意味着，任何试图通过梯度下降来优化形状或拓扑的端到端流程，都会在物理模拟这一环节被“截断”——梯度无法从物理损失回流到几何参数。

### 混合 FEM 的必要性与现有局限

另一个独立但同样关键的问题是弹性模拟器本身对材料刚度比的鲁棒性。标准位移-only FEM 在高刚度比（如软材料中嵌入刚性区域）下收敛极慢，牛顿迭代在有限步数内无法达到平衡。这一问题在形状优化中尤为致命：如果模拟器本身未能收敛到正确的物理状态，那么基于该状态计算的物理损失及其梯度都将是有偏的，进而误导优化方向。

Trusty et al.（2022）提出的旋转感知混合 FEM 通过引入独立的旋转和应变场，显著改善了大刚度比下的收敛性，但其原始公式仅限于特定的低阶单元类型，无法直接适配高阶形函数和规则网格上的通用离散化。

### 本文动机

上述两个问题——**不可微积分**与**有限元收敛性**——共同构成了“演化域可微弹性”这一研究空白的核心障碍。本文的动机正是同时攻克这两个瓶颈：

1. **打通梯度通道**：设计一种可微的求积方案，使得积分值随边界平滑变化，从而让物理损失对隐式表面参数的梯度可靠且非零。
2. **构建鲁棒模拟器**：将混合 FEM 推广到任意有限元和高阶基函数，确保在宽范围材料参数下模拟器本身能正确收敛，为上层优化提供准确的物理信号。

通过将求积规则的学习转化为一个小型神经网络的训练任务，本文提出了一种**神经集成有限元方法**，使得在粗网格上也能有效模拟演化隐式域的弹性行为，并支持在统一的优化循环中同时优化形状、拓扑和材料参数。

## 核心创新

本文的核心贡献在于打通了**从物理响应到隐式几何参数的端到端梯度通道**，使演化域上的可微弹性模拟与优化成为可能。围绕这一目标，作者在四个关键环节引入了创新设计，形成了“神经集成混合有限元”方法。

### 1. 神经求积：可微积分的关键使能器

传统有限元在隐式表面上进行积分时，面临根本性的可微性困境：**Full求积**（标准Gauss-Legendre）将求积点固定在全单元上，当边界移动时积分域突变，导致梯度不连续；**Clip求积**基于指示函数截断权重，在边界穿越求积点时产生跳变（Figure 2）。两者都无法为几何参数提供可靠的梯度信号。

作者将求积规则的学习转化为一个**小型神经网络的回归任务**：网络输入为单元各角点的SDF值，输出为该单元内的一组求积点位置与权重。网络通过最小化矩拟合误差（moment fitting）来训练，确保对指定阶数的多项式精确积分。由于MLP天然输出连续可微的映射，当SDF值随几何参数平滑变化时，求积点与权重也随之平滑更新，从而打通了从物理量积分到隐式表面参数的梯度通道。

**消融实验**（Figure 17）给出了决定性证据：将神经求积替换为Full或Clip求积后，物理损失对顶点SDF值的梯度完全消失，优化无法收敛。这确立了神经求积作为整个框架可微性基石的不可替代地位。

### 2. 四场旋转感知混合FEM：应对高刚度比的稳健求解

标准位移-only FEM在材料刚度比增大时收敛极慢，甚至停滞（Figure 6）。作者在Trusty et al.（2022）的混合FEM基础上，提出了**四场广义扩展**：将对称应变 $S$ 和旋转 $R$ 提升为独立原场，通过增广拉格朗日方法强制约束 $C(\mathbf{u}, R, S) = F(\mathbf{u}) - RS = 0$。这一解耦使得即使在刚度比高达 $10^9$ 的极端情况下，求解器仍能在250次牛顿迭代内收敛到正确的平衡形状。

该设计的关键因果机制在于：将非线性材料响应 $\psi(S)$ 与运动学约束分离，避免了位移-only FEM中因刚度矩阵条件数恶化导致的迭代停滞。在后续的形状与材料联合优化中（Figure 14, 16），混合FEM能正确估计物理损失，驱动优化器充分加强关键承载区域；而位移-only FEM因收敛不足而低估物理损失，导致材料优化不充分。

### 3. 平滑预条件器：抑制高频噪声的几何正则化

直接优化网格SDF值会导致重建表面出现高频噪声，使模拟和优化极不稳定。作者引入了一种简单而有效的**高斯模糊预条件器**：在每次重建和模拟之前，对网格上的SDF参数和顶点位移施加高斯核卷积。这一操作平滑了隐式表面的梯度场，抑制了虚假的高频几何特征，使优化过程稳定。

消融实验表明（Figure 17），移除平滑预条件器后，重建表面“几乎不可用”。该设计虽非本文独有，但在可微物理优化管线中起到了关键的稳定性保障作用。

### 4. 物理感知损失与分阶段调度：引导几何与材料协同进化

作者定义了一个**基于位移和应力的组合物理损失** $\mathcal{L}_{\mathrm{phys}}$，采用 $p=8$ 的高阶范数逼近极大范数，以惩罚最严重的变形和应力集中区域。该损失与几何重建损失协同工作，驱动隐式表面在保持目标形状的同时满足物理约束。

一个关键的工程创新是**分阶段损失调度**：前30%的优化迭代仅使用几何/渲染损失，使隐式表面先收敛到合理的初始形状，然后再激活物理损失。这避免了优化初期因几何未成形而导致的物理损失梯度噪声，显著提升了收敛稳定性。

### 创新点总结

| 创新槽位 | 基线方案 | 本文方案 | 因果作用 |
|---------|---------|---------|---------|
| 求积方案 | 固定Gauss点或Clip截断 | 小型MLP预测求积点与权重 | 打通SDF→积分的可微梯度通道 |
| FEM形式 | 位移-only或线性混合FEM | 四场旋转感知混合FEM | 解耦材料响应与运动学，应对高刚度比 |
| 梯度预条件 | 无 | 高斯模糊卷积 | 抑制高频噪声，稳定几何优化 |
| 损失调度 | 单阶段全损失 | 先几何后物理的分阶段激活 | 避免早期梯度噪声，保证收敛 |

这些创新相互依赖、协同作用：神经求积提供可微性，混合FEM保证求解精度与收敛性，平滑预条件器稳定优化过程，分阶段调度确保收敛质量。移除任一组件都会导致系统性能显著退化或完全失效。

## 整体框架

本文提出**神经集成混合有限元（Neurally Integrated Mixed FEM）**，一个面向演化隐式域的可微弹性模拟与优化框架。该框架的核心设计目标是：在隐式表面连续变形时，打通从物理响应（位移、应力）到几何参数（SDF网格值）的**平滑、可微梯度通道**，从而支持端到端的形状、拓扑与材料并发优化。

### 总体管线

整个系统由五个核心模块串联构成，形成“隐式表示 → 可微积分 → 物理求解 → 显式重建 → 损失驱动优化”的闭环：

1. **隐式几何表示**  
   几何体由一个定义在规则网格上的符号距离函数（SDF）隐式表达。网格分辨率可低至 $16^3$，几何演化通过直接优化网格顶点上的SDF值实现。

2. **神经求积网络（Neural Quadrature Network）**  
   针对每个网格单元，一个小型MLP以单元角落的SDF值 $(\phi_j)$ 为输入，预测该单元内部材料区域的求积点位置 $\mathbf{y}_p$ 与权重 $w_p$。该网络将传统固定求积规则（Full/Clip）替换为**平滑可微的映射**，从根本上解决了边界移动时积分跳变导致的梯度断裂问题（见 Figure 2）。

3. **混合有限元求解器（Mixed FEM Solver）**  
   在规则网格上执行准静态或动力学弹性模拟。采用**四场旋转感知混合有限元**公式，引入对称应变 $S$ 和旋转 $R$ 作为独立场，并通过增广拉格朗日惩罚约束 $F(\mathbf{u}) - RS = 0$。这使得求解器在材料刚度比高达 $10^9$ 时仍能稳定收敛，而传统纯位移FEM在此类情况下严重停滞（Figure 6, 24）。

4. **FlexiCubes 显式重建**  
   从优化后的隐式SDF中提取显式三角网格，用于渲染损失计算或边缘长度正则化。FlexiCubes（Shen et al., SIGGRAPH 2023）相比双行进立方体能更好地保留尖锐特征（Figure 17消融）。

5. **平滑预条件器（Smoothing Preconditioner）**  
   在每次优化迭代中，对网格SDF和顶点位移参数施加高斯模糊卷积，抑制高频噪声，稳定重建过程。消融实验表明，移除该模块会导致重建表面几乎不可用（Figure 17）。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2410_09417/figures/014_Figure_17.jpg]]
*Figure 17: Simulation of reconstructed shapes with various parts of our framework removed: top left: no Neural quadrature; top right: no smoothing preconditioner; bottom left: no edge-length loss; bottom-right: using dual marching-cube instead of FlexiCubes (cropped details)*

### 损失函数与优化策略

框架采用**分阶段损失调度**：
- **前30%迭代**：仅使用几何/渲染损失 $\mathcal{L}_{\text{FC}}$（如FlexiCubes重建损失、边缘长度损失），让形状快速逼近目标外观。
- **后70%迭代**：引入物理感知损失 $\mathcal{L}_{\text{phys}}$，其形式为位移 $\mathbf{u}$ 和应力 $\sigma$ 的 $p$-范数（$p=8$ 近似极大范数）在材料域上的积分：

$$\mathcal{L}_{\mathrm{phys}}(\Delta_t, \ell_{\mathbf{u}}, \ell_{\sigma}) := \sqrt[p]{ \int_{\Omega} \frac{1}{|\det \mathrm{d}\Omega|} \left( \ell_{\mathbf{u}} \|\mathbf{u}\|^p + \ell_{\sigma} \|\sigma\|^p \right) }$$

该损失驱动形状和材料参数同时优化，使物体在给定载荷下满足物理约束。

### 梯度计算

框架采用**混合自动微分与伴随法**计算损失对形状和材料参数的梯度。关键技巧在于：通过神经求积网络的可微性，将伴随法所需的偏导数 $\partial L / \partial p$ 转化为求解一个与单次牛顿迭代规模相当的线性系统，避免了完全回溯整个隐式欧拉求解过程的巨大开销。

### 输入输出流

- **输入**：目标形状（SDF或图像）、材料参数（杨氏模量、泊松比）、载荷条件（外力、固定边界）。
- **输出**：满足物理约束的优化形状（SDF值）、材料分布（逐单元刚度），以及对应的显式网格和应力/位移场，可直接用于下游仿真或制造。

## 核心模块与公式推导

### 3.1 隐式时间积分与弱形式

本工作采用增量势能最小化框架进行弹性动力学模拟。对于时间步长 $\Delta t$，系统状态通过最小化如下总势能来推进：

$$
\min_{\mathbf{u} \in V_{\Omega}} E_t(\mathbf{u}), \quad E_t(\mathbf{u}) := \psi(F(\mathbf{u})) + \frac{1}{2} a(\mathbf{u}, \mathbf{u}) - b(\mathbf{u})
$$

其中 $\mathbf{u}$ 为位移场，$F(\mathbf{u}) = \mathbb{I}_3 + \nabla \mathbf{u}$ 为变形梯度，$\psi$ 为超弹性能量密度，$a(\cdot,\cdot)$ 为惯性项双线性形式，$b(\cdot)$ 为外力功。该泛函的 Gâteaux 导数为零给出弱形式：

$$
a(\mathbf{u}, \mathbf{v}) + \int_{\Omega} \frac{\partial \Psi}{\partial F}(F(\mathbf{u})) : \nabla \mathbf{v} = b(\mathbf{v}) \quad \forall \mathbf{v} \in V_{\Omega}
$$

该弱形式是后续有限元离散的数学基础。

---

### 3.2 神经求积网络（Neural Quadrature Network）

**瓶颈**：传统固定求积方案在隐式表面演化时产生积分不连续或不可微，导致梯度无法可靠流向几何参数。

**核心思路**：将每个网格单元的求积点位置 $\mathbf{y}_p$ 与权重 $w_p$ 的生成转化为一个小型神经网络的学习任务。网络输入为单元各角点的 SDF 值 $\phi_j$，输出为该单元在材料域 $\Omega \cap K$ 上的求积规则。

**训练目标**基于矩拟合（moment fitting）原理：求积规则应精确积分给定阶数 $d$ 的多项式基 $\mathcal{B}_P^d$。积分误差定义为：

$$
Q_K := \sqrt{\sum_{P \in \mathcal{B}_P^d} \left( \int_{K \cap \Omega} P - \sum_p w_p P(\mathbf{y}_p) \right)^2}
$$

网络的总损失函数为：

$$
\mathcal{L}_{\mathrm{QuadNet}} := Q_K + 10^1 Q_{\perp} + \gamma_{\star} Q_{\star}
$$

其中三项分别惩罚：
- **$Q_K$**：多项式积分误差，保证数值精度；
- **$Q_{\perp}$**：边界障碍惩罚，防止求积点落在材料域外；
- **$Q_{\star}$**：权重条件数惩罚 $\frac{\max w_p}{\min w_p}$，抑制权重极端化导致数值不稳定。

**网络架构**：5 层 MLP，宽度 64/128，输出为 $P$ 个求积点的坐标与权重（Order-2 为 8 点，Order-4 为 27 点）。训练数据通过随机采样 SDF 配置生成，Order-2 网络在 RTX 3080Ti 上训练约 1.5 小时，Order-4 在 NVIDIA A40 上约 30 小时。推理阶段，对 $2^{18}$ 个体素的 Order-4 求积仅需 16ms。

**关键性质**：由于 MLP 天然连续可微，当边界 SDF 值平滑变化时，预测的求积点位置与权重也随之平滑更新，避免了 Full 和 Clip 方案的跳变（Figure 2）。

---

### 4.1 四场旋转感知混合有限元

为处理高刚度比材料（如 $10^9$ 量级的刚度差异），本工作将 Trusty et al. (2022) 的混合 FEM 推广为四场形式。引入两个额外的主变量——对称应变 $S \in \mathrm{Sym}_\Omega$ 和旋转 $R \in \mathrm{SO}_\Omega$，通过约束 $C(\mathbf{u}, R, S) := F(\mathbf{u}) - RS = 0$ 与变形梯度关联。

约束优化问题为：

$$
\min_{\mathbf{u}\in V_\Omega, S\in\mathrm{Sym}_\Omega, R\in\mathrm{SO}_\Omega} \frac{1}{2}a(\mathbf{u},\mathbf{u}) - b(\mathbf{u}) + \psi(S)
$$

引入 Lagrange 乘子 $\sigma$（即应力场），构造增广 Lagrangian：

$$
\mathcal{L}(\mathbf{u},S,R,\sigma) := \frac{1}{2}a(\mathbf{u},\mathbf{u}) - b(\mathbf{u}) + \Psi(S) + c(\mathbf{u},S,R,\sigma)
$$

关于对称应变的驻点条件为：

$$
\psi_{,S}(S;\tau) + c_{,S}\left(R; \tau, \sigma + \varepsilon C(\mathbf{u}, R, S)\right) = 0 \qquad \forall \tau \in \mathrm{Sym}_\Omega
$$

其中 $\varepsilon C$ 为约束违背的增广惩罚项。该系统通过投影 Newton 法求解，经过两次凝聚（double condensation）后得到仅含位移增量 $\delta\mathbf{u}$ 的对称正半定 Schur 补系统：

$$
\Big[ A + C_{,\mathbf{u}}^{T} \Lambda^{-1} C_{,\mathbf{u}} \Big] \thinspace \delta \mathbf{u} = \mathbf{b} - A \mathbf{u} + C_{,\mathbf{u}}^{T} \Lambda^{-1} \lambda
$$

该系统采用 Jacobi 预条件共轭梯度法高效求解。混合 FEM 在宽刚度比范围内保持 Newton 迭代的收敛速度，而纯位移 FEM 在刚度比增大时严重滞缓（Figure 6, 24）。

---

### 6.2 物理感知损失函数

为驱动形状与材料优化，定义基于位移 $\mathbf{u}$ 和应力 $\sigma$ 的组合损失：

$$
\mathcal{L}_{\mathrm{phys}}(\Delta_t, \ell_{\mathbf{u}}, \ell_{\sigma}) := \sqrt[p]{ \int_{\Omega} \frac{1}{|\det \mathrm{d}\Omega|} \left( \ell_{\mathbf{u}} \|\mathbf{u}\|^p + \ell_{\sigma} \|\sigma\|^p \right) }
$$

其中 $p=8$ 用于逼近极大范数，使优化倾向于降低峰值位移和应力。$\ell_{\mathbf{u}}$ 和 $\ell_{\sigma}$ 为两项的权重系数。

**梯度计算**：为避免完全回溯 Newton 求解过程的高昂开销，采用混合自动微分与解析伴随法。计算 $\mathrm{d}\mathcal{L}/\mathrm{d}p$ 仅需求解一个与单次 Newton 迭代规模相当的线性系统。

**优化调度**：前 30% 迭代仅使用几何/渲染损失 $\mathcal{L}_{\mathrm{FC}}$，之后加入 $\mathcal{L}_{\mathrm{phys}}$，使形状先收敛到目标几何附近再满足物理约束，避免早期梯度冲突。

---

### 辅助模块

- **平滑预条件器**：对网格 SDF 参数和顶点位移施加高斯模糊卷积，抑制高频噪声，稳定重建优化。
- **FlexiCubes 重建**：从可微隐式表面提取显式网格，用于渲染和边缘长度损失计算。

## 实验与分析

### 核心实验验证

#### 神经求积的平滑性与可微性

神经求积的核心优势在于其平滑性。Figure 2 展示了二维边界体素上三种求积方案的行为：当隐式边界移动时，Full 和 Clip 求积的积分点位置和权重发生跳变，而神经求积的积分点和权重平滑更新。这一平滑性直接打通了从物理响应到隐式表面参数的梯度通道——消融实验（Figure 17）证实，将神经求积替换为 Full 或 Clip 求积后，物理损失对顶点 SDF 值的梯度完全消失，优化无法收敛。

#### 粗网格下的精度保持

Figure 5 展示了哑铃平衡形状在不同分辨率下的表现。在精细的 $64^3$ 分辨率下，所有方法收敛到相同形状。但在粗分辨率下，差异显著：
- **Full 求积**（三次线性单元）显著低估变形量；
- **Clip 求积**出现数值不稳定；
- **线性四面体网格**（从隐式表面提取）同样低估变形；
- **神经求积 + 混合 FEM**（三次线性位移）在 $16^3$ 分辨率下仍能获得接近高分辨率参考的平衡形状，且与三次二次嵌入模拟和二次四面体网格的性能相当。

Figure 7 的屈曲实验进一步验证了这一结论：在粗分辨率下，使用三次二次位移的神经求积能够捕捉到与 $64^3$ 参考解高度一致的屈曲形状，而三次线性的 Full/Clip 求积则严重偏离。

#### 亚像素异质性捕获

Figure 8 展示了带有亚体素级特征的板的模拟结果。Full 求积将材料视为均匀介质，无法分辨亚像素结构；Clip 求积产生错误的应变传递；神经求积在不增加额外计算成本的前提下，正确捕获了亚像素几何的力学响应细节。

#### 高刚度比下的收敛性

Figure 6 揭示了混合 FEM 相对于纯位移 FEM 的关键优势。当哑铃中心区域的刚度比从 $10^0$ 逐步提升至 $10^9$ 时，纯位移 FEM 在 250 次牛顿迭代后仍远离收敛平衡态，而混合 FEM 始终保持快速收敛。Figure 24 进一步量化了这一差异：在均匀材料（黑色曲线）下三种 FEM 变体表现相近，但在 $10^6$ 刚度比（红色曲线）下，混合 FEM 在每次牛顿迭代和实际运行时间上均显著优于纯位移 FEM。这一优势直接影响了后续的材料优化任务——若使用纯位移 FEM，物理损失被系统性低估，导致材料刚度优化不充分（Figure 16）。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2410_09417/figures/004_Figure_6.jpg]]
*Figure 6: At high stiffness ratio, displacement-only FEM suffers from slow convergence, while Mixed FEM does not. Here, the center region of the dumbbell is stiffened by an increasing factor, and in each case the Newton loop is truncated after 250 iterations*

### 物理感知优化的应用验证

#### 应力最小化与拓扑演化

Figure 10 展示了支架在给定载荷下的应力最小化优化过程。优化器在前 30% 迭代中仅使用几何/渲染损失进行形状重建，随后激活物理损失。最终物理损失降低超过一个数量级，同时形状自然演化出符合力学直觉的拓扑结构。

#### 软体椅子重建与抗压能力

Figure 11 在 Pix3D 数据集上验证了物理感知重建的有效性。在极软材料（承受 2.5kN 和 0.5kN 力）条件下，纯几何重建的椅子严重坍塌，而物理感知重建的椅子能够抵抗载荷。Figure 12 展示了优化过程中出现的拓扑变化细节：靠背支撑的生长与雕琢、办公椅额外支撑脚的出现、以及损坏目标形状的自动修复。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2410_09417/figures/011_Figure_12.jpg]]
*Figure 12: Details of some topology changes in our soft chairs example. Top: Additional backrest support being grown then carved out. Bottom, left: Additional feet being grown for support on an office chair. Right: Repairing of a damaged target shape. Fig. 13. Optimizing the stability such that the chair remains stable to a force applied on the backrest. From left to right, reconstructed shape without (naive) then with (ours) physics-aware loss, simulated reconstruction without (naive) then with (ours) physics-aware loss. The yellow ball on the rest geometries indicates the position of the center of mass*

#### 稳定性优化

Figure 13 展示了椅子在靠背受力下的稳定性优化。纯重建的椅子因质心位置不当而倾覆；物理感知损失驱动优化器在椅子前部增加材料，使质心前移，椅子保持稳定。

#### 形状与材料并发优化

Figure 14 展示了椅子的形状和杨氏模量并发优化。优化器自动识别力学关键区域（腿部、连接处）并增加其刚度，最终显著减少下垂量。Figure 16 的弹性哑铃材料优化对比进一步验证：使用混合 FEM 的材料优化比纯位移 FEM 更有效——后者因收敛不足导致刚度提升不充分，残余变形更大。

### 消融实验

Figure 17 系统性地移除了框架的关键组件：

1. **移除神经求积**：物理损失对 SDF 的梯度消失，优化完全停滞。
2. **移除平滑预条件器**：重建表面出现严重噪声，几乎不可用。
3. **移除边缘长度损失**：表面出现浮动物和不必要的凸起。
4. **用双行进立方体替代 FlexiCubes**：尖锐特征无法被正确捕捉。

此外，Figure 23 将神经求积与仅优化权重的矩拟合方法（Müller et al., 2013）及 Clip 求积进行了积分误差统计对比，神经求积在 1000 个随机体素上的积分精度显著优于两种基线。

### 失败模式与局限性

尽管神经求积在积分精度和可微性上表现优异，但框架存在以下已知失败模式：

- **浮动材料问题**：当材料区域与主体断开连接时，位移自由度仍受限于底层连续形函数，导致浮动块无法在重力下自由掉落。论文指出这需要引入类似 XFEM 或 CPIC 的额外自由度来解决。
- **优化非全局收敛**：物理感知重建的结果对初始随机 SDF 值敏感，不同初始化可能导致显著不同的最终形状，且对损失函数选择高度敏感。
- **混合 FEM 的惩罚参数依赖**：当前四场混合 FEM 方案依赖经验性的惩罚参数 $\varepsilon$，尚未找到完全消除惩罚的双凝聚方案（仅在各向同性应变下有解析解）。
- **神经求积的泛化限制**：网络需针对特定积分阶数和元素类型训练，Order-4 网络训练耗时 30 小时（NVIDIA A40），推理虽快（$2^{18}$ 体素仅需 16ms），但更换弹性模型或网格类型可能需要重新训练。

### 公平性说明

需要指出，论文未与其它可微弹性或拓扑优化方法（如基于密度的 SIMP 方法、基于网格的拉格朗日方法）进行系统性定量比较。实验集中在准静态和少数动态场景，在大规模或高频动态问题中的表现尚未验证。神经求积网络的超参数敏感性分析也较为有限。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2410_09417/figures/017_Figure_21.jpg]]
*Figure 21: Statistics of integration error and conditioning max ???? /min ???? over 1000 random voxels for networks trained with order ?? and conditioning loss scaling factor ??★*

## 方法谱系与知识库定位

### 1. 方法演进脉络

本文提出的**神经集成混合有限元（Neurally Integrated Mixed FEM）** 处于两条技术路线的交汇点：基于隐式表面的可微物理模拟，以及面向演化域的数值积分方法。其核心创新在于用一个小型神经网络替代传统的固定求积规则，从而打通从物理响应（位移、应力）到隐式表面几何参数的梯度通道，使端到端的形状、拓扑与材料联合优化成为可能。

#### 1.1 可微弹性模拟的谱系

在可微物理模拟领域，已有工作主要沿两条路径展开：

- **基于网格的拉格朗日方法**：传统有限元在显式网格上执行，梯度通过伴随法或自动微分获得。然而，当几何拓扑发生变化时，显式网格需要频繁重划分，导致梯度流断裂。本文通过将几何表达统一为隐式表面（SDF），在固定规则网格上执行模拟，规避了网格拓扑变化带来的可微性障碍。

- **基于密度的拓扑优化（如SIMP方法）**：这类方法在像素或体素级别优化材料密度分布，天然可微但缺乏清晰的几何边界，难以与下游渲染或制造流程衔接。本文通过FlexiCubes从隐式表面提取显式网格，实现了物理模拟与几何重建的双向可微耦合。

本文的混合FEM求解器直接继承自**Trusty et al. (2022)** 的旋转感知混合有限元公式，但将其从两场（位移、应力）推广到四场（位移、对称应变、旋转、应力），并引入增广拉格朗日惩罚项以处理任意有限元离散。这一推广使得求解器能够在粗网格上处理高达10^9的刚度比（Figure 6, 24），而纯位移FEM在同等条件下收敛停滞。

#### 1.2 求积规则演化的瓶颈突破

在隐式表面演化过程中，数值积分的可微性是长期被忽视的瓶颈。传统方案存在根本性缺陷：

- **Full quadrature**（标准Gauss-Legendre求积）：在整个参考单元上积分，对跨越边界的单元引入不连续的材料分布，导致积分误差大且梯度不可靠。
- **Clip quadrature**（基于指示函数的加权求积）：在边界移动时求积点位置发生跳变（Figure 2），破坏了积分映射的连续性，使梯度无法流向几何参数。
- **Moment fitting**（矩拟合，如Müller et al. 2013）：通过线性规划选择稀疏求积子集，但对SDF值的微小变化会产生求积点位置的剧烈跳变（Figure 22），同样不可微。

本文的核心洞察在于：**将求积规则预测转化为一个学习任务**。通过训练一个小型MLP（5层，宽度64/128）从局部SDF值直接预测求积点位置和权重，既保证了积分精度（矩拟合误差作为损失函数的一部分），又天然输出连续可微的映射。消融实验（Figure 17）提供了决定性证据：移除神经求积后，物理损失对顶点SDF值的梯度完全消失，优化无法收敛。

### 2. 与基线方法的关系定位

#### 2.1 直接基线与对比

| 基线方法 | 角色 | 本文超越之处 |
|---------|------|-------------|
| Full quadrature | 常规数值积分基线 | 边界移动时积分不连续；本文神经求积实现平滑更新（Figure 2） |
| Clip quadrature | 基于指示函数的积分基线 | 求积点跳变导致梯度断裂；本文消除跳变，打通梯度通道 |
| Displacement-only FEM | 标准有限元弹性模拟器 | 高刚度比下收敛停滞；本文混合FEM在10^9刚度比下仍收敛（Figure 6） |
| **FlexiCubes** (Shen et al., SIGGRAPH 2023) | 纯几何重建基线 | 无物理感知；本文在其基础上加入物理损失，实现形状-物理联合优化 |
| **Mixed FEM** (Trusty et al., 2022) | 旋转感知混合FEM基线 | 限于两场公式；本文推广至四场，支持任意有限元离散 |

#### 2.2 与相邻工作的差异

- **vs. 可微MPM（物质点法）**：MPM天然处理大变形和拓扑变化，但难以提供清晰的几何边界用于渲染或制造。本文基于隐式表面+SDF的方案在几何表达精度上更优，但当前限于弹性材料，尚未扩展到MPM擅长的塑性或流体场景。
- **vs. 基于神经网络的物理代理模型**：一些工作用大型神经网络直接预测物理响应，但缺乏物理方程的结构化约束，泛化性存疑。本文的神经求积仅替代积分环节，仍保留完整的FEM求解器，保证了物理一致性。

### 3. 适用边界与局限

#### 3.1 已证实的适用范围

- **准静态与动态弹性模拟**：在规则网格上支持动力学和准静态求解，适用于宽范围材料刚度（Figure 6, 24）。
- **形状、拓扑与材料的联合优化**：在单一优化循环中同时调整SDF几何、拓扑连接和杨氏模量分布（Figure 14, 16）。
- **亚像素特征捕获**：神经求积能在粗网格上正确模拟亚体素尺度的异质性，而Full/Clip求积在相同网格下失败（Figure 8）。
- **图像引导的物理感知重建**：在Pix3D椅子数据集上，物理感知重建使软质椅子能承受2.5kN/0.5kN的外力而不坍塌（Figure 11）。

#### 3.2 已确认的局限

1. **浮动材料区的物理失实**：神经求积可以计算复杂隐式区域的积分，但位移自由度仍受限于底层连续形函数。这意味着与主体断开连接的浮动材料区域（floaters）无法正确模拟其在重力下的自由掉落行为。论文指出，引入XFEM或CPIC风格的额外自由度是可能的解决方向。

2. **全局收敛性缺失**：物理感知重建算法对初始SDF值敏感——不同的随机初始化会导致最终形状的显著差异。此外，结果对损失函数的选择非常敏感，目前缺乏理论保证的收敛性。

3. **混合FEM的惩罚参数依赖**：四场增广拉格朗日公式当前依赖于经验性选择的惩罚参数ε。对于非各向同性应变，尚未找到完全消除惩罚的双凝聚方案。

4. **神经求积网络的泛化限制**：网络需针对特定积分阶数和元素类型进行训练。Order-2网络训练约1.5小时（RTX 3080Ti），Order-4网络约30小时（NVIDIA A40）。推理虽快（Order-4对2^18体素约16ms），但更换弹性模型或网格类型可能需要重新训练，论文未讨论泛化性。

5. **材料模型受限**：当前方法限于弹性材料（使用Stable Neo-Hookean模型，Poisson比ν=0.4）。扩展到塑性、断裂或超弹性损伤等非线性材料尚未讨论。

### 4. 开放问题

1. **浮动区域的物理建模**：如何通过引入额外自由度（如XFEM富集函数或CPIC粒子）使断开连接的区域能真实地从主体脱落？

2. **全局收敛性改进**：能否通过更先进的优化策略（如信赖域方法）、基于感知的损失函数，或更好的预条件器来实现物理感知重建的全局收敛？

3. **跨物理过程的推广**：该框架能否扩展到其他物理过程？例如，用可微MPM初始化隐式表面以处理流体或颗粒材料，或用神经求积替代其他PDE求解器中的积分环节？

4. **参数自由的混合FEM**：是否可以为混合FEM推导出解析的本征体系，从而完全移除惩罚参数ε，实现参数自由的双凝聚方案？

5. **神经求积的进一步优化**：网络架构和训练策略是否可以改进以降低推理开销？能否训练一个统一的网络来处理多种积分阶数或元素类型？

6. **多物理场与复杂材料**：如何扩展以支持更丰富的材料模型（如塑性、黏弹性、损伤力学）以及热-力耦合等多物理场场景？

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/Neurally_Integrated_Finite_Elements_for_Differentiable_Elasticity_on_Evolving_Domains.pdf]]
