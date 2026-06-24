---
title: "Breaking Agent Backbones: Evaluating the Security of Backbone LLMs in AI Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Breaking_Agent_Backbones_Evaluating_the_Security_of_Backbone_LLMs_in_AI_Agents.pdf
openreview_forum_id: kga18ld70t
aliases:
- TSF
- BABESBLAA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "威胁快照（Threat Snapshots）框架：将安全评估聚焦于LLM调用的孤立状态，通过系统化攻击分类和攻击收集，建立直接度量LLM漏洞的基准。"
primary_logic: "（1）增强推理能力普遍提升LLM安全性，但模型大小与安全性无显著相关；（2）闭源模型系统级安全性优于开源模型；（3）安全性与效用总体正相关但存在显著离群值；（4）基准排名对攻击选择、聚合方式具有鲁棒性。"
claims:
- "威胁快照框架通过重构单次LLM调用上下文、攻击注入和评分函数，完整描述LLM漏洞实例。"
- "推理能力启用时，模型漏洞评分显著降低，安全性提升。"
- "b^3基准排名对攻击选择、聚合方式等设计因素具有强鲁棒性（Spearman相关系数≥0.75）。"
- "模型大小与安全性之间缺乏有意义的正相关。"
---

# Breaking Agent Backbones: Evaluating the Security of Backbone LLMs in AI Agents

> [!tip] 核心洞察
> （1）增强推理能力普遍提升LLM安全性，但模型大小与安全性无显著相关；（2）闭源模型系统级安全性优于开源模型；（3）安全性与效用总体正相关但存在显著离群值；（4）基准排名对攻击选择、聚合方式具有鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 突破Agent骨干：评估AI代理中骨干LLM的安全性 |
| 英文题名 | Breaking Agent Backbones: Evaluating the Security of Backbone LLMs in AI Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=kga18ld70t) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | 威胁快照框架（Threat Snapshots Framework） |
| Dataset |  |

## 概述

### 问题背景

大型语言模型（LLM）正日益成为AI代理系统的核心“骨干”，负责理解上下文、规划步骤与调用工具。然而，骨干LLM本身的安全漏洞可直接导致代理执行恶意指令、泄露敏感信息或产生有害输出。现有代理安全评测基准——如**Agent Security Bench (ASB)**（Zhang et al., 2025）、**AgentDojo**（Debenedetti et al., 2024）、**InjecAgent**（Zhan et al., 2024）和**AgentHarm**（Andriushchenko et al., 2025）——普遍采用模拟完整代理执行流的方式进行评估。这种范式存在两个根本性瓶颈：一是攻击覆盖依赖于特定代理架构，难以系统化地穷举攻击面；二是评测结果混合了LLM漏洞与代理框架的防御机制，无法**隔离**出骨干LLM本身的安全特性。因此，领域内缺乏一个能直接度量LLM安全漏洞、支持细粒度对比的框架，使得“选择哪个LLM作为代理骨干更安全”这一问题长期缺乏可靠的实证依据。

### 核心方法与贡献

本文提出**威胁快照框架（Threat Snapshots Framework）**，并基于此构建了**b³基准**。该方法的核心创新在于将安全评估从完整的代理执行流中抽离，聚焦于LLM被调用的**孤立时刻**——即威胁快照。每个威胁快照完整刻画了该时刻的代理状态（系统提示、上下文历史）和威胁描述（攻击分类、注入方式、评分函数），从而将LLM漏洞评估转化为一个可控、可复现的标准化测试。

在此基础上，作者构建了覆盖10种代理场景的30个威胁快照（每个场景含三个防御等级L1/L2/L3），并通过游戏化红队众包收集了194,331个针对性对抗攻击，系统性覆盖了6种攻击类型（按注入方式分为直接/间接，按目标能力分为消息/工具/两者兼有）。最终，对34个主流LLM进行评测，得出漏洞评分及基于Bootstrap的置信区间。

### 关键发现

1. **推理能力是安全性的关键杠杆**：启用推理能力（reasoning）的LLM漏洞评分显著更低（Figure 2），表明增强推理普遍提升安全性；但模型参数规模与安全性之间**无显著正相关**（Figure 9），更大模型未必更安全。

2. **闭源模型的系统级安全性优于开源模型**：Claude、GPT等闭源模型在b³基准上表现更优，但需注意闭源模型评估的是包含额外安全防护层的系统级安全性，而开源模型评估的是裸模型级安全性，直接对比存在公平性考量。

3. **安全性与效用总体正相关，但存在显著离群值**：在安全-效用权衡分析（Figure 16）中，多数模型呈现安全性与代理智能指数正相关的趋势，但claude-haiku-4.5、gpt-5.1、kimi-k2-thinking等模型表现出明显的偏离，提示安全与效用并非简单的线性权衡。

