---
title: "BIRD-INTERACT: Re-imagining Text-to-SQL Evaluation via Lens of Dynamic Interactions"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BIRD_INTERACT_Re_imagining_Text_to_SQL_Evaluation_via_Lens_of_Dynamic_Interactions.pdf
project_link: https://bird-interact.github.io
code_link: null
openreview_forum_id: nHrYBGujps
aliases:
- BIB
- BIRD-INTERACT
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "动态交互环境与功能驱动的用户模拟器：强制LLM在歧义查询、知识缺失和执行错误时主动请求澄清并合理调用环境资源，将评估重心从单步SQL生成转向端到端的交互式问题解决。"
primary_logic: "通过将全CRUD操作、五种歧义类型、状态依赖的后续子任务和可控的两阶段用户模拟器集成到基准中，可以准确暴露LLM在对话沟通、规划与推理方面的短板，从而为构建实用的多轮数据库助手提供明确的改进方向。"
claims:
- "GPT-5 在 BIRD-INTERACT-FULL 的 c-Interact 模式下仅完成 8.67% 的任务，a-Interact 模式下完成 17.00%，远低于理想单轮性能。"
- "记忆嫁接（Memory Grafting）实验表明，GPT-5 使用其他模型的高质量交互历史后，成功率显著提升，证明沟通交互能力是限制其性能的主要瓶颈。"
- "基准用户模拟器在处理不可回答问题（UNA）时失败率高达 67.4%，而函数驱动方法将失败率降至 2.7%，大幅提升了模拟器的鲁棒性。"
- "交互测试时缩放（ITS）规律表明，Claude-3.7-Sonnet 的成功率随交互耐心值的增加而单调提升，验证了更多交互机会能够持续转化为信息增益。"
---

# BIRD-INTERACT: Re-imagining Text-to-SQL Evaluation via Lens of Dynamic Interactions

