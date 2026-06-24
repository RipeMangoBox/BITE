---
title: "Fast training of accurate physics-informed neural networks without gradient descent"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Fast_training_of_accurate_physics_informed_neural_networks_without_gradient_descent.pdf
openreview_forum_id: 3VdSuh3sie
aliases:
- FP
- FTAPINNWGD
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "采用时空分离方法：冻结空间基函数（通过 ELM 或 SWIM 随机采样），解耦损失函数各分量，并将 PDE 转化为常微分方程，通过最小二乘和自适应 ODE 求解器计算时间相关系数，从而消除梯度下降并强制时间因果性。"
primary_logic: "核心洞见在于利用随机特征和时空分离，将 PDE 求解从困难的多目标优化问题转化为一个可高效求解的 ODE 问题，既大幅加快了训练速度，又自然引入了时间因果性。"
claims:
- "Frozen-PINN 通过冻结随机空间基函数降低了参数维数"
- "Frozen-PINN 通过解耦损失并分别优化，简化了优化问题"
- "时间相关的输出层参数通过最小二乘和自适应 ODE 求解器计算，完全替代了梯度下降"
- "Frozen-PINN 在多个 PDE 基准上实现了数量级的训练加速和精度提升"
---

# Fast training of accurate physics-informed neural networks without gradient descent

> [!tip] 核心洞察
> 核心洞见在于利用随机特征和时空分离，将 PDE 求解从困难的多目标优化问题转化为一个可高效求解的 ODE 问题，既大幅加快了训练速度，又自然引入了时间因果性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 无需梯度下降的快速高精度物理信息神经网络训练 |
| 英文题名 | Fast training of accurate physics-informed neural networks without gradient descent |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=3VdSuh3sie) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Frozen-PINN |
| Dataset | 线性对流方程 (β=40), 波动方程（多尺度）, 10 维热传导方程 |

> [!tip] 效果简介
> - 线性对流方程 (β=40) 上，相对 L² 误差 为 1e-4，对比 PINN 阶 O(1)，变化 提升超过 6 个数量级。
> - 波动方程（多尺度） 上，训练时间加速比 为 0.94s (CPU)，对比 GPU-trained PINN 625–5500× 更慢，变化 625–5500 倍。
> - 10 维热传导方程 上，相对 L² 误差 为 4.35e-4，对比 PINN (LBFGS) 3.98e-4 (但训练慢 100–1000 倍)，变化 训练加速 100–1000 倍。

## 概述

物理信息神经网络（PINN）将偏微分方程（PDE）的物理约束嵌入神经网络的损失函数中，提供了一种无需网格的 PDE 求解范式。然而，标准 PINN 的训练面临根本性困难：损失函数是高维、多目标且非凸的，同时将时间视为额外的空间维度破坏了物理系统的因果结构，使得基于梯度下降的优化极易陷入局部极小或收敛缓慢。

**Frozen-PINN** 针对这一瓶颈提出了一种完全摒弃梯度下降的训练框架。其核心机制是**时空分离**：通过 ELM 或 SWIM 随机采样并冻结空间基函数，将 PDE 求解从困难的多目标优化问题转化为一个常微分方程（ODE）问题。时间相关的输出层系数通过最小二乘拟合初始条件，并由自适应 ODE 求解器直接演化，从而在根本上消除了梯度下降，并自然引入了时间因果性。

该方法在多个 PDE 基准上实现了数量级的训练加速与精度提升：
- 对于线性对流方程（β=40），相对 L² 误差达到 1e-4 量级，较标准 PINN 提升超过 6 个数量级；
- 对于波动方程，CPU 训练仅需 0.94 秒，比 GPU 训练的 PINN 变体快 625–5500 倍；
- 对于 10 维热传导方程，在精度相当的前提下训练加速 100–1000 倍。

Frozen-PINN 的方法定位处于**随机特征方法**（ELM/SWIM）与**自适应 ODE 求解器**的交叉点，通过解耦损失函数各分量（PDE 残差、初始条件、边界条件），将 PINN 的训练重新定义为一系列可独立、高效求解的子问题。这一框架为时间依赖 PDE 的快速高精度求解开辟了新的技术路径。

## 背景与动机

### 物理信息神经网络的核心瓶颈

