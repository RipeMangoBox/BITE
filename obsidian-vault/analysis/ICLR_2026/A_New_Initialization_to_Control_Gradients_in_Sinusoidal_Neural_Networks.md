---
title: "A New Initialization to Control Gradients in Sinusoidal Neural Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_New_Initialization_to_Control_Gradients_in_Sinusoidal_Neural_Networks.pdf
aliases:
- SP0I
- NICGSNN
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/theory
core_operator: "通过设置预激活方差固定点σ_a = 0和雅可比方差σ_g = 1，可以同时控制前向传播的频谱范围和反向传播的梯度缩放。"
primary_logic: "在无限宽度和深度极限下，预激活方差收敛到一个由Lambert W函数给出的固定点；通过选择(c_w, c_b) = (√3, 0)使σ_a = 0，可以抑制深层网络中虚假高频成分的出现，同时保持梯度稳定。"
claims:
- "提出的初始化(σ_a=0)在深度增加时抑制了频谱展宽，而原始SIREN和σ_a=1初始化则出现明显的高频成分增长。"
- "提出的初始化在1D、2D、3D多尺度函数拟合任务中，在不同深度上平均泛化误差均低于原始SIREN和其他基线方法。"
- "在图像拟合任务中，提出的初始化(σ_a=0和σ_a=1)相比其他SOTA方法（如WIRE、FINER）显著提升了模型估计质量，保留了清晰特征。"
- "1D多尺度函数拟合 上 泛化误差 = 最低"
---

# A New Initialization to Control Gradients in Sinusoidal Neural Networks

> [!tip] 核心洞察
> 在无限宽度和深度极限下，预激活方差收敛到一个由Lambert W函数给出的固定点；通过选择(c_w, c_b) = (√3, 0)使σ_a = 0，可以抑制深层网络中虚假高频成分的出现，同时保持梯度稳定。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种控制正弦神经网络梯度的新初始化方法 |
| 英文题名 | A New Initialization to Control Gradients in Sinusoidal Neural Networks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=92d74WdgtG) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/theory |
| Method | SIREN Proposed (σ_a=0 initialization) |
| Dataset | 1D多尺度函数拟合, 2D多尺度函数拟合, 3D多尺度函数拟合, 图像拟合（L=10, N=256） |

> [!tip] 效果简介
> - 1D多尺度函数拟合 上，泛化误差 为 最低，对比 SIREN原始初始化误差较高，变化 显著降低。
> - 2D多尺度函数拟合 上，泛化误差 为 最低，对比 SIREN原始初始化误差较高，变化 显著降低。
> - 3D多尺度函数拟合 上，泛化误差 为 最低，对比 SIREN原始初始化误差较高，变化 显著降低。

## 概述

该工作针对正弦神经网络（SIREN）在深度增加时梯度失控（爆炸或消失）导致输出频谱中混入虚假高频成分、泛化能力下降的核心瓶颈，提出了一种新的初始化策略。其核心因果机制在于：通过理论推导，在无限宽度与深度极限下，将**预激活方差的固定点**（$\sigma_a$）和**雅可比条目方差**（$\sigma_g$）作为两个可独立控制的自由度。通过设置 $(\sigma_a = 0, \sigma_g = 1)$，即选择权重缩放因子 $c_w = \sqrt{3}$ 与偏置方差 $c_b = 0$，该方法能同时抑制前向传播中频谱随深度的展宽（$\sigma_a=0$ 是关键），并确保反向传播的梯度既不爆炸也不消失（$\sigma_g=1$ 是关键）。

主要结果方面，在1D、2D、3D多尺度函数拟合任务中，提出的初始化在多个深度上的平均泛化误差均低于原始SIREN初始化（Sitzmann et al., 2020）及其他基线方法（如WIRE、FINER）。在图像拟合任务中（L=10, N=256），该方法生成的图像清晰、无伪影，显著优于对比方法。在物理信息神经网络（PINN）任务（如2D Navier-Stokes方程、复杂几何上的2D热方程）中，该方法成功重建了物理解，而原始SIREN初始化出现高频伪影，其他基线方法（FINER, Tanh, ReLU）则完全失败。此外，该方法在音频、视频拟合及图像去噪任务中也表现出一致的优势。

