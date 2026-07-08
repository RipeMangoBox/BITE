---
title: Agentic Reinforcement Learning with Implicit Step Rewards
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Agentic_Reinforcement_Learning_with_Implicit_Step_Rewards.pdf
aliases:
- IISRAR
- ARLISR
acceptance: accepted
paradigm: 隐式步骤奖励（implicit step rewards）通过测量当前动作在新旧策略下的概率比，提供密集且低方差的信用分配信号，无需额外标注或回滚，且与多种RL算法兼容。
tags:
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
---

# Agentic Reinforcement Learning with Implicit Step Rewards

> [!tip] 核心洞察
> 隐式步骤奖励（implicit step rewards）通过测量当前动作在新旧策略下的概率比，提供密集且低方差的信用分配信号，无需额外标注或回滚，且与多种RL算法兼容。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于隐式步骤奖励的智能体强化学习 |
| 英文题名 | Agentic Reinforcement Learning with Implicit Step Rewards |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=ooROvpmxMV) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | iStar (implicit step rewards for agentic RL) |
| Dataset | WebShop, WebShop, VisualSokoban, SOTOPIA (Self-Chat, Hard) |

> [!tip] 效果简介
> - WebShop 上，Success Rate 为 86.5 ± 2.8，对比 84.1 ± 3.9 (GiGPO)，变化 +2.4。
> - WebShop 上，Score 为 93.6 ± 1.0，对比 91.2 ± 1.5 (GiGPO)，变化 +2.4。
> - VisualSokoban 上，Success Rate 为 91.7 ± 1.2，对比 85.9 ± 2.6 (GiGPO)，变化 +5.8。

## 概述

本论文提出了一种名为 **iStar (implicit step rewards for agentic RL)** 的新型强化学习框架，旨在解决智能体强化学习（agentic RL）中因奖励稀疏且延迟导致的信用分配困难问题。iStar 的核心思想是：通过在线收集的轨迹偏好数据，利用多轮 DPO 目标训练一个隐式过程奖励模型（implicit PRM），该模型能够为每个动作生成密集且低方差的步骤级奖励信号。这些隐式步骤奖励与回合级结果奖励相结合，共同指导策略模型的更新。实验结果表明，iStar 在 WebShop、VisualSokoban 和 SOTOPIA 等多个基准上均取得了最先进的性能，并显著提升了训练样本效率。

## 背景与动机

在智能体强化学习中，LLM 智能体需要与环境进行多轮交互以完成复杂任务。然而，这类任务通常面临以下核心瓶颈：

- **奖励稀疏且延迟**：环境仅在轨迹结束时提供结果奖励（outcome reward），中间步骤缺乏明确的反馈信号，导致信用分配困难。
- **轨迹长且非马尔可夫**：智能体的决策依赖于完整的交互历史，现有方法（如过程监督、隐式 PRM）存在标注偏差、奖励破解、方差高或状态重叠罕见等问题。

现有方法如 **PRIME**（Cui et al., 2025）使用 token 级过程奖励，但提供过于细粒度的奖励，在多轮 RL 中导致高方差和训练不稳定；**GiGPO**（Feng et al., 2025）通过同状态分组计算步骤级优势，但依赖于罕见的状态重叠。这些局限性促使研究者探索一种无需额外标注、低方差且与多种 RL 算法兼容的步骤级信用分配方法。

## 核心创新

iStar 的核心创新在于提出了一种**隐式步骤奖励**机制，通过以下关键设计解决信用分配问题：

1. **隐式 PRM 的在线学习**：利用多轮 DPO 目标，从旧策略采样的正负轨迹对中学习隐式过程奖励模型，无需人工标注的步骤标签。
2. **步骤级隐式奖励**：通过测量当前动作在新旧策略下的概率比，为每个动作生成密集且低方差的奖励信号。
3. **双层优势组合**：将回合级优势（基于结果奖励）与步骤级优势（基于隐式步骤奖励）加权组合，实现更精细的信用分配。
4. **移除 KL 散度惩罚**：允许策略模型自由探索动作空间，进一步提升性能。

## 整体框架

