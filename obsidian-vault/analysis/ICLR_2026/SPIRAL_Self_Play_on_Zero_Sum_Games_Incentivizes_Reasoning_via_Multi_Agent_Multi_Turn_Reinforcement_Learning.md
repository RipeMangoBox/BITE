---
title: "SPIRAL: Self-Play on Zero-Sum Games Incentivizes Reasoning via Multi-Agent Multi-Turn Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SPIRAL_Self_Play_on_Zero_Sum_Games_Incentivizes_Reasoning_via_Multi_Agent_Multi_Turn_Reinforcement_Learning.pdf
project_link: null
code_link: https://github.com/spiral-rl/spiral
openreview_forum_id: 7Yayy5fNLg
aliases:
- SPIRAL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过零和博弈上的自我对弈（SPIRAL）结合角色条件优势估计（RAE），模型可以在无人工监督的情况下，利用不断进化的对手自动生成训练课程，从而发展可迁移的推理能力。"
primary_logic: "零和博弈的竞争压力促使模型涌现出结构化推理模式（如个案分析、期望值计算、模式识别），这些模式通过自我对弈的自动课程效应无缝迁移到数学和其他推理任务中。角色条件优势估计通过角色特定的基线归一化奖励，防止多智能体训练中的“思考崩溃”，从而稳定训练并保障泛化性能。"
claims:
- "多游戏SPIRAL训练在8个推理基准上实现最高10.5%的绝对提升，且不使用任何领域特定数据。"
- "SPIRAL一致优于在25k专家游戏轨迹上进行监督微调（SFT）的方法。"
- "移除RAE后，模型在200步后发生思考崩溃，数学推理性能从35%下降至12%。"
- "自我对弈维持约50-52%的均衡胜率，而固定对手训练从0%升至62.5%，表明其仅学会利用静态策略而非真正推理。"
---

# SPIRAL: Self-Play on Zero-Sum Games Incentivizes Reasoning via Multi-Agent Multi-Turn Reinforcement Learning

