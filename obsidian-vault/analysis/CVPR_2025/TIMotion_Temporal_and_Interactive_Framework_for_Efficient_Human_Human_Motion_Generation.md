---
title: "TIMotion: Temporal and Interactive Framework for Efficient Human-Human Motion Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Motion_Generation.pdf
aliases:
- TIMotion
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过因果交互注入（Causal Interactive Injection）将两个单人运动序列显式建模为因果交互序列，利用运动的时间因果特性；配合角色演变扫描（Role-Evolving Scanning）适应主被动角色动态变化，以及局部模式放大（Localized Pattern Amplification）捕捉短时运动模式，从而精准调控生成质量。
primary_logic: 双人交互运动具有内在的时序因果性，通过交错排列两人运动帧可以实现统一序列中的因果建模，简化交互混合模块设计并提升生成效果。
claims:
- 在InterHuman数据集上，TIMotion+RWKV的FID达到4.702，显著低于InterGen的5.918。
- 在InterHuman数据集上，TIMotion+RWKV的R Precision Top1达到0.501，高于InterGen的0.371。
- 消融实验显示，同时应用Causal Interactive Injection、Role-Evolving Scanning和Localized Pattern Amplification三个组件后，FID从5.943降至4.702。
- 在不同的交互混合结构（Transformer、Mamba、RWKV）上，因果交互建模均优于单人类扩展和分离建模方式。
---

# TIMotion: Temporal and Interactive Framework for Efficient Human-Human Motion Generation

> [!tip] 核心洞察
> 双人交互运动具有内在的时序因果性，通过交错排列两人运动帧可以实现统一序列中的因果建模，简化交互混合模块设计并提升生成效果。

| 字段 | 内容 |
|------|------|
| 中文题名 | TIMotion：面向高效双人运动生成的时序与交互框架 |
| 英文题名 | TIMotion: Temporal and Interactive Framework for Efficient Human-Human Motion Generation |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://aigc-explorer.github.io/TIMotion-page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | TIMotion |
| Dataset | InterHuman, InterX |

> [!tip] 效果简介
> - InterHuman 上，FID 4.702 (TIMotion+RWKV) vs 5.918 (InterGen) (-1.216)；R Precision Top1 0.501 (TIMotion+RWKV) vs 0.371 (InterGen) (+0.130)。
> - InterX 上，FID 0.261 (TIMotion+RWKV) vs 0.475 (InterGen*) (-0.214)；R Precision Top1 0.414 (TIMotion+Mamba) vs 0.400 (InterGen*) (+0.014)。

## 概述

**问题瓶颈**：现有的双人运动生成方法（如 InterGen, Liang et al., IJCV 2024）在交互混合（Interaction Mixing）阶段主要依赖自注意力和交叉注意力机制，侧重空间交互建模而忽视运动序列内在的**时序因果特性**。这一设计导致参数冗余、长序列生成质量下降，尤其在角色动态变化的复杂交互场景中表现不佳。

**核心洞察**：双人交互运动天然具备时序因果性——一方的当前动作由双方的历史动作共同决定。基于此，TIMotion 提出将两个单人运动序列**交错排列为统一的因果交互序列**，使得交互混合模块可以在保持因果约束的前提下同时完成时序建模与交互融合，从而简化设计并提升生成质量。

**方法定位**：TIMotion 是一个**时序与交互融合的双人运动生成框架**，包含三个关键技术组件：
- **Causal Interactive Injection (CII)**：将两个单人序列按帧交错为因果交互序列，显式引入时序因果性。
- **Role-Evolving Scanning (RES)**：通过对称因果序列处理交互中主被动角色的动态切换。
- **Localized Pattern Amplification (LPA)**：利用 1D 卷积和自适应层归一化捕捉每个人的短时运动模式，抑制高频噪声。

该框架可适配多种交互混合架构（Transformer、Mamba、RWKV），在参数效率和生成质量上均具优势。

**主要结果**：
- 在 InterHuman 数据集上，TIMotion+RWKV 的 **FID 达到 4.702**，显著优于 InterGen 的 5.918（Table 1）；**R Precision Top1 达到 0.501**，对比 InterGen 的 0.371 提升明显。
- 在 InterX 数据集上，TIMotion+RWKV 的 **FID 为 0.261**，同样优于 InterGen* 的 0.475（Table 7），验证了方法的泛化能力。
- 消融实验证实三个组件均有正向贡献：同时应用 CII、RES 和 LPA 后，FID 从 5.943 降至 4.702（Table 3）；LPA 将运动特征的高频分量平均比例从 0.9063 降至 0.3729（Figure 6），生成运动更加平滑自然。

## 背景与动机

