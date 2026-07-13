---
title: "Large Motion Model for Unified Multi-modal Motion Generation"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Large_Motion_Model_for_Unified_Multi_modal_Motion_Generation.pdf
project_link: https://mingyuan-zhang.github.io/projects/LMM.html
code_link: null
aliases:
- LMML
- LMMUMMMG
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "统一的运动表示（基于TOMATO分解为10个身体部位）和部件感知注意力机制ArtAttention，使模型能够同时处理多任务、多模态输入并整合异质知识。"
primary_logic: "将人体运动分解为独立身体部位，利用注意力机制融合多模态条件，结合无监督预训练（随机帧率/掩码）与有监督微调，可在统一框架下实现跨任务运动生成，展现出涌现能力。"
claims:
- "LMM在HumanML3D文本到运动生成上实现最低FID 0.040和最高RPrecision Top-1 0.525，优于所有专家模型。"
- "在运动预测任务中，LMM-Large在AMASS（1000ms MPJPE 63.1 mm）和3DPW（1000ms MPJPE 68.0 mm）上显著优于其他方法。"
- "ArtAttention在大型运动模型场景下比原始SAMI（FineMoGen）更有效。"
- "随机下采样和随机掩码预训练策略显著提升多模态指标，是预训练的必要组件。"
---

# Large Motion Model for Unified Multi-modal Motion Generation

> [!tip] 核心洞察
> 将人体运动分解为独立身体部位，利用注意力机制融合多模态条件，结合无监督预训练（随机帧率/掩码）与有监督微调，可在统一框架下实现跨任务运动生成，展现出涌现能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向统一多模态运动生成的大规模运动模型 |
| 英文题名 | Large Motion Model for Unified Multi-modal Motion Generation |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://doi.org/10.1007/978-3-031-72624-8_23) · [Project](https://mingyuan-zhang.github.io/projects/LMM.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Large Motion Model (LMM) |
| Dataset | HumanML3D (Text-to-Motion), HumanML3D, AMASS (Motion Prediction), 3DPW (Motion Prediction) |

> [!tip] 效果简介
> - HumanML3D (Text-to-Motion) 上，FID 为 0.040 (LMM-Large)，对比 0.544 (MDM)，变化 -0.504。
> - HumanML3D 上，Top-1 RPrecision 为 0.525 (LMM-Large)，对比 0.491 (T2M-GPT)，变化 +0.034。
> - AMASS (Motion Prediction) 上，MPJPE@1000ms (mm) 为 63.1 (LMM-Large)，对比 see Table 4，变化 lower。

## 概要

多模态人体运动生成长期面临三个结构性瓶颈：**数据格式碎片化**（不同数据集采用SMPL、BVH、关节角度等异构表示）、**评价指标不统一**（各任务使用各自独立的度量体系）以及**任务间知识迁移困难**（单一任务模型无法复用其他任务学到的运动先验）。这些瓶颈导致现有方法普遍停留在“一任务一模型”的专家范式，泛化能力严重受限。

本文提出 **Large Motion Model (LMM)**，首个面向统一多模态运动生成的通才模型。其核心洞察在于：将人体运动按解剖结构分解为10个独立身体部位，利用部件感知注意力机制融合多模态条件信号，配合无监督预训练与有监督微调的两阶段策略，可在单一框架下同时处理文本到运动、运动预测、音乐到舞蹈等多种任务，并展现出跨任务的涌现能力。

在方法定位上，LMM以 **FineMoGen**（Zhang et al., NeurIPS 2023）的SAMI注意力模块为架构起点，进行了三个关键维度的改造：将运动表示统一为基于TOMATO的10部位分解格式；将注意力机制扩展为支持多模态条件、可变帧率和缺失部位处理的 **ArtAttention**；将训练策略从单任务有监督学习升级为“随机下采样+随机掩码”无监督预训练与多任务微调的组合。多模态条件（文本、语音、音乐、视频）通过ImageBind统一编码后注入模型。

