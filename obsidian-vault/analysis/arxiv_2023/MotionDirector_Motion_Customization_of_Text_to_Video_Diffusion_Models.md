---
title: "MotionDirector: Motion Customization of Text-to-Video Diffusion Models"
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/MotionDirector_Motion_Customization_of_Text_to_Video_Diffusion_Models.pdf
project_link: https://showlab.github.io/MotionDirector
code_link: https://github.com/AILab-CVC/
aliases:
- MotionDirector
tags:
- arxiv_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 通过双路径低秩适配（LoRA）架构，将外观学习与运动学习分离：空间LoRA仅从单帧学习外观，时间LoRA从多帧学习运动，并引入外观去偏时间损失以减少外观对时间训练任务的影响。
primary_logic: 在隐空间中，运动主要影响帧序列之间的连通结构，而外观主要影响不同序列点集之间的距离；通过分别用空间/时间LoRA建模这两类因素，并对外观偏差进行去中心化处理，可以解耦运动与外观，使运动定制泛化到任意外观。
claims:
- 提出的双路径架构将空间LoRA仅用于外观学习、时间LoRA用于运动学习，彼此解耦。
- 外观去偏时间损失通过去中心化噪声（φ操作）有效减少了外观对运动学习的影响。
- 在UCF Sports Action基准上，人类评估者对MotionDirector的运动保真度偏好率达75%以上，远高于基础模型的25%。
- 在LOVEU-TGVE-2023基准上，MotionDirector在外观多样性与运动保真度方面大幅领先可控生成方法和调谐方法。
---

# MotionDirector: Motion Customization of Text-to-Video Diffusion Models

