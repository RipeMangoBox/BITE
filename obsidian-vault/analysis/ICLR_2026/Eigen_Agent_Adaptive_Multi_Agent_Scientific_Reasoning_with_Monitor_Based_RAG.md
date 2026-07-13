---
title: "Eigen-Agent: Adaptive Multi-Agent Scientific Reasoning with Monitor-Based RAG"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Eigen_Agent_Adaptive_Multi_Agent_Scientific_Reasoning_with_Monitor_Based_RAG.pdf
project_link: null
code_link: https://github.com/tangxiangru/Eigen-1
openreview_forum_id: bGtmGTbmaz
aliases:
- Eigen-Agent
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "Monitor‑based RAG 以 token 级不确定性监控和隐式证据注入消除工具税；HSR 通过锚‑参考分层精炼取代平均化；QAIR 依据质量评分自适应迭代，实现收敛与早停。"
primary_logic: "隐式知识增强与结构化分层精炼可同时提升科学推理准确率和计算效率；检索任务依赖多样性，推理任务依赖共识。"
claims:
- "Explicit RAG 使迭代步数从 43.4 增至 94.8，token 消耗从 483.6K 升至 470.6K；Monitor‑based RAG 将 token 降至 218.4K、步骤降至 51.3，准确率保持 34.5%"
- "完整系统在 HLE Bio/Chem 达 48.3%，较 SciMaster 提升 13.4 个百分点，token 减少 53.5%，步骤减少 43.7%"
- "移除 HSR 导致准确率从 48.3% 降至 44.8%，移除 QAIR 降至 43.7%，证明分层精炼与质量感知迭代的关键作用"
- "92.8% 的失败含推理错误，88.7% 含知识缺口，两者高度重叠，说明工具税与劣质协作是共因"
---

# Eigen-Agent: Adaptive Multi-Agent Scientific Reasoning with Monitor-Based RAG

