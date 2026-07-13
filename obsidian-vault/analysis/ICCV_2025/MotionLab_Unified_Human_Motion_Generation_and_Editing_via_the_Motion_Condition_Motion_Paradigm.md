---
title: "MotionLab: Unified Human Motion Generation and Editing via the Motion-Condition-Motion Paradigm"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm.pdf
project_link: https://diouo.github.io/motionlab.github.io/
code_link: null
aliases:
- MotionLab
tags:
- ICCV_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "提出 Motion-Condition-Motion 统一范式，将所有任务抽象为源运动、条件、目标运动三要素；并设计 MotionFlow Transformer、Aligned ROPE、Task Instruction Modulation 和 Motion Curriculum Learning 实现多任务统一学习与高效推理。"
primary_logic: "借助修正流 (rectified flow) 将源运动到目标运动的映射建模为最优传输路径，并通过课程学习从简单到复杂逐步引入多模态任务，先学运动先验再适应编辑条件，使得单一框架能够同时处理生成与编辑，并利用多任务数据提升整体性能。"
claims:
- "通过 Motion-Condition-Motion 范式可将文本生成、轨迹生成、运动编辑、插值和风格迁移等任务统一为源运动、条件、目标运动三个概念的组合。"
- "在轨迹运动生成（骨盆控制）上，MotionLab 的 FID 为 0.095，大幅优于此前最优的 OmniControl (0.212)。"
- "移除 Motion Curriculum Learning 后，文本生成 FID 从 0.167 恶化至 1.956，说明课程学习对多任务训练至关重要。"
- "Aligned ROPE 对空间相关任务（轨迹生成、运动插值）尤为关键，移除后平均误差分别上升至 0.0886 和 0.0756。"
---

# MotionLab: Unified Human Motion Generation and Editing via the Motion-Condition-Motion Paradigm