物理信息神经网络（PINN）通过将物理定律以偏微分方程（PDE）残差的形式嵌入神经网络的损失函数，实现了在无标签数据条件下求解正问题和逆问题。然而，标准 PINN 的训练面临一个根本性瓶颈：其损失函数是 PDE 残差、初始条件、边界条件和数据项的高维加权组合，构成一个多目标、高度非凸的优化问题。更关键的是，PINN 将时间视为一个额外的空间维度，在整个时空域内同时最小化残差，这从根本上违背了物理系统的时间因果性——未来的状态不应影响过去的演化。

这种设计导致了两个严重后果。其一，基于梯度下降的优化器（如 Adam 和 L-BFGS）在如此复杂的损失景观中极易陷入局部极小值或收敛停滞，训练过程耗时极长且结果不可靠。其二，因果性的缺失使得 PINN 在处理高频解、混沌系统或长时间演化问题时表现尤为糟糕，误差会随时间累积并迅速发散。

### 现有改进的局限性

针对上述问题，研究者提出了多种改进方案。**Causal PINN**（Wang et al., 2024d）通过为每个时间步分配基于累积损失的权重，以软约束的形式引入时间因果性。然而，这并未从根本上改变优化问题的结构——它仍然依赖梯度下降在一个耦合的损失函数上迭代搜索，训练效率的提升有限，且在处理高对流速度等极端场景时依然失效。

从方法学角度看，这些改进都未触及 PINN 训练困难的核心矛盾：将 PDE 求解表述为一个通用的非凸优化问题，然后用通用的梯度优化器去求解。这种方法忽略了时间依赖 PDE 的内在结构——空间和时间维度在物理上具有本质不同的角色，可以也应该被区别对待。

### 本文动机：从优化问题到 ODE 问题

本文的核心动机在于一个根本性的视角转换：**能否完全绕过梯度下降，将 PINN 的训练从一个困难的优化问题转化为一个可高效求解的常微分方程（ODE）问题？**

这一转换的关键在于时空分离。如果能够将空间依赖的基函数预先确定并冻结，那么 PDE 的求解就简化为寻找一组时间依赖的系数，使其满足 PDE 约束。此时，PDE 残差不再是一个关于所有网络参数的非凸函数，而是一个关于时间系数的 ODE 系统。这个 ODE 系统可以通过成熟的自适应求解器高效求解，既天然保证了时间因果性（系数沿时间方向逐步演化），又彻底消除了梯度下降带来的训练困难。

这一思路在概念上简洁而有力，但其实现面临若干技术挑战：如何采样合适的空间基函数以提供足够的表示能力？如何处理不同类型的边界条件？如何控制 ODE 系统的规模以避免刚性或维度灾难？Frozen-PINN 正是围绕这些问题展开的系统性解决方案。

## 核心创新

Frozen-PINN 的核心创新在于从根本上重构了 PINN 的训练范式：**将高维、多目标、非凸的耦合优化问题转化为一个可高效求解的常微分方程（ODE）初值问题**，从而完全消除了对梯度下降的依赖，并自然地引入了时间因果性。

### 创新一：时空分离与空间基函数冻结

标准 PINN 将时间视为额外的空间维度，在整个时空域上联合采样配点并训练网络。这导致优化问题维度极高，且缺乏时间因果性——未来时刻的残差会影响过去时刻的预测。Frozen-PINN 采用**时空分离**策略，将近似解参数化为：

$$\hat{u}(x,t) = C(t)[\Phi(x), \mathbb{1}] = c(t)\sigma(W x^\top + b) + c_0(t)$$

其中空间基函数 $\Phi(x)$ 的隐藏层参数 $W, b$ 通过 **ELM**（Huang et al., 2006）或 **SWIM**（Bolager et al., 2023）随机采样后**冻结**，仅保留时间依赖的输出层系数 $C(t)$ 作为可训练参数。这一设计的直接效果是**大幅降低了参数空间的维度**：标准 PINN 需要优化 $O(M \cdot d)$ 个参数（$M$ 为隐藏层宽度，$d$ 为空间维度），而 Frozen-PINN 仅需优化 $O(M)$ 个时间相关系数。

### 创新二：损失函数完全解耦

