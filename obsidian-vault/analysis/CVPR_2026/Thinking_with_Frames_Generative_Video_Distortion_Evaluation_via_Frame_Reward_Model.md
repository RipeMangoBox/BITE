---
title: "Thinking with Frames: Generative Video Distortion Evaluation via Frame Reward Model"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Thinking_with_Frames_Generative_Video_Distortion_Evaluation_via_Frame_Reward_Model.pdf
project_link: null
code_link: null
aliases:
- TFGVDEFRM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过构建详细的失真分类体系，并结合帧级思维链推理和两阶段强化学习（GRPO）训练，使模型能够精确识别和评估结构失真。
primary_logic: 针对生成视频的结构失真进行帧级评估，通过定制化的分类体系和强化学习训练，比传统视频或图像评估器更准确地识别失真并提供可解释的评分。
claims:
- REACT在人类偏好对齐任务上显著优于现有视频评估器
- REACT在失真识别任务中取得最高F1分数（扭曲帧0.845, 正常帧0.671）
- 消融实验表明两阶段训练、配对奖励和动态采样对性能至关重要
- REACT-Video 上 偏好对齐准确率 (Acc w/ Tie) = 0.610
---

# Thinking with Frames: Generative Video Distortion Evaluation via Frame Reward Model

> [!tip] 核心洞察
> 针对生成视频的结构失真进行帧级评估，通过定制化的分类体系和强化学习训练，比传统视频或图像评估器更准确地识别失真并提供可解释的评分。

