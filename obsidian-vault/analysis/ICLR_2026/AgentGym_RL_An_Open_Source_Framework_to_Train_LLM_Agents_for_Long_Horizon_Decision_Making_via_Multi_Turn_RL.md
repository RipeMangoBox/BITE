---
title: "AgentGym-RL: An Open-Source Framework to Train LLM Agents for Long-Horizon Decision Making via Multi-Turn RL"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AgentGym_RL_An_Open_Source_Framework_to_Train_LLM_Agents_for_Long_Horizon_Decision_Making_via_Multi_Turn_RL.pdf
openreview_forum_id: ZgCCDwcGwn
aliases:
- SR
- AgentGym-RL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "渐进式交互轮次扩展策略（progressive horizon-scaling strategy）"
primary_logic: "通过从短交互轮次开始训练建立基础策略，再逐步扩展最大交互轮次，可以在保持训练稳定性的同时，引导智能体进行更深层次的探索，最终实现更高的长期性能。"
claims:
- "ScalingInter-RL 在多样化的 27 个任务上一致且显著地提升性能，Qwen-2.5-7B 平均提升 33.65 分，超越多个商用模型。"
- "直接使用长交互轮次（如10轮）会导致训练崩溃，而短轮次训练性能有限；渐进式扩展轮次（ScalingInter-RL）在保持稳定的同时获得更高奖励。"
- "在 TextCraft 上，ScalingInter-7B 相比基础模型提升近 50 分（91.00 vs 42.00），达到顶尖水平。"
- "ScalingInter-RL 对交互轮次列表和阶段转换频率等超参数不敏感，表现出很强的鲁棒性。"
---

# AgentGym-RL: An Open-Source Framework to Train LLM Agents for Long-Horizon Decision Making via Multi-Turn RL