4. **基准排名具有强鲁棒性**：b³基准的模型排名对攻击选择方式（Spearman相关系数≥0.75）、聚合方法（mean vs max）等设计因素不敏感（Figure 8），表明基准结论可靠。

### 方法定位

与现有基于完整代理模拟的评测范式相比，b³基准在三个维度上实现了差异化定位：**评估方法论**上，从模拟完整代理执行流转为威胁快照的单步隔离评估；**攻击生成方式**上，从固定模板攻击升级为基于众包的、针对上下文的对抗性攻击；**分析粒度**上，支持按攻击类型、防御等级、任务类型等维度进行细粒度排名。这一设计使b³成为首个系统化度量骨干LLM安全漏洞的基准，其威胁快照框架也可作为未来代理安全研究的基础抽象。

## 背景与动机

AI代理（AI Agent）正迅速成为大语言模型（LLM）的核心应用范式。在这些系统中，LLM作为“骨干”负责理解环境、规划行动并生成响应，其安全性直接决定了整个代理系统的可信程度。然而，当前社区对骨干LLM选择如何影响AI代理安全性仍缺乏系统性理解：现有安全评测基准要么覆盖的漏洞类型不全，要么需要模拟完整的代理执行流程，导致无法将LLM自身的安全缺陷与代理框架的其他组件解耦，难以形成可比较、可复现的LLM级安全度量。

这一瓶颈的根源在于两个层面。在概念层面，代理系统的安全风险分布在LLM调用、工具交互、多步推理等多个环节，缺乏一个统一的抽象来精确定义“LLM在代理中的脆弱性实例”。在工程层面，基于完整代理模拟的评测方案——如**Agent Security Bench (ASB)**（Zhang et al., 2025）、**AgentDojo**（Debenedetti et al., 2024）、**InjecAgent**（Zhan et al., 2024）和**AgentHarm**（Andriushchenko et al., 2025）——虽然能反映端到端的安全表现，但其结果混杂了代理框架的防御机制与任务设计的影响，难以直接归因于骨干LLM的安全属性。此外，这些基准多依赖固定模板的攻击，缺乏针对具体代理上下文的对抗性攻击，削弱了评估的真实性和区分度。

本文的核心动机正是填补这一空白：构建一个聚焦于LLM调用时刻的、可系统化评测骨干LLM安全性的框架。为此，作者提出**威胁快照（Threat Snapshots）**框架，将安全评估从完整的代理执行流中抽离出来，仅关注LLM被调用时的孤立状态——包括其上下文、注入的攻击以及评分标准。这一设计使得每个威胁快照完整描述了一个LLM脆弱性实例，从而建立起直接度量LLM漏洞的基准，而无需模拟整个代理。在此基础上，通过系统化的攻击分类和基于众包的对抗性攻击收集，b³基准实现了对34个主流LLM的细粒度安全排名，并揭示了推理能力、模型规模、闭源与开源等因素对安全性的因果影响。

## 核心创新

### 问题瓶颈：从“代理整体模拟”到“骨干LLM隔离”

现有AI代理安全基准——如**Agent Security Bench (ASB)**（Zhang et al., 2025）、**AgentDojo**（Debenedetti et al., 2024）、**InjecAgent**（Zhan et al., 2024）和**AgentHarm**（Andriushchenko et al., 2025）——均采用**模拟完整AI代理执行流**的评估范式。这类方法存在两个根本性局限：（1）评测结果混杂了代理架构、工具链、环境交互等非LLM因素的噪声，无法将漏洞归因于骨干LLM本身；（2）完整模拟的复杂性限制了攻击覆盖面的系统性扩展。这导致领域内**缺乏一个能隔离、度量并比较不同骨干LLM安全性的统一框架**。

### 核心创新：威胁快照框架

本工作的核心创新是提出**威胁快照框架（Threat Snapshots Framework）**，将安全评估从“模拟整个代理”转向“聚焦LLM调用时刻的孤立状态”。该框架包含三个关键设计：

**（1）评估范式的根本转变。** 威胁快照捕获代理执行流中LLM被调用的精确时刻，重构该时刻的模型上下文$C_t$（包含系统提示和历史），定义攻击者的注入方式、攻击目标以及评分函数，从而**完整描述一个LLM漏洞实例**（Figure 3, Appendix B.1）。这一设计将评估对象从“代理系统”缩小为“骨干LLM在特定上下文下的单次调用”，消除了代理架构差异带来的混淆。

**（2）系统化的攻击分类与收集。** 不同于现有基准普遍采用的**固定模板攻击**，本工作构建了向量-目标分离的攻击分类体系（Table 1），并通过**游戏化众包红队挑战**收集了194,331个针对上下文的对抗性攻击（Section 3.2）。从成功攻击中筛选出高质量子集（平均攻击得分0.56，远高于公开数据的0.18），确保攻击的针对性和有效性。

