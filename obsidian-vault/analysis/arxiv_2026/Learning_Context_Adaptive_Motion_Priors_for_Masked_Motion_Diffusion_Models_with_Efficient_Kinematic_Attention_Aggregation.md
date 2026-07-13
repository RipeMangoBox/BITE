---
title: Learning Context-Adaptive Motion Priors for Masked Motion Diffusion Models with Efficient Kinematic Attention Aggregation
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/Learning_Context_Adaptive_Motion_Priors_for_Masked_Motion_Diffusion_Models_with_Efficient_Kinematic_Attention_Aggregation.pdf
project_link: null
code_link: https://github.com/jjkislele/MMDM
aliases:
- MMDMM
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 运动学注意力聚合（KAA）机制在掩码扩散模型中将关节级空间结构信息聚合到姿势级表示，沿时间维度建模轨迹，在保持计算效率的同时显著增强运动上下文理解能力。
primary_logic: 通过在结构注意力和时间注意力之间桥接可学习的聚合令牌，KAA迭代地深度编码关节间的结构关系与时间依赖，使模型能够提取任务特定的上下文自适应运动先验，无需改变网络结构即可适应运动补全、细化与插值等多样化任务。
claims:
- KAA机制高效结合关节级与姿势级信息，实现深度时空特征编码。
- 集成KAA的掩码扩散模型MMDM能够利用部分高质量数据条件生成缺失运动。
- KAA对骨骼结构优先聚合的设置带来最高重建精度。
- 在Shelf和Campus公开基准上MMDM均取得最优平均PCP。
---

# Learning Context-Adaptive Motion Priors for Masked Motion Diffusion Models with Efficient Kinematic Attention Aggregation