| 字段      | 内容                                                                                                                                                                              |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | 以帧思考：面向生成视频结构失真评估的帧级奖励模型                                                                                                                                                        |
| 英文题名    | Thinking with Frames: Generative Video Distortion Evaluation via Frame Reward Model                                                                                             |
| 会议/期刊   | CVPR 2026                                                                                                                                                                       |
| Links   | [paper](https://arxiv.org/abs/2601.04033)                                                                                                    |
| Topic   | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method  | REACT                                                                                                                                                                           |
| Dataset | REACT-Video, REACT-Frame, VBench                                                                                                                                                |

> [!tip] 效果简介
> - REACT-Video 上，偏好对齐准确率 (Acc w/ Tie) 0.610 vs 0.416 (UnifiedReward) (+0.194)；偏好对齐准确率 (Acc w/o Tie) 0.813 vs 0.701 (UnifiedReward) (+0.112)。
> - REACT-Frame 上，失真帧F1分数 0.845 vs 0.765 (MagicAssessor) (+0.080)；正常帧F1分数 0.671 vs 0.652 (MagicAssessor) (+0.019)。
> - VBench (Flow-DPO) 上，Imaging Quality 0.691 vs 0.690 (UnifiedReward) (+0.001)。

## 概述

### 问题与核心瓶颈

当前生成视频（T2V）质量评估面临一个关键矛盾：主流视频奖励模型和图像质量评估器倾向于基于美学质量和时序一致性给出高分，却无法有效捕获生成视频中普遍存在的**结构失真**——如肢体变形、物体穿透、异常融合等。这导致高评分视频仍可能包含严重的视觉缺陷，评估结果与人类感知脱节。其根本原因在于，现有评估器缺乏对帧级结构完整性的细粒度推理能力，无法区分“画面精美但结构错误”与“真正高质量”的视频。

### 核心思想

针对上述瓶颈，本文提出 **REACT**（**R**eward model for **E**valuating structural distortions via fr**A**me reasoning with **C**hain-of-**T**hought），一种面向生成视频结构失真评估的帧级奖励模型。其核心洞察是：**将评估粒度从视频级下潜至帧级，通过构建专门的失真分类体系与思维链（CoT）推理，使模型能够精确识别和量化结构缺陷**。REACT 为每一帧分配逐点分数（point-wise score）和归属标签（attribution label），从而提供可解释的、与人类偏好对齐的评估结果。

### 方法定位

REACT 基于 Qwen2.5-VL-7B 多模态大语言模型构建，通过三个关键设计实现帧级结构失真评估：

1. **细粒度失真分类体系**：将生成视频中的结构失真系统归纳为“异常物体外观”与“异常物体交互”两大类别，覆盖 8 种具体失真类型，为模型训练提供清晰的标注框架。
2. **两阶段训练范式**：首先在合成的 CoT 推理数据上进行监督微调（SFT），并在第二轮 SFT 中引入 masked loss 以增强领域知识注入；随后采用分组相对策略优化（GRPO）进行强化学习，结合格式奖励、归属准确性奖励和配对偏好奖励，使模型输出与人类偏好对齐。
3. **动态帧采样机制**：推理时根据第一阶段评分分布自适应选择第二阶段采样帧，在固定帧数约束下聚焦于最可能包含失真的帧，提升评估效率与准确性。

### 主要结果概览

在自建的 REACT-Bench 基准上，REACT 相较于现有方法取得了显著提升：

- **人类偏好对齐**：在 REACT-Video 上，偏好对齐准确率（Acc w/ Tie）达到 **0.610**，较最强基线 UnifiedReward（0.416）提升 **+0.194**；去除平局后的准确率（Acc w/o Tie）达到 **0.813**（UnifiedReward 为 0.701）。
- **失真识别**：在 REACT-Frame 上，失真帧 F1 分数达到 **0.845**，正常帧 F1 分数达到 **0.671**，均优于 MagicAssessor 等专用图像评估器及 GPT-4o、GPT-o3 等通用多模态模型。
- **消融验证**：两阶段训练、配对偏好奖励和动态采样机制均对最终性能有决定性贡献——移除其中任一组件均导致准确率大幅下降（如仅用 RL 时 Acc w/ Tie 降至 0.387）。

### 局限与边界

REACT 的帧级分析范式也存在固有局限：它可能无法捕捉需要跨帧时序上下文的瞬时失真（如闪烁、物体瞬移）；在通用视频评估基准（如 VideoGen-RewardBench）上，其综合视觉质量评估能力略低于视频级评估器。此外，动态采样依赖预设阈值，训练数据集中于特定 T2V 模型生成的视频，分布偏移可能影响泛化能力。这些边界为未来将帧级推理扩展至时空上下文、融合视频级评估能力等方向留下了开放问题。

## 背景与动机

### 生成视频质量评估的现状与盲区

近年来，以 **Sora**（OpenAI, 2024）、**Hailuo**（MiniMax, 2024）等为代表的文本到视频（T2V）生成模型取得了长足进步，但生成视频中仍普遍存在一类被现有评估体系系统性忽视的缺陷——**结构失真**（structural distortions）。这类失真表现为肢体变形、物体穿透、异常融合等违反物理直觉的视觉错误，严重损害了生成内容的可用性和真实感。

当前主流的视频质量评估范式存在一个关键盲区：无论是基于美学质量、运动平滑度还是文本对齐度的评估器，都倾向于对包含明显结构缺陷的视频仍给出高分。如 **Figure 1** 所示，现有视频级评估器（如 **VideoScore2**、**UnifiedReward**、**VideoReward**）主要关注整体美学和时序一致性，却无法有效捕获帧级别的结构异常。与此同时，专为生成图像伪影设计的图像评估器（如 **Q-Insight**、**VisualQuality-R1**）虽然在静态图像伪影识别上表现优异，但面对生成视频帧中的结构失真时识别能力明显不足。

### 现有方法的根本瓶颈

这一困境的根源在于**评估粒度与失真类型之间的错配**。结构失真本质上是帧级的、空间性的缺陷，需要模型对单帧内的物体形态、空间关系和交互逻辑进行精确推理。然而：

- **视频级评估器**将视频作为整体进行评分，其优化目标（美学、运动质量）与结构完整性的相关性较弱，导致评分信号对结构失真不敏感。
- **图像评估器**虽然工作在帧级别，但其训练数据主要覆盖传统图像伪影（模糊、噪声、压缩痕迹），缺乏对生成视频特有的结构异常（如多指、肢体穿透、物体融合）的针对性建模。
- **通用多模态大模型**（如 **Qwen2.5-VL**、**Gemini-2.5-Flash/Pro**、**GPT-4o**）具备一定的视觉推理能力，但未经过针对结构失真的专门训练，在细粒度失真识别和可解释评分方面表现有限。

这一瓶颈导致了实际应用中的严重问题：高评分的生成视频仍可能包含令人无法接受的肢体变形或物体穿透，使得现有奖励模型难以作为可靠的生成质量守门人或强化学习中的奖励信号。

### 本文的核心动机与解决思路

针对上述缺口，本文提出 **REACT**（**RE**w**A**rd Model for Stru**C**tural Dis**T**ortion Evaluation），一个专为生成视频结构失真评估设计的**帧级奖励模型**。其核心动机在于：

1. **建立精细化的失真分类体系**：将生成视频中的结构失真系统性地划分为**异常物体外观**（abnormal object appearance）和**异常物体交互**（abnormal object interaction）两大类别，并进一步细分为8种具体失真类型（如肢体变形、多指、穿透、融合等），为模型提供明确的评估目标。

2. **实现帧级可解释评估**：不同于传统评估器输出单一视频级分数，REACT 通过对视频帧进行逐帧推理，输出**逐点分数**（point-wise scores）和**失真归属标签**（attribution labels），使评估结果具备可解释性——不仅告知用户视频存在缺陷，还能定位到具体帧和具体失真类型。

3. **对齐人类偏好**：通过构建包含超过15,000对偏好标注（约30,000帧）的大规模数据集，并结合两阶段训练（监督微调 + 分组相对策略优化 GRPO），使模型的评分分布与人类对结构完整性的偏好判断高度一致。

简言之，REACT 试图填补视频评估与图像评估之间的空白地带——以帧为基本评估单元，以结构失真为专门评估对象，以可解释推理为输出形式，从而为生成视频的质量把关提供更精准、更可信的自动化工具。

## 核心创新

### 问题重新定义：从“视频好不好看”到“结构对不对”

现有视频评估器（如 **VideoScore2**、**UnifiedReward**）的设计目标在于评判视频的美学质量与运动连贯性，其评分机制天然倾向于奖励画面美观、时序平滑的视频，即使这些视频中存在严重的结构失真（如肢体扭曲、物体穿透、多指等）。这导致一个关键瓶颈：高评分视频仍可能包含人类观察者无法接受的缺陷，使得现有评估器无法可靠地服务于生成视频的质量控制与偏好对齐。

REACT 的核心创新在于将评估目标从“整体视觉质量”重新聚焦到“结构正确性”这一维度。论文构建了一个精细的结构失真分类体系（Figure 3），将生成视频中的结构缺陷归纳为两大方面：**异常物体外观**（肢体变形、部件冗余/缺失、纹理异常等）和**异常物体交互**（穿透、融合、错位等），共覆盖 8 种具体失真类型。这一分类体系为后续的帧级评估提供了明确的判别依据。

### 粒度切换：帧级点分与归属标签

传统视频评估器输出单一的视频级评分，无法定位失真发生的具体帧，更无法解释评分的依据。REACT 将评估粒度从视频级下推到帧级，对每个采样帧输出两类信息：

- **点分（point-wise score）**：一个连续值，反映该帧的结构失真严重程度，分数越低表示失真越严重。
- **归属标签（attribution label）**：一组从失真分类体系中选取的标签，精确标注该帧存在的失真类型。

这种帧级、可归因的输出形式，使 REACT 不仅能判断“哪个视频更好”，还能回答“哪一帧出了问题、出了什么问题”，从而提供可解释的评估结果。这一设计直接回应了现有评估器“高分低质”的失效模式。

### 训练策略创新：两阶段训练与配对偏好奖励

REACT 的训练流程包含三个关键的设计选择，构成其性能提升的因果链条：

**（1）SFT 阶段的 masked loss。** 在监督微调阶段，REACT 对 Qwen2.5-VL-7B 进行两轮微调。第二轮微调引入 masked loss，仅对模型输出中的分数和归属标签部分计算损失，而对思维链（CoT）推理文本部分进行掩码。这一设计的目的在于防止模型过拟合到 CoT 文本的表面模式，强制其学习从视觉特征到评估结论的映射，而非依赖语言捷径。消融实验（Table 4）证实，移除 masked loss 会导致失真识别性能下降。

**（2）GRPO 阶段的配对偏好奖励。** 在强化学习阶段，REACT 采用分组相对策略优化（GRPO），并引入基于 BTT 损失的配对偏好奖励 $R_{\mathrm{pref}}$。该奖励的核心机制是：对于训练数据中的每个视频对（一帧为偏好帧、一帧为劣势帧），模型的两个 rollout 分别对两帧打分，然后根据真实偏好标签计算 rollout 评分与人类偏好一致的对数似然作为奖励。这使得模型在 RL 过程中直接学习将点分排序与人类偏好对齐，而非仅优化独立的帧级评分准确性。消融实验（Table 3）表明，移除偏好奖励会导致偏好对齐准确率从 0.610 骤降至 0.352，揭示了该组件的关键作用。

**（3）两阶段训练的必要性。** 消融实验（Table 3）进一步表明，跳过 SFT 直接进行 RL（即仅 RL）会导致偏好对齐准确率降至 0.387，远低于完整两阶段训练的 0.610。这说明 SFT 阶段提供的领域知识注入是 RL 阶段有效优化的前提——RL 负责对齐偏好，但需要 SFT 先建立对结构失真的基本识别能力。

### 推理机制创新：动态两阶段采样

在推理时，REACT 不采用固定帧率采样，而是设计了一个动态两阶段采样机制。第一阶段以固定间隔采样若干帧并评分，根据得分分布识别出可能存在失真的帧（分数显著低于均值）。第二阶段则根据第一阶段的得分分布自适应地选择额外帧，提高对疑似失真帧的采样概率。最终视频得分由两阶段采样帧的分数取平均得到。

这一机制的核心价值在于：在固定采样帧数（计算预算）的约束下，将采样资源向可能存在问题的帧倾斜，从而更准确地捕捉视频中的结构失真。消融实验（Table 3）显示，禁用动态采样（改为固定采样）会使偏好对齐准确率从 0.610 降至 0.519，证实了其有效性。

### 高效 CoT 合成流水线

为获取训练所需的帧级思维链数据，论文设计了一个高效的 CoT 合成流水线。人工标注者仅需在失真帧上绘制边界框并标注失真类别，无需撰写推理文本。随后，使用 Gemini 2.5 Pro 基于边界框位置和失真标签自动生成模拟的推理过程，并为每个失真分配伪分数。这一设计将人工标注成本压缩到最小（仅需画框和选标签），同时利用大模型的语言能力生成高质量的训练信号。论文报告标注的边界框准确率超过 95%，归属标签准确率超过 90%，最终产出约 6K 条高质量 CoT 实例用于训练。

### 与 baseline 的核心差异总结

| 维度 | 现有评估器 | REACT |
|------|-----------|-------|
| 评估目标 | 整体美学/运动质量 | 结构正确性（8 类失真） |
| 输出粒度 | 视频级单分数 | 帧级点分 + 归属标签 |
| 训练策略 | 标准 SFT 或偏好优化 | 两阶段：masked SFT → GRPO + 配对偏好奖励 |
| 推理采样 | 固定帧率 | 动态两阶段自适应采样 |
| 可解释性 | 黑盒评分 | 帧级 CoT 推理 + 失真归属 |

这些创新共同构成了 REACT 在结构失真评估任务上显著超越现有视频评估器和图像评估器的能力基础。

## 整体框架

REACT 的整体框架围绕“帧级结构失真评估”这一核心目标，构建了从数据构造、模型训练到推理采样的完整流水线，如 Figure 2 所示。框架由三个关键模块串联而成：

![[assets/figures/papers/paper_list_l2284_https_arxiv_org_abs_2601_04033/figures/002_Figure_2.jpg]]
*Figure 2: Overview of REACT: Frame-Level Reward Model for Structural Distortion Evaluation. (a) We first construct a large-scale annotated dataset, including human preference and attribution labels, based on our proposed detailed taxonomy of structural distortions. Furthermore, we synthesize CoT data through an efficient pipeline that leverages human-annotated issue bounding boxes and label-aware sampled frame-level scores. (b) We then train REACT based on Qwen2.5-VL-7B using a two-stage training framework. During SFT stage, a masked loss is applied to improve domain knowledge injection. During GRPO stage, pair-wise rewards are introduced to align the output point-wise scores of REACT with human pref...*

1. **大规模标注数据集与思维链合成**
2. **两阶段奖励模型训练（SFT + GRPO）**
3. **动态采样推理机制**

### 数据构造与思维链合成

框架的第一步是构建一个专门针对生成视频结构失真的标注数据集。作者首先提出了一套详细的失真分类体系，将结构失真归纳为**异常物体外观**和**异常物体交互**两大主类别，并进一步细分为 8 种具体失真类型（Figure 3）。基于该分类体系，收集真实视频生成提示，使用多个文本到视频（T2V）模型生成视频，并对帧对进行人类偏好标注和失真类别标注。最终构建了超过 **15k 对**（约 30k 帧）的训练数据。

为降低标注成本并保证质量，标注者只需在失真区域绘制边界框，标注准确率可达 95% 以上，归因标签准确率超过 90%。随后，利用 **Gemini 2.5 Pro** 基于这些边界框自动生成思维链（Chain-of-Thought, CoT）推理数据，模拟从观察到归因再到评分的完整推理过程，并为每帧分配伪分数。该流水线最终产出约 **6K 高质量 CoT 实例**用于训练。

### 两阶段奖励模型训练

REACT 以 **Qwen2.5-VL-7B** 作为基座模型，采用监督微调（SFT）与强化学习（GRPO）两阶段训练策略：

- **监督微调阶段**：在合成的 CoT 数据上进行两轮微调。第一轮使用标准损失函数注入领域知识；第二轮引入 **masked loss**，仅对推理相关的关键 token 计算损失，防止模型过拟合到 CoT 的固定表达模式。
- **强化学习阶段**：采用分组相对策略优化（Group Relative Policy Optimization, GRPO）。对于每个输入问题 $q$，从旧策略 $\pi_{\theta_{\text{old}}}$ 中采样一组 $G$ 个 rollout $\{o_i\}_{i=1}^G$，通过组内奖励归一化计算每个响应的优势值：

$$A_i = \frac{R(o_i) - \text{mean}(\{R(o_1), R(o_2), \dots, R(o_G)\})}{\text{std}(\{R(o_1), R(o_2), \dots, R(o_G)\})}$$

GRPO 的策略更新目标使用截断的重要性采样比率和 KL 惩罚：

$$\mathcal{I}_{\mathrm{GRPO}}(\boldsymbol{\theta}) = \mathbb{E}_{\boldsymbol{q} \sim \mathcal{Q}, \{\boldsymbol{o}_{i}\}_{i=1}^{G} \sim \pi_{\boldsymbol{\theta}_{\mathrm{old}}}(\boldsymbol{o}|\boldsymbol{q})} \left\{ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|\boldsymbol{o}_{i}|} \sum_{t=1}^{|\boldsymbol{o}_{i}|} -\beta \mathbb{D}_{KL}(\pi_{\theta} || \pi_{\mathrm{ref}}) + \min\left[ \frac{\pi_{\theta}(o_{i,t} \mid q, o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t} \mid q, o_{i,<t})} A_{i,t}, \mathrm{clip}\left(\frac{\pi_{\theta}(o_{i,t} \mid q, o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t} \mid q, o_{i,<t})}, 1-\epsilon, 1+\epsilon\right) A_{i,t} \right] \right\}$$

