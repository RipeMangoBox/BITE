---
title: "DreamMotion: Space-Time Self-Similar Score Distillation for Zero-Shot Video Editing"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/DreamMotion_Space_Time_Self_Similar_Score_Distillation_for_Zero_Shot_Video_Editing.pdf
project_link: https://hyeonho99.github.io/dreammotion
code_link: null
aliases:
- DreamMotion
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过匹配原始视频与编辑视频在扩散特征上的时空自相似性，能够有效约束结构并平滑时间动态，从而在优化过程中解耦外观注入与运动保持。"
primary_logic: "利用预训练文本到视频扩散模型内部的深度特征自相似性作为结构保持线索，结合分数蒸馏优化和掩码梯度过滤，实现了无需训练、模型无关的零样本视频外观编辑，同时精准保留了原始运动与结构。"
claims:
- "传统基于祖先采样的零样本视频编辑无法捕捉复杂真实世界运动。"
- "分数蒸馏优化（V-DDS）能够注入目标外观，但会累积结构误差，导致运动偏离。"
- "空间自相似性匹配（S-SSM）对齐了原始与编辑视频的扩散关键帧特征，从而保持结构完整性。"
- "时间自相似性匹配（T-SSM）有效地进行了时间平滑，消除了闪烁伪影。"
---

# DreamMotion: Space-Time Self-Similar Score Distillation for Zero-Shot Video Editing

