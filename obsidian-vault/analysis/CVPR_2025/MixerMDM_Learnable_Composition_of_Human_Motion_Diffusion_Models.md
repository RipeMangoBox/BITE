---
title: MixerMDM Learnable Composition of Human Motion Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- MLCHMDM
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 提出可学习的Mixer模块，以两个预训练模型的输出、条件和去噪时间步为输入，动态预测混合权重；并采用双判别器对抗训练，使混合后的运动分布同时逼近两个预训练模型的分布，从而在无真值监督下学习最优组合策略。
primary_logic: 利用预训练模型输出作为真实样本，通过对抗训练迫使混合运动骗过各自判别器，从而保留各模型的核心特征；动态权重使组合过程可自适应，实现对个体动作的精细控制和交互全局的保持。
claims:
- MixerMDM ST变体在整体对齐度（Overall Alignment）上达到0.335，比最强基线DualMDM（0.221）高出约51.6%。
- 用户研究中，MixerMDM在交互对齐的平均排名为1.182（1为最好），第一排名占比85.14%，远优于DualMDM的2.286和10.29%。
- 定性结果显示，当施加个体动作变化时，MixerMDM生成的混合运动在一致性和可控性上显著优于之前方法。
- 消融实验证实对齐变换对性能有贡献，但即使移除，MixerMDM仍优于先前方法；学习到的动态权重曲线表明个体模型在去噪早期起主导作用，交互模型在后期加强。
---

# MixerMDM Learnable Composition of Human Motion Diffusion Models

> [!tip] 核心洞察
> 利用预训练模型输出作为真实样本，通过对抗训练迫使混合运动骗过各自判别器，从而保留各模型的核心特征；动态权重使组合过程可自适应，实现对个体动作的精细控制和交互全局的保持。

| 字段 | 内容 |
|------|------|
| 中文题名 | MixerMDM：可学习的人体运动扩散模型组合 |
| 英文题名 | MixerMDM Learnable Composition of Human Motion Diffusion Models |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | MixerMDM |
| Dataset | InterHuman + HumanML3D |

> [!tip] 效果简介
> - InterHuman + HumanML3D (混合组合任务) 上，Overall Alignment (↑) 0.335±.01 (MixerMDM ST, in2IN/in2IN) vs DiffusionBlending: 0.217±.00; DualMDM: 0.221±.01 (比DualMDM提高51.6%)。
> - 用户研究 (35 participants) 上，平均排名 (↓) - 交互对齐 1.182±.467 vs DualMDM: 2.286±.641; DiffusionBlending: 2.531±.584 (相对DualMDM提升约48%)。
> - 常规评估 (R-Precision, FID等) 上，Interaction R-Precision Top-3 (↑) 0.672±.02 (MixerMDM T, in2IN/in2IN) vs DualMDM: 0.574±.00; DiffusionBlending: 0.577±.00 (提高约17.1%)。

## 概要

### 问题瓶颈

在人体运动生成领域，文本条件扩散模型已在单一动作生成与双人交互生成上分别取得显著进展。然而，将预训练的单人模型与交互模型组合以生成可控交互运动时，现有方法面临根本性瓶颈：**DiffusionBlending** 采用固定标量权重进行混合，**DualMDM** 虽引入时间步调度器，但其权重调度完全由手工设计。这两类方法的共同缺陷在于，混合策略无法根据输入的运动序列、文本条件以及去噪过程所处的时间步进行自适应调整，导致组合生成的交互运动难以同时保留两个预训练模型各自的专长特性——要么交互一致性受损，要么个体动作可控性丧失。

### 核心方法定位

MixerMDM 是首个可学习的运动扩散模型组合技术。其核心创新在于两点：

1. **可学习的动态混合器（Mixer）**：设计了一个轻量的 Transformer+MLP 模块，以两个预训练模型在去噪步的输出 $\boldsymbol{x_t^a}$、$\boldsymbol{x_t^b}$、各自的条件 $\boldsymbol{c^a}$、$\boldsymbol{c^b}$ 以及时间步 $t$ 为输入，动态预测混合权重。该权重替代了 DualMDM 中手工调度的 $w_t$，使混合操作 $\boldsymbol{x_t^m} = \boldsymbol{x_t^a} + \text{Mixer}(\cdot) \cdot (\boldsymbol{x_t^b} - \boldsymbol{x_t^a})$ 具备自适应能力，支持全局（G）、时间（T）、空间（S）、时空（ST）四种混合粒度。

2. **双判别器对抗训练**：为每个预训练模型配备一个专用判别器，以预训练模型自身的输出作为正样本、混合运动作为负样本，采用 hinge 损失和 L1 正则化进行对抗训练。该机制无需真值监督，迫使混合运动的分布同时逼近两个预训练模型的分布，从而保留各模型的核心生成特征。

### 主要结果

