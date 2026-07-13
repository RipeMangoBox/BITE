---
title: "Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Seeing_Listening_Remembering_and_Reasoning_A_Multimodal_Agent_with_Long_Term_Memory.pdf
project_link: null
code_link: https://github.com/ByteDance-Seed/m3-agent
openreview_forum_id: PMz29A7Muq
aliases:
- MA
- SLRRMALTM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "以实体为中心的多模态记忆图构建 + 语义记忆（身份等价、属性、关系、情节理解）生成 + 基于强化学习的多轮检索与推理控制。"
primary_logic: "M3-Agent 通过模仿人类认知的‘记忆-控制’双过程，将视频流转化为实体中心的结构化语义记忆，并利用 RL 训练的多轮推理来检索和利用这些记忆，从而显著提升长视频问答的准确性和一致性。"
claims:
- "M3-Agent 在 M3-Bench-robot 上相比最强基线 Gemini-GPT4o-Hybrid 准确率提升 6.7%"
- "移除语义记忆导致 M3-Bench-robot 精度下降 17.1 个百分点"
- "RL 训练（DAPO）使控制模型在多轮推理中优于仅提示的基线"
- "实体等价（face-voice mapping）对记忆质量至关重要，移除后精度大幅下滑"
---

# Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory

> [!tip] 核心洞察
> M3-Agent 通过模仿人类认知的‘记忆-控制’双过程，将视频流转化为实体中心的结构化语义记忆，并利用 RL 训练的多轮推理来检索和利用这些记忆，从而显著提升长视频问答的准确性和一致性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 看、听、记与推理：一种具备长期记忆的多模态智能体 |
| 英文题名 | Seeing, Listening, Remembering, and Reasoning: A Multimodal Agent with Long-Term Memory |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=PMz29A7Muq) · [GitHub](https://github.com/ByteDance-Seed/m3-agent) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | M3-Agent |
| Dataset | M3-Bench-robot (All), M3-Bench-web (All), VideoMME-long |

> [!tip] 效果简介
> - M3-Bench-robot (All) 上，准确率 (%) 为 30.7，对比 24.0 (Gemini-GPT4o-Hybrid)，变化 +6.7。
> - M3-Bench-web (All) 上，准确率 (%) 为 48.9，对比 41.2 (Gemini-GPT4o-Hybrid)，变化 +7.7。
> - VideoMME-long 上，准确率 (%) 为 61.8，对比 56.5 (Gemini-GPT4o-Hybrid)，变化 +5.3。

## 概要

**问题瓶颈**：传统长视频理解方法难以持续处理无限流式输入并构建一致的世界知识，导致长期记忆中的实体跟踪一致性差、跨片段推理困难。现有方案多依赖线性描述列表或无结构化记忆，缺乏对实体身份、属性、关系及情节的深层语义理解。

**核心思路**：M3-Agent 通过模仿人类认知的“记忆-控制”双过程，将视频流转化为以实体为中心的结构化语义记忆，并利用强化学习训练的多轮推理来检索和利用这些记忆。其关键设计包括三个层面：
- **记忆组织**：以实体为中心的多模态图记忆（文本、图像、音频节点按实体连接），替代传统线性描述列表；
- **记忆内容**：同时生成情景记忆（细粒度事件描述）和语义记忆（身份等价、角色属性、关系、情节理解、常识规则），超越仅依赖低层视觉信息的片段描述；
- **控制检索**：多轮迭代推理（[Search]/[Answer] 动作循环，最多 5 轮），替代单轮 RAG 一次性推理。

**方法定位**：M3-Agent 属于**记忆增强型多模态智能体**，其记忆模块由 MLLM 驱动的记忆生成器与外部图数据库构成，控制模块采用 Qwen3-32B 初始化后经 DAPO 强化学习训练，利用 GPT-4o 自动评估的二元奖励优化多轮检索策略。

**主要结果**：在三个长视频问答基准上，M3-Agent 均显著优于最强基线 Gemini-GPT4o-Hybrid：
- M3-Bench-robot：30.7% vs 24.0%（+6.7 个百分点）
- M3-Bench-web：48.9% vs 41.2%（+7.7 个百分点）
- VideoMME-long：61.8% vs 56.5%（+5.3 个百分点）

消融实验进一步验证了各组件的关键作用：移除语义记忆导致 M3-Bench-robot 精度骤降 17.1 个百分点；移除实体等价映射（face-voice equivalence）下降 11.2 个百分点；DAPO 强化学习训练相比仅提示的基线提升 6.7 个百分点。



长视频理解正从“离线分析固定片段”转向“在线持续感知无限流式输入”的智能体场景。一个能看、能听、能记、能推理的多模态智能体，需要从连续的视频流中持续构建一致的世界知识，并在任意时刻回答关于过去事件的复杂问题。然而，现有方法在这一目标上存在根本性瓶颈。

### 核心瓶颈：流式输入下的长期一致性与跨片段推理

传统长视频理解方法（如 **MovieChat** (Song et al., 2024)、**MA-LMM** (He et al., 2024a)、**Flash-VStream** (Zhang et al., 2024b)）虽然支持在线处理，但其记忆机制本质上仍是视频片段描述的线性列表或无结构存储。这导致两个关键缺陷：

1. **实体跟踪一致性差**：当同一人物或物体在视频不同片段中以不同模态（人脸、声音、衣着）出现时，系统缺乏将跨模态信息绑定到同一实体的能力。例如，听到一个声音却无法将其与之前看到的人脸关联，导致记忆碎片化。
2. **跨片段推理困难**：需要聚合分布在多个时间片段中的证据来回答问题时（如“机器人今天一共见了哪些人？”），线性记忆结构迫使模型进行低效的穷举检索，缺乏结构化的索引和语义关联。

苏格拉底式方法（Socratic models，如 **GPT-4o** (Hurst et al., 2024)、**Gemini-1.5-Pro** (Team et al., 2024)）将视频转换为文本描述后进行检索增强生成（RAG），虽然利用了强大大语言模型的推理能力，但仍然是单轮检索后一次性推理，无法进行多轮迭代式的“检索—推理—再检索”过程，且文本描述丢失了丰富的视觉和听觉细节。

### 本文动机：模拟人类“记忆—控制”双过程认知

人类在处理持续感知输入时，依赖两种互补的认知过程：**记忆**（将经验编码、存储和整合为结构化的世界知识）和**控制**（根据当前任务需求，主动检索并推理相关记忆）。现有智能体系统未能有效模拟这种双过程架构——它们要么缺乏结构化的长期记忆更新机制，要么控制策略过于简单，无法进行多轮策略性检索。

M3-Agent 的核心动机正是填补这一架构空白：通过以实体为中心的多模态记忆图构建，将视频流转化为具有身份等价、属性、关系和情节理解的语义记忆；同时，利用强化学习训练的控制模型，实现多轮迭代的 [Search]/[Answer] 动作循环，使智能体能够主动、策略性地利用自己的记忆来回答问题。这种设计从根本上解决了流式输入下长期记忆的一致性和跨片段推理问题。



## 核心方法与创新机理

M3-Agent 的核心创新在于将长视频理解从“一次性描述-检索”范式转向**以实体为中心的记忆-控制双过程架构**，通过结构化语义记忆和强化学习驱动的多轮推理，系统性解决了长期流式输入中实体跟踪一致性差、跨片段推理困难的根本瓶颈。

### 1. 从线性描述到实体中心的多模态图记忆

传统方法（如 Socratic 模型基线 **GPT-4o**、**Gemini-1.5-Pro** 及在线方法 **MovieChat**、**MA-LMM**）将视频记忆组织为线性描述列表或无结构片段，难以维护跨时间的实体身份一致性。M3-Agent 的记忆组织方式发生了根本性变化：

- **记忆组织**：构建以实体为中心的多模态图数据库，每个节点代表一个独立的记忆项（文本、图像或音频），按实体关联形成图结构。这种组织方式使得同一人物在不同时间点的视觉、声音、属性信息能够被统一索引和更新。
- **记忆内容**：超越传统的片段级视觉描述，生成两类互补记忆——**情景记忆**（细粒度事件描述，对应具体观察到的“发生了什么”）和**语义记忆**（从片段中提炼的通用知识，包括身份等价映射、角色属性、人物关系、情节理解和常识规则）。语义记忆的生成是 M3-Agent 区别于所有基线的最关键创新：消融实验显示，移除语义记忆模块导致 M3-Bench-robot 精度从 30.7% 骤降至 13.6%（下降 17.1 个百分点），表明抽象世界知识的构建对长程推理具有决定性作用。

### 2. 从单轮 RAG 到 RL 训练的多轮迭代推理

基线方法（如 Gemini-Agent、Gemini-GPT4o-Hybrid）采用单轮检索后一次性推理的策略，无法根据检索结果动态调整查询方向。M3-Agent 的控制过程引入了两个关键变革：

- **多轮 [Search]/[Answer] 动作循环**：控制模型在最多 H=5 轮内交替执行记忆检索和推理，每轮生成推理步骤、动作类型和检索参数。若动作为 `[Search]`，系统查询长期记忆库并将结果追加到上下文；若为 `[Answer]`，则终止循环并输出答案。这种迭代机制使模型能够根据中间检索结果调整后续查询策略，模拟人类“回忆-验证-再回忆”的认知过程。
- **RL 训练替代提示工程**：基线依赖未训练的提示模型（GPT-4o、Gemini），而 M3-Agent 使用 **Qwen3-32B** 初始化控制策略，通过 **DAPO**（Dynamic sAmpling Policy Optimization）强化学习算法进行训练，奖励信号由 GPT-4o 自动评估器提供的二元奖励（答案正确为 1，否则为 0）驱动。实验表明，RL 训练（DAPO）使控制模型在 M3-Bench-robot 上达到 30.7%，显著优于仅提示的 control-32b-prompt（24.0%），且 DAPO 优于 **GRPO**（30.0% vs 30.7%）。移除多轮指令（inter-turn instruction）导致精度骤降至 20.2%，移除推理步骤则下降 11.7 个百分点，验证了多轮推理机制和结构化思考过程的必要性。

### 3. 实体等价映射：跨模态身份绑定的关键机制

M3-Agent 在记忆构建过程中利用人脸和声音特征建立跨模态实体等价映射（face-voice equivalence），将同一人物的视觉外观和听觉信号绑定为统一的身份表示。这一机制直接解决了长视频中“同一人以不同模态出现时被误认为不同实体”的核心问题。消融实验证实，移除等价映射导致 M3-Bench-robot 精度下降 11.2 个百分点，说明跨模态身份一致性是记忆质量的关键支柱。

### 创新总结

M3-Agent 的创新链条可概括为：**实体中心图记忆（结构创新）→ 情景+语义双层记忆（内容创新）→ 跨模态等价绑定（一致性创新）→ RL 多轮检索推理（控制创新）**。这一“记忆-控制”双过程设计使模型在 M3-Bench-robot、M3-Bench-web 和 VideoMME-long 上分别以 6.7%、7.7% 和 5.3% 的优势超越最强基线 Gemini-GPT4o-Hybrid，尤其在人物理解（+15.5%）和跨模态推理（+6.7%）等需要深层记忆一致性的任务上表现突出。



![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_PMz29A7Muq/figures/006_Figure_1.jpg]]
*Figure 1: Architecture of M3-Agent, comprising a multimodal large language model (MLLM) and a multimodal long-term memory. It supports two parallel processes: memorization and control. The entity-centric memory structure enables accumulate world knowledge and maintain consistent, context-rich memory over time*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_PMz29A7Muq/figures/012_Table_3.jpg]]
*Table 3: Search functions supported by long-term memory*

