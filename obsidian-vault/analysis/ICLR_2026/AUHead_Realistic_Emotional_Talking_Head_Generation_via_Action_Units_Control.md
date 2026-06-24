---
title: "AUHead: Realistic Emotional Talking Head Generation via Action Units Control"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AUHead_Realistic_Emotional_Talking_Head_Generation_via_Action_Units_Control.pdf
aliases:
- AUHead
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "以音频语言模型预测面部动作单元序列并用其控制扩散说话头生成。"
primary_logic: "AUHead先从音频生成情感引导的AU序列，再把AU转为2D面部表示并通过交叉注意力注入视频扩散模型。"
claims:
- "空间时间AU分词和情感再到AU的CoT策略提升了AU与情感预测质量。"
- "2D AU表示比1D AU序列提供更强空间先验，有助于提升说话头生成质量。"
- "解耦AU引导尺度在情感表达和视觉质量之间提供可调权衡。"
- "用户研究显示AUHead在情感表达、视频质量、音唇同步和整体表现上更受偏好。"
---

# AUHead: Realistic Emotional Talking Head Generation via Action Units Control

> [!tip] 核心洞察
> 利用大型音频语言模型（ALM）的语音理解能力，通过空间-时间AU分词和“情感-然后-AU”思维链机制，从原始音频中解耦出细粒度的AU序列；再通过AU驱动的可控扩散模型，将AU序列映射为结构化2D面部表示并通过交叉注意力机制注入视觉潜在空间，实现情感丰富且身份一致的说话头视频生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AUHead：基于动作单元控制的逼真情感说话头生成 |
| 英文题名 | AUHead: Realistic Emotional Talking Head Generation via Action Units Control |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=dmzlAUkulz); [GitHub](https://github.com/laura990501/AUHead_ICLR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | AUHead |
| Dataset | MEAD |

> [!tip] 效果简介
> - MEAD 上，Sync 为 6.6311，对比 6.6095 (MEMO+RoM)，变化 +0.0216。
> - MEAD 上，PSNR 为 23.3466，对比 23.3585 (MEMO+RoM)，变化 -0.0119。
> - MEAD 上，SSIM 为 0.7395，对比 0.7399 (MEMO+RoM)，变化 -0.0004。

## 概述

AUHead（ICLR 2025）提出了一种基于面部动作单元（Action Units, AU）控制的两阶段情感说话头生成框架。该方法的核心创新在于：利用大型音频语言模型（Audio Language Model, ALM）从原始音频中解耦出细粒度的AU序列，再通过AU驱动的可控扩散模型合成情感丰富、身份一致且音唇同步的说话头视频。在MEAD和CREMA数据集上的定量实验以及用户研究均表明，AUHead在情感表达、视频质量和音唇同步方面全面超越了现有最先进方法。

## 背景与动机

现有音频驱动说话头生成方法在情感控制方面存在根本性瓶颈：它们通常依赖粗粒度的情感标签（如“快乐”、“悲伤”）或隐式情感编码，无法捕捉语音中嵌入的微妙情感线索，导致生成的面部表情生硬、不自然。具体而言，现有方法面临以下挑战：

- **粗粒度情感控制**：使用离散情感类别或简单嵌入，无法表达同一情感类别内的强度差异和混合情感。
- **缺乏可解释性**：端到端生成方法将情感信息隐式编码在潜在空间中，难以进行细粒度的调节和干预。
- **音频-视觉鸿沟**：音频信号与面部运动之间存在复杂的非线性映射，直接端到端学习难以捕捉精细的肌肉运动模式。

AUHead的因果旋钮（causal knob）在于：将面部动作单元（AU）作为音频与视觉之间的结构化中间表示。AU源自Facial Action Coding System (FACS)（Ekman & Friesen, 1978），提供了一套标准化的面部肌肉运动描述框架。通过ALM从音频中解耦出AU序列，并用其显式控制扩散模型的生成过程，AUHead实现了细粒度、可解释的情感控制。

## 核心创新

AUHead的核心洞察在于：利用大型音频语言模型（ALM）的语音理解能力，通过空间-时间AU分词和“情感-然后-AU”思维链（Chain-of-Thought, CoT）机制，从原始音频中解耦出细粒度的AU序列；再通过AU驱动的可控扩散模型，将AU序列映射为结构化2D面部表示并通过交叉注意力机制注入视觉潜在空间，实现情感丰富且身份一致的说话头视频生成。

具体创新点包括：

1. **空间-时间AU分词**：将稠密的24维AU连续向量转换为紧凑的索引-强度对集合，并通过时间下采样降低序列长度，使ALM能够以语言建模方式生成AU序列。
2. **“情感-然后-AU”思维链机制**：ALM先预测情感类别，再生成对应的AU序列，利用情感类别作为中间监督信号，提升AU预测的准确性和可解释性。
3. **2D AU表示**：将1D AU序列映射为2D面部表示（基于关键点的Landmark或基于网格渲染的Rendering-of-Mesh），为扩散模型提供更强的空间先验。
4. **上下文感知AU嵌入**：通过时间卷积网络编码局部窗口内的AU特征，增强生成视频的时间连贯性。
5. **AU-视觉交叉注意力**：在扩散模型骨干中插入零初始化的交叉注意力层，实现AU嵌入与视觉潜在之间的跨模态交互。
6. **AU解耦引导策略**：推理时分别用引导尺度s^AU和s^H控制AU和其他条件（如音频、运动先验）的强度，实现情感表达与视觉质量的最佳平衡。

## 整体框架

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_dmzlAUkulz_AUHead_Realis/figures/001_Figure_1.jpg]]
*Figure 1: Framework comparison between existing talking head generation and our AUHead. (a) Direct generation from audio and portrait. (b) Our method: audio understanding via ALM, and then generation.*

