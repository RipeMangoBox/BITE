---
title: "MARTI: A Framework for Multi-Agent LLM Systems Reinforced Training and Inference"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MARTI_A_Framework_for_Multi_Agent_LLM_Systems_Reinforced_Training_and_Inference.pdf
openreview_forum_id: E7jZqo0A50
aliases:
- MMARTI
- MARTI
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "采用多智能体强化学习（MARL）进行集中式交互、分布式策略训练，并结合基于历史表现对比的奖励塑形（delta-style reward shaping）来稳定多轮协作训练。"
primary_logic: "在相同推理预算下，通过多智能体强化学习训练，多智能体系统能够超越单智能体系统的性能上限；奖励塑形对于稳定多智能体多轮交互训练至关重要。"
claims:
- "MAD 2×2 + RL 在 AIME 上以 65.0 分超越单智能体 RL 基线（53.5），证明多智能体强化学习在同等推理预算下具有更高性能上限。"
- "在 Llama-3.2-3B-Instruct 上，MARTI 训练的 MAD 2×2 平均 32.1，优于单智能体 RL 的 28.7 和多数投票 RL 的 30.0。"
- "移除奖励塑形导致 MAD 2×2 平均性能从 45.6 降至 36.6，MoA 3×1 从 43.1 降至 38.1，表明奖励塑形对稳定多智能体 RL 至关重要。"
- "AIME (DeepScaleR-1.5B-Preview) 上 Accuracy = 65.0 (MAD 2×2 + RL)"
---

# MARTI: A Framework for Multi-Agent LLM Systems Reinforced Training and Inference

