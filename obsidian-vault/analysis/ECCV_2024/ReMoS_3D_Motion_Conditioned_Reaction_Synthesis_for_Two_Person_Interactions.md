---
title: "ReMoS: 3D Motion-Conditioned Reaction Synthesis for Two-Person Interactions"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/ReMoS_3D_Motion_Conditioned_Reaction_Synthesis_for_Two_Person_Interactions.pdf
project_link: https://vcai.mpi-inf.mpg.de/projects/remos
code_link: null
aliases:
- ReMoS
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 采用级联扩散模型，通过联合时空交叉注意力(CoST-XA)和距离感知反应损失，从演员运动中隐式学习反应运动的时空同步性。
primary_logic: 将反应建模为条件生成任务，利用组合时空注意力同时捕捉不同身体部位间的跨时间交互依赖，无需额外标签即可生成高质量反应运动。
claims:
- "ReMoS 在 ReMoCap 数据集上相比最佳基线(InterGen)将 MPJPE 降低至少 20%，FID(身体)降低约 45%（例如 Lindy Hop: 40.2 vs 55.1 MPJPE, 0.12 vs 0.22 FID）。"
- 用户研究表明 ReMoS 合成反应在运动质量（3.79/5）和反应合理性（3.88/5）上显著优于基线。
- 消融实验表明移除级联扩散、反应损失、CoST-XA、H-XA 或空间引导均导致性能显著下降，验证各模块的必要性。
- ReMoS 在无标签条件下也能生成精细的手部交互，如图1所示的手指级接触。
---

# ReMoS: 3D Motion-Conditioned Reaction Synthesis for Two-Person Interactions

