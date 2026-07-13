---
title: "Look Back to Reason Forward: Revisitable Memory for Long-Context LLM Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Look_Back_to_Reason_Forward_Revisitable_Memory_for_Long_Context_LLM_Agents.pdf
project_link: null
code_link: https://github.com/syr-cn/ReMemR1
openreview_forum_id: 1cymflI2Lh
aliases:
- LBRFRMLCLA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "在记忆更新过程中引入可检索历史记忆的回调查询机制，使智能体能非线性回溯；同时设计多级奖励（最终结果奖励与步骤级信息增益奖励）提供密集监督。"
primary_logic: "将显式记忆检索集成到记忆更新流程中，打破了不可逆的前向约束，使智能体能按需回顾并整合早期证据，从而缓解信息退化并提升复杂多跳推理能力。"
claims:
- "ReMemR1 consistently achieves the best accuracy across both HotpotQA and 2WikiMultiHopQA at all context lengths and model scales (Table 1)."
- "ReMemR1 significantly outperforms MemAgent under a constructed distant-evidence setup, demonstrating effective non-linear reasoning (Figure 5)."
- "The callback mechanism introduces less than 2 seconds latency and under 1MB memory overhead, while improving accuracy by up to 5% (Figure 6, Table 7)."
- "Multi-level reward with α = 0.8 yields the best accuracy across different context lengths (Table 3)."
---

# Look Back to Reason Forward: Revisitable Memory for Long-Context LLM Agents

