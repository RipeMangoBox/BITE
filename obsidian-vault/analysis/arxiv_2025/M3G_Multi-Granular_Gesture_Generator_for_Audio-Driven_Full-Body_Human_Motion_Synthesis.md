---
title: "M3G: Multi-Granular Gesture Generator for Audio-Driven Full-Body Human Motion Synthesis"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/M3G_Multi-Granular_Gesture_Generator_for_Audio-Driven_Full-Body_Human_Motion_Synthesis.pdf
project_link: null
code_link: null
aliases:
- MMGGG
- M3G
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 多粒度VQ‑VAE（共享码本 + 多尺度TCN / TransTCN）配合多粒度Token预测器，实现从粗到细的动作模式建模与生成。
primary_logic: 将全身动作在不同时间粒度下编码为共享离散潜空间中的多粒度令牌序列，使模型能够捕捉不同尺度的动作模式，并通过预测这些多尺度令牌实现更精确、更自然的手势生成。
claims:
- M3G在几乎所有评估指标上均超越现有最先进方法
- MGVQ‑VAE显著降低了重建误差，证实其能有效捕捉和保留动作模式信息
- 主观A/B测试中参与者一致倾向于M3G生成的动作，认为其比CaMN和EMAGE更自然
- 多粒度表示、独立身体部位Latent、TransTCN等关键组件均对生成质量有显著贡献
---

# M3G: Multi-Granular Gesture Generator for Audio-Driven Full-Body Human Motion Synthesis

> [!tip] 核心洞察
> 将全身动作在不同时间粒度下编码为共享离散潜空间中的多粒度令牌序列，使模型能够捕捉不同尺度的动作模式，并通过预测这些多尺度令牌实现更精确、更自然的手势生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | M3G：音频驱动的全身人体动作多粒度手势生成器 |
| 英文题名 | M3G: Multi-Granular Gesture Generator for Audio-Driven Full-Body Human Motion Synthesis |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2505.08293) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | M3G (Multi-Granular Gesture Generator) |
| Dataset | BEAT |

> [!tip] 效果简介
> - BEAT 上，FGD (Fréchet Gesture Distance) 4.784e-1 vs State-of-the-art (CaMN, EMAGE, etc.) (Significantly lower (best among all compared methods))；MSE (Mean Squared Error) 7.291e-8 vs State-of-the-art (CaMN, EMAGE, etc.) (Significantly lower)；LVD (Lips-Voice Distance) 7.439e-8 vs State-of-the-art (Significantly lower)。

## 概述

现有基于VQ‑VAE的音频驱动手势生成方法普遍假设每个动作Token仅表示单帧静态姿态，无法建模具有不同持续时间的完整手势模式。这一单粒度假设导致生成的动作缺乏表现力和时序一致性，构成了该领域的核心瓶颈。

针对上述问题，本文提出**M3G（Multi‑Granular Gesture Generator）**框架。其核心思路是将全身动作在不同时间粒度下编码为共享离散潜空间中的多粒度Token序列，使模型能够捕捉从粗到细的多尺度动作模式，并通过预测这些多尺度Token实现更精确、更自然的手势生成。方法包含两个关键阶段：首先训练**多粒度VQ‑VAE（MGVQ‑VAE）**学习动作的离散多粒度表示，然后训练**多粒度Token预测器**从音频与文本特征中预测对应的Token序列以驱动动作重建。

在BEAT数据集上的实验结果表明，M3G在FGD（Fréchet Gesture Distance）、MSE等主要指标上均超越现有最先进方法（如CaMN、EMAGE），同时MGVQ‑VAE的重建误差显著低于标准VQ‑VAE。消融实验进一步证实，多粒度表示、TransTCN解码器、独立身体部位潜变量以及全身边缘潜变量等关键设计对生成质量均有显著贡献。主观A/B测试中，参与者一致倾向于M3G生成的动作，认为其比基线方法更自然。

该方法在动作表示范式上引入了从单帧静态到多粒度动态的关键转变，为音频驱动的全身动作合成提供了新的技术路径。

## 背景与动机

### 问题背景：音频驱动的全身手势生成