**（3）细粒度、可切片的排名体系。** 框架天然支持基于攻击类型、防御等级、任务类型等维度的**子排名（Sub-ranking）**（Table 6），使安全分析从单一总分拓展为多维度的漏洞画像。例如，可按工具使用、内容安全、间接注入等切片分别排名（Figure 15），揭示模型在不同攻击面上的差异化表现。

### 方法定位：填补基准谱系的空白

在AI代理安全评估的方法谱系中，现有基准要么覆盖漏洞不全（受限于固定模板），要么需模拟完整代理而无法隔离LLM特有问题。威胁快照框架通过以下机制填补了这一空白：

- **隔离性**：将LLM安全性与代理架构解耦，提供骨干模型安全性的“下界估计”。
- **系统性**：攻击分类覆盖直接/间接注入、消息/工具/综合目标等6种攻击类型，10个威胁快照覆盖编码助手、RAG代理、多代理交易系统等典型场景。
- **鲁棒性**：基准排名对攻击选择方法、聚合方式（mean vs max）高度鲁棒，Spearman相关系数≥0.75（Figure 8），表明框架输出的排名信号稳定可靠。

## 整体框架

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/001_Figure_1.jpg]]
*Figure 1: (left) Illustration of how inputs flow within an AI agent, alternating between an LLM step that calls the backend LLM m with the current model context and a processing step that calls the processing function $f _ { \mathrm { p r o c } }$ until the final response is produced. (right) The $\mathrm { b ^ { 3 } }$ benchmark, which uses threat snapshots to isolate an LLM step from the context-output flow on the left. (right top) There are 30 threat snapshots in total based on 10 application with three levels L1, L2 and L3. (right bottom) Each threat snapshot is evaluated against the set of attacks where we evaluate each attack N times which is used to account for the variance in responses

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/004_Table_1.jpg]]
*Table 1: Separation of attack types by delivery method (either direct or indirect) and by which LLM capability they target*

### 代理安全评估的瓶颈与动机

现有AI代理安全基准——如**Agent Security Bench (ASB)**（Zhang et al., 2025）、**AgentDojo**（Debenedetti et al., 2024）、**InjecAgent**（Zhan et al., 2024）和**AgentHarm**（Andriushchenko et al., 2025）——均采用模拟完整代理执行流的方法论。这种设计存在两个结构性局限：其一，完整模拟将LLM漏洞与代理框架的其他组件（如工具调用、记忆管理）耦合在一起，难以隔离骨干LLM自身的安全特性；其二，基于固定模板的攻击生成方式限制了对抗性攻击的多样性和上下文针对性。

本文的核心瓶颈洞察是：**缺乏一个系统性理解骨干LLM选择如何影响AI代理安全性的框架**。现有评测要么覆盖漏洞不全，要么因模拟完整代理而无法分离LLM特有问题。由此驱动的方法论转向是：将安全评估聚焦于LLM调用的孤立状态，而非整个代理的执行轨迹。

### 威胁快照框架的核心设计

为解决上述瓶颈，论文提出**威胁快照框架（Threat Snapshots Framework）**，其因果调节变量是：**将安全评估从完整代理模拟中解耦，聚焦于单次LLM调用时刻的上下文与攻击注入**。该框架由五个顺序模块构成，形成一条从形式化定义到量化评估的完整pipeline：

1. **AI代理形式化（AI Agent Formalization）**：将AI代理定义为交替调用骨干LLM $m$ 和处理函数 $f_{\mathrm{proc}}$ 的序列，LLM被视为无状态函数 $m: \mathcal{C} \to \mathcal{O}$，仅依赖于当前模型上下文 $C_t$。这为后续威胁建模提供了精确的数学基础（见Algorithm 1）。

2. **威胁快照定义（Threat Snapshot Definition）**：一个威胁快照完整描述了LLM漏洞实例，包含两部分——**代理状态**（系统提示、上下文历史等模型上下文 $C_t$）和**威胁描述**（攻击者目标、攻击注入函数、评分函数）。该抽象将“攻击者如何通过部分上下文控制来操纵模型输出”这一核心安全场景形式化（见图3）。

3. **攻击分类体系（Attack Categorization）**：构建二维攻击分类——按**投递方式**（直接/间接）和**目标LLM能力**（消息/工具/两者兼具）交叉产生六种攻击类型（见表1）：直接注入输出（DIO）、直接工具注入（DTI）、直接上下文提取（DCE）、间接注入输出（IIO）、间接工具注入（ITI）、动态代理间安全（DAIS）。该分类为系统化覆盖攻击面提供了结构保证。

4. **众包攻击收集（Crowdsourcing Attack Collection）**：通过游戏化红队挑战收集高质量、针对特定上下文的对抗性攻击，从194,331个攻击中筛选出top-210个高质量攻击（平均得分0.56，而公开攻击数据仅0.18）。这与基线方法使用的固定模板攻击形成方法论差异。

