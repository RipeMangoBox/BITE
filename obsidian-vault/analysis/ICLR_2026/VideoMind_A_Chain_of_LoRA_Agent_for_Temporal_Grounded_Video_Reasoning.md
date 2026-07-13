---
title: "VideoMind: A Chain-of-LoRA Agent for Temporal-Grounded Video Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/VideoMind_A_Chain_of_LoRA_Agent_for_Temporal_Grounded_Video_Reasoning.pdf
project_link: https://videomind.github.io/
code_link: null
openreview_forum_id: 57EwidOnSf
aliases:
- VideoMind
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "提出多角色代理工作流以及高效的角色切换机制 (Chain-of-LoRA)，使模型能够像人类一样分解任务、定位、验证并回答，从而显著提升时间锚点推理。"
primary_logic: "将视频推理分解为规划、定位、验证和回答四个可组合的角色，并通过共享骨干加低秩适配器实现轻量级、灵活的角色切换，在最小计算开销下获得了精准的时间锚点能力。"
claims:
- "VideoMind-2B 在 CG-Bench 的 mIoU 和 rec.@IoU 上超越 GPT-4o 和 Gemini-1.5-Pro。"
- "Chain-of-LoRA 在实现高性能的同时，内存消耗仅为分布式方法的 1/4。"
- "添加验证器使 2B 模型的 Charades-STA R@0.7 相对提升 18.5%，mIoU 提升 7.4%。"
- "Planner 在视频+问题输入下达到 93% 的计划准确率，证明角色调度的可靠性。"
---

# VideoMind: A Chain-of-LoRA Agent for Temporal-Grounded Video Reasoning

