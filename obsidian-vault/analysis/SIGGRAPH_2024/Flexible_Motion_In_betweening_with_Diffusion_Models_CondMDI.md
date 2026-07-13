---
title: Flexible Motion In-betweening with Diffusion Models (CondMDI)
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/CondMDI_Flexible_Motion_In_betweening_with_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- CCMDB
- FMBDMC
tags:
- SIGGRAPH_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 训练时随机掩码（随机采样关键帧数和关节数）并显式将观测掩码与输入拼接，使模型学会从任意部分观测中补全运动。
primary_logic: 将运动补间统一为掩码条件扩散生成任务：在大量随机关键帧‑关节掩码上训练，模型获得从灵活用户约束中生成高质量、多样化连贯动作的能力。
claims:
- CondMDI 在 5 个随机关键帧条件下关键帧错误仅 0.1789，且 FID 为 0.1731，优于纯 imputation 和 reconstruction guidance 基线。
- 在根关节控制任务上，CondMDI 的 FID（0.2474）显著优于 OmniControl（12.59/9.42），且关键帧错误更低。
- CondMDI 能够从仅根轨迹或仅手腕关节的部分关键帧生成自然的下半身运动，并响应文本提示改变动作风格。
- HumanML3D (text‑to‑motion) 上 FID = 0.2538
---

# Flexible Motion In-betweening with Diffusion Models (CondMDI)

> [!tip] 核心洞察
> 将运动补间统一为掩码条件扩散生成任务：在大量随机关键帧‑关节掩码上训练，模型获得从灵活用户约束中生成高质量、多样化连贯动作的能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 灵活的动作补间：基于扩散模型的条件运动扩散补间 (CondMDI) |
| 英文题名 | Flexible Motion In-betweening with Diffusion Models (CondMDI) |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2405.11126) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | CondMDI (Conditional Motion Diffusion In-betweening) |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D (text‑to‑motion) 上，FID 0.2538 vs GMD (0.235) / MDM (0.556) (+0.0188 vs GMD, -0.3022 vs MDM)；R‑precision Top‑3 0.6450 vs GMD (0.652) / MDM (0.608) (-0.007 vs GMD, +0.037 vs MDM)。
> - HumanML3D (5 random keyframes) 上，Keyframe error 0.1789 vs IMP+RecG (0.0034) / Imputation (0.4254) (worse than guided, far better than pure imp.)；FID 0.1731 vs IMP (4.6791), IMP+RecG (1.7072) (-1.5341 vs guided, -4.506 vs pure imp.)。
> - HumanML3D (root joint control) 上，FID 0.2474 vs OmniControl (12.59 / 9.42) / MDM imp. (3.93) (-12.34 vs OmniControl)。

## 概要

运动补间（motion in-betweening）是计算机动画中的关键任务，旨在根据稀疏的关键帧约束生成连贯的中间运动。现有方法普遍受限于**固定的关键帧模式**，难以处理时空稀疏的部分关键帧约束——例如仅给定根关节轨迹或仅约束手腕位置——且推理时条件方法在运动质量和多样性之间存在显著权衡。

本文提出 **CondMDI（Conditional Motion Diffusion In-betweening）**，将运动补间统一为掩码条件扩散生成任务。其核心洞察是：**在训练时对关键帧数量和关节维度进行大规模随机掩码采样，使扩散模型学会从任意部分观测中补全运动**，从而在推理时灵活响应各类稀疏约束，同时保持生成质量。具体而言，CondMDI 将掩码后的带噪样本与观测掩码直接拼接馈入扩散模型，无需独立的编码模块或推理时的梯度引导。

在 HumanML3D 基准上的实验表明：
- **无条件文本‑动作生成**：CondMDI 的 FID 达到 0.2538，与骨干模型 **GMD**（Karunratanakul et al., 2023）的 0.235 接近，显著优于 **MDM**（Tevet et al., ICLR 2023）的 0.556（Table 1）。
- **灵活关键帧补间**：在 5 个随机关键帧条件下，CondMDI 的关键帧错误仅为 0.1789，FID 低至 0.1731，在运动质量上大幅优于纯 imputation（FID 4.6791）和 reconstruction guidance（FID 1.7072）（Table 2, Table 4）。
- **根关节控制**：CondMDI 的 FID 为 0.2474，远优于 **OmniControl**（Xie et al., 2023）的 12.59/9.42，且关键帧错误降低约一个数量级（Table 3）。

定性实验进一步验证了方法的灵活性：CondMDI 能够从仅根轨迹或仅手腕关节的部分关键帧生成自然的下半身运动，并响应文本提示改变动作风格（Figure 4, Figure 7），同时支持同一关键帧约束下生成多样化动作（Figure 6）。

### 动作补间的核心挑战

