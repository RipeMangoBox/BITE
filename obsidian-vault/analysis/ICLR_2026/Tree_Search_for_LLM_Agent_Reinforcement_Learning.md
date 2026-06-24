---
title: "Tree Search for LLM Agent Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Tree_Search_for_LLM_Agent_Reinforcement_Learning.pdf
openreview_forum_id: ZpQwAFhU13
aliases:
- TG
- TSLARL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "以智能体步骤（Thought-Action-Observation）为节点的树搜索采样策略：通过共享前缀增加有效样本量，并基于树结构构造树内组相对优势，将结局奖励自动转化为隐式步骤级偏好学习信号。"
primary_logic: "树内组相对策略优化（Intra-tree GRPO）在梯度结构上与步骤级DPO等价（仅权重项不同），从而在不引入额外标注的情况下，仅凭结局奖励即可实现细粒度过程监督，大幅提升样本效率与训练稳定性。"
claims:
- "Tree-GRPO在11个QA基准上全面超越链式GRPO，尤其在多跳任务上，小模型相对提升可达16%-69%。"
- "树内GRPO的梯度结构与步骤级DPO完全相同，二者仅在权重项上有别，从而赋予树内组优势隐式步骤级偏好学习的性质。"
- "树搜索在相同预算下可获约1.5倍样本量（因共享前缀降低平均深度），显著缓解多轮智能体RL的采样瓶颈。"
- "在极度受限的训练预算（≈2条完整轨迹）下，树式方法仍带来112%的多跳QA相对提升，远超链式方法。"
---

# Tree Search for LLM Agent Reinforcement Learning

