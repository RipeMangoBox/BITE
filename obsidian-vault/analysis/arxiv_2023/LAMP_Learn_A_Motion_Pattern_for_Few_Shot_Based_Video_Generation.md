---
title: "LAMP: Learn A Motion Pattern for Few-Shot-Based Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/LAMP_Learn_A_Motion_Pattern_for_Few_Shot_Based_Video_Generation.pdf
aliases:
- LAMP
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 第一帧条件化管道（first-frame-conditioned pipeline）与时间-空间运动学习层的引入，能够将运动模式与内容解耦，使模型仅从少量视频中学习通用运动规律。
primary_logic: 通过将文本到视频生成分解为第一帧的文本到图像生成（利用强大的 SD-XL）和基于第一帧的后续帧预测，并设计视频预测式的时间-空间卷积层和第一帧条件的自注意力，可以在 8~16 个视频、单 GPU 上学习特定的运动模式，同时保持内容多样性和语义泛化。
claims:
- 提出的第一帧条件化管道将 T2V 解耦为第一帧生成与后续帧预测，从而有效避免内容过拟合，提升生成自由度。
- 设计的时间-空间运动学习层同时捕获时间和空间特征，实现了视频预测式的帧间运动建模。
- 修改自注意力使后续帧的键和值均来自第一帧，并加入时间注意力，大幅增强帧间一致性。
- 共享噪声采样策略以极小的计算代价显著提升生成视频的稳定性。
---

# LAMP: Learn A Motion Pattern for Few-Shot-Based Video Generation

