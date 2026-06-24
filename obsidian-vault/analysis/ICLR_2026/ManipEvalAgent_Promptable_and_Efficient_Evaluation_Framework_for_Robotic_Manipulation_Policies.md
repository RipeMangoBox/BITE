---
title: "ManipEvalAgent: Promptable and Efficient Evaluation Framework for Robotic Manipulation Policies"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ManipEvalAgent_Promptable_and_Efficient_Evaluation_Framework_for_Robotic_Manipulation_Policies.pdf
openreview_forum_id: 3u6AkbWEls
aliases:
- ManipEvalAgent
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过将人类专家的小批量、多轮交互式评估行为形式化为智能体驱动的自适应流程，动态生成评估任务与工具，实现基于少量样本的高效、可提示、可解释评估。"
primary_logic: "模仿人类专家评估习惯，以智能体协同代码生成和视觉问答为核心，将评估从静态标注转化为动态、可交互的诊断过程，从而在大幅降低采样成本的同时，获得与大规模基准可比且更具洞察力的结论。"
claims:
- "ManipEvalAgent将评估时间从上百分钟缩短至数十分钟，同时大幅降低样本数量（例如ACT策略：42分钟 vs RoboTwin的167分钟、LIBERO的117分钟）"
- "ManipEvalAgent的结论与大规模仿真基准在多个能力维度上具有高度一致性（精确一致率30%-100%，误差容限一致率50%-100%）"
- "代码生成模块成功率高达98%（任务生成）和96%（工具生成），增强模块（RAG、视觉自检、README.Agent）均有正向贡献"
- "框架通过多轮反馈、动态规划和VLM视频理解，可对开放用户查询给出细粒度、可解释的分析报告"
---

# ManipEvalAgent: Promptable and Efficient Evaluation Framework for Robotic Manipulation Policies

> [!tip] 核心洞察
> 模仿人类专家评估习惯，以智能体协同代码生成和视觉问答为核心，将评估从静态标注转化为动态、可交互的诊断过程，从而在大幅降低采样成本的同时，获得与大规模基准可比且更具洞察力的结论。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ManipEvalAgent：面向机器人操作策略的可提示高效评估框架 |
| 英文题名 | ManipEvalAgent: Promptable and Efficient Evaluation Framework for Robotic Manipulation Policies |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3u6AkbWEls) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | ManipEvalAgent |
| Dataset | RoboTwin 2.0 (S.R.评估), LIBERO (S.R.评估), Multi-task Setting (RDT-1B), 代码生成成功率 |

> [!tip] 效果简介
> - RoboTwin 2.0 (S.R.评估) 上，评估时间 (分钟，ACT策略) 为 42，对比 167，变化 -125（减少75%）。
> - LIBERO (S.R.评估) 上，评估时间 (分钟，ACT策略) 为 42，对比 117，变化 -75（减少64%）。
> - Multi-task Setting (RDT-1B) 上，评估时间 (分钟) 为 97，对比 11102 (RoboTwin等效) 或 4909 (LIBERO等效)，变化 约减少99%。

## 概述

机器人操作策略评估长期依赖固定任务集与大规模穷举采样，如 **RoboTwin**（Chen et al., 2025）和 **LIBERO**（Liu et al., 2023），不仅耗时漫长，还仅输出单一成功率分数，缺乏面向用户需求的定制能力与可解释的诊断信息。这一瓶颈严重制约了策略的快速迭代与部署。

**ManipEvalAgent** 的核心洞察在于：将人类专家小批量、多轮交互的评估行为形式化为智能体驱动的自适应流程。框架由提议（Proposal）、生成（Generation）和执行（Execution）三个阶段构成多轮反馈闭环——根据用户查询动态分解评估维度、生成仿真任务与评估工具，并基于中间观测结果持续调整评估方向，最终输出以用户指令为中心的自然语言诊断报告。

实验表明，ManipEvalAgent 在显著压缩评估成本的同时，保持了与大规模基准高度一致的结论。以 ACT 策略为例，评估时间从 RoboTwin 的 167 分钟、LIBERO 的 117 分钟降至 42 分钟，样本量分别减少约 70% 和 43%（Table 1）。在多任务设定下，RDT-1B 的评估时间从等效基准的数千分钟压缩至 97 分钟（Table 4）。结论一致性方面，精确一致率在 30%–100% 之间，误差容限一致率达 50%–100%（Table 2），策略排名亦可通过少量采样复现（Spearman ρ，Table 9）。框架的代码生成模块成功率高达 98%（任务生成）和 96%（工具生成），RAG、视觉自检与 README.Agent 等增强模块均贡献正向增益（Table 3）。