> [!tip] 核心洞察
> 在隐空间中，运动主要影响帧序列之间的连通结构，而外观主要影响不同序列点集之间的距离；通过分别用空间/时间LoRA建模这两类因素，并对外观偏差进行去中心化处理，可以解耦运动与外观，使运动定制泛化到任意外观。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionDirector：文本到视频扩散模型的运动定制 |
| 英文题名 | MotionDirector: Motion Customization of Text-to-Video Diffusion Models |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2310.08465) · [Project](https://showlab.github.io/MotionDirector) · [Code](https://github.com/AILab-CVC/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | MotionDirector |
| Dataset | UCF Sports Action, LOVEU-TGVE-2023 |

> [!tip] 效果简介
> - UCF Sports Action (多视频运动定制) 上，人类偏好（运动保真度） vs 基础模型 ≥75% vs 25% (≥+50%)。
> - LOVEU-TGVE-2023 (单视频运动定制) 上，人类偏好（外观多样性） vs ModelScope 54.84 vs 45.16 (+9.68)；人类偏好（外观多样性） vs VideoComposer 72.83 vs 27.17 (+45.66)；人类偏好（运动保真度） vs VideoComposer 61.24 vs 38.76 (+22.48)。

## 概要

**问题瓶颈**：现有文本到视频扩散模型的适配方法（整体微调、参数高效调谐、单路径LoRA）在定制特定运动时，往往将运动与训练视频中的有限外观耦合，导致学到的运动难以泛化到不同的新外观。例如，当用户提供一段“某人挥手”的视频作为参考时，传统方法生成的视频不仅复现了挥手动作，还会不必要地保留原视频中的衣着、背景等外观特征，无法将挥手动作迁移到其他人物或场景中。

**核心洞察**：在隐空间中，运动主要影响帧序列之间的连通结构，而外观主要影响不同序列点集之间的距离。基于这一发现，MotionDirector提出通过双路径低秩适配（LoRA）架构，将外观学习与运动学习分离——空间LoRA仅从单帧学习外观，时间LoRA从多帧学习运动，并引入外观去偏时间损失以减少外观对时间训练任务的影响，最终实现运动与外观的解耦。

**方法定位**：MotionDirector属于基于预训练文本到视频扩散模型的参数高效微调方法，与**Tune-A-Video**（Wu et al., arXiv 2022）等单视频调谐方法以及**VideoComposer**（Wang et al., arXiv 2023）等可控生成方法形成互补关系。其独特之处在于首次将运动定制从外观定制中解耦出来，使学到的运动模式可以泛化到任意外观。

**主要结果**：
- 在UCF Sports Action多视频运动定制基准上，人类评估者对MotionDirector的运动保真度偏好率达75%以上，远超基础模型的25%。
- 在LOVEU-TGVE-2023单视频运动定制基准上，MotionDirector在外观多样性方面以72.83%的人类偏好率大幅领先VideoComposer（27.17%），同时在运动保真度方面以61.24%领先VideoComposer的38.76%。
- 与耦合的单路径LoRA训练相比，双路径架构显著提升了外观多样性（人类偏好54.84% vs 45.16%），且未损害运动保真度。



文本到视频（T2V）扩散模型近年来取得了显著进展，使得用户能够通过自然语言描述生成高质量的视频内容。然而，仅靠文本提示往往难以精确控制生成视频中的特定运动模式——例如“一个人以特定的步态从左走到右”或“相机以特定的弧线轨迹环绕主体”。这种对**运动概念的定制化需求**催生了一个新的研究问题：如何让预训练的T2V扩散模型学会参考视频中的特定运动，并将其泛化到任意新的外观上。

现有方法在解决这一问题时面临一个核心瓶颈：**运动与外观的耦合学习**。无论是整体微调（full fine-tuning）、参数高效调谐（parameter-efficient tuning），还是单路径低秩适配（LoRA），这些方法在从参考视频中学习运动时，往往同时将训练视频中有限的外观信息编码进模型参数。这导致学到的运动概念与特定外观强绑定——当用户尝试用新的文本描述或外观条件生成视频时，模型要么无法保留目标运动，要么会将训练视频的外观“泄漏”到生成结果中，严重限制了运动定制的泛化能力。

从任务定义来看（Figure 7），视频可以沿“外观”和“运动”两个轴进行定位。**外观定制**（如DreamBooth、Textual Inversion）旨在固定外观而泛化运动；**可控生成**（如VideoComposer、Control-A-Video）通过深度图、姿态等控制信号约束运动，但外观仍受限于文本描述。**运动定制**则提出了正交的需求：固定运动模式，泛化外观。这一任务在单参考视频和多参考视频两种设定下均有实际应用价值——前者要求从单个样本中提取运动概念，后者则利用多个共享相同运动但外观不同的视频进行更鲁棒的学习。

本文的核心动机在于：通过在隐空间中**解耦运动与外观的表示**，使运动学习不再受外观信息的干扰。具体而言，作者观察到在视频扩散模型的隐空间中，运动主要影响帧序列之间的连通结构（connectivity structure），而外观主要影响不同序列点集之间的距离（Figure 4）。基于这一洞察，MotionDirector提出了双路径LoRA架构和外观去偏时间损失，从模型架构和训练目标两个层面实现运动与外观的分离，从而使得定制后的运动可以泛化到任意外观——包括新的文本描述、其他视频的外观，甚至是单张静态图像。



## 核心方法与创新机理

MotionDirector 的核心创新在于**将运动定制从外观耦合中解耦出来**，使从参考视频中学到的运动模式能够泛化到全新的、多样化的外观上。这一目标的实现依赖于两个紧密配合的“changed slots”：**双路径低秩适配（LoRA）架构**与**外观去偏时间损失**。

### 双路径架构：外观与运动的分离学习

现有基于调谐的运动学习方法（如整体微调或单路径 LoRA）在从参考视频学习时，往往将运动与视频中有限的外观特征耦合在一起。当生成新视频时，学到的运动难以摆脱原始外观的“影子”，导致外观多样性丧失。

MotionDirector 通过一个双路径架构从根本上改变了这一学习范式（Figure 3）。该架构将训练过程分为两条并行的路径，分别对应外观和运动的学习：

- **空间路径（Spatial Path）**：仅注入可训练的**空间 LoRA** 到基础模型的空间 Transformer 的自注意力和前馈层中（刻意排除了交叉注意力层，以保持文本对齐能力）。该路径在每一步训练中仅从视频中**随机采样一帧**进行学习。由于单帧不包含任何时间信息，空间 LoRA 被迫专注于捕捉视频的静态视觉特征，即外观。
- **时间路径（Temporal Path）**：注入可训练的**时间 LoRA** 到时间 Transformer 的自注意力和前馈层中。同时，该路径中的空间 Transformer 会加载与空间路径**共享权重**的空间 LoRA。该路径从视频的**多帧**中学习。其设计逻辑是：共享的空间 LoRA 已经提供了外观信息，因此时间 LoRA 在训练时无需再为外观建模，可以专注于学习帧与帧之间的变化模式，即运动。

这种“分而治之”的架构是解耦的基础。在推理时，仅需将训练好的时间 LoRA 注入基础模型，即可驱动模型生成具有所学运动但外观完全由文本提示决定的新视频。

### 外观去偏时间损失：消除隐空间中的外观干扰

仅仅分离学习路径并不足以保证彻底解耦。作者在隐空间分析中发现（Figure 4），运动主要影响不同帧隐变量序列之间的**连通结构**，而外观则主要影响不同视频序列点集之间的**距离**。在标准的噪声预测损失下，外观差异会作为一种“偏差”干扰模型对运动连通结构的学习。

为此，MotionDirector 引入了一个**外观去偏时间损失（Appearance-debiased Temporal Loss）**。其核心操作是对噪声进行“去中心化”处理。对于一段视频的噪声序列，该操作将每一帧的噪声 $\epsilon_i$ 减去一个锚点噪声 $\epsilon_{anchor}$ 的缩放版本：

$$\phi(\epsilon_i) = \sqrt{\beta^2 + 1} \epsilon_i - \beta \epsilon_{anchor}$$

这一变换（Eq. 5）在数学上等价于将噪声点集平移，从而在保留帧间相对关系（即运动连通结构）的同时，消除了由外观引起的整体偏移。随后，模型在去偏后的噪声上计算预测损失（Eq. 6），并与原始时间损失结合，构成最终的时间训练目标（Eq. 7）。这使得时间 LoRA 的训练信号更加“纯净”，专注于运动本身。

### 创新总结

MotionDirector 通过上述两个“changed slots”，将运动学习任务从一个**耦合的、外观受限的拟合问题**转变为一个**解耦的、外观无关的概念学习问题**。双路径架构在模型结构层面提供了分离的可能性，而外观去偏时间损失则在优化目标层面强制实现了这种分离。二者的协同作用使得运动作为一种可泛化的“概念”被提取出来，这是该方法在运动保真度和外观多样性上同时取得显著提升的根本原因。



MotionDirector 的整体设计围绕一个核心目标展开：**将运动学习与外观学习解耦**，使定制后的运动能够泛化到任意外观。为此，该方法构建了一个双路径低秩适配（Dual-Path LoRA）架构，并辅以专门设计的外观去偏时间损失函数。

### 双路径架构

如图 3 所示，整个框架建立在冻结的预训练文本到视频扩散模型之上，通过向空间 Transformer 和时间 Transformer 分别注入可训练的 LoRA 权重来实现定制化学习。两条路径分工明确：

- **空间路径（Spatial Path）**：仅向空间 Transformer 的自注意力层和前馈层注入空间 LoRA，**刻意排除交叉注意力层**以保持文本对齐能力。该路径在每步训练中随机采样单帧进行学习，目标函数为单帧噪声预测损失（式(4)），从而专注于捕捉视频的外观特征。

- **时间路径（Temporal Path）**：在时间 Transformer 的自注意力和前馈层中注入时间 LoRA；同时，其空间 Transformer 共享空间路径中训练得到的空间 LoRA 权重。该路径以多帧作为输入，通过组合时间损失（式(7)）学习运动模式——共享的空间 LoRA 在此起到“外观锚定”作用，抑制外观信息对时间训练任务的干扰。

### 外观去偏时间损失

这是框架中关键的因果调节机制。标准的时间损失直接作用于所有帧的噪声预测，使得运动学习不可避免地耦合了外观信息。MotionDirector 引入去中心化操作 φ（式(5)）：将每帧噪声减去一个缩放后的锚点帧噪声，从而消除由外观引起的全局偏移，同时保留帧间连通结构所蕴含的运动信息（隐空间分析见 Figure 4）。外观去偏时间损失（式(6)）在去偏后的噪声上计算，与原始时间损失组合形成最终的时间训练目标（式(7)），迫使时间 LoRA 聚焦于运动一致性而非外观重建。

### 推理流程

训练完成后，推理阶段**仅注入时间 LoRA**（空间 LoRA 被丢弃）。给定任意的文本提示，预训练基础模型在时间 LoRA 的引导下生成具有所学运动模式但外观多样的视频。这种“训练时分离、推理时仅用运动模块”的设计，是实现运动泛化的关键——它确保定制运动不会与训练视频中的特定外观绑定。

### 模块关系总结

| 模块 | 训练时角色 | 推理时状态 |
|------|-----------|-----------|
| 空间 LoRA | 从单帧学习外观 | 丢弃 |
| 时间 LoRA | 从多帧学习运动（受外观去偏损失约束） | 注入基础模型 |
| 共享空间 LoRA | 在时间路径中提供外观锚定 | 随空间 LoRA 丢弃 |
| 外观去偏时间损失 | 消除外观对运动学习的偏差 | 不参与推理 |

该框架的灵活性还体现在：通过分别在不同视频上训练空间 LoRA 和时间 LoRA，可以实现**运动与外观的混合**——将来自视频 A 的运动与来自视频 B 的外观组合生成新视频。

### 补充图表

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/003_Figure_3.jpg]]
*Figure 3: The dual-path architecture of the proposed method. All pre-trained weights of the base diffusion model remain fixed. In the spatial path, the spatial transformers are injected with trainable spatial LoRAs as shown on the right side. In the temporal path, the spatial transformers are injected with spatial LoRAs sharing weights with those ones in the spatial path, and the temporal transformers are injected with trainable temporal LoRAs*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/009_Figure_7.jpg]]
*Figure 7: Each video is characterized by two aspects: appearance and motion. We can uniquely identify a video based on its values along the appearance and motion axes, as shown in the lowerleft corner of this figure. (a) Appearance customization aims to create videos whose appearances look like reference videos but have different motions. (b) The controllable generation aims to generate videos with the same motion represented by control signals. However, the control singles often have constraints on appearance, limiting the appearance diversity of the generated results. (c) Motion customization on a single video aims to generate videos with the specific motion learned from reference videos while keep...*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/001_Figure_1.jpg]]
*Figure 1: Motion customization of the text-to-video diffusion model*



