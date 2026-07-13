---
title: "Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Agentic_Context_Engineering_Evolving_Contexts_for_Self_Improving_Language_Models.pdf
project_link: https://ace-agent.github.io
code_link: https://github.com/ace-agent/ace
openreview_forum_id: eC4ygDs02R
aliases:
- AACE
- ACEECSILM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将上下文设计为一种结构化、可演化的“战术手册”，采用增量式增量更新（delta updates）和模块化的生成-反思-整合流程，以防止知识被压缩并保持上下文的丰富性。"
primary_logic: "ACE 不将上下文压缩为简短提示，而是通过生成器、反射器和策展器三个角色协同工作，以增量、条目的方式不断累积、精炼和组织策略，从而在不修改模型权重的前提下实现自我改进的智能体。"
claims:
- "ACE 在智能体基准 AppWorld 上平均准确率提升 10.6%，在金融领域基准上平均提升 8.6%，大幅超过强基线。"
- "增量式增量更新是防止上下文坍缩的关键：移除该设计后 AppWorld 测试集 TGC 和 SGC 分别下降 11.7% 和 27.8%。"
- "ACE 可以在没有真实标签监督下利用执行反馈进行有效自适应，平均仍高出 ReAct 基线 14.8%。"
- "在 AppWorld 排行榜上，使用较小开源模型的 ACE 与排名第一的 IBM CUGA 整体持平，并在更难的测试集上超越后者。"
---

# Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models