> [!tip] 核心洞察
> 利用预训练文本到视频扩散模型内部的深度特征自相似性作为结构保持线索，结合分数蒸馏优化和掩码梯度过滤，实现了无需训练、模型无关的零样本视频外观编辑，同时精准保留了原始运动与结构。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DreamMotion：基于时空自相似分数蒸馏的零样本视频编辑 |
| 英文题名 | DreamMotion: Space-Time Self-Similar Score Distillation for Zero-Shot Video Editing |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2403.12002) · [Project](https://hyeonho99.github.io/dreammotion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DreamMotion |
| Dataset | Zeroscope (非级联), Zeroscope (与DMT比较), Zeroscope (与Video-P2P比较) |

> [!tip] 效果简介
> - Zeroscope (非级联) 上，Text-Align (CLIP) 为 0.8209，对比 - (高于所有比较方法)，变化 -。
> - Zeroscope (非级联) 上，Frame-Con (CLIP) 为 0.9726，对比 - (高于所有比较方法)，变化 -。
> - Zeroscope (与DMT比较) 上，Motion-Fidelity 为 0.9259，对比 0.8697，变化 +0.0562。

## 概要

**核心问题**：零样本视频编辑面临一个根本性瓶颈——传统基于祖先采样的反向扩散方法难以在注入新外观的同时保持真实世界视频中原有的复杂运动，而直接应用分数蒸馏优化虽能引入目标外观，却会累积结构误差，导致运动偏移和闪烁伪影。

**核心结论**：DreamMotion 利用预训练文本到视频扩散模型内部深度特征的时空自相似性作为结构保持线索，在分数蒸馏优化过程中解耦外观注入与运动保持，实现了无需训练、模型无关的零样本视频外观编辑，同时精准保留了原始运动与结构完整性。

**方法定位**：DreamMotion 将视频编辑重新定义为从原始视频出发的优化问题，而非传统的从噪声出发的生成问题。其优化策略由三部分构成：视频 Delta Denoising Score 损失（V-DDS）负责注入目标外观；空间自相似性匹配（S-SSM）通过对齐扩散关键帧特征的空间自相似性图来保持每帧结构；时间自相似性匹配（T-SSM）通过匹配帧间时间自相似性矩阵实现时间平滑，消除闪烁。此外，利用检测框生成的二元掩码过滤梯度，将编辑限制在目标区域，避免模糊和过饱和。该方法可无缝适配非级联（如 Zeroscope）和级联（如 Show-1）两种视频扩散框架。

**主要结果**：在 Zeroscope 非级联设置下，DreamMotion 在文本对齐度（CLIP Text-Align: 0.8209）、帧一致性（CLIP Frame-Con: 0.9726）以及人类评估的编辑准确性（4.14/5）和结构/运动保持（4.33/5）上均优于所有对比基线。在 Show-1 级联设置下同样取得最优性能。与运动迁移方法 DMT 和局部编辑方法 Video-P2P 相比，DreamMotion 的运动保真度分别提升 0.0562 和 0.1875。消融实验证实，联合优化 V-DDS、S-SSM 和 T-SSM 是取得最优效果的必要条件。

视频编辑的核心挑战在于，如何在注入新外观的同时，精准保留原始视频中的复杂运动和结构信息。随着文本到视频（T2V）扩散模型的快速发展，零样本视频编辑——即无需针对特定视频进行微调即可完成编辑——成为一个极具吸引力的方向。然而，现有方法在处理真实世界视频中的复杂运动时，暴露出根本性的瓶颈。

**祖先采样的失效。** 当前主流的零样本视频编辑方法大多沿袭图像编辑的思路，依赖于对扩散模型进行**祖先采样**（ancestral sampling）——即从噪声或反转潜变量出发，通过反向扩散过程生成编辑后的视频。尽管这类方法（如 **Tune-A-Video**、**ControlVideo**、**TokenFlow** 等）在图像域取得了显著进展，但在视频域却面临一个致命缺陷：它们**无法捕捉复杂、真实的运动模式**。如 Fig. 2 所示，基于祖先采样的编辑结果往往产生运动失真、时序不一致的视频，因为反转过程难以将真实世界的动态信息完整编码到噪声空间中，而采样过程又缺乏有效的运动约束机制。

**分数蒸馏的潜力与陷阱。** 一个替代思路是放弃祖先采样，转而采用**分数蒸馏采样**（Score Distillation Sampling, SDS）驱动的优化范式。该范式的核心优势在于：它不依赖反转和采样，而是直接从原始视频出发，通过优化变量逐步注入目标外观。具体而言，可以利用预训练 T2V 模型中的 **Delta Denoising Score**（DDS）梯度来引导优化过程。然而，直接使用 DDS 梯度（即 V-DDS 损失）进行视频编辑存在严重的副作用：**不准确的梯度会在迭代优化中累积结构误差，导致运动偏离原始轨迹**。如 Fig. 3 所示，仅使用 V-DDS 优化时，编辑后的视频虽然获得了目标外观，但物体的运动路径和空间结构逐渐偏离输入视频，产生不可接受的形变和闪烁。

**核心瓶颈的因果分析。** 上述问题的根源在于，V-DDS 损失仅关注外观注入，缺乏对视频结构和时序动态的显式约束。扩散模型的特征空间本身蕴含着丰富的结构信息，但传统的分数蒸馏方法并未有效利用这些信息来保持运动一致性。因此，如何在优化过程中**解耦外观注入与运动保持**，成为零样本视频编辑能否真正落地的关键。

**DreamMotion 的动机。** 针对这一瓶颈，DreamMotion 提出了一种全新的解决方案：利用预训练 T2V 扩散模型内部的**深度特征自相似性**作为结构保持的线索。核心直觉是：原始视频在扩散特征空间中具有特定的时空自相似性模式，这些模式编码了物体的空间结构和帧间运动关系。通过在优化过程中显式匹配原始视频与编辑视频的时空自相似性，可以有效约束结构并平滑时间动态，从而在注入新外观的同时精准保留原始运动。这一思路将视频编辑从“采样生成”范式转变为“约束优化”范式，为模型无关、无需训练的零样本视频编辑开辟了新路径。

## 核心方法与创新机理

DreamMotion 的核心贡献在于**将零样本视频编辑的范式从“祖先采样”迁移到“分数蒸馏优化”**，并为此设计了一套**时空自相似性正则化机制**，在注入新外观的同时精准保留原始视频的运动与结构。这一转变解决了传统方法难以在零样本条件下捕捉复杂真实世界运动的瓶颈（Fig. 2）。

具体而言，方法层面的关键创新体现在以下四个 changed slots 上：

### 1. 编辑范式：从祖先采样到分数蒸馏优化

传统零样本视频编辑方法（如 **Tune-A-Video** (Wu et al., ICCV 2023)、**TokenFlow** (Geyer et al., arXiv 2023)）依赖基于祖先采样的反向扩散过程，从噪声或 DDIM 反转潜变量逐步生成编辑结果。然而，这种范式在生成过程中难以保持原始视频的复杂运动轨迹，容易导致运动失真（Fig. 2）。

DreamMotion 则**直接以原始视频为初始化变量**，通过分数蒸馏采样（SDS）驱动的优化来编辑视频。具体地，它利用预训练文本到视频扩散模型中的 Delta Denoising Score（DDS）梯度，逐步将目标外观注入视频变量，从而绕开了祖先采样过程中的运动丢失问题。

### 2. 运动保持机制：时空自相似性匹配正则化

仅使用分数蒸馏优化（V-DDS）虽能注入目标外观，但会累积结构误差，导致运动偏移和闪烁伪影（Fig. 3, Fig. 9）。DreamMotion 的核心创新在于引入了**双层次的自相似性匹配正则化**：

- **空间自相似性匹配（S-SSM）**：通过计算并匹配原始视频与编辑视频在扩散关键帧特征上的空间自相似性图，约束每帧的全局结构不偏离原始视频。其损失函数为：

  $$ \mathcal{L}_{\mathrm{S-SSM}}(\pmb{x}_t^{1:N}, \hat{\pmb{x}}_t^{1:N}) = \frac{1}{N} \sum_{n=1}^{N} \left\| \mathbf{SS}^n(\pmb{x}_t^{1:N}) - \mathbf{SS}^n(\hat{\pmb{x}}_t^{1:N}) \right\|_2^2 $$

  其中 $\mathbf{SS}^n$ 为第 $n$ 帧的空间自相似性矩阵，基于扩散关键帧特征的余弦相似度构建。

- **时间自相似性匹配（T-SSM）**：利用空间平均轮廓作为全局描述子，计算时间轴上的自相似性矩阵，并对齐目标视频与原始视频的时间自相似性，从而消除帧间闪烁和不一致。该机制有效实现了时间平滑，与 S-SSM 形成互补。

消融实验（Table 3, Fig. 9）表明，联合优化 V-DDS、S-SSM 和 T-SSM 在所有自动指标上取得最佳性能；移除任一自相似性损失都会导致运动一致性和结构保持能力的显著下降。

### 3. 梯度处理：掩码过滤机制

直接使用原始 SDS/DDS 梯度进行优化容易产生模糊和过饱和现象。DreamMotion 利用现成检测模型生成的检测框构建**二元掩码**，在 V-DDS 更新过程中选择性过滤梯度，仅编辑目标区域（Fig. 6）。消融实验（Table 3）证实，移除掩码条件会严重损害视觉保真度。

### 4. 模型适用范围：模型无关设计

与多数基线方法针对单一模型框架定制不同，DreamMotion 的优化策略具有**模型无关性**。它可同时应用于非级联视频扩散模型（如 Zeroscope）和级联框架（如 Show-1）。对于级联模型，优化仅局限在关键帧生成阶段，后续的时间插值和空间超分辨率模块正常执行，从而无缝适配不同架构（Table 1, Table 2）。

![[assets/figures/papers/paper_list_l36_DreamMotion_Space_Time_Self_Similar_Score_Distillation_for_Zero_Shot_Vid/figures/001_Figure_1.jpg]]
*Figure 1: Zero-shot video editing results. The second row presents videos produced with our method with a non-cascaded video diffusion model, while those in the bottom row are from a cascaded model. For a full display of results, visit our project page*

DreamMotion 是一种基于分数蒸馏优化的零样本视频编辑框架，其核心思想是**绕过传统的祖先采样过程，直接在原始视频变量上进行优化**。框架的输入为一组原始视频帧及其对应的源文本描述，输出为注入目标外观但保留原始运动与结构的新视频。

### 优化流程概览

整个优化过程围绕三个并行的目标函数展开，共享相同的噪声和时间步：

1. **外观注入**：通过视频 Delta Denoising Score（V-DDS）损失，利用预训练文本到视频扩散模型的分数梯度，将目标文本描述的外观逐步注入视频变量。
2. **空间结构保持**：通过空间自相似性匹配（S-SSM）损失，对齐编辑视频与原始视频在扩散关键帧特征上的空间自相似性图，约束每帧的全局结构不发生偏移。
3. **时间平滑**：通过时间自相似性匹配（T-SSM）损失，对齐编辑视频与原始视频沿时间轴的自相似性矩阵，消除帧间闪烁和不一致伪影。

最终优化目标为三者的联合：

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\mathrm{V-DDS}} + \mathcal{L}_{\mathrm{S-SSM}} + \mathcal{L}_{\mathrm{T-SSM}}$$