> [!tip] 核心洞察
> 通过将文本到视频生成分解为第一帧的文本到图像生成（利用强大的 SD-XL）和基于第一帧的后续帧预测，并设计视频预测式的时间-空间卷积层和第一帧条件的自注意力，可以在 8~16 个视频、单 GPU 上学习特定的运动模式，同时保持内容多样性和语义泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | LAMP：面向少样本视频生成的运动模式学习 |
| 英文题名 | LAMP: Learn A Motion Pattern for Few-Shot-Based Video Generation |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2310.10769) · [Project](https://rq-wu.github.io/projects/LAMP) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | LAMP |
| Dataset | Custom evaluation set, User study |

> [!tip] 效果简介
> - Custom evaluation set 上，Alignment 31.3547 (best)；Consistency 98.3085 (best)；Diversity 71.6535 (best)。
> - User study 上，Preference rate 46.84% vs AnimateDiff 19.11%, Tune-A-Video 22.15% (+24.69% over Tune-A-Video)。

## 概述

**核心问题：** 少样本视频生成面临双重困境——训练数据极度受限（8~16 个视频）时，模型极易过拟合视频内容，丧失生成多样性；同时，从有限样本中分离并学习可泛化的运动模式，对纯空间生成模型构成根本性挑战。

**方法定位：** LAMP 提出一种少样本微调框架，将文本到视频生成（T2V）解耦为两个阶段：第一帧的文本到图像生成（利用现成的 **SD-XL**），以及基于第一帧的后续帧预测。通过设计**第一帧条件化训练管道**、**时间-空间运动学习层**和**修改的自注意力机制**，LAMP 仅需在单 GPU 上使用 8~16 个视频即可学习特定运动模式，同时保持内容多样性和语义泛化能力。

**核心结果：** 在自定义评估集上，LAMP 在 Alignment（31.35）、Consistency（98.31）、Diversity（71.65）三项指标上均取得最优；用户偏好率（46.84%）显著优于 **AnimateDiff**（Guo et al., 2023）的 19.11% 和 **Tune-A-Video**（Wu et al., ICCV 2023）的 22.15%。消融实验证实，第一帧条件化管道是避免内容过拟合的关键，时间-空间运动层是帧间运动建模的瓶颈组件，共享噪声采样则以极小代价提升推理稳定性。

## 背景与动机

### 视频生成的范式瓶颈

近年来，文本到图像（T2I）扩散模型取得了令人瞩目的进展，然而文本到视频（T2V）生成仍面临两个核心瓶颈。其一，**内容过拟合**：在少样本设定下，模型极易记住训练视频的静态内容，丧失生成多样性。其二，**运动模式分离困难**：纯空间模型难以有效预测帧间运动并保持时间一致性，导致生成的视频缺乏连贯的动态表现。

现有方法尝试从不同角度缓解上述问题。**Tune-A-Video**（Wu et al., ICCV 2023）通过对单个视频进行微调实现视频编辑，但难以泛化到新的文本提示。**Text2Video-Zero**（Khachatryan et al., arXiv 2023）无需训练即可生成视频，却牺牲了运动质量与帧间一致性。**AnimateDiff**（Guo et al., arXiv 2023）在大规模视频数据上训练运动模块，但需要大量计算资源，且在特定运动模式的精确控制方面能力有限。这些方法的共性缺口在于：**缺乏一种在极少量视频（8～16 个）和单 GPU 资源下，既能学习特定运动模式，又能保持内容多样性与语义泛化能力的统一框架。**

### LAMP 的核心动机与因果调控

**LAMP** 的核心动机源于一个关键洞察：将 T2V 生成解耦为**第一帧的内容生成**与**后续帧的运动预测**，可以从因果层面切断内容与运动的纠缠。这一设计形成了两个关键调控节点：

1. **第一帧条件化管道**：利用强大的现成 T2I 模型（如 SD-XL）生成高质量的第一帧，扩散模型的去噪过程仅作用于第 2 至第 $l$ 帧。这从训练目标上避免了对视频内容的过拟合，使模型专注于运动模式的学习。

2. **时间-空间运动学习层**：在预训练的空间卷积层上引入 1D 时间卷积分支，以视频预测的方式（利用前两帧预测当前帧）同时捕获时间与空间特征，从根本上解决了纯空间模型无法建模帧间运动的问题。

通过上述因果调控，LAMP 在 8～16 个视频、单 GPU 的条件下即可学习特定的运动模式，同时保留了扩散模型良好的语义泛化特性——例如，可以将“微笑”的运动模式施加到训练集中未曾出现的漫画风格上（Figure 1）。这一设计在训练资源与生成自由度之间实现了有效的平衡。

## 核心创新

LAMP 的核心创新在于将少样本视频生成重新定义为一个**内容-运动解耦问题**，并通过三个紧密耦合的机制实现：第一帧条件化训练管道、时间-空间运动学习层，以及修改后的自注意力与共享噪声采样策略。这些创新直接回应了少样本场景下的根本瓶颈——训练数据有限时，模型极易同时记住视频内容与运动模式，导致生成多样性丧失。

### 内容-运动解耦：第一帧条件化管道

传统的文本到视频（T2V）扩散模型在训练时对所有帧统一添加噪声并计算损失，这使得模型必须同时学习“生成什么内容”和“如何运动”。在仅 8~16 个视频的少样本条件下，这种耦合必然导致严重的内容过拟合——模型只能复现训练视频中的特定物体和场景。

LAMP 的**第一帧条件化管道**（first-frame-conditioned pipeline）将这一耦合拆解：训练时，仅对第 2 至第 *l* 帧添加噪声并计算损失，第一帧保持原始信号不变。训练目标从标准扩散损失变为：

$$\mathcal{L} = \mathbb{E}_{\mathcal{Z}, \epsilon \sim \mathcal{N}(0, I), t, c} \left[ \left\| \epsilon^{2:l} - \epsilon_{\theta}^{2:l}(\mathcal{Z}_t, t, c) \right\|_2^2 \right]$$

这一公式（Eq. 4, Section 3.3）的含义是：模型仅需学习“给定第一帧，预测后续帧的噪声”，而无需建模第一帧的内容本身。推理时，第一帧由独立的文本到图像模型（SD-XL）生成，微调后的视频扩散模型仅负责基于该第一帧预测后续帧的运动。这种管道设计将内容生成的自由度完全交给了强大的 T2I 模型，而运动学习被限制在少样本视频中提取的通用运动规律上，从根本上避免了内容过拟合。

### 运动建模：时间-空间运动学习层

仅解耦内容与运动还不够——模型还需要有效捕获帧间的时空运动特征。LAMP 在预训练的 2D 卷积层上扩展出**时间-空间运动学习层**（Figure 3, Section 3.4），该层包含两个并行分支：

- **1D 时间卷积分支**：沿时间维度捕获帧间动态，且以视频预测方式工作——利用前两帧预测当前帧；
- **2D 空间卷积分支**：输出通道数为 1，控制空间层面的运动强度。

这种设计使得运动学习同时覆盖时间连续性和空间形变，而非简单地在预训练空间层上叠加时序模块。消融实验（Figure 5b）表明，移除该层直接导致帧间运动完全失败，验证了其对运动建模的必要性。

### 帧间一致性：修改的自注意力与共享噪声

运动学习层的输出需要被后续帧有效利用。LAMP 对标准自注意力进行了关键修改（Eq. 5, Section 3.4）：

$$\operatorname{Attention}(Q^i, K^1, V^1) = \operatorname{Softmax}\left( \frac{Q^i (K^1)^T}{\sqrt{d}} \right) V^1$$

其中，第 *i* 帧的查询 $Q^i$ 保持不变，但键 $K^1$ 和值 $V^1$ 均来自第一帧。这强制每个后续帧在生成时参考第一帧的外观和结构信息，从而大幅增强帧间一致性。同时，沿时间维度插入的时间自注意力层进一步促进跨帧交互。

在推理阶段，LAMP 引入**共享噪声采样**策略（Section 3.5）：每帧的初始噪声由共享噪声 $\epsilon^s$ 和独立噪声 $\epsilon^i$ 加权组合：

$$\epsilon^i = \alpha \epsilon^s + (1 - \alpha) \epsilon^i, \quad \alpha = 0.2$$

这一设计以极小的计算代价（仅需额外生成一个共享噪声张量）显著降低了帧间抖动，提升了生成视频的时序稳定性。消融实验（Figure 5c）显示，移除共享噪声后视频出现明显抖动。

### 创新总结

| 创新组件 | 解决的问题 | 与 baseline 的关键差异 |
|---------|-----------|---------------------|
| 第一帧条件化管道 | 内容过拟合，生成多样性丧失 | 仅对第 2~*l* 帧加噪训练，第一帧由 T2I 模型生成 |
| 时间-空间运动学习层 | 帧间运动建模困难 | 在 2D 卷积上扩展 1D 时间分支 + 2D 空间强度控制，以视频预测方式工作 |
| 修改的自注意力 | 帧间外观不一致 | 键和值均来自第一帧，强制后续帧参考第一帧 |
| 共享噪声采样 | 推理时视频抖动 | 共享噪声与独立噪声加权混合，$\alpha=0.2$ |

这些创新共同实现了在单 GPU、8~16 个视频的条件下学习特定运动模式，同时保持内容多样性和语义泛化能力——例如，将“微笑”的运动模式施加到训练中未见过的漫画风格角色上（Figure 1）。

## 整体框架

LAMP 的整体 pipeline 将文本到视频（T2V）生成解耦为两个阶段：**第一帧的内容生成** 与 **后续帧的运动预测**。这一设计直击少样本视频生成的核心瓶颈——训练数据有限时，模型极易同时记住视频的内容与运动，导致生成多样性丧失。通过将内容生成外包给一个冻结的强大 T2I 模型，LAMP 的微调部分仅需专注于学习运动模式，从而在 8~16 个视频、单 GPU 的条件下实现内容自由与运动保真度的平衡。

### Pipeline 总览

如图 2 所示，整个框架包含训练与推理两条路径，二者共享核心的去噪网络，但在第一帧的来源上存在根本差异。

**训练阶段**：输入为一个包含 $l$ 帧的视频序列。所有帧首先通过预训练的 VAE 编码器映射到潜在空间，得到潜在特征序列 $\mathcal{Z} = \{z^1, z^2, \dots, z^l\}$。随后，扩散过程仅对第 2 至 $l$ 帧添加噪声，保留第一帧的原始信号。去噪 U-Net 接收噪声化的后续帧特征与干净的第一帧特征，在文本条件 $c$（即运动描述 prompt）的引导下预测添加的噪声。训练损失仅计算在后续帧上：

$$
\mathcal{L} = \mathbb{E}_{\mathcal{Z}, \epsilon \sim \mathcal{N}(0, I), t, c} \left[ \left\| \epsilon^{2:l} - \epsilon_{\theta}^{2:l}(\mathcal{Z}_t, t, c) \right\|_2^2 \right]
$$

这一“第一帧条件化”的训练策略（Eq. 4, Section 3.3）是内容-运动解耦的关键：模型从未见过第一帧被噪声破坏的情形，因此无法将运动模式与第一帧的特定内容绑定，迫使它学习独立于内容的帧间变化规律。

**推理阶段**：流程反转。用户提供一个视频内容 prompt 和一个运动 prompt。首先，使用现成的 SD-XL 模型根据内容 prompt 生成第一帧 $I^1$，经 VAE 编码得到 $z^1$。随后，对后续 $l-1$ 帧初始化随机噪声，将 $z^1$ 与噪声化的后续帧特征拼接，送入微调后的去噪 U-Net。U-Net 在运动 prompt 的引导下，以第一帧为条件逐步去噪，生成后续帧的潜在特征。最终，所有帧的潜在特征通过 VAE 解码器恢复为像素空间视频。

### 模块关系与数据流

去噪 U-Net 内部集成了三个关键的架构修改，它们协同工作以实现运动学习与帧间一致性：

1. **时间-空间运动学习层**（Figure 3, Section 3.4）：在预训练的 2D 卷积层之上，并行添加 1D 时间卷积分支。1D 卷积沿时间维度滑动，利用前两帧的特征预测当前帧，显式建模帧间运动动态；同时保留 2D 空间卷积分支以维持空间细节。这种双分支设计使网络能够同时捕获运动的时间演化与空间形变。

2. **修改的自注意力层**（Eq. 5, Section 3.4）：标准自注意力中，查询（Q）、键（K）、值（V）均来自同一帧。LAMP 将其修改为：查询 $Q^i$ 来自当前第 $i$ 帧，而键 $K^1$ 和值 $V^1$ 均来自第一帧：

   $$
   \operatorname{Attention}(Q^i, K^1, V^1) = \operatorname{Softmax}\left( \frac{Q^i (K^1)^T}{\sqrt{d}} \right) V^1
   $$

   这强制每一帧在生成时“回顾”第一帧的外观与结构信息，从注意力层面保证了帧间一致性。

3. **时间注意力层**（Section 3.4）：在空间自注意力之后插入沿时间维度的自注意力层，使不同帧的同一空间位置能够直接交互，进一步增强时序连贯性。

### 推理阶段的稳定性增强

推理时，LAMP 引入**共享噪声采样策略**（Section 3.5）：各帧的初始噪声 $\epsilon^i$ 由共享噪声 $\epsilon^s$ 与独立噪声加权混合得到：

$$
\epsilon^{i} = \alpha \epsilon^{s} + (1 - \alpha) \epsilon^{i}, \quad \alpha = 0.2
$$

这一策略以极小的计算代价显著降低了视频的帧间抖动。此外，推理后处理阶段采用 **AdaIN 与直方图匹配**对生成帧进行色彩一致性校正（Section 3.5），进一步提升视觉连贯性。

### 关键设计意图

整个框架的核心设计意图在于**最小化可训练参数与所需数据量**，同时最大化生成自由度。训练时仅更新新增的时间-空间运动层、时间注意力层以及自注意力模块中的查询线性投影层，其余预训练权重全部冻结。这使得 LAMP 能够在 8~16 个视频上快速微调，且第一帧由 SD-XL 独立生成，保证了内容语义的泛化能力——模型可以将学到的运动模式（如“奔跑”）迁移到训练集中从未出现过的物体或风格上（如卡通风格的狗），这正是 Figure 1 所展示的核心优势。

> **证据强度说明**：第一帧条件化管道（confidence 0.95）与时间-空间运动学习层（confidence 0.95）均有明确的公式与消融实验支撑；共享噪声采样策略的消融证据稍弱（confidence 0.85），但仍可观察到明显的稳定性改善。复杂运动场景下的表现需要结合局限性部分综合评估。

### 补充图表

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2310_10769/figures/002_Figure_2.jpg]]
*Figure 2: Framework of LAMP. LAMP learns a motion pattern from a small video set, enabling the generation of videos imbued with the learned motion patterns. This approach strikes a balance between training resources and generation freedom in video generation. We transfer text-to-video generation to the first-frame generation and subsequent-frame prediction, i.e., decoupling a video’s contents and motions. During training, we add noise and compute loss functions for all frames except the first frame. Moreover, only the parameters of newly added layers and the query linear layers of self-attention blocks are tuned. During inference, we use a T2I model to generate the first frame. The tuned model only w...*

