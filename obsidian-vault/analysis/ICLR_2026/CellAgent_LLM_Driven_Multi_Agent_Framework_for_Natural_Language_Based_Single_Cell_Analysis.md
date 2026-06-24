---
title: "CellAgent: LLM-Driven Multi-Agent Framework for Natural Language-Based Single-Cell Analysis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CellAgent_LLM_Driven_Multi_Agent_Framework_for_Natural_Language_Based_Single_Cell_Analysis.pdf
openreview_forum_id: BsA2GNkJhz
aliases:
- CellAgent
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "采用Planner-Executor-Evaluator三层多智能体架构，结合自动评估与自反思优化机制，将分析流程的分解、执行和质量控制完全自动化，并通过匿名候选选择避免评估偏见。"
primary_logic: "通过将自动化的结果质量评估（Evaluator）与迭代优化机制内嵌于分析流程中，LLM驱动的智能体能够模拟人类专家决策，自主选择最优算法和超参数，在无需人工干预的情况下生成高质量、可复现的分析结果，实现了从自然语言到成品工作流的端到端自动化。"
claims:
- "CellAgent在超过60个数据集上实现平均96%以上的任务执行成功率，远超GPT-4的24%"
- "细胞类型注释任务中CellAgent的平均一致性得分达到0.85，优于所有基线方法（最高基线scGPT为0.77）"
- "批次校正任务中CellAgent取得最高的总得分0.67，超过次优方法scVI的0.66"
- "空间转录组学插补任务中CellAgent的Accuracy Score达到0.88，领先次优方法Tangram 17%"
---

# CellAgent: LLM-Driven Multi-Agent Framework for Natural Language-Based Single-Cell Analysis

> [!tip] 核心洞察
> 通过将自动化的结果质量评估（Evaluator）与迭代优化机制内嵌于分析流程中，LLM驱动的智能体能够模拟人类专家决策，自主选择最优算法和超参数，在无需人工干预的情况下生成高质量、可复现的分析结果，实现了从自然语言到成品工作流的端到端自动化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | CellAgent：基于LLM的多智能体框架用于自然语言驱动的单细胞分析 |
| 英文题名 | CellAgent: LLM-Driven Multi-Agent Framework for Natural Language-Based Single-Cell Analysis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=BsA2GNkJhz) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | CellAgent |
| Dataset | 细胞类型注释 (6个数据集), 批次校正 (5个数据集), 轨迹推断 (8个数据集), 空间域识别 (12个DLPFC切片) |

> [!tip] 效果简介
> - 细胞类型注释 (6个数据集) 上，平均一致性得分 (Average_score) 为 0.85，对比 0.77 (scGPT)，变化 +0.08。
> - 批次校正 (5个数据集) 上，总得分 (Overall_score) 为 0.67，对比 0.66 (scVI)，变化 +0.01。
> - 轨迹推断 (8个数据集) 上，总得分 (Overall_score) 为 0.50，对比 0.47 (Slingshot)，变化 +0.03。

## 概述

单细胞RNA测序（scRNA-seq）与空间转录组学数据分析长期面临一个核心瓶颈：它要求研究者同时具备深厚的计算技能和生物学专业知识，而现有工具生态高度碎片化，需要大量手动编程和多工具集成。这一高技术与时间门槛严重阻碍了生物学发现的效率。CellAgent 针对此问题，提出了一种基于LLM的多智能体分层决策框架，将分析流程的分解、执行和质量控制完全自动化。其核心洞察在于：通过将自动化的结果质量评估（Evaluator）与迭代优化机制内嵌于分析流程中，LLM驱动的智能体能够模拟人类专家决策，自主选择最优算法和超参数，在无需人工干预的情况下生成高质量、可复现的分析结果，实现了从自然语言到成品工作流的端到端自动化。

### 方法定位

CellAgent 采用 Planner-Executor-Evaluator 三层多智能体架构，并辅以全局与局部记忆控制模块。与依赖人工编写脚本的传统单细胞分析范式相比，CellAgent 在四个关键维度上实现了范式转换：

- **交互方式**：从手动编写代码和脚本转变为自然语言对话驱动的自动化分析。
- **工具选择与超参数调优**：由 Executor 中的 Tool Selector 从 sc-Omni 工具包自动选择最优工具并生成代码，替代人工选择与调参。
- **结果质量评估**：Evaluator 智能体对匿名化的候选执行结果进行自动化评估，并驱动自反思优化迭代，替代人工主观检查。
- **上下文记忆**：全局记忆存储各子步骤的最终代码，局部记忆保存执行跟踪信息以支持错误自修正，替代无系统性记忆的临时操作。

### 核心结论

在覆盖 60 余个数据集的五大下游任务上，CellAgent 展现出显著的性能优势：