双人运动生成（human-human motion generation）旨在根据文本描述或部分运动序列，合成两个交互角色的自然运动。这一任务在虚拟现实、游戏角色动画、人机交互等领域具有重要应用价值。然而，与单人运动生成相比，双人运动生成面临独特的挑战：它不仅需要刻画每个个体的运动质量，还必须精准建模两人之间的时空交互关系。

现有方法大多将双人运动生成视为一个交互混合（interaction mixing）问题，即通过注意力机制或图神经网络直接混合两个单人运动序列的特征。这类方法的核心瓶颈在于**侧重交互混合而忽视时序建模**。具体而言，它们通常将运动序列视为无时序先验的通用特征，依赖自注意力和交叉注意力（self/cross-attention）来捕获交互模式，但缺乏对运动时序因果性的显式利用。这导致两个突出问题：**生成质量欠佳**，尤其在长序列和复杂交互场景下，运动往往出现抖动、不协调甚至语义偏离；**参数冗余**，基于Transformer的交互混合模块参数量大，推理效率受限。

从更宏观的视角看，双人交互运动具有内在的**时序因果性**（temporal causality）：一方的动作往往是另一方动作的原因或结果，且这种因果关系随时间动态演变。例如，在一个推搡场景中，先出手的人是主动角色，随后被推者可能转为主动反击——角色关系并非静态，而是**角色演变**（role-evolving）的过程。此外，人体运动天然包含丰富的**局部短时模式**（localized short-term patterns），如步伐节奏、手势变化等，这些高频细节对运动平滑性至关重要，但现有方法缺乏针对性的建模手段。

本文提出**TIMotion（Temporal and Interactive Framework for Efficient Human-Human Motion Generation）**，一个面向高效双人运动生成的时序与交互框架。TIMotion的核心动机是通过三个关键设计弥补上述缺口：

1. **因果交互注入（Causal Interactive Injection, CII）**：将两个单人运动序列显式建模为统一的因果交互序列，利用运动的时间因果特性简化交互混合模块的设计，同时提升生成质量。
2. **角色演变扫描（Role-Evolving Scanning, RES）**：通过对称因果序列处理交互角色的动态切换，使模型能够适应主被动角色的实时变化。
3. **局部模式放大（Localized Pattern Amplification, LPA）**：利用1D卷积和自适应层归一化（AdaLN）捕捉每个人的短时运动模式，降低高频噪声，生成更平滑的运动。

TIMotion的设计遵循一个统一的抽象框架——**MetaMotion**，将双人运动生成过程解耦为时序建模和交互混合两个阶段。该框架不仅兼容多种交互混合架构（如Transformer、Mamba、RWKV），还显著降低了参数量和推理时间，展现出良好的通用性与效率。

## 核心创新

TIMotion 的核心创新在于将双人运动生成问题从“交互混合”主导的范式，重新定义为**时序因果建模**驱动的范式。其关键洞察是：双人交互运动具有内在的时序因果性——一个人的当前动作依赖于对方先前的动作。基于此，TIMotion 提出了一套系统性的创新方案，在三个关键维度上突破了现有方法的局限。

### 1. 因果交互注入（Causal Interactive Injection, CII）

**改变的槽位：交互混合机制（Interaction Mixing Mechanism）**

现有方法（如 InterGen，Liang et al., IJCV 2024）采用 Self-attention 和 Cross-attention 分别建模单人时序和双人交互，将时序建模与交互混合割裂为两个独立阶段。这种分离设计忽视了双人运动中“动作-反应”的因果链条，导致交互建模不够深入，且参数冗余。

TIMotion 提出 Causal Interactive Injection，将两个独立的单人运动序列交错排列为一个统一的因果交互序列。具体而言，设两个单人序列分别为 $x_a$ 和 $x_b$，CII 按位置索引奇偶性将它们交错：

