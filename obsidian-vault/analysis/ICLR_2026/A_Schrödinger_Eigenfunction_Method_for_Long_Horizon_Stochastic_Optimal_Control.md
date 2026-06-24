---
title: "A Schrödinger Eigenfunction Method for Long-Horizon Stochastic Optimal Control"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: "paperPDFs/ICLR_2026/A_Schrödinger_Eigenfunction_Method_for_Long_Horizon_Stochastic_Optimal_Control.pdf"
aliases:
- SDEMLHSEI
- SDEMLHSOC
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/physics
core_operator: "将HJB方程线性化后，利用算子L的离散谱展开，将长时域控制问题转化为学习薛定谔算子的基态本征函数及其梯度，从而将复杂度从O(Td)降至O(d)。"
primary_logic: "在梯度漂移假设下，线性化HJB算子L与薛定谔算子S = -Δ + V酉等价，后者具有纯离散谱；长时域最优控制由基态本征函数φ₀主导，高阶模态贡献随(T-t)指数衰减，因此仅需学习φ₀即可近似长时域控制。"
claims:
- "在梯度漂移假设下，算子L酉等价于具有纯离散谱的薛定谔算子S = -Δ + V"
- "长时域最优控制可近似为u*(x,t) = ∂_x log φ₀(x) + O(e^{-(λ₁-λ₀)(T-t)})"
- "提出的相对本征函数损失||Lψ/ψ - λ||²消除了隐式重加权，正确恢复控制所需的主导本征对"
- "在多个高维(d=20)长时域基准上，控制L²误差比现有方法提升约一个数量级"
---

# A Schrödinger Eigenfunction Method for Long-Horizon Stochastic Optimal Control

> [!tip] 核心洞察
> 在梯度漂移假设下，线性化HJB算子L与薛定谔算子S = -Δ + V酉等价，后者具有纯离散谱；长时域最优控制由基态本征函数φ₀主导，高阶模态贡献随(T-t)指数衰减，因此仅需学习φ₀即可近似长时域控制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种用于长时域随机最优控制的薛定谔本征函数方法 |
| 英文题名 | A Schrödinger Eigenfunction Method for Long-Horizon Stochastic Optimal Control |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=lcEw5NcSij) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/physics |
| Method | Schrödinger Eigenfunction Method for Long-Horizon SOC (EIGF+IDO) |
| Dataset | QUADRATIC (ISOTROPIC), QUADRATIC (REPULSIVE), QUADRATIC (ANISOTROPIC), DOUBLE WELL |

> [!tip] 效果简介
> - QUADRATIC (ISOTROPIC) 上，控制目标（越小越好） 为 32.7717 ± 0.014 (COMBINED SOCM)，对比 32.7870 ± 0.014 (IDO Relative entropy)，变化 -0.0153。
> - QUADRATIC (REPULSIVE) 上，控制目标（越小越好） 为 112.3444 ± 0.050 (COMBINED Relative entropy)，对比 112.5172 ± 0.051 (IDO Relative entropy)，变化 -0.1728。
> - QUADRATIC (ANISOTROPIC) 上，控制目标（越小越好） 为 31.3476 ± 0.016 (COMBINED Relative entropy)，对比 31.3664 ± 0.016 (IDO Log variance)，变化 -0.0188。

## 概述

本文针对长时域随机最优控制（SOC）中现有方法性能随规划时域T增长而急剧退化这一瓶颈，提出了一种基于薛定谔算子本征函数的方法。核心问题在于：传统方法（如FBSDE、IDO）的内存和运行时间至少线性增长于T，且重要性采样权重方差可能随T指数增长，导致高维长时域问题难以求解。

本文的核心洞察是：在梯度漂移假设（b = -∇E）下，通过Cole-Hopf变换线性化HJB方程后得到的算子L，酉等价于一个具有纯离散谱的薛定谔算子S = -Δ + V。这一等价性使得长时域最优控制由基态本征函数φ₀主导——高阶模态的贡献随谱隙(λ₁-λ₀)(T-t)指数衰减。因此，仅需学习φ₀及其对数梯度∂_x log φ₀，即可将时域复杂度从O(Td)降至O(d)。

方法定位上，本文提出了一套混合求解框架（EIGF+IDO）：首先通过引入的相对本征函数损失||Lψ/ψ - λ||²学习基态本征对，该损失消除了传统Deep Ritz或PINN损失中因隐式重加权导致的控制学习失败；随后在远终端时域（t ≤ T_cut）直接使用∂_x log φ₀作为控制，在近终端时域（t > T_cut）添加短时域IDO修正项。对于对称LQR情形，该方法甚至获得了任意终端成本的闭式解。

