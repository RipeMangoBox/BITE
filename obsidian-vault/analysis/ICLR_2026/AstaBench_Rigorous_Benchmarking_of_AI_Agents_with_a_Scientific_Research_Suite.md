---
title: "AstaBench: Rigorous Benchmarking of AI Agents with a Scientific Research Suite"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AstaBench_Rigorous_Benchmarking_of_AI_Agents_with_a_Scientific_Research_Suite.pdf
project_link: null
code_link: https://github.com/allenai/asta-bench
openreview_forum_id: M7TNf5J26u
aliases:
- AAEAETABS
- AstaBench
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "提供标准化的生产级科学文献检索环境（Asta Scientific Corpus）、冻结成本映射（litellm snapshot）、统一的任务接口和自动评分（agent‑eval 工具包），从而在严格控制工具、成本和日期的条件下公平比较不同代理架构和语言模型的核心科学推理与规划能力。"
primary_logic: "尽管在文献理解和问答上已有可用的代理（部分接近80%得分），但在代码编写、实验执行、数据分析和端到端科学发现等后续环节，当前最佳代理的完成率依然极低（端到端任务成功率最高仅约5%），且开放权重模型与闭源模型之间存在巨大差距；将代理专用工具与基座模型分离并进行成本‑质量联合评价，是推动科学AI从片段能力走向完整研究流水线的关键一步。"
claims:
- "最佳开源代理（开放权重LLM）的整体得分仅为11.1%，而最佳开源代理（闭源LLM）为53.0%，表明LLM质量是主要瓶颈。"
- "尽管单步实验步骤完成率可达~70%，但由于误差累积，端到端完成所有实验步骤的最大成功率仅有5%，表明多步连贯执行是最大的挑战。"
- "Asta v0通过任务路由和专用工具显著超越通用ReAct代理（总体53.0% vs 44.0%），同时gpt‑5在某些基准上相较o3有巨大提升（如SUPER‑Expert +24.8%），证明专用工具设计和模型升级都对性能有独立贡献。"
- "AstaBench 整体（11个子基准的宏平均） 上 宏平均得分（Macro Avg Score） = 53.0% (Asta v0 mixture)"
---

# AstaBench: Rigorous Benchmarking of AI Agents with a Scientific Research Suite

