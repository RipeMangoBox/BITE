---
title: "Gaia2: Benchmarking LLM Agents on Dynamic and Asynchronous Environments"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Gaia2_Benchmarking_LLM_Agents_on_Dynamic_and_Asynchronous_Environments.pdf
project_link: null
code_link: null
openreview_forum_id: 9gw03JpKK4
aliases:
- GBAF
- Gaia2
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "引入异步、事件驱动的环境与基于行动级写操作的验证器，使评估能真实反映智能体在时间压力、噪声和协作下的表现，并可直接用于可验证奖励的强化学习训练。"
primary_logic: "行动级细粒度验证结合异步模拟可以更准确地诊断和改善智能体在现实世界中的适用性，而此类动态基准是推动下一代实用智能体系统发展的关键。"
claims:
- "GPT-5 (high) 在总体任务上取得42.1% pass@1的最高分，但在时间敏感任务上得分为0.0%，说明推理能力与实时性之间存在根本权衡。"
- "ARE Verifier在450条人工标注轨迹上达到0.98的一致性和0.99的精确率，显著优于仅用LLM的In-context Verifier（一致性0.72）。"
- "消除生成延迟（instant模式）使GPT-5 (high)的时间分割得分从0.0%跃升至34.4%，表明推理速度是时间任务的关键瓶颈。"
- "并行工具调用（PTC）显著降低延迟和token消耗，但对任务成功率影响甚微（Δ pass@1: -6.3 ~ +3.0个百分点），证明瓶颈在于模型推理而非支架。"
---

# Gaia2: Benchmarking LLM Agents on Dynamic and Asynchronous Environments

> [!tip] 核心洞察
> 行动级细粒度验证结合异步模拟可以更准确地诊断和改善智能体在现实世界中的适用性，而此类动态基准是推动下一代实用智能体系统发展的关键。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Gaia2：在动态和异步环境中评测大语言模型智能体 |
| 英文题名 | Gaia2: Benchmarking LLM Agents on Dynamic and Asynchronous Environments |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=9gw03JpKK4) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Gaia2 Benchmark with ARE Framework |
| Dataset | 450 hand-labeled validation trajectories, Gaia2 Overall, Gaia2 Execution, Gaia2 Time |

> [!tip] 效果简介
> - 450 hand-labeled validation trajectories 上，Agreement 为 ARE Verifier: 0.98，对比 In-context Verifier (LLM only): 0.72，变化 +0.26。
> - Gaia2 Overall 上，pass@1 (%) 为 GPT-5 (high): 42.1，对比 Claude-4-Sonnet Thinking: 37.8，变化 +4.3 pp。
> - Gaia2 Execution 上，pass@1 (%) 为 GPT-5 (high): 69.2，对比 Claude-4-Sonnet Thinking: 62.1，变化 +7.1 pp。

## 概要

### 问题背景

现有大语言模型（LLM）智能体基准测试普遍采用静态或同步环境，评估方式多为最终答案匹配或终态比对，忽略了现实部署中普遍存在的异步事件、时间约束、噪声干扰与多智能体协作需求。这导致两大盲区：其一，推理能力强的模型常因思考时间过长而牺牲时效性，在时间敏感任务上系统性失败；其二，缺乏细粒度过程验证的评估无法暴露智能体在中间步骤中的因果错误与策略偏差。**GAIA**（Mialon et al., 2023）等早期基准仅依赖最终答案精确匹配，**AppWorld**（Trivedi et al., 2024）与**ToolSandbox**（Lu et al., 2025）引入了里程碑式验证但环境仍为同步驱动，**τ-bench / τ²-bench**（Yao et al., 2024; Barres et al., 2025）虽加入时序动态却未实现真正的异步独立演化。这些局限使现有评测无法诊断智能体在真实世界中“知道做什么”与“及时做到”之间的根本张力。

### 核心贡献

**Gaia2** 首次将异步事件驱动环境、行动级写操作验证、多智能体协作与可控噪声注入统一于同一基准框架。其核心方法建立在开源平台 **ARE（Agents Research Environments）** 之上，该平台提供应用（Apps）、环境（Environments）、事件（Events）、通知（Notifications）与场景（Scenarios）五层抽象，使环境可与智能体异步并行演化，并通过时间管理器调度独立事件。验证层面，**ARE Verifier** 对智能体的每一步写操作与预言机标注的最小正确序列进行拓扑匹配，强制执行一致性、因果性、时序容忍度与完整性检查，在450条人工标注轨迹上达到0.98的一致性和0.99的精确率，远超仅使用LLM判断的In-context Verifier（一致性0.72）。

### 关键发现

