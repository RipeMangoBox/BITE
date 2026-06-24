---
title: "Memory-T1: Reinforcement Learning for Temporal Reasoning in Multi-session Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Memory_T1_Reinforcement_Learning_for_Temporal_Reasoning_in_Multi_session_Agents.pdf
openreview_forum_id: vQf2YR2Kpd
aliases:
- MT
- Memory-T1
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过强化学习训练的时间感知记忆选择策略，结合多层次奖励（特别是时间一致性奖励），使代理能够从长对话历史中精准选择时间上一致的证据会话。"
primary_logic: "粗到细的检索与多粒度奖励（答案正确、证据接地、时间一致性）协同作用，为代理提供了密集的监督信号，使其能辨别时间模糊性、抵抗噪声，在长上下文中保持稳健的时间推理能力。"
claims:
- "Memory-T1 在 Time-Dialog 上达到 67.0% 的整体得分，显著超越 14B 基线（60.7%，提升 6.3 百分点/约 10.2%）及各类专门模型 (Time-R1 49.4%, MemAgent 49.9%)，证明了时间感知记忆策略的核心价值。"
- "消融实验显示，移除时间一致性奖励中的时序接近度 Rs 会导致简单任务性能提升 23.4% 但复杂推理崩溃 56.2%，而完全去除 Rt 则对各类任务均造成重大损害，突显时间一致性信号对复杂时间推理不可或缺。"
- "在长达 128k token 的上下文测试中，基线模型（Qwen2.5）性能崩溃，但 Memory-T1 保持高 F1 甚至提升，彰显粗到细检索的有效抗噪能力。"
- "使用 GRPO 训练的策略在整体与复杂任务上均显著优于 PPO（3B 模型整体 +18.5%），证明选择合适 RL 算法对稳定训练至关重要。"
---

# Memory-T1: Reinforcement Learning for Temporal Reasoning in Multi-session Agents

