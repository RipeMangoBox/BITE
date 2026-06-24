---
title: "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ReasoningBank_Scaling_Agent_Self_Evolving_with_Reasoning_Memory.pdf
openreview_forum_id: jL7fwchScm
aliases:
- RM
- ReasoningBank
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "构建一个能够从智能体自我判断的成功和失败经验中蒸馏高阶、可传递推理策略的记忆框架，并建立记忆与测试时扩展之间的正向协同机制。"
primary_logic: "REASONINGBANK通过将原始交互轨迹抽象为结构化的推理记忆项（标题、描述、内容），使智能体不仅复用成功策略，还能从失败中提取预防性教训，实现持续进化。MATTS在测试时通过并行自对比和顺序自精炼生成丰富的对比信号，提炼更高质量的记忆；而更好的记忆又引导更有效的扩展，形成记忆与扩展之间的强大协同，共同提升智能体性能。"
claims:
- "REASONINGBANK 在 WebArena 上整体成功率较无记忆基线提升+8.3%（Gemini-2.5-flash），且在三个不同LLM上持续优于 Synapse 和 AWM 基线。"
- "MATTS 与 REASONINGBANK 结合后，并行扩展 k=5 时 WebArena 整体成功率达到 51.8%，超越单一 REASONINGBANK 的 48.8%，且在所有子集上均取得效率增益。"
- "纳入失败轨迹用于记忆提取后，REASONINGBANK 成功率从 46.5% 提升至 49.7%，而 Synapse 和 AWM 加入失败经验后未见明显提升甚至下降。"
- "在 Mind2Web 跨域泛化测试中，REASONINGBANK 取得了最高的任务成功率，验证了其记忆项的鲁棒性和可迁移性。"
---

# ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory

