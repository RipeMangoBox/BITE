---
title: "SenCache: Accelerating Diffusion Model Inference via Sensitivity-Aware Caching"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SenCache_Accelerating_Diffusion_Model_Inference_via_Sensitivity_Aware_Caching.pdf
project_link: null
code_link: "https://github.com/vita-epfl/SenCache.git"
aliases:
- SSAC
- SenCache
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 基于去噪器对噪声潜在表示 x_t 和时间步 t 的局部 Jacobian 范数的一阶敏感性分数 S_t，并设置容忍度 ε 控制缓存重用决策：当 S_t ≤ ε 时重用缓存输出。
primary_logic: 用网络输出的 Jacobian 范数作为局部 Lipschitz 常数，显式建模潜在向量漂移和时间步间隔对输出的影响，从而建立有理论保证的自适应缓存准则，统一解释了先前启发式方法的有效性及失败原因。
claims:
- SenCache uses a theoretically motivated measure of network sensitivity to its input perturbations as the criterion for caching.
- "Cache rule: cache at step t if sensitivity score S_t ≤ ε."
- Both latent and timestep sensitivities contribute significantly, and effective caching criteria must account for both terms.
- Experiments on Wan 2.1, CogVideoX, and LTX-Video show that SenCache achieves better visual quality than existing caching methods under similar computational budgets.
---

# SenCache: Accelerating Diffusion Model Inference via Sensitivity-Aware Caching

> [!tip] 核心洞察
> 用网络输出的 Jacobian 范数作为局部 Lipschitz 常数，显式建模潜在向量漂移和时间步间隔对输出的影响，从而建立有理论保证的自适应缓存准则，统一解释了先前启发式方法的有效性及失败原因。