> [!tip] 核心洞察
> 通过将全CRUD操作、五种歧义类型、状态依赖的后续子任务和可控的两阶段用户模拟器集成到基准中，可以准确暴露LLM在对话沟通、规划与推理方面的短板，从而为构建实用的多轮数据库助手提供明确的改进方向。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BIRD-INTERACT：通过动态交互视角重新构想文本到SQL评估 |
| 英文题名 | BIRD-INTERACT: Re-imagining Text-to-SQL Evaluation via Lens of Dynamic Interactions |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=nHrYBGujps) · [Project](https://bird-interact.github.io) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | BIRD-INTERACT Benchmark |
| Dataset | BIRD-INTERACT-FULL, BIRD-INTERACT-LITE, UserSim-Guard |

> [!tip] 效果简介
> - BIRD-INTERACT-FULL 上，Overall Task Success Rate (c-Interact 模式) 为 最强对话助手 Gemini-2.5-Pro：16.33% (后续子任务)，对比 GPT-5：8.67% (后续子任务)，变化 +7.66%。
> - BIRD-INTERACT-FULL 上，Normalized Reward (a-Interact 模式) 为 GPT-5：25.52%，对比 Qwen-3-Coder-480B：10.58%，变化 +14.94%。
> - BIRD-INTERACT-LITE 上，Overall Task Success Rate (c-Interact 模式) 为 O3-Mini：37.33% (优先问题)，对比 DeepSeek-V3：22.00% (优先问题)，变化 +15.33%。

## 概要

现有文本到SQL基准（如**Spider**、**BIRD**、**SParC**、**CoSQL**）普遍采用静态交互历史与仅读（SELECT-only）操作，无法反映生产环境中多轮、有状态、需主动澄清和错误恢复的真实数据库交互，导致LLM的能力被系统性高估。**BIRD-INTERACT** 针对这一瓶颈，构建了首个覆盖全CRUD操作、注入五类歧义并引入状态依赖子任务的动态交互基准，通过功能驱动的用户模拟器与两种评估模式（c-Interact与a-Interact），将评估重心从单步SQL生成转向端到端的交互式问题解决。

核心结论表明，当前最强模型在真实交互场景下表现远低于理想单轮性能：**GPT-5** 在 BIRD-INTERACT-FULL 的 c-Interact 模式下仅完成 **8.67%** 的任务，a-Interact 模式下完成 **17.00%**。记忆嫁接实验进一步证实，沟通交互能力——而非SQL生成能力——是限制其性能的主要瓶颈。交互测试时缩放（ITS）规律显示，Claude-3.7-Sonnet 的成功率随交互耐心值的增加而单调提升，验证了更多交互机会可转化为持续的信息增益。

在方法定位上，BIRD-INTERACT 继承 **LIVESQLBENCH** 的可执行数据库环境与全CRUD任务基础，通过歧义注入、后续子任务生成和两阶段函数驱动用户模拟器，将静态单轮评估转化为动态多轮交互评估。其用户模拟器在不可回答问题（UNA）上的失败率从基线方法的 **67.4%** 降至 **2.7%**，大幅提升了评估的鲁棒性与可控性。

### 文本到SQL评估的静态困境

文本到SQL（Text-to-SQL）旨在将自然语言查询自动转换为可执行的SQL语句，是数据库交互智能化的核心技术。近年来，以**Spider**（Yu et al., 2018）和**BIRD**（Li et al., 2023b）为代表的基准数据集推动了该领域的快速发展，使大语言模型（LLM）在单轮、无歧义的SELECT查询上取得了令人瞩目的成绩。然而，这些基准所定义的“成功”与现实世界中数据库助手面临的挑战之间存在深刻鸿沟。

现有基准存在三个系统性缺陷。其一，**交互范式静态化**：无论是Spider还是BIRD，均采用单轮输入输出的评估模式，模型只需接收一条完整、无歧义的自然语言查询并生成SQL即可。即便**SParC**（Yu et al., 2019a）和**CoSQL**（Yu et al., 2019b）引入了多轮对话，它们依赖的仍是预先录制的静态对话历史，模型无法主动向用户提问以澄清歧义或获取缺失信息。其二，**操作范围受限**：主流基准几乎全部局限于SELECT查询，服务于商业智能（BI）场景，而完全忽略了INSERT、UPDATE、DELETE等数据管理（DM）操作——这些操作恰恰是生产环境中数据库交互的核心组成部分。其三，**环境状态缺失**：所有任务相互独立，不存在子任务间的状态依赖。模型无需关心前序操作对数据库状态的修改，也无需处理因环境不确定性引发的错误。

### 能力被系统性高估

上述缺陷导致LLM的真实交互能力被严重高估。当我们将模型置于一个需要主动澄清歧义、处理全CRUD操作、并在修改后的数据库状态上进行推理的真实交互场景时，性能断崖式下跌。以GPT-5为例，其在理想化的单轮无歧义任务上表现优异，但在**BIRD-INTERACT-FULL**的交互式评估中，c-Interact模式下的任务完成率仅为8.67%，a-Interact模式下也仅有17.00%（见Table 2）。这一差距揭示了当前评估体系的核心盲区：**现有基准衡量的是模型的SQL生成能力，而非端到端的交互式问题解决能力**。

### 从单步生成到交互式问题解决

真实场景下的数据库交互远非单步SQL生成所能概括。用户查询往往存在意图层面的模糊（“帮我查一下最近的订单”）、实现层面的歧义（“按时间排序”未指明升序还是降序），或依赖模型中不存在的领域知识（“VIP客户的定义是什么？”）。此外，数据库环境本身可能因前序操作而发生变化，模型需要理解并适应这种状态迁移。

这些挑战要求系统具备以下能力：（1）**主动澄清**——在歧义出现时向用户提问，而非猜测或失败；（2）**环境探索**——在知识缺失时检索数据库Schema或外部知识库；（3）**错误恢复**——在执行失败时分析原因并修正SQL；（4）**状态推理**——在数据库状态被前序子任务修改后，基于新状态生成后续查询。这些能力构成了“交互式问题解决”的核心，而现有基准无一能够全面评估。

### 本文动机与核心主张

针对上述缺口，本文提出**BIRD-INTERACT**基准，其核心主张是：**通过构建动态交互环境与功能驱动的用户模拟器，将文本到SQL评估从单步生成范式转向端到端的交互式问题解决范式**。具体而言，BIRD-INTERACT在三个维度上实现了突破：

1. **全CRUD操作覆盖**：任务同时涵盖BI查询与DM操作，由可执行测试用例进行功能等价性验证。
2. **歧义系统注入**：引入用户查询歧义、知识歧义（含知识链断裂）与环境歧义三类歧义，强制模型通过主动澄清获取必要信息。
3. **状态依赖的子任务链**：后续子任务的正确执行依赖于前序子任务对数据库状态的修改，模拟真实的操作序列。

通过上述设计，BIRD-INTERACT不仅暴露了当前最强LLM在交互式数据库任务上的显著短板，也为构建实用的多轮数据库助手提供了明确的改进方向与评估工具。

## 核心方法与创新机理

BIRD-INTERACT 的核心创新在于将文本到 SQL 的评估从静态、单轮、只读的范式推向**动态、多轮、全 CRUD 的交互式问题解决**。这一转变通过以下五个相互耦合的维度实现，每个维度都直接针对现有基准的系统性缺陷。

### 1. 从单轮静态到多轮动态交互

传统基准（如 **Spider** (Yu et al., 2018)、**BIRD** (Li et al., 2023b)）将评估简化为“输入查询→输出 SQL”的单步映射，完全忽略了生产环境中用户需求逐步澄清、系统主动提问的交互本质。BIRD-INTERACT 引入了两种互补的交互模式：

- **c-Interact**：遵循预定义对话协议的多轮对话模式，系统在受控的澄清轮次预算内与用户模拟器交互。预算公式为 $\tau_{\mathrm{clar}} = m_{\mathrm{amb}} + \lambda_{\mathrm{pat}}$，其中 $m_{\mathrm{amb}}$ 是必要歧义数，$\lambda_{\mathrm{pat}}$ 是用户耐心值。
- **a-Interact**：遵循 REACT 范式的开放代理模式，系统在预定义动作空间内自主规划与执行，总预算为 $B = B_{\mathrm{base}} + 2 m_{\mathrm{amb}} + 2 \lambda_{\mathrm{pat}}$。

这一设计使评估重心从“能否生成正确的 SQL”转向“能否通过有效沟通与规划解决用户问题”。实验证明，即使是最强模型 Gemini-2.5-Pro 在 c-Interact 下也只能完成 16.33% 的任务（后续子任务），GPT-5 在 a-Interact 下仅完成 17.00%，远低于它们在无歧义单轮设置下的理想性能。

### 2. 歧义注入：构建真实世界的不确定性

现有基准假设用户查询是完备且无歧义的，这与实际场景严重脱节。BIRD-INTERACT 系统性地注入了三类歧义：

- **用户查询歧义**：包括意图级别（如“重要客户”未定义）和实现级别（如聚合粒度不明确）的模糊性。
- **知识歧义**：通过**知识链断裂**（Knowledge Chain Breaking）遮蔽多跳知识链中的中间节点，迫使模型主动询问缺失的关联信息。
- **环境歧义**：模拟数据库对象不存在、权限不足等运行时不确定性。

这些歧义不是简单的噪声，而是需要模型识别信息缺口并主动发起澄清的结构化挑战。记忆嫁接实验提供了强有力的因果证据：当 GPT-5 使用 Qwen-3-Coder 或 O3-mini 的高质量交互历史后，优先问题成功率显著提升，说明**沟通交互能力（而非 SQL 生成能力）才是限制其性能的主要瓶颈**。

### 3. 状态依赖的子任务链

**CoSQL** (Yu et al., 2019b) 等对话式基准虽然支持多轮交互，但其问题之间相互独立，不涉及数据库状态的修改与继承。BIRD-INTERACT 的关键贡献在于引入了**子任务间的状态依赖**：后续子任务（如修改或查询）依赖于前序子任务执行后修改的数据库状态或新创建的对象。系统模型必须对修改后的数据库状态进行推理，而非仅仅理解静态的 schema。这一设计将评估从“孤立查询”提升为“事务性操作序列”，更贴近数据管理（DM）场景的真实需求。

### 4. 函数驱动的用户模拟器

用户模拟器是交互式基准的核心组件，但普通 LLM 模拟器存在严重的信息泄露问题：在处理不可回答问题（UNA）时，基线模拟器的失败率高达 67.4%。BIRD-INTERACT 提出了**两阶段函数驱动模拟器**：

- **第一阶段**：LLM 解析器将系统的澄清请求分类为三种预定义动作之一——`AMB()`（歧义澄清）、`LOC()`（知识定位）、`UNA()`（不可回答）。
- **第二阶段**：根据分类结果生成受控响应。对于 `LOC()` 动作，使用 AST 检索定位相关 SQL 片段，防止真值泄露。

这一设计将 UNA 场景下的模拟器失败率降至 2.7%，同时使 AI 模拟器与人类用户成功率之间的皮尔逊相关系数从 0.61 提升至 0.84（GPT-4o，p=0.02），大幅提升了评估的可靠性与公平性。

### 5. 全 CRUD 操作覆盖与双场景任务设计

**LIVESQLBENCH** (BIRD-Team, 2025) 已提供全 CRUD 任务的基础，BIRD-INTERACT 在此基础上增加了交互层和歧义注入。与仅支持 SELECT 的 **CoSQL** 不同，BIRD-INTERACT 同时覆盖商业智能（BI）与数据管理（DM）两大类场景，使基准能够评估系统在分析查询和事务性操作两种范式下的综合能力。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_nHrYBGujps/figures/001_Figure_1.jpg]]
*Figure 1: Task overview of BIRD-INTERACT showing the evaluated system interacting with DB Environment and User Simulator to complete the user task with a sequence of sub-tasks*