![[obsidian-vault/assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_ooROvpmxMV_Agentic_Reinforcement_Le/figures/001_Figure_1.jpg]]
*Figure 1: Overview of iStar. At each training step, an LLM agent interacts with the environment to generate multi-step rollouts ranked by an outcome reward verifier (or model) to construct positive-negative trajectory pairs. These pairs are used to train an implicit PRM via a multi-turn DPO objective, which generates implicit step rewards for each action produced by the agent. Finally, calculate step-level advantages using the implicit step rewards and episode-level advantages using outcome rewards to optimize the LLM agent (policy model) through RL.*

iStar 的训练流程如 **Figure 1** 所示，包含以下核心模块：

1. **策略模型（LLM 智能体）**：与环境交互生成多步轨迹。
2. **结果奖励验证器/模型**：为轨迹提供结果奖励，并构建正负轨迹对。
3. **隐式 PRM**：通过多轮 DPO 目标从轨迹对中学习，为每个动作生成隐式步骤奖励。
4. **优势计算模块**：分别计算回合级优势（Eq. 3）和步骤级优势（Eq. 4），并组合为最终优势（Eq. 5）。
5. **策略优化器**：使用组合优势更新策略模型（Eq. 6）。

**Figure 1** 展示了 iStar 的完整训练循环：LLM 智能体与环境交互生成轨迹 → 结果奖励验证器排序并构建正负轨迹对 → 隐式 PRM 通过多轮 DPO 目标训练 → 隐式 PRM 为每个动作生成步骤奖励 → 计算双层优势并更新策略模型。

**Figure 2** 展示了 iStar 的信用分配策略：回合级优势 A^E(τ) 基于结果奖励 r_o(τ) 计算，步骤级优势 A^S(a) 基于隐式步骤奖励 r_φ(a) 计算，最终优势为两者的组合。

## 核心模块与公式推导

### 5.1 隐式步骤奖励

隐式步骤奖励定义为当前动作在新学习的 PRM 下相对于旧策略的概率比：

$$r_{\phi}(o_{1:t}, a_t) = \beta \log \frac{\pi_{\phi}(a_t|o_{1:t}, x)}{\pi_{\theta_{\mathrm{old}}}(a_t|o_{1:t}, x)} \quad \text{(Eq. 1)}$$

其中，π_φ 是隐式 PRM，π_θ_old 是旧策略快照，β 是温度参数。

### 5.2 多轮 DPO 目标

隐式 PRM 通过在线多轮 DPO 目标进行优化：

$$\mathcal{L}_{\mathrm{PRM}}(\phi) = -\mathbb{E}_{(\tau^+, \tau^-) \sim \pi_{\theta_{\mathrm{old}}}} \left[ \log \sigma \left( \beta \log \frac{\pi_{\phi}(\tau^+|x)}{\pi_{\theta_{\mathrm{old}}}(\tau^+|x)} - \beta \log \frac{\pi_{\phi}(\tau^-|x)}{\pi_{\theta_{\mathrm{old}}}(\tau^-|x)} \right) \right] \quad \text{(Eq. 2)}$$

该目标使用旧策略采样的正负轨迹对，在线优化隐式 PRM。理论分析（Eq. 7）证明，该目标等价于具有步骤级奖励函数的 Bradley-Terry 模型。

### 5.3 双层优势计算

**回合级优势**（基于结果奖励的归一化）：

$$A^E(\tau_i) = (r_o(\tau_i) - \mathrm{mean}(R_o)) / \mathrm{std}(R_o) \quad \text{(Eq. 3)}$$

**步骤级优势**（基于隐式步骤奖励的归一化）：

$$A^S(a_t^i) = (r_{\phi}(a_t^i) - \mathrm{mean}(R_s)) / \mathrm{std}(R_s) \quad \text{(Eq. 4)}$$

**组合优势**：

$$A(a_t^i) = A^E(\tau_i) + \alpha A^S(a_t^i) \quad \text{(Eq. 5)}$$

其中 α 是平衡系数。

### 5.4 策略更新目标

策略模型通过以下替代目标进行更新：

$$\mathcal{L}_{\mathrm{policy}}(\theta) = \mathbb{E}_{\{\tau_i\}_{i=1}^N \sim \pi_{\theta_{\mathrm{old}}}} \left[ \frac{1}{NT} \sum_{i=1}^N \sum_{t=1}^{T_i} \min\left( \rho_\theta(a_t^i) A(a_t^i), \mathrm{clip}(\rho_\theta(a_t^i), 1\pm\epsilon) A(a_t^i) \right) \right] \quad \text{(Eq. 6)}$$

