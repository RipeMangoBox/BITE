---
title: "DoVer: Intervention-Driven Auto Debugging for LLM Multi-Agent Systems"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DoVer_Intervention_Driven_Auto_Debugging_for_LLM_Multi_Agent_Systems.pdf
project_link: https://aka.ms/DoVer
code_link: null
openreview_forum_id: mrEK16Jy6h
aliases:
- DoVer
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "在假设的失败点施加针对性干预（编辑消息、修改计划），并重执行以验证归因假设——通过主动“操作-验证”闭环替代被动日志分析，直接以任务成功或里程碑进展衡量修复效果。"
primary_logic: "将调试从不可靠的静态归因转向可检验的动态干预，以结果为导向评估修复，从而绕开标注歧义，同时支持多干预并行验证，使多智能体系统的故障修复变得更加可靠和可量化。"
claims:
- "WW数据集的重现实验表明，即使加入步骤索引和标注指南提示，GPT-4o在不确定案例上的步骤归因准确率仍仅为24%，而确定案例可达44%，验证了真实标签不确定性严重影响归因可靠性。"
- "DoVer在Magnetic‑One框架下，对AssistantBench (WW‑AB) 和 GAIA (WW‑GAIA) 的失败案例分别实现了18%和28%的翻转率，最高里程碑进展达16%。"
- "DoVer在WW‑GAIA和GAIA‑Level‑1上分别验证了16.2%和34.9%的失败假设，同时驳斥了21.2%和23.8%的假设，证明干预能够有效地确认或推翻归因诊断。"
- "在AG2 (AutoGen2) 框架和GSMPlus数据集上，DoVer更达到了49%的试验成功率，表明其泛化能力。"
---

# DoVer: Intervention-Driven Auto Debugging for LLM Multi-Agent Systems

