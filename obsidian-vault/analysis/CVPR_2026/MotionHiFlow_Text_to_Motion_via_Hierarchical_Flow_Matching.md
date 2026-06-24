---
title: "MotionHiFlow: Text-to-Motion via Hierarchical Flow Matching"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MotionHiFlow_Text_to_Motion_via_Hierarchical_Flow_Matching.pdf
aliases:
- MotionHiFlow
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 分层流匹配框架，通过在多个时间尺度上逐步生成运动，先学习粗粒度语义对齐，再逐步细化细节。
primary_logic: 粗尺度运动保留了丰富的文本语义信息，因此分层生成策略可以在低时间尺度上建立强语义对齐，然后在更高尺度上添加细节，从而同时优化语义一致性和运动细节。
claims:
- R-precision在降采样比0.2时仍保持稳定，表明粗尺度运动保留了大部分语义。
- 仅训练在粗尺度运动上的模型有时能获得比精细尺度更好的语义对齐。
- "分层流匹配（尺度为[1/3, 2/3, 1]）在HumanML3D上取得FID=0.032，优于单尺度基线。"
- 引入TMDiT和拓扑感知VAE后，FID从0.074显著提升至0.032。
---

# MotionHiFlow: Text-to-Motion via Hierarchical Flow Matching

> [!tip] 核心洞察
> 粗尺度运动保留了丰富的文本语义信息，因此分层生成策略可以在低时间尺度上建立强语义对齐，然后在更高尺度上添加细节，从而同时优化语义一致性和运动细节。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionHiFlow：基于分层流匹配的文本到动作生成 |
| 英文题名 | MotionHiFlow: Text-to-Motion via Hierarchical Flow Matching |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_MotionHiFlow_Text-to-Motion_via_Hierarchical_Flow_Matching_CVPR_2026_paper.html) · [Code](https://github.com/ai-lh/MotionHiFlow) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | MotionHiFlow |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-1, FID 0.563；R-Precision Top-1, FID 0.032；MM-Dist 2.691。
> - KIT-ML 上，R-Precision Top-1, FID 0.482；R-Precision Top-1, FID 0.135；MM-Dist 2.552。

## 概述

**问题瓶颈**：现有文本到动作生成方法（如 MDM (Tevet et al., ICLR 2023)、MoMask、MoGenTS (Yuan et al., NeurIPS 2024)）均在单一时间尺度上操作，难以同时捕捉全局语义结构和细节运动时序，导致语义对齐与运动连贯性不足。

**核心洞察**：粗尺度运动保留了丰富的文本语义信息——实验显示，即使将运动降采样至 0.2 倍，R-Precision 仍保持稳定（Figure 1），且仅训练在粗尺度运动上的模型有时能获得比精细尺度更好的语义对齐（Table 2）。这揭示了“先粗后细”分层生成策略的可行性。

**方法定位**：MotionHiFlow 是一个基于流匹配（Flow Matching）的分层生成框架，通过 K 个阶段逐步从低时间尺度到高时间尺度生成运动。其关键创新包括：（1）跨尺度去噪-上采样-重噪过渡过程，保证噪声一致性；（2）拓扑感知的 Graph CNN VAE 进行运动压缩编码；（3）双流 TMDiT 结合 Joint RoPE 位置编码处理文本条件与运动潜在变量。

**主要结果**：在 HumanML3D 数据集上，MotionHiFlow 取得 FID=0.032、R-Precision Top-1=0.563、MM-Dist=2.691；在 KIT-ML 上取得 FID=0.135、R-Precision Top-1=0.482、MM-Dist=2.552（Table 1）。消融实验表明，引入分层流匹配、TMDiT 和拓扑感知 VAE 后，FID 从 0.074 显著降至 0.032（Table 3）。用户研究进一步验证了该方法在真实性和文本对齐方面优于 MoMask 和 MoGenTS（Figure 5）。

## 背景与动机

### 文本到运动生成的核心挑战

从自然语言描述生成三维人体运动序列是一项跨模态生成任务，其核心难点在于同时满足两个高度耦合的约束：**语义对齐**（生成的运动必须准确反映文本描述的动作、时序与空间关系）与**运动真实性**（生成的运动序列需符合人体运动学规律，保持时序连贯与细节自然）。现有方法大多在单一时间尺度上操作——无论是基于扩散模型、掩码建模还是VAE的方案——这导致它们在全局语义结构与局部运动细节之间陷入两难：精细尺度上的建模容易丢失长程语义对应，而粗粒度建模又难以捕捉细微动作变化。

### 现有方法的瓶颈

当前主流方法可归为三类范式，各自存在结构性局限：

- **扩散/流匹配模型**（如**MDM** (Tevet et al., ICLR 2023)、**MoGenTS** (Yuan et al., NeurIPS 2024)）在原始运动空间或潜在空间上执行去噪生成。它们在整个时间维度上以相同分辨率处理运动序列，缺乏对不同时间尺度上信息层次的分辨能力。当文本描述包含复杂的时序关系（如“先走几步再转身挥手”）时，单尺度模型难以在保持全局结构的同时刻画细粒度关节动态。
- **掩码运动模型**（如**MoMask**、**MMM** (Pinyoanuntapong et al., CVPR 2024)）通过迭代预测被掩码的运动片段来生成序列。这类方法天然倾向于局部模式补全，在长序列的全局语义一致性上表现不足。
- **VAE+先验模型**通常将运动压缩到固定维度的潜在空间再生成。标准VAE（如MoGenTS中使用的2D卷积VAE）将运动序列视为规则的时空网格，忽略了人体骨架的拓扑结构，导致压缩-重建过程中丢失关节间的运动学约束信息。

一个关键观察是：**粗尺度运动保留了丰富的文本语义信息**。如Figure 1所示，当对运动序列进行降采样（downsampling）时，文本-运动检索的R-precision在降采样比低至0.2时仍保持稳定。这意味着粗粒度的运动表征已经编码了大部分文本相关的语义内容，而精细尺度主要承载细节纹理。然而现有方法并未显式利用这一层次特性来解耦生成过程。

### 本文动机

上述观察揭示了一个核心洞察：**生成过程应当遵循从粗到精的层次化策略**——先在低时间尺度上建立强语义对齐，再逐步在高尺度上添加运动细节。这类似于人类编排动作时的思维过程：先确定动作的总体框架和节奏，再填充具体的关节轨迹。

基于此，本文提出**MotionHiFlow**，一个分层流匹配（Hierarchical Flow Matching）框架。其设计动机直接回应三个关键问题：

1. **如何在多尺度上组织生成过程？** 框架将生成分解为K个阶段，每个阶段在特定的时间分辨率上执行流匹配，从低分辨率到高分辨率逐步细化运动。
2. **如何保证跨尺度的一致性？** 引入一种新颖的跨尺度过渡过程——通过去噪-上采样-重噪（denoising-upsampling-renoising）操作连接相邻尺度的流路径，确保噪声分布在整个生成过程中保持数学一致性。
3. **如何增强各尺度上的建模能力？** 设计拓扑感知的图卷积运动VAE来保留骨架结构信息，并提出双流文本-运动DiT（TMDiT）结合联合旋转位置编码（Joint RoPE），在去噪网络中更有效地融合词级文本条件与运动特征。

通过这种层次化设计，MotionHiFlow旨在从根本上解耦语义对齐与细节生成，使每个阶段专注于其对应尺度的建模目标，从而突破单尺度方法的性能瓶颈。

## 核心创新

MotionHiFlow的核心创新在于将文本到运动生成从单一时间尺度拓展为**分层多尺度流匹配框架**，并通过三个关键机制解决语义对齐与运动细节的矛盾。

### 1. 分层流匹配：从粗到细的生成范式

现有方法（如MDM、MoMask、MoGenTS）在单一时间尺度上操作，难以同时捕捉全局语义结构和细节运动。MotionHiFlow的**核心洞察**来自Figure 1：即使将运动序列降采样至0.2倍，R-precision仍保持稳定，表明粗尺度运动保留了大部分文本语义信息。基于此，框架将生成过程分解为K个阶段，每个阶段在不同的时间尺度 $r_k$ 上运行流匹配（文中采用 $r_k \in \{1/3, 2/3, 1\}$ 三阶段配置）。

**因果机制**：早期阶段在低时间尺度上建立强语义对齐，后续阶段在高尺度上逐步添加细节。Table 2的消融实验直接支持这一设计——仅训练在粗尺度运动上的模型有时能获得比精细尺度更好的语义对齐，验证了“粗尺度优先捕获语义”的假设。

### 2. 跨尺度过渡：去噪-上采样-重噪过程

分层生成面临的核心挑战是**跨尺度噪声一致性问题**。直接上采样噪声数据会破坏流匹配的概率路径连续性。MotionHiFlow引入了一个三步骤过渡过程：

1. **去噪**：使用当前阶段学到的速度场将状态推至近数据端
2. **上采样**：在近数据空间进行时间维度插值
3. **重噪**：将上采样后的状态重新推回噪声空间，作为下一阶段的起始点

这一过程由Eq.(8)-(10)形式化定义，确保跨尺度时噪声分布的一致性。这与baseline中简单的上采样策略形成根本性差异。

### 3. 拓扑感知的运动表征与条件建模

框架在三个层面引入了结构感知设计：

- **拓扑感知VAE**：替代baseline（如MoGenTS）的2D卷积VAE，采用Graph CNN显式编码人体运动学树结构，通过图池化实现空间降采样，增强对骨骼拓扑的感知能力。

- **Joint RoPE位置编码**：将标准Transformer位置编码替换为三合一旋转位置编码，同时编码时序位移、2D空间坐标和运动学深度信息，按比例 $[1/2, 1/8, 1/8, 1/4]$ 分段应用1D RoPE。

- **双流TMDiT**：替代单一句子级文本嵌入，采用双分支DiT架构独立处理运动特征和词级文本特征，前 $L_s$ 层使用独立参数，后续层共享参数以促进跨模态融合。

**证据强度**：Table 3的消融实验显示，引入TMDiT和拓扑感知VAE后，FID从0.074显著降至0.032（HumanML3D），验证了这些组件对生成质量的因果贡献。Table 1的主实验进一步表明，完整框架在HumanML3D上取得FID=0.032、R-Precision Top-1=0.563，在KIT-ML上取得FID=0.135、R-Precision Top-1=0.482，均达到最优水平。

## 整体框架

MotionHiFlow 构建了一个**从粗到细的多阶段生成管线**，核心思路是将文本到运动的生成过程分解为 K 个时间尺度递增的阶段，每个阶段通过流匹配（Flow Matching）学习对应尺度下的速度场。整个框架包含五个关键模块，形成“编码—条件去噪—解码”的完整链路。

### 管线总览

输入为自然语言描述文本，输出为目标人体运动序列。数据流经以下模块：

1. **Text Encoder（CLIP）**：提取文本的单词级嵌入，为后续去噪网络提供细粒度的语义条件。
2. **Motion VAE（拓扑感知）**：将原始运动序列压缩到低维潜在空间，并在生成末端将潜在表征解码回运动序列。该 VAE 在编码器端进行时序 4 倍降采样和基于人体拓扑图的空间降采样，显式捕捉骨架结构。
3. **TMDiT with Joint RoPE**：双流去噪网络，独立处理运动潜在变量和文本特征，通过自注意力和共享参数实现跨模态信息交换。Joint RoPE 将时序位移、2D 空间坐标和运动学树深度编码为统一的旋转位置编码。
4. **Hierarchical Flow Matching Scheduler**：多尺度流调度器，控制 K 个阶段的流匹配过程，执行跨尺度过渡和 ODE 求解。
5. **Motion Decoder**：将去噪后的潜在表征解码为最终的全尺度运动序列。

如 Figure 2 所示，早期阶段在低时间尺度（如 1/3 采样率）上运行，主要捕获高层语义和粗粒度运动结构；后期阶段逐步提升尺度（2/3 → 1），建模精细的时序细节。每个阶段内部执行流匹配去噪，阶段之间通过**去噪-上采样-重噪**的跨尺度过渡过程连接，确保噪声一致性在整个生成过程中得以保持。

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MotionHiFlow_Text_t/figures/002_Figure_2.jpg]]
*Figure 2: OverviewofourMotionHiFlow,whichprogressvelygeneratesmotionfromlowtohightemporalscalesacrossultiplestages. Theearlystagesainlyapturehigvelsemanticsandoarseotiosucture,hilelaterstagesodelfieaiedtemporaldtla cross-scaletrasioadoerato.entsalogtegaientoloeddashdeineiset(otoleftof(a)andindeotes a linear interpolation between its endpoints.Down/Up denotes downsampling/upsampling,respectively*

### 分层流匹配调度机制

分层流匹配是框架的核心调度逻辑。设总阶段数为 K，第 k 阶段的时间尺度由降采样比 $r_k$ 控制（$r_1 < r_2 < \dots < r_K = 1$）。每个阶段在一个时间区间 $[t_{k-1}, t_k]$ 上定义流路径：

- **阶段起点**（Eq. 4）：结合初始噪声 $\pmb{x}_0$ 和前一阶段的降采样运动信息，通过线性插值构造起始状态，保证跨阶段信息的连续性。
- **阶段终点**（Eq. 5）：为当前尺度下噪声与干净数据的线性插值，定义该阶段流匹配的目标方向。

在推理时，每个阶段通过求解 ODE $\mathrm{d} \pmb{x}_t = v_{\theta}(\pmb{x}_t, t) \mathrm{d} t$ 生成对应尺度的运动潜在变量；阶段切换时执行去噪→上采样→重噪操作，将当前输出传递到下一尺度（Algorithm 1）。训练时，分层流匹配损失 $\mathcal{L}_{HFM}$（Eq. 6）统一优化所有阶段的速度场。

### 关键设计选择

- **尺度选择**：论文采用 $r_k \in \{1/3, 2/3, 1\}$ 三层结构（Section 4.1）。消融实验（Table 2）表明，仅训练在粗尺度（1/3）上的模型在语义对齐上有时优于精细尺度模型，验证了“粗尺度保留大部分语义”的核心洞察。
- **跨尺度过渡**：不同于简单的噪声上采样，去噪-上采样-重噪过程从数学上保持了流路径的噪声分布一致性，这是分层框架有效性的关键（Section 3.4）。
- **双流 TMDiT**：前 3 个 block 使用独立的双分支参数以保留模态特异性，后 6 个 block 共享参数以学习跨模态共性表征（Section 4.1）。

整个管线采用两阶段训练策略：先训练 Motion VAE（重建损失 + KL 散度 + 增强损失 $\mathcal{L}_{aug}$），再冻结 VAE 训练 TMDiT 的分层流匹配损失（Section 3.6）。

## 核心模块与公式推导

### 3.1 基础流匹配

MotionHiFlow 建立在条件流匹配（Conditional Flow Matching）框架之上。给定噪声样本 $\pmb{x}_0 \sim p_0$ 与真实数据 $\pmb{x}_1 \sim p_1$，定义线性插值条件概率路径：

$$\pmb{x}_t = (1 - t) \pmb{x}_0 + t \pmb{x}_1 \quad \text{(Eq. 2)}$$

该路径对应的目标速度场为 $u_t(\pmb{x}_t | \pmb{x}_1) = \pmb{x}_1 - \pmb{x}_0$。训练目标是最小化速度场预测与目标速度场之间的均方误差：

$$\mathcal{L}_{FM}(\theta) = \mathbb{E}_{t \sim \mathcal{U}(0,1)} \| v_{\theta}(\pmb{x}_t, t) - u_t(\pmb{x}_t | \pmb{x}_1) \|^2 \quad \text{(Eq. 1)}$$

推理时，从 $\pmb{x}_0 \sim p_0$ 出发，通过求解常微分方程生成新数据：

$$\mathrm{d} \pmb{x}_t = v_{\theta}(\pmb{x}_t, t) \mathrm{d} t \quad \text{(Eq. 3)}$$

### 3.2 分层流匹配框架

核心瓶颈在于：单一时间尺度生成难以同时捕捉全局语义与局部细节。MotionHiFlow 将生成过程分解为 $K$ 个阶段，每个阶段在特定时间尺度 $r_k$ 上操作（$0 < r_1 < \dots < r_K = 1$），实现从粗到细的渐进式运动生成。

**阶段起始与终止状态。** 对第 $k$ 阶段，定义降采样函数 $f(\cdot, r)$ 将运动序列压缩至尺度 $r$。阶段起始状态 $\pmb{x}_{t_{k-1}}^{(k)}$ 需融合前序阶段信息与初始噪声，以保证跨尺度噪声一致性：

$$\pmb{x}_{t_{k-1}}^{(k)} = (1 - t_{k-1}) f(\pmb{x}_0, r_k) + t_{k-1} f(f(\pmb{x}_1, r_{k-1}), r_k / r_{k-1}) \quad \text{(Eq. 4)}$$

阶段终止状态为当前尺度下噪声与干净数据的线性插值：

$$\pmb{x}_{t_k}^{(k)} = (1 - t_k) f(\pmb{x}_0, r_k) + t_k f(\pmb{x}_1, r_k) \quad \text{(Eq. 5)}$$

**跨尺度过渡机制。** 这是本方法的关键创新点：不同于直接上采样噪声数据，MotionHiFlow 在阶段切换时执行“去噪—上采样—重噪”三步操作。先从上一阶段终止状态沿 ODE 反向去噪至纯噪声，上采样至下一尺度，再重新加噪至对应时间步。这一设计保证了跨尺度的噪声分布一致性。

**分层流匹配损失。** 训练时，对每个阶段的速度场进行联合优化：

$$\mathcal{L}_{HFM}(\theta) = \mathbb{E}_{k,t} \| v_{\theta}(x_t^{(k)}, t) - (x_{t_k}^{(k)} - x_{t_{k-1}}^{(k)}) \|^2 \quad \text{(Eq. 6)}$$

其中目标速度即为阶段终点与起点之差。推理过程见 Algorithm 1，各阶段依次执行 ODE 求解后过渡至下一尺度。

### 3.3 拓扑感知运动 VAE

运动 VAE 负责将运动序列压缩至紧凑潜在空间，其关键设计在于显式编码人体骨架拓扑。编码器采用图卷积网络（GCN）捕获关节间的运动学依赖关系，在时间维度进行 4 倍降采样，同时在空间维度通过图池化进行骨架压缩。解码器对称地执行上采样与图反池化。

为增强多尺度表征能力，引入数据增强损失：

$$\mathcal{L}_{aug} = \| \mathrm{Dec}(f(x, r)) - f(M, r) \|^2 \quad \text{(Eq. 11)}$$

该损失约束解码器从降采样潜在变量中重建降采样后的运动序列，使 VAE 适应不同时间尺度的输入。

### 3.4 双流文本-运动 DiT（TMDiT）与联合 RoPE

TMDiT 是去噪网络的核心，采用双流架构分别处理运动特征与文本特征。前 $L - L_s$ 层各分支使用独立参数以保留模态特化表征，后 $L_s$ 层共享参数以促进跨模态融合。自注意力机制在双流间交换信息，实现文本条件对运动生成的精细控制。

位置编码方面，提出联合 RoPE（Joint Rotary Position Embedding），将位置信息分解为四个段，按比例 $[1/2, 1/8, 1/8, 1/4]$ 分别编码：
- **时序位移**：帧间相对时间位置；
- **空间坐标**：关节在 2D 平面上的相对空间位置；
- **运动学深度**：关节在骨架树中的层级深度；
- **保留段**：为扩展预留。

每段独立应用 1D RoPE 后拼接，使模型同时感知时间、空间与拓扑三维度的相对位置关系。

### 3.5 训练策略

采用两阶段训练范式。第一阶段训练运动 VAE，优化目标包含重建损失、KL 散度正则项与增强损失 $\mathcal{L}_{aug}$；第二阶段冻结 VAE，在潜在空间训练 TMDiT，优化分层流匹配损失 $\mathcal{L}_{HFM}$。实验配置采用三个流层，尺度为 $r_k \in \{1/3, 2/3, 1\}$，TMDiT 共 9 个块，前 3 块双分支独立参数，后 6 块共享参数。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MotionHiFlow_Text_t/figures/003_Figure_3.jpg]]
*Figure 3: Iustrationof twomaincomponents inourTMDiT.(a)The TMDiblock employs two separate streams that independently processmotionandtextfeatures,whileself-atentionandsharedparametersenablesiformationexchangebetweestreams.(b)TheJoint RoPE integratesotationsderivedfromtemporaldisplacement,relative spatialcoordiates,andthe human bodytopologies.Here*

