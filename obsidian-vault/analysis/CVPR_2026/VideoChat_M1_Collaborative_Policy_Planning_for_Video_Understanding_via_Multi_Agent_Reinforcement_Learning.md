---
title: "VideoChat-M1: Collaborative Policy Planning for Video Understanding via Multi-Agent Reinforcement Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VideoChat_M1_Collaborative_Policy_Planning_for_Video_Understanding_via_Multi_Agent_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- VM
- VideoChat-M1
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入多智能体协同策略规划（CPP）范式，让多个智能体动态生成、执行并通信调用策略，基于同伴上下文灵活更新方案；同时通过多智能体强化学习（MARL）联合优化最终答案奖励和中间协作过程反馈，使智能体团队能够稳定、高效地探索丰富的视频线索。
primary_logic: 多智能体通过迭代策略生成-执行-通信，实现“群体智能”探索，打破单一固定策略的局限；MARL训练稳定了协作过程，赋予智能体自主优化协同行为的能力，从而在多种复杂视频理解任务上显著超越已有方法，并且该增益来源于协同学习框架本身，而非特定强工具。
claims:
- VideoChat-M1 在八个主流基准上全面达到最优，在 LongVideoBench 上比 GPT-4o 高 15.6%，比 Gemini 2.5 Pro 高 3.6%。
- 多智能体强化学习的完整配置（包含结果奖励、格式奖励、协作奖励及 Agent Dropout）在 Video-Holmes 和 LongVideoBench 上分别达到 60.5 和 82.3，且去除任意组件均导致性能下降，其中 Agent Dropout 是最关键的规范化器。
- 即使将专用的空间工具替换为通用视觉骨干（Qwen2.5-VL-7B），VideoChat-M1 仍保持最优性能，比巨型模型 InternVL-3.5-241B 高出 34.2%，证实效果源于 CPP 框架而非特定工具。
- 37B 的智能体团队在 VideoMMMU 上取得了与 235B 的 Qwen3-VL 相当的效果，参数效率极高。
---

# VideoChat-M1: Collaborative Policy Planning for Video Understanding via Multi-Agent Reinforcement Learning

> [!tip] 核心洞察
> 多智能体通过迭代策略生成-执行-通信，实现“群体智能”探索，打破单一固定策略的局限；MARL训练稳定了协作过程，赋予智能体自主优化协同行为的能力，从而在多种复杂视频理解任务上显著超越已有方法，并且该增益来源于协同学习框架本身，而非特定强工具。

| 字段 | 内容 |
|------|------|
| 中文题名 | VideoChat-M1：基于多智能体强化学习的协同策略规划视频理解 |
| 英文题名 | VideoChat-M1: Collaborative Policy Planning for Video Understanding via Multi-Agent Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19524) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VideoChat-M1 |
| Dataset | LongVideoBench, Charades-STA, Video-Holmes, VideoMME |

> [!tip] 效果简介
> - LongVideoBench 上，Accuracy 82.3 vs GPT-4o (66.7) (+15.6)。
> - Charades-STA 上，mIoU 67.7 vs Seed 1.5VL (64.7) (+3.0)。
> - Video-Holmes 上，Accuracy 60.5 vs Best foundation LLM agent group (56.2) (+4.3)。

## 概述

视频理解正从单模型端到端处理向智能体驱动的工具调用范式演进。然而，现有基于智能体的方法普遍采用**静态、不可学习的单一固定工具调用策略**，难以自适应地发现时空复杂视频中不同时间尺度上的多样化线索，导致感知和推理能力不足。

针对这一瓶颈，本文提出 **VideoChat-M1**，首个面向视频理解的多智能体协同框架。其核心创新在于引入**协同策略规划（Collaborative Policy Planning, CPP）**范式，让多个智能体动态生成、执行并通信调用策略，基于同伴上下文灵活更新方案。同时，通过**多智能体强化学习（Multi-Agent Reinforcement Learning, MARL）**联合优化最终答案奖励和中间协作过程反馈，使智能体团队能够稳定、高效地探索丰富的视频线索。

核心结论如下：

- **全面性能领先**：VideoChat-M1 在八个主流基准上达到最优，在 LongVideoBench 上比 GPT-4o 高 15.6%，比 Gemini 2.5 Pro 高 3.6%（见 Table 1）。
- **增益源于协同学习框架**：即使将专用空间工具替换为通用视觉骨干（Qwen2.5-VL-7B），VideoChat-M1 仍保持最优性能，比巨型模型 InternVL-3.5-241B 高出 34.2%（见 Table 11），证实效果源于 CPP 框架而非特定强工具。
- **参数效率极高**：37B 的智能体团队在 VideoMMMU 上取得了与 235B 的 Qwen3-VL 相当的效果，仅使用约 15% 的参数量。

