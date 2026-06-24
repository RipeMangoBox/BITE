---
title: "TM-Mamba: Text-controlled Motion Mamba: Text-Instructed Temporal Grounding of Human Motion"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/TM_Mamba_Text_controlled_Motion_Mamba_Text_Instructed_Temporal_Grounding_of_Human_Motion.pdf
aliases:
- TCMMTM
- TM-Mamba
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 文本控制的选择机制（Text-Controlled Selection Mechanism）：将 Mamba 的状态转移矩阵 A、B、C、Δ 同时参数化为运动输入与文本查询的函数，使文本能够动态控制长序列中的信息传播。
primary_logic: 将 Mamba 的输入依赖选择机制扩展为文本条件选择，使模型根据文本查询自适应地聚焦于运动序列的相关局部，同时引入关系嵌入捕获人体骨架的图拓扑信息，仅以线性内存成本实现长序列的精确时间定位。
claims:
- 移除文本控制选择机制后，模型性能大幅下降（双向 mAP@Avg 从 41.6 降至 39.2）。
- 双向建模比单向建模显著提升性能（mAP@Avg 39.2 vs 30.7）。
- 在长序列上，经典 Transformer 在 1200 帧时发生 GPU 内存溢出，而 TM-Mamba 内存消耗呈线性增长。
- BABEL-Grounding (max length = 500) 上 mAP@IoU=0.1 = 53.9
---

# TM-Mamba: Text-controlled Motion Mamba: Text-Instructed Temporal Grounding of Human Motion

> [!tip] 核心洞察
> 将 Mamba 的输入依赖选择机制扩展为文本条件选择，使模型根据文本查询自适应地聚焦于运动序列的相关局部，同时引入关系嵌入捕获人体骨架的图拓扑信息，仅以线性内存成本实现长序列的精确时间定位。

| 字段 | 内容 |
|------|------|
| 中文题名 | 文本控制的运动状态空间模型：基于文本指令的人体运动时间定位 |
| 英文题名 | TM-Mamba: Text-controlled Motion Mamba: Text-Instructed Temporal Grounding of Human Motion |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2404.11375) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Text-Controlled Motion Mamba (TM-Mamba) |
| Dataset | BABEL-Grounding |

> [!tip] 效果简介
> - BABEL-Grounding (max length = 500) 上，mAP@IoU=0.1 53.9 vs 50.5 (Temporal Transformer) (+3.4)。

## 概述

**问题瓶颈**：文本驱动的人体运动时间定位（Text-based Human Motion Grounding, THMG）要求模型在未修剪的长序列中，根据自然语言查询精确标定对应运动片段的时间边界。现有基于 Transformer 的方法依赖全局时间自注意力，其计算复杂度随序列长度呈二次增长，在长序列场景下面临严重的内存与效率瓶颈——经典 Transformer 在 1200 帧时即发生 GPU 内存溢出。

**核心方法**：本文提出 **Text-Controlled Motion Mamba (TM-Mamba)**，将状态空间模型 Mamba 的输入依赖选择机制扩展为**文本条件选择**。其关键设计是让状态转移矩阵的参数 $\Delta, \mathbf{B}, \mathbf{C}$ 同时依赖运动输入与文本查询嵌入，使模型能够根据文本指令动态控制长序列中的信息传播，仅以线性内存成本实现全局上下文的精准提取。同时引入关系嵌入（基于自适应图卷积网络）捕获人体骨架的图拓扑信息，并采用双向非因果结构克服原始 Mamba 的单向限制。

**方法定位**：TM-Mamba 属于状态空间模型在结构化人体运动理解任务上的首次应用。相比经典 Transformer 和 Flash-Attention-2 高效变体，它以线性复杂度统一了时间全局上下文、语言查询控制与空间图拓扑建模。在方法谱系上，它继承 Mamba 的选择性扫描机制，但将条件依赖从纯输入驱动改造为跨模态文本驱动，同时融合了图神经网络的关系归纳偏置。

**主要结果**：
- 在 BABEL-Grounding 数据集上，TM-Mamba 在最大序列长度 500 帧时达到 mAP@IoU=0.1 的 53.9%，超越 Temporal Transformer 基线 3.4 个百分点。
- 消融实验表明，文本控制选择机制是性能的核心来源：移除后双向模型 mAP@Avg 从 41.6 降至 39.2；关系嵌入进一步带来 2.4 个百分点的提升。
- 内存效率方面，TM-Mamba 的 GPU 内存消耗随序列长度呈线性增长，而经典 Transformer 在 1200 帧时即发生内存溢出，验证了其在长序列场景下的显著优势。