> [!tip] 核心洞察
> 将反应建模为条件生成任务，利用组合时空注意力同时捕捉不同身体部位间的跨时间交互依赖，无需额外标签即可生成高质量反应运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReMoS：基于3D运动条件的两人交互反应合成 |
| 英文题名 | ReMoS: 3D Motion-Conditioned Reaction Synthesis for Two-Person Interactions |
| 会议/期刊 | ECCV 2024 |
| Links | [Project](https://vcai.mpi-inf.mpg.de/projects/remos) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ReMoS |
| Dataset | ReMoCap Lindy Hop, ReMoCap Ninjutsu, InterHuman |

> [!tip] 效果简介
> - ReMoCap Lindy Hop (body only) 上，MPJPE (mm) ↓ 40.2 vs 55.1 (InterGen) (-14.9)。
> - ReMoCap Ninjutsu (body only) 上，MPJPE (mm) ↓ 137.2 vs 165.5 (InterGen) (-28.3)。
> - InterHuman 上，MPJPE (mm) ↓ 66.7 vs 69.5 (InterGen) (-2.8)。

## 概要

**核心问题**：在两人交互场景中，如何仅根据一方的 3D 运动（演员），自动生成另一方（反应者）时空同步、全身包含手部的合理反应运动，而无需依赖动作标签或文本提示？现有方法要么依赖额外的语义条件，要么忽略手部交互和精细的时空依赖，难以生成高质量的反应运动。

**方法定位**：ReMoS 将反应生成建模为条件生成任务，采用**级联扩散模型**作为主干。其核心设计包括：(1) **联合时空交叉注意力** (CoST-XA)，同时捕捉演员与反应者不同身体部位之间的空间与跨时间交互依赖；(2) **手部交互感知交叉注意力** (H-XA)，利用二值掩码显式关注交互手部；(3) **距离感知反应损失**，以指数衰减权重使模型更关注靠近演员的关节。整个框架分两阶段级联生成——先生成身体关节，再以身体生成结果为条件生成手部关节，无需额外标签即可隐式学习反应的时空同步性。

**主要结果**：在自建数据集 ReMoCap 上，ReMoS 相比最优基线 **InterGen** 将身体 MPJPE 降低至少 20%（Lindy Hop: 40.2 vs 55.1 mm），FID 降低约 45%（0.12 vs 0.22）。消融实验验证了级联扩散、反应损失、CoST-XA、H-XA 及推理时空间引导等各模块的必要性。用户研究表明，ReMoS 合成的反应在运动质量（3.79/5）和反应合理性（3.88/5）上均显著优于基线方法。在无标签条件下，ReMoS 也能生成手指级精细交互（Fig. 1）。

### 两人交互运动建模：从共生成到条件反应

三维人体运动生成近年来取得了显著进展，但大多数工作聚焦于单人场景。在两人交互场景中，现有方法通常将两人的运动视为一个整体进行**联合生成**（co-generation），例如基于文本描述同时输出双人运动序列。这类方法的典型代表包括 **InterGen**（基于文本到双人运动的扩散模型）、**ComMDM**（基于通信的双人扩散模型）以及 **RAIG**（角色感知的交互生成）。它们虽然能够产生视觉上合理的双人运动，但存在一个根本性局限：**生成过程需要额外的条件信号**——无论是动作类别标签、文本描述，还是预定义的交互图——来驱动两个角色的运动同步。

然而，在许多真实场景中，我们面对的并非“从零生成双人运动”的问题，而是**给定一方的运动，推断另一方的合理反应**。例如，在武术对练中，攻击方出拳，防守方需要做出相应的格挡或闪避；在双人舞蹈中，领舞者做出引导动作，跟舞者需要产生同步的舞步。这种“反应合成”（reaction synthesis）任务的核心挑战在于：反应运动的时空结构完全由演员运动隐式决定，无法通过简单的标签或文本描述来充分刻画。

### 现有方法的三个关键缺口

**缺口一：依赖显式条件信号，无法从演员运动直接推理。** 现有方法如 **InterFormer**（反应运动合成基线）和 **MixNMatch**（双人交互合成基线）通常需要动作标签或文本提示来约束生成过程。当仅给定演员的3D运动序列时，这些方法缺乏从运动学信号中隐式提取交互语义的能力，导致生成的反应运动与演员运动在时序上脱节。

**缺口二：忽略手部交互的精细建模。** 两人交互中，手部接触是最常见也最具表现力的交互形式——握手、击掌、格挡、引导旋转等均依赖手指级别的精确空间关系。然而，现有方法要么将手部视为身体关节的简单延伸进行隐式建模，要么完全忽略手部运动，导致生成的交互缺乏真实感。这一问题在需要精细手部协调的场景（如Lindy Hop舞蹈中的手部引导）中尤为突出。

**缺口三：时空依赖建模不充分。** 反应运动的质量取决于反应者能否在空间和时间两个维度上同时与演员保持同步。例如，防守方的手臂不仅需要在空间上到达正确的格挡位置，还需要在时间上精确匹配攻击方的出拳节奏。现有方法通常采用“先空间后时间”或“仅时间”的注意力机制，无法同时捕捉跨身体部位、跨时间步的交互依赖，导致生成的运动在局部关节对齐和全局时序一致性上均存在不足。

### ReMoS的动机与核心思路

针对上述缺口，**ReMoS**（**Re**active **Mo**tion **S**ynthesis）提出了一种新的问题范式：**以演员的3D全身运动为唯一条件，直接合成反应者的全身及手部运动，无需任何额外标签或文本提示**。这一范式将反应建模为条件生成任务，其核心洞察在于：反应运动的时空同步性可以通过**组合时空交叉注意力机制**从演员运动中隐式学习。

具体而言，ReMoS采用级联扩散模型，分两阶段生成反应运动：第一阶段生成反应者的身体关节，第二阶段以生成的身体运动为条件进一步生成手部关节。这种级联设计使得手部合成能够感知已生成的身体姿态，从而产生全局一致的全身反应。在每一阶段内部，**联合时空交叉注意力（CoST-XA）** 同时建模演员与反应者不同身体部位之间的空间和时间交互依赖，解决了传统方法中时空建模割裂的问题。此外，**距离感知反应损失**以指数衰减权重强调靠近演员的关节，使模型更关注交互密集的身体区域。

通过这一设计，ReMoS在无需显式交互标签的情况下，能够生成与演员运动高度同步的反应序列，包括手指级别的精细手部交互——如图1所示，在Ninjutsu对练和Lindy Hop舞蹈中，ReMoS合成的反应者（蓝色）与演员（红色）之间呈现出自然的身体对齐和手部接触。

## 核心方法与创新机理

ReMoS 的核心创新在于将两人交互中的反应运动生成重新定义为**纯运动条件生成问题**，并通过三个关键设计突破现有方法的瓶颈：**(1) 级联扩散生成策略**、(**2) 联合时空交叉注意力机制**、以及 **(3) 距离感知反应损失与推理时空间引导**。这些创新使 ReMoS 无需动作标签或文本提示，仅从演员的 3D 运动即可生成精确同步的全身及手部反应运动。

### 1. 从标签依赖到纯运动条件生成

现有两人交互运动合成方法普遍依赖额外条件信号：**InterGen** 需要文本描述来生成双人运动，**ComMDM** 利用通信信号进行条件生成，**RAIG** 依赖角色标签。这些方法无法直接从演员运动本身推断反应运动，且忽略了手部交互的精细时空依赖。ReMoS 首次将问题形式化为 $P(X|Y)$ 的建模——仅以演员运动 $Y$ 为条件，通过条件去噪扩散概率模型（DDPM）直接采样反应运动 $X$（Eq. 1-2）。这一设定消除了对标签或提示的依赖，使模型能够从运动数据中隐式学习交互规律。

### 2. 级联扩散：身体→手部的分阶段生成

与单阶段联合生成的基线方法（如 InterGen、ComMDM）不同，ReMoS 采用**级联两阶段生成策略**（Fig. 3）：

- **第一阶段（Body Synthesis Module）**：以演员身体运动 $Y_B$ 为条件，从噪声中生成反应者的身体关节位置 $X_B^{(0)}$（Eq. 3）。
- **第二阶段（Hands Synthesis Module）**：以演员手部运动 $Y_H$ 和已生成的身体运动 $X_B^{(0)}$ 为条件，生成反应者的手部关节位置 $X_H^{(0)}$（Eq. 4）。

这种级联设计的关键优势在于：身体关节的运动幅度大、交互模式相对稀疏，而手部关节需要精细的接触级同步。分阶段生成使模型能够先建立粗粒度的身体交互框架，再在此基础上精细刻画手部交互，避免了单阶段模型同时处理两种尺度信号时的优化困难。消融实验证实，移除级联架构（w/o cascaded）会导致身体和手部合成指标均显著下降（Table 2）。

### 3. 联合时空交叉注意力（CoST-XA）

现有方法通常采用**顺序注意力**（先空间后时间）或仅时间维度的注意力，这割裂了不同身体部位之间的跨时间交互依赖。ReMoS 提出的 **CoST-XA**（Combined Spatio-Temporal Cross-Attention）机制（Eq. 6）将演员与反应者身体运动的时空特征**联合编码**：

$$\mathrm{CoST-XA} = \mathrm{softmax}\left(\frac{Q_B K_B^T}{\sqrt{d_{K_B}}}\right) V_B$$

该机制同时考虑不同身体部位（如演员的左手与反应者的右手）在**不同时间步**上的空间交互关系，从而捕捉复杂的跨时空依赖模式。例如，在 Lindy Hop 舞蹈中，演员的引导手势与反应者的跟随旋转之间可能存在数帧的时间延迟，CoST-XA 能够建模这种非即时的因果关系。消融实验表明，移除 CoST-XA 会导致 MPJPE 显著升高（Table 2），验证了联合时空建模的必要性。

### 4. 手部交互感知交叉注意力（H-XA）

手部交互是两人交互中最精细但也最容易被忽略的部分。ReMoS 引入 **H-XA**（Hand-Interaction-Aware Cross-Attention），利用**二值手部交互掩码** $\mathbb{1}_{H_A}$ 和 $\mathbb{1}_{H_R}$ 显式引导模型关注正在交互的手部关节：

$$\mathrm{H-XA} = \mathrm{softmax}\left(\frac{(\mathbb{1}_{H_R} \odot Q_H)(\mathbb{1}_{H_A} \odot K_H)^T}{\sqrt{d_{K_H}}}\right) V_H$$

交互掩码通过计算演员与反应者手部关节的空间距离自动生成，使注意力权重集中在接触或接近的手部区域。这一设计使得 ReMoS 在无任何接触标注的情况下，也能生成手指级精度的交互（如 Fig. 1 中圈出的手部接触细节）。移除 H-XA 会导致手部合成质量明显退化（Table 2）。

### 5. 距离感知反应损失与推理时空间引导

传统运动生成方法仅使用标准重建损失（如 MPJPE），对所有关节赋予相等权重。ReMoS 提出**距离感知反应损失**（Eq. 9）：

$$\mathcal{L}_r = \frac{1}{NJ} \sum_{n=1}^N \sum_{j=1}^J \exp(-d(x_{n,j}, y_{n,j})) \cdot |d(x_{n,j}, y_{n,j}) - d(x_{n,j}^{(0)}, y_{n,j})|$$

该损失通过**指数衰减权重** $\exp(-d(\cdot))$ 使模型更关注靠近演员的关节（Fig. 4），因为这些关节的交互约束更强、对反应合理性影响更大。远离演员的关节（如自由摆动的后手）则获得较低权重，允许更大的生成自由度。

在推理阶段，ReMoS 进一步引入**空间引导**（Eq. 11），通过梯度下降最小化演员与反应者手臂关节距离：

$$X_B^{(0)} = X_B^{(0)} - \gamma \nabla_{X_B^{(0)}} G(\phi, \hat{\phi})$$

这在不重新训练的情况下改善了推理时的空间对齐精度。消融实验表明，移除反应损失或空间引导均导致性能下降（Table 2），证实了两者对生成质量的关键贡献。

### 创新总结

| 设计要素 | 基线方法 | ReMoS 创新 | 作用 |
|---------|---------|-----------|------|
| 条件信号 | 文本/动作标签/通信信号 | 纯演员运动 $Y$ | 消除标签依赖 |
| 生成策略 | 单阶段联合生成 | 级联（身体→手部） | 粗细粒度解耦优化 |
| 时空建模 | 顺序或仅时间注意力 | CoST-XA 联合时空注意力 | 捕捉跨时空交互依赖 |
| 手部建模 | 隐式或不建模 | H-XA + 二值交互掩码 | 精细手部交互生成 |
| 损失函数 | 标准重建损失 | 距离感知反应损失 | 关注交互关键关节 |
| 推理优化 | 无 | 空间引导梯度更新 | 改善推理对齐 |

这些创新共同构成了 ReMoS 的技术护城河：级联架构提供结构先验，CoST-XA 和 H-XA 提供注意力层面的归纳偏置，反应损失和空间引导则从优化和推理两端强化空间同步约束。消融实验的系统性验证（Table 2）表明，每个组件都是性能提升的必要条件，而非冗余设计。

ReMoS 将反应运动合成建模为一个条件生成任务：给定演员的 3D 全身运动序列 $Y = \{Y_B, Y_H\}$（分别表示身体关节与手部关节位置），生成反应者与之时空同步的全身运动 $X = \{X_B, X_H\}$。整个框架基于去噪扩散概率模型（DDPM），采用**级联两阶段生成策略**（Fig. 2, Fig. 3），逐级解码反应运动。

![[assets/figures/papers/paper_list_l1765_ReMoS_3D_Motion_Conditioned_Reaction_Synthesis_for_Two_Person_Interactio/figures/002_Figure_2.jpg]]
*Figure 2: ReMoS Overview. Given the motion of the actor (bottom-middle, in red), we synthesize a plausible motion for the reactor (bottom-left, in blue). We achieve this using a denoising diffusion-based probabilistic model (center ) trained on reactive motion sequences*

**第一阶段：身体合成模块（Body Synthesis Module）**。该阶段以演员的身体关节运动 $Y_B$ 为条件，从高斯噪声中逐步去噪生成反应者的身体关节位置 $X_B^{(0)}$：
$$X_B^{(0)} = f_{\theta_B}(X_B^{(t)}, t, Y_B)$$
其中 $f_{\theta_B}$ 为身体去噪网络，$t$ 为扩散时间步。核心在于网络内部采用的**联合时空交叉注意力（CoST-XA）**，它同时融合演员与反应者身体关节之间的空间和时间交互特征，从而高效地同步两者的运动节律与空间关系：
$$\mathrm{CoST-XA} = \mathrm{softmax}\left(\frac{Q_B K_B^T}{\sqrt{d_{K_B}}}\right) V_B$$

**第二阶段：手部合成模块（Hands Synthesis Module）**。该阶段以演员手部运动 $Y_H$、第一阶段生成的 $X_B^{(0)}$ 以及手部交互掩码为条件，生成反应者的手部关节位置 $X_H^{(0)}$：
$$X_H^{(0)} = f_{\theta_H}(X_H^{(t)}, t, Y_H, \mathbb{1}_{H_A}(Y_B) \mathbb{1}_{H_R}(X_B^{(0)}))$$
这里 $\mathbb{1}_{H_A}$ 和 $\mathbb{1}_{H_R}$ 分别为演员与反应者的二值手部交互掩码，用于标识交互中的手部关节。手部合成模块通过**手部交互感知交叉注意力（H-XA）** 显式关注交互手部的局部特征：
$$\mathrm{H-XA} = \mathrm{softmax}\left(\frac{(\mathbb{1}_{H_R} \odot Q_H)(\mathbb{1}_{H_A} \odot K_H)^T}{\sqrt{d_{K_H}}}\right) V_H$$

最终，反应者的全身运动由两个阶段的输出拼接得到 $X = \{X_B^{(0)}, X_H^{(0)}\}$。整个级联设计的关键优势在于：身体合成阶段建立了全局的时空对齐骨架，而手部合成阶段则借助已生成的身体姿态和交互掩码，专注于精细的手指级交互建模，从而无需任何动作标签或文本提示即可生成高质量的同步反应运动。

ReMoS 将反应运动生成建模为条件去噪扩散概率模型（DDPM），在给定演员运动 $Y$ 的条件下学习反应运动 $X$ 的条件分布 $P(X|Y)$。整体框架采用**级联两阶段生成策略**：首先生成反应者的身体关节位置 $X_B$，再以此为基础生成手部关节位置 $X_H$（Fig. 3）。

![[assets/figures/papers/paper_list_l1765_ReMoS_3D_Motion_Conditioned_Reaction_Synthesis_for_Two_Person_Interactio/figures/003_Figure_3.jpg]]
*Figure 3: ReMoS Framework. Given the full-body sequence of the actor (left, in red), we input noisy body and hand samples (from below) in a cascaded fashion. We synthesize the body samples first, and use them for hand-interaction-aware attention masking (top-center ) to synthesize the denoised hand samples (top-right). The full-body reactive motion is a concatenation of the denoised body and hand samples (right, in blue)*

### 扩散过程基础

前向扩散过程以闭式解向干净运动 $X^{(0)}$ 逐步注入高斯噪声：

$$X^{(t)} = \sqrt{\bar{\alpha}_t} X^{(0)} + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I) \tag{Eq. 1}$$