BIRD-INTERACT 的核心设计理念是将文本到 SQL 的评估从静态的单轮生成任务重构为**动态的多轮交互问题解决过程**。整个框架围绕三个关键实体展开：被评估的系统模型 $S_\theta$、函数驱动的用户模拟器 $\mathcal{U}_\gamma$，以及一个可执行的数据库环境 $\mathcal{E}$。三者通过结构化的交互协议耦合，形成完整的评估闭环（Figure 1）。

### 交互流程与状态更新

框架的交互过程遵循统一的多轮状态更新机制。对于第 $i$ 个子任务，在第 $t$ 轮交互中，用户模拟器根据当前交互历史 $h_i^{t-1}$、子任务目标 $q_i$ 和环境 $\mathcal{E}$ 生成用户响应 $u_i^t$；系统模型随后基于更新后的历史、用户响应和环境信息生成系统输出 $s_i^t$；交互历史通过拼接本轮输入输出进行更新：

$$u_i^t = \mathcal{U}_\gamma(h_i^{t-1}, q_i, \mathcal{E}), \quad s_i^t = S_\theta(h_i^{t-1}, u_i^t, \mathcal{E}), \quad h_i^t = h_i^{t-1} \oplus \langle u_i^t, s_i^t \rangle$$

这一设计强制系统模型在信息不完整时主动发起澄清请求，而非被动接受单轮输入。

