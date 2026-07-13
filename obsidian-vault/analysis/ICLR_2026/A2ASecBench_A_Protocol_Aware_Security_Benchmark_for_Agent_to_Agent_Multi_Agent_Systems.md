---
title: "A2ASecBench: A Protocol-Aware Security Benchmark for Agent-to-Agent Multi-Agent Systems"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A2ASecBench_A_Protocol_Aware_Security_Benchmark_for_Agent_to_Agent_Multi_Agent_Systems.pdf
project_link: https://safo-lab.github.io/A2ASecBench/
code_link: null
aliases:
- A2ASecBench
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/safety_security
core_operator: "是否在A2A协议中嵌入身份证明、能力签名验证、任务图环检测与并发资源限制。"
primary_logic: "多智能体系统的安全性不仅是提示词安全问题，更是一个协议语义问题；必须在发现、编排和执行全生命周期引进可验证的身份、声明的能力和资源消耗管理。"
claims:
- "通过仅10个伪AgentCard，A2A发现机制的Top-1选择攻击成功率高达99%（Table 7）。"
- "Capability Cloaking攻击在所有三个高风险领域中均实现100%的攻击成功率（Table 2）。"
- "即使部署NVIDIA NeMo Guardrails，Artifact-Triggered Script Injection的攻击成功率仍高达94%（Table 4）。"
- "攻击模式能够跨框架转移，在LangGraph和ANP上Cycle Overflow、ASRF、ATSI均达到100% ASR（Table 3）。"
---

# A2ASecBench: A Protocol-Aware Security Benchmark for Agent-to-Agent Multi-Agent Systems

