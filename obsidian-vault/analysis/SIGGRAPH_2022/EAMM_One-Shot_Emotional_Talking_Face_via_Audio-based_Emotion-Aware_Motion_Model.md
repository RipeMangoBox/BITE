---
title: "EAMM: One-Shot Emotional Talking Face via Audio-based Emotion-Aware Motion Model"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/EAMM_One_Shot_Emotional_Talking_Face_via_Audio_based_Emotion_Aware_Motion_Model.pdf
project_link: null
code_link: null
aliases:
- EEAMM
- EAMM
tags:
- SIGGRAPH_2022
- topic/vision_multimodal_applications
core_operator: 情绪动态被建模为面部相关的无监督关键点及其仿射变换上的线性可加位移，通过隐式情绪位移学习器从源视频中提取并叠加到音频驱动的中性运动表示上。
primary_logic: 无监督学习的面部相关关键点和雅可比矩阵之间的线性可加性，使得情绪可以从一个视频转移到另一个视频，而不会干扰口型运动和身份。
claims:
- 面部区域仅由三个面部相关关键点影响，且它们的相对位移是线性可加的。
- 情绪信息可以通过从情感视频中提取的关键点位移来编码并叠加到音频驱动的中性表示上。
- 隐式情绪位移学习器及其数据增强策略能够从源视频中提取仅含情绪的面部位移，抑制讲话内容和姿态的影响。
- LRW 上 M-LMD↓ = 1.61
---

# EAMM: One-Shot Emotional Talking Face via Audio-based Emotion-Aware Motion Model

> [!tip] 核心洞察
> 无监督学习的面部相关关键点和雅可比矩阵之间的线性可加性，使得情绪可以从一个视频转移到另一个视频，而不会干扰口型运动和身份。

| 字段 | 内容 |
|------|------|
| 中文题名 | EAMM：基于音频情绪感知运动模型的单样本情绪化说话人脸生成 |
| 英文题名 | EAMM: One-Shot Emotional Talking Face via Audio-based Emotion-Aware Motion Model |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://arxiv.org/abs/2205.15278) · [paper](https://arxiv.org/abs/2205.15278") |
| Topic | #topic/vision_multimodal_applications |
| Method | EAMM (Emotion-Aware Motion Model) |
| Dataset | LRW, MEAD |

> [!tip] 效果简介
> - LRW 上，M-LMD↓ 1.61 vs 1.67 (PC-AVS) (-0.06)。
> - MEAD 上，M-LMD↓ 2.41 vs 2.97 (PC-AVS) (-0.56)。
> - MEAD (emotion accuracy) 上，Acc_emo↑ 68.41 vs 14.07 (A2FD, neutral baseline) (+54.34)。

## 概要

**问题**：在单样本设定下，如何从任意情绪源视频中提取并传递情绪动态，同时保留音频同步口型和身份不变。

**方法**：提出 EAMM（Emotion-Aware Motion Model），包含两个核心模块——Audio2Facial-Dynamics 模块以无监督关键点及其一阶雅可比矩阵建模音频驱动的中性面部运动；Implicit Emotion Displacement Learner 从情绪源视频中提取仅含情绪的面部关键点位移，将其作为线性可加项叠加到中性运动表示上，实现情绪迁移。

**主要结果**：在 MEAD 数据集上，M-LMD 降至 2.41（PC-AVS 为 2.97），情绪分类准确率达到 68.41%（中性基线仅 14.07%）；用户研究在口型同步、表情自然度和视频质量上均优于对比方法。

**方法定位**：将情绪动态解耦为面部相关关键点上的可加位移，通过数据增强策略抑制语音内容和姿态干扰，在不修改音频驱动主干的前提下实现单样本情绪化说话人脸生成。

## 核心方法与创新机理

### 问题瓶颈与核心洞察

在单样本（one-shot）说话人脸生成中，现有方法通常仅利用音频驱动中性口型运动，缺乏对情绪表达的控制能力。EAMM 面临的核心瓶颈是：**如何在仅给定单张中性人脸图像、任意音频和任意情绪源视频的条件下，将情绪动态从源视频中提取并迁移到目标身份上，同时不破坏音频-口型同步和身份保真度**。

