---
title: "(U)NFV: (Un)Supervised Neural Finite Volume Methods for Solving Hyperbolic PDEs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/UNFV_UnSupervised_Neural_Finite_Volume_Methods_for_Solving_Hyperbolic_PDEs.pdf
project_link: https://www.nathanlichtle.com/research/nfv
code_link: null
aliases:
- UNNFV
- UNUSNFVMSHP
- "(U)NFV (Neural Finite Volume)"
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/algorithms
core_operator: "用轻量级神经网络替代手工设计的数值通量函数，同时保留经典FV更新规则以保证守恒性。通过扩展时空模板（a×b），网络可以学习更复杂的通量近似，而无需手动设计高阶重构。"
primary_logic: "将神经网络嵌入有限体积框架的守恒更新规则中，可以在保持守恒性和实现简单性的同时，通过学习扩展时空模板上的数值通量，显著提升对双曲守恒律中激波和间断的捕捉精度。"
claims:
- "NFV_2^1在Greenshields通量上达到1.3e-4的L2误差，优于Godunov (4.5e-4)、Lax-Friedrichs (1.3e-2)和Engquist-Osher (4.5e-4)。"
- "NFV_4^5在Burgers方程上达到2.2e-4的L2误差，比Godunov (8.3e-4)和WENO (6.4e-4)低一个数量级，接近DG (3.1e-5)。"
- "NFV_10^11在I-24高速公路现场数据上，在7个未见过的测试日上均优于Godunov，L1误差为1.12e-1，L2误差为2.20e-2。"
- "NFV_4^5能准确捕捉Burgers方程和LWR三角通量中的间断和不可微点，而Godunov方案则过度平滑。"
---

# (U)NFV: (Un)Supervised Neural Finite Volume Methods for Solving Hyperbolic PDEs

