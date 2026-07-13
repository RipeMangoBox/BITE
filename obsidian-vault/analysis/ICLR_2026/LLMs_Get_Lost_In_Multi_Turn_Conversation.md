---
title: "LLMs Get Lost In Multi-Turn Conversation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/LLMs_Get_Lost_In_Multi_Turn_Conversation.pdf
project_link: null
code_link: null
openreview_forum_id: VKGTGGcwl6
aliases:
- SSF
- LGLMTC
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "信息揭示的节奏（单轮全部提供 vs. 多轮逐片揭示）是影响模型性能和可靠性的主要调节因素；辅助调节因素包括模型的回答策略（是否过早给出完整答案、是否冗长）。"
primary_logic: "当前LLM在单轮、指令完整的理想条件下表现优异，但在更真实的多轮、指令逐渐揭示的对话中，性能平均下降39%；这一退化主要来源于不可靠性（interpercentile range）的成倍增长，而非模型能力（aptitude）的显著下降。即使降低温度、增加提示等常规优化手段也无法有效缓解，说明模型本质上缺乏在对话中恢复和重新聚焦的能力。"
claims:
- "All models see performance degrade on every task when comparing FULL and SHARDED performance, with an average degradation of -39%."
- "Unreliability skyrockets with an average increase of 112% in the sharded setting, while aptitude drops only 16%."
- "Lowering assistant temperature to 0.0 still leaves ~30% unreliability in SHARDED simulations, showing temperature cannot fix multi-turn reliability."
- "Even with only two shards, models already exhibit significant degradation (minor aptitude loss, large unreliability increase), demonstrating the lost in conversation phenomenon."
---

# LLMs Get Lost In Multi-Turn Conversation

> [!tip] 核心洞察
> 当前LLM在单轮、指令完整的理想条件下表现优异，但在更真实的多轮、指令逐渐揭示的对话中，性能平均下降39%；这一退化主要来源于不可靠性（interpercentile range）的成倍增长，而非模型能力（aptitude）的显著下降。即使降低温度、增加提示等常规优化手段也无法有效缓解，说明模型本质上缺乏在对话中恢复和重新聚焦的能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大语言模型在多轮对话中迷失方向 |
| 英文题名 | LLMs Get Lost In Multi-Turn Conversation |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=VKGTGGcwl6) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Sharded Simulation Framework |
| Dataset | 自定义六项任务集 (Code, Database, Actions, Data-to-text, Math, Summary), 同上, 翻译任务 (Translation), 四项任务 (Math, Code) |

> [!tip] 效果简介
> - 自定义六项任务集 (Code, Database, Actions, Data-to-text, Math, Summary) 上，平均性能 (P ) 为 SHARDED 平均 65%，对比 FULL 平均 90%，变化 -25个百分点，相对下降 39%。
> - 同上 上，不可靠性 (U) 为 平均增加 112%，对比 FULL 中的不可靠性，变化 +112%。
> - 翻译任务 (Translation) 上，BLEU 为 SHARDED，对比 FULL，变化 无明显性能下降（差异在 10% 以内）。

## 概要

### 问题：大语言模型在多轮对话中“迷失”

当前大语言模型（LLM）在单轮、指令完整的理想条件下表现优异，但在更贴近真实场景的多轮对话中，性能会出现严重且系统性的退化。本文通过构建一个可控的模拟环境，系统性地揭示了这一现象：当任务指令不是一次性完整给出，而是在多轮对话中逐片揭示时，几乎所有主流开源与闭源模型都会“迷失”——性能急剧下降，不可靠性成倍增长。

这一问题的核心瓶颈在于：模型过早尝试给出完整答案并产生过多未经证实的假设，同时过度依赖之前的错误回答，从而分散了对新揭示信息的关注。信息揭示的节奏（单轮全部提供 vs. 多轮逐片揭示）是影响模型性能和可靠性的主要调节因素。

### 核心结论

- **性能平均下降 39%**：在六项生成式任务上，15 个 LLM 从单轮完整指令（FULL）切换到多轮逐片揭示（SHARDED）后，平均性能从 90% 降至 65%（Table 1, Section 5.1）。
- **不可靠性飙升 112%**：性能退化的主因并非模型能力（aptitude）的显著下降（仅降 16%），而是不可靠性（interpercentile range）的成倍增长（Figure 5b, Section 5.2），意味着模型在多轮对话中表现极不稳定。
- **常规优化手段失效**：降低温度至 0.0 仍残留约 30% 的不可靠性（Table 7, Appendix G.2）；在系统提示中预告对话可能不完整，仅带来约 1% 的平均改善（Table 6, Appendix G.1）。
- **退化门槛极低**：指令一旦拆分为 2 个分片（即至少两轮对话），不可靠性即大幅上升，进一步拆分影响不大（Figure 5c, Section 5.3）。