> [!tip] 核心洞察
> 零和博弈的竞争压力促使模型涌现出结构化推理模式（如个案分析、期望值计算、模式识别），这些模式通过自我对弈的自动课程效应无缝迁移到数学和其他推理任务中。角色条件优势估计通过角色特定的基线归一化奖励，防止多智能体训练中的“思考崩溃”，从而稳定训练并保障泛化性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SPIRAL：多智能体多轮强化学习中的零和博弈自我对弈推理激励 |
| 英文题名 | SPIRAL: Self-Play on Zero-Sum Games Incentivizes Reasoning via Multi-Agent Multi-Turn Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7Yayy5fNLg) · [GitHub](https://github.com/spiral-rl/spiral) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SPIRAL |
| Dataset | 8个推理基准（MATH500, AIME24/25, Olympiad, AMC-23, Minerva, GPQA-D, MMLU-Pro）, 同上8个基准, 同上（多种子统计）, 6个游戏环境（含OOD） |

> [!tip] 效果简介
> - 8个推理基准（MATH500, AIME24/25, Olympiad, AMC-23, Minerva, GPQA-D, MMLU-Pro） 上，平均得分（%） 为 44.5（Qwen3-4B-Base + SPIRAL-Multi），对比 34.0（Qwen3-4B-Base），变化 +10.5。
> - 同上8个基准 上，平均得分（%） 为 49.6（Qwen3-8B-Base + SPIRAL-Multi），对比 39.5（Qwen3-8B-Base），变化 +10.1。
> - 同上（多种子统计） 上，平均得分（%） 为 44.5 ± 0.5（Qwen3-4B + SPIRAL-Multi），对比 39.6 ± 0.4（Qwen3-4B + SFT-Multi），变化 +4.9。

## 概要

### 问题瓶颈

当前基于可验证奖励的强化学习（RLVR）范式在推动大语言模型推理能力方面取得了显著进展，但其核心瓶颈在于**对人工设计数据的强依赖**：训练需要大量精心策划的问题-答案对和针对特定领域的奖励函数，难以低成本地扩展到多样化的推理挑战。这一可扩展性瓶颈限制了模型在缺乏人工标注的新任务上的泛化能力。

### 核心方案

SPIRAL 提出了一种根本不同的路径——**通过零和博弈上的自我对弈自动生成训练信号**。其核心机制包括两个层面：

- **自动课程生成**：模型在井字棋、Kuhn扑克和简单谈判等多回合零和游戏中与持续进化的自身副本对弈，竞争压力自然催生出越来越强的对手，形成无需人工干预的训练课程。
- **角色条件优势估计（RAE）**：针对多智能体训练中不同角色（玩家0/玩家1）的奖励分布不对称问题，RAE为每个（游戏，角色）对维护独立的指数移动平均基线，计算角色特定优势 $A_{G,p}(\tau) = R_p(\tau) - b_{G,p}$，从而稳定训练并防止“思考崩溃”。

### 方法定位

相较于依赖专家轨迹的监督微调（SFT）和使用固定对手的强化学习，SPIRAL 属于**无监督自我对弈强化学习**范式。它不引入任何领域特定的训练数据，而是利用博弈论中的零和竞争压力，驱动模型自发涌现结构化推理模式（个案分析、期望值计算、模式识别），并使其无缝迁移至数学和知识推理任务。

### 主要结果

- **推理基准提升**：多游戏 SPIRAL 训练使 Qwen3-4B-Base 在 8 个推理基准上的平均得分从 34.0% 提升至 44.5%（+10.5%），Qwen3-8B-Base 从 39.5% 提升至 49.6%（+10.1%），且一致优于在 25k 专家轨迹上微调的 SFT 基线（Table 1）。
- **RAE 的关键作用**：移除 RAE 后，模型在 200 步内发生思考崩溃，响应长度暴跌，数学推理准确率从 35% 骤降至 12%（Figure 6, Figure 9）。
- **自我对弈 vs. 固定对手**：固定对手训练使胜率从 0% 升至 62.5%，但其仅学会利用静态策略漏洞；自我对弈则维持约 50-52% 的均衡胜率，表明模型在持续发展真正的推理能力（Table 3）。
- **多游戏泛化优势**：多游戏模型在对抗 Gemini-2.0-Flash 的平均胜率达 59.5%，比最佳单游戏专家高出 6.6 个百分点，在分布外游戏上也展现出更强的迁移能力（Table 5）。



### 现有范式：基于可验证奖励的强化学习

近年来，基于可验证奖励的强化学习（RLVR）已成为提升大语言模型推理能力的核心范式。其基本逻辑是：针对数学、代码等具有客观评判标准的领域，人工设计奖励函数或答案验证器，将模型输出与标准答案进行比对，以此作为训练信号优化模型。这一范式在数学推理（如MATH、AIME）和代码生成等任务上取得了显著成效。

然而，RLVR的成功高度依赖于两个关键前提：

1. **人工设计的任务与奖励**：训练需要大量精心策划的问题-答案对，以及针对特定领域的奖励工程。这不仅是劳动密集型的，更本质性地限制了方法的可扩展性——每扩展到一个新领域，都需要重新设计任务格式和验证逻辑。
2. **静态的奖励信号**：奖励函数一旦设计完成便固定不变，无法随模型能力的提升而动态调整训练难度。模型可能通过记忆模式或表面统计线索“刷分”，而非发展真正的推理能力。

### 核心瓶颈：从领域特定到通用推理的扩展困境

这一范式的瓶颈在于：**可扩展推理能力的发展无法依赖人工设计的静态奖励**。当模型仅在数学题上训练时，它学到的是数学题的解题技巧；当模型仅在代码题上训练时，它学到的是代码生成模式。这些技能能否迁移到其他推理领域（如科学推理、逻辑分析），取决于任务之间潜在认知结构的相似性，而RLVR本身并不提供跨领域迁移的机制。

更根本的问题在于：RLVR假设“推理能力”可以通过在特定任务上最大化可验证奖励来获得。但推理的本质——分析、比较、排除、期望值计算——是领域无关的认知操作。如果训练环境本身不要求这些操作涌现，模型就没有动力去发展它们。

### SPIRAL的动机：用博弈压力替代人工奖励

SPIRAL的出发点是一个直观的假设：**零和博弈的竞争压力天然要求玩家进行结构化推理**。在井字棋中，玩家需要枚举对手的可能回应（个案分析）；在扑克中，玩家需要计算不同策略的期望值（期望值计算）；在谈判中，玩家需要识别对手的行为模式（模式识别）。这些认知操作恰好也是数学推理、科学推理等任务的核心组件。

关键洞察在于：如果让模型在零和博弈中进行自我对弈——即模型同时扮演双方，与不断进化的自己对抗——那么：

- **无需人工监督**：博弈的胜负本身就是天然的奖励信号，无需人工标注答案或设计奖励函数。
- **自动课程效应**：随着模型能力提升，对手也在同步变强，训练难度自动适配当前水平，形成持续的进步压力。
- **推理模式涌现**：为在竞争中获胜，模型被迫发展出结构化的推理策略，这些策略可能迁移到其他推理任务中。

这一思路将“推理能力获取”从“在特定任务上优化人工奖励”重新定义为“在竞争环境中通过自我对弈涌现可迁移的认知策略”。



## 核心方法与创新机理

SPIRAL的核心创新在于重新定义了LLM推理能力的获取路径：将训练信号从**人工设计的领域特定奖励**转向**零和博弈自我对弈的竞争压力**，并引入**角色条件优势估计（RAE）**来稳定这一多智能体训练过程。以下从三个关键维度展开。

### 创新一：从人工奖励工程到自我对弈自动课程

现有基于可验证奖励的强化学习（RLVR）方法面临根本性的可扩展性瓶颈——它们依赖人工策划的问题-答案对和特定领域的奖励函数，难以泛化到多样化的推理挑战。SPIRAL通过零和博弈的自我对弈彻底绕过了这一限制：

- **训练数据来源的根本转变**：传统方法需要人工标注的问答对作为训练信号，而SPIRAL的训练轨迹完全由多回合零和博弈的自我对弈自动生成，无需任何人工监督（Abstract: "eliminating the need for human supervision"）。
- **自动课程效应**：共享参数策略 $\pi_\theta$ 同时为博弈双方生成动作，对手随训练同步进化。这种设计使模型始终面对与自身能力匹配的挑战，形成天然的课程调度——自我对弈维持约50-52%的均衡胜率，而固定对手训练的胜率从0%升至62.5%（Table 3），表明后者仅学会利用静态策略漏洞，而非发展真正的推理能力。

### 创新二：角色条件优势估计（RAE）防止“思考崩溃”

多智能体零和博弈的策略梯度训练面临独特的方差问题：同一轨迹中玩家0和玩家1的奖励天然负相关，全局REINFORCE梯度无法区分这种角色不对称性。SPIRAL的核心技术贡献在于引入RAE：

- **角色特定的基线维护**：为每个游戏 $G$ 和角色 $p$ 维护独立的指数移动平均基线 $b_{G,p}$，计算角色条件优势 $A_{G,p}(\tau) = R_p(\tau) - b_{G,p}$（Equation 2）。这消除了位置不对称带来的梯度方差。
- **训练稳定性的决定性作用**：移除RAE后，模型在200步后发生灾难性的“思考崩溃”——响应长度暴跌至接近零，数学推理准确率从35%降至12%（Figure 9, Section E.2）。相比之下，带有RAE的REINFORCE保持了稳定的响应长度和持续提升的推理性能（Figure 6）。RAE通过将回报中心化到角色特定基线，防止梯度方差将策略推向退化解。

### 创新三：博弈推理模式向通用推理的迁移机制

SPIRAL揭示了零和博弈中涌现的结构化推理模式可无缝迁移到数学和其他推理任务，这是其超越游戏领域的核心价值：

- **三种核心推理模式的涌现**：在290条游戏轨迹和46,792个数学解答的追踪中，SPIRAL训练促使模型自发形成个案分析（Case-by-Case Analysis）、期望值计算（Expected Value Calculation）和模式识别（Pattern Recognition）三种推理模式。其中期望值计算在训练后期频率达到78%（Figure 4）。
- **迁移效果的量级**：多游戏SPIRAL训练在8个推理基准上实现最高10.5%的绝对提升（Qwen3-4B-Base: 34.0% → 44.5%; Qwen3-8B-Base: 39.5% → 49.6%, Table 1），且一致优于在25k专家游戏轨迹上进行监督微调（SFT）的方法。将SFT数据量翻倍至52k未带来实质提升（39.6% vs 39.7%），而SPIRAL-Multi达到44.5%（Table 9），说明收益来自强化学习的动态探索而非数据量。

### 与基线方法的系统性差异

| 创新维度 | 基线方法 | SPIRAL |
|---------|---------|--------|
| 训练数据来源 | 人工策划的问答对和领域特定奖励函数 | 零和博弈自我对弈自动生成的游戏轨迹 |
| 优势估计 | 全局REINFORCE梯度，未区分游戏和角色差异 | RAE：为每个 $(G, p)$ 对维护独立基线 |
| 对手策略 | 固定的预训练模型或静态策略 | 共享参数的自我对弈，对手同步进化 |

SPIRAL的核心洞察在于：零和博弈的竞争压力天然驱动模型发展结构化推理，而RAE确保了这种压力在多智能体训练中不会因方差失控而导致思考崩溃。这一框架的泛化性已通过多模型架构（Qwen3、Llama、DeepSeek-Distill-Qwen）的验证得到初步证实。



![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_7Yayy5fNLg/figures/003_Figure_3.jpg]]
*Figure 3: The SPIRAL Framework. SPIRAL employs an actor-learner architecture for scalable self-play training. Parallel actors sample trajectories from a diverse set of games using vectorized environments. A single policy $\pi _ { i }$ plays both roles, generating zero-sum, sparse reward game trajectories. The centralized learner processes these trajectories using Role-conditioned Advantage Estimation (RAE) to compute separate advantages, $A _ { 0 }$ ( s , a ) and $A _ { 1 }$ ( s , a ) , for each role. These are then used for on-policy reinforcement learning updates*