M3-Agent 的整体架构围绕“记忆-控制”双过程展开，其核心设计思想是模仿人类认知系统，将视频流转化为以实体为中心的结构化长期记忆，并通过多轮推理来检索和利用这些记忆以完成问答任务。架构如图 1 所示，系统由三个主要模块构成：**记忆生成（memorization）**、**长期记忆库（long-term memory）** 和 **控制推理（control）**。

### 双过程并行运行

记忆过程与控制过程**并行运行**：记忆过程持续感知实时多模态输入（视觉与音频），以约 30 秒为单位的视频片段（clip）增量构建和更新长期记忆；控制过程则独立接收外部指令（如问答），在需要时访问记忆库进行多轮检索与推理，最终给出答案。这种解耦设计使得记忆构建不受问答频率的影响，同时控制过程可以灵活地回溯历史记忆。

### 记忆生成：从视频流到结构化记忆

记忆生成模块接收视频片段后，执行两类记忆的提取：

- **情景记忆（Episodic Memory）**：对应视频中观察到的具体事件，以细粒度的文本描述形式记录。同时，模块会提取人脸特征和声音特征，并建立**实体等价映射**（face-voice equivalence），将不同模态中属于同一人物的信息关联起来，形成持久的身份表征。
- **语义记忆（Semantic Memory）**：从片段中抽象出通用知识，包括人物身份、角色属性、实体间关系、情节理解以及常识规则。语义记忆的生成依赖于一组多样化的提示模板（见 Table 10），引导模型从不同维度提炼知识。