在涵盖执行、搜索、歧义处理、适应性、时间、噪声与多智能体协作七个能力维度的800个可验证场景上，**GPT-5 (high)** 以42.1%的整体pass@1取得最高分，但**在时间分割上得分为0.0%**——这一“逆向缩放”现象揭示了强推理模型在实时性上的根本瓶颈。消除生成延迟后，GPT-5 (high)的时间分割分数跃升至34.4%，证实推理速度而非推理能力本身是时间任务的关键约束。并行工具调用（PTC）消融实验进一步表明，支架层面的并发优化可显著降低延迟与token消耗，但对任务成功率影响甚微（Δ pass@1: -6.3 ~ +3.0个百分点），说明瓶颈根植于模型推理而非编排机制。多智能体协作（Agent2Agent）模式下，异构模型配对（如Claude 4 Sonnet主智能体 + Claude 4 Sonnet应用智能体）可取得29.3%的pass@1，显著优于同构轻量模型配对的8.5%，但强大模型的协作收益可能被协调开销抵消。

### 方法定位

Gaia2在方法谱系中处于从“静态最终答案验证”向“动态过程级验证”演进的关键节点。相较于GAIA的精确匹配、AppWorld的里程碑状态检查，以及τ-bench的同步多智能体交互，Gaia2的差异化在于四个维度：**验证粒度**从终态下沉至每步写操作；**环境动态性**从智能体驱动变为独立异步演化；**多智能体支持**从预定义角色扩展至通过消息传递的层级化任务分解；**鲁棒性测试**引入工具API异常与环境事件噪声的可控注入。这一设计使基准可直接为基于可验证奖励的强化学习（RLVR）提供逐行动级奖励信号，桥接评估与训练之间的鸿沟。

### 局限与开放问题

当前基准存在若干待解约束：顺序ReAct支架无法表达需要并发动作的时间敏感场景；验证器对等效写操作（如通过Messages还是Chat发送消息）的严格区分可能低估智能体的灵活性；Agent2Agent模式中协调开销可能抵消协作收益；推理模型丢弃中间推理步骤的设置可能非最优。开放问题包括：如何设计自适应计算策略以平衡效率与性能；如何通过并行编排建构建模并发操作；如何将标量验证奖励与偏好信号结合以处理主观任务；以及如何放宽验证器对等效动作的限制以更真实反映智能体实用性。

### 静态基准的饱和与隐忧

大语言模型（LLM）智能体在现有基准上的表现已趋于饱和。以 **GAIA**（Mialon et al., 2023）为代表的早期工作，通过最终答案的精确匹配来评估智能体在 Web 环境中的多步推理能力，但其静态、同步的评估范式存在根本性局限：环境仅在智能体主动执行操作时才会发生变化，且评估仅关注最终结果，完全忽略了中间行为轨迹的正确性。类似地，**AppWorld**（Trivedi et al., 2024）和 **ToolSandbox**（Lu et al., 2025）引入了里程碑式的状态验证，但仍运行在同步、智能体驱动的环境中，无法暴露真实部署中的关键失败模式。

这些静态基准掩盖了一个核心矛盾：**推理能力强的模型常因思考时间过长而牺牲时效性**。当环境不施加时间压力时，模型可以通过反复试错和冗长的推理链弥补能力不足，但这与真实世界中异步事件、截止期限和噪声并存的场景严重脱节。虽然 **τ-bench / τ²-bench**（Yao et al., 2024; Barres et al., 2025）和 **VendingBench**（Backlund & Petersson, 2025）开始引入时序动态和多智能体交互，但它们本质上仍以同步或智能体驱动的方式运行，未能从根本上打破“环境等待智能体”的假设。

### 核心瓶颈：异步、时间与噪声的三重缺失

现有 LLM 智能体普遍缺乏有效处理以下三类挑战的能力：

1. **异步事件处理**：真实环境中，新邮件、日历提醒、用户消息等事件会在智能体推理期间独立发生，而现有基准的环境状态仅在智能体调用工具时更新，导致评估无法反映智能体对突发事件的响应能力。
2. **时间约束与推理延迟的权衡**：强推理模型（如 GPT-5、Claude-4-Sonnet Thinking）在复杂推理任务上表现优异，但其长链推理带来的生成延迟使它们在时间敏感任务上几乎完全失效。这一“逆缩放”现象——推理能力越强、时效性越差——在静态基准中完全不可见。
3. **噪声与鲁棒性**：现有基准缺乏对工具 API 异常、无关环境事件等扰动的受控注入，无法评估智能体在非理想条件下的鲁棒性。

### 评估范式的根本缺陷

从评估方法学的角度看，现有基准存在两个深层缺陷：

- **最终答案验证的脆弱性**：仅比对最终结果无法区分“正确路径”与“侥幸成功”，也无法为强化学习提供细粒度的奖励信号。基于 LLM 的上下文验证器（In-context Verifier）虽试图缓解此问题，但在 450 条人工标注轨迹上仅达到 0.72 的一致性，精确率低至 0.53，远不足以支撑可靠的自动评估。
- **单智能体假设的局限**：真实任务往往需要多角色协作，但现有基准或完全忽略多智能体场景，或将交互限定为预定义模式，无法考察智能体通过消息传递进行动态任务分解与协作的能力。

