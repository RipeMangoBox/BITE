---
title: Cross-Axis Feature Fusion with Joint-Wise Motion Difference Prediction for Text-Based 3D Human Motion Editing
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Cross_Axis_Feature_Fusion_with_Joint_Wise_Motion_Difference_Prediction_for_Text_Based_3D_Human_Motion_Editing.pdf
aliases:
- CAFFJWMDP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 引入关节锚定Transformer和基于Soft-DTW的关节运动差异预测辅助任务，显式驱动模型学习各关节的轨迹变化量，并通过跨轴融合块整合时空信息。
primary_logic: 将人体运动数据分解为空间关节轴和时间帧轴，分别用两个Transformer编码，再通过跨轴注意力实现信息交互，配备对旋转轨迹形状差异鲁棒的Soft-DTW辅助监督，能有效提升文本运动编辑的忠实度和生成质量。
claims:
- 所提出的架构由关节锚定Transformer、时间锚定Transformer和跨轴融合块组成，提供关节感知条件信号。
- 辅助任务使用Soft-DTW距离作为监督，引导模型理解各关节的变化量。
- 在MotionFix数据集上，该方法在生成-目标运动检索指标和FID上均达到最优。
- 消融实验表明，Soft-DTW辅助任务相对于L2距离能显著提升编辑性能。
---

# Cross-Axis Feature Fusion with Joint-Wise Motion Difference Prediction for Text-Based 3D Human Motion Editing

> [!tip] 核心洞察
> 将人体运动数据分解为空间关节轴和时间帧轴，分别用两个Transformer编码，再通过跨轴注意力实现信息交互，配备对旋转轨迹形状差异鲁棒的Soft-DTW辅助监督，能有效提升文本运动编辑的忠实度和生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 跨轴特征融合与关节运动差异预测的文本驱动3D人体运动编辑 |
| 英文题名 | Cross-Axis Feature Fusion with Joint-Wise Motion Difference Prediction for Text-Based 3D Human Motion Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Han_Cross-Axis_Feature_Fusion_with_Joint-Wise_Motion_Difference_Prediction_for_Text-Based_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Cross-Axis Feature Fusion with Joint-Wise Motion Difference Prediction |
| Dataset | MotionFix |

> [!tip] 效果简介
> - MotionFix 上，R@1 (Batch retrieval) 74.38；FID 0.097；R@1 (Test Set) 29.45。

## 概述

**问题瓶颈**：文本驱动的3D人体运动编辑要求模型根据自然语言指令精确修改源动作的局部关节行为。现有方法（如**SimMotionEdit** (Li et al., CVPR 2025)）仅建模帧级时间变化，缺少对关节级空间变化的显式建模与监督，导致无法精确控制编辑中具体关节的修改量。

**核心思路**：本文提出**跨轴特征融合与关节运动差异预测**（Cross-Axis Feature Fusion with Joint-Wise Motion Difference Prediction）方法。其核心洞察在于将人体运动数据沿空间关节轴和时间帧轴进行分解，分别用关节锚定Transformer和时间锚定Transformer编码，再通过跨轴注意力实现信息交互；同时引入基于Soft-DTW的关节级运动差异预测作为辅助任务，驱动模型学习各关节轨迹的变化量。Soft-DTW对旋转轨迹的局部时间偏移具有天然鲁棒性，相较于L2距离能更合理地度量运动差异。

**方法定位**：该方法属于条件扩散模型范式，以DiT（Diffusion Transformer）作为生成主干，在特征编码阶段将单一时序Transformer替换为双轴Transformer加跨轴融合块，并将辅助监督从帧级相似度预测升级为关节级Soft-DTW差异预测。相比**TMED** (Athanasiou et al., SIGGRAPH Asia 2024) 等监督式基线，本方法在架构层面实现了关节感知的条件信号注入。

**主要结果**：在MotionFix基准上，该方法在生成-目标运动检索指标（R@1达74.38）和FID（0.097）上均达到最优。消融实验证实，Soft-DTW辅助任务相对于L2距离能显著提升编辑性能，且同时使用帧级运动相似度预测和关节级Soft-DTW距离预测两种辅助任务可达到最佳效果。

## 背景与动机