> [!tip] 核心洞察
> 将显式记忆检索集成到记忆更新流程中，打破了不可逆的前向约束，使智能体能按需回顾并整合早期证据，从而缓解信息退化并提升复杂多跳推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 回顾以推理：长上下文LLM智能体的可回溯记忆 |
| 英文题名 | Look Back to Reason Forward: Revisitable Memory for Long-Context LLM Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=1cymflI2Lh) · [GitHub](https://github.com/syr-cn/ReMemR1) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | ReMemR1 |
| Dataset | HotpotQA (ID) 7B 50 docs, HotpotQA (ID) 7B 100 docs, HotpotQA (ID) 7B 6400 docs, 2WikiMultiHopQA (OOD) 7B 50 docs |

> [!tip] 效果简介
> - HotpotQA (ID) 7B 50 docs 上，Accuracy (%) 为 82.3，对比 81.8 (MemAgent)，变化 +0.5。
> - HotpotQA (ID) 7B 100 docs 上，Accuracy (%) 为 82.8，对比 78.9 (MemAgent)，变化 +3.9。
> - HotpotQA (ID) 7B 6400 docs 上，Accuracy (%) 为 80.8，对比 75.8 (MemAgent)，变化 +5.0。

## 概要

### 核心问题：长上下文推理中的线性记忆退化

大语言模型（LLM）智能体在处理长文档多跳问答时，主流范式是“边读边记”（memorize-while-reading）：模型顺序阅读文档块，逐步将信息压缩进一个固定大小的记忆状态。这一前向线性更新机制存在根本性瓶颈——早期关键证据一旦在记忆压缩中被剪枝或覆盖，便永久丢失，后续步骤无法回溯。同时，仅依赖最终答案正确性的稀疏奖励信号，难以有效优化长序列中的中间决策。

### 核心方案：可回溯记忆与多级奖励

ReMemR1 从两个维度打破上述约束：

1. **可回溯记忆更新**：将显式记忆检索集成到记忆更新流程中。在每个时间步，智能体不仅更新当前记忆 $m_t$，还生成一个回调查询 $q_t$，用于从历史记忆 $\{m_i\}_{i \le t}$ 中检索相关内容。状态从 $s_t = m_t$ 扩展为 $s_t = (m_t, q_t)$，使智能体能非线性地回顾并整合早期证据，缓解信息退化。

2. **多级奖励监督**：训练目标同时包含轨迹级结果奖励（最终答案精确匹配）和步骤级状态奖励（记忆信息增益、回调检索增益、格式奖励），以加权组合优势函数 $\hat{A}_t = \alpha \hat{A}_{\text{out}} + (1-\alpha)\hat{A}_{\text{state},t}$ 进行 GRPO 优化，提供密集的中间监督信号。

### 方法定位

ReMemR1 属于 **记忆增强型 LLM 智能体**，直接对标 **MemAgent**（Yu et al., 2025a）这一“边读边记”基线。与全文检索方案（存储开销大）和纯推理模型（如 **R1-Distill-Qwen**，DeepSeek-AI et al., 2025）不同，ReMemR1 在保持 $O(T)$ 时空复杂度的前提下，通过回调机制赋予记忆更新非线性回溯能力。

### 主要实验结果

- **分布内（HotpotQA）**：7B 模型在 6400 文档设置下，ReMemR1 准确率达 80.8%，较 MemAgent（75.8%）提升 5.0 个百分点；上下文越长，增益越显著（Table 1a）。
- **分布外（2WikiMultiHopQA）**：同等设置下准确率 50.3% vs 44.7%，提升 5.6 个百分点（Table 1b）。
- **远程证据设置**：在需要跨长距离整合证据的场景中，ReMemR1 显著优于 MemAgent，验证了非线性推理能力（Figure 5）。
- **计算开销可控**：回调机制引入的延迟低于 2 秒，内存开销低于 1MB，检索模块占总延迟不足 0.2%（Figure 6, Table 7）。
- **多级奖励有效性**：$\alpha = 0.8$ 在各上下文长度下取得最佳准确率（Table 3）；RL 训练使 MemAgent 和 ReMemR1 均显著优于无 RL 版本（Table 6）。

### 局限与开放问题

当前方法存在回调查询退化（生成不相关查询）、记忆污染（早期幻觉难以纠正）、训练资源需求高（3B 模型需 16 H800 GPU 训练 100 小时）等问题，且仅在两个多跳问答数据集上验证。未来方向包括：改进回调查询策略、设计记忆修正机制、自适应调整 $\alpha$、扩展到非问答类长上下文任务，以及探索可微检索函数替代词重叠召回。

### 长上下文推理中的记忆瓶颈

大语言模型（LLM）在处理长文档导航与多跳推理任务时，面临信息容量与推理深度的双重挑战。为应对这一挑战，**记忆增强智能体**（memory-augmented agent）被广泛采用，其核心思路是在逐块读取文档的过程中动态维护一个内部记忆状态，将长上下文压缩为紧凑的记忆表示，从而突破模型原生的上下文窗口限制。

然而，当前主流的**“边读边记”范式**（memorize-while-reading）存在一个根本性缺陷：记忆更新过程是**前向线性的**。具体而言，在每一步 $t$，智能体仅基于当前文档块 $c_t$ 和上一时刻的记忆 $m_t$ 生成新记忆 $m_{t+1}$，即 $m_{t+1} = \pi_\theta(Q, c_t, m_t)$。这种单向依赖关系导致两个严重后果：

1. **关键证据的过早剪枝与覆盖**：早期读取的关键信息若未即时写入记忆，或写入后在后续步骤中被覆盖，将永久丢失，无法在后续推理中回溯利用。
2. **稀疏奖励信号下的优化困难**：仅依靠最终答案正确性的二元奖励来优化整个长序列的中间步骤，梯度信号极度稀疏，模型难以习得有效的记忆管理策略。

这些瓶颈在多跳问答场景中尤为突出——当回答一个问题需要整合分布在文档不同位置的多条证据时，线性记忆机制极易在证据链尚未完整时丢弃关键环节。

### 现有方法及其局限

现有长上下文处理方法可归为两类范式，各有其固有局限：

- **全文检索范式**（Full-Text Retrieval）：将检索与推理分离，先检索相关文档再送入LLM推理。该方法需存储完整文档，存储开销巨大，且检索与推理的割裂导致端到端优化困难。
- **边读边记范式**（Memorize-while-Reading）：以 **MemAgent**（Yu et al., 2025a）为代表，在读取过程中动态更新记忆。该方法虽降低了存储负担，但如前述，其不可逆的前向更新机制导致信息退化，在长上下文和复杂推理任务中性能显著下降。

更一般的长上下文LLM，如 **Qwen2.5-1M**（Yang et al., 2025b），通过扩展上下文窗口直接处理长输入，但计算成本随上下文长度急剧增长，且缺乏显式的记忆管理机制。推理模型如 **R1-Distill-Qwen**（DeepSeek-AI et al., 2025）虽增强了推理能力，但并未解决长上下文中的记忆检索与整合问题。

### 核心洞察：打破不可逆的前向约束

本文的核心洞察在于：**将显式记忆检索集成到记忆更新流程中，打破不可逆的前向约束，使智能体能按需回顾并整合早期证据**。这一设计的关键在于：

- 在状态表示中引入**回调查询** $q_t$，将状态从 $s_t = m_t$ 扩展为 $s_t = (m_t, q_t)$；
- 在记忆更新时，利用回调查询从历史记忆 $\{m_i\}_{i \leq t}$ 中检索相关内容，使新记忆的生成能够整合当前上下文、上一时刻记忆以及**检索到的历史证据**；
- 通过**多级奖励设计**——结合轨迹级结果奖励与步骤级信息增益奖励——为记忆管理决策提供密集监督信号。

这一机制本质上赋予了智能体**非线性记忆访问**能力：它不再受限于“读过即忘”的线性路径，而是可以在任意时刻回溯到历史记忆中的关键信息，从而缓解信息退化并提升复杂多跳推理的可靠性。

## 核心方法与创新机理

ReMemR1 的核心创新在于打破了传统“边读边记”记忆智能体的前向线性约束，通过**状态空间扩展**、**可回溯记忆更新**和**多级密集奖励**三个维度的改变，使智能体能够按需回顾并整合早期证据。

### 状态空间扩展：从单一记忆到记忆-查询对

传统记忆智能体（如 **MemAgent**，Yu et al., 2025a）将状态简化为当前记忆 $s_t = m_t$，下一步记忆 $m_{t+1}$ 仅依赖于当前上下文 $c_t$ 和上一时刻记忆 $m_t$（Figure 3 左）。这种设计隐含了一个不可逆的假设：信息一旦被覆盖就无法再访问。

ReMemR1 将状态扩展为 $s_t = (m_t, q_t)$，其中 $q_t$ 是一个**回调查询**（callback query），用于在记忆历史中检索相关信息（Figure 3 右）。这一扩展赋予了智能体“主动回顾”的能力，从根本上改变了状态转移的信息来源。

### 记忆更新中的非线性回溯机制

基于扩展的状态空间，ReMemR1 的记忆更新函数发生了质变。传统方法中 $m_{t+1}$ 仅由策略 $\pi_\theta(Q, c_t, m_t)$ 生成；而 ReMemR1 的增强状态转移方程为：

$$s_{t+1} = (m_{t+1}, q_{t+1}) = \pi_{\theta}\bigl(Q, c_t, m_t, \mathcal{E}(\{m_i\}_{i \leqslant t}, q_t)\bigr)$$

其中 $\mathcal{E}$ 是基于词重叠召回（word-overlap recall）的检索函数，根据当前回调查询 $q_t$ 从历史记忆 $\{m_i\}_{i \leqslant t}$ 中选取最相关的内容（§2.2, Eq. 3）。这意味着每一步的记忆更新不仅依赖于当前文档块和上一时刻记忆，还能**显式地检索并整合历史中的关键证据**，从而打破了前向线性更新的不可逆约束。

这一设计的因果机制在于：当多跳推理所需的证据在文档流中被远距离分隔时，传统方法因中间步骤的剪枝和覆盖而丢失早期关键信息；回调查询机制使智能体能在后续步骤中主动“回顾”这些被覆盖的证据，实现非线性推理路径。

### 多级奖励：从稀疏结果监督到密集步骤信号

传统方法仅依赖最终答案的二元正确性奖励 $R_{\mathrm{out}}^{(g)}$（Eq. 4），这种稀疏监督难以有效优化长序列中的中间步骤。ReMemR1 引入了**多级奖励结构**（Figure 4），将监督信号分解为：

- **轨迹级结果奖励**：与基线一致，基于预测答案与标准答案的精确匹配。
- **步骤级状态奖励** $R_{\mathrm{state},t}^{(g)} = r_{\mathrm{memory},t}^{(g)} + r_{\mathrm{callback},t}^{(g)} + r_{\mathrm{format},t}^{(g)}$（Eq. 7），包含三个组件：
  - **记忆信息增益奖励** $r_{\mathrm{memory},t}^{(g)}$：衡量记忆更新后对真实答案实体召回率的增量（Eq. 5），直接评估记忆更新的信息价值。
  - **回调检索奖励** $r_{\mathrm{callback},t}^{(g)}$：衡量检索到的历史内容为当前上下文带来的额外信息增益（Eq. 6），鼓励生成有效的回调查询。
  - **格式奖励** $r_{\mathrm{format},t}^{(g)}$：检查 `<callback>`、`<memory>` 和 `\box{}` 标签的正确使用。

最终的优势函数将两个层级加权组合：$\hat{A}_{t}^{(g)} = \alpha \hat{A}_{\mathrm{out}}^{(g)} + (1 - \alpha) \hat{A}_{\mathrm{state},t}^{(g)}$（Eq. 9），其中 $\alpha$ 控制结果奖励与步骤奖励的平衡。消融实验表明 $\alpha = 0.8$ 在不同上下文长度下均取得最佳准确率（Table 3），验证了密集步骤信号对长序列优化的关键作用。

### 关键证据强度

上述三个 changed slots 的有效性由以下决定性证据支撑：

| 创新维度 | 核心证据 | 置信度 |
|---------|---------|--------|
| 状态扩展 + 回溯更新 | ReMemR1 在所有上下文长度和模型规模上一致优于 MemAgent，在 6400 文档设置下准确率提升达 5.0–5.6 个百分点（Table 1） | 0.98 |
| 非线性推理能力 | 在远程证据设置下，ReMemR1 显著优于 MemAgent，验证了回溯机制对远距离证据整合的有效性（Figure 5） | 0.95 |
| 多级奖励 | $\alpha = 0.8$ 取得最佳准确率，且 RL 训练使 MemAgent 和 ReMemR1 均显著优于非 RL 版本（Table 3, Table 6） | 0.95 |
| 计算效率 | 回调查询引入的延迟小于 2 秒、内存开销低于 1MB，占总开销的 <0.2%（Figure 6, Table 7） | 0.95 |

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_1cymflI2Lh/figures/002_Figure_2.jpg]]
*Figure 2: Framework of ReMemR1. (a) Memory Update with Callback: At each time step, the agent updates the current memory m _ { t } and generates a callback query q _ { t } to retrieve relevant history memories. The state update integrates the previous memory m _ { t - 1 } , , the current chunk, and the retrieved history. (b) Final Answer Generation: The final answer is synthesized using the latest memory state and a final query over the accumulated memory history*