> [!tip] 核心洞察
> 通过从短交互轮次开始训练建立基础策略，再逐步扩展最大交互轮次，可以在保持训练稳定性的同时，引导智能体进行更深层次的探索，最终实现更高的长期性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AgentGym-RL：一个训练LLM智能体进行长周期多轮决策的开源框架 |
| 英文题名 | AgentGym-RL: An Open-Source Framework to Train LLM Agents for Long-Horizon Decision Making via Multi-Turn RL |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ZgCCDwcGwn); [GitHub](https://github.com/WooooDyy/AgentGym-RL) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | ScalingInter-RL |
| Dataset | TextCraft, WebArena, Deep Search |

> [!tip] 效果简介
> - TextCraft 上，Overall Score 为 91.00 (ScalingInter-7B)，对比 42.00 (Qwen2.5-7B-Instruct)，变化 +49.00。
> - WebArena 上，Overall Accuracy 为 26.00 (ScalingInter-7B)，对比 16.00 (GPT-4o)，变化 +10.00。
> - Deep Search 上，Overall Score 为 38.3 (ScalingInter-7B)，对比 18.8 (Qwen2.5-7B-Instruct)，变化 +19.5。

## 概述

**问题瓶颈**：在长周期多轮决策任务中对大语言模型（LLM）智能体进行强化学习（RL）训练时，直接增加交互轮次会导致训练不稳定甚至崩溃，而限制交互轮次又会使性能过早饱和，难以完成复杂任务。

**核心方法**：本文提出 **ScalingInter-RL**，一种渐进式交互轮次扩展策略。该方法从短交互轮次开始训练以建立稳定的基础策略，随后按单调课程表逐步扩展最大交互轮次，在保持训练稳定性的同时引导智能体进行更深层次的探索，最终实现更高的长期性能。整个训练流程由开源框架 **AgentGym-RL** 承载，该框架采用环境、智能体、训练三大模块的解耦架构，支持多种主流 RL 算法和真实场景。

**关键结果**：
- 在覆盖 27 个任务的多样化基准上，基于 Qwen-2.5-7B 训练的 ScalingInter-RL 智能体平均提升 **33.65 分**，性能达到甚至超越 OpenAI o3、Gemini-2.5-Pro 等商用模型（Figure 1）。
- 在 TextCraft 上，ScalingInter-7B 相比基础模型提升近 **50 分**（91.00 vs 42.00），达到顶尖水平（Table 6）。
- 在 WebArena 上，ScalingInter-7B 以 **26.00** 的总体准确率超越 GPT-4o 的 16.00（Table 5）。
- 在 Deep Search 上，ScalingInter-7B 取得 **38.3** 分，显著优于基线的 18.8 分（Table 1）。
- 消融实验表明，ScalingInter-RL 对交互轮次列表和阶段转换频率等超参数不敏感，性能稳定在 36.8~39.1 之间（Table 3）。

**方法定位**：ScalingInter-RL 属于基于课程学习的在线 RL 训练策略，其核心调控变量为最大交互轮次的单调递增调度。与固定轮次的 **ReAct**（Yao et al., 2023）和 **SearchR1**（Jin et al., 2025b）等基线不同，该方法通过分阶段扩展交互预算来化解长周期训练的不稳定性。AgentGym-RL 框架则为上述训练提供了统一的轨迹收集、优势估计和策略优化流水线。

**局限与开放问题**：
- 在开放域环境（如 WebArena）中，RL 训练的性能提升相对有限，受任务复杂性和噪声反馈制约。
- 在科学推理任务中，RL 智能体仍存在用事实性回忆替代实验步骤的过程性执行失败。
- 所有模型在 SciWorld 的 Chem-Mix 子任务上得分均为零，表明现有方法缺乏处理复杂化学混合过程的能力。
- 长周期训练中的梯度异常与训练崩溃机制仍需进一步分析和缓解。

## 背景与动机

### 问题背景：LLM智能体的长周期决策挑战

以LLM为核心构建的自主智能体，需要在真实或模拟环境中进行多轮交互以完成复杂任务。这类任务可形式化为部分可观测马尔可夫决策过程（POMDP），定义为 $(\mathcal{U}, \mathcal{S}, \mathcal{A}, \mathcal{O}, \mathcal{T}, r)$，其中 $\mathcal{U}$ 为指令空间，$\mathcal{S}$ 为状态空间，$\mathcal{A}$ 为动作空间，$\mathcal{O}$ 为观测空间，$\mathcal{T}$ 为确定性状态转移函数，$r$ 为奖励函数。智能体根据策略 $\pi_\theta$ 在每轮生成动作，环境在多轮交互后给出结果奖励 $r(\tau) \in [0,1]$，RL优化的目标即最大化轨迹奖励的期望：

$$J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} [r(\tau)]$$

在此框架下，策略梯度估计为：

$$\nabla_{\theta} J(\theta) = \mathbb{E}_{\tau \sim \pi_{\theta}} \left[ r(\tau) \sum_{k=0}^{K} \nabla_{\theta} \log \pi_{\theta}(a_k | s_k) \right]$$

尽管RL为训练LLM智能体提供了理论完备的路径，实践中却面临一个核心瓶颈：**直接增加交互轮次进行RL训练会导致训练不稳定甚至崩溃，而限制交互轮次又会使性能达到平台期，难以完成复杂任务。**

### 现有方法缺口

现有方法在处理长周期决策任务时存在明显局限。以 **ReAct**（Yao et al., 2023）为代表的推理-行动范式虽被广泛采用，但其依赖固定的交互轮次设定，无法自适应地应对任务复杂度的变化。**SearchR1**（Jin et al., 2025b）等基于RL的搜索智能体方法，在训练中同样面临交互轮次扩展时的稳定性问题。当直接将最大交互轮次设为较长值（如10轮）时，训练过程往往出现奖励崩溃；而使用较短轮次（如5轮）虽能保持稳定，却导致性能过早饱和，无法完成需要深度探索的长周期任务。

这一困境的本质在于：长周期任务要求智能体在更长的动作序列中维持一致的策略质量，而RL训练的方差随轨迹长度增长急剧放大，使得梯度信号变得不可靠。

### 本文动机

为突破上述瓶颈，本文提出两个核心贡献：

