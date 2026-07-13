---
title: Variance Reduction for Expectations with Diffusion Teachers
type: paper
paper_level: A
venue: ICML
year: 2026
pdf_ref: paperPDFs/ICML_2026/Variance_Reduction_for_Expectations_with_Diffusion_Teachers.pdf
project_link: https://research.nvidia.com/labs/sil/projects/CARV/
code_link: null
aliases:
  - CCAVR
  - VREDT
tags:
  - ICML_2026
  - topic/vision_multimodal_applications
  - topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过在级联式三阶段框架中引入“双频专家”机制：在去噪过程的高噪声阶段注入对注意力模块施加低通滤波的低频专家，显式巩固全局语义结构；在低噪声阶段注入对前馈网络施加高通滤波的高频专家，精炼局部纹理细节；同时配合直接作用于潜空间的视频潜空间上采样器，以高效且保真的方式搭建从低分辨率运动先验到高分辨率内容增强的桥梁。
primary_logic: 缓存昂贵的渲染结果或生成器输出，并对每个缓存状态用多组噪声进行去噪，同时结合基于显式权重函数的重要性采样和分层逆CDF采样，可以在不修改原始SDS、DMD或归因损失的情况下，以同等计算开销获得2~3倍的有效计算乘数；这些技术互补且实现简单。
claims:
  - CARV在文本到3D蒸馏和归因实验中提供2–3倍有效计算乘数
  - 时间步重要性采样比均匀采样减少约1.2倍方差（在相同每轮计算成本下）
  - 在一步蒸馏（DMD）中，相同技术将梯度方差降低一个数量级，但下游FID并未改善
  - 在数据归因中，分层采样在合理预算下实现>2倍有效计算乘数
---

# Variance Reduction for Expectations with Diffusion Teachers

