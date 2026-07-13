---
title: "Do LLM Agents Know How to Ground, Recover, and Assess? Evaluating Epistemic Competence in Information-Seeking Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Do_LLM_Agents_Know_How_to_Ground_Recover_and_Assess_Evaluating_Epistemic_Competence_in_Information_Seeking_Agents.pdf
project_link: null
code_link: https://github.com/SHAO-Jiaqi757/SeekBench
openreview_forum_id: r0L9GwlnzP
aliases:
- Do_LLM_Agents_Kn
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将评测维度从单一的最终答案指标（如Exact Match, F1）扩展为过程级的认知能力指标——扎根推理质量（RQI）、证据恢复函数（ERF）和校准误差（CE），可揭示传统评测无法暴露的认知薄弱环节。"
primary_logic: "通过系统标注智能体的多轮搜索-推理轨迹，并定义证据状态（Evidence State），可对扎根性、恢复性和校准性三个核心认知能力进行可操作的量化，发现RL训练智能体虽能提高答案正确性和校准能力，却损害了扎根推理质量，且不同智能体在信息综合与证据搜集上各有专长，可通过智能体合成发挥互补优势。"
claims:
- "Few-shot 提示在扎根推理质量 (RQI) 上达到 0.27，高于所有经 RL 训练的智能体，揭示答案准确率与推理质量存在脱节。"
- "RL 训练显著降低过度自信回答比例（从 63.1% 降至 35.3%），并将校准误差降至 0.309，但在计划形成和状态评估上依然薄弱。"
- "SEARCH-R1 作为合成器在利用其他智能体的证据时带来平均 +2.61 F1 的提升，表明其信息综合能力强且回答保守，揭示过程能力可模块化复用。"
- "7 QA Benchmarks 上 Overall F1 = ASEARCHER 39.77%"
---

# Do LLM Agents Know How to Ground, Recover, and Assess? Evaluating Epistemic Competence in Information-Seeking Agents