方法上，CPP 范式包含三个关键过程：策略生成（Policy Generation）、策略执行（Policy Execution）和策略通信（Policy Communication），配合共享记忆缓冲区实现智能体间的信息交换与迭代优化。训练阶段采用监督微调（SFT）初始化策略生成能力，再通过 MARL 联合优化，引入结果奖励、格式奖励和协作奖励三合一信号，并加入 Agent Dropout 作为关键规范化手段以保证训练稳定性。

## 背景与动机

### 视频理解的瓶颈：从静态感知到时空协同推理

视频理解正从简单的场景分类、动作识别，迈向需要跨时间尺度进行复杂因果推理的阶段。长视频中的事件往往分散在数分钟甚至数小时的跨度内，涉及细粒度空间关系、时序定位、多步逻辑链等多样化线索。这对模型的感知粒度、记忆容量和推理深度同时提出了极高要求。

当前主流方案可分为两大路线。一类以 **GPT-4o**、**Gemini 2.5 Pro**、**InternVL-3.5-241B** 等超大规模多模态模型为代表，依赖海量预训练将视觉与语言空间对齐，再通过指令微调解锁视频问答能力。这类模型在常规基准上表现强劲，但在需要精细时空定位（如 Charades-STA 上的时序定位）或长视频多跳推理（如 LongVideoBench）时，往往因缺乏显式的线索搜索机制而力不从心。

另一类方案引入**智能体工具调用范式**，让模型根据用户查询自主选择并调用视频感知工具，如 **VideoChat-A1** 和 **VCA**。这类方法赋予了模型主动探索视频的能力，但其核心缺陷在于：**工具调用策略是单一、固定且不可学习的**。一旦初始策略未能覆盖关键线索，后续推理便陷入“盲人摸象”的困境——智能体无法根据中间发现动态调整搜索方向，更无法利用多个智能体之间的信息互补来突破单一个体的认知上限。

### 核心矛盾：静态策略 vs. 动态线索发现

这一缺陷的根源在于，现有智能体方法将“策略规划”视为一次性决策，而非一个持续演化的认知过程。真实视频理解中，关键证据往往隐藏在不起眼的片段里：一个瞬间的表情变化可能推翻整段对话的情感判断，远处背景中的微小物体可能成为事件因果链的决定性环节。固定策略无法保证这些线索恰好落入预设的搜索路径。

更本质地，单个智能体的注意力、记忆和推理能力都是有限的。面对复杂长视频，任何单一模型都难以在有限上下文窗口内同时兼顾全局结构感知与局部细节捕获。**群体智能**——让多个智能体各司其职、相互通信、协同探索——是突破这一瓶颈的自然思路，但如何让智能体团队学会“有效协作”，而非简单地并行执行独立任务，仍是一个开放挑战。

### 本文动机：从固定单策略到可学习的多智能体协同

针对上述困境，本文提出 **VideoChat-M1**，核心动机在于用**可学习的多智能体协同策略规划（Collaborative Policy Planning, CPP）**取代传统的静态单策略范式。具体而言，我们希望实现三个层面的突破：

1. **策略的动态生成与演化**：每个智能体不再执行预设的工具序列，而是根据当前查询和已有发现自主生成、执行并迭代更新策略。
2. **智能体间的有效通信**：在推理过程中，智能体通过共享记忆缓冲区交换中间线索，使后续策略能充分利用同伴的发现，实现真正的“1+1>2”。
3. **协作行为的端到端优化**：通过多智能体强化学习（MARL），让智能体团队在追求最终答案正确性的同时，学会产生高质量的中间协作过程——这正是以往方法完全缺失的关键环节。

这一设计理念的直觉在于：视频理解中的线索发现本质上是一个**搜索问题**，而多智能体协同搜索的效率远高于单智能体的线性扫描。当智能体 A 发现某一时间段的异常事件时，智能体 B 可以立即调整策略去验证相关的前因后果，智能体 C 则专注于空间细节的交叉检验。这种并行且相互引导的探索模式，使得团队能以更少的计算代价覆盖更丰富的证据空间。

## 核心创新