论文的核心洞察建立在一个关键观察之上：在基于无监督关键点的运动表示框架中，**面部区域仅由三个面部相关关键点（face-related keypoints）及其雅可比矩阵（Jacobians）控制，且这些运动表示在相对位移层面具有近似的线性可加性**。这一性质意味着，情绪动态可以被编码为面部关键点上的可加性位移，并直接叠加到音频驱动的中性运动表示上，从而在不干扰口型运动和身份的前提下实现情绪迁移。论文通过一个简单验证实验确认了这一假设：从情绪视频中提取的面部关键点位移可以直接叠加到任意人的中性运动表示上，并成功传递情绪动态。

### 框架总览

EAMM 的整体框架如图 2 所示，由两个核心模块构成：

1. **Audio2Facial-Dynamics (A2FD) 模块**：负责从单张中性人脸图像、音频和姿态序列生成音频驱动的中性说话人脸视频。该模块预测一组无监督关键点及其一阶雅可比矩阵作为运动表示，并通过流估计器和图像生成器产生最终帧。

2. **Implicit Emotion Displacement Learner (IEDL)**：从情绪源视频中提取仅含情绪的面部动态信息，将其编码为面部相关关键点和雅可比矩阵上的**线性可加位移**，然后叠加到 A2FD 模块生成的中性运动表示上，实现情绪化说话人脸生成。

### 模块一：Audio2Facial-Dynamics 模块

A2FD 模块继承自基于无监督关键点的运动建模范式，但针对音频驱动的说话人脸任务进行了适配。其输入包括：
- 单张源身份图像 $I_s$
- 音频片段
- 姿态序列（可选，用于控制头部姿态）

模块内部包含三个编码器（身份编码器、音频编码器、姿态编码器），将多模态输入编码后送入一个基于 LSTM 的解码器 $D$，逐帧预测运动表示。运动表示由 10 个无监督关键点 $\pmb{x}_t$ 及其雅可比矩阵 $\pmb{J}_t$ 组成，其中面部区域仅由三个面部相关关键点控制（如图 3 所示）。随后，流估计器 $F$ 基于预测的关键点和雅可比矩阵生成密集变形场，图像生成器 $G$ 根据变形场对源图像进行扭曲，产生输出帧 $\hat{I}_t$。

A2FD 模块的训练目标由两部分组成：

**关键点损失**（Key-point loss）：使音频预测的运动表示与预训练视觉模型提取的运动表示对齐，采用 L1 距离：

$$L_{kp} = \frac{1}{T} \sum_{t=1}^{T} (\| \pmb{x}_t^a - \pmb{x}_t^v \|_1 + \| \pmb{J}_t^a - \pmb{J}_t^v \|_1)$$

其中 $\pmb{x}_t^a, \pmb{J}_t^a$ 为音频驱动的预测值，$\pmb{x}_t^v, \pmb{J}_t^v$ 为从真实视频中提取的教师信号。

**感知损失**（Perceptual loss）：基于 VGG 特征的重构损失：

$$L_{\hat{P}^{er}} = \sum_{i=1}^{l} \| \mathrm{VGG}_i(\hat{I}_t) - \mathrm{VGG}_i(I_t) \|_1$$

总损失为两者的加权和：

$$L_{mo} = L_{kp} + \lambda_{per} L_{per}$$

### 模块二：Implicit Emotion Displacement Learner

IEDL 是 EAMM 的核心创新模块，负责从情绪源视频中提取情绪动态并编码为可加性位移。其设计基于前述的线性可加性假设：情绪模式可以被公式化为面部相关关键点和雅可比矩阵上的**互补位移** $(\Delta \pmb{x}', \Delta \pmb{J}')$。

**情绪位移提取**：给定情绪源视频，IEDL 首先将其送入与 A2FD 共享的运动预测网络，获得情绪视频的运动表示 $(\pmb{x}^{e\prime}, \pmb{J}^{e\prime})$。同时，利用 A2FD 模块对该视频的中性版本（或同一身份的中性帧）预测中性运动表示 $(\pmb{x}^{n\prime}, \bar{\pmb{J}}^{n\prime})$。情绪位移计算为两者的差值：