> [!tip] 核心洞察
> 隐式知识增强与结构化分层精炼可同时提升科学推理准确率和计算效率；检索任务依赖多样性，推理任务依赖共识。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Eigen-Agent：基于监视器检索的自适应多智能体科学推理框架 |
| 英文题名 | Eigen-Agent: Adaptive Multi-Agent Scientific Reasoning with Monitor-Based RAG |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=bGtmGTbmaz) · [GitHub](https://github.com/tangxiangru/Eigen-1) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | EIGEN‑AGENT |
| Dataset | HLE Bio/Chem Gold (149 题), SuperGPQA Hard Biology, TRQA |

> [!tip] 效果简介
> - HLE Bio/Chem Gold (149 题) 上，Pass@1 accuracy (%) 为 48.30，对比 34.92 (SciMaster, DeepSeek V3.1)，变化 +13.38。
> - SuperGPQA Hard Biology 上，Pass@1 accuracy (%) 为 69.57，对比 66.30 (SciMaster, DeepSeek V3.1)，变化 +3.27。
> - TRQA 上，Pass@1 accuracy (%) 为 54.65，对比 51.74 (Autogen, GPT‑4.1)，变化 +2.91。

## 概要

### 问题瓶颈

当前多智能体科学推理系统面临两个相互耦合的核心瓶颈。其一，**显式检索引入“工具税”**：代理在推理过程中主动发起检索调用，导致推理流频繁中断，步骤数和 token 消耗急剧膨胀。其二，**民主式多智能体协作稀释强解**：多数聚合策略（如投票、平均化批评-改写）无视候选解之间的质量差异，使得高质量解被低质量解平均化，且推理错误与知识缺口高度重叠——分析显示，92.8% 的失败案例包含推理错误，88.7% 包含知识缺口，二者显著共现（Figure 7）。

### 核心方法

**Eigen-Agent** 通过三个关键机制解决上述瓶颈：

- **Monitor-based RAG**：以 token 级不确定性监控取代显式工具调用。Monitor 以 512 字符块、128 字符重叠连续扫描推理流，检测到语义不确定性后隐式触发检索；Injector 对检索结果进行过滤、压缩和重写，无缝嵌入推理上下文，消除工具税（Figure 3）。
- **分层解精炼（HSR）**：轮流将每个候选解作为锚点，利用其余解作为参考进行逻辑补全、数值修正、方法替换和表达优化，以结构化跨解修复取代平均化聚合（Figure 5）。
- **质量感知迭代推理（QAIR）**：按加权评分 $q(s') = 0.2 \cdot q_{\text{logic}} + 0.6 \cdot q_{\text{answer}} + 0.2 \cdot q_{\text{explanation}}$ 评估候选解质量，仅对不达标解执行 Corrector，达到阈值 $\tau=3$ 或最大轮数后早停。

### 核心结论

在 HLE Bio/Chem Gold（149 题）上，Eigen-Agent 以 **48.3%** 的 Pass@1 准确率超越最强代理基线 SciMaster **+13.4 个百分点**，同时将 token 消耗降低 **53.5%**，代理步骤减少 **43.7%**（Figure 1, Table 2）。组件分析证实：Monitor 将 token 从 470.6K 降至 218.4K、步骤从 94.8 降至 51.3；移除 HSR 导致准确率下降 3.5 个百分点，移除 QAIR 下降 4.6 个百分点（Table 3）。此外，多样性-共识分析揭示了一项关键洞察：**检索任务受益于多样性（斜率 ≈0.369），推理任务受益于共识（斜率 ≈0.851）**，为分层精炼优于统一平均提供了机制性解释（Figure 8）。

### 方法定位

Eigen-Agent 属于**隐式检索增强的多智能体精炼框架**。相较于单轮 RAG（高效但不可适应）、迭代 RAG（改善接地性但增加延迟）和推理感知 RAG（耦合更紧密但仍依赖显式调用），Monitor-based RAG 在 token 级别隐式注入证据，实现了连续性与效率的统一（Table 1）。在多智能体协作维度，HSR 和 QAIR 的组合以质量感知的结构化精炼替代了 SciMaster 等系统的民主式流水线，形成“检索任务多样性、推理任务共识”的分层策略。

> **需注意**：当前实验仅覆盖生物学和化学领域，Monitor 的流式监控参数和 QAIR 的评分权重基于经验设定，在其他科学领域和不同模型上的泛化性尚待验证。



### 科学推理的两个瓶颈

当前大语言模型在专家级科学推理任务中面临两个高度耦合的瓶颈。第一个瓶颈来自**显式检索引入的“工具税”**。当推理过程需要外部知识时，智能体必须主动发出检索调用、暂停生成、将返回结果拼接到上下文中，然后重新连接推理流。这种中断式交互不仅大幅增加 token 消耗和代理步骤数，更关键的是破坏了推理的叙事连贯性——检索到的证据往往以“上下文悬浮”的方式存在，模型难以将其无缝融入原有的推理链条。

第二个瓶颈源于**民主式多智能体协作的质量稀释**。典型的多智能体流水线（如求解-批评-改写循环）将所有候选解视为平等贡献者，通过平均化或简单投票进行聚合。然而，候选解之间存在显著的质量差异：一个候选解可能在数值计算上正确但逻辑跳跃，另一个可能逻辑严谨但误用了领域公式。平均化聚合无法区分这些差异，导致强解被弱解稀释，而错误推理与知识缺口在失败案例中高度重叠（92.8% 的失败含推理错误，88.7% 含知识缺口）。

### 现有方法的局限

表 1 系统对比了四种 RAG 范式的能力维度。单轮 RAG 效率高但不可适应；迭代 RAG 改善了知识锚定但增加了延迟；推理感知 RAG 虽实现了更紧密的耦合，但仍依赖显式工具调用，无法从根本上消除工具税。在多智能体协作方面，现有框架（如 SciMaster 的批评-改写流水线、Autogen 的可配置对话）均采用统一聚合策略，未对候选解的质量差异进行建模。

### 本文动机与核心洞察

本文的核心洞察在于：**隐式知识增强与结构化分层精炼可以同时提升科学推理的准确率和计算效率**。具体而言，检索任务依赖多样性（不同查询视角覆盖更广的证据空间），而推理任务依赖共识（高质量解在逻辑和答案上趋于一致）。这一发现（检索任务斜率 ≈0.369，推理任务斜率 ≈0.851）直接否定了“统一平均化”的合理性，为分层精炼提供了经验依据。

基于上述分析，本文提出 Eigen-Agent 框架，通过两个关键机制解决前述瓶颈：Monitor-based RAG 以 token 级不确定性监控和隐式证据注入消除工具税；HSR（分层解精炼）通过锚-参考结构化精炼取代平均化；QAIR（质量感知迭代推理）依据加权质量评分自适应控制迭代深度。



## 核心方法与创新机理

Eigen‑Agent 的核心创新并非引入全新的推理范式，而是对现有多智能体科学推理系统中的三个结构性瓶颈——**工具税（tool tax）**、**民主式聚合稀释**与**质量盲迭代**——进行了因果层面的重新设计。三项关键创新分别对应三个 changed slot，形成一条从“知识获取 → 解空间精炼 → 迭代控制”的因果链。

### 创新一：Monitor‑based RAG —— 消除工具税的隐式知识增强

传统显式 RAG（如 SciMaster 中基于嵌入相似度的论文检索）要求推理代理主动发出工具调用、暂停生成、等待检索结果并重新连接上下文。这一过程引入显著的“工具税”：实验显示，添加外部论文库使准确率从 25.3% 升至 41.4%，但迭代步数从 43.4 翻倍至 94.8，token 消耗从 483.6K 升至 470.6K（Table 3）。更关键的是，检索结果以“查询‑结果原样拼接”方式注入，造成上下文悬浮与推理流断裂（Figure 2 右侧案例）。

Monitor‑based RAG 从根本上改变了检索的触发模式与整合方式：

- **触发模式变更**：Monitor 以 512 字符块、128 字符重叠的流式窗口连续扫描推理流，检测语义不确定性后**隐式触发**检索，而非等待代理主动调用。这使检索从“中断式工具调用”转变为“后台知识注入”（Table 1 中 Continuity 维度）。
- **整合方式变更**：Injector 先对检索结果进行过滤压缩，再重写为与当前推理上下文连贯的叙述，将证据无缝嵌入 Proposer 的推理流中，消除了显式 RAG 的上下文重新连接开销（Figure 4 单倍型计数案例）。

效果是显著的：在仅添加 Monitor 模块后（+Papers → +Monitor only），token 消耗从 470.6K 骤降至 218.4K（降幅 53.6%），步骤从 94.8 降至 51.3，而准确率保持在 34.5%（Table 3）。这证明 Monitor‑based RAG 在保持知识增益的同时，几乎完全消除了工具税。

### 创新二：HSR —— 从平均化到分层结构精炼

现有多智能体系统（如 SciMaster 的求解‑批评‑改写流水线）采用民主式聚合：所有候选解平等参与批评与改写，或通过简单投票选择最终答案。这种机制无视候选解之间的质量差异，强解常被弱解的平均化效应稀释。错误分析显示，92.8% 的失败案例包含推理错误，88.7% 包含知识缺口，且两者高度重叠（Figure 7），说明劣质协作与知识不足是共因。

HSR 将聚合策略从“平等平均”改为“锚‑参考分层精炼”：

- **旋转锚点机制**：依次将每个候选解设为锚点，其余解作为参考，对锚点进行逻辑补全、数值修正、方法替换和表达优化（Figure 5 示例）。
- **跨解结构化修复**：不同于 Corrector 的局部修复（无跨解视野），HSR 利用多解之间的互补信息进行针对性修正，而非简单平均。

增量构建实验验证了这一创新的独立贡献：添加 HSR 后准确率从 40.3% 提升至 43.7%（Table 3）。消融实验中，从完整系统移除 HSR 导致准确率从 48.3% 降至 44.8%（降幅 3.5 个百分点），证实分层精炼的不可替代性。

### 创新三：QAIR —— 质量感知的自适应迭代与早停

传统多智能体系统采用固定轮数或全量重改策略，缺乏对解质量的动态感知。QAIR 引入质量评分驱动的选择性迭代控制：

- **加权质量评分**：对每个候选解 $s'$ 计算加权分 $q(s') = 0.2 \cdot q_{\text{logic}}(s') + 0.6 \cdot q_{\text{answer}}(s') + 0.2 \cdot q_{\text{explanation}}(s')$，答案正确性权重最高（0.6），逻辑合理性与解释完备性各占 0.2。
- **选择性纠正与早停**：仅对未达到阈值 $\tau=3$ 的解触发 Corrector 进行修正，达到阈值或最大轮数后停止，避免无效迭代。

这一创新与 HSR 形成互补：HSR 提供结构化跨解精炼，QAIR 决定“何时精炼、精炼什么”。增量构建中，QAIR 将准确率从 43.7% 进一步提升至 48.3%（Table 3）；消融实验中移除 QAIR 导致准确率降至 43.7%（降幅 4.6 个百分点），与移除 HSR 的损失（4.5 个百分点）相当，证实两者的独立且互补的贡献。

### 创新间的因果耦合

三项创新并非孤立存在，而是形成一条因果链：Monitor‑based RAG 以最低成本提供高质量知识基础 → HSR 在此基础上进行跨解结构化精炼 → QAIR 确保精炼过程的质量收敛与计算效率。这一耦合关系在多样性‑共识分析中得到佐证：检索任务受益于多样性（斜率 ≈ 0.369），推理任务受益于共识（斜率 ≈ 0.851，Figure 8），而 Eigen‑Agent 的架构恰好实现了“检索阶段保持多样性、推理阶段追求共识”的自适应平衡。



![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_bGtmGTbmaz/figures/005_Figure_3.jpg]]
*Figure 3: Framework overview. (a) Monitor-based RAG operates globally during reasoning: the Monitor detects insufficiency in the reasoning stream, the Querier generates targeted queries, and the Injector integrates retrieved evidence into context with minimal disruption. (b) Building on this substrate, the Proposer generates initial candidate solutions. Each candidate is revised individually by the Corrector, which applies local targeted fixes without access to other solutions. The improved candidates are then passed to HSR, which enables cross-solution refinement via anchor–reference relationships. Finally, QAIR evaluates overall quality and may invoke the Corrector again if needed, while the Ranker...*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_bGtmGTbmaz/figures/004_Table_1.jpg]]
*Table 1: RAG paradigms vs. key capabilities. Single-round RAG is efficient but inadaptable; iterative RAG improves grounding but increases latency; reasoning-aware RAG offers tighter coupling yet still relies on explicit calls. Monitor-based RAG integrates evidence implicitly at the token level, improving continuity and efficiency*