反向去噪过程从高斯先验 $p(X^{(T)})$ 逐步重建反应运动：

$$p(X^{(0)}) = p(X^{(T)}) \prod_{t=1}^{T} p(X^{(t-1)} | X^{(t)}) \tag{Eq. 2}$$

### 级联两阶段生成

**第一阶段：身体合成（Body Synthesis Module）**。以演员身体运动 $Y_B$ 为条件，从噪声样本 $X_B^{(t)}$ 和时间步 $t$ 去噪生成反应者身体关节 $X_B^{(0)}$：

$$X_B^{(0)} = f_{\theta_B}(X_B^{(t)}, t, Y_B) \tag{Eq. 3}$$

**第二阶段：手部合成（Hands Synthesis Module）**。以演员手部运动 $Y_H$ 和已生成的身体运动 $X_B^{(0)}$ 为条件，并利用二值手部交互掩码 $\mathbb{1}_{H_A}(Y_B)$ 和 $\mathbb{1}_{H_R}(X_B^{(0)})$ 标识交互中的手部关节：

$$X_H^{(0)} = f_{\theta_H}(X_H^{(t)}, t, Y_H, \mathbb{1}_{H_A}(Y_B) \mathbb{1}_{H_R}(X_B^{(0)})) \tag{Eq. 4}$$