### 方法定位

本文提出 **Sharded Simulation Framework**，核心思路是将现有的单轮完整指令通过分片处理（sharding process）转化为一组逐片揭示的对话指令，并在多轮对话模拟中控制信息释放的节奏。该方法并非提出一个新模型，而是一个**评估框架**，用于系统性地测量 LLM 在信息逐步揭示的对话场景中的性能与可靠性。

在方法谱系中，该工作区别于以下两类基线：
- **FULL（单轮完整指令）**：代表理想化的实验室性能，一次性提供全部信息。
- **CONCAT（单轮拼接分片）**：将分片后的所有信息在单轮中拼接提供，用于控制重新措辞的影响。
- **Episodic multi-turn evaluation（先行工作）**：将多轮对话视为一组可独立评估的子任务，本文认为该方法高估了模型能力，因为它忽略了对话上下文中信息逐步积累和模型“迷失”的效应。

该方法的关键调节变量是**信息揭示方式**：从一次性完整提供（FULL）变为逐轮最多揭示一个信息分片（SHARDED）。这一改变直接作用于模型的回答策略和注意力分配，是导致性能退化的因果旋钮。

### 主要结果速览

| 指标 | FULL（基线） | SHARDED（多轮） | 变化 |
|------|-------------|----------------|------|
| 平均性能 (P̄) | 90% | 65% | **-25 个百分点（-39%）** |
| 不可靠性 (U) | — | — | **+112%** |
| 能力 (A) | — | — | **-16%** |

在翻译任务上，SHARDED 与 FULL 的性能差异在 10% 以内，未观察到显著的“迷失”现象（Table 8, Appendix G.3），提示该问题可能与任务的语义压缩程度和信息依赖性有关。

两种简单的缓解策略——**RECAP**（每轮重复已揭示信息）和 **SNOWBALL**（累积重复所有历史信息）——能在四项任务上带来 15–20% 的改善，但均无法恢复到 FULL 水平（Table 5, Section G.1），说明当前 LLM 本质上缺乏在多轮对话中恢复和重新聚焦的能力。



大语言模型（LLM）在单轮、指令完整的理想化基准测试中表现卓越，但真实世界的交互往往以多轮对话形式展开，用户需求并非一次性完整给出，而是在对话过程中逐步揭示。这种“指令逐渐明晰”的对话模式构成了当前LLM评估体系中的一个显著盲区：现有基准测试几乎完全忽略了多轮交互中信息逐片披露所带来的挑战。

本文通过构建一个名为 **Sharded Simulation** 的仿真框架，系统性地量化了这一盲区的影响。该框架的核心思路是将现有的单轮完整指令通过分片处理（sharding process）转化为一组更小的、去上下文的指令片段（shards），然后在多轮对话中由模拟用户逐片释放这些信息，从而严格复现“指令逐渐揭示”的真实对话场景。实验覆盖了15个主流开源与闭源LLM，涉及代码生成、数据库查询、数学推理等六类生成式任务，进行了超过20万次对话模拟。

结果揭示了一个系统性且严重的问题：所有模型在多轮对话设定下均出现性能衰退，平均性能从单轮完整指令下的90%骤降至65%，相对下降达**39%**。更关键的是，这一衰退主要源于模型**不可靠性（Unreliability）的急剧上升**——十分位距（interpercentile range）平均增加**112%**，而代表模型最佳能力上限的**能力值（Aptitude）仅下降16%**。这意味着模型并非“不会做”，而是“无法稳定地做对”，在多轮对话中表现出极大的输出波动。

即使将温度参数降至0.0，不可靠性仍维持在约30%的高位（GPT-4o），表明常规的确定性解码策略无法根治这一问题。进一步分析发现，模型在对话早期就倾向于给出完整答案、生成冗长回复、过度依赖之前的错误输出，以及忽略对话中间轮次引入的信息，这些行为模式共同构成了性能退化的因果链条。值得注意的是，推理型模型（如o3、R1）并未展现出明显优势，暗示当前的推理增强技术在设计时同样未考虑多轮对话的独特挑战。