文本驱动的3D人体运动编辑旨在根据自然语言指令修改给定的源运动序列，同时保留未指定的运动内容。该任务在动画制作、虚拟现实和游戏开发中具有重要应用价值，但其核心挑战在于：模型必须精确理解文本指令中隐含的“修改哪个关节、修改多少、如何修改”的细粒度语义，并将其转化为对特定关节轨迹的空间-时间调整。

现有方法在处理这一挑战时存在一个关键瓶颈：它们主要建模帧级（frame-level）的时间变化，而**缺少对关节级（joint-level）空间变化的显式建模与监督**。以强基线方法**SimMotionEdit**（Li et al., CVPR 2025）为例，其采用条件Transformer对源运动与文本进行帧级聚合，并辅以帧级运动相似度预测作为辅助任务。这种设计虽然能捕捉运动整体的时序演变，但无法显式地控制编辑过程中具体关节的修改量——当指令要求“抬起左手”时，模型缺乏机制来区分左手关节与右手关节应受到的不同程度的修改信号。

更一般地，人体运动数据天然具有两个正交的轴：**空间关节轴**（每个关节在整个序列上的轨迹）和**时间帧轴**（每一帧的全身姿态）。现有方法通常将运动展平为帧序列进行处理，忽视了关节轴上的全局轨迹信息，导致两个后果：（1）关节轨迹的形状相似性难以被有效捕获，尤其当源运动与目标运动在局部时间对齐上存在偏移时；（2）辅助监督信号只能作用于帧级表示，无法为关节级编码器提供直接的训练指导。

本文的动机正是针对上述缺口，提出一种**显式建模关节级运动差异**的编辑框架。核心思路是：将运动数据沿关节轴和时间轴分别编码，通过跨轴注意力实现信息交互，并引入基于**Soft-DTW**的关节运动差异预测作为辅助任务，驱动模型学习每个关节在编辑中应发生的轨迹变化量。Soft-DTW作为可微的动态时间规整距离，对旋转轨迹的形状差异敏感，同时对局部时间偏移鲁棒，这使得辅助监督能够更准确地反映关节运动的语义变化，而非被时间对齐噪声所干扰。

## 核心创新

### 问题瓶颈与设计动机

现有文本驱动的人体运动编辑方法（如 **SimMotionEdit**，Li et al., CVPR 2025）主要依赖单一的条件 Transformer 对帧级时序变化进行建模，并通过基于 L2 距离的帧级运动相似度预测作为辅助监督。这一范式存在一个关键盲区：**缺乏对关节级空间变化的显式建模与监督**。当编辑指令仅涉及特定身体部位（如“抬高右手”）时，帧级聚合特征难以精确刻画各关节的轨迹修改量，导致编辑结果在空间粒度上不够精准。

### 核心创新：跨轴特征融合与关节级 Soft-DTW 监督

本文的核心创新在于将人体运动数据解耦为两个正交轴——**空间关节轴**与**时间帧轴**——并分别建模，再通过跨轴注意力机制实现信息交互，同时引入基于 Soft-DTW 的关节级运动差异预测作为辅助任务。具体体现在以下三个 changed slots：

#### Changed Slot 1：从单一帧级编码器到双轴 Transformer 架构

| 维度 | 基线方法（SimMotionEdit） | 本文方法 |
|------|--------------------------|----------|
| 特征编码器 | 单一条件 Transformer（帧级聚合） | 关节锚定 Transformer + 时间锚定 Transformer + 跨轴融合块 |

- **关节锚定 Transformer（Joint-Anchored Transformer）**：以每个关节为锚点，聚合该关节在整个序列上的全局轨迹特征，输出关节级表示 $h_{\mathrm{joint}}$。这使得模型能够捕捉到“某一关节在整段运动中的行为模式”，而非仅关注某一帧的瞬时姿态。
- **时间锚定 Transformer（Time-Anchored Transformer）**：以每一帧为锚点，编码该帧的全身姿态特征，输出帧级表示 $h_{\mathrm{time}}$，保留时序上下文。
- **跨轴融合块（Cross-Axis Fusion Block）**：以帧特征 $h_{\mathrm{time}}$ 为 Query，关节特征 $h_{\mathrm{joint}}$ 为 Key 和 Value，通过多头注意力实现跨轴信息交互，产生融合表示 $h_{\mathrm{fusion}}$。这一设计使得每一帧的表示能够动态地关注到最相关的关节轨迹信息，从而为扩散模型提供**关节感知的条件信号**。

#### Changed Slot 2：从帧级 L2 相似度到关节级 Soft-DTW 运动差异预测

