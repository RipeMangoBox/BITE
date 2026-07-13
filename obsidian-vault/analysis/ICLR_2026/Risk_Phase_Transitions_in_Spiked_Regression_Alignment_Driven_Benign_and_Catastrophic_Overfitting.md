---
title: "Risk Phase Transitions in Spiked Regression: Alignment Driven Benign and Catastrophic Overfitting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Risk_Phase_Transitions_in_Spiked_Regression_Alignment_Driven_Benign_and_Catastrophic_Overfitting.pdf
project_link: null
code_link: null
aliases:
- MNIO
- RPTSRADBCO
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/theory
core_operator: "该理论分析最小范数插值在线性尖峰协方差回归中的渐近泛化风险分解。"
primary_logic: "数据模型分离尖峰和体噪声分量，再在比例极限下解析偏置、方差、噪声和目标对齐贡献。"
claims:
- "目标与尖峰方向对齐并不总是改善泛化，其效果依赖尖峰强度、过参数化比例和误设定。"
- "在算子范数标度下，对齐可随尖峰强度从温和风险转入灾难性再转入良性过拟合。"
- "合成实验、三层ReLU网络和MNIST衍生实验支持理论相变预测。"
---

# Risk Phase Transitions in Spiked Regression: Alignment Driven Benign and Catastrophic Overfitting

> [!tip] 核心洞察
> 在尖峰协方差线性回归中，泛化误差由偏置、方差、数据噪声和目标对齐四项精确分解控制。尖峰强度与对齐的相互作用可导致非单调相变：在良设定对齐问题中，增大尖峰强度会先引发灾难性过拟合，然后才进入良性过拟合；目标-尖峰对齐并非总是有利，其利弊取决于尖峰强度是否超过关键阈值以及模型是否误设定。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 尖峰回归中的风险相变：由对齐驱动的良性与灾难性过拟合 |
| 英文题名 | Risk Phase Transitions in Spiked Regression: Alignment Driven Benign and Catastrophic Overfitting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=fFG4wZee3f) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/theory |
| Method | 最小范数插值（Minimum-Norm Interpolating OLS） |
| Dataset | 合成数据（尖峰协方差线性回归） |

> [!tip] 效果简介
> - 合成数据（尖峰协方差线性回归） 上，渐近超额风险 R_c 为 良设定、算子范数标度、对齐、γ=ω_c(c²)：R_c → 0（良性），对比 良设定、算子范数标度、对齐、γ=Θ_c(1)：R_c → 正常数（温和），变化 从温和变为良性。
> - 合成数据（尖峰协方差线性回归） 上，渐近超额风险 R_c 为 良设定、算子范数标度、对齐、ω_c(1) ≤ γ ≤ o_c(c²)：R_c → ∞（灾难性），对比 良设定、算子范数标度、对齐、γ=Θ_c(1)：R_c → 正常数（温和），变化 从温和变为灾难性。
> - 合成数据（尖峰协方差线性回归） 上，渐近超额风险 R_c 为 良设定、Frobenius 范数标度、对齐、β*∥u：R_c → 0（良性），对比 良设定、Frobenius 范数标度、反对齐：R_c → α²τ²(‖β*‖² - (β*ᵀu)²) > 0（温和），变化 从温和变为良性。

## 概要

本文系统分析了尖峰协方差线性回归中最小范数插值解的泛化误差，揭示了尖峰强度、目标-尖峰对齐、模型误设定和协变量偏移对泛化误差的联合影响。核心贡献在于：在比例极限 d/n → c 和后续 c → ∞ 的框架下，完整刻画了良性、温和与灾难性过拟合的相变图景。研究发现，目标-尖峰对齐并非总是有利，其利弊取决于尖峰强度是否超过关键阈值以及模型是否误设定。在良设定对齐问题中，增大尖峰强度会先引发灾难性过拟合，然后才进入良性过拟合。实验验证表明，这些理论预测的相变在非线性深度网络（3层ReLU网络）中仍然存在。



现代机器学习中，过参数化模型（参数数量远多于样本数量）能够完美拟合训练数据，同时仍具有良好的泛化能力，这一现象被称为“良性过拟合”（benign overfitting）。然而，在某些条件下，过参数化模型也可能表现出“灾难性过拟合”（catastrophic overfitting），即泛化误差趋于无穷大。现有理论（Hastie et al., 2022; Bartlett et al., 2020; Mallinar et al., 2022）主要关注各向同性协方差或固定尖峰强度下的回归问题，无法系统刻画尖峰强度、目标-尖峰对齐、模型误设定和协变量偏移对泛化误差的联合影响，尤其是在过参数化极端区域（c → ∞）中良性、温和与灾难性过拟合的完整相变图景。

