---
title: MTVCrafter 4D Motion Tokenization for Open World Human Image Animation
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation.pdf
project_link: null
code_link: https://github.com/DINGYANB/MTVCrafter
aliases:
- M4MTOWHIA
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 直接用4D运动标记（量化的SMPL差分关节坐标）取代2D渲染姿态图像作为条件，解耦运动与形状/位置，并通过4D运动注意力注入扩散模型。
primary_logic: 将运动编码为离散的差分关节坐标标记，结合4D旋转位置编码（RoPE）的运动注意力，使模型能够学习稳健的时空运动语义，实现开放世界中的零样本泛化。
claims:
- 不使用量化时，VQ-VAE退化为标准自编码器，产生连续标记，导致性能下降（FVD从317.21升至332.97）。
- 完全移除4D位置编码（PE）导致FVD从317.21飙升至548.31，证明明确的4D位置信息不可或缺。
- MTVCraft-18B在TikTok基准上达到FVD 276.65，比最强的基线Unianimate-DiT (402.14) 降低31.2%。
- 在Fashion基准上，MTVCraft-18B同样取得最佳FVD 64.88，较Unianimate-DiT (88.36) 降低26.6%。
---

# MTVCrafter 4D Motion Tokenization for Open World Human Image Animation

> [!tip] 核心洞察
> 将运动编码为离散的差分关节坐标标记，结合4D旋转位置编码（RoPE）的运动注意力，使模型能够学习稳健的时空运动语义，实现开放世界中的零样本泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | MTVCrafter：面向开放世界人物图像动画的4D运动标记化 |
| 英文题名 | MTVCrafter 4D Motion Tokenization for Open World Human Image Animation |
| 会议/期刊 | arXiv 2025 |
| Links | [Code](https://github.com/DINGYANB/MTVCrafter) · [paper](https://arxiv.org/abs/2505.10238) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MTVCraft |
| Dataset | TikTok, Fashion |

> [!tip] 效果简介
> - TikTok 上，FVD 276.65 (MTVCraft-18B) vs 402.14 (Unianimate-DiT) (-125.49 (31.2%))；FID-VID 7.31 (MTVCraft-18B) vs 9.12 (Unianimate-DiT) (-1.81 (19.9%))。
> - Fashion 上，FVD 64.88 (MTVCraft-18B) vs 88.36 (Unianimate-DiT) (-23.48 (26.6%))；FID-VID 4.41 (MTVCraft-18B) vs 6.12 (Unianimate-DiT) (-1.71 (27.9%))。

## 概要

人物图像动画任务旨在将驱动视频中的运动迁移至给定的参考人物图像，生成具有一致身份和准确运动的视频。现有方法普遍依赖2D渲染的姿态图像（如DWPose骨架、SMPL渲染图或深度图）作为运动条件，这类表示仅提供有限的结构线索，丢弃了丰富的4D时空信息，导致在复杂运动下产生扭曲或伪影。MTVCraft提出了一种全新的范式：**直接对原始SMPL关节坐标序列进行4D运动标记化**，将运动编码为离散的差分关节坐标标记，从而解耦运动与绝对位置、形状变化。

核心思路包含两个关键组件：（1）**4DMoT（4D运动标记器）**，通过VQ-VAE框架将SMPL序列量化为紧凑的4D运动标记；（2）**MV-DiT（运动感知视频DiT）**，在扩散模型中插入4D运动注意力层，以视觉标记为查询、运动标记为键值，并应用4D旋转位置编码（RoPE）强化时空交互。身份保持则采用简洁的逐帧重复拼接策略，无需独立的参考网络。

在TikTok和Fashion两个标准基准上，MTVCraft-18B均取得最优结果：**TikTok FVD为276.65，较最强基线Unianimate-DiT（402.14）降低31.2%**；**Fashion FVD为64.88，较Unianimate-DiT（88.36）降低26.6%**。消融实验证实，离散量化、差分运动表示、4D RoPE等设计均对性能有显著贡献——移除4D位置编码后FVD从317.21飙升至548.31，移除量化后FVD升至332.97。此外，该方法展现出强大的零样本泛化能力，可处理全身/半身人物、动漫、像素艺术、水墨等多种风格，甚至扩展至动物和非生命体。

MTVCraft将运动条件从2D渲染图像推进到4D离散标记，为开放世界人物动画提供了一种更稳健、更具表达力的技术路径。



### 问题背景

人物图像动画（Human Image Animation）旨在根据给定的参考人物图像和驱动运动序列，生成一段保持人物身份一致、且准确复现目标运动的视频。这项技术在虚拟数字人、影视制作、社交媒体内容生成等领域具有广泛的应用前景。一个核心挑战在于：如何从驱动视频中提取运动信号，并将该信号有效地注入生成模型，使得生成的人物既能忠实跟随目标姿态，又能保持外观细节不丢失。

### 现有方法的瓶颈

当前主流方法普遍采用**2D渲染的姿态图像**作为运动条件。具体而言，这些方法先从驱动视频中估计出3D人体参数模型（如SMPL）的关节序列，再将3D姿态渲染为2D图像——例如DWPose骨架图、SMPL渲染图或深度图——最后将这些渲染图像作为条件输入扩散模型（Figure 2(a)）。这一范式存在根本性缺陷：

1. **信息损失严重**：将4D时空运动（3D关节坐标随时间变化）投影为2D渲染图像，不可避免地丢弃了深度信息、关节间精确的时空依赖关系，以及运动本身的语义结构。
2. **形状与位置偏差**：2D渲染图像天然耦合了人体的形状和绝对位置信息，导致模型容易过拟合到训练数据中特定人物的体型和画面构图，削弱了对新人物、新场景的泛化能力。
3. **复杂运动下的伪影**：当驱动视频包含大幅度旋转、遮挡或快速动作时，2D姿态图像的有限结构线索无法提供足够的时空约束，生成结果容易出现扭曲、抖动或身份漂移。

从定量结果来看，这一瓶颈的严重性在TikTok基准上表现得尤为突出：最强的2D姿态条件基线**Unianimate-DiT**的FVD高达402.14，而人类视觉对运动伪影的敏感度意味着这一指标仍有极大的改善空间（Table 1）。

### 本文动机

本文的核心动机在于**绕过2D渲染姿态图像这一信息瓶颈，直接对原始4D运动进行标记化建模**。直觉上，SMPL关节坐标序列本身就是一种紧凑、精确的运动表示，包含了完整的时空运动语义。如果能将其量化为离散标记（token），并设计相应的注意力机制将其注入视频扩散模型，就有望从根本上解决信息损失问题。

这一思路面临两个关键技术挑战：

- **如何将连续的SMPL关节序列编码为紧凑且富有表现力的离散标记？** 需要一种运动标记器（Motion Tokenizer），既能解耦运动与绝对位置、形状，又能通过量化抑制噪声、捕获高层运动语义。
- **如何让视频DiT模型有效地利用这些4D运动标记？** 需要设计一种运动感知的注意力机制，使视觉标记（video tokens）能够以时空一致的方式查询运动标记中的姿态信息。

Figure 2(b) 直观对比了两种范式：传统方法将3D运动渲染为2D图像再输入模型，而MTVCraft直接将4D运动标记作为条件，保留了完整的时空运动信息。这一设计使得模型能够学习到更稳健的运动-视觉对应关系，从而在开放世界中实现零样本泛化——包括任意视觉风格（动漫、像素画、水墨、写实）、任意人物类型（全身、半身），甚至非人角色（动物、无生命物体），如Figure 1所示。



## 核心方法与创新机理

MTVCraft 的核心创新在于**将运动条件从2D渲染姿态图像彻底替换为4D运动标记**，并围绕这一表示构建了端到端的条件生成框架。这一转变解决了现有方法的两大瓶颈：2D渲染图像仅提供稀疏的结构线索，丢弃了丰富的时空运动信息；同时，渲染过程将运动与人物形状、绝对位置耦合，导致模型难以学习纯粹的运动语义。

### 1. 运动条件的表示革命：从2D渲染到4D标记

传统方法（如 **MusePose**、**Animate-X**、**Unianimate-DiT** 等）普遍依赖从驱动视频中提取并渲染的2D姿态图像（如DWPose骨架、SMPL渲染图或深度图）作为运动条件。这些图像虽然直观，但存在根本性缺陷：它们将3D关节运动投影到2D平面，丢失了深度信息，且不可避免地嵌入了源人物的体型和位置信息，使运动信号与身份信息相互纠缠。

MTVCraft 的 **4DMoT（4D Motion Tokenizer）** 模块直接从原始SMPL关节坐标序列中学习紧凑的离散运动标记。具体而言，它将关节坐标转化为**差分表示**——即相邻帧间的关节位移——从而将运动与绝对位置和人物形状解耦。随后，通过一个基于2D卷积的编码器-解码器架构在时空维度上进行压缩，再经由向量量化器（VQ）将连续潜在表示离散化为4D运动标记。这一过程的关键设计包括：
- **差分运动编码**：显式建模相对关节位移，使标记专注于运动动力学本身。
- **4D量化（含深度轴）**：在时间、x、y、z四个维度上进行量化，保留完整的3D空间运动信息。消融实验证实，将量化从4D降为3D（仅x、y轴）会导致FVD从317.21升至329.86（Table 2），证明深度轴信息的不可或缺。
- **离散化**：VQ-VAE的码本量化不仅压缩了表示，还迫使模型学习稳健的离散运动语义。移除量化后，VQ-VAE退化为标准自编码器，产生连续标记，FVD从317.21恶化至332.97（Table 2）。

### 2. 条件注入机制的革新：4D运动注意力

传统方法通常将2D姿态图像与噪声视频帧在通道维度拼接，或通过附加控制网络（如ControlNet）注入条件。这种注入方式缺乏对运动标记与视觉区域之间时空对应关系的显式建模。

MTVCraft 在视频DiT（Diffusion Transformer）中引入了**4D运动注意力**层，实现视觉标记与运动标记之间的交叉注意力交互。视觉标记作为查询（Query），运动标记作为键（Key）和值（Value），使模型能够在生成过程中动态地检索与当前时空位置相关的运动信息。

更为关键的是，该注意力机制配备了**4D旋转位置编码（4D RoPE）**。标准RoPE在序列维度上编码位置信息，MTVCraft将其扩展至4D空间，在时间、x、y、z四个轴上分别应用旋转矩阵：

$$P_{\mathrm{4D}} = \mathrm{Concat}(R_t, R_x, R_y, R_z)$$

这使得注意力机制能够感知运动标记与视觉标记在完整4D时空中的相对位置关系。消融实验提供了决定性证据：完全移除4D位置编码后，FVD从317.21飙升至548.31（Table 2），证明明确的4D位置信息是运动-视觉跨模态交互的基石。

### 3. 身份保持策略的简化

与多数基线方法采用独立的参考网络（ReferenceNet）或额外外观编码器不同，MTVCraft 采用了一种更简洁的**重复拼接（repeat-and-concatenate）**方案。参考图像的潜在特征被逐帧重复后与噪声视频潜在特征在通道维度拼接：

$$z_{\mathrm{vision}} = \mathrm{Concat}\left(z_0, \mathrm{Repeat}(z_{\mathrm{ref}}, f)\right) \in \mathbb{R}^{f \times 2c \times h \times w}$$

这种设计避免了额外网络带来的计算开销和训练复杂性，同时通过运动注意力机制确保身份信息与运动条件在统一的Transformer架构中协同作用。

### 4. 运动感知的无分类器引导

MTVCraft 进一步引入可训练的**无条件运动标记**，在训练过程中以一定概率随机替换原始运动条件。推理时，通过运动感知的无分类器引导（Motion-aware CFG），模型可以在运动准确性与生成质量之间取得平衡。实验表明，CFG尺度为3.0时在TikTok基准上达到最佳FVD（Figure 11）。

综上，MTVCraft 通过“4D运动标记化 + 4D运动注意力 + 4D RoPE”的组合创新，将运动条件从间接的2D视觉信号提升为直接的4D时空语义表示，实现了运动与外观的彻底解耦，这是其在开放世界场景中取得显著零样本泛化能力的根本原因。



MTVCraft 的整体 pipeline 由两大核心模块串联构成：**4D 运动标记器（4DMoT）** 与 **运动感知视频 DiT（MV-DiT）**，形成一条从原始 SMPL 关节序列到动画视频的端到端生成链路。

### 输入输出流

给定一张参考图像（提供外观与身份信息）和一段驱动视频（提供运动信息），系统按以下流程工作：

1. **运动提取与标记化**：使用外部姿态估计器从驱动视频中提取 SMPL 关节坐标序列，随后通过 4DMoT 将其编码为离散的 4D 运动标记。这些标记是量化的差分关节坐标，显式解耦了运动与绝对位置、形状变化，从而获得紧凑且鲁棒的运动表征（Section 3.1, Figure 3）。

2. **身份注入**：参考图像经 VAE 编码为潜在特征 $z_{\text{ref}}$，通过逐帧重复并与噪声视频潜在特征 $z_0$ 沿通道维拼接，形成复合视觉潜在 $z_{\text{vision}} = \operatorname{Concat}(z_0, \operatorname{Repeat}(z_{\text{ref}}, f))$（Equation 3）。该方案替代了独立的 ReferenceNet，以简洁的方式注入身份信息。

3. **运动条件生成**：MV-DiT 以 $z_{\text{vision}}$ 和 4D 运动标记为输入，通过专门设计的 **4D 运动注意力层** 实现跨模态交互——视觉标记作为查询，运动标记作为键/值，并施加 4D 旋转位置编码（4D RoPE）来编码时空关系（Equations 4–8）。最终，模型在运动感知的无分类器引导下迭代去噪，生成具有一致身份和准确运动的动画视频。

### 模块关系

- **4DMoT**（Figure 3）是一个基于 VQ-VAE 的编码器-解码器框架。编码器通过沿时间轴和关节轴的 2D 卷积与平均池化，将 SMPL 序列映射到连续潜在空间；向量量化器将其离散化为紧凑的 4D 运动标记；解码器则从这些标记重建原始运动序列。训练目标为 L1 重建损失与码本承诺损失的组合（Equation 2）。

- **MV-DiT**（Figure 4, Figure 6）在标准视频 DiT 架构中插入 4D 运动注意力层。该注意力层的核心创新在于将 3D RoPE 扩展至 4D（$P_{\text{4D}} = \operatorname{Concat}(R_t, R_x, R_y, R_z)$），为运动标记赋予深度轴的位置信息，使视觉标记与运动标记之间的交叉注意力能够感知完整的时空结构。

- **运动感知 CFG**：引入可学习的无条件运动标记 $c_{\text{mo}\varnothing}$，训练时以一定概率替换条件运动标记，推理时通过引导尺度调节运动对齐与生成质量之间的平衡（Figure 11）。

### 关键设计决策

| 设计选择 | 动机 | 消融依据 |
|---------|------|---------|
| 离散量化而非连续标记 | 离散标记提供更强的语义归纳偏置 | 移除量化后 TikTok FVD 从 317.21 升至 332.97（Table 2） |
| 差分运动表示 | 显式建模相对关节位移，捕获细粒度时序动态 | 移除差分运动后 FVD 升至 325.40（Table 2） |
| 4D 量化（含 z 轴）而非 3D | 保留深度维度的空间信息 | 3D 量化 FVD 为 329.86，4D 降至 317.21（Table 2） |
| 4D RoPE | 建立运动与视觉标记之间的结构化时空交互 | 完全移除 PE 后 FVD 飙升至 548.31（Table 2） |

### 模型规模扩展

MTVCraft 提供两种参数规模：6B 版本基于 CogVideoX-5B 构建，18B 版本基于 Wan-2-1-14B 构建（Section 3.3）。在 18B 版本中，通过零填充将运动标记维度与 DiT 隐藏维度对齐，实现文本与运动的联合控制。消融实验表明，用线性层或 MLP 替代零填充无法在 10000 步内收敛，证明简单投影不足以稳定大规模运动学习（Appendix H）。

### 补充图表

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/001_Figure_1.jpg]]
*Figure 1: Teaser. We propose MTVCraft, a versatile framework that can effectively transfer pose sequences from a driven video in either full-body or half-body settings, while supporting a wide range of visual styles such as anime, pixel art, ink drawings, and photorealism. Beyond human characters, MTVCraft is further capable of handling non-human subjects such as animals and even inanimate objects, demonstrating superior robustness, strong generalizability to open-world scenarios, and the emergent ability to animate arbitrary characters*