> [!tip] 核心洞察
> 粗到细的检索与多粒度奖励（答案正确、证据接地、时间一致性）协同作用，为代理提供了密集的监督信号，使其能辨别时间模糊性、抵抗噪声，在长上下文中保持稳健的时间推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Memory-T1：多会话代理中时间推理的强化学习方法 |
| 英文题名 | Memory-T1: Reinforcement Learning for Temporal Reasoning in Multi-session Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vQf2YR2Kpd); [GitHub](https://github.com/Elvin-Yiming-Du/Memory-T1/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Memory-T1 |
| Dataset | Time-Dialog |

> [!tip] 效果简介
> - Time-Dialog 上，Overall Score 为 67.0 (Memory-T1 7B)，对比 60.7 (Qwen2.5-14B)，变化 +6.3 (约 +10.2%)。
> - Time-Dialog 上，Overall Score 为 66.9 (Memory-T1 3B)，对比 49.4 (Time-R1)，变化 +17.5。
> - Time-Dialog 上，Overall Score 为 66.9 (Memory-T1 3B)，对比 49.9 (MemAgent)，变化 +17.0。

## 概述

多会话对话代理需在冗长、跨时间的交互历史中精确定位事件并执行时间推理。现有长上下文模型将对话历史视为平文本，难以有效解析时间表达式，在噪声密集的多会话场景中易出现事件顺序混乱与信息混淆，导致时间推理性能急剧下降。

**Memory-T1** 针对这一瓶颈，提出一种基于强化学习的时间感知记忆选择框架。其核心思路是：通过粗到细的级联检索与多层次密集奖励（答案正确性、证据接地、时间一致性）的协同作用，使代理能够从长对话历史中精准选择时间上一致的证据会话，从而在嘈杂上下文中保持稳健的时间推理能力。

关键结果：
- 在 Time-Dialog 基准上，Memory-T1 7B 达到 **67.0%** 的整体得分，显著超越 Qwen2.5-14B 基线（60.7%，提升约 10.2%），以及各类专门模型如 Time-R1（49.4%）和 MemAgent（49.9%）。
- 在长达 128k token 的极端上下文测试中，基线模型性能崩溃，而 Memory-T1 保持高 F1 甚至提升，验证了粗到细检索的抗噪能力。
- 消融实验表明，时间一致性奖励中的时序接近度分量对复杂推理不可或缺——移除后简单任务虽提升 23.4%，但复杂推理崩溃 56.2%。

方法定位：Memory-T1 属于**记忆增强的强化学习代理**范畴，区别于全上下文输入、标准 RAG 以及仅用答案精度奖励训练的基线。其关键创新在于将时间感知的硬过滤与 GRPO 策略优化结合，为多会话时间推理提供了密集的监督信号。

## 背景与动机

### 长上下文对话中的时间推理困境

多会话对话代理（multi-session agents）需要跨越多次交互来理解用户意图、追踪事件演变并回答时间敏感问题。在诸如个人助手、客服系统、医疗咨询等场景中，对话历史可能累积至数万甚至数十万 token，其中夹杂大量与当前查询无关的闲聊和噪声信息。然而，现有长上下文模型（如 Qwen2.5、GPT-4 等）通常将整个对话历史视为平文本（flat text）直接输入，缺乏对时间维度的显式建模。这种处理方式导致两个核心问题：

1. **时间表达式解析困难**：模型难以从冗长、嘈杂的多会话记录中精确定位和解析“上个月”“三天前”等时间表达，容易将不同时间窗口的事件混淆。
2. **事件顺序混乱**：当多个会话在时间轴上交错分布时，平文本模型缺乏有效机制来辨别事件的先后顺序，导致时间推理性能急剧下降。

### 现有方法的瓶颈

针对上述挑战，学界和业界已提出多种方案，但均存在显著局限：

- **全上下文直接推理**：以 **Qwen2.5-14B**（Team, 2024）、**GPT-4**（Achiam et al., 2023）等通用指令模型为代表，将完整对话历史一次性输入模型。实验表明，当上下文长度超过 64k token 时，此类模型的性能出现严重崩溃（Figure 7），长文本中的噪声信息淹没了关键时间证据。
- **检索增强生成（RAG）**：**RAG**（Lewis et al., 2020）通过文本相似度检索相关片段，但缺乏时间感知能力，检索到的内容可能在时间上与查询无关，导致“答非所问”。
- **记忆增强代理**：**MemAgent**（Yu et al., 2025）引入记忆选择机制，但仅使用答案精度作为稀疏奖励训练，未能发展出有效的时间推理能力，在 Time-Dialog 基准上仅获 49.9% 整体得分。
- **面向时间的强化学习模型**：**Time-R1**（Liu et al., 2025）依赖结构化元数据进行时间推理，但在多会话场景下表现不佳（49.4%），说明仅靠元数据不足以应对复杂的对话时间逻辑。

上述方法的共同缺陷在于：**将对话历史视为平文本，缺乏对时间一致性的显式建模**。这导致代理在冗长、嘈杂的多会话对话中难以精准选择时间上一致的证据会话，时间推理性能遭遇瓶颈。

### 核心洞察与动机

本文的核心洞察是：**粗到细的检索策略与多粒度奖励信号的协同作用，能够为代理提供密集的监督信号，使其学会辨别时间模糊性、抵抗噪声，在长上下文中保持稳健的时间推理能力**。具体而言：

- **粗到细检索**：先通过时间窗口预测进行硬过滤，再通过相关度排序形成候选池，最后由强化学习代理精细选择证据会话。这种级联结构有效压缩了搜索空间，使代理能专注于时间相关的会话片段。
- **多粒度奖励**：在传统答案准确性奖励（$R_a$）之外，引入证据接地奖励（$R_g$）和时间一致性奖励（$R_t$）。其中，$R_t$ 进一步分解为会话级时序接近度（$R_s$）和话语级时序保真度（$R_f$），从粗到细地约束代理选择时间对齐的证据。

消融实验深刻揭示了时间一致性信号的关键作用：移除 $R_s$ 虽使简单定位任务（Category A）提升 23.4%，但导致复杂推理任务（Category B）崩溃 56.2%（Table 2），证明 $R_s$ 对复杂时间推理不可或缺。完全去除 $R_t$ 则对各类任务均造成重大损害，进一步验证了时间一致性奖励的核心价值。

基于上述洞察，本文提出 **Memory-T1**，一个基于强化学习的时间感知记忆选择框架，通过粗到细的级联检索和多层次奖励设计，使代理能够从长对话历史中精准选择时间上一致的证据会话，从而在多会话时间推理任务上实现显著突破。

## 核心创新

Memory-T1 的核心创新并非提出新的模型架构，而是针对多会话时间推理中“长上下文平文本导致事件顺序混乱”这一根本瓶颈，重构了记忆选取的**策略**与**训练信号**。其设计围绕三个紧密耦合的 changed slots 展开：粗到细的级联检索策略、多层次密集奖励函数，以及适配该任务的强化学习算法选择。

### 1. 从全上下文到时间感知的粗到细检索

现有长上下文模型（如 **Qwen2.5-14B** (Team, 2024)、**GPT-4** (Achiam et al., 2023)）将完整对话历史作为平文本输入，缺乏对时间结构的显式利用。Memory-T1 将这一过程重构为两阶段级联（Figure 2）：

- **Phase 1 — 候选生成**：先由 LLM 预测查询的目标时间窗口，据此执行**硬过滤**，丢弃时间戳不在该范围内的会话；再通过 BM25 对剩余会话进行相关度排序，取 Top-k 形成高召回候选池 $\mathcal{C}$。
- **Phase 2 — 精细选择**：RL 代理从候选池中端到端地选择证据会话并生成答案。

这一“时间过滤 → 文本相关度排序 → RL 精细选择”的粗到细流水线，从根本上改变了记忆检索的粒度。消融证据（Figure 3）表明，时间过滤是召回率的关键保障：在 top-k=10 时，证据会话召回率超过 90%，而移除时间过滤后性能显著下降。

### 2. 从稀疏奖励到多层次密集时间一致性奖励

传统记忆代理（如 **MemAgent** (Yu et al., 2025)）仅使用答案准确性 $R_a$ 作为稀疏奖励，导致模型在复杂时间推理上崩溃。Memory-T1 引入了三层密集奖励信号：

$$R = w_a R_a + w_g R_g + w_t R_t$$

其中：

- **$R_a$（答案准确性）**：对完全错误答案施加 -1 惩罚，否则以正确性得分作为奖励。
- **$R_g$（证据接地）**：通过 Jaccard 指数衡量模型引用的会话 ID 与金标准证据集的重叠度，迫使代理精确引用证据。
- **$R_t$（时间一致性）**：这是本工作的核心创新，由两个互补信号组成：
  - **时序接近度 $R_s$**：通过逻辑函数软惩罚所选会话与查询时间范围的距离，容忍微小偏差（margin $m$）。
  - **时序保真度 $R_f$**：在话语级别衡量相关话语内事件与查询时间范围的重叠密度，鼓励选择密集包含时间对齐证据的会话。

消融实验（Table 2）揭示了各奖励成分的因果作用：仅用 $R_a$ 导致整体分数暴跌 22.4%，复杂推理（Category B&C）完全崩溃；移除 $R_g$ 使定位与提取任务（Category A）下降 17.4%；而移除 $R_s$ 虽使简单任务提升 23.4%，却导致复杂推理暴跌 56.2%——这直接证明了时间一致性信号对复杂时间推理的不可替代性。

### 3. 从 PPO 到 GRPO 的策略优化适配

Memory-T1 选择 **GRPO**（Group Relative Policy Optimization）而非更通用的 PPO 作为 RL 算法，这一选择具有明确的因果依据。GRPO 利用批次内平均奖励作为基线来估计优势：

$$\hat{A}((q,C),(S_j,a_j)) = R((q,C),(S_j,a_j)) - \frac{1}{G}\sum_{j=1}^G R((q,C),(S_j,a_j))$$

这种组内相对比较机制天然适配时间推理任务中奖励信号的稀疏性和高方差特性。实验证据（Table 8）直接支撑这一设计选择：在 3B 模型上，GRPO 相较于 PPO 整体提升 18.5%，在复杂类别 B 和 C 上的提升更为显著。这表明，对于需要从长上下文中学习精细时间选择策略的任务，合适的 RL 算法选择本身就是一个关键创新维度。

**创新耦合机制**：上述三个 changed slots 并非孤立改进。粗到细检索为 RL 代理提供了高质量、时间上已预筛选的候选池，降低了动作空间复杂度；多层次奖励（尤其是 $R_t$）为代理提供了密集的监督信号，使其能够辨别时间模糊性；GRPO 则为这一稀疏奖励场景提供了稳定的策略优化。三者协同，使得 3B 规模的 Memory-T1 能够超越 14B 的全上下文基线（66.9 vs. 60.7，Table 1），并在 128k token 的超长上下文中保持甚至提升 F1（Figure 7），而基线模型在此条件下完全崩溃。

## 整体框架

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_vQf2YR2Kpd/figures/002_Figure_2.jpg]]
*Figure 2: An overview of Memory-T1. The framework employs a coarse-to-fine cascade to select time-consistent memories for multi-session temporal reasoning*