> [!tip] 核心洞察
> 树内组相对策略优化（Intra-tree GRPO）在梯度结构上与步骤级DPO等价（仅权重项不同），从而在不引入额外标注的情况下，仅凭结局奖励即可实现细粒度过程监督，大幅提升样本效率与训练稳定性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于树搜索的LLM智能体强化学习方法 |
| 英文题名 | Tree Search for LLM Agent Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ZpQwAFhU13); [GitHub](https://github.com/AMAP-ML/Tree-GRPO) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Tree-GRPO |
| Dataset | Multi-Hop QA (Qwen2.5-3b), Multi-Hop QA (Qwen2.5-1.5b), Web-Agent QA SimpleQA (Qwen2.5-7b), Multi-Hop QA under budget ~2 (Qwen2.5-3b) |

> [!tip] 效果简介
> - Multi-Hop QA (Qwen2.5-3b) 上，EM Avg. 为 36.8，对比 31.8 (GRPO)，变化 +5.0 (+16% rel.)。
> - Multi-Hop QA (Qwen2.5-1.5b) 上，EM Avg. 为 19.1，对比 11.3 (GRPO)，变化 +7.8 (+69% rel.)。
> - Web-Agent QA SimpleQA (Qwen2.5-7b) 上，F1 为 67.8，对比 65.4 (GRPO)，变化 +2.4。

## 概述

长周期多轮智能体任务的强化学习面临一个根本瓶颈：仅以最终结局奖励作为监督信号，导致信用分配极度稀疏，训练效率低下。传统的链式采样策略在同一 Token 与工具调用预算下产生大量冗余轨迹，无法有效利用有限的采样资源。本文提出 **Tree-GRPO**（Tree-based Group Relative Policy Optimization），一种基于树搜索的分组智能体强化学习方法。其核心思路是将智能体交互步骤（Thought-Action-Observation 三元组）组织为树节点，通过共享前缀在固定预算内显著增加有效样本量，并利用树结构自动将结局奖励转化为隐式的步骤级偏好学习信号。

方法定位上，Tree-GRPO 属于群组相对策略优化（GRPO）范式的扩展，与 **ReAct**（Yao et al., 2022）智能体框架和 **DeepSeek-R1 的 GRPO**（DeepSeek-AI Team, 2025）构成直接演进关系。其关键创新在于将采样策略从独立链式改为“初始化-扩展”的树搜索，并在优势估计中引入树内组相对优势与树间组相对优势的组合——前者提供细粒度过程监督，后者维持训练稳定性。理论分析表明，树内 GRPO 的梯度结构与步骤级 DPO 完全等价（仅权重项不同），从而在不引入额外标注的前提下实现了隐式步骤级偏好学习。

实验覆盖 11 个 QA 基准，涵盖单跳 QA、多跳 QA 和 Web-Agent QA 三类任务。主要结果如下：

- **多跳 QA 显著提升**：在 Qwen2.5-3b 上，Tree-GRPO 相较链式 GRPO 取得 16% 的相对提升（EM Avg. 36.8 vs. 31.8）；在更小的 Qwen2.5-1.5b 上，相对提升高达 69%（19.1 vs. 11.3）。
- **极限预算下的样本效率**：当训练预算仅约 2 条完整轨迹时，树式方法仍带来 112% 的多跳 QA 相对提升（26.7 vs. 12.6），远超链式方法。
- **Web-Agent QA 一致优势**：在 SimpleQA 等 Web 智能体任务上，Tree-GRPO 同样优于链式 GRPO（F1 67.8 vs. 65.4）。
- **节点粒度关键性**：智能体步骤级树搜索显著优于 Token/句子级树搜索（多跳 QA 36.8 vs. 22.2），验证了以完整交互步骤为节点的设计选择。

方法存在以下主要局限：树内优势在低预算下单独使用可能导致训练崩溃，需依赖树间优势稳定训练；树结构超参数（树数量 M、扩展数 N 和 L）对性能敏感，需根据任务和预算仔细调节；此外，评估目前集中在 QA 类任务，在更开放的非 QA 智能体场景（如代码调试、多步工具链）上的有效性尚待验证。

## 背景与动机

### 长周期智能体任务中的稀疏奖励困境

大语言模型（LLM）驱动的多轮智能体系统在开放域问答、网页检索与工具调用等任务中展现出强大的推理与交互能力。这类任务通常遵循 **Thought-Action-Observation** 循环：模型在每个步骤中生成思考（Thought）、执行动作（Action）并接收环境反馈（Observation），形成一条多步轨迹
$$\mathcal{H} = \{ (\tau_0, \alpha_0, o_0), (\tau_1, \alpha_1, o_1), \ldots, (\tau_{T-1}, \alpha_{T-1}, o_{T-1}) \}$$

强化学习（RL）是提升此类智能体策略的有效途径，然而其核心瓶颈在于**监督信号极度稀疏**：训练仅在完整轨迹结束时获得单一的结局奖励（outcome reward），而长达数步甚至数十步的中间过程完全缺乏反馈。这导致信用分配（credit assignment）困难——模型难以辨别哪些步骤对最终成功起关键作用，哪些步骤是冗余甚至有害的。

### 链式采样的效率瓶颈

当前主流的智能体RL方法（如基于 **GRPO** 的链式群组相对策略优化，DeepSeek-AI Team, 2025）采用**独立链式采样**策略：对每个提示，并行生成多条相互独立的完整轨迹，并基于这些轨迹的结局奖励计算全局组相对优势。这一范式存在两个根本性缺陷：

1. **样本冗余严重**：各轨迹独立生成，无法共享公共前缀。在多轮智能体场景中，不同轨迹的前几步往往高度相似（如同样的检索查询或推理路径），但链式采样迫使模型反复生成相同内容，造成Token和工具调用预算的极大浪费。树搜索采样通过共享前缀，在相同预算下可获得约**1.5倍有效样本量**（因共享前缀降低平均深度，参见Eq. (4)）。

2. **过程监督信号缺失**：全局组相对优势将整条轨迹视为一个原子单元进行评分，无法区分轨迹内部各步骤的质量差异。即使某条轨迹的前几步正确、仅最后一步出错，其结局奖励仍为负，模型会无差别地惩罚所有步骤——包括那些本应被强化的正确行为。

### 现有方法的局限

在LLM推理领域，已有工作尝试引入树搜索来改善采样效率，但这些方法通常以**Token或句子**作为树节点粒度（参见Figure 2中间图）。对于智能体RL而言，这种粒度过细：一个完整的工具调用往往需要多个Token才能完成，以Token为节点进行分支会破坏动作的语义完整性，且无法有效利用工具调用的结构信息。

另一条路线是引入**步骤级过程奖励模型**，但这需要昂贵的人工标注或额外的模型训练。如何在**仅使用结局奖励**的前提下，自动构造细粒度的过程监督信号，仍是一个开放问题。

### 本文动机

针对上述问题，本文提出 **Tree-GRPO**（Tree-based Group Relative Policy Optimization），核心动机可概括为两点：

- **以智能体步骤为节点的树搜索采样**：将树节点锚定在完整的Thought-Action-Observation三元组上，而非Token或句子。通过共享公共前缀，在固定Token/工具调用预算下显著增加有效轨迹数量，缓解采样瓶颈。

- **利用树结构自动构造隐式步骤级偏好学习信号**：树结构天然形成“同前缀、不同后续”的轨迹对。基于树内组相对优势（intra-tree advantage），结局奖励被自动分解为步骤级偏好信号——这一机制在梯度结构上与步骤级DPO等价（仅权重项不同，参见Proposition 3.1），从而在不引入任何额外标注的情况下实现细粒度过程监督。

## 核心创新

### 瓶颈与突破口

长周期多轮智能体任务的核心瓶颈在于**仅用结局奖励导致的监督信号极度稀疏**。在传统的链式采样（independent chain-based rollouts）下，每条轨迹独立生成，同一Token/工具调用预算内样本冗余严重，训练信号利用效率低下。Tree-GRPO 通过两个关键设计打破这一僵局：

| 创新维度 | 链式基线（GRPO） | Tree-GRPO |
|---------|-----------------|-----------|
| **采样策略** | 独立链式采样 | 以智能体步骤为节点的树搜索采样 |
| **优势估计** | 仅全局组相对优势（inter-tree） | 树内优势 + 树间优势组合 |
| **信用分配粒度** | 轨迹级别 | 智能体步骤级别 |

### 创新一：步骤级树搜索采样

Tree-GRPO 将采样策略从独立链式改为**以 Thought-Action-Observation 三元组为节点的树搜索**。具体采用 initialize-then-expand 流程：先并行生成 $M$ 条完整链式轨迹作为初始树，再从每棵树中随机采样非叶节点进行扩展，生成 $N$ 条后续轨迹并插入树中。

这一设计的直接收益是**在相同预算下获得约 1.5 倍有效样本量**。因为随机采样节点的期望深度为最大深度的一半，扩展成本仅为完整轨迹的 $B/2$，总期望预算为：

$$\mathbb{E}[B_{\mathrm{tree}}] = M \cdot B + L \cdot N \cdot B / 2$$

共享前缀机制天然增加了分支点附近的样本密度，为后续的隐式过程监督提供了结构基础。

### 创新二：树内组相对优势与隐式步骤级偏好学习

这是 Tree-GRPO 最核心的理论贡献。在树结构的每个分支点，不同叶节点的结局奖励差异自然构成了偏好学习信号。Tree-GRPO 在每棵树内计算**树内组相对优势**：

$$\hat{A}_{\mathrm{Intra-tree}}(\mathcal{H}^i) = \frac{R(\mathcal{H}^i) - \mathrm{mean}(\{R(\mathcal{H}^j)\}_{j=1}^{G_{\mathrm{Intra-tree}}})}{\mathrm{std}(\{R(\mathcal{H}^j)\}_{j=1}^{G_{\mathrm{Intra-tree}}})}$$

最终优势为树内与树间优势之和：

$$\hat{A}_{\mathrm{tree}}(\mathcal{H}^i) = \hat{A}_{\mathrm{Intra-tree}}(\mathcal{H}^i) + \hat{A}_{\mathrm{Inter-tree}}(\mathcal{H}^i)$$

**Proposition 3.1** 揭示了这一设计的深层性质：树内 GRPO 的梯度结构与步骤级 DPO **完全等价**（仅权重项不同）。统一梯度形式为：

$$\nabla_{\theta} J_{\mathrm{unified}}(\theta) = w \cdot \big( \nabla_{\theta} \log p_{\theta}(\mathcal{H}_{\geq t}^{\mathrm{win}}) - \nabla_{\theta} \log p_{\theta}(\mathcal{H}_{\geq t}^{\mathrm{loss}}) \big)$$

其中树内 GRPO 的权重 $w = p_{\theta}(\mathrm{win}) \cdot p_{\theta}(\mathrm{loss})$，步骤级 DPO 的权重 $w = \sigma(\beta\Delta\log P)$。这意味着 **Tree-GRPO 在不引入任何额外标注的情况下，仅凭结局奖励就实现了步骤级过程监督**，大幅提升了样本效率与训练稳定性。

### 创新三：节点粒度的选择

Tree-GRPO 明确将树节点锚定在**智能体步骤级别**而非 Token 或句子级别。消融实验（Table 6）表明这一选择至关重要：步骤级树搜索在多跳 QA 上平均得分 36.8，远高于 Token/句子级的 22.2。原因在于智能体步骤（Thought-Action-Observation）是工具调用和推理决策的自然边界，在此粒度上进行分支和信用分配，能更准确地捕捉决策质量差异。

### 关键证据强度

| 核心主张 | 证据锚点 | 置信度 |
|---------|---------|--------|
| 树内 GRPO 与步骤级 DPO 梯度结构等价 | Proposition 3.1, Eq. (12) | 0.95 |
| 树搜索使样本量提升约 1.5 倍 | Eq. (4), §3.1 分析 | 0.95 |
| 步骤级粒度远优于 Token/句子级 | Table 6 | 0.98 |
| 极度受限预算（≈2条轨迹）下相对提升 112% | Table 3 | 0.98 |
| 组合树内外优势是稳定训练的必要条件 | Table 4（仅用树内优势在低预算下崩溃） | 0.95 |

## 整体框架

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ZpQwAFhU13/figures/003_Figure_3.jpg]]
*Figure 3: The overview of the Tree-GRPO training pipeline. The rollout is conducted in a tree-search manner, where each node corresponds to a complete thought-action-observation step. The group relative advantages are estimated at both intra-tree and inter-tree levels. Tree-GRPO constructs steplevel process supervision signals through a tree structure with a less rollout budget*

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ZpQwAFhU13/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of chain-based and tree-based sampling strategies in LLM multi-turn agent RL. The tree structure brings two major advantages: (i) less rollout budget (both on tokens and toolcalls); (ii) higher performance*