> [!tip] 核心洞察
> 通过系统标注智能体的多轮搜索-推理轨迹，并定义证据状态（Evidence State），可对扎根性、恢复性和校准性三个核心认知能力进行可操作的量化，发现RL训练智能体虽能提高答案正确性和校准能力，却损害了扎根推理质量，且不同智能体在信息综合与证据搜集上各有专长，可通过智能体合成发挥互补优势。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LLM智能体是否懂得扎根、恢复与评估？信息检索智能体认知能力评测 |
| 英文题名 | Do LLM Agents Know How to Ground, Recover, and Assess? Evaluating Epistemic Competence in Information-Seeking Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=r0L9GwlnzP) · [GitHub](https://github.com/SHAO-Jiaqi757/SeekBench) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SeekBench |
| Dataset | 7 QA Benchmarks, Cross-agent Synthesis |

> [!tip] 效果简介
> - 7 QA Benchmarks 上，Overall F1 为 ASEARCHER 39.77%，对比 Base (Qwen-2.5-7B) 33.50%，变化 +6.27%。
> - 7 QA Benchmarks 上，Overconfident Answering Rate 为 RL-trained agents 0.353，对比 Base model 0.631，变化 -0.278 (↓44%)。
> - 7 QA Benchmarks 上，Reasoning Quality Index (RQI) 为 Few-shot 0.27，对比 Search-R1 0.08，变化 +0.19。

## 概要

当前信息寻求型LLM智能体的评测体系存在一个关键盲区：主流评测仅关注最终答案的正确性（如Exact Match、F1），却忽视了智能体在推理过程中是否真正基于证据进行思考、能否从低质量信息中恢复、以及是否根据证据充分性合理决策是否回答。这导致高分背后隐藏着大量未经证实的推理和过早回答等认知缺陷。

**核心瓶颈**：答案正确性与过程认知质量之间存在脱节。同一正确答案可能对应截然不同的推理过程——智能体可能忽略冲突信源、在证据模糊时仓促作答，也可能主动识别歧义、通过精炼搜索获取充分证据后再给出答案。传统指标无法区分这两种过程。

**方法定位**：本文提出SeekBench，首个面向LLM搜索智能体的过程级认知能力评测框架。其核心思路是将评测维度从单一答案指标扩展为三个可操作化的认知能力指标：
- **扎根推理质量（RQI）**：衡量推理步骤被证据支持的比例；
- **证据恢复函数（ERF）**：衡量智能体从低质量证据中恢复到充分证据状态的效率；
- **校准误差（CE）**：衡量智能体回答行为与理想策略（仅在证据充足时回答）的偏差。

为支持大规模评测，SeekBench构建了LLM-as-Judge自动化标注流水线（基于GPT-4.1-mini），在190条专家标注轨迹上验证了与人类的高度一致性（Cohen's κ > 0.7），并以此对8个智能体变体在7个QA基准上的28,493条轨迹进行了系统评测。

**决定性发现**：

1. **答案准确率与推理质量脱节**：Few-shot提示在扎根推理质量（RQI=0.27）上显著高于所有经RL训练的智能体（如Search-R1仅0.08），尽管RL智能体的最终F1更高。RL训练虽提升了答案正确性和校准能力（过度自信回答比例从63.1%降至35.3%，校准误差降至0.309），却损害了扎根推理质量。

2. **认知能力可模块化复用**：在智能体合成实验中，Search-R1作为合成器利用其他智能体搜集的证据时，带来平均+2.61 F1的提升，表明信息综合能力强的智能体可弥补证据搜集型智能体的不足，过程能力具有互补性。

3. **推理类型存在结构性弱点**：信息综合步骤在充分证据下扎根性最强，而计划形成和状态评估即便在证据充足时扎根性也显著偏低，揭示当前智能体在规划与自我监控环节存在普遍短板。

**方法谱系与知识库定位**：SeekBench在评测粒度上区别于仅关注最终答案的传统QA评测，在证据利用率上引入了证据状态的条件化评估，在可扩展性上以LLM-as-Judge替代纯人工评判。其评测对象涵盖基座模型（**Qwen-2.5-7B-Instruct**，Qwen et al., 2024）、少样本提示策略（Few-shot、CoT、ReAct）以及RL训练的搜索智能体（**SEARCH-R1**，Jin et al., 2025；**RESEARCH**，Chen et al., 2025；**ASEARCHER**，Gao et al., 2025；**DEEPRESEARCHER**，Zheng et al., 2025），为信息寻求型智能体的认知能力提供了系统性的诊断工具。

### 信息寻求型LLM智能体的崛起与评测盲区

大型语言模型（LLM）驱动的搜索智能体正被广泛部署于开放域问答、事实核查和深度研究等场景。这些智能体通过多轮“搜索-推理”循环与外部环境交互：每一轮先进行内部推理（$r_t$），再发起搜索查询（$s_t$），获取证据（$e_t$），最终给出答案（$a_T$）。当前主流的评测范式——无论是**Qwen-2.5-7B-Instruct**基座模型、**SEARCH-R1**（Jin et al., 2025）、**RESEARCH**（Chen et al., 2025）、**ASEARCHER**（Gao et al., 2025）还是**DEEPRESEARCHER**（Zheng et al., 2025）等RL训练变体——几乎无一例外地仅以最终答案的正确性作为评判标准（如Exact Match、F1）。

这一做法存在根本性盲区：**答案正确并不等于推理过程可靠**。如Figure 1所示，两个智能体对同一问题都给出了正确答案“455,000”，但过程质量天差地别——差的过程中智能体无视冲突信息源、未能识别模糊性、在证据不充分时过早作答；好的过程则识别了模糊性、通过精炼搜索获取最新官方数据、仅在证据充足后才回答。仅凭答案指标，二者将被等同视之。

### 核心瓶颈：答案指标掩盖了认知缺陷

这一评测盲区背后的深层瓶颈在于：**现有评测体系完全忽视了智能体在信息寻求过程中的认知能力（epistemic competence）**。具体而言，三个关键维度长期未被系统量化：

1. **扎根性（Groundedness）**：智能体的推理步骤是否真正基于检索到的证据，还是依赖内部先验知识进行“伪装推理”？
2. **恢复力（Recovery）**：当检索到低质量或模糊证据时，智能体能否通过调整搜索策略逐步恢复至充分证据状态？
3. **校准性（Calibration）**：智能体是否在仅有充分证据时才作答，还是在证据不足时过早给出答案（过度自信），或在证据充足时仍拒绝回答（过度谨慎）？

高分背后隐藏着大量未经证实的推理和过早回答等认知缺陷——这是仅关注最终答案指标的评测体系无法暴露的。

### 现有方法的局限性

当前评测方法在三个关键维度上存在结构性不足：

- **评测粒度粗**：仅关注最终答案正确性（Exact Match、F1），无法区分“蒙对”与“基于证据推理对”的本质差异。
- **证据利用率缺失**：未对检索到的证据状态进行区分——证据是清晰还是模糊？是充分还是不足？缺乏对证据质量的细粒度建模，导致无法评估智能体在不同证据条件下的行为差异。
- **可扩展性差**：依赖专家人工评判虽然可靠，但面对数万条多轮轨迹时成本过高，难以规模化。

### 本文动机：从答案评测到过程认知评测

针对上述缺口，本文提出**SeekBench**——首个面向LLM搜索智能体的过程级认知能力评测框架。其核心思路是：**将评测维度从单一的最终答案指标扩展为过程级的认知能力指标**，通过系统标注智能体的多轮搜索-推理轨迹，并定义证据状态（Evidence State），对扎根性、恢复性和校准性三个核心认知能力进行可操作的量化。

这一转变使得评测不仅能回答“智能体答对了吗”，更能回答“智能体是如何答对的”——其推理是否扎根于证据、能否从信息困境中恢复、是否在恰当的时机做出回答决策。通过揭示这些过程级的认知薄弱环节，SeekBench为智能体的诊断与改进提供了传统答案指标无法提供的细粒度信号。

## 核心方法与创新机理

SeekBench 的核心创新在于将信息寻求型 LLM 智能体的评测从“只看最终答案”转变为“审视认知过程”，并通过一套可规模化、可量化的指标体系，首次系统性地揭示了答案正确率背后隐藏的认知缺陷。

### 1. 评测粒度的根本转变：从答案指标到过程级认知指标

传统评测体系以最终答案的正确性（如 Exact Match、F1）为唯一标准，这种粗粒度指标无法区分“猜对”与“真懂”——两个智能体可能给出相同的正确答案，但一个在推理过程中无视矛盾证据、过早作答，另一个则通过精细搜索、确认证据充分后才给出回答（Figure 1）。SeekBench 将评测粒度从单一的答案指标扩展为三个过程级认知能力指标：

- **扎根推理质量（Reasoning Quality Index, RQI）**：衡量推理步骤是否被检索到的证据所支持；
- **证据恢复函数（Evidence Recovery Function, ERF）**：刻画智能体从低质量证据中恢复到充分证据状态的效率；
- **校准误差（Calibration Error, CE）**：评估智能体是否根据证据充分性合理决策“何时回答”。

这一转变的核心因果机制在于：答案正确率是认知能力的滞后且混杂的代理变量，而过程级指标直接观测智能体在信息处理链条各环节的认知行为，从而暴露了传统评测无法捕捉的薄弱环节——例如 Few-shot 提示在 RQI 上达到 0.27，显著高于所有 RL 训练智能体（Search-R1 仅 0.08），但其答案准确率却并非最高，揭示出答案正确率与推理质量之间存在脱节（Figure 3）。

### 2. 证据状态的形式化：为过程评测建立可操作的锚点

SeekBench 的第二个关键创新是引入**证据状态（Evidence State）**概念，将智能体每轮检索到的信息质量形式化为可计算的变量：

$$E_{i,t} := C_{i,t} + Q_{i,t}$$

其中 $C_{i,t} \in \{0,1\}$ 表示证据清晰度（信息是否明确、无歧义），$Q_{i,t} \in \{0,1\}$ 表示证据充足性（信息是否足以回答问题）。二者之和将证据状态划分为三个等级：$E=0$（差）、$E=1$（部分）、$E=2$（充分）。这一设计的核心价值在于为所有认知指标提供了**条件化评估的基准**——RQI 可按证据状态分解为 $\mathrm{RQI}_i = \sum_{k=0}^{2} \mathbb{P}(E=k) \times \mathbb{E}[G \mid E=k]$，从而区分“推理质量差是因为证据不足”还是“有充分证据却不会用”；CE 则以理想策略 $\pi^*(k) = \mathbb{I}[k=2]$（仅在证据充分时回答）为参照，精确量化智能体的过度自信或过度谨慎程度。

相较于以往仅靠专家人工评判、难以规模化的过程评估方法，SeekBench 通过 LLM-as-Judge 自动化标注流水线（基于 GPT-4.1-mini）实现了大规模部署，且与人类专家标注的一致性达到 $\kappa > 0.7$（Figure 6），在成本-信度帕累托前沿上取得最优平衡（Figure 7, Table 4）。

### 3. 揭露 RL 训练的认知代价：校准能力提升与扎根推理下降的逆向关系

SeekBench 最反直觉的发现是：**RL 训练虽然显著降低了过度自信回答比例（从 63.1% 降至 35.3%）并将校准误差降至 0.309（Table 3），却损害了扎根推理质量**——Few-shot 提示的 RQI（0.27）高于所有 RL 训练智能体。这一现象揭示了一个深层瓶颈：当前 RL 训练的奖励信号主要优化答案正确性，可能鼓励智能体在证据不充分时“谨慎不答”（提升校准），但并未有效激励其在推理过程中严格依据证据进行思考（扎根性下降）。此外，即便在证据充分（$E=2$）的条件下，所有模型在**计划形成（Plan Formation）**和**状态评估（State Assessment）**上的扎根性仍显著偏低（RQI < 0.2），而在**信息综合（Information Synthesis）**上相对较强（Figure 3, Figure 11），表明当前智能体的认知短板具有类型特异性。

### 4. 认知能力的模块化复用：智能体合成揭示互补潜力

SeekBench 进一步探索了认知能力是否可跨智能体模块化复用——将一个智能体作为“证据搜集者”（Producer），另一个作为“答案合成者”（Synthesizer）。结果显示，**SEARCH-R1 作为合成器在利用其他智能体的证据时带来平均 +2.61 F1 的提升**（Table 7），这表明其信息综合能力强且回答保守，能够有效利用他人搜集的证据。这一发现指向一个开放方向：模块化智能体架构（分别负责证据搜集、推理综合与决策）可能弥补单一智能体的认知短板，同时缓解扎根推理与答案校准之间的逆向关系。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_r0L9GwlnzP/figures/002_Table_1.jpg]]
*Table 1: Epistemic competencies and associated metrics. Each competency is quantified by a specific metric calculated from annotated features within the agent’s trace (shown in the rightmost column), enabling systematic evaluation of reasoning quality, recovery behavior, and evidence-aligned decision-making*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_r0L9GwlnzP/figures/020_Figure_9.jpg]]
*Figure 9: Annotation schema overview with definitions and examples. Abbreviations: Def=Definition, Ex=Example, G=Grounded, NG=Not Grounded, Suff=Sufficient, Insuff=Insufficient*