ManipEvalAgent 将评估从静态标注转化为动态、可交互的诊断过程，在效率、可定制性与可解释性上展现出明确优势。当前局限主要在于生成阶段错误（占系统错误的 69.8%，其中任务生成错误占 42.8%，Figure 6）、无法在模拟器中创建新资产，以及跨模拟器移植仍需人工适配。

## 背景与动机

机器人操作策略的评估长期依赖大规模仿真基准，如 **RoboTwin 2.0**（Chen et al., 2025）和 **LIBERO**（Liu et al., 2023）。这些基准提供标准化的固定任务集和预定义评估流程，通过穷举采样计算单一标量成功率来表征策略能力。

然而，这种评估范式存在三个结构性瓶颈：

**第一，评估成本高昂且缺乏灵活性。** 传统基准要求对所有预设任务进行大规模采样才能获得统计稳定的成功率估计。例如，在RoboTwin 2.0上评估ACT策略需耗时167分钟、采集56,592个样本（Table 1）。这一成本随策略数量和任务规模线性增长，在多任务设定下尤为突出——评估RDT-1B策略时，RoboTwin等效流程需耗时11,102分钟（Table 4）。更关键的是，这种固定流程无法响应用户的特定查询需求，评估方向完全由基准设计者预设。

**第二，输出信息单一，缺乏可解释性。** 现有基准仅输出一个成功率标量，无法揭示策略在具体能力维度上的强弱分布，也无法定位失败根因。当策略表现未达预期时，开发者缺乏诊断信息来指导迭代方向。

**第三，评估工具封闭，难以扩展。** 传统基准依赖预定义的规则化指标，无法针对新的评估需求动态生成度量工具，限制了评估的覆盖面和适应性。

上述瓶颈的根本原因在于：现有评估流程将评估视为一次性的、静态的标注过程，而非动态的、交互式的诊断过程。这导致评估效率、灵活性和洞察力之间存在不可调和的矛盾。

ManipEvalAgent的提出正是为了打破这一僵局。其核心动机是**模仿人类专家的小批量、多轮交互式评估行为**——人类专家评估策略时，不会对所有可能任务进行穷举测试，而是根据观察到的中间结果动态调整后续评估方向，逐步深入探测策略的能力边界。通过将这种专家行为形式化为智能体驱动的自适应流程，ManipEvalAgent旨在实现一个关键转变：**将评估从静态标注转化为动态诊断**，从而在大幅降低采样成本的同时，获得与大规模基准可比且更具洞察力的结论（Figure 1）。

## 核心创新

ManipEvalAgent 的核心创新在于将机器人操作策略的评估从“静态穷举测试”重构为“智能体驱动的自适应诊断过程”。其关键设计变更（changed slots）体现在以下四个维度：

### 1. 评估过程：从固定流程到动态规划

传统仿真基准（如 **RoboTwin 2.0** (Chen et al., 2025)、**LIBERO** (Liu et al., 2023)）依赖预定义的任务集和固定的评估流程，评估路径在策略执行前已完全确定。ManipEvalAgent 引入 **Plan Agent**，模拟人类专家的评估行为：接受用户自然语言查询后，将查询分解为多个子评估维度，并在每轮评估后观察中间结果，动态调整后续评估方向（Figure 2; Section 3.2）。这一设计使评估过程具备了“根据中间发现深入探测”的能力，Figure 5 的案例展示了系统如何从基本姿态泛化逐步深入到外观泛化的诊断过程。

### 2. 采样需求：从大规模穷举到小批量自适应

传统基准对所有预设任务进行大规模穷举采样，导致高昂的时间成本。ManipEvalAgent 采用小批量、多轮自适应采样策略：在每个子评估维度上仅采样少量轨迹，根据中间结果决定是否需要进一步采样或调整评估方向。Table 1 显示，以 ACT 策略为例，ManipEvalAgent 仅需 42 分钟和 16,927 个样本，而 RoboTwin 需 167 分钟和 56,592 个样本（减少 75%），LIBERO 需 117 分钟和 29,546 个样本（减少 64%）。在多任务设定下（Table 4），RDT-1B 策略的评估时间从等效的 11,102 分钟降至 97 分钟，降幅约 99%。

