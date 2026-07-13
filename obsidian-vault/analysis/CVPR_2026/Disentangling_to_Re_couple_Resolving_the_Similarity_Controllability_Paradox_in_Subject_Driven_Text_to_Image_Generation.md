---
title: "Disentangling to Re-couple: Resolving the Similarity-Controllability Paradox in Subject-Driven Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Disentangling_to_Re_couple_Resolving_the_Similarity_Controllability_Paradox_in_Subject_Driven_Text_to_Image_Generation.pdf
project_link: null
code_link: null
aliases:
- DRCRSCPSDTIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过文本-视觉解耦模块将主体身份信息绑定到参考图像，使提示语仅保留编辑意图，消除冲突来源；再通过群组相对策略优化（GRPO）和专用奖励模型重耦合视觉主体与文本背景，克服合成不自然问题。
primary_logic: 主体身份应完全由视觉参考图像定义，文本提示语应仅用于表达编辑需求；分离后通过强化学习使模型学会将纯视觉主体与纯文本上下文自然融合，从而同时获得高相似性和高可控性。
claims:
- 将提示语中的实体词替换为通用代词后，生成图像对参考主体的保真度明显提高（如鸭玩具、蜡烛案例）。
- 解耦后注意力图显示，来自文本实体词的不利注意力被抑制，而来自参考图像主体的注意力精确聚焦于生成图像的对应区域。
- DisCo 在 DreamBench 上实现了最高的主体相似度（CLIP‑I 0.928）和最高的文本对齐度（CLIP‑T 0.329）以及 ImageReward（1.339），全面超越所有基线。
- 消融实验表明，去掉文本-视觉解耦模块或去掉 GRPO 均导致相似度和/或文本对齐度显著下降，确认两个组件的必要性。
---

# Disentangling to Re-couple: Resolving the Similarity-Controllability Paradox in Subject-Driven Text-to-Image Generation

> [!tip] 核心洞察
> 主体身份应完全由视觉参考图像定义，文本提示语应仅用于表达编辑需求；分离后通过强化学习使模型学会将纯视觉主体与纯文本上下文自然融合，从而同时获得高相似性和高可控性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 解耦与重耦合：解决主体驱动文本生成图像中的相似性-可控性悖论 |
| 英文题名 | Disentangling to Re-couple: Resolving the Similarity-Controllability Paradox in Subject-Driven Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.00849) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | DisCo |
| Dataset | DreamBench, Human evaluation |

> [!tip] 效果简介
> - DreamBench 上，CLIP‑B‑I (subject similarity) 0.928 vs 0.899 (UNO / DreamO) (+0.029)；DINO‑I (subject similarity) 0.903 vs 0.827 (UNO) (+0.076)；CLIP‑B‑T (text controllability) 0.329 vs 0.322 (DreamO) / 0.311 (UNO) (+0.007 / +0.018)。
> - DreamBench++ 上，CLIP‑B‑I 0.801 vs 0.795 (DreamO) (+0.006)；DINO‑I 0.610 vs 0.589 (DreamO) (+0.021)。
> - Human evaluation (100 cases) 上，Win rate vs. UNO 80% vs — (—)。

## 概要

**核心问题：相似性-可控性悖论。** 主体驱动文本生成图像（Subject-Driven Text-to-Image Generation）任务要求生成图像既忠实保留参考主体的视觉身份，又准确遵循文本提示语中的编辑指令。现有方法普遍面临一个根本性冲突：文本提示语同时承担了“描述主体”和“下达修改指令”的双重角色。当模型从文本中获取的主体先验与参考图像提供的视觉特征不一致时，二者发生对抗，导致主体保真度受损或编辑意图被削弱——这一现象被本文定义为相似性-可控性悖论（Similarity-Controllability Paradox）。

**核心洞察：解耦信息源，再重耦合。** 本文的核心主张是：主体身份信息应完全由视觉参考图像定义，文本提示语应仅用于表达编辑需求。基于此，DisCo 框架采用“先解耦、后重耦合”的策略：首先通过文本-视觉解耦模块将两种信息源彻底分离，消除冲突根源；随后利用群组相对策略优化（GRPO）和专用奖励模型，使模型学会将纯视觉主体与纯文本上下文自然融合，从而同时获得高主体相似性和高文本可控性。

