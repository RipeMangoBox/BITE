---
title: "Metappearance: Meta-Learning for Visual Appearance Reproduction"
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Metappearance_Meta_Learning_for_Visual_Appearance_Reproduction.pdf
project_link: null
code_link: "https://github.com/mfischer-ucl/metappearance"
aliases:
- Metappearance
tags:
- SIGGRAPH_ASIA_2022
- topic/vision_multimodal_applications
core_operator: 元学习同时优化模型初始参数 θ0 和每参数学习率 α，使得内循环仅需约 10 步梯度下降即可高效拟合新任务，从而大幅缩短适应时间而不牺牲质量。
primary_logic: 将“如何高效过拟合单个样本”本身作为学习目标，通过双层元训练（外循环遍历任务，内循环约束少量步数过拟合）学习出强先验的初始化和自适应步长，使推理时能以极低成本实现接近全量过拟合的复现质量。
claims:
- 在纹理、BRDF、svBRDF、照明、光传输六个任务上，Meta 以少数量级的内循环步数（≤20步）达到接近 Overfit 的质量，同时推理速度接近 General 方法。
- 消融实验表明，仅学习初始化或仅学习步长均不能取得最优效果，二者组合（Meta）显著优于任何单一组件。
- 在等步数约束下（QuickFT），Meta 在所有任务上的误差均低于简单微调基线，说明元学习学到了非平凡的优化过程。
- 对于 BRDF 编码，Meta 仅需 5,120 个采样点（全量 MERL 约 1.46×10^6 点），带宽节省 99.6%，同时保持高精度。
---

# Metappearance: Meta-Learning for Visual Appearance Reproduction

> [!tip] 核心洞察
> 将“如何高效过拟合单个样本”本身作为学习目标，通过双层元训练（外循环遍历任务，内循环约束少量步数过拟合）学习出强先验的初始化和自适应步长，使推理时能以极低成本实现接近全量过拟合的复现质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | Metappearance：面向视觉外观复现的元学习方法 |
| 英文题名 | Metappearance: Meta-Learning for Visual Appearance Reproduction |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://mfischer-ucl.github.io/metappearance/) · [Code](https://github.com/mfischer-ucl/metappearance) |
| Topic | #topic/vision_multimodal_applications |
| Method | Metappearance |
| Dataset |  |

> [!tip] 效果简介
> - 在纹理、BRDF、svBRDF、照明、光传输六个任务上，Meta 以少数量级的内循环步数（≤20步）达到接近 Overfit 的质量，同时推理速度接近 General 方法。
> - 消融实验表明，仅学习初始化或仅学习步长均不能取得最优效果，二者组合（Meta）显著优于任何单一组件。
> - 对于 BRDF 编码，Meta 仅需 5,120 个采样点（全量 MERL 约 1.46×10^6 点），带宽节省 99.6%，同时保持高精度。

## 概要

视觉外观复现（纹理、BRDF、svBRDF、照明、光传输等）长期存在速度与质量不可兼得的困境：通用模型推理快但丢失高频细节，过拟合/微调模型精度高却需海量迭代，无法满足交互式应用需求。瓶颈在于优化范式本身——传统训练无法在极少步数内实现高保真适应。

Metappearance 提出以元学习重塑该范式：将“如何高效过拟合单个样本”作为学习目标，通过双层优化（外循环遍历任务集学习初始化 θ₀ 与逐参数学习率 α，内循环约束约 10 步梯度下降过拟合新实例）获得强先验的初始化和自适应步长。推理时仅需极少量内循环步数即可逼近全量过拟合的复现质量。

在六个视觉外观任务上，Meta 以 ≤20 步内循环达到接近 Overfit 的精度，推理速度接近 General 方法；消融实验证实初始化和步长联合学习是关键，缺一不可；等步数约束下的 QuickFT 实验中 Meta 全面优于简单微调基线；BRDF 编码仅需 5,120 采样点（较全量 MERL 节省 99.6% 带宽）仍保持高精度。该方法定位为通用、快速、精确且紧凑的外观复现框架，将元学习引入视觉计算领域，为交互式高质量渲染提供了新的优化路径。

## 核心方法与创新机理

### 问题瓶颈：优化效率的“不可能三角”

视觉外观复现任务中存在一个根本性的效率-质量矛盾。给定一个观测条件（如单张照片、稀疏测量），目标是重建一个能够泛化到任意视角/光照的辐射函数。传统方法可归为三类训练范式：

