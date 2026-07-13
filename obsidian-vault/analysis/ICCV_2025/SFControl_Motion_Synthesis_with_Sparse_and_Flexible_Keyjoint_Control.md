---
title: SFControl Motion Synthesis with Sparse and Flexible Keyjoint Control
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control.pdf
project_link: http://inwoohwang.me/SFControl
code_link: https://github.com/patrickkidger/torchcubicspline
aliases:
- SMSSFKC
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将控制问题解耦为低维关键关节轨迹合成与全身运动补全的两阶段扩散模型，利用关键关节的低维特性灵活适应稀疏、隐式及时间无关的控制信号。
primary_logic: 人类运动可由少量关键关节（末端效应器和根节点）的低维运动充分描述，因此在低维空间中可高效满足各类控制约束，然后通过强条件生成先验补全自然全身运动。
claims:
- 在仅使用0.454%关节信号作为控制的极端稀疏条件下，SFControl实现FID 0.224和Control Error 0.036m，显著优于CondMDI、OmniControl等方法。
- 两阶段分解相对于单阶段基线在目标驱动场景中将平均距目标距离从0.206m降至0.093m，且脚滑动更低。
- 时间无关控制使用弧长重参数化对齐损失，在无精确时间戳情况下将约束误差从0.4827（无时间无关机制）降至0.0256，并保持高运动质量。
- 随机掩码训练策略使得模型对不同控制信号选择（关节组合、稀疏度）具有鲁棒性，在多种极端设置下仍保持稳定性能。
---

# SFControl Motion Synthesis with Sparse and Flexible Keyjoint Control