> [!tip] 核心洞察
> 通过在结构注意力和时间注意力之间桥接可学习的聚合令牌，KAA迭代地深度编码关节间的结构关系与时间依赖，使模型能够提取任务特定的上下文自适应运动先验，无需改变网络结构即可适应运动补全、细化与插值等多样化任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向掩码运动扩散模型的上下文自适应运动先验学习与高效运动学注意力聚合 |
| 英文题名 | Learning Context-Adaptive Motion Priors for Masked Motion Diffusion Models with Efficient Kinematic Attention Aggregation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2603.07697) · [Code](https://github.com/jjkislele/MMDM) · [paper](https://arxiv.org/abs/2303.01469) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Masked Motion Diffusion Model (MMDM) |
| Dataset | Shelf, Campus, BUMocap, BUMocap-X |

> [!tip] 效果简介
> - Shelf 上，PCP (%) AVG 98.5±.15 vs 98.2 (JCSAT) (+0.3)。
> - Campus 上，PCP (%) AVG 97.6±.08 vs 97.3 (JCSAT) (+0.3)。
> - BUMocap (BU) 上，PCP↑ 96.2±.52 vs 95.5 (JCSAT) (+0.7)。

## 概要

从多视角视频中恢复准确的三维人体运动是计算机视觉中的长期难题，其核心瓶颈在于**遮挡**——当身体关键点被遮挡、二维姿态估计置信度低或三角测量误差大时，传统重建方法会严重退化。现有方案存在两个结构性缺陷：**掩码自编码器（MAE）** 只能从干净的无掩码部分重建缺失区域，无法处理噪声输入；**运动扩散模型**则要求完整序列作为输入，且计算开销巨大。两者均缺乏一个能够同时接受部分含噪输入、并高效融合关节级空间结构与姿势级时间依赖的生成式重建框架。

本文的核心贡献是提出了**运动学注意力聚合机制（Kinematic Attention Aggregation, KAA）**，并以此构建了**掩码运动扩散模型（Masked Motion Diffusion Model, MMDM）**。KAA通过在结构注意力与时间注意力之间引入可学习的聚合令牌，迭代地将关节级空间结构信息压缩至姿势级表示，再沿时间维度建模运动轨迹。这一设计使模型能够提取**上下文自适应的运动先验**——在推理时，以未遮挡的高质量关节为条件，对掩码的含噪区域执行条件逆扩散生成，无需改变网络结构即可适应运动补全、运动细化和运动插值等多样化任务。

MMDM在多个公开基准上取得最优结果：在Shelf和Campus数据集上平均PCP分别达到**98.5%**和**97.6%**，在更具挑战的BUMocap-X数据集上领先次优方法**3.6个百分点**（92.1% vs 88.5%）。在运动插值任务中，MMDM相较先前扩散方法**MDM**（Tevet et al., ICLR 2023）在L2位置误差、L2旋转误差和NPSS三项指标上分别降低**73%、75%和76%**。消融实验证实，KAA优先聚合骨骼结构的配置、预训练采用随机掩码而微调采用自适应加权掩码的策略，以及质心归一化的数据预处理，是性能提升的关键因素。

MMDM的主要局限性在于扩散逆过程仍需数百步迭代，单次评估耗时超过7小时，难以满足实时应用需求；此外，不同任务（补全、细化、插值）目前需要分别微调，尚未统一为单一模型。未来工作可探索更高效的采样策略以压缩推理时间，以及设计统一的端到端框架来覆盖多样化运动生成任务。



从多视角视频中重建准确的三维人体运动是计算机视觉领域的长期挑战，其核心瓶颈在于**遮挡**——当人体关节被自身、他人或环境遮挡时，二维姿态估计器提供的观测信息变得稀疏、含噪且不可靠，导致三维重建结果出现严重失真。这一问题的本质是**从部分、低质量观测中推断完整、高质量运动序列**的生成式重建任务。

现有方法在面对这一挑战时存在明显的结构性缺口。**掩码自编码器（Masked Autoencoders, MAE）** 能够从可见关节重建被掩码的关节，但其设计假设输入是“干净”的，无法处理观测中的噪声与不确定性。**运动扩散模型**则擅长从噪声中逐步去噪生成高质量运动，但其标准范式要求以完整运动序列作为输入，无法直接利用部分观测进行条件生成。换言之，MAE缺乏对噪声的鲁棒性，扩散模型缺乏对部分输入的条件化能力，二者各执一端，未能形成统一框架。

更深层的问题在于**运动表示方式**的分离。如表I所示，人体姿态估计相关方法倾向于在关节级提取特征，关注单个关节的空间位置；而运动生成方法则通常在姿势级建模，将整个骨架姿态视为一个整体。这种表示粒度上的割裂导致模型难以同时捕捉**关节间的骨骼结构约束**与**姿势序列的时间动态**，从而在遮挡条件下缺乏足够的运动上下文理解能力。

本文的动机正是弥合上述缺口：**能否设计一种生成式重建框架，同时具备（1）对部分、含噪输入的条件化能力，（2）对关节级结构与姿势级动态的高效融合能力？** 为此，我们提出**运动学注意力聚合（Kinematic Attention Aggregation, KAA）** 机制，通过可学习聚合令牌在结构注意力与时间注意力之间建立桥梁，迭代地深度编码关节间的空间关系与时间依赖，从而提取上下文自适应的运动先验。在此基础上，我们将KAA嵌入掩码扩散范式，构建**掩码运动扩散模型（Masked Motion Diffusion Model, MMDM）**，以未掩码的高质量观测为条件，对掩码噪声输入进行条件逆扩散生成，实现从部分到完整的运动重建。

如图1所示，MMDM突破了传统MAE与运动扩散模型的各自局限：它不再要求输入是干净完整的，而是能够利用部分高质量数据条件生成缺失运动，在运动补全、细化与插值等多样化任务中展现统一的生成能力。



## 核心方法与创新机理

本文的核心贡献在于提出了一种**上下文自适应的运动先验学习框架**，其关键创新并非引入全新的生成范式，而是通过三个紧密耦合的**changed slots**，系统性地解决了现有方法在部分含噪输入下进行高质量运动重建的瓶颈。

### 瓶颈诊断：MAE与扩散模型的互补盲区

现有方法在运动重建任务上存在明显的功能割裂（参见**Figure 1**）：

- **掩码自编码器（MAE）**（如**D-MAE**, ACMMM 2022）只能从干净的未掩码关节重建被掩码区域，无法处理含噪声的输入数据，缺乏生成多样性。
- **运动扩散模型**（如**MDM**, ICLR 2023；**GMD**, ICCV 2023）虽然能够通过去噪生成高质量运动，但通常要求完整的输入序列，且计算复杂，难以有效利用部分高质量观测作为条件进行定向生成。

核心瓶颈在于：**缺乏一个能够同时处理部分含噪声输入、并高效融合关节级空间结构与姿势级时序依赖的生成式重建框架**。

### 关键创新：运动学注意力聚合（KAA）机制

针对上述瓶颈，本文提出了**运动学注意力聚合（Kinematic Attention Aggregation, KAA）**机制，这是实现高效时空特征融合的**因果旋钮**。

- **设计原理**：KAA桥接了结构注意力（Spatial Attention）与时间注意力（Temporal Attention），通过可学习的聚合令牌（Aggregation Tokens）将关节级的空间结构信息迭代地聚合到姿势级表示中。其核心操作顺序为：**结构注意力 → 聚合 → 时间注意力**。
- **为什么有效**：消融实验证实，优先聚合骨骼结构信息（即结构注意力在前）能够带来最高的重建精度（*aggregating skeletal structure first yields the highest accuracy*）。这表明显式编码关节间的运动学依赖关系，是模型提取上下文自适应运动先验的基础。
- **效率优势**：KAA在保持计算效率的同时，实现了对时空依赖的深度编码，使模型无需改变网络结构即可适应运动补全、细化与插值等多样化任务。

### 范式融合：掩码运动扩散模型（MMDM）

基于KAA机制，本文进一步将**扩散生成与掩码重建进行范式级融合**，提出了**掩码运动扩散模型（Masked Motion Diffusion Model, MMDM）**。

- **融合方式**：MMDM将扩散过程嵌入到MAE的解码范式中。具体而言，以未掩码部分（高质量观测）作为条件，对掩码区域的噪声输入进行**条件逆扩散生成**。这与传统MAE仅从干净特征重建、或扩散模型处理完整噪声输入的方式截然不同。
- **工作流**：在编码器端，KAA从未掩码运动中提取运动学条件表示 $\mathbf{c}$；在解码器端，以 $\mathbf{c}$ 为条件，逐步对掩码噪声令牌进行去噪，最终重建完整的运动序列。

### 自适应掩码策略：任务感知的先验注入

为了让模型更好地适应真实世界中遮挡和低质量输入场景，MMDM引入了一种**基于2D置信度和三角误差的自适应加权掩码策略**。

- **掩码权重计算**：对于每个关节 $j$ 在时刻 $t$ 的掩码概率，由权重 $w_{j,t} = \omega \cdot e^{-\sum_{v=1}^{V} \rho_{j,v}^{t}} + \sigma_{j}^{t}$ 决定，其中 $\rho$ 为2D置信度，$\sigma$ 为三角测量误差。该设计使得被遮挡或估计质量低的关节更可能被掩码。
- **训练策略**：预训练阶段采用随机掩码（模式A）以学习通用运动先验，微调阶段切换为自适应加权掩码（模式C），以获得最佳的任务特定性能。消融实验表明，这种组合策略在Shelf数据集上取得了最优的平均PCP。

### 创新点总结

综上所述，本文的核心创新并非单一技术点，而是一个**协同增效的创新系统**：

1. **KAA机制**（核心因果旋钮）：高效融合关节级与姿势级特征，实现深度时空编码。
2. **掩码扩散范式**（范式融合）：首次将条件扩散生成与MAE掩码重建结合，处理部分含噪输入。
3. **自适应掩码策略**（任务适配）：根据输入质量动态调整掩码，增强模型对真实遮挡场景的鲁棒性。

这三个changed slots共同赋予了MMDM从部分、低质量数据中提取上下文自适应运动先验的能力，使其在运动补全、细化和插值等任务上均取得了显著优于现有方法的性能。



MMDM 的设计动机源于一个核心瓶颈：**传统掩码自编码器（MAE）无法处理噪声输入，而运动扩散模型需要完整输入且计算复杂**，二者均无法在部分含噪观测条件下生成高质量人体运动。为填补这一空白，MMDM 将**掩码扩散范式**与**运动学注意力聚合（KAA）**机制融合为一个统一的生成式重建框架，其整体架构如 Figure 1 所示。

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/002_Figure_1.jpg]]
*Figure 1: Architecture comparison of the proposed Masked Motion Diffusion Model (MMDM) against other methods. (a) Masked Autoencoders (MAEs) [4], [29], [30] reconstruct masked (low-confidence) joints from unmasked (visible/high-confidence) joints, but they are not designed for noisy input. (b) Motion diffusion models [27], [31] denoise pose sequences to generate high-quality motions, which typically require complete input tokens. (c) Our MMDM combines both paradigms, taking partial, noisy inputs and fusing joint- and pose-level representations via the proposed Kinematic Attention Aggregation (KAA) to output complete, high-quality motions*