> [!tip] 核心洞察
> ACE 不将上下文压缩为简短提示，而是通过生成器、反射器和策展器三个角色协同工作，以增量、条目的方式不断累积、精炼和组织策略，从而在不修改模型权重的前提下实现自我改进的智能体。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 智能体上下文工程：为自我改进的语言模型演化上下文 |
| 英文题名 | Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=eC4ygDs02R) · [GitHub](https://github.com/ace-agent/ace) · [Project](https://ace-agent.github.io) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | ACE (Agentic Context Engineering) |
| Dataset | AppWorld (Agent), Financial Analysis (FiNER + Formula), Financial Analysis (在线, GT 标签) |

> [!tip] 效果简介
> - AppWorld (Agent) 上，Average Score (TGC & SGC across splits) 为 59.4 (离线 + GT 标签)，对比 42.4 (ReAct)，变化 +17.0。
> - AppWorld (Agent) 上，Average Score (在线, 无 GT 标签) 为 59.5，对比 42.4 (ReAct)，变化 +17.1。
> - Financial Analysis (FiNER + Formula) 上，Average Accuracy 为 81.9 (离线 + GT 标签)，对比 69.1 (Base LLM)，变化 +12.8。

## 概要

**核心问题**：现有上下文自适应方法（如整体提示重写或进化搜索）普遍存在**简洁性偏差**与**上下文坍缩**——LLM 倾向于将上下文压缩为简短但信息贫瘠的摘要，导致领域知识丢失，在长期任务中性能急剧下降（Figure 2 展示了一个极端案例：上下文从 18,282 tokens 坍缩至 122 tokens，准确率从 66.7 跌至 57.1）。

**核心思路**：ACE（Agentic Context Engineering）将上下文重新设计为一种**结构化、可演化的战术手册**，通过**生成器-反射器-策展器**三个角色协同，以**增量式条目更新**替代整体重写，持续积累、精炼和组织策略，在不修改模型权重的前提下实现自我改进的智能体。

**方法定位**：ACE 处于上下文工程与智能体自适应的交叉点。与 In-Context Learning（Agarwal et al., 2024）的静态示例不同，ACE 动态演化上下文；与 MIPROv2（Opsahl-Ong et al., 2024）的贝叶斯优化和 GEPA（Agrawal et al., 2025）的进化搜索不同，ACE 采用模块化分工和增量更新；与 Dynamic Cheatsheet（Suzgun et al., 2025）的整体重写不同，ACE 的增量式增量更新从机制上防止上下文坍缩，同时将自适应延迟降低 86.9%、所需 rollout 数量减少 75.1%（Table 4）。

**主要结果**：
- 在智能体基准 AppWorld 上，ACE 平均准确率提升 10.6%（Table 1），即使没有真实标签监督，仍高出 ReAct 基线 14.8%。
- 在金融分析基准上，ACE 平均提升 8.6%（Table 2）。
- 在 AppWorld 排行榜上，使用较小开源模型的 ACE 与排名第一的生产级系统 IBM CUGA 整体持平，并在更难的测试集上超越后者（Figure 5）。
- 消融实验确认：移除增量式增量更新后，AppWorld 测试集 TGC 下降 11.7%、SGC 下降 27.8%，验证了该设计是防止上下文坍缩的核心机制（Table 18）。

**局限与开放问题**：ACE 在缺乏可靠反馈信号（如无真实标签或明确执行结果）时性能可能下降，且对持续对抗性噪声敏感。如何进一步增强无监督环境下的自我校正能力，以及如何将演化上下文与参数高效微调或检索增强生成结合，是值得探索的方向。

### 上下文自适应的两难：简洁性偏差与上下文坍缩

大语言模型（LLM）在执行复杂推理与智能体任务时，其行为高度依赖上下文（context）——包括系统提示、少样本示例以及运行时记忆。近年来的研究试图通过自适应方法动态优化上下文，例如基于贝叶斯优化的提示词优化器 **MIPROv2**（Opsahl-Ong et al., 2024）、基于进化搜索的 **GEPA**（Agrawal et al., 2025），以及测试时自适应记忆方法 **Dynamic Cheatsheet (DC)**（Suzgun et al., 2025）。这些方法在特定场景下取得了进展，但普遍面临一个核心瓶颈：**简洁性偏差（brevity bias）与上下文坍缩（context collapse）**。

当 LLM 被要求对整个上下文进行整体重写（monolithic rewrite）时，它倾向于将上下文压缩为更短、更“精炼”的摘要。这种压缩看似提高了效率，实则系统性地丢失了领域知识、工具使用细节和代码示例等关键信息，导致长期任务中的性能急剧下降。论文中 Figure 2 展示了一个典型例子：整体重写将上下文从 18,282 tokens 压缩至 122 tokens，准确率随之从 66.7 骤降至 57.1。这一现象揭示了现有方法的一个根本矛盾——**自适应过程本身正在破坏上下文的信息丰富性**。

### 现有方法的架构局限

除了上下文坍缩，现有自适应框架在架构设计上也存在明显局限。以 GEPA 和 Reflexion 为代表的方法通常由单一模型同时承担轨迹生成、错误反思和上下文改写三重职责。这种“单模型全流程”的设计缺乏分工，导致反思质量与改写策略难以解耦优化。DC 虽然引入了可累积的策略记忆，但其更新机制仍依赖 LLM 的整体重写，无法从根本上避免知识压缩。

更关键的是，现有方法普遍缺乏主动的**冗余控制与膨胀预防**机制。随着自适应轮次增加，上下文可能被重复或低质量条目污染，进一步加剧性能退化。

### ACE 的核心动机

针对上述缺口，本文提出 **ACE (Agentic Context Engineering)**，其核心动机可概括为三点：

1. **将上下文重新定义为可演化的“战术手册”（playbook）**：ACE 不将上下文视为需要压缩的单一提示文本，而是将其设计为结构化、条目化的子弹列表，每条子弹附带元数据和计数器。这种表示形式天然支持知识的累积与组织，而非压缩。

2. **用增量式增量更新（delta updates）替代整体重写**：ACE 通过生成器（Generator）、反射器（Reflector）和策展器（Curator）三角色协同工作，每次自适应仅产出紧凑的增量条目（delta bullets），由确定性合并逻辑整合到现有上下文中。这从根本上切断了上下文坍缩的因果链条——知识只增不减，除非被主动去重或裁剪。

3. **引入增长-精炼（grow-and-refine）机制平衡扩展与冗余**：ACE 通过语义嵌入进行条目去重，并在上下文长度超过阈值时触发裁剪，确保上下文在持续演化中保持高质量和高信息密度。

简言之，ACE 的动机不是发明更强的推理模型，而是**在不修改模型权重的前提下，通过工程化上下文演化，让任意 LLM 在长期任务中实现自我改进**。

## 核心方法与创新机理

ACE 的核心创新在于将上下文从“静态提示文本”重构为一种**结构化、可演化的战术手册**，并通过模块化的生成-反思-策展流程与增量式更新机制，系统性地解决了现有上下文自适应方法中普遍存在的**简洁性偏差**与**上下文坍缩**问题。

### 1. 上下文坍缩：问题的根源

现有方法（如 Dynamic Cheatsheet）在对上下文进行自适应时，通常依赖 LLM 对上下文进行整体重写。这种“单体重写”机制极易导致上下文坍缩：LLM 倾向于将丰富的领域知识压缩为简短、信息密度低的摘要。如图 2 所示，一次整体重写可将上下文从 18,282 tokens 压缩至 122 tokens，直接导致准确率从 66.7 骤降至 57.1。ACE 的设计正是从机制层面阻断这一坍缩路径。

### 2. 关键设计变更

ACE 相对基线方法的核心设计变更体现在四个关键槽位上：

| 设计槽位 | 基线方法 | ACE 设计方案 | 设计意图 |
|---------|---------|-------------|---------|
| **上下文表示形式** | 单一、整体的提示文本 | 结构化、条目化的子弹列表，附带元数据与计数器 | 防止知识被压缩，保持上下文的信息密度与可检索性 |
| **上下文更新机制** | LLM 整体重写 | 增量式增量更新，使用确定性逻辑合并 | 避免整体重写引发的坍缩，降低自适应延迟与计算成本 |
| **自适应流程架构** | 单一模型负责评估与改写 | 生成器-反射器-策展器三角色分工协作 | 将生成、反思、组织三个认知环节解耦，提升策略结晶质量 |
| **冗余控制与膨胀预防** | 无主动冗余控制 | 增长-精炼机制，通过语义嵌入进行去重与裁剪 | 在持续累积知识的同时防止上下文无限膨胀 |

### 3. 增量式增量更新：防坍缩的核心机制

增量式增量更新是 ACE 防止上下文坍缩的**因果旋钮**。与整体重写不同，ACE 的反射器仅从当前执行轨迹中提取增量教训，策展器将其转化为紧凑的增量条目，随后由非 LLM 的确定性合并器将其集成到现有上下文中。这一设计使得上下文始终保持增长而非被压缩。消融实验提供了决定性证据：移除增量式增量更新后，AppWorld 测试集 TGC 下降 11.7%，SGC 下降 27.8%，充分验证了该机制对性能的关键支撑作用。

### 4. 三角色分工：从单一反思到结构化结晶

ACE 将自适应流程拆分为三个专门化角色：
- **生成器**：基于当前上下文生成推理轨迹与执行代码；
- **反射器**：对轨迹进行反思，提取成功经验与失败教训；
- **策展器**：将反思结果提炼为结构化的增量条目。

这一分工避免了单一模型同时承担“执行-评估-改写”多重任务时的认知负荷问题。消融实验表明，移除反射器或减少迭代轮次会显著降低整体准确率，验证了反思与迭代精炼对性能的独立贡献。

### 5. 增长-精炼：知识累积的平衡机制

ACE 的增长-精炼机制解决了长期自适应中的冗余累积问题。新子弹通过唯一标识符追加到上下文，已有子弹则在原位置更新。随后，系统通过语义嵌入计算子弹间的相似度，对冗余条目进行去重；同时设置裁剪触发阈值，在上下文长度超过限制时移除低信息密度条目。这一机制使得上下文既能在多轮自适应中持续累积领域知识，又能避免因膨胀导致的推理成本失控。

### 6. 无权重修改的自我改进

ACE 的另一个关键创新在于其**不修改模型权重**即可实现智能体的自我改进。通过将上下文作为可演化的外部记忆载体，ACE 使 LLM 在推理时能够访问不断丰富的策略库，从而在不进行任何微调的情况下持续提升任务表现。这一特性使得 ACE 天然适用于模型即服务的场景，无需访问模型内部参数即可部署。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_eC4ygDs02R/figures/006_Figure_4.jpg]]
*Figure 4: The ACE Framework. Inspired by Dynamic Cheatsheet, ACE adopts an agentic architecture with three specialized components: a Generator, a Reflector, and a Curator*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_eC4ygDs02R/figures/003_Figure_1.jpg]]
*Figure 1: Overall Performance Results. Our proposed framework, ACE, consistently outperforms strong baselines across agent and domain-specific tasks*

