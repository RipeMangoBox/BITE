---
title: "Real-Time Reasoning Agents in Evolving Environments"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Real_Time_Reasoning_Agents_in_Evolving_Environments.pdf
project_link: null
code_link: null
openreview_forum_id: n1AvXiU2lu
aliases:
- RTRAEE
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "规划线程与反应线程之间的资源共享与协同机制，尤其是反应线程能否在最终时刻获取规划线程实时产生的部分推理轨迹。"
primary_logic: "通过双线程并行架构，令规划线程持续进行长程推理，同时让反应线程每步仅在最后时间窗口内激活，并直接读取规划线程的流式输出，从而使智能体在不打断深度思考的前提下实现毫秒级决策，有效平衡认知负荷与时间压力。"
claims:
- "AgileThinker 在所有游戏、认知负荷和时间压力条件下均一致优于所有单范式基线（反应式、规划式及其变体），且优势随任务难度和时间压力增大而扩大。"
- "反应式智能体在认知负荷增加时性能从 0.89 骤降至 0.15，而 AgileThinker 仅从 0.88 降至 0.50；规划式智能体在时间压力增大时性能从 0.92 骤降至 0.05，而 AgileThinker 从 0.90 降至 0.58，定量验证了单范式在效率-质量权衡上的失败。"
- "在基于真实挂钟时间的实验中，AgileThinker 在 Freeway/Snake/Overcooked 上分别取得 0.88/0.45/0.89，远超 Reaction 的 0.24/0.37/0.57 和 Planning 的 0.12/0.04/0.00，证明了 token-时间抽象的有效性。"
- "反应线程能够访问规划线程的部分推理轨迹是其决策质量提升的关键，案例研究显示这种实时引导帮助 AgileThinker 避免了贪婪陷阱。"
---

# Real-Time Reasoning Agents in Evolving Environments

> [!tip] 核心洞察
> 通过双线程并行架构，令规划线程持续进行长程推理，同时让反应线程每步仅在最后时间窗口内激活，并直接读取规划线程的流式输出，从而使智能体在不打断深度思考的前提下实现毫秒级决策，有效平衡认知负荷与时间压力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 动态环境中的实时推理智能体 |
| 英文题名 | Real-Time Reasoning Agents in Evolving Environments |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=n1AvXiU2lu) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | AgileThinker |
| Dataset | Real-Time Reasoning Gym (Freeway, Snake, Overcooked 平均评分), Wall-clock time: Freeway, Wall-clock time: Snake, Wall-clock time: Overcooked |

> [!tip] 效果简介
> - Real-Time Reasoning Gym (Freeway, Snake, Overcooked 平均评分) 上，Score (0-1) 为 Easy→Hard: 0.88→0.50; 32k→4k: 0.90→0.58，对比 Reactive (V3): Easy→Hard: 0.89→0.15; Planning (R1): 32k→4k: 0.92→0.05，变化 在 Hard 难度下领先 Reactive 0.35；在 4k 高压下领先 Planning 0.53。
> - Wall-clock time: Freeway 上，Score 为 0.88，对比 Reactive (V3) 0.24, Planning (R1) 0.12，变化 +0.64 over Reactive, +0.76 over Planning。
> - Wall-clock time: Snake 上，Score 为 0.45，对比 Reactive (V3) 0.37, Planning (R1) 0.04，变化 +0.08 over Reactive, +0.41 over Planning。

## 概要

**核心问题：** 现有基于大语言模型（LLM）的智能体在动态环境中面临根本性的效率-质量权衡。反应式智能体（Reactive Agent）为满足实时性而牺牲推理深度，缺乏长远规划能力；规划式智能体（Planning Agent）虽能进行多步推理，却因计算延迟无法及时响应环境变化，导致决策过时。这一瓶颈源于单一推理范式的固有局限——单一线程无法同时兼顾“深度思考”与“即时行动”。

**核心方法：** 本文提出 **AgileThinker**，一种双线程并行架构。其核心设计是令一个规划线程（Planning Thread）持续进行长程推理并流式输出思考过程，同时让一个反应线程（Reactive Thread）仅在每个环境步的最后时间窗口内激活，直接读取规划线程实时产生的部分推理轨迹来生成即时动作。这种时间共享协议使智能体在不打断深度规划的前提下实现毫秒级决策，有效平衡了认知负荷与时间压力。

**方法定位：** AgileThinker 属于并行推理智能体架构，区别于传统的单一推理线程设计。其关键创新在于**反应线程对规划线程流式输出的实时访问**——反应决策不仅基于当前环境观察，还融合了规划线程尚未完成的中间推理结果，从而在紧迫时限内做出“知情”决策。该方法在 Real-Time Reasoning Gym（涵盖 Freeway、Snake、Overcooked 三款实时游戏）上进行了验证，与反应式基线（DeepSeek-V3、DeepSeek-R1 + Budget Forcing）和规划式基线（DeepSeek-R1、DeepSeek-R1 + Code-Policy）进行了系统对比。

