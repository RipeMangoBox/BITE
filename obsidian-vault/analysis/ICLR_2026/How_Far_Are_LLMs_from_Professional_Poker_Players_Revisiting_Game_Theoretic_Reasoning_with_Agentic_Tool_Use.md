---
title: "How Far Are LLMs from Professional Poker Players? Revisiting Game-Theoretic Reasoning with Agentic Tool Use"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/How_Far_Are_LLMs_from_Professional_Poker_Players_Revisiting_Game_Theoretic_Reasoning_with_Agentic_Tool_Use.pdf
openreview_forum_id: vV54ShHvGi
aliases:
- How_Far_Are_LLMs
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过集成外部博弈求解器（如CFR+）提供GTO动作和辅助数值，弥补LLM内部策略的不足。"
primary_logic: "工具集成推理（TIR）框架允许LLM在推理过程中调用统一的外部求解API，获取GTO动作和精确数值，从而显著提升博弈性能和推理质量。"
claims:
- "ToolPoker在Leduc Hold’em中对传统算法的平均得分达+6.8 mbb/hand，在Limit Texas Hold’em中达+45.0 mbb/hand，为所有LLM方法中最高。"
- "GPT-4.1-mini在Leduc Hold’em中对CFR+仅得-24 chips，而ToolPoker的对应得分为-3.0 mbb/hand，差距显著缩小。"
- "移除奖励成分R_answer后，ToolPoker在Leduc Hold’em中对CFR+的性能从-3.0骤降至-54.5，推理平均得分从1.94降至1.58。"
- "o4-mini的LLM-as-a-Judge推理评分为1.73/1.70（Leduc/Limit），虽为最强LLM但仍远离专业水平（2.0），且在知行一致性上仍存在缺陷。"
---

# How Far Are LLMs from Professional Poker Players? Revisiting Game-Theoretic Reasoning with Agentic Tool Use

> [!tip] 核心洞察
> 工具集成推理（TIR）框架允许LLM在推理过程中调用统一的外部求解API，获取GTO动作和精确数值，从而显著提升博弈性能和推理质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大语言模型离职业扑克玩家有多远？重新审视博弈论推理与智能工具使用 |
| 英文题名 | How Far Are LLMs from Professional Poker Players? Revisiting Game-Theoretic Reasoning with Agentic Tool Use |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vV54ShHvGi) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | ToolPoker |
| Dataset | Leduc Hold’em, Limit Texas Hold’em |

> [!tip] 效果简介
> - Leduc Hold’em 上，Net chip gain vs CFR+ 为 -3.0 mbb/hand (ToolPoker)，对比 -24.0 chips (GPT-4.1-mini) / -8.0 chips (o4-mini)，变化 +21.0 over GPT-4.1-mini; +5.0 over o4-mini。
> - Limit Texas Hold’em 上，Net chip gain vs DeepCFR 为 -5.0 mbb/hand (ToolPoker)，对比 -205.0 chips (GPT-4.1-mini) / -117.0 chips (o4-mini)，变化 +200.0 over GPT-4.1-mini; +112.0 over o4-mini。
> - Leduc Hold’em 上，Avg. LLM-as-a-Judge reasoning score (HR/FA/AC) 为 1.97 / 1.94 / 1.95 (ToolPoker)，对比 1.80 / 1.56 / 1.85 (o4-mini)，变化 +0.17 / +0.38 / +0.10。

## 概述

### 问题瓶颈

大语言模型（LLM）在扑克等不完美信息博弈中面临三重结构性缺陷：**启发式依赖**——模型倾向于使用简单的经验规则而非精确的博弈论推导；**事实误解**——对牌面权益和对手范围的估计存在系统性错误；**知行不一致**——推理过程与最终动作之间缺乏逻辑一致性。这些缺陷的根源在于LLM无法自主进行精确的博弈论优化（GTO）推导，导致其面对均衡求解器时出现显著性能差距。例如，GPT-4.1-mini在Leduc Hold’em中对CFR+的净筹码损失高达-24 chips（Table 1），而o4-mini虽为最强LLM推理基线，其LLM-as-a-Judge推理评分也仅为1.73/1.70（Leduc/Limit），远未达到专业水平（2.0）。

### 核心方法：ToolPoker

针对上述瓶颈，本文提出**ToolPoker**——一个工具集成推理（Tool-Integrated Reasoning, TIR）框架。其核心调控机制是通过统一的外部求解器API，在推理过程中为LLM提供GTO动作和精确数值（如权益、范围分布），弥补模型内部策略的不足。方法包含四个关键模块：

- **统一求解器接口**：将CFR+求解器、权益计算器等功能整合为单一API，每次查询返回GTO动作及辅助数值。
- **结构化推理模板**：引导LLM按`<think>`推理、`<tool>`调用求解器、`<output>`读取结果、`<answer>`输出动作的流程进行推理。
- **行为克隆阶段（BC）**：在工具调用数据集上进行监督微调，教会模型何时及如何调用外部工具。
- **强化学习阶段（RL）**：使用复合奖励函数（答案正确性 + 格式符合度 + 工具调用成功度）通过PPO进行策略优化。