> [!tip] 核心洞察
> 尽管在文献理解和问答上已有可用的代理（部分接近80%得分），但在代码编写、实验执行、数据分析和端到端科学发现等后续环节，当前最佳代理的完成率依然极低（端到端任务成功率最高仅约5%），且开放权重模型与闭源模型之间存在巨大差距；将代理专用工具与基座模型分离并进行成本‑质量联合评价，是推动科学AI从片段能力走向完整研究流水线的关键一步。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AstaBench：基于科学研究套件的AI代理严格基准测试 |
| 英文题名 | AstaBench: Rigorous Benchmarking of AI Agents with a Scientific Research Suite |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=M7TNf5J26u) · [GitHub](https://github.com/allenai/asta-bench) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | AstaBench (with Asta Environment, agent‑eval toolkit, and agent‑baselines suite) |
| Dataset | AstaBench 整体（11个子基准的宏平均）, AstaBench 整体, LitQA2-FullText-Search（文献搜索）, SUPER-Expert（实验复现代码执行） |

> [!tip] 效果简介
> - AstaBench 整体（11个子基准的宏平均） 上，宏平均得分（Macro Avg Score） 为 53.0% (Asta v0 mixture)，对比 44.0% (ReAct with gpt‑5)，变化 +9.0%。
> - AstaBench 整体 上，每次问题的推理成本（美元） 为 0.04 (ReAct with gpt‑5‑mini, 得分32%)，对比 3.40 (Asta v0 mixture, 得分53.0%)，变化 成本降低约两个数量级，但得分下降21个百分点。
> - LitQA2-FullText-Search（文献搜索） 上，检索得分（Recall） 为 90.7 ± 6.6 (Asta Paper Finder)，对比 82.7 ± 8.6 (ReAct with gpt‑5)，变化 +8.0%。

## 概要

### 问题瓶颈

现有AI代理基准套件在评估科学AI代理时存在三个核心缺陷，导致无法公平、严格地衡量其实际研究辅助能力。首先，**缺乏可复现的科学文献搜索工具**：各代理自行选择搜索引擎或定制API，工具访问不可控、结果不可复现。其次，**混杂因素未受控制**：多数基准未报告或仅粗略估计计算成本，且对工具使用级别不作区分，使得性能差异难以归因于代理本身的推理与规划能力。第三，**缺少面向通用代理的标准化任务接口**：任务格式不统一，代理与评估框架紧耦合，集成新代理需要大量工程量。此外，现有基准普遍缺少基于真实产品使用的全面科学任务，未能覆盖从文献理解到端到端发现的完整研究流水线。

### 核心方法定位

AstaBench通过三个关键设计解决了上述瓶颈。**标准化科学文献检索环境**：提供生产级、日期受限的Asta Scientific Corpus，所有代理使用相同的语料库和检索工具，确保评估可复现。**冻结成本映射与时间不变成本计算**：通过agent‑eval工具包使用litellm快照成本图，在排行榜中同时记录得分与成本，形成成本‑质量Pareto前沿分析。**统一任务接口与自动评分**：所有任务共享基于Inspect的标准化输入/输出格式，任何代理只需满足该接口即可评估，显著降低集成成本。在此基础上，AstaBench配备了包含9类Asta专有代理和13类基线代理的agent‑baselines套件，覆盖22个代理类、57个代理实例。

### 核心发现

尽管在文献理解和问答上已有可用的代理（部分接近80%得分），但在代码编写、实验执行、数据分析和端到端科学发现等后续环节，当前最佳代理的完成率依然极低。**端到端任务的最大成功率仅约5%**：尽管单步实验步骤完成率可达约70%，但由于误差累积（假设典型实验含10步，串联成功率约$0.7^{10} \approx 3\%$），多步连贯执行是当前最大的挑战。**开放权重模型与闭源模型之间存在巨大差距**：最佳开源代理（开放权重LLM）的整体得分仅为11.1%，而最佳开源代理（闭源LLM）为53.0%，表明LLM质量是主要瓶颈。**专用工具设计和模型升级对性能有独立贡献**：Asta v0通过任务路由和专用工具显著超越通用ReAct代理（总体53.0% vs 44.0%），同时gpt‑5在某些基准上相较o3有巨大提升（如SUPER‑Expert +24.8%），证明两者均为提升科学AI能力的关键路径。将代理专用工具与基座模型分离并进行成本‑质量联合评价，是推动科学AI从片段能力走向完整研究流水线的关键一步。

### 科学AI代理的现状与瓶颈

近年来，基于大语言模型（LLM）的AI代理在科学研究中展现出巨大潜力，能够辅助文献检索、代码编写、数据分析乃至端到端的科学发现。然而，如何公平、严格地评估这些代理的实际研究辅助能力，仍是一个悬而未决的问题。

现有代理基准套件存在若干根本性缺陷，导致无法对科学AI代理进行可靠的能力诊断：

1. **工具环境不可控**：各代理自行选择搜索引擎或定制API，文献检索结果随时间和工具而异，评估结果无法复现。即便是同一代理，在不同时间运行也可能因论文数据库更新而得到截然不同的分数。

2. **成本等混杂因素未控制**：多数基准未报告推理成本，或仅粗略估计，无法区分“高投入高产出”与“真正高效”的代理。代理可能通过大量调用昂贵模型来掩盖推理能力的不足。

3. **任务接口不统一**：任务格式各异，代理通常与评估框架紧耦合，集成新代理需要大量工程量，阻碍了通用代理的横向对比。

4. **缺乏基于真实产品使用的全面科学任务**：现有基准往往聚焦于单一环节（如文献问答），未能覆盖从文献检索到代码执行、数据分析、端到端发现的完整研究流水线。

这些缺陷使得现有基准无法回答一个核心问题：**当前AI代理距离真正辅助科学家完成完整研究流程还有多远？**

### 本文动机

为填补上述缺口，本文提出 **AstaBench**——一个基于科学研究套件的AI代理严格基准测试平台。AstaBench的核心设计目标有三：

- **可控性**：通过标准化的生产级科学文献检索环境（Asta Scientific Corpus）和冻结的成本映射（litellm快照），在严格控制工具访问、计算成本和文献日期的条件下进行评估，使不同代理架构和语言模型的核心科学推理与规划能力得以公平比较。

- **全面性**：覆盖文献理解、代码与执行、数据分析和端到端发现四大任务类别，包含超过2400个问题，跨越计算机科学、生物学等多个科学领域，且大量问题源自真实用户对Asta代理的实际请求。

- **开放性**：提供标准化的任务接口（基于Inspect），任何代理只需满足该接口即可评估，显著降低集成成本；同时通过排行榜记录分数、成本、代理开放性及工具使用类别，支持外部提交和持续跟踪。

## 核心方法与创新机理

AstaBench 的核心创新在于通过**可控环境、标准化接口和成本‑质量联合评价**三个维度，将科学AI代理的评估从“片段能力”推向“完整研究流水线”的严格度量。其相对于现有基准套件的关键改变体现在以下三个“changed slots”上。

### 文献检索工具：从不可控到生产级可复现

现有代理基准中，文献检索工具通常由各代理自行选择搜索引擎或定制API，导致信息获取能力成为不可控的混杂变量——代理得分差异无法归因于推理能力还是检索质量。AstaBench 通过 **Asta Scientific Corpus** 将这一变量冻结为可控常数：所有代理共享同一套生产级文献检索工具（包括 `snippet_search`、`get_paper` 等 MCP 标准工具），且所有检索结果被严格限制在基准创建日期之前发表的论文（Table 2 中每个基准均有明确的 Date Cutoff）。这一设计使得评估结果不会因新论文的发表而“漂移”，从根本上解决了文献基准的可复现性危机。实验证据表明，即使仅使用标准语料库工具，专用文献搜索代理 **Asta Paper Finder** 在 LitQA2-FullText-Search 上的检索得分达到 90.7 ± 6.6，显著优于通用 ReAct with gpt‑5 的 82.7 ± 8.6（Table 5），验证了“统一语料库 + 专用检索策略”的组合优势。

### 成本评估：从缺失到时间不变的Pareto分析

多数代理基准不报告计算成本，或仅提供粗略估计，无法控制多次调用、缓存命中等因素带来的成本波动。AstaBench 通过 **agent‑eval 工具包**引入基于 litellm 冻结快照的成本映射，实现时间不变的成本计算——无论何时运行评估，同一代理‑模型组合的成本保持恒定。在此基础上，排行榜不仅展示得分，还绘制成本‑分数的 **Pareto 前沿**（Figure 2），使“经济‑质量”权衡可视化。例如，Asta v0 mixture 以 53.0% 的宏平均得分位居榜首，但每次问题成本高达 $3.40；而 ReAct with gpt‑5‑mini 仅以 $0.04 的成本获得 32% 的得分，成本降低约两个数量级（Table 4）。这种显式的成本维度迫使研究社区在追求高分的同时关注计算效率，避免“无上限堆算力”的军备竞赛式评估。

### 任务接口标准化：从紧耦合到即插即用

传统代理基准中，任务格式与评估框架紧耦合，集成新代理往往需要大量工程适配。AstaBench 将所有任务统一为基于 Inspect 的标准化输入/输出格式，任何代理只需满足该接口即可参与评估。这一设计直接体现在 **agent‑baselines Agents Suite** 的规模上：该套件包含 16 个代理类（9 个 Asta 专用代理 + 7 个基线代理），涵盖 ReAct、Smolagents Coder 等通用架构以及 Asta Paper Finder、Asta Scholar QA 等任务专用代理（Table 3）。标准化接口使得在相同环境下公平比较“通用代理 + 强大模型”与“专用代理 + 流程优化”成为可能——实验结果显示，Asta v0 通过任务路由和专用工具设计，在整体得分上比次优的 ReAct with gpt‑5 高出约 9 个百分点（53.0% vs 44.0%，Table 4），同时 gpt‑5 在 SUPER‑Expert 代码执行基准上相较 o3 带来 +24.8% 的巨大提升（Table 8），证明**专用工具设计和模型能力升级对性能有独立且可叠加的贡献**。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_M7TNf5J26u/figures/001_Table_1.jpg]]
*Table 1: AstaBench improves over existing agent benchmark suites in several ways. It tests holistic scientific reasoning (i.e., a broad spectrum of task types and across more than one scientific domain). Many of its problems are inspired by actual user requests to our deployed Asta agents. Its standard tool environment isolates core agentic abilities (e.g., planning, tool-calling, etc.) from information access. AstaBench’s scoring controls for confounders, such as computational cost, and its tasks are defined using a uniform format that supports general-purpose agents. The table’s final column, titled ‘Cls.’, indicates the number of agent classes (e.g., ReAct) that are used to instantiate (e.g., wit...*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_M7TNf5J26u/figures/003_Table_2.jpg]]
*Table 2: AstaBench benchmarks, spanning four task categories: Literature Understanding, Code & Execution, Data Analysis, and End-to-End Discovery. Benchmarks are fully reproducible when paired with the Asta Environment tools listed in the ‘Tools’ column, which come standard with each benchmark: Computational Notebook (Code) or Asta Scientific Corpus (Corpus) tools that restrict to papers before the specified ‘Date Cutoff’ (exclusive). (Original datasets were filtered to ensure questions are answerable with the environment.) ‡For ArxivDIGESTables-Clean, corpus tools are restricted to snippet search with specific paper IDs for each problem. ∗ indicates created by us, and † indicates previously unrelea...*