### 关键模块交互关系

- **视频初始化**：将待编辑视频变量 $\mathbf{x}_0^{1:N}(\theta)$ 直接初始化为原始视频 $\hat{\mathbf{x}}^{1:N}$，而非从随机噪声开始。这确保了优化的起点与原始视频在结构上完全一致。
- **V-DDS 外观注入**：在每一步优化中，对原始视频和编辑视频分别添加相同的噪声，送入预训练 T2V 模型获取噪声预测。V-DDS 损失计算两者预测噪声的差值，其梯度驱动编辑视频向目标外观靠拢。同时，利用现成检测模型生成的二元掩码过滤梯度，仅更新目标区域，避免背景模糊和过饱和。
- **S-SSM 结构约束**：从扩散模型的注意力关键帧特征中提取逐帧的空间自相似性图，计算编辑视频与原始视频之间的均方误差。该损失强制编辑视频保持与原始视频相同的空间结构关系。
- **T-SSM 时间正则化**：对关键帧特征沿空间维度求平均得到一阶全局描述子，再沿时间轴计算自相似性矩阵。通过匹配编辑视频与原始视频的时间自相似性矩阵，实现跨帧的时间平滑。

### 级联模型适配

对于级联视频扩散框架（如 Show-1），DreamMotion 将优化局限在**关键帧生成阶段**。后续的时间插值和空间超分辨率模块正常执行，无需额外修改。这种设计使得方法天然具备模型无关性，可同时应用于非级联（如 Zeroscope）和级联模型。

