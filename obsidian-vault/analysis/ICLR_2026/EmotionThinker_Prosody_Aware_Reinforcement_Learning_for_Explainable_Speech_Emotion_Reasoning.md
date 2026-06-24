---
title: "EmotionThinker: Prosody-Aware Reinforcement Learning for Explainable Speech Emotion Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EmotionThinker_Prosody_Aware_Reinforcement_Learning_for_Explainable_Speech_Emotion_Reasoning.pdf
openreview_forum_id: wbttgzp7MT
aliases:
- EmotionThinker
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过构建韵律感知的推理数据集（EmotionCoT-35K）并对基模型进行韵律增强微调，再结合逐步信任感知推理奖励的强化学习（GRPO-PTR），模型可主动学习利用声学线索进行多步推理，显著提升情感识别准确性和解释性。"
primary_logic: "将语音情感识别重新定义为深度推理问题，利用韵律增强和逐步信任感知推理奖励来平衡推理过程与结果准确性，从而首次实现可解释的语音情感推理。"
claims:
- "在四个情感识别基准上，EmotionThinker的平均准确率达到68.89%，超越之前最好的情感专用模型BLSP-Emo（65.41%）和其他所有基线模型。"
- "消融实验表明，所提出的GRPO-PTR在SER准确率和推理得分上均优于标准GRPO和纯监督微调（SFT），去除训练后的奖励模型或信任权重均导致性能下降。"
- "韵律中心的有监督微调使基模型的韵律感知能力大幅提升，例如音高感知准确率从25.71%提升至75.11%，验证了韵律增强的必要性。"
- "人类评估显示，EmotionThinker在所有推理质量维度上均显著优于代表性基线模型，在事实对齐和描述完整度方面表现尤为突出。"
---

# EmotionThinker: Prosody-Aware Reinforcement Learning for Explainable Speech Emotion Reasoning

