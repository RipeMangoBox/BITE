---
title: Focal-General Diffusion Model with Semantic Consistent Guidance for Sign Language Production
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Focal_General_Diffusion_Model_with_Semantic_Consistent_Guidance_for_Sign_Language_Production.pdf
project_link: null
code_link: null
aliases:
- FGDMF
- FGDMSCGSLP
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过两阶段去噪框架（局部关节建模和全局序列建模）介入姿态生成的依赖结构，并利用语义一致性引导（SCG）在扩散训练过程中注入跨模态语义监督。
primary_logic: 将姿态生成任务分解为先建模局部关节依赖、再聚合全局序列连贯性的两阶段过程，能够有效克服现有方法的全局偏差；在扩散模型中引入基于 CTC 的语义对齐损失，可以在不破坏生成多样性的前提下显著提升语义一致性。
claims:
- 组合 Focal 阶段与 SCG 策略后，模型在 PHOENIX14T 上相比基线将 WER 降低 -8.78%/-9.06%。
- 在 ASGCN 中移除上下文相关矩阵 A_a^i 导致 BLEU-1 严重下降（DEV -4.80%/TEST -4.16%），移除语义掩码 M^i 也引起明显下降，验证了局部自适应建模和语义信息的重要性。
- PHOENIX14T-TEST 上 WER = 70.70
- PHOENIX14T-TEST 上 BLEU-4 = 9.67
---

# Focal-General Diffusion Model with Semantic Consistent Guidance for Sign Language Production

> [!tip] 核心洞察
> 将姿态生成任务分解为先建模局部关节依赖、再聚合全局序列连贯性的两阶段过程，能够有效克服现有方法的全局偏差；在扩散模型中引入基于 CTC 的语义对齐损失，可以在不破坏生成多样性的前提下显著提升语义一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向手语生成的分层扩散模型与语义一致性引导 |
| 英文题名 | Focal-General Diffusion Model with Semantic Consistent Guidance for Sign Language Production |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yu_Focal-General_Diffusion_Model_with_Semantic_Consistent_Guidance_for_Sign_Language_CVPR_2026_paper.html) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Focal-General Diffusion Model (FGDM) |
| Dataset | PHOENIX14T-TEST, USTC-CSL Split-I, USTC-CSL Split-II |

> [!tip] 效果简介
> - PHOENIX14T-TEST 上，WER 70.70 vs Sign-IDD (-8.45% (vs. Sign-IDD))；BLEU-4 9.67 vs Sign-IDD (N/A (absolute SOTA))。
> - USTC-CSL Split-I 上，BLEU-1 92.04 vs Sign-IDD (+1.51%)。
> - USTC-CSL Split-II 上，BLEU-1 43.61 vs Sign-IDD (N/A (absolute SOTA))。

## 概要

**问题瓶颈**：手语生成（SLP）中的 Gloss-to-Pose (G2P) 子任务面临一个核心矛盾——现有方法（包括自回归框架和扩散模型）普遍采用全局建模策略，忽视关节级别的细粒度空间依赖，导致生成姿态的局部细节失真；同时，训练过程仅依赖回归损失，缺乏有效的跨模态语义监督，使得生成序列的语义一致性难以保证。

**核心洞察**：将姿态生成分解为“先建模局部关节依赖，再聚合全局序列连贯性”的两阶段过程，能够有效克服全局偏差；在扩散训练中引入基于 CTC 的语义对齐损失，可以在不破坏生成多样性的前提下，显著提升语义一致性。

**方法定位**：本文提出**分层扩散模型（Focal-General Diffusion Model, FGDM）**，包含三个关键创新：
- **两阶段去噪框架**：Focal 阶段通过自适应图卷积（ASGCN）与时间卷积（TCN）建模关节级别的空间-时间依赖；General 阶段通过 Transformer 解码器实现全局序列连贯性。
- **帧级自适应图卷积（ASGCN）**：整合上下文相关性、骨骼拓扑和语义条件，为每一帧动态构建邻接矩阵，替代传统的帧间共享静态图卷积。
- **语义一致性引导（SCG）**：通过 V2S 适配器和语义解码器将视觉特征投影到语义空间，并施加时间加权的 CTC 损失，实现跨模态语义监督。

