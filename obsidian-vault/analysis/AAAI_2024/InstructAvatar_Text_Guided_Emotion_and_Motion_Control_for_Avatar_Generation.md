---
title: "InstructAvatar: Text-Guided Emotion and Motion Control for Avatar Generation"
type: paper
paper_level: A
venue: AAAI
year: 2024
pdf_ref: paperPDFs/AAAI_2024/InstructAvatar_Text_Guided_Emotion_and_Motion_Control_for_Avatar_Generation.pdf
code_link: null
project_link: https://wangyuchi369.github.io/InstructAvatar/
aliases:
- InstructAvatar
tags:
- AAAI_2024
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "将控制信号从受限标签/参考视频扩展为自然语言文本指令，并设计双分支交叉注意力机制分别解析全局情绪风格与时序面部动作，使模型能够执行开放词汇的细粒度控制。"
primary_logic: "利用动作单元(AU)和GPT-4V自动构建细粒度文本-视频对，再通过零卷积门控将文本控制平稳注入预训练的无情绪模型，从而在保持生成质量的同时实现精确的表情与动作控制。"
claims:
- "采用双分支交叉注意力机制分别处理情绪指令（[EOS] token）和动作指令（全部token hidden states），实现全局风格与动态动作的分离控制。"
- "零卷积门控机制将文本交叉注意力的权重和偏置初始化为零，使得训练起始等价于无指令模型，随后逐步引入文本控制，稳定了训练并充分利用预训练知识。"
- "通过提取视频的动作单元（AU），并利用GPT-4V的视觉-语言能力将AU转述为自然语言句子，构建了细粒度且可泛化的指令-视频训练数据。"
- "MEAD (in-domain) 上 AU_F1 ↑ = 0.738"
---

# InstructAvatar: Text-Guided Emotion and Motion Control for Avatar Generation

