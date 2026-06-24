---
title: "Motion-Agent: A Conversational Framework for Human Motion Generation with LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with_LLMs.pdf
aliases:
- Motion-Agent
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将连续运动序列离散化为LLM可理解的token，并通过轻量LoRA微调预训练LLM实现双向文本-运动翻译，再利用GPT-4等对话LLM进行无训练的协调和控制，是解锁高效、灵活、多任务运动生成与理解的关键。
primary_logic: 通过将运动视为一种语言（token序列），可以直接利用预训练语言模型的强大泛化和对话能力，无需额外对话数据集或指令微调，即可构建统一的对话式运动生成、编辑与推理框架。
claims:
- 仅微调1-3%的参数（使用LoRA），MotionLLM在文本-运动生成上达到与全参数训练模型竞争的性能，在运动captioning上大幅超越前SOTA。
- Motion-Agent通过GPT-4协调，无需额外训练即可支持多轮对话，实现复杂的运动生成、编辑、理解与推理（如图1、3、5所示）。
- 自回归生成模式让MotionLLM无需指定目标长度，避免了非自回归模型因长度估计错误导致的严重漂移问题。
- HumanML3D 上 R Precision Top1 (generation) = 0.515±.004
---

# Motion-Agent: A Conversational Framework for Human Motion Generation with LLMs

> [!tip] 核心洞察
> 通过将运动视为一种语言（token序列），可以直接利用预训练语言模型的强大泛化和对话能力，无需额外对话数据集或指令微调，即可构建统一的对话式运动生成、编辑与推理框架。