这一发现揭示了LLM在从“实验室单轮”走向“真实多轮”应用时面临的根本性瓶颈：模型缺乏在对话中恢复和重新聚焦的能力，而现有评估范式系统性地高估了其实际可用性。



## 核心方法与创新机理

本文的核心创新在于**将多轮对话中 LLM 性能退化的根因从“模型能力不足”重新定位为“模型不可靠性失控”**，并设计了一套可复现的仿真框架来系统量化这一现象。

### 关键因果调节变量：信息揭示节奏

传统单轮评估（FULL 设定）将完整指令一次性提供给模型，代表理想化的实验室条件。本工作识别出，**信息揭示的节奏**——即指令是单轮全部提供还是多轮逐片揭示——是影响模型性能与可靠性的主导调节变量。为此，作者提出了 **Sharded Simulation Framework**，其核心 changed slot 为：

| 调节变量 | 基线设定 (FULL) | 创新设定 (SHARDED) |
|:---|:---|:---|
| 信息揭示方式 | 一次性在首轮提供完整指令 | 通过多轮交互逐片揭示指令信息，每轮最多一片 |

该框架通过一个半自动的 **Sharding Process**（分割→改写→验证→人工审核）将现有单轮基准指令转化为多个去上下文的“信息片”（shards），再由基于 GPT-4o-mini 的 User Simulator 在对话中逐片自然引入。这一设计使得研究者能够在控制信息总量的前提下，独立操纵信息揭示的时序节奏，从而剥离出多轮交互本身对模型行为的影响。

### 从“能力下降”到“不可靠性爆炸”的认知转变

已有工作（如 Episodic multi-turn evaluation）将多轮对话视为一组可独立评估的子任务，隐含假设模型能力的均值下降是主要问题。本文通过引入 **能力 (Aptitude)** 与 **不可靠性 (Unreliability)** 的分解，推翻了这一假设：

- **能力** $A^{90} = \mathrm{percentile}_{90}(S)$：模型在最佳情况下的表现上限；
- **不可靠性** $U_{10}^{90} = \mathrm{percentile}_{90}(S) - \mathrm{percentile}_{10}(S)$：由于随机性导致的质量波动范围。

实验揭示了一个反直觉的发现：从 FULL 到 SHARDED，模型的**平均性能下降 39%**，但其主因并非能力衰减（能力仅下降 16%），而是**不可靠性平均飙升 112%**（Figure 5b, Section 5.2）。这意味着模型在单轮中能稳定做对的事，在多轮中变得时而能做对、时而完全失败——问题出在“一致性”而非“上限”。

### 对常规缓解手段的证伪

这一认知转变也解释了为何常规优化手段失效：

- **降低温度至 0.0**：在 SHARDED 设定中，GPT-4o 的不可靠性仍高达约 30%（Table 7, Appendix G.2），说明随机采样并非不可靠性的主因；
- **系统提示预告对话不完整**：仅提升 GPT-4o 平均性能约 +1%，对可靠性影响有限（Table 6, Appendix G.1）；
- **RECAP/SNOWBALL 重复策略**：虽能带来 15–20% 的改善，但远未恢复到 FULL 水平（Table 5, Section G.1）。

这些结果表明，模型在多轮对话中的“迷失”并非简单的提示工程问题，而可能源于**注意力机制在渐进信息流下的结构性偏移**——模型过早锁定早期假设、过度依赖自身之前的错误回答，从而丧失了对新揭示信息的重新聚焦能力。



本文提出的**Sharded Simulation Framework**是一个将单轮完整指令转化为多轮逐片对话的仿真环境，旨在系统性地测量LLM在信息渐进揭示条件下的性能退化。该框架的核心思想是：将传统单轮评测中的“一次性完整指令”拆解为多个原子信息单元（shards），并通过多轮对话逐轮释放，从而模拟真实世界中用户逐步提供需求的交互模式。

### 框架总览

整个仿真框架由两大阶段构成：**指令分片预处理**和**多轮对话仿真循环**。

**指令分片预处理**将原始的单轮完整指令（fully-specified instruction）转化为一组分片指令（sharded instruction），每个分片承载原指令的一部分信息。**多轮对话仿真循环**则基于分片指令，通过用户模拟器逐轮释放信息，并监测助手模型（待评估LLM）的回复策略与最终答案质量。