> [!tip] 核心洞察
> 人类运动可由少量关键关节（末端效应器和根节点）的低维运动充分描述，因此在低维空间中可高效满足各类控制约束，然后通过强条件生成先验补全自然全身运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | SFControl：基于稀疏灵活关键关节控制的运动合成 |
| 英文题名 | SFControl Motion Synthesis with Sparse and Flexible Keyjoint Control |
| 会议/期刊 | ICCV 2025 |
| Links | [Project](http://inwoohwang.me/SFControl) · [Code](https://github.com/patrickkidger/torchcubicspline) · [paper](https://arxiv.org/abs/2503.15557) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SFControl |
| Dataset | HumanML3D, Goal-driven reaching task, Goal-driven all scenarios, Implicit control: hand-to-head contact |

> [!tip] 效果简介
> - HumanML3D (sparse joint control, 0.454% signals) 上，FID 0.224 vs 0.498 (CondMDI) (-0.274)；Control Error (m) 0.036 vs 0.111 (OmniControl) (-0.075)。
> - Goal-driven reaching task 上，Distance to Goal (m) 0.054 vs 0.141 (single-stage) (-0.087)。
> - Goal-driven all scenarios (reaching, climbing, sitting) 上，Distance to Goal (m) 0.093 vs 0.206 (single-stage) (-0.113)。

## 概要

可控人体运动生成面临一个根本性瓶颈：现有方法依赖密集的时空控制信号（如每帧精确的关节轨迹），手工指定困难且不切实际；同时，在高维全身运动空间中直接满足稀疏约束，导致控制精度与运动自然度难以兼顾。SFControl 针对这一问题，提出将控制问题解耦为**低维关键关节轨迹合成**与**全身运动补全**的两阶段扩散框架。其核心洞察在于：人类运动可由少量关键关节（末端效应器与根节点）的低维运动充分描述，因此在低维空间中可高效满足各类控制约束，再通过强条件生成先验补全自然全身运动。

该方法实现了对显式稀疏控制、目标驱动控制、隐式目标函数控制以及时间无关轨迹控制的统一支持，在仅使用 **0.454%** 关节信号作为控制的极端稀疏条件下，FID 达到 0.224，控制误差低至 0.036m，显著优于 CondMDI、OmniControl 等基线。两阶段分解使目标驱动场景的平均距目标距离从 0.206m 降至 0.093m；时间无关控制通过弧长重参数化对齐损失，将约束误差从 0.4827 降至 0.0256，消除了对逐帧时间戳的依赖。随机掩码训练策略赋予模型对关节组合、稀疏度及分布外信号的强鲁棒性。当前框架的主要局限在于扩散采样带来的推理延迟（DDPM 约 7.1s，DDIM 加速后 0.7–1.4s），尚不支持实时交互。

在方法谱系上，SFControl 属于**分解式扩散运动生成**，其两阶段设计与单阶段直接控制方法（如 OmniControl、MotionLCM、DNO）形成对比，通过低维中间表示桥接了稀疏控制灵活性与全身运动质量。



### 可控运动生成的核心挑战

生成自然且可控的人体运动是计算机图形学与具身智能领域的基础问题，其核心矛盾在于**控制精度**与**运动自然度**之间的权衡。现有的可控运动生成方法通常依赖密集的时空控制信号——例如为每一帧指定精确的骨盆轨迹或全身关节位置——这类信号手工指定极为困难，在实际应用中往往不切实际。当控制信号变得稀疏时，直接在高维的全身运动空间中满足这些约束变得异常困难：模型要么牺牲运动质量以贴合稀疏控制点，要么产生自然但偏离控制目标的运动。

### 现有方法的瓶颈

当前主流方法在控制灵活性上存在三个结构性缺陷：

1. **控制信号密度过高**：基于扩散模型的方法（如 **OmniControl** (Xie et al., arXiv 2023)、**MotionLCM**）通常要求用户提供密集的关节级空间控制信号，这在实际交互场景中成本高昂。即便是在 HumanML3D 基准上，典型设置也需要提供远超实际可用的控制信息量。

2. **时间对齐要求严格**：几乎所有现有方法都假定控制信号带有精确的逐帧时间戳。然而，当用户希望指定“沿某条曲线行走”时，通常只能提供路径的几何形状，而无法给出每帧对应路径上哪一点的精确时序信息。这一时间无关（time-agnostic）的控制需求在现有框架中缺乏有效支持。

3. **高维空间中的约束满足困难**：直接在全身运动的高维表示空间中施加稀疏约束，本质上是一个欠定问题。模型缺乏足够的归纳偏置来从少量控制点推断出合理的全身姿态序列，导致控制误差与运动质量难以兼顾。

### 核心洞察：关键关节的低维特性

SFControl 的核心洞察源于对人体运动结构的观察：**人类运动可以由少量关键关节（末端效应器和根节点）的低维运动充分描述**。具体而言，双手、双脚、头部和骨盆根节点这七个关键关节的运动轨迹已经编码了绝大多数人类运动的语义信息。这一观察将高维全身运动控制问题转化为一个更易处理的形式：先在低维关键关节空间中精确满足各类控制约束，再利用强条件生成先验补全出自然的全身运动。

### 本文的动机与目标

基于上述洞察，SFControl 旨在构建一个能够处理**稀疏、灵活且时间无关**控制信号的运动合成框架。该框架需满足以下目标：

- **极端稀疏性**：在仅使用总关节信号 0.454% 的极端稀疏条件下（例如仅指定单帧中单个关节的位置），仍能生成高质量且精确受控的运动。
- **控制信号多样性**：同时支持显式关节位置控制、目标驱动的末端效应器到达任务、以及通过可微目标函数定义的隐式约束（如手-头接触、狭窄空间行走）。
- **时间无关性**：无需逐帧时间戳，仅凭几何路径即可驱动运动生成，大幅降低用户交互负担。
- **鲁棒性**：对不同控制信号的选择（关节组合、稀疏度变化）保持稳定性能，且对分布外控制信号具有一定的泛化能力。



## 核心方法与创新机理

SFControl 的核心创新在于将可控运动生成从一个高维全身空间的直接约束满足问题，**解耦为低维关键关节轨迹合成与全身运动补全的两阶段扩散框架**。这一架构设计直击现有方法的根本瓶颈：密集时空控制信号的手工指定困难，以及在高维空间中同时满足稀疏约束与保持运动自然度的固有矛盾。

### 1. 两阶段解耦架构：从高维困境到低维可控

现有可控运动生成方法（如 CondMDI、OmniControl、MotionLCM）普遍采用单阶段扩散模型，直接在全身运动空间 $\mathbf{X} \in \mathbb{R}^{N \times D}$ 上施加控制信号。当控制信号极度稀疏（例如仅指定个别关节的若干关键帧位置）时，模型需要在 $D$ 维空间中同时推断其余所有关节的自由度，导致控制精度与运动质量难以兼顾。

SFControl 的核心洞察在于：**人类运动可由少量关键关节（末端效应器和根节点）的低维运动充分描述**。基于此，框架将生成过程分解为两个级联的扩散模型：

- **第一阶段（Keyjoint Trajectory Model $\mathcal{D}_{\mathbf{c}}$）**：在低维关键关节空间 $\mathbf{C} \in \mathbb{R}^{N \times d}$（$d \ll D$）中合成轨迹，精确满足各类控制信号。由于空间维度极低，模型可以高效地适应稀疏、隐式及时间无关的控制约束。
- **第二阶段（Full-Body Motion Completion Model $\mathcal{D}_{\mathbf{x}}$）**：以第一阶段生成的密集关键关节轨迹为强条件，补全自然的全身运动 $\mathbf{X}$。

这一解耦将“满足约束”与“保证自然度”两个目标分配至不同阶段，使每个模型各司其职。消融实验（Table 2）证实：单阶段变体在目标驱动场景中的平均距目标距离为 0.206m，而两阶段框架将其降至 0.093m，脚滑动也从 0.057 降至 0.047。

### 2. 稀疏与灵活的控制信号机制

与依赖密集时空信号（如全序列骨盆轨迹加精确时间戳）的先前工作不同，SFControl 设计了三种互补的控制信号处理机制，覆盖从显式到隐式、从时间精确到时间无关的全谱系控制需求。

**显式控制与随机掩码训练**。训练时，模型通过随机时空掩码 $\mathbf{m}_{\mathbf{C}}$ 将干净关键关节值注入噪声样本：
$$\mathbf{C}_t' = \mathbf{m}_{\mathbf{C}} \circ \mathbf{C}_0 + (1 - \mathbf{m}_{\mathbf{C}}) \circ \mathbf{C}_t$$
推理时则以用户指定的掩码 $\mathbf{m_s}$ 注入控制信号 $\mathbf{s}$：
$$\mathbf{C}_t' = \mathbf{m_s} \circ \mathbf{s} + (1 - \mathbf{m_s}) \circ \mathbf{C}_t$$
这一策略使模型在训练中见过任意关节组合、任意稀疏度的控制模式，从而在推理时对控制信号的选择具有高度鲁棒性。实验表明，在仅使用 **0.454%** 关节信号（即 22 个关节中仅控制 1 个关节的 10% 时间帧）的极端稀疏条件下，SFControl 实现 FID 0.224 和 Control Error 0.036m，显著优于 CondMDI（FID 0.498）和 OmniControl（Control Error 0.111m）（Table 1）。

**隐式控制与扩散潜变量优化**。对于无法表示为显式关键帧的约束（如“手触头”、“在狭窄空间行走”），SFControl 将控制信号定义为关键关节集上的可微目标函数 $\mathcal{F}(\cdot)$，并通过反向传播梯度在扩散潜空间中优化。关键创新在于：梯度优化作用于低维关键关节空间 $\mathbf{C}$ 而非高维全身空间，避免了高维优化的不稳定性和计算开销。在 hand-to-head contact 任务中，SFControl 的约束误差为 0.0084，优于直接在全身空间优化的 DNO 方法（0.0101）（Table 3）。

**时间无关控制与弧长重参数化**。针对无需精确时间戳的轨迹控制（如“手画一个圆”），SFControl 提出弧长重参数化对齐损失，消除了对逐帧时间标注的依赖。其核心是对关键关节轨迹段 $\mathbf{C}_{\mathrm{seg}}$ 计算累积弧长，并均匀重采样以构建时间无关表示，再通过组合损失进行优化：
$$\mathcal{L}_{\mathrm{align}} = \| \mathbf{C}_{\mathrm{seg}}^{\mathrm{res}} - \mathcal{T}^{\mathrm{res}} \| + \lambda_l \cdot | s_L - L(\mathcal{T}) |$$
第一项保证重采样轨迹与目标轨迹的几何一致性，第二项保证轨迹长度一致。这一机制将约束误差从无时间无关机制时的 0.4827 骤降至 0.0256，同时保持高运动质量（Table 3）。

### 3. 随机掩码训练策略带来的鲁棒性

SFControl 的随机掩码训练策略不仅是显式控制的技术实现，更是框架鲁棒性的核心保障。通过在训练中随机遮盖关键关节的时空维度，模型学会从任意部分观测中推断完整关键关节轨迹。这一策略带来三重收益：
- **关节选择鲁棒性**：无论控制单关节、多关节还是不同关节组合，FID 仅在 0.127–0.352 之间波动（Table 6）。
- **稀疏度鲁棒性**：在控制稀疏度跨越多个数量级时，FID 和控制误差保持稳定，优于所有基线方法（Figure 5）。
- **分布外鲁棒性**：即使控制信号被注入分布外噪声，方法仍保持可靠的控制精度和运动质量（Table 7）。

### 与基线方法的系统性差异

| 架构维度 | 基线方法 | SFControl |
|---------|---------|-----------|
| 管线架构 | 单阶段扩散直接生成全身运动 | 两阶段扩散：关键关节轨迹 → 全身补全 |
| 控制信号密度 | 密集时空信号（如全序列轨迹） | 稀疏灵活，低至 0.454% 关节信号 |
| 时间对齐需求 | 需精确逐帧时间戳 | 支持时间无关控制，无需时间标注 |
| 训练策略 | 以给定控制信号重建全身运动 | 随机时空掩码训练 + 无分类器引导 |
| 隐式控制 | 在全身边界空间优化（如 DNO） | 在低维关键关节空间优化 |

这些 changed slots 共同构成了 SFControl 相对于现有可控运动生成方法的系统性进步：不再要求用户提供密集精确的控制信号，而是通过架构解耦和灵活的信号处理机制，在保持高运动质量的前提下，大幅降低了可控运动生成的使用门槛。



SFControl 提出一种**两阶段解耦扩散框架**，将可控运动生成问题分解为低维关键关节轨迹合成与全身运动补全两个子任务。该设计的核心洞察在于：人类运动可由少量关键关节（双手、双脚、根节点、头部）的运动充分描述，因此在低维空间中高效满足各类控制约束后，再通过强条件生成先验补全自然全身运动，从而兼顾控制精度与运动质量。

### 两阶段流水线

框架的整体流程如图2所示，包含以下核心模块：

1. **关键关节轨迹模型 (Keyjoint Trajectory Model, D_c)**：第一阶段从稀疏、灵活的控制信号出发，合成完整的低维关键关节轨迹 C。该模型是一个条件扩散模型，在训练时通过随机掩码策略学习从任意稀疏观测中恢复完整关键关节运动；在推理时，通过将显式控制信号注入噪声样本或对隐式目标函数进行扩散潜变量优化，确保生成轨迹精确满足控制约束。

2. **全身运动补全模型 (Full-Body Motion Completion Model, D_x)**：第二阶段以第一阶段生成的关键关节轨迹 C_0 作为强条件，补全生成自然、高质量的全身运动 X。该模型同样基于条件扩散框架，在训练时将真实关键关节轨迹直接注入噪声化的全身运动样本中，迫使模型学习关键关节与全身姿态之间的协调映射。

### 输入输出流

- **输入**：控制信号 s 与文本描述 l。控制信号可以是显式的稀疏关键关节位置/轨迹、目标驱动的位置约束，或隐式的可微分目标函数；文本描述提供运动风格与类别的语义先验。
- **第一阶段输出**：完整的 N 帧关键关节轨迹 C ∈ ℝ^(N×d)，其中 d 为关键关节的自由度（远小于全身自由度 D）。
- **第二阶段输出**：最终的全身运动序列 X ∈ ℝ^(N×D)，在满足关键关节约束的同时保持运动自然度与多样性。

### 关键设计选择

- **随机掩码训练策略**：在关键关节轨迹模型的训练中，采用随机时空掩码 m_C 将干净关键关节值注入噪声样本（C_t' = m_C ∘ C_0 + (1 - m_C) ∘ C_t），使模型适应任意关节组合与稀疏度的控制信号，从而在推理时无需针对特定控制模式重新训练。
- **无分类器引导**：两阶段均在推理时采用无分类器引导（CFG，w=2.5），通过混合条件与无条件预测增强控制信号的约束力，同时保持生成质量。
- **时间无关控制机制**：对于无精确时间戳的轨迹控制，框架引入弧长重参数化与对齐损失（组合几何对齐项与长度一致性项），消除对逐帧时间标注的依赖。

> **注意**：关于各模块的具体公式推导、训练损失以及不同控制模式（显式、目标驱动、隐式、时间无关）的详细实现，请参见后续“核心方法”章节。



SFControl 将可控运动生成解耦为两个级联的扩散模型：**关键关节轨迹模型**（Keyjoint Trajectory Model, $\mathcal{D}_{\mathbf{c},\theta}$）与**全身运动补全模型**（Full-Body Motion Completion Model, $\mathcal{D}_{\mathbf{x},\theta}$）。其核心洞见在于：人类运动可由少量关键关节（末端效应器与根节点）的低维运动充分描述，因此在低维空间中可高效满足各类控制约束，再通过强条件生成先验补全自然全身运动。

### 关键关节轨迹模型

令 $\mathbf{C} = \{\mathbf{c}^n\}_{n=1}^{N} \in \mathbb{R}^{N \times d}$ 表示 $N$ 帧的关键关节轨迹，每帧 $\mathbf{c}^n$ 编码关键关节的运动学状态；全身运动表示为 $\mathbf{X} \in \mathbb{R}^{N \times D}$，其中 $D \gg d$。模型以文本描述 $l$ 为条件，训练目标为条件扩散的标准简单损失：

$$
\mathcal{L}_{\mathrm{simple},\mathbf{c}} = \mathbb{E}_{\mathbf{C}_0 \sim p(\mathbf{C}_0 \mid l),\, t \sim [1,T]} \left[ \| \mathbf{C}_0 - \mathcal{D}_{\mathbf{c},\theta}(\tilde{\mathbf{C}}_t, t, l) \|_2^2 \right]
$$

其中 $\tilde{\mathbf{C}}_t$ 为经控制信号注入后的噪声样本。

#### 显式控制信号的随机掩码注入

为使模型适应任意稀疏度与关节组合的控制信号，训练时采用随机时空掩码策略。给定干净轨迹 $\mathbf{C}_0$ 与噪声样本 $\mathbf{C}_t = \sqrt{\bar{\alpha}_t}\,\mathbf{C}_0 + \sqrt{1-\bar{\alpha}_t}\,\boldsymbol{\epsilon}$，通过随机二值掩码 $\mathbf{m_C}$ 将干净值注入噪声样本：

$$
\mathbf{C}_t' = \mathbf{m_C} \circ \mathbf{C}_0 + (1 - \mathbf{m_C}) \circ \mathbf{C}_t
$$

推理时，显式控制信号 $\mathbf{s}$ 通过其对应的掩码 $\mathbf{m_s}$ 注入当前噪声样本：

$$
\mathbf{C}_t' = \mathbf{m_s} \circ \mathbf{s} + (1 - \mathbf{m_s}) \circ \mathbf{C}_t
$$

该机制使得用户可任意指定被控关节、时间区间及稀疏度，无需完整轨迹标注。

#### 隐式控制与扩散潜变量优化

对于无法表示为显式关键点坐标的隐式约束（如手-头接触、狭窄空间行走），SFControl 将其定义为关键关节集 $\mathcal{I}$ 上的可微目标函数 $\mathcal{F}(\cdot)$。优化过程将目标函数的梯度通过扩散去噪网络反向传播至潜变量空间，更新噪声样本以逐步满足约束。这一机制使框架能够处理目标驱动场景——训练时仅将初始姿态与末帧目标控制关节作为控制信号注入，推理时通过潜变量优化使生成轨迹收敛至目标位置。

#### 时间无关的弧长重参数化

当控制轨迹 $\mathcal{T}$ 缺乏逐帧时间戳时，SFControl 采用弧长重参数化实现时间无关对齐。首先从生成轨迹中提取目标时间窗 $[t_0, t_1]$ 内的片段 $\mathbf{C}_{\mathrm{seg}}$，计算累积弧长：

$$
s_i = \begin{cases}
0, & i = 1 \\
s_{i-1} + \lVert \mathbf{c}^{t_0 + i - 1} - \mathbf{c}^{t_0 + i - 2} \rVert, & i = 2, \ldots, L
\end{cases}
$$

其中 $L = t_1 - t_0 + 1$。随后沿弧长均匀重采样 $L$ 个点：

$$
\tilde{s}_k = \frac{k-1}{L-1} \cdot s_L, \quad k \in \{1, \dots, L\}
$$

对齐损失由几何一致性项与长度约束项组合而成：

$$
\mathcal{L}_{\mathrm{align}} = \| \mathbf{C}_{\mathrm{seg}}^{\mathrm{res}} - \mathcal{T}^{\mathrm{res}} \| + \lambda_l \cdot | s_L - L(\mathcal{T}) |
$$

第一项衡量重采样轨迹与目标轨迹的 L2 距离，第二项约束轨迹总弧长与目标轨迹长度 $L(\mathcal{T})$ 一致。该公式消除了对逐帧时间对齐的依赖，使框架可直接接受无时间戳的路径输入。

### 全身运动补全模型

第一阶段生成的关键关节轨迹 $\mathbf{C}_0$ 作为强条件信号，指导全身运动补全模型生成最终的自然运动。训练时，将真实关键关节轨迹直接注入噪声化的全身运动 $\mathbf{X}_t$ 的对应维度：

$$
\mathbf{X}_t^{\mathrm{keyjoints}} = \mathbf{C}_0
$$

训练损失为条件扩散的标准形式：

$$
\mathcal{L}_{\mathrm{simple},\mathbf{x}} = \mathbb{E}_{\mathbf{X}_0 \sim p(\mathbf{X}_0 \mid \mathbf{C}_0, l),\, t \sim [1,T]} \left[ \| \mathbf{X}_0 - \mathcal{D}_{\mathbf{x},\theta}(\mathbf{X}_t, t, l) \|_2^2 \right]
$$

### 无分类器引导

两个阶段在推理时均采用无分类器引导，引导权重 $w = 2.5$，以增强条件一致性与生成质量：

$$
\hat{\mathbf{C}}_0 = w \cdot \mathcal{D}_{\mathbf{c},\theta}(\tilde{\mathbf{C}}_t, t, l) + (1 - w) \cdot \mathcal{D}_{\mathbf{c},\theta}(\tilde{\mathbf{C}}_t, t, \emptyset)
$$

全身模型采用相同形式的引导公式。

### 关键设计总结

两阶段分解的本质优势在于**维度隔离**：关键关节轨迹模型工作在极低维空间（$d \ll D$），使稀疏约束的满足变得高效且精确；全身补全模型则专注于从完整关键关节轨迹中恢复自然的高维运动。随机掩码训练策略赋予框架对任意控制信号配置的鲁棒性，弧长重参数化则突破了传统方法对精确时间戳的依赖，三者共同构成了 SFControl 灵活控制能力的算法基础。



## 实验与关键发现

### 核心实验设置

所有实验基于 **HumanML3D** 数据集进行，评估指标覆盖运动质量（**FID**、**Diversity**、**Foot Skating**）与控制精度（**Control Error**、**Distance to Goal**、**Constraint Error**）。基线方法包括 **CondMDI**、**OmniControl**（Xie et al., arXiv 2023）、**TLControl**、**MotionLCM** 和 **DNO**，均使用官方预训练模型或按原论文配置重新训练，推理时间对比统一在 NVIDIA RTX 2080 上进行。SFControl 默认使用 DDPM 50 步采样，无分类器引导权重 $w=2.5$。

---

### 主实验结果

#### 稀疏显式控制（Table 1）

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation of the sparse joint control. We validate our framework under a highly sparse control setting, which uses only 0.454% of total joint signal as control input. Bold represents the best value, and underlined represents the second-best*

在最极端的稀疏设置下——仅使用 **0.454%** 的全身关节信号作为控制输入（即仅指定关键关节的稀疏时空位置），SFControl 在所有指标上均显著优于基线：

- **FID**：0.224（SFControl） vs 0.498（CondMDI） vs 0.689（OmniControl），运动质量提升幅度超过 55%。
- **Control Error**：0.036m（SFControl） vs 0.111m（OmniControl） vs 0.128m（TLControl），控制精度提升约 67%。
- **Diversity**：9.674（SFControl） vs 8.823（OmniControl），表明在精确满足约束的同时仍保持了高运动多样性。

这一结果验证了核心设计思路：在低维关键关节空间中处理稀疏约束远比在高维全身空间中直接控制更为有效。CondMDI 虽能生成较自然的运动（FID 0.498），但其控制误差高达 0.227m，说明单阶段模型在稀疏控制下难以兼顾精度与质量。

#### 目标驱动控制（Table 2, Figure 3）

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/005_Table_2.jpg]]
*Table 2: Quantitative evaluation on the goal-driven scenarios. We train a unified network across three different tasks and evaluate it separately for each task as well as collectively*

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/003_Figure_3.jpg]]
*Figure 3: Qualitiative results of goal-driven motion scenarios, demonstrating reaching target hand positions, climbing with rock constraints, and sitting with hand control, respectively*