### 3. 输出可解释性：从单一标量到多维诊断报告

传统基准仅输出单一成功率分数，无法解释策略在何种条件下失败、失败的具体原因是什么。ManipEvalAgent 通过 VLM 驱动的视频理解与多轮反馈机制，生成以用户指令为中心的自然语言诊断报告，包含细粒度的多维度分析（Figure 1; Section 1）。这一设计使评估结果从“策略好不好”的二元判断升级为“策略在哪些方面好、哪些方面差、为什么”的可解释诊断。

### 4. 评估工具：从预定义规则到动态代码生成

传统基准使用预定义的规则化指标，工具集固定且不可扩展。ManipEvalAgent 通过 **TaskGen Agents** 和 **ToolGen Agents** 实时生成评估任务代码和评估工具代码（Figure 3; Figure 4; Section 3.3）。工具分为两类：规则化度量（$r(\zeta_{j,m})$）和基于 VLM 的 VQA 度量（$q(I_{0:T}, Q)$），后者通过视觉问答格式判断任务成功与否（Section 3.4）。Table 3 显示，任务生成成功率达 98%，工具生成成功率达 96%，且 RAG、视觉自检、README.Agent 三个增强模块均有正向贡献。

### 因果机制总结

上述四个 changed slots 协同作用，形成了“以智能体为驱动、以代码生成为手段、以多轮反馈为机制”的高效评估范式。其因果链条为：**用户查询 → Plan Agent 动态分解 → TaskGen/ToolGen 自适应生成任务与工具 → 小批量采样执行 → VLM 视频理解诊断 → 反馈调整评估方向 → 生成可解释报告**。这一设计使评估从“一次性大规模测试”转变为“渐进式交互诊断”，在保持与大规模基准结论高度一致（Table 2：精确一致率 30%–100%，误差容限一致率 50%–100%）的前提下，大幅降低了评估成本。

## 整体框架

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_3u6AkbWEls/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ManipEvalAgent framework. The system comprises three stages that form a multi-round feedback loop*

ManipEvalAgent 将人类专家的小批量、多轮交互式评估行为形式化为一个智能体驱动的自适应流程。如图 Figure 2 所示，系统由**提议（Proposal）、生成（Generation）、执行（Execution）**三个阶段构成，三者形成闭环反馈回路——系统根据每一轮执行产生的中间观测，动态调整后续评估方向，而非沿固定路径穷举采样。

**输入输出流**：系统接受一个开放式的用户查询（例如“评估该策略在姿态泛化和外观泛化上的表现”），最终输出一份以用户指令为中心的自然语言诊断报告，包含多维细粒度分析。中间过程由三个核心智能体协同完成：

- **Plan Agent** 负责模拟人类评估者的规划行为：将用户查询分解为若干正交的子评估维度 $a_j$，观察中间结果，并根据反馈调整评估方向，最终汇总生成总结报告。
- **TaskGen Agents** 根据每个子评估维度 $a_j$，利用模拟器能力 $\mathbb{S}$ 及任务库 $Kl_{task}$、资产库 $Kl_{asset}$、文档库 $Kl_{doc}$，通过代码生成合成可在模拟器中运行的任务 $\tau_j$，包含场景构建与成功判断逻辑。其流水线（Figure 3）由一个主流程和三个增强模块（RAG、视觉自检、README.Agent）组成。
- **ToolGen Agents** 为每个任务分配评估工具（Figure 4），支持两类度量方式：**规则化度量** $r(\zeta_{j,m})$ 直接对轨迹状态进行数值计算，或**VQA度量** $q(I_{0:T}, Q)$ 利用视觉语言模型对渲染视频帧进行视觉问答。工具可注册复用，形成可扩展的评估工具箱。

**执行与聚合**：对每个子评估维度 $a_j$，系统采样 $M_j$ 条轨迹 $\zeta_{j,m} = Rollout(\pi, \tau_j, seed_m)$，分别用对应工具计算得分 $y_{j,m}$，再经两级聚合得到最终结论：

$$Y_j = Aggregate\{ y_{j,m} \}_{m=1}^{M_j}, \quad Y = Aggregate\{ Y_j \}_{j=1}^N$$

这一设计将评估从传统的静态标注转变为动态、可交互的诊断过程，使得框架在保持结论可靠性的同时，大幅降低采样成本并提供可解释的细粒度分析。

