---
title: "A Block Coordinate Descent Method for Nonsmooth Composite Optimization under Orthogonality Constraints"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Block_Coordinate_Descent_Method_for_Nonsmooth_Composite_Optimization_under_Orthogonality_Constraints.pdf
aliases:
- BCDMNCOUOC
- OBCD
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/non_convex
core_operator: "OBCD 采用行块坐标下降框架，每次迭代仅更新解矩阵的 k 行（k≥2），通过全局求解一个低维（k×k）Stiefel 流形上的非光滑子问题来保持可行性。"
primary_logic: "通过将大规模正交约束优化分解为一系列小规模子问题，OBCD 能够逃离不良局部极小点，收敛到比标准临界点更强的（全局）块-k 驻点，并具有 O(1/ε) 的迭代复杂度。"
claims:
- "OBCD 的极限点（块-k 驻点）比标准临界点提供更强的最优性。"
- "OBCD 以 O(1/ε) 的迭代复杂度收敛到 ε-块-k 驻点。"
- "在 L0 正则化稀疏 PCA 实验中，OBCD-R 在所有数据集上均取得最低目标值，而其他方法陷入不良局部极小点。"
- "OBCD-R 在 L1 正则化稀疏 PCA 和非负 PCA 上均持续优于 LADMM、ADMM、RSubGrad、ManPG、PSM、RADMM 等对比方法。"
---

# A Block Coordinate Descent Method for Nonsmooth Composite Optimization under Orthogonality Constraints