> [!tip] 核心洞察
> 借助修正流 (rectified flow) 将源运动到目标运动的映射建模为最优传输路径，并通过课程学习从简单到复杂逐步引入多模态任务，先学运动先验再适应编辑条件，使得单一框架能够同时处理生成与编辑，并利用多任务数据提升整体性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionLab：基于运动-条件-运动范式的统一人体运动生成与编辑 |
| 英文题名 | MotionLab: Unified Human Motion Generation and Editing via the Motion-Condition-Motion Paradigm |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2412.02829) · [Project](https://diouo.github.io/motionlab.github.io/) |
| Topic |  |
| Method | MotionLab |
| Dataset | HumanML3D, MotionFix |

> [!tip] 效果简介
> - HumanML3D 上，FID (轨迹生成，仅骨盆) 为 0.095，对比 OmniControl: 0.212，变化 -0.117 (下降55%)。
> - MotionFix 上，R@1 (轨迹编辑) 为 72.65，对比 TMED*: 60.01，变化 +12.64。
> - HumanML3D 上，关键帧误差 (运动插值，5帧) 为 0.0283，对比 CondMDI: 0.1789，变化 -0.1506 (下降84%)。

## 概要

### 问题背景

人体运动生成与编辑是计算机视觉与图形学中的重要任务，涵盖文本到运动生成、轨迹控制生成、运动编辑、运动插值、风格迁移等多种子任务。然而，现有方法通常为不同任务设计孤立模型——例如，**MDM** 基于扩散模型处理文本生成，**OmniControl** 专注轨迹约束生成，**MotionFix** 仅处理运动编辑——这些方法各自独立训练，无法利用任务间的内在联系进行知识共享。这种碎片化范式导致实际应用中效率低下，每引入一个新任务就需要重新设计并训练专用模型，扩展性差。

### 核心思路

本文提出 **MotionLab**，一个统一的人体运动生成与编辑框架，其核心是 **Motion-Condition-Motion 范式**：将所有任务抽象为**源运动 (source motion)、条件 (condition)、目标运动 (target motion)** 三个要素的组合。例如，文本生成任务中源运动为空（高斯噪声）、条件为文本、目标运动为生成结果；运动编辑任务中源运动为待编辑序列、条件为编辑指令、目标运动为编辑后序列。这一范式使得单一模型能够覆盖 6 类主要任务（Table 2）。

在技术层面，MotionLab 建立在**修正流 (rectified flows)** 之上，将源运动到目标运动的映射建模为最优传输路径，相比扩散模型的弯曲轨迹，修正流的线性插值轨迹保持恒定速度，训练更稳定、推理更高效。框架采用 **MotionFlow Transformer (MFT)** 作为核心生成网络，通过联合注意力机制、模态专用路径和**对齐 ROPE (Aligned ROPE)** 位置编码处理多模态输入，并引入**任务指令调制 (Task Instruction Modulation)** 和**运动课程学习 (Motion Curriculum Learning)** 实现多任务统一训练。

### 主要发现

MotionLab 在多个任务上取得显著性能提升：

- **轨迹运动生成**（仅骨盆控制）：FID 达到 **0.095**，较此前最优方法 OmniControl (0.212) 下降 **55%**（Table 4）。
- **运动编辑**：轨迹编辑 R@1 达到 **72.65**，较基线 TMED* (60.01) 提升 **+12.64**（Table 5）。
- **运动插值**（5 帧关键帧）：关键帧误差仅 **0.0283**，较 CondMDI (0.1789) 下降 **84%**（Table 8）。
- **推理效率**：文本生成平均推理时间仅 **0.068 秒**，较 MDM (26.04 秒) 加速约 **380 倍**（Table 3）。

消融实验揭示了几个关键设计的作用：移除课程学习后文本生成 FID 从 0.167 恶化至 1.956，说明多任务训练中由易到难的课程顺序至关重要；移除 Aligned ROPE 后空间相关任务（轨迹生成、运动插值）的平均误差分别上升至 0.0886 和 0.0756，验证了该编码对空间感知的必要性（Table 6, Table 10）。

需要指出的是，在文本生成任务上，论文声称 MotionLab 取得了“最低 FID”，但 Table 3 显示 T2M-GPT 的 FID 为 **0.116**，低于 MotionLab 的 **0.167**，该声明存在矛盾，需进一步核实评估设置差异。

### 方法定位

MotionLab 属于**统一生成式框架**，区别于为单一任务设计的专用模型。其设计理念与扩散模型（如 MDM、MLD）和自回归模型（如 T2M-GPT）形成对比：后者通常依赖迭代去噪或逐帧预测，而 MotionLab 借助修正流实现少步数（甚至单步）高效生成。在任务覆盖面上，Table 1 显示 MotionLab 是首个同时原生支持文本生成、轨迹生成、文本编辑、轨迹编辑、运动插值和风格迁移的框架，而此前方法最多覆盖其中 2–3 项任务。



人体运动生成与编辑是计算机视觉与图形学领域的核心问题，其目标是根据文本描述、空间轨迹、风格参考等条件，自动合成自然、多样且符合物理约束的人体动作序列。该技术在动画制作、虚拟现实、游戏开发和机器人仿真等场景中具有广泛的应用前景。近年来，扩散模型（diffusion models）和自回归模型在该领域取得了显著进展，涌现出 **MDM**、**MLD**、**T2M-GPT** 等代表性方法，分别在生成质量和多样性上不断刷新基准。

然而，当前研究面临一个根本性的瓶颈：**不同任务（如文本生成、轨迹控制、运动编辑、插值、风格迁移）通常由孤立模型处理，缺乏统一的建模框架**。如 Table 1 所示，现有方法大多仅针对单一或少数任务进行训练，无法在多个任务间共享运动先验知识。这种碎片化的研究范式导致三个突出问题：

1. **效率低下**：每个任务需要独立训练和部署模型，计算与存储开销随任务数量线性增长。
2. **扩展性差**：新任务需要从头设计架构和训练策略，难以复用已有能力。
3. **知识隔离**：不同任务间的内在联系（如编辑任务依赖于生成任务学到的运动先验）无法被利用，限制了整体性能的上限。

从技术路径来看，现有方法在框架选择上主要分为两类：基于扩散模型的逐步去噪范式，和基于自回归模型的逐帧预测范式。扩散模型虽然生成质量较高，但推理速度慢（如 MDM 单次生成需约 26 秒）；自回归模型推理快但存在误差累积问题。更重要的是，这两种范式都缺乏对“源运动→目标运动”这一映射关系的显式建模，导致在编辑和插值等需要保持源运动语义的任务中表现受限。

本文的核心动机在于：**是否可以通过一个统一的范式，将人体运动生成与编辑的各类任务纳入同一框架，从而打破任务壁垒、实现知识共享？** 为此，本文提出 **Motion-Condition-Motion** 范式，将所有任务抽象为三个基本概念的组合——源运动（source motion）、条件（condition）和目标运动（target motion）——并基于修正流（rectified flows）的最优传输特性，设计统一的生成框架 **MotionLab**，以期在单一模型中同时实现多任务的高质量生成与高效推理。



## 核心方法与创新机理

MotionLab 的核心创新并非单一模块的修修补补，而是通过 **Motion-Condition-Motion 统一范式** 将人体运动生成与编辑的所有任务抽象为“源运动—条件—目标运动”三要素，从而在一个框架内实现知识共享（Table 2）。围绕这一范式，方法在四个关键维度上做出了根本性改变：

### 1. 生成框架：从扩散/自回归到修正流 + MM-DiT

现有方法普遍依赖扩散模型（如 **MDM**、**MLD**）或自回归模型（如 **T2M-GPT**）进行运动生成。MotionLab 转而采用 **修正流 (rectified flows)** 结合 **MM-DiT** 架构（1. Introduction）。其核心机理在于：修正流假设源运动与目标运动之间的传输轨迹为线性插值 $x_t = (1-t)x_0 + t x_1$，使得速度场 $v_t$ 保持恒定，从而比扩散模型的弯曲轨迹更稳定、更高效（Figure 7）。训练目标直接最小化预测速度与真实速度的 L2 距离：

$$\mathcal{L}_{RF}(\theta) = \int_{0}^{1} \mathbb{E}_{(x_{0}, x_{1}) \sim (p_{0}, p_{1})} [\| v_{\theta}(t, x_{t}) - v_{t} \|_{2}^{2}] dt$$

推理时通过欧拉步 $x_{t - \frac{1}{N}} = x_{t} - \frac{1}{N} v_{\theta}(t, x_{t})$ 即可从噪声快速生成目标运动。这一改变带来了约 380 倍的推理加速：文本生成任务上 MotionLab 的 AITS 仅 0.068 秒，而 MDM 需 26.04 秒（Table 3）。消融实验证实，移除修正流后各任务性能全面下降，文本生成 FID 从 0.167 升至 0.301（Table 6）。

### 2. 序列位置编码：从绝对/3D ROPE 到对齐的 1D ROPE

传统方法使用绝对位置编码或 3 维 ROPE 编码关节的空间关系。MotionLab 提出 **Aligned ROPE**，将所有模态的 token 统一用 1 维 ROPE 编码时序信息，确保源运动、条件与目标运动在时间维度上对齐（Sec. 5.1）。这一设计对空间相关任务尤为关键：移除 Aligned ROPE 后，轨迹生成的平均误差从 0.0334 飙升至 0.0886，运动插值平均误差从 0.0273 升至 0.0756（Table 6, Table 10）。定性结果也显示，使用 1D 可学习位置编码时插值运动出现明显错位，而 Aligned ROPE 能准确保持关键帧姿态（Figure 9）。

### 3. 任务适配机制：从独立模块到 Task Instruction Modulation

以往多任务运动系统要么为每个任务设计独立的交叉注意力模块，要么用简单的 one-hot 编码区分任务，难以捕捉任务间的语义关联。MotionLab 的 **Task Instruction Modulation** 利用 CLIP 文本嵌入 $I \in \mathbb{R}^{1 \times 768}$ 作为任务指令输入 MotionFlow Transformer，使同一网络能根据语义区分“文本生成”“轨迹编辑”“风格迁移”等任务（Sec. 5.2）。消融研究表明，CLIP 嵌入在所有指标上均优于 one-hot 编码和可学习标记（Table 9），证明预训练语言模型提供的语义先验对任务区分至关重要。

### 4. 多任务训练策略：从混合训练到 Motion Curriculum Learning

将所有任务直接混合训练会引发灾难性遗忘和优化冲突。MotionLab 提出 **运动课程学习**，采用“从易到难”的分层训练策略：先预训练文本生成任务以学习通用运动先验，再逐步引入轨迹生成、运动编辑、插值、风格迁移等更复杂的条件任务（Sec. 5.3）。这一策略是多任务训练的基石——移除课程学习后，文本生成 FID 从 0.167 崩溃至 1.956，其他任务同样全面退化（Table 6）。课程学习使得模型能够先建立稳定的运动表征，再适应多样化的编辑条件，从而实现正迁移而非相互干扰。

### 创新间的因果耦合

上述四个创新并非孤立存在，而是形成了一条因果链：**修正流** 提供了高效、稳定的生成基础；**Aligned ROPE** 确保多模态序列在时间上对齐；**Task Instruction Modulation** 使同一网络能区分不同任务；**课程学习** 则决定了这些能力能否被有效联合训练。缺失任一环节都会导致特定任务或整体性能的显著退化，这从 Table 6 的系统消融中得到了充分验证。



MotionLab 的核心设计理念是将人体运动生成与编辑统一于 **运动-条件-运动 (Motion-Condition-Motion)** 范式之下。该范式将所有任务抽象为三个基本要素：**源运动 (source motion)**、**条件 (condition)** 与 **目标运动 (target motion)**。无论任务表面形式是文本生成、轨迹控制、运动编辑还是风格迁移，其本质均可映射为“给定源运动与条件，生成目标运动”的统一问题 (Table 2)。这一抽象使得单一框架能够同时覆盖生成与编辑，并利用多任务数据间的内在联系进行知识共享。

在此范式之上，MotionLab 的整体 pipeline 由三个关键模块串联构成：

1. **MotionFlow Transformer (MFT)**：核心生成网络，负责在修正流 (rectified flow) 框架下预测从源运动到目标运动的速度场。MFT 接收多模态输入（源运动、目标运动噪声、文本、轨迹、风格等），通过联合注意力 (Joint Attention)、模态路径 (Modality Path) 和对齐旋转位置编码 (Aligned ROPE) 实现跨模态交互与条件生成，无需为不同任务设计独立模块。

2. **Task Instruction Modulation (任务指令调制)**：利用 CLIP 文本嵌入为每个任务生成可区分的指令向量 $I \in \mathbb{R}^{1 \times 768}$，输入 MFT 使其能够根据任务类型自适应地调整行为。该机制替代了传统的 one-hot 编码或可学习标记，为多任务统一训练提供了灵活的任务区分能力。

3. **Motion Curriculum Learning (运动课程学习)**：采用由易到难的分层训练策略，分阶段逐步引入任务——先学习运动先验（文本生成），再逐步引入编辑条件（轨迹、风格等）。这一策略有效缓解了多任务联合训练中的灾难性遗忘问题，是实现多任务统一框架的关键训练手段。

**输入输出流**：对于给定任务，源运动 $M_S$（在纯生成任务中为随机噪声）与条件 $C$（文本、轨迹、风格等）被编码后输入 MFT；MFT 在任务指令 $I$ 的调制下，预测从当前状态到目标运动的修正流速度场 $v_\theta$；最终通过数值积分（欧拉步）从噪声逐步生成目标运动 $M_T$。整个流程在 Figure 2 中有完整的架构示意。

**关键组件间的因果依赖**：消融实验 (Table 6, Table 10) 揭示了一条清晰的因果链——移除课程学习直接导致所有任务崩溃（文本生成 FID 从 0.167 飙升至 1.956），说明多任务统一的前提是合理的训练顺序；在此基础上，Aligned ROPE 对空间相关任务（轨迹生成、运动插值）至关重要，移除后平均误差分别上升至 0.0886 和 0.0756；而修正流框架则为整个 pipeline 提供了高效的生成基础，移除后各任务性能全面下降。三者共同构成了 MotionLab 统一框架不可分割的技术支柱。

### 补充图表

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/001_Figure_1.jpg]]
*Figure 1: Demonstration of our MotionLab’s versatility, performance and efficiency. Ours specialists refer to the proposed framework tailored for specified tasks. Previous SOTA refer to multiple models, including MotionLCM [12], OmniControl [64], MotionFix [6], CondMDI [11] and MCM-LDM [55]. All motions are represented using SMPL [39], where transparent motion indicates the source motion or condition, and the other represents the target motion. More qualitative results are available in the website and appendix*



