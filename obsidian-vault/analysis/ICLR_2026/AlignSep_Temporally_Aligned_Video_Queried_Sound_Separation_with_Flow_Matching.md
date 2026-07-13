---
title: "AlignSep: Temporally-Aligned Video-Queried Sound Separation with Flow Matching"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AlignSep_Temporally_Aligned_Video_Queried_Sound_Separation_with_Flow_Matching.pdf
project_link: https://AlignSep.github.io
code_link: null
openreview_forum_id: DVDkFcxU1D
aliases:
- AlignSep
tags:
- ICLR_2026
- topic/time_series_dynamical_systems
- topic/time_series_dynamical_systems/time_series_forecasting
core_operator: "使用条件流匹配进行生成式分离，并通过专门的时间连接机制和视觉时间编码器（CAVP）强制执行视听时间对齐。"
primary_logic: "生成式时间对齐框架能够明确利用视觉时间线索来区分同质音频源，同时缓解掩码方法固有的频谱空洞问题。"
claims:
- "AlignSep 是第一个基于流匹配的生成式 VQSS 模型，并采用时间连接策略。"
- "在 VGGSound-Hard 基准测试上，AlignSep 实现了 95.76% 的 T_A-V 时间一致性，远超所有基线方法。"
- "移除时间视觉编码器 (CAVP) 导致 VGGSound-Hard 上 T_A-V 下降 19.49 点，证明时间理解是关键。"
- "与交叉注意力相比，拼接融合策略在 VGGSound-Hard 上 T_A-V 提升了 22.38 点。"
---

# AlignSep: Temporally-Aligned Video-Queried Sound Separation with Flow Matching