$$(\pmb{x}^{e\prime} - \pmb{x}^{n\prime}, \pmb{J}^{e\prime} - \bar{\pmb{J}}^{n\prime})$$

该差值被假设包含情绪信息，但也混杂了讲话内容、姿态和身份等无关因素。

**数据增强策略**：为抑制讲话内容和姿态对情绪位移的污染，IEDL 采用关键的数据增强策略——在训练时对情绪视频的嘴部和下颌区域进行遮挡（occlusion），迫使模型仅从面部其他区域（如眉毛、脸颊、眼部周围）提取情绪动态。这一策略对于准确传递情绪动态而不牺牲身份保真度至关重要。

**位移叠加与训练**：在推理时，IEDL 从情绪源视频中提取位移 $(\Delta \pmb{x}', \Delta \pmb{J}')$，将其线性叠加到 A2FD 模块为任意目标身份生成的中性运动表示上，得到情绪增强的运动表示 $(\pmb{x}^{ea}, \pmb{J}^{ea})$。训练 IEDL 时，使用以下关键点损失约束情绪增强后的运动表示与直接从情绪视频提取的运动表示一致：

$$L_{kp} = \frac{1}{T} \sum_{t=1}^{T} ( \Vert \pmb{x}_{t}^{ea} - \pmb{x}_{t}^{e} \Vert_{1} + \Vert \pmb{J}_{t}^{ea} - \pmb{J}_{t}^{e} \Vert_{1} )$$

其中 $\pmb{x}_{t}^{ea}, \pmb{J}_{t}^{ea}$ 为情绪增强后的预测值，$\pmb{x}_{t}^{e}, \pmb{J}_{t}^{e}$ 为从情绪视频直接提取的教师信号。

### 关键 Changed Slots

相较于现有基线方法，EAMM 在以下三个维度进行了根本性改变：

1. **情绪建模方式**：基线方法（如 ATVG、SDA、MakeItTalk、PC-AVS）要么不提供情绪控制，要么仅生成音频驱动的中性口型。EAMM 首次将情绪动态显式建模为面部关键点上的**线性可加位移**，实现了从任意情绪源视频到任意目标身份的情绪迁移。

2. **运动表示组成**：基线方法的运动表示仅包含 10 个关键点及其雅可比矩阵，由音频和姿态引导。EAMM 在此基础上增加了从情绪视频中学习的**三个面部相关关键点的位移项**，将运动表示扩展为中性分量与情绪分量的线性组合。

3. **输入数据模态**：基线方法通常仅需单张中性人脸图像、音频和姿态序列。EAMM 额外引入**情绪源视频**作为输入，使模型能够从外部情绪参考中提取并传递情绪动态。

### 训练与推理路径

**训练路径**：A2FD 模块和 IEDL 模块采用分阶段或联合训练策略。A2FD 模块首先在大型说话人脸数据集（如 LRW）上训练，学习音频到中性运动表示的映射。IEDL 模块随后在带有情绪标注的数据集（如 MEAD）上训练，学习从情绪视频中提取面部关键点位移。训练时，IEDL 通过遮挡嘴部和下颌的数据增强策略，强制模型关注面部其他区域的情绪线索。

**推理路径**：给定一张目标身份的中性人脸图像、一段任意音频、一个情绪源视频和可选的姿态序列，EAMM 首先通过 A2FD 模块生成音频驱动的中性运动表示；同时，IEDL 从情绪源视频中提取面部关键点位移；两者线性叠加后，通过流估计器和图像生成器产生最终的情绪化说话人脸视频帧。

### 因果机制总结