## 核心模块与公式推导

LAMP 的核心设计围绕一个关键洞察展开：将文本到视频生成解耦为**第一帧内容生成**与**后续帧运动预测**两个独立阶段。这一解耦通过若干精心设计的模块实现，本节逐一剖析其机制与公式表达。

### 3.1 扩散模型基础

LAMP 构建于扩散模型框架之上。给定干净视频潜在表示 $x_0$，前向扩散过程逐步添加高斯噪声，其单步转移为：

$$q ( x _ { t } | x _ { t - 1 } ) = N ( x _ { t } ; \sqrt { 1 - \beta _ { t } } x _ { t - 1 } , \beta _ { t } I )$$

其中 $\beta_t$ 为噪声调度参数。利用重参数化技巧，任意时间步 $t$ 的噪声样本可直接从 $x_0$ 获得：

$$x _ { t } = \sqrt { \bar{\alpha} _ { t } } x _ { 0 } + \sqrt { 1 - \bar{\alpha} _ { t } } \epsilon , \quad \epsilon \sim \mathcal { N } ( 0 , I )$$

其中 $\bar{\alpha}_t = \prod_{s=1}^t (1-\beta_s)$。模型 $\epsilon_\theta$ 学习预测添加的噪声，训练目标为：

$$\underset { \theta } { \arg \operatorname* { m i n } } \mathbb { E } _ { \boldsymbol { x } _ { 0 } , \boldsymbol { \epsilon } \sim \mathcal { N } ( \boldsymbol { 0 } , \boldsymbol { I } ) , \boldsymbol { t } , \boldsymbol { c } } [ | | \boldsymbol { \epsilon } - \boldsymbol { \epsilon } _ { \theta } ( \boldsymbol { x } _ { t } , t , \boldsymbol { c } ) | | _ { 2 } ^ { 2 } ]$$