SeekBench 的整体流程围绕一个核心主张展开：**答案正确性不等于认知能力**。传统评测仅以 Exact Match 或 F1 作为终点指标，而 SeekBench 将评测粒度下探至智能体的多轮搜索-推理轨迹内部，建立了一套从标注到指标计算再到大规模部署的完整流水线。

### 流水线总览

SeekBench 的评测流水线由五个核心模块串联而成：

1.  **标注模式构建与验证（Annotation Schema Construction）**
    通过三轮专家迭代标注，从 190 条智能体轨迹（超过 1,800 步）中归纳出 8 个稳定标注字段，涵盖功能类型（搜索、推理、证据）与认知质量属性。字段间信度低于 0.5 的候选特征被裁剪或合并，确保模式可操作且可靠（Cohen's κ > 0.8）。

2.  **认知能力定义（Epistemic Competency Definition）**
    基于潜在构念推断，将智能体的过程级认知能力形式化为三个可测量的维度：**扎根性**（推理是否基于检索证据）、**恢复力**（能否从低质量信息中重新搜集充分证据）和**校准性**（是否仅在证据充足时作答）。三者共同构成 SeekBench 的评测靶点，其定义与对应指标见表 1。

3.  **指标可操作化（Metrics Operationalization）**
    将三个认知维度量化为具体数值指标（见 Table 1）：
    - **证据状态** $E_{i,t} := C_{i,t} + Q_{i,t}$，由清晰度 $C$ 与充足性 $Q$ 之和决定，取值为 0（差）、1（部分）、2（良好）。
    - **推理质量指数** $\mathrm{RQI}_{\mathrm{model}} := \mathbb{E}_{i\in\mathcal{I}}[\mathrm{RQI}_i]$，衡量所有轨迹中推理步骤被证据支持的平均比例。
    - **证据恢复函数** $\mathrm{ERF}(t) := \frac{1}{N}\sum_{i=1}^{N}\mathbb{I}(T_{\mathrm{recover},i}\leq t)$，刻画截至第 $t$ 轮已获得充分证据的轨迹累计比例。
    - **校准误差** $\mathrm{CE} := \mathbb{E}_{i\in\mathcal{I}}[\mathrm{CE}_i]$，其中 $\mathrm{CE}_i := \sum_{k=0}^{2}\mathbb{P}(E_{i,t}=k)|\mathbb{P}(\text{answer}_{i,t}=1|E_{i,t}=k)-\pi^*(k)|$，测量智能体回答行为与理想策略（仅在 $E=2$ 时回答）的期望偏差。