## 背景与动机

### 任务定义与挑战

文本驱动的人体运动时间定位（Text-based Human Motion Grounding, THMG）旨在给定一段未修剪的长时间人体运动序列和一个自然语言查询，定位出与该文本描述在语义上对应的所有运动时间片段。与视频时间定位不同，THMG 直接操作三维骨架序列，需要模型同时理解人体关节的空间拓扑结构、运动序列的全局时序依赖，以及文本语义与运动模式的跨模态对齐。

该任务面临一个核心瓶颈：**运动序列通常长达数百甚至上千帧，而现有基于 Transformer 的模型在处理此类长序列时，其全局时间自注意力机制的计算复杂度随序列长度呈二次增长**。这意味着当序列长度增加时，GPU 内存消耗急剧膨胀，甚至导致内存溢出（Out of Memory, OOM），使得模型无法在长序列上高效完成精确的时间定位。

### 现有方法的局限

在时间定位领域，主流方法大多基于 Transformer 架构，依赖自注意力机制捕获全局上下文。然而，这类方法存在两个显著缺陷：

1. **二次计算瓶颈**：经典 Transformer 的自注意力计算复杂度为 $O(L^2)$（$L$ 为序列长度），当运动序列超过 1000 帧时，内存消耗已超出常规 GPU 的承载能力。即使采用 Flash-Attention-2 等高效变体，虽能缓解部分内存压力，但仍未从根本上改变二次复杂度的本质。

2. **缺乏文本引导的选择性**：现有模型通常将文本查询与运动特征进行简单的跨模态融合后，再通过自注意力进行全局建模。这种“先融合、后建模”的策略缺乏文本对时序信息传播的精细控制——模型无法根据文本查询的内容，自适应地决定运动序列中哪些帧的信息应该被保留和传播，哪些应该被抑制。

### 状态空间模型的机遇

近年来，状态空间模型（State Space Models, SSMs）在长序列建模领域展现出巨大潜力。特别是 Mamba 架构，通过引入**输入依赖的选择机制**，使得状态转移矩阵 $\mathbf{A}$、$\mathbf{B}$、$\mathbf{C}$ 和离散化步长 $\Delta$ 能够根据输入内容动态调整，从而在保持线性计算复杂度的同时，实现了对长序列中关键信息的选择性记忆与传播。这一特性恰好契合 THMG 任务对长序列高效建模的需求。

然而，原始 Mamba 的选择机制仅依赖于输入序列本身，无法接受外部条件（如文本查询）的引导。在 THMG 任务中，模型需要根据文本查询的语义内容来确定“哪些运动片段是相关的”——这要求选择机制能够同时感知运动输入和文本查询两个信息源。

### 本文动机与核心思路

基于上述分析，本文的核心动机是：**将 Mamba 的输入依赖选择机制扩展为文本条件选择机制，使文本查询能够动态控制长序列中的信息传播，从而以线性内存成本实现精确的时间定位**。

具体而言，本文提出 **Text-Controlled Motion Mamba (TM-Mamba)**，其关键创新在于：

- **文本控制的选择机制**：将 Mamba 的状态转移参数 $\Delta$、$\mathbf{B}$、$\mathbf{C}$ 同时参数化为运动输入和文本查询嵌入的函数，使模型能够根据文本语义自适应地聚焦于运动序列的相关局部。

- **关系嵌入的拓扑感知**：通过自适应图卷积网络（AGCN）捕获人体骨架的图拓扑信息，将关系嵌入与运动特征拼接后送入状态空间模型，弥补了原始 Mamba 处理单变量序列时缺乏关节拓扑建模的不足。

- **双向非因果结构**：采用双向 SSM 结构替代原始 Mamba 的单向因果建模，使每一帧的表示能够同时融合前后文信息，显著提升定位精度。

这一设计使得 TM-Mamba 能够在一个统一的框架内，同时完成时间全局上下文的提取、语言查询的条件控制以及空间图拓扑的建模，且全程保持线性内存成本。

## 核心创新

