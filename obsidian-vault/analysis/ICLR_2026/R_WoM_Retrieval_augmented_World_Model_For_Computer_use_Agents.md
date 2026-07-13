---
title: "R-WoM: Retrieval-augmented World Model For Computer-use Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/R_WoM_Retrieval_augmented_World_Model_For_Computer_use_Agents.pdf
project_link: null
code_link: null
openreview_forum_id: 5ZaoXB3MdP
aliases:
- RWRAWM
- R-WoM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过检索外部教程为世界模型注入环境特定的过程性知识（grounding），并采用列表级相对奖励取代绝对奖励，从而稳定动作选择、减少幻觉。"
primary_logic: "LLM虽具备广泛的预训练知识，但缺少针对动态数字环境的精确、最新过程性知识。引入教程检索可为世界模型提供必要的上下文grounding，使长程rollout更准确；再结合列表级相对奖励比较而非绝对评分，可降低偏差，提升动作选择的鲁棒性。"
claims:
- "R-WoM在OSWorld和WebArena上相比最强基线分别取得最高23.4%和16.3%的相对提升，证实其整体有效性。"
- "LLM在无检索情况下的全流程规划对齐准确率不超过65%，揭示其长程计划能力的根本局限。"
- "教程grounding使得世界模型在更长的想象horizon（3步）上保持高于ungrounded模型的成功率，且WebDreamer在2步后开始下降。"
- "列表级奖励估计始终优于绝对奖励，在所有三个测试模型上带来2–3个百分点的提升。"
---

# R-WoM: Retrieval-augmented World Model For Computer-use Agents

> [!tip] 核心洞察
> LLM虽具备广泛的预训练知识，但缺少针对动态数字环境的精确、最新过程性知识。引入教程检索可为世界模型提供必要的上下文grounding，使长程rollout更准确；再结合列表级相对奖励比较而非绝对评分，可降低偏差，提升动作选择的鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向计算机使用Agent的检索增强世界模型 |
| 英文题名 | R-WoM: Retrieval-augmented World Model For Computer-use Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5ZaoXB3MdP) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | R-WoM (Retrieval-augmented World Model) |
| Dataset | OSWorld (subset of 87 tasks), WebArena (subset of 113 templates), OSWorld (Qwen-2.5-VL-72B), WebArena (Qwen-2.5-VL-72B) |

> [!tip] 效果简介
> - OSWorld (subset of 87 tasks) 上，Success Rate (%) 为 38.54 ± 1.92 (Claude-3.7-Sonnet)，对比 31.24 ± 2.88 (WebDreamer, second-best)，变化 ↑23.4% relative。
> - WebArena (subset of 113 templates) 上，Success Rate (%) 为 34.58 ± 1.10 (Claude-3.7-Sonnet)，对比 32.75 ± 0.72 (RAG, second-best)，变化 ↑5.6% relative。
> - OSWorld (Qwen-2.5-VL-72B) 上，Success Rate (%) 为 37.48 ± 2.29，对比 30.84 ± 1.07 (RAG)，变化 ↑21.5% relative。

## 概要

**核心问题**：当前基于大语言模型（LLM）的计算机使用Agent在长程任务中面临一个根本性瓶颈——LLM依赖静态参数化知识进行世界建模，缺乏对具体数字环境精确、最新的**过程性知识**（procedural knowledge），导致幻觉与复合误差快速累积，全流程规划对齐准确率在无检索条件下不超过65%（Table 1）。

**核心方法**：R-WoM（Retrieval-augmented World Model）通过两条关键机制解决上述问题：
1. **推理感知的检索增强grounding**：构建包含查询改写与LLM重排序的RAG管线，从外部教程中检索环境特定的过程性知识，为世界模型的想象rollout提供上下文grounding，使长程仿真更准确。
2. **列表级相对奖励估计**：对同一状态下多个候选rollout轨迹进行相对排名而非绝对评分，降低偏差，提升动作选择的鲁棒性。

**方法定位**：R-WoM属于世界模型驱动的计算机使用Agent方法，与迭代式rollout的代表方法**WebDreamer**（Gu et al., 2024）形成直接对比。WebDreamer完全依赖LLM内部静态世界知识且使用绝对稀疏奖励；R-WoM则引入外部教程grounding、LongCoT一次性rollout机制和列表级奖励，在保持世界模型框架的同时显著提升了长程规划与动作选择的可靠性。