AstaBench 的整体设计围绕一个核心矛盾展开：现有科学代理基准无法在**可控、可复现且成本透明的条件下**公平比较不同代理架构与语言模型的实际科研辅助能力。其根本瓶颈在于三个层面的混杂——文献检索工具不可复现、计算成本未被系统控制、任务接口缺乏标准化。为此，AstaBench 构建了一条从“统一环境 → 标准化任务 → 自动评分 → 成本‑质量联合排行榜”的完整流水线。

### 流水线总览

系统由四个松耦合模块构成，通过 **Inspect 评估框架**的标准接口串联：

1. **Asta Environment**：提供生产级、日期受限的文献检索工具（Asta Scientific Corpus）与状态化计算笔记本（Computational Notebook），所有代理共享完全相同的工具环境。
2. **标准化任务集**：11 个基准覆盖文献理解、代码与执行、数据分析、端到端发现四类任务，所有任务共享统一的输入/输出格式，任何代理只需满足该接口即可接入评估。
3. **agent‑eval 评估工具包**：基于 Inspect 的基准套件定义层，使用冻结的 litellm 成本快照进行**时间不变的成本计算**，并通过 LLM‑as‑judge 与多维度评分规则（rubric）自动评分。
4. **AstaBench 排行榜**：Web 界面展示每个代理的得分、推理成本、开放性类别（开源/闭源）及工具使用级别（Standard/Custom/Fully custom），同时绘制成本‑分数 Pareto 前沿。

