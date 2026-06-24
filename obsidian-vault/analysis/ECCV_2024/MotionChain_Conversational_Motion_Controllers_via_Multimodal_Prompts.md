---
title: "MotionChain: Conversational Motion Controllers via Multimodal Prompts"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts.pdf
aliases:
- MotionChain
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过构建统一的多模态离散令牌空间（运动、视觉、文本），并利用大规模预训练语言模型的上下文学习能力进行多轮指令微调，使模型能够根据对话历史连续生成运动或文本。
primary_logic: 将人体运动视为一种“外语”，通过VQ-VAE转化为离散令牌并与视觉、文本令牌统一表示，从而可以应用语言模型的序列建模和对话能力，实现多轮多模态交互。
claims:
- MotionChain由多模态分词器（文本、图像、运动至离散令牌）和视觉-运动感知语言模型构成，实现多模态统一学习。
- 多轮对话数据采用结构化格式，融合视觉令牌、源令牌和目标答案，使用统一的运动-语言词汇。
- MotionChain在运动推理任务上显著超越通用LLM，Bleu@1达37.92，而最佳基线Vicuna-1.5-7b为19.27。
- 令牌拼接（Tokens-joint）运动合成方法在时间连贯性上优于独立解码和基于过去条件的变体。
---

# MotionChain: Conversational Motion Controllers via Multimodal Prompts