4.  **LLM-as-Judge 自动化流水线**
    为突破人工标注的规模瓶颈，引入 GPT-4.1-mini 作为自动化评委。该模型在标注信度上与人类专家达到高度一致（κ = 0.731），且单条轨迹成本仅 $0.0087、耗时 2.48 秒，位于成本-信度帕累托前沿，使大规模过程级评测成为可能。

5.  **大规模评测执行**
    在 7 个 QA 基准上对 8 个智能体变体（含 Base、Few-shot、4 种 RL 训练智能体及 CoT/ReAct 提示策略）进行评测，共收集 28,493 条轨迹，系统计算 RQI、ERF、CE 三维指标。

### 输入输出流

- **输入**：智能体在问答任务中产生的多轮轨迹 $\mathcal{T} = \langle \tau_1, \tau_2, \dots, \tau_T \rangle$，其中非最终轮 $\tau_t = \langle r_t, s_t, e_t \rangle$ 包含推理、搜索与证据，最终轮 $\tau_T = \langle r_T, a_T \rangle$ 包含推理与答案。
- **处理**：LLM 评委对每条轨迹的每一步进行功能类型与质量属性标注，据此计算证据状态序列，再聚合为三维认知指标。
- **输出**：每个智能体的 RQI（含按推理类型细分）、ERF 曲线（含按操作类型细分的恢复效率）、CE（含过度自信/过度谨慎分解），以及与传统 F1 的对比分析。

### 与传统评测的关键差异

| 评测维度 | 传统评测 | SeekBench |
|---------|---------|-----------|
| 评测粒度 | 仅最终答案正确性 | 过程级认知指标（RQI, ERF, CE） |
| 证据利用 | 未区分证据状态 | 基于证据状态（E=0/1/2）条件化评估 |
| 可扩展性 | 依赖专家人工评判 | LLM-as-Judge 自动化流水线，与人类高度一致 |

Figure 2 展示了这一标注模式的整体结构：每条轨迹被分解为搜索步骤（检索信息）、推理步骤（处理证据并指导调查）和证据步骤（捕获检索信息的质量与清晰度），三者交织形成可被系统评测的认知过程全景。