> [!tip] 核心洞察
> 将神经网络嵌入有限体积框架的守恒更新规则中，可以在保持守恒性和实现简单性的同时，通过学习扩展时空模板上的数值通量，显著提升对双曲守恒律中激波和间断的捕捉精度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | (U)NFV：用于求解双曲型偏微分方程的（无）监督神经有限体积方法 |
| 英文题名 | (U)NFV: (Un)Supervised Neural Finite Volume Methods for Solving Hyperbolic PDEs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=AhtDnPyfOE) · [Project](https://nathanlichtle.com/research/nfv) · [Project](https://www.nathanlichtle.com/research/nfv) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/algorithms |
| Method | (U)NFV (Neural Finite Volume) |
| Dataset | Greenshields LWR, Triangular 1 LWR, Burgers |

> [!tip] 效果简介
> - Greenshields LWR 上，L2误差 为 1.3e-4 (NFV_2^1)，对比 4.5e-4 (Godunov)，变化 降低约3.5倍。
> - Triangular 1 LWR 上，L2误差 为 1.4e-3 (NFV_2^1)，对比 2.3e-3 (Godunov)，变化 降低约1.6倍。
> - Burgers 上，L2误差 为 2.2e-4 (NFV_4^5)，对比 8.3e-4 (Godunov)，变化 降低约3.8倍。

## 概要

本文提出神经有限体积方法（NFV），旨在解决传统有限体积方法在精度与实现复杂度之间的根本性权衡：高阶格式（如WENO、DG）精度高但实现复杂、计算成本高；低阶格式（如Godunov）实现简单但数值耗散严重，无法准确捕捉激波和间断。核心思路是将轻量级2D CNN嵌入经典FV守恒更新规则中，用神经网络替代手工设计的数值通量函数，从而在保持守恒性和实现简单性的同时，通过学习扩展的a×b时空模板上的通量近似，显著提升对双曲守恒律中激波和间断的捕捉精度。

主要结果包括：在Greenshields通量上，NFV_2^1的L2误差（1.3e-4）比Godunov（4.5e-4）降低约3.5倍；在Burgers方程上，NFV_4^5的L2误差（2.2e-4）比Godunov（8.3e-4）和WENO（6.4e-4）低一个数量级，接近DG（3.1e-5）。在I-24高速公路现场数据上，NFV_10^11在7个未见过的测试日上均优于Godunov拟合，L1误差降低约18%，L2误差降低约22%。方法同时支持监督学习（基于解数据）和无监督学习（基于弱形式残差损失），后者在无参考解时仍能有效训练。

双曲守恒律方程 $\partial_t u(x,t) + \partial_x f(u(x,t)) = 0$ 是描述激波、交通流等间断现象的核心数学模型，其数值求解长期面临根本性权衡：高阶格式（如WENO、不连续伽辽金法DG）精度高但实现复杂、计算成本高；低阶格式（如Godunov、Lax-Friedrichs）实现简单但数值耗散严重，无法准确捕捉激波和间断。传统有限体积方法的核心瓶颈在于，其数值通量函数 $F_{i+1/2}^n$ 必须手工设计——一阶通量（如Godunov）仅依赖相邻单元，精度受限；高阶重构（如WENO）虽能提升精度，却引入复杂的非线性权重计算和额外的实现复杂度。

现有机器学习求解器尝试用神经网络端到端替代整个数值求解器，但往往牺牲守恒性这一关键物理约束，导致长期预测发散。本文的因果杠杆在于：**保留经典有限体积更新规则 $u_i^{n+1} = u_i^n - (\Delta t / \Delta x)(F_{i+1/2}^n - F_{i-1/2}^n)$ 以确保质量守恒，仅用轻量级2D CNN神经网络替换手工设计的数值通量函数**。核心洞察是，通过扩展时空模板（$a \times b$，即 $a$ 个空间单元 $\times$ $b$ 个过去时间步），网络可以学习更复杂的通量近似，而无需手动设计高阶重构——这种结构约束（嵌入FV框架）同时保证了守恒性和实现简单性。

具体而言，该方法（Neural Finite Volume, NFV）将数值通量估计定义为 $\hat{F}_{i \pm 1/2}^n = \mathcal{N}(\mathbf{u}_{i \pm 1/2}^n(a, b))$，其中 $\mathcal{N}$ 是一个仅含6个隐藏层（每层15个神经元）的2D CNN，参数量仅为 $1105 + 16(ab + 1)$。NFV支持两种训练范式：监督学习（基于参考解的最小二乘损失 $\mathcal{L}_s = \mathbb{E}_{u_0 \sim \mathcal{R}} ||u - \hat{u}||_2^2$）和无监督学习（基于弱形式残差损失 $\mathcal{L}_w$ 直接从PDE学习，无需解数据）。这一设计填补了现有方法在"保持FV框架简单性的同时提升精度"的缺口。

## 核心方法与创新机理

(U)NFV 的核心创新在于**用轻量级神经网络替代手工设计的数值通量函数，同时严格保留经典有限体积（FV）方法的守恒更新规则**。这一设计直接针对传统 FV 方法在精度与实现复杂度之间的根本性权衡：高阶格式（如 WENO、DG）精度高但实现复杂、计算成本高；低阶格式（如 Godunov）实现简单但数值耗散严重，无法准确捕捉激波和间断。

**改变的组件（Changed Slots）**：

1.  **数值通量近似函数**：从手工设计的解析函数（如 Godunov 通量、Lax-Friedrichs 通量）替换为**轻量级 2D CNN 神经网络**。该网络基于局部 $a \times b$ 的时空模板（$a$ 个空间单元 × $b$ 个过去时间步）来预测数值通量 $\hat{F}_{i \pm 1/2}^n = \mathcal{N}(\mathbf{u}_{i \pm 1/2}^n(a, b))$。这使得网络能够学习比手工设计更复杂的通量近似，而无需手动设计高阶重构。

2.  **时空模板大小**：从传统 FV 方法通常使用的 $2 \times 1$（如 Godunov）或少量空间单元 × 1 个时间步，扩展为可配置的 $a \times b$ 模板，实验范围从 $2 \times 1$ 到 $10 \times 11$。更大的模板为网络提供了更丰富的局部时空上下文信息，是提升精度的关键杠杆。

3.  **训练方式**：从无训练的解析方法，变为支持**监督学习**（基于参考解数据的最小二乘损失 $\mathcal{L}_s = \mathbb{E}_{u_0 \sim \mathcal{R}} ||u - \hat{u}||_2^2$）和**无监督学习**（基于 PDE 弱形式残差损失 $\mathcal{L}_w$）两种方式。无监督版本（UNFV）无需真实解即可训练，拓宽了应用场景。

**不变的组件**：NFV 严格遵循经典 FV 的更新规则 $u_i^{n+1} = u_i^n - (\Delta t / \Delta x)(F_{i+1/2}^n - F_{i-1/2}^n)$，从而**确保质量守恒**。这保证了其解在物理上的可解释性和数值稳定性。

**决定性证据**：

*   在 Greenshields 通量上，NFV$_2^1$ 的 L2 误差（1.3e-4）比 Godunov（4.5e-4）低约 3.5 倍（Table 1）。
*   在 Burgers 方程上，NFV$_4^5$ 的 L2 误差（2.2e-4）比 Godunov（8.3e-4）和 WENO（6.4e-4）低一个数量级，接近 DG（3.1e-5）（Table 2）。
*   在 I-24 高速公路现场数据上，NFV$_{10}^{11}$ 在 7 个未见过的测试日上均优于 Godunov，L1 误差为 1.12e-1，L2 误差为 2.20e-2（Table 5）。
*   定性上，NFV$_4^5$ 能准确捕捉 Burgers 方程和 LWR 三角通量中的间断和不可微点，而 Godunov 方案则严重过度平滑（Figure 4）。

**因果机制**：传统 FV 方法的精度受限于手工通量函数的表达能力。NFV 通过神经网络学习通量，打破了这一瓶颈。更大的时空模板（$a \times b$）为网络提供了更多局部信息，使其能隐式地近似高阶重构，从而在保持 FV 框架简单性和守恒性的同时，显著提升了对激波和间断的捕捉精度。消融实验证实，NFV 模型对 CFL 比率变化更鲁棒，且在更粗网格上也能保持较低误差（Table 3, Figure 5）。

![[assets/figures/papers/iclr26_0001_AhtDnPyfOE_UNFV_UnSupervised_Neural_Finite_Volume_Methods_f/figures/007_Figure_4.jpg]]
*Figure 4: Comparison of the final density of the Burgers’ equation (left) and LWR triangular equation (right) for $\mathrm { N F V _ { 4 } ^ { 5 } }$ and the Godunov Scheme. The proposed method displays an excellent approximation of the exact solution, capturing sharp features such as discontinuities and points of non-differentiability. It contains some minor oscillations in the solution, which are not present in the Godunov scheme. The latter, however, fails to capture the discontinuities and points of non-differentiability, offering a very smoothed solution*

(U)NFV 的核心设计思路是**将轻量级神经网络嵌入经典有限体积（FV）方法的守恒更新规则中**，用数据驱动的通量近似替代手工设计的数值通量函数，从而在保持守恒性和实现简单性的同时，显著提升对双曲守恒律中激波和间断的捕捉精度。

**Pipeline 与模块关系**：整个框架由两个紧密耦合的模块构成。第一个模块是**神经网络通量估计器**，它是一个轻量级的 2D CNN，基于局部的 $a \times b$ 时空模板（$a$ 个空间单元 $\times$ $b$ 个过去时间步）来预测单元边界上的数值通量 $\hat{F}_{i \pm 1/2}^n$。第二个模块是**FV 守恒更新规则**，它接收估计出的通量，并严格按照经典 FV 公式 $u_i^{n+1} = u_i^n - (\Delta t / \Delta x)(\hat{F}_{i+1/2}^n - \hat{F}_{i-1/2}^n)$ 更新单元平均值，从而确保质量守恒。这种“神经网络预测通量 + FV 规则更新状态”的架构，使得模型在推理时以自回归方式运行：每个时间步，网络基于当前和过去的局部状态预测通量，FV 规则则利用这些通量计算出下一时间步的解。

**输入输出流**：输入是当前时刻及过去 $b-1$ 个时间步的局部 $a$ 个空间单元的密度/状态值（即 $a \times b$ 的时空模板）。输出是预测的数值通量，该通量被 FV 更新规则用来计算下一时间步的解。在自回归预测中，模型输出的解会作为下一时间步的输入的一部分。

**关键变化**：该方法改变了传统 FV 方法中“手工设计的解析通量函数”这一核心组件。通过将模板大小从 Godunov 的 $2 \times 1$ 扩展到 $10 \times 11$，网络能够学习到更复杂的、非局部的通量近似，从而在保持 FV 方法简单性的同时，获得接近甚至超越高阶方法（如 WENO、DG）的精度。此外，该方法支持两种训练范式：**监督学习（NFV）**，直接最小化预测解与参考解之间的均方误差；**无监督学习（UNFV）**，通过最小化 PDE 弱形式残差来训练，无需参考解。

### 1. 背景：守恒律与有限体积框架

(U)NFV 方法旨在求解一维标量双曲守恒律，其一般形式为：

$$\partial _ { t } u ( x , t ) + \partial _ { x } f ( u ( x , t ) ) = 0$$

其中 $u(x,t)$ 是守恒量（如交通流中的车辆密度），$f(u)$ 是通量函数（如流量）。

有限体积（FV）方法的核心是将计算域划分为单元 $I_i = [x_{i-1/2}, x_{i+1/2}]$，并追踪每个单元上的平均值：

$$u _ { i } ^ { n } = \frac { 1 } { \Delta x } \int _ { I _ { i } } u ( t _ { n } , x ) \mathrm { d } x$$

数值通量 $F_{i+1/2}^n$ 定义为单元边界 $x_{i+1/2}$ 上从 $t_n$ 到 $t_{n+1}$ 的通量时间积分：

$$F _ { i + 1 / 2 } ^ { n } = \int _ { t _ { n } } ^ { t _ { n + 1 } } f ( u ( t , x _ { i + 1 / 2 } ) ) \mathrm { d } t$$

FV 方法的精确守恒更新规则为：

$$u _ { i } ^ { n + 1 } = u _ { i } ^ { n } - \frac { \Delta t } { \Delta x } \left( F _ { { i + 1 } / { 2 } } ^ { n } - F _ { { i - 1 } / { 2 } } ^ { n } \right)$$

该公式保证了质量守恒，是 (U)NFV 方法不可改变的基石。

### 2. 核心创新：神经通量估计器

传统 FV 方法（如 Godunov、Lax-Friedrichs）使用手工设计的解析函数来近似数值通量 $F_{i+1/2}^n$。这些函数的推导依赖于对局部黎曼问题的精确或近似求解，其精度与实现复杂度之间存在根本性权衡。

(U)NFV 的核心洞察是：**用一个轻量级神经网络替代手工设计的通量函数**。该网络基于一个局部的 **$a \times b$ 时空模板**（$a$ 个空间单元 × $b$ 个过去时间步）来预测数值通量：

$$\hat { F } _ { i \pm 1 / 2 } ^ { n } = \mathcal { N } ( \pmb { u } _ { i \pm 1 / 2 } ^ { n } ( a , b ) )$$

其中 $\mathcal{N}$ 是一个二维 CNN，输入 $\pmb{u}_{i\pm1/2}^n(a,b)$ 是从 $a$ 个空间单元和 $b$ 个时间步中提取的局部解场。例如，$a=4, b=2$ 的模板（记作 $\mathrm{FV}_4^2$）会输入 2 个时间步 × 4 个空间单元共 8 个值。通过扩展模板尺寸（从匹配 Godunov 的 $2\times1$ 到 $10\times11$），网络能够学习到比任何手工设计格式更丰富的时空相关性。

### 3. 模型架构与参数量

NFV 模型架构是一个轻量级 2D CNN，由 6 个隐藏层组成，每层宽度为 15。对于模板尺寸为 $a \times b$ 的 NFV$_a^b$ 模型，其可训练参数总数为：

$$1105 + 16(ab + 1)$$

例如，NFV$_2^1$（与 Godunov 模板相同）的参数仅为 $1105 + 16(2\times1+1) = 1153$ 个；NFV$_{10}^{11}$ 的参数为 $1105 + 16(10\times11+1) = 2881$ 个。这种极低的参数量使得 NFV 在推理时的计算成本与 Godunov 方法相当（仅常数因子差异），远低于高阶方法如 WENO 和 DG。

### 4. 训练目标：监督与无监督

(U)NFV 提供两种训练范式：

**监督学习（NFV）**：使用参考解数据训练，最小化预测解与真实解之间的均方误差：

$$\mathcal { L } _ { s } = \underset { u _ { 0 } \sim \mathcal { R } } { \mathbb { E } } | | u - \hat { u } | | _ { 2 } ^ { 2 }$$

其中 $\mathcal{R}$ 是初始条件的分布。

**无监督学习（UNFV）**：无需参考解，直接利用 PDE 的弱形式残差作为损失函数。这通过最小化弱形式残差的平方和来实现：

$$\mathcal { L } _ { w } = \underset { \underset { u _ { 0 } \sim \mathcal { R } } { v \in \Phi } } { \mathbb { E } } \left[ \sum _ { n = 1 } ^ { N } \left( \sum _ { i = 1 } ^ { I _ { \operatorname* { m a x } } } \left( ( \Delta t ) ^ { - 1 } ( \hat { u } _ { i } ^ { n } - \hat { u } _ { i } ^ { n - 1 } ) \int _ { I _ { i } } \varphi + f ( \hat { u } _ { i } ^ { n } ) [ \varphi ] _ { x _ { i - 1 / 2 } } ^ { x _ { i + 1 / 2 } } \right) \right) ^ { 2 } \right]$$

其中 $\varphi$ 是测试函数族（如多项式、三角函数），$\Phi$ 是测试函数空间。该损失函数强制网络输出满足 PDE 的弱形式，从而在无标签数据下也能学习到物理一致的解。

### 5. 关键公式与变量含义总结

| 公式 | 含义 | 关键变量 |
|------|------|----------|
| $\partial_t u + \partial_x f(u) = 0$ | 一维标量守恒律 | $u$: 守恒量, $f$: 通量函数 |
| $u_i^n = \frac{1}{\Delta x} \int_{I_i} u(t_n,x) dx$ | 单元平均值 | $i$: 空间索引, $n$: 时间索引 |
| $u_i^{n+1} = u_i^n - \frac{\Delta t}{\Delta x}(F_{i+1/2}^n - F_{i-1/2}^n)$ | FV 守恒更新规则 | $\Delta t, \Delta x$: 时空步长 |
| $\hat{F}_{i\pm1/2}^n = \mathcal{N}(\pmb{u}_{i\pm1/2}^n(a,b))$ | NFV 神经通量估计 | $a,b$: 时空模板尺寸 |
| $1105 + 16(ab+1)$ | NFV 模型参数量 | — |

### 6. 方法的核心机制总结

(U)NFV 方法的因果机制可概括为：
- **瓶颈**：传统 FV 方法的精度受限于手工通量函数的表达能力，高阶格式（WENO, DG）虽精度高但实现复杂、计算成本高。
- **旋钮**：用轻量级 CNN 替代手工通量函数，同时保留 FV 守恒更新规则。通过调整时空模板尺寸 $a \times b$，可以平滑地控制模型容量和表达能力的权衡。
- **效果**：在保持 FV 方法简单性、守恒性和低计算成本的同时，显著提升了对激波和间断的捕捉精度。监督版本（NFV）在标签充足时表现最佳；无监督版本（UNFV）在无标签场景下仍能通过物理约束学习，且经验上收敛到熵解（尽管缺乏理论保证）。

## 实验与关键发现

### 主要结果：合成基准上的精度提升

(U)NFV 的核心实验在七个一维双曲守恒律基准上进行，评估集包含 1000 个分段常数初始条件。**表 1** 展示了关键对比：在 Greenshields 通量的 LWR 方程上，`NFV_2^1` 的 L2 误差为 `1.3e-4`，显著低于 Godunov (`4.5e-4`)、Lax-Friedrichs (`1.3e-2`) 和 Engquist-Osher (`4.5e-4`)。这一精度提升约 3.5 倍，且是在与 Godunov 完全相同的 2×1 时空模板下实现的，仅将手工设计的通量函数替换为轻量级神经网络。在 Triangular 1 和 Triangular 2 通量上，`NFV_2^1` 同样取得最低的一阶 FV 误差（分别为 `1.4e-3` 和 `2.4e-3`），验证了方法在不同通量函数上的鲁棒性。

![[assets/figures/papers/iclr26_0001_AhtDnPyfOE_UNFV_UnSupervised_Neural_Finite_Volume_Methods_f/figures/003_Table_1.jpg]]
*Table 1: Performance comparison between neural network models and classical numerical schemes. Results are computed over the evaluation set of 1000 piecewise constant initial conditions. For each method, we report mean and standard deviation in $L _ { 2 }$ norm (mean ( ( u - $\hat { u } ) ^ { 2 }$ ) , )*

**表 2** 进一步展示了扩展模板的潜力：`NFV_4^5` 在 Burgers 方程上达到 `2.2e-4` 的 L2 误差，比 Godunov (`8.3e-4`) 低约 3.8 倍，比高阶 WENO (`6.4e-4`) 低约 2.9 倍，性能接近不连续伽辽金 (DG) 方法 (`3.1e-5`)。这一结果的关键在于，`NFV_4^5` 在保持有限体积方法实现简单性和守恒性的同时，通过 4×5 的时空模板学习了更复杂的通量近似，从而大幅降低了数值耗散。

![[assets/figures/papers/iclr26_0001_AhtDnPyfOE_UNFV_UnSupervised_Neural_Finite_Volume_Methods_f/figures/008_Table_2.jpg]]
*Table 2: Evaluation of $\mathrm { N F V _ { 4 } ^ { 5 } }$ using piecewise constant initial conditions. Error is reported in $L _ { 2 }$ norm. NFV54 achieves outstanding performance, gaining up to an order of magnitude improvement compared to Godunov and WENO. Its performance is close to DG, while keeping the implementation simplicity of a finite volume method and the computational complexity of NFV*

**图 4** 提供了定性证据：在 Burgers 方程和 LWR 三角通量的最终密度对比中，`NFV_4^5` 能够准确捕捉激波和不可微点，而 Godunov 方案则严重过度平滑。值得注意的是，NFV 在间断附近会产生轻微振荡，这是其与 Godunov 方案的一个差异点，也是当前方法的一个已知限制。

### 消融与鲁棒性分析

**CFL 比率消融（表 3）**：`NFV_2^1` 和 `UNFV_2^1` 在所有测试的 CFL 比率下均一致优于 Godunov，且误差的标准差更小，表明其对时间步长变化更鲁棒。这一优势源于神经网络学习到的通量近似对数值稳定性条件的适应性更强。

![[assets/figures/papers/iclr26_0001_AhtDnPyfOE_UNFV_UnSupervised_Neural_Finite_Volume_Methods_f/figures/010_Table_3.jpg]]
*Table 3: Mean and standard deviation of final-time $L _ { 2 }$ error on the standard LWR benchmark with Greenshields’ flux for different CFL ratios, comparing $\mathrm { N F V _ { 2 } ^ { 1 } }$ with classical finite volume baselines and DG*

**网格收敛性（图 5）**：`NFV_2^1` 在训练网格（Δx=1/200）上训练后，在更细的网格上评估时仍能保持较低的 L2 误差，显示出良好的网格泛化能力。这一特性在实际应用中至关重要，因为模型可以在粗网格上高效训练，然后部署到更精细的网格上。

**模型容量扩展**：从 `NFV_2^1` 扩展到 `NFV_10^11` 仅增加 1728 个参数（总参数量公式为 `1105 + 16(ab + 1)`），但精度显著提升。这一近线性的参数增长与性能提升表明，NFV 框架能够自然地通过扩展时空模板来增加模型容量。

### 现场数据验证：I-24 高速公路

**表 4** 展示了 NFV 在 I-24 MOTION 现场数据上的表现。所有模型（包括 Godunov 拟合）均使用相同的第一小时数据（2022 年 11 月 29 日）进行训练/拟合。`NFV_2^1` 在所有指标上均优于所有经过通量函数拟合的 Godunov 变体，尽管输入大小和底层结构相同。随着模板增大，性能持续提升：`NFV_10^11` 在训练日上达到 L1 误差 `1.12e-1`，L2 误差 `2.20e-2`。

![[assets/figures/papers/iclr26_0001_AhtDnPyfOE_UNFV_UnSupervised_Neural_Finite_Volume_Methods_f/figures/011_Table_4.jpg]]
*Table 4: Improvements of NFV at different scales against numerical methods with fitted flow functions on field data. The reported metrics include L1 error (mean(|u − uˆ|)), L2 error (mean ( u - $\hat { u } ) ^ { 2 }$ ) , ), and relative error (mean ( | u - $\hat { u }$ | / | $\operatorname$* { m a x } $\{ \varepsilon$ , u $\}$ | ) ) ). The larger the input size of NFV, the better the performance. $\mathrm { N F V _ { 2 } ^ { 1 } }$ outperforms all calibrated Godunov fits, despite having the same input size and underlying structure