$$k = \left\{ a, \quad j \% 2 = 1 \right.$$

形成的因果交互序列 $x_{cii}$ 中，奇数位置来自人物 A，偶数位置来自人物 B。这种交错排列使得后续的交互混合模块（如 Transformer、Mamba、RWKV）能够在一个统一序列中同时完成时序建模和交互建模——当前帧的生成自然地依赖于序列中所有先前的帧，无论它们属于哪个人物。这从根本上简化了交互混合模块的设计，并赋予了模型显式的时序因果归纳偏置。

**证据强度**：Table 2 显示，在 Transformer、Mamba、RWKV 三种不同的交互混合架构上，CII 均显著优于“单人类扩展”和“分离建模”两种时序建模方式。以 RWKV 为例，CII 将 FID 从 9.181 降至 5.943（置信度 0.90）。

### 2. 角色演变扫描（Role-Evolving Scanning, RES）

**改变的槽位：角色建模（Role Modeling）**

现有方法通常采用静态角色分配或不进行显式角色建模，无法适应交互过程中主被动角色的动态切换。如 Figure 3 所示，在一次推搡交互中，人物 A 最初是主动方（推人），随后人物 B 变为主动方（反击），最终人物 A 被推倒——角色在交互过程中不断演变。

TIMotion 提出 Role-Evolving Scanning，通过构建对称因果交互序列来捕获这种角色动态。在获得因果交互序列 $x_{cii}$ 后，交换人物 A 和 B 的身份，生成对称因果序列 $x_{sym.cii}$，然后将两者在通道维度拼接：

$$X = \mathrm{Concat}(x_{cii}, x_{sym.cii})$$

这一设计使得交互混合模块能够同时处理两种角色视角，无论哪个人物在当前时刻是主动方还是被动方，模型都能从拼接特征中捕获相应的交互模式。

**证据强度**：Table 3 的消融实验显示，在 CII 基础上添加 RES 后，R-Precision 和 FID 均获得进一步提升（置信度 0.95）。

### 3. 局部模式放大（Localized Pattern Amplification, LPA）

**改变的槽位：局部运动模式处理（Local Motion Pattern Handling）**

现有方法缺乏专门的局部运动模式建模机制，导致生成的运动序列可能存在不自然的抖动或高频噪声。TIMotion 提出 Localized Pattern Amplification，通过两层 1D 卷积和自适应层归一化（AdaLN）配合残差连接，专门捕获每个人的短时运动模式：

$$\begin{array}{rl} & x_a^l = \mathrm{Conv}_3(\mathrm{AdaLN}(x_a, e)), \\ & y_a = \mathrm{Conv}_1(\mathrm{AdaLN}(x_a^l, e)), \\ & y_a^l = x_a + y_a, \end{array}$$

LPA 对每个单人序列独立操作：首先通过核大小为 3 的卷积捕获局部上下文，再通过核大小为 1 的卷积进行特征变换，最后通过残差连接保留原始信息。AdaLN 利用文本条件 $e$ 自适应地调节特征分布。

**证据强度**：Table 3 显示，在 CII+RES 基础上添加 LPA 后，FID 从 5.943 进一步降至 4.702，R Precision Top1 达到 0.501。Table 4 的消融实验证实 AdaLN 和 k=3,1 的卷积核配置为最优。Figure 6 的频谱分析进一步揭示了 LPA 的作用机制：它将运动特征的高频分量平均比例从 0.9063 降至 0.3729，生成的运动更加平滑自然。

### 创新总结

TIMotion 的三个创新组件形成了完整的解决方案链条：**CII** 从序列结构层面将双人运动建模为因果序列，**RES** 从角色语义层面适应交互中的主被动切换，**LPA** 从运动细节层面消除高频噪声、增强局部平滑性。三者协同作用，使得 TIMotion 在 InterHuman 数据集上取得了 FID 4.702 的最优性能，显著优于 InterGen 的 5.918（Table 1，置信度 0.98）。更重要的是，CII 的核心思想具有架构无关性，可适配 Transformer、Mamba、RWKV 等多种交互混合模块，展现出良好的通用性。

## 整体框架

TIMotion 的整体框架建立在作者提出的 **MetaMotion** 抽象之上，将双人运动生成过程解耦为两个核心阶段：**时序建模（Temporal Modeling）** 与 **交互混合（Interaction Mixing）**。基于这一抽象，TIMotion 设计了三个紧密协作的技术模块，形成一条从文本条件到双人运动序列的完整生成流水线。

### 输入与条件编码

生成过程的输入由两部分组成：一段描述双人交互的文本提示，以及从标准高斯分布采样的随机噪声。文本条件通过一个**冻结的 CLIP 文本编码器**（Frozen CLIP Text Encoder）提取为语义特征嵌入，作为后续所有模块的条件信号。噪声则被塑造为两个单人运动序列的初始表示，每个序列包含 $L$ 帧运动状态，每帧状态定义为关节位置、速度、6D 旋转和足部接触标签的拼接。

### 核心流水线：从噪声到双人运动

TIMotion 的生成流水线由以下模块级联构成，各模块之间的关系如 Figure 2 所示：

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/002_Figure_2.jpg]]
*Figure 2: The overall framework of our TIMotion. We contribute three primary technical designs. First, we propose Causal Interactive Injection to utilize the temporal properties of motion sequences. Then we present Role-Evolving Mixing to adjust to the ever-evolving roles during interaction. Finally, we design Localized Pattern Amplification to capture short-term motion patterns*

1. **Causal Interactive Injection (CII)**：将两个独立的单人运动序列按奇偶位置交错排列，形成一条统一的因果交互序列。具体而言，若两人分别为 $a$ 和 $b$，则因果序列的第 $j$ 帧来自 $a$（当 $j$ 为奇数）或 $b$（当 $j$ 为偶数）。这一交错操作将双人运动的时空关系转化为单一序列内的时序依赖，使得后续的交互混合模块能够自然地利用运动的因果特性，而无需显式的交叉注意力机制。