标准 PINN 将 PDE 残差、初始条件残差和边界条件残差耦合在单一损失函数中，通过加权求和进行联合优化，权重调谐困难且各目标相互干扰。Frozen-PINN 将三者**完全解耦**：

- **初始条件**：通过最小二乘法直接求解 $C(0) = u(X,0)^\top [\Phi(X), \mathbb{1}]^+$，一步到位满足初始条件。
- **边界条件**：通过**边界兼容层**（满足边界条件构造的基函数变换）或**增广 ODE**（在边界配点上添加约束项 $-\kappa (C(t)\Phi_A(X_b) - g(X_b)^\top)$）单独处理。
- **PDE 残差**：ODE 求解器仅需最小化 PDE 残差，避免了多目标冲突。

这一解耦使得各约束条件被精确满足，而非在优化中折衷妥协。

### 创新三：梯度下降的完全替代——ODE 演化

这是 Frozen-PINN 最根本的改变。将冻结后的网络近似解代入 PDE，可将 PDE 残差转化为输出系数 $C(t)$ 的 ODE：

$$C_t(t) = R(X, C(t))[\Phi(X), \mathbb{1}]^+$$

其中 $[\Phi(X), \mathbb{1}]^+$ 为伪逆。这意味着**不再需要反向传播和基于梯度的优化器**（如 Adam、L-BFGS），而是直接使用自适应 ODE 求解器（如 RK45、LSODA）从初始条件 $C(0)$ 开始演化 $C(t)$。这一设计同时带来了两个关键优势：

1. **训练速度数量级提升**：ODE 求解器具有步长自适应能力，且仅需在时间方向推进，避免了梯度下降的大规模迭代。
2. **时间因果性的自然引入**：ODE 求解器从前一时刻的状态计算下一时刻，天然保证了信息只从过去流向未来，解决了标准 PINN 中未来信息泄露的问题。

### 方法谱系与知识库定位

Frozen-PINN 处于 PINN（Raissi et al., 2019）与随机特征方法（ELM, SWIM）的交叉点，但其训练机制与两者均本质不同：

| 方法 | 空间基函数 | 时间系数计算 | 损失耦合 |
|------|-----------|-------------|---------|
| 标准 PINN | 梯度下降联合学习 | 梯度下降联合学习 | 单损失联合优化 |
| Causal PINN (Wang et al., 2024d) | 梯度下降联合学习 | 梯度下降 + 因果权重 | 加权耦合 |
| **Frozen-PINN** | **随机采样后冻结** | **最小二乘 + ODE 求解器** | **完全解耦** |

与 Causal PINN 通过软约束权重施加时间因果性不同，Frozen-PINN 通过 ODE 演化**硬编码**了时间因果性。与 ELM 仅用于静态函数逼近不同，Frozen-PINN 将随机特征扩展到了时间依赖 PDE 的动态演化框架中。

### 辅助创新：SVD 层与维度压缩

为进一步降低 ODE 系统的刚性和计算代价，Frozen-PINN 在空间基函数后引入可选的 **SVD 层**：对 $\mathcal{A}\Phi(X)$ 进行截断 SVD，将基函数维度从 $M$ 压缩至 $r \ll M$，同时通过正交化改善 ODE 的数值稳定性。消融实验表明，SVD 层可将计算速度提升**高达 75 倍**，ODE 系统维度降低 **20 倍**，且对精度影响可控。

## 整体框架

Frozen-PINN 的核心设计在于将时间依赖偏微分方程的求解从高维非凸优化问题转化为一个常微分方程初值问题。其整体 pipeline 由五个顺序衔接的模块构成，输入为 PDE 定义、初始/边界条件及空间配点集，输出为全时空近似解。

### Pipeline 模块关系与数据流

**1. 空间基函数随机采样（ELM/SWIM）**
首先构建单隐层神经网络近似解：
$$
\hat{u}(x,t) = C(t)[\Phi(x), \mathbb{1}] = c(t)\sigma(W x^\top + b) + c_0(t)
$$
其中 $\sigma = \tanh$，隐层参数 $W, b$ 通过 ELM（数据无关随机采样）或 SWIM（数据驱动的随机特征方法）一次性采样并冻结。SWIM 能将基函数定向放置于解梯度陡峭的区域（如激波附近），而 ELM 无法控制基函数位置。冻结空间参数是降低参数空间维度的关键操作。

