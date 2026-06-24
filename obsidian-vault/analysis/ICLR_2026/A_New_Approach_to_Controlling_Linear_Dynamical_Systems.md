---
title: "A New Approach to Controlling Linear Dynamical Systems"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_New_Approach_to_Controlling_Linear_Dynamical_Systems.pdf
aliases:
- OSCO
- NACLDS
- "Online Spectral Control (OSC)"
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/reinforcement_learning_and_planning
core_operator: "使用从特定Hankel矩阵（公式2.1）的特征向量构造的谱滤波器，将控制策略参数化，从而将问题转化为对低维谱特征的回归。"
primary_logic: "通过谱表示压缩扰动历史，将在线控制问题转化为在线凸优化问题，使得参数数量仅与log(T/γ)成正比，从而将运行时间对1/γ的依赖从多项式降低到多对数级别。"
claims:
- "OSC算法的运行时间仅为O(log^4(T/γ))，而GPC的运行时间为O(γ^{-1} log T)。"
- "OSC算法的遗憾界为Õ(γ^{-4} √T)，与GPC的Õ(γ^{-5.5} √T)相比，对γ的依赖更优。"
- "OSC使用远少于GPC的参数（h=O(polylog(T/γ)) vs. GPC的m=O(γ^{-1} log T)），但在多种设置下性能相当或更优。"
- "线性动力系统 (LDS) 上 累积损失 = OSC (线性头)"
---

# A New Approach to Controlling Linear Dynamical Systems

> [!tip] 核心洞察
> 通过谱表示压缩扰动历史，将在线控制问题转化为在线凸优化问题，使得参数数量仅与log(T/γ)成正比，从而将运行时间对1/γ的依赖从多项式降低到多对数级别。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 一种控制线性动力系统的新方法 |
| 英文题名 | A New Approach to Controlling Linear Dynamical Systems |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=BQIzu1T6F0) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/reinforcement_learning_and_planning |
| Method | Online Spectral Control (OSC) |
| Dataset | 线性动力系统 (LDS), 非线性动力系统 (LDS ReLU) |

> [!tip] 效果简介
> - 线性动力系统 (LDS) 上，累积损失 为 OSC (线性头)，对比 GPC (线性头)，变化 性能相当。
> - 非线性动力系统 (LDS ReLU) 上，累积损失 为 OSC (线性头)，对比 GPC (线性头)，变化 性能相当。
> - 线性动力系统 (LDS) 上，累积损失 为 OSC (100隐藏单元MLP头)，对比 GPC (100隐藏单元MLP头)，变化 性能相当。

## 概述

本文针对线性动力系统（LDS）的在线控制问题，提出了一种名为在线谱控制（Online Spectral Control, OSC）的新方法。该问题的核心瓶颈在于：现有方法（如GPC）的计算复杂度与系统稳定性裕度γ的倒数呈多项式关系，导致在边际稳定系统（γ很小）时运行时间过长。OSC通过引入一种基于特定Hankel矩阵谱分解的凸松弛技术，将控制策略参数化为对扰动与谱滤波器卷积的线性回归，从而将在线控制问题转化为低维谱特征空间上的在线凸优化问题。

**核心结论**：OSC实现了对γ的多对数依赖（运行时间O(log⁴(T/γ))），而GPC为多项式依赖（O(γ⁻¹ log T)）。在遗憾界方面，OSC达到Õ(γ⁻⁴√T)，优于GPC的Õ(γ⁻⁵·⁵√T)。实验结果表明，在多种设置下（线性/非线性动力学、不同状态维度、不同扰动分布），OSC使用远少于GPC的参数（h=15 vs. GPC的m=50），但性能相当或更优。

**方法定位**：OSC属于在线凸优化框架下的在线控制方法。其关键创新在于使用Hankel矩阵（公式2.1）的top-h特征对构建谱滤波器，将控制输入计算为：u_t = Σ σ_i^{1/4} M_i^t Ẅ_{t-1:t-m} φ_i。这使得参数数量仅与log(T/γ)成正比，而非GPC中与γ⁻¹成正比。算法由四个模块构成：离线谱滤波器计算、在线控制输入生成、扰动推断、以及投影在线梯度下降参数更新。

