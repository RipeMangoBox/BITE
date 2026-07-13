---
title: "Strategic Planning and Rationalizing on Trees Make LLMs Better Debaters"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Strategic_Planning_and_Rationalizing_on_Trees_Make_LLMs_Better_Debaters.pdf
project_link: null
code_link: https://github.com/LeiLiLab/TreeDebater
openreview_forum_id: E1hbqtHrvg
aliases:
- SPRTMLBD
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "引入排练树（Rehearsal Tree）和辩论流树（Debate Flow Tree），模拟人类辩手的树状推理与跟踪，使LLM能够前瞻对手攻击并实时选择最优辩论行动。"
primary_logic: "通过树状结构预先评估论点的抗攻击强度并在辩论中追踪交互状态，LLM可以模仿专家进行多样化、战略性强的动作选择，从而显著提升说服力。"
claims:
- "在阶段级对比中，DeepSeek骨干的TreeDebater说服力评分平均提升15.6%，赢率显著优于基线。"
- "在辩论级评估中，Gemini骨干的TreeDebater意见转变胜率提升3.5倍，DeepSeek提升1.3倍。"
- "消融实验表明移除排练树和辩论流树会导致说服力下降，验证了树结构的有效性。"
- "Stage-level head-to-head human evaluation 上 Average Persuasiveness Score (DeepSeek) = 4.01"
---

# Strategic Planning and Rationalizing on Trees Make LLMs Better Debaters

