---
title: "Opponent Shaping in LLM Agents"
type: paper
paper_level: B
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Opponent_Shaping_in_LLM_Agents.pdf
aliases:
- OSLA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/multi_agent
core_operator: "用结构化自然语言历史提示和 PPO+LoRA 微调，让 LLM 塑形者在重复博弈中影响对手学习动态。"
primary_logic: |
  将回合内与回合间交互历史写入 LLM 提示，LLM 生成文本动作并映射为博弈动作；塑形者通过 PPO 和 LoRA 按博弈收益及 KL 惩罚更新，利用历史中体现的对手策略变化实现无需显式梯度的模型无关对手塑形。
claims:
- "回合间历史是 LLM 对手塑形成功的关键信号，仅使用当前状态或回合内历史时塑形收益显著下降。"
- "ShapeLLM 在多个重复正规型博弈中显著提升塑形者奖励，并在合作性与竞争性设置中均显示效果。"
cited_by: 2
---

# Opponent Shaping in LLM Agents

> [!tip] 核心洞察
> LLM智能体可以通过结构化自然语言提示编码回合内与回合间的历史交互信息，从而间接观察对手的参数更新方向，实现模型无关的对手塑形，因为回合间历史包含了对手策略变化的痕迹，从而使塑形者无需显式梯度即可影响对手学习成为可能。

| 字段 | 内容 |
| ------- | --------------------------------------------------------------------------------------- |
| 中文题名 | LLM智能体中的对手塑形 |
| 英文题名 | Opponent Shaping in LLM Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=yJoHTqUNry) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/multi_agent |
| Method | ShapeLLM |
| Dataset | IPD, IMP, ICG, C-IPD, ISH |

> [!tip] 效果简介
> - 在IPD中，ShapeLLM使塑形者平均每步奖励达到3.96，而独立PPO基线仅为1.0，提升约296%。
> - 在IMP中，塑形者平均奖励为0.99，基线为-0.03，提升超过34倍。
> - 在合作性游戏C-IPD中，塑形者奖励达5.88，基线为1.0，提升488%。

## 概述

本文提出ShapeLLM，将对手塑形引入LLM智能体。方法把传统多智能体强化学习中的状态和动作表示替换为结构化自然语言提示与文本生成动作，并用PPO和LoRA对塑形者进行参数高效更新。其核心证据来自重复正规型博弈实验：塑形者利用回合间历史捕捉对手学习轨迹，在多个竞争性和合作性博弈中获得高于独立PPO基线的奖励。

## 背景与动机

在多智能体强化学习中，对手塑形（Opponent Shaping, OS）旨在让一个智能体通过自身行为策略性地影响对手的学习动态，从而引导对手朝向对己方有利的方向更新策略。经典的OS方法如LOLA（Learning with Opponent-Learning Awareness）通过计算对手梯度的高阶导数来实现塑形，但面临可扩展性差、需要对手模型等瓶颈。后续的模型无关OS方法（Lu et al., 2022; Khan et al., 2024）虽降低了计算复杂度，但仍依赖表格策略或循环神经网络，无法直接应用于基于Transformer的大语言模型（LLM）智能体。

现有LLM在博弈中的研究（如Akata et al., 2025）主要关注单次博弈或固定策略的重复博弈，尚未探索智能体能否通过交互主动改变对手的学习轨迹。核心瓶颈在于：LLM的离散文本输出、高维参数空间以及缺乏显式的对手模型，使得传统OS算法无法直接迁移。因此，本文提出ShapeLLM，首次将对手塑形引入LLM智能体领域。

## 核心创新

核心洞察：LLM智能体可以通过结构化自然语言提示编码回合内与回合间的历史交互信息，从而间接观察对手的参数更新方向，实现模型无关的对手塑形，因为回合间历史包含了对手策略变化的痕迹，从而使塑形者无需显式梯度即可影响对手学习成为可能。

具体而言，ShapeLLM将传统OS中的向量化状态替换为自然语言提示，将直接动作选择替换为文本生成，并通过LoRA微调实现参数高效更新。这一设计使得原本需要高阶导数的塑形过程，转化为基于PPO的强化学习问题，大幅降低了应用门槛。

## 整体框架

![[assets/figures/papers/d8d14098-7c88-4b22-b93c-e89703540ffb/figures/001_Figure_1.jpg]]
*Figure 1: Schematic representation of a trial. Each box corresponds to an episode (a game played for T rounds). Same-colored boxes represent episodes within the same parallel environment. Within each environment, episodes occur sequentially as indicated by the arrows. The shaper updates its parameters using the experience collected throughout the entire trial*

 ShapeLLM的整体框架围绕“试验（Trial）”组织，每个试验包含多个并行环境，每个环境运行若干回合（Episode），每个回合包含T步博弈。

系统包含四个核心模块：
1. **环境交互模块**：两个LLM智能体（塑形者与朴素学习者）在重复正规型博弈中生成文本动作，动作通过映射函数转换为博弈动作。
2. **提示构建模块**：为每个智能体构建结构化自然语言提示，包含博弈描述、当前状态、回合内历史以及回合间历史（即之前回合的摘要）。
3. **PPO微调模块**：使用PPO算法对塑形者的LLM进行LoRA微调，奖励为博弈收益减去KL散度惩罚，以保持生成稳定性。
4. **试验组织模块**：管理并行环境与回合的调度，确保塑形者能够跨回合积累经验。

## 核心模块与公式推导

**模块1：策略分布**

LLM智能体的策略定义为给定上下文c下生成token序列w_{1:L}的概率：