动作补间（motion in-betweening）是计算机动画与角色控制中的基础任务：给定稀疏的关键帧约束，生成连贯、自然且符合物理规律的中间运动序列。传统动画制作中，动画师通常仅设定少数关键姿态，其余帧由插值或数据驱动方法自动填充。然而，这一看似简单的任务在现实中面临双重挑战。

**质量与多样性的矛盾。** 早期基于样条插值或运动匹配的方法能够严格满足关键帧约束，但生成的中间运动往往缺乏自然度和表现力，尤其在处理复杂的全身协调动作（如空手道踢腿、瑜伽拜日式）时，容易产生不自然的滑步、关节抖动或运动学不可行的姿态。近年来，深度生成模型——特别是扩散模型——在无条件文本到动作生成上取得了显著进展，展现出强大的运动先验学习能力。然而，将此类模型直接用于条件补间时，如何在精确满足用户指定的稀疏约束的同时，保持生成样本的多样性和运动质量，仍是一个悬而未决的问题。

**关键帧模式的灵活性需求。** 实际动画制作中的关键帧约束远非单一模式：动画师可能仅指定根关节轨迹而让模型自主生成上半身动作，也可能仅约束手腕位置来驱动全身交互运动，甚至在同一序列中混合不同关节在不同时间点的部分观测。现有运动补间方法大多假设**固定的关键帧模式**——要么要求所有关节在关键帧处均被指定，要么依赖推理时的插值或引导策略来事后施加约束。这些方法在面对**时空稀疏的部分关键帧**（spatio-temporally sparse keyframes）时，往往面临两难困境：纯推理时插值方法（如扩散模型的掩码替换）虽能严格匹配观测，但生成质量急剧下降，表现为严重的脚滑和运动不自然；而基于梯度的重建引导方法虽能降低关键帧偏差，却以牺牲运动多样性和引入高频抖动为代价。

### 现有方法的瓶颈

从方法谱系来看，当前的运动补间方案可归为两条技术路线，二者各自存在结构性局限：

**推理时条件方法（inference-time conditioning）。** 这类方法以预训练的无条件或文本条件扩散模型为骨干，在采样过程中通过掩码替换（imputation）或重建损失梯度引导（reconstruction guidance）来注入关键帧约束。掩码替换在每一步扩散中将观测部分强制写回带噪样本，但模型从未在训练中见过此类部分观测模式，导致去噪过程与掩码操作之间产生分布偏移，最终生成的运动缺乏全局一致性。重建引导通过梯度下降优化未观测部分以匹配观测，能在一定程度上改善关键帧匹配精度，但其逐步优化的计算开销大，且引导强度与运动质量之间存在固有的权衡——强引导导致抖动和过拟合，弱引导则无法有效约束。

**训练时条件方法（training-time conditioning）。** 以 OmniControl（Xie et al., 2023）为代表的方法在训练阶段引入空间控制信号，使模型学习从部分关节约束中生成运动。然而，这类方法通常将控制模块设计为独立的编码分支，与主生成模型松耦合，且训练时的关键帧采样策略未充分覆盖实际使用中可能出现的灵活组合（如仅根关节、仅手腕、随机帧数+随机关节数的混合模式）。这导致模型在面对训练分布之外的约束组合时泛化能力不足——例如，在仅根关节控制任务上，OmniControl 的 FID 高达 12.59，远逊于无条件生成基线，表明其空间控制能力以显著牺牲整体运动质量为代价。

### 本文动机与核心思路

上述分析揭示了一个关键洞察：**运动补间本质上是一个掩码条件生成问题**——给定任意部分观测（关键帧约束），模型应能从学到的运动先验中补全缺失部分。这一视角将灵活的关键帧模式统一为对运动序列的时空掩码操作，从而将问题转化为：如何训练一个扩散模型，使其在推理时能够泛化到任意掩码模式？

CondMDI 的核心动机正是弥合训练与推理之间的条件分布鸿沟。其关键设计在于**训练时随机掩码策略**：在每次训练迭代中，不仅随机采样关键帧的数量和位置，还随机选择被约束的关节子集，并将二值观测掩码显式地与带噪运动序列拼接后馈入扩散模型。这一策略使模型在训练阶段就暴露于海量的、多样化的部分观测场景中，从而学会从任意掩码模式中推断完整运动——无需推理时的额外优化或引导，也无需针对特定约束模式重新训练。

简言之，CondMDI 将动作补间从一个“事后施加约束”的推理问题，转化为一个“从部分观测中重建完整运动”的统一生成建模问题。这一范式转换使得单个模型能够同时处理稀疏关键帧补间、根轨迹驱动、部分关节约束以及文本引导的风格控制等多种任务，且在各场景下均保持与无条件生成相当甚至更优的运动质量。

## 核心方法与创新机理

CondMDI 的核心创新在于将运动补间（motion in-betweening）重新定义为一个**掩码条件扩散生成任务**，从而一举突破了现有方法的两个关键瓶颈：一是对固定关键帧模式的依赖，二是推理时条件方法在运动质量和多样性上的不足。