Eigen‑Agent 由两条协同主线构成：**Monitor‑based RAG** 提供持续、低干扰的外部知识注入，**多智能体精炼流水线** 在知识基座上完成解生成、结构修正与自适应迭代。两者的核心设计目标一致：在提升科学推理准确率的同时，显著压缩传统显式检索和民主式协作引入的计算开销。

### 两条主线与模块关系

**1. Monitor‑based RAG 子系统（全局知识层）**  
该子系统在推理全过程中持续运行，不依赖代理显式发出工具调用。三个模块按序协作：

- **Monitor**：以流式方式扫描推理文本，按 512‑字符块、128‑字符重叠的固定窗口检测语义不确定性，输出二值决策——触发检索（1）或继续（0）。
- **Querier**：收到触发信号后，从当前推理片断中提取最小化关键词集合，生成一个或多个精准检索查询。
- **Injector**：对检索结果进行过滤、压缩与重写，将关键证据无缝嵌入 Proposer 的推理上下文，保持叙事连贯，避免“上下文悬浮”。

这一设计将知识获取从“中断‑查询‑拼接”的显式模式，转变为 token 级隐式注入，从而消除了传统 RAG 的**工具税**——即检索调用导致的推理流中断、token 膨胀和步骤翻倍。

**2. 多智能体精炼流水线（解质量层）**  
在 Monitor‑based RAG 提供的知识基座上，五个并行 Proposer 生成初始候选解。随后，流水线通过以下模块逐级提升解质量：