框架的关键设计在于：通过控制**信息揭示的节奏**这一因果调节变量，将单轮与多轮性能差异归因于对话的动态性本身，而非指令内容的损失。

### 指令分片预处理

分片预处理遵循四步半自动流程（Figure 6）：

1. **Segmentation（分割）**：提取原指令中的原子信息单元。
2. **Rephrasing（改写）**：将各原子信息改写为去上下文的、对话式的自然语句。
3. **Verification（验证）**：通过模拟FULL和CONCAT两种单轮设定，验证信息保留率不低于80%。
4. **Manual Inspection（人工审核）**：由作者人工审核并编辑最终的分片指令。

这一流程确保了分片后的指令集合能够完整传递原始指令的信息，排除了因信息丢失导致的性能下降。

### 多轮对话仿真循环

仿真循环（Figure 2）由四个核心模块组成，每轮对话按以下流程执行：

1. **User Simulator（用户模拟器）**：基于GPT-4o-mini，从剩余未揭示的分片中选择最自然的一片，以对话形式发送给助手。该模块模拟了真实用户逐步提供信息的交互模式。
2. **Assistant（待评估模型）**：接收用户消息后生成回复。这是框架中唯一的“仿真主体”（Figure 2中红色高亮部分），其行为是评测的核心对象。
3. **Strategy Classifier（策略分类器）**：同样基于GPT-4o-mini，将助手回复分类为七种策略之一：澄清（clarification）、拒答（refusal）、猜测（guess）、询问（inquiry）、讨论（discussion）、未响应（unresponsive）或答案尝试（answer attempt）。该分类器的主要作用是检测答案尝试轮次，以触发后续的答案提取。
4. **Answer Extractor（答案提取器）**：当分类器检测到答案尝试时，从助手回复中提取最终答案文本，用于自动评估。

仿真持续进行直至所有分片被揭示，或达到预设的最大轮次限制。手动审查数百次对话表明，各仿真组件的错误率低于5%，且不利于助手的错误率低于2%（Table 2），验证了仿真环境的可靠性。

### 仿真设定类型

基于分片指令，框架支持多种仿真设定（Figure 3），以控制信息揭示的节奏：

- **FULL**：将原始完整指令在首轮一次性提供，代表理想化的单轮实验室性能上限。
- **CONCAT**：将所有分片拼接后在单轮中提供，用于控制分片改写本身的影响。实验表明CONCAT性能平均达到FULL的95.1%（Table 1），验证了分片过程的信息保真度。
- **SHARDED**：每轮最多揭示一个分片，强制信息渐进释放。这是框架的核心设定，用于测量多轮对话中的性能退化。
- **RECAP / SNOWBALL**：在SHARDED基础上，通过重复注入历史用户指令来缓解模型的“迷失”现象。RECAP每轮重复上一轮的用户指令，SNOWBALL则累积重复所有已揭示的分片。

### 输入输出流

框架的输入是来自现有单轮评测基准的完整指令（涵盖Code、Database、Actions、Math、Data-to-text、Summary六类任务，Figure 4），输出是模型在每条指令上的多次独立仿真得分。通过对同一指令运行N=10次独立仿真，框架计算三个核心指标：

- **平均性能** $\overline{P} = \sum_{i=1}^{N} S_i / N$：模型在该指令上的无偏性能估计。
- **能力** $A^{90} = \mathrm{percentile}_{90}(S)$：模型表现的上限估计，即90分位数得分。
- **不可靠性** $U_{10}^{90} = \mathrm{percentile}_{90}(S) - \mathrm{percentile}_{10}(S)$：十分位距，衡量因模型随机性导致的质量波动。

这一指标体系将性能退化分解为“能力下降”与“不可靠性上升”两个正交维度，为后续的根因分析提供了量化基础。



### 分片仿真框架（Sharded Simulation Framework）

本文提出的核心方法论是一个将单轮指令转化为多轮对话的仿真框架，其设计目标是系统性地揭示LLM在信息逐步揭示过程中的性能退化。该框架由两大阶段构成：**指令分片处理**（Sharding Process）和**对话仿真循环**（Simulation Loop）。

#### 指令分片处理

指令分片处理是将原始的单轮完整指令（fully-specified instruction）转化为一组可逐轮揭示的“分片指令”（sharded instruction）的预处理流程。该流程包含四个步骤：