**2. 边界兼容层或增广 ODE**
边界条件通过两种策略之一单独处理，实现损失函数完全解耦：
- **边界兼容层**：构造满足边界条件的基函数 $\Phi_A(x)$，使边界条件由构造保证，ODE 求解器仅需最小化 PDE 残差。
- **增广 ODE**：对 Dirichlet 边界 $u(x)=g(x), x\in\partial\Omega$，在 ODE 系统中添加修正项 $-\kappa(\hat{u}(x)-g(x))$，形成增广系统强制边界满足。

**3. SVD 层**
对算子作用后的基函数矩阵进行截断 SVD：
$$
V_r \Sigma_r U_r^\top = \mathcal{A}\Phi(X)
$$
输出降维后的神经基函数 $\mathtt{b}_{A_r}(X) = (A_r\Phi(X), 1)^\top \in \mathbb{R}^{(r+1)\times N_c}$。该层可降低 ODE 刚性、将系统维度压缩高达 20 倍，并将计算速度提升达 75 倍。

**4. 最小二乘初始化**
通过最小二乘解计算输出层系数的初始值：
$$
C(0) = u(X,0)^\top \Phi_{A_r}(X)^+
$$
此步骤将初始条件损失与 PDE 损失完全解耦。

**5. 自适应 ODE 求解器**
将 PDE 残差通过伪逆转化为输出系数 $C(t)$ 的 ODE：
$$
C_t(t) = R(X, C(t)) \Phi_A(X)^+
$$
使用带步长控制的自适应求解器（如 RK45、LSODA）直接演化系数，完全替代梯度下降。

### 核心设计逻辑

整个框架的关键在于**时空分离**与**损失解耦**：空间基函数冻结后，时间依赖性完全由输出层系数 $C(t)$ 承载，PDE 被转化为关于 $C(t)$ 的 ODE。初始条件通过最小二乘单独满足，边界条件通过边界兼容层或增广 ODE 单独处理，使得 ODE 求解器仅需最小化 PDE 残差。这一设计不仅消除了梯度下降带来的训练困难，还自然引入了时间因果性——$C(t)$ 的演化严格遵循时间顺序。

> **注意**：关于网络参数重采样在克服 Kolmogorov n-宽度障碍中的作用，以及具体 PDE 设置下的普遍逼近性质，目前尚缺乏理论证明，需要进一步研究。

## 核心模块与公式推导

### 问题形式化

Frozen-PINN 针对以下通用时间依赖 PDE 设计：

$$u_t(x,t) + \mathscr{L} u(x,t) + \gamma \mathscr{N}(u)(x,t) = f(x)$$

其中 $\mathscr{L}$ 为线性微分算子，$\mathscr{N}$ 为非线性算子，$\gamma$ 控制非线性强度，$f(x)$ 为源项。初始条件 $u(x,0) = u_0(x)$ 和边界条件 $u(x,t) = g(x,t), x \in \partial\Omega$ 共同构成定解条件。

### 核心模块：时空分离与冻结基函数

Frozen-PINN 的核心架构是将解近似为空间基函数与时间相关系数的乘积：

$$\hat{u}(x,t) = C(t)[\Phi(x), \mathbb{1}] = c(t)\sigma(W x^\top + b) + c_0(t)$$

其中 $\sigma = \tanh$，$W \in \mathbb{R}^{M \times d}$ 和 $b \in \mathbb{R}^M$ 为隐藏层参数，$c(t) \in \mathbb{R}^{1 \times M}$ 和 $c_0(t) \in \mathbb{R}$ 为时间依赖的输出层系数。**关键操作**：$W$ 和 $b$ 通过 ELM 或 SWIM 采样后冻结，不再参与任何基于梯度的优化。这使得参数空间从 $O(Md)$ 降至 $O(M)$，且空间基函数 $\Phi(x)$ 完全独立于时间变量，天然实现了时空分离。

### 核心模块：PDE 到 ODE 的转化

将上述 ansatz 代入 PDE，利用冻结基函数在配点 $X = \{x_i\}_{i=1}^{N_c}$ 处的取值 $\Phi(X)$，可将 PDE 残差 $R(X, C(t))$ 转化为关于 $C(t)$ 的常微分方程：