> [!tip] 核心洞察
> 通过树状结构预先评估论点的抗攻击强度并在辩论中追踪交互状态，LLM可以模仿专家进行多样化、战略性强的动作选择，从而显著提升说服力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于树结构的战略规划与理性推理使大语言模型成为更优辩手 |
| 英文题名 | Strategic Planning and Rationalizing on Trees Make LLMs Better Debaters |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=E1hbqtHrvg) · [GitHub](https://github.com/LeiLiLab/TreeDebater) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | TreeDebater |
| Dataset | Stage-level head-to-head human evaluation, End-to-end debate human evaluation |

> [!tip] 效果简介
> - Stage-level head-to-head human evaluation 上，Average Persuasiveness Score (DeepSeek) 为 4.01，对比 3.47，变化 +0.54 (+15.6%)。
> - End-to-end debate human evaluation 上，Opinion Shift Win (DeepSeek) 为 0.40，对比 0.30，变化 +0.10 (+10pp)。
> - End-to-end debate human evaluation 上，Opinion Shift Win (Gemini) 为 0.46，对比 0.13，变化 +0.33 (3.5x)。

## 概要

**问题瓶颈**：现有基于大语言模型（LLM）的辩论系统在竞争性辩论中面临双重挑战——严格的时间限制使动态策略规划极为困难，而缺乏客观奖励信号又导致模型难以自主判断论点的说服力强弱。以 **Agent4Debate**（Zhang et al., 2024）为代表的多智能体框架虽已取得进展，但其依赖粗略字数估算控制时间，常出现超时或内容不足；同时缺乏对对手攻击的前瞻性推演，导致策略选择趋于单一。

**核心方法**：**TreeDebater** 借鉴人类辩手的树状推理模式，引入两类树结构来实现战略规划与理性推理。辩论前，系统为每个主要主张构建**排练树**（Rehearsal Tree），自顶向下生成潜在反驳与防御，并自底向上通过极小极大式递归计算强度分数，以预判论点的抗攻击能力。辩论中，**辩论流树**（Debate Flow Tree）实时追踪所有主张、攻击与防御的交互状态，从中提取候选行动并检索预演论据。此外，TreeDebater 采用 **FastSpeech** 模型精确估算语音时长，通过二分搜索迭代修订语句以严格满足时间约束；并引入基于人类辩论流树检索的**模拟观众反馈**机制，针对逻辑流、受众意识等维度提供改进建议。

**关键发现**：在阶段级头对头人工评估中，以 DeepSeek 为骨干的 TreeDebater 说服力评分平均达 4.01，相较基线提升 15.6%（+0.54）；在端到端辩论评估中，以 Gemini 为骨干时意见转变胜率从 0.13 跃升至 0.46，提升约 3.5 倍。消融实验表明，移除排练树或辩论流树均会导致各阶段说服力显著下降，且反驳阶段的动作多样性明显退化，验证了树结构对策略规划的关键作用。

辩论是人类理性沟通与集体决策的核心形式，要求参与者在严格的时间限制下，通过构建主张、发起攻击和进行防御来说服观众。近年来，大语言模型（LLM）在辩论任务中展现出潜力，但现有系统在竞争性辩论场景中仍面临根本性瓶颈。

现有LLM辩手的主要局限在于缺乏有效的动态策略规划能力。在真实的竞争性辩论中，每一轮陈述都面临严格的时间约束，辩手必须在有限时间内选择最优行动——是攻击对方论点、强化己方立场，还是两者兼顾。然而，当前系统通常仅依赖顺序记录或简单的链式推理，无法前瞻性地评估不同行动策略的潜在收益，也难以实时追踪辩论的复杂交互状态。更关键的是，辩论场景缺乏客观的奖励信号，使得LLM难以自主判断何种策略更可能说服观众。

以先进的多智能体辩论框架**Agent4Debate**（Zhang et al., 2024）为代表的现有方法，虽然在辩论流程自动化方面取得了进展，但其策略规划仍停留在反应式层面：辩手根据对手上一轮陈述生成回应，而未能预先推演对手可能的攻击路径并据此准备防御。同时，这些系统在时间控制上依赖粗略的字数估算，导致大量陈述超时或内容不足，进一步削弱了辩论的完整性和说服力。

上述瓶颈指向一个核心问题：**LLM辩手需要一种结构化的推理机制，使其能够像人类专家辩手一样，在辩论前进行前瞻性推演，在辩论中实时追踪攻防状态，并据此做出多样化的策略性行动选择。**

本文提出的TreeDebater正是针对这一缺口。其核心动机在于：通过引入树状结构来模拟人类辩手的推理与跟踪过程，使LLM能够在辩论前预演对手攻击并计算论点强度，在辩论中构建动态的攻防流图以指导实时决策，从而在严格时间约束下实现更具说服力的战略辩论。

## 核心方法与创新机理

TreeDebater 的核心创新在于将人类辩手的树状推理与规划机制引入 LLM 辩论框架，通过“排练树”和“辩论流树”双树结构，解决了现有方法在竞争性辩论中缺乏前瞻性策略规划与实时状态跟踪的根本瓶颈。

### 1. 排练树：辩论前的攻防预演

现有基线方法（如 **Agent4Debate**, Zhang et al., 2024）在辩论开始前不进行系统性的对手行为预测。TreeDebater 引入**排练树（Rehearsal Tree）**，为每个主要主张构建一棵最大深度为 L 的攻防树，自顶向下生成潜在反驳，自底向上计算强度分数（Section 3.2, Alg. 1）。

强度分数的计算采用极小极大（minimax）思想，从己方视角评估主张的稳健性。首先定义基础强度分数 $f_0(x^l)$，根据节点在树中的层级 $l$ 分别考虑支持分数 $r_s$ 和攻击分数 $r_a$：

$$
f _ { 0 } ( x ^ { l } ) = { \left\{ \begin{array} { l l } { r _ { s } ( x ^ { l } , s ) } & { { \mathrm { i f ~ } } l = 0 } \\ { r _ { a } ( x ^ { l } , x ^ { l - 1 } ) } & { { \mathrm { i f ~ } } l = 1 } \\ { { \frac { 1 } { 2 } } { \big ( } r _ { a } ( x ^ { l } , x ^ { l - 1 } ) + r _ { s } ( x ^ { l } , x ^ { l - 2 } ) { \big ) } } & { { \mathrm { i f ~ } } l \geq 2 } \end{array} \right. }
$$

随后通过 k 步递归计算考虑对手最优反驳后的预期效用，衰减系数 $\gamma = 0.8$：

$$
f _ { k } ( x ^ { l } ) = f _ { 0 } ( x ^ { l } ) - \gamma \cdot \operatorname* { m a x } _ { x ^ { l + 1 } \in \mathrm { C h i l d } ( x ^ { l } ) } f _ { k - 1 } ( x ^ { l + 1 } )
$$

这一机制使 TreeDebater 能够在辩论前评估各主张的抗攻击强度，为后续的策略选择提供量化依据。实验表明，超过半数的候选行动已在排练树中被预演（Figure 3），验证了其前瞻性预测的有效性。

### 2. 辩论流树：辩论中的实时状态跟踪与策略规划

基线方法缺乏显式的辩论状态跟踪机制，仅依赖顺序记录。TreeDebater 引入**辩论流树（Debate Flow Tree）**，在每轮结束后从对方陈述中提取 (action, claim, argument, target) 元组，实时更新树结构以记录所有主张及其攻防关系（Section 3.3, Alg. 2）。基于辩论流树，TreeDebater 能够识别当前活跃的候选行动，并从排练树中检索已准备的论据与强度分数，从而进行多样化的策略选择。

消融实验（Table 3）揭示了双树结构的关键作用：
- 移除排练树后，Opening、Rebuttal、Closing 说服力分数分别从 3.50 降至 3.00、3.50 降至 3.25、3.75 降至 3.50。
- 进一步移除辩论流树后，Opening 和 Rebuttal 分数继续降至 3.00。

在反驳阶段，TreeDebater 展示了与人类专家更为相似的动作分布，包括攻击兼反驳、单独攻击、单独强化等多种策略组合；而移除辩论流树后动作多样性显著下降（Figure 2）。这证明辩论流树是实现策略多样化的关键驱动因素。

### 3. 语音时间控制器：精确的时间预算管理

基线方法使用粗略的字数估算控制发言时长，常导致超时或内容不足。TreeDebater 采用轻量级文本转语音模型 **FastSpeech**（Ren et al., 2020）进行精确的语音时长估算，并通过二分搜索迭代修订语句，使其符合严格的时间限制 $[t_l, t_r]$（Section 3.5）。这一改进使 TreeDebater 在所有辩论阶段的格式和时间有效性均达到 100%，而基线在 Closing 阶段的时间有效性仅为 13.5%（Gemini）和 5.8%（DeepSeek）（Table 6）。

### 4. 模拟观众反馈：基于人类辩论经验的迭代优化

TreeDebater 引入基于检索的模拟观众机制（Section 3.4），从人类辩论流树中检索相似辩论上下文，提供针对逻辑流、受众意识、证据使用和主张质量等多维度的具体反馈。这一机制使 TreeDebater 能够在不依赖真实人类评估的情况下，迭代改进陈述质量，弥补了基线方法缺乏受众感知的不足。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_E1hbqtHrvg/figures/009_Figure_4.jpg]]
*Figure 4: (a) Rehearsal Tree. The root node is the main claim c. The blue nodes are from the same side as the root, and the green ones are the potential counterarguments from the opposite side. rs is the support score and r _ { a } is the attack score. (b) Debate Flow Tree of the Con side. The blue indicates its claims, while the green indicates the claims proposed by its opponent (Pro side) to attack the Con side’s claims. v indicates the visit number. Figure 4: Illustration of Rehearsal Tree (a) and Debate Flow Tree (b)*

