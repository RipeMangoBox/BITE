---
title: "PST Beyond Global Alignment: Fine-Grained Motion-Language Retrieval via Pyramidal Shapley-Taylor Learning"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval_via_Pyramidal_Shapley_Taylor_Learning.pdf
aliases:
- PSTPLF
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 引入金字塔式的细粒度对齐策略，并采用Shapley-Taylor交互（STI）度量来量化不同上下文下运动-语言元素对的交互强度，以此引导模型学习从关节级到片段级再到整体级的层次化对应关系。
primary_logic: 受人类运动感知的金字塔过程启发（从关节动态到片段连贯性再到整体理解），结合Shapley-Taylor交互指数，在逐级对齐过程中量化成对跨模态特征在上下文递增时的边际贡献，使得模型能够突出关键的细粒度运动-语言对应，从而显著提升检索精度。
claims:
- 在HumanML3D的Small batch协议下，文本到运动检索的R@1达到71.61，显著超过之前的强基线TMR（67.45）。
- 在KIT-ML的Small batch协议下，文本到运动检索的R@1为56.83，比MotionPatch的53.55提高了3.28。
- 关节级和片段级的对齐可视化（图3、图4）清晰地展示了模型成功捕获了运动关节与文本词语之间的细粒度语义关联。
- 消融实验表明，去掉自蒸馏损失（L_D）或STI蒸馏损失（L_SD）均会导致检索准确率明显下降，验证了分层对齐与交互建模的必要性。
---

# PST Beyond Global Alignment: Fine-Grained Motion-Language Retrieval via Pyramidal Shapley-Taylor Learning

> [!tip] 核心洞察
> 受人类运动感知的金字塔过程启发（从关节动态到片段连贯性再到整体理解），结合Shapley-Taylor交互指数，在逐级对齐过程中量化成对跨模态特征在上下文递增时的边际贡献，使得模型能够突出关键的细粒度运动-语言对应，从而显著提升检索精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 超越全局对齐：基于金字塔Shapley-Taylor学习的细粒度运动-语言检索 |
| 英文题名 | PST Beyond Global Alignment: Fine-Grained Motion-Language Retrieval via Pyramidal Shapley-Taylor Learning |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2405.04771) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Pyramidal Shapley-Taylor (PST) Learning Framework |
| Dataset | HumanML3D, KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R@1 (text-to-motion, Small batches) 71.61 vs 67.45 (TMR) (+4.16)。
> - KIT-ML 上，R@1 (text-to-motion, Small batches) 56.83 vs 53.55 (MotionPatch) (+3.28)。

## 概述

### 核心问题：全局对齐的瓶颈

现有运动-语言检索方法普遍采用**全局序列对齐**策略，将整段运动与整句文本映射到共享空间后直接计算余弦相似度。这一范式忽略了运动内部的层次化结构——人体运动天然由关节动态、时序片段和整体语义构成，而文本描述也包含词语、短语和句子级别的信息。全局对齐无法捕获这些**细粒度对应关系**，导致模型难以区分语义相近但局部细节不同的运动-文本对，成为检索性能提升的关键瓶颈。

### 核心方法：金字塔式Shapley-Taylor学习框架

本文提出**Pyramidal Shapley-Taylor (PST) 学习框架**，核心思路是模拟人类运动感知的金字塔过程——从关节动态到片段连贯性再到整体理解——构建层次化的跨模态对齐机制。框架包含两个关键创新：

1. **Shapley-Taylor交互 (STI) 度量**：引入合作博弈论中的Shapley-Taylor交互指数，量化不同上下文下运动-语言元素对的**边际贡献**。对于任意一对运动token和文本token，STI值反映其在所有可能token排列上的期望交互强度，暗色表示强语义关联，浅色表示弱关联。这一度量通过STI估计头进行蒸馏学习，为模型提供明确的成对交互监督信号。

2. **金字塔式三级对齐**：将对齐过程分解为**关节级→片段级→整体级**三个层次。关节级对齐在单个身体关节与文本词语之间建立对应；片段级对齐通过Token Compressor（基于卷积、自注意力和KNN-DPC）压缩token后捕获中尺度语义；整体级对齐聚合全局表示实现高层语义匹配。三级对齐之间通过**自蒸馏损失**保持跨粒度的一致性。

### 主要结果

在公开基准上的实验表明，PST框架显著超越现有方法：

- **HumanML3D数据集**（Small batch协议）：文本到运动检索R@1达到**71.61**，较此前最优方法TMR（67.45）提升**+4.16**。
- **KIT-ML数据集**（Small batch协议）：文本到运动检索R@1达到**56.83**，较MotionPatch（53.55）提升**+3.28**。

消融实验证实，移除STI蒸馏损失或自蒸馏损失均导致检索准确率明显下降，验证了分层对齐与交互建模的必要性。关节级和片段级的对齐可视化清晰展示了模型成功捕获运动关节与文本词语之间的细粒度语义关联。

