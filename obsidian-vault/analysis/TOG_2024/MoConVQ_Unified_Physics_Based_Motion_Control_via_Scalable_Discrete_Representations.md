---
title: "MoConVQ: Unified Physics-Based Motion Control via Scalable Discrete Representations"
type: paper
paper_level: A
venue: TOG
year: 2024
pdf_ref: paperPDFs/TOG_2024/MoConVQ_Unified_Physics_Based_Motion_Control_via_Scalable_Discrete_Representations.pdf
project_link: null
code_link: null
aliases:
- MoConVQ
tags:
- TOG_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "引入离散向量量化（VQ）作为运动表示，配合残差VQ架构提升模型容量，并采用基于模型的强化学习框架高效处理大规模数据，统一了下游任务的接口（编码-解码或纯解码），从而解决了可扩展性和易用性瓶颈。"
primary_logic: "通过离散向量量化运动编码，可以利用VQ-VAE的紧凑性和鲁棒性来捕捉多样化运动技能，而基于模型的RL方法使大型生成式神经网络能够高效地在大规模运动数据上训练，从而实现统一的物理角色运动控制框架。"
claims:
- "MoConVQ使用VQ-VAE学习离散运动表示，能够在超过20小时的运动数据集上训练。"
- "基于模型的RL方法通过联合训练世界模型，将物理模拟变为可微过程，从而高效训练大规模神经网络。"
- "向量量化对运动数据中的噪声具有极强的鲁棒性，连续VAE在噪声下性能急剧下降，而MoConVQ几乎不受影响。"
- "残差VQ层由粗到细地提升运动跟踪精度，同时保持了向量量化的鲁棒性。"
---

# MoConVQ: Unified Physics-Based Motion Control via Scalable Discrete Representations