> [!tip] 核心洞察
> 生成式时间对齐框架能够明确利用视觉时间线索来区分同质音频源，同时缓解掩码方法固有的频谱空洞问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AlignSep：基于流匹配的时间对齐视频查询声源分离 |
| 英文题名 | AlignSep: Temporally-Aligned Video-Queried Sound Separation with Flow Matching |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=DVDkFcxU1D) · [Project](https://AlignSep.github.io) |
| Topic | #topic/time_series_dynamical_systems #topic/time_series_dynamical_systems/time_series_forecasting |
| Method | AlignSep |
| Dataset | VGGSound-Hard, VGGSound-Clean |

> [!tip] 效果简介
> - VGGSound-Hard 上，T_A-V (时间一致性) 为 95.76，对比 OmniSep (76.27)，变化 +19.49。
> - VGGSound-Hard 上，MOS (Overall) 为 4.43，对比 OmniSep (4.07)，变化 +0.36。
> - VGGSound-Clean 上，S_A-A (语义一致性) 为 73.38，对比 OmniSep (70.83)，变化 +2.55。

## 概要

视频查询声源分离 (VQSS) 旨在从混合音频中提取与特定视频画面相对应的声音。现有方法面临一个核心瓶颈：**依赖语义类别标签的掩码判别模型缺乏时间建模能力，在面对同质干扰（如多只狗同时吠叫）和频谱重叠时，常产生不完整的分离结果和频谱空洞伪影**。AlignSep 通过条件流匹配框架将 VQSS 重构为生成式时间对齐任务，其核心洞见在于：**生成式时间对齐框架能够明确利用视觉时间线索来区分同质音频源，同时缓解掩码方法固有的频谱空洞问题**。

在方法定位上，AlignSep 是首个基于流匹配的生成式 VQSS 模型，通过三项关键设计区别于现有工作：用条件流匹配替代掩码判别模型或扩散模型进行生成式分离；引入 CAVP 视觉时间编码器提取时间同步的视频特征；采用时间拼接融合策略替代交叉注意力，在无交叉注意力的前馈 Transformer 中强制执行视听时间对应关系。推理时通过欧拉方法迭代求解 ODE，配合无分类器引导（尺度 s=4.5）平衡质量与多样性。

主要实验结果验证了设计的有效性：在 VGGSound-Hard 基准上，AlignSep 实现了 **95.76% 的 T_A-V 时间一致性**，较最优基线 OmniSep（76.27%）提升 19.49 点；主观 MOS 综合评分达 4.43（OmniSep 为 4.07）。消融实验进一步揭示因果机制——移除 CAVP 视觉时间编码器导致 T_A-V 骤降 19.49 点，证明时间理解而非生成模型选择是时间一致性的核心驱动力；拼接融合在 VGGSound-Hard 上 T_A-V 达 95.76，而交叉注意力仅 73.38，差距达 22.38 点，表明**强制的时间对应关系对区分同质源至关重要**。定性分析（Figure 4）显示，流匹配生成式框架有效缓解了掩码基线中的频谱空洞问题，产生更完整的频谱。

需注意的是，该方法仅在 8 秒视频片段上评估，VGGSound-Hard 经人工筛选后仅含 118 个样本，统计显著性有限；模型对 CAVP 编码器的依赖使其跨视觉域泛化能力尚待验证。



视频查询声源分离（Video-Queried Sound Separation, VQSS）旨在从混合音频中提取与给定视频中视觉对象相对应的声音成分。这一任务的核心挑战在于，视频中往往同时存在多个同质声源——例如多只狗同时吠叫，其中部分在屏幕内、部分在屏幕外。传统的基于类别语义的方法（如 CLIPSEP、i-Query、OmniSep）仅依赖视觉语义信息来区分声源，无法判断声音是否来自屏幕内的特定对象，导致在同质干扰场景下产生大量误分离。

现有 VQSS 方法存在两个关键瓶颈。**其一，缺乏时间建模能力。** 主流方法将视频帧作为语义嵌入注入分离网络，通过交叉注意力（Cross-Attention）融合视听特征，但这种方式丢失了视频帧与音频片段之间的精确时间对应关系。当多个同质声源在时间上交错出现时，模型无法利用“该声音是否与当前屏幕内动作同步”这一关键线索进行判别。**其二，掩码判别模型的固有缺陷。** 现有方法几乎都采用掩码判别范式，即直接预测时频掩码并与混合频谱相乘得到分离结果。这种“一刀切”的频谱抑制策略容易产生频谱空洞（Spectral Holes），导致分离音频不完整、存在伪影，尤其在频谱重叠严重的区域表现尤为明显。

生成式模型（如扩散模型 +Davis 和流匹配模型 tDavis-flow）为缓解频谱空洞问题提供了新思路，但它们同样缺乏时间对齐机制，在同质干扰场景下仍无法有效区分声源。因此，设计一个既能利用生成式建模产生完整频谱、又能强制执行视听时间对齐的框架，成为突破当前 VQSS 性能瓶颈的关键。

AlignSep 正是在这一背景下提出的：**首次将条件流匹配（Conditional Flow Matching）引入 VQSS 任务**，通过生成式框架缓解掩码方法固有的频谱空洞问题；同时设计专门的时间连接策略和视觉时间编码器 CAVP，强制执行视听时间对齐，使模型能够明确利用视觉时间线索区分同质音频源。



## 核心方法与创新机理

AlignSep 的核心创新在于将视频查询声源分离（VQSS）从传统的**掩码判别范式**重构为**时间对齐的条件生成范式**，通过三个相互耦合的机制设计——条件流匹配生成框架、时间感知视觉编码器（CAVP）和基于拼接的时间融合策略——系统性地解决了同质声源干扰和频谱空洞两大瓶颈问题。

### 瓶颈诊断：从“是什么”到“为什么”

现有 VQSS 方法面临两个深层失效模式：

1. **同质声源混淆**：传统方法（如 **CLIPSEP**，Dong et al., 2022；**i-Query**，Chen et al., 2023；**OmniSep**，Cheng et al., 2024）仅依赖语义信息进行分离，无法区分画内/画外同类别声源（如多只狗同时吠叫）。这些方法缺乏对视觉时间线索的显式建模，导致分离结果在时间维度上与视频内容错位。

2. **频谱空洞伪影**：掩码判别模型在频谱重叠区域通过“抹除”干扰源来提取目标，但这种硬掩码操作会在重叠频段留下不连续的频谱空洞，产生不自然的听觉伪影（Figure 4b）。

AlignSep 的解决方案是**将分离重新定义为多条件生成任务**——以混合音频和视频序列联合条件化输出分布，而非学习一个确定性的掩码映射。

### 创新机制一：条件流匹配生成框架

AlignSep 是**首个基于流匹配的生成式 VQSS 模型**（part_001, part_003）。与扩散模型（如 **+Davis**，Huang et al., 2024）和掩码判别模型不同，流匹配通过学习从混合音频分布到干净音频分布的传输向量场 $v(x, t, e; \theta)$，在连续时间 $t \in [0, 1]$ 上执行 ODE 驱动的概率密度变换：

$$\mathrm{d}x = u(x, t, e) \mathrm{d}t$$

训练采用条件流匹配（CFM）目标，避免直接计算真实向量场 $u$ 的困难：

$$L_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, p_c(\pmb{x}_c), p_t(\pmb{x}, \pmb{x}_c)} \big|\big| v(\pmb{x}, t, \pmb{e}; \theta) - u(\pmb{x}, t, \pmb{x}_c, \pmb{e}) \big|\big|^2$$

推理时通过欧拉方法迭代求解 ODE，配合无分类器引导（CFG，尺度 $s=4.5$）平衡生成质量与多样性：

$$\hat{v}(x, t, e; \theta) = s \cdot v(x, t, e; \theta) + (1-s) \cdot v(x, t, \varnothing; \theta)$$