- **通用训练**：在全部训练样本上学习从条件到外观的直接映射。推理时仅需一次前向传播，速度极快，但受限于隐空间的瓶颈效应——模型只能捕捉样本集的统计平均，高频细节和个体特异性被压缩丢失。
- **过拟合训练**：对每个样本从头开始迭代优化，直到完全拟合。精度最高，但单个样本需要数千至上万步梯度下降，耗时在秒级甚至分钟级，无法用于交互式应用。
- **微调训练**：先通用预训练，再对目标样本微调。精度介于二者之间，但微调仍需数百步迭代，速度远不能满足实时需求。

核心瓶颈在于**优化过程本身**：传统训练范式无法在极少迭代步数（如10步）内实现高精度适应。这并非模型容量不足，而是优化起点和步长策略缺乏对“如何高效过拟合单个样本”的先验知识。

### 核心创新：将“高效过拟合”本身作为元学习目标

Metappearance 的关键洞察在于：**“如何高效过拟合单个样本”本身可以被视为一个可学习的问题**。通过双层元训练，外循环遍历大量任务学习“如何快速适应”，内循环在严格步数约束下执行适应过程，最终产出一个具备强先验的初始化参数和自适应学习率——使得推理时仅需约10步梯度下降即可达到接近全量过拟合的复现质量。

这一思路从根本上改变了优化的起点：传统方法从随机或通用的初始点出发，需要大量迭代才能到达目标样本的局部最优；而元学习后的初始点已经位于“所有可能解”的流形附近，且每个参数拥有独立的自适应步长，使极少量迭代即可精确收敛。

### 三个核心 Changed Slots

#### Changed Slot 1：训练范式——从单层优化到双层元学习

**基线值**：General、Overfit 或 Finetune 均采用单层优化，直接最小化重构损失函数。

**提出值**：双层嵌套优化。外循环学习元参数 φ（包含初始模型参数 θ₀ 和每参数学习率 α）；内循环在固定步数约束下，从 θ₀ 出发，使用 α 对单个任务执行梯度下降，最小化该任务的过拟合损失。

外循环的元损失函数为：

$$\operatorname{Loss}_{\mathsf{Meta}}(\phi, \mathcal{T}) = \mathbb{E}_{i \in \mathcal{T}} \left[ \operatorname{Loss}_{\mathsf{Overfit}}\left( \operatorname{LEARN}(\phi, i), i \right) \right]$$

其中 $\mathcal{T}$ 为任务分布，$\operatorname{LEARN}(\phi, i)$ 表示以 φ 为元参数、在任务 i 上执行内循环优化后得到的适配参数。外循环通过对该损失的梯度反向传播，同时更新 θ₀ 和 α。

**因果机制**：外循环迫使 θ₀ 收敛到这样一个位置——从它出发，仅需少量内循环步数即可到达任意训练任务的局部最优。同时，α 被训练为每参数自适应的步长，使得优化过程能自动调节不同参数的更新幅度。这一双层结构将“快速适应”的归纳偏置直接编码进元参数中。

#### Changed Slot 2：可学习参数——从仅模型参数到模型初始化 + 每参数学习率

**基线值**：传统训练仅学习模型参数 θ（网络权重）。

**提出值**：元参数 φ 包含两部分：
- **初始模型参数 θ₀**：为内循环提供强先验起点。其效果可从 Fig. 2 的轨迹对比中直观看出：Meta 的初始点已接近目标 BRDF 的收敛区域，内循环轨迹（虚线）显著短于 Overfit 从随机点出发的轨迹。
- **每参数学习率 α**：一个与 θ 同形的张量，为每个可学习参数赋予独立的步长。Fig. 3 展示了学习步长的效果：对于 BRDF 任务，不同参数维度的损失地形各异，固定步长（灰色区间）可能导致某些维度震荡或收敛缓慢，而学习到的 α 能自动适配各维度的曲率特征。

![[assets/figures/papers/paper_list_l65_https_mfischer_ucl_github_io_metappearance/figures/003_Figure_2.jpg]]
*Figure 2: Learning the init: Trajectories for Meta and Overfit for the example task of BRDF representation. The dotted line denotes inner optimization. Note how the dotted trajectories for Meta are shorter, i.e., faster learning*

![[assets/figures/papers/paper_list_l65_https_mfischer_ucl_github_io_metappearance/figures/004_Figure_3.jpg]]
*Figure 3: Learning the step size: The orange and violet curve show the loss (vertical) for different parameters ?? (horizontal) for two BRDF tasks. The gray ??-intervals denote three alternative step sizes. The zig-zags are the convergence paths for specific choices of step size. Please see the text for discussion*