实验结果表明，在多个d=20的高维长时域基准问题（包括各向同性/各向异性/排斥型二次成本、双阱势、环形势）上，提出的方法在控制L²误差上比现有最优方法提升约一个数量级。例如，在DOUBLE WELL设置中，混合方法（COMBINED SOCM）的控制目标为32.4421 ± 0.0088，而最佳基线（IDO Log variance）为32.8645 ± 0.0094。消融实验验证了相对损失相对于绝对损失的显著优势、纯本征函数方法在近终端区域的退化以及混合方法的必要性。

## 背景与动机

长时域随机最优控制（SOC）问题在科学和工程中广泛存在，但其求解面临严重的计算瓶颈。现有方法——包括基于前向-后向随机微分方程（FBSDE）的深度求解器和迭代扩散优化（IDO）系列方法——在时间域 $T$ 增长时性能急剧下降：内存和运行时间至少线性增长于 $T$（复杂度 $O(Td)$），误差估计随 $T$ 增大而恶化（Han & Long, 2020, Theorem 4），重要性采样权重方差可能随 $T$ 指数增长（Liu et al., 2018）。如图 Figure 1 所示，现有方法在固定 $d$ 下随 $T$ 增大控制误差显著上升。

该问题的根源在于传统方法将控制参数化为全时域神经网络 $u_\theta(x,t)$，需同时处理整个时间区间 $[0,T]$。当 $T$ 增大时，网络需要拟合的时空复杂度线性增长，同时终端条件的影响通过时间反向传播传播，导致梯度信号衰减或爆炸。

本文的核心洞察在于：通过 Cole-Hopf 变换将 HJB 方程线性化后，得到的算子 $\mathcal{L}$ 在梯度漂移假设（$b = -\nabla E$）下酉等价于薛定谔算子 $S = -\Delta + \mathcal{V}$，后者具有纯离散谱。这一数学结构使得长时域最优控制可以仅由基态本征函数 $\phi_0$ 主导——高阶模态的贡献随谱隙 $(\lambda_1 - \lambda_0)$ 和剩余时间 $(T-t)$ 指数衰减，即 $u^*(x,t) = \partial_x \log \phi_0(x) + \mathcal{O}(e^{-(\lambda_1-\lambda_0)(T-t)})$。因此，当 $T-t$ 超过一个适度阈值（实验中 $T-t \geq 1$）时，仅用 $\phi_0$ 即可充分近似控制，将复杂度从 $O(Td)$ 降至 $O(d)$。

然而，直接学习本征函数面临现有损失函数的缺陷：Deep Ritz 损失和 PINN 损失 $\|\mathcal{L}\psi - \lambda\psi\|^2$ 隐式地重加权，导致在高价值函数区域学习失败（Figure 3 展示）。为此，本文提出相对本征函数损失 $\|\mathcal{L}\psi/\psi - \lambda\|^2$，消除重加权效应，正确恢复控制所需的主导本征对。

基于此，本文方法（EIGF+IDO）采用混合控制参数化：远终端时域（$t \leq T_{cut}$）仅用 $\partial_x \log \phi_0$，近终端时域（$t > T_{cut}$）添加指数衰减的短时域修正项 $e^{-(\lambda_1-\lambda_0)(T-t)/(2\beta)} v^{\theta_1}(x,t)$。这一设计在多个高维（$d=20$）长时域基准上实现控制 $L^2$ 误差比现有方法提升约一个数量级（Table 3, Table 4），同时为对称 LQR 问题提供了任意终端成本的闭式解析解（Theorem 4）。

## 核心创新

本文的核心创新在于将长时域随机最优控制问题的复杂度从 **O(Td)** 降低到 **O(d)**，即与时间域长度T无关。这一突破通过三个关键创新实现：**薛定谔算子酉等价**、**相对本征函数损失**和**混合控制参数化**。

### 1. 核心洞察：从HJB到薛定谔算子

现有方法（如FBSDE、IDO）在时域T增长时面临根本性瓶颈：内存和运行时间至少线性增长于T，且误差估计随T恶化，重要性采样权重方差可能随T指数增长。本文的核心洞察是：在**梯度漂移假设**下（b = -∇E），线性化HJB算子L与薛定谔算子S = -Δ + V酉等价，后者具有纯离散谱。这意味着长时域最优控制由基态本征函数φ₀主导，高阶模态贡献随谱隙指数衰减：

$$
u^*(x,t) = \partial_x \log \phi_0(x) + \mathcal{O}\left(e^{-(\lambda_1 - \lambda_0)(T-t)}\right)
$$

当T-t ≥ 1时，仅用φ₀即可充分近似控制。