TM-Mamba 的核心创新在于将 Mamba 的输入依赖选择机制扩展为**文本控制选择机制（Text-Controlled Selection Mechanism）**，使状态空间模型（SSM）的参数同时依赖于运动输入和文本查询，从而以线性内存成本实现长序列上的文本驱动时间定位。

### 关键改动槽位

#### 1. 选择机制的条件依赖扩展

原始 Mamba 的选择机制中，状态转移矩阵的参数 $\mathbf{A}, \mathbf{B}, \mathbf{C}, \Delta$ 仅随输入 $\mathbf{X}$ 变化。TM-Mamba 将这些参数重新参数化为输入序列与文本查询嵌入 $\mathbf{q}$ 的联合函数，使文本能够动态控制长序列中的信息传播路径。消融实验直接验证了这一设计的决定性作用：**移除文本控制选择机制后，双向模型的 mAP@Avg 从 41.6 降至 39.2**（TABLE II），降幅显著。

#### 2. 关系嵌入注入骨架拓扑

原始 Mamba 处理的是单变量序列，缺乏对关节间拓扑关系的建模能力。TM-Mamba 引入自适应图卷积网络（AGCN）计算关系嵌入 $\mathbf{R}$，将人体骨架的图拓扑信息显式注入状态表示。消融结果表明，在文本控制选择的基础上加入关系嵌入后，mAP@Avg 从 39.2 进一步提升至 41.6（TABLE II），证实了拓扑感知对定位精度的增益。

#### 3. 双向非因果建模

原始 Mamba 采用单向因果建模，限制了全局上下文的捕获。TM-Mamba 借鉴 Vision Mamba 的设计，采用**双向非因果结构**，使模型能够同时利用前后文信息进行帧级激活预测。消融对比显示，双向建模相较单向建模实现大幅跃升（mAP@Avg 39.2 vs. 30.7），性能提升约 28%（TABLE II）。

### 创新点的协同效应

上述三个改动槽位并非孤立叠加，而是形成协同机制：文本控制选择决定“关注哪里”，关系嵌入提供“关注对象的结构先验”，双向建模确保“前后文完整覆盖”。三者共同作用，使 TM-Mamba 在 BABEL-Grounding 数据集上以线性内存增长的特性超越了经典 Transformer——后者在序列长度达到 1200 帧时即发生 GPU 内存溢出（Fig. 8），而 TM-Mamba 的内存消耗保持线性增长，展现出处理超长未修剪运动序列的根本性优势。

## 整体框架

TM-Mamba 的整体流程遵循“文本嵌入 → 运动编码 → 拓扑增强 → 文本控制全局上下文提取 → 逐帧激活预测”的串行结构，如 **Figure 7** 左图所示。其核心设计目标是以线性内存成本同时捕获长序列的全局时间依赖、文本查询的语义控制以及人体骨架的空间拓扑。

![[assets/figures/papers/paper_list_l66_https_arxiv_org_abs_2404_11375/figures/007_Figure_7.jpg]]
*Figure 7: Left: overall architecture of our proposed model. Right: Illustration of TM-Mamba block. ‘Bidirectional SSM’ refers to the textcontrolled selection mechanism demonstrated in Algorithm 2 with bidirectional modeling. Text embedding q denotes the CLIP embedding of the input text query*

**输入与嵌入阶段。** 模型接收两个输入：一段未修剪的人体运动骨架序列（长度 L，关节点数 V）和一个自由形式的文本查询。文本查询通过冻结的 CLIP 文本编码器提取为固定维度的嵌入向量 **q**，作为后续所有文本控制操作的全局条件信号。运动序列首先经过一个线性嵌入层，将原始骨架坐标映射为初始运动特征 **X** ∈ R^{V×L×D}，其中 D 为特征维度。

**拓扑感知的关系嵌入。** 为了显式注入人体骨架的图拓扑信息，模型引入关系嵌入模块。该模块以自适应图卷积网络（AGCN）实现，以运动特征 **X** 为输入，计算图关系嵌入 **R** = f(**X**)。**R** 编码了各关节点之间的空间依赖关系，随后与原始运动特征沿特征维度拼接，形成拓扑增强的运动表示。这一设计弥补了原生 Mamba 处理单变量序列时缺乏关节拓扑建模的不足。