传统运动补间方法通常假设关键帧在时间上均匀分布且所有关节均被观测，或依赖推理时的插值（imputation）与重建引导（reconstruction guidance）来施加空间约束。这些方法在面对**时空稀疏的部分关键帧**（例如仅给定根轨迹或仅手腕关节）时，往往产生严重的脚滑、抖动或运动不自然（Figure 5）。CondMDI 的因果调控旋钮在于**训练策略的根本性转变**——不再将条件信号视为推理时的后处理，而是在训练过程中显式地建模条件反向扩散后验 $p_{\theta}(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{p}, \mathbf{c})$。

这一转变通过三个紧密耦合的 **changed slots** 实现：

1. **关键帧训练策略**：训练时从所有可能的补间场景中随机采样关键帧数量和关节数量，而非使用固定模式。模型因此学会从任意部分观测中补全运动，获得了对灵活用户约束的泛化能力（Algorithm 1, Section 4.3）。

2. **条件输入结构**：将掩码后的带噪样本 $\tilde{\mathbf{x}}_t = \mathbf{m} \odot \mathbf{c} + (1-\mathbf{m}) \odot \mathbf{x}_t$ 与二值观测掩码 $\mathbf{m}$ 沿特征维度拼接后，直接馈入主扩散模型（Figure 2, Section 4.3）。这种简洁的设计使模型无需额外的条件编码模块，即可感知哪些时空位置被观测。

3. **根表示**：将根关节表示从相对前一帧的位移和旋转改为全局绝对位移和旋转（Section 4.2, Appendix B），使关键帧定义更直观，且经实验验证对生成质量无负面影响（Appendix E）。

消融实验为这一创新提供了决定性证据（Table 4）：在 5 个随机关键帧条件下，CondMDI 的 FID 为 0.1731，远优于纯 imputation（4.6791）和重建引导（1.7072）；同时关键帧错误仅 0.1789，在保持极低约束误差的前提下实现了与无条件生成持平甚至更优的运动质量。相比之下，推理时方法（imputation + reconstruction guidance）虽能降低关键帧错误至 0.0034，但 FID 飙升至 1.7072，且引入明显抖动（Figure 5），暴露了条件精度与运动自然度之间的根本权衡——而 CondMDI 通过训练时随机掩码成功解耦了这一冲突。

值得注意的是，CondMDI 并非对骨干模型架构的颠覆性改造，而是对**训练范式**的重新设计。其骨干网络直接沿用 GMD（Karunratanakul et al., 2023）的 UNet 架构，真正的突破在于将“从任意部分观测中补全运动”的能力内化到模型参数中，而非依赖推理时的梯度引导或替换操作。这一设计哲学使 CondMDI 在根关节控制任务上，以 FID 0.2474 显著优于专门的关节控制方法 OmniControl（12.59/9.42），同时关键帧错误降低近一个数量级（Table 3）。

CondMDI 将灵活的动作补间统一为一个掩码条件扩散生成任务。其核心思想是：在训练时通过随机掩码（随机采样关键帧数量和关节数量）让模型学会从任意部分观测中补全完整运动，从而在推理时能够接受时空稀疏的部分关键帧约束，生成高质量、多样化的连贯动作。

### Pipeline 总览

整个框架的推理流程如图 Figure 2 所示，由以下模块串联构成：

![[assets/figures/papers/CondMDI_Flexible_Motion_In-betweening_with_Diffusion_Models_cfe713ed727d/figures/002_Figure_2.jpg]]
*Figure 2: Conditional Motion Diffusion In-betweening (CondMDI) overview. The model is fed a noisy motion sequence*

1. **CLIP 文本编码器**  
   将文本提示 `p` 编码为条件嵌入，注入扩散模型以控制动作语义风格。

2. **Mask Extractor**  
   根据用户给定的关键帧控制信号 `c`，生成一个二值观测掩码 `m`。掩码 `m` 的维度与运动序列 `x_t` 对齐，指示哪些帧的哪些关节被观测到。

3. **Masked Sum**  
   执行带掩码的加法操作，将观测关键帧“写入”带噪样本的对应位置：
   $$
   \tilde{\mathbf{x}}_t = \mathbf{m} \odot \mathbf{c} + (1 - \mathbf{m}) \odot \mathbf{x}_t
   $$
   其中 $\odot$ 表示逐元素乘法。这一操作确保模型在已知位置上获得精确约束，而在未知位置上保留扩散采样的灵活性。

4. **UNet 扩散模型（基于 GMD 骨干）**  
   接收拼接后的输入 $[\tilde{\mathbf{x}}_t, \mathbf{m}]$ 以及文本嵌入，预测干净样本 $\hat{\mathbf{x}}_0$。模型基于 **GMD**（Karunratanakul et al., 2023）的二阶段 UNet 架构，采用 AdaGN 归一化和样本估计参数化，扩散步数 $T = 1000$。与 GMD 的关键区别在于：(a) 根关节表示从相对坐标改为全局绝对坐标，使关键帧定义更直观；(b) 输入通道扩展以容纳观测掩码的拼接。

