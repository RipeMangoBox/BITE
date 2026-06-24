---
title: "ST4R-Splat: Spatio-Temporal Referring Segmentation in 4D Gaussian Splatting"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ST4R_Splat_Spatio_Temporal_Referring_Segmentation_in_4D_Gaussian_Splatting.pdf
project_link: null
code_link: null
aliases:
- ST4R-Splat
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过引入时间不变指代嵌入（Instance-Aware 4D Gaussian Referring Field）和独立的实例级时态状态映射模块（Instance-Level Temporal State Mapping），将‘在哪里’（实例身份）与‘在何时’（时态状态）显式解耦，使模型能独立优化空间定位和时间定位。
primary_logic: 核心思想是为每个4D高斯分配一个时间不变的指代嵌入以维持实例身份一致性，并在特征空间建立实例-时间到语义状态的直接映射（状态缓存），从而避免对2D渲染损失的依赖，实现视点无关的鲁棒时态定位。
claims:
- 在HyperNeRF基准上，ST4R-Splat在时间无关指代查询上达到77.67% mIoU，显著优于所有基线方法。
- 在时间敏感指代查询上，ST4R-Splat达到83.44% Acc和57.98% vIoU，实现了精确的时态定位和分割。
- 消融实验表明，移除位置感知跨模态注意力模块会导致mIoU从77.67%骤降至58.56%，证明了空间语言对齐的关键作用。
- 消融实验还表明，对比损失和实例正则化损失均有贡献，去除后性能分别降至70.85%和76.94%。
---

# ST4R-Splat: Spatio-Temporal Referring Segmentation in 4D Gaussian Splatting

> [!tip] 核心洞察
> 核心思想是为每个4D高斯分配一个时间不变的指代嵌入以维持实例身份一致性，并在特征空间建立实例-时间到语义状态的直接映射（状态缓存），从而避免对2D渲染损失的依赖，实现视点无关的鲁棒时态定位。

| 字段 | 内容 |
|------|------|
| 中文题名 | ST4R-Splat: 4D高斯泼溅中的时空指代分割 |
| 英文题名 | ST4R-Splat: Spatio-Temporal Referring Segmentation in 4D Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Meng_ST4R-Splat_Spatio-Temporal_Referring_Segmentation_in_4D_Gaussian_Splatting_CVPR_2026_paper.html) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | ST4R-Splat |
| Dataset | HyperNeRF |

> [!tip] 效果简介
> - HyperNeRF (STRS-4DGS benchmark) 上，mIoU (time-agnostic referring) 77.67%；Acc (time-sensitive referring) 83.44%；vIoU (time-sensitive referring) 57.98%。

## 概述

**问题瓶颈**：现有动态场景理解方法（如4DLangSplat）仅支持开放词汇的类别级查询，无法在显式4D高斯重建中实现实例级消歧和联合时空指代推理。其根本缺陷在于缺少将空间指代与时态状态解耦的机制，导致对“被人拿在手中断成两半的物体”这类复杂时空表达式的定位与分割性能差。

**核心思路**：ST4R-Splat通过引入**时间不变指代嵌入**（Instance-Aware 4D Gaussian Referring Field）和独立的**实例级时态状态映射模块**（Instance-Level Temporal State Mapping），将“在哪里”（实例身份）与“在何时”（时态状态）显式解耦。具体而言，为每个4D高斯分配一个时间不变的指代嵌入以维持实例身份一致性，并在特征空间建立实例-时间到语义状态的直接映射（状态缓存），从而避免对2D渲染损失的依赖，实现视点无关的鲁棒时态定位。

**方法定位**：该方法属于基于4D高斯泼溅的动态场景指代分割框架。在方法谱系上，它继承并突破了**4DLangSplat**（Li et al., CVPR 2025）的可变形语言场范式——后者仅支持类别/短语级检索，不具备实例消歧和精细时态定位能力。ST4R-Splat在四个关键维度上进行了改进：（1）高斯语义表示从随时间变化的语言特征转向时间不变指代嵌入；（2）跨模态对齐从简单点积转向注入空间坐标的位置感知注意力机制；（3）时态建模从隐式变形转向显式的实例-时间状态缓存；（4）监督信号从通用描述转向自动解耦的空间/时态双支标注。