- **任务执行成功率**：CellAgent 平均成功率超过 96%，远超 GPT-4 直接驱动的 24%（提高 72 个百分点）。
- **细胞类型注释**：平均一致性得分达 0.85，优于所有基线方法（次优方法 scGPT 为 0.77）。
- **批次校正**：总得分 0.67，略优于 scVI 的 0.66。
- **空间转录组学插补**：准确率得分 0.88，领先次优方法 Tangram 17%。
- **轨迹推断与空间域识别**：分别取得 0.50 和 0.47 的总得分，均小幅领先对应基线方法。

在与人类专家的对比中，CellAgent 将分析任务完成时间从 13 分钟缩短至 8 分钟，且质量评分高出 0.25。消融实验进一步表明，记忆优化机制对任务成功率的提升具有跨模型鲁棒性，而自反思优化机制能有效筛选最优候选算法，例如在轨迹推断任务中自动选择 Slingshot 并获得最高评分。

## 背景与动机

### 单细胞数据分析的自动化困境

单细胞RNA测序（scRNA-seq）和空间转录组学技术为解析细胞异质性、发育轨迹和组织微环境提供了前所未有的分辨率。然而，将这些原始数据转化为生物学发现的过程，构成了一个持久而深刻的瓶颈：**分析流程要求同时具备深厚的计算编程能力和生物学领域知识**。研究人员不仅需要理解数据的内在结构，还必须手动编写代码、选择工具、调优超参数，并在多个异构工具之间进行繁琐的集成。这种高技术与高时间门槛的双重约束，使得大量生物学研究者被排斥在高效的数据探索之外，严重阻碍了发现的迭代速度。

现有的单细胞分析工具生态虽然丰富，但其使用模式仍停留在“手动编程-单工具调用”的范式。无论是经典的批次校正方法如 **Harmony** (Korsunsky et al., 2019) 和 **scVI** (Lopez et al., 2018)，还是细胞类型注释工具 **Celltypist**，亦或是空间转录组学插补方法 **Tangram**，它们本质上都是离散的工具孤岛。将这些工具串联成一个完整、可复现的分析管线，完全依赖研究者的个人经验与手动操作。这种模式下，**工具选择与超参数调优**、**结果质量评估**、以及**跨步骤的上下文记忆**均缺乏系统性的自动化支持，导致分析结果高度可变、复现困难，且极易引入主观偏差。

### 大语言模型带来的新可能与现有局限

大语言模型（LLM）的兴起为自动化科学发现开辟了新路径。理论上，LLM具备理解自然语言指令、生成代码和进行推理的能力，有望成为连接生物学问题与计算工具的桥梁。然而，直接将通用LLM（如GPT-4）应用于单细胞数据分析面临根本性挑战：**任务执行成功率极低**。实验证据表明，GPT-4在超过60个数据集上的平均任务执行成功率仅为24%（Figure 5c），远不足以支撑可靠的科学分析。其失败根源在于：通用LLM缺乏对单细胞分析工作流的领域知识、无法进行精细的多步骤任务分解、不具备自动化的结果质量评估与纠错机制，且在复杂工具选择与超参数调优上表现脆弱。

### CellAgent的核心动机

针对上述双重困境——**手动分析的效率瓶颈**与**通用LLM的可靠性鸿沟**——本文提出CellAgent。其核心动机并非简单地将LLM作为代码生成器，而是构建一个**模拟人类专家“深度思考”工作流的多智能体层次化框架**。该框架通过三个关键机制回应核心挑战：

1. **自动化任务分解与执行**：将高层次的自然语言分析请求自动分解为有序的子任务序列，并自主选择最优工具生成可执行代码，消除手动编程与工具集成负担。
2. **内嵌的自反思优化闭环**：引入一个独立的评估智能体（Evaluator），对多个候选代码的执行结果进行自动化、匿名化的质量评估，并驱动迭代优化，从而模拟人类专家“试错-择优”的决策过程。
3. **结构化记忆与安全执行**：通过全局-局部双层记忆机制保留分析上下文与调试信息，并在隔离的代码沙箱中执行，确保可复现性与安全性。

简言之，CellAgent旨在实现从**自然语言指令到高质量、可复现分析工作流的端到端自动化**，使单细胞数据分析从“手动编程密集型”转变为“自然语言驱动型”，从而将研究者从繁琐的技术细节中解放出来，聚焦于生物学假设的生成与验证。

## 核心创新

CellAgent 的核心创新在于将 LLM 驱动的多智能体协作架构与自动化的自反思优化机制深度耦合，从而将单细胞数据分析从“手动编程+人工评估”的范式彻底转变为“自然语言驱动+自动化闭环优化”的范式。这一转变通过四个关键维度的创新实现。

### 1. 交互范式的根本性变革：从手动编程到自然语言对话

