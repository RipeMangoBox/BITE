---
title: "MotionCraft: Crafting Whole-Body Motion with Plug-and-Play Multimodal Controls"
type: paper
paper_level: A
venue: AAAI
year: 2025
pdf_ref: paperPDFs/AAAI_2025/MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Controls.pdf
project_link: https://cure-lab.github.io/MotionCraft
code_link: null
aliases:
- MotionCraft
tags:
- AAAI_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: MC-Attn模块中并行建模的静态人体骨架图（捕获基本结构）和动态拓扑关系图（适应场景偏移），结合两阶段粗到细训练策略（第一阶段文本语义预训练，第二阶段冻结主干添加控制分支）。
primary_logic: 人体运动知识可以通过静态和动态拓扑图进行分解与跨场景泛化；采用两阶段训练解耦粗粒度语义和细粒度低层控制，可避免混合训练的优化冲突，并实现即插即用的多模态控制。
claims:
- 在MC-Bench的HumanML3D子集上，MotionCraft-Mix的FID达到6.707，显著优于所有对比方法（最佳基线FineMoGen的FID为7.323）。
- MotionCraft-Mix在原始HumanML3D基准上取得Top-1 R Precision 0.501，超过其他SOTA方法。
- 消融实验证明，仅建模静态拓扑可在跨任务上提升泛化性，但联合建模静态和动态拓扑在所有任务上均取得最优性能。
- 模型规模从77M扩展到478M后性能先升后降，最佳配置为MotionCraft-all（4层，198M参数）。
---

# MotionCraft: Crafting Whole-Body Motion with Plug-and-Play Multimodal Controls

