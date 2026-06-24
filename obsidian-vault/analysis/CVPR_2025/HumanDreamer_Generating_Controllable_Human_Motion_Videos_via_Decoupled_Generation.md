---
title: "HumanDreamer: Generating Controllable Human Motion Videos via Decoupled Generation"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_Generation.pdf
aliases:
- HumanDreamer
tags:
- CVPR_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "将生成过程解耦为Text-to-Pose和Pose-to-Video两步，利用MotionDiT（含局部特征聚合与全局注意力）和LAMA损失增强文本到结构化姿态的生成，再通过姿态引导视频生成。"
primary_logic: "文本→姿态的映射比文本→像素更易学习；先生成符合文本的结构化2D姿态，再以此作为明确先验驱动视频生成，可大幅降低建模难度，同时兼顾控制灵活性与生成质量。"
claims:
- "解耦 + MotionDiT + LAMA 相较于最强基线在FID上实现62.4%的相对改进，R-precision Top-1提升41.8%，证明Text-to-Pose质量显著提高。"
- "消融实验中，逐步加入局部聚合、全局注意力和LAMA损失，FID从283.091持续降至149.007，R-precision和Diversity同步提升，说明每个组件都不可或缺。"
- "在Text-to-Video整体比较中，HumanDreamer的Sensory Quality (0.938 vs 0.531) 和Instruction Following (0.813 vs 0.688) 均远超CogVideoX，生成的视频运动幅度更大、更符合文本。"
- "MotionVid subset 上 FID = 149.007"
---

# HumanDreamer: Generating Controllable Human Motion Videos via Decoupled Generation