- **Corrector**：对单个候选解执行局部修复（无跨解视野）。
- **HSR（Hierarchical Solution Refinement）**：将候选解两两配对，轮转每个解作为“锚点”，其余解作为“参考”，对锚点进行逻辑补全、数值修正、方法替换和表达优化。这取代了传统多智能体系统中的平均化聚合，避免强解被弱解稀释。
- **QAIR（Quality‑Aware Iterative Reasoning）**：对每个候选解按加权公式 $q(s') = 0.2 \cdot q_{\text{logic}} + 0.6 \cdot q_{\text{answer}} + 0.2 \cdot q_{\text{explanation}}$ 评分，仅对未达阈值（$\tau=3$）的解调用 Corrector 进行定向修正，达到阈值或最大轮数后早停。
- **Ranker**：从最终候选池中选择最优解作为最终答案。

### 输入输出流

1. 用户输入科学问题，系统启动五个并行 Proposer。
2. 每个 Proposer 在推理过程中，Monitor 持续监控流式输出；一旦检测到知识不足，Querier 生成查询，Injector 将检索证据注入上下文，Proposer 继续推理。
3. 所有 Proposer 输出初始候选解后，Corrector 进行首轮局部修复。
4. HSR 对修正后的候选池执行锚‑参考轮转精炼。
5. QAIR 评估每个解的质量，选择性触发 Corrector 再次修正，直至满足早停条件。
6. Ranker 输出最终答案。

### 设计逻辑：检索依赖多样性，推理依赖共识

框架的模块分工背后有一条关键洞察：**检索任务受益于多样性，推理任务受益于共识**。Monitor‑based RAG 在知识获取阶段保持多 Proposer 的搜索多样性，而 HSR 和 QAIR 在推理精炼阶段通过结构化锚‑参考修正与质量阈值筛选，将多样性收敛为高质量共识。这一“先发散、后收敛”的架构，是 Eigen‑Agent 在 HLE Bio/Chem 上以 48.3% 准确率超越 SciMaster 13.4 个百分点、同时将 token 消耗降低 53.5% 的结构性原因。

> **注意**：上述管线中 Monitor 的流式参数（块大小 512、重叠 128）、QAIR 的权重分配与阈值 $\tau=3$ 均基于经验设定，未经过系统超参数调优，在不同任务上可能需要手动调整。



Eigen‑Agent 的推理架构由两个正交子系统构成：**Monitor‑based RAG** 负责隐式知识增强，**分层精炼流水线** 负责多解协作与质量收敛。以下仅展开其关键模块与核心公式。

### Monitor‑based RAG：隐式知识增强

传统显式 RAG 在推理过程中要求智能体主动发出工具调用，导致推理流中断（即“工具税”）。Monitor‑based RAG 通过三个模块实现 token 级的隐式证据注入。

**Monitor** 以流式方式持续扫描推理流：每 512 字符为一个检测窗口，相邻窗口重叠 128 字符，判断当前上下文是否存在语义不确定性。其决策函数为二值输出：

$$
\mathrm{Monitor}(\mathrm{context}) = \begin{cases} 1, & \text{if retrieval is required} \\ 0, & \text{otherwise} \end{cases}
$$

当 Monitor 输出 1 时，触发检索；否则推理继续，无任何中断。

**Querier** 接收 Monitor 标记的不确定片段，将其映射为一个或多个最小化关键词集合，生成精准检索查询：

$$
[\mathbf{query}_1, \dots, \mathbf{query}_n] = \mathrm{Querier}(\mathrm{context})
$$

这一精细化查询策略在控制精度与召回的同时，避免引入冗余信息。

**Injector** 对检索结果执行过滤、压缩与重写，将证据无缝嵌入 Proposer 的推理上下文，保持叙事连贯性。实验表明，添加 Injector 后准确率从 34.5% 跃升至 40.3%，说明证据整合（而非查询生成）是显式 RAG 的主要瓶颈（Table 3 增量构建）。

### 分层精炼流水线：HSR 与 QAIR

多智能体系统通常采用民主式聚合（投票或平均化），但这会稀释高质量候选解的优势。Eigen‑Agent 以 **HSR** 和 **QAIR** 两个模块实现结构化精炼与质量自适应迭代。

**HSR（Hierarchical Solution Refinement）** 将候选解池中的每个解依次作为“锚点”，其余解作为“参考”，执行跨解的结构化修复：逻辑补全、数值修正、方法替换和表达优化。这不同于简单平均化——HSR 通过锚‑参考关系实现定向修补，而非对不一致候选解的无差别融合。

**QAIR（Quality‑Aware Iterative Reasoning）** 在 HSR 输出的基础上对每个候选解进行三维质量评分：

$$
q(s') = 0.2 \cdot q_{\mathrm{logic}}(s') + 0.6 \cdot q_{\mathrm{answer}}(s') + 0.2 \cdot q_{\mathrm{explanation}}(s')
$$

其中 $q_{\mathrm{logic}}$ 评估逻辑合理性，$q_{\mathrm{answer}}$ 评估答案正确性，$q_{\mathrm{explanation}}$ 评估解释完备性。答案正确性被赋予最高权重（0.6），体现了科学推理中对最终结论的严格约束。

评分后，QAIR 将低于阈值 $\tau=3$ 的候选解标记为“未通过”，交由 Corrector 进行定向修正；通过的解直接保留。这一选择性纠正机制结合最大轮数约束，实现了自适应早停——既避免固定轮数的低效迭代，又防止过度修正引入新错误。组件消融实验证实：移除 HSR 使准确率从 48.3% 降至 44.8%，移除 QAIR 降至 43.7%，二者独立贡献均约 4.5–4.6 个百分点（Table 3 组件消融）。

### 因果机制总结

Monitor‑based RAG 消除了显式检索的工具税，使 token 消耗从 470.6K 降至 218.4K，步骤从 94.8 降至 51.3（Table 3 增量构建）；HSR 与 QAIR 分别解决了多解聚合中的平均化稀释与无差别迭代问题。两个子系统的协同作用使得完整框架在 HLE Bio/Chem 上以 53.5% 的 token 缩减和 43.7% 的步骤缩减，实现了 48.3% 的准确率。



## 实验与关键发现

### 主实验结果

Eigen‑Agent 在三个高难度科学推理基准上均取得最优成绩，并在计算效率上显著超越现有智能体系统。在 **HLE Bio/Chem Gold**（149 题，o3‑mini 自动评判）上，Eigen‑Agent 以 DeepSeek‑V3.1 为基础模型取得 **48.3%** 的 Pass@1 准确率，较最强智能体基线 **SciMaster** 的 34.9% 提升 **13.4 个百分点**，同时领先前沿 LLM（如 Grok‑4）达 18.1 个百分点（Table 2, Figure 1）。在 Pass@5 设定下，准确率进一步提升至 61.7%。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_bGtmGTbmaz/figures/002_Figure_1.jpg]]
*Figure 1: HLE Bio/Chem Gold overall accuracy. On the 149-problem HLE Bio/Chem Gold split (Pass@1, auto-judged by o3-mini), our system attains 48.3% accuracy, exceeding the strongest agent baseline (SciMaster) by +13.4 points and leading frontier LLMs by up to +18.1 points*

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_bGtmGTbmaz/figures/008_Table_2.jpg]]
*Table 2: Benchmark comparison under matched protocol. HLE Bio/Chem (149 problems; o3-mini judge), SuperGPQA Biology (hard split), and TRQA Literature (multiple-choice)*