MTVCraft 的核心设计围绕两个关键模块展开：**4DMoT（4D运动标记器）** 和 **MV-DiT（运动感知视频DiT）**。前者将原始SMPL关节坐标序列压缩为离散的4D运动标记，后者以这些标记为条件生成动画视频。

### 4DMoT：4D运动标记器

传统方法将3D人体网格渲染为2D姿态图像，这一过程丢弃了丰富的时空运动信息，并引入了形状和绝对位置偏差。4DMoT直接对原始SMPL关节坐标序列进行标记化，将运动与绝对位置和形状解耦，得到紧凑且鲁棒的运动表示。

具体而言，给定一段包含 $f$ 帧、每帧 $j$ 个关节的SMPL序列，4DMoT首先计算**差分运动表示**（相邻帧之间的关节坐标差），以显式建模相对关节位移。随后，编码器通过沿时间轴和空间轴的2D卷积残差块将运动序列映射到连续潜空间，再经由向量量化器将其离散化为紧凑的4D运动标记。解码器则从这些标记重建原始运动序列。

训练目标为标准VQ-VAE损失：

$$
\mathcal{L}_{\mathbf{vq}} = \underbrace{\|M - \hat{M}\|_1}_{\mathrm{reconstruction}} + \beta \underbrace{\|E - \mathrm{sg}[C]\|_2^2}_{\mathrm{commitment}}
$$

