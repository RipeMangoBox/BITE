---
title: LLaMo Human Motion Instruction Tuning
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/LLaMo_Human_Motion_Instruction_Tuning.pdf
aliases:
- LHMIT
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: LLaMo将运动数据作为独立模态直接输入LLM，并通过Cross Talker模块实现文本引导的自适应关键帧选择与双向跨模态融合，在保留运动细节的同时大幅降低计算复杂度。
primary_logic: 保留原始运动数据作为连续特征而不进行离散化，借助文本感知的关键帧压缩和特征对齐，能够更精准地捕捉人类动作的时空动态细节，从而提升在运动密集型场景下的行为分析和理解能力。
claims:
- LLaMo在MoVid-Bench和BABEL-QA上取得多项最优结果，证明其原生运动表示和跨模态融合的有效性。
- 在专业挥杆数据集上，LLaMo整体准确率大幅超越MotionLLM（24.80 vs 16.53），显示出对复杂专业动作的细粒度理解。
- 在Mo-RepCount的OBZ指标上LLaMo达到0.222，优于所有专用计数模型，证明其捕捉细粒度运动特征的能力。
- MoVid-Bench-Motion 上 Overall Acc. / Score = 55.32 / 3.67
---

# LLaMo Human Motion Instruction Tuning

> [!tip] 核心洞察
> 保留原始运动数据作为连续特征而不进行离散化，借助文本感知的关键帧压缩和特征对齐，能够更精准地捕捉人类动作的时空动态细节，从而提升在运动密集型场景下的行为分析和理解能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | LLaMo：人体运动指令微调 |
| 英文题名 | LLaMo Human Motion Instruction Tuning |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | LLaMo |
| Dataset | MoVid-Bench-Motion, MoVid-Bench-Video, BABEL-QA, profession-swing |

> [!tip] 效果简介
> - MoVid-Bench-Motion 上，Overall Acc. / Score 55.32 / 3.67 vs best competitor (GPT-3.5/MotionLLM) (outperformed most metrics)。
> - MoVid-Bench-Video 上，Overall Acc. / Score 52.33 / 3.10 vs best competitor (GPT-3.5/MotionLLM) (outperformed most metrics)。
> - BABEL-QA 上，Overall Score 0.458 vs best baseline (MotionLLM approx. 0.456) (+0.002 (approx.))。

## 概述

**核心问题与瓶颈**
现有将运动数据引入大语言模型（LLM）的方法——如 **MotionGPT**（Chen et al., NeurIPS 2024）和 **MotionLLM**（Chen et al., arXiv 2024）——普遍将连续的运动序列离散化为语言 token 或文本描述。这一转换不可避免地丢失了细粒度的时空运动信息，并且难以有效融合视频环境上下文，制约了模型对复杂人类行为的深度理解。

**核心思路**
LLaMo 提出将运动数据作为独立模态，以原生连续特征的形式直接输入 LLM。其核心创新 **Cross Talker 模块** 通过文本引导的自适应关键帧选择，将长运动序列压缩为少量关键帧，在保留运动细节的同时将自注意力计算复杂度从 $O((L_T+T)^2)$ 降至 $O((L_T+K)^2)$（$K \ll T$）。该模块进一步执行双向跨模态融合，使文本与运动特征在语义层面深度对齐。

**方法定位**
LLaMo 属于**多模态大语言模型（MLLM）在人体运动理解领域**的前沿工作。其架构包含三个核心模块：（1）多模态特征提取，支持视频和运动数据的直接输入；（2）Cross Talker，实现文本感知的运动关键帧选择与跨模态融合；（3）行为生成，基于融合特征输出行为文本描述。与 MotionGPT 的 token 化路线和 MotionLLM 的文本化路线形成鲜明对比，LLaMo 开辟了“原生运动表示 + 跨模态注意力融合”的新技术路径。

**主要结果**
- 在 **MoVid-Bench** 的运动和视频两个子基准上，LLaMo 在多数指标上超越 GPT-3.5、MotionLLM、Video-LLaVA 等基线。
- 在 **BABEL-QA** 上取得最高综合得分 0.458，优于所有对比方法。
- 在专业挥杆数据集上，LLaMo 综合准确率达 **24.80**，显著领先 MotionLLM 的 16.53（+8.27），展现出对复杂专业动作的细粒度理解。
- 在重复动作计数基准 **Mo-RepCount** 的 OBZ 指标上达到 **0.222**，超越所有专用计数模型（如 EScounts 的 0.198），证明了其捕捉细粒度运动特征的能力。