| 维度 | 基线方法（SimMotionEdit） | 本文方法 |
|------|--------------------------|----------|
| 辅助任务 | 帧级运动相似度预测（基于 L2） | 关节级 Soft-DTW 运动差异预测 |

辅助任务的设计从“整帧相似度”下沉到“逐关节运动差异”。具体而言：

1. **目标定义**：对于源运动 $S$ 和目标运动 $T$ 的每个旋转通道 $j$，计算其 Soft-DTW 距离作为监督信号：
   $$d_j = \mathrm{SoftDTW}_{\gamma}(S_j', T_j') \in \mathbb{R}$$
   其中 $\mathrm{SoftDTW}_{\gamma}$ 是可微的软动态时间规整距离，定义为：
   $$\mathrm{SoftDTW}_{\gamma}(x, y) = \mathrm{softmin}_{\pi \in \mathcal{A}}^{(\gamma)} \sum_{(n,m) \in \pi} d(x_n, y_m)$$

2. **预测与监督**：从关节锚定 Transformer 的输出 $h_{\mathrm{joint}}'$ 通过回归头 $\varphi_{\mathrm{reg}}$ 预测每个通道的运动差异 $\hat{d}_j$，并以 MSE 损失进行监督：
   $$\mathcal{L}_{\mathrm{aux}} = \frac{1}{K'} \sum_{j=1}^{K'} (\hat{d}_j - d_j)^2$$

选择 Soft-DTW 而非 L2 距离的核心原因在于：Soft-DTW 对轨迹的**局部时间偏移和持续时间差异具有天然的鲁棒性**，能够更准确地衡量两段运动在“形状”层面的相似度，而非被时间对齐误差所干扰。这引导关节锚定 Transformer 学习到更具语义意义的关节轨迹变化表征。

#### Changed Slot 3：从无显式跨轴融合到注意力驱动的轴间信息交互

基线方法的条件 Transformer 仅在帧维度上操作，空间信息隐含在帧内关节排列中，缺乏显式的轴间信息路由。本文的跨轴融合块通过将帧特征作为 Query 去查询关节特征，实现了**帧对关节轨迹的选择性关注**——每一帧可以自适应地决定“当前时刻哪些关节的全局行为最值得参考”。这种设计使得融合特征同时携带了局部时序上下文和全局关节轨迹信息，为后续的扩散生成提供了更丰富的条件信号。

### 整体架构与因果链路

完整的 pipeline 由以下模块串联构成：

1. **双轴编码**：源运动 $S$ 和文本指令 $c$ 同时输入关节锚定 Transformer 和时间锚定 Transformer，分别产出 $h_{\mathrm{joint}}$ 和 $h_{\mathrm{time}}$。
2. **跨轴融合**：跨轴融合块以 $h_{\mathrm{time}}$ 为 Query、$h_{\mathrm{joint}}$ 为 Key/Value 进行多头注意力，输出 $h_{\mathrm{fusion}}$。
3. **条件扩散生成**：$h_{\mathrm{fusion}}$ 与加噪运动 $M_{\tau}$ 拼接后输入 DiT（Diffusion Transformer），通过 DDPM 反向采样逐步去噪生成编辑后的运动。
4. **辅助监督**：回归头从 $h_{\mathrm{joint}}'$ 预测逐通道 Soft-DTW 距离，以 $\mathcal{L}_{\mathrm{aux}}$ 进行监督，与扩散模型的噪声预测损失 $\mathcal{L}_{\mathrm{diff}}$ 联合训练。

因果链路可概括为：**关节锚定编码 → Soft-DTW 辅助监督 → 关节轨迹差异感知 → 跨轴融合 → 关节感知条件信号 → 精准编辑生成**。消融实验（Table 2）证实，将辅助任务从 L2 替换为 Soft-DTW 可带来显著的性能增益，且同时使用帧级相似度预测和关节级 Soft-DTW 预测两种辅助任务时达到最优，验证了双粒度监督的互补性。

## 整体框架

该方法构建了一个以**条件扩散模型**为核心的文本驱动人体运动编辑框架。给定源运动序列 $S$ 和文本编辑指令 $c$，模型的目标是生成编辑后的运动 $\hat{M}$，使其既满足文本指令的语义要求，又保留源运动中不应被修改的内容。

