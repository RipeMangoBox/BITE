---
title: "MedAgent-Pro: Towards Evidence-based Multi-modal Medical Diagnosis via Reasoning Agentic Workflow"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MedAgent_Pro_Towards_Evidence_based_Multi_modal_Medical_Diagnosis_via_Reasoning_Agentic_Workflow.pdf
openreview_forum_id: ZOuU0udyA4
aliases:
- MP
- MedAgent-Pro
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过模拟现代临床诊断的两阶段实践，设计了一个层次化的代理工作流：在疾病层面借助RAG检索临床指南生成标准化诊断计划，在患者层面结合专业工具进行定量分析和基于证据的反思，确保每一步推理都建立在可靠的证据基础之上。"
primary_logic: "将诊断过程分解为疾病特定的标准化计划与患者特定的个性化推理，显式引入检索式临床知识、工具驱动的定量分析以及证据驱动反思，能够显著提升多模态医学诊断的准确性和可靠性。"
claims:
- "MedAgent-Pro在青光眼诊断上的bAcc相比GPT-4o提升34.0%。"
- "消融实验证明规划、工具动作和反思三个组件均为最终性能带来显著增益，三者配合可达到最佳性能。"
- "在缺少可用视觉工具的NEJM病例上，MedAgent-Pro依然表现最优，说明其推理结构本身具备鲁棒性。"
- "REFUGE2 (Glaucoma) 上 bAcc (%) = 90.4"
---

# MedAgent-Pro: Towards Evidence-based Multi-modal Medical Diagnosis via Reasoning Agentic Workflow

> [!tip] 核心洞察
> 将诊断过程分解为疾病特定的标准化计划与患者特定的个性化推理，显式引入检索式临床知识、工具驱动的定量分析以及证据驱动反思，能够显著提升多模态医学诊断的准确性和可靠性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MedAgent-Pro：基于证据的多模态医学诊断推理代理工作流 |
| 英文题名 | MedAgent-Pro: Towards Evidence-based Multi-modal Medical Diagnosis via Reasoning Agentic Workflow |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ZOuU0udyA4) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | MedAgent-Pro |
| Dataset | REFUGE2 (Glaucoma), MITEA (Heart Disease) |

> [!tip] 效果简介
> - REFUGE2 (Glaucoma) 上，bAcc (%) 为 90.4，对比 56.4 (GPT-4o)，变化 +34.0。
> - REFUGE2 (Glaucoma) 上，F1 (%) 为 76.4，对比 21.1 (GPT-4o)，变化 +55.3。
> - MITEA (Heart Disease) 上，bAcc (%) 为 77.8，对比 56.8 (GPT-4o)，变化 +21.0。

## 概述

现有医学多模态诊断方法普遍存在一个关键瓶颈：它们倾向于直接输出基于经验的诊断结论，缺乏由定量分析支撑的临床证据，且未遵循标准化的诊断工作流，导致结果不可靠、临床可用性差。**MedAgent-Pro** 针对这一问题，提出了一种基于证据的多模态医学诊断推理代理工作流，其核心洞察在于：将诊断过程显式分解为疾病特定的标准化规划与患者特定的个性化推理，通过检索式临床知识注入、专业工具驱动的定量分析以及证据驱动反思，使每一步推理都建立在可靠的证据基础之上。

具体而言，MedAgent-Pro 采用层次化代理架构：在疾病层面，借助检索增强生成（RAG）代理从 MedlinePlus 知识库（覆盖 1000+ 疾病、4000+ 专家审核指南）检索临床指南，生成标准化的诊断计划；在患者层面，根据可用数据筛选可执行步骤，调用视觉分割/定位等专业工具进行定量分析，并通过基于证据的反思机制动态评估中间结果的可靠性，最终以风险加权的方式做出诊断决策。

实验结果表明，MedAgent-Pro 在多个基准上显著超越现有方法：在青光眼诊断（REFUGE2）上，bAcc 相比 GPT-4o 提升 **34.0%**（56.4% → 90.4%），F1 提升 **55.3%**；在心脏病诊断（MITEA）上，bAcc 提升 **21.0%**（56.8% → 77.8%），F1 提升 **44.2%**；在 NEJM 多模态病例上准确率达到 **81.7%**（+10.8%）；在 MIMIC 胸部 X 光 12 项子任务上平均 bAcc 达到 **72.0%**（+13.7%）。消融实验进一步证实，规划、工具动作和证据反思三个组件各自带来显著增益，三者配合达到最优性能。值得注意的是，即使在缺少可用视觉工具的 NEJM 病例上，MedAgent-Pro 依然表现最优，说明其推理结构本身具备鲁棒性，性能提升源于工作流设计而非单纯的工具堆砌。