### 2. 相对本征函数损失

现有本征函数学习方法（Deep Ritz损失、PINN损失||Lψ - λψ||²）存在隐式重加权问题：在高价值函数区域学习失败，因为损失被低价值函数区域主导。本文提出的**相对损失**：

$$
\mathcal{R}_{Rel}^\rho(\phi) = \left\|\frac{\mathcal{L}\phi}{\phi} - \lambda\right\|_\rho^2 + \alpha\mathcal{R}_{reg}^\rho(\phi)
$$

通过除以ψ消除了隐式加权，鲁棒地恢复控制合成所需的主导本征对。实验（RING设置）表明，相对损失在控制精度上显著优于Deep Ritz和PINN损失，后者在V₀大的区域完全失败。

### 3. 混合控制参数化

本文提出混合参数化，将远终端和近终端控制分离：

$$
u_\theta(x,t) = \begin{cases} 
\beta^{-1}\nabla\log\phi_0^{\theta_0} & 0 \leq t \leq T_{cut}, \\
\beta^{-1}\left(\nabla\log\phi_0^{\theta_0}(x) + e^{-\frac{1}{2\beta}(\lambda_1-\lambda_0)(T-t)}v^{\theta_1}(x,t)\right) & T_{cut} < t \leq T.
\end{cases}
$$

- **远终端**：仅用基态本征函数的对数梯度∂_x log φ₀，复杂度O(d)
- **近终端**：添加短时域修正项（由IDO/FBSDE学习），修正项随谱隙指数衰减

这种设计利用了本征函数方法在远离终端时的准确性和短时域求解器在近终端时的灵活性。实验（Figure 5）显示，纯本征函数方法在t < T_cut时表现优异，但接近终端T时误差增大；混合方法结合两者优势，获得最低总体L²误差。

### 4. 对称LQR的闭式解

对于对称线性漂移、二次运行成本的情形，薛定谔算子S与量子谐振子的哈密顿量匹配，从而得到任意终端成本的闭式本征系统（定理4）。本征函数和本征值分别为：

$$
\phi_\alpha(x) = \frac{\exp\left(-\frac{\beta}{2}x^T(-A + U^T\Lambda^{1/2}U)x\right)}{(\lambda\pi)^{d/4}} \prod_{i=1}^d \frac{\Lambda_{ii}^{1/8}}{\sqrt{2^{\alpha_i}(\alpha_i!)}} H_{\alpha_i}\left(\sqrt{\beta}(\Lambda^{1/4}Ux)_i\right)
$$

$$
\lambda_\alpha = \beta\left(-\mathsf{Tr}(A) + \sum_{i=1}^d \Lambda_{ii}^{1/2}(2\alpha_i + 1)\right)
$$

这一结果扩展了经典LQR的适用范围，使其能够处理任意终端成本。

### 5. 关键改变总结

| 改变槽 | 基线值 | 本文值 | 证据 |
|--------|--------|--------|------|
| 时域复杂度 | O(Td)（内存和运行时间随T线性增长） | O(d)（与T无关） | 实验验证 |
| 控制参数化 | 全时域神经网络u_θ(x,t) | 混合参数化：远终端仅用φ₀，近终端添加修正 | Figure 5 |
| 本征函数损失 | Deep Ritz/PINN损失，隐式重加权 | 相对损失||Lψ/ψ - λ||² | Figure 3, 4 |
| 终端成本假设 | 经典LQR要求二次型 | 对称LQR可处理任意终端成本 | 定理4 |

### 6. 实验验证

在多个高维（d=20）长时域基准上，本文方法（EIGF+IDO）的控制L²误差比现有方法提升约一个数量级。具体地：
- QUADRATIC (ISOTROPIC)：控制目标从32.7870降至32.7717
- DOUBLE WELL：控制目标从32.8645降至32.4421
- 相对损失在RING设置中显著优于绝对损失，后者控制学习完全失败

消融实验表明：增加本征函数数量在d=20 LQR中收益递减；仅用基态本征函数的遍历估计器（EIGF）随T增长误差降低，但混合方法（EIGF+IDO）显著更优。

## 整体框架

![[assets/figures/papers/iclr26_0003_lcEw5NcSij_A_Schrödinger_Eigenfunction_Method_for_Long-Hori/figures/013_Figure_9.jpg]]
*Figure 9: In this experiment EIGF method uses an ergodic estimator based only on the first eigenfunction. EIFG+IDO curve corresponds to the application of the proposed controller (22) with Relative Entropy loss. The figure shows L ^ { 2 } control error for different methods after 30000 iterations*