在 InterHuman + HumanML3D 的混合组合任务上，MixerMDM 取得了显著优于先前方法的性能：

- **整体对齐度（Overall Alignment）**：MixerMDM ST 变体达到 0.335，比最强基线 DualMDM（0.221）高出约 **51.6%**（Table 1）。
- **用户研究**：35 名参与者的评估中，MixerMDM 在交互对齐的平均排名为 1.182（1 为最优），第一排名占比 85.14%，远优于 DualMDM 的 2.286 和 10.29%（Table 2）。
- **传统指标**：在 Interaction R-Precision Top-3 上，MixerMDM T 变体达到 0.672，较 DualMDM（0.574）提升约 17.1%（Table A）。

定性结果进一步表明，当施加个体动作变化时，MixerMDM 生成的混合运动在一致性和可控性上均显著优于先前方法（Figure 6, Figure 7）。消融实验证实，Mixer 学习到的动态权重曲线具有可解释的时序特性：个体模型在去噪早期起主导作用，交互模型在后期加强（Figure 5）；即使移除对齐变换，MixerMDM 仍优于先前方法（Table B）。此外，Mixer 权重具有良好的模块化和迁移能力，在不同预训练模型组合上可带来最高 37% 的性能提升（Table 3）。



### 人体运动生成与扩散模型

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列。近年来，扩散模型（Diffusion Models）凭借其高质量的生成能力和相对稳定的训练过程，已成为该领域的主流范式。通过在去噪过程中逐步将随机噪声转化为符合文本条件的运动序列，扩散模型在单人动作生成（如 **MDM**）和双人交互生成（如 **InterGen**、**in2IN**）等任务上均取得了显著进展。

然而，这些模型通常是在特定数据集上独立预训练的——例如，交互模型在 InterHuman 数据集上学习双人协作与对抗动作，而个体模型在 HumanML3D 数据集上学习单人动作。这导致了一个关键矛盾：交互模型擅长保持两人之间的全局协调性，但对个体动作的精细控制能力较弱；个体模型则恰好相反，能够精确执行指定的单人动作，却无法理解交互上下文。如何将两类预训练模型的专长进行组合，使生成的运动同时具备交互一致性和个体可控性，成为一个亟待解决的问题。

### 现有模型组合方法的局限

针对上述问题，研究者提出了扩散模型的组合技术，其核心思路是在每个去噪时间步将两个预训练模型的输出进行混合。代表性工作包括：

- **DiffusionBlending**：采用固定的标量权重，在整个去噪过程中以恒定比例混合两个模型的输出。这种方法完全忽略了不同去噪阶段对两类模型依赖程度的差异。
- **DualMDM**：引入了一个手工设计的权重调度器，根据去噪时间步 $t$ 动态调整混合权重 $w_t$，公式为：

$$
x_t^m = x_t^a + w_t \cdot (x_t^b - x_t^a)
$$

其中 $x_t^a$ 和 $x_t^b$ 分别为两个预训练模型在时间步 $t$ 的输出。DualMDM 相比固定权重有所改进，但其调度器仍然是人工预设的，无法根据输入动作序列的具体内容、文本条件的变化以及去噪过程的实时状态进行自适应调整。

**核心瓶颈**在于：无论是固定权重还是手工调度器，这些方法都采用了一种“一刀切”的组合策略。当输入条件发生变化时——例如，交互文本描述“两人正在拳击，突然一人踢腿”要求个体模型对特定人物施加精确的动作变化——静态的组合策略无法动态分配权重，导致混合运动要么丢失交互的全局协调性，要么无法忠实反映个体动作的细节变化。

### 本文动机与核心思路

MixerMDM 的提出正是为了突破上述瓶颈。其核心动机是：**将模型组合从手工设计的静态过程转变为可学习的动态过程**，使混合策略能够根据输入条件和去噪状态进行自适应优化。

具体而言，MixerMDM 引入了两个关键创新：

1. **可学习的 Mixer 模块**：一个轻量级的 Transformer+MLP 网络，以两个预训练模型的输出 $x_t^a, x_t^b$、各自的文本条件 $c^a, c^b$ 以及去噪时间步 $t$ 为输入，动态预测混合权重。这使得权重可以在不同时间步、不同空间位置（如不同关节）上自适应变化，实现从全局标量到时空向量的多粒度混合。

2. **对抗训练范式**：由于缺乏混合运动的真值监督，MixerMDM 采用双判别器对抗训练策略——每个预训练模型对应一个判别器，将预训练模型的真实输出作为正样本，混合运动作为负样本。通过迫使混合运动“骗过”两个判别器，Mixer 学习到一种能够同时保留两个预训练模型核心特征的组合策略，而无需任何人工标注的混合真值。