### 长期记忆库：实体中心的多模态图

长期记忆库是一个**实体中心的多模态图数据库**，节点代表独立的记忆项（文本、图像或音频），边表示节点之间的关联。同一实体的所有记忆节点被组织在一起，形成一致的实体表征。记忆库支持两种粒度的检索操作（Table 3）：

- **`search_node`**：检索与查询语义相关的节点，支持多模态输入（文本、图像、音频）。
- **`search_clip`**：返回与查询最相关的前 k 个视频片段，同时包含该片段的情景记忆和语义记忆。

记忆构建采用增量方式，新节点不断添加到图中。当出现冲突信息时，系统采用**加权投票机制**：频繁激活的节点或边累积更高权重，在推理时被优先采纳。

### 控制推理：多轮检索与推理循环

控制过程遵循 Algorithm 1 的流程，最大执行轮数设为 H=5。每一轮，控制策略 $\pi_\theta$ 生成一个包含三部分的响应：**推理过程（reasoning）**、**动作（action）** 和**动作参数（argument）**。动作类型有两种：

- **`[Search]`**：系统根据参数调用 `search_clip` 检索最相关的 2 个片段，将结果追加到上下文中，进入下一轮。
- **`[Answer]`**：模型基于当前上下文直接给出最终答案，结束循环。