目标驱动场景仅给定起始姿态和末端目标位置（如手部到达目标点、攀岩握点、坐姿控制），不提供中间轨迹。SFControl 与单阶段变体（Ours w/o decomp.）的对比揭示了**两阶段分解的关键作用**：

- 在所有三类任务（Reaching、Climbing、Sitting）的聚合评估中，**Distance to Goal** 从单阶段的 0.206m 降至 SFControl 的 **0.093m**（降幅 55%）。
- **Foot Skating** 从 0.057 降至 **0.047**，表明分解框架有助于保持足部接触的物理合理性。
- 在单独的 Reaching 任务上，距目标距离从 0.141m 降至 **0.054m**。

因果机制在于：第一阶段在低维关键关节空间中完成从起始到目标的轨迹合成，该空间的约束维度远低于全身空间，扩散模型更容易找到满足目标且运动合理的解；第二阶段的全身边界补全模型则继承了强条件关键关节轨迹，无需再处理目标约束，从而专注生成自然协调的全身运动。

#### 隐式控制与时间无关控制（Table 3, Figure 4）

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/007_Table_3.jpg]]
*Table 3: Quantitative evaluation on different objective defined task scenarios*

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/006_Figure_4.jpg]]
*Figure 4: Example of time-agnostic trajectory target input and synthesized motion from time-agnostic control*