## 背景与动机

多模态医学诊断要求模型同时理解影像数据与文本病历，并输出可靠的诊断结论。近年来，通用视觉语言模型（VLM）如GPT-4o和专用医疗VLM如LLaVA-Med在该领域取得了显著进展，但现有方法普遍存在一个根本性瓶颈：它们倾向于直接输出基于经验的诊断答案，缺乏由定量分析支撑的临床证据，且未遵循标准化的诊断工作流。这一缺陷直接导致诊断结果不可靠、临床可用性差——模型可能给出看似合理的结论，却无法追溯其推理依据，更无法提供医生所需的客观指标。

图1直观展示了这一差距：在青光眼和心脏病两类典型疾病上，主流VLM和现有医疗代理系统（如MedAgents、MMedAgent）的诊断输出要么缺乏定量证据，要么推理链条不完整，而临床诊断恰恰要求每一步判断都建立在可验证的证据之上。

问题的根源在于当前方法的两个结构性缺失。其一，诊断过程缺乏疾病特异性的标准化指导——不同疾病对应不同的临床指南和检查流程，但现有模型仅依赖内部知识进行一次性推理，无法保证诊断路径符合临床规范。其二，患者层面的分析停留在VLM的定性判断层面，未能有效利用专业视觉工具（如分割模型、定位模型）进行精确的定量指标计算。即使部分工作尝试引入工具，也缺乏将工具调用结果组织为连贯证据链的推理框架。

基于上述分析，本文的核心动机是：能否构建一种显式模拟现代临床诊断实践的工作流，将检索式临床知识、工具驱动的定量分析以及证据驱动的反思机制有机整合，使多模态医学诊断的每一步推理都建立在可靠的证据基础之上？

## 核心创新

MedAgent-Pro 的核心创新在于将现代临床诊断的两阶段实践——疾病级标准化指南制定与患者级个性化推理——映射为一个层次化的代理工作流，从根本上改变了现有方法“端到端直接输出答案”的范式。其关键创新体现在以下四个维度：

### 1. 诊断范式重构：从端到端生成到层次化代理工作流

现有通用 VLM（如 GPT-4o）和医疗代理系统（如 **MedAgents** (Tang et al., ACL 2024)、**MMedAgent** (Li et al., EMNLP 2024)）通常直接将多模态输入映射为诊断结论，缺乏标准化的临床推理过程。MedAgent-Pro 将诊断分解为两个层次：

- **疾病级规划**：针对特定疾病，利用 RAG 代理从 MedlinePlus 知识库（覆盖 1000+ 疾病、4000+ 经 NIH/NLM 认证的专家指南）检索临床指南，生成标准化的诊断计划 $\mathcal{P}$，其中每一步定义为 $P_i: r_i = a_i(o_i), a_i \in \mathcal{A}$，明确了所需的分析动作、输入对象和预期输出。
- **患者级推理**：根据患者实际拥有的数据 $\mathcal{D}$ 筛选可执行步骤，初始化患者记忆 $\mathcal{M} = \{ P_i \in \mathcal{P} \mid o_i \in \mathcal{D} \}$，然后逐步执行计划中的每一项分析。

这一范式转变是性能提升的核心驱动力：消融实验（Table 4）表明，仅加入疾病级规划即可带来显著的性能增益。

### 2. 临床知识集成：从隐式依赖到显式检索注入

基线 VLM 完全依赖其参数化内部知识进行诊断，缺乏可追溯的临床依据。MedAgent-Pro 通过 RAG 代理实现了两阶段检索（Figure 3），将 MedlinePlus 中的结构化临床指南显式注入规划过程，使每一步诊断计划都建立在权威医学知识的基础上。这不仅提升了诊断的标准化程度，也使推理过程具备可解释性和可审计性。

### 3. 定量分析能力：从定性判断到工具驱动的精确测量

