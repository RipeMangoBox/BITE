---
title: "A Two-Phase Deep Learning Framework for Adaptive Time-Stepping in High-Speed Flow Modeling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Two_Phase_Deep_Learning_Framework_for_Adaptive_Time_Stepping_in_High_Speed_Flow_Modeling.pdf
aliases:
- TPDLFATSHSFM
- ShockCast
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "引入一个神经CFL模型，从当前流场状态及其物理特征中预测自适应时间步大小，从而为神经求解器提供动态步长。"
primary_logic: "通过学习一个基于流场状态的Δₜ预测器，并使神经求解器以该步长为条件，能够使一阶训练目标的难度分布更加均匀，减少训练方差，提升在高速流中的稳定性和泛化能力。"
claims:
- "ShockCast采用两阶段框架：第一阶段预测Δₜ，第二阶段用预测的Δₜ推进系统状态。"
- "神经CFL模型将空间梯度和物理CFL特征（局部波速、速度幅值、声速）作为输入，并使用最大池化下采样来模拟CFL行为。"
- "按照速率变化反比例缩放Δₜ可以使训练对的难度分布更均匀，特别适用于梯度锐利程度差异大的高速流。"
- "Circular Blast (evaluation split) 上 Correlation Proportion ×10⁻² (↑) = 98.34 (0.26)"
---

# A Two-Phase Deep Learning Framework for Adaptive Time-Stepping in High-Speed Flow Modeling

