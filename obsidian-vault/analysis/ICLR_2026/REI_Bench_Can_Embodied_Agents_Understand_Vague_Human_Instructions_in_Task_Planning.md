---
title: "REI-Bench: Can Embodied Agents Understand Vague Human Instructions in Task Planning?"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/REI_Bench_Can_Embodied_Agents_Understand_Vague_Human_Instructions_in_Task_Planning.pdf
project_link: https://jcx0110.github.io/rei-bench-project
code_link: null
openreview_forum_id: vmBIF25KLf
aliases:
- TOCCT
- REI-Bench
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "Decoupling referring expression resolution from plan generation allows the LLM to first produce an explicit instruction before planning, reducing object omissions and improving ro..."
primary_logic: "Existing LLM planners over-allocate attention to plan generation, underutilizing their inherent language understanding. Injecting a dedicated context cognition step (TOCC) that rewrites vague instructions into clear ones substantially improves performance without changing the planner architecture."
claims:
- "Implicit REs cause up to 36.9% success rate drop in baseline planners."
- "The main failure mode is object omission, as shown by error analysis."
- "LLMs can actually resolve implicit REs when explicitly prompted, revealing a capacity-suppression issue during planning."
- "TOCC decouples RE resolution and planning, achieving 6.5% average improvement over vanilla LLaMA3.1-8B+SayCan."
---

# REI-Bench: Can Embodied Agents Understand Vague Human Instructions in Task Planning?