**生成式框架的关键优势**在于：迭代推理过程中，模型在每个去噪步骤都接受跨模态条件，能够持续校正分离结果，强制执行混合一致性和相位一致性（part_006），从而缓解掩码方法的频谱空洞问题。消融实验证实，将流匹配替换为扩散模型后，VGGSound-Clean 上的语义一致性 S_A-A 从 73.38 降至 64.12（Table 7），表明生成式建模的选择直接影响性能上限。

### 创新机制二：时间感知视觉编码器（CAVP）

CAVP 是 AlignSep 实现时间对齐能力的核心组件。与 ImageBind 等纯语义编码器不同，CAVP 通过**时间同步监督**提取视频帧的时间特征（4 FPS），使模型能够区分“何时”发生声音事件，而非仅识别“什么”在发声。

消融实验揭示了 CAVP 的决定性作用：移除 CAVP 后，VGGSound-Hard 上的时间一致性 T_A-V 从 95.76 骤降至 76.27（下降 19.49 点），退化为与 OmniSep 相当的水平（Table 7）。这一结果表明，**时间理解能力是区分同质声源的前提条件**，语义信息本身不足以解决画内/画外混淆问题。

Figure 3 进一步展示了时间信息量的影响：随着视频帧率从 0 FPS（纯语义）提升至 4 FPS，模型在 VGGSound-Hard 上的分离性能持续改善，验证了时间线索的边际收益。

### 创新机制三：拼接融合策略

AlignSep 采用**时间拼接 + 无交叉注意力的前馈 Transformer** 作为向量场估计器的融合架构（part_003, 3.3）。与 i-Query 和 OmniSep 使用的交叉注意力机制不同，拼接策略将视频特征直接沿时间维度拼接到音频潜变量上，形成强制的视听时间对应关系。

消融对比（Table 8）显示，拼接融合在 VGGSound-Hard 上实现 T_A-V = 95.76，而交叉注意力仅 73.38（差距 22.38 点）。这一显著差异表明，**交叉注意力的软对齐机制在时间敏感任务中容易丢失精确的时间对应关系**，而拼接策略通过硬编码的时空耦合强制模型关注视觉时间线索。

### 创新协同效应

三个创新机制并非独立运作，而是形成正向协同：

- **CAVP** 提供高质量的时间视觉特征；
- **拼接融合** 将这些特征以不可忽略的方式注入生成过程；
- **流匹配框架** 在迭代去噪过程中持续利用这些时间条件进行校正。

这种协同使得 AlignSep 在最具挑战性的 VGGSound-Hard 基准上实现了 95.76% 的时间一致性，远超最强基线 OmniSep 的 76.27%（Table 1），同时在主观评估 MOS 上也达到 4.43（Table 2）。定性分析（Figure 4a）证实，AlignSep 能够严格遵循视频中的击鼓节奏进行分离，而 OmniSep 在非击鼓时段仍产生鼓声伪影。

**需要指出的局限**：模型目前仅在 8 秒视频片段上验证，对长视频的可扩展性、CAVP 在不同视觉域的泛化能力，以及 VGGSound-Hard 仅 118 样本的统计显著性，均需进一步验证。



AlignSep 是一个基于条件流匹配（Conditional Flow Matching）的视频查询声源分离（VQSS）框架。其核心目标是在视觉条件的引导下，建立从混合音频分布到干净分离音频分布的映射。与现有基于掩码判别或扩散的方法不同，AlignSep 是首个将流匹配引入 VQSS 的生成式模型，并明确设计了时间对齐机制来利用视觉时间线索。

### Pipeline 概述

整个 pipeline 包含四个关键模块，构成一个端到端的条件生成流程：

1.  **音频变分自编码器（1D VAE）**：将输入的梅尔频谱图压缩为低维潜变量，作为流匹配的生成空间，并在推理阶段将潜变量重建回音频信号。
2.  **CAVP 视觉编码器**：以 4 FPS 的帧率从视频中提取时间对齐的视觉特征，为后续的时间融合提供时序敏感的视觉条件。
3.  **时间对齐向量场估计器**：框架的核心去噪/生成网络。它接收混合音频潜变量、时间步 $t$ 和视觉条件，通过前馈 Transformer 架构估计传输向量场 $v(x, t, e; \theta)$，驱动生成过程。
4.  **无分类器引导（CFG）**：在采样阶段，通过结合条件与无条件向量场（引导尺度 $s=4.5$）来调节生成质量与多样性之间的平衡。

### 模块关系与输入输出流

整个推理过程是一个迭代的 ODE 求解过程。给定一段混合音频 $A^m$ 和对应的视频帧序列 $V$，系统首先通过 1D VAE 的编码器将混合音频的梅尔频谱图映射为初始噪声潜变量 $x_0 \sim \mathcal{N}(0, I)$。同时，CAVP 编码器从视频帧中提取时间对齐的视觉嵌入 $e$。