在 **SuperGPQA Hard Biology** 上，Eigen‑Agent 达到 69.6%（Pass@1），较 SciMaster 提升 3.3 个百分点；在 **TRQA** 文献理解基准上，以 54.7% 的 Pass@1 准确率超越 **Autogen**（GPT‑4.1）的 51.7%（Table 2）。

更重要的是，这些准确率提升伴随显著的效率增益。完整系统与 SciMaster 相比，token 消耗减少 **53.5%**，智能体级迭代步骤减少 **43.7%**，证明 Monitor‑based RAG 和分层精炼机制在提升推理质量的同时有效控制了计算开销。

### 增量构建与组件消融

Table 3 从增量构建和组件移除两个维度揭示了各模块的独立贡献。基线配置（五个并行 Proposer + 网络搜索，无外部论文检索）在 HLE Bio/Chem 上仅达 **25.3%** 准确率，消耗 43.4 步、483.6K token。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_bGtmGTbmaz/figures/012_Table_3.jpg]]
*Table 3: Component analysis from two perspectives on the full HLE Bio/Chem benchmark (149 problems). (a) Incremental build-up: modules are added one by one. (b) Component ablation: each module is removed from the full system. The baseline configuration uses five parallel Proposers with web search but without external paper retrieval (no RAG). Steps = agent-level workflow iterations (not token-level reasoning)*