**因果机制**：θ₀ 和 α 协同作用。仅学习 θ₀（固定步长）能将起点移近目标，但步长策略仍是非自适应的；仅学习 α（随机起点）能加速收敛，但起点远离目标时仍需要较多步数。消融实验（Fig. 10）证实，二者组合（完整 Meta）在所有任务上显著优于任一单独组件。

#### Changed Slot 3：推理时的适应机制——从零次前向到少量步数内循环

**基线值**：General 方法在推理时执行单次前向传播，无迭代适应；Overfit/Finetune 需大量迭代。

**提出值**：推理时，对于新观测条件 I，从元学习的 θ₀ 出发，使用 α 执行 n_l 步内循环梯度下降（n_l 通常为 10-20），得到适配参数 θ*，再用于推理。

**因果机制**：这一设计将推理时的计算开销从“零”提升到“极少量迭代”，但换取了接近 Overfit 的质量。关键在于 n_l 的量级差异：Overfit 需数千步，Meta 仅需约 10 步，速度提升两个数量级以上，同时质量损失极小。

### 方法框架与模块顺序

Metappearance 的完整流程分为元训练和推理两个阶段。

**元训练阶段**（外循环 + 内循环）：

1. **任务采样**：从训练任务分布 $\mathcal{T}$ 中采样一个批次的任务，每个任务对应一个外观样本（如一张纹理、一个 BRDF 测量）。
2. **内循环初始化**：将当前元参数 φ = {θ₀, α} 复制为内循环的工作参数 θ ← θ₀。
3. **内循环优化**：对每个任务独立执行 n_l 步梯度下降。每步计算该任务的过拟合损失 $\operatorname{Loss}_{\mathsf{Overfit}}$，使用 α 作为每参数学习率更新 θ。公式为：θ ← θ - α ⊙ ∇_θ Loss_Overfit(θ, i)。
4. **外循环更新**：收集所有任务在内循环结束后的最终损失，计算元损失 $\operatorname{Loss}_{\mathsf{Meta}}$，通过反向传播穿过整个内循环过程，更新 φ。
5. **迭代**：重复 1-4 直至收敛。

**推理阶段**（仅内循环）：

1. **输入**：给定新观测条件 I 和对应的稀疏测量。
2. **内循环适应**：从元训练的 θ₀ 出发，使用 α 执行 n_l 步梯度下降，得到适配参数 θ*。
3. **推理输出**：使用 θ* 对任意查询坐标 x 计算辐射值 $L_{\theta^*}(\mathbf{x} | I)$。

### 关键公式与变量含义

**辐射函数表示**：$L_{\theta}(\mathbf{x} | I)$，其中 x 为位置-方向坐标，I 为观测条件，θ 为可调参数。

**过拟合损失**（内循环优化目标）：
$$\operatorname{Loss}_{\mathsf{Overfit}}(\theta, T) = \mathbb{E}_{i \in T} \left[ \Delta\left( L_{\theta}(\mathbf{x}_i | I), L_i \right) \right]$$
其中 I 为固定条件，Δ 为距离度量（如 L1、L2 或感知损失），T 为测量点集。

**通用损失**（对比基线）：
$$\operatorname{Loss}_{\mathsf{General}}(\theta, T) = \mathbb{E}_{i \in T} \left[ \Delta\left( L_{\theta}(\mathbf{x}_i | I_i), L_i \right) \right]$$
关键区别在于 I 随样本变化，模型需学习从 I 到外观的映射，而非过拟合单个样本。

**内循环学习过程** $\operatorname{LEARN}(\phi, i)$：以 φ = {θ₀, α} 为元参数，在任务 i 上执行 n_l 步梯度下降，返回最终参数 θ_{n_l}。

### 跨任务泛化的统一框架

Metappearance 的方法论不依赖特定网络架构或任务类型。论文在六个复杂度递增的任务上验证了统一框架的有效性：

1. **RGB 纹理**：基于 Ulyanov et al. (2016) 和 Henzler et al. (2020) 的纹理生成网络。
2. **BRDF 表示**：从稀疏方向测量重建各向同性 BRDF。
3. **静态 svBRDF**：从闪光灯图像恢复空间变化 BRDF。
4. **非静态 svBRDF**：扩展到包含空间变化光照条件的材质。
5. **照明估计**：从 RGB 图像和法线图重建环境光照。
6. **光传输**：学习场景的全局光传输函数。