MotionDirector 的核心设计围绕一个关键洞察展开：在视频扩散模型的隐空间中，运动主要影响帧序列之间的连通结构，而外观主要影响不同序列点集之间的距离（Figure 4）。基于此，方法通过双路径低秩适配（LoRA）架构与外观去偏时间损失，将外观学习与运动学习解耦。

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/004_Figure_4.jpg]]
*Figure 4: (a) Four example videos (the same as the videos in the first and fourth rows of Fig. 2) and their relationships in terms of motion and appearance. (b) We inverse the four videos based on the video diffusion model and visualize the denoising process. Each point corresponds to a latent code*

### 双路径 LoRA 架构

预训练视频扩散模型的所有权重保持冻结。方法注入两类 LoRA 模块：

**空间路径（Spatial Path）**：仅注入空间 LoRA 到空间 Transformer 的自注意力层和前馈层（不注入交叉注意力层，以保持文本对齐能力）。每训练步从参考视频中随机采样单帧，计算空间损失：

$$\mathcal{L}_{spatial} = \mathbb{E}_{z_0, y, \epsilon, t, i \sim \mathcal{U}(0, F)} \left[ \| \epsilon - \epsilon_{\theta} (z_{t,i}, t, \tau_{\theta}(y)) \|_2^2 \right] \quad \text{(Eq. 4)}$$