隐式控制通过可微目标函数 $\mathcal{F}(\cdot)$ 定义约束（如手-头接触、狭窄空间行走），无需显式指定关节位置。SFControl 将目标函数应用于关键关节轨迹层，通过扩散潜变量优化满足约束：

- **手-头接触**：Constraint Error 0.0084（SFControl） vs 0.0101（DNO）。
- **狭窄空间行走**：Constraint Error 0.0086（SFControl） vs 0.0093（Ours w/o decomp.），且 FID 从 0.255 改善至 0.228。

**时间无关控制**是 SFControl 的独特能力——用户仅提供无时间戳的空间轨迹（如一条 S 曲线），方法通过弧长重参数化与对齐损失 $\mathcal{L}_{\mathrm{align}}$ 自动匹配时序。消融实验（Table 3）显示：
- 无时间无关机制时，Constraint Error 高达 **0.4827**，运动完全无法跟随目标轨迹。
- 启用弧长对齐后，Constraint Error 骤降至 **0.0256**，且 FID 保持 0.256 的良好水平。

这一机制从根本上消除了对逐帧时间标注的依赖，极大降低了控制信号的手工指定成本。

---

### 消融研究

#### 两阶段分解的必要性（Table 2, Table 3）

多组消融一致证明两阶段分解是 SFControl 性能的核心来源：
- 在目标驱动场景中，单阶段变体在所有任务上均显著劣于两阶段版本（Distance to Goal: 0.206m vs 0.093m）。
- 在隐式控制中，将目标函数直接应用于全身边界模型（Ours w/o decomp.）导致更高的约束误差和更差的运动质量。
- 在时间无关控制中，单阶段模型无法有效利用弧长对齐机制，约束误差高达 0.4827。