通过这种可学习的动态组合机制，MixerMDM 旨在实现一个关键目标：当交互条件保持不变时，生成的混合运动应与交互模型的输出分布一致；当个体条件发生变化时，混合运动应能精确反映该变化，同时维持交互的全局一致性。这使得对双人交互中个体动作的精细控制成为可能。



## 核心方法与创新机理

MixerMDM 的核心创新在于将**静态、手工设计的模型组合**转变为**可学习的、自适应的动态混合**，通过两个关键机制实现：**动态权重预测**与**双判别器对抗训练**。

### 瓶颈与因果机制

现有扩散模型组合方法（如 DiffusionBlending、DualMDM）的根本瓶颈在于混合权重生成方式的固化：DiffusionBlending 采用固定的全局标量权重，DualMDM 虽引入了沿去噪时间步变化的手动调度器，但两者均无法根据输入运动序列的具体内容、文本条件以及当前去噪阶段进行自适应调整。这导致组合生成的运动难以同时保留各预训练模型的专长特性——例如，在生成双人交互时，既要保持交互的全局协调性（来自交互模型），又要精确控制个体动作（来自个体模型）。

MixerMDM 的因果调节旋钮（causal knob）在于引入了一个可训练的 **Mixer 模块**，以两个预训练模型的输出 $\boldsymbol{x_t^a}, \boldsymbol{x_t^b}$、各自的条件 $\boldsymbol{c^a}, \boldsymbol{c^b}$ 以及去噪时间步 $t$ 为输入，动态预测混合权重：

$$\boldsymbol{x_t^m} = \boldsymbol{x_t^a} + Mixer(\boldsymbol{x_t^a}, \boldsymbol{c^a}, \boldsymbol{x_t^b}, \boldsymbol{c^b}, t) \cdot (\boldsymbol{x_t^b} - \boldsymbol{x_t^a})$$

这一公式在形式上继承了 DualMDM 的混合框架（Eq. 1），但将手工设计的固定权重 $w_t$ 替换为由神经网络动态预测的权重向量，使组合过程具备了**内容感知**和**时间步感知**的双重适应性。

### 训练范式的根本转变

MixerMDM 的第二个核心创新在于**训练策略的突破**。此前的方法在组合阶段不更新任何参数，完全依赖手工预设的规则；MixerMDM 则采用**双判别器对抗训练**框架：为每个预训练模型配备一个专用判别器（$\mathcal{D}^a$ 和 $\mathcal{D}^b$），将预训练模型自身的输出作为正样本，混合后的运动作为负样本，通过 hinge 损失和 L1 正则化进行对抗优化：

$$\mathcal{L}_{\mathrm{adv}}^{\mathrm{G}} = - \mathcal{D}^{a}(x_t^m) - \mathcal{D}^{b}(x_t^m) + L1$$

$$\mathcal{L}_{\mathrm{adv}}^{\mathrm{D}} = \min(0, -1 - \mathcal{D}^{a}(x_t^m)) + \min(0, -1 - \mathcal{D}^{b}(x_t^m)) + \min(0, -1 + \mathcal{D}^{a}(x_t^a)) + \min(0, -1 + \mathcal{D}^{b}(x_t^b)) + L1$$

核心洞察在于：**利用预训练模型输出作为真实样本，通过对抗训练迫使混合运动骗过各自判别器**，从而在无真值监督的情况下，隐式地保留了各预训练模型的核心特征分布。这解决了组合生成中缺乏 ground-truth 混合运动这一根本性监督难题。

### 混合粒度的灵活扩展

MixerMDM 将混合权重的粒度从单一全局标量扩展为四种可配置模式：**Global (G)**、**Temporal (T)**、**Spatial (S)** 和 **Spatio-Temporal (ST)**。Mixer 模块（由 Transformer 编码器和 MLP 解码器构成，仅约 21M 参数）根据配置输出对应形状的权重向量，实现对个体动作的精细空间-时间控制。实验表明，ST（时空）模式在整体对齐度（Overall Alignment）上达到最优（0.335，Table 1），验证了更细粒度动态权重的有效性。

学习到的动态权重曲线（Figure 5）揭示了组合过程中的自适应行为：个体模型在去噪早期起主导作用，交互模型在后期逐渐加强，这与人类运动生成从粗到细的直觉相符，而此前的手工调度器无法捕捉这种规律。



MixerMDM 的整体流水线围绕一个核心思想展开：在去噪过程的每一个时间步，动态地组合两个预训练文本条件运动扩散模型的输出，从而生成兼具交互语义与个体可控性的混合运动。如图 Figure 2 所示，整个框架由三个关键环节串联而成：预训练模型的前向推理、Mixer 模块的权重预测，以及基于预测权重的运动混合操作。

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/002_Figure_2.jpg]]
*Figure 2: MixerMDM pipeline. At each timestep t of the denoising process, a mixed motion is generated by first obtaining motions from separate text-conditioned pre-trained motion diffusion models. Using these motions and their conditions, the Mixer predicts unique mixing weights that are subsequently used in the Mixing procedure to blend the generated motions and obtain the mixed motion $\boldsymbol { x } _ { t } ^ { m }$*