每个 rollout 的最终奖励 $R(\boldsymbol{\sigma}_i^j)$ 由三项加权组合而成：

$$R(\boldsymbol{\sigma}_i^j) = \lambda_1 R_{\mathrm{fmt}}(\boldsymbol{\sigma}_i^j) + \lambda_2 R_{\mathrm{attr}}(\boldsymbol{\sigma}_i^j) + \lambda_3 R_{\mathrm{pref}}(\boldsymbol{\sigma}_i^A, \boldsymbol{\sigma}_i^B)$$

其中：
- **格式奖励** $R_{\mathrm{fmt}}$：约束输出遵循预定义的结构化格式。
- **归因准确度奖励** $R_{\mathrm{attr}}$：根据正确、多余和缺失的归属标签计算，$R_{\mathrm{attr}} = 0.6 \cdot a_{\mathrm{right}} - 0.2 \cdot (a_{\mathrm{wrong}} + a_{\mathrm{missing}})$。
- **偏好奖励** $R_{\mathrm{pref}}$：基于 BTT 损失构建配对奖励。对于帧对 A 和 B，分别计算 A 优于 B、B 优于 A 以及平局的概率（Eq. 4-6），再根据真实偏好标签取对数似然作为奖励（Eq. 7）。该机制将帧级评分与人类偏好对齐，是模型能够区分“高美学评分但存在结构缺陷”的关键设计。