> [!tip] 核心洞察
> 将视频推理分解为规划、定位、验证和回答四个可组合的角色，并通过共享骨干加低秩适配器实现轻量级、灵活的角色切换，在最小计算开销下获得了精准的时间锚点能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VideoMind：用于时间锚点视频推理的LoRA链式代理 |
| 英文题名 | VideoMind: A Chain-of-LoRA Agent for Temporal-Grounded Video Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=57EwidOnSf) · [Project](https://videomind.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VideoMind |
| Dataset | CG-Bench, ReXTime, NExT-GQA, Charades-STA |

> [!tip] 效果简介
> - CG-Bench 上，mIoU 为 7.10 (7B)，对比 5.62 (GPT-4o)，变化 +1.48。
> - ReXTime 上，Acc@IoU 为 20.20 (7B, zero-shot)，对比 17.13 (VTimeLLM 7B, fine-tuned)，变化 +3.07。
> - NExT-GQA 上，R@0.3 IoU 为 50.2 (7B)，对比 41.2 (VideoChat-TPO 7B)，变化 +9.0。

## 概要

### 问题瓶颈

当前视频语言模型在处理长视频时面临一个核心瓶颈：缺乏**精确的时间定位能力**与**可解释的逐步推理机制**。现有方法通常直接生成文本答案，难以在数十分钟甚至更长的视频中准确锚定与查询相关的关键时刻，也无法追溯其推理过程。这一缺陷在需要时间锚点的视频问答（Grounded VideoQA）和时间定位（Temporal Grounding）任务中尤为突出。

### 核心思路

VideoMind 提出了一种**基于角色的代理工作流**，将复杂的视频推理任务分解为四个可组合的专门角色：

- **Planner（规划器）**：根据视频和查询动态协调其他角色，生成 JSON 格式的执行计划。
- **Grounder（定位器）**：配备专用的时间戳解码器，在视频中定位相关时刻并生成多个候选片段。
- **Verifier（验证器）**：通过 Zoom-in 机制对候选时刻进行二分类评估，筛选出最佳匹配片段。
- **Answerer（回答器）**：基于选定的视频片段生成最终的自然语言答案。

为使多角色切换既高效又灵活，VideoMind 引入了 **Chain-of-LoRA** 机制：所有角色共享同一个基座模型，仅通过切换不同的低秩适配器（LoRA）来激活不同角色。这一设计避免了多模型独立部署的巨大内存开销，在测试时实现了轻量级的角色链式调用。

### 主要结果

VideoMind 在多个基准上展现了显著的性能优势：

- **时间锚点视频问答**：在 CG-Bench 上，VideoMind-7B 的 mIoU 达到 7.10，超越 GPT-4o（5.62）和 Gemini-1.5-Pro；在 ReXTime 上，零样本性能（20.20 Acc@IoU）即超过微调后的 VTimeLLM（17.13）。
- **时间定位**：在 Charades-STA 上 R@0.3 达到 73.5，较 LLaVA-ST 提升 10.4 个百分点；在 NExT-GQA 上 R@0.3 IoU 达到 50.2，较 VideoChat-TPO 提升 9.0 个百分点。
- **通用视频问答**：在 MLVU 和 LVBench 上分别达到 64.4 和 40.8，均显著优于 LongVA、GPT-4o 和 Gemini-1.5-Pro 等强基线。
- **效率优势**：Chain-of-LoRA 在实现最优性能的同时，GPU 内存消耗仅为全分布式多模型方案的 1/4。

### 方法定位

VideoMind 属于**多模态代理推理**方法，其核心创新在于将视频推理形式化为可解释的角色链，并通过共享骨干加 LoRA 适配器实现高效的角色切换。该方法在时间锚点推理能力上显著超越了传统的单一模型直接生成范式，为长视频理解提供了一种结构化、可追溯的推理框架。



视频理解正从简单的场景分类走向复杂的时序推理。当用户提出“厨师是在什么时候往锅里加盐的？”这类问题时，模型不仅要理解画面内容，还需要在分钟级甚至小时级的长视频中，精确地锚定事件发生的起止时刻，并给出可解释的推理过程。这种能力被称为**时间锚点视频推理**（temporal-grounded video reasoning），是通往通用视频智能的关键一步。

### 现有方法的瓶颈

当前主流的视频语言模型（LMMs），无论是闭源的 **GPT-4o**、**Gemini-1.5-Pro**，还是开源的 **Video-LLaVA**、**TimeChat**、**VideoChat-TPO**、**LongVA** 等，在处理此类任务时普遍存在两个结构性缺陷：

1. **缺乏精确的时间定位能力**：大多数模型将时间戳建模为离散的文本 token 或特殊标记，通过语言模型的生成过程间接预测。这种“文本化”的时间表示本质上丢失了时间的连续性，导致定位精度不足。少数工作尝试引入专用定位头，但往往与语言推理过程割裂，难以在协同推理中发挥作用。

2. **缺乏可解释的逐步推理**：现有模型通常以端到端的方式直接从视频和问题映射到答案，如同一个黑箱。当面对需要多步逻辑、跨时间段比较的复杂查询时，单一前向传播难以可靠地完成“定位→验证→回答”的认知链条。长视频中大量无关片段的干扰进一步加剧了这一问题，模型容易在错误的时间锚点上产生幻觉。

### 核心洞察与本文动机

人类在面对复杂视频推理时，会自然地采取分而治之的策略：先规划需要查找哪些事件，再定位候选时刻，接着仔细验证哪个片段最匹配，最后基于确认的片段给出答案。这一认知过程启发我们：**能否让一个模型模拟这种多角色协作的工作流，同时保持轻量和高效？**

VideoMind 的核心动机正是弥合这一差距。我们识别出时间锚点推理所需的四项关键能力——**规划**（Planning）、**定位**（Grounding）、**验证**（Verification）和**回答**（Answering），并将它们建模为一个可组合的代理工作流。然而，直接部署多个独立模型会带来沉重的计算和内存开销。为此，我们提出 **Chain-of-LoRA 机制**：在共享的骨干网络上，通过切换不同的低秩适配器（LoRA）来激活不同角色，实现无缝的角色切换。这一设计使得 VideoMind 在仅增加极少参数的条件下，获得了结构化、可解释的逐步推理能力，为长视频时间锚点推理提供了一种高效且灵活的新范式。



## 核心方法与创新机理

### 1. 瓶颈洞察：从“直接回答”到“时间锚点推理”

当前视频语言模型（LMM）在处理长视频时面临一个根本性瓶颈：模型通常被训练为端到端地直接生成答案，缺乏对视频时间结构的显式建模。这导致两个关键缺陷：

- **时间定位不精确**：模型难以在数十分钟的长视频中准确定位与问题相关的短时刻，只能依赖粗略的全局上下文进行“猜测”。
- **推理过程不可解释**：单一前向传播无法展示模型如何从视频中检索证据、验证假设并得出结论，使得错误难以追溯和修正。

VideoMind 的核心洞察在于：**将视频推理显式分解为规划、定位、验证和回答四个可组合的角色**，模拟人类在回答时间敏感问题时的逐步推理过程。这一分解使模型能够像人类一样，先规划需要查找什么，再定位候选时刻，验证其相关性，最后基于确认的证据生成答案。

### 2. 关键机制：Chain-of-LoRA 角色切换

传统多角色系统通常需要部署多个独立模型（每个角色一个完整模型副本），导致显存开销随角色数量线性增长。VideoMind 提出了 **Chain-of-LoRA** 机制，从根本上改变了这一范式：

- **共享骨干网络**：所有角色（Planner、Grounder、Verifier、Answerer）共享同一个 LMM 基座模型（基于 Qwen2-VL 架构）。
- **LoRA 适配器切换**：每个角色仅通过独立的低秩适配器（LoRA）进行差异化，推理时由 Planner 动态调度，按需激活对应的 LoRA 权重。
- **效率优势**：相比分布式部署（需 4 份完整权重），Chain-of-LoRA 在保持最高性能的同时，峰值 GPU 显存消耗仅为前者的约 1/4（Table 7）。

这种设计实现了**灵活性与效率的最优平衡**：模型可以在测试时按需切换角色，而无需加载多个完整模型。

### 3. 时间定位机制革新：Timestamp Decoder

传统方法通常将时间定位简化为离散的文本时间戳预测或特殊 token 分类，精度受限于离散化粒度。VideoMind 的 Grounder 角色引入了专用的 **timestamp decoder**，实现了连续时间回归：

- **特征金字塔**：从压缩后的帧嵌入构建四层时间特征金字塔，通过 Conv1D → LayerNorm → SiLU 逐层下采样，捕获多尺度时间上下文（Table 20 表明四层金字塔比单层在 Charades-STA 上提升 3.89 mIoU）。
- **连续回归**：当 LLM 生成 `<REG>` token 时，timestamp decoder 接收该 token 及所有视觉 token 的隐藏状态，直接回归预测连续的开始和结束时间戳 `[t_start, t_end]`。
- **多损失联合优化**：结合 Focal Loss（帧级前景/背景分类）、L1 Loss（边界回归）和对比损失（帧-查询对齐），确保定位的精确性和语义相关性。

消融实验（Table 18）证实，timestamp decoder 在所有指标上显著优于文本时间戳、特殊 token 分类、嵌入匹配和时间标记等替代方案。

### 4. 验证机制的引入：Zoom-in Verifier

即使 Grounder 能生成多个候选时刻，如何从中选出最佳片段仍是一个关键挑战。VideoMind 引入了 **Verifier** 角色，采用“放大镜”策略：

- **边界扩展**：对每个候选时刻，将边界向两侧各扩展 50%，裁剪出扩大的视频片段。
- **特殊标记**：使用 `<SEG-START>` 和 `<SEG-END>` 标记显式标注片段边界，使模型能聚焦于精确的时刻内容。
- **二分类判断**：Verifier 对每个候选片段进行相关性判断，选出最佳匹配。

这一机制的效果显著：在 Charades-STA 上，添加 Verifier 使 2B 模型的 R@0.7 相对提升 18.5%，mIoU 提升 7.4%，且 32.9% 的样本的定位 IoU 得到了改善（Table 22）。Table 21 进一步表明，特殊标记样式在 R@0.5 上达到 51.05，优于直接判断、扩展判断和文本描述等替代方案。

### 5. 自适应规划：Planner 的任务调度

VideoMind 的 Planner 角色是整个系统的“大脑”，负责根据视频和查询内容动态决定需要激活哪些角色及执行顺序：

- **JSON 函数调用**：Planner 以结构化 JSON 格式输出调度指令（`{"type": "<role>", "value": "<argument>"}`），确保下游角色的输入规范。
- **三种推理计划**：支持直接回答、定位-回答、定位-验证-回答三种模式，根据查询复杂度自适应选择。
- **高可靠性**：在同时输入视频和问题时，Planner 的计划准确率达到 93%（Table 23），证明视频和文本联合上下文对任务调度至关重要。

### 6. 创新总结

| 创新维度 | 基线方法 | VideoMind 方案 | 核心优势 |
|---------|---------|---------------|---------|
| 推理架构 | 单一 LMM 直接生成答案 | 多角色代理工作流（Planner → Grounder → Verifier → Answerer） | 可解释的逐步推理，错误可追溯 |
| 时间定位 | 文本或特殊 token 离散化预测 | Timestamp decoder + 特征金字塔连续回归 | 精确定位，多尺度时间建模 |
| 角色切换 | 单一权重或多模型独立部署 | Chain-of-LoRA 共享骨干 + LoRA 切换 | 显存消耗降至 1/4，灵活性与效率兼得 |
| 验证机制 | 无验证或仅基于原始片段判断 | Zoom-in Verifier + 特殊标记 + 边界扩展 | 显著提升定位精度，32.9% 样本 IoU 改善 |

这些创新共同构成了一个**轻量、灵活且精确的时间锚点视频推理框架**，使 2B 参数的小模型在多個长视频基准上超越 GPT-4o 和 Gemini-1.5-Pro 等大规模闭源模型。



![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_57EwidOnSf/figures/004_Figure_2.jpg]]
*Figure 2: The overall workflow of VideoMind. Given a video and a query, it adaptively activates different roles (e.g., Planner → Grounder → Verifier → Answerer in this case) and performs step-by-step reasoning by calling individual modules. Figure 3: Planner coordinates all the other roles based on the video and query context, offering three reasoning plans and a query rephrasing mechanism to address diverse demands*