> [!tip] 核心洞察
> REASONINGBANK通过将原始交互轨迹抽象为结构化的推理记忆项（标题、描述、内容），使智能体不仅复用成功策略，还能从失败中提取预防性教训，实现持续进化。MATTS在测试时通过并行自对比和顺序自精炼生成丰富的对比信号，提炼更高质量的记忆；而更好的记忆又引导更有效的扩展，形成记忆与扩展之间的强大协同，共同提升智能体性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | REASONINGBANK：通过推理记忆实现智能体自我进化 |
| 英文题名 | ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jL7fwchScm); [GitHub](https://github.com/google-research/reasoning-bank) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | REASONINGBANK + MATTS |
| Dataset | WebArena Overall, WebArena Overall with MATTS, SWE-Bench-Verified, Mind2Web Cross-Domain |

> [!tip] 效果简介
> - WebArena Overall 上，Success Rate (SR) 为 48.8，对比 40.5 (No Memory)，变化 +8.3。
> - WebArena Overall with MATTS 上，Success Rate (SR) 为 51.8，对比 40.5 (No Memory)，变化 +11.3。
> - SWE-Bench-Verified 上，Resolve Rate 为 57.4，对比 54.0 (No Memory, Gemini-2.5-pro)，变化 +3.4。

## 概述

当前LLM智能体在执行连续任务流时面临一个核心瓶颈：它们无法有效利用积累的交互历史进行学习，导致重复犯错、丢弃有价值的洞察，缺乏自我进化能力。REASONINGBANK 针对这一问题，提出了一个以结构化推理记忆为核心的闭环框架。其核心洞察在于，将原始交互轨迹抽象为由标题、描述、内容构成的推理记忆项，使智能体不仅能复用成功策略，还能从失败中提取预防性教训，从而实现持续进化。

在此基础上，MATTS（Memory-Aware Test-Time Scaling）通过并行自对比和顺序自精炼，在测试时生成丰富的对比信号以提炼更高质量的记忆；而更好的记忆又反过来引导更有效的扩展，形成了**记忆与测试时扩展之间的正向协同机制**。

实验结果表明，REASONINGBANK 在 WebArena 基准上整体成功率较无记忆基线提升 **+8.3%**（Gemini-2.5-flash），结合 MATTS 并行扩展（k=5）后进一步提升至 **51.8%**（+11.3%）。在 SWE-Bench-Verified 上，解决率达到 **57.4%**（+3.4%），且平均交互步数减少 14.4%。消融实验证实，纳入失败轨迹是性能提升的关键因素（成功率从 46.5% 提升至 49.7%），而现有基线方法（Synapse、AWM）在加入失败经验后未见明显提升甚至下降。在 Mind2Web 跨域泛化测试中，REASONINGBANK 取得了最高的任务成功率，验证了其记忆项的鲁棒性和可迁移性。

## 背景与动机

### 问题背景：LLM智能体的“失忆症”

大型语言模型驱动的智能体在网页浏览、软件工程等复杂交互环境中展现出巨大潜力，但当它们面对连续任务流时，一个根本性的瓶颈逐渐暴露：**智能体无法有效利用积累的交互历史进行学习**。每完成一个任务，智能体获得的经验——无论是成功的策略还是失败的教训——都随着交互结束而被丢弃。这意味着智能体在下一个任务中可能重复完全相同的错误，无法从过往中汲取任何洞察。

这种“失忆症”导致两个直接后果：一是**重复犯错**，智能体在相似场景中反复陷入相同的陷阱；二是**效率低下**，缺乏经验引导使得智能体需要更多交互步骤才能完成任务。从系统角度看，这本质上是智能体缺乏**自我进化能力**——它无法随着任务经验的增长而变得更聪明。

### 现有记忆方法的缺口

研究者已经意识到记忆对智能体的重要性，并提出了若干方案，但这些方法存在明显的结构性问题。

**Synapse**（Zheng et al., 2024）将原始交互轨迹直接存储为上下文记忆。这种方法的问题在于，原始轨迹包含大量噪声和任务特异性细节，难以泛化到新场景。更关键的是，它仅从成功轨迹中提取记忆，完全忽略了失败经验中蕴含的预防性价值。

**AWM**（Wang et al., 2025d）从成功轨迹中抽取可重用的工作流作为记忆。相比 Synapse，它进行了一定程度的抽象，但记忆来源仍然单一——仅限于成功经验。这种“只看成功不看失败”的策略，使得智能体对潜在陷阱毫无防备。

两类方法的共同缺陷可以归纳为三点：第一，**记忆内容抽象级别不足**，停留在原始轨迹或具体工作流层面，缺乏对底层推理策略的提炼；第二，**失败轨迹被系统性忽略**，而失败恰恰是学习“什么不该做”的宝贵信号；第三，**记忆与测试时扩展之间缺乏协同**——记忆系统与推理时的计算扩展各自独立运行，无法形成正向反馈循环。

### 本文动机：从经验中蒸馏可传递的推理策略

本文的核心动机源于一个关键洞察：**智能体真正需要的不是对过去交互的逐字复现，而是从中蒸馏出的高阶、可传递的推理策略**。一次成功的网页导航之所以成功，不是因为它点击了某个特定按钮，而是因为它遵循了“先定位导航栏，再搜索目标页面”这样的推理模式。同样，一次失败之所以失败，背后往往存在可归纳的教训，例如“不要假设筛选器默认显示所有选项”。

基于这一洞察，REASONINGBANK 提出了一种全新的记忆范式：将原始交互轨迹抽象为结构化的**推理记忆项**（包含标题、描述和内容），使智能体不仅能复用成功策略，还能从失败中提取预防性教训。这种记忆不再是“做了什么”的记录，而是“为什么这样做”以及“为什么不该那样做”的推理知识。

更进一步，本文引入 **MATTS**（Memory-Aware Test-Time Scaling），在测试时通过并行自对比和顺序自精炼生成丰富的对比信号，用于提炼更高质量的记忆。更好的记忆反过来又引导更有效的扩展，形成**记忆与扩展之间的强大协同**，共同推动智能体性能的持续提升。

## 核心创新

REASONINGBANK 的核心创新在于**记忆内容的抽象层级跃迁**与**测试时扩展-记忆的正向协同机制**，二者共同解决了当前 LLM 智能体“交互-遗忘-重复犯错”的瓶颈。

### 从轨迹存储到推理策略蒸馏

传统记忆方法停留在原始交互轨迹的存储与回放层面：**Synapse**（Zheng et al., 2024）将完整轨迹作为上下文记忆，**AWM**（Wang et al., 2025d）仅从成功轨迹中抽取可重用工作流。这两种方法面临共同的局限——记忆粒度粗糙、缺乏对失败经验的结构化利用。

REASONINGBANK 将记忆内容的抽象级别从“轨迹/工作流”提升至“推理策略与推理提示”。每条记忆项由三个结构化字段构成：**标题**（title）、**描述**（description）和**内容**（content），将原始交互经验蒸馏为可传递的高阶推理单元。这一设计的因果机制在于：抽象后的策略不绑定于特定任务实例的表面特征，因而具备更强的跨任务迁移能力——在 Mind2Web 跨域泛化测试中，REASONINGBANK 取得了最高的任务成功率（Table 2），验证了记忆项的鲁棒性。

### 失败轨迹的预防性价值挖掘

现有方法对失败轨迹的处理存在根本性缺陷：Synapse 和 AWM 几乎完全忽略失败经验，或仅将其作为负样本排除。REASONINGBANK 的关键突破在于**对失败轨迹进行原因分析，提取预防性策略和教训**，将“犯错”转化为可复用的防御性知识。

消融实验（Figure 6）揭示了这一设计的决定性作用：
- 仅使用成功经验时，REASONINGBANK 成功率为 46.5%；
- 纳入失败经验后，成功率跃升至 49.7%；
- 相比之下，Synapse 加入失败经验后仅从 40.6% 微升至 41.7%，AWM 甚至从 44.4% 降至 42.2%。

这表明，失败轨迹的价值高度依赖于提取机制的质量——简单地将失败轨迹作为上下文不仅无益，反而可能引入噪声；而 REASONINGBANK 的“反思-提炼-预防”范式能够将失败转化为正向信号。

### 记忆与测试时扩展的协同闭环

传统测试时扩展（TTS）与记忆系统独立运行，扩展仅通过并行采样或顺序精炼提升单次决策质量，不产生持久化的学习信号。REASONINGBANK 引入的 **MATTS**（Memory-Aware Test-Time Scaling）打破了这一隔离：

- **并行扩展**：生成多条轨迹，通过自对比（self-contrast）提炼一致的成功模式与错误模式，用于记忆管理；
- **顺序扩展**：在单一轨迹上迭代自精炼，将中间推理笔记作为记忆信号注入记忆库。

这形成了双向增强的正反馈循环：**MATTS 通过丰富的对比信号提炼更高质量的记忆，而更好的记忆又引导更有效的扩展**。实验证据（Table 1）显示，REASONINGBANK 结合 MATTS 并行扩展（k=5）后，WebArena 整体成功率达到 51.8%，超越单一 REASONINGBANK 的 48.8%，且在所有子集上均取得效率增益。Figure 5 进一步验证了记忆质量与扩展性能之间的协同效应：在 REASONINGBANK 记忆机制下，Best-of-N 和 Pass@1 均显著优于其他记忆机制。

### 成本效率的结构性优势

值得关注的是，REASONINGBANK 的创新并未以显著的计算开销为代价。Table 5 显示，其总 token 消耗相比无记忆方法仅增加约 4.3%，但整体性能提升 20.5%，成本效益远优于 Synapse 和 AWM。这种“轻量记忆、显著增益”的特性，源于结构化推理策略的高信息密度——少量高质量记忆项即可提供有效的决策引导，而无需堆砌冗长的原始轨迹。

## 整体框架

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_jL7fwchScm/figures/003_Figure_2.jpg]]
*Figure 2: Overview of REASONINGBANK. Experiences are distilled into structured memory items with a title, description, and content. For each new task, the agent retrieves relevant items to interact with the environment, and constructs new ones from both successful and failed trajectories. These items are then consolidated into REASONINGBANK, forming a closed-loop memory process*