整个 pipeline 由三个关键阶段串联而成：**特征编码**、**条件注入**和**扩散生成**。

### 特征编码：双轴锚定与跨轴融合

特征编码器 $f(S, c)$ 是整个框架的核心创新所在。它由三个模块级联构成：

1. **关节锚定 Transformer（Joint-Anchored Transformer）**：将源运动 $S$ 和文本指令 $c$ 作为输入，沿关节轴对每个关节在整个时间序列上的全局轨迹进行编码，输出关节级特征 $h_{\mathrm{joint}}$。该模块的设计动机是显式捕获编辑中“哪些关节需要被修改、修改量有多大”的空间结构信息。

2. **时间锚定 Transformer（Time-Anchored Transformer）**：同样以 $S$ 和 $c$ 为输入，但沿时间轴对每一帧的全身姿态进行编码，输出帧级特征 $h_{\mathrm{time}}$，负责建模编辑在时间维度上的动态模式。

3. **跨轴融合块（Cross-Axis Fusion Block）**：以 $h_{\mathrm{time}}$ 为 Query、$h_{\mathrm{joint}}$ 为 Key 和 Value，通过多头注意力机制实现时空信息的交互融合，最终产生融合特征 $h_{\mathrm{fusion}}$。这种设计使得每一帧的表示能够自适应地聚合来自各关节轨迹的全局信息，从而为扩散模型提供关节感知的条件信号。

### 条件注入与扩散生成

融合特征 $h_{\mathrm{fusion}}$ 随后被拼接到扩散模型（DiT）的噪声运动输入中，作为生成过程的条件信号。扩散模型采用 DDPM 框架，其训练目标为噪声预测损失：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\tau, \epsilon} \left[ \| g\left(M_{\tau}; f(S, c), \tau\right) - \epsilon \|_2^2 \right]$$

推理时，从纯噪声 $M_T \sim \mathcal{N}(0, I)$ 出发，通过 300 步 DDPM 反向采样逐步去噪，每一步利用预测噪声 $\hat{\epsilon}_\tau$ 更新运动表示：

$$M_{\tau-1} = \frac{1}{\sqrt{\alpha_{\tau}}} \left( M_{\tau} - \frac{1-\alpha_{\tau}}{\sqrt{1-\bar{\alpha}_{\tau}}} \hat{\epsilon}_{\tau} \right) + \sqrt{\tilde{\beta}_{\tau}} z_{\tau}$$

最终得到编辑后的运动 $\hat{M} = M_0$。

### 辅助监督：关节级 Soft-DTW 运动差异预测

在训练阶段，框架引入了一个额外的辅助任务来强化关节锚定 Transformer 的学习。具体而言，在关节特征 $h_{\mathrm{joint}}$ 之上附加一个回归头 $\varphi_{\mathrm{reg}}$，为每个旋转通道 $j$ 预测一个标量值 $\hat{d}_j$：

$$\hat{d}_j = \left[ \varphi_{\mathrm{reg}} \big( h_{\mathrm{joint}}^{\prime} \big) \right]_j \in \mathbb{R}$$

该预测值的目标是源动作和目标动作在对应通道上的 Soft-DTW 距离：

$$d_j = \mathrm{SoftDTW}_{\gamma}(S_j^{\prime}, T_j^{\prime}) \in \mathbb{R}$$

辅助损失定义为预测值与真实 Soft-DTW 距离之间的均方误差：

$$\mathcal{L}_{\mathrm{aux}} = \frac{1}{K^{\prime}} \sum_{j=1}^{K^{\prime}} \bigl( \hat{d}_j - d_j \bigr)^2$$

总训练损失为 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{diff}} + \mathcal{L}_{\mathrm{aux}}$。Soft-DTW 作为距离度量的关键优势在于其对轨迹形状相似性的捕捉能力以及对局部时间偏移的鲁棒性——相比 L2 距离，它能更准确地反映关节运动模式的变化程度，从而引导关节锚定 Transformer 学习到更有判别力的关节级表示。

整个框架的输入输出流可概括为：**源运动 + 文本指令 → 双轴编码器 → 跨轴融合 → DiT 条件生成 → 编辑后运动**，其中辅助的 Soft-DTW 回归任务仅在训练时生效，为编码器提供额外的关节级监督信号。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Cross_Axis_Feature/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed approach and joint-wise supervision. (a) A joint-anchored transformer and a time-anchored transformer produce enhanced features*

