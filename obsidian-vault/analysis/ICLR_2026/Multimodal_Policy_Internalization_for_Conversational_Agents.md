---
title: "Multimodal Policy Internalization for Conversational Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Multimodal_Policy_Internalization_for_Conversational_Agents.pdf
openreview_forum_id: fSE0rUngCX
aliases:
- MPICA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过三阶段训练（视觉掩码连续预训练 VM-CPT、思维链监督微调 CoT SFT 和基于策略感知强化学习的 PolicyRollout）将策略知识内化到模型参数中，从而在推理时无需提供上下文策略，同时提高策略遵循能力。"
primary_logic: "直接对策略文本进行持续预训练能够显式注入策略知识，而 PolicyRollout 通过在 rollout 阶段引入策略感知响应而不改变训练路径，在增强探索的同时避免了训练-推理不一致。"
claims:
- "TriMPI 在 ClevrPolicy 和 GTAPolicy 上实现了相较于 CoT SFT 基线约 70.7% 的绝对准确率提升，相较于上下文策略设置提升 79.4%。"
- "消融研究显示 RL 阶段和 VM-CPT 阶段对性能贡献最大，且 PolicyRollout 进一步带来提升。"
- "内化后提示 token 数减少高达 93.9%，预填充推理时间减少 85.7%。"
- "TriMPI 在策略更新（Policy Override）和策略知识嵌入（Policy Referral）评估中一致优于基线，表现出更强的泛化能力。"
---

# Multimodal Policy Internalization for Conversational Agents

> [!tip] 核心洞察
> 直接对策略文本进行持续预训练能够显式注入策略知识，而 PolicyRollout 通过在 rollout 阶段引入策略感知响应而不改变训练路径，在增强探索的同时避免了训练-推理不一致。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向对话智能体的多模态策略内化 |
| 英文题名 | Multimodal Policy Internalization for Conversational Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=fSE0rUngCX) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | TriMPI |
| Dataset | ClevrPolicy-T (N=6), ClevrPolicy-M (N=6), GTAPolicy, 效率指标 (ClevrPolicy & GTAPolicy) |

> [!tip] 效果简介
> - ClevrPolicy-T (N=6) 上，准确率 (Acc) 为 65.85 (TriMPI w/ PoRo-GRPO)，对比 17.80 (CoT SFT)，变化 +48.05。
> - ClevrPolicy-M (N=6) 上，准确率 (Acc) 为 84.70 (TriMPI w/ PoRo-GRPO)，对比 14.30 (CoT SFT)，变化 +70.40。
> - GTAPolicy 上，整体分数 (Overall) 为 81.06 (TriMPI w/ PoRo-GRPO)，对比 54.50 (CoT SFT)，变化 +26.56。

## 概述

### 问题瓶颈

多模态对话智能体在推理时通常需要将冗长的策略（policy）作为上下文前缀输入模型。这些策略长度可达 1K–50K tokens，不仅带来固定的推理计算开销，更关键的是，模型难以一致地遵循这些需要复杂推理的策略。这一瓶颈随着策略复杂度的上升而急剧恶化——在 ClevrPolicy 基准上，即使最强的 Claude-4 模型，当决策树层数增至 N=6 时也开始出现显著性能下降（Table 1）。

### 核心方法

本文提出 **TriMPI**（Three-stage Multimodal Policy Internalization），通过三阶段训练将策略知识**内化**到模型参数中，使模型在推理时无需接收上下文策略即可生成策略符合的响应：

1. **视觉掩码连续预训练（VM-CPT）**：在监督微调之前，对含策略的思维链数据进行视觉 token 掩码的语言建模，直接将策略知识注入模型参数。
2. **思维链监督微调（CoT SFT）**：使用显式策略推理的思维链数据进行监督训练，使模型学习策略推理过程。
3. **基于 PolicyRollout 的强化学习**：在 GRPO/DAPO 的 rollout 阶段额外构建含上下文策略的输入实例，生成策略感知响应并加入 rollout 空间，在增强探索 grounded 程度的同时避免训练-推理不一致。

### 核心结论

**性能跃升**：TriMPI 在 ClevrPolicy 和 GTAPolicy 上实现了相较于 CoT SFT 基线约 **70.7%** 的绝对准确率提升，相较于上下文策略设置提升 **79.4%**（Table 2）。

**效率革命**：策略内化后，提示 token 数减少高达 **93.9%**，预填充推理时间减少 **85.7%**（Figure 6），显著降低了推理成本。

**泛化能力**：TriMPI 在策略更新（Policy Override）和策略知识嵌入（Policy Referral）评估中一致优于所有基线（Table 3），表明内化的策略知识具有鲁棒的可迁移性。

**消融验证**：强化学习阶段和 VM-CPT 阶段对性能贡献最大；PolicyRollout 在 GRPO 和 DAPO 上均带来额外增益，验证了策略感知 rollout 的有效性（Table 2 消融分析）。

### 方法谱系与知识库定位

TriMPI 处于**多模态对齐**与**提示压缩**的交叉地带，但其定位与现有工作有本质区别：