1. **AgentGym-RL框架**：一个模块化、解耦的开源框架，专门面向多轮决策任务中的RL训练。该框架将环境、智能体和训练三大模块清晰分离（见Figure 2），支持主流RL算法，覆盖深度搜索、网页导航、文本合成、科学实验等多种真实场景。

2. **ScalingInter-RL方法**：一种渐进式交互轮次扩展策略，作为破解长周期训练不稳定的关键机制。其核心思路是从短交互轮次开始训练以建立基础策略，再按课程表逐步扩展最大交互轮次，在保持训练稳定性的同时引导智能体进行更深层次的探索，最终实现更高的长期性能。

实验表明，基于ScalingInter-RL训练的Qwen-2.5-7B模型在27个多样化任务上平均提升33.65分，性能达到甚至超越OpenAI o3、Gemini-2.5-Pro等商用模型（见Figure 1）。

## 核心创新

本工作针对**长周期多轮决策中 RL 训练的根本瓶颈**提出解决方案：直接增加交互轮次进行 RL 训练会导致训练不稳定甚至崩溃，而限制交互轮次又会使性能达到平台期，难以完成复杂任务。其核心创新在于提出 **ScalingInter-RL**，一种**渐进式交互轮次扩展策略**（progressive horizon-scaling strategy）。

### 关键 changed slot：最大交互轮次调度

与现有方法相比，ScalingInter-RL 在训练范式上引入了一个关键的 **changed slot**：

| 维度 | 基线方法 | ScalingInter-RL |
|------|----------|-----------------|
| 最大交互轮次调度 | 固定轮次（如 5 或 10） | 从短到长的渐进扩展（如 [5, 8, 10]） |

具体而言，基线方法（如直接使用 ReAct 范式配合固定交互轮次的 RL 训练）面临两难困境：短轮次训练（如 5 轮）虽稳定但性能有限，长轮次训练（如 10 轮）则因探索空间急剧增大导致训练崩溃（见 Figure 4）。ScalingInter-RL 通过引入单调递增的交互轮次调度 $h_{t+1} = h_t + \delta_h$，在每 $\Delta$ 训练步后更新最大交互轮次，从短周期开始建立基础策略，再逐步引导智能体进行更深层次的探索。

### 核心机制：从 exploitation 到 exploration 的平滑过渡

ScalingInter-RL 的**核心洞察**在于：训练初期限制交互轮次使智能体专注于 exploitation，通过较简单的任务掌握基础解题技能；随着轮次逐步扩展，智能体在已有策略基础上进行更深度的 exploration，从而在保持训练稳定性的同时，最终实现更高的长期性能。这一机制通过条件轨迹采样 $\tau_t \sim \pi_{\theta}(\tau \mid h_t), \ \text{subject to } K_t \le h_t$ 实现，确保每个训练阶段的交互轮次不超过当前最大轮次 $h_t$。

### 证据强度

该创新的有效性得到多层次验证：

- **因果证据**：Figure 4 直接展示了不同最大交互轮次下的训练动态——固定 10 轮导致训练崩溃，而 ScalingInter-RL 在保持稳定的同时获得更高奖励（置信度 0.95）。
- **性能证据**：在 TextCraft 上，ScalingInter-7B 相比基础模型提升近 50 分（91.00 vs 42.00），达到顶尖水平（置信度 0.98）；在 27 个多样化任务上，Qwen-2.5-7B 平均提升 33.65 分（置信度 0.95）。
- **鲁棒性证据**：消融实验表明，ScalingInter-RL 对交互轮次列表和阶段转换频率等超参数不敏感，多种配置下性能均在 36.8~39.1 之间（置信度 0.99）。

### 与框架设计的关系

ScalingInter-RL 的提出与 AgentGym-RL 框架的模块化设计形成互补。框架通过解耦的环境模块、智能体模块和训练模块，为 RL 训练提供了统一的流水线；而 ScalingInter-RL 作为训练策略层面的创新，可在该框架内与多种 RL 算法（GRPO、REINFORCE++、PPO）结合使用，展现出良好的算法无关性（见 Table 4）。