### 4.1 修正流基础

MotionLab 的生成过程建立在**修正流 (rectified flows)** 之上。给定源运动 $x_0$ 和目标运动 $x_1$，修正流通过线性插值定义一条从噪声到数据的直线轨迹：

$$x_t = (1 - t) x_0 + t x_1, \quad t \in [0, 1]$$

该轨迹对应的**速度场**为常数，定义为：

$$v_t = \frac{d x_t}{d t} = \frac{\partial \varphi_t(x_0, x_1, t)}{\partial t}, \quad t \in [0, 1]$$

其中 $\varphi_t$ 为流映射。MotionLab 的核心网络（MotionFlow Transformer）学习预测该速度场 $v_\theta(t, x_t)$，训练目标为最小化预测速度与真实速度的 L2 距离：

$$\mathcal{L}_{RF}(\theta) = \int_{0}^{1} \mathbb{E}_{(x_0, x_1) \sim (p_0, p_1)} \left[ \| v_\theta(t, x_t) - v_t \|_2^2 \right] dt$$

推理时，从噪声 $x_1$ 出发，通过欧拉步逐步积分得到数据 $x_0$：

$$x_{t - \frac{1}{N}} = x_t - \frac{1}{N} v_\theta(t, x_t)$$

其中 $N$ 为采样步数。与扩散模型基于噪声调度的弯曲轨迹不同，修正流的线性轨迹保持恒定速度，使得模型学习更稳定且推理更高效（见 **Figure 7**）。