**主要结果：** 
- AgileThinker 在所有游戏、认知负荷和时间压力条件下均一致优于所有单范式基线，且优势随任务难度和时间压力增大而扩大。在高认知负荷下，反应式智能体性能从 0.89 骤降至 0.15，而 AgileThinker 仅从 0.88 降至 0.50；在极端时间压力（4k tokens/步）下，规划式智能体性能从 0.92 骤降至 0.05，而 AgileThinker 仅从 0.90 降至 0.58。
- 在基于真实挂钟时间的实验中，AgileThinker 在 Freeway/Snake/Overcooked 上分别取得 0.88/0.45/0.89，远超反应式的 0.24/0.37/0.57 和规划式的 0.12/0.04/0.00，验证了 token-时间抽象的有效性。
- 消融实验表明，性能提升源于认知分工而非资源堆积：即使在有限吞吐量下（并发交替推理），AgileThinker 仍大幅超越纯反应式和纯规划式基线。

**证据强度：** 核心结论由多维度实验支撑，包括受控的 token-时间模拟、真实挂钟时间验证、跨模型（DeepSeek-V3.2、Gemini-2.5-Flash）验证，以及统计显著性检验（配对 t 检验，p < 0.05）。主要局限在于实验仅基于 DeepSeek 开源模型（因其公开推理轨迹），且环境为三类特定实时游戏，向连续控制等更复杂场景的泛化有待验证。



### 动态环境中的智能体推理困境

大语言模型（LLM）驱动的智能体在静态环境中已展现出强大的推理与规划能力，但当环境在智能体思考期间持续演化时，一个根本性的瓶颈浮现：**反应速度与推理深度无法兼得**。现有的 LLM 智能体普遍采用单一推理范式——

- **反应式智能体**（Reactive Agent）在每个环境步仅基于当前观察输出一个动作，使用非思考模型或通过预算截断限制推理长度，确保及时响应。然而，这种“看到即反应”的策略缺乏长远规划能力，在认知负荷增加时性能急剧恶化：实验显示，其归一化得分从简单场景的 0.89 骤降至困难场景的 0.15（Figure 5）。
- **规划式智能体**（Planning Agent）在获得初始观察后跨多步进行深度推理，生成完整动作计划，随后在执行阶段不再思考。这种方式在时间充裕时表现优异（得分可达 0.92），但一旦时间压力增大——环境步分配的 token 预算从 32k 压缩至 4k——其得分便从 0.92 暴跌至 0.05，因为推理尚未完成环境已发生剧变，导致决策基于过时信息。

两种范式的失败模式截然不同，却指向同一个核心矛盾：**反应式智能体牺牲决策质量换取效率，规划式智能体牺牲时效性换取深度，而真实的动态环境同时要求两者**。

### 因果杠杆：推理轨迹的实时可用性

深入分析这一瓶颈的因果机制，关键杠杆并非单纯增加计算资源，而是**反应决策能否在最终时刻获取规划线程实时产生的部分推理轨迹**。在传统架构中，反应式智能体仅依赖当前观察，规划式智能体仅依赖事先冻结的完整计划——两者都缺失了“思考进行中”的中间产物。案例研究（Figure 6）揭示了一个典型场景：在 Snake 游戏中，反应式智能体贪婪地追逐最近的食物，三步后不可避免地撞向自身；规划式智能体仍在处理第一步的过时状态，默认向左移动，尽管它正确地识别出吃最近食物会导致未来碰撞。而 AgileThinker 的反应线程因能读取规划线程尚未完成的推理流，提前获知了“延迟进食可避免陷阱”的判断，从而选择向上移动至更安全的食物目标。

### 现有评估框架的失配

加剧这一困境的是，主流的 LLM 智能体评估框架（如 OpenAI Gym）假定环境在智能体推理期间静止不动（Figure 2），这使得智能体可以无限制地消耗计算时间而不受惩罚。这种静态设定掩盖了真实部署中推理延迟与决策时效之间的冲突，导致在实验室表现优异的智能体在动态场景中失效。论文提出的 Real-Time Reasoning Gym 通过引入认知负荷（cognitive load）和时间压力（time pressure）两个可控维度，首次系统性地暴露了单范式方法在效率-质量权衡上的失败（Figure 3）。

### 本文动机

