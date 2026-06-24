---
title: "BAGEL: Emerging Properties in Unified Multimodal Pretraining"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/BAGEL_Emerging_Properties_in_Unified_Multimodal_Pretraining.pdf
aliases:
- BAGEL
tags:
- arxiv_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 采用 Mixture-of-Transformers (MoT) 架构，将理解专家和生成专家的参数完全解耦，同时保持共享自注意力，实现无瓶颈的长上下文跨模态交互，并通过大规模交错多模态数据训练推动涌现能力。
primary_logic: 将理解和生成的参数分离但共享自注意力，能够缓解优化冲突，使得随着数据规模扩大，模型从基本理解和生成逐渐涌现出自由形式视觉编辑、世界建模和多步推理等复杂能力。
claims:
- MoT 架构在生成 MSE 和理解 CE 损失上均优于 Dense 和 MoE 变体，收敛更快且最终损失更低
- 随着训练 token 增加，模型智能编辑能力从 15 提升至 45，涌现出复杂推理能力
- Chain-of-Thought 推理将 IntelligentBench 得分从 44.9 提升至 55.3，并显著提升其他多模态推理基准
- MMMU 上 准确率 = 55.3
---

# BAGEL: Emerging Properties in Unified Multimodal Pretraining

> [!tip] 核心洞察
> 将理解和生成的参数分离但共享自注意力，能够缓解优化冲突，使得随着数据规模扩大，模型从基本理解和生成逐渐涌现出自由形式视觉编辑、世界建模和多步推理等复杂能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | BAGEL：统一多模态预训练中的涌现特性 |
| 英文题名 | BAGEL: Emerging Properties in Unified Multimodal Pretraining |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2505.14683) · [Project](https://bagel-ai.org/) · [Code](https://github.com/black-forest-labs/flux) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | BAGEL |
| Dataset | MMMU, GenEval, WISE, IntelligentBench |

> [!tip] 效果简介
> - MMMU 上，准确率 55.3 vs 41.0 (Janus-Pro) (+14.3)。
> - GenEval 上，Overall 分数 0.88 vs 0.82 (FLUX-1-dev) (+0.06)。
> - WISE 上，Overall 分数 0.70 (w/ CoT) vs 0.52 (w/o CoT) (+0.18)。

## 概述

### 问题与瓶颈

当前多模态统一模型在同时处理视觉理解与视觉生成任务时，面临三个核心瓶颈：第一，理解与生成任务之间存在**信息压缩瓶颈**——例如依赖外部扩散模型（External Diffuser）将图像压缩到潜空间，导致信息损失；第二，两类任务在单一参数空间中**优化目标冲突**，使得模型难以同时收敛到最优；第三，现有模型普遍缺乏**长上下文跨模态交互**能力，限制了复杂多模态推理的涌现。

### 核心思路

BAGEL 提出 **Mixture-of-Transformers (MoT)** 架构，将理解专家与生成专家的参数**完全解耦**——每个 Transformer 层包含两套独立的前馈网络和注意力参数，但**共享自注意力机制**。这一设计实现了三个关键突破：

- **消除信息瓶颈**：理解与生成各自拥有独立的参数空间，不再通过压缩潜变量进行信息传递，所有 token 通过共享自注意力实现无瓶颈的长上下文跨模态交互。
- **缓解优化冲突**：分离的参数使得理解和生成可以各自按照最优路径收敛，实验表明 MoT 在生成 MSE 损失和理解 CE 损失上均优于 Dense 和 MoE 变体（Figure 3）。
- **支撑涌现能力**：在大规模交错多模态数据（文本、图像、视频、网页）上训练后，模型随着训练 token 增加，从基本理解和生成**涌现出**自由形式视觉编辑、世界建模和多步推理等复杂能力（Figure 7）。

### 方法谱系与知识库定位

BAGEL 属于**统一多模态预训练模型**，采用 decoder-only Transformer 架构，同时支持视觉理解与视觉生成。在方法谱系中，其定位如下：

| 维度 | 基线方法 | BAGEL 的改进 |
|------|---------|-------------|
| **Transformer 架构** | 单一 Dense Transformer 或仅复制 FFN 的 MoE | MoT：完全复制所有参数作为生成专家，与理解专家共享自注意力（Figure 3） |
| **注意力机制** | 标准因果注意力 | 广义因果注意力：视觉 token 双向注意力，文本 token 因果注意力，支持交错多图像生成（Figure 15） |
| **数据构成** | 主要使用图像-文本对 | 大规模交错多模态数据（文本、图像、视频、网页），并添加推理增强数据（Table 1） |

与现有工作的关系：
- 相比 **Janus-Pro 7B** 等统一模型，BAGEL 通过 MoT 实现了理解与生成的更彻底解耦，在 MMMU 理解基准上提升 14.3 个百分点。
- 相比 **SD3-medium**、**FLUX.1-dev** 等专用生成模型，BAGEL 在 GenEval 文本到图像生成基准上达到 0.88，超越 FLUX.1-dev 的 0.82，同时保留了理解能力。
- 相比 **Step1X-Edit** 等编辑模型，BAGEL 在 IntelligentBench 复杂推理编辑任务上从 14.9 提升至 44.9，展示了涌现的推理能力。
- 与 **GPT-4o** 等私有系统相比，BAGEL 在部分复杂推理任务上仍有差距，但通过 Chain-of-Thought 推理可将 IntelligentBench 得分进一步提升至 55.3。

### 主要结果速览

| 基准测试 | 指标 | BAGEL | 对比基线 | 提升 | 证据锚点 |
|---------|------|-------|---------|------|---------|
| MMMU（理解） | 准确率 | 55.3 | 41.0 (Janus-Pro) | +14.3 | Table 4 |
| GenEval（生成） | Overall | 0.88 | 0.82 (FLUX.1-dev) | +0.06 | Table 5 |
| WISE（世界推理） | Overall | 0.70 (w/ CoT) | 0.52 (w/o CoT) | +0.18 | Table 6 |
| IntelligentBench（推理编辑） | Score | 44.9 | 14.9 (Step1X-Edit) | +30.0 | Table 8 |

### 局限与开放问题

模型在涉及特定 IP、复杂文本渲染、反事实场景、对象交换和去模糊等任务上表现不佳，与 GPT-4o 相比仍有明显差距（Figure 17）。MoT 架构如何随着参数和数据规模进一步扩展、如何更有效地评估需要强多模态推理的任务，以及如何通过强化学习或对抗训练进一步优化，仍是待探索的开放问题。

## 背景与动机

多模态人工智能正朝着统一理解和生成的方向演进，但当前方法面临一个核心瓶颈：**理解任务与生成任务在优化目标上的根本冲突**。理解任务通常依赖语义级别的视觉编码器（如 ViT）提取高层特征，而生成任务需要保留低层像素细节的潜空间表示（如 VAE）。现有统一模型要么采用单一 Dense Transformer 同时处理两种任务，导致优化困难；要么引入 External Diffuser 将生成信息压缩为潜变量再注入，形成信息瓶颈，限制了长上下文跨模态交互与复杂推理能力。

BAGEL 的核心洞察在于：**将理解与生成的参数完全解耦，同时保持共享自注意力，能够缓解优化冲突，并随着数据规模扩大涌现出自由形式视觉编辑、世界建模和多步推理等复杂能力**。为此，BAGEL 提出了 Mixture-of-Transformers (MoT) 架构，为理解专家和生成专家分配独立的完整参数副本，仅共享自注意力层，从而在无瓶颈的前提下实现长上下文跨模态交互。同时，BAGEL 采用大规模交错多模态数据（文本、图像、视频、网页）进行预训练，并引入推理增强数据，推动模型从基本理解和生成逐步涌现出更高级的智能编辑与推理能力。

实验证据表明，MoT 架构在生成 MSE 损失和理解 CE 损失上均优于 Dense 和 MoE 变体，收敛更快且最终损失更低（Figure 3）。随着训练 token 从 0.18T 增长至 3.61T，模型在 IntelligentBench 上的智能编辑得分从约 15 提升至 45，呈现出明显的涌现曲线（Figure 7）。此外，Chain-of-Thought 推理将 IntelligentBench 得分从 44.9 进一步提升至 55.3，并显著提升其他多模态推理基准（Table 8, Table 6, Table 9, Table 10）。这些结果共同验证了 MoT 架构设计和大规模交错数据训练的有效性。

## 核心创新

BAGEL 的核心创新在于通过 **Mixture-of-Transformers (MoT)** 架构实现了多模态理解与生成任务的参数级解耦，同时保持共享自注意力机制，从而从根本上缓解了统一多模态模型中的优化冲突与信息瓶颈问题。

### 架构创新：从参数共享到专家解耦

传统统一多模态模型通常采用单一 Dense Transformer 处理所有模态，或仅通过复制前馈网络（FFN）构建 Mixture-of-Experts (MoE) 变体。这类设计面临两个深层矛盾：

1. **信息瓶颈**：如 External Diffuser 等方法将视觉生成信息压缩为潜变量，限制了长上下文跨模态交互。
2. **任务冲突**：理解任务（优化交叉熵损失）与生成任务（优化均方误差损失）对参数更新方向存在竞争性需求。

BAGEL 的 MoT 架构对此进行了根本性重构：将 Transformer 层中的所有参数**完全复制**为两个专家——理解专家与生成专家，二者共享自注意力层。这一设计的关键因果机制在于：

- **参数解耦**：理解专家和生成专家各自拥有独立的 FFN 和 LayerNorm 等参数，可分别针对 CE 损失和 MSE 损失进行优化，消除了单一参数集上的梯度冲突。
- **注意力共享**：所有 token（文本、理解视觉、生成视觉）在同一自注意力层中进行跨模态交互，确保信息流无瓶颈，支持长上下文的多模态推理。

架构消融实验（Figure 3）提供了决定性证据：在 1.5B LLM 规模的对照实验中，MoT 变体在生成 MSE 损失和理解 CE 损失上均优于 Dense 和 MoE 变体，不仅收敛速度最快，最终损失也最低。这验证了“参数解耦 + 注意力共享”设计的有效性。

### 注意力机制创新：广义因果注意力

BAGEL 引入了**广义因果注意力**机制，突破了标准因果注意力的限制。在标准因果注意力下，每个 token 只能关注其之前的 token，这不利于图像内部的双向建模。BAGEL 的改进方案是：

- **视觉 token**：采用双向注意力，允许同一图像内的视觉 token 相互关注，充分捕获空间上下文。
- **文本 token**：保持因果注意力，确保语言建模的自回归特性。
- **交错多图像**：支持多图像场景下的灵活注意力模式，为多图像生成和编辑提供基础。

该设计在训练时通过精心构造的因果掩码实现（Figure 15），使得模型能够在保持文本生成因果性的同时，充分利用视觉信息的双向依赖。

### 数据策略创新：大规模交错多模态数据

BAGEL 的数据构成策略与架构设计形成了协同闭环。传统统一模型主要依赖图像-文本对数据训练，缺乏序列化的多模态推理信号。BAGEL 构建了包含文本、图像、视频和网页的**大规模交错多模态数据**（Table 1），并通过以下策略增强数据质量：

- **视频交错数据**：从原始视频中预处理和过滤，生成时间对齐的字幕，构建视觉-文本交错序列。
- **网页交错数据**：基于 OmniCorpus，采用两阶段过滤管线（LLM 分类器 + fastText）筛选教程、百科条目和设计类文档，并通过“caption-first”策略为每张图像生成简洁描述作为概念支架。

在此基础上，BAGEL 进一步添加了**推理增强数据**，为后续涌现的 Chain-of-Thought 推理能力提供了数据基础。

### 涌现能力的因果链

上述创新构成了一个因果闭环：MoT 架构缓解了优化冲突，使得模型能够在大规模交错数据上进行有效训练；随着训练 token 量增加，模型从基本理解和生成能力逐渐**涌现**出自由形式视觉编辑、世界建模和多步推理等复杂能力。Figure 7 的涌现曲线显示，模型的智能编辑能力随训练 token 增加从 15 提升至 45，呈现明显的相变特征。这一涌现现象的根本驱动力在于：参数解耦消除了任务间的负向干扰，而共享注意力保证了跨模态信息的无损传递，使得模型容量能够被充分释放用于学习复杂的多模态推理模式。

## 整体框架

BAGEL 是一个统一多模态预训练模型，其核心设计目标是在一个解码器框架内同时实现高质量的多模态理解与生成，并缓解两类任务间的优化冲突。为此，模型在架构、编码、注意力与训练流程上进行了系统性设计。

### 核心瓶颈与设计动机

现有多模态统一模型（如 EMU2、OmniGen）通常将理解与生成的参数耦合在同一个 Transformer 中，或仅通过外部扩散器（External Diffuser）处理生成任务。这种做法引入了两个关键瓶颈：

1. **信息瓶颈**：外部扩散器依赖潜变量压缩，限制了理解与生成之间的信息流通，难以支持复杂多模态推理。
2. **任务冲突**：理解任务（交叉熵优化）与生成任务（去噪/回归优化）对参数更新方向存在竞争，单一模型难以同时收敛到最优。

BAGEL 通过 **Mixture-of-Transformers (MoT)** 架构将理解专家与生成专家的参数完全解耦，同时保持共享自注意力，从而在无瓶颈的长上下文跨模态交互下，使模型随着数据规模扩大涌现出自由形式视觉编辑、世界建模和多步推理等复杂能力。

### 整体 Pipeline 与模块关系

BAGEL 的完整处理流程由以下模块串联构成，数据从原始多模态输入到最终文本/图像输出依次流经各模块：

```
输入（文本 + 图像/视频）
        │
        ├──► 理解视觉编码器 (SigLIP2 ViT + NaViT)
        │         │
        │         ▼
        │    MLP 连接器
        │         │
        │         ▼
        └──► 生成视觉编码器 (FLUX VAE) ──► 潜空间视觉 token
                  │                              │
                  ▼                              ▼
            视觉 token 序列              视觉 token 序列（含扩散时间步编码）
                  │                              │
                  └──────────┬───────────────────┘
                             │
                             ▼
                    MoT Transformer 层 × N
                    ┌─────────────────────────┐
                    │   共享多模态自注意力      │
                    │  ┌─────────┐ ┌─────────┐ │
                    │  │理解专家  │ │生成专家  │ │
                    │  │(参数 A) │ │(参数 B) │ │
                    │  └─────────┘ └─────────┘ │
                    └─────────────────────────┘
                             │
                             ▼
                    输出：文本 token（理解）
                          视觉 token → Rectified Flow 去噪 → 图像（生成）
```

#### 1. 双视觉编码器

模型采用两套独立的视觉编码器，分别服务于理解和生成任务，以捕获不同粒度的信息：

- **理解视觉编码器**：基于 **SigLIP2-so400m/14** 的 ViT，结合 **NaViT** 支持原生宽高比处理，提取语义级特征用于多模态理解。该编码器在 Alignment 阶段通过 MLP 连接器与 LLM 对齐，之后在整个预训练中保持冻结。
- **生成视觉编码器**：采用 **FLUX VAE**，将图像压缩到潜空间，保留低层像素信息用于生成任务。

这种双编码器设计使得语义理解与像素级生成各司其职，避免了单一编码器在两类任务间的折中。

#### 2. MLP 连接器

SigLIP2 ViT 输出的视觉特征通过一个 MLP 连接器映射到 LLM 的隐藏维度。该连接器在 **Alignment 阶段** 单独训练（ViT 和 LLM 均冻结），目的是弥合视觉编码器与语言模型之间的表示鸿沟，为后续大规模预训练提供稳定的初始化。

#### 3. MoT Transformer 层

这是 BAGEL 架构的核心创新。每个 Transformer 层包含：

- **共享多模态自注意力**：所有 token（文本 token、理解视觉 token、生成视觉 token）在统一的自注意力机制中交互。注意力掩码采用广义因果注意力——文本 token 执行标准因果注意力，视觉 token 执行双向注意力，从而支持交错多图像生成场景下的灵活上下文建模。
- **理解专家**：一套完整的 Transformer 参数（包括 FFN 等），专门处理理解相关的特征变换。
- **生成专家**：另一套完全独立的 Transformer 参数，专门处理生成相关的特征变换。

在每一层中，token 先通过共享自注意力进行跨模态交互，然后根据其类型分别路由到理解专家或生成专家进行前馈处理。这种“共享注意力 + 分离专家”的设计，既保证了多模态信息在长上下文中的充分融合，又通过参数解耦缓解了理解与生成的优化冲突。实验表明，MoT 架构在生成 MSE 损失和理解 CE 损失上均优于 Dense 和 MoE 变体，收敛更快且最终损失更低（Figure 3）。

#### 4. Rectified Flow 训练与扩散时间步编码

生成任务采用 **Rectified Flow** 框架进行去噪训练。视觉 token 在进入 Transformer 之前，会注入扩散时间步编码，使模型感知当前去噪阶段。训练时，模型接收加噪后的视觉 token，通过生成专家预测噪声，以 MSE 损失优化；推理时，从纯噪声出发，迭代去噪得到最终图像。

### 训练流程

BAGEL 采用多阶段训练策略，各阶段的数据构成与优化目标逐步递进：

| 阶段 | 目标 | 可训练参数 | 数据重点 |
|------|------|-----------|---------|
| **Alignment** | 视觉-语言对齐 | 仅 MLP 连接器 | 图像-文本对 |
| **Pre-training** | 大规模多模态预训练 | 全部（ViT 冻结） | 交错多模态数据（文本、图像、视频、网页） |
| **Continued Training** | 长上下文与推理增强 | 全部 | 增加推理增强数据 |
| **Supervised Fine-tuning** | 指令遵循与任务适配 | 全部 | 高质量指令数据 |

其中，Pre-training 阶段的数据构成是关键：模型在大规模交错多模态数据（包括视频和网页的交错视觉-文本序列）上训练，并添加推理增强数据以推动复杂推理能力的涌现。数据采样比例和学习率等超参数经过消融验证：提高生成数据采样比例可降低 MSE 损失，而 CE 损失无一致规律（Figure 5）；较大学习率加速生成收敛，较小学习率利于理解（Figure 6）。

### 输入输出流

- **输入**：任意交错的文本与图像序列，支持单图/多图/视频帧等视觉输入。
- **输出**：对于理解任务，模型自回归生成文本 token；对于生成任务，模型输出视觉 token 经 Rectified Flow 去噪后解码为图像。两类输出可在同一序列中交替出现，实现“思考辅助生成”——即先生成推理文本，再基于推理结果生成图像，显著提升复杂编辑与多步推理任务的性能（Table 8, Table 6）。

## 核心模块与公式推导

### 架构设计：Mixture-of-Transformers (MoT)

BAGEL 的核心架构创新在于采用 **Mixture-of-Transformers (MoT)** 设计，将多模态理解与生成的参数完全解耦，同时通过共享自注意力实现无瓶颈的跨模态交互。如 Figure 2 所示，模型包含以下关键模块：

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/003_Figure_2.jpg]]
*Figure 2: We use two Transformer experts to process understanding and generation information, and all tokens do shared multi-modal self attention in each Transformer block. We adopt two distinct encoders to separately capture semantic content and low-level pixel information for image understanding and generation tasks*