**预训练模型的双路推理。** 给定交互文本描述 $c^a$ 和两个个体的文本描述 $c^b_1, c^b_2$，系统首先调用两个预训练模型：
- $M^a$：在 InterHuman 数据集上预训练的交互运动生成模型，负责根据 $c^a$ 生成包含两人交互的运动 $x_t^a$。
- $M^b$：在 HumanML3D 数据集上预训练的个体运动生成模型，被复制两份，分别根据 $c^b_1$ 和 $c^b_2$ 生成两个独立的个体运动，经拼接后形成 $x_t^b$。

由于 $M^b$ 在单人数据上训练，其输出缺乏两人之间的全局位置与朝向关系。为此，流水线在 $M^b$ 输出后引入姿态变换步骤：对个体运动进行中心化处理，并将其全局位置与朝向对齐到 $x_t^a$ 中对应人物的根节点信息，确保 $x_t^b$ 在进入 Mixer 之前保持在 $M^b$ 的训练分布内。

**Mixer 模块的权重预测。** 在获得 $x_t^a$ 与 $x_t^b$ 之后，Mixer 模块（Figure 3）以五类信息作为输入：两个预训练模型的输出运动 $x_t^a, x_t^b$、各自的文本条件 $c^a, c^b$，以及当前去噪时间步 $t$。Mixer 内部由一个轻量级 Transformer 编码器和一个 MLP 解码器构成——编码器将多源输入融合为潜在表示，解码器则根据预设的混合粒度输出对应形状的权重向量 $w_t$。支持的粒度包括全局标量、逐时间步向量、逐关节点向量以及时空联合权重矩阵，使组合过程具备从粗到细的灵活控制能力。

**混合操作。** 最终，混合运动 $x_t^m$ 通过以下公式计算：

$$x_t^m = x_t^a + w_t \cdot (x_t^b - x_t^a)$$

这一形式以 $x_t^a$ 为基础运动，通过 $w_t$ 控制 $x_t^b$ 的贡献程度。当 $w_t$ 趋近于 0 时，混合运动趋近于纯交互生成结果；当 $w_t$ 趋近于 1 时，则更多地采纳个体模型的输出。与先前方法中手工设定固定标量权重或静态调度器不同，MixerMDM 的权重由 Mixer 根据当前运动内容、条件语义和去噪阶段动态预测，使得组合策略能够自适应地调整——消融实验揭示的权重曲线表明，个体模型在去噪早期起主导作用，而交互模型在后期逐步加强，最终实现个体动作的精细控制与交互全局一致性的统一。

整个流水线在训练时采用双判别器对抗学习框架（Figure 4），以预训练模型自身输出作为正样本、混合运动作为负样本，迫使 $x_t^m$ 的分布同时逼近 $M^a$ 和 $M^b$ 的分布，从而在无真值监督的条件下学习最优组合策略。

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/003_Figure_4.jpg]]
*Figure 4: Adversarial training. Each pre-trained model has a specific discriminator that is trained with a hinge loss. We use the outputs of the pre-trained model as positive samples, and the mixed predictions generated by MixerMDM as negative samples*

### 补充图表

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/004_Figure_3.jpg]]
*Figure 3: Mixer architecture. The Mixer is composed of a Transformer encoder that takes as input both generated motions by the pre-trained models, their respective conditions, and the actual timestep of the denoising process. This encoder generates a latent representation, which is decoded by an MLP that outputs the mixing weights. T : number of frames of the motion sequence*



MixerMDM 的核心创新在于将传统手工设定的固定混合权重替换为**可学习的动态混合模块（Mixer）**，并引入**双判别器对抗训练**来驱动该模块的学习。整个组合过程发生在扩散模型的去噪链中，每一步均动态决定两个预训练模型输出的混合比例。

### 预训练模型与姿态对齐

组合的基础是两个预训练的文本条件扩散模型：
- **交互生成模型** $\mathcal{M}^a$：在 InterHuman 数据集上预训练，擅长生成双人交互动作（如 **InterGen** 或 **in2IN** 的交互版本）。
- **个体生成模型** $\mathcal{M}^b$：在 HumanML3D 数据集上预训练，擅长生成单人动作（如 **MDM** 或 **in2IN** 的个体版本）。由于交互涉及两人，$\mathcal{M}^b$ 被复制两份，分别生成两个人的个体动作。

在将个体模型输出送入 Mixer 之前，需进行**姿态变换**：将个体运动的全局位置中心化至原点，并对齐交互模型的全局位置与朝向。这一步确保个体模型输入保持在其训练分布内，避免因坐标偏移导致生成质量下降（消融实验证实移除该变换会降低交互性能，见 Table B）。