所有任务共享相同的元训练范式，仅需替换网络架构和损失函数。这种统一性源于方法的核心抽象——将视觉外观复现统一为“从稀疏测量快速过拟合辐射函数”的元学习问题。

### 紧凑性优势的机制

除速度和质量外，元学习还带来了紧凑性的增益。由于元训练学到了任务空间的强先验，模型本身可以更小，且推理时所需的测量点数量大幅减少。例如，BRDF 表示任务中，Meta 仅需 5,120 个采样点即可达到全量 MERL 数据库（约 1.46×10⁶ 个点）的精度，带宽节省 99.6%。这一效果的因果链为：元学习的强初始化使得模型能从极稀疏的观测中可靠地推断完整外观函数，而传统过拟合在稀疏观测下容易陷入局部最优或过拟合噪声。

![[assets/figures/papers/paper_list_l65_https_mfischer_ucl_github_io_metappearance/figures/014_Figure_10.jpg]]
*Figure 10: We compare the influence of a learned learning rate (column b) and initialization (column c). Cf. the main text for details*

## 实验与关键发现

### 实验设计概述

论文在六个视觉外观复现任务上系统评估 Metappearance：i) RGB 纹理，ii) BRDF，iii) 静态 svBRDF，iv) 非静态 svBRDF，v) 光照图，vi) 光传输。每个任务均对比三种训练范式：**General**（通用泛化训练，单阶段直接映射）、**Overfit**（单实例过拟合至收敛）、**Finetune**（先通用训练再微调至收敛）。元学习训练时，内循环步数 $n_l$ 远小于完整过拟合步数 $n$（$n_l \ll n$），推理时仅需 $n_l$ 步梯度下降即可获得该实例的专用模型。

### 主结果：质量-速度权衡的突破

Table 2 汇总了全部任务上四种方法的误差与推理时间。核心发现是 Meta 在质量-速度平面上占据了前所未有的优势区域：质量接近 Overfit/Finetune，而推理速度接近 General。

以纹理任务为例，Meta 的测试误差为 0.252，推理时间仅 0.619（相对单位），而 Overfit 误差 0.249 但耗时 1.000，Finetune 误差 0.248 耗时 1.912。BRDF 任务上，Meta 误差 0.720、耗时 0.031，Overfit 误差 0.716、耗时 1.000，Finetune 误差 0.711、耗时 1.941。svBRDF 任务上，Meta 误差 0.311、耗时 1.484，Overfit 误差 0.304、耗时 1.000，Finetune 误差 0.298、耗时 1.909。在所有任务中，Meta 的推理时间较 Finetune 减少数倍至数十倍，而质量损失极小。

Table 2 的质量-速度散点图直观展示了这一优势：Meta 的数据点始终位于右上角（高质量、高速度）区域，General 位于左上（低质量、高速度），Overfit 和 Finetune 位于右下（高质量、低速度）。收敛曲线进一步表明，Meta 在内循环仅约 10 步时即达到 Overfit 需数百步才能达到的误差水平。

对于 BRDF 复现，Meta 在 99% 的测试材质上达到结构相似性（SSIM）≥ 0.95。光传输任务上（Table 3），Meta 在等采样数条件下取得低负对数似然（NLL），表明其能正确适应目标光传输函数。

![[assets/figures/papers/paper_list_l65_https_mfischer_ucl_github_io_metappearance/figures/012_Table_3.jpg]]
*Table 3: Mean absolute percentage error and Structural Dissimilarity (DSSIM) across the Transport test-set. Lower is better for both metrics*

### 关键消融实验

消融实验（Fig. 10 及 Sec. 5.1）揭示了元学习各组件的独立贡献。实验对比了三种变体：仅学习初始化参数 $\theta_0$、仅学习每参数学习率 $\alpha$、以及完整 Meta（同时学习二者）。结果表明，任一单独组件均无法达到完整 Meta 的性能，二者组合在所有任务上取得最优误差。这验证了核心设计：好的初始化将参数置于有利的损失函数区域，而自适应步长则加速在该区域内的收敛，二者协同才能实现极少步数内的高精度适应。

### 等步数对比实验