**主要结果**：理论分析（Theorem 2.1）给出了OSC相对于对角化稳定线性策略类S的遗憾上界，Corollary 2.2证明了平均运行时间为O(log⁴(T/γ))。实验验证（Figure 2）显示OSC在LDS和LDS ReLU两种动力学下，无论使用线性头还是MLP头，累积损失均与GPC相当。消融实验（Figure 4）表明，当谱参数h=20时，OSC已完全匹配GPC性能。

## 背景与动机

在线控制线性动力系统（LDS）的核心挑战在于：系统状态演化遵循 $\mathbf{x}_{t+1} = A \mathbf{x}_t + B \mathbf{u}_t + \mathbf{w}_t$，控制器需要在未知、可能对抗性的扰动 $\mathbf{w}_t$ 下，仅基于历史观测即时生成控制输入 $\mathbf{u}_t$。这一问题在实际应用中广泛存在，从机器人控制到过程自动化，但现有方法在处理边际稳定系统时面临严重的计算瓶颈。

**现有方法的根本瓶颈**在于计算复杂度与系统稳定性裕度 $\gamma$ 的关系。稳定性裕度 $\gamma$ 衡量系统矩阵 $A$ 的最大特征值与单位圆之间的距离——$\gamma$ 越小，系统越接近不稳定，控制问题越困难。以代表性的在线控制方法 GPC（Agarwal et al., 2019a）为例，其运行时间为 $O(\gamma^{-1} \log T)$，即与 $1/\gamma$ 呈多项式关系。这意味着当系统接近边际稳定（$\gamma$ 很小）时，GPC 的运行时间会急剧增长，使得实际部署变得不可行。这一依赖源于 GPC 的策略参数化方式：它直接对过去 $m = O(\gamma^{-1} \log T)$ 个扰动进行线性回归，参数数量随 $1/\gamma$ 线性增长，导致每次迭代的计算开销也随之增长。

**本文的核心动机**是打破这种多项式依赖，实现运行时间对 $1/\gamma$ 的多对数依赖。作者观察到，虽然控制策略理论上需要记忆很长的扰动历史来抵消系统的不稳定性，但这些历史信息存在大量的结构冗余。具体而言，系统对扰动的响应可以通过一个特定的 Hankel 矩阵（其元素为 $H_{ij} = (1-\gamma)^{i+j-1} / (i+j-1)$）的特征分解来高效压缩。该矩阵的特征向量 $\phi_i$ 构成了自然的时间滤波器，能够以指数级效率提取扰动历史中与控制决策最相关的成分。

**因果机制的关键旋钮**在于策略参数化的重新设计。OSC 不直接对原始扰动进行回归，而是将控制输入参数化为 $\mathbf{u}_t = \sum_{i=1}^h \sigma_i^{1/4} M_i^t \tilde{W}_{t-1:t-m} \phi_i$，其中 $\sigma_i$ 和 $\phi_i$ 是 Hankel 矩阵的 top-$h$ 特征对。这一谱表示将问题从高维时间序列回归转化为对低维谱特征的回归——参数数量从 $O(m n d)$ 压缩到 $O(h n d)$，其中 $h = O(\text{polylog}(T/\gamma))$ 远小于 $m = O(\gamma^{-1} \log T)$。这种压缩的物理直觉是：系统对扰动的响应主要由低频成分主导，而 Hankel 矩阵的特征向量恰好捕捉了这些主导模式（如 Figure 1 所示，特征向量呈现出光滑的振荡形态）。

**核心理论洞察**是，通过这种谱参数化，在线控制问题被转化为在线凸优化问题，从而可以利用投影在线梯度下降高效求解。其直接后果是：OSC 的运行时间仅为 $O(\log^4(T/\gamma))$（Corollary 2.2），将 $1/\gamma$ 的依赖从多项式降低到多对数级别。同时，遗憾界也从 GPC 的 $\tilde{O}(\gamma^{-5.5} \sqrt{T})$ 改进到 $\tilde{O}(\gamma^{-4} \sqrt{T})$（Table 1），虽然对 $\gamma$ 的依赖仍然存在，但已经显著缓解。

**证据强度评估**：上述核心声明有明确的定理和推论支撑（Corollary 2.2, Theorem 2.1, Table 1），置信度达到 0.98。但需注意，理论分析假设系统动力学 $(A, B)$ 已知且时不变，遗憾界中的常数 $C_1 = G \kappa_B \kappa^8 W^2$ 可能在实际中很大，导致预热时间较长。此外，实验仅在合成数据上进行（Figure 2-6），虽然验证了 OSC 与 GPC 在各种设置下性能相当，但缺乏真实世界控制任务的验证，这是该工作的一个明确局限性。