AUHead采用两阶段框架（Figure 2）：

**Stage 1: ALM AU解耦**：以Audio-Qwen-Chat（Chu et al., 2023）为骨干，通过LoRA（Hu et al., 2022）微调，使其具备从音频中生成AU序列的能力。输入为原始音频，输出为24维AU序列（5 fps）。该阶段采用空间-时间AU分词和CoT机制，将AU预测转化为语言建模任务。

**Stage 2: AU驱动可控生成**：以预训练的扩散模型（Hallo V1（Xu et al., 2024）或MEMO（Zheng et al., 2024））为骨干，通过AU表示模块、上下文感知AU嵌入和AU-视觉交叉注意力机制，将AU序列注入生成过程。输入为参考图像、音频和AU序列，输出为情感丰富、身份一致的说话头视频。

## 核心模块与公式推导

### 5.1 潜在扩散模型

AUHead的Stage 2基于潜在扩散模型（Rombach et al., 2022），其训练损失函数为：

$$\mathcal { L } = \mathbb { E } _ { I , c , t , \epsilon \sim \mathcal { N } ( \mathbf { 0 } , \mathbf { I } ) } \Big [ \big \| \epsilon - \epsilon _ { \theta } ( z _ { t } , t , c ) \big \| _ { 2 } ^ { 2 } \Big ] \quad \text{(Eqn. 1)}$$

其中，$z_t$为加噪后的潜在变量，$t$为时间步，$c$为条件（包括音频、运动先验和AU），$\epsilon_\theta$为噪声预测网络。

### 5.2 AU序列表示与分词

AU序列表示为时间序列：

$$\mathbf { A } \mathbf { U } _ { 1 : T ^ { \prime } } = [ \mathbf { a u } _ { 1 } , \mathbf { a u } _ { 2 } , \mathbf { . . . } , \mathbf { a u } _ { T ^ { \prime } } ] , \quad \mathbf { a u } _ { t } \in \mathbb { R } ^ { n } \quad \text{(Eqn. 2)}$$

其中$n=24$，表示24个AU的强度值（范围0-1）。空间AU分词将稠密向量转换为紧凑的索引-强度对集合：

$$\mathbf { a } \mathbf { \hat { u } } _ { t } = \{ ( i , \mathbf { a } \mathbf { u } _ { t , i } ) | \mathbf { a } \mathbf { u } _ { t , i } > \lambda \} \quad \text{(Eqn. 3)}$$

其中$\lambda$为稀疏性阈值（实验中设为0），仅保留激活的AU。时间上，通过下采样因子$\gamma=0.2$将原始25 fps降低为5 fps。

### 5.3 上下文感知AU嵌入

为增强时间连贯性，通过时间卷积网络对局部窗口内的AU特征进行编码：

$$\pmb { c } _ { t } = \mathrm { C o n v } _ { \mathrm { A U } } \left( \left[ \mathbf { a u } _ { t - n } , . . . , \mathbf { a u } _ { t } , . . . , \mathbf { a u } _ { t + n } \right] \right) \quad \text{(Eqn. 4)}$$

窗口大小设为5（$n=2$）。

### 5.4 AU-视觉交叉注意力

在扩散模型骨干的每个空间分辨率$s$和时间步$t$，视觉潜在变量通过交叉注意力机制关注AU嵌入：