> [!tip] 核心洞察
> 将语音情感识别重新定义为深度推理问题，利用韵律增强和逐步信任感知推理奖励来平衡推理过程与结果准确性，从而首次实现可解释的语音情感推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | EmotionThinker：基于韵律感知的强化学习可解释语音情感推理 |
| 英文题名 | EmotionThinker: Prosody-Aware Reinforcement Learning for Explainable Speech Emotion Reasoning |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=wbttgzp7MT); [GitHub](https://github.com/dingdongwang/EmotionThinker) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | EmotionThinker |
| Dataset | IEMOCAP, MELD, RAVDESS, SAVEE |

> [!tip] 效果简介
> - IEMOCAP 上，Accuracy (%) 为 77.68，对比 76.00 (BLSP-Emo)，变化 +1.68。
> - MELD 上，Accuracy (%) 为 59.71，对比 59.13 (Kimi-Audio)，变化 +0.58。
> - RAVDESS 上，Accuracy (%) 为 71.56，对比 72.00 (BLSP-Emo)，变化 -0.44。

## 概述

### 问题瓶颈

现有语音大语言模型（SpeechLLMs）在语音情感识别（SER）中存在两个根本性缺陷。其一，模型普遍缺乏对韵律等细粒度声学细节的感知能力，仅依赖语义或粗粒度声学表征进行判断。其二，主流方法将情感识别简化为分类任务，输出仅为离散情感标签，无法提供可解释的推理过程。此外，该领域长期缺乏带有细粒度推理标注的训练数据，进一步制约了模型的可解释性发展。

### 核心方法

EmotionThinker 针对上述瓶颈提出三阶段训练框架：

1. **EmotionCoT-35K 数据集构建**：通过自动化标注管线，整合韵律特征提取与 GPT-4o 推理生成，构建首个韵律感知的思维链情感推理数据集（35K 样本）。
2. **韵律增强基座训练**：基于 Qwen2.5-Omni-7B 进行韵律中心的有监督微调，使模型获得对音高、语速、能量、语调、重音等声学特征的感知能力。
3. **GRPO-PTR 强化学习**：提出逐步信任感知推理奖励（Progressive Trust-aware Reasoning Reward），结合格式奖励与结果准确性奖励，通过强化学习优化策略模型，在推理过程与结果准确性之间取得平衡。

### 关键结果

在 IEMOCAP、MELD、RAVDESS 和 SAVEE 四个情感识别基准上，EmotionThinker 的平均准确率达到 **68.89%**，超越此前最优的情感专用模型 BLSP-Emo（65.41%）及其他 16 个开源 SpeechLLM 基线。在推理质量方面，EmotionThinker 的四维评分（事实对齐、解释质量、描述完整度、流畅性与结构）平均得分 **3.98**（满分 5），显著优于最强基线 MERaLiON2 的 3.04 分。人类评估进一步验证了其在事实对齐和描述完整度上的突出优势。

### 方法谱系与知识库定位

EmotionThinker 位于语音情感识别与可解释推理的交叉地带，其方法谱系可沿两个维度定位：

- **模型架构谱系**：以全模态大模型 Qwen2.5-Omni-7B 为基座，区别于通用语音大模型（如 **GLM-4-Voice**、**Qwen-Audio-Chat**、**Kimi-Audio**）和情感专用语音大模型（如 **BLSP-Emo**、**SECap**），EmotionThinker 通过韵律增强微调赋予基座模型声学感知能力，再以强化学习注入推理能力。

- **训练策略谱系**：相较于直接监督微调（SFT）或标准 GRPO 仅依赖规则奖励的做法，GRPO-PTR 引入训练后的推理奖励模型，并设计信任权重机制抑制噪声奖励，实现了推理质量与识别准确率的联合优化。消融实验表明，移除推理奖励模型或信任权重均导致性能显著下降，验证了该策略的必要性。

## 背景与动机

语音情感识别（Speech Emotion Recognition, SER）旨在从语音信号中自动辨识说话人的情感状态，是情感计算与人机交互领域的核心任务。长期以来，主流方法将其建模为一个封闭式分类问题：输入一段语音，输出一个离散的情感标签（如“愤怒”“悲伤”“中性”）。然而，这种“黑箱”范式存在两个根本性缺陷。

**第一，缺乏对声学细节的结构化感知。** 语音中的韵律特征——音高、语速、能量、语调和重音——是情感表达的核心载体。例如，悲伤语音通常伴随较低的音高、缓慢的语速和减弱的能量；愤怒则表现为音高升高、语速加快和能量集中。现有语音大语言模型（SpeechLLMs）虽然能够处理语音输入并生成文本响应，但其内部表示往往以语义为中心，对上述细粒度声学线索的感知能力严重不足。换言之，模型“听到”了语音，却未能“听懂”其中的韵律信息。

**第二，无法提供可解释的推理过程。** 仅输出一个情感标签，既无法解释模型为何做出该判断，也无法让用户信任其结果。在医疗诊断、心理健康监测、教育反馈等高风险场景中，这种不可解释性构成了部署障碍。部分近期工作尝试为语音情感生成描述性文字（如SECap、OSUM-EChat），但这些描述多为笼统的声学特征罗列，缺乏从声学线索到情感结论的因果推理链条。

上述两个缺陷的叠加，导致了一个更深层的瓶颈：**现有SpeechLLMs将情感识别视为“感知→分类”的单步映射，而非“感知→推理→判断”的多步认知过程。** 人类在识别他人情感时，会主动整合说话人特征、韵律线索、语义内容和上下文逻辑，形成可被审视和质疑的推理链。然而，目前没有任何公开的语音情感数据集提供此类思维链（Chain-of-Thought, CoT）标注，使得模型无法学习这一能力。

针对上述缺口，本文提出核心动机：**将语音情感识别重新定义为深度推理问题**——模型需要显式地分析韵律模式、整合多模态线索，并生成可验证的推理过程，最终给出情感判断。为实现这一目标，需要同时解决三个子问题：（1）构建包含韵律标注和推理链的训练数据；（2）增强基座模型对韵律特征的感知能力；（3）设计能够平衡推理质量与结果准确性的优化策略。

> **注意**：本章节基于论文引言与相关工作的分析综合而成。关于具体数据集的韵律标注细节、基座模型选型及强化学习框架的设计，将在后续章节中展开。

## 核心创新

EmotionThinker 的核心创新在于将语音情感识别（SER）从传统的分类任务重新定义为**可解释的深度推理问题**，并通过“数据—模型—训练策略”三个维度的协同改造，首次实现了基于韵律感知的语音情感推理。

### 创新一：韵律感知的思维链数据集（EmotionCoT-35K）

现有语音描述数据集（如 PromptSpeech、Expresso、EARS 等）普遍缺乏对韵律细节的细粒度标注和情感推理的思维链（CoT）标注（见 Table 1）。EmotionThinker 构建了首个韵律感知的 CoT 数据集 **EmotionCoT-35K**，包含 35K 条样本，每条样本均带有：
- **韵律标注**：音高（pitch）、语速（speed）、能量（energy）、语调（intonation）、重音（stress）等声学特征
- **推理文本**：由 GPT-4o 基于韵律提示生成的逐步推理过程，格式化为 `<think>` 和 `<answer>` 标签

这一数据集的构建填补了“声学细节感知”与“可解释推理”之间的数据空白，为后续的韵律增强训练和推理强化学习提供了基础。

### 创新二：韵律增强的基座模型（EmotionThinker-Base）

基于 **Qwen2.5-Omni-7B** 构建的 EmotionThinker-Base，通过韵律增强的有监督微调（SFT），使模型从“仅处理语义”升级为“语义+韵律”双通道感知。消融实验（Table 5）表明，该阶段使基模型的韵律感知能力大幅提升：
- 音高感知准确率：25.71% → **75.11%**
- 语速感知准确率：29.94% → **68.70%**
- 能量感知准确率：27.67% → **69.42%**

韵律感知能力的跃升是后续推理质量提升的关键前提——模型必须先“听见”声学线索，才能基于这些线索进行推理。

### 创新三：逐步信任感知推理奖励的强化学习（GRPO-PTR）

传统 GRPO 仅依赖结果准确性奖励（outcome reward），无法有效引导模型生成高质量的推理过程。EmotionThinker 提出的 **GRPO-PTR** 框架包含三个关键机制：

1. **训练专用的推理奖励模型（Reward Model）**：基于 Qwen2.5-Omni-3B 微调，从事实对齐、解释质量、描述完整度、流畅性与结构四个维度评估推理质量，输出标量奖励 $R_t$。

2. **信任权重 $\tau$**：根据正确预测组与错误预测组的平均推理奖励差异动态计算。当错误组的推理奖励更高时，信任权重呈指数衰减，抑制“推理看似合理但结论错误”的噪声奖励信号：
   $$\tau = \begin{cases} 1, & \bar{R}_t^{(c)} \ge \bar{R}_t^{(w)}, \\ \exp(\bar{R}_t^{(c)} - \bar{R}_t^{(w)}), & \bar{R}_t^{(c)} < \bar{R}_t^{(w)}. \end{cases}$$

3. **渐进式奖励调度**：训练初期仅使用规则奖励（格式奖励 $R_f$ + 结果奖励 $R_o$），待情感准确率稳定后再引入经信任权重调制的推理奖励，避免训练初期因推理信号不稳定导致的优化震荡。总奖励为：
   $$R_i = \alpha_f R_f + \alpha_o R_o + \alpha_t \tau \cdot R_t$$

消融实验（Table 4）验证了以上设计的有效性：GRPO-PTR 相比标准 GRPO，SER 准确率从 62.91% 提升至 68.89%，推理得分从 3.45 提升至 3.98；移除训练后的奖励模型或信任权重均导致性能显著下降。

### 方法谱系与知识库定位

EmotionThinker 在语音情感识别领域的方法谱系中占据独特位置：

| 方法类别 | 代表工作 | 核心能力 | 局限性 |
|---------|---------|---------|--------|
| 通用语音大模型 | Qwen2-Audio-Instruct、Kimi-Audio、SALMONN 等 | 通用语音理解 | 缺乏韵律感知，仅输出分类标签 |
| 情感专用语音大模型 | BLSP-Emo、SECap、OSUM-EChat | 情感识别优化 | 仍以分类为主，缺乏可解释推理 |
| 全模态大模型 | Qwen2.5-Omni-7B、Phi-4-Multimodal | 多模态融合 | 情感推理能力未专门优化 |
| **EmotionThinker（本工作）** | — | **韵律感知 + 可解释推理** | 训练数据规模有限，跨语言泛化待验证 |

EmotionThinker 的关键突破在于：通过 **EmotionCoT-35K** 提供韵律-推理对齐数据，通过 **韵律增强 SFT** 赋予模型声学感知能力，通过 **GRPO-PTR** 实现推理过程与结果准确性的平衡优化。三者形成闭环，使模型首次能够基于声学线索进行多步推理并输出可解释的情感判断。

## 整体框架

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_wbttgzp7MT/figures/004_Figure_3.jpg]]
*Figure 3: Architecture of EmotionThinker with the proposed GRPO-PTR framework. The upper part depicts the high-level GRPO-PTR training pipeline, where only the policy model is optimized. The lower part details PTR strategy, which progressively introduces reasoning reward to stabilize training and enhance reasoning*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_wbttgzp7MT/figures/003_Table_1.jpg]]
*Table 1: Comparison of different speech captioning datasets across various acoustic features. Reasoning denotes the availability of emotion reasoning with chain-of-thought (CoT) annotations*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_wbttgzp7MT/figures/002_Figure_2.jpg]]
*Figure 2: EmotionCoT-35K data curation pipeline*