SPIRAL 构建了一套全在线、多智能体、多轮次的强化学习系统，使语言模型通过对弈零和博弈来自主发展可迁移的推理能力。其核心架构采用 **Actor-Learner 分布式设计**（Figure 3），将轨迹采样与策略更新解耦，实现可扩展的自我对弈训练。

### 架构总览

系统由四个关键模块构成闭环：

1. **共享策略网络（LLM）**：单一策略 $\pi_\theta$ 通过角色提示（role-conditioned system prompts）同时扮演玩家 0 和玩家 1，为双方生成包含推理链的完整动作。参数完全共享，$\theta_0 = \theta_1 = \theta$。

2. **vLLM 推理引擎**：部署在 actor 端，负责高效生成多回合的模型响应（reasoning + action），支撑并行采样。

3. **TextArena 游戏模拟器**：提供多回合语言游戏的向量化环境，处理状态转移与终局判定（胜/负/平），返回稀疏的零和奖励信号。

4. **角色条件优势估计（RAE）模块**：部署在集中式 learner 端，为每个（游戏 $G$，角色 $p$）对维护独立的指数移动平均基线 $b_{G,p}$，计算方差缩减后的优势信号 $A_{G,p} = R_p - b_{G,p}$，替代原始蒙特卡洛回报驱动策略梯度更新。