**方法定位。** DisCo 并非重新设计扩散模型架构，而是在现有 FLUX 基础模型上构建了一个两阶段训练范式。第一阶段引入文本-视觉解耦（TVD）模块，利用视觉语言模型识别并替换提示语中的实体词为通用代词，同时通过视觉定位模型将主体身份绑定到参考图像的视觉特征上；第二阶段引入 GRPO 强化学习，配合基于合成偏好数据训练的奖励模型，对解耦后可能出现的合成不自然问题进行矫正。该方法在方法谱系上属于“编码器注入 + 强化学习后训练”的混合路径，区别于纯编码器方法（如 IP-Adapter、SSR-Encoder）和纯上下文生成方法（如 UNO、FLUX Kontext）。

**主要结果。** 在 DreamBench 基准上，DisCo 实现了最高的主体相似度（CLIP-I 0.928，DINO-I 0.903）和最高的文本对齐度（CLIP-T 0.329），综合质量指标 ImageReward 达到 1.339，全面超越包括 DreamO、UNO、FLUX Kontext 在内的所有基线方法。消融实验证实，移除 TVD 模块或 GRPO 阶段均导致相似度和/或文本对齐度显著下降，验证了两个组件的必要性。在 DreamBench++ 上的泛化测试和人类评估（100 组对比中胜率超 80%）进一步支撑了方法的有效性和鲁棒性。



### 主体驱动生成中的相似性-可控性悖论

主体驱动文本生成图像（Subject-Driven Text-to-Image Generation）旨在根据一张参考图像和一段文本提示语，生成保留参考主体身份、同时服从文本编辑指令的图像。这一任务面临一个根本性困境——**相似性-可控性悖论**：文本提示语同时承担着“描述主体”和“下达修改指令”的双重角色。模型从文本中获得的主体先验（如类别、形状、纹理等）往往与参考图像提供的视觉特征产生冲突，导致生成结果要么主体保真度受损，要么编辑指令执行不彻底。

Figure 1 直观展示了这一现象：当提示语中包含具体实体词（如“a toy duck”、“a candle”）时，即使参考图像中的主体外观与文本先验存在偏差，生成结果也会向文本先验倾斜，损害保真度。这一冲突的根源在于，现有方法（如 FLUX Kontext、IP-Adapter 等）将文本条件与视觉条件**纠缠**在一起注入模型，使模型难以分辨身份信息究竟应来自文本还是图像。

### 现有方法的局限

当前主流的主体驱动生成方法大致可分为两类：

- **基于编码器的方法**（如 **IP-Adapter**（Ye et al., arXiv 2023）、**SSR-Encoder**（Zhang et al., 2024）、**RealCustom++**（Duan et al., 2024））：通过独立的图像编码器将参考主体特征注入扩散模型，但文本提示语中仍保留实体词，文本先验与视觉特征之间的冲突未被消除。
- **基于统一序列的方法**（如 **OminiControl**（Tan et al., arXiv 2024）、**ACE++**、**UNO**、**DreamO**）：将参考图像令牌直接拼接到文本令牌序列中，利用多模态注意力机制融合信息。这类方法虽然简化了架构，但同样面临文本-视觉信息纠缠的问题——实体词在注意力计算中会与参考图像令牌竞争，引入不利于保真度的文本先验。

Figure 2 的注意力可视化揭示了这一机制：在未解耦时，文本实体词对生成图像区域产生显著的不利注意力；而参考图像主体的注意力则相对分散，无法精确聚焦于生成图像的对应区域。这表明，**只要文本提示语中保留实体词，文本先验就会通过注意力机制干扰主体身份的表达**。

### 核心动机：解耦与重耦合

本文的核心洞察是：**主体身份应完全由视觉参考图像定义，文本提示语应仅用于表达编辑需求**。基于这一洞察，DisCo 框架提出“先解耦，后重耦合”的策略：

1. **解耦（Disentangle）**：通过文本-视觉解耦模块（TVD），将提示语中的实体词替换为通用代词（如“this item”、“it”），使文本仅携带编辑意图；同时利用 GroundingDINO 从参考图像中定位并提取主体视觉特征，彻底切断文本对主体身份的影响。
2. **重耦合（Re-couple）**：解耦虽然消除了冲突来源，但可能导致主体与背景的合成不自然。DisCo 引入群组相对策略优化（GRPO）作为第二阶段训练，并配套训练一个专门的奖励模型，使模型学会将纯视觉主体与纯文本上下文自然融合，从而同时获得高相似性和高可控性。

