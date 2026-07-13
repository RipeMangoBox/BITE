---
title: "WebDevJudge: Evaluating (M)LLMs as Critiques for Web Development Quality"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WebDevJudge_Evaluating_MLLMs_as_Critiques_for_Web_Development_Quality.pdf
project_link: null
code_link: https://github.com/lcy2723/WebDevJudge
openreview_forum_id: CCSPm6V5EF
aliases:
- WB
- WebDevJudge
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "改善模型对功能等价性的识别能力、提升交互式可行性验证的精度与召回率，以及有效缓解位置偏见，是缩小LLM评委与人类专家差距的关键因果调节点。"
primary_logic: "在网页开发等复杂开放性任务中，LLM评委与人类专家存在约15%的性能鸿沟；成对比较范式显著优于单答案评分（平均提升超8%），且评估能力是模型内化技能，外部指导收益有限；智能体工作流受限于规划与执行的累积错误，尚未超越基础模型。"
claims:
- "最优模型GPT-4.1在成对比较下的一致率仅为70.34%，与人类专家的84.56%存在约14%的差距。"
- "成对比较范式在所有类别中显著优于单答案评分，平均提升超过8%。"
- "基于量规树的标注方法将标注者间一致率从65%提升至92%，验证了结构化评估框架的有效性。"
- "智能体工作流（UI-TARS-1.5）未能超越基础模型，主要由于多阶段错误累积，包括规划脆弱和执行不可靠。"
---

# WebDevJudge: Evaluating (M)LLMs as Critiques for Web Development Quality