ACE 将上下文重新定义为一种结构化、可演化的“战术手册”（playbook），而非传统的单一整体提示文本。其核心由一个三角色协同的智能体架构构成，通过模块化的生成-反思-策展流程，实现对上下文的增量式、条目化更新。

### 三角色分工与协作流程

ACE 框架包含三个专门化的角色组件，如图 Figure 4 所示：

1. **生成器（Generator）**：负责根据当前上下文生成推理轨迹和执行代码。生成器接收当前累积的上下文条目，并输出针对具体任务实例的思维链与动作序列。

2. **反射器（Reflector）**：对生成器产生的轨迹进行反思，从中提取成功经验和失败教训。反射器利用执行反馈信号（如代码执行成功/失败、真实标签等）来识别模式，并将观察结果转化为结构化的洞察。

3. **策展器（Curator）**：将反射器的输出提炼为结构化的增量条目（delta bullets），每条条目包含具体策略、元数据和使用计数器。策展器确保新知识的格式与现有上下文一致，为后续的合并操作做准备。

三个角色默认使用相同的基础 LLM（如 DeepSeek-V3.1 的非思考模式），以隔离上下文构建方法本身的贡献，避免更强的反射器或策展器向生成器传递知识优势（§4.2）。

### 增量式增量更新机制