### 动态采样推理机制

推理时，REACT 采用两阶段动态采样策略，在固定帧数约束下提高失真帧的命中概率：

1. **第一阶段**：均匀采样 $N$ 帧，模型对每帧输出点分数和归因标签。
2. **第二阶段**：根据第一阶段得分分布，自适应选择得分较低的帧进行补充采样，重点关注可能包含结构失真的帧。

最终视频得分由两阶段采样帧的分数取平均得到。该机制使模型能够在有限的计算预算内灵活聚焦于问题帧，避免均匀采样遗漏关键失真。消融实验（Table 3）表明，禁用动态采样后偏好对齐准确率从 0.610 降至 0.519，验证了其必要性。

### 模块间数据流

整体数据流可概括为：**标注边界框 → Gemini 2.5 Pro 合成 CoT 数据（含伪分数与归因标签）→ SFT 注入领域知识（第二轮使用 masked loss）→ GRPO 对齐人类偏好（格式 + 归因 + 配对偏好奖励）→ 动态采样推理输出帧级分数与失真归因**。这一设计使得 REACT 能够输出可解释的帧级评估结果，而非仅给出单一的视频级评分。

### 补充图表

![[assets/figures/papers/paper_list_l2284_https_arxiv_org_abs_2601_04033/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of REACT with SOTA Video and Image Evaluators. (a) While existing evaluators tend to assign high scores based on aesthetics and temporal consistency, even in the presence of structural defects, our REACT model outperforms them by accurately identifying structural distortions in generative videos and providing more reliable scores (b) While image evaluators excel in recognizing image artifacts, they struggle to detect distortions in generative video frames. In contrast, REACT demonstrates superior performance in recognizing and evaluating structural distortions in video frames*

## 核心模块与公式推导

REACT 的核心技术路线围绕三个关键模块展开：面向结构失真的精细化数据构建、两阶段奖励模型训练（SFT + GRPO），以及推理时的动态帧采样机制。以下逐一剖析各模块的设计逻辑与关键公式。

### 数据构建与思维链合成

REACT 的训练数据构建遵循“人工标注边界框 → 自动合成思维链”的高效流水线。首先，研究者建立了一个结构失真分类体系，将生成视频中的结构缺陷归为两大类：**异常物体外观**（如肢体变形、多余肢体）和**异常物体交互**（如穿透、融合）。标注者只需在失真区域绘制边界框，无需撰写详细的自然语言描述，大幅降低标注成本——论文报告边界框准确率超过 95%，归属标签准确率超过 90%。

随后，利用 Gemini 2.5 Pro 基于标注边界框模拟推理过程，自动生成包含定位描述和失真归因的思维链（CoT）文本，并为每个帧分配伪分数。该流水线最终产出约 6K 高质量 CoT 实例，用于后续的监督微调。整个数据集包含超过 15K 帧对（约 30K 帧），覆盖多种 T2V 模型生成的视频。

### 监督微调与掩码损失

REACT 以 **Qwen2.5-VL-7B** 为基座模型，在 CoT 数据上进行监督微调。微调分两轮执行：第一轮使用标准交叉熵损失；第二轮引入**掩码损失（masked loss）**，仅对模型生成的推理文本部分计算损失，而对输入的视频帧 token 进行掩码处理。这一设计旨在防止模型过拟合到视觉输入的表面统计特征，迫使其聚焦于推理链本身的语义正确性。消融实验表明，两阶段 SFT 配合 masked loss 在失真识别任务中取得了最佳 F1 分数。

### 强化学习与多奖励设计

在 SFT 之后，REACT 采用**分组相对策略优化（GRPO）** 进行强化学习训练。GRPO 的核心思想是对同一提示采样一组响应，通过组内奖励归一化计算优势值，从而消除对独立价值网络的依赖。

对于第 $i$ 个响应 $o_i$，其优势值 $A_i$ 定义为组内奖励的标准化：

$$A_{i} = \frac{R(o_{i}) - \text{mean}(\{R(o_{1}), R(o_{2}), \dots, R(o_{G})\})}{\text{std}(\{R(o_{1}), R(o_{2}), \dots, R(o_{G})\})}$$

策略更新目标 $\mathcal{I}_{\mathrm{GRPO}}(\boldsymbol{\theta})$ 采用截断的重要采样比率和 KL 散度惩罚：

$$\mathcal{I}_{\mathrm{GRPO}}(\boldsymbol{\theta}) = \mathbb{E}_{\boldsymbol{q} \sim \mathcal{Q}, \{\boldsymbol{o}_{i}\}_{i=1}^{G} \sim \pi_{\boldsymbol{\theta}_{\mathrm{old}}}(\boldsymbol{o}|\boldsymbol{q})} \left\{ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|\boldsymbol{o}_{i}|} \sum_{t=1}^{|\boldsymbol{o}_{i}|} -\beta \mathbb{D}_{KL}(\pi_{\theta} || \pi_{\mathrm{ref}}) + \min\left[ \frac{\pi_{\theta}(o_{i,t} \mid q, o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t} \mid q, o_{i,<t})} A_{i,t}, \text{clip}\left(\frac{\pi_{\theta}(o_{i,t} \mid q, o_{i,<t})}{\pi_{\theta_{\mathrm{old}}}(o_{i,t} \mid q, o_{i,<t})}, 1-\epsilon, 1+\epsilon\right) A_{i,t} \right] \right\}$$