> [!tip] 核心洞察
> 在网页开发等复杂开放性任务中，LLM评委与人类专家存在约15%的性能鸿沟；成对比较范式显著优于单答案评分（平均提升超8%），且评估能力是模型内化技能，外部指导收益有限；智能体工作流受限于规划与执行的累积错误，尚未超越基础模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | WebDevJudge：评估（多模态）大语言模型作为网页开发质量评审员的评测基准 |
| 英文题名 | WebDevJudge: Evaluating (M)LLMs as Critiques for Web Development Quality |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=CCSPm6V5EF) · [GitHub](https://github.com/lcy2723/WebDevJudge) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | WebDevJudge Benchmark |
| Dataset | WEBDEVJUDGE, WEBDEVJUDGE (Single Answer) |

> [!tip] 效果简介
> - WEBDEVJUDGE 上，Agreement Rate (Pairwise) 为 GPT-4.1 70.34%，对比 Human 84.56%，变化 -14.22%。
> - WEBDEVJUDGE 上，Avg. Improvement (Pairwise vs Single) 为 Pairwise，对比 Single，变化 >8.0%。
> - WEBDEVJUDGE (Single Answer) 上，Agreement Rate (Rubric vs Likert) 为 Rubric higher，对比 Likert，变化 significant (see Figure 3)。

## 概要

**问题瓶颈**：当前LLM评委在网页开发质量评估中的核心瓶颈并非表面的一致率不足，而是其底层能力的三个结构性缺陷：**功能等价性识别失败**（无法识别不同实现方式在功能上的等价性）、**可行性验证失衡**（静态模型精度低而交互式智能体召回低）以及**系统性位置偏见**（即使明确指令也无法消除）。这些缺陷导致最优模型GPT-4.1在成对比较范式下与人类专家仍存在约15%的一致率差距（Table 3），且在交互式任务领域尤为突出。

**核心结论**：在网页开发这类复杂开放性任务中，成对比较范式显著优于单答案评分，平均提升超过8%（Section 4.1）。评估能力本质上是模型内化的技能——直接判断的一致率与使用结构化量规相当，外部指导的边际收益有限（Figure 3）。智能体工作流受限于规划脆弱与执行不可靠带来的多阶段错误累积，其评估性能未能超越基础模型。基于量规树的结构化标注方法将标注者间一致率从65%提升至92%（Table 1），验证了结构化评估框架在提升标注质量上的有效性。

**方法定位**：WebDevJudge构建了一个面向网页开发质量评估的元评估基准，其方法谱系可追溯至MT-Bench（Zheng et al., 2023）和JudgeBench（Tan et al., 2025）等LLM-as-a-judge评测框架，但在三个关键维度上进行了实质性扩展：（1）评估模态从纯文本扩展至代码、网页截图与可交互浏览器环境的多模态组合；（2）标注方法从原始偏好标签升级为基于查询的量规树结构化标注；（3）任务领域从多轮对话转向需同时评估功能、界面、代码和交互的网页开发场景。

**主要结果**：在654个高质量评估实例上，GPT-4.1以70.34%的成对比较一致率领先所有模型，但与人类专家的84.56%仍有显著差距（Table 3）。代码是最关键的评估模态——仅提供代码时性能下降远小于仅提供截图（Table 4）。在可行性验证子任务上，LLM评委呈现高精度低召回特征（GPT-4.1精确率72.1%），而智能体则相反（UI-TARS-1.5召回率70.3%），暴露了两类方法的互补缺陷（Table 6）。模型普遍存在位置偏见，去除偏见后整体一致率变化不大，但偏见本身是模型的内在缺陷（Table 5）。



### 问题背景：LLM-as-a-Judge 的兴起与瓶颈

随着大语言模型（LLM）能力的快速提升，利用LLM作为自动评估者（LLM-as-a-Judge）已成为替代昂贵人工评估的主流范式。从早期的**MT-Bench**（Zheng et al., 2023）到近期的**JudgeBench**（Tan et al., 2025）和**AgentRewardBench**（Lu et al., 2025），研究者持续探索LLM在对话质量、指令跟随等任务上的评估可靠性。然而，这些基准主要局限于静态文本评估，尚未触及一个根本性问题：**在需要同时理解代码、视觉呈现和交互行为的复杂开放性任务中，LLM评委的能力边界究竟在哪里？**

### 现有基准的方法缺口

现有元评估基准存在三个关键缺口：

1.  **评估模态单一**：如MT-Bench仅依赖纯文本对话，无法反映真实世界中多模态、交互式任务的评估需求。
2.  **标注方法粗糙**：多数基准采用原始偏好标签，标注者间一致率较低（如MT-Bench仅63%），缺乏结构化的标注框架来保证标签质量。
3.  **任务领域局限**：现有工作集中于对话或文本指令跟随，尚未涉足需要综合评估功能正确性、界面质量、代码规范和交互体验的网页开发领域。

### 本文动机：网页开发作为理想测试场

网页开发为LLM评估能力的研究提供了独特的测试环境：每个实现可被表示为**源代码**、**渲染截图**和**可交互浏览器环境**三种观察形式，天然支持从静态到动态的多层次评估。然而，这一领域也带来了严峻挑战——评估者必须识别功能等价性（不同实现是否满足同一需求）、验证交互可行性（任务是否可执行），并克服系统性偏见。

为此，本文构建**WebDevJudge**基准，旨在系统性地回答一个核心问题：**当前最先进的（多模态）大语言模型作为网页开发质量的评审员，与人类专家之间还存在多大差距？差距的根源是什么？**



## 核心方法与创新机理

WebDevJudge 的核心创新在于将 LLM-as-a-judge 的元评估从静态文本领域推进到动态、多模态的网页开发质量评审，并围绕三个关键维度重构了评估范式。

**1. 评估模态：从纯文本到多模态交互式环境**

此前的 LLM-as-a-judge 基准（如 **MT-Bench** (Zheng et al., 2023)、**JudgeBench** (Tan et al., 2025)）仅依赖纯文本输入进行静态判断。WebDevJudge 将评估模态扩展为三种互补的观察形式：源代码、渲染截图和完全可交互的浏览器环境（Figure 1）。这一设计使评估能够同时覆盖静态代码质量与动态交互行为，而网页开发任务天然需要同时评估功能、界面、代码和交互，构成了理想的复杂动态评估测试床。

**2. 标注方法：基于查询的量规树结构化标注**

传统基准（如 MT-Bench）依赖原始偏好标签，标注者间一致性较低。WebDevJudge 引入了查询锚定的量规树（query-grounded rubric tree），将高层需求分解为可验证的细粒度标准层次结构。量规树沿三个核心维度组织：意图（intention）、静态质量（static quality）和动态行为（dynamic behavior），每个叶节点对应一个二元检验，其结果逐层聚合至父节点。这一结构化框架将标注者间一致率从 65% 显著提升至 92%（Table 1），且 LLM 自动生成的量规树与人工编写的量规树一致率达到 90%，验证了自动化标注管线的可行性。

**3. 任务领域：聚焦网页开发的复合质量评估**

不同于 MT-Bench 等聚焦多轮对话或纯文本指令跟随的基准，WebDevJudge 将评估对象定位于网页实现的质量比较。任务形式化为偏好评估四元组 $(Q, W_{\mathrm{a}}, W_{\mathrm{b}}, l_{\mathrm{p}})$，其中 $Q$ 为查询需求，$W_{\mathrm{a}}$ 和 $W_{\mathrm{b}}$ 为两个网页实现，$l_{\mathrm{p}}$ 为专家偏好标签。这一领域选择迫使评估者同时处理功能等价性识别、代码质量判断和交互可行性验证等复合挑战，暴露了 LLM 评委在识别功能等价性和验证任务可行性方面的根本性瓶颈——最优模型 GPT-4.1 与人类专家仍存在约 15% 的一致率差距（Table 3）。

**4. 评估范式：成对比较与单答案评分的系统对比**

WebDevJudge 同时支持成对比较和单答案评分两种范式，并发现成对比较在所有类别中平均提升超过 8% 的一致率（Table 3）。这一发现揭示了相对判断作为模型内化能力的特性——在成对比较中，直接判断（无评估标准）的一致率与使用李克特量表或量规相当（Figure 3），表明核心比较能力已内化于模型，外部指导的边际收益有限。



![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/001_Figure_1.jpg]]
*Figure 1: Overview of WEBDEVJUDGE. Left: Data Collection with query-based and environmentbased filtering. Center: Preference label annotation with verifiable rubric tree. Right: Evaluate (M)LLM-based and agentic evaluators under pairwise and single-answer paradigms*