**主要结果**：在HyperNeRF基准上，ST4R-Splat在时间无关指代查询上达到**77.67% mIoU**，显著优于所有基线方法；在时间敏感指代查询上达到**83.44% Acc**和**57.98% vIoU**，实现了精确的时态定位与分割。消融实验表明，位置感知跨模态注意力模块的移除会导致mIoU骤降至58.56%，验证了空间-语言对齐的关键作用；对比损失和实例正则化损失的去除分别使性能降至70.85%和76.94%，证明各部分均有实质贡献。

## 背景与动机

动态场景理解是计算机视觉的核心问题之一。近年来，以3D高斯泼溅（3D Gaussian Splatting, 3DGS）为代表的显式辐射场表示在静态场景的重建与语义理解上取得了显著进展。然而，当场景随时间动态变化时，如何在4D空间中实现精确的**实例级指代分割**——即根据自然语言表达式定位并分割出特定物体——仍然是一个开放挑战。

现有方法在动态场景语言驱动的分割上存在两个根本性缺口。其一，**缺乏实例级消歧能力**。以 **4DLangSplat**（Li et al., CVPR 2025）为代表的动态语言场方法，通过可变形网络将语言特征适配到不同时间步，能够支持开放词汇的类别级或短语级查询，但无法区分同一类别下的不同实例。当场景中存在多个外观相似的物体时，这类方法难以根据指代表达式精确锁定目标个体。

其二，**空间指代与时态状态耦合不足**。现实中的时空指代往往同时涉及“在哪里”（空间定位）和“在何时/处于何种状态”（时态定位）两个维度。例如，查询“被人拿在手中断成两半的物体”要求模型同时理解物体的空间身份（是哪一个物体）和其时态状态（在何时被拿起并断裂）。现有方法缺少将这两者显式解耦的机制，导致对复杂时空表达式的定位与分割性能不佳。

上述缺口的本质瓶颈在于：现有4D高斯表示中的语义特征通常随时间变化，无法为同一实例维护跨时间的一致身份签名；同时，时态状态的判断往往依赖2D渲染损失间接优化，缺乏在特征空间直接建模的机制，导致时态定位对视点变化敏感且精度有限。

针对这些问题，ST4R-Splat 提出了两个核心设计思路：为每个4D高斯分配**时间不变的指代嵌入**以维持实例身份一致性，并在特征空间建立**实例-时间到语义状态的直接映射**，从而实现空间定位与时态定位的显式解耦与独立优化。

## 核心创新

ST4R-Splat 的核心创新在于首次在显式4D高斯重建框架中实现了**实例身份与时态状态的解耦建模**，从而支持复杂时空指代查询（如“被人拿在手中断成两半的物体”）。此前的动态场景指代方法（如 **4DLangSplat**，Li et al., CVPR 2025）仅通过可变形语言场实现开放词汇的类别级检索，缺乏实例级消歧与精细时态定位能力。ST4R-Splat 通过三个关键的“changed slots”突破了这一瓶颈。

### 时间不变指代嵌入：实例身份的解耦

**基线方法**（4DLangSplat）为每个高斯分配随时间变化的语言特征，这使得实例身份随帧变化而漂移，无法在时间维度上保持一致的实例标识。

**ST4R-Splat 的方案**是为每个4D高斯 $g_i(t)$ 引入一个可学习的、时间不变的指代嵌入 $e_i \in \mathbb{R}^d$，构成 **Instance-Aware 4D Gaussian Referring Field**。这一设计的因果机制在于：将“在哪里”（实例身份）与“在何时”（时态状态）在表示层面显式分离——$e_i$ 负责编码实例的细粒度语义与身份信息，而时间变化由高斯自身的变形场 $( \mu _ { i } ( t ) , s _ { i } ( t ) , r _ { i } ( t ) ) = ( \mu _ { i } + \Delta \mu _ { i } ( t ) , s _ { i } + \Delta s _ { i } ( t ) , r _ { i } + \Delta r _ { i } ( t ) )$ 单独处理。这使得模型能够在所有时间帧上维持稳定的实例标识，为后续的跨帧指代推理提供基础。

### 位置感知跨模态注意力：空间语言对齐的强化

**基线方法**通常采用简单的点积或CLIP特征相似度来计算高斯与查询文本的匹配分数，忽略了高斯的空间位置信息。