> [!tip] 核心洞察
> Existing LLM planners over-allocate attention to plan generation, underutilizing their inherent language understanding. Injecting a dedicated context cognition step (TOCC) that rewrites vague instructions into clear ones substantially improves performance without changing the planner architecture.

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | REI-Bench：具身代理能否理解任务规划中模糊的人类指令？ |
| 英文题名 | REI-Bench: Can Embodied Agents Understand Vague Human Instructions in Task Planning? |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vmBIF25KLf) · [Project](https://jcx0110.github.io/rei-bench-project) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Task-Oriented Context Cognition (TOCC) |
| Dataset | REI-Bench, REI-Bench (Standard Context) |

> [!tip] 效果简介
> - REI-Bench 上，隐式指代表达使基线规划器成功率最高下降 36.9%。
> - REI-Bench 上，Average Success Rate Improvement by TOCC on LLaMA3.1-8B+SayCan 为 TOCC，对比 No TOCC (vanilla)，变化 +6.5%。
> - REI-Bench (Standard Context) 上，Object Omission Error Rate (Implicit REs) reduction by TOCC 为 40.1%，对比 53.9%，变化 -13.8%。

## 概要

### 问题瓶颈

基于大语言模型（LLM）的机器人任务规划器在多轮人机对话中无法有效解析**隐式指代表达（Implicit Referring Expressions, REs）**——即人类使用“加热过的那个”而非“土豆”这类模糊指代时，规划器会出现严重的对象遗漏，导致任务成功率大幅下降。现有LLM规划器将注意力过度分配给计划生成，抑制了其固有的语言理解能力，这是造成该瓶颈的深层原因。

### 核心结论

本文提出**REI-Bench**——首个系统建模模糊指代表达的机器人任务规划基准，并揭示了以下关键发现：

1. 隐式REs可使基线规划器的成功率**下降高达36.9%**，主要失效模式为对象遗漏。
2. LLM本身**具备解析隐式REs的能力**，但在直接生成规划时该能力被抑制——当通过显式提示引导时，LLM能够正确解析指代。
3. 将指代解析与规划生成**解耦**是有效的解决路径：先让LLM将模糊指令重写为清晰指令，再基于清晰指令进行规划，可显著降低对象遗漏率并提升鲁棒性。

### 方法定位

本文提出的**面向任务的上下文认知（Task-Oriented Context Cognition, TOCC）**方法，属于**规划前置的指令消歧模块**，位于LLM规划器的输入端。TOCC不改变规划器架构，仅通过一个轻量级重写步骤，将含隐式REs的原始指令转化为显式清晰指令（$I_{\mathrm{clear}}$），再送入下游规划器。该方法与Aware Prompt（AP）、Chain-of-Thought（CoT）、In-Context Learning（ICL）等提示工程方法形成对比，在效果和效率上均表现更优。

### 主要结果

- **整体提升**：TOCC在LLaMA3.1-8B+SayCan上实现平均成功率提升**6.5%**。
- **错误削减**：在标准上下文的隐式REs条件下，对象遗漏错误率从53.9%降至**40.1%**，降低了13.8个百分点。
- **效率优势**：TOCC仅增加3.95%的token消耗和26.18%的推理延迟，远优于CoT和ICL方法。
- **消融验证**：移除上下文记忆会导致对象遗漏率急剧上升，确认上下文对隐式RE解析的必要性；AP方法在显式指令上可能出现性能退化（幻觉），ICL在小模型上甚至导致性能下降。

### 局限与开放问题

当前工作仅聚焦于指代表达这一种语言模糊类型，未涉及指示语、句法模糊等其他形式；实验在AI2-THOR模拟器上进行，且受限于7B–9B参数级别的端侧部署约束，更大模型的行为有待验证。如何将分析扩展到多模态感知环境、长时域任务以及更大规模模型，是值得进一步探索的方向。



### 具身任务规划中的指令模糊性挑战

在人类与机器人的自然交互中，指令往往携带大量模糊的指代表达（Referring Expressions, REs）。例如，“把那个加热过的拿过来”中的“加热过的”就是一个隐式指代，它依赖于对话历史中的上下文记忆才能被正确解析为具体物体（如“土豆”）。然而，当前主流的基于大语言模型（LLM）的机器人任务规划器——包括 **SayCan**、**DAG-Plan**、**HPE** 和 **LLM+P** 等框架——在设计上默认接收的是指代明确的指令，缺乏对多轮对话中隐式指代的系统建模能力。

这一能力缺口导致了严重的性能退化。在 REI-Bench 基准测试中，隐式指代的存在使基线规划器的任务成功率最高下降了 **36.9%**。以 LLaMA3.1-8B+SayCan 为例，其成功率从显式指代场景下的 57.7% 骤降至隐式指代场景下的 46.9%。这表明，指代模糊性已成为制约 LLM 规划器在真实人机交互场景中可靠运行的核心瓶颈。

### 失败根源：物体遗漏而非执行错误

深入分析失败模式后，一个关键的因果机制浮出水面：隐式指代导致的主要失败形式是**物体遗漏（Object Omission）**，而非动作执行错误。当指令中的指代变得模糊时，规划器倾向于完全忽略需要被操控的目标物体，直接跳过相关子任务。数据表明，随着指代隐式程度从 Explicit 提升到 Implicit，LLaMA3.1-8B 的物体遗漏错误率从 22.6% 急剧攀升至 53.9%，而执行错误率反而从 30.5% 下降至 24.0%。这说明 LLM 并非“做错了”，而是“没看见”——它在生成规划时过度分配了注意力给动作序列的编排，从而抑制了其本应具备的语言理解能力。

### 被抑制的能力：LLM 其实能理解隐式指代

一个反直觉的发现进一步揭示了问题的本质：当通过人工反思提示（Reflection Prompt）显式地引导 LLM 去解析隐式指代时，它能够正确识别目标物体（如 Figure 3 中行所示）。这意味着，LLM 的语言理解能力并未丧失，而是在端到端规划生成的过程中被“压制”了。现有的规划框架将指代消解与计划生成耦合在单次推理步骤中，导致模型注意力资源竞争，最终牺牲了语言理解的质量。

### 现有缓解方案的局限

针对这一问题，研究者尝试了多种提示工程方法，包括：
- **Aware Prompt（AP）**：在提示中显式告知模型指令可能存在模糊性；
- **Chain-of-Thought（CoT）**：引导模型逐步推理后再生成计划；
- **In-Context Learning（ICL）**：在上下文中提供指代消解的示例。

然而，这些方法效果有限。AP 在多数场景下有所改善，但在显式指代场景下反而可能引发幻觉，导致性能下降；CoT 优于 AP，但仍未能充分释放 LLM 的语言理解潜力；ICL 在小规模 LLM（7B–9B）上甚至导致性能退化，可能源于有限的上下文学习能力。这些结果表明，仅仅在提示层面“提醒”模型是不够的，需要从架构上对问题求解流程进行结构性调整。

### 本文动机与核心思路

基于上述分析，本文的核心动机在于：**解耦指代消解与任务规划**，让 LLM 先专注于理解“到底要做什么”，再生成可执行的动作序列。为此，我们提出了 **Task-Oriented Context Cognition（TOCC）** 方法，它通过在规划前插入一个独立的“上下文认知”步骤，将模糊的人类指令重写为清晰、无歧义的显式指令 $I_{\mathrm{clear}}$，然后再输入到原有的规划器中。这一设计不改变规划器本身的结构，仅通过调整输入信息的质量来提升整体鲁棒性，兼顾了效果与部署效率。



## 核心方法与创新机理

现有LLM驱动机器人任务规划器在解析多轮人机对话中的**隐含指称表达（Implicit Referring Expressions）**时存在严重能力缺口，导致对象遗漏率急剧上升，任务成功率最高下降**36.9%**（Abstract）。本工作的核心洞察在于：**LLM并非缺乏语言理解能力，而是在规划生成过程中过度分配注意力，抑制了其对模糊指称的解析能力**。证据来自Figure 3中行：当通过人类反思提示显式引导LLM进行指称消解时，LLM能够正确识别隐含指称所指的对象。

基于此洞察，本文提出**任务导向的上下文认知（Task-Oriented Context Cognition, TOCC）**方法，其关键创新在于**将指称表达解析与规划生成解耦**。具体而言，TOCC改变了规划器的输入槽位——将原始可能模糊的指令替换为经过解析的显式指令 $I_{\mathrm{clear}}$。这一改动通过以下流程实现：

1. **提示构建（promptTOCC）**：构造一个重写查询，强制LLM解析上下文中的隐含指称并生成清晰指令。
2. **指令重写**：LLM执行 $I_{\mathrm{clear}} \leftarrow M(\text{promptTOCC})$，将模糊的人类指令改写为显式、无歧义的形式。
3. **规划生成**：LLM规划器使用 $I_{\mathrm{clear}}$ 而非原始指令进行动作生成。

与AP（Aware Prompt）、CoT（Chain-of-Thought）、ICL（In-Context Learning）等基线提示方法相比，TOCC的独特优势在于**不改变规划器架构本身**，仅在输入端注入一个专用的上下文认知步骤。实验表明，TOCC在LLaMA3.1-8B+SayCan上取得平均**6.5%**的成功率提升（Section 4.3），同时将Implicit REs下的对象遗漏错误率从**53.9%降至40.1%**（Table 3），而引入的额外开销仅为token量增加3.95%、推理延迟增加26.18%（Table 6），远优于CoT/ICL。

值得注意的是，AP在某些Explicit REs场景下反而导致性能下降，这一反直觉现象（Section 4.3）进一步印证了核心洞察：简单地让LLM“意识到”模糊性并不足够，关键在于在规划前完成指称消解。移除上下文记忆的消融实验则证实，上下文是隐含指称解析的必要条件——在Explicit REs下性能与TOCC相当，但在Mixed REs下急剧下降（Section 4.3）。



![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_vmBIF25KLf/figures/002_Table_1.jpg]]
*Table 1: Comparison of REI-Bench with existing datasets and benchmarks*

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_vmBIF25KLf/figures/004_Figure_3.jpg]]
*Figure 3: Addressing implicit referring expressions in task planning. Top row: LLM succeeds with explicit REs (“potato”), but misidentifies the object with implicit REs (“the heated one”). Middle row: a reflection prompt from humans can guide the LLM to resolve the implicit REs and identify the correct object. Bottom row: Comparison among different prompting methods, including aware prompt (AP), chain-of-thought (CoT), in-context learning (ICL), and our task-oriented context cognition (TOCC)*