## 核心创新

OSC的核心创新在于通过**谱表示压缩扰动历史**，将在线控制问题转化为**低维凸优化问题**，从而从根本上改变了策略参数化方式和对系统稳定性裕度γ的计算依赖。

**瓶颈与因果机制。** 现有在线控制方法（如GPC）的计算复杂度和遗憾界对稳定性裕度γ的倒数呈多项式依赖（GPC运行时间为O(γ⁻¹ log T)，遗憾界为Õ(γ^{-5.5} √T)）。当系统接近边际稳定（γ很小）时，这类方法需要极长的记忆长度和大量参数，导致运行时间不可接受。OSC的因果机制在于：使用从特定Hankel矩阵（公式2.1：H_{ij} = (1-γ)^{i+j-1}/(i+j-1)）的特征向量构造的**谱滤波器**，将控制策略参数化。这使得策略参数数量仅与log(T/γ)成正比，而非与1/γ成正比。

**核心改变：策略参数化。** 这是最关键的变化槽位。基线方法（GPC）直接对过去m个扰动进行线性回归，参数数量为O(m n d)，其中m = O(γ⁻¹ log T)。OSC则对扰动与谱滤波器的卷积进行线性回归（Algorithm 1, line 6: u_t = Σ σ_i^{1/4} M_i^t Ẅ φ_i），参数数量为O(h n d)，其中h = O(polylog(T/γ))。这意味着OSC可以用远少于GPC的参数达到可比性能——实验中GPC使用50d个参数，而OSC仅使用15d个参数（h=15），且当h=20时性能几乎相同（Figure 4）。

**计算复杂度的质变。** 第二个关键变化槽位是计算复杂度对γ的依赖从多项式降为多对数：OSC的平均运行时间为O(log⁴(T/γ))（Corollary 2.2），而GPC为O(γ⁻¹ log T)。这一质变源于谱表示将在线控制问题转化为在线凸优化问题（Algorithm 1本质上是投影在线梯度下降，应用于凸集K，损失函数ℓ_t为凸函数（Lemma B.2）），使得每次迭代只需处理h个低维谱特征，而非m个高维原始扰动。

**遗憾界的改善。** 第三个变化槽位是遗憾界对γ的依赖从Õ(γ^{-5.5} √T)降低到Õ(γ^{-4} √T)（Table 1）。虽然仍存在多项式依赖，但改进来源于谱控制器类Π_{h,m,γ}^{SC}（Definition 4.1）能够更高效地逼近开环最优控制器类Π_m^{OLOC}（Lemma A.3），从而减少了近似误差。

**算法管道。** OSC包含四个模块：(1) 离线计算Hankel矩阵的top-h特征对{(σ_j, φ_j)}（Algorithm 1, line 2）；(2) 在线计算控制输入u_t（line 6）；(3) 利用已知动力学推断扰动w_t = x_{t+1} - A x_t - B u_t（line 7）；(4) 通过投影在线梯度下降更新参数M_{1:h}以最小化记忆无关损失ℓ_t（line 8）。这一管道的关键设计是：谱滤波器在离线阶段一次性计算，在线阶段仅需对低维谱特征进行回归，避免了GPC中每步对长历史扰动的显式操作。

**实验证据强度。** 实验证据支持核心创新：在多种设置下（线性/非线性动力学、线性/MLP头），OSC与GPC性能相当（Figure 2），但参数数量减少约70%（GPC: 50d vs. OSC: 15d）。消融实验进一步验证了谱表示的有效性：即使h=5，OSC也具有竞争力；h=20时性能几乎相同（Figure 4）。然而，实验仅在合成数据上进行，缺乏真实世界控制任务的验证，这是一个明确的弱点。遗憾界中的常数C₁ = G κ_B κ⁸ W²可能很大，导致实际中需要较长的预热时间。

## 整体框架

Online Spectral Control (OSC) 的整体 pipeline 围绕一个核心洞察构建：将在线控制问题转化为在线凸优化问题，通过谱表示压缩扰动历史，使参数数量仅与 $\log(T/\gamma)$ 成正比。