5. **漏洞评分计算（Vulnerability Score Computation）**：模型 $m$ 在威胁快照集合 $\mathcal{T}$ 上的漏洞评分定义为所有攻击在所有快照上的平均得分：

$$V(m, T) := \frac{1}{|\mathcal{T}|} \sum_{(i,\ell) \in \mathcal{T}} \frac{1}{|\mathcal{A}_i|} \sum_{a \in \mathcal{A}_i} \frac{1}{N} \sum_{k=1}^{N} s_k(a, \mathrm{TS}_i^\ell)$$

并通过非参数Bootstrap估计95%置信区间 $[V^{\mathrm{lower}}(m, T), V^{\mathrm{upper}}(m, T)]$。

### 输入-输出流与基准结构

图1展示了框架的完整数据流。左侧为AI代理的通用执行流：用户输入 $I$ 进入后，代理在LLM调用（以当前上下文 $C_t$ 调用模型 $m$）和处理步骤（调用 $f_{\mathrm{proc}}$ 更新上下文）之间交替，直至满足停止条件 $f_{\mathrm{stop}}$ 产生最终响应 $R$。右侧为 $\mathrm{b}^3$ 基准的结构：从该执行流中提取30个威胁快照（基于10种代理应用 × 3个防御等级L1/L2/L3），每个快照对应一个孤立的LLM调用状态；对每个快照，使用筛选后的攻击集进行 $N=5$ 次重复评估以控制响应方差。

### 与基线方法的差异槽位

相较于现有基准，威胁快照框架在三个关键槽位上实现了方法论转变：

| 差异维度 | 基线方法 | 威胁快照框架 |
|---------|---------|------------|
| **评估方法论** | 模拟完整AI代理执行流 | 仅聚焦LLM调用时刻的上下文和攻击，无需模拟完整代理 |
| **攻击生成方式** | 基于固定模板的攻击 | 基于众包的、针对上下文的对抗性攻击（194k+攻击池） |
| **细粒度排名** | 不支持基于攻击类型/防御等级的分片排名 | 支持按威胁快照子集、防御等级、攻击类型等维度的细粒度漏洞得分排名 |

其中，评估方法论的转变是核心创新——通过将安全评估压缩到单步LLM调用的“快照”上，框架实现了对骨干LLM漏洞的直接度量，同时避免了完整代理模拟中非LLM组件的干扰。攻击生成方式的转变（从模板化到众包对抗性攻击）则提升了攻击的多样性和强度，使得基准更难被“过拟合”。细粒度排名能力（见表6的Sub-ranking列）允许研究者按任务类型、防御等级等维度切片分析模型的安全特性，这是现有基准不具备的分析深度。

### 框架的覆盖范围与局限

威胁快照框架目前聚焦于单步威胁快照，以在覆盖多样性和评估可行性之间取得平衡。对于多步攻击（如渐进式越狱），框架支持将其分解为威胁快照链进行建模（见图5的Crescendo攻击示例），但本文的基准评测仅使用单步快照。这一设计选择意味着：**基准得分应被解释为LLM安全性的下界估计**，因为多步攻击可能揭示额外的漏洞。此外，基准数据集基于当前代理架构构建的10种威胁快照，可能无法覆盖未来新型攻击面和代理架构。

## 核心模块与公式推导

### 威胁快照框架的五个核心模块

**模块一：AI代理形式化（AI Agent Formalization）**

论文首先将AI代理严格定义为交替调用骨干LLM $m$ 与处理函数 $f_{\mathrm{proc}}$ 的序列算法。LLM被建模为从模型上下文空间 $\mathcal{C}$ 到输出空间 $\mathcal{O}$ 的映射 $m: \mathcal{C} \to \mathcal{O}$，且被视为无状态——其行为仅取决于当前上下文 $C_t$，而不依赖历史内部状态。处理函数 $f_{\mathrm{proc}}: \mathcal{O} \times \mathcal{C} \times \bar{\mathbb{N}} \to \mathcal{C}$ 接收模型输出、当前上下文和步数计数器，生成下一时刻的模型上下文。这一形式化将复杂的代理行为压缩为LLM调用与上下文更新的交替循环，为后续的威胁建模提供了精确的数学基础（Section 2.1, Algorithm 1）。

**模块二：威胁快照定义（Threat Snapshot Definition）**

威胁快照是框架的核心抽象，用于完整描述一个LLM漏洞实例。每个威胁快照包含两部分：（1）**代理状态**，通过重构当前模型上下文 $C_t$（含系统提示和交互历史）来刻画LLM被调用时的精确状态；（2）**威胁描述**，包括攻击分类、攻击注入函数（定义攻击如何嵌入上下文）和评分函数（定义攻击成功的判断标准）。这一设计将安全评估聚焦于LLM调用的孤立时刻，无需模拟完整的代理执行流，从而实现了对LLM层面漏洞的直接度量（Section 2.2.1, Figure 3）。