### 输入输出流

- **输入**：原始视频帧序列、源文本描述 $\hat{y}$、目标文本描述 $y$。
- **处理**：在原始视频变量上迭代优化，每一步同时计算 V-DDS、S-SSM、T-SSM 三个损失的梯度，更新视频变量。
- **输出**：编辑后的视频帧序列，其外观符合目标描述，同时精确保留了原始视频的运动轨迹和空间结构。

DreamMotion 的核心优化框架由三个损失项联合驱动，分别负责外观注入、空间结构保持和时间平滑。所有损失共享相同的噪声 $\epsilon$ 和时间步 $t$，在统一的分数蒸馏框架下协同工作。

### 外观注入模块：视频 Delta 去噪分数损失 (V-DDS)

该模块将 Delta Denoising Score (DDS) 机制从图像域扩展至视频域。其核心思想是利用预训练文本到视频扩散模型的分数蒸馏能力，通过计算目标分支与参考分支之间的分数差异来注入新外观。

给定原始视频 $\hat{\pmb{x}}^{1:N}$ 和待优化的目标视频变量 $\pmb{x}_0^{1:N}(\theta)$，V-DDS 损失定义为：

$$\mathcal{L}_{\mathrm{V-DDS}}(\theta; y) = \left\| \epsilon_{\phi}^{w}(\pmb{x}_t^{1:N}(\theta), t, y) - \epsilon_{\phi}^{w}(\hat{\pmb{x}}_t^{1:N}, t, \hat{y}) \right\|_2^2$$

其中：
- $\pmb{x}_t^{1:N}(\theta)$ 和 $\hat{\pmb{x}}_t^{1:N}$ 分别是目标视频和原始视频经前向扩散加噪至时间步 $t$ 的潜变量
- $\epsilon_{\phi}^{w}(\cdot)$ 表示预训练 T2V 扩散模型在分类器自由引导下的噪声预测函数
- $y$ 为目标文本描述，$\hat{y}$ 为原始视频的描述
- 梯度仅作用于优化变量 $\theta$