EmotionThinker 提出了一套三阶段训练框架，旨在赋予语音大语言模型可解释的情感推理能力。其核心逻辑是：**先教会模型“听”韵律，再教会模型“想”情感，最后通过强化学习让模型“说”出推理过程**。

### 三阶段训练管线

整个框架按照因果依赖关系组织为三个递进阶段：

**阶段一：韵律增强监督微调**
基座模型 Qwen2.5-Omni-7B 在包含韵律标注的语音数据上进行监督微调，使其获得对音高、语速、能量、语调、重音等声学特征的感知能力。这一阶段产出的模型称为 EmotionThinker-Base，是后续推理训练的基础。

**阶段二：冷启动推理监督微调**
利用 EmotionCoT-35K 数据集对 EmotionThinker-Base 进行推理格式的冷启动训练。该数据集中的每条样本均包含 `<think>` 和 `<answer>` 标签结构，模型学习在 `<think>` 块中输出多步推理过程，在 `<answer>` 块中给出情感标签。此阶段使模型初步掌握“先推理、后分类”的输出范式。

**阶段三：GRPO-PTR 强化学习后训练**
在前两阶段的基础上，采用所提出的 **逐步信任感知推理奖励（GRPO-PTR）** 策略进行强化学习优化。该阶段仅优化策略模型，通过三类奖励信号的加权组合引导模型提升推理质量和识别准确率。