> [!tip] 核心洞察
> 通过离散向量量化运动编码，可以利用VQ-VAE的紧凑性和鲁棒性来捕捉多样化运动技能，而基于模型的RL方法使大型生成式神经网络能够高效地在大规模运动数据上训练，从而实现统一的物理角色运动控制框架。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MoConVQ：基于可扩展离散表示的统一物理运动控制 |
| 英文题名 | MoConVQ: Unified Physics-Based Motion Control via Scalable Discrete Representations |
| 会议/期刊 | TOG 2024 |
| Links | [paper](https://arxiv.org/abs/2310.10198) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | MoConVQ |
| Dataset | Human3.6M, Human3.6M (motion quality) |

> [!tip] 效果简介
> - Human3.6M 上，PA-MPJPE 为 69.3 mm，对比 （见原论文对比Table 2）。
> - Human3.6M 上，PA-MPJPE, MPJPE 为 125.6 mm。
> - Human3.6M (motion quality) 上，运动平滑度 e_smooth 为 3.4。

## 概要

物理仿真角色的运动控制是计算机图形学中的一项长期挑战。传统方法通常需要为每一类运动手工设计奖励函数，并针对特定技能单独训练强化学习（RL）策略，难以扩展到大规模、多样化的运动数据集上。其根本瓶颈在于：**现有的连续潜在表示缺乏语义可解释性，且训练过程依赖不可微的物理模拟器，导致模型容量受限、训练效率低下。**

MoConVQ 针对上述瓶颈，提出了一个统一的、基于物理的运动控制框架。其核心思路是引入**离散向量量化（VQ-VAE）** 作为运动表示，将连续运动压缩为紧凑的离散潜在码序列，并配合**残差VQ架构**由粗到细地提升表示容量。同时，采用**基于模型的强化学习**方法，联合训练一个可微世界模型来近似物理模拟器，使整个解码过程可微，从而支持在大规模运动数据（超过20小时）上高效训练大型生成式神经网络。

该方法在多个下游任务上展现了统一的接口能力：在运动跟踪任务上，MoConVQ 在 Human3.6M 数据集上取得了 69.3 mm 的 PA-MPJPE，并显著提升了生成运动的物理质量（平滑度 3.4，加速度变化 5.1）；在文本到动作生成任务上，基于 MoConVQ 的 T2M-MoConGPT 在 HumanML3D 测试集上取得了 0.367 的 R-precision Top1 和 0.254 的 FID。消融实验进一步验证了向量量化对输入噪声的强鲁棒性，以及残差VQ层对跟踪精度的关键提升作用。

**方法谱系与知识库定位：** MoConVQ 建立在 VAE（Kingma & Welling, 2014）和 VQ-VAE（van den Oord et al., 2017）的基础之上，与同样采用世界模型作为可微模拟器的物理运动生成工作（Won et al., 2022; Yao et al., 2022）最为接近。其关键区别在于用离散码本替代连续潜在空间，并通过残差量化扩展容量，使得运动表示天然具备语义聚类特性，便于后续与 GPT 类自回归模型及大语言模型（LLM）集成。在下游任务中，它与运动学方法 **HybrIK**（Li et al., 2021）、**SimPoE**（Yuan et al., 2021）形成互补，与文本到动作方法 **MDM**（Tevet et al., 2023）、**T2MGPT**（Zhang et al., 2023b）等形成对比。

在计算机图形学与机器人学中，让物理仿真角色从大规模运动数据中学习多样化的运动技能是一个长期挑战。传统基于物理的角色控制方法通常需要为每一类运动手工设计奖励函数，并额外进行强化学习（RL）训练。这种“一类运动、一套奖励、一次训练”的范式使得系统难以扩展到大规模、非结构化的运动数据集上，也阻碍了统一运动控制框架的构建。

现有工作的核心瓶颈在于**运动表示的可扩展性与语义可解释性不足**。连续潜在变量模型（如标准VAE）虽然能够压缩运动数据，但其潜在空间缺乏结构化语义，且对输入噪声极为敏感——在引入中等高斯噪声时，连续VAE的跟踪性能急剧下降，而离散表示几乎不受影响。另一方面，无模型RL方法依赖不可微的物理仿真器，训练效率低下，难以处理包含数十小时运动示例的大规模数据集。

MoConVQ的核心动机是：**能否设计一种统一的运动表示与训练框架，使得物理角色能够从大规模运动数据中高效学习，并以一致的方式支持运动跟踪、交互控制、文本到动作生成等多种下游任务？**

为此，MoConVQ引入两个关键机制来突破上述瓶颈：

1. **离散向量量化（VQ）作为运动表示**。通过VQ-VAE框架将连续运动压缩为离散潜在码，利用向量量化的紧凑性和鲁棒性来捕捉多样化运动技能。配合残差VQ架构（多码本级联），模型容量得以显著提升，同时保留了离散表示对噪声的鲁棒性。

2. **基于模型的强化学习训练**。联合训练一个可微世界模型来近似黑箱物理仿真器，使整个解码过程可微，从而支持端到端训练。这使得大规模生成式神经网络能够在超过20小时的运动数据上高效训练。

这种设计使得MoConVQ能够在统一的框架下覆盖四大应用场景（Figure 1）：运动跟踪、交互控制、文本到动作生成，以及与大语言模型（LLM）的集成。

## 核心方法与创新机理

MoConVQ 的核心突破在于用**离散向量量化（VQ）**替代传统的连续潜在变量，从根本上改变了物理运动控制的表示与训练范式。这一创新并非孤立的技术替换，而是围绕“离散表示”这一因果旋钮，在模型容量、训练策略和下游任务接口三个维度上形成的系统性重构。

### 从连续到离散：表示层的根本转变

现有物理运动控制方法普遍采用连续 VAE 的潜在空间来表示运动。这种连续表示存在两个致命缺陷：其一，潜在空间缺乏语义可解释性，无法将不同运动技能自然地解耦为可组合的单元；其二，连续表示对输入噪声高度敏感——当测试运动被注入中等强度的高斯噪声时，连续 VAE 的跟踪性能急剧下降，而 MoConVQ 的性能几乎不受影响。这一鲁棒性差异来自 VQ 的量化操作本身：最近邻量化将每个潜在向量强制映射到码本中距离最近的离散条目，相当于在表示空间中引入了一道“量化屏障”，天然滤除了小幅扰动。

离散表示的另一个关键优势是紧凑性。每个运动片段最终被压缩为一组离散索引序列，这不仅是高效的存储形式，更重要的是为后续的生成建模和大语言模型集成提供了天然接口——离散索引可以被自回归 Transformer 直接建模，也可以作为“运动词汇”供 LLM 进行上下文学习。

### 残差 VQ：容量扩展的精细机制

单一码本的 VQ-VAE 面临容量瓶颈：增大码本尺寸会带来训练不稳定和计算开销激增。MoConVQ 采用**残差 VQ（Residual VQ）**架构来解决这一问题。其工作原理是由粗到细的渐进量化：第一层 VQ 捕获运动的整体特征（如身体轨迹和大致姿态），后续残差层依次对前一层的量化残差进行建模，逐步补充更精细的运动细节。消融实验直观地揭示了这一机制——当仅使用单层 VQ 时，左肘旋转等精细关节运动的跟踪曲线与真值存在明显偏差；随着残差层数从 1 层增加到 8 层，跟踪精度持续提升，同时保持了向量量化的鲁棒性。

从表示容量的角度看，残差 VQ 将码本容量从 $\mathcal{O}(|\mathcal{B}|)$ 扩展为 $\mathcal{O}(|\mathcal{B}|^N)$（$N$ 为残差层数），实现了指数级容量增长，使得模型能够在超过 20 小时的大规模运动数据集上进行有效训练。

### 基于模型的 RL：打通可扩展训练的瓶颈

大规模离散表示模型的训练面临一个工程瓶颈：物理模拟器本身是不可微的黑箱，无法通过标准反向传播直接优化。MoConVQ 通过**联合训练一个可微的世界模型 $\mathcal{W}$** 来近似真实仿真器，将解码过程转化为端到端可微的计算图：

$$\hat{\mathbf{a}}^t = \pi(\hat{\mathbf{s}}^t, \mathbf{u}^t), \quad \hat{\mathbf{s}}^{t+1} = \mathcal{W}(\hat{\mathbf{s}}^t, \hat{\mathbf{a}}^t)$$

世界模型 $\mathcal{W}$ 通过最小化其合成运动 $\tilde{M}_{\mathcal{W}}$ 与真实仿真运动 $\tilde{M}_{\mathrm{sim}}$ 之间的差异来持续优化。这一设计使得梯度可以从重建损失直接传导至编码器、码本和策略网络，从而高效处理数十小时规模的训练数据。与无模型 RL 方法相比，这种基于模型的训练策略避免了奖励函数手工设计和策略梯度估计方差大的问题，是实现统一大规模训练的关键使能技术。

### 统一的任务接口：从手工奖励到编码-解码范式

传统物理运动控制方法需要为每类运动单独设计奖励函数并重新训练 RL 策略，这严重限制了方法的通用性。MoConVQ 将下游任务统一为两类接口：

- **编码器-解码器任务**（如运动跟踪）：直接使用预训练编码器从参考运动提取潜在码，解码器负责物理仿真复现；
- **纯解码器任务**（如交互控制、文本生成动作）：训练一个独立的高层任务策略，根据特定条件（操纵杆输入、文本描述等）自回归地生成潜在码序列。

这种统一范式的关键在于：所有任务共享同一个预训练的物理解码器，运动技能被封装在离散码本中，任务策略只需学习“何时调用哪个运动技能”的组合逻辑，而非从头学习物理控制。这从根本上消除了手工奖励设计的依赖，使得框架能够以统一的方式支持运动跟踪、交互控制、文本到动作生成和 LLM 集成等四种截然不同的应用场景。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2310_10198/figures/001_Figure_1.jpg]]
*Figure 1: (d) LLM Integration Fig. 1. We present a method for learning discrete motion representation from a large-scale unstructured motion dataset for physics-based characters. The framework allows various applications, including those shown in this figure, to be accomplished in a unified fashion*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2310_10198/figures/002_Figure_2.jpg]]
*Figure 2: Framework overview. Our MoConVQ system consists of a motion encoder, a physics-based decoder, and a series of codebooks. A residual architecture is adopted to enhance the system’s representational capacity. The system represents motion as a sequence of quantized latent codes. Each latent code combines the quantized vectors from all residual layers. Equivalently, it can be represented by the indices of these quantized vectors in the codebooks of their corresponding residual layers*