- **vs. 软提示（Soft Prompting）**：不训练额外的任务专用嵌入，避免损害模型的通用推理能力。
- **vs. 审议对齐（Deliberative Alignment）**：共享“将外部规范内化”的高层动机，但 TriMPI 聚焦于多模态策略推理场景，且通过 VM-CPT 实现显式的策略知识注入。
- **vs. 标准 GRPO/DAPO**：PolicyRollout 在不改变策略梯度路径的前提下，通过策略感知响应扩展探索空间，解决了标准 RL 在复杂策略场景下探索不足的问题。

### 局限与开放问题

当前方法在合成数据集（ClevrPolicy）和小规模真实数据（GTAPolicy，451 训练样本）上验证，策略复杂度仍相对有限；视觉掩码预训练策略较为简单，缺乏更精细的多模态知识注入机制；仅在 Qwen2.5-VL 系列上评估，未验证跨架构泛化性。未来方向包括：扩展到更多样化的真实世界任务、开发更复杂的多模态持续预训练策略、探索多策略同时内化时的干扰问题，以及 PolicyRollout 思想向其他 RL 算法的推广。

## 背景与动机

多模态对话智能体在真实应用中需要遵循日益复杂的策略（policy）——这些策略通常以提示前缀（prompt prefix）的形式提供给模型，长度可达约1K至50K tokens。这种依赖带来了两个核心瓶颈：

1. **固定推理计算开销**：长策略作为上下文的一部分，每次推理都需要编码，导致预填充（prefill）时间显著增加。
2. **策略遵循困难**：即使最先进的多模态模型（如Claude-4）也难以一致地遵循需要多步推理的复杂策略。实验表明，当策略复杂度随决策树层数（N）增加时，所有模型的零样本上下文性能均显著下降（Table 1），在GTAPolicy上最佳工具调用准确率仅为60%左右。

现有缓解方案存在明显局限。**软提示（soft prompting）**方法通过训练特殊嵌入来压缩提示，但这些嵌入与特定任务绑定，限制了模型的通用推理能力和鲁棒性。**监督微调（SFT）**基线方法（如Direct SFT和CoT SFT）虽然尝试让模型在无上下文策略的情况下学习策略遵循，但在复杂策略上性能仍然不足——CoT SFT在ClevrPolicy-M（N=6）上准确率仅为14.30%（Table 2），远未达到实用水平。

本文的核心动机在于：**能否将策略知识内化（internalize）到模型参数中，使模型在推理时无需显式提供上下文策略，同时提升策略遵循能力？** 这一目标与deliberative alignment共享高层动机，但强调超越简单的提示压缩，追求模型与策略的深度对齐。Figure 1直观对比了标准上下文推理与策略内化后推理的差异：前者依赖长策略输入但遵循效果有限，后者在移除上下文策略后反而实现更准确、更高效的策略遵循生成。

## 核心创新

### 问题瓶颈：长策略提示带来的推理负担与遵循困难

多模态对话智能体在部署时通常需要将复杂的行为策略作为上下文前缀（prompt prefix）提供给模型。这些策略长度可达约 1K–50K tokens，带来两个核心问题：

1. **固定推理计算开销**：每次推理都必须处理完整的策略文本，造成大量冗余的预填充（prefill）计算。
2. **策略遵循困难**：模型难以一致地遵循需要多步推理的复杂策略，尤其在策略涉及视觉条件判断时表现显著下降（Table 1 显示，即使最强基线 Claude‑4‑Sonnet 在 ClevrPolicy‑M N=6 上准确率也仅 77.76%）。

TriMPI 的核心创新在于将策略知识**内化到模型参数中**，使推理时无需提供上下文策略，同时提升策略遵循能力。其形式化目标为：

$$A = \mathcal{M}_{\theta}(Q, I, P) \xrightarrow[\theta]{\mathrm{Policy\ Internalization}} A = \mathcal{M}_{\theta}(Q, I)$$

其中 $\mathcal{M}_{\theta}$ 为多模态模型，$Q$ 为查询，$I$ 为图像输入，$P$ 为策略文本。内化后，模型在仅接收 $Q$ 和 $I$ 的条件下即可生成策略符合的响应 $A$。

### 关键 changed slots：三阶段训练框架

TriMPI 相对于基线方法（Direct SFT、CoT SFT）的三个核心 changed slots 构成了一条从“显式注入策略知识”到“策略感知强化探索”的完整链路。

#### Changed Slot 1：视觉掩码连续预训练（VM‑CPT）

**基线做法**：直接进行监督微调（SFT），模型仅从输入‑输出对中隐式学习策略规则。

**TriMPI 做法**：在 SFT 之前引入一个连续预训练阶段。具体而言，构造包含策略文本的思维链（CoT）数据集变体，对其中所有非视觉 token 计算下一 token 预测损失：

$$\mathcal{L}(\boldsymbol{\theta}) = -\mathbb{E}_{x \sim \mathcal{D}}\left[\frac{1}{\sum_{t=1}^{T} m_{t}} \sum_{t=1}^{T} m_{t} \log p_{\theta}(x_{t} \mid x_{<t})\right], \quad m_{t} = \mathbf{1}[x_{t} \notin P_{I} \cup I]$$