### 3.1 标注模式构建与验证

SeekBench 的标注模式通过三轮专家迭代标注构建，初始 12 个候选标注字段经信度筛选（Cohen's κ < 0.5 则剪枝或合并）后保留 8 个精确定义的特征。标注涵盖两个核心维度：

- **功能类型（Functional Type）**：将智能体每一步行为归类为搜索步骤（Search）、推理步骤（Reasoning）或证据步骤（Evidence），推理步骤进一步细分为信息综合（Information Synthesis）、计划形成（Plan Formation）和状态评估（State Assessment）。
- **质量属性（Quality Attribute）**：评估每一步的认知健全性，包括推理是否扎根于证据（Groundedness）、检索到的证据是否清晰（Clarity）与充足（Sufficiency）。

验证阶段，GPT-4.1-mini 作为 LLM 评委与人类专家标注的一致性达到 Cohen's κ = 0.731，GPT-5 达到 κ = 0.754，整体平均 κ = 0.811，表明自动化标注流水线可规模化部署。GPT-4.1-mini 以每条轨迹 $0.0087 和 2.48 秒的成本位于成本-信度帕累托前沿（Figure 7, Table 4），被选为大规模评测的默认评委模型。

### 3.2 证据状态定义

证据状态是 SeekBench 指标体系的基石，用于条件化地评估智能体行为。

**定义 3.1（证据状态 Evidence State）** 对第 $i$ 条轨迹的第 $t$ 轮，证据状态 $E_{i,t}$ 定义为清晰度 $C_{i,t}$ 与充足性 $Q_{i,t}$ 之和：

$$E_{i,t} := C_{i,t} + Q_{i,t}$$

其中：
- $C_{i,t} \in \{0, 1\}$ 表示该轮检索到的信息是否清晰、无歧义；
- $Q_{i,t} \in \{0, 1\}$ 表示该轮证据是否足以支撑回答；
- $E_{i,t} \in \{0, 1, 2\}$ 分别对应差（Poor）、部分（Partial）、好（Good）三种证据水平。

Table 2 以“Black Sabbath 乐队主唱是谁”为例展示了四种证据状态场景：当检索结果既模糊又不完整时 $E=0$；当仅有清晰度或仅有充足性时 $E=1$；当两者兼备时 $E=2$。

### 3.3 扎根推理质量指标

扎根性（Groundedness）衡量推理步骤的事实内容是否被检索证据所支持。对第 $i$ 条轨迹的第 $t$ 个推理步骤，二元扎根标签 $G_{i,t} \in \{0, 1\}$ 表示该步骤是否证据扎根。

**定义 3.2（轨迹级 RQI）** 第 $i$ 条轨迹的推理质量指数 $\mathrm{RQI}_i$ 为该轨迹所有推理步骤中扎根比例：

$$\mathrm{RQI}_i = \frac{1}{|S_i|} \sum_{t \in S_i} G_{i,t}$$

其中 $S_i$ 为该轨迹中所有推理步骤的索引集合。

**定义 3.3（模型级 RQI）** 模型级 $\mathrm{RQI}_{\mathrm{model}}$ 为所有评估轨迹上 $\mathrm{RQI}_i$ 的期望：

$$\mathrm{RQI}_{\mathrm{model}} := \mathbb{E}_{i \in \mathcal{I}}[\mathrm{RQI}_i]$$

为揭示扎根性的证据条件依赖性，$\mathrm{RQI}_i$ 可进一步分解为证据状态分布与条件扎根性的加权和：

$$\mathrm{RQI}_i = \sum_{k=0}^{2} \mathbb{P}_{t \in S_i}(E_{i,t}=k) \times \mathbb{E}_{t \in S_i}[G_{i,t} \mid E_{i,t}=k]$$

该分解使得分析者能够区分“推理质量差是因为证据不足”还是“即使有充分证据也无法扎根推理”两种根本不同的失败模式。

### 3.4 证据恢复函数

恢复力（Recovery）衡量智能体从低质量证据状态（$E \in \{0, 1\}$）逐步改善至充分证据（$E=2$）或给出正确答案的能力。

**定义 3.4（证据恢复函数 ERF）** 令 $T_{\mathrm{recover}, i}$ 为第 $i$ 条轨迹首次达到 $E=2$ 或给出正确答案的轮次，则证据恢复函数为截至第 $t$ 轮已恢复轨迹的累计比例：

$$\mathrm{ERF}(t) := \frac{1}{N}\sum_{i=1}^{N}\mathbb{I}(T_{\mathrm{recover}, i} \leq t)$$

由于轨迹长度不一且存在右删失数据（轨迹在恢复前即终止），论文采用 Kaplan-Meier 生存分析方法对恢复概率进行稳健估计。ERF 曲线的陡峭程度直接反映恢复效率——曲线越陡，智能体越能快速摆脱低质量证据困境。

### 3.5 校准误差

校准性（Calibration）衡量智能体的回答决策与证据充分性的对齐程度。理想策略 $\pi^*(k) = \mathbb{I}[k = 2]$ 规定：仅在证据充足（$E=2$）时回答，否则应继续搜索。