5. **分类器自由引导（Classifier-Free Guidance）**  
   在采样时混合条件预测与无条件预测：
   $$
   G_\theta(\mathbf{x}_t, t, \mathbf{p}) = G_\theta(\mathbf{x}_t, t, \emptyset) + w \left( G_\theta(\mathbf{x}_t, t, \mathbf{p}) - G_\theta(\mathbf{x}_t, t, \emptyset) \right)
   $$
   其中 $w$ 为引导强度，控制文本对齐程度。

### 训练策略

CondMDI 的核心创新在于训练时的随机掩码策略（见 Algorithm 1）：

- **随机关键帧采样**：从完整运动序列中随机采样 $K$ 帧作为关键帧，$K$ 本身也随机变化。
- **随机关节采样**：对每个选中的关键帧，进一步随机选择部分关节作为观测，而非总是使用完整帧的所有关节。
- **掩码拼接**：将掩码后的带噪样本 $\tilde{\mathbf{x}}_t$ 与观测掩码 $\mathbf{m}$ 沿通道维度拼接后直接馈入 UNet，使模型显式感知哪些位置是观测约束。

这种训练方式使模型覆盖了“所有可能的运动补间场景”，从而在推理时无需任何微调即可处理任意组合的关键帧约束——无论是稀疏的全身关键帧、仅根关节轨迹，还是仅手腕关节的部分观测。

### 与推理时方法的对比

CondMDI 与两类推理时条件方法形成鲜明对比：

- **纯 Imputation**：在采样每一步用观测关键帧替换对应位置，但模型训练时未见过掩码，导致运动不自然和严重脚滑（Table 4 中 FID 高达 4.6791）。
- **Reconstruction Guidance**：通过观测部分的 MSE 梯度引导未观测部分更新，能降低关键帧错误但引入抖动并损害 FID（Table 4 中 FID 为 1.7072）。

CondMDI 通过训练时显式建模条件后验 $p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{p}, \mathbf{c})$，在保持极低关键帧错误（0.1789）的同时，FID（0.1731）与无条件生成持平甚至更优，证明了训练时随机掩码是兼顾约束精度与运动质量的关键设计。

### 补充图表

CondMDI 将灵活的动作补间统一为掩码条件扩散生成任务。其核心架构基于 **GMD** (Karunratanakul et al., 2023) 的二阶段 UNet 扩散骨干，并在输入层和训练策略上进行了三项关键改造：根表示全局化、随机掩码训练、以及观测掩码拼接输入。

### 运动表示与根坐标全局化

每帧动作表示为 263 维特征向量，由全局根运动与局部姿态拼接而成：

$$
\mathbf{x}_t = (\mathbf{x}_t^{\mathrm{global}}, \mathbf{x}_t^{\mathrm{local}}) \in \mathbb{R}^{263}
$$

其中 $\mathbf{x}_t^{\mathrm{global}}$ 包含根关节的全局绝对位移和旋转，$\mathbf{x}_t^{\mathrm{local}}$ 包含其余关节相对于根关节的局部姿态参数。与 GMD 原版采用的“相对前一帧”根表示不同，CondMDI 将根轨迹改为全局坐标表示。这一改动使得关键帧约束的定义更为直观（用户无需关心帧间相对关系），且消融实验表明对生成质量无负面影响（Appendix B, E）。

### 扩散过程基础

CondMDI 沿用 DDPM 的扩散框架。前向过程逐步向干净样本 $\mathbf{x}_0$ 添加高斯噪声：

$$
q(\mathbf{x}_t | \mathbf{x}_{t-1}) := \mathcal{N}(\mathbf{x}_t; \sqrt{1 - \beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I})
$$

其中 $\beta_t$ 为方差调度参数。反向过程学习从噪声中恢复干净样本，以文本提示 $\mathbf{p}$ 为条件：

$$
p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{p}) := \mathcal{N}(\mathbf{x}_{t-1}; \boldsymbol{\mu}_\theta(\mathbf{x}_t, t, \mathbf{p}), \Sigma_t)
$$

模型实际预测干净样本 $\hat{\mathbf{x}}_0 = G_\theta(\mathbf{x}_t, t, \mathbf{p})$，训练目标为均方误差：

$$
\mathcal{L} := \mathbb{E}_{(\mathbf{x}_0,\mathbf{p}), t} \left[ \| \mathbf{x}_0 - G_\theta(\mathbf{x}_t, t, \mathbf{p}) \|^2 \right]
$$

### 条件反向扩散：从 $p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t,\mathbf{p})$ 到 $p_\theta(\mathbf{x}_{t-1}|\mathbf{x}_t,\mathbf{p},\mathbf{c})$