$$C_t(t) = R(X, C(t))[\Phi(X), \mathbb{1}]^+$$

其中 $[\Phi(X), \mathbb{1}]^+$ 表示增广基函数矩阵的 Moore-Penrose 伪逆。这一转化将原本需要联合优化空间和时间参数的非凸多目标问题，简化为仅需沿时间方向积分的 ODE 初值问题。

### 核心模块：损失解耦与边界处理

Frozen-PINN 将标准 PINN 的联合损失函数彻底解耦为三个独立处理的部分：

1. **初始条件**：通过最小二乘直接计算 $C(0) = u(X,0)^\top [\Phi(X), \mathbb{1}]^+$，而非通过梯度下降拟合。
2. **边界条件**：通过两种策略处理——
   - **边界兼容层**：构造满足边界条件的基函数 $\Phi_A(x)$，使得 $\hat{u}(x,t) = C(t)\Phi_A(x)$ 自动满足边界条件，此时 ODE 简化为 $C_t(t) = R(X, C(t))\Phi_A(X)^+$。
   - **增广 ODE**：对于 Dirichlet 边界 $u(x) = g(x)$，在边界配点 $X_b$ 上添加修正项，求解增广系统：
     $$C_t(t) = [R(X, C(t)), -\kappa (C(t)\Phi_A(X_b) - g(X_b)^\top)] \Phi_A([X, X_b])^+$$
     其中 $\kappa$ 控制边界约束强度。
3. **PDE 残差**：ODE 求解器在时间推进过程中仅需最小化 PDE 残差，不再与初始条件和边界条件耦合。

### 核心模块：SVD 降维层

为降低 ODE 系统的维度和刚性，Frozen-PINN 引入 SVD 层对基函数进行正交化压缩。对算子 $\mathcal{A}$ 作用于基函数的结果进行截断 SVD：

$$V_r \Sigma_r U_r^\top = \mathcal{A}\Phi(X)$$

保留前 $r$ 个奇异值对应的分量，构造降维后的神经基函数 $\mathtt{b}_{A_r}(X) = (A_r\Phi(X), 1)^\top \in \mathbb{R}^{(r+1) \times N_c}$。消融实验表明，SVD 层可将计算速度提升高达 75 倍，并将 ODE 系统维度降低约 20 倍，同时保持解精度。

### 训练流程

Frozen-PINN 的完整训练算法（见 Algorithm 1）可概括为：采样并冻结空间基函数 → 构造边界兼容基函数 → SVD 截断降维 → 最小二乘初始化 $C(0)$ → 调用自适应 ODE 求解器（如 RK45、LSODA）沿时间推进 $C(t)$。整个流程无需任何反向传播或梯度下降迭代，训练时间由 ODE 求解器的步长控制决定。

## 实验与分析

### 核心性能表现

Frozen-PINN 在八个时间依赖 PDE 基准上展现了数量级的训练加速与精度提升。Table 1 汇总了主要结果：对于高对流速度的对流方程（β=40），Frozen-PINN 在低精度区间以 45–533 倍的训练加速实现了约 1e-4 的相对 L² 误差，而标准 PINN 的误差在 O(1) 量级（提升超过 6 个数量级）。对于多尺度波动方程，CPU 训练的 Frozen-PINN 仅需 0.94 秒，比 GPU 训练的 PINN 变体快 625–5500 倍。在 10 维热传导方程上，Frozen-PINN-elm 达到 4.35e-4 的相对 L² 误差，训练速度比 PINN（L-BFGS）快 100–1000 倍，且精度相当。

Figure 4 进一步揭示了对流方程上的三个关键特性：左图表明 Frozen-PINN 在高对流速度（β 高达 10000）下仍保持低误差，而 PINN 和 Causal PINN 的误差随 β 增大急剧恶化；中图显示 Frozen-PINN 的测试误差随网络宽度（基函数数量）增加呈指数衰减，而标准 PINN 的误差衰减趋于平缓；右图验证了长时间仿真能力——在 1000 秒的仿真中，Frozen-PINN 的相对 L² 误差保持在 0.001% 以下。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of experimental results for the advection equation: (Left): high advection speeds - effect of advection coefficient β on the test error for different PDE solvers, (Middle): fast convergence - with $\beta$ = 1 0 , Frozen PINNs achieve exponential decay in test error as indicated by the reference dotted line, while standard PINNs display plateaued error decay despite increasing number of basis functions (hidden layer size), (Right): long time simulation - Slow error growth with time*