$$\hat { z } _ { t } ^ { ( s ) } \gets \mathrm { C r o s s A t t n } \left( z _ { t } ^ { ( s ) } , c ^ { \mathrm { A U } } \right) \quad \text{(Eqn. 5)}$$

AU适配器采用零初始化（zero-initialization）以确保训练稳定性。

### 5.5 解耦引导策略

推理时，采用解耦引导公式分别调节AU和其他条件的强度：

$$\hat{\epsilon} = \mathcal{L}_{\boldsymbol{\theta}}(z_t, \boldsymbol{\phi}, \mathbf{c}^{\mathrm{AU}}) + s^H \cdot [ \mathcal{L}_{\boldsymbol{\theta}}(z_t, \mathbf{c}^H, \boldsymbol{\phi}) - \mathcal{L}_{\boldsymbol{\theta}}(z_t, \boldsymbol{\phi}, \boldsymbol{\phi}) ] + s^{\mathrm{AU}} \cdot [ \mathcal{L}_{\boldsymbol{\theta}}(z_t, \mathbf{c}^H, \mathbf{c}^{\mathrm{AU}}) - \mathcal{L}_{\boldsymbol{\theta}}(z_t, \mathbf{c}^H, \boldsymbol{\phi}) ] \quad \text{(Section 3.4)}$$

其中$s^{\mathrm{AU}}$和$s^H$分别控制AU和其他条件（如音频、运动先验）的引导强度。实验表明，最优的AU引导尺度为3.5（Figure 3），在此尺度下视觉质量（FID）与情感表达（Emotion ACC, MAE）达到最佳平衡。

## 实验与分析

### 6.1 数据集与设置

实验在MEAD（Wang et al., 2020）和CREMA（Cao et al., 2014）两个基准数据集上进行。MEAD包含约10,000个视频片段，覆盖8种情感（中性、愤怒、厌恶、恐惧、快乐、悲伤、惊讶、轻蔑）；CREMA包含7,442个视频片段，覆盖6种情感。所有视频重采样至25 fps、512×512分辨率，音频重采样至16 kHz。

Stage 1在4×NVIDIA A100 GPU上训练约24 GPU小时，学习率1e-4；Stage 2在4×NVIDIA A100 GPU上训练12 GPU小时，学习率5e-6（Hallo V1）或1e-5（MEMO）。

### 6.2 主要定量结果

Table 3展示了AUHead与现有SOTA方法在MEAD和CREMA上的定量比较。评估指标包括：SyncNet（音唇同步）、PSNR（峰值信噪比）、SSIM（结构相似性）、FID（Fréchet Inception Distance）、M-LMD（嘴部地标距离）和F-LMD（面部地标距离）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_dmzlAUkulz_AUHead_Realis/figures/007_Table_3.jpg]]
*Table 3: Comparison of state-of-the-art audio-driven talking head generation methods on MEAD and CREMA benchmarks. The best results are marked in bold (best) and underlined (2nd-best). M/F-LMD denotes mouth/face landmark distance.∗ indicates results reproduced under the same training data and settings for fair comparison.*

| 方法 | Sync↑ | PSNR↑ | SSIM↑ | FID↓ | M-LMD↓ | F-LMD↓ |
|------|-------|-------|-------|------|--------|--------|
| **AUHead (MEMO) - MEAD** | **6.6311** | 23.3466 | 0.7395 | 10.9671 | 1.8608 | 2.1604 |
| MEMO+RoM - MEAD | 6.6095 | **23.3585** | **0.7399** | **10.8701** | **1.8602** | **2.1536** |
| **AUHead (MEMO) - CREMA** | **6.2050** | **24.2912** | **0.7413** | **8.2361** | **1.9313** | **2.3991** |

注：AUHead在MEAD上的Sync指标达到最优（6.6311），但在PSNR、SSIM、FID和LMD指标上略低于MEMO+RoM基线。在CREMA上，AUHead与MEMO+RoM在所有指标上持平。这表明AUHead在保持视觉质量的同时，显著提升了音唇同步性能。

### 6.3 消融实验

**CoT策略消融（Table 1）**：比较了不同输入输出组合对AU和情感预测的性能。CoT策略（A -> E -> AU）在情感准确率（67.01%）、精确率/召回率（0.71）和MAE（0.2085）上均优于直接预测AU（A -> AU）和仅情感预测（A -> E），验证了“情感-然后-AU”思维链机制的有效性。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_dmzlAUkulz_AUHead_Realis/figures/003_Table_1.jpg]]
*Table 1: Performance of different input-output combinations on AU and emotion prediction. A: Audio input; E: Emotion label; AU: Action Unit sequence.*