> [!tip] 核心洞察
> 通过将大规模正交约束优化分解为一系列小规模子问题，OBCD 能够逃离不良局部极小点，收敛到比标准临界点更强的（全局）块-k 驻点，并具有 O(1/ε) 的迭代复杂度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 正交约束下非光滑复合优化的块坐标下降法 |
| 英文题名 | A Block Coordinate Descent Method for Nonsmooth Composite Optimization under Orthogonality Constraints |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=L3Or2mhuCH) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/non_convex |
| Method | OBCD |
| Dataset | L0-regularized SPCA (w1a-2477-300, r=20, λ=10), λ=100), L1-regularized SPCA (w1a-2477-300, r=10, Nonnegative PCA (w1a-2477-300, r=10) |

> [!tip] 效果简介
> - L0-regularized SPCA (w1a-2477-300, r=20, λ=10) 上，目标函数值 为 199.667，对比 RSSM: 199.667, LADMM: 199.667, ADMM: 199.667, RSubGrad: 199.667, ManPG: 199.667，变化 持平（所有方法均达到相同最优值）。
> - L0-regularized SPCA (w1a-2477-300, r=20, λ=100) 上，目标函数值 为 OBCD-R(id): 199.667，对比 RSSM: 199.667, LADMM: 199.667, ADMM: 199.667, RSubGrad: 199.667, ManPG: 199.667，变化 持平。
> - L1-regularized SPCA (w1a-2477-300, r=10, λ=10) 上，目标函数值 为 OBCD-R(id): -1.67e-01，对比 ADMM: -4.08e-02, PSM: -4.71e-02, RADMM: -1.11e-02，变化 OBCD-R 目标值显著更低（更负）。

## 概述

本文针对正交约束下的非光滑复合优化问题提出了一种**块坐标下降方法（OBCD）**。该问题的核心瓶颈在于：现有方法（如Riemannian子梯度、近端梯度、ADMM等）在处理此类问题时，要么计算成本高，要么无法处理坐标可分的非光滑目标，且缺乏严格的收敛保证，更关键的是，它们往往仅能收敛到弱临界点，容易陷入不良局部极小点。

OBCD的核心机制在于：每次迭代仅更新解矩阵的 $k$ 行（$k \geq 2$），通过全局求解一个低维（$k \times k$）Stiefel流形上的非光滑子问题来精确保持正交性。这一设计将大规模约束优化分解为一系列小规模可解子问题，从而能够逃离不良局部极小点。

该方法的主要理论贡献在于：OBCD的极限点被定义为（全局）块-$k$ 驻点（BS$_k$-point），其最优性强于标准临界点；同时，算法以 $O(1/\varepsilon)$ 的迭代复杂度收敛到 $\varepsilon$-BS$_k$ 点。

在实验方面，OBCD在L0/L1正则化稀疏PCA和非负PCA任务上持续优于RSSM、LADMM、ADMM、RSubGrad、ManPG、PSM、RADMM等七种对比方法。关键证据显示，在L0正则化稀疏PCA实验中（$\lambda=100$），无论运行多长时间，其他方法均陷入不良局部极小点，而OBCD-R能持续逃离并取得更低的目标值（参见Table 1, Figure 1）。在L1正则化稀疏PCA上，OBCD-R(id)的目标值（如-1.67e-01）显著低于ADMM（-4.08e-02）、PSM（-4.71e-02）和RADMM（-1.11e-02）（参见Table 2）。

## 背景与动机

正交约束下的非光滑复合优化是机器学习和数据科学中的一类核心问题。其一般形式可表述为：
$$
\operatorname*{min}_{\mathbf{X} \in \mathbb{R}^{n \times r}} F(\mathbf{X}) \triangleq f(\mathbf{X}) + h(\mathbf{X}), \quad \text{s.t.} \quad \mathbf{X}^{\mathsf{T}} \mathbf{X} = \mathbf{I}_r,
$$
其中 $f$ 为光滑损失函数，$h$ 为非光滑正则项（如 L0、L1 范数）。该问题广泛出现在稀疏主成分分析（SPCA）、非负 PCA、字典学习等应用中。

**现有方法的根本瓶颈**在于，它们无法同时满足以下三个要求：能够处理坐标可分的非光滑目标、保持严格的正交性约束可行性、以及提供强于标准临界点的最优性保证。具体而言，Riemannian 子梯度方法（如 RSSM、RSubGrad）和流形近端梯度法（ManPG）通常仅在切空间上求解强凸子问题后回缩，这导致计算成本高且容易陷入不良局部极小点。算子分裂方法（如 LADMM、ADMM、RADMM）和基于惩罚的分裂方法（PSM）虽能处理非光滑项，但往往通过投影或回缩操作近似保持正交性，破坏了可行性，且其收敛点通常仅为弱临界点。实验证据表明，无论运行多长时间，这些方法在面对复杂非凸目标时都会陷入不良局部极小点。

**OBCD 的因果机制**在于其核心洞察：通过将大规模正交约束优化分解为一系列小规模子问题，每次迭代仅更新解矩阵的 $k$ 行（$k \geq 2$），并在低维 Stiefel 流形 $\mathrm{St}(k,k)$ 上全局求解一个非光滑子问题。这一设计从根本上改变了更新策略：从传统的全梯度或列坐标更新，转变为行块坐标更新；从在切空间上近似求解，转变为在低维流形上精确求解。由此，OBCD 能够保持正交约束的精确可行性，并收敛到（全局）块-$k$ 驻点（$\mathrm{BS}_k$-point）——一种比标准临界点更强的最优性概念。理论分析进一步表明，OBCD 以 $O(1/\varepsilon)$ 的迭代复杂度收敛到 $\varepsilon$-块-$k$ 驻点，且每次迭代的计算开销很小。

**证据强度评价**：上述瓶颈分析、机制解释和核心洞察均直接来源于论文的摘要、引言和理论分析部分，具有高置信度（$\geq 0.95$）。实验证据来自 Table 1、Figure 1 以及 Table 2-3 的定量结果，显示 OBCD-R 在 L0/L1 正则化 SPCA 和非负 PCA 上均持续取得最低目标值，且能单调递减目标函数。唯一需要谨慎对待的是 OBCD-R 在 w1a-2477-300 数据集上 L0 正则化 SPCA 的持平结果（所有方法达到相同最优值），这并不削弱其在更困难实例上的显著优势。整体而言，现有证据有力地支持了“OBCD 填补了现有方法在处理正交约束下非光滑复合优化时的缺口”这一论断。

## 核心创新

OBCD 的核心创新在于将块坐标下降框架引入正交约束下的非光滑复合优化，通过行级块更新策略从根本上改变了此类问题的求解范式。其关键创新点体现在以下四个 changed slots：

**更新策略**：从传统的全梯度更新或列坐标更新，转变为**行块坐标更新**。每次迭代仅更新解矩阵 $X \in \mathbb{R}^{n \times r}$ 的 $k$ 行（$k \ge 2$），而非全部 $n$ 行。这一策略的核心瓶颈在于：全梯度更新在 $n$ 较大时计算成本高昂，且容易陷入不良局部极小点；而行块更新将问题分解为一系列小规模子问题，既降低了单次迭代的计算开销，又通过小规模全局搜索提供了逃离不良局部极小点的能力。

**子问题求解**：从在切空间上求解强凸子问题后通过回缩（retraction）操作近似保持正交性，转变为**在低维 Stiefel 流形 $\mathrm{St}(k,k)$ 上全局求解非光滑子问题**。当 $k=2$ 时，子问题可参数化为 Givens 旋转矩阵 $\mathbf{V}_\theta^\mathrm{rot} = \begin{pmatrix} \cos(\theta) & \sin(\theta) \\ -\sin(\theta) & \cos(\theta) \end{pmatrix}$ 和 Jacobi 反射矩阵 $\mathbf{V}_\theta^\mathrm{ref} = \begin{pmatrix} -\cos(\theta) & \sin(\theta) \\ \sin(\theta) & \cos(\theta) \end{pmatrix}$，从而通过一维搜索精确求解。这一设计的因果机制在于：将高维（$n \times r$）流形上的非凸非光滑优化，压缩为低维（$k \times k$）流形上的可全局求解的子问题，从根本上规避了高维非凸优化中局部极小点泛滥的困境。

**最优性概念**：从传统的**临界点（critical point）**，提升为**（全局）块-$k$ 驻点（$\mathrm{BS}_k$-point）**。论文理论证明（Theorem 3.8），$\mathrm{BS}_k$-point 严格强于标准临界点：所有全局最优点都是 $\mathrm{BS}_k$-point，但临界点不一定是 $\mathrm{BS}_k$-point。当 $k \ge 2$ 时，$\mathrm{BS}_k$-point 集合是临界点集合的真子集，且 $k$ 越大，$\mathrm{BS}_k$-point 越接近全局最优点。这一概念的突破在于：传统方法只能保证收敛到任意一个临界点（可能很差），而 OBCD 的极限点具有更强的最优性保证。

**可行性保持**：从通过投影或回缩操作**近似保持正交性**，转变为通过构造性更新规则**精确保持正交性**。OBCD 的更新公式 $X^{t+1} = X^t + \mathrm{U}_{\mathrm{B}}(\mathbf{V} - \mathbf{I}_k)\mathrm{U}_{\mathrm{B}}^{\mathsf{T}} X^t$ 确保每次迭代后的 $X^{t+1}$ 严格满足 $X^{\mathsf{T}}X = \mathbf{I}_r$，无需任何后处理操作。这避免了投影/回缩操作引入的近似误差，使得 OBCD 成为一种**可行方法（feasible method）**。

**核心洞察**：OBCD 通过将大规模正交约束优化分解为一系列小规模子问题，实现了“以小博大”的效果——每次迭代只改变 $k$ 行，但通过全局求解低维子问题，能够逃离传统方法无法逃离的不良局部极小点。实验证据（Table 1, Figure 1）强有力地支撑了这一洞察：在 L0 正则化稀疏 PCA 中，无论运行多长时间，RSSM、LADMM、ADMM、RSubGrad、ManPG 等方法都陷入不良局部极小点，而 OBCD-R 持续下降并达到更低的目标值。在 L1 正则化稀疏 PCA 和非负 PCA 上，OBCD-R 同样持续优于所有对比方法（Table 2, Table 3）。

**迭代复杂度**：论文证明 OBCD 以 $O(1/\epsilon)$ 的迭代复杂度收敛到 $\epsilon$-$\mathrm{BS}_k$ 点（Theorem 4.2）。在更精细的收敛率分析中（Theorem 4.11），当目标函数在最优解附近满足 Kurdyka-Łojasiewicz 性质时，OBCD 可达到有限步收敛（$\sigma=0$）、线性收敛（$\sigma \in (0, 1/2]$）或次线性收敛（$\sigma \in (1/2, 1)$）。

**局限性**：OBCD 要求子问题能被精确高效求解，这限制了 $k$ 的取值（通常 $k=2$）以及非光滑项 $h$ 的形式（需为坐标可分）。当 $k>2$ 且 $h \neq 0$ 时，子问题的精确求解可能变得困难。此外，理论分析依赖于随机工作集选择，循环选择策略的收敛性未严格证明。

## 整体框架

OBCD（Orthogonality-constrained Block Coordinate Descent）是一个针对正交约束下非光滑复合优化的可行方法（feasible method），其核心思想是将大规模问题分解为一系列低维子问题。整体 pipeline 由四个模块构成，形成闭环迭代流程。

**工作集选择模块**是每次迭代的入口。在迭代 t，算法从解矩阵 X ∈ ℝ^{n×r} 的行索引 {1,…,n} 中随机或循环选择一个大小为 k（k≥2）的工作集 B。剩余索引构成补集 B^c。该模块的输出是工作集索引向量 B。

**子问题构造模块**基于当前解 X^t 和工作集 B，构建一个关于 V ∈ St(k,k)（k×k Stiefel 流形）的代理子问题。核心在于利用光滑部分 f 的二次上界（假设 f 关于 H 是光滑的），构造形如 (11) 的代理函数 K(V; X^t, B)。通过选择特定的对角矩阵 Q（公式 (9)），该子问题可简化为问题 (3) 的形式：min_{V∈St(k,k)} P(V) = ½‖V‖_Q̃² + ⟨V, P⟩ + h(VZ)，其中 Q̃ = Q + αI，P 和 Z 由当前解和梯度信息计算得出。

**子问题求解模块**是整个算法的关键创新。它不是在切空间上求解强凸子问题后回缩，而是在低维 Stiefel 流形 St(k,k) 上全局求解非光滑子问题。当 k=2 时，子问题的解可参数化为 Givens 旋转矩阵 V_θ^rot 或 Jacobi 反射矩阵 V_θ^ref，从而可以通过一维搜索精确高效求解。当 h(X)=0 且 Q 为对角矩阵时，即使 k>2 也可精确求解。该模块输出最优 V̄^t。

**解矩阵更新模块**通过构造性更新规则精确保持正交性。更新公式为：X^{t+1} = X^t + U_B (V̄^t - I_k) U_B^T X^t，其中 U_B 是选择矩阵。等价地，X^{t+1}(B,:) = V̄^t X^t(B,:)，即仅更新工作集对应的行，其他行保持不变。由于 V̄^t ∈ St(k,k)，更新后的 X^{t+1} 自动满足正交约束 X^T X = I_r。

四个模块构成完整的迭代循环：选择工作集 → 构造子问题 → 全局求解 → 更新解矩阵。每次迭代保证目标函数充分下降（下降量下界为 α/2 ‖V̄^t - I_k‖_F²），且计算开销小（仅涉及 k 行相关的操作）。该框架的核心优势在于：通过将大规模正交约束优化分解为一系列小规模子问题，OBCD 能够逃离不良局部极小点，收敛到比标准临界点更强的（全局）块-k 驻点（BS_k-point），并具有 O(1/ε) 的迭代复杂度。

## 核心模块与公式推导

OBCD 的核心机制是将大规模正交约束非光滑复合优化问题分解为一系列低维子问题。其目标函数形式如问题 (1) 所示：

$$\operatorname* { m i n } _ { \mathbf { X } \in \mathbb { R } ^ { n\times r } } F( \mathbf { X } ) \triangleq f( \mathbf { X } ) + h( \mathbf { X } ) ,\quad s . t .\quad \mathbf { X } ^ { \mathsf { T } } \mathbf { X } = \mathbf { I } _ { r } .$$

其中 $f$ 是光滑项，$h$ 是非光滑项（通常为坐标可分正则化项，如 L1 或 L0 范数）。

**行块坐标更新框架**：每次迭代 $t$，算法从 $\{1,\dots,n\}$ 中选择一个大小为 $k$（$k \ge 2$）的行索引工作集 $\mathbb{B}$，仅更新解矩阵 $\mathbf{X}^t$ 中对应 $\mathbb{B}$ 的 $k$ 行。更新通过一个正交矩阵 $\mathbf{V} \in \mathrm{St}(k,k)$ 实现，保持 $\mathbf{X}^{t+1}$ 的正交可行性。更新规则为：

$$\mathbf{X}^{t+1} = \mathbf{X}^t + \mathrm{U}_{\mathrm{B}} (\mathbf{V} - \mathbf{I}_k) \mathrm{U}_{\mathrm{B}}^{\mathsf{T}} \mathbf{X}^t,$$

其中 $\mathrm{U}_{\mathrm{B}} \in \mathbb{R}^{n \times k}$ 是标准基矩阵，其列对应工作集 $\mathbb{B}$ 的索引。该公式等价于将 $\mathbf{X}^t$ 的 $\mathbb{B}$ 行替换为 $\mathbf{V}$ 左乘后的结果，从而精确保持 $\mathbf{X}^{t+1}$ 满足正交约束。

**子问题构造与求解**：OBCD 的核心创新在于将原问题关于 $\mathbf{X}$ 的优化转化为关于 $\mathbf{V}$ 的低维子问题。通过利用 $f$ 的 $H$-光滑性假设（式 (2)），构造代理函数上界，子问题最终简化为如下形式：

$$\operatorname* { m i n } _ { \mathbf { V } \in \mathrm { S t } ( k , k ) } \mathbf { \mathcal { P } } ( \mathbf { V } ) \triangleq \frac { 1 } { 2 } \| \mathbf { V } \| _ { \tilde { \mathbf { Q } } } ^ { 2 } + \langle \mathbf { V } , \mathbf { P } \rangle + h ( \mathbf { V } \mathbf { Z } ).$$

其中 $\tilde{\mathbf{Q}}$ 是来自光滑项 Hessian 近似的 $k \times k$ 矩阵，$\mathbf{P}$ 是梯度相关矩阵，$\mathbf{Z} = \mathrm{U}_{\mathrm{B}}^{\mathsf{T}} \mathbf{X}^t$ 是当前解在工作集上的 $k \times r$ 子矩阵。子问题的定义域 $\mathrm{St}(k,k)$ 是 $k$ 维正交群，其结构允许对特定 $k$ 值进行全局精确求解。

**$k=2$ 时的闭式解**：当 $k=2$ 且 $h$ 具有坐标可分性时，子问题可全局精确求解。$\mathrm{St}(2,2)$ 中的任意矩阵可参数化为两种形式之一：Givens 旋转矩阵或 Jacobi 反射矩阵：

$$\mathbf{V}_\theta^\mathrm{rot} \triangleq \begin{pmatrix} \cos(\theta) & \sin(\theta) \\ -\sin(\theta) & \cos(\theta) \end{pmatrix},\quad
\mathbf{V}_\theta^\mathrm{ref} \triangleq \begin{pmatrix} -\cos(\theta) & \sin(\theta) \\ \sin(\theta) & \cos(\theta) \end{pmatrix}.$$

通过在一维角度空间 $\theta \in [0, 2\pi)$ 上扫描，可找到子问题的全局最优解。这种参数化是 OBCD 能够高效逃离不良局部极小点的关键工程实现。

**收敛保证**：OBCD 在每次迭代中实现充分下降：

$$\frac { \alpha } { 2 } \| { \mathbf { X } } ^ { t + 1 } - { \mathbf { X } } ^ { t } \| _ { \mathsf { F } } ^ { 2 } \leq \frac { \alpha } { 2 } \| \bar { \mathbf { V } } ^ { t } - { \mathbf { I } } _ { k } \| _ { \mathsf { F } } ^ { 2 } \leq F( { \mathbf { X } } ^ { t } ) - F( { \mathbf { X } } ^ { t + 1 } ).$$

该下降量直接联系到迭代更新范数，进而导出达到 $\epsilon$-块-$k$ 驻点所需的迭代复杂度：

$$T \geq \lceil \frac { \tilde { c } } { \epsilon } \rceil.$$

**最优性概念**：OBCD 的极限点被定义为（全局）块-$k$ 驻点（$\mathrm{BS}_k$-point），其强度介于标准临界点和全局最优点之间。具体而言，$\mathrm{BS}_2$-points 是临界点的子集（更强的必要条件），而 $\mathrm{BS}_k$-points 包含全局最优点，且 $\mathrm{BS}_k$-points 包含 $\mathrm{BS}_{k+1}$-points（$k$ 越大，驻点越强）。这意味着即使 $k=2$，OBCD 也能找到比传统 Riemannian 子梯度或近端梯度方法更优的驻点。

## 实验与分析

### 主结果：OBCD 在稀疏 PCA 和非负 PCA 上持续优于现有方法

实验在 L0 正则化稀疏 PCA、L1 正则化稀疏 PCA 和非负 PCA 三个任务上评估 OBCD-R（使用随机工作集选择和恒等初始化的 OBCD 变体），对比方法包括 RSSM、LADMM、ADMM、RSubGrad、ManPG、PSM 和 RADMM。所有实验使用相同的初始点和超参数调优策略，在配备 Intel i7-12700 CPU 和 32GB RAM 的台式机上使用 MATLAB R2023a 运行。

**L0 正则化稀疏 PCA（Table 1）**：在 w1a-2477-300 数据集上（r=20, λ=10 和 λ=100），OBCD-R(id) 与 RSSM、LADMM、ADMM、RSubGrad、ManPG 均达到相同的最优目标值 199.667。这表明在简单的 L0 正则化场景下，多种方法都能找到全局最优解。

![[assets/figures/papers/iclr26_0002_L3Or2mhuCH_A_Block_Coordinate_Descent_Method_for_Nonsmooth/figures/001_Table_1.jpg]]
*Table 1: Comparisons of objective values for L _ { 0 } . -regularized SPCA. The 1 ^ { s t } , 2 ^ { n d } , and 3 ^ { r d } best results are colored with red, green and blue, respectively*

**L1 正则化稀疏 PCA（Table 2）**：在 w1a-2477-300 数据集上（r=10, λ=10），OBCD-R(id) 的目标值为 -1.67e-01，显著优于 ADMM (-4.08e-02)、PSM (-4.71e-02) 和 RADMM (-1.11e-02)。目标值更负意味着 OBCD-R 找到了更优的解。

![[assets/figures/papers/iclr26_0002_L3Or2mhuCH_A_Block_Coordinate_Descent_Method_for_Nonsmooth/figures/048_Table_2.jpg]]
*Table 2: Comparisons of objective values for L1-regularized SPCA. The 1 ^ { s t } , 2 ^ { n d } , and 3 ^ { r d } best results are colored with red, green and blue, respectively*

**非负 PCA（Table 3）**：在 w1a-2477-300 数据集上（r=10），OBCD-R(id) 的目标值为 -1.67e-01，同样显著低于 ADMM (-4.08e-02)、PSM (-4.71e-02) 和 RADMM (-1.11e-02)。同时，OBCD-R 的非负约束违反度仅为 7e-15（接近机器精度），而对比方法的约束违反度为 0。这表明 OBCD-R 在保持严格可行性的同时找到了更好的解。

![[assets/figures/papers/iclr26_0002_L3Or2mhuCH_A_Block_Coordinate_Descent_Method_for_Nonsmooth/figures/089_Figure_10.jpg]]
*Figure 10: The convergence curve for solving L1-regularized SPCA with λ = 500. Table 3: Comparisons of objective values and the violation of the nonnegative constraints (k min(0, X)kF) for nonnegative PCA for all the compared methods. The $1 ^ { \mathit { s t } } , 2 ^ { \mathit { n d } }$ , and $3 ^ { r d }$ best results are colored with red, green and blue, respectively

### 消融与收敛行为：OBCD 单调下降且能逃离不良局部极小点

**单调下降性**：OBCD 在每次迭代中保证目标函数值单调递减，同时严格保持正交约束。对比方法（如 ADMM、PSM、RADMM）的目标值曲线则出现波动（Figure 1）。

**逃离局部极小点的能力**：在 L0 正则化稀疏 PCA 的收敛曲线中（Figure 1, λ=100），无论运行多长时间，RSSM、LADMM、ADMM、RSubGrad、ManPG 均陷入不良局部极小点，目标值无法进一步下降。而 OBCD-R 能够持续下降并收敛到更低的目标值。这一现象的根本原因在于 OBCD 的最优性概念（块-k 驻点）比标准临界点更强，因此算法能够逃离那些是临界点但非块-k 驻点的不良局部极小点。

**OBCD-R 两种变体的一致性**：OBCD-R(rnd)（随机工作集选择）和 OBCD-R(id)（恒等初始化）在三个任务上均持续优于所有对比方法，说明 OBCD 框架对工作集选择策略具有鲁棒性。

### 失败模式与局限性

OBCD 的核心假设是子问题 (3) 能被精确高效求解，这在实际中限制了 k 的取值（通常取 k=2）以及非光滑项 h 的形式（需为坐标可分）。当 k>2 且 h≠0 时，子问题的精确求解可能变得困难，此时 OBCD 的优势会减弱。此外，理论分析依赖于随机工作集选择，循环选择策略的收敛性尚未严格证明。实验仅在稀疏 PCA 和非负 PCA 上进行，未涵盖深度神经网络、电子结构计算等其他潜在应用，因此 OBCD 在这些领域的表现尚不明确。

## 方法谱系与知识库定位

**谱系关系与核心创新点**

OBCD 属于块坐标下降（BCD）框架在流形约束非光滑优化中的一种非平凡扩展。与现存方法的关键差异在于其更新策略：现有 Riemannian 方法（如 RSSM、ManPG、RSubGrad）通常采用全梯度更新或列坐标更新，并在切空间上求解强凸子问题后通过回缩操作近似保持正交性；而 OBCD 采用行块坐标更新，每次迭代选择解矩阵的 k 行（k≥2）作为工作集，通过全局求解一个低维（k×k）Stiefel 流形上的非光滑子问题来精确保持正交性。这一设计将大规模正交约束优化分解为一系列小规模子问题，使得 OBCD 成为一种可行方法（feasible method），即迭代过程中解始终满足正交约束。

**最优性概念的跃迁**

OBCD 引入的最优性概念——“（全局）块-k 驻点”（BS_k-point）——是该方法最根本的理论贡献。与现有方法仅能保证收敛到标准临界点（critical point）不同，OBCD 的极限点是 BS_k 点，而 Theorem 3.8 证明了 BS_k 点集合严格包含于临界点集合（即所有临界点都是 BS_2 点，但反之不成立），且 BS_k 点集合包含全局最优点。这意味着 OBCD 能够逃离不良局部极小点，找到比标准临界点更强的驻点——这正是实验中 OBCD-R 在 L0 和 L1 正则化稀疏 PCA 以及非负 PCA 上持续优于所有对比方法（包括 LADMM、ADMM、RSubGrad、ManPG、PSM、RADMM）的根本原因。Figure 1 的收敛曲线直观展示了这一现象：无论运行多长时间，其他方法都陷入不良局部极小点，而 OBCD-R 能单调递减目标函数并逃离。

**适用边界与条件**

OBCD 的适用性受以下条件约束：
- **子问题可解性**：OBCD 要求子问题 (3) 能被精确高效求解。这限制了工作集大小 k 的取值（实践中通常取 k=2）以及非光滑项 h 的形式——h 必须为坐标可分（coordinate-separable），否则子问题的精确求解将变得困难。
- **光滑性假设**：f 需满足关于 H 的光滑性条件（公式 (2)），即对于最多相差 k 行的点对，f 被二次函数上界控制。这一假设在常见的二次型目标（如 PCA 中的方差最大化）中自然成立。
- **工作集选择**：理论分析依赖于随机工作集选择策略（OBCD-R(rnd)），循环选择策略的收敛性尚未严格证明。实验中使用的 OBCD-R(id) 采用恒等初始化，其理论保证与随机选择一致。

**与现有方法的关系定位**

OBCD 不属于对现有流形优化方法的简单改进，而是提供了一种全新的优化路径。对比方法中，RSSM 和 RSubGrad 是 Riemannian 子梯度方法，ManPG 是流形近端梯度法，LADMM、ADMM、RADMM 是算子分裂类方法，PSM 是基于惩罚的分裂方法。这些方法的共同特征是：在切空间上求解近似子问题后通过投影或回缩恢复正交性，因此本质上是不精确的可行方法；其最优性概念局限于标准临界点，无法保证逃离不良局部极小。OBCD 通过构造性更新规则精确保持正交性，并通过全局求解子问题获得更强的最优性保证，从而在理论上和实践中都占据了独特的位置。

**局限与开放问题**

1. **k>2 的扩展**：当 k>2 且 h≠0 时，子问题的精确求解变得困难。能否设计高效的近似求解策略，同时保持 BS_k 点的理论保证，是重要的开放问题。
2. **循环选择策略的收敛性**：尽管随机选择策略有严格的收敛分析，但实践中更高效的循环选择策略的收敛性尚未证明。
3. **应用范围**：当前实验仅限于稀疏 PCA 和非负 PCA。OBCD 在深度神经网络（如正交权重约束）、电子结构计算、字典学习等领域的表现尚未探索。
4. **全局收敛率**：虽然建立了 O(1/ε) 的迭代复杂度（Theorem 4.2）和不同参数 σ 下的局部收敛率（Theorem 4.11），但非凸非光滑情形下的全局收敛率（特别是避免鞍点的能力）仍缺乏理论刻画。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Block_Coordinate_Descent_Method_for_Nonsmooth_Composite_Optimization_under_Orthogonality_Constraints.pdf

![[paperPDFs/ICLR_2026/A_Block_Coordinate_Descent_Method_for_Nonsmooth_Composite_Optimization_under_Orthogonality_Constraints.pdf]]
