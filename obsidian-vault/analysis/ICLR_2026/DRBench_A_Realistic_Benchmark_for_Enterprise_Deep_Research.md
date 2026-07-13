---
title: "DRBench: A Realistic Benchmark for Enterprise Deep Research"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DRBench_A_Realistic_Benchmark_for_Enterprise_Deep_Research.pdf
project_link: null
code_link: https://github.com/ServiceNow/drbench
aliases:
- DADDEF
- DRBench
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "自适应行动规划（AAP）允许智能体根据已检索信息动态调整搜索策略，弥补信息鸿沟；这一机制在消融实验中单独最大程度地提高了洞察召回率（+2.79）和报告质量。"
primary_logic: "自适应探索机制是提升关键信息覆盖率的核心驱动力，但会以牺牲部分事实性为代价；轻量级规划则更有利于保持事实基础，说明未来系统需在探索与严谨性之间取得更好的平衡。"
claims:
- "DRBA + AAP achieves highest overall harmonic mean of 39.74 and improves insight recall by 2.79 over base, while SRP reduces factuality."
- "GPT-5 backbone boosts insight recall to 36.52 (23.34 improvement over Llama-3.1-405B), but still misses majority of groundtruth insights."
- "Browser-only agent recall is only 1.11%, illustrating the difficulty of navigating the enterprise environment without API access."
- "Distractor avoidance remains high (>90%) for all configurations, showing agents can avoid irrelevant content but fail to prioritize relevant insights."
---

# DRBench: A Realistic Benchmark for Enterprise Deep Research