CondMDI 的核心创新在于将关键帧控制信号 $\mathbf{c}$ 显式引入反向扩散。其条件反向后验为：

$$
p_\theta(\mathbf{x}_{t-1} | \mathbf{x}_t, \mathbf{p}, \mathbf{c})
$$

实现这一条件化的关键操作是**掩码求和**（Masked Sum）。首先，Mask Extractor 模块根据控制信号 $\mathbf{c}$ 生成二值观测掩码 $\mathbf{m}$，指示哪些帧的哪些关节维度被用户指定。随后，将带噪样本中被观测部分的特征替换为 $\mathbf{c}$ 的对应值：

$$
\tilde{\mathbf{x}}_t = \mathbf{m} \odot \mathbf{c} + (1 - \mathbf{m}) \odot \mathbf{x}_t
$$

最后，将替换后的样本 $\tilde{\mathbf{x}}_t$ 与观测掩码 $\mathbf{m}$ 沿通道维拼接，共同馈入 UNet 扩散模型。这一设计使模型能够明确感知哪些特征来自用户约束、哪些需要生成补全，从而学会从任意部分观测中推断完整运动。

### 训练策略：随机掩码采样

CondMDI 的训练策略是使其获得灵活补间能力的关键因果机制（Algorithm 1）。每次训练迭代中，从完整运动序列中随机采样：

- **关键帧数量**：从 1 到序列总帧数之间随机选取
- **关键帧位置**：在时间轴上随机分布
- **被观测关节**：随机选取部分关节维度进行掩码

这种“在全部可能补间场景的空间中采样”的策略，迫使模型学习从任意时空稀疏约束中恢复完整运动，而非适应某一固定关键帧模式。消融实验证实，仅训练随机全帧（random frames）的模型在部分关节条件下无法泛化（Table 4）。

### 分类器自由引导

采样时，CondMDI 使用分类器自由引导（Classifier-Free Guidance）控制文本对齐强度。训练时以一定概率将文本提示 $\mathbf{p}$ 置为空集 $\emptyset$，使模型同时学习条件与无条件生成。推理时混合两者预测：

$$
G_\theta(\mathbf{x}_t, t, \mathbf{p}) = G_\theta(\mathbf{x}_t, t, \emptyset) + w \left( G_\theta(\mathbf{x}_t, t, \mathbf{p}) - G_\theta(\mathbf{x}_t, t, \emptyset) \right)
$$

其中 $w$ 为引导权重，控制生成动作与文本描述的对齐程度。

### 与推理时条件方法的对比

CondMDI 的显式条件建模与两类推理时基线形成对照：

- **纯 Imputation**：每步将观测部分替换为 $\mathbf{c}$，但模型未在训练中见过掩码分布，导致严重脚滑和运动不自然（Table 4, Figure 5）。
- **重建引导（Reconstruction Guidance）**：利用观测部分的 MSE 梯度引导未观测部分更新：

$$
\hat{\mathbf{x}}_{0,t}^{\mathsf{p}} = \hat{\mathbf{x}}_{0,t}^{\mathsf{p}} - \frac{w_r \sqrt{\bar{\alpha}_t}}{2} \nabla_{\mathbf{x}_t^{p}} \| \mathbf{c} - \hat{\mathbf{x}}_{0,t}^{0} \|^2
$$

该方法能降低关键帧误差，但会引入运动抖动并显著恶化 FID（Table 4：IMP+RecG 的 FID 为 1.7072，而 CondMDI 为 0.1731）。

### 文本编码模块

文本提示 $\mathbf{p}$ 通过预训练的 CLIP 文本编码器转换为条件嵌入，随后注入 UNet 的 AdaGN 归一化层。该模块沿用 GMD 的设计，CondMDI 未做修改。

## 实验与关键发现

### 无条件文本-动作生成能力验证

CondMDI 首先在标准文本-动作生成任务上验证了其骨干网络的生成能力。如 **Table 1** 所示，CondMDI 在 HumanML3D 测试集上取得了 FID 0.2538、R-precision Top-3 0.6450 和 Diversity 9.7489 的成绩。与骨干模型 **GMD**（Karunratanakul et al., 2023）相比，FID 仅轻微上升 0.0188，R-precision 下降 0.007，表明将根表示从相对坐标改为全局绝对坐标（见 **Section 4.2**）对生成质量无实质负面影响。与 **MDM**（Tevet et al., ICLR 2023）相比，CondMDI 的 FID 降低了 0.3022，R-precision 提升了 0.037，验证了基于 UNet 的骨干在无条件生成上的竞争力。

![[assets/figures/papers/CondMDI_Flexible_Motion_In-betweening_with_Diffusion_Models_cfe713ed727d/figures/003_Table_1.jpg]]
*Table 1: Text-to-motion evaluation on the HumanML3D test set*

### 灵活关键帧补间：核心定量结果