Figure 1 以系统架构图的形式展示了这一流程：多个 Agent+LLM 变体通过标准化工具访问统一任务，经 Rubric 与 LLM Judge 评分后，输出 Accuracy vs Compute Cost 的排行榜。

### 关键模块与因果机制

**Asta Scientific Corpus** 是整个框架可复现性的基石。它提供 `snippet_search`、`get_paper` 等 MCP 标准工具，并强制将所有检索结果限制在基准创建日期之前的论文——这一“日期截止”机制直接切断了新发表论文污染评估结果的可能（Table 2 为每个基准标注了具体截止日期）。与之配合的 **Computational Notebook** 则是一个沙箱化的 Jupyter 执行环境，支持 Python 与 IPython 魔法命令，变量在多次调用间持久化，用于代码编写与实验执行类任务。

**agent‑eval 工具包**解决了成本这一关键混杂变量。它通过冻结 litellm 的成本映射快照，使不同时间运行的评估成本可比，同时计入缓存折扣（但不计入延迟折扣）。在排行榜上，代理按开放性（开源权重/闭源权重/仅 API/仅 UI）和工具使用级别（Standard/Custom/Fully custom）分类，避免混淆不同透明度和工具优势带来的影响。

**agent‑baselines 代理套件**包含 16 个代理类，其中 9 个为 Asta 专有代理（如 Asta v0、Asta Paper Finder、Asta Scholar QA），7 个为通用基线（如 ReAct、Smolagents Coder）。Table 3 详细列出了每个代理类的任务优化方向、开源状态和工具使用级别。Asta v0 通过任务路由和专用工具设计，在整体宏平均得分上达到 53.0%，显著超越次优的通用 ReAct 代理（44.0%），验证了“专用工具+流程设计”的独立价值。

### 输入输出流

- **输入**：每个基准任务以标准化格式定义，包含问题描述、所需工具列表（Corpus/Code/Snippet）、评分规则（rubric）和日期截止。代理接收任务描述后，通过统一接口调用 Asta Environment 中的工具。
- **输出**：代理生成答案后，系统通过 LLM‑as‑judge 结合 rubric 进行自动评分（端到端任务还综合论文、代码、制品三个维度的交叉验证，如 Table 21 所示）；同时记录每次 API 调用的 token 消耗，通过冻结成本映射计算推理成本。最终结果汇聚到排行榜，以得分和成本两个维度展示 Pareto 前沿。

### 方法谱系与知识库定位

AstaBench 在现有代理基准生态中的定位可通过 Table 1 的六维对比清晰呈现。相较于 **SWE‑bench**、**GAIA**、**ScienceAgentBench** 等已有套件，AstaBench 是首个同时满足以下条件的基准：(1) 测试跨领域的整体科学推理能力；(2) 大量问题源自真实产品用户请求；(3) 提供可控、可复现的生产级文献检索工具；(4) 系统控制计算成本等混杂因素；(5) 采用标准化通用代理接口；(6) 覆盖 22 个代理类、57 个代理实例。

在基线方法层面，AstaBench 纳入了 **ReAct**（通用代理基线，无科学任务优化）、**Smolagents Coder**（以代码形式表示动作的通用代理）、**OpenAI Deep Research**（商用闭源文献理解代理）、**FutureHouse Falcon**（仅 API 的商用文献理解代理）、**Elicit**（商用文献报告生成代理）和 **STORM**（开源文献报告生成代理）等。这些基线与 Asta 专有代理的对比，清晰揭示了“专用工具设计”与“基座模型能力”对性能的独立贡献。

### 关键模块

AstaBench 的严格评估能力建立在四个核心模块之上，它们共同实现了工具访问、成本计算和代理接口的标准化控制。

**Asta Scientific Corpus（生产级可复现文献检索工具集）**
这是首个面向代理的生产级可复现科学文献检索环境。它基于 MCP（Model Context Protocol）标准提供 `snippet_search`、`get_paper` 等工具，所有代理通过统一接口访问同一语料库。其关键控制机制是**日期截止过滤**——所有检索结果被限制在基准创建日期之前的论文，防止新发表文献污染评估结果，确保不同时间点的评估可复现（Table 2 中每个基准标注了独立的 Date Cutoff）。