### 模块关系与数据流

下图展示了框架中关键模块的协作关系：

```
EmotionCoT-35K 数据构建管线
    │
    ├──→ [阶段一] 韵律增强 SFT → EmotionThinker-Base
    │                                    │
    └──→ [阶段二] 冷启动推理 SFT ←────────┘
                                        │
                                        ▼
                              [阶段三] GRPO-PTR RL
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
              格式奖励 Rf          结果奖励 Ro          推理奖励 τ·Rt
                    │                   │                   │
                    └───────────────────┼───────────────────┘
                                        ▼
                                  总奖励 Ri = αf·Rf + αo·Ro + αt·τ·Rt
                                        │
                                        ▼
                                  最终策略模型
```

**输入流：** 原始语音音频 → 韵律特征提取器（外部工具）→ 韵律描述文本 + 语音 Token → EmotionThinker 模型。

**输出流：** 模型生成包含 `<think>推理过程</think><answer>情感标签</answer>` 的结构化文本。

### 关键模块说明

1. **EmotionCoT-35K 数据构建管线**（Figure 2）：自动标注管线首先利用外部特征提取器获取音高、语速、能量、语调和重音的归一化描述，随后将这些韵律信息作为上下文提示输入 GPT-4o，生成逐步推理轨迹。每条推理轨迹经人工审核后，形成包含韵律标注和思维链推理的完整训练样本。该数据集覆盖 9 类情感，总计约 35K 条样本，是首个面向语音情感识别的韵律感知思维链数据集（Table 1）。

2. **推理奖励模型（Reward Model）**：基于 Qwen2.5-Omni-3B 构建，在 101,400 条 (问题, 推理, 评分) 三元组上微调，用于评估开放域推理的四个维度：事实对齐（Factual Alignment）、解释质量（Interpretative Quality）、描述完整度（Caption Completeness）和流畅性与结构（Fluency and Structure）。四个维度的评分归一化后加权求和得到标量推理奖励 $R_t$。

3. **GRPO-PTR 策略**：采用渐进式奖励调度——训练初期仅使用格式奖励 $R_f$ 和结果奖励 $R_o$，待情感准确率稳定后再引入推理奖励 $R_t$。同时引入信任权重 $\tau$，当错误预测组的平均推理奖励高于正确组时，$\tau$ 呈指数衰减以抑制噪声奖励信号。

### 框架设计的因果逻辑

现有语音大语言模型的核心瓶颈在于：**缺乏对韵律细节的感知能力，且仅将情感识别视为分类任务**。EmotionThinker 通过三个因果干预点解决这一问题：
- **韵律增强 SFT** 解决了“模型听不到声学线索”的问题（韵律感知准确率提升 2 倍以上，Table 5）；
- **冷启动推理 SFT** 建立了“先推理后分类”的输出结构；
- **GRPO-PTR** 通过逐步引入带信任权重的推理奖励，平衡了推理过程质量与结果准确性，解决了标准 GRPO 中推理信号过早引入导致的训练不稳定问题（消融实验 Table 4 验证了渐进策略和信任权重的必要性）。

