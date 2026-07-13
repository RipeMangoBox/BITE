---
title: "Helmsman: Autonomous Synthesis of Federated Learning Systems via Collaborative LLM Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Helmsman_Autonomous_Synthesis_of_Federated_Learning_Systems_via_Collaborative_LLM_Agents.pdf
project_link: null
code_link: https://github.com/haoyuan-l/Helmsman
openreview_forum_id: Voiy13SK3r
aliases:
- Helmsman
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过引入一个多智能体系统（Helmsman），将端到端的FL系统设计从手工转变为自动化合成，通过三个协作阶段（交互式规划、模块化编码、自主评估）来导航组合复杂性。"
primary_logic: "将FL研发工作流模拟为结构化的多智能体协作流水线，利用大语言模型（LLM）进行规划、编码和验证，并通过人机回环（HITL）确保可靠性，从而在无需人工编码的情况下生成性能媲美甚至超越手工设计的FL解决方案。"
claims:
- "Helmsman生成的策略在多个异构FL基准上（如CIFAR-10N标签噪声、HAR用户异构、Speech Commands说话人变化、Fed-ISIC2019站点异构、CIFAR-100资源约束）达到最佳性能，显著优于FedAvg/FedProx，并经常超越专门设计的方法。"
- "在持续学习任务Split-CIFAR100上，Helmsman合成的方法（通过客户端经验回放与全局模型蒸馏的组合策略）取得了50.95%的准确率，远超FedAvg（15.38%）、FedProx（15.86%）和专门基线FedWeIT（29.45%），证明了自动化合成复杂策略的能力。"
- "消融实验表明，移除双层验证导致所有任务的成功率为0%，而完整的Helmsman系统实现了100%的成功率，验证了自主评估与细化循环的关键性。"
- "与现有代理代码生成系统（Codex, Claude Code）相比，Helmsman在AgentFL-Bench 16个任务上的成功率从37.5%/43.75%提升至100%，成本显著降低，且生成代码结构稳定。"
---

# Helmsman: Autonomous Synthesis of Federated Learning Systems via Collaborative LLM Agents