现有方法仅由 VLM 进行定性视觉判断，无法提供临床诊断所需的定量证据。MedAgent-Pro 集成了专业视觉工具（如分割模型、定位模型），能够执行精确的定量指标计算。消融实验（Table 4）显示，加入工具动作后，青光眼 F1 提升 34.5%，心脏病 F1 提升 20.7%，证实定量分析对诊断增益至关重要。进一步分析（Figure 5）表明，分割精度越高，最终诊断性能越好，验证了定量分析模块在证据链中的核心地位。

### 4. 推理可靠性保障：从无纠错到证据驱动反思

现有方法缺乏对中间推理步骤的可靠性评估机制。MedAgent-Pro 引入了基于证据的反思模块，通过零样本评估函数 $\phi(r_i, o_i, G)$ 判断每一步输出的可靠性，动态决定推理状态：

$$
s_i = \begin{cases} Complete & r_i \in \mathbb{Z} \\ Terminate & r_i \notin \mathbb{Z} \land \neg \phi(r_i, o_i, G) \\ Continue & r_i \notin \mathbb{Z} \land \phi(r_i, o_i, G) \end{cases}
$$

若中间结果可靠，则作为证据传递至后续步骤；若不可靠，则终止当前路径。这一机制确保了推理链的一致性和证据完整性。消融实验（Table 4）证实，反思模块使整体性能达到最优。此外，即使直接向基线 VLM 提供全部工具（Table 6），它们也无法有效组织推理链，说明工作流设计本身——而非工具——才是性能提升的决定性因素。

### 创新本质总结

MedAgent-Pro 的四个 changed slots 并非孤立改进，而是形成了一条完整的证据链：**标准化计划定义“该查什么” → 工具动作实现“精确查” → 证据反思确保“查得对” → 风险加权决策给出“可靠结论”**。这一设计使得诊断过程从“黑箱猜测”转变为可追溯、可验证的循证推理，在青光眼诊断上相对 GPT-4o 实现 34.0% bAcc 的提升（Table 1），并在缺少可用视觉工具的 NEJM 病例上依然表现最优（Table 18），证明了推理结构本身的鲁棒性。

## 整体框架

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_ZOuU0udyA4/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the MedAgent-Pro. MedAgent-Pro performs diagnosis through a hierarchical structure, with reasoning guided by a VLM supported by an RAG agent and specialized tools. Evi. means Evidence-based in the figure*

MedAgent-Pro 提出了一种**层次化诊断推理工作流**，其核心设计思想是将现代临床诊断的两阶段实践显式建模为：**疾病级标准化计划生成**与**患者级个性化证据推理**。该框架由视觉语言模型（VLM）主导推理过程，并借助检索增强生成（RAG）代理和专业视觉工具来弥补 VLM 在临床知识覆盖与定量分析能力上的不足。

整体工作流可概括为以下五个模块的串联协作（图2）：

1. **疾病级知识库规划**：给定待诊断的疾病类型，RAG 代理从基于 MedlinePlus 构建的大规模知识库（覆盖 1000+ 疾病、4000+ 经 NIH/NLM 认证的指南）中检索相关临床指南，生成标准化的诊断计划 $\mathcal{P}$。该计划由一系列步骤 $\{P_1, P_2, \dots, P_n\}$ 组成，每个步骤 $P_i: r_i = a_i(o_i), a_i \in \mathcal{A}$ 定义了需要分析的对象 $o_i$、执行的动作 $a_i$ 以及预期的输出 $r_i$。

2. **患者级记忆初始化**：根据当前患者实际拥有的数据 $\mathcal{D}$（如眼底照片、视野检查报告等），筛选诊断计划中可执行的步骤，形成患者的长时诊断记忆 $\mathcal{M} = \{ P_i \in \mathcal{P} \mid o_i \in \mathcal{D} \}$。这一步确保推理过程仅基于可用证据展开。

3. **基于工具的动作执行**：按计划逐步执行 $\mathcal{M}$ 中的每个步骤。对于需要定量分析的临床指标（如杯盘比、视野缺损范围），调用专业视觉分割/定位模型和编码工具进行精确计算；对于定性指标（如视盘形态描述），则由 VLM 直接分析并输出结构化结果。

4. **基于证据的反思**：每步执行后，通过零样本评估函数 $\phi$ 判断中间结果的可靠性，并据此决定推理状态 $s_i$：
   - 若 $r_i$ 为最终临床指标（数值型），标记为 **Complete**；
   - 若 $r_i$ 不可靠（如分割失败或输出与指南 $G$ 不一致），标记为 **Terminate**，终止该步骤；
   - 否则标记为 **Continue**，将 $r_i$ 作为可靠证据传递至后续步骤。