## 实验与分析

### 核心动机验证：粗尺度运动保留语义

在介绍主实验之前，论文先通过一个预实验验证了分层生成策略的根本动机。Figure 1 展示了在不同时间降采样比例下的文本-运动检索精度（R-Precision）。结果表明，即使将运动序列降采样至原始帧率的 0.2 倍，R-Precision 依然保持稳定。这说明**粗时间尺度的运动已经保留了绝大部分文本语义信息**。基于这一发现，MotionHiFlow 的分层策略在低时间尺度上先建立强语义对齐，再逐步添加细节，这一设计具有坚实的经验基础。

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MotionHiFlow_Text_t/figures/001_Figure_1.jpg]]
*Figure 1: Text-to-Motion retrieval precision under different downsampling ratios. The R-precision remains stable as the downsampling ratio decrease,which means that models trained on coarse motions can achieve robust semantic alignment*

### 主实验结果

Table 1 给出了在 HumanML3D 和 KIT-ML 两个标准数据集上与当前最优方法的定量对比。MotionHiFlow 在所有核心指标上均达到最优：

**HumanML3D 数据集：**
- R-Precision Top-1 达到 **0.563**，为所有方法中最高
- FID 降至 **0.032**，显著优于已有方法
- MultiModal Distance（MM-Dist）为 **2.691**，同样为最优