实验层面，LMM在九个广泛使用的基准上取得了有竞争力的结果。在 **HumanML3D** 文本到运动生成任务上，LMM-Large实现了最低FID **0.040**（对比MDM的0.544）和最高RPrecision Top-1 **0.525**；在 **AMASS** 和 **3DPW** 运动预测任务上，1000ms的MPJPE分别降至 **63.1 mm** 和 **68.0 mm**，显著优于现有方法。消融实验证实，随机掩码预训练和ArtAttention架构是性能提升的必要组件。模型的主要局限在于音乐到舞蹈任务的FID指标未全面超越专家模型（推测因音乐数据占比较小），且最大参数量达760M，对轻量化部署不友好。

人体运动生成是计算机视觉与图形学中的核心问题，涵盖文本到运动、运动预测、音乐到舞蹈、语音手势生成等多种任务。然而，该领域长期面临三大结构性瓶颈：

**数据格式碎片化。** 不同任务依赖异构数据集，运动表示格式各异（如SMPL参数、关节旋转矩阵、3D坐标序列），缺乏统一的中间表示。这导致模型难以跨数据集联合训练，知识无法复用。

**评价体系割裂。** 各子任务采用不同的评估指标和协议，缺乏可比较的基准。例如，文本到运动生成关注FID和R-Precision，运动预测则使用MPJPE，音乐到舞蹈还需评估节拍对齐分数。这种割裂使得难以系统性衡量模型的泛化能力。

**任务间知识迁移困难。** 现有方法多为单任务专家模型，如**MDM**（Tevet et al., ICLR 2022）专注于文本到运动的扩散生成，**Bailando**（Siyao et al., CVPR 2022）针对音乐到舞蹈设计，**EDGE**（Tseng et al., CVPR 2023）则在音乐驱动舞蹈上采用编舞导向的扩散策略。这些模型在各自任务上表现良好，但无法利用其他任务的数据与监督信号，泛化能力受限。

上述瓶颈的根源在于缺乏一个统一的框架，能够同时处理多模态条件输入（文本、语音、音乐、视频）、兼容不同运动表示格式，并在多任务联合训练中实现正向知识迁移。**FineMoGen**（Zhang et al., NeurIPS 2023）提出的SAMI注意力机制在细粒度运动生成上取得了进展，但其设计仍局限于单模态条件和固定帧率场景，无法直接扩展为通用运动生成模型。

本文的核心动机是构建第一个通用多模态运动生成模型——Large Motion Model (LMM)，通过统一数据格式、部件感知注意力机制和无监督预训练策略，在单一框架内解决多任务运动生成问题，并探索大规模混合训练带来的涌现能力。

## 核心方法与创新机理

LMM 的核心创新围绕三个“可变插槽”（changed slots）展开，分别对应运动表示、注意力机制与训练策略的系统性重构，使其从单任务专家模型跃迁为统一的多模态运动生成通才。

### 1. 统一运动表示：TOMATO 分解为 10 个身体部位

此前运动生成模型通常绑定单一数据格式（如 SMPL 参数），不同任务间数据无法互通。LMM 采用 **TOMATO** 作为统一中间表示，并进一步将全身运动显式分解为 **10 个独立身体部位**（Section 3.3）。这一设计的关键因果作用是：它将“全身运动生成”转化为“多个子部位的运动补全”，使模型天然具备处理**部分身体可见、可变帧率、跨数据集格式**的能力。形式上，每帧运动表示 $m_i$ 包含根关节角速度 $\dot{r}^a$、线速度 $\dot{r}^x, \dot{r}^z$、根高度 $r^y$，以及各关节的位置 $\mathbf{j}^p$、速度 $\mathbf{j}^v$、旋转 $\mathbf{j}^r$ 和面部表情 $\mathbf{f}$（Eq. 2）。

为桥接统一表示与各数据集的特定输出格式，LMM 在输入/输出端分别引入 **Read-In / Read-Out 层**（Section 4.2）。这些轻量的数据集相关转换器仅在测试阶段按需调用，核心模型始终在统一表示空间中运行，避免了多任务训练中的表示冲突。

