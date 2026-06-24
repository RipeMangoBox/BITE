---
title: "Adaptive Collaboration with Humans: Metacognitive Policy Optimization for Multi-Agent LLMs with Continual Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Adaptive_Collaboration_with_Humans_Metacognitive_Policy_Optimization_for_Multi_Agent_LLMs_with_Continual_Learning.pdf
openreview_forum_id: IKVUB9Exuc
aliases:
- HLMACHDLPOD
- ACHMPOMALCL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过元认知策略控制智能体何时自主推理、何时求助人类专家，并将专家反馈通过持续学习转化为模型能力的长期提升。"
primary_logic: "将人机协作从被动求助升级为策略性元认知框架，使智能体学会权衡自主求解的风险与求助的成本，同时利用专家反馈持续扩展知识边界，而非仅作一次性修复。"
claims:
- "HILA在LLaMA3-8B骨干上全面超越最强自主MAS基线，在GSM8K上达到89.86%（+17.10），AMC 35.83%（+24.47），HumanEval 72.15%（+24.59），MMLU 73.62%（+15.63）。"
- "去除双环中的外环（仅GRPO）导致性能增长平庸，而完整DLPO带来第二阶段大幅提升，表明长期能力增长主要源于外环将专家反馈转化为监督信号。"
- "跨骨干实验显示HILA在不同家族（Qwen、LLaMA）和规模（3B-8B）上均表现最优，具有泛化性。"
- "真实人类专家（博士研究生）作为反应式专家时，HILA性能进一步提升（GSM8K 78.67%，AMC 61.67%，MMLU 75.33%），且主动提供完整推理路径可极大提高准确率。"
---

# Adaptive Collaboration with Humans: Metacognitive Policy Optimization for Multi-Agent LLMs with Continual Learning