该方法的整体 pipeline 围绕一个核心洞察构建：在梯度漂移假设（b = -∇E）下，长时域随机最优控制的复杂度可以从 O(Td) 降至 O(d)。这一降维的关键在于将 HJB 方程线性化后得到的算子 L 酉等价于一个具有纯离散谱的薛定谔算子 S = -Δ + V，从而允许使用谱展开来求解控制问题。

**模块关系与输入输出流**：

1. **酉等价与谱验证模块**：输入为系统动力学参数（漂移 b、扩散 σ、运行成本 f、终端成本 g），输出为算子 L 的谱性质保证（纯离散谱）。该模块证明在梯度漂移假设下，L 与薛定谔算子 S 酉等价，为后续本征函数展开提供理论基础。这一步骤是理论保证，不涉及数值计算。

2. **本征函数学习模块**：输入为系统参数（β, f, b），输出为基态本征函数 φ₀ 及其对应的特征值 λ₀。该模块使用提出的**相对本征函数损失** $\mathcal{R}_{Rel}^\rho(\phi) = \left\| \frac{\mathcal{L}\phi}{\phi} - \lambda \right\|_\rho^2 + \alpha \mathcal{R}_{reg}^\rho(\phi)$ 来学习 φ₀。这一损失函数消除了现有方法（如 Deep Ritz 损失或 PINN 损失 $\|\mathcal{L}\phi - \lambda\phi\|^2$）中的隐式重加权问题，使得在高价值函数区域也能正确学习控制。实验证明（Figure 4, Figure 7），相对损失在 RING 设置中显著优于绝对损失，后者在 V₀ 大的区域完全失败。

3. **混合控制合成模块**：输入为 φ₀、λ₀、谱隙 (λ₁-λ₀) 以及现有短时域求解器（IDO 或 FBSDE），输出为完整时间域 [0,T] 上的最优控制 u_θ(x,t)。该模块采用**混合参数化**策略：
   - **远终端区域**（0 ≤ t ≤ T_cut）：仅使用基态本征函数的对数梯度 $u^*(x,t) \approx \beta^{-1}\nabla\log\phi_0(x)$，此时高阶模态贡献随 $e^{-(\lambda_1-\lambda_0)(T-t)}$ 指数衰减，误差可控。实验表明当 T-t ≥ 1 时，仅用 φ₀ 即可充分近似控制。
   - **近终端区域**（T_cut < t ≤ T）：添加短时域修正项 $v^{\theta_1}(x,t)$，其幅度由指数衰减因子 $e^{-\frac{1}{2\beta}(\lambda_1-\lambda_0)(T-t)}$ 控制。修正项使用现有 IDO 或 FBSDE 求解器学习。

**关键因果机制**：长时域控制的瓶颈在于现有方法（FBSDE、IDO 等）需要处理整个时间域 [0,T]，导致内存和运行时间线性增长于 T，且误差随 T 增大而恶化（Figure 1）。该方法通过谱分解将时间依赖转移到指数衰减因子 $e^{-\lambda_i \tau}$ 上，使得长时域行为由基态主导，从而将时域复杂度从 O(Td) 降至 O(d)。这一降维的代价是要求系统满足梯度漂移假设，且有效势能 V(x) → ∞ 当 ||x|| → ∞。

**证据强度**：理论部分（酉等价、谱离散性）有严格证明，置信度 1.0。实验部分（Figure 5, Table 3, Table 4）显示在多个 d=20 的高维长时域基准上，控制 L² 误差比现有方法提升约一个数量级。但需注意，T_cut 的选择缺乏先验方法，需根据谱隙和具体应用决定，这是一个需要手动验证的弱点。

## 核心模块与公式推导

### 问题形式化与线性化

考虑受控随机过程：

$$
\mathrm{d}X_t^u = (b(X_t^u) + \sigma u(X_t^u,t))\mathrm{d}t + \sqrt{\beta^{-1}}\sigma \mathrm{d}W_t, \quad X_0^u \sim p_0
$$

其中 $u(x,t)$ 为控制，$\beta>0$ 为逆温度参数。最小化的成本泛函为：

$$
J(u;x,t) = \mathbb{E}\left[\int_t^T \left(\frac{1}{2}\|u(X_t^u,t)\|^2 + f(X_t^u)\right)\mathrm{d}t + g(X_T^u) \Bigg| X_t = x\right]
$$

值函数 $V(x,t) = \min_u J(u;x,t)$ 满足 Hamilton-Jacobi-Bellman (HJB) 方程：

$$
\partial_t V + \mathcal{K}V = 0 \quad \text{in } \mathbb{R}^d \times [0,T], \quad V(\cdot,T) = g \quad \text{on } \mathbb{R}^d
$$