Memory‑T1 的设计核心是将多会话时间推理重新表述为一个**记忆检索问题**：给定一个可能跨越数十甚至上百个对话会话的庞大历史，代理需要从中精准定位与用户查询时间上一致的证据，并据此生成正确答案。该框架遵循“粗到细”（coarse‑to‑fine）的级联过滤原则，将整个流程组织为两个主要阶段——**候选生成**与**细粒度选择**——并通过一个多层次的强化学习奖励函数驱动端到端优化（图 2）。

### 问题建模

系统将对话历史建模为一组会话 $\mathcal{S}_i$，每个会话由一系列话语 $u_{ij}$ 及其关联的事件集 $\mathcal{E}_{ij}$ 组成：

$$
\mathcal{S}_i = \{ (u_{i1}, \mathcal{E}_{i1}), (u_{i2}, \mathcal{E}_{i2}), \dots, (u_{iL_i}, \mathcal{E}_{iL_i}) \}
$$

每个事件 $e_k \in \mathcal{E}_{ij}$ 可附带语义描述符 $\kappa_k$ 和时间跨度 $(t_k^{\text{start}}, t_k^{\text{end}})$（图 1）。用户查询 $q$ 同样被标注目标时间范围 $I_Q$。代理的任务是从所有会话中选取一个证据子集 $U \subseteq \{\mathcal{S}_i\}$，并基于 $U$ 生成自然语言答案 $a$。

### 阶段一：候选生成

该阶段的目标是**快速、高召回地压缩搜索空间**，由两个顺序执行的过滤器构成：

1. **时间过滤**：利用大型语言模型预测查询 $q$ 的目标时间窗口，丢弃时间戳完全落在该窗口之外的会话，实现硬剪枝。
2. **相关性过滤**：对时间过滤后的剩余会话，使用 BM25 检索器按文本相似度排序，取前 $k$ 个形成候选池 $\mathcal{C}$：

   $$
   \mathcal{C} = \operatorname{arg top-}k \big( \operatorname{Retriever}(q, S_i) \big)
   $$

实验表明，将 $k$ 设为 10 即可达到约 90% 的证据召回率，而时间过滤器则保证了候选池的高精度（图 3）。

### 阶段二：基于强化学习的细粒度选择

在候选池 $\mathcal{C}$ 之上，一个经强化学习微调的代理负责**最终证据会话选择与答案生成**。代理以查询 $q$ 和候选池 $\mathcal{C}$ 为输入，输出一组选定的会话 ID 及自然语言答案。训练采用 **GRPO**（Group Relative Policy Optimization）算法：