**主要结果**：在OSWorld和WebArena两个基准上，R-WoM相比最强基线分别取得最高**23.4%**和**16.3%**的相对提升（Table 2）。消融实验证实：教程grounding质量单调影响性能（无检索 < R-WoM检索 < R-WoM oracle，Figure 4）；列表级奖励在所有测试模型上带来约2–3个百分点的稳定提升（Table 14）；grounded世界模型在更长的想象horizon（3步）上保持优势，而WebDreamer在2步后即开始下降（Figure 5）。



### 计算机使用Agent与世界模型

计算机使用Agent（Computer-use Agent）旨在根据自然语言指令，在真实的数字环境中自主完成复杂的多步操作任务。一个典型的交互轨迹可形式化为：

$$( g , ( o _ { 1 } , t _ { 1 } , a _ { 1 } ) , ( o _ { 2 } , t _ { 2 } , a _ { 2 } ) , \dots , ( o _ { n } , t _ { n } , a _ { n } ) )$$

其中 $g$ 为目标指令，$o_i$ 为第 $i$ 步的环境观察（如截图或无障碍树），$t_i$ 为内部思考，$a_i$ 为执行的动作。策略模型 $\pi_p$ 在每一步基于目标和历史上下文生成思考—动作对：

$$( t _ { i } , a _ { i } ) \sim \pi _ { p } \big ( \cdot \mid g , o _ { i } , \{ ( o _ { j } , t _ { j } , a _ { j } ) \} _ { j = v } ^ { i - 1 } \big )$$

为提升决策质量，世界模型（World Model）被引入以在行动前“想象”可能的未来状态。以代表性工作 **WebDreamer**（Gu et al., 2024）为例，其通过迭代式rollout机制，让策略模型与世界模型进行多轮通信以生成想象轨迹，并使用绝对稀疏奖励（如 $\{0, 0.5, 1.0\}$ 分别表示失败/进行中/成功）来评估候选动作。

### 核心瓶颈：静态世界知识导致的规划失准

尽管LLM具备广泛的预训练知识，但在面对特定数字环境（如操作系统、Web应用）时，其内部世界知识存在两个根本性缺陷：**静态性**（参数冻结后无法获取环境更新）和**缺乏环境特定的过程性知识**（不知道“在这个环境中如何正确地完成某事”）。

R-WoM通过三项探测实验量化了这一瓶颈（Table 1）：

1. **下一状态识别**：模型需从词汇高度相似的干扰项中区分真实的下一个状态。LLM整体准确率超过75%，说明其短程状态变化捕捉能力尚可。