根本原因：全身运动空间维度高（$D \gg d$），扩散模型在满足稀疏/隐式约束时面临严重的优化困难；而低维关键关节空间（仅含双手、双脚、根节点、头部）使约束满足变得可控，随后通过强条件生成补全全身运动。

#### 随机掩码训练策略的鲁棒性（Table 6）

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/011_Table_6.jpg]]
*Table 6: Quantitative evaluation of diverse control signal selection strategies. Our method demonstrates robust performance, regardless of sparsity, the number or combinations of multiple joints*

SFControl 在训练时采用随机时空掩码 $\mathbf{m_C}$ 注入干净控制信号，使模型适应任意关节组合与稀疏度。Table 6 验证了该策略的有效性：
- 单关节控制（仅左手、仅右脚等）：FID 在 0.127-0.352 之间，Control Error 在 0.017-0.045m。
- 多关节组合（双手+双脚、所有关键关节等）：性能保持稳定，FID 最低 0.127（所有关键关节），最高 0.352（仅头部）。
- 不同稀疏度（从 1 帧到全序列）：FID 波动范围仅 0.127-0.352，Control Error 始终低于 0.045m。

Figure 5 进一步展示了控制稀疏度（对数尺度）与 FID/Control Error 的关系曲线：SFControl 的性能曲线近乎平坦，而所有基线方法随稀疏度增加性能急剧恶化。

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/010_Figure_5.jpg]]
*Figure 5: We plot the performance of log control sparsity (x-axis) against the FID score and Control error (y-axis), which assess motion quality and precision, respectively. Our framework maintains consistent performance across varying control input sparsity, outperforming all baselines*