其中 $M$ 为原始运动序列，$\hat{M}$ 为重建序列，$E$ 为编码器输出，$C$ 为量化码本向量，$\mathrm{sg}[\cdot]$ 表示停止梯度操作。第一项为L1重建损失，确保运动信息的保真度；第二项为码本承诺损失，约束编码器输出靠近最近的码本向量，$\beta$ 为平衡系数。

### MV-DiT：运动感知视频DiT

MV-DiT以4D运动标记和参考图像为条件，生成具有一致身份和准确运动的动画视频。其核心创新在于**4D运动注意力**机制和**4D旋转位置编码（RoPE）**。

**身份保持**：MV-DiT采用简洁的“重复-拼接”策略，无需额外的参考网络。将参考图像潜变量 $z_{\mathrm{ref}}$ 逐帧重复后与噪声视频潜变量 $z_0$ 沿通道维度拼接：

$$
z_{\mathrm{vision}} = \mathrm{Concat}\left(z_0, \mathrm{Repeat}(z_{\mathrm{ref}}, f)\right) \in \mathbb{R}^{f \times 2c \times h \times w}
$$

**4D运动注意力**：在DiT的Transformer块中插入运动注意力层，以视觉标记作为查询（Query），以4D运动标记作为键（Key）和值（Value），实现运动条件与视觉生成的跨模态交互。