| 字段 | 内容 |
|------|------|
| 中文题名 | Motion-Agent：基于大语言模型的对话式人体运动生成框架 |
| 英文题名 | Motion-Agent: A Conversational Framework for Human Motion Generation with LLMs |
| 会议/期刊 | ICLR 2025 |
| Links | [Project](https://knoxzhao.github.io/Motion-Agent) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Motion-Agent |
| Dataset | HumanML3D |

> [!tip] 效果简介
> - HumanML3D 上，R Precision Top1 (generation) 0.515±.004 vs MotionGPT 0.492±.003 (+0.023)；FID (generation, lower better) 0.230±.009 vs MotionGPT 0.232±.008 (-0.002 (略微降低))；Bert Score (captioning) 42.63 vs MotionChain 36.9 (先前最佳) (+5.73)。

## 概述

**Motion-Agent** 是一个旨在解决3D人体运动生成领域两个核心瓶颈的对话式框架：**通用性不足**与**交互能力缺失**。现有方法通常需要大量任务特定训练，难以处理长序列、复杂组合提示及多轮编辑。Motion-Agent的因果机制在于将连续运动序列离散化为语言模型可理解的token，并通过轻量级LoRA适配器微调预训练LLM，实现文本与运动之间的双向翻译。在此基础上，利用GPT-4等对话LLM作为无训练的协调器，驱动翻译代理完成生成、编辑、理解与推理，从而解锁高效、灵活的多任务运动生成能力。

**核心结论**：仅微调1–3%的模型参数，MotionLLM在文本到运动生成上即可达到与全参数训练模型竞争的性能（HumanML3D数据集上R Precision Top1达0.515，FID为0.230），在运动描述生成（captioning）上更以Bert Score 42.63大幅超越此前最佳结果（+5.73）。Motion-Agent通过GPT-4协调，无需额外训练即可支持多轮对话，实现复杂运动序列的生成、过渡组合和编辑（图1、3、5）。其自回归生成模式天然支持可变长度输出，避免了非自回归模型因长度估计错误导致的严重漂移问题。

**方法定位**：Motion-Agent将运动视为一种语言，直接继承预训练语言模型的泛化与对话能力，构建了统一的对话式运动生成、编辑与推理框架。与需要指令微调才能支持多轮交互的方法（如MotionChain, Jiang et al., 2024c）不同，Motion-Agent无需额外对话数据集。框架由三个组件构成：GPT-4作为对话协调器，MotionLLM作为文本-运动双向翻译代理，以及运动分词器/解分词器负责连续运动与离散token之间的转换。

**主要结果**：在HumanML3D基准上，MotionLLM在生成质量和文本对齐方面达到或超越现有方法，同时在captioning任务上建立了新的最优水平。定性分析表明，Motion-Agent能准确生成包含系列动作的复杂运动，而其他模型在类似复杂描述下输出短而模糊的动作。消融实验证实，精心设计的翻译代理对框架性能至关重要——替换为MotionGPT后运动过渡不平滑；较小的开源LLM（如Llama-3-7B）作为协调器时无法可靠遵循JSON格式，影响可用性。

## 背景与动机

### 问题背景：3D人体运动生成的现状与瓶颈

3D人体运动生成旨在根据自然语言描述合成逼真的动作序列，在动画制作、虚拟现实和人机交互等领域具有重要应用价值。近年来，该领域涌现了大量方法，包括基于扩散模型的 **MDM**（Tevet et al., 2023）、**MLD**（Chen et al., 2023b）和 **MotionDiffuse**（Zhang et al., 2022），以及基于自回归Transformer的 **T2M-GPT**（Zhang et al., 2023b）和非自回归的 **MoMask**（Guo et al., 2024）等。这些方法在标准基准上取得了显著进展，但其核心瓶颈在于：**需要大量任务特定的训练，缺乏通用性和对话交互能力**。

具体而言，现有方法面临以下结构性缺口：

1. **任务隔离与训练冗余**：大多数模型针对单一任务（如文本到运动生成）从头训练，无法复用预训练知识。即使是支持双向翻译的 **MotionGPT**（Jiang et al., 2024b），仍需为每个任务进行专门的模型训练或微调，缺乏统一的框架来同时处理运动生成、理解和编辑。

2. **交互能力的缺失**：传统模型仅支持单轮指令输入，无法进行多轮对话。用户无法通过迭代反馈逐步细化运动细节，也无法要求模型对已生成的运动进行编辑或续写。**MotionChain**（Jiang et al., 2024c）虽然尝试引入多轮能力，但需要额外的指令微调数据，增加了训练成本和数据依赖。

3. **复杂长序列处理的困难**：当面对包含多个连续动作的复杂描述时，现有方法往往生成短促、模糊的运动。非自回归模型需要手动指定目标长度或依赖长度估计器，而估计器的错误预测会导致严重的运动漂移（如 **Figure 10** 所示）。

### 核心动机：将运动视为语言

上述瓶颈的根本原因在于，现有方法将运动生成视为一个独立的连续信号建模问题，割裂了运动与自然语言之间的深层语义联系。本文的核心洞察是：**通过将运动视为一种语言（token序列），可以直接利用预训练语言模型的强大泛化和对话能力，无需额外对话数据集或指令微调，即可构建统一的对话式运动生成、编辑与推理框架。**

这一动机基于两个关键观察：

- **运动的可离散化**：人体运动本质上是一系列姿态的时间序列，可以通过VQ-VAE编码为离散token，这些token与自然语言token在形式上具有同构性，使得统一建模成为可能。
- **预训练LLM的泛化潜力**：现代大语言模型（LLM）在海量文本上预训练，已具备强大的语义理解、推理和对话能力。如果运动token能与LLM的词汇空间对齐，则仅需极轻量的参数微调（如LoRA，仅1-3%参数），即可让LLM“学会”运动语言，从而将文本领域的泛化能力迁移到运动生成任务上。

基于此动机，**Motion-Agent** 框架应运而生。它通过三个组件——对话协调器（GPT-4）、运动翻译代理（MotionLLM）和运动分词器/解分词器——实现了无需额外训练的对话式运动生成、编辑、理解和推理，从根本上突破了传统方法的任务隔离和交互限制。

## 核心创新

Motion-Agent 的核心创新在于将“运动视为语言”，通过离散化运动表示与轻量级大语言模型适配，构建了一个无需额外对话训练的统一框架，实现了从单次生成到多轮对话式交互的跨越。

### 1. 运动即语言：离散表示与LLM词汇对齐

传统方法（如 **MDM** (Tevet et al., 2023)、**MLD** (Chen et al., 2023b)）在连续特征空间中操作运动，而 **T2M-GPT** (Zhang et al., 2023b) 等虽使用离散 token，但其 token 空间与自然语言割裂。Motion-Agent 的关键改变在于，通过 VQ-VAE 将连续运动序列编码为离散 token，并直接将这些 token 的索引映射为 LLM 可理解的“运动词汇” $\mathbf{V}_m$（见 Section 3.3）。这使得预训练 LLM 无需从头学习运动表示，只需通过 LoRA 适配器微调 1-3% 的参数，即可在文本与运动 token 序列之间执行双向翻译。这一设计直接利用了 LLM 预训练中积累的语义理解与序列建模能力，是框架能够以极低成本实现多任务泛化的因果枢纽。

### 2. 无训练的对话协调：GPT-4 作为计划生成器

现有支持多轮运动编辑的方法（如 **MotionChain** (Jiang et al., 2024c)）需要额外的指令微调数据。Motion-Agent 完全绕过了这一需求：它引入 GPT-4 作为对话协调器，其唯一职责是将用户的自然语言指令解析为结构化的 JSON 任务计划（Section 3.1）。该计划决定了何时调用翻译代理 MotionLLM、调用次数以及每次调用的参数。GPT-4 本身不参与运动生成，仅负责高层规划，而 MotionLLM 作为无状态的翻译工具被多次调用。这种“规划-执行”解耦使得框架无需任何多轮对话训练数据即可支持复杂的连续交互（如图 1、3、5 所示），包括理解、生成、编辑和推理。

### 3. 自回归长度控制：摆脱非自回归的长度依赖

非自回归方法（如 **MoMask** (Guo et al., 2024)）在推理时需要显式指定或估计目标运动长度，而长度估计器的失效会导致严重的运动漂移（见 Figure 10）。Motion-Agent 中的 MotionLLM 采用自回归生成模式，持续预测 token 直到输出终止符 `</Motion>`，天然支持可变长度运动生成。这一设计消除了对真实运动长度的依赖，在无长度先验的场景下具有更强的鲁棒性，这也是其在复杂长序列生成中表现更稳定的关键机制。

### 4. 框架层面的功能统一

Table 1 对比了近期运动生成模型的功能覆盖。Motion-Agent 是首个同时支持文本到运动生成、运动 captioning、多轮对话编辑、长序列合成与运动过渡组合的框架，且所有这些能力均通过同一套未做任务特定微调的组件实现。这种统一性源于“运动 token 化 + LLM 翻译 + GPT-4 协调”的模块化设计，而非为每个任务单独训练专用模型。

## 整体框架

Motion-Agent 是一个由大语言模型驱动的对话式人体运动生成与理解框架，其核心设计理念是将运动视为一种语言，从而直接复用预训练语言模型的泛化与对话能力。整个系统由三个关键模块构成：**对话协调器（GPT-4）**、**翻译代理（MotionLLM）** 以及 **运动分词器/解分词器（Motion Tokenizer/Detokenizer）**。三者的协作流程如 Figure 2 所示。

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/003_Figure_2.jpg]]
*Figure 2: Motion-Agent pipeline. GPT-4 can interact with the translation agent (i.e., MotionLLM) to generate or interpret motions based on input requirements. The generated motion tokens are concatenated and decoded, and the textual caption produced by MotionLLM is returned and processed by GPT-4*