其中 $P_I$ 和 $I$ 分别表示策略文本和输入中的视觉 token。通过屏蔽视觉 token 的损失计算，VM‑CPT 将策略知识**显式注入**模型参数，为后续的 SFT 和 RL 阶段提供更强的先验。

**证据强度**：消融实验（Table 2）显示，移除 VM‑CPT 阶段（即仅 CoT SFT + GRPO）导致性能明显下降，验证了预训练策略注入对后续 RL 探索的促进作用。

#### Changed Slot 2：强化学习阶段（RL with GRPO/DAPO）

**基线做法**：仅使用 SFT（Direct SFT 或 CoT SFT），模型缺乏对策略相关行为的系统性探索。

**TriMPI 做法**：在 CoT SFT 之后加入基于 GRPO 或 DAPO 的强化学习阶段。RL 利用奖励信号（ClevrPolicy 采用精确匹配奖励 $R_{\mathrm{Acc}} = \mathbf{1}[\mathrm{Exact.Match}(y, \hat{y})]$，GTAPolicy 采用工具调用准确率与参数分数的加权平均）驱动模型探索策略遵循行为空间。

**证据强度**：消融实验（Table 2）表明，移除 RL 阶段（仅 VM‑CPT + CoT SFT）使 ClevrPolicy‑T 准确率从 65.85 骤降至 22.75，证实 RL 对复杂策略内化至关重要。

#### Changed Slot 3：PolicyRollout（PoRo）

**基线做法**：标准 GRPO/DAPO rollout 仅基于无策略输入 $Q, I$ 采样响应，探索空间缺乏策略 grounding。

**TriMPI 做法**：PolicyRollout 在 rollout 阶段额外构造一组包含上下文策略的输入实例 $(Q, I, P)$，生成策略感知响应，并将其与无策略响应拼接形成扩展的 rollout 空间。修改后的 GRPO 目标为：

$$\mathcal{T}_{\mathrm{poRo-GRPO}}(\theta) = \mathbb{E}_{[\{\sigma_i\}_{i=1}^{G} \sim \pi_{\theta_{old}}(O|Q,I), \{\sigma_j\}_{j=G}^{2G} \sim \pi_{\theta_{old}}(O|Q,I,P)]} \frac{1}{2G} \sum_{i=1}^{2G} \{ \min[r_i(\theta)\hat{A}_i, \mathrm{clip}(r_i(\theta), 1-\epsilon_l, 1+\epsilon_h)\hat{A}_i] - \beta \mathbb{D}_{KL}[\pi_{\theta}||\pi_{ref}] \}$$

其中一半 rollout 来自无策略路径，一半来自有策略路径，但**策略梯度仅应用于无策略路径**（条件仅依赖于 $Q, I$），从而确保训练与推理的一致性。

**核心洞察**：PolicyRollout 通过引入策略感知响应扩展探索空间，使模型在训练中接触到更高质量的策略遵循行为，同时避免训练‑推理不一致。这本质上是一种“利用上下文策略指导探索但不改变训练路径”的巧妙设计。

**证据强度**：Table 2 显示，PolicyRollout 在 GRPO 和 DAPO 上均带来额外提升（TriMPI w/ GRPO vs TriMPI w/ PoRo‑GRPO；TriMPI w/ DAPO vs TriMPI w/ PoRo‑DAPO），验证了策略感知 rollout 的有效性。

### 创新总结

TriMPI 的三个 changed slots 形成了一条因果链路：**VM‑CPT 显式注入策略知识 → CoT SFT 学习显式推理 → RL + PolicyRollout 进行策略感知的 grounded 探索**。这一设计使得模型在推理时完全摆脱上下文策略依赖，同时实现显著的性能提升（相比于 CoT SFT 基线绝对准确率提升约 70.7%，相比于上下文策略设置提升 79.4%）和效率提升（提示 token 数减少高达 93.9%，预填充推理时间减少 85.7%）。

## 整体框架

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_fSE0rUngCX/figures/005_Figure_4.jpg]]
*Figure 4: Overview of different training algorithms for multimodal policy internalization. The solid purple outlines indicate the parts where the next-token prediction loss is computed. On the right, we illustrate the proposed three-stage training strategy, TriMPI, which enables direct policy knowledge injection through the VM-CPT stage and policy-grounded reinforcement learning through PolicyRollout. The PolicyRollout algorithm is detailed in §4.3 and illustrated in Figure 5*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_fSE0rUngCX/figures/001_Figure_1.jpg]]
*Figure 1: Motivation of the proposed Multimodal Policy Internalization task. The goal is to enhance the policy-following abilities of a large multimodal model without requiring the policy to be provided in-context during inference, thereby improving both performance and efficiency*

### 核心问题与内化目标

多模态对话智能体在现实部署中依赖以提示前缀形式提供的复杂策略 (policy)，这些策略文本长度可达 1K–50K tokens，不仅带来巨大的固定推理计算开销，而且模型难以一致地遵循这些需要推理的策略。TriMPI 的核心思路是将策略知识从外部上下文“内化”到模型参数中，使得推理时无需再提供策略提示，同时提升策略遵循的准确率。其形式化目标为：