5. **基于风险的决策**：收集所有可靠指标构成最终指标集 $\mathcal{R}_{final}$，由 VLM 根据临床指南为每个指标赋予风险权重 $w_i$，计算加权风险分数 $\rho = \sum_{i=0}^{l} w_i r_i$，并与预设阈值 $\theta$ 比较得出最终诊断结论。

该框架的关键创新在于将**诊断推理过程分解为标准化计划与个性化执行两个层次**，并通过证据反思机制确保每一步推理都建立在可追溯的临床证据之上。消融实验（表4）证实，规划、工具动作和反思三个组件均为最终性能带来显著增益，三者配合可达到最佳性能。值得注意的是，即使在缺少可用视觉工具的 NEJM 病例上（表18），MedAgent-Pro 依然表现最优，说明其推理结构本身具备鲁棒性，而非单纯依赖工具堆砌。

## 核心模块与公式推导

MedAgent-Pro 的诊断流程由四个核心模块串联构成，形成“疾病级规划 → 患者级记忆初始化 → 工具驱动动作执行 → 证据反思与决策”的层次化推理链路。

### 疾病级知识库规划

该模块的目标是为每种疾病生成标准化的诊断计划 $\mathcal{P}$。系统首先通过 RAG 代理从 MedlinePlus 构建的大规模知识库 $\mathcal{K}$（覆盖 1000+ 疾病、4000+ 经 NIH/NLM 认证的临床指南）中检索相关指南 $G$，再由 VLM 依据指南生成结构化的诊断步骤序列。每个步骤 $P_i$ 定义为一个动作-对象-结果三元组：

$$P_i: r_i = a_i(o_i), \quad a_i \in \mathcal{A}$$

其中 $o_i$ 为输入对象（如眼底图像、OCT 扫描），$a_i$ 为预定义动作集 $\mathcal{A}$ 中的操作（如分割、定位、定性评估），$r_i$ 为该步骤的输出结果。这一形式化定义将临床诊断流程转化为可执行的行动计划，确保每一步推理都有明确的临床依据。

### 患者级记忆初始化

诊断计划 $\mathcal{P}$ 是针对疾病的标准模板，而具体患者的可用数据 $\mathcal{D}$ 各不相同。患者级记忆初始化模块负责筛选可执行步骤，形成该患者的长期诊断记忆 $\mathcal{M}$：

$$\mathcal{M} = \{ P_i \in \mathcal{P} \mid o_i \in \mathcal{D} \}$$

该公式的含义是：仅当诊断计划中某步骤所需的输入对象 $o_i$ 在患者数据 $\mathcal{D}$ 中存在时，该步骤才被纳入记忆并进入后续执行队列。这一机制使得同一套疾病级计划能够灵活适配不同患者的数据完备性。

### 基于工具的动作执行

在患者级推理阶段，系统按照记忆 $\mathcal{M}$ 中的步骤顺序，调用专业视觉工具（如分割模型、定位模型）和编码工具执行定量或定性分析。对于需要精确测量的临床指标（如杯盘比、房角角度），工具输出数值型结果；对于依赖视觉判断的定性指标，则由 VLM 在指南引导下完成评估。

### 基于证据的反思

每一步动作执行后，系统通过零样本评估函数 $\phi$ 对中间结果的可靠性进行判断，并据此决定推理状态 $s_i$：

$$s_i = \begin{cases} Complete & r_i \in \mathbb{Z} \\ Terminate & r_i \notin \mathbb{Z} \land \neg \phi(r_i, o_i, G) \\ Continue & r_i \notin \mathbb{Z} \land \phi(r_i, o_i, G) \end{cases}$$

三种状态的含义如下：
- **Complete**：$r_i$ 为最终临床指标（数值型），该步骤直接完成；
- **Terminate**：$r_i$ 非最终指标且评估函数 $\phi$ 判定其不可靠，终止该步骤并将失败信息记录；
- **Continue**：$r_i$ 非最终指标但被判定为可靠，将其作为证据传递至后续步骤。

这一反思机制是 MedAgent-Pro 区别于端到端 VLM 的关键设计：它强制每一步推理都经过可靠性校验，不可靠的中间结果不会污染后续推理链。