ACE 的核心设计原则是将上下文表示为结构化的条目化子弹列表，而非单一的整体提示（§3.1）。与此对应，ACE 不采用整体重写（full rewrite）来更新上下文，而是通过**增量式增量更新（incremental delta updates）** 机制：

- 反射器和策展器协作产生紧凑的“增量上下文”（delta context），即一小批候选子弹条目。
- 增量合并器（Delta Merger）使用确定性非 LLM 逻辑将新子弹合并到现有上下文中：新标识符的子弹被追加，已有标识符的子弹在原位更新。
- 这一设计从根源上避免了整体重写导致的上下文坍缩（context collapse）——即 LLM 将丰富上下文压缩为简短、信息贫乏的摘要，导致性能急剧下降（Figure 2）。

### 增长-精炼与冗余控制

为平衡上下文的持续增长与冗余控制，ACE 引入**增长-精炼（grow-and-refine）** 机制（§3.2）：

- **增长阶段**：新子弹通过增量合并不断追加到上下文中。
- **精炼阶段**：通过语义嵌入对子弹进行去重（deduplication），移除语义冗余的条目；同时设置裁剪触发长度（pruning trigger），当上下文超过阈值时自动修剪低使用率的子弹。

这一机制确保上下文在长期演化中保持信息密度，既不会因过度压缩而丢失领域知识，也不会因无限膨胀而超出长上下文模型的窗口限制。

### 自适应模式

ACE 支持两种上下文自适应模式：

- **离线自适应（offline adaptation）**：在部署前利用训练集或开发集样本对系统提示（system prompt）进行预热优化，生成高质量的初始上下文。
- **在线自适应（online adaptation）**：在推理过程中根据每个测试样本的执行反馈实时更新上下文，实现持续的策略累积。

两种模式共享相同的生成器-反射器-策展器流水线，区别仅在于自适应发生的阶段和数据来源。

ACE 框架将上下文自适应过程分解为三个专门化角色的协作：**生成器 (Generator)**、**反射器 (Reflector)** 和**策展器 (Curator)**，并通过**增量式增量更新 (Incremental Delta Updates)** 和**增长-精炼 (Grow-and-Refine)** 机制来防止上下文坍缩（Figure 4, §3.0）。

### 生成器 (Generator)

生成器接收当前的结构化上下文（以条目化子弹列表形式组织），生成针对给定任务的推理轨迹和执行代码。其核心作用是将上下文作为“战术手册”来指导 LLM 的行为，而非简单地将上下文视为静态提示（§3.0）。

### 反射器 (Reflector)

反射器对生成器产出的轨迹进行事后分析，从成功和失败中提取具体、可操作的教训。反射器不负责修改上下文本身，而是输出结构化的反思结果，作为后续策展器的输入。消融实验表明，移除反射器会导致 AppWorld 基准上的性能显著下降，验证了其在策略结晶中的关键作用（Table 3, §4.6）。

### 策展器 (Curator)