> [!tip] 核心洞察
> 将FL研发工作流模拟为结构化的多智能体协作流水线，利用大语言模型（LLM）进行规划、编码和验证，并通过人机回环（HITL）确保可靠性，从而在无需人工编码的情况下生成性能媲美甚至超越手工设计的FL解决方案。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Helmsman：通过协作式LLM代理自主合成联邦学习系统 |
| 英文题名 | Helmsman: Autonomous Synthesis of Federated Learning Systems via Collaborative LLM Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Voiy13SK3r) · [GitHub](https://github.com/haoyuan-l/Helmsman) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Helmsman |
| Dataset | CIFAR-10N (Label Noise), HAR (User Heterogeneity), Speech Commands (Speaker Variation), Fed-ISIC2019 (Site Heterogeneity) |

> [!tip] 效果简介
> - CIFAR-10N (Label Noise) 上，Accuracy (%) 为 81.62±0.62，对比 80.55±0.47 (FedNS†)，变化 +1.07。
> - HAR (User Heterogeneity) 上，Accuracy (%) 为 96.28±0.42，对比 95.19±0.75 (FedNova*)，变化 +1.09。
> - Speech Commands (Speaker Variation) 上，Accuracy (%) 为 86.58±0.38，对比 83.48±0.49 (FedNova*)，变化 +3.10。

## 概要

联邦学习（FL）的设计空间正面临难以驾驭的组合复杂性：数据异质性、系统约束、任务目标变化等多维挑战与日益增多的专门策略之间形成指数级组合，使得端到端FL系统的研发高度依赖领域专家的手工设计。这种手动范式不仅耗时且易出错，更成为阻碍FL在真实场景中广泛采用的瓶颈。

**Helmsman** 针对这一瓶颈提出了根本性转变——将FL系统设计从手工编码转变为**自动化合成**。其核心洞见在于：将FL研发工作流模拟为结构化的多智能体协作流水线，利用大语言模型（LLM）进行规划、编码和验证，并通过人机回环（HITL）确保可靠性，从而在无需人工编码的情况下生成性能媲美甚至超越手工设计的FL解决方案。

系统通过三个协作阶段导航组合复杂性：
- **交互式规划**：将高层用户查询通过自我反思与人机回环验证精炼为可执行的研究计划；
- **模块化编码**：由主管代理分解蓝图，四个专门编码团队（Task、Client、Strategy、Server）按依赖图协同开发；
- **自主评估**：在沙盒仿真中执行双层验证（L1运行时完整性检查 + L2语义正确性检查），并通过Debugger代理自动修补，形成闭环精炼。

在覆盖16个任务的AgentFL-Bench基准上，Helmsman合成的策略在多个异构FL场景中达到最佳性能——在标签噪声（CIFAR-10N）、用户异构（HAR）、说话人变化（Speech Commands）、站点异构（Fed-ISIC2019）等任务上显著优于FedAvg和FedProx，并经常超越专门设计的方法（如FedNova、FedNS、HeteroFL）。尤其在持续学习任务Split-CIFAR100上，Helmsman合成的方法取得了50.95%的准确率，远超专门基线FedWeIT的29.45%（+21.50个百分点），证明了自动化合成复杂策略的能力。消融实验进一步揭示，移除双层验证导致所有任务成功率为0%，验证了自主评估与精炼循环的关键性。



联邦学习（Federated Learning, FL）允许多个参与方在不共享原始数据的前提下协同训练机器学习模型，在隐私敏感的应用场景中展现出巨大潜力。然而，联邦学习系统的实际设计过程远非简单——它要求研究者同时应对数据异质性、系统异质性、通信效率、个性化、持续学习以及隐私约束等多重挑战。这些挑战并非孤立存在，而是以组合方式叠加，形成了**棘手的设计空间**（intractable design space，参见图2）：针对标签噪声、用户异构、资源约束等不同问题，存在FedProx、FedNova、FedNS、HeteroFL、FedPer、FedWeIT等大量专门化的策略，而将这些策略与具体任务约束进行匹配，需要深度的领域知识和大量的试错实验。

当前联邦学习系统的研发范式高度依赖**人工专家**：研究者需要手动分析问题、查阅文献、设计算法、编写代码、运行实验并反复调试。这种手动设计范式构成了联邦学习广泛采用的关键瓶颈——设计空间的组合复杂性使得即便是经验丰富的研究者，也难以在合理的时间内穷举所有可行方案，更遑论非专家用户。

近年来，大语言模型（LLM）在代码生成和自动化推理方面取得了显著进展，催生了如Codex、Claude Code等代理式代码生成系统。然而，这些系统在面对联邦学习这种需要**跨模块协调、领域知识密集、且对语义正确性有严格要求**的复杂系统设计时，暴露出明显不足：生成的代码结构不稳定、容易引入运行时错误、缺乏对联邦学习特定语义约束的验证能力。实验表明，现有代理代码生成系统在AgentFL-Bench的16个联邦学习任务上成功率仅为37.5%–43.75%，远未达到实用要求。

上述缺口揭示了一个核心矛盾：**联邦学习系统的设计复杂性已经超出了单一LLM代理的处理能力，但该领域的自动化需求又极为迫切**。本文的动机正是弥合这一鸿沟——能否通过结构化的多智能体协作，将人类专家的联邦学习研发工作流系统性地转化为自动化流水线，从而在保持生成质量的同时，大幅降低设计门槛？



## 核心方法与创新机理

Helmsman的核心创新在于将联邦学习系统的端到端研发流程从“专家手工设计”转变为“多智能体协作的自动化合成”。这一转变并非简单的自动化替换，而是通过三个紧密耦合的机制——**交互式规划**、**模块化编码**和**自主评估闭环**——来导航FL设计空间的组合复杂性，从而在无需人工编码的前提下，生成性能媲美甚至超越手工设计的FL解决方案。

### 创新一：从手工设计到自动化合成流水线的范式转变

传统FL系统开发依赖领域专家手动完成需求分析、策略选择、代码实现和实验验证。当面对数据异质性、系统约束、任务目标变化等多重挑战的交叉组合时，这种手工范式面临难以处理的设计空间爆炸（intractable design space，Figure 2）。Helmsman通过引入一个结构化的多智能体流水线，将这一过程完全自动化：

| 设计环节 | 传统手工范式 | Helmsman自动化范式 |
|----------|------------|------------------|
| 需求分析 | 专家查阅文献、手动设计方案 | Planning Agent + Reflection Agent 自动生成并自我批判研究计划，辅以人机回环验证 |
| 代码实现 | 专家手工编写端到端代码 | Supervisor Agent 将计划分解为四个模块蓝图，四个专门编码团队（Task/Client/Strategy/Server）按依赖图协同开发 |
| 测试验证 | 手工运行测试、分析日志 | Evaluator Agent 在沙盒仿真中执行双层验证（L1运行时完整性 + L2语义正确性），Debugger Agent 自动修补直至成功 |

这一范式转变的核心因果机制在于：**将FL研发工作流建模为结构化的多智能体协作流水线**，利用大语言模型进行规划、编码和验证，并通过人机回环确保可靠性。消融实验提供了决定性证据：移除双层验证后，所有AgentFL-Bench任务的成功率降至0%，而完整系统实现了100%的成功率（Table 6），验证了自主评估与修复循环对整个系统正确性的关键作用。

### 创新二：依赖感知的模块化多智能体编码架构

与现有基于单一LLM代理的代码生成系统（如Codex、Claude Code）不同，Helmsman采用了一种**依赖感知的模块化编码架构**。Supervisor Agent将研究计划分解为Task、Client、Strategy、Server四个模块的详细蓝图，并强制执行依赖图——例如，Server模块的编码工作仅在Strategy和Task模块稳定后才启动。每个模块由配对的Coder Agent和Tester Agent负责实现和实时验证。

这一设计的核心优势在于**生成代码的结构稳定性**。Figure 4的对比实验显示：Claude Code在三次独立运行中产生了完全不同的文件夹结构和实现方式，而Helmsman在所有运行中保持了相同的系统结构。这种稳定性不仅确保了可复现性，还实现了即插即用的模块化能力——用户可以单独替换某个模块而无需重构整个系统。

### 创新三：双层验证与自主修复闭环

Helmsman的评估阶段引入了一个**双层验证机制**，这是确保生成代码正确性的关键创新：

- **L1 运行时完整性验证**：扫描仿真日志中的显式错误签名（如异常堆栈、导入错误等）。
- **L2 语义正确性验证**：分析结构化输出，检查联邦学习特有的语义约束（如聚合逻辑是否正确、通信协议是否符合预期）。

该闭环的数学形式为：

$$L _ { i } = \mathrm { S i m u l a t e } ( C _ { i } , N )$$

$$( S _ { i } , E _ { i } ) = f _ { e v a l } ( L _ { i } , \mathcal { H } )$$

$$C _ { i + 1 } = f _ { d e b u g } ( C _ { i } , \bar { E } _ { i } )$$

其中，Evaluator代理 $f_{eval}$ 使用启发式规则集 $\mathcal{H}$ 分析仿真日志 $L_i$，输出状态 $S_i$ 和错误报告 $E_i$；Debugger代理 $f_{debug}$ 基于错误报告修补代码基，生成新版本 $C_{i+1}$。该循环最多执行10次迭代，确保代码既可执行又语义正确。消融实验表明，这一机制是整个系统成功的决定性因素——移除后成功率为0%，而完整系统达到100%（Table 6）。

### 创新四：组合策略的自主合成能力

Helmsman展现出了超越简单策略选择的**组合策略合成能力**。在持续学习任务Split-CIFAR100上，系统自主合成了一个将客户端经验回放与全局模型蒸馏相结合的混合策略，取得了50.95%的准确率，远超FedAvg（15.38%）、FedProx（15.86%）和专门设计的FedWeIT（29.45%）（Table 4）。这种组合策略并非来自预定义的模板库，而是系统在理解任务需求后自主生成的创新方案，体现了从“策略选择”到“策略合成”的质变。



![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/002_Figure_1.jpg]]
*Figure 1: The automated FL development workflow of Helmsman. (a) Planning: A user query is refined into an actionable research plan via human-in-the-loop dialogue. (b) Coding: Specialized agent teams, managed by a Supervisor, collaboratively build a modular codebase. (c) Evaluation: The final code is autonomously tested and refined in a closed simulation loop until correct*