**文本控制选择性状态空间模型（核心模块）。** 拼接后的特征被送入 TM-Mamba 块，这是整个框架的核心计算单元（**Figure 7** 右图）。每个 TM-Mamba 块内部执行文本控制的选择性状态空间模型（SSM），其关键创新在于：Mamba 原有的输入依赖选择机制被扩展为文本条件选择——状态转移矩阵的参数 **Δ**、**B**、**C** 同时依赖于运动输入和文本查询嵌入 **q**。这使得模型能够根据文本查询的内容，自适应地选择在长序列中传播哪些信息、抑制哪些信息，从而实现“文本指导的全局上下文聚焦”。此外，模型采用双向非因果结构（借鉴 Vision Mamba），使每一帧的表示既能感知前向历史，也能感知后向未来，显著提升了时间定位的精度。

**输出与损失函数。** 经过多层 TM-Mamba 块处理后，模型对关节维度执行平均池化，将特征压缩为逐帧的标量表示，再通过一个 MLP 层生成每一帧的激活分数 s_t ∈ [0, 1]。训练目标为逐帧的二元交叉熵损失：

$$\mathcal{L}_{ce} = -\frac{1}{T}\sum_{t}^{T}(y_t \log s_t + (1-y_t)\log(1-s_t))$$

其中 y_t 为真实标签，指示第 t 帧是否属于文本查询对应的目标时间片段。

**模块间关系总结。** 文本嵌入 **q** 作为全局条件信号贯穿整个 TM-Mamba 块的计算；关系嵌入 **R** 在 SSM 之前注入，为状态空间提供骨架拓扑先验；双向 SSM 以线性复杂度完成长序列的全局上下文提取；最终 MLP 将全局上下文解码为帧级定位决策。整个 pipeline 的内存消耗随序列长度线性增长，在 1200 帧时经典 Transformer 已发生 GPU 内存溢出，而 TM-Mamba 仍可正常训练（**Figure 8**）。

### 补充图表

![[assets/figures/papers/paper_list_l66_https_arxiv_org_abs_2404_11375/figures/003_Figure_3.jpg]]
*Figure 3: An illustration of the data augmentation pipeline, highlighting the differences between the original BABEL annotations and the BABEL-Grounding annotations*

## 核心模块与公式推导

### 状态空间模型基础

TM-Mamba 的核心计算单元建立在选择性状态空间模型（Selective SSM）之上。连续时间下的 SSM 将一维输入信号 $x(t) \in \mathbb{R}$ 通过隐状态 $h(t) \in \mathbb{R}^N$ 映射到输出 $y(t) \in \mathbb{R}$：

$$h'(t) = \mathbf{A} h(t) + \mathbf{B} x(t), \quad y(t) = \mathbf{C} h(t)$$

其中 $\mathbf{A} \in \mathbb{R}^{N \times N}$ 为状态转移矩阵，$\mathbf{B} \in \mathbb{R}^{N \times 1}$ 和 $\mathbf{C} \in \mathbb{R}^{1 \times N}$ 分别为输入和输出投影矩阵。

为适配离散序列处理，使用零阶保持（ZOH）方法进行离散化，引入时间尺度参数 $\Delta$：

$$\overline{\mathbf{A}} = \exp(\Delta \mathbf{A}), \quad \overline{\mathbf{B}} = (\Delta \mathbf{A})^{-1} (\exp(\Delta \mathbf{A}) - \mathbf{I}) \cdot \Delta \mathbf{B}$$

离散化后的递归计算形式为：

$$h_t = \overline{\mathbf{A}} h_{t-1} + \overline{\mathbf{B}} x_t, \quad y_t = \mathbf{C} h_t$$

为支持高效并行训练，SSM 可转化为全局卷积形式，其卷积核 $\overline{\mathbf{K}} \in \mathbb{R}^L$ 为：

$$\overline{\mathbf{K}} = (\mathbf{C} \overline{\mathbf{B}}, \mathbf{C} \overline{\mathbf{A} \mathbf{B}}, \dots, \mathbf{C} \overline{\mathbf{A}}^{L-1} \overline{\mathbf{B}})$$

Mamba 的关键创新在于将 $\mathbf{A}$、$\mathbf{B}$、$\mathbf{C}$、$\Delta$ 全部参数化为输入 $\mathbf{X}$ 的函数，实现了**输入依赖的选择机制**，使模型能够根据输入内容动态决定信息的保留与丢弃。

### 文本控制选择机制