**主要结果**：在 PHOENIX14T 测试集上，FGDM 的 WER 降至 70.70%，较此前最优的扩散方法 **Sign-IDD**（Tang et al., AAAI 2025）降低 8.45%，同时 BLEU-4 达到 9.67% 的新 SOTA。消融实验表明，引入 Focal 阶段使 WER 相对基线降低 5.85%，叠加 SCG 后进一步降至 9.06%，验证了各组件的独立贡献。在 USTC-CSL 数据集上，FGDM 同样在两个划分方案上全面超越现有方法。



手语生成（Sign Language Production, SLP）旨在将口语文本自动转化为连续的手语姿态序列，是打破聋人与听人之间沟通壁垒的关键技术。典型的 SLP 流程包含两个串联子任务：文本到注释（Text-to-Gloss, T2G）和注释到姿态（Gloss-to-Pose, G2P）。其中 G2P 负责将离散的手语注释序列映射为连续、自然的人体关键点坐标，其生成质量直接决定最终手语的可懂度与自然度。本文聚焦于 G2P 这一核心环节。

当前 G2P 方法面临两个相互关联的瓶颈。其一，现有工作普遍采用全局建模策略——无论是自回归框架（如 **Progressive Transformer**，Saunders et al., ECCV 2020）还是扩散框架（如 **Sign-IDD**，Tang et al., AAAI 2025；**G2P-DDM**，Xie et al., AAAI 2024），均以整个姿态序列为单元进行生成，忽略了对关节级别细粒度依赖的显式建模。这导致生成姿态的局部细节（如手指形态、手腕角度）容易失真，尤其在快速过渡或复杂手势中表现明显。其二，主流方法仅依赖回归损失（L1/L2）进行监督，缺乏有效的跨模态语义对齐机制，使得生成姿态虽在数值上接近真值，却在语义层面与目标注释序列产生偏差。

上述问题的根源在于：G2P 任务本质上要求模型同时掌握“局部关节协同”与“全局序列连贯”两个层次的依赖结构，而现有方法将二者混杂在单一建模过程中，造成全局偏差对局部细节的淹没效应。此外，扩散模型虽然展现出优异的生成多样性，但其随机采样特性在没有语义约束的情况下，难以保证生成结果与输入注释的严格对应。

针对这些缺口，本文提出**分层扩散模型（Focal-General Diffusion Model, FGDM）**，核心动机是将 G2P 分解为两个阶段：先通过 Focal 阶段建模关节级空间-时间依赖，再通过 General 阶段实现全局序列的连贯聚合。同时引入**语义一致性引导（Semantic Consistent Guidance, SCG）**，在扩散训练过程中注入基于 CTC 对齐的跨模态语义监督，在不牺牲生成多样性的前提下显著提升语义保真度。



## 核心方法与创新机理

FGDM 的核心创新在于对 Gloss-to-Pose (G2P) 去噪过程的依赖结构进行重新设计，并引入跨模态语义监督，从而系统性地解决了现有方法的两大瓶颈：**全局建模偏差导致的关节级细节失真**，以及**缺乏语义监督导致的生成姿态与语义不一致**。

### 1. 两阶段去噪范式：Focal–General 框架

现有扩散式 G2P 方法（如 **Sign-IDD** (Tang et al., AAAI 2025)、**G2P-DDM** (Xie et al., AAAI 2024)）普遍采用单一阶段的全局去噪网络，这种结构在捕捉手语姿态中细粒度的关节间依赖关系时存在天然不足。FGDM 将去噪过程解耦为两个阶段（Figure 2）：

- **Focal 阶段**：专注于**关节级依赖建模**。该阶段由堆叠的 ASGCN 与 TCN 构成，遵循空间-时间解耦设计——ASGCN 负责建模帧内关节间的空间依赖，TCN 负责建模关节沿时间维度的动态变化。这种设计使模型能够精细地刻画局部姿态细节，而非被全局信息淹没。

- **General 阶段**：在 Focal 阶段输出基础上进行**全局序列连贯性建模**。该阶段实现为 Transformer 解码器，通过自注意力机制聚合整个序列的上下文信息，确保生成姿态在时序上的平滑与自然。

两阶段之间通过 F2G 转换（$X_t^g = T_{FG}(X_t^{f_o}) + PE$）衔接，将 Focal 阶段的空间-时间特征重塑为 General 阶段的序列输入，并添加位置编码以保留时序信息。

### 2. 帧级自适应图卷积：ASGCN