$$A = \mathcal{M}_{\theta}(Q, I, P) \xrightarrow[\theta]{\mathrm{Policy Internalization}} A = \mathcal{M}_{\theta}(Q, I)$$

其中 $\mathcal{M}_{\theta}$ 为多模态模型，$Q$ 为用户查询，$I$ 为视觉输入，$P$ 为策略文本。内化后的模型在仅接收 $Q$ 和 $I$ 的条件下，即可生成策略符合的响应 $A$。

### 三阶段训练管线

TriMPI 通过三个顺序阶段将策略知识逐步注入模型参数 (Figure 4)：

1. **视觉掩码连续预训练 (VM-CPT)**：在 SFT 之前，利用包含策略的思维链 (CoT) 数据对基座模型进行持续预训练。该阶段对所有非视觉 token 计算下一个 token 预测损失，显式屏蔽策略文本和输入中的视觉 token，从而将策略知识直接注入模型参数。其损失函数为：

   $$\mathcal{L}(\boldsymbol{\theta}) = -\mathbb{E}_{x \sim \mathcal{D}}\left[\frac{1}{\sum_{t=1}^{T} m_{t}} \sum_{t=1}^{T} m_{t} \log p_{\theta}(x_{t} \mid x_{<t})\right], \quad m_{t} = \mathbf{1}[x_{t} \not\in P_{I} \cup I]$$

2. **思维链监督微调 (CoT SFT)**：使用生成的 CoT 数据对模型进行监督训练，使模型学习显式的策略推理过程。CoT 序列 $O = [C; A]$ 由推理链 $C$ 和答案 $A$ 拼接而成，训练目标为标准的负对数似然：

   $$\mathcal{L}_{\mathrm{SFT}} = -\mathbb{E}_{(Q,O) \sim \mathcal{D}} \left[ \sum_{t=1}^{|O|} \log p_{\theta}(o_t | Q, o_{<t}) \right]$$

3. **强化学习与 PolicyRollout**：在 CoT SFT 之后引入 GRPO/DAPO 强化学习，利用奖励信号进行探索，更好地覆盖策略相关行为。该阶段的核心创新是 **PolicyRollout (PoRo)**：在 rollout 阶段额外构建含上下文策略的输入实例，生成策略感知响应并将其加入 rollout 空间，从而在不改变训练-推理路径的前提下增强探索的 grounded 程度。具体而言，对于每个采样实例，一半 rollout 来自无策略路径 $(Q, I)$，另一半来自有策略路径 $(Q, I, P)$；策略梯度仅应用于无策略路径，确保训练与推理一致 (Figure 5)。

   修改后的 GRPO 目标为：

   $$\mathcal{T}_{\mathrm{poRo-GRPO}}(\theta) = \mathbb{E}_{[\{\sigma_i\}_{i=1}^{G} \sim \pi_{\theta_{old}}(O|Q,I), \{\sigma_j\}_{j=G}^{2G} \sim \pi_{\theta_{old}}(O|Q,I,P)]} \frac{1}{2G} \sum_{i=1}^{2G} \{ \min[r_i(\theta)\hat{A}_i, \mathrm{clip}(r_i(\theta), 1-\epsilon_l, 1+\epsilon_h)\hat{A}_i] - \beta \mathbb{D}_{KL}[\pi_{\theta}||\pi_{ref}] \}$$

### 输入输出流与模块关系

整体管线中，策略 $P$ 仅在训练阶段出现，推理时模型仅接收查询 $Q$ 和图像 $I$。三个模块的因果关系为：VM-CPT 显式注入策略知识 $\rightarrow$ CoT SFT 学习显式推理过程 $\rightarrow$ RL + PolicyRollout 通过策略感知探索进一步强化策略遵循能力。消融实验表明，RL 阶段和 VM-CPT 阶段对性能贡献最大，且 PolicyRollout 在 GRPO 和 DAPO 上均带来额外提升，验证了各模块间的协同效应。

## 核心模块与公式推导

### 问题形式化

多模态策略内化（MPI）的目标是将策略 $P$ 的知识嵌入模型参数 $\theta$，使模型在推理时无需提供上下文策略即可生成策略符合的响应。形式化表示为：

$$A = \mathcal{M}_{\theta}(Q, I, P) \xrightarrow[\theta]{\mathrm{Policy Internalization}} A = \mathcal{M}_{\theta}(Q, I)$$

其中 $\mathcal{M}_{\theta}$ 为多模态大模型，$Q$ 为查询，$I$ 为视觉输入，$P$ 为策略文本，$A$ 为答案。内化后，模型仅依赖 $Q$ 和 $I$ 即可输出策略合规的 $A$。

### TriMPI 三阶段训练框架

TriMPI 由三个顺序阶段构成：**视觉掩码连续预训练（VM-CPT）**、**思维链监督微调（CoT SFT）** 和 **基于 PolicyRollout 的强化学习（RL）**。各阶段的核心机制如下。