**局限与展望**
当前跨模态融合技术仍需细化以适应更复杂的真实环境，计算效率尚不足以支持实时应用。在部分重复动作计数指标上未能全面超越专用模型，表明时序精细计数仍有提升空间。未来可探索向医疗康复、虚拟人交互等领域的扩展。

## 背景与动机

### 人体运动理解的模态鸿沟

理解视频中的人体行为是计算机视觉的核心任务之一，涉及动作识别、时序定位、运动生成等多个子方向。近年来，大语言模型（LLM）在自然语言处理领域取得的突破，催生了一系列将视觉信息引入LLM的多模态方法。然而，在人体运动这一特定领域，现有方案普遍面临一个根本性瓶颈：**运动数据的表示方式与LLM的文本处理范式之间存在不可调和的模态鸿沟**。

具体而言，以 **MotionGPT**（Chen et al., NeurIPS 2024）和 **MotionLLM**（Chen et al., arXiv 2024）为代表的现有方法，倾向于将连续的运动数据转换为离散的语言token或文本描述，再送入LLM进行处理。这种“运动→文本”的转换策略虽然实现了模态统一，却不可避免地**丢失了细粒度的时空运动信息**——关节角度、速度变化、动作节奏等关键细节在离散化过程中被严重压缩。此外，这些方法往往缺乏对视频环境上下文的有效融合能力，导致模型难以理解复杂人类行为中动作与场景的耦合关系。

### 现有方法的三个关键缺口

1. **运动细节的表示损失**：将连续运动序列离散化为token的过程，本质上是对高维时空信号的降采样。对于需要精确捕捉关节运动轨迹、力度变化和时序依赖的任务（如体育动作分析、重复动作计数），这种信息损失是致命的。

2. **跨模态融合的浅层化**：现有方案或独立处理运动、视频、文本模态，或仅在特征层面进行简单拼接，缺乏**文本引导的自适应跨模态注意力机制**。这意味着模型无法根据语言查询动态地关注运动序列中的关键帧，也无法在运动和文本之间建立双向的细粒度对齐。

3. **计算效率与细节保留的矛盾**：全序列自注意力的计算复杂度为 $O((L_T+T)^2)$（其中 $L_T$ 为文本token数，$T$ 为运动帧数），当处理长时序运动数据时计算开销急剧增长。现有方法缺乏有效的帧选择策略来在保留关键运动信息的同时降低计算负担。

### LLaMo的动机与设计哲学

针对上述缺口，LLaMo提出了一个根本性的设计转变：**将运动数据作为独立模态直接输入LLM，保留其原生连续特征表示**。这一选择的核心洞察在于——运动数据的价值恰恰蕴藏在其连续性之中，任何形式的离散化都会不可逆地损害模型对时空动态的感知能力。

在此基础上，LLaMo通过两个关键创新来解决跨模态融合与计算效率的问题：

- **Cross Talker模块**：一种文本引导的自适应关键帧选择与双向跨模态融合机制。它利用文本查询动态识别运动序列中与语义最相关的关键帧，并在这些关键帧周围构建自适应局部上下文窗口进行特征聚合，最终通过双向交叉注意力实现运动与文本特征的深度融合。

- **运动估计器与特征增强器**：支持视频和运动数据的直接输入，当仅有视频时可通过运动估计器提取运动信息，确保模型在多种输入条件下均能保持对运动细节的感知能力。

这种设计使LLaMo能够在保留运动时空细节的前提下，将有效序列长度从 $T$ 压缩至 $K$（$K \ll T$），将自注意力复杂度降至 $O((L_T+K)^2)$，从而在**细粒度运动理解与计算效率之间取得平衡**。

## 核心创新

LLaMo 的核心创新在于**将运动数据作为独立模态原生引入大语言模型**，并通过**文本引导的跨模态关键帧压缩与双向融合机制**，在保留细粒度时空运动信息的同时大幅降低计算复杂度，从而显著提升模型在运动密集型场景下的行为理解能力。

### 1. 原生运动模态表示