## 核心模块与公式推导

### 3.1 扩散模型基础：噪声预测与反向采样

方法采用扩散模型作为运动生成骨架。给定源运动 $S$ 和文本指令 $c$，特征编码器 $f$ 提取条件信号 $f(S, c)$，用于指导去噪网络 $g$ 从噪声中恢复目标运动。

**噪声预测损失** 训练去噪网络以最小化预测噪声与真实噪声之间的 $L_2$ 距离：

$$\mathcal{L}_{\mathrm{diff}} = \mathbb{E}_{\tau, \epsilon} \left[ \| g\left(T_{\tau}; f(S, c), \tau\right) - \epsilon \|_2^2 \right] \tag{1}$$

其中 $T_{\tau}$ 为在时间步 $\tau$ 加噪后的目标运动，$\epsilon$ 为标准高斯噪声。

**DDPM 反向采样** 推理时，从纯噪声 $M_T \sim \mathcal{N}(0, I)$ 出发，通过 300 步 DDPM 采样逐步去噪生成编辑后的运动：

$$M_{\tau-1} = \frac{1}{\sqrt{\alpha_{\tau}}} \left( M_{\tau} - \frac{1-\alpha_{\tau}}{\sqrt{1-\bar{\alpha}_{\tau}}} \hat{\epsilon}_{\tau} \right) + \sqrt{\tilde{\beta}_{\tau}} z_{\tau} \tag{3}$$

其中 $\hat{\epsilon}_{\tau} = g(M_{\tau}; f(S, c), \tau)$ 为当前步的噪声预测，$\alpha_{\tau}$、$\bar{\alpha}_{\tau}$、$\tilde{\beta}_{\tau}$ 为 cosine 噪声调度器的参数，$z_{\tau} \sim \mathcal{N}(0, I)$ 为随机噪声项。

### 3.2 双轴锚定编码器与跨轴融合

特征编码器 $f$ 的核心由三个模块构成：**关节锚定 Transformer**、**时间锚定 Transformer** 和**跨轴融合块**。其设计目标是将源运动 $S$ 分解为空间关节轴和时间帧轴两个正交维度分别编码，再通过注意力机制实现信息交互。

**关节锚定 Transformer** 以每个关节在整个序列上的全局轨迹为输入单元，输出关节级特征 $h_{\mathrm{joint}}$。该模块使模型能够捕捉各关节跨时间的运动模式，为后续关节级差异预测提供表示基础。

**时间锚定 Transformer** 以每一帧的全身姿态为输入单元，输出帧级特征 $h_{\mathrm{time}}$。该模块负责建模帧间的时序依赖关系。

**跨轴融合块** 接收 $h_{\mathrm{time}}$ 作为 Query，$h_{\mathrm{joint}}$ 同时作为 Key 和 Value，通过多头注意力实现跨轴信息融合：

- Query（$h_{\mathrm{time}}$）携带"当前帧需要怎样的关节信息"的查询信号；
- Key/Value（$h_{\mathrm{joint}}$）提供各关节的全局轨迹上下文。

融合后的特征 $h_{\mathrm{fusion}}$ 与加噪运动输入拼接，作为 DiT 的条件信号。这种设计使扩散模型同时获得帧级时序上下文和关节级空间上下文，且文本指令的信息已通过两个 Transformer 隐式融入融合特征中。

### 3.3 关节级 Soft-DTW 运动差异预测

为弥补帧级运动相似度预测（如 SimMotionEdit 所用）缺少关节级空间监督的不足，方法引入了一个辅助回归任务：从关节特征预测源运动与目标运动在各旋转通道上的 Soft-DTW 距离。

**回归预测** 对关节锚定 Transformer 的输出 $h_{\mathrm{joint}}'$，通过回归头 $\varphi_{\mathrm{reg}}$ 预测每个旋转通道 $j$ 的运动差异标量：