#### 分布外（OOD）控制信号的鲁棒性（Table 7）

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/012_Table_7.jpg]]
*Table 7: Experiments on Out-of-Distribution control signals. By comparing with in-distribution results (denoted as “In-data”), our method demonstrates robust performance with out-of-distribution signals*

向控制信号注入不同程度的高斯噪声以模拟分布外输入，SFControl 表现出强鲁棒性：
- 在噪声标准差 $\sigma=0.05$ 时，Control Error 仅从 0.036m（In-data）轻微上升至 0.042m，FID 从 0.224 变为 0.231。
- 即使 $\sigma=0.1$，Control Error 仍保持在 0.056m，显著优于基线方法在无噪声下的表现。

#### 采样策略与推理效率（Table 5, Table 9）

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/015_Table_9.jpg]]
*Table 9: Quantitative evaluation of various sampling strategies for diffusion models*

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/009_Table_5.jpg]]
*Table 5: Time required for motion control*

- DDPM 50 步总推理时间约 **7.1s**（关键关节模型 0.4s + 全身模型 6.7s）。
- DDIM 5 步将总时间降至 **0.7s**（约 10 倍加速），FID 仅从 0.224 升至 0.248，Control Error 从 0.036m 升至 0.049m，仍优于所有基线。
- DDIM 10 步在 1.4s 内实现与 DDPM 50 步接近的性能（FID 0.235, Control Error 0.041m）。