传统 G2P 方法使用的图卷积通常采用帧间共享的静态邻接矩阵，无法适应不同帧中关节依赖关系的动态变化。FGDM 在 Focal 阶段提出了**帧级自适应图卷积 ASGCN**，其核心是构建帧级自适应的邻接矩阵 $\mathbf{A}^i$（Figure 3）：

$$\mathbf{A}^i = (\mathbf{A}_a^i + \mathbf{A}_b^i) \odot \mathcal{M}^i$$

该矩阵由三个组件融合而成：

- **上下文相关矩阵** $\mathbf{A}_a^i$：通过计算当前帧与相邻帧（窗口 $[-n, n]$）之间的关节特征相似度 $\mathbf{C}^i = \{ \mathbf{W}_\psi X^i \cdot \mathbf{W}_\tau X^{i+j} \mid j \in [-n, n] \}$，捕获时序上下文中的关节协同变化模式。

- **骨骼拓扑矩阵** $\mathbf{A}_b^i$：编码人体骨架的物理连接先验，为图结构提供稳定的拓扑基础。

- **语义掩码** $\mathcal{M}^i$：将 gloss 语义信息注入图结构。具体而言，首先从 gloss 特征序列生成原型掩码集 $M = \{ \mathcal{MG}(G^l) \mid l \in [1, L] \}$，然后通过帧-词对齐权重 $w^i = Softmax( (\mathbf{W}_{\psi'} \frac{1}{J} \sum_{j=1}^{J} X_j^i) \cdot (\mathbf{W}_{\tau'} G) )$ 对原型掩码进行加权聚合，最终经缩放 sigmoid 映射至 $[0, 2]$ 区间，实现对连接强度的增强或抑制。

消融实验（Table 5）提供了决定性证据：移除上下文相关矩阵 $\mathbf{A}_a^i$ 导致 BLEU-1 在 DEV/TEST 上分别下降 4.80%/4.16%，WER 上升 2.59%/4.56%；移除语义掩码 $\mathcal{M}^i$ 同样引起显著性能退化（BLEU-1 下降 3.09%/2.83%，WER 上升 1.09%/3.29%）。这验证了自适应上下文建模和语义条件注入对精确定位关节级依赖的关键作用。

### 3. 语义一致性引导：SCG

现有 G2P 方法通常仅依赖回归损失（如 L1/L2）进行监督，这无法显式保证生成姿态与目标 gloss 序列之间的语义对齐。FGDM 提出的**语义一致性引导（SCG）** 机制在扩散训练过程中引入了跨模态语义监督，其工作流程如下：

1. **V2S Adapter**：将 General 阶段的视觉特征 $X_t^{G_o}$ 通过两层线性层与 ReLU 激活映射为中间过渡特征 $X_t^{trans}$，实现视觉空间到语义空间的桥接。

2. **语义解码器**：由局部语义解码器（LSD）、全局语义解码器（GSD）和 Gloss 分类器级联组成，将过渡特征解码为语义序列 $y_t^o$。

3. **CTC 语义对齐损失**：SCG 的核心是带时间权重的 CTC 损失：

$$\mathcal{L}_{\mathrm{SCG}} = -\frac{1}{e^{\alpha \frac{t}{T}}} \log \sum_{\pi \in \mathcal{B}^{-1}(\mathcal{G})} p(\pi \mid y_t^o)$$

其中时间权重因子 $e^{\alpha \frac{t}{T}}$ 随扩散时间步 $t$ 增大而衰减——在去噪初期（高噪声阶段）施加更强的语义引导，在去噪后期（低噪声阶段）逐步减弱引导强度。这种设计使得语义监督能够在不破坏扩散模型生成多样性的前提下，有效约束生成姿态的语义一致性。

总损失函数将回归损失与 SCG 损失联合优化：

$$\mathcal{L} = \mathcal{L}_{joint} + \lambda \cdot \mathcal{L}_{bone} + \gamma \cdot \mathcal{L}_{SCG}$$

消融实验（Table 3）表明：在仅含 General 阶段的基线上引入 Focal 阶段后，DEV 上 WER 降低 4.43%/5.85%（DEV/TEST）；进一步叠加 SCG 策略后，WER 较基线总计降低 8.78%/9.06%，获得最佳效果。这证明两阶段去噪与语义一致性引导之间存在显著的协同增益。

### 方法局限性

