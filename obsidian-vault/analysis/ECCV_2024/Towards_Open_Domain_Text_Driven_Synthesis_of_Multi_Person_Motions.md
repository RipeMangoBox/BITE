---
title: Towards Open Domain Text Driven Synthesis of Multi Person Motions
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Towards_Open_Domain_Text_Driven_Synthesis_of_Multi_Person_Motions.pdf
aliases:
- TSDFIPML
- TODTDSMPM
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过从大规模图像和视频数据集中估计姿态和运动构建数据集，并设计交错pose和motion层的两阶段扩散模型，实现从文本生成任意人数的运动。
primary_logic: 从单帧多姿态和多帧单姿态数据联合训练，利用交错层分别建模帧内交互和时序运动，并结合两阶段生成与冻结pose层的策略，使模型能够从开放域文本生成高质量的多人运动。
claims:
- 方法采用两阶段管道：首先生成多人姿态帧，然后以该帧为条件生成运动序列。
- 交错pose和motion层通过重塑维度分别学习每帧交互和每个主体的时序。
- 在2人生成上，P-R-Precision Top-1达到0.323，远超InterGen的0.073。
- Two-person motion generation with open-domain prompts 上 P-R-Precision Top-1 = 0.323
---

# Towards Open Domain Text Driven Synthesis of Multi Person Motions

> [!tip] 核心洞察
> 从单帧多姿态和多帧单姿态数据联合训练，利用交错层分别建模帧内交互和时序运动，并结合两阶段生成与冻结pose层的策略，使模型能够从开放域文本生成高质量的多人运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向开放域文本驱动的多人运动合成 |
| 英文题名 | Towards Open Domain Text Driven Synthesis of Multi Person Motions |
| 会议/期刊 | ECCV 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Two-stage diffusion framework with interleaved pose and motion layers |
| Dataset | Two-person motion generation with open-domain prompts, Multi-person motion generation |

> [!tip] 效果简介
> - Two-person motion generation with open-domain prompts 上，P-R-Precision Top-1 0.323 vs InterGen 0.073 (+0.250)。
> - Multi-person motion generation (vs. naive baselines) 上，P-FID / M-FID P-FID 0.229, M-FID 0.684 vs Pose-Only (P-FID 0.077, M-FID 0.903) / Motion-Only (P-FID 0.317, M-FID 0.613) (vs. Pose-Only: P-FID +0.152 (worse), M-FID -0.219 (better); vs. Motion-Only: P-...)。

## 概述

### 问题背景

文本驱动的运动生成已在单人或双人场景取得显著进展，但现有方法受限于两个关键瓶颈：**缺乏大规模多人运动数据集**，以及模型架构和提示分布仅针对单人或双人交互设计。这导致现有模型无法处理开放域文本描述下的任意人数运动生成。本文直面这一空白，目标是从开放域文本描述中合成任意人数的多人运动序列。

### 核心方法

该方法的核心洞察是：**从单帧多姿态和多帧单姿态数据中联合学习**，利用交错设计的姿态层和运动层分别建模帧内多人交互与逐主体时序运动。具体而言，方法采用**两阶段扩散管道**：第一阶段从文本生成单帧多人姿态，第二阶段以该姿态帧为条件生成完整运动序列。训练时，第一阶段先训练文本到姿态模型，第二阶段插入运动层并冻结姿态层进行联合训练。此外，通过从大规模图像数据集（LAION-400M）和视频数据集（WebVid-10M）中估计姿态与运动，构建了LAION-Pose（800万元组）和WebVid-Motion（3500元组）两个数据集，突破了数据瓶颈。

### 主要结果

在两人运动生成任务上，该方法在开放域提示下达到P-R-Precision Top-1 **0.323**，远超基线InterGen（Liang et al., arXiv 2023）的0.073（+0.250）。在多人运动生成上，与朴素基线相比，该方法在P-FID和M-FID之间取得了更好的平衡（P-FID 0.229, M-FID 0.684）。消融实验验证了两阶段训练、冻结姿态层以及WebVid-Motion数据对性能的关键作用。

## 背景与动机

### 开放域文本到多人运动合成的核心瓶颈