**泛化测试（表 5）**：这是最严格的评估——在 7 个完全未见过的测试日上比较 `NFV_10^11` 与最佳 Godunov 拟合。NFV 在所有 7 天中均一致优于 Godunov，平均 L1 误差为 `1.12e-1`（Godunov 为 `1.37e-1`），平均 L2 误差为 `2.20e-2`（Godunov 为 `2.83e-2`），相对误差降低约 18-22%。这一结果的关键意义在于：NFV 仅从 1 小时的训练数据中学习，就能泛化到不同日期、不同交通模式的全新场景，而 Godunov 拟合即使经过校准也无法达到同等泛化能力。

**图 6** 和 **图 13** 的可视化分析揭示了 NFV 的优势来源：`NFV_10^11` 能够捕捉更多停-走波（红色区域）和快速低密度波（绿色区域），从而正确预测最后两个波动的早期消散。然而，在预测窗口末期出现振荡，这被归因于训练数据中低密度（深绿色）模式的稀缺导致的泛化不足——这一限制在实验数据建模中是可以接受的，因为主要目标是准确捕捉拥堵波的演化。

### 失败模式与限制

1. **间断附近的振荡**：如 **图 4** 所示，NFV 在捕捉间断时会产生轻微振荡，而 Godunov 方案则没有此问题。这是神经网络近似不连续通量时的固有问题，也是未来工作的重要方向。
2. **无监督 UNFV 的理论保证**：虽然 `UNFV_2^1` 在经验上收敛到熵解，但理论上并未保证。这一点的确需要手动验证，因为弱形式损失可能无法唯一确定熵解。
3. **数据稀缺下的泛化**：在 I-24 实验中，`NFV_10^11` 在预测窗口末期出现振荡，提示当前训练数据中某些模式（如极低密度）的稀疏性限制了模型的泛化能力。
4. **一维标量限制**：当前方法仅针对一维标量守恒律验证，尚未扩展到多维系统或方程组（如欧拉方程），这是最关键的开放问题。