> [!tip] 核心洞察
> 在相同推理预算下，通过多智能体强化学习训练，多智能体系统能够超越单智能体系统的性能上限；奖励塑形对于稳定多智能体多轮交互训练至关重要。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MARTI：多智能体LLM系统强化训练与推理框架 |
| 英文题名 | MARTI: A Framework for Multi-Agent LLM Systems Reinforced Training and Inference |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=E7jZqo0A50); [GitHub](https://github.com/TsinghuaC3I/MARTI) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MARTI (Multi-Agent Reinforced Training and Inference) |
| Dataset | AIME (DeepScaleR-1.5B-Preview), Llama-3.2-3B-Instruct (avg over AIME/AMC/MATH500), Qwen2.5-3B (avg over AIME/AMC/MATH500) |

> [!tip] 效果简介
> - AIME (DeepScaleR-1.5B-Preview) 上，Accuracy 为 65.0 (MAD 2×2 + RL)，对比 53.5 (Single-Agent RL)，变化 +11.5。
> - Llama-3.2-3B-Instruct (avg over AIME/AMC/MATH500) 上，Avg Accuracy 为 32.1 (MAD 2×2 + RL MARTI)，对比 28.7 (Single Agent + RL)，变化 +3.4。
> - Qwen2.5-3B (avg over AIME/AMC/MATH500) 上，Avg Accuracy 为 46.0 (MAD 2×2 + GRPO)，对比 37.9 (Single-Agent + GRPO)，变化 +8.1。

## 概述

**问题瓶颈**：现有基于大语言模型（LLM）的多智能体系统（MAS）普遍沿用单智能体训练范式，导致智能体难以有效遵循角色指定，也无法充分利用智能体间的交互信息。这使得多智能体工作流（如辩论、链式协作）在实际执行中频繁失败，性能提升远低于预期。

**核心思路**：MARTI 框架将多智能体强化学习（MARL）引入 LLM 协作训练，采用“集中式交互、分布式策略训练”的架构，并通过基于历史表现对比的 delta 式奖励塑形（reward shaping）来稳定多轮协作训练。其关键洞察在于：在相同推理预算下，经 MARL 训练的多智能体系统能够超越单智能体系统的性能上限。

**主要结果**：
- 在 AIME 基准上，基于 DeepScaleR-1.5B-Preview 的多智能体辩论工作流（MAD 2×2 + RL）以 **65.0** 分显著超越单智能体 RL 基线（53.5），提升达 +11.5 分。
- 在 Llama-3.2-3B-Instruct 上，MARTI 训练的 MAD 2×2 平均得分 **32.1**，优于单智能体 RL（28.7）和多数投票 RL（30.0）。
- 在 Qwen2.5-3B 上，MAD 2×2 + GRPO 平均得分 **46.0**，较单智能体 GRPO（37.9）提升 +8.1 分。
- 消融实验表明，移除奖励塑形会导致 MAD 2×2 平均性能从 45.6 骤降至 36.6，验证了奖励塑形对多智能体 RL 稳定性的关键作用。

**方法定位**：MARTI 是首个同时支持多智能体推理与多智能体强化学习训练的框架。相较于仅支持单智能体 RL 的 TRL、OpenRLHF、verl，以及仅支持 MAS 推理但缺乏 MAS RL 的 AReaL，MARTI 填补了多智能体协作训练的基础设施空白（见 Table 1）。框架基于 OpenRLHF 构建，支持异步多轮交互生成，在深层交互场景下可有效降低端到端延迟。

## 背景与动机

大型语言模型（LLM）在单智能体推理任务上已取得显著进展，通过强化学习（RL）训练，模型能够发展出反思、验证和自我纠错等高级认知行为。然而，当这些经过RL训练的单智能体被直接部署到多智能体系统（MAS）中时，其协作能力往往不尽如人意。现有LLM多智能体系统普遍采用单智能体训练范式，导致智能体无法有效遵循角色指定，也难以充分利用智能体间的交互信息，最终造成多智能体工作流失败，性能提升有限。

这一瓶颈的根源在于训练与推理之间的范式错配：单智能体RL训练的目标是最大化个体性能，而多智能体协作要求智能体在动态交互中适应同伴行为、进行有效的信息交换与整合。现有的RL框架——如TRL（von Werra et al., 2020）、OpenRLHF（Hu et al., 2024）和verl（Sheng et al., 2024）——仅支持单智能体RL训练；而支持多智能体推理的框架（如CAMEL、AutoGen）又缺乏多智能体RL训练能力。AReaL（Fu et al., 2025）虽然支持多智能体推理，但同样缺少多智能体RL训练功能。这一能力缺口构成了当前多智能体系统性能上限的硬约束。

MARTI的动机正是弥合这一缺口。其核心洞察在于：在相同的推理预算下，通过多智能体强化学习训练，多智能体系统能够超越单智能体系统的性能上限。初步实验表明，基于DeepScaleR-1.5B-Preview的多智能体辩论工作流在AIME基准上达到65.0分，显著超越单智能体RL基线的53.5分，验证了这一假设。为实现这一目标，MARTI采用多智能体强化学习范式，通过集中式交互协调与分布式策略训练，使每个智能体在保持独立策略更新的同时，能够感知并利用同伴的生成结果。此外，MARTI引入基于历史表现对比的delta式奖励塑形机制，以稳定多轮协作训练中的非平稳性问题——这是多智能体RL训练能否成功的关键因素。

## 核心创新

MARTI 的核心创新在于将多智能体交互从推理时的静态编排提升为可训练的协作策略，并通过三项关键设计解决现有方法的瓶颈。

### 从单智能体训练到多智能体强化学习

现有 LLM 多智能体系统（如 CAMEL、AutoGen）仅支持推理时的多智能体编排，其底层策略仍由单智能体 RL 框架（TRL、OpenRLHF、verl）独立训练。这种单智能体训练范式导致模型无法有效遵循角色指定，也无法利用智能体间的交互信息进行策略优化，使得多智能体工作流在实际性能上提升有限。

MARTI 首次将多智能体强化学习（MARL）引入 LLM 训练流程，采用**集中式交互、分布式策略训练**的架构。具体而言，框架包含三个核心模块：

- **Multi-Agent World**：执行异步多轮交互工作流（辩论、链式、混合等），生成轨迹并管理信用分配机制。
- **Centralized Reward Models**：收集全局轨迹，进行信用分配与奖励塑形，将全局奖励分解为智能体级别的训练信号。
- **Agent Policy Trainer**：各智能体独立使用相同的 RL 算法（REINFORCE++/GRPO/PPO）进行分布式策略更新，并可结合 SFT/DPO 以稳定训练。

这一设计使得多智能体系统在**相同推理预算**下能够超越单智能体的性能上限。实验表明，MAD 2×2 + RL 在 AIME 上以 65.0 分显著超越单智能体 RL 基线（53.5）；在 Llama-3.2-3B-Instruct 上平均得分 32.1，优于单智能体 RL 的 28.7 和多数投票 RL 的 30.0。

### 推理感知的奖励塑形机制

多智能体多轮交互面临严重的非平稳性问题——智能体在不同轮次的表现高度依赖其他智能体的输出，直接使用基于最终结果的单一奖励会导致训练不稳定。MARTI 引入了一种推理感知的 delta 式奖励塑形策略，通过对比智能体当前表现与其自身历史表现来分配奖励，而非仅依赖绝对正确性。

具体而言，对于智能体 $i$ 在第 $t$ 轮的表现，首先计算其历史性能估计：

$$Q_{t}^{i} = \frac{1}{|\mathcal{H}_{t}^{i}|} \sum_{k \in \mathcal{H}_{t}^{i}} R_{k}^{i}$$

然后根据两种模式计算塑形项：

- **Margin 模式**：$\Delta_{t}^{i} = R_{t}^{i} - Q_{t}^{i}$，鼓励超越历史平均水平
- **Quality 模式**：$\Delta_{t}^{i} = Q_{t}^{i} \cdot R_{t}^{i} - (1 - Q_{t}^{i})(1 - R_{t}^{i})$，鼓励当前表现与历史正确性保持一致

最终塑形奖励为 $\tilde{R}_{t}^{i} = R_{t}^{i} + \alpha \cdot \Delta_{t}^{i}$，其中 $\alpha$ 为可调节系数。

消融实验验证了这一机制的关键作用：移除奖励塑形后，MAD 2×2 平均性能从 45.6 降至 36.6，MoA 3×1 从 43.1 降至 38.1，表明奖励塑形对稳定多智能体 RL 训练不可或缺。

### 异步多轮生成支持

传统多智能体系统采用同步批量生成，在交互轮次加深时端到端延迟线性增长。MARTI 是首个支持多轮多智能体场景异步生成的框架，允许不同智能体在不同时间步独立执行推理。实验表明，异步生成在深度交互工作流中能有效降低延迟：Chain-of-Agents 在异步 ×512 设置下从同步的 612.6s 降至 498.4s。

## 整体框架

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_E7jZqo0A50/figures/002_Figure_1.jpg]]
*Figure 1: Overview and motivation behind of MARTI*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_E7jZqo0A50/figures/001_Table_1.jpg]]
*Table 1: Comparison between Multi-Agent and RL Framework*