$$
\max_\theta J_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{(q,c)\sim\mathcal{D}, \{(S_j,a_j)\}\sim\pi_{\mathrm{ref}}}\left[\frac{1}{G}\sum_{j=1}^G \min(r_j(\theta)\hat{A}_j, \operatorname{clip}(r_j(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_j)\right] - \beta\mathbb{E}_{(q,c)\sim\mathcal{D}}[D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})]
$$

其中优势估计 $\hat{A}$ 为单次生成奖励与批次内平均奖励之差：

$$
\hat{A}((q,C),(S_j,a_j)) = R((q,C),(S_j,a_j)) - \frac{1}{G}\sum_{j=1}^G R((q,C),(S_j,a_j))
$$

GRPO 利用批次平均作为基线以降低方差，并加入 KL 散度惩罚项防止策略偏离参考模型过远。消融实验证实，GRPO 在 3B 模型上相较 PPO 整体提升 18.5%，在复杂推理类别上优势更为显著（Table 8）。

### 多层次奖励函数

代理的每一步生成都依据一个复合奖励信号进行优化，该信号由三个子奖励加权求和得到（若输出格式解析失败则给予固定惩罚 −0.5）：

$$
R = \begin{cases} w_a R_a + w_g R_g + w_t R_t, & \text{if parsing succeeds}, \\ -0.5, & \text{otherwise} \end{cases}
$$

- **答案准确性 $R_a$**：对完全错误答案惩罚 −1，否则以原始正确性得分作为奖励。
- **证据接地 $R_g$**：通过 Jaccard 指数衡量代理引用的会话 ID 集合与金标准证据集的重叠度，强制代理将推理锚定在真实证据上。
- **时间一致性 $R_t = \alpha R_s + \beta R_f$**：这是 Memory‑T1 的核心创新，从两个粒度约束所选证据的时间合理性：
  - **时序接近度 $R_s$**（会话级）：通过逻辑函数软惩罚所选会话时间戳与查询时间范围的偏差，容忍微小偏移（margin $m$）。
  - **时序保真度 $R_f$**（话语级）：衡量相关话语内事件与查询时间范围的重叠密度，鼓励选择密集包含时间对齐证据的会话。

消融实验揭示了这一奖励结构的关键因果作用：仅用 $R_a$ 训练会导致整体分数暴跌 22.4%，复杂推理（Category B & C）彻底崩溃；移除 $R_g$ 则使定位与提取任务下降 17.4%；而去除 $R_s$ 虽使简单任务提升 23.4%，却导致复杂推理崩溃 56.2%，证明时间一致性信号对深层时间推理不可或缺（Table 2）。

### 输入输出流总结

| 阶段 | 输入 | 处理 | 输出 |
|------|------|------|------|
| 时间过滤 | 全部对话历史 + 查询 $q$ | LLM 预测查询时间窗，硬剪枝 | 时间相关的会话子集 |
| 相关性过滤 | 时间过滤后的会话 | BM25 排序，取 top‑$k$ | 候选池 $\mathcal{C}$ |
| 细粒度选择 | 查询 $q$ + 候选池 $\mathcal{C}$ | RL 代理（GRPO）选择证据会话并生成答案 | 选定会话 ID + 自然语言答案 $a$ |
| 奖励计算 | 代理输出 + 金标准 | 计算 $R_a, R_g, R_t$ 并加权求和 | 标量奖励 $R$ |

该流水线在推理时仅需平均 1.26 秒/查询，与同类方法持平（Table 5），但在长达 128k token 的极端噪声上下文下仍能保持高 F1 甚至实现正向增益，而基线模型性能则完全崩溃（Figure 7），充分验证了粗到细检索与多层次时间奖励协同抗噪的有效性。

## 核心模块与公式推导

Memory-T1 框架围绕一个核心命题展开：**在冗长、嘈杂的多会话对话中，代理必须精准选择时间上一致的证据会话，而非将整个历史视为平文本处理**。为此，框架采用“粗到细”级联架构，将记忆检索分解为两个关键阶段，并通过多层次密集奖励函数驱动强化学习策略优化。

### 3.1 问题形式化

给定一个多会话对话历史，每个会话 $\mathcal{S}_i$ 被定义为一序列话语及其关联的事件集：

$$\mathcal{S}_i = \{ (u_{i1}, \mathcal{E}_{i1}), (u_{i2}, \mathcal{E}_{i2}), \dots, (u_{iL_i}, \mathcal{E}_{iL_i}) \}$$

其中 $u_{ij}$ 为第 $i$ 个会话的第 $j$ 条话语，$\mathcal{E}_{ij}$ 为该话语中涉及的事件集合，每个事件 $e_k$ 可选地标注语义描述符 $\kappa_k$ 和时间跨度 $(t_k^{\text{start}}, t_k^{\text{end}})$。代理的任务是，给定用户查询 $q$，从历史中选取证据会话子集并生成答案 $a$。

### 3.2 粗到细级联检索

框架分为两个阶段，形成从大规模记忆库到精确证据的递进式收缩：

**阶段一：候选生成（Candidate Generation）**。该阶段旨在快速将海量记忆库剪枝为高召回率的可控候选集，包含两步顺序过滤：