**显式检索的代价。** 添加外部论文库（Explicit RAG）使准确率跃升至 **41.4%**，但步骤翻倍至 94.8，token 增至 470.6K。这直接验证了“工具税”瓶颈：检索虽补全知识缺口，却因频繁中断推理流而大幅抬高计算成本。

**Monitor 的逆转效应。** 引入 Monitor 后，token 骤降至 **218.4K**，步骤降至 51.3，准确率保持在 34.5%。这证明 token 级不确定性监控和隐式证据注入能够在不牺牲推理连续性的前提下，将检索开销压缩至可控范围。进一步叠加 Querier 和 Injector 后，准确率回升至 **40.3%**，表明证据整合（而非查询生成）是 Monitor‑based RAG 的关键增益来源。

**HSR 与 QAIR 的互补增益。** 在 Monitor‑based RAG 基础上添加 HSR，准确率从 40.3% 提升至 **43.7%**，验证了锚‑参考分层精炼相比民主式平均化的优势。QAIR 进一步将准确率推至 **48.3%**，证明质量感知的选择性迭代能够有效收敛推理过程。消融实验反向印证：从完整系统中移除 HSR 导致准确率下降 4.5 个百分点（至 44.8%），移除 QAIR 下降 4.6 个百分点（至 43.7%），两者贡献独立且互补。

### 失败模式分析

Figure 7 对错误解的日志分析显示，**92.8%** 的失败案例包含推理过程错误，**88.7%** 包含知识应用错误，且两者高度重叠。这一强耦合关系揭示了核心瓶颈：知识缺口与推理错误并非独立发生，而是相互加剧——错误的公式记忆导致推理偏航，而检索中断又使正确知识无法有效融入推理流。Monitor‑based RAG 和 HSR 分别从知识注入和跨解修复两个层面针对这一共因进行干预。

### 多样性‑共识权衡