### 2. 部件感知注意力：ArtAttention

LMM 的架构主干基于 **FineMoGen**（Zhang et al., NeurIPS 2023）中的 SAMI 模块，但对其注意力机制进行了关键升级，形成 **ArtAttention**（Section 4.3）。升级针对三个新需求：

- **多模态条件融合**：文本、语音、音乐、视频等异构条件信号先经 **ImageBind** 编码为统一特征序列 $\mathbf{C}_t, \mathbf{C}_s, \mathbf{C}_m, \mathbf{C}_v$，再通过两层可学习的 Transformer 编码器精炼后注入注意力计算。
- **可变帧率处理**：ArtAttention 不对帧率做硬性假设，使模型能适应预训练中随机下采样引入的帧率变化。
- **缺失身体部位处理**：由于数据中天然存在不完整身体标注，且预训练阶段会人工掩码部分身体部位，ArtAttention 采用**逐帧动态计算注意力系数**，而非固定系数集合，从而鲁棒地处理部位缺失。

ArtAttention 的输出为空间注意力（身体部位注意力）$\mathbf{Y_s}$ 与时间注意力 $\mathbf{Y_t}$ 之和：$\mathbf{Y} = \mathbf{Y_s} + \mathbf{Y_t}$。消融实验证实，在大规模运动模型场景下，ArtAttention 相比原始 SAMI 更有效（Section 5.3，置信度 0.95）。

### 3. 两阶段训练策略：无监督预训练 + 有监督微调

LMM 摒弃了单任务有监督训练范式，转而采用**无监督预训练 + 有监督微调**的两阶段策略（Section 4.4）：

- **预训练阶段**：仅使用运动数据本身，通过**随机下采样**和**随机掩码**两种增强策略，迫使模型学习鲁棒的运动先验。消融实验（Table 6）表明，随机掩码是预训练的**必要组件**，而下采样与掩码策略共同提升了文本到运动任务中的多模态指标（置信度 0.95）。
- **微调阶段**：引入多模态条件信号，训练条件与运动的关联。为支持**无分类器引导（classifier-free guidance）**，训练时以 10% 概率随机丢弃条件信号。

这种训练策略的因果机制在于：预训练阶段让模型在无标签的大规模运动数据上习得通用的运动动力学先验，微调阶段则仅需学习条件-运动的映射关系。两者解耦使得模型能够高效吸收来自 16 个数据集、10 种任务的异质知识，最终在统一框架下展现出跨任务的涌现能力。

### 创新总结

| 可变插槽 | Baseline 值 | LMM 方案 | 因果作用 |
|---------|------------|---------|---------|
| 运动表示 | 单一格式（如 SMPL） | TOMATO 分解为 10 个身体部位 | 统一多数据集格式，支持部分身体生成 |
| 注意力机制 | SAMI（FineMoGen） | ArtAttention | 融合多模态条件，处理可变帧率与部位缺失 |
| 训练策略 | 单任务有监督 | 无监督预训练 + 有监督微调 | 吸收异质大规模数据，解耦运动先验与条件映射 |
| 条件输入 | 单一模态（如文本） | ImageBind 统一多模态编码 | 使文本、语音、音乐、视频条件可互换 |

![[assets/figures/papers/paper_list_l34_https_doi_org_10_1007_978_3_031_72624_8_23/figures/005_Figure_3.jpg]]
*Figure 3: Overall pipeline of LMM. Left: Our two-stage training procedure, including unsupervised pretraining and supervised fine-tuning. Random down-sampling and random mask strategies are applied to enhance knowledge absorption. Right: The generic inference process of LMM. The noised motion sequence and the given context are initially merged before being input into the network. LMM will then synthesize motion sequences, consistent with the provided multi-modal condition signals*

LMM 的整体框架围绕一个统一的运动生成范式构建，其核心思想是将异构的运动生成任务抽象为统一的数学形式，并通过两阶段训练策略（无监督预训练 + 有监督微调）在单一模型中整合多模态条件与多任务知识。