为排除“Meta 仅因步数少而快”的简单解释，论文设计了 **QuickFT** 实验（Table 4）：将 Finetune 的内循环步数强制限制为与 Meta 相同的 $n_l$ 步。若 Meta 的优势仅来自步数约束，则 QuickFT 应与 Meta 性能相当。实验结果否定了这一假设：在所有六个任务上，Meta 的测试误差均显著低于 QuickFT。以纹理为例，Meta 误差 0.252，QuickFT 误差 0.304；BRDF 上 Meta 误差 0.720，QuickFT 误差 0.776。这表明元学习学到了非平凡的优化轨迹——其初始化与步长组合所引导的梯度下降路径，远优于从通用预训练参数出发、以固定或简单调整的步长进行等步数微调。

![[assets/figures/papers/paper_list_l65_https_mfischer_ucl_github_io_metappearance/figures/016_Table_4.jpg]]
*Table 4: Average error across the respective application’s test-set for our QuickFinetune-experiment. For the metrics reported, please cf. Supplemental Tab. 2. For convenience, we repeat results for methods General and Meta from Tab. 2*

### 紧凑表示与采样效率

Meta 的另一个关键优势是紧凑性。以 BRDF 编码为例，传统 MERL 数据库需约 $1.46 \times 10^6$ 个采样点表征一个 BRDF，而 Meta 仅需 5,120 个采样点（带宽节省 99.6%）即可达到高精度复现。这源于元学习学到的强先验：初始参数 $\theta_0$ 已编码了 BRDF 空间的整体结构，内循环仅需少量观测即可将参数调整至目标 BRDF。对于光传输任务，Meta 在极低采样预算下仍能保持低 NLL，进一步验证了其采样效率。

### 失败模式与适用边界

论文未显式报告失败案例，但从方法机制可推断若干边界条件。首先，元学习的外循环需遍历大量任务以学习通用先验，若目标任务分布与训练任务分布存在显著偏移，Meta 的初始化可能不再有效，内循环适应质量将退化。其次，内循环步数 $n_l$ 是固定超参数：步数过少则欠拟合，过多则推理时间增加。论文未系统研究 $n_l$ 的敏感性，但 Table 2 的收敛曲线暗示约 10–20 步为实用甜点区。再次，对于高度非平稳的外观（如复杂空间变化的 svBRDF），Meta 虽优于 General，但与 Overfit 的绝对误差差距略大于简单任务，表明极强空间变化的适应仍需更多步数或更强先验。

### 实验公平性说明

所有方法的模型架构、损失函数（纹理用 L1，BRDF 用对数空间 L2，svBRDF 用 L1 等）和优化器基础设置保持一致，仅在训练范式上存在差异。推理时间测量包含完整的内循环梯度下降过程，确保了对比的公平性。

![[assets/figures/papers/paper_list_l65_https_mfischer_ucl_github_io_metappearance/figures/002_Table_1.jpg]]
*Table 1: Different ways to optimize for visual appearance reproduction*

## 定位与知识库关联

### 改变的槽位：训练范式从单层优化切换为双层元学习

Metappearance 与三类基线方法（General、Overfit、Finetune）的核心差异不在于网络架构或损失函数形式，而在于**训练范式这一个槽位**。传统方法采用单层优化：General 直接最小化跨任务期望损失以学习通用映射，Overfit 对每个实例独立执行完整梯度下降，Finetune 则先通用预训练再逐实例微调。三者的共同本质是“优化模型参数以拟合数据”，优化过程本身是固定的。

Metappearance 将槽位替换为**双层元学习**：外循环遍历任务分布，学习元参数 $\phi = (\theta_0, \alpha)$（初始参数和每参数学习率）；内循环以极少量步数（$n_l \ll n$，典型值约 10 步）在单个任务上执行受约束的过拟合。这一改变使“如何高效过拟合”本身成为学习目标，从而在推理时以接近 General 的速度获得接近 Overfit 的质量。

### 与已有方法谱系的本质差异

**Table 1** 将视觉外观复现的优化方法划分为四个象限，Metappearance 占据“快速 + 精确”的右上角区域，这是此前方法无法同时满足的组合。

- **General 方法**（如 Ulyanov et al., 2016; Henzler et al., 2020 的纹理合成管线）：通过编码器将条件输入映射到隐空间再解码，推理仅需一次前向传播，速度极快。但其隐空间瓶颈会丢失细节——如论文 Sec. 2.2 所述，虽然隐空间大多包含有效样本，“代价是瓶颈减少了特定细节”。在 BRDF 复现等高频任务中，这一信息损失直接体现为精度下降。

- **Overfit 方法**：对每个实例从头过拟合，无信息瓶颈，精度最高。但需数千步梯度下降，推理时间不可接受。这是典型的“精度-速度”权衡的极端点。