控制模型以 Qwen3-32B 为初始策略，使用 **DAPO（Dynamic Adaptive Policy Optimization）** 算法进行强化学习训练。训练数据包含 500 个长视频（对应 26,943 个 30 秒片段）和 2,736 个问答对，通过合成扩展至 10,952 个样本。奖励函数为二元奖励：若 GPT-4o 自动评估器判定答案正确，则 $R_i = 1$，否则 $R_i = 0$。DAPO 优化目标在截断重要性采样的基础上，要求每批次中至少存在一个正奖励和一个负奖励轨迹，以稳定训练。

### 输入输出流总结

1. **视频流** → 记忆生成模块 → 情景记忆 + 语义记忆 → 存入长期记忆图数据库。
2. **问答指令** → 控制模块 → 多轮 `[Search]` 检索记忆库 → 上下文累积 → `[Answer]` 输出最终答案。

> **需要人工核实**：论文中未明确说明记忆生成模块与控制模块是否共享同一个 MLLM 基座，以及两者是否在推理时完全独立部署。此外，记忆库的加权投票机制的具体实现细节（如权重衰减策略）在提供的片段中未充分展开。



### 记忆生成与长期记忆库

M3-Agent 的认知架构由两个并行过程驱动：**记忆生成**与**控制推理**。记忆生成模块持续接收视频流，以片段为单位逐步构建以实体为中心的多模态记忆图。与基线方法仅生成线性视频描述不同，M3-Agent 的记忆内容包含两类互补表征：

- **情景记忆**：对应视频中可观察的具体事件，提供细粒度的事件描述。
- **语义记忆**：从片段中抽象出的一般性世界知识，涵盖身份等价映射、角色属性、人物关系、情节理解及常识规则。

长期记忆库实现为外部数据库，以实体为中心组织文本、图像、音频节点，形成多模态图结构。记忆更新采用增量添加与加权投票机制：频繁激活的节点或边累积更高权重，用于推理时的冲突消解。该记忆库支持两种粒度的检索操作，如表 3 所示：`search_node` 处理节点级查询，`search_clip` 返回最相关的视频片段。

### 控制推理与多轮检索

控制过程遵循 Algorithm 1 的循环逻辑。给定问题 $q$，控制策略 $\pi_\theta$ 在每个轮次生成包含推理、动作及参数的响应。动作为 `[Search]` 时，系统以参数查询记忆库 $D$，将检索结果追加至上下文供下一轮使用；动作为 `[Answer]` 时，输出最终答案。最大执行轮次设为 $H=5$，`search_clip` 返回最相关的 top-2 片段。

这一多轮迭代检索与推理机制，替代了基线方法中普遍采用的单轮 RAG 模式，使智能体能够逐步定位分散在长视频中的证据片段，实现跨片段、跨模态的因果链推理。

### 强化学习训练与奖励设计

控制策略基于 Qwen3-32b 初始化，采用 DAPO 算法进行强化学习训练。训练数据包含 500 个长视频对应的 26,943 个 30 秒片段及 2,736 个问答对，经合成扩充至 10,952 个样本。

奖励函数为二元判定：