### Mixer 模块架构

Mixer 是一个轻量级网络（约 21M 参数，远小于预训练模型的 >300M 参数），其结构如图 Figure 3 所示：

- **输入**：两个预训练模型在当前去噪步 $t$ 的输出运动 $\boldsymbol{x}_t^a$、$\boldsymbol{x}_t^b$，各自对应的文本条件 $\boldsymbol{c}^a$、$\boldsymbol{c}^b$，以及去噪时间步 $t$。
- **编码器**：一个 Transformer Encoder，将所有输入编码为潜在表示。
- **解码器**：一个 MLP，将潜在表示解码为混合权重 $\boldsymbol{w}_t$。

混合权重的粒度支持四种模式（Type）：
- **Global (G)**：标量权重，全局统一混合比例。
- **Temporal (T)**：逐帧权重，不同时间步可不同。
- **Spatial (S)**：逐关节权重，不同身体部位可不同。
- **Spatio-Temporal (ST)**：时空联合权重，同时考虑帧与关节维度。

### 核心混合公式

混合操作沿用 DualMDM 的线性插值框架，但将手工调度的权重 $\boldsymbol{w}_t$ 替换为 Mixer 的动态预测：

$$
\boldsymbol{x}_t^m = \boldsymbol{x}_t^a + \text{Mixer}(\boldsymbol{x}_t^a, \boldsymbol{c}^a, \boldsymbol{x}_t^b, \boldsymbol{c}^b, t) \cdot (\boldsymbol{x}_t^b - \boldsymbol{x}_t^a)
$$

其中：
- $\boldsymbol{x}_t^m$：混合后的运动序列。
- $\boldsymbol{x}_t^a$：交互模型 $\mathcal{M}^a$ 在去噪步 $t$ 的输出（作为基础运动）。
- $\boldsymbol{x}_t^b$：个体模型 $\mathcal{M}^b$ 的输出。
- $\text{Mixer}(\cdot)$：Mixer 模块预测的混合权重，其形状取决于所选粒度模式。
- $(\boldsymbol{x}_t^b - \boldsymbol{x}_t^a)$：两个模型输出的差异向量，加权后叠加到基础运动上。

与 DualMDM 的关键区别：DualMDM 的 $\boldsymbol{w}_t$ 是手工设计的固定调度器（仅随时间步变化），而 MixerMDM 的权重同时依赖于两个模型的输出内容、文本条件及时间步，实现了**内容自适应的动态组合**。

### 对抗训练框架

由于没有混合运动的真值监督，MixerMDM 采用对抗训练来学习最优组合策略。训练框架如 Figure 4 所示，包含一个生成器（Mixer + 预训练模型）和两个判别器：

- **判别器 $\mathcal{D}^a$**：对应交互模型 $\mathcal{M}^a$，以 $\mathcal{M}^a$ 的真实输出 $\boldsymbol{x}_t^a$ 为正样本，混合运动 $\boldsymbol{x}_t^m$ 为负样本。
- **判别器 $\mathcal{D}^b$**：对应个体模型 $\mathcal{M}^b$，以 $\mathcal{M}^b$ 的真实输出 $\boldsymbol{x}_t^b$ 为正样本，$\boldsymbol{x}_t^m$ 为负样本。

**生成器对抗损失**（驱动 Mixer 学习）：

$$
\mathcal{L}_{\mathrm{adv}}^{\mathrm{G}} = - \mathcal{D}^{a}(\boldsymbol{x}_t^m) - \mathcal{D}^{b}(\boldsymbol{x}_t^m) + \lambda_{L1} \cdot \|\boldsymbol{w}_t\|_1
$$

Mixer 的目标是最小化该损失：前两项迫使混合运动同时骗过两个判别器（即混合运动在各自判别器看来都像真实样本），L1 正则项鼓励稀疏权重，防止过拟合。

**判别器对抗损失**（Hinge Loss）：

$$
\mathcal{L}_{\mathrm{adv}}^{\mathrm{D}} = \min(0, -1 - \mathcal{D}^{a}(\boldsymbol{x}_t^m)) + \min(0, -1 - \mathcal{D}^{b}(\boldsymbol{x}_t^m)) + \min(0, -1 + \mathcal{D}^{a}(\boldsymbol{x}_t^a)) + \min(0, -1 + \mathcal{D}^{b}(\boldsymbol{x}_t^b)) + \lambda_{L1} \cdot (\|\boldsymbol{w}_t\|_1)
$$

判别器的目标是正确区分真实样本（输出 $>1$）与混合样本（输出 $<-1$），从而为 Mixer 提供有意义的梯度信号。

### 训练细节