其中 $c$ 为条件信息（如文本提示）。

### 3.2 第一帧条件化管道

这是 LAMP 最关键的机制创新。传统 T2V 方法对所有帧均匀添加噪声并计算损失，在少样本场景下极易导致模型同时记忆视频内容与运动模式，丧失生成多样性。LAMP 的解决方案是**仅对第 2 至 $l$ 帧添加噪声并计算损失，保留第一帧的原始信号**：

$$\mathcal { L } = \mathbb { E } _ { \mathcal { Z } , \epsilon \sim \mathcal { N } ( 0 , I ) , t , c } [ | | \epsilon ^ { 2 : l } - \epsilon _ { \theta } ^ { 2 : l } ( \mathcal { Z } _ { t } , t , c ) | | _ { 2 } ^ { 2 } ]$$

其中 $\mathcal{Z}_t$ 为加噪后的视频潜在表示，$\epsilon^{2:l}$ 和 $\epsilon_\theta^{2:l}$ 分别表示仅作用于第 2 至 $l$ 帧的真实噪声与预测噪声。这一设计的因果机制在于：第一帧作为未受噪声破坏的“锚点”，为后续帧提供稳定的内容参考；模型只需学习“给定第一帧，如何生成连贯的后续帧”这一运动预测任务，从而将运动模式与具体内容解耦。推理时，第一帧由强大的 SD-XL 文本到图像模型生成，微调后的视频扩散模型仅负责去噪后续帧。