## 整体框架

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/003_Figure_4.jpg]]
*Figure 4: Training dynamics under different maximum interaction turns in Deep Search environment. Our ScalingInter-RL method progressively increases the interaction horizon, and ultimately achieves higher and more efficient long-term performance*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/005_Figure_6.jpg]]
*Figure 6: Training rewards in different environments leveraging AgentGym-RL framework with the ScalingInter-RL method*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the AgentGym-RL framework. It features a decoupled, flexible, and extensible architecture, comprising three primary modules—the environment, the agent, and the training module. It supports diverse scenarios, environments, and algorithms*

AgentGym-RL 采用解耦、灵活、可扩展的模块化设计，将基于 RL 的 LLM 智能体训练流水线划分为三个核心模块：**环境模块（Environment Module）**、**智能体模块（Agent Module）** 和 **训练模块（Training Module）**。三者通过明确定义的接口协作，完整覆盖从环境交互到策略优化的 RL 全生命周期（见图 2 和图 3）。

### 模块职责与交互流

**环境模块**将每种任务环境封装为独立服务，通过 HTTP 暴露统一的 API 接口（如 `/observation`、`/step`），支持 Web 导航、科学推理、文本合成等多种真实场景。**智能体模块**负责封装 LLM 的推理–行动循环：接收环境返回的观测，基于当前策略生成动作（如调用工具、执行搜索），并将动作发送回环境。**训练模块**则管理轨迹收集、优势估计、策略优化和奖励塑形等完整的 RL 训练流水线，支持 GRPO、REINFORCE++、PPO 等主流在线/离线算法。

整个交互流程可形式化为部分可观测马尔可夫决策过程（POMDP）：给定任务指令 $u \in \mathcal{U}$，智能体在状态 $s_k$ 下根据策略 $\pi_\theta$ 采样动作 $a_k$，环境返回观测 $o_{k+1}$ 和状态 $s_{k+1}$。经过 $N$ 轮交互后，环境给出结果奖励 $r(\tau) \in [0, 1]$，RL 优化的目标即最大化轨迹奖励期望：

$$J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} [r(\tau)]$$

策略梯度估计采用基础形式：

$$\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta} \left[ r(\tau) \sum_{k=0}^{K} \nabla_\theta \log \pi_\theta(a_k | s_k) \right]$$

### 核心瓶颈与 ScalingInter-RL

直接增加交互轮次进行 RL 训练存在根本性矛盾：短轮次训练使性能迅速达到平台期，无法完成复杂任务；而直接使用长轮次（如 10 轮）则会导致训练不稳定甚至崩溃（见图 4）。**ScalingInter-RL** 通过**渐进式交互轮次扩展策略**解决了这一瓶颈：训练从短交互轮次开始，迫使智能体先掌握基础任务解决技能，随后按单调递增的轮次调度表逐步扩展最大交互轮次。

具体而言，在第 $t$ 阶段，轨迹采样受限于当前最大轮次 $h_t$：

$$\tau_t \sim \pi_\theta(\tau \mid h_t), \quad \mathrm{subject\ to\ } K_t \le h_t$$

每 $\Delta$ 训练步后，按递增步长 $\delta_h$ 更新轮次上限：

$$h_{t+1} = h_t + \delta_h$$

该策略在保持训练稳定性的同时，引导智能体进行更深层次的探索，最终实现更高的长期性能（见图 4、图 6）。实验表明，ScalingInter-RL 对轮次列表和阶段转换频率等超参数不敏感，多种配置下性能波动极小（Table 3），表现出很强的鲁棒性。

## 核心模块与公式推导

### 多轮决策的形式化建模