REI-Bench 的整体工作流围绕一个核心发现展开：现有 LLM 任务规划器在生成计划时过度分配注意力，导致其未能充分利用固有的语言理解能力来解析隐式指代表达式（RE）。基于此，框架被设计为**解耦指代消解与计划生成**，从而在不改变规划器架构的前提下，系统性地提升机器人在模糊指令下的任务成功率。

### 问题建模与流水线总览

框架将人机对话中的任务规划建模为一个两阶段问题：首先，机器人接收包含上下文记忆的多轮对话指令；其次，规划器需基于当前指令和上下文生成可执行的动作序列。核心瓶颈在于，当人类指令包含隐式 RE（如“加热过的那个”而非“土豆”）时，LLM 规划器会因注意力被计划生成占据而无法正确消解指代，导致**对象遗漏错误**急剧上升（从 Explicit REs 下的 22.6% 飙升至 Implicit REs 下的 53.9%，LLaMA3.1-8B+SayCan，Table 2）。

为解决此问题，论文提出了 **Task-Oriented Context Cognition (TOCC)** 方法，其流水线由三个模块串联构成：

1. **Prompt 构造（prompt_TOCC）**：将原始模糊指令 *I* 与任务模板 *T_TOCC* 组合，形成一个强制 LLM 进行指代消解的改写查询。
2. **指令改写（M(prompt_TOCC)）**：LLM 基于上下文记忆，解析隐式 RE 并将指令重写为显式、无歧义的形式 *I_clear*。
3. **计划生成（M(prompt_plan)）**：规划器以 *I_clear* 为输入，在环境状态 *S* 的约束下生成可执行动作序列 *a*。

