---
title: "Diffusion Sampling Path Tells More: An Efficient Plug-and-Play Strategy for Sample Filtering"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Diffusion_Sampling_Path_Tells_More_An_Efficient_Plug_and_Play_Strategy_for_Sample_Filtering.pdf
project_link: null
code_link: "https://github.com/NVlabs/edm2"
aliases:
- CR
- DSPTMEPPSSF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 分类器自由引导（CFG）过程中条件得分与无条件得分之间的累积差异（ASD），该差异与样本位于数据流形高密度区域的概率强相关，可通过控制早期步骤的阈值 γ 和超参数 τ 来筛选样本。
primary_logic: 在 CFG 去噪轨迹中，条件与无条件得分的累积差异（ASD）与最终样本质量及数据分布密度间存在强正相关，因此可将 ASD 作为内在、无奖励的信号用于早期拒绝低质量样本，实现高效过滤。
claims:
- 在二维玩具分布上，高 ASD 样本集中于高密度主干区域，低 ASD 样本出现在低密度分支，且 ASD 与对数密度呈线性正相关。
- 在 ImageNet 上，使用 AvgkNN 和 LOF 密度估计器确认低 ASD 样本更倾向于占据低似然区域，验证了 ASD-密度相关性。
- 基于 ASD 的过滤策略（Top 10% 或 τ=10）在 ImageNet 上持续提升 PickScore（+0.23）和 HPSv2（+0.44）等人类偏好指标。
- 在 GenEval 和 DPG-Bench 基准上，CFG-Rejection 对 SDv1.5 的整体得分提升最高达 4.6 个百分点，且 τ=10 时即可接近性能上限。
---

# Diffusion Sampling Path Tells More: An Efficient Plug-and-Play Strategy for Sample Filtering

> [!tip] 核心洞察
> 在 CFG 去噪轨迹中，条件与无条件得分的累积差异（ASD）与最终样本质量及数据分布密度间存在强正相关，因此可将 ASD 作为内在、无奖励的信号用于早期拒绝低质量样本，实现高效过滤。