### 方法谱系与知识库定位

PST框架处于**运动-语言跨模态检索**方向，在以下维度上区别于现有工作：

| 维度 | 已有方法 | PST框架 |
|------|---------|---------|
| 对齐粒度 | 全局序列对齐（**TMR**, Petrovich et al., ICCV 2023；**MotionPatch**, Yu et al., CVPR 2024） | 金字塔式关节级、片段级、整体级细粒度对齐 |
| 跨模态交互度量 | 全局余弦相似度 | 基于STI的成对边际贡献度量 |
| 特征压缩 | 无（直接使用编码器输出） | 卷积+自注意力+KNN-DPC的Token Compressor |
| 训练信号一致性 | 仅全局对比损失 | 关节级到片段级的KL自蒸馏损失 |

PST框架的STI度量源自合作博弈论，为跨模态检索引入了一种可解释的成对交互量化工具。金字塔式对齐策略则与多尺度视觉-语言模型的设计理念相呼应，但在运动模态上首次实现了从关节到整体的完整层次化对应。

## 背景与动机

### 运动-语言跨模态检索的现状与瓶颈

人体运动与自然语言之间的跨模态检索旨在根据文本描述查找最匹配的运动序列，或反之。近年来，基于对比学习的全局对齐方法在这一领域取得了显著进展，代表性工作包括 **TEMOS**（Petrovich et al., ECCV 2022）、**T2M**（Guo et al., CVPR 2022）、**TMR**（Petrovich et al., ICCV 2023）以及 **MotionPatch**（Yu et al., CVPR 2024）。这些方法通常将完整的运动序列和文本描述分别编码为单一的全局特征向量，并通过余弦相似度进行匹配。

然而，这种全局对齐范式存在一个根本性瓶颈：**它忽略了运动序列内部丰富的时空结构与文本标记之间的细粒度对应关系**。具体而言，一段运动由多个时间片段和空间身体关节的动态变化构成，而文本描述则包含对局部动作、身体部位和时序细节的精确刻画。全局对齐将所有这些细节压缩为一个整体表示，导致模型无法捕获诸如“先慢跑再停下摆出侧身格斗姿势”这类涉及多阶段、多关节协调的精确语义，从而限制了检索性能的上限。

### 人类运动感知的启示

人类对运动的感知天然遵循一种**金字塔式的层次化过程**：从底层关节的动态变化，到中层运动片段的连贯性，再到高层对整体动作的语义理解。这种由细到粗、逐级聚合的感知机制，使得人类能够同时把握运动的局部细节与全局语义。然而，现有的运动-语言检索方法并未显式建模这一层次化过程，缺乏在关节级、片段级和整体级之间建立结构化对齐的能力。

### 核心动机：从全局对齐走向细粒度层次化对齐

基于上述观察，本文的核心动机在于**填补全局对齐与细粒度语义理解之间的鸿沟**。具体目标包括：

1. **建立多粒度的对齐机制**：在关节、片段和整体三个层次上分别建立运动与语言之间的对应关系，使模型能够同时捕获从微观到宏观的跨模态语义关联。
2. **量化跨模态交互强度**：引入一种能够度量运动-语言元素对在不同上下文下交互强度的机制，从而识别出真正关键的细粒度对应，而非依赖简单的全局相似度。
3. **保持跨粒度一致性**：确保不同粒度级别的对齐结果在语义上相互一致，避免关节级的细粒度匹配与整体级的高层语义产生冲突。

这些动机直接催生了本文提出的**金字塔Shapley-Taylor（PST）学习框架**，该框架通过Shapley-Taylor交互度量来量化成对跨模态特征的边际贡献，并以金字塔式的层级结构实现从关节到整体的逐步对齐，从而显著提升细粒度运动-语言检索的精度。

## 核心创新

现有运动-语言检索方法普遍采用全局序列对齐策略，将整段运动与整句文本映射到共享空间后直接计算余弦相似度。这一范式忽略了运动内部的层次化结构——从关节级动态到片段级连贯性再到整体语义——以及文本中词语与具体身体部位之间的细粒度对应关系，导致模型难以捕获精确的语义细节，在复杂动作描述上检索性能受限。

PST框架的核心创新在于引入**金字塔式细粒度对齐**与**Shapley-Taylor交互（STI）度量**相结合的层次化学习范式，从三个关键维度突破了全局对齐的瓶颈。

**对齐粒度的层次化升级。** 与现有方法的全局序列对齐不同，PST将运动-语言对齐分解为关节级、片段级和整体级三个层次（Sec. 3.3）。关节级对齐在单个运动关节token与文本词token之间建立最细粒度的语义对应；片段级对齐通过Token Compressor将token压缩为运动片段与文本短语的中尺度表示后进行匹配；整体级对齐则聚合全局特征提供高层语义约束。这种金字塔结构模拟了人类运动感知从局部关节动态到整体动作理解的渐进过程。