REASONINGBANK 构建了一个闭环记忆系统，使 LLM 智能体能够在连续任务流中持续积累、蒸馏和复用推理经验。其核心流水线由三个模块串联而成，辅以 MATTS 在测试时扩展阶段提供记忆驱动的协同增强。

### 记忆检索（Memory Retrieval）

当智能体面对新任务时，系统首先基于嵌入相似度从记忆库中检索与当前任务最相关的 top-k 记忆项。这些记忆项并非原始交互轨迹的简单存储，而是经过抽象的结构化推理单元，包含**标题**（title）、**描述**（description）和**内容**（content）三个字段（Figure 2）。标题概括策略要点，描述说明适用场景，内容承载具体的推理提示和操作经验。检索到的记忆项被注入智能体的上下文，引导其后续决策。

### 记忆提取（Memory Extraction）

任务执行完毕后，系统通过 LLM-as-a-Judge 对交互轨迹进行自我评判，生成二元的成功/失败信号。针对成功轨迹，提取模块总结其成功原因，蒸馏出可复用的推理策略；针对失败轨迹，提取模块进行原因分析，提炼出预防性教训和避错提示（Figure 2, Figure 9）。这一双重提取机制是 REASONINGBANK 区别于 Synapse（仅存储原始轨迹）和 AWM（仅从成功轨迹中抽取工作流）的核心设计：失败经验被转化为具有预防价值的记忆项，而非被丢弃。