传统单细胞分析流程要求研究人员手动编写代码、选择工具并调参，这不仅耗时且要求深厚的计算与生物学双重专业知识。CellAgent 将交互方式从**手动编写代码和脚本**转变为**通过自然语言对话自动化分析**（Section 1）。用户只需提供数据集和自然语言描述的分析需求，框架即可自动完成从任务规划到结果输出的全流程。这一改变消除了编程门槛，使生物学家能够直接以领域语言驱动分析，显著降低了技术壁垒。

### 2. 工具选择与超参数调优的自动化：从人工决策到智能体自主推理

在传统流程中，研究人员需要手动从众多可用工具中选择合适的方法并调整超参数。CellAgent 通过 Executor 中的 **Tool Selector** 模块实现了这一过程的自动化：Tool Selector 根据当前子任务需求，从集成了专家知识的 **sc-Omni 工具包**中自动识别最合适的工具（Section 3.2），并由 **Code Programmer** 生成可执行的 Python 代码。这一机制将工具选择的决策权从人类专家转移至 LLM 智能体，实现了分析流程中关键决策点的自动化。

### 3. 结果质量评估的闭环化：从人工主观评估到自动化自反思优化

这是 CellAgent 最核心的架构创新。传统分析中，结果质量的评估依赖人工检查和主观判断，缺乏系统性的反馈机制。CellAgent 引入了 **Evaluator 智能体**，该智能体接收匿名化的候选代码输出、任务特定指标和诊断图，自动评估结果质量并驱动**自反思优化机制**（Section 1）。具体而言，Executor 为每个子任务生成多个候选代码，Evaluator 匿名评估后选择最优解，若结果不理想则提供反馈触发 Executor 重新生成代码，形成“生成-评估-优化”的闭环迭代。这一设计将质量控制的决策权内嵌于框架之中，使系统能够模拟人类专家的迭代优化行为。

### 4. 上下文记忆的系统化设计：从无记忆到双层记忆架构

传统单次分析缺乏系统性的记忆机制。CellAgent 设计了**全局记忆**与**局部记忆**的双层架构（Section 3.3）：全局记忆仅存储每个子步骤的最终代码，为后续子任务提供上下文连续性；局部记忆作为短期工作区，捕获当前子步骤的完整执行跟踪（包括错误代码和错误信息），支撑 Executor 的**错误自修正**能力。这种记忆隔离设计既保证了跨子任务的信息传递，又避免了冗余或错误信息对后续决策的干扰，是框架高执行成功率的关键支撑。

## 整体框架

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/001_Figure_1.jpg]]
*Figure 1: Schematic of the CellAgent Framework. Users interact with CellAgent via natural language to obtain high-quality, automated analysis results tailored to their specific needs. Then the framework operates hierarchically, with a high-level Planner that performs fine-grained task decomposition based on input data characteristics and user queries. In the lower-level execution phase, subtasks are completed sequentially. An Executor selects optimal tools from the sc-Omni toolkit to generate and execute code. An Evaluator then rigorously assesses the outcomes, proposing refinements if needed. This self-reflective optimization loop iterates to enhance precision, and the final results from all subtask...*

CellAgent 是一个基于 LLM 的分层多智能体框架，其核心设计目标是将单细胞 RNA 测序与空间转录组学数据分析从手动编码彻底转变为自然语言驱动的自动化流程。框架的整体架构遵循 **Planner → Executor → Evaluator** 三层决策范式，并通过全局与局部记忆机制形成闭环优化。

### 输入输出流

用户通过自然语言交互提交分析请求，包括任务描述、具体需求和数据集。CellAgent 接收这些输入后，自动完成从任务分解到最终分析报告生成的全流程，输出高质量、可复现的分析结果。整个过程无需人工编写代码或手动选择工具。

### 核心模块与协作关系

**Planner（规划器）** 作为高层调度者，首先检查数据集的摘要信息 $\psi(D)$，以将策略锚定在数据的具体特征上。随后，它将用户的高层次目标分解为有序的子任务序列 $t_1, t_2, ..., t_n$。Planner 的系统提示 $p_{sys}^p$ 注入了单细胞与空间转录组学工作流的专家知识，确保分解结果符合领域最佳实践。

**Executor（执行器）** 负责逐步完成 Planner 分解出的每个子任务。它包含两个子组件：**Tool Selector** 从集成的 sc-Omni 工具包中为当前子任务选择最优工具集 $\mathcal{T}_{t_i}$；**Code Programmer** 则根据任务上下文、工具文档和记忆模块 $\mathcal{M}$ 生成可执行的 Python 代码 $c_i$ 及分析文本 $w_i$。Executor 具备错误自修正能力——当代码执行失败时，它会利用局部记忆中捕获的执行跟踪信息进行调试和重试。

**Evaluator（评估器）** 是框架实现质量闭环的关键。它接收多个匿名化候选代码的执行结果、任务特定指标和诊断图，从中选择最优解 $\bar{c_i}$。评估器不接触算法名称或 Executor 的提示词，仅基于客观输出进行判断，从而避免自我偏好偏差。若结果未达预期，评估器会提供反馈，驱动 Executor 进行自反思优化迭代。