TreeDebater 的核心设计围绕两个树结构展开——**排练树（Rehearsal Tree）** 在辩论前构建，前瞻对手攻击与防御；**辩论流树（Debate Flow Tree）** 在辩论中实时追踪交互状态并指导行动选择。整个 pipeline 在每一阶段按固定流程运行，如图 1 所示。

### 系统工作流

在每个辩论阶段（Opening / Rebuttal / Closing），TreeDebater 执行以下步骤：

1. **更新辩论流树**：从当前对手陈述中提取 `(action, claim, argument, target)` 元组，更新己方的辩论流树以反映最新辩论状态（Section 3.3, Alg. 2）。
2. **检索预演论据**：从排练树中，根据当前辩论流树识别出的候选行动，检索已准备的论据及其强度分数（Section 3.3）。
3. **生成草稿**：基于检索到的论据和强度分数，由 LLM 生成辩论陈述草稿（Figure 1 step iii）。
4. **模拟观众反馈**：利用基于人类辩论流树检索构建的模拟观众，从逻辑流、受众意识、证据使用和主张清晰度等维度提供针对性反馈（Section 3.4）。
5. **修订与时间控制**：结合模拟观众反馈和语音时间控制器的约束，迭代修订陈述，使其既具有说服力又满足严格的时间限制（Section 3.5）。

### 模块关系与数据流