### 宏观架构：编码器-解码器与扩散过程的融合

MMDM 采用标准的自编码器结构，由**运动学编码器（Kinematic Encoder）**和**运动解码器（Motion Decoder）**两部分组成。与常规 MAE 不同的是，扩散学习策略被直接嵌入到解码范式中：编码器从**未掩码（高质量）运动数据**中提取条件表示，解码器则以此为条件，对**掩码噪声令牌**执行条件逆扩散生成，逐步从高斯噪声中重建完整运动序列。

具体而言，给定一段部分观测的运动数据，模型首先将关节划分为未掩码部分 $\mathbf{d}^{\overline{m}}$ 和掩码部分 $\mathbf{d}^{m}$。编码器 $E_{\phi}$ 对未掩码输入进行编码，输出两类信息：
- **未掩码运动令牌** $\mathbf{h}^{\overline{m}}$：保留可见关节的时空特征；
- **运动学条件** $c$：由 KAA 机制深度聚合后的全局上下文表示。

解码器 $D_{\theta}$ 接收拼接后的令牌 $[\mathbf{h}^{\overline{m}}; \mathbf{z}_{k}^{m}]$（其中 $\mathbf{z}_{k}^{m}$ 为扩散步 $k$ 的掩码噪声令牌），并以条件 $c$ 和扩散步索引 $k$ 为引导，预测去噪后的运动 $\widehat{\mathbf{d}}_{k-1}^{m}$。这一过程从 $k=K$ 迭代至 $k=0$，每一步中解码器输出的未掩码部分被原始高质量输入 $\mathbf{d}^{\overline{m}}$ 替换，以保持运动上下文的完整性（见 Figure 2）。