Figure 8 揭示了任务类型对多智能体协作策略的根本性影响。以 Proposer 间答案一致性为横轴、正确性评分为纵轴的连续评估表明：**检索任务**收益于多样性（拟合斜率 ≈ 0.369），而**推理任务**强烈依赖共识（拟合斜率 ≈ 0.851）。这一发现直接佐证了 Eigen‑Agent 的设计选择——HSR 通过结构化精炼追求共识，而非简单平均化所有候选解；QAIR 则以质量阈值为导向，在保持必要多样性的同时实现早停。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_bGtmGTbmaz/figures/013_Figure_8.jpg]]
*Figure 8: Diversity vs. consensus. Task-dependent effect of solution diversity: retrieval tasks benefit from variety, while reasoning tasks benefit from agreement. The horizontal axis reports the average pairwise consistency score among Proposers, computed by an LLM-based judge that evaluates semantic overlap between answers on a 0–1 scale. The vertical axis shows the average accuracy score, also judged by an LLM, which rates the degree of correctness of each answer relative to ground truth on a continuous 0–1 scale (rather than a binary 0/1). This continuous evaluation enables us to capture fine-grained trends between diversity and correctness across tasks. The fitted trend lines further highlight t...*

### 检索后端与语料影响

Figure 6 对比了不同检索后端在 Monitor‑based RAG 框架下的表现。**HippoRAG** 因其细粒度图结构索引获得最一致的增益，表明检索粒度与推理需求的匹配度是隐式知识增强的关键因素。Table A5 进一步显示，使用通用混合领域语料仍可达 45.6%，仅略低于生物/化学专用语料（48.3%），说明框架本身的架构优势是性能提升的主要驱动力，而非单纯依赖领域语料的覆盖度。

---

**证据强度说明：** 上述结论均基于 Table 2、Table 3、Figure 7、Figure 8 等已标注的高置信度证据。实验在相同基础模型（DeepSeek‑V3.1，温度 0.5，64K token 限制）、相同并行 Proposer 数量和相同外部工具访问权限下进行，确保增量变化仅源于模块本身。



## 定位与知识库关联

### 1. 核心瓶颈与因果抓手

当前多智能体科学推理系统面临两个高度耦合的瓶颈。其一为**显式检索引入的“工具税”**：推理代理在生成过程中主动暂停以调用外部检索工具，导致推理流中断、上下文碎片化，同时大幅推高 token 消耗与步骤数。其二为**民主式多智能体协作的稀释效应**：多数现有系统采用平均化或简单投票聚合候选解，无视解间质量差异，导致强解被弱解稀释，且错误推理与知识缺口高度重叠——论文分析显示 92.8% 的失败包含推理错误，88.7% 包含知识缺口，两者显著共现（Figure 7）。

Eigen-Agent 的因果调控旋钮围绕三个机制展开：
- **Monitor‑based RAG**：以 token 级不确定性监控替代显式工具调用，实现隐式证据注入，消除工具税；
- **HSR（Hierarchical Solution Refinement）**：通过锚点‑参考分层精炼取代平均化聚合，对候选解进行结构化跨解修复；
- **QAIR（Quality‑Aware Iterative Reasoning）**：依据质量评分自适应触发纠正与早停，实现收敛控制。

核心洞察可概括为：**隐式知识增强与结构化分层精炼可同时提升科学推理的准确率与计算效率；检索任务依赖多样性，推理任务依赖共识**（Figure 8，检索任务斜率约 0.369，推理任务斜率约 0.851）。

### 2. 在 RAG 范式谱系中的定位

论文将现有 RAG 范式归纳为四类（Table 1），Eigen-Agent 的 Monitor‑based RAG 在五个维度上形成差异化：

| 范式 | 触发方式 | 粒度 | 连续性 | 效率 | 适应性 |
|------|----------|------|--------|------|--------|
| 单轮 RAG | 查询级 | 粗 | ✓ | ✓ | ✗ |
| 迭代 RAG | 轮次级 | 中 | ✗ | ✗ | ✓ |
| 推理感知 RAG | 推理步级 | 细 | ✗ | ✗ | ✓ |
| **Monitor‑based RAG** | **token 级** | **细** | **✓** | **✓** | **✓** |

关键区分在于：单轮 RAG 仅在初始查询时检索一次，效率高但无法适应推理过程中的动态知识需求；迭代 RAG 和推理感知 RAG 虽然提高了知识接地性，但仍依赖显式工具调用，每次检索都中断推理流，产生显著的上下文重连成本。Monitor‑based RAG 则以 512 字符块、128 字符重叠的流式监控（Table A2）持续扫描推理流中的语义不确定性，仅在检测到知识不足时才隐式触发检索，由 Injector 对检索结果进行过滤、压缩和重写后无缝嵌入推理上下文，保持叙事连贯性（Figure 4）。