Tree-GRPO 的核心思路是将多轮智能体强化学习中的采样从独立链式轨迹替换为以**智能体步骤（Thought-Action-Observation 三元组）为节点的树搜索**，并在树结构上构造组内与组间双重相对优势，从而在不引入额外标注的前提下，仅凭结局奖励获得隐式步骤级过程监督信号。

### 问题设定

一个多轮智能体交互轨迹定义为 $T$ 步的序列：

$$\mathcal{H} = \{ (\tau_0, \alpha_0, o_0), (\tau_1, \alpha_1, o_1), \ldots, (\tau_{T-1}, \alpha_{T-1}, o_{T-1}) \}$$

其中 $\tau_t$ 为思考（Thought）、$\alpha_t$ 为工具调用（Action）、$o_t$ 为环境观测（Observation）。策略模型 $\pi_\theta$ 的目标是最大化期望回报 $\mathbb{E}_{\mathcal{H} \sim p_\theta}[R(\mathcal{H})]$，但长周期任务中仅有的结局奖励 $R(\mathcal{H})$ 导致信用分配极度稀疏。

### 训练流水线概览

Tree-GRPO 的训练流水线（Figure 3）由以下核心模块串联构成：

1. **树初始化（Tree Initialization）**：对每个提示，并行生成 $M$ 条完整链式轨迹作为初始树。
2. **节点采样（Node Sampling）**：从每棵树中随机采样非叶节点作为扩展点。
3. **扩展（Expansion）**：从采样节点的共享前缀上下文出发，继续生成 $N$ 条后续轨迹。由于随机扩展的期望深度为最大深度的一半，扩展阶段仅需约一半预算。
4. **树内组相对优势估计（Intra-tree Advantage）**：在每棵树内，基于各轨迹的结局奖励计算组内相对优势，隐式构造步骤级偏好信号。
5. **树间组相对优势估计（Inter-tree Advantage）**：跨所有树计算全局组相对优势，提供稳定的基线估计。
6. **策略优化（Policy Optimization）**：将树内与树间优势相加得到最终树结构优势 $\hat{A}_{\mathrm{tree}}$，代入 PPO 式剪辑目标并附加 KL 惩罚进行策略更新。