AgentGym-RL 将智能体与环境的多轮交互建模为部分可观测马尔可夫决策过程（POMDP），形式化定义为六元组 $(\mathcal{U}, \mathcal{S}, \mathcal{A}, \mathcal{O}, \mathcal{T}, r)$。其中 $\mathcal{U}$ 为任务指令空间，$\mathcal{S}$ 为环境状态空间，$\mathcal{A}$ 为动作空间，$\mathcal{O}$ 为观测空间，$\mathcal{T}$ 为确定性状态转移函数，$r$ 为奖励函数。给定指令 $u \in \mathcal{U}$，智能体在每一轮交互中基于策略 $\pi_\theta$ 生成动作 $a_k \sim \pi_\theta(\cdot | s_k)$，经过 $N$ 轮交互后，环境返回结果奖励 $r(\tau) \in [0, 1]$ 以衡量任务完成程度。

### 策略梯度基础

RL 训练的核心目标为最大化轨迹奖励的期望：

$$J(\theta) = \mathbb{E}_{\tau \sim \pi_{\theta}} [r(\tau)]$$

其中 $\tau$ 为从策略 $\pi_\theta$ 采样得到的完整交互轨迹。基础策略梯度估计采用以下形式：

$$\nabla_{\theta} J(\theta) = \mathbb{E}_{\tau \sim \pi_{\theta}} \left[ r(\tau) \sum_{k=0}^{K} \nabla_{\theta} \log \pi_{\theta}(a_k | s_k) \right]$$

该估计以轨迹奖励 $r(\tau)$ 乘以每一步动作对数概率梯度的期望来更新策略参数 $\theta$。

### 框架三大核心模块

AgentGym-RL 采用解耦的模块化架构，由三个核心模块构成：

**环境模块（Environment Module）**：将每种任务环境封装为独立服务，通过 HTTP 暴露标准化 API（如 `/observation`、`/step`），支持 WebArena、TextCraft、SciWorld 等多种真实场景的接入。该设计使得新环境的添加无需修改智能体或训练模块。

**智能体模块（Agent Module）**：封装 LLM 的推理-行动循环，接收环境观测并输出动作（如 API 调用、工具使用）。模块支持多种提示策略（如 ReAct 范式，Yao et al., 2023）和采样配置，为不同任务提供统一的交互接口。

**训练模块（Training Module）**：提供完整的在线/离线 RL 训练流水线，统一管理轨迹收集、优势估计、策略优化和奖励塑形四个关键环节。框架原生支持 GRPO 和 REINFORCE++ 等主流算法，其中 GRPO 以同一查询的多条轨迹均值作为基线计算优势，而 REINFORCE++ 在批次内进行归一化。

### ScalingInter-RL 的渐进式轮次扩展

针对直接使用长交互轮次训练导致的不稳定甚至崩溃问题，ScalingInter-RL 引入渐进式交互轮次扩展策略。其核心思想是将训练划分为多个阶段，每个阶段 $t$ 设定最大交互轮次 $h_t$，轨迹采样受此约束：

$$\tau_t \sim \pi_{\theta}(\tau \mid h_t), \quad \mathrm{subject\ to\ } K_t \le h_t$$

其中 $K_t$ 为实际交互轮次。阶段间的轮次更新遵循单调递增的课程调度：

$$h_{t+1} = h_t + \delta_h$$

每 $\Delta$ 训练步后按增量 $\delta_h$ 提升最大交互轮次。训练从短轮次（如 5 轮）开始，使智能体先掌握基础任务求解技能，再逐步扩展至更长轮次（如 8 轮、10 轮），在保持训练稳定性的同时引导更深层次的探索。

## 实验与分析

### 核心瓶颈与动机验证

AgentGym-RL 的实验设计首先回答一个根本问题：**直接扩展交互轮次进行 RL 训练为何不可行？** 如 Figure 4 所示，在 Deep Search 环境中，当最大交互轮次固定为 10 轮时，训练奖励在早期阶段即出现剧烈振荡并最终崩溃。相反，将轮次限制在 5 轮虽然训练稳定，但性能迅速达到平台期，无法完成需要深层探索的复杂任务。这一现象揭示了长周期 RL 训练的核心矛盾：**交互轮次不足则探索深度受限，交互轮次过长则训练不稳定**。