## 背景与动机

隐式神经表示（INR）通过神经网络将空间坐标直接映射到信号值，已广泛应用于图像、音频、视频和物理场建模。然而，标准MLP（如ReLU网络）受限于频谱偏置——倾向于学习低频成分，难以捕获高频细节。SIREN（Sitzmann等人，2020）通过使用正弦激活函数突破了这一限制，其周期性非线性使网络能够表示丰富的频率分量。但SIREN在深度增加时面临严重的梯度稳定性问题：原始Sitzmann初始化无法控制前向传播中预激活方差的增长，导致深层网络的输出频谱中虚假高频成分急剧膨胀，同时反向传播的梯度要么爆炸要么消失。这直接限制了SIREN的深度扩展能力，而深度正是提升表示复杂度和泛化性能的关键。

现有方法未能从根本上解决这一瓶颈。WIRE（Saragadam等人，2022）和FINER（Liu等人，2024）等SOTA架构虽然改进了INR性能，但并未从初始化层面系统性地控制正弦网络的梯度传播。标准初始化策略（如PyTorch默认、Xavier）在正弦激活下完全失效，因为正弦函数的非线性特性使得传统的方差分析不再适用。ReLU网络配合位置编码虽能缓解频谱偏置，但引入了额外的超参数和架构复杂性。

本文的核心动机是：能否通过理论驱动的初始化设计，同时控制SIREN的前向传播频谱范围和反向传播梯度缩放，从而在任意深度下保持稳定且表达力强的学习动力学？作者从无限宽度和深度极限下的信号传播理论出发，推导出预激活方差收敛到由Lambert W函数给出的固定点（Theorem 3.1），并揭示了关键因果旋钮：通过选择权重缩放因子 $c_w = \sqrt{3}$ 和偏置方差 $c_b = 0$，可使预激活方差固定点精确为 $\sigma_a = 0$。这一设置抑制了深层网络中虚假高频成分的指数级增长（见Figure 4的傅里叶频谱对比），同时通过确保雅可比条目方差 $\sigma_g = 1$ 维持梯度稳定。实验证据表明，该初始化在1D、2D、3D多尺度函数拟合任务中，在不同深度上的平均泛化误差均低于原始SIREN和其他基线方法（Figure 1）；在图像拟合任务中，相比WIRE、FINER等SOTA方法，显著提升了重建质量，保留了清晰特征且无伪影（Figure 2）。

## 核心创新

该工作的核心创新在于提出了一种精确控制正弦神经网络（SIREN）前向传播频谱与反向传播梯度的初始化策略，从根本上解决了原始SIREN初始化（Sitzmann等人，2020）在深度增加时因梯度失控而引入虚假高频成分并损害泛化能力的瓶颈。其关键因果旋钮在于同时设定两个统计量的目标固定点：**预激活方差** $\sigma_a = 0$ 与**雅可比方差** $\sigma_g = 1$。

**理论洞察与推导：** 论文证明，在无限宽度与深度极限下，SIREN网络的预激活方差收敛到一个由Lambert W函数 $\mathcal{W}_0$ 给出的固定点：$\sigma_a^2 = c_b^2 + \frac{c_w^2}{6} + \frac{1}{2} \mathcal{W}_0\left( -\frac{c_w^2}{3} e^{-\frac{c_w^2}{3} - 2c_b^2} \right)$（Theorem 3.1）。同时，逐层雅可比条目的缩放方差极限为 $\sigma_g = \frac{c_w^2}{6} \left( 1 + e^{-2\sigma_a^2} \right)$。原始SIREN初始化（$c_w=\sqrt{6}, c_b=0$）导致 $\sigma_a \approx 1$，这使网络在深层时前向传播的频谱向高频展宽，反向传播的梯度范数随深度呈几何级数增长（$\sigma_g > 1$），最终产生虚假高频噪声并降低泛化能力。

