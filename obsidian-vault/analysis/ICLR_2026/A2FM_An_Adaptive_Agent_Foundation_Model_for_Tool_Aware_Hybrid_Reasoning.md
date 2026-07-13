---
title: "A$^2$FM: An Adaptive Agent Foundation Model for Tool-Aware Hybrid Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A2FM_An_Adaptive_Agent_Foundation_Model_for_Tool_Aware_Hybrid_Reasoning.pdf
project_link: null
code_link: null
aliases:
- AAFMF
- 2FAAFMTAHR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "引入任务感知路由器（Task-Aware Router），统一调度即时回答、推理和智能体三种执行模式，并通过自适应策略优化（APO）在强化学习中联合优化路由决策与轨迹生成，从而平衡准确率与计算成本。"
primary_logic: "采用“先路由后对齐”的两阶段训练框架：首先通过监督微调学习模式分类与条件轨迹生成，再通过APO强化学习引入基于成本正则化的自适应奖励，奖励在简单查询上优先选择即时模式，惩罚不必要的昂贵模式，实现准确且低成本的模式选择。"
claims:
- "A²FM在32B规模上在智能体任务（BrowseComp 13.4%）、推理任务（AIME25 70.4%）和通用任务（HLE 16.7%）上均达到同规模模型的最先进水平。"
- "自适应执行将每个正确回答的推理成本降至$0.00487，相比纯推理模式降低45.2%，相比纯智能体模式降低33.5%，在保持相当准确率的同时显著提升成本效率。"
- "消融实验表明，自适应奖励项使即时模式使用比例从50.2%提升至58.6%，而分数仅微降0.9点（54.7 vs 55.6），有效鼓励了简单查询的低开销解答。"
- "采用“先路由后对齐”的两阶段训练框架：首先通过监督微调学习模式分类与条件轨迹生成，再通过APO强化学习引入基于成本正则化的自适应奖励，奖励在简单查询上优先选择即时模式，惩罚不必要的昂贵模式，实现准确且低成本的模式选择。"
---

# A$^2$FM: An Adaptive Agent Foundation Model for Tool-Aware Hybrid Reasoning

> [!tip] 核心洞察
> 采用“先路由后对齐”的两阶段训练框架：首先通过监督微调学习模式分类与条件轨迹生成，再通过APO强化学习引入基于成本正则化的自适应奖励，奖励在简单查询上优先选择即时模式，惩罚不必要的昂贵模式，实现准确且低成本的模式选择。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | A²FM：一种面向工具感知混合推理的自适应智能体基础模型 |
| 英文题名 | A$^2$FM: An Adaptive Agent Foundation Model for Tool-Aware Hybrid Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3kvV1nfWVq) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | Adaptive Agent Foundation Model (A²FM) |
| Dataset |  |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

当前大语言模型（LLM）在能力上呈现明显分化：以推理为核心的长链模型缺乏工具调用能力，以智能体为核心的模型则深度推理较弱；且在大量简单查询上二者均存在“过度推理”或“过度调用工具”的现象，导致计算开销高、效率低下（Analysis truth: real_bottleneck）。

针对这一瓶颈，本文提出自适应智能体基础模型 **A²FM**（Adaptive Agent Foundation Model），在统一主干网络下集成**即时回答（instant）、推理（reasoning）和智能体（agentic）**三种执行模式，并引入**任务感知路由器**（Task-Aware Router）动态进行模式选择。模型采用“先路由后对齐”（route-then-align）的两阶段训练范式：首先通过监督微调学习模式分类与条件轨迹生成，再通过**自适应策略优化**（Adaptive Policy Optimization, APO）延展GRPO，在强化学习中联合优化路由决策与模式内轨迹。APO的核心在于设计了一个**成本正则化的自适应奖励**：对简单查询优先奖励即时模式，对非即时模式在成本维度施加惩罚，从而在准确率与计算效率之间寻求平衡（Analysis truth: causal_knob, core_insight）。

在主要结果上，A²FM在32B参数规模下取得了多项同尺寸模型最优：