### 输入输出流

- **输入**：训练提示 $\mathbf{x} \sim \mathcal{D}$，参考策略 $\pi_{\mathrm{ref}}$，树结构超参数 $(M, N, L)$。
- **采样输出**：树结构轨迹集合，每条轨迹包含完整的 $(\tau, \alpha, o)$ 序列及其结局奖励 $R(\mathcal{H})$。
- **优势输出**：每条轨迹的树结构优势 $\hat{A}_{\mathrm{tree}}(\mathcal{H}^i) = \hat{A}_{\mathrm{Intra-tree}}(\mathcal{H}^i) + \hat{A}_{\mathrm{Inter-tree}}(\mathcal{H}^i)$。
- **优化目标**：

$$J_{\mathrm{Tree-GRPO}}(\theta) = \mathbb{E}_{\mathbf{x}, \mathcal{H} \sim \pi_{\mathrm{old}}} \left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|\mathcal{H}^i|} \sum_{t=1}^{|\mathcal{H}^i|} \min \left( r_{i,t}(\theta) \hat{A}_{\mathrm{tree}}, \mathrm{clip}(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_{\mathrm{tree}} \right) - \beta \mathbb{D}_{\mathrm{KL}} \right]$$

### 方法定位

Tree-GRPO 构建在群组相对策略优化（**GRPO**, DeepSeek-AI Team, 2025）之上，核心改动在于将独立链式采样替换为树搜索采样，并将优势估计从单一的全局组相对优势扩展为树内+树间双重结构。对比的基线方法包括：**ReAct**（Yao et al., 2022）作为智能体交互框架起点；**Search-o1**（Li et al., 2025c）作为集成搜索的非 RL 方法；**GSPO**（Zheng et al., 2025）作为另一种群组策略优化方法。