1. **时间过滤（Temporal Filtering）**：利用 LLM 预测查询 $q$ 的目标时间窗口 $I_Q = [t_Q^{\text{start}}, t_Q^{\text{end}}]$，丢弃时间戳完全落在该窗口之外的会话。这一步实现了对搜索空间的硬剪枝。
2. **相关度过滤（Relevance Filtering）**：对时间过滤后的会话，通过 BM25 检索器按文本相似度排序，取 top-$k$ 形成候选池 $\mathcal{C}$：

$$\mathcal{C} = \operatorname{arg top-}k \big( \operatorname{Retriever}(q, S_i) \big)$$

**阶段二：基于强化学习的精细选择（Fine-grained Selection via RL）**。在候选池 $\mathcal{C}$ 上，由 RL 微调后的模型以端到端方式完成最终证据会话选择与答案生成。策略优化采用 **GRPO（Group Relative Policy Optimization）**，其目标函数为：

$$\max_\theta J_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{(q,c)\sim\mathcal{D}, \{(S_j,a_j)\}\sim\pi_{\mathrm{ref}}}\left[\frac{1}{G}\sum_{j=1}^G \min(r_j(\theta)\hat{A}_j, \operatorname{clip}(r_j(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_j)\right] - \beta\mathbb{E}_{(q,c)\sim\mathcal{D}}[D_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}})]$$

其中 $r_j(\theta) = \frac{\pi_\theta(a_j|q,\mathcal{C})}{\pi_{\text{ref}}(a_j|q,\mathcal{C})}$ 为概率比，$\hat{A}_j$ 为优势估计。GRPO 的核心优势在于利用批次内平均奖励作为基线来降低方差，避免了训练独立价值网络的开销。单次生成的优势估计为：

$$\hat{A}((q,\mathcal{C}),(S_j,a_j)) = R((q,\mathcal{C}),(S_j,a_j)) - \frac{1}{G}\sum_{j=1}^G R((q,\mathcal{C}),(S_j,a_j))$$

即个体奖励减去批次内 $G$ 次采样的平均奖励。消融实验证实，GRPO 在 3B 模型上相较 PPO 整体提升 **18.5%**，在复杂推理类别上增益更为显著（Table 8）。

### 3.3 多层次奖励函数

奖励设计是驱动代理习得时间感知记忆选择策略的关键因果旋钮。总奖励 $R$ 为三个子奖励的加权和，若输出格式解析失败则给予固定惩罚：

$$R = \begin{cases} w_a R_a + w_g R_g + w_t R_t, & \text{if parsing succeeds}, \\ -0.5, & \text{otherwise} \end{cases}$$

三个子奖励分别对应不同粒度的监督信号：

- **答案准确性奖励 $R_a$**：对完全错误答案（Score = 0）惩罚 $-1$，否则直接以正确性得分作为奖励。该信号确保代理以任务完成为基本目标。
- **证据接地奖励 $R_g$**：通过计算代理引用的会话 ID 集合与金标准证据集 $\mathcal{M}^*$ 之间的 **Jaccard 系数** 量化匹配度，鼓励代理精准定位证据来源。
- **时间一致性奖励 $R_t$**：这是框架区别于同类方法的核心创新，由两个互补成分加权组合：

$$R_t = \alpha R_s + \beta R_f, \quad (\alpha + \beta = 1)$$

其中：

- **时序接近度 $R_s$（会话级）**：通过逻辑函数软惩罚所选会话时间戳与查询时间范围的距离，容忍微小偏差（margin $m$）：

$$R_s = \frac{c}{1+\exp(x)} - d, \quad x = \frac{\operatorname{gap}(U, I_Q) - m}{s}$$

该设计使得代理倾向于选择时间上邻近的会话，但不会因微小偏移而受到过度惩罚。

- **时序保真度 $R_f$（话语级）**：衡量相关话语内事件与查询时间范围的重叠密度，鼓励选择密集包含时间对齐证据的会话：

$$R_f(U, I_Q) = \begin{cases} \frac{1}{|U_{\mathrm{rel}}|}\sum_{u\in U_{\mathrm{rel}}} \left(\frac{1}{|E_u|}\sum_{e\in E_u} r_e(e, I_Q)\right), & |U_{\mathrm{rel}}| > 0, \\ 0, & \text{otherwise} \end{cases}$$

其中 $r_e(e, I_Q)$ 度量单个事件 $e$ 的时间跨度与查询窗口 $I_Q$ 的重叠程度。

**消融实验的因果证据**（Table 2）直接验证了各奖励成分的必要性：仅用 $R_a$ 导致整体分数暴跌 **22.4%**，复杂推理（Category B & C）崩溃；移除 $R_g$ 使定位与提取任务（Category A）下降 **17.4%**；移除 $R_s$ 虽使简单任务提升 23.4%，却导致复杂推理暴跌 **56.2%**——这揭示了时间一致性信号对辨别时间模糊性、抵抗噪声的不可替代作用。

## 实验与分析

### 主要结果

Memory-T1 在 Time-Dialog 基准上建立了新的最优水平。以 3B 参数规模为例，Memory-T1 取得 66.9% 的整体得分，不仅大幅超越同规模指令模型 Qwen2.5-3B，更以显著优势压倒 14B 通用模型 Qwen2.5-14B（60.7%，提升 6.2 个百分点）和闭源模型 GPT-4 Full Prompt（64.8%）。7B 版本进一步将整体得分推至 67.0%，验证了方法的可扩展性。

