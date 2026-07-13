---
title: "Enhancing Motion in Text-to-Video Generation with Decomposed Encoding and Conditioning"
type: paper
paper_level: A
venue: NeurIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/Enhancing_Motion_in_Text_to_Video_Generation_with_Decomposed_Encoding_and_Conditioning.pdf
project_link: https://PR-Ryan.github.io/DEMO-project/
code_link: null
aliases:
- EMTVGDEC
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "通过将文本编码和条件分解为内容与运动两个独立分支，并引入文本-运动监督和视频-运动监督来分别增强运动编码和运动生成。"
primary_logic: "将文本编码分解为内容编码器和运动编码器，配合文本-运动监督提升编码器对动作词的敏感性，同时在条件端引入时间维度的运动条件模块并用视频-运动监督约束生成视频的运动模式，可显著提升生成视频的运动动态性和真实感，同时保持静态内容的生成质量。"
claims:
- "在MSR-VTT上，DEMO的FVD从557降至422，FID从14.89降至11.77，表明整体视频质量显著提升。"
- "在EvalCrafter上，DEMO的运动评分Flow Score从2.51提升至4.89，Motion AC-Score从44提升至58，验证了运动动态性的显著增强。"
- "消融实验显示，移除视频-运动损失后，Motion AC-Score仅为46，而完整模型为58，证明了视频-运动监督的关键作用。"
- "运动编码器仅在使用文本-运动损失和正则化损失联合训练时，才能在不丧失内容敏感性的前提下获得更高的运动敏感性。"
---

# Enhancing Motion in Text-to-Video Generation with Decomposed Encoding and Conditioning