对于强非线性混沌系统 Kuramoto-Sivashinsky 方程，Frozen-PINN 成功捕捉了复杂的时空动力学行为（Figure 6），证明了该方法在高度非线性问题上的适用性。

### 高维问题扩展性

Figure 7 展示了 Frozen-PINN 在高维热传导方程上的表现。在维度从 1 到 100 的测试中，Frozen-PINN-elm 的精度始终比经典 PINN 高 10–1000 倍。对于 100 维热方程，CPU 训练的 Frozen-PINN 达到 2.28e-5 的相对 L² 误差，同时训练速度比 GPU 训练的 PINN 快数百倍。误差随网络宽度的衰减曲线（Figure 7 底部）表明，Frozen-PINN 的误差随宽度增加快速下降直至饱和，而 PINN 的误差衰减则早早进入平台期。

### 消融实验

**SVD 层的作用。** SVD 层通过正交化基函数降低 ODE 系统的刚性和维度。Figure 10 的消融实验表明，适中的 SVD 截断阈值可将计算速度提升高达 75 倍，并将 ODE 系统维度降低约 20 倍。过大的截断阈值（即保留过少奇异值）会导致非线性扩散方程的解发散（图中黑色三角标记），揭示了基函数信息保留与数值稳定性之间的权衡。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/012_Figure_10.jpg]]
*Figure 10: Impact of the SVD truncation threshold $\epsilon _ { S V D }$ used for the SVD layer on the time-tosolution and accuracy of Frozen-PINN across three PDEs. Black triangles in the nonlinear diffusion plot indicate solution blow-up at large SVD cutoffs*

**初始条件拟合精度。** 对于对流方程，初始条件的最小二乘拟合精度直接影响全时空解的精度。Figure 9 显示，全时空解的相对误差与初始条件拟合的相对误差呈正相关，验证了解耦策略中初始条件精确满足的重要性。

**基函数选择的影响。** SWIM 基函数在处理激波时显著优于傅里叶和切比雪夫谱方法（Figure 22, Figure 23）。SWIM 通过数据驱动的方式在激波附近放置具有陡峭梯度的基函数，而 ELM 的数据无关采样缺乏这种控制能力（Figure 2）。此外，SWIM 通过将空间坐标投影到初始解的梯度方向，嵌入了方向信息，使其基函数与问题的内在变化维度对齐。

### 公平性说明

实验中的公平性考量包括：在相等精度下进行基准测试，划分低精度和高精度区间分别比较；对于涉及 FEM 的对比，FEM 网格点被复用为 Frozen-PINN 的配点以最小化 PDE 残差，确保计算资源可比。

### 已知局限