Mixer 使用 AdamW 优化器训练（学习率 $1\times10^{-5}$，权重衰减 $1\times10^{-5}$，$\beta=(0.9, 0.999)$），batch size 128，训练 300 个 epoch，采用 16 位混合精度，在单张 Nvidia 4090 GPU 上约需 36 小时。预训练模型在训练期间保持冻结，仅更新 Mixer 和判别器参数。

### 补充图表

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/005_Figure_5.jpg]]
*Figure 5: Mean mixing weights. The mean mixing weights of the best models for each variation of the Mixer output. Previous model composition techniques appear in the Global plot with a dotted line (DiffusionBlending [41]) and a dashed line (DualMDM [39])*



## 实验与关键发现

### 核心瓶颈与因果机制

现有扩散模型组合方法（**DiffusionBlending** 与 **DualMDM**）采用手工设定的固定混合权重或静态调度器，无法根据输入动作序列、文本条件及去噪时间步进行自适应调整，导致组合生成的运动难以同时保留各预训练模型的专长特性。MixerMDM 的核心因果调控变量在于：以两个预训练模型的输出、条件和去噪时间步为输入，通过可学习的 **Mixer 模块**动态预测混合权重；同时采用双判别器对抗训练，使混合后的运动分布同时逼近两个预训练模型的分布，从而在无真值监督下学习最优组合策略。其深层洞察是利用预训练模型输出作为真实样本，通过对抗训练迫使混合运动骗过各自判别器，从而保留各模型的核心特征；动态权重使组合过程可自适应，实现对个体动作的精细控制和交互全局的保持。

### 主实验结果

#### 整体对齐度与适应性

Table 1 报告了各方法在混合组合任务上的定量比较。MixerMDM 的 **ST（时空）变体**在整体对齐度（Overall Alignment）上达到 **0.335±.01**，比最强基线 DualMDM（0.221±.01）高出约 **51.6%**，比 DiffusionBlending（0.217±.00）高出约 54.4%。在适应性指标（Adaptability）上，MixerMDM ST 同样取得最优结果。值得注意的是，MixerMDM 的所有混合粒度变体（G/T/S/ST）均显著优于先前方法，其中 ST 模式因同时建模时间和空间维度的权重变化而表现最佳。

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation. Top: state-of-the-art comparison. Bottom: ablation of all the variations tested with MixerMDM. Type: type of mixing weights predicted by the Mixer. Adp.: Adaptability metric. All evaluations are executed 10 times to elude the randomness of the generation. ± indicates the 95% confidence interval. Best results are highlighted*

#### 用户研究

Table 2 展示了 35 名参与者对 20 个随机选择生成动作的排名结果。在交互对齐维度上，MixerMDM 的平均排名为 **1.182±.467**（1 为最好），第一排名占比高达 **85.14%**，远优于 DualMDM 的 2.286±.641 和 10.29%，以及 DiffusionBlending 的 2.531±.584 和 3.43%。在个体对齐维度上，MixerMDM 同样取得最优平均排名（1.467±.653）和第一排名占比（63.14%）。这表明人类评估者高度认可 MixerMDM 在保持交互一致性和个体动作准确性方面的优势。

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/008_Table_2.jpg]]
*Table 2: User study. Average rank (Avg), First ranked (1st). ± indicates standard deviation*

#### 常规指标评估

Table A 补充了使用传统指标（R-Precision、FID 等）的评估结果。MixerMDM T 变体在 Interaction R-Precision Top-3 上达到 **0.672±.02**，比 DualMDM（0.574±.00）提高约 17.1%。在 FID 指标上，MixerMDM 同样优于所有基线方法，进一步验证了其生成质量。

### 消融实验

#### 对齐变换的贡献

Table B 显示，移除对齐变换（alignment transformation）后，MixerMDM 的交互性能有所下降，但仍优于先前方法。这证实对齐变换对性能有正向贡献，但并非 MixerMDM 优势的唯一来源；动态混合权重与对抗训练本身已提供了显著的性能增益。

#### 混合权重粒度的影响

Table 1 的消融部分对比了四种混合权重粒度：Global（G）、Temporal（T）、Spatial（S）和 Spatio-Temporal（ST）。结果表明，粒度越细，整体对齐度越高，ST 模式达到最优。Figure 5 进一步可视化了各变体学到的平均混合权重曲线：个体模型在去噪早期起主导作用（权重较高），交互模型在后期加强，这与直觉一致——早期去噪决定动作的大致形态，后期细化交互细节。

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/015_Figure.jpg]]

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/016_Figure.jpg]]

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/017_Figure.jpg]]

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/018_Figure.jpg]]

#### 模块化与迁移能力