1.  **Segmentation（分割）**：提取原指令中的原子信息单元。
2.  **Rephrasing（改写）**：将各原子信息改写为去上下文的、对话式的自然语句，使其在单独呈现时仍保持可理解性。
3.  **Verification（验证）**：通过模拟FULL和CONCAT两种单轮设置，验证分片后信息的完整保留率不低于80%。
4.  **Manual Inspection（人工审核）**：由作者对最终的分片指令进行人工审核和编辑，确保质量。

该流程的关键设计意图在于：确保分片后的指令在信息总量上与原始指令等价，从而将多轮对话中的性能差异**归因于信息揭示的节奏**（一次性提供 vs. 逐片揭示），而非信息本身的缺失或扭曲。

#### 对话仿真循环

对话仿真循环基于分片后的指令，模拟一个用户与待测LLM（助理）之间的多轮交互。其核心组件包括：

-   **User Simulator（用户模拟器）**：基于GPT-4o-mini，负责选择并自然体现下一片信息。它不直接粘贴分片文本，而是将信息融入对话语境中。
-   **Assistant（待测模型）**：接收用户消息后生成回复，是仿真评估的对象。
-   **Strategy Classifier（策略分类器）**：基于GPT-4o-mini，将助理的每轮回复分类为澄清、拒答、猜测、询问、讨论、未响应或答案尝试。其主要作用是**检测答案尝试轮次**，以触发后续的答案提取和评分。
-   **Answer Extractor（答案提取器）**：从被标记为答案尝试的回复中提取最终答案文本，用于自动化评估。

仿真循环的核心约束是：**每轮对话至多揭示一片信息**。这一约束强制执行了信息逐步揭示的设定，是导致模型“迷失”的实验条件。

### 关键评估指标与公式

为量化模型在多轮对话中的表现，本文定义了一组基于多次独立仿真得分的统计指标。对同一指令进行 $N$ 次独立仿真，得到得分集合 $S = \{S_1, S_2, ..., S_N\}$。

#### 平均性能（Averaged Performance）

平均性能 $\overline{P}$ 是模型在给定指令上表现的**无偏估计**，定义为 $N$ 次仿真得分的算术平均：

$$\overline{P} = \sum_{i=1}^{N} S_i / N$$

该指标反映了模型的**期望表现**，是全文最核心的性能度量。

#### 能力（Aptitude）

能力 $A^{90}$ 用于估计模型表现的**理论上限**，即模型在最佳情况下的能力。它被操作化定义为所有仿真得分的**90分位数**：

$$A^{90} = \mathrm{percentile}_{90}(S)$$

选择90分位数而非最大值，是为了减少单次仿真中偶然“幸运”结果的干扰，提供更稳健的上限估计。

#### 不可靠性（Unreliability）

不可靠性 $U_{10}^{90}$ 衡量由于模型随机性导致的**表现波动幅度**。它被定义为得分的**十分位距**（interpercentile range），即90分位数与10分位数之差：

$$U_{10}^{90} = \mathrm{percentile}_{90}(S) - \mathrm{percentile}_{10}(S)$$

该指标的值越大，说明模型在相同指令下的表现越不稳定，即**不可靠性越高**。这是本文揭示的核心退化维度。

#### 可靠性（Reliability）

可靠性 $R_{10}^{90}$ 是不可靠性的互补指标，定义为：

$$R_{10}^{90} = 1 - U_{10}^{90}$$

该指标的值越接近1，表示仿真得分越稳定。在实验中，所有得分被映射至 $[0, 1]$ 区间，因此该公式具备数值上的直观性。

**指标间的因果解释关系**：实验结果表明，多轮对话中的平均性能下降（$\overline{P}$ 降低）主要源于不可靠性 $U_{10}^{90}$ 的急剧上升（平均增加112%），而非能力 $A^{90}$ 的显著下降（平均仅下降16%）。这一分解是本文的核心洞察：**模型并非“做不到”，而是“时灵时不灵”**。



## 实验与关键发现

### 核心发现：多轮对话中的系统性性能退化

研究通过分片仿真框架，对15个主流大语言模型在6项生成式任务上进行了超过200,000次模拟对话，揭示了多轮对话中普遍存在的“迷失”现象。**Table 1** 汇总了主要结果：所有模型在从单轮完整指令（FULL）转向多轮分片指令（SHARDED）时，性能无一例外地出现下降，平均退化幅度高达**-39%**。在FULL设定下，模型平均性能可达90%，而在SHARDED设定下骤降至65%，绝对降幅为25个百分点。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/005_Table_1.jpg]]
*Table 1: Averaged Performance (P ) of LLMs on six tasks ( Code, Database, Actions, Data-to-text, Math, and Summary). For each task, conversations are simulated in three settings: FULL, CONCAT, and SHARDED. Models are sorted in ascending order of average FULL scores across tasks. Background color indicates the level of degradation from the FULL setting. The last two columns average the performance drops from the CONCAT and SHARDED compared to the FULL in percentages across the six tasks*