其中 $z_{t,i}$ 为第 $i$ 帧在时间步 $t$ 的加噪隐变量，$F$ 为总帧数。该路径仅学习视频的外观特征。

**时间路径（Temporal Path）**：空间 Transformer 注入与空间路径共享权重的空间 LoRA，时间 Transformer 的自注意力和前馈层注入可训练的时间 LoRA。训练时输入完整多帧视频，使时间 LoRA 专注于学习帧间运动模式。

### 外观去偏时间损失

标准噪声预测损失直接作用于所有帧时，外观信息会通过噪声分布干扰运动学习。为此，MotionDirector 引入去中心化操作 $\phi$：

$$\phi(\epsilon_i) = \sqrt{\beta^2 + 1} \epsilon_i - \beta \epsilon_{anchor} \quad \text{(Eq. 5)}$$

其中 $\epsilon_{anchor}$ 为锚点帧噪声（实验中采用随机锚点），$\beta$ 控制去偏强度。该操作将每帧噪声减去锚点噪声的缩放版本，消除外观偏差的同时保留帧间连通结构（Figure 4(d)）。

外观去偏时间损失定义为：

$$\mathcal{L}_{ad-temp} = \mathbb{E}_{z_0, y, \epsilon, t} \left[ || \phi(\epsilon) - \phi(\epsilon_{\theta}(z_t, t, \tau_{\theta}(y))) ||_2^2 \right] \quad \text{(Eq. 6)}$$