#### 全身边界补全模型的输入源分析（Table 4）

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/008_Table_4.jpg]]
*Table 4: Quantitative evaluation of full-body motion completion model on different keyjoint source*

Table 4 探究了全身边界模型使用不同来源的关键关节轨迹（真实数据 vs 第一阶段合成）对最终运动质量的影响。使用第一阶段合成轨迹时，FID 仅从 0.208（使用真实轨迹）轻微退化至 0.224，验证了第一阶段关键关节合成的准确性，以及第二阶段对合成轨迹的良好兼容性。

---

### 失败模式与局限性

1. **实时性不足**：即使使用 DDIM 加速，最快推理仍需 0.7s，无法满足实时交互应用（如游戏、VR）的毫秒级响应需求。
2. **无在线/自回归能力**：当前框架为离线批处理生成，无法在运动执行过程中动态接收新控制信号并流式生成后续帧。
3. **训练数据分布限制**：对于训练集中未出现的极端运动（如高难度体操动作）或复杂多关节协调模式，生成质量可能出现退化，Figure 6 中部分手动指定的 S 曲线轨迹虽被跟随，但运动自然度有所下降。
4. **隐式控制的计算开销**：依赖反向传播优化扩散潜变量，增加了推理计算量，且对于高度非凸的约束函数可能陷入局部最优，无法保证全局约束满足。
5. **关键关节集合的完备性**：当前集合（双手、双脚、根、头）对日常运动足够，但能否覆盖舞蹈、武术等需要躯干精细控制的运动类型尚待验证。

![[assets/figures/papers/paper_list_l1896_SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control/figures/014_Figure_6.jpg]]
*Figure 6: Qualitative results on manually specified challenging control signals, such as S-curves and straight paths. Our method successfully follows the intended trajectories, demonstrating strong generalization to unseen and difficult motion constraints*

---

### 重要图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| **Table 1** | 0.454% 极端稀疏控制下，SFControl 在 FID（0.224）和 Control Error（0.036m）上全面超越所有基线 |
| **Table 2** | 两阶段分解使目标驱动场景的距目标距离从 0.206m 降至 0.093m，降幅 55% |
| **Table 3** | 弧长对齐机制将时间无关控制的约束误差从 0.4827 降至 0.0256，实现无时间戳轨迹跟随 |
| **Figure 5** | SFControl 在不同控制稀疏度下性能近乎恒定，基线方法随稀疏度增加急剧恶化 |
| **Table 6** | 随机掩码训练使模型对任意关节组合和稀疏度具有高度鲁棒性 |
| **Table 7** | 对分布外噪声控制信号保持鲁棒，Control Error 在 $\sigma=0.1$ 时仍仅 0.056m |
| **Table 9** | DDIM 5 步在 0.7s 内实现接近 DDPM 50 步的性能，FID 仅从 0.224 升至 0.248 |



## 定位与知识库关联

### 1. 核心瓶颈与因果机制

现有可控运动生成方法面临一个根本性瓶颈：**密集时空控制信号与手工指定成本之间的矛盾**。主流方法（如基于 ControlNet 的 **OmniControl** (Xie et al., arXiv 2023)、基于扩散噪声优化的 **DNO**、以及基于潜码优化的 **TLControl**）通常要求用户提供每帧精确的关节轨迹或空间约束，这在实践中极不切实际。与此同时，当控制信号变得稀疏时，在高维全身运动空间（通常 $D \gg 100$）中直接满足这些约束会导致**控制精度与运动自然度难以兼顾**——模型要么过度拟合稀疏信号而丧失运动多样性，要么为保持自然度而牺牲控制精度。