> [!tip] 核心洞察
> 将调试从不可靠的静态归因转向可检验的动态干预，以结果为导向评估修复，从而绕开标注歧义，同时支持多干预并行验证，使多智能体系统的故障修复变得更加可靠和可量化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DoVer：面向LLM多智能体系统的干预驱动自动调试 |
| 英文题名 | DoVer: Intervention-Driven Auto Debugging for LLM Multi-Agent Systems |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=mrEK16Jy6h) · [Project](https://aka.ms/DoVer) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | DoVer |
| Dataset | WW-AB (AssistantBench, Magentic-One), WW-GAIA (GAIA, GAIA-Level-1 (Magentic-One) |

> [!tip] 效果简介
> - WW-AB (AssistantBench, Magentic-One) 上，Trial Success Rate 为 17.6%，对比 0% (no intervention)，变化 +17.6个百分点。
> - WW-GAIA (GAIA, Magentic-One) 上，Trial Success Rate 为 17.6%，对比 0% (no intervention)，变化 +17.6个百分点。
> - GAIA-Level-1 (Magentic-One) 上，Trial Success Rate 为 27.5%，对比 0% (no intervention)，变化 +27.5个百分点。

## 概要

基于日志的LLM多智能体系统失败归因存在根本性瓶颈：归因假设缺乏执行验证，且多轮尝试、多智能体交互导致单步/单智能体标注高度不确定——在WW GAIA数据集的29个案例中，有14个存在真实标签不确定性，使得即使经过提示精调，GPT-4o的步骤归因准确率仍仅为20–24%，难以实用。

**DoVer** 提出了一种干预驱动的主动调试范式，将调试从不可靠的静态归因转向可检验的动态干预。其核心思路是：在假设的失败点施加针对性干预（编辑消息、修改计划），并重执行以验证归因假设，直接以任务成功或里程碑进展作为硬性验证信号，从而绕开标注歧义，同时支持多干预并行验证。

在 **Magentic-One** 框架下，DoVer 对 AssistantBench (WW‑AB) 和 GAIA (WW‑GAIA) 的失败案例分别实现了 **18%** 和 **28%** 的翻转率，最高里程碑进展达 **16%**；在 **AG2 (AutoGen2)** 框架和 GSMPlus 数据集上，试验成功率更达到 **49%**，展现出跨框架、跨任务的泛化能力。此外，DoVer 在 WW‑GAIA 和 GAIA‑Level‑1 上分别验证了 **16.2%** 和 **34.9%** 的失败假设，同时驳斥了 **21.2%** 和 **23.8%** 的假设，证明干预能够有效确认或推翻归因诊断。

DoVer 的方法定位介于纯日志分析与全自动修复之间：它不修改子智能体内部能力，而是通过编排器层的干预生成与执行验证，形成“假设→干预→重执行→评估”的闭环。这使其在方法谱系中区别于基于日志的单次归因方法（如 Zhang et al., WW, 2025c 的 All‑at‑Once），同时为更大调试循环中的子智能体能力改进提供了定位依据。



### 多智能体系统的调试困境

基于大语言模型（LLM）的多智能体系统在复杂任务上展现出强大能力，但其失败调试仍面临根本性挑战。当系统未能完成任务时，开发者需要从冗长的会话日志中定位失败原因——是编排器的规划偏差，还是某个子智能体的执行失误？这一归因过程的可靠性直接决定了后续修复的有效性。

### 日志归因的结构性缺陷

现有方法依赖对失败会话日志的静态分析，试图通过单次LLM调用直接输出失败步骤或智能体的标注。然而，这种"全量一次性"（All-at-Once）归因范式存在两个结构性缺陷：

**标注不确定性问题。** 多智能体系统的失败往往涉及多轮尝试（trial）和跨智能体的交互失配。以WW-HC数据集的Case 3为例（Figure 1），一次会话包含四个独立的trial，每个trial采用不同策略（如直接滚动 vs. 日历导航），在不同步骤上遭遇不同类型的错误。在Trial 2中，编排器发出了无效指令，而WebSurfer智能体又执行了无关操作，形成了跨智能体的责任模糊。在这种情况下，将失败归因于单一智能体的单一步骤，本质上是一种高度不确定的简化。

对WW数据集中29个GAIA案例的重新审查证实了这一点：其中14个案例存在真实标签（ground-truth）不确定性，标注者自身对失败步骤的认定即存在歧义（Table 6, Table 7）。

**归因准确率难以实用。** 即使通过提示工程进行精调——添加显式步骤索引、嵌入标注者指南提醒（Figure 3）——日志归因的准确率仍然很低。在WW-GAIA的不确定案例上，GPT-4o的步骤归因准确率仅为24%，GPT-5更是降至7%；即使在确定性较高的案例上，GPT-4o也仅达到44%（Section 3, Table 5）。这意味着，在最具挑战性的场景中，超过四分之三的归因结果是不可靠的。

### 核心洞见：从静态归因到动态验证

上述困境的根源在于：日志归因将"生成假设"等同于"完成调试"，缺乏对假设正确性的验证机制。DoVer的核心洞见是**将调试从不可靠的静态归因转向可检验的动态干预**——在假设的失败点施加针对性干预（编辑消息、修改计划），然后重执行系统以验证假设是否成立。通过以任务成功或里程碑进展作为硬性验证信号，DoVer绕开了标注歧义问题，同时支持多干预并行验证，使多智能体系统的故障修复变得更加可靠和可量化。



## 核心方法与创新机理

DoVer的核心创新在于将LLM多智能体系统的调试范式从**被动日志归因**转向**主动干预验证**。现有方法（如WW提出的All-at-Once归因）仅基于会话日志生成失败假设，却缺乏验证环节——论文通过重现实验揭示，即使在提示精调后，GPT-4o在标注不确定案例上的步骤归因准确率也仅为24%，而确定案例也仅达44%（Section 3）。这种归因不可靠性的根源在于多轮尝试（trial）和多智能体交互带来的标注歧义：WW数据集中14/29个GAIA案例存在真实标签不确定性（Table 6, Table 7）。

DoVer通过三个关键机制突破上述瓶颈：

**1. 干预驱动的“假设-验证”闭环**
DoVer将失败归因视为可检验的假设，而非最终诊断。框架在可疑失败点施加针对性干预——编辑子智能体消息或修改编排器计划——并重执行系统行为，以任务成功或里程碑进展作为硬性验证信号（Section 4.1）。这一“操作-验证”范式使归因正确性不再依赖不可靠的人工标注或LLM推理，而是通过反事实轨迹的结果直接评判。

**2. 多假设并行验证的试验段粒度**
不同于传统方法将整个会话视为单次归因对象，DoVer按重新规划（re-plan）步骤将失败轨迹切分为多个试验段（trial），并对每个trial独立生成归因假设和干预（Figure 2）。这种设计天然适配多智能体系统“多次尝试、动态调整”的执行特性，支持对多个潜在失败点并行验证，有效解决了跨trial和跨智能体的责任归属模糊问题。

**3. 以结果为导向的假设分类**
DoVer不仅验证假设，还通过里程碑进展（Progress Made）将干预效果量化为连续指标：

$$Prog(\tau, \tilde{\tau}_I) = \frac{A(\tilde{\tau}_I) - A(\tau)}{K} \in [-1, 1]$$

并据此将假设分类为Validated、Refuted、Partially Validated或Inconclusive（Section 4.2）。实验表明，在WW-GAIA上16.2%的假设被验证，21.2%被驳斥（Table 3），证明干预能够有效确认或推翻归因诊断——这是纯日志分析方法无法实现的。

综上，DoVer的本质创新在于**用可执行的干预替代不可靠的静态推断**，将调试从“猜测哪里出错”转变为“测试修复是否有效”，使多智能体系统的故障定位和修复变得可量化、可验证。



![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_mrEK16Jy6h/figures/002_Figure_2.jpg]]
*Figure 2: DoVer (Do–then–Verify) Debugging Pipeline. (1) Trial segmentation: split the failed session log into trials using re-plan steps as cut points. (2) Failure attribution: for each trial, propose a hypothesis h _ { i } that marks a faulty step or agent. (3) Intervention generation: turn h _ { i } into an actionable intervention that edits either the plan or the attributed message or step in the original log. (4) Intervention execution: replay the trajectory in place, i.e., preserve all steps before the intervened step, then execute the intervention and measure progress of the new log. Colors indicate plan/re-plan (blue), execution (green), attributed failure (red), terminal failure (dark red),...*

DoVer 将调试从基于日志的被动归因转变为**干预驱动的主动验证闭环**。其核心流程由四个串行模块构成，如图 2 所示：

1.  **Trial Segmentation（试验段分割）**：以编排器（Orchestrator）的重新规划（re-plan）步骤为切分点，将完整的失败会话日志 $\boldsymbol{\tau} = \{ ( a_t, m_t, \sigma_t ) \}_{t=1}^{T}$ 拆分为多个独立的试验段（trial）$\tau^i$。这一操作缩短了上下文窗口，并为后续并行干预创造了条件。
2.  **Failure Attribution（失败归因/假设生成）**：对每个试验段 $\tau^i$，生成一个候选失败归因假设 $h_i = ( \hat{a}_{\hat{t}}^i, r_{\hat{t}}^i )$，明确指定可疑的步骤索引 $\hat{t}$、可疑智能体 $\hat{a}^i$ 以及自然语言理由 $r^i$。
3.  **Intervention Generation（干预生成）**：将归因假设 $h_i$ 转化为可执行的干预操作 $I_i$。干预类型主要包括两类：**消息/指令编辑**（修改对子智能体的指令或补充缺失上下文）和**计划更新**（修订编排器的高层计划，如重排序或替换步骤）。
4.  **Intervention Execution & Evaluation（干预执行与评估）**：在原始轨迹的干预点处**原位重放**系统行为——保留干预步骤之前的所有上下文，执行干预 $I_i$，生成反事实轨迹 $\tilde{\tau}_I$。随后以任务成功（Trial Success Rate）和里程碑进展（Progress Made）作为硬性验证信号，对假设进行分类：**Validated**（假设确认，干预后成功）、**Refuted**（假设驳斥，干预未改善）、**Partially Validated**（部分验证，有进展但未完全成功）或 **Inconclusive**（无结论，智能体未忠实执行干预）。

这一管道的设计本质在于：**以结果为导向的可检验干预，替代了不可靠的静态归因**。通过“生成假设→施加干预→重执行→验证”的闭环，DoVer 绕开了多智能体交互中固有的标注歧义，使故障修复变得可量化和可操作。



### 4.1 失败会话的形式化表示

DoVer 将一次多智能体系统的完整执行记录建模为结构化会话日志：

$$\boldsymbol{\tau} = \{ ( a_t, m_t, \sigma_t ) \}_{t=1}^{T}$$

其中 $a_t$ 为第 $t$ 步的活跃智能体，$m_t$ 为该步产生的消息，$\sigma_t$ 为状态信息（用于轨迹恢复与重放）。$T$ 为会话总步数。

### 4.2 四阶段调试管道

DoVer 的核心调试流程由四个串行模块构成（Figure 2）：

**（1）试验段分割（Trial Segmentation）**

将完整失败日志 $\boldsymbol{\tau}$ 按重新规划（re-plan）步骤切分为多个试验段 $\boldsymbol{\tau}^i$。其设计动机在于：多智能体系统在一次会话中常经历多次策略调整（Figure 1 展示了含四个 trial 的典型案例），单步归因跨越不同规划阶段会产生严重的标注歧义。通过以 re-plan 为切分点，每个 trial 对应一个独立的“规划-执行”周期，从而缩短上下文并支持并行干预。

**（2）失败归因（Failure Attribution / Hypothesis Generation）**

对每个试验段 $\boldsymbol{\tau}^i$ 生成候选失败归因假设：

$$h_i = ( \hat{a}_{\hat{t}}^i, r_{\hat{t}}^i )$$

其中 $\hat{t}$ 为被归因的失败步骤索引，$i$ 为试验段索引，$\hat{a}^i$ 为被怀疑的智能体，$r^i$ 为自然语言形式的归因理由。该模块将归因视为待验证的**假设**而非最终结论，从而从根本上改变了调试范式——不再追求单次推理的准确性，而是为后续验证提供可操作的起点。

**（3）干预生成（Intervention Generation）**

将归因假设 $h_i$ 转化为可执行的干预操作 $I_i$，主要包括两类干预形式：
- **消息编辑**：修改对子智能体的指令，间接影响其行为（如补充缺失的上下文信息）；
- **计划更新**：修订编排器（Orchestrator）的高层计划，如重排、分解或替换步骤，以绕过已识别的故障点。

干预设计遵循“最小化”原则——仅修改归因步骤处的消息或计划，保留所有前置上下文不变。

**（4）干预执行与评估（Intervention Execution & Evaluation）**

在原始轨迹的干预点 $\hat{t}$ 处原地重放系统行为：保留 $\hat{t}$ 之前的所有步骤，在 $\hat{t}$ 处施加干预 $I_i$，随后让多智能体系统从该点继续执行，生成反事实轨迹 $\tilde{\boldsymbol{\tau}}_I$。

### 4.3 评估指标的形式化定义

DoVer 采用两类硬性验证信号评估干预效果，避免依赖不可靠的归因标注。

**里程碑达成计数**：首先从任务描述中提取 $K$ 个人工标注的关键里程碑 $\{\mathbf{m}^k\}_{k=1}^{K}$（$K \leq 5$），然后统计轨迹 $\gamma$ 中达成的里程碑数量：

$$A(\gamma) = \sum_{k=1}^{K} \mathbb{I}\big[ \text{milestone } \mathbf{m}^k \text{ is achieved in } \gamma \big]$$

**进展度量（Progress Made）**：衡量干预后轨迹 $\tilde{\boldsymbol{\tau}}_I$ 相对于原始轨迹 $\boldsymbol{\tau}$ 的额外里程碑比例：

$$Prog(\tau, \tilde{\tau}_I) = \frac{A(\tilde{\tau}_I) - A(\tau)}{K} \in [-1, 1]$$

正值表示进展，负值表示倒退。该指标将调试效果量化为任务完成度的增量，绕开了对归因正确性的直接判断。

**假设验证分类**：基于干预执行结果，将每个 trial 的归因假设分为四类：
- **Validated**：干预后任务成功完成，假设被证实；
- **Refuted**：干预后无进展或倒退，假设被推翻；
- **Partially Validated**：干预后取得部分里程碑进展但未完全成功；
- **Inconclusive**：智能体未能忠实执行干预指令，无法得出结论。

### 4.4 关键设计决策

DoVer 的管道设计体现了三个核心决策：

1. **以 trial 而非 session 为调试单元**：切分后的 trial 上下文更短，归因歧义更低，且支持多 trial 并行干预，提升调试吞吐量。

2. **以执行结果而非推理一致性为验证准则**：不依赖 LLM 判断归因是否正确，而是通过实际重执行后的任务成功或里程碑进展来硬性验证——这从根本上绕开了 Section 3 揭示的归因准确率仅 20-24% 的瓶颈。

3. **干预仅限于编排器层**：当前 DoVer 仅修改消息或计划，不触及子智能体的内部工具或代码。这一约束简化了干预生成，但也导致 30-67% 的案例因子智能体执行能力不足而陷入 Inconclusive 状态（详见 Section 5.2 和 Appendix E 的消融分析）。



## 实验与关键发现

### 3.1 实验设置与评估指标

DoVer 的实验覆盖两个多智能体框架（Magentic-One 和 AG2/AutoGen2）及四个数据集：WW‑AB（AssistantBench）、WW‑GAIA（GAIA）、GAIA‑Level‑1 和 GSMPlus。各数据集的失败案例与干预规模如 Table 1 所示——WW 系列数据集的平均试验段数约为 3，而 GSMPlus 虽失败案例最多（214 例），但平均每例仅 1.4 个试验段，反映其任务结构相对线性。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_mrEK16Jy6h/figures/003_Table_1.jpg]]
*Table 1: Summary of failed and intervened cases across datasets, showing the total number of cases, failed cases, intervened cases, total intervened trials, and the average number of trials per case*