> [!tip] 核心洞察
> 将人机协作从被动求助升级为策略性元认知框架，使智能体学会权衡自主求解的风险与求助的成本，同时利用专家反馈持续扩展知识边界，而非仅作一次性修复。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 与人自适应协作：多智能体LLM的元认知策略优化与持续学习 |
| 英文题名 | Adaptive Collaboration with Humans: Metacognitive Policy Optimization for Multi-Agent LLMs with Continual Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IKVUB9Exuc); [GitHub](https://github.com/USC-Melady/HILA.git) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Human-In-the-Loop Multi-Agent Collaboration (HILA) with Dual-Loop Policy Optimization (DLPO) |
| Dataset | GSM8K, AMC, AIME, HumanEval |

> [!tip] 效果简介
> - GSM8K 上，Solve Rate (%) 为 89.86，对比 G-Swarm (84.89)，变化 +4.97。
> - AMC 上，Solve Rate (%) 为 35.83，对比 G-Debate (20.48)，变化 +15.35。
> - AIME 上，Solve Rate (%) 为 9.37，对比 G-Swarm (5.78)，变化 +3.59。

## 概述

### 问题瓶颈

自主多智能体系统（MAS）在数学推理、代码生成等需要深度认知的任务上已取得显著进展，但其能力受限于预训练知识的封闭世界。当面对需要领域专长、实时信息或超出训练分布的未见语境时，这些系统缺乏生成新知识或自适应调整的能力，容易发生集体性失败。现有的人机协作方案多将人类定位为被动监督者或基于启发式阈值的求助对象，未能将人类专家的反馈转化为模型能力的长期增长。

### 核心思路

HILA（Human-In-the-Loop Multi-Agent Collaboration）将人机协作从被动求助升级为**策略性元认知框架**。其核心洞察是：让智能体学会权衡自主求解的风险与求助的成本，而非简单地执行固定协作协议。具体而言，HILA为每个智能体引入一个元认知策略，在每一轮交互中动态选择三种高层认知动作——**EVAL**（评估并采纳同伴方案）、**CREATE**（自主生成新方案）、**DEFER**（策略性求助人类专家）。当触发DEFER时，人类专家的反馈不仅用于当前任务的即时修复，更被存储为监督信号，通过持续学习扩展模型的知识边界。

为解耦即时决策与长期能力增长，本文提出**双环策略优化（DLPO）**：
- **内环**：使用组相对策略优化（GRPO）配合成本感知奖励函数，训练元认知策略在自主求解与求助之间做出最优权衡。
- **外环**：将DEFER触发的人类专家演示转化为监督微调（SFT）数据，持续更新基础模型，使专家知识内化为模型的永久能力。

### 方法定位

HILA区别于现有工作的三个关键设计维度：

| 设计维度 | 现有MAS基线 | HILA |
|---------|-----------|------|
| **交互协议** | 固定工作流或预定义角色（辩论、拓扑控制） | GRPO优化的元认知策略动态决策（EVAL/CREATE/DEFER） |
| **人类参与** | 被动监督或启发式阈值求助 | 策略性DEFER调用，反馈用于持续学习 |
| **模型适应** | 静态模型，仅依赖上下文推理 | 外环持续学习（SFT on expert demos）更新基础模型 |

在方法谱系中，HILA位于**多智能体协作**、**人在回路学习**与**持续学习**的交汇点。与LLM-Debate、GPTSwarm等纯自主MAS相比，HILA引入了策略性人类求助机制；与传统人在回路方法相比，HILA将人类反馈从一次性修复升级为持续能力增长的驱动力。

### 主要结果

在LLaMA3-8B骨干上，HILA全面超越最强自主MAS基线：

- **GSM8K**：89.86%（+4.97 vs GPTSwarm 84.89%，+17.10 vs Vanilla）
- **AMC**：35.83%（+15.35 vs G-Debate 20.48%，+24.47 vs Vanilla）
- **HumanEval**：72.15%（+9.95 vs AFlow 62.20%，+24.59 vs Vanilla）
- **MMLU**：73.62%（+3.73 vs G-Debate 69.89%，+15.63 vs Vanilla）
- **AIME**：9.37%（+3.59 vs GPTSwarm 5.78%）

跨骨干实验（Qwen2.5-7B/3B、LLaMA3-8B/3B）验证了方法的泛化性。消融实验揭示：仅使用内环GRPO带来的性能增长平庸，而完整DLPO的外环持续学习是性能大幅提升的关键驱动力——它将专家反馈转化为基础模型能力的永久增益，使DLPO更新后的骨干即使在其他推理框架（Vanilla、DyLAN、Debate）上也一致提升。真实人类专家（20名博士研究生）参与实验进一步验证了框架的有效性：主动提供完整推理路径可将GSM8K提升至90.67%，AMC至65.83%，MMLU至86.67%。

### 局限与开放问题

当前方法依赖高质量领域专家，真实部署中专家可用性可能受限；使用GPT-4o-mini作为人类代理虽经济，但与真实人类直觉存在差异；双环训练增加了计算与工程复杂度。开放问题包括：如何引入更精细的元认知评估（如贝叶斯不确定估计）取代规则启发式？能否设计完全自监督机制使智能体在无外部专家时自主判断何时放弃并学习？长期持续学习下如何避免灾难性遗忘？

## 背景与动机

### 自主多智能体系统的知识边界

大型语言模型驱动的多智能体系统（MAS）近年来在数学推理、代码生成、知识问答等任务上取得了显著进展。通过引入辩论、拓扑控制、动态网络等协作协议，这些系统能够在一定程度上超越单智能体的表现。然而，这类系统的核心瓶颈在于：**所有智能体共享同一封闭世界的预训练知识**。当任务需要领域专长、实时信息或超出训练分布的新知识时，智能体集体陷入知识盲区，无法生成有效推理，更无法自主突破这一知识上限。现有方法无论协作机制如何精巧，本质上仍是在封闭知识空间内重新排列组合，而非真正扩展系统的认知边界。

### 现有人机协作的被动性

将人类引入协作回路是突破上述瓶颈的自然思路。但在现有范式中，人类通常扮演两种角色：一是**被动监督者**，仅在最终输出阶段进行审核或矫正；二是**基于启发式阈值的求助对象**，由预设规则（如置信度低于某阈值）触发求助。这两种模式存在共同缺陷：人类反馈是**一次性修复**，模型不会从中学习，下次遇到同类问题仍会重复求助；求助决策缺乏策略性，无法权衡自主求解的风险与求助的成本；人类知识无法转化为模型能力的持久增长。

### 从被动求助到元认知策略

本文的核心动机在于**将人机协作从被动求助升级为策略性元认知框架**。具体而言，我们提出两个关键转变：

1. **决策层面**：赋予智能体一个可学习的元认知策略，使其能够动态评估当前认知状态，在自主求解（EVAL/CREATE）与求助人类专家（DEFER）之间做出成本感知的最优决策。这类似于人类的元认知能力——知道自己何时知道、何时不知道，以及何时需要外部帮助。

2. **学习层面**：将人类专家的反馈通过持续学习机制转化为模型能力的长期提升。当智能体策略性地选择求助时，专家的解答不仅用于当前任务，更被存储为监督信号，通过外环持续微调更新基础模型，逐步扩展其知识边界。这意味着求助频率应随学习进程自然下降——模型真正“学会”了原本不知道的知识。

### 双环解耦的设计动机

上述两个转变对应着不同时间尺度的优化目标：内环的求助决策需要快速适应任务上下文，外环的能力增长需要累积大量专家反馈。因此，我们提出**双环策略优化**（Dual-Loop Policy Optimization, DLPO）来解耦这两个过程——内环通过组相对策略优化（GRPO）训练元认知策略的即时决策能力，外环通过专家演示的监督微调实现基础模型的持续进化。这种解耦使得系统既能灵活应对当前任务的认知挑战，又能将人类智慧沉淀为持久的模型能力，而非仅作一次性修复。

## 核心创新

HILA 的根本创新在于将人机协作从被动求助升级为**策略性元认知框架**，使多智能体系统学会权衡自主求解的风险与求助的成本，而非依赖固定的工作流或启发式阈值。这一转变通过三个关键设计槽位的重新定义实现，并由 Dual-Loop Policy Optimization (DLPO) 统一驱动。

### 1. 交互协议：从固定工作流到元认知策略

现有自主多智能体系统（如 LLM-Debate、G-Debate、GPTSwarm 等）依赖预定义的辩论、拓扑控制或工作流优化协议，智能体行为由静态规则决定，缺乏对“何时应独立求解、何时应求助”的动态判断能力。HILA 将交互协议重构为由 GRPO 优化的元认知策略（Section 3.2.2; Section 3.3.1），智能体在每个协作轮次从三个高层认知动作中动态选择：

- **EVAL**：评估并验证已有解答
- **CREATE**：生成新的候选解答
- **DEFER**：将问题策略性地推迟给人类专家

这一动作空间的设计使智能体的协作行为从“被编排”变为“被学习”。消融实验（Table 3; Table 5）显示，仅应用 GRPO（内环）时，动作分布开始向 EVAL 倾斜，但任务准确率仅有小幅波动；真正的大幅性能提升发生在加入外环持续学习之后，表明**元认知策略本身解决了“何时求助”的控制问题，而能力增长则来自求助后对专家知识的吸收**。

### 2. 人类参与：从被动监督到策略性求助与知识转化

传统人机协作中，人类通常作为被动监督者（标注数据、事后纠错）或基于启发式阈值（如置信度低于某门限）的求助对象。HILA 通过 DEFER 动作将人类参与策略化（Section 3.2.2; Section 3.3.2）：智能体自主评估问题的不确定性与集体能力的边界，仅在自主求解风险过高时才发起求助。

更重要的是，人类反馈在 HILA 中不仅是单次修复，而是**能力增长的燃料**。每次 DEFER 触发的专家演示被转化为监督微调（SFT）样本，通过外环持续学习注入基础模型。跨骨干迁移实验（Table 4）为这一机制提供了决定性证据：用 DLPO 更新后的骨干替换原始 LLaMA3-8B 后，即使在其他推理框架（Vanilla、DyLAN、Debate）上也一致提升，表明**外环学习增强了基础模型本身的能力，而非仅优化了特定协作协议**。

### 3. 模型适应：从静态推理到双环持续学习

现有 MAS 的模型能力是静态的——智能体仅依赖预训练知识和上下文推理，受限于“封闭世界”假设。HILA 通过 DLPO 的双环架构解耦了两个时间尺度的学习（Section 3.3）：

- **内环（GRPO）**：使用成本感知奖励函数 $R(s_t, a_t)$ 优化短期的元认知决策，其中 $C_{\text{defer}} > C_{\text{create}} \geq 0$，鼓励优先选择低成本动作
- **外环（SFT on Expert Demos）**：将 DEFER 触发的人类专家演示转化为监督信号 $\mathcal{L}_{\text{SFT}}(\theta)$，实现长期能力增长

最终目标函数 $\mathcal{L}_{\text{total}}(\theta)$ 将两者统一，通过 $\lambda_{\text{sft}}$ 平衡策略优化与知识获取。消融实验（Table 3）直接验证了这一设计的必要性：从 Init Policy 到 GRPO 再到 DLPO，性能逐步提升，且外环带来的第二阶段增益远超内环单独作用。Table 5 进一步显示，完整 DLPO 训练后 DEFER 比例从初始的 29% 降至 17%（GSM8K），同时 EVAL 升至 55%，表明**模型在吸收专家知识后自主能力增强，对外部干预的依赖同步降低**——这正是元认知策略优化与持续学习协同作用的核心证据。

## 整体框架

![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_IKVUB9Exuc/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed HILA framework and its Dual-Loop Policy Optimization (DLPO) training paradigm. Left: HILA coordinates multi-agent collaboration with both proactive human guidance and reactive expert feedback via metacognitive states and strategic actions (EVAL, CREATE, DEFER). Right: DLPO optimizes the meta-policy in an inner RL loop with cost-aware rewards, and expands the model’s knowledge boundary in an outer continual-learning loop by storing DEFER-triggered human feedback as offline supervision*

HILA（Human-In-the-Loop Multi-Agent Collaboration）框架将人机协作建模为一个**元认知马尔可夫决策过程（Meta-MDP）**，其核心目标是让多智能体系统学会**何时自主求解、何时策略性地求助人类专家**，并将专家反馈转化为模型能力的长期增长。

### 框架总览

HILA由三个关键组件构成，形成一条从感知到决策再到持续学习的完整闭环：

1. **结构化认知状态空间**：每个智能体在每一轮协作中接收一个策略状态 $s_t$，该状态由任务上下文、自身上下文、同伴上下文以及可选的结构化认知信号（社会共识 $\mathbf{z}_t^{\mathrm{soc}}$、元认知监测 $\mathbf{z}_t^{\mathrm{mon}}$、元认知控制 $\mathbf{z}_t^{\mathrm{ctrl}}$）拼接而成（公式1）。这种设计使智能体不仅能感知“问题是什么”，还能感知“自己知道什么”和“同伴在做什么”。

2. **元认知策略与动作空间**：基于状态 $s_t$，每个智能体的元认知策略从三个高层认知动作中选择其一：
   - **EVAL**：评估并验证现有解答的合理性
   - **CREATE**：生成新的候选解答
   - **DEFER**：将问题推迟给人类专家，获取外部知识

   动作选择决定了智能体的输出来源：若为EVAL或CREATE，智能体自主生成输出 $g_{\theta}(s_t)$；若为DEFER，则直接采纳人类专家的解答 $y_{\mathrm{human},t}$（公式2）。

3. **双环策略优化（DLPO）**：这是HILA的核心训练范式，将短期决策优化与长期能力增长解耦为两个相互协同的优化环：
   - **内环（GRPO）**：使用组相对策略优化（Group Relative Policy Optimization）和成本感知奖励函数训练元认知策略。奖励函数对EVAL给予全额正确性奖励，对CREATE和DEFER分别扣除成本 $C_{\mathrm{create}}$ 和 $C_{\mathrm{defer}}$（$C_{\mathrm{defer}} > C_{\mathrm{create}} \geq 0$），鼓励智能体优先选择低成本动作（公式3）。优势函数通过减去组内平均奖励进行中心化（公式4），内环损失结合了策略梯度、KL散度惩罚和熵奖励以确保稳定探索（公式6）。
   - **外环（持续学习）**：当智能体选择DEFER并获得人类专家演示后，系统将该演示转化为监督微调（SFT）样本，使用交叉熵损失更新基础模型（公式7）。这意味着**外环不仅修复当前错误，更将专家知识内化到模型参数中**，使智能体在未来面对类似问题时减少对外部干预的依赖。

最终训练目标将内外环损失统一：仅在智能体采取DEFER动作时才激活外环SFT损失，由超参数 $\lambda_{\mathrm{sft}}$ 平衡两者权重（公式8）。

### 输入输出流

- **输入**：多智能体系统接收一个任务查询，以及可选的人类主动引导（如高层思路或完整推理路径，可在初始化阶段注入）。
- **多轮协作**：在每一轮 $t$，所有 $N$ 个智能体并行接收共享的认知状态 $s_t$，各自采样元认知动作并生成相应输出。协作持续多轮，智能体可观察同伴的输出和动作历史。
- **DEFER触发**：当任一智能体选择DEFER时，系统将当前查询路由至人类专家池，获取反馈后注入协作流程。
- **输出**：系统最终产生一个解答，同时DEFER触发的专家演示被存储为结构化监督数据，供外环持续学习使用。
- **持续更新**：经过DLPO训练后，基础模型的能力边界得到扩展——消融实验表明，用DLPO更新后的骨干替换原始骨干，即使在其他推理框架（如Vanilla、DyLAN、Debate）上也一致提升性能（Table 4），证明外环学习增强了模型本身而非仅优化了特定协作协议。

## 核心模块与公式推导

### 元认知策略状态表示

HILA将人机协作建模为元认知马尔可夫决策过程（Meta-MDP），其核心是智能体在每个协作轮次 $t$ 根据结构化认知状态选择高层策略动作。策略状态 $s_t$ 由以下组件拼接而成：

$$s_t = \mathrm{concat}\big( \mathbf{x}_t^{\mathrm{task}}, \mathbf{x}_t^{\mathrm{self}}, \mathbf{x}_t^{\mathrm{peer}}, \mathbf{z}_t^{\mathrm{soc}}, \mathbf{z}_t^{\mathrm{mon}}, \mathbf{z}_t^{\mathrm{ctrl}} \big)$$

其中 $\mathbf{x}_t^{\mathrm{task}}$ 为任务上下文（问题描述与历史交互），$\mathbf{x}_t^{\mathrm{self}}$ 为智能体自身的推理轨迹，$\mathbf{x}_t^{\mathrm{peer}}$ 为同伴智能体的输出摘要，三者构成基础上下文。可选的结构化认知信号包括：$\mathbf{z}_t^{\mathrm{soc}}$（社会共识，即同伴答案的一致性程度）、$\mathbf{z}_t^{\mathrm{mon}}$（元认知监测，如自身置信度估计）、$\mathbf{z}_t^{\mathrm{ctrl}}$（元认知控制，如历史求助频率）。这些信号以启发式规则计算，为策略提供显式的认知状态线索。

### 策略动作空间与协作输出

动作空间定义为三种高层认知策略：

$$\mathcal{A} = \{a^{\mathrm{eval}}, a^{\mathrm{create}}, a^{\mathrm{defer}}\}$$

- **EVAL**：评估同伴解答的正确性，不生成新内容。
- **CREATE**：自主生成新的推理或解答。
- **DEFER**：判断当前问题超出集体能力边界，触发向人类专家的求助。

基于所选动作，智能体 $i$ 在轮次 $t$ 的输出为：

$$y_{i,t} = \begin{cases} g_{\theta}(s_t), & \text{if } a_{i,t} \in \{a^{\mathrm{eval}}, a^{\mathrm{create}}\}, \\ y_{\mathrm{human},t}, & \text{if } a_{i,t} = a^{\mathrm{defer}}. \end{cases}$$

当动作为 EVAL 或 CREATE 时，智能体通过策略模型 $g_{\theta}$ 自主生成输出；当动作为 DEFER 时，直接采用人类专家提供的解答 $y_{\mathrm{human},t}$，该解答同时被存储为外环持续学习的监督信号。

### 内环：成本感知的GRPO优化

内环采用组相对策略优化（GRPO）训练元认知策略，使智能体学会在自主求解与求助之间做出最优权衡。奖励函数显式编码了动作成本：

$$R(s_t, a_t) = \begin{cases} R_{\mathrm{gt}}(\hat{y}(a_t)), & a_t = \mathrm{EVAL}, \\ R_{\mathrm{gt}}(\hat{y}(a_t)) - C_{\mathrm{create}}, & a_t = \mathrm{CREATE}, \\ R_{\mathrm{gt}}(\hat{y}_{\mathrm{human}}(a_t)) - C_{\mathrm{defer}}, & a_t = \mathrm{DEFER}. \end{cases}$$

其中 $R_{\mathrm{gt}}$ 为任务正确性奖励（答案匹配为1，否则为0），$C_{\mathrm{create}} \geq 0$ 和 $C_{\mathrm{defer}} > 0$ 分别为自主创建和求助的成本，且 $C_{\mathrm{defer}} > C_{\mathrm{create}}$，鼓励智能体优先尝试低成本动作，仅在必要时求助。

GRPO通过组内相对优势进行优化。对于状态 $s_t$ 下采样的 $K$ 个动作 $\{a_1, \dots, a_K\}$，动作 $a_k$ 的优势为：

$$A(s_t, a_k) = R(s_t, a_k) - \frac{1}{K} \sum_{j=1}^{K} R(s_t, a_j)$$

即个体奖励减去组内平均奖励，实现奖励中心化，降低方差。

内环的完整损失函数为：

$$\mathcal{L}_{\mathrm{Inner}} = \mathcal{L}_{\mathrm{PG}} + \beta_{\mathrm{kl}} \mathcal{L}_{\mathrm{KL}} - \beta_{\mathrm{ent}} \mathcal{L}_{\mathrm{Entropy}}$$

其中 $\mathcal{L}_{\mathrm{PG}}$ 为基于优势的策略梯度损失，$\mathcal{L}_{\mathrm{KL}}$ 为KL散度惩罚项（约束策略不偏离参考模型过远），$\mathcal{L}_{\mathrm{Entropy}}$ 为熵奖励项（鼓励探索）。$\beta_{\mathrm{kl}}$ 和 $\beta_{\mathrm{ent}}$ 为对应的权重系数。

### 外环：基于专家演示的持续学习

当智能体选择 DEFER 并获取人类专家的解答 $y_{\mathrm{human}} = (t_1, \dots, t_L)$ 后，该演示被转化为监督微调（SFT）样本。外环通过交叉熵损失将专家知识固化为模型能力：

$$\mathcal{L}_{\mathrm{SFT}}(\theta) = - \sum_{i=1}^{L} \log \pi_{\theta}(t_i \mid s_t, t_{1:i-1})$$

其中 $\pi_{\theta}$ 为当前策略模型，$t_{1:i-1}$ 为前序token。该损失仅对 DEFER 触发的样本生效，使模型学习专家的推理过程，而非简单的答案复制。

### 双环联合优化目标

最终训练目标将内环策略优化与外环知识获取统一：

$$\mathcal{L}_{\mathrm{total}}(\theta) = \mathbb{E}_{(s_t, a_t)} \left[ \mathcal{L}_{\mathrm{Inner}}(\theta) + \lambda_{\mathrm{sft}} \cdot \mathbb{I}(a_t = a^{\mathrm{defer}}) \cdot \mathcal{L}_{\mathrm{SFT}}(\theta) \right]$$

其中 $\mathbb{I}(a_t = a^{\mathrm{defer}})$ 为指示函数，仅在动作为 DEFER 时激活外环SFT损失。$\lambda_{\mathrm{sft}}$ 为平衡系数，控制策略学习与知识获取的相对强度。该设计的核心机制在于：内环决定“何时求助”，外环决定“从求助中学到什么”，两者解耦但协同——内环优化的求助策略为外环筛选高质量学习信号，外环的能力增长又反过来减少未来对求助的依赖。

## 实验与分析

### 核心结果：LLaMA3-8B 主干上的全面领先

Table 1 给出了以 LLaMA3-8B 为统一骨干的完整对比。HILA 在所有五个基准上均取得最优，且相对最强自主 MAS 基线的提升幅度显著：


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_IKVUB9Exuc/figures/002_Table_1.jpg]]
*Table 1: Comparison of baseline and proposed methods using the LLaMA3-8B backbone. All values are percentages (the percent sign is omitted in the table). Values in parentheses denote absolute differences relative to the Vanilla baseline (first row). Underlined numbers indicate the best-performing baseline on each benchmark. “SA” denotes single-agent, and “MA” denotes multi-agent settings*