**具体改动（Changed Slots）：** 相比原始SIREN初始化，该方法做出了四项精确调整：
1.  **权重初始化分布（隐藏层）**：从 $U(-\sqrt{6}/\sqrt{N}, \sqrt{6}/\sqrt{N})$ 改为 $U(-c_w/\sqrt{N}, c_w/\sqrt{N})$，其中 $c_w = \sqrt{3}$。
2.  **偏置初始化分布**：从 $U(-1/\sqrt{N}, 1/\sqrt{N})$ 改为 $N(0, c_b^2)$，其中 $c_b = 0$。
3.  **预激活方差固定点**：从近似为1（未精确控制）改为精确设定为 $\sigma_a = 0$。
4.  **雅可比方差**：从未控制（随深度增长）改为通过 $c_b = \sqrt{1 - \frac{c_w^2}{3} - \frac{1}{2} \log(6/c_w^2 - 1)}$ 曲线精确确保 $\sigma_g = 1$。

**核心机制与证据：**
- **频谱控制**：设定 $\sigma_a = 0$ 使得深层网络的预激活分布集中在零点附近，从而抑制了正弦非线性引入的高频成分。实验证据（Figure 4）显示，在深度 $L \in \{4,8,16,32\}$ 和驱动频率 $w_0 \in \{100,1000\}$ 下，提出的初始化（$\sigma_a=0$）的傅里叶频谱展宽被强烈抑制，而原始SIREN和 $\sigma_a=1$ 初始化则出现明显的高频成分增长。这一机制直接解决了“拟合高频会损害泛化”这一核心问题（Figure 17-19, 1D/2D/3D多尺度函数拟合中泛化误差最低）。
- **梯度控制**：设定 $\sigma_g = 1$ 确保了端到端雅可比矩阵的最大奇异值在深度增加时保持准酉（nearly unitary），从而防止梯度爆炸或消失（Figure 8）。同时，这使得NTK矩阵的平均特征值随深度线性而非指数增长（Figure 6, 左图），保证了稳定的学习动力学。
- **NTK视角**：论文进一步从神经正切核（NTK）角度揭示了该初始化如何影响学习动态。NTK的特征向量呈现出类似傅里叶模态的振荡行为（Figure 5），而 $\sigma_a=0$ 初始化使得NTK特征基与傅里叶模态的重叠在深度增加时保持稳定，且低频对应小特征值（Figure 10），从而保留了SIREN固有的频谱偏差特性，同时避免了病态条件。

**实验验证与优势：** 在图像拟合（Figure 2）、音频拟合（Figure 11）、视频拟合（Figure 12）、图像去噪（Figure 13）以及物理信息神经网络（PINN）任务（Burgers方程、Navier-Stokes方程、复杂几何热方程，Figure 14-16）中，提出的初始化（$\sigma_a=0$）在视觉质量和定量指标上均显著优于原始SIREN、$\sigma_a=1$初始化、WIRE、FINER等SOTA方法。特别地，在2D Navier-Stokes PINN任务中，原始Sitzmann初始化产生高频伪影，而FINER、Tanh、ReLU方法完全失败，只有提出的初始化成功重建了物理解（Figure 15）。

**局限与未解问题：** 论文坦诚指出，该初始化**未实现完全动态等距**（Section B.1），表明仍有改进空间。此外，在Burgers 1D PINN实验中，原始Sitzmann初始化表现略优，暗示对于某些具有尖锐传播前沿的问题，高度病态的梯度分布可能反而有利。Theorem 3.1中描述的预激活方差 $\sigma_\ell$ 向零缓慢衰减的行为恰好补偿了非线性，避免了频谱的爆炸或坍缩，这一机制仍未得到解释，需要进一步研究。