其中 $\pi_{\theta}$ 和 $\pi_{\theta_{\mathrm{old}}}$ 分别为当前策略和旧策略，$\beta$ 控制 KL 惩罚强度，$\epsilon$ 为截断阈值。

REACT 的奖励函数由三个分量加权组成：

**归属准确度奖励** $R_{\mathrm{attr}}$：根据模型输出的归属标签与真实标签的匹配情况计分。令 $a_{\mathrm{right}}$、$a_{\mathrm{wrong}}$、$a_{\mathrm{missing}}$ 分别表示正确、多余和缺失的标签数量：

$$R_{\mathrm{attr}}({\pmb\sigma}_{i}^{j}) = 0.6 \cdot a_{\mathrm{right}} - 0.2 \cdot (a_{\mathrm{wrong}} + a_{\mathrm{missing}})$$

该设计对错误和遗漏施加对称惩罚，鼓励模型精确输出失真类别归属。

**偏好奖励** $R_{\mathrm{pref}}$：基于 Bradley-Terry-Thompson（BTT）损失构建成对偏好奖励。对于帧对 $(f^A, f^B)$，模型为两个 rollout 分别输出点分数 $s_i^A$ 和 $s_i^B$，定义偏好概率：

$$P(\pmb{o}_{i}^{A} \succ \pmb{o}_{i}^{B} | c) = \frac{e^{s_{i}^{A}}}{\theta e^{s_{i}^{A}} + e^{s_{i}^{B}}}$$