> [!tip] 核心洞察
> 将人体运动视为一种“外语”，通过VQ-VAE转化为离散令牌并与视觉、文本令牌统一表示，从而可以应用语言模型的序列建模和对话能力，实现多轮多模态交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | MotionChain：通过多模态提示的对话式运动控制器 |
| 英文题名 | MotionChain: Conversational Motion Controllers via Multimodal Prompts |
| 会议/期刊 | ECCV 2024 |
| Links | [Code](https://github.com/OpenMotionLab/MotionChain) · [arXiv](https://arxiv.org/abs/2112.10752) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MotionChain |
| Dataset | Conversation test set, BABEL |

> [!tip] 效果简介
> - Conversation test set (Motion Reasoning) 上，Bleu@1 37.92 vs 19.27 (Vicuna-1.5-7b) (+18.65)。
> - BABEL (Temporal Motion Composition) 上，PA-MPJPE 53.72 vs 61.07 (TEACH) (-7.35)。

## 概述

**问题瓶颈**：现有运动生成模型仅支持单轮条件生成（如文本到运动），缺乏多轮对话上下文理解与连续运动生成能力。这导致用户无法通过直觉式多轮交互逐步细化运动指令，限制了在机器人示教、虚拟助手等场景中的应用。

**核心洞察**：MotionChain 将人体运动视为一种“外语”，通过 VQ-VAE 将连续运动序列转化为离散令牌，与文本令牌、视觉令牌统一在同一词汇空间中。基于这一统一表示，可以借助大规模预训练语言模型的序列建模与上下文学习能力，实现多轮、多模态的对话式运动生成与推理。

**方法定位**：MotionChain 属于**统一视觉-运动-语言生成式预训练模型**，由三个核心组件构成：
- **运动分词器**：基于 VQ-VAE + 残差量化，将原始运动编码为离散运动令牌并支持解码回连续运动。
- **视觉分词器**：通过冻结的 CLIP 视觉编码器提取特征，经可学习线性投影转换为与语言模型嵌入空间对齐的视觉令牌。
- **视觉-运动感知语言模型**：以 Flan-T5 为基座，使用统一的文本-运动词汇，自回归地根据多模态输入和对话历史生成运动序列或文本回复。

与现有工作的关键区别在于：基线方法（如 **T2M-GPT**、**MLD**、**MotionGPT**）仅处理单轮条件生成，模态间缺乏统一词汇；MotionChain 引入**统一离散词汇**、**多轮对话上下文拼接**以及**令牌拼接式运动合成**，实现了连续时间连贯的多轮运动生成。

**主要结果**：
- **运动推理**：在对话测试集上，MotionChain 的 Bleu@1 达到 37.92，显著优于最佳通用 LLM 基线 Vicuna-1.5-7b 的 19.27（Table 1）。
- **时间运动合成**：在 BABEL 数据集上，PA-MPJPE 为 53.72，优于 TEACH 的 61.07（Table 2）。
- **令牌拼接消融**：Tokens-joint 方式在时间连贯性上显著优于独立解码和基于过去条件的变体（Table 3, Fig. 4）。

**局限性**：当前模型仅支持关节人体运动，无法处理面部、手部以及人与物体/场景的交互。

## 背景与动机

### 问题背景：从单轮条件生成到对话式运动交互

生成式人体运动模型近年来取得了显著进展，特别是在文本到运动（text-to-motion）任务上，扩散模型、GPT式自回归模型等方法已能根据自然语言描述生成较为逼真的三维人体动作序列。然而，这些模型几乎无一例外地遵循“单轮条件生成”范式：用户提供一个描述性文本，模型输出一段对应的运动序列，交互随即终止。

这一范式在需要直觉式、多轮交互的实际场景中存在根本性局限。考虑以下典型需求：

- **机器人示教**：操作员通过连续的语言指令逐步调整机器人的动作，“先抬起右手，再向前迈一步，最后蹲下”——这要求模型理解指令的时间顺序，并将多轮指令合成为一段连贯的运动。
- **虚拟助手与游戏NPC**：用户与虚拟角色进行对话，角色不仅需要用语言回应，还需要根据对话上下文做出相应的肢体动作，且动作需随对话推进而自然演变。
- **运动分析与编辑**：用户可能先询问“这个动作的加速度峰值在哪里？”，然后基于回答进一步要求“把起跳阶段的滞空时间延长20%”——这要求模型同时具备运动推理能力和运动生成能力，且能在对话历史中保持上下文一致性。

上述场景共同指向一个未被满足的核心需求：**多轮、多模态的对话式运动生成与理解**。现有模型之所以无法胜任，根源在于其架构设计上的两个关键缺口。

### 现有方法的结构性缺口

**缺口一：缺乏统一的多模态表示空间**

传统文本到运动模型将文本编码（如CLIP嵌入）和运动特征视为两个独立空间中的实体，通过跨模态映射（如对比学习或条件注入）建立关联。这种“分离处理”策略使得模型难以将视觉信息（图像、视频）纳入同一推理框架，更无法在统一的词汇表内实现文本、运动、视觉三种模态的联合建模。当用户交替提供图像参考、文本指令和运动示例时，分离式架构缺乏一个共享的“语言”来融合这些异构输入。

**缺口二：无对话历史记忆，无法进行上下文连续生成**

单轮条件生成模型在每次推理时仅接收当前输入，不保留任何历史状态。这意味着：
- 模型无法根据上一轮的问答内容调整当前轮的生成策略；
- 多轮运动指令无法被累积合成为一段时间连贯的长序列——每轮独立解码的运动片段之间必然存在不自然的跳变或停顿；
- 运动推理（如“这个动作属于哪种运动类型？”）与运动生成被视为两个独立任务，无法在同一对话流中交替进行。

尽管近期有工作（如**MotionGPT**）尝试将运动离散化为令牌，并利用语言模型进行统一建模，但其本质上仍面向单轮文本-运动转换，并未构建多轮对话机制，也未将视觉模态纳入统一词汇表。

### 核心洞察与本文动机

本文的核心洞察在于：**如果将人体运动视为一种“外语”，那么就可以借助大规模语言模型（LLM）的序列建模和上下文学习能力，实现多模态、多轮的对话式运动交互。**

这一洞察的技术含义是深远的：

1. **统一词汇表的构建**：通过VQ-VAE将连续运动序列量化为离散的运动令牌（motion tokens），使其与文本令牌（通过SentencePiece分词器获得）和视觉令牌（通过CLIP视觉编码器+投影层获得）共享同一嵌入空间。三种模态的数据由此转化为同一“语言”中的不同“单词”，可以被同一个自回归语言模型统一处理。

2. **对话上下文的自然建模**：语言模型天然具备处理长序列和保持上下文的能力。将多轮对话中的历史问答、当前多模态输入拼接为一个序列，语言模型可以自回归地预测目标令牌——无论是文本回答还是运动序列。这使得运动推理和运动生成可以在同一轮对话中无缝切换。

3. **时间连贯的运动合成**：通过将过去轮次和当前轮次的运动令牌拼接后统一解码（而非逐轮独立解码），可以保证多轮指令生成的运动在时间维度上平滑连贯，消除片段间的跳变。

基于上述洞察，本文提出了**MotionChain**——一个统一的视觉-运动-语言对话式生成框架。MotionChain由多模态分词器（文本、视觉、运动）和视觉-运动感知语言模型两部分构成，通过在大规模多模态对话数据集上进行多轮指令微调，首次实现了根据文本、图像、运动等多模态提示进行连续多轮对话，并在对话中交替生成文本回答和人体运动序列的能力。

## 核心创新

MotionChain的核心创新在于将人体运动视为一种可被语言模型理解的“外语”，从而将多轮多模态交互问题转化为序列建模问题。与传统运动生成方法相比，其关键突破体现在以下四个维度的范式转变上。

### 1. 多模态统一令牌空间

**基线现状**：现有方法（如T2M-GPT、MLD、MotionGPT）对文本、运动、视觉等模态采用分离的特征提取方式——文本通常使用CLIP嵌入，运动使用独立编码器，缺乏统一的词汇体系。这导致不同模态信息无法在同一语义空间内进行联合推理。

**MotionChain方案**：构建了统一的多模态离散词汇空间，将文本令牌、运动码本（$V_m$）和视觉投影令牌（$X_v$）合并到同一嵌入空间中（Fig. 2, Sec. 3.3）。具体而言：
- **运动分词器**：基于VQ-VAE架构，采用残差量化（$Q=4$层，码本大小$K=512 \times 1024$），将连续运动序列编码为离散运动令牌，形成“运动词汇表”
- **视觉分词器**：冻结CLIP视觉编码器，通过可学习的线性投影将图像/视频特征转换为与语言模型对齐的视觉令牌
- **文本分词器**：使用SentencePiece模型进行标准文本令牌化

这种统一词汇设计使得语言模型可以无缝处理多模态输入，为后续的对话式交互奠定了基础。

### 2. 对话式上下文理解与多轮生成

**基线现状**：传统运动生成模型（如T2M-GPT、MLD）仅支持单轮条件生成——给定文本描述，生成对应运动序列。模型缺乏对历史对话的记忆，无法在交互式场景中维持上下文连贯性。

**MotionChain方案**：将运动生成任务重新定义为多轮对话问题（Sec. 3.3）。通过向前拼接所有历史问答及当前源令牌，以自回归方式生成目标令牌：

$$p_{\theta}(X_a \mid X_v, X_s) = \prod_i p_{\theta}\left(x_a^i \mid X_v, X_{s,<i}, X_{a,<i}\right)$$

训练目标为最大化目标令牌的对数似然：

$$\mathcal{L}_{LM} = -\sum_{i=0}^{L_t-1} \log p_{\theta}\left(x_a^i \mid X_v, X_{s,<i}, X_{a,<i}\right)$$

这一设计使得模型能够根据对话历史连续生成运动或文本回复，支持图像条件运动生成、运动推理、运动编辑等多模态交互任务（Fig. 1）。

### 3. 时间连贯的运动合成机制

**基线现状**：在多轮运动生成场景中，若每轮独立解码动作，帧间可能出现不连贯、突变等问题，缺乏对运动序列时间连续性的显式建模。

**MotionChain方案**：提出了令牌拼接（Tokens-joint）运动合成方法（Sec. 3.2, Eq. 3）：

$$z_{\mathrm{whole}}^{1:(L_p+L_c)} = [z_p^{1:L_p}, z_c^{1:L_c}]$$

将过去轮次的运动令牌与当前轮次的运动令牌拼接后，通过VQ解码器一次性解码为连续运动序列。消融实验（Table 3, Fig. 4）表明，Tokens-joint方式在MPJPE等指标上显著优于独立解码（Independent）和基于过去条件的解码（Past-condition），有效保证了多轮生成运动的时间连贯性。

### 4. 视觉输入的统一处理

**基线现状**：大多数运动生成方法不使用视觉输入，或仅简单拼接视觉特征，缺乏将视觉信息与运动生成深度融合的机制。

**MotionChain方案**：设计了专用的视觉分词器（Sec. 3.2），将图像/视频转换为与语言嵌入对齐的视觉令牌，置于源序列前部。消融实验（Table 4）对比了三种架构：
- **Q-former**：基于查询的交叉注意力机制
- **Perceiver**：感知器架构
- **Linear**：简单线性投影

结果显示，简单的线性投影在首帧MPJPE上优于Q-former和Perceiver，表明在运动生成任务中，轻量级的视觉特征对齐策略反而更有效。

### 创新总结

MotionChain的核心贡献在于通过“统一令牌空间 + 语言模型对话能力”的技术路线，将多模态运动生成从单轮条件映射提升为多轮上下文感知的交互式生成。这一范式转变的关键在于：**将运动离散化为语言模型的“词汇”，使得预训练语言模型的序列建模和上下文学习能力可以被直接迁移到运动生成领域**。该方法在运动推理任务上取得了37.92的Bleu@1分数，远超通用LLM基线Vicuna-1.5-7b的19.27（Table 1），验证了统一多模态令牌空间和对话式微调策略的有效性。

## 整体框架

MotionChain 是一个**视觉-运动-语言统一生成式预训练模型**，其核心目标是将人体运动视为一种“外语”，通过构建统一的多模态离散令牌空间，使大规模语言模型能够以对话方式连续生成运动或文本回复。该框架由两大核心组件构成：**多模态分词器**（Multi-modal Tokenizer）与**视觉-运动感知语言模型**（Vision-Motion-aware Language Model），整体架构如 Fig. 2 所示。

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/002_Figure_2.jpg]]
*Figure 2: Method overview: MotionChain consists of a motion tokenizer VM ( Sec. 3.2), a vision tokenize VI (r Sec. 3.2) and a vision-motion-aware language model (Sec. 3.3). By leveraging motion tokens generated by*