### 基于风险的决策

当所有可执行步骤完成后，系统收集所有可靠的最终临床指标 $\mathcal{R}_{final}$，由 VLM 依据临床指南 $G$ 为每个指标赋予风险权重 $W$，计算加权风险分数 $\rho$：

$$\rho = \sum_{i=0}^{l} w_i r_i, \quad \text{s.t. } w_i \in W, r_i \in \mathcal{R}_{final}$$

最终诊断通过将 $\rho$ 与预设风险阈值 $\theta$ 比较得出。权重 $w_i$ 反映了各指标在特定疾病诊断中的临床重要性——例如青光眼诊断中杯盘比的权重可能高于视神经纤维层厚度的定性评估——这种基于指南的权重分配使得决策过程具备临床可解释性。

## 实验与分析

### 整体实验设置

MedAgent-Pro 以 GPT-4o（Achiam et al., 2023）作为默认骨干 VLM，RAG 代理基于 LangChain（Topsakal & Akinci, 2023）实现。知识库 $\mathcal{K}$ 构建自 MedlinePlus，涵盖 1000+ 种疾病及 4000+ 条经 NIH/NLM 认证的专家评审指南。实验覆盖四个基准数据集：REFUGE2（青光眼诊断）、MITEA（心脏病诊断）、NEJM（多模态临床病例）和 MIMIC（12 项胸部 X 光分类子任务）。评估指标包括平衡准确率（bAcc）、F1 分数、准确率（Acc）和 AUC。

### 主实验结果

#### 与通用 VLM 及医疗代理系统的对比

Table 1 展示了 MedAgent-Pro 在三个数据集上与通用 VLM 和现有医疗代理系统的全面对比。在 REFUGE2 青光眼诊断任务上，MedAgent-Pro 取得了 90.4% 的 bAcc 和 76.4% 的 F1，相比 GPT-4o 的 56.4% bAcc 和 21.1% F1 分别提升了 34.0 和 55.3 个百分点。在 MITEA 心脏病诊断任务上，bAcc 从 56.8% 提升至 77.8%（+21.0），F1 从 28.1% 提升至 72.3%（+44.2）。在 NEJM 多模态病例诊断上，MedAgent-Pro 以 81.7% 的准确率显著超越 GPT-4o（70.9%）及 MedAgents（Tang et al., ACL 2024）、MMedAgent（Li et al., EMNLP 2024）、MDAgent（Kim et al., NeurIPS 2024）等医疗代理系统。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_ZOuU0udyA4/figures/005_Table_1.jpg]]

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_ZOuU0udyA4/figures/006_Table_1.jpg]]
*Table 1: Comparison with general VLMs and medical agentic systems on REFUGE2, MITEA and NEJM (%). ”Opht.” is the short form of Ophthalmology. Our setting is highlighted in green . Table 2: Comparison with general VLMs on the MIMIC dataset (%). “Avg.” is the average performance across 12 sub-tasks. Only bAcc values are presented; F1 score can be found in Appendix A*

值得注意的是，Janus-Pro-7B、LLaVA-Med、BioMedClip 等专门面向医疗场景的 VLM 在青光眼和心脏病任务上的 F1 均未超过 30%，反映出端到端生成式方法在需要精确临床判断的任务上的根本性局限。

#### MIMIC 胸部 X 光多子任务诊断

Table 2 展示了在 MIMIC 数据集 12 个子任务上的 bAcc 对比。MedAgent-Pro 取得了 72.0% 的平均 bAcc，较 GPT-4o（58.3%）提升 13.7 个百分点。在 Cardiomegaly（心脏肥大）和 Edema（肺水肿）等关键指标上，MedAgent-Pro 分别达到 82.1% 和 77.3%，而 GPT-4o 仅为 64.4% 和 60.2%。InternVL2.5-8B 和 Qwen2.5-7B-VL 等开源 VLM 的平均 bAcc 在 50% 左右徘徊，进一步验证了仅依赖模型内部知识进行医学诊断的不可靠性。

#### 与特定任务模型的对比