基于上述分析，本文的核心动机是：**设计一种能够在毫秒级时间约束下做出知情决策，同时不打断深度思考的智能体架构**。这要求从根本上重构推理流程——不是在一个线程内顺序地“思考-行动”，而是让深度规划与即时反应在并行线程中协同进行，并通过流式推理轨迹的共享机制，使反应线程获得“正在形成的远见”。



## 核心方法与创新机理

AgileThinker 的核心创新在于通过**双线程并行架构**与**实时推理轨迹共享**，从根本上解决了单范式 LLM 智能体在动态环境中“反应速度”与“推理深度”不可兼得的瓶颈。

### 1. 瓶颈定位：单范式的效率-质量失衡

现有 LLM 智能体普遍采用单一推理范式，在动态环境中暴露出结构性缺陷：

- **反应式智能体**（如基于 DeepSeek-V3 的 Reactive Agent）每步仅依据当前观察生成动作，虽能保证及时响应，但因计算预算受限而完全缺乏长远规划能力。随着任务认知负荷增加，其性能从 0.89 骤降至 0.15（Figure 5，§4），暴露出决策质量的严重退化。
- **规划式智能体**（如基于 DeepSeek-R1 的 Planning Agent）跨多步进行深度推理后生成完整动作计划，但在执行期间不再思考，对环境变化极度迟钝。当时间压力增大时，其性能从 0.92 暴跌至 0.05（Figure 5，§4），几乎完全失效。

这一瓶颈的**因果机制**在于：单一线程的串行执行模式，使得智能体必须在“思考”与“行动”之间做出非此即彼的选择，无法在环境持续演化的条件下兼顾两者。

### 2. 核心机制：双线程并行与时间共享协议

AgileThinker 的关键创新体现为三个 **changed slots**，分别对应架构、决策依据和资源调度三个维度：

**（1）推理架构：从单线程到双线程并行**

基线方法采用单一推理线程，顺序执行思考与动作。AgileThinker 引入双线程并行设计（§3，Figure 4）：

- **规划线程（Planning Thread, P）**：持续运行深度推理模型（如 DeepSeek-R1），负责不间断地生成多步动作计划，并**流式输出**思考过程。
- **反应线程（Reactive Thread, R）**：在每个环境步末尾激活，在严格时间约束下输出一个即时动作。

这一架构使得深度规划与及时响应得以并行进行，互不阻塞。

**（2）反应决策依据：从孤立观察到知情决策**

基线反应式智能体仅基于当前观察做出决策，规划式智能体则依赖事先生成的完整计划。AgileThinker 的核心突破在于：**反应线程能够直接读取规划线程实时产生的部分推理轨迹**（§1），从而在不等待完整分析的前提下实现“知情”的实时决策。案例研究（Figure 6）显示，这种实时引导帮助 AgileThinker 避免了反应式智能体的贪婪陷阱——当反应式智能体因贪图最近食物而必然撞墙时，AgileThinker 的反应线程借助规划线程对“延迟进食以避免碰撞”的推理，选择了向上移动的安全路径。

**（3）时间共享策略：从独占资源到可调节共享**

基线方法中，单一线程占用全部环境步时间。AgileThinker 采用**时间共享协议**（§3）：规划线程在每一步全程运行，反应线程仅在最后 $T_{\mathcal{R}}$ 时间窗口占用计算资源，且满足 $T_{\mathcal{R}} \leq T_{\mathcal{E}}$（环境步时长）。超参数 $T_{\mathcal{R}}$ 控制双线程间的资源分配，为在不同任务场景下平衡规划深度与反应速度提供了可控旋钮。

### 3. 创新效果：定量验证

上述创新带来的性能提升具有统计显著性（Figure 8，配对 t 检验）：

- 在 Hard 难度下，AgileThinker 领先反应式基线 **0.35**（0.50 vs 0.15）
- 在 4k tokens/步的高压下，AgileThinker 领先规划式基线 **0.53**（0.58 vs 0.05）
- 在基于真实挂钟时间的实验中（Table 2），AgileThinker 在 Freeway/Snake/Overcooked 上分别取得 0.88/0.45/0.89，远超反应式（0.24/0.37/0.57）和规划式（0.12/0.04/0.00）

消融实验进一步证实，性能提升源于**认知分工**而非资源堆积：在有限吞吐量下（并发交替推理而非并行），AgileThinker 仍大幅超越纯反应式和纯规划式基线（Table 11，§C.5）。



![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_n1AvXiU2lu/figures/009_Figure_4.jpg]]
*Figure 4: Two parallel threads in AgileThinker*

AgileThinker 的核心架构是一个**双线程并行推理流水线**，其设计目标是在不中断深度规划的前提下实现毫秒级的环境响应。该流水线包含三个关键模块，其协作关系如 Figure 4 所示。