TM-Mamba 的核心突破在于将 Mamba 的选择机制从“仅依赖输入”扩展为“同时依赖输入与文本查询”。具体而言，离散化参数 $\Delta$ 以及投影矩阵 $\mathbf{B}$、$\mathbf{C}$ 均被参数化为运动输入 $\mathbf{X}$ 和文本查询嵌入 $\mathbf{q}$ 的联合函数：

$$\Delta, \mathbf{B}, \mathbf{C} = f(\mathbf{X}, \mathbf{q})$$

其中文本嵌入 $\mathbf{q}$ 由冻结的 **CLIP 文本编码器** 提取。这一设计的因果逻辑在于：文本查询作为“条件信号”直接参与状态转移矩阵的生成，使得模型能够根据文本语义自适应地聚焦于运动序列中的相关局部区域，而非对所有时间步一视同仁。

消融实验（TABLE II）提供了决定性证据：移除文本控制选择机制后，双向模型的 mAP@Avg 从 41.6 降至 39.2，验证了文本条件注入对定位精度的关键贡献。

### 关系嵌入与骨架拓扑建模

人体运动序列天然具有图结构——骨架关节点之间存在物理连接关系。为注入这一拓扑先验，TM-Mamba 引入了**关系嵌入**模块。该模块采用自适应图卷积网络（AGCN）对输入运动特征 $\mathbf{X} \in \mathbb{R}^{V \times L \times D}$ 建模，计算关系嵌入 $\mathbf{R} = f_{\text{AGCN}}(\mathbf{X})$，其中 $V$ 为关节点数，$L$ 为序列长度，$D$ 为特征维度。

关系嵌入 $\mathbf{R}$ 与原始运动特征拼接后送入文本控制选择性 SSM 块。消融实验表明，加入关系嵌入后 mAP@Avg 从 39.2 提升至 41.6（TABLE II），证实了骨架拓扑信息对时间定位的增益。

### 双向非因果结构

原始 Mamba 采用单向因果建模，仅允许信息从过去流向未来。TM-Mamba 借鉴 Vision Mamba 的方案，采用**双向非因果结构**：分别沿正向和反向扫描序列，将两个方向的输出融合。这一设计使每一帧能够同时感知前后文信息，对于需要全局上下文的时间定位任务至关重要。

消融实验（TABLE II）显示，在均含文本控制的前提下，双向结构（mAP@Avg 39.2）相比单向结构（mAP@Avg 30.7）提升达 8.5 个百分点，效果极为显著。

### 帧激活与训练目标

经过多个 TM-Mamba 块处理后，模型对关节维度做平均池化，得到逐帧表示，再通过 MLP 生成标量激活分数 $s_t \in [0, 1]$，表示第 $t$ 帧属于文本查询对应时间段的概率。

训练采用标准的帧级二元交叉熵损失：

$$\mathcal{L}_{ce} = -\frac{1}{T}\sum_{t}^{T}(y_t \log s_t + (1-y_t)\log(1-s_t))$$

其中 $y_t \in \{0, 1\}$ 为真实标签，$T$ 为序列总帧数。该损失直接监督每一帧的归属判断，驱动模型学习精确的时间边界定位。

## 实验与分析

### 核心实验设置

TM-Mamba 的训练与评估均基于作者从 BABEL 数据集重构的 **BABEL-Grounding** 数据集。该数据集包含 5,339 个运动序列，总计 21,307 条文本-时间片段标注，平均序列长度为 743 帧，真实时间片段平均跨度为 112 帧（Fig. 2）。所有实验在相同 GPU 硬件上运行，采用 AdamW 优化器与统一的训练超参数，评估指标为标准的时间定位 mAP@IoU，阈值从 0.1 到 0.7 共 7 个档位，以 mAP@Avg 作为综合性能指标。

![[assets/figures/papers/paper_list_l66_https_arxiv_org_abs_2404_11375/figures/002_Figure_2.jpg]]
*Figure 2: Dataset statistics of BABEL-Grounding. ‘Frame Number’ refers to the length of motion sequences. ‘Text Query Length’ denotes the length of textual annotations in the data. ‘Grounded Length Ratio’ indicates the ratio of the length of temporal segments corresponding to each text query to the total length of the sequence. ‘Segment Counts per Query’ refers to the number of temporal segments corresponding to each text query*

### 主实验结果

#### 与基线方法的全面对比

TABLE III 给出了 TM-Mamba 与多种基线方法在 BABEL-Grounding 上的性能对比。TM-Mamba 在所有 IoU 阈值下均取得最优结果，mAP@Avg 达到 41.6，显著超越基于 LSTM 的方法和经典 Transformer 架构。