$$\hat{d}_j = \left[ \varphi_{\mathrm{reg}} \big( h_{\mathrm{joint}}' \big) \right]_j \in \mathbb{R}, \quad j = 1, \ldots, K' \tag{4}$$

**Soft-DTW 距离** 作为监督目标，对源运动通道 $S_j'$ 和目标运动通道 $T_j'$ 计算可微的软动态时间规整距离：

$$d_j = \mathrm{SoftDTW}_{\gamma}(S_j', T_j') \in \mathbb{R} \tag{7}$$

其中 Soft-DTW 定义为：

$$\mathrm{SoftDTW}_{\gamma}(x, y) = \mathrm{softmin}_{\pi \in \mathcal{A}}^{(\gamma)} \sum_{(n,m) \in \pi} d(x_n, y_m) \tag{6}$$

与经典 DTW（$\mathrm{DTW}(x, y) = \min_{\pi \in \mathcal{A}} \sum_{(n,m) \in \pi} d(x_n, y_m)$，式 5）相比，Soft-DTW 用 softmin 替代硬最小化，保持可微性且对局部时间偏移具有鲁棒性。温度参数 $\gamma$ 控制软化的程度：$\gamma \to 0$ 时趋近经典 DTW，$\gamma \to \infty$ 时退化为平均对齐。

**辅助损失** 采用均方误差监督预测值与真实 Soft-DTW 距离的一致性：

$$\mathcal{L}_{\mathrm{aux}} = \frac{1}{K'} \sum_{j=1}^{K'} \bigl( \hat{d}_j - d_j \bigr)^2 \tag{8}$$

该辅助任务的核心作用在于：显式驱动关节锚定 Transformer 学习各关节轨迹形状的差异量，而 Soft-DTW 对起始时间和持续时间的差异具有天然容忍度，使其能专注于轨迹形状本身的相似性。这与帧级运动相似度预测形成互补——前者关注"每个关节改了多少"，后者关注"整体运动有多像"。

**总训练目标** 为扩散损失与辅助损失的加权组合，联合优化去噪质量和关节级差异感知能力。

## 实验与分析

### 主实验结果

为评估所提方法的有效性，本文在 MotionFix 数据集上与当前最优的文本驱动运动编辑方法进行了全面对比。MotionFix 包含 6,730 个带文本指令标注的「源运动-目标运动」三元组，评估采用基于 TMR 特征空间的生成-目标运动检索指标（R@1、R@2、R@3、AvgR）和 FID。

定量结果如 Table 1 所示。所提方法在所有检索指标和 FID 上均达到最优。在批量检索设置下，R@1 达到 **74.38**，显著超越现有方法；FID 降至 **0.097**，表明生成运动与目标运动在分布层面高度一致。在测试集检索设置下，R@1 达到 **29.45**（Table 4 中 Ours 行）。这些结果验证了跨轴特征融合与关节级运动差异预测联合设计的有效性。

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Cross_Axis_Feature/figures/003_Table_1.jpg]]
*Table 1: Quantitative results. We compare the generated-to-target motion-to-motion retrieval performance of the proposed method with that of state-of-the-art text-based motion editing models. We report the top-1 (R@1), top-2 (R@2), and top-3 (R@3) retrieval accuracies along with the average rank (AvgR). To evaluate the fidelity and diversity of the generated motion, we additionally compute the FID between the edited motions and the target motions. Metrics are marked with ↑ (higher is better) or ↓ (lower is better). We highlight the best results in bold and the second-best results with an underline*

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Cross_Axis_Feature/figures/006_Table_4.jpg]]
*Table 4: Ablation results on additional explicit text conditioning. Ours uses only the implicit fused feature*

定性结果如 Figure 2 所示。与 **TMED**（Athanasiou et al., SIGGRAPH Asia 2024）和 **SimMotionEdit**（Li et al., CVPR 2025）等基线方法相比，所提方法生成的编辑运动在时序一致性和编辑精确度上均表现更优，能够更准确地响应文本指令对特定关节的修改要求。

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Cross_Axis_Feature/figures/002_Figure_2.jpg]]
*Figure 2: Qualitative results. We visualize the source motion, ground truth, and the edited motions from our method and competing methods, given a text instruction. To effectively illustrate the temporal progression, rendered meshes are translated to the right over time. For each motion, frame recency is encoded by saturation: lower saturation represents earlier frames, while higher saturation indicates more recent frames. Best viewed zoomed in*

### 消融实验

#### 辅助任务的贡献

Table 2 分析了帧级运动相似度预测（Motion Sim.）和关节级运动差异预测（Joint Delta）两个辅助任务的影响。核心发现如下：

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Cross_Axis_Feature/figures/004_Table_2.jpg]]
*Table 2: We conducted an ablation study to analyze the impact of auxiliary tasks on the text-based human motion editing performance. We evaluated the contributions of both the motion similarity prediction (Motion Sim.) task and the joint-wise distance prediction task (Joint Delta) by experimenting with whether each task was performed. For the joint-wise motion distance prediction task, we additionally conducted an experiment using the L2 distance as the distance metric, comparing it against Soft-DTW. Metrics are marked with ↑ (higher is better) or ↓ (lower is better). We highlight the best results in bold and the second-best results with an underline*