- **GSM8K**：89.86%（最强基线 G-Swarm 84.89%，+4.97 pp），相对 Vanilla 单智能体提升 17.10 pp。
- **AMC**：35.83%（最强基线 G-Debate 20.48%，+15.35 pp），相对 Vanilla 提升 24.47 pp——这是所有基准中绝对涨幅最大的场景，说明在需要深层数学推理的任务上，策略性求助与持续学习带来的知识增益最为关键。
- **AIME**：9.37%（最强基线 G-Swarm 5.78%，+3.59 pp）。该基准整体得分较低，反映任务本身的高难度，但 HILA 仍保持相对优势。
- **HumanEval**：72.15%（最强基线 AFlow 62.20%，+9.95 pp），相对 Vanilla 提升 24.59 pp，表明元认知策略在程序合成任务上同样有效。
- **MMLU**：73.62%（最强基线 G-Debate 69.89%，+3.73 pp），相对 Vanilla 提升 15.63 pp。

值得注意的是，现有自主 MAS 方法（如 G-Swarm、DyLAN、AFlow 等）虽然在 GSM8K 上能将 Vanilla 的 72.76% 推至 84.89%，但在 AMC 上仅从 11.36% 提升至 20.48%，暴露了封闭世界推理的瓶颈——当任务超出预训练知识覆盖范围时，仅靠智能体间的拓扑重组或辩论协议无法产生新知识。HILA 通过 DEFER 动作打开“开放世界”动态，直接突破这一知识天花板，因此在 AMC 上的边际收益最为突出。