与同类时间推理或记忆增强方法的对比更突显 Memory-T1 的核心优势：Time-R1 仅获 49.4%，MemAgent 仅获 49.9%，Memory-T1 分别领先 17.5 和 17.0 个百分点。这一差距的根源在于奖励设计——Time-R1 和 MemAgent 仅依赖答案精度作为稀疏奖励，缺乏对证据定位和时间一致性的显式监督，导致代理在多会话噪声中无法有效筛选时间对齐的证据。

从子任务维度看（Table 1），Memory-T1 在 Category A（定位与提取类）和 Category B（显式推理类）上均表现突出，尤其在 Co-temporality 和 Contextual Temporal Filtering 等需要精细时间辨别的任务上显著领先。然而，Comparison 和 Timeline 子任务得分仍接近零，揭示当前框架在深层组合逻辑推理上存在根本性瓶颈。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_vQf2YR2Kpd/figures/003_Table_1.jpg]]
*Table 1: Performance comparison across different models and training strategies on temporal reasoning subtasks. Category A’s metrics include Location (Loc.), Duration Comparison (DC.), Comparison (Comp.), Order Comparison (OC.), and Extraction (Ext.). Category B’s metrics covers ER.=Event Reasoning, OR.=Order Reasoning, RR.=Range Reasoning. Category C’s metrics comprises CTF.=Contextual Temporal Filtering, Co-tmp.=Co-temporality, TL.=Timeline. Bold and underline denote column-wise best and second-best among non-GPT rows. †Oracle setting using gold test evidence*

### 消融实验：奖励函数的分层贡献

Table 2 的消融结果清晰刻画了各奖励成分的功能分工与不可替代性：

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_vQf2YR2Kpd/figures/005_Table_2.jpg]]
*Table 2: Ablation study on the reward function of Memory-T1 (3B). Relative changes compared to the full model are shown in parentheses*

- **仅用任务精度奖励（$R_a$ only）**：整体得分暴跌 22.4%，Category B 和 C 的复杂推理几乎完全崩溃。这直接印证了核心瓶颈——稀疏的答案正确性信号无法引导代理学会从冗长对话中筛选时间一致的证据，代理倾向于依赖表面文本匹配而非时序逻辑。
- **移除证据接地奖励（w/o $R_g$）**：整体下降 9.1%，Category A 受损最重（-17.4%）。$R_g$ 通过 Jaccard 系数强制代理精确引用证据会话，缺失后代理在定位和提取任务上退化为模糊检索。
- **移除时序接近度 $R_s$（w/o $R_s$）**：呈现典型的“任务权衡”现象。Category A 提升 23.4%，但 Category B 暴跌 56.2%。$R_s$ 通过逻辑函数软惩罚所选会话与查询时间窗的距离，容忍微小偏差（margin $m$）。移除后代理在简单定位任务上不再受时间约束限制，检索更自由；但复杂推理任务因缺乏时间结构引导而彻底失效，证明 $R_s$ 对高层时序推理不可或缺。
- **移除时序保真度 $R_f$（w/o $R_f$）**：Category B 下降 14.9%，Category C 下降 8.7%。$R_f$ 在话语级别衡量所选会话内事件与查询时间范围的重叠密度，缺失时代理可能选中时间窗正确但内部事件稀疏的会话，导致证据不足。

完整奖励配置（$w_a=0.6, w_g=0.2, w_t=0.2$）在所有类别上取得最佳平衡，权重敏感度分析（Figure 6）进一步表明该组合在多种上下文长度下均保持稳健。

### 粗到细检索的有效性

Figure 3 验证了级联检索策略的双重价值。时间过滤（Temporal Filtering）是关键瓶颈突破点：在 top-k=10 时，启用时间过滤使证据会话召回率从约 60% 跃升至 90% 以上，同时 F1 提升超过 15 个百分点。若移除时间过滤，即使增大 top-k，基线模型 Qwen2.5-3B 的 F1 仍显著低于 Memory-T1，说明单纯扩大检索池无法替代时间感知剪枝。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_vQf2YR2Kpd/figures/004_Figure_3.jpg]]
*Figure 3: Performance comparison between Memory-T1 (3B) and Qwen2.5-3B (Instruct) under different top-k values (bar charts represent overall F1 scores; line charts represent evidence session recall rate. Comparison conditions: With/without temporal filtering; Top-k refers to the number of sessions retrieved in the candidate generation phase.)*

增大 top-k 至 10 对证据召回至关重要，但继续增大边际收益递减——这反映了粗到细设计的精妙之处：粗阶段用 LLM 预测查询时间窗进行硬过滤，将搜索空间从全对话历史压缩至高召回候选池；细阶段由 RL 代理从候选池中精准选择，避免在全历史上做昂贵的序列决策。

### 长上下文鲁棒性

Figure 4 按输入长度分组（0k–128k tokens）展示了模型的行为分化。Qwen2.5-7B 在 64k–128k 区间 F1 暴跌 35.4 点，呈现典型的长上下文崩溃；而 Memory-T1 7B 在同一区间反而提升 25.0 点。这一反直觉现象源于时间过滤的“去噪”效应——超长对话中包含大量时间无关的会话，基线模型被噪声淹没，而 Memory-T1 的时间窗剪枝将有效上下文压缩至查询相关的时间邻域，噪声比例大幅降低，代理反而能更聚焦地推理。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_vQf2YR2Kpd/figures/008_Figure_4.jpg]]
*Figure 4: Comparison of Qwen2.5 and Memory-T1 models on the test set, where examples are grouped by the length of each test example (tokens) (0k–8k, 8k–16k, 16k–32k, 32k–64k, 64k–128k) to assess performance variation across lengths, along with overall evaluation*