**1. 双视觉编码器**

- **理解视觉编码器**：采用 **SigLIP2-so400m/14** 作为 ViT 骨干，并集成 **NaViT** 以支持原生宽高比的图像处理。该编码器负责提取高层语义特征，服务于多模态理解任务。
- **生成视觉编码器**：采用 **FLUX VAE**，将图像压缩到潜空间表示，服务于图像生成任务。两个编码器各司其职，分别捕获语义内容和低层像素信息。

**2. MLP 连接器**

在 Alignment 阶段，仅训练 MLP 连接器，将 SigLIP2 ViT 的视觉特征映射到 LLM 的隐空间维度，同时冻结视觉编码器和语言模型。这一设计确保视觉语义与语言表征的有效对齐。

**3. MoT Transformer 层**

这是 BAGEL 的核心计算单元。每个 Transformer 块包含两个独立的专家——**理解专家**和**生成专家**，两者完全复制所有参数（而非仅复制 FFN 的 MoE 方案），但共享同一个自注意力模块。所有 token（文本 token 和视觉 token）在每一层都参与共享的多模态自注意力计算，消除了传统 External Diffuser 方案中的潜变量压缩瓶颈。

**4. 广义因果注意力**

BAGEL 采用广义因果注意力机制（见 Figure 15）：视觉 token 之间使用双向注意力以充分利用图像内部的空间上下文，文本 token 使用标准因果注意力以保持自回归生成能力。这一设计天然支持交错的多图像生成，使模型能够处理复杂的多模态序列。