### 统一问题形式化

LMM 将所有运动生成任务统一为以下形式：

$$\Theta = M ( \mathbf { x } , \mathbf { m } , \mathbf { c } )$$

其中 $M$ 为运动生成函数，$\mathbf{x}$ 表示运动数据，$\mathbf{m}$ 定义可见性范围（即哪些帧或身体部位被掩码），$\mathbf{c}$ 为多模态条件控制信号。通过调整 $\mathbf{m}$ 的掩码边界，同一框架可涵盖文本到运动生成、运动预测、运动补全、音乐到舞蹈等多种任务（任务定义详见 Table 1）。

### 两阶段训练与推理流程

如 Figure 3 所示，LMM 的 pipeline 分为两个阶段：

**无监督预训练阶段**：模型仅从大规模运动数据中学习运动先验，不依赖任何条件信号。此阶段引入两个关键增强策略——**随机下采样**（random down-sampling）和**随机掩码**（random masking）——以提升模型对可变帧率和缺失身体部位的鲁棒性。消融实验证实，这两种策略是预训练的必要组件，尤其对提升文本到运动任务的多模态指标有显著贡献（Table 6, Section 5.3）。

**有监督微调阶段**：模型接收预处理后的多模态条件 token 序列作为额外输入，学习条件信号与运动之间的关联。为支持无分类器引导（classifier-free guidance），训练中条件信号以 10% 的概率被随机掩码。

推理时，带噪声的运动序列与给定的上下文条件先进行融合，再输入网络；LMM 据此合成与多模态条件信号一致的运动序列。

### 模块关系与数据流

LMM 的架构以 **Transformer 扩散模型**为基础，数据流经以下核心模块（详见 Figure 4）：

1. **Read-In / Read-Out 层**：负责数据集相关的运动编解码。Read-In 将统一中间表示映射到隐空间特征，Read-Out 则将生成结果转换回特定数据集的表示格式。
2. **ArtAttention 模块**：作为网络主干的核心计算单元，通过空间注意力（身体部位注意力）和时间注意力两个分支细化特征表示。该模块在 FineMoGen（Zhang et al., NeurIPS 2023）的 SAMI 基础上进行了三项关键升级：支持多模态条件输入、处理可变帧率、容忍缺失身体部位（Section 4.3）。
3. **多模态条件编码**：文本、语音、音乐、视频等异构条件信号通过 **ImageBind** 统一编码为 token 序列，再经两层可学习的 Transformer 编码器精炼后注入 ArtAttention 模块。

最终，ArtAttention 的空间注意力输出 $\mathbf{Y_s}$ 与时间注意力输出 $\mathbf{Y_t}$ 相加得到模块输出 $\mathbf{Y} = \mathbf{Y_s} + \mathbf{Y_t}$，完成对运动特征的多维度融合与精炼。

LMM 的核心架构围绕三个关键设计展开：统一运动表示、ArtAttention 注意力机制，以及两阶段训练策略。以下逐一剖析其机理与公式含义。

### 统一运动表示：TOMATO 分解

LMM 将所有运动数据统一转换为基于 TOMATO 的中间表示，并进一步将人体分解为 10 个独立身体部位。这一分解是模型处理多数据源、多任务的核心前提。

对于第 $i$ 帧，统一运动表示定义为：

$$m _ { i } = \left\{ \dot { r } ^ { a } , \dot { r } ^ { x } , \dot { r } ^ { z } , r ^ { y } , \mathbf { j } ^ { p } , \mathbf { j } ^ { v } , \mathbf { j } ^ { r } , \mathbf { f } \right\}$$

各变量含义如下：
- $\dot{r}^a, \dot{r}^x, \dot{r}^z$：根关节绕各轴的角速度
- $r^y$：根关节的高度
- $\mathbf{j}^p, \mathbf{j}^v, \mathbf{j}^r$：局部关节的位置、速度、旋转
- $\mathbf{f}$：面部表情参数