#### 长序列下的效率与精度优势

TABLE IV 展示了不同最大序列长度下 TM-Mamba 与 Temporal Transformer 的性能对比。在序列长度 500 帧时，TM-Mamba 的 mAP@IoU=0.1 达到 53.9，较 Transformer 的 50.5 提升 +3.4 个百分点。更关键的是，**经典 Transformer 在序列长度达到 1200 帧时发生 GPU 内存溢出（OOM）**，而 TM-Mamba 的内存消耗呈线性增长（Fig. 8），展现出在长未修剪运动序列上的根本性效率优势。基于 Flash-Attention-2 的高效 Transformer 虽能缓解内存压力，但仍无法完全避免长序列下的性能退化。

![[assets/figures/papers/paper_list_l66_https_arxiv_org_abs_2404_11375/figures/010_Figure_8.jpg]]
*Figure 8: Comparison of memory consumption for TM-Mamba and its LSTM, classic Transformer and Flash-attention-2-based (FA2) Transformer counterparts under varying motion sequence lengths. The classic Transformer runs out of GPU memory when the sequence length reaches 1200*

### 消融实验

TABLE II 系统性地拆解了 TM-Mamba 各核心组件的贡献，揭示了以下因果链条：

**文本控制选择机制是性能的核心支柱。** 在双向建模配置下，移除文本控制选择机制后，mAP@Avg 从 41.6 骤降至 39.2（降幅 2.4 个百分点），验证了文本查询对状态空间信息传播进行动态调控的必要性。这一机制使得模型能够根据文本语义自适应地聚焦于运动序列的相关局部，而非被动地平等对待所有时间步。

**关系嵌入提供拓扑感知的增益。** 在文本控制选择的基础上，引入通过自适应图卷积网络（AGCN）计算的关系嵌入 R，将 mAP@Avg 从 39.2 进一步提升至 41.6（+2.4 个百分点）。这表明注入人体骨架的图拓扑信息能够有效增强状态空间模型对关节间空间依赖的建模能力。

**双向非因果结构是长序列建模的关键。** 在均包含文本控制选择机制的前提下，单向因果建模的 mAP@Avg 仅为 30.7，而双向非因果结构达到 39.2（+8.5 个百分点）。这一巨大差距说明，对于时间定位任务而言，未来帧的上下文信息对准确判断当前帧是否属于目标片段至关重要，原始 Mamba 的单向因果约束在此任务上构成了严重的性能瓶颈。

**模型深度存在饱和点。** TABLE V 显示，TM-Mamba 块数从 1 增至 2 时，mAP@Avg 从 36.1 跃升至 40.9；增至 3 块时达到最优 41.6，但提升幅度已明显收窄。当块数增至 4 时，GPU 内存溢出，表明在计算资源约束下，3 块 TM-Mamba 是性能与效率的最佳平衡点。

### 可视化分析

Fig. 9 展示了不同消融模型在单个序列上的逐帧激活分数预测。完整模型的预测曲线（红色实线）与真实时间片段（灰色条形）高度吻合，而移除文本控制的模型（蓝色虚线）和移除关系嵌入的模型（灰色虚线）在边界处出现明显的激活偏移和误激活，直观验证了各组件对精确定位边界的贡献。

![[assets/figures/papers/paper_list_l66_https_arxiv_org_abs_2404_11375/figures/011_Figure_9.jpg]]
*Figure 9: Visualizations of predicted frame activation score. The solid red line denotes the predicted score of our full model, while the dashed blue and gray lines denote the model without text control and relational embeddings, respectively. The gray bars below illustrate the ground-truth temporal segments. Best viewed in color*

Fig. 10 进一步对比了完整模型与消融模型在多个文本查询下的定位结果。TM-Mamba 在检索到的片段数量和每个片段时间边界精度上均显著优于消融版本，尤其在处理一个文本查询对应多个不连续时间片段的复杂场景时优势更为突出。

![[assets/figures/papers/paper_list_l66_https_arxiv_org_abs_2404_11375/figures/012_Figure_10.jpg]]
*Figure 10: Visualizations of the grounding results of TM-Mamba compared to ablative models. ‘GT’ denotes ground-truth temporal segments corresponding to the text query. Our TM-Mamba demonstrates superior performance in motion grounding, in terms of the number of retrieved segments and the temporal boundaries of each segment. Best viewed in color*