## 核心模块与公式推导

### 3.1 形式化定义

ManipEvalAgent 将评估过程形式化为一个智能体驱动的自适应采样与诊断流水线。给定策略 $\pi$、用户查询 $Q$ 和模拟器 $\mathbb{S}$，框架首先将 $Q$ 分解为 $N$ 个正交的子评估维度 $\{a_j\}_{j=1}^N$，随后对每个维度动态生成任务与工具，执行采样并聚合结果。

**Rollout 定义**：策略 $\pi$ 在任务 $\tau$ 上的一次 rollout 生成状态-观测-动作轨迹，并渲染出视觉帧序列用于后续评估：

$$\zeta = Rollout(\pi, \tau, seed) = \{ (s_t, o_t, a_t) \}_{t=0}^T, \qquad I_{0:T} = Render(\zeta)$$

其中 $s_t$ 为状态，$o_t$ 为观测，$a_t$ 为动作，$I_{0:T}$ 为渲染得到的图像/视频帧序列（Section 3.1）。

**任务生成**：TaskGen 根据子评估维度 $a_j$，利用模拟器能力 $\mathbb{S}$ 及任务库 $Kl_{task}$、资产库 $Kl_{asset}$、文档库 $Kl_{doc}$ 合成可执行任务：

$$\tau_j = TaskGen(a_j, \mathbb{S}, Kl_{task}, Kl_{asset}, Kl_{doc})$$

生成的任务 $\tau_j$ 包含场景构建代码与成功判断逻辑（Section 3.1）。

**评估采样与度量**：对每个子维度 $a_j$，采样 $M_j$ 条轨迹，分别采用规则化工具 $r(\cdot)$ 或 VQA 工具 $q(\cdot)$ 计算得分：

$$\zeta_{j,m} = Rollout(\pi, \tau_j, seed_m), \quad y_{j,m} = \begin{cases} r(\zeta_{j,m}), & \text{规则工具}, \\ q(I_{0:T}, Q), & \text{VQA工具}. \end{cases}$$

**结果聚合**：先对子维度内 $M_j$ 个样本聚合，再对 $N$ 个子维度聚合，形成最终评估结论：

$$Y_j = Aggregate\{ y_{j,m} \}_{m=1}^{M_j}, \quad Y = Aggregate\{ Y_j \}_{j=1}^N$$

### 3.2 三阶段多轮反馈架构

如 Figure 2 所示，ManipEvalAgent 由三个核心阶段构成，形成多轮反馈闭环：

**Proposal 阶段（Plan Agent）**：模拟人类评估专家的行为模式，接收用户查询后将其分解为若干正交的子评估维度，观察每轮中间评估结果，动态调整后续评估方向，最终汇总生成以用户指令为中心的自然语言诊断报告。这是实现“可提示评估”的关键——评估路径完全由用户意图驱动，而非预设的固定任务集。

**Generation 阶段（TaskGen + ToolGen Agents）**：该阶段是框架的核心生成引擎，通过代码生成实现评估任务与工具的按需构造。

- **TaskGen Agents**（Figure 3）：根据 Proposal 阶段输出的子评估维度，生成可在模拟器中直接运行的任务代码。流水线包含一条主流程与三个增强模块——检索增强生成（RAG）、视觉自检（Visual Self-Check）和 README.Agent——分别从文档检索、渲染结果验证和代码库上下文学习三个维度提升生成成功率。消融实验表明，完整配置下任务生成成功率达 98%，移除任一增强模块均导致 2–3% 的性能下降（Table 3）。

- **ToolGen Agents**（Figure 4）：为每个生成的任务分配评估工具，支持两种范式：基于规则度量的确定性工具（如位置误差阈值判断）和基于 VQA 的视觉语义工具（通过 VLM 对渲染视频进行问答式判断）。工具可注册复用，形成可扩展的评估工具箱。

**Execution 阶段**：执行策略 rollout 并收集评估信号，调用规则度量或 VQA 评估器产生得分，将结果反馈至 Plan Agent 以触发下一轮评估规划。

### 3.3 关键设计决策

**动态自适应采样 vs. 穷举采样**：传统仿真基准对所有预设任务进行大规模穷举采样，而 ManipEvalAgent 采用小批量、多轮自适应采样——每轮仅采样少量轨迹，根据中间观察决定后续评估方向。Table 1 显示，ACT 策略在 ManipEvalAgent 下仅需 42 分钟、16927 样本，而 RoboTwin 需 167 分钟、56592 样本，LIBERO 需 117 分钟、29546 样本，时间压缩比达 64%–75%。

