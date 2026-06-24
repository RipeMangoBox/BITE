---
title: In-the-Flow Agentic System Optimization for Effective Planning and Tool Use
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/In-the-Flow_Agentic_System_Optimization_for_Effective_Planning_and_Tool_Use.pdf
aliases:
- AFG
- FASOEPTU
acceptance: accepted
tags:
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/multi_agent
openreview_forum_id: Mf5AleTUVK
core_operator: 采用模块化智能体系统，并将 planner 模块置于系统循环中在线优化，通过将轨迹级稀疏奖励广播到每一轮，实现有效的多轮信用分配。
primary_logic: 将多轮强化学习问题转化为一系列单轮策略更新：在每一轮，planner 基于完整的记忆上下文接收相同的全局成功信号，利用组标准化优势稳定训练，从而从稀疏反馈中学习有效的长程策略。
claims:
- Flow-GRPO 通过广播单一可验证的轨迹级奖励到每一轮，将多轮 RL 转化为单轮更新。
- 组标准化优势减少方差，增强信用分配。
- 单轮更新的等价性及单调改进保证。
- 在线 Flow-GRPO 大幅超越离线 SFT 和冻结 planner。
paradigm: 将多轮强化学习问题转化为一系列单轮策略更新：在每一轮，planner 基于完整的记忆上下文接收相同的全局成功信号，利用组标准化优势稳定训练，从而从稀疏反馈中学习有效的长程策略。
---

# In-the-Flow Agentic System Optimization for Effective Planning and Tool Use

> [!tip] 核心洞察
> 将多轮强化学习问题转化为一系列单轮策略更新：在每一轮，planner 基于完整的记忆上下文接收相同的全局成功信号，利用组标准化优势稳定训练，从而从稀疏反馈中学习有效的长程策略。

| 字段 | 内容 |
|------|------|
| 中文题名 | 在线智能体系统优化以实现有效的规划与工具使用 |
| 英文题名 | In-the-Flow Agentic System Optimization for Effective Planning and Tool Use |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=Mf5AleTUVK) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/multi_agent |
| Method | AGENTFLOW (with Flow-GRPO) |
| Dataset | Bamboogle (Search Intensive), 2Wiki (Search Intensive), HotpotQA (Search Intensive), Musique (Search Intensive) |

> [!tip] 效果简介
> - Bamboogle (Search Intensive) 上，Accuracy (%) 为 69.6，对比 59.6 (AutoGen)，变化 +10.0。
> - 2Wiki (Search Intensive) 上，Accuracy (%) 为 77.2，对比 44.0 (AutoGen)，变化 +33.2。
> - HotpotQA (Search Intensive) 上，Accuracy (%) 为 57.0，对比 54.0 (GPT-4o)，变化 +3.0。

## 概述

现有工具增强的大语言模型推理方法通常采用一体化策略：在完整的上下文轨迹中交替进行“思考”与工具调用。这种范式在长程规划、多样化工具组合和动态工具反馈面前难以稳定扩展，且推理时对未见任务和工具的泛化能力有限。与此同时，多模块智能体系统虽然结构上更灵活，却普遍缺乏在线训练机制，无法从实时交互中学习，导致在仅有最终成功信号的稀疏奖励场景下，信用分配极为困难。

针对上述瓶颈，本文提出 **AGENTFLOW**——一种可训练的“在环”智能体系统，并配套设计了 **Flow-GRPO** 在线优化算法。其核心思路是：将多轮强化学习问题转化为一系列可处理的单轮策略更新。具体而言，Flow-GRPO 将轨迹级别的单一可验证奖励广播至每一轮交互，使规划器在每一轮都能接收到相同的全局成功信号；同时引入组标准化优势来降低方差、增强信用分配，从而在稀疏反馈下稳定地学习长程策略。

在系统架构上，AGENTFLOW 由四个专门模块协作构成：**Action Planner**（可训练的策略核心，负责制定子目标并选择工具）、**Tool Executor**（执行选定工具并返回观察）、**Execution Verifier**（评估执行有效性并决定继续或终止）以及 **Solution Generator**（在循环终止时生成最终答案）。四个模块通过共享的演化记忆在多轮交互中迭代配合，仅有 Planner 模块通过 Flow-GRPO 在线优化，其余模块保持冻结。