### 失败模式与局限性

尽管 TM-Mamba 在 BABEL-Grounding 上取得了最优性能，论文中未明确报告具体的失败案例或错误模式。从消融实验可推断，当文本查询语义模糊或与运动内容存在弱关联时，文本控制选择机制可能难以精确界定时间边界——Fig. 9 中移除文本控制的模型在非目标区域出现激活波动即暗示了这一潜在脆弱性。此外，模型在 4 块 TM-Mamba 时即发生 OOM，表明其扩展性仍受限于当前 GPU 显存容量，对于超过 2000 帧的超长序列可能需要额外的序列分块策略。这些推断需要进一步实验验证。

### 补充图表

![[assets/figures/papers/paper_list_l66_https_arxiv_org_abs_2404_11375/figures/008_Table.jpg]]
*Table: II ABLATION STUDIES ON BABEL-GROUNDING DATASET. THE BEST RESULTS ARE IN BOLD*

![[assets/figures/papers/paper_list_l66_https_arxiv_org_abs_2404_11375/figures/009_Table.jpg]]
*Table: III PERFORMANCE COMPARISONS TO BASELINE METHODS ON BABEL-GROUNDING DATASET. THE BEST RESULTS ARE IN BOLD. TABLE IV PERFORMANCE COMPARISON OF TM-MAMBA AND ITS TEMPORAL TRANSFORMER COUNTERPART UNDER DIFFERENT MAXIMUM SEQUENCE LENGTH*

![[assets/figures/papers/paper_list_l66_https_arxiv_org_abs_2404_11375/figures/013_Figure_11.jpg]]
*Figure 11: Visualizations of the grounding results of TM-Mamba compared to baseline models. ‘GT’ denotes ground-truth temporal segments corresponding to the text query. Best viewed in color*

![[assets/figures/papers/paper_list_l66_https_arxiv_org_abs_2404_11375/figures/014_Table.jpg]]
*Table: V IMPACT OF THE NUMBER OF TM-MAMBA BLOCKS ON THE GROUNDING PERFORMANCE. GPU MEMORY OVERFLOW OCCURRED WITH 4 BLOCKS*

## 方法谱系与知识库定位

### 一、与基线方法的关系

TM-Mamba 的核心定位是解决经典 Transformer 在**长序列文本驱动人体运动时间定位（THMG）**中面临的二次计算瓶颈。其方法谱系可从三条基线对比路径来理解：

**1. 与经典 Transformer 的对比：线性 vs 二次复杂度**
经典 Transformer 依赖全局时间自注意力捕获长程依赖，但计算成本随序列长度 $L$ 呈 $O(L^2)$ 增长。在 BABEL-Grounding 数据集上，当最大序列长度设为 500 帧时，TM-Mamba 的 mAP@IoU=0.1 达到 **53.9**，优于 Temporal Transformer 的 **50.5**（Table IV）。更关键的是，当序列长度扩展至 1200 帧时，经典 Transformer 直接触发 GPU 内存溢出（OOM），而 TM-Mamba 的内存消耗呈**线性增长**（Fig. 8）。即使采用 Flash-Attention-2 优化的 Transformer（FA2），其内存增长趋势仍明显高于 TM-Mamba，表明 Mamba 架构的选择性状态空间机制在长序列场景下具有根本性的效率优势。

**2. 与 LSTM 的对比：长程记忆能力的代际差异**
LSTM 作为时间序列建模的经典基线，在长序列上面临梯度消失和有限记忆容量的固有问题。Fig. 8 的内存对比曲线表明，LSTM 虽未出现 OOM，但其建模能力受限于隐状态的固定容量。TM-Mamba 通过输入依赖的选择机制动态决定信息保留与丢弃，本质上突破了 LSTM 的固定记忆瓶颈。

**3. 与原始 Mamba 的对比：从输入依赖到文本条件依赖**
原始 Mamba 的选择机制参数 $\mathbf{A}, \mathbf{B}, \mathbf{C}, \Delta$ 仅依赖于输入 $\mathbf{X}$，适用于单模态序列建模。TM-Mamba 的核心改造在于将这些参数同时参数化为运动输入 $\mathbf{X}$ 和文本查询嵌入 $\mathbf{q}$ 的函数，使文本能够**动态控制**长序列中的信息传播（Algorithm 2）。消融实验直接验证了这一改造的必要性：移除文本控制后，双向模型的 mAP@Avg 从 **41.6** 降至 **39.2**（TABLE II），表明文本条件选择是性能的关键支撑。