2. **全流程规划对齐**：模型需生成多步执行计划，由LLM法官判断其是否与环境特定的参考教程在操作逻辑和环境约束上对齐：
   $$B = \Phi \Big ( \langle g , o _ { 1 } \rangle , \hat { P } , P ^ { * } \Big ) = \left\{ \begin{array} { l l } { \mathrm { T r u e , } } & { \mathrm { i f } \ \hat { P } \mathrm { a l i g n s ~ w i t h } \ P ^ { * } , } \\ { \mathrm { F a l s e , } } & { \mathrm { o t h e r w i s e . } } \end{array} \right.$$
   **在无检索条件下，全流程规划对齐准确率不超过65%**。这是核心瓶颈的直接证据：LLM虽能理解短程状态，但无法可靠地生成符合环境实际约束的长程操作序列，容易产生幻觉与复合误差。

3. **里程碑过渡识别**：模型需判断一段中间过渡序列是否反映了朝向目标的有效进展：
   $$\hat { S } = \arg \operatorname* { m a x } _ { S \in \{ S ^ { \mathrm { t r u e } } , S ^ { \mathrm { f a l s e } } \} } P ( \operatorname { s u c c e s s } \mid S , g )$$
   Claude-3.7-Sonnet在此任务上达到86.7%，表明模型具有一定的进度判别能力，但这一能力高度依赖对环境的正确理解。

Figure 1以具体任务“将桌面截图复制到光标所在位置”直观展示了这一差距：依赖LLM内部世界知识的Agent丢失了光标位置信息并陷入死循环，而拥有教程grounding的Agent则正确使用了“插入图片”操作并保持光标位置。

### 现有方法的缺口

现有方法在两个关键维度上存在不足：

- **WebDreamer** 的世界模型完全依赖LLM内部的静态世界知识进行rollout仿真，缺乏对环境特定过程性知识的grounding。这导致其在较长想象horizon（2步以上）时性能开始下降（Figure 5），因为累积的幻觉和偏差随rollout步数放大。

- **RAG基线** 虽引入了外部知识检索，但仅使用原始任务描述作为查询进行向量检索，不含查询改写或语义重排序，检索到的文档常与任务仅有表面词汇相似而缺乏实质相关性。

- **奖励估计** 方面，WebDreamer采用的绝对稀疏奖励容易引入偏差：模型对不同候选轨迹的评分缺乏相对比较基准，难以在多个看似合理的候选动作中做出精细区分。

这些缺口共同指向一个核心问题：**如何为LLM世界模型注入环境特定的、精确的过程性知识，并在仿真过程中以鲁棒的方式利用这些知识进行动作选择？** R-WoM正是围绕这一问题展开设计。



## 核心方法与创新机理

R-WoM 的核心创新在于为 LLM 世界模型引入**外部过程性知识的检索增强 grounding**，并配合**列表级相对奖励估计**，从而系统性地缓解 LLM 在长程数字环境建模中的幻觉与复合误差问题。相较于现有基线，该方法在以下关键维度实现了结构性改进。

### 1. 从静态世界知识到检索增强的教程 grounding

LLM 虽具备广泛的预训练知识，但在面对特定数字环境（如操作系统、网页应用）的精确操作流程时，其内部静态知识往往不完整或过时。论文的探测实验（Table 1）揭示了这一瓶颈：在不使用检索的情况下，LLM 的全流程规划对齐准确率**不超过 65%**，表明其长程计划能力存在根本性局限。

**WebDreamer**（Gu et al., 2024）作为代表性的世界模型基线，完全依赖 LLM 内部静态世界知识进行 rollout 仿真，缺乏环境特定的 grounding。R-WoM 通过**推理感知的 RAG 管线**改变了这一范式：

- **查询改写**：将任务目标转换为去语境化的通用查询，减少表面词汇差异对检索的影响（Section 4.2; Appendix A.3）。
- **LLM 重排序**：对初步检索得到的 top-k 文档进行语义相关性排序，过滤仅表面相似但语义无关的教程，产生高相关性的教程证据集 $\mathcal{E}$（Equation 9）。
- **条件化仿真**：世界模型在 rollout 时以教程证据 $\mathcal{E}$ 作为条件，使生成的想象轨迹具备环境特定的过程性知识支撑（Equation 10）。

消融实验（Figure 4）证实了 grounding 质量的因果作用：性能随 grounding 质量**单调提升**，即无检索 < R-WoM（检索教程）< R-WoM（oracle 教程），验证了教程信息的质量是性能提升的关键控制变量。

### 2. 从绝对奖励到列表级相对奖励估计

**WebDreamer** 采用绝对稀疏奖励（如 {0, 0.5, 1.0} 表示失败/进行中/成功），这种评分方式容易受到 LLM 评分偏差的影响。R-WoM 转而采用**列表级相对奖励排名**：对同一状态下多个候选 rollout 轨迹进行 LongCoT 推理，并按相对优劣排序，选择最优候选（Equation 11）。

这一设计的优势在于，相对比较比绝对评分更鲁棒——LLM 更擅长判断“A 比 B 更好”而非“A 应该得几分”。消融实验（Table 14）证实了该设计的有效性：列表级奖励在所有三个测试模型上均带来 **2–3 个百分点的提升**。

### 3. 从迭代式到 LongCoT 一次性 rollout

**WebDreamer** 采用迭代式 rollout 机制，策略模型与世界模型之间需要多轮通信生成轨迹，调用次数多、推理效率低。R-WoM 采用 **LongCoT rollout**：世界模型在单个前向推理链中一次性生成整个 $k$ 步想象轨迹（Equation 10），显著降低了模型调用次数，同时保持了仿真质量。

长程稳定性实验（Figure 5）表明，R-WoM 在想象 horizon 达到 3 步时性能达到峰值，且始终优于 WebDreamer；而后者在 horizon 超过 2 步后性能开始下降。这验证了教程 grounding 对长程仿真的稳定作用。

### 4. 自适应候选生成与去重

现有基线通常固定生成 $m$ 个候选动作或仅生成单个动作，缺乏对计算效率的考量。R-WoM 引入了**自适应分支**与**动作去重**两个互补机制：

- **自适应分支**：仅在策略模型不确定时生成多个候选（$1 \leq m \leq n$），避免在确定性高的步骤上浪费计算资源。
- **动作去重**：在投入世界模型仿真前，用策略模型自身作为验证器，识别并移除语义等价的冗余候选动作。

实验表明（Tables 6–8），自适应 R-WoM 在保持接近全量 R-WoM 性能的同时，将 token 消耗**减少 50% 以上**，世界模型触发次数降至原来的 **15–20%**，在性能与效率之间取得了实用化的平衡。

### 创新点总结

| 改进维度 | 基线做法 | R-WoM 做法 | 关键证据 |
|---------|---------|-----------|---------|
| 世界模型 grounding | 无外部知识注入（WebDreamer） | 推理感知 RAG 管线注入教程证据 | Figure 4：性能随 grounding 质量单调提升 |
| 奖励估计 | 绝对稀疏奖励 | 列表级相对奖励排名 | Table 14：2–3 个百分点提升 |
| Rollout 机制 | 迭代式多轮通信 | LongCoT 单次前向推理 | Figure 5：长 horizon 下稳定性显著优于基线 |
| 候选动作管理 | 固定数量或无优化 | 自适应分支 + 语义去重 | Tables 6–8：token 减少 50%+，性能基本持平 |
| 检索流程 | 原始查询直接检索（RAG） | 查询改写 + LLM 重排序 | Figure 3：召回率显著提升 |



![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_5ZaoXB3MdP/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the R-WoM pipeline. At each time step i, the policy model generates m candidate actions. For each candidate, the world model grounded by retrieved tutorials performs k-step rollouts to simulate a possible future trajectory. The rewards of rollout trajectories are finally estimated by world models to select the best action*

R-WoM 的整体流水线围绕一个核心洞察构建：LLM 虽然具备广泛的预训练知识，但缺少针对动态数字环境的精确、最新过程性知识。为此，R-WoM 在每个时间步引入检索增强的世界模型仿真机制，将外部教程证据注入想象轨迹的生成与评估过程，从而为动作选择提供环境特定的 grounding。

### 流水线总览

图 2 展示了 R-WoM 的完整推理流程。在每个时间步 i，系统执行以下闭环：

1. **策略模型生成候选动作**：给定任务目标 g、当前观察 o_i 和历史上下文，策略模型 π_p 生成 m 个候选思想-动作对 (t_i^(j), a_i^(j))。候选数量 m 通过自适应分支机制动态决定——当策略模型对当前状态信心充足时，m=1；仅在不确定性较高时扩展至多个候选（1 ≤ m ≤ n），以平衡探索与计算开销。

2. **动作去重**：在投入世界模型仿真前，系统以策略模型自身作为验证器，识别并移除语义等价的冗余候选动作，避免对相似动作重复进行昂贵的 rollout。

3. **推理感知检索**：系统通过查询改写将原始任务描述转换为去语境化的通用查询，减少表面词汇差异对检索的影响；随后用 LLM 作为列表级重排序器，从 top-k 候选集中筛选出高相关性的教程证据集 E。

4. **Grounded 世界模型 LongCoT Rollout**：对于每个去重后的候选动作，世界模型 π_w 以教程证据 E 为条件，通过单次 LongCoT 推理链生成完整的 k 步想象轨迹 τ̂_i^(j)，模拟未来的状态变化与动作后果。与 WebDreamer 的迭代式 rollout 不同，LongCoT 机制将多步仿真折叠进单个前向推理序列，显著降低了模型调用次数。

5. **列表级奖励估计与动作选择**：世界模型对所有候选 rollout 轨迹进行相对比较与排名，而非分配绝对分数。系统选择使列表级相对分数最大的思想-动作对作为最优执行动作，从而降低绝对奖励估计中的系统性偏差。

### 关键公式

检索证据集的生成遵循：

$$ \mathcal{E} = f_p^{\mathrm{rank}}(\mathcal{C}_k, q) $$

其中 C_k 为初步检索的 top-k 候选教程，q 为改写后的查询，f_p^rank 为 LLM 重排序器。

世界模型的 LongCoT rollout 轨迹定义为：

$$ \hat{\tau}_i^{(j)} = \pi_w^{\mathrm{LongCoT}}(o_i, t_i^{(j)}, a_i^{(j)}; \mathcal{E}) $$

最终动作选择通过列表级相对排名完成：

$$ (t_i^*, a_i^*) = \arg\max_{(t_i^{(j)}, a_i^{(j)}) \in \mathcal{A}_c} \Big[ f_w \big( R(\hat{\tau}_i^{(j)}, g, \mathcal{E}) \big) \Big] $$

其中 A_c 为去重后的候选动作集合，R(·) 为 rollout 轨迹的奖励信号，f_w 为世界模型的相对排名函数。

### 模块协作关系

流水线中的七个核心模块形成层级依赖：查询改写与 LLM 重排序器构成推理感知检索管线，为世界模型提供 grounding 基础；Grounded 世界模型利用 LongCoT rollout 完成多步仿真；列表级奖励估计器对仿真结果进行相对比较；自适应分支与动作去重则在前端控制候选动作的质量与数量，直接影响世界模型的调用频率与整体计算开销。消融实验（Table 6-8）表明，自适应机制在保持接近全量 R-WoM 性能的同时，将 token 消耗减少 50% 以上，世界模型触发降至原来的 15–20%。



R-WoM 的核心架构由七个协同模块构成，围绕“检索增强的世界模型仿真”与“列表级相对奖励估计”两条主线展开。以下按推理流程逐一说明关键模块及其对应的核心公式。

### 推理感知的检索管线

传统 RAG 方法直接将原始任务描述作为查询进行向量检索，忽略了任务描述中的环境特定词汇（如具体文件名、路径）对检索精度的干扰。R-WoM 采用两阶段推理感知检索管线：

**查询改写（Query Rewriting）。** 该模块将任务目标转换为去语境化的通用查询，剥离表面词汇差异对检索的影响。例如，将“把桌面上的 1.png 复制到光标所在位置”改写为“如何在文档中插入图片”，从而匹配更广泛的教程内容。

**LLM 重排序（LLM-based Reranker）。** 初步向量检索返回的 top-k 候选教程中，可能存在仅表面相似但语义无关的文档。该模块利用 LLM 对候选集进行列表级语义相关性排序，过滤噪声，最终产生高质量的教程证据集 $\mathcal{E}$：

$$
\mathcal{E} = f_p^{\mathrm{rank}}(\mathcal{C}_k, q)
$$

其中 $\mathcal{C}_k$ 为初步检索返回的 top-k 候选集，$q$ 为改写后的查询。消融实验（Figure 3）表明，查询改写与重排序联合使用时，Recall@1 可达 49.0%，Recall@5 达 79.6%，显著优于单独使用任一策略。

### 自适应动作分支与去重

策略模型在每一步生成候选动作时，R-WoM 采用自适应分支策略：仅在模型信心不足时生成多个候选（$1 \le m \le n$），避免不必要的计算开销。在投入世界模型仿真之前，**动作去重模块**利用策略模型自身作为验证器，识别并移除语义等价的冗余候选动作。消融实验（Table 7）显示，自适应机制在保持接近全量 R-WoM 性能的同时，将世界模型触发次数降至原来的 15–20%。

### 基于 LongCoT 的 Grounded 世界模型

与 WebDreamer 采用的迭代式 rollout（策略模型与世界模型多轮通信）不同，R-WoM 的世界模型在单个 LongCoT 前向推理链中一次性生成完整的 $k$ 步想象轨迹。该过程以检索到的教程证据 $\mathcal{E}$ 为条件，为仿真注入环境特定的过程性知识：

$$
\hat{\tau}_i^{(j)} = \pi_w^{\mathrm{LongCoT}}(o_i, t_i^{(j)}, a_i^{(j)}; \mathcal{E})
$$

其中 $o_i$ 为当前观察，$(t_i^{(j)}, a_i^{(j)})$ 为第 $j$ 个候选思想-动作对，$\hat{\tau}_i^{(j)}$ 为生成的 $k$ 步想象轨迹。教程 grounding 的核心作用在于：LLM 内部静态世界知识在长程仿真中容易产生幻觉与复合误差，而外部教程提供了精确的环境操作约束。Figure 5 证实，grounded 世界模型在 horizon=3 时达到最优，且始终优于无 ground 的 WebDreamer（后者在 horizon=2 后性能开始下降）。

### 列表级奖励估计器

传统世界模型（如 WebDreamer）采用绝对稀疏奖励（$\{0, 0.5, 1.0\}$ 表示失败/进行中/成功）对 rollout 轨迹评分，容易引入评分偏差。R-WoM 改为列表级相对奖励排名：对同一状态下所有候选 rollout 轨迹进行 LongCoT 推理，按相对优劣排序，选择最优候选：

$$
(t_i^*, a_i^*) = \arg\max_{(t_i^{(j)}, a_i^{(j)}) \in \mathcal{A}_c} \Big[ f_w \big( R(\hat{\tau}_i^{(j)}, g, \mathcal{E}) \big) \Big]
$$

其中 $\mathcal{A}_c$ 为去重后的候选动作集，$R(\cdot)$ 为相对奖励函数，$f_w(\cdot)$ 为列表级比较函数。消融实验（Table 14）表明，列表级奖励在所有三个测试模型上均带来 2–3 个百分点的稳定提升。

### 策略模型

策略模型 $\pi_p$ 基于任务目标 $g$、当前观察 $o_i$ 和历史上下文生成候选思想-动作对，作为世界模型仿真的起点。其输出形式为：

$$
(t_i, a_i) \sim \pi_p \big( \cdot \mid g, o_i, \{(o_j, t_j, a_j)\}_{j=v}^{i-1} \big)
$$

该模块本身不包含世界建模能力，其生成质量依赖于后续世界模型的验证与筛选。



## 实验与关键发现

### 端到端性能主结果

R‑WoM 在 OSWorld（87 个任务子集）和 WebArena（113 个模板子集）上均一致优于所有基线方法（Table 2）。以最强的 Claude‑3.7‑Sonnet 为 backbone 时，R‑WoM 在 OSWorld 上达到 38.54% 的成功率，相比第二好的 WebDreamer（31.24%）实现了 23.4% 的相对提升；在 WebArena 上达到 34.58%，相比第二好的 RAG（32.75%）提升了 5.6%。该优势在不同 backbone 上保持稳定：Qwen‑2.5‑VL‑72B 上相对提升分别为 21.5%（OSWorld）和 16.3%（WebArena），Claude‑3.5‑Sonnet 上分别为 10.8% 和 8.0%。所有结果均报告三次运行的均值 ± 标准差，且所有方法使用相同的 backbone LLM 与 top‑5 检索块，保证公平性。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_5ZaoXB3MdP/figures/004_Table_2.jpg]]
*Table 2: End-to-end performance on OSWorld and WebArena across three runs. Best in bold; second-best underlined. ↑· denotes this relative improvement over the second-best baseline*