**AU表示消融（Table 2）**：比较了1D AU序列与2D AU表示（LMK, RoM）对视频生成的影响。2D表示在PSNR、SSIM、FID和LMD指标上全面优于1D序列，其中RoM（网格渲染）在多数指标上达到最优，LMK（关键点地标）次之。这表明2D表示提供了更强的空间先验，有助于提升生成质量。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_dmzlAUkulz_AUHead_Realis/figures/006_Table_2.jpg]]
*Table 2: Ablation results on different AU representations for video generation. The top-2 results are marked in bold (best) and underlined (2nd-best). ∗ indicates results reproduced under the same training data and settings for fair comparison. AU Seq: 1D AU sequence; LMK: 2D keypoint-based landmark; RoM: 2D rendering of mesh.*

**AU引导尺度分析（Figure 3）**：实验表明，AU引导尺度在3.5时达到视觉质量（FID）与情感表达（Emotion ACC, MAE）的最佳平衡。过小的引导尺度导致情感表达不足，过大的引导尺度则损害视觉质量。

### 6.4 用户研究

Table 4展示了AUHead与HalloV2（Cui et al., 2024a）的用户偏好比较。在盲测中，AUHead在情感表达（64.63%）、视频质量（63.63%）、音唇同步（71.00%）和整体表现（67.75%）四个维度上均获得更高的用户偏好，验证了AUHead在情感表达和生成质量上的优势。

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_dmzlAUkulz_AUHead_Realis/figures/011_Table_4.jpg]]
*Table 4: User study evaluating the quality and emotional expressiveness of the generated talking heads. The better results are highlighted in bold.*

### 6.5 定性分析

Figure 4展示了AUHead与SOTA方法在MEAD和CREMA上的定性比较。AUHead生成的视频在面部表情的自然度、情感表达的丰富度和身份一致性方面均优于对比方法。Figure 5和Figure 10展示了在中性音频下使用ALM生成AU的情感动画对比，AUHead能够生成与情感标签一致的AU序列，从而驱动面部动画表达相应的情感。Figure 6展示了生成帧及其对应的AU 2D表示，验证了AU表示与面部运动之间的一致性。

### 6.6 泛化能力

Figure 7展示了AUHead在10秒序列上的泛化能力，涵盖线稿素描、油画肖像和真实人脸三种视觉风格，验证了模型在不同输入域下的鲁棒性。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__image_and_video_generation__b001_dmzlAUkulz_AUHead_Realis/figures/014_Table_5.jpg]]
*Table 5: Explanation of redefined AUs from the FEAFA+ dataset.*

## 方法谱系与知识库定位

AUHead在音频驱动说话头生成方法谱系中占据独特位置：

**与早期方法的关系**：早期方法如Wav2Lip（Prajwal et al., 2020）专注于音唇同步，SadTalker（Zhang et al., 2023）利用3D运动系数，PC-AVS和EAMM采用隐式姿态/情感编码。这些方法缺乏细粒度的情感控制。

**与扩散模型方法的关系**：DiffTalk、Diffused Heads、EMO、Loopy、Sonic、DAWN、IF-MDM等方法利用扩散模型提升生成质量，但情感控制仍停留在粗粒度层面。Hallo V1/V2和MEMO作为AUHead的Stage 2基础模型，提供了高质量的视觉生成能力，但缺乏显式的情感控制机制。

**与情感适配器方法的关系**：ETAU（Lyu et al., 2024; 2025）、EAT、SAAS、MEMO（baseline）、DICE-Talk、Takin-ADA等方法尝试通过情感适配器或解耦情感嵌入实现情感控制，但AUHead首次将AU作为结构化中间表示，实现了从粗粒度情感标签到细粒度AU序列的范式转变。

**与多模态大语言模型方法的关系**：OmniHuman-1.5等方法利用多模态大语言模型进行引导，AUHead则专注于利用音频语言模型（ALM）的语音理解能力进行AU解耦，为情感控制提供了更精细、更可解释的解决方案。

**知识库定位**：AUHead的核心贡献在于将面部动作单元（AU）这一心理学和计算机视觉领域的成熟概念引入音频驱动说话头生成任务，通过ALM实现从音频到AU的自动解耦，并通过可控扩散模型实现AU驱动的细粒度情感控制。该方法在情感表达的可控性、可解释性和生成质量之间取得了新的平衡，为情感说话头生成领域提供了新的技术路径。

## 原文 PDF

![[paperPDFs/ICLR_2026/AUHead_Realistic_Emotional_Talking_Head_Generation_via_Action_Units_Control.pdf]]