### 核心瓶颈与设计动机

现有LLM多智能体系统面临一个根本性瓶颈：它们通常采用单智能体训练范式，导致智能体无法有效遵循角色指定，也难以充分利用智能体间的交互信息。这使得多智能体工作流在复杂协作场景中频繁失败，性能提升极为有限。MARTI框架正是针对这一问题而设计，其核心洞察是：**在相同推理预算下，通过多智能体强化学习训练，多智能体系统能够超越单智能体系统的性能上限**。

### 框架总体架构

MARTI采用“集中式交互、分布式训练”的架构理念，由三个核心模块构成闭环系统（Figure 1）：

| 模块 | 功能角色 | 关键机制 |
|------|---------|---------|
| **Multi-Agent World** | 多智能体交互环境，执行异步工作流生成轨迹，管理信用分配 | 支持辩论、链式、混合等多种交互拓扑；集中式协调，异步rollout |
| **Centralized Reward Models** | 集中式计算全局奖励，进行信用分配与奖励塑形 | 将全局奖励分解为智能体级奖励；引入delta式奖励塑形机制 |
| **Agent Policy Trainer** | 分布式策略训练器，对每个智能体独立进行SFT或RL训练 | 各智能体使用相同RL算法（REINFORCE++/GRPO/PPO），可选SFT/DPO稳定训练 |