> [!tip] 核心洞察
> 将文本编码分解为内容编码器和运动编码器，配合文本-运动监督提升编码器对动作词的敏感性，同时在条件端引入时间维度的运动条件模块并用视频-运动监督约束生成视频的运动模式，可显著提升生成视频的运动动态性和真实感，同时保持静态内容的生成质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于分解编码与条件的文本到视频运动增强 |
| 英文题名 | Enhancing Motion in Text-to-Video Generation with Decomposed Encoding and Conditioning |
| 会议/期刊 | NeurIPS 2024 |
| Links | [paper](https://arxiv.org/abs/2410.24219) · [Project](https://PR-Ryan.github.io/DEMO-project/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DEMO |
| Dataset | MSR-VTT, WebVid-10M |

> [!tip] 效果简介
> - MSR-VTT 上，FVD 为 422，对比 557 (ModelScopeT2V)，变化 -135。
> - MSR-VTT 上，FID 为 11.77，对比 14.89 (ModelScopeT2V)，变化 -3.12。
> - MSR-VTT 上，CLIPSIM 为 0.2965，对比 0.2941 (ModelScopeT2V)，变化 +0.0024。

## 概要

文本到视频（T2V）生成领域，现有模型在提升视觉质量方面取得了显著进展，但在生成逼真、丰富的运动动态方面仍存在明显瓶颈。本文通过一项先导研究揭示了问题的根源：当前广泛使用的CLIP文本编码器对表示运动的词性（如动词）的敏感性显著低于对表示内容的词性（如名词），导致模型倾向于生成静态或运动匮乏的视频。此外，主流的文本条件机制仅通过逐帧的空间交叉注意力注入文本信息，缺乏时间维度上对运动模式的显式整合。

针对上述瓶颈，论文提出**DEMO**（Decomposed Encoding and Conditioning for Motion Enhancement），其核心思路是将文本编码和文本条件过程分解为**内容**与**运动**两个独立分支。具体而言，DEMO在编码端引入一个可训练的运动编码器，并通过文本-运动监督损失和正则化损失联合训练，使其在保持内容敏感性的前提下大幅提升对运动信息的表征能力；在条件端，DEMO在3D U-Net的时间维度插入专用的运动条件模块，并辅以视频-运动监督损失，直接约束生成视频的帧间运动模式与真实视频一致。

实验结果表明，DEMO在多个基准数据集上取得了运动动态性和整体视频质量的显著提升。在MSR-VTT上，FVD从557降至422，FID从14.89降至11.77；在EvalCrafter上，运动评分Flow Score从2.51提升至4.89，Motion AC-Score从44提升至58。消融实验进一步验证了各损失组件的必要性：移除视频-运动损失后，Motion AC-Score骤降至46，运动提升效果有限。同时，论文也指出了方法的局限性，包括无法生成文本指定的顺序动作、运动增强可能伴随时序闪烁的轻微增加等。

文本到视频生成（Text-to-Video Generation, T2V）的目标是根据自然语言描述合成逼真且动态的视频。近年来，基于潜在视频扩散模型（Latent Video Diffusion Models, LVDMs）的方法在这一领域取得了显著进展，其核心架构通常采用3D U-Net，通过空间与时间维度的自注意力和交叉注意力机制，在压缩的潜空间中逐步去噪以生成视频帧。然而，现有T2V模型在生成视频的运动质量方面仍存在明显不足——生成的视频往往呈现静态或仅有微弱运动的场景，与文本中描述的动作语义之间存在显著差距。

这一瓶颈的根源在于两个关键环节的设计缺陷。首先，**文本编码器对运动信息的表征能力不足**。目前主流的T2V模型普遍采用CLIP文本编码器提取文本特征，但如本研究通过先导实验（Figure 1）所揭示的，CLIP编码器对表示运动的词性（如动词）的敏感性显著低于对表示内容的词性（如名词）的敏感性。当文本中包含丰富的动作描述时，编码器倾向于忽略这些动态信息，导致后续生成过程缺乏有效的运动语义引导。其次，**文本条件机制缺乏时间维度的运动整合能力**。现有模型的条件注入方式仅通过逐帧的空间交叉注意力实现，每一帧独立地融合文本特征，缺少跨帧的运动信息交互通道。这种设计使得模型难以从文本中捕捉和传递时序动态信息，即使文本编码器能够提取运动特征，这些特征也无法有效转化为视频中的连贯运动。

针对上述问题，本文提出DEMO（Decomposed Encoding and Conditioning for Motion Enhancement），其核心动机是：**将文本编码和条件机制分解为内容与运动两个独立分支，通过专门的编码器增强运动语义提取，通过时间维度的条件模块实现运动信息注入，并辅以双重运动监督信号保障运动生成质量**。这一设计使得模型能够在保持静态内容生成质量的前提下，显著提升生成视频的运动动态性和真实感。

## 核心方法与创新机理

DEMO的核心创新在于对文本到视频（T2V）生成流程中**文本编码**和**文本条件机制**的双重分解，并辅以多层次的运动监督信号，从而在不依赖额外运动输入（如深度图、光流）的前提下，显著提升生成视频的运动动态性。

### 1. 文本编码分解：内容编码器与运动编码器

现有T2V模型（如 **ModelScopeT2V**）通常使用单一的CLIP文本编码器提取文本特征。先导研究（Figure 1）表明，CLIP编码器对表示运动的词性（如动词）的敏感性显著低于表示内容的词性（如名词），导致模型偏向于生成静态内容而忽略运动动态。

DEMO将文本编码分解为两个独立分支：
- **内容编码器** $\mathcal{E}_c$：冻结原始CLIP文本编码器，负责提取静态内容嵌入（对象、空间布局等）。
- **运动编码器** $\mathcal{E}_m$：以CLIP初始化并进行微调，专门提取运动嵌入（动作、方向等动态信息）。

运动编码器的微调通过两个损失函数联合监督：
- **文本-运动损失** $\mathcal{L}_{\text{text-motion}}$：约束 `[eot]` token的交叉注意力图的光流与真实视频光流的余弦相似度最大化，迫使编码器关注文本中的运动信息。
  
  $$\mathcal{L}_{\text{text-motion}} = -\mathbb{E}_{t, x_0, \epsilon \sim \mathcal{N}(0,1), p} \left[ \frac{1}{M} \sum_{i=1}^{M} \cos(\phi(A_{[eot]}^i), \phi(x_0)) \right]$$

- **正则化损失** $\mathcal{L}_{\text{reg}}$：将运动文本嵌入与中间帧的图像嵌入对齐，防止微调过程中的灾难性遗忘，确保运动编码器在提升运动敏感性的同时不丧失内容敏感性。

  $$\mathcal{L}_{\text{reg}} = -\mathbb{E}_{x_0, p} \left[ \cos(\mathcal{E}_m(p), \mathcal{E}^{\text{img}}(x_0^{F/2})) \right]$$

消融实验证实，仅使用 $\mathcal{L}_{\text{text-motion}}$ 微调会导致灾难性遗忘；加入 $\mathcal{L}_{\text{reg}}$ 后，运动编码器在保持内容敏感性的同时显著提升运动敏感性（Section 4.4, Figure 1）。

### 2. 文本条件分解：内容条件与运动条件

基线模型（ModelScopeT2V）的条件机制仅通过逐帧的空间交叉注意力注入文本特征，缺乏时间维度上的运动信息整合。

DEMO将条件机制分解为：
- **内容条件模块**：沿用3D U-Net中原有的空间交叉注意力层，逐帧融合内容嵌入，维持静态内容的生成质量。
- **运动条件模块**：在3D U-Net的时间维度上插入额外的时间Transformer，专门融入运动嵌入以引导运动生成。

这种分解使内容和运动信息通过各自的专用通道注入生成过程，避免了单一条件机制中两类信息的相互干扰。

### 3. 视频-运动监督：直接约束生成视频的运动模式

除文本编码端的监督外，DEMO在视频生成端引入**视频-运动损失** $\mathcal{L}_{\text{video-motion}}$。该损失通过最小化预测干净潜变量的帧差与真实潜变量帧差的L2距离，直接约束生成视频的运动模式：

$$\mathcal{L}_{\text{video-motion}} = \mathbb{E}_{t, z_0, \epsilon \sim \mathcal{N}(0,1)} \| \Phi(z_0) - \Phi(\hat{z}_{0,t}) \|_2^2$$

其中运动特征提取器 $\Phi(z_0) = z_0^{2:F} - z_0^{1:F-1}$ 为连续帧差操作。

消融实验（Table 4）表明，移除 $\mathcal{L}_{\text{video-motion}}$ 后，EvalCrafter上的Motion AC-Score从58降至46；仅添加运动编码器而不使用该损失，MSR-VTT上的FVD仅从557微降至552（Table 6）。这验证了视频-运动监督对于生成强运动动态的关键作用。

### 创新总结

| 改动槽位 | 基线方案 | DEMO方案 | 核心作用 |
|---------|---------|---------|---------|
| 文本编码策略 | 单一CLIP编码器 | 冻结内容编码器 + 可训练运动编码器（含文本-运动监督和正则化） | 提升编码器对运动词的敏感性 |
| 文本条件机制 | 逐帧空间交叉注意力 | 空间交叉注意力（内容）+ 时间Transformer（运动） | 在时间维度上整合运动信息 |
| 训练目标 | 仅扩散损失 | 扩散损失 + 文本-运动损失 + 正则化损失 + 视频-运动损失 | 多层次监督编码端和生成端的运动质量 |

这三个改动槽位形成因果链条：运动编码器提取运动敏感的文本表示 → 运动条件模块在时间维度注入该表示 → 视频-运动损失直接约束生成结果的运动模式。三者协同作用，使DEMO在MSR-VTT上FVD从557降至422、FID从14.89降至11.77（Table 1），在EvalCrafter上Flow Score从2.51提升至4.89（Table 4）。


DEMO 的整体框架围绕一个核心洞察展开：现有文本到视频（T2V）模型中的文本编码器偏向于表示静态内容而忽略运动动态，且条件机制仅进行逐帧空间交叉注意力，缺乏时间维度上的运动信息整合。为解决这一问题，DEMO 在标准潜变量视频扩散模型（LVDM）的基础上，将文本编码与文本条件过程分别分解为内容与运动两个独立分支，并通过三个额外的监督信号——文本-运动损失、正则化损失和视频-运动损失——来分别增强运动编码和运动生成。

### Pipeline 结构与模块关系

如图 2 所示，DEMO 的训练流程包含以下核心模块及其交互关系：

1. **双文本编码器**：原始 CLIP 文本编码器被保留为**内容编码器**（Content Encoder），冻结参数，负责提取文本中与静态内容相关的嵌入（如对象、空间布局）。同时引入一个可训练的**运动编码器**（Motion Encoder），由 CLIP 文本编码器初始化，在文本-运动损失和正则化损失的联合监督下微调，专门提取与运动相关的嵌入（如动作、方向）。

2. **双文本条件模块**：在 3D U-Net 的去噪网络中，原有的空间交叉注意力层作为**内容条件模块**（Content Conditioning Module），逐帧融合内容嵌入。同时，在 3D U-Net 的时间维度上插入一个额外的**运动条件模块**（Motion Conditioning Module），即一个专门的时间 Transformer，将运动嵌入融入时间特征，引导运动生成。

3. **三层训练监督**：
   - **扩散损失** $\mathcal{L}_{\mathrm{diffusion}}$：标准潜变量扩散模型的噪声预测损失，如公式 (1) 所示。
   - **编码器级监督**：**文本-运动损失** $\mathcal{L}_{\mathrm{text-motion}}$ 约束运动编码器中 [eot] token 的交叉注意力图的光流与真实视频光流一致，迫使编码器关注运动信息；**正则化损失** $\mathcal{L}_{\mathrm{reg}}$ 通过使运动文本嵌入与中间帧的图像嵌入对齐，防止微调过程中的灾难性遗忘。
   - **生成器级监督**：**视频-运动损失** $\mathcal{L}_{\mathrm{video-motion}}$ 通过最小化预测干净潜变量的帧差与真实潜变量帧差的 L2 距离，确保生成视频的运动模式逼真。

### 输入输出流

- **输入**：文本提示 $p$ 和随机采样的噪声潜变量 $z_t$。
- **编码阶段**：文本 $p$ 分别通过冻结的内容编码器 $\mathcal{E}_c$ 和可训练的运动编码器 $\mathcal{E}_m$，得到内容嵌入和运动嵌入。
- **去噪阶段**：3D U-Net 的去噪网络 $\epsilon_\theta$ 接收噪声潜变量 $z_t$、时间步 $t$、内容嵌入和运动嵌入，通过空间交叉注意力（内容条件）和时间 Transformer（运动条件）融合两类信息，预测噪声 $\epsilon$。
- **训练目标**：总损失为四部分加权和：$\mathcal{L} = \mathcal{L}_{\mathrm{diffusion}} + \alpha\mathcal{L}_{\mathrm{text-motion}} + \beta\mathcal{L}_{\mathrm{reg}} + \gamma\mathcal{L}_{\mathrm{video-motion}}$，如公式 (10) 所示。
- **输出**：通过逐步去噪生成具有增强运动动态的视频帧序列。

### 关键因果机制

- **运动编码器的有效性**：先导研究（Figure 1）表明，原始 CLIP 文本编码器对表示运动的词性（如动词）的敏感性显著低于对表示内容的词性（如名词）。仅使用文本-运动损失微调会导致灾难性遗忘；只有联合使用正则化损失时，运动编码器才能在保持内容敏感性的同时显著提升运动敏感性。
- **视频-运动损失的必要性**：消融实验（Table 4, Table 6）显示，仅添加运动编码器而不使用视频-运动损失时，MSR-VTT 上的 FVD 仅从 557 降至 552，EvalCrafter 上的 Motion AC-Score 仅为 46；而完整模型将 Motion AC-Score 提升至 58，证明了视频-运动监督对于生成强运动动态的关键作用。

### 3.1 基础扩散框架

DEMO 建立在潜视频扩散模型（LVDM）之上，其核心是一个 3D U-Net，由下采样、中间和上采样块堆叠而成，每个块包含空间 Transformer 和时间 Transformer。空间 Transformer 由空间自注意力、空间交叉注意力和前馈层组成，时间 Transformer 则由时间自注意力和前馈层构成。给定文本提示 $p$，模型通过文本编码器 $\mathcal{E}$ 提取文本嵌入，并注入 U-Net 进行条件生成。

扩散过程在潜空间中进行。前向加噪过程定义为：

$$z _ { t } = \sqrt { \bar { \alpha } _ { t } } z _ { 0 } + \sqrt { 1 - \bar { \alpha } _ { t } } \epsilon , \quad \bar { \alpha } _ { t } = \prod _ { s = 1 } ^ { t } \alpha _ { s } \tag{2}$$

其中 $z_0$ 为干净视频潜变量，$\epsilon \sim \mathcal{N}(0,1)$ 为标准高斯噪声，$\bar{\alpha}_t$ 为累积噪声调度参数。标准扩散损失为噪声预测损失：

$$\mathcal { L } _ { \mathrm { d i f f u s i o n } } = \mathbb { E } _ { t , z _ { 0 } , \epsilon \sim \mathcal { N } ( 0 , 1 ) , p } \left[ \| \epsilon - \epsilon _ { \theta } ( z _ { t } , t , \mathcal { E } ( p ) ) \| _ { 2 } ^ { 2 } \right] \tag{1}$$

其中 $\epsilon_\theta$ 为噪声预测网络（3D U-Net），$\mathcal{E}(p)$ 为文本条件嵌入。

### 3.2 分解式文本编码

DEMO 的核心创新在于将文本编码分解为内容与运动两个独立分支：

- **内容编码器** $\mathcal{E}_c$：保留原始冻结的 CLIP 文本编码器，提取静态内容嵌入（对象、空间布局等）。
- **运动编码器** $\mathcal{E}_m$：新增一个可训练的文本编码器，由 CLIP 初始化，专门提取运动嵌入（动作、方向等动态信息）。

运动编码器通过两个监督信号进行微调：

**文本-运动监督**：约束交叉注意力图的时间变化与真实视频的光流一致。首先计算第 $i$ 层交叉注意力图（跨头平均）：

$$\mathcal { A } ^ { i } = \frac { 1 } { N } \sum _ { n } ^ { N } \mathrm { s o f t m a x } \left( \frac { Q ^ { ( n ) } ( K ^ { ( n ) } ) ^ { T } } { \sqrt { d _ { n } } } \right) \tag{3}$$

实证发现 `[eot]` token 对应的交叉注意力图对运动生成起关键作用。文本-运动损失最大化该注意力图的光流 $\phi(\mathcal{A}_{[eot]}^i)$ 与真实视频光流 $\phi(x_0)$ 的余弦相似度：

$$\mathcal { L } _ { \mathrm { t e x t - m o t i o n } } = - \mathbb { E } _ { t , x _ { 0 } , \epsilon \sim \mathcal { N } ( 0 , 1 ) , p } \left[ \frac { 1 } { M } \sum _ { i = 1 } ^ { M } \cos \left( \phi ( \mathcal{A} _ { [ e o t ] } ^ { i } ) , \phi ( x _ { 0 } ) \right) \right] \tag{5}$$

其中 $M$ 为注意力层数，$\phi(\cdot)$ 为光流提取算子。

**正则化损失**：防止运动编码器在微调中发生灾难性遗忘，约束运动文本嵌入与中间帧图像嵌入对齐：

$$\mathcal { L } _ { \mathrm { r e g } } = - \mathbb { E } _ { x _ { 0 } , p } \left[ \cos \left( \mathcal { E } _ { m } ( p ) , \mathcal { E } ^ { i m g } ( x _ { 0 } ^ { F / 2 } ) \right) \right] \tag{6}$$

其中 $\mathcal{E}^{img}$ 为 CLIP 图像编码器，$x_0^{F/2}$ 为视频中间帧。消融实验证实，仅用 $\mathcal{L}_{text-motion}$ 微调会导致运动编码器丧失内容敏感性；联合使用 $\mathcal{L}_{reg}$ 和 $\mathcal{L}_{text-motion}$ 后，运动编码器在保持内容敏感性的同时显著提升对运动词（如动词）的敏感性（Figure 1, Section 4.4）。

### 3.3 分解式文本条件与视频-运动监督

DEMO 在条件端同样进行分解：

- **内容条件模块**：沿用 3D U-Net 中逐帧的空间交叉注意力层，融合内容特征 $\mathcal{E}_c(p)$。
- **运动条件模块**：在 3D U-Net 的时间维度插入额外的时间 Transformer，接收运动特征 $\mathcal{E}_m(p)$，引导运动生成。

为进一步强化运动生成质量，引入**视频-运动监督**。首先利用扩散模型在步骤 $t$ 估计无噪声潜变量：

$$\hat { z } _ { 0 , t } ( t , z _ { t } , \mathcal { E } _ { m } ( p ) , \mathcal { E } _ { c } ( p ) ) = \frac { z _ { t } - \sqrt { 1 - \bar { \alpha } _ { t } } \epsilon _ { \theta } ( z _ { t } , t , \mathcal { E } _ { m } ( p ) , \mathcal { E } _ { c } ( p ) ) } { \sqrt { \bar { \alpha } _ { t } } } \tag{7}$$

运动特征通过连续帧差提取：

$$\Phi ( z _ { 0 } ) = z _ { 0 } ^ { 2 : F } - z _ { 0 } ^ { 1 : F - 1 } \tag{9}$$

视频-运动损失约束预测潜变量的运动特征与真实潜变量一致：

$$\mathcal { L } _ { \mathrm { v i d e o - m o t i o n } } = \mathbb { E } _ { t , z _ { 0 } , \epsilon \sim \mathcal { N } ( 0 , 1 ) } \left\| \Phi ( z _ { 0 } ) - \Phi ( \hat { z } _ { 0 , t } ) \right\| _ { 2 } ^ { 2 } \tag{8}$$

消融实验表明，去除 $\mathcal{L}_{video-motion}$ 后，EvalCrafter 上的 Motion AC-Score 从 58 降至 46，MSR-VTT 上的 FVD 仅从 557 降至 552（Table 4, Table 6），验证了该损失对运动增强的关键作用。

### 3.4 总损失函数

训练总损失为上述各项的加权和：

$$\mathcal { L } = \mathcal { L } _ { \mathrm { d i f f u s i o n } } + \alpha \mathcal { L } _ { \mathrm { t e x t - m o t i o n } } + \beta \mathcal { L } _ { \mathrm { r e g } } + \gamma \mathcal { L } _ { \mathrm { v i d e o - m o t i o n } } \tag{10}$$

其中 $\alpha$、$\beta$、$\gamma$ 为超参数权重，完整训练超参数见 Table 7。

## 实验与关键发现

### 主实验结果

DEMO在多个零样本文本到视频生成基准上对运动动态性和视频质量进行了系统评估，主要与基础模型**ModelScopeT2V**及其微调版本、**LaVie**、**VideoCrafter2**等先进方法对比。所有定量比较遵循ModelScopeT2V论文中的评估协议，定性比较使用相同的随机种子以保证可比性。

**MSR-VTT零样本结果**（Table 1）显示，DEMO在视频质量指标上取得显著提升：FVD从557降至422（降低135），FID从14.89降至11.77（降低3.12），同时CLIPSIM从0.2941微升至0.2965，表明文本-视频对齐能力得到保持。值得注意的是，ModelScopeT2V微调版本仅将FVD降至552，说明DEMO的改进并非单纯来自额外微调。

![[assets/figures/papers/paper_list_l14_Enhancing_Motion_in_Text_to_Video_Generation_with_Decomposed_Encoding_an/figures/003_Table_1.jpg]]
*Table 1: Results of zero-shot T2V generation on MSR-VTT (Evaluation protocol comparison can be found in the appendix)*

**WebVid-10M域内验证**（Table 3）进一步验证了方法的有效性：FVD从508降至351（降低157），FID从10.80降至8.98，CLIPSIM从0.3105提升至0.3142，表明在训练分布内DEMO同样具有稳定的质量增益。

![[assets/figures/papers/paper_list_l14_Enhancing_Motion_in_Text_to_Video_Generation_with_Decomposed_Encoding_an/figures/005_Table_3.jpg]]
*Table 3: Results of T2V generation on WebVid-10M (Val)*

**运动质量专项评估**是DEMO的核心验证维度。在EvalCrafter基准（Table 4）上，运动评分Flow Score从2.51提升至4.89（提升95%），Motion AC-Score从44提升至58（提升14分），验证了运动动态性的显著增强。在VBench基准（Table 5）上，Motion Dynamics从62.50提升至68.90（提升6.40），进一步确认了运动质量的改善。

![[assets/figures/papers/paper_list_l14_Enhancing_Motion_in_Text_to_Video_Generation_with_Decomposed_Encoding_an/figures/006_Table_4.jpg]]
*Table 4: Results of zero-shot T2V generation on EvalCrafter*

**UCF-101零样本结果**（Table 2）显示，DEMO的FVD从647降至576，但IS从36.21微降至35.79——模型可能因过度关注运动而略微限制了生成多样性，这构成一个值得注意的权衡。

![[assets/figures/papers/paper_list_l14_Enhancing_Motion_in_Text_to_Video_Generation_with_Decomposed_Encoding_an/figures/004_Table_2.jpg]]
*Table 2: Results of zero-shot T2V generation on UCF-101 (Evaluation protocol comparison can be found in the appendix)*

**用户研究**（Table 12）的成对比较结果进一步支持了定量发现：在与ModelScopeT2V、LaVie、VideoCrafter2的对比中，DEMO在运动质量维度上获得了压倒性偏好，在文本-视频对齐和视觉质量上也保持竞争优势。

**定性对比**（Figure 3）直观展示了上述差异：ModelScopeT2V生成的视频运动幅度极小，LaVie存在类似问题，VideoCrafter2虽然运动动态较大但伴随运动模糊，而DEMO在保持清晰度的同时捕捉到了文本描述的运动本质。

### 消融实验

消融实验揭示了DEMO各组件的因果贡献，验证了核心设计选择的必要性。

**运动编码器训练策略**（Section 4.4, Figure 1先导研究）是关键消融点。仅使用文本-运动损失$\mathcal{L}_{\text{text-motion}}$微调运动编码器会导致灾难性遗忘——编码器丧失了对内容词（名词）的敏感性。引入正则化损失$\mathcal{L}_{\text{reg}}$后，运动编码器在保持内容敏感性的同时显著提升了对动作词（动词）的敏感性，验证了联合训练策略的必要性。

**视频-运动损失的关键作用**（Table 4, Table 6）是最具决定性的消融发现。去除$\mathcal{L}_{\text{video-motion}}$后，EvalCrafter上的Motion AC-Score从58骤降至46，运动提升极为有限。在MSR-VTT上，仅添加运动编码器而不使用视频-运动损失时，FVD仅从557降至552（改进仅5点），而完整DEMO降至422（改进135点）。这明确证明：视频-运动监督是驱动生成强运动动态的核心因果机制，运动编码器单独存在不足以产生显著的运动质量增益。

![[assets/figures/papers/paper_list_l14_Enhancing_Motion_in_Text_to_Video_Generation_with_Decomposed_Encoding_an/figures/008_Table_6.jpg]]
*Table 6: Ablation study on additional parameters in motion encoder*

**方法泛化性验证**（Table 11）将DEMO方法应用于**ZeroScope**基线，同样观察到一致的性能提升，表明分解编码与条件的设计不依赖于特定的基础模型架构。

![[assets/figures/papers/paper_list_l14_Enhancing_Motion_in_Text_to_Video_Generation_with_Decomposed_Encoding_an/figures/014_Table_11.jpg]]
*Table 11: Quantitative results on ZeroScope*

### 失败模式与局限

**顺序动作生成失败**（Figure 4）是DEMO最显著的局限：模型无法生成文本中指定的顺序动作序列。当提示包含多个时间上应先后发生的动作时（如“a man standing in a kitchen and talking”与“a mixer and a carton of milk are shown”），这些动作会同时出现而非依次发生。这源于文本编码器缺乏对动作时序关系的建模能力。

**运动-质量权衡**在多个维度上显现。在VBench（Table 5）上，提升运动动态性的同时，Temporal Flickering和Motion Smoothness指标出现轻微下降，表明更强的运动生成可能引入时间一致性问题。在UCF-101上，IS的微降暗示运动关注可能以牺牲生成多样性为代价。

**视觉质量上限受限**于训练数据。Table 8显示DEMO使用WebVid-10M数据集训练，而LaVie和VideoCrafter2使用了更高质量的Vimeo-25M和JDB数据集，因此DEMO在纯视觉质量上仍存在差距——这是数据约束而非方法缺陷。

**过拟合迹象**：论文指出继续微调仅带来边际视频质量改进，且CLIPSIM出现轻微退化，表明当前训练策略存在性能饱和点。

## 定位与知识库关联

DEMO 的工作建立在潜视频扩散模型（LVDM）的基础之上，其核心基座是 **ModelScopeT2V**，一个基于 3D U-Net 架构的文本到视频生成模型。该架构由下采样、中间和上采样模块组成，每个模块包含卷积层以及空间和时间 Transformer。空间 Transformer 内部由空间自注意力、空间交叉注意力和前馈网络层构成，文本条件通过交叉注意力逐帧注入。DEMO 正是在此标准范式上，针对文本编码与条件机制进行了结构性改造。

与 DEMO 形成对比的同期先进方法包括 **LaVie** 和 **VideoCrafter2**。这些模型通常通过引入更高质量的训练数据（如 Vimeo-25M 和 JDB 数据集）来提升视觉质量，但并未从根本上解决文本编码器对运动动态表征不足的问题。DEMO 的策略与之正交：它不依赖额外的数据信号，而是通过分解编码和条件来显式增强运动生成，因此在运动动态性指标上取得了显著优势，尽管在视觉质量上受限于 WebVid-10M 数据集而略逊于上述模型。

在知识库定位上，DEMO 的方法属于“基于文本条件分解的运动增强”范畴，其核心贡献在于三个可插拔的模块化改造：**分解式文本编码**（冻结的内容编码器与可微调的运动编码器）、**分解式条件注入**（空间交叉注意力与时间运动 Transformer 并行）、以及**双层级运动监督**（文本-运动损失与视频-运动损失）。这种设计使得 DEMO 可以作为插件应用于其他 LVDM 架构，论文在 **ZeroScope** 上的泛化实验（Table 11）初步验证了这一点。

### 适用边界与局限

DEMO 的适用边界清晰。它适用于需要增强生成视频中运动动态性的场景，特别是那些对动作、方向等动态语义有明确要求的文本提示。其方法在零样本设定下表现良好，在 MSR-VTT、UCF-101、WebVid-10M、EvalCrafter 和 VBench 等多个基准上均验证了有效性。

然而，该方法存在若干已知局限：

1. **时序动作顺序缺失**：DEMO 无法生成文本中指定的顺序动作。当提示包含多个连续动作时（如“一个人站在厨房说话，然后搅拌机和牛奶盒出现”），所有动作会同时发生，而非按序展开。这表明运动编码器和条件模块虽然增强了对运动本身的敏感性，但并未建模动作之间的时序依赖关系。

2. **运动-质量权衡**：在 VBench 上，虽然 Motion Dynamics 指标从 62.50 提升至 68.90，但 Temporal Flickering 和 Motion Smoothness 指标出现轻微下降。这说明增强运动动态性与保持时序稳定性之间存在内在张力，当前方法尚未完全解决这一冲突。

3. **生成多样性受限**：在 UCF-101 上，IS 指标略有下降，可能源于模型过度聚焦于运动模式而限制了生成多样性。

4. **视觉质量瓶颈**：由于仅在 WebVid-10M 数据集上训练，DEMO 的视觉质量与使用更高质量数据集的模型（如 LaVie、VideoCrafter2）相比仍有差距。

### 开放问题

基于上述局限，论文明确指出了若干待解决的开放问题：

- 如何使模型理解并生成具有时序顺序的多个动作，而非将其同时呈现？
- 如何改进文本编码器对动作顺序的语义理解能力？
- 如何在提升运动动态性的同时，减轻时序闪烁和运动平滑度的退化？
- 如何训练模型以支持变长视频生成，从而适应不同长度的运动序列？
- 如何在不依赖大规模高质量视频数据集的前提下提升视觉质量？

这些问题指向了文本到视频生成领域从“静态质量”向“动态真实感”演进过程中的关键瓶颈：运动建模不仅需要空间-时间维度的解耦，更需要时序因果性和物理一致性的深层建模。DEMO 的分解式框架为后续研究提供了可扩展的架构基础，但其在时序推理和长程运动连贯性方面的能力仍有待突破。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/Enhancing_Motion_in_Text_to_Video_Generation_with_Decomposed_Encoding_and_Conditioning.pdf]]