### 1. 对话协调器：GPT-4

GPT-4 在整个框架中承担高层语义理解与任务规划的角色。当用户输入自然语言指令后，GPT-4 解析意图并生成一个结构化的 JSON 计划，该计划明确指定了需要调用翻译代理的次数、每次调用的参数（如文本描述或运动 token），以及最终如何组装结果。这种设计使得 Motion-Agent 无需额外训练即可支持多轮对话，涵盖运动生成、理解、编辑和推理等多种任务。

### 2. 翻译代理：MotionLLM

MotionLLM 是一个经过轻量微调的预训练语言模型，专门负责文本与运动之间的双向翻译。其工作流程为：

- **文本→运动（生成）**：接收自然语言描述，自回归地生成运动 token 序列，直到输出终止符 `</Motion>`。
- **运动→文本（captioning）**：接收运动 token 序列，生成对应的自然语言描述。

MotionLLM 仅通过 LoRA 适配器微调了 1–3% 的参数，冻结了原始文本 token 的嵌入层和输出层，从而在保持 LLM 原有语言能力的同时，高效地习得运动-文本的对齐关系。

### 3. 运动分词器与解分词器

连续运动数据与离散 token 之间的转换由一对 VQ-VAE 模块完成：

- **运动分词器（Encoder）**：将原始运动序列 $\mathbf{m}$ 编码为潜在嵌入 $\mathbf{z}_t$，并通过量化操作将其映射到码本 $\mathbf{C}$ 中最近的向量 $\hat{\mathbf{z}}_t$，得到离散的运动 token 索引。量化公式为：