> [!tip] 核心洞察
> 利用动作单元(AU)和GPT-4V自动构建细粒度文本-视频对，再通过零卷积门控将文本控制平稳注入预训练的无情绪模型，从而在保持生成质量的同时实现精确的表情与动作控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | InstructAvatar：文本引导的情绪与动作控制头像生成 |
| 英文题名 | InstructAvatar: Text-Guided Emotion and Motion Control for Avatar Generation |
| 会议/期刊 | AAAI 2024 |
| Links | [paper](https://arxiv.org/abs/2405.15758) · [Project](https://wangyuchi369.github.io/InstructAvatar/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | InstructAvatar |
| Dataset | MEAD (in-domain), TalkingHead 1KH (out-of-domain) |

> [!tip] 效果简介
> - MEAD (in-domain) 上，AU_F1 ↑ 为 0.738，对比 0.711 (DreamTalk)，变化 +0.027。
> - MEAD (in-domain) 上，SyncD ↓ 为 9.412，对比 9.542 (GAIA)，变化 -0.130。
> - TalkingHead 1KH (out-of-domain) 上，AU_F1 ↑ 为 0.552，对比 0.542 (EAT)，变化 +0.010。

## 概要

**核心问题**：现有情感说话人脸生成方法依赖离散情绪标签或参考视频作为控制信号，缺乏细粒度、开放词汇的用户控制能力，难以同时传达丰富的表情变化与动态面部动作，导致生成视频表现力不足且可控性差。

**核心洞见**：将控制接口从受限标签/参考视频扩展为自然语言文本指令，并利用动作单元（AU）与多模态大模型自动构建细粒度文本-视频训练对，使模型能够理解开放词汇的表情与动作描述。

**方法定位**：InstructAvatar 是一种基于扩散模型的文本驱动头像生成框架。其关键设计包括：（1）双分支交叉注意力机制，分别解析全局情绪风格与时序面部动作；（2）零卷积门控，将文本控制平稳注入预训练的无情绪模型，在保持生成质量的前提下实现精确控制；（3）基于 AU 提取与 GPT-4V 转述的自动标注管线，构建指令-视频配对数据。

**主要结果**：在域内（MEAD）和域外（TalkingHead 1KH）基准上，InstructAvatar 在表情控制精度（AU_F1）、唇形同步（SyncD）和主观评分（MOS）上均优于基于标签的模型（如 **EAT**）和基于参考视频的模型（如 **DreamTalk**、**StyleTalk**）。消融实验证实，零卷积门控对稳定训练和保持唇形同步至关重要（移除后 SyncD 恶化至 12.832），AU 辅助损失对细粒度表情控制贡献显著（移除后 AU_F1 降至 0.435），自然语言指令比类别标签提供更丰富的控制信号。

**局限与待解问题**：当前模型难以实现完全解耦的单一动作单元控制，对极端域外外观的泛化能力有限，且无法同时处理包含情绪与动作的复合文本指令。



情感驱动的人脸动画生成是数字人、虚拟主播和沉浸式交互中的核心技术。其目标是根据音频、文本或参考信号，生成具有丰富表情、自然动作和高质量唇形同步的说话人脸视频。近年来，基于扩散模型和变分自编码器的方法在生成质量和身份保持方面取得了显著进展，但在用户控制能力上仍面临根本性瓶颈。

**现有方法的控制接口受限。** 当前的情感说话人脸生成方法主要依赖两类控制信号：一是离散的情绪类别标签（如“高兴”“悲伤”），二是参考视频中的表情序列。例如，**EAT** 采用 one-hot 标签驱动情绪表达，**DreamTalk** 和 **StyleTalk** 则通过参考视频传递情感风格。然而，这种控制方式存在本质缺陷：标签只能指定粗略的情绪类别，无法描述“嘴角微微上扬但眉头紧锁”这样的细粒度表情组合；参考视频则需要用户预先准备合适的素材，灵活性和泛化性均受到严重制约。正如论文所指出的，现有方法“缺乏细粒度且灵活的用户控制方式，难以同时传达丰富的表情和动态动作，导致生成视频不生动、可控性差”。

**文本作为控制信号的潜力未被充分挖掘。** 自然语言是人类表达意图最灵活、最直观的方式。一句“她先是惊讶地睁大眼睛，然后慢慢露出欣慰的微笑”所蕴含的时序信息和表情细节，远非一个情绪标签或一段参考视频所能承载。然而，将文本指令引入说话人脸生成面临双重挑战：一是如何构建细粒度的文本-视频配对训练数据，二是如何设计模型架构以精确解析文本中的全局情绪风格与时序动作指令，并将其平稳注入生成过程而不破坏已有的唇形同步能力。

**InstructAvatar 的核心动机**正是填补这一空白——将控制信号从受限的标签/参考视频扩展为自然语言文本指令，使模型能够执行开放词汇的细粒度情绪与动作控制。该工作通过三项关键设计实现这一目标：(1) 利用动作单元和 GPT-4V 自动构建细粒度文本-视频对；(2) 设计双分支交叉注意力机制分别解析全局情绪风格与时序面部动作；(3) 引入零卷积门控将文本控制平稳注入预训练的无情绪模型，在保持生成质量的同时实现精确的表情与动作控制。



## 核心方法与创新机理

InstructAvatar 的核心创新在于将情感说话人脸的控制接口从受限的离散标签或参考视频彻底转向**开放词汇的自然语言文本指令**，并围绕这一范式转移设计了配套的架构与数据方案。其关键创新点可归纳为以下四个“changed slots”：

### 1. 控制接口：从标签/参考视频到自然语言文本

现有情感说话人脸方法依赖两类控制信号：**EAT** 等模型使用 one-hot 情绪标签，仅能指定粗粒度的整体风格；**StyleTalk、DreamTalk** 等模型需要参考视频，控制成本高且难以泛化。InstructAvatar 将控制信号扩展为自然语言文本指令（`T`），使得用户可以通过一句话同时指定情绪类型、强度以及面部动作细节，实现了从“类别选择”到“描述式生成”的跨越。

> **证据锚点**：“we steer towards a textual instruction-based talking avatar generation model... Enhanced control over fine-grained details rather than just the overall style”

### 2. 文本注入方式：双分支交叉注意力

为解析文本指令中的异构信息，模型在扩散降噪块的每一层将数据流拆分为两个分支（Figure 4）：

- **情绪分支**：使用 CLIP 文本编码器的 `[EOS]` token 的适配输出 $\mathcal{A}_e(\mathcal{C}(T)_{[EOS]})$，捕获全局情绪风格；
- **动作分支**：使用全部 token 的隐状态适配输出 $\mathcal{A}_m(\mathcal{C}(T)_{all})$，保留时序细粒度的面部动作信息。

两个分支通过独立的 Adapter（两层 MLP）进行分布对齐后，分别以交叉注意力注入运动隐变量。这种设计使得全局风格与动态动作的分离控制成为可能。

> **证据锚点**：“we split the data flow into two branches in each denoising block... For the emotion branch, we use the [EOS] token... For the motion branch, we utilize the hidden states of all tokens... we introduce different Adapters A_e, A_m to better align the distributions”

### 3. 门控机制：零卷积门控

直接将文本交叉注意力插入预训练的无情绪模型（如 GAIA）会导致训练初期的不稳定。InstructAvatar 引入了**零卷积门控**（Zero Convolution Gate）：

$$h_i = h_{i-1} + \mathcal{Z}(\text{CrossAttn}(h, \text{Rep}(\mathbf{T})))$$

其中 $\mathcal{Z}$ 是一个沿隐状态维度滑动的 1D 卷积，其权重和偏置均初始化为零。训练起始时 $h_i = h_{i-1}$，等价于无文本条件的预训练模型；随后梯度逐步更新门控参数，平稳地将文本控制信号注入生成过程。消融实验（Table 4）表明，移除该门控后 SyncD 恶化至 12.832，验证了其对保持唇形同步的关键作用。

> **证据锚点**：“Z is a zero convolution operation... with both the weight and bias initialized to zero. Therefore, at the start of training, h_i = h_{i-1}”

### 4. 训练数据标注：AU + GPT-4V 自动管线

细粒度文本控制需要对应的文本-视频对训练数据，但手工标注成本极高。InstructAvatar 设计了一条自动化标注管线（Figure 3）：

1. 使用现成的 AU 检测模型从视频片段中提取动作单元（Action Units）；
2. 随机选取三帧取交集以保证一致性；
3. 调用 GPT-4V 将 AU 组合转述为自然语言句子。

这一管线不仅提供了可泛化的指令-视频对，还利用 GPT-4V 的视觉-语言能力纠正了 AU 检测器的误检与漏检（Figure 11）。消融实验（Table 5）显示，若用情绪标签替代文本指令训练，AU_F1 从 0.738 骤降至 0.469，充分证明了自然语言描述相比类别标签能提供更丰富的控制信号。

> **证据锚点**：“we design an automatic annotation pipeline to construct an instruction-video paired training dataset... AUs are extracted... GPT-4V to paraphrase AUs into a natural textual description”

### 创新点协同关系

上述四个 changed slots 构成了一条完整的创新链条：**文本接口**定义了“控制什么”，**AU+GPT-4V 管线**解决了“如何获取训练信号”，**双分支交叉注意力**决定了“如何解析指令”，**零卷积门控**保证了“如何稳定注入预训练模型”。四者相互依赖，缺一不可。



InstructAvatar 的整体目标是根据音频 $A$、参考肖像 $I$ 和自然语言指令 $T$ 生成说话人脸视频 $V$，其核心映射关系为 $V = \mathcal{F}(A, I, T)$。该方法将生成过程分解为两个级联阶段：**运动-外观解耦**与**文本引导的运动生成**，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l1499_https_arxiv_org_abs_2405_15758/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview: The InstructAvatar consists of two components: VAE H to disentangle motion information from the video and a motion generator G to generate the motion latent conditioned on audio and instruction. As we have two types of data, two switches in instruction and audio are designed. During inference, the motion encoder in the VAE will be dropped and we iteratively denoise Gaussian noise to obtain the predicted motion latent. Together with the user-provided portrait, the resulting video is generated by the decoder of the VAE*

**第一阶段：运动-外观解耦。** 采用一个预训练的 VAE（记作 $\mathcal{H}$）将视频分解为运动隐变量 $M$ 和外观信息。外观信息从参考肖像 $I$ 中提取，运动隐变量 $M$ 则编码了面部动态、表情变化和头部姿态等时序信息。最终视频通过 $V = \mathcal{H}(M, I)$ 重建。这一解耦设计使得后续模型只需专注于生成运动隐变量，而外观保持由肖像 $I$ 保证，显著降低了生成任务的复杂度。

**第二阶段：文本引导的运动生成器。** 运动生成器 $\mathcal{G}$ 是一个基于扩散模型的条件生成模块，根据音频 $A$ 和文本指令 $T$ 生成运动隐变量 $M$，即 $M = \mathcal{G}(A, T)$。该模块以 Conformer 为骨干网络，包含 12 个 Conformer 块，隐状态维度为 768。其内部数据流分为三个关键环节：

1. **音频感知输入块：** 将音频编码特征 $\mathcal{W}(A)$ 通过逐元素加法注入到噪声运动隐变量 $\mathcal{M}_t$ 中，形成音频感知的噪声隐变量 $\mathcal{M}_t^A = \mathcal{M}_t \oplus \mathcal{W}(A)$。这一步将音频的韵律和内容信息与运动生成过程初步绑定。

2. **双分支文本感知降噪块：** 在每个降噪块中，文本信息通过两条独立分支注入模型。**情绪分支**使用 CLIP 文本编码器输出的 [EOS] token，经 Adapter $\mathcal{A}_e$ 对齐后，通过交叉注意力注入全局情绪风格；**动作分支**则利用所有 token 的隐藏状态，经 Adapter $\mathcal{A}_m$ 对齐后，注入细粒度的时序面部动作控制信号。双分支设计实现了全局风格与动态动作的分离控制。

3. **零卷积门控机制：** 文本交叉注意力的输出通过零初始化的一维卷积 $\mathcal{Z}$ 进行门控，再以残差方式加入隐状态：$h_i = h_{i-1} + \mathcal{Z}(\mathrm{CrossAttn}(h, \mathrm{Rep}(\mathbf{T})))$。由于权重和偏置初始化为零，训练起始时该分支输出为零，模型等价于无文本条件的基础模型，从而平稳地逐步引入文本控制信号，充分利用预训练知识并稳定训练过程。

**辅助训练目标。** 在运动生成器末端附加了两个辅助分类头：AU（动作单元）预测头和情绪强度预测头。这些辅助任务迫使模型关注面部的细粒度动态细节，对应的损失项 $\mathcal{L}_{au}$ 和 $\mathcal{L}_{inten}$ 与运动 MSE 损失 $\mathcal{L}_{mse}$、姿态 MSE 损失 $\mathcal{L}_{pose}$ 加权组合为总训练损失 $L = \mathcal{L}_{mse} + \lambda_{pose}\mathcal{L}_{pose} + \lambda_{au}\mathcal{L}_{au} + \lambda_{inten}\mathcal{L}_{inten}$。

**数据流开关。** 由于模型同时训练情绪说话和纯动作控制两类任务，框架中设置了数据流开关（Figure 2 中的 switches）。对于情绪说话任务，音频 $A$ 和情绪指令 $T$ 同时输入；对于无音频的面部动作控制任务，音频输入被置零，仅依赖动作指令 $T$ 驱动生成。这种统一框架使 InstructAvatar 既能完成传统的音频驱动情绪说话人脸生成，也能实现此前方法不具备的纯文本驱动面部动作控制。



InstructAvatar 的整体生成映射为 $V = \mathcal{F}(A, I, T)$，即从音频 $A$、肖像 $I$ 和文本指令 $T$ 生成视频 $V$。其核心架构由两大组件构成：VAE 解耦模块 $\mathcal{H}$ 与扩散运动生成器 $\mathcal{G}$。

### 运动-外观解耦

VAE 模块 $\mathcal{H}$ 将视频的运动信息与外观信息分离，视频可通过运动隐变量 $M$ 和肖像 $I$ 重建：

$$V = \mathcal{H}(M, I)$$

运动生成器 $\mathcal{G}$ 的任务是根据音频和文本指令生成运动隐变量：

$$M = \mathcal{G}(A, T)$$

### 音频感知输入

在扩散去噪过程的输入端，音频特征通过逐元素加法注入噪声运动隐变量：

$$\mathcal{M}_t^A = \mathcal{M}_t \oplus \mathcal{W}(A)$$

其中 $\mathcal{W}$ 为音频编码器，$\oplus$ 表示逐元素相加。这一设计使音频信号直接参与运动生成的初始条件。

### 双分支文本指令表示

文本指令通过 CLIP 编码器 $\mathcal{C}$ 编码后，根据指令类型分别处理：

$$\mathrm{Rep}(T) = \begin{cases} \mathcal{A}_e(\mathcal{C}(T)_{[EOS]}) & \text{若 } T \text{ 为情绪说话指令} \\ \mathcal{A}_m(\mathcal{C}(T)_{all}) & \text{若 } T \text{ 为动作控制指令} \end{cases}$$

- **情绪分支**：取 CLIP 输出的 `[EOS]` token，经 Adapter $\mathcal{A}_e$ 映射，捕获全局情绪风格。
- **动作分支**：取全部 token 的 hidden states，经 Adapter $\mathcal{A}_m$ 映射，保留时序细粒度动作信息。

两个 Adapter 均为两层 MLP，用于对齐文本特征与扩散模型隐空间的分布。

### 零卷积门控注入

文本条件通过交叉注意力与零卷积门控平稳注入每个去噪块：

$$h_i = h_{i-1} + \mathcal{Z}(\mathrm{CrossAttn}(h, \mathrm{Rep}(\mathbf{T})))$$

其中 $\mathcal{Z}$ 为一维卷积操作，其权重和偏置均初始化为零。训练起始时 $h_i = h_{i-1}$，模型等价于无文本条件的原始扩散模型；随着训练推进，门控逐步开放，文本控制信号被平稳引入。这一机制是稳定训练、充分利用预训练知识的关键。

### 辅助监督与总损失

为强化面部细节控制，模型在去噪过程中附加 AU 预测头和情绪强度分类头。总训练损失为四项的加权和：

$$L = \mathcal{L}_{mse} + \lambda_{pose}\mathcal{L}_{pose} + \lambda_{au}\mathcal{L}_{au} + \lambda_{inten}\mathcal{L}_{inten}$$

- $\mathcal{L}_{mse}$：运动隐变量的均方误差。
- $\mathcal{L}_{pose}$：关键点姿态的均方误差。
- $\mathcal{L}_{au}$：动作单元的多标签二元交叉熵损失。
- $\mathcal{L}_{inten}$：情绪强度的交叉熵损失。

### 评价公式

**AU-F1** 衡量生成视频与真值之间多标签动作单元的一致性：

$$\operatorname{AU}_{\mathbf{F1}} = \frac{1}{n} \sum_{j=1}^{n} \frac{2 \sum_{i=1}^{M} \mathbf{y}_i^{(j)} \cdot \hat{\mathbf{y}}_i^{(j)}}{\sum_{i=1}^{M} \mathbf{y}_i^{(j)} + \sum_{i=1}^{M} \hat{\mathbf{y}}_i^{(j)}}$$

其中 $n$ 为 AU 类别数，$M$ 为帧数，$\mathbf{y}_i^{(j)}$ 和 $\hat{\mathbf{y}}_i^{(j)}$ 分别为第 $j$ 类 AU 在第 $i$ 帧的真值与预测值。

**CLIPS 动作控制指标** 评估生成视频与文本指令的语义对齐程度，取所有帧中余弦相似度的最大值：

$$s = \max_i \frac{\mathcal{E}_t(t) \cdot \mathcal{E}_v(v_i)}{\|\mathcal{E}_t(t)\| \cdot \|\mathcal{E}_v(v_i)\|}$$

其中 $\mathcal{E}_t$ 和 $\mathcal{E}_v$ 分别为 CLIP 的文本编码器和视觉编码器，$t$ 为文本指令，$v_i$ 为第 $i$ 帧。



## 实验与关键发现

### 1. 实验设置

**数据集与评估协议**：模型在 MEAD、CC v1 和 HDTF 三个数据集的混合体上进行训练，涵盖多种说话人和情绪类型。评估分为域内（in-domain）和域外（out-of-domain）两组：域内测试在 MEAD 数据集上进行，域外测试在 TalkingHead 1KH 数据集上进行，以检验模型的泛化能力。

**对比基线**：选取了三类代表性方法作为对比：
- **无情绪说话人脸模型**：GAIA、MakeItTalk，用于验证情绪控制模块的增益；
- **基于标签的情绪模型**：EAT，用于对比文本接口相对于离散标签的优势；
- **基于参考视频的情绪模型**：StyleTalk、DreamTalk，用于对比文本控制相对于参考视频驱动的灵活性和精度。

**评价指标**：采用客观指标与主观评分相结合的多维度评估体系：
- **AU_F1**：计算生成视频与真值之间多标签动作单元的 F1 分数，衡量细粒度表情控制精度；
- **SyncD**：衡量唇形同步质量，数值越低越好；
- **FID**：评估生成帧的视觉质量；
- **CLIPS**：计算生成帧与文本指令的余弦相似度最大值，评估指令遵循程度；
- **MOS（Mean Opinion Score）**：邀请人类评估者对情绪表现力（Emo.）和唇形同步质量（Lip.）进行主观打分。

### 2. 情绪说话控制主结果

**Table 1** 展示了域内（MEAD）和域外（TalkingHead 1KH）设置下的客观指标对比。InstructAvatar 在核心指标上取得了最优或次优结果：

- 在域内设置下，AU_F1 达到 **0.738**，优于最强基线 DreamTalk 的 0.711（+0.027），表明文本指令能比参考视频提供更精确的细粒度表情控制。SyncD 为 **9.412**，略优于 GAIA 的 9.542，证明零卷积门控机制在引入文本控制的同时保持了唇形同步质量。
- 在域外设置下，AU_F1 为 **0.552**，仍优于 EAT 的 0.542，验证了模型对未见说话人的泛化能力。值得注意的是，基于标签的 EAT 在域外 AU_F1 上表现尚可（0.542），但其域内 AU_F1 仅为 0.469，显著低于 InstructAvatar，说明自然语言指令比离散标签携带更丰富的控制信息。

**Table 2** 的主观评分进一步印证了上述结论：
- 情绪表现力（Emo.）MOS 在域内达到 **4.64**，域外达到 **4.52**，均优于 DreamTalk（4.59 / 4.45），表明文本驱动的情绪表达更自然、更具感染力。
- 唇形同步质量（Lip.）MOS 在域内达到 **4.74**，域外达到 **4.63**，优于所有基线，证明双分支交叉注意力和零卷积门控的组合设计有效避免了文本控制对音频-唇形对齐的干扰。

**Figure 5** 的定性对比直观展示了 InstructAvatar 的优势：在相同音频和肖像输入下，InstructAvatar 生成的表情更丰富、更贴合指令描述的情绪风格，而基线方法（如 DreamTalk）的表情变化幅度有限，且存在唇形模糊或与音频不同步的问题。

### 3. 文本驱动面部动作控制

**Table 3** 报告了无音频的面部动作控制任务结果。InstructAvatar 在 CLIPS 指标上取得最高分，表明生成的动作序列与文本指令的语义一致性最强。主观评分方面，动作准确性（Motion Acc.）和自然度（Naturalness）均优于基线，证明了双分支交叉注意力中动作分支（使用全部 token hidden states）的设计能够有效捕获时序动作信息。

**Figure 6** 展示了具体的动作控制案例：模型能够执行“挑眉”、“张嘴”、“微笑”等单一动作指令，也能平滑连接多个连续动作（如“先惊讶地挑眉，然后微笑”），展现出良好的时序连贯性和指令遵循能力。

### 4. 消融实验

**Table 4** 和 **Table 5** 通过系统消融验证了各核心设计的必要性：

**零卷积门控**：移除零卷积门控后，SyncD 从 9.412 恶化至 **12.832**，唇形同步质量大幅下降。这验证了零初始化策略的关键作用——训练起始等价于无文本条件模型，使文本控制信号得以平稳注入，避免了对预训练音频-运动对齐的破坏。

**AU 辅助损失**：移除 AU 预测损失后，AU_F1 从 0.738 骤降至 **0.435**，降幅达 41%。这说明辅助的 AU 二元交叉熵损失和情绪强度交叉熵损失对模型学习细粒度面部动作单元至关重要，仅靠扩散模型的 MSE 损失无法充分捕捉微妙的表情变化。

**文本指令 vs. 情绪标签**：将文本指令替换为 one-hot 情绪标签训练时，AU_F1 降至 **0.469**，与基于标签的 EAT 方法（0.469）水平相当。这直接证明了自然语言描述相比离散类别标签能提供更丰富的控制信号，是 InstructAvatar 性能优势的核心来源。

**CLIP Adapter**：去除 Adapter 后，AU_F1 和动作控制 CLIPS 评分均出现下降。Adapter 的作用在于将 CLIP 文本编码器的输出分布对齐到扩散模型的隐空间，简单的直接拼接或交叉注意力无法有效利用预训练的语义知识。

**GPT-4V 转述的有效性**：**Table 6** 的人类评估显示，GPT-4V 转述的动作描述在流畅性和准确性上均优于直接拼接 AU 标签的基线方案。**Figure 11** 的案例进一步表明，GPT-4V 不仅能将 AU 转化为自然语言，还能纠正 AU 检测模型的错误并补充遗漏的动作单元，从而提升训练数据的质量。

### 5. 文本指令的独立控制能力验证

**Figure 9** 通过控制变量实验证明了文本指令的独立控制能力：固定中性肖像和中性音频，仅改变文本指令（如“开心地说话”、“悲伤地说话”、“生气地说话”），生成视频的情绪表达发生显著且符合预期的变化。这排除了音频或外观对情绪表达的混淆影响，确证了文本接口的有效性。

### 6. 失败模式与局限性

尽管 InstructAvatar 在整体指标上表现优异，分析揭示了以下失败模式：

- **动作单元耦合**：训练数据中某些动作单元高度相关（如“嘴角上扬”与“脸颊提升”常同时出现），模型难以实现完全解耦的单一 AU 控制。当指令要求仅激活某个孤立 AU 时，生成结果可能附带其他相关 AU 的变化。
- **域外鲁棒性不足**：域外 AU_F1（0.552）与域内（0.738）存在明显差距，表明模型对极端分布外外观（如夸张卡通风格）或罕见指令组合的泛化能力有限。
- **复合指令处理缺失**：当前模型无法同时处理包含情绪和动作描述的复合文本指令（如“开心地说，同时挑眉”），因为训练样本通常只具备单一类型标签，双分支架构未设计多任务融合机制。

这些局限指向了三个开放问题：如何实现真正独立可组合的动作单元控制；如何在有限数据下提升极端域外泛化能力；以及如何扩展架构以支持情绪与动作的联合文本指令解析。

### 补充图表

![[assets/figures/papers/paper_list_l1499_https_arxiv_org_abs_2405_15758/figures/009_Table_3.jpg]]
*Table 3: Objective and subjective metrics for text-guided facial motion control. Table 4: Ablation studies on the proposed techniques*


![[assets/figures/papers/paper_list_l1499_https_arxiv_org_abs_2405_15758/figures/013_Figure_9.jpg]]
*Figure 9: neutral Fig. 9: Illustration of the effectiveness of textual instructions. All videos are generated utilizing identical portraits and neutral audio, with variations only in the textual instructions*


![[assets/figures/papers/paper_list_l1499_https_arxiv_org_abs_2405_15758/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with baselines for in-domain/out-of-the-domain settings. The bold values indicate the best results, while the underlined values represent the second-best. Guid. Mod. indicates the modality of emotional guidance. Since there is no ground truth video in the out-of-the-domain setting, the FID metric is left empty. It can be observed that our model outperforms the baselines across many metrics. Notably, for SyncD, the ground truth video has a SyncD of 9.172 in the in-domain setting, which is the closest to our model*

![[assets/figures/papers/paper_list_l1499_https_arxiv_org_abs_2405_15758/figures/006_Table_2.jpg]]
*Table 2: Subjective evalution results for InstructAvatar and other baselines for indomain/out-of-the-domain settings. The bold values indicate the best results, while the underlined values represent the second-best*

![[assets/figures/papers/paper_list_l1499_https_arxiv_org_abs_2405_15758/figures/015_Table_5.jpg]]
*Table 5: More ablation studies on the proposed techniques*







## 定位与知识库关联

### 1. 与现有工作的关系

InstructAvatar 处于音频驱动说话人脸生成与细粒度可控生成两条技术路线的交汇点，其核心贡献在于将控制信号从受限的类别标签或参考视频扩展为开放词汇的自然语言文本指令，并通过双分支交叉注意力架构实现全局情绪风格与时序面部动作的解耦控制。

**与无情绪音频驱动模型的对比。** 早期的音频驱动说话人脸生成方法，如 **GAIA** 和 **MakeItTalk**，仅以音频和肖像作为输入，完全缺乏对表情或情绪的控制能力——生成结果的表情由音频信号隐式决定，用户无法指定“高兴地说话”或“悲伤地说话”。InstructAvatar 在保持音频驱动唇形同步能力的前提下，通过文本指令接口赋予用户显式的情绪与动作控制权，这是功能维度的根本性扩展。

**与基于标签的情绪说话人脸模型的对比。** **EAT** 等方法使用 one-hot 情绪标签（如“happy”、“sad”）作为控制信号。这类方法存在两个固有限制：(1) 类别标签只能传达粗粒度的整体情绪风格，无法描述“嘴角微微上扬的同时眉毛轻皱”这类细粒度表情；(2) 类别空间封闭，无法泛化到训练时未见过的情绪描述。InstructAvatar 用自然语言指令替代类别标签，并通过 GPT-4V 将动作单元（AU）转述为自然语言描述，构建了开放词汇的控制通道。消融实验（Table 5）直接验证了这一优势：将文本指令替换为情绪标签训练时，AU_F1 从 0.738 降至 0.469，降幅达 36%，充分说明自然语言描述能提供更丰富的细粒度控制信号。

**与基于参考视频的情绪说话人脸模型的对比。** **StyleTalk** 和 **DreamTalk** 等方法通过参考视频传递情绪风格，用户需要提供一个包含目标表情的示例视频。这种方式的局限在于：(1) 用户必须拥有合适的参考视频，使用门槛高；(2) 参考视频传递的是整体风格，难以独立控制单个动作单元。InstructAvatar 的文本接口天然避免了这两个问题——用户只需输入一句自然语言描述，且文本可以精确指定特定面部动作（如“闭上眼睛”），无需完整参考视频。

**与通用扩散模型可控生成技术的关系。** InstructAvatar 中的零卷积门控机制（zero-convolution gate）在思想上与 ControlNet 的零卷积初始化一脉相承：将新增控制分支的权重和偏置初始化为零，使得训练起始等价于预训练的无控制模型（$h_i = h_{i-1}$），随后逐步引入控制信号。这一设计稳定了训练过程，避免了随机初始化对新模态特征的破坏性干扰。消融实验（Table 4）显示，移除零卷积门控后，唇形同步指标 SyncD 从 9.412 恶化至 12.832，验证了平稳初始化对保持预训练质量的关键作用。

### 2. 适用边界与局限

InstructAvatar 在以下条件下表现良好：
- **域内情绪控制**：在 MEAD 数据集上，AU_F1 达到 0.738，情绪主观评分（MOS）达到 4.64，均优于所有基线方法。
- **域外泛化**：在 TalkingHead 1KH 数据集上，AU_F1 为 0.552，仍保持对基线方法的优势，说明模型具备一定的跨数据集泛化能力。
- **无音频的面部动作控制**：模型支持纯文本驱动的面部动作控制（Figure 6），这是此前方法不具备的功能。

然而，该方法存在以下明确局限：

**动作单元解耦不完全。** 训练数据中的动作单元存在天然相关性（例如“嘴角上扬”常伴随“脸颊提升”），模型难以实现完全独立的单一动作单元控制。论文明确指出，这是训练数据分布导致的固有限制，而非架构缺陷。

**极端域外样本鲁棒性有限。** 当面对高度分布外的指令或外观（如极端卡通风格肖像、训练数据中未出现的复合表情描述）时，模型性能会下降。论文认为需要更大规模和更多样化的训练数据来解决这一问题。

**无法同时处理复合文本指令。** 当前模型的训练样本通常只具备单一类型标签（情绪标签或动作单元标注），因此模型无法解析同时包含情绪描述和动作描述的复合指令（如“高兴地说话，同时眨左眼”）。这是数据构造范式而非模型架构的根本限制。

### 3. 开放问题

基于上述局限，以下问题值得进一步探索：

1. **真正独立的动作单元控制**：如何设计算法或数据构造策略，打破训练数据中动作单元之间的相关性，实现可组合的、完全解耦的细粒度面部控制？这可能需要合成数据、因果解耦学习或对比学习等技术的介入。

2. **极端域外泛化能力提升**：在有限数据资源下，如何显著提升模型对未见表情组合、非写实风格肖像等极端域外样本的鲁棒性？少样本适配、测试时优化或更强的数据增强策略可能是潜在方向。

3. **复合指令解析与执行**：能否扩展模型架构或训练范式，使其能够解析并同时执行包含情绪风格与具体动作描述的复杂文本指令？这需要构建多标签、多类型的指令-视频配对数据集，并设计相应的条件融合机制。

4. **文本控制精度的可量化评估**：当前使用 CLIPS 指标（取所有帧中与文本指令余弦相似度的最大值）评估指令遵循程度，但该指标可能无法捕捉时序上的控制精度。设计更细粒度的文本-视频对齐评估方法，将是推动该方向发展的基础设施性工作。



## 原文 PDF

![[paperPDFs/AAAI_2024/InstructAvatar_Text_Guided_Emotion_and_Motion_Control_for_Avatar_Generation.pdf]]