### 3.3 时间-空间运动学习层

为同时捕获帧间时序依赖与帧内空间结构，LAMP 设计了专门的时间-空间运动学习层（Figure 3），在预训练 2D 卷积层基础上扩展两个分支：

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2310_10769/figures/003_Figure_3.jpg]]
*Figure 3: The details of the proposed temporal-spatial motion layers. (b) illustrates that 1D convolutions are added on pre-trained layers to capture information along the temporal dimension. 2D convolution layers with an output channel number of 1 control the spatial level’s motion strength. The 1D convolutional layers utilize the former two frames to generate the current frame, as shown in (a)*

- **1D 时间卷积分支**：沿时间维度操作，利用前两帧预测当前帧，实现视频预测式的运动建模。
- **2D 空间卷积分支**：输出通道数为 1，控制空间层面的运动强度。

这种设计使运动学习层既能捕捉“物体如何移动”的时序规律，又能保留“移动发生在画面何处”的空间信息，相比纯时序或纯空间建模具有更强的运动表征能力。消融实验（Figure 5b）证实，移除此层将导致帧间运动完全失败。

### 3.4 修改的自注意力与时间注意力

为确保后续帧在生成过程中持续参考第一帧的外观信息，LAMP 对标准自注意力进行了关键修改：**键（Key）和值（Value）均取自第一帧**，仅查询（Query）来自当前帧：