**模块三：攻击分类体系（Attack Categorization）**

论文构建了专为本工作设计的二维攻击分类体系，而非沿用现有分类法。第一维按**攻击向量**（delivery method）分为直接攻击与间接攻击；第二维按**攻击目标**（targeted LLM capability）分为消息能力、工具能力或两者兼有。这一交叉分类产生了六种攻击类型（Table 1）：DIO（直接消息）、DTI（直接工具）、DCE（直接复合）、IIO（间接消息）、ITI（间接工具）、DAIS（间接复合）。该体系旨在系统化覆盖AI代理的攻击面，为后续攻击收集和细粒度排名提供结构化框架（Section 2.2.2, Appendix A）。

**模块四：众包攻击收集（Crowdsourcing Attack Collection）**

攻击收集通过游戏化红队挑战进行。参与者被随机分配至7种骨干LLM之一，针对特定威胁快照生成对抗性攻击。从约194k条攻击中，筛选出攻击强度最高的210条（每快照每防御等级7条）用于最终基准评估。值得注意的是，公开数据集的平均攻击得分仅为0.18，而保留的top-210攻击平均得分达0.56，意味着公开版本的攻击强度被显著削弱，以降低基准过拟合风险（Section 3.2, Appendix G）。

**模块五：漏洞评分计算（Vulnerability Score Computation）**

漏洞评分是整个框架的量化输出，其计算过程由公式(1)定义，并通过公式(2)的非参数Bootstrap估计置信区间。

### 关键公式

**漏洞评分公式**

$$V(m, T) := \frac{1}{|\mathcal{T}|} \sum_{(i,\ell) \in \mathcal{T}} \frac{1}{|\mathcal{A}_i|} \sum_{a \in \mathcal{A}_i} \frac{1}{N} \sum_{k=1}^{N} s_k(a, \mathrm{TS}_i^\ell)$$

**变量含义**：
- $m$：被评估的骨干LLM
- $T$：威胁快照集合 $\mathcal{T} = \{(i, \ell)\}$，其中 $i$ 标识具体快照，$\ell$ 标识防御等级（L1/L2/L3）
- $\mathcal{A}_i$：针对威胁快照 $i$ 的攻击集合
- $N$：每条攻击的重复评估次数（论文中设为 $N=5$）
- $s_k(a, \mathrm{TS}_i^\ell)$：攻击 $a$ 在第 $k$ 次重复中对威胁快照 $\mathrm{TS}_i^\ell$ 的评分
- $V(m, T)$：模型 $m$ 在威胁快照集 $T$ 上的总漏洞评分，为所有攻击在所有快照上的三重平均

该公式的本质是将安全评估量化为攻击成功率的三层聚合：先在重复试验上平均以控制LLM输出的随机性，再在攻击上平均以覆盖攻击多样性，最后在威胁快照上平均以反映整体安全性。得分越低表示模型越安全。

**Bootstrap置信区间**

$$[V^{\mathrm{lower}}(m, T), V^{\mathrm{upper}}(m, T)]$$

通过非参数Bootstrap方法计算漏洞评分的95%置信区间，用于量化因攻击选择和LLM输出随机性引入的估计不确定性（Section 3.3, Equation 2）。

**精确匹配度量**

$$r_{\mathrm{exact}}(x,y) = \min(r_{\mathrm{ROUGE}}^{\mathrm{recall}}(x,y), r_{\mathrm{ROUGE}}^{\mathrm{precision}}(x,y))$$

基于ROUGE-L的精确匹配得分，取召回率和精确度的最小值，用于评分函数中判断攻击是否成功改变了模型输出（Appendix D.1）。

**长度惩罚因子**

$$r_{\mathrm{length}}(x) = \min\left(0.5 + (1-0.5)\frac{\ell(x)}{100}, 1\right)$$

对过短输出施加的惩罚因子。当输出长度 $\ell(x) \geq 100$ 字符时，因子为1（无惩罚）；当输出极短时，因子趋近0.5，防止模型通过拒绝回答（输出极短的安全回复）来获得虚假的低漏洞评分（Appendix D.3, Equation 4）。

## 实验与分析

### 主要结果

**b³基准对34个主流骨干LLM进行了系统评估**，每个模型在10个威胁快照、3个防御等级上，使用210个高质量攻击（每快照每等级7个），每个攻击重复5次（N=5），总计约10.7万次模型调用。漏洞得分$V(m, T)$按公式(1)计算，95%置信区间通过非参数Bootstrap按公式(2)估计。

#### 总体排名与关键发现