> [!tip] 核心洞察
> 缓存昂贵的渲染结果或生成器输出，并对每个缓存状态用多组噪声进行去噪，同时结合基于显式权重函数的重要性采样和分层逆CDF采样，可以在不修改原始SDS、DMD或归因损失的情况下，以同等计算开销获得2~3倍的有效计算乘数；这些技术互补且实现简单。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散教师期望的方差缩减 |
| 英文题名 | Variance Reduction for Expectations with Diffusion Teachers |
| 会议/期刊 | ICML 2026 |
| Links | [paper](https://arxiv.org/abs/2605.21489) · [Project](https://research.nvidia.com/labs/sil/projects/CARV/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CARV (Compute-Aware Variance-Reduction) |
| Dataset | Text-to-3D SDS Optimization, One-step Distillation (DMD), Data Attribution |

> [!tip] 效果简介
> - Text-to-3D SDS Optimization 上，Effective Compute Multiplier (ECM) 为 ~3.3× (IW+Strat, R=1, K=8)，对比 1.0× (uniform, K=1)，变化 +2.3×。
> - Text-to-3D SDS Optimization 上，CLIP score convergence 为 Reaches baseline CLIP score in ~half iterations，对比 Standard SDS，变化 ~2× wall-clock speedup。
> - One-step Distillation (DMD) 上，Gradient variance reduction 为 3.4–16× reduction (resampling + stratification)，对比 DMD baseline (8,1)，变化 3.4–16×。

## 概要

在文本到3D优化、扩散蒸馏和数据归因等任务中，使用冻结扩散教师计算梯度时，蒙特卡洛估计的高方差是制约计算效率的核心瓶颈。该方差的根源在于时间步和噪声的随机采样，而渲染、编码或生成等上游操作的成本远高于去噪操作，使得简单地增加样本数以降低方差的策略代价高昂。

本文提出**CARV (Compute-Aware Variance-Reduction)**，一套计算感知的方差缩减策略，在不改变原始优化目标且保持无偏性的前提下，将计算开销从昂贵的上游操作转移至廉价的噪声采样上。CARV由三项互补技术构成：

1. **计算重用**：缓存昂贵的渲染或生成器输出，对每个缓存状态使用多组独立噪声进行重新去噪，在几乎不增加上游开销的情况下提升有效样本数。
2. **时间步重要性采样**：利用扩散教师显式权重函数构造提议分布，对时间步进行重加权采样，相比均匀采样获得约1.2倍方差缩减。
3. **分层采样**：将时间步域划分为等概率层，保证批次内噪声水平的均匀覆盖，可与重要性采样通过分层逆CDF结合，实现近最优的无偏分配。

实验表明，在文本到3D的SDS优化中，CARV提供**2–3倍的有效计算乘数**，以同等计算成本将收敛速度提升约2倍；在数据归因中，分层采样在合理预算下实现超过2倍的有效计算乘数；在一步蒸馏（DMD）中，梯度方差降低一个数量级以上。三项技术互补，组合使用时在推荐配置下可额外获得约25–31%的增益，且实现简单、即插即用。

值得注意的是，方差缩减并不总能转化为下游指标的提升——在DMD中尽管梯度方差大幅降低，FID并未改善——这揭示了方差与收敛动力学之间更深层的关系，也是未来研究的重要方向。



### 扩散模型作为冻结教师

扩散模型已成为高质量生成的核心组件，其训练目标通常表示为带权重 $w(t)$ 的期望形式：

$$
\mathcal{L}_{\mathrm{wDiff}}(\phi) = \underset{(\mathbf{x},\mathbf{c}),t,\epsilon}{\mathbb{E}}[w(t)\ell_{\mathrm{Diff}}(\mathrm{Encode}(\mathbf{x}),\mathbf{c},t,\epsilon,\phi)]
$$

其中 $\ell_{\mathrm{Diff}}$ 为每样本代价，$t$ 和 $\epsilon$ 分别表示时间步和噪声。当扩散模型训练完成后，它可以作为**冻结教师**嵌入到各类下游任务中，提供梯度信号来优化其他参数 $\theta$——例如文本到3D生成中的神经辐射场（NeRF）参数、一步蒸馏中的生成器参数，或数据归因中的影响函数计算。

### 三类典型下游任务中的梯度估计

**Score Distillation Sampling（SDS）** 是文本到3D优化的核心方法，其参数梯度方向为：

$$
\mathbf{u}_{\mathrm{SDS}}(\theta) = \underset{\alpha^\dagger c}{\mathbb{E}} \left[ w_{\mathrm{SDS}}(t) \mathbf{r}^{\mathrm{dz}}/\mathrm{d}\theta \right], \quad w_{\mathrm{SDS}}(t) = w(t) \alpha_t
$$

该方法利用扩散教师的去噪残差 $\mathbf{r}^{\mathrm{dz}}$ 通过链式法则反向传播至可微渲染器参数。

**Distribution Matching Distillation（DMD）** 旨在将多步扩散采样压缩为单步生成器，其梯度为两个得分函数之差的蒙特卡洛期望：

$$
\nabla_{\theta} D_{\mathrm{KL}} \simeq \underset{\epsilon, t, \epsilon'}{\mathbb{E}} \Big[ w(t) \alpha_t \big( \mathbf{s}_{\mathrm{fake}}(\mathbf{z}_t) - \mathbf{s}_{\mathrm{real}}(\mathbf{z}_t) \big) \frac{\partial \mathbf{z}_t}{\partial \theta} \Big]
$$

**数据归因** 通过计算查询样本与训练样本的归一化梯度余弦相似度来估计训练数据影响，其中共享的 $(t, \epsilon)$ 采样对直接影响归因排名的稳定性。

### 核心瓶颈：高方差蒙特卡洛估计

这三类任务的共同特征是：**梯度估计依赖于对时间步 $t$ 和噪声 $\epsilon$ 的蒙特卡洛采样**，而每次采样都需要执行昂贵的上游操作——SDS中的渲染与编码、DMD中的生成器前向传播、数据归因中的梯度计算。当这些上游操作的成本远高于去噪操作时，时间步和噪声引入的方差成为计算成本的主要瓶颈。

具体而言，标准做法采用 $t \sim \mathrm{Uniform}(t_{\min}, t_{\max})$ 和 $\epsilon \sim \mathcal{N}(0, I)$ 的独立同分布采样，每个样本仅执行一次上游计算和一次去噪（即 $K=1$）。这种朴素策略忽略了两个关键事实：

1. **不同时间步的梯度贡献差异显著**：某些噪声水平下的梯度范数远大于其他水平，均匀采样将大量计算浪费在低信息量的时间步上。
2. **上游计算结果可被复用**：缓存一次渲染或生成器输出后，可以用多组 $(t, \epsilon)$ 重新去噪，以极低的额外成本增加有效样本数。

### 现有方法的缺口

现有工作主要依赖下游指标（如CLIP分数、FID）来间接衡量优化质量，缺乏对**梯度估计方差本身**的系统测量和控制。少数方法尝试通过控制变量（如SteinDreamer）来降低方差，但这些方法通常改变了优化目标，引入了偏差。目前尚不存在一套**无偏、即插即用、计算感知**的方差缩减框架，能够在不修改原始损失函数的前提下，系统性地将计算开销从昂贵的上游操作转移到廉价的噪声采样上。

### 本文动机

本文提出 **CARV（Compute-Aware Variance-Reduction）**，一个由三项互补技术构成的方差缩减框架：

- **计算重用（重新去噪）**：缓存昂贵的上游计算结果，对每个缓存状态用 $K > 1$ 组噪声进行去噪，在不增加渲染/编码开销的情况下扩大有效样本量。
- **时间步重要性采样**：利用扩散教师固有的显式权重 $w(t)$ 构造提议分布 $q(t) \propto p(t) w(t)$，将采样密度集中在梯度范数较大的时间步上，以似然比修正保持无偏性。
- **分层逆CDF采样**：将时间步域划分为等概率层，保证批次内噪声水平的均匀覆盖，消除IID采样中的聚集效应，并可与重要性采样无缝结合。

这三项技术均不改变原始优化目标，实现简单，且相互补充。论文的目标是建立一个**计算感知的方差记账框架**，通过有效计算乘数（ECM）和相对效率（RE）等指标，量化每种技术在同等计算预算下的实际收益，并揭示方差缩减何时、为何能转化为下游性能提升——以及何时不能。



## 核心方法与创新机理

CARV（Compute-Aware Variance-Reduction）的核心创新在于**将方差缩减的视角从“优化目标设计”转向“梯度估计器的采样结构”**，在不修改原始损失函数的前提下，通过三个互补的采样策略实现2–3倍的有效计算乘数。其关键洞察是：在文本到3D优化、一步蒸馏和数据归因等任务中，渲染、编码或生成器前向传播等上游操作的成本远高于去噪操作，因此可以通过**缓存昂贵的中间结果**并**对廉价的噪声采样进行重分配**来换取方差缩减。

### 变更槽位一：从均匀采样到重要性采样

**基线做法**：标准SDS（DreamFusion、Magic3D、ProlificDreamer）在 $[t_{\min}, t_{\max}]$ 上对时间步进行均匀采样，每个渲染仅使用一对 $(t, \epsilon)$。

**CARV做法**：引入基于显式权重函数的重要性采样提议分布 $q(t) \propto p(t) w_{\text{SDS}}(t)$，其中 $w_{\text{SDS}}(t) = w(t) \alpha_t$ 是SDS更新方向中吸收调度系数的权重（Eq. 8）。该提议的构造几乎零额外开销，因为 $w_{\text{SDS}}(t)$ 本身就是扩散训练中已有的显式权重。采样后通过似然比 $\tilde{w}(t) = p(t)/q(t)$ 进行修正以保持无偏性。

**因果机制**：实证表明，$w_{\text{SDS}}(t)$ 主导了梯度范数在时间步上的依赖关系（App. Fig. 22），因此以 $w_{\text{SDS}}$ 为提议可近似理论最优的方差最小化分布 $q^\star(t) \propto p(t) \sqrt{\mathbb{E}[\|\mathbf{f}(t,\xi)\|_2^2 \mid t]}$（Eq. 24）。权重启发式实现达到神谕提议方差缩减的94–97%（Table 6, Fig. 23），单独使用时相比等K均匀采样提供约1.05–1.24倍相对效率（Table 2）。

### 变更槽位二：从IID采样到分层采样

**基线做法**：时间步在批次内独立同分布采样，无分层结构，导致某些噪声水平可能被过度采样而另一些被遗漏。

**CARV做法**：将时间步域划分为 $B$ 个等概率层，确保每个批次中不同噪声水平被均匀覆盖。具体实现分两种模式：
- **每渲染分层**（Eq. 15）：当 $K > 1$ 时，在每个渲染内部对 $K$ 个时间步进行分层采样，利用层次结构减少渲染内方差；
- **全局分层**（Eq. 14）：当 $K = 1$ 时，跨所有渲染进行全局分层，此时每渲染分层退化为均匀采样。

**因果机制**：分层采样通过强制覆盖整个时间步域来消除批次间的“聚集效应”（Fig. 2），减少因采样不均引入的方差。在 $K \in \{2,4,8\}$ 的甜区，单独分层采样提供约1.0–3.0倍有效计算乘数（Table 1），且在高 $K$ 下效果更显著。

### 变更槽位三：从单次去噪到计算重用（重新去噪）

**基线做法**：每个渲染仅进行一次去噪（$K=1$），梯度的有效样本数受限于昂贵的渲染次数。

**CARV做法**：缓存每个渲染结果 $\mathbf{x}^{(r)}$，然后对同一缓存状态采样多组 $(t, \epsilon)$ 进行重新去噪（Eq. 13）：
$$\hat{\nabla}_{\boldsymbol{\theta}}^{\mathrm{reuse}} = \frac{1}{R} \sum_{r=1}^{R} \Big( \frac{1}{K} \sum_{k=1}^{K} \mathbf{f}(\mathbf{x}^{(r)}, t^{(r,k)}, \epsilon^{(r,k)}) \Big) \frac{\partial \mathbf{x}^{(r)}}{\partial \boldsymbol{\theta}}$$

该估计器是无偏的，因为 $(t, \epsilon)$ 独立于 $\mathbf{x}^{(r)}$ 重采样。其成本为 $R(c_{\text{render+encode}} + K c_{\text{denoise}})$，当 $c_{\text{render+encode}} \gg c_{\text{denoise}}$ 时，可在几乎不增加总成本的情况下大幅增加有效样本数。

**因果机制**：计算重用的增益高度依赖于渲染与去噪的成本比值（App. Fig. 21）。在文本到3D优化中，渲染成本主导总开销，因此 $K=8$ 时仅计算重用即可提供约2.6倍有效计算乘数（Fig. 5）。当上游成本可忽略时，最优 $K$ 较小。

### 三个策略的互补性

重要性采样、分层采样和计算重用是**互补而非替代**的关系。分层采样确保时间步覆盖的均匀性，重要性采样将更多概率质量分配到高梯度范数的区域，而计算重用则在固定渲染预算下增加去噪样本数。组合IW和分层采样在 $K \in \{2,4,8\}$ 的甜区相比均匀采样额外提供约25–31%的方差缩减（Fig. 11），三者联合在 $(R=1, K=8)$ 配置下达到约3.3倍有效计算乘数（Table 1, Fig. 5）。

### 变更槽位四：方差测量与效率指标

**基线做法**：无系统方差测量，通常依赖下游指标（如CLIP分数、FID）间接评估。

**CARV做法**：建立计算感知的方差记账框架（Sec. 3.2），使用Welford在线算法估计参数梯度的协方差迹 $\operatorname{tr}(\operatorname{Cov}(\nabla_{\boldsymbol{\theta}}))$，并定义两个效率指标：
- **有效计算乘数**（ECM）：在等方差条件下，基线成本与方法成本的比值；
- **相对效率**（RE）：在相同 $(R, K)$ 配置下，均匀采样方差与方法方差的比值。

该框架使得不同采样策略可以在**相等每轮计算成本**下进行公平比较，而非仅比较等迭代数的方差。所有实验均以wall-clock时间为成本度量，确保对比的公平性。



CARV (Compute-Aware Variance-Reduction) 是一个在冻结扩散教师下进行无偏梯度估计的方差缩减框架。其核心思想是：将计算开销从昂贵的上游操作（渲染、编码、生成器前向传播）转移到廉价的噪声采样和去噪操作上，同时保持估计器的无偏性。框架由三个互补的技术模块和一个计算感知的方差记账系统构成。

### Pipeline 总览

整个框架围绕一个层次化的蒙特卡洛估计器组织。给定一批需要优化的参数 $\theta$（例如 NeRF 权重、生成器参数），一次完整的梯度估计迭代包含以下步骤：

1. **渲染/编码缓存**：对 $R$ 个渲染视角或生成器输出进行一次性前向计算，将结果 $\mathbf{x}^{(r)}$ 缓存。这是整个 pipeline 中计算成本最高的环节。

2. **重新去噪模块**：对每个缓存状态 $\mathbf{x}^{(r)}$，独立采样 $K$ 组时间步和噪声对 $(t^{(r,k)}, \epsilon^{(r,k)})$，执行去噪计算得到残差 $\mathbf{f}(\mathbf{x}^{(r)}, t^{(r,k)}, \epsilon^{(r,k)})$。$K$ 的增大几乎不增加上游开销，仅增加廉价的去噪计算。

3. **重要性采样模块**：时间步的采样分布从均匀分布 $p(t)$ 替换为提议分布 $q(t) \propto p(t) w(t)$，其中 $w(t)$ 是扩散教师的显式权重函数（在 SDS 中为 $w_{\text{SDS}}(t) = w(t)\alpha_t$）。采样后通过似然比 $\tilde{w}(t) = p(t)/q(t)$ 进行修正以保持无偏性。

4. **分层采样模块**：将时间步域划分为 $B$ 个等概率层，在每个渲染内部（当 $K > 1$ 时）或全局范围内（当 $K = 1$ 时）保证时间步的均匀覆盖。当与重要性采样结合时，通过逆 CDF 映射实现分层逆变换采样。

5. **梯度组装**：将每个渲染下经过分层-IS 平均后的贡献组合为参数梯度，根据链式法则进行反向传播。

### 模块关系与数据流

三个方差缩减技术是正交且互补的。重新去噪利用渲染/去噪成本的不对称性，在固定总计算预算下增加有效样本数；重要性采样将概率质量集中到梯度范数较大的时间步区域；分层采样消除批次内时间步的随机聚集，保证噪声水平的均匀覆盖。三者可以任意组合，且均为无偏的 drop-in 替换，不改变原始优化目标（SDS、DMD 或数据归因损失）。

### 效率度量框架

CARV 包含一个计算感知的方差记账系统，用于公平比较不同采样策略。核心指标包括：

- **有效计算乘数 (ECM)**：在等方差条件下，基线方法所需计算成本与提出方法所需计算成本的比值 $\text{ECM} = \text{cost}_{\text{baseline}} / \text{cost}_{\text{method}}$。
- **相对效率 (RE)**：在相同 $(R, K)$ 配置下，均匀采样的方差与提出方法的方差之比 $\text{RE} = \text{Var}_u / \text{Var}_m$。

方差测量使用 Welford 在线算法，无需存储完整样本序列，并与高样本参考值进行交叉验证以确保估计准确。所有比较均在相等的每轮计算成本（wall-clock time）下进行。

### 关键设计选择

- **每渲染分层 vs. 全局分层**：当 $K > 1$ 时，每渲染分层利用层次结构降低渲染内方差，与计算重用自然组合；当 $K = 1$ 时，每渲染分层退化为均匀采样，此时应使用全局分层。
- **重要性采样提议**：使用基于显式权重的启发式提议 $q(t) \propto p(t) w(t)$，该提议实现简单、几乎零额外开销，且能达到神谕最优提议方差缩减的 94–97%。
- **计算重用倍数 $K$ 的选择**：最优 $K$ 取决于上游成本与去噪成本的比值。当渲染/编码成本远高于去噪时，增大 $K$ 带来显著增益；当上游成本可忽略时，较小的 $K$ 即可。



### 3.1 问题形式化：扩散期望的蒙特卡洛估计

CARV 针对的核心计算模式可统一表述为：对冻结扩散教师的期望进行蒙特卡洛估计，其中被积函数包含一个**昂贵的前向计算**（渲染、编码或生成器前传）和一个**廉价的去噪残差计算**。该模式覆盖 SDS、DMD 和数据归因三类下游任务。

令 $\mathbf{x}^{(r)} = g(\boldsymbol{\theta}, \boldsymbol{\xi}^{(r)})$ 表示第 $r$ 次上游计算（如 NeRF 渲染），$\mathbf{f}(\mathbf{x}^{(r)}, t, \epsilon)$ 为去噪残差。标准的一次性估计器为：

$$
\hat{\nabla}_{\boldsymbol{\theta}}^{\mathrm{naive}} = \frac{1}{R} \sum_{r=1}^{R} \mathbf{f}(\mathbf{x}^{(r)}, t^{(r)}, \epsilon^{(r)}) \frac{\partial \mathbf{x}^{(r)}}{\partial \boldsymbol{\theta}}
$$

其中每个样本消耗一次上游计算和一次去噪调用。当上游成本 $c_{\mathrm{render}} + c_{\mathrm{encode}} \gg c_{\mathrm{denoise}}$ 时，该方案将大部分计算预算浪费在昂贵的操作上，而非在噪声空间进行更多采样以降低方差。

### 3.2 核心模块一：计算重用与重新去噪

**设计动机**：上游计算（渲染/编码）的输出 $\mathbf{x}^{(r)}$ 在给定 $\boldsymbol{\theta}$ 下是确定性的，而方差的主要来源是时间步 $t$ 和噪声 $\epsilon$ 的随机采样。因此，缓存每个 $\mathbf{x}^{(r)}$ 并用多组 $(t, \epsilon)$ 重新去噪，可在不增加上游开销的情况下增加有效样本数。

**层次化估计器**（Eq. 13）：

$$
\hat{\nabla}_{\boldsymbol{\theta}}^{\mathrm{reuse}} = \frac{1}{R} \sum_{r=1}^{R} \left( \frac{1}{K} \sum_{k=1}^{K} \mathbf{f}(\mathbf{x}^{(r)}, t^{(r,k)}, \epsilon^{(r,k)}) \right) \frac{\partial \mathbf{x}^{(r)}}{\partial \boldsymbol{\theta}}
$$

**变量含义**：
- $R$：渲染/上游计算的总次数
- $K$：每个渲染对应的重新去噪次数（每组使用独立的 $(t, \epsilon)$）
- $\mathbf{x}^{(r)}$：第 $r$ 次渲染的缓存输出
- $t^{(r,k)}, \epsilon^{(r,k)}$：第 $r$ 个渲染下的第 $k$ 组时间步和噪声样本

**关键性质**：
- **无偏性**：$(t, \epsilon)$ 独立于 $\mathbf{x}^{(r)}$ 采样，不改变期望
- **计算成本**：$R \cdot (c_{\mathrm{render}} + c_{\mathrm{encode}} + K \cdot c_{\mathrm{denoise}})$，将开销从昂贵操作转移至廉价去噪
- **有效样本数**：总计 $R \times K$ 个去噪残差，但仅需 $R$ 次上游计算

当 $K > 1$ 时，该模块构成后续分层策略的层次结构基础：外层循环遍历渲染，内层循环在每个渲染内执行 $K$ 次去噪。

### 3.3 核心模块二：时间步重要性采样

**设计动机**：均匀采样 $t \sim \mathcal{U}[t_{\min}, t_{\max}]$ 忽略了不同噪声水平对梯度方差的贡献差异。实验表明，SDS 的显式权重函数 $w_{\mathrm{SDS}}(t) = w(t) \alpha_t$ 与每时间步梯度范数高度相关（App. Fig. 22），因此可直接用作重要性采样的提议分布。

**提议分布**：

$$
q(t) \propto p(t) \cdot w_{\mathrm{SDS}}(t)
$$

其中 $p(t)$ 为训练时的先验分布（通常为均匀分布）。

**重要性加权估计器**（Eq. 5 框架）：

$$
\hat{\boldsymbol{\mu}}_q = \frac{1}{N} \sum_{n=1}^{N} \tilde{w}(t^{(n)}) \cdot \mathbf{f}(t^{(n)}, \boldsymbol{\xi}^{(n)}), \quad \tilde{w}(t) = \frac{p(t)}{q(t)}
$$

似然比 $\tilde{w}(t)$ 保证无偏性：从 $q$ 采样但用 $p/q$ 加权，等价于从 $p$ 采样的期望。

**与理论最优提议的关系**：方差最小的理论最优提议为 $q^\star(t) \propto p(t) \sqrt{\mathbb{E}[\|\mathbf{f}(t, \boldsymbol{\xi})\|_2^2 \mid t]}$（Eq. 24）。权重启发式 $w_{\mathrm{SDS}}(t)$ 作为其代理，实现了 Oracle 提议方差缩减的 94–97%，且几乎零额外计算开销（Table 6, Fig. 23）。

### 3.4 核心模块三：分层采样及其与重要性采样的结合

**设计动机**：IID 采样可能在批次中遗漏某些噪声水平区间，导致高方差。分层采样将时间步域划分为 $B$ 个等概率（或等权重）层，每层采样一个点，保证批次内对噪声水平的均匀覆盖。

**每渲染分层估计器**（Eq. 15）：

$$
\bar{\mathbf{f}}_{\mathrm{strat}}^{(r)} = \frac{1}{B} \sum_{b=1}^{B} \mathbf{f}(\mathbf{x}^{(r)}, t_b^{(r)}, \epsilon_b^{(r)})
$$

其中 $t_b^{(r)}$ 从第 $b$ 层采样，$B = K$ 即每渲染的重新去噪次数。

**分层-重要性采样结合**（Eq. 17）：

当同时使用重要性采样和分层采样时，通过逆 CDF 映射将分层均匀样本转换到提议分布的分位点空间：

$$
u_b^{(r)} = \frac{b - 1 + \xi_b^{(r)}}{B}, \quad t_b^{(r)} = \mathrm{CDF}_q^{-1}(u_b^{(r)})
$$

其中 $\xi_b^{(r)} \sim \mathcal{U}[0, 1]$ 为层内随机扰动。对应的每渲染贡献为：

$$
\bar{\mathbf{f}}_{\mathrm{strat-IS}}^{(r)} = \frac{1}{B} \sum_{b=1}^{B} \tilde{w}(t_b^{(r)}) \cdot \mathbf{f}(\mathbf{x}^{(r)}, t_b^{(r)}, \boldsymbol{\epsilon}_b^{(r)})
$$

**分层策略选择**：
- **每渲染分层**（Eq. 15/17）：在 $K > 1$ 时优先使用，利用层次结构降低渲染内方差，与计算重用自然组合
- **全局分层**（Eq. 14）：当 $K = 1$ 时每渲染分层退化为均匀采样，此时应使用全局分层，将所有 $R \times K$ 个样本统一分层

### 3.5 方差测量与效率指标

**方差定义**（Eq. 3）：对无偏向量估计器 $\hat{\boldsymbol{\mu}}$，方差定义为协方差矩阵的迹：

$$
\operatorname{Var}(\hat{\boldsymbol{\mu}}) := \mathbb{E}[\|\hat{\boldsymbol{\mu}} - \boldsymbol{\mu}\|_2^2] = \operatorname{tr}(\operatorname{Cov}(\hat{\boldsymbol{\mu}}))
$$

该标量度量了参数梯度各分量方差的聚合，等价于均方误差。

**效率指标**：效率与方差和计算成本的乘积成反比，即 $\propto 1 / (\mathrm{Var} \cdot \mathrm{cost})$。基于此定义两个核心指标：

- **有效计算乘数** (ECM)：在等方差条件下，基线方法的计算成本与方法计算成本的比值。ECM $> 1$ 表示方法更高效
- **相对效率** (RE)：在相同 $(R, K)$ 配置下，均匀采样的方差与方法方差的比值。RE $> 1$ 表示方法在同等计算量下方差更低

**测量方法**：使用 Welford 在线算法估计方差，无需存储全部样本；通过将估计器运行至收敛并与高样本参考值交叉验证，确保估计准确性（Sec. 3.2）。

### 3.6 完整算法流程

CARV 的完整梯度估计流程（Algorithm 1）：

1. **渲染缓存**：对每个渲染视角 $r = 1, \ldots, R$，计算 $\mathbf{x}^{(r)} = g(\boldsymbol{\theta}, \boldsymbol{\xi}^{(r)})$ 并缓存
2. **分层-IS 采样**：对每个渲染，使用逆 CDF 映射从提议分布 $q$ 的分层中采样 $K$ 组 $(t_b^{(r)}, \epsilon_b^{(r)})$
3. **去噪与加权**：计算去噪残差 $\mathbf{f}(\mathbf{x}^{(r)}, t_b^{(r)}, \epsilon_b^{(r)})$，乘以重要性权重 $\tilde{w}(t_b^{(r)})$
4. **层内平均**：对每个渲染的 $K$ 个贡献取平均，得到 $\bar{\mathbf{f}}_{\mathrm{strat-IS}}^{(r)}$
5. **梯度组装**：通过链式法则组合为参数梯度 $\hat{\nabla}_{\boldsymbol{\theta}} = \frac{1}{R} \sum_{r=1}^{R} \bar{\mathbf{f}}_{\mathrm{strat-IS}}^{(r)} \frac{\partial \mathbf{x}^{(r)}}{\partial \boldsymbol{\theta}}$

三个模块（计算重用、重要性采样、分层采样）均为**无偏的即插即用替换**，不改变原始优化目标，仅替换采样策略。



## 实验与关键发现

### 核心方差缩减效果：SDS 文本到3D优化

CARV 在 SDS 文本到3D 优化中实现了显著的有效计算乘数（ECM）。**Table 1** 报告了不同重去噪次数 $K$ 下的 ECM 值：仅计算重用（Uniform, $K>1$）即可达到约 2.6× 的 ECM；组合重要性加权与分层采样（IW+Strat）在 $(R=1, K=8)$ 配置下达到约 3.3× 的 ECM，这意味着在同等方差水平下，该方法仅需基线约 30% 的计算成本。

**Table 2** 进一步分解了各技术的相对效率（RE，即等 $(R,K)$ 配置下与均匀采样的方差比）。重要性加权单独提供约 1.05–1.24× 的 RE，分层采样单独提供约 1.0–3.0× 的 RE（取决于 $K$），两者组合后在 $K \in \{2,4,8\}$ 的甜区提供额外约 25–31% 的增益。这一互补性在 **Figure 11** 中得到详细量化：以 $(R=1, K=4)$ 为例，计算重用使方差降至基线的约 50%，同时成本降至约 65%；叠加 IW 和分层后进一步压缩方差。


![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/017_Figure_11.jpg]]
*Figure 11: Quantifying variance reduction from hierarchical cost awareness with importance weighting (IW) and stratification (Strat.). Combined effect of IW, stratification, and compute reuse on variance and ECM. Left: Variance (MSE to the ground-truth gradient late in SDS training, equal to variance for unbiased estimators) versus compute. Colors: uniform, IW, Strat, IW+Strat (red); points annotated by ( R , K ) . Middle: ECM vs. the uniform $\bar { ( }$ R = 2 , K = 1 ) baseline. Best K = 8 rows reach $\sim$ 2 . 6 $\times$ (uniform), $\sim$ 3 . 0 $\times \mathrm { ( I W ) }$ ， $\sim$ 3 . 0 $\times$ (Strat.), ∼ 3.3× (IW+Strat). Right: ECM isolating IW/Strat gains at fixed ( R , K ) ${ \mathrm { : } }$ Strat $\sim$ 1 0...

**Figure 5** 从方差-计算量曲线给出了更直观的视角：IW+Strat 的曲线始终位于均匀基线下方，在等计算量下方差更低，在等方差下所需计算量更少。底部面板直接给出 ECM 随计算量变化的趋势。


![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/006_Figure_5.jpg]]
*Figure 5: Quantifying variance reduction from IW and stratification (SDS). Top: Variance $\operatorname { \mathrm { ( t r } } ( \operatorname { C o v } ( \nabla _ { \pmb { \theta } }$ ) ) ) late in training) vs. compute. Colors: uniform baseline and IW+Strat. Points annotated by ( R , K ) . Bottom: Effective compute multiplier vs. uniform baseline. Lines trace ( $\dot { R _ { } }$ = 1 , K ) , peaking at (1, 8): $\mathrm { \sim }$ 2 . 6 $\times$ (uniform), ∼ 3.3× (IW+Strat). Ablations in App. Fig. 11; breakdowns in Tables 1, 2. Figure 6: Quantifying Changes in Data Attribution. Top: Gradient variance vs. evaluations per data point. Stratified sampling beats uniform sampling at an equal budget. Bottom: Mean co...