### 记忆巩固（Memory Consolidation）

新生成的记忆项被直接添加至记忆库，形成闭环更新。这一简单的直接添加策略是作者为隔离记忆内容质量影响而有意选择的，避免了复杂巩固机制对实验结论的干扰。随着任务流的推进，记忆库持续膨胀，为后续任务提供日益丰富的推理参考。

### MATTS：记忆感知的测试时扩展

MATTS 在 REASONINGBANK 的基础上引入两种测试时扩展策略，与记忆形成正向协同（Figure 3）：

- **并行扩展（Parallel Scaling）**：对同一任务生成 $k$ 条独立轨迹，通过跨轨迹的**自对比**（self-contrast）提炼一致的成功模式和错误模式，用于记忆管理和最终答案选择。
- **顺序扩展（Sequential Scaling）**：在单条轨迹上迭代进行**自精炼**（self-refinement），将中间推理笔记作为额外的记忆信号注入，丰富记忆库的质量。

两种策略中，扩展因子 $k$ 分别表示并行轨迹数量或顺序精炼步数。MATTS 的核心洞察在于：更高质量的记忆能引导更有效的扩展，而扩展过程中产生的丰富对比信号又能反哺记忆提炼——记忆与扩展之间形成强大的协同效应（Figure 5）。实验表明，MATTS 的并行扩展（$k=5$）将 REASONINGBANK 的 WebArena 整体成功率从 48.8% 进一步提升至 51.8%（Table 1），且在所有子集上均取得效率增益。

### 整体数据流

整个框架的数据流可概括为：**检索 → 行动 → 评判 → 提取 → 巩固**的闭环。智能体策略 $\pi_{\mathcal{L}}(\cdot|\mathcal{M},\mathcal{A})$ 以骨干 LLM $\mathcal{L}$ 参数化，受记忆模块 $\mathcal{M}$ 和动作空间 $\mathcal{A}$ 条件约束。在每一步，智能体基于历史观察 $o_{0:t}$、历史动作 $a_{0:t}$、检索到的记忆和可用动作空间生成下一动作 $a_{t+1}$。任务完成后，环境转移函数 $\bar{\mathcal{T}}(s_{t+1}|s_t, a_t)$ 给出的轨迹状态被送入提取模块，完成记忆的蒸馏与巩固。

## 核心模块与公式推导

### 智能体策略的形式化定义

REASONINGBANK 将智能体策略参数化为一个以骨干大语言模型 $\mathcal{L}$ 为核心、受记忆模块 $\mathcal{M}$ 和动作空间 $\mathcal{A}$ 共同约束的决策函数：

$$\pi _ { \mathcal { L } } ( \cdot | \mathcal { M } , \mathcal { A } )$$

环境的状态转移由以下函数刻画，表示在状态 $s_t$ 下执行动作 $a_t$ 后进入下一状态 $s_{t+1}$ 的过程：

$$\bar { \mathcal { T } } ( s _ { t + 1 } | s _ { t } , a _ { t } )$$

在每一步交互中，智能体基于历史观察序列 $o_{0:t}$、历史动作序列 $a_{0:t}$、检索到的记忆 $\mathcal{M}$ 以及动作空间 $\mathcal{A}$，生成下一步动作 $a_{t+1}$：

$$\pi _ { \mathcal { L } } \left( o _ { 0 : t } , a _ { 0 : t } ; \mathcal { M } , \mathcal { A } \right) \to a _ { t + 1 }$$

以上公式构成了 REASONINGBANK 闭环记忆系统的基础决策框架（Section 3.1）。