2. **Role-Evolving Scanning (RES)**：考虑到交互过程中主被动角色会动态切换（如 Figure 3 所示的推搡场景），RES 在 CII 的基础上构造一条**对称因果交互序列**——交换 $a$ 和 $b$ 的角色分配后重新执行交错操作。原始因果序列与对称因果序列在通道维度上拼接，形成最终的混合输入 $X = \mathrm{Concat}(x_{cii}, x_{sym.cii})$。这一设计使模型能够同时感知两种角色分配下的时序模式，从而适应交互中角色的演变。

3. **Localized Pattern Amplification (LPA)**：在交互混合之前，LPA 对每个人的运动特征分别进行局部增强。该模块由两层 1D 卷积、自适应层归一化（AdaLN）和残差连接组成：第一层卷积（核大小为 3）捕获短时运动模式，第二层卷积（核大小为 1）进行通道映射，残差连接保留原始信息。LPA 的作用是放大单人运动中的局部细节模式，实验证明它能显著降低运动特征中的高频分量（平均振幅比例从 0.9063 降至 0.3729），使生成的运动更加平滑自然。

4. **Interaction Mixing Module**：经过 CII、RES 和 LPA 处理后的特征序列进入交互混合模块。TIMotion 的设计与具体混合架构解耦——论文验证了 **Transformer**、**Mamba** 和 **RWKV** 三种结构均可作为该模块的骨干。交互混合模块对因果交互序列进行特征融合，捕捉两人运动之间的协调关系。

5. **Motion Decoder**：交互混合后的特征通过最终的线性投影层映射回运动参数空间，预测去噪后的双人运动序列。

### 训练与损失函数

TIMotion 采用扩散模型的训练范式，以预测噪声与真实噪声之间的均方误差作为基础损失：

$$\mathcal{L}_t = \mathbb{E}_{\mathbf{x}_0, \epsilon} \left[ \left\| \epsilon - \epsilon_\theta \left( \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, t \right) \right\|^2 \right]$$

在此基础上，总运动损失集成了多项几何正则化项：

$$\mathcal{L}_{motion} = \mathcal{L}_{simple} + \lambda_{vel}\mathcal{L}_{vel} + \lambda_{foot}\mathcal{L}_{foot} + \lambda_{BL}\mathcal{L}_{BL} + \lambda_{DM}\mathcal{L}_{DM} + \lambda_{RO}\mathcal{L}_{RO}$$

包括速度损失、足部接触损失、骨骼长度损失、掩码关节距离图损失和相对朝向损失。所有损失权重与 InterGen（Liang et al., IJCV 2024）保持一致，确保对比的公平性。

### 设计理念总结

TIMotion 的核心设计哲学在于：**将双人交互运动的内在时序因果性显式地注入模型结构**。通过 CII 将两个序列交错为统一因果序列，TIMotion 避免了传统方法中复杂的交叉注意力设计，大幅降低了交互混合模块的参数量。RES 和 LPA 则分别解决了角色动态演变和局部运动模式捕捉的挑战。这种模块化设计使 TIMotion 能够灵活适配不同的交互混合架构，在保持高效性的同时取得领先的生成质量。

### 补充图表

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/001_Figure_1.jpg]]
*Figure 1: MetaMotion and performance of MetaMotion-based models on InterHuman validation set. We abstract the MetaMotion concept that illustrates the intrinsic properties of human-human motion generation in the interaction process. (a) and (b) show the two types of methods currently, and (c) shows our method TIMotion, LPA refers to the Localized Pattern Amplification. In (d) we compare the performance of the different methods on the InterHuman dataset*

## 核心模块与公式推导

TIMotion 的核心技术架构建立在作者提出的 **MetaMotion** 抽象框架之上，该框架将双人运动生成过程拆解为两个阶段：时序建模（Temporal Modeling）与交互混合（Interaction Mixing）。基于这一抽象，TIMotion 引入了三个关键模块，分别针对现有方法的瓶颈进行设计。

### 3.1 因果交互注入（Causal Interactive Injection, CII）

现有方法（如 InterGen）通常将两个单人的运动序列分别进行时序建模，再通过交叉注意力（Cross-Attention）等方式进行交互混合。这种分离式建模忽略了双人运动内在的时序因果性——一个人的动作往往是另一个人动作的因或果。

CII 模块的核心思想是将两个单人运动序列交错排列，构建一个统一的**因果交互序列**。设两个单人的运动序列分别为 $x_a = \{x_a^1, x_a^2, \dots, x_a^L\}$ 和 $x_b = \{x_b^1, x_b^2, \dots, x_b^L\}$，CII 通过以下索引规则生成因果交互序列 $x_{cii}$：