这一范式的核心优势在于从根源上消除了文本-视觉冲突，而非在冲突发生后进行妥协或折中。后续章节将详细阐述 DisCo 的方法设计、实验验证及其相对于现有基线的显著提升。



## 核心方法与创新机理

DisCo 的核心创新在于识别并解决主体驱动文本生成图像中长期存在的**相似性-可控性悖论**。在传统方法中，文本提示语同时承担描述主体身份和下达修改指令的双重功能，导致模型从文本中获得的主体先验与参考图像的视觉特征产生冲突，损害生成图像对参考主体的保真度（见 Figure 1）。DisCo 通过“解耦-重耦合”两阶段框架从根本上消除这一冲突，其关键创新体现在以下三个维度的设计转变上。

### 1. 提示语功能的重定义：从双角色纠缠到纯指令化

传统方法（如 FLUX Kontext、IP-Adapter、SSR-Encoder 等）的提示语中，实体词（如“a duck toy”）同时参与主体特征控制，使文本信号与视觉信号纠缠在一起。DisCo 的**文本-视觉解耦模块（TVD）** 从根本上改变了这一设计：利用 VLM 识别提示语中的实体词，将其替换为通用代词（如“this item”或“it”），使提示语仅保留编辑意图（如“this item on a beach”）。主体身份信息则完全由参考图像通过 GroundingDINO 定位后提取的视觉特征来定义。这一设计转变的核心逻辑在于：**主体身份应完全由视觉参考图像定义，文本提示语应仅用于表达编辑需求**。

Figure 2 的注意力图可视化为这一创新提供了直接证据：解耦前，文本实体词对生成图像产生不利的注意力干扰；解耦后，来自实体词的注意力被抑制，而来自参考图像主体的注意力精确聚焦于生成图像的对应区域，证明模型已学会从纯视觉来源获取主体信息。

### 2. 主体身份引入方式的转变：从多源混合到纯视觉绑定

基线方法（如 IP-Adapter、SSR-Encoder、RealCustom++）通常通过文本描述和参考图像编码器共同注入主体信息，这种多源混合不可避免地引入信息冲突。DisCo 将主体身份引入方式转变为**纯视觉绑定**：通过 GroundingDINO 从参考图像中定位并提取主体视觉特征，文本流中不再提供任何主体相关信号。这一转变消除了文本先验对视觉保真度的干扰，使模型在生成过程中仅依赖参考图像的视觉特征来还原主体外观。

### 3. 训练策略的升级：从纯监督学习到强化学习重耦合

解耦操作虽然解决了信息冲突，但也引入了一个新问题：纯视觉主体与纯文本上下文之间的合成可能不够自然，出现“组合鸿沟（compositional gap）”。DisCo 在传统扩散损失的基础上，创新性地引入**群组相对策略优化（GRPO）** 作为第二阶段训练，并配套训练一个专用的奖励模型（基于 Qwen3-VL-30B），通过自动合成的负样本偏好数据训练该奖励模型，使其能够评估主体相似性和合成和谐度。

GRPO 的核心机制在于：对同一提示语生成一组图像（12 张），利用奖励模型计算每张图像的偏好得分，通过组内相对优势 $\hat{A}_t^i$ 进行策略优化：

$$\hat{A}_t^i = \frac{R(x_0^i, c) - \mathrm{mean}(\{R(x_0^i, c)\}_{i=1}^G)}{\mathrm{std}(\{R(x_0^i, c)\}_{i=1}^G)}$$

这一设计使模型在强化学习的引导下学会将纯视觉主体与纯文本上下文自然融合，实现“重耦合”。消融实验（Table 2）明确验证了这一创新的必要性：仅使用 TVD 模块时，虽然主体相似度保持较高（CLIP-I 0.922），但文本对齐度（CLIP-T 0.319）和整体质量（ImageReward 1.189）显著低于完整模型（CLIP-T 0.329, ImageReward 1.339），表明 GRPO 对克服解耦后的合成不自然问题至关重要。

### 创新总结

DisCo 的三个 changed slots——提示语功能纯指令化、主体身份纯视觉绑定、训练策略引入 GRPO 强化学习——构成了一个逻辑自洽的创新链条：解耦消除冲突来源，重耦合恢复合成自然度。这一范式转变使 DisCo 在 DreamBench 上同时实现了最高的主体相似度（CLIP‑I 0.928）和文本可控性（CLIP‑T 0.329），突破了传统方法在相似性与可控性之间的权衡困境。