通过 Hopf-Cole 变换 $V(x,t) = -\beta^{-1}\log\psi(x, \frac{1}{2\beta}(T-t))$，将非线性 HJB 方程线性化为：

$$
\partial_\tau \psi + \mathcal{L}\psi = 0, \quad \psi(\cdot,0) = \psi_0, \quad \text{where } \mathcal{L}\psi = -\mathsf{Tr}(\sigma\sigma^T\nabla^2\psi) - 2\beta b^T\nabla\psi + 2\beta^2 f\cdot\psi, \quad \psi_0 = \exp(-\beta g)
$$

其中 $\tau = (2\beta)^{-1}(T-t)$。最优控制可通过 $\psi$ 的对数梯度恢复：$u^*(x,t) = \partial_x \log \psi(x,\tau)$。

### 算子谱理论与薛定谔等价

核心理论突破在于：在**梯度漂移假设** $b = -\nabla E$ 下，算子 $\mathcal{L}$ 酉等价于薛定谔算子，从而具备纯离散谱。具体地，$\mathcal{L}$ 在 $L^2(\mu)$ 上的形式为：

$$
\mathcal{L}\psi = -\Delta\psi + 2\beta\langle\nabla E, \nabla\psi\rangle + 2\beta^2 f\psi
$$

通过酉变换 $U: \psi \mapsto e^{-\beta E}\psi$，得到：

$$
U\mathcal{L}U^{-1} = -\Delta + \beta^2\|\nabla E\|^2 - \beta\Delta E + 2\beta^2 f
$$

记有效势能 $\mathcal{V} = \beta^2\|\nabla E\|^2 - \beta\Delta E + 2\beta^2 f$，则薛定谔算子为 $S = -\Delta + \mathcal{V}$。当 $\mathcal{V}(x) \to \infty$ 随 $\|x\|\to\infty$ 时，$S$ 具有紧预解子和纯离散谱（Reed & Simon, 1978, Theorem XIII.67, XIII.64, XIII.47）。

### 本征函数展开与长时域近似

设 $\{(\lambda_i, \phi_i)\}_{i\in\mathbb{N}}$ 为算子 $\mathcal{L}$ 的本征对，满足 $\mathcal{L}\phi_i = \lambda_i \phi_i$，$\lambda_0 < \lambda_1 \leq \lambda_2 \leq \cdots$。线性 PDE 的解可展开为：

$$
\psi(\tau) = \sum_{i\in\mathbb{N}} e^{-\lambda_i\tau} \langle\phi_i, \psi_0\rangle \phi_i
$$

当 $\tau = (2\beta)^{-1}(T-t)$ 较大时（即远离终端时间 $T$），高阶模态 $i \geq 1$ 的贡献随谱隙 $(\lambda_1 - \lambda_0)$ 指数衰减：

$$
u^*(x,t) = \partial_x \log \phi_0(x) + \mathcal{O}\left(e^{-(\lambda_1 - \lambda_0)(T-t)}\right)
$$

该公式是方法的核心：**长时域最优控制由基态本征函数的对数梯度主导**，且误差随 $(T-t)$ 增大而指数衰减。实验表明，当 $T-t \geq 1$ 时，仅用 $\phi_0$ 即可充分近似控制。

### 对称 LQR 的闭式解

对于对称线性-二次型调节器（LQR），即 $b(x) = -Ax$（$A$ 对称正定）、$f(x) = \frac{1}{2}x^T Q x$（$Q$ 对称正定），薛定谔算子退化为量子谐振子哈密顿量。设 $A = U^T \Lambda U$ 为特征分解，则本征函数为：

$$
\phi_\alpha(x) = \frac{\exp\left(-\frac{\beta}{2}x^T(-A + U^T\Lambda^{1/2}U)x\right)}{(\lambda\pi)^{d/4}} \prod_{i=1}^d \frac{\Lambda_{ii}^{1/8}}{\sqrt{2^{\alpha_i}(\alpha_i!)}} H_{\alpha_i}\left(\sqrt{\beta}(\Lambda^{1/4}Ux)_i\right)
$$

对应的本征值为：

$$
\lambda_\alpha = \beta\left(-\mathsf{Tr}(A) + \sum_{i=1}^d \Lambda_{ii}^{1/2}(2\alpha_i + 1)\right)
$$

其中 $H_{\alpha_i}$ 为 Hermite 多项式，$\alpha = (\alpha_1,\ldots,\alpha_d)$ 为多重指标。该闭式解适用于**任意终端成本** $g$，突破了经典 LQR 对二次型终端成本的限制。

### 相对本征函数损失