Table 3 展示了 Mixer 权重的模块化评估。将最优 Mixer（来自 Table 1）的权重重用于其他预训练模型组合时，最差组合的整体对齐度相对提升最高达 **37%**。这表明 Mixer 学到的动态混合策略具有跨模型组合的迁移能力，体现了方法的模块化设计优势。

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/010_Table_3.jpg]]
*Table 3: Modularity Evaluation. The worst combination of pretrained models is evaluated by using the weights of the best Mixer from Tab. 1. Impr.: relative Overall Alignment improvement (%) with respect to the original evaluation*

#### LLM 辅助推理

Table C 显示，使用 LLM 在推理时自动推断个体描述，对交互动作质量和文本对齐几乎没有影响。这验证了 MixerMDM 对输入条件的鲁棒性，即使在缺少精确个体描述的场景下也能保持生成质量。

### 定性分析

Figure 6 和 Figure 7 展示了定性对比结果。当施加个体动作变化时（如将拳击交互中的一人改为踢腿），MixerMDM 生成的混合运动在一致性和可控性上显著优于先前方法：交互全局得以保持，同时个体动作变化被准确分配到正确的人物上。相比之下，DiffusionBlending 和 DualMDM 往往出现动作混淆或交互结构破坏。补充定性示例（Figure A、Figure B）进一步支持了这一结论。

![[assets/figures/papers/paper_list_l5_MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models/figures/007_Figure_6.jpg]]
*Figure 6: Text Interaction: Two persons are in a boxing match when suddenly one person throws a kick Text Individual 1: An individual throws a kick with his right leg Text Individual 2: An individual is boxing Figure 6. Consistency. When an individual variation (underline) is performed in one of the interactions, MixerMDM achieves a greater level of consistency and individual assignment generating the mixed motion*

### 失败模式与局限性

尽管 MixerMDM 在组合生成上取得了显著优势，但仍存在以下局限：

1. **计算开销**：Mixer 模块在每个去噪步进行推理，引入额外计算开销，增加了生成时间。
2. **训练复杂度**：对抗训练引入了额外的超参数（如 L1 权重、判别器结构），调优复杂且训练过程不如监督训练稳定。
3. **预训练模型依赖**：方法依赖预训练模型的质量，若预训练模型本身能力不足，组合效果可能受限。
4. **数据表示统一性要求**：需要预训练模型输出具有统一的数据表示，不同格式需额外转换甚至重新训练，限制了即插即用的便利性。
5. **场景泛化未验证**：当前验证仅局限于将交互模型与个体模型组合，对其他类型的运动生成模型（如音频驱动、不同骨架）的通用性有待探索。

### 公平性说明

所有定量实验均进行 10 次独立评估并报告 95% 置信区间，以减少随机性影响。用户研究邀请了 35 名参与者对 20 个随机选择的生成动作进行排名，确保评估的代表性。提出的 Alignment 和 Adaptability 指标是针对模型组合任务专门设计的，弥补了传统指标在评估组合质量方面的不足。



## 定位与知识库关联

### 核心瓶颈与创新动机

现有的人体运动扩散模型组合方法面临一个根本性瓶颈：**组合策略是静态且手工设计的**。**DiffusionBlending** 采用全局固定标量权重，而 **DualMDM** 虽然引入了随时间步变化的权重调度器，但调度曲线仍由人工预设。这两种方法均无法根据输入的运动序列、文本条件以及去噪时间步进行自适应调整，导致组合生成的混合运动难以同时保留各预训练模型的专长特性——例如，当需要将“拳击比赛”的交互描述与“右腿踢击”的个体描述相结合时，静态策略无法动态权衡交互模型与个体模型的贡献，造成动作一致性和可控性的损失。

MixerMDM 的因果调节变量是**可学习的动态混合模块（Mixer）**，它取代了手工设定的权重机制。Mixer 以两个预训练模型的输出、各自的文本条件以及当前去噪时间步为输入，通过 Transformer 编码器和 MLP 解码器预测混合权重。这一设计使组合过程具备了条件自适应性：模型可根据输入内容自动判断在去噪的哪个阶段、空间的哪些关节上更依赖交互模型或个体模型。训练策略上，MixerMDM 采用**双判别器对抗训练**——每个预训练模型对应一个判别器，以预训练模型的真实输出为正样本、混合运动为负样本，迫使混合后的运动分布同时逼近两个预训练模型的分布，从而在无真值监督下学习最优组合策略。

### 与前驱方法的演进关系

MixerMDM 直接继承并改造了 DualMDM 的混合公式。DualMDM 的混合形式为：

$$x_t^m = x_t^a + w_t \cdot (x_t^b - x_t^a)$$

其中 $w_t$ 是手工设计的随时间步变化的标量权重。MixerMDM 将这一公式中的 $w_t$ 替换为 Mixer 模块的动态预测输出：

$$\boldsymbol{x_t^m} = \boldsymbol{x_t^a} + Mixer(\boldsymbol{x_t^a}, \boldsymbol{c^a}, \boldsymbol{x_t^b}, \boldsymbol{c^b}, t) \cdot (\boldsymbol{x_t^b} - \boldsymbol{x_t^a})$$