VideoChat-M1 的核心创新在于将视频理解中**静态、不可学习的单一工具调用策略**替换为**可学习、可通信、可迭代演化的多智能体协同策略规划（Collaborative Policy Planning, CPP）**，并通过多智能体强化学习（MARL）赋予智能体团队自主优化协同行为的能力。以下从三个“changed slots”展开其相对于已有智能体方法的本质突破。

### 从固定策略到动态生成的协同策略规划

现有基于智能体的视频理解方法（如 **VCA** 和 **VideoChat-A1**）依赖单一固定或预定义的不可学习策略：智能体按预设顺序调用工具，无法根据视频内容的时空复杂性自适应调整探索路径。VideoChat-M1 的 CPP 范式彻底改变了这一范式：

- **策略生成（Policy Generation）**：每个智能体独立根据用户查询 $\mathcal{Q}$ 和工具集 $\mathcal{T}$ 生成独特的初始工具调用策略 $\mathcal{P}_i = \mathcal{G}_i(\mathcal{Q}, \mathcal{T})$，而非共享同一固定计划。
- **策略执行（Policy Execution）**：智能体按自身策略逐步调用工具处理视频，每一步基于前一步的中间答案 $\mathcal{A}_{i,n-1}$ 产生新的中间结果 $\mathcal{A}_{i,n} = \mathcal{P}_{i,n}(\mathcal{V}, \mathcal{T}, \mathcal{A}_{i,n-1})$。
- **策略通信（Policy Communication）**：执行过程中，智能体通过共享内存缓冲区 $\mathcal{M}$ 交换中间线索，并基于同伴的上下文决定是否更新自身策略 $\mathcal{P}_i' = \mathcal{G}_i(\mathcal{Q}, \mathcal{T}, \mathcal{M}, \mathcal{P}_i)$，形成迭代的“生成—执行—通信—更新”闭环。

这一机制的本质优势在于**群体智能探索**：多个智能体从不同视角、不同时间尺度上同时探索视频线索，通过通信实现信息汇聚与策略自适应调整，打破了单智能体固定策略的视野局限。Figure 2 和 Figure 3 清晰展示了这一范式与现有方法的架构差异及推理阶段工作流。

### 从无训练到多智能体强化学习的联合优化

已有智能体方法通常不进行训练，或仅对单智能体做微调，智能体间的协作行为完全依赖人工设计的规则，缺乏优化空间。VideoChat-M1 引入了一套完整的多智能体训练流水线：

1. **SFT 数据构造**：利用强智能体团队自动标注高质量策略计划，经正确性和可执行性筛选后构造监督微调数据集，为每个智能体提供初始的策略生成能力。
2. **MARL 训练（基于 GRPO）**：采用三种奖励信号的组合进行端到端联合优化：
   - **结果奖励（Result Reward）**：评估最终答案的正确性。
   - **格式奖励（Format Reward）**：约束输出格式的规范性。
   - **协作奖励（Collaboration Reward）**：评估智能体间信息交换与策略更新的有效性。
   
   训练使用 GRPO 算法，通过优势标准化 $A_R^{(k)}$ 和 KL 散度正则化 $\beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})$ 保证训练稳定性，同时引入 **Agent Dropout** 作为关键规范化器，防止智能体过度依赖特定队友。

Table 6 的消融实验表明，完整的 MARL 配置（含结果、格式、协作奖励及 Agent Dropout）在 Video-Holmes 和 LongVideoBench 上分别达到 60.5 和 82.3，去除任意组件均导致性能下降，其中 Agent Dropout 是最关键的规范化器。Table 7 进一步证实 SFT + RFT 完整流水线的必要性：单独 SFT 或单独 RFT 均显著低于完整训练。

### 从无通信到基于共享记忆的策略通信

现有方法中，多智能体之间要么无中间通信，要么仅进行简单的静态信息传递。VideoChat-M1 在策略执行阶段插入**策略通信**机制：智能体将中间结果写入共享内存 $\mathcal{M}$，并在每轮通信中基于当前策略 $\mathcal{P}_i$ 和共享记忆决定是否更新后续策略。这种通信是**动态、双向且可迭代的**——智能体既贡献自身发现，也利用同伴线索调整自身行为，形成真正的协同推理。

消融实验（Table 9）表明，多智能体讨论机制中多数投票（Vote）优于单智能体回答或简单拼接，验证了协同通信机制的有效性。

### 增益来源的因果验证