### 域外泛化

在 LoCoMo 基准的零样本评估中（Table 3），Memory-T1 3B 在 Non-RAG 设置下取得 37.7% 的整体准确率，较 Qwen2.5-3B 提升 4.2 个百分点。值得注意的是，在 RAG 设置下 Memory-T1 的优势收窄至 3.2 个百分点，暗示当外部检索器已提供高质量候选时，时间感知选择策略的边际增益减小——这为实际部署中的模块组合提供了参考。

### 延迟与效率

Table 5 显示 Memory-T1 的平均推理延迟为 1.26 秒/查询，与 Time-R1（1.24 秒）和 Qwen2.5-3B（1.36 秒）相当。粗到细检索引入的额外开销（时间窗预测 + BM25 排序）被后续 RL 代理在压缩候选池上的高效决策所抵消，整体延迟在可控范围内。

### 失败模式与局限

1. **组合逻辑崩溃**：Comparison 和 Timeline 子任务得分接近零。这类任务要求代理综合多个会话中的事件进行跨时间段的比较或排序，当前粗到细检索每次仅选择少量证据会话，缺乏多跳组合的机制。
2. **时间噪声敏感**：Table 4 显示，当时间标签注入 10% 噪声时整体得分降至 63.4，20% 噪声时进一步降至 60.0。时间过滤和时序奖励均依赖标注的时间范围，标注质量直接影响性能下限。
3. **奖励权重敏感**：Figure 6 的热力图表明不同权重组合（$W_1$–$W_4$）在子任务间产生显著性能波动，部署时需针对场景调参，增加了工程复杂度。
4. **RL 算法选择**：Table 8 显示 GRPO 在 3B 模型上较 PPO 整体提升 18.5%，但 7B 模型上差距缩小。GRPO 的批次平均基线降低了方差，对小模型稳定训练尤为关键，但该优势随模型容量增大而递减。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_vQf2YR2Kpd/figures/014_Table_8.jpg]]
*Table 8: PPO vs. GRPO: F1 performance on Memory-T1 models of different sizes*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

Memory-T1 的核心定位是**面向多会话对话的时间推理记忆代理**，其方法谱系可从三个维度展开：记忆增强代理、时间推理模型、以及强化学习训练范式。

**通用指令模型与全上下文基线。** 最直接的基线是将整个对话历史作为平文本输入通用指令微调模型。Qwen2.5-3B/7B/14B (Instruct)（Team, 2024）、Gemma-4B-it（Team, 2025）、Llama-3-8B (Instruct)（Dubey et al., 2024）以及 GPT-4（Achiam et al., 2023）均采用此范式。实验表明，即使将模型规模扩大至 14B，Qwen2.5-14B 在 Time-Dialog 上仅取得 60.7% 的整体得分，而 Memory-T1 的 3B 版本即达到 66.9%（+6.2 百分点），7B 版本达到 67.0%（+6.3 百分点）。GPT-4 在全提示模式下得分为 64.8%，即使采用 ReAct 范式（Yao et al., 2023）也仅提升至 65.8%。这一差距的核心原因在于：通用模型将冗长、嘈杂的对话历史视为无结构的平文本，缺乏对时间维度的显式建模，导致事件顺序混乱和信息混淆。

**标准 RAG 基线。** 标准检索增强生成（RAG）（Lewis et al., 2020）通过文本相似度检索相关片段，但不考虑时间约束。在 Time-Dialog 上，RAG 基线的证据会话召回率显著低于 Memory-T1 的粗到细检索策略（Figure 3），因为纯语义检索无法区分“文本相似但时间不匹配”的会话——这正是时间推理中最隐蔽的失败模式。

**记忆增强代理。** MemAgent（Yu et al., 2025）是记忆增强对话代理的代表，但其训练仅使用答案精度奖励（$R_a$ only）。在 Time-Dialog 上，MemAgent 仅取得 49.9% 的整体得分，与 Memory-T1 的 66.9% 相差 17.0 百分点。消融实验（Table 2）揭示了这一差距的因果机制：仅用 $R_a$ 训练导致整体分数下降 22.4%，复杂推理类别（Category B&C）严重崩溃。这表明，稀疏的答案精度信号无法为代理提供足够密集的监督来学习时间感知的记忆选择策略。

**时间推理专用模型。** Time-R1（Liu et al., 2025）是面向时间推理的强化学习模型，但其依赖结构化元数据进行检索和推理。在 Time-Dialog 上，Time-R1 仅取得 49.4%，远低于 Memory-T1 的 66.9%。这一对比凸显了 Memory-T1 设计的关键优势：粗到细检索策略不依赖外部结构化元数据，而是通过 LLM 预测查询时间窗进行硬过滤，再经 BM25 相关度排序形成候选池，使方法更具通用性和可迁移性。

**监督微调基线。** 在 Qwen2.5-3B 上进行监督微调（SFT）（Ouyang et al., 2022）的基线模型表现同样不佳，进一步验证了：对于需要精确定位时间证据的复杂推理任务，标准的行为克隆范式难以捕获时间一致性这一隐式约束。