Helmsman 是一个多智能体系统，其核心设计思想是将联邦学习（FL）研发工作流建模为结构化的多智能体协作流水线。系统接收用户的高层自然语言查询作为输入，通过三个协作阶段的自动化流水线，输出一个功能完整、可执行的 FL 代码基，整个过程无需人工编写代码。

系统包含以下七个核心代理模块，按流水线阶段组织：

**规划阶段（Planning Stage）**

- **Planning Agent**：接收用户查询，调用 Web 搜索和 RAG 工具获取 FL 文献知识，生成初始研究计划。
- **Reflection Agent**：对计划进行自动批判性评估，检查逻辑连贯性、实验设置完整性和可行性，输出 `COMPLETE` 或 `INCOMPLETE` 状态及反馈。该阶段采用两步验证循环——先由 Reflection Agent 自动反思，再通过人机回环（HITL）由用户确认，确保计划既合理又与用户意图对齐。

**编码阶段（Coding Stage）**

- **Supervisor Agent**：将研究计划分解为 Task、Client、Strategy、Server 四个模块的详细蓝图，并管理模块间的依赖图。例如，Server 模块的开发仅在 Strategy 和 Task 模块稳定后才启动。
- **Coder Agent**：针对每个模块分别实现代码，遵循 Flower 框架的接口规范。
- **Tester Agent**：与 Coder Agent 配对，对生成的模块进行实时验证和调试。