现有方法（如 **MotionGPT**（Chen et al., NeurIPS 2024）、**MotionLLM**（Chen et al., arXiv 2024））将运动数据转换为语言 token 或文本描述，导致细粒度时空运动信息丢失。LLaMo 改变了这一范式：

- **Changed Slot：运动数据表示** — 从“转换为语言 token 或文本描述”改为“保留原生连续运动特征，作为独立模态输入”（[Abstract]）。这一设计使得运动特有的时空动态细节（如速度变化、关节角度时序）得以完整保留，避免了离散化过程中的信息损失。

### 2. Cross Talker：文本引导的跨模态融合

LLaMo 提出了 **Cross Talker 模块**，实现文本引导的自适应关键帧选择与双向跨模态融合，是方法的核心计算与表征创新：

- **Changed Slot：模态交互与融合** — 从“独立处理运动或视频，缺乏跨模态注意力”改为“通过 Cross Talker 进行文本引导的关键帧选择、自适应局部/全局注意力及双向跨模态融合”（[Sec. 3.2]）。具体而言，Cross Talker 首先计算文本 token 与运动帧之间的交叉注意力矩阵 $A = \mathrm{Softmax}\left( \frac{ F_T W_Q (\tilde{F}_M W_K)^\top }{ \sqrt{d} } \right)$，再通过最大池化 $s_j = \max_{i} A_{i,j}$ 获得每帧的重要性得分，从而选出与文本语义最相关的 $K$ 个关键帧。

- **Changed Slot：序列计算复杂度** — 从全序列自注意力的 $O((L_T+T)^2)$ 降至 $O((L_T+K)^2)$，其中 $K \ll T$（[Sec. 3.2]）。这一压缩机制使得模型在长时序运动数据上仍可高效运行。

- 选出的关键帧进一步通过自适应局部窗口 $W_k = \{ j \mid |j - k| \le r_k \times T \}$ 聚合上下文特征，再与分段级全局特征融合，最终通过双向交叉注意力与文本特征对齐，形成融合表征 $F_{\mathrm{fusion}} = [ F_T ; \{ F_M(k) \}_{k \in K} ]$。

### 3. 视频与运动双模态协同

- **Changed Slot：视频输入处理** — 从“仅支持运动或视频单一模态”改为“同时支持原始视频和运动数据的直接输入，并通过运动估计器从视频中提取运动信息”（[Sec. 3.1]）。当运动数据不可用时，运动估计器可从视频帧中估计运动特征，增强了模型的场景适应性。视频特征通过交叉注意力进一步丰富运动表示，使模型能够融合环境上下文进行更全面的行为分析。

### 4. 创新有效性验证

上述创新在多个基准上得到验证：

- 在 **MoVid-Bench** 上，LLaMo 在 Motion 和 Video 两个子集上均取得最优整体准确率（55.32 / 52.33）和得分（3.67 / 3.10），全面超越 GPT-3.5、MotionGPT 和 MotionLLM（[Table 1]）。
- 在 **BABEL-QA** 上，LLaMo 以 0.458 的整体得分取得最高（[Table 2]）。
- 在 **专业挥杆数据集** 上，LLaMo 的综合准确率达 24.80，大幅领先 MotionLLM 的 16.53（+8.27）（[Table 3]），证明其对复杂专业动作的细粒度理解能力。
- 在 **Mo-RepCount** 的 OBZ 指标上，LLaMo 达到 0.222，超越所有专用计数模型（如 **EScounts**（Sinha et al., arXiv 2024）的 0.198），显示出原生运动表示在捕捉细粒度运动特征上的独特优势（[Table 4]）。

## 整体框架

LLaMo 的整体设计围绕一个核心洞察展开：**保留原始运动数据作为连续特征而非将其离散化为语言 token，能够更精准地捕捉人类动作的时空动态细节**。为此，LLaMo 将运动数据作为独立模态直接输入大语言模型（LLM），并通过三个协同模块构建起从多模态感知到行为语言生成的端到端流水线（Figure 2）。