**KIT-ML 数据集：**
- R-Precision Top-1 达到 **0.482**
- FID 降至 **0.135**
- MM-Dist 为 **2.552**

三个指标分别衡量语义对齐精度（R-Precision）、生成质量与分布匹配（FID）以及文本-运动特征空间距离（MM-Dist），MotionHiFlow 在三个维度上的一致性优势表明分层流匹配框架能够同时优化语义一致性和运动细节。所有实验均重复 20 次并报告 95% 置信区间，训练与推理设置与现有方法保持一致，保证了比较的公平性。

### 消融实验

#### 分层流匹配的有效性

Table 2 评估了不同时间尺度设置下的系统性能。关键发现包括：

- **分层流匹配（尺度 [1/3, 2/3, 1]）相比单尺度匹配显著降低 FID 和 MM-Dist**，验证了多尺度逐步生成策略的有效性。
- **仅在粗尺度上训练的模型有时能获得比精细尺度模型更好的语义对齐**。这一反直觉的结果进一步支持了论文的核心洞察：粗尺度运动富含语义信息，过早引入细节反而可能干扰语义学习。

#### 关键组件的贡献

Table 3 对系统各组件的贡献进行了消融分析。从基础配置出发逐步添加组件：

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MotionHiFlow_Text_t/figures/007_Table_3.jpg]]
*Table 3: Evaluation of key components on the system performance*