**4D RoPE**：为增强时空关系建模，将标准3D RoPE扩展至4D，添加深度轴以适配运动标记的时空结构：

$$
P_{\mathrm{4D}} = \mathrm{Concat}(R_t, R_x, R_y, R_z)
$$

其中 $R_t, R_x, R_y, R_z$ 分别为时间、水平、垂直、深度轴的旋转矩阵。每个轴的旋转矩阵作用于对应的查询/键向量维度对：

$$
R_i(x, m) = \begin{bmatrix} \cos(m\theta_i) & -\sin(m\theta_i) \\ \sin(m\theta_i) & \cos(m\theta_i) \end{bmatrix} \begin{bmatrix} x_{2i} \\ x_{2i+1} \end{bmatrix}
$$

$m$ 为位置索引，$\theta_i$ 为频率参数。在运动注意力中，视觉标记的查询和运动标记的键分别应用4D RoPE：

$$
\mathbf{Q} = \mathrm{RoPE}(\mathrm{LayerNorm}(W_q(z_{\mathrm{vision}})), P_{4\mathrm{D}}^{\mathrm{vision}})
$$

**运动感知无分类器引导**：引入可学习的无条件运动标记 $c_{mo\varnothing}$，训练时以一定概率随机替换条件运动标记，推理时通过引导尺度平衡运动保真度与生成质量。