整个流程为：Multi-Agent World根据指定的交互工作流执行prompt驱动的rollout，生成多轮交互轨迹；Centralized Reward Models收集轨迹，先计算全局奖励，再通过信用分配和奖励塑形将其分解为每个智能体的个体奖励；Agent Policy Trainer接收智能体特定的轨迹和奖励，对骨干LLM进行监督微调或强化学习训练。这一闭环使得多智能体协作能力可以通过RL持续优化。

### 奖励塑形：稳定多智能体RL的关键

多智能体多轮交互训练面临严重的非平稳性问题。MARTI从MAPoRL引入推理感知的delta式奖励塑形策略，核心思想是**让智能体与自身历史表现对比，而非仅依赖绝对正确性**。

具体而言，对于智能体 $i$ 在第 $t$ 轮的表现，首先计算其历史性能估计：

$$Q_{t}^{i} = \frac{1}{|\mathcal{H}_{t}^{i}|} \sum_{k \in \mathcal{H}_{t}^{i}} R_{k}^{i}$$

其中 $\mathcal{H}_{t}^{i}$ 为智能体 $i$ 的历史交互集合，$R_{k}^{i}$ 为历史即时奖励。基于此，MARTI提供两种塑形模式：

- **Margin模式**：$\Delta_{t}^{i} = R_{t}^{i} - Q_{t}^{i}$，鼓励智能体超越自身历史平均水平；
- **Quality模式**：$\Delta_{t}^{i} = Q_{t}^{i} \cdot R_{t}^{i} - (1 - Q_{t}^{i})(1 - R_{t}^{i})$，鼓励当前表现与历史表现的一致性。

最终塑形奖励为：

$$\tilde{R}_{t}^{i} = R_{t}^{i} + \alpha \cdot \Delta_{t}^{i}$$

其中 $\alpha \in \mathbb{R}_{\geq 0}$ 为可调节的超参数。消融实验（Table 4）充分验证了这一机制的必要性：移除奖励塑形后，MAD 2×2的平均性能从45.6骤降至36.6，MoA 3×1从43.1降至38.1，降幅分别达9.0和5.0个百分点。

### 异步生成与系统效率

MARTI是首个在多轮多智能体场景中支持异步生成的框架。在交互轮次较深的工作流（如Chain-of-Agents）中，异步rollout能有效降低端到端延迟：Chain同步模式下耗时612.6秒，异步×512降至498.4秒（Table 5）。对于浅层交互，加速效果则相对有限。

### 框架定位与能力对比

Table 1将MARTI与现有框架进行了系统对比。现有MAS框架（CAMEL、AutoGen、MetaGPT、GPTSwarm等）仅支持多智能体推理，缺乏RL训练能力；RL框架（TRL、OpenRLHF、verl）仅支持单智能体RL；AReaL虽支持MAS推理，但缺少MAS RL功能。MARTI是首个同时支持多智能体推理与多智能体强化学习训练的框架，填补了这一关键空白。MARTI底层基于OpenRLHF构建，以确保RL训练的可扩展性和高性能。

## 核心模块与公式推导

### 三大核心模块

MARTI 框架由三个核心模块构成，分别负责多智能体交互执行、奖励计算与分配、以及分布式策略训练。