- **智能体任务**：BrowseComp得分 13.4%（Abstract, Figure 1）；
- **推理任务**：AIME25得分 70.4%（Abstract, Figure 1）；
- **通用知识任务**：HLE得分 16.7%（Abstract）；
- 在智能体、推理与通用三个大类上综合排名分别位列第1、第2和第1（Figure 1）。

效率方面，自适应执行机制将每个正确回答的推理成本降至 **$0.00487**，相比纯推理模式降低45.2%，相比纯智能体模式降低33.5%，而准确率保持相当（Abstract, Figure 4b）。消融实验进一步证实，APO的自适应奖励项使简单查询的即时模式使用率从50.2%显著提升至58.6%，而综合分数仅微降0.9点（54.7 vs. 55.6），表明该方法有效抑制了不必要的昂贵模式，实现了低成本且准确的模式选择（Table 4）。以上结果表明，A²FM通过统一路由与自适应成本控制，成功缓解了LLM在能力分化与效率失衡上的核心矛盾。



当前大语言模型（LLM）的演进呈现出两种主要范式：以推理为核心的模型（如DeepSeek‑R1）擅长多步数学推导与逻辑链生成，却缺乏调用外部工具的智能体能力；以智能体为中心的模型（如DeepSeek‑V3.1）具备搜索、工具交互等功能，但在深层推理任务上表现较弱。这种分化不仅迫使用户在不同任务下切换模型，更暴露出一个关键的效率瓶颈——**无论查询复杂与否，模型往往会对简单问题执行“过度推理”或“过度调用工具”**，生成冗长的思维链或发起不必要的工具交互，导致推理成本高昂、延迟增加。例如，当强制所有查询都走纯推理或纯智能体模式时，每个正确答案的平均推理成本可达约$0.0089$，其中大量开销消耗在可以直接回答的简单查询上（Figure 4b）。

造成这一困境的深层次原因是，现有方法缺乏一种**查询自适应的执行选择机制**。理想情况下，模型应根据查询难度动态决定采用轻量即时回答、深度多步推理还是工具驱动的智能体操作。但主流做法要么将推理与智能体能力分开对齐（如Qwen3‑32B分别训练两种能力），要么仅通过长度正则化粗粒度地控制推理长度，无法实现精确、低开销的模式调度。

针对上述缺口，本文提出**自适应智能体基础模型A²FM（Adaptive Agent Foundation Model）**，其核心动机在于：在统一Transformer主干中同时集成即时（instant）、推理（reasoning）和智能体（agentic）三种执行模式，并通过一个可学习的**任务感知路由器（Task‑Aware Router）** 动态选择最经济的模式，从而在保持高准确率的同时大幅降低推理成本。A²FM的假设是，采用“先路由后对齐”的两阶段训练框架——先通过监督微调学会模式分类与条件轨迹生成，再通过自适应策略优化（APO）强化学习，在奖励中显式惩罚简单查询上不必要的昂贵模式——能够让模型自动为简单问题分配即时模式，而对复杂任务启用深度推理或工具调用。初步证据显示，该设计使每个正确答案的推理成本降至$\\$0.00487$，较纯推理模式降低45.2% ，较纯智能体模式降低33.5%，且在数学（AIME25 70.4%）、智能体（BrowseComp 13.4%）和通用知识（HLE 16.7%）等多样化基准上均达到同规模模型的最先进水平，为构建高效、自适应的基础智能体提供了可行路径。



## 核心方法与创新机理

现有大语言模型在能力上趋于极化：以推理为核心的模型（如 DeepSeek‑R1）缺乏工具调用能力，以智能体为核心的模型（如 DeepSeek‑V3.1）深度推理较弱，且两类模型在简单查询上均存在过度推理或过度调用工具的问题，导致高昂的计算开销。A²FM 的关键创新在于打破这种能力‑效率的权衡，通过以下三个相互协同的“变更槽位”实现统一：

1. **三模式统一主干与任务感知路由**
   与推理与工具调用松散耦合的基线不同，A²FM 在单个骨干网络中集成了即时回答（instant）、推理（reasoning）和智能体（agentic）三种执行模式 $\mathcal{M}$，并由可学习的任务感知路由器 $\pi_{\mathrm{route}}(m \mid x)$ 对查询 $x$ 动态选择模式 $m$。该路由器消除了此前方案中无统一调度、无法根据任务难度自适应切换的问题，使模型在简单查询上避免不必要的深度思考或工具调用，在复杂查询上自动调用最强模式（Figure 2, Section 3.1）。