$$R_{i} = \left\{ \begin{array}{ll} 1, & \mathrm{gpt-4o-evaluator}(q, a, y_i) = \mathrm{True} \\ 0, & \mathrm{otherwise} \end{array} \right.$$

其中 $q$ 为问题，$a$ 为参考答案，$y_i$ 为第 $i$ 条控制轨迹的最终输出。GPT-4o 自动评估器与人工多数投票一致性达 96%。

### DAPO 优化目标

DAPO 的截断重要性采样目标为：

$$\mathcal{J}_{\mathrm{DAPO}}(\theta) = \mathbb{E}_{(q,a) \sim \mathcal{D}, \{\tau_i\}_{i=1}^G \sim \pi_{\theta}^{\mathrm{od}}(\cdot|q)} \left[ \frac{1}{\sum_{i=1}^G \sum_{t=1}^{|\tau_i|} \mathbb{I}(\tau_{i,t})} \sum_{i=1}^G \sum_{t=1}^{|\tau_i|} \mathbb{I}(\tau_{i,t}) \cdot \min\left( \frac{\pi_{\theta}(\tau_{i,t}|\tau_{i,<t})}{\pi_{\theta}^{\mathrm{od}}(\tau_{i,t}|\tau_{\tau,<t})} \hat{A}_{i,t}, \mathrm{clip}\left( \frac{\pi_{\theta}(\tau_{i,t}|\tau_{i,<t})}{\pi_{\theta}^{\mathrm{od}}(\tau_{i,t}|\tau_{i,<t})}, 1-\epsilon_{\mathrm{low}}, 1+\epsilon_{\mathrm{high}} \right) \hat{A}_{i,t} \right) \right]$$

其中 $\tau_i$ 为第 $i$ 条轨迹，$\mathbb{I}(\tau_{i,t})$ 为指示函数（仅对生成 token 为 1），$\hat{A}_{i,t}$ 为优势估计，$\epsilon_{\mathrm{low}}$ 和 $\epsilon_{\mathrm{high}}$ 为不对称截断参数。DAPO 的关键约束是每批次中必须同时包含正奖励和负奖励样本，这一设计避免了纯正或纯负奖励组导致的梯度消失问题。

### 消融实验的因果验证

消融实验从记忆与控制两个维度验证了各模块的因果贡献。移除语义记忆模块后，M3-Bench-robot 精度从 30.7 骤降至 13.6，降幅达 17.1 个百分点，表明抽象世界知识对长视频问答至关重要。移除情景记忆中的实体等价映射（face-voice 关联）导致精度下降 11.2 个百分点，验证了跨模态身份对齐对记忆一致性的核心作用。控制端，移除多轮指令使精度降至 20.2，移除推理步骤导致精度下降 11.7%，二者共同证实了多轮推理与显式思维链对检索决策的支撑作用。DAPO 相比 GRPO 在 M3-Bench-robot 上取得 30.7 vs 30.0 的微弱优势，且 RL 收益随模型规模扩大而递增。



## 实验与关键发现

### 主实验结果

M3-Agent 在三个长视频问答基准上全面超越所有基线方法。表 4 汇总了各方法在 M3-Bench-robot、M3-Bench-web 和 VideoMME-long 上的准确率。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_PMz29A7Muq/figures/013_Table_4.jpg]]
*Table 4: Results on M3-Bench-robot, M3-Bench-web, and VideoMME-long, with comparisons across M3-Bench question types: multi-evidence reasoning (ME), multi-hop reasoning (MH), crossmodal reasoning (CM), person understanding (PU), and general knowledge extraction (GK)*

在 M3-Bench-robot 上，M3-Agent 达到 30.7% 的准确率，相比最强的 agent 基线 Gemini-GPT4o-Hybrid（24.0%）提升 **6.7 个百分点**。这一优势在 M3-Bench-web 上进一步扩大至 **7.7 个百分点**（48.9% vs 41.2%），在 VideoMME-long 上则为 **5.3 个百分点**（61.8% vs 56.5%）。值得注意的是，Socratic 模型基线（如 GPT-4o、Gemini-1.5-Pro）在 M3-Bench-robot 上的表现极差（GPT-4o 仅 8.5%），说明仅靠视频描述生成加 RAG 检索无法应对需要长期记忆整合的复杂推理任务。在线视频理解方法中，MA-LMM 表现最佳（M3-Bench-robot 24.4%），但仍显著落后于 M3-Agent。

按问题类型细分，M3-Agent 在需要跨片段信息整合的题型上优势尤为突出。与 Gemini-GPT4o-Hybrid 相比，M3-Bench-web 上的 **Person Understanding** 提升 15.5 个百分点（59.3% vs 43.8%），**Cross-modal Reasoning** 提升 6.7 个百分点（44.3% vs 37.6%）。这直接验证了实体中心的多模态记忆图在身份跟踪和视听信息关联上的关键作用。