### 核心模块与数据流

框架由五个关键模块构成，形成从任务构建到评估执行的完整流水线：

**1. 歧义注入与标注模块** 负责将 LIVESQLBENCH 的单轮任务转换为交互式场景。该模块系统性地注入三类歧义：
- **表层用户查询歧义**：用户意图本身存在模糊性，需要系统主动澄清
- **知识歧义**：通过知识链断裂（masking intermediate nodes in multi-hop knowledge chains）制造信息缺口，迫使模型识别知识缺失并请求补充
- **环境歧义**：模拟数据库环境中的不确定性

**2. 后续子任务生成模块** 基于五类分类法生成依赖于先前状态的后续子任务，形成完整的交互链。关键设计在于：**后续子任务仅在首个子任务成功完成后才被释放**，引入了状态依赖——系统必须对修改后的数据库状态或新创建的对象进行推理。这使得评估从独立的 SQL 生成扩展到包含 CRUD 操作后果的端到端问题解决。

**3. 函数驱动用户模拟器** 采用两阶段设计以防止真值泄露：
- **第一阶段（LLM 解析器）**：将系统模型的澄清请求分类为三种预定义动作之一——`AMB()`（歧义澄清）、`LOC()`（定位相关 SQL 片段）、`UNA()`（不可回答问题）
- **第二阶段（受控响应生成）**：根据分类结果生成精确回答。对于 `LOC()` 动作，使用 AST 检索步骤定位相关 SQL 片段，避免直接暴露完整答案

该设计将基线模拟器在不可回答问题上的失败率从最高 67.4% 降至最低 2.7%（Figure 6），大幅提升了模拟器的鲁棒性。

**4. 评估协议管理器** 实现两种互补的评估模式：
- **c-Interact**：预定义对话协议模式，澄清轮次受预算约束 $\tau_{\mathrm{clar}} = m_{\mathrm{amb}} + \lambda_{\mathrm{pat}}$，其中 $m_{\mathrm{amb}}$ 为必要歧义数，$\lambda_{\mathrm{pat}}$ 为用户耐心值
- **a-Interact**：遵循 REACT 范式的自主代理模式，系统在预定义动作空间内自主规划与执行，任务总预算为 $B = B_{\mathrm{base}} + 2 m_{\mathrm{amb}} + 2 \lambda_{\mathrm{pat}}$，其中基础预算 $B_{\mathrm{base}}=6$

两种模式均包含预算约束，模拟真实场景中的交互成本限制。

**5. 可执行测试与奖励系统** 为每个子任务提供可执行测试用例进行功能等价性验证。预测 SQL $\sigma_{i,j}$ 通过所有测试用例 $\mathcal{T}_{i,j}$ 时视为正确：

$$\mathrm{SR}_j = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}[\mathcal{T}_{i,j}(\sigma_{i,j}) = \mathrm{True}]$$

归一化奖励根据评估模式采用不同的计算方式：a-Interact 模式下单任务奖励依据两个子任务的通过状态给予离散分数（1.0/0.7/0），c-Interact 模式则按完成阶段和调试情况进行加权。

### 与已有基准的关键差异