### 数据流与训练循环

训练遵循严格的在线自我对弈流程（Algorithm 1）：

- **采样阶段**：多个并行 actor 从游戏集合 $\mathcal{G}$ 中随机抽取游戏，使用当前策略 $\pi_\theta$ 为双方生成完整对弈轨迹 $\tau$。每条轨迹包含多轮交互，每轮模型需先输出推理过程再给出动作，最终根据游戏规则获得终局奖励 $R_p(\tau) \in \{-1, 0, +1\}$。

- **学习阶段**：集中式 learner 接收轨迹批次，RAE 模块按游戏和角色分别更新基线：$b_{G,p} \leftarrow \alpha b_{G,p} + (1 - \alpha) R_p(\tau)$，随后计算角色条件优势 $A_{G,p}(\tau)$。最终使用方差缩减后的 SPIRAL 策略梯度更新参数：

$$\nabla_{\theta} J_{\mathrm{SPIRAL}}(\theta) = \mathbb{E}_{G \sim \mathcal{G}} \mathbb{E}_{\tau \sim \pi_{\theta} \times \pi_{\theta} \mid G} \left[ \sum_{p \in \{0,1\}} \sum_{t \in T_p} A_{G,p}(\tau) \cdot \nabla_{\theta} \log \pi_{\theta}(y_t^{(p)} | s_t, p, G) \right]$$

- **同步阶段**：更新后的策略参数即时同步至所有 actor，对手能力随训练同步进化，形成自动课程效应——模型始终面对与自己实力相当的对手。

### 关键设计决策

与传统的基于可验证奖励的强化学习（RLVR）相比，SPIRAL 在三个核心维度上实现了根本性转变：

- **数据来源**：从人工策划的问题-答案对和领域特定奖励函数，转向由多回合零和博弈自我对弈自动生成的游戏轨迹，完全消除人工监督需求。

- **优势估计**：从全局 REINFORCE 梯度（未区分游戏和角色差异），转向角色条件优势估计（RAE），为每个游戏和角色维护独立基线，消除位置不对称带来的梯度方差。

- **对手策略**：从固定的预训练模型或静态策略，转向共享参数的自我对弈——对手随训练同步进化，迫使模型持续发展更复杂的推理策略而非利用静态漏洞。

实验表明，RAE 是稳定训练的关键保障：移除 RAE 后，模型在约 200 步后发生“思考崩溃”（thinking collapse），响应长度从约 2000 字符暴跌至接近零，数学推理准确率从 35% 降至 12%（Figure 6, Figure 9）。RAE 通过将回报中心化到角色特定基线，防止梯度方差将策略推向退化解。



### 共享策略自对弈框架

SPIRAL 的核心设计是使用**单一共享策略** $\pi_\theta$ 同时扮演零和博弈中的双方角色。与传统的独立策略自对弈不同，SPIRAL 设置 $\theta_0 = \theta_1 = \theta$，即玩家 0 和玩家 1 共享同一组参数。策略通过系统提示（system prompt）进行角色条件化，使同一模型能够学习针对不同位置的差异化策略。

训练采用 REINFORCE 算法，基于蒙特卡洛回报计算策略梯度。在共享策略设定下，原始梯度形式为：

$$
\nabla_{\theta} J(\theta) = \mathbb{E}_{G \sim \mathcal{G}} \mathbb{E}_{\tau \sim \pi_{\theta} \times \pi_{\theta} \mid G} \left[ \sum_{t \in T_0} \nabla_{\theta} \log \pi_{\theta}(y_t^{(0)} | s_t, 0, G) \cdot R_0(\tau) + \sum_{t \in T_1} \nabla_{\theta} \log \pi_{\theta}(y_t^{(1)} | s_t, 1, G) \cdot R_1(\tau) \right]
$$

其中 $G$ 为从游戏集合 $\mathcal{G}$ 中采样的游戏，$\tau$ 为自对弈产生的完整轨迹，$T_p$ 为玩家 $p$ 的决策时间步集合，$R_p(\tau)$ 为玩家 $p$ 获得的稀疏终局奖励（通常为 $\{+1, -1, 0\}$）。该梯度直接使用原始回报作为权重，未进行方差缩减，在多智能体自对弈环境中存在严重的不稳定性。

### 角色条件优势估计（RAE）

RAE 是 SPIRAL 实现稳定训练的关键模块。其核心思想是为**每个游戏 $G$ 和每个角色 $p$ 维护独立的指数移动平均基线** $b_{G,p}$，从而消除零和博弈中位置不对称性引入的方差。

基线更新规则为：