### 记忆模块消融

表 5 固定控制模型为 control-32b-rl，系统性地消融记忆模块的各个组件，结果揭示了语义记忆和实体等价映射的决定性贡献：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_PMz29A7Muq/figures/014_Table_5.jpg]]
*Table 5: Ablation of memorization models. The control is fixed as control-32b-rl*

- **移除语义记忆**：M3-Bench-robot 准确率从 30.7% 骤降至 13.6%，降幅达 **17.1 个百分点**。这表明单纯的情节记忆（细粒度事件描述）远不足以支撑复杂推理，从视频中抽象出的身份属性、角色关系、情节理解和常识规则等语义知识是问答能力的核心支柱。
- **移除实体等价映射（face-voice equivalence）**：M3-Bench-robot 准确率下降 **11.2 个百分点**。等价映射负责将同一实体的不同模态表征（人脸图像与声音片段）关联为统一的身份节点，其移除直接破坏了长期记忆中的实体一致性，导致跨片段的人物跟踪失败。
- **记忆模型的模仿学习（SFT）同样不可或缺**：使用未微调的 prompt 模型生成记忆（memory-7b-prompt）时，M3-Bench-robot 准确率仅为 20.7%，远低于 memory-7b-sft 的 30.7%，说明高质量记忆的生成需要专门的监督训练。

### 控制模块消融

表 6 固定记忆模型为 memory-7b-sft，从训练算法、模型规模和关键组件三个维度消融控制模块：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_PMz29A7Muq/figures/015_Table_6.jpg]]
*Table 6: Ablation of control methods, including: (1) a comparison between GRPO and DAPO training algorithms; (2) performance gains from DAPO scale with model size; (3) the effect of removing inter-turn instruction and reasoning. The memorization model is fixed as memory-7b-sft*

**RL 训练 vs. Prompt 基线**：control-32b-rl（DAPO 训练）在 M3-Bench-robot 上达到 30.7%，而 control-32b-prompt（仅提示，无训练）仅为 24.0%，差距达 6.7 个百分点。这证明多轮检索与推理的决策能力难以通过提示工程获得，需要 RL 训练来优化搜索策略和推理路径。

**DAPO vs. GRPO**：DAPO 训练的 control-32b-rl 在三个基准上均优于 GRPO 训练的 control-32b-grpo（M3-Bench-robot: 30.7 vs 30.0; M3-Bench-web: 48.9 vs 47.7; VideoMME-long: 61.8 vs 58.7）。DAPO 的核心优势在于其优化目标要求每批次中至少存在一个正奖励和一个负奖励轨迹，从而避免了 GRPO 可能出现的奖励坍缩问题。

**模型规模扩展**：RL 训练带来的收益随模型规模增大而递增。control-8b-rl 相比 control-8b-prompt 提升有限，而 control-32b-rl 的提升幅度最大，表明更大规模的基座模型能更有效地利用 RL 训练来学习复杂的多轮检索策略。

**关键组件必要性**：
- 移除**轮间指令（inter-turn instruction）**：M3-Bench-robot 准确率从 30.7% 暴跌至 20.2%（降幅 10.5 个百分点）。轮间指令在每轮检索后向模型提供当前状态和剩余轮数信息，是维持多轮推理连贯性的关键信号。
- 移除**推理步骤（reasoning）**：M3-Bench-robot 准确率下降 11.7%（从 30.7% 降至约 19.0%）。推理步骤是模型在生成 [Search]/[Answer] 动作前进行的显式思考过程，其移除相当于剥夺了模型的规划能力。

### 错误分析

表 19 对 M3-Agent 的常见错误类型进行了量化分类，揭示了当前方法的主要失效模式：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_PMz29A7Muq/figures/031_Table_19.jpg]]
*Table 19: Summary of common error types*

- **细粒度细节推理错误（50%）**：占比最高的错误类型，表明模型对视频中视觉细节的理解和记忆仍然不足。例如，无法准确回忆物体的颜色、数量或精确位置。
- **空间推理错误（20%）**：当前记忆以文本描述为主，缺乏丰富的视觉内容（如关键帧快照），导致模型在需要空间关系推理时表现不佳。
- **搜索策略错误（12%）**：控制模型未能选择正确的检索函数或检索参数，导致无法定位相关记忆片段。
- **人名缺失（10%）**：实体跟踪中未能正确识别或关联人物姓名。