SFControl 的核心因果调节旋钮在于**将控制问题解耦为两个不同维度的子问题**：首先在低维关键关节空间（仅包含末端效应器和根节点，维度 $d \ll D$）中合成满足各类控制约束的轨迹，然后利用强条件生成先验将该轨迹补全为自然全身运动。这一解耦策略的深层洞察是：**人类运动可由少量关键关节的低维运动充分描述**，因此在低维空间中可高效满足各类控制约束（显式、隐式、目标驱动、时间无关），而全身运动补全模型只需学习从关键关节到全身的自然映射，无需同时处理控制约束。

### 2. 方法谱系中的定位

SFControl 在可控运动生成的方法谱系中占据了一个独特位置，其与相关工作的关系可沿以下维度展开：

**控制信号密度维度**：传统方法如 **CondMDI**（基于扩散的运动补间）和 **MotionLCM**（基于潜一致性模型）依赖密集的时空控制信号，要求用户提供完整的轨迹或关键帧序列。SFControl 通过随机掩码训练策略和两阶段解耦，将控制信号密度降至仅 **0.454%** 的关节信号，在极端稀疏条件下仍保持 FID 0.224 和控制误差 0.036m（Table 1）。

**控制信号类型维度**：**OmniControl** 和 **MotionLCM** 主要处理显式空间约束，**DNO** 通过扩散噪声优化支持可微目标函数但直接作用于全身运动空间。SFControl 统一了显式控制（通过掩码注入）、隐式控制（通过扩散潜空间梯度反传）和目标驱动控制（通过修改训练时的掩码策略），且所有控制类型均在低维关键关节空间中处理，避免了高维空间中的优化困难。

**时间对齐需求维度**：几乎所有现有方法（包括 **OmniControl**、**CondMDI**、**DNO**）都要求精确的逐帧时间戳注释。SFControl 通过弧长重参数化和对齐损失（Eq. (1)）首次实现了**时间无关控制**，使得用户只需提供几何路径而无需指定时间节奏，将约束误差从 0.4827（无时间无关机制）降至 0.0256（Table 3）。

**架构范式维度**：SFControl 的两阶段扩散框架与单阶段基线（**Ours w/o decomp.**）形成鲜明对比。消融实验表明，两阶段分解在所有目标驱动场景上将距目标距离从 0.206m 降至 0.093m，脚滑动从 0.057 降至 0.047（Table 2），验证了"先控制后补全"范式的优越性。

### 3. 适用边界与局限

尽管 SFControl 在稀疏和灵活控制方面取得了显著进展，其适用边界和局限性同样明确：

**实时性不足**：当前两阶段扩散框架非实时，DDPM 需要 50 步采样耗时约 7.1 秒；即使使用 DDIM 加速，仍需 0.7–1.4 秒（Table 5, Table 9），难以满足实时交互应用（如游戏、VR）的需求。

**离线批处理范式**：方法采用离线批处理生成模式，未探索自回归或在线采样策略，无法在运动执行过程中动态接收控制信号并实时生成后续帧。这限制了其在交互式场景中的应用。

**数据分布依赖**：运动质量和多样性受限于训练数据分布（HumanML3D）。对于训练集中未出现的极端运动（如体操、舞蹈中的复杂多关节协调）可能存在退化，尽管在分布外（OOD）噪声注入的控制信号下仍表现出一定鲁棒性（Table 7）。

**隐式控制的计算开销**：隐式控制和目标驱动场景依赖反向传播优化，增加了推理计算开销，且较难保证困难约束（如复杂避障）的全局满足。当前实验中的隐式任务（手触头、窄空间行走）相对简单，更复杂的物理约束可能面临挑战。

**关键关节集合的完备性**：当前关键关节集合（双手、双脚、根、头）是否足以描述所有类型的复杂运动（如涉及脊柱、肩部的精细动作）仍是一个开放问题。

### 4. 开放问题与未来方向

基于上述局限，SFControl 开启了以下值得探索的方向：

1. **实时交互式生成**：如何在保证控制精度和运动质量的前提下实现实时或交互式运动生成？可能的路径包括蒸馏为一致性模型、减少扩散步数、或采用流匹配等更高效的生成范式。

2. **流式在线控制**：能否将自回归采样与运动执行相结合，实现流式控制（online control），使用户能够在运动生成过程中动态调整控制目标？

3. **多角色与动态环境交互**：如何将两阶段框架扩展到多角色交互（如双人舞蹈、对抗运动）或与动态环境交互（如移动障碍物）的场景？

4. **关键关节集合的扩展**：对于体操、舞蹈等需要全身精细协调的运动，是否需要扩展关键关节集合（如增加脊柱、肘部、膝盖）？如何自动学习最优的关键关节选择？

5. **更高效的隐式控制优化**：能否通过预测梯度、学习优化器或物理先验来加速隐式控制的推理过程，并提高困难约束的满足率？

6. **跨数据集泛化**：当前仅在 HumanML3D 上验证，如何将框架迁移到其他运动数据集（如 AMASS、LAFAN1）或不同骨架结构，仍需进一步探索。



## 原文 PDF

![[paperPDFs/ICCV_2025/SFControl_Motion_Synthesis_with_Sparse_and_Flexible_Keyjoint_Control.pdf]]