2. **“先路由后对齐”的两阶段训练范式**
   Qwen3‑32B 等混合模型通过分离的对齐阶段分别训练推理与智能体能力，无法联合优化路由。A²FM 提出全新的训练管线：
   - **第一阶段（监督微调）**：利用 `<classification>` 标签学习模式分类与条件轨迹生成，要求模型根据所选模式 $m$ 生成一致的输出 $y \sim \pi_m(y \mid x)$（Section 3.2）。
   - **第二阶段（自适应策略优化，APO）**：将 GRPO 强化学习扩展为联合优化路由决策与模式内轨迹。APO 通过强制采样（forced rollouts）保证各模式充分探索，同时进行自适应采样（adaptive rollouts）以奖励正确的路由选择，避免模式欠采样（Section 3.3）。该策略优化使模型在单一过程中同时提升准确率与路由准确性。

3. **基于任务难度的自适应成本奖励**
   相比于仅基于准确率的二元奖励或简单长度正则化，APO 引入自适应奖励 $r_{\mathrm{adaptive}}$，显式编码准确率‑效率权衡：若选择非即时模式（推理或智能体），$r_{\mathrm{adaptive}} = 1 - p^{\alpha}$，其中 $p$ 为该查询在强制采样下的经验成功率（难度指标），$\alpha$ 为缩放因子；选择即时模式则奖励保持为 $1$。这一设计对简单查询上的昂贵模式施加惩罚，促使模型优先使用低开销的即时模式。消融实验表明，加入自适应奖励后，即时模式使用比例从 50.2% 提升至 58.6%，分数仅下降 0.9 点（Table 4），最终将每个正确的推理成本降至 $0.00487，比纯推理模式降低 45.2%，比纯智能体模式降低 33.5%（Figure 4b）。

上述三个变更槽位——执行模式整合、路由‑对齐训练范式、自适应成本奖励——共同构成了 A²FM 相对现有基线的决定性创新，使其在 32B 规模下在智能体（BrowseComp 13.4%）、推理（AIME25 70.4%）和通用任务（HLE 16.7%）上均达到同尺寸模型的最优水平，并率先在保持高准确率的同时大幅降低推理成本。