其中 ρ_θ(a_t^i) = π_θ(a_t^i|o_{1:t}^i, x) / π_θ_old(a_t^i|o_{1:t}^i, x) 是重要性采样比率。

## 实验与分析

![[obsidian-vault/assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_ooROvpmxMV_Agentic_Reinforcement_Le/figures/003_Table_1.jpg]]
*Table 1: Performance on WebShop and VisualSokoban. Qwen2.5-7B-Instruct and Qwen2.5- VL-7B-Instruct serve as the base models for the policy model in WebShop and VisualSokoban, respectively. Note that Deepseek-R1 and PPO training do not currently support multi-modal scenarios, and PRIME is only applicable to tasks with binary outcome rewards. Results are averaged over three random seeds.*

![[obsidian-vault/assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_ooROvpmxMV_Agentic_Reinforcement_Le/figures/004_Table_2.jpg]]
*Table 2: Performance on Sotopia. ‘Self-Chat” refers to dialogues where the model under evaluation interacts with itself, while “GPT-4o-as-Partner” denotes interactions between the model and GPT-4o. “Goal” refers to the goal completion rate (on a scale of 0-10). The ”Hard” subset comprises test scenarios in SOTOPIA that require advanced reasoning capabilities, and ”All” represents the complete test set. Results are averaged over three random seeds.*

![[obsidian-vault/assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_ooROvpmxMV_Agentic_Reinforcement_Le/figures/015_Table_3.jpg]]
*Table 3: Ablation studies on core components of iStar. “RLOO”: only outcome rewards are used to compute advantages for policy updates. “w/ environmental process rewards”: use raw step rewards provided by VisualSokoban to calculate step-level advantages. “w/ merged rewards”: implicit step rewards are added directly to outcome rewards before advantage computation. “w/ token-level process rewards”: the implicit PRM produces rewards for each token along the entire trajectory rather than step-level rewards for each action sequence. Results are reported using one seed.*

![[obsidian-vault/assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_ooROvpmxMV_Agentic_Reinforcement_Le/figures/016_Table_4.jpg]]
*Table 4: SOTOPIA. We use Qwen2.5-7B-Instruct (Yang et al., 2024) and Llama3.1-8B-Instruct (Meta, 2024) as the base models for policy learning to demonstrate the robustness of our method to different model backbones. The maximum prompt length is 6144 tokens and the maximum response length is 2048 tokens. As with WebShop, we sample 16 different groups per rollout in WebShop, resulting in a total of 16×8 = 128 environments (PPO uses 128 separate environments). The rollout temparature is set to 0.7. Each experiment implemented in veRL consists of 800 training steps. Table 4: Performance of our method on WebShop with varying α and β. Qwen2.5-7B-Instruct is used as the base model.*

![[obsidian-vault/assets/figures/papers/iclr26_reinforcement_learning_planning_agents__deep_rl__b001_ooROvpmxMV_Agentic_Reinforcement_Le/figures/020_Table_5.jpg]]
*Table 5: Performance on WebShop with Qwen2.5-1.5B-Instruct as the base model. Results are reported using one seed.*

### 6.1 主要结果

**Table 1** 展示了 iStar 在 WebShop 和 VisualSokoban 上的主要结果。iStar 在所有指标上均优于所有基线方法：

| 方法 | WebShop Success | WebShop Score | VisualSokoban Success |
|------|----------------|---------------|----------------------|
| GPT-5 | 62.5 | 79.1 | 28.0 |
| Gemini-2.5-Pro | 60.1 | 78.4 | 30.0 |
| DeepSeek-R1 | 67.8 | 82.3 | - |
| Claude-Sonnet-4-Thinking | 65.2 | 80.5 | 32.0 |
| PPO | 72.3 ± 3.1 | 85.1 ± 1.8 | - |
| GRPO | 76.8 ± 2.5 | 87.6 ± 1.2 | 78.5 ± 3.1 |
| RLOO | 80.2 ± 3.5 | 89.3 ± 1.5 | 85.4 ± 2.8 |
| REINFORCE++ | 79.5 ± 2.9 | 88.7 ± 1.3 | 84.1 ± 3.2 |
| PRIME | 81.5 ± 1.8 | 91.3 ± 0.6 | - |
| GiGPO | 84.1 ± 3.9 | 91.2 ± 1.5 | 85.9 ± 2.6 |
| **iStar (RLOO w/ iStar)** | **86.5 ± 2.8** | **93.6 ± 1.0** | **91.7 ± 1.2** |