- 引入 **TMDiT**（双流文本-运动 DiT）后，FID 出现明显下降
- 进一步引入**拓扑感知 VAE**（以图卷积网络显式建模人体骨架拓扑）后，FID 从 0.074 进一步降至 **0.032**

两项组件的叠加带来了 FID 约 57% 的相对改善，证明双流条件机制和拓扑感知压缩编码对生成质量具有实质性贡献。

### 用户研究

Figure 5 展示了用户研究的结果，从真实性和文本对齐两个维度对比了 MotionHiFlow 与 **MoMask**、**MoGenTS**（Yuan et al., NeurIPS 2024）以及真实运动（Ground Truth）。MotionHiFlow 在两个维度上均优于基线方法，表明分层生成策略不仅提升了自动指标，也在人类主观评价中获得认可。

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MotionHiFlow_Text_t/figures/006_Figure_5.jpg]]
*Figure 5: Results of a user study comparing the realism and text alignment of various methods,including our approach, with baseline competitors (MoMask,MoGenTS),and Ground Truth*

### 定性分析

Figure 4 提供了三个不同文本描述下的生成运动可视化对比。关键帧显示 MotionHiFlow 生成的运动会方向（以绿线表示）与文本描述一致，而基线方法（以红线表示）在部分帧上出现了方向错误。这说明分层流匹配框架在时序连贯性和细粒度语义对齐方面具有优势。

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MotionHiFlow_Text_t/figures/005_Figure_4.jpg]]
*Figure 4: Visualompasosetweediereetosivethreedistictextdesciptios.Onlyeyframsaredispad,withrow indicatingthearactersmovemntdirecti.Gnlineseoteoretdeciosileedlinesidcateicoectdirectios atdoot match the text content.Refer to the demo video for complete motion clips and more visualization results*