本文通过引入尖峰协方差数据模型和分离尖峰/体噪声依赖的目标生成模型，填补了这一理论空白。



## 核心方法与创新机理

1. **精确风险分解**：将泛化误差分解为偏置（Bias）、方差（Variance）、数据噪声（Data Noise）和目标对齐（Target Alignment）四项（Theorem 5），为理解各因素贡献提供了可解释框架。

2. **对齐利弊的相变发现**：挑战了“目标-尖峰对齐总是有利”的传统认知，证明对齐的利弊取决于尖峰强度标度、过参数化程度 c 和模型误设定程度 α_Z/α_A。

3. **完整过拟合分类**：基于尖峰强度 γ、过参数化比 c 和目标对齐 (β_*^⊤ u)²，给出了良性、温和与灾难性过拟合的完整分类（Table 1）。

4. **非线性模型验证**：在3层ReLU网络和MNIST衍生数据上验证了理论预测的相变，表明结果具有更广泛的适用性。



![[assets/figures/papers/iclr26_0002_fFG4wZee3f_Risk_Phase_Transitions_in_Spiked_Regression_Alig/figures/003_Figure_1.jpg]]
*Figure 1: (a) Operator norm scaling ( $\theta ^ { 2 }$ = c $\tau ^ { 2 }$ ) . Alignment initially improves generalization, but have catastrophic risk as c $\to \infty$ , . Anti-alignment yields tempered risk.

论文的整体框架由四个核心模块组成：

- **数据生成模块**：生成尖峰协方差数据 X = Z + A 和目标 y，其中 Z 为秩一尖峰信号，A 为各向同性体噪声。
- **估计器模块**：计算最小范数插值解 β_int = X^† y。
- **风险分解模块**：将泛化误差分解为偏置、方差、数据噪声和目标对齐四项。
- **渐近分析模块**：在比例极限 d/n → c 下计算各项的期望和方差，然后取 c → ∞ 得到过拟合分类。



### 5.1 数据模型

**信号模型**（Assumption 1）：
$$Z = \theta \mathbf{u} \mathbf{v}^\top$$
秩一尖峰信号，强度 θ，方向 u，随机系数 v。

**目标生成模型**（Equation 2）：
$$y_i = \alpha_Z \mathbf{z}_i^\top \beta_* + \alpha_A \mathbf{a}_i^\top \beta_* + \varepsilon_i$$
目标 y 由尖峰分量 z、体噪声分量 a 和噪声 ε 生成，系数 α_Z 和 α_A 控制对尖峰和体噪声的依赖。当 α_Z ≠ α_A 时，引入模型误设定。

### 5.2 估计器与风险

**最小范数插值估计器**（Equation 3）：
$$\beta_{\text{int}} = X^\dagger \mathbf{y}$$

**泛化风险**（Equation 4）：
$$\mathcal{R}(\beta_{\text{int}}) = \mathbb{E}\left[ (\tilde{y} - \tilde{\mathbf{x}}^\top \beta_{\text{int}})^2 \right]$$

### 5.3 良设定情况下的渐近超额风险

**Theorem 1** 给出了良设定尖峰回归下的渐近超额风险。

**算子范数标度**（θ² = γτ², c > 1）：
$$\mathcal{R}_c = \alpha^2 \tau^2 \left(1-\frac{1}{c}\right) \left( \|\beta_*\|^2 + \frac{\gamma c^2 - 2\gamma c - \gamma^2}{(\gamma+c)^2} (\beta_*^\top u)^2 \right) + \tau_\varepsilon^2 \frac{1}{c-1}$$

**Frobenius 范数标度**（θ² = dτ², c > 1）：
$$\mathcal{R}_{c>1} = \alpha^2 \tau^2 \left(1-\frac{1}{c}\right) \left( \|\beta_*\|^2 - (\beta_*^\top u)^2 \right) + \tau_\varepsilon^2 \frac{1}{c-1}$$

### 5.4 对齐有利的条件