### 下游性能增益

方差缩减转化为实际优化加速。**Figure 7** 展示了 CLIP 分数随迭代次数的变化（30 个提示词、3 个随机种子、多视角平均，等每轮计算成本约 300–400 ms）。IW+Strat 方法在约一半的迭代步数内达到基线收敛后的 CLIP 分数，对应约 2× 的实际加速。**Figure 8** 的定性渲染轨迹进一步佐证：在固定计算预算下，CARV 的优化结果在早期迭代即展现出更清晰的几何结构和更好的提示对齐度。

### 一步蒸馏（DMD）中的方差缩减与下游指标的脱节

在 DMD 实验中，方差缩减效果更为剧烈。**Table 3** 显示，重采样配置 $(R=8, K=16)$ 相比 $(R=8, K=1)$ 将参数梯度方差从 982 降至 59.9（约 16× 降低）；在此基础上叠加分层采样进一步降至 30.7（再降低约 2×）。教师评分和评分差异的方差同样降低 3.4–16×。

然而，**这些大幅方差缩减并未转化为 FID 的改善**。这是一个关键的失败模式：梯度估计精度的提升并未改变生成器的收敛行为，暗示 DMD 的优化动态可能由辅助损失或双层优化中的其他因素主导。该发现被列为开放问题，需要进一步研究。