### 检索策略的贡献

推理感知的检索管线是 grounding 质量的关键。Figure 3 显示，查询改写（query rewriting）与 LLM 重排序（reranking）各自都能提升 Recall@k，但两者联合使用时效果最优：在 OSWorld 上 Recall@1 达到 49.0%，Recall@5 达到 79.6%。这表明去语境化的通用查询与语义级重排序共同过滤掉了表面相似但语义无关的教程，为世界模型提供了更精确的环境过程性知识。

### Grounding 质量对性能的因果作用

Figure 4 揭示了 grounding 质量与成功率之间的单调关系：无教程的 WebDreamer 性能最低，R‑WoM（检索教程）居中，R‑WoM（oracle 教程）最高。这一趋势在 OSWorld 和 WebArena 上均成立，直接证实了教程证据 E 的质量是控制世界模型仿真准确性的关键因果旋钮——检索质量越高，世界模型产生的想象轨迹越接近真实环境动态，动作选择越可靠。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_5ZaoXB3MdP/figures/009_Figure_4.jpg]]
*Figure 4: Performance under different grounding settings, where we compare ungrounded world model: WebDreamer, world model grounded with retrieved tutorials: R-WoM, and world model grounded with oracle tutorials: R-WoM (oracle). (a) OSWorld*