## 整体框架

![[assets/figures/papers/iclr26_0003_92d74WdgtG_A_New_Initialization_to_Control_Gradients_in_Sin/figures/018_Figure_17.jpg]]
*Figure 17: 1d Averaged generalization and training error for the 1D fitting problem. The results are averaged over 10 runs for each architecture of width N = 1 2 8 . The error bars represent the standard deviation of the results*

本文提出的方法是一个针对正弦神经网络（SIREN）的初始化框架，其核心在于通过理论推导出的固定点条件，同时控制前向传播的预激活方差和反向传播的梯度缩放。整个 pipeline 由四个紧密耦合的模块构成：

**1. 第一层权重初始化：输入频率编码**

- **实现**：第一层权重 $\mathbf{W}_1$ 从均匀分布 $U(-\omega_0/n_0, \omega_0/n_0)$ 中采样，其中 $\omega_0$ 是驱动频率，$n_0$ 是输入维度。
- **作用**：将输入坐标映射到网络的第一层正弦激活函数的频率范围，决定网络能够编码的输入频率带宽。

**2. 隐藏层权重初始化：控制预激活方差固定点**

- **实现**：对于所有隐藏层 $\ell \in \{2, \dots, L\}$，权重 $\mathbf{W}_\ell$ 从均匀分布 $U(-c_w/\sqrt{N}, c_w/\sqrt{N})$ 中采样，其中 $c_w = \sqrt{3}$。
- **关键机制**：此设置使得在无限宽度和深度极限下，预激活方差的固定点 $\sigma_a = 0$（由 Lambert W 函数推导得出）。这是抑制深层网络中出现虚假高频成分的因果旋钮。相比之下，原始 SIREN 初始化（$U(-\sqrt{6}/\sqrt{N}, \sqrt{6}/\sqrt{N})$）未精确控制此固定点，导致预激活方差随深度发散，进而引发频谱展宽。

**3. 偏置初始化：配合梯度控制**

- **实现**：所有层的偏置 $\mathbf{b}_\ell$ 从正态分布 $N(0, c_b^2)$ 中初始化，其中 $c_b = 0$。
- **作用**：$c_b = 0$ 是确保预激活方差固定点 $\sigma_a = 0$ 的必要条件。同时，它与权重缩放因子 $c_w$ 共同满足雅可比方差 $\sigma_g = 1$ 的约束条件，即 $c_b = \sqrt{1 - c_w^2/3 - 1/2 \log(6/c_w^2 - 1)}$。

**4. 梯度控制：通过雅可比方差 $\sigma_g = 1$**

- **实现**：通过上述 $(c_w, c_b) = (\sqrt{3}, 0)$ 的选择，自动满足 $\sigma_g = 1$。
- **作用**：确保逐层雅可比条目的方差在极限下为 1，从而在反向传播过程中，梯度既不会爆炸也不会消失。这直接控制了神经正切核（NTK）矩阵的迹随深度的缩放关系，避免其呈几何级数增长（当 $\sigma_g^2 \neq 1$ 时）。

**整体输入输出流**：网络输入 $\mathbf{x}$ 经过第一层线性变换和正弦激活后，进入由 $L-1$ 个隐藏层组成的序列。每个隐藏层执行 $\sin(\mathbf{W}_\ell \mathbf{h}_{\ell-1} + \mathbf{b}_\ell)$ 操作。最终通过一个线性输出层 $\mathbf{W}_L$ 产生预测 $\boldsymbol{\Psi}_\theta(\mathbf{x})$。整个框架的核心贡献在于，通过理论推导出的初始化参数 $(c_w, c_b)$，在初始化时刻同时锁定了前向传播的频谱特性（$\sigma_a = 0$）和反向传播的梯度稳定性（$\sigma_g = 1$），从而避免了原始 SIREN 在深度增加时出现的梯度失控和频谱展宽问题。