现有方法（Deep Ritz、PINN）使用绝对损失 $\|\mathcal{L}\phi - \lambda\phi\|_\rho^2$，该损失在 $\phi$ 值较大的区域隐式赋予更高权重，导致在高价值函数区域学习失败。为此提出**相对本征函数损失**：

$$
\mathcal{R}_{Rel}^\rho(\phi) = \left\|\frac{\mathcal{L}\phi}{\phi} - \lambda\right\|_\rho^2 + \alpha\mathcal{R}_{reg}^\rho(\phi)
$$

该损失消除了 $\phi$ 的隐式重加权，使网络在所有区域均匀学习，正确恢复控制所需的基态本征对。实验表明，在 RING 设置中，相对损失显著优于 Deep Ritz 和 PINN 损失，而绝对损失完全无法学习正确控制。

### 混合控制参数化

结合本征函数方法（远终端）与现有短时域求解器（近终端），提出混合控制：

$$
u_\theta(x,t) = \begin{cases} 
\beta^{-1}\nabla\log\phi_0^{\theta_0} & 0 \leq t \leq T_{cut}, \\
\beta^{-1}\left(\nabla\log\phi_0^{\theta_0}(x) + e^{-\frac{1}{2\beta}(\lambda_1-\lambda_0)(T-t)}v^{\theta_1}(x,t)\right) & T_{cut} < t \leq T.
\end{cases}
$$

其中 $T_{cut}$ 为截止时间（实验中取 $T_{cut} = T-1$），$v^{\theta_1}$ 由短时域 IDO/FBSDE 求解器学习。该参数化将复杂度从 $O(Td)$ 降至 $O(d)$，同时通过指数衰减因子 $e^{-(\lambda_1-\lambda_0)(T-t)}$ 平滑衔接两个区域。

## 实验与分析

### 主结果：控制目标与L²误差

本文在多个高维（d=20）长时域随机最优控制基准上评估了所提方法，核心指标为控制目标（越小越好）和控制L²误差。所有方法使用相同神经网络架构，训练迭代统一为30k次（本征函数预训练80k次），控制目标通过N=65536次蒙特卡洛模拟估计。

**定量结果（控制目标）**：在QUADRATIC (ISOTROPIC)设置中，EIGF+IDO混合方法（COMBINED SOCM）达到32.7717±0.014，优于最佳基线IDO Relative entropy的32.7870±0.014，改进幅度-0.0153。在QUADRATIC (REPULSIVE)设置中，COMBINED Relative entropy达到112.3444±0.050，优于IDO Relative entropy的112.5172±0.051，改进-0.1728。值得注意的是，SOCM方法在该设置中未收敛，动力学发散。在QUADRATIC (ANISOTROPIC)中，COMBINED Relative entropy达到31.3476±0.016，优于IDO Log variance的31.3664±0.016。在DOUBLE WELL设置中，COMBINED SOCM达到32.4421±0.0088，显著优于IDO Log variance的32.8645±0.0094，改进幅度达-0.4224。

**控制L²误差**：在多个基准上，混合方法实现了比现有方法约一个数量级的L²误差改进。这一改进在Figure 5中可视化呈现：上排显示L²误差随迭代的指数移动平均，混合方法（EIGF+IDO）始终低于纯IDO或纯EIGF方法；下排显示L²误差随时间t∈[0,T]的变化，纯EIGF方法在t < T_cut时表现优异，但接近终端T时误差显著增大，而混合方法通过切换至短时域修正项保持了低误差。

**本征函数数量影响**：Figure 2显示，在d=20 LQR中，增加本征函数数量的收益递减——仅用基态本征函数φ₀即可获得大部分改进，这与理论预测一致（高阶模态贡献随谱隙指数衰减）。当T-t ≥ 1时，仅用φ₀即可充分近似控制。

### 消融研究：损失函数与混合策略

**相对本征函数损失 vs 绝对损失**：这是方法的核心消融。在RING设置（d=2）中，相对损失||Lψ/ψ - λ||²正确恢复了控制所需的主导本征对，而Deep Ritz损失和PINN损失（||Lψ - λψ||²）在高价值函数区域学习失败。Figure 3直观展示了这一差异：现有方法在V₀大的区域控制箭头方向错误。Figure 4进一步量化了不同损失函数下∇log φ₀的L²误差，相对损失在所有设置中显著优于绝对损失。

**混合方法 vs 纯本征函数方法**：Figure 5底部行揭示了关键模式：纯EIGF方法在远离终端时（t < T_cut）L²误差极低，但在接近T时误差急剧上升。混合方法（EIGF+IDO）结合了两者优势——远终端使用∂_x log φ₀的闭式近似，近终端切换至短时域IDO求解器添加修正项——从而在整个时域保持低误差。Figure 9进一步验证了这一结论：在T增长时，纯EIGF方法的遍历估计器误差降低，但混合方法始终显著更优。