策展器将反射器的非结构化反思提炼为紧凑的**增量条目 (delta bullets)**——一组候选的上下文更新子弹。每个子弹是独立的、结构化的知识单元，包含元数据（如来源、计数器等），而非对整体上下文的完整重写（§3.1）。

### 增量式增量更新 (Incremental Delta Updates)

与传统方法（如 Dynamic Cheatsheet）通过 LLM 整体重写上下文不同，ACE 采用增量式更新策略：策展器仅生成需要新增或修改的子弹集合，然后由**确定性合并器 (Delta Merger)** 将这些增量条目合并到现有上下文中。合并逻辑不依赖 LLM，从而避免了上下文坍缩——即 LLM 在重写时将详细领域知识压缩为简短、信息贫乏的摘要（Figure 2, §3.1）。

消融实验证实了该设计的核心地位：移除增量更新后，AppWorld 测试集 TGC 下降 11.7%，SGC 下降 27.8%（Table 18, §C.2）。

### 增长-精炼机制 (Grow-and-Refine)

为防止上下文无限膨胀，ACE 引入了增长-精炼机制（§3.2）：

- **增长阶段**：新子弹以附加方式并入上下文，已有子弹在原位更新。
- **精炼阶段**：通过语义嵌入计算子弹间的相似度，进行去重裁剪。冗余子弹被移除，上下文长度被控制在预设阈值内。

该机制的关键超参数包括去重相似度阈值和裁剪触发长度，其敏感性分析见 Table 20 和 Table 21。

### 关键公式与变量

本文未引入新的数学公式或推导。ACE 的核心贡献在于架构设计（模块化角色分工）和上下文更新策略（增量式增量更新 + 增长-精炼），而非新的数学建模。所有模块的实现均基于 LLM 的提示词工程和确定性规则逻辑，不涉及可导出的闭式公式。

## 实验与关键发现

### 核心瓶颈验证：上下文坍缩与简洁性偏差

现有上下文自适应方法普遍面临两个相互关联的失败模式。**简洁性偏差**使得语言模型倾向于将上下文压缩为极简摘要，而**上下文坍缩**则导致领域知识在整体重写过程中被系统性丢失。Figure 2 展示了一个典型案例：上下文从 18,282 tokens 被压缩至仅 122 tokens，准确率随之从 66.7 骤降至 57.1。这一现象揭示了整体式重写的根本缺陷——语言模型缺乏判断“哪些信息对未来任务有价值”的可靠机制，在压缩过程中倾向于保留表面模式而丢弃关键细节。

ACE 通过两项设计直接对抗这一瓶颈：（1）将上下文表示为结构化、条目化的子弹列表，而非单一整体提示文本；（2）采用增量式增量更新替代整体重写。Table 18 的消融实验提供了决定性证据：移除增量更新机制后，AppWorld 测试集 TGC 下降 11.7%，SGC 下降 27.8%，证实增量更新是防止上下文坍缩的核心因果杠杆。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_eC4ygDs02R/figures/025_Table_18.jpg]]
*Table 18: Ablation on Incremental Context Updates (AppWorld, DeepSeek-V3.1). We run offline context adaptation with ACE with/without incremental updates and evaluate on test-normal. Improvements are relative to ReAct*

### 智能体基准主结果

Table 1 报告了 AppWorld 智能体基准上的完整对比结果（基模型为 DeepSeek-V3.1-671B）。在离线自适应设置下（有真实标签监督），ReAct + ACE 达到 59.4% 的平均准确率，相较 ReAct 基线（42.4%）提升 17.0 个百分点，相较 ReAct + ICL 和 ReAct + GEPA 分别高出 12.3% 和 11.9%。在在线自适应设置下（无真实标签，仅利用执行反馈），ACE 仍达到 59.5%，相对 ReAct 基线提升 14.8%，大幅超过 Dynamic Cheatsheet（+7.6%）。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_eC4ygDs02R/figures/007_Table_1.jpg]]
*Table 1: Results on the AppWorld Agent Benchmark (DeepSeek-V3.1-671B as the Base LLM). “GT labels” indicates whether ground-truth labels are available to the Reflector during adaptation. We evaluate the ACE framework against multiple baselines on top of the official ReAct implementation, both for offline and online context adaptation. ReAct + ACE outperforms selected baselines by an average of 10.6%, and could achieve good performance even without access to GT labels*