**证据强度说明**：该 pipeline 的模块划分和参数选择在论文的“方法”部分（Section 3）有明确的理论推导和公式支持（公式 8-10），置信度高。有限宽度和深度下的实验验证（Figure 20, 21）表明，即使在非理想条件下（如 N=32 或 L=40），该框架仍能保持较低噪声水平，但其理论推导基于无限宽度和深度的假设，因此在实际有限设置中可能存在偏差。

## 核心模块与公式推导

### 1. SIREN架构与初始化问题

本文研究的对象是**正弦神经网络（SIREN）**，其网络输出定义为逐层正弦激活的复合函数，最终接一个线性层（Equation 5）：

$$
\boldsymbol{\Psi}_{\boldsymbol\theta}(\pmb{x}) = \mathbf{W}_L \sin\Big( \mathbf{W}_{L-1} \sin( ... \sin( \mathbf{W}_1 \pmb{x} + \mathbf{b}_1 ) ) + \mathbf{b}_{L-1} \Big) + \mathbf{b}_L
$$

其中第 $\ell$ 层的预激活为 $\mathbf{z}_\ell = \mathbf{W}_\ell \mathbf{h}_{\ell-1} + \mathbf{b}_\ell$。

**真实瓶颈**：原始SIREN初始化（Sitzmann等人，2020）在深度增加时无法控制梯度，导致梯度爆炸或消失，从而在重建信号中引入虚假的高频成分，降低泛化能力。

### 2. 预激活方差的固定点理论

**核心因果旋钮**：通过设置预激活方差固定点 $\sigma_a = 0$ 和雅可比方差 $\sigma_g = 1$，可以同时控制前向传播的频谱范围和反向传播的梯度缩放。

在无限宽度和深度极限下，预激活方差的**固定点**由Lambert W函数给出（Theorem 3.1, Equation 10）：

$$
\sigma_a^2 = c_b^2 + \frac{c_w^2}{6} + \frac{1}{2} \mathcal{W}_0\left( -\frac{c_w^2}{3} e^{-\frac{c_w^2}{3} - 2c_b^2} \right)
$$

其中 $c_w$ 和 $c_b$ 分别控制权重和偏置的初始化缩放。该公式来源于预激活方差的递推关系（Appendix A.1）：

$$
\sigma_\ell^2 = \frac{c_w^2}{6}\left(1 - e^{-2\sigma_{\ell-1}^2}\right) + c_b^2
$$

以及正弦函数对方差的影响（Lemma A.2）：$\mathrm{Var}[\sin(z)] = \frac{1}{2}\left(1 - e^{-2\sigma^2}\right)$。

### 3. 雅可比方差控制

逐层雅可比条目方差的极限值为（Section 3.2）：

$$
\sigma_g = \frac{c_w^2}{6} \big( 1 + e^{-2\sigma_a^2} \big)
$$

为确保梯度既不爆炸也不消失，需要 $\sigma_g = 1$。由此导出**权重-偏置方差曲线**（Equation 8）：

$$
c_b = \sqrt{1 - \frac{c_w^2}{3} - \frac{1}{2} \log\biggl( \frac{6}{c_w^2} - 1 \biggr)}
$$

这条曲线给出了所有能使梯度保持稳定的 $(c_w, c_b)$ 组合。

### 4. 提出的初始化方案

**核心洞察**：在无限宽度和深度极限下，通过选择 $(c_w, c_b) = (\sqrt{3}, 0)$ 使 $\sigma_a = 0$，可以抑制深层网络中虚假高频成分的出现，同时保持梯度稳定（Equation 9）：

$$
\sigma_a = 0 \quad (\mathrm{Proposed}): (c_w, c_b) = (\sqrt{3}, 0)
$$