尽管 Frozen-PINN 在实验中表现优异，但其理论分析尚存空白：尚未从理论上证明该方法在具体 PDE 设置下的普遍逼近性质，网络参数重采样在克服 Kolmogorov n-宽度障碍方面的作用也尚不明确。这些开放问题为后续理论研究指明了方向。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/008_Table_2.jpg]]
*Table 2: Comparison of Frozen-PINNs with mesh-based FEM and classical PINNs in different problem settings presented in this paper: The comparison is grounded in results reported in Section 3 for the PDEs and solvers studied. ✓ denotes compatibility, and ✗ denotes either incompatibility or the need for substantial modifications. Curse of Dimensionality is abbreviated as CoD. Figure 7: High-dimensional heat equation: (Top): comparison of test errors for varying PDE dimensions (different hatch patterns indicate different benchmarks), (Bottom): fast decay of test error with network width (dashed: Frozen-PINN-swim, solid: Frozen-PINN-elm)*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/010_Figure_8.jpg]]
*Figure 8: Comparison of Frozen-PINNs (bottom row) that leverage a gradient-descent-free training algorithm, with conventional PINNs (top row) that rely on gradient-based iterative optimization: conventional PINNs use basis functions in the entire spatio-temporal domain and solve a fully coupled optimization problem involving multiple loss terms via gradient-based iterative training. In contrast, Frozen-PINNs sample basis functions only in space, make time dependence explicit only in the output layer, decouple initial/boundary conditions, and leverage least squares and adaptive ODE solvers. Parameters dependent on space, time, and both are indicated by blue, orange, and blue-orange colors, respectivel...*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/013_Figure_11.jpg]]
*Figure 11: Examples of B-Splines representing the 1D domain [0, 1]. Number of nodes = 6 and degree of polynomials = 2. (Left): The original B-Splines. (Middle): Adapted B-Splines to satisfy the Dirichlet boundary condition. (Right): Adapted B-Splines to satisfy the periodic boundary condition. Note that the first (blue) spline is identical to the second last (brown) one, and the second (orange) spline is identical to the last (pink) one, as they share the same coefficient. The gray dashed lines indicate where the domain starts and ends*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/015_Figure.jpg]]
*Figure: (a) Frozen-PINN-swim*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/026_Figure.jpg]]
*Figure: (a) Frozen-PINN-swim (b) Frozen-PINN-elm (c) IGA*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/027_Figure.jpg]]
*Figure: (d) PINN (LBFGS) (e) PINN (Adam) (f) Ground truth*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/029_Figure_17.jpg]]
*Figure 17: The Euler-Bernoulli beam equation on Winkler foundation: absolute error plots and ground truth*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/033_Figure_18.jpg]]
*Figure 18: Wave equation Equation (27e): Ground truth, Frozen-PINN-swim solution, absolute error*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/034_Figure.jpg]]
*Figure: (a) (Left): Ground truth, (Middle): Frozen-PINN-swim solution, (Right): point-wise absolute error*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_3VdSuh3sie/figures/037_Figure_20.jpg]]
*Figure 20: (b) (Left): Ground truth, (Middle): Frozen-PINN-swim solution, where black and gray dashed lines mark time snapshots selected for a comparison (in (d) on the right) and the collocation points resampling times, respectively, (Right): point-wise absolute error. (c) Comparison between Frozen-PINN-swim and numerical solutions at three time instances. Figure 20: Illustration of experimental results for the Burgers’ equation*

## 方法谱系与知识库定位

### 1. 与标准 PINN 及其变体的关系

Frozen-PINN 直接回应了标准物理信息神经网络（**PINN**, Raissi et al., 2019）的核心训练瓶颈：其损失函数的高维、多目标和非凸性质，以及将时间视为额外空间维度所导致的因果性缺失，使得基于梯度下降的优化极其困难。Frozen-PINN 通过两条根本性路径切断了这一瓶颈的因果链条：

1. **空间基函数冻结**：标准 PINN 通过梯度下降（如 L-BFGS 或 Adam）迭代更新整个网络的权重，包括空间和时间参数。Frozen-PINN 则采用 **ELM**（Huang et al., 2006）或 **SWIM**（Bolager et al., 2023）随机采样空间层权重并冻结，使空间基函数独立于时间，从而将参数维数大幅降低。这本质上将神经网络从“可训练的通用函数逼近器”重新定位为“具有随机固定基函数的时空分离表示”。

2. **梯度下降的完全替代**：标准 PINN 的时间依赖系数通过反向传播和基于梯度的优化器联合学习；Frozen-PINN 则通过最小二乘拟合初始条件，随后利用自适应 ODE 求解器（如 RK45、LSODA）直接演化时间相关系数。损失函数被完全解耦——初始条件通过最小二乘单独满足，边界条件通过边界兼容层或增广 ODE 单独处理，ODE 求解器仅需最小化 PDE 残差。这从根本上消除了梯度下降的需求，并自然强制了时间因果性。

与 **Causal PINN**（Wang et al., 2024d）的对比尤为关键：Causal PINN 试图在梯度下降框架内通过软约束引入时间因果性，但仍受限于优化的困难；Frozen-PINN 则通过 ODE 求解器在构造层面保证了因果性，无需任何软约束技巧。

### 2. 与网格方法（FEM/IGA-FEM）的关系

Frozen-PINN 与经典有限元法（FEM）和等几何分析有限元法（**IGA-FEM**, Hughes et al., 2005）构成了互补关系，而非直接替代。在低维 PDE 上，IGA-FEM 作为精确基准；Frozen-PINN 的优势在于：