**ST4R-Splat 的方案**是引入位置感知的跨模态注意力机制 $\phi$，将时间变形后的空间坐标 $\mu_i(t)$ 显式注入对齐过程：$e _ { i } ^ { \prime } ( t ) = \phi ( e _ { i } , \mu _ { i } ( t ) , E )$，其中 $E$ 为查询文本的单词嵌入。增强后的特征 $e_i'(t)$ 再与所有单词嵌入计算平均内积作为语义相关性分数 $m _ { i } ( t ) = \frac { 1 } { L } \sum _ { j = 1 } ^ { L } \langle e _ { i } ^ { \prime } ( t ) , E _ { j } \rangle$。这一设计的因果机制在于：通过让每个高斯“看到”自己当前的空间位置，模型能够区分空间上邻近但语义不同的实例，从而显著提升空间指代的精确度。消融实验为此提供了决定性证据：**移除该跨模态注意力模块后，mIoU从77.67%骤降至58.56%**（Table 2），降幅达19.11个百分点，证明空间语言对齐是整个框架的核心性能驱动因素。

### 实例级时态状态映射：视点无关的时序定位

**基线方法**（4DLangSplat）通过可变形网络将语言场整体变形以适应时间变化，但这种方式将时态信息与空间表示纠缠在一起，且依赖于2D渲染损失，导致在新视点下的时态定位鲁棒性差。

**ST4R-Splat 的方案**是引入 **Instance-Level Temporal State Mapping** 模块，在特征空间直接建立实例-时间到语义状态的映射。具体而言，对于每个实例 $k$，其代表性特征 $\bar{e}_k$ 与时间戳 $t$ 通过映射函数 $\mathcal{F}$ 生成动态状态特征 $c_{k,t} = \mathcal{F}(\bar{e}_k, t)$，并预先计算状态缓存 $\mathcal{C}_k = \{c_{k,t} \mid t \in [0, T]\}$。这一设计的因果机制在于：将时态定位从2D渲染空间转移到高维特征空间，通过特征相似度匹配实现**视点无关**的时序推理——模型无需依赖特定视角的渲染图像即可判断“物体在何时处于何种状态”。在时间敏感指代查询任务上，该方法达到 **83.44% Acc** 和 **57.98% vIoU**（Table 1b），验证了其在精确时态定位上的有效性。

### 解耦监督信号：自动化文本标注管道

**基线方法**通常使用通用的视频或帧级描述，不区分空间语义和时间状态信息。

**ST4R-Splat 的方案**是构建基于MLLM的自动化标注管道，分别生成两类解耦的文本监督：帧级描述性caption $C ^ { \mathrm { d e s c } } ( o _ { k } , t )$ 用于空间监督，以及时间感知状态caption $C ^ { \mathrm { s t a t e } } ( o _ { k } , t )$ 用于时态监督。这一设计为上述三个技术模块提供了精确匹配的解耦训练目标，使模型能够分别优化空间定位损失 $\mathcal{L}_{ref}$（BCE）和对比损失 $\mathcal{L}_{con}$，以及实例正则化损失 $\mathcal{L}_{comp}$ 和 $\mathcal{L}_{dist}$。消融实验表明，**移除对比损失后mIoU降至70.85%，移除实例正则化损失后降至76.94%**（Table 2），分别贡献了6.82和0.73个百分点的性能提升，验证了解耦监督与相应损失设计的协同作用。

## 整体框架

ST4R-Splat 的核心设计理念是将时空指代分割中的“在哪里”（实例身份）与“在何时”（时态状态）**显式解耦**，分别交由两个独立模块优化。如图1所示，框架由三个关键组件串联构成：

1. **基于多模态大语言模型（MLLM）的对象标注**：自动生成解耦的文本监督信号——帧级描述性文本（空间监督）和时间感知状态文本（时态监督）。
2. **实例感知的4D高斯指代场**：为每个4D高斯分配一个时间不变的指代嵌入，并通过位置感知的跨模态注意力机制实现空间实例定位。
3. **实例级时态状态映射**：在特征空间建立实例嵌入与时态状态特征的直接映射（状态缓存），实现视点无关的时序定位。

### 输入输出流