$$P(\pmb{o}_{i}^{A} \prec \pmb{o}_{i}^{B} | c) = \frac{e^{s_{i}^{B}}}{\theta e^{s_{i}^{A}} + e^{s_{i}^{B}}}$$

$$P(\pmb{o}_{i}^{A} = \pmb{o}_{i}^{B} | c) = \frac{(\theta^{2} - 1) e^{s_{i}^{A}} e^{s_{i}^{B}}}{(e^{s_{i}^{A}} + \theta e^{s_{i}^{B}})(\theta e^{s_{i}^{A}} + e^{s_{i}^{B}})}$$

其中 $\theta$ 控制平局概率的尺度。偏好奖励取真实偏好标签下的对数似然：

$$R_{\mathrm{pref}}(\pmb{o}_{i}^{A}, \pmb{o}_{i}^{B}) = \mathbb{I}(f^{A} \succ f^{B}) \log P(\pmb{o}_{i}^{A} \succ \pmb{o}_{i}^{B}|c) + \mathbb{I}(f^{A} \prec f^{B}) \log P(\pmb{o}_{i}^{A} \prec \pmb{o}_{i}^{B}|c) + \mathbb{I}(f^{A} = f^{B}) \log P(\pmb{o}_{i}^{A} = \pmb{o}_{i}^{B}|c)$$

**最终 rollout 奖励** 综合格式奖励 $R_{\mathrm{fmt}}$、归属准确度奖励和偏好奖励：

$$R(\pmb{\sigma}_{i}^{j}) = \lambda_{1} R_{\mathrm{fmt}}(\pmb{\sigma}_{i}^{j}) + \lambda_{2} R_{\mathrm{attr}}(\pmb{\sigma}_{i}^{j}) + \lambda_{3} R_{\mathrm{pref}}(\pmb{\sigma}_{i}^{A}, \pmb{\sigma}_{i}^{B})$$

消融实验表明，移除偏好奖励导致偏好对齐准确率（Acc w/ Tie）从 0.610 骤降至 0.352，验证了成对偏好信号对点分数校准的关键作用。

### 动态帧采样机制

推理时，REACT 采用两阶段动态采样策略以在固定帧数约束下最大化失真帧的捕获概率。第一阶段对视频均匀采样 $N$ 帧并评分；根据第一阶段得分分布，第二阶段自适应选择得分最低（即最可能包含失真）的 $M$ 帧进行补充分析。最终视频分数由两阶段采样帧的得分取平均得到。消融实验中，禁用动态采样使偏好对齐准确率降至 0.519，证实了该机制对性能的显著贡献。

### 补充图表

![[assets/figures/papers/paper_list_l2284_https_arxiv_org_abs_2601_04033/figures/007_Figure_3.jpg]]
*Figure 3: Detailed Explanation of Our Proposed Taxonomy of Structural Distortions in Generative Videos. Representative examples for each distortion category are also provided*

## 实验与分析

### 实验设置与基准构建

为系统评估REACT的性能，作者构建了**REACT-Bench**基准，包含两个子集：**REACT-Video**（视频对偏好评估）和**REACT-Frame**（帧级失真识别标注）。REACT采用**Qwen2.5-VL-7B**作为基座模型。对比基线覆盖三类方法：视频级评估器（**VideoScore2**、**UnifiedReward**、**VideoReward**）、图像评估器（**Q-Insight**、**VisualQuality-R1**、**MagicAssessor**）以及通用多模态大模型（**Qwen2.5-VL-7B/32B**、**Gemini-2.5-Flash/Pro**、**GPT-4o**、**GPT-o3**）。为保障对比公平性，对基于MLLM的图像评估器（Q-Insight和VisualQuality-R1）专门优化了提示词以增强其对结构失真的识别能力，所有方法均采用2fps采样进行评估。

### 人类偏好对齐任务

在REACT-Video基准上，REACT在人类偏好对齐任务中显著优于现有SOTA方法（Table 1）。具体而言，REACT在含平局准确率（Acc w/ Tie）上达到**0.610**，较最优基线UnifiedReward（0.416）提升**+0.194**；在不含平局准确率（Acc w/o Tie）上达到**0.813**，较UnifiedReward（0.701）提升**+0.112**。这一结果表明，现有视频级评估器倾向于基于美学和时序一致性给出高分，即使在存在严重结构缺陷的情况下也是如此，而REACT通过帧级推理能够更准确地反映人类对结构失真的偏好判断。

![[assets/figures/papers/paper_list_l2284_https_arxiv_org_abs_2601_04033/figures/003_Table_1.jpg]]
*Table 1: Comparison of REACT with SOTA Models on Human Preference Alignment. The best and second-best results are highlighted in bold, and “+Rep” indicates that the model is evaluated with a refined prompt. Our REACT model outperforms existing methods, achieving the highest accuracy in preference assignment based on structural distortion*