作为对照的CONCAT设定（将分片信息拼接后在单轮提供）的平均性能达到FULL的95.1%，表明性能下降并非由分片过程中的信息改写或损失所导致，而是源于信息在多轮对话中逐片揭示这一交互模式本身。

### 退化根因：不可靠性飙升而非能力崩塌

研究进一步将性能分解为**能力（Aptitude, A⁹⁰）** 和**不可靠性（Unreliability, U₁₀⁹⁰）** 两个维度。能力衡量模型在最佳情况下的表现上限（90分位数），不可靠性衡量由于随机性导致的质量波动（90分位数与10分位数之差）。**Figure 5b** 的结果揭示了退化的真实结构：

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/006_Figure_5.jpg]]
*Figure 5: (a) Visual introduction to the concepts of Aptitude and Unreliability when overlaid on a box-plot visualization, (b) reliability results based on experimental simulations with 15 LLMs, (c) summary of results from gradual sharding experiment, with instructions sharded in gradually larger shard sets (from 1 to 8 shards)*

- **能力仅下降16%**：模型在最佳情况下仍保留了大部分单轮性能，说明模型的基本能力并未在多轮对话中丧失。
- **不可靠性飙升112%**：模型输出的质量波动成倍增长，意味着模型在多轮对话中变得极不稳定——同样的指令在不同模拟运行中可能产生截然不同的结果。

这一发现表明，LLM在多轮对话中“迷失”的本质不是能力不足，而是可靠性崩溃。模型有时仍能给出正确答案，但无法稳定地做到这一点。

### 关键调节因素与失败模式

#### 1. 过早给出完整答案

**Table 3** 分析了模型首次尝试给出完整答案的时机与最终性能的关系。在代码和数学任务中，若模型在对话的前20%阶段就做出首次答案尝试，平均性能仅为**30.9**；而当首次答案尝试发生在对话后80%阶段时，平均性能提升至**64.4**。这表明模型在多轮对话中过早地基于不完整信息做出判断，是导致性能退化的重要行为模式。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/010_Table_3.jpg]]
*Table 3: Averaged performance (P ) breakdown, based on how early in the conversation the LLM makes its first answer attempt. Analysis conducted on simulations of two tasks: Code and Math*

#### 2. 回复冗长与性能负相关

**Table 4** 按助手回复长度对模型进行分组分析。在六项任务中的五项里，回复最短分组的性能比最长分组高出**10-50%**。冗长的回复往往包含更多未经证实的假设和对先前错误回答的反复讨论，分散了模型对新揭示信息的注意力。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/013_Table_4.jpg]]
*Table 4: Averaged performance (P ) of LLMs on the six experimental tasks, arranged based on model relative verbosity (length of response). Performance degrades when models generate longer responses on five of the six tasks*

在SHARDED设定中，模型的答案尝试长度随尝试次数递增，且显著长于FULL/CONCAT中的答案——即使在最终正确的解答中，SHARDED中的代码也比FULL中长**27%**（**Figure 8**）。这进一步印证了模型在多轮对话中倾向于生成冗余内容，而非精准聚焦于当前信息。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/011_Figure_8.jpg]]
*Figure 8: Average length (in number of characters) of answer attempts across four tasks (Code, Database, Data-to-text, and Summary) in SHARDED conversations. Answer attempts in the FULL and CONCAT settings tend to be shorter on average than those from SHARDED setting. SHARDED answer attempts increase in length as the LLMs make more answer attempts*

#### 3. “中间轮次丢失”现象

**Figure 9** 揭示了模型在摘要任务中的信息引用模式：模型更倾向于引用对话中第一轮或最后一轮引入的文档信息，而系统性地忽略中间轮次引入的内容。这种“中间轮次丢失”（loss-in-middle）现象表明，模型在多轮对话中无法均匀地整合逐步揭示的信息，而是过度依赖首尾信息。

#### 4. 渐进分片实验：两轮即触发退化