$$\operatorname { A t t e n t i o n } ( Q ^ { i } , K ^ { 1 } , V ^ { 1 } ) = \operatorname { S o f t m a x } ( \frac { Q ^ { i } ( K ^ { 1 } ) ^ { T } } { \sqrt { d } } ) V ^ { 1 }$$

其中 $Q^i$ 为第 $i$ 帧的查询，$K^1$、$V^1$ 为第一帧的键和值，$d$ 为特征维度。这一机制强制每一后续帧在生成时“查询”第一帧的内容特征，从而大幅增强帧间外观一致性。

此外，LAMP 沿时间维度插入**时间自注意力层**，使不同帧的特征在时间轴上直接交互，进一步强化运动连贯性。

### 3.5 共享噪声采样

推理阶段，传统方法为各帧独立采样高斯噪声，容易引入帧间随机抖动。LAMP 采用共享噪声策略，将第 $i$ 帧的初始噪声构造为共享噪声与独立噪声的加权组合：

$$\epsilon^{i} = \alpha \epsilon^{s} + (1 - \alpha) \epsilon^{i}$$

其中 $\epsilon^s$ 为所有帧共享的噪声，$\alpha=0.2$ 控制共享程度。这一策略以几乎零额外计算代价显著提升生成视频的时序稳定性（消融见 Figure 5c）。

### 3.6 后处理：AdaIN 与直方图匹配

为进一步提升色彩一致性，LAMP 在推理后对生成帧应用自适应实例归一化（AdaIN）与直方图匹配，将后续帧的色彩分布对齐到第一帧。消融实验表明移除此步骤会降低色彩连贯性，但该模块属于轻量后处理，不参与核心运动学习。

## 实验与分析

### 主实验结果