### 实验设置摘要

为保证结果可复现，论文提供了详细的训练配置：
- **Motion VAE**：AdamW 优化器，batch size 256，初始学习率 2×10⁻⁴，MultiStepLR 调度器在 50% 和 75% 训练步数时衰减至原来的 0.2
- **TMDiT**：AdamW 优化器，batch size 64，初始学习率 2×10⁻⁴，同样采用 MultiStepLR 衰减策略
- 分层流匹配采用三层流，尺度分别为 [1/3, 2/3, 1]
- TMDiT 共 9 个 block，前 3 个 block 的双分支使用独立参数，后 6 个 block 共享参数

### 待验证项

Table 1 中各基线方法的具体数值在分析材料中未精确提取，建议在最终版本中补充完整对比数据。此外，论文未报告推理时间与计算开销，分层多尺度策略在实际部署中的效率需要进一步评估。

### 补充图表

![[assets/figures/papers/paper_list_l13_https_openaccess_thecvf_com_content_CVPR2026_html_Li_MotionHiFlow_Text_t/figures/004_Table.jpg]]

## 方法谱系与知识库定位

### 1. 核心问题定位

现有文本到运动生成方法普遍在单一时间尺度上操作，导致一个结构性矛盾：精细尺度有利于捕捉细节运动，但难以建立全局语义对齐；粗粒度尺度有利于语义理解，却丢失了时序细节。MotionHiFlow将这一瓶颈形式化为**尺度-语义权衡问题**，其核心因果机制在于：粗尺度运动保留了大部分文本语义信息（Figure 1显示降采样比0.2时R-precision仍保持稳定），因此可以先在低时间尺度上建立强语义锚点，再逐层注入细节。