**跨模态交互度量的根本性改变。** 全局对齐方法仅依赖余弦相似度衡量整体匹配程度，无法量化特定运动-语言元素对在不同上下文中的交互强度。PST引入Shapley-Taylor交互指数（k=2），通过计算一对运动token与文本token在所有可能上下文排列上的期望边际贡献，精确量化其交互强度（Eq. 2）：

$$\phi ( e _ { i } ^ { \mathrm { t } } , e _ { j } ^ { \mathrm { m } } ) = \mathbb { E } _ { \boldsymbol \pi } \Big [ F ( S _ { \boldsymbol \pi } \cup \{ e _ { i } ^ { \mathrm { t } } , e _ { j } ^ { \mathrm { m } } \} ) - F ( S _ { \boldsymbol \pi } \cup \{ e _ { i } ^ { \mathrm { t } } \} ) - F ( S _ { \boldsymbol \pi } \cup \{ e _ { j } ^ { \mathrm { m } } \} ) + F ( S _ { \boldsymbol \pi } ) \Big ]$$

这一度量使得模型能够识别出真正关键的细粒度对应关系（如“jump”与腿部关节、“wave”与手部关节），而非将所有元素对等对待。

**训练信号一致性约束的引入。** 现有方法仅依赖各阶段独立的对比损失进行训练，缺乏跨粒度的语义一致性保障。PST设计了两个蒸馏损失：STI蒸馏损失 $\mathcal{L}_{\mathrm{SD}}$ 使STI估计头 $\mathcal{H}$ 输出的交互分布逼近标准STI分布（Eq. 6），自蒸馏损失 $\mathcal{L}_{\mathrm{D}}$ 通过KL散度让片段级相似度分布模仿关节级分布（Eq. 9），确保压缩过程中不丢失关键的细粒度对齐信息。消融实验表明，移除任一损失均导致检索准确率明显下降（Table 3, Table 4），验证了层次化对齐与交互建模的必要性。

**特征压缩机制的结构化设计。** 区别于直接使用编码器输出的做法，PST在关节级到片段级过渡时引入基于卷积、自注意力和KNN-DPC的Token Compressor（Fig. 6(b)），以压缩比 $\rho = 0.25$ 在保留关键细节的同时整合上下文信息，为片段级对齐提供紧凑且语义丰富的表示。

上述创新共同构成了PST框架的核心技术路径：通过STI量化细粒度交互强度，在金字塔式对齐过程中逐级突出关键的运动-语言对应，并以蒸馏损失保持跨粒度的语义一致性，最终实现从关节到整体的精确检索。

## 整体框架

PST 学习框架的核心设计动机源于一个观察：现有运动-语言检索方法（如 **TMR** (Petrovich et al., ICCV 2023)、**MotionPatch** (Yu et al., CVPR 2024)）主要依赖全局序列对齐，忽略了运动内部从局部关节到整体动作的层次化语义结构，导致模型难以捕获精确的细粒度对应关系。PST 框架通过引入金字塔式对齐策略与 Shapley-Taylor 交互（STI）度量，构建了一个从细粒度到粗粒度的层次化跨模态检索流水线。

### 框架总览

整体流水线由三个核心模块串联构成：**特征编码**、**金字塔对齐**与**训练信号蒸馏**。输入的运动序列首先通过基于 ViT 的 Motion Encoder 编码为运动 token，文本描述则通过 DistilBERT 编码为文本 token。随后，这些 token 进入金字塔对齐阶段，依次经历关节级（joint-wise）、片段级（segment-wise）和整体级（holistic）三个粒度的对齐。在相邻粒度之间，Token Compressor 负责压缩 token 数量并整合上下文信息。整个训练过程由对比损失、STI 蒸馏损失和自蒸馏损失联合驱动。

### 核心机制：Shapley-Taylor 交互度量

框架的关键创新在于将 STI（k=2）引入跨模态对齐。对于任意一对运动 token $e_j^{\mathrm{m}}$ 和文本 token $e_i^{\mathrm{t}}$，其 STI 值 $\phi(e_i^{\mathrm{t}}, e_j^{\mathrm{m}})$ 量化了该 token 对在所有上下文排列上的期望边际贡献：

$$\phi ( e _ { i } ^ { \mathrm { t } } , e _ { j } ^ { \mathrm { m } } ) = \mathbb { E } _ { \boldsymbol \pi } \Big [ F ( S _ { \boldsymbol \pi } \cup \{ e _ { i } ^ { \mathrm { t } } , e _ { j } ^ { \mathrm { m } } \} ) - F ( S _ { \boldsymbol \pi } \cup \{ e _ { i } ^ { \mathrm { t } } \} ) - F ( S _ { \boldsymbol \pi } \cup \{ e _ { j } ^ { \mathrm { m } } \} ) + F ( S _ { \boldsymbol \pi } ) \Big ]$$