**系统模型与问题设置**：考虑标准线性动力系统 $\mathbf{x}_{t+1} = A \mathbf{x}_t + B \mathbf{u}_t + \mathbf{w}_t$（公式1.1），其中状态 $\mathbf{x}_t \in \mathbb{R}^d$，控制输入 $\mathbf{u}_t \in \mathbb{R}^n$，扰动 $\mathbf{w}_t$ 由对抗性环境产生。系统动力学 $(A, B)$ 已知且时不变，满足 $(\kappa, \gamma)$-强稳定性条件。目标是设计在线策略，在未知未来扰动的情况下最小化累积损失。

**瓶颈与因果机制**：现有方法如 GPC 的计算复杂度与稳定性裕度 $\gamma$ 的倒数呈多项式关系，导致在边际稳定系统（$\gamma$ 很小）中运行时间过长。OSC 的因果机制在于：使用从特定 Hankel 矩阵 $H_{ij} = \frac{(1-\gamma)^{i+j-1}}{i+j-1}$（公式2.1）的特征向量构造的谱滤波器，将控制策略参数化。该 Hankel 矩阵的谱衰减极快，使得仅需 $h = O(\log T \log(T/\gamma))$ 个 top 特征对即可高精度近似任意稳定线性策略。

**四模块 pipeline**：

1. **谱滤波器计算（离线）**：计算 Hankel 矩阵 $H_m$ 的 top-$h$ 特征对 $\{(\sigma_j, \phi_j)\}_{j=1}^h$。该矩阵编码了稳定线性策略的响应结构，其快速谱衰减（Lemma C.2）保证了低秩近似的有效性。此步骤离线执行，计算成本为 $O(m^3)$，其中 $m = O(\gamma^{-1} \log(T/\gamma))$。

2. **控制输入生成（在线）**：在每步 $t$，基于过去 $m$ 个扰动的窗口 $\tilde{W}_{t-1:t-m}$，计算控制输入：
   
$$
\mathbf{u}_t = \sum_{i=1}^h \sigma_i^{1/4} M_i^t \tilde{W}_{t-1:t-m} \phi_i
$$

   其中 $M_i^t \in \mathbb{R}^{n \times d}$ 是当前可学习参数。该计算本质上是将扰动历史与谱滤波器卷积后进行线性回归，参数数量仅 $O(h n d)$，而 GPC 需要 $O(m n d)$ 个参数。

3. **扰动推断（在线）**：利用已知动力学和观测状态推断当前扰动：
   
$$
\mathbf{w}_t = \mathbf{x}_{t+1} - A \mathbf{x}_t - B \mathbf{u}_t
$$

   此步骤将未观测的扰动转化为可用的特征，使算法能够基于完整的历史扰动窗口进行决策。

4. **投影在线梯度下降（在线）**：更新参数 $M_{1:h}$ 以最小化记忆无关损失 $\ell_t$。损失函数 $\ell_t(M_{1:h})$ 在 $M_{1:h}$ 上是凸的（Lemma B.2），且具有显式的 Lipschitz 常数（Lemma B.3）。投影步确保参数保持在凸可行集 $K$ 内，该集合通过状态和控制的界 $\|x_t^M\|, \|u_t^M\| \leq 3\kappa^3 W/\gamma$ 和参数范数界 $\|M_{1:h}\| \leq \kappa^3 \sqrt{2h/\gamma}$（Definition 4.2）定义。

**输入输出流**：系统在每个时间步 $t$ 接收：当前状态 $\mathbf{x}_t$、上一步控制 $\mathbf{u}_{t-1}$、上一步扰动 $\mathbf{w}_{t-1}$（从第3步推断）。输出：当前控制输入 $\mathbf{u}_t$。算法维护一个长度为 $m$ 的扰动滑动窗口 $\mathbf{w}_{t-1:t-m}$，以及 $h$ 个可学习矩阵 $M_{1:h}$。

**理论保证**：OSC 的遗憾界为 $\mathrm{Regret}_T(\mathrm{OSC}, \mathcal{S}) = \frac{C_0 C_1 \sqrt{T}}{\gamma^4} \log^3\left(\frac{C_1 T d}{\gamma^3}\right)$（Theorem 2.1），相比 GPC 的 $\tilde{O}(\gamma^{-5.5} \sqrt{T})$ 对 $\gamma$ 的依赖更优。关键在于，每个时间步的平均运行时间仅为 $O(\log^4(T/\gamma))$（Corollary 2.2），而 GPC 为 $O(\gamma^{-1} \log T)$，实现了从多项式到多对数的飞跃。