具体的初始化分布为：
- **第一层权重**：$W_1 \sim U(-\omega_0/n_0, \omega_0/n_0)$，控制输入频率编码
- **隐藏层权重**：$W_\ell \sim U(-c_w/\sqrt{N}, c_w/\sqrt{N})$，其中 $c_w = \sqrt{3}$
- **偏置**：$b_\ell \sim N(0, c_b^2)$，其中 $c_b = 0$

### 5. NTK动力学分析

在NTK框架下，梯度下降下残差的连续时间演化由NTK矩阵驱动（Section 4）：

$$
\frac { \mathrm { d } \pmb { u } ( t ) } { \mathrm { d } t } = \mathbf { K } _ { \theta _ { t } } \pmb { u } ( t )
$$

残差可表示为NTK特征模态的指数衰减和：

$$
\pmb { u } ( t ) = \exp ( - t \mathbf { K } _ { \theta _ { 0 } } ) \pmb { u } ( 0 ) = \sum _ { i = 1 } ^ { | \mathbb { I } | } e ^ { - t \lambda _ { i } } \langle \pmb { u } ( 0 ) , \pmb { v } _ { i } \rangle \pmb { v } _ { i }
$$

NTK迹随深度的缩放关系为：

$$
\frac { 1 } { \vert { \mathbb { I } } \vert N } \operatorname { T r } ( \mathbf { K } _ { \theta _ { 0 } } ) \propto \frac { ( \sigma _ { g } ^ { 2 } ) ^ { L + 1 } - 1 } { \sigma _ { g } ^ { 2 } - 1 }
$$

当 $\sigma_g^2 \neq 1$ 时，NTK迹呈几何级数增长或衰减，导致训练不稳定。提出的初始化通过设置 $\sigma_g = 1$ 避免了这一问题。

### 6. 关键变量含义总结

| 变量 | 含义 | 关键值 |
|------|------|--------|
| $\sigma_a$ | 预激活方差的固定点 | 提出：0 |
| $\sigma_g$ | 逐层雅可比条目方差的极限值 | 提出：1 |
| $c_w$ | 权重初始化缩放因子 | 提出：$\sqrt{3}$ |
| $c_b$ | 偏置初始化标准差 | 提出：0 |
| $\omega_0$ | 第一层驱动频率 | 问题相关 |
| $N$ | 隐藏层宽度 | 架构参数 |
| $L$ | 网络深度 | 架构参数 |
| $\mathcal{W}_0$ | Lambert W函数主分支 | 固定点解 |

**证据强度说明**：所有公式均来自论文原文，置信度1.0。理论推导在无限宽度和深度极限下成立，有限宽度和有限深度下可能存在偏差。论文指出提出的初始化未实现完全动态等距（Section B.1），表明仍有改进空间。

## 实验与分析

### 主结果：提出初始化在多项任务中实现最低泛化误差

在1D、2D、3D多尺度函数拟合任务中，提出的初始化（σ_a=0）在不同深度上平均泛化误差均低于原始SIREN、σ_a=1初始化以及其他SOTA方法（如WIRE、FINER）（Figure 1, 17, 18, 19）。在图像拟合任务中（L=10, N=256），提出的初始化（σ_a=0和σ_a=1）相比其他基线方法显著提升了模型估计质量，保留了清晰特征，而原始SIREN初始化则出现明显的高频噪声伪影（Figure 2）。在音频拟合（Figure 11）、视频拟合（ERA-5数据集，Figure 12）和图像去噪（Figure 13）任务中，提出的初始化同样取得了最佳视觉质量。在PINN实验中，提出初始化在Navier-Stokes 2D问题中成功重建物理解，而原始Sitzmann初始化出现高频伪影，FINER、Tanh、ReLU方法完全失败（Figure 15）；在2D热方程（复杂几何）中，提出初始化成功复现真实解，而σ_a=1初始化产生明显噪声和不稳定解（Figure 16）。在Burgers 1D PINN实验中，原始Sitzmann初始化表现略优（Figure 14），这表明对于某些具有尖锐传播前沿的问题，高度病态的梯度分布可能反而有利——这是方法的一个已知局限。