### 计算效率

在推理时，NFV 的运行时间在 Godunov 的一个小常数因子内，大约是 ENO 和 WENO 的两倍快，比 DG 快一个数量级以上。训练在 RTX A5000 GPU 上约需 30 分钟，模型通常在几分钟内就超越 Godunov 基线，15 分钟内达到大部分最终性能（**图 15**）。这一效率使得 NFV 在实际应用中具有可行性。

![[assets/figures/papers/iclr26_0001_AhtDnPyfOE_UNFV_UnSupervised_Neural_Finite_Volume_Methods_f/figures/002_Figure_2.jpg]]
*Figure 2: Example stencil for $\mathrm { F V } _ { 4 } ^ { 2 }$ . , taking in a stencil of 2 time steps times 4 space cells*

## 定位与知识库关联

### 与Baseline/Follow-up的关系

(U)NFV方法的核心创新在于用轻量级2D CNN替代经典有限体积（FV）方法中手工设计的数值通量函数，同时保留FV守恒更新规则 $u_i^{n+1} = u_i^n - (\Delta t/\Delta x)(F_{i+1/2}^n - F_{i-1/2}^n)$ 以确保质量守恒。这一设计直接针对传统方法的核心瓶颈：高阶格式（如WENO、DG）精度高但实现复杂、计算成本高；低阶格式（如Godunov）实现简单但数值耗散严重，无法准确捕捉激波和间断。