### 本文动机

上述缺口指向一个根本需求：**构建异步、事件驱动的评估环境，并在行动级别进行细粒度验证**。Gaia2 正是在这一方向上迈出的关键一步。它建立在开源的 Agents Research Environments（ARE）平台之上，通过以下三个核心设计直接回应前述瓶颈：

- **异步事件驱动模拟**：环境拥有独立的时间管理器和事件依赖图，在智能体推理期间持续演化，真实复现时间压力和突发事件。
- **行动级写操作验证器（ARE Verifier）**：对每一次状态变更操作进行硬检查（精确参数匹配）和软检查（LLM 判断灵活内容），强制满足因果性、时序容忍度和完整性约束，同时使基准可直接用于可验证奖励的强化学习训练（RLVR）。
- **多智能体协作与噪声注入**：通过 Agent2Agent 机制支持主智能体与子智能体间的消息传递协作，并通过可配置的噪声水平注入工具异常和无关事件，系统评估鲁棒性。

正如 Figure 1 的预算缩放曲线所示，即便当前最强的模型（GPT-5 high 达到 42.1% pass@1），其性能也随预算增加迅速进入平台期，表明标准支架和现有模型仍缺少实现持续进步的关键要素。Gaia2 通过暴露这些隐藏的失败模式，为下一代实用智能体系统的发展提供了不可或缺的诊断工具。

## 核心方法与创新机理

Gaia2的核心创新在于将**异步事件驱动的环境模拟**与**行动级细粒度验证**相结合，构建了一个能暴露真实部署中关键失败模式的评测框架。相较于现有基准，它在四个关键维度上实现了根本性的设计转变。

### 从最终答案验证到行动级写操作验证

传统LLM智能体基准（如**GAIA**（Mialon et al., 2023））依赖最终答案的精确匹配，**AppWorld**（Trivedi et al., 2024）和**ToolSandbox**（Lu et al., 2025）虽引入里程碑式中间检查，却均未对智能体的完整行动轨迹进行逐步骤验证。这种“只看结果、不问过程”的方式无法诊断智能体在执行路径上的具体失败模式，也无法为强化学习提供可验证的奖励信号（RLVR）。

Gaia2提出的**ARE Verifier**将验证粒度下沉至每一次写操作：它将智能体的写行动序列与人工标注的oracle序列进行拓扑排序匹配，强制执行**一致性**（工具名称、参数精确匹配）、**因果性**（行动依赖DAG的拓扑约束）、**时序性**（时间戳容差检查）和**完备性**（所有必要写操作是否齐全）四维检查。在450条人工标注的验证轨迹上，ARE Verifier达到**0.98的一致性**和**0.99的精确率**，远超仅用LLM的In-context Verifier（一致性0.72，精确率0.53）（Table 1）。这一设计使Gaia2可直接输出标量验证奖励用于RLVR训练，这是此前基准无法提供的。

### 从同步静态环境到异步事件驱动模拟

现有基准的环境状态仅在智能体执行操作时发生改变，无法模拟真实世界中独立演化的外部事件。**τ-bench / τ²-bench**（Yao et al., 2024; Barres et al., 2025）和**VendingBench**（Backlund & Petersson, 2025）虽引入了时间动态和多智能体交互，但仍以同步或智能体驱动的方式运行。

Gaia2基于ARE平台实现了真正的**异步、事件驱动**环境：环境拥有独立的时间管理器，外部事件（如新邮件到达、日历提醒触发）按照事件依赖DAG自主调度执行，**在智能体推理期间仿真持续进行**。这一设计直接暴露了强推理模型在时间敏感任务上的根本性瓶颈——GPT-5 (high)在Time分割上得分为**0.0%**，而消除生成延迟（instant模式）后跃升至**34.4%**（Figure 8），证明推理速度而非推理能力是实时任务的关键制约。

### 从单智能体工具调用到层级化多智能体协作

Gaia2的**Agent2Agent**机制支持主智能体通过消息传递与多个应用智能体协作，实现任务的层级化分解。主智能体负责决策和子目标分配，应用智能体执行具体的工具调用序列。这种设计允许跨模型配对——实验表明，异构团队（Claude主智能体 + Llama应用智能体）的pass@1为**18.3**，显著优于全轻量团队（Llama主 + Llama应用）的**8.5**（Table 3），揭示了强决策者与轻量执行者组合的潜力。

### 从无扰评估到可控噪声注入

Gaia2引入**噪声分割**，在评估中系统性地注入工具异常（随机失败、签名变更）和无关环境事件（垃圾通知），并支持可配置的噪声强度。Claude 4 Sonnet在Gaia2-mini上从无噪声时的**31.2**降至高噪声时的**8.1**（Table 7），表明当前模型在鲁棒性方面存在显著短板，而此前基准无法量化这一维度。