### 记忆闭环的三大核心模块

REASONINGBANK 的记忆集成过程由三个关键模块串联构成（Section 3.2, Figure 2）：

1. **记忆检索（Memory Retrieval）**：对于每个新任务，系统基于嵌入相似度从记忆库中检索 top-k 条最相关的结构化记忆项，作为当前决策的上下文注入智能体策略。检索采用简单的嵌入匹配策略，目的是隔离记忆内容质量的影响以进行公平评估（Appendix A.2）。

2. **记忆提取（Memory Extraction）**：任务执行完毕后，系统通过 LLM-as-a-Judge 对轨迹进行成功/失败判定，随后分别调用不同的提取提示词：成功轨迹被提炼为可复用的推理策略（“成功洞察”），失败轨迹则被分析失败原因并提取预防性教训（“失败反思”）。每条记忆项由三个结构化字段组成——**标题**（title）、**描述**（description）和**内容**（content），将原始交互轨迹抽象为高阶、可传递的推理单元（Figure 9）。

3. **记忆巩固（Memory Consolidation）**：新生成的记忆项直接加入记忆库，无需复杂的合并或去重策略，形成闭环更新。这一简化设计有意排除了复杂巩固方法带来的干扰，使实验能够聚焦于记忆内容质量本身的影响。

### MATTS：记忆感知的测试时扩展

MATTS 引入了两种测试时扩展策略，将记忆与扩展深度耦合（Section 3.3, Figure 3）：

- **并行扩展（Parallel Scaling）**：对同一任务独立执行 $k$ 条轨迹，通过跨轨迹的**自对比**（self-contrast）机制识别一致的成功模式和错误模式，提炼出更可靠的记忆项。扩展因子 $k$ 表示并行轨迹的数量。

- **顺序扩展（Sequential Scaling）**：在单条轨迹完成后，迭代进行 $k$ 步**自精炼**（self-refinement），将中间推理笔记作为额外的记忆信号注入记忆库。扩展因子 $k$ 表示精炼步数。

两种策略的核心差异在于：并行扩展通过轨迹间的横向对比提取共识性洞察，而顺序扩展通过纵向迭代挖掘单一推理链中的深层信号。MATTS 的关键设计在于，记忆不仅是扩展的输入，扩展过程中产生的对比信号和精炼笔记又反向丰富了记忆库，形成**记忆质量与扩展性能之间的正向协同循环**（Figure 5）。

### 评估指标公式

实验采用两个核心指标衡量智能体性能（Section B.1）：

- **成功率（Success Rate, SR）**：成功任务数占总任务数的比例：
  $$SR = \frac{1}{N} \sum_{i=1}^{N} \text{isSuccess}(q_i)$$

- **平均步数（Average Steps, AS）**：所有任务执行步数的算术平均：
  $$AS = \frac{1}{N} \sum_{i=1}^{N} \text{Steps}(q_i)$$

其中 $\text{isSuccess}(q_i)$ 为任务 $q_i$ 的二元成功判定结果，$\text{Steps}(q_i)$ 为该任务执行的总交互步数。

## 实验与分析

### 主实验结果

REASONINGBANK 在三个基准上均展现出对无记忆基线及现有记忆方法（Synapse、AWM）的显著优势。在 WebArena 基准上（Table 1），REASONINGBANK 以 Gemini-2.5-flash 为骨干时，整体成功率从无记忆基线的 40.5% 提升至 48.8%（+8.3 个百分点）；在 Gemini-2.5-pro 和 Claude-3.7-sonnet 上分别取得 +7.2 和 +4.6 的提升，表明方法对不同 LLM 骨干具有鲁棒的增益。同时，REASONINGBANK 将平均交互步数从 9.7 步降至 8.3 步，实现了约 14.4% 的效率提升。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_jL7fwchScm/figures/005_Table_1.jpg]]
*Table 1: Experiment results of REASONINGBANK and MATTS (parallel scaling, k = 5, pass@1) on WebArena benchmark. Success rate (SR ↑) and the number of steps (Step ↓) are reported on 5 subsets for 3 different backbone LLMs*

当 MATTS 并行扩展（k=5）与 REASONINGBANK 结合时，WebArena 整体成功率进一步提升至 51.8%，较无记忆基线净增 11.3 个百分点。这一增益在所有五个子集（Shopping、Admin、Gitlab、Reddit、Map）上均一致出现，验证了记忆与测试时扩展之间的正向协同效应。