这一结果的关键意义在于：ACE 在没有真实标签监督的条件下，仅通过代码执行成功/失败等自然反馈信号，就能实现与有监督设置相当的性能。这验证了反射器-策展器流程能够从执行轨迹中提取结构化教训，而非简单依赖标签匹配。

Figure 5 的 AppWorld 排行榜对比进一步强化了这一结论：使用较小开源模型（DeepSeek-V3.1）的 ACE 在整体平均分上与排名第一的生产级系统 IBM CUGA（60.3%）持平，并在更难的 test-challenge 分割上超越后者。这表明 ACE 的上下文工程方法在模型能力受限的情况下仍具有竞争力。

Table 5 和 Table 6 分别报告了 GPT-OSS-120B 和 GPT-5.1 作为基模型的结果，ACE 在所有设置下均保持一致的领先优势，验证了方法的跨模型鲁棒性。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_eC4ygDs02R/figures/012_Table_5.jpg]]
*Table 5: Results on the AppWorld Agent Benchmark (GPT-OSS-120B as the Base LLM). “GT labels” indicates whether ground-truth labels are available to the Reflector during adaptation. We evaluate the ACE framework against multiple baselines on top of the official ReAct implementation, both for offline and online context adaptation*

### 领域特定基准结果

Table 2 展示了金融分析基准（FiNER + Formula）的结果。在离线有标签设置下，ACE 达到 81.9% 的平均准确率，相较基模型（69.1%）提升 12.8 个百分点。在线有标签设置下为 76.6%（+7.5%）。值得注意的是，当缺乏可靠反馈信号时（无标签设置），ACE 和 Dynamic Cheatsheet 均出现性能下降，表明上下文自适应的有效性关键依赖于反馈质量。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_eC4ygDs02R/figures/008_Table_2.jpg]]
*Table 2: Results on Financial Analysis Benchmark (DeepSeek-V3.1-671B as the Base LLM). “GT labels” indicates whether ground-truth labels are available to the Reflector during adaptation. With GT labels, ACE achieves consistent improvements in both offline and online settings, highlighting the advantage of structured and evolving contexts for domain-specific reasoning. However, we also observe that in the absence of reliable feedback signals (e.g., ground-truth labels or execution outcomes), both ACE and other adaptive methods such as Dynamic Cheatsheet may degrade, suggesting that context adaptation depends critically on feedback quality*

在医学推理基准 DDXPlus 上（Table 10），ACE 达到 90.2% 的平均准确率（+15.0%），且在 Challenging 难度子集上增益最为显著。Text-to-SQL 基准 BIRD-SQL 上（Table 11），ACE 达到 52.9%（+5.1%），进一步验证了该方法在结构化推理任务上的泛化能力。

### 消融研究：设计选择的因果贡献

Table 3 的系统消融揭示了 ACE 各组件的贡献层次：

- **移除反射器**：性能显著下降，验证了反思-精炼循环对策略结晶的必要性。
- **减少迭代轮次**：单轮自适应即可获得大部分增益，但多轮迭代（multi-epoch）能进一步累积改进，表明上下文演化具有增量收益特性。
- **离线预热**：在在线自适应前进行离线预热可提供额外的性能提升，说明预训练的上下文知识可作为有效的先验。

Table 16 和 Table 17 检验了反射器质量的鲁棒性。使用较弱反射器模型时，ACE 仍能获得显著增益；仅在持续对抗性更新（每步注入有害反馈）下性能才会低于基线。这表明 ACE 的增长-精炼机制（grow-and-refine）具有一定的噪声过滤能力，但极端对抗场景仍构成风险边界。

### 成本与效率分析

Table 4 报告了 ACE 与 GEPA（离线）和 DC（在线）的成本对比。在 AppWorld 离线自适应中，ACE 将自适应延迟降低 86.9%（9,517s vs. 53,898s），将所需 rollout 数量减少 75.1%（357 vs. 1,434）。在 FiNER 在线自适应中，ACE 将延迟降低 91.5%，将 token 费用降低 83.6%。效率提升的根本原因是增量式增量更新避免了 GEPA 的提示-验证循环和 DC 的重复整体重写。