整个流程可形式化为：
- *I_clear ← M(prompt_TOCC)*
- *a ← ConstrainedDecode(M, prompt_plan, S)*

### 基准构造与评估维度

REI-Bench 的基准构造流水线（Figure 2）从 ALFRED 数据集的种子指令出发，分三步生成多层次的模糊性测试样本：

1. **上下文记忆生成**：利用 GPT-4o-mini 基于文本化的模拟器场景描述，扩展种子指令的对话上下文。
2. **上下文变体构造**：生成三种上下文类型——**Standard**（完整上下文）、**Noised**（插入歧义名称噪声）、**Short**（截断上下文），以模拟真实人机交互中的信息不完整性。
3. **RE 隐式化替换**：采用 CoT 策略，依据 OntoNotes 中的替换示例，将指令中的显式 RE 按比例替换为隐式 RE，形成三个难度等级——**Explicit REs**（全部保留显式 RE）、**Mixed REs**（部分替换）、**Implicit REs**（全部替换）。

由此，基准形成 3×3 的评估矩阵（三种上下文类型 × 三种 RE 难度），覆盖九种不同程度的指代模糊性。

### 方法对比与输入输出流

在 TOCC 之外，论文对比了三种基线提示方法，以验证“解耦”策略的必要性：

- **Aware Prompt (AP)**：在规划提示中直接告知 LLM 当前指令可能存在模糊性，但不改变输入结构。
- **Chain-of-Thought (CoT)**：要求 LLM 在生成计划前先进行逐步推理，但仍将推理与计划耦合在同一次生成中。
- **In-Context Learning (ICL)**：提供少量示例，但受限于小模型（7B-9B）的上下文学习能力，反而导致性能退化。