综上，Gaia2通过**行动级验证 × 异步模拟 × 多智能体协作 × 噪声注入**的四维创新，将LLM智能体评测从“静态问答正确率”推进至“动态环境适用性诊断”，为下一代实用智能体系统的开发提供了关键基础设施。

### 设计动机与核心瓶颈

现有LLM智能体基准测试普遍采用静态或同步环境，仅通过最终答案匹配或末端状态比对进行评估。这种设计无法暴露真实部署中的关键失败模式：推理能力强的模型常因思考时间过长而牺牲时效性，导致时间敏感任务系统性失败；异步事件、噪声干扰与多智能体协作等现实挑战被完全忽略。Gaia2的核心洞察在于，**行动级细粒度验证结合异步模拟可以更准确地诊断和改善智能体在现实世界中的适用性**，而此类动态基准是推动下一代实用智能体系统发展的关键。

### ARE平台架构

Gaia2构建于开源的**Agents Research Environments (ARE)** 平台之上。ARE提供了一套构建异步、事件驱动基准的通用抽象，其架构如图2所示，包含五个核心模块：

- **Apps（有状态API）**：将消费者移动环境中的功能封装为可读写工具（Messages、Chat、Email、Calendar、Contacts等共12个应用、101个工具），每个工具被显式标注为读操作或写操作，为细粒度验证奠定基础。
- **Environments（环境容器）**：托管一组Apps、一个时间管理器及治理规则，与智能体和用户异步运行。环境状态可独立演化，不依赖智能体的动作触发。
- **Events（事件系统）**：一切交互（工具调用、状态变更、定时更新）均被建模为事件。事件通过绝对或相对时间戳调度，组织为依赖DAG（有向无环图），支持条件触发与并行执行。
- **Notifications（通知层）**：可配置的可观测性层，决定哪些事件被推送至智能体上下文。支持low/medium/high三种详细程度（表4），Gaia2默认使用medium级别，仅推送高优先级事件。
- **Scenarios（场景）**：由初始状态、事件DAG（包含用户请求与中间事件）和验证逻辑组成的动态轨迹。通过条件触发器扩展为多轮交互，支持环境在智能体等待期间主动推送新信息。

### 智能体编排支架

Gaia2采用模型无关的ReAct循环作为基线编排支架，并针对异步环境进行了关键增强：

1. **Pre-step钩子**：每次LLM调用前，将环境中排队的通知注入智能体上下文，确保智能体感知外部变化。
2. **Post-step钩子**：工具调用后检查终止条件，决定是否继续循环。
3. **并行工具调用（PTC）变体**：作为消融实验的替代方案，允许智能体同时发起多个工具调用。实验表明PTC可显著降低端到端延迟和token消耗（例如GPT-5 low在Execution分割上Δ -435s, Δ -5109 tokens），但对pass@1影响微弱（-6.3至+3.0个百分点），证明**瓶颈在于模型推理能力而非顺序支架**（表6）。

### ARE验证器

验证是ARE框架的核心创新。与传统最终答案匹配不同，ARE Verifier在**行动级别**对智能体的每一次写操作进行验证：

1. **轨迹匹配**：将智能体的写操作序列与人工标注的oracle序列进行拓扑排序比对。
2. **四维检查**：
   - **一致性**：工具名称、调用次数必须匹配；刚性字段（如ID）使用精确匹配，柔性字段（如文本内容）使用LLM评分器评估，并内置防攻击检查。
   - **因果性**：操作必须遵循事件DAG定义的依赖顺序。
   - **时序性**：操作需在允许的时间容差内完成。
   - **完备性**：所有必需的写操作必须全部执行。
3. **验证性能**：在450条人工标注轨迹上，ARE Verifier达到0.98的一致性和0.99的精确率，显著优于仅用LLM的In-context Verifier（一致性0.72）（表1）。

### 能力评估分类

Gaia2通过七个能力分割维度系统评估智能体（图4）：

- **Execution**：链式写操作的正确执行。
- **Search**：链式读操作的信息检索。
- **Ambiguity**：在信息不明确时主动请求澄清。
- **Adaptability**：对环境动态变化的适应性调整。
- **Time**：时间感知与截止日期管理。
- **Noise**：在工具异常和无关事件干扰下的鲁棒性。
- **Agent2Agent**：通过消息传递进行多智能体层次化协作。

### 输入输出流

1. **输入**：场景定义（初始状态 + 事件DAG + 用户任务描述），智能体通过工具接口与环境交互。
2. **运行过程**：环境异步演化，通知层选择性推送事件；智能体在ReAct循环中接收观察、推理、执行工具调用。
3. **输出**：完整的行动轨迹日志，由ARE Verifier离线或在线进行行动级验证，生成二值成功/失败判定及细粒度诊断信息。验证聚焦于写操作，避免对探索策略的过度约束，同时使基准可直接用于基于可验证奖励的强化学习（RLVR）训练。