实验覆盖搜索密集型、智能体、数学推理和科学推理四类共十个基准。以 7B 规模的 Qwen2.5-7B-Instruct 为基座，AGENTFLOW 在搜索任务上平均超越最强基线 14.9%，在智能体任务上平均超越 14.0%，在数学推理任务上平均超越 14.5%。消融实验进一步表明：Flow-GRPO 在线训练相比冻结 Planner 带来平均 17.2% 的绝对提升，而离线监督微调（SFT）则导致性能崩溃；即使将冻结 Planner 替换为更强的 GPT-4o，其增益也远不及 Flow-GRPO 训练的 7B Planner。

> **注意**：以下各节将依次展开问题背景、方法设计、实验分析及局限性讨论。本节仅做全局概览，具体细节请参见对应章节。

## 背景与动机

### 大语言模型推理的瓶颈：从单一策略到工具增强

大语言模型（LLM）在推理任务上取得了显著进展，但面对需要长程规划、多步搜索和复杂工具调用的任务时，其能力仍受限于模型内部知识的边界。工具增强推理（Tool-Integrated Reasoning, TIR）被广泛视为突破这一瓶颈的关键路径——通过让模型在推理过程中调用外部工具（如搜索引擎、代码解释器），可以动态获取新信息并验证中间结果。

然而，当前主流的 TIR 实践存在一个深层结构性缺陷：**单一策略的全上下文交错范式**。如图 3 所示，现有方法通常训练一个一体化（monolithic）策略模型，将推理步骤（如 `<think>` 块）与工具调用（如 `<tool_call>`）在单一轨迹中交错生成。这种范式面临三个根本性挑战：

1. **长程规划的稳定性问题**：随着规划步数增加，单一策略需要同时维护推理链、工具调用序列和反馈整合，上下文窗口迅速膨胀，导致策略在长程任务上容易发散。
2. **多工具协调的复杂性**：不同工具具有不同的调用接口、返回格式和可靠性特征，一体化策略难以对多样化工具进行有效编排。
3. **动态反馈的泛化困难**：工具返回的实际内容往往与训练分布存在偏差，冻结策略在推理时难以自适应调整，导致对未见任务和工具的泛化性较差。

### 模块化智能体系统的困境：在线训练的缺失

为缓解一体化范式的压力，研究者提出了模块化智能体系统（如 AutoGen），将任务分解为多个专门模块（规划器、执行器、验证器等）协同工作。这种架构天然适合处理多工具、多轮交互的场景，但现有系统普遍存在一个关键瓶颈：**缺乏在线训练能力**。

具体而言，现有智能体系统的各个模块通常以冻结的指令微调模型部署，无法从实时交互中学习和改进。这导致两个严重后果：

- **信用分配（Credit Assignment）困难**：在多轮交互中，最终成功或失败的信号需要回溯到每一轮的具体决策。长程稀疏奖励下，缺乏有效机制将全局信号合理分配到各个中间步骤。
- **策略固化与次优行为**：冻结的规划器无法根据执行反馈调整策略偏好，容易陷入重复性错误或低效的工具使用模式。例如，在搜索任务中，规划器可能反复调用相同的搜索词，即使前几次返回的信息已经充分。

### 核心动机：在系统执行流中优化规划器

本文的核心动机源于一个关键洞察：**将多轮强化学习问题转化为一系列单轮策略更新**。如果能在每一轮向规划器广播相同的全局成功信号，并利用组标准化优势稳定训练，就可以从稀疏的最终奖励中学习有效的长程策略。

基于这一动机，本文提出 AGENTFLOW——一个可训练的在线智能体系统，以及配套的 Flow-GRPO 算法。该框架直接在系统执行循环内优化规划器模块，使智能体能够从实际交互的成败中持续改进其规划和工具使用策略，从而突破冻结系统的性能天花板。

## 核心创新

AGENTFLOW 的核心创新在于将多模块智能体系统与在线强化学习深度融合，从根本上改变了工具增强推理的训练范式。其关键突破体现在三个维度。

**从一体式策略到模块化智能体系统。** 现有工具增强推理方法（如 TIR、Search-R1）通常训练单一、一体化的策略模型，在全上下文下交错进行思考与工具调用（Figure 3a）。这种范式在长规划、多样工具和动态反馈下难以稳定扩展，且推理时对未见任务的泛化性较差。AGENTFLOW 将系统分解为四个专门模块——Action Planner、Tool Executor、Execution Verifier 和 Solution Generator——通过共享的演化记忆协同工作（Figure 2）。这一模块化设计使每个组件专注于特定功能，planner 负责子目标规划与工具选择，executor 执行工具调用，verifier 评估执行有效性并输出终止信号，generator 在循环终止时基于完整记忆生成最终答案。系统的联合生成过程为：