MoConVQ 的整体 pipeline 围绕**离散运动表示的学习与利用**展开，其核心思想是：将大规模非结构化运动数据压缩为一组紧凑的离散潜在码（latent codes），并通过一个物理感知的解码器将这些码还原为满足物理约束的角色运动。整个系统由三个核心模块构成：**运动编码器（Motion Encoder）**、**残差向量量化层（Residual VQ Layers）** 和**物理解码器（Physics-Based Decoder）**，如图 2 所示。

### 输入输出流

系统的输入是一段运动序列 $\mathbf{M}$，输出是经过物理仿真重建的运动序列 $\tilde{\mathbf{M}}$。数据流遵循以下路径：

1. **编码**：运动编码器 $\mathcal{E}$（一个 1D 卷积网络）将原始运动片段下采样为连续潜在向量序列 $\mathbf{V}$。
2. **量化**：残差 VQ 模块 $\mathcal{B}$ 将每个连续潜在向量量化为离散码本中最近邻向量的组合，得到离散表示 $\mathbf{Z}$。每个潜在码由所有残差层的量化向量拼接而成，等价地可用各层码本中的索引序列表示。
3. **解码**：解码器 $\mathcal{D}$ 将离散码 $\mathbf{Z}$ 重建为运动 $\tilde{\mathbf{M}}$。解码过程包含三个子步骤：
   - **上采样**：1D 反卷积网络将量化后的运动表示上采样为与运动帧率一致的中介编码序列 $\mathbf{u}^t$。
   - **控制**：策略网络 $\pi$ 根据当前角色状态 $\mathbf{s}^t$ 和中介编码 $\mathbf{u}^t$ 计算输出动作 $\mathbf{a}^t$（关节目标角度）。
   - **仿真**：物理模拟器根据动作 $\mathbf{a}^t$ 推进角色状态至 $\mathbf{s}^{t+1}$。