BIRD-INTERACT 在多个维度上突破了已有基准的局限（Table 4）。与 **Spider**（Yu et al., 2018）、**BIRD**（Li et al., 2023b）等单轮基准相比，它引入了动态交互层和歧义处理；与 **SParC**（Yu et al., 2019a）、**CoSQL**（Yu et al., 2019b）等依赖静态对话历史的多轮基准相比，它提供了函数驱动的用户模拟器和可执行环境；与 **LIVESQLBENCH**（BIRD-Team, 2025）相比，它在全 CRUD 操作基础上增加了交互层和歧义注入。平均交互轮次达到 7.46-7.83 轮，远超其他交互式基准。

### 问题定义与交互范式

BIRD-INTERACT 将文本到SQL任务形式化为系统模型 $S_\theta$ 与用户模拟器 $\mathcal{U}_\gamma$ 在数据库环境 $\mathcal{E}$ 中的多轮交互过程。对于包含 $N$ 个子任务的任务 $i$，第 $t$ 轮交互的状态更新由以下公式定义：

$$u_i^t = \mathcal{U}_\gamma(h_i^{t-1}, q_i, \mathcal{E}), \quad s_i^t = S_\theta(h_i^{t-1}, u_i^t, \mathcal{E}), \quad h_i^t = h_i^{t-1} \oplus \langle u_i^t, s_i^t \rangle$$

其中 $h_i^t$ 为截至第 $t$ 轮的交互历史，$u_i^t$ 为用户模拟器在当前轮次发出的输入（可能是新子任务或对系统澄清请求的回应），$s_i^t$ 为系统模型的输出（SQL 语句或澄清问题），$\oplus$ 表示历史拼接操作。该框架的核心约束在于：**后续子任务仅在先前子任务成功完成后才会被释放**，从而引入了状态依赖——系统必须基于被修改的数据库状态或新创建的对象进行推理。

### 歧义注入模块

基准构建的关键模块是将 LIVESQLBENCH 的单轮任务转换为多轮交互场景，通过两类标注策略实现：

1. **歧义注入**：在原始查询中系统性地引入三类歧义——
   - 表层用户查询歧义（意图级与实现级，共含五类细分子类型）
   - 知识歧义，包括**知识链断裂**——遮蔽多跳知识链中的中间节点，迫使模型主动询问缺失的依赖关系
   - 环境歧义，模拟数据库状态的不确定性

2. **后续子任务生成**：基于五类原则生成依赖于先前子任务执行结果的后续子任务，形成完整的交互链。

### 函数驱动用户模拟器

用户模拟器采用两阶段函数驱动设计，以防止真值泄露并确保响应可控：

- **第一阶段（动作分类）**：将系统的澄清请求映射到三个预定义动作之一——`AMB()`（歧义澄清）、`LOC()`（定位相关SQL片段）、`UNA()`（不可回答问题）
- **第二阶段（响应生成）**：根据分类结果生成精确回答。对于 `LOC()` 动作，模拟器通过基于 AST 的检索步骤定位相关 SQL 片段后返回

该设计与普通 LLM 模拟器形成关键区别：基线模拟器在 `UNA()` 问题上失败率高达 67.4%，而函数驱动方法将失败率降至 2.7%，大幅提升了模拟器的鲁棒性。

### 评估协议与预算约束

BIRD-INTERACT 定义两种评估模式，分别对应不同的交互预算公式：

**c-Interact 模式**（对话助手）：系统在预定义对话协议内进行多轮澄清，总允许澄清轮次为：

$$\tau_{\mathrm{clar}} = m_{\mathrm{amb}} + \lambda_{\mathrm{pat}}$$

其中 $m_{\mathrm{amb}}$ 为任务中标注的歧义点数（必要澄清预算），$\lambda_{\mathrm{pat}}$ 为用户耐心参数（默认值为 3）。

**a-Interact 模式**（自主代理）：系统遵循 REACT 范式在预定义动作空间内自主规划与执行，任务总预算为：

$$B = B_{\mathrm{base}} + 2 m_{\mathrm{amb}} + 2 \lambda_{\mathrm{pat}}$$

其中基础预算 $B_{\mathrm{base}} = 6$，歧义点数和耐心参数的系数为 2，反映代理模式下更高的交互自由度需求。

### 奖励函数

系统的最终表现通过可执行测试用例进行功能等价性验证。第 $j$ 个子任务的成功率定义为：

$$\mathrm{SR}_j = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}[\mathcal{T}_{i,j}(\sigma_{i,j}) = \mathrm{True}]$$

即预测 SQL $\sigma_{i,j}$ 通过所有关联测试用例 $\mathcal{T}_{i,j}$ 的任务比例。总体归一化奖励为：

$$R = \frac{\sum_i r_i}{N} \times 100$$

其中单任务奖励 $r_i$ 在 a-Interact 模式下采用离散评分：

$$r_i = \begin{cases} 1.0 & \text{两个子任务均通过} \\ 0.7 & \text{仅第一个子任务通过} \\ 0 & \text{其他情况} \end{cases}$$