#### 阶段一：VM-CPT —— 策略知识直接注入

VM-CPT 在 SFT 之前执行，目标是将策略知识显式注入模型参数。具体做法：构造包含策略的 CoT 数据变体，对序列中除视觉 token 外的所有 token 计算下一个 token 预测损失。

$$\mathcal{L}(\boldsymbol{\theta}) = -\mathbb{E}_{x \sim \mathcal{D}}\left[\frac{1}{\sum_{t=1}^{T} m_{t}} \sum_{t=1}^{T} m_{t} \log p_{\theta}(x_{t} \mid x_{<t})\right], \quad m_{t} = \mathbf{1}[x_{t} \not\in P_{I} \cup I]$$

其中 $m_t$ 为掩码指示函数：当 token $x_t$ 不属于策略中的视觉 token 集合 $P_I$ 或输入中的视觉 token 集合 $I$ 时取 1，否则取 0。这种选择性掩码确保模型专注于学习策略文本中的语言知识与推理逻辑，而非视觉特征。

#### 阶段二：CoT SFT —— 显式推理过程学习

在 VM-CPT 之后，使用生成的思维链数据对模型进行监督微调。输出序列 $O = [C; A]$ 由思维链 $C$ 和答案 $A$ 拼接而成，训练目标为标准的负对数似然：

$$\mathcal{L}_{\mathrm{SFT}} = -\mathbb{E}_{(Q,O) \sim \mathcal{D}} \left[ \sum_{t=1}^{|O|} \log p_{\theta}(o_t | Q, o_{<t}) \right]$$

该阶段使模型学会显式地推理策略规则，为后续 RL 阶段的探索提供良好的初始化。

#### 阶段三：RL with PolicyRollout —— 策略感知的强化学习

RL 阶段采用 GRPO/DAPO 算法，并引入 **PolicyRollout（PoRo）** 机制。核心创新在于：rollout 阶段额外构造包含上下文策略的输入实例，生成策略感知响应并加入 rollout 空间，但策略梯度仅应用于无策略路径，从而在增强探索的同时避免训练-推理不一致。

以 GRPO 为例，PoRo-GRPO 的目标函数为：

$$\mathcal{T}_{\mathrm{poRo-GRPO}}(\theta) = \mathbb{E}_{[\{\sigma_i\}_{i=1}^{G} \sim \pi_{\theta_{old}}(O|Q,I), \{\sigma_j\}_{j=G}^{2G} \sim \pi_{\theta_{old}}(O|Q,I,P)]} \frac{1}{2G} \sum_{i=1}^{2G} \{ \min[r_i(\theta)\hat{A}_i, \mathrm{clip}(r_i(\theta), 1-\epsilon_l, 1+\epsilon_h)\hat{A}_i] - \beta \mathbb{D}_{KL}[\pi_{\theta}||\pi_{ref}] \}$$

其中 $r_i(\theta) = \frac{\pi_{\theta}(\sigma_i|Q,I)}{\pi_{\theta_{old}}(\sigma_i|Q,I)}$ 为重要性采样比率。关键设计：前 $G$ 个 rollout 来自无策略条件 $\pi_{\theta_{old}}(O|Q,I)$，后 $G$ 个来自策略感知条件 $\pi_{\theta_{old}}(O|Q,I,P)$，但所有 rollout 在计算优势 $\hat{A}_i$ 和策略梯度时统一视为无策略路径生成，确保训练与推理条件一致。

#### 奖励函数设计

针对不同基准采用不同的准确率奖励：

- **ClevrPolicy**：解析响应与真实答案完全匹配时奖励为 1，否则为 0。
  $$R_{\mathrm{Acc-ClevrPolicy}} = \mathbf{1}[\mathrm{Exact.Match}(y, \hat{y})]$$

- **GTAPolicy**：工具调用准确率与参数分数的加权平均。
  $$R_{\mathrm{Acc-GTAPolicy}} = 0.5 \times \mathrm{Tool.Acc} + 0.5 \times \mathrm{Argument.Score}$$

### 各模块的因果贡献

消融实验揭示了三个阶段的因果重要性：

1. **RL 阶段贡献最大**：移除 RL（仅保留 VM-CPT + CoT SFT）使 ClevrPolicy-T 准确率从 65.85 骤降至 22.75，表明 RL 对复杂策略的探索与优化不可或缺。
2. **VM-CPT 提供关键先验**：移除 VM-CPT（仅 CoT SFT + GRPO）导致性能下降，说明预训练阶段的策略知识注入为 RL 探索提供了更好的起点。
3. **PolicyRollout 带来额外增益**：在 GRPO 和 DAPO 上分别加入 PoRo 均带来一致提升，验证了策略感知 rollout 在增强探索 grounded 程度方面的有效性。

## 实验与分析

### 核心性能突破