**Figure 5c** 展示了渐进分片实验的结果。当指令被拆分为仅**2个分片**（即至少两轮对话）时，模型即表现出明显的不可靠性上升，而进一步增加分片数量（至8个）并未导致退化显著加剧。这说明“迷失”现象在信息揭示从单轮变为多轮的那一刻即被触发，而非随对话轮次累积而渐进恶化。

### 缓解策略的有限效果

研究测试了多种常规缓解手段，发现其效果均十分有限：

- **降低温度至0.0**（**Table 7**）：在SHARDED设定中，GPT-4o的不可靠性仍高达约**30%**，GPT-4o-mini在温度降低后甚至无改善。这说明温度参数无法解决多轮对话中的可靠性问题，退化根源于模型本身的推理机制而非采样随机性。
- **系统提示预告**（**Table 6**）：在系统提示中明确告知模型对话可能不会一次性提供完整信息，仅使GPT-4o的平均性能提升**+1%**，对可靠性的影响微乎其微。
- **RECAP与SNOWBALL策略**（**Table 5**）：通过在每轮对话中重复之前用户提供的信息来帮助模型保持聚焦。SNOWBALL（累积重复所有历史信息）在四项任务上带来了**15-20%**的性能改善，但仍远未恢复到FULL水平；RECAP（仅重复上一轮信息）的改善更为有限。这表明简单的信息重复只能部分缓解问题，无法从根本上解决模型在多轮对话中的迷失。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/015_Table_5.jpg]]
*Table 5: Experimental Results with additional simulation types: Recap and Snowball. Both strategies involve repeating user-turn information to mitigate models getting lost in conversations. Table 6: Comparing performance in SHARDED conversations of GPT-4o given no system prompt (default) vs. providing a specialized system prompt hinting that the conversation will likely be underspecified. Results reported on four tasks: Math, Actions, Database, and Code*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/016_Table_7.jpg]]
*Table 7: Unreliability of models when changing assistant temperature (AT) and user temperature (UT) in FULL, CONCAT and SHARDED settings. The lower the number the more reliable the assistant is*

### 翻译任务的边界案例

值得注意的是，**翻译任务**在SHARDED设定下未表现出明显的性能退化（**Table 8**），FULL与SHARDED的BLEU得分差异在10%以内。这为理解“迷失”现象的边界条件提供了线索：翻译任务中，每片信息（待翻译的句子）本身就是独立完整的子任务，模型无需跨轮次整合信息即可完成，因而避开了多轮对话中的信息整合困境。

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/017_Table_8.jpg]]
*Table 8: Performance on the translation task for FULL, CONCAT, and SHARDED simulations*

### 补充图表

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/001_Figure_1.jpg]]
*Figure 1: Our simulated conversations for 6 generation tasks on the 15 LLMs observe a major performance drop in multi-turn settings (-39%), explained by some loss in Aptitude, and large loss in Reliability*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/008_Table_2.jpg]]
*Table 2: Results of the manual inspection of 100 simulated SHARDED conversations across four tasks: Actions, Code, Math, and Database. The first column aggregates annotation results on the four tasks*

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/014_Table.jpg]]

![[assets/figures/papers/paper_list_l21_https_openreview_net_forum_id_VKGTGGcwl6/figures/018_Table_9.jpg]]
*Table 9: Definition of turn categories. We include the description in the prompt to categorize assistant responses*



## 定位与知识库关联

### 核心方法定位：从单轮基准到多轮仿真的范式迁移

本文的核心贡献在于提出了一种**信息揭示节奏可控的多轮对话仿真框架**（Sharded Simulation Framework），其本质是将传统单轮指令遵循基准（如 BIG-Bench、HumanEval 等）中“一次性完整提供指令”的评估范式，系统性地迁移到“逐轮揭示信息”的多轮对话场景中。这一迁移揭示了当前 LLM 评估体系中的一个关键盲区：**实验室单轮性能无法外推至真实多轮交互场景**。

与该框架形成对比的基线设定包括：

- **FULL 设定**（单轮完整指令基线）：代表理想化的实验室性能，即一次性在首轮提供完整指令。这是传统 LLM 评估的默认范式，也是本文所有性能退化的参照基准。
- **CONCAT 设定**（单轮拼接分片）：将分片后的所有信息在单轮中拼接提供，用于控制“重新措辞”本身的混淆效应。实验表明，CONCAT 性能平均达到 FULL 的 95.1%，说明性能退化的主因并非信息的重新表述，而是**多轮逐片揭示的交互节奏**。
- **Episodic multi-turn evaluation**（先行工作）：将多轮对话视为一组可独立评估的子任务。本文认为该方法**高估了模型能力**，因为它忽略了模型在多轮对话中因过早承诺、过度依赖先前错误回答而产生的累积性退化。