该表示将人体运动信息完整编码为结构化向量，10 个身体部位的划分使得模型能够独立关注各部位的运动模式，同时天然支持缺失部位的处理——当某部位数据不可用时，对应位置可直接置为可学习的空标记。

### 统一问题形式化

所有运动生成任务被统一为如下形式：

$$\Theta = M ( \mathbf { x } , \mathbf { m } , \mathbf { c } )$$

其中：
- $\mathbf{x}$：运动数据序列
- $\mathbf{m}$：可见性范围掩码，定义哪些帧/部位需要生成
- $\mathbf{c}$：多模态条件控制信号（文本、语音、音乐、视频等）
- $M$：运动生成函数，由 LMM 参数化

这一形式化将文本到运动生成、运动预测、音乐到舞蹈等异构任务统一为同一框架下的条件生成问题，差异仅体现在 $\mathbf{m}$ 和 $\mathbf{c}$ 的具体取值上。

### ArtAttention：身体部位感知注意力

ArtAttention 是 LMM 的核心计算模块，在 **FineMoGen**（Zhang et al., NeurIPS 2023）的 SAMI 模块基础上进行了三项关键升级：
1. **多模态条件注入**：支持同时接收文本、语音、音乐、视频等多种条件信号
2. **可变帧率处理**：适应不同数据集的帧率差异
3. **缺失身体部位处理**：兼容数据固有的缺失部位和预训练中人工掩码的部位

ArtAttention 的最终输出为空间注意力与时间注意力之和：

$$\mathbf{Y} = \mathbf{Y_s} + \mathbf{Y_t}$$

其中 $\mathbf{Y_s} \in \mathbb{R}^{F \times H \times D}$ 为身体部位（空间）注意力输出，$\mathbf{Y_t}$ 为时间注意力输出。$F$ 为帧数，$H$ 为身体部位数（10），$D$ 为特征维度。

在身体部位注意力分支中，模型对每一帧独立计算部位间的注意力权重。由于数据中存在固有缺失部位和预训练引入的人工掩码部位，注意力系数无法固定，而是根据各部位的实际可用性动态调整。这一设计使得模型在训练和推理中都能鲁棒地处理不完整的运动输入。

多模态条件信号通过 **ImageBind** 统一编码为 token 序列，再经两层可学习的 Transformer 编码器精炼后注入 ArtAttention。条件 token 序列的形式为：

$$\mathbf{C}_t \in \mathbb{R}^{L_t \times (H \cdot D)}, \quad \mathbf{C}_s \in \mathbb{R}^{L_s \times (H \cdot D)}, \quad \mathbf{C}_m \in \mathbb{R}^{L_m \times (H \cdot D)}, \quad \mathbf{C}_v \in \mathbb{R}^{L_v \times (H \cdot D)}$$

分别对应文本、语音、音乐、视频条件，$L_*$ 为各模态的 token 长度。

### 预训练与微调策略

**预训练阶段**采用无监督学习，核心操作包括：
- **随机下采样**：以不同帧率采样运动序列，增强模型对可变帧率的鲁棒性
- **随机掩码**：随机遮蔽部分身体部位或帧，迫使模型学习从部分观测重建完整运动的能力

被掩码的部位（由 $\mathbf{M}_t$ 标记）替换为可学习的空 token，损失计算时忽略由 $\mathbf{M}_s$ 标记的部位。消融实验证实，随机掩码是预训练的**必要组件**，与下采样共同作用可显著提升文本到运动任务的多模态指标（Table 6）。

**有监督微调阶段**引入条件信号，将预处理后的条件 token 序列作为额外输入。为支持无分类器引导（classifier-free guidance），训练时以 10% 概率随机丢弃条件信号。推理时，通过调节引导强度可在生成质量与条件一致性之间取得平衡。

### 数据集适配层

Read-In 层和 Read-Out 层作为数据集相关的编解码器，负责在统一中间表示与各数据集特定格式之间进行转换。这一设计将数据格式差异隔离在输入输出端，使核心网络完全与具体数据集解耦，是实现多数据集联合训练的关键工程组件。