### 关键设计决策

**残差 VQ 架构** 是提升模型容量的核心手段。标准 VQ-VAE 使用单一码本，表达能力受限于码本大小；残差 VQ-VAE 通过多个量化层级联，每层量化前一层的残差，使有效码本组合数随层数指数增长，从而在不显著增加码本尺寸的前提下大幅提升表示能力。消融实验证实，残差层在保持向量量化鲁棒性的同时，由粗到细地提升运动跟踪精度——首层 VQ 捕获整体运动轨迹，后续残差层逐步补充精细的运动细节（如关节旋转）。

**基于世界模型的端到端训练** 解决了物理模拟器不可微的问题。真实物理仿真器是一个黑箱函数，无法直接进行梯度回传。MoConVQ 联合训练一个可微的**世界模型 $\mathcal{W}$** 来近似仿真器的动力学，使整个解码过程可微，从而支持大规模神经网络的端到端训练。世界模型的损失函数为 $\mathcal{L}_{\mathcal{W}} = \| \tilde{M}_{\mathrm{sim}} - \tilde{M}_{\mathcal{W}} \|$，即最小化真实仿真结果与世界模型合成结果之间的差异。

**动作正则化** 通过指数移动平均（EMA）实现。策略输出的动作序列 $\hat{\mathbf{a}}^t$ 可能包含高频抖动，导致不自然的运动。MoConVQ 将 EMA 作为软约束引入优化问题，正则化损失 $\mathcal{L}_{\mathrm{reg}} = \sum_t w_1 \| \hat{\mathbf{a}}^t - \bar{\mathbf{a}}_t \| + w_2 \| \hat{\mathbf{a}}^t \|$ 限制动作与其 EMA 平滑版本之间的差异，有效抑制了脚滑和高频抖动。经验上，平滑因子 $\beta = 0.8$ 可获得合理的视觉效果。

### 上下游任务接口

MoConVQ 的统一接口支持两类下游任务配置：

- **编码器-解码器任务**（如运动跟踪）：使用预训练编码器从输入运动计算潜在码序列，再通过解码器生成物理正确的运动。
- **纯解码器任务**（如交互控制、文本到动作生成、LLM 集成）：训练独立的高层任务策略，根据特定条件（操纵杆输入、文本描述、LLM 规划）直接生成潜在码序列，无需编码器参与。

这种设计使得 MoConVQ 成为一个通用运动生成平台：相同的预训练编解码器可服务于多种应用，避免了传统方法中为每类运动手工设计奖励函数并重新训练 RL 策略的繁琐流程。

### 整体流水线

MoConVQ 框架由三条核心流水线串联构成：**运动编码器**将原始运动压缩为连续潜在向量，**残差向量量化层**将连续向量映射为离散码本索引，**物理解码器**从离散表示中自回归地重建出物理仿真运动。其编码-量化-解码的形式化定义为：

$$ \mathbf{V} = \mathcal{E}(\mathbf{M}), \quad \mathbf{Z} = \mathcal{B}(\mathbf{V}), \quad \tilde{\mathbf{M}} = \mathcal{D}(\mathbf{Z}) $$

其中 $\mathbf{M}$ 为输入运动片段，$\mathcal{E}$ 为编码器，$\mathbf{V}$ 为连续潜在向量序列，$\mathcal{B}$ 为码本量化操作，$\mathbf{Z}$ 为量化后的离散表示，$\mathcal{D}$ 为解码器，$\tilde{\mathbf{M}}$ 为重建运动。

### 运动编码器

编码器 $\mathcal{E}$ 采用 **1D 卷积神经网络**，以固定比例对输入运动片段 $\mathbf{M}$ 进行下采样，将其压缩为 $\mathbf{K}$ 个潜在向量 $\mathbf{V} = \{v^k\}_{k=1}^{K}$。编码器与解码器中的上采样模块构成对称的全卷积结构，支持流式处理（streaming processing），使实时运动生成成为可能。

### 残差向量量化

标准 VQ-VAE 的码本容量随维度增长而指数膨胀，单一大码本难以高效覆盖多样化运动技能。MoConVQ 采用**残差 VQ 架构**，通过 $\mathbf{N}$ 层级联的量化层逐步细化运动表示。每个潜在向量 $v^k$ 的量化过程为：首层在码本 $\mathcal{B}_0$ 中找到最近邻向量作为主成分，后续残差层依次量化前一层重建后的残差。最终离散表示 $\mathbf{Z}$ 等价于各层码本索引的序列组合。