音频驱动的全身手势生成旨在根据语音音频自动合成与语音内容、节奏和情感相协调的全身三维人体动作，包括身体姿态、手势、面部表情以及脚部接触等。这一任务在虚拟人、数字人交互、游戏动画和影视制作等领域具有广泛的应用前景。

全身手势动作天然具有**多时间尺度的动态模式**：一个完整的表达性手势可能持续数百毫秒到数秒，而面部微表情、手指细节动作则可能发生在更短的时间窗口内。Figure 1 直观地展示了这一现象——不同粒度层级下，手势序列呈现出截然不同的运动模式特征。

### 现有方法的瓶颈：单帧Token假设

当前主流方法普遍采用VQ-VAE范式，将连续动作序列量化为离散Token序列，再通过预测这些Token来生成动作。然而，这些方法存在一个根本性的瓶颈：**假设每个动作Token仅表示单帧的静态姿态**（即时间粒度为1）。这一假设导致两个关键问题：

1. **无法建模完整手势模式**：一个自然的手势动作（如挥手、指向）通常跨越多个帧，具有内在的时序结构和持续时间。单帧Token将这种连续的运动模式割裂为孤立的静态姿态，丢失了动作的时序连贯性。
2. **表现力与自然度不足**：由于缺乏对粗粒度动作模式的显式建模，生成的动作往往缺乏宏观的结构性和表现力，容易出现抖动、不连贯或与语音节奏脱节的问题。

### 本文动机：多粒度动作建模

针对上述瓶颈，本文的核心动机是**突破单帧Token的局限，在离散潜空间中同时建模不同时间粒度的动作模式**。具体而言：

- **粒度层次化**：将全身动作在不同时间尺度下编码为多粒度Token序列——粗粒度Token捕捉宏观的手势语义和节奏结构，细粒度Token保留局部的姿态细节和微表情。
- **共享离散空间**：所有粒度的Token共享同一个码本，确保不同尺度动作模式在统一的语义空间中对齐，避免多码本带来的训练不稳定和语义割裂。
- **从粗到细的生成**：在生成阶段，先预测粗粒度的动作Token确定整体手势框架，再逐步细化到更细粒度，使生成的动作兼具结构一致性和细节丰富性。

这一思路直接催生了本文提出的**M3G（Multi-Granular Gesture Generator）**框架，其核心创新——**多粒度VQ-VAE（MGVQ-VAE）**和**多粒度Token预测器**——正是围绕“多粒度动作模式编码与生成”这一因果机制展开的。

## 核心创新

M3G 的核心创新在于**用多粒度离散潜空间替代传统的单帧静态姿态 Token 表示**，使模型能够显式建模具有不同持续时间的完整手势模式，从而突破现有 VQ‑VAE 方法在表现力与时序一致性上的瓶颈。

### 问题诊断：单帧 Token 的粒度缺陷

现有基于 VQ‑VAE 的动作生成方法（如 **CaMN**、**EMAGE**（Liu et al., 2023））将每个动作 Token 仅表示为一帧静态姿态，即时间粒度固定为 `granularity=1`。这种设计隐含地假设所有动作模式都具有相同的时间尺度，但实际上手势包含从快速的手指微动到持续数秒的上肢摆动的多尺度模式。单帧 Token 无法捕获这些跨时间尺度的结构，导致生成的动作缺乏表现力与连贯性。

### 核心机制：多粒度 VQ‑VAE（MGVQ‑VAE）

M3G 通过 MGVQ‑VAE 将全身动作序列在不同时间粒度下编码为共享离散潜空间中的多粒度 Token 序列。具体而言：

- **多尺度编码**：使用 $n$ 个 TCN 网络对输入动作序列 $\mathbf{g}$ 进行编码，每个 TCN 输出的特征序列长度为 $T/2^i$（$i=1,2,...,n$），形成多粒度特征 $\mathbf{F} = [\mathbf{f}_1, ..., \mathbf{f}_n]$（式 2）。粗粒度 Token 捕获大尺度动作模式（如身体摆动），细粒度 Token 保留局部细节（如手指姿态）。

- **共享码本**：所有粒度层次共享同一个码本 $Z$，确保不同时间尺度的嵌入语义一致性，同时减少参数量（式 3）。