$$\rho_\theta(w_{1:L} | c) = \prod_{l=1}^{L} \rho_\theta(w_l | c, w_{<l})$$

其中θ为LoRA微调参数，c包含博弈描述、历史状态和动作标签。该公式将传统策略网络替换为自回归语言模型，使得策略能够利用预训练知识。

**模块2：动作映射**

由于LLM输出为文本，需要映射到离散博弈动作：

$$\phi_i(w) = \begin{cases} a_1 & \text{if } w = w_{a_1} \\ a_2 & \text{if } w = w_{a_2} \\ a_{\text{null}} & \text{otherwise} \end{cases}$$

其中w_{a_1}和w_{a_2}是预定义的动作标签（如“Cooperate”和“Defect”），a_null表示无效输出时的默认动作。该映射确保了LLM生成与博弈动作空间的对齐。

**模块3：PPO训练目标**

塑形者通过PPO最大化期望收益，同时加入KL惩罚项以约束策略更新幅度：

$$\mathcal{L}(\theta) = \mathbb{E}_t \left[ \min(r_t(\theta) A_t, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon) A_t) \right] - \beta \cdot \text{KL}[\rho_{\theta_{\text{old}}} \| \rho_\theta]$$

其中r_t(θ)为重要性采样比率，A_t为优势函数，β为KL系数。该目标在塑形者与朴素学习者之间非对称更新：仅塑形者更新参数，朴素学习者保持固定或独立PPO更新。

## 实验与分析

实验在五个经典重复正规型博弈上进行：IPD（囚徒困境）、IMP（匹配硬币）、ICG（斗鸡博弈）、C-IPD（合作性囚徒困境）和ISH（猎鹿博弈）。基模型为gemma-2-2b-it，使用LoRA（秩2）微调。

**主要结果**：![[assets/figures/papers/d8d14098-7c88-4b22-b93c-e89703540ffb/figures/008_Table_1.jpg]]
*Table 1: Post-training evaluation results for the IPD, IMP, and ICG comparing baseline (two naive learners) versus shaper-naive learner pairs. Average rewards per step are reported with 95% confidence intervals across 5 random seeds, except for the ICG baseline, where we use 10. Transitions involving $a _ { \mathrm { n u l l } }$ are excluded (comprising 2% of actions in IPD, 0.1% in IMP, and 1% in ICG)*

展示了塑形者与朴素学习者配对后的平均每步奖励。在竞争性博弈中，ShapeLLM显著提升了塑形者收益：IPD中塑形者达3.96（基线1.0），IMP中达0.99（基线-0.03），ICG中达2.98（基线2.0）。在合作性博弈中，C-IPD塑形者达5.88（基线1.0），ISH达3.96（基线1.3）。所有结果均基于5-10个随机种子的95%置信区间，统计显著性高。

**消融实验**：![[assets/figures/papers/d8d14098-7c88-4b22-b93c-e89703540ffb/figures/036_Table_16.jpg]]
*Table 16: Post-training evaluation results for the IPD with one shaper against a naive learner, where the shaper receives varying levels of intra- and inter-episode history. Average rewards per step are reported with 95% confidence intervals across 5 random seeds. Transitions with $\boldsymbol { a } _ { \mathrm { n u l l } }$ are excluded from the analysis (∼ 1% of actions)

验证了回合间历史的关键作用。当仅提供当前状态或仅提供回合内历史时，塑形者奖励降至约0.99（IPD），与基线无异，说明回合间历史是塑形成功的必要条件。此外，![[assets/figures/papers/d8d14098-7c88-4b22-b93c-e89703540ffb/figures/037_Figure_9.jpg]]
*Figure 9: Average reward per step (top row) and state visitation (bottom row) during training for the IPD ablation experiments. The shaper receives either only the current state (left) or full intra-episode history (right), with no inter-episode information in either case. In the state visitation figures, the outcome $\bar { } ^ { 6 6 } \bar { } \Gamma ^ { 3 }$ encompasses all transitions where either player chose $a _ { \mathrm { n u l l } }$ . The results are reported along with a 95% confidence interval over 5 random seeds

展示了不同对手初始策略下的训练曲线，塑形效果在p0=0.25、0.50、0.75时均保持稳定，表明ShapeLLM对对手初始化具有鲁棒性。

**跨模型验证**：使用Llama-3.2-1B-Instruct进行初步验证，结果与gemma-2-2b-it一致，提示ShapeLLM可能具有一定的架构泛化能力（置信度0.6）。

## 方法谱系与知识库定位

ShapeLLM属于模型无关对手塑形（Model-free opponent shaping）方法谱系，直接继承自Lu et al. (2022)和Khan et al. (2024)的工作，并受到LOLA (Foerster et al., 2018)的概念启发。

**改变的槽位**：
- **架构**：从表格策略/RNN替换为Transformer LLM + LoRA（创新性：高）。
- **推理策略**：从直接动作选择替换为自然语言生成（创新性：高）。
- **数据管道**：从向量状态替换为结构化自然语言提示（创新性：高）。
- **训练配方**：从标准PPO修改为PPO + LoRA + 非对称更新（创新性：中）。

**知识库定位**：ShapeLLM是“LLM智能体对手塑形”这一种子任务的首个方法，评估于重复正规型博弈数据集。其父方法为模型无关对手塑形，基线包括独立PPO学习者和LOLA。未来工作可沿以下方向展开：扩展到连续动作空间、更复杂的博弈环境、以及多智能体塑形场景。当前证据表明，ShapeLLM在简单矩阵博弈中有效，但跨架构泛化能力仍需更多验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Opponent_Shaping_in_LLM_Agents.pdf]]