![[assets/figures/papers/iclr26_0004_3kvV1nfWVq_A2FM_An_Adaptive_Agent_Foundation_Model_for_Tool/figures/005_Figure_2.jpg]]
*Figure 2: Overview of A2FM. Left: the framework integrates three execution modes—instant, reasoning, and agentic—under a unified backbone with task-aware routing. Right: mode allocation across six benchmarks (MMLU-Pro, GPQA-d, AIME25, MATH500, Xbench-DeepSearch (Xbench), and GAIA-text (GAIA), illustrating how A2FM adapts routing to task characteristics*

![[assets/figures/papers/iclr26_0004_3kvV1nfWVq_A2FM_An_Adaptive_Agent_Foundation_Model_for_Tool/figures/006_Figure_3.jpg]]
*Figure 3: Overview of Adaptive Policy Optimization (APO). Left: Rollout and reward process. For each query, mode-specific rollouts are generated either by prefix injection (forced agentic/reasoning/instant) or by adaptive classification. Both prefix-injection tokens and tool-response tokens are excluded from loss since they are not model-generated. Right: Accuracy–efficiency trajectory under APO, showing how A2FM progressively approaches the Pareto frontier by improving accuracy while reducing non-instant triggering (excluding AIME24/25)*

现有大语言模型在处理多样任务时，通常分化为两类独立范式：以推理为核心的模型缺乏工具调用能力，而以智能体为核心的模型深度推理较弱；同时，二者都容易在简单查询上过度推理或过度调用工具，导致计算开销高、效率低下。A²FM（Adaptive Agent Foundation Model）通过在一套统一的主干网络中动态调度三种执行模式，从根本上破解了这一瓶颈。

### 统一主干与任务感知路由

A²FM 整合了三种执行模式：
- **即时模式（instant）**：对简单事实型问题直接生成答案；
- **推理模式（reasoning）**：需要多步逻辑推导时输出完整的思维链；
- **智能体模式（agentic）**：当需要与外部工具交互（如搜索、网页抓取、代码执行）时，生成工具调用序列并融合工具返回结果。

三种模式共享同一个解码器模型，由一个自学习的**任务感知路由器（Task-Aware Router）** 在推理时刻动态选择。形式上，给定查询 $x$，路由器输出模式概率分布，并采样得到模式 $m$：

$$
m \sim \pi_{\mathrm{route}}(m \mid x), \quad m \in \mathcal{M} = \{\text{instant}, \text{reasoning}, \text{agentic}\}
$$

随后，由对应模式的策略生成最终回答 $y$：

$$
y \sim \pi_m(y \mid x)
$$

模型输出不仅包含答案本身，还可能包含推理链或工具调用轨迹，具体结构由模式内建的格式模板控制。这一机制通过在输入中加入分类标签（如 `<classification> instant </classification>`）实现模式条件的生成控制，确保不同模式之间轨迹风格的一致性（见 Section 3.2 和附录 K 的模板定义）。

### 两阶段训练流程

A²FM 采用“先路由后对齐”的训练策略，将模式选择与模式内轨迹生成进行联合优化。

**第一阶段：路由-对齐监督微调（Route-Then-Align SFT）**  
利用高质量标注数据，每条训练样本同时包含模式分类标签（`<classification>` 标记）和该模式下的完整生成轨迹。微调过程强制模型学习：
- 根据查询内容正确输出分类标签；
- 在给定分类标签的条件下，生成与模式一致的高质量回答。
此阶段为后续强化学习提供了合理的初始化策略，使模型具备初步的模式感知生成能力（见图 2 左侧框架，Section 3.2）。

**第二阶段：自适应策略优化（Adaptive Policy Optimization, APO）**  
基于 GRPO 强化学习框架，APO 进行了两项关键扩展，以直接优化准确率-效率的权衡：
1. **定制化的 Rollout 策略**：每一批样本中包含强制模式 Rollout 与自适应 Rollout。强制模式下，通过前缀注入迫使模型分别以即时、推理、智能体三种模式各生成 $\rho$ 条轨迹；自适应模式下，则由模型自主选择模式并生成 $\gamma$ 条轨迹。这种设计既保证了所有模式得到充分探索，又能对正确的自选模式行为进行奖励。
2. **自适应奖励函数**：除了基于答案正确性的二元奖励 $r_{\mathrm{acc}}$ 和格式合规奖励 $r_{\mathrm{format}}$ 之外，APO 引入一个与任务难度挂钩的奖励项 $r_{\mathrm{adaptive}}$：
   
$$
r_{\mathrm{adaptive}} = \begin{cases}
   1 - p^{\alpha}, & \text{若选择了非即时模式} \\
   1, & \text{若选择即时模式}
   \end{cases}
$$

   其中 $p$ 为该查询在强制模式下的经验成功率（衡量任务可被廉价的方式解决的概率），$\alpha$ 为放缩因子。该奖励在简单查询（$p$ 高）上对非即时模式施加惩罚，从而鼓励路由器在低难度任务上优先输出即时模式，仅在必要时才触发昂贵的推理或工具调用（见图 3，Section 3.3）。

### 输入输出流与效率评估

在推理阶段，输入为自然语言查询 $x$，模型首先通过路由器输出分类标记，确定执行模式，再依模式生成完整输出。对于智能体模式，输出中包含多步工具调用与中间观察，外部工具（搜索引擎、页面抓取、代码沙箱等）被标准化为统一接口，每次调用后的观察结果拼接回上下文，最终产生整合答案。

整体框架的效率通过 **Cost-of-Pass（CoP）** 衡量，即每个正确回答的平均推理成本。实验证实，A²FM 的自适应执行将 CoP 降至 $0.00487，相比纯推理模式降低 45.2%，相比纯智能体模式降低 33.5%，在保持相当准确率的同时显著提升了成本效率（见 Abstract 与 Figure 4b）。消融实验进一步表明，自适应奖励使得简单查询上即时模式的使用比例从 50.2% 提升至 58.6%，而综合分数仅轻微下降 0.9 点，验证了该路由机制能够准确识别查询难度并作出低成本决策（Table 4）。

综上，A²FM 通过统一主干下的模式集成、任务感知路由以及联合优化的两阶段训练，构建了一个既能处理复杂推理与工具交互需求，又能在简单任务上保持轻量高效的混合推理框架。



A²FM的核心设计在于将三类执行模式整合到统一主干网络中，并通过一个可学习的路由器进行动态调度。在此基础上，两阶段“先路由后对齐”训练与自适应策略优化（APO）联合优化模式选择与模式内轨迹质量，平衡准确率与推理成本。以下仅呈现有明确证据的模块定义与关键公式。

### 三模式统一框架与路由决策
模型定义模式集合  
$$
\mathcal{M} = \{\mathrm{instant, reasoning, agentic}\}
$$  
其中 **instant** 模式直接给出答案；**reasoning** 模式进行深度链式推理；**agentic** 模式调用工具并执行多步交互。对于输入查询 $x$，任务感知路由器（Task‑Aware Router）依据策略 $\pi_{\mathrm{route}}$ 选择模式  
$$
m \sim \pi_{\mathrm{route}}(m \mid x)
$$  
随后由对应模式的策略生成最终输出  
$$
y \sim \pi_m(y \mid x)
$$  
该设计使得同一主干网络可以根据查询特性动态切换执行路径，避免对简单查询进行不必要的复杂展开。

### 自适应策略优化（APO）中的奖励设计
APO在GRPO基础上引入自适应奖励，以显式编码准确率‑效率权衡。每个模式 $m$ 下的轨迹 $y$ 获得复合奖励。核心组件如下：

**正确性奖励**：由LLM‑as‑Judge（$M_j$）判断答案是否正确，  
$$
r_{\mathrm{acc}} = \mathbb{I}\big[ M_j( x , \hat{y} ) = 1 \big]
$$

**格式奖励**：强制轨迹必须遵守所选模式的输出模板，否则归零，  
$$
r_{\mathrm{format}} = \begin{cases} 1, & \text{若 } y \text{ 符合模式 } m \text{ 的格式} \\ 0, & \text{否则} \end{cases}
$$

**自适应奖励**：仅在模型选择非即时模式时生效，用以抑制对简单查询的过度计算。惩罚项依赖查询的“强制成功率”$p$——即在强制使用某一昂贵模式时，该模式能够答题正确的经验概率（通过离线采样估计）。惩罚强度由缩放因子 $\alpha$ 控制（论文设定 $\alpha=2$），  
$$
r_{\mathrm{adaptive}} = \begin{cases} 1 - p^{\alpha}, & \text{若选择了非即时模式} \\ 1, & \text{否则} \end{cases}
$$  
查询越简单（$p$ 越接近1），非即时模式受到的惩罚越重，从而引导路由器将更多算力分配给真正需要推理或工具调用的查询。

APO的总奖励为上述三项的加权组合（具体权重由实验配置决定），在同一次查询的多次 rollout 中同时包含强制模式采样与自适应采样，确保所有模式得到充分探索并奖励正确的自主路由决策。消融实验证实，该自适应奖励项使即时模式使用比例从50.2%提升至58.6%，而综合分数仅微降0.9点，有效实现了成本控制与任务质量的平衡。



## 实验与关键发现

### 核心瓶颈与实验动机

现有大语言模型面临显著的功能分化：以DeepSeek‑R1为代表的推理核心模型缺乏原生的工具调用能力，而以DeepSeek‑V3.1为代表的智能体核心模型则深度推理能力较弱。更关键的是，二者在简单查询上均表现出过度推理或过度调用工具的问题，导致不必要的计算开销。A²FM的因果旋钮在于引入任务感知路由器（Task‑Aware Router），统一调度即时、推理和智能体三种执行模式，并通过自适应策略优化（APO）在强化学习中联合优化路由决策与轨迹生成，从而平衡准确率与计算成本。

### 主要结果：跨任务泛化能力

Figure 1 呈现了A²FM在通用基准上的平均性能对比。在32B规模下，A²FM在同尺寸模型中达到领先水平：智能体任务BrowseComp得13.4%，推理任务AIME25得70.4%，通用任务HLE得16.7%（置信度：0.95，来自Abstract及Figure 1）。Table 1 给出了三类基准上的详细统一结果——A²FM在XBench‑DS上获得56.0%，超越AFM‑Search的54.0%（置信度：1.0，Table 1a）；在MATH500上达到95.0%，与o1持平（置信度：1.0，Table 1b）。GAIA上的适应性模式得57.3%，强制智能体模式则达到60.7%，确立了同尺寸模型的新最优水平（置信度：1.0，Table 1a）。这一差距揭示了一个关键权衡：适应性路由虽牺牲少量绝对准确率，但换取了显著的计算效率提升。

![[assets/figures/papers/iclr26_0004_3kvV1nfWVq_A2FM_An_Adaptive_Agent_Foundation_Model_for_Tool/figures/011_Table_1.jpg]]
*Table 1: Unified results across (a) agentic, (b) reasoning, and (c) general-knowledge benchmarks. Bold = best; underline = second-best. Teal/Red superscripts indicate gain/loss of the forced mode relative to adaptive A2FM. ∗ indicates results reproduced by us. All numbers are reported as avg@1, except AIME24/25 which use avg@32*

![[assets/figures/papers/iclr26_0004_3kvV1nfWVq_A2FM_An_Adaptive_Agent_Foundation_Model_for_Tool/figures/003_Figure_1.jpg]]
*Figure 1: Average performance on agentic, reasoning, and general (ARG) benchmarks. Overall, $\mathbf { A } ^ { \mathrm { 2 } } \mathbf { F } \mathbf { M } ^ { * }$ ranks 1st, 2nd, and 1st on the three categories, respectively. Moreover, $\mathrm { A ^ { 2 } F M ^ { * } }$ , denoted as a variant that uses the best-suited mode for each benchmark, further improves over the adaptive version by +0.8 on agentic and +3.2 on general benchmarks

### 效率与成本：从Cost‑of‑Pass看模式选择

Adaptive execution将每个正确回答的推理成本降至$0.00487，相比纯推理模式降低45.2%，相比纯智能体模式降低33.5%（置信度：0.95，来自Abstract及Figure 4b）。Figure 4进一步揭示了模式分配与任务难度之间的关系：低难度区间即时模式占据主导，而随着问题复杂度上升，非即时模式的分配比例逐步升高，且此趋势与准确率曲线高度耦合。Table 7对比了“推理+智能体双模式”与自适应路由方案在200道SuperGPQA子集上的表现——前者Pass@2为67.0，CoP为0.00812；后者Pass@2为62.5，CoP仅为0.00432。自适应路由以约4.5个点的Pass@2代价，换来近两倍的成本效率提升，验证了路由决策中“少即是多”的核心设计理念。

![[assets/figures/papers/iclr26_0004_3kvV1nfWVq_A2FM_An_Adaptive_Agent_Foundation_Model_for_Tool/figures/023_Table_7.jpg]]
*Table 7: Comparison of efficiency and performance on a 200-query subset of SuperGPQA*

### 消融分析：自适应奖励的驱动效应

APO中的自适应奖励项是调节效率的关键杠杆。Table 4展示了该奖励的消融结果：加入自适应奖励后，SuperGPQA上即时模式使用比例从50.2%升至58.6%，而总体得分仅微降0.9点（54.7 vs. 55.6），表明模型在简单查询上被有效引导至低成本解答路径（置信度：1.0，Table 4及对应分析）。这一效应背后的机制是惩罚性奖励$r_{\mathrm{adaptive}} = 1 - p^{\alpha}$，它利用经验强制成功率$p$来衡量问题难度，并对非即时模式施加与难度成反比的压力——简单题上较大的惩罚迫使路由器偏好即时模式，而困难题上惩罚趋近于零，允许模型调用代价更高的推理或工具链。

![[assets/figures/papers/iclr26_0004_3kvV1nfWVq_A2FM_An_Adaptive_Agent_Foundation_Model_for_Tool/figures/018_Table_4.jpg]]
*Table 4: Ablation Results of Adaptive Reward in APO on SuperGPQA*

### APO阶段增益与模式效率

Table 9系统对比了SFT阶段与APO阶段后的性能跃迁——APO在所有10个基准上均显著提升了准确率（如XBench从51.0→56.0，MATH500从84.0→95.0，HLE从11.0→16.7），同时大幅降低了非即时触发率（Non‑Instant Triggering Rate，NITR），在通用基准上NITR平均下降超过10个百分点（置信度：0.95，来自Section G的相关分析）。这表明APO不仅通过强化学习提升了解题轨迹质量，还成功内化了成本感知的路由策略。

并行执行架构同样贡献于效率提升。Table 8显示，并行智能体执行在GAIA上达到50.5（对比顺序基线的47.6），BrowseComp上12.2（对比9.1），XBench上47.0（对比42.0）；同时，Cost‑of‑Pass在三个基准上均明显低于顺序方案，证实并行工具调用在提升证据收集覆盖度的同时并未引入冗余开销。

### 失败模式与局限性说明

当前实验中，部分细节的证据强度较低。Figure 6仅从数据分布角度呈现训练数据构成，但其在消融解释中的支撑力度需人工核实。此外，教师模型蒸馏过程中原始性能退化明显——Table 6显示GPT‑5‑Mini在BC‑200上的原始得分为31.0，蒸馏后SFT得分提升至51.5，但这一提升发生于基线极低的背景下，蒸馏方法的泛化稳定性仍需审慎解读。LLM‑as‑Judge的信号一致性在GAIA上表现良好（GPT‑5‑Mini与人工判断的0/103分歧，见Table 5），但这一结果仅覆盖单一任务场景，对其他类型基准的评判一致性缺乏直接证据。

### 开放性问题

当前实验尚未量化在不同LLM骨架间切换时路由策略的可迁移性——Table 10显示A²FM‑Qwen2.5‑32B‑Instruct与A²FM‑Qwen3‑32B在HLE上的得分分别为11.0与10.5，存在倒挂现象，提示不同基座模型的先验分布可能影响路由行为。此外，小规模模型上的SFT‑only结果（Table 11和Table 12）虽确认了路由‑对齐范式在14B和4B规模的有效性，但APO阶段在这些规模上的增益尚缺乏实验证据。自适应奖励中难度估计的鲁棒性——尤其当问题分布偏移时$p$的可靠性——仍需进一步分析。



## 定位与知识库关联

### 与现有方法的关系

A²FM 在统一主干网络下集成了即时回答、推理与智能体三种执行模式，并通过任务感知路由器实现模式的选择与切换，这一设计直接回应了当前大语言模型在推理与工具使用能力上二元分化的瓶颈：DeepSeek‑R1 等模型以长链推理见长但缺乏原生的工具调用接口，而 DeepSeek‑V3.1 等智能体模型虽有工具执行能力深度推理却较弱。同时，即使是采用混合思路的 Qwen3‑32B，其推理与智能体能力也分属分离的对齐阶段，没有形成统一的调度与权衡机制。A²FM 通过以下三个关键槽位的改变构建了与这些基线不同的方法谱系位置：

| 设计槽位 | 基线值（代表性模型） | A²FM 取值 | 证据锚点 |
|----------|-------------------|-----------|----------|
| 执行模式整合 | 推理与工具使用松散耦合，路由缺失或间接（DeepSeek‑R1, DeepSeek‑V3.1, Qwen3‑32B） | 统一主干下，自学习路由器在即时、推理、智能体三种模式间动态选择 | Figure 2, Section 3.1 |
| 训练范式 | 分离的对齐阶段或仅优化推理长度（Qwen3‑32B 分别训练推理与智能体，GRPO 仅考虑长度正则化） | 两阶段“路由‑对齐”微调 + 自适应策略优化（APO），联合优化路由决策与模式内轨迹生成 | Section 3.2, Section 3.3 |
| 成本控制奖励 | 纯准确率二元奖励或长度正则化奖励（如 GRPO） | 自适应奖励：对简单查询，选非即时模式时施加与任务难度相关的惩罚因子 $1 - p^{\alpha}$，鼓励低成本模式 | Adaptive Reward formula, Section 3.3 |

在基础强化学习框架上，APO 直接建立在 GRPO 之上，但注入了两个关键扩展：（i）针对三种模式强制采样的 rollout 策略（强制模式各 $\rho$ 次，再加 $\gamma$ 次自适应选择），避免模式采样不足；（ii）将准确率‑效率权衡显式编码为自适应奖励，使策略在学习过程中自动识别简单查询并倾向于即时模式。这种面向多模式路由的奖励设计是 A²FM 区别于纯推理长度控制的重要方法创新。

### 适用边界与局限

论文并未单独列出局限与开放问题的章节，以下基于实验设计与工具链的事实性内容进行的推断，**建议读者结合实际场景仔细验证**。

- **规模与资源边界**：所有实验均在 32B 参数规模完成，最大序列长度限制为 32 768（SFT）和 65 536 个 token（APO）。虽然在该规模上取得了与更大模型可比的性能（通用基准上 A²FM\* 以 55.3 分超越 GPT‑4.1、Claude 4 Sonnet 等），但模型在进一步缩放至百亿或千亿级参数时的行为，以及超过 65K token 的极长上下文任务上的可靠性尚未得到检验。
- **工具链依赖性**：智能体模式所使用的工具——Google 搜索（SerpAPI）、网页抓取与摘要（Jina API + gpt‑5‑mini）以及代码沙箱（nsjail，CPU 5 s，内存 5 GB）——是固定的外部服务。API 的可用性、响应延迟和摘要质量会直接影响智能体轨迹的稳定性；代码执行在时间与内存上的硬性限制也使 A²FM 不适用于需要长时间运行或大量内存的编程任务。
- **路由精度与难度估计**：自适应奖励中的难度估计依赖强制模式下的成功概率 $p$，该概率由教师模型（如 gpt‑5‑mini）在训练数据上离线计算得到。当任务分布偏移（例如全新领域的难度特征不同于训练集）时，该估计可能失准，导致路由器选择不合适的模式。消融实验显示，引入自适应奖励后整体分数微降 0.9 点（55.6 → 54.7），虽然即时模式使用率显著上升，但已说明在某些任务上模式选择可能牺牲了极少量准确率。
- **评估的广度**：主要结果集中在智能体（GAIA, BrowseComp, XBench‑DS）、推理（MATH500, AIME24/25）和通用知识（GPQA‑d, SuperGPQA, MMLU‑Pro, HLE）基准，尚未覆盖对话安全性、长程交互一致性或多模态任务。因此模型在全场景部署下的行为尚缺乏充足的实证。

### 开放问题

论文正文与附录均未明确提出后续需要解决的开放问题。从方法设计和实验留下的线索中可以提炼出若干值得社区关注的追问（均未在原文中获得直接答案）：

1. **路由策略能否在更细粒度的内部推理步骤中复用**：当前路由器在查询级进行模式决策，但许多任务内部可能兼具推理与检索需求。是否可以将类似的自适应奖励机制用于细粒度的步骤级路由（例如在单次回答中交替进行推理和工具调用），从而进一步降低计算开销？
2. **自适应奖励的超参数稳定性**：APO 的惩罚因子 $p^{\alpha}$ 中 $\alpha$ 被固定为 2，强制采样数 $\rho$ 与自适应采样数 $\gamma$ 均为 3。这些超参数在更大模型或不同任务分布下是否需要重新搜索，以及是否存在一种原则性的取值策略，仍是未决问题。
3. **工具能力扩展与代理可靠性**：当前仅绑定了三种工具，如何将自适应路由框架平滑扩展到动态添加新工具或多步工具组合的场景，并保证安全约束，尚未涉及。
4. **模型的持续学习与分布外泛化**：在老师模型能力有限或任务分布自然漂移时，强制模式成功概率的估计如何在线更新，以及路由器能否持续适应新难度特征，属于待验证的长期挑战。

> 注：以上开放问题基于对论文方法与实验设计的推演，原文并未直接声明，需读者在后续研究中自行评估。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A2FM_An_Adaptive_Agent_Foundation_Model_for_Tool_Aware_Hybrid_Reasoning.pdf

![[paperPDFs/ICLR_2026/A2FM_An_Adaptive_Agent_Foundation_Model_for_Tool_Aware_Hybrid_Reasoning.pdf]]