- **TransTCN 解码器**：将标准 TCN 解码器替换为 Transpose TCN（TransTCN），对各粒度的量化特征分别解码后求和得到重建动作 $\hat{\mathbf{g}}$（式 5）。此外，卷积输出按核大小缩放（式 6），以稳定多粒度信号的融合。

这一设计使模型能够从粗到细地捕捉动作模式，在压缩离散表示的同时保留跨尺度的运动信息。实验表明，MGVQ‑VAE 的重建误差显著低于 Vanilla VQ‑VAE（Table 4），验证了多粒度表示的有效性。

### 生成端的协同设计：多粒度 Token 预测器

在生成阶段，M3G 的多粒度 Token 预测器与 MGVQ‑VAE 的表示结构深度耦合：

- **身体部位分离潜变量**：将隐层特征投影为面部、上半身、手部和下半身的独立潜变量（式 9‑10），替代传统的全身统一潜变量，使不同部位的运动模式可被独立建模。

- **粗到细迭代预测**：从最粗粒度开始，利用上一级的预测 Token 与当前特征通过交叉注意力逐步预测更细粒度的 Token（式 14），形成层次化的生成过程。

- **音频‑文本融合**：通过逐元素注意力系数 $\alpha$ 动态融合节奏音频特征与文本内容特征（式 8），为多粒度预测提供多模态条件信号。

### 关键组件贡献

消融实验（Table 3）量化了各创新组件的贡献：

- **移除 TransTCN**（回退为标准 TCN 解码器）导致 FGD 从 $4.784\times10^{-1}$ 升至 $6.178\times10^{-1}$，多样性显著下降，表明 TransTCN 对多粒度信号重建至关重要。
- **移除全身潜变量**使 MSE 从 $7.291\times10^{-8}$ 升至 $7.440\times10^{-8}$，验证了其在维持身体运动一致性中的作用。
- **移除 TCN 编码器**（Token 预测器中）损害面部重建质量与运动多样性。
- **移除身体部位分离潜变量**影响整体生成质量，证实部位特定表示的必要性。

粒度数量选择实验（Table 2）进一步表明，随着粒度数量从 1 增至 4，性能持续提升（FGD: $4.784\times10^{-1}$，MSE: $7.291\times10^{-8}$），但继续增加粒度会导致性能下降，揭示出粒度层次与表示容量之间存在最优权衡。

## 整体框架

M3G 采用两阶段训练范式，将音频驱动的全身手势生成分解为动作离散化与条件预测两个子问题。第一阶段训练**多粒度 VQ‑VAE（MGVQ‑VAE）**，学习全身动作的离散多粒度潜在表示；第二阶段训练**多粒度令牌预测器**，从音频与文本特征中预测这些离散令牌。

### 输入与输出定义

系统输入为音频信号 $\mathbf{a} \in \mathbb{R}^{L \cdot sf}$，其中 $L$ 为期望手势帧数，$sf = sr_{audio} / fps_{gestures}$ 为每帧音频采样数。输出为全身 3D 手势序列 $\mathbf{g} \in \mathbb{R}^{L \times (55 \times 6 + 100 + 4 + 3)}$，包含 55 个关节的 Rot6D 旋转表示、100 维面部表情参数、4 个足部接触标签以及 3 维全局平移量。

### 第一阶段：MGVQ‑VAE

MGVQ‑VAE 是标准 VQ‑VAE 的多粒度扩展。给定动作序列 $\mathbf{g}$，编码器 $\mathcal{E}$ 使用 $n$ 个时间卷积网络（TCN）生成 $n$ 组长度递减的特征序列：

$$\mathbf{F} = [\mathbf{f}_1, ..., \mathbf{f}_n] = \mathcal{E}(\mathbf{g}) = [TCN_1(\mathbf{g}), ..., TCN_n(\mathbf{g})]$$

其中第 $i$ 个 TCN 输出的序列长度为 $T_{source} / 2^i$，对应不同时间粒度。所有粒度的特征序列共享同一个码本 $Z$，经量化后得到离散令牌序列 $\hat{\mathbf{F}}$。解码器 $\mathcal{D}$ 使用 Transpose TCN（TransTCN）对各粒度量化特征分别解码，再求和得到重建动作：