为防止优化过程中的模糊和过饱和，该模块引入基于检测框的二元掩码对梯度进行选择性过滤。使用现成的检测模型生成目标区域的边界框，将其转换为二元掩码后，仅允许目标区域的梯度参与参数更新。这一机制在保持非编辑区域视觉保真度方面起到了关键作用。

### 空间结构保持模块：空间自相似性匹配 (S-SSM)

V-DDS 单独使用时，不准确的梯度会累积结构误差，导致运动偏移。S-SSM 通过匹配扩散模型内部深层特征的空间自相似性来约束结构。

对于第 $n$ 帧，在扩散模型的关键帧特征 $K^n(\pmb{x}_t^{1:N})$ 上，空间位置 $i$ 和 $j$ 之间的自相似性定义为余弦相似度：

$$SS_{i,j}^{n}(\pmb{x}_t^{1:N}) = \cos\left(K_i^n(\pmb{x}_t^{1:N}), K_j^n(\pmb{x}_t^{1:N})\right)$$

该自相似性图刻画了帧内任意两点之间的特征关系，对局部纹理变化不敏感但能有效捕获全局结构布局。S-SSM 损失通过逐帧最小化目标视频与原始视频自相似性图之间的均方误差来实现结构对齐：

$$\mathcal{L}_{\mathrm{S-SSM}}(\pmb{x}_t^{1:N}, \hat{\pmb{x}}_t^{1:N}) = \frac{1}{N} \sum_{n=1}^{N} \left\| \mathbf{SS}^n(\pmb{x}_t^{1:N}) - \mathbf{SS}^n(\hat{\pmb{x}}_t^{1:N}) \right\|_2^2$$

该损失强制目标视频在深层语义结构上与原始视频保持一致，从而在注入新外观的同时保留物体的空间布局和姿态。

### 时间平滑模块：时间自相似性匹配 (T-SSM)

S-SSM 仅作用于单帧内部，无法显式建模帧间的时间一致性，编辑后视频可能出现闪烁伪影。T-SSM 通过建模时间轴上的自相似性来解决这一问题。

首先，对每帧的关键帧特征沿空间维度求平均，得到一个一阶全局描述子——空间边缘均值：

$$M[K(\pmb{x}_t^{1:N})] = \frac{1}{H \cdot W} \sum_{i=1}^{H \cdot W} K_i(\pmb{x}_t^{1:N})$$

随后，基于该全局描述子计算任意两帧之间的时间自相似性，形成时间自相似性矩阵 $\mathbf{TS}(\pmb{x}_t^{1:N})$。T-SSM 损失定义为目标视频与原始视频时间自相似性矩阵之间的均方误差：

$$\mathcal{L}_{\mathrm{T-SSM}}(\pmb{x}_t^{1:N}, \hat{\pmb{x}}_t^{1:N}) = \left\| \mathbf{TS}(\pmb{x}_t^{1:N}) - \mathbf{TS}(\hat{\pmb{x}}_t^{1:N}) \right\|_2^2$$

该损失强制编辑后视频的帧间动态模式与原始视频保持一致，有效消除了闪烁和不连贯的运动伪影。

### 联合优化目标

完整的优化目标为三个损失项的加权组合：

$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\mathrm{V-DDS}} + \mathcal{L}_{\mathrm{S-SSM}} + \mathcal{L}_{\mathrm{T-SSM}}$$

优化从原始视频初始化目标变量 $\pmb{x}_0^{1:N}(\theta) \leftarrow \hat{\pmb{x}}^{1:N}$ 开始，通过梯度下降迭代更新。对于级联视频扩散框架，优化仅作用于关键帧生成阶段，后续的时间插值和空间超分辨率模块正常执行，从而保证了方法的模型无关性。

## 实验与关键发现

### 主实验结果

DreamMotion 在非级联和级联两种视频扩散框架下均取得了最优性能，验证了其模型无关的设计优势。