最近邻量化的核心操作定义为：

$$ z^{k}, I^{k} = \arg\min_{z_i \in \mathcal{B}} \| z_i - v^{k} \|_2^2 $$

即每个潜在向量 $v^k$ 被替换为码本 $\mathcal{B}$ 中距离最近的码向量 $z^k$，并记录其索引 $I^k$。残差 VQ 使模型容量随层数呈指数增长，同时保持了向量量化对输入噪声的鲁棒性。

### 物理解码器

解码器 $\mathcal{D}$ 由三个子模块组成：

1. **反卷积上采样模块**：将量化后的离散表示 $\mathbf{Z}$ 上采样为与运动帧率对齐的中介编码序列 $\mathbf{u}^t$。
2. **控制策略 $\pi$**：基于当前角色状态 $\mathbf{s}^t$ 和中介编码 $\mathbf{u}^t$，输出目标关节角度作为动作 $\mathbf{a}^t$：

$$ \mathbf{a}^t = \pi(\mathbf{s}^t, \mathbf{u}^t) $$

3. **物理仿真模块**：根据动作 $\mathbf{a}^t$ 推进角色状态：

$$ \mathbf{s}^{t+1} = \mathrm{Sim}(\mathbf{s}^t, \mathbf{a}^t) $$

角色由 PD 控制器驱动，关节力矩计算为 $\tau = k_p (\bar{\theta} - \theta) - k_d \dot{\theta}$，其中 $\bar{\theta}$ 为目标关节角度，$\theta$ 和 $\dot{\theta}$ 分别为当前关节角度和角速度。

### 可微世界模型

物理仿真器 $\mathrm{Sim}$ 是黑盒不可微的，阻碍了端到端梯度传播。MoConVQ 采用**基于模型的强化学习**策略，联合训练一个可微网络 $\mathcal{W}$（世界模型）来近似真实仿真器：

$$ \hat{\mathbf{a}}^t = \pi(\hat{\mathbf{s}}^t, \mathbf{u}^t), \quad \hat{\mathbf{s}}^{t+1} = \mathcal{W}(\hat{\mathbf{s}}^t, \hat{\mathbf{a}}^t) $$

世界模型通过最小化其合成运动 $\tilde{M}_{\mathcal{W}}$ 与真实仿真运动 $\tilde{M}_{\mathrm{sim}}$ 之间的差异来更新：

$$ \mathcal{L}_{\mathcal{W}} = \| \tilde{M}_{\mathrm{sim}} - \tilde{M}_{\mathcal{W}} \| $$

这使得整个解码过程可微，允许大规模神经网络在数十小时的运动数据集上高效训练。

### 训练损失函数

MoConVQ 的总训练损失由四项组成：

$$ \mathcal{L} = \| \mathbf{M} - \tilde{\mathbf{M}}_{\mathcal{W}} \| + \beta_1 \| \mathcal{E}(\mathbf{M}) - \mathrm{sg}(\mathbf{Z}) \| + \beta_2 \| \mathrm{sg}(\mathcal{E}(\mathbf{M})) - \mathbf{Z} \| + \beta_3 \mathcal{L}_{\mathrm{reg}} $$

- 第一项为**重建损失**，约束世界模型输出的运动与原始运动一致。
- 第二项为**承诺损失**，鼓励编码器输出靠近量化后的码向量（$\mathrm{sg}$ 为停止梯度算子）。
- 第三项为 **VQ 目标损失**，推动码向量向编码器输出靠拢。
- 第四项 $\mathcal{L}_{\mathrm{reg}}$ 为**动作正则化损失**。

### 动作 EMA 正则化

为抑制高频抖动和脚滑等物理不真实现象，MoConVQ 使用指数移动平均作为软约束。动作的 EMA 计算为：

$$ \bar{\mathbf{a}}^t = (1-\beta)\bar{\mathbf{a}}^{t-1} + \beta \hat{\mathbf{a}}^t $$

其中 $\beta=0.8$ 为经验平滑因子。正则化损失限制当前动作与 EMA 的偏差及动作幅度：

$$ \mathcal{L}_{\mathrm{reg}} = \sum_t w_1 \| \hat{\mathbf{a}}^t - \bar{\mathbf{a}}^t \| + w_2 \| \hat{\mathbf{a}}^t \| $$

与硬性 EMA 后处理不同，此软约束将平滑性纳入优化目标，在保持运动自然度的同时避免过度平滑。

## 实验与关键发现

### 核心实验设置