$$\hat{\mathbf{g}} = \mathcal{D}(\hat{\mathbf{F}}) = \text{sum}(TransTCN_1(\hat{\mathbf{f}}_1), ..., TransTCN_n(\hat{\mathbf{f}}_n))$$

训练损失包含重建损失、速度损失、加速度损失以及码本承诺损失：

$$\mathcal{L}_{\text{VQ-VAE}} = \mathcal{L}_{rec} + \mathcal{L}_{vel} + \mathcal{L}_{acc} + ||sg[\mathbf{F}] - \hat{\mathbf{F}}||_2^2 + ||\mathbf{F} - sg[\hat{\mathbf{F}}]||_2^2$$

### 第二阶段：多粒度令牌预测器

预测器以音频和文本为条件生成多粒度令牌。音频特征方面，系统提取 onset 和 amplitude 组合为节奏特征 $\mathbf{r} \in \mathbb{R}^{T \times d}$，并与文本内容特征 $\mathbf{c}$ 通过逐元素注意力系数 $\alpha$ 动态融合：

$$\alpha = \text{Softmax}(MLP(\mathbf{r}_{1:T}, \mathbf{c}_{1:T})), \quad \mathbf{f}_{1:T} = \alpha \times \mathbf{r}_{1:T} + (1-\alpha) \times \mathbf{c}_{1:T}$$

融合特征随后被投影为面部、上半身、手部、下半身四个独立的身体部位潜在表示。同时，各部位 TCN 潜在序列求和形成全身多粒度潜在序列 $\mathbf{H}_{full}$，并通过交叉注意力（TCAT）与平均潜在序列交互：

$$\tilde{\mathbf{H}}_{parts} = \mathcal{TCAT}(\mathbf{H}_{mean}^{parts}, \mathbf{H}_{full})$$

令牌预测采用从粗到细的迭代策略：从最粗粒度开始，利用上一级预测令牌与当前特征逐级预测更细粒度的令牌：

$$\hat{\mathbf{q}}_i^{parts} = \text{MLP}(\tilde{\mathbf{h}}_i^{parts} + \hat{\mathbf{q}}_{i+1}^{parts}), \quad i \in [0, n-2]$$

最终，预测的多粒度令牌序列送入已训练好的 MGVQ‑VAE 解码器，生成完整的全身手势动作。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2505_08293/figures/002_Figure_2.jpg]]
*Figure 2: The Overall Workflow of M3G. We illustrate the workflow in two stages: 1. Training MGVQ-VAE to learn discrete latent representations of motions, as known as tokens, for encode and reconstruction. 2. Training Multi-Granular Token Predictor to predict the discrete latent representations from audio*

## 核心模块与公式推导

M3G 采用两阶段训练范式：第一阶段训练**多粒度 VQ-VAE（MGVQ-VAE）**，学习全身动作的离散多粒度潜在表示；第二阶段训练**多粒度令牌预测器**，从音频和文本特征中预测这些离散令牌。

### 3.1 动作表示与问题定义

给定一段音频输入 $\mathbf{a} \in \mathbb{R}^{L \cdot sf}$，其中 $sf = sr_{audio} / fps_{gestures}$ 表示每帧对应的音频采样点数，目标是生成对应的全身 3D 手势序列：

$$\mathbf{g} \in \mathbb{R}^{L \times (55 \times 6 + 100 + 4 + 3)}$$

该向量包含：55 个关节的 6D 连续旋转表示（Rot6D）、100 维面部表情参数、4 个脚部接触标签、3 个全局平移参数。

### 3.2 多粒度 VQ-VAE（MGVQ-VAE）

MGVQ-VAE 的核心创新在于将动作序列在不同时间粒度下编码为共享离散潜空间中的多粒度令牌序列。标准 VQ-VAE 流程为：

$$\mathbf{f} = \mathcal{E}(\mathbf{g}), \quad \mathbf{q} = \mathcal{Q}(\mathbf{f}), \quad \hat{\mathbf{f}} = \text{lookup}(Z, \mathbf{q}), \quad \hat{\mathbf{g}} = \mathcal{D}(\hat{\mathbf{f}})$$