文本驱动的三维人体运动生成是计算机视觉与图形学中的基础任务，其目标是根据自然语言描述生成逼真的人体运动序列。近年来，基于扩散模型的方法在**单人运动生成**上取得了显著进展，例如 MDM（Tevet et al., ICCV 2023）利用 Transformer 编码器在动作捕捉数据上实现了高质量的文本到运动合成。然而，当问题扩展到**多人场景**时，领域面临一个根本性瓶颈：**缺乏大规模多人运动数据集**。

现有数据集（如 HumanML3D、KIT-ML）仅包含单人运动，而双人交互数据集（如 InterHuman）规模有限且场景受限。这导致两个连锁问题：
1. **人数受限**：现有模型（如 InterGen、RIG、ComMDM）最多只能处理两人场景，且训练于受控的交互工作室环境。
2. **提示分布受限**：模型无法泛化到开放域文本描述，例如“三个人在公园里散步聊天”这类任意人数、任意场景的日常活动。

这一瓶颈的本质在于：多人运动的标注成本极高，传统动作捕捉（MoCap）难以规模化采集多人自由交互数据。因此，**如何在不依赖昂贵多人运动标注的前提下，使模型获得开放域多人运动生成能力**，成为该方向的关键挑战。

### 现有方法的缺口

当前多人运动生成方法可归为两类，均存在明显局限：

| 方法类别 | 代表工作 | 核心局限 |
|---------|---------|---------|
| 双人交互生成 | InterGen（Liang et al., arXiv 2023）、RIG（Tanaka et al., ICCV 2023）、ComMDM（Shafir et al., arXiv 2023） | 仅支持 2 人，训练域受限，无法处理开放域文本 |
| 单人运动生成扩展 | MDM 等直接拼接多人序列 | 缺乏帧内多人交互建模，生成结果不协调 |

这些方法的共同缺口在于：**架构设计未解耦“帧内多人交互”与“时序运动建模”**，导致模型无法从异构数据源（图像姿态 + 视频运动 + 动作捕捉）中联合学习。具体而言：
- 单一 Transformer 编码器将所有帧和所有主体平铺为序列，难以分别捕捉每帧内的空间交互和每个主体的时序一致性。
- 单阶段端到端训练无法利用大规模图像姿态数据预训练高质量姿态先验，导致开放域泛化能力不足。

### 本文动机与核心思路

针对上述瓶颈，本文提出了一种**从大规模图像和视频数据中挖掘多人运动监督信号**的方案，绕过了对昂贵多人运动标注的依赖。核心动机在于：互联网规模的图像（如 LAION-400M）和视频（如 WebVid-10M）中蕴含丰富的多人姿态和运动信息，可以通过现成的姿态估计和运动重建工具提取。

基于这一动机，本文的方法论围绕两个关键设计展开：

1. **多源数据联合训练**：构建 LAION-Pose（800 万图像-姿态-文本三元组）和 WebVid-Motion（3500 视频-运动-文本三元组）数据集，与现有动作捕捉数据联合训练，使模型接触开放域多人场景。

2. **交错式两阶段扩散架构**：设计交替排列的 **pose 层**（逐帧建模多人空间交互）和 **motion 层**（逐主体建模时序运动），通过维度重塑机制使各层专注于其设计目标。训练采用两阶段策略——先训练文本到姿态模型，再冻结姿态层训练运动层——确保姿态先验不被运动数据干扰。

这一设计使得模型能够**从开放域文本生成任意人数（最多 10 人）的运动序列**，在双人生成上将 P-R-Precision Top-1 从 InterGen 的 0.073 提升至 0.323，首次实现了开放域多人运动生成的实用化突破。

## 核心创新

本文的核心创新在于突破了现有多人运动生成模型在**人数规模**和**文本域开放程度**上的双重限制，构建了一个能够从开放域文本描述中生成任意人数运动序列的框架。其关键创新点可归纳为以下四个维度：

### 1. 支持任意人数的开放域生成