所有干预实验独立重复 3 次以缓解 LLM 随机性。评估围绕三个核心指标展开：

- **试验成功率（Trial Success Rate）**：干预后试验段完整完成任务的比例。基线为无干预的原始轨迹（成功率 0%）。
- **进展度量（Progress Made）**：定义为 $\text{Prog}(\tau, \tilde{\tau}_I) = \frac{A(\tilde{\tau}_I) - A(\tau)}{K}$，其中 $A(\gamma) = \sum_{k=1}^{K} \mathbb{I}[\text{milestone } \mathbf{m}^k \text{ is achieved in } \gamma]$，$K \leq 5$ 为人工标注的里程碑数。正值表示干预使任务更接近完成，负值表示倒退。
- **假设验证分类**：将每个试验段的干预结果归为四类——**已验证（Validated）**（干预后任务成功）、**部分验证（Partially Validated）**（进展为正但未完全成功）、**已驳斥（Refuted）**（进展无改善或倒退）、**无结论（Inconclusive）**（Agent 未能忠实执行干预指令）。

进展度量依赖 LLM 从人工标注步骤中提取里程碑并评判达成情况。论文使用 GPT‑5 进行评估以降低自评偏差，但部分环节仍使用 GPT‑4o，可能引入评估噪声。

### 3.2 主结果：失败翻转与进展提升