$$k = \begin{cases} a, & j \bmod 2 = 1 \\ b, & j \bmod 2 = 0 \end{cases}$$

$$x_{cii} = \{x_k^{\lfloor j/2 \rfloor}\}_{j=1}^{2L}$$

其中 $j$ 为因果序列中的位置索引。奇数位置填充人物 $a$ 的帧，偶数位置填充人物 $b$ 的帧。这种交错排列使得交互混合模块（如 RWKV、Mamba 等）能够自然地利用序列的因果特性进行建模，无需额外的交叉注意力机制。

### 3.2 角色演变扫描（Role-Evolving Scanning, RES）

在真实交互中，主动方与被动方的角色并非固定不变。例如，在推搡场景中，先推人者是主动方，随后被推者反击时角色发生互换（参见 Figure 3）。CII 生成的因果序列隐式地假定了固定的角色顺序（$a$ 先于 $b$），无法适应这种动态变化。

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of changing active and passive roles. The first person acts as the active role in the early stages, and as time progresses, the other person becomes the active role of the motion*

RES 模块通过构造**对称因果交互序列**来解决这一问题。具体而言，在生成 $x_{cii}$ 的基础上，交换 $a$ 和 $b$ 的角色，生成对称序列 $x_{sym.cii}$：

$$x_{sym.cii} = \{x_{k'}^{\lfloor j/2 \rfloor}\}_{j=1}^{2L}, \quad k' = \begin{cases} b, & j \bmod 2 = 1 \\ a, & j \bmod 2 = 0 \end{cases}$$

最终，将两个序列在通道维度拼接：

$$X = \text{Concat}(x_{cii}, x_{sym.cii})$$

这样，交互混合模块可以同时感知两个方向的因果依赖关系，从而适应交互过程中角色的动态演变。

### 3.3 局部模式放大（Localized Pattern Amplification, LPA）

双人交互中的许多动作模式具有短时特性，如挥手、点头、快速躲避等。这些局部模式容易被长序列建模所平滑或忽略。LPA 模块专门用于捕捉和增强每个人的短时运动模式。

LPA 的设计采用两层 1D 卷积配合自适应层归一化（AdaLN）和残差连接。对于单人特征 $x_a$ 和文本条件嵌入 $e$，其计算过程为：

$$\begin{aligned}
x_a^l &= \text{Conv}_3(\text{AdaLN}(x_a, e)) \\
y_a &= \text{Conv}_1(\text{AdaLN}(x_a^l, e)) \\
y_a^l &= x_a + y_a
\end{aligned}$$

其中 $\text{Conv}_3$ 和 $\text{Conv}_1$ 分别表示卷积核大小为 3 和 1 的 1D 卷积。第一层卷积（核大小 3）负责捕获局部时序上下文，第二层卷积（核大小 1）进行通道混合。残差连接 $x_a + y_a$ 确保局部增强不会破坏原有的全局特征。AdaLN 使归一化参数以文本条件为条件，增强文本-运动的一致性。

### 3.4 交互混合模块

因果交互序列 $X$ 经过 LPA 的局部增强后，送入可替换的**交互混合模块**（Interaction Mixing Module）进行特征融合：

$$Y = \text{InteractionMixing}(X)$$

TIMotion 的一个关键优势在于其对交互混合架构的普适性。论文验证了三种主流架构：**Transformer**（自注意力）、**Mamba**（状态空间模型）和 **RWKV**（线性注意力），均能有效适配 CII + RES 的因果序列输入。消融实验（Table 2）表明，在三种架构上，因果交互建模均优于单人类扩展和分离建模方式。

### 3.5 训练目标

TIMotion 沿用扩散模型的噪声预测范式。给定干净运动 $\mathbf{x}_0$ 和噪声 $\epsilon$，加噪后的运动为 $\sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\epsilon$，去噪网络 $\epsilon_\theta$ 的优化目标为：

$$\mathcal{L}_t = \mathbb{E}_{\mathbf{x}_0, \epsilon} \left[ \left\| \epsilon - \epsilon_\theta \left( \sqrt{\bar{\alpha}_t} \mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, t \right) \right\|^2 \right]$$

在此基础上，总运动损失函数结合了多种几何正则化项：

$$\mathcal{L}_{motion} = \mathcal{L}_{simple} + \lambda_{vel}\mathcal{L}_{vel} + \lambda_{foot}\mathcal{L}_{foot} + \lambda_{BL}\mathcal{L}_{BL} + \lambda_{DM}\mathcal{L}_{DM} + \lambda_{RO}\mathcal{L}_{RO}$$

各正则化项分别为速度损失、脚部接触损失、骨骼长度损失、关节距离映射损失和相对朝向损失。所有超参数 $\lambda$ 与 InterGen 保持一致，确保公平比较。

## 实验与分析

### 核心瓶颈与实验设计逻辑

现有双人运动生成方法（如 **InterGen**，Liang et al., IJCV 2024）侧重交互混合而忽视时序建模，导致运动生成质量欠佳、参数冗余，尤其在长序列和复杂交互中表现不佳。TIMotion 的实验设计围绕三个因果调控旋钮展开：**Causal Interactive Injection (CII)** 将两个单人运动序列显式建模为因果交互序列；**Role-Evolving Scanning (RES)** 适应主被动角色的动态变化；**Localized Pattern Amplification (LPA)** 捕捉短时运动模式。实验旨在验证：(1) 因果交互建模在不同交互混合架构上的普适优势；(2) 各组件的独立贡献；(3) 生成运动的平滑性与计算效率。

所有对比方法使用相同的损失函数和超参数设置（与 InterGen 一致），在 8×NVIDIA L40S 硬件下训练，使用公开的 InterHuman 和 InterX 数据集，评估协议遵循 InterGen 标准，所有实验重复 20 次并报告 95% 置信区间。

### 主实验结果

**InterHuman 数据集**（Table 1）：TIMotion+RWKV 在所有关键指标上取得最优或次优结果。FID 达到 **4.702**，显著低于 InterGen 的 5.918（Δ = -1.216），表明生成质量大幅提升。R Precision Top1 达到 **0.501**，相较 InterGen 的 0.371 提升 0.130，说明生成运动与文本描述的一致性更强。TIMotion+Transformer 同样取得次优表现（FID 5.433, Top1 0.491），验证了框架对不同交互混合模块的兼容性。

值得注意的是，TIMotion 在 R Precision 上的优势更为突出，这与 CII 的因果建模直接相关：交错排列两人运动帧使得交互特征在统一时序中自然耦合，而非依赖额外的交叉注意力模块。

**InterX 数据集**（Table 7）：TIMotion+RWKV 的 FID 为 **0.261**，显著优于 InterGen* 的 0.475（Δ = -0.214）；TIMotion+Mamba 的 R Precision Top1 为 **0.414**，高于 InterGen* 的 0.400。跨数据集验证表明因果交互建模具备良好的泛化能力。

### 消融实验：因果交互建模的普适性

**Table 2** 对比了三种时序建模方式（单人类扩展、分离建模、因果交互建模）在三种交互混合结构（Transformer、Mamba、RWKV）上的表现。因果交互建模在所有架构上均优于另两种方式。以 RWKV 为例：CII 将 FID 从 9.181（分离建模）降至 **5.943**，R Precision Top1 同步提升。这验证了核心洞察：双人交互运动具有内在的时序因果性，通过交错排列两人运动帧可以在统一序列中实现因果建模，无需复杂的交叉注意力设计。

### 消融实验：组件贡献

**Table 3** 展示了三个组件的逐步叠加效果。在 RWKV 架构上：
- 仅应用 CII：FID 5.943
- CII + RES：FID 进一步降低，R Precision 提升，验证了角色演变扫描对动态角色切换的适应能力
- CII + RES + LPA：FID 降至 **4.702**，R Precision Top1 达到 0.501，证明局部模式放大有效捕捉短时运动细节并提升整体生成质量

### LPA 的深入分析

**Table 4** 对 LPA 的归一化方式和卷积核尺寸进行消融。自适应层归一化（AdaLN）显著优于批归一化（BN）和层归一化（LN），卷积核 k=3,1 取得最佳性能。AdaLN 能够根据条件特征动态调整归一化参数，使局部模式建模更具适应性。

**Figure 6** 从频域角度揭示了 LPA 的作用机制。无 LPA 时，运动特征的高频分量平均振幅比例为 **0.9063**；添加 LPA 后降至 **0.3729**。高频分量的大幅减少直接对应生成运动的平滑性提升，这与 FID 指标的改善形成因果闭环。

### 计算效率

**Table 5** 展示了计算复杂度对比。TIMotion 在参数量和推理时间上均优于 InterGen，这与 CII 简化交互混合模块设计直接相关：因果交互序列避免了冗余的交叉注意力参数，同时保持了生成质量。

### 失败模式与局限性

1. **多人扩展未验证**：TIMotion 仅验证了双人运动生成（text-to-motion 和 motion in-betweening），未扩展到三人及以上场景。因果交互序列的交错策略在多人情境下的索引机制需要重新设计。
2. **数据集类型受限**：受限于现有双人数据集（InterHuman、InterX）的动作类别，未在包含物体交互或更多样化交互类型的数据集上验证。
3. **物理合理性未显式约束**：方法主要基于 InterGen 的损失函数和评估指标，未考虑穿透、脚部滑动等物理合理性约束，可能在复杂接触场景下产生不合理结果。
4. **角色演变的边界情况**：RES 通过对称因果序列处理角色切换，但在快速、高频角色交替的场景中，序列拼接方式可能引入时序断裂。

### 开放问题

- 如何将因果交互建模扩展到三人及以上参与者的运动生成？
- 在更丰富多样的交互数据集（如包含物体交互、多人运动）上，TIMotion 的表现如何？
- 能否将 LPA 的思想应用于其他时序生成任务（如语音驱动手势生成）？

### 补充图表

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation on the InterHuman [16] test set. We run all the evaluations 20 times. ± indicates a 95% confidence interval. Bold indicates the best result, while underline refers to the second best. ComMDM∗ indicates the ComMDM model fine-tuned in the original few-shot setting with 10 training samples and ComMDM indicates fine-tuned on the entire InterHuman training set*

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/005_Table_2.jpg]]
*Table 2: Comparison of different temporal modeling approaches on different interaction mixing structures. Our proposed causal interactive modeling is able to adapt to different interaction mixing architectures and outperforms the other two ways*

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/009_Table_3.jpg]]
*Table 3: Ablation studies on the effectiveness of each component in TIMotion. “CII” denotes Causal Interactive Injection, “RES” denotes Role-Evolving Scanning, and “LPA” denotes Localized Pattern Amplification*

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/010_Table_4.jpg]]
*Table 4: Ablation studies on LPA. “BN” denotes batch normalization, “LN” denotes layer normalization and “AdaLN” denotes adaptive layer normalization. “k=3,1” means that the first kernel size of the convolution is 3 and the second kernel size is 1*

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/013_Figure_6.jpg]]
*Figure 6: Spectrum of motion features. (a) and (b) show the spectrum of TIMotion w/o and w/ LPA, respectively. The horizontal axis denotes the frequency and the vertical axis represents the normalized magnitude. TIMotion w/ LPA contains fewer highfrequency components and therefore generates smoother motion*

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/012_Table_5.jpg]]
*Table 5: Comparison of computational complexity*

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/015_Table_7.jpg]]
*Table 7: Quantitative evaluation on the InterX [39] test set. We run the evaluations 20 times. ± indicates a 95% confidence interval. Bold indicates the best result, while underline refers to the second best. The results of comparative methods are directly borrowed from the InterX [39] paper except T2M∗ [10] and InterGen∗ [16]. The results of T2M∗ are taken from the open source repository of InterX [39] and the results of InterGen∗ are our own replication based on the unorganized training code provided by the authors of InterX and their open source validation code*

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative comparison with Intergen on human-human motion generation. Darker color indicates later frames. The sequences generated by TIMotion are more consistent with the text description*