LAMP 在自定义评估集上取得了 **Alignment** 31.3547、**Consistency** 98.3085、**Diversity** 71.6535 的三项最优指标（Table 1），全面优于对比基线。在用户研究中，LAMP 获得了 **46.84%** 的偏好率，显著高于 **AnimateDiff**（Guo et al., arXiv 2023）的 19.11% 和 **Tune-A-Video**（Wu et al., ICCV 2023）的 22.15%，领先幅度达 +24.69 个百分点（Sec. 4.3）。定性对比（Figure 4）进一步显示，LAMP 生成的视频在时序一致性和运动自然度上均优于三个基线方法，而 **Text2Video-Zero**（Khachatryan et al., arXiv 2023）等基线在帧间过渡和内容保真度上存在明显不足。

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2310_10769/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons with the evaluated text-tovideo methods*

### 消融实验

Figure 5 展示了各关键组件的消融效果：

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2310_10769/figures/006_Figure_5.jpg]]
*Figure 5: Ablation results. The given prompt is ‘A red horse runs in the sky’*

- **移除第一帧条件化管道（w/o first-frame-condition）**：视频内容出现严重过拟合，模型几乎完全复制训练视频的外观，丧失生成多样性（Figure 5a）。
- **移除时间-空间运动学习层（w/o temp-spatial layer）**：帧间运动完全失败，视频呈现静止或随机抖动，无法形成连贯的运动模式（Figure 5b）。
- **移除共享噪声采样策略（w/o shared-noise）**：视频出现明显抖动，帧间稳定性显著降低（Figure 5c），验证了共享噪声以极小的计算代价（α=0.2 的加权混合）提升推理稳定性的有效性。
- **移除 AdaIN 后处理**：色彩一致性有所下降（Sec. 3.5），但该组件对整体质量的影响相对次要。

### 失败模式与局限性

尽管 LAMP 在少样本运动学习上表现突出，仍存在以下失败模式：

1. **复杂运动学习困难**：当训练视频包含大幅度物体交互或快速运动时，模型偶尔无法准确捕捉运动模式，生成的视频出现运动失真或语义偏差。
2. **前景-背景运动耦合**：前景物体的运动有时会干扰背景的稳定性，导致背景出现不自然的抖动或漂移，表明模型缺乏对前景和背景运动的独立建模能力。
3. **极端少样本下的泛化瓶颈**：训练视频数量仅为 8~16 个，在特定场景下泛化能力可能受限，尤其是当测试提示与训练视频的语义分布差异较大时。

### 应用拓展

LAMP 的第一帧条件化管道天然支持两类下游应用：

- **真实图像动画化**（Figure 7）：以真实图像作为第一帧，调优后的网络预测后续帧，将学习到的运动模式施加于静态图像。
- **视频编辑**（Figure 6）：结合 **ControlNet** 和 **DDIM inversion**，对第一帧进行可控编辑后，利用 LAMP 的运动先验生成编辑后的视频序列。

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2310_10769/figures/007_Figure_6.jpg]]
*Figure 6: Visual results of our video editing application. Zoom in for the best view*

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2310_10769/figures/008_Figure_7.jpg]]
*Figure 7: Visual results of LAMP animates the real-world images*

### 待解决问题

基于上述失败模式，以下方向值得进一步探索：设计更强的运动学习模块以处理复杂运动；独立建模前景和背景运动以稳定背景；确定少样本视频扩散训练的最少数据需求；以及将方法推广到更长、更高分辨率的视频生成。

### 补充图表

![[assets/figures/papers/paper_list_l1048_https_arxiv_org_abs_2310_10769/figures/001_Figure_1.jpg]]
*Figure 1: Our text-to-video results. The motion prompts and video prompts are listed, respectively. Our LAMP works effectively on diverse motions. The generated videos are temporal consistent and close to the video prompts. Moreover, two advantages of LAMP can be reflected in the above results. (1) The proposed first-frame-conditioned training strategy allows us to use powerful SD-XL for first-frame generation, which is beneficial to producing highly detailed following frames. (2) Good semantic generalization properties of the diffusion model are preserved (e.g. imposing smile’s motion on unseen comic style) since our tuning way*

## 方法谱系与知识库定位

### 技术路线定位