$$\hat{\mathbf{z}}_t = \underset{\mathbf{c}_k \in \mathbf{C}}{\arg\min} \|\mathbf{z}_t - \mathbf{c}_k\|_2$$

- **运动解分词器（Decoder）**：将运动 token 序列解码还原为连续的运动表示。当 GPT-4 协调多次生成时，解分词器还负责平滑不同运动片段之间的过渡，确保最终输出的连贯性。

VQ-VAE 的训练损失由三部分组成：

$$\mathcal{L}_{vq} = \underbrace{\|\mathbf{m} - \hat{\mathbf{m}}\|_1}_{\mathcal{L}_{re}} + \alpha \underbrace{\|\mathbf{p} - \hat{\mathbf{p}}\|_1}_{\mathcal{L}_{p}} + \beta \underbrace{\|\mathbf{z} - sg[\hat{\mathbf{z}}]\|_2}_{\mathcal{L}_{commit}}$$

其中 $\mathcal{L}_{re}$ 为重建损失，$\mathcal{L}_{p}$ 为关节位置正则化项，$\mathcal{L}_{commit}$ 为承诺损失，用于约束编码器输出靠近所选码本向量。

### 4. 整体数据流

一次典型的对话式运动生成流程如下：

1. **用户输入**自然语言指令（如“生成一个人先走路再跳跃的动画”）。
2. **GPT-4** 解析指令，将其分解为子任务（如“走路”和“跳跃”），生成 JSON 计划。
3. **MotionLLM** 根据每个子任务的文本提示，自回归生成对应的运动 token 序列。
4. 所有运动 token 序列被**拼接**后送入解分词器，解码为连续的 3D 运动数据。
5. 若用户进行多轮编辑或追问，GPT-4 继续协调 MotionLLM 完成后续操作，整个过程无需额外训练。

这种模块化设计使得 Motion-Agent 天然支持可变长度运动生成（自回归直到终止符），避免了非自回归模型中因长度估计错误导致的严重漂移问题。同时，通过 GPT-4 的分解-拼接策略，框架理论上可以生成任意长度的复杂运动序列。

## 核心模块与公式推导

### 3.1 Motion-Agent 整体框架

Motion-Agent 由三个核心组件构成：**对话协调器（GPT-4）**、**运动分词/解分器（Motion Tokenizer/Detokenizer）** 和 **翻译代理（MotionLLM）**。

GPT-4 作为协调器，解析用户的多轮自然语言指令，生成结构化的 JSON 任务计划，决定何时调用 MotionLLM 执行运动生成或运动理解任务。MotionLLM 接收文本描述或运动 token 序列，执行双向翻译；生成的多个运动 token 序列被拼接后，由冻结的解码器统一解码为连续运动。当需要运动理解时，MotionLLM 生成文本描述，再由 GPT-4 加工后返回给用户。

### 3.2 运动分词（Motion Tokenization）

运动分词器采用 VQ-VAE 架构，将连续运动序列编码为离散 token，使其能被 LLM 处理。

**编码与量化**：给定运动序列 $\mathbf{m} = (\mathbf{m}_1, \mathbf{m}_2, \dots, \mathbf{m}_T)$，编码器 $E$ 将其映射为潜在嵌入序列 $\mathbf{z} = (\mathbf{z}_1, \mathbf{z}_2, \dots, \mathbf{z}_{T/N})$，其中 $N$ 为下采样率。每个嵌入向量 $\mathbf{z}_t$ 被替换为码本 $\mathbf{C} = \{\mathbf{c}_k\}_{k=1}^K$ 中最近的向量：

$$\hat{\mathbf{z}}_t = \underset{\mathbf{c}_k \in \mathbf{C}}{\arg\min} \|\mathbf{z}_t - \mathbf{c}_k\|_2$$