EAMM 的核心因果链为：**无监督关键点的面部区域局部性 → 面部运动表示的线性可加性 → 情绪位移的可提取性与可迁移性**。面部区域仅由三个关键点控制这一结构特性，使得情绪动态可以被局部化地编码为关键点位移，而不会泄漏到口型或身份相关的运动分量中。数据增强中的嘴部遮挡进一步切断了讲话内容对情绪位移的干扰路径，确保 IEDL 提取的是纯粹的情绪动态。这一设计使得 EAMM 能够在单样本设定下，首次实现从任意情绪源视频到任意目标身份的情绪化说话人脸生成。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2205_15278/figures/001_Figure_1.jpg]]
*Figure 1: Qualitative results of our Emotion-Aware Motion Model. Given a single portrait image, we can synthesize emotional talking faces, where mouth movements match the input audio and facial emotion dynamics follow the emotion source video. Natural video (top row) from LRW dataset [Chung and Zisserman 2016a] ©BBC. Emotional videos (at left corner) from MEAD dataset [Wang et al. 2020b] ©SenseTime and RAVDESS dataset [Livingstone and Russo 2018] ©SMART Lab (CC BY-NC-SA). Natural face (middle row) from CFD dataset [Ma et al. 2015] ©The University of Chicago. Natural face (bottom row) from CREMA-D dataset [Cao et al. 2014] (ODbL)*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2205_15278/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our Emotion-Aware Motion Model. Our framework includes two modules: Audio2Facial-Dynamics module for one-shot audio-driven talking head generation and Implicit Emotion Displacement Learner for extracting emotional patterns*

## 实验与关键发现

### 定量对比：口型同步与视频质量

EAMM在LRW和MEAD两个数据集上与多个基线方法进行了定量对比（Table 1）。需要特别说明的是，LRW数据集缺少情感标注，因此在该基准上的结果仅由Audio2Facial-Dynamics模块生成，不涉及情绪位移学习器——这意味着LRW上的对比本质上是验证中性口型同步能力。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2205_15278/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparisons with state-of-the-art methods. We show quantitative results on LRW [Chung and Zisserman 2016a] and MEAD [Wang et al. 2020b] datasets. The results of LRW are only generated by the Audio2Facial-Dynamics Module, as there is no emotion annotation in LRW. The metrics related to video quality and landmarks are calculated by comparing the generated results with the ground truth. Here M- denotes mouth and F- denotes face region. The signages “↑” and*

在MEAD数据集上，EAMM在所有指标上均取得最优。以M-LMD（嘴部关键点距离）为例，EAMM达到2.41，而最强基线PC-AVS（Zhou et al., CVPR 2021）为2.97，降低了0.56，表明嘴部运动与真实值的偏差显著更小。在LRW数据集上，EAMM的M-LMD为1.61，PC-AVS为1.67，降低了0.06。F-LMD（面部关键点距离）在MEAD上从PC-AVS的3.03降至2.55，降幅0.48，说明情绪位移学习器的引入并未破坏面部运动的保真度，反而有所改善。

在视频质量指标上，EAMM在MEAD上SSIM为0.66、PSNR为29.29，均优于PC-AVS（SSIM 0.63, PSNR 28.72）和MakeItTalk（Zhou et al., TOG 2020）等基线。SyncNet置信度在MEAD上达到2.26，同样领先。这些结果表明，线性叠加的情绪位移不仅没有干扰口型同步，反而因为整体框架的端到端训练而维持了生成质量。

### 用户研究与情绪分类准确率

由于客观指标难以直接度量情绪表达的真实性，论文通过用户研究（Table 2）从三个维度进行了主观评估：口型同步、表情自然度和视频质量（满分5分）。EAMM在三个维度上均获得最高分，分别为3.81、3.47和3.89。作为参考，真实数据（Ground Truth）在这三个维度上的得分分别为4.21、4.07和4.13，EAMM在视频质量维度与真实数据的差距最小（0.24），表情自然度差距最大（0.60），说明情绪表达的自然度仍是主要瓶颈。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2205_15278/figures/006_Table_2.jpg]]
*Table 2: User study results evaluated on three different aspects (the maximum score value is 5) and the emotion classification accuracy*

情绪分类准确率（Acc_emo）提供了更客观的情绪传递能力验证。在MEAD数据集上，EAMM达到68.41%，而中性基线A2FD仅为14.07%，提升高达54.34个百分点。这一巨大差距直接证明了隐式情绪位移学习器能够成功从源视频中提取并传递情绪信息。值得注意的是，PC-AVS和MakeItTalk等基线本身不具备情绪控制能力，其情绪分类准确率接近随机水平，进一步凸显了EAMM在情绪感知上的独特优势。