VideoMind 是一个多角色代理工作流，旨在赋予视频语言模型精确的时间锚点推理能力。其核心思想是将复杂的视频推理任务分解为四个可组合的专门角色——规划器（Planner）、定位器（Grounder）、验证器（Verifier）和回答器（Answerer）——并通过一种轻量级的角色切换机制 Chain-of-LoRA 将它们串联起来。

### 系统架构

整个框架建立在共享的 LMM 骨干网络之上，该骨干网络源自 Qwen2-VL 架构，包含一个 LLM 主干和一个支持动态分辨率输入的 ViT 视觉编码器。四个角色共享同一个骨干网络，但各自配备独立的 LoRA 适配器。此外，定位器独享一个专用的时间戳解码器（Timestamp Decoder），用于执行精确的时间边界预测。

图 2 展示了 VideoMind 的整体工作流程。给定一个视频和一个查询，系统首先由规划器根据视频和查询的上下文，动态协调后续角色的调用顺序。规划器生成一个 JSON 格式的执行计划，指定需要激活的角色及其参数。随后，定位器识别并定位与查询相关的视频片段，生成多个候选时刻。验证器通过“放大观察”（Zoom-in）策略对候选时刻进行评估和筛选，选出最佳匹配片段。最后，回答器基于选定的视频片段或完整视频生成最终的自然语言回答。