> [!tip] 核心洞察
> 文本→姿态的映射比文本→像素更易学习；先生成符合文本的结构化2D姿态，再以此作为明确先验驱动视频生成，可大幅降低建模难度，同时兼顾控制灵活性与生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | HumanDreamer：通过解耦生成实现可控人体运动视频生成 |
| 英文题名 | HumanDreamer: Generating Controllable Human Motion Videos via Decoupled Generation |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2412.02056) · [Project](https://humandreamer.github.io/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | HumanDreamer |
| Dataset | MotionVid subset, Pose-to-Video (MotionVid) |

> [!tip] 效果简介
> - MotionVid subset 上，FID 为 149.007，对比 MLD 396.949，变化 62.4% relative improvement。
> - MotionVid subset 上，Rp-top1 为 0.451，对比 MLD 0.318，变化 41.8% relative improvement。
> - MotionVid subset 上，Diversity 为 68.220，对比 MLD 64.442，变化 +3.778。

## 概述

**核心问题**：从文本直接生成人体运动视频面临巨大的搜索空间——模型需同时推断人体结构、运动时序与外观细节，导致动作不连贯、肢体扭曲且难以控制。现有姿态引导方法虽能改善可控性，却依赖已有视频提取姿态，丧失了文本驱动的灵活性。

**核心思路**：HumanDreamer 将这一难题解耦为两步——先由文本生成结构化的 2D 人体姿态序列（Text-to-Pose），再以该姿态为明确先验驱动视频生成（Pose-to-Video）。其关键洞察在于：文本→姿态的映射远比文本→像素的映射更易学习；先生成符合语义的骨架运动，再“填入”外观，可大幅降低建模难度，同时兼顾文本控制的灵活性与姿态引导的精确性。

**方法定位**：在 Text-to-Pose 阶段，HumanDreamer 提出 MotionDiT——一种在扩散 Transformer 中集成局部特征聚合与全局注意力的架构，并辅以 LAMA 损失（基于对比语言-运动预训练模型 CLoP 的语义对齐），强化生成姿态与文本描述的一致性。Pose-to-Video 阶段则采用潜在视频扩散模型，以参考图像和生成姿态为条件输出最终视频。训练数据源自大规模 2D 姿态数据集 MotionVid（约 120 万经严格清洗的文本-姿态对）。

**主要结果**：在 MotionVid 子集上，HumanDreamer 的 Text-to-Pose 相较最强基线 **MLD** 实现 FID 相对改进 62.4%，R-precision Top-1 提升 41.8%；消融实验证实局部聚合、全局注意力与 LAMA 损失三者缺一不可。整体 Text-to-Video 对比中，其感官质量（0.938 vs 0.531）与指令遵循度（0.813 vs 0.688）均远超 **CogVideoX**，生成的视频运动幅度更大、语义贴合度更高。

## 背景与动机

### 问题背景

生成逼真且可控的人体运动视频是计算机视觉与图形学中的核心挑战，在虚拟数字人、影视制作、增强现实等领域具有广泛的应用前景。近年来，文本到视频（Text-to-Video, T2V）生成模型取得了显著进展，然而在人体运动视频这一特定子任务上，现有方法仍面临根本性困难。

其核心瓶颈在于**直接文本到像素映射的搜索空间过大**。文本描述本身是高度抽象和语义化的，而人体运动视频需要在时间维度上保持精细的骨骼结构一致性、肢体运动连贯性以及外观细节的稳定性。将这两者直接耦合在一个端到端生成模型中，使得模型需要同时学习语言理解、人体结构先验和时空动态建模，导致生成质量差、动作不连贯、肢体扭曲等问题频发。

### 现有方法缺口

当前主流的人体运动视频生成方法可大致分为两类，但各自存在明显局限：

**第一类**是纯文本驱动的方法（如 CogVideoX、Mochi1），直接从文本描述生成视频。这类方法虽然具有较高的控制灵活性——用户只需提供自然语言描述即可——但由于缺乏对人体姿态的显式结构化约束，生成结果往往出现身体扭曲、运动连续性弱、面部细节缺失等问题。如 Figure 5 所示，CogVideoX 和 Mochi1 在复杂动作场景下难以维持人体结构的完整性。

**第二类**是基于姿态引导的方法（如 AnimateAnyone、MimicMotion、Animate-X），以给定的姿态序列作为条件来驱动视频生成。这类方法通过引入精确的姿态先验，显著提升了对人体结构的控制能力，但其致命缺陷在于**依赖已有的姿态序列作为输入**，缺乏从文本生成新姿态的灵活性。用户必须提供完整的姿态数据，无法仅通过文本描述自由创作运动内容。

换言之，现有方法在“文本控制的灵活性”与“姿态引导的可控性”之间存在无法调和的矛盾：纯文本方法灵活但不可控，姿态引导方法可控但不灵活。

### 核心洞察与动机

HumanDreamer 的核心洞察在于：**文本→姿态的映射比文本→像素的映射更容易学习**。文本描述本质上是对人体动作的语义刻画，而 2D 人体姿态正是这种语义的结构化表达。如果能够先生成符合文本描述的结构化 2D 姿态序列，再以此作为明确的空间-时间先验来驱动视频生成，就可以大幅降低建模难度，同时兼顾控制灵活性与生成质量。

基于这一洞察，HumanDreamer 提出**解耦生成**框架，将人体运动视频生成分解为两个阶段：
1. **Text-to-Pose**：从文本描述生成结构化 2D 人体姿态序列；
2. **Pose-to-Video**：以生成的姿态和参考图像为条件，通过潜在视频扩散模型生成最终的人体运动视频。

这一解耦设计的优势在于：Text-to-Pose 阶段专注于语义到结构的映射，搜索空间远小于直接像素生成；Pose-to-Video 阶段则继承了姿态引导方法的精确可控性，同时姿态本身由文本灵活生成，打破了传统姿态引导方法对已有姿态数据的依赖。

### 技术挑战

尽管解耦框架在概念上简洁，但 Text-to-Pose 阶段本身并非易事。从文本生成时间连贯、语义一致的人体姿态序列面临以下挑战：
- **局部细节捕获**：相邻关节（如肘部和腕部）之间存在强相关性，生成模型需要有效捕捉这些局部依赖；
- **全局连贯性**：整个姿态序列中，远距离帧之间的动作需要保持语义一致和物理合理；
- **文本-姿态语义对齐**：生成的姿态序列必须精确反映文本描述的语义内容，而非仅生成“看起来合理”但与文本无关的动作。

为此，HumanDreamer 在 Text-to-Pose 阶段引入了三项关键设计：**MotionDiT**（集成局部特征聚合与全局注意力机制的扩散 Transformer）、**CLoP**（对比语言-运动预训练模型）以及 **LAMA 损失**（潜在语义对齐损失），以系统性地解决上述挑战。这些技术细节将在后续章节中详细展开。

## 核心创新

HumanDreamer 的核心创新在于将人体运动视频生成分解为 **Text-to-Pose** 和 **Pose-to-Video** 两个解耦阶段，从根本上降低了直接文本到像素映射的搜索空间复杂度。在此基础上，方法引入了三个关键的 **changed slots**，共同构成了 Text-to-Pose 阶段的核心技术贡献。

### 解耦生成框架

传统文本到视频方法（如 **CogVideoX**）试图直接从文本描述映射到高维像素空间，导致人体运动不连贯、肢体扭曲等问题。HumanDreamer 的核心洞察是：**文本→姿态的映射远比文本→像素的映射更易学习**。通过先生成符合文本语义的结构化 2D 姿态序列，再以此作为明确的空间先验驱动视频生成，框架兼顾了文本控制的灵活性与姿态引导的可控性（Figure 1）。

### MotionDiT：面向姿态序列的扩散 Transformer

在 Text-to-Pose 阶段，HumanDreamer 设计了 **MotionDiT**，在标准 DiT 架构基础上引入了两个关键模块：

1.  **局部特征聚合（Local Feature Aggregation）**：在每个 MotionDiT 块中，先通过 1D ResNet 残差块处理姿态潜变量，再经空间自注意力增强相邻关节间的局部相关性（Equation 2）。该模块专门捕获人体运动中的局部细节，如关节间的协调关系。

2.  **全局注意力块（Global Attention Block）**：在网络中间层对所有帧和所有关键点应用全局自注意力，捕获远距离的姿态关联。这使得模型能够建模整个动作序列的全局连贯性，避免动作断裂或不自然过渡。

消融实验（Table 2）验证了这两个模块的独立贡献：从基础 DiT（FID 283.091）到加入局部聚合（FID 183.213），再到进一步加入全局注意力（FID 162.022），性能持续提升，且多模态得分（MM）从 41.890 跃升至 57.848，表明全局上下文对动作连贯性至关重要。

### LAMA 损失：潜在语义对齐

除了架构改进，HumanDreamer 引入了 **LAMA（Latent Semantic Alignment）损失**，这是第三个关键 changed slot。传统扩散模型仅使用噪声预测的 MSE 损失（Equation 4），缺乏对生成姿态与文本语义一致性的显式约束。

LAMA 损失的工作机制如下：
- 首先通过 **CLoP（对比语言-运动预训练）** 学习文本与姿态的联合嵌入空间（Equation 5），为语义对齐提供基座。
- 在 MotionDiT 训练过程中，将第 $l$ 层的潜变量经两层 MLP 投影后，与 CLoP 姿态特征计算特征对齐损失 $\mathcal{L}_f$（Equation 6）。
- 总损失为扩散降噪损失与 LAMA 损失的加权组合：$\mathcal{L} = \mathcal{L}_d + \lambda_f \mathcal{L}_f$（Equation 7）。

消融实验（Table 2）表明，加入 LAMA 损失后，FID 从 162.022 进一步降至 **149.007**，Rp-top1 达到最高 **0.451**，证明语义对齐损失对提升生成精度和文本一致性不可或缺。

### 创新总结

三个 changed slots 形成递进式改进：局部聚合捕获细节 → 全局注意力保障连贯 → LAMA 损失强化语义对齐。在 MotionVid 子集上，完整方法相较于最强基线 **MLD** 实现了 **FID 62.4% 的相对改进**和 **R-precision Top-1 41.8% 的提升**（Table 1），验证了每个创新组件的有效性。

## 整体框架

HumanDreamer 将人体运动视频生成解耦为两个串行阶段：**文本到姿态生成（Text-to-Pose）** 与 **姿态到视频生成（Pose-to-Video）**。这一设计的核心动机在于，文本→姿态的映射空间远小于文本→像素的直接映射空间，因此先学习结构化的 2D 人体姿态序列，再以其作为显式先验驱动视频生成，可以显著降低建模难度，同时兼顾文本控制的灵活性与姿态引导的可控性。

### 整体流程

整个框架的输入为一段描述人体动作的文本提示，输出为一段包含该动作的人体运动视频。流程如下：

1. **Text-to-Pose 阶段**：以文本为条件，通过 MotionDiT（一种扩散 Transformer）在 Pose VAE 的潜空间中生成与文本语义一致的 2D 人体姿态序列。该阶段还引入 CLoP 模型提供的 LAMA 损失，对生成过程中的潜变量进行语义对齐约束。
2. **Pose-to-Video 阶段**：以一张参考图像和第一阶段生成的姿态序列为条件，利用潜在视频扩散模型生成最终的人体运动视频。

Figure 1 给出了框架的整体示意，Figure 3 和 Figure 9 则分别展示了 Text-to-Pose 和 Pose-to-Video 的训练流水线。

![[assets/figures/papers/paper_list_l25_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_G/figures/003_Figure_3.jpg]]
*Figure 3: Training pipeline of the proposed Text-to-Pose generation. Pose data are encoded in latent space via the Pose VAE, which are then processed by the proposed MotionDiT, where local feature aggregation and global attention are utilized to capture information from the entire pose sequence. Finally, the LAMA loss is calculated via the proposed CLoP, which enhances the training of MotionDiT*

### 模块关系与数据流

各核心模块在 Pipeline 中的角色与连接关系如下：

- **Pose VAE**：将 2D 人体姿态序列编码到低维潜空间，并支持从潜变量解码重建姿态。其作用是为 MotionDiT 提供一个紧凑、可微分的生成空间。
- **MotionDiT**：扩散 Transformer，接收文本条件与噪声潜变量，在 Pose VAE 的潜空间中迭代去噪，生成目标姿态潜变量。MotionDiT 内部集成了局部特征聚合（Local Feature Aggregation）和全局注意力块（Global Attention Block），分别用于捕获相邻关节的局部相关性和全序列帧间的远距离依赖。
- **CLoP**：对比语言-运动预训练模型，为 LAMA 损失提供语义对齐基座。CLoP 将文本和姿态映射到共享特征空间，LAMA 损失则约束 MotionDiT 中间层潜变量的投影与 CLoP 姿态特征之间的一致性。
- **Pose-to-Video 模型**：以参考图像和生成的 2D 姿态序列为条件，通过潜在视频扩散生成最终视频。该模块本身不是 HumanDreamer 的核心贡献，但作为下游组件，其性能会影响最终视频质量。

数据流可概括为：文本 → MotionDiT（在 Pose VAE 潜空间中）→ 2D 姿态序列 → Pose-to-Video 模型 → 输出视频。CLoP 仅在训练阶段介入，通过 LAMA 损失对 MotionDiT 进行语义监督。

### 设计依据与证据强度

解耦策略的有效性得到了多组实验的验证。在 Text-to-Pose 阶段，HumanDreamer 在 MotionVid 子集上的 FID 达到 149.007，相比最强基线 MLD 的 396.949 实现了 62.4% 的相对改进；R-precision Top-1 从 0.318 提升至 0.451，相对提升 41.8%（Table 1）。在整体 Text-to-Video 评估中，HumanDreamer 的 Sensory Quality（0.938 vs. CogVideoX 的 0.531）和 Instruction Following（0.813 vs. 0.688）均显著领先（Table 7），表明解耦框架在视频质量和指令遵循方面均具有明显优势。以上证据的可信度均较高（confidence ≥ 0.95）。

## 核心模块与公式推导

HumanDreamer 的 Text-to-Pose 阶段由三个核心模块构成：**Pose VAE**、**MotionDiT** 和 **CLoP**，三者协同完成从文本到结构化 2D 姿态序列的生成。

### Pose VAE：姿态潜空间编解码

为降低扩散模型在高维姿态序列上的计算开销，Pose VAE 将 2D 姿态序列压缩至低维潜空间。给定姿态序列 $\mathbf{p}$，编码器 $\mathcal{E}$ 将其映射为潜变量，解码器则负责重建：

$$l_{p} = \mathcal{F}_{\mathrm{Patch}}(\mathcal{E}(\mathbf{p})) \quad \text{(Equation 1)}$$

其中 $\mathcal{F}_{\mathrm{Patch}}$ 为补丁嵌入操作，将编码后的潜变量转换为适合 Transformer 处理的序列形式。VAE 的训练目标由重建损失和 KL 散度组成：

$$\mathcal{L}_{\mathrm{VAE}} = \mathcal{L}_{\mathrm{R}} + \beta \mathcal{L}_{\mathrm{KL}} \quad \text{(Equation 11)}$$

$$L_{\mathrm{R}} = \| \mathbf{p} - \mathbf{p}_r \|_2^2 \quad \text{(Equation 12)}$$

$$L_{\mathrm{KL}} = \frac{1}{2} \sum_{i=1}^{k} \left( \sigma_i^2 + \mu_i^2 - \log(\sigma_i^2) - 1 \right) \quad \text{(Equation 13)}$$

$\mathcal{L}_{\mathrm{R}}$ 约束输入姿态 $\mathbf{p}$ 与重建姿态 $\mathbf{p}_r$ 的逐点一致性，$\mathcal{L}_{\mathrm{KL}}$ 则促使潜变量分布逼近标准正态先验，$\beta$ 为权衡超参数。

### MotionDiT：局部-全局联合建模的扩散 Transformer

MotionDiT 是 Text-to-Pose 生成的核心扩散骨干，其关键创新在于同时捕获姿态序列的**局部关节相关性**和**全局时序依赖性**。

**局部特征聚合**：在每个 DiT 块中，先通过 1D ResNet 残差块处理潜变量，再施加空间自注意力以增强相邻关节间的特征交互：

$$l_{p} = \mathcal{F}_{\mathrm{sa}}(\mathcal{F}_{\mathrm{res}}(l_{p}) + l_{p}) \quad \text{(Equation 2)}$$

$\mathcal{F}_{\mathrm{res}}$ 为 1D 残差卷积块，$\mathcal{F}_{\mathrm{sa}}$ 为空间自注意力操作。该设计使模型能精细捕捉局部姿态细节（如手部关节的相对位置），消融实验中单独加入此模块使 FID 从 283.091 降至 183.213（Table 2）。

**全局注意力块**：在网络中间层对所有帧、所有关键点施加全局自注意力，打破局部窗口限制，捕获远距离姿态关联（如起跳与落地帧之间的协调性）。消融显示，在局部聚合基础上加入全局注意力后，FID 进一步降至 162.022，多模态得分（MM）从 41.890 跃升至 57.848，证明全局上下文对动作连贯性至关重要。

**扩散过程**：MotionDiT 根据噪声潜变量 $z_t$、时间步 $t$ 和文本条件 $s$ 预测噪声：

$$\epsilon_{\mathrm{pred}} = g_{\theta}(z_t, t, s) \quad \text{(Equation 3)}$$

基础扩散损失为标准的噪声预测均方误差：

$$\mathcal{L}_{d} = \mathbb{E}_{t, z_0, \epsilon}\left[\lVert \epsilon - \epsilon_{\mathrm{pred}} \rVert^{2}\right] \quad \text{(Equation 4)}$$

### CLoP 与 LAMA 损失：语义对齐约束

**CLoP（Contrastive Language-Motion Pretraining）** 通过对比学习将文本嵌入与姿态嵌入对齐到共享语义空间，其对称交叉熵损失为：

$$\mathcal{L}_{c} = \frac{\ell_{ce}\left(\ell_{2}\left(\mathbf{h}_{e}\mathbf{h}_{p}^{T}\right); y\right) + \ell_{ce}\left(\ell_{2}\left(\mathbf{h}_{p}\mathbf{h}_{e}^{T}\right); y\right)}{2} \quad \text{(Equation 5)}$$

其中 $\mathbf{h}_{e}$、$\mathbf{h}_{p}$ 分别为 L2 归一化后的文本和姿态嵌入，$\ell_{ce}$ 为交叉熵损失，$y$ 为匹配标签。CLoP 不仅为 LAMA 损失提供语义基座，还用于 MotionVid 数据集的 Caption Quality Filter 筛选。

**LAMA（Latent Semantic Alignment）损失** 在扩散训练过程中约束 MotionDiT 中间层潜变量与 CLoP 姿态特征在语义空间的一致性：

$$\mathcal{L}_{f} = d\left(g_{\omega}\left(\mathbf{h}_{d}^{l}\right), \mathbf{h}_{p}\right) \quad \text{(Equation 6)}$$

$g_{\omega}$ 为两层 MLP 投影器，将 MotionDiT 第 $l$ 层潜变量 $\mathbf{h}_{d}^{l}$ 映射至 CLoP 特征空间，$d(\cdot)$ 度量投影后特征与目标姿态嵌入 $\mathbf{h}_{p}$ 的差异。最终 MotionDiT 的总损失为：

$$\mathcal{L} = \mathcal{L}_{d} + \lambda_{f} \mathcal{L}_{f} \quad \text{(Equation 7)}$$

$\lambda_{f}$ 为语义对齐损失的权重。消融实验证实，在 DiT+Local+Global 基础上加入 LAMA 损失后，模型达到最佳 FID 149.007 和最高 Rp-top1 0.451（Table 2），证明语义对齐约束对提升生成精度和文本一致性不可或缺。

### 关键公式变量汇总

| 符号 | 含义 |
|------|------|
| $\mathbf{p}$ | 输入 2D 姿态序列 |
| $\mathcal{E}$ | Pose VAE 编码器 |
| $l_p$ | 补丁嵌入后的姿态潜变量 |
| $\mathcal{F}_{\mathrm{res}}$ | 1D ResNet 残差块 |
| $\mathcal{F}_{\mathrm{sa}}$ | 空间自注意力 |
| $z_t$ | 时间步 $t$ 的噪声潜变量 |
| $\epsilon_{\mathrm{pred}}$ | MotionDiT 预测的噪声 |
| $\mathbf{h}_{e}, \mathbf{h}_{p}$ | CLoP 文本/姿态嵌入 |
| $g_{\omega}$ | LAMA 投影 MLP |
| $\lambda_f$ | LAMA 损失权重 |

## 实验与分析

### 核心实验设置

所有对比实验均在 MotionVid 子集（50K 数据）上以统一设置进行训练和评估。对于原生 3D 姿态生成方法，将其输出转换为 2D 姿态后再参与对比。Text-to-Pose 评测指标包括 **FID**（Fréchet Inception Distance）、**R-precision top-1/2/3**（文本-姿态匹配精度）、**Diversity**（生成多样性）和 **Multimodality**（单文本多采样多样性）；Pose-to-Video 评测指标包括 **LPIPS**、**FVD** 和 **SSIM**；整体 Text-to-Video 评测采用 VBench 的 **Sensory Quality** 和 **Instruction Following** 分数。

### Text-to-Pose 主结果

Table 1 展示了 HumanDreamer 与 T2M-GPT、PriorMDM、MLD 等主流 Text-to-Pose 方法在 MotionVid 子集上的对比。HumanDreamer 在所有指标上均取得最优：**FID 降至 149.007**，相较最强基线 MLD（396.949）实现 **62.4% 的相对改进**；**R-precision top-1 达到 0.451**，较 MLD（0.318）提升 **41.8%**；Diversity 从 64.442 提升至 68.220。这些结果表明，解耦策略结合 MotionDiT 和 LAMA 损失能够显著增强文本到结构化姿态的映射质量，生成的姿态序列与文本描述更加吻合，同时保持了更高的运动多样性。

![[assets/figures/papers/paper_list_l25_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_G/figures/004_Table_1.jpg]]
*Table 1: Comparison to Other State-of-the-Art Methods on the MotionVid Subset. The metrics demonstrate that our method outperforms others in terms of pose-text alignment and diversity. Bold indicates the best result*

Figure 4 的可视化对比进一步证实了上述结论：基线方法生成的姿态常出现关键点漂移、运动抖动或与文本约束不一致的问题，而 HumanDreamer 生成的姿态关键点完整性更好，运动连贯性更强，且能更准确地反映文本中的动作语义。

### 消融实验

Table 2 系统消融了 MotionDiT 的三个核心组件，以验证每个设计选择的因果贡献：

![[assets/figures/papers/paper_list_l25_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_G/figures/005_Table_2.jpg]]
*Table 2: The ablation study presents four configurations, progressively adding components of Local, Global, and LAMA loss to the original model. As we move from the initial configuration to the fully enhanced model, performance metrics consistently improve, highlighting the positive impact of each additional component*

| 配置 | FID ↓ | Rp-top1 ↑ | Diversity ↑ | MM ↑ |
|------|-------|-----------|-------------|------|
| Vanilla DiT | 283.091 | 0.367 | 63.650 | 38.359 |
| + Local Aggregation | 183.213 | 0.415 | 66.260 | 41.890 |
| + Global Attention | 162.022 | 0.437 | 67.180 | 57.848 |
| + LAMA Loss (完整模型) | **149.007** | **0.451** | **68.220** | **58.720** |

**局部特征聚合（Local Feature Aggregation）** 将 FID 从 283.091 大幅降至 183.213，R-precision top-1 从 0.367 升至 0.415，证明 1D ResNet 残差块与空间自注意力的组合有效捕获了相邻关节间的局部细节，减少了姿态抖动。

**全局注意力（Global Attention）** 的加入使 FID 进一步降至 162.022，Multimodality 得分从 41.890 跃升至 57.848。这表明跨帧、跨关键点的全局自注意力机制对于建模远距离姿态关联、保证长序列动作连贯性至关重要。

**LAMA 损失** 使模型达到最佳性能：FID 149.007，R-precision top-1 0.451。该语义对齐损失通过 CLoP 预训练特征空间约束生成姿态与文本的语义一致性，显著提升了生成精度和稳定性，是模型不可或缺的组成部分。

### 数据规模扩展性

Table 3 展示了训练数据量从 50K 逐步扩展至 1.25M 时模型性能的变化趋势。R-precision top-1 从 0.451 单调提升至 0.513，FID 和 Diversity 也持续改善。这表明 HumanDreamer 的 2D 姿态生成框架具有良好的数据扩展性，大规模 2D 运动数据的积累可进一步提升模型性能，无需依赖稀缺的 3D 标注。

![[assets/figures/papers/paper_list_l25_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_G/figures/008_Table_3.jpg]]
*Table 3: By increasing the amount of training data, we observe an improvement in model performance, which validates the potential for rapid scalability using large-scale 2D motion data*

### Pose-to-Video 结果

Table 6 对比了 HumanDreamer 与 AnimateAnyone、MimicMotion、Animate-X 等主流 Pose-to-Video 方法。HumanDreamer 取得 **LPIPS 0.148**（较 Animate-X 的 0.232 降低 36.2%）和 **FVD 116.74**（较 Animate-X 的 139.01 降低 16.0%）的最优结果，同时 SSIM 达到 0.817。这说明解耦框架中生成的 2D 姿态能够作为高质量的结构先验，有效驱动下游视频生成模型。

![[assets/figures/papers/paper_list_l25_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_G/figures/016_Table_6.jpg]]
*Table 6: Evaluation of Pose-to-Video*

### 整体 Text-to-Video 对比

Table 7 将 HumanDreamer 的端到端 Text-to-Video 输出与 CogVideoX-5B 进行对比。HumanDreamer 在 **Sensory Quality（0.938 vs 0.531）** 和 **Instruction Following（0.813 vs 0.688）** 上均大幅领先。Figure 5 的可视化显示，CogVideoX 和 Mochi1 等通用文本到视频模型存在身体扭曲、运动连续性弱、面部生成缺失等问题，而 HumanDreamer 生成的视频运动幅度更大、过渡更平滑，且对面部细节有更好的保持。

![[assets/figures/papers/paper_list_l25_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_G/figures/017_Table_7.jpg]]
*Table 7: Evaluation between HumanDreamer and CogVideoX-5B*

### 失败模式与局限性

尽管 HumanDreamer 在定量和定性评估中表现优异，但存在以下已知限制：

1. **单人场景约束**：训练和评估均局限于单人、面部可见的场景，尚未验证在多人交互或严重遮挡条件下的性能。
2. **下游模型依赖**：最终视频质量部分受限于所选 Pose-to-Video 模型的性能，且未与其他先进文本到图像/视频骨干进行组合测试。
3. **姿态估计误差传播**：方法依赖精确的 2D 姿态提取作为中间步骤，姿态估计误差可能传播并放大到后续生成阶段。
4. **数据覆盖偏差**：尽管 MotionVid 规模大且经过严格清洗，但仍可能遗漏某些运动类型（如极端杂技动作），导致模型在这些场景下泛化不足。

### 关键图表结论速览

- **Table 1**：HumanDreamer 在 MotionVid 子集上全面超越 MLD 等基线，FID 相对改进 62.4%，验证了解耦 + MotionDiT + LAMA 的核心有效性。
- **Table 2**：逐步消融证实局部聚合、全局注意力和 LAMA 损失三者缺一不可，每个组件均带来显著且互补的性能增益。
- **Table 3**：数据规模从 50K 扩展至 1.25M 时性能持续提升，展示出良好的扩展潜力。
- **Table 6 & 7**：Pose-to-Video 和端到端 Text-to-Video 结果均显著优于对比方法，证明解耦框架在灵活性与可控性上的综合优势。

### 补充图表

![[assets/figures/papers/paper_list_l25_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_G/figures/013_Table_4.jpg]]
*Table 4: The table presents the specific composition of MotionVid, including the sources from which it was collected, the names of the datasets, the number of clips after video quality filter (VQF), the number of clips after human quality filter (HQF) and caption filter (CF), and the data types. It shows that MotionVid includes a diverse range of data categories, including general, action, and actions specific to different body parts, indicating a high degree of diversity*

![[assets/figures/papers/paper_list_l25_HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_G/figures/014_Table_5.jpg]]
*Table 5: Statistics of MotionVid’s eval set and HumanML3D*

## 方法谱系与知识库定位

### 1. 在文本驱动人体运动生成谱系中的位置

HumanDreamer 处于**文本驱动人体运动视频生成**这一交叉领域，其核心贡献在于将端到端的文本到视频（Text-to-Video）生成解耦为两个子任务：文本到姿态（Text-to-Pose）和姿态到视频（Pose-to-Video）。这一解耦策略直接回应了现有方法的两个核心瓶颈：

**与 Text-to-Pose 方法的对比**：在文本到姿态生成子任务中，HumanDreamer 与三类代表性基线展开对比。**T2M-GPT** 采用 VQ-VAE 与自回归 Transformer 的组合，将运动生成建模为离散 token 的序列预测；**PriorMDM** 基于扩散模型，以 CLIP 文本嵌入为条件直接生成 3D 运动序列；**MLD** 则在潜空间中执行扩散过程，是当前该子任务的最强基线。HumanDreamer 的核心差异在于：（1）引入 MotionDiT 架构，在标准 DiT 基础上叠加局部特征聚合（1D ResNet + 空间自注意力）和全局注意力机制，显式建模相邻关节的局部相关性与远距离帧间的长程依赖；（2）提出 LAMA 损失，利用 CLoP 对比预训练模型提供的语义对齐信号，在扩散训练过程中约束生成姿态与文本描述在特征空间的一致性。实验证据表明，这一设计组合使 FID 相对 MLD 降低 62.4%，R-precision Top-1 提升 41.8%（Table 1），且消融实验证实每个组件均不可或缺（Table 2）。

**与 Pose-to-Video 方法的对比**：在姿态到视频生成子任务中，HumanDreamer 与 **AnimateAnyone**、**MimicMotion** 和 **Animate-X** 等主流基线进行比较。这些方法均以参考图像和姿态序列为条件生成视频，其中 Animate-X 为当前最强基线。HumanDreamer 的 Pose-to-Video 模块在 LPIPS 指标上相较 Animate-X 实现 36.2% 的相对降低（0.148 vs. 0.232），FVD 降低 16.0%（Table 6），表明其生成视频的感知质量与时间一致性更具优势。

**与 Text-to-Video 方法的对比**：在端到端文本到视频的最终评测中，HumanDreamer 与通用文本到视频模型 **CogVideoX-5B** 和 **Mochi1** 进行对比。CogVideoX 在 Sensory Quality（0.938 vs. 0.531）和 Instruction Following（0.813 vs. 0.688）两项人工评估指标上均显著落后于 HumanDreamer（Table 7），且可视化结果显示 CogVideoX 和 Mochi1 存在身体扭曲、运动连续性差、面部生成缺失等问题（Figure 5）。这验证了解耦策略相较于直接文本到像素映射的优越性：文本→姿态的映射比文本→像素更易学习，结构化 2D 姿态作为显式中间先验有效降低了建模难度。

### 2. 适用边界与关键局限

HumanDreamer 的设计与评估存在以下明确边界：

**场景边界**：训练和评估均局限于**单人、面部可见**的场景。数据清洗流水线中的人体质量过滤器（Human Quality Filter）明确筛选单人场景且要求面部可见，过滤掉约 75% 的原始数据（Section 3.1）。因此，方法在多人交互、严重遮挡或面部不可见条件下的性能尚未验证，这是该框架从研究走向应用的核心缺口。

**下游依赖瓶颈**：解耦框架的最终视频质量受限于下游 Pose-to-Video 模型的性能天花板。论文未探索将生成的 2D 姿态序列与更先进的文本到图像/视频骨干网络（如 Sora 架构或最新视频扩散模型）组合的可能性，当前实验仅验证了特定 Pose-to-Video 骨干的有效性。

**数据分布偏差**：尽管 MotionVid 数据集规模达到约 1.25M 文本-姿态对，且经过视频质量过滤、人体质量过滤和字幕质量过滤等多轮清洗，但仍可能存在标注偏差。数据集涵盖通用动作、特定动作和不同身体部位的动作（Table 4），但无法保证覆盖所有运动类型，尤其是极端或罕见动作。

**姿态估计误差传播**：方法依赖精确的 2D 姿态提取作为中间步骤。数据流水线中的姿态估计误差可能通过 Pose VAE 编码和 MotionDiT 生成两个阶段传播并放大，论文未对此误差传播机制进行定量分析。

### 3. 开放问题与后续方向

从 HumanDreamer 的设计出发，以下开放问题值得关注：

**多人场景扩展**：如何将解耦框架推广到多人交互场景，同时保持文本控制的灵活性和姿态引导的可控性？这需要解决多人姿态的联合建模、个体身份保持以及交互语义的文本对齐等挑战。

**LAMA 损失的跨域迁移**：LAMA 损失中的语义对齐策略（利用 CLoP 对比预训练模型约束扩散生成过程）能否直接应用于 3D 姿态生成或更复杂的动作类型？该策略的核心在于构建文本与结构化运动表示的共享语义空间，其泛化能力值得进一步探索。

**数据集扩展与泛化**：MotionVid 的进一步扩展（例如引入更多交互动作类别或 3D 标注）能否显著提升模型的泛化能力？Table 3 显示训练数据量从 50K 扩大到 1.25M 时，Rp-top1 从 0.451 单调提升至 0.513，表明数据扩展性良好，但性能增益的边际递减趋势和上限尚不明确。

**两阶段误差累积的缓解**：解耦生成的两阶段设计天然存在误差累积问题——Text-to-Pose 的生成误差会传播到 Pose-to-Video 阶段。是否存在端到端微调或联合优化策略以减轻这一累积效应，同时不丧失解耦带来的灵活性和可控性优势？这是框架进一步优化的关键方向。

## 原文 PDF

![[paperPDFs/CVPR_2025/HumanDreamer_Generating_Controllable_Human_Motion_Videos_via_Decoupled_Generation.pdf]]