### 核心结论

ToolPoker在游戏性能和推理质量上均取得显著提升：

- **游戏性能**：在Leduc Hold’em中，ToolPoker对CFR+的净筹码损失仅为-3.0 mbb/hand，相比GPT-4.1-mini的-24 chips和o4-mini的-8 chips大幅缩小差距；在Limit Texas Hold’em中，对DeepCFR的损失为-5.0 mbb/hand，而GPT-4.1-mini和o4-mini分别为-205和-117 chips（Table 5）。
- **推理质量**：ToolPoker在Leduc Hold’em上的LLM-as-a-Judge推理评分达到1.97/1.94/1.95（HR/FA/AC），较o4-mini的1.80/1.56/1.85全面提升（Figure 2a）。
- **消融验证**：移除答案正确性奖励（R_answer）后，ToolPoker对CFR+的性能从-3.0骤降至-54.5，推理平均分从1.94降至1.58，证实了该组件的关键作用（Table 9, Table 10）。

### 方法定位与局限性

ToolPoker属于**工具增强的LLM推理**范式，与纯内部策略的LLM基线（如GPT-4o、o4-mini）和传统博弈求解器（如CFR+、DeepCFR）形成互补。其局限性在于：面对均衡求解器时仍略微落后，无法完美逼近纳什均衡；依赖预训练的CFR求解器，对无已知求解器或状态空间极大的游戏难以直接迁移；当前仅在有限种类的扑克环境中验证，尚未拓展至无限制德州扑克等更复杂场景。

## 背景与动机

### 不完美信息博弈与扑克

扑克是典型的不完美信息博弈，其核心挑战在于玩家无法直接观测对手的私有信息（手牌），必须在信息不对称的条件下进行序贯决策。从博弈论视角看，扑克可以被形式化为部分可观测马尔可夫决策过程（POMDP）：在时刻 $t$，真实状态 $s^t = \{s_{pub}^t, s_{pri(i)}^t, s_{pri(-i)}^t\}$ 包含公共信息和双方私有手牌，而玩家 $i$ 仅能获得部分观测 $o_i^t = (s_{pub}^t, s_{pri(i)}^t)$，并基于历史 $h_i^t$ 选择动作以最大化累积收益 $\sum_{t=1}^{T} r_i^t$。

博弈论最优（Game-Theoretic Optimal, GTO）策略的目标是收敛至纳什均衡——即满足 $U_i(a_i^*, a_{-i}^*) \geq U_i(a_i, a_{-i}^*), \forall a_i \in \mathcal{A}_i$ 的策略组合，在该状态下任何单方面偏离都无法获得更高收益。传统方法通过反事实遗憾最小化（CFR）及其变体（如 **CFR+**，Tammelin 2014）在小型博弈中精确求解纳什均衡，或通过 **DeepCFR**（Brown et al., 2019）等深度学习方法拓展至更大规模游戏。然而，这些方法依赖大量迭代计算，且难以产出人类可理解的推理过程。

### 大语言模型的博弈论推理现状

近年来，大语言模型（LLM）在数学推理、代码生成等任务中展现出强大能力，但其在博弈论推理中的表现尚未得到系统审视。初步实验揭示了一个核心瓶颈：**LLM在博弈论任务中普遍依赖启发式推理、存在事实误解和知行不一致，无法自主进行精确的GTO推导。**

具体而言，在Leduc Hold’em和Limit Texas Hold’em两个标准扑克环境中，原始LLM面对传统算法时表现惨淡。**GPT-4.1-mini**（OpenAI, 2025）对阵CFR+时净损失达-24 chips，即使是最强的推理模型 **o4-mini**（OpenAI, 2024）也仅能缩小至-8 chips（Table 1）。在更大规模的Limit Texas Hold’em中，GPT-4.1-mini对阵DeepCFR的净损失高达-205 chips，o4-mini为-117 chips。这些结果表明，单纯依靠LLM内部策略远不足以逼近均衡水平。

为进一步诊断LLM的推理缺陷，研究者引入LLM-as-a-Judge框架，从三个维度评估推理轨迹：启发式推理（HR，评估手牌阅读和对手建模）、事实对齐（FA，评估对游戏规则和统计事实的掌握）、行动-推理一致性（AC，评估推理结论与实际动作的一致性）。结果揭示了系统的能力短板：

- **o4-mini**在Leduc Hold’em中取得最高平均分1.73/2.0，但仍远离专业水平（Table 2）。
- **Qwen2.5-3B**（Qwen, 2024）的FA得分仅0.18，表明小模型对博弈事实存在严重误解。
- 即使是最强模型，AC得分（o4-mini为1.85）也未达满分，存在“知行不一致”——模型推理正确但最终动作与推理结论矛盾。