**Memory Control（记忆控制）** 采用双层记忆架构：**全局记忆**保存每个已完成子步骤的最终代码 $\mathcal{M} \{\bar{c_1}, \bar{c_2}, \dots\}$，为后续步骤提供上下文连续性；**局部记忆**作为 Executor 在当前子任务内的短期工作区，捕获完整的执行跟踪信息（包括错误代码和错误消息），支撑代码自修正。

**Code Sandbox（代码沙箱）** 通过 Jupyter Notebook 转换机制隔离生成的代码执行环境，增强安全性和可重现性。

### 架构示意

框架整体架构如 **Figure 1** 所示，展示了从用户自然语言交互、Planner 任务分解、Executor 工具选择与代码生成、Evaluator 质量评估到最终结果合成的完整层次化工作流。sc-Omni 工具包（**Table 2**）集成了覆盖预处理、基础分析和高级分析三个层次的 18 项分析任务，为 Executor 提供了丰富的工具选择空间。框架支持的八大核心分析任务详见 **Table 3**，涵盖批次校正、细胞类型注释、轨迹推断、空间域识别、空间插补等单细胞与空间转录组学分析的关键需求。

## 核心模块与公式推导

### 架构总览

CellAgent 采用 Planner–Executor–Evaluator 三层多智能体层次化架构，辅以双通道记忆控制和隔离式代码沙箱，形成“规划—执行—评估—优化”的闭环自动化流程（Figure 1）。各模块的职责与协作关系通过以下公式化定义加以精确刻画。

### 任务规划（Planner）

Planner 作为高层调度者，接收用户请求、数据集摘要和领域知识，将复杂分析目标分解为有序的子任务序列。其系统提示 $p_{\mathrm{sys}}^p$ 注入了单细胞 RNA 测序与空间转录组学工作流的专家知识，包括标准操作顺序和任务特有约束，以抑制幻觉并确保分解的合理性。

Planner 的分解过程形式化为：

$$t_1, t_2, \dots, t_n \gets \mathcal{A}_p^{\mathrm{LLM}}(p_{\mathrm{sys}}^p, u_{\mathrm{task}}, u_{\mathrm{req}}, u_D, \psi(D))$$

其中 $\mathcal{A}_p^{\mathrm{LLM}}$ 表示 Planner 智能体所调用的大语言模型，$u_{\mathrm{task}}$ 为用户任务描述，$u_{\mathrm{req}}$ 为用户需求约束，$u_D$ 为数据集元信息，$\psi(D)$ 为数据集统计摘要（如基因数、细胞数、批次标签等），输出为 $n$ 个有序子任务 $\{t_1, t_2, \dots, t_n\}$。

### 执行器（Executor）

Executor 由工具选择器（Tool Selector）和代码程序员（Code Programmer）两个子模块组成，负责将每个子任务转化为可执行的分析代码。

**工具选择**：Tool Selector 从 sc-Omni 工具包 $\mathcal{T}$ 中为当前子任务 $t_i$ 筛选最优工具集：

$$\mathcal{T}_{t_i} \gets \mathcal{A}_t^{\mathrm{LLM}}(p_{\mathrm{sys}}^t, u_{\mathrm{req}}, \mathcal{T}, t_i)$$

其中 $p_{\mathrm{sys}}^t$ 为工具选择的系统提示，输出 $\mathcal{T}_{t_i}$ 为 $t_i$ 对应的候选工具子集。

**代码生成**：Code Programmer 基于任务上下文、工具文档 $\mathrm{Doc}(\mathcal{T}_{t_i})$ 和记忆模块 $\mathcal{M}$，生成可执行 Python 代码 $c_i$ 及配套分析文本 $w_i$：

$$(c_i, w_i) \gets A_c^{\mathrm{LLM}}(p_{\mathrm{sys}}^c, u_{\mathrm{task}}, u_{\mathrm{req}}, u_D, \psi(D), \mathcal{M}, t_i, \mathrm{Doc}(\mathcal{T}_{t_i}))$$

Code Programmer 具备错误自修正能力：当代码执行失败时，局部记忆中的执行跟踪信息（错误日志、中间输出）被反馈至模型，驱动代码修正重试。

### 评估器与自反思优化（Evaluator）

Evaluator 对 Executor 生成的多组候选代码进行匿名化评估，选择最优解并驱动自反思优化迭代。评估过程严格隔离信息：Evaluator 仅接收匿名化输出、任务指标和诊断图，不接触算法名称或 Executor 提示词，以避免自我偏好偏差。

最优候选选择的形式化定义为：

$$\bar{c_i} = \mathcal{A}_e^{\mathrm{LLM}}(p_{\mathrm{sys}}^e, u_{\mathrm{req}}, u_D, t_i, \{c_i^j\})$$