最终时间训练目标为原始时间损失与去偏损失的组合：

$$\mathcal{L}_{temporal} = \mathcal{L}_{org-temp} + \mathcal{L}_{ad-temp} \quad \text{(Eq. 7)}$$

### 推理阶段

推理时仅注入训练好的时间 LoRA（空间 LoRA 不参与），基础模型即可生成具有所学运动模式但外观多样化的视频。若需同时定制外观与运动，可额外注入空间 LoRA。

### 公式符号说明

| 符号 | 含义 |
|------|------|
| $z_0$ | 原始视频隐变量 |
| $z_t$ | 时间步 $t$ 的加噪隐变量，$z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$ |
| $\epsilon$ | 标准高斯噪声 |
| $\epsilon_\theta$ | 扩散模型预测的噪声 |
| $\tau_\theta(y)$ | 文本提示 $y$ 的嵌入 |
| $\phi(\cdot)$ | 外观去偏操作 |
| $\beta$ | 去偏强度系数 |

### 关键设计决策

1. **空间 LoRA 不注入交叉注意力层**：避免干扰文本-视觉对齐，确保运动定制后的视频仍能响应任意文本提示。
2. **时间路径共享空间 LoRA 权重**：使时间训练阶段能利用已学到的外观表征，减少外观对时间训练的干扰。
3. **锚点噪声的随机选择**：实验采用随机帧作为锚点，未引入额外计算开销；最优锚点策略仍为开放问题。



## 实验与关键发现

MotionDirector 在两类运动定制场景下进行了全面验证：**多视频运动定制**（从多个包含相同运动但外观不同的视频中学习运动概念）和**单视频运动定制**（从单个视频中提取特定主体的运动或相机运动）。评估维度覆盖自动指标与大规模人类评估，后者通过 Amazon MTurk 发布超过 1800 个比较任务，采用 3/5 共识机制，从文本对齐、时间一致性和运动保真度三个维度进行评判。

### 多视频运动定制：运动概念学习与泛化

在多视频场景下，核心目标是验证所学运动能否泛化到训练集之外的全新外观。实验使用 UCF Sports Action 等基准，从同一动作类别的多个视频中学习运动概念。

**人类偏好结果**显示，MotionDirector 的运动保真度获得了压倒性优势：在人类评估者对比中，MotionDirector 生成视频的运动保真度被偏好比例达到 **75% 以上**，而基础模型仅约 25%（见 4.1 节）。这一结果表明，双路径架构和外观去偏时间损失有效实现了运动与外观的解耦，使运动模式可以迁移到任意新外观上。