### 跨骨干泛化性

Table 2 在四种 LLM 骨干（LLaMA3-3B/8B、Qwen2.5-3B/7B）上评测 GSM8K。HILA 在所有骨干上均排名第一：Qwen2.5-7B 上达 94.72%，Qwen2.5-3B 上达 91.17%，LLaMA3-3B 上达 83.85%。这表明元认知策略优化与持续学习机制不依赖于特定模型家族或规模，具有较好的泛化能力。


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_IKVUB9Exuc/figures/003_Table_2.jpg]]
*Table 2: Performance of baselines across four LLM backbones on GSM8K. All values are percentages (percent sign omitted). Parentheses show absolute differences (percentage points) relative to the Vanilla row for each backbone. HILA refers to the proposed method with DLPO*

### 消融：双环优化的各自贡献

Table 3 和 Table 5 联合揭示了内环（GRPO）与外环（持续学习）的不同作用。


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_IKVUB9Exuc/figures/005_Table_3.jpg]]
*Table 3: Performance of HILA under progressively stronger training regimes. Init Policy denotes the unoptimized system, GRPO applies only the inner-loop policy optimization, and DLPO adds the outer-loop update from expert demonstrations. The results show that the full dual-loop objective delivers the strongest overall performance. Table 4: Transferability of the backbone updated by DLPO. Base denotes the original LLaMA3-8B backbone, while DLPO denotes the same backbone after DLPO training. For each inference framework, we keep the test-time protocol unchanged and only replace the backbone. All values are percentages*