其中 $\{c_i^j\}$ 为 Executor 在第 $j$ 轮生成的候选代码集合，$\bar{c_i}$ 为 Evaluator 选出的当前子任务最优代码。若评估结果未达阈值，Evaluator 生成反馈建议，触发 Executor 重新生成代码，形成自反思优化循环（默认最多 3 轮迭代）。

### 记忆控制（Memory Control）

CellAgent 采用双通道记忆机制以协调上下文管理与执行隔离：

- **全局记忆** $\mathcal{M}$：仅存储各已完成子步骤的最终代码，形成 $\mathcal{M} = \{\bar{c_1}, \bar{c_2}, \dots\}$，为后续子任务提供可复用的代码上下文，同时避免错误代码的累积污染。
- **局部记忆**：作为 Executor 在单个子任务内的短期工作区，捕获完整的实时执行跟踪，包括所有生成代码（正确与错误版本）、错误消息和中间输出，支撑代码自修正。

### 代码沙箱（Code Sandbox）

所有生成代码在隔离的 Jupyter Notebook 环境中通过 nbconvert 执行，确保执行安全性和结果可重现性，防止恶意或错误代码影响宿主系统。

### 关键评估指标公式

以下公式用于下游任务的定量评估，均在附录 D 中有详细定义：

**批次校正总得分**：以 4:6 权重组合批次效应移除指标与生物信号保留指标：

$$\mathrm{Overall} = \mathrm{AvgBatch} \times 0.4 + \mathrm{AvgBio} \times 0.6$$

**细胞类型注释平均一致性得分**：基于完全匹配、部分匹配和错配的加权量化：

$$\mathrm{Average_{score}} = 1 \times \text{fully match} + 0.5 \times \text{partially match} + 0 \times \text{mismatch}$$

**轨迹推断总得分**：四项轨迹质量指标的几何平均：

$$\mathrm{Overall} = \sqrt[4]{\mathrm{cor_{dist}} \times \mathrm{edgeflip} \times \mathrm{F1_{branches}} \times \mathrm{wcor_{features}}}$$

**空间插补准确率得分**：PCC、SSIM、RMSE、JS 四项指标排名的算术平均：

$$\mathrm{AS} = \frac{1}{4} (\mathrm{RANK_{PCC}} + \mathrm{RANK_{SSIM}} + \mathrm{RANK_{RMSE}} + \mathrm{RANK_{JS}})$$

## 实验与分析

### 主要结果

CellAgent 在覆盖单细胞 RNA 测序（scRNA-seq）与空间转录组学（ST）的五大类下游任务上进行了系统评估，所有定量结果汇总于 **Table 1**。框架的核心优势体现在三个层面：任务执行成功率、下游任务指标表现，以及与人类专家的效率-质量权衡。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/003_Table_1.jpg]]
*Table 1: Comparison of multiple tasks. cell type annotation, batch correction, trajectory inference, spatial domain identification, and spatial imputation*

**任务执行成功率。** 在跨越 60 余个数据集的八项分析任务中，CellAgent 经过至多三次自反思优化迭代后（CellAgent@3），平均执行成功率达到 **96% 以上**，而直接使用 GPT-4 的成功率仅为 24%（**Figure 5c**）。这一 72 个百分点的差距直接验证了多智能体分层架构与自反思优化机制在自动化复杂分析流程中的决定性作用——单纯依赖强大基座模型远不足以应对工具选择、代码生成与错误修正的级联挑战。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/012_Figure_5.jpg]]
*Figure 5: Performance comparison. a, Comparison of the efficiency of CellAgent and Human Expert on eight tasks involving scRNA-seq and spatial transcriptomics data analysis. Efficiency was assessed in minutes (Table 3 in Appendix). b, Comparison of the quality of CellAgent and Human Expert on eight tasks involving scRNA-seq and spatial transcriptomics data analysis. Quality was rated on a scale from 0 to 10, with evaluations conducted by evaluators (n=5). c, Comparison of the success rates of GPT-4, CellAgent, and CellAgent@3 (representing the best outcome after up to three attempts) across the 8 tasks. d, Assessment of the facilitation of CellAgent, GPT-4, and Online Webserver on scRNA-seq and data...*

**下游任务定量表现。** 在五类核心任务上，CellAgent 均达到或超越现有最佳专用方法的水平：