一个关键问题是：VideoChat-M1 的性能提升究竟源于 CPP 框架本身，还是源于其使用的特定强工具？Table 11 的工具依赖性消除实验给出了决定性证据：即使将专用空间工具替换为通用视觉骨干 Qwen2.5-VL-7B，VideoChat-M1 仍保持最优性能，且比巨型模型 InternVL-3.5-241B 高出 34.2%。这直接证实**增益来源于协同学习框架而非特定工具**。同时，37B 的智能体团队在 VideoMMMU 上取得了与 235B 的 Qwen3-VL 相当的效果，参数效率极高。

## 整体框架

VideoChat-M1 的整体框架围绕**协同策略规划（Collaborative Policy Planning, CPP）** 范式构建，其核心思想是用一个多智能体团队取代传统视频理解智能体中单一、固定的工具调用策略。系统由三类核心组件构成：一组**策略智能体** $\mathcal{G} = \{\mathcal{G}_i\}$、一组**视频感知工具** $\mathcal{T} = \{\mathcal{T}_j\}$，以及一个**共享记忆缓冲区** $\mathcal{M}$。

### 推理阶段流水线

在推理阶段，CPP 的工作流（见 Figure 3）分为三个迭代交织的过程：

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/003_Figure_3.jpg]]
*Figure 3: The workflow of Collaborative Policy Planning (CPP) in the Reasoning Phase. Multiple agents independently generate initial plans, communicate to exchange reasoning states, and iteratively refine their policies using different tools. Through repeated rounds of communication and plan updates, the agents collectively vote or summarize to produce a reliable final answer*

1.  **策略生成（Policy Generation）**：给定用户查询 $\mathcal{Q}$ 和可用工具集 $\mathcal{T}$，每个智能体 $\mathcal{G}_i$ 独立生成其初始工具调用策略 $\mathcal{P}_i$：
    $${\mathcal{P}}_{i} = {\mathcal{G}}_{i}(\mathcal{Q}, {\mathcal{T}})$$
    该策略是一个结构化的步骤序列，指定了每个推理阶段应调用哪些工具以及如何处理中间结果。

2.  **策略执行（Policy Execution）**：各智能体按照自身策略逐步调用工具处理视频 $\mathcal{V}$。在第 $n$ 步，智能体 $i$ 使用策略步骤 $\mathcal{P}_{i,n}$，结合前一步的中间答案 $\mathcal{A}_{i,n-1}$，生成当前步骤的答案：
    $$\mathcal{A}_{i,n} = \mathcal{P}_{i,n}(\mathcal{V}, \mathcal{T}, \mathcal{A}_{i,n-1})$$
    执行过程中的所有中间结果均被存入共享记忆 $\mathcal{M}$。

3.  **策略通信（Policy Communication）**：执行完一步后，智能体团队进入通信阶段。每个智能体审视共享记忆 $\mathcal{M}$ 中其他智能体的中间结果和推理线索，并据此决定是否更新自己的后续策略：
    $$\mathcal{P}_{i}^{\prime} = \mathcal{G}_{i}(\mathcal{Q}, \mathcal{T}, \mathcal{M}, \mathcal{P}_{i})$$
    策略通信与执行迭代进行，使智能体能够动态吸收同伴发现的线索，灵活调整工具调用方案。这一机制是打破单一固定策略局限、实现“群体智能”探索的关键。

最终，所有智能体的答案通过**答案聚合**模块产生最终输出：对于多选问题采用多数投票，对于开放式或时序定位问题则由专职智能体汇总。

### 训练阶段流水线

VideoChat-M1 采用“监督微调（SFT）+ 多智能体强化学习（MARL）”的两阶段训练方案（见 Figure 4）：

1.  **SFT 数据构造**：首先利用一个强智能体团队（如基于 GPT-4o 的智能体群）自动为视频问答任务标注高质量的策略计划。这些计划经过正确性和可执行性筛选后，构成 SFT 数据集（每任务约 2000 条初始计划）。随后，使用交叉熵损失对团队中每个智能体进行初步微调，使其学会生成合理的初始策略。