整个pipeline的输入为一段动态场景的多视角视频，输出为给定自然语言查询（如“被人拿在手中断成两半的物体”）的时空分割掩码。流程如下：

- **Step 1 — 文本监督生成**：利用MLLM对每个对象 $o_k$ 在时刻 $t$ 生成两种互补的文本描述：
  - 帧级描述性文本 $C^{\mathrm{desc}}(o_k, t)$，提供对象的细粒度空间语义；
  - 时间感知状态文本 $C^{\mathrm{state}}(o_k, t)$，描述对象在特定时刻的瞬时状态或运动状态。
  这两种文本在后续训练中分别驱动空间定位和时态定位。

- **Step 2 — 4D高斯场景表示**：采用可变形4D高斯泼溅（4DGS）作为底层场景表示。每个规范高斯 $g_i$ 通过时间变形网络映射到时刻 $t$ 的状态：
  $$(\mu_i(t), s_i(t), r_i(t)) = (\mu_i + \Delta\mu_i(t), s_i + \Delta s_i(t), r_i + \Delta r_i(t))$$
  其中 $\mu_i, s_i, r_i$ 分别为规范高斯的中心位置、尺度和旋转。

- **Step 3 — 空间实例定位**：在4DGS基础上，为每个高斯 $g_i(t)$ 附加一个可学习的、**时间不变的指代嵌入** $e_i \in \mathbb{R}^d$。该嵌入通过位置感知跨模态注意力 $\phi$ 与文本单词嵌入 $E$ 交互，得到增强特征：
  $$e_i'(t) = \phi(e_i, \mu_i(t), E)$$
  随后计算增强特征与所有单词嵌入的平均内积作为语义相关性分数 $m_i(t)$，并通过可微渲染生成预测掩码 $M_{pred}(t)$。掩码与伪真值 $M_{gt}(t)$ 之间的二元交叉熵构成指代损失 $\mathcal{L}_{ref}$。

- **Step 4 — 时态状态定位**：对于每个对象 $k$，从其所属高斯的指代嵌入中聚合得到代表性特征 $\bar{e}_k$，通过映射 $\mathcal{F}$ 获得时刻 $t$ 的目标状态特征：
  $$c_{k,t} = \mathcal{F}(\bar{e}_k, t)$$
  该映射被实现为显式的对象中心状态缓存 $\mathcal{C}_k = \{c_{k,t} \mid t \in [0, T]\}$。在推理时，给定时间敏感查询（如“断成两半的物体”），系统在状态缓存中检索匹配的帧，实现**视点无关**的时态定位。

### 模块间关系

三个组件的依赖关系清晰：**MLLM标注**为后续两个模块提供解耦的监督信号；**实例感知指代场**负责空间维度的“哪个对象”；**时态状态映射**负责时间维度的“何时发生”。这种解耦设计使得空间定位和时态定位可以独立优化——空间模块仅需关注实例身份的跨帧一致性，时态模块仅需在特征空间学习实例-时间到语义状态的映射，从而避免了对2D渲染损失的依赖，实现了新视角下的鲁棒时态定位。

> **需要手动验证**：框架图中各模块间的具体数据流维度（如指代嵌入维度 $d$、状态缓存的存储结构）在提供的分析中未明确给出，建议查阅原文 Sec. 3.2 及 Fig. 1 确认细节。