MGVQ-VAE 将其扩展为多粒度形式。编码器使用 $n$ 个 TCN 网络，分别对应 $n$ 个粒度层级，生成不同长度的嵌入序列：

$$\mathbf{F} = [\mathbf{f}_1, ..., \mathbf{f}_n] = \mathcal{E}(\mathbf{g}) = [TCN_1(\mathbf{g}), ..., TCN_n(\mathbf{g})]$$

其中第 $i$ 个 TCN 输出的序列长度为 $T_{source} / 2^i$，通过步长卷积实现时间下采样。所有粒度的嵌入序列**共享同一个码本 $Z$**，以保证嵌入语义的一致性。

解码阶段，对各粒度的量化特征使用 **Transpose TCN（TransTCN）** 进行上采样解码，然后求和得到重建动作：

$$\hat{\mathbf{g}} = \mathcal{D}(\hat{\mathbf{F}}) = \text{sum}(TransTCN_1(\hat{\mathbf{f}}_1), ..., TransTCN_n(\hat{\mathbf{f}}_n))$$

TransTCN 的关键改进在于对卷积输出进行**核大小归一化**，即除以卷积核尺寸，避免上采样过程中的幅度累积偏差。

MGVQ-VAE 的总训练损失为：

$$\mathcal{L}_{\text{VQ-VAE}} = \mathcal{L}_{rec} + \mathcal{L}_{vel} + \mathcal{L}_{acc} + ||sg[\mathbf{F}] - \hat{\mathbf{F}}||_2^2 + ||\mathbf{F} - sg[\hat{\mathbf{F}}]||_2^2$$

其中 $\mathcal{L}_{rec}$、$\mathcal{L}_{vel}$、$\mathcal{L}_{acc}$ 分别为重建损失、速度损失和加速度损失，后两项为码本承诺损失（$sg[\cdot]$ 表示停止梯度算子）。

### 3.3 多粒度令牌预测器

第二阶段训练一个预测器，从音频和文本特征中预测 MGVQ-VAE 产生的多粒度离散令牌。

**音频-文本融合**：首先将节拍起始点 $o$ 和幅度 $a$ 组合为节奏音频特征 $\mathbf{r}_{1:T}$，与文本内容特征 $\mathbf{c}_{1:T}$ 通过逐元素注意力系数 $\alpha$ 动态融合：

$$\alpha = \text{Softmax}(MLP(\mathbf{r}_{1:T}, \mathbf{c}_{1:T})), \quad \mathbf{f}_{1:T} = \alpha \times \mathbf{r}_{1:T} + (1-\alpha) \times \mathbf{c}_{1:T}$$

**身体部位潜在表示**：融合特征通过 TCN 编码器后，分别投影为面部、上半身、手部和下半身的独立潜在表示 $\mathbf{h}^{parts}$。同时，将所有身体部位的 TCN 潜在序列求和，形成全身多粒度潜在序列：

$$\mathbf{H}_{full} = \mathbf{H}_{tcn}^{upper} + \mathbf{H}_{tcn}^{hands} + \mathbf{H}_{tcn}^{lower}$$

通过均值池化后的部位潜在序列与全身潜在序列进行交叉注意力（TCAT），增强部位间的一致性：

$$\tilde{\mathbf{H}}_{parts} = \mathcal{TCAT}(\mathbf{H}_{mean}^{parts}, \mathbf{H}_{full})$$

**从粗到细的令牌预测**：从最粗粒度开始，利用上一级的预测令牌和当前特征，迭代预测各粒度令牌：

$$\hat{\mathbf{q}}_i^{parts} = \text{MLP}(\tilde{\mathbf{h}}_i^{parts} + \hat{\mathbf{q}}_{i+1}^{parts}), \quad i \in [0, n-2]$$

这种从粗到细的预测策略使模型能够先捕捉整体动作趋势，再逐步细化局部细节。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2505_08293/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of gesture sequences with expressive motion patterns in different granularities*

## 实验与分析

### 整体性能对比

M3G在BEAT数据集上与现有主流方法进行了全面对比，结果如Table 1所示。在FGD（Fréchet Gesture Distance）指标上，M3G达到**4.784e-1**，显著优于CaMN和EMAGE等现有方法；在MSE指标上达到**7.291e-8**，同样取得最优结果。在衡量唇音同步质量的LVD（Lips-Voice Distance）指标上，M3G达到**7.439e-8**，进一步验证了其在面部动作生成上的精确性。