### 数据归因中的分层采样优势

在数据归因任务中，分层采样在等预算下一致优于均匀采样。**Table 4** 报告了不同评估预算下的有效计算乘数：预算为 4 时达到 2.44×，预算为 64 时达到 3.82×，在典型实际预算下均超过 2×。**Figure 6** 的上方面板展示了梯度方差随每数据点评估次数的下降趋势，下方面板展示了有限评估排名与真实梯度的平均相关性——分层采样在更少的时间步下实现更高的相关性。

值得注意的是，数据归因中重要性采样的收益有限。这是因为该任务下梯度范数在时间步上近似恒定（App. Fig. 29），使得均匀采样已接近最优提议，权重启发式无法提供额外增益。这揭示了该方法的一个边界条件：**当显式权重与梯度范数的相关性较弱时，重要性采样的边际收益会缩小**。

### 消融实验关键发现

1. **权重启发式的重要性采样几乎达到神谕性能**：**Figure 23** 比较了均匀采样、权重启发式提议 $q(t) \propto p(t) w_{\text{SDS}}(t)$ 和不可行的理论最优提议。权重启发式实现了神谕提议方差缩减的 94–97%，且几乎零额外开销（Table 6）。


![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/031_Figure_23.jpg]]
*Figure 23: Importance Sampling Strategy Comparison: Weight-Based Heuristic versus Oracle. This figure compares three importance sampling approaches for parameter gradient estimation: uniform sampling (baseline), our weight-based importance sampling using q ( t ) $\propto$ p ( t ) $w _ { \mathrm { S D S } }$ ( t ) as described in Sec. 3.1.2, and the intractable oracle proposal $q ^ { \star }$ ( t ) $\propto$ p ( t ) \| $\nabla _ { \theta } \mathbf { \bar { f } }$ ( t ) \| that requires computing per-timestep gradient norms. L e f t ${ \mathrm { : } }$ Parameter gradient variance versus compute budget in milliseconds. Points are annotated by ( R , K ) configurations. M i d d l e { : } Effective compute multiplier i...