在 Mind2Web 跨域泛化测试中（Table 2），REASONINGBANK 在所有三种泛化设置（Cross-Task、Cross-Website、Cross-Domain）上均取得最高的任务级成功率（SR），尤其在最具挑战性的跨域设置下，SR 从无记忆基线的 1.0 提升至 1.6，表明其记忆项具有跨任务和跨域的可迁移性。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_jL7fwchScm/figures/006_Table_2.jpg]]
*Table 2: Results on Mind2Web benchmark for cross-task, cross-website, and cross-domain generalization test. EA (↑) is short for element accuracy, $\mathrm { A F _ { 1 } }$ (↑) is short for action $\mathrm { F _ { 1 } }$ . , and SSR (↑) is short for step success rate. SR (↑) is the task-level success rate measuring if all steps are correct. that memory curated by REASONINGBANK is more robust and transferable, enabling agents to generalize effectively across diverse scenarios

在 SWE-Bench-Verified 代码修复任务上（Table 3），REASONINGBANK 以 Gemini-2.5-pro 为骨干时取得 57.4 的解决率，较无记忆基线（54.0）提升 3.4 个百分点；以 Gemini-2.5-flash 为骨干时取得 38.8，较基线提升 2.3 个百分点。值得注意的是，REASONINGBANK 在取得更高解决率的同时，平均步数（AS）也显著降低，体现了记忆引导对问题解决效率的改善。

### 效率与成本分析

REASONINGBANK 的效率优势不仅体现在步数减少上。Table 4 的细粒度分析显示，REASONINGBANK 在成功实例上的步数缩减尤为显著——在 Shopping 子集上从 7.8 步降至 5.7 步，相对缩减达 26.9%。即使在失败实例上，REASONINGBANK 也一致减少了交互步数，说明记忆引导有助于智能体更快地识别不可行路径。

在 token 消耗方面（Table 5），REASONINGBANK 的总 token 消耗相比无记忆方法仅增加约 4.3%，但整体性能提升达 20.5%。相比之下，Synapse 和 AWM 的 token 开销更高而性能增益更小，REASONINGBANK 展现出最优的成本效益比。token 消耗的分解显示，额外开销主要来自记忆提取阶段的 LLM 调用，而记忆检索和巩固的代价极低。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_jL7fwchScm/figures/020_Table_5.jpg]]
*Table 5: Breakdown results of total token consumption required for each task*

### 消融研究

**失败轨迹的价值**（Figure 6）。仅使用成功轨迹提取记忆时，REASONINGBANK 的成功率为 46.5%；纳入失败轨迹后提升至 49.7%。这一增益是 REASONINGBANK 独有的——Synapse 加入失败经验后仅从 40.6 微升至 41.7，而 AWM 反而从 44.4 降至 42.2。这表明 REASONINGBANK 的结构化记忆提取策略能够有效从失败中蒸馏预防性教训，而简单的轨迹存储或仅抽取成功工作流无法利用失败中的信息。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_jL7fwchScm/figures/011_Figure_6.jpg]]
*Figure 6: Ablation results of incorporating failure trajectories for memory induction*

**检索经验数量的影响**（Figure 13）。将检索的记忆项数量从 1 增加到 5 时，成功率从 49.7% 逐渐下降至 44.4%。这一反直觉的结果揭示了一个关键瓶颈：记忆质量远比数量重要。过多的低相关性记忆项会引入噪声，干扰智能体的决策过程。当前简单的嵌入相似度检索可能无法精确筛选最相关的记忆，这指向了未来引入推理密集型检索控制器的必要性。

**LLM-as-a-Judge 准确率的鲁棒性**（Figure 7）。通过模拟不同准确率水平的评判器，实验表明 REASONINGBANK 在 70%–90% 的评判精度范围内保持稳定的成功率。这意味着即使正确性信号存在一定噪声，框架仍能有效运作。但当准确率低于 70% 时，性能开始明显下降，说明更可靠的验证器是进一步提升的关键。