### 模型缩放

MTVCraft提供6B和18B两个版本。6B版本基于CogVideoX-5B骨干网络，18B版本采用Wan-2-1-14B骨干网络。在18B版本中，通过零填充将运动标记维度对齐到DiT的隐藏维度，实现联合文本-运动控制，进一步提升了生成性能。

### 补充图表

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of 4DMoT. An encoder-decoder framework learns spatial-temporal latent representations of SMPL joint coordinates, and a vector quantizer learns 4D compact yet expressive tokens in a unified space. All operations are in 2D space along the frame and joint axes*

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/004_Figure_4.jpg]]
*Figure 4: Architecture of MTVCraft-6B. Based on the video DiT model, we design unique 4D motion attention to leverage 4D motion tokens as context for vision generation. To enhance spatialtemporal relationships, we apply 4D RoPE over*

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/008_Figure_6.jpg]]
*Figure 6: Architecture of MTVCraft-18B. To demonstrate the versatility of our approach and further improve performance, we scale the model to a larger DiT and enable joint text-motion control. Here, zero-padding aligns the motion token dimension with the DiT hidden dimension*



## 实验与关键发现

### 核心实验设置

所有方法在相同的评估框架下进行公平对比：使用固定的文本提示（“a person is dancing”），采用 DDIM 50 步推理，随机种子固定。运动条件统一从驱动视频中提取 SMPL 序列。训练使用 8 块 NVIDIA H100 GPU，bfloat16 精度和 DeepSpeed ZeRO-2 优化。MTVCraft 提供两个参数规模版本：6B 版本基于 CogVideoX-5B 骨干网络，18B 版本基于 Wan-2-1-14B 骨干网络。