### 1. 规划线程（Planning Thread, P）

规划线程是一个持续运行的深度推理模块，通常由具备长链推理能力的大语言模型（如 DeepSeek-R1）驱动。其核心职责是**不间断地生成多步动作计划**，并以流式方式输出完整的思考过程（thinking traces）。在每一个环境步内，P 线程全程占用计算资源，持续进行跨步的长程推理，从而为反应线程提供前瞻性的决策依据。

### 2. 反应线程（Reactive Thread, R）

反应线程是一个在严格时间约束下运行的即时决策模块。它在每个环境步的**最后 $T_{\mathcal{R}}$ 时间窗口内激活**，接收两个关键输入：当前环境的最新观察（observation），以及规划线程 P 在此前已流式输出的**部分推理轨迹**（partial reasoning traces）。基于这两类信息，R 线程输出一个瞬时动作，确保智能体在环境步结束前做出及时响应。

### 3. 时间共享协调协议

双线程之间的资源分配由一个**时间共享协议**管理。该协议的核心规则是：在每个环境步的持续时间内，P 线程全程运行而不被 R 线程阻塞；R 线程仅在最后 $T_{\mathcal{R}}$ 时间单位内获得计算资源。这一设计的因果调节变量（causal knob）是超参数 $T_{\mathcal{R}}$，它直接控制规划与反应之间的资源权衡——$T_{\mathcal{R}}$ 越大，反应线程获得的推理预算越充足，但会相应压缩规划线程在该步末端的有效运行时间。

### 输入输出流

整个流水线的数据流可概括为以下循环：

1. **环境步开始**：环境状态更新，P 线程继续其流式推理过程。
2. **时间窗口末端**：在距环境步结束 $T_{\mathcal{R}}$ 时刻，R 线程被激活，接收当前观察与 P 线程的实时输出。
3. **动作输出**：R 线程在 $T_{\mathcal{R}} \leq T_{\mathcal{E}}$ 的约束下生成动作，提交至环境。
4. **环境步结束**：环境执行动作并进入下一状态，P 线程无缝衔接至下一步的推理。

### 与传统范式的关键差异

| 设计维度 | 单范式基线 | AgileThinker |
|---------|-----------|-------------|
| 推理架构 | 单一推理线程，顺序执行思考与动作 | 双线程并行：P 持续推理，R 仅在末端激活 |
| 反应决策依据 | 仅基于当前观察（反应式）或预先规划的完整计划（规划式） | 基于当前观察 + P 线程的实时部分推理轨迹 |
| 时间共享策略 | 单一线程占用全部环境步时间，或固定预算限制 | 时间共享协议：P 全程运行，R 仅在 $T_{\mathcal{R}}$ 窗口占用资源 |

这一架构的关键创新在于：反应线程能够**在不等待完整分析的前提下获取规划线程的实时推理引导**，从而在认知负荷与时间压力之间实现动态平衡。案例研究（Figure 6）表明，这种实时引导帮助 AgileThinker 在 Snake 等游戏中避免了贪婪陷阱——当反应式智能体因短视而追逐最近食物导致碰撞时，AgileThinker 的反应线程因读取到规划线程关于“延迟进食可避免未来碰撞”的推理片段，选择向上移动至更安全的食物目标。



### 3.1 解码时间抽象与时间压力形式化

在真实世界中，智能体对环境变化的感知与响应速度受限于其计算延迟。为在模拟中可复现地刻画这一约束，论文将 LLM 的解码时间建模为输出 token 数的线性函数：

$$T = N_T \times \mathrm{TPOT}$$

其中 $N_T$ 为生成的 token 总数，$\mathrm{TPOT}$（Time Per Output Token）为每输出 token 的平均耗时。该建模的合理性得到了实验验证：在 DeepSeek 官方 API 上，实测 token 数与挂钟时间之间呈现极强的线性相关性（$R^2 = 0.9986$），线性拟合形式为 $T = \alpha N + \beta_{\ell}$（$\alpha = 0.0473$ s/token）。

基于此抽象，Real-Time Reasoning Gym 将时间压力形式化为：环境每经过 $N_{T_\mathcal{E}}$ 个智能体生成 token 便执行一步。若智能体未能在时限内输出有效动作，环境将以默认动作（DEFAULT ACTION）推进，从而模拟现实部署中因计算延迟导致的“失机”代价。

### 3.2 反应式与规划式基线的形式约束

为建立可比较的基线，论文对两种单范式智能体施加了统一的 token 预算约束。

**反应式智能体**（Reactive Agent）在每个环境步均需输出一个动作，其 token 预算严格受限于环境步长：

$$\bar{N_i} \leq \bar{N_{T_\varepsilon}}$$