### 联合时空交叉注意力（CoST-XA）

CoST-XA 是身体合成模块的核心机制，同时捕捉演员与反应者身体关节间的**空间与时间交互依赖**。它组合了不同身体部位之间的时空交互特征，使反应运动与演员运动在时空维度上同步：

$$\mathrm{CoST-XA} = \mathrm{softmax}\left(\frac{Q_B K_B^T}{\sqrt{d_{K_B}}}\right) V_B \tag{Eq. 6}$$

其中 $Q_B$、$K_B$、$V_B$ 融合了反应者与演员身体运动的时空特征表示，$d_{K_B}$ 为键的维度。与传统的先空间后时间或仅时间维度的注意力不同，CoST-XA 在一次计算中联合建模跨身体部位、跨时间步的交互依赖。

### 手部交互感知交叉注意力（H-XA）

H-XA 用于手部合成模块，通过二值交互掩码显式聚焦于正在交互的手部关节，鼓励模型学习局部化的手部交互特征：

$$\mathrm{H-XA} = \mathrm{softmax}\left(\frac{(\mathbb{1}_{H_R} \odot Q_H)(\mathbb{1}_{H_A} \odot K_H)^T}{\sqrt{d_{K_H}}}\right) V_H \tag{Eq. 7}$$

其中 $\mathbb{1}_{H_A}$ 和 $\mathbb{1}_{H_R}$ 分别为演员和反应者的手部交互掩码，$\odot$ 表示逐元素乘法。掩码确保注意力权重集中于交互手部区域，从而生成精细的手指级接触运动。