## 核心模块与公式推导

EmotionThinker 的核心架构由三个关键模块构成：**EmotionCoT-35K 数据构建管线**、**韵律增强基座模型（EmotionThinker-Base）** 和 **GRPO-PTR 强化学习框架**。各模块协同工作，将语音情感识别重新定义为可解释的深度推理问题。

### 3.1 EmotionCoT-35K 数据构建管线

该管线（Figure 2）是首个面向语音情感识别的韵律感知思维链数据集构建流程。其核心机制为：首先利用外部特征检测器从原始语音中提取音高、语速、能量、语调和重音等细粒度韵律标注；随后将这些韵律信息作为上下文提示输入 GPT-4o，生成包含逐步推理过程的情感解释文本。输出被格式化为 `<think>`（推理过程）和 `<answer>`（情感标签）XML 标签结构，为后续监督微调和强化学习提供结构化训练信号。

与现有语音描述数据集（Table 1）相比，EmotionCoT-35K 在声学特征覆盖（涵盖 9 类特征）和推理标注（首次引入 CoT 注释）两个维度上具有显著优势。

### 3.2 韵律增强基座模型

EmotionThinker-Base 基于 Qwen2.5-Omni-7B 构建，通过两阶段监督微调实现韵律感知能力的冷启动：

- **韵律增强 SFT**：在 500+ 小时韵律增强语音数据上训练一个 epoch，使基座模型学会识别和利用声学线索。消融实验（Table 5）表明，该阶段使音高感知准确率从 25.71% 提升至 75.11%，能量感知从 27.67% 提升至 69.42%，验证了韵律增强的必要性。
- **冷启动推理 SFT**：使用 EmotionCoT-35K 数据训练模型遵循 `<think>/<answer>` 格式输出推理链，为后续强化学习提供初始策略。

### 3.3 GRPO-PTR 强化学习框架

GRPO-PTR（GRPO with Progressive Trust-aware Reasoning）是 EmotionThinker 的核心训练框架（Figure 3），在标准 GRPO 基础上引入**渐进式信任感知推理奖励**机制。

#### 3.3.1 基础奖励函数

框架首先定义两个规则奖励：

**格式奖励**：
$$R_{\mathrm{f}}(o) = \begin{cases} 1, & o \text{ follows the format schema}, \\ 0, & \text{otherwise}. \end{cases}$$
奖励输出是否遵循预定义的 `<think>/<answer>` XML 标签结构。

**结果准确性奖励**：
$$R_{\circ}(\hat{y}, y^*) = \begin{cases} 1, & \hat{y} = y^*, \\ 0, & \text{otherwise}. \end{cases}$$
当预测情感标签与真实标签一致时给予奖励。

#### 3.3.2 推理奖励与信任机制

为评估开放域推理质量，框架训练了一个基于 Qwen2.5-Omni-3B 的推理奖励模型（Reward Model），在 101,400 个 `(问题, 推理, 评分)` 三元组上微调，输出四个维度的评分：事实对齐（Factual Alignment）、解释质量（Interpretative Quality）、描述完整度（Caption Completeness）和流畅性与结构（Fluency and Structure）。

**标量推理奖励**将四维评分归一化后加权求和：
$$R_t = \sum_{j=1}^{4} w_j \tilde{g}_j, \quad \tilde{g}_j = \frac{g_j}{5}, \; \sum_j w_j = 1, w_j \ge 0$$

**信任权重**用于抑制奖励模型在错误样本上仍给出高推理评分的噪声：
$$\tau = \begin{cases} 1, & \bar{R}_t^{(c)} \ge \bar{R}_t^{(w)}, \\ \exp(\bar{R}_t^{(c)} - \bar{R}_t^{(w)}), & \bar{R}_t^{(c)} < \bar{R}_t^{(w)}. \end{cases}$$
其中 $\bar{R}_t^{(c)}$ 和 $\bar{R}_t^{(w)}$ 分别为正确组和错误组的平均推理奖励。当错误组推理奖励更高时，信任权重呈指数级衰减。

**渐进式调度策略**：训练初期仅使用 $R_{\circ}$ 和 $R_{\mathrm{f}}$ 优化，待情感准确率稳定后再引入推理奖励，避免过早引入复杂信号导致训练不稳定。