**本征函数数量消融**：Figure 2显示，从1个增加到2个本征函数时改进明显，但继续增加时收益迅速递减，支持了仅需基态近似即可的理论主张。

### 失败模式与公平性说明

**SOCM收敛失败**：在QUADRATIC (REPULSIVE)设置中，SOCM方法未收敛导致动力学发散（Table 3），表明该方法对势能函数类型敏感。


![[assets/figures/papers/iclr26_0003_lcEw5NcSij_A_Schrödinger_Eigenfunction_Method_for_Long-Hori/figures/014_Table_3.jpg]]
*Table 3: Control objective for the different methods in the QUADRATIC (ISOTROPIC) and QUADRATIC (REPULSIVE) settings. The SOCM method did not converge, and hence the dynamics diverge*

**纯本征函数方法的终端退化**：纯EIGF方法在接近终端时误差增大（Figure 5），这是理论预期的——当T-t不足以使高阶模态衰减时，仅用基态近似的O(e^{-(λ₁-λ₀)(T-t)})误差不可忽略。这要求T_cut的合理选择，目前缺乏先验方法。

**计算成本差异**：Table 2报告了不同方法的迭代时间，但未对总计算时间进行公平性校正。本征函数方法因需要计算网络对输入的导数（要求GELU等平滑激活函数），单次迭代成本可能高于IDO方法。


![[assets/figures/papers/iclr26_0003_lcEw5NcSij_A_Schrödinger_Eigenfunction_Method_for_Long-Hori/figures/008_Table_2.jpg]]
*Table 2: Iteration times by method and loss*

**公平性说明**：所有方法使用相同神经网络架构（IDO方法使用ReLU激活的简化U-Net，本征函数方法使用GELU激活以保证导数平滑性）。训练迭代次数统一，但本征函数预训练需要额外80k次迭代。控制目标通过N=65536次蒙特卡洛模拟估计，报告均值±标准误差。

### 补充图表

![[assets/figures/papers/iclr26_0003_lcEw5NcSij_A_Schrödinger_Eigenfunction_Method_for_Long-Hori/figures/005_Table_1.jpg]]
*Table 1: Opinion dynamics, final control objective (smaller is better)*

![[assets/figures/papers/iclr26_0003_lcEw5NcSij_A_Schrödinger_Eigenfunction_Method_for_Long-Hori/figures/015_Table_4.jpg]]
*Table 4: Control objective for the different methods in the QUADRATIC (ANISOTROPIC) and DOUBLE WELL settings*


## 方法谱系与知识库定位

### 与现有方法的关系

本文提出的薛定谔本征函数方法（EIGF+IDO）直接针对现有长时域随机最优控制（SOC）方法的根本瓶颈：当时域 $T$ 增长时，内存和运行时间至少线性增长于 $T$（复杂度 $O(Td)$），且误差估计随 $T$ 增大而恶化（Han & Long, 2020, Theorem 4），重要性采样权重方差可能随 $T$ 指数增长（Liu et al., 2018）。图1直观展示了现有方法（FBSDE、IDO变体）随 $T$ 增大性能退化的趋势。

本文的方法论创新在于将HJB方程线性化后，利用算子 $\mathcal{L}$ 的离散谱展开，将长时域控制问题转化为学习薛定谔算子的基态本征函数及其梯度，从而将复杂度从 $O(Td)$ 降至 $O(d)$。这一思路与现有方法形成鲜明对比：
- **FBSDE**：基于前向-后向随机微分方程的深度求解器，需处理整个时域 $[0,T]$。
- **IDO（Iterative Diffusion Optimization）**：包括相对熵损失、对数方差损失、SOCM损失、伴随匹配损失等多种变体，同样需全时域参数化。
- **EIGF+IDO（本文）**：采用混合参数化——在 $t \leq T_{\text{cut}}$ 时仅用 $\partial_x \log \phi_0$，在 $t > T_{\text{cut}}$ 时添加短时域修正项 $e^{-(\lambda_1-\lambda_0)(T-t)/(2\beta)} v^{\theta_1}(x,t)$，从而将大部分时域的控制计算简化为与 $T$ 无关的本征函数梯度。

### 核心改进与证据

本文的 decisive evidence 包括四个关键环节：

1. **酉等价与谱保证**：证明在梯度漂移假设（$b = -\nabla E$）下，算子 $\mathcal{L}$ 酉等价于薛定谔算子 $S = -\Delta + V$，后者具有纯离散谱。这一理论保证是后续所有方法的基础。