### 损失函数

总损失由三项加权组成：

$$\mathcal{L} = \lambda_c \mathcal{L}_c + \lambda_r \mathcal{L}_r + \lambda_k \mathcal{L}_k \tag{Eq. 8}$$

其中 $\mathcal{L}_c$ 为接触重建损失，$\mathcal{L}_r$ 为距离感知反应损失，$\mathcal{L}_k$ 为运动学损失。权重设置为 $\lambda_c=10.0$，$\lambda_r=10.0$，$\lambda_k=1.0$。

**距离感知反应损失（Distance-Aware Reaction Loss）** 是 ReMoS 的关键创新之一，利用指数衰减权重使模型更关注靠近演员的关节：

$$\mathcal{L}_r = \frac{1}{NJ} \sum_{n=1}^N \sum_{j=1}^J \exp(-d(x_{n,j}, y_{n,j})) \cdot |d(x_{n,j}, y_{n,j}) - d(x_{n,j}^{(0)}, y_{n,j})| \tag{Eq. 9}$$

其中 $d(\cdot,\cdot)$ 为关节间欧氏距离，$\exp(-d(\cdot,\cdot))$ 为指数衰减权重（Fig. 4）。该设计使近距离关节（如握手时的手部关节）获得更高权重，远距离关节（如脚部）权重自然衰减，从而引导模型优先学习交互紧密区域的时空同步性。