**总体奖励**为各信号的加权和：
$$R_i = \alpha_f R_f + \alpha_o R_o + \alpha_t \tau \cdot R_t$$
默认权重设置为 $\alpha_f = 0.3$、$\alpha_o = 1.0$、$\alpha_t = 0.5$。敏感性分析（Table 7）表明，将 $\alpha_t$ 增大至 1.0 会导致平均准确率下降至 65.52%，凸显多信号强化学习中奖励平衡的重要性。

消融实验（Table 4）验证了各组件的有效性：移除训练后的奖励模型（V3）使推理得分从 3.98 降至 3.36；移除信任权重 $\tau$（V4）使 ER 得分降至 3.74；禁用渐进式调度（V5）同样导致性能下降。完整的 GRPO-PTR（V6）在 SER 准确率（68.89%）和推理得分（3.98）上均达到最优。

## 实验与分析

### 主实验结果

**情感识别基准测试**。在四个标准情感识别基准（IEMOCAP、MELD、RAVDESS、SAVEE）上，EmotionThinker 的平均准确率达到 **68.89%**，超越此前最优的情感专用模型 **BLSP-Emo**（65.41%）达 3.48 个百分点，同时优于所有 16 个开源基线模型（Table 2）。在单一数据集层面，EmotionThinker 在 IEMOCAP（77.68%）、MELD（59.71%）和 SAVEE（73.96%）上均取得领先，仅在 RAVDESS 上以 71.56% 略低于 BLSP-Emo（72.00%），差距为 -0.44%。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_wbttgzp7MT/figures/005_Table_2.jpg]]
*Table 2: Performance comparison across models. Emotion recognition is measured by accuracy (%), while reasoning quality is assessed on the overall test dataset on four dimensions: Factual Alignment (FA.), Interpretative Quality (IQ.), Caption Completeness (CC.), and Fluency and Structure (FS.), each on a 5-point scale. Top two results are highlighted in bold and underline, respectively*

**推理质量评估**。在 5 分制的推理质量评分中，EmotionThinker 以平均 **3.98** 分显著超越次优模型 MERaLiON2（3.04 分），领先幅度达 0.94 分（Table 2）。四个评估维度中，模型在事实对齐（FA）和描述完整度（CC）方面表现尤为突出。

**人类评估验证**。在 100 个样本的人工评估中，EmotionThinker 在所有推理质量维度上均优于代表性基线（Table 3）：事实对齐 3.7 分、可解释性质量 4.2 分、描述完整度 4.7 分、流畅性与结构 4.9 分，平均分 4.4 分。相比之下，次优模型 Qwen2.5-Omni-7B 平均仅 3.5 分，而通用语音大模型 BLSP 仅 1.7 分，表明韵律感知和推理增强对生成质量的关键作用。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_wbttgzp7MT/figures/006_Table_3.jpg]]
*Table 3: Human evaluation results on emotion reasoning based on a consistent 100-sample set*

### 消融实验

**训练策略对比**（Table 4）。以纯监督微调（SFT，Baseline 2）为起点，逐步引入各组件的效果如下：
- **标准 GRPO**（V1）：仅使用格式奖励和结果准确率奖励，SER 准确率 62.91%，推理得分 3.45。
- **GRPO-PTR**（V6，完整方法）：SER 准确率提升至 68.89%，推理得分提升至 3.98，较标准 GRPO 分别提升 5.98 个百分点和 0.53 分。
- **移除训练后的奖励模型**（V3）：推理得分大幅下降至 3.36，验证了专门训练推理奖励模型的必要性。
- **移除信任权重 τ**（V4）：推理得分从 3.98 降至 3.74，表明信任机制有效抑制了噪声奖励的干扰。
- **移除渐进式调度**（V5）：同时引入所有奖励信号导致性能下降，凸显逐步引入推理奖励对训练稳定性的重要性。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_wbttgzp7MT/figures/008_Table_4.jpg]]
*Table 4: Ablation study on different training strategies for average speech emotion recognition accuracy (SER) and emotion reasoning (ER) score, evaluated on the overall test dataset. Variants V1–V6 are built upon Baseline 2*

**韵律增强验证**（Table 5）。对比基座模型 Qwen2.5-Omni-7B 与经过韵律增强 SFT 的 EmotionThinker-Base，韵律感知能力实现跨越式提升：音高准确率从 25.71% 升至 75.11%，语速从 29.94% 升至 68.70%，能量从 27.67% 升至 69.42%，语调从 25.83% 升至 60.25%，重音从 30.24% 升至 71.50%。这证实了韵律增强微调是赋予模型声学细节感知能力的关键步骤。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_wbttgzp7MT/figures/009_Table_5.jpg]]
*Table 5: Prosody perception comparison across pitch (Pit.), speed (Spee.), energy (Ene.), intonation (Into.), and stress (Stre.). Evaluation is based on accuracy (%). Table 6: GRPO-PTR with varying K settings*