### 单视频运动定制：外观多样性与运动保真度

单视频场景更具挑战性——仅有一个参考视频，模型需在保留其运动特征的同时生成外观多样化的新视频。实验在 LOVEU-TGVE-2023 基准上进行，对比方法包括可控生成方法（**VideoComposer** (Wang et al., arXiv 2023)、Control-A-Video、VideoCrafter）、调谐方法（**Tune-A-Video** (Wu et al., arXiv 2022)）以及基础模型（ModelScope、ZeroScope）。

**与耦合调谐的消融对比**（Table 1）揭示了双路径架构的核心作用：单路径 LoRA（同时在空间和时间层上训练）将外观与运动耦合学习，导致外观多样性显著下降——人类评估者对外观多样性的偏好仅为 45.16%（vs ModelScope），而 MotionDirector 达到 **54.84%**，提升了 9.68 个百分点。关键的是，这一外观多样性的提升并未以牺牲运动保真度为代价，MotionDirector 同时保持了最高的运动保真度评分。

**与可控生成和调谐方法的全面对比**（Table 2）进一步验证了 MotionDirector 的显著优势。在外观多样性维度上，MotionDirector 以 **72.83%** 的人类偏好率大幅领先 VideoComposer 的 27.17%（差距达 45.66 个百分点）；对比 Control-A-Video（78.43% vs 21.57%）、VideoCrafter（71.11% vs 28.89%）和 Tune-A-Video（69.14% vs 30.86%）同样呈现碾压性优势。在运动保真度维度上，MotionDirector 对 VideoComposer 的偏好率为 **61.24%** vs 38.76%（差距 22.48 个百分点），对 Tune-A-Video 为 62.86% vs 37.14%。

这些结果表明，可控生成方法虽然可以通过控制信号（如深度图、姿态）约束运动，但往往以牺牲外观多样性为代价；而调谐方法则倾向于将运动与参考视频的外观过度绑定。MotionDirector 的双路径解耦策略从根本上解决了这一张力。

### 消融分析：双路径架构与外观去偏损失

消融实验的核心发现可归纳为两个因果机制：

1. **双路径 vs 单路径**：将空间 LoRA 与时间 LoRA 分离训练（而非在同一路径中联合优化）是外观多样性的关键保障。单路径耦合训练使时间 LoRA 在学习帧间运动时不可避免地捕获外观信息，导致生成结果的外观坍缩到参考视频的有限外观分布。双路径架构通过让空间 LoRA 仅从随机单帧学习外观，时间 LoRA 仅从多帧学习运动，从架构层面切断了两者的纠缠路径。

2. **外观去偏时间损失**：即使采用双路径架构，时间路径中的共享空间 LoRA 仍可能引入残留外观偏差。外观去偏时间损失通过去中心化噪声操作 $\phi(\epsilon_i) = \sqrt{\beta^2 + 1} \epsilon_i - \beta \epsilon_{anchor}$（Eq. 5）消除各帧噪声中的外观共模分量，使时间损失 $\mathcal{L}_{ad-temp}$（Eq. 6）更专注于帧间运动一致性而非外观一致性。实验表明，加入该损失后运动保真度进一步提升，且对外观多样性的保持有正向贡献。

### 定性结果分析

Figure 5 和 Figure 6 分别展示了多视频和单视频场景下的定性对比。在多视频场景中，MotionDirector 生成的视频在保持所学运动模式（如“挥杆”、“跳跃”等动作的时间动态）的同时，能够呈现与训练视频截然不同的背景、人物着装和光照条件。在单视频场景中，相比于 Tune-A-Video 和 VideoComposer 等方法，MotionDirector 在保持参考视频运动特征的前提下，生成了外观上显著更多样化的结果，避免了其他方法中常见的“外观复制”现象。

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison results of motion customization on multiple videos*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison results of motion customization on single videos*

