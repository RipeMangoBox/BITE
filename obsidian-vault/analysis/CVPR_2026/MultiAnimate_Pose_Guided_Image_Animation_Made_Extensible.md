---
title: "MultiAnimate: Pose-Guided Image Animation Made Extensible"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MultiAnimate_Pose_Guided_Image_Animation_Made_Extensible.pdf
project_link: "https://hyc001.github.io/MultiAnimate/"
code_link: null
aliases:
- MultiAnimate
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过Identifier Assigner和Identifier Adapter为每个角色分配独特的标识符，并在训练中随机采样标识符，使模型学习将角色与空间掩码而非固定通道关联，从而灵活推广到更多角色。
primary_logic: 随机标识符分配训练策略使所有标识符通道互异，模型学会泛化到任意数量的角色，无需为每个角色数量收集数据和重新训练。
claims:
- UniAnimate-DiT在扩展到两角色动画时失败，并且微调后无法泛化到不同数量的角色
- MultiAnimate在Swing Dance和Gen-dataset以及Unseen舞蹈视频上均取得最先进性能
- 掩码驱动设计（Identifier Assigner + Adapter）比加法驱动设计更能保持身份一致性和扩展到三角色
- Swing Dance (test) 上 PSNR↑ = 19.40 (Stage 1)
---

# MultiAnimate: Pose-Guided Image Animation Made Extensible