c-Interact 模式则采用更细粒度的分阶段奖励计算（含调试阶段的增量收益）。

## 实验与关键发现

### 核心结果：LLM 在交互式文本到SQL任务中表现远低于理想单轮性能

BIRD-INTERACT-FULL 基准上的主实验揭示了当前最强 LLM 在真实交互场景下的系统性能力缺陷。如 Table 2 所示，即使是最先进的对话助手 **Gemini-2.5-Pro**，在 c-Interact 模式下仅完成 **16.33%** 的后续子任务；而在 a-Interact 模式下，**GPT-5** 虽取得最佳优先问题成功率（29.17%），但其整体任务成功率仅为 **17.00%**。归一化奖励指标进一步印证了这一困境：Gemini-2.5-Pro 和 GPT-5 在两种模式下分别仅捕获了 20.92% 和 25.52% 的可用奖励。这些数字与理想单轮性能（Figure 4 虚线所示）之间存在巨大鸿沟，表明**静态单轮评估系统性高估了 LLM 的实际数据库交互能力**。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_nHrYBGujps/figures/005_Table_2.jpg]]
*Table 2: Success Rate and Final Normalized Reward of different models on BIRD-INTERACT-FULL. The success rate is cumulative; Reward* is the normalized reward. The values reported in c-Interact are after debugging phase, and (+n) means the performance gained via debugging. Avg. Cost is the cost for one task on average in USD. Our user simulator has an avg. cost of 0.03 USD. BI = Business Intelligence User Queries, DM = Data Management User Queries*

模型在不同交互模式下呈现出显著的性能反转。GPT-5 在 c-Interact 模式中表现最差（优先问题成功率仅 14.50%），却在 a-Interact 中跃居首位；而 Gemini-2.5-Pro 则在 c-Interact 中表现最优。这种模式依赖性提示：**模型的训练数据分布与架构归纳偏置深刻影响着其交互策略的有效性**，不存在统一的“最强模型”。

BIRD-INTERACT-LITE 子集上的结果（Table 10）呈现相似趋势，但整体成功率更高。O3-Mini 在 c-Interact 模式下优先问题成功率达到 37.33%，而 DeepSeek-V3 仅为 22.00%，差距达 15.33 个百分点。值得注意的是，所有模型在 LITE 上的性能仍远未饱和，说明即使简化任务规模，交互式数据库助手的能力瓶颈依然突出。

### 交互测试时缩放规律：更多交互机会持续转化为信息增益

Figure 4 展示了 BIRD-INTERACT-LITE 上不同用户耐心参数下的性能变化，揭示了清晰的**交互测试时缩放（Interaction-Time Scaling, ITS）规律**。以 **Claude-3.7-Sonnet** 为例，在 c-Interact 模式下，当用户耐心从 0 提升至 7 时，优先问题成功率从约 8% 单调上升至约 30%+，增幅超过 22 个百分点。这种单调递增趋势在多个模型上复现，验证了**更多交互机会能够持续转化为信息增益**，符合 ITS 定律的核心预测。

然而，缩放曲线的斜率在不同模型间差异显著。部分模型（如 GPT-4o）在耐心值达到 3 后出现收益递减，而 Claude-3.7-Sonnet 则持续受益于额外交互轮次。这表明**模型利用交互机会的效率存在本质差异**，可能源于其规划与信息整合能力的上限不同。

### 记忆嫁接实验：沟通交互能力是 GPT-5 的核心瓶颈

Figure 5 展示的记忆嫁接（Memory Grafting）实验为诊断性能瓶颈提供了因果证据。当 GPT-5 被注入来自 **Qwen-3-Coder** 或 **O3-mini** 的成功交互历史后，其优先问题成功率显著提升。这一结果表明：**GPT-5 的 SQL 生成能力本身并非限制因素，其核心短板在于沟通交互策略**——即无法有效提出澄清问题、识别知识缺口并整合用户反馈。该发现直接指向了未来改进方向：与其追求更强的代码生成能力，不如着力提升模型在对话沟通与主动信息获取方面的能力。

### 行动分布分析：过早依赖执行试错阻碍任务成功

对 a-Interact 模式下模型行动序列的分析（Figure 11, Figure 12）揭示了成功与失败轨迹的结构性差异。**提交（submit）动作比例与优先问题成功率呈正相关（r≈0.41），而执行（execute）动作比例呈负相关（r≈-0.52）**。成功模型倾向于遵循“先探索环境（get_schema, get_knowledge_definition），再提交”的模式，而失败模型则过早陷入“执行-试错”循环。这一发现表明：**在代理模式下，策略性的信息收集比盲目的代码执行更为关键**，当前模型普遍缺乏有效的元认知来规划探索与利用的平衡。