### 4.2 MotionFlow Transformer (MFT)

MotionFlow Transformer 是 MotionLab 的核心生成网络，基于 MM-DiT 架构设计，接收多模态输入并预测速度场。MFT 包含三个关键组件（见 **Figure 2**）：

- **联合注意力 (Joint Attention)**：使来自不同模态的 token 能够充分交互。在多任务统一框架中，源运动、目标运动（噪声）、文本、轨迹、风格等模态的 token 被拼接后送入联合注意力层，实现跨模态信息融合。

- **模态路径 (Modality Path)**：为每种模态分配独立的处理路径，用于区分不同模态的 token 并提取其特定表征。路径设计确保各模态信息在进入联合注意力之前得到适当的编码。

- **对齐 ROPE (Aligned ROPE)**：采用一维旋转位置编码对序列中各组件进行时间对齐。与传统的三维 ROPE 或绝对位置编码不同，Aligned ROPE 针对运动序列的时序特性进行优化，对空间相关任务（轨迹生成、运动插值）尤为关键。消融实验（**Table 6, Table 10**）表明，移除 Aligned ROPE 后，轨迹生成平均误差从 0.0334 升至 0.0886，运动插值平均误差从 0.0273 升至 0.0756。

### 4.3 任务指令调制 (Task Instruction Modulation)