**5. Rectified Flow 训练与扩散时间步编码**

视觉 token 的生成采用 Rectified Flow 框架进行去噪训练。扩散时间步信息通过专门的时间步编码注入视觉 token，使模型能够感知去噪过程的当前阶段。

### 关键公式与变量

根据提供的分析数据，论文中未提取到需要在此展示的具体公式 LaTeX 代码。以下仅基于架构描述给出概念性说明，**不推导未见公式**：

- **理解损失**：采用标准的交叉熵损失（CE loss），作用于文本 token 的预测，衡量多模态理解能力。
- **生成损失**：采用均方误差损失（MSE loss），作用于视觉 token 的去噪预测，衡量图像生成质量。如 Figure 3 的消融实验所示，MoT 架构在 CE 和 MSE 两项损失上均优于 Dense 和 MoE 变体，收敛速度最快且最终损失最低。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/004_Figure_3.jpg]]
*Figure 3: Loss curves of various designs. CE loss and MSE loss are computed on multimodal understanding and generation tasks, respectively. Ablation experiments are carried out on a 1.5B LLM. The sampling ratio for generation and understanding data is set at 4:1*

### 训练配方中的优化器设置

论文明确给出的优化器超参数为 AdamW：

$$
\beta_1 = 0.9,\quad \beta_2 = 0.95,\quad \epsilon = 1.0 \times 10^{-15}
$$