WebDevJudge 基准的整体流水线围绕三个核心模块构建：数据过滤、结构化标注和多范式评估，形成从原始网页实现对到偏好标签再到评估者性能度量的闭环。

**数据过滤模块**采用两阶段清洗策略。第一阶段为查询过滤，从初始的10k+样本中剔除语义模糊或需求不完整的查询；第二阶段为环境验证，确保每个网页实现可在目标浏览器环境中正常渲染和交互。这一流程将原始数据压缩为654个高质量评估实例，覆盖功能实现、界面设计、代码质量和交互行为等多个维度。

**量规树标注模块**是框架的核心创新。系统首先利用少量人工编写的量规树作为示例，驱动大语言模型自动生成结构化量规树。每棵量规树沿三个核心维度展开：意图匹配、静态质量和动态行为。叶节点对应可验证的二元测试，其判定结果自底向上聚合至父节点，最终形成对两个网页实现的综合偏好判断。基于量规树的标注方法将标注者间一致率从65%提升至92%，验证了结构化评估框架在复杂开放式任务中的有效性。

**多模态评估环境**为每个网页实现提供三种观察形式：源代码、渲染截图和可交互浏览器环境。评估者可根据任务类型选择静态或交互式评估模式。框架支持两种主流评估范式：成对比较直接输出偏好判定，单答案评分则通过李克特量表或量规树对单个实现进行多维打分。智能体评估流水线进一步将交互式评估建模为多阶段管道：查询经规划器生成含测试用例的执行计划，由执行器在浏览器中运行测试，最终由总结器综合结果形成判定。

整个框架的输入为评估实例四元组 $(Q, W_{\mathrm{a}}, W_{\mathrm{b}}, l_{\mathrm{p}})$，其中 $Q$ 为网页开发查询，$W_{\mathrm{a}}$ 和 $W_{\mathrm{b}}$ 为两个候选实现，$l_{\mathrm{p}}$ 为专家偏好标签。输出为评估者预测与人类偏好的一致率，以此度量大语言模型和智能体作为网页开发质量评审员的可靠程度。



### 评估实例的形式化表示

WEBDEVJUDGE将网页开发质量评估建模为偏好判断任务。每个评估实例被形式化为一个四元组：

$$(Q, W_{\mathrm{a}}, W_{\mathrm{b}}, l_{\mathrm{p}})$$

其中 $Q$ 表示用户查询（即网页开发需求），$W_{\mathrm{a}}$ 和 $W_{\mathrm{b}}$ 分别代表两个待比较的网页实现，$l_{\mathrm{p}}$ 为专家标注的偏好标签（指示哪个实现更优或二者持平）。这一形式化框架将开放式的质量评估转化为可度量的成对比较问题，为后续的元评估提供了统一的数据结构。