- **双辅助任务协同最优**：同时使用两个辅助任务时，所有指标均达到最佳。仅使用关节级距离预测时性能次之，仅使用帧级相似度预测时性能进一步下降，完全移除辅助任务时性能最差。这表明两个辅助任务从不同粒度提供互补的监督信号。
- **Soft-DTW 显著优于 L2 距离**：在关节级距离预测任务中，将 Soft-DTW 替换为 L2 距离会导致性能大幅下降。原因在于 L2 距离对轨迹的局部时间偏移敏感，而 Soft-DTW 通过可微的动态时间规整能够鲁棒地捕捉旋转轨迹的形状相似性，从而提供更具信息量的监督信号。

#### Soft-DTW 温度参数 γ 的敏感性

Table 3 展示了 Soft-DTW 的温度参数 γ 在 0.1 到 50 范围内变化时的性能表现。结果表明，模型对该参数不敏感，各 γ 值下的检索指标和 FID 保持稳定。这一鲁棒性降低了超参数调优的工程负担，验证了 Soft-DTW 作为辅助监督的实用性。

![[assets/figures/papers/paper_list_l12_https_openaccess_thecvf_com_content_CVPR2026_html_Han_Cross_Axis_Feature/figures/005_Table_3.jpg]]
*Table 3: We analyze the model’s performance by varying the γ value for Soft-DTW from 0.1 to 50. Metrics are marked with ↑ (higher is better) or ↓ (lower is better). We highlight the best results in bold and the second-best results with an underline*

#### 显式文本条件的影响

Table 4 探究了在扩散模型（DiT）中是否提供额外的显式文本条件对性能的影响。令人意外的是，仅使用隐式融合特征（即跨轴融合块的输出）而不提供额外显式文本条件时，模型在测试集检索指标上达到最优。当同时输入显式文本条件时，R@1 反而下降。一个可能的解释是：跨轴融合块已经通过注意力机制将文本信息充分整合到条件特征中，额外的显式文本条件引入了冗余或冲突的信号，干扰了扩散模型的去噪过程。该现象仍需进一步研究验证。

#### 架构组件的消融

Table 4 还分析了编码器架构的影响。仅使用关节锚定 Transformer 的条件优于仅使用时间锚定 Transformer，说明关节级全局轨迹特征对编辑任务的贡献更大。完整架构（关节锚定 + 时间锚定 + 跨轴融合）在所有指标上均优于单一编码器，验证了双轴特征互补与跨轴信息交互的必要性。

### 训练与推理配置

模型使用 AdamW 优化器训练，学习率 1×10⁻⁴，批大小 64，训练 1,500 个 epoch。推理采用 DDPM 采样，固定 300 步扩散过程，配合余弦噪声调度器。采用双向条件策略，文本和源运动的引导尺度均设为 2.0。

### 局限性与待验证问题

本文未报告显式的失败模式分析。一个开放的疑问是：为何在隐式融合特征已包含文本信息的情况下，增加显式文本条件反而导致性能下降？该现象可能指向条件信号冗余或冲突的深层机制，需通过更细粒度的注意力分析和梯度归因实验进一步验证。

## 方法谱系与知识库定位

### 核心方法定位

本文提出的**跨轴特征融合与关节运动差异预测**方法，本质上是对文本驱动人体运动编辑任务中“条件信号编码”环节的系统性重构。其方法论定位可从以下两个维度理解：

**（1）相对于监督式运动编辑基线的改进路径**

该方法建立在两条基线的演进脉络之上：

- **TMED**（Athanasiou et al., SIGGRAPH Asia 2024）作为监督式文本运动编辑的早期工作，确立了“源运动+文本指令→编辑运动”的任务范式，但其条件编码机制较为基础，缺乏对运动时空结构的显式建模。