量化后的嵌入序列 $\hat{\mathbf{z}}$ 经解码器 $D$ 重建为运动 $\hat{\mathbf{m}}$。

**训练损失**：VQ-VAE 的总损失由三部分组成：

$$\mathcal{L}_{vq} = \underbrace{\|\mathbf{m} - \hat{\mathbf{m}}\|_1}_{\mathcal{L}_{re}} + \alpha \underbrace{\|\mathbf{p} - \hat{\mathbf{p}}\|_1}_{\mathcal{L}_{p}} + \beta \underbrace{\|\mathbf{z} - sg[\hat{\mathbf{z}}]\|_2}_{\mathcal{L}_{commit}}$$

- $\mathcal{L}_{re}$：运动重建损失，约束解码器输出与原始运动的 L1 距离。
- $\mathcal{L}_{p}$：关节位置正则化，对解码后的关节位置 $\hat{\mathbf{p}}$ 与真实位置 $\mathbf{p}$ 施加 L1 约束，权重为 $\alpha$。
- $\mathcal{L}_{commit}$：承诺损失，鼓励编码器输出 $\mathbf{z}$ 靠近量化向量 $\hat{\mathbf{z}}$，其中 $sg[\cdot]$ 表示停止梯度算子，权重为 $\beta$。

**运动词汇表构建**：码本索引直接构成运动 token 词汇表 $\mathbf{V}_m = \{\mathtt{<Motion\_i>}\}_{i=1}^{K}$，并添加特殊 token `<Motion>` 和 `</Motion>` 标记序列起止。这些 token 被注入预训练 LLM 的词汇表，嵌入层和输出层保持冻结，仅通过 LoRA 适配器微调。

### 3.3 MotionLLM：双向翻译代理

MotionLLM 的核心功能是实现文本序列与运动 token 序列之间的自回归翻译。

**训练目标**：给定条件 $c$（文本描述或运动 token 前缀），MotionLLM 以自回归方式预测目标 token 序列 $x = (x_1, x_2, \dots, x_L)$，训练目标为负对数似然：

$$\mathcal{L}_{LLM} = -\sum_{t} \log p_{\theta}(x_t | x_{<t}, c)$$

- 文本到运动生成：条件 $c$ 为自然语言描述，目标序列为运动 token（以 `<Motion>` 起始，以 `</Motion>` 终止）。
- 运动到文本生成：条件 $c$ 为运动 token 序列，目标序列为文本 token。

**关键设计**：仅通过 LoRA 微调 LLM 中 1-3% 的参数（生成任务 rank=64，captioning 任务 rank=32），原始文本 token 的嵌入层和输出层保持冻结。自回归生成直到预测出 `</Motion>` 终止 token，天然支持可变长度运动生成，无需手动指定目标长度。

### 补充图表

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/002_Figure_1.jpg]]
*Figure 1: Multi-turn Conversation Between User and Motion-Agent. First Turn: Motion Understanding; Second Turn: Motion Generation; Third Turn: Motion Understanding with Previously Generated Motion; Fourth Turn: Motion Editing; Fifth Turn: Continue Motion Generation; Last Turn: Motion Editing on Long Sequence. Note that all turns are continuous*

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/005_Figure_3.jpg]]
*Figure 3: Motion-Agent can comprehend abstract, complex user prompts and generate accurate, long motions. It also understands and answers user questions based on real-world knowledge. Notably, the three turns in this figure stem from a continuous conversation, demonstrating the flexibility of its multi-turn capability in scenarios that should not be influenced by previous turns*

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/007_Figure_5.jpg]]
*Figure 5: Motion-Agent can compose motions with smooth transitions. In this example, the two motions “a person falls down on the back” and “a person is walking” are provided to Motion-Agent in two turns. The system then generates a “stand up” motion to facilitate a seamless composition of the two motions*

## 实验与分析

### 核心定量结果：MotionLLM的双向翻译性能

MotionLLM作为Motion-Agent框架的翻译代理，其核心设计目标是以极低的训练开销实现与全参数模型竞争的双向翻译性能。Table 2在HumanML3D测试集上的综合评估验证了这一目标。

