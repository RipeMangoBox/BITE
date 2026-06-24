---
title: Motion-Conditioned Diffusion Model for Controllable Video Synthesis
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/Motion_Conditioned_Diffusion_Model_for_Controllable_Video_Synthesis.pdf
aliases:
- MMCDM
- MCDMCVS
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 引入流补全（Flow Completion）模块，将稀疏运动控制转化为稠密光流（dense flow），为后续的扩散模型提供丰富的运动先验和空间一致性信号，从而显著提升合成质量和运动可控性。
primary_logic: 将可控视频合成分解为“稀疏-稠密光流补全”和“基于稠密流的未来帧预测”两个子任务，显式解耦运动理解与帧生成，降低了学习难度，使扩散模型在复杂场景中仍能生成高质量且忠实于用户笔触运动指令的视频。
claims:
- 消融实验表明，移除流补全模块（单阶段模型）会导致FVD从194.30大幅上升至273.86，证实流补全对生成质量的决定性作用。
- 在TaiChi-HD和Human3.6M上，MCDiff在FVD指标上显著优于先前的笔触引导视频合成方法II2V和iPOKE，达到state-of-the-art视觉质量。
- 通过运动可控性指标（ADE）评估，MCDiff能更精确地遵循输入笔触的运动指令，尤其在多个笔触（5/9个）时优势明显，ADE显著低于II2V和iPOKE。
- TaiChi-HD 上 FVD (lower is better) = 142.57 (1 stroke), 126.69 (5 strokes), 113.12 (9 strokes)
---

# Motion-Conditioned Diffusion Model for Controllable Video Synthesis

> [!tip] 核心洞察
> 将可控视频合成分解为“稀疏-稠密光流补全”和“基于稠密流的未来帧预测”两个子任务，显式解耦运动理解与帧生成，降低了学习难度，使扩散模型在复杂场景中仍能生成高质量且忠实于用户笔触运动指令的视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | 运动条件扩散模型用于可控视频合成 |
| 英文题名 | Motion-Conditioned Diffusion Model for Controllable Video Synthesis |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2304.14404) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | MCDiff (Motion-Conditioned Diffusion Model) |
| Dataset | TaiChi-HD, Human3.6M, TaiChi-HD / Human3.6M |