## 核心模块与公式推导

### 3.1 树搜索采样策略

Tree-GRPO 的采样策略以**智能体步骤（Thought-Action-Observation 三元组）为节点**，采用“先初始化后扩展”（initialize-then-expand）的并行化方案，包含三个核心步骤：

1. **Tree Initialization**：对每个提示 $\mathbf{x}$，并行生成 $M$ 条完整链式轨迹作为初始树，每条轨迹消耗预算 $B$。
2. **Node Sampling**：从每棵树中随机采样非叶节点作为扩展点。
3. **Expansion**：从采样节点的共享前缀上下文出发，继续生成 $N$ 条后续轨迹。由于随机采样的节点期望深度为最大深度的一半，每次扩展仅需约 $B/2$ 的预算，重复 $L$ 轮。

该策略的期望总预算为：

$$\mathbb{E}[B_{\mathrm{tree}}] = M \cdot B + L \cdot N \cdot B / 2 \tag{4}$$

其中 $M$ 为树的数量（控制探索广度），$N$ 为每次扩展的分支数，$L$ 为扩展轮次（后两者共同控制过程信号的粒度）。相比独立链式采样，共享前缀机制使相同预算下可获得约 **1.5 倍有效样本量**，显著缓解多轮智能体 RL 的采样瓶颈。

### 3.2 树结构优势估计

Tree-GRPO 的优势估计由两部分组合而成：

**树内组相对优势**（Intra-tree Advantage）：在每棵树 $\mathcal{T}_i$ 内，基于各轨迹的结局奖励计算组内相对优势：

$$\hat{A}_{\mathrm{Intra-tree}}(\mathcal{H}^i) = \frac{R(\mathcal{H}^i) - \mathrm{mean}(\{R(\mathcal{H}^j)\}_{j=1}^{G_{\mathrm{Intra-tree}}(\mathcal{T}_i)})}{\mathrm{std}(\{R(\mathcal{H}^j)\}_{j=1}^{G_{\mathrm{Intra-tree}}(\mathcal{T}_i)})} \tag{6}$$

在分支点处，不同叶子节点的结局奖励差异自然构成隐式的步骤级偏好学习信号。

**树间组相对优势**（Inter-tree Advantage）：跨所有树计算全局组相对优势，提供稳定的基线估计。

**最终树结构优势**为二者之和：

$$\hat{A}_{\mathrm{tree}}(\mathcal{H}^i) = \hat{A}_{\mathrm{Intra-tree}}(\mathcal{H}^i) + \hat{A}_{\mathrm{Inter-tree}}(\mathcal{H}^i) \tag{7}$$

### 3.3 策略优化目标

基于树结构优势，采用带剪辑的重要性采样与 KL 惩罚进行策略优化：

$$\begin{aligned}
J_{\mathrm{Tree-GRPO}}(\theta) = \mathbb{E}_{\mathbf{x}\sim\mathcal{D},\mathcal{H}\sim\pi_{\mathrm{old}}} \Bigg[ 
\frac{1}{G} \sum_{i=1}^{G} \frac{1}{|\mathcal{H}^i|} \sum_{t=1}^{|\mathcal{H}^i|} 
\min \Big( r_{i,t}(\theta) \hat{A}_{\mathrm{tree}}(\mathcal{H}^i), \mathrm{clip}(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_{\mathrm{tree}}(\mathcal{H}^i) \Big) \\
- \beta \mathbb{D}_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}})
\Bigg]
\end{aligned} \tag{8}$$