在**文本到运动生成**（Text-to-Motion Generation）任务上，MotionLLM仅微调1-3%的参数（使用LoRA适配器），即取得了与全参数训练模型竞争的指标：
- **R Precision Top 1**达到0.515±.004，超过**MotionGPT**（Jiang et al., 2024b）的0.492±.003（+0.023），表明生成运动与输入文本的语义对齐更精确。
- **FID**为0.230±.009，与**MotionGPT**的0.232±.008基本持平（-0.002），处于同一性能层级。

需要注意的是，FID比较存在公平性问题：非自回归方法（如**MoMask**，Guo et al., 2024）在评估时使用了真实运动长度（ground truth lengths），而自回归的MotionLLM生成可变长度运动，这可能导致FID偏高。因此，FID的微小差距不应被过度解读为性能劣势。

在**运动到文本captioning**（Motion Captioning）任务上，MotionLLM展现出显著优势：
- **Bert Score**达到42.63，大幅超越此前最佳方法**MotionChain**（Jiang et al., 2024c）的36.9（+5.73），相对提升约15.5%。
- 评估使用了未经预处理的真实描述文本，避免了先前工作中忽略语法时态等问题，使各方法的语言指标比较更加一致。

这一结果揭示了一个关键洞察：预训练LLM的语言先验在运动理解任务上具有极强的迁移优势，仅需轻量微调即可将连续运动信号映射为语义准确的文本描述，而生成任务则对运动表示的精细度有更高要求。

### 自回归生成模式的关键优势

MotionLLM采用自回归架构，这一设计选择在无真实运动长度输入的场景下展现出决定性优势。Figure 10对比了MotionLLM与非自回归模型**MoMask**（Guo et al., 2024）的表现：MoMask依赖一个长度估计器（length estimator）根据文本预测目标运动长度，当估计器失效时，错误的长度预测会导致严重的运动漂移（severe drifting）。相反，MotionLLM自回归地预测运动token，直到输出终止token `</Motion>`，天然消除了对运动长度先验知识的依赖。

这一特性使得Motion-Agent在处理长序列和复杂描述时更加鲁棒，无需用户手动指定运动时长，也避免了长度估计错误引发的级联故障。

### 消融实验：组件选择的影响

**LLM骨干与LoRA配置**（Table 3）：
在KIT-ML数据集上的消融实验表明，使用更大的LLM骨干（如Gemma-9B vs Gemma-2B）或提高LoRA rank可整体提升生成指标（R Precision、FID等）。这验证了更强的语言先验和更大的适配容量对运动生成质量的正向贡献。

**翻译代理的不可替代性**（Figure 6）：
将MotionLLM替换为**MotionGPT**后，生成的过渡运动不平滑（cannot generate smooth motion transition）。这表明，尽管MotionGPT也支持文本-运动双向生成，但其运动表示和训练方式与GPT-4协调器的拼接解码策略不兼容。精心设计的翻译代理——特别是其运动tokenizer/detokenizer与LLM词汇的对齐——对框架的整体性能至关重要。

**对话协调器的能力要求**（Table 5）：
在双轮对话提示的测试中，较小的LLM（如Llama-3-7B、Mixtral-8x7B）无法可靠遵循要求的JSON格式，导致输出无法解析。这揭示了当前框架的一个关键依赖：对话协调器必须具备足够强的指令遵循能力（instruction following），而GPT-4级别的模型是目前实现可靠多轮交互的必要条件。

### 定性分析：长序列生成与运动组合

Figure 4展示了Motion-Agent与其他方法在复杂运动生成上的定性对比。当输入描述包含一系列连续动作（如“a person walks forward, then turns around, and sits down”）时，Motion-Agent能准确生成连贯的动作序列，而其他模型倾向于输出短而模糊的运动（short and unclear motions）。这得益于GPT-4协调器将长描述分解为多个子任务，由MotionLLM分别生成短运动片段，再通过detokenizer平滑拼接。

Figure 5进一步展示了运动组合（motion composition）能力：给定“a person falls down on the back”和“a person is walking”两个运动，Motion-Agent在两轮对话中生成中间动作“stand up”，实现无缝过渡组合。这种能力源于框架的模块化设计——GPT-4识别过渡需求，MotionLLM生成补全运动，detokenizer确保运动边界平滑。

### 失败模式与局限性