在每一个去噪步骤 $t \in [0, 1]$ 中，向量场估计器接收当前噪声潜变量 $x_t$、时间步 $t$ 和视觉条件 $e$，输出估计的向量场 $\hat{v}(x_t, t, e; \theta)$。随后，通过欧拉方法对 ODE 进行数值积分来更新潜变量：

$$x_{t+\epsilon} = x_t + \epsilon \cdot \hat{v}(x_t, t, e; \theta)$$

经过预设的迭代步数（如 25 步）后，得到最终的干净音频潜变量 $x_1$。最后，1D VAE 的解码器将 $x_1$ 重建为分离后的音频波形。

### 关键技术决策：时间拼接融合

在向量场估计器内部，AlignSep 采用了一种关键的**时间拼接（Temporal Concatenation）融合策略**，而非此前方法（如 i-Query、OmniSep）常用的交叉注意力机制。具体而言，CAVP 提取的视觉特征序列被直接拼接到对应的音频特征序列上，然后送入一个无交叉注意力的前馈 Transformer 编码器进行处理。这种设计强制模型在特征层面建立显式的视听时间对应关系，而非通过注意力权重隐式学习。消融实验证实，在挑战性的 VGGSound-Hard 基准上，拼接融合策略相比交叉注意力将时间一致性（T_A-V）提升了 22.38 个百分点（从 73.38 提升至 95.76），是框架实现高精度时间对齐的核心机制。

### 训练目标

训练阶段，模型采用条件流匹配（CFM）目标进行优化，该目标通过设计特定的概率路径，避免了直接计算真实传输向量场 $u$ 的困难：

$$L_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, p_c(\mathbf{x}_c), p_t(\mathbf{x} | \mathbf{x}_c)} \big|\big| v(\mathbf{x}, t, \mathbf{e}; \theta) - u(\mathbf{x}, t, \mathbf{x}_c, \mathbf{e}) \big|\big|^2$$

其中，$\mathbf{x}_c$ 代表干净音频的条件样本，$p_t(\mathbf{x} | \mathbf{x}_c)$ 是定义的条件概率路径。通过最小化该损失，向量场估计器学会在视觉条件 $\mathbf{e}$ 的引导下，将任意噪声样本逐步变换为对应的干净音频。

**局限性提示**：当前框架仅在 8 秒的视频片段上进行训练和评估，其在更长视频序列上的可扩展性和内存占用尚未验证。此外，框架对 CAVP 视觉编码器的依赖意味着其性能上限受限于该编码器的泛化能力，在不同视觉领域（如非自然视频）的适用性需要进一步研究。



### 3.1 问题形式化

给定混合音频 $A^{m} = \{A_{1}^{m}, \cdots, A_{n}^{m}\}$，其由干净源音频 $A^{c} = \{A_{1}^{c}, \cdots, A_{n}^{c}\}$ 与干扰源音频 $A^{i} = \{A_{1}^{i}, \cdots, A_{n}^{i}\}$ 线性叠加而成。VQSS 任务的目标是：以视频序列 $V$ 为查询条件，从 $A^{m}$ 中分离出与 $V$ 对应的 $A^{c}$。AlignSep 将此建模为多条件生成任务——混合音频与视频序列联合条件化输出分布。

### 3.2 条件流匹配框架

AlignSep 将分离过程形式化为从混合音频分布到干净音频分布的概率密度变换，由一个时变常微分方程（ODE）控制：

$$\mathrm { d } x = u ( x , t , e ) \mathrm { d } t , \quad t \in [ 0 , 1 ]$$

其中 $u(x, t, e)$ 为传输向量场，$e$ 为条件（视频特征），$t \in [0, 1]$ 为时间变量。$t=0$ 时 $x$ 服从混合音频分布，$t=1$ 时服从干净音频分布。

为训练神经网络 $\theta$ 逼近 $u$，标准流匹配目标为：

$$L _ { \mathrm { F M } } ( \theta ) = \mathbb { E } _ { t , p _ { t } ( \mathbf { x } ) } \big | \big | v ( \mathbf { x } , t , e ; \theta ) - u ( \mathbf { x } , t , e ) \big | \big | ^ { 2 }$$

由于直接计算 $u$ 不可行，AlignSep 采用条件流匹配（CFM）目标，通过设计特定概率路径避免直接计算：

$$L _ { \mathrm { C F M } } ( \theta ) = \mathbb { E } _ { t , p _ { c } ( { \pmb x } _ { c } ) , p _ { t } ( { \pmb x } , { \pmb x } _ { c } ) } \big | \big | v ( { \pmb x } , t , { \pmb e } ; \theta ) - u ( { \pmb x } , t , { \pmb x } _ { c } , { \pmb e } ) \big | \big | ^ { 2 }$$

推理时，使用欧拉方法对 ODE 进行数值积分，从 $t=0$ 的噪声逐步迭代至 $t=1$ 的干净音频：