**Multi-Agent World（多智能体交互环境）** 是框架的执行引擎，核心职责包括：根据指定的交互工作流（如多智能体辩论 MAD、链式智能体 CoA、混合智能体 MoA）执行 prompt 驱动的异步 rollout，管理轨迹的信用分配机制，并将生成的轨迹传递给后续模块。

**Centralized Reward Models（集中式奖励模型）** 负责收集 Multi-Agent World 产生的轨迹，进行信用分配和奖励塑形。该模块首先计算全局奖励，随后将其分解为智能体级别的奖励，供各智能体独立训练使用。框架同时支持基于规则的奖励模型和生成式奖励模型（GenRM），后者适用于可验证问题和开放域问题。

**Agent Policy Trainer（智能体策略训练器）** 接收智能体专属的轨迹和奖励信号，对每个智能体独立进行强化学习训练。所有智能体采用相同的 RL 算法（如 REINFORCE++、GRPO），并可选择性结合 SFT 或 DPO 等模仿学习策略以稳定训练过程。该模块基于 OpenRLHF（Hu et al., 2024）构建，实现可扩展的高性能训练。

### 奖励塑形公式推导

MARTI 的核心创新之一是推理感知的 delta 式奖励塑形机制，该机制通过对比智能体当前轮次表现与其自身历史表现来生成塑形信号。

**历史性能估计**：对于智能体 $i$，其在历史交互集合 $\mathcal{H}_{t}^{i}$ 上的平均奖励定义为：

$$Q_{t}^{i} = \frac{1}{|\mathcal{H}_{t}^{i}|} \sum_{k \in \mathcal{H}_{t}^{i}} R_{k}^{i}$$

该估计值为后续塑形项提供了动态基准线。

**Margin 模式塑形项**：即时奖励与历史平均性能的差值，鼓励智能体超越自身历史平均水平：

$$\Delta_{t}^{i} = R_{t}^{i} - Q_{t}^{i}$$

**Quality 模式塑形项**：鼓励当前表现与历史表现的一致性，当历史表现较好时放大当前奖励，反之则惩罚：

$$\Delta_{t}^{i} = Q_{t}^{i} \cdot R_{t}^{i} - (1 - Q_{t}^{i})(1 - R_{t}^{i})$$

**最终塑形奖励**：将原始即时奖励与可调节的历史一致性奖励项线性组合，其中 $\alpha \in \mathbb{R}_{\geq 0}$ 为调节系数：

$$\tilde{R}_{t}^{i} = R_{t}^{i} + \alpha \cdot \Delta_{t}^{i}$$

该奖励塑形机制的关键因果作用在消融实验中得到验证：移除奖励塑形后，MAD 2×2 的平均性能从 45.6 降至 36.6，MoA 3×1 从 43.1 降至 38.1（Table 4），表明 delta 式奖励塑形对稳定多智能体多轮 RL 训练至关重要。

## 实验与分析

### 核心发现：多智能体RL突破单智能体性能上限

MARTI的核心主张——在相同推理预算下，多智能体强化学习能够超越单智能体系统的性能上限——通过多组对照实验得到了一致验证。

**推理模型上的决定性证据。** 在DeepScaleR-1.5B-Preview（Luo et al., 2025）上，采用MARTI训练的MAD 2×2辩论工作流在AIME基准上达到65.0分，显著超越单智能体RL基线的53.5分（+11.5）。这一结果直接证明了多智能体交互式RL训练的有效性，而非简单增加推理预算带来的收益。