这一度量能够显式反映成对跨模态特征在不同上下文中的交互强度，为后续的细粒度对齐提供了可量化的学习目标。由于精确计算 STI 的计算代价极高，框架引入了一个轻量级的 STI Estimation Head（由卷积和自注意力构成，详见 Figure 6(a)），通过 STI 蒸馏损失 $\mathcal{L}_{\mathrm{SD}}$ 逼近标准 STI 分布。

### 金字塔对齐流水线

金字塔对齐分为三个递进阶段：

1. **关节级对齐**：在最细粒度层面，计算每个单词 token 与每个关节 token 之间的交互，捕获最底层的语义关联。
2. **片段级对齐**：通过 Token Compressor（由卷积、自注意力和 KNN-DPC 聚类算法组成，详见 Figure 6(b)）将关节级 token 压缩为片段/短语级表示（压缩比 $\rho=0.25$），在此粒度上进行中尺度语义对齐。
3. **整体级对齐**：将片段级嵌入聚合为全局表示，提供高层语义对应。

### 训练信号与损失函数

框架的总损失函数整合了三个粒度的对比损失、两个阶段的 STI 蒸馏损失以及跨粒度的自蒸馏损失：

$$\mathcal { L } = \mathcal { L } _ { \mathrm { C } } ^ { \mathrm { j n t } } + \mathcal { L } _ { \mathrm { C } } ^ { \mathrm { s g m } } + \mathcal { L } _ { \mathrm { C } } ^ { \mathrm { h l t } } + \lambda _ { \mathrm { S } } ( \mathcal { L } _ { \mathrm { S D } } ^ { \mathrm { j n t } } + \mathcal { L } _ { \mathrm { S D } } ^ { \mathrm { s g m } } ) + \lambda _ { \mathrm { D } } \mathcal { L } _ { \mathrm { D } }$$

其中，$\mathcal{L}_{\mathrm{C}}$ 为各阶段的 InfoNCE 对比损失，$\mathcal{L}_{\mathrm{SD}}$ 为 STI 蒸馏损失（通过 KL 散度使估计头输出逼近标准 STI 分布），$\mathcal{L}_{\mathrm{D}}$ 为自蒸馏损失——通过 KL 散度让片段级相似度分布模仿关节级分布，保持跨粒度语义一致性。

### 关键设计选择与消融验证

消融实验证实了各模块的必要性：移除自蒸馏损失 $\mathcal{L}_{\mathrm{D}}$ 或 STI 蒸馏损失 $\mathcal{L}_{\mathrm{SD}}$ 均会导致检索准确率明显下降（Table 3、Table 4），验证了分层对齐与显式交互建模的核心作用。压缩比 $\rho=0.25$ 在效率与细节保留之间取得了最优平衡，更高或更低的值均未带来进一步提升。此外，使用 Guo 特征表示替代 MotionPatch 作为运动输入会显著降低召回率，表明结构化的局部运动表示对细粒度检索至关重要。

### 数据流与推理

在推理阶段，文本和运动序列分别经过编码器后，通过 Projection Head 投影为标量相似度分数，最终基于余弦相似度进行检索排序。整个框架无需在推理时计算 STI，保持了高效的检索速度。

### 补充图表

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our Pyramidal Shapley-Taylor (PST) learning framework. Our PST learning framework consists of Shapley-Taylor Interaction (STI), described in Sec. 3.2, and pyramidal modeling scheme, described in Sec. 3.3. As illustrated in the middle cube, each cell represents the interaction strength between a motion token and a text token within a batch, where darker colors indicate stronger semantic correlations, and lighter colors represent weaker ones*

## 核心模块与公式推导

### 基础相似度度量

PST框架以文本token $t_i$ 与运动token $m_j$ 之间的余弦相似度作为跨模态对齐的基础度量。给定文本编码器 $\boldsymbol{\mathcal{E}}_T$ 和运动编码器 $\boldsymbol{\mathcal{E}}_M$，相似度定义为：

$$s ( t _ { i } , m _ { j } ) = \frac { \boldsymbol { \mathcal { E } } _ { T } ( t _ { i } ) \cdot \boldsymbol { \mathcal { E } } _ { M } ( m _ { j } ) } { \| \boldsymbol { \mathcal { E } } _ { T } ( t _ { i } ) \| \| \boldsymbol { \mathcal { E } } _ { M } ( m _ { j } ) \| }$$

该公式为后续所有对齐阶段的评分函数提供统一基础。在训练阶段，投影头 $PH$ 将高维嵌入映射为标量相似度分数，实际使用的相似度形式为 $s(t_i, m_j) = \frac{PH(\mathcal{E}_T(t_i)) \cdot PH(\mathcal{E}_M(m_j))}{\|PH(\mathcal{E}_T(t_i))\| \|PH(\mathcal{E}_M(m_j))\|}$。

### Shapley-Taylor交互（STI）度量