### 输入输出流与模块关系

MotionChain 的 pipeline 遵循“多模态编码 → 统一令牌拼接 → 自回归生成 → 条件解码”的端到端流程：

1. **多模态输入编码**：系统接收三类输入——文本指令、图像/视频、人体运动序列。三类输入分别由三个分支的分词器处理：
   - **文本分词器**：采用 SentencePiece 模型，将自然语言指令转化为文本令牌。
   - **运动分词器** $\mathcal{V}_{\mathcal{M}}$：基于 VQ-VAE 架构，将原始运动序列编码为离散运动令牌，并可通过解码器从令牌重建连续运动。
   - **视觉分词器** $\mathcal{V}_{\mathcal{I}}$：使用冻结的 CLIP 视觉编码器提取图像/视频特征，经可学习的线性投影（或感知器）转化为与语言模型嵌入空间对齐的视觉令牌 $X_v$。

2. **统一词汇空间**：文本词汇表 $\mathcal{V}_t$ 与运动词汇表 $\mathcal{V}_m$ 被合并为一个统一的词汇表 $\mathcal{V}$，运动码本 $\mathcal{Z}$ 的条目顺序被保留，并加入特殊边界令牌以区分模态。视觉令牌嵌入 $X_v$ 则通过投影直接对齐到该共享嵌入空间。

3. **上下文拼接与自回归生成**：在多轮对话场景中，所有历史问答对及当前轮的源令牌（文本、视觉令牌、运动令牌）被向前拼接，形成完整的上下文序列。视觉-运动感知语言模型（以 Flan-T5 为基座）以自回归方式根据该上下文预测目标答案令牌 $X_a$，其条件概率分解为：
   $$p_{\theta}(X_a \mid X_v, X_s) = \prod_i p_{\theta}\left(x_a^i \mid X_v, X_{s,<i}, X_{a,<i}\right)$$
   训练损失为标准的负对数似然：
   $$\mathcal{L}_{LM} = -\sum_{i=0}^{L_t-1} \log p_{\theta}\left(x_a^i \mid X_v, X_{s,<i}, X_{a,<i}\right)$$