**评估阶段（Evaluation Stage）**

- **Evaluator Agent**：在沙盒仿真环境中执行代码并分析日志，执行双层验证：
  - **L1 运行时完整性检查**：扫描日志中的显式错误签名。
  - **L2 语义正确性检查**：分析结构化输出，判断模型行为是否符合预期。
- **Debugger Agent**：基于错误报告修补有缺陷的代码，生成新版本代码基。系统最多尝试 10 次修复，形成闭环迭代。

整个系统的输入输出流可概括为：**用户查询 → 研究计划（经 HITL 确认）→ 模块化代码基（经依赖感知的协作编码）→ 可执行的 FL 解决方案（经双层验证与修复闭环）**。系统的 LLM 后端采用 Gemini-2.5-flash 负责规划，Claude-Sonnet-4.0 负责编码与评估，底层基于 LangGraph 和 LangChain 框架构建。



### 系统架构总览

Helmsman是一个多智能体框架，通过三个编排阶段将高层用户目标转化为可执行的联邦学习代码基。系统架构围绕一条闭环流水线构建，其核心逻辑可概括为：**交互式规划 → 模块化编码 → 自主评估与修复循环**。三个阶段的协作关系如Figure 1所示，各阶段内部由专门的智能体团队完成特定子任务。

### 关键模块

#### 1. 规划阶段模块

规划阶段采用**两步验证循环**，结合自主自我修正与人在回环监督。

- **Planning Agent**：接收用户查询，调用Web搜索和RAG工具获取FL文献知识，生成初始研究计划。
- **Reflection Agent**：在计划提交用户之前执行自动化批判性评估。该代理依据预定义标准（逻辑连贯性、实验设置完整性、可行性）系统性地审查草案，输出`COMPLETE`或`INCOMPLETE`状态及反馈。只有通过反思代理审查的计划才会进入人机回环（HITL）审查。

这一双层过滤机制确保研究计划在进入编码阶段前既经过算法验证，又获得人类意图对齐。

#### 2. 编码阶段模块

编码阶段由一个监督代理管理四个专门的编码团队，执行依赖感知的模块化开发。

- **Supervisor Agent**：将研究计划分解为四个模块的详细蓝图——**Task**（数据加载与预处理）、**Client**（客户端本地训练逻辑）、**Strategy**（聚合策略）、**Server**（服务端编排）。监督代理强制执行依赖图：例如，Server模块的开发仅在Strategy和Task模块稳定后才启动。
- **Coder Agent × 4**：分别针对Task、Client、Strategy、Server模块实现代码，遵循Flower框架的接口规范。
- **Tester Agent × 4**：与对应Coder配对，对生成的模块进行实时验证和调试。

这种模块化分解将复杂的FL系统设计问题降维为可并行开发的子问题，同时通过依赖图保证模块间接口的一致性。

#### 3. 评估与修复阶段模块

评估阶段构成系统的核心闭环——在沙盒仿真中执行代码，通过双层验证诊断问题，并自动修补。

- **Evaluator Agent**：在仿真环境中执行代码并分析日志，执行分层诊断：
  - **L1 运行时完整性验证**：扫描日志中的显式错误签名（异常、崩溃）。
  - **L2 语义正确性验证**：分析结构化输出，检查训练损失是否下降、准确率是否提升等语义信号。
- **Debugger Agent**：基于Evaluator产生的错误报告，对缺陷代码进行修补，生成新版本代码基。系统设置最大调试尝试次数为10次，若无法收敛则终止并请求人工干预。

### 关键公式

评估修复循环的形式化描述如下。

**仿真日志生成**：
$$L_i = \mathrm{Simulate}(C_i, N)$$
其中 $C_i$ 为第 $i$ 轮迭代的代码基，$N$ 为沙盒仿真中的联邦通信轮次（系统设定 $N=5$），$L_i$ 为产生的仿真日志。