**仅内环 GRPO（无外环）**：相比未优化的 Init Policy，GRPO 带来的准确率提升有限甚至在某些指标上持平。Table 5 的动作分布变化揭示了其原因——GRPO 的主要效果是调整策略行为：DEFER 占比从 29% 降至 26%（GSM8K）、24% 降至 20%（AMC）、19% 降至 15%（MMLU），EVAL 相应上升。这说明 GRPO 学会了更精准地判断何时求助，但模型本身的知识边界并未扩展，因此任务准确率的增长平庸。

**完整 DLPO（内环 + 外环）**：引入外环持续学习后，性能出现第二阶段跃升。GSM8K 从 GRPO 的约 87% 跳至 89.86%，AMC 从约 27% 跳至 35.83%，MMLU 从约 70% 跳至 73.62%。同时，DEFER 占比进一步大幅下降（GSM8K 17%、AMC 12%、MMLU 5%），EVAL 成为主导动作（分别达 55%、64%、74%）。这揭示了核心因果机制：**外环将人类专家的反馈转化为 SFT 监督信号，使模型内化了原本需要求助才能获得的知识，从而在减少外部依赖的同时提升了自主求解能力。** 换言之，内环决定“何时求助”，外环决定“从求助中学到什么”，两者缺一不可。

**骨干可迁移性**（Table 4）：将 DLPO 更新后的 LLaMA3-8B 骨干替换到 Vanilla、DyLAN、Debate 等不同推理框架中，所有框架的性能均一致提升。例如，Vanilla 在 AMC 上从 11.36% 升至 16.67%，DyLAN 从 18.33% 升至 22.50%。这进一步证实外环学习强化的是基础模型能力本身，而非仅优化特定协作协议。