4. **运动合成与解码**：当目标答案为运动令牌时，采用**令牌拼接**（Tokens-joint）策略——将过去轮次的运动令牌 $z_p$ 与当前轮次生成的运动令牌 $z_c$ 沿时间维度拼接为 $z_{\text{whole}}^{1:(L_p+L_c)} = [z_p^{1:L_p}, z_c^{1:L_c}]$，再通过运动分词器的解码器 $\mathcal{D}_{\mathcal{M}}$ 一次性解码为连续运动序列，以保证多轮生成运动的时间连贯性。

### 关键设计决策

- **运动分词器**：运动序列经编码器 $\mathcal{E}_{\mathcal{M}}$ 和时间下采样（下采样率 $l$）后，运动帧数 $M$ 被压缩为 $L = M/l$ 个令牌。量化过程通过残差 VQ 实现，将每个隐向量替换为码本 $\mathcal{Z}$ 中最近邻条目：$z_i = Q(\hat{z}^i) := \arg \min_{z_k \in \mathcal{Z}} \|\hat{z}_i - z_k\|_2$。训练损失 $\mathcal{L}_{\mathcal{V}} = \mathcal{L}_r + \mathcal{L}_e + \mathcal{L}_c$ 由重建损失、嵌入损失和承诺损失组成。

- **视觉分词器架构选择**：消融实验（Table 4）表明，简单的线性投影（Linear）在首帧 MPJPE 指标上优于 Q-former 和 Perceiver，因此被采纳为默认方案。

- **多轮对话机制**：与现有单轮条件生成方法（如 T2M-GPT、MLD、MotionGPT）的根本区别在于，MotionChain 通过向前拼接全部对话历史来保持上下文记忆，而非每轮独立处理。

### 数据流与训练范式

MotionChain 的训练分为两个阶段：首先在统一的运动-语言数据上进行多任务预训练，随后使用专门构建的**多模态多轮对话数据集**进行指令微调。该对话数据集通过 ChatGPT 和文本-运动检索模型 TMR 从现有文本-运动配对数据（如 HumanML3D）中增强生成，涵盖运动推理、运动编辑等 14 类任务，数据收集流程见 Fig. 3。

### 补充图表

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/027_Table_10.jpg]]
*Table 10: Architecture of our vision perceiver*

## 核心模块与公式推导

MotionChain 的核心架构由三个相互协作的模块构成：运动分词器、视觉分词器，以及视觉-运动感知语言模型。其设计哲学是将人体运动视为一种“外语”，通过离散令牌统一文本、视觉和运动三种模态，从而将大语言模型的序列建模与对话能力迁移到多模态运动生成任务中。

### 运动分词器（Motion Tokenizer）

运动分词器 $\mathcal{V}_{\mathcal{M}}$ 基于 VQ-VAE 架构，由运动编码器 $\mathcal{E}_{\mathcal{M}}$ 和运动解码器 $\mathcal{D}_{\mathcal{M}}$ 组成。其功能是将原始运动序列压缩为离散令牌序列，并能从令牌中重建连续运动。

**压缩与离散化流程**：给定一段包含 $M$ 帧的人体运动序列，编码器通过时间下采样将其压缩为 $L = M / l$ 个隐向量，其中 $l$ 为下采样率。随后，每个隐向量 $\hat{z}_i$ 通过查找最近邻的方式被量化为码本 $\mathcal{Z}$ 中的离散条目：

$$z_i = Q(\hat{z}^i) := \arg \min_{z_k \in \mathcal{Z}} \|\hat{z}_i - z_k\|_2$$

这一量化过程将连续运动转化为离散的“运动词汇”序列，使其能够与文本令牌在同一嵌入空间中统一表示。

**训练目标**：运动分词器的训练总损失由三项组成：

$$\mathcal{L}_{\mathcal{V}} = \mathcal{L}_r + \mathcal{L}_e + \mathcal{L}_c$$

其中 $\mathcal{L}_r$ 为运动重建损失，$\mathcal{L}_e$ 为嵌入损失，$\mathcal{L}_c$ 为承诺损失。消融实验表明，采用 $Q=4$ 层残差量化、码本大小 $K=512$、码本维度 $d=1024$ 的参数设置可获得最佳的 FID 重建质量（Table 9）。

**运动合成机制**：在多轮对话的运动生成场景中，MotionChain 采用令牌拼接（Tokens-joint）方式融合历史运动与当前运动。具体而言，将过去 $L_p$ 个运动令牌 $z_p$ 与当前轮次生成的 $L_c$ 个运动令牌 $z_c$ 沿时间维度拼接：

$$z_{\mathrm{whole}}^{1:(L_p+L_c)} = [z_p^{1:L_p}, z_c^{1:L_c}]$$

拼接后的完整令牌序列通过运动解码器一次性解码为连续运动序列，从而保证多轮生成运动的时间连贯性。消融实验（Table 3, Fig. 4）证实，Tokens-joint 方式在 MPJPE 等指标上显著优于独立解码（Independent）和基于过去条件的分离解码（Past-condition）。

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/004_Figure_4.jpg]]
*Figure 4: Motion Composition Variants: We illustrate the baselines for motion composition during multi-turn motion generation (a). independent decoding each turn (b). separate decoding conditioned on the last few tokens from the prior turn (c). decoding with joint motion tokens. Green tokens stand for image condition, blue tokens stand for textual instruction, and orange tokens stand for human motions*