**双模态评估工具**：规则工具保证确定性度量的精确性，VQA 工具则赋予框架对开放语义（如“物体是否被稳定抓取”）的判断能力。Table 7 和 Table 8 的扰动实验表明，VQA 工具在场景杂乱、背景纹理变化和光照扰动下仍保持高准确率（>0.98）和高 AUROC（>0.96），为 VLM 驱动的评估可靠性提供了实证支撑。

## 实验与分析

ManipEvalAgent 的核心实验围绕三个维度展开：**评估效率**（能否在大幅降低时间与采样成本的同时保持结论可靠性）、**代码生成鲁棒性**（各增强模块的实际贡献与系统错误分布）、以及**框架的泛化与可解释性**（多任务设定、开放查询与一致性验证）。

### 评估效率与结论一致性

Table 1 给出了最直接的效率对比。以 ACT 策略为例，ManipEvalAgent 仅需 42 分钟、16927 个样本即完成评估，而 RoboTwin 需 167 分钟、56592 个样本，LIBERO 需 117 分钟、29546 个样本——时间分别减少 75% 和 64%，采样量降低约 43%–70%。这一优势在 DP、DP3、RDT、π₀ 等策略上一致复现，证实框架的小批量、多轮自适应采样机制是效率提升的因果杠杆。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_3u6AkbWEls/figures/005_Table_1.jpg]]
*Table 1: Compared with existing simulation benchmarks, ManipEvalAgent significantly reduces the overall evaluation time across multiple robot manipulation policies*

效率提升若以牺牲结论准确性为代价则无意义。Table 2 汇报了 ManipEvalAgent 与现有仿真基准在多个能力维度上的结论一致性。ACT 策略在精确一致率上为 50%，误差容限一致率达 90%；DP 策略分别为 60% 和 100%。其他策略与维度下的精确一致率在 30%–100% 之间波动，误差容限一致率普遍在 50%–100% 区间。这表明框架在少量采样下即可获得与大规模基准高度可比的定性结论，但精确数值存在一定偏差——这与 Table 10 中“绝对正确性逊于传统基准”的结论一致，属于框架设计取舍的必然代价。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_3u6AkbWEls/figures/006_Table_2.jpg]]
*Table 2: We compare the consistency of conclusions between ManipEvalAgent and existing simulation benchmarks across multiple capability dimensions. Across ten trials of the ManipEvalAgent, the percentage of results falling within the exact range (left) or within the error margin (right) is shown*

多任务设定进一步放大了效率优势。Table 4 显示，RDT-1B 策略在 ManipEvalAgent 上仅需 97 分钟、约 27K 样本，而等效的 RoboTwin 评估需 11102 分钟，LIBERO 需 4909 分钟，时间降低约 99%。Table 5 验证了该设定下结论一致性仍然稳健：RDT 和 π₀ 在多数维度上精确一致率与误差容限一致率均维持较高水平。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_3u6AkbWEls/figures/010_Table_4.jpg]]
*Table 4: Total evaluation time and sample count of ManipEvalAgent under the multi-task setting*

策略排名一致性由 Table 9 的 Spearman ρ 量化。在仅 10 次 rollout 条件下，ManipEvalAgent 与标准仿真基准的策略优劣排序已呈现显著正相关；随 rollout 数增至 20 和 50，相关性进一步增强且置信区间收窄。这证明框架在极小采样预算下即可可靠地复现策略间的相对排序。

### 代码生成模块消融与系统错误分析

代码生成是整个框架的基石，其成功率直接决定评估流程的稳定性。Table 3 报告了消融结果：完整 TaskGen 任务生成成功率达 98%，ToolGen 工具生成成功率达 96%。移除 RAG 后，TaskGen 降至 95%，ToolGen 降至 92%；移除视觉自检（Visual Self-Check）或 README.Agent 后，TaskGen 均降至 96%。三项增强模块各自贡献 2–4 个百分点的成功率提升，考虑到评估系统需反复执行、对稳定性要求极高，这些增益具有实际意义。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_3u6AkbWEls/figures/009_Table_3.jpg]]
*Table 3: Ablation of Code Generation Modules*