### 超参数与敏感性分析

**采样规模 K 的影响**（Table 6）。GRPO-PTR 在 K=8 时取得最佳平均性能（67.35%），K 过小（4）或过大（16）均导致性能下降，表明适中的候选采样数有利于平衡探索与利用。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_wbttgzp7MT/figures/010_Table_6.jpg]]

**奖励权重的敏感性**（Table 7）。固定结果奖励权重 α_o=1.0，调节推理奖励权重 α_t：
- α_t=0.5 时平均准确率最高（68.89%）。
- α_t 增至 1.0 时，平均准确率降至 65.52%，表明过度强调中间推理信号会引发优化不稳定，凸显多信号强化学习中奖励平衡的重要性。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_wbttgzp7MT/figures/011_Table_7.jpg]]
*Table 7: Sensitivity analysis on reward penalty*

### 失败模式与局限性

1. **RAVDESS 上的性能回退**：EmotionThinker 在 RAVDESS 上略低于 BLSP-Emo（-0.44%），可能与该数据集情感表达较为夸张、韵律模式与训练数据分布存在偏差有关，具体原因需进一步验证。

2. **推理质量评估的主观性**：尽管有人类评估校准，推理质量的自动评分仍依赖 GPT-4o，评分标准的主观性可能影响结论的稳健性。

3. **数据规模与覆盖范围**：EmotionCoT-35K 仅覆盖 9 类情感，训练数据以英语为主，在极端情感或跨语言场景下的泛化能力未经验证。

4. **强化学习对超参数的敏感性**：α_t 和 K 的取值对最终性能有显著影响，实际部署时需仔细调参。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_wbttgzp7MT/figures/014_Table_8.jpg]]
*Table 8: Case study comparing emotion reasoning outputs from EmotionThinker and 12 representative SpeechLLMs on the same audio sample. The ground-truth label is sad, and the analysis highlights differences in prosodic cue recognition, semantic integration, and logical coherence across models. EmotionThinker demonstrates more accurate and comprehensive capture of acoustic information, together with stronger logical consistency in its emotion reasoning*

## 方法谱系与知识库定位

### 核心瓶颈与因果机制

现有语音大语言模型（SpeechLLMs）在处理语音情感时面临双重瓶颈：**（1）韵律感知缺失**——通用语音模型（如 **Qwen2-Audio-Chat**、**SALMONN**、**Kimi-Audio**）和全模态模型（如 **Qwen2.5-Omni-7B**、**Phi-4-Multimodal**）主要依赖语义理解，对音高、语速、能量等声学细节缺乏感知能力；**（2）推理能力缺失**——即使情感专用模型（如 **BLSP-Emo**、**SECap**）也仅将情感识别视为分类任务，无法提供可解释的推理过程。此外，现有语音描述数据集（如 PromptSpeech、Expresso、EARS）在声学特征覆盖和思维链（CoT）标注上均存在不足（见 Table 1），导致模型无法学习利用声学线索进行多步推理。

EmotionThinker 的核心因果机制是：**将语音情感识别重新定义为深度推理问题**，通过构建韵律感知的推理数据集（EmotionCoT-35K）并对基模型进行韵律增强微调，再结合逐步信任感知推理奖励的强化学习（GRPO-PTR），使模型主动学习利用声学线索进行多步推理，从而同时提升情感识别准确性和解释性。

### 方法谱系定位

EmotionThinker 处于三个研究方向的交汇点：

**（1）通用语音大模型的继承与突破**：基座模型选用 **Qwen2.5-Omni-7B**（Xu et al., 2025b），这是一个全模态大模型，具备语音-文本联合理解能力。与 **GLM-4-Voice**、**MERaLiON2**、**MiniCPM-O**、**Megrez-3B-Omni** 等同类模型相比，EmotionThinker 的关键突破在于引入韵律增强微调（韵律感知准确率提升 2 倍以上，见 Table 5）和推理强化学习，而非仅依赖预训练的语义能力。

**（2）情感专用模型的超越**：**BLSP-Emo** 是此前表现最好的情感专用语音大模型（平均准确率 65.41%），但其缺乏推理能力。**SECap** 和 **OSUM-EChat** 虽关注情感描述，但未引入韵律感知和强化学习优化。EmotionThinker 在平均准确率上超越 BLSP-Emo 约 3.5 个百分点（68.89% vs 65.41%），同时首次实现可解释推理（推理得分 3.98/5.0，超越第二名 MERaLiON2 的 3.04，见 Table 2）。