### 视觉分词器（Vision Tokenizer）

视觉分词器负责将图像或视频输入转换为与语言模型嵌入空间对齐的视觉令牌嵌入 $X_v$。其结构采用冻结的 CLIP 视觉编码器提取视觉特征，随后通过一个可学习的投影模块将特征映射到语言模型的令牌空间。

架构消融实验（Table 4）对比了三种投影结构：Q-former、Perceiver 和简单的线性投影（Linear）。结果表明，线性投影在首帧 MPJPE 指标上表现最优，且实现最为简洁，因此被采纳为默认方案。

### 视觉-运动感知语言模型

该模块以 Flan-T5 为基座，采用统一的文本-运动词汇表 $\mathcal{V}$。词汇表由文本词汇 $\mathcal{V}_t$ 和运动词汇 $\mathcal{V}_m$ 合并而成，并引入特殊边界令牌以区分不同模态的令牌片段。

**自回归生成**：给定视觉令牌 $X_v$ 和源令牌序列 $X_s$（包含对话历史中的文本指令、运动令牌等），模型以自回归方式生成目标答案令牌 $X_a$（可以是文本回复或运动序列）。其条件概率分解为：

$$p_{\theta}(X_a \mid X_v, X_s) = \prod_i p_{\theta}\left(x_a^i \mid X_v, X_{s,<i}, X_{a,<i}\right)$$

**训练损失**：语言模型的训练目标是最小化目标令牌的负对数似然：

$$\mathcal{L}_{LM} = -\sum_{i=0}^{L_t-1} \log p_{\theta}\left(x_a^i \mid X_v, X_{s,<i}, X_{a,<i}\right)$$

通过这一统一的序列建模框架，MotionChain 能够同时处理文本生成和运动生成任务，并在多轮对话中保持对历史上下文的感知——每轮推理时，所有历史问答及当前源令牌被向前拼接，作为自回归生成的条件。

### 关键设计选择总结

| 模块 | 关键设计 | 消融验证锚点 |
|------|----------|-------------|
| 运动分词器 | VQ-VAE + 残差量化 ($Q=4$, $K=512$, $d=1024$) | Table 9 |
| 运动合成 | Tokens-joint 拼接 > Independent / Past-condition | Table 3, Fig. 4 |
| 视觉分词器 | CLIP 编码器 + 线性投影 > Q-former / Perceiver | Table 4 |
| 语言模型 | 统一词汇 + 自回归生成 + 多轮历史拼接 | Sec. 3.3, Eq. (4)(5) |
| 令牌共享 | 独立运动令牌（每层独立代码）优于跨层共享 | Table 8 |

## 实验与分析

### 4.1 实验设置

MotionChain采用两阶段训练范式。第一阶段为**运动分词器预训练**：在HumanML3D数据集上训练VQ-VAE运动分词器，码本设置为 $K \in \mathbb{R}^{512 \times 1024}$，量化层数 $Q=4$，该配置在FID重建质量上达到最优（Table 9）。第二阶段为**视觉-运动感知语言模型的多轮指令微调**：基于Flan-T5基座，使用统一的多模态词汇（合并文本词汇 $V_t$ 与运动词汇 $V_m$，维持运动分词器码本顺序，并加入特殊边界令牌），在多模态、多任务、多轮对话数据集上进行微调。该对话数据集通过对现有text-to-motion和人体网格重建数据集进行增强构建，包含运动推理、运动编辑等14类任务。模型参数量为280M。

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/013_Table_9.jpg]]
*Table 9: Evaluation of our motion tokenizer on the motion part of HumanML3D [24] dataset. We follow MLD [103] to evaluate our VQ-VAE model V: MPJPE and PAMPJPE are measured in millimeter. ACCL indicates acceleration error. We evaluate FID and Diversity the same as Tab. 3. The baselines of VPoser-t [65] and ACTOR [68] are borrowed from MLD. K indicates the codebook size, d indicates the codebook dimension , Q indicates the Residual-VQ layers*

### 4.2 运动推理性能

运动推理任务是MotionChain的核心创新场景之一，要求模型根据对话历史中的运动数据回答相关问题。Table 1展示了MotionChain与通用LLM在运动推理测试集上的对比结果。

**核心发现**：MotionChain在所有语言学指标上均大幅超越通用LLM基线。具体而言，MotionChain的Bleu@1达到**37.92**，而最佳基线Vicuna-1.5-7b仅为19.27，提升幅度高达**+18.65**（相对提升约96.7%）。在Bleu@4（19.19）、Rouge（38.05）、Cider（24.53）、BertScore（32.24）等指标上同样保持绝对领先。

**关键分析**：
- **领域微调的决定性作用**：Table 1中所有基线模型（Flan-t5-base/large/xl、Llama-2-7b、Vicuna-1.5-7b/13b）均仅使用预训练权重而未在运动领域微调，其Bleu@1普遍低于20，平均回答长度（Length_avg）也明显偏短。这表明通用LLM缺乏对运动令牌语义的理解能力，无法有效进行运动推理。
- **公平性需注意**：基线模型未针对运动推理任务进行微调，这种对比存在一定的不公平性。但这也恰恰印证了论文的核心主张——**将运动视为"外语"并通过统一词汇进行指令微调是赋予LLM运动理解能力的关键路径**。
- **定性验证**：Figure 7的定性对比进一步佐证，MotionChain的回答不仅更准确，而且具有上下文感知能力，能够基于对话历史给出连贯的推理结果。