### 角色协调与数据流

四个角色的职责与交互关系如下：

- **规划器（Planner）**：作为工作流的调度中心，规划器接收视频和查询输入，生成 JSON 格式的函数调用对象 `{"type": "<role>", "value": "<argument>"}`，动态决定激活哪些角色及其执行顺序。规划器提供三种推理计划并具备查询改写机制，以应对多样化的推理需求（图 3）。实验表明，在同时输入视频和问题时，规划器的计划准确率达到 93%（表 23），证明了角色调度的可靠性。

- **定位器（Grounder）**：当规划器调用定位器时，定位器通过专用的时间戳解码器定位相关视频时刻。其工作流程包括：将视觉标记压缩为每帧一个标记（1D 平均池化），构建四层时间特征金字塔，通过 Transformer 编码器融合帧嵌入与查询嵌入，最终在生成 `<REG>` 标记时输出开始和结束时间戳。定位器可以生成多个候选时刻供验证器进一步筛选。

- **验证器（Verifier）**：验证器对定位器生成的候选时刻进行二分类评估。它采用 Zoom-in 策略，将每个候选片段的边界向两侧扩展 50%，并对扩展后的片段进行时间裁剪。验证器使用特殊标记 `<SEG-START>` 和 `<SEG-END>` 显式标记片段边界，然后判断该片段是否与查询匹配，最终选出最佳候选。

- **回答器（Answerer）**：回答器基于验证器选定的视频片段（或完整视频）生成最终的自然语言回答。回答器使用标准的多模态对话格式，将视频和问题作为输入，输出答案文本。

### Chain-of-LoRA：高效的角色切换机制

Chain-of-LoRA 是实现多角色无缝切换的关键技术。与传统的多模型独立部署或单一权重方案不同，Chain-of-LoRA 让所有角色共享同一个 LMM 骨干网络，仅通过切换不同的 LoRA 适配器来激活不同角色。在推理时，框架根据规划器的指令动态加载对应的 LoRA 权重，实现角色间的灵活切换。

这种设计在效率与灵活性之间取得了平衡。如表 7 所示，Chain-of-LoRA 在 Video-MME 上达到 55.4 的整体准确率和 46.3 的长视频准确率，而峰值 GPU 内存消耗仅为分布式方法的 1/4。相比之下，将多个角色独立部署为多个模型会带来显著的内存开销，而将所有能力压缩到单一权重中则会导致性能下降。

### 训练策略