该配置在所有训练阶段统一使用，旨在抑制损失尖峰，确保训练的稳定性。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/010_Figure_5.jpg]]
*Figure 5: Loss curves of different data ratios. Ablation experiments are carried out on a 1.5B LLM. "1g1u" means that the sampling ratio for generation and understanding data is set at 1:1*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/011_Figure_6.jpg]]
*Figure 6: Loss curves of different learning rates. Ablation experiments are carried out on a 1.5B LLM. The sampling ratio for generation and understanding data is set at 1:1*

## 实验与分析

### 核心架构消融：MoT 为何有效

BAGEL 的设计起点是对统一多模态模型架构空间的系统性消融。在 1.5B 规模的 LLM 上，作者对比了三种 Transformer 变体：**Dense**（单一 Transformer 处理所有 token）、**MoE**（仅复制 FFN 层作为专家）和 **MoT**（完全复制所有参数作为生成专家，与理解专家共享自注意力）。如 Figure 3 所示，在生成数据与理解数据采样比例为 4:1 的条件下，MoT 在生成任务的 MSE 损失和理解任务的 CE 损失上均表现出最快的收敛速度和最低的最终损失。Dense 变体由于理解和生成的优化目标冲突，在两个损失上均表现最差；MoE 虽有所改善，但其仅解耦 FFN 的设计仍不足以充分缓解模态间的竞争。这一结果直接支撑了论文的核心因果主张：**将理解和生成的参数完全分离，同时保持共享自注意力，是实现无瓶颈跨模态交互的关键**。