STI是PST框架的核心创新，用于量化一对运动-语言token在所有可能上下文排列下的期望边际贡献。对于运动token $e_j^{\mathrm{m}}$ 和文本token $e_i^{\mathrm{t}}$，其STI值定义为：

$$\phi ( e _ { i } ^ { \mathrm { t } } , e _ { j } ^ { \mathrm { m } } ) = \mathbb { E } _ { \boldsymbol \pi } \Big [ F ( S _ { \boldsymbol \pi } \cup \{ e _ { i } ^ { \mathrm { t } } , e _ { j } ^ { \mathrm { m } } \} ) - F ( S _ { \boldsymbol \pi } \cup \{ e _ { i } ^ { \mathrm { t } } \} ) - F ( S _ { \boldsymbol \pi } \cup \{ e _ { j } ^ { \mathrm { m } } \} ) + F ( S _ { \boldsymbol \pi } ) \Big ]$$

其中 $\boldsymbol{\pi}$ 表示token的随机排列，$S_{\boldsymbol{\pi}}$ 为排列中位于该对之前的token集合，$F(\cdot)$ 为评分函数。该公式通过四次函数值计算，精确剥离单个token的独立贡献，仅保留成对交互效应。PST框架将STI阶数设为 $k=2$，专门建模成对跨模态交互。

由于精确计算STI需要对所有排列求期望，计算代价极高。为此，PST引入一个轻量级的**STI估计头 $\mathcal{H}$**（结构见Figure 6(a)），通过卷积与自注意力网络近似STI值。该估计头以运动token和文本token为输入，输出估计的交互概率分布。训练时通过STI蒸馏损失 $\mathcal{L}_{\mathrm{SD}}$ 使估计分布逼近标准STI分布：

$$\mathcal { L } _ { \mathrm { S D } } = \mathrm { K L } \left( \mathcal { D } _ { \mathrm { m 2 t } } ^ { \phi } \parallel \mathcal { D } _ { \mathrm { m 2 t } } ^ { \mathcal { H } } \right) + \mathrm { K L } \left( \mathcal { D } _ { \mathrm { t 2 m } } ^ { \phi } \parallel \mathcal { D } _ { \mathrm { t 2 m } } ^ { \mathcal { H } } \right)$$

其中 $\mathcal{D}_{\mathrm{m2t}}^{\phi}$ 和 $\mathcal{D}_{\mathrm{t2m}}^{\phi}$ 为标准STI分布，$\mathcal{D}_{\mathrm{m2t}}^{\mathcal{H}}$ 和 $\mathcal{D}_{\mathrm{t2m}}^{\mathcal{H}}$ 为估计头输出的分布，KL散度在运动到文本和文本到运动两个方向上同时约束。

### Token压缩器

在从关节级对齐过渡到片段级对齐时，需要将细粒度的token压缩为中尺度的片段/短语级表示。**Token Compressor**（结构见Figure 6(b)）由三个组件串联构成：卷积层提取局部上下文、自注意力层建模全局依赖、以及基于K近邻密度峰值聚类（KNN-DPC）的中心选择机制。KNN-DPC根据局部密度和相对距离自动选取聚类中心，将原始token压缩为代表性token。

压缩比定义为 $\rho_* = N_*^{\mathrm{sgm}} / N_*^{\mathrm{jnt}}$，其中 $* \in \{\mathrm{m}, \mathrm{t}\}$ 分别表示运动和文本模态，$N^{\mathrm{jnt}}$ 和 $N^{\mathrm{sgm}}$ 为压缩前后的token数量。实验中将 $\rho_*$ 统一设为0.25，在效率与细节保留之间取得平衡。

### 对比损失与自蒸馏损失

每个对齐阶段（关节级、片段级、整体级）均采用InfoNCE对比损失进行训练。以文本到运动方向为例：

$$\mathcal L _ { \mathrm { t 2 m } } = - \frac { 1 } { B } \sum _ { i = 1 } ^ { B } \log \frac { \exp ( s ( t _ { i } , m _ { i } ) / \tau ) } { \sum _ { j = 1 } ^ { B } \exp ( s ( t _ { i } , m _ { j } ) / \tau ) }$$

其中 $B$ 为批次大小，$\tau$ 为温度参数。运动到文本方向 $\mathcal{L}_{\mathrm{m2t}}$ 对称定义，完整的阶段对比损失 $\mathcal{L}_{\mathrm{C}}$ 为两者之和。

为保持跨粒度的语义一致性，PST引入**自蒸馏损失 $\mathcal{L}_{\mathrm{D}}$**，通过KL散度使片段级的相似度分布模仿关节级的分布：

$$\mathcal { L } _ { \mathrm { D } } = \mathrm { K L } ( \mathcal { D } _ { \mathrm { m 2 t } } ^ { \mathrm { s g m } } | | \mathcal { D } _ { \mathrm { m 2 t } } ^ { \mathrm { j n t } } ) + \mathrm { K L } ( \mathcal { D } _ { \mathrm { t 2 m } } ^ { \mathrm { s g m } } | | \mathcal { D } _ { \mathrm { t 2 m } } ^ { \mathrm { j n t } } )$$

