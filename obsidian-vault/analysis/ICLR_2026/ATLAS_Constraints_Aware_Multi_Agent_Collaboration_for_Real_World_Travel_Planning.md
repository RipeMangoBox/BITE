---
title: "ATLAS: Constraints-Aware Multi-Agent Collaboration for Real-World Travel Planning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ATLAS_Constraints_Aware_Multi_Agent_Collaboration_for_Real_World_Travel_Planning.pdf
project_link: null
code_link: null
aliases:
- AABTPLAS
- ATLAS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "ATLAS将旅行规划形式化为CSP，并用约束管理器、规划器、检查器和搜索顾问分工协作。"
primary_logic: "系统先提取搜索域和显隐式约束，再循环生成、验证、诊断信息缺口并触发自适应搜索。"
claims:
- "显式约束构建使旅行规划不再依赖LLM隐式记忆常识约束。"
- "规划器与检查器的迭代循环将计划生成和约束验证解耦。"
- "自适应交错搜索在TravelPlanner和真实多轮规划场景中提升最终通过率。"
---

# ATLAS: Constraints-Aware Multi-Agent Collaboration for Real-World Travel Planning

> [!tip] 核心洞察
> 通过将旅行规划形式化为约束满足问题（CSP），并引入专门的约束管理器（Constraint Manager）来枚举显式和隐式约束、检查器（Checker）进行迭代验证、搜索顾问（Search Advisor）在不可满足时诊断信息缺口并引导自适应搜索，可以系统性地解决复杂约束下的规划问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ATLAS：面向真实世界旅行规划的约束感知多智能体协作框架 |
| 英文题名 | ATLAS: Constraints-Aware Multi-Agent Collaboration for Real-World Travel Planning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=mIYGiBf9Pm) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | ATLAS (Agent-based Travel planning with Live Adaptive Search) |
| Dataset | TravelPlanner (validation set), TravelPlanner (test set), Live Travel Planning (real-world, multi-turn), Flex-TravelPlanner (multi-turn) |

> [!tip] 效果简介
> - TravelPlanner (validation set) 上，Final Pass 为 44.44，对比 23.3 (best alternative)，变化 +21.14。
> - TravelPlanner (test set) 上，Final Pass 为 35.00，对比 N/A，变化 N/A。
> - Live Travel Planning (real-world, multi-turn) 上，Final Pass 为 84，对比 59 (ReAct), 27 (Monolithic)，变化 +25 (vs ReAct), +57 (vs Monolithic)。

## 概要

ATLAS（Agent-based Travel planning with Live Adaptive Search）是一个面向真实世界旅行规划的约束感知多智能体协作框架。该框架将旅行规划形式化为约束满足问题（CSP），通过五个专门化的智能体模块——搜索智能体（Search Agent）、约束管理器（Constraint Manager）、规划器（Planner）、检查器（Checker）和搜索顾问（Search Advisor）——系统性地解决显式约束、隐式常识约束以及动态演化约束带来的挑战。在TravelPlanner基准上，ATLAS将最终通过率（Final Pass）从最佳基线的23.3%提升至44.4%；在包含实时搜索和多轮反馈的真实场景中，ATLAS达到84%的最终通过率，显著优于ReAct（59%）和单体智能体（27%）。

现有LLM方法在旅行规划任务中面临三个根本性挑战：

- **约束构建（Constraint Construction）**：约束不仅来自用户查询中的显式要求（如预算、日期、人数），还来自搜索结果中的隐含规则（如酒店最低入住天数），以及常识性约束（如到达后需要午餐、往返行程需闭环）。现有方法隐式依赖LLM内部知识，无法系统性地枚举这些约束。

- **约束感知规划（Constraints-Aware Answering）**：即使约束被识别，LLM在生成计划时仍频繁违反约束，产生逻辑错误和幻觉。如Figure 1所示，即使先进模型如Gemini-2.5-Pro也会出现“上午9点到达却遗漏午餐”或“推荐不同城市的餐厅”等关键失败。