### 失真识别任务

在REACT-Frame基准上，REACT在失真帧识别中取得了最高的**F1分数0.845**，显著优于图像评估器MagicAssessor（0.765）和通用模型GPT-4o（0.713），在正常帧识别上也以**0.671**的F1分数领先（Table 2）。值得注意的是，尽管图像评估器在传统图像伪影识别上表现良好，但在生成视频帧的结构失真检测中能力不足，REACT通过定制化的失真分类体系和思维链推理有效弥补了这一差距。

![[assets/figures/papers/paper_list_l2284_https_arxiv_org_abs_2601_04033/figures/004_Table_2.jpg]]
*Table 2: Comparison of REACT with SOTA Models in Distortion Recognition. The best and second-best results are marked in bold and underlined, respectively. Our REACT model achieves the highest F1-score in distinguishing distorted frames, demonstrating its superior accuracy in recognizing structural distortions in video frames*

### 消融实验

消融实验系统验证了REACT各设计组件的贡献（Table 3和Table 4）：

- **两阶段训练的必要性**：移除SFT阶段（仅进行RL训练）导致偏好对齐准确率从0.610骤降至**0.387**，表明SFT为RL提供了关键的初始化基础。
- **偏好奖励的作用**：移除偏好奖励后，Acc w/ Tie降至**0.352**，说明配对偏好信号对模型学习人类偏好至关重要。
- **动态采样机制**：禁用动态采样使Acc w/ Tie降至**0.519**，验证了自适应选择失真帧策略的有效性。
- **Masked Loss**：在SFT第二阶段使用masked loss在失真识别任务中获得最佳F1分数，表明该策略有效防止了领域知识注入过程中的过拟合。

### 通用基准与生成质量提升

在GenAI Benchmark和VideoGen-RewardBench上的额外实验（Table 5）显示，REACT在通用视频评估任务上的总体偏好准确率略低于视频级评估器，反映出其帧级分析范式在综合视觉质量评估上的固有局限——无法充分捕捉需要跨帧时序上下文的失真（如瞬时闪烁）。然而，在VBench上评估奖励模型对视频生成质量的提升效果时（Table 6），REACT在Imaging Quality（0.691）和Aesthetic Quality（0.549）上均达到与UnifiedReward相当的水平，且将其与其他SOTA奖励模型集成可带来额外增益，表明REACT的结构失真评估能力与现有方法具有互补性。

![[assets/figures/papers/paper_list_l2284_https_arxiv_org_abs_2601_04033/figures/011_Table_6.jpg]]
*Table 6: Comparison of Reward Models for Improving Video Generation Quality on VBench. Our REACT substantially improves video generation quality, and integrating it with other SOTA reward models yields additional gains*

![[assets/figures/papers/paper_list_l2284_https_arxiv_org_abs_2601_04033/figures/008_Table_5.jpg]]
*Table 5: Additional Experiments on GenAI Benchmark and VideoGen-RewardBench*

### 失败模式分析

REACT的主要失败模式集中在以下方面：①帧级分析无法有效捕获需要时序上下文的失真类型（如瞬时闪烁、物体消失），这是方法设计的固有局限；②动态采样机制依赖预设阈值，在失真分布极端的场景下可能采样不足或过度；③训练数据集中于特定T2V模型生成的视频，当面对分布偏移较大的新模型输出时，泛化能力可能受限。这些失败模式指向了未来将帧级推理扩展到时空上下文建模的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l2284_https_arxiv_org_abs_2601_04033/figures/005_Table_3.jpg]]
*Table 3: Ablation Study on RL Starting Point, Reward Design, and Sampling Mechanism in Human Preference Alignment. Our REACT model with the default settings performs best*

![[assets/figures/papers/paper_list_l2284_https_arxiv_org_abs_2601_04033/figures/006_Table_4.jpg]]
*Table 4: Ablation Study on RL Starting Point, SFT Epoch, and Loss Function in Distortion Recognition Task. Our REACT model, trained with a two-stage paradigm (i.e., SFT and GRPO) and utilizing masked loss in the second epoch of SFT, achieves the best performance in distortion recognition*

## 方法谱系与知识库定位

### 1. 问题域定位：生成视频结构失真评估的空白

当前生成视频评估的主流范式以视频级奖励模型（Video Reward Model）为核心，代表性工作包括 **VideoScore2**、**UnifiedReward** 和 **VideoReward**。这些模型的设计目标是对视频的整体美学质量、运动平滑度和文本对齐度进行综合评分。然而，REACT 揭示了一个关键的评估盲区：**即使视频在美学和时序一致性上获得高分，仍可能包含严重的结构失真**（如肢体变形、物体穿透、多肢等）。Figure 1 直观地展示了这一断层——现有评估器倾向于对存在结构缺陷的视频赋予高分，而 REACT 能够精确识别这些失真并给出更可靠的评分。

与图像质量评估器（如 **Q-Insight**、**VisualQuality-R1**、**MagicAssessor**）相比，REACT 的定位差异更为微妙。图像评估器擅长识别生成图像中的伪影（artifacts），但在面对生成视频帧时，其性能显著下降。原因在于，视频帧中的结构失真往往与运动模糊、压缩伪影等视频特有噪声耦合，且失真形态（如肢体穿透、物体融合）与静态图像伪影存在本质差异。REACT 通过构建面向生成视频的**八类结构失真分类体系**（Figure 3），填补了这一跨模态评估的鸿沟。