### 核心模块：运动学注意力聚合（KAA）

KAA 是连接关节级与姿势级表示的关键机制，部署于运动学编码器内部。编码器由 $N$ 对自注意力块堆叠而成，每对包含一个**结构注意力块（Structural Attention）**和一个**时间注意力块（Temporal Attention）**，二者通过 KAA 机制互联。

KAA 的工作流如下：
1. **结构注意力**首先在关节维度上建模骨骼结构关系，提取关节间的空间依赖；
2. **可学习聚合令牌**将关节级结构信息压缩并传递至姿势级表示；
3. **时间注意力**在姿势级沿时间维度建模运动轨迹与动态演化。

这一“结构注意力 → 聚合 → 时间注意力”的循环在 $N$ 对块中迭代执行，使模型能够深度编码关节间的结构关系与时间依赖，从而提取**任务特定的上下文自适应运动先验**。消融实验证实，优先聚合骨骼结构（即结构注意力在前）的设置带来最高重建精度，这也是最终 KAA 设计的依据。

### 输入输出流与任务适配

MMDM 的输入输出流根据下游任务灵活调整，无需改变核心网络结构：

- **运动补全**：输入为部分高质量关节与掩码低质量关节，输出为完整运动序列。自适应掩码策略依据 2D 置信度和三角测量误差计算掩码权重 $w_{j,t} = \omega \cdot e^{-\sum_{v=1}^{V} \rho_{j,v}^{t}} + \sigma_{j}^{t}$，在预训练阶段采用随机掩码（模式 A），微调阶段切换为加权自适应掩码（模式 C），掩码比例分别设为 0.5 和 0.3 时性能最优。

- **运动细化**：输入为低质量完整运动序列，逆扩散过程直接从含噪数据启动而非纯高斯噪声。训练损失 $\ell_{k}^{\mathrm{refine}} = \mathbb{E}_{k \sim \{1, K\}, \mathbf{d}_{k}} \left\| \mathbf{d}_{k} - \widehat{\mathbf{d}}_{k} \right\|_{2}$ 同时更新全序列，并采用滑动窗口捕获完整时间上下文。

- **运动插值**：输入由前驱段 $\mathbf{d}^{p}$、当前过渡段 $\mathbf{d}_{k}^{q}$、后继段 $\mathbf{d}^{r}$ 及文本嵌入 $\mathbf{v}$ 拼接而成，逆扩散步公式为 $\mathbf{d}_{k-1}^{q} = E_{\phi}(\mathbf{d}^{p} ++ \mathbf{d}_{k}^{q} ++ \mathbf{d}^{r} ++ \mathbf{v}, k)$，编码器直接预测下一状态。

### 与基线方法的架构差异

相比于现有方法，MMDM 在两个关键维度上实现了架构创新：

| 维度 | 基线方法 | MMDM |
|------|----------|------|
| 运动表示融合 | MAE 类方法（如 **D-MAE**, ACMMM 2022）仅从干净部分重建掩码区域，关节级与姿势级信息分离；扩散模型（如 **MDM**, ICLR 2023）以单一编码器处理完整运动 | KAA 通过可学习令牌将关节级结构信息聚合至姿势级，再经时间注意力建模，实现高效深度融合 |
| 扩散与掩码的结合 | MAE 不涉及扩散；**GMD**（ICCV 2023）、**MDM** 等扩散模型需完整输入进行去噪 | 将扩散过程嵌入 MAE 解码器，以未掩码部分为条件对掩码噪声输入进行条件逆扩散生成 |

这种设计使 MMDM 能够同时利用部分高质量数据的条件信息与扩散模型的生成能力，在运动补全、细化与插值任务上均取得了最优性能（详见实验部分 Table II–V）。



### 3.1 运动学注意力聚合（KAA）机制

MMDM 的核心创新在于运动学注意力聚合（Kinematic Attention Aggregation, KAA）机制，它解决了传统方法中关节级（joint-level）与姿势级（pose-level）表示相互割裂的问题。KAA 嵌入在运动学编码器（Kinematic Encoder）内部，该编码器由 $N$ 对自注意力模块堆叠而成，每对包含一个结构注意力（Structural Attention）块和一个时间注意力（Temporal Attention）块，二者通过 KAA 机制桥接。

**工作流程**：结构注意力块首先在关节维度上建模同一帧内各关节之间的骨骼空间关系；随后 KAA 通过一组可学习的聚合令牌（aggregation tokens），将关节级特征压缩并注入到姿势级表示中；最后时间注意力块沿时间轴建模姿势序列的动态依赖。这一“结构注意力 → 聚合 → 时间注意力”的循环在 $N$ 层中迭代执行，使模型能够深度编码时空运动特征，同时保持计算效率。