1. **多人运动生成尚处初步阶段**（Figure 11）：仅进行了初步探索，尚未进行全面评估和优化，性能缺乏量化保证。

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/019_Figure_11.jpg]]
*Figure 11: Multi-human Motion Generation using Motion-Agent*

2. **长运动依赖分解-拼接范式**：底层HumanML3D数据集的运动序列通常短于10秒，长运动生成通过LLM分解描述、逐段生成、拼接实现。虽然理论上可生成无限长运动，但全局动作的连贯性受限于片段间的过渡质量。

3. **对话协调器的闭源依赖**：如Table 5所示，较小开源LLM无法可靠遵循JSON格式输出，限制了框架的完全开源部署。如何通过改进协调机制或使用更强开源LLM降低对GPT-4的依赖，是一个待解决的关键问题。

4. **运动表示的粒度限制**：当前方法仅处理整体身体运动，未涉及手部姿态或面部表情细节，这限制了其在精细交互场景（如手物交互）中的应用。

### 补充图表

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/008_Table_2.jpg]]
*Table 2: Quantitative evaluation of MotionLLM on the HumanML3D (Guo et al., 2022a) test set. For motion generation, we follow T2M (Guo et al., 2022a) for the evaluation metrics. The evaluations are conducted 20 times to obtain a 95% confidence interval. Methods indicated in italics utilize the ground truth lengths for estimation. Models above capable of bidirectional generation are also included in the captioning evaluation. For motion captioning, we use the ground truth captions without pre-processing and linguistic metrics suggested by Guo et al. (2022b) for evaluation. Best scores are highlighted in boldface, while underscore refers to the second best*

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/004_Table_1.jpg]]
*Table 1: Comparison on functionalities among recent motion generation models. Italicized model indicates the corresponding model requires pre-training and task-specific tuning*

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/006_Figure_4.jpg]]
*Figure 4: Comparison with Other Methods. Our Motion-Agent accurately generates motions involving a series of actions, while other models struggle with more complex descriptions like this, resulting in short and unclear motions*

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/009_Figure_6.jpg]]
*Figure 6: Motion-Agent Ablation Study. We substituted MotionLLM with MotionGPT and noticed that MotionGPT cannot generate smooth motion transition*

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/010_Table_3.jpg]]
*Table 3: Ablation on MotionLLM We conducted an ablation study to examine the impact of different LLM backbones and adapter sizes. The results are shown in Table 3, from which we may conclude that using larger backbone models or increasing the LoRA rank leads to overall improvements in the metrics*

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/018_Figure_10.jpg]]
*Figure 10: Comparison between MotionLLM and MoMask (Guo et al., 2024), which is nonautoregressive. During regular inference, MoMask uses a length estimator to predict the length conditioned on the text. This estimator is likely to fail. In this example, their incorrect predicted length causes severe drifting*

![[assets/figures/papers/paper_list_l1903_Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with/figures/011_Figure_7.jpg]]
*Figure 7: More examples of Motion-Agent*

## 方法谱系与知识库定位

### 1. 方法与基线的关系

**Motion-Agent** 的核心贡献在于将人体运动生成问题重新表述为一种语言翻译任务，并通过“对话LLM协调器 + 轻量翻译代理”的架构，在不引入额外对话训练数据的前提下，实现了多轮、多任务的运动生成、编辑与理解。其设计在多个维度上与现有基线形成对比：

- **相对于扩散模型（MDM、MLD、MotionDiffuse）**：扩散模型通常在连续隐空间中对运动进行建模，需要从噪声开始迭代去噪，推理速度较慢，且天然不支持多轮对话或运动理解任务。Motion-Agent 将运动离散化为 token，利用自回归语言模型的快速推理和对话泛化能力，绕开了扩散模型的这些结构限制。基线中，**MDM**（Tevet et al., 2023）和 **MLD**（Chen et al., 2023b）均属于此类。

- **相对于 VQ-VAE + 自回归/非自回归的专用模型（T2M-GPT、MoMask）**：**T2M-GPT**（Zhang et al., 2023b）和 **MoMask**（Guo et al., 2024）同样采用了“离散 token + 生成式建模”的路线，但二者均为任务特定的专用架构，不具备双向翻译（captioning）能力，也不支持对话交互。此外，MoMask 作为非自回归模型，在推理时需要依赖长度估计器来指定目标运动长度；当估计错误时，会产生严重的运动漂移（见 Figure 10）。Motion-Agent 的自回归生成模式天然避免了这一问题——模型持续预测 token 直到输出终止符 `</Motion>`，无需显式指定长度。