### 现有方法的缺口与本文动机

上述发现揭示了两个关键缺口：

1. **内部策略的固有局限**：LLM无法在推理过程中进行精确的博弈论计算（如权益估算、策略范围分析），这导致FA维度得分系统性偏低，且游戏性能与均衡求解器之间存在巨大鸿沟。

2. **微调方法的有限改进**：初步尝试的两阶段框架BC-RIRL（行为克隆+遗憾引导强化学习）虽能提升性能（如Qwen2.5-7B在Leduc Hold’em中对GPT-4.1-mini取得+17.0 chips，Table 3），并在HR和AC维度有所改善，但FA得分提升甚微（仅从0.87升至1.12，Table 4），表明仅靠训练信号优化无法弥补模型对博弈事实的根本性误解。

这些发现指向一个核心洞察：**通过集成外部博弈求解器提供GTO动作和辅助数值，可以弥补LLM内部策略的不足。** 这构成了本文提出ToolPoker框架的直接动机——利用LLM的工具使用能力，将精确的博弈论计算注入推理过程，从而同时提升游戏性能和推理质量。

## 核心创新

本文的核心创新在于提出 **ToolPoker**——一个工具集成推理（Tool-Integrated Reasoning, TIR）框架，其根本洞察是：LLM 在博弈论任务中的瓶颈并非“推理能力不足”，而是**无法自主进行精确的博弈论优化（GTO）推导**，普遍依赖启发式推理、存在事实误解和知行不一致。ToolPoker 通过**集成外部博弈求解器**来弥补 LLM 内部策略的这一结构性缺陷。

### 关键创新点（Changed Slots）

相对于纯 LLM 基线和先前的微调方法（如 BC-RIRL），ToolPoker 在以下四个维度上实现了根本性改变：

**1. 工具使用：从无外部调用到统一求解器 API**

基线 LLM 完全依赖内部策略进行决策，无法获取精确的 GTO 动作和数值信息。ToolPoker 设计了一个**统一工具接口**（Unified Solver Interface），将多个扑克求解器（CFR、权益计算器等）整合为单一 API，每次查询同时返回 GTO 动作和辅助数值（Sec 5.1）。这一设计简化了工具调用流程，稳定了训练过程。

**2. 推理过程：从自由形式到结构化标签**

ToolPoker 引入了标准化的工具调用模板，引导 LLM 按 `<think>`（推理）、`<tool>`（调用求解器）、`<output>`（读取结果）、`<answer>`（输出动作）的结构化流程进行操作（Tab. 21）。这种约束不仅规范了推理格式，还使模型学会“何时调用工具”和“如何解读工具返回的精确数值”。

**3. 动作来源：从纯 LLM 策略到 GTO 动作保证**

这是最关键的改变。纯 LLM 的动作选择完全基于内部知识，而 ToolPoker 通过调用 CFR 求解器获取**可证明的 GTO 动作**作为决策依据。实验证据表明，这一改变使 ToolPoker 在 Leduc Hold’em 中对 CFR+ 的差距从 GPT-4.1-mini 的 -24 chips 缩小至 -3.0 mbb/hand，在 Limit Texas Hold’em 中从 -205 chips 缩小至 -5.0 mbb/hand（Table 1, Table 5）。

**4. 训练策略：从标准提示到两阶段复合奖励训练**

ToolPoker 采用**两阶段训练策略**（Sec 5.2）：
- **行为克隆（BC）阶段**：在代码增强的工具调用数据集上进行监督微调，教会模型何时以及如何调用外部工具；
- **强化学习（RL）阶段**：使用复合奖励函数进行 PPO 优化，复合奖励由三部分组成：

$$R ( a _ { i } ^ { t } , \hat { a } _ { i } ^ { t } , \rho _ { i } ^ { t } ) = R _ { \mathrm { answer } } ( a _ { i } ^ { t } , \hat { a } _ { i } ^ { t } ) + \alpha _ { f } \cdot R _ { \mathrm { format } } ( \rho _ { i } ^ { t } ) + \alpha _ { t } \cdot R _ { \mathrm { tool } } ( \rho _ { i } ^ { t } )$$

其中 $R_{\mathrm{answer}}$ 为答案正确性奖励，$R_{\mathrm{format}}$ 为格式符合度奖励，$R_{\mathrm{tool}}$ 为工具调用成功度奖励。

消融实验揭示了各奖励组件的因果作用：**移除 $R_{\mathrm{answer}}$ 导致性能崩溃**（对 CFR+ 从 -3.0 骤降至 -54.5，推理平均分从 1.94 降至 1.58），说明答案正确性信号是 RL 阶段的核心驱动力；移除 $R_{\mathrm{format}}$ 仅轻微影响性能，主要导致格式混乱；移除 $R_{\mathrm{tool}}$ 小幅降低游戏性能和 FA/AC 分数（Table 9, Table 10）。