**通用模型上的跨架构验证。** 在Llama-3.2-3B-Instruct上（Table 2），MARTI训练的MAD 2×2在AIME/AMC/MATH500三个基准上平均达到32.1，优于单智能体RL的28.7（+3.4）和多数投票RL的30.0（+2.1）。在Qwen2.5-3B上（Table 3），MAD 2×2 + GRPO平均达到46.0，相比单智能体GRPO的37.9提升8.1个点。跨模型系列的一致性提升表明，MARTI的收益不依赖于特定模型架构。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_E7jZqo0A50/figures/005_Table_2.jpg]]
*Table 2: Results for Llama-3.2-3B-Instruct across various workflows and training configurations. Under an equivalent inference budget, MARTI consistently outperforms both single-agent reinforcement learning and majority-vote baselines*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_E7jZqo0A50/figures/006_Table_3.jpg]]
*Table 3: Comparison of REINFORCE++ (RF++) and GRPO on Qwen2.5-3B. Both algorithms produce strong performance gains; GRPO achieves marginally better results on most evaluated metrics*

**公平性保障。** 所有对比在严格控制的推理预算下进行：单智能体Majority@4与MAD 2×2均产生4条完整轨迹，MoA 3×1产生3条轨迹加一次聚合。Table 6进一步显示，MAD 2×2的平均输出令牌数（3221）与单智能体Avg@4（3520）相当甚至更低，排除了“多智能体系统仅因生成更多文本而获胜”的替代解释。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_E7jZqo0A50/figures/015_Table_6.jpg]]
*Table 6: (b) Time vs. interaction rounds (seconds)*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_E7jZqo0A50/figures/025_Table_6.jpg]]
*Table 6: Average number of output tokens per instance on Qwen2.5-3B across tasks and workflows. Multi-agent workflows operate under a comparable token budget to Majority@4, and can even be more efficient*

### 奖励塑形：多智能体RL稳定性的关键

消融实验（Table 4）揭示了奖励塑形机制的决定性作用。移除MARTI的delta式奖励塑形后：

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_E7jZqo0A50/figures/007_Table_4.jpg]]
*Table 4: Ablation study on reward shaping for Qwen2.5-3B. Removing reward shaping results in substantial performance degradation for both MAD and MoA architectures*

- MAD 2×2平均性能从45.6骤降至36.6（-9.0）
- MoA 3×1从43.1降至38.1（-5.0）

这一退化幅度远超算法选择带来的波动（GRPO vs REINFORCE++仅差0.4），说明在多智能体多轮交互场景中，直接使用全局奖励训练各智能体策略会导致严重的非平稳性问题。MARTI的奖励塑形通过将当前轮次表现与智能体自身历史平均表现（$Q_t^i$）对比，生成相对改进信号（$\Delta_t^i$），有效稳定了训练动态。

### 算法鲁棒性与训练动态

Table 3对比了REINFORCE++和GRPO在Qwen2.5-3B上的表现：MAD 2×2 + GRPO达到46.0，略优于RF++的45.6。差异微小但方向一致，表明MARTI框架对底层策略梯度算法的选择具有鲁棒性——核心增益来自多智能体交互范式与奖励塑形，而非特定RL变体。

训练曲线（Figure 5, Figure 9）展示了MAD和MoA在MATH基准上的RL训练动态：准确率随训练步数持续上升，未出现单智能体RL中常见的性能平台或退化现象，进一步验证了奖励塑形在维持训练稳定性方面的作用。

### 异步生成的效率增益

Table 5展示了MARTI异步生成机制的实际效果。对于交互深度较大的工作流，异步生成带来显著加速：

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_E7jZqo0A50/figures/014_Table_5.jpg]]
*Table 5: Statistics of asynchronous rollouts in MARTI. (a) End-to-end rollout time vs. concurrency for Chain-of-Agents and MAD. (b) Total rollout time vs. number of interaction rounds for different concurrency settings. (a) Time vs. concurrency (seconds)*

- Chain-of-Agents：同步模式612.6秒 → 异步×512降至498.4秒
- MAD：同步模式593.5秒 → 异步×512降至561.2秒

然而，对于浅层交互（如仅2轮辩论），异步加速效果有限。这一结果揭示了异步机制的价值边界：当交互轮次增加、智能体间等待时间占比上升时，异步并行的收益才真正显现。