## 实验与关键发现

### 主实验结果

LMM 在文本到运动生成、运动预测和音乐到舞蹈生成三个核心任务上进行了全面评估，验证了统一多模态运动生成框架的有效性。

**文本到运动生成（HumanML3D）**。LMM-Large 在所有关键指标上均取得最优或次优结果（Table 3）。具体而言，FID 降至 **0.040**，较 MDM（Tevet et al., ICLR 2022）的 0.544 大幅降低 0.504，表明生成运动的分布与真实运动高度一致。在文本-运动匹配精度上，Top-1 RPrecision 达到 **0.525**，超越 T2M-GPT（Zhang et al., arXiv 2023）的 0.491；MultiModality 指标为 2.943，在多样性与准确性之间取得平衡。值得注意的是，LMM 作为通用模型，在未针对该任务进行专门设计的情况下，超越了所有专家模型，这直接验证了多任务联合训练带来的知识迁移效应。


**运动预测（AMASS / 3DPW）**。在长时预测场景下，LMM-Large 展现出显著优势（Table 4）。在 AMASS-BMLrub 上，1000ms 预测的 MPJPE 降至 **63.1 mm**；在更具挑战性的 3DPW 数据集上，1000ms 预测的 MPJPE 为 **68.0 mm**，均显著优于现有方法。这表明统一运动表示和随机掩码预训练策略使模型能够学习到鲁棒的运动动力学先验，对长时依赖关系建模尤为有效。

![[assets/figures/papers/paper_list_l34_https_doi_org_10_1007_978_3_031_72624_8_23/figures/008_Table_4.jpg]]
*Table 4: Quantitative results of motion prediction on the AMASS and 3DPW test set for different time steps (ms). We report the MPJPE error in mm*

**音乐到舞蹈生成（AIST++）**。LMM-Large 取得有竞争力的结果（Table 5）：FID_k 为 22.08，FID_g 为 21.97，Best Align Score 为 0.2249。然而，FID 指标未能全面超越 Bailando（Siyao et al., CVPR 2022）和 EDGE（Tseng et al., CVPR 2023）等专家模型。作者推测这是由于 MotionVerse 数据集中音乐到舞蹈数据的占比较小，导致模型在该任务上的训练信号相对不足。

![[assets/figures/papers/paper_list_l34_https_doi_org_10_1007_978_3_031_72624_8_23/figures/009_Table_5.jpg]]
*Table 5: Quantitative results for Music-conditioned Dance Generation. Quantitative results on AIST++ test set*

### 消融实验

消融实验围绕预训练策略和注意力机制两个核心设计展开，均在 LMM-Base 上进行。

**预训练策略的必要性**。Table 6 展示了预训练组件的消融结果。随机掩码被证实是预训练的**必要组件**：移除随机掩码后，模型在文本到运动任务上的多模态指标出现明显下降。进一步分析表明，随机下采样和随机掩码策略**共同作用**才能有效提升多模态指标，单独使用其中一种策略均无法达到最优效果。其因果机制在于：随机下采样迫使模型适应不同帧率，随机掩码则强制模型利用未掩码的身体部位推断完整运动，两者共同增强了模型对运动先验的归纳偏置。

![[assets/figures/papers/paper_list_l34_https_doi_org_10_1007_978_3_031_72624_8_23/figures/010_Table_6.jpg]]
*Table 6: Ablation of the pretraining strategy. All experiments utilized LMM-Base as the base model*

**ArtAttention 的有效性**。与 FineMoGen（Zhang et al., NeurIPS 2023）中的原始 SAMI 模块相比，ArtAttention 在大型运动模型场景下表现出更强的适用性。这一差异源于 ArtAttention 的三个关键升级：支持多模态条件输入、处理可变帧率、以及允许缺失身体部位——这些能力在单一任务场景下并不关键，但在统一多任务框架中成为性能瓶颈。

### 定性分析