**Figure 2 (right)** 展示了所有模型的总漏洞得分排名（得分越低安全性越高）。核心发现包括：


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/003_Figure_2.jpg]]
*Figure 2: (top left) Vulnerability scores for each task type (see Section 2.2.2), showing that the security of a model depends on the task type. We only include models that perform the best or the worst in at least one task type. (bottom left) LLMs with reasoning enabled have lower total vulnerability scores (lower is better). (right) Ranking based on total vulnerability scores for all models – lower score is better*

1. **推理能力显著提升安全性**：**Figure 2 (bottom left)** 显示，启用推理功能后，大多数模型的漏洞得分明显降低。这一趋势在多个模型家族中一致出现，表明增强推理能力是当前提升LLM安全性的有效机制。

2. **闭源模型系统级安全性优于开源模型**：**Figure 2 (bottom right)** 排名前几位的系统均使用闭源权重（如Claude系列、GPT系列），最佳开源模型kimi-k2-thinking得分约为0.34。需注意，闭源模型评估的是包含额外安全层和防护措施的系统级安全性，而开源模型评估的是模型级安全性，直接对比时应考虑这一差异。

3. **模型大小与安全性无显著正相关**：**Figure 9** 比较了同一模型家族中不同规模版本的漏洞得分。结果表明，未启用推理时，更大版本未表现出显著的安全优势；启用推理后，模型规模增大仅带来适度改善。这一发现挑战了“更大模型更安全”的直觉假设。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/014_Figure_9.jpg]]
*Figure 9: Vulnerability scores for differently sized models of the same families. There is no clear trend indicating that large models are more secure*

4. **安全性与效用总体正相关但存在显著离群值**：**Figure 16** 将b³漏洞得分与Artificial Analysis (2025)的Agent Intelligence Index（综合Terminal-Bench Hard和τ²-Bench Telecom）进行对比。大多数模型沿正相关方向聚集（安全性越高，效用越强），但存在几个显著离群值，如claude-haiku-4.5（高安全性、较低效用）和gpt-5.1、kimi-k2-thinking（较高效用、相对较低安全性）。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/024_Figure_16.jpg]]
*Figure 16: Security-utility tradeoff for different backbone LLMs. For security, we use the total vulnerability score from the $b ^ { 3 }$ . -benchmark (lower values indicate greater security); for agent utility, we use the agent intelligence index (Artificial Analysis, 2025) (higher values indicate stronger capabilities). The agent intelligence index combines results from the Terminal-Bench Hard, $\tau ^ { 2 }$ . -Bench Telecom. While security and utility are correlated, there are several outliers (e.g., claude-haiku-4.5, gpt-5.1 and kimi-k2-thinking)*

5. **安全性随时间略有改善但趋势微弱**：**Figure 11** 展示了漏洞得分与模型发布日期之间的关系。整体OLS趋势线显示安全性略有改善，但幅度很小。考虑到AI领域发展迅速但时间窗口较短、数据点有限，这一结果应谨慎解读。

#### 按任务类型的细粒度分析

**Figure 2 (top left)** 展示了不同任务类型下的漏洞得分。模型的安全表现因任务类型而异——某些模型在特定任务类型上表现最佳或最差，但在其他任务类型上排名可能完全不同。这验证了b³基准支持基于攻击类型进行细粒度排名的设计目标（Table 6中的Sub-ranking列）。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/026_Table_6.jpg]]

**Figure 15** 进一步展示了跨威胁快照关键切片的得分对比，包括内容安全相关任务和工具使用任务。模型排名在关键切片上大致保持稳定，但部分模型在特定类别上表现突出。

#### 按防御等级的对比

**Figure 14** 比较了不同防御等级（弱防御L1、强防御L2、自我判断L3）下的漏洞得分。claude-haiku-4.5在三个防御等级上均保持最安全的位置，表明其防护机制在不同强度防御设置下具有鲁棒性。

### 消融实验与鲁棒性分析

#### 攻击选择方法的鲁棒性

**Figure 8** 系统评估了攻击选择方法对整体排名的影响。通过比较选定攻击数据集与其他构造选择（分层采样、更大攻击集、低质量攻击、max聚合、排除部分攻击等）的Spearman秩相关系数：


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/012_Figure_8.jpg]]
*Figure 8: Overall ranking are not heavily influenced by the method used to select attacks. We plot the Spearman’s rho rank correlation between the selected attack dataset and other choices in the benchmark construction. The box plot on the left shows Spearman’s rho for random rankings*

- 所有修改方案的Spearman ρ均接近1，远高于随机排名的分布（左箱线图，中位数接近0，范围[-1, ~0.95]）
- 攻击质量对排名影响相对最大，但仍在可接受范围内
- 使用max聚合替代mean聚合对排名影响极小（ρ接近1）

这表明b³基准的排名对攻击选择方法具有强鲁棒性。

#### 威胁快照选择的影响

威胁快照变体与原快照的排名相关性为0.75，而重新适配攻击的相关性为0.57。这说明**快照选择比攻击选择更为重要**——威胁快照的设计质量对基准有效性具有更大影响。