这一改动看似简单，但本质上将组合从“固定规则”升级为“可学习策略”。同时，MixerMDM 将混合权重的粒度从 DualMDM 的全局标量或单维度时间调度，扩展为四种模式：Global (G)、Temporal (T)、Spatial (S) 和 Spatio-Temporal (ST)，使模型能够在时间帧、空间关节或两者的联合维度上独立调整权重，显著提升了组合的精细度。

在训练范式上，MixerMDM 是首个在模型组合中引入对抗训练的工作。生成器（Mixer）的对抗损失为：

$$\mathcal{L}_{\mathrm{adv}}^{\mathrm{G}} = - \mathcal{D}^{a}(x_t^m) - \mathcal{D}^{b}(x_t^m) + L1$$

判别器采用 hinge 损失，分别以对应预训练模型的输出为正样本、混合运动为负样本。这种设计使得 Mixer 无需任何真值混合运动即可学习——两个预训练模型各自定义了“真实”的运动分布，Mixer 的目标是生成能同时骗过两个判别器的混合运动，从而隐式地保留了各模型的核心生成特征。

### 方法适用边界

**组合范围**：当前方法聚焦于将**一个交互生成模型**（在 InterHuman 数据集上预训练）与**两个个体生成模型副本**（在 HumanML3D 上预训练）进行组合。交互模型负责生成两人交互的全局结构，个体模型则注入单人动作的精细控制。这一设定适用于“交互场景下的个体动作编辑”任务，但尚未验证对其他类型模型组合的通用性（如音频驱动模型、不同骨架结构的模型）。

**数据表示要求**：方法依赖预训练模型输出具有**统一的数据表示**——具体而言，需要将个体模型的输出通过中心化和朝向对齐变换，使其与交互模型的全局坐标系一致。若预训练模型采用不同的运动表示格式（如关节位置 vs. 旋转矩阵、不同的人体拓扑），则需额外设计转换模块，甚至重新训练，限制了即插即用的便利性。

**预训练模型依赖性**：MixerMDM 的组合质量受限于预训练模型本身的能力。若交互模型或个体模型在特定文本条件上生成质量不佳，Mixer 无法弥补这一缺陷，因为对抗训练的正样本来自这些模型。实验中使用的主要预训练模型包括 **InterGen**、**in2IN**（交互与个体版本）和 **MDM**。

### 局限性与开放问题

**计算开销**：Mixer 模块在去噪过程的每一步都需要执行前向推理（包含 Transformer 编码和 MLP 解码），引入了额外计算成本。虽然 Mixer 仅有约 21M 参数（相比预训练模型的 300M+ 参数量较小），但在 1000 步去噪过程中累积的推理时间仍不可忽视。

**训练稳定性**：对抗训练引入了额外的超参数（如 L1 正则化权重、判别器结构、hinge 损失的 margin），调优过程复杂，且 GAN 训练本身的不稳定性可能导致收敛困难。是否有更稳定的训练范式（如利用扩散模型自身的引导机制替代 GAN）是一个开放方向。

**泛化能力**：当前验证局限于单交互模型与单个体模型的二组合场景。能否扩展到更多模型的组合（如三个以上预训练模型）、更复杂的多人场景或长序列运动生成，尚待探索。

**自动对齐**：如何处理不同数据表示之间的自动对齐，实现完全免训练的即插即用组合，是推动该方法实用化的关键问题。

### 证据强度评估

MixerMDM 的核心主张得到了较为充分的实验支撑。在定量评估中，MixerMDM ST 变体在 Overall Alignment 指标上达到 0.335，比最强基线 DualMDM（0.221）高出约 51.6%（Table 1）。用户研究进一步验证了感知质量：MixerMDM 在交互对齐的平均排名为 1.182（1 为最好），第一排名占比 85.14%，远优于 DualMDM 的 2.286 和 10.29%（Table 2）。消融实验证实了对齐变换的贡献（Table B），以及学习到的动态权重曲线揭示了有意义的时序模式——个体模型在去噪早期起主导作用，交互模型在后期加强（Figure 5）。模块化评估表明，重用最佳 Mixer 权重可显著提升其他预训练模型组合的性能（最高提升 37%，Table 3），体现了方法的迁移能力。

需要注意的是，Overall Alignment 和 Adaptability 指标是作者为模型组合任务专门设计的，其与下游任务实际表现的对应关系仍需更多验证。所有定量实验均进行了 10 次独立评估并报告 95% 置信区间，用户研究邀请了 35 名参与者，方法论上较为严谨。



## 原文 PDF

![[paperPDFs/CVPR_2025/MixerMDM_Learnable_Composition_of_Human_Motion_Diffusion_Models.pdf]]