TriMPI 在 ClevrPolicy 和 GTAPolicy 两个基准上均实现了相较于基线方法的显著提升。**Table 2** 展示了主要结果：在最具挑战性的 ClevrPolicy-M（N=6）设置下，TriMPI w/ PoRo-GRPO 达到 84.70% 准确率，而 CoT SFT 基线仅为 14.30%，绝对提升高达 70.40 个百分点；相较于上下文策略（In-Context）设置，提升幅度达到 79.4%。在 ClevrPolicy-T（N=6）上，TriMPI w/ PoRo-GRPO 达到 65.85%，较 CoT SFT 的 17.80% 提升 48.05 个百分点。在 GTAPolicy 上，TriMPI w/ PoRo-GRPO 的整体分数（Overall）达到 81.06，远超 CoT SFT 的 54.50（+26.56 个百分点）。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_fSE0rUngCX/figures/007_Table_2.jpg]]
*Table 2: Main results and ablations on multimodal policy internalization performance. By default, we use Qwen2.5-VL-7B as the base model. PoRo refers to PolicyRollout. The metrics are reported as percentages (%) and are detailed in Appendix C.3. We observe significant improvements of TriMPI over in-context and SFT baselines. Comprehensive ablations demonstrate the importance of each stage and the effectiveness of PolicyRollout. The RL steps indicate the actual update steps (for the three datasets, respectively, separated by “|”). Early stopping (marked with “*”) may occur in DAPO (Yu et al., 2025) runs due to its dynamic sampling strategy. Notably, on DAPO, TriMPI achieves competitive or stronger pe...*

这些结果表明，三阶段训练框架能够将复杂策略知识有效内化到模型参数中，使模型在推理时无需上下文策略即可生成策略符合的响应。

### 效率增益

策略内化带来的效率提升同样显著。**Figure 6** 显示，内化后提示 token 数减少高达 93.9%，预填充推理时间减少 85.7%。这一效率增益源于推理时完全移除了原本长达 1K-50K tokens 的策略前缀，从根本上降低了固定推理计算开销。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_fSE0rUngCX/figures/009_Figure_6.jpg]]
*Figure 6: Efficiency metrics before and after MPI*

### 消融实验：各阶段贡献

**Table 2** 的消融实验系统验证了三阶段训练框架中每个模块的必要性：

**RL 阶段的关键作用**：移除 RL 阶段（仅保留 VM-CPT + CoT SFT）导致 ClevrPolicy-T 准确率从 65.85 骤降至 22.75，表明对于需要复杂推理的策略，单纯依赖 SFT 无法有效内化策略知识。RL 阶段通过奖励信号驱动的探索，使模型能够覆盖更广泛的策略相关行为空间。

**VM-CPT 阶段的注入效应**：比较 CoT SFT + GRPO 与 TriMPI w/ GRPO（即增加 VM-CPT 阶段），后者在各项指标上均有提升，验证了在 SFT 前通过视觉掩码持续预训练直接注入策略知识的有效性。VM-CPT 为后续的 RL 探索提供了更好的参数初始化。

**PolicyRollout 的增益**：PolicyRollout 在 GRPO 和 DAPO 两种 RL 算法上均带来额外提升。TriMPI w/ PoRo-GRPO 相较于 TriMPI w/ GRPO，在 ClevrPolicy-M 上从 83.30 提升至 84.70；TriMPI w/ PoRo-DAPO 相较于 TriMPI w/ DAPO，在 ClevrPolicy-T 上从 73.35 提升至 77.80。这验证了策略感知 rollout 扩展探索空间的有效性——通过在 rollout 阶段引入含上下文策略的响应，使模型接触到更 grounded 的策略遵循行为，同时保持训练-推理一致性（策略梯度仅应用于无策略路径）。

### 泛化能力评估

**策略覆盖（Policy Override）**：**Table 3（左）** 评估了模型在推理时接收更新后策略的表现。TriMPI w/ PoRo-GRPO 在 ClevrPolicy-T 上达到 48.70%，在 ClevrPolicy-M 上达到 82.70%，在 GTAPolicy 上整体分数为 63.00%，一致优于所有基线。这表明内化后的模型能够灵活地在内化策略和上下文指令之间切换，符合实际部署中策略动态更新的需求。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_fSE0rUngCX/figures/010_Table_3.jpg]]
*Table 3: Left: Policy Override results. We show that TriMPI consistently outperforms strong baselines in generalizing to updated policies, demonstrating favorable real-world usage where model behavior can be governed by both internalized policies and in-context instructions. Right: Policy Referral results. We use Claude-4 to rank the consistency between the model’s intermediate thoughts and the original policy on a scale of 0-10. A higher score indicates better embedded policy knowledge*

**策略引用（Policy Referral）**：**Table 3（右）** 通过 Claude-4 评判模型中间推理与原始策略的一致性（0-10 分）。TriMPI 获得最高评分，表明其内化的策略知识更为准确和完整，模型在推理过程中能够正确引用策略规则。

**策略上下文恢复**：**Table 4** 显示，即使推理时重新加入策略上下文，TriMPI 仍然优于所有基线方法。在 GTAPolicy 上，TriMPI w/ PoRo-GRPO 整体分数达到 66.81，超过 CoT SFT + GRPO 的 64.66。这说明 TriMPI 不仅实现了策略内化，还通过训练过程增强了模型利用策略信息的能力。