2. **每渲染分层 vs. 全局分层**：当 $K>1$ 时，每渲染分层（Eq. 15）优于全局分层（Eq. 14），因为它利用了层次化结构减少渲染内方差；当 $K=1$ 时每渲染分层退化为均匀采样，此时全局分层是必要选择（App. Fig. 24）。


![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/032_Figure_24.jpg]]
*Figure 24: Comparing Per-Render and Global Stratification Strategies. This figure ablates two stratified sampling approaches: per-render stratification (Eq. 15), which stratifies timesteps independently within each render’s K re-noisings, versus global stratification (Eq. 14), which stratifies timesteps across all R $\times$ K samples in the batch. Left: Variance versus compute budget for uniform baseline (orange), global stratification (green), and per-render stratification (purple). Points are annotated by (R, K) configurations. Middle: Effective compute multiplier isolating the gain from stratification by comparing to uniform sampling at the same (R, K) configuration. Right: Effective compute multipl...*

3. **计算重用的成本依赖性**：重去噪的增益高度依赖于上游操作（渲染/编码）与去噪操作的成本比值。当上游成本远大于去噪成本时，增大 $K$ 可显著提升效率；当上游成本可忽略时，最优 $K$ 较小（App. Fig. 21）。在 SDS 实验中，渲染成本占主导，因此 $K=8$ 附近为甜区。