2.  **MARL 联合优化**：在 SFT 基础上，采用 GRPO（Group Relative Policy Optimization）算法对整个智能体团队进行端到端的强化学习训练。训练信号由三部分奖励组成：
    - **结果奖励** $\mathcal{R}_{res}$：评估最终答案的正确性；
    - **格式奖励** $\mathcal{R}_{format}$：约束策略输出的格式规范性；
    - **协作奖励** $\mathcal{R}_{col}$：评估智能体是否有效利用了同伴的中间线索。
    
    GRPO 通过标准化优势函数来更新策略：
    $$A_{R}^{(k)} = \frac{ R(o_k) - \mathrm{mean}(\{R(o_1),\dots,R(o_K)\}) }{ \mathrm{std}(\{R(o_1),\dots,R(o_K)\}) }$$
    
    优化目标为最大化加权优势，同时用 KL 散度正则化防止策略过度偏移参考策略：
    $$\max_{\pi_\theta} \mathbb{E}_{o\sim\pi_{\theta_{\mathrm{old}}}} \left[ \sum_{k=1}^{K} \frac{\pi_\theta(o_k)}{\pi_{\theta_{\mathrm{old}}}(o_k)} \cdot A_{R}^{(k)} - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}}) \right]$$
    
    此外，训练中引入了 **Agent Dropout** 正则化——随机丢弃部分智能体的输出，迫使剩余智能体学会更鲁棒的独立推理与协作能力。消融实验表明，Agent Dropout 是 MARL 中最关键的规范化组件，移除后性能下降约 2%（Table 6）。

### 模块关系与数据流总结

整个框架的数据流可概括为：用户查询与视频输入 → 各智能体独立生成初始策略 → 并行执行策略并调用工具 → 共享记忆汇总中间线索 → 智能体通信并迭代更新策略 → 答案聚合输出最终结果。训练阶段则通过 SFT 赋予智能体基本的策略生成能力，再通过 MARL 的三合一奖励信号和 Agent Dropout 规范化，使智能体团队学会稳定、高效的协同探索行为。

### 补充图表

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/002_Figure_2.jpg]]
*Figure 2: Architecture and Working Mode Comparison (Existing Agent-based Method vs. Our VideoChat-M1). While prior methods rely on a fixed policy, VideoChat-M1 introduces a collaborative multi-agent policy planning pipeline that generates, executes, communicates and refines plans iteratively, enabling more adaptive and accurate long-video reasoning*

## 核心模块与公式推导

VideoChat‑M1 的核心架构由**协同策略规划（CPP）**推理范式和**多智能体强化学习（MARL）**训练框架两大支柱构成。CPP 负责在推理阶段让多个智能体动态生成、执行并通信工具调用策略；MARL 则通过三合一奖励信号联合优化整个智能体团队，使其学会稳定、高效地协同探索视频线索。

### 协同策略规划（CPP）

CPP 范式包含三个基本组件：一组策略智能体 $\mathcal{G} = \{\mathcal{G}_i\}$、一组视频感知工具 $\mathcal{T} = \{\mathcal{T}_j\}$ 以及一个共享记忆缓冲区 $\mathcal{M}$。其工作流由三个关键过程串联而成：

**策略生成（Policy Generation）**  
每个智能体 $\mathcal{G}_i$ 根据用户查询 $\mathcal{Q}$ 和可用工具集 $\mathcal{T}$ 独立生成初始工具调用策略：

$${\mathcal{P}}_{i} = {\mathcal{G}}_{i}(\mathcal{Q}, {\mathcal{T}}) \tag{1}$$

策略 $\mathcal{P}_i$ 是一系列工具调用步骤的有序计划，决定了智能体如何逐步分析视频。

**策略执行（Policy Execution）**  
智能体按策略步骤依次调用工具。第 $n$ 步的中间答案 $\mathcal{A}_{i,n}$ 由当前策略步骤 $\mathcal{P}_{i,n}$ 处理视频 $\mathcal{V}$、工具集 $\mathcal{T}$ 以及前一步答案 $\mathcal{A}_{i,n-1}$ 得到：

$$\mathcal{A}_{i,n} = \mathcal{P}_{i,n}(\mathcal{V}, \mathcal{T}, \mathcal{A}_{i,n-1}) \tag{2}$$

**策略通信（Policy Communication）**  
执行过程中，智能体将中间结果存入共享记忆 $\mathcal{M}$。随后，每个智能体参考自身当前策略和团队中间记忆，决定是否更新后续策略：

$$\mathcal{P}_{i}^{\prime} = \mathcal{G}_{i}(\mathcal{Q}, \mathcal{T}, \mathcal{M}, \mathcal{P}_{i}) \tag{3}$$

策略通信与执行迭代进行，使智能体能够基于同伴发现的线索灵活调整自身计划，实现“群体智能”探索。最终答案通过多数投票（多选问题）或专职智能体汇总（开放式/时序定位问题）产生。

### 多智能体强化学习（MARL）

训练分为两个阶段：监督微调（SFT）和强化微调（RFT/MARL）。