LAMP 处于**少样本视频扩散微调**这一新兴技术路线上，其核心思想是将文本到视频（T2V）生成解耦为“第一帧的文本到图像生成”与“基于第一帧的后续帧预测”两个阶段。这一设计与现有方法形成鲜明对比：

- **Tune-A-Video** (Wu et al., ICCV 2023) 采用单视频微调策略，通过对一个视频的过拟合来学习其运动模式，但内容多样性严重受限。LAMP 通过第一帧条件化管道，将内容生成外包给 SD-XL，仅让视频扩散模型学习运动模式，从而在 8~16 个视频上即可保持内容泛化能力。
- **AnimateDiff** (Guo et al., arXiv 2023) 在大规模视频数据上训练通用时间模块，追求“万能运动先验”，但需要大量计算资源且难以针对特定运动模式定制。LAMP 则走向相反方向：在单 GPU 上用极少视频学习一个特定运动模式，在“训练成本”与“生成自由度”之间取得平衡。
- **Text2Video-Zero** (Khachatryan et al., arXiv 2023) 是免训练方法，通过潜空间操作模拟运动，但时间一致性和运动真实感较弱。LAMP 通过时间-空间运动学习层和修改后的自注意力机制，在帧间一致性上显著优于免训练方案。

从知识库角度看，LAMP 的关键贡献在于证明：**扩散模型中的运动模式与内容可以在低数据量下有效解耦**。其设计的三个核心机制——第一帧条件化训练损失（Eq. 4）、时间-空间运动学习层（Figure 3）、修改后的自注意力（Eq. 5）——共同构成了一套完整的少样本运动学习方案。

### 适用边界

**有效域：**
- 训练视频数量：8~16 个视频，单 GPU 可完成微调。
- 运动类型：重复性、周期性或具有明确模式的动作（如“马奔跑”“鸟飞翔”“火燃烧”），模型能够从少量样本中提取通用运动规律。
- 内容泛化：由于第一帧由 SD-XL 生成，LAMP 可以将学到的运动模式施加到训练集未见的物体、风格和场景上（Figure 1 展示了将“微笑”运动施加到未见漫画风格的能力）。
- 应用场景：文本驱动的视频生成、真实图像动画化（Figure 7）、视频编辑（Figure 6，结合 ControlNet 和 DDIM 反演）。

**失效域与局限（需手动验证）：**
- **复杂运动学习成功率下降**：当运动涉及大幅度物体交互、遮挡或非线性变形时，模型偶尔无法准确捕捉运动模式。这是时间-空间运动学习层表达能力的天花板。
- **前景-背景运动耦合**：前景物体的运动有时会干扰背景的稳定性，产生不自然的背景抖动。当前设计缺乏对前景和背景运动的独立建模机制。
- **数据量敏感**：训练视频数量极少（8~16 个）意味着特定场景下的泛化能力可能受限——如果训练视频的多样性不足以覆盖目标运动的变化，生成质量会下降。
- **分辨率与时长限制**：论文未验证该方法在更长视频（如超过 16 帧）或更高分辨率下的扩展性，这需要进一步验证。

### 开放问题

1. **复杂运动建模**：如何设计更强大的运动学习模块（如引入光流先验、可变形卷积或运动解耦表示）以处理大幅度、非线性的复杂运动？
2. **前景-背景解耦**：如何独立建模前景物体的运动和背景的稳定性，避免前景运动对背景的“拖拽”效应？
3. **最少数据量边界**：少样本视频扩散训练所需的最少视频数量是多少？运动模式的复杂度与所需数据量之间的关系是什么？
4. **长视频与高分辨率扩展**：如何将当前方法推广到更长时序（如 32 帧以上）和更高空间分辨率的视频生成，同时保持时间一致性？
5. **多运动模式组合**：能否在一个模型中同时学习多个运动模式，并在推理时通过条件控制来组合或切换？

## 原文 PDF

![[paperPDFs/arxiv_2023/LAMP_Learn_A_Motion_Pattern_for_Few_Shot_Based_Video_Generation.pdf]]