这些错误模式指明了未来的改进方向：需要更丰富的视觉记忆表征以增强细节和空间推理能力，以及更智能的注意力机制来实现选择性记忆。



## 定位与知识库关联

### 1. 与现有工作的关系

M3-Agent 的贡献建立在两个相互关联的瓶颈之上：**长视频理解中的记忆一致性**，以及**面向无限流输入的推理控制**。现有方法在这两个维度上呈现出清晰的谱系分化，而 M3-Agent 通过将二者统一为“记忆-控制”双过程架构，实现了对各类基线的系统性超越（Table 4 主结果）。

#### 1.1 记忆组织：从线性描述到实体中心的多模态图

传统在线视频理解方法采用线性记忆表征。**MovieChat**（Song et al., 2024）、**MA-LMM**（He et al., 2024a）和 **Flash-VStream**（Zhang et al., 2024b）将视频流压缩为片段级描述序列，缺乏跨片段实体关联机制。这导致两个关键失效模式：（1）同一人物在不同片段中被视为不同实体，无法进行身份等价的跨模态映射（如人脸与声音的关联）；（2）记忆检索退化为关键词匹配，无法支持需要聚合分布式证据的 Multi-evidence Reasoning。

M3-Agent 的记忆槽位变更直击这一瓶颈：

| 记忆维度 | 基线值 | M3-Agent 方案 | 证据强度 |
|---------|--------|-------------|---------|
| 组织方式 | 线性描述列表 | 实体中心的多模态图（文本/图像/音频节点按实体连接） | Table 5 消融：移除等价映射使 M3-Bench-robot 精度下降 11.2 个百分点 |
| 内容层次 | 仅低层视觉描述 | 情景记忆（细粒度事件）+ 语义记忆（身份等价、属性、关系、情节理解） | Table 5 消融：移除语义记忆使精度下降 17.1 个百分点 |

语义记忆的引入是该架构的关键因果旋钮。它模仿人类认知中将具体经验抽象为世界知识的过程，使智能体不仅能回答“刚才发生了什么”（情景记忆），还能回答“这个人通常扮演什么角色”（语义记忆中的角色属性）或“这两个事件之间有何因果联系”（情节理解）。Table 5 显示，仅使用情景记忆的 `memory-7b-sft w/o semantic memory` 在 M3-Bench-robot 上仅得 13.6%，而完整 M3-Agent 为 30.7%——17.1 个百分点的差距表明，语义记忆对长视频推理而言不是锦上添花，而是结构性必需。

#### 1.2 控制检索：从单轮 RAG 到 RL 驱动的多轮迭代推理

Socratic 模型基线（**GPT-4o**、**Gemini-1.5-Pro**、**Qwen2.5-Omni-7b**、**Qwen2.5-VL-7b**）采用“描述生成 + RAG”范式：先用 MLLM 生成视频描述，再将描述与问题拼接进行单轮推理。这种范式在 M3-Bench-robot 上表现极差（GPT-4o Socratic 仅 8.5%，Table 4），原因在于：（1）单轮 RAG 无法处理需要多步推理的 Multi-hop Reasoning；（2）描述生成阶段的压缩损失不可逆，后续推理无法回溯原始信息。

Agent 基线（**Gemini-Agent** 和 **Gemini-GPT4o-Hybrid**）引入了多轮记忆检索，但仍依赖未训练的提示模型进行控制决策。M3-Agent 的关键创新在于将控制过程形式化为强化学习问题：使用 DAPO 算法训练 Qwen3-32b 模型，使其学会在 `[Search]` 和 `[Answer]` 动作之间进行最优轮次分配（最多 H=5 轮）。Table 6 的消融揭示了 RL 训练的因果效应：

- `control-32b-prompt`（仅提示，未训练）：M3-Bench-robot 24.0%
- `control-32b-rl`（DAPO 训练）：M3-Bench-robot 30.7%（+6.7 个百分点）
- `control-32b-grpo`（GRPO 训练）：M3-Bench-robot 30.0%（DAPO 优于 GRPO 0.7 个百分点）

DAPO 相对于 GRPO 的优势源于其约束条件——要求每批次中至少存在一个正奖励和一个负奖励轨迹，这迫使模型学习区分有效检索与无效检索，而非简单模仿历史动作分布。

#### 1.3 基准定位：M3-Bench 填补的评测空白