**Table 2** 展示了 iStar 在 SOTOPIA 上的性能。在自聊天设置下，iStar 将困难场景的目标完成率从 7.92 提升至 8.06（提升 14%）；在与 GPT-4o 聊天时，从 6.68 提升至 7.16（提升 48%）。

### 6.2 消融实验

**Table 3** 展示了核心组件的消融实验结果：

- 使用 token 级过程奖励（PRIME）在 WebShop 上仅达到 82.0% 成功率和 90.0 分数，低于 iStar 的 89.1% 和 94.7。
- 将隐式步骤奖励合并到回合奖励中（merged rewards）在 WebShop 上仅达到 81.3% 成功率和 90.7 分数。
- 使用环境提供的原始步骤奖励（VisualSokoban）达到 91.0 成功率，低于 iStar 的 93.0。

**Table 7** 展示了 KL 散度惩罚的消融：移除 KL 惩罚后，WebShop 成功率从 82.8% 提升至 89.1%，分数从 92.0 提升至 94.7。

### 6.3 训练效率与动态分析

**Figure 4** 展示了 RL 训练期间的验证性能。iStar 实现了更快的性能提升和更高的最终性能，在 WebShop 上仅用 105 步就达到了 vanilla RLOO 的分数，训练效率提升约 2 倍。

**Figure 5** 展示了训练动态：(a)-(b) 显示隐式步骤奖励在训练早期即开始提升（尤其在 VisualSokoban 中），随后回合奖励跟进，表明 iStar 首先捕获了良好的局部动作启发式；(c)-(d) 显示 iStar 减少了不必要的动作，导致回合长度缩短而不影响任务成功率。

**Figure 3** 验证了 iStar 与多种 RL 算法（GRPO、RLOO、REINFORCE++、DAPO）的兼容性，在所有算法上均带来一致提升。

### 6.4 小模型与更多训练步数

**Table 5** 显示，使用 Qwen2.5-1.5B-Instruct 时，RLOO w/ iStar 达到 80.5% 成功率和 91.5 分数，优于 vanilla RLOO 的 71.9% 和 85.7。

**Figure 10-12** 显示，在更多训练步数和 GPU 小时数下，iStar 的性能提升保持稳定且一致。

## 方法谱系与知识库定位

iStar 属于**智能体强化学习**与**过程奖励建模**的交叉领域，其方法谱系如下：

- **基础方法**：DPO（Rafailov et al., 2024b）提供了隐式奖励建模的理论基础；PPO（Schulman et al., 2017）提供了策略更新的替代目标框架。
- **直接相关方法**：PRIME（Cui et al., 2025）使用 token 级隐式过程奖励，但仅适用于单轮 RL 任务；GiGPO（Feng et al., 2025）通过同状态分组计算步骤级优势，但依赖于罕见的状态重叠。
- **兼容算法**：iStar 可与 GRPO（Shao et al., 2024）、RLOO（Ahmadian et al., 2024）、REINFORCE++（Hu et al., 2025）和 DAPO（Yu et al., 2025）等主流 RL 算法无缝集成。

iStar 的核心贡献在于：首次将隐式步骤奖励引入多轮智能体 RL，通过在线多轮 DPO 学习步骤级奖励函数，并创新性地组合回合级与步骤级优势，实现了无需额外标注、低方差且与多种算法兼容的信用分配方案。该方法在 WebShop、VisualSokoban 和 SOTOPIA 等多样化任务上均取得了最先进的性能，为智能体强化学习中的信用分配问题提供了新的解决范式。

## 原文 PDF

## 相关样本

- [[obsidian-vault/analysis/ICLR_2026/In-the-Flow_Agentic_System_Optimization_for_Effective_Planning_and_Tool_Use.md|In-the-Flow]]：同属 agentic RL 样本，可对照隐式 step reward 与 flow-level planner 优化。

![[obsidian-vault/paperPDFs/ICLR_2026/Agentic_Reinforcement_Learning_with_Implicit_Step_Rewards.pdf]]