DisCo 框架的核心设计理念源于对主体驱动生成中**相似性-可控性悖论**的因果剖析：文本提示语同时承担“描述主体”和“下达修改指令”的双重角色，导致模型从文本获得的主体先验与参考图像的视觉特征发生冲突。DisCo 通过“先解耦、后重耦合”的两阶段策略从根本上消除这一冲突源。

### 框架总览

如图 3 所示，DisCo 由三个核心模块串联构成一个闭环 pipeline：

1. **文本-视觉解耦模块（Textual-Visual Decoupling, TVD）**：将主体身份信息与文本控制信号彻底分离。主体身份完全由参考图像定义，文本提示语仅保留编辑意图。
2. **奖励模型训练**：基于合成负面样本，训练一个专用偏好预测器，用于评估生成图像在主体相似性和合成和谐度两个维度上的质量。
3. **群组相对策略优化重耦合阶段（GRPO Re-coupling）**：以奖励模型为反馈信号，通过强化学习使模型学会将纯视觉主体与纯文本上下文自然融合。

### 输入输出流

整个 pipeline 的输入包括两部分：一张包含目标主体的参考图像和一条描述所需编辑的文本提示语。输出为一张既保留参考主体视觉特征、又严格遵循文本编辑指令的生成图像。

具体流程如下：

**第一阶段——解耦**：TVD 模块接收原始提示语和参考图像。它利用视觉语言模型识别提示语中的实体词（如“a yellow duck toy”中的“duck toy”），将其替换为通用代词（如“this item”或“it”），使提示语仅携带编辑指令。同时，使用 GroundingDINO 对参考图像中的主体进行视觉定位，提取其视觉特征。经过解耦后，文本条件令牌 $\mathbf{C}_T$ 和图像条件令牌 $\mathbf{C}_I$ 分别携带着互不重叠的信息——前者只包含编辑意图，后者只包含主体身份。

**第二阶段——重耦合**：解耦后的条件输入到基于 FLUX 的扩散模型中。然而，仅靠解耦会导致合成不自然的问题——模型难以将“无上下文”的视觉主体与文本描述的编辑场景和谐拼接。为此，DisCo 引入 GRPO 强化学习阶段：首先生成一组候选图像，由专门训练的奖励模型对每张图像进行评分（综合主体相似度和合成和谐度），然后通过群组相对策略优化更新模型参数，使其逐步学会将视觉主体与文本上下文自然融合。

### 基础模型架构

DisCo 建立在 FLUX 扩散模型之上，其多模态注意力机制将噪声图像令牌 $\mathbf{X}$、文本条件令牌 $\mathbf{C}_T$ 和参考图像令牌 $\mathbf{C}_I$ 拼接为统一序列 $\mathbf{S} = [\mathbf{X}; \mathbf{C}_T; \mathbf{C}_I]$，并通过标准注意力计算实现跨模态信息融合：

$$\mathbf{MMA}([\mathbf{X}; \mathbf{C}_T; \mathbf{C}_I]) = \mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d}}\right)V$$

解耦操作的核心效果在于改变了注意力分布：原始设置中，文本实体词会向生成图像注入主体相关的先验信息，与参考图像特征产生冲突；解耦后，来自实体词的注意力被抑制，而来自参考图像主体的注意力精确聚焦于生成图像的对应区域（见 Figure 2）。这一注意力重定向机制是 DisCo 实现高主体相似度的关键。

### 补充图表

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/003_Figure_3.jpg]]
*Figure 3: The architecture of our proposed DisCo framework. DisCo first decouples subject identity (from the image) from textual control (from the prompt). We generate corrupted images to construct preference pairs with the ground truth images to train the Reward Model. Subsequently, it employs GRPO to re-couple textual and visual features, generating a coherent image that preserves subject details while adhering to the prompt*



DisCo 框架围绕“解耦—重耦合”这一核心思想，设计了三个关键模块：文本-视觉解耦（TVD）模块、奖励模型训练、以及群组相对策略优化（GRPO）重耦合阶段。整体架构如图 Figure 3 所示。

### 3.1 多模态注意力基础