Table 3 将 MedAgent-Pro 与三类专用模型进行对比：（1）REFUGE2 挑战获胜者 VUNO EYE TEAM 和 MIG，在青光眼任务上 MedAgent-Pro 的 AUC 达到 95.1%，超越二者（88.3% 和 87.6%）；（2）眼科专用 VLM RetiZero 和 VisionUnite，MedAgent-Pro 的 bAcc 为 90.4%，显著高于 RetiZero（50.8%）；（3）胸部 X 光专用 VLM Maira-2 和 CheXagent，MedAgent-Pro 的平均 bAcc 为 72.0%，同样优于二者。这表明，通过层次化工作流引入临床知识和定量分析工具，通用 VLM 的表现可以超越专门针对特定领域训练的模型。

### 消融实验

#### 核心组件消融

Table 4 系统性地消融了 MedAgent-Pro 的三个核心组件：疾病级规划（Planning）、工具动作（Tool-based Action）和证据反思（Evidence-based Reflection）。以 GPT-4o 直接推理为基线，仅加入规划模块后，青光眼 F1 即从 21.1% 跃升至 55.6%（+34.5），心脏病 F1 从 28.1% 升至 48.8%（+20.7），证实了临床指南驱动的标准化诊断计划对性能提升的核心作用。在此基础上引入工具动作，青光眼 bAcc 进一步提升至 83.0%，F1 达到 66.7%。最终加入证据反思后，系统达到最佳性能（青光眼 bAcc 90.4%，F1 76.4%；心脏病 bAcc 77.8%，F1 72.3%）。三个组件各自提供显著增益，且三者协同配合才能达到最优效果。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_ZOuU0udyA4/figures/008_Table_4.jpg]]

#### 定性分析模块消融

Table 5 探索了将通用 VLM（GPT-4o）替换为眼科专用模型 VisionUnite 进行定性指标分析的效果。结果显示，VisionUnite 仅带来微弱提升（bAcc 从 90.4% 升至 92.9%，F1 从 76.4% 升至 79.1%），表明在临床指南的引导下，通用 VLM 已经能够胜任定性评估任务，专用模型的边际收益有限。

#### 工具提供方式的影响

Table 6 的关键发现是：即使直接向 GPT-4o、Janus-Pro-7B 等基线 VLM 提供全部视觉工具（分割模型、定位模型等），这些模型也无法有效组织推理链来利用工具，性能几乎没有提升。这直接证明了性能提升的根本原因在于 MedAgent-Pro 的层次化工作流设计，而非工具本身。

#### 分割精度对诊断的影响

Figure 5 展示了定量分析模块中分割精度与最终诊断性能之间的关系。实验表明，随着分割模型精度的提高，青光眼和心脏病的诊断 bAcc 和 F1 均呈现单调上升趋势，直接证实了精确的定量分析对可靠诊断的支撑作用。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_ZOuU0udyA4/figures/010_Figure_5.jpg]]
*Figure 5: Ablation on quantitative indicator analysis that reveals how segmentation accuracy influences diagnostic outcomes*

### 鲁棒性分析

在缺少可用视觉工具的 NEJM 病例子集上（Table 18），MedAgent-Pro 依然取得了最优性能。这表明即使无法执行定量分析，其基于指南的标准化推理结构和证据反思机制本身仍具备显著的鲁棒性，不会因为工具缺失而完全失效。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_ZOuU0udyA4/figures/026_Table_18.jpg]]
*Table 18: Comparison of methods on the NEJM cases where no suitable visual tools are available. As shown in the table, our method still achieves the best performance, highlighting that the reasoning structure of MedAgent-Pro is capable of leveraging tool outputs when available, and maintaining strong performance even when tool access is limited due to the system’s planning capability and integration of retrieved knowledge*

### 失败模式与局限性

尽管 MedAgent-Pro 在多个基准上取得了显著提升，实验和分析也揭示了以下局限：

1. **视觉工具依赖**：当前框架对专业分割模型的依赖较强，当遇到缺少适配工具的影像类型时，定量分析模块无法发挥作用，诊断能力受限。
2. **VLM 幻觉风险**：定性分析部分仍由 VLM 执行，存在模型幻觉的可能性，可能影响中间证据的可靠性并进而干扰最终判断。
3. **知识库覆盖范围**：疾病级规划依赖于预先构建的 MedlinePlus 知识库，对罕见疾病或最新临床指南的覆盖能力尚未在实验中充分验证。
4. **推理效率**：层次化推理虽然提升了可靠性，但相较于单步 VLM 推理，多轮代理交互和工具调用显著增加了计算耗时。

## 方法谱系与知识库定位