![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/027_Figure_21.jpg]]
*Figure 21: Sensitivity of variance reduction to render-vs-denoise cost ratio. Analysis of Fig. 11 repeated with simulated cost $\boldsymbol { B } = \alpha \boldsymbol { R } + \boldsymbol { R } \boldsymbol { K }$ to isolate render cost. Top (α = 0): Render free; re-noising still reduces variance but benefit saturates ( K $\leq$ 2 ) . Bottom ( $\alpha$ = 1 ) $\colon$ Equal cost; higher K gives larger ECM as render amortization grows. Colors and annotations follow Fig. 11

4. **提示词鲁棒性**：**Table 7** 的提示词消融显示，IW+Strat 在五个不同提示词下均以 $\bar{K}=8$ 为最优配置，表明该方法对提示词变化具有较好的鲁棒性。


![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/033_Table_7.jpg]]
*Table 7: Prompt ablation for variance reduction methods. Five prompts (emerald beetle, gold mask, mahogany piano, orchid pot, teddy bear). (a) ECM for IW+Strat by K; $\bar { \boldsymbol { K } } = \bar { \boldsymbol { 8 } }$ is optimal across prompts. (b) RE vs. uniform for IW+Strat; peak at K = 2 - 4 . (c) ECM for all methods at K = 8 ; rankings (IW+Strat > IW ≈ Strat > Uniform) are stable. (d) RE vs. uniform at K = 8 ; $\operatorname { I W }$ and Strat are complementary across prompts. (a) ECM by K (IW+Strat)