**小模型上的泛化性**（Table 6）。在 Gemma-3-12B-Instruct 小模型上，REASONINGBANK 取得 24.1% 的成功率和 11.8 的平均步数，均优于无记忆基线（17.1%，13.7）、Synapse（16.0%，14.0）和 AWM（21.4%，13.3）。这表明方法不依赖特定大模型的能力，可推广至开源小模型。

### 记忆与测试时扩展的协同

Figure 5 揭示了记忆质量与测试时扩展之间的深层协同机制。当使用 REASONINGBANK 的记忆时，Best-of-5（BoN）从 49.7 提升至 55.1；而使用 Synapse 或 AWM 的记忆时，扩展带来的增益远小于 REASONINGBANK。更关键的是，REASONINGBANK 的 Pass@1（随机选取单条轨迹）也随扩展提升，而弱记忆方法在扩展时 Pass@1 几乎停滞。这说明高质量记忆不仅直接提升单次尝试的成功率，还使测试时扩展更有效——更好的记忆引导更优的轨迹生成，更优的轨迹又提炼出更好的记忆，形成正向反馈循环。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_jL7fwchScm/figures/010_Figure_5.jpg]]
*Figure 5: Snapshot of MATTS on WebArenaory mechanism enables stronger test-time scalinShopping subset with different memory mechanisms with k ~ = ~ 5 We compute BoN for all ds better memory curation.5 trajectories and Pass@1 with one randomly selected trajectory*

MATTS 的并行扩展（Figure 4a）在 k=1 到 k=5 区间内，成功率从 49.7 单调提升至 55.1，随后趋于饱和。顺序扩展（Figure 4b）同样呈现上升趋势，但增益幅度略低于并行扩展。MATTS 始终优于无聚合的普通测试时扩展（vanilla TTS），验证了记忆感知的协调与聚合机制的重要性。

### 失败模式与涌现行为

案例研究（Figure 8、Figure 17）展示了 REASONINGBANK 通过记忆项产生的涌现行为。智能体不仅能复用过往的成功策略（如“检查完整订单历史而非仅最近订单”），还能从失败中习得预防性规则（如“在提交表单前验证所有必填字段”）。这些记忆项以标题-描述-内容的结构化形式存储，使得推理提示具有高度可复用性。Figure 16 展示了一个典型案例：REASONINGBANK 通过回忆过往的导航推理提示，将完成同一任务的步数从 29 步降至 10 步。

然而，方法存在以下已知局限：（1）简单的嵌入检索可能召回不相关的记忆，引入噪声；（2）LLM-as-a-Judge 在模糊任务上的误判可能传播错误信号；（3）当前记忆巩固策略为直接添加，缺乏去重和冲突消解机制，长期运行可能导致记忆库膨胀。这些问题在实验中的表现为：增加检索数量后性能下降（Figure 13），以及评判准确率低于 70% 时性能退化（Figure 7）。

## 方法谱系与知识库定位

### 1. 与现有记忆方法的谱系关系

REASONINGBANK 的核心贡献在于将智能体记忆的**抽象层级**从“原始轨迹存储”或“成功工作流复用”提升至“结构化推理策略蒸馏”。它与两类代表性基线形成明确的谱系递进关系：

- **Synapse**（Zheng et al., 2024）：将完整的交互轨迹作为上下文记忆直接存储。其记忆内容是**未经抽象的观察-动作序列**，缺乏对成功/失败因果机制的提炼。当任务分布偏移或轨迹噪声较大时，原始轨迹的复用价值有限。

- **AWM**（Wang et al., 2025d）：从成功轨迹中抽取可重用工作流作为记忆。相比 Synapse，AWM 进行了初步抽象，但其记忆来源**仅限成功经验**，丢弃了失败轨迹中蕴含的预防性知识。

REASONINGBANK 在这条谱系上实现了两个关键跃迁：
1. **记忆内容的抽象层级**：从原始轨迹（Synapse）和成功工作流（AWM）跃迁至结构化推理策略——每条记忆项包含标题、描述和内容三个组件，蒸馏出可传递的高阶推理提示。
2. **失败经验的系统化利用**：通过对失败轨迹进行原因分析，提取预防性策略和教训，使记忆库同时包含“怎么做”和“不要怎么做”的双向知识。