$$\pmb { x } _ { t + \epsilon } = \pmb { x } + \epsilon \pmb { v } ( \pmb { x } , t , \pmb { e } ; \theta )$$

### 3.3 核心模块

AlignSep 由三个关键模块构成流水线：

**1D 音频变分自编码器（VAE）**：将 80-bin 梅尔频谱图（16 kHz 采样率，hop size 256）压缩为低维潜变量，并负责从潜变量重建音频波形。该模块作为音频的压缩编码器/解码器，使流匹配在低维空间中高效运行。

**CAVP 视觉编码器**：从视频中提取时间对齐的视觉特征。视频被降采样至 4 FPS，截断为 8 秒片段。CAVP 通过时间同步监督训练，使提取的视觉特征与音频事件在时间轴上精确对应——这是区分同质声源（如多只狗吠）的关键。消融实验表明，移除 CAVP 导致 VGGSound-Hard 上 $T_{A-V}$ 从 95.76 骤降至 76.27（-19.49 点），证明时间视觉理解是性能核心。

**时间对齐向量场估计器**：采用无交叉注意力的前馈 Transformer 架构（4 层，隐藏维度 576），通过**时间拼接**策略融合视频特征与音频潜变量。具体而言，视频特征沿时间维度直接拼接到音频潜变量上，而非使用交叉注意力进行隐式对齐。消融证实，拼接融合在 VGGSound-Hard 上实现 95.76 $T_{A-V}$，而交叉注意力仅 73.38（+22.38 点差距），证明显式的时间对应关系强制对时间对齐分离至关重要。

### 3.4 无分类器引导（CFG）

采样时，AlignSep 采用无分类器引导平衡生成质量与多样性。引导后的向量场为条件向量场与无条件向量场的线性组合：

$$\hat { v } ( x , t , e ; \theta ) = s \cdot v ( x , t , e ; \theta ) + ( 1 - s ) \cdot v ( x , t , \theta ; \theta )$$

其中 $s$ 为引导尺度，AlignSep 设置 $s = 4.5$。无条件向量场通过随机丢弃视频条件训练得到。该机制在迭代采样中增强视频条件对生成过程的控制力。

### 3.5 关键设计决策的因果机制

AlignSep 的核心创新在于**生成式时间对齐**的双重设计：

- **流匹配替代掩码判别模型**：掩码方法在频谱重叠区域产生“频谱空洞”（spectral holes），因为掩码是逐帧独立估计的，缺乏跨帧一致性约束。流匹配的迭代生成过程在每一步都接受跨模态条件化，能够显式利用时间信息并逐步修正分离结果，产生更完整的频谱。
- **拼接融合替代交叉注意力**：交叉注意力通过软对齐聚合视觉信息，无法保证严格的时间对应关系。拼接策略将视觉特征按时间位置直接注入音频潜变量，迫使模型学习精确的视听时间对应，是 $T_{A-V}$ 大幅领先的根本原因。

消融实验进一步揭示：将流匹配替换为扩散模型时，VGGSound-Clean 上 $S_{A-A}$ 从 73.38 降至 64.12，说明生成式建模影响语义质量上限；但时间一致性主要源于 CAVP 视觉编码器而非生成模型选择。



## 实验与关键发现

### 基准测试与评估体系

AlignSep 在三个不同难度的基准上进行了系统评估：**MUSIC-Clean**（单乐器视频）、**VGGSound-Clean**（通用视听场景）以及本文专门构建的挑战性基准 **VGGSound-Hard**。VGGSound-Hard 的核心设计在于引入“同质干扰”——即画外存在与画内目标源类别相同的干扰声（如多只狗同时吠叫），迫使模型必须依赖时间对齐而非仅语义信息进行分离。该基准经人工筛选后包含 118 个高质量样本（Table 1 标题注释）。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_DVDkFcxU1D/figures/003_Table_1.jpg]]
*Table 1: Comparison of visually-queried sound separation performance on MUSIC-Clean, VGGSound-Clean, and VGGSound-Hard (VG-Hard). The evaluation considers semantic consistency between audio–audio ( $\mathsf { S } _ { A - A }$ ) , semantic consistency between audio–visual ( $\mathsf { S } _ { A - V }$ ) , and temporal consistency between audio–visual ( $\mathrm { T } _ { A - V }$ ) to assess the quality of the separated results. † Since Davis is originally trained on different datasets, we retrained their models on the same dataset to ensure a fair comparison

评估采用三个互补指标：
- **S_A-A**（音频-音频语义一致性）：通过 CLAPScore 衡量分离音频与干净目标音频的语义匹配度
- **S_A-V**（音频-视觉语义一致性）：通过 ImageBind 相似度衡量分离音频与视频语义的匹配度
- **T_A-V**（音频-视觉时间一致性）：本文提出的核心指标，衡量分离音频的起始/结束时间与视频中视觉事件的时间对齐精度