MoConVQ在超过20小时的大规模无结构运动数据集上进行训练，数据来源包括AMASS和LaFAN（Table 1）。训练采用基于模型的强化学习方法，联合训练一个可微世界模型来近似黑盒物理仿真器，从而使得整个解码过程可微，支持端到端的梯度优化。动作正则化采用指数移动平均（EMA）作为软约束，平滑因子β=0.8在实践中取得合理的视觉效果。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2310_10198/figures/006_Table_1.jpg]]
*Table 1: Motion dataset. LaFAN is from [Harvey et al. 2020], the other datasets are from AMASS [Mahmood et al. 2019]*

### 运动跟踪与物理姿态估计

在Human3.6M数据集上，MoConVQ与多个基线方法进行了定量比较（Table 2）。在PA-MPJPE指标上，MoConVQ达到69.3 mm，MPJPE为125.6 mm。需要指出的是，对比的基线方法（HybrIK、PhysCap、SimPoE）中，HybrIK为纯运动学方法，未引入物理约束；MoConVQ的核心优势在于生成物理正确性，而非单纯的追踪精度。在HDM05数据集上，MoConVQ的MPBPE为6.3 cm。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2310_10198/figures/008_Table_2.jpg]]
*Table 2: Evaluation on Human3.6M dataset. The baseline methods are HybrIK [Li et al. 2021], PhysCap [Shimada et al. 2020], and SimPoE [Yuan et al. 2021]*

运动质量评估（Table 3）进一步验证了物理正确性：MoConVQ生成的运动平滑度e_smooth达到3.4，加速度变化Accel为5.1，表明模型能够产生物理合理、无明显抖动的运动序列。

### 文本到动作生成

在HumanML3D测试集上，MoConVQ的文本到动作生成变体T2M-MoConGPT与多个最先进方法进行了比较（Table 4）。在R-precision Top1指标上，T2M-MoConGPT达到0.367，FID为0.254。作为参考，经过角色骨架重定向处理的Ground Truth运动（GT Retargeted）的R-precision Top1为0.440——这一差距表明重定向过程本身引入了系统性精度损失，构成了当前方法的性能上界约束。对比的基线方法包括基于扩散模型的MDM（Tevet et al., 2023）、基于GPT的T2MGPT（Zhang et al., 2023b）等运动学方法，MoConVQ在生成物理正确运动的同时，在语义匹配精度上与运动学方法仍存在差距。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2310_10198/figures/016_Table_4.jpg]]
*Table 4: Comparison with the state-of-the-art text-to-motion generation methods. We compute the metrics following [Guo et al. 2022a] on the test set of HumanML3D. Metrics for Hier [Ghosh et al. 2021], MDM [Tevet et al. 2023], TM2T [Guo et al. 2022b], and T2MGPT [Zhang et al. 2023b] has been reported in their papers. To demonstrate the effect of the retargeting process, we retarget the ground truth motion to our character and then retarget it back, the results are shown in the row of GT (Retargeted). Fig. 12. Prompt used for in-context learning with an LLM*

### 消融实验

**向量量化的鲁棒性**是最关键的消融发现。在HDM05测试集上，当对输入运动引入中等强度的高斯噪声时，连续VAE模型的跟踪性能急剧下降，而MoConVQ的性能几乎不受影响（Figure 17）。这一结果表明，向量量化对运动数据中的噪声具有极强的鲁棒性——离散码本的量化操作天然地抑制了噪声在潜在空间中的传播，使得模型在真实世界的噪声条件下（如不完美的姿态估计输入）依然能够稳定运行。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2310_10198/figures/020_Figure_17.jpg]]
*Figure 17: (a) Clean motion data (b) Motion data corrupted by adding Gaussian noise $\epsilon \sim { \cal N }$ ( 0 , 0 . 1 ) Fig. 17. Tracking error of different motion representations on the same test set from HDM05 [Müller et al. 2007]. We test three models: i) The continuous VAE model with KL regularization, ii) Our MoConVQ model with 8 VQ layers, and iii) Our MoConVQ model with only the VQ layer. The curves represent kernel density estimations

**残差VQ层的贡献**体现在精度与鲁棒性的平衡上。Figure 17同时显示，仅使用单层VQ的MoConVQ虽然保持了鲁棒性，但跟踪精度不足；而完整的8层残差VQ模型在保持鲁棒性的同时，显著提升了运动跟踪精度。Figure 18进一步揭示了残差结构的工作机制：首层VQ捕获运动的整体特征（如身体轨迹），后续残差层逐步补充精细的运动细节（如左肘旋转曲线）。这种由粗到细的表示能力是残差VQ架构的核心优势。

**EMA动作正则化**有效抑制了高频抖动和脚滑等不真实运动。通过将EMA作为软约束加入优化目标，模型在保持运动自然度的同时，避免了硬平滑带来的过度阻尼问题。

### 失败模式与局限性