**评估诊断**：
$$(S_i, E_i) = f_{eval}(L_i, \mathcal{H})$$
其中 $f_{eval}$ 为Evaluator代理，$\mathcal{H}$ 为启发式规则集，$S_i \in \{\text{SUCCESS}, \text{FAIL}\}$ 为评估状态，$E_i$ 为错误报告。

**调试修补**：
$$C_{i+1} = f_{debug}(C_i, \bar{E}_i)$$
其中 $f_{debug}$ 为Debugger代理，$\bar{E}_i$ 为错误报告，$C_{i+1}$ 为修补后的代码基。该过程迭代执行，直至 $S_i = \text{SUCCESS}$ 或达到最大尝试次数。

这三个公式刻画了系统从“执行→诊断→修复”的闭环逻辑，是Helmsman实现自主代码生成与验证的核心机制。消融实验（Table 6）表明，移除双层验证（即取消 $f_{eval}$ 的L1/L2检查）后所有任务成功率为0%，验证了该闭环的关键性。

### 模块间数据流

规划阶段产出的研究计划经HITL确认后，传递至Supervisor Agent进行模块分解。Supervisor生成的蓝图驱动四个Coder-Tester团队并行开发，各模块完成后由Evaluator在沙盒中集成执行。若双层验证失败，Debugger介入修补，修补后的代码基重新进入仿真循环。这一数据流确保了从高层语义查询到可执行代码基的端到端自动化，同时通过人在回环节点保留人类对关键决策的控制权。



## 实验与关键发现

### 主要结果：异构联邦学习基准性能

Helmsman在AgentFL-Bench的16个任务上进行了系统性评估，覆盖数据异质性、系统异质性、通信效率、个性化、主动学习和持续学习等多个FL研究领域。表2–4汇总了核心性能对比，其中Helmsman生成的策略在所有任务上均显著优于FedAvg和FedProx基线，并在多数任务上达到或超越专门设计的方法。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/005_Table_2.jpg]]
*Table 2: Performance evaluation on heterogeneous federated learning benchmarks (a). We compare our agent-synthesized strategy against task-specific baselines. Results are averaged over 3 independent runs with standard deviation. The best performing method is marked in bold, while the second-best is underlined. Results for specialized methods are denoted by symbols: FedNova∗ (Wang et al., 2020), FedNS† (Li et al., 2024), and HeteroFL‡ (Diao et al., 2020)*

**数据异质性与分布偏移**（Table 2）：在CIFAR-10N标签噪声任务（Q3）上，Helmsman达到81.62%准确率，超过专门方法FedNS†（80.55%）。在HAR用户异构（Q5）和Speech Commands说话人变化（Q6）任务上，Helmsman分别取得96.28%和86.58%，较FedNova*分别提升1.09和3.10个百分点。在Fed-ISIC2019站点异构（Q7）上，Helmsman（63.75%）同样优于FedNova*（62.88%）。

**通信效率与个性化**（Table 3）：在CIFAR-100带宽限制（Q10）任务上，Helmsman以48.78%准确率显著超越FedNova*（45.77%），提升3.01个百分点。在FEMNIST连接限制（Q11）上，Helmsman（89.73%）优于FedNova*（89.11%）。在个性化任务（Q12–Q13）中，Helmsman同样表现出竞争力，生成的策略在CIFAR-100个性化任务上达到62.94%，超越HeteroFL‡（62.62%）。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/007_Table_3.jpg]]
*Table 3: Performance evaluation on heterogeneous federated learning benchmarks (b). We compare our agent-synthesized strategy against task-specific baselines. Results are averaged over 3 independent runs with standard deviation. Results for specialized methods are denoted by symbols: FedNova∗ (Wang et al., 2020), FedPer§ (Arivazhagan et al., 2019), and FedWelt¶ (Yoon et al., 2021)*

**联邦持续学习**（Table 4）：这是Helmsman自动化合成能力最突出的证据。在Split-CIFAR100增量任务（Q16，Task=5）上，Helmsman合成的方法达到50.95%准确率，远超FedAvg（15.38%）、FedProx（15.86%）和专门基线FedWeIT¶（29.45%），提升幅度达21.50个百分点。分析生成代码发现，Helmsman自主组合了客户端经验回放与全局模型蒸馏两种技术，形成了新颖的混合策略，这验证了系统在复杂组合性挑战下导航设计空间的能力。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/008_Table_4.jpg]]
*Table 4: Performance evaluation on heterogeneous federated learning benchmarks (c). We compare our agent-synthesized strategy against task-specific baselines. Results are averaged over 3 independent runs with standard deviation. Results for specific federated learning methods are denoted by symbols: FedWelt¶ (Yoon et al., 2021), FAST# (Li et al., 2025)*