ScalingInter-RL 的渐进式轮次扩展策略（progressive horizon-scaling strategy）正是针对这一瓶颈设计的因果调节变量。通过从短轮次（如 5 轮）开始建立基础策略，再按单调递增调度逐步扩展至 8 轮、10 轮，该方法在保持训练稳定性的同时，引导智能体进行更深层次的探索。Figure 4 的训练动态曲线清晰地展示了这一效果：ScalingInter-RL 的奖励曲线平滑上升，最终超越了所有固定轮次配置的峰值性能。

### 主要结果

#### Deep Search 基准

Table 1 展示了 Deep Search 基准上的全面对比。ScalingInter-7B（基于 Qwen2.5-7B-Instruct）以 **38.3 的 Overall 分数**位列“Our RL Models”组最佳，相较于基础指令模型 Qwen2.5-7B-Instruct 的 18.8 分提升了 19.5 分。值得注意的是，该分数超越了多个更大规模的开源模型，包括 Qwen2.5-72B-Instruct（35.0）和 Llama-3.1-70B-Instruct（32.5），并与部分商用模型形成竞争。AgentGym-RL-7B（未使用渐进式轮次扩展）也取得了 34.0 分，验证了 RL 训练本身的收益，但 ScalingInter-RL 的额外提升证实了轮次调度策略的独立贡献。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/006_Table_1.jpg]]
*Table 1: Evaluation results on Deep Search benchmark. For each group, the best result is in bold, and the second-best is underlined. SearchR1-it-v0.3 baseline uses Search-R1-v0.3 models (Jin et al., 2025a). See Appendix D for results of tasks on other scenarios*

#### WebArena 基准

在 WebArena 这一开放域网页导航基准上（Table 5），ScalingInter-7B 取得了 **26.00 的 Overall Accuracy**，显著优于基础模型的 16.00（提升 10 个百分点），并超越了 GPT-4o 的 16.00。这一结果尤为值得关注，因为 WebArena 涉及真实网页交互，任务复杂性和噪声反馈远高于受控环境。然而，相较于 TextCraft 等封闭环境，提升幅度相对有限，这暗示了开放域 RL 训练中奖励函数设计和环境反馈质量的瓶颈。

#### TextCraft 基准

Table 6 展示了 TextCraft 基准上的结果，这是性能提升最显著的场景。ScalingInter-7B 取得了 **91.00 的 Overall Score**，相较于 Qwen2.5-7B-Instruct 的 42.00 分提升了近 50 分（+49.00），达到了与商用顶尖模型相当的水平。按合成深度分层分析，ScalingInter-7B 在所有深度级别上均保持优势，表明渐进式轮次训练不仅提升了浅层任务的执行效率，更赋予了智能体处理深层合成任务的能力。

#### SciWorld 基准

Table 8 展示了 SciWorld 科学推理基准上的结果。RL 训练带来了巨大提升，ScalingInter-7B 在多个子任务上从接近零分提升至满分或接近满分。然而，所有模型在 **Chem-Mix（chemistry-mix）子任务上得分均为零**，暴露了现有方法在处理复杂化学混合过程时的根本性能力缺失——智能体倾向于用事实性回忆替代应有的逐步实验操作，而非真正执行程序性科学推理。

### 消融实验

Table 3 的消融研究验证了 ScalingInter-RL 对超参数的鲁棒性。实验测试了不同的交互轮次列表（如 [5,8,10]、[5,10] 等）和阶段转换频率配置，结果显示各配置下的性能波动极小，均在 **36.8 至 39.1** 的狭窄区间内。这一鲁棒性得益于阶段化设计：只要遵循“由短到长”的渐进原则，具体的轮次递增步长和转换时机对最终性能影响有限，降低了实际部署中的调参负担。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/009_Table_3.jpg]]
*Table 3: Ablation study of ScalingInter-RL*

### 算法兼容性