2. **本征函数主导性**：证明最优控制可近似为 $u^*(x,t) = \partial_x \log \phi_0(x) + O(e^{-(\lambda_1-\lambda_0)(T-t)})$，即高阶模态贡献随谱隙指数衰减。实验表明，当 $T-t \geq 1$ 时，仅用基态本征函数 $\phi_0$ 即可充分近似控制。

3. **相对本征函数损失**：引入损失 $\|\mathcal{L}\psi/\psi - \lambda\|^2_\rho$，消除传统Deep Ritz或PINN损失（$\|\mathcal{L}\psi - \lambda\psi\|^2$）的隐式重加权问题。图3展示：现有损失函数在高价值函数区域 $V_0$ 学习失败，而相对损失正确恢复控制。图4在RING设置中进一步验证了这一改进。

4. **实验验证**：在多个高维（$d=20$）长时域基准上，控制 $L^2$ 误差比现有方法提升约一个数量级。具体地：
   - QUADRATIC (ISOTROPIC)：控制目标从32.7870降至32.7717（COMBINED SOCM）
   - QUADRATIC (REPULSIVE)：从112.5172降至112.3444（COMBINED Relative entropy）
   - DOUBLE WELL：从32.8645降至32.4421（COMBINED SOCM）

### 适用边界

本方法的适用性受以下条件约束：
- **梯度漂移假设**：要求漂移 $b = -\nabla E$，限制了非保守力场或非梯度漂移系统的应用。
- **势能增长条件**：需要有效势能 $V(x) \to \infty$ 当 $\|x\| \to \infty$，以保证纯离散谱，排除周期势等情形。
- **终端成本假设**：理论保证依赖于条件(69)，即终端成本 $g$ 相对于基态 $\phi_0$ 和能量 $E$ 的比值有界（$m \leq \exp(-\beta g) / (\exp(\beta E(x)) \phi_0) \leq M$）。
- **时间无关系数**：方法目前仅处理时间无关的漂移和噪声系数。
- **平滑激活函数**：本征函数学习需计算网络对输入的导数，要求使用平滑激活函数（如GELU而非ReLU），可能增加计算成本。

### 局限与开放问题

**已知局限**：
- 截止时间 $T_{\text{cut}}$ 的选择缺乏先验方法，需根据应用和谱隙 $\lambda_1 - \lambda_0$ 决定。实验中使用 $T_{\text{cut}} = T - 1$，但这不是通用准则。
- 纯本征函数方法（EIGF）在 $t < T_{\text{cut}}$ 时表现优异，但接近终端 $T$ 时误差增大（图5底部行）。混合方法（EIGF+IDO）虽能结合两者优势，但增加了方法复杂度。
- 增加本征函数数量在 $d=20$ LQR中收益递减（图2），说明仅需基态即可获得主要性能提升。
- SOCM方法在QUADRATIC (REPULSIVE)设置中未收敛，导致动力学发散（Table 3），说明某些IDO变体在特定问题上可能失效。

**开放问题**：
1. 如何自动确定最优截止时间 $T_{\text{cut}}$？这可能需要根据谱隙 $\lambda_1 - \lambda_0$ 和期望误差容限进行自适应估计。
2. 能否将方法扩展到非梯度漂移或时间相关系数？这可能需要寻找其他酉等价变换或放弃纯离散谱假设。
3. 条件(69)（终端成本与基态之比有界）在实际问题中如何验证或放松？当终端成本 $g$ 在低概率区域取值极端时，该条件可能被违反。
4. 当谱隙 $\lambda_1 - \lambda_0$ 很小时，仅用基态近似的误差会增大。如何处理此类问题？可能需要学习多个本征函数或采用其他近似策略。
5. 能否将方法扩展到多个本征函数以处理更小的谱隙？附录C.2给出了PINN和变分损失的多本征函数扩展，但实验表明收益递减，需要更高效的多模态学习策略。

**公平性说明**：所有方法使用相同神经网络架构（IDO方法使用ReLU激活的简化U-Net，本征函数方法使用GELU激活），训练迭代次数统一为30k次（除本征函数预训练80k次外）。控制目标通过 $N=65536$ 次蒙特卡洛模拟估计。但迭代时间因方法而异（Table 2），未对总计算时间进行公平性校正。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Schrödinger_Eigenfunction_Method_for_Long_Horizon_Stochastic_Optimal_Control.pdf

![[paperPDFs/ICLR_2026/A_Schrödinger_Eigenfunction_Method_for_Long_Horizon_Stochastic_Optimal_Control.pdf]]