TOCC 与上述方法的本质区别在于**输入流的改变**：基线方法均以原始模糊指令直接驱动计划生成，而 TOCC 在计划生成前插入了一个独立的“认知”阶段，将输入从 *I* 转换为 *I_clear*。这一解耦使得 LLM 能够在不受计划生成干扰的情况下，专注于指代消解——实验表明，LLM 在显式提示下**本就具备**消解隐式 RE 的能力（Figure 3 中行），只是在耦合生成时该能力被抑制。

### 关键证据与效率权衡

TOCC 在 LLaMA3.1-8B+SayCan 上实现了平均 6.5% 的成功率提升（Figure 5），并将 Implicit REs 下的对象遗漏率从 53.9% 降至 40.1%（Table 3）。同时，TOCC 的 token 开销仅比 vanilla 规划器增加 3.95%，推理延迟增加 26.18%，远低于 CoT 和 ICL 的额外开销（Table 6），在效率与性能之间取得了较好的平衡。

**需要人工核实**：Figure 1 的框架示意图中是否明确标注了 TOCC 模块与规划器之间的解耦关系，以及 *I_clear* 在流水线中的位置。若图示不够清晰，建议在正文中补充对模块间数据流的文字描述。



TOCC 的设计动机源于一个关键发现：LLM 在直接生成规划时，其注意力过度分配给动作序列的生成，导致其固有的语言理解能力被抑制——即 LLM 实际上具备解析隐式指代表达的能力，但在联合执行规划与指代消解时无法有效调用该能力。Figure 3 的中行实验证实了这一点：当人类提供反射性提示引导 LLM 先解析指代时，LLM 能够正确识别目标对象。

基于此，TOCC 将指代表达消解与规划生成解耦为两个串行阶段。其核心模块与数据流如 Algorithm 1 所述：

1. **Prompt 构建模块 (promptTOCC)**：根据任务模板 $T_{\text{TOCC}}$ 与原始模糊指令 $I$ 构建重写查询：
   $$\text{prompt}_{\text{TOCC}} \leftarrow \text{ComposePrompt}(T_{\text{TOCC}}, I)$$
   该模板强制 LLM 将指代消解作为独立任务完成，而非作为规划过程的附属步骤。

2. **指令重写模块**：LLM $M$ 接收 $\text{prompt}_{\text{TOCC}}$，在对话上下文的辅助下解析所有隐式指代表达，输出消歧后的明确指令 $I_{\text{clear}}$：
   $$I_{\text{clear}} \leftarrow M(\text{prompt}_{\text{TOCC}})$$
   $I_{\text{clear}}$ 是经过指代消解和语言重组后的简洁、无歧义指令。该步骤是 TOCC 区别于其他提示方法的核心——AP 仅让 LLM 意识到模糊性存在，CoT 让 LLM 在生成规划的同时进行推理，而 TOCC 将指代消解作为独立的前置认知步骤完成。

3. **规划生成模块**：下游规划器接收 $I_{\text{clear}}$ 替代原始模糊指令，在技能集 $S$ 的约束下生成可执行动作序列：
   $$a \leftarrow \text{ConstrainedDecode}(M, \text{prompt}_{\text{plan}}, S)$$

该解耦设计的因果机制在于：将指代消解从规划生成的注意力竞争中剥离，使 LLM 在两个阶段分别集中处理语言理解与动作规划，从而显著降低因指代解析失败导致的对象遗漏错误。Table 3 的消融实验验证了这一机制——TOCC 在 Implicit REs 条件下将对象遗漏错误率从 53.9% 降至 40.1%，而移除上下文记忆的对照组（-Context）则出现对象遗漏率的急剧上升，进一步证实上下文在指代消解阶段的关键作用。



## 实验与关键发现

### 核心瓶颈：隐式指代表达式导致任务成功率大幅下降