此外，通过人类主观评估（MOS）在四个维度上进行验证：噪声残留（NR）、视听一致性（AVC）、音频质量（AQ）和总体评分（OS）。

### 主要定量结果

**Table 1** 展示了 AlignSep 与各基线方法的全面对比。在 VGGSound-Hard 上，AlignSep 实现了 **95.76% 的 T_A-V**，相比最强基线 **OmniSep**（Cheng et al., 2024）的 76.27% 提升了 **+19.49 点**，证明了时间对齐机制在处理同质干扰时的决定性优势。在 VGGSound-Clean 上，AlignSep 的 S_A-A 达到 73.38，超出 OmniSep 的 70.83 约 2.55 点，表明生成式框架在语义保真度上也具有优势。

值得注意的是，在 MUSIC-Clean 这一相对简单的单乐器场景上，AlignSep 与判别式方法（如 i-Query）的性能差距较小（S_A-A: 89.21 vs 88.76），说明时间对齐机制的增益主要体现在复杂干扰场景中。

**Table 2** 的 MOS 人类评估进一步验证了上述结论。在 VGGSound-Hard 上，AlignSep 的总体评分（OS）达到 **4.43**，显著高于 OmniSep 的 4.07（+0.36）。尤其在视听一致性（AVC）维度上，AlignSep 获得 4.57，而 OmniSep 仅为 3.93，差距达 0.64 分，直接反映了时间对齐机制在人类感知层面的显著改善。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_DVDkFcxU1D/figures/004_Table_2.jpg]]
*Table 2: Mean Opinion Score (MOS) across four evaluation dimensions: Noise Residuals (NR), Audio-Visual Consistency (AVC), Audio Quality (AQ), and Overall Score (OS). sounds originating off-screen. After this filtering process, we obtain 118 high-quality audio–visual pairs that exhibit strong semantic homogeneity yet clearly distinct temporal patterns, forming the final VGGSound-Hard benchmark*

### 消融实验：因果机制的分解验证

消融实验系统性地验证了 AlignSep 的三个核心设计选择。

**生成模型选择的影响（Table 7）**：将流匹配替换为扩散模型（+Davis, Huang et al., 2024）后，VGGSound-Clean 上的 S_A-A 从 73.38 降至 64.12（-9.26 点），S_A-V 从 73.64 降至 69.59（-4.05 点）。这表明流匹配在生成质量和语义保真度上优于扩散模型。然而，更关键的发现是：**移除 CAVP 时间视觉编码器**（保留流匹配但仅用语义视觉特征）导致 VGGSound-Hard 上 T_A-V 从 95.76 骤降至 76.27（-19.49 点），直接回退到 OmniSep 的水平。这确凿地证明：**时间一致性主要源于 CAVP 编码器的时间理解能力，而非生成模型本身**。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_DVDkFcxU1D/figures/011_Table_7.jpg]]
*Table 7: Ablation study on generative model choice*

**时间融合策略的对比（Table 8）**：将本文的拼接融合策略替换为交叉注意力机制后，VGGSound-Hard 上的 T_A-V 从 95.76 降至 73.38（-22.38 点），在 MUSIC-Clean 上也从 98.75 降至 97.25。这一显著差距揭示了交叉注意力在保持精细时间对应关系上的根本性局限——注意力机制的软加权特性容易在时间维度上产生模糊匹配，而拼接策略通过强制位置对应关系，确保了视觉时间线索与音频帧之间的严格对齐。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_DVDkFcxU1D/figures/012_Table_8.jpg]]
*Table 8: Ablation on different temporal fusion strategies*

**去噪步数的效率-质量权衡（Table 3）**：AlignSep 在 25 步采样时即可达到接近收敛的性能（VGGSound-Hard T_A-V 95.76），此时推理吞吐量为 4 FPS。进一步增加步数至 50 或 100 步，S_A-V 和 S_A-A 仅有边际提升（如 VGGSound-Clean S_A-V 从 73.64 升至 74.12），但推理时间成倍增加。5 步采样的性能显著下降（S_A-V 降至 64.47），表明过少的迭代不足以有效利用跨模态条件进行精细分离。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_DVDkFcxU1D/figures/005_Table_3.jpg]]
*Table 3: Evaluation of different denoising steps on VGGSound-Clean, MUSIC-VGGSound, and VGGSound-Hard. We report ImageBind similarity, CLAPScore, and alignment accuracy (AlignAcc). The last two columns present inference time and corresponding throughput (FPS). Best results are highlighted in bold*

### 时间信息量的敏感性分析