各角色采用独立训练的方式，使用不同的数据集（表 1）。规划器在 39K 样本上训练规划与查询改写能力；定位器在 210K 样本上训练时间定位能力；验证器则利用重新标注的公共基准数据进行训练。所有角色均基于相同的预训练 LMM 骨干，仅训练各自新增的 LoRA 适配器和定位器专属的时间戳解码器。

### 当前局限

尽管 VideoMind 在时间锚点推理上取得了显著进展，但框架仍存在以下局限：各角色当前独立训练，未进行联合优化，推理管道中存在误差传播的风险；音频模态未被整合，限制了对需要听觉理解的视频的支持；顺序执行多角色会引入额外延迟，尽管自动规划可部分缓解，但对长视频仍可能成为瓶颈。



VideoMind 的推理能力由四个功能独立的角色模块构成，它们共享同一个 LMM 骨干网络，并通过 Chain-of-LoRA 机制实现轻量级的角色切换。以下聚焦于 Grounder 模块的核心架构与训练目标，因为它是实现精确时间锚点的关键所在。

### Grounder 的时间戳解码器

Grounder 的角色是在长视频中定位与查询相关的时刻。其核心是一个专用的 timestamp decoder，该解码器接收 LLM 产生的视觉和文本隐藏状态，并输出连续的时间边界。具体流程如下：

**视觉标记压缩**：为降低计算量，首先将 ViT 编码器输出的视觉标记 $\mathbf{h}_v$ 沿空间维度进行 1D 平均池化，将每一帧压缩为一个标记：

$$\mathbf{h}_v' = \mathrm{AvgPool}(\mathbf{h}_v) \in \mathbb{R}^{T \times D_L}$$

其中 $T$ 为帧数，$D_L$ 为 LLM 的隐藏层维度。

**特征投影与融合**：压缩后的帧特征 $\mathbf{h}_v'$ 和查询的文本特征 $\mathbf{h}_r$ 分别通过线性层 $E_v$ 和 $E_r$ 投影到较小的维度 $D$：