### 消融实验：情绪位移学习器的关键组件

Table 3的定量消融实验对比了五个变体与完整EAMM的性能，核心发现如下：

**数据增强策略至关重要。** 移除数据增强后，情绪准确率从68.41%大幅下降，同时M-LMD和F-LMD恶化，SSIM降低。数据增强的核心操作是对情绪源视频的嘴部和下颌区域进行遮挡，以阻止语音内容信息混入情绪位移。若不进行此操作，学习到的位移会包含与音频内容相关的口型变化，导致叠加后嘴部运动与输入音频不一致。

**隐式情绪位移学习器的三个组件均有效。** 消融实验分别移除了位移学习器中的关键设计（具体组件在论文Figure 5和Table 3中详细列出），每个组件的移除都导致情绪准确率下降和面部关键点偏差增大。这验证了从视频中提取纯情绪位移需要专门设计的网络结构，而非简单的特征相减。

**特征空间解耦的失败。** 论文明确指出，在特征空间进行情绪解耦的尝试效果不佳——面部形状不稳定且情绪不明显。这一消融结论支撑了方法设计的核心动机：情绪动态必须在关键点运动表示层面进行线性叠加，而非在深层特征空间操作。这从反面验证了“面部关键点位移线性可加性”这一核心假设的合理性。

### 失败模式与适用边界

论文揭示了以下局限：

1. **嘴部情绪动态不足。** 数据增强中对嘴部区域的遮挡虽然有效阻止了语音内容泄漏，但也导致嘴部相关的情绪动态（如惊讶时张嘴、厌恶时撇嘴）被部分抑制。这是当前设计的一个固有矛盾：需要在“阻止内容泄漏”和“保留嘴部情绪”之间权衡。

2. **跨个体情绪迁移缺乏个性化适配。** 情绪位移是从特定源视频中提取的，直接叠加到不同身份的目标人脸上时，可能产生不自然的表情。这是因为不同个体的面部肌肉结构、皮肤弹性等差异会导致相同的位移量产生不同的视觉效果。当前方法未对此进行建模。

3. **情绪源与音频内容不一致的风险。** EAMM未显式利用音频中的情绪线索，而是完全依赖外部情绪源视频。当情绪源视频的情感类别与音频中隐含的情绪语调不一致时（例如悲伤的音频配合愤怒的表情），生成结果会出现情感冲突。这一边界条件在实际应用中需要手动确保输入一致性。

4. **依赖情绪视频的可用性。** 方法需要完整的情绪源视频作为输入，无法从单张图像或文本描述中合成情绪动态。这限制了在缺乏合适情绪视频场景下的应用灵活性。

### 证据强度评估

- **高置信度证据**：M-LMD和F-LMD的定量改善（Table 1）、情绪分类准确率的巨大提升（Table 3）、用户研究的主观评分优势（Table 2），均有明确的数值支撑和统计意义。
- **中置信度证据**：消融实验中各组件的贡献方向明确，但缺少更细粒度的控制变量分析（如不同遮挡策略的量化对比）。
- **需人工验证的点**：论文未报告跨身份情绪迁移的一致性指标（如不同源-目标配对下的情绪准确率方差），个性化适配的失败程度缺乏量化表征。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2205_15278/figures/008_Table_3.jpg]]
*Table 3: Quantitative ablation study. We provide quantitative results of five variants and our EAMM on emotion accuracy, M-LMD, F-LMD and SSIM*

## 定位与知识库关联

EAMM 的核心定位是在**单样本音频驱动说话人脸生成**这一任务上，首次将**情绪动态**作为一个显式可控的维度引入，且不依赖情绪类别标签。相对于已有方法，它改变的关键 slot 是**情绪建模方式**：此前的方法（如 **MakeItTalk** (Zhou et al., TOG 2020)、**Wav2Lip** (Prajwal et al., ACMMM 2020)、**PC-AVS** (Zhou et al., CVPR 2021)）要么完全不具备情绪控制能力，仅生成与音频同步的中性口型；要么需要情绪类别标签来驱动表情生成。EAMM 则通过**从任意情绪源视频中提取面部关键点位移，并将其作为线性可加项叠加到音频驱动的中性运动表示上**，实现了无需情绪标签的任意情绪迁移。