### 训练动态与数据配比

训练过程中的数据采样比例和学习率对模型性能有显著影响。Figure 5 显示，将生成数据的采样比例从 50% 提升至 80%，MSE 损失有约 0.4% 的绝对降低，但 CE 损失并无一致规律——在训练步数约 14,000 时，不同配比间的 CE 损失最大差距仅为 0.07。这表明**生成任务对数据量更为敏感，而理解任务在较低采样比例下即可获得充分训练**。

学习率的影响则呈现出理解与生成之间的内在张力（Figure 6）：较大的学习率加速生成损失的收敛，但会损害理解损失的优化；较小的学习率有利于理解任务，却减缓生成的收敛速度。这一发现进一步验证了 MoT 架构解耦参数的必要性——在统一模型中，不同模态的学习动态天然存在冲突，而参数分离为各自适配不同的优化策略提供了空间。

### 涌现能力的实证观察

BAGEL 最引人注目的实验发现是随着预训练 token 数量增加而出现的**能力涌现**现象。Figure 7 追踪了多个任务在不同训练阶段的表现曲线：

- **智能编辑能力**：在 IntelligentBench 上，模型得分从约 15 跃升至约 45，呈现出明显的相变特征。这种能力并非渐进提升，而是在训练后期突然出现，暗示模型在足够的跨模态交互训练后习得了复杂推理能力。
- **移除 ViT token 的影响**：消融实验表明，移除 ViT 特征会导致智能编辑任务性能下降 16%，说明语义理解通路对复杂推理编辑至关重要。