$$
b_{G,p} \leftarrow \alpha b_{G,p} + (1 - \alpha) R_p(\tau), \quad A_{G,p}(\tau) = R_p(\tau) - b_{G,p}
$$

其中 $\alpha$ 为衰减系数（论文中未深入消融该超参数），$A_{G,p}(\tau)$ 为角色条件优势。该设计的因果机制在于：在零和博弈中，玩家 0 和玩家 1 的奖励分布天然负相关，若使用全局基线会将对手的劣势错误地归因为自身策略的改进，导致梯度信号混乱。RAE 通过角色特定基线将回报中心化，使优势估计仅反映相对于同角色历史表现的增量，从而阻断这一混淆路径。

### SPIRAL 方差缩减策略梯度

将 RAE 计算的 $A_{G,p}(\tau)$ 替代原始奖励 $R_p(\tau)$，得到最终的 SPIRAL 策略梯度：

$$
\nabla_{\theta} J_{\mathrm{SPIRAL}}(\theta) = \mathbb{E}_{G \sim \mathcal{G}} \mathbb{E}_{\tau \sim \pi_{\theta} \times \pi_{\theta} \mid G} \left[ \sum_{p \in \{0,1\}} \sum_{t \in T_p} A_{G,p}(\tau) \cdot \nabla_{\theta} \log \pi_{\theta}(y_t^{(p)} | s_t, p, G) \right]
$$

该梯度的决定性证据来自消融实验：移除 RAE 后，模型在约 200 步训练后发生“思考崩溃”（thinking collapse）——响应长度从约 2000 字符暴跌至接近零，数学推理准确率从 35% 下降至 12%（Figure 9, Section E.2）。相比之下，使用 RAE 的训练在响应长度和基准性能上均保持稳定（Figure 6）。

### 分布式 Actor-Learner 架构

SPIRAL 的工程实现采用 Actor-Learner 分布式架构，包含以下核心模块：

- **vLLM 推理引擎**：负责高效生成多回合的模型响应（包含推理链 + 动作），支撑多个 actor 的并行采样。
- **TextArena 游戏模拟器**：提供多回合语言游戏的模拟环境，处理状态转换和终局判定，支持向量化环境以加速采样。
- **集中式 Learner**：接收 actor 采样的轨迹，执行 RAE 基线更新和优势计算，随后进行在线策略梯度更新。Learner 与 actor 之间的参数同步采用全参数更新方式。

该架构使 SPIRAL 能够在 8 张 H100 GPU 上完成 Qwen3-4B 约 25 小时、Qwen3-8B 约 28 小时的完整训练。所有实验采用统一的超参数（学习率 $1 \times 10^{-6}$，温度 1.0，熵系数 0.01），不因游戏或模型尺度调整，保证了对比的公平性。



## 实验与关键发现

### 核心结果：零和博弈自我对弈实现跨域推理迁移

SPIRAL的核心主张是：模型通过在零和博弈上进行多回合自我对弈，无需任何领域特定训练数据即可显著提升通用推理能力。Table 1 的主实验结果直接支撑了这一主张。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_7Yayy5fNLg/figures/004_Table_1.jpg]]
*Table 1: Reasoning benchmark performance. The “-Kuhn” suffix denotes fine-tuning solely on a single game (Kuhn Poker), while the “-Multi” suffix indicates fine-tuning on all three games. SPI-RAL improves reasoning without any domain-specific training data. ∗Few-shot evaluation following Qwen3 technical report*

在 Qwen3-4B-Base 上，多游戏 SPIRAL 训练（SPIRAL-Multi）将 8 个推理基准的平均得分从基线的 34.0% 提升至 44.5%，绝对提升达 **+10.5%**。在更大的 Qwen3-8B-Base 上，同样观察到从 39.5% 到 49.6% 的 **+10.1%** 提升。这一提升模式在多种模型架构上一致复现（Table 9），包括 Octothinker-8B、Llama-3.1-8B 和 DeepSeek-Distill-Qwen-7B，表明 SPIRAL 的收益并非特定于某一模型系列。

值得注意的是，SPIRAL 一致优于在 25k 条专家游戏轨迹上进行监督微调（SFT）的方法。在 Qwen3-4B-Base 上，SFT-Multi 仅达到 39.6%，而 SPIRAL-Multi 达到 44.5%（Table 10，3 个种子的均值 ± 标准差为 44.5 ± 0.5 vs 39.6 ± 0.4）。将 SFT 数据量翻倍至 52k 条轨迹并未带来实质提升（39.7% vs 39.6%），而 SPIRAL 仍显著优于两者（Table 9）。这说明收益来自强化学习的动态探索过程，而非单纯的数据规模。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_7Yayy5fNLg/figures/007_Table_3.jpg]]
*Table 3: Win rates at different training stages of Gemini Opponent and Self-Play vs its opponent*

### 推理模式涌现与迁移机制

SPIRAL 的推理提升并非黑箱现象。作者通过 LLM-as-a-judge 框架，在 290 条游戏轨迹和 46,792 个数学解答中追踪了三种核心推理模式的演化（Figure 4，Table 2）：