当前方法存在若干明确的失败模式：

1. **高难度动作学习困难**：对于数据稀疏的极低频动作（如后空翻、武术），模型难以学习到有效的运动表示。这是数据驱动方法的固有瓶颈，训练集中相关样本的稀缺导致码本对这些技能的覆盖不足。

2. **解码器延迟问题**：解码器依赖未来运动编码进行重建，引入了额外的时序延迟。这使得MoConVQ难以直接部署到要求极低延迟的实时控制场景中。

3. **控制粒度受限**：当前框架不支持对单个肢体或关节的直接控制，控制接口为隐式的潜在码序列，限制了精细动作编辑的能力。

4. **LLM集成的不确定性**：大语言模型集成实验仅为定性展示，LLM可能输出不可靠的动作序列（如“作弊”或误解示例）。Figure 15中，LLM被要求控制角色走出正方形轨迹，但由于缺乏角度信息，实际轨迹近似三角形，暴露了上下文学习在精确空间推理上的不足。

5. **复杂环境交互缺失**：框架尚未验证对搬动物体、开门等需要精细接触建模的任务，以及多智能体协作场景的支持。

### 关键图表结论

- **Figure 5**：MoConVQ的典型学习曲线显示，模型在训练初期快速收敛，随后进入稳定的精细化阶段，验证了基于模型的RL方法在大规模运动数据上的训练效率。
- **Figure 9**：操纵杆控制信号的响应曲线表明，角色能够准确跟踪用户输入的目标速度和方向，验证了交互控制配置（decoder-only）的有效性。

- **Figure 10**：MoConGPT的无条件生成展示了从相同初始状态出发，通过随机采样产生多样化、平滑的运动类型和轨迹，验证了离散运动表示作为生成式运动先验的潜力。

## 定位与知识库关联

### 1. 方法谱系：从连续潜在空间到离散运动表征

MoConVQ 的方法学根基建立在三个技术脉络的交汇点上：

**变分自编码器与运动生成。** 该工作的编码-解码架构直接继承自 VAE（Kingma & Welling, 2014），但在运动控制语境下做了关键改造。与最接近的前驱工作——**Won et al. (2022)** 和 **Yao et al. (2022)**——相比，MoConVQ 共享了“用世界模型作为可微仿真器、将物理运动生成归约为 VAE 训练”这一核心思路。然而，前驱工作采用**连续潜在变量**，这带来了两个结构性问题：一是潜在空间缺乏语义可解释性，二是模型对输入噪声高度敏感。MoConVQ 将潜在空间从连续域切换到**离散向量量化（VQ-VAE）**域，从根本上改变了表征的鲁棒性和可组合性。

**向量量化表征学习。** 离散码本的设计直接源于 VQ-VAE（van den Oord et al., 2017），但 MoConVQ 面临的核心挑战是容量瓶颈——单一码本难以覆盖数十小时运动数据中的多样化技能。为解决此问题，MoConVQ 引入**残差 VQ（Residual VQ）**架构，通过多层码本级联将表示容量指数级扩展：首层 VQ 捕获运动整体轨迹（粗粒度结构），后续残差层逐步补充精细细节（如关节旋转的微妙变化）。这一设计使模型能在保持 VQ 鲁棒性的前提下，达到与连续 VAE 相当的跟踪精度。

**基于模型的强化学习。** 物理仿真的不可微性是端到端训练的核心障碍。MoConVQ 采用基于模型的 RL 范式，联合训练一个可微世界模型 $\mathcal{W}$ 来近似黑箱物理模拟器，使得从离散码到角色动作再到仿真状态的整个解码链可微。这一选择使大规模生成式神经网络能在超过 20 小时的运动数据上高效训练，而无需为每类运动手工设计奖励函数或进行额外的 RL 微调。

### 2. 关键设计决策与因果机制

MoConVQ 的四个核心设计槽位及其因果效应可概括如下：

| 设计槽位 | 基线方案 | MoConVQ 方案 | 因果效应 |
|---------|---------|-------------|---------|
| 潜在表示类型 | 连续潜在变量（标准 VAE） | 离散向量量化（VQ-VAE） | 赋予模型对输入噪声的强鲁棒性；连续 VAE 在噪声下性能急剧下降，MoConVQ 几乎不受影响 |
| 容量扩展方式 | 增大单一码本 | 残差 VQ（多码本级联） | 由粗到细地提升跟踪精度，同时保持 VQ 的鲁棒性；仅用单层 VQ 精度不足 |
| 训练方法 | 无模型 RL 或标准 VAE 直接训练 | 基于模型的 RL 联合训练可微世界模型 | 使大规模神经网络能在不可微物理仿真环境中端到端训练 |
| 动作正则化 | 无或硬 EMA 平滑 | EMA 作为软约束加入正则化损失 $\mathcal{L}_{\mathrm{reg}}$ | 有效抑制高频抖动和脚滑等非物理伪影 |