其中 $\mathcal{D}^{\mathrm{jnt}}$ 和 $\mathcal{D}^{\mathrm{sgm}}$ 分别为关节级和片段级的相似度分布。该损失确保压缩后的片段表示不会丢失关节级捕获的细粒度对应信息。

### 总体训练目标

PST框架的最终损失函数整合了三个对齐阶段的对比损失、两个阶段（关节级和片段级）的STI蒸馏损失以及跨粒度的自蒸馏损失：

$$\mathcal { L } = \mathcal { L } _ { \mathrm { C } } ^ { \mathrm { j n t } } + \mathcal { L } _ { \mathrm { C } } ^ { \mathrm { s g m } } + \mathcal { L } _ { \mathrm { C } } ^ { \mathrm { h l t } } + \lambda _ { \mathrm { S } } ( \mathcal { L } _ { \mathrm { S D } } ^ { \mathrm { j n t } } + \mathcal { L } _ { \mathrm { S D } } ^ { \mathrm { s g m } } ) + \lambda _ { \mathrm { D } } \mathcal { L } _ { \mathrm { D } }$$

其中 $\lambda_{\mathrm{S}}$ 和 $\lambda_{\mathrm{D}}$ 分别为STI蒸馏损失和自蒸馏损失的权重系数。消融实验（Table 3、Table 4）证实，移除 $\mathcal{L}_{\mathrm{D}}$ 或 $\mathcal{L}_{\mathrm{SD}}$ 均会导致检索准确率显著下降，验证了分层对齐与显式交互建模的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/010_Figure_6.jpg]]
*Figure 6: Detailed architecture. (a) Structure of the STI Estimation Head. (b) Structure of the Token Compressor*

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/002_Figure_2.jpg]]
*Figure 2: An intuitive illustration of the STI*

## 实验与分析

### 主实验结果

PST 框架在两个主流基准上均取得了领先的检索性能。在 **HumanML3D** 的 Small batch 协议下，文本到运动检索的 R@1 达到 **71.61**，相比此前最强的基线 **TMR**（Petrovich et al., ICCV 2023）的 67.45 提升了 **+4.16** 个百分点（Table 1）。在 **KIT-ML** 数据集上，同样协议下文本到运动检索的 R@1 为 **56.83**，比 **MotionPatch**（Yu et al., CVPR 2024）的 53.55 高出 **+3.28** 个百分点（Table 2）。运动到文本方向的检索也呈现一致的优势，HumanML3D 上的 MedR 降至 1.00，表明模型几乎总能将最匹配的文本排在首位。

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/003_Table_1.jpg]]
*Table 1: Motion-to-text and text-to-motion retrieval results on HumanML3D*

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/004_Table_2.jpg]]
*Table 2: Motion-to-text and text-to-motion retrieval results on KIT-ML*

这些增益的核心驱动力来自金字塔式的细粒度对齐策略：模型不再仅依赖全局序列的余弦相似度，而是通过关节级、片段级和整体级三个层次逐级建立跨模态对应关系。Table 1 和 Table 2 中 PST 在所有 Recall 指标（R@1、R@5、R@10）和 MedR 上均超越各基线，验证了分层对齐的普适有效性。

### 消融实验

消融实验系统性地拆解了 PST 框架各组件的贡献（Table 3、Table 4）。

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/005_Table_3.jpg]]
*Table 3: Ablation on HumanML3D*

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/006_Table_4.jpg]]
*Table 4: Ablation on KIT-ML*

**自蒸馏损失 L_D 的作用。** 移除自蒸馏损失（即仅保留各阶段的独立对比损失）导致 HumanML3D 和 KIT-ML 上文本到运动及运动到文本的 Recall 全面下降。L_D 通过 KL 散度强制片段级的相似度分布向关节级分布对齐，维持了跨粒度的语义一致性。缺少这一约束时，中间层级的对齐信号会退化，模型难以有效传递细粒度信息。

**STI 蒸馏损失 L_SD 的作用。** 同样地，去除 STI 蒸馏损失会使性能显著降低。L_SD 让 STI 估计头学习逼近标准 Shapley-Taylor 交互分布，显式地量化了每对运动-语言 token 在不同上下文中的边际贡献。没有这一明确的成对交互建模，模型退化为简单的多层级余弦相似度匹配，无法捕获关键的细粒度语义关联。

**压缩比 ρ 的敏感性。** 默认压缩比 ρ=0.25 在效率与细节保留之间取得了平衡。将其调高或调低均未带来进一步提升，表明 0.25 是一个稳健的选择——既能有效压缩 token 数量以降低计算开销，又保留了足够的局部信息用于片段级对齐。