| 模块 | 输入 | 输出 | 执行时机 |
|------|------|------|----------|
| **Rehearsal Tree Builder** | 主要主张、支持/攻击评分模型 $r_s$, $r_a$ | 排练树（含 k 步强度分数） | 辩论前（一次性） |
| **Debate Flow Tree Updater** | 对手陈述中的行动元组 | 更新后的辩论流树 | 每轮辩论后 |
| **Argument Retriever** | 辩论流树中的候选行动 | 排练树中匹配的论据与分数 | 每阶段生成前 |
| **Draft Generator** | 检索论据、强度分数、阶段提示 | 陈述草稿 | 每阶段生成时 |
| **Simulated Audience** | 陈述草稿、检索的人类辩论流树 | 多维度反馈 | 草稿生成后 |
| **Speech Time Controller** | 陈述文本、时间上下界 $[t_l, t_r]$ | 时间合规的修订文本 | 最终修订阶段 |

### 关键设计选择

- **双树解耦**：排练树负责“战前推演”，辩论流树负责“战中跟踪”，两者在时间维度上解耦，使得前瞻规划不占用辩论时的推理预算。
- **强度分数驱动**：排练树采用极小极大思想递归计算 k 步强度分数（Eqn 1-2），为后续行动选择提供定量依据，而非仅依赖 LLM 的即时判断。
- **时间控制闭环**：通过 FastSpeech 模型精确估算语音时长，并结合二分搜索迭代修订，确保生成文本始终满足时间约束——这是基线方法（仅用粗略字数估算）常失败的关键瓶颈。

TreeDebater 的核心设计围绕两类树结构展开：**排练树（Rehearsal Tree）** 用于辩论前的战略预演，**辩论流树（Debate Flow Tree）** 用于辩论中的实时状态跟踪与行动规划。二者协同使 LLM 辩手能够前瞻对手攻击、检索预设论据并做出多样化、高强度的动作选择。

### 排练树（Rehearsal Tree）

排练树在辩论开始前为每个主要主张 $c = x^{(0)}$ 构建一棵最大深度为 $L$ 的树，自顶向下逐层生成潜在反驳与防御，模拟双方可能的攻防回合（Section 3.2, Alg. 1）。根节点为己方主张，蓝色节点为同方论证，绿色节点为对手潜在反驳。构建完成后，自底向上计算每个节点的强度分数，用于评估主张的抗攻击能力。

**基础强度分数** 定义为：