### 2. 方法谱系与关键差异

MotionHiFlow位于**分层生成×流匹配×运动VAE**的方法交叉点，与以下基线形成明确差异：

**与扩散/流匹配方法的差异：**
- **MDM**（Tevet et al., ICLR 2023）：基于扩散模型在单一时间尺度上生成运动，缺乏跨尺度的语义-细节解耦机制。
- **MoGenTS**（Yuan et al., NeurIPS 2024）：采用扩散+VAE框架，但其VAE基于2D卷积，未显式建模人体拓扑结构；且生成过程仍在单一尺度完成。

**与掩码运动模型的差异：**
- **MoMask**和**MMM**（Pinyoanuntapong et al., CVPR 2024）：基于掩码建模的生成范式，通过迭代填充生成运动。MotionHiFlow与之根本不同：采用流匹配的ODE求解框架，且引入分层尺度策略，将生成过程显式分解为语义对齐→细节细化的递进阶段。

**关键设计变更：**

| 设计维度 | 基线做法 | MotionHiFlow方案 | 证据锚点 |
|---------|---------|-----------------|---------|
| 生成尺度策略 | 单一时间尺度 | 分层多尺度流匹配（K个阶段，尺度如[1/3, 2/3, 1]） | Section 3.4, Figure 2(a) |
| 跨尺度连接 | 直接上采样噪声数据 | 去噪-上采样-重噪过程保持噪声一致性 | Section 3.4, Eq. (8)-(10) |
| 位置编码 | 标准Transformer位置编码 | Joint RoPE集成时序位移、空间坐标和运动学树 | Section 3.5, Figure 3(b) |
| 运动VAE架构 | 2D卷积VAE（如MoGenTS） | 拓扑感知Graph CNN VAE | Section 3.5 |
| 文本条件方式 | 单一句子级嵌入 | 双流TMDiT处理词级文本嵌入 | Section 3.5, Figure 3(a) |