### 长程想象 horizon 的稳定性

Figure 5 比较了 R‑WoM 与 WebDreamer 在不同想象 horizon（1–4 步）下的成功率。R‑WoM 在 horizon 3 处达到峰值，且在所有 horizon 下均优于 WebDreamer；而 WebDreamer 在 horizon 2 后性能开始下降。这说明教程 grounding 使世界模型在更长程的 rollout 中保持了对环境状态的准确跟踪，有效抑制了无 grounding 时随 horizon 增长而加剧的幻觉与复合误差。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_5ZaoXB3MdP/figures/010_Figure_5.jpg]]
*Figure 5: Success rates (%) across imagination horizons on OSWorld (a) and WebArena (b). R-WoM (green, solid) consistently outperforms WebDreamer (red, dashed) and reaches its peak at larger imagination horizon (at horizon around 3)*

### 奖励估计策略的消融

Table 14 对比了列表级相对奖励与绝对奖励变体在 OSWorld 上的表现。在 Qwen‑2.5‑VL‑72B、Claude‑3.5‑Sonnet 和 Claude‑3.7‑Sonnet 三个 backbone 上，列表级奖励始终比绝对奖励高出约 2–3 个百分点。这一致性提升表明，对同一状态下的候选 rollout 进行相对排序，比依赖绝对稀疏评分（如 {0, 0.5, 1.0}）更能消除评分偏差，使动作选择更鲁棒。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_5ZaoXB3MdP/figures/025_Table_14.jpg]]
*Table 14: Comparison between R-WoM (listwise reward) and its absolute reward variant on the OSWorld benchmark*