**运动表示的影响。** 将 MotionPatch 表示替换为 Guo 特征表示后，召回率显著下降。这说明结构化的局部运动表示（基于 ViT 的 patch 编码）对细粒度检索至关重要，因为它保留了关节和局部时序信息，为金字塔对齐提供了高质量的底层特征。

### 定性可视化分析

Figure 3 和 Figure 4 分别展示了片段级和关节级的对齐可视化结果。在片段级对齐中，模型成功将文本短语与对应的运动片段建立高相似度映射——例如，“jogs forward”与运动序列的前半段高度相关，“stops”则精准对应运动的中断时刻。关节级对齐进一步揭示了更精细的语义关联：文本中的“left hand”、“right leg”等词语与对应身体关节的运动 token 呈现深色高相似度，而无关关节则保持浅色低相似度。这种层次化的对应关系直观地验证了金字塔对齐策略的有效性。

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/009_Figure_4.jpg]]
*Figure 4: Visualization results of joint-wise alignment. Darker colors indicate higher similarity scores*

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/007_Figure_3.jpg]]
*Figure 3: Visualization results of segment-wise alignment. We omit \<EOS> for clarity and use commas to separate each individual word*

Figure 5 提供了文本到运动检索的定性示例，PST 检索到的运动序列在动作类型、节奏和空间轨迹上均与查询文本高度吻合，进一步佐证了定量指标的提升并非来自统计偏差，而是源于真正的语义理解。

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative results of text-to-motion retrieval*

### LLM 增强实验

Table 5 报告了在 HumanML3D 上使用 LLM 驱动的文本增强后的结果。增强策略在训练阶段利用 LLM 生成身体部位级别的描述，测试时仍使用原始文本，保证了对比的公平性。PST 在增强后取得了进一步的性能提升，表明更丰富的局部语义描述有助于模型学习更精确的关节级和片段级对齐。然而，该策略目前仅适用于文本描述多样性较高的 HumanML3D，对于 KIT-ML 等描述相对简单的数据集效果有限，尚不具备通用性。

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/015_Table_5.jpg]]
*Table 5: Motion-to-text and text-to-motion retrieval results on HumanML3D with LLM-driven text enhancement*

### 失败模式与局限性

尽管 PST 在主流基准上表现优异，但在复杂、罕见的动作类别上仍存在局部偏差。关节级和片段级对齐对训练集中频繁出现的姿势和运动模式拟合较好，但对长尾动作的泛化能力有限。此外，现有数据集的文本描述多为整体动作概括，缺乏对个别身体部位运动的明确标注，这从根本上限制了模型学习真正精确的细粒度对齐的上限。LLM 增强虽能部分缓解这一问题，但其适用范围受限于数据集本身的文本多样性，尚未形成通用的解决方案。

### 补充图表

![[assets/figures/papers/paper_list_l62_https_arxiv_org_abs_2405_04771/figures/016_Figure_11.jpg]]
*Figure 11: Text prompt for generating part-level descriptions*

## 方法谱系与知识库定位

### 核心瓶颈与突破路径

现有运动‑语言检索方法——包括 **TEMOS** (Petrovich et al., ECCV 2022)、**T2M** (Guo et al., CVPR 2022)、**TMR** (Petrovich et al., ICCV 2023) 以及 **MotionPatch** (Yu et al., CVPR 2024)——主要依赖全局序列对齐，即通过编码器将整段运动和文本描述压缩为单一嵌入向量，再计算余弦相似度进行检索。这种范式忽略了运动内部的时间片段、空间身体关节与文本标记之间的细粒度对应关系，导致模型无法捕获精确的语义细节，从而构成该领域的核心瓶颈。

本文提出的 **Pyramidal Shapley‑Taylor (PST) 学习框架** 针对上述瓶颈进行了系统性突破。其核心因果机制在于引入金字塔式的细粒度对齐策略，并采用 **Shapley‑Taylor 交互 (STI)** 度量来量化不同上下文下运动‑语言元素对的交互强度，以此引导模型学习从关节级到片段级再到整体级的层次化对应关系。这一设计受人类运动感知的金字塔过程启发——从关节动态到片段连贯性再到整体理解——通过逐级量化成对跨模态特征在上下文递增时的边际贡献，使模型能够突出关键的细粒度运动‑语言对应。

### 方法谱系中的关键变化槽位

相较于先前工作，PST 框架在四个关键维度上进行了实质性改造：

| 变化槽位 | 基线方案 | PST 方案 | 证据锚点 |
|----------|----------|----------|----------|
| 对齐粒度 | 全局序列对齐 | 金字塔式关节级、片段级、整体级细粒度对齐 | Sec. 3.3, Fig. 1 |
| 跨模态交互度量 | 全局余弦相似度 | 基于 STI 的成对边际贡献度量 | Sec. 3.2, Eq. 2 |
| 特征压缩机制 | 无（常直接使用编码器输出） | 基于卷积、自注意力和 KNN‑DPC 的 Token Compressor | Sec. 3.3, Fig. 6(b) |
| 训练信号一致性约束 | 无（仅全局对比损失） | 关节级到片段级的 KL 自蒸馏损失 $\mathcal{L}_{\mathrm{D}}$ | Sec. 3.4, Eq. 9 |