**Table 2** 展示了 CondMDI 在不同关键帧配置下的核心性能。在 5 个随机关键帧（K=5）条件下，CondMDI 取得 FID 0.1731、关键帧错误 0.1789 和 Foot skating ratio 0.0957。这一结果揭示了方法的一个关键特性：**条件生成的质量（FID）甚至优于无条件生成（0.2538）**，说明关键帧约束不仅未损害运动自然度，反而通过提供空间锚点帮助模型缩小了生成空间。

随着关键帧数量从 K=1 增加到 K=20，关键帧错误从 0.3739 单调下降至 0.0680，FID 从 0.1551 变化至 0.1956，始终保持在较低水平。这表明 CondMDI 能够有效利用从极稀疏到较密集的不同约束强度。

在部分关节条件场景下，CondMDI 同样表现稳健：
- **仅根关节轨迹条件**：FID 0.2474，关键帧错误 0.0525，Foot skating ratio 0.1030
- **VR 关节条件**（头部+双手腕）：FID 0.2296，关键帧错误 0.1156

### 与推理时条件方法的消融对比

**Table 4** 的消融实验系统对比了 CondMDI 与两种推理时条件基线（均使用相同 GMD 预训练骨干，K=5 随机关键帧）：

| 方法 | FID ↓ | 关键帧错误 ↓ | R-precision Top-3 ↑ |
|------|-------|-------------|-------------------|
| 纯 Imputation (IMP) | 4.6791 | 0.4254 | 0.4434 |
| Imputation + 重建引导 (RecG, w_r=20) | 1.7072 | **0.0034** | 0.5538 |
| **CondMDI（本方法）** | **0.1731** | 0.1789 | **0.6647** |

这三种方法呈现出清晰的“质量-约束精度”权衡：
- **纯 imputation** 在每一步用观测值替换对应位置（C=0），虽能保持关键帧约束，但导致 FID 恶化至 4.6791，运动严重不自然。**Figure 5** 的定性结果显示该方法在 S 形行走轨迹上完全无法跟随关键帧。
- **重建引导** 通过梯度优化将关键帧错误压至极低的 0.0034，但代价是 FID 升至 1.7072，且 **Figure 5** 显示生成动作出现明显抖动和不连贯——这是引导方法在扩散采样后期引入高频梯度的典型失败模式。
- **CondMDI** 的关键帧错误（0.1789）虽高于引导方法，但 FID（0.1731）比引导方法低 1.5341，R-precision（0.6647）甚至优于无条件生成。这说明 **训练时随机掩码策略使模型学会了在保持运动自然度的前提下“合理接近”约束，而非机械地精确匹配**。

### 消融：随机帧+关节采样的必要性

**Table 4** 还对比了 CondMDI 与仅训练随机全帧关键帧的变体（random frames）。在部分关节条件（如仅根关节或仅手腕）下，仅训练全帧的模型无法泛化，因为它在训练中从未见过“部分关节被观测”的模式。CondMDI 通过在训练时同时随机采样关键帧数量和关节数量，使模型学会了从任意稀疏观测中补全运动，这是方法能够处理灵活约束的核心机制。

### 与专用空间控制方法的对比

**Table 3** 在根关节控制任务上将 CondMDI 与 **OmniControl**（Xie et al., 2023）和 MDM imputation 基线进行对比。CondMDI 的 FID 为 0.2474，而 OmniControl（全关节训练）的 FID 高达 12.59，即使仅在根关节上训练的 OmniControl 也达 9.42。CondMDI 的关键帧错误为 0.0525，远低于 OmniControl 的 0.446/0.308。这一显著差距揭示了专用空间控制方法在仅给定单一关节轨迹时面临的泛化困难，而 CondMDI 的掩码训练策略天然支持此类部分观测。

### 多样性分析

**Table 2** 的 Diversity 指标显示，CondMDI 在不同关键帧配置下的多样性（9.58-9.83）与无条件生成（9.75）基本持平，未因约束而坍缩。**Figure 6** 定性展示了同一组关键帧约束下生成的多个运动序列，在最后一个关键帧之后呈现出多样且时间连贯的行为，验证了方法在保持约束的同时保留了扩散模型的随机生成能力。

### 文本条件与空间约束的协同

**Figure 7** 展示了 CondMDI 在仅根轨迹约束下，通过不同文本提示（“a person is waving their hands above their head” vs “a person tosses a ball”）生成不同上半身动作的能力。这表明文本条件与空间约束在 CondMDI 框架中可协同工作：根轨迹定义全局位移，文本控制局部姿态风格。

### 推理效率

**Table 6** 报告了推理时间对比。CondMDI 在单张 RTX 2070 上的推理时间与 GMD 骨干相当（均为约 1.2 秒/序列，1000 步 DDPM 采样），因为条件机制仅增加了掩码拼接操作，未引入额外网络模块或优化循环。相比之下，重建引导方法因每步需计算梯度，推理时间显著增加。

### 已知失败模式