REI-Bench的基准测试揭示了当前LLM任务规划器的一个关键瓶颈：多轮人机对话中的隐式指代表达式（Implicit REs）会严重削弱规划性能。在标准上下文（Standard Context）条件下，随着指令从显式REs过渡到混合REs再到隐式REs，所有测试模型的成功率均出现系统性下降。以LLaMA3.1-8B+SayCan为例，其在显式REs下的成功率为57.7%，但在隐式REs条件下降至46.9%，降幅达10.8个百分点；而整体上，不同规划器框架的成功率降幅最高可达**36.9%**（Abstract）。这一结果表明，模糊的指代关系是当前LLM规划器在实际部署中的主要性能瓶颈。

### 失败模式归因：对象遗漏是主导性错误类型

为理解性能下降的根本原因，论文将规划错误分为两类：**对象遗漏错误**（Object Omission Error）和**执行错误**（Execution Error）。表2（Standard Context）的数据显示，随着隐式REs比例增加，对象遗漏错误率急剧上升，而执行错误率反而下降：

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_vmBIF25KLf/figures/018_Table_2.jpg]]
*Table 2: Error rates (%) for the object omission and execution error types in different benchmark models. Results under the “Standard Context” for three types of implicit REs are reported*

- **GPT-4o-mini**：对象遗漏率从显式REs的7.1%飙升至隐式REs的46.2%，执行错误率则从47.9%降至29.5%。
- **LLaMA3.1-8B**：对象遗漏率从22.6%升至53.9%，执行错误率从30.5%降至24.0%。
- **Deepseek-8B**：对象遗漏率从33.0%升至56.9%，执行错误率从40.0%降至28.4%。

这一趋势说明，隐式REs的核心危害在于**导致规划器无法正确识别和保留目标对象**，而非在已知对象的前提下执行错误。当指令中缺乏明确的物体名称时，LLM倾向于在规划过程中“丢失”关键对象，直接导致任务失败。

### TOCC的有效性：解耦指代消解与规划生成

TOCC（Task-Oriented Context Cognition）通过在规划前将模糊指令重写为清晰形式，显著缓解了上述问题。在LLaMA3.1-8B+SayCan上，TOCC取得了**平均6.5%的成功率提升**（Section 4.3）。表3的细粒度错误分析进一步证明了TOCC的作用机制：

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_vmBIF25KLf/figures/019_Table_3.jpg]]
*Table 3: Error rates (%) for the object omission and execution error types under different prompting methods (for LLaMA3.1-8B with “Standard Context”)*

- 在隐式REs条件下，对象遗漏率从基线（无TOCC）的**53.9%降至40.1%**，降幅达13.8个百分点。
- 在混合REs条件下，对象遗漏率从38.8%降至33.1%。
- 在显式REs条件下，整体错误率从53.1%降至41.0%，降幅为12.1个百分点。

这表明TOCC的核心贡献在于**恢复了LLM在规划过程中被抑制的指代消解能力**，使规划器能够正确识别并保留目标对象。值得注意的是，即使在显式REs条件下TOCC也带来了改进，说明其指令重写过程不仅消解了指代歧义，还可能通过重新组织语言使指令更加清晰。

### 消融实验：不同提示方法的对比

论文系统比较了四种缓解策略：感知提示（AP）、思维链（CoT）、上下文学习（ICL）和TOCC。在LLaMA3.1-8B+SayCan上（Figure 5）：

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_vmBIF25KLf/figures/016_Figure_5.jpg]]
*Figure 5: Success rates (%) of various prompting methods applied to LLaMA 3.1-8B and Qwen2.5- Explicit REs & Mixed REs & Mi7B models with the SayCan framework on the REI dataset*