**SFT 阶段**利用强智能体团队自动标注高质量策略计划，经正确性和可执行性筛选后构造数据集，以交叉熵损失最大化真实计划的生成概率，对每个智能体独立微调。

**MARL 阶段**采用三合一奖励信号联合优化所有智能体：

- **结果奖励 $\mathcal{R}_{res}$**：最终答案与标准答案的匹配程度；
- **格式奖励 $\mathcal{R}_{format}$**：策略输出是否遵循预定义的结构化格式；
- **协作奖励 $\mathcal{R}_{col}$**：二元信号，评估智能体是否有效利用了同伴的中间结果。

总奖励 $\mathcal{R} = \mathcal{R}_{res} + \mathcal{R}_{format} + \mathcal{R}_{col}$。基于 GRPO 算法，对每条候选输出 $o_k$ 计算标准化优势：

$$A_{R}^{(k)} = \frac{ R(o_k) - \mathrm{mean}(\{R(o_1),\dots,R(o_K)\}) }{ \mathrm{std}(\{R(o_1),\dots,R(o_K)\}) } \tag{4}$$

GRPO 目标函数在最大化加权优势的同时，用 KL 散度正则化防止策略过度偏离参考策略 $\pi_{\mathrm{ref}}$：

$$\max_{\pi_\theta} \mathbb{E}_{o\sim\pi_{\theta_{\mathrm{old}}}} \left[ \sum_{k=1}^{K} \frac{\pi_\theta(o_k)}{\pi_{\theta_{\mathrm{old}}}(o_k)} \cdot A_{R}^{(k)} - \beta D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}}) \right] \tag{5}$$

训练中还引入 **Agent Dropout** 规范化：随机丢弃部分智能体的输出，迫使剩余智能体学习更鲁棒的协作策略。消融实验表明，Agent Dropout 是 MARL 中最关键的规范化器，移除后性能下降约 2%。

### 补充图表

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/004_Figure_4.jpg]]
*Figure 4: Training the Agent Group using Our Multi-Agent Reinforcement Learning (MARL) Method. Agents generate policies, communicate, and iteratively refine them with tool feedback, while reward and reference models guide stable joint optimization*

## 实验与分析

### 主实验结果

VideoChat-M1 在涵盖长视频问答、视频推理、空间智能与时序定位四大类任务的八个主流基准上全面达到最优水平（Table 1）。在长视频理解标杆 LongVideoBench 上，VideoChat-M1（37B 智能体团队）取得 82.3 的准确率，比闭源顶级模型 GPT-4o（66.7）高出 15.6 个百分点，比 Gemini 2.5 Pro 高出 3.6 个百分点；在 Video-Holmes 视频推理基准上达到 60.5，优于基础 LLM 智能体群的最佳成绩 56.2（Table 5、Table 6）。在时序定位任务 Charades-STA 上，mIoU 达到 67.7，超越 Seed 1.5VL 的 64.7。在 VideoMME 综合评估中取得 83.4，比代表性开源基线 Qwen2.5-VL-7B（64.2）提升 19.2 个百分点。

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/005_Table_1.jpg]]
*Table 1: Algorithm Comparison. Our VideoChat-M1 results are bolded, and the best results of each group of methods are marked in blue*

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/010_Table_6.jpg]]
*Table 6: Ablation on Components of MARL*

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/006_Table_5.jpg]]
*Table 5: Comparison with Foundation LLM Agent Groups*

参数效率方面，37B 的智能体团队在 VideoMMMU 上取得了与 235B 的 Qwen3-VL 相当的效果，仅使用了后者约 15% 的参数量，验证了 CPP 框架的强扩展效率。

效率维度（Table 2），VideoChat-M1 平均仅使用 69.9 帧输入，推理延迟约 19.8 秒（4 块 A100 80G 并行），在同等参数量级下效率优于多数开源模型。若部署于单卡 A100，延迟将增加至约 38.9 秒，这是当前框架在资源受限场景下的主要瓶颈。

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/007_Table_2.jpg]]
*Table 2: Average Frame Number and Inference Latency*

### 消融实验

#### MARL 组件消融

Table 6 系统拆解了多智能体强化学习各奖励组件与规范化策略的贡献。完整配置（结果奖励 + 格式奖励 + 协作奖励 + Agent Dropout）在 Video-Holmes 和 LongVideoBench 上分别达到 60.5 和 82.3。移除任一组件均导致性能下降：