## 核心模块与公式推导

### 问题设定与状态演化

考虑一个线性动力系统（LDS），其状态演化由以下方程描述：

$$
\mathbf{x}_{t+1} = A \mathbf{x}_t + B \mathbf{u}_t + \mathbf{w}_t
$$

其中 $\mathbf{x}_t \in \mathbb{R}^n$ 是状态向量，$\mathbf{u}_t \in \mathbb{R}^d$ 是控制输入，$\mathbf{w}_t$ 是扰动。系统动力学 $(A, B)$ 已知且时不变。该问题的核心瓶颈在于：现有在线控制方法（如GPC）的计算复杂度与系统稳定性裕度 $\gamma$ 的倒数呈多项式关系，导致在边际稳定系统（$\gamma$ 很小）中运行时间过长。

### 谱滤波器与Hankel矩阵

OSC方法的核心创新在于使用从特定Hankel矩阵的特征向量构造的谱滤波器来参数化控制策略。该Hankel矩阵的元素定义为：

$$
H_{ij} = \frac{(1-\gamma)^{i+j-1}}{i+j-1}
$$

其中 $\gamma$ 是系统的稳定性裕度。该矩阵的谱衰减特性是算法效率的关键：其奇异值呈指数级衰减，使得仅需少量top特征对即可近似整个矩阵。具体地，对于大小为 $m$ 的Hankel矩阵 $H_m$，其奇异值满足：

$$
\sigma_j \leq 156800 \log\left( \frac{2}{\gamma} \right) \cdot \exp\left( -\frac{\pi^2 j}{4 \log T} \right)
$$

这一指数衰减保证了仅需 $h = O(\log T \log(Td/\gamma^3))$ 个top特征对即可达到所需精度。

### 谱控制器类

OSC将控制策略参数化为对扰动与谱滤波器的卷积进行线性回归。谱控制器类定义为：

$$
\Pi_{h,m,\gamma}^{\mathrm{SC}} = \left\{ \pi_{h,m,\gamma,M}^{\mathrm{SC}}(\mathbf{w}_{t-1:t-m}) = \sum_{i=1}^h \sigma_i^{1/4} M_i \tilde{W}_{t-1:t-m} \phi_i \right\}
$$

其中：
- $h$ 是使用的top特征对数量，$h = \lceil 4 \log T \log(900 C_1 d T / \gamma^3) \rceil$
- $m$ 是记忆长度，$m = \lceil (1/\gamma) \log(8 C_1 \sqrt{T} / \gamma^3) \rceil$
- $\sigma_i$ 和 $\phi_i$ 分别是Hankel矩阵 $H_m$ 的第 $i$ 个特征值和特征向量
- $M_i \in \mathbb{R}^{n \times d}$ 是可学习的参数矩阵
- $\tilde{W}_{t-1:t-m}$ 是扰动历史的特定变换

与GPC直接使用过去 $m$ 个扰动进行线性回归（参数数量 $O(m n d)$）不同，OSC的参数数量仅为 $O(h n d)$，其中 $h = O(\text{polylog}(T/\gamma))$，远小于GPC的 $m = O(\gamma^{-1} \log T)$。

### 控制输入计算

在每时间步 $t$，控制输入通过以下方式计算：

$$
\mathbf{u}_t = \sum_{i=1}^h \sigma_i^{1/4} M_i^t \tilde{W}_{t-1:t-m} \phi_i
$$

其中 $M_i^t$ 是时间步 $t$ 时的参数矩阵。该计算可以解释为对扰动与谱滤波器的卷积进行线性回归，谱滤波器由Hankel矩阵的特征向量构造。

### 在线学习框架

OSC算法本质上是在线投影梯度下降（Projected Online Gradient Descent）的一个实例。参数集合 $K$ 定义为：

$$
K = \left\{ M_{1:h} \in \mathbb{R}^{h \times n \times d} \mid \|x_t^M\|, \|u_t^M\| \leq \frac{3\kappa^3 W}{\gamma}, \|M_{1:h}\| \leq \kappa^3 \sqrt{\frac{2h}{\gamma}} \right\}
$$

该集合是凸的（Lemma B.1），且损失函数 $\ell_t(M_{1:h})$ 关于参数 $M_{1:h}$ 是凸的（Lemma B.2）。损失函数的Lipschitz常数为：