消融实验证实，**优先聚合骨骼结构（结构注意力在前）** 的配置带来最高重建精度，这成为最终 KAA 设计的依据。

### 3.2 掩码扩散模型（MMDM）架构

MMDM 采用编码器-解码器结构，将扩散生成范式嵌入掩码自编码器（MAE）的解码流程中。

**运动学编码器** $E_\phi$ 接收未掩码运动数据 $\mathbf{d}^{\overline{m}}$，输出两类表示：
- 未掩码运动令牌 $\mathbf{h}^{\overline{m}}$，保留可见关节的隐特征；
- 运动学条件 $c$，由 KAA 聚合后的姿势级上下文表示，用于指导解码器生成。

**运动解码器** $D_\theta$ 由 $N$ 个交叉注意力块组成，以拼接后的令牌 $[\mathbf{h}^{\overline{m}}; \mathbf{z}_k^m]$ 为输入，以条件 $c$ 为引导，在扩散步 $k$ 上预测去噪后的运动。其中 $\mathbf{z}_k^m$ 为掩码位置的噪声令牌。

**关键设计**：在每个逆扩散步，解码器输出的未掩码部分 $\widehat{\mathbf{d}}_k^{\overline{m}}$ 被直接替换为原始输入 $\mathbf{d}^{\overline{m}}$，确保可见关节的信息在去噪过程中不被污染，模型仅对掩码区域进行条件生成。

### 3.3 关键公式

**MAE 编码与解码**：

$$\mathbf{h}^{\overline{m}} = E_{\phi}(\mathbf{d}^{\overline{m}}) \tag{1}$$

$$\widehat{\mathbf{d}} = D_{\theta}(\mathbf{h}^{\overline{m}} \oplus \mathbf{z}^{m}) \tag{2}$$

其中 $\oplus$ 表示沿序列维度的拼接操作，$\mathbf{z}^{m}$ 为可学习的掩码嵌入向量。

**掩码扩散训练损失**：

$$\ell_k = \mathbb{E}_{k \sim \{1, K\}, \mathbf{d}_k^{m}} \left\| \mathbf{d}_k^{m} - \widehat{\mathbf{d}}_k^{m} \right\|_2 \tag{8}$$

该损失仅在掩码关节上计算，模型以未掩码部分为条件，学习从噪声中重建被遮挡或低质量关节的运动。

**自适应掩码权重**：

$$w_{j,t} = \omega \cdot e^{-\sum_{v=1}^{V} \rho_{j,v}^{t}} + \sigma_{j}^{t} \tag{9}$$

其中 $\rho_{j,v}^{t}$ 为第 $v$ 个视角下关节 $j$ 在时刻 $t$ 的 2D 置信度，$\sigma_j^t$ 为三角测量重投影误差，$\omega$ 为缩放因子。该权重综合了多视图 2D 检测置信度和 3D 三角化误差，使得低质量关节具有更高的掩码概率。

**运动细化损失**：

$$\ell_k^{\text{refine}} = \mathbb{E}_{k \sim \{1, K\}, \mathbf{d}_k} \left\| \mathbf{d}_k - \widehat{\mathbf{d}}_k \right\|_2 \tag{10}$$

与补全任务不同，细化任务的损失在**全部关节**上计算，同时更新掩码和未掩码部分，使模型能够全局优化运动序列质量。

**运动插值逆扩散步**：

$$\mathbf{d}_{k-1}^{q} = E_{\phi}(\mathbf{d}^{p} \oplus \mathbf{d}_k^{q} \oplus \mathbf{d}^{r} \oplus \mathbf{v}, k) \tag{11}$$

其中 $\mathbf{d}^p$ 和 $\mathbf{d}^r$ 分别为前驱和后继运动段，$\mathbf{d}_k^q$ 为当前扩散步的过渡段，$\mathbf{v}$ 为文本动作嵌入。编码器直接预测下一扩散步的状态，无需额外解码器，体现了 KAA 对多样化任务的自适应能力。

### 3.4 模块间的因果机制

KAA 是 MMDM 性能提升的**因果旋钮**：它通过可学习聚合令牌将关节级空间结构信息注入姿势级表示，再经时间注意力建模时序依赖，使编码器能够提取任务特定的上下文自适应运动先验。这一设计使得模型无需改变网络结构即可适应运动补全、细化与插值等任务——区别仅在于掩码策略和损失函数的作用范围。消融实验表明，扩散目标从预测噪声切换为预测信号时性能几乎不变（Shelf 上 PCP 98.47 vs 98.48），说明性能增益主要来自 KAA 的表示学习能力，而非扩散目标的特定选择。

### 补充图表

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/004_Figure_2.jpg]]
*Figure 2: Illustration of the reverse diffusion process in the proposed Masked Motion Diffusion Model (MMDM). It begins at iteration*



## 实验与关键发现

### 主实验结果