此前的方法（如 **InterGen** (Liang et al., arXiv 2023)、**RIG** (Tanaka et al., ICCV 2023)、**ComMDM** (Shafir et al., arXiv 2023)）仅限于生成 1 人或 2 人的运动，且训练数据来自受限的动作捕捉工作室场景。本文首次将生成能力扩展到**任意人数（最多 10 人）**，并支持开放域文本提示。这一突破的因果杠杆在于**数据层面的根本性扩展**：通过从大规模图像数据集 LAION-400M 和视频数据集 WebVid-10M 中估计多人姿态与运动，构建了 LAION-Pose（800 万图像-姿态-文本三元组）和 WebVid-Motion（3500 视频-运动-文本三元组）两个新型数据集，使模型得以接触丰富多样的多人场景描述。

### 2. 交错 Pose 层与 Motion 层的解耦架构

传统方法（如基于 MDM 的单 Transformer 编码器）将帧内交互与时序运动混合建模，难以同时保证单帧姿态的合理性和跨帧运动的连贯性。本文提出的核心架构创新是**交错排列的 Pose 层与 Motion 层**：

- **Pose 层**：逐帧处理，将时间维度重塑为批次维度，专注于学习单帧内多人之间的姿态与位置关系（帧内交互）。
- **Motion 层**：逐主体处理，将主体维度重塑为批次维度，专注于学习每个人的时序运动（跨帧连贯性）。

这种解耦设计使得帧内空间关系与时序动态可以被分别建模，避免了单一编码器中的表征冲突。

### 3. 两阶段训练与冻结策略

训练策略的创新同样关键。本文采用**两阶段训练**：

- **第一阶段**：训练一个文本到姿态（Text-to-Pose）模型，仅使用 Pose 层，从文本生成单帧多人姿态。
- **第二阶段**：在每个 Pose 层后插入 Motion 层，**冻结预训练的 Pose 层**，仅训练 Motion 层，以第一阶段生成的姿态帧作为中间帧条件来生成完整运动序列。

消融实验（Sec. 5.6）证实了这一策略的有效性：单阶段联合训练（不预训练 Pose 模型）效果显著下降，因为高质量的姿态模型为每帧提供了强条件信号；若在联合训练阶段解冻 Pose 层，运动数据反而会干扰已学到的姿态表征，导致性能退化。

### 4. 多源数据联合训练与引导采样

模型在训练时联合使用动作捕捉数据、LAION-Pose 图像姿态数据和 WebVid-Motion 视频运动数据，实现了**跨数据源的知识融合**。在采样阶段，进一步引入独立的文本到姿态和文本到单人运动模型作为引导项，通过组合引导公式提升生成质量：

$$G_{s_p, s_m}(x_t, t, c) = (1 - s_p - s_m) \cdot G(x_t, t, c) + s_p \cdot G_p(x_t, t, c) + s_m \cdot G_m(x_t, c)$$

其中 $s_p + s_m \leq 1$，通过调节引导权重平衡多人模型与独立引导模型的贡献。

**总结**：本文的创新本质在于通过**数据扩展 + 架构解耦 + 分阶段训练**的组合策略，将多人运动生成从封闭的二人交互域推向开放域任意人数场景，其核心机制是让模型分别学会“单帧内的多人空间关系”和“单人的时序运动”，再通过冻结策略保护已学到的姿态表征不被运动训练所破坏。

## 整体框架

该方法采用**两阶段扩散管道**，将开放域文本到多人运动生成分解为两个可控子问题。整体流程如下：

**第一阶段：文本到多人姿态生成。** 模型接收一段开放域文本描述，生成单帧包含多人姿态的样本。该帧作为第二阶段的条件信号，为后续运动生成提供空间布局和人物交互的锚点。

**第二阶段：文本与姿态条件到多人运动生成。** 以上一阶段生成的姿态帧作为中间帧条件，结合文本描述，模型生成完整的运动序列。此阶段确保生成的运动序列以该姿态帧为中间帧，保证时序一致性和与文本的语义对齐。

### 核心架构：交错姿态层与运动层

两阶段共享相同的 Transformer 架构设计，核心创新在于**交错排列的姿态层（Pose Layers）与运动层（Motion Layers）**。该设计基于 MDM 框架扩展而来，通过维度重塑机制实现帧内交互与时序运动的解耦建模：

- **姿态层**逐帧处理，学习单帧内多人之间的姿态与空间位置关系。在进入姿态层前，将时间维度重塑到批次维度，使 Transformer 编码器专注于每帧内的主体交互。
- **运动层**逐主体处理，学习每个个体的合理时序运动。在进入运动层前，将主体维度重塑到批次维度，使模型专注于单人的运动轨迹。