- **无网格特性**：无需网格生成，可直接处理高维问题（如 100 维热传导方程），而 FEM 在高维下遭遇维度灾难。
- **训练效率**：在非线性扩散方程上，Frozen-PINN 比 FEM 快约 4.83 倍（低精度区间），同时比标准 PINN 快 145–456 倍。
- **公平性设计**：为公平比较，FEM 的网格点被复用为 Frozen-PINN 的配点，确保两者在相同的空间离散点上评估 PDE 残差。

### 3. 随机特征方法的谱系定位

Frozen-PINN 的空间基函数采样策略植根于随机特征方法谱系：

- **ELM**（Huang et al., 2006）：数据无关采样，权重和偏置从固定分布中随机抽取，无需数据驱动。在 Frozen-PINN 中，ELM 基函数适用于无激波或弱非线性的 PDE 场景。
- **SWIM**（Bolager et al., 2023）：数据相关采样，利用解的梯度信息将基函数自适应地放置在激波或陡峭梯度区域。Frozen-PINN-swim 在处理对流方程的高 β 值（β=40）和 Burgers 方程的激波时，显著优于 ELM、傅里叶和切比雪夫谱方法（Figure 22, Figure 23）。

Frozen-PINN 的创新在于将这些原本用于静态函数逼近的随机特征方法，通过时空分离框架动态化为 PDE 求解的基函数生成器。

### 4. 关键模块的消融证据

- **SVD 层**：正交化基函数可将 ODE 求解速度提升高达 75 倍，并将 ODE 系统维度降低 20 倍（Figure 10）。SVD 截断阈值 ε_SVD 的选择直接影响精度-效率权衡：过大的阈值导致解爆炸（非线性扩散方程中的黑色三角标记）。
- **网络宽度**：Frozen-PINN 的误差随网络宽度增加呈指数衰减，而标准 PINN 的误差衰减趋于平缓（Figure 4 Middle, Figure 7 bottom），表明随机基函数在充分宽度下可逼近最优表示。
- **初始条件拟合精度**：对于对流方程，初始条件的最小二乘拟合精度直接影响全时空解精度（Figure 9），验证了损失解耦策略中初始条件独立处理的关键性。

### 5. 适用边界与局限

**适用边界**：
- Frozen-PINN 适用于可表示为 $u_t(x,t) + \mathscr{L} u(x,t) + \gamma \mathscr{N}(u)(x,t) = f(x)$ 形式的时间依赖 PDE，覆盖线性/非线性、低维/高维、对流/扩散/波动/混沌等多种类型。
- 在八个 PDE 基准上（Table 1），包括对流方程（β=1 到 40）、波动方程（多尺度）、Burgers 方程、非线性扩散方程、Kuramoto-Sivashinsky 方程（强非线性混沌）、以及高达 100 维的热传导方程，均实现了数量级的训练加速（最高 5500 倍）和精度提升。

**局限**：
1. **理论缺口**：尚未从理论上证明 Frozen-PINN 在具体 PDE 设置下的普遍逼近性质。虽然实验展示了指数收敛，但缺乏类似标准 PINN 的一致性定理或误差界分析。
2. **Kolmogorov n-宽度障碍**：网络参数重采样在克服 Kolmogorov n-宽度障碍方面的作用尚不明确。对于某些 PDE（如高频振荡或强激波传播），固定基函数可能无法有效捕捉解的动态演化，需要进一步研究重采样策略的理论基础。
3. **边界条件处理**：边界兼容层和增广 ODE 策略目前主要针对 Dirichlet 边界条件进行验证；对于更复杂的 Robin 边界或混合边界条件，方法的通用性需进一步确认。

### 6. 开放问题

1. **普遍逼近性质的理论研究**：针对具体 PDE 设置（如非线性算子的 Lipschitz 条件、初边值的光滑性），建立 Frozen-PINN 的误差收敛理论。
2. **网络参数重采样的作用机制**：理解随机基函数重采样如何克服 Kolmogorov n-宽度障碍，以及最优重采样频率和策略的设计。
3. **扩展到稳态 PDE 和逆问题**：当前框架聚焦于时间依赖的正问题；能否将时空分离思想推广到稳态 PDE 或参数反演问题，尚待探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/Fast_training_of_accurate_physics_informed_neural_networks_without_gradient_descent.pdf]]