### 公平性保障

所有比较均在**相等的每轮计算成本（wall-clock time）**下进行。方差测量使用 Welford 在线算法，并与高样本参考值交叉验证以确保估计准确。所提方法均为**无偏估计器**，不改变原始优化目标，仅替换采样策略，因此性能提升完全归因于方差缩减而非目标函数的修改。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/015_Figure.jpg]]
*Figure: Total Time (ms) Per-Iteration Compute (ms)*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/019_Figure_13.jpg]]
*Figure 13: Variance reduction across training, low classifier-free guidance $\left( \omega$ = 2 5 $\right$) . Analogous to Fig. 11, measured at three optimization checkpoints. Rows: training step 1000, 2000, and 9000. Left: variance vs. compute. Middle: effective compute multiplier vs. the uniform ( R = 2 , K = 1 ) baseline. Right: relative efficiency vs. uniform at matched ( R , K ) . Higher K wins more strongly early in training, when rendering is more expensive relative to denoising and re-noising amortizes that cost most efficiently; the gap closes in late training but variance reduction continues to dominate the uniform baseline at every checkpoint, demonstrating that the wins persist throughout opti...

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/020_Figure.jpg]]
*Figure: Total Time (ms) Per-Iteration Compute (ms)*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/022_Figure.jpg]]
*Figure: Total Time (ms) Per-Iteration Compute (ms)*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/030_Figure_22.jpg]]
*Figure 22: Weight function closely tracks gradient magnitude across timesteps. We visualize empirical gradient norms as a function of timestep t during SDS optimization, alongside the proposal densities used for importance sampling (right axes). Left: Latent-space gradient contribution \| $w _ { \mathrm { S D S } }$ ( t ) $\mathbf { r }$ \|$_ { 2 }$ , where ${ \bf$ r } = $\hat { \epsilon } _ { \phi } ( { \bf$ z $} _ { t }$ , t , ${ \bf$ c } ; $\omega$ ) - $\epsilon$ is the noise prediction residual. Right: Full parameter gradient norm \| $\mathbf { f }$ ( t , $\pmb { \xi }$ ) \|$_ { 2 }$ aggregated over camera views, renders, and noise. The weight-based proposal q \ $\propto$ \ p ( t ) $w _ { \mathrm { S D S } }$ ( t ) closely...

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2605_21489/figures/035_Figure.jpg]]
*Figure: Training Steps (×1000) Training Steps (×1000) Total Training Time (hours) Total Training Time (hours)*




## 定位与知识库关联

### 问题定位：扩散教师期望中的梯度估计方差

CARV 针对的核心瓶颈是：在使用冻结扩散模型作为“教师”时，下游任务（文本到3D优化、一步蒸馏、数据归因）的梯度蒙特卡洛估计存在高方差。该方差主要来源于时间步 $t$ 和噪声 $\epsilon$ 的随机采样。当上游操作（渲染、编码、生成器前向）的成本远高于去噪操作时，传统的“每样本一次渲染、一次去噪”（K=1）策略将大量计算预算浪费在昂贵的上游操作上，而廉价的噪声采样未被充分利用。

这一瓶颈在多个代表性工作中普遍存在：**DreamFusion**（Poole et al., 2022）引入的 SDS 梯度估计器、**Magic3D**（Lin et al., CVPR 2023）和 **ProlificDreamer**（Wang et al., NeurIPS 2023）均采用均匀时间步采样和 K=1 的默认配置；**DMD**（Yin et al., 2023）在一步蒸馏中同样依赖对时间步和噪声的蒙特卡洛平均；基于梯度的数据归因方法（如 **TRAK**（Park et al., 2023）和 **TracIn**（Pruthi et al., 2020））在计算每个训练样本的影响分数时，也需要对扩散时间步进行重复采样。

### 方法谱系：方差缩减技术的整合与适配