### 3. 与现有多智能体系统的关系

Eigen-Agent 在**多智能体精炼策略**上与以下系统形成对比：

- **SciMaster**（求解‑批评‑改写流水线 + 选择器）：采用民主式迭代精炼，所有候选解平等参与批评与改写，缺乏质量感知的选择性纠正。Eigen-Agent 在相同基础模型 DeepSeek‑V3.1 下，以 48.3% vs 34.9% 的准确率优势（Table 2），同时减少 53.5% token 和 43.7% 步骤，核心差异源于 HSR 的结构化锚点‑参考精炼和 QAIR 的质量阈值早停机制。
- **Autogen**（可配置多智能体对话框架）：通用对话框架，未内建领域知识检索与分层精炼。在 TRQA 基准上，Eigen-Agent（GPT‑4.1）以 54.7% vs 51.7% 领先（Table 2）。
- **OpenAI Deep Research**（基于 o4‑mini 的深度研究代理）和 **Grok‑4**（前沿 LLM 基准）：均依赖模型内部知识，无外部论文检索。Eigen-Agent 在 HLE Bio/Chem 上领先 Grok‑4 近 18 个百分点（Figure 1），领先 Deep Research 约 11 个百分点（Table A4）。
- **Biomni**（生物学领域专用代理）：领域特化但未采用 Monitor‑based RAG 或分层精炼，在 SuperGPQA Hard Biology 上以 66.3% vs 69.6% 落后于 Eigen-Agent（Table 2）。

### 4. 适用边界与局限

**已验证的适用领域**：当前实验仅覆盖生物学和化学领域（HLE Bio/Chem Gold 149 题、SuperGPQA Hard Biology、TRQA），在其他科学领域（物理、工程等）的泛化性能未经测试。消融实验显示，使用通用混合领域语料时准确率仍达 45.6%，仅略低于生物/化学专用语料的 48.3%（Table A5），表明架构本身是主要驱动力，但领域迁移仍需验证。

**超参数敏感性**：
- Monitor 的流式监控参数（块大小 512、重叠 128）和检索 top‑k=3 的选择基于经验设定，未进行系统调优；
- QAIR 的评分权重（逻辑 0.2、答案 0.6、解释 0.2）和阈值 τ=3 固定，可能对不同任务需要调节。

**工具税衡量的不完整性**：当前仅以 token 数量和步骤数衡量工具税，未涵盖推理延迟、内存消耗等完整开销指标。

**多智能体假设的简化**：系统假设独立的 Proposer/Corrector 角色，未考虑智能体动态角色切换或异构模型组合的可能性。

**自动评判的局限**：所有实验依赖 o3‑mini 进行自动评判，其与人类专家的对齐度仅在部分样本上验证。

### 5. 开放问题

1. **框架可移植性**：Monitor‑based RAG 能否在不修改模型架构的条件下无缝集成到其他推理范式（如 ReAct、Tree‑of‑Thoughts）？其流式监控接口是否与现有代理框架兼容？

2. **多样性‑共识的动态权衡**：Figure 8 揭示的任务依赖性（检索任务偏好多样性，推理任务偏好共识）是否可以通过在线学习动态调整，而无需预定义任务类别？QAIR 的固定阈值策略在此场景下可能次优。

3. **QAIR 迭代评价的内生偏差**：QAIR 本身是一个基于 LLM 的评价器，其评分可能对熟悉模式产生过拟合，如何检测和缓解这种评价偏差？

4. **多模态扩展**：框架如何扩展到多模态输入（图表、化学结构式、分子式等）？Monitor 和 Querier 的设计需要如何调整以处理非文本不确定性信号？

5. **低资源环境可行性**：在纯黑盒 API 或无本地部署能力的低资源环境下，隐式检索的延迟和成本是否仍然可控？Monitor 的流式处理是否引入额外的 API 调用开销？

6. **错误类型的因果解耦**：推理错误与知识缺口之间的强重叠（Figure 7）暗示深层因果关系——知识不足是否直接诱发推理错误，还是两者共享共同的底层表征缺陷？因果建模能否实现更根本的修正，而非仅靠检索和精炼进行症状缓解？



## 原文 PDF

![[paperPDFs/ICLR_2026/Eigen_Agent_Adaptive_Multi_Agent_Scientific_Reasoning_with_Monitor_Based_RAG.pdf]]