### 方法谱系中的位置：填补评估生态的空白

在 LLM 评估方法谱系中，本文的工作处于**单轮基准评估**与**真实人机对话评估**之间的中间地带。其核心创新在于：

1. **可控性**：通过半自动分片流程（Segmentation → Rephrasing → Verification → Manual Inspection），将真实对话的不可控性转化为信息揭示节奏的单一调节变量，使因果分析成为可能。
2. **可复现性**：仿真用户（基于 GPT-4o-mini）和标准化评估流程确保了大规模、低成本的实验可复现性（200,000+ 次模拟，总成本约 $5,000）。
3. **粒度分析**：通过引入能力（Aptitude, $A^{90}$）和不可靠性（Unreliability, $U_{10}^{90}$）的分解，将“性能下降”这一粗粒度指标拆解为两个可独立追踪的因果通道。

### 适用边界与泛化限制

本文的实验设计存在明确的适用边界，需在引用其结论时谨慎对待：

| 维度 | 覆盖范围 | 未覆盖/限制 |
|------|---------|------------|
| **任务类型** | 六项生成式任务（Code, Database, Actions, Math, Data-to-text, Summary） | 创意性任务（故事写作、诗歌等）、翻译任务（实验显示无明显退化） |
| **语言** | 仅英文 | 多语言环境下的表现未知 |
| **对话长度** | 上下文基本控制在 20k tokens 内 | 超长对话（数百轮）中的累积效应未测试 |
| **用户行为** | 基于 GPT-4o-mini 的仿真用户 | 真实用户的不可预测性可能使实际退化更严重 |
| **模型范围** | 15 个主流 LLM（涵盖开源与闭源） | 部分模型（Phi-4、OLMo-2-13B）因上下文限制被排除在摘要任务外 |
| **缓解策略** | 仅探索了 RECAP 和 SNOWBALL 两种基于重复的简单策略 | 更复杂的 agent 设计（如显式记忆模块、反思机制）未被涵盖 |

### 关键局限与证据强度评估

**强证据支持的结论**（confidence ≥ 0.9）：
- 所有模型在所有任务上均出现性能退化，平均 -39%（Table 1）。
- 退化的主因是不可靠性飙升（平均 +112%），而非能力显著下降（仅 -16%）（Figure 5b）。
- 即使仅拆分为 2 个分片（即至少两轮对话），不可靠性已大幅上升（Figure 5c）。
- 降低温度至 0.0 无法有效缓解多轮不可靠性（Table 7）。

**需要手动验证或进一步研究的结论**：
- 根因分析（过早尝试完整答案、冗长回复、“中间轮次丢失”）基于相关性和观察，而非直接的因果干预实验。论文自身承认这一点，因此这些归因应被视为**强假设**而非已证实的因果机制。
- 仿真用户的错误率虽低于 5%，但在大规模模拟中仍可能引入系统性偏差，尤其是在模型对用户措辞敏感的边界情况下。
- 由于使用商业 API 且模型版本持续更新，完全重现实验结果具有挑战性。

### 开放问题与未来方向

本文揭示的现象为后续研究打开了若干关键方向：

1. **泛化边界的确立**：创意性任务、多语言、多模态场景下的退化程度是否同样严重？翻译任务的“免疫”现象是否暗示某些任务结构天然抗退化？
2. **根本性修复路径**：如何通过训练或架构改进赋予 LLM 在多轮对话中**恢复和重新聚焦**的能力，而非仅依赖外部提示工程（如 RECAP/SNOWBALL 仅带来 15-20% 的改善）？
3. **推理模型的潜力挖掘**：推理模型（如 o3、R1）为何未表现出明显优势？是否可以在多轮对话中优化 test-time compute 的使用策略？
4. **人因研究的必要性**：用户交互研究能否揭示这种不可靠性如何影响真实用户的信任和采用决策？仿真框架的结论在多大程度上能迁移到真实人机对话中？



## 原文 PDF

![[paperPDFs/ICLR_2026/LLMs_Get_Lost_In_Multi_Turn_Conversation.pdf]]