Table 4 展示了 ScalingInter-RL 与不同 RL 算法的兼容性。在 TextCraft、BabyAI 和 SciWorld 三个基准上，将渐进式轮次扩展策略应用于 PPO 和 REINFORCE++ 均带来了显著收益，ScalingInter-7B 一致优于未使用该策略的 AgentGym-RL-7B。这表明 ScalingInter-RL 是一种**算法无关的训练策略**，而非特定于某一 RL 算法的技巧。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/011_Table_4.jpg]]
*Table 4: Applying ScalingInter-RL to more algorithms*

Table 2 进一步对比了不同 RL 算法的基础性能。GRPO 在 TextCraft（75.00 vs 28.00）、BabyAI 和 Deep Search 上均显著优于 REINFORCE++，这归因于 GRPO 使用多条轨迹的均值作为基线进行优势估计，有效降低了梯度方差；而 REINFORCE++ 仅在批次内进行归一化，在高方差的长周期任务中容易导致训练不稳定。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/008_Table_2.jpg]]
*Table 2: Evaluation results of different RL algorithms*

### 测试时交互轮次扩展

Figure 5 展示了测试时交互轮次扩展的效果。所有模型在增加测试轮次后均表现出性能提升，但提升幅度逐渐趋于平台期。关键发现是：**经过 ScalingInter-RL 训练的模型在相同测试轮次下始终优于固定轮次训练的模型**，且其性能平台期出现在更高的水平。这表明渐进式训练不仅提升了策略质量，还使智能体学会了更有效地利用额外的交互预算。

### 失败模式分析

尽管取得了显著的整体提升，实验揭示了若干系统性失败模式：

1. **科学推理中的过程性执行失败**：在 SciWorld 中，RL 智能体虽然能完成部分任务，但经常用事实性知识回忆替代应有的实验步骤。例如，在需要逐步测量和混合的化学任务中，智能体倾向于直接“猜测”结果，而非执行完整的实验流程。

2. **网页导航中的过度交互**：在 WebArena 中，RL 智能体表现出冗余点击和无效滚动行为，缺乏精确高效的动作选择能力。这暗示当前的奖励函数可能未能充分惩罚低效交互，导致智能体采用“暴力探索”策略。

3. **Chem-Mix 任务的零分困境**：所有模型在 SciWorld 的 Chem-Mix 子任务上得分均为零，表明现有 LLM 智能体缺乏处理多步骤、有状态依赖的化学混合过程所需的空间推理和程序记忆能力。这一失败模式指向了当前架构的根本性局限，而非训练策略可解决的问题。

### 效率分析

Figure 8 的效率分析表明，得益于阶段化设计，ScalingInter-RL 在实现更高长期性能的同时，保持了相对较高的训练效率。早期短轮次阶段的快速迭代降低了单步训练成本，而后期长轮次阶段仅在策略已有较好基础时引入，避免了在随机策略阶段浪费大量计算资源进行深度探索。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/010_Figure_8.jpg]]
*Figure 8: Analysis of computational resources and efficiency*

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/001_Figure.jpg]]

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/019_Figure_12.jpg]]
*Figure 12: Comparison of our RL agent with the base agent on the BabyAI task. Our RL model significantly outperforms the base model, successfully navigating to the blue box while the base model fails to complete the task*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/022_Figure_15.jpg]]
*Figure 15: RL agent vs. Base Model on WebArena task. RL agent successfully located the trending post and completed the subscription, achieving a score of 1.0., while the base model scores 0.0*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_ZgCCDwcGwn/figures/023_Figure_16.jpg]]
*Figure 16: Trajectory visualization in the WebArena task, highlighting the agent’s path through the environment, action execution, and feedback*

## 方法谱系与知识库定位

### 与现有工作的关系

**ScalingInter-RL** 处于 LLM Agent 强化学习训练的交叉地带，其核心贡献——渐进式交互轮次扩展策略——填补了“固定短轮次训练性能受限”与“直接长轮次训练不稳定”之间的空白。

从方法谱系看，本工作建立在以下基线之上：