其中 $\bar{N_i}$ 为第 $i$ 步的生成 token 数，$\bar{N_{T_\varepsilon}}$ 为环境步分配的 token 预算。该约束迫使反应式智能体在极有限的计算资源下做出决策，牺牲了深度推理的可能性。

**规划式智能体**（Planning Agent）则跨多步生成完整动作计划，然后执行期间不再思考。其核心脆弱性在于：当环境在执行阶段发生意外变化时，预设计划即刻失效，而智能体无法及时重新推理。

### 3.3 AgileThinker 的双线程并行架构

AgileThinker 的核心设计是引入两个并行运行的 LLM 线程，通过认知分工同时满足及时响应与深度规划的需求（Figure 4）。

**规划线程 P（Planning Thread）**：运行具备深度推理能力的模型（如 DeepSeek-R1），在每一步中不间断地进行长程规划，并流式输出其思考过程。P 不直接输出执行动作，而是生成对当前全局态势的分析与多步前瞻策略。

**反应线程 R（Reactive Thread）**：在严格的时间约束下运行，其运行时间 $T_{\mathcal{R}}$ 必须不超过环境步长 $T_{\mathcal{E}}$：

$$T_{\mathcal{R}} \leq T_{\mathcal{E}}$$

R 在每个环境步的末尾时间窗口内激活，接收两项输入：（1）最新的环境观察；（2）规划线程 P 截至此刻已流式输出的部分推理轨迹。基于这两类信息，R 输出一个即时动作。

### 3.4 时间共享协调协议

双线程之间的资源分配遵循时间共享协议：在每个环境步内，P 全程持续运行；R 仅在最后的 $T_{\mathcal{R}}$ 时间单位内激活并占用计算资源。这一设计的精妙之处在于：P 的深度推理过程不会因 R 的动作生成而被阻塞或打断，同时 R 总能在决策前获取 P 的最新推理进展。

超参数 $T_{\mathcal{R}}$ 控制了两个线程之间的资源权衡——增大 $T_{\mathcal{R}}$ 赋予反应线程更多计算资源以生成更优的即时决策，但会压缩规划线程的有效运行时间。论文通过消融实验（Figure 7）揭示了 $T_{\mathcal{R}}$ 对应的 token 预算 $N_{T_{\mathcal{R}}}$ 的最优取值规律：当 $N_{T_{\mathcal{R}}}$ 接近 R 的自然 token 用量的 CDF 上界时，性能达到峰值；预算过小会导致 R 无法充分读取 P 的推理信息，过大则造成资源浪费。

### 3.5 分数归一化

为跨环境比较智能体性能，论文将原始奖励 $R$ 归一化到 $[0, 1]$ 区间：

$$S = \frac{R - R_{\min}}{R_{\max} - R_{\min}}$$

其中 $R_{\min}$ 和 $R_{\max}$ 分别为所有实验轨迹中观察到的最小和最大原始奖励。该归一化消除了不同游戏奖励尺度差异对综合评估的影响。



## 实验与关键发现

### 核心瓶颈验证：单范式智能体在动态压力下的失效模式

实验首先验证了论文的核心瓶颈假设——单一推理范式的 LLM 智能体无法在动态环境中兼顾反应速度与推理深度。Figure 5 和 Table 6-7 的完整数据揭示了两种截然不同的失效模式：


![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_n1AvXiU2lu/figures/005_Figure_5.jpg]]
*Figure 5: ★- AgileThinker (Ours) ·Max Performance of Single-Paradigm Methods ■- Reactive (V3）-+- Reactive (R1 + Budget Forcing) -- Planning (R1) O- Planning (R1 + Code-Policy)*

![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_n1AvXiU2lu/figures/019_Table_6.jpg]]
*Table 6: Complete agent performance across various cognitive load levels (Easy, Medium, Hard) with time pressure fixed at 8k tokens/step. Freeway*

**反应式智能体的认知崩溃**：基于 DeepSeek-V3 的 Reactive Agent 在认知负荷从 Easy 升至 Hard 时，Freeway 得分从 0.9551 骤降至 0.4659（Table 6），整体平均得分从约 0.89 降至 0.15（§4）。其失效根因在于缺乏前瞻性规划：在 Snake 案例中（Figure 6），反应式智能体在第 3 步贪婪地追逐最近的食物，未预见到三步后必然发生的碰撞。值得注意的是，即便使用思考模型 DeepSeek-R1 并通过 Budget Forcing 截断推理（Muennighoff et al., 2025），反应式智能体在 Hard 难度下仍因截断导致频繁输出无效动作，性能并未显著改善。