消融实验（Figure 6）为这一谱系定位提供了决定性证据：仅使用成功经验时，REASONINGBANK 成功率为 46.5%；纳入失败经验后提升至 49.7%。而 Synapse 和 AWM 在加入失败经验后未见明显提升甚至下降，表明其记忆提取机制无法有效处理失败信号。这验证了 REASONINGBANK 的记忆抽象策略是性能优势的关键因果杠杆。

### 2. 与测试时扩展方法的协同定位

REASONINGBANK 与 MATTS 的结合构建了**记忆与测试时扩展之间的正向反馈循环**，这是现有方法谱系中尚未被系统探索的维度。

- **传统测试时扩展（Vanilla TTS）**：多条轨迹独立运行，彼此无信息聚合。记忆模块仅作为静态检索源，扩展过程不产生新的记忆信号。
- **MATTS 并行扩展**：通过多条轨迹的自对比，提炼一致的成功模式和错误模式，生成更可靠的记忆项。
- **MATTS 顺序扩展**：在单条轨迹上迭代自精炼，将中间推理笔记作为记忆信号注入记忆库。

Figure 5 揭示了这一协同机制的核心动力学：当记忆质量较低时（如 Synapse、AWM），扩展反而可能放大噪声；而 REASONINGBANK 的高质量记忆使扩展产生正向增益——并行扩展 k=5 时，WebArena 整体成功率从 48.8% 提升至 51.8%（Table 1）。这表明**记忆质量是测试时扩展效果的调节变量**，二者形成“更好的记忆→更有效的扩展→更丰富的对比信号→更高质量的记忆”的闭环。

### 3. 适用边界与局限性

REASONINGBANK 的设计存在以下明确的适用边界：

1. **记忆架构的简化假设**：为隔离记忆内容质量的影响，框架有意采用了简单的嵌入相似度检索和直接添加式巩固策略。这意味着在当前实现中，记忆的组织和检索尚未利用更复杂的架构（如情节记忆、分层记忆、工作记忆）。作者明确指出这些架构与 REASONINGBANK 的记忆内容可互补，但集成后的性能上限有待验证。

2. **正确性信号的噪声容忍**：成功/失败判定依赖 LLM-as-a-Judge，在模糊任务或评判模型自身犯错时可能引入噪声。Figure 7 的模拟实验表明，框架在 70%-90% 评判精度范围内保持鲁棒，但超出此范围的性能退化未充分测试。更可靠的验证器（如环境奖励信号、人机协作反馈）可能进一步释放性能。

3. **记忆质量的边际递减**：Figure 13 显示，增加检索经验数量超过 1 后成功率逐渐下降（49.7→44.4），表明**记忆质量比数量更重要**。当前简单检索策略可能在信息过载时引入干扰，更精细的记忆选择机制是潜在改进方向。

4. **跨域泛化的验证范围**：Mind2Web 上的跨域测试（Table 2）初步验证了记忆项的鲁棒性，但仅在 Web 导航任务内跨域。更广泛的跨环境、跨模态泛化能力尚未评估。

### 4. 开放问题

作者明确提出了若干开放问题，指向该方法谱系的未来演进方向：

- **记忆组合与抽象**：如何将多个记忆项组合成更高层次的策略或可重用宏？这涉及从“单条推理提示”到“复合推理模式”的抽象跃迁。
- **多记忆架构集成**：如何将 REASONINGBANK 的推理策略记忆与情节记忆、工作记忆、长期记忆等架构有机整合？这需要解决不同记忆类型的检索优先级、更新策略和冲突消解问题。
- **推理密集型记忆检索**：如何超越简单的嵌入相似度检索，引入推理密集型控制器进行记忆查找？例如，基于当前任务状态主动推理需要何种类型的记忆，而非被动依赖语义相似度。
- **正确性信号增强**：如何减少 LLM-as-a-Judge 的噪声？可能的方向包括引入环境自带的验证信号、多评判器集成、或人机协作反馈机制。
- **成本-性能的帕累托优化**：Table 5 显示 REASONINGBANK 总 token 消耗仅增加约 4.3%，但整体性能提升 20.5%，成本效益优于 Synapse 和 AWM。然而，当扩展到更大规模任务流时，记忆库的存储和检索成本如何增长，以及是否存在更优的记忆压缩策略，仍需进一步研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/ReasoningBank_Scaling_Agent_Self_Evolving_with_Reasoning_Memory.pdf]]