在知识库挂载层面，EAMM 可挂载到以下节点：

1. **无监督关键点运动表示**：EAMM 的 Audio2Facial-Dynamics 模块直接继承自 FOMM (Siarohin et al., NeurIPS 2019) 和 **PC-AVS** (Zhou et al., CVPR 2021) 的无监督关键点与一阶雅可比矩阵运动表示范式。它保留了 10 个无监督关键点（其中 3 个控制面部区域，7 个控制嘴部和下颌）及其雅可比矩阵作为运动表征，通过 LSTM 解码器从音频和姿态特征中序列预测。这一基础架构是 PC-AVS 的直接延续，但 EAMM 在此基础上新增了一个独立的情绪位移学习器，而非修改原有模块。

2. **线性可加的情绪迁移假设**：EAMM 的核心创新在于发现并利用了一个关键性质——面部区域的动态运动仅由三个面部相关关键点控制，且这些关键点及其雅可比矩阵的相对位移在情绪表达上是**近似线性可加的**。这一发现使得情绪迁移可以被简化为一个位移叠加操作，无需在隐空间中进行复杂的特征解耦。这为后续的情绪化说话人脸生成提供了一个简洁而有效的范式：情绪 = 中性运动 + 位移偏差。

3. **隐式情绪位移学习器**：该模块的设计动机来源于对情绪偏差的直接计算尝试——从情绪视频中提取的运动表示减去中性运动表示，理论上应包含情绪信息。但直接使用此偏差会导致面部边界伪影和嘴部内容泄露。为此，EAMM 设计了一个可学习的位移提取器，并配合数据增强策略（遮挡嘴部和下颌区域、随机时间偏移）来抑制语音内容和姿态信息的干扰，仅保留纯粹的情绪动态。这一设计思路——在运动空间而非特征空间进行情绪操作——是经过实验验证的关键选择：论文明确指出“情绪无法在特征空间很好地解耦，仅在特征层面操作会导致面部形状不稳定且情绪不明显”。

**适用边界与局限**：

- EAMM 的情绪迁移是**全局性**的，它从源视频中提取的情绪模式会不加区分地应用到目标人物上，缺乏对个性化情绪表达风格的适配。这意味着同一个“愤怒”源视频应用到不同身份上会产生相同的面部动态模式，可能在某些身份上显得不自然。
- 嘴部情绪动态（如撇嘴、咬唇等）由于数据增强中的遮挡策略而被部分抑制，导致嘴部情绪表达不够明显。这是当前设计的一个内在权衡：为了阻断语音内容泄露而牺牲了部分嘴部情绪表现力。
- 该方法**未利用音频中的情绪线索**，完全依赖外部情绪源视频来驱动情绪。当音频本身携带情绪信息（如愤怒的语调）而情绪源视频提供的是中性或不同情绪时，会产生视听不协调。这一限制指向了一个自然的改进方向：融合音频情绪识别与视觉情绪迁移。
- 在 LRW 数据集上的评估仅使用了 Audio2Facial-Dynamics 模块（因为 LRW 缺乏情绪标注），因此情绪生成能力在该基准上未得到验证。MEAD 数据集上的完整评估才是该方法情绪能力的有效证据。

**后续启发与开放问题**：

EAMM 建立的“中性运动 + 情绪位移”范式为后续研究提供了几个明确的改进方向：一是如何使情绪位移具备身份感知能力，实现个性化的情绪迁移；二是如何利用音频中的情绪线索来辅助或替代外部情绪源视频，避免视听不协调；三是如何在保持语音内容抑制的同时恢复嘴部的情绪动态表现力。此外，该方法在无情绪类别标签条件下处理任意情绪源视频的能力，使其天然适用于开放域的情绪化说话人脸生成场景，这是相对于需要预定义情绪类别的方法（如基于标签的条件生成）的一个显著优势。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/EAMM_One_Shot_Emotional_Talking_Face_via_Audio_based_Emotion_Aware_Motion_Model.pdf]]