| 字段 | 内容 |
|------|------|
| 中文题名 | 扩散采样路径揭示更多：一种高效的即插即用样本过滤策略 |
| 英文题名 | Diffusion Sampling Path Tells More: An Efficient Plug-and-Play Strategy for Sample Filtering |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.23343) · [Code](https://github.com/NVlabs/edm2) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CFG-Rejection |
| Dataset | ImageNet, GenEval, DPG-Bench |

> [!tip] 效果简介
> - ImageNet (EDM2-S, 50 classes) 上，PickScore 20.61 (Top 10% by E_T(c)) vs 20.38 (Full set) (+0.23)；HPSv2 26.57 (Top 10% by E_T(c)) vs 26.13 (Full set) (+0.44)。
> - GenEval (SDv1.5, guidance=5) 上，Overall↑ 0.4594 (τ=20) vs 0.4152 (random) (+0.0442)。
> - GenEval (SDv1.5, guidance=9) 上，Overall↑ 0.4785 (τ=20) vs 0.4322 (random) (+0.0463)。

## 概要

扩散模型在文本到图像生成中取得了显著进展，但其采样过程本质上是随机的，导致生成质量存在较大波动。现有推理时对齐方法，如 **Best-of-N** 采样、**DNO**（Direct Noise Optimization）和 **LGD**（Loss-Guided Diffusion），通常依赖外部奖励模型对完整去噪后的样本进行筛选或引导，这不仅引入了额外的模型开销，也无法在早期阶段识别并终止低质量轨迹。

本文的核心发现是：在分类器自由引导（CFG）的去噪轨迹中，条件得分与无条件得分之间的累积差异（Accumulated Score Differences, ASD）与样本位于数据流形高密度区域的概率存在强正相关——高 ASD 样本倾向于集中在高密度、高语义对齐的区域，而低 ASD 样本则更可能出现在低密度、语义模糊的区域。这一关联在二维玩具分布和 ImageNet 真实数据上均得到了密度估计的验证。

基于此洞察，论文提出 **CFG-Rejection**，一种即插即用的高效样本过滤策略。该方法无需外部奖励模型或额外训练，仅利用 CFG 过程中固有的得分差异信号，在去噪早期（步骤 $T-\tau$ 之后）计算部分累积得分差 $\mathcal{E}_{\tau:T}(c)$，并通过阈值 $\gamma$ 提前终止低质量轨迹，从而在有限推理预算下显著提升样本质量。

实验结果表明，CFG-Rejection 在 ImageNet、GenEval 和 DPG-Bench 等多个基准上持续提升人类偏好指标：在 ImageNet 上，Top 10% 筛选使 PickScore 提升 +0.23、HPSv2 提升 +0.44；在 GenEval 上，SDv1.5 的整体得分最高提升 4.6 个百分点，且 $\tau=10$ 时即可接近性能上限。在受限推理预算下，CFG-Rejection 通过早期过滤在低时间区内比 Best-of-N 更快取得高分，展现出显著的计算效率优势。该方法同时适用于 EDM2、SDv1.5、SDXL 和 FLUX 等多种扩散模型架构。

需要指出的是，CFG-Rejection 依赖于分类器自由引导机制，不适用于无条件生成任务；当引导强度过高导致样本多样性极低时，ASD 的区分度会下降；此外，ASD 与样本质量的关联目前基于经验观察，缺乏严格的理论保证，且超参数 $\tau$ 和 $\gamma$ 需根据具体模型和任务进行调优。

扩散模型已成为视觉内容生成的核心技术，其采样过程本质上是随机微分方程（SDE）或常微分方程（ODE）的数值求解。给定数据分布 $p_{\mathrm{data}}(\mathbf{x})$，模型通过逐步向数据注入高斯噪声将其转化为可处理的先验分布，再学习逆转这一扩散过程。在推理阶段，采样从纯噪声出发，沿反向轨迹逐步去噪，最终产生符合目标分布的样本。这一随机性带来了多样性，但也意味着并非所有采样轨迹都能产生高质量样本——部分轨迹会收敛到低似然区域，导致伪影、语义错位或文本对齐失败。

当前提升扩散模型推理质量的主流方法可分为两类：**基于外部奖励的过滤方法**（如 Best-of-N 采样）要求生成完整的候选样本池，再借助预训练的奖励模型（如 PickScore、HPSv2）进行后验选择；**推理时对齐方法**（如 Loss-Guided Diffusion、Direct Noise Optimization）则在采样过程中引入额外的梯度信号来引导生成。这两类方法的共同瓶颈在于：它们都依赖**外部信号源**（奖励模型或损失函数），且需要在**完整去噪过程**完成后或贯穿全过程才能评估样本质量。这导致两个关键缺陷：一是外部奖励模型的训练和推理带来额外开销，且其偏好可能与实际任务存在偏差；二是无法在去噪早期识别并终止低质量轨迹，造成计算资源的浪费。

一个被忽视的机遇在于：分类器自由引导（Classifier-Free Guidance, CFG）作为扩散模型的标准推理技术，其内部已经蕴含了丰富的质量信号。CFG 通过混合条件得分 $S_\theta(\mathbf{x}_t; \sigma_t, \mathbf{c})$ 和无条件得分 $S_\theta(\mathbf{x}_t; \sigma_t, \emptyset)$ 来增强条件对齐，但这一混合过程在每一步产生的**得分差异**本身是否携带关于最终样本质量的信息，此前未被系统探索。

本文的核心动机正是利用这一内在信号，构建一个**无需外部奖励、无需完整去噪**的即插即用样本过滤策略。其关键洞察是：在 CFG 去噪轨迹中，条件得分与无条件得分之间的累积差异（Accumulated Score Differences, ASD）与样本位于数据流形高密度区域的概率存在强正相关——高 ASD 样本倾向于占据高似然、语义清晰的区域，而低 ASD 样本则更可能出现在低密度、语义模糊的区域。这一相关性使得 ASD 可以作为一种**内在的、无奖励的质量评估指标**，在去噪早期即可识别并提前终止低质量采样轨迹，从而在不牺牲生成质量的前提下显著降低计算开销。

## 核心方法与创新机理

CFG-Rejection 的核心创新在于**将扩散模型采样路径中的内在信号——分类器自由引导（CFG）过程中的累积得分差异（ASD）——转化为无需外部奖励模型的样本质量评估指标**，并利用该信号在去噪早期阶段实现低质量轨迹的提前终止，从而在保持生成质量的同时显著降低计算开销。

### 创新点一：从外部奖励到内在信号的范式转换

现有推理时对齐方法普遍依赖外部奖励模型对完整去噪后的样本进行质量评估与筛选。**Best-of-N sampling** 需要生成 N 个完整样本后由奖励模型选择最优者；**Direct Noise Optimization (DNO)** 和 **Loss-Guided Diffusion (LGD)** 等方法则利用奖励信号直接引导去噪过程。这些方法的共同瓶颈在于：（1）必须完成全部去噪步骤才能获得评估结果；（2）依赖外部奖励模型，引入额外的计算成本和模型依赖。

CFG-Rejection 的核心突破在于发现并利用了**分类器自由引导机制中已存在的内在信号**——条件得分与无条件得分之间的累积差异（ASD）。该方法无需任何外部奖励模型或模型重训练，实现了完全自包含、零额外成本的样本质量评估。这一范式转换的关键因果机制在于：CFG 中条件与无条件得分的差异本质上反映了条件信息对生成轨迹的影响强度，而该强度与样本位于数据流形高密度区域的概率存在强正相关。

### 创新点二：基于部分 ASD 的早期拒绝式过滤

传统方法必须在完整去噪后进行筛选，而 CFG-Rejection 通过监控去噪早期步骤的部分累积得分差 $\mathcal{E}_{\tau:T}(c)$，能够在轨迹完成前预判样本质量并提前终止低质量生成。具体而言，该方法在去噪过程的前 $\tau$ 步后计算：

$$\mathcal{E}_{\tau:T}(c) = \sum_{t=T-\tau}^{T} \mathcal{G}_t(c)^2$$

其中 $\mathcal{G}_t(c) = \| S_{\theta}(\mathbf{x}_t; \sigma_t, \mathbf{c}) - S_{\theta}(\mathbf{x}_t; \sigma_t, \emptyset) \|_2$ 为第 $t$ 步的条件与无条件得分预测的 L2 距离。当 $\mathcal{E}_{\tau:T}(c)$ 低于预设阈值 $\gamma$ 时，该生成轨迹被判定为低质量并立即终止，从而节省剩余的推理计算。

这一机制的可行性建立在 ASD 与样本质量之间稳健的经验关联之上。在二维玩具分布实验中（Figure 3），高 ASD 样本集中于数据分布的高密度主干区域，低 ASD 样本则出现在稀疏分支区域，且 ASD 与对数密度呈线性正相关。在 ImageNet 上，使用 AvgkNN 和 LOF 密度估计器进一步验证了这一相关性：随着 ASD 从最高等级降至最低等级，样本系统性地从高密度区域向低密度区域迁移（Figure 4）。

### 创新点三：即插即用的部署特性

CFG-Rejection 作为一个即插即用策略，不需要修改模型架构、训练流程或采样算法本身，仅需在现有扩散模型的去噪循环中插入得分差记录与阈值判断逻辑。该方法已在 EDM2、SDv1.5、SDXL 和 FLUX 等多个扩散模型上验证了其通用性，覆盖了 ImageNet 类条件生成、GenEval 和 DPG-Bench 文本到图像生成、以及视觉文本渲染等多种任务场景。

### 与基线方法的关键差异总结

| 维度 | Best-of-N / DNO / LGD | CFG-Rejection |
|------|----------------------|---------------|
| **质量评估信号** | 外部奖励模型（如 PickScore） | 内在信号：CFG 累积得分差异（ASD） |
| **筛选时机** | 完整去噪后进行 | 去噪早期（步骤 $T-\tau$ 后）提前终止 |
| **额外计算成本** | 需运行外部奖励模型 | 零额外模型成本 |
| **模型依赖** | 依赖奖励模型的可用性与质量 | 完全自包含 |

CFG-Rejection 是一种即插即用的推理时样本过滤策略，其核心设计目标是在不引入外部奖励模型、不进行模型重训练的前提下，利用扩散采样过程本身蕴含的内在信号，在去噪早期识别并终止低质量样本的生成轨迹。

### 框架总览

图 1 对比了传统 Best-of-N 采样与 CFG-Rejection 的工作流差异。Best-of-N 方法需要完成全部去噪步骤，生成 N 个完整样本后，再借助外部奖励模型（如 PickScore）进行质量评估和择优；而 CFG-Rejection 在去噪过程的早期阶段即可做出过滤决策，提前终止低质量轨迹，仅保留有潜力的样本继续完成剩余去噪步骤。这一设计使得方法天然具备计算效率优势——在受限推理预算下，CFG-Rejection 能以更少的计算开销获得比 Best-of-N 更优的质量分数（图 6）。

### 核心信号：累积得分差异

CFG-Rejection 的质量评估信号来源于分类器自由引导（CFG）机制中条件得分与无条件得分之间的累积差异。具体而言，在每个去噪步骤 $t$，记录条件得分预测 $S_{\theta}(\mathbf{x}_t; \sigma_t, \mathbf{c})$ 与无条件得分预测 $S_{\theta}(\mathbf{x}_t; \sigma_t, \emptyset)$ 之间的 L2 距离：

$$\mathcal{G}_t(c) = \| S_{\theta}(\mathbf{x}_t; \sigma_t, \mathbf{c}) - S_{\theta}(\mathbf{x}_t; \sigma_t, \emptyset) \|_2$$

该值反映了当前步骤中条件信息对去噪方向的瞬时影响强度。将去噪轨迹上指定区间的平方得分差累加，即得到累积得分差异（ASD）：

$$\mathcal{E}_{\tau:T}(c) = \sum_{t=T-\tau}^{T} \mathcal{G}_t(c)^2$$

其中 $T$ 为总去噪步数，$\tau$ 为控制累积窗口长度的超参数。$\mathcal{E}_{\tau:T}(c)$ 作为无外部奖励的内在质量指标，其有效性建立在以下关键观察之上：高 ASD 样本倾向于集中在数据分布的高密度主干区域，而低 ASD 样本则更多地出现在低密度分支区域，ASD 与样本的对数密度之间呈现线性正相关关系（图 3）。这一相关性在 ImageNet 生成样本上通过 AvgkNN 和 LOF 两种密度估计器得到了进一步验证（图 4）。

### 管道模块与数据流

CFG-Rejection 的推理管道由三个顺序模块构成：

1. **步骤得分差记录**：在去噪过程的每一步 $t$，同步计算并记录 $\mathcal{G}_t(c)$。该模块不改变原有的采样动力学，仅从 CFG 的中间计算中提取信息，因此计算开销极低。

2. **部分 ASD 累积**：当去噪进行到步骤 $T-\tau$ 时，开始累积从该步至当前步的平方得分差，形成 $\mathcal{E}_{\tau:T}(c)$。超参数 $\tau$ 控制着累积窗口的长度——$\tau$ 越大，累积的步骤越多，信号越稳定但计算开销也相应增加。实验表明，$\tau=10$ 即可带来显著改善，$\tau \geq 10$ 后性能趋于饱和。

3. **样本拒绝决策**：将 $\mathcal{E}_{\tau:T}(c)$ 与预设阈值 $\gamma$ 进行比较。若 $\mathcal{E}_{\tau:T}(c) < \gamma$，则判定当前样本为低质量轨迹，立即终止去噪过程；否则保留样本并继续完成剩余去噪步骤。阈值 $\gamma$ 可根据目标过滤比例或绝对质量要求进行设定，例如选取 Top 10% 高 ASD 样本或固定 $\tau=10$ 进行过滤。

### 适用范围与前提条件

需要指出，CFG-Rejection 的有效性依赖于分类器自由引导机制的存在，因此**不适用于无条件生成任务**。此外，当引导强度过高导致样本多样性极度收缩时（如 SDXL 在 $\omega=9$ 的设置下），ASD 的区分能力下降，方法的增益会相应减弱。该方法的 ASD-质量关联目前基于经验观察，尚缺乏严格的理论保证，其在不同 ODE 求解器和噪声调度下的行为也是值得进一步探索的开放问题。

![[assets/figures/papers/paper_list_l857_https_arxiv_org_abs_2505_23343/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of filtering framework. Best-of-N completes all denoising steps, using an external reward model to select the high-quality image, while our method halts low-quality generations early with the intrinsic information in the sampling path*

### 3.1 关键信号：累积得分差异（ASD）

CFG‑Rejection 的核心洞察在于：分类器自由引导（CFG）过程中，条件得分与无条件得分之间的差异并非单纯的“引导强度”副产品，而是与样本最终质量及所在数据流形密度存在强关联。该差异在完整去噪轨迹上的累积量被定义为**累积得分差异（Accumulated Score Differences, ASD）**，作为无需外部奖励模型的内在质量信号。

在二维玩具分布上的验证（Figure 3）表明：高 ASD 样本集中于数据分布的高密度主干区域，低 ASD 样本则出现在低密度分支，且 ASD 与局部对数密度之间呈现近似线性正相关。这一发现构成了整个方法的理论直觉基础。

### 3.2 公式体系与变量定义

CFG‑Rejection 的公式体系围绕三个核心量构建，逐步从单步差异到全轨迹累积，再到可早期计算的局部累积。

**步骤得分差** 定义为去噪过程中第 $t$ 步条件得分预测与无条件得分预测之间的 $L_2$ 距离：

$$
\mathcal { G } _ { t } ( c ) = \| S _ { \theta } ( \mathbf { x } _ { t } ; \sigma _ { t } , \mathbf { c } ) - S _ { \theta } ( \mathbf { x } _ { t } ; \sigma _ { t } , \emptyset ) \| _ { 2 }
\tag{5}
$$

其中：
- $S_{\theta}(\mathbf{x}_t; \sigma_t, \mathbf{c})$ 为条件 $\mathbf{c}$ 下的得分网络输出；
- $S_{\theta}(\mathbf{x}_t; \sigma_t, \emptyset)$ 为无条件（空文本嵌入）下的得分网络输出；
- $\sigma_t$ 为当前噪声尺度；
- $\mathcal{G}_t(c)$ 反映第 $t$ 步条件信息对去噪方向的瞬时影响强度。

**全轨迹累积得分差异** 将各步得分差的平方沿整条去噪轨迹求和：

$$
\mathcal { E } _ { T } ( c ) = \sum _ { t = 1 } ^ { T } \mathcal { G } _ { t } ( c ) ^ { 2 }
\tag{6}
$$

$\mathcal{E}_T(c)$ 刻画了条件信息在整个生成过程中对采样路径的总体影响程度，是用于最终样本质量排序的完整 ASD 指标。

**部分累积得分差异** 则是为实现早期过滤而引入的关键变体——仅累积从步骤 $T-\tau$ 到 $T$（即去噪过程的最后 $\tau$ 步）的平方得分差：

$$
\mathcal { E } _ { \tau : T } ( c ) = \sum _ { t = T - \tau } ^ { T } \mathcal { G } _ { t } ( c ) ^ { 2 }
\tag{7}
$$

其中 $\tau$ 为超参数，控制参与早期评估的步数。$\mathcal{E}_{\tau:T}(c)$ 使得方法无需等待完整去噪即可对样本质量做出预判，是实现计算节省的核心机制。

### 3.3 方法模块与执行流程

CFG‑Rejection 由三个顺序执行的模块构成，嵌入标准 CFG 采样流程中，无需修改模型权重或训练过程：

1. **步骤得分差追踪**：在每个去噪步骤 $t$，同步记录条件与无条件输出的 $L_2$ 差 $\mathcal{G}_t(c)$。该操作仅需一次额外的前向差分计算，开销极低。

2. **部分 ASD 累积**：从预设的起始步骤 $T-\tau$ 开始，按式 (7) 累积平方得分差，得到 $\mathcal{E}_{\tau:T}(c)$。$\tau$ 的选取平衡了评估可靠性与计算节省——$\tau$ 过小则信号不足，过大则失去早期过滤的意义。

3. **样本拒绝决策**：将 $\mathcal{E}_{\tau:T}(c)$ 与预设阈值 $\gamma$ 进行比较。若 $\mathcal{E}_{\tau:T}(c) < \gamma$，则判定当前轨迹为低质量路径，立即终止后续去噪步骤并丢弃该样本；否则继续完成完整去噪。这一“拒绝式”机制从根本上改变了传统 Best‑of‑N 的“先生成后选择”范式，将筛选时机前移至去噪早期。

## 实验与关键发现

### 核心机制验证：ASD 与样本密度的正相关

CFG-Rejection 的有效性建立在累积得分差异（ASD）与样本位于数据分布高密度区域概率之间的强关联之上。作者首先在可控的二维玩具分布上验证了这一假设。在分形结构的两类分布上使用 CFG（ω=2）生成样本，并按 ASD 进行颜色编码（Figure 3）。结果显示，高 ASD 样本高度集中于分布的主干高密度区域，而低 ASD 样本则散落在稀疏分支区域；进一步分析表明，ASD 与局部对数密度之间呈现对数-线性正相关趋势。这一观察在 ω=2.5、3、3.5 等不同引导强度下均保持一致（Figure 7–9，附录）。

在真实图像生成场景中，该相关性在 ImageNet 50 类上使用 EDM2-S 模型得到了系统验证（Figure 4）。作者采用 AvgkNN 和 LOF 两种密度估计器，将生成样本按 ASD 从高（rank 0）到低（rank 3）分为四组。密度估计曲线显示，随着 ASD 等级降低，样本分布从高密度区域系统性地向低密度区域偏移——这一模式在多个类别（如 Crib、Fountain、Parachute、Bulbul、Goldfish 等）上高度一致（Figure 10–12，附录）。定性对比（Figure 5）进一步佐证：低 ASD 样本常出现伪影、语义不对齐等问题，而高 ASD 样本则展现出更好的保真度和提示遵循度。

![[assets/figures/papers/paper_list_l857_https_arxiv_org_abs_2505_23343/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison on the ImageNet dataset. (Top) Baseline samples with the lowest*

**证据强度**：ASD-密度相关性在玩具分布和真实图像数据集上均得到一致验证，且使用两种独立的密度估计方法交叉确认，结论可信度高。

### 主实验结果：人类偏好与基准性能提升

#### ImageNet 上的质量过滤效果

Table 1 汇总了 EDM2-S 在 ImageNet 50 类上的过滤结果。以全部生成样本（Full set）为基线，选取 ASD 最高的前 10% 样本（Top 10%）后，PickScore 从 20.38 提升至 20.61（+0.23），HPSv2 从 26.13 提升至 26.57（+0.44），AES 从 4.82 提升至 4.86。值得注意的是，仅使用部分 ASD（τ=10，即仅观察最后 10 步的累积得分差）进行过滤，即可获得与使用完整 ASD（τ=T）接近的性能——PickScore 达 20.57，HPSv2 达 26.50。这表明早期信号已包含足够的质量判别信息，为提前终止低质量轨迹提供了实证基础。

![[assets/figures/papers/paper_list_l857_https_arxiv_org_abs_2505_23343/figures/006_Table_1.jpg]]
*Table 1: The quantitative results on ImageNet dataset*

#### GenEval 与 DPG-Bench 上的跨基准泛化

在更大规模的文本到图像生成基准上，CFG-Rejection 展现出跨模型和跨引导强度的鲁棒性。在 SDv1.5 模型上（Table 2），当引导强度为 5 时，使用 τ=20 的部分 ASD 过滤将 GenEval 整体得分从随机采样的 0.4152 提升至 0.4594（+4.42 个百分点）；当引导强度提升至 9 时，整体得分从 0.4322 提升至 0.4785（+4.63 个百分点）。DPG-Bench 上的趋势一致（Table 3）：SDv1.5 在引导强度为 5 时，τ=20 过滤将整体得分从 62.45 提升至 64.14（+1.69）。

![[assets/figures/papers/paper_list_l857_https_arxiv_org_abs_2505_23343/figures/008_Table_2.jpg]]
*Table 2: The quantitative results on GenEval. Model: SDv1.5*

![[assets/figures/papers/paper_list_l857_https_arxiv_org_abs_2505_23343/figures/009_Table_3.jpg]]
*Table 3: The quantitative results on DPG-bench. Model: SDv1.5*

在 SDXL 模型上（Table 4–5，附录），CFG-Rejection 同样有效，但增益幅度有所收窄。当引导强度从 5 提升至 9 时，过滤带来的提升减小，这与高引导强度下样本多样性降低、ASD 区分度下降的预期一致——此时大多数样本已经高度对齐条件，ASD 信号的可区分性自然减弱。

![[assets/figures/papers/paper_list_l857_https_arxiv_org_abs_2505_23343/figures/027_Table_4.jpg]]
*Table 4: The quantitative results on GenEval. Model: SDXL*

#### 受限推理预算下的计算效率优势

CFG-Rejection 的核心设计优势在于早期过滤带来的计算节省。在受限推理预算的对比实验中（Figure 6），作者将 CFG-Rejection 与 Best-of-N 策略进行对比：前者在去噪早期（步骤 T-τ 后）即可根据部分 ASD 决定是否终止当前轨迹，后者则需完成全部去噪步骤后再用外部奖励模型选择。结果显示，在低时间预算区，CFG-Rejection 以更少的计算量取得了更高的 PickScore 和 HPSv2 分数，证明其在实用场景中的效率优势。

### 消融研究

#### 超参数 τ 的影响

τ 控制用于早期过滤决策的 ASD 累积步数。Table 1 显示，τ 从 5 增加到 10 时性能已有显著改善，τ≥10 后性能趋于饱和。这意味着仅需观察最后约 10 步的得分差异，即可有效判别样本质量，大幅降低了过滤所需的最小计算开销。在 GenEval 和 DPG-Bench 上，τ=20 通常已接近性能上限。

#### 引导强度与过滤比例的交互

在 SDXL 上，当引导强度从 5 增加到 9 时，CFG-Rejection 的提升幅度减小（Table 4–5）。这是因为高引导强度本身已迫使生成过程强烈偏向条件模式，ASD 的方差缩小，过滤空间受限。此外，作者验证了在不同总生成数下保持相同过滤比例（如 4/20 与 4/50）时，性能接近，说明该方法在有限推理预算下仍能有效工作。

### 视觉文本生成与复杂提示对齐

在 FLUX 模型上的定性实验（Figure 2, 21–23）展示了 CFG-Rejection 在复杂文本渲染任务中的能力。对于包含长文本的提示（如“A night sky with constellations forming the words...”），低 ASD 样本常出现笔画缺失或文本不可读，而高 ASD 样本则能可靠地渲染完整短语。在海报生成任务中（Figure 23），高 ASD 样本的标题位置合理且清晰可辨，低 ASD 样本则标题缺失或不完整。这些结果提示 ASD 信号捕捉到了与细粒度文本-图像对齐相关的语义信息。

### 失败模式与局限性

1. **无条件生成不适用**：CFG-Rejection 依赖分类器自由引导中的条件-无条件得分差异，因此无法用于无条件生成任务。
2. **高引导强度下区分度下降**：当引导强度过高导致样本多样性极低时（如 SDXL 在 ω=9），ASD 的方差收窄，过滤增益有限。
3. **缺乏严格理论保证**：ASD 与样本质量的关联基于经验观察，尚未建立严格的理论框架。
4. **超参数需任务级调优**：τ 和阈值 γ 的选择需要根据具体模型和任务进行调整，缺乏自适应的自动化机制。
5. **语义保真度风险**：早期过滤在何种条件下可能丢失特定语义属性（如 DPG-Bench 中 Attribute 与 Relation 类别对 τ 变化的不同响应），仍需进一步研究。

## 定位与知识库关联

### 问题定位：扩散模型推理时对齐的效率瓶颈

扩散模型在文本到图像生成中已取得显著进展，但采样过程的随机性导致生成质量不稳定——同一提示词可能产生高保真图像，也可能输出语义缺失或结构扭曲的样本。现有推理时对齐方法主要分为两类：**基于外部奖励的后选择方法**（如 Best-of-N 采样）和**基于奖励引导的生成方法**（如 **Direct Noise Optimization (DNO)** 和 **Loss-Guided Diffusion (LGD)**）。前者需要生成完整样本后通过奖励模型（如 PickScore、HPSv2）筛选，后者则直接在去噪过程中注入外部奖励信号进行优化。

这两类方法共享两个根本性局限：其一，**依赖外部奖励模型**，引入额外的模型加载、推理和存储开销，且奖励模型本身可能存在偏差；其二，**需要完整的去噪过程**，无法在早期识别并丢弃低质量轨迹，导致计算资源的大量浪费。CFG-Rejection 正是在这一效率瓶颈上提出突破——利用扩散模型采样路径中**固有的内在信号**替代外部奖励，并在去噪早期实现低质量样本的**提前终止**，从而将筛选成本从“全流程生成后评估”压缩为“部分去噪后决策”。

### 与现有方法的关系图谱

#### 对比方法：Best-of-N 采样

Best-of-N 是最直接的推理时质量提升策略：从同一提示词独立生成 N 个完整样本，通过外部奖励模型评分后选取最优者。该方法的核心缺陷在于**计算效率极低**——所有 N 个样本必须完成全部去噪步骤，即使其中大部分最终会被丢弃。CFG-Rejection 在机制上构成了 Best-of-N 的**对偶方案**：前者是“生成-筛选”，后者是“筛选-生成”。实验表明（Figure 6），在受限推理预算下，CFG-Rejection 通过早期过滤在低时间区内比 Best-of-N 更快取得高分，验证了“先筛选后生成”策略的计算效率优势。

#### 对比方法：奖励引导生成方法（DNO / LGD）

**Direct Noise Optimization (DNO)** 和 **Loss-Guided Diffusion (LGD)** 通过在去噪过程中引入外部奖励模型的梯度信号来引导生成方向，本质上属于**优化式对齐**。这类方法虽然避免了 Best-of-N 的重复生成开销，但仍需加载并查询外部奖励模型，且梯度计算增加了单步去噪的计算负担。CFG-Rejection 与这类方法的根本区别在于**信号来源**：DNO/LGD 依赖外部奖励模型提供的“他评”信号，而 CFG-Rejection 利用 CFG 机制中条件得分与无条件得分之间的累积差异（ASD）作为“自评”信号。这一设计使 CFG-Rejection 实现了**完全自包含的质量评估**，无需任何外部模型或额外训练。

#### 方法定位：即插即用的过滤式策略

从方法论谱系看，CFG-Rejection 属于**过滤式推理时对齐**（filtering-based inference-time alignment），区别于优化式方法（DNO/LGD）和全量后选择方法（Best-of-N）。其核心创新在于将过滤时机从“去噪后”前移至“去噪中”，并将过滤信号从“外部奖励”转换为“内在 ASD”。作为即插即用策略，CFG-Rejection 不修改模型权重、不改变采样调度器、不引入额外网络，可直接应用于任何使用分类器自由引导的扩散模型（如 EDM2、Stable Diffusion v1.5、SDXL、FLUX）。

### 适用边界与局限性

#### 对 CFG 机制的强依赖

CFG-Rejection 的核心信号 ASD 来源于分类器自由引导过程中条件与无条件得分的差异，因此**不适用于无条件生成任务**（如无条件图像合成、纯噪声驱动的生成）。当 CFG 引导强度 ω=1（即无条件生成）时，ASD 恒为零，方法完全失效。这一依赖将方法的适用范围限定在文本到图像、类别条件生成等有条件场景。

#### 高引导强度下的区分度衰减

在 SDXL 模型上，当引导强度从 ω=5 增加到 ω=9 时，CFG-Rejection 的提升幅度减小（Table 4, Table 5）。分析表明，过高的引导强度会压缩样本多样性，使 ASD 在不同质量样本间的区分度下降——当几乎所有样本都被强引导至相似的高密度区域时，ASD 作为筛选信号的有效性自然衰减。这一现象揭示了 ASD 信号质量与生成多样性之间的内在张力：**方法在需要高多样性的场景中最为有效，而在追求极致一致性的低多样性场景中增益有限**。

#### 超参数调优需求

CFG-Rejection 引入了两个关键超参数：部分累积起始步 τ 和拒绝阈值 γ。τ 控制“观察窗口”的长度——τ 过小则信号不足以区分质量，τ 过大则损失早期过滤的效率优势。实验表明 τ=10 即可接近性能上限（Table 1），但该最优值可能随模型架构、噪声调度器和任务类型而变化。阈值 γ 决定了过滤的严格程度，需要在“通过率”与“质量提升幅度”之间权衡。目前缺乏自动确定最优 τ 和 γ 的机制，实际部署时需要针对具体模型和任务进行**经验性调优**。

#### 理论保证的缺失

ASD 与样本质量之间的关联基于**经验观察**——在二维玩具分布（Figure 3）和 ImageNet 真实数据（Figure 4）上均验证了 ASD 与数据密度的正相关性，但这一相关性缺乏严格的理论证明。论文未给出 ASD 作为质量信号的一致性保证或误差界，使得方法在安全关键应用中的可靠性存疑。此外，早期过滤在何种条件下可能丢失语义保真度，目前仅停留在定性讨论层面，缺乏系统的失效模式分析。

### 开放问题与未来方向

1. **ASD-密度相关性的结构条件**：在什么模型架构、噪声调度和数据类型下，累积分数差异与样本密度之间的正相关关系能够被严格保证？回答这一问题需要从得分匹配的理论性质出发，分析 CFG 轨迹的几何结构。

2. **早期过滤的语义保真度边界**：在去噪早期（高噪声阶段）终止轨迹，是否会导致某些需要细粒度语义推理的样本被系统性误杀？例如，DPG-Bench 中 Attribute 与 Relation 类别对 τ 变化的响应差异（Table 3）暗示不同语义维度对 ASD 的敏感度不同，这能否用于设计更细粒度的过滤策略？

3. **求解器与噪声调度的交互效应**：不同 ODE 求解器（如 Heun、DPM-Solver）和噪声调度策略（线性、余弦）如何影响 ASD 信号的时序特征和区分能力？这一问题的回答将决定 CFG-Rejection 在不同扩散模型实现间的可迁移性。

4. **ASD 信号的语义可解释性**：ASD 捕捉的究竟是全局图像质量、局部细节保真度、还是文本-图像对齐强度？不同生成任务中 ASD 的变化趋势差异（如视觉文本渲染任务中 ASD 对文字完整性的强指示作用，Figure 2）提示 ASD 可能编码了多维度的语义信息，解耦这些维度有望实现更可控的生成质量调控。

5. **与优化式方法的融合潜力**：CFG-Rejection 的过滤式策略与 DNO/LGD 的优化式策略并非互斥——能否先用 ASD 快速过滤掉明显低质量轨迹，再对保留的少量轨迹施加轻量级奖励引导，从而在效率与质量之间取得更优平衡？

## 原文 PDF

![[paperPDFs/CVPR_2026/Diffusion_Sampling_Path_Tells_More_An_Efficient_Plug_and_Play_Strategy_for_Sample_Filtering.pdf]]