$$
\frac{6 G \kappa_B \kappa^5 W^2 \sqrt{m} h}{\gamma^2} \log^{1/4}\left(\frac{2}{\gamma}\right)
$$

学习率设置为：

$$
\eta = C_2 \sqrt{\frac{\gamma^3}{T m h}}
$$

### 遗憾界与运行时间

OSC算法相对于对角化稳定线性策略类 $\mathcal{S}$ 的遗憾上界为：

$$
\mathrm{Regret}_T(\mathrm{OSC}, \mathcal{S}) = \frac{C_0 C_1 \sqrt{T}}{\gamma^4} \log^3\left(\frac{C_1 T d}{\gamma^3}\right)
$$

其中 $C_1 = G \kappa_B \kappa^8 W^2$。与GPC的 $\tilde{O}(\gamma^{-5.5} \sqrt{T})$ 遗憾界相比，OSC对 $\gamma$ 的依赖从 $\gamma^{-5.5}$ 降低到 $\gamma^{-4}$。

算法的平均运行时间为 $O(\log^4(T/\gamma))$，而GPC的运行时间为 $O(\gamma^{-1} \log T)$。这一改进源于谱表示对扰动历史的压缩，使得参数数量仅与 $\log(T/\gamma)$ 成正比，从而将对 $1/\gamma$ 的依赖从多项式降低到多对数级别。

## 实验与分析

### 主结果：OSC 与 GPC 的性能对比

实验的核心发现是：**OSC 在累积损失上与 GPC 性能相当，但参数数量显著更少**。在 **Figure 2** 的四组对比中，OSC 与 GPC 的累积损失曲线几乎重合，这一结论在以下四种设置下均成立：
- **线性动力学（LDS）**：使用线性头（无隐藏层）时，两者性能相当（Figure 2(a)）。
- **非线性动力学（LDS ReLU）**：系统变为 `x_{t+1} = ReLU(A x_t + B u_t) + w_t`，使用线性头时，OSC 仍与 GPC 持平（Figure 2(c)）。
- **带 MLP 头的设置**：当控制策略头替换为 100 隐藏单元的 MLP 时，OSC 在 LDS（Figure 2(b)）和 LDS ReLU（Figure 2(d)）上均未出现退化，说明谱特征的表达能力足以支撑更复杂的策略头。

**关键参数对比**：GPC 使用最后 50 个扰动作为输入特征（参数数量 50d），而 OSC 仅使用 top-15 Hankel 特征向量（参数数量 15d），参数压缩比超过 3 倍。这一结果直接验证了核心洞察——谱滤波器通过压缩扰动历史，保留了预测所需的结构信息。

### 消融实验与失败模式分析

**（1）状态维度 d 的影响（Figure 3）**
随着状态维度从 2 增加到 20，两种方法的损失均上升，但 OSC 与 GPC 的差距保持稳定。这表明 OSC 对状态空间维度的扩展性良好，其性能退化主要来源于单输入通道对高维状态的控制瓶颈，而非谱表示本身的局限性。

**（2）谱参数数量 h 的影响（Figure 4）**
这是验证谱表示有效性的核心消融：
- **h=5 时**：OSC 已具有竞争力，说明少量谱特征即可捕获系统关键动态。
- **h=20 时**：OSC 性能与 GPC 几乎完全相同，而此时 OSC 的参数数量仅为 GPC 的 40%（20d vs. 50d）。
- **边际收益递减**：当 h 超过 20 后，性能提升趋于饱和，这与理论分析中 h 只需对数级增长（`h = O(log T log(1/γ))`）的结论一致。

![[assets/figures/papers/iclr26_0003_BQIzu1T6F0_A_New_Approach_to_Controlling_Linear_Dynamical_S/figures/010_Figure_4.jpg]]
*Figure 4: Effect of spectral parameters h: even small h gives strong performance, and by h = 20 OSC matches GPC with far fewer parameters*

**（3）系统稳定性裕度 γ 的影响（Figure 5）**
实验通过增大矩阵 A 的特征值（即减小 γ）来模拟更难的边际稳定系统。结果显示：
- 随着 γ 减小，两种方法的损失均上升，但 OSC 在所有 γ 取值下均保持与 GPC 的竞争力。
- 这验证了理论遗憾界中 OSC 对 γ 的依赖（`Õ(γ^{-4} √T)`）虽未超越 GPC（`Õ(γ^{-5.5} √T)`），但在实际中并未导致性能崩溃。