LMM-Large 的生成结果展示了细粒度控制能力（Figure 5）。在文本驱动生成中，模型能准确响应多样化的语义描述，包括复杂动作序列和空间关系约束。在多模态条件生成中，模型能够同时遵循文本指令和音乐节拍，生成语义正确且节奏同步的运动序列。这体现了 ArtAttention 机制在融合异构条件信号方面的有效性。

![[assets/figures/papers/paper_list_l34_https_doi_org_10_1007_978_3_031_72624_8_23/figures/011_Figure_5.jpg]]
*Figure 5: Visualization results of LMM-Large. Figure a)-d) show examples of textdriven motion generation. Figure e) and f) show synthesized motion sequences under both textual and musical constraints*

### 失败模式与局限性

尽管整体表现优异，LMM 仍存在以下局限：

1. **数据稀疏任务性能不足**：音乐到舞蹈任务的 FID 指标未能超越专家模型，根本原因在于训练数据中音乐-运动配对样本占比过小，模型难以充分学习音乐节奏与运动风格的精细映射关系。
2. **计算资源需求高**：LMM-Large 参数量达 760M，推理和训练成本显著高于单任务专家模型，不利于轻量化部署和实时应用场景。
3. **零样本泛化能力待验证**：对于训练中未见的条件组合（如文本+视频），模型仍需额外微调或提示设计，其涌现能力的边界尚不明确。

### 关键图表结论

- **Table 3**：LMM-Large 在文本到运动生成上全面超越专家模型，FID 降至 0.040，验证了统一框架的知识整合能力。
- **Table 4**：LMM-Large 在长时运动预测上取得显著优势，1000ms MPJPE 降至 63.1 mm（AMASS）和 68.0 mm（3DPW）。
- **Table 5**：音乐到舞蹈生成表现有竞争力但未全面领先，揭示数据配比是影响多任务模型性能的关键因素。
- **Table 6**：随机下采样与随机掩码是预训练的必要组件，二者协同作用才能最大化多模态指标提升。
- **Figure 5**：定性结果展示模型在细粒度文本控制和多模态条件融合方面的涌现能力。

![[assets/figures/papers/paper_list_l34_https_doi_org_10_1007_978_3_031_72624_8_23/figures/001_Figure_1.jpg]]
*Figure 1: We present Large Motion Model (LMM), the first generalist multi-modal motion generation model, that can perform multiple motion generation tasks simultaneously and achieve competitive performance across nine widely used benchmarks*

## 定位与知识库关联

LMM 的方法谱系根植于**基于 Transformer 的扩散生成框架**与**运动感知注意力机制**两条技术路线，其直接架构基础来自 **FineMoGen**（Zhang et al., NeurIPS 2023）中的 SAMI 模块。LMM 并非简单复用，而是在三个维度上进行了结构性升级，使其从单任务专家模型跃迁为多任务通用模型。

### 与基线工作的继承与改造关系

**架构继承**：LMM 的模型骨架遵循“Transformer + 扩散”的经典范式，与 **MDM**（Tevet et al., ICLR 2022）等扩散运动生成模型共享框架哲学。其核心注意力模块 ArtAttention 直接脱胎于 FineMoGen 的 SAMI，但针对大规模多任务场景进行了三项关键改造：

1. **多模态条件注入**：原始 SAMI 仅处理单一条件模态，ArtAttention 引入 ImageBind 统一编码文本、语音、音乐、视频四类条件信号，并通过可学习的 Transformer 编码层将条件特征精炼为 $\mathbf{C}_t, \mathbf{C}_s, \mathbf{C}_m, \mathbf{C}_v$ 四组 token 序列，实现条件信号的统一接入。
2. **可变帧率适应**：SAMI 假设固定帧率输入，ArtAttention 通过身体部位注意力机制解耦帧间依赖，使模型能处理随机下采样后的非均匀时间序列。
3. **缺失身体部位处理**：传统注意力依赖固定系数矩阵，ArtAttention 针对数据固有的缺失部位（如不同数据集标注的身体关节数不同）和预训练阶段人工掩码的部位，采用动态注意力权重计算，避免对缺失部位产生虚假关联。