![[assets/figures/papers/paper_list_l1765_ReMoS_3D_Motion_Conditioned_Reaction_Synthesis_for_Two_Person_Interactio/figures/004_Figure_4.jpg]]
*Figure 4: Visualization of Distance Aware Reaction Loss. We use an exponentially decaying distance-aware reaction loss to focus more on the reactor’s joints that are closer to the actor*

**运动学损失（Kinematic Loss）** 约束生成运动的物理合理性：

$$\mathcal{L}_k = \lambda_v \mathcal{L}_{vel} + \lambda_a \mathcal{L}_{acc} + \lambda_b \mathcal{L}_{bone} + \lambda_f \mathcal{L}_{foot} \tag{Eq. 10}$$

其中 $\mathcal{L}_{vel}$ 为关节速度损失，$\mathcal{L}_{acc}$ 为加速度损失，$\mathcal{L}_{bone}$ 为骨骼长度一致性损失，$\mathcal{L}_{foot}$ 为足部滑动约束损失。权重设置为 $\lambda_v=10.0$，$\lambda_a=1.0$，$\lambda_b=1.0$，$\lambda_f=20.0$。

### 推理时空间引导

在推理阶段，ReMoS 对去噪后的身体姿态施加空间引导，通过梯度下降最小化演员与反应者手臂关节间的距离，进一步改善空间对齐：

$$X_B^{(0)} = X_B^{(0)} - \gamma \nabla_{X_B^{(0)}} G(\phi, \hat{\phi}) \tag{Eq. 11}$$

其中 $\phi$ 和 $\hat{\phi}$ 分别为演员和反应者的手臂关节位置，$G$ 为基于交互掩码的距离最小化目标，引导尺度 $\gamma = 10^{-3}$。该机制仅在推理时使用，不增加训练开销。

> **注**：上述公式均来自论文原文（Sec. 3.1–3.4），变量含义与原文一致。各模块的必要性已通过消融实验验证（Table 2）：移除级联扩散、CoST-XA、H-XA、反应损失或空间引导均导致性能显著下降。

## 实验与关键发现

### 核心定量结果

ReMoS 在自建数据集 ReMoCap 上对全部基线方法建立了显著优势。表 2 报告了全身（含手部）指标：在 Lindy Hop 动作上，ReMoS 的 MPJPE 降至 40.7 mm，而最强基线 **InterGen** 为 55.1 mm（降幅约 26%）；在 Ninjutsu 动作上，MPJPE 为 139.2 mm，远低于 InterGen 的 165.5 mm。运动质量指标 FID 同样领先——Lindy Hop 上 ReMoS 的 FID（身体）仅为 0.12，InterGen 为 0.22（降幅约 45%）。仅评估身体关节时（Table D.3），Lindy Hop 的 MPJPE 为 40.2 mm vs. 55.1 mm，Ninjutsu 为 137.2 mm vs. 165.5 mm，优势保持稳定。

在外部数据集上，ReMoS 展现出良好的泛化能力。在 InterHuman 数据集上（Table D.1），ReMoS 以 MPJPE 66.7 mm 优于 InterGen 的 69.5 mm。在 ExPI 和 2C 数据集上（Table 3），ReMoS 同样在多数指标上取得最优或次优结果，说明方法并非仅在自建数据上过拟合。

![[assets/figures/papers/paper_list_l1765_ReMoS_3D_Motion_Conditioned_Reaction_Synthesis_for_Two_Person_Interactio/figures/008_Table_3.jpg]]
*Table 3: Quantitative Evaluation on the ExPI and 2C datasets. We compare ReMoS with state-of-theart motion synthesis methods on the ExPI [24] and 2C datasets [55]. ↓: lower is better, ↑: higher is better, →: values closer to GT are better. Bold indicates best*