- **细胞类型注释**（6 个数据集）：CellAgent 的平均一致性得分（Average_score）为 **0.85**，显著优于次优基线 scGPT 的 0.77（+0.08）。该指标基于完全匹配（1 分）、部分匹配（0.5 分）和错配（0 分）的加权计算，反映了注释结果与金标准在细胞类型层级上的精细对齐程度。
- **批次校正**（5 个数据集）：CellAgent 以 **0.67** 的总得分（Overall_score）略优于 scVI 的 0.66。该总得分以 0.4 权重组合批次效应移除指标（AvgBatch）和 0.6 权重组合生物信号保留指标（AvgBio），体现了在消除技术噪声与保留生物学变异之间的平衡。
- **轨迹推断**（8 个数据集）：CellAgent 的总得分达到 **0.50**，超过 Slingshot 的 0.47（+0.03）。该得分是四项轨迹质量指标（拓扑距离相关性、边翻转率、分支 F1、特征加权相关性）的几何平均，对拓扑保真度和伪时间精度进行综合量化。
- **空间域识别**（12 个 DLPFC 切片）：CellAgent 的平均调整兰德指数（ARI）为 **0.47**，以微弱优势领先 BayesSpace 的 0.46。
- **空间转录组学插补**（7 个数据集）：CellAgent 的准确率得分（AS）达到 **0.88**，大幅领先次优方法 Tangram 的 0.75（**+17%**）。AS 是 PCC、SSIM、RMSE 和 JS 散度四项指标排名的算术平均，综合衡量插补结果与真实表达谱在相关性和分布层面的保真度。

值得注意的是，在插补任务上的显著领先（+17%）与批次校正任务上的微弱优势（+0.01）形成对比，暗示 CellAgent 的优势在不同任务类型上存在结构性差异：插补任务受益于工具选择与超参数优化的自动化空间更大，而批次校正领域的方法已高度成熟，自动化提升的边际收益有限。

**与人类专家的对比。** **Figure 5a-b** 展示了 CellAgent 与人类专家在八项任务上的效率和质量的直接对比：CellAgent 平均完成任务耗时 **8 分钟**，而人类专家需要 13 分钟（缩短 38%）；同时，由五位评估者给出的质量评分显示 CellAgent 高出 **0.25 分**（10 分制）。这一结果表明，LLM 驱动的自动化框架不仅在速度上具有优势，更能在结果质量上超越人工操作——这背后的因果机制在于 Evaluator 驱动的自反思优化能够系统性地探索工具-超参数组合空间，避免了人类专家可能存在的路径依赖和次优选择。

### 消融实验

**记忆机制的有效性。** **Figure 8** 展示了全局记忆与局部记忆模块对任务执行成功率的贡献。在 GPT-4o、Qwen3 等三种不同基座模型上，启用记忆优化机制后任务执行成功率均显著提升。这一结果验证了记忆模块的两个关键功能：全局记忆通过保存各子步骤的最终代码避免了跨子任务的重复试错，局部记忆通过捕获当前子步骤的完整执行跟踪（包括错误代码和报错信息）使 Executor 具备有效的错误自修正能力。记忆机制的跨模型有效性进一步表明，该设计是对 LLM 固有局限（如上下文遗忘、错误传播）的通用性补偿，而非对特定模型的过拟合。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/015_Figure_8.jpg]]
*Figure 8: Memory Mechanism Optimization across Different Base Models in CellAgent. We evaluate the performance gain in task execution success rate provided by the memory optimization mechanism across eight analysis tasks (detailed in Table 3) and three distinct base models. The gray dots represent the baseline success rate of the model without memory optimization, while the colored markers and annotated numerical values display the performance gain contributed by enabling the memory optimization mechanism*

**基座模型的鲁棒性。** **Figure 7** 表明，当将基座模型替换为不同 LLM 时，CellAgent 在下游任务上的性能持续优于基线方法。这意味着框架的分层决策架构和自反思优化机制对基座模型的选择具有鲁棒性——框架的设计优势不依赖于某一种特定 LLM 的能力边界。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/014_Figure_7.jpg]]
*Figure 7: Performance comparison of CellAgent with other single-cell analysis agents. We evaluated the performance across five downstream tasks: Spatial Imputation, Domain Identification, Trajectory Inference, Cell Type Annotation, and Batch Correction. The x-axis represents the performance metric score (see Appendix D.1). CellAgent, particularly the version powered by GPT-4o (indicated by red diamonds), consistently outperforms baseline methods*

**自反思优化的候选筛选能力。** 在轨迹推断任务的案例分析中（**Figure 14**），自反思优化机制成功从多个候选算法中自动选择了 Slingshot 并获得最高评分。这一过程的关键设计在于 Evaluator 仅接收匿名化的候选输出和任务指标，不接触算法名称或 Executor 的提示词（详见 Appendix C.6），从而避免了自我偏好偏差——即 LLM 倾向于选择自己生成或“熟悉”的方法，而非客观上最优的方法。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/031_Figure_14.jpg]]
*Figure 14: Results on trajectory inference through dialogue. In response to user dissatisfaction with the initial trajectory differential expression results, CellAgent automatically evaluated three distinct trajectory inference methods and selected the highest-scoring one (Slingshot). It then visualized the top 20 differentially expressed genes along the refined trajectory*

### 关键图表分析