### 数据过滤流水线

基准构建的关键模块是两阶段数据过滤流水线（Table 8）：

1. **查询过滤（Query-based filtering）**：从原始约10k+样本中剔除低质量查询，包括需求模糊、过于简单或无法客观评估的实例。
2. **环境验证（Environment-based filtering）**：在交互式浏览器环境中实际运行网页实现，排除因渲染失败、功能缺失或环境不兼容导致的无效样本。

经过两阶段过滤后，最终保留654个高质量评估实例，覆盖意图匹配、静态质量与动态行为三大维度。

### 量规树标注模块

量规树（Rubric Tree）是WEBDEVJUDGE的核心结构化标注框架，其设计遵循三个关键原则：

- **层级分解**：将高层需求沿三个核心维度（意图、静态质量、动态行为）递归拆解为细粒度子标准。
- **二值化验证**：每个叶节点对应一个可验证的二值测试（通过/未通过），其结果自底向上聚合至父节点，形成层级化判断。
- **自动化生成**：采用少样本LLM生成策略，以人工编写的量规树为示例，自动为每个查询生成结构化量规树。

量规树的引入将标注者间一致率从原始的65%显著提升至92%（人工编写量规）和90%（LLM生成量规）（Table 1），验证了结构化评估框架对降低主观偏见的有效性。

### 多模态评估环境

评估者可通过三种观察形式获取网页实现信息：

- **源代码**：完整的HTML/CSS/JavaScript代码。
- **网页截图**：渲染后的页面视觉呈现。
- **可交互浏览器环境**：支持动态操作与实时反馈的完整交互环境。

这三种模态分别对应静态代码质量、视觉界面质量和动态交互质量的评估需求。消融实验表明，代码是最关键的模态——仅提供代码时性能下降远小于仅提供截图（Table 4），说明代码理解是LLM评委能力的核心瓶颈。

### 智能体评估流水线

对于交互式评估，WEBDEVJUDGE引入智能体工作流，将评估建模为多阶段流水线：

$$\mathrm{Query} \xrightarrow{Planner} \mathrm{Plan\ with\ test\ cases} \xrightarrow{Executor} \mathrm{Results} \xrightarrow{Summarizer} \mathrm{Judge}$$

- **Planner（规划器）**：根据查询生成可验证的评估计划，包含具体测试用例。
- **Executor（执行器）**：在交互式环境中运行测试用例并记录结果。本文采用UI-TARS-1.5（Seed, 2025）作为执行器。
- **Summarizer（总结器）**：综合执行结果，输出最终判断。

### 门控集成策略

为整合LLM评委与智能体评委的互补优势，本文设计了门控集成策略。在单答案量规评估中，意图和静态任务采用LLM判断，动态任务则采用逻辑或集成：

$$Res_{\mathrm{dynamic}} = Agent \lor LLM$$

这一设计的依据来自可行性验证实验（Table 6）：LLM评委在可行性验证中表现出高召回但低精确率（如GPT-4.1精确率72.1%、召回率90.0%），而智能体则相反（UI-TARS-1.5精确率较高但召回率仅70.3%）。逻辑或集成利用LLM的高召回确保不遗漏可行任务，同时借助智能体的高精确率过滤误判，实现互补。实验表明，集成后一致率有边际提升（如GPT-4.1从65.0%升至66.2%）（Table 7），但整体增益有限，说明当前智能体工作流的规划与执行可靠性仍是主要瓶颈。



## 实验与关键发现

### 评估范式对比：成对比较显著优于单答案评分

主实验结果（Table 3）揭示了评估范式对一致率的决定性影响。**成对比较范式在所有模型和类别上均显著优于单答案评分，平均提升超过8个百分点。** 最优模型GPT-4.1在成对比较下达到70.34%的一致率，而其在单答案评分下（使用量规指导）仅为60.55%。这一差距在交互式动态任务上尤为突出：成对比较范式下，GPT-4.1在Dynamic类别上达到67.44%，而单答案评分下仅53.49%，相差近14个百分点。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/005_Table_3.jpg]]
*Table 3: Agreement Rate (%) of different evaluators under different evaluation paradigms. The best average performance of the whole dataset is highlighted in bold and the second best is underlined*