**定义 3.5（校准误差 CE）** 模型级校准误差为各轨迹校准误差的期望：

$$\mathrm{CE} := \mathbb{E}_{i \in \mathcal{I}}[\mathrm{CE}_i]$$

其中单条轨迹的校准误差为各证据状态下实际回答概率与理想策略的加权绝对偏差：

$$\mathrm{CE}_i := \sum_{k=0}^{2}\mathbb{P}(E_{i,t}=k)\left|\mathbb{P}(\text{answer}_{i,t}=1 \mid E_{i,t}=k) - \pi^*(k)\right|$$

该公式惩罚两类校准失败：在证据不足时过早回答（过度自信，Overconfident），以及在证据充足时仍拒绝回答（过度谨慎，Overcautious）。Table 3 将轨迹按这两种失败模式进行细分统计。

### 3.6 指标体系的模块化关系

三个认知指标形成互补的评估闭环：

- **RQI** 回答“推理过程是否基于证据”，聚焦推理步骤的内部质量；
- **ERF** 回答“能否从劣质信息中恢复”，聚焦搜索策略的动态效率；
- **CE** 回答“回答时机是否与证据水平匹配”，聚焦决策行为的校准程度。

三者共同覆盖了信息寻求型智能体“搜集证据—基于证据推理—根据证据决策”的完整认知链条，使得过程级缺陷可被定位到具体环节。例如，Figure 3 揭示 Few-shot 提示在 RQI（0.27）上全面优于 RL 训练智能体，但 Table 3 显示 RL 训练将过度自信回答率从 63.1% 降至 35.3%，表明 RL 优化了决策校准却损害了推理扎根性——这一矛盾仅在三维指标同时观测时才可被发现。

## 实验与关键发现

### 核心发现：答案正确性 ≠ 认知能力

SeekBench在7个问答基准上对8个智能体变体进行了大规模评测，共分析28,493条多轮搜索-推理轨迹。实验揭示了一个关键脱节：**高答案准确率并不等同于高认知能力**。如表5所示，经RL训练的ASEARCHER以39.77%的整体F1分数领先，但扎根推理质量（RQI）却仅为0.14，远低于Few-shot提示版本的0.27（图3左）。这一发现直接验证了本文的核心瓶颈——仅关注最终答案的评测体系会掩盖推理过程中的严重认知缺陷。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_r0L9GwlnzP/figures/021_Table_5.jpg]]
*Table 5: Overall F1 performance across agent variants. Trained agents consistently outperform the base model, with ASearcher achieving the highest score*

### 扎根性：RL训练损害推理质量

图3呈现了扎根推理质量的双维度分析。在模型级RQI上，Few-shot以0.27显著领先所有RL训练智能体，而SEARCH-R1仅为0.08，揭示**RL训练虽然提升了答案正确性，却系统性地削弱了推理对证据的依赖**。在推理类型细分中，所有智能体均表现出异质性弱点：

- **信息综合（Information Synthesis）** 是相对强项，ASEARCHER达到0.56，表明智能体在整合已获取信息方面具有一定能力。
- **计划形成（Plan Formation）** 和**状态评估（State Assessment）** 是所有模型的共同短板，所有智能体的RQI均低于0.2，即便在证据充足（E=2）的条件下（图11，附录F.2），这两类推理的扎根性依然显著偏低。

附录图10进一步揭示了证据条件化推理的差异：Base与Few-shot模型展现出最清晰的证据敏感性——当证据状态从E=1提升至E=2时，其预期扎根率从0.49升至0.64。相比之下，RL训练智能体在不同证据状态下的扎根性变化幅度较小，暗示其推理过程对证据质量的区分度不足。

### 恢复力：操作类型决定恢复效率

证据恢复函数（ERF）曲线（图4左）显示，不同智能体从低质量证据中恢复的速度存在显著差异。Kaplan-Meier生存分析被用于处理变长轨迹的右删失数据，确保恢复概率估计的鲁棒性。

更具操作性价值的发现来自操作类型的恢复效率分析（图4右）：**REFINE（搜索优化）和FOLLOW-UP（追问）操作能最快使智能体摆脱低证据状态**，其ERF曲线斜率显著高于其他操作类型。相比之下，REPEAT（重复搜索）操作几乎不带来证据改善，表明盲目重复检索是低效的恢复策略。这一发现为智能体的搜索策略设计提供了明确指引：应优先采用查询细化和信息追踪，而非简单重复。

### 校准性：RL训练降低过度自信但仍有盲区

表3呈现了校准误差的核心对比。Base模型表现出严重的过度自信——63.1%的轨迹在证据不充分时即给出回答。RL训练将这一比例大幅降至35.3%，并将整体校准误差从高位压缩至0.309。图5进一步说明，RL训练智能体在证据充足（E=2）时回答准确率达31.6%，而在无证据时仅为8.4%，展现出更合理的证据条件化回答行为。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_r0L9GwlnzP/figures/010_Table_3.jpg]]
*Table 3: Calibration Error Analysis. traces categorized as: calibration error, overconfident, or overcautious. Lower values indicate better calibration. RL-trained agents show the lowest overconfident answer rate and lowest CE. Bold indicates best performance*