### 3.1 ARE 平台核心抽象

Gaia2 构建于 **Agents Research Environments (ARE)** 平台之上，该平台为异步、事件驱动的智能体评测提供了五类核心抽象（Figure 2）：

1.  **Apps（有状态 API）**：封装为可读/可写工具集，供智能体与消费者移动环境交互（消息、聊天、邮件、日历、通讯录等）。每个工具调用被标记为“读”或“写”，写操作是后续细粒度验证的基础。
2.  **Environments（环境）**：托管一组 App、一个时间管理器及治理规则。环境与智能体和用户异步运行，其状态可独立于智能体的动作而演化。
3.  **Events（事件）**：表示环境中发生的一切（工具调用、状态变更、定时更新）。事件通过绝对/相对时间戳调度，并被组织为依赖 DAG，支持并发与条件执行（Figure 11）。
4.  **Notifications（通知）**：可配置的可观测层，决定哪些事件被推送至智能体上下文。支持低/中/高三种详细程度，默认使用 medium 级别，仅推送高优先级事件。
5.  **Scenarios（场景）**：由初始状态、事件 DAG（含用户请求与中间事件）及验证逻辑组成的动态轨迹。通过条件触发器扩展为多轮交互（Figure 12, Figure 16）。

### 3.2 智能体编排支架

所有模型使用统一的**模型无关 ReAct 循环**，并针对异步环境进行了增强：

-   **Pre-step 钩子**：在每次 LLM 调用前，将环境中排队的通知注入智能体上下文。
-   **Post-step 钩子**：在工具调用后检查终止条件。
-   **并行工具调用（PTC）**：作为消融实验的替代方案，允许智能体在一次推理中发起多个独立工具调用，以降低端到端延迟和 token 消耗，但对任务成功率影响微弱（Table 6）。

### 3.3 ARE Verifier 验证机制

验证器是 Gaia2 区别于静态基准的核心组件，它基于**写操作级别的轨迹匹配**，而非仅比较最终答案或终态。

**验证维度**：
-   **一致性（Consistency）**：工具名称与调用次数必须匹配；参数验证中，刚性字段（如 ID）采用精确匹配，柔性字段（如文本内容）采用 LLM 评分准则，并包含反注入检查以防止验证器被欺骗（Figure 17）。
-   **因果性（Causality）**：智能体的写操作序列必须满足 Oracle 事件 DAG 的拓扑排序约束。
-   **时效性（Timing）**：写操作必须在指定的时间容差窗口内完成。
-   **完备性（Completeness）**：所有必需的写操作必须被覆盖，无遗漏。

**验证流程**：将智能体的写操作轨迹与人工标注的 Oracle 序列进行匹配。对于无法精确匹配的柔性内容，调用 LLM 作为软判断器；对于刚性约束，执行硬检查。该设计使验证器可直接输出标量奖励，适用于**可验证奖励的强化学习（RLVR）** 训练。

### 3.4 关键公式

Gaia2 中唯一显式给出的公式用于预算-性能缩放曲线的计算：

$$ \sum \mathbb{1} \{ \text{scenario result} = \text{True} \land \text{scenario cost} < \text{max budget} \} $$

**变量含义**：
-   $\text{scenario result}$：单个场景的通过状态（布尔值）。
-   $\text{scenario cost}$：完成该场景所消耗的 API 调用成本（美元）。
-   $\text{max budget}$：预设的最大预算阈值。

该公式对每个最大预算值，统计成功完成且成本低于该预算的场景总数，用于绘制 Figure 1 中的预算-性能缩放曲线，揭示模型在不同成本约束下的能力上限与平台效应。

## 实验与关键发现

### 主结果：能力分化与根本权衡

Gaia2 在 7 个能力维度上对 14 个主流 LLM 进行了系统评测，所有模型均使用相同的 ReAct 支架、temperature=0.5、≥128K 上下文、16K token 生成上限，每个场景运行 3 次以保证统计稳定性。

**Table 2** 报告了各模型在各能力分割上的 pass@1 得分。GPT-5 (high) 以 42.1% 的总体得分领先，Claude-4-Sonnet Thinking 以 37.8% 紧随其后，开源模型中 Kimi-K2 以约 21% 居首。然而，总体排名掩盖了各模型在不同能力维度上的显著分化（**Figure 5** 对各能力独立重排名）：

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_9gw03JpKK4/figures/006_Table_2.jpg]]
*Table 2: Pass@1 scores on Gaia2 scenarios per model and capability split. All models are evaluated with the same baseline ReAct scaffolding described in Section 3 and with three runs to account for potential variance. The overall score is the average across splits*