### 4.3 时间运动合成性能

时间运动合成任务要求模型根据多轮指令生成时间上连贯的长运动序列。Table 2展示了在BABEL数据集上与TEACH方法的对比。

**核心发现**：MotionChain在PA-MPJPE指标上达到**53.72**，显著优于TEACH的61.07（降低**-7.35**，约12%的相对改善）。在MPJPE、FID等指标上同样表现出竞争力。

**关键分析**：
- **令牌拼接策略的优势**：MotionChain的Tokens-joint运动合成方式（将过去与当前运动令牌拼接后统一解码）是保证时间连贯性的核心机制。Table 3的消融实验在HumanML3D上系统对比了三种运动合成变体：
  - **Independent**（每轮独立解码）：帧间完全不连贯，MPJPE最高。
  - **Past-condition**（基于过去若干帧条件解码）：部分改善连贯性，但仍存在衔接不自然。
  - **Tokens-joint**（拼接过去与当前令牌后统一解码）：在所有指标上最优，运动最连贯。
  
  Figure 4通过示意图直观展示了这三种变体的差异，Tokens-joint方式通过 $z_{\mathrm{whole}}^{1:(L_p+L_c)} = [z_p^{1:L_p}, z_c^{1:L_c}]$ 的拼接操作（Eq. 3），使得VQ解码器能够一次性生成无间隔的连续运动序列。

### 4.4 文本到运动生成与运动描述

虽然MotionChain的核心创新在于多轮对话，但其在传统text-to-motion和motion captioning任务上也达到了有竞争力的性能。

**文本到运动生成**（Table 5）：在HumanML3D数据集上，MotionChain在FID、Diversity、R-Precision等指标上与T2M-GPT、MLD、MotionGPT等专用方法可比。值得注意的是，MotionChain在"Pre-trained"（统一预训练但未针对该任务微调）和"Fine-tuned"（针对该任务微调）两种设置下均表现出色，证明了统一多模态词汇的有效性。

**运动描述生成**（Table 6）：MotionChain在Bleu@4（12.46）、Rouge（38.80）、Cider（60.82）、BertScore（33.15）等指标上取得了有竞争力的结果，展示了其双向运动-语言理解能力。

### 4.5 视觉分词器架构消融

视觉分词器是MotionChain实现图像/视频条件运动生成的关键模块。Table 4在Bedlam数据集上对比了三种视觉分词器架构：

**核心发现**：简单的**线性投影（Linear）**在首帧MPJPE上优于Q-former和Perceiver。这表明在将CLIP视觉特征对齐到语言模型空间时，过复杂的感知器结构可能引入不必要的归纳偏置，反而损害了运动重建精度。

**实现细节**：视觉分词器采用冻结的CLIP视觉编码器提取特征，再通过可学习的线性投影层将特征转换为与语言模型嵌入空间对齐的视觉令牌 $X_v$，置于源序列前部。

### 4.6 运动分词器参数消融

Table 9系统消融了VQ-VAE运动分词器的关键参数：

**核心发现**：
- **码本大小与维度**：$K=512, d=1024$ 的设置在FID（0.479）和MPJPE（44.1）上达到最佳平衡。过小的码本（256）导致表达能力不足，过大的码本（1024）则可能引入训练不稳定。
- **量化层数**：$Q=4$ 层残差量化优于 $Q=2$ 和 $Q=8$，在重建质量与训练难度间取得最优折衷。
- **令牌共享策略**（Table 8）：独立运动令牌（每残差量化层使用独立代码）在文本到运动FID上优于跨层共享令牌，说明多层独立量化能更精细地表征运动细节。

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/012_Table_8.jpg]]
*Table 8: Comparison of text-to-motion on HumanML3D [24]. The empty MModality indicates Real motion is deterministic. Pre-trained and Fine-tuned indicate uniform motion-language pretraining and specific fine-tuning on this task. The arrows (→) indicate that closer to Real is desirable. Bold and underline indicate the best and the second best result on text-to-motion task*

### 4.7 推理速度

Table 11展示了不同模型规模下的推理速度（FPS）。在单张Tesla V100上，较小模型规模可获得更快的FPS，为实际部署提供了参考。

### 4.8 失败模式与局限性

尽管MotionChain在多模态运动对话任务上取得了显著进展，仍存在以下局限：

1. **人体表征范围受限**：当前模型仅支持关节人体运动，无法处理面部表情、手部精细动作以及人与物体/场景的交互运动。这限制了其在更广泛具身智能场景中的应用。
2. **数据稀缺瓶颈**：运动推理和对话数据的构建依赖于现有的文本-运动配对数据集，其规模远小于图像-语言数据集。如何在数据受限条件下进一步提升运动推理质量是一个开放问题。
3. **多模态冲突处理未量化**：当面临模糊或矛盾的多模态提示（如文本指令与图像条件不一致）时，MotionChain的响应行为缺乏系统性的量化评估，目前仅依赖定性示例。
4. **运动推理评估指标单一**：当前运动推理任务主要采用NLP领域的语言学指标（Bleu、Rouge等），缺乏针对运动语义理解正确性的专用量化指标。