### 人类专家质量的影响

Table 6 和 Figure 2 展示了外部专家能力对 HILA 性能的单调影响：使用 GPT-4o 作为人类代理时，GSM8K 达 89.76%、AMC 36.67%、MMLU 72.28%；使用较弱的 GPT-3.5-turbo 时则分别降至 86.67%、30.00%、66.28%。这表明 DEFER 的价值高度依赖于专家反馈的质量——更强的专家不仅能纠正错误，其提供的推理路径作为 SFT 数据也更具教学价值。


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_IKVUB9Exuc/figures/013_Table_6.jpg]]
*Table 6: Effect of human proxy capability on HILA. Using stronger language models as the external expert consistently improves performance on GSM8K, AMC, and MMLU, showing that the quality of external guidance is an important factor in the effectiveness of strategic deferral*

真实人类专家实验（Table 11–13）进一步验证了这一趋势。20 名博士研究生组成的人类专家池在独立测试中达到 GSM8K 78.67%、AMC 61.67%、MMLU 75.33%（Table 11）。当他们作为反应式专家（仅在 DEFER 时介入）时，HILA 性能提升至 GSM8K 78.67%、AMC 61.67%、MMLU 75.33%（Table 12）。更重要的是，当人类在协作初始化阶段主动提供完整推理路径（proactive full reasoning）时，准确率进一步提升至 GSM8K 95.33%、AMC 75.00%、MMLU 79.67%（Table 13），且后续 DEFER 请求大幅减少（Figure 12）。这说明**前置的高质量知识注入能有效塑造智能体的初始搜索空间，降低后续求助需求**。