### 失败模式分析

尽管 TriMPI 取得了显著提升，但实验揭示了若干值得关注的局限性：

**策略复杂度瓶颈**：**Table 1** 显示，随着决策树层数 N 从 2 增加到 6，所有模型的零样本上下文性能均显著下降。即使最强的 Claude-4-Sonnet，在 ClevrPolicy-M（N=6）上也仅达到 77.76%。这表明当前策略复杂度已接近模型能力的边界，更复杂的真实业务策略可能带来更大挑战。

**感知错误传播**：在 ClevrPolicy 的视觉推理任务中，当物体被遮挡或视觉特征不明确时，模型可能产生感知错误，进而导致策略推理在错误的感知基础上进行。**Figure 14** 的分支错误分析显示，TriMPI 在部分条件分支（如 ID 3.2、4.1、5.1）上的分布与 Gold CoT 存在较大偏差，提示模型在特定策略路径上仍存在系统性错误。

**数据集规模限制**：GTAPolicy 仅包含 451 个训练样本，ClevrPolicy 基于合成数据生成，可能无法完全覆盖真实场景中的策略多样性和视觉复杂性。这限制了方法在更广泛实际应用中的泛化性验证。

**模型架构单一性**：所有实验均基于 Qwen2.5-VL 系列模型（3B/7B），未在其他多模态大模型架构（如 LLaVA 系列）上验证 TriMPI 的泛化性。**Table 8** 显示性能增益在 3B 和 7B 模型上均成立，且复杂策略上的增益更显著，但跨架构的迁移性仍有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_fSE0rUngCX/figures/006_Figure_5.jpg]]
*Figure 5: Illustration of the PolicyRollout algorithm (applied to GRPO as an example). During the rollout phase, we additionally construct a set of input instances with the policy included in-context. These policy-aware responses are added to the rollout space as if they were generated from the original inputs without the policy in-context. The advantage and policy gradient are then computed on the combined rollouts, indicated by the thick red outlines. PolicyRollout enables more policyaware exploration without introducing a gap between training and inference, leading to significant improvements in MPI, especially on complex policies*

## 方法谱系与知识库定位

### 问题定位：从上下文策略到参数化策略

TriMPI 的核心动机源于多模态对话智能体面临的一个现实瓶颈：为约束模型行为而设计的策略（policy）通常以提示前缀形式注入上下文，其长度可达 1K–50K tokens。这不仅带来固定的推理计算开销，更关键的是，现有大模型难以一致地遵循这些需要多步推理的复杂策略。TriMPI 将这一问题形式化为**多模态策略内化**（Multimodal Policy Internalization, MPI），其目标是将策略知识从上下文迁移至模型参数，使推理时无需显式提供策略即可生成策略符合的响应：

$$
A = \mathcal{M}_{\theta}(Q, I, P) \xrightarrow[\theta]{\mathrm{Policy Internalization}} A = \mathcal{M}_{\theta}(Q, I)
$$

这一目标与 deliberative alignment（Guan et al., 2024; Zhang et al., 2025）共享高层动机——强调提升模型对策略的对齐能力，而非仅仅压缩提示。与软提示（soft prompting）方法不同，TriMPI 不训练额外的特殊嵌入，因为后者与特定任务强绑定，会限制模型的通用推理能力和鲁棒性。

### 基线方法谱系

论文对比了两类直接基线：

- **Direct SFT**：不使用思维链的监督微调，直接从输入映射到答案。该方法缺乏显式的策略推理过程，难以捕获策略中的条件逻辑。
- **CoT SFT**：使用思维链数据进行监督微调，让模型在训练时显式推理策略规则。其训练目标为在拼接的思维链 $C$ 和答案 $A$ 上计算负对数似然：

  $$\mathcal{L}_{\mathrm{SFT}} = -\mathbb{E}_{(Q,O) \sim \mathcal{D}} \left[ \sum_{t=1}^{|O|} \log p_{\theta}(o_t | Q, o_{<t}) \right], \quad O = [C; A]$$

  尽管 CoT SFT 引入了推理过程，但仅靠监督信号难以充分覆盖策略中的边界情况和复杂决策路径。

在强化学习层面，TriMPI 基于 **GRPO**（Shao et al., 2024）和 **DAPO**（Yu et al., 2025）两种 GRPO 风格的 RL 算法构建，并通过 PolicyRollout 对其进行扩展。

### TriMPI 三阶段训练框架

TriMPI 通过三个递进阶段将策略知识内化到模型参数中：

**阶段一：视觉掩码连续预训练（VM-CPT）**。在 SFT 之前，对包含策略的 CoT 数据变体进行语言建模，但屏蔽策略和输入中的所有视觉 token，仅对文本 token 计算下一个 token 预测损失：

$$\mathcal{L}(\boldsymbol{\theta}) = -\mathbb{E}_{x \sim \mathcal{D}}\left[\frac{1}{\sum_{t=1}^{T} m_{t}} \sum_{t=1}^{T} m_{t} \log p_{\theta}(x_{t} \mid x_{<t})\right], \quad m_{t} = \mathbf{1}[x_{t} \notin P_{I} \cup I]$$