每个层实现为 Transformer 编码器。扩散时间步、文本嵌入（CLIP）以及参考姿态条件被编码并求和，形成一个条件令牌（condition token），拼接到序列开头，贯穿所有层。

### 输入输出流

1. **文本编码**：使用 CLIP 文本编码器将输入描述映射为嵌入向量。
2. **输入投影**：多人姿态参数（包含全局位置和 SMPL 姿态参数）通过线性层投影到高维空间（维度 512）。
3. **条件注入**：扩散时间步与文本嵌入分别投影后求和，生成条件令牌。
4. **交错处理**：投影后的序列与条件令牌拼接，依次通过多对姿态层和运动层。第一阶段模型含 8 个姿态层；第二阶段模型含 8 对姿态层与运动层。
5. **输出投影**：最终表示通过线性层投影回原始姿态维度，得到去噪后的多人运动参数。

### 两阶段训练策略

训练采用分阶段策略以保证各模块学习质量：

1. **第一阶段**：仅使用姿态层训练文本到姿态模型，在 LAION-Pose 等多源数据上学习文本与多人姿态的映射关系。
2. **第二阶段**：初始化多人运动模型，在每个姿态层后插入运动层，并**冻结所有姿态层参数**。在联合数据（含 WebVid-Motion 等运动数据）上训练运动层，使模型学习时序运动生成能力。

这种冻结策略避免了运动数据对第一阶段已学到的姿态表示的干扰，同时让运动层专注于时序建模。

### 采样时的引导机制

在推理阶段，除标准的无分类器引导外，该方法额外引入**独立的文本到姿态模型**和**文本到单人运动模型**作为引导项。最终预测由多人模型、姿态引导模型和运动引导模型三者的输出加权组合而成：

$$G_{s_p, s_m}(x_t, t, c) = (1 - s_p - s_m) \cdot G(x_t, t, c) + s_p \cdot G_p(x_t, t, c) + s_m \cdot G_m(x_t, c)$$

其中 $s_p$ 和 $s_m$ 分别为姿态和运动引导尺度，满足 $s_p + s_m \leq 1$。该机制进一步提升了生成结果的空间合理性和运动自然度。

### 补充图表

![[assets/figures/papers/paper_list_l1766_Towards_Open_Domain_Text_Driven_Synthesis_of_Multi_Person_Motions/figures/003_Figure_3.jpg]]
*Figure 3: Our model is a diffusion framework consisting of interleaving pose and motion layers. At each pose/motion layer, we reshape the temporal/subject dimension into the batch dimension so that the layer focuses on generating per frame subject interaction and per-subject temporal movements respectively. Each layer is implemented as a transformer encoder. Diffusion time steps and text or pose conditions are encoded and summed up as a condition token concatenated to the beginning of the sequence*

## 核心模块与公式推导

### 整体架构概述

该方法构建于 **MDM** 框架之上，采用基于 Transformer 编码器的扩散模型，并通过引入交错的姿态层（Pose Layers）与运动层（Motion Layers）将其扩展至多人场景。整体架构如图 3 所示，核心思路是将多人运动序列 $x^{1:N,1:F}$（$N$ 个主体，$F$ 帧）在不同维度上进行分解建模。

### 关键模块

**1. 输入线性投影（Input Linear Projection）**

将原始姿态参数通过线性层投影到高维空间（$C' = 512$），为后续 Transformer 层提供统一的表示维度。

**2. 条件嵌入（Condition Embeddings）**

扩散时间步 $t$ 与文本的 CLIP 嵌入分别经投影后求和，得到条件令牌（condition token），拼接在序列起始位置，贯穿所有 Transformer 层。

**3. 姿态层（Pose Layers）**

姿态层逐帧应用，在每帧内部学习多个主体之间的姿态与空间位置关系。进入姿态层前，将时序维度重塑（reshape）到批次维度，使 Transformer 编码器关注单帧内的多人交互。

**4. 运动层（Motion Layers）**

运动层逐主体应用，学习每个主体的时序运动模式。进入运动层前，将主体维度重塑到批次维度，使 Transformer 编码器关注单个主体在时间轴上的运动连贯性。