Table 2 汇总了各设置下的核心结果。在 Magentic-One 框架下，DoVer 在 WW‑AB 和 WW‑GAIA 上均实现了 **17.6%** 的试验成功率，而基线（无干预）为 0%。在 GAIA‑Level‑1 子集上，试验成功率进一步提升至 **27.5%**，平均进展达到 **+15.7%**——这是所有设置中进展最大的，表明对于相对简单的任务，干预驱动的修复更加有效。WW‑GAIA 的平均进展为 +8.8%。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_mrEK16Jy6h/figures/004_Table_2.jpg]]
*Table 2: Experimental results on failure-flipping metrics across settings. The table reports the number of Intervened Trials, the Trial Success Rate, and the average Progress Made*

在 AG2 框架和 GSMPlus 数据集上，DoVer 的表现更为突出：试验成功率高达 **49.0%**，远高于 Magentic-One 设置下的结果。这一差异可能源于 GSMPlus 任务的数学推理特性——失败往往集中在单步推理错误或计划偏差上，干预的可操作性更强；而 GAIA 的失败更多根植于子智能体执行能力不足（如无法滚动页面、PDF 解析失败），编排器层干预难以直接修复。

### 3.3 假设验证：确认与驳斥的双重价值

Table 3 展示了失败假设的验证结果分类。DoVer 不仅能够验证正确的归因假设，还能**驳斥错误假设**——这一能力在纯被动归因范式中完全缺失。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_mrEK16Jy6h/figures/005_Table_3.jpg]]
*Table 3: Validation outcomes of failure hypotheses across datasets. The table reports the number and percentage of trials classified as Validated, Inconclusive, Partially Validated, or Refuted*