Figure 8 和 Figure 9 的定性对比进一步展示了这一涌现过程：在训练 token 量较小时，模型仅能完成基本的文本到图像生成和简单编辑；随着训练量增加，模型逐渐展现出需要多步推理和世界知识的复杂编辑能力。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/014_Figure_8.jpg]]
*Figure 8: Comparison of models with different amounts of training tokens. We present cases of Text-to-Image generation and image editing*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/015_Figure_9.jpg]]
*Figure 9: Comparison of models with different amounts of training tokens. We present cases of intelligent editing that requires strong multimodal reasoning abilities*

### 主实验结果

#### 视觉理解

在多个标准多模态理解基准上，BAGEL 显著优于开源统一模型。如 Table 4 所示，在 MMMU 上达到 **55.3%** 准确率，相比 Janus-Pro 7B 的 41.0% 提升 **+14.3 个百分点**。这一结果验证了 MoT 架构在保持强大理解能力方面的有效性。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/016_Table_4.jpg]]
*Table 4: Comparison with state-of-the-arts on viusal understanding benchmarks. MME-S refers to the summarization of MME-P and MME-C. For MoE models, we report their activate params / total params. †: MetaQuery [57] adopts pre-trained model from Qwen2.5-VL [4] and freezes it during training. ∗∗: Partial results are from by MetaMorph [73] or MetaQuery [57]*

#### 文本到图像生成

在 GenEval 基准上（Table 5），BAGEL 的 Overall 分数达到 **0.88**，超越了专用生成模型 FLUX.1-dev（0.82）和 SD3-medium（0.74），同时显著优于其他统一模型如 Janus-Pro（0.32）和 EMU2（0.54）。这表明 BAGEL 在生成质量上可与最先进的专用生成模型竞争。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/017_Table_5.jpg]]
*Table 5: Evaluation of text-to-image generation ability on GenEval benchmark. ‘Gen. Only’ stands for an image generation model, and ‘Unified’ denotes a model that has both understanding and generation capabilities. † refer to the methods using LLM rewriter*

#### 世界知识推理