| 字段 | 内容 |
|------|------|
| 中文题名 | SenCache: 基于灵敏度感知缓存的扩散模型推理加速 |
| 英文题名 | SenCache: Accelerating Diffusion Model Inference via Sensitivity-Aware Caching |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.24208) · [Code](https://github.com/vita-epfl/SenCache.git) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | SenCache (Sensitivity-Aware Caching) |
| Dataset | Wan 2.1, CogVideoX, LTX-Video |

> [!tip] 效果简介
> - Wan 2.1 上，LPIPS (↓) 0.0540 (SenCache-fast) vs 0.0603 (MagCache-fast) (-0.0063)。
> - CogVideoX 上，LPIPS (↓) 0.1901 (SenCache) vs 0.1952 (MagCache) (-0.0051)。
> - LTX-Video 上，LPIPS (↓) 0.1625 (SenCache) vs 0.1795 (MagCache) (-0.0170)。

## 概要

扩散模型在视频生成等任务中展现出卓越的视觉质量，但其推理过程需要执行大量序列化去噪步骤，导致高昂的计算开销。为缓解这一问题，现有训练无关的缓存方法（如 **TeaCache**（Liu et al., CVPR 2025）和 **MagCache**（Ma et al., arXiv 2025））通过重用历史去噪输出来跳过部分网络评估，从而降低推理成本。然而，这些方法依赖启发式准则（如残差幅度比、时间嵌入差异）并采用静态固定的缓存调度，无法适应不同样本的难度差异和去噪网络在不同时间步的敏感性变化，容易导致过度缓存（损害生成质量）或欠缓存（浪费加速机会）。

**SenCache** 针对上述瓶颈，提出了一种基于灵敏度感知的自适应缓存方法。其核心思路是：将去噪网络输出对输入扰动的一阶灵敏度——即网络对噪声潜在表示 $\mathbf{x}_t$ 和时间步 $t$ 的 Jacobian 范数——作为缓存决策的理论依据。具体而言，SenCache 在每个去噪步计算组合灵敏度评分 $S_t = \|J_x\| \|\Delta \mathbf{x}_t\| + \|J_t\| |\Delta t|$，并与容忍度 $\varepsilon$ 比较：当 $S_t \leq \varepsilon$ 时重用缓存输出，否则刷新缓存。这一准则显式建模了潜在向量漂移和时间步间隔对输出的联合影响，为缓存决策提供了有理论保证的自适应机制，并统一解释了先前启发式方法的有效性及其失败原因。

在 Wan 2.1、CogVideoX 和 LTX-Video 三个视频生成模型上的实验表明，在相近的计算预算下，SenCache 相比现有缓存方法能更好地保持生成样本的视觉质量。例如，在 Wan 2.1 上，SenCache-fast 的 LPIPS 降至 0.0540（MagCache-fast 为 0.0603）；在 LTX-Video 上，LPIPS 从 0.1795 降至 0.1625。同时，端到端墙钟延迟从原始模型的 182.3 秒降至 107.3 秒（41.1% 加速），总计算量减少 57.8%。消融实验进一步验证了灵敏度估计的高效性：仅需 8 个多样化视频即可获得接近大批次（4096）的敏感性曲线，表明该方法无需大规模校准即可部署。

在方法谱系上，SenCache 属于训练无关的全前向缓存方法，与 TeaCache、MagCache 共享“跳过部分去噪网络评估”的加速范式，但其关键区分点在于用基于 Jacobian 范数的理论准则替换了启发式触发器，实现了模态无关、架构无关、采样器无关的动态缓存决策。该方法与全局时间步优化方法（如直接搜索最优采样轨迹）形成互补：SenCache 的局部灵敏度可视为跳过一步的边际代价代理，未来可结合全局调度提供动态 $\varepsilon(t)$ 以进一步优化速度-质量权衡。

扩散模型已成为视觉内容生成的核心架构，但其推理过程需要执行数十甚至上百次序列化去噪步骤，每次步骤都需完整调用参数量庞大的去噪网络。这一串行计算范式导致推理延迟极高，严重制约了扩散模型在实时交互、大规模内容生产等场景中的实际部署。

为缓解上述瓶颈，研究者提出了多种训练无关的缓存加速策略。其核心思路是：在采样轨迹中，相邻时间步的去噪网络输出往往高度相似，因此可以跳过部分网络前向计算，直接复用先前缓存的结果。代表性工作包括 **TeaCache**（Liu et al., CVPR 2025）和 **MagCache**（Ma et al., arXiv 2025）。TeaCache 基于时间嵌入差异与残差幅度构建启发式缓存判据，MagCache 则以残差幅度比率作为复用决策依据。

然而，这些方法存在两个根本性缺陷。其一，**判据依赖启发式设计**，缺乏对缓存误差的理论刻画——它们无法定量回答“复用缓存会在输出中引入多大偏差”这一核心问题。其二，**缓存调度策略是静态且全局固定的**，对所有样本采用相同的重用步长，完全忽视了不同样本在去噪轨迹上的难度差异以及模型在不同区域敏感性的显著变化。这种“一刀切”策略在简单样本上可能过度缓存导致质量退化，在困难样本上则可能缓存不足而浪费加速机会。

SenCache 的提出正是为了填补上述理论与实用层面的缺口。该方法将缓存决策建立在**去噪网络对其输入扰动的局部敏感性**这一具有理论依据的度量之上，从而将缓存问题从经验试错提升为有理论保证的自适应决策。其核心动机可以概括为：**用网络输出的 Jacobian 范数作为局部 Lipschitz 常数，显式建模潜在向量漂移和时间步间隔对输出的影响，建立一个统一、可解释且无需训练的缓存准则**。这一视角不仅为缓存决策提供了严格的上界保证，还能从理论上解释先前启发式方法为何有时有效、何时会失效。

## 核心方法与创新机理

SenCache 的核心创新在于将扩散模型去噪器的**局部敏感性**显式建模为缓存决策的理论准则，取代了以往方法中依赖的启发式触发器。这一转变从根本上改变了缓存策略的设计范式：从“猜测哪些步骤可以跳过”变为“基于一阶近似估计输出变化，仅在变化足够小时重用缓存”。

### 从启发式到理论驱动的缓存准则

已有的训练无关缓存方法，如 **TeaCache**（Liu et al., CVPR 2025）和 **MagCache**（Ma et al., arXiv 2025），均采用全前向（full-forward）缓存策略，但其缓存决策依赖手工设计的启发式指标——前者基于时间嵌入差异与残差建模，后者基于残差幅度比率。这些启发式准则存在两个根本缺陷：（1）它们仅捕捉了影响去噪器输出的单一因素，无法全面反映输入扰动对输出的影响；（2）它们采用静态、全局固定的缓存调度，无法适应不同样本的难度差异和模型在不同去噪阶段的敏感性变化。

SenCache 的关键洞察在于：**网络输出对其输入的 Jacobian 范数可以作为局部 Lipschitz 常数**，为缓存误差提供可量化的上界。具体而言，对于去噪网络 $f_{\theta}(\mathbf{x}_t, t, c)$，其输出变化可由一阶泰勒展开近似：

$$f_{\theta}(\mathbf{x}_{t+\Delta t}, t+\Delta t, c) - f_{\theta}(\mathbf{x}_t, t, c) \approx J_x \Delta \mathbf{x}_t + J_t \Delta t$$

其中 $J_x = \frac{\partial f_{\theta}}{\partial \mathbf{x}_t}$ 和 $J_t = \frac{\partial f_{\theta}}{\partial t}$ 分别为网络对噪声潜在向量和时间步的 Jacobian。由此可导出输出变化的上界：

$$\| f_{\theta}(\mathbf{x}_{t+\Delta t}, t+\Delta t, c) - f_{\theta}(\mathbf{x}_t, t, c) \| \leq \|J_x\| \|\Delta \mathbf{x}_t\| + \|J_t\| |\Delta t| + O(\|\Delta \mathbf{x}_t\|^2 + |\Delta t|^2)$$

基于此上界，SenCache 定义**灵敏度评分** $S_t = \|J_x\| \|\Delta \mathbf{x}_t\| + \|J_t\| |\Delta t|$，并设置容忍度 $\varepsilon$ 作为缓存决策阈值：当 $S_t \leq \varepsilon$ 时重用缓存输出，否则刷新缓存。这一准则同时显式建模了潜在向量漂移和时间步间隔对输出的影响，统一解释了先前启发式方法为何有效（当它们隐式捕捉了部分敏感性因素时）以及何时会失效（当它们忽略的因素成为主导时）。

### 三个关键 changed slots

相较于基线方法，SenCache 在以下三个维度上实现了根本性改变：

| 维度 | 基线方法 | SenCache |
|------|----------|----------|
| **缓存决策准则** | 启发式（残差大小、时间嵌入差异） | 基于一阶敏感性近似 $S_t$ 与容忍度 $\varepsilon$ 比较 |
| **缓存调度策略** | 静态/全局固定重用步长 | 动态/每个样本自适应，根据局部敏感性实时决定 |
| **敏感性建模** | 仅考虑单一因素 | 同时显式建模对噪声潜在 $\mathbf{x}_t$ 和时间步 $t$ 的 Jacobian 范数 |

其中，**动态自适应调度**是 SenCache 区别于先前方法最显著的特征。TeaCache 和 MagCache 对所有样本采用相同的缓存步长配置，而 SenCache 在推理过程中根据每个样本当前的局部敏感性实时决定是否跳过当前去噪步。这使得 SenCache 能够在“容易”的样本或去噪阶段更积极地缓存以加速推理，而在“困难”的区域保持更密集的网络评估以维持生成质量。

### 敏感性预计算与实用设计

为避免在线计算 Jacobian 的高昂开销，SenCache 采用**离线预计算**策略：使用少量样本（仅 8 个多样化视频）通过有限差分估计 $\|J_x\|$ 和 $\|J_t\|$ 沿时间步的曲线，推理时直接查表获取。消融实验表明，8 个视频与 4096 个视频得到的敏感性曲线已高度吻合，验证了该估计策略的数据高效性。此外，SenCache 引入最大连续缓存步数 $n$ 作为安全机制，防止长期缓存导致的漂移累积。

### 方法谱系与知识库定位

SenCache 属于**训练无关的扩散模型推理加速**方法，与 TeaCache、MagCache 等同属全前向缓存（full-forward caching）范式。其理论贡献在于首次将网络敏感性分析引入缓存决策，建立了从 Jacobian 范数到缓存误差上界的严格推导。这一框架具有模态无关、架构无关和采样器无关的特性——因为它仅依赖局部模型敏感性和步间实际输入变化，而非手工设计的触发器。该工作与以下方向形成互补：（1）基于模型压缩的加速方法（如剪枝、量化）；（2）基于高效采样器的方法（如 DDIM、DPM-Solver）；（3）基于知识蒸馏的方法。SenCache 可与这些方法正交叠加，进一步降低推理成本。

**局限性提示**：当前固定 $\varepsilon$ 的策略无法像全局调度方法那样动态分配误差预算；一阶近似在高度非线性区域可能低估输出变化；敏感性预计算需针对每个模型单独进行（但仅需极少样本）。这些限制为后续研究指明了方向。

SenCache 是一种训练无关、架构无关、采样器无关的全前向缓存方法，其核心思想是将扩散模型去噪网络对输入扰动的局部敏感性作为缓存决策的理论依据。整个推理加速框架由三个功能模块串联构成：**敏感性预计算模块**、**自适应缓存循环**与**缓存生命周期控制**。

### 整体流程

推理开始前，SenCache 首先通过**敏感性预计算模块**，使用极少量校准样本（仅需 8 个多样化视频，如 MixKit 数据集）对目标去噪网络进行一次性离线分析。该模块通过有限差分法分别估计网络输出对噪声潜在表示 $\mathbf{x}_t$ 的 Jacobian 范数 $\|J_x\|$ 和对时间步 $t$ 的 Jacobian 范数 $\|J_t\|$，从而获得模型在不同时间步上的敏感性剖面。这一剖面作为先验知识被存储下来，供推理阶段实时查询，无需在每次生成时重复计算。

在推理阶段，**自适应缓存循环**在每个去噪步执行如下决策流程（对应 Figure 2 与 Algorithm 1）：首先计算当前步相对于上一次缓存刷新步的累积输入变化量——即潜在向量的漂移 $\|\Delta \mathbf{x}_t\|$ 和时间步间隔 $|\Delta t|$；随后结合预计算的敏感性范数，计算灵敏度评分 $S_t = \|J_x\| \|\Delta \mathbf{x}_t\| + \|J_t\| |\Delta t|$。该评分基于一阶泰勒展开，显式界定了去噪器输出在当前输入扰动下预期变化的上界。若 $S_t \leq \varepsilon$（$\varepsilon$ 为预设的容忍度超参数），则判定网络输出变化足够小，直接重用先前缓存的去噪器输出，跳过当前步的昂贵网络前向计算；否则，执行完整的网络前向传播并刷新缓存状态。

![[assets/figures/papers/paper_list_l2054_https_arxiv_org_abs_2602_24208/figures/002_Figure_2.jpg]]
*Figure 2: SenCache uses sensitivity as a caching criterion. At each denoising step, if the changes in the noisy latent*

为防止长期漂移导致缓存误差累积，框架引入了**缓存生命周期控制**机制：通过超参数 $n$ 限制最大连续缓存步数。当连续重用次数达到 $n$ 时，缓存被强制刷新，确保潜在轨迹不会因过度重用而偏离真实去噪路径。

### 模块间的输入输出关系

三个模块形成清晰的单向数据依赖链。敏感性预计算模块的输出（$\|J_x\|$ 和 $\|J_t\|$ 曲线）是自适应缓存循环的静态输入，仅在模型切换时需要重新计算。自适应缓存循环接收当前采样状态（$\mathbf{x}_t$, $t$, 条件 $c$）和缓存状态作为动态输入，输出缓存命中/刷新的二元决策，并据此决定是否调用去噪网络 $f_\theta$。缓存生命周期控制则作为循环内部的约束条件，通过对连续命中计数的监控来触发强制刷新信号。整个框架无需修改预训练模型权重，也不依赖特定的采样器实现，因此可以即插即用地嵌入各类扩散模型推理管线中。

### 问题形式化：缓存误差的敏感性分解

扩散模型推理的核心计算瓶颈在于每个去噪步都需要完整评估去噪网络 $f_{\theta}(\mathbf{x}_t, t, c)$。缓存方法的基本思路是：当连续步骤间网络输出变化足够小时，重用先前的计算结果。问题的关键转化为：**如何准确预测输出变化，从而决定何时可以安全地缓存**。

SenCache 的核心洞察是将缓存误差形式化为网络对其输入扰动的一阶敏感性分析。考虑从时间步 $t$ 到 $t+\Delta t$ 的累积变化，网络输出的差异可以表示为：

$$f_{\theta}(\mathbf{x}_{t+\Delta t}, t+\Delta t, c) - f_{\theta}(\mathbf{x}_t, t, c) \approx J_x \Delta \mathbf{x}_t + J_t \Delta t$$

其中 $J_x = \frac{\partial f_{\theta}(\mathbf{x}_t, t, c)}{\partial \mathbf{x}_t}$ 和 $J_t = \frac{\partial f_{\theta}(\mathbf{x}_t, t, c)}{\partial t}$ 分别是去噪网络输出对噪声潜在向量和时间步的 Jacobian。$\Delta \mathbf{x}_t = \mathbf{x}_{t+\Delta t} - \mathbf{x}_t$ 是潜在向量的累积漂移，$\Delta t$ 是时间步间隔。

利用 Jacobian 范数作为局部 Lipschitz 常数，可推导出输出变化的上界：

$$\| f_{\theta}(\mathbf{x}_{t+\Delta t}, t+\Delta t, c) - f_{\theta}(\mathbf{x}_t, t, c) \| \leq \|J_x\| \|\Delta \mathbf{x}_t\| + \|J_t\| |\Delta t| + O(\|\Delta \mathbf{x}_t\|^2 + |\Delta t|^2)$$

这一分解揭示了先前启发式方法的本质与局限：**有效的缓存准则必须同时考虑潜在漂移和时间步间隔两个因素**。仅依赖时间嵌入差异（如 TeaCache）或残差幅度（如 MagCache）的单一代理变量，在某一项占主导时可能失效。

### 核心模块一：灵敏度评分与自适应缓存决策

基于上述理论框架，SenCache 定义了一个组合灵敏度评分 $S_t$：

$$S_t = \|J_x\| \|\Delta \mathbf{x}_t\| + \|J_t\| |\Delta t|$$

该评分直接量化了当前步骤累积输入变化在局部敏感度加权下对输出的预期影响。缓存决策规则为：

- **若 $S_t \leq \varepsilon$**：预测输出变化在容忍度内，重用缓存的 $f_{\theta}(\mathbf{x}_t, t, c)$
- **若 $S_t > \varepsilon$**：刷新缓存，在当前位置重新评估网络

其中 $\varepsilon$ 是用户指定的误差容忍度超参数，控制速度-质量权衡。该准则具有模态无关、架构无关和采样器无关的特性，因为它仅依赖局部模型敏感性和实际输入变化，而非手工设计的触发条件。

为防止长期漂移累积，SenCache 引入最大连续缓存步数 $n$：连续重用 $n$ 次后强制刷新缓存（见 **Table 2** 消融分析，$n$ 超过 4 后 NFE 饱和且视觉质量下降）。

### 核心模块二：敏感性预计算与高效估计

直接在每个推理步计算 Jacobian 范数代价过高。SenCache 采用两阶段策略：

**离线预计算阶段**：使用少量校准样本（8 个多样化视频，来自 MixKit 数据集）通过有限差分估计 Jacobian 范数随 $t$ 变化的曲线：

$$\|J_x\| \approx \frac{\| f_{\theta}(\mathbf{x}_t + \Delta \mathbf{x}, t, c) - f_{\theta}(\mathbf{x}_t, t, c) \|_2}{\|\Delta \mathbf{x}\|_2}$$

$$\|J_t\| \approx \frac{\| f_{\theta}(\mathbf{x}_t, t+\Delta t, c) - f_{\theta}(\mathbf{x}_t, t, c) \|_2}{|\Delta t|}$$

**Figure 4** 的消融实验表明，仅需 8 个多样化视频即可获得与 4096 个视频接近的敏感性估计，大幅降低了校准成本。

**在线推理阶段**：在每一步查询预计算的 $\|J_x\|$ 和 $\|J_t\|$ 曲线，结合累积的 $\Delta \mathbf{x}_t$ 和 $\Delta t$ 计算 $S_t$，与 $\varepsilon$ 比较做出缓存决策（见 **Algorithm 1** 和 **Figure 2** 流程概览）。

### 敏感性分析的关键发现

**Figure 3(a)** 揭示了两个关键现象：(1) $\|J_x\|$ 和 $\|J_t\|$ 在广泛的 $t$ 范围内均不可忽略，且随 $t$ 显著变化；(2) 两者的变化模式不同，说明单一代理变量无法全面捕捉网络敏感性。**Figure 3(b)** 进一步验证了敏感性引导的步骤选择远优于均匀选择：在相同 NFE 下，前者几乎无视觉退化，后者则出现显著质量下降。这为 SenCache 的动态、逐样本自适应调度提供了经验支撑。

### 方法定位与谱系

SenCache 属于**训练无关的全前向缓存方法**，与 TeaCache（Liu et al., CVPR 2025）和 MagCache（Ma et al., arXiv 2025）处于同一技术路线。核心差异在于缓存准则的理论基础：

| 方法 | 缓存准则 | 理论保证 | 调度策略 |
|------|---------|---------|---------|
| TeaCache | 时间嵌入差异 + 残差建模 | 启发式 | 静态 |
| MagCache | 残差幅度比率 | 启发式 | 静态 |
| **SenCache** | **一阶敏感性 $S_t = \|J_x\| \|\Delta \mathbf{x}_t\| + \|J_t\| \|\Delta t\|$** | **有界误差（一阶近似）** | **动态/逐样本自适应** |

SenCache 的统一敏感性框架解释了 TeaCache 和 MagCache 有效性的条件：当 $\|J_x\| \|\Delta \mathbf{x}_t\|$ 主导时，残差幅度是合理代理；当 $\|J_t\| |\Delta t|$ 主导时，时间嵌入差异是合理代理。但两者均无法在两项贡献可比时做出准确决策，而 SenCache 通过显式建模两项避免了这一失效模式。

![[assets/figures/papers/paper_list_l2054_https_arxiv_org_abs_2602_24208/figures/003_Figure.jpg]]
*Figure: (b) Comparison of 25-step sampling between Sensitivity-guided selection vs. Uniform selection*

## 实验与关键发现

### 主实验结果

SenCache 在三个主流视频生成模型上与两类代表性缓存方法进行了对比：**TeaCache**（Liu et al., CVPR 2025，基于时间嵌入差异的启发式缓存）和 **MagCache**（Ma et al., arXiv 2025，基于残差幅度比率的启发式缓存），以无缓存的 Vanilla 推理为参考基线。所有方法使用相同的预训练模型和采样器配置，无需额外训练或模型修改，比较在相似的计算预算下进行。效率指标采用 NFE（Number of Function Evaluations）和缓存重用率，视觉质量指标采用 LPIPS、PSNR 和 SSIM。

Table 1 汇总了三个模型上的定量结果。在 Wan 2.1 上，SenCache-fast 配置以 NFE 匹配 MagCache-fast 为前提，LPIPS 达到 0.0540，相比 MagCache-fast 的 0.0603 降低了 0.0063，视觉保真度优势明显。在 CogVideoX 上，SenCache 的 LPIPS 为 0.1901，优于 MagCache 的 0.1952（Δ = -0.0051）；在 LTX-Video 上，SenCache 的 LPIPS 为 0.1625，显著低于 MagCache 的 0.1795（Δ = -0.0170）。在所有模型上，SenCache 在 PSNR 和 SSIM 指标上也保持了一致优势。从实际推理延迟看，Wan 2.1 上 SenCache 将端到端推理时间从 Vanilla 的 182.3 秒降至 107.3 秒，加速比达到 41.1%。

![[assets/figures/papers/paper_list_l2054_https_arxiv_org_abs_2602_24208/figures/006_Table_1.jpg]]
*Table 1: We conduct a quantitative evaluation of inference efficiency and visual quality in video generation models. Efficiency was measured by the NFE and the cache ratio, while visual quality was assessed using LPIPS, PSNR, and SSIM. Our results show that with the same amount of compute as previous methods, SenCache achieves superior visual quality with improved LPIPS, PSNR, and SSIM scores*

这些结果验证了核心主张：在相似计算预算下，基于敏感性的自适应缓存策略相比启发式方法能更好地保留生成样本的视觉质量。

### 消融实验

**最大连续缓存步数 n 的影响。** Table 2 展示了在 Wan 2.1 模型上固定 ε = 0.05 时，超参数 n 对效率和质量的调控作用。增大 n 允许更长的连续缓存序列，从而降低 NFE、提高推理效率。但当 n 超过 4 后，NFE 趋于饱和而视觉质量持续下降，说明过长的连续缓存会导致潜在向量漂移累积，超出敏感性准则的容忍范围。该实验支持将 n 作为控制缓存激进程度的安全阀。

**误差容忍度 ε 的影响。** Table 3 展示了在 Wan 2.1 模型上固定 n = 3 时，ε 的扫描结果。增大 ε 放宽了缓存重用的条件，NFE 随之降低，但 LPIPS 等视觉质量指标同步恶化，呈现出清晰的准确度-效率权衡曲线。这一结果验证了 ε 作为核心控制旋钮的有效性：用户可根据实际部署需求在速度和质量之间灵活调节。

**校准集规模的影响。** Figure 4 考察了敏感性预计算阶段校准视频数量的影响。实验对比了使用 8 个多样化视频（来自 MixKit 数据集）与使用 4096 个视频估计的敏感性曲线，发现两者高度吻合。这表明 SenCache 的敏感性估计对校准数据规模不敏感，仅需极少样本即可获得稳定的 Jacobian 范数曲线，大幅降低了预计算开销。

### 诊断分析

Figure 5 展示了不同模型在连续时间步上去噪器输出的平均绝对误差（MAE）。该分析揭示了不同模型在去噪轨迹上的输出变化幅度存在显著差异，为理解为何统一静态缓存策略在不同模型间表现不一致提供了直观解释。SenCache 通过显式建模局部敏感性，能够自适应地应对这种模型间差异，而启发式方法因依赖固定阈值或单一代理变量，在输出变化剧烈的区域容易产生显著的缓存误差。

![[assets/figures/papers/paper_list_l2054_https_arxiv_org_abs_2602_24208/figures/009_Figure_5.jpg]]
*Figure 5: MAE between the denoiser outputs at two consecutive timesteps*

### 失败模式与局限性

尽管 SenCache 在多个模型上展现了稳定的性能优势，其设计仍存在若干边界条件。首先，固定 ε 策略在整个去噪过程中分配相同的误差容忍度，但不同时间步对输出质量的影响并非均等：在去噪早期，输出变化剧烈，一阶近似可能低估真实误差，导致缓存引入的漂移超出预期；而在去噪后期，输出趋于平滑，固定的 ε 可能过于保守，错失进一步加速的机会。其次，在高度非线性的网络响应区域，一阶 Taylor 展开的截断误差不可忽略，敏感性评分 S_t 可能低估实际输出变化，导致缓存决策失误。这些失效模式提示，未来的改进方向可考虑引入时间步自适应的动态容忍度 ε(t)，或采用高阶敏感性估计器以提升非线性区域的近似精度。

![[assets/figures/papers/paper_list_l2054_https_arxiv_org_abs_2602_24208/figures/007_Table_2.jpg]]
*Table 2: Ablation study on*

![[assets/figures/papers/paper_list_l2054_https_arxiv_org_abs_2602_24208/figures/008_Table_3.jpg]]
*Table 3: Ablation study on the error tolerance ε. Performed on Wan 2.1 [38] with*

## 定位与知识库关联

### 一、与基线方法的关系

SenCache 属于**训练无关的全前向缓存（full-forward caching）** 方法族，其核心差异在于将缓存决策从启发式准则提升为**基于网络局部敏感性的理论驱动准则**。理解这一谱系定位，需要对比两类代表性基线：

**TeaCache**（Liu et al., CVPR 2025）通过监测时间嵌入的差异和残差输出来决定是否重用缓存。其隐含假设是：当时间嵌入变化小且残差幅度低时，去噪器输出变化也小。然而，这种单一代理变量无法捕捉潜在向量漂移与时间步间隔的耦合效应——当潜在向量发生较大偏移而时间步间隔较小时，TeaCache 可能误判为“安全缓存”，导致输出误差累积。

**MagCache**（Ma et al., arXiv 2025）基于残差幅度比率进行缓存决策，同样依赖单一启发式信号。在 Wan 2.1 和 CogVideoX 等模型上，MagCache 虽能实现可观的 NFE 降低，但其静态的全局缓存调度无法适应不同样本的难度差异：对于运动剧烈、纹理复杂的视频序列，固定步长的缓存策略容易在关键去噪阶段引入不可逆的视觉退化。

SenCache 的理论框架**统一解释了上述启发式方法的有效性与失败边界**。通过将缓存误差形式化为去噪器输出对输入扰动的一阶敏感性：

$$S_t = \|J_x\| \|\Delta \mathbf{x}_t\| + \|J_t\| |\Delta t|$$

其中 $J_x = \frac{\partial f_{\theta}(\mathbf{x}_t, t, c)}{\partial \mathbf{x}_t}$ 和 $J_t = \frac{\partial f_{\theta}(\mathbf{x}_t, t, c)}{\partial t}$ 分别为网络输出对噪声潜在和时间步的 Jacobian。该公式揭示了两个关键事实：

1. **潜在敏感性与时间敏感性的贡献均不可忽略**（Figure 3a 显示两者在宽时间步范围内均有显著幅值），因此仅依赖时间嵌入差异（TeaCache）或残差幅度（MagCache）的单一代理变量本质上是不完备的。
2. **实际缓存误差取决于敏感性与输入变化量的乘积**，而非任一因素的绝对值。这意味着即使网络在某一区域高度敏感，若输入变化极小（例如采样步长密集时），缓存仍可能是安全的；反之，在低敏感区域若输入漂移过大，缓存同样会引入显著误差。

### 二、方法边界与适用条件

**适用前提：**
- **架构无关性**：SenCache 仅需访问去噪器的前向传播输出，不依赖特定的网络结构（DiT、U-Net 均可），也不要求修改模型权重或训练过程。这一特性使其可直接应用于现有预训练扩散模型。
- **模态无关性**：敏感性准则基于输入-输出的局部 Lipschitz 性质，与数据模态（图像、视频）无关。论文在 Wan 2.1、CogVideoX 和 LTX-Video 三个视频生成模型上验证了这一点。
- **采样器无关性**：无论是概率流 ODE 采样器还是随机微分方程（SDE）采样器，只要去噪步骤可序列化执行，SenCache 的缓存逻辑均适用。

**适用边界：**
- **高度非线性区域的近似误差**：一阶泰勒展开在去噪轨迹的曲率较大区域（如早期去噪步）可能低估输出变化。此时 $S_t \leq \varepsilon$ 的判定可能过于乐观，导致缓存引入的误差超出容忍度。论文通过引入最大连续缓存步数 $n$ 来限制长期漂移，但这是一种折中而非根本性解决。
- **固定容忍度 $\varepsilon$ 的局限性**：当前设计中 $\varepsilon$ 为全局常数，无法像全局调度方法（如动态规划优化整个去噪轨迹）那样在不同时间步之间动态分配误差预算。在极端效率需求下（如极低 NFE 场景），固定 $\varepsilon$ 可能导致早期步过度缓存或后期步缓存不足。
- **敏感性预计算的模型特异性**：虽然仅需 8 个多样化视频即可获得稳定的 Jacobian 范数估计（Figure 4 消融实验证实），但该过程仍需对每个目标模型单独执行。对于需要频繁切换模型的场景，这会引入额外的校准开销。

**与无缓存基线（Vanilla）的关系**：当 $\varepsilon \to 0$ 时，SenCache 退化为无缓存的全步推理，因为任何非零的输入变化都会触发缓存刷新。这保证了方法在最保守设置下的保真度——用户可通过调节 $\varepsilon$ 在“完全保真”和“最大加速”之间连续插值。

### 三、局限性与开放问题

**已识别的局限性：**

1. **一阶近似的固有误差**：在去噪轨迹的高曲率段，$O(\|\Delta \mathbf{x}_t\|^2 + |\Delta t|^2)$ 的高阶项不可忽略。当前方法缺乏对这些区域的显式检测与补偿机制，可能在复杂纹理或快速运动场景中产生伪影。

2. **静态 $\varepsilon$ 的次优性**：全局固定的容忍度无法感知不同去噪阶段的差异化需求。早期去噪步主要处理全局结构，对误差相对鲁棒；后期去噪步精调细节，对微小扰动更敏感。固定 $\varepsilon$ 无法利用这种阶段性差异进一步优化效率-质量权衡。

3. **校准集的分布偏移**：敏感性估计基于 MixKit 数据集的 8 个视频。若推理时的数据分布与校准集显著不同（例如极端光照、非自然场景），预计算的 Jacobian 范数曲线可能偏离实际敏感性，导致缓存决策失准。

**开放研究问题：**

1. **高阶或可学习敏感性估计器**：能否使用二阶导数信息或轻量级可学习模块替代一阶有限差分，以减少非线性区域的近似误差？这需要在估计精度与计算开销之间取得平衡。

2. **动态 $\varepsilon(t)$ 调度**：能否设计跨时间步的自适应容忍度分配策略，将有限的误差预算集中在视觉敏感的去噪阶段？这类似于率失真优化中比特分配问题的变体，可借助动态规划或强化学习方法求解。

3. **跨模态扩展**：敏感性感知缓存的核心思想——利用网络局部 Lipschitz 常数指导计算重用——是否可推广至文本到语音、音频生成或多模态扩散系统？不同模态的去噪动力学可能存在本质差异，需要验证 Jacobian 范数是否仍为有效的缓存预测器。

4. **全局轨迹优化与局部敏感性的融合**：当前方法仅依赖局部敏感性进行贪婪决策。若能结合全局轨迹优化（如通过 ODE 求解器的自适应步长控制），为每个时间步提供上下文感知的容忍度，有望进一步逼近理论最优的效率-质量前沿。

5. **与模型压缩技术的协同**：SenCache 与量化、剪枝、蒸馏等正交加速技术结合时，敏感性准则是否需要重新校准？压缩后的网络其局部 Lipschitz 常数可能发生显著变化，这为联合优化提供了研究空间。

## 原文 PDF

![[paperPDFs/CVPR_2026/SenCache_Accelerating_Diffusion_Model_Inference_via_Sensitivity_Aware_Caching.pdf]]