在非级联设定中，DreamMotion 以 Zeroscope 为骨干网络，与 **Tune-A-Video** (Wu et al., ICCV 2023)、**ControlVideo** (Zhang et al., arXiv 2023)、**Control-A-Video** (Chen et al., arXiv 2023)、**TokenFlow** (Geyer et al., arXiv 2023) 和 **Gen-1** (Esser et al., ICCV 2023) 等基线方法进行了全面比较。如 Table 1 所示，DreamMotion 在所有七项指标上均优于对比方法：文本-视频对齐得分（Text-Align）达到 0.8209，帧间一致性（Frame-Con）达到 0.9726，运动保真度（Motion-Fidelity）达到 0.9259。人类评估进一步印证了这一优势——编辑准确性（Edit Accuracy）得分 4.14，结构与运动保持（Structure & Motion Preservation）得分 4.33，均显著领先。

![[assets/figures/papers/paper_list_l36_DreamMotion_Space_Time_Self_Similar_Score_Distillation_for_Zero_Shot_Vid/figures/008_Table_1.jpg]]
*Table 1: Quantitative evaluations. DreamMotion with Zeroscope outperforms various video editing methods in all seven features*

在级联设定中，DreamMotion 以 Show-1 为骨干网络，Table 2 显示其在五项指标上超越了其他级联基线方法，Text-Align 达 0.7747，Frame-Con 达 0.9755，编辑准确性 3.97，结构与运动保持 4.30。需要指出的是，所有级联基线方法均使用相同的 Show-1 视频模型实现，确保了公平比较。

![[assets/figures/papers/paper_list_l36_DreamMotion_Space_Time_Self_Similar_Score_Distillation_for_Zero_Shot_Vid/figures/010_Table_2.jpg]]
*Table 2: Quantitative evaluations. DreamMotion utilizing Show-1 surpasses other cascaded baselines across the five features. Other baselines were also implemented using the same video model, ensuring a fair comparison*

与运动保持相关的专项对比中，DreamMotion 在 Motion-Fidelity 指标上以 0.9259 显著优于 **DMT** (Yatim et al., arXiv 2023) 的 0.8697 和 **Video-P2P** (Liu et al., arXiv 2023) 的 0.7384（Table 4），分别提升 0.0562 和 0.1875，充分证明了时空自相似性正则化在复杂运动保持上的核心作用。

![[assets/figures/papers/paper_list_l36_DreamMotion_Space_Time_Self_Similar_Score_Distillation_for_Zero_Shot_Vid/figures/016_Table_4.jpg]]
*Table 4: Additional quantitative comparison with DMT and Video-P2P*

### 消融实验

为验证各组件的独立贡献，Table 3 报告了系统的定量消融结果。

**联合优化的必要性。** 仅使用 $\mathcal{L}_{\mathrm{V-DDS}}$ 而不施加任何自相似性正则化时，编辑视频会出现严重的结构误差和帧间闪烁伪影（Fig. 9）。定量上，单独移除空间自相似性损失（$\mathcal{L}_{\mathrm{S-SSM}}$）或时间自相似性损失（$\mathcal{L}_{\mathrm{T-SSM}}$）均导致运动一致性和结构保持能力的显著下降。完整的联合优化 $\mathcal{L}_{\mathrm{V-DDS}} + \mathcal{L}_{\mathrm{S-SSM}} + \mathcal{L}_{\mathrm{T-SSM}}$ 在所有自动指标上取得最佳表现，这直接支撑了核心洞察：外观注入与运动保持可通过分数蒸馏优化和自相似性正则化实现有效解耦。

**掩码梯度过滤的作用。** 移除二元掩码条件后，编辑视频出现明显的模糊和过饱和现象，严重损害视觉保真度（Table 3 及 Fig. 13）。这表明利用检测框生成的掩码来过滤 V-DDS 梯度，是维持非编辑区域结构完整性的关键机制——它防止了分数蒸馏过程中外观信号向背景区域的不当扩散。

### 失败模式与局限性