其中 $r_{i,t}(\theta) = \frac{\pi_{\theta}}{\pi_{\mathrm{old}}}$ 为重要性采样比，$\epsilon$ 为剪辑阈值，$\beta$ 为 KL 惩罚系数。

### 3.4 与步骤级 DPO 的结构等价性

**Proposition 3.1** 揭示了树内 GRPO 与步骤级 DPO 在梯度结构上的深层联系。在分支点 $t$ 处，将结局奖励较高的轨迹段记为 $\mathcal{H}_{\geq t}^{\mathrm{win}}$，较低的记为 $\mathcal{H}_{\geq t}^{\mathrm{loss}}$，二者梯度可统一为：

$$\nabla_{\theta} J_{\mathrm{unified}}(\theta) = w \cdot \big( \nabla_{\theta} \log p_{\theta}(\mathcal{H}_{\geq t}^{\mathrm{win}}) - \nabla_{\theta} \log p_{\theta}(\mathcal{H}_{\geq t}^{\mathrm{loss}}) \big) \tag{12}$$

两者的梯度结构**完全相同**，仅权重项 $w$ 不同：
- **树内 GRPO**：$w = p_{\theta}(\mathcal{H}_{\geq t}^{\mathrm{win}}) \cdot p_{\theta}(\mathcal{H}_{\geq t}^{\mathrm{loss}})$
- **步骤级 DPO**：$w = \sigma(\beta \Delta \log P)$

这一等价性意味着，Tree-GRPO 在不引入任何额外标注的情况下，仅凭结局奖励即可自动实现与步骤级 DPO 同构的细粒度过程监督，从而大幅提升样本效率与训练稳定性。

## 实验与分析

### 核心实验结果

Tree-GRPO在11个QA基准上系统性地验证了其有效性，涵盖单跳QA、多跳QA与Web-Agent QA三类任务。表1汇总了单跳与多跳QA的Exact Match（EM）分数，表2汇总了Web-Agent QA的F1分数。

**多跳QA上的显著提升。** 这是Tree-GRPO优势最突出的场景。在Qwen2.5-3b上，Tree-GRPO相比链式GRPO实现16%的相对提升（EM Avg. 36.8 vs. 31.8）；在更小的Qwen2.5-1.5b上，相对提升高达69%（EM Avg. 19.1 vs. 11.3）。值得注意的是，链式方法在1.5b模型上几乎无法激发多轮工具使用行为，而Tree-GRPO仍保持有效。在Qwen2.5-14b上，Tree-GRPO同样以8.4%的相对提升领先（Table 1）。


![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ZpQwAFhU13/figures/005_Table_1.jpg]]
*Table 1: Overall performance on single-hop QA and multi-hop QA, with EM scores for each dataset. The best results are indicated in bold*

**单跳QA上的稳定增益。** 虽然单跳QA的任务结构对过程监督的需求较弱，Tree-GRPO仍在小模型上表现出稳定提升。例如，Qwen2.5-1.5b和Qwen2.5-3b在单跳QA上的EM分数均超过链式GRPO和其他基线（Table 1）。

**Web-Agent QA上的持续优势。** 在四个Web-Agent QA基准（SimpleQA、GAIA、WebWalkerQA、BrowseComp）上，Tree-GRPO一致优于链式GRPO。最显著的提升出现在GAIA数据集，Qwen2.5-7b下Tree-GRPO的F1达到67.8，相比GRPO的65.4有+2.4的绝对提升（Table 2）。但在BrowseComp这类极难任务上，所有RL方法的提升幅度均有限，这被归因于该任务缺乏高质量训练数据。

### 样本效率与预算消融

Table 3揭示了Tree-GRPO在极度受限训练预算下的核心优势。当每个提示仅分配约2条完整轨迹的预算时，树式方法在多跳QA上取得26.7的EM平均分，而链式方法仅为12.6，相对提升达112%。随着预算增加至4、8、16，树式方法始终保持领先，且优势在低预算区间最为显著。这一结果直接验证了树搜索通过共享前缀增加有效样本量的机制——在相同Token和工具调用预算下，树结构可获约1.5倍样本量（Eq. (4)），从而显著缓解多轮智能体RL的采样瓶颈。