姿态层与运动层交替堆叠：第一阶段文本到姿态模型包含 8 个姿态层；第二阶段多人运动模型包含 8 对姿态层与运动层。

**5. 输出线性投影（Output Linear Projection）**

将高维表示通过线性层投影回原始姿态维度 $C$。

**6. 两阶段训练策略**

- **第一阶段**：训练文本到姿态模型，仅使用姿态层，从文本生成单帧多人姿态。
- **第二阶段**：在每个姿态层后插入运动层，冻结所有姿态层参数，仅训练运动层。该冻结策略确保运动数据不会干扰第一阶段学到的高质量姿态表示。

**7. 引导模型（Guidance Models）**

采样时额外引入独立的文本到姿态模型 $G_p$ 和文本到单人运动模型 $G_m$，与多人模型 $G$ 的输出加权组合，以增强姿态合理性与运动质量。

### 核心公式推导

**扩散前向过程**

多人运动序列的马尔可夫加噪过程定义为：

$$q(x_t^{1:N,1:F} \mid x_{t-1}^{1:N,1:F}) = \mathcal{N}(\sqrt{\alpha_t} x_{t-1}^{1:N,1:F}, (1-\alpha_t)I)$$

其中 $x_t^{1:N,1:F}$ 表示 $t$ 时刻的噪声化序列，$\alpha_t$ 为噪声调度参数。

**去噪训练目标**

模型 $G$ 以噪声样本 $x_t$、时间步 $t$ 和条件 $c$（文本及参考姿态帧）为输入，直接预测原始信号 $x_0$，损失函数为：

$$\mathcal{L} = \mathbb{E}_{x_0 \sim q(x_0|c), t \sim [1,T], x_t \sim q_t(x_t|x_0,c)} \left[ \| x_0 - G(x_t, t, c) \|_2^2 \right]$$

此即 $x_0$-prediction 形式的简化扩散损失。

**无分类器引导（Classifier-Free Guidance）**

采样时，通过引导尺度 $s$ 增强文本条件的对齐程度：

$$G_s(x_t, t, c) = G(x_t, t, \emptyset) + s \cdot (G(x_t, t, c) - G(x_t, t, \emptyset))$$

其中 $\emptyset$ 表示空文本条件，$s > 1$ 时放大条件信号。

**姿态/运动联合引导**

将多人模型输出与独立的姿态引导模型 $G_p$、运动引导模型 $G_m$ 线性组合，权重满足 $s_p + s_m \leq 1$：

$$G_{s_p, s_m}(x_t, t, c) = (1 - s_p - s_m) \cdot G(x_t, t, c) + s_p \cdot G_p(x_t, t, c) + s_m \cdot G_m(x_t, c)$$

该公式使得采样过程同时受多人交互约束、逐帧姿态合理性和逐主体运动连贯性三方面信号的共同指导。

### 补充图表

![[assets/figures/papers/paper_list_l1766_Towards_Open_Domain_Text_Driven_Synthesis_of_Multi_Person_Motions/figures/002_Figure_2.jpg]]
*Figure 2: Dataset visualizations. Top 2 rows: LAION-Pose dataset. Left is original image from LAION-400M [59], right is BEV [63] detection. Bottom 2 rows: Webvid-Motion dataset. Left is original video first frame from WebVid-10M [2], right is the motion sequence estimated by TRACE [62] visualized from a different camera angle*

## 实验与分析

### 主实验结果

为验证所提方法在开放域多人运动生成上的有效性，作者从多人和双人两个维度进行了定量评估。由于缺乏统一的多人运动生成基准，评估采用解耦的**姿态质量**与**运动质量**指标：姿态指标（P-FID、P-R-Precision）在 LAION-Pose 数据集上计算，运动指标（M-FID、M-Diversity）在 HumanML3D 或 InterHuman 数据集上计算。

**多人生成对比。** 作者将完整模型与两个朴素基线进行对比：仅使用姿态层（Pose-Only）和仅使用运动层（Motion-Only）。如表 1 所示，完整模型在 P-FID 上为 0.229，介于 Pose-Only（0.077）和 Motion-Only（0.317）之间；在 M-FID 上为 0.684，优于 Pose-Only（0.903）但略逊于 Motion-Only（0.613）。这一结果表明，交错姿态层与运动层的设计在姿态逼真度和运动自然度之间取得了平衡——单独任一方都会在另一维度上明显劣化。