![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_n1AvXiU2lu/figures/011_Figure_6.jpg]]
*Figure 6: Thinking trajectories of different paradigms at critical steps At step 3, Reactive Agent (V3) greedily pursues the nearest food and collides inevitably after three steps. Planning Agent (R1) , still reasoning over the outdated step-1 state, defaults left. However, it correctly identifies that eating the nearest food would result in a future collision, and that its lifespan is sufficient to delay consumption. Guided by the reasoning of Reactive Thread, Planning Thread in the AgileThinker anticipates the trap and chooses to move upward toward a safer food target*

**规划式智能体的时间崩溃**：基于 DeepSeek-R1 的 Planning Agent 在时间压力从 32k tokens/步收紧至 4k 时，Freeway 得分从 0.9834 骤降至 0.1025（Table 7），整体平均得分从约 0.92 降至 0.05（§4）。其失效根因在于推理延迟导致决策与实时状态脱节：Figure 6 显示，规划式智能体在第 3 步仍在推理第 1 步的过时状态，最终输出默认左转动作，尽管其推理过程已正确识别到“吃最近食物会导致碰撞”的危险。


![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_n1AvXiU2lu/figures/022_Table_7.jpg]]
*Table 7: Complete agent performance across time pressure levels (4k to 32k tokens/step) with cognitive load fixed at Medium. Freeway*

这一对比定量验证了单范式方法在效率-质量权衡上的根本性失败：反应式牺牲决策质量换取效率，规划式牺牲时效性换取深度，而 AgileThinker 通过双线程并行架构同时规避了这两种失效模式。

### AgileThinker 的主要性能优势

**跨条件一致性优势**：AgileThinker 在所有游戏、认知负荷和时间压力条件下均一致优于所有单范式基线（Figure 1, Figure 5）。具体而言：
- 在认知负荷从 Easy 到 Hard 的变化中，AgileThinker 平均得分从 0.88 降至 0.50，而 Reactive (V3) 从 0.89 降至 0.15，优势从几乎持平扩大至 +0.35（§4）。
- 在时间压力从 32k 到 4k tokens/步的收紧中，AgileThinker 从 0.90 降至 0.58，而 Planning (R1) 从 0.92 降至 0.05，优势从 -0.02 逆转为 +0.53（§4）。

**挂钟时间验证**：为排除 token-时间抽象的潜在偏差，论文在真实挂钟时间下进行了验证实验。Table 2 显示，AgileThinker 在 Freeway/Snake/Overcooked 上分别取得 0.88/0.45/0.89，远超 Reactive (V3) 的 0.24/0.37/0.57 和 Planning (R1) 的 0.12/0.04/0.00。Figure 10 进一步证实了 token 计数与挂钟时间之间的强线性相关性（拟合公式 $T = \alpha N + \beta_{\ell}$，$\alpha=0.0473$ s/token，$R^2=0.9986$），验证了 token 作为硬件无关时间代理的有效性。


![[assets/figures/papers/paper_list_l32_https_openreview_net_forum_id_n1AvXiU2lu/figures/013_Table_2.jpg]]
*Table 2: Wall-clock time performance comparison across agent systems, confirming AgileThinker advantages persist in realworld deployment scenarios*

**跨模型鲁棒性**：在 DeepSeek-V3.2 上的实验（Table 8）进一步确认了 AgileThinker 的优势。在 High 认知负荷、8k tokens/步条件下，AgileThinker 得分 0.6352，领先 Reactive（thinking off）的 0.4659 约 +0.17，领先 Planning（thinking on）的 0.1025 约 +0.53。值得注意的是，Planning Agent 在 4k 高压下得分归零（0.0000），而 AgileThinker 仍保持 0.2266，再次验证了双线程架构在极端时间压力下的韧性。

**统计显著性**：Figure 8 的 p 值热力图显示，AgileThinker 相对于单范式基线的优势在大多数条件下具有统计显著性（$p < 0.05$），且优势随认知负荷和时间压力的增大而增大。配对 t 检验使用统计量 $t = \frac{\bar{d}}{s_d / \sqrt{n}}$（App. C.2）。

### 消融实验：双线程协同机制的关键设计要素

**反应线程 token 预算的影响**：Figure 7 展示了 AgileThinker 性能随反应线程 token 预算 $N_{T_R}$ 的变化规律。当 $N_{T_R}$ 接近反应线程自然 token 用量的上界（CDF 末端）时，性能达到峰值；预算过小导致反应线程无法充分读取规划线程的部分推理轨迹，退化为纯反应式决策；预算过大则挤占规划线程的计算资源，损害长程推理质量。这一发现揭示了双线程资源分配存在一个由任务固有计算需求决定的“甜区”。