**（3）强化学习训练范式的创新**：标准 GRPO（Shao et al., 2024）仅依赖基于输出标签准确性的规则奖励。EmotionThinker 提出的 GRPO-PTR（Progressive Trust-aware Reasoning）引入三个关键创新：
- **逐步奖励调度**：训练初期仅使用格式奖励 $R_{\mathrm{f}}$ 和结果奖励 $R_{\circ}$，待模型适应后再引入推理奖励 $R_t$，避免早期训练不稳定；
- **训练后的推理奖励模型**：基于 Qwen2.5-Omni-3B 微调，在 101,400 个 $(q, r, g)$ 元组上训练，从事实对齐、解释质量、描述完整度、流畅性与结构四个维度评估推理质量；
- **信任权重机制**：根据正确组和错误组平均推理奖励的差异计算信任权重 $\tau$，当错误组推理奖励更高时呈指数级衰减，有效抑制噪声奖励。

### 关键证据链

**决定性证据**：
- 在四个情感识别基准（IEMOCAP、MELD、RAVDESS、SAVEE）上，EmotionThinker 平均准确率 68.89%，超越 16 个开源 SpeechLLMs（Table 2，置信度 0.98）。
- 消融实验表明，GRPO-PTR 在 SER 准确率（68.89%）和推理得分（3.98）上均优于标准 GRPO（62.91%/3.45）和纯 SFT（66.67%/3.36）；移除训练后的奖励模型或信任权重均导致性能下降（Table 4，置信度 0.95）。
- 韵律中心 SFT 使基模型的音高感知准确率从 25.71% 提升至 75.11%，验证了韵律增强的必要性（Table 5，置信度 0.98）。

**弱证据或需人工验证的点**：
- 人类评估显示 EmotionThinker 在事实对齐（3.7）和描述完整度（4.7）上表现突出（Table 3），但评估仅基于 100 样本集，且评分主观性可能影响结论。
- 训练数据和评估主要基于英文情感数据集，泛化到其他语言的能力未经实验验证，需人工确认跨语言适用性。

### 适用边界与局限

**适用边界**：
- 适用于需要可解释情感推理的场景（如心理健康评估、对话系统情感分析），而非仅需分类标签的任务。
- 依赖外部韵律特征检测器（如音高、能量提取器），无法端到端学习韵律表示。
- 当前仅覆盖 9 类离散情感（EmotionCoT-35K 数据集），不适用于连续维度情感空间（如 Valence-Arousal-Dominance）。

**已知局限**：
- **数据偏见**：GRPO-PTR 依赖 GPT-4o 生成推理训练数据，可能继承大语言模型固有的偏见和错误。
- **规模限制**：模型规模（7B 参数）和训练数据量（35K 推理样本）可能限制在复杂或模棱两可情感中的推理能力。
- **超参数敏感性**：强化学习训练对超参数敏感——当推理奖励权重 $\alpha_t$ 从 0.5 增加到 1.0 时，平均准确率反而降至 65.52%（Table 7），实际部署时需仔细调参。
- **评估主观性**：推理质量评估部分依赖基于 GPT 的自动评分，尽管有人类评估作为校准，但评分标准的主观性仍可能影响结论。

### 开放问题

1. **细粒度情感扩展**：EmotionCoT 数据集仅覆盖 9 类情感，能否扩展到更细粒度或连续维度空间（如 Valence-Arousal）？
2. **信任权重泛化**：GRPO-PTR 的信任权重设计是否可在其他强化学习任务（如文本推理、多模态对齐）中推广？
3. **端到端韵律学习**：当前韵律特征提取依赖外部检测器，端到端的韵律学习是否可行且更优？
4. **多轮对话推理**：该框架能否与文本对话模型结合，实现多轮交互中的情感推理和动态更新？
5. **鲁棒性验证**：在嘈杂、重叠语音、多说话人等更具挑战性的场景下，框架的鲁棒性如何？需额外实验验证。
6. **跨语言泛化**：训练数据主要为英文，泛化到其他语言（如中文、阿拉伯语）的能力未经验证，需构建多语言韵律感知推理数据集。

## 原文 PDF

![[paperPDFs/ICLR_2026/EmotionThinker_Prosody_Aware_Reinforcement_Learning_for_Explainable_Speech_Emotion_Reasoning.pdf]]