> [!tip] 核心洞察
> 多智能体系统的安全性不仅是提示词安全问题，更是一个协议语义问题；必须在发现、编排和执行全生命周期引进可验证的身份、声明的能力和资源消耗管理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | A2ASecBench：面向智能体间多智能体系统的协议感知安全基准 |
| 英文题名 | A2ASecBench: A Protocol-Aware Security Benchmark for Agent-to-Agent Multi-Agent Systems |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=LfdFnakqGJ) · [Project](https://safo-lab.github.io/A2ASecBench/) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/safety_security |
| Method | A2ASecBench |
| Dataset | A2A-MAS (Travel) |

> [!tip] 效果简介
> - A2A-MAS (Travel) 上，ASR (AgentCard Spoofing) 为 0.820，对比 0.000 (secure target)，变化 +0.820。
> - A2A-MAS (Travel) 上，ASR (Capability Cloaking) 为 1.00，对比 0.00，变化 +1.00。
> - A2A-MAS (Travel) 上，ASR (Cycle Overflow) 为 1.00，对比 0.00，变化 +1.00。

## 概要

当前智能体间（Agent-to-Agent, A2A）多智能体系统在协议层面普遍缺乏对智能体身份真实性和能力一致性的验证机制，任务编排也未对循环依赖和资源过度占用进行检测，导致攻击者能够通过构造恶意代理卡片、隐藏能力声明、诱导循环任务流等手段实现欺骗、隐蔽执行和拒绝服务等攻击。本文提出 **A2ASecBench**，一个面向 A2A 多智能体系统的协议感知安全基准框架，其核心定位在于：安全风险不仅来自提示词输入，更根植于协议语义——必须在智能体的发现、编排和执行全生命周期引入可验证的身份、声明能力约束与资源管理。

围绕这一视角，A2ASecBench 首先构建了一个威胁分类，将 A2A 生态系统中的攻击归纳为**供应链操纵类**（AgentCard Spoofing、Capability Cloaking）与**协议逻辑缺陷类**（Cycle Overflow、Half-Open Task Flooding、Agent-Side Request Forgery、Artifact-Triggered Script Injection）共六种具体攻击向量（Table 1）。在此基础上，框架通过场景适配器（Scenario Adapter）利用 LLM 动态生成跨领域的可执行测试用例，并引入**安全-效用联合评估**方法，在每次对抗试验旁配对良性任务，测量攻击成功率（ASR）与系统有用性下降之间的权衡（Abstract, §4.3）。

主要实验结果表明，在基于官方 A2A-MAS 示例的旅行、医疗、金融三个高风险环境中：
- AgentCard Spoofing 的 ASR 达到约 **0.82**，且攻击成功率随注入的伪 AgentCard 数量 k 单调增长（k=10 时 Top-1 欺骗成功率达 **99%**，Table 7）；
- Capability Cloaking 在所有三个领域中 ASR 均为 **1.00**（Table 2）；
- Cycle Overflow、Half-Open Task Flooding、Agent-Side Request Forgery 和 Artifact-Triggered Script Injection 等协议逻辑攻击在无防护条件下普遍达到 **1.00** 的 ASR（Table 2）；
- 攻击模式具有跨框架可转移性：在 LangGraph 和 ANP 等不同协议框架上，Core-Overflow、ASRF、ATSI 等攻击同样能够实现 **1.00** ASR（Table 3）；
- 即使部署 NVIDIA NeMo Guardrails 等生产级防御措施，Artifact-Triggered Script Injection 的 ASR 仍高达 **0.91–0.94**，其他部分攻击的 ASR 也有显著残留（Table 4）。

上述发现表明，现有单一提示词防御范式无法有效应对协议层面的系统性威胁，A2A 多智能体系统亟需在协议核心中嵌入轻量级身份校验、能力签名验证及任务图环检测等机制——这正是 A2ASecBench 作为安全评估基础设施所揭示的核心瓶颈与改进方向。



随着大语言模型（LLM）驱动的智能体被广泛应用于复杂任务，智能体间（Agent-to-Agent，A2A）协议通过标准化的发现、编排与执行流程，使异构智能体能够动态协作，成为下一代智能体应用的核心支撑。Figure 1 描绘了 A2A 协议生态系统的完整供应链、交互流与智能体应用架构；截至 2025 年 11 月，已有多家企业的商业产品采用 A2A 协议（Table 9），表明其正迅速从实验走向大规模部署。

然而，A2A 多智能体系统（MAS）的安全保障存在根本性缺口。现有安全研究主要聚焦于单智能体的提示注入（prompt injection）与越狱攻击，而忽略了协议层特有的攻击面。核心瓶颈在于：**协议层面缺乏对智能体身份真实性、能力一致性、任务图循环依赖以及并发资源占用的系统性验证**，使得系统暴露在欺骗、隐蔽行为与拒绝服务等攻击之下。如 Table 1 所示，A2A 生态面临两大类威胁——供给链操纵（AgentCard 欺骗、能力隐藏）与协议逻辑弱点（循环溢出、半开任务洪水、智能体侧请求伪造、工件触发脚本注入）。实验证据证实了这些威胁的严重性：

- 仅通过注入 10 个伪 AgentCard，A2A 发现机制的 Top‑1 选择攻击成功率高达 **99%**（Table 7）；
- 能力隐藏（Capability Cloaking）在所有三个高风险领域中实现 **100%** 攻击成功率（Table 2）；
- 即使部署 NVIDIA NeMo Guardrails 生产级安全网关，工件触发脚本注入（ATSI）的攻击成功率仍高达 **94%**（Table 4）；
- 攻击模式可跨框架转移：在 LangGraph 和 ANP 上，循环溢出、智能体侧请求伪造（ASRF）、ATSI 均达到 **100% ASR**（Table 3）。

上述结果一致表明，多智能体系统的安全性远非单纯的提示词安全问题，而是一个**协议语义问题**——核心控制的因果节点在于：是否在 A2A 协议的全生命周期（发现、编排、执行）中引入可验证的身份证明、能力签名验证、任务图环检测与并发资源限制。传统以单智能体为中心的评估方法既无法覆盖这类协议攻击，也未能联合度量安全性降低与有用性损失之间的权衡。

因此，构建一个**协议感知的、可伸缩的综合评估基准**，系统量化攻击成功率与效用代价，并驱动防御机制设计，成为紧迫需求。本文首次提出 A2ASecBench——一个面向 A2A 生态的安全基准框架，通过形式化六种具体攻击向量、引入动态场景适配器，并在旅行、医疗、金融三个高风险领域实施大规模安全‑效用联合评估，旨在填补这一关键空白，并为下一代安全 A2A 协议设计提供实证基础。



## 核心方法与创新机理

当前针对智能体的安全研究几乎全部聚焦于提示注入与单代理边界内的越权行为，默认多智能体通信是安全可信的。但 A2ASecBench 系统性地揭示了一个更深层的瓶颈：Agent-to-Agent (A2A) 多智能体系统的脆弱性**本质上是协议语义问题**，而非孤立的提示安全问题。若不在发现、编排与执行全生命周期引入可验证的身份绑定、声明的能力证明及资源消耗管理，所有基于提示词的防御都将被绕开。基于这一洞察，工作相对于现有安全评估基线做出了三个核心改变。

**改变 1：威胁模型从“单点提示安全”升级为“协议感知全生命周期威胁分类”。**  
现有安全基准大多覆盖提示注入或模型越狱，而忽略 A2A 协议特有的供给链操作与协议逻辑弱点。A2ASecBench 提出两层威胁分类（供给链操控 vs. 协议逻辑弱点），并将威胁实例化为六个具体攻击向量：AgentCard Spoofing (AS)、Capability Cloaking (CC)、Cycle Overflow (CO)、Half-Open Task Flooding (HOTF)、Agent-Side Request Forgery (ASRF)、Artifact-Triggered Script Injection (ATSI)（Table 1）。每个攻击向量都映射至协议生命周期的特定阶段（发现、选择、运行等），并通过数学定义其成功条件（例如 `∃C⊆Et: cycle(C)=true ∧ termination(Gt)=timeout` 表示循环溢出成功）。这种形式化不仅明确了攻击因果机制，也使得评估可复现、可证伪。基线系统（未受保护的 Gemini 2.5 Flash A2A-MAS）对该六种攻击几乎完全不设防，其中 CC、CO、HOTF、ASRF、ATSI 在三类高风险场景下均达到 100% 攻击成功率（Table 2），充分说明原威胁模型是根本性缺失的。

**改变 2：评估方法论从“单一安全指标”转向“安全-效用联合权衡”。**  
传统评估往往仅报告攻击成功率，忽略安全防护引入的有用性衰减。A2ASecBench 将每个攻击试验与良性任务配对执行，同时计算攻击成功率（ASR）和有用性下降，从而给出安全与功能之间的权衡曲线。这一改变直接回应了实际部署中“安全不能以功能丧失为代价”的工程约束，并且暴露了仅依赖安全网关的局部缓解效果：例如 NVIDIA NeMo Guardrails 可使部分攻击的 ASR 显著下降（ASRF 降至 0.23–0.48），但对 Artifact-Triggered Script Injection 的 ASR 仍高达 0.91–0.94（Table 4），提示单纯的提示级防御无法根治协议级漏洞，也强调了安全-效用联合评估的必要性。

**改变 3：基准构造从“手工制作单域样本”升级为“LLM 驱动的跨域自适应生成”。**  
过去的安全基准需要大量人工针对每个领域逐一撰写攻击样本，难以扩展到多领域，且容易引入人为偏差。A2ASecBench 引入场景适配器（Scenario Adapter），形式化为映射 `Adapter:𝒜×𝒮→𝒯`，利用 LLM 根据攻击向量描述和场景规范自动生成 JSON 结构的可执行测试用例（Prompt 10）。这一设计使基准能够在旅行、医疗、金融三个高风险领域以统一的方式生成总量达 1800 的测试任务（Table 5），保证了跨领域评估的公平性，同时支持攻击模式在 LangGraph、ANP 等不同框架上的可转移性验证（CO、ASRF、ATSI 在 LangGraph 上 ASR 均为 1.00，六种攻击在 ANP 上 ASR ≥ 0.98，Table 3），证明了所发现漏洞的通用性而非偶然性。

这三个改变将 A2A 多智能体系统的安全从提示词层面推到协议语义层面，并提供了自动化、可扩展且带有效用权衡的评估框架，构成 A2ASecBench 对当前基线最本质的提升。



![[assets/figures/papers/iclr26_0016_LfdFnakqGJ_A2ASecBench_A_Protocol-Aware_Security_Benchmark/figures/001_Figure_1.jpg]]
*Figure 1: A2A Protocol Ecosystem: Supply Chain, Interaction Flow, and Agentic Application*

![[assets/figures/papers/iclr26_0016_LfdFnakqGJ_A2ASecBench_A_Protocol-Aware_Security_Benchmark/figures/002_Table_1.jpg]]
*Table 1: Six Concrete A2A-Specific Threats*

A2ASecBench 是一种协议感知的安全基准框架，旨在系统性地暴露 A2A 多智能体系统中协议层面的脆弱性。整个 pipeline 以威胁建模为起点，经由攻击向量形式化、自动化测试用例生成，最终在受测系统上执行评估并输出安全‑效用权衡分析。框架由四个核心模块级联而成，模块间的输入输出流将理论威胁转化为可度量的攻击成功率与效用下降。

**威胁分类与建模模块**  
该模块对 A2A 生态系统进行威胁建模，将风险归并为两大类：**供给链操纵**与**协议逻辑弱点**，并由此细化出六种具体攻击向量——AgentCard Spoofing、Capability Cloaking、Cycle Overflow、Half‑Open Task Flooding、Agent‑Side Request Forgery 与 Artifact‑Triggered Script Injection。每种威胁均被映射到协议生命周期阶段、受影响的组件以及安全目标（CIA），形成结构化的威胁表格（Table 1），为下游攻击生成提供语义锚点。框架将 A2A 系统抽象为有向图 $G = (V, E)$，其中节点 $V$ 为智能体，边 $E$ 为 Agent‑to‑Agent 通信，并用生命周期映射 $\Lambda$ 规范协议状态转换（发现→选择→创建→操作→更新→终止），从而建立起统一的攻击面描述。

**攻击向量形式化模块**  
在明确的威胁分类之上，该模块用数学条件定义每种攻击成功的判据，使攻击向量成为可验证的规范。例如，AgentCard Spoofing 的候选集定义为 $\mathcal{C}^{*} = \{ C^{+}(a) \} \cup \{ C_{1}^{-}(a), \ldots, C_{k}^{-}(a) \}$，以衡量发现机制的选择偏差；Capability Cloaking 通过隐藏能力集 $\Delta U \triangleq \tilde{U}_{\mathrm{act}} \setminus \tilde{U}_{\mathrm{decl}} \neq \emptyset$ 描述声明的能力与实际能力的差异；Cycle Overflow 的成功条件则为 $\exists C \subseteq E_{t}: \mathrm{cycle}(C) = \mathrm{true} \land \mathrm{termination}(G_{t}) = \mathrm{timeout}$；Half‑Open Task Flooding 则引入指示器 $\mathbb{I}_{\mathrm{flood}}(\alpha; T)$ 来检测半开任务数的阈值。这些形式化条件不仅为攻击生成提供了精确的目标，也构成了评估引擎判断攻击成功的基础。

**场景适配器模块**  
为将攻击向量转化为可自动化执行的测试用例，框架引入基于 LLM 的场景适配器。该适配器被形式化为映射 $\mathrm{Adapter}: \mathcal{A} \times \mathcal{S} \longrightarrow \mathcal{T}$，其中 $\mathcal{A}$ 为攻击向量集合，$\mathcal{S}$ 为场景规范（如旅行、医疗、金融等高风险域），$\mathcal{T}$ 为可执行的 JSON 测试用例集合。适配器通过结构化提示（参见 Prompt 10）动态生成与场景语义一致的攻击实例，确保跨领域、跨攻击类型的批量生成，从而避免了手工构造样本的瓶颈。该模块的输出直接送入评估引擎，支持对相同受测系统的可复现攻击。

**评估引擎**  
评估引擎在目标 A2A‑MAS（基于官方 A2A 示例，搭载 Gemini 2.5 Flash）上批量执行适配器生成的测试用例，并采用联合安全‑效用评估方法论：每项攻击试验旁均配对对应的良性任务，同时记录攻击成功率 $\mathrm{ASR} = \frac{\sum_{i=1}^{N} \mathbb{I}_i}{N}$ 和良性任务效用下降，最终输出安全‑效用权衡报告。该引擎还能兼容不同的多智能体框架（LangGraph、ANP），验证攻击模式的可转移性（Table 3），并可用于评估现有防御措施（如 NVIDIA NeMo Guardrails）的缓解效果（Table 4）。通过此闭环，框架不仅揭示了当前 A2A 系统在发现、编排与执行阶段的协议级弱点（如 AgentCard Spoofing 在仅 10 个伪卡注入下 Top‑1 选择攻击成功率高达 99%），还为领域提供了统一、可量化的安全基准。



### 1. 框架核心模块
A2ASecBench 的自动化评估管道由四个功能互补的核心模块构成，分别覆盖威胁建模、形式化判据、测试样例生成与定量评估。

- **威胁分类与建模模块**  
  对 A2A 生态系统进行系统威胁分析，将安全风险划分为**供给链操作**与**协议逻辑弱点**两大类，并细化出六种具体攻击向量：AgentCard Spoofing、Capability Cloaking、Cycle Overflow、Half‑Open Task Flooding、Agent‑Side Request Forgery 与 Artifact‑Triggered Script Injection，其影响的生命周期阶段、协议组件与安全目标集中定义于 Table 1（§3）。该模块是整个基准的语义基础，决定了后续攻击形式化的覆盖范围。

- **攻击向量形式化模块**  
  为每一种攻击构建可计算的数学判据，将安全条件转为布尔/数值指标。核心数据结构包括欺骗候选集 $\mathcal{C}^{*}$、隐藏能力集 $\Delta U$、循环检测函数 $\mathrm{cycle}(\cdot)$、洪水指示器 $\mathbb{I}_{\mathrm{flood}}$ 等（§4.2）。这些定义使攻击成功与否不再依赖人类判读，而是基于任务图状态、时间约束或输出产物中的金丝雀标记自动裁决。

- **场景适配器模块**  
  形式化为映射 $\mathrm{Adapter}: \mathcal{A} \times \mathcal{S} \longrightarrow \mathcal{T}$（§4.3），其中 $\mathcal{A}$ 为攻击向量描述空间，$\mathcal{S}$ 为领域场景规范空间，$\mathcal{T}$ 为可执行测试用例空间。实现上，通过结构化 Prompt（Prompt 10）驱动 LLM，从攻击原语和场景元数据生成 JSON 格式的测试样本。该模块解决了人工构造攻击样本的伸缩性问题，使得同一攻击向量可低成本迁移到旅行、医疗、金融三个高风险领域。

- **评估引擎**  
  在目标多智能体系统（基于官方 A2A‑MAS 示例，使用 Gemini 2.5 Flash 作为基础模型）上批量执行测试用例。每个攻击试验均配对一个等量良性任务，以同时度量**攻击成功率（ASR）**与**有用性下降**，输出安全‑效用权衡报告（§5.2, Table 2）。引擎支持对未防护基线、NVIDIA NeMo Guardrails 加固后的系统以及跨框架迁移场景（LangGraph、ANP）的统一评测。

### 2. 关键公式与变量含义
以下公式支撑攻击形式化与定量评估，所有符号均来自已公开的论文本体（标注对应文内位置）。

**系统图表示**  
$$G = \left( V , E \right) \quad \text{(§4.1)}$$
- $V$：智能体节点集合。  
- $E$：节点间 A2A 通信的有向边集合。  
在运行时，系统实例化为 $G_t = (V, E_t)$，其中 $E_t$ 携带当前任务产生的动态边，是循环溢出等攻击的直接作用对象。

**AgentCard 欺骗候选集**  
$$\mathcal{C}^{*} = \{ C^{+}(a) \} \cup \{ C_{1}^{-}(a), \ldots, C_{k}^{-}(a) \}, \quad |\mathcal{C}^{*}| = k+1 \quad \text{(§4.2)}$$
- $C^{+}(a)$：合法的真实 AgentCard。  
- $C_i^{-}(a)$：注入的第 $i$ 个恶意变体（“伪卡”）。  
- $k$：攻击者注入的伪卡数量。  
发现机制需要从 $\mathcal{C}^{*}$ 中选取最合适的卡片，该集合大小直接控制欺骗难度；实验表明 $k=10$ 时 Top‑1 欺骗成功率可达 99%（Table 7）。

**隐藏能力集（Capability Cloaking）**  
$$\Delta U \triangleq \tilde{U}_{\mathrm{act}} \setminus \tilde{U}_{\mathrm{decl}} \neq \emptyset \quad \text{(§4.2)}$$
- $\tilde{U}_{\mathrm{act}}$：智能体后端实际实现的能力集合。  
- $\tilde{U}_{\mathrm{decl}}$：AgentCard 中声明暴露的能力集合。  
当 $\Delta U \neq \emptyset$ 时，存在“声称无害但实际可执行恶意行为”的能力差，攻击视为成功。该类攻击在所有受测领域均达 100% ASR（Table 2）。

**循环溢出成功条件**  
$$\exists C \subseteq E_{t}: \mathrm{cycle}(C) = \mathrm{true} \land \mathrm{termination}(G_{t}) = \mathrm{timeout} \quad \text{(§4.2)}$$
- $C$：运行时任务边集 $E_t$ 的子图。  
- $\mathrm{cycle}(C)$：布尔函数，判定 $C$ 是否为有向循环。  
- $\mathrm{termination}(G_t) = \mathrm{timeout}$ 表示工作流未能在规定的最大步数内正常终止。  
二者同时满足即判定攻击成功，对应任务调度无法收敛的拒绝服务状态。

**半开任务洪水指示器**  
$$\mathbb{I}_{\mathrm{flood}}(\alpha; T) = \begin{cases} 1 & \text{if } |\{ t \in T : s(t) = s_{\mathrm{in}} \}| \geq \Theta_{\mathrm{thres}} \\ 0 & \text{otherwise} \end{cases} \quad \text{(§4.2)}$$
- $T$：系统当前的任务集合。  
- $s(t)$：任务 $t$ 的状态，$s_{\mathrm{in}}$ 表示“半开”状态（任务已创建但未推进至完成/失败）。  
- $\Theta_{\mathrm{thres}}$：触发洪水的阈值。  
当处于半开状态的任务数达到或超过阈值，$\mathbb{I}_{\mathrm{flood}}=1$，指示资源耗尽型攻击成功。

**攻击成功率（ASR）**  
$$\mathrm{ASR} = \frac{\sum_{i=1}^{N} \mathbb{I}_i}{N} \quad \text{(§5.2)}$$
- $N$：针对某一攻击向量在特定领域的试验总次数（通常为 100）。  
- $\mathbb{I}_i \in \{0,1\}$：第 $i$ 次试验中攻击是否成功的二值指示器，由相应形式化判据裁定。  
ASR 是基准的核心度量，反映攻击向量在当前系统配置下的可利用性。

**场景适配器形式映射**  
$$\mathrm{Adapter}: \mathcal{A} \times \mathcal{S} \longrightarrow \mathcal{T} \quad \text{(§4.3)}$$
- $\mathcal{A}$：攻击向量语义描述的空间。  
- $\mathcal{S}$：领域场景规范（角色、工具、交互约束等）的空间。  
- $\mathcal{T}$：可执行测试用例（JSON 格式）的空间。  
该映射由 LLM 实例化，使基准能够从抽象攻击原语自动扩展到不同领域，无需逐例手工编写。



## 实验与关键发现

### 主结果：六类攻击的跨领域高成功率

A2ASecBench 在旅行、医疗、金融三个高风险领域各部署 100 个良性任务与 100 个攻击任务（共 1800 个任务，Table 5），对基于 Gemini 2.5 Flash 的 A2A‑MAS 基线系统进行了全面评估。结果表明，**五种攻击的跨领域攻击成功率（ASR）达到 100%，仅 AgentCard 欺骗略低**（Table 2）：

![[assets/figures/papers/iclr26_0016_LfdFnakqGJ_A2ASecBench_A_Protocol-Aware_Security_Benchmark/figures/004_Table_2.jpg]]
*Table 2: ASR across three scenarios for six attacks*

- Capability Cloaking 在全部三个场景中 ASR = 1.00，说明注册时仅公开良性能力而隐藏恶意行为的攻击模式极易成功。
- Cycle Overflow、Half‑Open Task Flooding、Agent‑Side Request Forgery、Artifact‑Triggered Script Injection 同样均获得 1.00 的 ASR，显示编排、执行与终止阶段均缺乏协议层面的防护。
- AgentCard Spoofing 的 ASR 在 0.82 左右，虽未达满分，但仍意味着超过八成攻击可成功劫持任务路由。

上述结果揭示了 A2A 系统的脆弱性具有**协议语义根源**。攻击模式在跨框架迁移实验中进一步得到验证：将攻击移植到 LangGraph 与 ANP 后，Cycle Overflow、ASRF 和 ATSI 保持 1.00 ASR；在 ANP 上六种攻击的 ASR ≥ 0.98（Table 3），说明漏洞普适存在于 A2A 协议，而非实现特例。

![[assets/figures/papers/iclr26_0016_LfdFnakqGJ_A2ASecBench_A_Protocol-Aware_Security_Benchmark/figures/007_Table_3.jpg]]
*Table 3: Transferability of attack patterns. We evaluate CO, ASRF, ATSI patterns in Lang-Graph and all six in ANP. Table 4: Attack Mitigation and Guardrail Performance. Evaluation of defensive measures across four protocol-level attacks CO, ASRF, ATSI, HOTF using NVIDIA NeMo Guardrail*

### 现有防御的局限与失败模式

引入 NVIDIA NeMo Guardrails 这一成熟内容安全网关后，部分攻击的 ASR 有所下降，但总体仍不满足安全需求（Table 4）：

![[assets/figures/papers/iclr26_0016_LfdFnakqGJ_A2ASecBench_A_Protocol-Aware_Security_Benchmark/figures/008_Table_4.jpg]]

- Cycle Overflow 的 ASR 降至 0.66–0.73，Half‑Open Task Flooding 降至 0.85–0.91，表明网关对流程级异常仅有微弱抑制作用。
- Agent‑Side Request Forgery 的 ASR 降至 0.23–0.48，是缓解幅度最大的攻击，因为网关能识别部分恶意请求文本。
- **Artifact‑Triggered Script Injection（ATSI）的 ASR 仍高达 0.91–0.94**，显示基于内容的过滤无法应对通过工件间接注入并在渲染阶段激活的恶意逻辑。

这些数据暴露了内容导向防御的**结构性失败**：攻击者利用协议交互状态和工件传递链路绕过检查，而网关缺乏对代理间任务图、资源消耗以及返回结果信任边界的全局感知。因此，单点提示防护或内容过滤无法阻止面向协议逻辑的攻击。

### 消融实验：欺骗规模与发现机制的弱点

AgentCard 欺骗对注入的伪卡数量 k 表现出高度敏感性（Table 6）：当 k 从 3 增加至 7 时，ASR 从 76% 单调上升至 95%。  
在 k=10 的发现排名实验中（Table 7、8），A2A 的 Top‑1 欺骗成功率达 99%，Top‑3 为 87%；ANP 的 Top‑1 更是达到 100%，Top‑3 为 81.25%。这表明 A2A 发现机制主要依赖文本相似度匹配，**缺乏对 AgentCard 身份的密码学绑定或完整性校验**，攻击者只需注入少量高相似度伪卡即可掌控任务分配。

![[assets/figures/papers/iclr26_0016_LfdFnakqGJ_A2ASecBench_A_Protocol-Aware_Security_Benchmark/figures/016_Table_7.jpg]]
*Table 7: A2A discovery ranking under AgentCard Spoofing with k“10 injected lookalikes*

Capability Cloaking 通过良性任务的效用下降间接度量，虽避免了直接抓取恶意行为带来的工程复杂性，但该方法可能低估攻击的真实危害——隐藏能力仅在特定上下文中触发，且不一定产生显著效用波动，存在**探测敏感度不足的风险**。

### 关键图表结论

- **Table 1** 将六种攻击映射至 A2A 生命周期的发现、选择、创建、操作等阶段与 CIA 属性，构成整个基准的威胁建模骨架。
- **Table 2** 直观展示了核心漏洞的数量级：除 AgentCard 欺骗外，其余攻击的跨域 ASR 均为 100%，表明默认 A2A 系统全域脆弱。
- **Table 3** 证明攻击模式具备跨框架迁移性，确认漏洞属于协议层面而非平台特例。
- **Table 4** 暴露了安全网关的防护短板：ATSI 和洪水攻击几乎不受抑制，ASRF 的部分缓解提示需要将协议语义纳入防御设计。
- **Table 6–8** 的消融结果指出身份验证是 A2A 安全的首要瓶颈：少量伪造即可颠覆发现过程，需通过嵌入身份证明、能力签名等机制从根本上加固协议。

综上，实验系统地表明，A2A 多智能体系统的安全风险是协议层面固有的结构性问题。仅靠提示工程或内容网关无法解决身份伪造、循环依赖和资源滥用等攻击。后续防御必须引入可验证身份、声明能力加密签名，以及任务图环检测与并发限制等协议级机制。



## 定位与知识库关联

A2ASecBench 的核心贡献在于将多智能体系统的安全分析从传统的提示词注入与单代理安全（baseline 的主流关注点）推向协议语义层面。已有安全措施（如 NVIDIA NeMo Guardrails 增强的 A2A‑MAS）主要工作在应用‑模型边界，试图通过输入/输出内容审查拦截恶意行为，但这类防御在面对协议级威胁时暴露了本质瓶颈：它不理解智能体身份的真实性、声明的能力与实际行为的差异，也不掌握任务图的拓扑结构。因此，作为生产级安全网关代表的 NeMo Guardrails 对半开任务洪水（HOTF）的 ASR 仍高达 0.85–0.91，对 Cycle Overflow 仅降至 0.66–0.73，对工件触发脚本注入（ATSI）的抑制几乎无效（ASR 0.91–0.94，Table 4）。这一结果并非防御强度的不足，而是防御假设的错位——协议层的语义欺骗在内容层往往合法且无明显恶意特征。

与 LangGraph 和 ANP 等不同协议框架的基准系统对比，进一步证实了攻击模式的因果机制独立于特定实现：只要 A2A 交互的生命周期（发现→选举→创建→操作→更新→终止）缺失对身份证明、能力签名、任务图无环性及资源上界的约束，通过 AgentCard 欺骗、能力隐藏、循环依赖注入等方式实现供给链操弄或协议逻辑破坏的条件就天然存在。例如，仅注入 10 个伪 AgentCard，Top‑1 发现的选择攻击成功率高达 99%（Table 7），而隐藏恶意能力背后的“声明‑实际能力差”$\Delta U$ 在三大高风险领域均造成 100% 的效用下降（Table 2）。这验证了一个深层规律：**安全性不是附加的提示词过滤问题，而是内嵌于协议原语的身份与行为语义验证问题。**

### 适用边界与假设条件

A2ASecBench 的适用性建立在一组明确的系统假设之上：
- **协议范围**：工作聚焦于 A2A 协议的发现、编排和执行阶段（Table 1），并经由场景适配器 $\mathrm{Adapter}: \mathcal{A} \times \mathcal{S} \longrightarrow \mathcal{T}$ 将攻击向量映射为可执行的测试用例。对于不遵循 A2A 语义（如非代理‑客户端直接点对点通信，或不使用 AgentCard 进行能力宣传）的多智能体系统，需重写适配逻辑。
- **攻击覆盖**：当前基准仅覆盖六个具体攻击向量（AgentCard 欺骗、能力隐藏、循环溢出、半开任务洪水、代理侧请求伪造、工件触发脚本注入）。A2A 生态系统可能存在的其他威胁（如加密密钥泄露、模型提取、隐私推断）未被纳入。
- **环境与数据生成**：评估基于官方 A2A‑MAS 示例（Gemini 2.5 Flash）及三个模拟领域（旅行、医疗、金融）。攻击样本由 LLM 驱动的适配器生成（Prompt 10），虽然保证了跨领域伸缩性，但可能引入样本偏向。跨框架可转移性实验（LangGraph、ANP）验证了攻击模式并非框架依赖，但在真实大规模生产环境中的表现仍有待观察。
- **效用度量**：Capability Cloaking 等攻击的效果通过良性任务效用下降间接衡量，而非直接抓取恶意行为意图；在更隐蔽或分条件触发的威胁面前，该间接度量可能低估风险。

### 局限性

原文已系统列出的局限包括：仅覆盖六种攻击，未能穷尽 A2A 协议全部漏洞；评估仅基于模拟的中等规模系统，未在真实生产级部署中运行；测试用例通过 LLM 生成，需人工专家审计以控制质量；所提议的分层防御方案（系统提示硬化、安全网关、安全协议）仅停留在指南层面，缺少集成完整防护原型后的再评估。

### 开放问题与未来方向

从本工作的发现自然延伸出几个关键研究问题：
- **全面性与自适应性**：能否构建一个覆盖更多协议攻击类型且能动态演化的安全基准，使其能够对抗适应性的敌手？
- **轻量级密码学证明**：能否在 A2A 协议核心中引入身份与声明的密码学证明（如基于零知识或证书透明的轻量签名），在不对端到端延迟产生显著影响的前提下彻底消除 AgentCard 欺骗与能力隐藏的威胁？
- **协议级安全网关**：应用层安全网关（如 NeMo）如何获得对多智能体交互拓扑与状态转换的理解，以有效检测循环依赖、资源洪水等结构化攻击，而不仅仅是审查文本内容？
- **自我保护宿主**：是否可能在宿主端实现最小权限资源限制和任务图验证，从而从根本上消除半开任务洪水和循环溢出攻击的生存空间？

这些问题的回答将决定 A2A 多智能体系统从“功能可用”走向“安全可靠”的路径。



## 原文 PDF

![[paperPDFs/ICLR_2026/A2ASecBench_A_Protocol_Aware_Security_Benchmark_for_Agent_to_Agent_Multi_Agent_Systems.pdf]]