- **期望值计算（Expected Value Calculation）**：在游戏训练后期达到 78% 的出现频率，是最为显著的涌现模式。该模式在数学推理中同样展现出最强的迁移效果。
- **逐案分析（Case-by-Case Analysis）**：在游戏和数学场景中均稳定增长。
- **模式识别（Pattern Recognition）**：出现频率相对较低，但仍可观察到正向迁移。

这些模式的具体表现形式在 Table 2 中通过 Kuhn 扑克和数学问题的对比示例得到展示。Figure 4 的关键发现是：随着游戏训练的推进，这些推理模式的出现频率同步增长，而数学基准得分也从 31.2 提升至 39.6，为“博弈推理可迁移至数学推理”提供了因果性证据。

### 消融实验：自我对弈 vs 固定对手

自我对弈的自动课程效应是 SPIRAL 区别于传统 RL 的核心设计。Table 3 和 Figure 5 通过对比实验揭示了这一机制的关键作用。

在固定对手训练中（对手为 Gemini-2.0-Flash-Lite），模型胜率从初始的 0% 单调上升至 62.5%。然而，这并非真正的推理能力提升——模型学会的是利用静态对手的漏洞，而非发展通用策略。相比之下，自我对弈模型与其 16 步前的历史版本对战时，胜率始终维持在 50-52% 的均衡区间（Step 16: 52.3%, Step 128: 51.7%, Step 384: 50.9%），表明模型在持续面对不断进化的对手，被迫发展更深层的推理能力。

Figure 5 进一步显示，固定对手训练在推理基准上的提升远低于自我对弈，验证了自动课程的必要性。

### 消融实验：角色条件优势估计（RAE）的关键作用

RAE 是 SPIRAL 训练稳定性的技术核心。移除 RAE 后，使用普通 REINFORCE 梯度进行训练会导致灾难性的“思考崩溃”（thinking collapse）：

- Figure 6（左）显示，无 RAE 时模型的响应长度从约 2,000 字符暴跌至接近零，模型完全停止了推理链的生成。
- Figure 9（中）量化了这一崩溃的后果：数学推理准确率从 35% 断崖式下降至 12%。
- Figure 6（右）显示通用推理性能从 44% 下降至 40%。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_7Yayy5fNLg/figures/014_Figure_6.jpg]]
*Figure 6: Training dynamics comparing REINFORCE with RAE (orange) versus vanilla REINFORCE (gray). RAE maintains stable performance across all metrics while vanilla REINFORCE suffers catastrophic thinking collapse. Left: Response length reveals thinking collapse where models stop generating reasoning traces; Right: Performance on general reasoning benchmarks*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_7Yayy5fNLg/figures/020_Figure_9.jpg]]
*Figure 9: Extended training dynamics comparing REINFORCE with RAE versus vanilla REIN-FORCE (continued from Figure 6). Left: Game win rates showing RAE achieves faster initial learning compared to vanilla REINFORCE. Middle: Math reasoning performance crashes from 35% to 12% without RAE. Right: Policy gradient norms exhibit instability then collapse to nearzero without RAE, while RAE maintains stable gradients around 0.1*

崩溃发生在训练约 200 步之后（Figure 9）。RAE 通过为每个游戏 G 和角色 p 维护独立的指数移动平均基线 $b_{G,p}$，计算角色条件优势 $A_{G,p}(\tau) = R_p(\tau) - b_{G,p}$，有效消除了零和博弈中位置不对称带来的梯度方差，防止策略向退化解方向漂移。

### 多游戏训练与泛化能力

Table 5 展示了多游戏训练相对于单游戏专家的优势。多游戏模型在 6 个游戏环境（含 OOD）上对抗 Gemini-2.0-Flash 的平均胜率达到 **59.5%**，优于最佳单游戏专家的 52.9%（+6.6%）。在训练游戏上，多游戏模型与各自专家水平接近；在 OOD 游戏上，多游戏模型展现出更强的灵活推理能力。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_7Yayy5fNLg/figures/012_Table_5.jpg]]
*Table 5: Multi-game training achieves competitive performance across all training games while excelling at novel composite challenges. All win rates shown are against Gemini-2.0-Flash as a fixed opponent. The multi-game model outperforms all specialists on average, demonstrating that diverse game training develops more flexible reasoning*

Table 4 进一步揭示了游戏技能的结构化迁移：TicTacToe 专家在需要空间推理的 Snake 游戏上达到 56.0% 胜率；扑克专家在概率驱动的 Pig Dice 上达到 91.7%；谈判专家在策略性的 Truth and Deception 上达到 55.8%。这表明不同游戏训练出的认知技能具有可辨识的迁移模式，为“游戏技能→推理能力”的映射提供了初步实证。

### 与 RLVR 的协同效应

Table 12 探索了 SPIRAL 与现有基于可验证奖励的强化学习（RLVR）的集成方式。在 Qwen3-4B-Base 上，先 RLVR 后 SPIRAL（RLVR→SPIRAL）的配置达到最高平均得分 47.9%，优于单独 RLVR 的 46.0% 和单独 SPIRAL 的 44.5%。先 SPIRAL 后 RLVR（SPIRAL→RLVR）也达到 47.4%。这表明 SPIRAL 可作为 RLVR 的有效补充，在 RLVR 的前后阶段均能提供增益，两者捕获的推理能力具有互补性。