然而，校准能力的改善并非全面。图14（附录）的证据条件化回答时机分析揭示了一个普遍问题：**所有模型在“是否已获得充足证据”和“是否已给出回答”之间缺乏清晰的时间分离**。理想情况下，已获得充足证据的轨迹（橙色曲线）应在未获得充足证据的轨迹（蓝色曲线）之前上升，但实际观测中两条曲线几乎同步，确认了广泛存在的过早回答行为。这表明当前RL训练的校准改善主要集中在减少极端过度自信，而非实现真正的证据对齐决策。

### 智能体合成：过程能力的模块化复用

表7的跨智能体合成实验验证了认知能力的模块化可复用性。实验将不同智能体分别作为证据搜集者（P）和答案合成器（S），测量合成器利用他人证据时的F1提升。核心发现：

- **SEARCH-R1作为合成器表现最优**，在所有证据源上平均带来+2.61 F1的提升，表明其信息综合能力强且回答保守，适合作为“决策层”。
- 不同智能体展现出互补性：某些智能体擅长证据搜集（高恢复力），而另一些擅长基于证据进行推理综合（高扎根性）。
- 合成效果并非简单叠加——当合成器与搜集器相同时，提升为零（基线），说明模块化组合能释放单一智能体无法实现的协同增益。

### 消融与鲁棒性验证

**标注模式验证**：通过三轮专家标注迭代，SeekBench的标注模式从初始12个候选字段精简至8个高信度特征，移除了Cohen's κ<0.5的低一致性字段。图6显示，GPT-4.1-mini与人类标注者在各字段上达到κ>0.7的一致性，GPT-5达到κ=0.754。表4的成本-信度分析表明，GPT-4.1-mini以$0.0087/条轨迹和2.48秒/条的成本位于帕累托前沿，适合大规模部署。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_r0L9GwlnzP/figures/013_Table_4.jpg]]
*Table 4: Per-trace cost and Inter-Annotator Agreement (IAA) for LLM Judges on 190 sampled traces. Token cost (in USD$ per trace), time cost (in seconds per trace), and IAA measured as Cohen’s κ with standard deviation. Models marked with † are Pareto-optimal*

**多工具场景泛化**：表9验证了标注模式在代码执行、复杂工作流等多种工具类型上的人类-LLM一致性，初步证明认知指标体系对多样化工具场景的适用性。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_r0L9GwlnzP/figures/031_Table_9.jpg]]
*Table 9: Human-LLM Agreement Across Diverse Tool Types. Scores for Type and Groundedness pertain to tool input actions (such as search queries), while Clarity and Sufficiency scores assess the tool output (i.e., the produced evidence)*

**基准清洗**：实验对七个基准数据集进行了系统清洗，移除了模糊不可答问题、数据污染实例以及仅凭模型内部知识即可回答的问题（Pass@3），确保证据状态仅反映检索质量，减少单一答案指标的评估偏差。

### 失败模式总结

1. **RL训练的逆向效应**：RL优化答案正确性的奖励信号，却导致智能体在推理过程中减少对证据的依赖（RQI下降），形成“高分低能”的认知空洞。
2. **计划与评估盲区**：所有智能体在形成搜索计划和评估当前证据状态时扎根性极低，表明元认知能力是当前LLM智能体的系统性短板。
3. **伪校准**：RL训练虽降低了极端过度自信，但智能体仍未实现真正的证据条件化决策——过早回答行为在所有模型中普遍存在（图14）。
4. **恢复策略低效**：智能体倾向于使用REPEAT等低效操作，而非REFINE和FOLLOW-UP等高效恢复策略，说明搜索行为的策略性不足。

## 定位与知识库关联

### 评测范式的迁移：从答案正确性到认知能力

SeekBench 的核心贡献在于将信息寻求型 LLM 智能体的评测从**最终答案正确性**（Exact Match、F1）迁移到**过程级认知能力**。传统评测中，一个智能体可能给出正确答案但推理过程完全未经证据支撑（如 Figure 1 所示），这种“高分低能”现象在现有指标下不可见。SeekBench 通过三个可操作的认知指标——扎根推理质量（RQI）、证据恢复函数（ERF）和校准误差（CE）——填补了这一空白。

这一范式迁移的关键操作是将推理过程**条件化于证据状态**（Evidence State, $E_{i,t} := C_{i,t} + Q_{i,t}$）。与仅看最终输出的评测不同，SeekBench 要求评估“在什么证据条件下做了什么推理、是否应该回答”，从而揭示智能体的认知薄弱环节。该方法在概念上借鉴了认知科学中的扎根认知（Grounded Cognition）和校准理论，但将其首次系统化地应用于 LLM 搜索智能体的过程评估。

### 与基线方法的定位关系

论文评测了八种智能体变体，形成清晰的方法谱系：