### 消融实验：系统组件的因果贡献

Table 6的系统消融揭示了各组件对成功率的决定性影响：

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/010_Table_6.jpg]]
*Table 6: Ablation study of Helmsman system component contributions on AgentFL-bench tasks (Claude-Sonnet-4.5) across six settings. Components denote: ⃝1 Planning Group with Supervision; ⃝2 Collaborative Modular Coding Group; ⃝3 Sandboxed Simulation with Dual-Layer Verification. The fifth setting denotes the full Helmsman System without having human-in-the-loop (HITL)*

- **双层验证是关键瓶颈**：移除沙盒仿真中的双层验证（L1运行时完整性检查 + L2语义正确性检查）后，所有AgentFL-Bench任务的成功率直接降为0%。这表明自主评估与修复闭环是系统正确性的必要条件——没有它，生成的代码无法保证可执行性和语义正确性。
- **完整系统达到100%成功率**：包含规划组（Planning Agent + Reflection Agent）、协作模块化编码组和双层验证的完整Helmsman系统，在测试设置中实现了100%的任务成功率。
- **人机回环（HITL）提升鲁棒性**：移除HITL后系统仍能工作，但鲁棒性下降。HITL在处理不完整或超出模式的输入查询时尤为关键——Table 7显示，Helmsman能够检测缺失信息并请求用户补充，或通过手动审查路由异常输入。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/011_Table_7.jpg]]
*Table 7: Helmsman’s Response to Different Input Schemas for Query 1 (CIFAR-10-LT FL Task)*

### 与现有代码生成系统的对比

Tables 8–12将Helmsman与Codex和Claude Code进行了全面对比，涵盖成本、Token消耗、墙钟时间和成功率：

- **成功率**：Codex和Claude Code在AgentFL-Bench 16个任务上的成功率仅为37.5%和43.75%，而Helmsman达到100%。基线系统在多数任务上直接失败，无法生成可执行的FL代码。
- **成本与效率**：Helmsman（GPT-5.1变体）在多数任务上实现了最低的金钱成本和Token消耗，同时墙钟时间也具有竞争力。
- **代码稳定性**：Figure 4展示了关键的结构性差异——Claude Code在三次独立运行中产生完全不同的文件夹结构和实现，而Helmsman在所有运行中保持相同的系统结构，确保了可复现性和即插即用的模块化特性。

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/017_Figure_4.jpg]]
*Figure 4: (a) Claude Code (Run 1) (b) Claude Code (Run 2) (c) Claude Code (Run 3) (d) Helmsman (All Runs) Figure 4: Code generation stability comparison on Q1 task across 3 independent runs. Claude Code (Claude-Sonnet-4.5) produces distinct folder structures and implementations in each run (a-c), demonstrating inconsistent code generation. In contrast, Helmsman maintains an identical system structure across all runs (d), ensuring reproducibility and enabling plug-and-play modularity*

### 失败模式与局限性

尽管Helmsman在基准测试中表现优异，系统仍存在明确的失败边界：

- **迭代修复不保证收敛**：Debugger代理最多尝试10次修复。在特别复杂或定义不清的任务中，修复循环可能无法找到有效补丁，系统会因达到最大尝试次数而终止，此时需要更高层次的人工干预。
- **LLM后端依赖**：当前系统使用Gemini-2.5-flash进行规划、Claude-Sonnet-4.0进行编码和评估，性能和成本可能随LLM版本变化。
- **框架耦合**：系统使用Flower框架作为沙盒仿真环境，生成的代码依赖Flower API，迁移到其他框架需要额外适配。
- **基准覆盖范围**：AgentFL-Bench的16个任务虽覆盖了多个FL研究领域，但可能未涵盖所有真实世界的极端情况。

### 核心图表结论

| 图表 | 核心结论 |
|------|----------|
| Table 2–4 | Helmsman在所有异构FL任务上超越FedAvg/FedProx，在多数任务上达到或超越专门方法；Split-CIFAR100上提升21.50个百分点，证明自动化合成复杂策略的能力 |
| Table 6 | 双层验证是系统正确性的必要条件（移除后成功率0%）；完整系统达100%成功率 |
| Figure 4 | Helmsman生成代码结构稳定、可复现，而Claude Code每次运行产生不同结构 |
| Tables 8–12 | Helmsman在成功率（100% vs 37.5%/43.75%）、成本和Token效率上全面优于Codex和Claude Code |