$$\mathbf{e}_v = E_v(\mathbf{h}_v') \in \mathbb{R}^{T \times D}, \quad \mathbf{e}_r = E_r(\mathbf{h}_r) \in \mathbb{R}^{1 \times D}$$

随后，帧嵌入与查询嵌入被送入一个 Transformer 编码器进行跨模态融合，并加入可学习的模态指示符 $\mathbf{m}_v, \mathbf{m}_r$ 和位置编码 $\mathbf{e}_p$：

$$[\mathbf{e}_v'; \mathbf{e}_r'] = \mathrm{Transformer}([\mathbf{e}_v + \mathbf{m}_v + \mathbf{e}_p; \mathbf{h}_r + \mathbf{m}_r])$$

**时间特征金字塔**：为捕捉不同时间尺度的事件，融合后的帧嵌入 $\mathbf{e}_v'$ 被送入一个四层的时间特征金字塔。每一层由一个 Conv1D → LayerNorm → SiLU 块构成，Conv1D 的卷积核大小和步长均为 2，从而逐层降低时间分辨率并扩大感受野。消融实验证实，四层金字塔在 Charades-STA 上相比单层结构提升了 3.89 mIoU (Table 20)。

**时刻边界回归**：当 LLM 在生成过程中输出特殊的 `<REG>` 标记时，该标记的最后一层隐藏状态与所有视觉标记的隐藏状态一同被送入 timestamp decoder。Decoder 的每一层对每一帧预测三个量：
- 前景/背景置信度得分 $\hat{c}_i$
- 相对于当前帧的开始边界偏移量 $\hat{b}_i^s$
- 结束边界偏移量 $\hat{b}_i^e$

最终的预测时刻由所有层的结果聚合得出，形式为 $[t_{start}, t_{end}]$。

### 损失函数设计

Timestamp decoder 的训练由三个损失项联合驱动，作用于金字塔的每一层：

**Focal Loss 用于帧级分类**：解决正负帧严重不均衡的问题，促使模型准确区分前景帧与背景帧：

$$\mathcal{L}_{cls} = -\lambda_{cls} \alpha (1 - \hat{c}_i)^\gamma \log(\hat{c}_i)$$

其中 $\lambda_{cls}=5.0$ 为损失权重，$\alpha$ 和 $\gamma$ 为 Focal Loss 的标准超参数。

**L1 Loss 用于边界回归**：直接回归预测边界与真实边界之间的绝对偏差：

$$\mathcal{L}_{reg} = \lambda_{reg} (|b_i^s - \hat{b}_i^s| + |b_i^e - \hat{b}_i^e|)$$

其中 $\lambda_{reg}=1.0$ 为回归损失权重，$b_i^s, b_i^e$ 为真实的边界偏移量。

**对比损失用于帧-查询对齐**：鼓励真正的正样本帧与查询之间的相似度 $s_p$ 高于其他帧，增强跨模态对齐的判别力：

$$\mathcal{L}_{con} = -\lambda_{con} \log \frac{\exp(s_p / \tau)}{\exp(s_p / \tau) + \sum_{i \in \Theta} \exp(s_i / \tau)}$$

其中 $\lambda_{con}=0.05$，温度系数 $\tau=0.07$，$\Theta$ 为相似度超过 $s_p$ 的帧索引集合。

三个损失项在所有金字塔层上求和，构成 Grounder 的最终训练目标。消融实验表明，这一专用的 timestamp decoder 设计在 Charades-STA 上全面优于基于文本、特殊 token、嵌入匹配和时间标记等替代方案 (Table 18)，是 VideoMind 实现精准时间锚点的核心机制。



## 实验与关键发现

### 核心瓶颈与因果机制

当前视频推理方法的核心瓶颈在于缺乏精确的时间定位能力与可解释的逐步推理机制，尤其在长视频中处理复杂时间关系时表现乏力。VideoMind 通过引入多角色代理工作流，将视频推理分解为**规划（Planner）、定位（Grounder）、验证（Verifier）和回答（Answerer）**四个可组合的角色，并通过 **Chain-of-LoRA** 机制实现轻量级、灵活的角色切换，从而在最小计算开销下获得精准的时间锚点能力。

### 主实验结果

#### 时间锚点视频问答（Grounded VideoQA）

在 CG-Bench 上（Table 2），VideoMind-2B 在 mIoU 和 rec.@IoU 指标上超越了 GPT-4o 和 Gemini-1.5-Pro，7B 版本进一步将 mIoU 提升至 7.10（相较于 GPT-4o 的 5.62，提升 +1.48），并在 clue-grounded QA 的 acc.@IoU 上取得新 SOTA。在 ReXTime 上（Table 3），VideoMind-7B 在 zero-shot 设置下 Acc@IoU 达到 20.20，超越微调后的 VTimeLLM 7B（17.13），提升 +3.07。在 NExT-GQA 上（Table 4），7B 模型的 R@0.3 IoU 达到 50.2，显著优于 VideoChat-TPO 7B 的 41.2（+9.0）。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_57EwidOnSf/figures/008_Table_2.jpg]]
*Table 2: Performance comparison on Grounded VideoQA on CG-Bench (Chen et al., 2024a)*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_57EwidOnSf/figures/010_Table_4.jpg]]
*Table 4: Performance comparison on Grounded VideoQA on NExT-GQA (Xiao et al., 2024)*

#### 视频时间定位（Video Temporal Grounding）

在 Charades-STA 上（Table 5），VideoMind-7B 在 R@0.3 上达到 73.5，较 LLaVA-ST 7B 的 63.1 提升 +10.4；在 QVHighlights 上微调后同样取得 SOTA（Table 13）。在 ActivityNet-RTL 推理时间定位任务上（Table 14），zero-shot 的 VideoMind-7B 大幅超越微调后的 LITA-13B。

#### 通用视频问答（General VideoQA）

在 MLVU 上（Table 6），VideoMind-7B 的 M-Avg 达到 64.4，较 LongVA 7B 的 56.3 提升 +8.1。在 LVBench 上（Table 6），7B 模型的 Overall 达到 40.8，超越 Gemini-1.5-Pro 的 33.1（+7.7）。在 Video-MME 上（Table 7），Chain-of-LoRA 取得 55.4 All / 46.3 Long 的性能。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_57EwidOnSf/figures/014_Table_7.jpg]]
*Table 7: Performance and efficiency comparison of different test-time scaling and role integration strategies. Mem indicates the peak GPU memory consumption. Notably, Chain-of-LoRA achieves the best performance with minimal memory cost. Table 8: Effects of individual roles. A, G, V, P, G% denote the answerer, grounder, verifier, planner, and the percentage of samples processed with the grounder, respectively*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_57EwidOnSf/figures/012_Table_6.jpg]]
*Table 6: Performance comparison on General VideoQA on Video-MME (Fu et al., 2024a), MLVU (Zhou et al., 2024), and LVBench (Wang et al., 2024c)*

### Chain-of-LoRA 效率分析