尽管整体表现优异，CondMDI 在以下场景仍存在局限：
1. **高度动态动作的脚滑与抖动**：在关键帧极为稀疏时（如 K=1），Foot skating ratio 为 0.0936，高于无条件生成的 0.0869（**Table 2**），说明模型在缺乏足够空间约束时难以保证物理合理性。
2. **根关节依赖**：当前运动表示要求根关节必须包含在观测中，因为全局轨迹与局部姿态在特征向量中耦合（263 维，见 **Eq. (7)**）。这限制了仅给定末端效应器（如手腕）而完全不提供根信息的应用场景。
3. **随机采样与动画实践的对齐**：训练时的均匀随机采样未针对动画师实际使用的典型关键帧组合进行优化，可能导致某些实用配置下的性能未达最优。

![[assets/figures/papers/CondMDI_Flexible_Motion_In-betweening_with_Diffusion_Models_cfe713ed727d/figures/004_Table_2.jpg]]
*Table 2: Quantitative results for different keyframes on the HumanML3D test set. ?? ∈ {1, 5, 20} means number of keyframes randomly placed along the motion trajectory. Root Joint and VR Joints mean conditioning on the root joint trajectory and the head and both wrist joints repectively*

### 补充图表

![[assets/figures/papers/CondMDI_Flexible_Motion_In-betweening_with_Diffusion_Models_cfe713ed727d/figures/008_Table_3.jpg]]
*Table 3: Quantitative results for root-joint control on the HumanML3D test set. OmniControl (on all) means the model is trained on all joints*

![[assets/figures/papers/CondMDI_Flexible_Motion_In-betweening_with_Diffusion_Models_cfe713ed727d/figures/007_Table_4.jpg]]
*Table 4: Ablation results on the HumanML3D test set. All methods are conditioned on ?? = 5 keyframes randomly sampled from the ground truth motion trajectories with the same text prompts in the test set. IMP means pure imputation when replacement stops at diffusion step 1. C=0 refers to pure imputation with replacement at every diffusion step. RecG refers to reconstruction guidance with the default guidance weight*

![[assets/figures/papers/CondMDI_Flexible_Motion_In-betweening_with_Diffusion_Models_cfe713ed727d/figures/011_Table_6.jpg]]
*Table 6: Inference time*

## 定位与知识库关联

### 1. 与运动生成基线的谱系关系

CondMDI 的方法设计根植于文本条件运动扩散模型的发展脉络，其核心贡献在于将运动补间任务统一为掩码条件扩散生成框架，从而填补了“灵活关键帧约束下的高质量运动生成”这一空白。

**骨干模型选择：GMD 而非 MDM。** 与多数推理时条件方法（如 imputation、reconstruction guidance）通常以 **MDM** (Tevet et al., ICLR 2023) 为骨干不同，CondMDI 选择 **GMD** (Karunratanakul et al., 2023) 作为基础扩散模型。GMD 采用 UNet 架构配合 AdaGN 归一化，并使用样本估计参数化（即直接预测干净样本 $\hat{\mathbf{x}}_0$）和 1000 步扩散过程。这一选择使得 CondMDI 在无条件文本-动作生成上即已具备竞争力：在 HumanML3D 测试集上，CondMDI 的 FID 为 0.2538，仅略逊于 GMD 的 0.235，而显著优于 MDM 的 0.556（Table 1）。这表明 GMD 骨干为后续的条件训练提供了更优的生成先验。

**与文本-动作扩散模型的关系。** 在无条件生成维度，CondMDI 与 **T2M** (Guo et al., 2022)、**MotionDiffuse** (Zhang et al., 2022)、**MLD** (Chen et al., 2023) 等文本-动作生成方法共享评估基准（HumanML3D），但其设计目标并非在无条件生成上取得最优，而是为条件补间提供统一的生成底座。Table 1 的对比验证了 CondMDI 在引入条件机制后并未牺牲无条件生成质量，这是后续灵活条件能力的前提。

### 2. 与条件运动生成方法的对比

现有条件运动生成方法可大致分为两类：训练时显式条件建模，与推理时条件施加。CondMDI 属于前者，但其训练策略的灵活性使其区别于所有现有工作。

**与显式条件模型的对比。** **OmniControl** (Xie et al., 2023) 是支持多关节空间控制的代表性扩散模型，但其训练时需指定受控关节集合。在根关节控制任务上，CondMDI 的 FID 为 0.2474，而 OmniControl 在“所有关节训练”和“仅根关节训练”两种设置下分别为 12.59 和 9.42；关键帧错误方面，CondMDI 为 0.0525，OmniControl 为 0.446/0.308（Table 3）。这一巨大差距源于 OmniControl 的训练-推理条件模式不匹配：当推理时仅给定根关节而模型训练时见过所有关节，其条件机制无法有效泛化。CondMDI 通过训练时随机掩码策略解决了这一泛化瓶颈。