在基准对比中，NFV_2^1（使用与Godunov相同的2×1时空模板）在Greenshields通量上L2误差为1.3e-4，较Godunov（4.5e-4）降低约3.5倍；在Triangular 1上为1.4e-3，较Godunov（2.3e-3）降低约1.6倍。NFV_4^5在Burgers方程上达到2.2e-4，比Godunov（8.3e-4）和WENO（6.4e-4）低一个数量级，接近DG（3.1e-5）。在I-24高速公路现场数据上，NFV_10^11在7个未见过的测试日上L1误差为1.12e-1，L2误差为2.20e-2，均优于拟合通量的Godunov方案。

方法支持监督学习（NFV）和无监督学习（UNFV）两种训练方式。无监督变体通过弱形式残差损失直接从PDE学习，无需参考解，这对缺乏精确解的实际场景具有重要意义。NFV模型在推理时与Godunov的计算成本相当（常数因子内），远低于WENO和DG。

### 适用边界

该方法目前仅针对一维标量守恒律进行了验证，包括LWR交通流模型（六种通量函数）和Burgers方程。时空模板大小可扩展至10×11（11个空间单元×11个过去时间步），模型参数量为1105 + 16(ab + 1)。在网格泛化上，NFV在更粗的网格上也能保持较低误差，且对CFL比率变化比Godunov更鲁棒。