> [!tip] 核心洞察
> 通过学习一个基于流场状态的Δₜ预测器，并使神经求解器以该步长为条件，能够使一阶训练目标的难度分布更加均匀，减少训练方差，提升在高速流中的稳定性和泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 高速流建模中自适应时间步进的两阶段深度学习框架 |
| 英文题名 | A Two-Phase Deep Learning Framework for Adaptive Time-Stepping in High-Speed Flow Modeling |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=d4gzLgGl7I); [GitHub](https://github.com/divelab/AIRS); [Project](https://huggingface.co/divelab) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | ShockCast |
| Dataset | Circular Blast (evaluation split), Coal Dust Explosion (evaluation split) |

> [!tip] 效果简介
> - Circular Blast (evaluation split) 上，Correlation Proportion ×10⁻² (↑) 为 98.34 (0.26)，对比 ≈98.38 (Oracle with ground-truth Δt, inferred from difference)，变化 -0.04 (×10⁻²)。
> - Coal Dust Explosion (evaluation split) 上，Solution time (s) on GPU 为 2.15 ± 0.07 (CNO Affine, GPU)，对比 67,441 (mean, classical solver on 16 CPU cores)，变化 超过四个数量级的加速。
> - Coal Dust Explosion (evaluation split) 上，Turbulence Kinetic Energy Relative Error ×10⁻² (↓) 为 8.91 ± 0.16 (U-Net MoE)，对比 9.85 ± 0.24 (U-Net Affine)，变化 -0.94。

## 概述

高速流模拟中，激波等局部梯度极陡的区域要求使用极小的时间步长以保证数值稳定性。传统方法采用均匀时间步时，必须全程依赖由最严酷区域决定的最小步长，导致巨大的计算代价。基于神经算子的替代求解器虽然能够降低计算开销，但其通常使用粗化时空网格和部分物理变量，经典 Courant‑Friedrichs‑Lewy (CFL) 条件无法直接为其确定合适的步长，从而限制了一阶训练目标的均匀性和模型的泛化能力。

为应对上述瓶颈，本文提出 ShockCast，一种面向高速流建模的自适应时间步进两阶段深度学习框架。其核心思想是通过一个神经 CFL 模型从当前流场状态中预测自适应时间步 $\Delta_t$，再将该预测步长作为条件输入驱动时间条件神经求解器完成状态推进，使得训练目标中的难度分布更加均衡，降低训练方差。第一阶段，神经 CFL 模型以空间梯度、局部波速、速度幅值和声速等物理特征作为输入，并采用最大池化下采样模拟 CFL 条件中的最大值操作，从而学习出与流场变化速率反比例缩放的步长。第二阶段，时间条件神经求解器以当前流场和预测的 $\Delta_t$ 为输入，通过 Affine、Euler 或 Mixture‑of‑Experts (MoE) 条件化策略将系统状态向前演化。整个框架可搭配多种神经算子主干（如 CNO、F‑FNO、U‑Net、Transolver），且训练与推理流程清晰分步。

实验表明，ShockCast 在圆形爆炸和煤尘爆炸等高速流基准上显著加速：在 GPU 上的推理时间较经典 16 核 CPU 求解器加快逾四个数量级，同时保持高质量预测，湍流动能相对误差和平均流相对误差较纯 Affine 条件基线均有明显下降，质量守恒误差控制在初始质量的 0.2% 以内。神经 CFL 模型预测的 $\Delta_t$ 与真实时间步的关联时间比例与使用真实步长的 Oracle 上限极为接近，验证了自适应步长预测的有效性。这些结果说明，通过将时间步预测与状态演化解耦且互为条件，ShockCast 能够在保证精度的前提下大幅降低高速流神经模拟的计算成本，并提升模型在不同尖锐度梯度区域上的泛化性能。

## 背景与动机

高速流动（如激波、爆轰波）在空间上形成局部极陡的梯度，经典数值方法必须在该区域使时间步长大幅收缩以满足 CFL 稳定性条件  
$$\Delta t \leq \frac{C}{\lambda_{\max}} \min_{x,y}(\Delta x, \Delta y), \quad \lambda_{\max} := \max_{x,y} \lambda(x,y), \quad \lambda(x,y) := \max\left( |u(x,y)| + a(x,y), |v(x,y)| + a(x,y) \right).$$  
若采用均匀时间步，则全程被迫使用激波区的极小步长，导致计算代价极高。传统自适应步长方法可以直接利用全量物理场和高分辨率网格计算 $\lambda_{\max}$ 来动态调整 $\Delta t$，但这一策略无法直接迁移到数据驱动的神经代理模型——后者通常仅输入粗化的时空网格和部分守恒变量，缺失关键的波速和声速场，因而无法确定安全的步长边界。因此，现有神经求解器普遍沿用固定时间步长，在样本间梯度锐度差异巨大的高速流数据上，训练目标的分布极不均匀，优化方差大，泛化稳定性差。

ShockCast 的动机源于一个简单的观察：若让 $\Delta t$ 按流场变化的速率反比例缩放，就能使相邻时刻的差异 $\| \dot{\mathbf{u}}(t) - \mathbf{u}(t+\Delta t) \|$ 在不同激波强度下趋于均匀，从而降低训练损失的方差。这实质上是让神经求解器“看清”每个样本的时间演进步长，并将步长转化为一个可控的条件变量。为此，ShockCast 设计了一个两阶段框架：第一阶段训练一个神经 CFL 模型 $\psi$，输入当前流场状态 $\mathbf{u}_j$ 及其空间梯度 $\nabla \mathbf{u}$、局部波速和声速等物理 CFL 特征，输出预测的时间步大小 $\Delta_j$；第二阶段将预测的 $\Delta_j$ 作为时步条件注入神经求解器 $\phi$，使其从 $\mathbf{u}_j$ 推进到 $\mathbf{u}_{j+1}$。这一构思不要求神经求解器本身计算 CFL 约束，而是让一个独立的预测器学习从粗网格数据中推断步长，使整体框架在数据驱动条件下复现了物理自适应步进的核心逻辑，从而在保持推理效率的同时显著提升对高速瞬变流动的建模能力。

## 核心创新

ShockCast 的核心创新在于将自适应时间步进机制**可微分地嵌入**深度学习框架，解决高速流神经模拟中由激波等尖梯度结构导致的训练与推断瓶颈。相对于固定步长基线，其关键贡献体现在以下五个「插槽」的替换或新增：

| 变更槽位 | 基线策略 | ShockCast 方案 |
|---------|---------|---------------|
| 时间步确定方式 | 均匀固定步长（训练网格粗化） | 神经CFL模型 ψ 由流场状态预测逐步 Δₜ |
| 神经求解器输入 | 仅流场变量 u(t) | u(t) ⊕ 预测/真实 Δₜ（经时间条件模块注入）|
| 神经CFL输入特征 | 基本流场变量子集 | 额外加入空间梯度 ∇u 及 CFL 物理特征（局部波速、速度幅值、声速）|
| 空间下采样 | 均值池化 | 最大池化（模拟 CFL 条件中的 max 操作）|
| 时间步条件化策略 | Affine 条件化（时延层归一化/空间‑频谱调制）| 新增 Euler 条件化（前向欧拉残差）与 MoE 条件化（多专家条件计算）|

上述插槽共同构成一个**两阶段框架**，其创新逻辑可分解为两条互为倚仗的主线。

### 动态时间步预测：神经 CFL 模型

传统神经算子在一阶训练目标下，固定 Δₜ 导致**训练难度严重不均**——尖梯度区域（如激波面）的 `‖u(t+Δₜ)−u(t)‖` 远大于平滑区域，造成训练方差高、泛化困难。ShockCast 的关键洞见是：**按流场状态变化速率反比例缩放 Δₜ**，使不同空间位置的训练误差分布更均匀，从而降低优化方差。

为此，第一阶段训练一个独立的神经 CFL 模型 ψ，输入当前流场状态，输出预测的步长 Δₜ，训练目标为 MAE：

$$
\mathbb{E}_{j \sim T, U \sim \mathcal{D}} \left[ \mathcal{L}_c \left( \psi(\mathbf{u}_j), \Delta_j \right) \right]
$$

该模型之所以称为“神经 CFL”，源于其输入设计直接**物化经典 CFL 条件的计算逻辑**。经典 CFL 条件

$$
\Delta t \leq \frac{C}{\lambda_{\max}} \min_{x,y}(\Delta x, \Delta y),\quad \lambda_{\max} := \max_{x,y} \lambda(x,y),\quad \lambda(x,y) := \max\left( |u(x,y)| + a(x,y), |v(x,y)| + a(x,y) \right)
$$

中的两个核心运算——**空间下采样的 max 操作**和**波速的物理依赖**——被显式编码进模型架构与特征工程：

- **最大池化下采样**取代常规均值池化，模拟 CFL 中 $\max_{x,y}$ 的行为；
- **CFL 物理特征**直接作为输入通道加入，包括局部波速 $\lambda(x,y)$、速度幅值 $|u|,|v|$ 和声速 $a(x,y)$；
- **空间梯度 ∇u**（有限差分计算）增强模型对流动锋面锐度的感知。

消融实验（Figure 2）证实：同时包含 ∇u、CFL 特征与最大池化的模型（Base）取得了最低单步归一化 MAE，而缺失物理特征或使用均值池化均导致预测误差显著上升。特征重要性分析进一步表明，当前流场 u(t) 对 Δₜ 预测贡献最大，y‑方向偏导数次之，CFL 特征虽直接贡献较小，但作为归纳偏置对模型泛化起关键作用。

### 时间步条件化策略的深化

第二阶段训练时间条件神经求解器 φ，使其在接收当前流场 u(t) **与预测（或真实）步长 Δₜ** 的条件下，推演下一时步流场：

$$
\mathbb{E}_{j \sim \mathcal{T}, U \sim \mathcal{D}} \left[ \mathcal{L}_s \left( \phi(\mathbf{u}_j, \Delta_j), \mathbf{u}_{j+1} \right) \right]
$$

与仅使用 Affine 条件化（时延层归一化或空间‑频谱调制）的基线不同，ShockCast 探索了两种**具备物理动机的增强策略**：

- **Euler 条件化**：将前向欧拉残差作为跳跃连接注入，使 Δₜ 的信息显式参与状态推进；
- **MoE 条件化**：利用混合专家路由机制，根据 Δₜ 大小选择不同的计算路径，增强模型对不同步长区间的适应性。

在煤尘爆炸和圆形爆炸基准上，Euler 与 MoE 条件化在湍流动能（TKE）误差和长时关联时间比例上均优于纯 Affine 基线，且 MoE 条件化在增高推理成本的同时换取了更低的 TKE 误差（如 U-Net MoE 相比 Affine 的 TKE 相对误差降低 0.94×10⁻²）。值得注意的是，当使用真实 Δₜ（Oracle）时，ShockCast 与固定步长的性能差距极小（关联时间比例仅差 −0.04×10⁻²，Table 7），表明神经 CFL 模型的预测已逼近最优自适应步长。

## 整体框架

![[assets/figures/papers/iclr26_0004_d4gzLgGl7I_A_Two-Phase_Deep_Learning_Framework_for_Adaptive/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the ShockCast framework for time-adaptive modeling of high-speed flows. Left: Training pipeline. The neural CFL model and time-conditioned neural solver are conditioned on the current flow state and predict the corresponding timestep size $\Delta$ t and flow state $\Delta$ t ahead, respectively. Right: Inference pipeline. ShockCast autoregressively alternates between predicting the timestep size given the current flow state using the neural CFL model and evolving the flow state forward in time by the predicted timestep size using the neural solver model. Note that the example data are from the circular blast dataset we generated in this work

ShockCast 是一个面向高速可压缩流建模的两阶段深度学习框架，其核心思想是**将自适应时间步的选择也纳入可学习过程**：第一阶段预测当前流场状态下最合适的时间步长 Δt，第二阶段则将该步长作为条件，驱动神经求解器推进系统状态。这种设计打破了以往神经求解器使用均匀时间步（或仅依赖训练数据粗化步长）的局限，使得模型能够根据流场中激波、界面等尖梯度结构的动态变化自主调整步长，从而缓解均匀步长带来的计算浪费和训练目标高方差问题。

**两阶段流程**  
1. **神经 CFL 模型（Neural CFL Model）**：该模块 $ψ$ 以当前流场状态 $\mathbf{u}_j$ 为输入，输出一个标量步长预测值 $\hat{Δ}_j$。训练时最小化 $\hat{Δ}_j$ 与真实步长 $Δ_j$ 之间的平均绝对误差（MAE），即  
   $$\mathbb{E}_{j \sim T, U \sim \mathcal{D}} \left[ \mathcal{L}_c \left( ψ(\mathbf{u}_j), Δ_j \right) \right],$$  
   其中 $\mathcal{L}_c$ 为 MAE。为引入物理先验，模型的输入除基本流场变量外，还显式包含空间梯度 $∇\mathbf{u}$ 以及基于局部波速、速度幅值和声速构建的 CFL 特征；空间下采样采用最大池化以模拟经典 CFL 条件中的 $\max$ 运算。

2. **时间条件神经求解器（Time‑conditioned Neural Solver）**：该模块 $ϕ$ 同时接受当前流场 $\mathbf{u}_j$ 和预测步长 $\hat{Δ}_j$（或训练时的真实步长 $Δ_j$），输出下一时刻的流场 $\mathbf{u}_{j+1}$。训练目标为平均相对误差：  
   $$\mathbb{E}_{j \sim \mathcal{T}, U \sim \mathcal{D}} \left[ \mathcal{L}_s \left( ϕ(\mathbf{u}_j, Δ_j), \mathbf{u}_{j+1} \right) \right].$$  
   步长通过“时间条件化”策略注入求解器：基础方案包括仿射变换（时间条件层归一化或空间‑频谱调制），进阶方案引入了欧拉残差条件化（Euler conditioning）和混合专家（MoE）条件化，以更精细地建模步长对演化过程的影响。

**训练与推理流程**  
- **训练阶段**：两个模块**解耦训练**。首先利用传统 CFD 求解器生成的自适应步长数据训练神经 CFL 模型，使其学会从流场特征推断合适的步长；然后用固定步长（训练时的真实 Δt）训练时间条件神经求解器，使求解器学习在给定步长下的一步演化规律。  
- **推理阶段**：采用自回归方式。从初始流场 $\mathbf{u}_0$ 出发，循环执行“预测步长 → 推进流场”两步：先由 $ψ$ 预测当前步长 $\hat{Δ}_t$，再将 $\mathbf{u}_t$ 和 $\hat{Δ}_t$ 传入 $ϕ$ 得到 $\mathbf{u}_{t+Δt}$；随后以新流场为输入进入下一循环。整个过程无需传统 CFL 条件或网格信息，完全由数据驱动。

**框架动机与优势**  
高速流中激波等结构要求步长随局部梯度剧烈变化而急剧减小，均匀步长迫使整个模拟采用最严格的最小步长，计算代价极高。ShockCast 通过学习“流场状态 → 步长”的映射，使神经求解器获得的训练对的难度分布更加均匀——尖锐梯度区域对应的步长小、缓变区域步长大，从而**降低训练目标的方差**，提升模型在强非线性和大梯度条件下的稳定性和泛化能力。同时，步长预测与流场推进的分离设计也降低了两任务的耦合复杂度，便于针对性地改进各模块。

## 核心模块与公式推导

### 两阶段自适应时间步进框架

ShockCast 将高速流的时间推进建模拆解为两个协同训练的模块：**神经CFL模型**（Neural CFL Model）与 **时间条件神经求解器**（Time‑conditioned Neural Solver）。神经CFL模型根据当前流场状态预测下一时间步的大小Δₜ；神经求解器则以当前流场状态与预测的Δₜ为联合输入，将系统状态向前推进一个Δₜ的步长，输出下一时刻的流场。该设计使得神经求解器能够以动态、依赖于流场特征的步长运行，从而在激波等梯度尖锐区域自动缩小步长、在平缓区域增大步长，缓解全均匀步长造成的计算浪费与训练方差过大的问题。

### 神经CFL模型

**输入特征**：神经CFL模型 ψ 的输入不限于神经求解器所使用的流场子集 u(t)，还显式引入了空间梯度和物理CFL特征。具体做法为：对 u 中所有场用有限差分计算空间梯度 ∇u；添加局部波速 λ(x,y)、速度幅值 |u(x,y)|、|v(x,y)| 以及局部声速 a(x,y) 作为附加通道，其中 λ(x,y) = max( |u(x,y)|+a(x,y), |v(x,y)|+a(x,y) )。这些特征提供了信息传播速度的空间分布信息。

**结构特点**：为模拟经典CFL条件中“取全局空间最大值”的行为，模型中的空间下采样采用**最大池化**（max pooling）而非平均池化。

**训练目标**：神经CFL模型通过最小化预测步长与真实步长之间的 **平均绝对误差（MAE）** 来训练，损失函数为

$$
\mathbb{E}_{j \sim \mathcal{T},\, U \sim \mathcal{D}} \Big[ \mathcal{L}_c \big( \psi(\mathbf{u}_j),\, \Delta_j \big) \Big],
\qquad \mathcal{L}_c = \mathrm{MAE}\big( \psi(\mathbf{u}_j), \Delta_j \big).
$$

其中 j 遍历时间网格上的训练步索引，U 从数据集分布 D 中采样，u_j 为当前流场状态，Δ_j 为对应的真实时间步长。这一损失引导模型学习从流场局部特征到全局允许步长的映射，无需显式编码经验 Courant 数。

### 时间条件神经求解器

神经求解器 φ 接收当前流场 u_j 和预测步长 Δ_j（训练时可直接使用真实 Δ_j），输出 u_{j+1}，训练目标为最小化预测流场与真实值之间的**归一化相对误差**（按场平均）：

$$
\mathbb{E}_{j \sim \mathcal{T},\, U \sim \mathcal{D}} \Big[ \mathcal{L}_s \big( \phi(\mathbf{u}_j, \Delta_j),\, \mathbf{u}_{j+1} \big) \Big],
\qquad \mathcal{L}_s = \frac{1}{N_{\text{fields}}} \sum_{k} \frac{\big\| \phi(\mathbf{u}_j, \Delta_j)_k - (\mathbf{u}_{j+1})_k \big\|}{\big\| (\mathbf{u}_{j+1})_k \big\|}.
$$

该损失确保求解器在不同Δₜ下的预测质量，并因其以步长为显式条件，迫使模型适应步长变化带来的求解器难度差异。训练时若使用预测步长，则构成端到端的“神经CFL→求解器”管线。

**时间条件化策略**（核心变体）：
- **Affine 条件化**：通过时间条件层归一化（或 F‑FNO 的空间‑频谱调制）将 Δₜ 的嵌入注入特征图。
- **Euler 条件化**：在 Affine 基础上叠加前向欧拉残差模块，显式编码Δₜ 对状态更新的影响。
- **MoE 条件化**：引入多专家结构，由Δₜ 决定专家的激活权重，以增大模型容量并精细捕捉不同步长下的动态。

上述策略均有实验证据支持其在不同指标上的增益（如 Euler 与 MoE 改善湍流动能误差），但具体公式不属于本节自推导内容，此处不展开。

### 自适应步长动机与经典 CFL 条件

高速流中激波等尖锐梯度结构要求极小的时间步长，均匀时间步格式必须全程采用最严苛的限制步长，造成巨大计算浪费。同时，神经求解器通常工作在粗化的时空网格上、且仅解析部分流场变量，经典 CFL 条件无法直接沿用。

经典 CFL 条件要求

$$
\Delta t \le \frac{C}{\lambda_{\max}} \min_{x,y}(\Delta x, \Delta y),
\qquad \lambda_{\max} := \max_{x,y} \lambda(x,y),
\quad \lambda(x,y) := \max\big( |u(x,y)| + a(x,y),\, |v(x,y)| + a(x,y) \big),
$$

其中 C 为 Courant 数，Δx, Δy 为网格间距，λ_max 为全局最大波速，a(x,y) 为声速。该条件确立了最大时间步长与局部信息传播速度之间的反比关系。

ShockCast 不再显式使用该条件，而是通过神经 CFL 模型从流场状态中隐式学习这一关系，从而在粗网格、部分变量的条件下仍然能够输出有效的自适应 Δₜ。直觉上，按流场变化的速率反比例缩放Δₜ可以使训练目标的难度分布更加均匀，大幅降低因梯度尖锐程度差异造成的方差，进而提升神经求解器的稳定性和泛化能力。

## 实验与分析

### 主实验结果

ShockCast 在煤尘爆炸（Coal Dust Explosion）评测拆分上展现出超过四个数量级的推理加速：以 CNO Affine 变体在 GPU 上的平均推理时间 $2.15 \pm 0.07$ s 为基准，传统有限体积求解器在 16 核 CPU 上的平均求解时间为 67,441 s，加速比达到四个数量级以上（Table 4、Table 5）。该加速比在后文所有神经求解器变体上保持相近量级，且不牺牲长期统计量的精度。

![[assets/figures/papers/iclr26_0004_d4gzLgGl7I_A_Two-Phase_Deep_Learning_Framework_for_Adaptive/figures/032_Table_4.jpg]]
*Table 4: ShockCast runtime to compute a solution via autoregressive unrolling in both settings on CPU and GPU, presented as mean (standard error)*

![[assets/figures/papers/iclr26_0004_d4gzLgGl7I_A_Two-Phase_Deep_Learning_Framework_for_Adaptive/figures/033_Table_5.jpg]]
*Table 5: Classical solver runtime to compute a solution on 16 CPU cores in seconds for the Coal Dust Explosion setting*

在长期统计量方面，ShockCast 在湍流动能（TKE）和平均流两个物理量上均实现误差降低。煤尘爆炸评测拆分上，U‑Net MoE 变体的 TKE 相对误差为 $8.91 \pm 0.16 \times 10^{-2}$，相比 U‑Net Affine 的 $9.85 \pm 0.24 \times 10^{-2}$ 下降 $0.94 \times 10^{-2}$（Table 16）。圆爆炸（Circular Blast）评测拆分上，F‑FNO MoE 的平均流相对误差为 $3.41 \pm 0.03 \times 10^{-2}$，相比 CNO Affine 的 $4.28 \pm 0.11 \times 10^{-2}$ 下降 $0.87 \times 10^{-2}$（Table 15）。

![[assets/figures/papers/iclr26_0004_d4gzLgGl7I_A_Two-Phase_Deep_Learning_Framework_for_Adaptive/figures/082_Table_16.jpg]]
*Table 16: Relative error for TKE on evaluation splits*

关联时间比例（Correlation Proportion）是衡量自回归稳定性的关键指标。圆爆炸评测拆分上，ShockCast 与使用真实 $\Delta t$ 的 Oracle 上界之间的差异极小，U‑Net Affine 仅差 $-0.04 \times 10^{-2}$（Table 7），表明神经 CFL 对自适应时间步的预测已接近最优下界。

![[assets/figures/papers/iclr26_0004_d4gzLgGl7I_A_Two-Phase_Deep_Learning_Framework_for_Adaptive/figures/054_Table_7.jpg]]
*Table 7: Correlation proportion averaged over fields for ShockCast and difference between the ShockCast correlation proportion and the correlation proportion for the neural solver component using the ground truth ∆t in the circular blast setting*

### 消融与成分分析

#### 神经 CFL 模型的输入特征与池化策略

Figure 2 的神经 CFL 单步归一化 MAE 显示，完整使用空间梯度 $\nabla u$ 与 CFL 物理特征（局部波速 $\lambda(x,y)$、速度幅值 $|u(x,y)|$ 和 $|v(x,y)|$、声速 $a(x,y)$）的 Base 模型误差最低（约 0.032）。与之对比，仅使用 $\nabla u$（约 0.042）或 $\nabla u$ 与 CFL 特征分开使用且缺乏合理组合（约 0.040–0.042）时误差显著升高。这证实空间梯度信息与物理 CFL 特征之间存在协同效应。

![[assets/figures/papers/iclr26_0004_d4gzLgGl7I_A_Two-Phase_Deep_Learning_Framework_for_Adaptive/figures/003_Figure_2.jpg]]
*Figure 2: One-step MAE of Neural CFL models on ∆t averaged over 3 training runs, where ∆t is normalized to have standard deviation 1. Error bars $\mathrm { a r e } \pm$ 2 standard errors

池化策略同样关键：将空间下采样函数从均值池化替换为最大池化可模拟 CFL 条件中的 $\max$ 操作，进一步提升预测精度。消融实验中 $\nabla u$+Max 与 $\nabla u$+Max+CFL 的误差位于 Base 和粗特征变体之间（约 0.037），说明最大池化部分缓解了特征不完整带来的损失，但不能完全替代物理信息。

#### 时间步条件化策略

Affine 条件化（对于 F‑FNO 为空间‑频谱调制，对于其他架构为时间条件层归一化）是基础方案。在此基础上引入 Euler 条件化（前向欧拉残差）和 MoE 条件化（多专家条件计算）可在长期统计量上获得额外收益。

煤尘爆炸评测方面，U‑Net 在 Euler 和 MoE 条件下依次取得 TKE 误差的最低和次低（Figure 5），而 F‑FNO 在圆爆炸评测方面以 Euler 和 MoE 条件取得最低的 TKE 误差（Figure 6）。这表明 Euler 残差结构能够减轻时间步变化导致的训练目标漂移，MoE 则通过多专家分解为不同步长范围提供专门化的计算路径，代价是参数和 FLOPs 增加（Table 4、Table 5 中 Euler 和 MoE 的 GPU 时间比 Affine 多出 20–60% 不等）。

#### 特征重要性

Figure 29 的特征重要性研究表明，当前流场 $u(t)$ 本身是 $\Delta t$ 预测中最重要的输入，其次为 $y$‑方向偏导数，而 CFL 物理特征（波速、声速等）的直接贡献低于空间梯度分量。这并不削弱 CFL 特征的作用——消融实验已证明其不可替代性——而是表明神经网络在自动学习耦合关系的条件下，显式梯度信号比手工提取的物理特征具有更强的信息密度。

#### 质量守恒

ShockCast 在自回归推演中保持相对质量偏差在初始质量的 0.2% 以内（Figure 21），这表明自适应时间步并未引入累积质量泄漏，两阶段框架在长期仿真中维持了流体力学的基本守恒律。

### 公平性说明

所有模型使用相同的数据集划分和评价指标，训练在相同硬件条件下进行，代码与数据集已公开，便于复现与改进。Table 2 和 Table 3 统一给出了神经求解器、神经 CFL 模型和 3D 变体（U‑Net‑3D、F‑FNO‑3D、ConvNeXT‑3D）的超参数、参数量、GFLOPs 及峰值 GPU 内存，保证模型间的可比性。

### 小结与未覆盖风险

实验证实两阶段自适应时间步框架在加速比（>10⁴倍）、长期统计精度（TKE 与平均流误差）以及稳定性（关联时间比例接近 Oracle）三个维度均优于均匀时间步的基线。消融实验指向三个有效设计要素：空间梯度与 CFL 特征的组合输入、最大池化下采样、以及 Euler/MoE 时间步条件化。

当前报告未涉及本框架在多物种反应流或考虑黏性与热传导的全 Navier‑Stokes 设置下的表现。此外，虽然关联时间比例接近 Oracle，但在极端激波间断处和极高初始压力比的配置中，ShockCast 的自回归误差传播模式尚未有公开失效分析，这一点需要进一步实验确认。

## 方法谱系与知识库定位

### 与基线神经算子的关系

ShockCast 并非重新设计一个全新的神经算子架构，而是为现有神经求解器主干提供一种通用的自适应时间步进附加机制。方法在四个主流主干上一致实例化，包括卷积神经算子 CNO、因子化傅里叶神经算子 F‑FNO、U‑Net 和 Transolver。这些主干原本采用均匀固定步长（训练时间网格的均匀粗化），ShockCast 在不修改主干核心结构的前提下引入两个级联变更：① 将时间步从均匀固定步长替换为神经 CFL 模型 ψ 从当前流场状态预测的自适应 Δₜ；② 将预测的 Δₜ 通过时间条件模块注入神经求解器 ϕ。

在条件化策略上，Affine 条件构成最直接的对照基线——它仅使用时间步条件化的层归一化（非 F‑FNO 架构）或时空-频谱调制（F‑FNO），将 Δₜ 编码为尺度与偏置参数。Euler 条件化与 MoE 条件化在此基础上叠加前向欧拉残差，其中 MoE 条件化使用多专家计算实现条件化的非线性路由，以模型容量换取表达能力。这一差异在高速流物理量上表现突出：在 Circular Blast 上，F‑FNO MoE 将平均流相对误差降至 3.41×10⁻²，而 CNO Affine 为 4.28×10⁻²；在 Coal Dust Explosion 上，U‑Net MoE 的湍流动能误差降至 8.91×10⁻²，优于 U‑Net Affine 的 9.85×10⁻²。

值得注意的上限基线与下限基线：Oracle 基线直接使用真实 Δₜ 作为神经求解器的步长输入，构成 Δₜ 预测能力的理想上限——在 Circular Blast 上与预测 Δₜ 的 U‑Net Affine 关联时间比例差距仅为 −0.04×10⁻²，表明神经 CFL 模型预测的自适应步长已接近最优。Mean prediction 基线始终预测训练集的平均 Δₜ，构成最低下限，用于标定随机猜测水平的性能。

### 适用边界与条件依赖

ShockCast 设计的前提条件来自高速流计算的三个约束耦合：① 激波等尖梯度区域需要极小的时间步长，经典均匀步长被迫全程使用该最小值，导致计算复杂度膨胀；② 神经求解器使用的空间网格较粗（相对传统求解器数百倍的下采样），且输入变量仅为传统 CFL 条件所需变量的子集，使得直接使用经典 CFL 条件确定步长不可行；③ 训练目标难度极度不均匀——梯度尖锐区域的一步残差远大于平滑区域，导致训练方差增大。

在上述边界内，ShockCast 的因果路径有效：神经 CFL 模型通过编码空间梯度 ∇u 和物理 CFL 特征（局部波速 λ、速度幅值 |u|, |v|、声速 a），并采用最大池化模拟 CFL 条件中的 max 操作，学习从粗网格、部分变量输入中推断近似 CFL 步长。特征重要性研究表明，当前流场 u(t) 对 Δₜ 预测影响最大，其次是 y‑方向偏导数，CFL 特征的直接贡献相对较小。这一结果暗示，在激波主导区域内，梯度信息本身足以蕴含步长所需的关键时空约束。

从计算代价角度看，ShockCast 的加速优势基于神经求解器粗时间步进与 GPU 高并行度的结合：在 Coal Dust Explosion 上，ShockCast 的 CNO Affine 变体 GPU 求解时间为 2.15±0.07 秒，而经典求解器在 16 个 CPU 核上需要 67,441 秒，实现四个数量级以上的加速。这一加速比高度依赖所允许的粗化因子与激波强度之间的权衡——更粗的网格意味着更大的加速，但也对 Δₜ 预测精度和求解器鲁棒性提出更高要求。

### 局限与开放问题

质量守恒是长期自回归仿真的核心约束。ShockCast 的质量守恒误差保持在初始质量的 0.2% 以内，这为长时间推断提供了基本保障，但这是在评估场景上的观测值，未能刻画极端工况（如极强激波、多激波干涉、复杂边界条件）下的保守性退化。这一验证面向的仅是已有样本分布的泛化，对分布外流入条件的鲁棒性仍需人工验证。

神经 CFL 模型的预测能力在单步 MAE 上表现优异，且与 Oracle 的关联时间比例差距极小，但当前消融仅覆盖了 Circular Blast 上的特征组合效果——加入 ∇u 与 CFL 特征的组合在 Base 模型上取得最低单步归一化 MAE，而单独使用 ∇u 或 ∇u+CFL 无组合效果时误差显著升高。这一现象暗示预测精度对特征组合方式的敏感度，但未给出在不同流况之间的泛化转移性证据。

开放问题集中在以下方向：① 神经 CFL 模型对训练分布外激波构型的泛化能力——当前验证仅限于与训练同分布条件下的泛化，尚未评估跨初始条件、跨流体模型的迁移；② 多尺度耦合问题——当激波、湍流和其他流态场景共存时，单一的标量 Δₜ 预测机制能否充分捕捉局部步长需求的异质性；③ 与经典自适应步长控制策略（如 PID 控制器）的理论等价关系——若神经 CFL 模型本质上是在学习某种近似误差估计与步长缩放，其与经典控制理论的桥接将有助于解释其泛化边界。这些方向需在更宽范围内进行体系化验证。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Two_Phase_Deep_Learning_Framework_for_Adaptive_Time_Stepping_in_High_Speed_Flow_Modeling.pdf

![[paperPDFs/ICLR_2026/A_Two_Phase_Deep_Learning_Framework_for_Adaptive_Time_Stepping_in_High_Speed_Flow_Modeling.pdf]]