### 公平性保障与实验配置

所有对比方法均使用官方实现或论文推荐配置，在相同硬件环境（NVIDIA A5000）下进行训练和推理。超参数在消融和对比中保持一致：LoRA rank=32，学习率=1e-4，dropout=0.1，训练步数根据视频长度统一设定。人类评估通过 Amazon MTurk 平台进行，每个比较任务由 5 名评估者独立完成，采用多数共识（至少 3/5 一致）作为最终判断，有效降低了主观偏差。

### 失败模式与局限性

尽管 MotionDirector 在运动定制任务上表现优异，实验中也暴露出若干边界条件：

- **多主体复杂运动**：当前方法主要针对单个主体或单一相机运动的定制。对于包含多个交互主体的场景（如群体运动、多人舞蹈），运动与外观的解耦难度显著增加，双路径架构的分离能力可能下降。这是论文明确指出的未探索方向。
- **锚点噪声选择**：外观去偏损失中的锚点噪声 $\epsilon_{anchor}$ 在实验中采用随机选择策略，未系统研究最优锚点策略。在极端外观干扰下（如参考视频外观高度一致时），去偏效果可能存在残留偏差。
- **数据需求**：运动概念的可靠学习目前需要多个参考视频（多视频场景）或至少一个包含清晰运动的视频（单视频场景），尚未扩展至纯文本描述驱动的运动定制。

### 补充图表

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/006_Table_1.jpg]]
*Table 1: Automatic and human evaluations results of motion customization on single videos*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/008_Table_2.jpg]]
*Table 2: Automatic and human evaluations results of motion customization on single videos*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/014_Figure_12.jpg]]
*Figure 12: Comparison of different methods on the task of motion customization given a single reference video*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/010_Figure_8.jpg]]
*Figure 8: Examples of two benchmarks for testing motion customization on multiple videos and a single video, respectively*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/011_Figure_9.jpg]]
*Figure 9: Example of one task for 5 human raters on Amazon MTurk to complete. Each task involves three questions comparing two generated results in terms of text alignment, temporal consistency, and motion fidelity*

![[assets/figures/papers/paper_list_l1058_https_arxiv_org_abs_2310_08465/figures/012_Figure.jpg]]
*Figure: Reference Videos: A person is skateboarding. Generated Results by MotionDirector*



## 定位与知识库关联

### 核心问题与因果机制

文本到视频扩散模型在定制特定运动时面临一个根本瓶颈：现有适配方法（整体微调、参数高效调谐、单路径LoRA）在从少量参考视频学习运动时，不可避免地将运动模式与训练视频中的有限外观耦合，导致学到的运动无法泛化到新的外观。MotionDirector的因果调节变量是通过**双路径低秩适配架构**将外观学习与运动学习在训练阶段分离：空间路径仅从单帧学习外观，时间路径从多帧学习运动，并引入**外观去偏时间损失**以减少外观对时间训练任务的干扰。

这一设计的核心洞察来源于对隐空间结构的分析：在视频扩散模型的隐空间中，运动主要影响帧序列之间的**连通结构**，而外观主要影响不同序列点集之间的**距离**（Figure 4）。通过分别用空间LoRA和时间LoRA建模这两类因素，并对外观偏差进行去中心化处理（Eq. 5-7），可以实现运动与外观的解耦，使运动定制的泛化成为可能。

### 与基线方法的关系

**单路径耦合调谐（Coupled tuning）** 是MotionDirector最直接的对比基线：在空间和时间Transformer层同时注入LoRA，使用标准噪声预测损失进行联合训练。Table 1的消融实验表明，耦合调谐虽然能保持较高的运动保真度，但严重损害了外观多样性——人类评估者对其外观多样性的偏好率仅为45.16%（vs ModelScope），而MotionDirector达到54.84%。这验证了双路径解耦的必要性：耦合训练使外观信息通过共享的LoRA权重泄漏到运动学习中。

在更广泛的视频生成方法谱系中，MotionDirector与三类方法形成对比：