Table 7 的关键结论：Chain-of-LoRA 在实现最佳性能的同时，内存消耗仅为全分布式方法（需 4× 权重副本）的约 1/4（4.2G vs 16.8G）。相较于单任务联合训练，Chain-of-LoRA 在 NExT-GQA（28.6 mIoU）、Charades-STA（51.1 mIoU）和 Video-MME（55.4 All）上均取得最优结果，在效果与效率之间达到最佳平衡。

### 消融实验

#### 各角色贡献

Table 8 的消融表明：添加 Grounder 后 NExT-GQA mIoU 提升显著；进一步添加 Verifier 使 Charades-STA mIoU 额外提升 3.2；Planner 的自动调度使 Grounder 仅需处理 48% 的样本，在保持性能的同时降低计算开销。

#### 时间戳建模方案

Table 18 表明，Timestamp decoder 在所有指标上显著优于文本、特殊 token、嵌入匹配和时间标记等替代方案，验证了连续时间回归设计的优越性。

#### 时间特征金字塔

Table 20 显示，四层时间特征金字塔在 Charades-STA 上较单层方案提升 3.89 mIoU，证明多尺度时间建模对精确定位至关重要。

#### 验证器设计

Table 21 比较了不同验证器样式：采用 Special Token（<SEG-START>/<SEG-END>）的方案在 Charades-STA 上 R@0.5 达 51.05，超越 Direct、Expand 和 Textual 样式。Table 22 进一步表明，添加 Verifier 使 2B 模型的 Charades-STA R@0.7 相对提升 18.5%，mIoU 提升 7.4%，IoU 提高样本占比达 32.9%，充分验证了 Zoom-in 验证机制的有效性。


![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_57EwidOnSf/figures/035_Table_22.jpg]]
*Table 22: Effect of the verifier on Charades-STA (Gao et al., 2017). IoU Raise means the percentage of the samples whose grounding IoU is raised by the verifier*

#### Planner 调度准确性

Table 23 显示，Planner 在同时输入视频和问题时达到 93% 的正确规划准确率，证明视频和文本联合上下文对任务调度至关重要。

### 失败模式分析

Table 19 和 Figure 7 揭示了不同模型规模的错误分布：2B 模型的 Grounding 错误占比较高，而 7B 模型的 Planning 和 Answering 错误相对突出。Figure 8 进一步表明，Grounding IoU 与最终 QA 准确率之间存在强相关性，说明定位质量是整体性能的关键瓶颈。

### 局限性

1. **误差传播**：当前各角色独立训练，未进行联合优化，推理管道存在误差传播风险。
2. **音频缺失**：音频模态未被整合，限制了对需要听觉理解的视频的支持。
3. **推理延迟**：顺序执行多角色引入额外延迟，对长视频可能成为瓶颈（Table 24 显示 CG-Bench 平均推理时间对比）。
4. **泛化边界**：在 Ego4D-NLQ 等特定域数据集上，zero-shot 性能与专用方法仍有差距（Table 12）。



## 定位与知识库关联

### 任务定位与核心瓶颈

VideoMind 聚焦于**时间锚点视频推理**（Temporal-Grounded Video Reasoning），该任务要求模型不仅理解视频语义，还需精确地定位与查询相关的视频片段。当前主流范式存在两个根本性瓶颈：其一，现有视频大语言模型（Video LMM）通常直接端到端生成答案，缺乏可解释的逐步推理能力，难以处理长视频中的复杂时间关系；其二，时间定位机制普遍采用文本离散化或特殊 token 预测时间戳，精度不足且无法有效利用视频的连续时间结构。

### 方法谱系与差异化对比

VideoMind 在以下维度上与代表性基线方法形成差异化：

| 维度 | 基线方法 | VideoMind 的改进 |
|------|---------|-----------------|
| **推理架构** | 单一 LMM 直接生成答案（如 **GPT-4o**、**Gemini-1.5-Pro**、**Video-LLaVA**） | 多角色代理工作流（Planner → Grounder → Verifier → Answerer），模拟人类分步推理 |
| **时间定位** | 文本或特殊 token 离散化预测（如 **TimeChat**、**VideoChat-TPO**） | 专用 timestamp decoder + 四层时间特征金字塔的连续时间回归 |
| **角色管理** | 单一权重或多模型独立部署 | Chain-of-LoRA：共享骨干网络 + LoRA 适配器按需切换，内存仅为分布式方法的 1/4 |
| **验证机制** | 无验证或仅基于原始片段判断 | Zoom-in 验证器，利用特殊标记（`<SEG-START>`/`<SEG-END>`）和边界扩展（50%）评估候选时刻 |