具体而言，**对齐粒度** 从单一全局层面扩展为三个层次：关节级对齐直接计算每个单词 token 与每个关节 token 的交互；片段级对齐通过 Token Compressor 将 token 压缩为片段/短语级表示后进行对齐；整体级对齐则聚合全局表示进行高层语义对应。**跨模态交互度量** 从简单的余弦相似度升级为 STI 度量，其核心公式为：

$$\phi(e_i^{\mathrm{t}}, e_j^{\mathrm{m}}) = \mathbb{E}_{\boldsymbol{\pi}} \Big[ F(S_{\boldsymbol{\pi}} \cup \{e_i^{\mathrm{t}}, e_j^{\mathrm{m}}\}) - F(S_{\boldsymbol{\pi}} \cup \{e_i^{\mathrm{t}}\}) - F(S_{\boldsymbol{\pi}} \cup \{e_j^{\mathrm{m}}\}) + F(S_{\boldsymbol{\pi}}) \Big]$$

该公式度量一对运动‑语言 token 在所有排列上的期望边际贡献，量化其交互强度。**特征压缩机制** 采用卷积、自注意力和 K‑近邻密度峰值聚类（KNN‑DPC）算法，在关节级到片段级过渡时压缩 token 数量并整合上下文信息，压缩比 $\rho_* = N_*^{\mathrm{sgm}} / N_*^{\mathrm{jnt}}$ 设为 0.25，在效率与细节保留之间取得平衡。**训练信号一致性约束** 通过 KL 散度让片段级相似度分布模仿关节级分布，保持跨粒度的一致性：

$$\mathcal{L}_{\mathrm{D}} = \mathrm{KL}( \mathcal{D}_{\mathrm{m2t}}^{\mathrm{sgm}} \parallel \mathcal{D}_{\mathrm{m2t}}^{\mathrm{jnt}} ) + \mathrm{KL}( \mathcal{D}_{\mathrm{t2m}}^{\mathrm{sgm}} \parallel \mathcal{D}_{\mathrm{t2m}}^{\mathrm{jnt}} )$$

### 与同期工作的关系

在细粒度运动‑语言对齐方向上，PST 框架与 **Lyu et al. (2025)** 和 **SGAR**（LLM‑增强对比方法）形成互补但不同的技术路线。Lyu et al. (2025) 同样关注细粒度对齐，但其具体技术方案在可用分析中未详细展开；SGAR 则借助 LLM 生成部位级描述来增强训练数据。PST 框架在训练阶段也可集成 LLM 增强（见 Table 5），但测试时仍使用原始文本描述，确保对比公平。PST 的核心区分点在于其金字塔式层级对齐与 STI 交互度量的理论统一，而非单纯依赖数据增强。

### 适用边界与局限

尽管 PST 框架在 HumanML3D 和 KIT‑ML 上取得了显著提升，其适用边界仍存在以下约束：

1. **复杂/罕见动作的局部偏差**：关节级和片段级检索在训练集中少见的姿势或运动模式上可能无法良好泛化，导致局部对齐质量下降。
2. **数据集文本描述的粒度限制**：现有数据集的文本描述主要为整体动作，缺乏对个别身体部位运动的明确描述，模型难以学习真正精确的细粒度对齐。即使使用 LLM 增强，增强效果也局限于描述多样性较高的 HumanML3D，对于文本描述较为简单的 KIT‑ML 等数据集效果有限。
3. **LLM 增强策略的通用性不足**：当前的 LLM 驱动文本增强策略尚未实现通用的细粒度增强方案，对简单文本描述的数据集效果有限。

### 开放问题

PST 框架的提出同时打开了若干值得进一步探索的方向：

1. **开放词汇运动‑语言理解**：如何将金字塔 Shapley‑Taylor 学习框架扩展到开放词汇场景，使其能够处理训练中未见过的动作和描述？
2. **通用文本增强策略**：如何设计更通用的文本增强策略（可能不依赖特定 LLM）来为多样化数据集生成高质量的身体部位级描述？
3. **长尾动作鲁棒性**：能否通过多任务学习、数据增强或引入外部知识来缓解关节级和片段级对齐中的局部偏见，提高对长尾动作的鲁棒性？
4. **轻量化 STI 估计**：STI 估计头的轻量化设计是否可以在极低计算资源下保持高保真度，从而推动实时或移动端的应用？

## 原文 PDF

![[paperPDFs/arxiv_2026/PST_Beyond_Global_Alignment_Fine_Grained_Motion_Language_Retrieval_via_Pyramidal_Shapley_Taylor_Learning.pdf]]