- **Agent Dropout 是最关键的规范化器**：去除后性能下降约 2 个百分点，表明在 MARL 训练中随机屏蔽部分智能体可有效防止策略坍缩，迫使团队学习鲁棒的协同行为。
- **协作奖励**：去除后性能显著下降，证实显式建模智能体间协作质量对训练稳定性至关重要。
- **格式奖励**：去除后模型生成策略的可执行性下降，间接影响最终答案质量。

#### SFT 与 RFT 消融

Table 7 对比了仅监督微调（SFT）、仅强化微调（RFT）与完整 SFT + RFT 流水线的效果。完整流水线在两个基准上均取得最优（60.5 / 82.3），单独 SFT 或单独 RFT 均显著低于完整训练。这表明 SFT 提供的策略初始化与 MARL 的协作探索形成互补——SFT 赋予智能体基本的策略生成能力，而 MARL 通过群体交互奖励信号进一步优化协同决策。

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/012_Table_7.jpg]]
*Table 7: Ablation on SFT and RFT*

#### 智能体规模与组成

Figure 5 展示了同构智能体数量从 1 增至 8 时的性能变化趋势：性能随智能体数量单调提升，在 4 个智能体时接近饱和，继续增加收益递减。Table 3 进一步验证了异构智能体组合（不同架构骨干）相比同构组合的优势，而 Table 4 表明适度的架构多样性（如混合不同规模的 Qwen 与 InternVL 系列）可带来额外增益。

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/011_Figure_5.jpg]]
*Figure 5: Effects of the Number of Homogeneous Agents*

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/008_Table_3.jpg]]
*Table 3: Effects of Agent Group Composition and Scale*

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/009_Table_4.jpg]]
*Table 4: Impact of Architectural Diversity in the 4-Agent Group*

#### 讨论机制与微调方法

Table 9 对比了多种答案聚合机制：多数投票（Vote）在多选任务上显著优于单智能体回答或简单拼接，验证了群体决策在 CPP 框架中的核心作用。Table 8 显示 LoRA 微调可获得与全参数微调相近的性能（59.4 / 81.2 vs 60.5 / 82.3），大幅降低训练开销，为实际部署提供了高效的替代方案。

### 工具依赖性验证

Table 11（附录 A.6）的关键消融实验将专用空间工具替换为通用视觉骨干 Qwen2.5-VL-7B，VideoChat-M1 仍保持最优性能，甚至比超大规模模型 InternVL-3.5-241B 高出 34.2%。这一结果强有力地证明：性能提升的核心来源是 CPP 协同学习框架本身，而非对特定强工具的依赖。

![[assets/figures/papers/paper_list_l2730_https_arxiv_org_abs_2511_19524/figures/022_Table_11.jpg]]
*Table 11: Tool Reliance Ablation on VSIBench*

### 失败模式与局限

尽管整体性能领先，VideoChat-M1 仍存在以下可观测的失败模式：

1. **轻量智能体的能力瓶颈**：当团队中包含较小规模模型（如 Qwen2.5-3B）时，该智能体在复杂时序定位任务中可能无法产生正确答案（如图 7 示例），其错误策略会通过通信机制影响整体决策质量。
2. **单卡部署的延迟放大**：并行推理依赖 4 块 A100 80G GPU，单卡部署时延迟增至约 38.9 秒，限制了在资源受限场景下的实时应用。
3. **SFT 数据噪声与覆盖度**：策略数据由强智能体自动标注，存在一定噪声；每任务仅收集约 2,000 个初始计划，对长尾场景的覆盖有限，可能导致部分复杂查询的策略生成质量不足。

### 重要图表结论汇总

- **Figure 1**：VideoChat-M1 在主流视频任务上全面超越闭源（GPT-4o、Gemini 系列）与开源（InternVL-3.5-241B）SOTA 模型。
- **Figure 2**：通过架构对比直观展示 CPP 范式如何打破传统固定策略的局限，引入策略生成-执行-通信的迭代协同流程。
- **Figure 4**：揭示 MARL 训练中奖励模型与参考模型如何联合引导智能体群的稳定优化。
- **Figure 5**：量化了智能体数量对性能的边际贡献，为团队规模选择提供依据。
- **Table 6**：完整刻画了 MARL 各组件的因果贡献，Agent Dropout 被识别为最关键规范化器。

## 方法谱系与知识库定位

VideoChat‑M1 的方法定位可以从三个维度来理解：它与现有基于智能体的视频理解工作的继承与断裂、它通过多智能体强化学习（MARL）引入的独特训练机制，以及该框架的适用边界与未决问题。

### 与现有智能体视频理解方法的关系

VideoChat‑M1 的直接对比对象是两类基于智能体的视频理解范式：