ReMemR1 的整体 pipeline 围绕“带历史回调查询的记忆更新”这一核心机制展开。如图 2 所示，系统由四个主要模块串联构成：**文档分块流式输入**、**带回调的记忆更新**、**历史检索**和**最终答案生成**。与传统的“边读边记”范式（MemAgent，Yu et al., 2025a）不同，ReMemR1 将显式的历史检索嵌入到记忆更新的每一步，使智能体能够非线性地回溯并整合早期证据，从而缓解信息退化。

### 输入输出流

系统接收一个长上下文文档集合和一个自然语言问题 $Q$。文档被预处理为固定大小的分块序列 $\{c_0, c_1, \ldots, c_{T-1}\}$，按顺序流式输入。每一步 $t$ 的输入包括：当前文档分块 $c_t$、上一步的记忆 $m_t$ 和回调查询 $q_t$（初始 $m_0$ 和 $q_0$ 为空）。模块输出为更新后的记忆 $m_{t+1}$ 和新回调查询 $q_{t+1}$。遍历完所有文档后，系统基于最终记忆 $m_T$ 和全历史记忆的最终查询生成答案。

### 模块关系与数据流

1. **文档分块流式输入**：将长文档按固定粒度切分为 $T$ 个分块，依次作为环境输入提供给记忆更新模块。这一设计使系统能处理远超上下文窗口的文档量，同时保持计算开销可控。