![[assets/figures/papers/paper_list_l1750_TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Mo/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative results on the motion in-betweening task. The first and last frames are fixed. Darker colors indicate later frames. Our method achieves smooth and natural transitions between the conditioned motions*

## 方法谱系与知识库定位

### 1. 问题定位与基线关系

TIMotion 针对的是**双人运动生成**（human-human motion generation）这一细分任务，其核心瓶颈在于：现有方法侧重交互混合（interaction mixing）而忽视时序建模（temporal modeling），导致长序列和复杂交互场景下生成质量欠佳，且参数冗余。

在基线对比方面，TIMotion 与以下代表性工作形成直接参照关系：

- **InterGen**（Liang et al., IJCV 2024）：当前双人运动生成的主要基线方法，采用 Transformer 架构中的 self-attention 和 cross-attention 实现交互混合。在 InterHuman 测试集上，InterGen 的 FID 为 5.918，R Precision Top1 为 0.371。TIMotion+RWKV 将 FID 降至 4.702，R Precision Top1 提升至 0.501，分别改善 20.5% 和 35.0%（Table 1）。

- **MDM**（Tevet et al., ICLR 2023）：单人扩散运动生成方法，被扩展至双人场景作为基线。其单独建模两个人物、缺乏显式交互机制的做法，在双人任务上表现明显不足。

- **ComMDM**（Shafir et al., arXiv 2023）：在双人数据上微调 MDM 的版本。Table 1 显示，ComMDM 在全量数据微调后 FID 为 7.435，仍显著弱于 TIMotion 各变体，说明简单微调无法弥补交互建模的结构性缺失。

- **RIG**（Tanaka et al., ICCV 2023）：引入角色感知的交互生成方法，但角色分配是静态的，无法适应交互过程中主被动角色的动态演变。

- **T2M**（Guo et al., CVPR 2022）与 **TEMOS**（Petrovich et al., ECCV 2022）：通用文本到运动生成方法，缺乏针对双人交互的专门设计，在双人基准上表现有限。

### 2. 方法谱系中的定位：MetaMotion 抽象与因果交互建模

TIMotion 的核心贡献在于提出了 **MetaMotion** 抽象框架，将双人运动生成过程解耦为两个阶段：**时序建模**（temporal modeling）与**交互混合**（interaction mixing）。基于这一抽象，现有方法可被归为两类（Figure 1a-b）：一类先分别建模单人时序再混合交互，另一类先混合后建模时序。TIMotion 则属于第三类（Figure 1c）：通过**因果交互注入**（Causal Interactive Injection, CII）将时序建模与交互混合统一在因果序列框架中。

这一设计的关键洞察是：双人交互运动具有内在的**时序因果性**——在交互的每个瞬间，一方的运动因果性地影响另一方的响应。通过将两个单人运动序列交错排列为统一的因果交互序列 $x_{cii}$（Eq. 6），模型可以在单一序列中同时完成时序建模和交互混合，从而简化交互混合模块的设计并提升生成效果。

与基线方法的关键差异体现在三个“变化槽”（changed slots）：

| 技术槽 | 基线值 | TIMotion 方案 | 证据锚点 |
|--------|--------|---------------|----------|
| 交互混合机制 | Self-attention + Cross-attention（Transformer 类方法） | 因果交互注入（CII）+ 角色演变扫描（RES） | Section 4.4.1, Table 2 |
| 角色建模 | 静态角色分配或无显式角色建模 | 角色演变扫描（RES），通过对称因果序列适应动态角色切换 | Section 3.3.2, Table 3 |
| 局部运动模式处理 | 无专用局部模式建模 | 局部模式放大（LPA），使用 1D 卷积 + AdaLN + 残差连接 | Section 3.3.3, Table 4 |

### 3. 架构兼容性与泛化能力

TIMotion 的一个重要特性是其**架构无关性**：CII + RES 的因果交互建模方案可以适配不同的交互混合骨干网络。Table 2 展示了在 Transformer、Mamba、RWKV 三种架构上，因果交互建模均优于“单人扩展”（single-person extension）和“分离建模”（separate modeling）两种替代方案。以 RWKV 为例，因果交互建模的 FID 为 5.943，而分离建模的 FID 高达 9.181。

这种兼容性意味着 TIMotion 并非绑定于某一特定架构，而是提供了一种通用的交互建模范式，可随底层序列建模技术的演进而持续受益。

在跨数据集泛化方面，TIMotion 在 InterX 测试集上也展现出竞争力（Table 7）：TIMotion+RWKV 的 FID 为 0.261，优于 InterGen* 的 0.475；TIMotion+Mamba 的 R Precision Top1 达到 0.414，略高于 InterGen* 的 0.400。

### 4. 适用边界与局限

基于论文提供的分析，TIMotion 的适用边界和局限可归纳如下：

1. **参与者数量限制**：方法仅在双人运动生成任务上验证（text-to-motion 和 motion in-betweening），未扩展到三人及以上场景。因果交互注入的交错排列策略在三人以上时如何泛化，是一个开放问题。

2. **数据集覆盖范围**：实验基于 InterHuman 和 InterX 两个双人交互数据集，未在更多样化的交互类型（如包含物体交互、多人运动）或域外数据集上验证。方法的跨域鲁棒性尚待检验。

3. **评估指标依赖**：方法主要沿用 InterGen 的损失函数和评估指标（FID、R Precision、Diversity 等），未考虑物理合理性（如穿透检测、力学约束）等额外约束。生成的视觉质量（Figure 4）虽有改善，但缺乏物理层面的严格验证。

4. **角色演变的隐式建模**：RES 通过对称因果序列的通道拼接来隐式处理角色演变，而非显式建模角色状态转移。在极端不对称或长时角色切换场景下，这种隐式机制的有效性边界尚不明确。

### 5. 开放问题

1. **多人扩展**：如何将因果交互建模从双人交错序列推广到三人及以上的多参与者运动生成？直接的多序列交错可能导致因果距离过长，需要新的序列组织策略。

2. **跨任务迁移**：Localized Pattern Amplification 通过 1D 卷积捕获短时运动模式的思想，能否应用于其他时序生成任务（如语音驱动手势生成、群体行为模拟）？

3. **物理合理性约束**：在现有扩散损失和几何正则化基础上，引入物理仿真或接触约束是否能进一步提升生成运动的真实性和合理性？

4. **更大规模预训练**：TIMotion 的 CLIP 文本编码器是冻结的，若在大规模运动-文本数据上进行端到端或部分微调，是否能进一步提升文本-运动对齐精度？

## 原文 PDF

![[paperPDFs/CVPR_2025/TIMotion_Temporal_and_Interactive_Framework_for_Efficient_Human_Human_Motion_Generation.pdf]]