需要指出的是，ACE 在评估阶段的单次推理 token 用量因上下文增长而增加（Table 15），这可能影响在线服务的延迟。但作者在 §5 中报告的提示缓存研究表明，91.8% 的输入 token 可从缓存服务，实际计费成本降低 82.6%，部分缓解了这一担忧。

### 失败模式与边界条件

综合实验证据，ACE 的主要失败模式包括：

1. **反馈信号缺失或污染**：当缺乏真实标签或明确的执行成功/失败信号时，上下文可能被错误教训污染（Table 2 无标签设置）。
2. **对抗性反射器攻击**：持续注入有害反馈可导致性能降至基线以下（Table 17），表明反射器质量是系统可靠性的关键单点。
3. **领域覆盖有限**：当前验证集中于智能体、金融、医学和 Text-to-SQL 任务，尚未在开放域生成或多模态任务上检验。

## 定位与知识库关联

### 1. 与现有上下文自适应方法的关系

ACE 处于**测试时自适应（test-time adaptation）** 的上下文工程谱系中，其核心目标是在不修改模型权重的前提下，通过优化上下文来提升 LLM 在下游任务上的表现。与现有方法的根本差异在于对“上下文”这一对象的表征和更新方式。

**与 In-Context Learning (ICL) 的关系**：ICL（Agarwal et al., 2024）通过在提示中固定地插入少样本示例来引导模型行为，是静态的上下文增强方法。ACE 继承了 ICL 利用上下文传递领域知识的基本思路，但将其从“静态示例复制”升级为“动态策略累积”——ACE 生成的不是示例本身，而是从成功和失败中提炼出的**可复用策略条目**。实验表明，ReAct + ACE 在 AppWorld 上平均超出 ReAct + ICL 12.3%（Table 1），说明动态演化的策略上下文比静态示例更有效。

**与提示词优化器的关系**：MIPROv2（Opsahl-Ong et al., 2024）和 GEPA（Agrawal et al., 2025）代表了基于搜索的提示词优化路线。MIPROv2 使用贝叶斯优化在离散提示空间中搜索最优组合；GEPA 则通过进化搜索和全量重写来优化提示。ACE 与它们的核心分歧在于**上下文更新的粒度**：GEPA 对提示进行整体重写，这直接触发了“上下文坍缩”（context collapse）问题——LLM 倾向于将长上下文压缩为简短的摘要，导致领域知识丢失（Figure 2 展示了从 18,282 tokens 坍缩至 122 tokens 后准确率从 66.7 降至 57.1 的典型案例）。ACE 通过**增量式增量更新（incremental delta updates）** 替代全量重写，仅添加或修订少量条目，从机制上规避了坍缩。成本对比（Table 4）进一步量化了这一优势：相比 GEPA，ACE 在 AppWorld 离线自适应中将延迟降低 86.9%，所需 rollout 数量减少 75.1%。

**与测试时记忆方法的关系**：Dynamic Cheatsheet（DC, Suzgun et al., 2025）是最接近 ACE 的前驱工作。DC 提出了通过累积可复用策略来改进提示的思路，为 ACE 的“战术手册”隐喻提供了直接启发（Figure 4 明确提及“Inspired by Dynamic Cheatsheet”）。ACE 对 DC 的关键改进在于两点：（1）**结构化表示**——DC 将上下文视为单一文本块，而 ACE 将其表示为带元数据和计数器的条目化子弹列表，使更新和检索更精确；（2）**分工架构**——DC 由单一模型负责评估和改写，ACE 则引入生成器-反射器-策展器（Generator-Reflector-Curator）三角色分工，将“执行”“反思”“组织”解耦。在 AppWorld 在线自适应中，ACE 平均超出 DC 7.6%（Table 1）；在 FiNER 在线自适应中，ACE 将自适应延迟降低 91.5%，token 成本降低 83.6%（Table 4b）。

### 2. 核心设计决策的因果机制

ACE 的性能优势可归因于三个相互耦合的设计选择，消融实验为每个选择提供了因果证据。

**增量式增量更新是防止上下文坍缩的枢纽机制**。移除增量更新（即改用全量重写）后，AppWorld 测试集 TGC 下降 11.7%，SGC 下降 27.8%（Table 18）。这一消融直接验证了全量重写是上下文坍缩的充分条件，而增量更新是其有效解药。增量更新的非 LLM 合并逻辑（确定性 delta merger）同时带来了成本优势——避免了 GEPA 的提示-验证循环和 DC 的重复全量重写。