- 在 WW‑GAIA 上，**16.2%** 的假设被验证，**21.2%** 被驳斥，合计 **37.4%** 的假设获得了明确结论。
- 在 GAIA‑Level‑1 上，验证率升至 **34.9%**，驳斥率为 **23.8%**，合计 **58.7%** 的假设得到明确判定。
- WW‑AB 的验证率最低（**9.3%**），但驳斥率最高（**33.3%**），表明 AssistantBench 的失败归因尤其困难，但 DoVer 仍能有效排除错误假设。

值得注意的是，**30–67%** 的试验段落入“无结论”类别。深入分析表明，这些案例的失败根源在于子智能体**执行能力不足**（如缺少滚动工具、PDF 解析能力缺失），而非编排器层的指令或计划错误。DoVer 的干预目前仅限于编排器层，无法修改子智能体内部能力，构成了当前框架的主要瓶颈。

### 3.4 消融实验：模型敏感性与少样本提示

Table 4 的消融实验在 WW‑GAIA 设置下考察了不同调试模型和少样本提示的影响：

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_mrEK16Jy6h/figures/006_Table_4.jpg]]
*Table 4: Ablation of DoVer models and few-shot prompting in the WW-GAIA setting*

- 将调试模型从 GPT‑4o 替换为 **Qwen3‑32B**，试验成功率仅从 17.6% 微降至 **16.9%**，表明 DoVer 框架对底层模型不敏感，具有较强的模型鲁棒性。
- 对于较弱的 **Qwen3‑8B**，0‑shot 设置下成功率仅为 11.3%，但**3‑shot 提示将其提升至 14.3%**，展示了少样本示例对弱模型调试效果的正面影响。
- 进一步增加至 5‑shot 未带来额外增益，提示示例数量的边际效益在 3 左右趋于饱和。