- **SimMotionEdit**（Li et al., CVPR 2025）通过引入条件Transformer和帧级运动相似度预测辅助任务，显著提升了编辑精度，成为本文的直接对标基线。然而，SimMotionEdit的核心瓶颈在于：其条件编码仅建模**帧级**时间变化，缺少对**关节级**空间变化的显式建模与监督。这意味着模型无法精确感知“哪些关节需要被修改、修改幅度多大”，导致编辑粒度粗放。

本文的改进策略是**将条件编码从一维（帧级时间轴）扩展为二维（关节空间轴+帧时间轴）**，并辅以相应的辅助监督，从而实现对编辑区域的精细化控制。

**（2）跨轴特征融合的方法论贡献**

该方法的核心创新在于将人体运动数据显式分解为两个正交维度并分别建模：

| 模块 | 编码维度 | 功能 |
|------|----------|------|
| 关节锚定Transformer | 每个关节在完整序列上的全局轨迹 | 捕获关节级运动模式与变化量 |
| 时间锚定Transformer | 每一帧的全身姿态 | 捕获帧级时序依赖 |
| 跨轴融合块 | 以帧特征为Query、关节特征为Key/Value的多头注意力 | 实现时空信息的双向交互 |

这种“分轴编码→跨轴融合”的架构设计，在方法论上区别于现有工作中常见的单一序列编码范式。它使得条件信号同时携带“哪些帧需要改变”（时间轴）和“哪些关节需要改变”（空间轴）的双重信息，为扩散模型的去噪过程提供了更精准的引导。

### 辅助任务设计的理论动机

本文引入的**关节级Soft-DTW运动差异预测**辅助任务，其设计逻辑值得关注：

- **为什么用Soft-DTW而非L2？** 消融实验（Table 2）表明，使用Soft-DTW作为距离度量显著优于L2。其理论原因在于：编辑前后的运动可能在局部时间轴上存在偏移（如动作起始时间不同、持续时间缩放），L2距离对这类时间错位高度敏感，会产生误导性的监督信号；而Soft-DTW通过动态规划对齐轨迹形状，对局部时间偏移具有天然鲁棒性，能更准确地反映轨迹形状的相似度。

- **为什么是关节级而非帧级？** 帧级相似度预测（SimMotionEdit的辅助任务）只能告诉模型“整个运动序列与目标的整体相似度”，而关节级差异预测直接告诉模型“每个关节各自需要改变多少”。这种细粒度监督与关节锚定Transformer的编码结构形成闭环，驱动模型学习各关节的轨迹变化量。

### 适用边界与局限

基于论文提供的实验证据和分析，该方法的适用边界可归纳如下：

**适用场景：**
- 文本驱动的局部运动编辑，特别是需要精确控制特定身体部位修改量的任务
- 编辑前后运动存在时间偏移的场景（Soft-DTW的鲁棒性优势）
- 基于MotionFix数据集的监督式编辑范式

**已知局限与开放问题：**

1. **显式文本条件的反直觉退化**：消融实验（Table 4）揭示了一个值得关注的现象——在模型已通过融合特征接收隐式文本信息的情况下，额外增加显式文本条件反而导致检索性能下降。论文将此作为开放问题提出，但未给出机制层面的解释。一种可能的假设是：跨轴融合块已经完成了文本与运动的充分对齐，额外的显式条件引入了冗余信号，导致条件空间过约束。这一点需要后续工作验证。

2. **数据集依赖性**：该方法在MotionFix数据集（6,730个标注三元组）上进行训练和评估，其对其他运动编辑数据集或更广泛编辑类型的泛化能力尚未验证。

3. **计算开销**：双Transformer编码器加跨轴融合的设计相比单编码器基线增加了计算复杂度，论文未提供推理延迟或参数量对比，实际部署效率需要进一步评估。

### 在知识库中的位置

该方法在文本驱动运动编辑领域的方法谱系中，可定位为**从“帧级条件编码”向“时空双轴条件编码”演进的关键节点**。其方法论贡献——将运动数据分解为关节轴和时间轴分别建模再融合——为后续工作提供了一个可扩展的架构模板。未来工作可能沿以下方向延伸：（1）将双轴分解推广到更多运动表征维度；（2）探索更高效的跨轴融合机制以降低计算开销；（3）将显式文本条件退化的现象理论化，设计更优的条件注入策略。

## 原文 PDF

![[paperPDFs/CVPR_2026/Cross_Axis_Feature_Fusion_with_Joint_Wise_Motion_Difference_Prediction_for_Text_Based_3D_Human_Motion_Editing.pdf]]