值得注意的是，当前语义掩码生成器 $\mathcal{MG}(\cdot)$ 仅采用简单的线性层实现，其表达能力有限，可能无法充分挖掘 gloss 特征中的语义信息。此外，FGDM 目前仅针对 G2P 子任务设计，尚未涵盖从文本到姿态的完全端到端建模。



FGDM 的核心设计理念是将姿态去噪过程分解为“先局部关节建模、再全局序列聚合”的两个阶段，并引入跨模态语义一致性引导，从而克服现有 G2P 方法因全局偏差导致的局部细节失真和语义不一致问题。

### 两阶段去噪范式

FGDM 的框架由 **Focal 阶段** 和 **General 阶段** 串联构成。给定从 gloss 序列上采样得到的初始噪声姿态序列 $X_T$，模型通过逐步去噪恢复出目标姿态 $\hat{X}_0$。

- **Focal 阶段**：负责帧级关节依赖的精细建模。该阶段由 $L_1$ 层堆叠的 ASGCN 与 TCN 组成，其中 ASGCN 建模空间维度上关节间的依赖关系，TCN 则捕获时间维度上的关节动态变化，两者遵循时空解耦设计。
- **F2G 转换**：Focal 阶段的输出 $X_t^{f_o}$ 经过重塑与位置编码注入后，转换为 General 阶段的输入 $X_t^g$。
- **General 阶段**：基于 Transformer 解码器实现，由 $L_2$ 层堆叠构成。它以全局自注意力的方式对 Focal 阶段输出的局部特征进行聚合，确保整段姿态序列的连贯性。

### 语义一致性引导（SCG）

在 General 阶段输出 $X_t^{G_o}$ 之后，FGDM 引入 SCG 模块提供辅助语义监督。该模块包含三个子组件：

1. **V2S Adapter**：将视觉特征 $X_t^{G_o}$ 映射到中间语义过渡空间，得到 $X_t^{trans}$。
2. **Semantic Decoder**：由局部语义解码器（LSD）和全局语义解码器（GSD）组成，逐步将过渡特征解码为语义序列 $y_t^g$。
3. **Gloss Classifier**：对 $y_t^g$ 进行分类，输出 $y_t^o$，并通过 CTC 对齐损失 $\mathcal{L}_{\mathrm{SCG}}$ 与目标 gloss 序列建立语义约束。

SCG 的独特之处在于，它在扩散训练过程中首次引入了跨模态语义对齐损失，在不破坏生成多样性的前提下，显著提升了生成姿态与目标语义的一致性。

### 训练与推理流程

在训练阶段，模型同时优化回归损失（关节级 L1 损失 $\mathcal{L}_{joint}$ 与骨骼长度损失 $\mathcal{L}_{bone}$）和语义一致性损失 $\mathcal{L}_{SCG}$，总损失为三者的加权和。在推理阶段，模型采用 DDIM 式采样策略，从纯噪声出发，通过预测 $\hat{X}_0$ 和噪声 $\epsilon_t$ 进行迭代更新，逐步生成最终姿态序列。SCG 模块仅在训练时参与语义监督，推理时无需额外计算。

整个框架的创新点在于：通过 Focal–General 两阶段设计改变了去噪网络的依赖结构，使模型能够先关注局部关节的精确建模，再聚合为全局连贯序列；同时通过 SCG 将语义信号注入扩散训练，实现了跨模态的细粒度对齐。

### 补充图表