### 3.5 失败模式与能力瓶颈

通过对无结论案例的深入分析，论文识别出两类主要失败模式：

1. **子智能体能力缺失**：在 WW‑GAIA 的多个案例中，WebSurfer 智能体无法执行滚动操作或处理 PDF 文件，导致即使编排器给出了正确指令，任务仍无法完成。附录 E 报告了一个关键发现：对原本无结论的 3 个案例（Case 20, 21, 26）进行子智能体工具增强（添加滚动到底部和 PDF 处理能力）后，**仅凭编排器级干预即可解决**。这证明 DoVer 能够定位子智能体瓶颈并指导针对性改进，但目前尚无法自动触发此类修复。

2. **Agent 不忠实执行干预**：部分干预指令未被 Agent 忠实执行，导致无法得出明确结论。这种执行不确定性削弱了假设验证的可信度，尤其是在需要多步协调的复杂干预场景中。

### 3.6 归因准确率复现：标注不确定性的量化证据

论文在 WW 数据集上复现了基于日志的 All‑at‑Once 归因方法（Table 5）。在加入显式步骤索引和标注者指南提醒两项提示精调后，GPT‑4o 在 WW‑HC 上的步骤归因准确率从 6% 提升至 24%，但仍远低于实用水平。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_mrEK16Jy6h/figures/007_Table_5.jpg]]
*Table 5: Reproduced evaluation results on the WW dataset using the All-at-Once method with the ground-truth annotation. Results are reported for both Hand-Crafted and Algorithm-Generated scenarios at agent-level and step-level accuracy. Rows show baseline results from WW, our reproduction with GPT-4o, and refinements with explicit step indices and guidance reminders, as well as the latest GPT-5 model*

更关键的是，通过对 29 个 WW GAIA 案例的标注不确定性分析（Table 7），论文发现 **14 个案例存在真实标签不确定性**——即人工标注者本身对失败步骤的归属存在歧义。在这 14 个不确定案例上，GPT‑4o 的平均步骤归因准确率仅为 **24%**，GPT‑5 更是低至 **7%**。而在 15 个确定案例上，GPT‑4o 和 GPT‑5 的准确率分别达到 **44%** 和 **53%**。这一对比直接验证了核心论断：**真实标签不确定性严重影响归因可靠性**，基于日志的被动归因在此类多轮尝试、多智能体交互场景中存在根本性缺陷。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_mrEK16Jy6h/figures/010_Table_7.jpg]]