**运动捕获 (Motion Capture)**。在公开多视图基准 Shelf 和 Campus 上，MMDM 的平均 PCP 分别达到 **98.5±.15** 和 **97.6±.08**（Table II），均优于先前最优方法 JCSAT（TVCG 2025）的 98.2 和 97.3。在更具挑战性的 BUMocap 和 BUMocap-X 数据集上（Table III），MMDM 同样取得最优，其中 BUMocap-X 上的 PCP 领先 JCSAT 达 **3.6 个百分点**（92.1 vs. 88.5），表明模型在严重遮挡场景下的重建能力显著增强。

**运动细化 (Motion Refinement)**。Table IV 报告了 Shelf 数据集上的细化结果。MMDM 对初始运动捕获结果进行细化后，平均 PCP 从 97.0 提升至 98.1（Δ=+1.1%），其中遮挡最严重的 Actor 3 提升幅度最大（Δ=+2.2%），验证了扩散细化对低质量关节的有效修正。

**运动插值 (Motion In-betweening)**。在 BABEL-TEACH 数据集的 30 帧过渡任务上（Table V），MMDM 在所有指标上大幅超越先前方法：L2-P 降至 **0.0607**（MDM 为 0.2236，降幅 73%），L2-Q 降至 **0.0358**（降幅 75%），NPSS 降至 **0.2757**（降幅 76%）。这表明 KAA 机制提取的时空运动先验对长时过渡生成具有关键作用。

**计算效率**。Figure 6 展示了各方法在 BABEL-TEACH 上的 L2P-参数量权衡。MMDM 以较小的参数量取得最优插值质量，而 GMD（ICCV 2023）等方法的性能-计算比明显逊色。

### 消融实验

**KAA 聚合顺序**。Table VI（“MOCAP”数据）显示，优先聚合骨骼结构（结构注意力在前）的设置取得最高平均 PCP，验证了“先空间结构、后时间依赖”的聚合策略的有效性。

**掩码策略与比例**。Figure 5 系统消融了掩码模式与比例。结果表明：预训练采用模式 A（随机掩码），微调采用模式 C（加权自适应掩码）获得最佳性能；预训练掩码比 0.5、微调掩码比 0.3 为最优配置。自适应掩码权重 $w_{j,t} = \omega \cdot e^{-\sum_{v=1}^{V} \rho_{j,v}^{t}} + \sigma_{j}^{t}$（Eq. 9）使模型能根据 2D 置信度和三角测量误差动态屏蔽低质量关节。

**数据预处理**。质心归一化相比髋关节归一化使 Shelf 平均 PCP 从 93.9 提升至 98.5，揭示坐标系选择对运动重建精度的影响极为显著。

**扩散目标与模型规模**。Table III 显示，将扩散目标从预测噪声切换为预测信号（signal vs. noise）几乎不影响性能（98.47 vs. 98.48）。模型规模从 Normal 增至 Large 时性能提升微弱（98.48→98.52），表明 Normal 版本为最优结构设计。

**2D 姿态估计器泛化性**。Table IV 报告了使用 AlphaPose、SimCC、OpenPose 三种不同 2D 估计器的结果，性能波动极小，证明 MMDM 对前端 2D 姿态输入的强泛化能力。

### 定性分析

**运动捕获可视化**（Figure 3）。在 2D 投影和 3D 新视角渲染中，MMDM 重建的骨骼（蓝色/红色）与真值（绿色）高度吻合。红色虚线框标注了其他方法的失败案例——通常发生在严重遮挡或多人交叉区域——而 MMDM 在这些场景下仍能生成合理的姿态。

**运动插值可视化**（Figure 4）。灰色段表示给定的前驱与后继运动，彩虹渐变段（黄→紫）为生成的过渡序列。MMDM 生成的骨盆、肘、肩、膝及末端效应器轨迹最接近真值，而 MDM 等方法存在明显过平滑和抖动问题。

### 失败模式与限制

尽管 MMDM 在多数场景下表现优异，分析揭示了以下不足：