- **单智能体迭代工具调用方法**，以 **VideoChat‑A1** 为代表。这类方法让一个智能体在固定策略下依次调用工具，但其策略是静态的、不可学习的。VideoChat‑M1 将这一范式拓展为多智能体协同策略规划（CPP），核心变化在于：策略不再是单一固定的，而是由多个智能体动态生成、执行并通信，使系统能够自适应地探索视频中不同时间尺度的线索。
- **基于固定策略的多智能体方法**，如 **VCA**。这些方法虽然引入了多个智能体，但智能体之间缺乏策略层面的交互学习与通信，本质上仍是独立执行预定义策略。VideoChat‑M1 的关键突破在于引入了策略通信环节——智能体在执行过程中通过共享内存缓冲区交换中间结果，并据此决定是否更新后续策略，从而实现了真正的“群体智能”探索。

从更宏观的模型谱系来看，VideoChat‑M1 还与一系列闭源和开源大规模多模态模型形成对比，包括 **GPT‑4o**、**Gemini 2.5 Pro**、**Gemini 1.5 Pro**、**InternVL‑3.5‑241B**、**Qwen3‑VL‑235B** 以及 **Seed‑1.5VL**（时序定位基线）。这些模型依赖超大规模参数和大量训练数据来隐式地获取视频理解能力，而 VideoChat‑M1 则通过显式的多智能体协同与工具调用，在仅 37B 的参数规模下实现了超越或持平于这些巨型模型的性能——例如在 VideoMMMU 上与 235B 的 Qwen3‑VL 效果相当，参数效率极高。

### MARL 训练机制的独特贡献

VideoChat‑M1 的另一个核心定位在于它是首个将多智能体强化学习（MARL）引入视频理解智能体训练的工作。其训练框架包含三个层次：

1. **监督微调（SFT）阶段**：利用强智能体团队自动标注高质量策略计划，经正确性和可执行性筛选后构造训练数据，为每个智能体提供初始的策略生成能力。
2. **强化微调（RFT/MARL）阶段**：采用 GRPO 算法进行端到端联合优化，同时引入三种奖励信号——结果奖励（最终答案正确性）、格式奖励（输出结构合规性）和协作奖励（智能体间信息共享的有效性）。消融实验（Table 6）表明，完整的三种奖励配置在 Video‑Holmes 和 LongVideoBench 上分别达到 60.5 和 82.3，去除任意组件均导致性能下降。
3. **Agent Dropout 规范化**：在 MARL 训练中随机丢弃部分智能体的输出，被证明是最关键的规范化器——消除该机制会导致约 2% 的性能下降。

这一训练框架的独特价值在于：它使智能体团队能够稳定地学习协同行为，而非仅仅依赖预定义的协作规则。工具依赖性消除实验（Table 11）进一步证实，即使将专用空间工具替换为通用视觉骨干（Qwen2.5‑VL‑7B），VideoChat‑M1 仍保持最优性能，比巨型模型 InternVL‑3.5‑241B 高出 34.2%，说明性能增益源于 CPP 协同学习框架本身，而非特定强工具。

### 适用边界与局限

尽管 VideoChat‑M1 在八个主流基准上全面达到最优，其适用性仍受以下因素制约：

- **计算资源门槛**：推理需要 4 块 A100 80G GPU 并行，单卡推理延迟会增至约 38.9 秒，在资源受限场景下部署困难。
- **智能体能力下限**：轻量级智能体（如 Qwen2.5‑3B）在部分复杂任务上可能无法给出正确答案，影响团队整体性能——这暗示 CPP 框架的有效性依赖于组成智能体的基本能力水平。
- **训练数据覆盖度**：SFT 策略数据由强智能体自动标注，存在一定噪声，且每任务仅收集约 2000 个初始计划，覆盖度有限。

### 开放问题

论文提出的范式同时打开了若干值得进一步探索的方向：

- 如何在不显著增加计算开销的前提下扩展到更多智能体或更大规模模型？
- CPP 范式是否可以迁移至其他多模态任务（如图像理解、文档分析）？
- 更高效的多智能体通信机制（如选择性通信、图网络）能否进一步提升协作效率？
- 能否将协作奖励从二元评估扩展为连续细粒度信号，以提供更丰富的训练指导？

## 原文 PDF

![[paperPDFs/CVPR_2026/VideoChat_M1_Collaborative_Policy_Planning_for_Video_Understanding_via_Multi_Agent_Reinforcement_Learning.pdf]]