### 泛化鲁棒性

Table 8 测试了 SPIRAL 在复杂度提升的 OOD 环境上的泛化性能。在 Tic-Tac-Toe（4×4 棋盘）、Kuhn Poker（增加牌面）和 Simple Negotiation（增加物品）的 OOD 变体上，SPIRAL 一致优于 SFT 基线。这进一步支持了自我对弈培养的是可迁移推理策略而非环境特定捷径的论点。

### 实验公平性说明

所有实验采用统一的超参数配置（学习率 1e-6，温度 1.0，熵系数 0.01），不因游戏或模型尺度调整（Table 6）。主实验在 Qwen3-4B-Base 上报告了 3 个种子的统计结果，其他模型报告单一运行。推理基准评估统一采用零样本设定（温度 0.6, top-p 0.95），数学题使用 0-shot，部分知识题遵循原论文的 few-shot 协议。计算预算方面，Qwen3-4B 训练约需 25 小时（8 H100 GPU），Qwen3-8B 约 28 小时，所有方法在相同资源约束下比较。

### 局限与失败模式

尽管 SPIRAL 展现出显著的推理迁移能力，仍存在明确的局限：

1. **环境多样性受限**：实验仅限于三种简单零和游戏（井字棋、Kuhn 扑克、简单谈判），尚未验证在更复杂、非零和或部分可观测游戏上的有效性。
2. **迁移效果不均衡**：在 GPQA-Diamond 和 MMLU-Pro 等知识密集型基准上，提升相对有限，表明博弈推理向事实性知识的迁移存在边界。
3. **训练稳定性依赖 RAE**：RAE 的超参数 α 未经深入消融，游戏组合的课程调度策略未被探索，可能影响更复杂场景下的训练稳定性。
4. **计算成本**：8 H100 GPU 训练 25-28 小时的资源需求限制了快速实验迭代。



## 定位与知识库关联

### 1. 方法谱系：从 RLVR 到自我对弈推理

SPIRAL 的核心定位是**在无人工监督的条件下，通过零和博弈的自我对弈自动生成训练课程，从而发展可迁移的推理能力**。其方法谱系可从三个维度理解：

**与 RLVR 的关系。** 现有基于可验证奖励的强化学习（RLVR）方法依赖人工策划的问题-答案对和特定领域的奖励工程，形成了可扩展性瓶颈——每引入一个新推理领域，都需要重新设计奖励函数和训练数据。SPIRAL 将这一范式替换为：训练数据由多回合零和博弈的自我对弈自动生成，奖励信号仅来自游戏的稀疏结局判定（胜/负/平），无需任何领域特定的奖励设计。这一转变使模型在训练过程中从未见过任何数学或推理基准数据，却能实现跨域迁移。

**与模仿学习的关系。** 论文将 SPIRAL 与监督微调（SFT）基线进行了直接对比：使用 Qwen3-32B 生成的 25k 专家游戏轨迹进行 SFT，在 8 个推理基准上的平均得分仅为 39.6%，而 SPIRAL-Multi 达到 44.5%（Table 1）。将 SFT 数据量翻倍至 52k 后，性能几乎无变化（39.7% vs 39.6%），而 SPIRAL 仍显著优于两者（Table 9）。这表明收益来源于强化学习的探索动态，而非训练数据量——SFT 只能模仿静态的专家策略，无法产生自我对弈中的自动课程效应。

**与固定对手 RL 的关系。** 论文对比了两类固定对手：Mistral-Small-3 和 Gemini-2.0-Flash-Lite。关键发现是：固定对手训练导致模型学习利用静态策略漏洞，而非发展真正的推理能力。证据来自 Table 3：自我对弈在训练全程维持约 50-52% 的均衡胜率（对手为 16 步前的自身），而固定 Gemini 对手训练的胜率从 0% 单调上升至 62.5%——这表明模型仅学会针对特定对手的弱点，而非持续提升自身能力。

### 2. 核心技术机制：角色条件优势估计（RAE）

SPIRAL 的关键技术贡献是**角色条件优势估计**（Role-conditioned Advantage Estimation, RAE），其设计动机来自多智能体自对弈的独特挑战。

**问题本质。** 在共享策略的自对弈中，同一个策略 $\pi_\theta$ 同时为玩家 0 和玩家 1 生成动作。若使用标准 REINFORCE 梯度（Equation 1），梯度信号会因零和博弈中双方奖励的对称性而产生高方差——模型可能通过“停止思考”来降低损失，即输出极短的响应以回避复杂推理。

**RAE 的解决方案。** RAE 为每个游戏 $G$ 和角色 $p \in \{0,1\}$ 维护独立的指数移动平均基线 $b_{G,p}$，并计算角色条件优势 $A_{G,p}(\tau) = R_p(\tau) - b_{G,p}$（Equation 2）。这本质上是**将全局奖励归一化到角色特定的期望水平**，消除了因位置不对称（如先手/后手）带来的方差。最终梯度更新使用这些角色条件优势代替原始奖励（Equation 3）。