$$f _ { 0 } ( x ^ { l } ) = { \left\{ \begin{array} { l l } { r _ { s } ( x ^ { l } , s ) } & { { \mathrm { i f ~ } } l = 0 } \\ { r _ { a } ( x ^ { l } , x ^ { l - 1 } ) } & { { \mathrm { i f ~ } } l = 1 } \\ { { \frac { 1 } { 2 } } { \big ( } r _ { a } ( x ^ { l } , x ^ { l - 1 } ) + r _ { s } ( x ^ { l } , x ^ { l - 2 } ) { \big ) } } & { { \mathrm { i f ~ } } l \geq 2 } \end{array} \right. }$$

其中 $r_s(\cdot)$ 为支持分数，$r_a(\cdot)$ 为攻击分数，$l$ 为节点所在层级。根节点（$l=0$）仅考虑其对立场 $s$ 的支持强度；直接子节点（$l=1$）仅考虑其对父节点的攻击强度；更深层节点（$l \geq 2$）则同时考虑对父节点的攻击和对祖父节点的支持。

**$k$ 步递归强度分数** 采用极小极大思想，从己方视角评估在对手最优反驳下的预期效用：

$$f _ { k } ( x ^ { l } ) = f _ { 0 } ( x ^ { l } ) - \gamma \cdot \operatorname* { m a x } _ { x ^ { l + 1 } \in \mathrm { C h i l d } ( x ^ { l } ) } f _ { k - 1 } ( x ^ { l + 1 } )$$

其中 $\gamma = 0.8$ 为衰减系数，$\mathrm{Child}(x^l)$ 表示节点 $x^l$ 的所有子节点（即对手的潜在反驳）。该公式递归地减去对手最优子节点的强度，模拟多步攻防后主张的净效用。$k$ 步分数越高，表明该主张在经受 $k$ 轮攻击后仍具有较强说服力。

为获得 $r_s$ 和 $r_a$ 分数，TreeDebater 在 Kialo 数据集上训练了两个基于 LLaMA-3.2-3B-Instruct 的奖励模型，分别预测支持影响力和反驳影响力（Section 4.1）。需注意，这些奖励模型准确率有限（支持影响力 0.67，反驳影响力 0.72），可能影响排练树中分数计算的可靠性。

### 辩论流树（Debate Flow Tree）

辩论流树在辩论过程中实时维护，记录所有已提出的主张及其攻击和防御关系（Section 3.3, Alg. 2）。每轮听取对方陈述后，TreeDebater 首先从中提取行动元组 `(action, claim, argument, target)`，随后将这些元组更新到辩论流树中。该树结构使系统能够清晰识别当前活跃的候选行动，并从排练树中检索对应的预设论据和强度分数，为草稿生成提供策略依据。

### 语音时间控制器（Speech Time Controller）

为满足辩论中严格的时间限制，TreeDebater 采用轻量级文本转语音模型 **FastSpeech**（Ren et al., 2020）估算陈述的语音时长，并通过二分搜索迭代修订语句，使其落入合理的时间区间 $[t_l, t_r]$（Section 3.5）。这解决了基线方法（如 **Agent4Debate**，Zhang et al., 2024）因粗略字数估算而频繁超时或字数不足的问题。

### 模拟观众反馈（Simulated Audience Feedback）

TreeDebater 从人类辩论数据集中检索辩论流树，构建模拟观众，对生成的草稿提供多维度反馈，涵盖逻辑流、受众意识、证据使用和主张清晰度等方面（Section 3.4）。该反馈用于进一步修订陈述，提升说服力。需注意，模拟观众的覆盖面和代表性受限于检索数据集，可能影响对真实观众反应的模拟效果。

## 实验与关键发现

### 主实验结果

TreeDebater 在两种骨干模型（Gemini-2.0-flash 与 DeepSeek-V3）上均显著优于基线 Agent4Debate（Zhang et al., 2024），验证了树结构规划与时间控制策略的有效性。

**阶段级头对头评估（Table 1）。** 在固定辩论上下文下，评估者同时对两方陈述进行说服力评分（1-5分）。DeepSeek 骨干下，TreeDebater 的平均说服力从 3.47 提升至 4.01（+15.6%）；Gemini 骨干下，TreeDebater 在 11/12 个阶段对比中胜出，胜率约为基线的 1.5 倍（DeepSeek 下为 2.5 倍）。需注意，当双方表现均较好时，评估者更易依赖对动议的固有信念，导致区分度下降。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_E1hbqtHrvg/figures/002_Table_1.jpg]]
*Table 1: Scalar persuasiveness score and win rate in head-to-head human evaluation. A higher score indicates the statement is more persuasive. Win:Tie:Lose indicates the number of cases that TreeDebater wins, gets a tie, or loses in the pairwise comparison. The standard deviation results are put in Table 7 in the appendix because of the length limit. Table 2: End-to-End human evaluation result. The score in each stage indicates how persuasive the statement is. Opinion Shift Win indicates the percentage of votes that shift towards its stance after the debate. We ignore the percentage of Tie here*

**辩论级端到端评估（Table 2）。** 以“意见转变胜率”（Opinion Shift Win）衡量辩论后观众立场向辩手方向偏移的比例。Gemini 骨干下，TreeDebater 的意见转变胜率从 0.13 提升至 0.46（3.5 倍）；DeepSeek 骨干下从 0.30 提升至 0.40（+10 个百分点）。该指标直接反映辩论对真实观众信念的实际影响力。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_E1hbqtHrvg/figures/003_Table_2.jpg]]

**公平性保障。** 两种方法使用相同的骨干 LLM 和 Tavily API 进行证据检索，TreeDebater 沿用 Agent4Debate 的阶段专用提示模板，仅增加树信息用于规划。阶段级评估随机化陈述版本顺序以消除顺序偏差；辩论级评估通过交换立场取平均分消除先验立场偏见。仅使用格式和时间均有效的辩论进行人工评价——TreeDebater 始终满足格式与时间要求，基线因超时或格式错误被过滤或硬性截断（Table 6）。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_E1hbqtHrvg/figures/015_Table_6.jpg]]
*Table 6: Percentage of valid debate statements. Format Validity is the percentage of the debate competitions where all statements have the correct format. Time validity is the percentage of the statements that meet the time constraint before the hard cut*

### 消融分析

消融实验（Table 3）系统剥离了两个核心树结构，揭示其各自的贡献：

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_E1hbqtHrvg/figures/004_Table_3.jpg]]
*Table 3: Ablation Studies on Stage-level Head-to-Head Human Evaluation*