**双人生成对比。** 作者进一步将模型限制为双人输出，与现有双人运动生成方法 **InterGen**（Liang et al., arXiv 2023）、**RIG**（Tanaka et al., ICCV 2023）和 **ComMDM**（Shafir et al., arXiv 2023）进行对比。如表 2 所示，本文方法在 P-R-Precision Top-1 上达到 **0.323**，远超 InterGen 的 0.073（提升 +0.250），表明生成姿态与开放域文本的对齐程度显著更强。需要指出的是，基线方法均在受限的两人交互数据集上训练，而本文模型面向开放域提示评估，提示域差异可能导致基线表现偏低，但结果仍清晰地展示了本文方法在开放域场景下的泛化优势。

### 消融实验

作者通过消融实验（Table 3）系统验证了各设计选择的有效性：

- **两阶段训练 vs. 单阶段训练（A）。** 移除预训练的姿态模型条件、直接采用单阶段联合训练，性能明显下降。这表明高质量的文本到姿态模型能为第二阶段提供强条件信号，使每一帧的姿态更加合理。
- **冻结姿态层 vs. 解冻姿态层（B）。** 在第二阶段联合训练时解冻预训练的姿态层同样导致性能退化。这说明运动数据可能干扰姿态层在第一阶段学到的高质量姿态表示，冻结策略有效保护了姿态知识。
- **移除 WebVid-Motion 数据（C）。** 去掉来自 WebVid-10M 视频的运动数据后，P-R-Precision Top-1 从 0.539 降至 0.383，降幅显著。这验证了视频运动数据对增强文本-姿态对齐的关键作用。
- **移除所有运动文本（D）。** 进一步去除与运动相关的文本描述，姿态与文本的对齐度继续下降，表明运动文本提供了互补的语义监督信号。

### 定性结果

图 4 展示了文本到姿态生成的定性结果，模型能够根据开放域文本描述生成包含多人、姿态合理且空间关系协调的单帧姿态。图 5 展示了文本到运动生成的定性结果，生成的多人运动序列在时序上连贯，且不同主体间的交互行为与文本描述一致。这些可视化结果与定量指标相互印证，表明交错姿态层与运动层的设计有效解耦了帧内交互建模与时序运动建模。

### 关键图表结论

- **图 1** 概括了多源数据联合训练与两阶段生成管线的整体流程，是理解方法全貌的核心图示。
- **图 3** 详细展示了交错姿态层和运动层的扩散框架结构，包括维度重塑机制和条件嵌入方式。
- **表 2** 是本文最具说服力的定量证据：在开放域双人运动生成上，P-R-Precision Top-1 以 0.323 大幅领先 InterGen 的 0.073。
- **表 3** 的消融结果系统证实了两阶段训练、冻结姿态层、以及视频运动数据三个设计选择的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l1766_Towards_Open_Domain_Text_Driven_Synthesis_of_Multi_Person_Motions/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative result for text-to-pose generation*