**消融证据。** 移除 RAE 后，模型在约 200 步后发生“思考崩溃”：响应长度从约 2000 字符暴跌至接近零，数学推理准确率从 35% 降至 12%（Figure 9, Section E.2）。Figure 6 进一步显示，标准 REINFORCE 的响应长度和基准性能均崩溃，而 RAE 保持稳定。这表明 RAE 不仅是方差缩减技术，更是**防止多智能体训练中策略退化的必要组件**。

### 3. 推理迁移的因果机制

SPIRAL 声称的核心洞察是：零和博弈的竞争压力**涌现**出结构化推理模式，这些模式通过自我对弈的自动课程效应**无缝迁移**到数学和其他推理任务。论文通过 LLM-as-a-judge 框架追踪了三种核心推理模式在 290 条游戏轨迹和 46,792 个数学解答中的演化：

- **个案分析**（Case-by-Case Analysis）：枚举博弈树分支
- **期望值计算**（Expected Value Calculation）：量化不确定结果的收益
- **模式识别**（Pattern Recognition）：识别棋盘或手牌中的结构特征

Figure 4 显示，期望值计算在训练后期达到 78% 的出现频率，且这些模式在数学解答中的频率与基准得分同步上升（从 31.2 提升至 39.6）。Table 2 给出了具体示例，如 Kuhn 扑克中的期望值计算与数学题中的概率计算使用了相同的推理结构。

**但需注意：** 这一因果链的证据是相关性的（模式频率与得分同步上升），而非干预性的。论文未进行消融实验来证明“若抑制某种推理模式，迁移效果会消失”，因此“推理模式是迁移的因果中介”这一论断需要更谨慎地解读。

### 4. 适用边界与局限

**已验证的适用范围：**
- 三种简单零和博弈：井字棋（完全信息）、Kuhn 扑克（不完全信息）、简单谈判（策略互动）
- 8 个推理基准：MATH500、AIME24/25、Olympiad、AMC-23、Minerva、GPQA-Diamond、MMLU-Pro
- 模型尺度：4B 至 8B 参数（Qwen3、Llama-3.1、Octothinker、DeepSeek-Distill-Qwen 等架构）
- 迁移效果在数学推理（MATH500 +13.2%, AIME24 +10.0%）上最显著，在知识密集型基准（GPQA-Diamond +2.4%, MMLU-Pro +1.3%）上相对有限

**明确的局限：**
1. **游戏复杂度上限未知。** 实验仅覆盖三种简单游戏，尚未验证在更复杂的非零和、部分可观测或多智能体协作场景下的有效性。
2. **迁移的选择性。** 某些基准（如 GPQA-Diamond、MMLU-Pro）的提升幅度有限，表明从游戏到事实性知识的迁移存在瓶颈——游戏训练主要增强结构化推理能力，而非知识检索。
3. **计算成本。** 训练需要 8 块 H100 GPU，Qwen3-4B 约 25 小时，Qwen3-8B 约 28 小时。虽然与基线方法在相同资源约束下比较，但相比标准 SFT 仍显著更高。
4. **RAE 超参数未消融。** 指数移动平均的衰减系数 $\alpha$ 未经系统调优，其对训练稳定性的敏感度未知。
5. **课程调度未探索。** 游戏组合的采样比例和训练顺序可能进一步优化迁移效果，但未被研究。

### 5. 开放问题

1. **SPIRAL 能否扩展到大型非零和游戏或多智能体协作场景？** 零和博弈的对称奖励结构是 RAE 有效的前提——在非零和或混合动机场景中，角色条件基线是否仍然有效，或需要何种新的优势估计方法？

2. **如何形式化游戏技能与推理能力的映射关系？** 当前的选择（井字棋→空间推理，扑克→概率推理，谈判→策略推理）基于直觉。若能建立形式化的技能映射理论，将指导新型训练环境的设计，实现更有针对性的推理能力培养。

3. **自我对弈的均衡胜率是否会导致性能饱和？** 在更长训练步数下，若双方策略收敛至纳什均衡，自动课程效应是否会停滞？是否需要引入种群训练（population-based training）或更先进的课程策略来维持进步动力？

4. **SPIRAL 与 RLVR 的融合潜力。** 将游戏自我对弈与领域特定的可验证奖励交替训练，或通过共享表征联合优化，是否能实现更强的端到端推理能力？这需要解决两种奖励信号的尺度匹配和训练动态协调问题。

5. **推理模式迁移的因果验证。** 当前仅展示了模式频率与性能的相关性。需要干预性实验（如通过提示抑制特定模式，或分析模式出现与否对解题成功率的影响）来建立因果关系。



## 原文 PDF

![[paperPDFs/ICLR_2026/SPIRAL_Self_Play_on_Zero_Sum_Games_Incentivizes_Reasoning_via_Multi_Agent_Multi_Turn_Reinforcement_Learning.pdf]]