DisCo 建立在 FLUX 扩散模型的多模态注意力机制之上。给定噪声图像令牌 $\mathbf{X}$、文本条件令牌 $\mathbf{C}_T$ 和参考图像令牌 $\mathbf{C}_I$，模型首先将它们拼接为统一的多模态序列：

$$\mathbf{S} = [ \mathbf{X}; \mathbf{C}_T; \mathbf{C}_I ]$$

随后在该序列上执行标准注意力计算：

$$\mathbf{MMA}( [ \mathbf{X}; \mathbf{C}_T; \mathbf{C}_I ] ) = \mathrm{softmax}\left( \frac{Q K^\top}{\sqrt{d}} \right) V$$

这一机制使得文本、图像和参考图像的信息在注意力层中相互融合，但同时也正是文本与视觉条件在此处的纠缠，成为了相似性-可控性悖论的根源。

### 3.2 文本-视觉解耦（TVD）模块

TVD 模块是 DisCo 解决悖论的核心机制。其基本洞察是：**主体身份应完全由参考图像定义，文本提示语应仅用于表达编辑需求**。该模块从两个维度实现解耦：

**提示语简化**：利用视觉语言模型（VLM）识别提示语中描述主体的实体词，将其替换为通用代词（如“this item”或“it”），使提示语仅保留编辑指令，不再携带主体身份信息。例如，将“a photo of a red toy duck on the beach”简化为“a photo of this item on the beach”。

**视觉主体定位**：使用 GroundingDINO 从参考图像中定位主体区域，将主体视觉特征作为唯一的身份来源注入模型。

解耦的效果可通过注意力图直观验证（见 Figure 2）。在解耦前，文本实体词对生成图像存在广泛且不利的注意力分布；解耦后，来自实体词的注意力被抑制，而来自参考图像主体的注意力精确聚焦于生成图像的对应区域，表明模型已将主体特征来源从文本切换为视觉参考。

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/002_Figure_2.jpg]]
*Figure 2: Visualization of the attention maps between entity word and subject to the generated image, respectively*

### 3.3 奖励模型训练

解耦后，模型失去了文本对主体的描述性引导，可能导致主体与背景的合成不自然。为解决这一问题，DisCo 训练了一个专用的奖励模型，用于评估生成图像在主体相似性和合成和谐度两个维度上的质量。

奖励模型基于 **Qwen3-VL-30B**，通过自动合成的偏好对进行训练。具体而言，对真实图像施加局部破坏（如模糊、扭曲主体区域或替换背景）生成负面样本，构造正负例对 $(x_0, \tilde{x}_0)$。训练损失为负对数似然：

$$\mathcal{L}_{\phi} = \mathbb{E}_{(x_0,\tilde{x}_0,c_I,c_T)\sim\mathcal{D}} \left[ -\log P_{\phi}(x_0 \succ \tilde{x}_0 \mid c_I, c_T) \right]$$

其中 $P_{\phi}(x_0 \succ \tilde{x}_0 \mid c_I, c_T)$ 表示在给定参考图像条件 $c_I$ 和文本条件 $c_T$ 下，$x_0$ 优于 $\tilde{x}_0$ 的预测概率。

### 3.4 GRPO 重耦合阶段

在获得奖励模型后，DisCo 引入群组相对策略优化（GRPO）作为第二阶段训练，使生成模型学会将纯视觉主体与纯文本上下文自然融合。

对于每个条件 $c$，从旧策略 $\pi_{\theta_{\mathrm{old}}}$ 中采样一组 $G$ 张图像 $\{x^i\}_{i=1}^G$。每张图像的奖励定义为其在组内击败所有其他样本的概率之和：

$$R_i = \sum_{1 \le j \le G} P_{\phi}(x_0^i \succ x_0^j \mid c_I, c_T)$$

随后计算归一化优势：

$$\hat{A}_t^i = \frac{R(x_0^i, c) - \mathrm{mean}(\{R(x_0^i, c)\}_{i=1}^G)}{\mathrm{std}(\{R(x_0^i, c)\}_{i=1}^G)}$$

GRPO 的策略优化目标为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{c \sim C, \{x^i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}(\cdot \vert c)} f(r, \hat{A}, \theta, \varepsilon, \beta)$$

其中 $f(\cdot)$ 的具体形式为包含剪切比率和 KL 惩罚的代理损失：