### 相对于 BC-RIRL 的进步

ToolPoker 的前身 BC-RIRL 虽然通过遗憾引导的强化学习（RIRL）在推理质量上有所提升（HR 达 1.93，AC 达 1.86），但其**事实对齐（FA）得分仍仅 1.12**，且游戏性能明显落后于 CFR+（Table 3, Table 4）。ToolPoker 通过引入外部求解器工具调用，直接解决了 FA 瓶颈——工具返回的精确数值替代了 LLM 内部不可靠的“事实记忆”，使推理评分全面提升至接近满分水平（HR 1.97、FA 1.94、AC 1.95，Fig. 2(a)）。

### 创新边界与局限

尽管 ToolPoker 显著缩小了与均衡求解器的差距，但仍存在以下局限：
- 面对 CFR+ 时**略微落后**（-3.0 mbb/hand），尚未完美逼近纳什均衡；
- **依赖预训练的 CFR 求解器**，对于无已知求解器或状态空间极大的游戏可能难以直接迁移；
- 训练推理数据集规模较小（约 5k 样本），可能影响长序列推理的泛化能力；
- 当前仅在有限种类的扑克环境中验证，尚未拓展到无限制德州扑克等更复杂场景。

## 整体框架

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_vV54ShHvGi/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of ToolPoker and its advantages over LLMs using internal policies*

ToolPoker 是一个工具集成推理（Tool-Integrated Reasoning, TIR）框架，其核心思想是让大语言模型在博弈推理过程中主动调用外部扑克求解器，以获取博弈论最优（GTO）动作和精确的辅助数值，从而弥补 LLM 内部策略在精确博弈推导上的不足。

### 框架总览

整个 pipeline 由三个关键模块串联而成，形成“推理—查询—决策”的闭环：

1. **结构化推理模板**：LLM 按照 `<think>` → `<tool>` → `<output>` → `<answer>` 的固定标签序列进行推理。模型先在 `<think>` 中分析当前局面，然后在 `<tool>` 中生成对求解器的调用请求，接着在 `<output>` 中读取求解器返回的结果，最后在 `<answer>` 中输出最终动作。
2. **统一求解器接口（Unified Solver Interface）**：将多个扑克求解器（如 CFR 反事实遗憾最小化求解器、权益计算器）整合为单一 API。每次查询返回 GTO 动作和辅助数值（如胜率、期望收益），简化了工具调用的复杂度，也稳定了后续训练。
3. **两阶段训练策略**：
   - **行为克隆阶段（BC）**：在代码增强的工具调用数据集上进行监督微调，教会模型何时以及如何调用外部工具。
   - **强化学习阶段（RL）**：使用复合奖励函数（答案正确性 $R_{\text{answer}}$ + 格式符合度 $R_{\text{format}}$ + 工具调用成功度 $R_{\text{tool}}$）通过 PPO 进行策略优化，使模型在保持 GTO 一致性的同时生成专业水平的推理轨迹。

### 输入输出流

- **输入**：当前牌局的部分观测信息 $o_i^t = (s_{\text{pub}}^t, s_{\text{pri}(i)}^t)$，即公共信息和玩家的私有手牌。
- **推理中间步骤**：模型在 `<think>` 中分析局面后，通过 `<tool>` 调用统一求解器接口，获取 GTO 动作建议和辅助数值。
- **输出**：最终动作 $a_i^t$，由模型在 `<answer>` 中给出，该动作结合了求解器的 GTO 建议和 LLM 的上下文推理。

### 与纯 LLM 内部策略的对比

图 1 展示了 ToolPoker 相对于纯 LLM 内部策略的优势。纯 LLM 依赖启发式推理，存在事实误解和知行不一致的问题；而 ToolPoker 通过外部求解器提供了 GTO 动作保证，将 LLM 的角色从“独立决策者”转变为“求解器增强的推理者”。

### 关键设计决策

- **统一接口而非多工具**：将多个求解器整合为单一 API，避免了 LLM 在多个工具间切换时的不稳定性，也降低了训练难度。
- **复合奖励而非单一信号**：$R_{\text{answer}}$ 确保动作正确性，$R_{\text{format}}$ 维持结构化输出，$R_{\text{tool}}$ 激励正确的工具调用行为。消融实验表明，移除 $R_{\text{answer}}$ 会导致性能骤降（对 CFR+ 从 -3.0 降至 -54.5 mbb/hand），而 $R_{\text{format}}$ 和 $R_{\text{tool}}$ 的移除影响相对较小。
- **两阶段训练而非端到端 RL**：BC 阶段提供了工具调用的基础能力，RL 阶段则在此基础上进行精细对齐，两者结合使得 ToolPoker 在 Leduc Hold’em 中对传统算法的平均得分达 +6.8 mbb/hand，在 Limit Texas Hold’em 中达 +45.0 mbb/hand，为所有 LLM 方法中最高。