- **信息缺口解决（Resolving Information Gap）**：当当前信息不足以生成有效计划时，系统需要诊断缺失信息并引导自适应搜索。现有方法要么无自适应搜索，要么仅执行固定搜索，无法针对性地填补信息缺口。

## 核心方法与创新机理

ATLAS的核心创新在于将旅行规划形式化为约束满足问题（CSP），并通过多智能体分工协作系统性地解决上述挑战：

1. **约束管理器（Constraint Manager）**：显式枚举来自用户查询和搜索结果的显式约束（$C_E^{t,\ell}$）以及来自常识规则的隐式约束（$C_I$），将约束处理从隐式依赖LLM内部知识转变为显式编码。

2. **规划器-检查器迭代循环（Planner-Checker Loop）**：规划器生成候选计划后，检查器验证其是否满足所有约束，输出valid/invalid/unsat三种判决并提供反馈。这一迭代过程（最多K次）实现了“生成-测试”范式，将规划与验证解耦。

3. **自适应交错搜索（Adaptive Interleaved Search）**：当检查器返回unsat时，搜索顾问诊断信息缺口并生成针对性搜索反馈，驱动搜索智能体获取新信息。这一机制实现了在部分可观测环境中的规划与感知行动交错。

4. **多轮对话缓存机制**：在多轮场景中，ATLAS缓存上一轮的域信息，仅当检查器在K次修订后仍返回unsat时才触发新的交错搜索，避免从头开始。

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_mIYGiBf9Pm_ATLAS_Constra/figures/001_Figure_1.jpg]]
*Figure 1: Monolithic agent cannot solve real-world travel planning. The true challenge in realworld travel planning is satisfying both explicit user requests and implicit, commonsense expectations (in dotted bubble 1). Even advanced models like Gemini-2.5-Pro fall short, as seen in critical failures like omitting lunch after a 9 a.m. arrival or suggesting a restaurant in a different city. This highlights the vital need for a multi-agentic solution like ATLAS.*

ATLAS的整体工作流程如Figure 2所示。给定用户查询$Q^t$，框架按以下步骤运行：

1. **搜索阶段**：搜索智能体通过工具调用收集原始观测$O^{t,\ell}$，并提取结构化域$D^{t,\ell}$。
2. **约束构建阶段**：约束管理器从查询和域中提取显式约束$C_E^{t,\ell}$，并结合隐式约束$C_I$，形成完整约束集$C^{t,\ell}$。
3. **规划阶段**：规划器基于当前域和约束集，结合历史失败分配和反馈，生成候选计划$\sigma^{t,\ell,k}$。
4. **检查阶段**：检查器验证候选计划是否满足所有约束，输出判决$V^{t,\ell,k}$和反馈$F_{plan}^{t,\ell,k}$。
5. **自适应搜索阶段**：若检查器返回unsat，搜索顾问诊断信息缺口并生成搜索反馈$F_{search}^{t,\ell}$，触发新的搜索步骤。

框架使用两个超参数：$K$（最大检查步骤数）和$L$（交错搜索步数）。在单轮规划中，默认设置$K=3, L=10$；在多轮实时搜索中，默认设置$K=3, L=5$。

### 5.1 问题形式化

ATLAS将旅行规划形式化为约束满足问题（CSP）：

$$P = \langle X, D, C \rangle$$

其中$X$为变量集（如每日的交通、餐饮、景点、住宿），$D$为域集（各变量的可选值范围），$C$为约束集。一个完整分配$\sigma$满足约束$c_j$当且仅当：

$$\langle \sigma(x) | x \in \mathrm{scope}(c_j) \rangle \in \mathrm{rel}(c_j)$$

多轮对话将问题转化为动态CSP，即一系列静态CSP的序列$\mathcal{P}^1, \mathcal{P}^2, \ldots, \mathcal{P}^t$，每个分配$\sigma_t$必须满足其对应问题$P^t$中的所有约束。

### 5.2 搜索智能体（Search Agent）

搜索智能体通过工具调用与外部环境交互，收集原始观测并提取结构化域：