### 补充图表

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/004_Table_1.jpg]]
*Table 1: The structured natural language template for specifying tasks to Helmsman. This template guides the user to provide a comprehensive and unambiguous problem definition, ensuring the Planning Agent receives the necessary context regarding the application domain, data characteristics, and desired FL objectives. The provided query example shows a complete instantiation of this template*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/009_Table_5.jpg]]
*Table 5: Performance on Split-CIFAR100 (α = 0.5). We evaluate methods under 5-task and 10-task scenarios, reporting average accuracy (Acc ↑) and forgetting (F ↓). Best results are in bold*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/012_Table_8.jpg]]
*Table 8: Comprehensive performance comparison across federated learning tasks (Part a: Q1-Q3). For each task, we report Cost ($, lower the better), Total Tokens (in thousands, lower the better), Walltime (seconds, lower the better), and Outcome. Best results per metric are in bold*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/013_Table_9.jpg]]
*Table 9: Comprehensive performance comparison across federated learning tasks (Part b: Q4-Q6). For each task, we report Cost ($, lower the better), Total Tokens (in thousands, lower the better), Walltime (seconds, lower the better), and Outcome. Best results per metric are in bold*

![[assets/figures/papers/paper_list_l19_https_openreview_net_forum_id_Voiy13SK3r/figures/014_Table_10.jpg]]
*Table 10: Comprehensive performance comparison across federated learning tasks (Part c: Q7-Q9). For each task, we report Cost ($, lower the better), Total Tokens (in thousands, lower the better), Walltime (seconds, lower the better), and Outcome. Best results per metric are in bold*



## 定位与知识库关联

### 1. 在联邦学习自动化设计谱系中的位置

Helmsman 处于“联邦学习系统自动化合成”这一新兴方向的起点位置。传统联邦学习系统设计完全依赖领域专家手工完成，从问题分析、策略选择、代码实现到实验验证形成闭环。Helmsman 首次将这一完整工作流建模为结构化的多智能体协作流水线，实现了从高层用户查询到可执行代码基的端到端自动化。

与现有代码生成代理（如 Codex、Claude Code）的单体式“一步生成”范式不同，Helmsman 引入了三个关键的结构化创新：
- **交互式规划**：通过 Planning Agent 与 Reflection Agent 的双步验证循环，结合人机回环（HITL），将模糊的用户查询精炼为可验证的研究计划，而非直接跳入编码。
- **模块化编码**：Supervisor Agent 将研究计划分解为 Task、Client、Strategy、Server 四个模块的详细蓝图，由四个专门的编码团队（每队含 Coder 和 Tester）按依赖图协同开发，而非由单一代理生成整体代码。
- **自主评估闭环**：在沙盒仿真中执行双层验证（L1 运行时完整性检查 + L2 语义正确性检查），由 Evaluator Agent 分析日志，Debugger Agent 根据错误报告自动修补，最多尝试 10 次，形成“执行—诊断—修复”闭环。

这种结构化设计使得 Helmsman 在 AgentFL-Bench 的 16 个任务上实现了 100% 的成功率，而 Codex 和 Claude Code 的成功率仅为 37.5% 和 43.75%（Tables 8-12）。更重要的是，Helmsman 生成的代码结构在多次独立运行中保持稳定（Figure 4），而 Claude Code 每次运行产生不同的文件夹结构和实现，这为联邦学习系统的可复现性和模块化复用提供了基础保障。

### 2. 与现有联邦学习方法的对比关系

Helmsman 本身不是一个具体的联邦学习算法，而是一个**算法合成系统**。它在 AgentFL-Bench 上生成的策略与以下手工设计的基线方法进行了系统对比：

| 基线方法 | 针对问题 | 来源 |
|---------|---------|------|
| **FedAvg** | 基础联邦平均 | McMahan et al., 2017 |
| **FedProx** | 系统异质性 | Li et al., 2020a |
| **FedNova** | 分布偏移 | Wang et al., 2020 |
| **FedNS** | 标签噪声 | Li et al., 2024 |
| **HeteroFL** | 异构模型 | Diao et al., 2020 |
| **FedPer** | 个性化联邦学习 | Arivazhagan et al., 2019 |
| **FedWeIT** | 联邦持续学习 | Yoon et al., 2021 |
| **FAST** | 联邦主动学习 | Li et al., 2025 |