系统错误分布（Figure 6）揭示了瓶颈所在：**生成阶段错误占全部系统错误的 69.8%，其中任务生成错误占 42.8%，为最大单一错误来源**。工具生成错误和提案/执行阶段错误占比相对较小。这一发现直接指向未来优化的优先级——提升任务生成鲁棒性，尤其是在复杂、长期限的多任务评估场景中，是进一步降低框架失效率的关键。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_3u6AkbWEls/figures/008_Figure_6.jpg]]
*Figure 6: System Error Breakdown*

### VQA 评估工具的可靠性

框架依赖 VLM 驱动的 VQA 工具进行细粒度视觉诊断。Table 7 和 Table 8 分别汇报了 GPT-4o、Gemini 1.5 Pro、GPT-4o mini 在 RoboTwin 2.0 上面对场景杂乱、背景纹理变化、光照扰动时的 VQA 准确率与 AUROC。所有模型在各类扰动下准确率均保持在 0.98 以上，AUROC 超过 0.96，证明 VQA 工具对视觉域偏移具有较强鲁棒性，支撑了框架在开放环境中的诊断可信度。

### 开放查询评估与可解释性

Figure 5 展示了一个开放式用户查询的评估案例：ManipEvalAgent 首先探测策略的姿态泛化能力，再逐步深入评估外观泛化，体现了 Plan Agent 根据中间观察动态调整评估方向的能力。最终输出不是单一标量分数，而是围绕用户指令展开的多维度自然语言诊断报告，实现了从“多少成功率”到“为什么成功/失败、在哪些条件下退化”的范式转换。

### 人-智能体一致性

Table 6 报告了子评估维度分解上的人-智能体一致性（Precision）。GPT-4o 达到 0.943，Gemini 1.5 Pro 为 0.927，GPT-4o mini 为 0.891。这表明 Plan Agent 的评估维度分解与人类专家高度吻合，为框架的自动化评估规划提供了可信度背书。

### 局限与待验证点

尽管整体表现强劲，仍有约 5% 的评估过程受各模块错误影响，任务生成错误占比最高，需在后续工作中优先解决。此外，当前框架无法在模拟器中生成新资产，只能检索已有资产，限制了任务多样性；跨模拟器移植仍需人工适配；且所有实验均在仿真环境中完成，真实世界部署的可行性与挑战尚未验证。这些局限在 Table 10 的特性对比中亦有体现——ManipEvalAgent 在用户驱动、可解释性、动态生成等维度占优，但绝对正确性与可重复性不及传统静态基准。

## 方法谱系与知识库定位

### 与传统仿真评估基准的关系

ManipEvalAgent 的核心定位是对现有机器人操作策略仿真评估范式的**效率重构与能力扩展**，而非替代。传统基准如 **RoboTwin 2.0**（Chen et al., 2025）和 **LIBERO**（Liu et al., 2023）提供了标准化任务集、可重复的评估流程和稳定的成功率指标，但存在三个结构性瓶颈：评估过程固定、采样成本高昂、输出仅为单一标量分数。ManipEvalAgent 将这些基准视为"评估能力锚点"，通过智能体驱动的自适应流程，在保持结论可比性的同时，将评估范式从静态标注转向动态诊断。

具体而言，两者在评估过程、采样需求、输出可解释性和评估工具四个维度上形成鲜明对比：

| 维度 | 传统仿真基准 | ManipEvalAgent |
|------|-------------|----------------|
| 评估过程 | 固定任务集，预定义流程，无用户输入 | 按用户查询动态规划评估路径，多轮自适应生成任务与工具 |
| 采样需求 | 对所有预设任务进行大规模穷举采样 | 小批量、多轮自适应采样，根据中间结果调整后续评估 |
| 输出可解释性 | 单一标量成功率 | 用户指令为中心的自然语言诊断报告，包含多维细粒度分析 |
| 评估工具 | 预定义的规则化指标，无动态工具生成 | 通过代码生成实时构建规则化度量与VLM驱动的VQA评估工具，工具箱可扩展 |

这一关系在 Table 10 中得到了系统对比：ManipEvalAgent 在用户驱动性、可解释性、动态生成能力和工具开放性上占据优势，但在评估结论的**绝对正确性**上逊于传统基准——这是灵活性换取的代价，也是方法边界的关键约束。

### 方法适用边界

ManipEvalAgent 的有效性建立在三个前提之上：