#### 任务类型排名的鲁棒性

**Figure 10** 展示了单个任务类型排名在不同扰动下的Spearman ρ。六个任务类型（IIO、DTI、ITI、DIO、DAIS、DCE）在多种扰动下均保持较高的秩相关性，进一步验证了排名的稳定性。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/015_Figure_10.jpg]]
*Figure 10: Spearman’s rho rank correlation between the ranking for individual task types resulting from our selected benchmark setting and individual perturbations to that setting. (left) Box plot of Spearman’s rho for random rankings*

### 数据收集偏差分析

**Figure 13** 分析了自适应众包轮次中目标模型与非目标模型的漏洞得分分布。平均而言，被参与者选为目标攻击的模型与未被选中的模型具有相似的漏洞得分，表明数据收集过程中不存在强烈的选择偏差。这一发现支持了众包攻击收集方法的公平性。

### 公开与隐藏攻击的强度差异

公开数据集中已移除最强攻击以降低基准过拟合风险。公开攻击的平均得分为0.18，而用于评估的前210个高质量攻击平均得分为0.56，差距显著。这意味着公开版本的攻击强度明显较弱，模型开发商应避免仅针对公开测试集进行优化。

### 失败模式与局限性

1. **单步评估的固有局限**：威胁快照仅评估单步LLM调用，可能无法完全反映多步攻击的复杂性。然而，这可视为安全性的下界估计——若单步已存在漏洞，多步攻击场景下风险只增不减。

2. **覆盖度限制**：当前基准仅包含基于10种代理架构构建的威胁快照，可能无法覆盖未来新型攻击面和代理架构。Table 2列出了这10个威胁快照的详细攻击向量和目标分类。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/010_Table_2.jpg]]
*Table 2: Overview of the agents and attack categorization used in the threat snapshots. These remain fixed for the different defenses ℓ ∈ {L1, L2, L3}*

3. **开源与闭源模型的可比性**：闭源模型包含额外的安全层和防护措施，与开源模型的直接比较可能存在不公平性。这一差异在解读排名时应予以考虑。

4. **推理Token用量的影响**：**Table 4** 报告了部分模型的推理Token用量（部分提供商未返回此数据）。推理能力的启用伴随着计算成本的增加，但本文未深入分析安全性提升与推理开销之间的权衡关系。

### 补充图表

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/011_Table_3.jpg]]
*Table 3: Overview of different subsets of threat snapshots to condition on*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/025_Table_5.jpg]]
*Table 5: List of all models with developer and API provider that were evaluated in this paper. Models marked with ∗ were run with the AWS Bedrock API during data collection. Models marked with † were evaluated twice, both with reasoning enabled at a medium setting and with reasoning disabled (where possible) or set to the minimum level*

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_kga18ld70t/figures/020_Table_4.jpg]]
*Table 4: Reasoning tokens used, as reported by in API responses. Some model providers do not return this data and are therefore not included*

## 方法谱系与知识库定位

### 1. 与现有基准的关系与差异化

**威胁快照框架**（Threat Snapshots Framework）的提出，根植于现有AI代理安全基准的两个结构性局限：**评估粒度过粗**与**攻击覆盖不足**。本节从评估方法论和攻击生成两个维度，定位其相对于代表性基线工作的创新。

#### 1.1 评估方法论：从全代理模拟到单步隔离

现有安全基准普遍采用**完整代理模拟**范式，要求构建完整的代理执行环境并模拟多步交互流程：

- **Agent Security Bench (ASB)**（Zhang et al., 2025）基于代理模拟评估LLM安全性，但其评估结果混杂了代理框架本身的鲁棒性，难以归因于骨干LLM的固有漏洞。
- **AgentDojo**（Debenedetti et al., 2024）和**InjecAgent**（Zhan et al., 2024）同样依赖完整代理执行流，评估成本高且可复现性受代理实现细节影响。
- **AgentHarm**（Andriushchenko et al., 2025）虽聚焦安全危害，但评估范式仍绑定于端到端代理行为。

威胁快照框架的核心方法论转换在于：**将安全评估聚焦于LLM调用的孤立状态**，而非完整代理执行流。具体而言，框架通过重构单次LLM调用时刻的上下文 $C_t$、攻击注入方式和评分函数，完整描述一个LLM漏洞实例（Section 2.2.1, Figure 3）。这一设计带来了两个关键优势：

1. **归因清晰**：漏洞评分直接反映骨干LLM的安全性，排除了代理框架中处理函数 $f_{\mathrm{proc}}$ 等外部组件的干扰。
2. **覆盖广泛**：无需为每种代理架构重新构建模拟环境，10个威胁快照即可覆盖多种应用场景下的安全威胁。

#### 1.2 攻击生成：从模板化到众包对抗