- **Execution（执行链式写操作）**：GPT-5 (high) 达到 69.2%，Claude-4-Sonnet Thinking 为 62.1%，表明强推理模型在需要多步状态变更的任务上具有明显优势。
- **Time（时间敏感任务）**：GPT-5 (high) 得分为 0.0%，而 Claude-4-Sonnet Thinking 也仅为 8.5%。这是最关键的失败模式——推理能力越强的模型，思考时间越长，越容易错过截止时间，呈现出**逆向缩放**（inverse scaling）现象。
- **Adaptability（动态适应）**：Claude-4-Sonnet Thinking 以 42.1% 领先，GPT-5 (high) 为 40.4%，说明处理环境异步变化的能力与纯推理强度并非线性相关。
- **Noise（噪声鲁棒性）**：GPT-5 (high) 以 51.9% 领先，但所有模型在高噪声下均显著退化（见下文消融分析）。

**Figure 1** 的预算缩放曲线揭示了更深层的瓶颈：所有模型在 $2–$10 的预算区间后均出现平台效应，即使无限增加预算也无法持续提升成功率。这表明当前的标准支架和模型缺少实现持续进步的关键要素。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_9gw03JpKK4/figures/001_Figure_1.jpg]]
*Figure 1: Gaia2 budget scaling curve: for each max budget, we plot $\textstyle \sum \mathbb { 1 } {scenario result = True ∧ scenario cost < max budget}$. Equipped with a simple ReAct-like scaffold (see Section 3), no model evaluated here dominates across the intelligence spectrum—each trades off capability, efficiency, and budget. At equal cost, some models fare better, yet all curves plateau, suggesting that standard scaffolds and/or models miss ingredients for sustained progress. Cost estimates from Artificial Analysis model pricing data (accessed September 10, 2025)

**Figure 6** 进一步量化了成本-性能-时间的三角权衡：Claude 4 Sonnet 的成本约为 GPT-5 (low) 的 3 倍，但运行速度更快；人类在时间效率上仍远超所有模型。**Figure 7** 显示 pass@1 与工具调用次数和输出 token 量呈正相关，强调了探索行为的重要性，但 Claude 4 Sonnet 以极高的 token 消耗处于 Pareto 前沿之外。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_9gw03JpKK4/figures/017_Figure_7.jpg]]
*Figure 7: Left: Gaia2 pass@1 versus average model calls per scenario. The performance of models is highly correlated to the number of tool calls, emphasizing the importance of exploration. Right: Gaia2 pass@1 score versus average output tokens per scenario (log scale). Claude 4 Sonnet, while costing a lot exists beyond the Pareto frontier*

### 验证器可靠性

**Table 1** 在 450 条人工标注轨迹上对比了 ARE Verifier 与纯 LLM 的 In-context Verifier：

| 指标 | In-context Verifier | ARE Verifier |
|------|---------------------|--------------|
| Agreement | 0.72 | **0.98** |
| Precision | 0.53 | **0.99** |
| Recall | 0.83 | **0.95** |

ARE Verifier 通过拓扑排序对比智能体写操作与 oracle 序列，强制执行一致性、因果性、时序性和完整性检查，其 0.99 的精确率和 0.98 的一致性为基准评测提供了可靠基础。**Table 5** 的补充实验表明，ARE Verifier 在不同后端模型上均保持高性能，验证了其鲁棒性。

### 关键消融实验

#### 推理速度是时间任务的瓶颈

**Figure 8** 的 instant 模式消融直接证明了这一假设：消除生成延迟后，GPT-5 (high) 在 Time 分割的得分从 0.0% 跃升至 34.4%，其他模型的提升同样显著。这说明当前推理模型的思考时间与实时性要求之间存在根本冲突——模型并非缺乏时间推理能力，而是推理过程本身消耗了过多时间。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_9gw03JpKK4/figures/019_Figure_8.jpg]]
*Figure 8: Left: Pass@1 on Gaia2-Time in default vs. instant. Right: Inverse scaling on Time—reasoning-heavy models are slower and miss deadlines*

#### 并行工具调用改善效率但未提升性能

**Table 6** 对比了 ReAct 与 Parallel Tool Calling (PTC) 支架在 3 个模型上的表现。PTC 显著降低了端到端延迟和 token 消耗（例如 GPT-5 low 在 Execution 上 Δ -435s, Δ -5109 tokens），但对 pass@1 的影响微弱（-6.3 至 +3.0 个百分点）。这一结果直接证明：**瓶颈在于模型推理能力本身，而非顺序支架的调用效率**。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_9gw03JpKK4/figures/033_Table_6.jpg]]
*Table 6: Ablations of 3 models with Parallel TC vs ReAct scaffold. Values indicate the net contribution of PTC over ReAct (∆)*

#### 噪声鲁棒性的脆弱性