### 局限与开放问题

**已知局限：**
1. NFV_10^11在I-24数据预测窗口末期出现振荡，可能源于训练数据中低密度模式稀缺导致的泛化不足。
2. 无监督UNFV虽然经验上收敛到熵解，但理论上并未保证收敛到熵解。
3. 当前方法仅针对一维标量守恒律验证，尚未扩展到多维系统或方程组。
4. NFV在捕捉间断时会产生轻微振荡，而Godunov方案则无此问题。
5. I-24实验中NFV仅使用单个边界单元，更大模型可能从更多上下文信息中受益。

**开放问题：**
- 如何将(U)NFV扩展到多维双曲守恒律系统（如欧拉方程）？
- 无监督UNFV收敛到熵解的理论保证是什么？
- 如何进一步减少NFV在间断附近产生的轻微振荡？
- NFV在速度公式化（学习速度-通量关系）上的表现如何？
- 不同测试函数族（超越多项式）对无监督学习的影响是什么？
- 更大模板尺寸(a)或更多输入通道(b)对未见交通模式的泛化有何影响？

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/UNFV_UnSupervised_Neural_Finite_Volume_Methods_for_Solving_Hyperbolic_PDEs.pdf

![[paperPDFs/ICLR_2026/UNFV_UnSupervised_Neural_Finite_Volume_Methods_for_Solving_Hyperbolic_PDEs.pdf]]