![[assets/figures/papers/paper_list_l989_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Focal_General_Diffu/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of FGDM during training and inference. In training, the noisy sequence*

![[assets/figures/papers/paper_list_l989_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Focal_General_Diffu/figures/001_Figure_1.jpg]]
*Figure 1: Top: Illustration pipeline of SLP, including T2G and G2P. T2G converts text into glosses, while G2P maps each gloss to its corresponding pose sequence and generates smooth transitions to ensure naturalness. This work primarily focuses on G2P. Bottom: Comparison with existing methods on the challenging PHOENIX14T [5] dataset. Our approach achieves new SOTA results across all metrics on both DEV and TEST sets*



### 1. 两阶段去噪框架

FGDM 的核心创新在于构建了一个“先局部、后全局”的两阶段去噪网络，将姿态生成任务分解为**Focal 阶段**（关节级依赖建模）与**General 阶段**（全局序列连贯性建模）的递进过程。这一设计直接回应了现有方法因全局建模偏差而导致局部细节失真的瓶颈。

**Focal 阶段**由 $L_1$ 层堆叠的 ASGCN 与 TCN 构成，采用空间-时间解耦设计：ASGCN 负责建模帧内关节间的空间依赖，TCN 则捕捉关节沿时间维度的动态变化。该阶段的输出 $X_t^{f_o}$ 经 **F2G 转换** 重塑后馈入 General 阶段：

$$X_t^g = T_{FG}(X_t^{f_o}) + PE \tag{10}$$

其中 $PE$ 为位置编码。**General 阶段**实现为 $L_2$ 层堆叠的 Transformer 解码器，通过自注意力机制聚合全局序列信息：

$$X_t^{g'} = MHA(Q, K, V) \mid_{Q=K=V=X_t^g} \tag{11}$$

最终，经层归一化与 MLP 输出预测的干净姿态 $\hat{X}_0$。

### 2. 帧级自适应图卷积 (ASGCN)

ASGCN 是 Focal 阶段的核心算子，通过构造**帧级自适应邻接矩阵** $\mathbf{A}^i$ 替代传统静态图卷积，实现灵活精确的手语姿态建模。其图卷积操作采用深度可分离设计：

$$X_{out}^i = \mathbf{W}_\theta \sum_{k}^{K_v} \mathbf{W}_{\delta k} \odot (X_{in}^i \mathbf{A}_k^i) \tag{2}$$

自适应邻接矩阵由三个组件综合生成：

$$\mathbf{A}^i = (\mathbf{A}_a^i + \mathbf{A}_b^i) \odot \mathcal{M}^i \tag{3}$$

- **上下文相关矩阵 $\mathbf{A}_a^i$**：通过计算当前帧与邻域帧 $[i-n, i+n]$ 之间的特征相关性得到，捕捉帧间动态依赖：

$$\mathbf{C}^i = \{ \mathbf{W}_\psi X^i \cdot \mathbf{W}_\tau X^{i+j} \mid j \in [-n, n] \} \tag{4}$$

- **骨骼拓扑矩阵 $\mathbf{A}_b^i$**：编码人体关节的固有物理连接关系。
- **语义掩码 $\mathcal{M}^i$**：将图结构与 gloss 语义对齐，是 ASGCN 的关键创新。其生成流程为：
  1. 从 gloss 特征序列 $G = G^1, G^2, ..., G^{\bar{L}}$ 通过掩码生成器 $\mathcal{MG}(\cdot)$（当前实现为线性层）构建原型掩码集：

$$M = \{ \mathcal{MG}(G^l) \mid l \in [1, L] \} \tag{6}$$

  2. 计算第 $i$ 帧与各 gloss 的相似度权重，聚合原型掩码：

$$w^i = Softmax\left( (\mathbf{W}_{\psi'} \frac{1}{J} \sum_{j=1}^{J} X_j^i) \cdot (\mathbf{W}_{\tau'} G) \right) \tag{7}$$

  3. 通过缩放 sigmoid 将聚合掩码映射至 $[0, 2]$，实现对连接强度的增强或抑制：

$$\mathcal{M}^i = 2 \cdot \sigma(\mathbf{W}_s \bar{M}^i) \tag{9}$$

消融实验（Table 5）表明，移除 $\mathbf{A}_a^i$ 导致 BLEU-1 下降 -4.80%/-4.16%（DEV/TEST），WER 上升 +2.59%/+4.56%；移除 $\mathcal{M}^i$ 同样引起显著退化（BLEU-1: -3.09%/-2.83%），验证了上下文建模与语义信息对关节级建模的关键作用。

### 3. 语义一致性引导 (SCG)

SCG 机制在扩散训练过程中引入跨模态语义监督，通过 **V2S Adapter** 与 **语义解码器** 将视觉特征投影至语义空间，并利用 CTC 对齐损失约束生成姿态与 gloss 序列的语义一致性。

- **V2S Adapter**：将 General 阶段输出 $X_t^{G_o}$ 转换为语义空间的中间表示 $X_t^{trans}$，作为视觉到语义的桥梁。
- **语义解码器**：由局部语义解码器 (LSD)、全局语义解码器 (GSD) 和 Gloss 分类器级联构成，输出语义预测 $y_t^o$。
- **SCG 损失**：采用带时间权重的 CTC 损失，在扩散早期施加较强语义约束，随去噪进程逐步减弱：

$$\mathcal{L}_{\mathrm{SCG}} = -\frac{1}{e^{\alpha \frac{t}{T}}} \log \sum_{\pi \in \mathcal{B}^{-1}(\mathcal{G})} p(\pi \mid y_t^o) \tag{18}$$

### 4. 训练与推理

**训练总损失** 联合回归损失与语义一致性损失：

$$\mathcal{L} = \underbrace{\mathcal{L}_{joint} + \lambda \cdot \mathcal{L}_{bone}}_{\mathrm{Regression\ Loss}} + \gamma \cdot \mathcal{L}_{SCG} \tag{19}$$

其中 $\mathcal{L}_{joint} = \frac{1}{S} \sum_{s=1}^{S} \| X_0^s - \hat{X}_0^s \|_1$ 为关节坐标的 L1 损失。

**推理采样** 采用 DDIM 式更新，从噪声逐步恢复干净姿态：

$$X_{t'} = \sqrt{\bar{a}_{t'}} \cdot \hat{X}_0 + \sqrt{1 - \bar{a}_{t'} - \sigma_t^2} \cdot \epsilon_t + \sigma_t \cdot \epsilon \tag{13}$$

消融实验（Table 3）证实，引入 Focal 阶段后 DEV 上 BLEU-1 提升至 28.09%，WER 降低 -4.43%/-5.85%；叠加 SCG 后 WER 进一步降低至 -8.78%/-9.06%（较基线），验证了两阶段去噪与语义引导的协同增益。

### 补充图表

![[assets/figures/papers/paper_list_l989_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Focal_General_Diffu/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of ASGCN. Taking the i-th frame as an example, ASGCN constructs a frame-wise adaptive adjacency matrix by integrating (a) contextual correlations*



## 实验与关键发现

### 核心主张与证据强度

FGDM 的核心主张可以拆解为两个因果杠杆：**Focal 阶段**通过解耦关节级依赖来纠正全局建模偏差，**SCG 策略**则在扩散训练中注入跨模态语义监督以提升语义一致性。消融实验直接验证了这一因果链：以 General 阶段为基线，引入 Focal 阶段后，PHOENIX14T DEV 集上 BLEU-1 提升至 28.09%，BLEU-4 提升至 9.84%，WER 降低 -4.43%/-5.85%（DEV/TEST）；在此基础上叠加 SCG 策略，WER 进一步降低至 -8.78%/-9.06%，达到最佳效果（Table 3）。上述消融证据置信度较高（0.95），构成了支撑核心主张的决定性证据链。

![[assets/figures/papers/paper_list_l989_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Focal_General_Diffu/figures/007_Table_3.jpg]]
*Table 3: Ablations for the main innovations on PHOENIX14T, where the General stage is regarded as our baseline*

### 主实验结果：PHOENIX14T

Table 1 汇总了 PHOENIX14T 上的全面对比。FGDM 在所有指标上均达到 SOTA：DEV 集 BLEU-4 为 9.48，TEST 集 BLEU-4 为 9.67；WER 分别为 72.22 和 70.70。与最近的扩散基线 **Sign-IDD**（Tang et al., AAAI 2025）相比，TEST 集 WER 降低 -8.45%，BLEU-4 取得绝对值最优。与自回归 SOTA **Progressive Transformer**（Saunders et al., ECCV 2020）及多假设聚合方法 **Gloss-driven conditional diffusion**（Tang et al., TOMM 2025）相比，FGDM 在所有指标上均有显著优势。表中以 “†” 标注了作者复现的结果（如 GEN-OBT），保证了比较的公平性。

![[assets/figures/papers/paper_list_l989_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Focal_General_Diffu/figures/004_Table_1.jpg]]
*Table 1: Comparison with existing methods on PHOENIX14T. ‘†’ indicates reproduced results, while ‘–’ denotes results missing in the original paper. Best results are in bold, and the second-best are underlined*

### 主实验结果：USTC-CSL

Table 2 展示了 USTC-CSL 数据集上两种划分方案的结果。在 Split-I 上，FGDM 的 BLEU-1 达到 92.04，较 Sign-IDD 提升 +1.51%，BLEU-4 提升 +3.92%，WER 降低 -1.03%。在更具挑战性的 Split-II 上，FGDM 同样取得绝对 SOTA（BLEU-1 43.61），显著优于所有对比方法。跨数据集的稳定优势表明，Focal–General 两阶段框架与 SCG 策略的组合具有良好的泛化能力。

![[assets/figures/papers/paper_list_l989_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Focal_General_Diffu/figures/005_Table_2.jpg]]
*Table 2: Comparison with existing methods on USTC-CSL. Split-I and Split-II refer to two partitioning schemes [13]. ’†’ indicates reproduced results. Best results are in bold, and the second-best are underlined*

### 消融研究：ASGCN 内部组件

Table 5 对 ASGCN 的三个关键组件进行了消融：上下文相关矩阵 $A_a^i$、骨骼拓扑矩阵 $A_b^i$ 和语义掩码 $M^i$。移除 $A_a^i$ 导致最大性能下降（DEV BLEU-1: -4.80%，TEST BLEU-1: -4.16%；DEV WER: +2.59%，TEST WER: +4.56%），验证了帧间上下文相关性对关节建模的核心作用。移除语义掩码 $M^i$ 同样引起显著下降（DEV BLEU-1: -3.09%，TEST BLEU-1: -2.83%；DEV WER: +1.09%，TEST WER: +3.29%），证明语义条件对图结构对齐的重要性。移除 $A_b^i$ 的影响相对较小，表明骨骼拓扑作为静态先验，其贡献低于自适应建模组件。

![[assets/figures/papers/paper_list_l989_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Focal_General_Diffu/figures/006_Table_5.jpg]]
*Table 5: Ablations for*

### 超参数消融

Table 4 展示了 Focal 阶段层数 $L_1$ 和 General 阶段层数 $L_2$ 的消融结果。实验表明，$L_1$ 和 $L_2$ 的取值需要在局部建模能力与全局连贯性之间取得平衡，具体最优配置可参考原表（此处缺少精确数值，需手动查阅原文确认）。

![[assets/figures/papers/paper_list_l989_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Focal_General_Diffu/figures/008_Table_4.jpg]]
*Table 4: Ablations for parameters*

### 定性分析与失败模式

Figure 4 对比了 FGDM 与 PT、Sign-IDD 的生成质量。在放大区域 (a)–(c) 中，FGDM 生成的手部细节更自然且与 GT 姿态一致；即使在 GT 不准确的情况下（如 (b)(c)），FGDM 仍能产生逼真结果。Figure 5 进一步对比了有无 Focal 阶段的生成效果，验证了 Focal 阶段对局部细节建模的贡献。

![[assets/figures/papers/paper_list_l989_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Focal_General_Diffu/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative comparison of generation quality with previous methods on PHOENIX14T. We compare FGDM with PT [31] and Sign-IDD [41], together with the corresponding gloss sequence, raw images, and ground truth (GT) poses. Panels (a)–(c) present zoomedin regions where FGDM generates more natural and GT-consistent hand details. Even when the GT is inaccurate (as in (b) (c)), FGDM still produces realistic results, demonstrating its superior performance*

![[assets/figures/papers/paper_list_l989_https_openaccess_thecvf_com_content_CVPR2026_html_Yu_Focal_General_Diffu/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative comparison of generation quality without and with the Focal stage (w/o Focal vs. w/ Focal). Hand details are enlarged for better observation*

### 已知局限

1. 语义掩码生成器 $\mathcal{MG}(\cdot)$ 目前仅使用线性层实现，表达能力有限，可能无法充分挖掘语义信息来指导图结构。
2. 方法仅针对 G2P 子任务，尚未涵盖文本到姿态的完全端到端建模，实际部署时需依赖上游 T2G 模块的质量。



## 定位与知识库关联

### 1. 方法继承与基线关系

**FGDM** 的核心任务定位在 **Gloss-to-Pose (G2P)** 子任务，其方法谱系可追溯至两条主要技术路线：**自回归序列建模** 与 **扩散概率模型**。

在自回归路线中，**Progressive Transformer (PT)**（Saunders et al., ECCV 2020）是 G2P 任务的代表性 SOTA 方法，采用渐进式解码策略生成姿态序列。**GEN-OBT**（Tang et al., ACM MM 2022）则引入在线回译机制作为强基线。这类方法的共同局限在于全局建模偏差——它们侧重于序列整体的连贯性，而忽略了关节级别的细粒度依赖关系，导致局部细节失真。

在扩散模型路线中，**G2P-DDM**（Xie et al., AAAI 2024）首次将离散扩散模型引入 G2P 任务；**Gloss-driven conditional diffusion**（Tang et al., TOMM 2025）进一步采用多假设聚合策略；**Sign-IDD**（Tang et al., AAAI 2025）则通过象似性解耦（iconicity disentanglement）达到该路线下的 SOTA 水平。然而，这些扩散方法均采用单一阶段的去噪网络，缺乏对关节级依赖结构的显式建模。

FGDM 的差异化突破在于**改变去噪网络的内部结构**（changed slot：去噪网络结构），将单一全局建模替换为 **Focal–General 两阶段范式**：Focal 阶段通过 ASGCN 建模关节级空间依赖，General 阶段通过 Transformer 解码器实现全局序列连贯。这一设计直接回应了现有方法“全局偏差”的瓶颈问题。

### 2. 技术增量与因果机制

FGDM 的技术增量可分解为三个关键模块：

**（1）帧级自适应图卷积（ASGCN）**：相较于基线方法中帧间共享的静态图卷积，ASGCN 引入三个可验证的改进：
- **上下文相关矩阵** $A_a^i$：通过多帧特征交互捕捉时序上下文中的关节相关性（公式 4）。
- **语义掩码** $\mathcal{M}^i$：从 gloss 特征生成原型掩码集，经帧-词对齐权重聚合后，通过缩放 sigmoid 映射至 $[0,2]$，实现对图连接强度的增强或抑制（公式 6–9）。消融实验表明，移除 $A_a^i$ 导致 BLEU-1 下降 -4.80%/-4.16%、WER 上升 +2.59%/+4.56%；移除 $\mathcal{M}^i$ 导致 BLEU-1 下降 -3.09%/-2.83%、WER 上升 +1.09%/+3.29%，验证了这两项设计的因果重要性。

**（2）语义一致性引导（SCG）**：现有扩散方法仅依赖回归损失（L1/L2），缺乏跨模态语义监督。SCG 通过 V2S Adapter 和语义解码器将视觉特征投影至语义空间，并引入基于 CTC 的时间加权语义对齐损失 $\mathcal{L}_{\mathrm{SCG}}$（公式 18），在不破坏扩散生成多样性的前提下显著提升语义一致性。消融实验表明，添加 SCG 后所有指标均有显著提升。

**（3）两阶段去噪的协同效应**：消融实验（Table 3）揭示了 Focal 与 SCG 的协同机制——单独引入 Focal 阶段使 DEV 上 BLEU-1 提升至 28.09%、WER 降低 -4.43%/-5.85%；进一步组合 SCG 后，WER 较基线降低 -8.78%/-9.06%，达到最优效果。这表明 Focal 阶段解决了局部依赖建模的结构性缺陷，而 SCG 则从语义层面提供了互补的监督信号。

### 3. 适用边界与局限

FGDM 的适用边界受以下因素制约：

- **任务范围**：方法仅针对 G2P 子任务，尚未涵盖文本到姿态（T2P）的完全端到端建模。上游的 Text-to-Gloss (T2G) 模块仍需独立处理。
- **语义掩码的表达能力**：语义掩码生成器 $\mathcal{MG}(\cdot)$ 目前仅使用简单的线性层实现，其建模能力有限，可能无法充分挖掘 gloss 语义中的细粒度信息。作者将此列为明确的局限性。
- **数据集依赖**：主要验证在 PHOENIX14T（德语手语）和 USTC-CSL（中国手语）两个数据集上进行，跨语言、跨文化手语的泛化能力尚需进一步验证。

### 4. 开放问题

作者明确指出的开放问题包括：

1. **跨模态语义引导的深化**：如何在扩散框架中更有效地利用语义信号进行跨模态引导，仍是一个有待探索的开放问题。当前 SCG 仅在训练阶段提供辅助监督，推理时是否可引入无分类器引导（classifier-free guidance）等机制值得研究。

2. **语义掩码生成网络的增强**：能否设计更强大的语义掩码生成网络（如引入注意力机制或图神经网络），以进一步提升关节级建模精度，是直接的技术延伸方向。

3. **端到端扩展**：将 FGDM 的 Focal–General 范式扩展至完整的文本到姿态生成流程，实现 T2G 与 G2P 的联合优化，是向实用化迈进的关键步骤。



## 原文 PDF

![[paperPDFs/CVPR_2026/Focal_General_Diffusion_Model_with_Semantic_Consistent_Guidance_for_Sign_Language_Production.pdf]]