### 主结果：TikTok 基准

Table 1 展示了在 TikTok 基准上的定量对比。MTVCraft-18B 在所有指标上均取得最优结果，FVD 达到 276.65，相比最强基线 **Unianimate-DiT**（402.14）**降低 31.2%**；FID-VID 为 7.31，较 Unianimate-DiT（9.12）降低 19.9%。6B 版本同样展现出竞争力，FVD 为 317.21，显著优于其他基于 2D 渲染姿态图像的方法（如 **MusePose**、**MooraAA**、**ControlNeXt**、**MimicMotion** 等）。这表明直接用 4D 运动标记替代 2D 渲染姿态图像作为条件，能够为扩散模型提供更丰富、更准确的时空运动信息。

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/005_Table_1.jpg]]
*Table 1: Quantitative Results on TikTok (Jafarian & Park, 2021) Benchmark*

Figure 5 的定性对比进一步验证了这一结论。MTVCraft 在多种场景和多样化角色上始终展现出最佳的运动迁移质量和外观一致性，而基线方法在复杂运动下容易出现肢体扭曲或身份丢失。

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative Comparison. Our MTVCraft consistently demonstrates the best motion transfer performance and high appearance consistency across various scenes and diverse characters*

### 主结果：Fashion 基准

Table 3 报告了 Fashion 基准上的结果，MTVCraft-18B 同样取得全面最优：FVD 为 64.88，较 Unianimate-DiT（88.36）**降低 26.6%**；FID-VID 为 4.41，较 Unianimate-DiT（6.12）降低 27.9%。Fashion 基准包含更多半身和复杂着装场景，MTVCraft 的优势表明 4D 运动标记化对不同类型的运动条件具有良好的鲁棒性。

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/014_Table_3.jpg]]
*Table 3: Quantitative Results on Fashion (Zablotskaia et al., 2019) Benchmark*

### 消融研究：4D 运动标记化组件

Table 2 系统拆解了 4D 运动标记化（4D Motion Tokenizer）和 4D 运动注意力（4D Motion Attention）各组件的作用。

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/007_Table_2.jpg]]
*Table 2: Ablation Study on TikTok (Jafarian & Park, 2021) Benchmark*

**离散量化的必要性。** 移除量化后，VQ-VAE 退化为标准自编码器，产生连续运动标记，导致 FVD 从 317.21 升至 332.97。离散标记空间通过码本约束迫使模型学习更紧凑、更具判别力的运动表征，连续标记则引入了噪声和冗余。

**差分运动表示。** 移除差分运动后，FVD 升至 325.40。差分关节坐标显式建模相对位移，使模型能够捕捉细粒度的时序运动动态，而绝对坐标则混合了位置和形状信息，削弱了运动本身的表达能力。

**4D 量化优于 3D 量化。** 将 4D 量化（含 z 轴深度）替换为 3D 量化后，FVD 从 317.21 升至 329.86。深度轴为运动标记提供了完整的空间上下文，缺失该维度会导致运动表征的信息损失。

### 消融研究：4D 运动注意力与位置编码

**4D RoPE 是不可或缺的。** 完全移除 4D 位置编码后，FVD 从 317.21 飙升至 548.31，增幅高达 72.8%，是所有消融实验中影响最大的因素。Figure 10 揭示了其作用机制：4D RoPE 使运动标记与视觉标记之间的交叉注意力图呈现结构化模式，不同 Transformer 层形成差异化的时空交互，而移除 PE 后注意力分布趋于无序。4D RoPE 通过在 (t, x, y, z) 四个维度上编码位置关系，为跨模态调制提供了稳定的空间锚点。