**Table 7** 展示了 Claude-4 Sonnet 在 Gaia2-mini 上随噪声强度变化的性能退化：无噪声时 pass@1 为 31.2，低噪声时意外升至 35.0（可能因噪声触发了更谨慎的行为），但在高噪声下骤降至 8.1。这表明当前模型对工具 API 异常和无关环境事件的鲁棒性严重不足。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_9gw03JpKK4/figures/035_Table_7.jpg]]
*Table 7: Model performance on Gaia2-mini across different noise levels. *Default setting*

#### 多智能体协作的异质性收益

**Table 3** 的跨模型 Agent2Agent 实验揭示了异质团队的价值：Claude 4 Sonnet 主智能体 + Claude 4 Sonnet 应用智能体达到 29.3% pass@1，而 Llama 4 Maverick 同质配对仅为 8.5%。当强主智能体搭配轻量执行者（Claude-main + Llama-app）时，得分为 18.3%，显著优于全轻量团队。**Figure 10** 进一步显示，增加协作者比例（提高 Agent2Agent ratio r）可改善 Llama 4 Maverick 的 pass@k 缩放规律，但未能改善 Claude 4 Sonnet 的成本归一化性能——强模型的协调开销可能抵消协作收益。


### 主要失败模式

1. **时间敏感性失败**：推理模型因思考时间过长而错过截止时间，这是当前最突出的失败模式，在 Time 分割上表现为逆向缩放。
2. **噪声干扰崩溃**：高噪声环境下模型性能急剧下降（从 31.2 降至 8.1），表明缺乏对工具异常和无关事件的鲁棒过滤机制。
3. **协作开销**：Agent2Agent 模式下，强模型（Claude 4 Sonnet）未能从增加协作者中获益，层级化分解的协调成本可能超过其收益。
4. **探索-利用失衡**：性能与工具调用次数正相关，但预算缩放曲线的平台效应表明，单纯的探索增加无法突破性能上限。
5. **验证器等效动作限制**：ARE Verifier 假定不存在等效的写操作路径（如通过 Messages 还是 Chat 发送消息被视为不同），可能低估了智能体的实际灵活性。

## 定位与知识库关联

### 1. 与现有基准的关系

Gaia2 的核心贡献在于将智能体评估从静态、同步的最终答案匹配范式推进到异步、事件驱动的行动级验证范式。为理解这一跃迁，需要将其置于现有基准的演进脉络中。

**静态最终答案基准**：**GAIA**（Mialon et al., 2023）是代表性工作，它通过精确匹配最终答案来评估智能体的网页浏览和工具使用能力。其根本局限在于：仅检查终点状态，完全忽略了智能体在达成目标过程中是否采取了合理、高效的路径。例如，一个智能体可能通过暴力穷举而非推理来找到答案，这在 GAIA 的评估框架下无法被诊断。

**状态验证基准**：**AppWorld**（Trivedi et al., 2024）和 **ToolSandbox**（Lu et al., 2025）引入了里程碑式的中间状态检查，部分弥补了路径不可见的问题。然而，它们的环境仍是同步的——环境仅在智能体执行动作时发生变化。这意味着，它们无法模拟真实世界中独立于智能体运行的外部事件（如新邮件到达、日历提醒触发），也无法评估智能体对时间压力和异步中断的响应能力。

**引入时间动态的基准**：**τ-bench / τ²-bench**（Yao et al., 2024; Barres et al., 2025）和 **VendingBench**（Backlund & Petersson, 2025）开始引入时间动态和多智能体交互，但本质上仍是智能体驱动的：环境演化仍由智能体的行动触发，而非独立运行。Gaia2 的关键突破在于，其基于 **ARE 平台**构建的环境是**完全异步、事件驱动**的：环境拥有独立的时间管理器和事件调度器，在智能体进行推理（甚至“思考”）期间，外部事件持续发生，模拟持续演进。这一设计直接暴露了现有推理模型的根本瓶颈——长推理时间导致错过时间窗口。

### 2. 方法设计的核心变更槽位

Gaia2 相对于上述基准的方法创新可归纳为四个关键设计槽位的变更：

**验证方法：从终点匹配到行动级写操作验证**。GAIA 等基准仅检查最终答案的精确匹配。Gaia2 的 **ARE Verifier** 将验证粒度细化到每一次状态变更的写操作，与人工标注的 oracle 序列进行比对。验证涵盖四个维度：一致性（工具名称与参数匹配）、因果性（动作依赖 DAG 的拓扑顺序）、时序（动作的时间戳容差）和完备性（所有必要写操作是否执行）。在 450 条人工标注轨迹上，ARE Verifier 达到 0.98 的一致性（Agreement）和 0.99 的精确率（Precision），显著优于仅用 LLM 的 In-context Verifier（一致性 0.72）。这一细粒度验证不仅提供了更准确的诊断，还使基准可直接用于基于可验证奖励的强化学习（RLVR）训练。