$$p_{\theta}\Big(\{a^t, e^t, v^t\}_{t=1}^T, o \mid q, K\Big) = \left[\prod_{t=1}^T \pi_{\theta}\big(a^t \mid q, K, M^t\big) \mathcal{E}(e^t \mid a^t, K) \mathcal{V}(v^t \mid q, e^t, M^t)\right] \mathcal{G}(o \mid q, M^T)$$

**从离线训练到在线 in-the-flow 优化。** 多模块智能体系统（如 AutoGen）通常缺乏在线训练能力，各模块保持冻结，无法适应实时交互动态。AGENTFLOW 首次将 planner 模块置于系统执行循环中直接优化：在每一轮，系统使用当前策略 rollout 完整的 AGENTFLOW 流程，收集实际轨迹，并利用可验证的最终结果信号更新策略。这一"in-the-flow"训练范式使 planner 能够从真实的多轮交互反馈中学习，而非依赖静态的离线数据。

**从稀疏奖励困境到单轮信用分配。** 多轮交互中，最终奖励信号稀疏且难以分配到每一轮的具体动作，这是长程智能体优化的核心瓶颈。Flow-GRPO 算法通过两个关键机制解决此问题：首先，将单一可验证的轨迹级奖励广播到每一轮的所有动作，即 $r = R(a^t) = \bar{R}(o, q, y^*), \forall t = 1, \ldots, T$，从而将多轮 RL 问题转化为一系列可处理的单轮策略更新；其次，引入组标准化优势来减少方差并增强信用分配：

$$A_i^t = \frac{\bar{R}(o_i, q, y^*) - \mathrm{mean}\left(\{\bar{R}(o_k, q, y^*)\}_{k=1}^G\right)}{\mathrm{std}\left(\{\bar{R}(o_k, q, y^*)\}_{k=1}^G\right)}$$

这一设计使得即使在长程稀疏奖励下，planner 也能有效学习。理论分析进一步证明了单轮更新的等价性（Theorem B.1）和单调改进保证（Theorem B.3），为方法的有效性提供了形式化支撑。

消融实验（Table 3）直接验证了上述创新的关键作用：Flow-GRPO 在线训练相比冻结 planner 平均提升 17.2%，而离线 SFT 因 token 级模仿目标与轨迹级任务成功之间的错位导致性能崩溃（平均仅 19.5%）。即使使用更强的 GPT-4o 作为冻结 planner，也仅带来 5.8% 的平均增益，远低于 Flow-GRPO 训练的 7B planner（55.7% vs 44.3%），表明系统循环内的在线优化本身比模型规模更为关键。

## 整体框架

![[obsidian-vault/assets/figures/papers/iclr26_0012_Mf5AleTUVK_In-the-Flow_Agentic_System_Optimization_for_Effe/figures/002_Figure_2.jpg]]

![[obsidian-vault/assets/figures/papers/iclr26_0012_Mf5AleTUVK_In-the-Flow_Agentic_System_Optimization_for_Effe/figures/005_Figure_3.jpg]]
*Figure 3: Comparison of two paradigms of LLMs with tool use. (a) Monolithic tool-integrated reasoning models train a single policy to interleave reasoning (e.g., <think>) and tool calls (e.g., < \mathrm { t o o l . c a l 1 > } ) within a single, full-context trajectory. (b) Agentic systems decompose tasks across multiple specialized modules (e.g., planner, coder) that collaborate. These systems are typically training-free, orchestrated by handcrafted logic or prompting*

![[obsidian-vault/assets/figures/papers/iclr26_0012_Mf5AleTUVK_In-the-Flow_Agentic_System_Optimization_for_Effe/figures/006_Figure_4.jpg]]
*Figure 4: Optimization for our proposed agentic system AGENTFLOW. Given a query q, an evolving memory M, and a toolset K, the policy model generates actions that target sub-goals and select tools. It is trained via Flow-based Group Refined Policy Optimization (Flow-GRPO), which enables multi-turn reinforcement learning and stable optimization under collaborative dynamics*