2. **带回调的记忆更新**（核心模块）：在每个时间步 $t$，智能体基于问题 $Q$、当前分块 $c_t$、当前记忆 $m_t$ 以及**从历史记忆中检索到的内容**，生成新的记忆 $m_{t+1}$ 和回调查询 $q_{t+1}$。其状态转移方程为：
   $$s_{t+1} = (m_{t+1}, q_{t+1}) = \pi_{\theta}\bigl(Q, c_t, m_t, \mathcal{E}(\{m_i\}_{i \leqslant t}, q_t)\bigr)$$
   其中 $\mathcal{E}$ 为历史检索函数，$q_t$ 是上一步生成的回调查询。这一步是 ReMemR1 与传统方法的关键分水岭：传统方法的状态仅包含 $m_t$，且 $m_{t+1}$ 仅依赖 $c_t$ 和 $m_t$（图 3 左），形成不可逆的前向约束；ReMemR1 通过引入回调查询 $q_t$ 和检索历史 $\mathcal{E}(\{m_i\}_{i \leqslant t}, q_t)$，打破了这一约束（图 3 右），使智能体能在任意时刻回溯并利用早期写入的关键证据。

3. **历史检索**：检索函数 $\mathcal{E}$ 采用基于词重叠的召回策略，从所有历史记忆 $\{m_i\}_{i \leqslant t}$ 中选取与回调查询 $q_t$ 词重叠度最高的记忆片段。具体地，$\mathcal{E}(X, b) = \arg\max_{x \in X} \text{recall}(b, x)$，其中 $\text{recall}(a, b)$ 衡量 $a$ 中的词在 $b$ 中出现的比例。该模块的计算开销极小（<0.2% 总延迟，<0.001% 内存），但为记忆更新提供了关键的非线性信息通道。

4. **最终答案生成**：遍历完所有 $T$ 个文档分块后，系统基于最终记忆状态 $m_T$ 和问题 $Q$，并通过一次针对全历史记忆的最终查询，合成最终答案 $\hat{y}$。这一阶段与训练时使用的轨迹级结果奖励 $R_{\text{out}}$ 直接关联。

### 训练流程