1. **推理效率**：扩散逆过程需数百步迭代，单次评估耗时超过 7 小时，难以满足实时应用需求。Table VI 中 DDIM 加速（5×/10×）可部分缓解，但性能有所下降。
2. **任务特异性**：补全、细化、插值任务需分别微调或调整架构，尚无法提供统一模型。
3. **极端遮挡鲁棒性**：当输入 2D 姿态面临严重漏检或误检时，仅依赖部分观测关节的条件生成仍可能产生不合理姿态。
4. **外部引导无效**：GMD 的强调投影与密集梯度传播技术对 MMDM 几乎无增益，暗示 KAA 本身已隐含类似的空间加权能力，但这一假设需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/007_Table.jpg]]
*Table: II MOTION CAPTURE PERFORMANCE ON SHELF AND CAMPUS DATASETS USING THE PCP (%) METRIC. “A-N” CORRESPONDS TO THE n-TH ACTOR, WHILE ‘AVG’ DENOTES THE AVERAGE PCP. ‘†’ INDICATES THE CORRECTED VALUE. BOLD INDICATES THE BEST PERFORMANCE; UNDERLINED INDICATES THE SECOND-BEST*

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/008_Table.jpg]]
*Table: III MOTION CAPTURE PERFORMANCE ON THE BUMOCAP (BU) AND BUMOCAP-X (BU-X) DATASETS. AVERAGE PCP (%), PRECISION (%), RECALL (%), AND MPJPE (MM) ARE REPORTED*

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/009_Table.jpg]]
*Table: IV QUANTITATIVE COMPARISONS FOR THE MOTION REFINEMENT TASK ON THE SHELF DATASET. WE REPORT THE RESULTS BEFORE AND AFTER REFINEMENT, WITH THE INCREMENTAL CHANGE ∆ (%)*

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/011_Table.jpg]]
*Table: V MOTION IN-BETWEENING RESULTS ON THE BABEL-TEACH DATASET. THE PERFORMANCE OF THE 30-FRAME TRANSITION IS REPORTED. MDM⋆ AND $\mathbf { M D M }$ _ ${ \star$ $\star }$ REPRESENT TWO MDM VARIANTS. 10×, 50×, 100× DENOTE RESULTS UNDER DDIM SAMPLING *

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/012_Table.jpg]]
*Table: VI MOTION REFINEMENTS RESULTS ON THE SHELF DATASET USING “MOCAP” DATA. 5× AND 10× DENOTE THE SPEED-UP RATIOS UNDER DDIM SAMPLING *

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/013_Figure_6.jpg]]
*Figure 6: Computational complexity and motion in-betweening performance of each model are evaluated on the BABEL-TEACH dataset [55] using the L2P metric. The size of the circle indicates the number of parameters, with a larger area representing a greater number*

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/010_Figure_5.jpg]]
*Figure 5: Ablation study for the motion refinement task. We report the average PCP on the Shelf dataset [51]. The line graphs depict: (a) horizontal axis for the fine-tune masking patterns, with lines showing pre-train masking patterns; (b) horizontal axis for fine-tune masking ratios, with lines showing pre-train masking ratios; (c) horizontal axis for diffusion steps*

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/003_Table.jpg]]
*Table: I COMPARISONS OF MOTION REPRESENTATION IN STATE-OF-THE-ART STUDIES, WITH THEIR OBJECTIVES: HUMAN POSE ESTIMATION (HPE), MOTION IN-BETWEENING (MIB), AND MOTION GENERATION (MG)*

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparisons for motion in-betweening task. Motion sequences are sampled into key poses at a fixed ratio. Grey segments illustrate preceding and succeeding parts, while the transitioning part is color-coded from yellow to purple in a rainbow gradient, indicating the chronological order. We emphasize the joint trajectories of the pelvis, elbows, shoulders, knees, and four end-effectors. Our model generates trajectories that are closest to the ground truth, whereas other methods suffer from issues such as over-smoothing and jitter*

![[assets/figures/papers/paper_list_l90_https_arxiv_org_abs_2603_07697/figures/016_Figure_1.jpg]]
*Figure 1: Demonstration for the reserve diffusion process at k time step. Green and blue skeletons denote the ground truth and the prediction, respectively. The masked joints are first sampled from a normal distribution and iteratively denoised*



## 定位与知识库关联

### 1. 问题定位与核心瓶颈

现有的基于视觉的运动捕捉方法在遮挡发生时难以准确重建3D人体运动。该问题的技术瓶颈在于三类主流范式的结构性缺陷：**掩码自编码器（MAE）** 仅能从干净的未掩码部分重建掩码区域，无法处理噪声输入；**运动扩散模型** 需要完整的噪声输入序列进行去噪生成，计算复杂且缺乏对部分观测的条件化机制；**多视图姿态估计方法** 虽能提取关节级时空特征，但缺乏将关节级信息高效聚合为姿势级表示的能力。MMDM正是在这一交叉缺口上提出——构建一个能同时处理部分含噪声输入、并高效融合关节级与姿势级表示的生成式重建框架。

### 2. 与基线工作的关系定位

**Table I** 系统梳理了现有工作在运动表示方式上的分野：人体姿态估计（HPE）相关方法（如 **4DAG** (CVPR 2020)、**D-MAE** (ACMMM 2022)、**JCSAT** (TVCG 2025)）倾向于提取关节级表示，在空间和时间维度上对关键关节建模；而运动生成方法（如 **MDM** (ICLR 2023)、**GMD** (ICCV 2023)）则采用姿势级表示，将完整姿态作为整体处理。MMDM通过KAA机制桥接了这两种表示层级——模型在关节级操作，通过可学习聚合令牌将结构信息汇聚到姿势级，再沿时间维度建模轨迹依赖。

具体而言，MMDM对以下基线工作形成了直接改进或对比：