**Figure 3** 和 **Figure 4** 从可视化层面佐证了定量结果。在人类 PBMC 数据集的细胞类型注释中（**Figure 3a**），CellAgent 预测的细胞类型在 UMAP 嵌入上与原始研究的注释高度一致，表明自动化流程能够准确复现专家级别的注释模式。在 Aging HSC 数据集的轨迹推断中（**Figure 3b**），CellAgent 重建的细胞分组和伪时间轨迹成功捕获了从 LT-HSC 经 ST-HSC 到 MPP 的造血分化连续谱。在空间转录组学方面，**Figure 4a** 显示 CellAgent 在 DLPFC 切片 151673 上识别的空间域与金标准的层状结构高度吻合；**Figure 4c** 中，插补后识别的前十个空间可变基因按 Moran's I 空间自相关分数排序，表明插补结果有效恢复了基因表达的空间结构信息。

**Figure 5d** 的用户评估进一步表明，在 20 名参与者对 CellAgent、GPT-4 和在线网络服务器的辅助效果评价中，CellAgent 获得了最高的可用性评分，验证了自然语言交互界面在降低单细胞分析技术门槛方面的实际效用。

### 补充图表

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/013_Table_2.jpg]]

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/046_Table_2.jpg]]
*Table 2: The overview of the sc-Omni toolkit. Each task is categorized into preliminary, essential, or advanced analysis, with representative tools or algorithms*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/047_Table_3.jpg]]
*Table 3: Overview of the eight major tasks in scRNA-seq and spatial transcriptomics analyses. These tasks include batch correction, preprocessing and clustering, cell type annotation, trajectory inference, spatial neighborhood analysis, spatially variable gene identification, spatial transcriptomics imputation, and spatial domain identification. The table also outlines the primary objectives of each task*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/048_Table_4.jpg]]
*Table 4: Overview of batch correction datasets. The table summarizes the key characteristics of the five datasets used for batch correction evaluation, including the number of cells and batches, as well as the tested features such as tissue types, experimental protocols, and laboratory sources*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/049_Table_5.jpg]]
*Table 5: Overview of cell type annotation datasets. The table summarizes the key characteristics of the datasets used for cell type annotation evaluation, including the number of cells, the number of genes, and the number of cell types in each dataset*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_BsA2GNkJhz/figures/050_Table_6.jpg]]
*Table 6: Overview of trajectory inference datasets. The table summarizes the key characteristics of the datasets used for trajectory inference evaluation, including the number of cells, gene count, and the trajectory type (e.g., linear, bifurcation, cycle, or multifurcation) for each dataset*

## 方法谱系与知识库定位

### 1. 核心设计思路与定位

CellAgent 的核心设计思路是将单细胞数据分析流程完全委托给 LLM 驱动的多智能体系统，通过 **Planner-Executor-Evaluator** 三层架构实现从自然语言请求到最终分析结果的端到端自动化。其定位并非提出新的单细胞分析算法，而是构建一个**元框架**，将现有的分析工具和领域知识整合进智能体的决策循环中。

该框架的关键机制是**自反思优化**（self-reflective optimization）：Evaluator 智能体对 Executor 生成的多个候选代码的运行结果进行自动化评估，选择最优解，并在结果不满足要求时驱动 Executor 进行迭代修正。这一闭环使得系统能够模拟人类专家的试错与优化过程，自主完成工具选择、超参数调优和结果质量控制。

### 2. 与基线方法的对比分析

CellAgent 在五项下游任务上与多个专用方法进行了定量对比。需要注意的是，这些基线方法本身是 CellAgent 在执行过程中可能调用的工具，而非直接的框架级竞争对手。

#### 2.1 细胞类型注释

在 6 个数据集上，CellAgent 的平均一致性得分（Average Score）达到 **0.85**，优于所有专用基线方法。次优方法为单细胞基础模型 **scGPT**（Cui et al., 2024），得分为 0.77，CellAgent 领先 **+0.08**。其他对比方法包括 **Celltypist** 等专用注释工具。CellAgent 的优势在于其 Tool Selector 能够根据数据集特征自动选择最合适的注释方法，并通过自反思机制优化注释结果。

#### 2.2 批次校正

在 5 个数据集上，CellAgent 的总得分（Overall Score）为 **0.67**，略高于次优方法 **scVI**（Lopez et al., 2018）的 0.66，以及 **Harmony**（Korsunsky et al., 2019）等经典方法。该总得分由批次效应移除和生物信号保留两类指标加权合成（公式为 $\text{Overall} = \text{AvgBatch} \times 0.4 + \text{AvgBio} \times 0.6$）。虽然优势幅度较小（+0.01），但 CellAgent 无需人工选择校正方法即可达到与最优专用工具相当的性能。

#### 2.3 轨迹推断