ReMemR1 的训练采用基于 GRPO 变体的强化学习框架，其奖励设计包含两个层次（图 4）：
- **轨迹级结果奖励**：在轨迹结束时，根据预测答案与标准答案的精确匹配给出二元奖励 $R_{\text{out}}^{(g)} = \max_{y \in Y} \mathbb{I}(\hat{y}^{(g)} = y)$。
- **步骤级状态奖励**：在每个中间步骤 $t$，计算记忆信息增益奖励 $r_{\text{memory},t}$、回调检索奖励 $r_{\text{callback},t}$ 和格式奖励 $r_{\text{format},t}$ 之和 $R_{\text{state},t}$。

两种奖励通过超参数 $\alpha$ 加权组合为综合优势函数 $\hat{A}_{t}^{(g)} = \alpha \hat{A}_{\text{out}}^{(g)} + (1 - \alpha) \hat{A}_{\text{state},t}^{(g)}$，用于策略优化。这种多级奖励设计为长序列中间步骤提供了密集监督，有效缓解了仅依赖最终答案的稀疏奖励问题（消融实验证实 $\alpha = 0.8$ 时性能最优，Table 3）。

### 训练动态

引入回调查询机制后，模型需要额外学习输出 `<callback>` 和 `<memory>` 标签的格式规范。如图 7 所示，训练初期格式奖励较低（约 0.55），但模型在约 20 步内迅速学会遵循格式要求，格式奖励快速收敛至接近 1.0 并保持稳定，表明格式约束不会构成长期训练障碍。

### 1. 文档流式编码与基础状态转移

智能体顺序接收文档块 $c_t$，在时间步 $t \in [0, T-1]$ 维护内部记忆状态。传统“边读边记”范式将状态简化为 $s_t = m_t$，状态转移由策略 $\pi_\theta$ 根据当前问题 $Q$、当前块 $c_t$ 和上一步记忆 $m_t$ 生成下一步记忆：

$$s_{t+1} = m_{t+1} = \pi_{\theta}(Q, c_t, m_t)$$

最终答案生成阶段，策略以问题 $Q$ 和最终记忆 $m_T$ 为输入（无文档块）输出答案：

$$s_{T+1} = o = \pi_{\theta}(Q, \emptyset, m_T)$$

该线性转移的瓶颈在于：记忆更新仅依赖当前上下文和上一时刻记忆，早期关键证据一旦被覆盖则不可恢复。

### 2. 增强状态与回调查询机制

ReMemR1 将状态扩展为 $s_t = (m_t, q_t)$，其中 $q_t$ 为回调查询。在每个时间步，智能体不仅生成新记忆 $m_{t+1}$，还生成查询 $q_{t+1}$ 用于检索历史记忆。增强状态转移方程为：

$$s_{t+1} = (m_{t+1}, q_{t+1}) = \pi_{\theta}\bigl(Q, c_t, m_t, \mathcal{E}(\{m_i\}_{i \leqslant t}, q_t)\bigr)$$

检索函数 $\mathcal{E}$ 基于词重叠召回率选择与查询最相关的历史内容：

$$\mathcal{E}(X, b) = \arg\max_{x \in X} \mathrm{recall}(b, x)$$

其中 $\mathrm{recall}(a, b)$ 表示 $a$ 中出现在 $b$ 中的词的比例。该机制使智能体能够非线性回溯早期证据，打破前向记忆更新的不可逆约束。

### 3. 多级奖励设计

#### 3.1 轨迹级结果奖励

在轨迹 $g$ 的终止状态，根据预测答案 $\hat{y}^{(g)}$ 与真实答案集 $Y$ 的精确匹配给予二元奖励：

$$R_{\mathrm{out}}^{(g)} = \max_{y \in Y} \mathbb{I}(\hat{y}^{(g)} = y)$$

#### 3.2 步骤级状态奖励

步骤级奖励由三部分组成，提供密集监督：

**记忆信息增益奖励**：衡量记忆更新后对真实答案实体的召回率增量：

$$r_{\mathrm{memory},t}^{(g)} = \max_{y \in Y} \mathrm{recall}(m_t^{(g)}, y) - \max_{y \in Y} \mathrm{recall}(m_{t-1}^{(g)}, y)$$

**回调检索奖励**：衡量检索到的历史内容为当前上下文带来的额外信息增益：

$$r_{\mathrm{callback},t}^{(g)} = \max_{y \in Y} \mathrm{recall}\bigl(y, \mathcal{E}(\{m_i^{(g)}\}_{i \leq t}, q_t^{(g)}) \cup m_t^{(g)} \cup c_t\bigr) - \max_{y \in Y} \mathrm{recall}(y, m_t^{(g)} \cup c_t)$$

**格式奖励** $r_{\mathrm{format},t}^{(g)}$：检查中间状态是否正确使用 `<callback>` 和 `<memory>` 标签，终止步是否包含 `\box{}` 标签。