### 补充图表

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_mrEK16Jy6h/figures/001_Figure_1.jpg]]
*Figure 1: Failure trace of Case 3 in WW-HC, illustrating ambiguity in failure attribution. The session consists of four distinct trials, each initiated by a plan update and executed via a ReAct-style Yao et al. (2023) loop. Different strategies (e.g., direct scrolling in Trial 1 vs. calendar navigation in Trial 2) yield separate error points, making single-step attribution across the session inherently ambiguous. Trial 2 (Steps 53–55) further shows inter-agent misalignment: the Orchestrator issued an invalid instruction, while the WebSurfer compounded the error by executing an unrelated action*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_mrEK16Jy6h/figures/009_Table_6.jpg]]
*Table 6: Detailed annotation notes for each GAIA case in WW. The table records trial-level observations, potential errors, ambiguous attributions, and API issues associated with the ground-truth labels*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_mrEK16Jy6h/figures/011_Table_8.jpg]]
*Table 8: Continued from previous page*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_mrEK16Jy6h/figures/012_Table_7.jpg]]
*Table 7: Tagging results for each GAIA case in WW. The table reports ground-truth annotations, uncertainty tags, possibility for multi-failure step attribution, presence of ambiguous attributions, potential API or flaky errors, and case-specific details such as number of trials and model outputs. Model predictions matching , d-truth failure step are highlighted i*



## 定位与知识库关联

### 1. 与基线方法的关系

#### 1.1 基于日志的被动归因：All‑at‑Once 范式

DoVer 的直接对比对象是基于日志的失败归因方法，即 **All‑at‑Once** 范式（Zhang et al., WW, 2025c）。该方法将完整的多智能体会话日志一次性输入 LLM（如 GPT‑4o 或 GPT‑5），要求模型输出单个失败步骤或失败智能体的归因假设。其核心假设是：日志文本本身包含足够信息，使 LLM 能够准确定位故障根源。

DoVer 的动机分析（Section 3）通过复现实验揭示了该范式的根本缺陷：
- 在 WW‑GAIA 数据集上，即使加入显式步骤索引和标注者指南提示（Figure 3），GPT‑4o 在**不确定案例**上的步骤归因准确率仅为 **24%**，GPT‑5 更低至 **7%**；而在**确定案例**上，GPT‑4o 准确率为 44%，GPT‑5 为 53%（Table 5）。
- 14/29 个 WW‑GAIA 案例存在真实标签不确定性（Table 7），根源在于多轮尝试（trial）和多智能体交互导致的归因歧义——同一会话中不同 trial 采用不同策略，各有独立失败点（Figure 1），单步/单智能体标注本质上是不确定的。

All‑at‑Once 范式的两个关键局限由此暴露：**（1）归因假设无验证机制**，正确性仅凭人工标注或逻辑推理判断；**（2）单步归因粒度**无法处理多 trial 场景下的责任分散。DoVer 将这两个维度同时升级：用干预执行的结果作为硬验证信号，用 trial 级多假设并行验证替代单点归因。

#### 1.2 随机基线

随机基线（Random baseline）随机猜测失败归因步骤或智能体，作为归因精度的下限参考。在 WW‑GAIA 的 26 个失败案例上，随机基线无法翻转任何失败（0% 恢复率），而 DoVer 恢复了 17.6% 的 trial（Table 2）。这一差距表明 DoVer 的归因假设虽不完美，但远优于随机猜测，验证了干预驱动闭环的有效性。

### 2. 与后续工作的潜在关联

DoVer 在方法谱系中占据**从被动日志分析到主动干预验证**的转折点，为以下方向提供了基础设施：

- **自动修复循环**：DoVer 目前仅完成“诊断→验证”闭环，但已验证的假设可直接触发修复动作。论文指出 30–67% 的案例因子智能体执行能力不足而陷入 Inconclusive 状态（Section 5.2），这暗示未来工作可将 DoVer 与编码智能体结合，自动合成工具或修改子智能体代码（Open Question 1）。
- **能力感知调试**：DoVer 的干预目前不显式建模子智能体的能力边界。后续工作可引入能力模型，使干预生成时考虑“该智能体是否具备执行此指令的工具/权限”（Open Question 4），从而减少 Agent 不忠实执行干预的概率。
- **多智能体联合干预**：当前 DoVer 的干预以单点编辑为主（编排器消息或计划），未来可扩展到同时修改多个智能体的指令以协调修复（Open Question 6）。