### 频谱控制：σ_a=0初始化抑制深层虚假高频成分

核心因果机制验证实验（Figure 4）展示了关键证据：对于不同深度L ∈ {4,8,16,32}和驱动频率w_0 ∈ {100,1000}，提出的初始化（σ_a=0）在深度增加时显著抑制了频谱展宽，网络输出的傅里叶频谱保持集中。相比之下，原始SIREN初始化和σ_a=1初始化在深度增加时均出现明显的高频成分增长，这些虚假高频成分直接导致了泛化能力的下降。这一结果直接支持了论文的核心洞察：通过设置预激活方差固定点σ_a=0，可以控制前向传播的频谱范围，避免深层网络中虚假高频成分的出现。

### NTK分析：梯度控制和频谱偏置的机制解释

通过NTK框架分析发现（Section 4），NTK迹随深度的缩放关系由σ_g控制：当σ_g^2 ≠ 1时，NTK迹呈几何级数增长（式：`(1/|I|N) Tr(K_θ_0) ∝ ((σ_g^2)^(L+1) - 1)/(σ_g^2 - 1)`）。提出的初始化通过设置σ_g=1确保NTK迹不随深度爆炸或消失。Figure 5展示了NTK矩阵的前六个特征向量呈现类似傅里叶模态的振荡行为，特征值随模式索引递减。Figure 6进一步显示，σ_a=0初始化下NTK平均特征值随深度保持稳定，而原始Sitzmann初始化则出现指数级增长。Figure 9和Figure 10分别展示了NTK特征值谱和特征基与傅里叶模态的重叠随深度的演化：σ_a=0和σ_a=1初始化保持相对稳定的特征值分布，且σ_a=0初始化在低频区域（低于w_0）保持了几乎完美的傅里叶对齐，这解释了其更好的泛化能力。

### 雅可比奇异值谱和动态等距

Figure 8展示了端到端雅可比矩阵的奇异值谱随深度的演化。提出的σ_a=0初始化保持了近乎单位归一化的最大奇异值，且谱分布随深度稳定；而原始Sitzmann初始化的奇异值谱随深度显著展宽。然而，论文明确指出（Section B.1）"our initialization does not achieve full dynamical isometry, indicating that there remains room for improvement"——即提出的初始化未实现完全动态等距，这是方法的一个已知局限和未来改进方向。

### 消融研究：有限宽度和大深度的影响

有限宽度实验（Figure 20）显示，当宽度N=32时，提出的初始化仍能保持较低噪声水平，而Sitzmann和σ_a=1初始化噪声较高；当N=128时，所有方法性能提升，但提出初始化仍最优。大深度实验（Figure 21）揭示了有趣的现象：当深度L=40时，σ_a=0初始化性能甚至提升，噪声进一步降低；σ_a=1初始化性能出奇地好但高频成分增长；而原始Sitzmann初始化泛化性能严重下降。这进一步验证了σ_a=0初始化在深度增加时的稳定性优势。


![[assets/figures/papers/iclr26_0003_92d74WdgtG_A_New_Initialization_to_Control_Gradients_in_Sin/figures/021_Figure_20.jpg]]
*Figure 20: Comparison of the discussed initialization method, and how finite width ( N = 3 2 and N = 1 2 8 ) affects their performance and behavior. The setting of the experiments are the same as one described in Figure 2*

![[assets/figures/papers/iclr26_0003_92d74WdgtG_A_New_Initialization_to_Control_Gradients_in_Sin/figures/022_Figure_21.jpg]]
*Figure 21: Comparison of the discussed initialization method, and how large depth affect their performance and behavior. The setting of the experiments are the same as one described in Figure 2*