**基座模型与提示策略：**
- **Base**（Qwen-2.5-7B-Instruct, Qwen et al., 2024）：未经搜索训练的基座模型，代表“纯内部知识”基线。
- **Few-shot / CoT / ReAct**：基于提示工程的策略，不涉及参数更新。其中 Few-shot 在扎根推理质量上表现最优（RQI=0.27），但校准能力薄弱（过度自信回答率高达 63.1%）。

**RL 训练的搜索智能体：**
- **SEARCH-R1**（Jin et al., 2025）、**RESEARCH**（Chen et al., 2025）、**ASEARCHER**（Gao et al., 2025）、**DEEPRESEARCHER**（Zheng et al., 2025）：均基于 Qwen-2.5-7B 通过强化学习训练，具备多轮搜索-推理能力。这些方法在答案正确性上优于基座模型（ASEARCHER 达 39.77% F1，Base 为 33.50%），且校准能力显著改善（过度自信率降至 35.3%，CE 降至 0.309）。

**关键的逆向发现：** RL 训练在提升答案正确性和校准能力的同时，**损害了扎根推理质量**。Few-shot 的 RQI（0.27）显著高于所有 RL 智能体（如 Search-R1 仅 0.08）。这表明当前 RL 训练目标（如答案正确性奖励）并未鼓励智能体进行证据支撑的推理，智能体可能学会了“猜对答案”而非“基于证据推理”。

### 模块化能力与合成潜力

论文进一步揭示了不同智能体在认知子能力上的**互补性**：
- **信息综合**（Information Synthesis）是各智能体的相对强项（ASEARCHER 达 0.56 RQI），而**计划形成**（Plan Formation）和**状态评估**（State Assessment）是普遍短板（所有智能体 RQI < 0.2）。
- 在跨智能体合成实验中，**SEARCH-R1 作为合成器**（synthesizer）利用其他智能体搜集的证据时，平均带来 **+2.61 F1** 的提升，表明其信息综合能力强且回答保守，而 ASEARCHER 作为证据搜集器（producer）最为有效。这暗示模块化架构（分离证据搜集与推理综合）可能在实际部署中发挥互补优势。

### 自动化评估的技术路线

SeekBench 的可扩展性依赖于 **LLM-as-Judge 自动化标注流水线**。论文通过三轮专家标注（190 条轨迹，1800+ 步骤）构建并验证了标注模式，将初始 12 个标注字段精简为 8 个高信度特征（Cohen's κ > 0.5）。GPT-4.1-mini 作为评委与人类专家达到 κ=0.731 的一致性，且成本极低（$0.0087/trace, 2.48s），位于成本-信度的帕累托前沿。这一技术路线使大规模过程级评测（28,493 条轨迹）成为可能。

### 适用边界与局限

1. **任务范围受限：** 当前评估聚焦于问答任务，尽管在 GAIA 基准和多工具场景下做了初步验证（Table 8, Table 9），但对代码执行、复杂工作流等更多样化工具的认知能力泛化性仍需更多实证。工具使用分布显示搜索和访问操作占约 99%（Figure 15），其他工具类型覆盖不足。

2. **LLM-as-Judge 的鲁棒性边界：** 在高度模糊的推理判断上，LLM 评委与人类的一致性下降（κ ≈ 0.65-0.70）。这意味着在边缘案例中，自动化评估的可靠性需要人工复审兜底。

3. **指标间的张力未解决：** 论文揭示了 RQI 与答案正确率之间的逆向关系，但未提供缓解方案。如何在训练中同时优化扎根推理质量和最终答案准确性，是框架揭示但未闭合的核心问题。

4. **认知维度的覆盖：** 扎根性、恢复性和校准性三个维度虽已覆盖信息寻求的核心认知过程，但仍有其他维度（如信息源的批判性评估、推理链的逻辑一致性）未被量化。

### 开放问题

1. **多目标优化：** 能否通过多目标强化学习或训练技巧，同时提升 RQI 与最终答案正确率，缓解二者之间的逆向关系？这需要重新设计奖励函数，显式奖励证据支撑的推理步骤。

2. **模块化架构的实战验证：** 模块化智能体架构（分别负责证据搜集、推理综合与决策）能否在真实部署中有效结合，并弥补单一智能体的认知短板？合成实验提供了概念验证，但需要端到端的系统评估。

3. **认知维度的扩展：** 除扎根性、恢复性和校准性外，还有哪些认知维度（如信息源的权威性批判评估、不确定性表达的质量）可通过类似的过程级指标体系量化？

4. **RL 训练机制的诊断：** 为什么 RL 训练会损害扎根推理质量？是奖励信号的稀疏性问题，还是探索-利用的权衡导致智能体学会了“捷径”？这需要进一步剖析 RL 训练的中间过程。

## 原文 PDF

![[paperPDFs/ICLR_2026/Do_LLM_Agents_Know_How_to_Ground_Recover_and_Assess_Evaluating_Epistemic_Competence_in_Information_Seeking_Agents.pdf]]