> [!tip] 核心洞察
> 自适应探索机制是提升关键信息覆盖率的核心驱动力，但会以牺牲部分事实性为代价；轻量级规划则更有利于保持事实基础，说明未来系统需在探索与严谨性之间取得更好的平衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DRBench：面向企业深度研究的现实基准 |
| 英文题名 | DRBench: A Realistic Benchmark for Enterprise Deep Research |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IGYQ4c92e2) · [GitHub](https://github.com/ServiceNow/drbench) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | DRBench Agent (DRBA) and DRBench evaluation framework |
| Dataset | DRBench FullBenchmark |

> [!tip] 效果简介
> - DRBench FullBenchmark 上，Insight Recall 为 36.52 (GPT-5 no planning)，对比 16.10 (Llama-3.1-405B no planning)，变化 +20.42。
> - DRBench FullBenchmark 上，Harmonic Mean 为 39.74 (DRBA + AAP)，对比 34.82 (Base DRBA)，变化 +4.92。
> - DRBench FullBenchmark 上，Factuality 为 72.11 (GPT-5 no planning)，对比 69.30 (Llama-3.1-405B no planning)，变化 +2.81。

## 概要

企业深度研究要求智能体从混杂的公开网页与内部私有文档中抽取关键洞察，但现有系统在面对复杂、多源的企业信息空间时，普遍难以过滤噪声和区分信息优先级。其结果是，即便最强的前沿模型，其基础事实洞察的召回率也不足 40%（Table 3），而干扰规避却能轻松达到 90% 以上（Table 2, Table 3）。这一鲜明反差表明，当前智能体的主要瓶颈并非被无关内容误导，而是**无法有效发现并优先处理真正重要的洞察**。

为系统诊断这一瓶颈，本文提出了 **DRBench**——首个面向企业深度研究的现实基准。该基准构建了容器化的可复现企业环境（集成 Nextcloud、Mattermost 等多应用），并采用基于 LLM 合成与人工验证的任务生成流水线，保证了高质量的地面事实洞察与可控的干扰项（Section 3.1, Figure 2）。评估体系从原子洞察级别出发，同时覆盖洞察召回、干扰规避、事实性与报告质量四个维度，弥补了以往基准仅关注任务级准确率的不足（Table 1）。

作为配套基线，**DRBench Agent (DRBA)** 围绕规划–检索–报告的生命周期设计，其核心创新在于**自适应行动规划（AAP）**——允许智能体根据已检索到的信息动态调整搜索策略，从而弥补信息缺口。消融实验表明，AAP 单独将洞察召回率提升了 2.79 个百分点，并使 DRBA 在 FullBenchmark 上取得了最高的调和均值 39.74（Table 2）。这正是该基准所揭示的关键关系：自适应探索机制是覆盖关键信息的核心驱动力，但它同时会以牺牲一定事实性为代价；相比之下，轻量级的简单规划则更有利于保持事实基础，揭示了未来系统必须在**探索广度与推理严谨性之间寻求更好的平衡**。

模型规模的提升同样显著：以 GPT-5 为骨干时，无规划的 DRBA 即可达到 36.52 的洞察召回，较 Llama-3.1-405B 提高 20.4 个点（Table 3），但依旧错过大部分基础事实洞察。此外，纯浏览器智能体在不具备 API 级工具访问的情况下，其洞察召回率仅为 1.11%（Section 5.5），凸显了工具接口深度对企业深度研究环境的关键影响。DRBench 及其分析为构建更可靠的企业级深度研究智能体指明了瓶颈所在与优化方向，同时也指出了基准本身在指标覆盖、行业推广性等方面的不足，有待进一步扩展。



现代企业决策越来越依赖对异构信息源的深度综合分析：分析师、管理者或合规人员需要从邮件、聊天记录、云端文件、电子表格、PDF 报告以及公开网络信息中提取关键洞察，并形成可追溯的证据链。这类任务远超出简单的信息检索或单轮问答，它要求智能体在多应用、多格式、多来源的环境中执行多步推理，既要区分有用信息与噪声，又要在事实准确性和报告完整性之间取得平衡。然而，现有的大语言模型智能体——即便是专门为“深度研究”设计的系统——在企业场景下仍普遍面临**洞察召回率低**的核心瓶颈：最佳模型在完整的企业基准中也只能召回不足 40% 的 groundtruth 洞察（Table 3），而仅依赖浏览器操作、无 API 访问权限的通用网页智能体的洞察召回率甚至低至 1.11%（Section 5.5），暴露出导航复杂企业环境的极大困难。

这一性能缺口很大程度上源于当前深度研究基准与真实企业环境之间的距离。过去的工作（如 GAIA、Deep Research Bench 等）主要关注**公共网络检索**，任务通常局限在单一域、单一格式的问答或报告写作，评估也以任务级准确率为主（Table 1）。这类基准不仅没有提供企业应用（如 Nextcloud 云存储、Mattermost 聊天、邮件系统）中常见的多模态、多结构数据源，更缺乏对智能体在**干扰项中识别关键洞察**能力以及**报告事实可靠性**的细粒度诊断。因此，在这些简化场景中表现良好的智能体，一旦被放到同时包含公开网页与私有企业文档、且有大量语义上相关但非关键的干扰信息的环境中，就会暴露出严重的**优先级排序失败**：智能体能够避开绝大部分不相关内容（干扰规避率普遍超过 90%，Table 2 和 Table 3），却无法系统性地捕获 groundtruth 中的核心洞察，导致对关键信息的覆盖率显著偏低。

这一现象揭示了现有方法的一个重要矛盾：系统虽然具备一定的事实基础（尤其在采用轻量级规划时），但当尝试通过更复杂的自适应探索来提高洞察召回率时，往往会牺牲部分事实准确性（Table 2 中 Adaptive Action Planning 与 Simple Research Planning 的组合造成 factuality 下降）。也就是说，**探索性与严谨性之间尚未取得平衡**，而企业深度研究恰恰要求两者兼备。

正是这些缺口直接驱动了 DRBench 的设计。我们首次构建了一个融合公共网络检索与本地企业数据的现实基准，其中 100 个任务均围绕具体的企业角色和行业场景展开，要求智能体在容器化的真实应用环境中搜索、过滤、推理并生成带引用的结构化报告。评估框架跳出了任务级准确率，转而通过原子洞察召回、干扰规避、事实性检验和报告质量四个轴线进行细粒度诊断，从而揭示智能体在**信息检索覆盖面、噪声过滤、事实归因以及最终综合表达**上的具体弱点。这种设计不仅填补了现有基准在企业多源深度研究上的空白，也为后续智能体架构的改进提供了明确的靶点：如何在保障事实基础的同时，通过自适应的行动计划弥补信息鸿沟，从而实质性提升关键洞察的召回率。



## 核心方法与创新机理

DRBench 在任务设置、评估方法与智能体设计三个层面引入了相对于现有基准与基线系统的根本性变化，这些变化直指企业深度研究中“信息过载与关键洞察遗漏”这一核心瓶颈。下文围绕四个关键的 **changed slots** 分析每一项创新如何改变问题的求解空间，并依据消融实验与多环境对比揭示其因果效应与剩余风险。

### 从任务级正确率到原子洞察级多维评估
传统深度研究基准（如 GAIA、DeepResearchBench 等）以任务级二值正确率或单一问答得分为主，无法诊断智能体究竟遗漏了哪些关键信息，亦无法区分其避开了无关内容还是主动忽视了高价值信号。DRBench 将评估粒度提升至**原子洞察（atomic insight）**级别，构建了四项互补指标：*Insight Recall*（注入的真实洞察被报告采纳的比例）、*Distractor Avoidance*（干扰信息未被误用的比例）、*Factuality*（引用准确性）以及 *Report Quality*（报告结构、清晰度等）。这一改变（对应 `evaluation granularity` 槽位）使得基准能够直接暴露系统的真实弱点：实验显示所有配置的 *Distractor Avoidance* 均高于 90%，但 *Insight Recall* 最佳值仍低于 40%（GPT‑5，Table 2 & 3），证明智能体的核心困难并非被误导，而是**无法优先并召回分散在企业多源文件中的关键洞察**。该评估框架的可靠性得到人类研究验证（91.3% 人工评委与 LLM 评委一致率），为后续创新提供了可信的诊断基础。

### 混合数据源与容器化企业环境
过去基准要么仅依赖公开网页（如 Web Research），要么仅传递本地文件（如“flat pass”本地模式），而企业工作流天然需要**同时检索公共信息与内部私密文档（邮件、聊天、云盘、电子表格等）**。DRBench 通过可复现的容器化环境集成了 Nextcloud、Mattermost 等真实企业应用，并构建了 100 个带人格化上下文的研究任务，要求智能体自主在公共 Web 与本地私密应用间交替寻证。这一“data source”与“enterprise environment”双槽位的变化使得基准的难度显著攀升：当同一组文件必须通过企业应用检索而非直接交给智能体时，最强模型 GPT‑5 的 *Insight Recall* 从本地环境的 46.41 骤降至 36.52（Table 5），而纯浏览器智能体（AgentLab）仅获得 1.11% 的召回率（Section 5.5），说明 API 级别的工具访问与环境复杂度是当前研究能力的关键限制。这种混合设置的引入从根源上改变了任务的信息密度与导航复杂度，迫近真实企业决策场景。

### LLM‑人工协作的洞察注入式任务构建
为了得到可量化、可复现的 *Insight Recall* 评估，DRBench 开发了 **LLM 生成与人工验证结合的五阶段任务构造流水线**（Figure 2）。该流水线在生成公司背景、干扰文档与研究问题的同时，向企业文件系统注入预定义的 ground‑truth 洞察（如 PDF 中的合规报告、邮件中的统计数据），再经人工把关选出最终版本。相较于传统基于整体文稿评分的评估，这种“task construction”槽的改进为深度研究提供了**原子级归因能力**：每个被采纳或遗漏的洞察均可追溯，避免了评估中“报告漂亮但缺少关键信息”的盲区。人类评估确认 96% 的研究问题具备真实企业深度研究的合理性，且注入的语义对齐性经 t‑SNE 验证（Figure 4），说明该流水线在保高保真度的同时获得了客观评测的便利。

### 自适应行动规划：动态弥补信息鸿沟的关键模块
在企业混合环境带来的高噪音与高分散场景下，智能体通常难以在检索前就预估所有必要信息来源。DRBA 中提出的 **自适应行动规划（Adaptive Action Planning, AAP）**是相对于基础 DRBA 以及简单/复杂研究规划（SRP/CRP）的核心架构创新。AAP 允许智能体在每一轮研究循环后，依据已检索到的内容**动态评估信息缺口并调整后续搜索策略**，而非执行预先固定的行动列表。消融实验（Table 2）表明：在 Base DRBA 中添加 AAP 使 *Insight Recall* 提高 2.79 点，*Report Quality* 提高 1.85 点，总调和均值达到所有规划配置中最高的 39.74；这一增益远超过 SRP（+0.20）或 CRP 单独带来的提升。这一定量分离证实，**动态适应机制**正是突破企业任务信息覆盖瓶颈的最强单项干预。

然而，因果分析也揭示了 AAP 的单边性：当与复杂规划结合时，*Factuality* 出现下降（Table 2），说明无约束的探索可能牺牲引用可靠性。该发现构成论文的关键张力：自适应探索以部分事实性为代价换来更高的洞察覆盖率，而轻量级规划则更有利于保持证据基础。这一 trade‑off 为下一代企业智能体指明了方向——需要在探索的灵活性与答案的严谨性之间寻求新的平衡机制。目前该结论虽强（Table 2 置信度 0.95），但限于 GPT‑5 单骨干的规划消融，在其他模型上的交互效应仍需扩展验证。



![[assets/figures/papers/iclr26_0014_IGYQ4c92e2_DRBench_A_Realistic_Benchmark_for_Enterprise_Dee/figures/003_Table_1.jpg]]
*Table 1: Comparison of deep research benchmarks (top) and AI agent benchmarks with a computer environment (middle). Columns report dataset size, whether both public and local data are required, the provided environment type, task domains, task description, and evaluation method. Unlike prior work, DRBench combines public web retrieval with local enterprise data in realistic enterprise applications and evaluates both insight recall, distractor avoidance and report quality. Task Description: types of tasks covered by the benchmark: WR for Web Research, DR for Deep Research with both public and local data, CU for Computer Use and/or Mobile Use. DRBench has 1093 total # groundtruth insights that need to...*

![[assets/figures/papers/iclr26_0014_IGYQ4c92e2_DRBench_A_Realistic_Benchmark_for_Enterprise_Dee/figures/005_Figure_3.jpg]]
*Figure 3: DRBench Agent architecture showing the enterprise research workflow from question submission through iterative research cycles to final report generation, using both enterprise and web search capabilities. Reports are generated in two formats: a raw report, consisting of free-form narrative text, and a structured report that lists the main insights with their corresponding citation(s)*

DRBench的整体流程（图1）围绕逼真的企业深度研究场景展开，依次完成五个核心阶段：①任务上下文定义，将研究问题置于具体的公司背景与人物角色中；②任务数据加载，把干扰项与注入的ground‑truth洞察以PDF、DOCX、PPTX、XLSX、聊天记录等格式存入容器化的企业应用环境；③DRBench Agent (DRBA) 同时访问公共网络和本地企业数据，提取相关证据；④生成结构化研究报告；⑤通过多维度自动评估衡量报告质量。这一pipeline将深度研究从单一网页检索提升到融合异构企业信息的综合信息定位与合成任务。

**任务构造与输入流**  
为保障任务的真实性与可复现性，DRBench采用五阶段LLM生成加人工验证流水线（图2），产出100个涵盖零售、医疗、电动汽车三个行业、十个领域的深度研究问题（表1）。每个任务绑定一个公司背景与决策者角色，同时提供多份企业文档与聊天记录——其中既包含回答所需的支持性洞察，也注入大量语义相关但不直接回答问题的干扰项。所有数据被加载到一套可复现的容器化企业环境，该环境集成了Nextcloud云存储、Mattermost企业即时通讯、邮件与用户文件系统等真实应用，要求智能体像人类分析师一样在不同应用间导航、搜索并理解跨格式信息。

**DRBA模块化架构**  
DRBA（图3）是首个专门面向企业深度研究的基线智能体，其架构围绕四个核心模块组织，并辅以向量存储支撑检索。

1. **研究规划（Research Planning）**：将深度研究问题分解为若干可独立探查的领域，为后续检索划定方向。
2. **行动规划（Action Planning）**：根据当前知识状态生成带优先级的工具调用动作（如搜索文件、读取消息、访问网页），决定下一个要执行的操作。
3. **自适应研究循环（Research Loop with AAP）**：迭代执行行动规划产生的动作，每次检索后分析所得信息，识别信息缺口，并动态调整后续搜索策略，这一机制即自适应行动规划（AAP），是提升洞察召回率的核心驱动力（消融实验中AAP单独使召回率提高2.79点）。
4. **报告撰写（Report Writing）**：综合所有收集到的信息，生成两种格式的报告——自由文本叙事版和逐条列出主要洞察及其引文的结构化版。
5. **向量存储（Vector Store）**：维护检索到的文档与片段的嵌入，支持报告生成阶段的语义检索与引用回溯。

各模块通过共享状态协同：研究规划产生的调查领域为行动规划提供目标；自适应研究循环反复调用工具，将检索到的内容追加到上下文，并根据AAP判断继续深入还是切换方向；报告撰写最终从研究循环积累的证据池中提炼见解，并借助向量存储精确定位原文出处。

**输出与评估框架**  
最终报告同时输出原始叙事和结构化洞察列表。评估阶段（图1步骤⑤）采用统一的LLM‑as‑a‑judge方法，在四个维度上分别打分：
- **洞察召回率（Insight Recall）**：衡量报告中是否还原了预注入的ground‑truth洞察，检测系统“找到关键信息”的能力。
- **干扰项回避（Distractor Avoidance）**：衡量是否误将干扰内容当作洞察，防止“编造”或“大面积粘贴”。
- **事实性（Factuality）**：验证每个声明是否被其引用的来源支撑，严格检查归因错误。
- **报告质量（Report Quality）**：评估报告的结构、清晰度、全面性等整体写作水平。

与传统基准以任务级正确与否给分的做法不同，DRBench将评估粒度下沉到原子洞察级别，分别统计每个ground‑truth洞察是否被准确回忆、每个干扰项是否被正确忽略，从而更精细地诊断智能体在复杂信息环境中提取关键信号的真正瓶颈。这种设计使得整体框架不仅能排名模型，还能揭示各模块（尤其是AAP带来的探索与事实性之间的权衡）对系统行为的因果贡献。



### 关键模块

DRBench Agent (DRBA) 是首个面向企业环境深度研究任务构建的基准智能体，其架构围绕四个核心组件展开（Section 4, Figure 3）：

1. **研究规划 (Research Planning)**：将深度研究问题分解为若干可独立探查的子领域，为后续搜索提供高层方向。
2. **行动规划 (Action Planning)**：根据研究规划生成带优先级的工具调用动作，决定“搜索什么”与“何时搜索”。
3. **自适应研究循环 (Adaptive Research Loop with AAP)**：迭代执行检索与信息加工，同时根据已获取的内容动态检测信息缺口，并调整后续搜索策略。**自适应行动规划 (Adaptive Action Planning, AAP)** 是该循环的关键机制——它允许智能体依据当前证据链的薄弱点主动修改行动序列，而非机械遵循初始计划。消融实验表明，在基础 DRBA 上叠加 AAP 可将洞察召回率提高 **+2.79**，谐波均值达到最高 **39.74**（Table 2），是单一模块中对关键信息覆盖率提升贡献最大的设计。
4. **报告生成 (Report Writing)**：汇总研究循环收集的证据，生成包含引用的结构化报告，支持原始报告与要点列表两种输出形式。

此外，**向量存储 (Vector Store)** 在后台持续维护语义嵌入，用于在报告生成阶段进行高效的相关片段检索。

DRBA 的规划策略还包含两个变体：**简单研究规划 (SRP)** 与 **复杂研究规划 (CRP)**。SRP 提供轻量级任务分解，有助于保持事实性；CRP 则进行更精细的多层次规划，能进一步提升干扰项规避能力（Distractor Avoidance 可达 97.14），但可能损失部分洞察召回（Table 2, Table 3）。这些模块共同构成了 DRBA 的主干，并使研究者能够系统地调控“探索深度”与“报告忠实度”之间的权衡。

### 关键公式及变量含义

在人工评估中，每个任务上的智能体得分由 groundtruth 洞察级别的打分平均得到，其公式定义为（Appendix R）：

$$S_{a,t} = \frac{1}{n} \sum_{i=1}^{n} s_{a,i}$$

- $S_{a,t}$：智能体 $a$ 在任务 $t$ 上的人类得分；
- $n$：该任务中预设的 groundtruth 洞察总数；
- $s_{a,i}$：第 $i$ 个 groundtruth 洞察的个体得分，取值 $\{-1, 0, 1\}$，依次代表错误识别、未识别、正确识别。

该分数用于校准自动化洞察召回指标，人工评估结果显示两者高度一致（Figure 8），验证了自动化指标的可靠性。注：其他核心评价指标（如 Insight Recall、Distractor Avoidance、Factuality）采用 LLM-as-a-judge 流程进行判定，原文未提供封闭形式的数学表达式，此处不再推导。



## 实验与关键发现

### 总体表现：核心瓶颈在洞察召回率

DRBench 从原子洞察级别评估智能体，核心指标包括洞察召回率（Insight Recall）、事实性（Factuality）、干扰项回避（Distractor Avoidance）、报告质量（Report Quality）以及调和均值（Harmonic Mean）。所有配置下干扰项回避均超过 90%，表明智能体能有效避开无关内容，但洞察召回率普遍低下——即使最强的 GPT‑5（无额外规划）也仅达 36.52%，意味着绝大多数 groundtruth 洞察被漏检（Table 2, Table 3）。这一对比揭示了当前系统的真实瓶颈：在多源、高噪声的企业环境中，智能体缺乏有效的筛选与优先级排序能力，难以从大量数据中锁定关键信息。


![[assets/figures/papers/iclr26_0014_IGYQ4c92e2_DRBench_A_Realistic_Benchmark_for_Enterprise_Dee/figures/006_Table_2.jpg]]
*Table 2: DRBA performance with different planning configurations on DRBench(FullBenchmark). We compare the base agent with variants using Simple Research Planning (SRP), Complex Research Planning (CRP), Adaptive Action Planning (AAP), and their combinations. See Appendix K for the standard error across 3 runs on MinEval. Note that higher numbers correspond to better scores, and the best result on each metric is bolded*

![[assets/figures/papers/iclr26_0014_IGYQ4c92e2_DRBench_A_Realistic_Benchmark_for_Enterprise_Dee/figures/007_Table_3.jpg]]
*Table 3: Performance of DRBA on the FullBenchmark subset using different backbone language models and planning strategies. Note that higher numbers correspond to better scores, and the best result on each metric is bolded. The full table with more models is given in Appendix M*

### 规划策略消融：自适应行动规划推动召回提升但牺牲事实性

Table 2 展示了 DRBA 在不同规划配置下的全量基准结果。基础 DRBA 的洞察召回率仅为 13.18，调和均值 34.82。单独加入自适应行动规划（Adaptive Action Planning, AAP）将洞察召回提升至 16.97（+2.79），调和均值达到 39.74，是所有 DRBA 变体中的最高值。然而，AAP 也导致事实性从 58.04 降至 54.13，而在与简单研究规划（SRP）或复杂研究规划（CRP）组合时，事实性进一步下滑（例如 AAP+SRP 的事实性仅 51.57）。这说明自适应搜索通过动态补全信息缺口提高了覆盖度，但倾向于生成更多细节，增加了事实错误的概率。与之相对，SRP 与 CRP 单独使用时对召回无明显增益，甚至略微降低，但 CRP 能小幅改善干扰项回避。该消融结果直接支撑核心因果机制：自适应探索是提升关键信息覆盖率的主驱动力，但其代价是事实严谨性下降；轻量规划相对更有利于维持事实基础。

### 骨干模型扩展：规模红利显著，但远未触及召回上限

Table 3 对比了不同骨干模型在无规划、SRP、CRP 下的性能。GPT‑5 基础配置的洞察召回率高达 36.52，较 Llama‑3.1‑405B 的 16.10 提升 +20.42；调和均值从 34.62 跃升至 63.81。DeepSeek‑V3.1 与 Qwen‑2.5‑72B 的召回仅约 13–14，事实性与报告质量亦明显落后，证实更强的基座模型是企业深度研究的必要前提。但即使 GPT‑5 的召回依然低于 40%，表明单纯扩展模型规模并不能突破搜索、推理与信息综合的上限。此外，CRP 对 GPT‑5 仅微小提升干扰项回避（93.23→94.26）而略微损失召回（36.52→35.36），对其他小模型则普遍改善回避但降低召回，再次说明过度结构化规划可能压制探索，对弱模型尤其不利。

### 环境交互与浏览器代理的失败

Table 5 的对比显示，当所有文件直接作为本地输入（local）提供时，GPT‑5 的洞察召回可升至 50.38，较真实应用环境（app‑based）中的 36.52 高出 13.86，这一定量差距揭示了企业环境的检索与交互负载对智能体的严重削弱。进一步的极限测试（Section 5.5）中，纯浏览器代理（AgentLab）仅取得 1.11% 的洞察召回率，几乎完全失败。根本原因在于没有 API 级工具访问时，智能体无法进行定向搜索与结构化数据提取，只能依赖脆弱的页面导航与视觉解析，从而在复杂的企业文件系统、聊天与邮件中彻底迷失。


![[assets/figures/papers/iclr26_0014_IGYQ4c92e2_DRBench_A_Realistic_Benchmark_for_Enterprise_Dee/figures/009_Table_5.jpg]]
*Table 5: Model Performance Comparison Across Local or App-based Environments on the FullBenchmark. Note that higher numbers correspond to better scores, and the best result on each metric is bolded*

### 超参数与评估可靠性

循环迭代次数的消融实验（Table 27）表明，从 5 次提升到 50 次并未持续改善性能，最佳权衡出现在中等次数，过多的迭代反而引入冗余探索或噪声积累。评估方面，LLM 评判（GPT‑4o）对事实性和干扰项回避的多次运行方差很小；人类评估对深度研究问题的质量认可度达 96%，且自动洞察召回分数与人类评分高度一致（Figure 8），为评估指标提供了校准信度。需要指出的是，Insight Recall 的截断方式（k = groundtruth 数量 +5）虽防止了系统“刷分”，但也限制了其奖励真正新颖发现的能力，这是当前度量设计的已知局限。


![[assets/figures/papers/iclr26_0014_IGYQ4c92e2_DRBench_A_Realistic_Benchmark_for_Enterprise_Dee/figures/048_Figure_8.jpg]]
*Figure 8: Comparison of Human Scores and Insight Recall Scores. As can be seen the human evaluation results are aligned with our automated evaluation*

### 重要图表结论

- **Table 2**：AAP 是当前最具效力的规划模块，但与其他规划叠加时收益递减，并会降低事实性，表明探索与严谨性之间存在明确的权衡取舍。
- **Table 3**：GPT‑5 带来代际跳跃，但召回仍远未饱和；CRP 对强模型影响微弱，对弱模型则可能抑制发现。
- **Table 5 & Section 5.5**：真实企业环境与缺乏 API 工具的代价被量化——环境自身降低超过 13 个百分点的召回，而纯浏览器方案近乎零覆盖。
- **Figure 8**：人类与自动评估的对齐为洞察级别的衡量提供了可信度，支撑基准的整体有效性。
- **Table 27**：循环次数需控制在合理区间（中等即可），过度迭代不会带来显著增益，可为系统设计提供超参数选取指引。



## 定位与知识库关联

### 与现有基准及系统的谱系关系

DRBench 建立在一系列面向研究型智能体与通用人工智能助手的基准之上，但其设计空间存在多处关键位移。从基准维度看，早期工作如 Deep Research Bench（Bosse et al., 2025; Du et al., 2025）仅依赖公开网络数据并以任务级准确性作为评估终点，而 GAIA（Mialon et al., 2024）面向的是无需深度研究的助手问答。DRBench 通过三个核心维度实现突破：**评估粒度**从任务级转为原子洞察级，同时引入干扰项回避、事实性和报告质量等多轴评分（Section 5.1）；**数据源**同时覆盖公共网络与私有企业文档（Table 1）；**企业环境**由真实的容器化多应用场景（Nextcloud、Mattermost 等）构成，而非单纯的模拟桌面。在智能体侧，作为基线系统的 DRBench Agent（DRBA）是首个专为企业深度研究设计的智能体，其架构包含研究规划、动作规划、自适应研究循环与报告生成（Figure 3），并可搭配自适应行动规划（AAP）等策略动态调整检索方向。与之形成对照的是，OpenAI Deep Research（GPT-5 骨干）与 AgentLab 的纯浏览器智能体均被纳入比较，前者的强骨干带来最高综合得分（Table 3），后者则在无 API 访问时几乎完全失效（洞察召回率仅 1.11%，Section 5.5），突显了本研究在工具可编程性假设上的特殊性。

### 适用边界与条件

实验证据清晰地标定了 DRBench 及其智能体的适用边界：

1. **API 依赖与浏览器受限**：AgentLab 的通用浏览器智能体应用 GPT‑4.1 骨干，在完全企业环境中无法突破 2% 的洞察召回率（Section 5.5）。这意味着当前基准的有效性高度依赖于面向应用的 API 访问（如文件系统、聊天工具等编程接口），而基于视觉的纯 Web 智能体在此类复杂、多源的企业信息检索中几乎无任何实用能力。
2. **企业环境交互成本**：Table 5 直接对比了“本地文件直接传递”与“应用环境检索”两种设定下的模型表现。以 DRBA（GPT‑5）为例，其洞察召回率在该环境下为 36.52，而在本地环境下明显更高；事实性和报告质量同样呈现类似的差距。这说明真实的企业导航与搜索开销是当前模型的主要阻碍之一。
3. **规划策略的权衡空间**：消融实验（Table 2）表明，自适应行动规划（AAP）以牺牲部分事实性为代价，单独最大程度地提高了洞察召回率（+2.79），最终取得最优综合谐波均值（39.74）；而结构化研究规划（SRP/CRP）在提升干扰项回避的同时，倾向降低洞察召回率或事实性。因此，面对不同精度—覆盖率需求时，需在“探索激进性”与“事实严谨性”之间作出选择，且单纯增加研究循环迭代次数（5→50）并不能持续带来性能增益（Appendix O, Table 27），进一步证实了缺乏规划自适应的盲搜索效用有限。

### 局限与失败模式

尽管 DRBench 提供了迄今为止最为全面的企业深度研究评估，其设计中的若干内在限制也会约束结论的外推：

- **评估粒度与奖励上限**：洞察召回率采用截止数 $k = \text{groundtruth} + 5$ 的设定（Sections 5.1, Appendix T），该设计成功防止了系统通过大量输出“刷分”，但同时也截断了真正新颖且有效发现的奖励空间，使指标无法完全反映智能体的发现能力上限。
- **归因粒度不足**：事实性评估并未深入到片段或令牌级的归因，原子洞察级别的判断可能遗漏细粒度的引用错误或局部杜撰。
- **任务合成的人工残留**：尽管采用了 LLM 生成+人工参与的高质控流水线（Figure 2），且人类评估确认问题质量通过率达 96%（Section 6），合成文档与洞察仍可能携带分布特征上的偏倚，基准的生态效度有待持续扩展验证。
- **领域与行业的覆盖度**：当前 100 个任务仅涵盖零售、医疗和电动汽车三个行业、十个领域（Appendix B），其在金融、法律、制造等其他企业工作流中的推广性尚未得到验证。
- **精英模型仍大量遗漏核心洞察**：即便在最优配置下（GPT‑5 骨干 + AAP），最佳模型的洞察召回率亦未突破 40%（Table 2, Table 3），表明现有智能体在嘈杂多源环境中识别高价值信息的核心瓶颈远未解除。干扰项回避虽持续高于 90%，但智能体在面对真实信息时无法有效将其优先级提高，呈现出“回避有余、提取不足”的系统性失败模式。
- **环境可移植性挑战**：当前所有主要实验均依赖容器化应用 API；将 DRBench 的方法论直接迁移至完全基于浏览器操作或更受限的企业环境中，可能面临工具生态不兼容的风险，浏览器智能体实验已初步印证此点。

### 开放问题

基于上述边界与局限，DRBench 揭示出一系列亟待解决的研究问题：

1. **规划中的探索‑严谨平衡机制**：如何在智能体规划中兼顾自适应探索带来的覆盖率增益与事实可靠性？目前 AAP 与 SRP/CRP 的简单组合反而削弱了事实性（Table 2），表明不存在简单的叠加方案，亟需设计内在耦合的规划—校验结构。
2. **纯浏览器深度研究能力的构建**：如何赋予浏览器智能体结构化检索与跨应用推理能力，使其在无法直接调用 API 的企业场景下也能执行深度研究？这可能需要视觉解析、应用状态建模和长期行动记忆等技术的协同突破。
3. **基准的维度扩展**：如何将 DRBench 延伸至跨团队决策、纵向审计、事件响应等更多企业任务原型？如何引入覆盖度与新颖性等新评估指标，以弥补当前 Insight Recall 指标的局限性？
4. **评估信号的精细化**：能否引入更细粒度的归因信号（如引用对齐、事实链追踪），使事实性评估从原子洞察级提升至证据片段级，从而实现更可靠的自动诊断？
5. **领域适应性的系统性研究**：当智能体被部署到迥异的企业领域时，其搜索策略和规划偏好应如何自适应调整？开放基准的行业与领域扩展将是推动此类研究的基础设施条件。



## 原文 PDF

![[paperPDFs/ICLR_2026/DRBench_A_Realistic_Benchmark_for_Enterprise_Deep_Research.pdf]]