### 理论预测的实验验证

Figure 3验证了预激活分布和雅可比条目分布的理论预测。实验测量的σ_a和σ_g等高线与理论预测（黑色实线表示σ_a=1，虚线表示σ_g=1）高度一致，验证了Theorem 3.1和Theorem 3.2在有限宽度（N=256, L=10）下的有效性。红色和黑色圆点分别对应Proposition 3.1中定义的三种初始化方案（Sitzmann原始、σ_a=1、σ_a=0），实验测量值与理论值吻合良好。

## 方法谱系与知识库定位

### 与 Baseline/Follow-up 的关系

本文的核心贡献是对 Sitzmann 等人 (2020) 提出的原始 SIREN 初始化方案进行了理论驱动的修正。原始 SIREN 初始化（隐藏层权重 `U(-√6/√N, √6/√N)`，偏置 `U(-1/√N, 1/√N)`）在深度增加时无法有效控制梯度，导致网络输出频谱展宽，引入虚假高频成分，从而损害泛化能力。本文通过均值场分析，揭示了该问题的因果机制：预激活方差的固定点 `σ_a` 和雅可比条目的方差 `σ_g` 是控制网络行为的关键旋钮。

提出的方法将初始化参数化为 `(c_w, c_b)` 两个标量，并精确设置 `(c_w, c_b) = (√3, 0)`，使得 `σ_a = 0` 且 `σ_g = 1`。这一改动直接抑制了深层网络中高频成分的指数级增长（见 Figure 4），同时确保了前向传播和反向传播的稳定性。与后续的 SOTA 架构（如 WIRE、FINER）相比，该方法在图像拟合（Figure 2）、多尺度函数拟合（Figure 1）及 PINN 任务（Figure 15、16）中均展现出更优或相当的性能，且无需改变网络架构本身。

### 适用边界

该方法的有效性建立在无限宽度和无限深度的理论极限推导之上。实验验证表明，在有限宽度（如 N=32，见 Figure 20）和极大深度（如 L=40，见 Figure 21）下，该方法依然能保持较低噪声水平，显示出对网络规模的良好鲁棒性。然而，该方法对输入频率编码参数 `w_0` 的依赖较强，需要针对不同问题（如 Burgers 方程用 `w_0=2`，热方程用 `w_0=1`）进行手动调整。其适用场景主要集中在需要精确表示高频细节且网络深度较大的隐式神经表示（INR）任务中。

### 局限与开放问题

1.  **动态等距未完全实现**：论文明确指出“our initialization does not achieve full dynamical isometry”（Section B.1），这意味着端到端雅可比矩阵的奇异值谱并非完全集中在1附近，仍有优化空间。能否通过额外的权重分布约束来增强动态等距稳定性，是一个待解决的问题。

2.  **理论空白**：Theorem 3.1 中描述的预激活方差 `σ_ℓ` 向零缓慢衰减的行为，恰好补偿了正弦函数的非线性，避免了频谱的爆炸或坍缩。这种“恰到好处”的补偿机制在理论上仍未得到充分解释。

3.  **特定任务下的性能反转**：在 Burgers 1D PINN 实验中，原始 Sitzmann 初始化表现略优于提出方法。这表明对于具有尖锐传播前沿的问题，高度病态的梯度分布可能反而有利，揭示了梯度控制与任务需求之间的复杂权衡。

4.  **扩展方向**：未来工作可将该方法扩展到更复杂的损失函数（如物理信息设置），并探索其在基于 INR 的大气和海洋场重建中的潜在应用。此外，通过考虑层雅可比矩阵的奇异值分布等网络结构特性，可以进一步拓宽理论视角。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_New_Initialization_to_Control_Gradients_in_Sinusoidal_Neural_Networks.pdf

![[paperPDFs/ICLR_2026/A_New_Initialization_to_Control_Gradients_in_Sinusoidal_Neural_Networks.pdf]]