为实现多任务的统一处理，MotionLab 引入任务指令调制机制。对于每个任务，使用 CLIP 文本编码器提取任务特定的指令向量：

$$I \in \mathbb{R}^{1 \times 768}$$

该指令向量与运动 token 一同输入 MFT，使网络能够根据任务类型自适应地调整其行为。消融实验（**Table 9**）表明，使用 CLIP 文本嵌入优于 one-hot 编码和可学习标记，在多个指标上取得最佳效果。具体任务指令文本示例见 **Table 13**。

### 4.4 运动课程学习 (Motion Curriculum Learning)

多任务联合训练面临任务难度差异大、知识共享困难等挑战。MotionLab 采用从易到难的分层训练策略：

1. **预训练阶段**：先在文本-运动生成任务上训练，使模型学习基本的运动先验知识。
2. **微调阶段**：逐步引入运动编辑、轨迹生成、运动插值、风格迁移等更复杂的条件任务。

消融实验（**Table 6**）显示，移除课程学习直接导致所有任务崩溃——文本生成 FID 从 0.167 飙升至 1.956，验证了课程学习对多任务训练的关键作用。

### 4.5 无分类器引导

在运动生成任务中，MotionLab 采用无分类器引导 (CFG) 增强条件控制。给定条件 $C$，引导后的速度场为：

$$v_\theta(M_T, t, C) = v_\theta(M_T \mid t, \emptyset) + \lambda_C \left[ v_\theta(M_T \mid t, C) - v_\theta(M_T \mid t, \emptyset) \right]$$

其中 $\lambda_C$ 为条件引导强度，$\emptyset$ 表示无条件。各任务的引导强度参数见 **Table 14**。



## 实验与关键发现

### 核心性能表现

MotionLab 在多个任务上展现出显著优势，尤其在轨迹生成、运动编辑和运动插值任务中大幅超越此前最优方法。

**文本运动生成**：在 HumanML3D 基准上，MotionLab 取得 FID 0.167、R@3 0.810、MM Dist 2.830、Mmodality 2.912（Table 3）。虽然论文声称“最低 FID”，但需注意 T2M-GPT 的 FID 为 0.116，低于 MotionLab 的 0.167，该声明与表格数据存在矛盾，建议读者对比时以表格实测值为准。MotionLab 的核心优势体现在推理效率——单次生成仅需 0.068 秒（AITS），相比扩散模型基线 MDM 的 26.04 秒实现约 380 倍加速，这得益于修正流只需极少推理步数即可完成采样。