从因果机制看，这些提升源于多粒度离散潜空间对动作模式的有效压缩——粗粒度Token捕捉整体姿态趋势，细粒度Token保留局部表现力细节，两者协同使生成器能同时优化全局一致性与局部精度。

### 粒度数量选择

Table 2展示了不同粒度数量对性能的影响。实验表明，将粒度数量从1逐步增加到4时，FGD持续下降（从单粒度的较高值降至**4.784e-1**），MSE也同步改善至**7.291e-8**。然而，当粒度数量超过4后，性能出现退化。

这一现象揭示了多粒度建模的非单调特性：过少的粒度无法充分捕捉动作模式的多尺度结构，而过多的粒度则引入冗余信息，增加了码本学习的难度。4粒度配置（对应时间尺度$T/2, T/4, T/8, T/16$）在当前任务上达到了最优的表示能力与学习难度的平衡。

### 关键组件消融

Table 3系统消融了M3G各核心组件的贡献：

**TransTCN解码器**：将TransTCN替换为标准TCN解码器后，FGD从**4.784e-1**显著上升至**6.178e-1**，同时Diversity指标下降。这证实了TransTCN通过转置卷积上采样操作，能更有效地将多粒度潜变量映射回原始时间分辨率，标准TCN的下采样特性在此任务中存在信息瓶颈。

**全身Latent**：移除全身Latent后，MSE从**7.291e-8**上升至**7.440e-8**，表明跨身体部位的全局潜变量对维持动作一致性具有正向作用。该组件通过汇总上半身、手部和下半身的TCN潜变量序列，为各部位提供了全局上下文约束。

**独立身体部位Latent**：将面部、上半身、手部、下半身的独立潜变量替换为统一潜变量后，整体生成质量下降。这验证了不同身体部位具有差异化的运动模式——例如手部动作的精细度远高于下肢，独立潜空间使各部位能学习到适配自身特性的离散表示。

**TCN编码器**：在Token预测器中移除TCN编码器后，面部重建质量和动作多样性均出现退化。TCN编码器通过时序卷积捕捉音频-文本融合特征的局部依赖关系，为后续的跨注意力粗到细预测提供了时序结构化的隐变量。

### 重建质量验证

Table 4对比了MGVQ-VAE与Vanilla VQ-VAE的重建误差。在面部JRMSE指标上，MGVQ-VAE达到**1.368 ± 0.022（×10⁻³）**，显著低于Vanilla VQ-VAE，证实多粒度离散表示能更完整地保留原始动作中的表现力信息。卷积输出除以卷积核大小的缩放策略（Eq.6）也对重建稳定性有贡献。

### 主观评价

Figure 3展示了18名参与者在40个随机片段上的A/B测试结果。参与者一致倾向于M3G生成的动作，认为其比CaMN和EMAGE更自然。这从感知层面验证了多粒度建模带来的表现力提升——人类观察者对动作自然度的判断高度依赖于多尺度时序模式的协调性。

### 需要人工验证的问题

1. **Table 1的具体数值**：本文仅提供了FGD和MSE的精确数值，其余指标（如BA、Diversity）的具体对比值需查阅原文确认。
2. **跨数据集泛化**：当前实验仅基于BEAT数据集，该方法在其他数据集（如TED Gesture、Trinity）上的表现需要额外验证。
3. **失败模式**：原文未系统报告失败案例，但从粒度消融可以推断，在动作模式极为单一或极度复杂的场景下，固定的4粒度配置可能不是最优选择。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2505_08293/figures/004_Table_1.jpg]]
*Table 1: Overall Comparison of various methods. The best performance of each metric is in boldface fonts. The sign ↑ beside the metric denotes that the larger the value, the better it is, while the sign ↓ is the reverse*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2505_08293/figures/003_Table_2.jpg]]
*Table 2: Experiments for Granularity Selection*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2505_08293/figures/006_Table_3.jpg]]
*Table 3: Ablation Experiments for Proposed Components*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2505_08293/figures/008_Table_4.jpg]]
*Table 4: Experiments for Reconstruction Errors*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2505_08293/figures/005_Figure_3.jpg]]
*Figure 3: Perceptual study results on motion generation*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2505_08293/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative results*