### 二、适用边界与技术约束

TM-Mamba 的设计隐含以下适用边界，需在知识库中明确标注：

**1. 序列长度的上限**
尽管 TM-Mamba 展现了线性内存优势，但消融实验显示，当 TM-Mamba 块数增至 4 时仍会发生 GPU 内存溢出（TABLE V）。这意味着在极端长序列（如超过 2000 帧）场景下，即使线性复杂度模型也可能需要额外的序列分块或梯度检查点策略。论文未给出 TM-Mamba 的绝对最大序列长度上限，这一边界需要在实际部署中根据 GPU 显存进行验证。

**2. 文本编码器的选择依赖性**
TM-Mamba 采用冻结的 CLIP 文本编码器提取查询嵌入 $\mathbf{q}$。CLIP 的对齐空间偏向于视觉-语言联合表示，其在纯文本运动描述上的语义细粒度是否充分，论文未进行对比实验。若替换为 BERT、T5 等纯文本编码器，或对 CLIP 进行微调，定位精度可能发生变化——这是一个开放问题。

**3. 骨架拓扑建模的通用性**
关系嵌入通过自适应图卷积网络（AGCN）捕获人体骨架的图拓扑信息。这一设计假设输入为结构化的人体骨架序列，其泛化到非人体运动数据（如通用时间序列、视频帧序列）时，AGCN 模块需要重新设计或替换。

### 三、局限与开放问题

论文未在正文中明确列出局限性，但从实验设计和架构选择中可以推断以下潜在局限和待探索方向：

**1. 文本控制选择机制的可解释性**
虽然消融实验定量证明了文本控制的有效性，但该机制如何具体影响状态转移矩阵 $\overline{\mathbf{A}}$ 和全局卷积核 $\overline{\mathbf{K}}$ 的信息选择行为，论文未提供深入的可视化或归因分析。Fig. 9 的帧激活分数对比仅展示了最终输出层面的差异，而非选择机制的内部运作。

**2. 多段定位的边界精度**
BABEL-Grounding 数据集中每个文本查询可能对应多个时间片段（Fig. 2 的 Segment Counts per Query 分布）。TM-Mamba 通过逐帧激活分数 $s_t$ 进行定位，其多段检索能力依赖于激活分数的峰值检测。Fig. 10 的可视化显示，消融模型在片段数量和边界精度上均存在退化，但完整模型在边界模糊或片段密集场景下的失效模式未被系统分析。

**3. 跨模态扩展的可行性**
论文提出 TM-Mamba 统一了时间全局上下文、语言查询控制和空间图拓扑，这一框架理论上可扩展到视频模态（RGB 视频 + 3D 运动联合定位）。但视频的视觉特征与骨架运动特征在时序粒度、噪声特性和语义抽象层级上存在差异，直接迁移需要验证。

**4. 多人体与遮挡场景的泛化能力**
BABEL-Grounding 基于 BABEL 数据集构建，后者主要包含单人运动捕捉序列。在多人交互、部分遮挡或视角变化的真实场景中，骨架提取的噪声和拓扑变化可能影响 AGCN 的关系嵌入质量，进而影响定位精度。这一泛化边界尚未被验证。

### 四、知识库定位总结

TM-Mamba 在方法谱系中属于**文本驱动的长序列时间定位模型**，其核心贡献在于将 Mamba 的选择性状态空间模型从单模态输入依赖扩展为跨模态文本条件依赖，同时引入图拓扑感知的关系嵌入。相较于 Transformer 基线，其在长序列上的线性内存优势是确定的（由 Fig. 8 的 OOM 对比直接证实）；相较于原始 Mamba，文本控制选择机制的增益由消融实验定量支撑（mAP@Avg +2.4）。该方法适用于需要高效处理长序列、且具备明确文本查询的跨模态时间定位任务，但在极端序列长度、文本编码器选择、非人体运动数据和复杂真实场景下的表现仍需进一步验证。

## 原文 PDF

![[paperPDFs/arxiv_2025/TM_Mamba_Text_controlled_Motion_Mamba_Text_Instructed_Temporal_Grounding_of_Human_Motion.pdf]]