**轨迹运动生成**：在仅骨盆控制条件下，MotionLab 的 FID 降至 0.095，大幅优于此前最优的 OmniControl（0.212），相对提升约 55%（Table 4）。同时平均轨迹误差仅为 0.0286，表明生成的运动在空间约束上的精确性。

**运动编辑**：在 MotionFix 数据集上，MotionLab 的 R@1 达到 72.65（文本编辑），显著高于重新实现的 TMED*（60.01）（Table 5）。需注意 TMED* 为适应 HumanML3D 格式而重新实现，可能引入偏差。

**运动插值**：在 5 帧关键帧条件下，MotionLab 的关键帧误差仅为 0.0283，而基线 CondMDI 为 0.1789，误差下降约 84%（Table 8），展示了模型在稀疏关键帧之间生成平滑过渡运动的强能力。

**运动风格迁移**：定性对比（Figure 8）显示 MotionLab 在保持源运动语义和吸收风格运动特征两方面均优于 MCM-LDM。

### 关键组件消融分析

Table 6 的系统消融揭示了各组件对多任务统一训练的关键作用：

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/011_Table_6.jpg]]
*Table 6: Ablation studies of key components of MotionLab on each task. Refer to the text for the detailed configuration of each variant*

**修正流（Rectified Flows）**：移除修正流后，各任务性能全面下降。文本生成 FID 从 0.167 升至 0.301，轨迹生成平均误差从 0.0286 升至 0.0359。修正流的核心优势在于其线性插值轨迹 $x_t = (1-t)x_0 + t x_1$ 保持恒定速度，相比扩散模型的非线性轨迹（Figure 7），学习过程更稳健、推理效率更高。

**对齐位置编码（Aligned ROPE）**：该组件对空间相关任务尤为关键。移除后，轨迹生成平均误差从 0.0334 急剧上升至 0.0886，运动插值平均误差从 0.0273 升至 0.0756（Table 6, Table 10）。Figure 9 的定性消融直观展示了使用 1D 可学习位置编码时生成运动与关键帧姿态明显偏离，而 Aligned ROPE 能精确对齐输入关键帧。

**运动课程学习（Motion Curriculum Learning）**：这是多任务训练中最关键的组件。完全移除课程学习后，文本生成 FID 从 0.167 飙升至 1.956，几乎导致模型崩溃（Table 6）。Table 11 进一步表明，从简单任务（文本生成）到复杂任务（多条件编辑）的渐进式训练策略对防止灾难性遗忘和促进知识共享不可或缺。

**任务指令调制（Task Instruction Modulation）**：Table 9 的消融对比了三种任务区分方式——CLIP 文本嵌入、one-hot 编码和可学习标记。CLIP 文本嵌入在多数指标上取得最优，验证了利用基础模型语义表示区分任务模态的有效性。

### 推理效率与步数分析

Figure 6 展示了推理步数对性能与效率的 trade-off 关系。MotionLab 仅需极少量步数即可达到优异性能，在图中靠近左下方（高性能+高效率）区域。Table 7 报告了模型的内存占用和时间开销，具体数值需查阅原文。

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/014_Table_7.jpg]]
*Table 7: The memory usage and time cost of MotionLab*

### 任务组合分析

Table 12 探索了不同任务组合对训练效果的影响。结果表明，多任务联合训练能通过任务间的知识共享提升整体性能，但任务选择需合理搭配——某些任务组合可能因条件冲突导致性能下降，具体组合效果需参考原表。

### 方法能力对比

Table 1 系统对比了 MotionLab 与现有方法在 8 类任务上的覆盖能力。MotionLab 是唯一在所有任务上均完成训练（✓）的框架，而其他方法通常仅覆盖 1-3 个任务，其余任务要么无法实现（×），要么仅能以零样本方式勉强运行（−）。这凸显了统一范式在实用性和扩展性上的根本优势。

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/002_Table_1.jpg]]
*Table 1: Summary of methods focusing on motion generation and editing. ✓ indicates that the method has been trained for the task, × indicates that the method fails to implement, and − indicates that the method has not been trained but can implement in a zero-shot manner*

### 公平性说明