### 诊断范式的演进：从端到端VLM到层次化代理工作流

当前多模态医学诊断的主流范式可分为三条技术路线：通用视觉语言模型（VLMs）、医疗专用VLMs，以及近期兴起的医疗代理系统。MedAgent-Pro 的定位是在第三条路线中引入**临床指南驱动的标准化诊断工作流**，从而弥合代理系统与循证医学实践之间的鸿沟。

**通用VLMs**（如 **GPT-4o** (Achiam et al., 2023)、**Janus-Pro-7B** (Chen et al., 2025a)、**Qwen2.5-7B-VL** (Wang et al., 2024b)、**InternVL2.5-8B** (Chen et al., 2024a)）虽然具备广泛的视觉理解能力，但在医学诊断场景中面临两个核心瓶颈：其一，诊断过程完全依赖模型内部知识，缺乏可追溯的临床证据支撑；其二，仅能进行定性判断，无法执行杯盘比、心影比等临床常规定量指标的精确计算。在 REFUGE2 青光眼诊断任务上，GPT-4o 的 bAcc 仅为 56.4%，F1 仅为 21.1%（Table 1），反映了端到端范式的根本性局限。

**医疗专用VLMs**试图通过领域适配来缓解上述问题。**LLaVA-Med** (Li et al., 2024b) 和 **BioMedClip** (Zhang et al., 2023a) 通过医学图文数据微调来增强领域知识；眼科领域则有 **RetiZero**、**VisionUnite** (Li et al., 2024c) 等专用模型；胸部X光领域有 **Maira-2** 和 **CheXagent** (Chen et al., 2024b)。然而，这些模型本质上仍是端到端的黑箱推理，并未改变“直接输出结论”的底层逻辑。Table 3 显示，即使是最优的眼科专用 VLM VisionUnite，在青光眼 F1 上也仅为 85.8%，仍显著低于 MedAgent-Pro 的 76.4%（注：原文如此，需要核实 VisionUnite 的 F1 是否确实高于 MedAgent-Pro——经核实 Table 3 中 VisionUnite 的 F1 为 85.8%，但 MedAgent-Pro 的 F1 为 76.4%，此处的“显著低于”存在歧义，实际是 MedAgent-Pro 在 bAcc 上以 90.4% 优于 VisionUnite 的 85.8%）。

**医疗代理系统**代表了更接近临床实践的尝试。**MedAgents** (Tang et al., ACL 2024) 采用多代理协作策略，**MMedAgent** (Li et al., EMNLP 2024) 和 **MDAgent** (Kim et al., NeurIPS 2024) 则引入了工具调用的能力。但这些系统仍存在关键缺陷：它们往往直接输出基于经验的结论，缺乏由定量分析支撑的临床证据，并且未遵循标准化的诊断工作流。Table 1 的数据印证了这一点——MedAgents 在青光眼 bAcc 上仅为 50.0%（甚至低于 GPT-4o 的 56.4%），说明单纯的代理协作并不足以解决医学诊断的可靠性问题。

### MedAgent-Pro 的核心差异化设计

MedAgent-Pro 的关键创新在于将诊断过程**解耦为两个层次**（Section 3.1），这一设计直接对应了现代临床诊断的实践逻辑：

1. **疾病级标准化规划**：通过 RAG 代理从 MedlinePlus 知识库（覆盖 1,000+ 疾病、4,000+ 专家审校指南，经 NIH/NLM 认证）检索临床指南，生成结构化的诊断计划 $P_i: r_i = a_i(o_i), a_i \in \mathcal{A}$（Section 3.2）。这一步确保每个疾病的诊断路径都符合临床标准，而非依赖模型的自由发挥。

2. **患者级个性化推理**：根据患者实际拥有的数据 $\mathcal{D}$ 筛选可执行的计划步骤，形成患者记忆 $\mathcal{M} = \{ P_i \in \mathcal{P} \mid o_i \in \mathcal{D} \}$（Section 3.3, Eq. 2），随后逐步调用专业工具执行定量分析，并通过基于证据的反思机制 $s_i$ 动态评估中间结果的可靠性（Section 3.3, Eq. 3），最终以加权风险分数 $\rho = \sum_{i=0}^{l} w_i r_i$ 做出诊断决策（Section 3.3, Eq. 4）。

与现有代理系统相比，MedAgent-Pro 的四个关键差异化槽位（changed slots）如下：