**Computational Notebook（状态化计算笔记本）**
一个在独立沙箱中运行的 Jupyter notebook 执行环境。代理可以通过工具调用执行 Python 代码和标准 IPython 魔法命令，且 Python 变量和环境在多次调用之间持久保持。这种**状态化设计**使代理能够进行多步迭代的数据分析和实验执行，是支撑 Code & Execution 和 End-to-End Discovery 任务的基础设施。

**agent‑eval Evaluation Toolkit（时间不变的成本评估工具包）**
基于 UK AISI 的 Inspect 框架构建，核心创新在于**冻结的成本映射**：通过 litellm 的快照成本图进行时间不变的成本计算，计入缓存折扣但不计入延迟折扣。这使得不同时间提交的代理结果在成本维度上可比。该工具包同时定义了代理的**开放性分类**（开源开放权重/开源闭权重/闭源API可用/仅UI闭源）和**工具使用级别**（Standard/Custom interface/Fully custom），在排行榜中显式标注，避免混淆不同透明度和工具优势带来的影响。

**agent‑baselines Agents Suite（标准化代理实现套件）**
包含 16 个代理类（9 个 Asta 专用代理和 7 个基线代理），所有代理共享 Inspect 兼容的标准化输入/输出接口。这一设计将**代理架构与基座模型解耦**：同一代理类可搭配不同 LLM 实例化，从而在严格控制工具和接口的条件下，独立评估代理架构设计和底层模型能力对科学任务性能的贡献。

### 关键公式

**端到端实验成功概率的指数衰减模型**

$$\text{成功率} \approx 0.7^{10} \approx 3\%$$

- **变量含义**：假设一个典型实验包含约 10 个必须步骤，每步独立成功率约 70%（基于 Table 10 中单步完成率的观测上界），则串联执行的总成功率按指数衰减至约 3%。
- **来源与作用**：该公式用于解释 End-to-End Discovery 任务中极低的整体通过率（Table 20 显示所有代理的最大完成率仅 5%）。它揭示了当前代理面临的核心瓶颈并非单步能力不足，而是**多步连贯执行中的误差累积效应**——即使单步表现合理，串联后的整体成功率也趋近于零。

**类别层次标准误的加权传播公式**

$$\mathrm{SE}_{\mathrm{category}} = \frac{\sqrt{\sum w_i^2 \cdot \mathrm{SE}_i^2}}{\sum w_i}$$

- **变量含义**：$w_i$ 为第 $i$ 个基准的权重，$\mathrm{SE}_i$ 为该基准的标准误，$\mathrm{SE}_{\mathrm{category}}$ 为聚合后的类别级标准误。
- **来源与作用**：该公式用于在聚合多个基准得分（如 Literature Understanding 类别下的多个子基准）时传播不确定性。它假设任务间独立，通过对各任务标准误加权平方和开方再归一化，为排行榜中的置信区间提供计算基础（Appendix D）。

## 实验与关键发现

### 一、整体表现：专用代理与通用代理的成本-质量博弈

AstaBench 在 11 个子基准上对 22 个代理类（共 57 个具体代理）进行了系统评估，结果汇总于 Table 4。核心发现是：**专用科学代理 Asta v0（混合模型）以 53.0% 的宏平均得分位居榜首，比最强的通用代理 ReAct + gpt‑5（44.0%）高出约 9 个百分点**，验证了为科学任务定制工具和工作流的价值。然而这一质量优势伴随着巨大的成本代价：Asta v0 每次问题的推理成本高达 $3.40，而 ReAct + gpt‑5‑mini 仅需 $0.04，得分 32%——成本降低近两个数量级，得分下降约 21 个百分点。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_M7TNf5J26u/figures/006_Table_4.jpg]]
*Table 4: Overall results for agents that can solve all the tasks (additional results in Table 11). Reported values are macro averages over benchmark statistics; confidence intervals are omitted. † denotes models not pinned to a date-stamped version. Bold denotes the agent is on Pareto-optimal frontier for that column pair*

开放权重模型与闭源模型之间存在巨大鸿沟。最佳开源代理（开放权重 LLM）为 Smolagents Coder + Llama‑4‑Scout‑17B‑16E‑Instruct，整体得分仅 11.1%；而最佳开源代理（闭源 LLM）Asta v0 达到 53.0%。这一差距表明，**当前阶段 LLM 的基础能力仍是科学代理性能的首要瓶颈**。

Figure 2 以成本-分数散点图呈现了四个任务类别的 Pareto 前沿。文献理解类别已出现多个接近前沿的高性价比方案；代码执行和数据分析类别中，性能随成本上升的边际收益递减明显；端到端发现类别则整体处于极低得分区间，所有代理的成本-质量均远未达到可用水平。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_M7TNf5J26u/figures/005_Figure_2.jpg]]
*Figure 2: Score vs. cost analysis for overall and category results (from Tables 4, 11, 16 and 17). Points indicate means. Points on the Pareto frontier are connected with dotted lines, representing optimal quality-cost trade-offs for each category (Literature Understanding, Code & Execution, Data Analysis, End-to-End Discovery). † denotes models not pinned to a date-stamped version. Note: the x-axis (cost per answer in dollars) uses a log scale. For more detailed plots for individual categories and benchmarks, see Appendix D*