![[assets/figures/papers/paper_list_l47_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_ST4R_Splat_Spatio/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the ST4R-Splat framework. It mainly consists of three main components: (I) MLLM-based object captioning for generating decoupled textual supervision, (II) an Instance-Aware 4D Referring Field for spatial grounding, and (III) an Instance-Level Temporal State Mapping module for robust temporal localization*

## 核心模块与公式推导

ST4R-Splat 将时空指代分割任务显式解耦为“在哪里”（实例身份）与“在何时”（时态状态）两个正交子问题，通过三个核心模块协同实现。本节按数据流顺序阐述关键模块及其核心公式。

### 4D 高斯变形基础

本方法建立在 4D 高斯泼溅（4DGS）之上。每个规范高斯 $g_i$ 通过可学习的时间变形网络映射到时刻 $t$ 的动态状态：

$$( \mu _ { i } ( t ) , s _ { i } ( t ) , r _ { i } ( t ) ) = ( \mu _ { i } + \Delta \mu _ { i } ( t ) , s _ { i } + \Delta s _ { i } ( t ) , r _ { i } + \Delta r _ { i } ( t ) ) \tag{1}$$

其中 $\mu_i, s_i, r_i$ 分别为规范高斯的中心位置、尺度和旋转四元数，$\Delta\mu_i(t), \Delta s_i(t), \Delta r_i(t)$ 为时间相关偏移量。该变形场为后续所有时空操作提供动态几何基础。

### MLLM 驱动的解耦文本监督生成

为获得解耦的空间与时态监督信号，ST4R-Splat 设计了基于多模态大语言模型（MLLM）的自动标注管道，为每个对象 $o_k$ 在时刻 $t$ 生成两类互补描述：

**帧级描述性 Caption（空间监督）**：利用单帧 RGB 图像和对象裁剪区域，结合基础描述文本作为提示，生成细粒度空间描述：

$$C ^ { \mathrm { d e s c } } ( o _ { k } , t ) = \mathbf { M L L M } ( \{ I _ { t } ( o _ { k } ) , I _ { t } \} , \{ T ^ { \mathrm { b a s e } } ( o _ { k } , t ) , \mathcal { P } ^ { \mathrm { d e s c } } \} ) \tag{2}$$

其中 $I_t(o_k)$ 为对象裁剪图，$I_t$ 为全帧图像，$T^{\mathrm{base}}$ 为初始描述文本，$\mathcal{P}^{\mathrm{desc}}$ 为描述生成提示模板。

**时态状态 Caption（时态监督）**：利用视频片段 $\mathcal{V}(o_k, t)$ 和对象级摘要文本，生成对象在时刻 $t$ 的瞬时状态描述（如“被人拿在手中”“断成两半”）：

$$C ^ { \mathrm { s t a t e } } ( o _ { k } , t ) = \mathbf { M L L M } ( \mathcal { V } ( o _ { k } , t ) , \{ \mathcal { T } ^ { \mathrm { s u m } } ( o _ { k } ) , \mathcal { P } ^ { \mathrm { s t a t e } } \} ) \tag{3}$$

这种解耦标注策略使模型能够分别学习空间语义和时态语义，避免两类信息在特征空间中纠缠。

### 实例感知 4D 高斯指代场（空间定位核心）

该模块是空间实例定位的核心。每个时变高斯 $g_i(t)$ 被赋予一个**时间不变指代嵌入** $e_i \in \mathbb{R}^d$，其关键性质是不随时间变化，从而在整个视频中维持实例身份一致性。

为实现语言与高斯场的精细对齐，引入**位置感知跨模态注意力机制** $\phi$。该机制以高斯当前位置 $\mu_i(t)$ 作为空间先验，动态增强指代嵌入：

$$e _ { i } ^ { \prime } ( t ) = \phi ( e _ { i } , \mu _ { i } ( t ) , E ) \tag{4}$$

其中 $E$ 为查询文本的单词嵌入序列。增强后的特征 $e_i'(t)$ 同时编码了实例语义和空间上下文。

随后计算增强特征与所有单词嵌入的平均内积作为**语义相关性分数**：

$$m _ { i } ( t ) = \frac { 1 } { L } \sum _ { j = 1 } ^ { L } \langle e _ { i } ^ { \prime } ( t ) , E _ { j } \rangle \tag{5}$$

该分数通过 Sigmoid 激活后沿视线累积渲染为预测掩码 $M_{\mathrm{pred}}(t)$，并由二元交叉熵损失监督：

$$\mathcal { L } _ { r e f } = \mathrm { B C E } ( M _ { p r e d } ( t ) , M _ { g t } ( t ) ) \tag{6}$$

为进一步强化特征判别力，引入**对比损失**将实例聚合特征 $e_g(t)$ 与文本句子级嵌入 $e_{txt}$ 对齐：

$$\mathcal { L } _ { c o n } = \mathbf { C o n } ( e _ { g } ( t ) , e _ { t x t } ) \tag{7}$$

同时辅以**实例感知正则化损失**，包含类内紧凑性损失 $\mathcal{L}_{\mathrm{comp}}$ 和类间区分性损失 $\mathcal{L}_{\mathrm{dist}}$：

$$\mathcal { L } _ { c o m p } = \frac { 1 } { N } \sum _ { k = 1 } ^ { N } \left( \frac { 1 } { | M _ { k , t } | } \sum _ { v \in M _ { k , t } } \| F _ { t } ( v ) - \overline { F } _ { k , t } \| _ { 2 } \right) \tag{8}$$

$$\mathcal { L } _ { d i s t } = \frac { 1 } { N ( N - 1 ) } \sum _ { k \neq k ^ { \prime } } \frac { 1 } { \| \overline { F } _ { k , t } - \overline { F } _ { k ^ { \prime } , t } \| _ { 2 } ^ { 2 } + \epsilon } \tag{9}$$

其中 $\overline{F}_{k,t}$ 为实例 $k$ 在时刻 $t$ 的特征原型。这两项损失共同作用，使同类实例特征聚拢、异类特征推开，提升嵌入空间的实例判别性。

### 实例级时态状态映射（时态定位核心）

时态定位的核心挑战在于：同一对象在不同时刻可能呈现截然不同的语义状态（如“完整”vs“断裂”），且这种状态判断应独立于观测视角。

ST4R-Splat 的解决方案是**实例级时态状态映射模块**。该模块在特征空间直接建立从“实例身份 + 时间戳”到“语义状态特征”的映射：

$$c_{k,t} = \mathcal{F}(\bar{e}_k, t) \tag{12}$$

其中 $\bar{e}_k$ 为实例 $k$ 的代表性指代嵌入（由该实例所有高斯的 $e_i$ 聚合得到），$c_{k,t}$ 为实例 $k$ 在时刻 $t$ 的语义状态特征。

为简化实现并提升效率，映射 $\mathcal{F}$ 被具体实现为显式的**对象中心状态缓存**：

$$\mathcal{C}_k = \{c_{k,t} \mid t \in [0, T]\} \tag{13}$$

该缓存预计算每个实例在所有时间戳上的状态特征。在推理时，给定时间敏感查询（如“被人拿在手中的物体”），模型通过检索状态缓存定位正确的时间帧，再结合空间指代场完成分割。由于状态映射完全在特征空间进行，不依赖 2D 渲染损失，因此天然具有视点无关的鲁棒性。

### 模块间因果机制总结

三个核心模块形成清晰的因果链条：**MLLM 标注管道**提供解耦的空间与时态文本监督 → **实例感知指代场**利用时间不变嵌入和位置感知注意力实现空间实例定位 → **时态状态映射模块**在特征空间建立实例-时间到状态的直接映射，实现视点无关的时态定位。消融实验（Table 2）验证了这一设计的有效性：移除位置感知跨模态注意力导致 mIoU 从 77.67% 骤降至 58.56%，移除对比损失降至 70.85%，移除实例正则化损失降至 76.94%，证明各组件均对最终性能有不可替代的贡献。

## 实验与分析

### 主实验结果

ST4R-Splat 在两个维度上全面验证了其时空指代分割能力：时间无关查询（实例定位）和时间敏感查询（时态定位）。所有实验均在基于 HyperNeRF 构建的 STRS-4DGS 基准上完成，该基准包含 6 个场景、26 个物体，共设计 52 个时间无关查询和 8 个时间敏感查询。

**时间无关指代查询（Time-Agnostic Referring）** 评估模型在忽略时态变化时，仅凭空间语义定位目标实例的能力。如 Table 1a 所示，ST4R-Splat 在所有测试帧上平均 mIoU 达到 **77.67%**，显著优于包括 **4DLangSplat**（Li et al., CVPR 2025）在内的所有基线方法。这一结果表明，时间不变指代嵌入配合位置感知跨模态注意力机制，能够在动态 4D 场景中建立稳定的实例级空间对应关系。Figure 2 的定性对比进一步印证了这一结论：4DLangSplat 的激活热力图在目标区域外存在大量噪声响应，而 ST4R-Splat 的响应高度聚焦于目标实例，分割掩码也更为精确。

**时间敏感指代查询（Time-Sensitive Referring）** 要求模型同时理解“在哪里”和“在何时”，例如定位“被人拿在手中断成两半的物体”对应的帧区间。Table 1b 报告了 ST4R-Splat 在该任务上的两项指标：时态准确率 Acc 达到 **83.44%**，表明模型能可靠地识别目标状态出现的帧；vIoU 达到 **57.98%**，综合衡量了时态定位准确性与分割质量。Figure 3 展示了新视角下的定性结果，ST4R-Splat 在视角变化时仍能保持一致的时态定位，这得益于实例级时态状态映射模块在特征空间而非渲染空间进行时态推理的设计。

### 消融实验

Table 2 通过逐步移除关键组件，量化了各模块对时间无关查询 mIoU 的贡献：

![[assets/figures/papers/paper_list_l47_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_ST4R_Splat_Spatio/figures/006_Table_2.jpg]]
*Table 2: Ablation study of different components in our ST4R-Splat framework. The performance is evaluated using the mIoU metric for time-agnostic queries on the HyperNeRF dataset*

**位置感知跨模态注意力模块** 是性能的核心支柱。移除该模块后，mIoU 从 77.67% 骤降至 **58.56%**（降幅约 19 个百分点）。该模块将高斯的时变空间坐标 $\mu_i(t)$ 注入跨模态注意力计算（Eq. (4)），使语言特征能够显式感知 3D 几何位置。失去这一空间对齐机制后，模型退化为简单的语义匹配，无法区分空间中不同位置的同类物体，证实了空间-语言对齐在实例级指代中的决定性作用。

**对比损失 $\mathcal{L}_{con}$** 的移除导致 mIoU 降至 **70.85%**。该损失将实例聚合特征与文本句子级嵌入对齐（Eq. (7)），其约 7 个百分点的贡献表明，显式的高斯-文本对比学习对于建立有区分力的跨模态特征空间至关重要。

**实例感知特征正则化损失 $\mathcal{L}_{inst}$** 的移除使 mIoU 降至 **76.94%**。该损失包含类内紧凑性（Eq. (8)）和类间区分性（Eq. (9)）两个子项，分别将同一实例的特征拉向原型、将不同实例的原型推开。虽然其单独贡献（约 0.7 个百分点）小于前两者，但它确保了时间不变嵌入在特征空间中的结构化组织，为实例身份一致性提供了基础约束。

### 失败模式与局限

当前基准仅覆盖 6 个场景和 26 个物体，场景多样性和物体数量有限，模型在更复杂动态环境中的泛化性尚待验证。此外，时间敏感查询仅设计了 8 个，可能不足以全面评估时态定位的细粒度能力。自动标注管道生成的伪标签噪声对最终性能的量化影响尚未被分离分析。在极长视频或高速运动场景下，状态缓存 $\mathcal{C}_k$ 的存储与计算开销是否可控，论文未提供实验证据，需要进一步验证。

### 关键图表结论

- **Table 1a**：时间无关查询 mIoU 77.67%，验证了实例感知 4D 指代场的空间定位能力。
- **Table 1b**：时间敏感查询 Acc 83.44% / vIoU 57.98%，验证了时态状态映射模块的时态定位与分割能力。
- **Table 2**：位置感知跨模态注意力是最大性能瓶颈（移除后 mIoU 降幅达 19pp），对比损失和实例正则化损失均有正向贡献。
- **Figure 2**：定性展示 ST4R-Splat 在时间无关查询上的激活聚焦度和掩码精度均优于 4DLangSplat。
- **Figure 3**：定性展示 ST4R-Splat 在新视角下仍能保持一致的时态定位，验证了视点无关的时态推理设计。

![[assets/figures/papers/paper_list_l47_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_ST4R_Splat_Spatio/figures/003_Figure_2.jpg]]
*Figure 2: Qualitative comparison of time-agnostic referring querying results between 4DLangSplat [22] and our method. For both methods, we visualize the activation heatmaps and the final predicted masks (highlighted in red)*

![[assets/figures/papers/paper_list_l47_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_ST4R_Splat_Spatio/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative comparison of time-sensitive query results in novel viewpoints between 4DLangSplat [22] and our method*

### 补充图表

![[assets/figures/papers/paper_list_l47_https_openaccess_thecvf_com_content_CVPR2026_html_Meng_ST4R_Splat_Spatio/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons on the HyperNeRF dataset. We report (a) time-agnostic referring querying (mIoU in %) and (b) timesensitive referring querying (Acc and vIoU in %). Best results are highlighted in bold*

## 方法谱系与知识库定位

### 1. 动态场景理解与指代分割的演进脉络

ST4R-Splat 处于**显式4D场景表示**与**开放词汇指代分割**的交叉点上。该工作的直接前身是 **4DLangSplat**（Li et al., CVPR 2025），后者首次将语言场引入可变形4D高斯泼溅（4DGS）框架，实现了对动态场景的开放词汇查询。然而，4DLangSplat 的核心局限在于：其语言场仅支持**类别/短语级**的语义检索，缺乏实例级消歧能力，且无法处理“在何时”的时态约束。这意味着面对“被人拿在手中断成两半的物体”这类复合时空表达式时，4DLangSplat 既无法区分同一类别的不同实例，也无法定位物体的特定状态时刻。

ST4R-Splat 的突破点在于**显式解耦“在哪里”（实例身份）与“在何时”（时态状态）**。这一设计选择使其区别于两类相关工作：

- **基于CLIP特征匹配的3D/4D分割方法**（如LERF、LangSplat、4DLangSplat）：这些方法依赖点积相似度或类别原型进行语义定位，本质上将指代视为单阶段检索问题。ST4R-Splat 则通过时间不变的指代嵌入 $e_i$ 维持实例身份一致性，将指代转化为实例识别与时态匹配的两阶段推理。
- **基于可变形语言场的方法**（如4DLangSplat）：其通过变形网络隐式建模时间变化，但语义特征本身随时间漂移，导致同一实例在不同时刻可能被识别为不同实体。ST4R-Splat 的 Instance-Aware 4D Gaussian Referring Field 通过固定 $e_i$ 并仅让位置坐标 $\mu_i(t)$ 参与跨模态注意力，从根本上避免了身份漂移。

### 2. 因果机制与方法边界

ST4R-Splat 的核心因果机制可概括为**身份固化 + 状态缓存**：

1. **身份固化**：每个4D高斯被赋予一个可学习的、时间不变的指代嵌入 $e_i$，该嵌入通过位置感知的跨模态注意力 $\phi(e_i, \mu_i(t), E)$ 与文本查询动态交互，但本身不随时间变化。这确保了实例在任意时刻的语义身份一致。
2. **状态缓存**：Instance-Level Temporal State Mapping 模块在特征空间建立 $\mathcal{C}_k = \{c_{k,t} \mid t \in [0, T]\}$ 的显式映射，将时态定位从2D渲染损失中解放出来，实现视点无关的鲁棒推断。

**适用边界**：
- 该方法假设场景中实例数量有限且可预先识别（当前基准仅含6个场景、26个物体），对大规模开放场景的扩展性尚未验证。
- 状态缓存 $\mathcal{C}_k$ 需要预计算所有时间戳的状态特征，在极长视频或高速运动场景下存储开销线性增长，可能成为瓶颈。
- 自动标注管道依赖MLLM生成解耦的空间描述 $C^{\mathrm{desc}}$ 和时态描述 $C^{\mathrm{state}}$，伪标签噪声对下游性能的影响未量化。

### 3. 知识库定位与开放问题

在4D场景理解的知识体系中，ST4R-Splat 填补了**实例级时空指代分割**的空白。与现有工作相比：

| 方法 | 场景表示 | 查询粒度 | 时态建模 |
|------|----------|----------|----------|
| LERF | 3D特征场 | 开放词汇 | 无 |
| LangSplat | 3DGS | 开放词汇 | 无 |
| 4DLangSplat | 4DGS+变形场 | 类别/短语 | 隐式（特征变形） |
| **ST4R-Splat** | **4DGS+变形场** | **实例级** | **显式（状态缓存）** |

**开放问题**：
1. 状态缓存机制能否通过层次化或稀疏化策略扩展到包含数百个实例的长视频？
2. 自动标注管道的伪标签噪声对最终性能的定量影响需进一步消融。
3. 该方法能否处理多对象交互场景（如“A递给B的物体”）以及更复杂的时态逻辑（先后顺序、持续时间）？
4. 当前基准规模有限，在更大规模、更多样化的动态场景数据集上的泛化性有待验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/ST4R_Splat_Spatio_Temporal_Referring_Segmentation_in_4D_Gaussian_Splatting.pdf]]