## 核心模块与公式推导

### 模块一：行为克隆阶段（BC）

ToolPoker的训练分为两个阶段。第一阶段为行为克隆，其目标是在代码增强的工具调用数据集上对LLM进行监督微调，教会模型何时以及如何调用外部求解器API。该阶段使用的损失函数为标准负对数似然：

$$ \mathcal { L } _ { \mathrm { B C } } = - \mathbb { E } _ { ( h ^ { t } , a ^ { t } ) \sim \mathcal { D } _ { b } } [ \log \pi _ { \theta } ( a ^ { t } \mid h ^ { t } ) ] $$

其中，$h^t$ 表示时间步 $t$ 的历史信息，$a^t$ 为专家动作，$\mathcal{D}_b$ 为行为克隆数据集。该损失函数最小化模型策略 $\pi_\theta$ 与专家动作之间的差异，为后续工具集成推理奠定基础。

### 模块二：强化学习阶段（RL）

第二阶段采用复合奖励函数，通过PPO算法进行策略优化。复合奖励由三个组件构成：

$$ R ( a _ { i } ^ { t } , \hat { a } _ { i } ^ { t } , \rho _ { i } ^ { t } ) = R _ { \mathrm { answer } } ( a _ { i } ^ { t } , \hat { a } _ { i } ^ { t } ) + \alpha _ { f } \cdot R _ { \mathrm { format } } ( \rho _ { i } ^ { t } ) + \alpha _ { t } \cdot R _ { \mathrm { tool } } ( \rho _ { i } ^ { t } ) $$

- **$R_{\mathrm{answer}}$**：答案正确性奖励，衡量模型输出的动作 $a_i^t$ 与GTO动作 $\hat{a}_i^t$ 的一致性。
- **$R_{\mathrm{format}}$**：格式符合度奖励，评估推理轨迹 $\rho_i^t$ 是否遵循结构化标签（`<think>`、`<tool>`、`<output>`、`<answer>`）。
- **$R_{\mathrm{tool}}$**：工具调用成功度奖励，判断是否成功调用统一求解器API并获取有效结果。
- **$\alpha_f, \alpha_t$**：控制各奖励组件权重的超参数。

消融实验证实，$R_{\mathrm{answer}}$ 是最关键的组件——移除该奖励后，ToolPoker在Leduc Hold’em中对CFR+的性能从-3.0骤降至-54.5，推理平均得分从1.94降至1.58（参见Table 9和Table 10）。移除 $R_{\mathrm{format}}$ 主要导致输出格式混乱，对游戏性能影响轻微；移除 $R_{\mathrm{tool}}$ 小幅降低游戏性能和事实对齐（FA）分数。

### 模块三：PPO优化目标

RL阶段使用带有裁剪机制和KL散度惩罚的PPO目标函数：

$$ \mathcal { L } _ { \mathrm { P P O } } ( \theta ) = - \mathbb { E } \Bigg[ \min \Bigg( \frac { \pi _ { \theta } } { \pi _ { \mathrm { o l d } } } A , \operatorname{clip} \Bigg( \frac { \pi _ { \theta } } { \pi _ { \mathrm { o l d } } } , 1 - \epsilon , 1 + \epsilon \Bigg) \Bigg) - \beta \mathbb { D } _ { \mathrm { KL } } ( \pi _ { \theta } \vert\vert \pi _ { \mathrm { ref } } ) \Bigg] $$

其中，$\pi_\theta$ 为当前策略，$\pi_{\mathrm{old}}$ 为旧策略，$A$ 为优势函数，$\epsilon$ 为裁剪范围，$\beta$ 控制KL散度惩罚强度，$\pi_{\mathrm{ref}}$ 为参考策略。该目标在限制策略更新幅度的同时，最大化复合奖励信号的期望。

### 模块四：统一求解器接口

ToolPoker的核心创新之一是设计了一个统一工具接口，将多个扑克求解器（如CFR+、权益计算器）整合为单一API。每次查询返回GTO动作及辅助数值（如手牌权益、底池赔率），简化了工具调用流程并稳定了训练过程。模型在推理时按结构化模板执行：`<think>` 进行启发式推理 → `<tool>` 调用求解器 → `<output>` 读取返回结果 → `<answer>` 输出最终动作。该设计使得LLM能够弥补内部策略的不足，在Leduc Hold’em和Limit Texas Hold’em中分别达到+6.8和+45.0 mbb/hand的平均得分（参见Table 5），为所有LLM方法中最高。

## 实验与分析

### 核心瓶颈：LLM的三大系统性缺陷

在未引入外部工具的情况下，所有LLM在扑克博弈中均暴露出三个系统性缺陷，构成了其与职业玩家之间的根本差距：