- **AP**在多数场景下有所改善，但在部分显式REs场景中**性能反而下降**，表明单纯让模型“意识到”模糊性可能导致过度纠正或幻觉。
- **CoT**优于AP，但仍不及TOCC。其逐步推理过程虽然有助于指代消解，但未能将消解结果与规划过程有效解耦。
- **ICL**在几乎所有类别中**导致性能退化**，可能原因是较小的LLM（7-9B参数）的上下文学习能力有限，提供的示例反而引入了噪声。
- **移除上下文记忆**（-Context）在显式REs下性能接近TOCC，但在混合和隐式REs下**性能急剧下降**，确认了对话上下文对于隐式指代消解的必要性。

### 效率分析：TOCC的轻量性

TOCC在提升性能的同时保持了较高的计算效率。表6（Appendix A.5）显示，与原始SayCan相比，TOCC的总token使用量仅增加**3.95%**，推理延迟增加**26.18%**。相比之下，CoT方法的token使用量是原始方法的2倍以上，ICL的延迟增加更为显著。TOCC的效率优势源于其简洁的设计——仅需一次额外的指令重写步骤，而非在规划过程中进行复杂的多步推理。

### 失败案例定性分析

Figure 6展示了一个典型失败案例（Mixed REs & Short Context，LLaMA3.1-8B+SayCan）。在该场景中，由于上下文信息不足且存在干扰物体，规划器错误地将目标物体放置在了错误位置。这一案例揭示了短上下文条件下隐式REs消解的双重困难：不仅需要从有限信息中推断指代对象，还需要在多个候选物体中做出正确选择。TOCC通过显式化指令中的指代关系，部分缓解了这一问题，但在上下文极度压缩的场景下仍存在改进空间。

### 评估设置说明

实验在从REI-Bench中通过分层抽样选取的1,000个任务子集上进行（Table 5），保持了原始ALFRED数据集中六种任务类型的分布比例（13.3%-18.5%）。人类基线在随机子集上进行评估作为参考。所有实验均在AI2-THOR模拟器环境中完成，使用相对较小的开源LLM（7-9B参数）以满足机载部署约束。这一设置可能限制了对更大模型行为的推断，需要在实际部署中进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_vmBIF25KLf/figures/015_Figure_4.jpg]]
*Figure 4: Success rate (%) of three task planner frameworks, SayCan, DAG-Plan, and HPE, using three LLMs (GPT-4o-mini, LLaMA3.1-8B, DeepSeekMath-7B), together with an additional “GPT-4o + SayCan” planner and a human baseline on the REI dataset. Explicit, Mixed, and Implicit REs denote three levels of implicit REs in human instructions, and Standard, Noised, and Short Contexts represent three context memory types*



## 定位与知识库关联

### 1. 问题定位：模糊指代在任务规划中的瓶颈

REI-Bench 将问题锚定在人机对话（HRI）中的**指代表达（Referring Expressions, REs）模糊性**上。现有 LLM 任务规划器（如 **SayCan**、**DAG-Plan**、**HPE**、**LLM+P**）在接收清晰、显式指代的指令时表现尚可，但在多轮对话中遭遇隐式 REs（如“加热过的那个”而非“土豆”）时，成功率急剧下降——最大降幅可达 36.9%（Abstract）。错误分析表明，核心失败模式是**对象遗漏（object omission）**：随着隐式 REs 比例升高，对象遗漏错误率显著上升，而执行错误率反而下降（Table 2）。这意味着规划器并非“执行错了”，而是根本“没看到”该操作的对象。

这一发现揭示了一个关键矛盾：LLM **具备**解析隐式 REs 的语言能力（当人类显式提示反思时，LLM 可以正确解析，见 Figure 3 中行），但在端到端规划时该能力被**抑制**。因果机制是：LLM 在单步生成中将注意力过度分配给规划决策，导致对指代消解的语言理解资源不足。

### 2. 方法谱系：TOCC 与现有方法的比较

论文提出的 **Task-Oriented Context Cognition (TOCC)** 是一种**解耦策略**：将指代消解与规划生成分离，先让 LLM 将模糊指令改写为清晰形式 $I_{\mathrm{clear}}$，再送入规划器。这一思路与以下基线方法形成对比：