![[assets/figures/papers/iclr26_0003_BQIzu1T6F0_A_New_Approach_to_Controlling_Linear_Dynamical_S/figures/012_Figure_5.jpg]]
*Figure 5: Effect of system stability on performance. Smaller stability margins (larger eigenvalues of A) make the problem harder, but OSC remains competitive with GPC across regimes*

**（4）扰动分布的影响（Figure 6）**
在 Rademacher 随机扰动和正弦结构化扰动两种设置下，OSC 与 GPC 的相对表现一致。这表明谱滤波器的压缩能力不依赖于扰动的统计特性，对对抗性或结构化扰动同样有效。

![[assets/figures/papers/iclr26_0003_BQIzu1T6F0_A_New_Approach_to_Controlling_Linear_Dynamical_S/figures/014_Figure_6.jpg]]
*Figure 6: Effect of disturbance distribution on performance. OSC and GPC exhibit similar relative behavior under random (Rademacher) and structured (sinusoidal) disturbances*

### 实验设置与公平性

所有实验使用相同的优化器（Adam，lr=1e-4，β1=0.9，β2=0.999）和投影到单位球的设置。性能报告为 20 次运行的平均值，并取最后 100 步成本的均值。这些细节确保了对比的公平性，但需注意所有实验均在合成数据上进行，缺乏真实世界控制任务的验证。

### 潜在失败模式与未验证场景

虽然 OSC 在实验中表现稳健，但存在以下未覆盖的失败模式：
1. **理论常数的影响**：遗憾界中的常数 `C_1 = G κ_B κ^8 W^2` 可能很大（见公式 `Regret_T(OSC, S) = (C_0 C_1 √T)/γ^4 log³(...)`），导致实际中需要较长的预热时间才能达到理论性能。实验未报告预热期的表现。
2. **非线性系统的局限性**：仅测试了 ReLU 激活函数，更复杂的非线性（如饱和、摩擦、滞后）未经验证。谱滤波器对非线性的泛化能力尚未建立。
3. **部分可观测性**：算法假设完全状态观测，不适用于 POMDP 设置。在部分可观测系统中，扰动推断步骤（`w_t = x_{t+1} - A x_t - B u_t`）会失效。

### 主要图表结论总结

| 图表 | 核心结论 |
|------|----------|
| Table 1 | OSC 在通用性（对抗扰动、未知成本）和运行时间（`O(log^4(T/γ))`）上优于所有基线 |
| Figure 2 | OSC 与 GPC 在 4 种设置下性能相当，参数减少 3 倍 |
| Figure 4 | h=20 时 OSC 匹配 GPC，验证了谱表示的对数级参数需求 |
| Figure 5 | 在更难的边际稳定系统中，OSC 仍保持竞争力 |

### 补充图表

![[assets/figures/papers/iclr26_0003_BQIzu1T6F0_A_New_Approach_to_Controlling_Linear_Dynamical_S/figures/001_Table_1.jpg]]
*Table 1: where $\gamma$ is the stability margin. The runtime scales only polylogarithmically in 1 / $\gamma$ , , improving on the polynomial dependence of GPC (Agarwal et al., 2019a) via fast online convolution (Agarwal et al., 2024a). Table 1: Comparison of different control methods. The highlighted row corresponds to our proposed approach. In the regret bounds, we hide polylogarithmic factors by the notation ${ \tilde { O } } ( \cdot$ ) . Our method is the only one to perform in the most general setting with the best running time

## 方法谱系与知识库定位

### 与基线的谱系关系

OSC（Online Spectral Control）直接继承并改进了 Agarwal et al. (2019a) 提出的 GPC（Gradient Policy Class）框架。两者的核心共性在于：都将在线控制问题转化为在线凸优化问题，通过参数化策略类并执行在线梯度下降来逼近最优线性策略。关键差异在于策略参数化的底层表示：

- **GPC** 直接对过去 $m$ 个扰动进行线性回归，参数数量为 $O(m n d)$，其中记忆长度 $m = O(\gamma^{-1} \log T)$ 随稳定性裕度 $\gamma$ 的倒数线性增长。
- **OSC** 将扰动与从特定 Hankel 矩阵（公式 2.1）的特征向量构造的谱滤波器进行卷积，再对卷积结果进行线性回归，参数数量仅为 $O(h n d)$，其中 $h = O(\operatorname{polylog}(T/\gamma))$。