> [!tip] 效果简介
> - TaiChi-HD 上，FVD (lower is better) 142.57 (1 stroke), 126.69 (5 strokes), 113.12 (9 strokes) vs II2V ≈ 191 (1 stroke), iPOKE ≈ 168 (1 stroke) [exact numbers not extracted; MCD... (MCDiff achieves substantially lower FVD (e.g., ~49 lower than II2V for 1 stroke...)。
> - Human3.6M 上，FVD (lower is better) 117.60 (1 stroke), 114.82 (5 strokes), 111.38 (9 strokes) vs II2V ≈ 177 (1 stroke), iPOKE ≈ 131 (1 stroke) [exact numbers not extracted] (MCDiff clearly outperforms prior methods across all stroke counts)。
> - TaiChi-HD / Human3.6M 上，Average Displacement Error (ADE, lower is better) TaiChi-HD: 2.77 (1 stroke), 2.72 (5 strokes), 2.90 (9 strokes); Human3.6M: 1.64... vs II2V: TaiChi-HD 4.17/7.51/11.36; iPOKE: 2.63/5.09/8.94 (MCDiff reduces ADE by up to ~8.5 on TaiChi-HD (9 strokes) and ~3 on Human3.6M)。

## 概述

**核心问题**：给定一张起始帧和用户指定的稀疏运动笔触（sparse strokes），直接生成高质量、运动可控的视频帧存在高度歧义——稀疏笔触仅提供少量像素的位移信号，缺乏对场景内容的语义理解，导致单阶段扩散模型训练困难，难以产生忠实于运动指令的视频。

**核心洞察**：MCDiff 将可控视频合成分解为两个子任务——**稀疏‑稠密光流补全**与**基于稠密流的未来帧预测**。这一分解显式解耦了运动理解与帧生成，使扩散模型在复杂场景下仍能生成高质量且严格遵循笔触运动指令的视频。

**方法定位**：MCDiff 是一个两阶段自回归框架。第一阶段通过流补全模块（Flow Completion Model）将稀疏笔触转化为语义丰富、空间连续的稠密光流图，为后续生成提供强运动先验；第二阶段以当前帧和预测的稠密光流为条件，利用条件扩散模型步进式合成未来帧。两个模块先分别预训练，再端到端级联微调，消除模块间的领域偏差。相比于先前的笔触引导方法 **II2V**（基于隐空间操纵与循环网络）和 **iPOKE**（基于单像素扰动与运动传播），MCDiff 在运动条件表示形式、模型结构与训练策略三个关键维度上做出了系统性改进。

**主要结果**：在 TaiChi‑HD 和 Human3.6M 两个基准上，MCDiff 在视频质量（FVD）和运动可控性（ADE）指标上均显著优于 II2V 与 iPOKE。消融实验进一步证实：移除流补全模块（即退化为单阶段扩散模型）会导致 FVD 从 194.30 急剧上升至 273.86，验证了两阶段设计对生成质量的决定性作用。

## 背景与动机

### 问题背景：稀疏运动控制下的视频合成

可控视频合成旨在根据用户提供的运动指令，从给定的起始帧生成一段符合预期的视频序列。一种直观且灵活的控制形式是**稀疏笔触（sparse strokes）**——用户只需在起始帧上绘制若干带有方向的箭头，即可指定特定像素在后续帧中的位移。然而，这一任务面临根本性挑战：稀疏笔触仅提供了极少数受控像素的运动信息，而绝大多数像素的运动是完全未知的，这种高度歧义的输入使得从稀疏控制直接生成完整视频帧变得异常困难。

### 现有方法缺口：单阶段建模的困境

在MCDiff提出之前，笔触引导的可控视频合成方法（如**II2V**和**iPOKE**）主要采用单阶段框架，试图直接从稀疏笔触和当前帧中生成后续帧。这类方法面临两个核心瓶颈：

1. **语义理解缺失**：稀疏笔触本身不包含对视频内容的语义理解（如前景人体与背景场景的区分），模型难以推断未受控像素的合理运动。
2. **学习难度过高**：将运动推断与帧生成耦合在单一模型中，要求扩散模型同时解决“运动补全”和“内容生成”两个子问题，训练信号复杂，导致生成质量受限。

论文中的消融实验直接验证了这一困境：若将MCDiff的流补全模块移除，退化为单阶段条件扩散模型（**Ours w/o F**），在MPII Human Pose数据集上FVD从194.30急剧恶化至273.86（Table 2），证实了单阶段设计难以产出高质量视频。

### 核心动机：解耦运动理解与帧生成

MCDiff的核心动机源于一个关键洞察：**将可控视频合成分解为“稀疏-稠密光流补全”与“基于稠密流的未来帧预测”两个子任务，可以显式解耦运动理解与内容生成，从而显著降低学习难度**。

具体而言，MCDiff引入一个**流补全模型（Flow Completion Model）**，先将用户提供的稀疏笔触转化为语义丰富、空间连续的稠密光流图（dense flow map），为后续的帧生成扩散模型提供丰富的运动先验和空间一致性信号。这一两阶段设计使得扩散模型不再需要从高度歧义的稀疏输入中同时推断运动和内容，而是基于可靠的稠密运动场专注于高质量帧的合成。

### 方法定位

MCDiff属于**运动条件扩散模型**在可控视频合成中的应用。与先前方法不同，MCDiff并非在隐空间中进行运动操控，而是通过显式的光流补全将稀疏控制转化为稠密运动场，再以该运动场为条件驱动扩散模型生成未来帧。该方法在TaiChi-HD和Human3.6M两个基准上显著优于II2V和iPOKE，在视觉质量（FVD）和运动可控性（ADE）两个维度均取得了当时的最优结果（Table 1, Table 3）。

## 核心创新

MCDiff 的核心创新在于将可控视频合成从“从稀疏笔触直接生成视频帧”这一高度歧义的单阶段任务，重构为“稀疏‑稠密流补全 + 基于稠密流的未来帧预测”的两阶段级联框架。这一设计显式解耦了运动理解与帧生成，使扩散模型能够在复杂场景中稳定输出高质量且忠实于用户运动指令的视频。

### 关键 changed slots

#### 运动条件表示形式：从稀疏笔触到稠密光流

基线方法（如 **II2V** 和 **iPOKE**）直接以用户指定的稀疏笔触作为运动条件输入生成模型。这些稀疏流图包含大量缺失值，缺乏对视频内容的语义理解，导致生成过程面临极高的歧义性，难以同时保证视觉质量和运动可控性。

MCDiff 引入**流补全模块（Flow Completion Model, F）**，将稀疏瞬时运动 $\boldsymbol{S} = \{ \boldsymbol{s}_{12}, \dots, \boldsymbol{s}_{(n-1)n} \}$ 转化为语义丰富且空间连续的稠密光流图 $\hat{d}_{a \to b}$。该模块以当前帧和稀疏流为输入，通过 UNet 预测每个像素的运动矢量，为后续扩散生成提供了强有力的运动先验和空间一致性信号（图2）。

#### 模型结构：从单阶段到两阶段级联

单阶段基线（包括论文中的消融变体 **Ours w/o F**）直接将稀疏笔触与图像拼接后送入条件扩散模型，试图一步完成运动理解与帧生成。这种方式在复杂场景下训练困难，输出视频往往存在严重的伪影和运动偏差。

MCDiff 采用两阶段级联架构：

1. **流补全模块 F** 负责从稀疏笔触和当前帧中推断稠密运动场；
2. **未来帧预测模块 G** 以当前帧和预测的稠密光流为条件，通过条件扩散 UNet 生成下一帧。

两个模块以自回归方式步进式合成完整视频 $\mathcal{X} = \{ x_1, \dots, x_n \}$（图2）。消融实验证实了这一设计的决定性作用：在 MPII Human Pose 上，移除流补全模块后 FVD 从 194.30 急剧上升至 273.86（表2），表明单阶段模型难以有效利用稀疏运动信息。

#### 训练策略：从独立训练到端到端联合微调

MCDiff 的训练分为两个阶段：首先分别预训练 F 和 G 各 400k 次迭代，随后将两个模块级联并进行 100k 次迭代的端到端联合微调。微调目标为流补全损失与扩散生成损失的加权和：

$$\mathcal{L} = \lambda_F \cdot \mathcal{L}_F + \lambda_G \cdot \mathcal{L}_G$$

其中流补全损失 $\mathcal{L}_F$ 采用运动幅度加权的 MSE，以缓解静止场景下零值支配问题；未来帧预测损失 $\mathcal{L}_G$ 为标准扩散模型的噪声预测损失。联合微调消除了模块间的领域偏差，进一步提升了生成视频的保真度和连贯性。

## 整体框架

MCDiff 将可控视频合成分解为**流补全**与**未来帧预测**两个子任务，以自回归方式逐帧生成视频。给定起始帧 $x_1$ 和用户指定的稀疏瞬时运动集合 $\boldsymbol{S} = \{ \boldsymbol{s}_{12}, \dots, \boldsymbol{s}_{(n-1)n} \}$，模型输出 $n$ 帧视频序列 $\mathcal{X} = \{ x_1, \dots, x_n \}$，使每一帧的内容和运动忠实于输入条件。

### 两阶段自回归管线

如图2所示，MCDiff 由两个核心模块串联构成：

1. **流补全模型 $F$**：在每一时间步，接收当前帧 $x_i$ 和对应的稀疏笔触 $\boldsymbol{s}_{i \to i+1}$，预测稠密光流图 $\hat{d}_{i \to i+1}$，实现从稀疏运动控制到像素级运动场的推断。该模块为后续帧生成提供丰富的运动先验和空间一致性信号。

2. **未来帧预测模型 $G$**：以当前帧 $x_i$ 和预测的稠密光流 $\hat{d}_{i \to i+1}$ 为条件，通过条件扩散过程生成下一帧 $x_{i+1}$。扩散模型在去噪过程中将噪声变量与两个条件（当前帧、稠密光流）沿通道维度拼接，使生成帧在保持内容连贯性的同时精确遵循指定运动。

### 端到端微调

为消除模块间的领域偏差，MCDiff 将 $F$ 与 $G$ 级联为端到端可微管线 $G(x_a, F(x_a, s_{ab}))$，并联合优化流补全损失 $\mathcal{L}_F$ 与未来帧预测损失 $\mathcal{L}_G$：

$$\mathcal{L} = \lambda_F \cdot \mathcal{L}_F + \lambda_G \cdot \mathcal{L}_G$$

### 训练监督信号

流补全模型和未来帧预测模型的训练均依赖从真实视频中提取的稠密光流真值（图3）。具体而言，通过 HRNet 检测人体关键点并结合 PIP 一般点跟踪算法，获取视频中跟踪点的轨迹，进而插值得到逐像素的稠密光流图作为监督信号。

### 关键设计动机

消融实验（Table 2）证实了该两阶段设计的决定性作用：移除流补全模块（即单阶段扩散模型，直接将稀疏笔触与图像拼接作为扩散输入）会导致 FVD 从 194.30 大幅上升至 273.86。这表明稀疏笔触的高度歧义性使得单阶段模型难以学习从稀疏控制到视频帧的直接映射，而显式解耦运动理解与帧生成显著降低了学习难度。

### 补充图表

![[assets/figures/papers/paper_list_l1055_https_arxiv_org_abs_2304_14404/figures/002_Figure_2.jpg]]
*Figure 2: Overview. MCDiff is an autoregressive video synthesis model. For each time step, the model is guided by the previous frame (i.e. start or previously predicted frame) and the momentary segment of input strokes (marked as colored arrows, a brighter color indicates a larger motion). Our flow completion model first predicts dense flows representing perpixel momentary motion. Then, the future-frame prediction model synthesizes the next frame based on the previous frame and the predicted dense flow through a conditional diffusion process. Finally, the collection of all predicted frames forms a video sequence adhering to the context provided by the start frame and the motion specified by the strok...*

## 核心模块与公式推导

MCDiff 将可控视频合成分解为两个级联的子任务，形成端到端可微的流水线。给定起始帧 $x_a$ 与用户指定的瞬时稀疏运动笔触集合 $\boldsymbol{s}_{ab}$，系统首先通过**流补全模型 $F$** 预测稠密光流图，随后由**未来帧预测模型 $G$** 以扩散过程生成下一帧 $x_b$，整体可表示为 $G(x_a, F(x_a, s_{ab}))$（Section 3.4）。

### 流补全模型 $F$

流补全模型的核心功能是将高度歧义的稀疏笔触转化为空间连续、语义丰富的稠密光流图。其输入为当前帧 $x_i$ 与瞬时稀疏光流 $\boldsymbol{s}_{i \to i+1}$，输出为预测的稠密光流图 $\hat{d}_{i \to i+1}$。该模块通过 UNet 架构实现，利用对视频帧的语义理解来推断未被笔触覆盖区域的合理运动。

训练 $F$ 采用加权 MSE 损失，以缓解静止场景下零值光流主导梯度的问题。损失函数按像素位置 $p$ 对预测误差进行加权，权重 $w_p$ 由该位置真实光流幅值决定：

$$
\mathcal{L}_F = \frac{1}{\|\mathcal{P}\|} \sum_{p \in \mathcal{P}} w_p \cdot \| d_{a \to b}(p) - \hat{d}_{a \to b}(p) \|_2, \quad w_p = \lambda + \frac{\|\hat{d}_{a \to b}(p)\|_2}{\hat{d}_{\max}}
$$

其中 $\mathcal{P}$ 为所有像素位置的集合，$\lambda$ 为基础权重常数，$\hat{d}_{\max}$ 为当前真实光流图中的最大幅值。该设计使大运动区域获得更高优化权重，避免模型偏向预测全零光流（Section 3.2, Eq. (1)）。

### 未来帧预测模型 $G$

$G$ 是一个条件扩散模型，以当前帧 $x_a$ 和流补全模型预测的稠密光流 $\hat{d}_{ab}$ 为条件，通过迭代去噪生成下一帧 $x_b$。具体实现上，将带噪变量 $x_b^t$ 与条件 $x_a$、$\hat{d}_{ab}$ 沿通道维度拼接后输入去噪 UNet $\epsilon_\theta$，使其学会预测所添加的噪声 $\epsilon$。

训练目标为标准扩散模型的噪声预测损失：

$$
\mathcal{L}_G = \mathbb{E}_{x_b, \epsilon \sim \mathcal{N}(0,1), t} \| \epsilon - \epsilon_\theta(x_b^t, t, x_a, \hat{d}_{ab}) \|_2^2
$$

其中 $t$ 为扩散时间步，$x_b^t$ 为对真实下一帧 $x_b$ 加噪后的隐变量。该损失驱动模型在给定运动先验和内容上下文的条件下，生成与真实后续帧分布一致的预测（Section 3.3, Eq. (2)）。

### 端到端联合微调

为消除 $F$ 与 $G$ 分阶段训练引入的领域偏差，将两个模块级联后进行端到端微调。此时 $G$ 的条件光流来自 $F$ 的实时预测输出，而非预计算的真值光流，使整个流水线形成可微通路。联合优化目标为两阶段损失的加权和：

$$
\mathcal{L} = \lambda_F \cdot \mathcal{L}_F + \lambda_G \cdot \mathcal{L}_G
$$

其中 $\lambda_F$ 与 $\lambda_G$ 为平衡两项损失的超参数。消融实验证实，端到端微调后的完整模型（Table 2 中 Ours Full）在 MPII Human Pose 上取得 FVD 194.30，相比单阶段变体（Ours w/o F, FVD 273.86）有显著提升，验证了流补全模块及其与帧生成模块联合优化的关键作用（Section 3.4, Eq. (3); Table 2）。

### 补充图表

![[assets/figures/papers/paper_list_l1055_https_arxiv_org_abs_2304_14404/figures/003_Figure_3.jpg]]
*Figure 3: Annotations of Video Dynamics. We express video dynamics by tracking both the keypoints (red, marked with body skeletons for better visualization) and a grid of general points (gray). With the trajectories of the tracking points throughout a video, we can easily yield the dense flow map*

![[assets/figures/papers/paper_list_l1055_https_arxiv_org_abs_2304_14404/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative Results of Flow Completion Model on MPII Human Pose [1]. From top to bottom, we show (a) the input frame with the strokes, (b) the next frame in the real video, and (c) our predicted flows. Our flow completion model can predict high-quality flows based on the semantic understanding of the video frame and the sparse motion control*

## 实验与分析

### 1. 实验设置

**数据集与评价指标**。MCDiff在三个基准上评估：**TaiChi-HD** (Siarohin et al., 2019) 和 **Human3.6M** (Ionescu et al., 2014) 用于与先前方法比较，**MPII Human Pose** (Andriluka et al., 2014) 用于消融和多样化场景验证。视频质量评价采用 **FVD** (Unterthiner et al., 2018) 作为主要指标，辅以 **LPIPS** (Zhang et al., 2018)、**SSIM** 和 **PSNR**。运动可控性通过 **Average Displacement Error (ADE)** 和 **召回率 (Recall)** 衡量——使用HRNet关键点检测器统一提取受控像素的轨迹，消除评估算法偏差。

**训练策略**。MCDiff的训练分两个阶段：(1) 分别预训练流补全模块F和未来帧预测模块G各400k次迭代（batch size 40）；(2) 端到端联合微调整个管线100k次迭代（batch size 20）。F的训练使用随机采样的跟踪点流：每人的30%关键点加上8个（MPII）或4个（TaiChi-HD/Human3.6M）一般点。所有比较方法使用相同的起始帧和从测试视频提取的笔触控制，确保输入条件一致。

### 2. 主要结果

**视频质量对比**。如Table 1所示，MCDiff在TaiChi-HD和Human3.6M上均显著优于先前方法 **II2V** 和 **iPOKE**。以FVD衡量，在TaiChi-HD上MCDiff在1个笔触时达到142.57，而II2V约191，iPOKE约168；随着笔触数量增加至9个，MCDiff的FVD进一步降至113.12，性能差距持续扩大。在Human3.6M上趋势一致：MCDiff在1/5/9个笔触下的FVD分别为117.60、114.82、111.38，显著低于II2V（~177）和iPOKE（~131）。

**运动可控性**。Table 3的ADE评估表明，MCDiff能更精确地遵循用户笔触的运动指令。在TaiChi-HD上，MCDiff在5个笔触时ADE为2.72（II2V: 7.51，iPOKE: 5.09），9个笔触时ADE为2.90（II2V: 11.36，iPOKE: 8.94），优势随笔触数量增加而扩大。Human3.6M上MCDiff同样保持最低ADE（1.64–1.86），而II2V和iPOKE的误差随笔触增多急剧上升。召回率指标也呈现一致的领先趋势。

**定性分析**。Figure 4的定性对比显示，MCDiff生成的视频在人体形状保持和运动匹配度上均优于iPOKE。iPOKE在多笔触场景下容易出现肢体变形和运动偏差，而MCDiff借助稠密流先验能更忠实地执行指定的关键点位移。

### 3. 消融实验

**流补全模块的关键性**。Table 2报告了核心消融结果：移除流补全模块（单阶段扩散模型，Ours w/o F）导致FVD从194.30飙升至273.86，LPIPS从0.116升至0.131，SSIM从0.762降至0.734。这一显著退化证实了“稀疏→稠密”流补全对于降低学习难度和提升生成质量的决定性作用。

**端到端微调的贡献**。Table 2中的Full模型即为端到端微调后的两阶段模型。与单独训练后直接级联相比，联合微调进一步弥合了F和G之间的领域偏差，使预测的稠密流更适配后续扩散生成过程，从而提升了视频的保真度和时序连贯性。

### 4. 流补全模型的可视化

Figure 5展示了流补全模块在MPII Human Pose上的定性结果。给定输入帧和稀疏笔触（红箭头），模型能基于对帧内容的语义理解，预测出高质量、空间连续的稠密光流图。预测流不仅覆盖了笔触指定的区域，还合理推断了背景和非受控区域的运动（如背景因相机运动产生的整体位移），验证了从稀疏控制到稠密运动推断的有效性。

### 5. 多样化场景下的泛化能力

Figure 6展示了MCDiff在MPII Human Pose上多种人体活动和相机调整场景下的合成结果。模型能处理跳舞、运动等复杂人体动作，同时在底部两行展示了前景/背景流的分离能力——当笔触指定在背景区域时，模型正确理解为相机变焦操作而非前景物体运动，生成了合理的缩放效果。这验证了流补全模块对前景/背景运动语义的隐式学习。

### 6. 局限性与失败模式

尽管MCDiff在受控人体场景中表现优异，但仍存在以下局限：

- **分布外泛化不足**：训练数据以人体动作为主，对于新颖物体组合或与训练分布差异较大的编辑可能产生不理想的输出。模型的运动理解能力受限于训练数据的语义覆盖范围。
- **运动真值获取瓶颈**：流补全模块的训练依赖HRNet关键点和PIP一般点跟踪提取的稠密光流真值。在纹理缺失表面或存在视觉错觉的区域，现有点跟踪算法难以获得物理上准确的光流，限制了模型对复杂运动的建模精度。
- **步进式误差累积**：作为自回归模型，MCDiff在长序列生成中可能因前序帧的微小误差逐步放大而导致后期帧质量下降。论文未对此进行定量分析，需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l1055_https_arxiv_org_abs_2304_14404/figures/004_Table_1.jpg]]
*Table 1: MCDiff outperforms prior methods on two major benchmarks [23, 39]. We report FVD [46], LPIPS [54], SSIM [50], and PSNR (↓ indicates the lower the better, and vice versa). Given video synthesis naturally does not have a definitive ground truth for reference-based evaluation, FVD is currently the most reliable metric for assessing visual quality and diversity. MCDiff shows substantial performance gain on both datasets under different numbers of input strokes*

![[assets/figures/papers/paper_list_l1055_https_arxiv_org_abs_2304_14404/figures/007_Table_2.jpg]]
*Table 2: Ablation analysis of Flow Completion Model on MPII Human Pose [1]. We report FVD [46], LPIPS [54], SSIM [50], and PSNR. The numbers show the effectiveness of the two-stage model design*

![[assets/figures/papers/paper_list_l1055_https_arxiv_org_abs_2304_14404/figures/009_Table_3.jpg]]
*Table 3: MCDiff achieves superior motion controllability on two major benchmarks [23, 39]. We report the Average Displacement Error (AVD) and the recall rate (Recall). MCDiff outperforms prior methods with a substantial performance gap on both datasets under different numbers of input strokes*

![[assets/figures/papers/paper_list_l1055_https_arxiv_org_abs_2304_14404/figures/001_Figure_1.jpg]]
*Figure 1: MCDiff enables flexible and accurate motion control in high-quality video synthesis with diffusion models. Given a start frame and a set of user-specified strokes (red arrows), our proposed MCDiff synthesizes a video following the desired motion while preserving the content. We show that MCDiff learns the concept of foreground and background flows, where the former specifies the motions of foreground objects (as top-two rows), while the latter controls the camera adjustments (e.g., zoom-in or zoom-out as bottom-two rows)*

![[assets/figures/papers/paper_list_l1055_https_arxiv_org_abs_2304_14404/figures/008_Figure_6.jpg]]
*Figure 6: MCDiff synthesizes high-quality videos with diverse contents and motions. We input MCDiff with the start frames sampled from the testing videos of MPII Human Pose [1] and the strokes manually specified by humans. Under diverse conditions and activities, MCDiff can synthesize high-quality and temporally consistent videos while attending to the input conditions. Noticeably, in the bottom two rows, the model is aware of the strokes assigned on the background scene indicating the camera adjustment. We show more visual results in Appendix B*

![[assets/figures/papers/paper_list_l1055_https_arxiv_org_abs_2304_14404/figures/005_Figure_4.jpg]]
*Figure 4: MCDiff achieves better visual quality and controllability compared to iPOKE [6] on two benchmarks [23, 39]. We input iPOKE [6] and MCDiff with the same start frames (the leftmost column of each sequence) and motions of 5 human keypoints (red arrows on the nose, elbows, and knees), which are sampled from the testing videos (the top row of each sequence). The target locations of the keypoints are marked at the end frames (red crosses at the rightmost column of each sequence). MCDiff is able to synthesize the videos with better quality while more faithfully following the motions specified by the strokes*

## 方法谱系与知识库定位

### 1. 与基线方法的对比定位

MCDiff 处于**稀疏笔触引导的可控视频合成**这一任务线上，其直接对比的前序工作包括 **II2V** 和 **iPOKE**。这两者均试图从用户指定的稀疏运动笔触生成未来帧，但在运动条件表示和模型架构上存在根本差异：

- **II2V** 采用隐空间操控与循环网络相结合的方式，直接从稀疏笔触推断视频动态。其核心瓶颈在于稀疏笔触本身具有高度歧义——同一组笔触可对应无数种可能的像素级运动，单阶段模型缺乏足够的运动先验来消解这种歧义，导致生成质量受限。在 TaiChi-HD 上 1 笔触设置下，II2V 的 FVD 约为 191，而 MCDiff 为 142.57（Table 1）。

- **iPOKE** 通过“戳动”单个像素并传播运动来实现控制，本质上仍是一种稀疏运动表示下的直接帧生成。在 Human3.6M 上 1 笔触设置下，iPOKE 的 FVD 约为 131，MCDiff 为 117.60（Table 1）。定性对比（Figure 4）进一步显示，iPOKE 在人体形状保持和运动条件忠实度上均弱于 MCDiff。

- **单阶段扩散模型（Ours w/o F）** 是 MCDiff 自身消融出的基线：将稀疏笔触与当前帧直接拼接输入条件扩散 UNet 进行帧生成。在 MPII Human Pose 上，该变体的 FVD 从完整模型的 194.30 飙升至 273.86（Table 2），从反面验证了流补全模块对生成质量的决定性作用。

上述对比揭示了一个共性瓶颈：**稀疏运动条件与高维像素生成之间的语义鸿沟**。MCDiff 通过插入显式的“稀疏→稠密”流补全阶段，将运动理解与帧生成解耦，从而系统性地缓解了这一瓶颈。

### 2. 技术谱系中的位置

从方法学角度，MCDiff 处于以下几条技术线的交叉点：

- **条件扩散模型**：MCDiff 的未来帧预测模块 G 直接继承自 LDM（Latent Diffusion Model）的条件范式，将当前帧和稠密光流作为条件拼接到扩散 UNet 的输入通道中。这与同期大量条件扩散工作共享相同的噪声预测训练框架（$\mathcal{L}_G = \mathbb{E}_{x_b, \epsilon, t} \| \epsilon - \epsilon_\theta(x_b^t, t, x_a, \hat{d}_{ab}) \|_2^2$）。

- **光流补全与运动推断**：流补全模块 F 本质上是一个运动先验学习器，从稀疏跟踪点推断密集运动场。这一设计借鉴了光流估计和运动外推领域的思想，但将其嵌入到生成式管线中作为中间表示，而非最终输出。加权 MSE 损失（$\mathcal{L}_F$）中按运动幅度加权的策略（$w_p = \lambda + \|\hat{d}_{a \to b}(p)\|_2 / \hat{d}_{\max}$）专门针对静止场景下零值主导的分布不平衡问题，这是一项务实的训练技巧。

- **自回归视频生成**：MCDiff 以自回归方式逐帧生成视频，每步以前一帧和当前瞬时笔触为条件。这种步进式生成策略与 VideoGPT 等自回归视频模型同源，但 MCDiff 的运动条件来自用户笔触而非隐变量先验。

- **两阶段训练与端到端微调**：先分别预训练 F 和 G（各 400k 次迭代），再级联端到端微调（100k 次迭代），这一策略平衡了模块收敛与联合优化，类似于“预训练+微调”的迁移学习范式，但应用于同一管线的子模块间。

### 3. 适用边界与局限

基于论文报告的结果和训练设置，MCDiff 的适用边界可归纳如下：

- **数据分布依赖**：训练数据主要来自 TaiChi-HD、Human3.6M 和 MPII Human Pose，三者均以人体动作为主。论文明确指出，对于与训练分布差异较大的新颖物体组合或编辑，模型可能产生不理想的输出。这意味着 MCDiff 目前是一个**领域专用（domain-specific）**模型，而非通才型视频合成器。

- **运动真值获取的物理限制**：流补全模块的训练依赖于从视频中提取的稠密光流真值，而该真值通过 HRNet 关键点和 PIP 一般点跟踪获得。在纹理缺失表面或存在视觉错觉的区域，基于视觉特征的点跟踪算法难以获得物理上准确的光流，这构成了运动建模的上限。论文将此列为开放问题，指出需要物理真实运动场（如通过仿真或专用传感器获取）来突破这一限制。

- **笔触数量与运动可控性的关系**：Table 3 显示，随着笔触数量从 1 增加到 9，MCDiff 的运动可控性指标 ADE 在 TaiChi-HD 上从 2.77 变为 2.90（略有波动），而 II2V 则从 4.17 急剧恶化至 11.36。这表明 MCDiff 对笔触数量增加的鲁棒性显著优于基线，但其自身的 ADE 并未随笔触增加而单调改善——这是一个需要进一步分析的细微现象。

- **评估指标的固有局限**：论文主要依赖 FVD 作为视觉质量指标，并承认视频合成天然缺乏确定性真值，因此基于参考的指标（如 PSNR、SSIM）的参考价值有限。运动可控性评估（ADE 和召回率）虽通过统一使用 HRNet 进行关键点检测来消除算法偏差，但仍受限于关键点检测器本身的精度。

### 4. 开放问题

从论文的讨论和实验结果中，可提炼出以下值得后续探索的方向：

1. **流补全在高度歧义场景下的鲁棒性**：当稀疏笔触极少（如 1 个笔触）且场景语义复杂时，流补全模型如何保持预测的合理性？论文展示了定性结果（Figure 5），但缺乏针对极端歧义场景的系统性压力测试。

2. **通才型运动控制模型的构建**：能否将 MCDiff 扩展为统一处理任意物体和背景运动的通用框架？这需要构建包含多样化物体类别和运动模式的大规模数据集，并可能需要在流补全模块中引入更强的语义泛化能力。

3. **物理真实运动场的获取与利用**：对于纹理缺失表面和视觉错觉场景，现有的视觉跟踪方案存在根本性局限。引入物理仿真、深度传感器或多模态信号可能是突破这一瓶颈的路径。

4. **笔触数量与生成质量的非单调关系**：Table 1 中 MCDiff 的 FVD 随笔触数量增加而改善（TaiChi-HD: 142.57 → 126.69 → 113.12），但 ADE 并未同步改善。这种视觉质量与运动精度的潜在权衡值得更深入的分析。

5. **自回归误差累积**：MCDiff 的自回归生成方式意味着早期帧的预测误差会向后续帧传播。论文未专门分析长序列生成时的误差累积效应，这是自回归视频生成方法的共性问题。

## 原文 PDF

![[paperPDFs/arxiv_2023/Motion_Conditioned_Diffusion_Model_for_Controllable_Video_Synthesis.pdf]]