**运动表示革新**：与 **T2M-GPT**（Zhang et al., arXiv 2023）等采用离散 token 表示的模型不同，LMM 选择基于 TOMATO 的连续表示，并将其分解为 10 个独立身体部位。这一设计的因果作用在于：将“人体运动”从整体耦合信号解耦为局部独立部件的组合，使得模型能在预训练阶段通过随机掩码学习部件间的组合泛化，在微调阶段灵活适配不同数据集的身体关节定义。

**训练策略跃迁**：基线方法普遍采用单任务有监督训练，LMM 引入“无监督预训练 + 有监督微调”的两阶段策略。预训练阶段通过随机下采样和随机掩码两种数据增强，迫使模型学习运动本身的时空先验，而非特定任务的条件映射。消融实验证实，随机掩码是预训练的**必要组件**，下采样和掩码策略共同提升了文本到运动任务的多模态指标（Table 6）。

### 适用边界与任务覆盖

LMM 的形式化定义 $\Theta = M ( \mathbf{x}, \mathbf{m}, \mathbf{c} )$ 统一了 10 类运动生成任务，覆盖文本到运动、运动预测、音乐到舞蹈、运动补全等场景。其适用边界由以下因素决定：

- **数据覆盖密度**：在文本到运动（HumanML3D）和运动预测（AMASS, 3DPW）等数据充足的任务上，LMM-Large 取得最优或次优结果；但在音乐到舞蹈（AIST++）任务上，LMM-Large 的 FID 指标（FID_k 22.08, FID_g 21.97）未能全面超越专家模型 **Bailando**（Siyao et al., CVPR 2022）和 **EDGE**（Tseng et al., CVPR 2023），推测因训练数据中音乐数据占比较小。
- **身体部位完整性**：ArtAttention 虽能处理缺失部位，但对极度稀疏的关节输入（如仅 3-5 个关键点）的性能仍需验证。
- **条件组合泛化**：LMM 在文本+音乐联合条件下展现出涌现能力，但对于训练中未见过的条件组合（如文本+视频），其零样本泛化上限尚不明确。

### 局限与开放问题

**已识别的局限**：
1. **音乐到舞蹈任务的性能瓶颈**：大规模混合训练中，各任务数据量不均衡导致稀疏任务性能未达最优，任务间的平衡策略如何影响最终表现是待解问题。
2. **模型规模与部署成本**：LMM-Large 参数量达 760M，推理和训练资源需求高，不利于轻量化部署和实时应用。
3. **零样本泛化能力有限**：对于未见过的任务组合，仍需额外微调或提示设计，尚未展现出类似大语言模型的即插即用零样本能力。

**开放问题**：
1. 如何进一步提升数据稀疏任务（如稀疏关节、低帧率）的性能？是否可通过数据增强或元学习策略弥补？
2. 大规模混合训练中，各任务间的采样比例、损失权重等平衡策略如何系统性地影响最终表现？
3. 能否将 LMM 的部件感知注意力机制扩展到更高层次的人-场景/人-物交互生成，将环境上下文作为额外的“身体部位”纳入统一框架？
4. 模型对未见过的条件组合（如文本+视频）的泛化上限在哪里？是否需要引入跨模态对比学习等额外预训练目标？

### 知识库定位

LMM 在运动生成领域的知识图谱中占据“**通用基座模型**”的位置。与传统的单任务专家模型（如 MDM、T2M-GPT、Bailando、EDGE）不同，LMM 通过统一的运动表示和多模态条件接口，将多类运动生成任务收敛到同一参数空间中。其核心贡献不在于单一任务的指标突破，而在于**证明了大规模混合训练能够产生跨任务的涌现能力**——这一范式与 NLP 领域的 GPT 系列、CV 领域的通用视觉模型形成呼应，为运动生成领域从“任务专用模型”向“通用运动智能”的范式转变提供了首个可行方案。

## 原文 PDF

![[paperPDFs/ECCV_2024/Large_Motion_Model_for_Unified_Multi_modal_Motion_Generation.pdf]]