$$f(\cdot) = \frac{1}{G} \sum_{i=1}^G \frac{1}{T} \sum_{t=0}^{T-1} \left[ \min\left( r_t^i(\theta) \hat{A}_t^i, \mathrm{clip}(r_t^i(\theta), 1-\varepsilon, 1+\varepsilon) \hat{A}_t^i \right) - \beta \mathbb{D}_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}}) \right]$$

其中 $r_t^i(\theta) = \frac{p_\theta(x_{t-1}^i | x_t^i, c)}{p_{\theta_{\mathrm{old}}}(x_{t-1}^i | x_t^i, c)}$ 是新旧策略在去噪步 $t$ 的概率比值，$\varepsilon$ 控制剪切范围，$\beta$ 控制 KL 惩罚强度。这一设计使得模型在保持生成多样性的同时，向高奖励方向稳定更新，最终实现视觉主体与文本上下文的重耦合。

### 补充图表

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/001_Figure_1.jpg]]
*Figure 1: The results with different prompts of the same reference image generated by FLUX Kontext [dev]*

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/012_Figure_9.jpg]]
*Figure 9: The prompt used to generate editing instructions*



## 实验与关键发现

### 核心定量结果：DreamBench 上的全面领先

DisCo 在 DreamBench 基准上系统性地超越了所有对比方法，在主体相似度、文本可控性和整体图像质量三个维度均取得最优（Table 1）。具体而言，DisCo 的主体相似度指标 CLIP‑B‑I 达到 **0.928**，相比最强基线 UNO / DreamO（0.899）提升 +0.029；DINO‑I 达到 **0.903**，较 UNO（0.827）大幅领先 +0.076。在文本对齐度方面，DisCo 的 CLIP‑B‑T 为 **0.329**，超越 DreamO（0.322）和 UNO（0.311）。更关键的是，综合质量指标 ImageReward 达到 **1.339**，相比 DreamO（1.186）提升 +0.153，表明解耦-重耦合策略不仅解决了相似性-可控性冲突，还显著改善了合成图像的自然度和和谐度。

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of DisCo and baselines on DreamBench. Bold and underline represent the highest and second-highest metrics, respectively*

这一优势在更具挑战性的 DreamBench++ 上同样保持：DisCo 的 CLIP‑B‑I 为 0.801（vs. DreamO 0.795），DINO‑I 为 0.610（vs. DreamO 0.589），验证了方法的泛化能力（Table 4）。

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/013_Table_4.jpg]]
*Table 4: Quantitative results on DreamBench++*

### 消融实验：TVD 与 GRPO 的因果贡献

Table 2 的消融实验清晰揭示了文本-视觉解耦模块（TVD）和群组相对策略优化（GRPO）各自的因果作用：

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/009_Table_2.jpg]]
*Table 2: Ablation study of DisCo on DreamBench. TVD represents Textual-visual Decoupling Module*

- **移除 TVD**（仅保留 GRPO）：CLIP‑I 从 0.928 降至 0.915，CLIP‑T 从 0.329 降至 0.319。这确认了解耦操作对主体相似度和文本可控性的双重贡献——当提示语中的实体词未被替换为通用代词时，文本先验会干扰视觉主体特征的准确提取。
- **移除 GRPO**（仅保留 TVD）：CLIP‑I 仍保持在 0.922 的较高水平，但 CLIP‑T 降至 0.319，ImageReward 从 1.339 骤降至 1.189。这表明解耦后的纯视觉主体与纯文本上下文之间确实存在“合成鸿沟”（compositional gap），仅靠解耦无法保证自然融合，GRPO 的强化学习阶段对文本对齐和整体合成质量具有不可替代的作用。
- **完整 DisCo**（TVD + GRPO）：三项指标均达到最高（CLIP‑I 0.928, CLIP‑T 0.329, ImageReward 1.339），验证了两组件协同工作的必要性。

### 人类评估：感知质量的优势确认

在 100 组随机抽样的成对人类评估中（Figure 6），DisCo 相对于各基线取得了压倒性胜率：
- vs. UNO：**80%** 胜率
- vs. DreamO：**82%** 胜率
- vs. OminiControl：71% 胜率
- vs. ACE++：66% 胜率

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/007_Figure_6.jpg]]
*Figure 6: Pairwise human evaluation on 100 cases*