### 用户模拟器评估：函数驱动方法大幅提升鲁棒性

用户模拟器的质量直接影响基准评估的可信度。在 UserSim-Guard 基准上（Table 11），基线 LLM 模拟器在处理不可回答问题（UNA）时失败率高达 **67.4%**，存在严重的真值泄露风险。而论文提出的**两阶段函数驱动模拟器**将失败率降至最低 **2.7%**（GPT-4o 骨干），同时在 AMB 和 LOC 类别上保持高准确率（97.3% UNA 准确率）。Table 3 的相关性分析进一步证实：函数驱动模拟器与人类用户成功率之间的 Pearson 相关系数达到 0.84（p=0.02），显著优于无函数调用的基线（r=0.61, p=0.14），验证了其作为人类用户可靠代理的有效性。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_nHrYBGujps/figures/040_Table_11.jpg]]
*Table 11: Accuracy (%) of user simulators on the UserSim-Guard benchmark using updated evaluation results. Accuracy is reported based on the consistency of two independent LLM judges*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_nHrYBGujps/figures/009_Table_3.jpg]]
*Table 3: Correlation analysis between AI and human users*

### 失败模式与成本分析

所有模型在 BIRD-INTERACT 上的低成功率揭示了当前 LLM 在以下关键能力上的系统性不足：（1）**歧义识别与主动澄清**——模型常忽略查询中的意图歧义或知识链断裂，直接生成错误 SQL；（2）**状态依赖推理**——后续子任务需基于前序操作修改的数据库状态，多数模型无法正确追踪状态变化；（3）**预算约束下的策略规划**——尤其在 a-Interact 模式中，模型未能合理分配有限的行动预算。

成本方面（Table 2），GPT-5 平均每任务成本为 $0.08，而 Claude-Sonnet-4 高达 $0.29，Gemini-2.5-Pro 仅 $0.04。用户模拟器的平均成本为 $0.03/任务，在可控范围内。成本与性能之间未呈现单调关系，说明更昂贵的模型未必具备更强的交互能力。

**注意**：Table 3（人机相关性分析）的具体数值、Figure 11/12（行动分布相关性）的完整图表数据需查阅原文确认细节，本节仅基于分析锚点给出已验证的关键结论。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_nHrYBGujps/figures/011_Table_4.jpg]]
*Table 4: Data statistics of features in BIRD-INTERACT compared to the evaluation set of related benchmarks. # Avg Turns: Number of User-System interactions by unfolding the model’s interaction trajectory. # Toks./Output: Average number of tokens in the reference output; “/” indicates benchmarks without reference output. Dynamic User: Whether the benchmark supports real-time user interaction (vs. static offline datasets). Dynamic Env State: Whether the database or environment state can be modified during interaction. Amb. Sources: Sources of ambiguity in user queries or environments. LLM + Guard means LLM as user simulator with Guard mechanism to make actions more controllable. [†]: Results taken fro...*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_nHrYBGujps/figures/012_Table_5.jpg]]
*Table 5: Comparison of released databases across benchmarks*

## 定位与知识库关联

### 与现有基准的关系

BIRD-INTERACT 并非从零构建，而是在 **LIVESQLBENCH**（BIRD-Team, 2025）的单轮全 CRUD 任务基础上，通过系统性地注入交互层和歧义机制构建而成。这一设计选择使其与现有文本到 SQL 基准形成了清晰的继承与超越关系：

- **相对于经典单轮基准**：**Spider**（Yu et al., 2018）和 **BIRD**（Li et al., 2023b）分别解决了跨数据库泛化和外部知识利用问题，但两者均假设输入查询无歧义、无需用户交互。BIRD-INTERACT 通过注入三类歧义（用户查询歧义、知识歧义、环境歧义）并引入功能驱动的用户模拟器，将评估重心从单步 SQL 生成转向端到端的交互式问题解决。实验表明，在消除歧义后的理想单轮性能（Idealized Performance，见 Figure 4 虚线）与 c-Interact 模式下的实际成功率之间存在巨大鸿沟——例如 Claude-3.7-Sonnet 在耐心=0 时成功率仅约 8%，而理想单轮性能远高于此——这直接暴露了传统基准对 LLM 能力的系统性高估。