WISE 基准评估文本到图像生成中的复杂语义理解和世界知识（Table 6）。BAGEL 在使用 Chain-of-Thought 推理后达到 **0.70** Overall 分数，相比不使用 CoT 的 0.52 提升 **+0.18**，且显著优于所有对比的专用和统一模型。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/018_Table_6.jpg]]
*Table 6: Comparison of world knowledge reasoning on WISE. WISE examines the complex semantic understanding and world knowledge for T2I generation. ‘Gen. Only’ stands for an image generation model, and ‘Unified’ denotes a model that has both understanding and generation capabilities. **: Results of GPT-4o are tested by [92]*

#### 图像编辑与智能编辑

在 GEdit-Bench 上（Table 7），BAGEL 展现出竞争力的编辑能力。而在更具挑战性的 IntelligentBench 上（Table 8），BAGEL 以 **44.9** 分大幅超越专用编辑模型 Step1X-Edit 的 14.9 分（**+30.0**），并接近私有系统 Gemini 2.0 的表现。值得注意的是，GPT-4o 在 350 题中仅回答了 318 题，BAGEL 则能够处理全部问题。Figure 12 的定性对比显示，BAGEL 能有效处理需要多步推理和世界知识的复杂编辑案例，而 Step1X-Edit 则完全失败。

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/020_Table_7.jpg]]
*Table 7: Comparison on GEdit-Bench. All metrics are reported as higher-is-better (↑). G_SC, G_PQ, and G_O refer to the metrics evaluated by GPT-4.1*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/021_Table_8.jpg]]
*Table 8: Comparison on IntelligentBench. IntelligentBench examines complex reasoning ability in an image-editing context. ∗∗: Results are reported only on the subset of cases answered (some responses were rejected). GPT-4o answered 318 of 350 questions, while Gemini 2.0 answered 349 questions*

#### 推理增强的跨任务增益

Chain-of-Thought 推理带来的增益不仅限于 WISE。Table 9 和 Table 10 分别报告了 RISEBench 和 KRIS-Bench 的结果，CoT 推理均带来一致的性能提升。在 IntelligentBench 上，CoT 将得分从 44.9 进一步提升至 **55.3**（Table 8）。这些结果表明，BAGEL 的涌现推理能力可以通过显式的思维链提示被有效激活。

### 失败模式与局限

尽管整体表现强劲，BAGEL 在特定场景下仍存在明显不足（Figure 17）：

- **复杂文本渲染**：在需要精确渲染文字的场景中，生成质量下降明显。
- **特定 IP 生成**：涉及知名角色或品牌的内容生成存在困难。
- **反事实场景**：需要违背常识的编辑请求（如“让猫飞起来”）处理不佳。
- **对象交换与去模糊**：在精确替换对象或恢复模糊图像的任务上表现有限。

与 GPT-4o 相比，BAGEL 在这些挑战性场景上仍存在差距。作者指出，增加包含文本的图像数据、扩大模型容量或应用 RLHF 可能是解决这些问题的潜在方向，但目前尚未验证。

### 模型规模效应

Figure 16 展示了模型规模对生成质量的影响：更大的模型展现出更好的提示遵循能力和更高的图像质量。这暗示 MoT 架构具有良好的可扩展性，但具体的扩展规律仍需进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2505_14683/figures/005_Table_1.jpg]]
*Table 1: Data statistics for BAGEL. Since data are randomly sampled during pre-training, the dataset size does not directly correspond to the total number of seen tokens. Multimodal interleaved data is highlight in gray*

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

现有多模态统一模型（如 **EMU2**、**OmniGen**、**Janus-Pro 7B**）试图在单一模型中同时完成视觉理解和视觉生成任务，但普遍面临三个结构性瓶颈：

1. **信息瓶颈**：部分方法（如 External Diffuser 方案）依赖潜变量压缩来桥接理解与生成，导致跨模态信息传递受限，难以支持需要细粒度交互的复杂推理。
2. **任务冲突**：理解任务（优化交叉熵损失）和生成任务（优化均方误差损失）对参数更新方向存在竞争性需求，共享全部参数时难以同时达到最优。
3. **上下文交互不足**：传统架构缺乏对长序列交错多模态 token 的有效建模机制，限制了模型在需要多步推理的视觉编辑、世界建模等任务上的表现。

BAGEL 通过 Mixture-of-Transformers (MoT) 架构直接回应上述瓶颈：将理解专家和生成专家的参数完全解耦，同时保持共享自注意力，实现无瓶颈的长上下文跨模态交互。

### 2. 架构设计空间中的位置

从 Transformer 架构的谱系来看，BAGEL 的 MoT 设计位于以下方案的交叉点上：