**认知分工 vs. 资源堆积**：为排除“性能提升仅源于更多计算资源”的替代解释，论文在有限吞吐量条件下进行了消融（Table 11）。在并发交替推理（而非理想并行）模式下，AgileThinker 仍大幅超越纯反应式和纯规划式基线，表明性能提升的核心机制是认知分工——规划线程负责长程推理、反应线程负责即时决策——而非简单的资源堆积。

**动态预算调整**：为减少对手工调参 $N_{T_R}$ 的依赖，论文引入了基于 AIMD 启发式的动态预算调整机制（Table 12）。该机制无需预定义固定预算，即可达到与手工最优预算接近的性能，为实际部署中的自适应资源分配提供了可行路径。

### 案例研究：部分推理轨迹的关键引导作用

Figure 6 的案例分析直观展示了 AgileThinker 双线程协同的决策过程。在 Snake 游戏的关键第 3 步：
- **Reactive Agent (V3)**：仅基于当前观察，贪婪追逐最近食物，三步后必然碰撞。
- **Planning Agent (R1)**：仍在推理过时的第 1 步状态，输出默认左转动作；但其推理过程已正确识别“吃最近食物会导致碰撞”且“寿命足够延迟进食”。
- **AgileThinker**：反应线程读取了规划线程流式输出的部分推理轨迹（即上述关于碰撞风险和延迟进食的分析），从而预见到陷阱并选择向上移动，转向更安全的食物目标。

这一案例直接验证了核心因果机制：反应线程能够访问规划线程的部分推理轨迹是其决策质量提升的关键，使智能体在不打断深度思考的前提下实现知情的即时决策，有效避免了贪婪陷阱。

### 失败模式与局限性

尽管 AgileThinker 在整体上表现出色，实验仍揭示了若干值得关注的失败模式：
- **极端时间压力下的退化**：在 4k tokens/步的最高时间压力下，AgileThinker 在 Overcooked 上的得分仅为 0.15（Table 7），表明当反应线程的时间窗口 $T_R$ 被压缩至极小时，即便部分推理轨迹也无法被有效利用。
- **模型依赖性**：AgileThinker 的完整设计依赖于 LLM 公开推理轨迹，目前仅在 DeepSeek 模型家族上验证。其他商业模型（如 Gemini 系列）因不公开完整推理过程而无法直接应用（Figure 9 显示 Gemini-2.5-Flash 的内置预算控制功能无法精确调控响应 token 数）。
- **环境局限性**：实验环境为三类特定的离散动作空间实时游戏，可能不能涵盖连续控制、部分可观测等更复杂的真实动态场景。



## 定位与知识库关联

### 1. 核心瓶颈与因果杠杆

**真实瓶颈**：现有的单范式 LLM 智能体无法在动态环境中兼顾反应速度与推理深度。反应式智能体（Reactive Agent）因计算预算受限而缺乏长远规划能力，在认知负荷增加时性能从 0.89 骤降至 0.15（Figure 5）；规划式智能体（Planning Agent）因推理延迟而无法及时响应环境变化，在时间压力增大时性能从 0.92 骤降至 0.05。这一“效率-质量”权衡构成了动态环境中 LLM 智能体的根本性挑战。

**因果杠杆**：规划线程与反应线程之间的资源共享与协同机制，尤其是反应线程能否在最终时刻获取规划线程实时产生的部分推理轨迹。这一机制直接决定了智能体能否在不打断深度思考的前提下实现知情决策——案例研究显示，正是这种实时引导帮助 AgileThinker 避免了贪婪陷阱（Figure 6）。

### 2. 与单范式基线的结构关系

AgileThinker 的设计并非在现有方法上做增量改进，而是通过架构层面的范式融合，系统性地解决了单范式方法的结构性缺陷。

**反应式基线**包括两类变体：(a) 使用非思考模型（DeepSeek-V3）的纯反应式智能体，每环境步输出一个动作并限制 token 预算，确保及时响应但缺乏前瞻；(b) 使用思考模型但通过预算截断（Budget Forcing, Muennighoff et al., 2025）强行限制推理长度的变体，虽快速但截断常导致无操作。这两类方法的共同缺陷在于：决策依据仅限于当前观察，无法利用跨步推理来预判长期后果。

**规划式基线**同样包括两类变体：(a) 跨多步推理生成完整动作计划后不再思考的标准规划式智能体（DeepSeek-R1），对环境变化迟钝；(b) 生成代码片段自动产生动作的 Code-Policy 方法（Liang et al., 2022），在结构化任务中有效，但复杂场景下短视。这两类方法的共同缺陷在于：推理与执行分离，推理期间环境可能已发生显著变化。

AgileThinker 通过三个关键设计槽位实现了对上述基线的系统性超越：