1. **仿真环境的可编程性**：框架依赖模拟器提供的 Python API 来动态生成任务代码和评估工具。当前实现绑定于特定仿真引擎（RoboTwin 2.0 和 LIBERO 的底层模拟器），跨模拟器移植仍需一定量的人工适配，尚未实现与模拟器底层无关的自动通用评估。

2. **资产库的完备性**：任务生成受限于已有资产库的覆盖范围。系统当前无法在模拟器中生成新的3D资产，只能检索和使用已有对象，这限制了任务多样性和评估覆盖面，尤其在需要新物体类型或场景元素的开放式查询中。

3. **代码生成模块的可靠性**：框架的核心能力——任务生成（TaskGen）和工具生成（ToolGen）——依赖大语言模型的代码合成质量。尽管完整系统实现了98%的任务生成成功率和96%的工具生成成功率（Table 3），但约5%的评估过程仍受各模块错误影响，其中生成阶段错误占系统错误的69.8%，任务生成错误最为突出（42.8%）（Figure 6）。这意味着在极端复杂或长周期多任务评估中，错误累积可能导致评估中断或结论偏差。

此外，系统完全基于仿真引擎运行，尚未在真实世界环境中部署验证。从仿真到真实的迁移（sim-to-real gap）是该框架当前未覆盖的维度。

### 局限性

1. **生成阶段的错误主导性**：系统错误分布高度集中于生成阶段（69.8%），其中任务生成错误占42.8%。尽管RAG、视觉自检和README.Agent三个增强模块各自贡献了2-3%的成功率提升（消融实验显示移除任一模组后成功率下降至95-96%），但剩余错误率仍构成评估稳定性的系统性风险。

2. **资产生成的缺失**：无法在模拟器中动态创建新物体，只能检索已有资产。这一限制在用户查询涉及新颖物体或场景时，直接约束了评估的覆盖广度和诊断深度。

3. **跨平台通用性不足**：当前实现与特定仿真引擎接口紧密耦合，迁移到新模拟器需要人工适配，距离"与底层无关的通用评估系统"仍有距离。

4. **绝对正确性的妥协**：如 Table 10 所示，灵活性和可解释性以牺牲评估结论的绝对正确性为代价。框架在结论一致性上表现良好（精确一致率30%-100%，误差容限一致率50%-100%，Table 2），但并非完全可靠，存在一定不确定性。

5. **真实环境验证的缺失**：所有实验均在仿真环境中完成，框架在真实机器人操作场景下的部署可行性和性能表现尚未得到验证。

### 开放问题

1. **资产生成能力的集成**：如何将3D资产生成流水线（如基于扩散模型的物体生成）融入ManipEvalAgent，以突破当前资产库的覆盖限制，支持更灵活的对象创建和评估场景构建？

2. **模拟器解耦的通用评估接口**：能否构建一个仅通过GUI交互、与底层模拟器接口完全解耦的自动评估系统？这将使框架具备真正的跨平台通用性，降低迁移成本。

3. **静态基准与动态评估的统一**：如何将传统仿真基准的稳定性、可重复性与ManipEvalAgent的灵活性、自然语言驱动特性相结合，形成既能保证结论可靠性又能响应用户定制需求的统一评估框架？

4. **真实世界部署的可行性**：ManipEvalAgent在真实环境中的主要挑战是什么？视觉感知噪声、动作执行不确定性、场景动态变化等因素对VQA评估工具的鲁棒性影响如何？附录中Table 7和Table 8展示了VQA在多种视觉扰动下的高准确率和高AUROC，但这些扰动仅覆盖仿真环境，真实世界的复杂性可能引入新的失效模式。

5. **多模态感知的融合**：引入事件相机、深度估计、触觉传感等额外感知模态，能否进一步提升评估可靠性、诊断能力和对策略失败根因的定位精度？

6. **长周期评估的错误率控制**：在复杂、长期限的多任务评估场景中，任务生成和工具生成环节的错误累积效应如何抑制？是否需要引入更细粒度的错误恢复机制或分层验证策略？

7. **人机协同的评估范式**：Table 6显示GPT-4o在子评估维度分解上与人类的一致性达0.943，但仍有约6%的偏差。如何设计有效的人机协同机制，在保持效率优势的同时，通过最小化的人工干预纠正智能体的偏差？

## 原文 PDF

![[paperPDFs/ICLR_2026/ManipEvalAgent_Promptable_and_Efficient_Evaluation_Framework_for_Robotic_Manipulation_Policies.pdf]]