攻击生成方式构成另一关键差异点。现有基准多采用**固定模板攻击**（templated attacks），攻击多样性受限于预设模板的覆盖范围。b³基准则采用**基于众包的、针对上下文的对抗性攻击**（crowd-sourced, context-dependent adversarial attacks）：

- 通过游戏化红队挑战，收集了194,331个独特攻击（Section 3.2）。
- 攻击者被随机分配到7种骨干LLM之一，针对特定威胁快照生成攻击，确保攻击与上下文的适配性。
- 从成功攻击中筛选出top 210个高质量攻击用于最终评估，其平均得分达0.56，显著高于公开攻击数据的0.18（Section 3.2）。

这一设计使攻击库具备更强的针对性和对抗强度，但也引入了公开基准攻击强度被人为削弱的风险——最强攻击已从公开数据集中移除，以防止模型开发商过拟合。

#### 1.3 细粒度排名能力

威胁快照框架支持基于不同维度的**细粒度漏洞得分排名**，这是现有基准普遍缺乏的能力。具体而言，b³基准允许按以下维度切片排名（Table 6, Table 3）：

- **防御等级**：弱防御（L1）、强防御（L2）、自判断（L3）
- **攻击类型**：直接/间接、消息/工具/混合目标
- **任务类型**：内容安全、工具使用等
- **威胁快照子集**：有无工具、攻击路径等

这种细粒度排名能力使安全评估从单一总分扩展到多维安全画像，为模型选择提供更丰富的决策信息。

### 2. 攻击分类体系的知识贡献

本工作构建了**独立的攻击分类体系**，而非沿用现有分类法（Section 2.2.2）。该分类从两个正交维度系统化覆盖攻击面：

- **攻击向量**（delivery method）：直接攻击（Direct）与间接攻击（Indirect）
- **攻击目标**（targeted LLM capability）：消息生成（Message）、工具调用（Tool）、两者兼具（Both）

这一2×3分类矩阵产生了六种攻击类型（Table 1）：DIO、DTI、DCE、IIO、ITI、DAIS。该分类体系的设计目标是为威胁快照的构建提供系统化覆盖保证，而非追求与现有分类法的兼容性。

### 3. 适用边界与局限

威胁快照框架的适用边界由其设计选择直接决定，以下局限需要在应用时审慎考量：

**单步评估的固有局限**。威胁快照仅评估单步LLM调用，无法完全反映多步攻击的复杂性。尽管框架支持将多步攻击分解为威胁快照链（如Crescendo攻击的分解，Figure 5），但本工作仅聚焦单步快照。这意味着b³基准提供的安全评分应被理解为**安全性的下界估计**——实际多步攻击场景中，漏洞可能被放大。

**覆盖范围的时效性约束**。基准数据集仅包含基于当前代理架构构建的10种威胁快照，可能无法覆盖未来新型攻击面和代理架构（如多模态代理、具身代理等）。

**开源与闭源模型的比较不对称**。闭源模型（如Claude、GPT系列）评估的是**系统级安全性**，包含额外的安全层和防护措施；而开源模型（如Llama系列）评估的是**模型级安全性**。直接对比这两类模型的安全评分时，需注意这一结构性差异。

**公开基准的攻击强度衰减**。为降低过拟合风险，最强攻击已从公开数据集中移除，公开版本的攻击强度（平均得分0.18）显著弱于完整评估所用攻击（平均得分0.56）。这可能导致公开基准的区分度不足，且模型开发商可能针对公开测试集进行过拟合。

**攻击收集的潜在偏差**。数据收集过程中，参与者被随机分配到特定骨干LLM，统计分析表明目标模型与非目标模型的漏洞评分相似（Figure 13），偏差较小但仍不可完全排除。

### 4. 开放问题

基于上述局限，以下开放问题值得后续工作关注：

1. **多模态与多步扩展**：如何将威胁快照框架拓展到多模态代理及非文本攻击？如何系统化评估多步攻击链中漏洞的传播与放大效应？

2. **自动化攻击生成**：如何实现自动化对抗攻击生成以替代昂贵的人工红队，同时保持攻击质量和上下文适配性？这将直接影响基准的可扩展性和更新频率。

3. **安全评分与系统风险的关联**：在真实生产环境中，如何将骨干LLM的安全评分与总体代理系统的安全风险关联？单步漏洞评分如何映射到端到端安全危害？

4. **基准的自动演进**：随着模型和代理架构的演进，如何自动化地更新威胁快照集以保持基准的覆盖度和代表性？这涉及攻击面发现、快照生成和质量验证的完整自动化链路。

5. **从评估到防御**：将威胁快照用于针对性防御机制（如动态系统提示加固）的效果如何？框架能否从评估工具演进为防御生成工具？

## 原文 PDF

![[paperPDFs/ICLR_2026/Breaking_Agent_Backbones_Evaluating_the_Security_of_Backbone_LLMs_in_AI_Agents.pdf]]