### 4.9 关键图表结论汇总

| 图表 | 核心结论 | 置信度 |
|------|----------|--------|
| Table 1 | MotionChain在运动推理上Bleu@1达37.92，远超通用LLM基线（最佳19.27），证明统一词汇+指令微调赋予LLM运动理解能力 | 高 |
| Table 2 | Tokens-joint运动合成在PA-MPJPE上优于TEACH（53.72 vs 61.07），验证拼接解码策略的时间连贯性优势 | 高 |
| Table 3 | Tokens-joint在所有指标上优于Independent和Past-condition，消融确认拼接策略的必要性 | 高 |
| Table 4 | 线性投影视觉分词器优于Q-former和Perceiver，简单对齐策略更有效 | 高 |
| Table 9 | $Q=4, K=512, d=1024$ 为运动分词器最优参数配置 | 高 |
| Fig. 4 | 直观展示三种运动合成变体的机制差异，Tokens-joint实现无缝连续运动 | 高 |

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/005_Table_1.jpg]]
*Table 1: Comparison of motion reasoning on the test set of our conversation dataset. Our proposed MotionChain is fine-tuned on motion reasoning tasks while other methods’ results are generated by their pre-trained weight*

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/006_Table_2.jpg]]
*Table 2: Comparison of temporal motion composition on Babel [73]. We evaluate the state-of-theart motion temporal composition method Teach [4] under the 95 % confidence interval from 20 times running. (cf. Sec. 4.1 for notations.)*

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/007_Table_3.jpg]]
*Table 3: Evaluation of motion composition methods on HumanML3D [24]. Here Independent, Past-condition, and Tokens-joint stand for different motion composition varients during multi-turn motion conversation, as illustrated in Fig. 4*

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/008_Table_4.jpg]]
*Table 4: Evaluation of vision tokenizer architecture on Bedlam [50]. We implement three different architectures, including Q-former, Perceiver, and Linear. We evaluate these results with the metrics in motion reconstruction. Additional information regarding the implementation is in the supplementary materials. (cf. Tab. 2 for notations.)*

### 补充图表

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/009_Table_5.jpg]]
*Table 5: Comparison of text-to-motion on HumanML3D [24]. The empty MModality indicates Real motion is deterministic. Pre-trained and Fine-tuned indicate uniform motion-language pretraining and specific fine-tuning on this task. The arrows (→) indicate that closer to Real is desirable. Bold and underline indicate the best and the second best result on text-to-motion task*

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/010_Table_6.jpg]]
*Table 6: Comparison of motion captioning on HumanML3D [24]. The evaluation metrics follow [25], while we use the ground truth texts without pre-processing for linguistic metrics calculation. Bold indicate the best*

![[assets/figures/papers/paper_list_l1877_MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts/figures/028_Table_11.jpg]]
*Table 11: The inference time costs of text-driven motion generation by evaluating the Frames Per Second (FPS), which is obtained by averaging the number of frames generated per second. We present the time costs for various model sizes and observe that, under the same 1 Tesla V100, smaller model sizes achieve faster FPS*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

MotionChain 的核心定位在于将**多模态统一词汇**与**预训练语言模型的上下文学习能力**相结合，以解决现有运动生成模型仅支持单轮条件生成的瓶颈。其方法谱系可从以下几个维度进行梳理：

#### 1.1 与统一运动-语言模型的对比

MotionChain 直接继承并扩展了 **MotionGPT** (Jiang et al., 2023) 的统一运动-语言学习范式。两者均采用 VQ-VAE 将人体运动转化为离散令牌，并与文本令牌共享嵌入空间，从而利用语言模型进行序列建模。然而，MotionChain 在以下关键维度上实现了突破：

- **多模态输入扩展**：MotionGPT 仅处理文本-运动双模态，而 MotionChain 引入了**视觉分词器**（冻结 CLIP 编码器 + 可学习线性投影），将图像/视频转化为视觉令牌 $X_v$，使模型能够基于图像条件生成运动（Table 4, Fig. 1 第一列）。这一扩展使 MotionChain 从双模态框架升级为**视觉-运动-语言三模态统一框架**。
- **对话能力引入**：MotionGPT 本质上仍是单轮条件生成模型（给定文本，生成运动），缺乏对多轮对话历史的理解。MotionChain 通过构造多轮对话数据集（Fig. 3）并进行指令微调（Sec. 3.4），使模型能够根据所有历史问答及当前源令牌，自回归生成目标令牌，真正实现了**对话式运动控制**。这是从“翻译式生成”到“交互式生成”的范式转变。
- **运动合成机制**：在连续运动生成场景中，MotionChain 提出了**令牌拼接（Tokens-joint）**策略（Eq. 3: $z_{\mathrm{whole}}^{1:(L_p+L_c)} = [z_p^{1:L_p}, z_c^{1:L_c}]$），将过去与当前的运动令牌联合输入 VQ 解码器，一次性解码为连续运动序列。消融实验（Table 3）表明，该方法在时间连贯性上显著优于独立解码（Independent）和基于过去条件的解码（Past-condition），这是对 MotionGPT 等单轮模型在时序组合能力上的重要补充。

#### 1.2 与文本到运动基线的对比