### 二、分任务类别结果

#### 2.1 文献理解：搜索与问答已接近可用

在文献搜索任务上，专用代理 Asta Paper Finder 在 LitQA2‑FullText‑Search 上取得 90.7 ± 6.6 的检索得分，显著优于 ReAct + gpt‑5 的 82.7 ± 8.6（Table 5）。在 PaperFindingBench 上同样保持领先。这表明**针对文献检索优化的专用工具链（语义查询 + 日期过滤 + 论文 ID 限制）能有效超越通用 ReAct 代理的即兴搜索行为**。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_M7TNf5J26u/figures/007_Table_5.jpg]]
*Table 5: Literature Understanding search benchmarks results (additional results in Table 12). † denotes models not pinned to a date-stamped version. Bold denotes the agent is on Pareto-optimal frontier for that column pair*

文献问答方面（Table 6），Asta Scholar QA 在 ScholarQA‑CS2 上表现突出，商用代理 OpenAI Deep Research 和 Elicit 在 LitQA2‑FullText 上也取得了有竞争力的结果。值得注意的是，部分商用代理在得分接近 80% 的同时，其推理成本远高于开源方案，说明文献理解领域已存在可用的代理能力，但经济性仍是推广障碍。

表格合成任务 ArxivDIGESTables‑Clean（Table 7）上，Asta Table Synthesis 系列代理通过专用表格提取与合成流程，在得分上领先通用代理。Figure 5 的 Pareto 图显示，Asta Table Synthesis + gpt‑5‑mini 以极低成本实现了接近最优的质量，是该任务上性价比最高的方案。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_M7TNf5J26u/figures/020_Table_14.jpg]]
*Table 14: Literature Understanding ArxivDIGESTables-Clean task benchmark results*

#### 2.2 代码执行：模型升级带来跳跃式提升

代码与执行类别（Table 8）揭示了模型代际差异的显著影响。在 SUPER‑Expert（实验复现代码执行）上，ReAct + gpt‑5 取得 41.1 ± 12.9，较 ReAct + o3 的 16.3 ± 9.9 提升了 +24.8 个百分点——这是所有基准中最大的单模型升级增益。然而，在 CORE‑Bench‑Hard⁻ 和 DS‑1000 上，gpt‑5 相较 o3 的提升幅度有限，表明 **gpt‑5 的能力增益具有强烈的任务偏斜性：在需要复杂多步推理和实验设计的代码任务上增益巨大，在相对常规的编程任务上增益温和**。

一个值得警惕的发现是：**部分专用代理在切换到 gpt‑5 后性能反而退化**。这可能是因为专用代理的工作流设计和提示模板针对早期模型（如 o3）进行了深度优化，而 gpt‑5 的行为特征变化破坏了这些精心调校的交互模式。这一现象提出了一个开放问题：如果未来基座模型持续向 ReAct 风格的通用调用模式演进，特定应用的工作流是否将失去竞争优势？

#### 2.3 数据分析：DiscoveryBench 上的瓶颈

数据分析任务（Table 9）以 DiscoveryBench 为评估基准。Asta DataVoyager 等专用代理在得分上略优于通用代理，但整体得分水平仍然较低。成本-分数 Pareto 图（Figure 7）显示，该类别中性能提升高度依赖成本投入，且边际收益递减显著，暗示**数据分析任务的核心瓶颈可能不在于工具设计，而在于模型本身的统计推理和因果发现能力**。

#### 2.4 端到端发现：从“单步可行”到“全流程崩溃”

端到端发现任务是 AstaBench 中最具挑战性的类别。Table 10 显示，尽管单步实验步骤的完成率可达约 70%，但**完成所有必须步骤的端到端成功率最高仅约 5%**（Table 20），多数代理配置下该指标接近零。

这一现象可通过简单的指数衰减模型解释：假设典型实验包含 10 个步骤，每步独立成功率为 70%，则串联完成全部步骤的概率约为：

$$\approx 0.7^{10} \approx 3\%$$

该估算与实际观测的 5% 上限高度吻合，揭示了当前科学代理的根本性局限：**误差在多步串联中呈指数级累积，使得即便单步能力尚可的代理，在端到端科学发现流水线中仍然完全不可用**。E2E‑Bench‑Hard 上的结果更为惨淡，所有代理的完成率均趋近于零，表明当任务难度和步骤数量增加时，现有代理架构缺乏有效的错误恢复和全局规划机制。

### 三、消融分析：专用工具与模型能力的独立贡献