![[assets/figures/papers/paper_list_l28_https_openreview_net_forum_id_IKVUB9Exuc/figures/025_Table_13.jpg]]
*Table 13: Comparison of different real human participation modes under HILA. In the proactive setting, human information is injected before the initial agent reasoning, while GPT-4o remains available as the reactive expert for later DEFER decisions. All values are percentages*

### 协作规模与效率权衡

**智能体数量**（Table 7–8, Figure 3a）：在 AMC 上，智能体数从 1 增至 10，准确率从 26.67% 升至 35.83%，但总 token 消耗从 4,445 飙升至 253,206（约 57 倍）。MMLU 上趋势类似但收益递减更明显：4 个智能体后准确率增长趋于平缓。这表明适度的集体规模（4–6 个智能体）在多数场景下提供了较好的性能-效率平衡点。

**协作轮数**（Table 9–10, Figure 3b）：在 AMC 上，轮数从 1 增至 4，准确率持续提升至峰值，但第 5 轮出现下降——过度迭代引入噪声或冗余信息，反而损害性能。MMLU 上 4 轮同样表现最优。这一非单调模式提示：更深层的迭代不一定更好，元认知策略需要在信息增益与计算开销之间动态权衡。

### 推迟成本作为策略控制旋钮

Figure 7 展示了推迟成本 $C_{\text{defer}}$ 对策略行为的调控作用。随着 $C_{\text{defer}}$ 增大，DEFER 动作占比显著下降，EVAL 占比上升，但任务准确率在适度范围内保持稳定，仅在成本过高时才出现下降。这说明 $C_{\text{defer}}$ 可作为一个实用的控制旋钮：部署者可根据专家可用性和预算，调节系统在“自主性”与“求助频率”之间的偏好，而不必重新训练整个策略。

### 失败模式与局限

1. **专家依赖瓶颈**：当外部专家能力不足（如使用 GPT-3.5-turbo）时，HILA 的性能提升幅度显著收窄，且错误反馈可能通过外环 SFT 被固化。真实部署中高质量领域专家的可用性是关键约束。
2. **过度迭代退化**：协作轮数超过 4 轮后准确率下降，说明当前元认知策略缺乏对“信息已饱和”状态的检测能力，可能在冗余讨论中引入错误共识。
3. **成本-性能的尖锐矛盾**：10 智能体配置下 token 消耗增长近 60 倍，但准确率仅提升约 9 pp（AMC），对于资源受限场景缺乏实用性。
4. **任务覆盖有限**：当前评测集中在数学推理和程序合成等结构化任务，元认知策略在开放域对话、知识密集型问答等场景的有效性未经检验。
5. **启发式认知信号的精度瓶颈**：元认知状态中的社会共识、监测信号等依赖规则启发式，可能在复杂推理场景中给出误导性评估，进一步学习型的认知评估有望提升策略质量。

## 方法谱系与知识库定位

### 核心创新与差异化

HILA的核心创新在于将人机协作从被动求助升级为**策略性元认知框架**。传统多智能体系统（MAS）依赖预定义的工作流或固定角色分配——例如LLM-Debate采用辩论协议，GPTSwarm使用图优化拓扑控制，AgentPrune通过剪枝策略管理智能体——但均将人类定位为被动的监督者或基于启发式阈值的求助对象。HILA的关键突破在于：