1. **启发式推理**：LLM倾向于依赖表面化的经验法则（如“手牌强就加注”）而非进行精确的数学计算，缺乏对底池赔率、隐含赔率等核心概念的量化分析。
2. **事实误解**：模型频繁错误解读公共牌面信息或对手行动序列，导致在关键决策点出现严重偏差。例如，**Qwen2.5-3B**在Leduc Hold’em中的事实对齐得分仅为0.18/2.0（Table 2），几乎完全无法正确理解牌局状态。
3. **知行不一致**：即使LLM在推理过程中得出了正确的结论，其最终输出的动作仍可能与推理内容矛盾。**o4-mini**作为推理能力最强的LLM，其在Leduc Hold’em中的动作-推理一致性得分仅为1.85/2.0（Table 2），表明“知道该做什么”与“实际做什么”之间存在显著鸿沟。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_vV54ShHvGi/figures/003_Table_2.jpg]]
*Table 2: LLM-as-a-Judge score (0-2) evaluating reasoning traces of various LLMs in Leduc Hold’em and Limit Texas Hold’em. Bold and underlined numbers indicate the best and worst performance, respectively*

### 主要结果：ToolPoker的博弈性能

**ToolPoker**通过工具集成推理框架，在所有LLM方法中取得了最优的博弈表现。Table 5的核心结果如下：

- **Leduc Hold’em**：ToolPoker（Qwen2.5-7B）对传统算法的平均得分为**+6.8 mbb/hand**，远超**GPT-4.1-mini**（-24 chips vs CFR+）和**o4-mini**（-8 chips vs CFR+）。对CFR+的得分仅为**-3.0 mbb/hand**，将差距从GPT-4.1-mini的-24 chips缩小至接近均衡水平。
- **Limit Texas Hold’em**：ToolPoker的平均得分达**+45.0 mbb/hand**，对DeepCFR的得分为**-5.0 mbb/hand**。相比之下，GPT-4.1-mini对DeepCFR的得分为-205 chips，o4-mini为-117 chips，差距分别缩小了200和112 chips。

这一性能提升的关键机制在于：统一求解器API为LLM提供了精确的GTO动作和辅助数值（如权益计算、累积遗憾值），从根本上弥补了LLM内部策略在数学精确性上的不足。ToolPoker对CFR+仅略微落后（-3.0 mbb/hand），表明工具增强已使LLM接近但尚未完全达到纳什均衡水平。

### 推理质量评估

采用LLM-as-a-Judge框架从三个维度评估推理轨迹（Table 2, Table 4, Figure 2）：


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_vV54ShHvGi/figures/010_Figure_2.jpg]]
*Figure 2: Results for ToolPoker: (a) and (b) present reasoning analysis in Leduc Hold’em and Limit Texas Hold’em; (c) and (d) show ablation studies on gameplay and reasoning in Leduc Hold’em*

- **启发式推理**：ToolPoker在Leduc Hold’em中达到**1.97/2.0**，较o4-mini的1.80提升+0.17，表明工具调用使推理过程更加结构化，减少了模糊的经验判断。
- **事实对齐**：ToolPoker得分**1.94/2.0**，较o4-mini的1.56提升+0.38，这是提升幅度最大的维度。外部求解器提供的精确数值直接消除了LLM对牌局状态的事实误解。
- **动作-推理一致性**：ToolPoker得分**1.95/2.0**，较o4-mini的1.85提升+0.10。结构化标签（`<think>`、`<tool>`、`<output>`、`<answer>`）强制模型在输出动作前完成工具调用和结果解析，有效减少了知行不一致。

值得注意的是，**o4-mini**作为未使用工具的LLM中推理能力最强的模型，其平均推理得分仅为1.73/1.70（Leduc/Limit），远未达到专业水平（2.0），进一步验证了纯内部推理的局限性。

### 消融实验：复合奖励的关键作用

消融实验（Table 9, Table 10, Figure 2c-d）揭示了复合奖励函数中各组件的重要性：


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_vV54ShHvGi/figures/014_Table_9.jpg]]
*Table 9: Gameplay performance of ToolPoker and ablations in Leduc Hold’em. Qwen2.5-7B-Instruct is the backbone model*

- **移除R_answer**（答案正确性奖励）导致性能灾难性下降：对CFR+的得分从-3.0骤降至**-54.5 mbb/hand**，推理平均分从1.94降至1.58。这表明答案正确性奖励是驱动模型学习GTO动作的核心信号。
- **移除R_format**（格式符合度奖励）对博弈性能影响轻微，主要导致输出格式混乱，验证了结构化模板的辅助作用而非核心驱动作用。
- **移除R_tool**（工具调用成功度奖励）小幅降低博弈性能和FA/AC分数，说明工具调用频率和准确性的轻微退化会影响事实对齐和动作一致性。