### 局限性与待验证问题

当前实验主要在数学推理数据集（AIME、AMC、MATH500）上验证，真实世界任务的泛化性尚未探索。此外，多智能体RL的奖励模型仍依赖基于规则的奖励或生成式奖励模型（GenRMs），在复杂协作场景下可能不够精细。框架虽支持异步生成，但大规模并行时仍受计算资源约束。这些限制提示，MARTI在代码生成、科学推理等领域的适用性，以及更精细的多智能体专用奖励模型设计，是未来需要重点验证的方向。

## 方法谱系与知识库定位

### 多智能体LLM系统的训练范式断层

当前多智能体LLM系统（MAS）的研究存在明显的“推理-训练”断层。一方面，以CAMEL、AutoGen、Meta-GPT、GPTSwarm为代表的MAS框架（见Table 1）专注于编排多智能体交互以实现复杂任务推理，但它们的智能体策略是冻结的——仅依赖预训练或指令微调后的模型，缺乏面向协作的任务特异性优化。另一方面，LLM强化学习社区涌现了TRL（von Werra et al., 2020）、OpenRLHF（Hu et al., 2024）、verl（Sheng et al., 2024）等成熟框架，但它们的设计假设是单智能体独立决策，无法处理多智能体交互产生的非平稳动态和信用分配问题。AReaL（Fu et al., 2025）虽然支持多智能体推理，但同样缺乏多智能体强化学习（MARL）能力。

这一断层的后果是：即便多智能体工作流（如Multi-Agent Debate、Mixture-of-Agents）在理论上具有超越单智能体的潜力，实际性能提升往往有限，因为各智能体无法有效遵循角色指定，也无法从交互中学习。MARTI正是在这一裂缝中定位——它并非重新发明RL算法，而是构建了一个**多智能体RL训练基础设施**，使现有的策略梯度方法（REINFORCE++、GRPO、PPO）能够作用于多智能体交互轨迹。

### 与单智能体RL基线的关系

MARTI的核心论证是：**在相同推理预算下，经过MARL训练的多智能体系统能够超越单智能体RL的性能上限**。这一主张通过严格的预算对齐实验得到验证：

- **Single Agent + RL**（REINFORCE++/GRPO）：单智能体独立生成一条轨迹并接受RL训练，是当前LLM推理能力提升的主流范式（如DeepSeek-R1）。
- **Single Agent (Maj@4/6) + RL**：单智能体独立采样多条轨迹后多数投票，训练时每条轨迹独立计算奖励。这是对单智能体RL的“暴力扩展”，但缺乏智能体间的结构化交互。
- **MAD 2×2 + RL（MARTI）**：两个智能体进行两轮辩论，同样产生4条轨迹（与Maj@4预算对齐），但智能体间存在信息交换和角色分工。

实验表明，在Llama-3.2-3B-Instruct上，MARTI训练的MAD 2×2平均得分32.1，显著优于Single Agent + RL的28.7和Maj@4 + RL的30.0（Table 2）。在DeepScaleR-1.5B-Preview上，MAD 2×2 + RL在AIME上达到65.0分，超越单智能体RL基线的53.5分（+11.5）。这一差距揭示了一个深层机制：多智能体交互本身提供了**结构化的探索空间**——辩论迫使智能体审视对方推理、修正自身错误，这种“对抗性协作”是单智能体独立采样无法模拟的。

### 奖励塑形：从MAPoRL到MARTI的delta式设计

MARTI的奖励塑形策略借鉴了MAPoRL中的推理感知塑形思想，但将其适配到多智能体多轮交互场景。其核心创新在于**基于历史表现对比的delta式塑形**：