### 消融实验：各模块的必要性

Table 2 中的消融行揭示了每个设计选择的因果贡献：

![[assets/figures/papers/paper_list_l1765_ReMoS_3D_Motion_Conditioned_Reaction_Synthesis_for_Two_Person_Interactio/figures/006_Table_2.jpg]]
*Table 2: Quantitative Evaluation on ReMoCap. We compare ReMoS with our baselines and ablated versions (Sec. 5.2) on the ReMoCap dataset. We evaluate these methods on metrics such as MPJPE, MPJVE, FID, and Diversity. ↓: lower is better, ↑: higher is better, →: values closer to GT are better. Bold indicates best*

- **移除扩散过程（w/o diffusion）**：直接回归替代去噪扩散，导致 Lindy Hop MPJPE 从 40.7 mm 骤升至 72.5 mm（+31.8 mm），Ninjutsu 从 139.2 mm 升至 224.5 mm（+85.3 mm）。这表明扩散模型的多步去噪机制对生成高质量反应运动至关重要。
- **移除反应损失（w/o reaction loss）**：仅保留标准重建损失，Lindy Hop 全身 MPJPE 增至 62.7 mm。距离感知反应损失通过指数衰减权重强制模型关注靠近演员的关节，缺失后空间同步性显著恶化。
- **移除 CoST-XA**：将联合时空交叉注意力替换为普通交叉注意力，身体和手部指标均出现明显退化，验证了同时捕捉空间与时间交互依赖的必要性。
- **移除 H-XA**：取消手部交互感知交叉注意力后，手部相关指标下降最为突出，说明二值交互掩码对精细手指级建模不可或缺。
- **移除级联架构**：将两阶段生成合并为单阶段联合生成，身体与手部指标均受损，支持“先身体后手部”的分解策略。
- **移除推理时空间引导（w/o spatial guidance）**：推理阶段禁用手臂关节距离最小化，导致空间对齐精度下降，尤其影响近距离交互动作。

### 用户研究

Table 4 报告了五点李克特量表上的用户评分。ReMoS 在运动质量（3.79/5）和反应合理性（3.88/5）两个维度上均显著优于所有基线方法。相比之下，InterGen 的合理性评分仅为 2.91/5，MixNMatch 为 2.63/5。用户研究从感知层面验证了定量指标的优势：ReMoS 生成的反应运动不仅数值上更接近真值，在人类观察者眼中也更自然、更符合交互逻辑。

### 定性分析与应用

Fig. 5 展示了定性对比结果。在 Lindy Hop 和 Ninjutsu 场景中，ReMoS 合成的反应者（蓝色）与演员（红色）的空间对齐明显优于基线方法——InterGen 和 ComMDM 常出现手臂穿透或时序错位，而 ReMoS 保持了紧密且合理的相对位置关系。Fig. 1 进一步放大了手部交互细节：即使在无显式手部标签的条件下，ReMoS 也能生成手指级的接触姿态（如握持、引导），这归因于 H-XA 模块对手部交互掩码的利用。