在 8 个数据集上，CellAgent 的总得分（Overall Score）为 **0.50**，略高于 **Slingshot** 的 0.47（+0.03）。轨迹推断的总得分是四项指标（拓扑距离相关性、边翻转比例、分支 F1 分数、特征加权相关性）的几何平均：$\text{Overall} = \sqrt[4]{cor_{dist} \times edgeflip \times F1_{branches} \times wcor_{features}}$。消融实验（Figure 14）表明，自反思优化机制能够有效筛选出最优候选算法，例如在特定数据集上自动选择 Slingshot 并获得最高评分。

#### 2.4 空间域识别

在 12 个 DLPFC 切片上，CellAgent 的调整兰德指数（ARI）为 **0.47**，与 **BayesSpace** 的 0.46 基本持平（+0.01）。该任务的性能提升有限，可能反映了空间域识别本身对算法选择的敏感度较低，或当前工具集在该任务上的性能天花板。

#### 2.5 空间转录组学插补

这是 CellAgent 优势最显著的任务：在 7 个数据集上，CellAgent 的准确率得分（Accuracy Score, AS）达到 **0.88**，领先次优方法 **Tangram** 的 0.75 达 **17%**。AS 是 PCC、SSIM、RMSE 和 JS 散度四项指标排序的平均值：$\text{AS} = \frac{1}{4} (\text{RANK}_{PCC} + \text{RANK}_{SSIM} + \text{RANK}_{RMSE} + \text{RANK}_{JS})$。这一结果表明 CellAgent 在需要多工具协同和参数调优的复杂任务上具有明显优势。

### 3. 与人类专家及通用 LLM 的对比

CellAgent 的设计目标之一是降低单细胞分析的技术门槛。与人类专家的对比实验（Figure 5）显示：
- **效率**：CellAgent 平均 8 分钟完成任务，人类专家平均需要 13 分钟（缩短约 38%）。
- **质量**：CellAgent 的质量评分（0-10 分制）比人类专家高出 0.25 分。
- **成功率**：CellAgent@3（最多三次迭代）在 8 项任务上的平均执行成功率达到 **96%**，远超 GPT-4 直接生成代码的 **24%**。这 72% 的差距直接归因于 CellAgent 的多智能体架构和自反思优化机制。

### 4. 架构鲁棒性与消融分析

消融实验揭示了两个关键设计要素的有效性：

- **记忆优化机制**（Figure 8）：在 GPT-4o、Qwen3 等三种不同 LLM 基础模型上，启用全局+局部记忆机制后，任务执行成功率均显著提升。全局记忆保存各子步骤的最终代码以避免重复计算，局部记忆存储当前子步骤的执行跟踪信息以支持错误自修正。
- **模型鲁棒性**（Figure 7）：当基础模型替换为不同 LLM 时，CellAgent 的性能持续优于基线方法，表明框架的有效性不完全依赖于特定 LLM 的能力。

### 5. 适用边界与局限性

基于现有证据，CellAgent 的适用边界可归纳如下：

- **任务范围**：当前框架覆盖 scRNA-seq 和空间转录组学的八项主要分析任务，包括批次校正、预处理与聚类、细胞类型注释、轨迹推断、空间邻域分析、空间可变基因识别、空间转录组学插补和空间域识别。对于超出 sc-Omni 工具集覆盖范围的新型分析需求，需要手动扩展工具集。
- **评估公平性保障**：Evaluator 仅接收匿名化的候选输出和任务指标，不接触算法名称或 Executor 的提示词（Appendix C.6），以避免自我偏好偏差。执行与评估的记忆严格隔离，防止信息泄露导致评估偏斜。
- **潜在局限**：在空间域识别等任务上，CellAgent 相比专用方法的提升有限（ARI 仅 +0.01），表明当工具集内各方法性能接近时，智能体选择的边际收益较小。此外，框架的性能仍受限于底层 LLM 的代码生成能力和 sc-Omni 工具集的质量。

### 6. 开放问题

论文未明确讨论以下开放问题，需要进一步研究或手动验证：

- **工具集的动态扩展机制**：当新算法发布时，如何以最小的人工干预将其纳入 sc-Omni 工具集并更新 Planner 的领域知识？
- **跨模态泛化能力**：当前框架专注于转录组学数据，其在蛋白质组学、表观基因组学等其他单细胞模态上的适用性尚待验证。
- **评估指标的完备性**：自反思优化依赖于 Evaluator 使用的自动化指标，这些指标是否在所有生物学场景下都能准确反映分析质量，仍需生物学家的经验性验证。
- **计算成本与可及性**：多次迭代的 LLM 调用和多候选代码执行带来的计算开销，是否会在大规模数据集上成为实际应用的瓶颈，论文未提供详细分析。

## 原文 PDF

![[paperPDFs/ICLR_2026/CellAgent_LLM_Driven_Multi_Agent_Framework_for_Natural_Language_Based_Single_Cell_Analysis.pdf]]