通过对比相同代理架构下不同 LLM 的表现，以及相同 LLM 下不同代理架构的表现，可以分离出工具设计和模型能力的独立贡献：

1.  **专用工具的价值**：在文献搜索和问答任务上，Asta Paper Finder 和 Asta Scholar QA 等专用代理在相同 LLM 下显著优于 ReAct，验证了“**专用工具 + 流程设计**”对特定科学任务的增益（Table 5、Table 6）。

2.  **模型能力的任务偏斜**：在 ReAct 架构下切换 LLM，gpt‑5 在 SUPER‑Expert 上相较 o3 提升 +24.8%，但在其他代码基准上增益有限。这表明**模型升级的收益高度依赖任务类型**，在需要深度科学推理的任务上，模型代际差异被放大。

3.  **代理-模型交互效应**：gpt‑5 对 ReAct 的提升幅度大于对部分专用代理的提升，甚至导致后者性能退化。这暗示**专用代理的工作流设计与特定模型行为深度耦合**，模型升级可能破坏已有的优化假设。

### 四、失败模式与评估可靠性

端到端任务的评分采用 LLM‑as‑judge 结合三维度校验（报告、代码、制品），Table 21 的纠错分析显示：约 16% 的答案中，生成的论文文本声称满足了某评分项，但代码或制品实际并未满足——三维度联合评分成功将这些假阳性纠正为零分。开发集上的人工验证表明 E2E scorer 的判定正确率达 92%，但作者仍坦承 LLM‑as‑judge 存在潜在偏向，特别是对参与评分准则制定的系统可能更宽容。

成本核算基于冻结的 litellm 成本映射，确保了不同时间评估的成本可比性，但不计入延迟折扣和批处理折扣，因此排行榜成本与实际部署的总拥有成本之间可能存在系统性偏差。

### 五、关键结论

综合实验结果，AstaBench 揭示了科学 AI 代理的当前能力边界：

-   **文献理解已接近实用门槛**：最佳代理在搜索和问答上得分接近 80%，且存在高性价比方案。
-   **代码执行和数据分析仍处于早期阶段**：模型升级带来跳跃式提升，但整体得分水平和任务覆盖率有限。
-   **端到端科学发现是当前代理的“不可能任务”**：误差累积导致全流程成功率趋近于零，亟需突破多步规划、错误恢复和全局状态管理能力。
-   **开放权重模型与闭源模型差距悬殊**：整体得分相差约 42 个百分点，LLM 基础能力是首要瓶颈。
-   **专用工具与通用架构的张力**：专用代理在特定任务上优势明显，但模型升级可能破坏工作流优化，未来需探索更鲁棒的代理-模型协同设计范式。

## 定位与知识库关联

### 1. 基准设计谱系：从片段评估到整体科学推理

AstaBench 在基准设计上直接回应了现有代理评估套件的若干结构性缺陷。Table 1 将 AstaBench 与 10 个现有基准套件在六个维度上进行了系统对比，其核心改进可归纳为三个设计原则。

**第一，从单任务片段到整体科学推理。** 早期科学代理基准通常聚焦于单一任务类型——例如文献问答（LitQA2）、代码执行（DS-1000）或数据分析（DiscoveryBench）——而 AstaBench 将 11 个子基准组织为四个递进的任务类别：Literature Understanding、Code & Execution、Data Analysis 和 End-to-End Discovery。这些任务跨越计算机科学、生物学等多个科学领域，且相当比例的问题来源于 Asta 产品用户的真实请求，使评估更贴近实际科研工作流。

**第二，从不可控工具到标准化、可复现环境。** 现有基准通常允许代理自由选择搜索引擎或定制 API，导致工具访问质量成为不可控混杂因素。AstaBench 通过 Asta Scientific Corpus 提供生产级、日期受限的文献检索工具（包括 `snippet_search`、`get_paper` 等 MCP 标准工具），确保所有代理在相同的语料库边界内竞争。这一设计的因果意义在于：将“信息获取能力”从“代理推理与规划能力”中分离出来，使基准能够独立衡量后者的进步。

**第三，从忽略成本到成本-质量联合评价。** 多数基准仅报告准确率，而 AstaBench 通过 agent‑eval 工具包引入基于冻结 litellm 成本映射的时间不变成本核算，并在排行榜上同时展示分数和成本（Figure 2）。这一设计使得研究者可以在 Pareto 前沿上识别经济-质量最优策略，而非单纯追求绝对分数。

### 2. 代理方法谱系：专用工具与通用架构的张力

AstaBench 的代理基线套件（agent‑baselines Agents Suite）包含 16 个代理类，可划分为两大谱系。

**通用代理基线。** 包括 ReAct（无科学任务优化，使用标准工具）和 Smolagents Coder（以代码形式表示动作）。这些代理代表了当前主流的通用代理架构，其性能主要受底层 LLM 能力驱动。实验表明，在相同 ReAct 架构下，将底层模型从 o3 切换为 gpt‑5 可使整体得分提升约 9 个百分点（Table 4），但在不同任务类别上增益高度不均衡——gpt‑5 在 SUPER‑Expert 代码执行任务上带来 +24.8% 的跃升，而在其他基准上增益有限（Section 5）。