**Figure 3** 展示了视频帧率（FPS）对分离性能的影响。当仅使用 1 FPS（即几乎无时间信息）时，AlignSep 的 T_A-V 表现接近 OmniSep 的纯语义水平。随着 FPS 从 1 增加到 4，T_A-V 持续提升并在 4 FPS 时达到饱和。这一趋势证实了两个关键点：(1) 时间信息量是时间一致性的直接控制变量；(2) 4 FPS 是在计算效率和时间分辨率之间的合理平衡点。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_DVDkFcxU1D/figures/006_Figure_3.jpg]]
*Figure 3: Comparison of sound separation performance with different levels of temporal information on VGGSOUND-Hard. OmniSep represents the performance when relying solely on semantic information. The x-axis indicates the number of video frames per second (FPS) used for VQSS*

### 定性分析：频谱空洞的缓解

**Figure 4** 提供了两个典型案例的频谱可视化。(a) 展示了时间错位问题：OmniSep 在目标声源静默期间错误生成了鼓声（红色区域），而 AlignSep 严格遵循视觉节奏线索，仅在画面中出现敲击动作时产生对应音频（绿色区域）。(b) 揭示了掩码判别方法的固有缺陷——频谱空洞：当多个声源在频谱上重叠时，掩码方法倾向于过度抑制，导致分离音频出现不连续的频谱断裂（红色区域）。AlignSep 的生成式框架通过迭代去噪过程，能够从混合信号中重建出更完整、更自然的频谱结构（绿色区域），有效缓解了这一伪影。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_DVDkFcxU1D/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative comparison of VQSS. (a) illustrates a temporal misalignment case, while (b) demonstrates the spectral holes artifact. We highlight the critical regions using different colors*

### 失败模式与局限性

尽管在受控基准上表现优异，AlignSep 存在以下已知局限：

1. **时长限制**：模型仅在 8 秒的视频片段上训练和评估，对长视频的扩展性未经验证。时间连接机制的内存开销与序列长度呈线性关系，可能成为长序列处理的瓶颈。

2. **基准规模**：VGGSound-Hard 虽具有挑战性，但仅包含 118 个样本，统计显著性有限。在更大规模、更多样化的野外场景下的泛化性能尚待验证。

3. **视觉编码器依赖**：模型性能高度依赖 CAVP 编码器的泛化能力。若视觉域发生显著偏移（如从自然视频转向动画或低光照场景），时间对齐精度可能下降。该编码器在非训练域上的鲁棒性未经验证。

4. **实时性不足**：当前 25 步采样的 4 FPS 吞吐量远未达到实时处理要求（>25 FPS）。尽管减少步数可提升速度，但 5 步采样的性能已出现明显退化，表明质量-速度的帕累托前沿限制了实时部署的可能性。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_DVDkFcxU1D/figures/008_Table_4.jpg]]
*Table 4: Architecture details of 1D VAE for spectrogram compression*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_DVDkFcxU1D/figures/009_Table_5.jpg]]
*Table 5: Hyperparameters of the vector field estimator of AlignSep*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_DVDkFcxU1D/figures/010_Table_6.jpg]]
*Table 6: Mean Opinion Score (MOS) Rating Criteria*



## 定位与知识库关联

### 1. 方法谱系：从判别掩码到生成式时间对齐

AlignSep 的提出源于对视频查询声源分离（VQSS）领域两个核心瓶颈的直接回应：**时间建模的缺失**与**掩码判别模型的固有缺陷**。现有方法可沿两条轴线定位其谱系位置。

**判别掩码范式。** 早期 VQSS 工作以语义条件化为主，典型代表包括 **CLIPSEP**（Dong et al., 2022）等基于预训练视觉语义嵌入的方法。这些方法将视频帧压缩为全局语义向量，通过交叉注意力注入分离网络，本质上仅利用了“是什么”的类别信息，而完全忽略了“何时发生”的时间结构。**i-Query**（Chen et al., 2023）和 **OmniSep**（Cheng et al., 2024）虽在特征交互机制上有所改进，但均沿用了单次前向掩码生成范式——网络直接预测时频掩码，将混合频谱与掩码相乘得到分离结果。这一范式的致命弱点在于：当多源音频在频谱上高度重叠时，掩码的二元抑制特性不可避免地造成频谱空洞（spectral holes），表现为分离音频中的断续伪影和音质退化。

**生成式分离的初步探索。** 扩散模型在音频生成领域的成功催生了生成式 VQSS 的尝试。**+Davis**（Huang et al., 2024）和 **tDavis-flow**（Huang et al., 2025）分别基于扩散模型和流匹配进行音频分离，但未针对视频查询场景设计专门的时间融合机制。AlignSep 的定位正是在此基础上，将流匹配生成框架与显式的时间对齐机制深度耦合，成为**首个基于流匹配的生成式 VQSS 模型**。

### 2. 关键技术决策的因果机制

AlignSep 相对于基线的三个关键设计变更，各自对应明确的因果逻辑：