- **移除排练树（w/o Rehearsal Tree）：** Opening 说服力从 3.50 降至 3.00，Rebuttal 从 3.50 降至 3.25，Closing 从 3.75 降至 3.50。排练树对开场阶段的贡献最大，因为此时辩手最依赖预先准备的论点强度评估。
- **进一步移除辩论流树（w/o both trees）：** Opening 和 Rebuttal 分数进一步降至 3.00，表明辩论流树对维持辩论中的动态跟踪和策略选择不可或缺。

**动作多样性分析（Figure 2）。** 在反驳阶段，TreeDebater 展示了更接近人类专家的动作分布——攻击兼反驳（attack & rebut）、单独攻击、单独强化各占显著比例。移除辩论流树后，动作多样性明显下降，趋于单一化。这验证了辩论流树为 LLM 提供了实时状态感知，使其能像人类辩手一样根据辩论态势灵活选择策略。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_E1hbqtHrvg/figures/006_Figure_2.jpg]]
*Figure 2: Action distribution in the rebuttal stage. We extract the Debate Flow Tree from human debates and categorize the distribution of actions. The actions are less diverse in the baseline and TreeDebater w/o T _ { d } Figure 3: Percentage of actions that can be found in the Rehearsal Trees. The Rehearsal Trees of both sides contribute to the hit rate*

**排练树预演命中率（Figure 3）。** 超过半数的候选行动已在排练树中被预先生成，说明排练树能有效预测对手的攻击方向，为辩手提供充足的准备时间。

### 关键机制分析

TreeDebater 的性能提升可归因于三个因果路径：

1. **前瞻性准备（排练树）：** 通过极小极大式递归强度计算（Eqn 2），辩手在辩论前即可评估每个主张的抗攻击能力，优先选择强度更高的论点。这直接提升了开场阶段的说服力。
2. **动态策略选择（辩论流树）：** 实时跟踪所有主张、攻击与防御的树状关系，使辩手能从候选行动中检索预演论据并做出多样化的战术选择。这在反驳阶段尤为关键。
3. **时间约束满足（语音时间控制器）：** 基于 FastSpeech 的精确语音时长估算和二分搜索迭代修订，确保陈述始终符合严格的时间限制。基线方法常因超时被硬性截断，导致陈述不完整（Table 6 显示基线 Closing 阶段时间有效率仅 5.8%-13.5%）。

### 局限与失效模式

- **奖励模型精度有限：** 在 Kialo 数据集上训练的 LLaMA 奖励模型准确率有限（支持影响力 0.67，反驳影响力 0.72），可能影响排练树中强度分数计算的可靠性。
- **模拟观众的覆盖偏差：** 模拟观众反馈依赖于从人类辩论数据集检索的流树，其代表性和覆盖面可能限制对真实观众反应的模拟效果。
- **区分度衰减：** 当双方表现均较好时，评估者更依赖固有信念而非辩论策略本身，导致阶段级对比的区分度下降。这一效应在 Gemini 骨干的部分阶段中可见。
- **对手行为预测范围：** 排练树当前假设对手采取对称策略；对于非对称或非常规攻击路径的预测能力有限，这可能限制其在更复杂辩论场景中的鲁棒性。

## 定位与知识库关联

### 1. 与基线方法的关系

TreeDebater 的核心对比基线是 **Agent4Debate**（Zhang et al., 2024），一个先进的多智能体辩论框架。两者的关键差异体现在四个结构性创新上：

**排练树（Rehearsal Tree）vs. 无前瞻规划**：Agent4Debate 未包含任何形式的前瞻性树结构，其辩论策略依赖于 LLM 的即时推理。TreeDebater 则在辩论前为每个主要主张构建排练树，通过自顶向下生成潜在反驳并自底向上计算 k 步强度分数（Eqn 1–2），模拟对手的最优攻击路径。这一差异的因果机制在于：排练树将“预测对手行为”这一隐性认知过程显式化为可检索的结构化知识，使 LLM 在时间压力下仍能做出经过预评估的决策。

**辩论流树（Debate Flow Tree）vs. 顺序记录**：Agent4Debate 依赖顺序记录或无显式状态跟踪，难以在复杂辩论中维持对全局交互状态的认知。TreeDebater 的辩论流树以树结构实时记录所有主张、攻击与防御，提取候选行动并检索预演论据。这一设计的瓶颈突破点在于：辩论流树将非结构化的对话历史转化为可导航的行动空间，使策略选择从“基于记忆的模糊判断”升级为“基于结构的精确检索”。