1. **文本生成 FID 声明矛盾**：论文声称 MotionLab 取得“最低 FID”，但 Table 3 中 T2M-GPT 的 FID（0.116）低于 MotionLab（0.167）。该差异可能源于指标计算方式或评估设置不同，需手动核实。
2. **TMED 重新实现**：运动编辑基线 TMED* 为适应 HumanML3D 格式重新实现，与原始 TMED 可能存在性能偏差。
3. **训练资源**：MotionLab 在 4×RTX 4090D 上训练约 4 天，相比部分轻量基线资源需求较高，但考虑到其统一多任务的能力，该开销在可接受范围内。

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/006_Table_3.jpg]]
*Table 3: Evaluation of text-based motion generation on HumanML3D [21] dataset. The models in bold are the optimal models, and the models in underline are the sub-optimal models*

### 补充图表

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/013_Figure_7.jpg]]
*Figure 7: Demonstration of the difference between diffusion models and rectified flows. This difference lies in that the trajectory of diffusion models is based on $x _ { t } = \sqrt { ( 1 - \overline { { \alpha _ { t } } } ) } x _ { 0 } + \sqrt { \overline { { \alpha _ { t } } } } \epsilon$ , while the trajectory of rectified flows is based on $x _ { t }$ = ( 1 - t ) $x _ { 0 }$ + tx1. This distinction leads to more robust learning by maintaining a constant velocity, contributing to the model’s efficiency [70]

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/003_Table_2.jpg]]
*Table 2: Structuring human motion tasks within our Motion-Condition-Motion paradigm*

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/005_Table.jpg]]

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/007_Table_4.jpg]]
*Table 4: Evaluation of trajectory-based motion generation on HumanML3D [21] dataset. Table 5. Evaluation of text-based and trajectory-based motion editing on MotionFix [6] dataset. TMED∗ mean that we reimplement the models since the original models are in the skeleton of SMPL format, while ours is in HumanML3D format*

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/015_Table_8.jpg]]
*Table 8: Evaluation of motion in-between with CondMDI [11] on HumanML3D [21] dataset*

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/017_Table_9.jpg]]
*Table 9: Ablation studies of Task Instruction Modulation*

![[assets/figures/papers/paper_list_l22_MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Con/figures/019_Figure_9.jpg]]
*Figure 9: Ablation results of MotionLab on the motion in-between (with text). Beige motion is use 1D-learnable position encoding, purple motion use Aligned ROPE, and gray motions are the poses provided in keyframes, demonstrating the importance of Aligned ROPE*



## 定位与知识库关联

### 1. 统一生成与编辑的范式演进

人体运动生成领域长期处于“一任务一模型”的碎片化状态。文本到运动生成主要依赖扩散模型（如 **MDM**、**MLD**）或自回归模型（如 **T2M-GPT**），轨迹可控生成则有 **OmniControl** 等专用方案，而运动编辑（**MotionFix**）、插值（**CondMDI**）和风格迁移（**MCM-LDM**）各自采用独立的架构设计。这种割裂带来的核心瓶颈在于：不同任务之间无法共享运动先验知识，每新增一种编辑需求就需要重新训练完整模型，导致实际部署效率低下且扩展性差。

MotionLab 的根本突破在于提出 **Motion-Condition-Motion 范式**（Table 2），将所有任务抽象为“源运动—条件—目标运动”三要素的组合。这一抽象使得文本生成（源运动=噪声，条件=文本）、轨迹生成（源运动=噪声，条件=轨迹）、运动编辑（源运动=待编辑运动，条件=编辑指令）、运动插值（源运动=起始帧，条件=关键帧约束）和风格迁移（源运动=内容运动，条件=风格运动）在数学上同构化，从而可以在单一框架内统一处理。

### 2. 生成框架的谱系定位：从扩散模型到修正流

MotionLab 的生成核心选择**修正流 (rectified flows)** 而非主流的扩散模型，这一选择具有明确的效率动机。扩散模型依赖随机微分方程（SDE）的逐步去噪，其轨迹基于 $x_t = \sqrt{1-\bar{\alpha}_t} x_0 + \sqrt{\bar{\alpha}_t} \epsilon$ 的非线性插值，导致速度场在时间上剧烈变化，需要大量推理步数（MDM 的 AITS 高达 26.04 秒）。相比之下，修正流假设线性轨迹 $x_t = (1-t)x_0 + t x_1$，速度场 $v_t = \frac{dx_t}{dt}$ 为常数，训练目标为最小化预测速度与真实速度的 L2 距离（Equation 3），这使得采样仅需少数欧拉步即可完成（Equation 2）。在 HumanML3D 文本生成任务上，MotionLab 的推理时间降至 0.068 秒，相比 MDM 加速约 380 倍（Table 3），同时保持了可比的生成质量。