消融结果表明，**R_answer是ToolPoker性能的因果性关键组件**，其移除会导致模型退化为类似未使用工具的LLM的性能水平。

### 失败模式与局限性

尽管ToolPoker显著缩小了与均衡求解器的差距，但仍存在以下失败模式：

1. **偶发的工具调用错误**：模型在少数情况下未能正确解析求解器返回的数值，或调用了错误的工具参数，导致动作偏离GTO策略。这是ToolPoker对CFR+仍略微落后（-3.0 mbb/hand）的主要原因。
2. **求解器依赖性**：ToolPoker的性能上限受限于预训练CFR求解器的质量。对于无已知求解器或状态空间极大的游戏，该方法难以直接迁移。
3. **训练数据规模限制**：当前推理数据集仅约5k样本，可能影响模型在长序列推理和复杂牌局中的泛化能力。
4. **环境局限性**：当前验证仅限于Leduc Hold’em和Limit Texas Hold’em两种扑克变体，尚未拓展到无限制德州扑克等更复杂的多智能体不完美信息博弈场景。

### 关键图表结论

- **Table 1**：所有原始LLM在面对CFR+时均遭受重大损失（GPT-4.1-mini: -24 chips, o4-mini: -8 chips），证实纯LLM策略无法逼近纳什均衡。
- **Table 5**：ToolPoker在所有LLM方法中取得最优博弈性能，对传统算法平均得分+6.8（Leduc）和+45.0（Limit）mbb/hand。
- **Figure 2a-b**：ToolPoker在三个推理维度上均接近满分，事实对齐的改善最为显著（+0.38 over o4-mini）。
- **Table 9**：移除R_answer导致对CFR+性能从-3.0骤降至-54.5，确认为核心因果组件。


![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_vV54ShHvGi/figures/002_Table_1.jpg]]
*Table 1: Comparison of various vanilla LLMs against different traditional algorithms trained in Leduc Hold’em and Limit Texas Hold’em environments. Each method plays 100 games with varying random seeds and alternated player positions. Results report net chip gains. In Leduc Hold’em, values range from 1 to 14 chips; in Limit Texas Hold’em, they range from 1 to 99 chips. Bold and underline indicate the best and worst performance in each column, respectively. The “Avg.” columns summarize LLMs’ mean performance across the four traditional baselines*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_vV54ShHvGi/figures/006_Table_5.jpg]]
*Table 5: Comparison of various LLM-based methods against different traditional algorithms trained in Leduc Hold’em and Limit Texas Hold’em environments. Other settings follow these in Tab. 1. Bold and underline indicate the best and worst performance in each column, respectively*

## 方法谱系与知识库定位

### 1. 方法演进脉络

ToolPoker 的提出建立在对 LLM 博弈推理能力系统性诊断的基础上。原始 LLM（如 GPT-4o、o4-mini）在扑克环境中普遍依赖启发式推理，存在事实误解（Factual Alignment 得分低至 0.18）和知行不一致（Action–Reasoning Consistency 不完美）等根本性缺陷，无法自主进行精确的博弈论优化（GTO）推导。这一诊断结果构成了方法设计的核心动机。

在此基础上，方法演进经历了两个关键阶段：

**第一阶段：BC-RIRL 的初步尝试。** 研究者首先提出了一个两阶段框架 BC-RIRL，将行为克隆（Behavior Cloning, BC）与遗憾启发的策略优化（Regret-Inspired Reinforcement Learning, RIRL）相结合。BC 阶段利用专业级推理轨迹进行监督微调，RIRL 阶段则利用预训练 CFR 求解器给出的累积遗憾值作为奖励信号，通过 PPO 进行策略优化。这一尝试虽然在启发式推理（HR）和知行一致性（AC）上取得了改善，但事实对齐（FA）的改进极为有限——BC-RIRL 的 FA 得分仅从基线的 0.87 提升至 1.12，远未达到专业水平（2.0）。这表明，仅靠内部策略优化难以克服 LLM 对博弈数值的固有误解。

**第二阶段：ToolPoker 的工具集成推理。** 针对 BC-RIRL 的瓶颈，ToolPoker 将思路从“优化内部策略”转向“集成外部求解器”。其核心创新在于工具集成推理（Tool-Integrated Reasoning, TIR）框架：设计统一的求解器 API，将 CFR 求解器、权益计算器等功能整合为单一接口，每次查询返回 GTO 动作和辅助数值；同时引入结构化推理模板（`<think>` → `<tool>` → `<output>` → `<answer>`），引导 LLM 在推理过程中显式调用外部工具。训练采用两阶段策略：先在代码增强的工具调用数据集上进行行为克隆，教会模型何时及如何调用工具；再使用复合奖励（答案正确性 + 格式符合度 + 工具调用成功度）通过 PPO 进行强化学习微调。

### 2. 与基线方法的关系