即便面对强基线 FLUX Kontext [dev]，DisCo 仍以 51% 胜率（24% 负率）获得多数偏好。这一结果与自动化指标高度一致，确认 DisCo 生成的图像在主体保真度和编辑合理性方面更符合人类感知。

### 失败模式与局限性

尽管 DisCo 在整体上表现优异，其设计仍存在若干可识别的失败模式和局限：

1. **解耦阶段的 VLM 依赖**：TVD 模块需要外部 VLM 识别提示语中的实体词并改写为通用代词。在复杂实体（如多词构成的专有名词）或罕见描述场景中，VLM 可能产生识别错误或不当简化，导致输入条件质量下降，进而影响生成结果。
2. **奖励模型的领域泛化**：GRPO 阶段依赖专门训练的奖励模型，该模型基于合成负面样本训练。当测试场景的分布与训练数据存在显著偏移时，奖励信号的准确性可能衰减，影响重耦合效果。
3. **多主体场景未覆盖**：当前方法仅针对单主体生成设计，多主体场景下的解耦（多个视觉主体与文本指令的分离）和重耦合（多主体与背景的协调）机制尚未探索，构成明确的扩展边界。
4. **计算开销**：GRPO 训练需要维护奖励模型并执行群组采样（每提示语 12 张图像），相比纯监督学习方法增加了训练成本。

### 实验设置公平性说明

所有基线均使用官方开源代码及默认超参数在 DreamBench 上测评，涵盖 30 个主体和 750 个评测案例。主体相似度采用 SAM 分割后再计算 CLIP‑I/DINO‑I，文本对齐度使用多种 CLIP 模型评估，辅以 ImageReward 综合评分。人类评估基于随机抽样的 100 组图片对，由多位评估者进行偏好判断。这些措施保证了对比的公平性和结论的可靠性。

### 补充图表

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison with baseline methods on DreamBench*

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results on complex scenarios*

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/011_Table_3.jpg]]
*Table 3: Quantitative results on DreamBench*