**良设定、算子范数标度**：对齐有利当且仅当 γ > c(c-2)。当 γ = c 时，对齐在 1 < c < 3 有利，c > 3 有害。

**良设定、Frobenius 范数标度**：对齐总是有利的（c > 1）。

**误设定、无协变量偏移、算子范数标度**：对齐有利的区域随 c 增大而缩小（若 γ = o_c(c²)），或趋于 0 ≤ α_Z/α_A ≤ 2（若 γ = ω_c(c²)）。

**误设定、无协变量偏移、Frobenius 范数标度**：对齐有利的区域是 1/c ≤ α_Z/α_A ≤ 2 - 1/c，且随 c 扩大。

### 5.5 过拟合分类

**Table 1** 总结了基于尖峰标度、目标对齐和误设定的渐近过拟合分类：

| 设定 | 标度 | 对齐条件 | 过拟合类型 |
|------|------|----------|------------|
| 良设定 | 算子范数 | γ = Θ_c(1) | 温和 |
| 良设定 | 算子范数 | ω_c(1) ≤ γ ≤ o_c(c²), β_* ∥ u | 灾难性 |
| 良设定 | 算子范数 | γ = ω_c(c²), β_* ∥ u, ‖β_*‖=1 | 良性 |
| 良设定 | Frobenius 范数 | β_* ∥ u, ‖β_*‖=1 | 良性 |
| 良设定 | Frobenius 范数 | β_* ∦ u | 温和 |
| 误设定、无协变量偏移 | 算子范数 | 任何条件 | 良性：永不发生 |
| 误设定、无协变量偏移 | 算子范数 | ω_c(1) ≤ γ ≤ o_c(c²), β_* ∦ u | 灾难性 |
| 误设定、无协变量偏移 | Frobenius 范数 | 1/c < α_Z/α_A < 2 - 1/c | 对齐有利 |



## 实验与关键发现

### 6.1 合成数据实验

**Figure 1** 展示了良设定下超额风险 vs. c 的曲线：
- (a) 算子范数标度（θ² = cτ²）：对齐初始改善泛化，但随 c → ∞ 导致灾难性过拟合；反对齐产生温和风险。
- (b) Frobenius 范数标度（θ² = dτ²）：对齐导致良性过拟合，反对齐产生温和风险。

![[assets/figures/papers/iclr26_0002_fFG4wZee3f_Risk_Phase_Transitions_in_Spiked_Regression_Alig/figures/004_Figure_1.jpg]]
*Figure 1: (b) Equal Frobenius norm scaling ( $\theta ^ { 2 }$ = d $\tau ^ { 2 }$ ) . Alignment leads to benign overfitting, while anti-alignment results in tempered risk. Figure 1: Excess error vs. overparameterization ratio c = d / n in the well-specified case. Each plot shows the risk for aligned and anti-aligned targets under different spike scaling regimes. The scatter plots are empirically obtained and the lines are theory.

**Figure 2** 展示了轻度误设定下从有利到有害对齐的转变：
- (a) 算子范数标度（α_Z=1, α_A=2）：对齐初始改善泛化，但超过临界点后变得有害，导致灾难性过拟合。
- (b) Frobenius 范数标度（α_A=1, α_Z=1.1）：对齐始终优于反对齐，但除非 α_Z=α_A，否则无法实现良性过拟合。

**Figure 3** 展示了尖峰对齐影响的相边界：
- (a) 算子范数标度，c=2：大的有利区域。
- (b) 算子范数标度，c=20：较小的有利区域。
- (c) Frobenius 范数标度，c=1000：有利区域在极端过参数化下持续存在。

![[assets/figures/papers/iclr26_0002_fFG4wZee3f_Risk_Phase_Transitions_in_Spiked_Regression_Alig/figures/005_Figure_3.jpg]]
*Figure 3: (a) Under operator norm scaling ( $\theta ^ { 2 }$ \ : = \ : c $\tau ^ { 2 }$ ) with $\alpha _ { Z }$ = 1 , $\alpha _ { A }$ = 2 , alignment initially improves generalization for small c, but becomes harmful beyond a critical point, leading to catastrophic overfitting.

### 6.2 非线性模型实验

**Figure 4** 展示了3层ReLU网络中泛化误差 vs. 对齐角度的曲线：
- α_Z=0.1：对齐有利。
- α_Z=1：混合行为。
- α_Z=4：对齐有害。