- **Dense Transformer**：所有 token 共享全部参数，理解和生成任务在同一个参数空间中优化，任务冲突显著。
- **Mixture-of-Experts (MoE)**：仅复制前馈网络（FFN）作为多个专家，通过路由机制选择性激活。BAGEL 的消融实验（Figure 3）表明，MoE 在生成 MSE 损失和理解 CE 损失上均不及 MoT，因其参数解耦程度不足以缓解优化冲突。
- **MoT（BAGEL 方案）**：完全复制所有参数（包括注意力投影矩阵和 FFN）作为生成专家，与理解专家共享自注意力计算。这一设计使得两个专家可以独立优化各自的损失函数，同时通过共享注意力实现 token 级别的跨模态信息融合。

在视觉编码器层面，BAGEL 采用双编码器策略——SigLIP2 ViT + NaViT 用于语义理解，FLUX VAE 用于像素级生成——这与 **Janus-Pro** 等统一模型形成对比，后者通常使用单一编码器处理两种任务。

### 3. 与基线工作的关系

BAGEL 在以下维度上与现有工作形成对比：

| 维度 | 专用生成模型 | 现有统一模型 | BAGEL |
|------|-------------|-------------|-------|
| 代表工作 | **SD3-medium**、**FLUX.1-dev** | **Janus-Pro 7B**、**EMU2**、**OmniGen** | BAGEL |
| 架构 | 扩散模型专用架构 | 单一 Transformer 或 MoE | MoT（完全参数解耦 + 共享自注意力） |
| 理解能力 | 无 | 有，但与生成共享参数 | 有，独立专家优化 |
| 生成质量 | 高（GenEval 0.82） | 通常弱于专用模型 | 0.88（GenEval），超越 FLUX.1-dev |
| 推理编辑 | 不支持 | 有限 | 44.9（IntelligentBench），远超 Step1X-Edit 的 14.9 |

在视觉理解基准 MMMU 上，BAGEL 达到 55.3，较 Janus-Pro 的 41.0 提升 +14.3 个百分点（Table 4），表明参数解耦并未损害理解能力，反而通过大规模交错数据训练获得了增益。

在智能编辑任务 IntelligentBench 上，BAGEL（44.9）显著超越专用编辑模型 **Step1X-Edit**（14.9），差距达 +30.0（Table 8）。这验证了 MoT 架构在需要强多模态推理的复杂编辑任务上的优势。

与私有系统 **GPT-4o** 相比，BAGEL 在多个基准上仍有差距，但作为开源模型已展现出竞争力，特别是在 WISE 世界知识推理基准上，结合 Chain-of-Thought 推理后达到 0.70（Table 6）。

### 4. 适用边界与局限

BAGEL 的当前能力边界主要体现在以下方面（Figure 17 失败案例分析）：

- **特定 IP 生成**：在涉及受版权保护的特定角色、品牌标识等生成任务上表现不佳。
- **复杂文本渲染**：在图像中准确渲染长文本、特定字体或复杂排版时存在困难。
- **反事实场景**：对于需要违背常识或物理规律的图像编辑请求，模型难以合理响应。
- **对象交换与去模糊**：在需要精确保持身份特征的对象替换、以及低质量图像的去模糊任务上表现有限。
- **复杂人体姿态**：生成具有精确人体姿态控制的图像时，质量可能下降。

此外，模型生成图像的分辨率和视觉质量受限于 FLUX VAE 的潜空间压缩及训练分辨率。长上下文推理能力虽已涌现，但在某些需要多步组合推理的任务上仍不及 GPT-4o 等私有系统。

### 5. 开放问题

1. **架构扩展性**：MoT 架构如何随着参数规模（如扩展到 30B+）和数据规模（超过万亿 token）进一步扩展？专家数量的增加是否会引入新的路由或负载均衡挑战？

2. **评估体系**：如何更有效地评估需要强多模态推理和复杂任务组合的能力？现有基准（如 IntelligentBench、WISE）覆盖的任务类型仍有限。

3. **失败案例修复路径**：
   - 增加包含文本渲染、复杂人体姿态的图像数据能否改善对应任务？
   - 扩大模型容量或应用 RLHF/DPO 等偏好对齐技术能否解决当前失败案例？
   - 是否需要引入专门的文本渲染模块或姿态控制模块？

4. **推理能力深化**：Chain-of-Thought 推理已带来显著提升（IntelligentBench 从 44.9 到 55.3，Table 8），但如何进一步激发模型的推理能力——例如通过强化学习优化推理路径——仍是开放问题。

5. **安全与对齐**：当前训练流程未包含强化学习或对抗训练阶段，可能限制了模型在安全性、偏见控制和用户偏好对齐方面的表现。

## 原文 PDF

![[paperPDFs/arxiv_2025/BAGEL_Emerging_Properties_in_Unified_Multimodal_Pretraining.pdf]]