### 候选动作数量与自适应机制

候选动作数量 m 的消融（Table 15）显示，m=3 时整体性能最优；m=5 时收益递减，对较弱模型甚至略有下降。基于此，自适应分支机制仅在策略模型不确定时生成多个候选，动作去重机制则在 rollout 前移除语义等价冗余。Tables 6–8 表明，自适应 R‑WoM 在保持接近全量 R‑WoM 性能的同时，将 token 消耗减少 50% 以上，世界模型触发次数降至全量版本的 15–20%，显著降低了计算开销。

### 失败模式分析

Table 11 按任务类型划分的失败分布显示，内容修改类任务（如精确编辑文档、代码）是主要失败来源，这类任务需要更精细的元素定位与多步推理，对世界模型的细粒度状态追踪能力提出了更高要求。Table 10 进一步表明，即使检索成功，R‑WoM 在部分任务上仍会失败，说明教程 grounding 虽大幅减少幻觉，但 LLM 在长程全流程规划中的对齐能力依然有限，偶尔会生成看似合理但实际不可执行的步骤。

### 教程稀缺场景的泛化

Table 3 评估了 R‑WoM 在缺少现成在线教程的场景下的表现。通过自博弈轨迹合成教程，R‑WoM 在 Claude‑3.7‑Sonnet、Claude‑4‑Sonnet 和 Claude‑4.5‑Sonnet 上分别达到 35.71%、39.28% 和 49.29% 的成功率，均优于 Vanilla、RAG 和 WebDreamer 基线。这说明 R‑WoM 的检索增强范式在教程稀缺时仍可通过合成数据维持 grounding 的有效性，但合成质量与覆盖度直接影响性能上限。