这验证了理论预测的相变：对齐的效果随 α_Z 增加而切换。

**Figure 5** 展示了MNIST衍生数据上深度网络的泛化误差 vs. 对齐角度，对 (α_Z, α_a) ∈ {1,4}² 进行扫描，进一步验证了理论在真实数据上的适用性。

### 6.3 消融实验

- **岭正则化**（Figure 6）：即使使用岭正则化，灾难性过拟合仍然存在。
- **协变量偏移**（Section 3.3）：在误设定、有协变量偏移、Frobenius 范数标度下，若 α_Z ≠ α̃_Z，则对所有 c≠1 有 R_c = ∞。若训练误设定但测试良设定且 α_Z = α̃_Z = α̃_A，则可实现良性过拟合。

### 补充图表

![[assets/figures/papers/iclr26_0002_fFG4wZee3f_Risk_Phase_Transitions_in_Spiked_Regression_Alig/figures/001_Table_1.jpg]]
*Table 1: Asymptotic Generalization Regimes. This table summarizes conditions for when overfitting is benign, tempered, or catastrophic in the limit where d / n c and subsequently c $\to \infty$ The behavior depends on the spike scaling relative to the bulk, target alignment ( $\beta$ ; ∗ relative to spike direction u), and target specifications $\alpha _ { A } , \alpha _ { Z }$ (train) and $\tilde { \alpha } _ { A } , \tilde { \alpha } _ { Z } \mathrm { ( t e s t ) }$ . Here, $\theta ^ { 2 }$ quantifies the scaled spike strength and $\bar { \tau ^ { 2 } }$ the scaled bulk variance; the two primary scaling regimes are operator norm based ( $\theta ^ { 2 } = \gamma \tau ^ { 2 }$ ) and Frobenius norm based...

![[assets/figures/papers/iclr26_0002_fFG4wZee3f_Risk_Phase_Transitions_in_Spiked_Regression_Alig/figures/002_Table_2.jpg]]
*Table 2: Conditions for Beneficial Spike Alignment at Finite Aspect Ratios ( c = d / n ) . . This table outlines the specific regions where alignment of the target signal with the data’s principal spike direction improves generalization. Conditions depend on the problem setting (well-specified vs. mis-specified), the spike scaling regime (operator or frobenius norm based), the overparameterization level c = d / n , and the relative dependence of the targets y on the spike versus the bulk $\alpha _ { Z } / \alpha _ { A }$ ·

![[assets/figures/papers/iclr26_0002_fFG4wZee3f_Risk_Phase_Transitions_in_Spiked_Regression_Alig/figures/017_Table_3.jpg]]
*Table 3: Glossary of recurrent parameters and symbols. All Θ(1) constants are independent of n , d .*



## 定位与知识库关联

本文的方法谱系定位如下：

- **基础模型**：尖峰协方差线性回归，扩展了 Hastie et al. (2022) 的各向同性回归（θ=0, α_Z=0 时退化为各向同性模型）和 Sonthalia and Nadakuditi (2023) 的尖峰恢复模型（τ²=1/d, τ_ε²=0, α_A=0 时的尖峰恢复）。
- **过拟合分类框架**：基于 Bartlett et al. (2020) 和 Mallinar et al. (2022) 的良性、温和、灾难性过拟合分类。
- **理论工具**：使用随机矩阵理论（Marchenko-Pastur 律）、混合球面超收缩性（mixed spherical hypercontractivity）和 Sherman-Morrison 型伪逆展开（Meyer, 1973）进行渐近分析。

**局限性**：
- 理论分析限于线性回归的最小范数插值解，未扩展到非线性模型或正则化方法（除岭回归初步结果外）。
- 数据模型假设尖峰为秩一结构，未考虑多尖峰或更一般的低秩结构。
- 实验验证限于合成数据和 MNIST 衍生数据，未在更大规模真实数据集上验证。

**开放问题**：
- 如何将分析扩展到多尖峰或一般低秩协方差结构？
- 岭正则化或其他正则化方法如何改变相边界？
- 在非线性模型（如深度网络）中，理论预测的相变是否严格成立，还是仅作为近似？



## 原文 PDF

![[paperPDFs/ICLR_2026/Risk_Phase_Transitions_in_Spiked_Regression_Alignment_Driven_Benign_and_Catastrophic_Overfitting.pdf]]