![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ZpQwAFhU13/figures/007_Table_3.jpg]]
*Table 3: Performance with different training budget (defined as the cost of several complete agent trajectories per prompt). The base model is Qwen2.5-3b. The best results are indicated in bold*

### 树结构优势消融

Table 4将优势估计分解为三个变体：纯树内优势（Intra-tree only）、纯树间优势（Inter-tree only）、组合优势（Intra-tree + Inter-tree）。在预算≈4的设置下，组合优势相比纯链式基线提升约16%，而单独使用树内优势在低预算下会导致训练崩溃。这验证了树间优势作为稳定基线估计的必要性——树内优势虽能提供隐式步骤级过程信号，但其方差较大，需与全局组相对优势组合才能实现稳定训练。


![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ZpQwAFhU13/figures/014_Table_4.jpg]]
*Table 4: Ablation study on tree-based advantages*

### 树搜索粒度消融

Table 6对比了Token/句子级树搜索与智能体步骤级树搜索（本文方法）的性能差异。在相同的Qwen2.5-3b基座和预算（4/提示）下，智能体步骤级树搜索在多跳QA上取得36.8的EM平均分，远超Token/句子级的22.2；在单跳QA上同样领先（50.0 vs. 46.2）。Figure 7的训练奖励曲线进一步显示，智能体步骤级树搜索在整个训练过程中保持稳定且更高的奖励水平。这验证了以完整Thought-Action-Observation三元组为节点粒度的合理性：步骤级节点能更准确地捕获智能体决策的结构化边界，从而构造更有效的过程监督信号。


![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_ZpQwAFhU13/figures/016_Table_6.jpg]]
*Table 6: Test score comparison between tree search at token/sentence-level and agent step-level. The base model is Qwen2.5-3b. The rollout budget is 4/per prompt. Tree search parameters are M = 2 , N = 2 , L = 1*

### 树结构超参数敏感性

Table 7探索了树结构超参数M（树数量）、N（扩展节点数）、L（扩展轮次）对性能的影响。在不同预算水平下，最优配置存在差异：低预算（≈2）时，(M=2, N=2, L=1) 取得最佳平均分；高预算（≈16）时，(M=2, N=4, L=1) 表现更好。总体趋势表明，M控制探索广度（树的数量），N和L控制利用深度（过程信号粒度）；过高M或过低N/L均导致性能下降，需根据任务和预算仔细调节。

### 训练动态分析

Figure 5展示了树式与链式RL在训练过程中的奖励和工具调用次数对比。树式方法不仅获得更高的训练奖励，还促使模型产生更长的交互轨迹——平均工具调用次数从2.4增加到3.0。这表明树搜索的过程监督信号不仅提升了答案质量，还鼓励了更充分的探索行为。Figure 6的学习率预热比例与KL系数消融进一步表明，Tree-GRPO在各种超参数设置下均稳定优于链式基线，方法鲁棒性良好。

### 失败模式分析

案例研究（Table 10, Table 11）揭示了Tree-GRPO的两类典型失败模式：

1. **检索不完整。** 在多跳QA中，模型虽能检索到部分相关信息，但未能穷举所有正确答案。例如，某案例中模型仅返回David Hasselhoff，而忽略了问题涉及的其他演员（Table 10）。这说明模型在已获取相关信息后，仍缺乏系统性的信息整合与验证能力。

2. **缺乏反思推理。** 在Web-Agent QA中，模型有时沿错误推理路径持续深入，缺乏中途反思和纠错的能力。例如，某WebWalkerQA案例中，模型在初始检索结果不相关后，未能调整搜索策略，导致最终答案错误（Table 11）。这指向一个开放问题：如何在仅用结局奖励的框架内，进一步引入反思推理机制到训练循环中。
## 方法谱系与知识库定位

### 核心基线关系

Tree-GRPO 的直接技术前身是 **GRPO**（Group Relative Policy Optimization，DeepSeek-AI Team, 2025），后者将一组独立采样的链式轨迹作为群组，基于群组内结局奖励的均值与标准差构造相对优势估计。Tree-GRPO 继承了 GRPO 的群组相对优势框架与 PPO 式剪辑目标，但在两个关键维度上进行了结构性改造：**采样策略**从独立链式采样变为以智能体步骤为节点的树搜索采样，**优势估计**从纯全局组相对优势扩展为树内-树间双层组合优势。这一改造的因果机制在于：树结构在分支点处自动将结局奖励的差异转化为隐式步骤级偏好信号，从而在不引入额外过程标注的前提下缓解了长周期多轮任务的信用分配稀疏问题。