- **相对于多轮/对话式基准**：**SParC**（Yu et al., 2019a）和 **CoSQL**（Yu et al., 2019b）引入了多轮对话，但依赖静态对话历史，用户侧无动态模拟，且 CoSQL 局限于 SELECT 查询。BIRD-INTERACT 的关键突破在于：① 覆盖全 CRUD 操作，使数据库状态在交互过程中发生实质性修改；② 后续子任务依赖于先前子任务执行后的数据库状态（状态依赖），而不仅是对话上下文依赖；③ 用户模拟器可动态响应系统的澄清请求，而非回放固定脚本。这一设计使得 BIRD-INTERACT 成为目前唯一同时具备“动态用户模拟 + 全 CRUD + 状态依赖子任务”的交互式文本到 SQL 基准。

### 适用边界

BIRD-INTERACT 的评估框架适用于以下场景，但存在明确边界：

1. **适用场景**：需要多轮澄清、主动信息获取和错误恢复的数据库助手系统，涵盖商业智能（BI）查询和数据管理（DM）操作。两种评估模式分别对应不同部署形态——c-Interact 模拟对话助手（受控澄清流程），a-Interact 模拟自主代理（开放规划与工具调用）。

2. **不适用场景**：
   - **单轮查询场景**：若应用场景中查询无歧义且无需交互，传统基准（如 BIRD）更为高效且成本更低。
   - **非 PostgreSQL 环境**：当前评估环境限定在 PostgreSQL 14 Docker 实例，未验证在 MySQL、BigQuery 等其他数据库引擎上的泛化能力。
   - **多语言场景**：所有任务均为英文，未覆盖多语言或本地化交互场景。
   - **高并发/事务性场景**：任务设计未涉及嵌套事务、并发修改等复杂事务逻辑。

### 局限与开放问题

**方法局限**：

- **用户模拟器的骨干依赖**：两阶段函数驱动模拟器虽通过 AMB()/LOC()/UNA() 动作分类和 AST 检索大幅降低了信息泄露（UNA 失败率从基线最高 67.4% 降至 2.7%，见 Figure 6），但其响应质量仍受骨干 LLM 能力约束，可能存在细微偏差或对特定系统模型表现出无意的偏向性。

- **预算参数的经验性设定**：c-Interact 的澄清轮次预算 $\tau_{\mathrm{clar}} = m_{\mathrm{amb}} + \lambda_{\mathrm{pat}}$ 和 a-Interact 的总预算 $B = B_{\mathrm{base}} + 2 m_{\mathrm{amb}} + 2 \lambda_{\mathrm{pat}}$ 中，用户耐心参数 $\lambda_{\mathrm{pat}}$ 默认设为 3，基础预算 $B_{\mathrm{base}}=6$，这些设定依赖人工经验，可能未完全对齐真实用户的交互习惯。

- **领域覆盖的有限性**：尽管任务涵盖 BI 与 DM 两大类，但领域分布与真实企业应用的多样性相比仍有局限，特别是缺少对特定垂直领域（如医疗、金融合规）的深度覆盖。

**开放问题**：

1. **工具利用激励**：在 a-Interact 模式下，成功模型的行动序列遵循“先探索环境，再提交”的模式（提交动作比例与优先问题成功率呈正相关 $r \approx 0.41$，执行动作比例呈负相关 $r \approx -0.52$，见 Figure 11-12），但多数模型仍过早依赖高成本的 `submit` 或 `ask` 动作。如何激励模型更充分地利用 `get_schema`、`get_knowledge_definition` 等低成本探索工具，是提升代理模式效率的关键。

2. **模式偏好与架构偏置**：GPT-5 在 c-Interact 中表现最差（优先问题成功率仅 14.50%），却在 a-Interact 中表现最佳（29.17%），而 Gemini-2.5-Pro 在 c-Interact 中领先（优先问题 27.67%）。这种模式间的性能反转是否源于模型训练数据分布与架构归纳偏置，以及如何针对性地进行预训练或微调以提升特定模式下的能力，尚待研究。

3. **高阶歧义的规划鸿沟**：Claude-3.7-Sonnet 在 ITS 实验中展现出随交互机会增加而单调提升的缩放行为（Figure 4），验证了更多交互可转化为信息增益，但多数模型在消除线性歧义与高阶歧义之间仍存在显著性能鸿沟。能否设计更高效的规划策略或内部信念状态来弥合这一差距，是一个开放挑战。

4. **用户模拟器的公平性评估**：如何评估和确保用户模拟器在更多样化的对话风格（如简洁、冗长、非母语表达）下的公平性与一致性，以及如何量化模拟器对特定系统模型的潜在偏向，仍需系统性研究。

5. **任务复杂度的进一步扩展**：引入更复杂的事务性逻辑（如嵌套事务、并发修改、权限约束）是否能更全面地暴露系统能力边界，并推动更鲁棒的交互策略设计，是一个值得探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/BIRD_INTERACT_Re_imagining_Text_to_SQL_Evaluation_via_Lens_of_Dynamic_Interactions.pdf]]