1. **元认知策略学习**：通过GRPO优化的策略网络，智能体学会在EVAL（评估）、CREATE（创造）和DEFER（求助）三个高层认知动作之间动态决策，而非遵循固定的交互协议。这一决策基于结构化的认知状态空间，包括任务上下文、自身推理上下文、同伴上下文，以及可选的社会共识、元认知监测和元认知控制信号。

2. **求助即学习**：DEFER动作不仅触发人类专家介入解决当前问题，更重要的是将专家反馈转化为外环持续学习的监督信号。这与传统方法中人类仅提供一次性纠正形成根本差异——HILA的DLPO框架将求助转化为模型能力的**长期增长机制**，而非临时补丁。

3. **双环解耦**：内环（GRPO）优化“何时求助”的策略决策，外环（SFT on expert demos）解决“从求助中学什么”的能力增长问题。消融实验（Table 3, Table 5）明确显示，仅靠GRPO带来的性能增长平庸，而完整DLPO在第二阶段带来大幅提升，证实了外环持续学习是性能突破的关键因果机制。

### 与现有方法的谱系关系

HILA处于**自主MAS**与**人机协作系统**的交汇点，其方法谱系可沿以下维度定位：

- **相对于自主MAS基线**：Vanilla、CoT、SC属于单智能体方法，PHP、LLM-Debate、G-Debate、DyLAN、GPTSwarm、AgentPrune、AFlow属于多智能体方法。这些方法的共同局限在于依赖预训练知识的封闭世界推理，缺乏生成新知识或适应未见语境的能力。HILA通过DEFER动作打破这一封闭性，引入外部专家知识，在GSM8K上相对最强自主基线GPTSwarm提升+4.97个百分点，在AMC上相对G-Debate提升+15.35个百分点（Table 1）。

- **相对于人机协作系统**：传统方法将人类视为基于启发式阈值（如置信度低于某值）的被动求助对象，或作为事后监督者。HILA将人类角色升级为**策略性调用的知识源**，且通过外环持续学习将人类知识内化到模型中。Table 4的迁移实验证明，经过DLPO更新的骨干模型即使在Vanilla、DyLAN、Debate等其他推理框架下也一致提升，说明外环学习增强了基础模型本身的能力，而非仅优化了协作协议。

- **相对于强化学习驱动的LLM优化**：GRPO作为近端策略优化（PPO）的变体，已被用于LLM的偏好对齐。HILA将其应用于元认知动作空间的探索，并通过成本感知奖励函数（$C_{\text{defer}} > C_{\text{create}} \geq 0$）鼓励优先选择低成本自主动作，形成策略性的求助行为。

### 适用边界与局限

1. **专家依赖**：HILA的性能与外部专家质量强相关。Table 6显示，更强的专家代理（GPT-4o > GPT-4o-mini > GPT-3.5-turbo）带来一致的性能提升。真实部署中，高质量领域专家的可用性和响应延迟可能成为瓶颈。使用GPT-4o-mini作为人类代理虽经济可行，但其表现不能完全等同于真实人类专家。

2. **任务域限制**：当前验证集中在数学推理（GSM8K、AMC、AIME）和程序合成（HumanEval）以及知识问答（MMLU）等相对结构化的任务。在开放域对话、创造性写作或需要持续交互的场景中，元认知策略的适用性未经验证。

3. **计算与工程复杂度**：双环训练增加了显著的计算开销——外环需要收集和存储DEFER触发的人类演示，内环需要维护GRPO的组采样和优势估计。Table 7-10显示，增加智能体数量和协作轮数在提升准确率的同时带来急速上升的token成本，存在性能-效率的权衡。

4. **元认知信号的精确性**：当前元认知状态中的启发式信号（如社会共识、元认知监测）可能不够精确。更精细的认知评估机制（如贝叶斯不确定估计）可能进一步提升策略质量，但尚未被纳入框架。

### 开放问题

1. **自监督求助机制**：能否设计完全自监督的机制，使智能体在无外部专家时也能自主判断何时放弃并学习？这需要模型具备更精确的不确定性量化和自我评估能力。

2. **多智能体求助协调**：在大规模部署中，多个智能体可能同时或冗余地向人类求助。如何动态平衡群体内的求助策略，防止冲突或信息过载，是一个开放的协调问题。

3. **跨模态扩展**：元认知框架能否扩展到多模态或具身智能体协作场景？视觉推理、物理交互等任务中的“求助”语义可能与文本推理有本质差异。

4. **灾难性遗忘**：长期持续学习下，外环SFT可能覆盖内环GRPO学到的策略行为，或导致模型在先前擅长的任务上性能退化。如何保持既有能力的同时整合新知识，需要引入更精细的记忆管理机制。

5. **延迟成本建模**：当前成本感知奖励仅考虑静态的动作成本常数。真实人机协作中，人类专家的响应延迟是一个关键变量，需要动态的时间感知成本模型。

## 原文 PDF

![[paperPDFs/ICLR_2026/Adaptive_Collaboration_with_Humans_Metacognitive_Policy_Optimization_for_Multi_Agent_LLMs_with_Continual_Learning.pdf]]