Table 2 的系统对比表明，现有 LVQA 基准（EgoSchema、LongVideoBench、HourVideo、MVBench、Video-MME、MLVU）均未覆盖“智能体在场”场景——即视频中存在一个可交互的具身智能体，需要对其进行持续的身份跟踪和行为理解。M3-Bench-robot 的 100 个第一人称机器人视频填补了这一空白，其五类问题设计（Table 1）直接对应 M3-Agent 的记忆与推理能力维度：Multi-evidence Reasoning 测试分布式证据聚合，Multi-hop Reasoning 测试多步因果链推理，Cross-modal Reasoning 测试视听信息融合，Person Understanding 测试实体跟踪与身份等价，General Knowledge Extraction 测试语义记忆抽象能力。

### 2. 适用边界与局限

尽管 M3-Agent 在三个基准上均取得最优，其设计存在明确的适用边界和已知失效模式。

#### 2.1 细粒度视觉理解不足

Table 19 的错误类型分析显示，**细粒度细节推理错误占 50%**，是所有错误类型中占比最高的。这表明当前记忆系统对视觉细节（如物体纹理、精确空间位置、小目标外观）的编码不够充分。深层原因在于：记忆生成依赖 MLLM 将视频片段转化为文本描述，这一压缩过程不可避免地丢失了细粒度视觉信息。虽然记忆图支持存储图像节点，但检索机制（`search_node` 和 `search_clip`）本质上仍以文本查询为驱动，无法实现基于视觉相似性的细粒度匹配。

#### 2.2 空间推理的固有缺陷

**空间推理错误占 20%**，是第二大类错误。当前记忆缺乏丰富的视觉内容（如关键帧快照或深度信息），导致智能体难以回答涉及空间关系的问题（如“物体 A 在物体 B 的左边还是右边”）。这一局限与记忆表示的选择直接相关：实体中心的图结构擅长编码实体间的语义关系（如“属于”“拥有”），但对空间关系的几何约束编码能力有限。

#### 2.3 语义记忆的预定义类别依赖

语义记忆生成依赖于预定义的提示模板（Table 10），这限制了其可扩展性。在开放域场景中，智能体可能遇到预定义类别之外的知识类型（如特定领域的专业概念），此时语义记忆模块无法自动发现新的知识类别。这与人类认知中的“学习如何学习”能力存在差距——人类可以在无监督条件下自发形成新的概念类别。

#### 2.4 记忆构建缺乏选择性注意

当前记忆构建过程对每一视频片段进行等权处理，缺乏注意力机制以选择性记忆。这可能导致两个问题：（1）认知过载——无关信息占据记忆容量，干扰后续检索；（2）关键信息淹没——重要但短暂的视觉事件（如一闪而过的面部表情）可能因片段级的平均池化而被稀释。论文明确将此列为未来工作方向。

### 3. 开放问题

基于上述局限，M3-Agent 的架构指向以下开放研究方向：

**选择性记忆的注意力机制**：如何使智能体根据任务上下文动态调整记忆的粒度和焦点？这一问题与神经科学中的“记忆巩固”过程高度相关——人类海马体在睡眠中会选择性强化重要记忆并抑制无关信息。在工程层面，可探索基于检索频率的加权机制（当前已有加权投票的雏形）或基于预测误差的显著性检测。

**更丰富的视觉记忆表示**：如何在保持检索效率的前提下，将关键帧快照、深度图或神经场等更丰富的视觉表征整合进长期记忆？Table 5 中移除等价映射的 11.2 个百分点损失表明，跨模态对齐对记忆质量至关重要；类似地，整合更丰富的视觉信息可能显著改善空间推理（当前 20% 错误率）和细粒度推理（当前 50% 错误率）。

**终身学习与世界知识更新**：当前 M3-Agent 的记忆构建与任务执行是分离的过程——记忆在视频播放阶段预先构建，控制阶段仅进行检索。能否将二者耦合，使智能体在回答问题的过程中发现记忆的矛盾或缺失，并主动更新记忆？这将使系统从“离线记忆”进化为“在线学习”，更接近人类认知的持续更新特性。

**语义记忆的自动类别发现**：如何使智能体在没有预定义提示的情况下，自主发现新的语义知识类别？这需要结合开放世界学习和概念抽象的前沿研究，可能的方向包括基于聚类的新概念发现或基于大语言模型的零样本知识模式识别。



## 原文 PDF

![[paperPDFs/ICLR_2026/Seeing_Listening_Remembering_and_Reasoning_A_Multimodal_Agent_with_Long_Term_Memory.pdf]]