| 方法 | 策略 | 效果与局限 |
|------|------|------------|
| **Aware Prompt (AP)** | 在提示中注入对模糊性的觉察 | 多数场景有效，但在显式 REs 场景下可能引发幻觉，性能反而下降（Section 4.3） |
| **Chain-of-Thought (CoT)** | 引导 LLM 逐步推理 | 优于 AP，但仍逊于 TOCC；推理步骤在规划上下文中可能偏离核心指代消解任务 |
| **In-Context Learning (ICL)** | 提供少量示例 | 在小模型（7B–9B）上几乎全面退化，可能因上下文学习能力不足（Section 4.3） |
| **TOCC (本文)** | 解耦：先改写为 $I_{\mathrm{clear}}$，再规划 | 在 LLaMA3.1-8B+SayCan 上平均成功率提升 6.5%；对象遗漏率从 53.9% 降至 40.1%（Implicit REs, Table 3） |

TOCC 的本质是**输入槽位变换**：将规划器的输入从原始模糊指令替换为消解后的显式指令。这一变换不改变规划器架构，仅在前端插入一个“上下文认知”模块，由 `promptTOCC` 驱动 LLM 完成改写（Algorithm 1）。效率方面，TOCC 仅增加 3.95% 的 token 消耗和 26.18% 的推理延迟，远优于 CoT/ICL（Table 6, Appendix A.5）。

### 3. 适用边界与局限

**适用边界：**
- TOCC 面向**文本域**的 LLM 任务规划器，在 AI2-THOR 模拟器中验证，尚未在物理机器人上部署。
- 聚焦于**指代表达（REs）** 这一特定模糊类型，不涵盖指示语模糊、句法模糊、辖域模糊等其他语用现象。
- 实验限于 7B–9B 参数的开源小模型（LLaMA3.1-8B、Qwen2.5-7B、DeepSeekMath-7B 等），以满足机载部署约束；更大模型的行为可能不同。

**已知局限：**
1. **模糊类型覆盖窄**：仅建模 REs，未探索其他语用模糊维度（论文明确列为开放问题）。
2. **合成数据偏差**：上下文记忆由 GPT-4o-mini 生成，可能引入系统性偏差。
3. **模拟器与现实差距**：AI2-THOR 无法完全复现真实世界的物理与多模态复杂性。
4. **上下文依赖性强**：消融实验表明，移除上下文记忆后，混合 REs 场景下性能急剧下降（Section 4.3），说明 TOCC 高度依赖上下文的完整性和质量。
5. **额外延迟成本**：虽然优于 CoT/ICL，但相比 vanilla 规划器仍有 26.18% 的延迟增加。

### 4. 知识库定位与开放问题

**在知识谱系中的位置：**
- REI-Bench 是首个**系统建模语用模糊 REs** 的机器人任务规划基准（Table 1 显示其在 Planning、Systematic Vagueness、Multi-turn Context 三个维度上均覆盖，而现有基准如 AmbiK、CLARA、KNOWNO、DialFRED 等至少缺失一个维度）。
- TOCC 属于**轻量级提示工程方法**，与更重型的规划框架（如 LLM+P 的符号规划混合、HPE 的分层规划）正交，可作为插件叠加。

**开放问题：**
1. 其他语用模糊类型（指示语、句法模糊、辖域模糊）如何影响任务规划？能否统一建模？
2. 随着 LLM 规划器能力提升，分析能否扩展到长周期、多目标任务？
3. 融入视觉和空间感知等多模态信息后，模糊指令的解释机制会如何变化？
4. TOCC 能否适配更大规模 LLM，或在零样本设定下无需显式提示工程即可工作？



## 原文 PDF

![[paperPDFs/ICLR_2026/REI_Bench_Can_Embodied_Agents_Understand_Vague_Human_Instructions_in_Task_Planning.pdf]]