这一改变的因果机制是：谱滤波器压缩了扰动历史中的冗余信息，同时保留了与预测最相关的结构（Section 5.1）。Hankel 矩阵 $H_{ij} = (1-\gamma)^{i+j-1}/(i+j-1)$ 的特征值呈指数级衰减（Lemma C.2），使得仅需 $h = O(\log T \log(dT/\gamma^3))$ 个 top 特征向量即可达到足够逼近精度（Theorem 2.1）。

### 计算复杂度的质变

OSC 最显著的贡献是将运行时间对 $1/\gamma$ 的依赖从 **多项式** 降至 **多对数**：

- GPC: $O(\gamma^{-1} \log T)$ 每步
- OSC: $O(\log^4(T/\gamma))$ 每步（Corollary 2.2）

这一质变源于参数数量的压缩：GPC 需要 $m = O(\gamma^{-1} \log T)$ 个历史扰动作为特征，而 OSC 仅需 $h = O(\operatorname{polylog}(T/\gamma))$ 个谱特征。在边际稳定系统（$\gamma$ 很小）中，这一差异从线性增长变为对数增长，理论上使得 OSC 能够处理 GPC 因计算代价过高而无法实际运行的场景。

### 遗憾界的比较

OSC 的遗憾界为 $\tilde{O}(\gamma^{-4} \sqrt{T})$，优于 GPC 的 $\tilde{O}(\gamma^{-5.5} \sqrt{T})$（Table 1）。两者对 $T$ 的依赖相同（$\sqrt{T}$），但 OSC 对 $\gamma$ 的依赖减少了 1.5 个幂次。这一改进的直接来源是谱参数化带来的更紧的 Lipschitz 常数和更小的可行集半径。然而，遗憾界中的常数 $C_1 = G \kappa_B \kappa^8 W^2$ 可能很大（涉及系统范数、控制增益范数等），意味着在短时间范围内，理论优势可能被常数项掩盖。

### 适用边界

OSC 的适用条件与 GPC 基本一致：

1. **系统动力学已知且时不变**：算法假设 $(A, B)$ 已知，实际应用需要先进行系统辨识。
2. **完全状态观测**：不适用于部分可观测系统（POMDP）。
3. **线性或弱非线性系统**：实验仅验证了 ReLU 非线性下的有效性（Figure 2c-d），更复杂的非线性（如饱和、摩擦、迟滞）未经验证。
4. **合成数据验证**：所有实验在合成 LDS 上进行，缺乏真实世界控制任务（如机器人、机械通风）的实证。

### 局限与开放问题

**理论局限**：
- 遗憾界对 $\gamma$ 的依赖（$\gamma^{-4}$）仍然较高，能否降至 $\gamma^{-2}$ 是开放问题（Section E 表明 $\gamma = 1/T^k$ 的设置可大幅降低聚合损失，但理论分析尚未覆盖）。
- 常数 $C_1$ 可能极大，导致实际中需要较长的预热时间才能体现理论优势。
- 算法假设扰动有界（$\|w_t\| \leq W$），对抗性或重尾扰动下的鲁棒性未分析。

**实证局限**：
- 实验仅在 $d \leq 20$ 的低维系统上测试（Figure 3），高维系统（如 $d > 100$）的性能未知。
- 谱滤波器数量 $h$ 在 $h=20$ 时即与 GPC 性能相当（Figure 4），但 $h$ 的自动选择机制未提供。
- 与 GPC 的性能对比仅在合成数据上进行，且两者在多数设置下性能相当而非显著优于（Figure 2），OSC 的核心优势在于计算效率而非控制精度。

**开放问题**：
1. **非线性扩展**：谱滤波方法能否与 CNN、Transformer 等更强大的架构结合处理复杂非线性？
2. **部分可观测**：能否将谱表示扩展到 POMDP 设置，利用观测历史而非完整状态？
3. **未知动力学**：是否需要联合进行系统辨识与在线控制，以及谱表示在此场景下的稳定性？
4. **时变系统**：算法假设时不变动力学，对抗性或时变系统下的适用性未分析。
5. **真实世界验证**：在机器人控制、机械通风等真实任务中的实证性能是下一步关键。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_New_Approach_to_Controlling_Linear_Dynamical_Systems.pdf

![[paperPDFs/ICLR_2026/A_New_Approach_to_Controlling_Linear_Dynamical_Systems.pdf]]