**反射器-策展器分工是策略结晶的质量保证**。移除反射器（即由生成器直接自我修正）导致性能显著下降（Table 3），证明“执行”与“反思”的分离对于提取高质量教训至关重要。反射器负责从执行轨迹中识别成功模式和失败原因，策展器则将其转译为结构化的增量条目——这种“生成-反思-整合”循环使得上下文中的每条策略都经过显式验证和精炼。多轮反射迭代（multi-epoch）和离线预热（offline warmup）均能进一步提升性能（Table 3），表明策略结晶是一个需要反复打磨的过程。

**增长-精炼（grow-and-refine）机制平衡了知识累积与冗余控制**。ACE 通过语义嵌入进行去重（deduplication）和基于长度的裁剪（pruning），防止上下文无限膨胀。去重阈值和裁剪触发长度的敏感性分析（Table 20, Table 21）表明该机制对超参数具有一定鲁棒性，但极端设置下仍会影响性能——需要在信息保留与上下文长度之间取得权衡。

### 3. 适用边界与失效模式

ACE 的有效性高度依赖**反馈信号的质量**，这构成了其最关键的适用边界。

**无可靠反馈时性能可能退化**。在金融分析基准中，当真实标签不可用且缺乏明确的执行成功/失败信号时，ACE 和 DC 等自适应方法的性能均可能下降（Table 2 的讨论明确指出“context adaptation depends critically on feedback quality”）。这是因为反射器需要可靠的反馈来区分有效策略和无效策略——在信号缺失或稀疏的场景下，反射器可能提取出虚假的“教训”，从而污染上下文。

**反射器的鲁棒性存在边界**。ACE 对反射器质量表现出一定的鲁棒性：即使使用较弱的反射器模型，仍能获得显著增益（Table 16）。然而，在**持续对抗性更新**下（即反射器每 X 步注入一次有害反馈），ACE 的性能可能低于基线（Table 17）。这表明 ACE 缺乏主动检测和过滤恶意反馈的机制——当前的去重和裁剪仅处理语义冗余，而非语义正确性。

**评估阶段的 token 成本权衡**。增量更新大幅降低了自适应阶段的成本，但由于上下文在演化过程中持续增长，评估阶段单次推理的 token 用量会增加（Table 15 显示评估阶段平均输入 token 高于 GEPA）。尽管 prompt-caching 可缓解该问题（§5 报告 91.8% 的输入 token 可从缓存服务，降低 82.6% 的计费成本），但对于无法使用缓存的在线服务场景，长上下文推理的延迟仍是实际部署的考量因素。

### 4. 开放问题

当前工作的边界揭示了若干有待探索的方向：

**无监督/噪声鲁棒的自校正**。ACE 在缺乏真实标签或执行反馈时的退化表明，需要研究如何在反馈稀疏或不可靠的环境中维持上下文质量。可能的路径包括引入不确定性量化、多反射器一致性校验，或利用模型自身的置信度估计来筛选反馈。

**与参数高效微调的混合系统**。ACE 在不修改模型权重的前提下通过演化上下文实现自我改进，这与 LoRA 等参数高效微调方法在机制上互补。上下文演化擅长快速适应和知识累积，参数微调擅长深层行为调整——两者的结合可能产生“上下文引导微调”或“微调增强上下文”的混合范式。

**持续演化中的灾难性遗忘**。在跨领域、持续变化的开放世界场景中，ACE 的增量式知识累积是否会覆盖或遗忘早期学到的有效策略？当前的实验在固定任务分布上进行，未评估任务分布漂移下的长期稳定性。

**更大教师模型与对比反思**。当前 ACE 使用与生成器相同的模型作为反射器。引入更强的教师模型进行对比反思（例如，比较生成器与教师模型的推理差异来提取改进方向）可能进一步提升策略结晶的质量，但需权衡额外的计算成本。

## 原文 PDF

![[paperPDFs/ICLR_2026/Agentic_Context_Engineering_Evolving_Contexts_for_Self_Improving_Language_Models.pdf]]