DreamMotion 的核心约束在于其结构保持机制本质上依赖于原始视频的空间布局。当编辑任务需要显著的几何或结构变化时——例如大幅变形、新增物体或改变物体类别——方法的表现受限（Fig. 10）。这是因为空间自相似性匹配（S-SSM）明确对齐了目标视频与原始视频的扩散特征自相似性图，从而将编辑结果锚定在原始视频的结构支配之下。这一局限性揭示了当前框架的根本边界：它擅长外观迁移与风格化编辑，但无法脱离原始视频的语义结构进行创造性生成。

### 需要人工核实的内容

以下结论基于分析材料推断，建议人工核对原文具体数值：
- Table 3 中完整模型与各消融变体在 CLIP-T、CLIP-F、Tem-Con、Warp-Err 四项指标上的具体差值。
- Table 1 和 Table 2 中人类评估部分各维度的完整评分分布及统计显著性检验结果。
- Fig. 13 所示移除掩码条件后的具体视觉退化模式。

![[assets/figures/papers/paper_list_l36_DreamMotion_Space_Time_Self_Similar_Score_Distillation_for_Zero_Shot_Vid/figures/003_Figure_3.jpg]]
*Figure 3: Appearance Injection with Space-TimeSelf-Similarity Man→spider-man Fig. 3: Optimization progress visualization. The proposed self-similarity regularization effectively preserves the structure and motion of the original video*

![[assets/figures/papers/paper_list_l36_DreamMotion_Space_Time_Self_Similar_Score_Distillation_for_Zero_Shot_Vid/figures/018_Figure_14.jpg]]
*Figure 14: “Amanisdoingakickflip.”→“Anastronautisdoingakickflip." Fig. 14: Visualization of optimization progress*

## 定位与知识库关联

DreamMotion 的核心突破在于用**分数蒸馏优化**替代了零样本视频编辑中主流的**祖先采样**范式，并引入**时空自相似性匹配**作为结构保持的正则化手段。本节从范式迁移、基线对比、适用边界与开放问题四个维度定位该方法在领域知识库中的位置。

### 范式迁移：从祖先采样到分数蒸馏优化

传统零样本视频编辑方法（如 Tune-A-Video、ControlVideo、TokenFlow 等）普遍依赖扩散模型的反向去噪过程：将输入视频通过 DDIM 反演映射到噪声空间，再在祖先采样过程中注入目标文本条件。这一范式存在根本性瓶颈——反演-采样循环难以精确重建复杂真实运动，导致生成视频的运动模式与原始视频出现显著偏移（Fig. 2）。

DreamMotion 彻底绕开了这一范式。它直接将原始视频作为优化变量初始化，在像素空间上执行基于分数的迭代优化，利用预训练文本到视频扩散模型内部的 Delta Denoising Score（DDS）梯度逐步注入目标外观。这一策略的关键因果机制在于：**优化过程从原始视频出发，而非从噪声出发**，因此天然保留了视频的底层运动结构，只需额外正则化来防止优化过程中的结构漂移。

### 与基线方法的关系与差异化

下表梳理 DreamMotion 与代表性基线方法在核心设计维度上的差异：

| 方法 | 编辑范式 | 运动保持机制 | 梯度处理 | 模型适用范围 |
|------|---------|-------------|---------|-------------|
| **Tune-A-Video** (Wu et al., ICCV 2023) | 祖先采样（膨胀2D扩散模型） | 隐式依赖膨胀注意力 | 标准去噪 | 单模型定制 |
| **ControlVideo** (Zhang et al., arXiv 2023) | 祖先采样 + ControlNet | 显式结构控制（深度/边缘图） | 标准去噪 | 需ControlNet适配 |
| **TokenFlow** (Geyer et al., arXiv 2023) | 祖先采样 + 特征传播 | 扩散特征一致性约束 | 标准去噪 | 依赖特征提取 |
| **Gen-1** (Esser et al., ICCV 2023) | 祖先采样 + 结构条件 | 深度/边缘图引导 | 标准去噪 | 需结构估计模块 |
| **Video-P2P** (Liu et al., arXiv 2023) | 祖先采样 + 交叉注意力控制 | 注意力图注入 | 标准去噪 | 仅局部编辑 |
| **DMT** (Yatim et al., arXiv 2023) | 祖先采样 + 特征匹配 | 时空扩散特征迁移 | 标准去噪 | 依赖特征对齐 |
| **DreamMotion** (本文) | **分数蒸馏优化** | **时空自相似性匹配** | **掩码过滤梯度** | **模型无关** |