### 3. 适用边界

| 维度 | 适用条件 | 不适用/受限场景 |
|------|----------|-----------------|
| **任务类型** | 短周期、可重放的多智能体任务（如 GAIA、AssistantBench、GSMPlus） | 长时运行、不可重放的生产环境任务；安全关键场景未经验证 |
| **干预空间** | 编排器层消息编辑或计划修改 | 需要修改子智能体内部工具/能力（如添加滚动、PDF 解析）的场景——这些案例在 DoVer 中陷入 Inconclusive |
| **评估方式** | 有人工标注里程碑（milestone）的任务，可计算 Progress Made | 缺少人工标注中间步骤的数据集（如 GSMPlus），Progress Made 指标不可用 |
| **底层模型** | 对底层 LLM 不敏感：GPT‑4o→Qwen3‑32B 仅导致成功率从 17.6% 微降至 16.9%（Table 4） | 极弱模型（如 Qwen3‑8B 0‑shot 仅 11.3%）效果显著下降，但 3‑shot 提示可提升至 14.3%（Table 4） |

### 4. 局限与开放问题

#### 4.1 已识别局限

**（1）干预空间受限**：DoVer 的干预仅限于编排器层的消息或计划编辑，无法直接修改子智能体内部能力。30–67% 的案例因此陷入 Inconclusive 状态（Section 5.2），根源在于子智能体执行能力不足（如缺少滚动到底部工具、PDF 解析失败）。附录 E 的案例研究表明，为子智能体添加工具后，3 个原本 Inconclusive 的案例（Case 20, 21, 26）仅凭编排器级干预即可解决，说明 DoVer 能定位瓶颈但无法自行修复。

**（2）进展度量依赖 LLM 评判**：Progress Made 指标需要 LLM 从人工标注步骤中提取里程碑并评判达成情况（Figure 9–10），可能引入评估偏差。论文使用 GPT‑5 进行里程碑评估以降低自评偏差，但部分环节仍使用 GPT‑4o。对于缺少人工标注中间步骤的数据集（如 GSMPlus），该指标不可用。

**（3）Agent 执行不确定性**：Agent 可能无法忠实地执行干预指令，导致部分干预无法得出明确结论（Inconclusive）。这种执行不确定性削弱了假设验证的可信度，因为无法区分“假设错误”和“Agent 未正确执行干预”。

**（4）长周期/安全关键场景未验证**：所有实验在短周期、非安全关键任务上进行，DoVer 在长时运行、生产环境或安全关键场景下的效能与安全性未经验证。

**（5）对前沿 LLM 的依赖**：DoVer 的归因和干预生成仍依赖 GPT‑4o 级别的前沿模型。虽然消融实验显示 Qwen3‑8B 也可运行（Table 4），但其有效性与任务复杂度相关，且在复杂任务上可能显著退化。

#### 4.2 开放问题

1. **全自动修复循环**：如何将 DoVer 与编码智能体结合，利用已验证的子智能体弱点自动触发工具/能力修复？
2. **无标注进展指标**：在缺乏人工标注里程碑的数据集上，如何设计客观的进展指标以避免 LLM 评判偏差？
3. **能力感知干预生成**：如何使干预生成显式考虑当前子智能体的已知限制（例如缺少某工具）而调整策略？
4. **降低执行不忠实概率**：如何通过更精准的指令形式、更强制的执行机制或多模态验证，降低 Agent 不忠实执行干预的概率？
5. **扩展修复空间**：DoVer 框架能否扩展到需要修改子智能体源代码或合成新工具的故障场景？
6. **多智能体联合干预**：在更复杂的多智能体协调场景中，如何自动区分责任归属并生成针对多个 Agent 的联合干预？



## 原文 PDF

![[paperPDFs/ICLR_2026/DoVer_Intervention_Driven_Auto_Debugging_for_LLM_Multi_Agent_Systems.pdf]]