AGENTFLOW 是一个可训练的在线智能体系统，由四个专门模块通过共享的演化记忆协同工作：**Action Planner**（可训练的策略 $\pi_\theta$）、**Tool Executor**、**Execution Verifier** 和 **Solution Generator**。系统在多轮交互中迭代运行，每轮的状态转移遵循统一的范式：Planner 基于当前记忆 $M^t$ 和工具集 $K$ 规划子目标并选择工具，Executor 执行工具返回观察 $e^t$，Verifier 评估执行结果并输出终止/继续信号 $v^t$，循环终止后 Generator 基于完整记忆生成最终答案 $o$。

核心设计在于将多轮工具增强推理分解为显式的模块化联合生成过程：

$$p_{\theta}\Big(\{a^t, e^t, v^t\}_{t=1}^T, o \mid q, K\Big) = \left[\prod_{t=1}^T \pi_{\theta}\big(a^t \mid q, K, M^t\big) \mathcal{E}(e^t \mid a^t, K) \mathcal{V}(v^t \mid q, e^t, M^t)\right] \mathcal{G}(o \mid q, M^T)$$

与一体式工具集成推理模型（Monolithic TIR）在全上下文下交错思考与工具调用的范式不同，AGENTFLOW 将推理链显式记录为可审计的记忆 $M$，使规划、执行和验证各阶段解耦。Planner 的指令模板（Table 5）引导其从工具集（Base Generator、Python Coder、Google Search、Wikipedia Search、Web Search）中选择最优工具；Verifier 的指令模板（Table 6）则评估累积记忆是否足以回答问题或需要继续调用工具。

训练时，仅优化 Planner 模块——系统完整 rollout 生成轨迹 $\tau = \{a^t, e^t, v^t\}_{t=1}^T$，基于最终答案正确性计算全局奖励 $r = \bar{R}(o, q, y^*)$，并将同一奖励广播到轨迹内所有轮次，通过 Flow-GRPO 算法将多轮 RL 转化为一系列单轮策略更新。Executor、Verifier 和 Generator 保持冻结，这种非对称优化设计在保证系统稳定性的同时，使 Planner 从稀疏的轨迹级反馈中学习有效的长程规划策略。

## 核心模块与公式推导

### 系统模块架构

AGENTFLOW 由四个专门模块组成，通过共享的演化记忆 $M$ 在多轮交互中协同工作：

- **Action Planner ($P$)**：可训练的策略模块 $\pi_\theta$，基于当前记忆 $M^t$ 和工具集 $K$ 制定子目标、选择工具 $k \in K$ 并提取相关上下文，输出动作 $a^t$。
- **Tool Executor ($E$)**：调用选定工具并返回执行观察 $e^t$。
- **Execution Verifier ($V$)**：评估 $e^t$ 的有效性和记忆充分性，输出二值验证信号 $v^t$，决定继续或终止循环。
- **Solution Generator ($G$)**：循环终止时基于完整记忆 $M^T$ 生成最终答案 $o$。

整个系统的联合生成过程为：

$$
p_{\theta}\Big(\{a^t, e^t, v^t\}_{t=1}^T, o \mid q, K\Big) = \left[\prod_{t=1}^T \pi_{\theta}(a^t \mid q, K, M^t) \, \mathcal{E}(e^t \mid a^t, K) \, \mathcal{V}(v^t \mid q, e^t, M^t)\right] \mathcal{G}(o \mid q, M^T)
$$

其中 $q$ 为查询，$K$ 为工具集，$T$ 为总交互轮数。记忆 $M^t$ 显式记录了规划、执行和验证的完整历史，这与一体式模型中隐式推理链形成本质区别。

### Flow-GRPO 核心公式

#### 信用分配机制

Flow-GRPO 的核心创新是将多轮强化学习转化为一系列单轮策略更新。其关键操作是将轨迹级稀疏奖励广播到每一轮：

$$
r = R(a^t) = \bar{R}(o, q, y^*), \quad \forall t = 1, \ldots, T
$$

即轨迹内所有动作获得相同的全局奖励，该奖励仅取决于最终答案 $o$ 与标准答案 $y^*$ 的可验证正确性。这解决了长程交互中信用分配的难题。

#### 组标准化优势

为减少方差并增强信用分配，Flow-GRPO 对组内轨迹奖励进行标准化：