> [!tip] 核心洞察
> 人体运动知识可以通过静态和动态拓扑图进行分解与跨场景泛化；采用两阶段训练解耦粗粒度语义和细粒度低层控制，可避免混合训练的优化冲突，并实现即插即用的多模态控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionCraft：通过即插即用多模态控制生成全身运动 |
| 英文题名 | MotionCraft: Crafting Whole-Body Motion with Plug-and-Play Multimodal Controls |
| 会议/期刊 | AAAI 2025 |
| Links | [Project](https://cure-lab.github.io/MotionCraft) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MotionCraft |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D (whole-body SMPL-X, MC-Bench) 上，FID↓ 6.707 (MotionCraft-Mix) vs 7.323 (FineMoGen) (-0.616)；Top-1 R Precision↑ 0.600 (MotionCraft-Mix) vs 0.565 (FineMoGen) (+0.035)。
> - HumanML3D (original body-only format) 上，Top-1 R Precision↑ 0.501 (MotionCraft-Basic) vs 0.504 (FineMoGen) (-0.003)。

## 概要

运动生成领域长期面临一个核心瓶颈：**不同生成任务之间存在显著的分布漂移**。文本到运动（T2M）、语音到手势（S2G）和音乐到舞蹈（M2D）等场景的运动数据在潜在空间中呈现出截然不同的分布（见Figure 2 t-SNE可视化），导致在单一模型中混合训练多模态条件时，粗粒度的文本语义与细粒度的语音/音乐低层控制信号产生优化冲突。现有方法要么针对单一任务设计，要么在融合多模态信号时缺乏对跨场景运动知识迁移的有效建模。

MotionCraft 针对这一瓶颈提出了**两阶段粗到细的即插即用多模态控制框架**。其核心洞察在于：人体运动知识可以通过静态骨架拓扑和动态关系拓扑进行分解与跨场景泛化。具体而言，第一阶段利用文本作为粗粒度语义引导，在多个数据集的全身运动数据上进行预训练，使模型习得跨场景的运动先验；第二阶段冻结主干网络，通过零初始化线性桥接添加可插拔的控制分支，独立学习不同模态的低层控制信号，从而避免混合训练的优化冲突。

方法的关键调控机制是 **MC-Attn** 模块，它并行建模三类信息：（1）可学习的静态骨架图，捕获人体关节的基本结构关系；（2）基于注意力的动态拓扑图，适应不同场景下的运动分布偏移；（3）时间注意力，融合文本语义与运动时序信息。这种设计使模型在跨任务泛化中兼具稳定性和灵活性。

在实验验证方面，MotionCraft 在 MC-Bench 的 HumanML3D 子集上取得了 **FID 6.707**，显著优于最佳基线 FineMoGen 的 7.323（Table 2）；在原始 HumanML3D 基准上，Top-1 R Precision 达到 0.501，与 SOTA 方法持平或超越（Table 5）。消融实验进一步证实，联合建模静态与动态拓扑在所有任务上均取得最优性能，而仅建模静态拓扑虽在跨任务上有所提升，但在 T2M 上略有下降（Table 4a）。模型规模从 77M 扩展到 478M 后性能呈先升后降趋势，最优配置为 4 层、198M 参数的 MotionCraft-all（Table 4b）。

在方法谱系中，MotionCraft 区别于 **T2M-GPT**（Zhang et al., 2023b）、**MDM**（Tevet et al., 2023）等单一任务方法，以及 **MCM**（Ling et al., 2023）、**Motion-Verse**（Zhang et al., 2024b）等现有多模态方法。其核心差异在于：不将多模态信号映射至统一潜在空间进行联合建模，而是通过冻结主干加控制分支的方式实现真正的即插即用；同时首次在多模态运动生成中显式建模静态与动态人体拓扑图，以对抗分布漂移。

当前方法的主要局限包括：缺乏帧级或细粒度的全身文本描述（尤其在 S2G 和 M2D 任务中只能使用伪文本标注）；SMPL-X 轴角表示中根旋转和根轨迹的 6D 参数影响训练稳定性；模型规模扩展受限于带标注的多模态运动数据量。这些方向为后续研究提供了明确的改进空间。

### 问题背景

人体运动生成是计算机视觉与图形学领域的核心问题，涵盖文本到运动（Text-to-Motion, T2M）、语音到手势（Speech-to-Gesture, S2G）和音乐到舞蹈（Music-to-Dance, M2D）等多个子任务。这些任务共享一个共同目标：根据给定的控制信号生成逼真、多样化且语义一致的全身运动序列。然而，现有方法通常将每个子任务视为独立问题，设计专门的模型架构和训练策略，缺乏统一的生成框架。

近年来，扩散模型和Transformer架构在运动生成领域取得了显著进展。代表性方法包括：
- **MDM**（Tevet et al., 2023）：基于扩散的文本到运动生成框架；
- **T2M-GPT**（Zhang et al., 2023b）：将运动生成建模为序列预测任务；
- **MotionDiffuse**（Zhang et al., 2024a）：引入文本引导的扩散过程；
- **FineMoGen**（Zhang et al., 2023c）：通过细粒度控制提升生成质量；
- **MCM**（Ling et al., 2023）和**Motion-Verse**（Zhang et al., 2024b）：尝试多模态运动生成；
- **Talkshow**（Yi et al., 2023）和**EMAGE**（Liu et al., 2024a）：专注语音到手势生成。

尽管这些方法在各自任务上取得了可观效果，但在构建统一的多模态全身运动生成系统时仍面临根本性挑战。

### 核心瓶颈：分布漂移与优化冲突

MotionCraft的核心洞察建立在两个关键观察之上：

**观察一：跨任务运动分布漂移。** 如Figure 2的t-SNE可视化所示，不同生成任务（T2M、S2G、M2D）的运动数据在潜在空间中呈现显著的分布差异。这种分布漂移意味着，简单地将多任务数据混合训练会导致模型难以学习统一的运动表征，因为不同场景下的运动模式、关注的身体部位和动态特性存在本质区别。

**观察二：多粒度控制信号的优化冲突。** 文本提供的是粗粒度语义控制（如“一个人向前走并挥手”），而语音和音乐提供的是细粒度的低层时序控制（如节奏、韵律对应的手势或舞蹈动作）。当这些不同粒度的控制信号在端到端训练中被混合建模时，优化目标相互干扰：粗粒度语义学习需要抽象全局特征，而细粒度控制要求精确的局部时序对齐。

### 现有方法缺口

Table 1系统对比了MotionCraft与先前方法的能力差异，揭示了现有方法的三个主要缺口：

1. **缺乏跨场景拓扑知识迁移机制。** 现有方法要么为每个任务设计独立模型，要么在共享潜在空间中简单混合多模态信号（如ImageBind或Transformer token嵌入），但均未显式建模人体运动的拓扑结构如何在静态骨架约束和动态交互关系两个层面进行跨场景泛化。

2. **无法实现即插即用的多模态控制。** 多模态方法如MCM和Motion-Verse虽然支持多种控制信号，但其条件融合方式要求所有模态在训练时同时可用，无法灵活添加新的控制模态而不影响已有能力。

3. **数据格式不统一。** 不同任务使用不同的运动表示格式（Rot6D、SMPL、SMPL-X），缺乏统一的全身运动基准，阻碍了跨任务知识共享和公平比较。

### 本文动机

基于上述分析，MotionCraft的动机可以归纳为三个层次：

**核心动机：** 人体运动知识可以通过静态骨架拓扑和动态交互拓扑进行分解，这种分解具有跨场景的泛化性。静态拓扑（如关节连接关系）在所有任务中保持一致，而动态拓扑（如不同动作下的关节协同模式）随场景变化但遵循可学习的规律。

**方法动机：** 采用两阶段粗到细训练策略，将粗粒度语义学习和细粒度低层控制解耦，可以避免混合训练的优化冲突。第一阶段专注于文本到运动的语义预训练，建立跨场景的运动知识基础；第二阶段通过冻结主干并添加即插即用的控制分支，实现对新模态的高效适应。

**应用动机：** 构建统一的全身运动基准MC-Bench，将所有数据转换为SMPL-X轴角格式，为跨任务运动生成研究提供标准化评估平台，并支持未来新控制模态的灵活扩展。

## 核心方法与创新机理

MotionCraft 的核心创新在于**通过可分解的人体拓扑知识实现跨场景运动生成的泛化**，并采用**两阶段粗到细训练策略**解耦不同粒度的控制信号。与现有方法相比，其关键改进体现在以下三个维度的“changed slots”上。

### 1. MC-Attn：静态骨架图与动态拓扑图的并行建模

传统运动生成方法（如 **MDM** (Tevet et al., 2023)、**T2M-GPT** (Zhang et al., 2023b)）通常采用标准自注意力或动态注意力机制，难以显式捕获人体骨架的固有结构约束与跨场景的拓扑变化。MotionCraft 设计的 **MC-Attn** 模块首次在扩散Transformer中并行建模两类互补的拓扑知识：

- **静态骨架图学习器（Static-Skeleton Graph Learner）**：以对角单位矩阵初始化可学习邻接矩阵 $\mathbf{A}_s \in \mathbb{R}^{N_b \times N_b}$，输出 $\mathbf{E}_s = \hat{\mathbf{A}}_s \cdot \mathbf{H}_s$。该分支捕获人体骨架的基本连接关系，为跨场景运动生成提供稳定的结构先验。
- **动态拓扑图学习器（Dynamic-Topology Graph Learner）**：基于注意力动态计算邻接矩阵 $\mathbf{A}_d$，输出 $\mathbf{E}_d = \mathbf{A}_d \cdot \mathbf{H}_d$。该分支自适应地建模不同生成任务（T2M、S2G、M2D）中关节间的动态关联，以应对运动分布漂移（如 Figure 2 的 t-SNE 可视化所示）。
- **时间注意力（Temporal Attention）**：通过拼接运动与文本特征的键值对，融合粗粒度语义信息，输出 $\hat{\mathbf{E}_t}$。

最终 MC-Attn 的输出为三者的和：$\mathbf{E} = \mathbf{E}_s + \mathbf{E}_d + \mathbf{E}_t$。消融实验（Table 4a）证实：**仅建模静态拓扑可在 S2G 和 M2D 任务上大幅提升泛化性，仅建模动态拓扑几乎无增益，而联合建模两者在所有任务上均取得最优性能**。这验证了“静态骨架约束 + 动态拓扑适应”的互补机制是跨场景泛化的关键因果 knob。

### 2. 两阶段粗到细训练：解耦语义与低层控制

现有方法（如 **MCM** (Ling et al., 2023)、**Motion-Verse** (Zhang et al., 2024b)）通常将多模态信号映射至公共潜在空间进行端到端混合训练，导致不同粒度控制信号（粗粒度文本 vs. 细粒度语音/音乐）在优化时相互干扰。MotionCraft 采用两阶段策略实现解耦：

- **Stage 1：文本到运动语义预训练**。主干网络 $f_m(\cdot)$ 在 MC-Bench 的多场景文本-运动配对数据上学习粗粒度跨场景运动知识。
- **Stage 2：即插即用低层控制适配**。冻结 Stage 1 的主干，添加一个完整复制的主干副本作为控制分支，通过**零初始化线性桥接层（Zero-initialized Linear Bridge）** $W_p$ 将控制分支的逐层输出注入冻结主干。这一设计使新控制模态（如语音、音乐）可以即插即用，无需重新训练整个模型。

与 Motion-Verse 等将多模态信号统一嵌入 Transformer token 的方式相比，MotionCraft 的独立控制分支避免了不同模态间的优化冲突。Table 2 显示，MotionCraft-Mix 在 MC-Bench 的 HumanML3D 子集上 FID 达到 **6.707**，显著优于最佳基线 FineMoGen 的 7.323。

### 3. 局部解冻策略：保留全局拓扑知识的同时增强针对性生成

Stage 2 中，MotionCraft 可选择性地解冻与特定控制信号相关的身体部位编码器/解码器。例如，在语音到手势（S2G）任务中仅解冻手部和面部编码器/解码器，在音乐到舞蹈（M2D）任务中仅解冻手部。Table 6 的消融表明，完全解冻可增强特定部位生成质量，但部分解冻有助于保留 Stage 1 学到的全局拓扑知识，实现更好的整体平衡。这一“Local-Unfreeze”策略是 MotionCraft 在身体编码器/解码器微调上的独特设计。

### 4. 统一运动表示与基准：MC-Bench

为支撑跨场景训练，MotionCraft 构建了 **MC-Bench**，将所有数据统一转换为 SMPL-X 轴角格式，并对缺失部位进行填充。这解决了先前方法因数据格式不一致（Rot6D、SMPL、SMPL-X 混用）而无法联合训练的瓶颈。统一表示使 MC-Attn 的静态骨架图能够在不同数据集间共享，是实现拓扑知识迁移的基础设施保障。

**局限与待验证点**：当前 MC-Attn 中动态拓扑学习是否存在崩溃或错误收敛的失败案例，论文未提供明确分析，需进一步验证。此外，SMPL-X 轴角表示中根旋转和根轨迹的 6D 参数可能影响训练稳定性，作者已将其列为未来改进方向。

MotionCraft 是一个基于扩散 Transformer 的两阶段、粗到细多模态全身运动生成框架，其核心设计目标是在统一架构下支持文本、语音、音乐等多种控制信号的即插即用式生成。框架的整体信息流如下：

**输入层**：不同任务的控制信号（文本、语音、音乐）首先经过各自的模态编码器提取特征。文本条件由预训练语言模型编码为特征张量 $\mathbf{H}_{text} \in \mathbb{R}^{B \times \check{F}_t \times D_i}$，运动序列经身体部位编码器（Body-wise Encoder）编码为 $\mathbf{H}_{motion} \in \mathbb{R}^{B \times F_m \times D_m}$，其中 $B$ 为批次大小，$F_t$/$F_m$ 为文本/运动长度，$D_i$/$D_m$ 为特征维数。

**两分支架构**：框架采用主分支（Main Branch $f_m$）与控制分支（Control Branch）并行的双路结构。主分支负责粗粒度语义生成，以文本作为高层语义引导；控制分支是主分支的结构复制，在第二阶段作为即插即用的低层控制适配器添加，用于接收语音、音乐等细粒度控制信号。控制分支的输出通过**零初始化线性桥接层**（Zero-initialized Linear Bridge $W_p$）逐层注入冻结的主干网络，该零初始化策略确保在训练初期控制分支的输出不会干扰主干的已有语义知识，从而稳定连接。

**核心模块 MC-Attn**：主分支与控制分支共享相同的 MC-Attn 注意力模块，这是框架实现跨场景运动知识迁移的关键。MC-Attn 包含三个并行组件：
- **静态骨架图学习器**：以可学习的邻接矩阵 $\hat{\mathbf{A}}_s$（对角初始化）与顶点表示 $\mathbf{H}_s$ 相乘，输出 $\mathbf{E}_s = \hat{\mathbf{A}}_s \cdot \mathbf{H}_s$，捕获人体骨架的基本结构先验。
- **动态拓扑图学习器**：基于注意力机制动态构建邻接矩阵 $\mathbf{A}_d$ 与顶点表示 $\mathbf{H}_d$，输出 $\mathbf{E}_d = \mathbf{A}_d \cdot \mathbf{H}_d$，适应不同生成场景下的运动分布漂移。
- **时间注意力**：通过拼接运动序列与文本特征的键值对进行跨模态融合，输出 $\hat{\mathbf{E}_t}$，建模帧间时序依赖。

三个分支的输出以残差方式融合为最终表示 $\mathbf{E} = \mathbf{E}_s + \mathbf{E}_d + \mathbf{E}_t$。

**两阶段训练流程**：
1. **第一阶段——文本到运动语义预训练**：仅训练主分支 $f_m$，使用 MC-Bench 中来自多场景的文本-运动配对数据，让模型学习跨场景的粗粒度运动语义知识。
2. **第二阶段——多模态低层控制适配**：冻结主分支全部参数，添加控制分支（主分支的复制）及零初始化线性桥接层，仅训练控制分支和桥接层，使模型在保留第一阶段语义能力的同时，习得不同模态的低层控制信号。针对特定生成场景，还可选择性地解冻与对应控制信号相关的身体部位编码器/解码器（如语音到手势任务中解冻手部和面部编解码器），在保留全局拓扑知识的同时增强局部生成质量。

**输出层**：经多步扩散去噪后，身体部位解码器（Body-wise Decoder）将特征解码为统一的 SMPL-X 轴角格式全身姿态表示 $\mathbf{m}_i = \{ \dot{r}^r, \dot{r}^t, \theta^r, \mathbf{f}^s, \mathbf{f}^e, \theta^j, \theta^b \}$，包含根旋转、根轨迹、局部关节旋转、面部形状、面部表情、颌旋转及体型参数，实现全身运动的统一生成。

![[assets/figures/papers/paper_list_l1824_MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Con/figures/004_Figure_3.jpg]]
*Figure 3: Architecture of MotionCraft. MotionCraft is a transformer-based diffusion model. In the first stage, MotionCraft uses text as a semantic control guide to learn coarse-grained cross-scenario motion knowledge across multiple datasets; in the second stage, MotionCraft freezes the backbone while adding a plug-and-play control branch to learn the different low-level control signals. The core of MotionCraft is*

### 全身运动表示

MotionCraft 将所有运动数据统一转换为 SMPL-X 轴角格式，第 $i$ 帧的全身姿态定义为：

$$
\mathbf{m}_i = \{ \dot{r}^r, \dot{r}^t, \theta^r, \mathbf{f}^s, \mathbf{f}^e, \theta^j, \theta^b \}
$$

其中各分量含义：$\dot{r}^r$ 为根轴角旋转，$\dot{r}^t$ 为根轨迹，$\theta^r$ 为局部关节轴角，$\mathbf{f}^s$ 为面部形状，$\mathbf{f}^e$ 为面部表情，$\theta^j$ 为颌旋转，$\theta^b$ 为体型参数。这一统一表示是 MC-Bench 构建的基础，使不同任务（T2M、S2G、M2D）的数据能够在同一框架下联合训练。

### 两阶段粗到细框架

**第一阶段：文本到运动语义预训练。** 主干网络 $f_m(\cdot)$ 以文本条件特征 $\mathbf{H}_{text} \in \mathbb{R}^{B \times \check{F}_t \times D_i}$ 和运动序列特征 $\mathbf{H}_{motion} \in \mathbb{R}^{B \times F_m \times D_m}$ 为输入，学习跨场景的粗粒度语义运动知识。其中 $B$ 为批次大小，$F_t$ 为文本 token 长度，$F_m$ 为运动帧数，$D_i$ 和 $D_m$ 分别为文本与运动的特征维度。

**第二阶段：多模态低层控制适配。** 冻结第一阶段预训练的主干，添加一个复制分支作为即插即用的低层控制适配器（如语音或音乐控制）。通过零初始化线性桥接层 $W_p$ 将控制分支的逐层输出注入冻结主干，避免训练初期破坏已学到的语义知识。该设计使新模态控制信号的加入无需重新训练整个模型。

### MC-Attn 核心模块

MC-Attn 是 MotionCraft 的核心注意力模块，包含三个并行组件：静态骨架图学习器、动态拓扑关系图学习器和时间注意力，分别建模运动的空间静态结构、空间动态关系和时间依赖。

**静态骨架图学习器** 使用可学习的邻接矩阵 $\hat{\mathbf{A}}_s$（初始化为对角单位矩阵）捕获人体骨架的基本结构连接，其输出为：

$$
\mathbf{E}_s = \hat{\mathbf{A}}_s \cdot \mathbf{H}_s
$$

其中 $\mathbf{H}_s$ 为静态图顶点表示。该模块提供了跨场景泛化的基础拓扑先验。

**动态拓扑图学习器** 基于注意力机制构建动态邻接矩阵 $\mathbf{A}_d$，适应不同运动场景下的关节协同变化，输出为：

$$
\mathbf{E}_d = \mathbf{A}_d \cdot \mathbf{H}_d
$$

其中 $\mathbf{H}_d$ 为动态顶点表示。该模块使模型能够灵活捕捉运动分布漂移下的拓扑关系变化。

**时间注意力** 通过拼接运动与文本的键值对，融合时序动态与语义信息：

$$
\hat{\mathbf{E}_t} = \mathrm{Softmax}\left(\mathbf{Q}_{H_t}[\mathbf{K}_{H_t}^T, \mathbf{K}_{H_{text}}^T] / \sqrt{D_b}\right) \cdot [\mathbf{V}_{H_t}^T, \mathbf{V}_{H_{text}}^T]
$$

其中 $\mathbf{Q}_{H_t}$ 为时间查询，$\mathbf{K}_{H_t}$、$\mathbf{V}_{H_t}$ 和 $\mathbf{K}_{H_{text}}$、$\mathbf{V}_{H_{text}}$ 分别为运动和文本的键值对，$D_b$ 为缩放因子。

**MC-Attn 最终输出** 为三个分支的求和：

$$
\mathbf{E} = \mathbf{E}_s + \mathbf{E}_d + \mathbf{E}_t
$$

消融实验（Table 4a）证实：仅建模静态拓扑可在 S2G 和 M2D 上大幅提升性能，但联合建模静态与动态拓扑在所有任务上均取得最优，验证了分解人体运动知识为静态结构和动态关系两条路径的有效性。

### 身体部位编码器/解码器

MotionCraft 将身体拓扑划分为 12 个部位，每个部位使用隐编码维度 64 的独立编码器/解码器。第二阶段可选择局部解冻与特定控制信号相关的身体部位编码器/解码器（如 S2G 任务解冻手部和面部，M2D 任务解冻手部），在保留第一阶段全局拓扑知识的同时增强针对性生成质量（Table 6）。

### 评估用检索模型训练目标

用于评估的文本-运动检索模型采用多损失联合训练：

$$
\min \mathcal{L}_{rec} + \lambda_{KL} \mathcal{L}_{KL} + \lambda_{E} \mathcal{L}_{E} + \lambda_{NCE} \mathcal{L}_{NCE}
$$

其中 $\mathcal{L}_{rec}$ 为重构损失，$\mathcal{L}_{KL}$ 为 KL 散度，$\mathcal{L}_{E}$ 为跨模态相似度损失，$\mathcal{L}_{NCE}$ 为 InfoNCE 对比损失。该检索模型用于计算 R-Precision 和 MM-Dist 等语义相关性指标。

## 实验与关键发现

### 核心瓶颈与实验设计逻辑

MotionCraft 的实验设计围绕一个核心观察展开：不同运动生成任务（文本到运动 T2M、语音到手势 S2G、音乐到舞蹈 M2D）之间存在显著的分布漂移。如 Figure 2 的 t-SNE 可视化所示，三种任务的运动潜在空间分布几乎不重叠，这解释了为何端到端混合训练容易导致优化混乱。实验评估的核心目标是验证两个因果调节变量——**MC-Attn 模块中静态骨架图与动态拓扑图的联合建模**，以及**两阶段粗到细训练策略**——能否有效缓解这一瓶颈。

为统一评估，作者构建了 MC-Bench 基准，将所有数据转换为 SMPL-X 轴角格式并填充缺失部位。实验涵盖两个模型变体：仅在 HumanML3D 子集上训练的 MotionCraft-Basic，以及在整个 MC-Bench 上训练的 MotionCraft-Mix。两者共享 4 层 Transformer 主干，身体拓扑划分为 12 部分，每部分隐藏编码维度为 64。

### 主实验结果

**文本到运动（T2M）。** 在 MC-Bench 的 HumanML3D 子集上（Table 2），MotionCraft-Mix 的 FID 达到 6.707，显著优于所有对比方法，包括此前最优的 FineMoGen（FID 7.323）。Top-1 R Precision 达到 0.600，同样领先 FineMoGen 的 0.565。MotionCraft-Mix 相比仅用子集训练的 MotionCraft-Basic 有显著提升，这直接验证了 MC-Attn 学到的拓扑知识可以跨场景泛化。

在原始 HumanML3D 基准上（Table 5），MotionCraft-Basic 的 Top-1 R Precision 为 0.501，与 FineMoGen 的 0.504 基本持平，但 FID 和多样性指标表现更优。这表明即使在单一任务设置下，MC-Attn 的静态-动态拓扑建模也能提供有竞争力的运动生成质量。

![[assets/figures/papers/paper_list_l1824_MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Con/figures/010_Table_5.jpg]]
*Table 5: Results of text-to-motion in origin HumanML3D benchmark. We compare the results of text-to-motion generation between ours and the SOTA methods. Our method achieves better semantic relevance, fidelity, and diversity performances. Red background indicates best results , yellow background indicates second best results*

**语音到手势（S2G）。** 在 BEAT2 数据集上（Table 3），MotionCraft 在手部 FID（$FID_H$）和全身 FID（$FID_B$）上均取得最优或次优结果，但面部 L2 损失方面略逊于专为 S2G 设计的 EMAGE 和 Talkshow。这一差距可能源于训练数据中面部数据的质量限制。

**音乐到舞蹈（M2D）。** 在 FineDance 数据集上（Table 3），MotionCraft 的 $FID_H$ 和 $FID_B$ 均达到最优。但需注意，FineDance 缺乏真实文本描述，所有方法在该任务上只能使用伪文本标注，这可能是 M2D 任务 FID 绝对值偏高的一个结构性原因。

### 消融实验

**MC-Attn 设计消融（Table 4a）。** 这是最关键的消融，直接验证了核心洞察：
- **仅建模静态拓扑**：在 S2G 和 M2D 上性能大幅提升，但在 T2M 上略有下降。这说明静态骨架结构知识对于跨场景泛化至关重要，但单独使用不足以覆盖所有任务。
- **仅建模动态拓扑**：几乎无增益，说明单纯依赖注意力驱动的动态关系无法提供稳定的拓扑先验。
- **联合建模静态与动态拓扑**：在所有任务上取得最优性能，证明两者的互补性——静态图提供基本结构锚点，动态图适应场景偏移。

**模型规模扩展（Table 4b）。** 从 77M 参数扩展到 478M 参数时，性能呈现先升后降的趋势。最佳配置为 MotionCraft-all（4 层，198M 参数）。这一现象与当前带标注多模态运动数据量有限的现实相符——模型规模超过数据所能支撑的复杂度时，反而出现过拟合或优化困难。

**第二阶段微调策略（Table 6）。** 完全解冻身体编码器/解码器可增强特定部位生成质量（如 S2G 的手部和面部、M2D 的手部），但部分解冻（Local-Unfreeze）有助于保留第一阶段学到的全局拓扑知识。这一发现为即插即用控制分支的实际部署提供了灵活的策略选择。

**时间建模范式（Table 6）。** 时间打块（Temporal-Patching）在所有任务上反而降低性能。作者推测这是因为 SMPL-X 轴角表示比一般时间序列更敏感，压缩相邻帧会引入显著的累积误差。这一发现提示，在运动生成任务中，逐帧建模可能是更安全的选择，尽管计算成本更高。

### 失败模式与局限性

1. **面部表达生成不足**：在 S2G 任务中，MotionCraft 的面部 L2 损失劣于 EMAGE 和 Talkshow。这与训练数据中面部数据的质量和数量直接相关，属于数据侧瓶颈而非方法缺陷。

2. **M2D 任务的文本缺失问题**：FineDance 数据集缺乏真实文本描述，所有方法被迫使用伪文本标注，这从根本上限制了语义对齐的评估可信度和生成保真度。

3. **根轨迹参数的不稳定性**：SMPL-X 轴角表示中根旋转和根轨迹的 6D 参数会影响训练稳定性，这是表示层面的固有局限，作者提出未来可引入投影 3D 关节点位置作为额外约束。

4. **模型规模扩展的天花板**：在有限的多模态运动数据下，模型规模扩展带来的收益递减，198M 参数即达到性能峰值，进一步扩大无法带来增益。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Figure 2 | 不同生成任务的运动分布存在显著漂移，是混合训练的核心瓶颈 |
| Table 2 | MotionCraft-Mix 在 MC-Bench T2M 任务上 FID 达 6.707，显著超越所有基线 |
| Table 3 | S2G 和 M2D 任务上取得最优或次优，面部表达受限于数据质量 |
| Table 4a | 静态+动态拓扑联合建模在所有任务上最优，单一动态拓扑几乎无增益 |
| Table 4b | 模型规模 198M 为最佳配置，继续扩展性能下降 |
| Table 5 | 原始 HumanML3D 基准上语义相关性、保真度和多样性均具竞争力 |
| Table 6 | 局部解冻优于完全冻结或完全解冻；时间打块降低性能 |

![[assets/figures/papers/paper_list_l1824_MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Con/figures/007_Table_3.jpg]]
*Table 3: Results of Speech-to-Gesture in BEAT2 and Music-to-Dance in FineDance of MC-Bench. We respectively evaluate the*

![[assets/figures/papers/paper_list_l1824_MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Con/figures/011_Table_6.jpg]]
*Table 6: Additional Ablation Study. we explored the second stage model training strategy about the body-wise encoder (decoder) and motion sequence temporal relationship modeling paradigm. The “Local-Unfreeze” column indicates that during the second phase, only specific body parts corresponding to certain control signals are unfrozen in the body-wise encoder and decoder. For instance, in the Speech-to-Gesture task, only the encoders and decoders for hands and face are unfrozen, while in Music-to-Dance, only the encoder and decoder for the hands are unfrozen. The ”Temporal-Patching” column means performing patching operations on adjacent frames, compressing a specified number of neighboring frames int...*

![[assets/figures/papers/paper_list_l1824_MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Con/figures/008_Table_4.jpg]]
*Table 4: Ablation Study. (a) Ablation on model design (Upper half). The results suggest that jointly modeling dynamic and static human skeleton topologies significantly improves performance since this provides robust topology knowledge against distribution drifts. (b) Ablation on scaling up impacts (Lower half). We design four scaling model variants, where*

![[assets/figures/papers/paper_list_l1824_MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Con/figures/002_Table_1.jpg]]
*Table 1: Comparison of MotionCraft with previous motion generation methods. MotionCraft jointly models the static human skeleton structure and dynamic human topology relationships to achieve flexible motion knowledge transfer across various whole-body generation scenarios, supporting plug-and-play with any new control signal modality*

## 定位与知识库关联

### 1. 与现有工作的关系

MotionCraft 处于多模态全身运动生成的交汇点，其设计思路与以下工作形成了明确的继承、对比或互补关系。

**文本到运动（T2M）基线。** 在 T2M 任务上，MotionCraft 直接对标的主流方法包括 **T2M-GPT** (Zhang et al., 2023b)、**MDM** (Tevet et al., 2023)、**MotionDiffuse** (Zhang et al., 2024a) 和 **FineMoGen** (Zhang et al., 2023c)。这些方法均采用单一的文本条件控制，在 HumanML3D 等标准基准上取得了有竞争力的结果。MotionCraft 在原始 HumanML3D 基准上的 Top-1 R Precision 达到 0.501，与 FineMoGen 的 0.504 基本持平（Table 5），表明其文本语义建模能力已达到 SOTA 水平。然而，这些方法无法处理语音、音乐等低层控制信号，且缺乏跨场景的运动知识迁移机制——这正是 MotionCraft 通过两阶段训练和 MC-Attn 所解决的核心问题。

**多模态运动生成基线。** 在多模态控制方面，**MCM** (Ling et al., 2023) 和 **Motion-Verse** (Zhang et al., 2024b) 是直接对比对象。MCM 采用多条件联合嵌入的方式，Motion-Verse 则引入了动态注意力机制。MotionCraft 与它们的关键差异在于控制分支的“即插即用”设计：通过零初始化线性桥接（$W_p$）将第二阶段添加的控制分支逐层注入冻结的主干，而非将所有模态映射到同一潜在空间进行联合建模。这种解耦策略避免了不同粒度控制信号（粗粒度文本 vs. 细粒度语音/音乐）在混合训练时的优化冲突，是 MotionCraft 在跨任务泛化上优于 MCM 和 Motion-Verse 的结构性原因（Table 1 对比了各方法的能力矩阵）。

**语音到手势（S2G）与音乐到舞蹈（M2D）基线。** 在 S2G 任务上，MotionCraft 与 **Talkshow** (Yi et al., 2023) 和 **EMAGE** (Liu et al., 2024a) 进行了对比。在 M2D 任务上，对比基线包括 **Edge**（文献未提供完整引用，需人工核实）。在 MC-Bench 的 BEAT2 子集上，MotionCraft 在 FID$_H$、FID$_B$ 和 Beat Align Score 等指标上取得了最优或次优结果（Table 3）。值得注意的是，在面部表情生成质量上，MotionCraft 略逊于 EMAGE 和 Talkshow，这被归因于训练数据中面部数据的覆盖不足——这是一个数据驱动型局限，而非方法设计缺陷。

**知识库定位。** MotionCraft 的核心贡献在于提出了“静态骨架图 + 动态拓扑图”的并行建模范式（MC-Attn），这是首次在多模态运动生成中显式分解并联合学习人体的结构先验与场景自适应关系。与仅依赖自注意力或动态注意力的现有方法不同，MC-Attn 中的静态骨架图学习器使用对角初始化的可学习邻接矩阵 $\hat{\mathbf{A}}_s$，捕获与场景无关的人体基本连接结构；动态拓扑图学习器则通过基于注意力的邻接矩阵 $\mathbf{A}_d$ 适应不同生成场景下的关节协同关系。消融实验（Table 4a）提供了决定性证据：仅建模静态拓扑可在跨任务上提升泛化性，仅建模动态拓扑几乎无增益，而联合建模两者在所有任务上均取得最优性能。这一发现揭示了人体运动知识可被分解为“场景不变的骨架约束”与“场景自适应的拓扑关系”两个可迁移组件，为后续的多任务运动生成提供了可复用的知识分解范式。

### 2. 适用边界

**数据格式统一的前提。** MotionCraft 的有效性依赖于 MC-Bench 的数据预处理流水线：将不同来源的运动数据统一转换为 SMPL-X 轴角格式，并对缺失的身体部位进行填充。这一步骤消除了数据格式层面的分布差异，但同时也引入了轴角表示的固有问题——根旋转和根轨迹的 6D 参数会影响训练稳定性（见论文 limitations）。若下游应用使用 Rot6D 或关节位置等其他表示，需要额外的转换步骤，且可能损失 MotionCraft 在轴角空间中学到的拓扑知识。

**文本条件质量的依赖。** 在 Stage 1 的文本到运动语义预训练中，模型依赖文本描述来学习粗粒度的跨场景运动知识。然而，在 S2G 和 M2D 任务中，FineDance 等数据集缺乏真实的帧级文本描述，目前只能使用伪文本标注。这限制了 Stage 1 预训练在这些场景下的语义对齐质量，进而影响 Stage 2 低层控制分支的起点。论文明确指出这是当前的主要局限之一。

**模型规模与数据量的匹配。** 规模扩展实验（Table 4b）显示了一个“先升后降”的性能趋势：模型参数从 77M 扩展到 198M（4 层，12 身体部位，编码维度 64）时性能提升，但进一步扩展到 478M 后性能反而下降。这表明在带标注的多模态运动数据量有限的情况下，盲目扩大模型规模不会带来收益，甚至可能因过拟合或优化困难而损害泛化性。因此，MotionCraft 的最佳配置与当前可用数据规模紧密耦合。

**时间打块的失效。** 消融实验（Table 6）揭示了一个重要的适用边界：在 SMPL-X 轴角表示下，对相邻帧进行时间打块（Temporal-Patching）会降低性能，而非像在一般时间序列中那样提升效率。论文推测这是因为 SMPL-X 轴角表示比一般时间序列更敏感，压缩子序列会引入显著的累积误差。这意味着 MotionCraft 的设计选择——按帧建模而非时间打块——是其有效性的必要条件，也暗示该框架可能不适用于需要长程时间压缩的场景。

### 3. 局限与开放问题

**数据层面的局限。** 最突出的局限是缺乏高质量帧级或细粒度的全身文本描述，尤其在 S2G 和 M2D 任务中。这导致 Stage 1 的语义预训练在这些场景下只能依赖伪标注，限制了文本-运动对齐的上限。一个直接的开放问题是：如何为 S2G 和 M2D 任务引入可靠的帧级或细粒度文本描述？可能的路径包括利用多模态大模型自动生成描述，或设计弱监督的对齐学习策略。

**训练稳定性的改进空间。** 当前 SMPL-X 轴角表示中根旋转和根轨迹的 6D 参数会影响训练稳定性。论文提出未来可引入投影 3D 关节点位置作为额外约束。这引出一个可验证的开放问题：添加投影 3D 关节点位置能否有效稳定训练过程，同时不损害生成质量？

**动态拓扑学习的鲁棒性。** 尽管 MC-Attn 中的动态拓扑图学习器在消融实验中与静态图联合使用时效果显著，但其单独使用时的增益几乎为零（Table 4a）。这暗示动态拓扑学习可能存在崩溃或错误收敛的失败模式——当缺乏静态骨架先验的锚定作用时，基于注意力的动态邻接矩阵可能无法学到有意义的关节关系。一个值得探索的开放问题是：能否通过更好的初始化策略或正则化项（如稀疏性约束、对称性先验）来提升动态拓扑学习的独立有效性？

**时间打块失效的深层原因。** 为什么在运动序列中时间打块反而降低性能？论文推测与 SMPL-X 轴角表示的特殊耦合有关，但这一现象的具体机制尚不明确。如果轴角表示中各关节参数的相互依赖使得帧间压缩破坏了运动学一致性，那么这一发现可能对更广泛的运动建模范式（如基于 VQ-VAE 的离散化方法）具有警示意义。

**跨任务泛化的上限。** 在有限的运动数据下，模型规模扩展已触及收益递减的拐点。一个根本性的开放问题是：在数据量不变的约束下，如何进一步提升大规模模型的跨任务泛化能力？可能的探索方向包括更高效的数据增强策略、元学习框架下的任务自适应微调，或引入物理仿真器作为额外的监督信号。

## 原文 PDF

![[paperPDFs/AAAI_2025/MotionCraft_Crafting_Whole_Body_Motion_with_Plug_and_Play_Multimodal_Controls.pdf]]