实验结果表明，Helmsman 合成的策略在多个异构 FL 基准上达到最佳或次佳性能：
- 在 CIFAR-10N 标签噪声任务上达到 81.62%，超越专门方法 **FedNS**（80.55%）（Table 2, Q3）；
- 在 HAR 用户异构任务上达到 96.28%，超越 **FedNova**（95.19%）（Table 2, Q5）；
- 在 Speech Commands 说话人变化任务上达到 86.58%，显著超越 **FedNova**（83.48%）（Table 2, Q6）；
- 在 Split-CIFAR100 持续学习任务上达到 50.95%，大幅超越专门基线 **FedWeIT**（29.45%），提升幅度达 21.50 个百分点（Table 4, Q16）。

值得注意的是，Helmsman 在持续学习任务上的突破性表现源于其自动合成的**组合策略**——将客户端经验回放与全局模型蒸馏相结合。这种策略组合在手工设计范式中通常需要专家深入理解多个技术方向并进行非平凡的集成，而 Helmsman 通过多智能体协作自主发现了这一有效组合。

### 3. 适用边界与关键约束

尽管 Helmsman 展现了强大的自动化合成能力，其适用性受到以下边界的约束：

**技术栈依赖**：Helmsman 使用 Flower 框架作为沙盒仿真环境，生成的代码依赖 Flower 的 API。迁移到其他联邦学习框架（如 FedML、PySyft）需要额外适配。这是系统架构层面的固有约束，而非实验覆盖不足。

**LLM 后端绑定**：当前系统使用 Gemini-2.5-flash 进行规划，Claude-Sonnet-4.0 进行编码和评估。消融实验（Table 6）和成本对比（Tables 8-12）均基于这些特定模型。LLM 能力的版本变化可能影响系统性能和成本特征，这是方法层面的可迁移性约束。

**迭代修复的上限**：Debugger Agent 的修复循环最多尝试 10 次。分析指出，在特别复杂或定义不清的任务中，Debugger 可能无法找到有效补丁，系统会因达到最大尝试次数而终止，需要更高层次的人工干预。这意味着 Helmsman 在“可自动修复”与“需人工介入”之间存在一个模糊边界，该边界的精确位置尚未被系统刻画。

**基准覆盖范围**：实验在 AgentFL-Bench 的 16 个任务上进行，覆盖了数据异质性、系统异质性、个性化、通信效率、主动学习和持续学习等主要 FL 研究方向，但可能未涵盖所有真实世界的极端情况（如拜占庭攻击、差分隐私约束、跨机构合规要求等）。

**自动化与人工参与的权衡**：人机回环（HITL）在规划阶段提高了可靠性（消融实验显示移除 HITL 后鲁棒性下降），但降低了全自动化程度。Table 7 表明 Helmsman 能处理不完整或超出模式的输入查询，但这一能力依赖于 HITL 机制，可能不适用于完全无人类参与的场景。

### 4. 未解决的问题与未来方向

分析揭示了以下开放问题，需要后续工作验证：

- **自我进化能力**：Helmsman 当前是一个静态流水线，其生成策略的质量受限于底层 LLM 的能力和知识截止日期。能否引入记忆机制，使系统从历史成功和失败案例中持续学习，实现策略生成能力的自我进化？这是方法层面的根本性开放问题。

- **跨范式泛化**：Helmsman 的设计原则（结构化多智能体协作、双层验证、依赖感知编码）能否扩展到更广泛的分布式机器学习系统，如去中心化学习、分割学习、联邦强化学习？当前实验仅限于标准联邦学习场景，跨范式的迁移需要新的基准和验证。

- **形式化验证集成**：当前的双层验证依赖启发式规则和 LLM 的语义分析，本质上仍是经验性的。能否在不显著增加成本和延迟的前提下，集成形式化验证技术（如针对通信协议的正确性证明）以进一步提高生成代码的可靠性？这是一个质量保证层面的开放问题。

- **非功能性需求对齐**：在完全无人类参与的情况下，Helmsman 生成的系统如何保证与伦理、公平性、隐私保护等非功能性需求的长期对齐？当前系统通过 HITL 间接处理这些需求，但自动化对齐机制尚未被探索。

- **成本与性能的帕累托前沿**：Tables 8-12 显示不同 LLM 后端（GPT-5.1 vs. Claude-Sonnet-4.5）在成本、延迟和成功率之间存在权衡。是否存在更优的代理分工策略或模型选择策略，能够在保持 100% 成功率的同时进一步降低成本？这需要更系统的成本-性能联合优化研究。



## 原文 PDF

![[paperPDFs/ICLR_2026/Helmsman_Autonomous_Synthesis_of_Federated_Learning_Systems_via_Collaborative_LLM_Agents.pdf]]