另一重要基线是 **GSPO**（Zheng et al., 2025），同为群组策略优化方法，但未采用树结构采样，因此在相同预算下无法获得前缀共享带来的样本量增益。实验表明 Tree-GRPO 在 11 个 QA 基准上全面超越链式 GRPO，小模型（Qwen2.5-1.5b）在多跳 QA 上的相对提升可达 69%（Table 1），验证了树结构改造的因果有效性。

### 与非 RL 方法的边界

在 Web-Agent QA 场景中，Tree-GRPO 与 **Search-o1**（Li et al., 2025c）——一种集成搜索的进阶 RAG 方法——形成对比。Search-o1 依赖外部检索增强推理，而 Tree-GRPO 通过 RL 微调直接优化智能体的工具调用策略。两者的适用边界不同：Search-o1 在知识密集型单跳检索任务上可能更具样本效率，但 Tree-GRPO 在多轮交互决策任务中展现出更强的泛化能力，尤其在训练预算极度受限时（≈2 条完整轨迹）仍能取得 112% 的多跳 QA 相对提升（Table 3）。

### 方法谱系中的定位

从梯度结构的角度，Tree-GRPO 的树内组相对优势与步骤级 DPO 存在深刻的等价关系。**Proposition 3.1** 证明，两者梯度具有统一形式：

$$\nabla_{\theta} J_{\mathrm{unified}}(\theta) = w \cdot \big( \nabla_{\theta} \log p_{\theta}(\mathcal{H}_{\geq t}^{\mathrm{win}}) - \nabla_{\theta} \log p_{\theta}(\mathcal{H}_{\geq t}^{\mathrm{loss}}) \big)$$

仅权重项 $w$ 不同：树内 GRPO 的 $w = p_{\theta}(\mathrm{win}) \cdot p_{\theta}(\mathrm{loss})$，步骤级 DPO 的 $w = \sigma(\beta \Delta \log P)$。这表明 Tree-GRPO 在仅使用结局奖励的条件下，自动实现了与需要显式偏好标注的步骤级 DPO 等效的过程监督学习。这一性质将 Tree-GRPO 定位为**隐式过程监督 RL** 方法，填补了纯结局奖励 RL（如 GRPO）与显式步骤级偏好学习（如步骤级 DPO）之间的方法论空白。

### 适用边界与局限

1. **训练数据质量依赖**：在 Web-Agent QA 的极难基准（如 BrowseComp）上，RL 带来的提升有限，根因在于训练数据质量不足，而非方法本身失效。这是当前方法的适用上界。

2. **树内优势的不稳定性**：单独使用树内优势在低预算下易导致训练崩溃（Table 4），必须组合树间优势作为稳定基线。这表明树内信号虽能提供细粒度过程监督，但其方差较大，需要全局归一化来抑制梯度震荡。

3. **超参数敏感性**：树结构超参数 $M$（树数量，控制探索广度）、$N$（扩展节点数）和 $L$（扩展轮次，控制过程信号粒度）需根据任务和预算仔细调节。过高 $M$ 或过低 $N/L$ 均导致性能下降（Table 7），说明树搜索的探索-利用平衡对最终效果有显著影响。

4. **任务类型局限**：当前验证集中在 QA 类智能体任务（单跳 QA、多跳 QA、Web-Agent QA），未覆盖代码调试、多步工具链组合等更开放的非 QA 智能体场景。这是方法泛化性的待验证边界。

### 开放问题

- 如何在保持仅用结局奖励的前提下，将反思推理（reflection）和更丰富的探索策略（如 MCTS 式选择扩展）引入训练循环？
- 为什么模型在已检索到相关信息时仍不能穷举所有正确答案（如 Case 3 仅返回 David Hasselhoff 而忽略其他演员）？这是检索-推理耦合的深层问题。
- Tree-GRPO 在非 QA 智能体任务（如代码调试、多步工具使用）中的适用性如何？树结构的步骤级信用分配是否能在更长的工具链上保持有效？

## 原文 PDF

![[paperPDFs/ICLR_2026/Tree_Search_for_LLM_Agent_Reinforcement_Learning.pdf]]