- **ReAct** (Yao et al., 2023) 确立了推理-行动交替的通用交互范式，AgentGym-RL 框架中的 Agent Module 本质上遵循这一范式，在每轮交互中接收观测并输出动作。
- **SearchR1** (Jin et al., 2025b) 代表了此前基于 RL 的搜索 Agent 方法，在 Deep Search 基准上作为直接对比基线（Table 1 中 SearchR1-it-v0.3）。
- 基础指令模型 **Qwen2.5-7B-Instruct** (Yang et al., 2024) 作为未经 RL 训练的基线，在 TextCraft 上仅得 42.00 分，而 ScalingInter-7B 达到 91.00 分（Table 6），提升近 50 分。

在 RL 算法层面，ScalingInter-RL 并非一种新算法，而是一种**训练调度策略**，可叠加于多种 on-policy RL 算法之上。实验验证了其与 **GRPO**、**PPO** 和 **REINFORCE++** 的兼容性（Table 4），且 GRPO 在多数场景下表现最优（Table 2，TextCraft 上 GRPO 75.00 vs REINFORCE++ 28.00，3B 模型）。

### 适用边界与局限

尽管 ScalingInter-RL 在 27 个任务上取得了一致且显著的提升，其适用边界和局限同样明确：

1. **开放域环境的提升有限**：在 WebArena 上，ScalingInter-7B 达到 26.00 的总体准确率，虽超越 GPT-4o（16.00），但绝对值仍然较低（Table 5）。任务复杂性和环境反馈的噪声制约了 RL 训练的效果上限。

2. **科学推理中的过程性失败**：RL Agent 在 SciWorld 等需要严格程序性执行的任务中，容易用事实性回忆替代应有的实验步骤，暴露出逐步推理与实验能力的不足。

3. **网页导航中的过度交互**：RL Agent 表现出冗余点击、滚动等低效行为，缺乏精确高效的动作选择能力，说明奖励信号未能有效引导交互效率。

4. **极端子任务的零分困境**：所有模型在 SciWorld 的 Chem-Mix 子任务上得分均为零，表明现有方法（包括 ScalingInter-RL）完全缺乏处理复杂化学混合过程的能力，这指向了当前 LLM Agent 在特定领域知识推理上的根本性缺失。

5. **长周期训练的稳定性边界**：虽然渐进式扩展策略有效缓解了训练崩溃，但 Figure 4 显示直接使用 10 轮交互仍会导致崩溃，说明该方法是在稳定性与探索深度之间的折中方案，而非根本解决了长周期 RL 的不稳定问题。

### 开放问题

1. **长周期 RL 稳定性的根本解决**：ScalingInter-RL 通过课程调度规避了训练崩溃，但如何从梯度估计、优势归一化或探索策略层面根本性地解决长周期 RL 的不稳定性，仍是开放问题。GRPO 的 per-query 基线归一化优于 REINFORCE++ 的 batch 内归一化（Table 2），暗示方差控制是一个关键方向。

2. **程序性执行能力的培养**：在 SciWorld 等科学任务中，如何让 RL Agent 学会严格的逐步推理与实验执行，而非依赖事实性记忆，需要新的奖励塑形策略或辅助训练信号。

3. **开放域奖励函数设计**：WebArena 等环境缺乏密集、信息丰富的奖励信号，如何设计更有效的环境反馈以引导高效探索，是提升开放域性能的关键瓶颈。

4. **Chem-Mix 等极端子任务的突破路径**：所有模型在此类任务上得分为零，背后缺失的具体能力是什么？是化学知识的深层推理、多步合成规划，还是对实验操作序列的精确建模？这需要从任务设计和模型能力两个维度进行诊断。

5. **交互效率与任务完成度的权衡**：Figure 5 显示增加测试时交互轮次能提升性能但存在平台期，而 RL Agent 又表现出过度交互问题。如何在训练阶段引导 Agent 学习高效的动作选择，而非单纯依赖更多交互轮次，是一个值得深入的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/AgentGym_RL_An_Open_Source_Framework_to_Train_LLM_Agents_for_Long_Horizon_Decision_Making_via_Multi_Turn_RL.pdf]]