总步骤级状态奖励为三者之和：

$$R_{\mathrm{state},t}^{(g)} = r_{\mathrm{memory},t}^{(g)} + r_{\mathrm{callback},t}^{(g)} + r_{\mathrm{format},t}^{(g)}$$

#### 3.3 组合优势与优化目标

轨迹级结果优势与步骤级状态优势分别通过组内归一化计算：

$$\hat{A}_{\mathrm{out}}^{(g)} = R_{\mathrm{out}}^{(g)} - \frac{1}{G} \sum_{k=1}^{G} R_{\mathrm{out}}^{(k)}$$

$$\hat{A}_{\mathrm{state},t}^{(g)} = R_{\mathrm{state},t}^{(g)} - \frac{1}{G} \sum_{k=1}^{G} R_{\mathrm{state},t}^{(k)}$$

两者通过超参数 $\alpha$ 加权组合，形成最终优势估计：

$$\hat{A}_{t}^{(g)} = \alpha \hat{A}_{\mathrm{out}}^{(g)} + (1 - \alpha) \hat{A}_{\mathrm{state},t}^{(g)}$$

该组合优势用于 GRPO 变体算法进行策略优化。消融实验（Table 3）表明 $\alpha = 0.8$ 在不同上下文长度下均取得最佳准确率，验证了步骤级密集监督与轨迹级稀疏奖励协同作用的有效性。

## 实验与关键发现

### 主实验结果

ReMemR1在HotpotQA（分布内）和2WikiMultiHopQA（分布外）两个多跳问答基准上，系统性地超越了所有基线方法，且优势随上下文长度增加而扩大。核心发现如下：

**HotpotQA（Table 1a）**：7B规模的ReMemR1在50篇文档设置下达到82.3%准确率，略高于MemAgent的81.8%；当文档数扩展至6400篇时，ReMemR1仍保持80.8%，而MemAgent已退化至75.8%，差距拉大至+5.0%。3B规模下趋势一致，6400篇文档时ReMemR1领先MemAgent达+7.3%。这表明回调查询机制有效缓解了长序列中的信息退化问题。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_1cymflI2Lh/figures/005_Table_1.jpg]]
*Table 1: Long-context QA results on HotpotQA (Yang et al., 2018) and 2WikiMultiHopQA (Ho et al., 2020). Values are accuracy (%), rounded to 1 decimal. Bold denotes the best performances. (a) Accuracy on HotpotQA (In-Distribution)*

**2WikiMultiHopQA（Table 1b）**：作为分布外测试，该数据集要求更强的跨文档推理能力。7B规模的ReMemR1在50篇文档下达到63.9%（vs MemAgent 61.7%），6400篇文档下为50.3%（vs MemAgent 44.7%），差距为+5.6%。3B规模下，6400篇文档时ReMemR1领先幅度达+7.6%。值得注意的是，ReMemR1在分布外场景中同样展现出稳健的泛化能力。

**跨模型规模一致性**：无论是基于Qwen2.5-3B还是Qwen2.5-7B，ReMemR1在所有上下文长度下均取得最优准确率，验证了方法的模型规模无关性。

### 非线性推理能力验证

为直接验证ReMemR1是否真正实现了非线性文档利用，作者构造了“远程证据”设置（Figure 5）：将回答问题所需的两篇关键文档分别放置在文档序列的首尾两端，中间填充大量无关文档。在此设置下，传统前向记忆智能体因早期证据被后续更新覆盖而难以回溯，而ReMemR1通过回调查询可显式检索早期记忆。

结果表明，ReMemR1在2WikiMultiHopQA上显著超越MemAgent，差距远超常规设置下的表现。这直接证明了回调查询机制赋予了智能体非线性回溯早期证据的能力，而非仅依赖最近上下文进行推理。

### 计算效率分析

ReMemR1在引入回调查询的同时保持了可接受的计算开销（Figure 6, Table 7）：

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_1cymflI2Lh/figures/009_Figure_6.jpg]]
*Figure 6: Computational performance under different context lengths. (a) Comparison of accuracy and total memory usage between ReMemR1 and MemAgent. (b) Time and memory overhead introduced by the retrieval module. ReMemR1 consistently achieves higher accuracy with only modest additional computation (\< 2s latency and \< 1MB memory)*

- **推理延迟**：检索模块引入的额外延迟不足2秒，占总推理时间的比例低于0.2%。
- **内存开销**：检索模块的内存占用低于1MB，占总内存使用量的比例低于0.001%。
- **准确率-效率权衡**：在6400篇文档的设置下，ReMemR1以不到2秒的额外延迟和不到1MB的额外内存，换取了5%的准确率提升。