$$D^{t,\ell} := \mathsf{Search}(Q^t, F_{\mathrm{search}}^{t,\ell-1}) = (\Gamma \circ \Omega)(Q^t, F_{\mathrm{search}}^{t,\ell-1})$$

其中$\Omega$为原始观测收集函数，$\Gamma$为域提取函数。

### 5.3 约束管理器（Constraint Manager）

约束管理器将来自查询和域的显式约束与隐式约束合并：

$$C^{t,\ell} := \mathrm{Constrain}(Q^t, D^{t,\ell}) = C_E^{t,\ell} \cup C_I, \quad C_E^{t,\ell} := \Pi(Q^t, D^{t,\ell})$$

其中$\Pi$为显式约束提取函数，$C_I$为固定常识约束集。Table 4列出了考虑的约束类型，包括硬约束（如预算、日期、人数）和常识约束（如闭环行程、合理用餐时间）。

### 5.4 规划器（Planner）

规划器利用先前分配和反馈的历史生成候选分配：

$$\boldsymbol{\sigma}^{t,\ell,k} := \mathsf{Plan}\big(X, D^{t,\ell}, C^{t,\ell}; \{(\boldsymbol{\sigma}^{t,\ell,i}, F_{plan}^{t,\ell,i})\}_{i=1}^{k-1}\big)$$

### 5.5 检查器（Checker）

检查器验证分配是否满足约束，返回判决和反馈：

$$(V^{t,\ell,k}, F_{\mathrm{plan}}^{t,\ell,k}) := \mathrm{Check}(Q^t, D^{t,\ell}, C^{t,\ell}, \sigma^{t,\ell,k})$$

判决$V \in \{\text{valid}, \text{invalid}, \text{unsat}\}$，其中unsat表示当前信息下无法生成有效计划。

### 5.6 搜索顾问（Search Advisor）

当检查器返回unsat时，搜索顾问利用规划历史$H$诊断信息缺口并生成搜索反馈：

$$F_{\mathrm{search}}^{t,\ell} := \mathsf{SearchAdvise}(Q^t, D^{t,\ell}, C^{t,\ell}, H^{t,\ell,k})$$

### 5.7 多轮扩展

在多轮场景中，新CSP使用上一轮缓存的域和来自新查询的显式约束：

$$P^{t+1,1} = \langle X, D^{t,L}, C^{t+1,1} \rangle, \quad C^{t+1,1} := C_E^{t+1,1} \cup C_I, \quad C_E^{t+1,1} = \Pi(Q^{t+1}, D^{t,L})$$

## 实验与关键发现

### 6.1 主要结果

ATLAS在TravelPlanner基准上的主要结果如Table 1所示：

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_mIYGiBf9Pm_ATLAS_Constra/figures/003_Table_1.jpg]]
*Table 1: ATLAS consistently achieves the highest performance on the TravelPlanner benchmark.*

| 方法 | 验证集 Final Pass | 测试集 Final Pass |
|------|-------------------|-------------------|
| ATLAS (Gemini-2.5-Pro) | **44.44** | **35.00** |
| ATLAS (Claude-Sonnet-4) | 23.33 | 18.00 |
| 最佳基线 | 23.3 | - |

在实时旅行规划场景中（Figure 4），ATLAS经过多轮反馈后达到84%的最终通过率，显著优于ReAct（59%）和单体智能体（27%）。

### 6.2 消融实验

关键组件的消融实验结果如Figure 3和Table 5所示：

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_mIYGiBf9Pm_ATLAS_Constra/figures/012_Table_5.jpg]]
*Table 5: Ablations on the key components of ATLAS . Results are on the TravelPlanner validation set using Gemini-2.5-pro. (a) Without vs with Constraint Manager using 5 check steps and 10 interleaved search steps.*

- **约束管理器**：禁用约束管理器导致硬约束宏通过率绝对下降14.4%（Figure 3a）。
- **检查步骤数**：单次检查步骤（$K=1$）将最终通过率从20.6%提升至29.4%（Figure 3b）。
- **交错搜索步数**：交错搜索（$L=5$）将最终通过率从31.1%提升至44.4%（Figure 3c）。
- **基准特定提示**：提供基准特定的非常规提示作为显式约束后，最终通过率从44%提升至60%（Figure 6）。