### 评估鲁棒性验证

Table 12 报告了不同 LLM 法官给出的全流程规划对齐评分，结果在不同法官间保持一致，验证了规划对齐评估指标的鲁棒性。Table 13 在更强的 backbone（Claude‑4‑Sonnet、Claude‑4.5‑Sonnet）上进一步确认了 R‑WoM 的优势，表明该方法随 backbone 能力增强而持续受益。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_5ZaoXB3MdP/figures/002_Table_1.jpg]]
*Table 1: Probing results across three tasks: next-state identification, full-procedure planning alignment, and milestone transition recognition. All values are percentages*



## 定位与知识库关联

### 1. 方法谱系：从内部世界知识到检索增强的grounded仿真

R-WoM 的核心贡献在于将LLM世界模型从**依赖静态内部知识**推进到**检索增强的环境特定grounding**，并在奖励估计与rollout机制上进行了系统重构。其方法谱系可沿以下维度展开：

**世界建模范式的演进。** 传统计算机使用Agent（如 Vanilla 基线）完全跳过世界模型，直接由策略模型基于当前观察生成动作。**WebDreamer**（Gu et al., 2024）首次引入迭代式世界模型rollout——策略模型与世界模型通过多轮通信生成想象轨迹，但其世界模型完全依赖LLM内部静态知识，缺乏对环境特定过程性知识的访问。R-WoM 在此基础上做出关键突破：通过推理感知的RAG管线检索外部教程，将世界模型从“无grounding”转变为“教程grounded”的仿真模式。这一转变的因果效应在 Figure 4 中得到清晰验证：性能随grounding质量单调提升（无grounding < 检索教程 < oracle教程），证实教程证据是性能提升的直接操纵变量。