| 设计维度 | 基线方案 | MedAgent-Pro 方案 |
|---------|---------|------------------|
| 诊断范式 | 端到端 VLM 直接生成诊断答案 | 层次化代理工作流：疾病级指南规划 + 患者级证据推理 |
| 临床知识集成 | 依赖 VLM 内部知识 | RAG 代理动态检索医学指南并注入规划过程 |
| 定量分析 | 仅由 VLM 进行定性判断 | 集成专业视觉分割/定位模型并配合编码工具进行精确指标计算 |
| 错误纠正与推理一致性 | 无 | 基于证据的反思机制：评估每步可靠性，动态调整记忆并决定推理状态 |

### 与任务专用模型的边界关系

在 REFUGE2 挑战的获胜方法中，**VUNO EYE TEAM** 和 **MIG** 等方案针对青光眼诊断进行了深度优化，但它们的适用边界严格限定在特定疾病和特定成像模态。MedAgent-Pro 则以通用 VLM（GPT-4o）为基座，通过工作流设计而非模型微调来跨疾病泛化——Table 1 和 Table 2 显示，同一套框架在青光眼（bAcc 90.4%）、心脏病（bAcc 77.8%）、NEJM 多模态病例（Acc 81.7%）和 MIMIC 胸片 12 项子任务（Avg bAcc 72.0%）上均取得最优或接近最优的结果。

值得注意的是，Table 5 的消融实验揭示了一个反直觉的发现：用眼科专用模型 VisionUnite 替代 GPT-4o 进行定性分析仅带来微弱提升（bAcc 从 90.4% 到 92.9%），这表明在临床指南的引导下，通用 VLM 已能胜任定性评估任务，**工作流设计而非模型能力才是性能提升的主因**。Table 6 进一步强化了这一论点：即使直接向基线 VLMs 提供全部工具，它们也无法有效组织推理链，性能远不及具备规划能力的完整系统。

### 适用边界与已知局限

MedAgent-Pro 的有效性建立在以下前提之上，这些前提同时也划定了其适用边界：

1. **对专业视觉工具的依赖**：框架的性能与可用的视觉分割/定位模型强绑定。Figure 5 的消融实验证实分割精度越高，最终诊断性能越好。当遇到缺少适配工具的影像类型时（如部分 NEJM 病例），诊断能力会受到限制。Table 18 显示在无可用视觉工具的 NEJM 子集上 MedAgent-Pro 仍表现最优，但这更多证明了推理结构本身的鲁棒性，而非定量分析的优势。

2. **知识库的覆盖范围**：疾病级规划依赖于预先构建的 MedlinePlus 知识库，其对罕见疾病或最新临床指南的覆盖能力尚未充分验证。当前框架缺乏自动扩展诊断计划以覆盖新疾病和成像模态的机制。

3. **VLM 幻觉的残余风险**：定性分析部分仍由 VLM 执行，尽管有指南约束和证据反思，模型幻觉仍可能影响最终判断的可靠性。证据反思模块目前采用零样本评估函数，其可靠性评估能力可能通过微调得到进一步提升。

4. **计算效率的权衡**：层次化推理虽然提升了可靠性，但相较于单步 VLM 推理增加了计算耗时。论文未提供详细的推理延迟数据，这一工程性局限在实际部署中需要关注。

### 开放问题

从 MedAgent-Pro 的设计逻辑向外推演，以下问题构成了该方向的自然延伸：

- **自适应工具发现**：当前框架依赖人工定义的工具和动作集合 $\mathcal{A}$。能否实现自适应工具发现与调用，使系统在面对新模态时自动寻找或生成适配的分析工具？
- **知识库的自动扩展**：如何自动构建和扩展诊断计划，以覆盖更多疾病和成像模态，而非依赖静态的 MedlinePlus 快照？
- **隐私保护下的反馈优化**：如何在保护患者隐私的前提下利用真实临床数据进行反馈优化，使证据反思模块和风险权重分配从经验中学习？
- **反思能力的增强**：证据反思模块是否可以通过微调获得更准确的可靠性评估能力，而非依赖零样本提示的启发式判断？

## 原文 PDF

![[paperPDFs/ICLR_2026/MedAgent_Pro_Towards_Evidence_based_Multi_modal_Medical_Diagnosis_via_Reasoning_Agentic_Workflow.pdf]]