![[assets/figures/papers/paper_list_l1860_LLaMo_Human_Motion_Instruction_Tuning/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the LLaMo framework. It includes three main modules: (1) Multimodal Feature Extraction for encoding video and motion data; (2) Cross Talker for aligning and fusing motion and text features; and (3) Behavior Generation Module to produce text descriptions of human behavior based on integrated features*

### 流水线概览

LLaMo 框架由以下三个主模块串联而成：

1. **多模态特征提取模块（Multimodal Feature Extraction）**  
   负责编码视频与运动数据，并进行特征增强。该模块同时支持原始视频帧和运动数据的直接输入，并内置运动估计器（Motion Estimator），可在仅有视频而缺少显式运动数据的场景下，从视频帧中估计运动信息。

2. **跨模态对话模块（Cross Talker）**  
   这是 LLaMo 的核心创新组件。它接收增强后的视频/运动特征与文本指令特征，执行文本引导的关键帧选择、自适应上下文聚合以及双向跨模态融合，最终输出文本感知的细粒度运动表示。

3. **行为生成模块（Behavior Generation）**  
   基于融合后的多模态特征，调用语言模型生成描述观察到的行为的文本序列。

### 特征提取与增强

给定视频帧序列 $V$ 和运动数据 $M$，首先通过各自的编码器提取特征：

$$F_V = f_v(V) = \{ f_v(v_1), f_v(v_2), \dots, f_v(v_T) \}$$

$$F_M = f_m(M) = \{ f_m(m_1), f_m(m_2), \ldots, f_m(m_T) \}$$

随后，视频特征 $F_V$ 和运动特征 $F_M$ 分别经过自注意力操作以捕获时序依赖，得到增强特征 $F_V'$ 和 $F_M'$。为了进一步利用视频中的语义信息来丰富运动表示，LLaMo 设计了一个交叉注意力块，以增强后的运动特征作为 Query，从视频特征中提取有效的语义信息，生成最终的增强运动特征 $\tilde{F}_M$。

### Cross Talker：文本引导的跨模态融合

Cross Talker 模块（Figure 3）是连接运动感知与语言理解的关键桥梁，其工作流程分为三步：

**第一步：语言引导的帧选择（Language-Guided Frame Selection）**  
通过文本 token 特征 $F_T$ 与运动帧特征 $\tilde{F}_M$ 之间的交叉注意力，计算注意力矩阵：

$$A = \mathrm{Softmax}\left( \frac{ F_T W_Q (\tilde{F}_M W_K)^\top }{ \sqrt{d} } \right)$$

对每个运动帧 $j$，取其在所有文本 token 上的最大注意力值作为重要性得分：

$$s_j = \max_{i=1,\dots,L_T} A_{i,j}$$

根据得分排序选择 top-$K$ 个关键帧，将有效运动序列长度从 $T$ 压缩至 $K$（$K \ll T$），从而将自注意力复杂度从 $O((L_T+T)^2)$ 降至 $O((L_T+K)^2)$。

**第二步：自适应上下文聚合（Adaptive Contextual Feature Aggregation）**  
对每个关键帧 $k$，模型预测一个感受野大小 $r_k$，定义其局部上下文窗口：

$$W_k = \{ j \mid |j - k| \le r_k \times T \}$$

在局部窗口内通过自注意力增强关键帧特征：

$$F_{\mathrm{local}}(k) = \tilde{F}_M(k) + \mathrm{Attention}(\tilde{F}_M(k), \tilde{F}_M(W_k), \tilde{F}_M(W_k))$$

随后将局部特征与分段级别的全局特征 $F_M^{\mathrm{seg}}$ 进行注意力融合：

$$F_{\mathrm{global}}(k) = F_{\mathrm{local}}(k) + \mathrm{Attention}(F_{\mathrm{local}}(k), F_M^{\mathrm{seg}}, F_M^{\mathrm{seg}})$$

**第三步：双向跨模态融合（Bidirectional Cross-Modal Fusion）**  
将文本特征与全局增强后的关键帧特征进行双向交叉注意力——运动特征作为 Query、文本特征作为 Key/Value，反之亦然——最终将两者拼接形成融合特征：

$$F_{\mathrm{fusion}} = [ F_T ; \{ F_M(k) \}_{k \in K} ]$$

### 行为生成与训练

融合特征 $F_{\mathrm{fusion}}$ 被送入语言模型解码器，生成行为描述文本序列：

$$Y = h(F_{\mathrm{fusion}}) = \{ y_1, y_2, \dots, y_L \}$$

训练采用标准的负对数似然损失，优化生成 token 与真实标签之间的差距：

$$L = -\frac{1}{N}\sum_{i=1}^N \sum_{t=1}^{L^{(i)}} \log p(\hat{y}_t^{(i)} \mid \hat{y}_{1:t-1}^{(i)}, F_{\mathrm{fusion}}^{(i)})$$

### 设计优势总结

与 MotionGPT 将运动转换为语言 token、MotionLLM 将运动转为文本描述的做法不同，LLaMo 的框架设计带来了三个关键优势：

- **运动细节保真**：原生连续运动表示避免了离散化带来的细粒度时空信息损失。
- **计算效率**：文本引导的关键帧选择机制大幅压缩序列长度，降低自注意力计算开销。
- **多模态兼容**：同时支持视频和运动数据的直接输入，并通过运动估计器覆盖无运动数据的场景。

### 补充图表

![[assets/figures/papers/paper_list_l1860_LLaMo_Human_Motion_Instruction_Tuning/figures/001_Figure_1.jpg]]
*Figure 1: A comparison of MotionLLM [1], MotionGPT [2], and LLaMo highlights LLaMo’s motion-specific capabilities. Equipped with a Motion Enhancer and Cross Talker module to align motion and text, LLaMo supports both video and motion inputs, enabling text-aware, fine-grained motion analysis*

## 核心模块与公式推导

LLaMo 的核心架构由三个模块串联构成（Figure 2）：**多模态特征提取模块**、**Cross Talker 模块**和**行为生成模块**。其中，Cross Talker 是实现文本引导运动细粒度理解的关键创新。

### 多模态特征提取

该模块负责将视频和运动数据编码为统一特征空间中的表示。

对于视频输入 $V = \{v_1, v_2, \dots, v_T\}$，视频编码器提取逐帧视觉特征：

$$F_V = f_v(V) = \{ f_v(v_1), f_v(v_2), \dots, f_v(v_T) \}$$

对于运动数据 $M = \{m_1, m_2, \dots, m_T\}$，运动编码器提取运动特征：

$$F_M = f_m(M) = \{ f_m(m_1), f_m(m_2), \ldots, f_m(m_T) \}$$

当仅有视频输入而无显式运动数据时，LLaMo 内置的**运动估计器**可直接从视频帧中估计运动信息，确保模型在运动数据缺失场景下仍可运行。随后，视频特征和运动特征分别经过自注意力操作，捕获各自序列内部的时序依赖关系，得到增强特征 $F_V'$ 和 $F_M'$。为进一步利用视频中的语义信息补充运动表示，模型引入一个交叉注意力块，以增强后的运动特征作为 Query，从视频特征中提取有效语义信息，得到最终的增强运动特征 $\tilde{F}_M$。

### Cross Talker 模块

Cross Talker 是 LLaMo 的核心创新模块（Figure 3），通过文本引导实现关键帧选择与跨模态融合，在保留细粒度运动信息的同时大幅降低计算复杂度。该模块包含三个子步骤。

![[assets/figures/papers/paper_list_l1860_LLaMo_Human_Motion_Instruction_Tuning/figures/003_Figure_3.jpg]]
*Figure 3: Overview of the Cross Talker Module, which selects key frames based on text guidance and fuses them with text features for enhanced analysis*

**第一步：语言引导的帧选择。** 给定文本 token 特征 $F_T \in \mathbb{R}^{L_T \times d}$ 和增强运动特征 $\tilde{F}_M \in \mathbb{R}^{T \times d}$，通过交叉注意力计算文本与运动帧之间的关联矩阵：

$$A = \mathrm{Softmax}\left( \frac{ F_T W_Q (\tilde{F}_M W_K)^\top }{ \sqrt{d} } \right)$$

其中 $W_Q, W_K$ 为可学习的投影矩阵，$d$ 为特征维度。矩阵 $A \in \mathbb{R}^{L_T \times T}$ 的每个元素 $A_{i,j}$ 表示第 $i$ 个文本 token 对第 $j$ 个运动帧的关注程度。随后，对每个运动帧取其在所有文本 token 上的最大注意力作为重要性得分：

$$s_j = \max_{i=1,\dots,L_T} A_{i,j}$$

根据得分排序，选择 top-$K$ 个关键帧（$K \ll T$），将有效运动序列长度从 $T$ 压缩至 $K$，从而将后续自注意力的计算复杂度从 $O((L_T+T)^2)$ 降至 $O((L_T+K)^2)$。

**第二步：自适应上下文聚合。** 对于每个选中的关键帧 $k$，模型预测其感受野大小 $r_k$，据此定义局部上下文窗口：

$$W_k = \{ j \mid |j - k| \le r_k \times T \}$$

在该窗口内，通过自注意力增强关键帧的局部特征：

$$F_{\mathrm{local}}(k) = \tilde{F}_M(k) + \mathrm{Attention}(\tilde{F}_M(k), \tilde{F}_M(W_k), \tilde{F}_M(W_k))$$

随后，将局部特征与分段级别的全局运动特征 $F_M^{\mathrm{seg}}$ 进行注意力融合：

$$F_{\mathrm{global}}(k) = F_{\mathrm{local}}(k) + \mathrm{Attention}(F_{\mathrm{local}}(k), F_M^{\mathrm{seg}}, F_M^{\mathrm{seg}})$$

这种“局部-全局”两级聚合机制使模型既能关注关键帧周围的细粒度时序上下文，又能捕获长程运动模式。

**第三步：双向跨模态融合。** 在获得关键帧的全局增强特征后，模型执行运动特征与文本特征之间的双向交叉注意力——运动特征作为 Query、文本特征作为 Key/Value，反之亦然——实现深层的跨模态语义对齐。最终，将文本特征与选出的关键运动帧特征拼接，形成融合表示：

$$F_{\mathrm{fusion}} = [ F_T ; \{ F_M(k) \}_{k \in K} ]$$

### 行为生成与训练

融合特征 $F_{\mathrm{fusion}}$ 被送入语言模型解码器，自回归地生成行为描述序列：

$$Y = h(F_{\mathrm{fusion}}) = \{ y_1, y_2, \dots, y_L \}$$

模型通过标准的负对数似然损失进行端到端训练：

$$L = -\frac{1}{N}\sum_{i=1}^N \sum_{t=1}^{L^{(i)}} \log p(\hat{y}_t^{(i)} \mid \hat{y}_{1:t-1}^{(i)}, F_{\mathrm{fusion}}^{(i)})$$

其中 $N$ 为训练样本数，$L^{(i)}$ 为第 $i$ 个样本的标注序列长度，$\hat{y}_t^{(i)}$ 为第 $t$ 个目标 token。

### 关键设计总结

LLaMo 的核心技术决策在于**保留运动数据的连续原生表示**，而非将其离散化为语言 token。Cross Talker 通过文本感知的帧选择实现计算压缩，同时借助自适应局部窗口和双向跨模态注意力，确保压缩过程不丢失对细粒度时空动态的敏感性。这一设计在专业挥杆分析（All Score 24.80 vs. MotionLLM 16.53）和重复动作计数（OBZ 0.222 vs. 最佳专用模型 0.198）等运动密集型任务上得到了充分验证。

## 实验与分析

### 主要实验结果

LLaMo在多个基准上进行了系统评估，涵盖通用人体活动理解、专业运动分析和细粒度动作计数等场景。实验设置详见原文第4.1节，训练数据包括MoVid、Swing、HumanML3D、KIT-ML和Mo-RepCount等数据集。

**MoVid-Bench基准**（Table 1）同时评估了运动模态和视频模态下的表现。在MoVid-Bench-Motion上，LLaMo取得总体准确率55.32、综合得分3.67；在MoVid-Bench-Video上，总体准确率为52.33、综合得分3.10，在绝大多数指标上均超越GPT-3.5、MotionGPT（Chen et al., NeurIPS 2024）和MotionLLM（Chen et al., arXiv 2024）等基线模型。这一结果表明，保留原生运动连续特征并引入跨模态融合机制，能有效捕捉运动密集型场景中的时空细节。

**BABEL-QA数据集**（Table 2）侧重于运动语言理解。LLaMo取得0.458的总体得分，超越所有基线模型（MotionLLM约0.456），验证了文本引导的关键帧选择策略在运动-语言对齐任务中的有效性。

**专业挥杆数据集**（Table 3）是体现细粒度运动理解能力的关键场景。LLaMo综合准确率（All Score）达到24.80，大幅领先MotionLLM的16.53（+8.27）。这表明Cross Talker模块通过自适应局部/全局注意力聚合，能够精准捕捉专业动作中的关键帧信息，从而显著提升对复杂行为模式的判别能力。

**Mo-RepCount重复动作计数**（Table 4）进一步检验模型对运动细节的敏感性。LLaMo在OBZ指标上达到0.222，优于所有专用计数模型（最佳基线EScounts为0.198），证明其原生运动表示在细粒度时序特征捕获方面具有独特优势。但需注意，LLaMo在部分计数指标上并未全面超越EScounts、PoseRAC等专用模型，说明在纯时序精度方面仍有提升空间。

### 消融实验

分析材料中未提供系统消融实验的具体数据，无法确认各模块（如Cross Talker的关键帧选择、自适应窗口聚合、双向跨模态融合等）的独立贡献度。该部分需结合原文手动核实。

### 失败模式与局限性

1. **时序精细计数不足**：在Mo-RepCount的某些指标上，LLaMo未能全面超越专用计数模型（如EScounts、PoseRAC），表明模型在处理需要精确时序定位的重复动作时仍存在瓶颈。
2. **场景泛化性有限**：实验主要集中于运动密集型场景（体育分析、专业挥杆），在更广泛的行为理解任务（如日常活动、医疗康复）上的泛化能力尚未验证。
3. **计算效率约束**：尽管Cross Talker将自注意力复杂度从$O((L_T+T)^2)$降至$O((L_T+K)^2)$，但当前方法仍不足以支持实时应用，跨模态融合效率需进一步优化。
4. **复杂环境适应性不足**：跨模态集成技术在真实复杂环境（如遮挡、多人物交互）下的鲁棒性需要进一步验证。

### 关键图表结论

- **Figure 4 / Table 1**：LLaMo在MoVid-Bench的运动和视频两个子基准上均取得最优结果，验证了同时支持双模态输入和原生运动表示的优势。
- **Table 2**：BABEL-QA上的最高总体得分证明了文本引导关键帧选择对运动-语言对齐的有效性。
- **Table 3**：专业挥杆数据集上对MotionLLM的大幅领先（+8.27）是细粒度运动理解能力的最有力证据。
- **Table 4**：OBZ指标超越专用模型，表明LLaMo在捕捉运动细节方面具有独特优势，但其他指标上的差距也揭示了时序精度的局限性。

![[assets/figures/papers/paper_list_l1860_LLaMo_Human_Motion_Instruction_Tuning/figures/007_Figure_4.jpg]]
*Figure 4: Example outputs from LLaMo across human activities and professional sports, showcasing its reasoning capabilities and domainspecific knowledge in motion-intensive scenarios*

![[assets/figures/papers/paper_list_l1860_LLaMo_Human_Motion_Instruction_Tuning/figures/008_Table_2.jpg]]
*Table 2: Comparison on BABEL-QA dataset. Higher scores indicate better performance*

![[assets/figures/papers/paper_list_l1860_LLaMo_Human_Motion_Instruction_Tuning/figures/009_Table_3.jpg]]
*Table 3: Performance on the profession-swing dataset across four indicators. Higher accuracy and score values indicate better performance*

![[assets/figures/papers/paper_list_l1860_LLaMo_Human_Motion_Instruction_Tuning/figures/010_Table_4.jpg]]
*Table 4: Motion and video details capture evaluation on Mo-RepCount*

## 方法谱系与知识库定位

### 1. 方法谱系：从运动离散化到原生模态保留

LLaMo 处于**多模态大语言模型（MLLM）与人体运动理解**的交叉地带。其核心定位源于对现有路线的根本性背离：

- **运动token化路线**：以 **MotionGPT**（Chen et al., NeurIPS 2024）为代表，将连续运动数据转换为离散语言token，使LLM能以统一的自回归方式处理。但该转换过程不可避免地丢失细粒度时空运动信息。
- **文本描述化路线**：以 **MotionLLM**（Chen et al., arXiv 2024）为代表，将运动数据转化为文本描述再输入LLM，同样面临信息压缩损失。
- **通用视频-语言路线**：以 **Video-LLaVA**（Lin et al., arXiv 2023）和 **Chat-UniVi**（Jin et al., CVPR 2024）为代表，虽能处理视频输入，但缺乏对运动模态的专门建模，在运动密集型场景中理解能力不足。

LLaMo 的关键突破在于**将运动数据作为独立连续模态直接注入LLM**，无需任何离散化或文本化转换。这一设计选择构成了其与前述所有路线的根本分界线，使得原生运动特征中的时序动态和空间细节得以完整保留。

在重复动作计数这一细分领域，LLaMo 与专用模型形成对比：**RepNet**（Wandt et al., CVPR 2019）、**TransRAC**（Hu et al., CVPR 2022）、**PoseRAC**（Yao et al., arXiv 2023）和 **EScounts**（Sinha et al., arXiv 2024）均为针对计数任务设计的专用架构，而LLaMo以通用行为理解框架在OBZ指标上超越了这些专用模型，显示出其运动特征提取的通用性和细粒度。

### 2. 知识库定位：跨模态融合与计算效率的平衡点

LLaMo 的知识贡献集中在三个相互关联的技术决策上：

**（1）文本引导的自适应关键帧选择**：通过计算文本token与运动帧之间的交叉注意力矩阵 $A = \mathrm{Softmax}\left( \frac{ F_T W_Q (\tilde{F}_M W_K)^\top }{ \sqrt{d} } \right)$，并对每个运动帧取最大注意力得分 $s_j = \max_{i=1,\dots,L_T} A_{i,j}$，实现由语言查询驱动的运动帧重要性排序。这一机制使模型能根据具体问题动态聚焦相关帧，而非被动处理全序列。

**（2）自适应局部-全局上下文聚合**：为每个选出的关键帧预测感受野大小 $r_k$，定义局部窗口 $W_k = \{ j \mid |j - k| \le r_k \times T \}$，先进行局部自注意力增强，再与分段级全局特征融合。这既保留了关键帧周围的精细时序上下文，又捕获了跨分段的宏观运动模式。

**（3）双向跨模态融合与复杂度控制**：将文本特征与选出的$K$个关键运动帧特征拼接为 $F_{\mathrm{fusion}} = [ F_T ; \{ F_M(k) \}_{k \in K} ]$，并通过双向交叉注意力实现深度融合。同时，自注意力复杂度从全序列的 $O((L_T+T)^2)$ 降至 $O((L_T+K)^2)$，其中 $K \ll T$，在保留关键信息的前提下大幅降低计算开销。

### 3. 适用边界与局限

**已验证的适用场景**：
- 运动密集型人类活动识别（MoVid-Bench-Motion 综合准确率 55.32）
- 视频环境下的人类行为理解（MoVid-Bench-Video 综合准确率 52.33）
- 专业体育动作的细粒度分析（profession-swing 综合得分 24.80 vs MotionLLM 16.53）
- 重复动作计数（Mo-RepCount OBZ 指标 0.222）

**已知局限**（需人工验证具体边界）：
- **跨模态集成细化不足**：当前跨模态融合技术尚不能完全适应复杂真实环境中的多变条件，如遮挡、多人物交互等场景下的鲁棒性有待验证。
- **实时性不足**：尽管通过关键帧选择降低了计算复杂度，但整体流程的计算效率仍不足以支持实时应用。
- **时序精细计数仍有差距**：在Mo-RepCount的部分指标上未能全面超越专用计数模型（如EScounts、PoseRAC），表明在纯时序维度的精细计数方面仍有提升空间。
- **场景泛化性未充分验证**：实验集中在体育分析等运动密集型场景，在医疗康复、日常行为理解等更广泛任务上的表现尚不明确。

### 4. 开放问题

1. **领域扩展**：LLaMo的原生运动表示和跨模态融合机制能否迁移至医疗康复（如步态分析）、虚拟人交互（如手势识别）等需要精细运动理解的领域？
2. **效率优化**：如何进一步压缩关键帧选择与跨模态融合的计算开销，以满足实时应用（如在线体育教学反馈）的延迟要求？
3. **单模态鲁棒性**：在仅有运动数据而无视频输入的条件下，模型能否保持同等的细粒度理解能力？这直接关系到该方法在无摄像头场景（如可穿戴传感器）中的适用性。
4. **更复杂行为的理解**：当前方法主要处理单人动作，如何扩展到多人交互、群体行为等更复杂的运动场景？

## 原文 PDF

![[paperPDFs/CVPR_2025/LLaMo_Human_Motion_Instruction_Tuning.pdf]]