### 2. 方法适用边界

**任务类型边界。** Memory-T1 在 Time-Dialog 的三类子任务上表现差异显著（Table 1, Table 6）：
- **Category A（定位与提取）**：包括 Location、Duration Comparison、Order Comparison、Extraction 等任务，模型表现较强。这些任务的核心需求是精确定位时间对齐的证据会话，恰好对应粗到细检索和时间一致性奖励的设计目标。
- **Category B（显式推理）**：包括 Event Reasoning、Order Reasoning、Range Reasoning。模型在此类任务上表现中等，需要一定程度的逻辑组合，但仍在时间感知检索的能力范围内。
- **Category C（深层组合推理）**：包括 Contextual Temporal Filtering、Co-temporality、Timeline。其中 Comparison（Comp.）和 Timeline（TL）子任务得分仍接近于零（Section C.5），表明当前代理在处理需要深层组合逻辑的任务上能力有限。这是方法的核心适用边界——粗到细检索和多层次奖励可以有效解决“找到正确时间证据”的问题，但对于“对多个时间证据进行复杂组合推理”的任务，仍需更强大的推理架构。

**上下文长度边界。** 在长达 128k token 的上下文测试中（Figure 4, Figure 7），基线模型 Qwen2.5 性能崩溃（7B 模型 F1 下降 35.4），但 Memory-T1 保持高 F1 甚至提升（+25.0）。这表明粗到细检索策略在超长上下文中具有显著的抗噪能力。然而，这一结论目前仅在 Time-Dialog 和 LoCoMo 两个数据集上验证，对其他多会话场景（如客服、法律对话）的泛化性未经验证。

**域外泛化边界。** 在 LoCoMo 域外评估中（Table 3），Memory-T1（3B）在 Non-RAG 设置下取得 37.7% 的整体准确率，相较 Qwen2.5-3B-Instruct 的 33.5% 提升 4.2 百分点。这一正向迁移表明时间感知记忆策略具有一定的泛化能力，但绝对分数仍然较低，说明域间差异（如对话风格、时间表达方式、事件密度）对模型性能有显著影响。

**训练数据依赖边界。** 训练所需的事件级时间注释依赖人工与大模型标注（Appendix A），可能引入噪声或偏差。Table 4 的鲁棒性实验显示，在 10% 时间标签噪声下整体得分降至 63.4，在 20% 噪声下降至 60.0，但 Co-temporality 和 Relative Reasoning 等子任务仍保持较高 F1（94.4 和 88.9）。这表明模型对适度噪声具有一定容忍度，但高质量时间标注仍是性能保障的前提。

### 3. 局限与开放问题

**深层组合推理的瓶颈。** Comparison 和 Timeline 子任务得分接近零，暴露了当前框架的根本局限：粗到细检索策略擅长定位时间对齐的证据，但缺乏对多证据进行逻辑组合和时序关系推导的能力。如何将 Memory-T1 的检索策略扩展到需要多跳组合推理的任务，是首要的开放问题。

**时间一致性奖励的标注依赖。** 时间一致性奖励（$R_t$）的计算依赖细粒度的事件级时间标注（$R_s$ 需会话时间戳，$R_f$ 需话语级事件时间范围）。一个关键的开放问题是：是否可以在不依赖细粒度事件标注的情况下，通过对比学习或自监督信号近似时间一致性奖励？这直接关系到方法在不同领域的迁移成本。

**时间表达的模糊性处理。** 当前奖励设计假设时间戳是精确且一致的。当对话中的时间表达模糊（如“上个月”“前几天”）或时间戳缺失、不一致时，奖励信号的有效性未经验证。真实对话中大量存在此类情况，如何使代理在时间信息不完美时仍能做出合理推断，是一个重要的开放问题。

**与其他记忆架构的集成。** 当前框架使用 BM25 进行相关性检索，候选池大小受限于 top-k 参数。该框架能否与向量数据库、结构化知识图谱等记忆架构结合，以支持十万级甚至更长的对话历史？不同检索架构对时间过滤和 RL 代理选择策略的影响尚待探索。

**在线适应能力。** Memory-T1 目前以离线方式训练和评估。在真实流式对话场景下，新会话不断加入，查询的时间范围动态变化。模型如何进行在线适应，在不需要完全重新训练的情况下持续优化记忆选择策略，是一个具有实际价值的开放问题。

**RL 训练的工程复杂度。** 奖励权重的敏感度分析（Figure 6）显示，不同权重组合 $(w_a, w_g, w_t)$ 对性能有显著影响，部署时需要仔细调参。GRPO 相较于 PPO 在 3B 模型上整体提升 18.5%（Table 8），但这一优势是否在不同任务和规模上持续稳定，仍需更多验证。RL 训练对超参数的敏感性增加了工程部署的复杂度，如何设计更鲁棒的训练策略是实用的开放问题。

**多模态扩展。** 当前框架仅处理文本对话。更复杂的现实世界多会话场景可能涉及图像、表格等多模态信息，时间推理的维度将更加复杂。Memory-T1 的粗到细检索和多层次奖励范式能否扩展到多模态场景，是一个前瞻性的开放问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Memory_T1_Reinforcement_Learning_for_Temporal_Reasoning_in_Multi_session_Agents.pdf]]