人类专家在成对比较下的一致率为84.56%，与GPT-4.1之间存在约14%的性能鸿沟，表明当前LLM评委在复杂网页开发评估中仍存在显著能力缺口。

**单答案评分内部，二元量规（Rubric）显著优于多级李克特量表（Likert）**（Figure 3）。李克特量表需要模型进行内部校准，将抽象质量映射到5级刻度上，这一过程引入了额外的不确定性。相比之下，二元量规将评估分解为可验证的是/否判断，降低了模型的认知负担。

### 指导策略分析：评估能力是模型内化技能

Figure 3展示了不同指导协议下的一致率对比。在成对比较范式下，**直接判断（无任何评估标准）的一致率与使用李克特量表或结构化量规基本相当**，说明相对判断的核心能力已内化于模型之中，外部指导的边际收益有限。这一发现表明，对于成对比较任务，复杂的提示工程和评估框架并非必需。

然而，在单答案评分范式下，指导策略的影响更加显著。二元量规在所有模型上均优于直接判断和李克特量表，验证了结构化评估框架在绝对评分场景中的价值。

### 模态消融：代码是最关键的评估模态

Table 4展示了输入模态对多模态评估器性能的影响。**代码是评估网页开发质量最关键的模态**：仅提供代码时，模型性能下降幅度远小于仅提供截图。以GPT-4.1为例，仅提供代码时一致率下降约3个百分点，而仅提供截图时下降超过10个百分点。这一结果说明，LLM评委主要依赖代码层面的语义理解进行质量判断，视觉信息虽有助于界面评估，但在功能正确性和代码质量判断中处于辅助地位。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/007_Table_4.jpg]]
*Table 4: Impact of observation forms on the performance of multimodal evaluators. The numbers in parentheses indicate the performance change relative to the setting with both code and image inputs*

### 位置偏见：模型内在系统性缺陷

Table 5揭示了成对比较中的系统性位置偏见。不同模型表现出截然不同的位置偏好模式：Claude-4-sonnet在直接判断下偏好第一个位置（5.7% vs 4.7%），而GPT-4.1则强烈偏好第二个位置（0.9% vs 15.8%）。即使明确指令要求忽略位置信息，偏见依然存在（Appendix E.1），说明这是模型的内在缺陷而非提示工程可解决的问题。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/008_Table_5.jpg]]
*Table 5: Positional bias in pairwise comparison. Preference for specific position, consistency and the absolute difference in agreement rate (∆ AR) between original and swapped orders are reported*

值得注意的是，去除位置偏见后整体一致率变化不大（Table 13），但偏见本身暴露了模型评估机制的脆弱性——模型并非完全基于内容质量做出判断。

### 模糊比较：平局案例是主要错误来源

排除平局案例后（Table 14），所有评估者的一致率大幅提升。GPT-4.1在成对比较下的一致率从70.34%跃升至83.49%，提升超过13个百分点。这一结果表明，**模型在判断两个实现质量相当时的表现远差于判断明确优劣时**，模糊比较是当前LLM评委的主要错误来源。

### 可行性验证：LLM与智能体的互补缺陷

WebDevJudge-Unit子集上的可行性验证实验（Table 6）暴露了两类方法的互补缺陷。**LLM评委表现出高召回、低精度的特点**：GPT-4.1召回率达90.0%，但精确率仅72.1%，说明LLM倾向于过度判断任务为可行。相反，**基于智能体的方法（UI-TARS-1.5）表现出高精度、低召回**：精确率达85.7%，但召回率仅70.3%，说明智能体因操作失败而频繁将可行任务误判为不可行。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/010_Table_6.jpg]]
*Table 6: Performance on the WebDevJudge-Unit for feasibility verification. We report precision (P), recall (R), F1-score, and accuracy (Acc)*

基于这一发现，研究者设计了门控集成策略，对动态任务采用智能体与LLM的逻辑或（$Res_{\mathrm{dynamic}} = Agent \lor LLM$），整合智能体的高精度与LLM的高召回。Table 7显示，集成后一致率有小幅提升（GPT-4.1从65.0%升至66.2%），但整体收益有限，未能从根本上解决可行性验证的挑战。

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/011_Table_7.jpg]]

### 智能体工作流：多阶段错误累积制约性能