**运动感知 CFG 的尺度选择。** Figure 11 展示了运动感知无分类器引导（Motion-aware CFG）尺度对生成质量的影响。较高的 CFG 尺度带来更好的姿态对齐，但同时引入更多伪影。实验表明尺度 3.0 在 TikTok 基准上取得最佳 FVD 权衡。

**大规模模型中的投影策略。** 在 18B 版本中，用线性层或 MLP 替代零填充来对齐运动标记维度与 DiT 隐藏维度，无法在 10000 步内收敛，证明简单投影不足以稳定大规模运动学习，零填充策略在保持运动语义完整性的同时实现了高效扩展。

### 失败模式与局限性

尽管 MTVCraft 在定量和定性评估中均表现优异，仍存在若干值得关注的失败模式：

1. **手部控制精度有限。** 训练数据中缺乏专门的手部监督信号，导致手指运动生成可能出现不自然的扭曲或缺失细节，这在需要精细手部交互的场景中尤为明显。

2. **外部姿态估计器的误差传导。** 模型依赖外部 SMPL 姿态估计器（如 NLF-Pose）提取运动序列，当驱动视频中的姿态估计出现误差时，该误差会直接传导至 4D 运动标记，进而影响生成结果的运动准确性。

3. **极端姿态下的不稳定扭曲。** 对于高难度体操动作或大幅度非典型姿态，尽管模型展现出令人瞩目的零样本泛化能力，仍可能出现局部肢体扭曲或运动不连贯的情况。

4. **单人限制。** 当前版本仅支持单人动画，无法处理多人交互或复杂的多主体场景，这限制了其在群舞、体育比赛等场景中的应用。

5. **非人物体的泛化边界。** 尽管 Figure 1 展示了动物甚至非生命物体的动画能力，但对于形态与人体差异极大的目标，运动标记的固定维度可能无法充分表达其运动特性，导致细节丢失或运动失真。

### 关键图表结论汇总

- **Table 1 & Table 3**：MTVCraft-18B 在两个标准基准上全面超越所有基于 2D 渲染姿态的基线方法，FVD 相对提升 26%-31%。
- **Table 2 & Table 4**：离散量化、差分运动、4D 量化和 4D RoPE 均为关键设计，其中 4D RoPE 的影响最为显著，移除后 FVD 恶化 72.8%。
- **Figure 5 & Figure 13**：定性结果一致表明 MTVCraft 在运动保真度和外观一致性上具有显著优势。
- **Figure 10**：4D RoPE 通过结构化交叉注意力实现有效的运动-视觉交互。
- **Figure 11**：运动感知 CFG 尺度 3.0 为最优平衡点。

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/013_Figure_10.jpg]]
*Figure 10: Effectiveness of 4D RoPE for Motion-Vision Interaction. (a) Cross-attention maps at different Transformer blocks show that 4D RoPE enables structured interactions between motion and vision tokens. (b) Visualization of mean joint coordinates across the dataset, used to compute 4D RoPE, providing typical spatial cues that facilitate consistent cross-modal modulation*

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/015_Table_4.jpg]]
*Table 4: Ablation Study on Fahsion (Zablotskaia et al., 2019) Benchmark*

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/016_Figure_11.jpg]]
*Figure 11: Ablation of Motion-aware CFG. A higher CFG scale leads to better pose alignment, but also introduces more artifacts. In our experiments, a scale of 3.0 achieves the best trade-off*

![[assets/figures/papers/paper_list_l1831_MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation/figures/018_Figure_13.jpg]]
*Figure 13: More Comparisons (1). Our MTVCraft consistently demonstrates the best performance with high-quality human motion and high-fidelity appearance across different styles and scenes*



## 定位与知识库关联

### 与现有方法的关系与根本差异

MTVCraft 的核心突破在于**运动条件表示的根本性转变**：从传统方法普遍采用的 2D 渲染姿态图像，转向直接对原始 4D 运动序列进行离散标记化。这一转变解决了该领域长期存在的瓶颈——2D 渲染姿态图像仅提供有限的结构线索，丢弃了丰富的 4D 时空信息，导致复杂运动下生成扭曲或伪影。

具体而言，MTVCraft 与现有基线方法在三个关键维度上存在本质差异：