- **D-MAE** (掩码自编码器运动补全)：MAE范式仅从干净未掩码部分重建，无法处理观测噪声。MMDM将扩散过程嵌入MAE解码器，以未掩码部分为条件对掩码噪声输入进行条件逆扩散生成，使模型具备噪声鲁棒性。
- **MDM** (运动扩散生成)：MDM需要完整序列输入进行去噪，缺乏对部分观测的条件化能力。MMDM通过掩码扩散范式，仅利用部分高质量数据条件生成缺失运动，在运动插值任务上L2-P从0.2236降至0.0607（降幅73%），NPSS从1.1508降至0.2757（降幅76%）（Table V）。
- **GMD** (引导运动扩散生成)：GMD引入强调投影与密集梯度传播作为引导信号。但该技术对MMDM的提升有限，暗示KAA机制本身可能已隐含了类似的空间加权能力，这是一个值得进一步探究的现象。
- **JCSAT** (多视图人体姿态估计)：作为多视图HPE的强基线，JCSAT在Shelf上取得98.2 PCP，Campus上取得97.3 PCP。MMDM在此基础上分别提升至98.5和97.6（Table II），在更具挑战性的BUMocap-X数据集上优势更为显著（92.1 vs 88.5，提升3.6个百分点，Table III）。
- **DiffPose** (扩散模型人体姿态估计)：同为扩散范式在姿态估计中的应用，但DiffPose面向单帧姿态估计，MMDM则将扩散生成扩展到运动序列的时空联合建模。

### 3. 方法谱系中的创新定位

MMDM的核心创新——**运动学注意力聚合（KAA）**——在方法谱系中占据独特位置。KAA通过在结构注意力和时间注意力之间桥接可学习的聚合令牌，迭代地深度编码关节间的结构关系与时间依赖。消融实验确认，优先聚合骨骼结构（结构注意力在前）的设置带来最高重建精度，这验证了“结构先于时序”的设计直觉。

在扩散生成与掩码重建的结合方式上，MMDM提出了不同于现有工作的融合策略：将扩散过程嵌入MAE解码器，以未掩码部分为条件，对掩码噪声输入进行条件逆扩散生成。这与传统的“MAE仅重建”或“扩散模型全序列去噪”形成了明确的范式差异（Fig. 1）。

掩码策略方面，MMDM引入基于2D置信度和三角误差的自适应加权掩码（式9），在预训练阶段采用随机掩码（模式A，掩码比0.5），微调阶段切换为加权自适应掩码（模式C，掩码比0.3），这一两阶段策略被消融实验证实为最优配置（Fig. 5）。

### 4. 适用边界与局限

**推理效率瓶颈**：扩散模型的逆过程需要数百步迭代，单次评估推理时间超过7小时，难以应用于实时运动捕获场景。Table VI显示，采用DDIM采样可在5×或10×加速下保持性能，但仍未达到实时要求。

**任务特异性需求**：MMDM针对运动补全、细化和插值三类任务需要分别进行微调或调整架构——补全任务使用自适应掩码策略，细化任务采用滑动窗口捕获完整时间上下文并更新全序列（式10），插值任务则修改编码器输入以拼接前驱、当前、后继及文本嵌入（式11）。目前尚不能提供统一的单个模型处理所有任务。

**极端遮挡下的鲁棒性**：当输入2D姿态估计面临严重漏检或误检时，仅依赖部分观测关节的条件生成仍可能出现不合理姿态。自适应掩码策略的鲁棒性在此类场景下有待进一步提升。

**GMD引导技术的无效性**：强调投影与密集梯度传播对MDM有效但对MMDM几乎无增益，这一现象的原因尚不明确，可能指向KAA与引导信号之间的功能重叠。

### 5. 开放问题

1. **推理加速**：能否进一步压缩扩散步数或采用更高效的采样策略（如一致性模型、蒸馏技术），将推理时间降低至秒级以满足实时运动捕获需求？
2. **统一框架设计**：如何设计端到端的统一框架，无需任务特定微调即可处理补全、细化、插值等多样化运动生成任务？
3. **KAA与空间加权的内在关系**：强调投影为何对MDM有效而对MMDM几乎无增益？这是否暗示KAA本身已隐含了类似的空间加权能力？需要进一步的机制分析。
4. **极端条件下的鲁棒性**：当输入2D姿态估计面临严重漏检或误检时，自适应掩码策略的鲁棒性如何进一步提升？是否需要引入不确定性建模或贝叶斯推断？
5. **跨数据集泛化**：Table IV显示使用不同2D姿态估计器（AlphaPose、SimCC、OpenPose）时性能波动很小，表明模型对2D输入源具有较强的泛化性。但这种泛化性在更大规模、更多样化的运动数据上是否仍然成立，尚需验证。



## 原文 PDF

![[paperPDFs/arxiv_2026/Learning_Context_Adaptive_Motion_Priors_for_Masked_Motion_Diffusion_Models_with_Efficient_Kinematic_Attention_Aggregation.pdf]]