- **可控视频生成方法**：**VideoComposer**（Wang et al., arXiv 2023）、**Control-A-Video**、**VideoCrafter**等依赖控制信号（如深度图、姿态、运动向量）来指定运动。这些方法需要额外的条件输入，且控制信号本身并不捕获参考视频中的细腻运动特征。Table 2显示，MotionDirector在运动保真度上以61.24%的人类偏好率显著优于VideoComposer的38.76%，在外观多样性上优势更为悬殊（72.83% vs 27.17%）。

- **单视频调谐方法**：**Tune-A-Video**（Wu et al., arXiv 2022）通过对单个视频的全参数或参数高效微调来生成变体，但其设计目标并非运动定制，而是保持原视频外观的同时进行有限编辑。Table 2中Tune-A-Video的外观多样性人类偏好率仅为30.86%，说明其难以将运动泛化到新外观。

- **预训练基础模型**：ModelScope和ZeroScope作为零样本基线，直接使用文本提示生成视频。它们虽能产生多样外观，但无法精确复现参考视频中的特定运动模式，运动保真度人类偏好率仅约25%。

### 方法适用边界

MotionDirector的当前设计存在明确的适用边界：

1. **运动复杂度限制**：方法主要针对**单个主体或单个相机运动**的定制（如特定人物的走路姿态、特定相机的运镜方式）。对于包含多个交互主体的复杂运动场景（如群体运动），解耦效果可能下降，因为不同主体的运动在隐空间中可能产生重叠的连通结构，仅靠外观去偏难以完全分离。

2. **数据需求**：运动概念的学习需要**多个参考视频**（用于学习可泛化的运动概念）或**单个视频**（用于学习特定实例的运动）。目前尚未扩展至文本描述驱动或零样本泛化的运动定制，即无法仅通过自然语言描述（如“从左走到右，再转身”）来指定运动模式。

3. **外观去偏的锚点依赖**：外观去偏时间损失中的锚点噪声选择（实验中采用随机锚点）直接影响去偏效果。在极端外观干扰下（如参考视频包含复杂纹理或动态背景），仍可能有残留的外观偏差。论文未系统研究最优锚点策略，这是方法鲁棒性的一个潜在薄弱点。

### 局限与开放问题

**已知局限**（论文明确讨论或实验揭示）：

- 对多主体、多运动交叠的复杂场景尚未探索，这是从单运动定制走向真实世界应用的关键障碍。
- 外观去偏效果依赖于锚点选择策略，当前随机锚点方案在极端条件下可能不足。
- 运动概念的学习依赖参考视频，缺乏文本驱动的运动指定能力。

**开放问题**（从方法设计和实验结果中自然延伸）：

1. **多主体运动解耦**：能否在隐空间中实现更细粒度的运动分离，例如通过解耦表示学习为不同主体分配独立的运动子空间，从而实现可控的多主体运动组合？

2. **运动强度的可控性**：当前方法学习的是二元运动概念（有/无该运动），能否扩展为学习连续的运动强度或运动风格参数，使用户可以调节运动幅度、速度等属性？

3. **文本驱动的运动定制**：是否可以通过自然语言描述直接指定运动模式，而无需提供参考视频？这需要建立文本-运动的对齐机制，或将运动概念编码为可与文本条件交互的表示。

4. **自适应锚点策略**：外观去偏时间损失中的锚点选择是否可以自适应，例如基于视频内容动态选择最具代表性的帧作为锚点，或学习一个可优化的锚点参数，以进一步降低对外观变化的敏感度？

5. **与外观定制方法的协同**：MotionDirector专注于运动定制，而已有工作（如DreamBooth、CustomDiffusion）专注于外观定制。两者是否可以组合，实现同时指定“谁”和“怎么做”的完全定制化视频生成？Figure 2 Row 3的初步实验表明这种混合是可行的，但系统性的联合训练框架仍有待探索。



## 原文 PDF

![[paperPDFs/arxiv_2023/MotionDirector_Motion_Customization_of_Text_to_Video_Diffusion_Models.pdf]]