**专用科学代理。** Asta 系列包含 9 个针对特定科学任务优化的代理类，如 Asta Paper Finder（文献检索）、Asta Scholar QA（文献问答）、Asta Table Synthesis（表格合成）、Asta DataVoyager（数据分析）和 Asta Panda（端到端发现）。这些代理通过任务路由和专用工具设计，在对应子任务上显著超越通用代理：Asta Paper Finder 在 LitQA2‑FullText‑Search 上达到 90.7 ± 6.6 的检索得分，较 ReAct with gpt‑5 高出约 8 个百分点（Table 5）。

**关键张力。** 专用代理与通用代理之间的性能差距揭示了当前科学 AI 的一个核心矛盾：Asta v0（混合多个专用代理）以 53.0% 的宏平均得分领先 ReAct with gpt‑5 约 9 个百分点（Table 4），但其单问题成本（$3.40）是后者的近两个数量级。更耐人寻味的是，gpt‑5 对某些专用代理（如 Asta Paper Finder、Asta Scholar QA）反而造成性能退化，却大幅提升了 ReAct 的表现（Section 5 discussion）。这一现象暗示：如果基座模型持续朝着 ReAct 风格的通用调用模式优化，特定应用的工作流设计可能面临竞争力衰减的风险。

### 3. 商用代理的定位与局限

AstaBench 还纳入了若干商用科学代理作为外部参照点。OpenAI Deep Research 和 FutureHouse Falcon 在文献理解任务上表现强劲，但受限于仅提供 API 或 UI 访问，无法在所有子基准上完整评估。Elicit 和 STORM 等文献报告生成代理在 ScholarQA‑CS2 等问答任务上提供了有价值的对比基线（Table 6）。然而，这些商用系统在代码执行、数据分析和端到端发现等后续环节的能力未被充分验证，其封闭性也限制了对内部架构和工具使用策略的深入分析。

### 4. 适用边界与局限

AstaBench 的设计选择同时定义了其适用边界。

**可复现性边界。** 所有基准的文献语料库设有日期截止（Table 2），这确保了不同时间的评估结果可复现，但也意味着基准会随科学进步而迅速过时。当前版本的知识截止日期一旦被超越，需要持续添加新问题并更新截止日期以维持有效性。

**领域覆盖边界。** 尽管覆盖了计算机科学、生物学等领域，但在生物医学、材料科学等关键科学领域的任务深度和广度仍然不足（open questions 中明确指出），尚不能全面评估跨领域研究能力。

**成本核算边界。** 成本计算基于冻结的价格映射，计入缓存折扣但不考虑延迟折扣和批处理折扣（Section 4.2），因此无法精确反映实际部署中的总拥有成本。

**评分偏差风险。** 部分任务使用 LLM‑as‑judge 进行主观评分。尽管通过人工验证（E2E scorer 在 dev set 上 92% 正确）和多维度一致性校验（Table 21 展示了如何通过报告、代码、制品三维度交叉验证来纠正假阳性/假阴性），但仍存在评分系统偏向参与评分准则制定的代理的风险（Appendix F.9）。

**端到端任务的实际意义。** 端到端发现任务要求代理完成从文献检索到实验执行、数据分析的完整流程，但当前最佳代理的完整步骤成功率最高仅约 5%（Table 20）。尽管单步完成率可达约 70%，10 个步骤串联后的指数衰减（$\approx 0.7^{10} \approx 3\%$）解释了这一极低成功率。这意味着该基准目前更适合衡量逐步能力而非整体科学发现水平，需要开发更细粒度的诊断工具。

### 5. 开放问题

AstaBench 揭示的若干开放问题指向该领域的未来方向：

1. **评分公平性**：如何改进 LLM‑as‑judge 流程，避免因评分系统参与训练而导致的系统性偏向？
2. **基准保鲜**：面对科学文献的持续增长，如何设计自动更新且不易被污染的基准问题生成机制？
3. **工具集成**：如何将专用科学工具（如 PaperFinder、CodeScientist）无缝集成到通用代理框架中，同时保持后者的灵活性和可维护性？
4. **模型-架构协同演化**：如果基座模型持续为 ReAct 风格调优，特定应用的工作流设计是否将失去竞争优势？这需要更系统的消融研究来分离模型能力与代理架构的独立贡献。
5. **人机协同**：如何在端到端发现任务中引入 human‑in‑the‑loop，使任务既保持挑战性又具备实际科研指导意义？

## 原文 PDF

![[paperPDFs/ICLR_2026/AstaBench_Rigorous_Benchmarking_of_AI_Agents_with_a_Scientific_Research_Suite.pdf]]