### 6.3 多轮规划结果

在Flex-TravelPlanner多轮规划基准上（Table 2和Table 6），ATLAS达到42.19%的最终通过率，在所有约束类型上均保持100%的交付率（Delivery）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_mIYGiBf9Pm_ATLAS_Constra/figures/007_Table_2.jpg]]
*Table 2: Main results on the Flex-TravelPlanner benchmark for multi-turn planning.*

### 6.4 难度与天数消融

- **旅行天数**（Table 9）：ATLAS在3天行程上表现最佳，最终通过率75.00%（Gemini-2.5-Pro），7天行程下降至26.67%。
- **任务难度**（Table 10）：ATLAS在困难子集上最终通过率55.00%，优于ReAct的21.67%，且表现优于中等难度子集，表明框架对复杂约束场景特别有效。

### 6.5 成本分析

如Table 11所示，ATLAS的中位运行时间在3天行程上为4.07分钟，5天为8.26分钟，7天为7.97分钟。规划器是最耗资源的组件，但约束相关智能体（检查器和约束管理器）增加的开销相对于其带来的性能提升是微小的。

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_mIYGiBf9Pm_ATLAS_Constra/figures/010_Table_3.jpg]]
*Table 3: Typed function signatures for the agents in ATLAS. We use $P ^ { t , \ell }$ as a shorthand for the CSP instance $\langle \overset { \bullet \mathrm { ~ \scriptscriptstyle ~ 1 ~ } } { X } , D ^ { t , \ell } , C ^ { t , \ell } \rangle$ . The indices t, ℓ, k represent the conversation turn, the (interleaved) search step, and the planner-checker interaction step, respectively.

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_mIYGiBf9Pm_ATLAS_Constra/figures/011_Table_4.jpg]]
*Table 4: Descriptions on the considered constraint.*

## 定位与知识库关联

ATLAS的方法论根植于经典人工智能中的约束满足问题（CSP）框架（Mackworth, 1977; Brailsford et al., 1999b），并借鉴了以下研究脉络：

- **LLM规划与约束感知**：与Kambhampati et al. (2024)的“LLM-modulo”框架一脉相承，ATLAS采用“生成-测试”范式，将LLM作为规划生成器，通过外部验证器确保约束合规。与Parmar et al. (2025)和Lee et al. (2025)等假设所有信息预先可用的方法不同，ATLAS通过自适应搜索处理信息缺口。

- **多智能体协作**：ATLAS扩展了PMC（Zhang et al., 2025）和EvoAgent（Yuan et al., 2025）等多智能体框架，引入了专门的约束管理器和搜索顾问，实现了更细粒度的分工。

- **工具增强LLM**：基于ReAct（Yao et al., 2023）和Toolformer（Schick et al., 2023）等工具调用范式，ATLAS的搜索智能体通过工具调用与外部环境交互。

- **动态CSP**：多轮对话处理借鉴了动态CSP（Mittal & Falkenhainer; Dechter & Dechter, 1988）的思想，将问题视为一系列静态CSP的序列。

ATLAS在知识库中的定位是：**首个将CSP形式化、显式约束管理、迭代验证和自适应搜索系统性地整合到多智能体LLM框架中的旅行规划方法**。其核心贡献在于证明了通过解耦约束处理、规划生成和验证反馈，可以显著提升LLM在复杂约束场景下的规划能力。未来工作方向包括：集成并行测试时扩展技术（Chen et al., 2025）提升规划器效率，增强检查器为形式化CSP求解器（Hao et al., 2025b）实现更鲁棒的验证，以及将框架迁移到隐私策略合规、个性化用户偏好建模等新领域。

## 原文 PDF

![[paperPDFs/ICLR_2026/ATLAS_Constraints_Aware_Multi_Agent_Collaboration_for_Real_World_Travel_Planning.pdf]]