- **相对于运动-语言统一模型（MotionGPT、MotionChain）**：**MotionGPT**（Jiang et al., 2024b）是首个将运动视为语言的统一模型，支持文本到运动和运动到文本的双向生成。Motion-Agent 在此基础上做了两个关键改进：其一，采用 LoRA 微调仅 1–3% 的预训练 LLM 参数，大幅降低了训练成本；其二，引入 GPT-4 作为对话协调器，使框架无需额外指令微调即可支持多轮对话。相比之下，**MotionChain**（Jiang et al., 2024c）虽然也支持多轮运动生成，但需要专门的指令微调数据。在运动 captioning 任务上，MotionLLM 的 Bert Score 达到 42.63，显著高于 MotionChain 的 36.9（Table 2）。

- **相对于传统 text-to-motion 模型（T2M、TM2T）**：**T2M**（Guo et al., 2022a）和 **TM2T**（Guo et al., 2022b）分别代表了早期专用生成模型和双向翻译模型的基线。这些方法需要从零开始训练完整架构，缺乏泛化到新任务和对话场景的能力。

### 2. 适用边界与局限性

尽管 Motion-Agent 在功能覆盖面和效率上展现出显著优势，其当前设计仍存在明确的适用边界：

- **运动表示的粒度限制**：当前框架仅处理整体身体运动，未涉及手部姿态或面部表情的细节建模。这意味着对于需要精细手部交互（如抓取物体）或面部表情同步的应用场景，Motion-Agent 尚无法直接适用。

- **多人运动生成尚处于初步阶段**：论文展示了多人运动生成的初步示例（Figure 11），但未进行系统的定量评估和优化。该功能的稳定性和生成质量仍需进一步验证。

- **对强对话 LLM 的依赖**：框架的对话协调器依赖 GPT-4 级别的强大语言模型来生成结构化 JSON 计划。消融实验（Table 5）表明，较小的开源 LLM（如 Llama-3-7B、Mixtral-8x7B）无法可靠遵循所需的 JSON 格式，导致输出无法解析。这限制了框架在纯离线或开源环境中的部署灵活性。

- **长运动生成的拼接式策略**：由于底层 HumanML3D 数据集中的运动序列通常短于 10 秒，长运动生成是通过 LLM 将复杂描述分解为多个短动作、再分别生成并拼接实现的。这种分解-拼接策略可能影响全局动作的物理连贯性，尤其是在需要连续流畅过渡的长序列场景中。

- **缺乏 3D 场景感知**：当前框架未集成 3D 视觉理解能力，无法根据环境中的物体（如椅子、楼梯）生成与环境交互的运动。这使其难以直接应用于具身智能或人-场景交互生成任务。

### 3. 开放问题

基于上述局限性，以下几个方向构成了值得关注的开放问题：

1. **细粒度运动表示的扩展**：如何将当前的离散 token 表示和生成框架扩展到包含手部姿态、面部表情甚至全身接触力的运动数据中？这可能需要更高维度的码本设计或层次化的 token 结构。

2. **3D 场景感知的集成**：能否将 3D 视觉编码器（如点云或体素编码器）的输出作为额外条件信号注入 MotionLLM，使系统能够根据环境物体的几何和语义信息生成合理的交互运动？

3. **多人运动生成的系统化验证**：多人运动生成涉及角色间的时空协调和物理约束。如何设计合适的评估基准和指标，并优化框架以处理多人场景中的碰撞避免、动作同步等问题？

4. **降低对闭源大模型的依赖**：能否通过改进协调机制的鲁棒性（如引入约束解码或格式校验模块），或利用能力更强的开源 LLM，使整个框架在完全离线的环境中也能稳定运行？

5. **长序列生成的端到端优化**：当前分解-拼接策略的长运动生成是否可以通过端到端的训练（如引入跨片段的注意力机制或全局运动先验）来提升连贯性，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2025/Motion_Agent_A_Conversational_Framework_for_Human_Motion_Generation_with_LLMs.pdf]]