**决策一：掩码判别 → 条件流匹配。** 流匹配的生成式框架将分离问题重新定义为从混合音频分布到干净音频分布的概率密度传输。与掩码方法的“硬切割”不同，生成模型通过迭代 ODE 求解逐步“填充”频谱，从根本上规避了频谱空洞问题。消融实验（Table 7）佐证了这一逻辑：将流匹配替换为扩散模型后，VGGSound-Clean 上的语义一致性 $S_{A-A}$ 从 73.38 骤降至 64.12，表明生成式建模的质量上限确实影响了分离的语义保真度。但值得注意的是，时间一致性 $T_{A-V}$ 的下降幅度远小于移除视觉编码器的情形，说明**时间对齐主要源于视觉编码器，而非生成模型本身**。

**决策二：交叉注意力 → 时间拼接融合。** 现有方法普遍采用交叉注意力将视频特征注入音频特征，这种方式允许跨时间步的自由信息流动，但同时也模糊了精确的视听时间对应关系。AlignSep 采用的时间拼接策略，将视频特征沿时间维度与音频特征直接拼接后送入无交叉注意力的前馈 Transformer，强制模型建立一对一的时序对应。消融实验（Table 8）给出了决定性证据：拼接融合在 VGGSound-Hard 上实现 $T_{A-V}=95.76$，而交叉注意力仅为 73.38，差距达 22.38 点。这一巨大差异揭示了时间对齐任务中**显式结构化偏置**优于**隐式学习**的关键规律。

**决策三：语义视觉编码器 → CAVP。** CAVP（时间同步视觉编码器）通过时间同步监督信号，使提取的视频特征本身即携带精确的时间结构信息。移除 CAVP（Table 7）导致 VGGSound-Hard 上 $T_{A-V}$ 从 95.76 跌至 76.27，降幅高达 19.49 点，是所有消融实验中影响最大的单一因素。这验证了核心洞察：**时间视觉编码是时间对齐分离的充分必要条件**。

### 3. 适用边界与局限

AlignSep 的有效性建立在几个关键前提之上，这些前提同时界定了其适用边界：

**时间尺度约束。** 模型在 8 秒视频片段上训练和评估，视频帧率固定为 4 FPS。这一设计隐含假设了分离目标的时间动态处于秒级尺度。对于更长视频序列，时间拼接策略的内存和计算开销将线性增长，前馈 Transformer 的序列长度限制可能成为瓶颈。文中未提供长视频场景下的性能数据，该边界的实际位置需进一步验证。

**视觉编码器的泛化瓶颈。** CAVP 的性能直接决定了整个系统的上限。若输入视频的视觉域与训练数据（VGGSound 的音乐演奏场景为主）存在显著分布偏移——例如动画、低光照、快速镜头切换——视觉编码器提取的时间特征质量将退化，进而影响分离的时间精度。文中未在跨域数据上进行评估。

**基准规模的统计显著性。** VGGSound-Hard 基准虽然挑战性高，但经过人工筛选后仅包含 118 个样本。在此规模上报告的 $T_{A-V}=95.76$ 虽远超基线，但置信区间的宽度可能较大，结论的统计显著性需要更大规模测试集的验证。

**推理效率与实时性的权衡。** 流匹配的迭代推理特性带来了计算开销。25 步采样可实现约 4 FPS 的推理吞吐（Table 3），但距离实时应用（>25 FPS）仍有数量级差距。虽然 10 步采样可提升速度，但语义一致性会相应下降，存在明确的质量-效率帕累托前沿。

### 4. 开放问题

1. **长视频可扩展性。** 当视频长度超过 8 秒时，时间拼接的内存复杂度为 $O(L^2)$（$L$ 为序列长度）。是否可以通过滑动窗口、层次化时间编码或稀疏注意力机制实现线性扩展，同时保持时间对齐精度？

2. **跨域鲁棒性。** 在 VGGSound-Hard 之外的真实场景（如会议录音、户外监控）中，多源重叠程度更高、背景噪声更强、视觉线索更模糊。CAVP 在这些条件下的时间特征提取能力是否仍能支撑可靠的分离？

3. **完全同质源的分离极限。** 当两个音频源在语义类别、频谱特征和时间模式上均高度相似时（如两把同型号小提琴同时演奏），视觉时间线索是否仍能提供足够的区分度？这触及了 VQSS 的信息论极限。

4. **实时流式推理。** 当前框架依赖离线批处理。若需实现流式分离，ODE 求解的迭代特性与低延迟要求之间存在根本性矛盾。是否可以通过蒸馏、一致性模型或提前退出策略将推理压缩至单步或少量步骤，同时维持可接受的分离质量？

5. **视觉-音频异步场景。** 现实视频中常存在视听不同步（如配音、网络延迟）。AlignSep 的强制时间对齐假设在此类场景下可能产生错误的对应关系。如何检测并适应视听时间偏移，是一个尚未探索的方向。



## 原文 PDF

![[paperPDFs/ICLR_2026/AlignSep_Temporally_Aligned_Video_Queried_Sound_Separation_with_Flow_Matching.pdf]]