该阶段的核心作用是**显式注入策略知识**，为后续 SFT 和 RL 提供更好的参数初始化。

**阶段二：思维链监督微调（CoT SFT）**。使用生成的 CoT 数据对模型进行标准监督训练，使模型学习显式的策略推理过程。

**阶段三：基于 PolicyRollout 的强化学习**。在 CoT SFT 之后引入 RL 阶段，利用奖励信号进行探索，更好地覆盖策略相关行为。奖励函数根据任务设计：ClevrPolicy 采用精确匹配奖励 $R_{\mathrm{Acc-ClevrPolicy}} = \mathbf{1}[\mathrm{Exact.Match}(y, \hat{y})]$；GTAPolicy 采用工具调用准确率与参数分数的加权平均 $R_{\mathrm{Acc-GTAPolicy}} = 0.5 \times \mathrm{Tool.Acc} + 0.5 \times \mathrm{Argument.Score}$。

### PolicyRollout：策略感知的强化学习探索

PolicyRollout 是 TriMPI 的关键创新。标准 GRPO/DAPO 的 rollout 仅基于无策略的输入 $(Q, I)$，探索空间缺乏策略约束。PolicyRollout 在 rollout 阶段额外构建含上下文策略的输入实例 $(Q, I, P)$，生成策略感知响应并与无策略响应拼接，形成扩展的 rollout 空间：

$$\mathcal{T}_{\mathrm{poRo-GRPO}}(\theta) = \mathbb{E}_{[\{\sigma_i\}_{i=1}^{G} \sim \pi_{\theta_{old}}(O|Q,I), \{\sigma_j\}_{j=G}^{2G} \sim \pi_{\theta_{old}}(O|Q,I,P)]} \frac{1}{2G} \sum_{i=1}^{2G} \{ \min[r_i(\theta)\hat{A}_i, \mathrm{clip}(r_i(\theta), 1-\epsilon_l, 1+\epsilon_h)\hat{A}_i] - \beta \mathbb{D}_{KL}[\pi_{\theta}||\pi_{ref}] \}$$

关键设计在于：**策略梯度仅应用于无策略路径**（仅条件于 $Q$ 和 $I$），从而确保训练与推理的一致性，避免引入 train-inference gap。这一机制使模型在训练时能借助策略感知响应进行更 grounded 的探索，同时推理时无需策略上下文。

### 适用边界与局限

**数据集规模与多样性有限**。ClevrPolicy 基于合成数据生成，GTAPolicy 仅包含 451 个训练样本。尽管决策树层数可达 6 层，但真实业务策略可能包含更复杂的逻辑分支、更长的上下文以及更丰富的视觉场景。当前评估无法完全反映真实世界的复杂性。

**模型架构验证范围窄**。所有实验仅基于 Qwen2.5-VL 模型系列（3B 和 7B），未在其他多模态大模型架构（如 LLaVA 系列、InternVL 系列）上验证泛化性。不同架构的视觉编码器和跨模态融合机制可能影响策略内化的效果。

**视觉掩码策略较为简单**。VM-CPT 仅屏蔽视觉 token，缺乏更精细的多模态知识注入方法。对于需要细粒度视觉推理的策略（如 ClevrPolicy-M 中的多模态示例），这种粗粒度掩码可能限制了视觉-策略联合知识的有效注入。

**单一策略类型**。训练和评估关注单一策略类型，尚未探索混合多个策略或动态策略切换的场景。在实际应用中，智能体可能需要同时遵循多种响应格式或行为约束的策略，如何避免策略间干扰是未解决的问题。

**感知错误的连锁效应**。在复杂视觉场景中，感知错误（如遮挡物体识别失败）如何影响策略推理链条，以及模型如何改进鲁棒性，论文未深入探讨。

### 开放问题

1. **数据扩展方向**：如何将数据集扩展到更多样化的真实世界图像和任务，以提升策略内化方法的实用性？合成数据与真实数据的领域差距是当前方法落地的主要障碍。

2. **持续预训练策略深化**：能否开发更复杂的持续预训练策略，而不仅仅是屏蔽视觉 token？例如，设计对比学习目标或视觉-策略对齐任务，以更好地处理多模态策略中的视觉条件分支。

3. **多策略内化**：当需要同时内化多个不同响应格式的策略时，如何设计有效的训练策略避免干扰？策略间的知识共享与冲突消解是实际部署中的关键挑战。

4. **PolicyRollout 的推广**：PolicyRollout 的思想——在 rollout 空间中加入 grounded 响应但不改变梯度路径——是否可以推广到 GRPO/DAPO 之外的其他强化学习算法（如 PPO、REINFORCE）？这一设计模式可能具有更广泛的适用性。

5. **感知-推理联合优化**：在策略内化框架中，如何联合优化视觉感知和策略推理模块，使模型在感知不确定时仍能做出稳健的策略符合决策？

## 原文 PDF

![[paperPDFs/ICLR_2026/Multimodal_Policy_Internalization_for_Conversational_Agents.pdf]]