其中，离散表征的鲁棒性是最具区分度的性质。消融实验（Figure 17）表明：当测试运动被注入中等高斯噪声时，连续 VAE 的跟踪误差急剧增大，而 MoConVQ 的性能基本不变。这一性质使得 MoConVQ 能够处理来自真实传感器（如单目姿态估计器）的含噪输入，而无需额外的滤波或后处理。

### 3. 知识库定位：统一接口与下游任务谱系

MoConVQ 的核心贡献在于将物理运动控制统一为**“编码-解码”与“纯解码”**两类配置，消除了传统方法中为每类运动单独设计奖励函数并重新训练 RL 策略的碎片化问题：

- **编码-解码任务（如运动跟踪、基于物理的姿态估计）：** 利用预训练编码器从输入运动（或姿态估计结果）计算潜在码序列，解码器直接生成物理正确的运动。在此配置下，MoConVQ 与 **HybrIK**（Li et al., 2021）、**PhysCap**（Shimada et al., 2020）、**SimPoE**（Yuan et al., 2021）等纯运动学方法形成对比——MoConVQ 的核心优势在于生成运动的物理正确性（脚滑抑制、动量守恒），而非单纯的追踪精度。

- **纯解码任务（如交互控制、文本到动作生成、LLM 集成）：** 训练独立的高层任务策略或生成模型（如 MoConGPT），直接预测潜在码序列。在文本到动作生成任务上，MoConVQ 与 **Hier**（Ghosh et al., 2021）、**MDM**（Tevet et al., 2023）、**TM2T**（Guo et al., 2022b）、**T2MGPT**（Zhang et al., 2023b）等运动学方法形成对比。值得注意的是，由于角色骨架重定向过程引入系统误差，MoConVQ 的 R-precision 等语义指标相对于原始运动有所下降（GT Retargeted 的 Top1 R-precision 为 0.440，MoConVQ 为 0.367），但其生成的运动会自动满足物理约束，这是纯运动学方法无法保证的。

### 4. 适用边界与已知局限

尽管 MoConVQ 在统一性和鲁棒性上取得了显著进展，其适用边界受以下因素制约：

1. **数据稀疏的高难度动作。** 当前方法难以学习极低频的复杂动作（如后空翻、武术），因为相关训练数据在数据集中占比极低。这不是架构问题，而是数据分布的长尾效应——残差 VQ 的容量足够，但训练信号不足。

2. **解码延迟与实时控制。** 解码器依赖未来运动编码（通过 1D 卷积的感受野），引入了额外延迟。这使得 MoConVQ 难以直接应用于要求极低延迟的实时控制场景（如游戏角色实时响应玩家输入）。

3. **控制粒度受限。** 当前接口不支持对单个肢体或关节进行直接控制——控制是通过潜在码序列隐式完成的。这意味着用户无法指定“抬起左手到特定角度”这样的精细指令。

4. **环境交互验证不足。** 框架尚未验证对复杂环境交互（如搬动物体、开门）和多智能体协作的支持。LLM 集成实验仅为定性展示，且 LLM 可能输出不合理的动作序列（如“作弊”或误解示例），缺乏闭环反馈机制。

### 5. 开放问题与后续方向

从 MoConVQ 的局限出发，可识别以下开放问题：

- **低资源动作学习：** 如何扩展框架以学习数据稀少的高难度动作？可能的方向包括数据增强、迁移学习、或引入基于物理的显式先验（如动捕数据中的关键帧约束）。

- **低延迟解码：** 能否用因果卷积或自回归解码器替代当前依赖未来帧的编码器，从而消除延迟？这需要在表征质量和实时性之间寻找新的平衡点。

- **细粒度控制接口：** 能否用更细粒度的控制信号（如单关节目标角度或末端执行器位置）替代当前的隐式潜在码控制？这可能需要重新设计码本结构或引入层次化表征。

- **LLM 闭环控制：** 如何将环境交互反馈纳入大语言模型的推理循环，使 LLM 能根据仿真结果动态调整动作序列？这涉及将物理仿真状态转化为 LLM 可理解的文本或 token 表示。

- **多模态与多智能体扩展：** 框架能否扩展至多智能体协作场景，以及更丰富的多模态输入（如音乐、语音）驱动？离散码的紧凑性可能使其成为连接不同模态的自然接口。

## 原文 PDF

![[paperPDFs/TOG_2024/MoConVQ_Unified_Physics_Based_Motion_Control_via_Scalable_Discrete_Representations.pdf]]