**1. 运动条件表示**
- **基线方法**（MusePose、MooraAA、ControlNeXt、Animate-X、MimicMotion、RealisDance-DiT、Unianimate-DiT 等）均依赖从驱动视频中提取的 2D 渲染姿态图像作为运动条件，如 DWPose 骨架、SMPL 渲染或深度图。这些表示将 3D 运动投影到 2D 平面，不可避免地引入形状和绝对位置偏差，且丢失深度维度的运动信息。
- **MTVCraft** 通过 4DMoT（4D Motion Tokenizer）直接将 SMPL 关节坐标序列量化为离散的 4D 运动标记。该标记化过程显式解耦运动与绝对位置和形状变化，保留了完整的时空运动语义。消融实验证实，移除差分运动表示后 FVD 从 317.21 升至 325.40（Table 2），证明相对关节位移对捕捉细粒度时序运动动态至关重要。

**2. 条件注入机制**
- **基线方法**通常在扩散模型中拼接姿态图像，或通过附加控制网络（如 ControlNet）注入运动条件。这种方式将运动信息与视觉特征在空间维度上混合，缺乏对运动时空结构的显式建模。
- **MTVCraft** 在 DiT 架构中插入专用的 4D 运动注意力层，以视觉标记为查询、运动标记为键/值进行交叉注意力计算，并应用 4D 旋转位置编码（RoPE）编码时空位置关系。这一设计使视觉标记能够自适应地关注相关运动标记，实现结构化的跨模态交互。Figure 10 的可视化证实，4D RoPE 使运动标记与视觉标记之间形成有组织的注意力模式。消融实验表明，完全移除位置编码导致 FVD 从 317.21 飙升至 548.31（Table 2），证明明确的 4D 位置信息不可或缺。

**3. 身份保持策略**
- **基线方法**通常采用独立的参考网络（如 ReferenceNet）或额外外观编码器来保持身份一致性，增加了模型复杂度和计算开销。
- **MTVCraft** 采用简洁的 repeat-and-concatenate 方案：将参考图像潜在特征逐帧重复后与噪声视频潜在特征拼接（$z_{\mathrm{vision}} = \mathrm{Concat}(z_0, \mathrm{Repeat}(z_{\mathrm{ref}}, f))$），无需额外网络模块即可有效注入身份信息。

### 方法适用边界

MTVCraft 在以下场景展现出显著优势：
- **开放世界零样本泛化**：支持任意角色（真人、动漫、像素画、水墨画等风格）的全身/半身动画，甚至扩展至动物和非生命物体。
- **大规模模型扩展**：方法可平滑从 6B 参数（基于 CogVideoX-5B）扩展至 18B 参数（基于 Wan-2-1-14B），18B 版本在 TikTok 基准上 FVD 达 276.65，较最强基线 Unianimate-DiT（402.14）降低 31.2%（Table 1）；在 Fashion 基准上 FVD 达 64.88，较 Unianimate-DiT（88.36）降低 26.6%（Table 3）。

然而，方法存在明确的适用边界和已知局限：
- **手部控制精度有限**：训练数据中缺乏专门的手部监督信号，导致手指运动生成质量不足。
- **依赖外部姿态估计器**：方法依赖 NLF-Pose 等外部 SMPL 姿态估计器，其误差可能传导至生成结果，影响运动准确性。
- **仅支持单人动画**：当前版本无法处理多人交互或复杂的多主体场景。
- **极端姿态不稳定**：对于高难度体操动作或非人物体，仍可能出现不稳定的扭曲。
- **运动标记维度固定**：可能不适用于极其复杂或超长的运动序列，可能丢失部分细节。

### 开放问题与未来方向

MTVCraft 开辟了若干值得探索的研究方向：

1. **多人动画扩展**：如何将 4D 运动标记化扩展至多人动画或人物交互场景，是提升方法实用性的关键挑战。
2. **跨类别运动建模**：该方法可否适配其他类型的运动数据（如动物或关节物体），实现统一的运动标记化框架。
3. **手部细节增强**：引入手部关键点损失或专门的手部监督信号，改进手指运动的生成质量。
4. **多模态条件融合**：结合文本、音频等多模态条件，实现更丰富的控制信号，拓展应用场景。
5. **推理效率优化**：在大规模实时应用（如数字人、直播）中，如何优化推理速度和计算成本，是产业化落地的关键瓶颈。



## 原文 PDF

![[paperPDFs/arxiv_2025/MTVCrafter_4D_Motion_Tokenization_for_Open_World_Human_Image_Animation.pdf]]