| 设计槽位 | 单范式基线值 | AgileThinker 取值 |
|---------|-------------|------------------|
| 推理架构 | 单一推理线程，顺序执行思考与动作 | 双线程并行：规划线程持续长程推理并流式输出；反应线程在每步末尾激活，依据最新观察和规划线程的部分输出生成动作 |
| 反应决策依据 | 仅基于当前观察（反应式）或事先规划的完整计划（规划式） | 基于当前观察及规划线程实时产生的部分推理轨迹 |
| 时间共享策略 | 单一线程占用全部环境步时间，或固定预算限制 | 时间共享协议：规划线程全程运行，反应线程仅在最后 $T_{\mathcal{R}}$ 时间窗口占用计算资源 |

### 3. 知识库定位与适用边界

**方法谱系定位**：AgileThinker 处于“实时推理智能体”这一新兴交叉领域，其设计灵感源于认知科学中的双过程理论（System 1 / System 2），但在工程实现上做出了独特贡献——允许 System 1（反应线程）访问 System 2（规划线程）的实时部分推理轨迹，而非传统双过程模型中两个系统的独立运作。这一设计使 AgileThinker 区别于简单的“快慢结合”方案，形成了一种信息非对称的协同架构。

**已验证的适用条件**：
- 环境类型：离散动作空间的实时游戏（Freeway、Snake、Overcooked），其中环境状态在每个时间步独立演化
- 模型基础：DeepSeek 模型家族（V3 和 R1），利用其公开的推理轨迹实现双线程协同
- 时间抽象：token 计数作为硬件无关的时间代理，其有效性通过挂钟时间实验验证（$R^2 = 0.9986$，Figure 10）

**已知局限**（需手动验证的边界）：
1. **模型依赖**：仅基于 DeepSeek 模型进行了实验，其他商业模型因不公开推理轨迹而无法直接应用 AgileThinker 的完整设计——反应线程访问规划线程部分推理轨迹这一核心机制依赖于可获取的思维链输出。
2. **认知科学性未验证**：尚未通过严格的认知科学实验验证 AgileThinker 的双线程架构是否精确模拟了人类双过程理论。
3. **环境覆盖有限**：实验环境为三类特定的实时游戏，可能不能涵盖所有真实动态场景（如连续动作空间、部分可观测环境、多智能体竞争等）。
4. **超参数敏感性**：反应线程时间窗口 $T_{\mathcal{R}}$ 需要针对不同环境手动调节，缺乏自动化的自适应机制。

### 4. 消融洞察与失效模式

**关键消融发现**：
- **反应线程 token 预算**（$N_{T_{\mathcal{R}}}$）：性能在预算接近其自然 token 用量的上界（CDF 末端）时达到峰值；预算过小导致无法利用规划信息，过大则浪费资源（Figure 7）。
- **吞吐量独立性**：在有限吞吐量下（并发交替推理而非并行），AgileThinker 仍大幅超越纯反应式和纯规划式基线（Table 11），表明性能提升主要源于认知分工而非资源堆积。
- **动态预算调整**：引入 AIMD 启发式动态预算调整机制，可在无需预定义固定 $N_{T_{\mathcal{R}}}$ 的情况下达到与手工最优预算接近的性能（Table 12），这为自动化调参提供了可行路径。

**已知失效模式**：
- 当时间压力极端（4k tokens/步）且认知负荷为 Hard 时，AgileThinker 得分降至 0.58，虽仍远超基线（Reactive 0.15, Planning 0.05），但绝对性能仍有较大提升空间。
- 当前 LLM 自身的预算控制能力不足——如 Gemini-2.5-Flash 在设定预算下仍经常生成过量 tokens（Figure 9），这限制了 AgileThinker 向其他模型迁移时的精度。

### 5. 开放问题

1. **环境扩展**：如何将 Real-Time Reasoning Gym 扩展到更贴近现实的场景（如连续控制、多智能体竞争、部分可观测）？
2. **协同机制优化**：如何在规划线程和反应线程之间实现更高效的协同机制，减少手工调参（如 $T_{\mathcal{R}}$）的依赖？动态预算调整机制能否泛化到不同的模型架构和任务？
3. **模型能力提升**：能否利用该 Gym 训练出对时间压力具有“紧迫感”的 LLM 智能体？当前 LLM 的 token/时间控制能力不足，如何从模型层面提供精确的控制？
4. **Code-as-Policy 改进**：Code-as-Policy 方法在复杂环境中应对长期后果和上下文推理的能力如何改进？



## 原文 PDF

![[paperPDFs/ICLR_2026/Real_Time_Reasoning_Agents_in_Evolving_Environments.pdf]]