具体而言：

- **与通用视频 LMM 对比**：**LongVA**、**InternVL2**、**LLaVA-OneVision** 等模型在通用视频问答上表现良好，但缺乏专门的时间定位能力。VideoMind 通过独立的 Grounder 角色实现了精确的时刻检索，在 Charades-STA 上 R@0.3 达到 73.5（7B），远超 **LLaVA-ST**（63.1）。

- **与时间锚点视频 LMM 对比**：**TimeChat** 和 **VideoChat-TPO** 虽具备时间定位能力，但采用文本离散化方式预测时间戳，精度受限。VideoMind 的 timestamp decoder 在所有指标上显著优于文本、特殊 token、嵌入匹配和时间标记等方案（Table 18），在 NExT-GQA 上 R@0.3 IoU 达到 50.2，较 VideoChat-TPO 的 41.2 提升 9.0 个点。

- **与闭源大模型对比**：VideoMind-2B 在 CG-Bench 的 mIoU 和 rec.@IoU 上超越 **GPT-4o** 和 **Gemini-1.5-Pro**（Table 2），在 LVBench 上 7B 模型以 40.8 超越 Gemini-1.5-Pro 的 33.1，证明了小模型在结构化推理框架下的潜力。

### Chain-of-LoRA 的角色切换机制

Chain-of-LoRA 是 VideoMind 的核心效率创新。其技术方案为：所有角色共享同一个 LMM 骨干网络（基于 **Qwen2-VL** 架构），每个角色仅训练独立的低秩适配器（LoRA）。推理时，Planner 根据查询动态生成 JSON 格式的函数调用（`{"type": "<role>", "value": "<argument>"}`），框架据此激活对应的 LoRA 适配器，实现无缝角色切换。

这一设计的关键优势在于：
- **内存高效**：仅需维护一份骨干权重和多组轻量 LoRA 参数，峰值 GPU 内存消耗仅为分布式部署（4× 权重副本）的 1/4（Table 7）。
- **性能无损**：在 NExT-GQA、Charades-STA 和 Video-MME 三个基准上，Chain-of-LoRA 均取得最佳综合性能，超越单模型多任务训练和全分布式方案。
- **灵活扩展**：新增角色仅需训练新的 LoRA 适配器，无需修改骨干网络。

### 适用边界与局限

尽管 VideoMind 在多个基准上取得了领先结果，其设计仍存在以下边界条件：

1. **独立训练与误差传播**：各角色当前独立训练，未进行端到端联合优化。Planner 的规划准确率虽达 93%（Table 23），但规划错误仍会导致后续 Grounder 和 Verifier 在错误方向上工作，形成误差级联。

2. **音频模态缺失**：当前框架仅处理视觉和文本模态，未整合音频信息。对于需要听觉理解的任务（如对话理解、环境音推理），模型能力受限。

3. **顺序执行的延迟开销**：多角色顺序调用引入了额外推理延迟。尽管自动规划可跳过不必要的角色调用（如简单问题直接由 Answerer 回答），但对于需要完整 Planner → Grounder → Verifier → Answerer 链的长视频，延迟仍可能成为瓶颈。

4. **长视频处理的帧数限制**：受限于 1 FPS 采样和最大 150 帧的设定，对于超长视频（如数小时监控视频），信息密度与时序分辨率之间存在权衡。

### 开放问题

基于上述局限，以下方向值得进一步探索：

- **多角色联合优化**：能否设计端到端的训练策略，使 Planner、Grounder、Verifier 和 Answerer 在统一的损失函数下协同优化，从根本上缓解误差传播？
- **音频模态融合**：如何将音频编码器及其对应的 LoRA 适配器高效地融入 Chain-of-LoRA 框架，而不破坏现有的角色切换机制？
- **实时推理扩展**：Chain-of-LoRA 机制能否通过模型量化、投机解码或角色并行化等技术，扩展到实时或近实时的视频推理场景？
- **开放域泛化**：该框架在更复杂、开放域的长视频（如未经剪辑的日常生活视频、多视角视频）上的泛化能力尚待验证。
- **更细粒度的角色分解**：是否可以将现有四角色进一步分解为更多原子能力（如对象跟踪器、关系推理器），以应对更复杂的组合查询？



## 原文 PDF

![[paperPDFs/ICLR_2026/VideoMind_A_Chain_of_LoRA_Agent_for_Temporal_Grounded_Video_Reasoning.pdf]]