### 2. 方法谱系：从通用 MLLM 到专用帧级奖励模型

REACT 的方法演进路径可概括为：**通用多模态语言模型 → 监督微调注入领域知识 → 强化学习对齐人类偏好**。

**基座模型选择**：REACT 以 **Qwen2.5-VL-7B** 为基座，这与直接使用更大规模通用模型（如 **Qwen2.5-VL-32B**、**Gemini-2.5-Pro**、**GPT-4o**）的策略形成对比。实验表明，未经领域适配的通用 MLLM 在结构失真识别上表现不佳——即使 Gemini-2.5-Pro 在失真帧 F1 上也仅为 0.765，远低于 REACT 的 0.845（Table 2）。这说明**通用视觉语言能力无法自动迁移到精细的结构失真判别任务**。

**训练范式创新**：REACT 采用两阶段训练框架，这在视频奖励模型领域具有独特性：

- **第一阶段（SFT）**：传统做法是单轮 SFT，但 REACT 引入第二 epoch 的 **masked loss** 机制，仅对模型输出部分计算损失，防止对预训练知识的灾难性遗忘。消融实验（Table 4）证实，masked loss 使失真帧 F1 从 0.824 提升至 0.845。
- **第二阶段（GRPO）**：REACT 将分组相对策略优化（GRPO）引入视频评估任务，并设计了**配对 BTT 奖励**（pairwise BTT reward），利用训练帧对的偏好标签为每个 rollout 分配奖励。这与标准 RLHF 中使用单一标量奖励的方式不同，能够更精细地捕捉帧间质量的细微差异。

**推理机制差异**：REACT 的**动态两阶段采样机制**是其区别于固定帧率采样评估器的关键设计。第一阶段均匀采样获取全局质量分布，第二阶段根据得分自适应选择最可能包含失真的帧进行精细分析。Table 3 消融显示，禁用动态采样导致偏好对齐准确率从 0.610 降至 0.519，降幅达 9.1 个百分点，验证了该机制的核心作用。

### 3. 与现有工作的关系：互补而非替代

REACT 并非旨在替代视频级评估器，而是与之形成互补。Table 5 的结果揭示了这一关系：在通用视频评估基准 VideoGen-RewardBench 上，REACT 的总体偏好准确率略低于视频级评估器，反映出其对综合视觉质量的评估能力有限。但在结构失真敏感的 REACT-Video 基准上，REACT 以 0.813 的准确率（w/o Tie）显著超越 UnifiedReward 的 0.701。

Table 6 进一步验证了互补性：将 REACT 与 UnifiedReward 等视频级奖励模型联合使用时，在 VBench 上的视频生成质量（Imaging Quality 和 Aesthetic Quality）获得额外提升。这表明 REACT 捕获的帧级结构信息是现有视频评估器所缺失的关键维度。

### 4. 适用边界与局限性

基于论文提供的证据，REACT 的适用边界可归纳为以下四点：

**（1）帧级分析的时间盲区**：REACT 的核心设计是逐帧推理，这使其天然无法捕获需要跨帧时序上下文的失真类型。论文明确承认，瞬时闪烁、物体突然消失等时序依赖缺陷超出了模型的能力范围。这是方法架构层面的固有限制，而非训练数据或模型规模可解决的问题。

**（2）通用视频质量评估的局限**：REACT 在 VideoGen-RewardBench 上的表现表明，其对美学构图、色彩和谐度、运动流畅性等传统视频质量维度的评估能力弱于专用视频评估器。这意味着 REACT 更适合作为结构失真检测的专用工具，而非通用的视频评分器。

**（3）动态采样阈值的敏感性**：动态采样机制依赖预设阈值来判定帧是否"可能包含失真"。论文未详细讨论阈值的调优策略或跨数据集的鲁棒性，这暗示该机制可能在某些场景下性能不稳定，需要手动验证。

**（4）训练数据的分布偏移风险**：REACT 的训练数据来源于特定 T2V 模型（论文未明确列出所有模型）生成的视频。随着视频生成模型快速迭代（如 **Sora** [OpenAI, 2024]、**Hailuo** [MiniMax, 2024]），新型失真模式可能出现，导致模型泛化能力下降。论文未提供跨生成器分布的泛化实验，这一点需要进一步验证。

### 5. 开放问题

1.  **时空推理扩展**：如何将帧级推理扩展到时序维度？可能的路径包括引入时序注意力机制或设计跨帧一致性奖励，使模型能够建模运动轨迹异常和时间上的失真传播。

2.  **多粒度评估融合**：能否将 REACT 的结构失真评估能力与视频级评估器（如 UnifiedReward）融合为统一的视频奖励模型？这需要在架构层面解决帧级信号与视频级信号的权重分配问题。

3.  **自动化阈值调优**：动态采样机制的阈值是否可以自动化学习？例如，通过元学习或基于验证集反馈的自适应调整策略，减少人工调参的依赖。

4.  **失真分类体系的完备性**：当前八类失真是否覆盖了所有生成视频结构缺陷？随着视频生成技术的发展，可能需要持续扩展分类体系（如增加"物理规律违反"类别），这要求数据标注和模型训练流程具备可扩展性。

## 原文 PDF

![[paperPDFs/CVPR_2026/Thinking_with_Frames_Generative_Video_Distortion_Evaluation_via_Frame_Reward_Model.pdf]]