- **Finetune 方法**：先通用训练获得先验，再逐实例微调。理论上应兼具二者优势，但论文实验表明，在等步数约束下（QuickFT），其误差在所有任务上均高于 Meta（Table 4），说明简单的“预训练 + 微调”组合并未学到高效的适应策略。

Metappearance 的本质突破在于：**将过拟合过程本身参数化并纳入学习**。外循环迫使内循环在极严格步数预算下完成任务，从而学到强先验的初始化和自适应步长——初始化使内循环起点靠近优质解区域，每参数学习率使不同参数维度以不同速率收敛（Fig. 2 和 Fig. 3 分别可视化这两个组件的效应）。这并非 General 和 Overfit 的简单拼合，而是一种新的优化范式。

### 知识库挂载点

Metappearance 在知识库中的核心挂载点为 **MAML（Model-Agnostic Meta-Learning, Finn et al., ICML 2017）及其在视觉计算中的扩展**。MAML 提出学习易于快速适应的初始化参数，Metappearance 在此基础上增加了两个关键扩展：

1. **同时学习每参数学习率 $\alpha$**：标准 MAML 使用全局学习率，Metappearance 将其提升为与 $\theta_0$ 同维度的可学习向量。消融实验（Fig. 10）表明，仅学习初始化或仅学习步长均不能达到最优，二者组合（完整 Meta）显著优于任一单组件。

2. **应用于视觉外观复现这一特定领域**：MAML 原用于少样本分类和强化学习，Metappearance 将其引入纹理、BRDF、svBRDF、照明、光传输等六类外观复现任务，覆盖从低维 RGB 纹理到高维光传输的复杂度谱系。

次要挂载点为**神经隐式表示（Neural Implicit Representations）**与**坐标网络（Coordinate Networks）**的快速拟合。Metappearance 将外观表示为辐射函数 $L_\theta(\mathbf{x}|I)$，本质是一个以空间/方向坐标 $\mathbf{x}$ 为输入、以条件 $I$ 为上下文的神经场。与此前需逐场景大量采点训练的工作（如 NeRF 系列）相比，Metappearance 的元学习策略使新场景适应仅需约 10 步梯度下降，且对 BRDF 编码仅需 5,120 个采样点（全量 MERL 数据库约 $1.46 \times 10^6$ 点），带宽节省 99.6%。

### 适用边界与限制条件

1. **任务分布假设**：元学习要求训练任务与测试任务来自相同分布。Metappearance 在六个应用中均采用同分布训练/测试划分，对分布外（out-of-distribution）外观的泛化能力未经验证。若测试外观与训练集差异显著，内循环 10 步的适应预算可能不足。

2. **内循环步数的任务依赖性**：不同任务的最优内循环步数不同（纹理约 10 步，光传输约 20 步），需针对应用单独设定。步数过少则欠拟合，过多则推理时间增加且可能过拟合到噪声。

3. **架构依赖**：元参数 $\phi$ 的维度与模型参数 $\theta$ 相同，对于极大规模模型（如高分辨率神经场），存储和优化每参数学习率的开销线性增长。论文中最大模型为光传输任务，参数规模可控，但扩展到更大模型时需考虑内存限制。

4. **非监督任务的验证有限**：对于 svBRDF 非平稳任务（svBRDFNonStat），论文使用 $L_1$ 监督损失，但真实场景中 Ground Truth 难以获取。元学习在此类弱监督或自监督场景下的有效性需进一步验证。

### 后续研究启发

1. **元学习与压缩的深度结合**：论文指出元学习天然支持紧凑表示（仅需极少量采样点），未来可探索将元学习与神经压缩（如 INR 压缩）联合优化，实现“一次元训练，处处快速解码”的外观压缩框架。

2. **跨模态元迁移**：当前每个应用独立元训练，若能跨纹理、BRDF、照明等模态共享元先验，可能进一步降低对新应用的元训练成本，类似“元-元学习”。

3. **自适应内循环步数**：当前内循环步数 $n_l$ 为固定超参数，若能根据任务难度动态决定停止时机（如基于损失阈值），可在简单任务上进一步节省推理时间。

4. **与扩散模型的连接**：扩散模型的去噪过程可视为一种隐式优化，元学习学到的“快速适应”可能与扩散模型的高效采样策略存在理论联系，值得深入探究。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Metappearance_Meta_Learning_for_Visual_Appearance_Reproduction.pdf]]