> [!tip] 核心洞察
> 随机标识符分配训练策略使所有标识符通道互异，模型学会泛化到任意数量的角色，无需为每个角色数量收集数据和重新训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | MultiAnimate：可扩展的姿态引导图像动画 |
| 英文题名 | MultiAnimate: Pose-Guided Image Animation Made Extensible |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21581) · [Project](https://hyc001.github.io/MultiAnimate/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | MultiAnimate |
| Dataset | Swing Dance, Gen-dataset, Unseen dance videos |

> [!tip] 效果简介
> - Swing Dance (test) 上，PSNR↑ 19.40 (Stage 1) vs 16.15 (UniAnimate-DiT) (+3.25)；FVD↓ 648.84 (Stage 1) vs 746.29 (DisPose) (-97.45)。
> - Gen-dataset (test) 上，FVD↓ 454.92 (Stage 1) vs 565.50 (UniAnimate-DiT) (-110.58)。
> - Unseen dance videos 上，FVD↓ 358.74 (Extended model) vs 624.45 (UniAnimate-DiT) (-265.71)。

## 概要

多角色姿态引导图像动画要求根据一张参考图像和驱动姿态序列，生成多个角色保持身份一致且动作协调的视频。然而，现有方法面临两个核心瓶颈：**身份混淆**与**可扩展性缺失**。简单地将单角色方法（如UniAnimate-DiT）扩展到多角色场景时，模型无法区分不同人物，导致身份错乱和不合理的遮挡（Figure 2）；同时，固定参与人数的训练范式使得模型无法泛化到训练时未见过的角色数量，每增加一种人数配置就需要重新收集数据并训练。

MultiAnimate 是首个基于现代 DiT 视频生成器的可扩展多角色图像动画框架。其核心思路是**通过随机标识符分配策略，让模型学习将角色与空间掩码而非固定通道关联**，从而在仅使用两角色数据训练的情况下，泛化到三人甚至更多人的动画生成（Figure 1）。这一能力源于两个关键设计：**Identifier Assigner** 将每人的跟踪掩码统一为标签映射并独热编码，显式保留空间关系；**Identifier Adapter** 则将标签映射转化为 DiT 特征空间中的标识符特征。训练时从 Identity Label Bank 中随机采样标识符，迫使所有标识符通道互异，使模型在推理时能灵活适应任意数量的角色。

在 Swing Dance、Gen-dataset 和未见舞蹈视频三个基准上，MultiAnimate 均取得最优性能：在 Swing Dance 上 PSNR 达到 19.40（相比 UniAnimate-DiT 提升 +3.25），在未见舞蹈视频上 FVD 降至 358.74（相比 UniAnimate-DiT 降低 265.71）。消融实验进一步证实，掩码驱动的标识符设计比加法驱动设计更能保持身份一致性，并成功扩展到三角色动画。

姿态引导的图像动画（Pose-Guided Image Animation）旨在从单张参考图像和一段驱动姿态序列生成目标视频，使参考人物按照驱动姿态运动，同时保持外观与身份的一致性。这一任务在虚拟主播、数字人、电影制作等领域具有广泛应用。近年来，基于扩散模型（Diffusion Models）的方法在单角色动画上取得了显著进展，代表性工作包括**MimicMotion**（Zhang et al., ICML 2025）、**DisPose**（Li et al., arXiv 2024）和**UniAnimate-DiT**（Wang et al., Sci. China Inf. Sci. 2025）等。

然而，当场景从单人扩展到多角色时，现有方法面临两个核心困境（Figure 2）：

1. **身份混淆**：将单角色方法直接扩展至多角色场景时，模型无法区分不同人物的外观特征，导致人物之间的外观混叠和不合理的遮挡关系。例如，UniAnimate-DiT在扩展到两角色动画时直接失败。
2. **可扩展性缺失**：即使对单角色方法进行微调使其适配固定人数（如两人），模型也无法泛化到训练时未见过的角色数量。这意味着每增加一种参与人数，就需要重新收集该人数的数据并重新训练模型，成本极高。

上述困境的深层原因在于，**相同的姿态序列在多角色场景中可能对应多种合理的运动轨迹**（Figure 3）。单角色方法仅依赖姿态信号驱动运动，缺乏对“谁是谁”的空间感知能力，因而无法消解这种运动歧义性。要解决这一问题，模型必须获得额外的空间线索——即每个角色的跟踪掩码（Tracking Mask），以明确各人物的空间归属和交互关系。

基于此，MultiAnimate 提出了两个关键设计目标：
- **多角色身份一致性**：在复杂交互场景下保持每个角色的外观和身份不混淆；
- **可扩展性**：模型在仅使用两角色数据训练后，能够泛化到任意数量的角色，无需为不同人数重新训练。

## 核心方法与创新机理

MultiAnimate 的核心创新在于将多角色图像动画从一个**固定人数、通道绑定的生成任务**重新定义为一个**掩码驱动、可扩展的身份建模问题**。其关键洞察是：现有方法之所以在多角色场景下出现身份混淆和泛化失败，根源不在于生成模型的容量不足，而在于**身份信息的注入方式缺乏空间显式性和分配灵活性**。

### 瓶颈定位：从通道绑定到空间掩码

单角色动画方法（如 **UniAnimate-DiT** (Wang et al., Sci. China Inf. Sci. 2025)）在扩展到两角色时面临双重困境（Figure 2）：直接推理时产生严重的身份混淆和不合理遮挡；即使针对两人场景微调，模型也无法泛化到未见过的角色数量。这一瓶颈的因果机制在于：这些方法将不同人物的身份信息隐式地编码在固定的特征通道中，导致模型将“人物A”与“某个特定通道”强绑定，而非学习到“人物”与“空间位置”之间的对应关系。

MultiAnimate 通过两个关键模块改变了这一因果结构：

- **Identifier Assigner**：将每人的跟踪掩码统一为一幅标签映射 $\mathcal{L} \in \{0, a, b\}^{H \times W}$，再通过独热编码生成 $\hat{\mathcal{L}} \in \{0, 1\}^{3 \times H \times W}$ 的二进制张量。这一操作将身份信息从“通道维度”转移到“空间维度”，显式保留了人物之间的空间关系和交互结构。

- **Identifier Adapter**：通过堆叠的 3D 卷积层将标签映射转化为 DiT 特征空间中的标识符特征，使模型能够在生成过程中持续感知每人的空间边界和相对位置。

这一设计带来的因果效应在消融实验中得到了验证（Figure 8, Figure 9）：加法驱动设计（如 **DanceTogether** (Chen et al., 2025) 中直接求和每人姿态和掩码特征的方式）虽然能处理两角色，但在增加角色时性能崩溃，出现背景噪声和身份混淆；而掩码驱动设计不仅保持了两角色的身份一致性，还能平滑扩展到三角色动画。

### 可扩展性机制：随机标识符分配训练

仅靠空间掩码还不足以解决泛化问题。当推理时的人物标签分配与训练时不一致时，模型仍会产生身份不一致（Figure 5）。MultiAnimate 的第二个关键创新是**随机标识符分配训练策略**：

- 构建一个大小为 $n$ 的 Identity Label Bank，在每次训练迭代中随机为两个角色分配标识符，并激活 Identity Weight Bank 中对应的权重通道。
- 这一策略确保所有 $n$ 个标识符通道在训练中都被充分访问且互异，模型被迫学习“任意标识符与空间掩码的对应关系”，而非“特定标识符与特定通道的固定绑定”。

因果效应直接体现在可扩展性上：仅使用两角色数据训练的模型，在推理时可以直接泛化到三人甚至七人场景（Figure 1），无需为每个角色数量收集数据和重新训练。这本质上是一种**组合泛化**——模型学会了将“身份标识”作为一个可插拔的变量，而非固定的网络结构参数。

### 双流架构中的创新嵌入

上述创新通过双流架构实现（Figure 4）：Reference Stream 编码参考图像和参考姿态以捕获外观信息，Motion Stream 编码目标姿态序列和跟踪掩码以建模运动和空间条件。Identifier Assigner 和 Identifier Adapter 嵌入在 Motion Stream 中，将空间身份信息注入 DiT 的特征空间，与姿态特征协同指导生成过程。两流通过元素级加法融合，保持了与单角色方法的架构兼容性（Figure 10, Table 2）。

MultiAnimate 是一个基于现代 DiT 视频生成器的多角色图像动画框架，其核心设计目标是解决现有多角色动画中身份混淆与可扩展性不足的问题。框架的整体 pipeline 由两条并行的处理流构成：**参考流（Reference Stream）** 和 **运动流（Motion Stream）**，两条流通过逐元素相加的方式进行特征融合。

### 输入定义

给定一张参考图像 $I_{\mathrm{ref}} \in \mathbb{R}^{3 \times H \times W}$、一段驱动姿态序列 $P \in \mathbb{R}^{T \times 3 \times \breve{H} \times W}$ 以及每个角色的跟踪掩码 $\{M_i\}_{i=1}^n$（其中 $M_i \in \mathbb{R}^{T \times 1 \times H \times W}$），框架的目标是生成与姿态序列对应且保持各角色身份一致的目标视频 $V_{\mathrm{tar}} \in \mathbb{R}^{T \times 3 \times H \times W}$。

### 参考流

参考流负责编码参考图像的外观信息。首先通过 **VAE Encoder** 将参考图像编码为潜空间表示，同时由 **Image Encoder**（堆叠的 2D 卷积层）处理参考姿态。编码后的外观特征与噪声拼接后经 patchify 操作转化为 DiT 可处理的 token 序列。

### 运动流

运动流负责编码多角色姿态序列和空间条件。**Pose Encoder**（3D 卷积编码器）从目标姿态序列中提取运动动力学特征。与此同时，**Identifier Assigner** 和 **Identifier Adapter** 联合处理跟踪掩码，为每个角色生成独特的身份标识特征：

- **Identifier Assigner**：将每个角色的跟踪掩码统一为一幅标签映射 $\mathcal{L} \in \{0, a, b\}^{H \times W}$（以两角色为例，背景为 0，角色 A、B 分别为不同的非零标识符），随后进行独热编码，生成三通道的二进制张量 $\hat{\mathcal{L}} \in \{0, 1\}^{3 \times H \times W}$，显式保留各角色的空间关系。
- **Identifier Adapter**：通过堆叠的 3D 卷积层将独热编码后的标签映射转化为 DiT 特征空间中的标识符特征，从而在特征层面建模角色间的空间交互。

运动流生成的运动与空间条件特征最终与参考流的 token 通过逐元素相加进行融合，送入 DiT 主干网络进行去噪生成。

### 训练策略：随机标识符分配

为确保框架能够泛化到训练时未见过的角色数量，MultiAnimate 引入了随机标识符分配训练策略。训练时，每个迭代从大小为 $n$ 的 **Identity Label Bank** 中随机为两个角色分配标识符标签，并激活 **Identity Weight Bank** 中对应的权重通道。这迫使所有 $n$ 个通道在训练过程中互异，使模型学会将角色身份与空间掩码而非固定通道绑定。推理时，即使面对超过训练时角色数量的场景，模型也能通过未使用过的通道正确区分各角色。这一机制是框架仅用两角色数据训练即可扩展到三角色甚至七角色场景（Figure 1）的关键所在。

![[assets/figures/papers/paper_list_l1074_https_arxiv_org_abs_2602_21581/figures/001_Figure_1.jpg]]
*Figure 1: Multi-character pose-guided image animation generated by our framework. Our method performs multi-character image animation with consistent identity and appearance for each character. Notably, our framework, trained only on two-character data, is capable of producing identity-consistent three-person videos and can, in principle, be extended to scenarios with even more participants (e.g., seven characters)*

### 与基线方法的根本差异

与简单的“加法驱动”设计（如 **DanceTogether** (Chen et al., 2025) 直接将每人的姿态和掩码特征求和）相比，MultiAnimate 的掩码驱动设计通过 Identifier Assigner 和 Identifier Adapter 显式建模每个角色的空间组织关系。消融实验表明，加法驱动设计在角色数量增加时会出现背景噪声和身份混淆，而掩码驱动设计能够保持清晰的角色空间布局，并具备更强的可扩展性（Figure 8, Figure 9）。

### 问题形式化

MultiAnimate 的形式化输入包括参考图像 $I_{\mathrm{ref}} \in \mathbb{R}^{3 \times H \times W}$、驱动姿态序列 $P \in \mathbb{R}^{T \times 3 \times \breve{H} \times W}$、以及每人的跟踪掩码 $\{M_i\}_{i=1}^n$，其中 $M_i \in \mathbb{R}^{T \times 1 \times H \times W}$。目标是生成包含 $n$ 个角色的目标视频 $V_{\mathrm{tar}} \in \mathbb{R}^{T \times 3 \times H \times W}$，且各角色身份与外观保持一致。

这一设定直接暴露了多角色动画的核心矛盾：相同的姿态序列可能对应多种不同的运动轨迹分配（Figure 3）。因此，仅靠姿态信息无法消除角色间的运动歧义，必须引入空间标识机制来绑定每个角色与其对应的运动路径。

### 双流架构与融合策略

框架由两条并行的处理流构成（Figure 4）：

**Reference Stream（参考流）** 负责编码外观信息。参考图像经 VAE Encoder 映射到潜空间，参考姿态通过 2D 卷积 Image Encoder 提取结构特征，两者与噪声拼接后进行 patchify 操作，生成外观感知的 latent tokens。

**Motion Stream（运动流）** 负责编码运动与空间条件。多角色目标姿态序列由 3D 卷积 Pose Encoder 提取时序运动动力学特征，同时跟踪掩码经 Identifier Assigner 和 Identifier Adapter 转化为身份标识特征。两条流的 latent tokens 通过 **逐元素相加**（element-wise addition）进行融合，送入 DiT backbone 进行去噪生成。

### Identifier Assigner：从掩码到空间标签

Identifier Assigner 解决的核心问题是：如何将 $n$ 个独立的二值跟踪掩码 $\{M_i\}_{i=1}^n$ 统一为一幅保留空间关系的结构化表示。

对于两角色场景，Assigner 将所有掩码合并为一幅标签图 $\mathcal{L} \in \{0, a, b\}^{H \times W}$，其中 0 表示背景，$a$ 和 $b$ 分别为角色 A 和 B 的非零标识符。随后对 $\mathcal{L}$ 进行独热编码，生成三通道二进制张量 $\hat{\mathcal{L}} \in \{0, 1\}^{3 \times H \times W}$，分别对应背景、角色 A 和角色 B 的空间占据区域。

这一设计的因果机制在于：通过独热编码将“谁在哪里”的空间信息显式注入特征空间，使模型能够区分不同角色的空间布局，而非像加法驱动设计那样将多角色信息简单求和后丢失个体边界（消融实验 Figure 8 证实加法驱动仅能处理两角色，扩展到更多角色时出现背景噪声和身份混淆）。

### Identifier Adapter：空间标签到 DiT 特征空间

Identifier Adapter 将 Assigner 输出的独热标签图转化为 DiT backbone 可消费的特征表示。其结构为堆叠的 3D 卷积层，对标签图进行时空建模，输出与 DiT 特征空间对齐的标识符特征。这一模块的核心价值在于建模角色间的交互关系——3D 卷积的感受野能够捕获相邻角色在空间和时间维度上的共现模式，从而在生成过程中维持角色间的合理遮挡和空间一致性。

消融实验（Figure 9）表明，Identifier Assigner 与 Identifier Adapter 的结合使用显著提升了身份一致性，并使得框架能够扩展到三角色动画场景，而单独使用任一组件的效果均不及二者协同。

![[assets/figures/papers/paper_list_l1074_https_arxiv_org_abs_2602_21581/figures/010_Figure_9.jpg]]
*Figure 9: Ablation on Identifier Assigner & Identifier Adapter. The combination of Identifier Assigner and Identifier Adapter improves identity consistency and enhances the framework’s extensibility, enabling three-characters image animation*

### 随机标识符分配与可扩展性训练

框架的可扩展性来源于训练阶段的随机标识符分配策略。具体而言，系统维护一个大小为 $n$ 的 Identity Label Bank 和对应的 $n$ 通道 Identity Weight Bank。每次训练迭代中，从 Label Bank 中随机为两个角色分配标识符，并激活 Weight Bank 中对应的权重通道参与前向传播。

这一策略的因果机制是：所有 $n$ 个通道在训练过程中均被充分激活并学习到互异的表示，模型学会将角色身份与标识符通道而非固定的空间位置绑定。因此，推理时只需从 Weight Bank 中选取任意未使用的通道分配给新增角色，即可泛化到训练时未见过的角色数量。Figure 1 展示了仅用两角色数据训练即可泛化到三人甚至七人场景的效果，Figure 5 则揭示了若不采用随机分配、推理时标签与训练时不一致会导致身份错乱的失败模式。

![[assets/figures/papers/paper_list_l1074_https_arxiv_org_abs_2602_21581/figures/005_Figure_5.jpg]]
*Figure 5: Our framework performs well at early training stages, but inconsistencies emerge when the person-assigned labels at inference differ from those seen during training*

## 实验与关键发现

### 主实验结果与定量分析

MultiAnimate 在三个不同来源的测试基准上均取得了最优性能，验证了其多角色动画的质量与泛化能力。Table 1 汇总了与 MimicMotion (Zhang et al., ICML 2025)、DisPose (Li et al., arXiv 2024)、UniAnimate-DiT (Wang et al., Sci. China Inf. Sci. 2025) 及 VACE (Jiang et al., ICCV 2025) 的定量对比。

![[assets/figures/papers/paper_list_l1074_https_arxiv_org_abs_2602_21581/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison with other SOTA methods on the test split of Swing Dance,Gen-dataset and Unseen dance videos*

在 Swing Dance 测试集上，MultiAnimate 的 Stage 1 模型取得了 **19.40 dB 的 PSNR**，较 UniAnimate-DiT 的 16.15 dB 提升 3.25 dB；FVD 降至 **648.84**，优于 DisPose 的 746.29。在 Gen-dataset 上，FVD 进一步降至 **454.92**，相比 UniAnimate-DiT 的 565.50 降低了 110.58，表明模型对分布外运动模式具有鲁棒的迁移能力。在未见舞蹈视频上的优势最为显著：扩展模型（Extended model）的 FVD 仅为 **358.74**，而 UniAnimate-DiT 为 624.45，降幅达 265.71。这组数据直接支撑了核心主张——随机标识符分配训练策略使模型学会了将角色与空间掩码而非固定通道关联，从而在推理时无需微调即可泛化到训练中未见过的角色数量。

值得注意的是，Gen-dataset 的结果是在未额外训练的条件下取得的，这进一步验证了框架的零样本迁移特性。

### 定性分析

Figure 6 的定性对比显示，MultiAnimate 在 Swing Dance 数据集上生成的视频保持了每个角色一致的身份外观和清晰的空间关系。相比之下，其他方法在复杂交互场景中容易出现身份混淆或背景噪声。Figure 7 展示了在 Gen-dataset 上微调的效果：模型能够更好地维持时序一致性，并在武器持有等复杂运动-场景交互中保持物体的完整性。

![[assets/figures/papers/paper_list_l1074_https_arxiv_org_abs_2602_21581/figures/008_Figure_7.jpg]]
*Figure 7: Training on the Gen-dataset enhances the model’s ability to maintain temporal consistency and adapt to diverse motion–scene interaction*

### 消融实验

消融实验围绕两个关键设计展开：掩码驱动（mask-driven）的标识机制与加法驱动（addition-driven）的对比，以及 Identifier Assigner 与 Identifier Adapter 的组件贡献。

**加法驱动 vs. 掩码驱动。** Figure 8 对比了加法驱动设计（如 DanceTogether, Chen et al., 2025）与 MultiAnimate 的掩码驱动设计。加法驱动在两角色场景下可以工作，但当角色数量增加时性能急剧崩溃，出现背景噪声和严重的身份混淆。这验证了直接求和每人姿态和掩码特征的方式无法保留清晰的空间组织关系。MultiAnimate 的掩码驱动设计则通过标签映射和独热编码显式建模每人的空间区域，保持了清晰的空间组织，从而具备更强的可扩展性。

**Identifier Assigner 与 Identifier Adapter 的组件贡献。** Figure 9 的消融表明，Identifier Assigner 与 Identifier Adapter 的组合使用是提升身份一致性和扩展性的关键。仅使用其中之一时，模型在三角色动画场景下会出现身份漂移或空间混乱；两者联合使用时，模型能够成功扩展到三角色动画，且每个角色的外观保持稳定。

**单角色兼容性。** 尽管 MultiAnimate 为多角色场景引入了额外的训练复杂度（Identifier Assigner 和 Adapter），但框架仍保持与单角色动画方法的兼容性。Figure 10 和 Table 2 显示，在 TikTok 数据集上的单角色动画任务中，MultiAnimate 的性能与专注单角色的方法保持可比，未因多角色设计而退化。

### 关键图表结论

- **Table 1**：MultiAnimate 在 Swing Dance、Gen-dataset 和 Unseen dance videos 三个基准上全面超越现有方法，FVD 降幅最高达 265.71，验证了可扩展性设计的有效性。
- **Figure 8**：加法驱动设计无法泛化到三角色场景，掩码驱动是保证空间组织和可扩展性的必要条件。
- **Figure 9**：Identifier Assigner 与 Identifier Adapter 的组合是实现身份一致性和三角色扩展的充分条件，单独使用任一组件的效果有限。
- **Figure 10 / Table 2**：多角色设计未损害单角色性能，框架具有良好的向下兼容性。

![[assets/figures/papers/paper_list_l1074_https_arxiv_org_abs_2602_21581/figures/012_Table_2.jpg]]
*Table 2: Quantitative results on TikTok dataset. Our approach maintains comparable performance to other models which target at single character animation*

## 定位与知识库关联

### 任务定位与核心突破

MultiAnimate 解决的是**多角色姿态引导图像动画**（multi-character pose-guided image animation）问题：给定一张包含多人的参考图像、一段驱动姿态序列以及每人的跟踪掩码，生成一段保持身份一致性的目标视频。该任务的形式化定义为：

$$I_{\mathrm{ref}} \in \mathbb{R}^{3 \times H \times W}, P \in \mathbb{R}^{T \times 3 \times \breve{H} \times W}, \{M_i\}_{i=1}^n, M_i \in \mathbb{R}^{T \times 1 \times H \times W}, V_{\mathrm{tar}} \in \mathbb{R}^{T \times 3 \times H \times W}$$

其中 $I_{\mathrm{ref}}$ 为参考图像，$P$ 为驱动姿态序列，$\{M_i\}$ 为每人的跟踪掩码，$V_{\mathrm{tar}}$ 为生成的目标视频。该任务的核心难点在于：多角色场景下，相同的姿态序列可能导致多种合理的运动轨迹（Figure 3），模型必须同时理解空间位置关系与身份归属。

### 与现有方法的关系

**单角色动画方法的直接扩展失败。** 现有基于扩散变换器（DiT）的单角色动画方法，如 **UniAnimate-DiT**（Wang et al., Sci. China Inf. Sci. 2025），在直接扩展到两角色场景时会出现严重的身份混淆和不合理遮挡（Figure 2a）。即使对 UniAnimate-DiT 进行微调使其适配两角色数据，微调后的模型也无法泛化到训练时未见过的角色数量（Figure 2b）。这揭示了单角色方法的根本瓶颈：它们缺乏对多角色空间关系的显式建模能力。

**加法驱动多角色设计的局限性。** 另一条技术路线是将每人的姿态特征和掩码特征直接求和后送入模型——这种“加法驱动”（addition-driven）设计以 **DanceTogether**（Chen et al., 2025）为代表。消融实验表明，加法驱动设计在两角色场景下可以工作，但当角色数量增加时性能急剧崩溃，出现背景噪声和身份混淆（Figure 8）。其深层原因在于：简单的特征求和无法保留角色间的空间组织结构，模型难以区分不同角色的特征归属。

**MultiAnimate 的差异化设计。** MultiAnimate 提出了**掩码驱动**（mask-driven）的替代方案，其核心创新在于两个模块的协同设计：

1. **Identifier Assigner**：将每人的跟踪掩码统一为一幅标签图 $\mathcal{L} \in \{0, a, b\}^{H \times W}$，其中背景为 0，人物 A、B 分别为不同的非零标识符 $a$、$b$。随后对该标签图进行独热编码，生成 $\hat{\mathcal{L}} \in \{0, 1\}^{3 \times H \times W}$ 的二进制张量。这种设计将多角色空间关系显式地编码为结构化的空间表示，而非简单的通道求和。

2. **Identifier Adapter**：通过堆叠的 3D 卷积层将独热编码的标签映射转化为 DiT 特征空间中的标识符特征，使模型能够在特征层面建模人物间的交互关系。

与加法驱动设计相比，掩码驱动设计保留了清晰的逐角色空间组织结构，在多角色场景中展现出更强的可扩展性（Figure 9）。

### 可扩展性的因果机制

MultiAnimate 的可扩展性并非来自网络结构的特殊设计，而是源于**训练策略的根本性改变**。具体而言，模型维护一个大小为 $n$ 的 Identity Label Bank 和对应的 Identifier Weight Bank。在每次训练迭代中，从 Identity Label Bank 中随机为两个角色分配标识符，并激活 Identifier Weight Bank 中对应的权重通道。这使得所有 $n$ 个通道在训练过程中都被充分激活，且彼此互异。

这一训练策略的因果逻辑在于：模型学会将角色身份与**空间掩码**而非**固定通道索引**关联。当推理时出现训练未见过的角色数量（如三人或七人），模型只需从 Identifier Weight Bank 中激活对应数量的通道即可，无需重新训练。Figure 1 展示了两角色训练模型直接泛化到三角色甚至七角色场景的能力，验证了这一机制的有效性。

### 适用边界与局限

**训练数据规模约束。** MultiAnimate 的训练仅使用两角色数据，通过随机标识符分配策略实现泛化。这意味着模型对多角色交互的理解完全来自两角色样本的统计模式。当推理场景中的角色数量远超训练分布（如七人密集交互）时，模型可能缺乏对复杂遮挡和多人空间关系的充分建模能力——尽管 Figure 1 展示了初步的泛化效果，但该方向的定量评估尚不充分。

**单角色兼容性的代价。** 尽管 MultiAnimate 在单角色动画场景下仍保持与专用方法可比拟的性能（Table 2, TikTok 数据集），但多角色设计的引入增加了训练复杂度（Figure 10）。在仅需处理单角色的应用场景中，直接使用 **MimicMotion**（Zhang et al., ICML 2025）或 **DisPose**（Li et al., arXiv 2024）等专用方法可能更具效率优势。

**掩码依赖性。** MultiAnimate 的性能高度依赖于跟踪掩码的质量。在真实场景中，自动多人跟踪算法可能产生不准确的掩码，这将成为整个 pipeline 的性能瓶颈。论文未讨论掩码质量下降时的鲁棒性表现，这一点需要在实际部署中手动验证。

### 开放问题

1. **角色数量的理论上限。** Identifier Weight Bank 的通道数 $n$ 决定了可支持的最大角色数量。论文未探讨 $n$ 的扩展对训练稳定性和模型容量的影响，也未给出 $n$ 的合理选择范围。当 $n$ 增大时，随机采样策略可能导致某些通道训练不充分，进而影响对应角色的生成质量。

2. **角色外观的细粒度控制。** 当前框架通过参考图像隐式提供外观信息，但缺乏对角色外观属性的显式解耦控制（如服装颜色、发型等）。在多角色场景中，用户可能希望独立编辑某一角色的外观而不影响其他角色，这要求更细粒度的外观解耦机制。

3. **与视频编辑方法的融合潜力。** **VACE**（Jiang et al., ICCV 2025）等视频创建和编辑方法提供了对生成内容的精细控制能力。MultiAnimate 的掩码驱动设计天然提供了逐角色的空间控制接口，与视频编辑方法的结合可能实现更灵活的多角色内容创作流程，这一方向尚待探索。

4. **跨域泛化能力。** 当前实验主要在舞蹈场景（Swing Dance）和通用人物场景（Gen-dataset）上进行。模型在更复杂的交互场景（如体育竞技、多人对话）中的泛化能力尚未验证。这些场景中的人物姿态和空间关系模式与舞蹈有显著差异，可能需要额外的域适应策略。

## 原文 PDF

![[paperPDFs/CVPR_2026/MultiAnimate_Pose_Guided_Image_Animation_Made_Extensible.pdf]]