**与推理时条件方法的对比。** 推理时 imputation（掩码替换）和 reconstruction guidance（基于重建损失的梯度引导）是施加空间约束的通用手段。在 K=5 随机关键帧条件下，纯 imputation（C=0，每步替换）的 FID 高达 4.6791，且产生严重脚滑和不自然运动；加入 reconstruction guidance（RecG, $w_r=20$）可将关键帧错误降至 0.0034，但 FID 仍为 1.7072，并引入运动抖动（Table 4, Figure 5）。CondMDI 在关键帧错误 0.1789 的同时，FID 低至 0.1731，实现了约束精度与运动质量的最佳折衷。这证明训练时随机掩码使模型学会了从部分观测中“自然补全”，而非推理时强制拟合。

### 3. 适用边界与限制

CondMDI 的灵活性建立在以下前提之上，这些前提同时也划定了其适用边界：

**根关节的必要性。** 当前模型依赖每帧 263 维的完整特征表示，其中包含全局根运动（绝对位移和旋转）。当部分关键帧不包含根关节观测时，全局-局部表示的耦合使得条件机制无法正常工作。这是一个根本性的表示层面限制，而非训练策略问题。论文将此列为开放问题：如何将框架扩展到不包含根关节观测的部分关键帧场景。

**动态动作的物理合理性。** 尽管 CondMDI 在脚滑比率（Foot skating ratio）上表现良好（K=5 时为 0.0936，Table 2），但在高度动态动作中仍可能出现脚滑和运动抖动，尤其在关键帧极为稀疏时。这与 **PhysDiff** (Yuan et al., 2023) 等物理引导扩散方法形成对比——后者通过物理先验显式约束运动合理性。未来工作可探索将物理先验或接触约束融入 CondMDI 框架。

**训练采样的统计对齐。** CondMDI 的训练策略是从所有可能的关键帧-关节组合中均匀随机采样。这一策略保证了泛化性，但未针对动画师实际使用的典型关键帧组合进行显式对齐。例如，动画制作中更常见的是在动作转折点设置关键帧，而非完全随机放置。这种分布偏移可能导致在特定实际工作流中的表现不及预期。

### 4. 局限与开放问题

**推理效率。** CondMDI 继承 GMD 的 1000 步扩散过程，推理时间相对较长（Table 6 提供了推理速度对比，具体数值需查阅原文）。能否将 CondMDI 与更轻量的扩散采样策略（如 DDIM 加速、蒸馏方法）结合，在保持灵活性的同时大幅降低推理时间，是一个重要的工程化问题。

**特征维度的不均匀表示。** 部分关键帧条件下，观测掩码 $\mathbf{m}$ 的稀疏模式可能导致某些关节信息严重不足。例如，仅观测手腕关节时，下半身运动的生成完全依赖模型先验。当前方法未对不同关节的信息重要性进行显式建模，这可能导致特定条件组合下的生成质量下降。

**框架的可迁移性。** CondMDI 的掩码条件训练范式本质上是一种通用的部分观测生成框架。其核心思想——训练时随机掩码、推理时灵活条件——是否可以迁移到其他需要灵活空间约束的生成任务（如人物-物体交互、多人场景、甚至非运动领域），是一个值得探索的方向。

**与物理先验的结合。** 如第 3 点所述，引入物理先验或接触约束以进一步减少动态动作的脚滑和抖动，是提升运动物理合理性的直接路径。这可以通过在训练损失中加入物理正则项，或在采样过程中引入物理引导来实现。

### 5. 知识库定位

CondMDI 在运动生成知识谱系中的定位可概括为：

| 维度 | 定位 |
|------|------|
| **任务类型** | 灵活关键帧约束下的运动补间（motion in-betweening） |
| **方法范式** | 训练时显式条件扩散模型（explicit conditional diffusion） |
| **核心机制** | 随机掩码训练 + 观测掩码拼接输入 |
| **骨干架构** | GMD UNet（样本估计参数化，1000 步 DDPM） |
| **条件信号** | 文本提示 + 时空稀疏关键帧（任意帧数、任意关节组合） |
| **表示空间** | 全局根运动 + 局部姿势（每帧 263 维） |
| **评估基准** | HumanML3D 测试集，标准协议（Guo et al., 2022） |
| **与基线的关系** | 在无条件生成上与 GMD 持平；在条件补间上显著超越 OmniControl 和推理时方法 |
| **主要局限** | 依赖根关节观测、动态动作物理合理性、推理效率 |
| **开放方向** | 无根关节条件、物理先验融合、轻量采样、框架迁移 |

CondMDI 的核心价值在于证明了一条简单而有效的路径：通过训练时充分探索条件空间（随机掩码），可以使单一模型在推理时泛化到任意部分观测条件。这一洞察超越了运动补间任务本身，对更广泛的 conditional generation 研究具有启发意义。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/CondMDI_Flexible_Motion_In_betweening_with_Diffusion_Models.pdf]]