**语音时间控制器（Speech Time Controller）vs. 粗略字数估算**：Agent4Debate 使用粗略的字数估算控制时间，常导致超时或不足。TreeDebater 采用 FastSpeech（Ren et al., 2020）进行精确语音时长估算，并通过二分搜索迭代修订语句以符合严格时间限制。这一改进解决了竞争性辩论中“时间约束刚性”与“生成质量弹性”之间的矛盾。

**模拟观众反馈（Simulated Audience Feedback）vs. 无反馈**：Agent4Debate 未使用模拟观众反馈。TreeDebater 基于检索的人类辩论流树构建模拟观众，提供针对逻辑流、受众意识、证据使用和主张清晰度的多维度反馈。这一模块填补了“缺乏客观奖励信号”这一核心瓶颈——在真实辩论中，说服力的最终裁判是观众，而非辩论对手。

### 2. 方法适用边界

TreeDebater 的设计假设与适用范围如下：

- **辩论形式**：适用于有明确立场对立、回合制交替发言的竞争性辩论。当前验证集中于开篇陈述、反驳和总结陈述三阶段格式，其在更复杂的交叉质询（cross-examination）或自由辩论形式中的表现尚待验证。
- **领域覆盖**：实验使用的 13 个动议涵盖经济、金融、健康、科学、技术、文化和教育领域（Table 5），但所有动议均来自 OpentoDebate、New York Times 等公开辩论平台，其在高度专业化领域（如法律辩论、学术答辩）的迁移能力未经验证。
- **语言与模态**：当前仅验证了英文文本辩论。语音时间控制器虽使用了 TTS 模型估算时长，但实际输出仍为文本，不涉及语音生成或韵律控制。
- **对手假设**：排练树假设对手会采取最大化其效用的攻击策略（minimax 视角），这一假设在面对非对称策略或刻意误导性辩论时可能失效。

### 3. 局限性与失败模式

TreeDebater 存在以下已验证或潜在的局限性：

**区分度衰减**：当辩论双方表现均较好时，人工评估者更容易依赖个人对动议的固有信念而非辩论策略本身进行判断，导致阶段级对比的区分度下降。这一现象在标注者间一致性仅为 60.7% 的数据中有所体现。

**奖励模型精度有限**：排练树的强度分数依赖两个基于 LLaMA-3.2-3B-Instruct 训练的奖励模型，其在 Kialo 数据集上的准确率有限——支持影响力评分准确率为 0.67，反驳影响力评分准确率为 0.72。这一精度瓶颈可能影响排练树中节点强度计算的可靠性，进而误导策略选择。

**模拟观众的覆盖偏差**：模拟观众反馈依赖于从人类辩论数据集中检索的流树，其覆盖面和代表性可能无法充分模拟真实观众的多样性。当辩论动议涉及特定文化背景或小众领域时，检索到的历史流树可能缺乏相关性。

**对手行为预测的局限性**：排练树的前瞻深度受限于预设的最大深度 L 和生成式 LLM 的推理能力。实验显示超过半数的候选行动确实被排练树预见到（Figure 3），但仍有相当比例的行动未被覆盖，表明当前方法无法预测所有可能的对手策略。

### 4. 开放问题

- 排练树能否改进以预测更广泛的对手行动，包括非对称策略和刻意误导性论证？当前的自顶向下生成范式可能系统性地遗漏某些攻击路径。
- 模拟观众反馈机制在更复杂的辩论形式（如议会制辩论、政策辩论）或真实比赛环境中的通用性如何？其依赖于检索历史流树的范式是否可扩展至未见过的辩论格式？
- 如何进一步平衡陈述中的情绪语气以满足不同观众偏好？当前工作主要关注逻辑结构和证据使用，对情感说服维度的建模尚不充分。
- 语音时间控制器能否推广至其他对语音长度敏感的生成任务，如演讲生成、教学视频脚本等？其核心的二分搜索迭代修订策略是否适用于更长的生成内容？

## 原文 PDF

![[paperPDFs/ICLR_2026/Strategic_Planning_and_Rationalizing_on_Trees_Make_LLMs_Better_Debaters.pdf]]