**环境动态：从同步到异步事件驱动**。传统基准中，环境仅在智能体调用工具时发生状态变更。Gaia2 的环境基于 ARE 平台的事件管理器独立运行，支持绝对/相对时间戳调度、事件依赖 DAG 和条件触发。这意味着，一个日历提醒可能在智能体正在处理另一任务时到期，一封新邮件可能在智能体“思考”期间到达。这一设计是暴露“推理能力-时效性”权衡的关键因果杠杆。

**多智能体支持：从单智能体到层级化协作**。Gaia2 的 **Agent2Agent** 模式允许主智能体通过消息传递将子任务委托给应用智能体，支持层级化任务分解和跨模型配对。这超越了简单多轮对话，引入了真正的协作动态。

**噪声与鲁棒性测试**。Gaia2 的噪声分割（Noise split）向工具 API 注入随机故障和签名变更，并向环境注入无关事件（如垃圾邮件），可配置噪声强度。这测试了智能体在非理想条件下的鲁棒性，而此前的基准缺乏此类受控扰动。

### 3. 适用边界与局限

尽管 Gaia2 在评估真实性上取得了显著进步，其设计本身也引入了若干适用边界：

**顺序编排支架的表达力限制**。当前默认的 ReAct 循环是顺序的，无法表达需要在狭窄时间窗口内并发执行多个操作的时间敏感场景。例如，在收到消息后 5 秒内同时回复并设置提醒，顺序支架可能因工具调用延迟而超时。这一局限并非基准本身的问题，而是暴露了现有编排范式的不足。

**验证器的等效动作盲区**。ARE Verifier 假定不存在等效的写操作路径：如果 oracle 标注为通过“Messages”应用发送消息，而智能体通过“Chat”应用发送了相同内容，验证器会判定为失败。这低估了智能体在真实场景中的灵活性，因为用户通常不关心通过哪个渠道完成任务。

**层级化协作的协调开销**。在 Agent2Agent 模式下，即使主智能体理论上可以无限生成子智能体，协作效益可能被协调开销抵消。实验表明，增加协作者比例可提升轻量级模型（Llama 4 Maverick）的 pass@k，但未能改善 Claude 4 Sonnet 的成本归一化性能——强模型本身已能有效处理任务，额外的协调反而增加了成本。

**领域泛化性未验证**。当前 Gaia2 仅覆盖消费者移动领域（12 个应用，101 个工具），其在桌面自动化、客户支持、代码生成等其他领域的通用性有待验证。ARE 平台本身是通用的，但 Gaia2 的场景设计锚定于移动环境。

**推理模型的次优设置**。评估时丢弃了推理模型（如 GPT-5、Claude-4-Sonnet）的中间推理步骤，仅保留 (Thought, Action) 结构。此设置可能对某些模型并非最优，社区可探索替代方案以充分释放推理模型的潜力。

### 4. 开放问题

基于上述局限和实验结果，以下开放问题值得后续工作关注：

1. **自适应计算策略**：如何在简单任务上使用轻量模型，仅在必要时触发深度推理，以平衡效率与性能？预算缩放曲线（Figure 1）显示所有模型最终都趋于平台，暗示单纯增加推理预算并非可持续的改进路径。

2. **并行编排架构**：能否设计支持并发工具调用的编排支架，以建模时间敏感场景中所需的并发操作？消融实验（Table 6）表明，并行工具调用（PTC）能显著降低延迟和 token 消耗，但对成功率影响甚微——这说明瓶颈在于模型推理而非支架，但并发编排可能解锁新的策略空间。

3. **层级化分解的收益条件**：Agent2Agent 中的层级化分解在何种条件下收益大于协调开销？如何自动决定任务分配策略？跨模型配对实验（Table 3）显示异构团队（强主智能体+轻量执行者）优于同构轻量团队，但最优配对策略仍待系统研究。

4. **混合奖励信号**：如何将标量验证奖励与偏好信号相结合的混合方法应用于 RLVR 训练，以提升智能体在主观任务（如消息措辞的自然度）上的表现？当前验证器对灵活内容使用 LLM judge 进行软检查，但这种检查可能被智能体通过嵌入条件逻辑来“攻击”（Figure 17）。

5. **等效动作的宽松验证**：如何放宽验证器对等效动作的严格限制，更真实地反映智能体的实用性？这需要在不牺牲验证可靠性的前提下，定义跨应用的功能等价性。

6. **基础设施可靠性**：如何消除模型 API 的速率限制和宕机问题，提供可靠的基础设施以支持实时响应的代理系统？当前的 API 延迟和不可靠性是部署时间敏感智能体的实际障碍，而非模型能力问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Gaia2_Benchmarking_LLM_Agents_on_Dynamic_and_Asynchronous_Environments.pdf]]