![[assets/figures/papers/paper_list_l2306_https_arxiv_org_abs_2604_00849/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative results with leading general image editing candlemodels*



## 定位与知识库关联

### 1. 问题谱系：从“编码器注入”到“统一序列”再到“解耦-重耦合”

主体驱动生成（Subject-Driven Generation）的核心矛盾在于**相似性-可控性悖论**：文本提示语同时承担“描述主体”和“下达编辑指令”的双重功能，导致模型从文本中获得的主体先验与参考图像的视觉特征产生冲突。已有方法沿两条技术路线试图缓解这一问题，但均未从根本上解决冲突。

**（1）基于编码器的注入方法（Encoder-based Injection）**  
以 **IP-Adapter**（Ye et al., arXiv 2023）、**SSR-Encoder**（Zhang et al., 2024）和 **RealCustom++**（Duan et al., 2024）为代表的 SDXL 体系方法，通过额外的图像编码器将参考主体特征注入扩散模型的交叉注意力层。这类方法的根本局限在于：文本提示语中的实体词仍然参与注意力计算，文本先验与视觉先验在特征空间中持续竞争，导致主体保真度在复杂编辑指令下显著退化。

**（2）统一序列方法（Unified Sequence Methods）**  
以 **OminiControl**（Tan et al., arXiv 2024）、**ACE++**、**UNO**、**DreamO** 和 **FLUX Kontext [dev]** 为代表的 FLUX 体系方法，将参考图像令牌与文本令牌拼接为统一的多模态序列，通过多模态注意力（MMA）联合建模。如公式所示：

$$\mathbf{S} = [ \mathbf{X}; \mathbf{C}_T; \mathbf{C}_I ]$$

$$\mathbf{MMA}( [ \mathbf{X}; \mathbf{C}_T; \mathbf{C}_I ] ) = \mathrm{softmax}\left( \frac{Q K^\top}{\sqrt{d}} \right) V$$

这种设计虽然增强了视觉条件的表达能力，但**并未阻断文本实体词对主体特征的不利影响**——文本中实体词对应的注意力仍会干扰参考图像主体特征的精确传递（见 Figure 2 的注意力图可视化证据）。

**（3）DisCo 的解耦-重耦合范式**  
DisCo 的核心突破在于**重新定义了信息源的责任边界**：主体身份应完全由视觉参考图像定义，文本提示语应仅用于表达编辑需求。这一设计哲学通过两个关键模块实现：

- **文本-视觉解耦模块（TVD）**：利用 VLM 识别提示语中的实体词，将其替换为通用代词（如 "this item"），使文本不再携带主体相关信号；同时用 GroundingDINO 从参考图像中定位并提取主体视觉特征。
- **GRPO 重耦合阶段**：在解耦后，模型面临“纯视觉主体”与“纯文本上下文”之间的合成鸿沟。DisCo 引入群组相对策略优化（GRPO），配合专门训练的奖励模型（基于 Qwen3-VL-30B），使模型学会将二者自然融合。

这一范式与现有方法的本质区别在于：**它不是“缓解”冲突，而是“消除”冲突来源**——通过彻底分离信息源，从根本上避免了文本先验与视觉先验的竞争。

### 2. 方法谱系中的位置：强化学习驱动的后训练优化

DisCo 的另一个重要定位在于**将强化学习引入主体驱动生成任务**。在扩散模型的后训练优化谱系中：

- 主流方法仅使用扩散损失进行监督学习（如 IP-Adapter、SSR-Encoder 等）。
- DisCo 在标准扩散训练之后，增加了 GRPO 强化学习阶段，利用奖励模型的偏好信号调整生成策略。GRPO 的目标函数为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{c \sim C, \{x^i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}(\cdot \vert c)} f(r, \hat{A}, \theta, \varepsilon, \beta)$$

其中优势函数通过组内标准化计算：

$$\hat{A}_t^i = \frac{R(x_0^i, c) - \mathrm{mean}(\{R(x_0^i, c)\}_{i=1}^G)}{\mathrm{std}(\{R(x_0^i, c)\}_{i=1}^G)}$$

这一设计使 DisCo 成为**主体驱动生成领域中率先将 GRPO 与专用奖励模型结合的框架**，为后续研究开辟了“解耦-强化学习-重耦合”的新技术路线。

### 3. 适用边界与局限

**（1）外部依赖与鲁棒性边界**  
解耦过程依赖外部 VLM 识别实体词并改写提示语。在复杂实体或罕见描述场景中，VLM 的识别错误会直接污染输入条件质量，形成级联误差。当前论文未提供 VLM 识别失败率的定量分析，这一边界需要进一步验证。

**（2）计算与工程开销**  
GRPO 训练需要额外训练奖励模型（基于 Qwen3-VL-30B）并合成偏好数据对。训练配置为 8 张 NVIDIA H20 80G GPU，GRPO 阶段每提示语生成 12 张图像用于组内比较（采样步数 16，噪声水平 0.3），带来了显著的计算和工程开销。

**（3）任务范围限制**  
目前 DisCo 仅展示单主体生成能力。多主体场景下的“分离-重组”机制尚未探索——当多个主体同时存在时，如何解耦各自的视觉特征并独立控制编辑指令，仍是一个开放问题。

**（4）奖励模型的泛化性**  
奖励模型的质量直接影响 GRPO 的优化方向。当前奖励模型基于合成负面样本训练，其在分布外主体类别或极端编辑指令下的泛化能力尚未得到充分验证。

### 4. 开放问题

1. **多主体扩展**：解耦-重耦合范式是否可无缝扩展到多主体或交互式编辑任务？需要设计何种机制来独立绑定多个主体的视觉特征？
2. **视觉绑定的鲁棒性**：通用代词是否在所有语言和概念上都能有效阻止模型引入文本先验？是否存在更稳健的视觉绑定机制（如可学习的视觉占位符）？
3. **自监督反馈信号**：能否设计完全自监督的反馈信号替代人工设计的奖励模型，降低训练成本并提升泛化性？
4. **人机偏好对齐**：在更大规模的用户交互场景中，人类对合成自然度的偏好与自动化指标（CLIP-I、CLIP-T、ImageReward）的一致性如何演变？当前人类评估（100 组）的规模有限，需要更大规模的研究验证。
5. **与通用图像编辑的融合**：Figure 8 展示了 DisCo 与通用图像编辑模型的对比，但解耦-重耦合范式是否可以与 InstructPix2Pix 等编辑方法深度融合，形成统一的“主体保持+指令编辑”框架？



## 原文 PDF

![[paperPDFs/CVPR_2026/Disentangling_to_Re_couple_Resolving_the_Similarity_Controllability_Paradox_in_Subject_Driven_Text_to_Image_Generation.pdf]]