训练阶段（Table 2），ReMemR1每步平均耗时1467.72秒，略高于MemAgent的1247.17秒；峰值内存131.15 GB vs 124.97 GB。这一开销主要来自回调查询的生成与检索操作，但仍在可接受的训练预算范围内。

### 多级奖励消融

**奖励权重α的影响（Table 3）**：α控制轨迹级结果奖励与步骤级状态奖励的平衡（α=1.0表示仅用结果奖励）。实验表明α=0.8在HotpotQA各上下文长度下一致取得最优准确率。α过小（0.2）或过大（1.0）均导致性能下降，说明适度的步骤级密集监督对长序列推理至关重要，但过度依赖中间信号也会损害最终目标的对齐。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_1cymflI2Lh/figures/011_Table_3.jpg]]
*Table 3: Accuracy on HotpotQA with different α values*

**RL训练的作用（Table 6）**：以Qwen2.5-3B为基础模型，对比有/无RL训练下的性能。结果显示，多级奖励驱动的RL训练对MemAgent和ReMemR1均有显著提升，且ReMemR1的增益更为突出。这表明多级奖励不仅提供了密集监督，还与回调查询机制形成协同效应——步骤级奖励信号有效指导了何时以及如何发起回调查询。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_1cymflI2Lh/figures/015_Table_6.jpg]]
*Table 6: Ablation on RL training. We report accuracy (%) on HotpotQA and 2WikiMultiHopQA with and without RL. The based models are Qwen2.5-3B Instruct*

**回调策略对比（Table 4）**：对比三种回调实现：（1）无回调（即MemAgent）、（2）基于规则的启发式回调、（3）RL驱动的自适应回调（ReMemR1）。RL驱动回调在所有上下文长度和数据集上均取得最优准确率，而规则式回调虽优于无回调，但与RL驱动方案存在明显差距。这验证了让模型自主学习“何时检索、检索什么”的策略优于固定规则。

![[assets/figures/papers/paper_list_l38_https_openreview_net_forum_id_1cymflI2Lh/figures/012_Table_4.jpg]]
*Table 4: Comparison of accuracy (%) on HotpotQA and 2WikiMultiHopQA across different callback implementations. Bold denotes the best performance*

### 训练动态

Figure 7展示了格式奖励随训练步数的变化。由于ReMemR1要求模型同时生成内部记忆和回调查询，引入了额外的格式约束（如`<callback>`和`<memory>`标签），训练初期解析错误频繁，格式奖励较低。但在约20步内，格式奖励迅速攀升至接近1.0并保持稳定，表明模型能快速适应结构化输出要求。Figure 8展示了不同α值下结果奖励的训练曲线，进一步验证了α=0.8在收敛速度和最终性能上的优势。

### 失败模式与局限性

尽管ReMemR1整体表现优异，分析揭示了以下主要失败模式：

1. **回调查询退化**：当模型无法在记忆中定位相关信息时，回调查询会坍塌为不相关的通用查询（例如反复询问“美国总统是谁”），导致检索结果无助于当前推理步骤。这种“召回退化”现象在信息稀疏的长序列中尤为突出。
2. **记忆污染**：模型在早期步骤中生成的错误信息（幻觉）会被写入记忆，并在后续步骤中通过回调查询被反复检索和强化，形成错误传播链。当前框架缺乏显式的记忆纠错机制，难以在发现矛盾时修正早期记忆。
3. **任务覆盖范围有限**：评估仅局限于HotpotQA和2WikiMultiHopQA两个多跳问答数据集，未涉及长文档摘要、多文档翻译等其他类型的长上下文任务，方法的通用性有待进一步验证。
4. **训练成本较高**：3B模型需16块H800 GPU训练约100小时，7B模型需32块H800训练约80小时，对资源受限的研究场景不够友好。

## 定位与知识库关联

### 1. 与前人工作的关系

ReMemR1 的直接前身是 **MemAgent**（Yu et al., 2025a），后者遵循“边读边记”（memorize-while-reading）范式：智能体顺序读取文档块，在每个时间步将当前上下文与上一时刻的记忆融合，生成新的记忆状态。这一范式继承了记忆增强推理的基本框架，但其状态转移是严格前向的——记忆一旦被覆盖便不可回溯，导致早期关键证据在长序列中因剪枝和信息覆盖而永久丢失。

本文的核心突破在于打破了这一不可逆约束。ReMemR1 将状态从单纯记忆 $s_t = m_t$ 扩展为 $(m_t, q_t)$，其中 $q_t$ 是智能体自主生成的**回调查询**，用于从完整记忆历史中检索相关内容。这一设计将显式记忆检索集成到记忆更新流程内部，使智能体能够非线性地回溯早期证据，从而缓解了“边读边记”范式的根本瓶颈——信息退化和关键证据遗漏。