![[assets/figures/papers/paper_list_l1765_ReMoS_3D_Motion_Conditioned_Reaction_Synthesis_for_Two_Person_Interactio/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative Results and Applications. We show some visual results and the application of ReMoS as a motion editing tool. (a) The reactor (in blue) synthesized by ReMoS has the most plausible alignment with the actor (in red) compared to the baselines. (b) We manually control the right-hand wrist joint of the reactor and let ReMoS synthesize the remaining body joints conditioned on the actor. (c) ReMoS synthesizes the reactor’s motion in-between the start and end frames*

论文还演示了 ReMoS 作为运动编辑工具的潜力（Fig. 5b-c）：用户可以手动指定反应者右手腕关节位置，ReMoS 自动补全其余身体关节；或给定起始与结束帧，生成中间过渡运动。这些应用得益于条件扩散模型的灵活采样能力。

### 推理效率与局限

当前实现的推理速度是主要瓶颈：生成 50 帧全身及手部运动约需 24 秒（身体 12.5 秒 + 手部 11.5 秒），难以满足实时交互需求。训练成本方面，Lindy Hop 约需 8 小时，Ninjutsu 约需 11 小时（NVIDIA RTX A4000）。作者指出可通过 DDIM、Pro-DDPM 等加速采样方法改善推理效率，但尚未实现。

此外，ReMoCap 数据集仅包含 Lindy Hop 和 Ninjutsu 两种动作类型，多样性有限，可能限制模型在更广泛交互场景中的泛化能力。方法当前仅支持两人交互，无法直接扩展至多人场景。关节位置表示也无法处理网格级皮肤接触和穿透问题，这在实际部署中可能产生视觉伪影。

## 定位与知识库关联

ReMoS 聚焦于**基于3D运动条件的两人交互反应合成**这一特定任务：给定演员（actor）的全身运动序列，生成反应者（reactor）的同步全身及手部运动，且无需任何动作标签或文本提示。该任务位于条件运动生成、人体交互建模与扩散模型的交叉地带，与现有工作形成以下谱系关系。

### 与现有基线的关键差异

现有两人交互运动生成方法可大致分为三类，ReMoS 在每一类上都引入了结构性改进：

1. **基于标签或文本的交互生成方法**：**InterGen** 等文本到两人运动的扩散模型需要文本提示作为条件，无法直接从演员运动生成反应。ReMoS 将条件从文本切换为演员的3D运动序列，使反应生成更直接且精确。

2. **角色感知的交互生成方法**：**RAIG** 等角色感知方法虽考虑交互角色，但依赖动作标签。ReMoS 通过级联扩散模型隐式学习角色间的时空同步性，消除了对标签的依赖。

3. **基于通信机制的扩散模型**：**ComMDM** 等通信式两人扩散模型在去噪过程中交换信息，但未显式建模手部交互和精细时空依赖。ReMoS 的联合时空交叉注意力（CoST-XA）和手部交互感知交叉注意力（H-XA）填补了这一空白。

在方法层面，ReMoS 的核心贡献在于五个关键设计（Table 2 消融实验验证各模块必要性）：

| 设计槽位 | 基线做法 | ReMoS 做法 |
|---------|---------|-----------|
| 交叉注意力 | 顺序空间-时间或仅时间注意力 | 联合时空交叉注意力（CoST-XA） |
| 生成策略 | 单阶段联合生成 | 级联两阶段（身体→手部） |
| 手部交互建模 | 隐式或不建模 | 手部交互感知交叉注意力（H-XA）+ 二值交互掩码 |
| 反应损失 | 仅标准重建损失 | 距离感知反应损失（指数衰减权重） |
| 推理时引导 | 无（标准DDPM） | 手臂关节空间引导 |

### 适用边界与局限

**适用场景**：ReMoS 适用于两人近距离交互场景下的反应运动生成，尤其擅长需要精细手部交互的动作类型（如 Lindy Hop 舞蹈、Ninjutsu 对练）。其级联架构和 H-XA 机制使其在手指级接触建模上具有独特优势（Fig. 1 展示的手指级接触无需额外标签即可生成）。

**已知局限**（论文明确列出）：

1. **推理速度瓶颈**：生成 50 帧全身及手部运动约需 24 秒（身体 12.5s + 手部 11.5s），难以满足实时应用需求。
2. **表示层面限制**：仅使用关节位置表示，无法直接处理网格级皮肤接触和穿透问题，交互真实感受限于关节级对齐。
3. **数据多样性不足**：ReMoCap 数据集仅包含 Lindy Hop 和 Ninjutsu 两种动作类型，模型在更广泛交互类型上的泛化能力有待验证。
4. **交互人数限制**：当前框架仅支持两人交互，无法扩展到多人场景。

### 开放问题与后续方向

论文明确指出的开放问题为后续工作提供了直接切入点：

- **推理加速**：采用 DDIM、Pro-DDPM 等加速采样方法以降低 24s 的推理延迟。
- **多人扩展**：将级联扩散框架从两人推广到多人交互运动生成。
- **场景感知交互**：引入场景上下文，使反应运动不仅与演员同步，还与物理环境协调。
- **网格级建模**：整合网格级接触建模以提高交互真实感，解决穿透问题。
- **数据与泛化**：采集更多样化的复杂交互数据以提升跨动作类型的泛化能力。

### 知识库定位

ReMoS 在条件运动生成领域建立了**从演员运动到反应者运动的直接映射**这一新范式。与 InterGen 等文本条件方法互补，ReMoS 的运动条件设置更适用于交互编辑、运动补全等无需文本描述的应用场景。其级联扩散 + 联合时空注意力的架构设计为后续的交互运动生成工作提供了可复用的技术框架，而 ReMoCap 数据集则为该方向提供了首个包含精细手部标注的两人交互基准。

## 原文 PDF

![[paperPDFs/ECCV_2024/ReMoS_3D_Motion_Conditioned_Reaction_Synthesis_for_Two_Person_Interactions.pdf]]