关键差异化体现在三个层面：

1. **编辑范式**：DreamMotion 是首个将分数蒸馏采样（SDS/DDS）引入零样本视频编辑的工作。与祖先采样方法需要反演-采样闭环不同，DreamMotion 的优化过程是单向的——从原始视频出发，沿 DDS 梯度方向逐步更新，无需反演步骤。这消除了反演误差对运动保真度的级联影响。

2. **运动保持机制**：现有方法要么依赖模型自身的隐式时间一致性（如 Tune-A-Video 的膨胀注意力），要么引入外部结构条件（如 ControlVideo 的深度图）。DreamMotion 的时空自相似性匹配则利用了预训练扩散模型**内部**的深度特征——空间自相似性对齐（S-SSM）通过匹配关键帧特征的自相似性图来保持逐帧结构，时间自相似性对齐（T-SSM）通过匹配帧间特征的时序相关性来消除闪烁。这种“自监督”结构约束无需额外模型训练或外部条件提取，且与外观注入过程解耦。

3. **模型无关性**：DreamMotion 可同时应用于非级联框架（Zeroscope）和级联框架（Show-1），仅需将优化局限在级联框架的关键帧生成阶段。这种灵活性源于其优化范式不依赖特定模型架构的去噪过程。

### 适用边界与局限性

DreamMotion 的设计决定了其**适用边界**：它擅长在保持原始视频运动和结构的前提下注入新的外观风格或纹理，但在需要**显著几何或结构变化**的编辑任务上表现受限。Fig. 10 明确展示了这一局限——当目标编辑涉及大幅变形或新增物体时，方法无法脱离原始视频结构的支配。

这一局限的深层原因在于：空间自相似性损失 $\mathcal{L}_{\mathrm{S-SSM}}$ 显式约束编辑视频与原始视频的特征自相似性图保持一致，这等价于要求二者的全局空间结构高度相关。当编辑目标需要根本性地改变物体形状或场景布局时，该约束会与外观注入损失 $\mathcal{L}_{\mathrm{V-DDS}}$ 产生冲突，导致优化陷入局部最优。

此外，消融实验（Table 3）揭示了各模块的失效模式：
- 移除掩码条件会导致严重的模糊和过饱和（Fig. 13），说明无约束的 DDS 梯度会污染非目标区域；
- 仅使用 $\mathcal{L}_{\mathrm{V-DDS}}$ 而不加任何自相似性正则化，会累积结构误差并引发运动偏移（Fig. 9）；
- 移除时间自相似性损失会导致帧间闪烁伪影，表明 T-SSM 是时间平滑的必要条件。

### 开放问题

1. **结构变化编辑的扩展**：如何将框架扩展到需要显著结构变化的编辑任务？可能的路径包括引入可学习的形变场、将自相似性约束从“严格对齐”松弛为“结构感知”的软约束，或结合 3D 先验（如 NeRF）来引导几何变换。

2. **失败模式的细粒度分析**：当省略空间自相似性损失时，具体的失败模式是否存在对特定视频类型的敏感性？例如，快速移动或遮挡严重的视频是否更容易出现结构崩溃？这需要更系统的诊断实验来揭示。

3. **与其他视频先验的融合**：分数蒸馏优化能否与光流信息、深度估计或轨迹约束等显式运动先验结合？这种融合可能进一步降低对掩码的依赖，并在复杂运动场景下提升时间一致性。

4. **计算效率与收敛性**：DreamMotion 需要多步优化迭代，其收敛速度与视频长度、编辑复杂度的关系尚未被系统研究。探索更高效的优化策略（如自适应步长、预热阶段设计）是实用化部署的关键方向。

## 原文 PDF

![[paperPDFs/ECCV_2024/DreamMotion_Space_Time_Self_Similar_Score_Distillation_for_Zero_Shot_Video_Editing.pdf]]