## 方法谱系与知识库定位

### 核心瓶颈与因果机制

现有基于VQ‑VAE的音频驱动手势生成方法存在一个关键假设：每个动作Token仅表示单帧静态姿态（即时间粒度固定为1）。这一假设导致模型无法捕捉具有不同持续时间的完整手势模式——例如，一次挥手的宏观节奏与手指的微观颤动属于不同的时间尺度，却被迫用同一粒度编码。**M3G** 的因果调节变量是“多粒度离散潜空间”：通过共享码本配合多尺度时间卷积网络（TCN/TransTCN），将全身动作在不同时间粒度下编码为共享离散潜空间中的多粒度Token序列，使模型能够从粗到细地建模动作模式。这一机制直接回应了单粒度表示在表现力和时序一致性上的瓶颈。

### 方法谱系定位

在音频驱动全身手势生成的方法谱系中，M3G 相对于主要基线方法进行了以下关键槽位替换：

| 方法槽位 | 基线方案 | M3G 方案 | 证据锚点 |
|---------|---------|---------|---------|
| 动作Token时间粒度 | 单帧Token（粒度=1），如 **EMAGE** (Liu et al., 2023) | 多粒度Token，长度 $T/2^i$（$i=1..n$） | Section 3.3, Eq.2 |
| VQ‑VAE解码器 | 标准TCN解码器 | Transpose TCN（TransTCN）+ 多粒度重建求和 | Section 3.3, Eq.5 |
| 码本策略 | 分离或单一码本 | 所有粒度共享同一码本 $\mathbf{Z}$ | Section 3.3, Eq.3 |
| Token预测器架构 | 单尺度Token预测 | 多粒度预测器（均值池化 + TCN编码器 + 粗到细迭代预测） | Section 3.4, Eq.11‑14 |
| 身体部位表示 | 全身统一Latent | 面部、上半身、双手、下半身独立Latent | Section 3.4, Eq.9‑10 |
| 卷积输出缩放 | 无归一化 | 卷积输出除以卷积核大小 | Section 3.3, Eq.6 |

M3G 的两阶段流水线——先训练 **MGVQ‑VAE** 学习离散多粒度潜表示，再训练 **多粒度Token预测器** 从音频‑文本融合特征中预测多粒度Token——在架构层面与现有工作的本质区别在于：它不是在一个固定尺度上优化生成，而是构建了一个从粗粒度（宏观动作模式）到细粒度（局部细节）的层次化预测通路。

### 适用边界与局限

**适用边界**：
- 输入依赖：需要音频（节奏特征 onset + amplitude）和文本（内容特征）双模态输入，适用于有语音内容的手势生成场景。
- 身体表示：采用55个关节的Rot6D旋转表示 + 100维面部表情 + 4个足部接触标签 + 3个全局平移参数，覆盖全身手势。
- 数据集：当前验证基于 **BEAT** 数据集的标准训练/测试划分。

**已知局限**：
- 论文未明确报告该方法在极端情感表达、不同语言或说话风格下的泛化性能。
- 粒度层次数量（最优为4）需通过实验确定，缺乏自适应选择机制。
- 多粒度Token对段落级长时序依赖的建模能力尚未验证。

### 开放问题

1. **自适应粒度选择**：如何根据输入音频的节奏复杂度和语义内容，自适应地选择最优的粒度层次和每个层次的时间尺度？
2. **长时序一致性**：多粒度Token能否有效建模段落级甚至篇章级的时序依赖，从而保证长时间手势序列的风格一致性？
3. **跨域泛化**：该方法在不同语言、情感强度和说话风格条件下的泛化性能如何？是否需要域适应策略？
4. **与生成式大模型的结合**：能否将多粒度离散表示与扩散模型或大型语言模型结合，利用后者的强先验进一步提升手势生成的自然度和可控性？

## 原文 PDF

![[paperPDFs/arxiv_2025/M3G_Multi-Granular_Gesture_Generator_for_Audio-Driven_Full-Body_Human_Motion_Synthesis.pdf]]