从更广的谱系看，ReMemR1 位于三种记忆范式的交叉点上：
- **全文检索范式**：将检索与推理分离，存储所有原始文档，但存储负担重且检索与推理的割裂限制了端到端优化。
- **“边读边记”范式**：通过在线记忆压缩降低存储，但线性覆盖导致信息丢失。
- **本文范式**：在保持轻量存储的同时，通过回调机制赋予智能体非线性的记忆访问能力，兼顾了存储效率与信息保真度。

在训练策略上，ReMemR1 将 GRPO（Shao et al., 2024）算法适配到记忆增强智能体中，并设计了多级奖励：轨迹级结果奖励提供最终答案的稀疏监督，步骤级状态奖励（记忆信息增益、回调检索增益、格式奖励）提供密集的中间步骤塑形信号。这与仅依赖最终答案奖励的传统方法形成对比，显著缓解了长序列中的稀疏监督问题。

### 2. 与同期/后续工作的关系

在长上下文推理领域，ReMemR1 与以下工作存在互补或对比关系：

- **Qwen2.5-1M**（Yang et al., 2025b）：通过扩展上下文窗口直接处理长序列，避免记忆压缩的信息损失，但计算成本随序列长度线性增长。ReMemR1 通过记忆压缩保持恒定推理开销，在超长上下文场景下具有效率优势。
- **R1-Distill-Qwen**（DeepSeek-AI et al., 2025）：作为蒸馏推理模型，具备强推理能力但缺乏显式记忆机制。ReMemR1 可与推理模型结合，在需要多跳证据整合的长上下文任务中互补。
- **Qwen2.5**（Yang et al., 2024）：通用大语言模型，作为 ReMemR1 的基础模型用于初始化策略网络，但本身不包含记忆增强或回调机制。

ReMemR1 的回调机制与检索增强生成（RAG）存在概念上的亲缘关系，但关键区别在于：RAG 通常从外部知识库检索，而 ReMemR1 的检索对象是智能体自身在推理过程中构建的**内部记忆历史**，检索时机和查询内容均由策略网络端到端学习，而非依赖固定的检索规则。

### 3. 适用边界

**适用场景：**
- 多跳问答任务，尤其是证据分散在长文档序列中的场景（如 HotpotQA、2WikiMultiHopQA）。
- 需要非线性回溯早期证据的推理任务，如跨文档实体链接、时序事件推理。
- 对推理延迟和内存开销有约束的长上下文场景（回调模块引入 <2 秒延迟和 <1MB 内存开销）。

**不适用或未验证的场景：**
- 非问答类长上下文任务（如长文档摘要、多文档翻译、长文本生成），当前评估未覆盖。
- 需要精确数值计算或结构化数据操作的任务，词重叠检索可能不足以捕捉语义关联。
- 极大规模模型（70B 及以上）上的扩展性尚未验证。

### 4. 局限与开放问题

**已识别的局限：**

1. **回调查询退化**：当上下文缺乏相关信息时，回调查询可能退化为不相关的通用查询（如重复问“美国总统”），导致检索失败。这表明查询生成策略缺乏对信息缺失的鲁棒处理。

2. **记忆污染**：早期步骤产生的错误信息（幻觉）一旦写入记忆便难以纠正，并可能覆盖后续正确证据。当前框架缺乏记忆修正或回滚机制。

3. **训练成本**：3B 模型需 16 块 H800 GPU 训练 100 小时，7B 模型需 32 块 H800 训练 80 小时，资源需求较高。

4. **评估范围有限**：仅在两个多跳问答数据集上验证，泛化性尚未在更广泛的长上下文任务中得到检验。

**开放问题：**

- 回调查询生成能否引入不确定性估计，在信息不足时主动抑制低质量查询？
- 能否设计记忆修正模块，在后续步骤检测并纠正早期写入的错误信息？
- 多级奖励的超参数 $\alpha$ 能否根据上下文长度或训练动态自适应调整，而非固定为 0.8？
- 检索函数 $\mathcal{E}$ 能否替换为可微的语义相似度模型（如基于嵌入的检索），以替代简单的词重叠召回？
- ReMemR1 在非问答类任务（如长文档摘要、多文档翻译）中的表现如何？回调机制在这些任务中是否同样有效？
- 在更大规模模型（如 70B 及以上）上的扩展性及性能增益如何？训练成本是否可接受？

## 原文 PDF

![[paperPDFs/ICLR_2026/Look_Back_to_Reason_Forward_Revisitable_Memory_for_Long_Context_LLM_Agents.pdf]]