**检索策略的深化。** 标准RAG基线仅使用原始任务描述作为查询进行向量检索（LangChain + FAISS），不含查询改写或重排序。R-WoM 引入了推理感知检索管线：先对任务查询进行匿名化/泛化改写以减少表面词汇差异的影响，再用LLM进行列表级重排序以过滤仅表面相似但语义无关的教程。Figure 3 显示，查询改写与重排序结合使用时检索召回率最高，为后续世界模型仿真提供了更高质量的grounding证据。

**奖励估计的范式转换。** WebDreamer 采用绝对稀疏奖励（如 {0, 0.5, 1.0} 表示失败/进行中/成功），这种绝对评分方式容易引入偏差且对阈值敏感。R-WoM 转向列表级相对奖励排名：对同一状态下多个候选rollout轨迹进行LongCoT推理并按相对优劣排序，选择最优候选。Table 14 的消融实验表明，列表级奖励在所有三个测试模型上均带来约2–3个百分点的稳定提升，证实相对比较策略优于绝对评分。

**Rollout机制的效率优化。** WebDreamer 的迭代式rollout需要策略模型与世界模型之间进行多轮交互，计算开销大。R-WoM 采用LongCoT rollout，使世界模型在单个前向推理链中一次性生成整个 k 步想象轨迹，显著降低了模型调用次数。同时，自适应动作分支与去重机制进一步优化了效率：自适应R-WoM在保持接近全量R-WoM性能的同时，将token消耗减少50%以上，世界模型触发降至原来的15–20%（Tables 6-8）。

### 2. 适用边界与局限

**教程依赖与稀缺场景。** R-WoM 的性能与检索教程的质量和覆盖度强相关。在缺乏现成在线教程的场景下，需依赖自博弈轨迹合成教程（Table 3），合成质量直接影响grounding效果。此外，检索模块在任务描述模糊或需要深层语义推理时可能失败（Table 9），尽管有回退策略，但仍会削弱grounding效果。

**长程规划的固有上限。** 即使加入教程检索，LLM在长程全流程规划中的对齐能力仍然有限（Table 1显示无检索时不超过65%）。模型偶尔会生成看似合理但实际不可执行的步骤，这揭示了LLM在过程性知识推理上的根本局限，而非检索质量所能完全弥补。

**任务类型的非对称表现。** 内容修改类任务（如精确编辑文档、代码）是主要失败来源（Table 11），这类任务需要更精细的元素定位与多步推理，超出了当前世界模型仿真与教程grounding的能力边界。

**计算开销。** 世界模型仿真带来了额外的计算与token开销（Table 5, Table 8），虽已通过自适应与去重优化，但在较长horizon下成本依然不小，限制了其在资源受限场景中的部署。

### 3. 开放问题

1. **多模态grounding的扩展。** 当前检索仅依赖文本教程，如何将检索扩展至多模态信息（如视觉截图），以提供更丰富的环境grounding？
2. **动态检索机制。** 能否设计步骤感知的动态检索机制，使其在长程推理过程中自适应调整检索焦点，而非仅在初始阶段进行一次性检索？
3. **奖励模型的增强。** 列表级相对奖励能否与基于偏好的微调方法（如DPO）结合，进一步强化世界模型的动作选择能力？
4. **检索失败的优雅纠正。** 当检索结果完全失败时，如何从世界模型内部更优雅地纠正而非仅依赖启发式回退？这需要世界模型具备更强的内部知识校准能力。
5. **真实环境泛化性。** R-WoM 在更开放或对安全性要求更高的真实计算机使用环境中的表现与泛化性如何？当前评测限于OSWorld和WebArena的受控子集，向真实桌面环境的迁移仍需验证。



## 原文 PDF

![[paperPDFs/ICLR_2026/R_WoM_Retrieval_augmented_World_Model_For_Computer_use_Agents.pdf]]