在标准文本到运动生成任务上，MotionChain 与以下代表性基线进行了对比（Table 5）：
- **T2M-GPT** (Zhang et al., 2023)：基于 GPT 架构的自回归运动生成模型。
- **MLD** (Chen et al., 2023)：基于扩散模型的运动生成方法。
- **MotionGPT**：统一运动-语言模型。

MotionChain 在这些任务上取得了有竞争力的结果，但其核心优势并不在于单轮文本到运动生成的绝对指标，而在于**多轮对话上下文理解和连续运动生成能力**——这是上述基线完全不具备的功能。

#### 1.3 与通用大语言模型的对比

在运动推理任务上（Table 1），MotionChain 与多个通用 LLM 进行了对比：
- **Flan-T5** 系列（base/large/xl, Chung et al., 2022）
- **Llama-2-7b** (Touvron et al., 2023)
- **Vicuna-1.5** 系列（7b/13b, Zheng et al., 2023）

MotionChain 以 Bleu@1 达 37.92 的成绩显著超越最佳基线 Vicuna-1.5-7b（19.27），提升幅度达 +18.65（约 97%）。这一巨大差距的核心原因在于：通用 LLM 虽然具备强大的语言理解能力，但其预训练权重**未接触运动领域知识**，无法理解运动令牌的语义。MotionChain 通过统一词汇和多轮指令微调，使语言模型真正“学会”了运动语言。

> **公平性说明**：上述通用 LLM 基线仅使用预训练权重进行推理，未针对运动领域进行微调。这在一定程度上影响了对比的公平性，但同时也恰恰证明了 MotionChain 的核心贡献——通过统一词汇和领域微调，赋予语言模型运动理解能力。

#### 1.4 与时间运动合成基线的对比

在时间运动合成任务上（Table 2），MotionChain 与 **TEACH** (Athanasiou et al., 2023) 进行了对比。TEACH 是专门针对时间运动组合任务设计的方法，而 MotionChain 在 PA-MPJPE 上达到 53.72，优于 TEACH 的 61.07（降低 7.35，约 12%）。这表明 MotionChain 的令牌拼接策略即使与专用方法相比也具有优势。

### 2. 适用边界与局限

#### 2.1 适用场景

MotionChain 在以下场景中展现出显著优势：
- **多轮对话式运动生成与编辑**：用户可以通过多轮自然语言交互，逐步细化运动生成需求，模型能够保持上下文连贯性。
- **多模态条件运动生成**：支持文本、图像、运动序列的任意组合作为输入条件。
- **运动推理与问答**：模型能够回答关于运动物理特性、运动分析等领域问题。
- **连续长运动合成**：通过令牌拼接策略，生成时间连贯的长运动序列。

#### 2.2 已知局限

论文明确指出的局限包括：
- **仅支持关节人体**：当前版本无法处理面部表情、手部精细动作、人与物体/场景的交互。这限制了模型在全身交互场景（如抓取物体、操作工具）中的应用。
- **数据依赖性**：模型的运动推理能力高度依赖文本-运动配对数据集的质量和规模。相较于图像-语言数据集的丰富性，运动-文本配对数据相对稀缺，这可能导致模型在长尾运动类型上的泛化能力不足。

#### 2.3 潜在风险与边界

基于方法设计的分析，以下边界值得注意：
- **模糊/矛盾提示处理**：当面临模糊或矛盾的多模态提示时（例如文本描述与图像内容不一致），模型的行为尚未被量化评估。仅依赖定性示例（Fig. 5）不足以证明其鲁棒性。
- **运动推理的深层语义理解**：当前运动推理任务的评估主要依赖语言学指标（Bleu, Rouge, Cider, BertScore），这些指标可能无法完全反映模型对运动物理规律的真实理解深度。
- **视觉条件的精度**：视觉分词器采用简单的线性投影（Table 4），虽然在首帧 MPJPE 上优于 Q-former 和 Perceiver，但其对复杂场景中人体姿态的细粒度感知能力可能存在上限。

### 3. 开放问题与未来方向

基于论文的分析和已知局限，以下开放问题值得后续工作关注：

1. **数据扩展与泛化**：如何有效缓解文本-运动配对数据集的稀缺问题？可能的路径包括利用大规模图像-语言数据辅助训练、合成数据增强、或跨模态迁移学习。

2. **交互范围扩展**：如何将模型扩展到处理面部表情、手部动作以及人与物体的交互？这需要重新设计运动表示格式（当前基于 HumanML3D 的 263 维特征或 SMPL 参数）和分词器架构。

3. **鲁棒性评估**：当面临模糊或矛盾的多模态提示时，MotionChain 如何做出响应？需要建立专门的对抗性测试集和量化评估协议。

4. **推理质量量化**：除了现有的语言学指标和定性示例，是否有更直接量化运动推理质量的方法？例如，基于物理模拟的合理性验证、或与运动捕捉数据的对比分析。

5. **推理效率优化**：Table 11 显示了不同模型参数下的推理 FPS，但是否有特定的工程优化（如模型量化、令牌缓存、投机解码）可以进一步提升推理速度，以满足实时交互场景的需求？

6. **感知器架构的深入探索**：Table 4 显示简单线性投影优于 Q-former 和 Perceiver，但这是否是任务特定的现象？在更复杂的视觉条件运动生成任务中，更强大的感知器架构是否会展现出优势？

## 原文 PDF

![[paperPDFs/ECCV_2024/MotionChain_Conversational_Motion_Controllers_via_Multimodal_Prompts.pdf]]