尽管智能体工作流在动态任务上表现优于静态LLM评估，但其整体一致率未能超越基础模型（Table 3）。分析表明，**多阶段错误累积是核心瓶颈**：规划器生成的测试计划可能不完备（规划脆弱），执行器在浏览器交互中可能操作失败（执行不可靠），这些错误在流水线中逐级放大。Figure 10中的失败案例展示了智能体因无法在截图中定位目标元素而错误判定任务不可行的典型场景。

### 功能等价性识别失败

Figure 4展示了LLM评委无法识别功能等价性的典型案例。当网页实现使用"Presentation"替代查询要求的"Demonstration"时，部分模型因字面差异而误判为功能缺失，未能理解两者在语义上的等价性。这一失败模式在DeepSeek-R1-0528等深度推理模型上同样存在（Figure 10），说明当前模型的语义理解能力仍不足以处理实现多样性带来的评估挑战。

### 补充图表

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/002_Table_1.jpg]]
*Table 1: Annotation agreement rates with and without the verifiable rubric. The ‘without rubric’ part shows agreements between: (1) annotators and (2) annotators and the original labels. The ‘with rubric’ part shows inter-annotator agreements under human-written and LLM-generated rubrics*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/003_Table_2.jpg]]
*Table 2: Categories and their respective subcategories of queries in WEBDEVJUDGE*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/012_Table_8.jpg]]
*Table 8: Overview of the filtering pipeline, including the number of instances before and after filtering, and the purpose of each filtering stage*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/014_Table_10.jpg]]
*Table 10: Statistics of the generated rubric trees*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/015_Table_11.jpg]]
*Table 11: Details of the agent settings*

![[assets/figures/papers/paper_list_l50_https_openreview_net_forum_id_CCSPm6V5EF/figures/016_Table_12.jpg]]
*Table 12: Statistics of the WebDevJudge-Unit dataset*



## 定位与知识库关联

### 1. 基线对比与增量贡献

WebDevJudge 的核心定位是面向网页开发质量评估的 LLM-as-a-judge 元评估基准。相较于此前以纯文本对话或指令跟随为主的评判基准，WebDevJudge 在三个关键维度上实现了系统性扩展：

**评估模态的升级。** 早期基准如 **MT-Bench** (Zheng et al., 2023) 和 **JudgeBench** (Tan et al., 2025) 仅依赖静态文本输入进行偏好判断，无法捕捉网页开发中代码逻辑、视觉呈现与交互行为之间的复杂耦合。WebDevJudge 将每个网页实现以三种观察形式呈现——源代码、渲染截图和完全可交互的浏览器环境——使评估者能够同时进行静态分析（代码质量、界面设计）和动态验证（功能可行性、交互行为）。这一设计直接回应了 LLM 评委在可行性验证中暴露的精度-召回率权衡问题：LLM 在静态判断中精确率低（GPT-4.1 精确率 72.1%，Table 6），而智能体在交互测试中召回率低（UI-TARS-1.5 召回率 70.3%），两种模态的互补性构成了后续门控集成策略的基础。

**标注方法的结构化。** MT-Bench 依赖原始偏好标签，标注者间一致率仅约 63%。WebDevJudge 引入了基于查询的量规树（rubric tree）标注方法，将高层需求分解为可验证的细粒度二元测试，沿意图、静态质量、动态行为三个核心维度组织。这一结构化框架将标注者间一致率从 65% 提升至 92%（人工编写量规）和 90%（LLM 生成量规）（Table 1），验证了可验证评估标准对标注质量的因果性改善。

**任务领域的特殊性。** 与 **AgentRewardBench** (Lu et al., 2025) 关注通用智能体任务不同，WebDevJudge 聚焦于网页开发这一需要同时评估功能正确性、界面质量、代码规范和交互行为的复合领域。这一选择并非偶然：网页开发的开放性使得“绝对答案”缺乏意义，而偏好比较范式天然适合此类任务——这正是 WebDevJudge 将评估框架建立在成对比较之上的深层原因。

### 2. 方法适用边界

WebDevJudge 的有效性受限于以下边界条件：