在架构层面，MotionFlow Transformer (MFT) 继承自 **MM-DiT** 的多模态联合注意力设计，但针对运动生成进行了关键适配：为源运动、目标运动、文本、轨迹和风格等模态分配独立的模态路径，通过联合注意力实现跨模态交互。这一设计避免了为每个任务添加独立交叉注意力模块的冗余，使得模型容量在不同任务间共享。

### 3. 关键技术组件的创新定位

**Aligned ROPE** 解决了统一框架中多模态序列的时间对齐问题。传统方法通常使用绝对位置编码或三维 ROPE，但不同模态的序列长度和时间尺度差异显著（如文本 token 序列与运动帧序列）。Aligned ROPE 采用一维 ROPE 对各模态分别编码，确保相同时间步的跨模态 token 共享一致的位置信息。消融实验（Table 6, Table 10）表明，移除该组件后空间相关任务严重退化：轨迹生成平均误差从 0.0334 升至 0.0886，运动插值平均误差从 0.0273 升至 0.0756，验证了时间对齐对空间约束任务的关键作用。

**Task Instruction Modulation** 采用 CLIP 文本嵌入作为任务区分信号，替代了传统的 one-hot 编码或可学习任务标记。这一设计的优势在于：CLIP 嵌入蕴含丰富的语义信息，能够自然地编码任务之间的相似性（如“文本生成”与“文本编辑”在语义空间中的距离小于“文本生成”与“风格迁移”），从而促进相关任务间的知识迁移。消融实验（Table 9）证实 CLIP 嵌入在多项指标上优于 one-hot 和可学习标记。

**Motion Curriculum Learning** 是统一训练成功的关键使能技术。该策略采用“从易到难”的分阶段训练：预训练阶段仅使用文本生成任务学习运动先验，微调阶段逐步引入编辑、插值和风格迁移等多模态条件任务。移除课程学习后，文本生成 FID 从 0.167 飙升至 1.956（Table 6），表明直接混合训练会导致严重的任务间干扰和灾难性遗忘。这一发现揭示了多任务运动生成的核心挑战：不同任务的优化目标冲突（生成任务追求多样性，编辑任务追求精确可控），需要精心设计的训练策略来平衡。

### 4. 适用边界与局限

**文本生成性能的争议**：论文声称 MotionLab 在文本生成上取得“最低 FID”，但 Table 3 数据显示 T2M-GPT 的 FID 为 0.116，低于 MotionLab 的 0.167。这一矛盾可能源于指标计算方式或评估设置的差异，需手动核实。若 T2M-GPT 确实更优，说明自回归模型在纯文本生成任务上仍具优势，MotionLab 的统一性可能以轻微牺牲单一任务最优性为代价。

**运动编辑的基线偏差**：运动编辑任务中，基线 TMED 被重新实现为 TMED* 以适应 HumanML3D 格式（Table 5 注释），这一适配可能引入偏差，使得对比的公平性存疑。

**训练成本**：MotionLab 的训练需要 4×RTX 4090D 和约 4 天时间，对于资源受限的研究团队构成一定门槛。课程学习的多阶段训练进一步增加了调参复杂度。

### 5. 开放问题

1. **任务顺序的敏感性**：课程学习中任务引入顺序的选择是否影响最终性能？是否存在更优的顺序（如先生成后编辑 vs. 先空间后语义）？论文未对此进行消融。

2. **模态扩展能力**：当前框架覆盖文本、轨迹、关键帧和风格四种条件，能否扩展至音频驱动、视频驱动或物理仿真约束等更复杂的条件模态？新增模态是否需要重新设计课程学习策略？

3. **实时场景适用性**：尽管推理速度已大幅提升（0.068 秒），但在需要毫秒级响应的实时交互场景（如 VR 中的实时运动编辑）中是否足够？模型压缩或蒸馏是否可行？

4. **评估指标的统一性**：不同任务使用不同的评估指标（FID、R@3、平均误差、关键帧误差），缺乏跨任务的可比性度量，难以量化统一框架相对于专用模型的整体性能折衷。



## 原文 PDF

![[paperPDFs/ICCV_2025/MotionLab_Unified_Human_Motion_Generation_and_Editing_via_the_Motion_Condition_Motion_Paradigm.pdf]]