![[assets/figures/papers/paper_list_l1766_Towards_Open_Domain_Text_Driven_Synthesis_of_Multi_Person_Motions/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative results for text-to-motion generation*

![[assets/figures/papers/paper_list_l1766_Towards_Open_Domain_Text_Driven_Synthesis_of_Multi_Person_Motions/figures/007_Table_1.jpg]]
*Table 1: Quantitative metrics comparing our multi-person results with naive baselines. Metrics for real data are evaluated with LAION-Pose and HumanML3D*

![[assets/figures/papers/paper_list_l1766_Towards_Open_Domain_Text_Driven_Synthesis_of_Multi_Person_Motions/figures/008_Table_2.jpg]]
*Table 2: Quantitative metrics comparing our 2-person results with baselines. The pose and motion metrics for real data are evaluated with LAION-Pose and InterHuman [39]*

![[assets/figures/papers/paper_list_l1766_Towards_Open_Domain_Text_Driven_Synthesis_of_Multi_Person_Motions/figures/009_Table.jpg]]

## 方法谱系与知识库定位

### 技术继承与演进

本文方法直接构建在 **MDM**（Tevet et al., ICCV 2023）的 Transformer 编码器扩散框架之上，将其从单人运动生成扩展至多人场景。核心继承点在于：以预测原始信号 $x_0$ 替代噪声预测的训练目标（Equation 2），以及基于 Transformer 的扩散去噪骨干网络。在此基础上，本文引入了两个关键的结构性创新：**交错式 pose/motion 层**和**两阶段训练策略**，以解耦帧内多人交互与单主体时序运动的学习。

与现有两人运动生成方法相比，本文的差异化定位体现在三个维度：

- **InterGen**（Liang et al., arXiv 2023）和 **ComMDM**（Shafir et al., arXiv 2023）均面向受限的两人交互场景，训练数据为动作捕捉工作室采集的双人交互数据，提示分布局限于明确的交互类别。本文通过从 LAION-400M 图像和 WebVid-10M 视频中估计姿态与运动，构建了覆盖开放域文本描述的大规模多人数据集，使模型能够处理任意人数（最多 10 人）的生成。
- **RIG**（Tanaka et al., ICCV 2023）同样聚焦双人生成，但架构上未显式分离帧内姿态关系与时序运动建模。本文的交错层设计通过维度重塑操作，使 pose 层逐帧学习多人空间关系，motion 层逐主体学习时序动态，实现了对这两个正交因素的显式解耦。
- 在训练策略上，已有方法普遍采用单阶段端到端训练，而本文的两阶段训练先独立训练文本到姿态模型（8 层 pose 层），再冻结姿态层插入 motion 层训练运动生成模型（8 对 pose+motion 层）。消融实验表明，单阶段模型（A）和联合训练时解冻姿态层（B）均会导致性能下降，验证了高质量姿态条件信号对运动生成的关键作用以及运动数据可能干扰姿态表示的风险。

### 适用边界与局限

本文方法适用于开放域文本描述驱动的多人运动生成任务，在提示多样性和人数灵活性上显著超越了现有基线。然而，其适用边界和潜在局限需要明确：

1. **评估度量的分解性**：由于缺乏真正的多人运动评估指标，本文采用分解式评估——分别用 LAION-Pose 评估姿态质量（P-FID, P-R-Precision）和 HumanML3D 或 InterHuman 评估运动质量（M-FID）。这种分解评估与真实多人运动感知质量之间的相关性尚未建立，属于开放问题。
2. **数据依赖与分布偏差**：模型性能高度依赖 LAION-Pose（800 万图像-姿态-文本三元组）和 WebVid-Motion（3500 视频-运动-文本三元组）的质量。消融实验显示，移除 WebVid-Motion 数据（C）会导致 P-R-Precision Top-1 从 0.539 降至 0.383，移除所有运动文本（D）同样降低姿态-文本对齐。这表明运动文本数据的规模和覆盖度是当前性能的重要约束。
3. **与基线比较的域差异**：在两人运动生成评估中（Table 2），本文模型与 InterGen 等基线存在提示域不匹配——本文模型在开放域提示上评估，而基线在受限交互类别上训练。P-R-Precision Top-1 达到 0.323（vs InterGen 0.073）的优势部分反映了开放域训练的泛化能力，但严格受控比较仍需进一步验证。
4. **计算开销**：两阶段训练需要 4 块 GPU 训练 1 天（第一阶段 500k 步）和 8 块 A100 GPU 训练 2 天（第二阶段 250k 步），相比单阶段方法增加了训练复杂度和资源需求。

### 开放问题

1. 如何设计一个真正面向多人运动的统一评估指标，能够同时捕捉帧内交互质量和时序运动一致性，而非依赖分解式度量的组合？
2. 交错 pose/motion 层的 Transformer 编码器内部架构细节（如注意力头数、前馈网络维度、层归一化位置等）在论文中未完全展开，其对不同人数规模的可扩展性有待进一步分析。
3. 当前方法通过冻结姿态层隔离运动数据对姿态表示的干扰，是否存在更优雅的联合训练策略（如梯度解耦、多任务学习）能够在保留姿态质量的同时实现端到端优化？

## 原文 PDF

![[paperPDFs/ECCV_2024/Towards_Open_Domain_Text_Driven_Synthesis_of_Multi_Person_Motions.pdf]]