- **任务类型边界。** 当前基准包含 654 个实例，覆盖了网页开发的主要子类别（Table 2, Figure 2），但无法代表所有复杂场景。特别是，基准中的交互式任务比例有限，而正是在这类任务上，智能体工作流因规划脆弱和执行不可靠导致的多阶段错误累积最为严重，未能超越基础模型。
- **评估范式边界。** 成对比较范式在所有类别中显著优于单答案评分（平均提升超过 8%，Table 3），但这一优势建立在偏好标签的可靠性之上。偏好标签由少量专家标注，可能受其个人品味与专业背景影响——当评估任务涉及强主观性维度（如界面美学）时，这一偏差可能被放大。
- **模态依赖边界。** 消融实验表明，代码是最关键的模态：仅提供代码时性能下降远小于仅提供截图（Table 4）。这意味着 WebDevJudge 对纯视觉评估场景（如无源码的网页截图比较）的适用性有限，其评估框架内在地偏向于代码理解能力强的模型。
- **位置偏见边界。** 模型存在系统性位置偏见，且仅靠指令无法消除（Table 5）。WebDevJudge 未采用位置交换策略，以模拟真实单次评估场景，但这意味着在需要高可靠性的生产环境中，位置偏见可能成为隐蔽的失败源。

### 3. 已知局限与开放问题

**核心性能鸿沟。** 最优模型 GPT-4.1 在成对比较下的一致率仅为 70.34%，与人类专家的 84.56% 存在约 14% 的差距（Table 3）。排除平局案例后，GPT-4.1 一致率升至 83.49%（Table 14），说明模糊比较（tie）是主要错误来源。这一发现指向一个深层问题：LLM 评委在需要精细区分“几乎等价”的实现时，缺乏人类专家那种基于领域经验的直觉判断能力。

**功能等价性识别的根本困难。** LLM 评委倾向于因字面差异而误判功能等价性——例如将“Presentation”与“Demonstration”视为不同需求（Figure 4），尽管两者在网页语境中功能等价。这是当前评估框架中最难根除的失败模式，因为它要求模型具备语义层面的意图理解，而非简单的模式匹配。

**智能体工作流的悖论。** 尽管智能体工作流在理论上更适合交互式动态评估，其实际表现未能超越基础模型。原因在于多阶段流水线（Planner → Executor → Summarizer）中的错误累积效应：规划器生成的测试计划可能不完整，执行器（UI-TARS-1.5）在操作网页时可能因视觉感知错误而遗漏关键元素，总结器则可能错误综合不完整的执行结果。这一发现挑战了“更复杂的评估流程必然带来更好结果”的直觉。

**可行性验证的精度-召回率权衡。** LLM 评委在可行性验证中呈现高召回、低精度的模式（倾向于过度判定任务可行），而智能体则呈现低召回、高精度的模式（倾向于保守判定不可行）。门控集成策略（$Res_{\mathrm{dynamic}} = Agent \lor LLM$）虽能部分缓解这一问题（Table 7），但本质上是两种缺陷模式的机械组合，未能从根本上解决精度与召回率的联合优化问题。

**深度推理模型的意外不足。** 深度推理模型（如 DeepSeek-R1-0528）在功能等价性识别中表现出犹豫和误判（Figure 10），说明更强的推理能力并不自动转化为更好的评估判断——评估能力可能是一种需要专门训练的内化技能，而非通用推理能力的副产品。这一发现与成对比较中直接判断（无评估标准）与使用量规表现相当的消融结果（Figure 3）形成呼应：相对判断的核心能力已内化于模型，外部指导的边际收益有限。

**开放问题清单：**

1. 如何设计评估机制使 LLM 评委能够准确识别功能等价性，避免因字面差异而误判？
2. 如何提高可行性验证的精度与召回率，尤其是在静态代码分析与交互式测试之间取得平衡？
3. 为什么智能体工作流在交互式任务中未能超越基础模型？如何减少多阶段错误累积？
4. 如何在开放式任务中有效解耦个人偏好与客观质量，以构建更公正的自动评估体系？
5. 如何扩展评估基准以覆盖更多样化的网页开发任务，并支持多轮迭代评估？
6. 能否通过增强模型的代码理解与视觉感知来提升 LLM 评委的综合能力，而不仅仅依赖外部指导？



## 原文 PDF

![[paperPDFs/ICLR_2026/WebDevJudge_Evaluating_MLLMs_as_Critiques_for_Web_Development_Quality.pdf]]