- **历史性能估计**：$Q_{t}^{i} = \frac{1}{|\mathcal{H}_{t}^{i}|} \sum_{k \in \mathcal{H}_{t}^{i}} R_{k}^{i}$，追踪智能体$i$在历史交互中的平均奖励。
- **Margin模式**：$\Delta_{t}^{i} = R_{t}^{i} - Q_{t}^{i}$，奖励超越自身历史平均水平的行为。
- **Quality模式**：$\Delta_{t}^{i} = Q_{t}^{i} \cdot R_{t}^{i} - (1 - Q_{t}^{i})(1 - R_{t}^{i})$，鼓励当前表现与历史表现的一致性。

最终塑形奖励为 $\tilde{R}_{t}^{i} = R_{t}^{i} + \alpha \cdot \Delta_{t}^{i}$。这一设计的关键在于：它不依赖全局最优或智能体间横向比较，而是让每个智能体与自身的“过去”竞争。这在多智能体RL中尤为重要——当其他智能体的策略也在更新时（非平稳环境），以自身历史为基准的奖励信号比绝对正确性奖励更稳定。

消融实验（Table 4）强有力地验证了这一点：移除奖励塑形后，MAD 2×2平均性能从45.6骤降至36.6，MoA 3×1从43.1降至38.1。这表明，在多智能体多轮交互中，原始任务奖励的稀疏性和噪声足以破坏RL训练的稳定性，而delta式塑形充当了有效的“方差缩减器”。

### 适用边界与局限

MARTI的当前验证集中在**数学推理领域**（AIME、AMC、MATH-500），这一选择具有合理性——数学问题提供清晰的规则奖励（答案正确性），便于隔离多智能体协作的净效应。但这也构成了框架的**第一重适用边界**：在奖励信号模糊或需要人工评估的开放域任务（如创意写作、复杂对话）中，集中式奖励模型的设计将面临更大挑战。MARTI虽然支持生成式奖励模型（GenRMs），但其在多智能体场景下的校准和偏差问题尚未被系统研究。

**第二重边界**在于智能体角色的同质性。当前实验中的辩论、链式、混合工作流均使用相同基座模型的不同副本，角色差异主要通过提示工程和RL训练动态涌现，而非预设的异构能力。当智能体具有本质不同的能力剖面（如一个擅长检索、一个擅长推理）时，信用分配和奖励塑形策略可能需要更精细的设计。

**第三重边界**是计算效率。异步生成机制（Table 5）在深层交互中能降低端到端延迟（如Chain从同步的612.6s降至异步×512的498.4s），但对浅层交互（如MAD仅两轮）加速有限。此外，多智能体RL的训练成本是单智能体的数倍——每个智能体都需要独立的策略训练器，且交互轨迹的生成需要协调多个模型的推理。

### 开放问题

1. **多智能体专用奖励模型**：现有的规则奖励（如数学答案匹配）和通用生成式奖励在多智能体协作中可能不够精细。例如，一个智能体的部分正确推理如何被恰当地奖励，即使最终答案错误？这需要奖励模型能够评估推理过程的质量，而不仅仅是结果。

2. **真实世界任务的迁移**：数学推理提供了一个“干净”的测试床，但多智能体RL在代码生成、科学推理、多步规划等任务中的适用性尚未被验证。这些任务中的奖励稀疏性、子目标分解和长期信用分配问题可能更加突出。

3. **on-policy与off-policy的混合策略**：MARTI当前采用on-policy的RL训练（每个rollout后立即更新策略），但在多智能体场景中，off-policy的经验回放可能有助于提高样本效率。如何在非平稳环境中安全地混合两种策略，是一个开放的理论和实践问题。

4. **异构智能体和动态拓扑**：未来多智能体系统可能包含具有不同能力、知识库和目标的智能体，交互拓扑也可能随任务动态调整。MARTI的集中式协调架构能否扩展到此场景，以及如何设计相应的信用分配机制，值得进一步探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/MARTI_A_Framework_for_Multi_Agent_LLM_Systems_Reinforced_Training_and_Inference.pdf]]