### 3. 知识库定位与适用边界

**方法定位：** MotionHiFlow属于**流匹配生成模型**家族，其分层设计借鉴了多尺度生成的思想，但通过流匹配的ODE框架实现了更简洁的跨尺度过渡。与扩散模型相比，流匹配避免了复杂的噪声调度；与掩码模型相比，提供了连续且可逆的生成路径。

**适用边界：**
- **已验证场景：** HumanML3D和KIT-ML数据集上的文本到运动生成，涵盖日常动作和简单交互。
- **潜在扩展但未验证：** 方法是否适用于其他骨架拓扑（如动物、多人物）或运动类型（如舞蹈、体育动作）需要进一步验证。拓扑感知VAE的图池化策略依赖于人体运动学树结构，迁移到不同骨架需重新设计图拓扑。
- **计算成本边界：** 分层尺度数量和具体尺度的选择对计算成本的影响尚未系统分析。当前采用三层流匹配（尺度[1/3, 2/3, 1]），更多层级可能进一步提升质量但增加推理开销。

### 4. 局限与开放问题

**已识别的局限：**
论文未明确列出局限性，但从实验设计可以推断：
- 跨尺度过渡的数学保证：去噪-上采样-重噪过程如何严格保证噪声一致性，论文未提供理论证明，仅通过实验验证有效性。
- 尺度选择的通用性：当前尺度配置[1/3, 2/3, 1]基于经验选择，缺乏对最优尺度组合的理论分析或自动化搜索策略。

**开放问题：**
1. **跨尺度噪声一致性的理论基础：** Eq. (8)-(10)定义的跨尺度过渡过程依赖于启发式设计，其与流匹配ODE理论框架的兼容性需要更严格的数学分析。
2. **拓扑感知VAE的池化策略影响：** 图池化操作如何影响运动重建质量和生成多样性，不同的池化策略（如基于运动学距离vs.基于语义分组）对最终性能的影响未充分探索。
3. **分层尺度的自动化选择：** 能否根据输入文本的复杂度自适应调整尺度数量和分布，而非固定三层结构？
4. **与其他模态的扩展：** 方法框架是否适用于音频到运动、视频到运动等其他条件生成任务，需要进一步研究。
5. **Table 1基线数值补充：** 当前分析中Table 1的baseline具体数值未精确提取，需要手动验证各对比方法在HumanML3D和KIT-ML上的完整指标。

## 原文 PDF

![[paperPDFs/CVPR_2026/MotionHiFlow_Text_to_Motion_via_Hierarchical_Flow_Matching.pdf]]