CARV 并非提出全新的方差缩减理论，而是将三类经典技术——计算重用、重要性采样、分层采样——系统性地适配到扩散教师期望的特定计算结构上，并通过计算感知的记账框架（ECM/RE）进行统一评估。

**1. 计算重用（Amortized Re‑noising）**

核心思想源于分层蒙特卡洛：将昂贵的外层采样（渲染/编码）与廉价的内层采样（噪声/时间步）解耦。对每个缓存的上游输出，用 $K$ 组独立的 $(t, \epsilon)$ 重新去噪（Eq. 13），在不增加上游开销的情况下增加有效样本数。这一策略的有效性高度依赖于上游成本与去噪成本的比值：当渲染成本主导时（如 NeRF 渲染），$K$ 可取较大值；当上游成本可忽略时，最优 $K$ 较小（App. Fig. 21）。该技术与 **SteinDreamer**（控制变量法）等方法正交，理论上可叠加使用。

**2. 重要性采样（Importance Sampling）**

将时间步采样从均匀分布 $p(t)$ 替换为提议分布 $q(t) \propto p(t) w_{\text{SDS}}(t)$，并用似然比 $\tilde{w}(t) = p(t)/q(t)$ 保持无偏。这一设计的核心洞察是：SDS 的显式权重函数 $w_{\text{SDS}}(t)$ 在经验上主导了梯度范数对时间步的依赖（App. Fig. 22），因此使用该权重作为代理提议几乎不需要额外计算开销，却能实现 Oracle 最优提议（Eq. 24）方差缩减的 94–97%（Table 6, Fig. 23）。与需要在线估计梯度范数的自适应重要性采样方法相比，CARV 的权重启发式方案实现简单、即插即用。

**3. 分层采样（Stratified Sampling）**

将时间步域划分为 $B$ 个等概率层，保证每个批次中不同噪声水平均匀覆盖。CARV 区分了两种分层策略：当 $K>1$ 时，每渲染分层（Eq. 15）利用层次结构降低渲染内方差；当 $K=1$ 时，每渲染分层退化为均匀采样，此时全局分层（Eq. 14）是必要替代（App. Fig. 24）。分层采样可与重要性采样通过逆 CDF 映射无缝结合（Eq. 17, Fig. 4），实现分层-重要性采样（Stratified-IS），在 $K \in \{2,4,8\}$ 的甜区提供约 25–31% 的额外增益（Fig. 11）。

### 与基线方法的关系

CARV 的三种技术均为**无偏估计器**，不修改原始优化目标（SDS、DMD、归因损失），仅替换采样策略。因此，它们可以作为即插即用的 drop‑in 替换，直接应用于现有框架：

- 相对于 **Standard SDS**（DreamFusion/Magic3D/ProlificDreamer 的默认配置：均匀采样，K=1），CARV 在同等每轮计算成本下实现约 3.3× 有效计算乘数（IW+Strat, R=1, K=8; Fig. 5, Table 1），CLIP 分数收敛速度约提升 2×（Fig. 7）。
- 相对于 **DMD baseline**，重采样（8,16）将参数梯度方差降低 3.4–16×，分层进一步降低约 2×（Table 3）。
- 相对于 **TRAK/TracIn** 的均匀时间步采样，分层采样在合理预算下实现 >2× 有效计算乘数（Table 4, Fig. 6）。

### 适用边界与局限

**1. 方差缩减不保证下游指标提升**

这是 CARV 最关键的适用边界。在 DMD 一步蒸馏中，梯度方差降低了 3.4–16×，但下游 FID 并未改善（Sec. 4.2, Table 3）。这表明 DMD 的收敛行为可能由辅助损失或双层优化动态主导，而非梯度估计精度。类似地，在数据归因中，重要性采样的收益有限，因为梯度范数在时间步上近似恒定（App. Fig. 29）。用户需根据具体任务验证方差缩减是否转化为实际收益。

**2. 计算重用依赖成本比值**

重新去噪的增益高度依赖于上游成本与去噪成本的比值。当上游操作廉价（如轻量生成器前向）或输入可变性占主导时，增加 $K$ 的边际增益会缩小（App. Fig. 21）。框架假设教师模型保持冻结；在教师被微调或联合适应的场景下，需考虑参数漂移对采样策略的影响。

**3. 权重启发式的任务依赖性**

基于 $w_{\text{SDS}}(t)$ 的重要性采样代理假设显式权重与梯度范数相关。当该假设不成立时（如数据归因中梯度范数在时间步上近似恒定），该策略收益有限。对于新任务，建议先运行方差扫描以确认权重启发式的有效性。

**4. 方差测量框架的前期开销**

ECM/RE 的计算需要将每个估计器运行至收敛（Sec. 3.2），这在方法比较时引入前期计算开销。论文的 SDS 评估使用了较旧的堆栈（Stable Diffusion 2.1, NeRF）；虽然框架本身对教师和渲染器不敏感，但更先进的堆栈可能需要重新运行方差扫描以获得精确的 ECM 值。

### 开放问题

1. **方差缩减到下游指标的转化条件**：为何 DMD 中方差缩减未带来 FID 提升？哪些辅助损失或双层优化动态主导了收敛行为？能否建立理论或经验原则预测转化条件？

2. **与非冻结教师的兼容性**：如何将方差缩减扩展至教师被微调或联合适应的设置，并处理教师参数漂移对时间步采样策略的影响？

3. **与其他方差缩减技术的组合**：方差缩减能否与 **SteinDreamer** 等控制变量方法结合，实现加性改善？分层和重要性采样在与梯度截断、引导截断等有偏技术的交互中，能否通过轻微引入偏差来交换更大的方差缩减？

4. **自适应超参数选择**：能否通过 AutoML 或任务选择工具为新提示和模态自适应选择估计器超参数 $(R, K)$？

5. **跨模态扩展**：在 4D 场景优化、音频生成、物理仿真等跨模态任务中扩展方差缩减，并评估在不同教师架构和预测参数化下的迁移效果。

6. **最优配对分布的在线近似**：如何在不解决完整传输问题的情况下，在线近似 Sinkhorn 最优配对分布以进一步降低方差？



## 原文 PDF

![[paperPDFs/ICML_2026/Variance_Reduction_for_Expectations_with_Diffusion_Teachers.pdf]]