$$
A_i^t = \frac{\bar{R}(o_i, q, y^*) - \text{mean}\big(\{\bar{R}(o_k, q, y^*)\}_{k=1}^G\big)}{\text{std}\big(\{\bar{R}(o_k, q, y^*)\}_{k=1}^G\big)}
$$

其中 $G$ 为每组采样的轨迹数。该优势值在轨迹内所有时间步保持恒定（$A_i^t \equiv A_i$），这是 Flow-GRPO 将多轮问题分解为单轮更新的理论基础。

#### 完整优化目标

Flow-GRPO 的完整目标函数为：

$$
\mathcal{T}_{\text{Flow-GRPO}}(\theta) = \mathbb{E}_{(q, y^*) \sim \mathcal{D},\, \{\tau_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{T_i} \sum_{t=1}^{T_i} \frac{1}{|a_i^t|} \sum_{j=1}^{|a_i^t|} \min\Big\{\rho_{i,j}^t A_i^t,\; \text{clip}(\rho_{i,j}^t, 1-\epsilon, 1+\epsilon) A_i^t\Big\} - \beta \, \mathbb{D}_{\text{KL}}(\pi_\theta \parallel \pi_{\text{ref}}) \right]
$$

其中 token 级重要性比率定义为：

$$
\rho_{i,j}^t = \frac{\pi_\theta(a_{i,j}^t \mid s_i^t, a_{i,1:j-1}^t)}{\pi_{\theta_{\text{old}}}(a_{i,j}^t \mid s_i^t, a_{i,1:j-1}^t)}
$$

该目标在 token 级别进行 PPO 风格的裁剪更新，并通过 KL 散度惩罚项 $\beta \, \mathbb{D}_{\text{KL}}(\pi_\theta \parallel \pi_{\text{ref}})$ 约束策略不偏离参考策略过远。

#### 理论保证

附录 B 提供了两个关键理论结果（Theorem B.1 和 Theorem B.3）：全局多轮优化目标等价于期望 token 级局部目标，且 Flow-GRPO 满足策略单调改进保证。这些结果为广播奖励到每轮并采用组标准化优势的做法提供了形式化支撑。

## 实验与分析

![[obsidian-vault/assets/figures/papers/iclr26_0012_Mf5AleTUVK_In-the-Flow_Agentic_System_Optimization_for_Effe/figures/003_Figure_1.jpg]]
*Figure 1: Left: Performance of AGENTFLOW with a 7B-scale backbone before and after Flow-GRPO tuning across ten diverse reasoning benchmarks. Flow-GRPO substantially improves performance by enhancing planning quality and tool-calling reliability. Right: AGENTFLOW achieves consistent gains over top baselines, including base LLMs, tool-integrated RL models, and trainingfree agentic systems. All 7B results use Qwen2.5-7B-Base/Instruct as the backbone and tools*

![[obsidian-vault/assets/figures/papers/iclr26_0012_Mf5AleTUVK_In-the-Flow_Agentic_System_Optimization_for_Effe/figures/007_Table_1.jpg]]
*Table 1: Accuracy comparison on search-intensive and agentic tasks. 7B-Base refers to Qwen-2.5-7B-Base and 7B-Inst refers to Qwen-2.5-7B-Instruct. AutoGen and our AGENTFLOW method are agentic systems, which use Qwen-2.5-7B-Instruct for the LLM-powered agents and tools for fair comparison. We visualize the gains of AGENTFLOW to the each baseline in the ∆ columns*

![[obsidian-vault/assets/figures/papers/iclr26_0012_Mf5AleTUVK_In-the-Flow_Agentic_System_Optimization_for_Effe/figures/008_Table_2.jpg]]
*Table 2: Accuracy comparison of mathematical and scientific reasoning tasks*

### 核心瓶颈与解决路径

现有工具增强推理方法存在两个结构性缺陷。其一，主流范式采用单一、一体化的策略模型，在全上下文下交错进行思考与工具调用，难以随长程规划、多样工具和动态工具反馈稳定扩展（Figure 3）。其二，多模块智能体系统虽能解耦任务，但缺乏在线训练机制，无法适应实时交互动态，导致长程稀疏奖励下的信用分配困难。AGENTFLOW 通过将 planner 模块置于系统循环中在线优化，并利用 Flow-GRPO 将轨迹级稀疏奖励广播到每一轮，实现了有效的多轮信用分配。

### 主实验结果

#### 搜索密集型与智能体任务

Table 1 展示了搜索密集型和智能体任务上的准确率对比。AGENTFLOW（w/ Flow-GRPO）在搜索密集型任务上平均达到 57.3%，较 AutoGen 等最优基线提升 14.9 个百分点。具体而言：在 Bamboogle 上达到 69.6%（+10.0 vs AutoGen），在 2Wiki 上达到 77.2%（+33.2 vs AutoGen），在 HotpotQA 上达到 57.0%（+3.0 vs GPT-4o），在 Musique 上达到 25.3%（+1.3 vs GPT-4o）。在智能体任务 GAIA 上达到 33.1%，较 Search-R1 提升 14.0 个百分点。

值得注意的是，AGENTFLOW 在所有搜索密集型任务上均超越了 GPT-4o，增益范围在 8.2% 至 18.0% 之间。这验证了模块化架构配合在线强化学习在长程规划与工具调用上的优势。

#### 数学与科学推理任务

Table 2 展示了数学和科学推理任务的准确率对比。AGENTFLOW（w/ Flow-GRPO）在数学任务上平均提升 14.5%：AIME24 达到 40.0%（+9.3 vs Luffy），AMC23 达到 61.5%（+1.5 vs ToRL），GameOf24 达到 53.0%（+20.0 vs 最优基线）。在科学推理任务 GPQA 和 MedQA 上分别达到 47.0%（+2.0 vs SimpleRL-reason）和 80.0%（+3.2 vs TIR），平均提升 4.1%。

Figure 1 汇总了 Flow-GRPO 训练前后 AGENTFLOW 的性能对比。训练后的 7B 模型在十个多样化推理基准上均取得显著提升，且一致超越包括 GPT-4o 在内的更大规模专有模型。

### 消融实验

#### 训练范式对比

Table 3 的消融实验揭示了训练范式的决定性影响。Flow-GRPO 在线训练的平均准确率达到 55.7%，而冻结 planner 仅为 38.5%，提升幅度达 17.2 个百分点。关键发现包括：

- **离线 SFT 导致性能崩溃**：SFT 的平均准确率仅为 19.5%，远低于冻结基线。这是因为 token 级别的模仿学习目标与轨迹级别的任务成功之间存在根本性错位，导致 planner 无法适应动态工具反馈或从复合错误中恢复。
- **更强模型不等于更好 planner**：使用 GPT-4o 作为冻结 planner 仅带来 5.8% 的平均增益（44.3% vs 38.5%），远低于 Flow-GRPO 训练的 7B planner。这表明 in-the-flow 在线优化比单纯扩大模型规模更有效。

#### 推理轮次扩展性

Figure 7 展示了最大交互轮数 $T_{\max}$ 的影响。将 $T_{\max}$ 从 3 增加到 10，平均准确率持续提升，证明 in-the-flow 优化具有良好的可扩展性。Table 4 进一步显示，实际使用的轮数随 $T_{\max}$ 增加而增长，GAIA 任务需要的轮数最多。

#### 工具调用行为变化

Figure 8 揭示了 Flow-GRPO 训练后工具调用比率的显著变化。优化后的 planner 更偏好使用 Google Search 和 Web Search，在 2Wiki 上 Google Search 的调用比率增加了 42.0%。这表明在线强化学习使 planner 学会了根据任务需求选择更有效的工具。

#### 训练动态

Figure 9 展示了训练过程中的奖励和响应长度变化。奖励稳步上升，响应长度先下降后稳定，表明 Flow-GRPO 在样本效率和训练稳定性方面表现良好。

### 缩放与泛化

Figure 6 展示了模型规模缩放实验。Flow-GRPO 在 3B 和 7B 基座模型上均提供一致的性能增益，证明该方法在不同模型容量下均有效。Figure 10 的工具缩放研究表明，将工具后端从 Qwen2.5-7B-Instruct 升级到 GPT-4o 可进一步提升性能，在 HotpotQA 上增益达 13.0 个百分点。

### 失败模式与定性分析

Figure 5 的案例研究展示了 Flow-GRPO 带来的策略转变。冻结 planner 在遭遇重复错误后陷入循环，而经 Flow-GRPO 训练的 planner 在两次失败尝试后于第 4 轮探索出新的解决路径。这表明在线优化使 planner 学会了从错误中恢复并调整策略。

### 实验公平性说明

所有 7B 系统均使用 Qwen2.5-7B-Instruct 作为模块基座，工具也基于该模型，与 AutoGen 等系统保持可比性。评估使用统一的 judge 模型（GPT-4o），通过语义、数值和选项级别等价判断确保公平。所有结果报告三次试验的平均准确率以降低随机性影响。

### 局限性

当前方法存在以下局限：仅优化 planner 模块，executor、verifier 和 generator 保持冻结，可能限制了性能上限；工具集合主要围绕搜索和代码执行，尚未扩展到数据库、API 调用等更多样化工具；仅在最多 10 轮交互内评估，超长程任务需要进一步验证；奖励信号完全依赖最终答案的可验证正确性，不适用于开放式生成任务；所有实验基于 Qwen2.5 架构，向其他模型家族的迁移有待验证。

## 方法谱系与知识库定位

### 与基线方法的关系

AGENTFLOW 处于两类主流范式的交叉点上：**一体式工具集成推理模型**（Monolithic Tool-Integrated Reasoning, TIR）与**多智能体系统**。理解其定位需要首先厘清这两条技术路线的本质差异。

**一体式 TIR 模型**（如 Search-R1、TIR、ToRL、Luffy 等）训练单一策略在全上下文下交错生成推理过程与工具调用。这种范式将“思考”与“行动”压缩到同一个自回归生成过程中，优势在于端到端可微、实现简单；但瓶颈同样明显：随着规划长度增长、工具种类增多、工具反馈动态变化，单一策略难以稳定扩展，且推理时对未见任务和工具的泛化性较差。AGENTFLOW 的模块化设计正是对这一瓶颈的直接回应——通过将规划、执行、验证、生成四个环节解耦为专门模块，使每个模块只需关注自身职责，从而降低单点复杂度。

**多智能体系统**（以 AutoGen 为代表）同样采用模块分解思路，但其核心缺陷在于缺乏在线训练能力。AutoGen 依赖冻结的 LLM 模块通过预定义协议协作，无法从交互动态中学习改进。AGENTFLOW 的关键突破在于将 planner 模块置于系统循环中在线优化，使模块化系统的优势得以通过强化学习被放大而非被冻结限制。实验数据验证了这一判断：使用相同 Qwen2.5-7B-Instruct 基座的 AutoGen 在搜索密集型任务上的平均准确率仅为 51.2%，而经 Flow-GRPO 训练后的 AGENTFLOW 达到 57.3%（Table 1）。

**纯推理 RL 模型**（SimpleRL-reason、Open-Reasoner-Zero、General-Reasoner 等）代表了另一条技术路线：通过强化学习激发 LLM 的推理能力，但不涉及工具使用。这类方法在数学和科学推理上表现强劲，但面对需要外部知识检索的任务时能力受限。AGENTFLOW 在继承 GRPO 族算法（Group Relative Policy Optimization）的组标准化优势思想基础上，将其扩展到多轮工具交互场景，实现了推理能力与工具使用能力的联合优化。

### 核心区分机制：Flow-GRPO 的信用分配策略

AGENTFLOW 与所有基线方法最根本的区分在于**信用分配**机制。这一机制直接回应了长程稀疏奖励下的核心难题：当系统经过多轮交互后才获得一个最终的二元成功/失败信号，如何判断每一轮决策的贡献？

- **离线 SFT** 试图通过模仿理想轨迹的 token 级交叉熵来规避信用分配问题，但 token 级模仿目标与轨迹级任务成功之间存在根本性错位。实验显示 SFT 导致性能崩溃（平均准确率仅 19.5%，Table 3），原因在于它无法让 planner 适应动态工具反馈或从累积错误中恢复。

- **冻结 planner（含 GPT-4o）** 完全放弃了信用分配，依赖预训练能力的静态迁移。即使使用更强的 GPT-4o 作为 planner，平均准确率也仅 44.3%，远低于 Flow-GRPO 训练的 7B planner（55.7%，Table 3）。这表明**在线优化比模型规模更重要**。

- **Flow-GRPO** 的策略是将同一轨迹级最终奖励广播到所有轮次，配合组标准化优势进行方差缩减。这一设计的理论依据在于：在最终奖励仅取决于最终答案正确性的设定下，轨迹内所有动作共享相同的全局信号是合理的；组标准化则在采样组内对奖励进行归一化，使优势估计更稳定。附录 B 中的定理 B.1 和 B.3 分别给出了单轮更新与全局目标的等价性证明及单调改进保证，为这一策略提供了形式化支撑。

### 适用边界

AGENTFLOW 的设计隐含了若干适用前提，超出这些边界时方法的有效性需要审慎评估：

1. **可验证的最终奖励**：Flow-GRPO 完全依赖最终答案的二元正确性作为奖励信号。这适用于数学计算、事实问答、代码执行等有明确对错的任务，但不适用于开放式生成（如创意写作、对话系统），因为后者缺乏可自动验证的客观标准。

2. **工具可调用且反馈明确**：系统的 executor 模块依赖工具返回结构化或半结构化的执行结果供 verifier 评估。如果工具反馈模糊、延迟或不可靠，整个循环的稳定性会受到影响。当前实验中的工具集主要为搜索引擎和代码解释器，反馈形式相对规整。

3. **任务可分解为多轮子目标**：AGENTFLOW 的规划-执行-验证循环假定任务可以通过逐步的子目标分解来完成。对于需要一次性全局推理的任务，多轮交互可能引入不必要的开销。

4. **模块基座模型能力下限**：虽然 Flow-GRPO 训练带来了显著提升，但 executor、verifier 和 generator 模块保持冻结，其基础能力构成了系统性能的上限。实验显示 3B 和 7B 基座均能受益于 Flow-GRPO 训练（Figure 6），但在更小或更弱的基座上，冻结模块可能成为瓶颈。

### 已知局限与开放问题

**当前局限**（论文已明确指出的约束）：

- **仅优化 planner 模块**：executor、verifier 和 generator 保持冻结，限制了系统整体性能的天花板。当 planner 学会更优的规划策略后，执行或验证环节的固定能力可能成为新的瓶颈。
- **工具集范围有限**：当前工具主要围绕搜索（Google Search、Web Search、Wikipedia）和代码执行（Python Interpreter），尚未扩展到数据库查询、API 调用、文件操作等更丰富的工具类型。
- **交互轮数上限**：实验在最多 10 轮的设定下评估，超长程任务（如多文件软件开发、复杂数据分析流水线）的性能表现未知。
- **模型架构依赖**：所有实验基于 Qwen2.5 架构，向 Llama、Mistral 等其他模型家族的迁移效果有待验证。

**开放研究问题**（从方法设计和实验结果中自然引申的方向）：

- **端到端联合优化**：能否将 Flow-GRPO 的在线训练框架扩展到所有四个模块，实现 planner、executor、verifier、generator 的协同进化？这涉及非平稳环境下的多智能体 RL 问题，信用分配的复杂度将显著上升。

- **动态工具环境的适应**：当工具集动态变化（新工具加入、旧工具失效、工具行为改变）时，Flow-GRPO 能否快速适应？这需要研究在线 RL 的持续学习能力与灾难性遗忘之间的平衡。

- **奖励信号的丰富化**：当前二元奖励丢弃了大量中间信息。能否设计部分正确性奖励、效率奖励（如最少轮数完成）、或基于过程的验证信号，在保持可自动验证的前提下提供更细粒度的反馈？

- **更大规模的 scaling 行为**：Figure 6 展示了 3B 到 7B 的 scaling 趋势，但 32B、70B 乃至更大模型的 scaling law 尚不明确。特别是，当基座模型本身已具备较强规划能力时，Flow-GRPO 的边际收益是否会递减？

- **超长程任务的收敛性**：当交互轮数从 10 扩展到 50 或 100 时，广播同一奖励到所有轮次的策略是否仍然有效？更靠前的轮次与最终结果之间的因果链变长，信用分配的信噪比可能恶化，可能需要引入折扣因子或分层奖励结构。

## 原文 PDF

## 相关样本

- [[obsidian-vault/analysis/ICLR_2026/Agentic_Reinforcement_Learning_with_Implicit_Step_Rewards.md|Agentic RL with Implicit Step Rewards]]：同属 agentic RL 样本，可对照 planner 优化与隐式 step reward。
- [[obsidian-vault/analysis/ICLR_2026/AdaReasoner_Dynamic_Tool_Orchestration_for_Iterative_Visual_Reasoning.md|AdaReasoner]]：同属工具使用与规划优化样本，可对照通用 agent flow 和视觉工具编排。

![[obsidian-vault/paperPDFs/ICLR_2026/In-the-Flow_Agentic_System_Optimization_for_Effective_Planning_and_Tool_Use.pdf]]