**相对于传统博弈求解器：** CFR+（Tammelin, 2014）和 DeepCFR（Brown et al., 2019）等求解器通过迭代计算收敛至纳什均衡，在博弈论意义上是最优的。ToolPoker 并不试图替代这些求解器，而是将其作为外部工具集成到 LLM 的推理流程中。实验表明，ToolPoker 对 CFR+ 的净筹码损失仅为 -3.0 mbb/hand（Leduc Hold'em），远优于纯 LLM 的 -24.0 chips，但仍略微落后于求解器本身——这意味着工具集成虽大幅缩小了差距，但偶发的工具调用错误仍使模型无法完美逼近纳什均衡。

**相对于强化学习方法：** NFSP（Heinrich & Silver, 2016）、DQN（Mnih et al., 2015）和 DMC（Zha et al., 2021b）等深度强化学习方法通过自我博弈或值函数逼近来学习策略。ToolPoker 对这些方法取得了显著优势：在 Leduc Hold'em 中平均得分为 +6.8 mbb/hand，在 Limit Texas Hold'em 中达 +45.0 mbb/hand。这一优势源于 ToolPoker 直接利用 CFR 求解器提供的 GTO 动作保证，而非从零开始探索策略空间。

**相对于纯 LLM 方法：** GPT-4.1-mini（OpenAI, 2025）、GPT-4o（Hurst et al., 2024）和 o4-mini（OpenAI, 2024）等商用 LLM 在扑克任务中表现不佳，尤其面对 CFR+ 时损失惨重（GPT-4.1-mini 在 Limit Texas Hold'em 中对 DeepCFR 损失 -205 chips）。ToolPoker 通过工具集成将这一差距缩小了 200 chips 以上。在推理质量上，ToolPoker 的 LLM-as-a-Judge 评分（HR/FA/AC 分别为 1.97/1.94/1.95）显著优于 o4-mini（1.80/1.56/1.85），接近满分 2.0。

**相对于开源 LLM：** Qwen2.5 系列（Qwen, 2024）中，3B 模型表现极差（对 NFSP 损失 -143.5 chips），72B 模型虽有改善但仍远逊于商用模型。ToolPoker 以 Qwen2.5-7B 为骨干模型，通过工具集成和两阶段训练，使其性能超越了未经微调的 72B 模型和 o4-mini，证明了工具增强比单纯扩大模型规模更有效。

### 3. 适用边界与局限

**已知局限：**

1. **对均衡求解器的依赖：** ToolPoker 的性能高度依赖预训练的 CFR 求解器。对于无已知求解器或状态空间极大的游戏（如无限注德州扑克），该方法难以直接迁移。这一依赖限制了其向更复杂多智能体不完美信息博弈的扩展。

2. **训练数据规模有限：** 工具增强推理数据集仅约 5k 样本，可能影响模型在长序列推理中的泛化能力。数据构建成本（需要专业级推理标注和程序化工具调用模板生成）也限制了该范式的广泛应用。

3. **偶发的工具调用错误：** 即使经过复合奖励优化，ToolPoker 仍存在工具调用失败或结果误读的情况，导致对 CFR+ 仍有 -3.0 至 -5.0 mbb/hand 的微小差距。消融实验表明，移除答案正确性奖励（R_answer）后性能骤降（从 -3.0 降至 -54.5），说明答案对齐是维持性能的关键。

4. **环境验证范围有限：** 当前仅在 Leduc Hold'em 和 Limit Texas Hold'em 两种有限扑克环境中验证，尚未拓展到无限注德州扑克等更复杂场景。

**适用条件：** ToolPoker 适用于存在可调用外部求解器或规则引擎的博弈环境，且求解器能提供精确的动作建议和数值辅助。对于需要实时决策且求解器计算开销过大的场景，该方法的实用性受限。

### 4. 开放问题

1. **工具调用鲁棒性：** 如何进一步减少偶发的工具调用错误，以完全消除与 CFR+ 的性能差距？是否需要在推理模板中引入更强的错误恢复机制？

2. **可扩展性：** ToolPoker 能否扩展到无限注德州扑克或其他多智能体不完美信息博弈？这需要解决求解器的可扩展性问题和更大规模训练数据的构建问题。

3. **与人类博弈数据的结合：** 当前方法主要依赖求解器提供的 GTO 策略，但 GTO 策略在面对人类对手时未必最优。该方法是否能与人类博弈数据结合，以提升对真实对手的适应能力？

4. **数据构建成本：** 如何降低构建高质量工具增强推理数据的成本？是否可以通过自动化的求解器-LLM 交互来生成训练数据，使该范式能更广泛地应用于其他领域？

## 原文 PDF

![[paperPDFs/ICLR_2026/How_Far_Are_LLMs_from_Professional_Poker_Players_Revisiting_Game_Theoretic_Reasoning_with_Agentic_Tool_Use.pdf]]
