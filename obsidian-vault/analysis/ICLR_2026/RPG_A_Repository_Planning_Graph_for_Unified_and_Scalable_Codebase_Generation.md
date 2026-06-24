---
title: "RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RPG_A_Repository_Planning_Graph_for_Unified_and_Scalable_Codebase_Generation.pdf
aliases:
- RPG
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "将自然语言规划替换为结构化、机器可解析的仓库规划图（RPG），并以此驱动整个代码生成流程。"
primary_logic: "通过统一“提案级规划”（功能分解）与“实现级规划”（文件结构/数据流/接口设计）的图表示，RPG 能够提供稳定的长期规划基础，实现覆盖率和代码体量的近线性扩展，并显著加速代理的定位与调试。"
claims:
- "ZeroRepo（o3-mini）在 RepoCraft 上实现 81.5% 的功能覆盖率，相较最强的基线 Claude Code（54.2%）提升 27.3 个百分点，并在代码体量上超越 3.9 倍。"
- "RPG 驱动的图引导定位相较于无图定位，将集成测试、增量开发和调试中的搜索步数降低 30-50%。"
- "ZeroRepo 在迭代过程中保持 LOC 近线性增长（~980 LOC/迭代，R²=0.97），而基于自然语言的基线在 3-4K LOC 停滞。"
- "即使在移除全局特征树知识库的情况下，RPG 结构仍支撑 87.2% 覆盖率和稳定的 LOC 增长，表明结构化图本身是扩展性的主要驱动力。"
---

# RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation

> [!tip] 核心洞察
> 通过统一“提案级规划”（功能分解）与“实现级规划”（文件结构/数据流/接口设计）的图表示，RPG 能够提供稳定的长期规划基础，实现覆盖率和代码体量的近线性扩展，并显著加速代理的定位与调试。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RPG：面向统一与可扩展代码库生成的仓库规划图 |
| 英文题名 | RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=VAQq3Y8tIF); [GitHub](https://github.com/microsoft/RPG-ZeroRepo) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | ZeroRepo |
| Dataset | RepoCraft |

> [!tip] 效果简介
> - RepoCraft 上，Coverage (%) 为 81.5 (o3-mini) / 75.1 (Qwen3-Coder)，对比 54.2 (Claude Code CLI, strongest baseline)，变化 +27.3 / +20.9。
> - RepoCraft 上，Pass Rate (%) 为 69.7 (o3-mini) / 57.3 (Qwen3-Coder)，对比 33.9 (Claude Code CLI)，变化 +35.8 / +23.4。
> - RepoCraft 上，LOC (generated) 为 36,941 (Qwen3-Coder) / 23,977 (o3-mini)，对比 10,586.7 (Claude Code CLI)，变化 ~3.9× / ~3.5×。

## 概述

仓库级代码生成面临的核心瓶颈在于：自然语言规划缺乏显式结构，难以准确追踪长期依赖关系，导致模块划分混乱、数据流断裂以及生成代码的可扩展性受限。为了解决这一问题，本文提出了一种统一的、机器可解析的**仓库规划图**（Repository Planning Graph, RPG），将功能分解与实现级设计编码为一张层次化、可追溯的图结构，并基于该图构建了零样本仓库生成框架 **ZeroRepo**。

ZeroRepo 通过三个阶段将自然语言意图转化为可执行仓库：1) **提案级构建**：利用大规模功能特征树和 explore–exploit 策略，从用户查询中生成功能目标图；2) **实现级构建**：在此基础上嵌入文件骨架、模块间数据流和函数/类接口，形成完整的 RPG；3) **图引导代码生成**：按拓扑顺序遍历 RPG，执行测试驱动开发、图引导定位和迭代修复，最终生成完整代码库。

实验在涵盖六个真实 Python 项目的 RepoCraft 基准上进行。结果表明，ZeroRepo 显著优于现有智能体框架和终端型编程方法：以 o3-mini 为后端时，功能覆盖率（Coverage）达到 81.5%，较最强基线 Claude Code 的 54.2% 提升 **27.3 个百分点**；通过率（Pass Rate）达到 69.7%，提升 **35.8 个百分点**；生成代码行数达 36,941（Qwen3-Coder），约为基线的 **3.9 倍**。更重要的是，RPG 带来的结构驱动力使生成过程实现了近线性的规模扩展——覆盖率和代码体量随迭代近乎线性增长（LOC 增长拟合斜率约 980 LOC/迭代，$R^2=0.97$），而基于自然语言规划的基线在 3–4K LOC 后即趋于停滞。消融实验进一步证实：即便移除全局特征树知识库，RPG 仍然支撑 87.2% 的覆盖率与稳定扩展，表明图结构本身是扩展性的主要驱动力。此外，图引导的故障定位将集成测试、增量开发与调试中的搜索步骤减少了 **30–50%**。

综上所述，ZeroRepo 通过将规划介质从自然语言转变为结构化 RPG，突破了仓库生成的任务复杂度与规模瓶颈，为统一、可扩展的代码库自动生成提供了新的范式。

## 背景与动机

### 仓库级代码生成的规划瓶颈
自动化代码生成正从单函数、单文件向完整仓库级系统演进。在仓库级生成中，系统不仅需要准确实现各模块功能，还必须维护跨文件、跨模块的依赖关系、数据流与接口契约。然而，当前主流的代码生成代理（如 MetaGPT、ChatDev、OpenHands、Claude Code CLI 等）几乎全部依赖**自然语言**进行规划——需求被表示为自由形式的 Markdown 或规格文档，并由代理在迭代中逐步扩展。这种基于自然语言的规划存在根本性缺陷：

1. **语义模糊与结构缺失**：自然语言难以精确、无歧义地描述模块边界、接口签名、数据流动方向和文件组织方式。代理在每次决策时都需要重新解释长篇自然语言文本，导致模块划分前后不一致、接口设计退化。
2. **长程依赖追踪困难**：仓库级系统通常包含数十个文件、数百个函数。自然语言规划无法提供显式的依赖图，代理在定位错误、增量开发或调试时，不得不通过反复搜索和试错来理解组件关系，搜索步数激增，效率低下。
3. **扩展性受限**：随着代码规模增大，自然语言描述的复杂度和歧义性呈非线性增长，导致生成过程陷入“规划衰退”：在达到一定体量（3–4 K LOC）后，功能覆盖率和有效代码量几乎不再增长，形成**可扩展性壁障**。

### 现有方法的缺口
在 RepoCraft 基准（涵盖六个真实 Python 开源仓库）上，基于自然语言规划的代理系统均表现出明显的覆盖率天花板。以当前最强的终端代理 Claude Code CLI 为例，即使经过 30 轮迭代，功能覆盖率仍仅有 54.2%，生成的有效代码量不足 10.6 K LOC。相比之下，基于结构化规划的 ZeroRepo 在同一条件下实现了 81.5%  的覆盖率，代码体量达到 ~24 K LOC，提升约 3.9 倍（Table 2）。这直接揭示出现有框架的规划机制是核心瓶颈，而非模型能力或工具集成不足。

更深层的问题在于，自然语言规划无法为代理提供**机器可解析的全局视图**。在集成测试、增量开发和调试等任务中，无图引导的定位过程需要大量搜索步骤；而一旦引入结构化图引导，搜索步数可降低 30–50%（Table 4）。这说明缺乏结构化的规划不仅制约最终产物的覆盖率，更拖累整个开发周期的效率。

### 本文动机：以结构化图取代自然语言规划
上述瓶颈的根源在于规划介质本身：自然语言是一种适合于人类交流的非形式化载体，但**不适合被机器精准解析与长期维护**。为此，本文提出将规划介质从自然语言**替换为一种结构化、机器可解析的仓库规划图（Repository Planning Graph，RPG）**，并以此驱动整个代码生成流程。

RPG 的核心洞见在于：将仓库的**提案级规划**（功能分解与模块化）与**实现级规划**（文件结构、数据流及接口设计）统一表达为一张图——节点显式编码能力需求、文件、类和函数，边捕获层次关系、数据流动和依赖。这种“规划即图”的表示使得代理在每一轮迭代中都能直接在图上索引、扩展和修正，从而获得三个关键优势：

1. **长期一致性**：图结构固有地保存了模块边界与依赖关系，避免了自然语言中规划意图的衰减与漂移。
2. **近线性可扩展性**：迭代中生成的代码行数（LOC）随轮次呈近线性增长（~980 LOC/迭代，R² > 0.97），突破了自然语言规划在 3–4 K LOC 后停滞的扩展壁障。
3. **高效定位与调试**：代理可直接沿图边进行导航式定位，显著减少搜索步数，使开发流程更稳定且可预测。

值得注意的是，即使移除外部知识库（EpiCoder Feature Tree）的辅助，仅凭 RPG 结构本身仍能支撑 87.2% 的覆盖率和稳定的代码体量增长，这表明**结构化图本身就是解耦规划模糊性与实现复杂性的核心驱动力**，而非简单的知识增加或模型升级。

基于这一动机，本文设计了 ZeroRepo 框架，以 RPG 为统一规划基础，将仓库生成解耦为三个阶段：提案级构建、实现级构建和图引导的代码生成。后续章节将详细阐述其设计与实验验证。

## 核心创新

### 痛点与动机：自然语言规划的扩展天花板

现有仓库级代码生成系统（如 MetaGPT、ChatDev、OpenHands、Claude Code CLI 等）普遍采用自由文本形式的自然语言规范作为规划媒介。该范式在中小规模仓库上尚可工作，但面对数百文件、数十模块的长期演化任务时，自然语言的歧义性迅速暴露为根本瓶颈：模块边界模糊、数据流关系隐式表达、跨迭代规划漂移，导致生成的不一致性与扩展停滞。实测中，以 Claude Code（o3-mini 驱动的终端代理）为首的最强基线在 RepoCraft 上的代码行数仅增长至约 10.6K 便在 3–4K LOC 附近陷入平台期，无法向更大仓库线性扩展（Figure 6）。

### 关键范式转换：从自然语言计划到结构化仓库规划图

本工作的**唯一却牵一发而动全身的“changed slot”**在于将**规划媒介（planning_medium）从自然语言彻底替换为结构化、机器可解析的仓库规划图（Repository Planning Graph, RPG）**（§1，§3.1）。RPG 是一张有向异构图，其节点显式编码**提案级功能目标**（如高层 capabilities、模块分解）与**实现级设计实体**（文件、类、函数），边则刻画层级归属、模块间数据流、函数调用和接口依赖（Figure 2）。这种显式图结构具备三大关键属性，直接回应自然语言规划的缺陷：

1. **双重规划的统一表示**：RPG 在同一图中承载“功能分解”（用户意图→子任务图谱）和“实现规划”（文件骨架、数据流 DAG、函数接口），消除了传统方法中高层意图与底层代码之间的语义鸿沟。
2. **持久、可追溯的长期记忆**：图节点与边一经建立便在迭代过程中保持稳定，编码代理可直接遍历图以检索依赖上下文，避免自然语言描述在长链推理中的遗忘与畸变。
3. **拓扑可生成性**：RPG 定义了严格的偏序关系——必须先实现被依赖的接口才能生成消费方代码。代码生成过程天然遵循图拓扑排序，从而将复杂的协同实现转化为可控的逐步展开任务。

### ZeroRepo 框架：围绕 RPG 的三阶段构造与驱动

为充分发挥 RPG 的潜力，论文设计了 **ZeroRepo 框架**，其核心流程完全围绕 RPG 的生命周期展开（Figure 1）：

- **提案级构造（Proposal-Level Construction）**：从用户自然语言查询出发，LLM 依托一个大规模全局特征树（EpiCoder Feature Tree）通过“探索-利用”子图采样（explore–exploit subtree selection，§3.2）生成一棵初始的功能性图谱；随后 LLM 通过目标对齐重构将功能节点聚合成高内聚模块，形成第一次结构化的功能分解。全局特征树在此充当先验知识库以避免遗漏常见功能类目，但其移除后 RPG 仍可独立支撑近线性扩展（Table 6），表明**图结构本身才是可扩展性的最大驱动力**。

- **实现级构造（Implementation-Level Construction）**：在功能图谱的基础上，LLM 进一步插入文件骨架节点（文件夹/文件名，§3.3.1）并设计模块间数据流的有向无环图（DAG），同时明确每个节点的类/函数接口签名（§3.3.2）。经过该阶段，RPG 已包含从文件夹到具体接口的完整实现视点。

- **图引导代码生成（Graph-Guided Code Generation）**：生成代理严格按 RPG 的拓扑序遍历节点，对每个节点执行测试驱动开发（TDD）：先生成单元测试，再生成实现代码，最后以测试为判据进行修复。当遇到错误或缺失依赖时，**图引导定位（graph-guided localization）** 根据 RPG 中的边信息快速将注意力聚焦到相关子图，相比无图搜索，步数降低 30–50%（Table 4）。该机制使代理能在数十次迭代中持续有效修复，而非陷入盲目重写。

### 创新驱动下的性能飞跃

以下来自 RepoCraft 基准的核心实验结果直接量化了上述创新的综合效果（Table 2）：

- **功能覆盖率的阶跃式提升**：ZeroRepo（o3-mini）达到 **81.5%** 的 Coverage，相较最强基线 Claude Code CLI（54.2%）**绝对提升 27.3 个百分点**；即使使用同规模的 Qwen3-Coder，Coverage（75.1%）仍高出 20.9 个百分点。
- **代码体量与规模的近线性扩展**：ZeroRepo（Qwen3-Coder）生成的代码量达到 **36,941 LOC**，约为基线 Claude Code 的 **3.9 倍**；且 LOC 增长随迭代次数保持近线性趋势（$y \approx 983x + 2992$, $R^2=0.97$，Figure 6），而所有自然语言基线均在 3–4K LOC 处停滞。
- **正确性的实质突破**：Pass Rate 从基线的 33.9% 提升至 **69.7%**（o3-mini），+35.8 个百分点，逼近人类开发者的 81.0%（Gold Projects 所反映的评测天花板），证明结构化规划对生成代码语义正确性的根本性改善。
- **消融强化内部归因**：移除外挂的 EpiCoder Feature Tree 后，ZeroRepo 在第 30 轮仍保持 **87.2%** 覆盖率和 **25,202 LOC** 的线性增长趋势（Table 6；Figure 7-8），确证 RPG 结构本身而非外部知识记忆承载了关键的可扩展性。

综言之，RPG 用一种图灵完备的结构替换了模糊的自然语言规划，使仓库级生成首次摆脱了扩展崩溃，为统一且可扩展的代码智能体提供了新的范式基础。该创新亦可解读为“思考实体化”——将代理的长期规划外化为显式图，赋予其人类工程的分层设计与迭代可控性。

## 整体框架

![[assets/figures/papers/iclr26_0013_VAQq3Y8tIF_RPG_A_Repository_Planning_Graph_for_Unified_and/figures/001_Figure_1.jpg]]
*Figure 1: The ZeroRepo pipeline for repository generation. (A) Proposal-Level Construction maps query to a functionality graph. (B) Implementation-Level Construction refines via (B1) File Structure Encoding into a file-augmented graph and (B2) Data-Flow/Function Encoding into the Repository Planning Graph (RPG). (C) Graph-Guided Code Generation traverses RPG to generate the repository*

![[assets/figures/papers/iclr26_0013_VAQq3Y8tIF_RPG_A_Repository_Planning_Graph_for_Unified_and/figures/002_Figure_2.jpg]]
*Figure 2: Repository Planning Graph: nodes encode repository capabilities, edges capture hierarchy and flows*

ZeroRepo 的核心设计在于用结构化的 **仓库规划图（Repository Planning Graph, RPG）** 替代自然语言规划，以解决自由文本规范在仓库级代码生成中固有的模糊性、缺乏显式结构以及难以追踪长期依赖这三个关键瓶颈。RPG 将“提案级规划”（功能分解）与“实现级规划”（文件结构/数据流/接口设计）统一为单一的可机读表示——图中节点捕获层次化的功能能力（可细化至文件、类、函数），边则显式编码语义关系与数据流（§3.1, Figure 2）。整个生成管线（Figure 1）围绕 RPG 的构造与执行展开，分为三个阶段。

**输入**：用户以自然语言描述的对目标仓库的整体意图（例如“一个类似 pandas 的数据分析库”）。

**阶段 Ⅰ — 提案级图构造（Proposal-Level Construction）**  
该模块将用户意图映射为一颗功能规划图。它从一个大规模全局特征树（EpiCoder Feature Tree）出发，通过 **探索‑利用**（explore–exploit）策略迭代选择与仓库目标相关的子树，并按照软件工程的内聚与耦合原则，对选出的功能节点进行重构与模块划分，最终得到一棵面向该仓库的 **功能图（functionality graph）**（§3.2, Appendix B.1）。这一阶段输出的是仅包含高层功能分解的图，尚未涉及文件、类或函数。

**阶段 Ⅱ — 实现级图构造（Implementation-Level Construction）**  
在功能图的基础上，系统进一步注入实现细节，将其扩展为完整的 RPG。该过程包含两个子步骤（Figure 1‑B1, B2）：
1. **文件结构编码**：为每个功能模块指派目录命名空间，生成文件骨架，将功能节点与具体的文件和文件夹关联。
2. **数据流与函数/接口编码**：在图中添加模块间/模块内的数据流边（构成有向无环图 DAG），并细化出类与函数的接口签名，形成可直接指导代码生成的精确规格（§3.3, Appendix C.1）。

至此，RPG 成为一个同时编码“做什么”与“怎么做”的统一规划实体，能够为后续生成提供稳定的、长程可追踪的结构基础。

**阶段 Ⅲ — 图引导的代码生成（Graph-Guided Code Generation）**  
代码生成阶段以 RPG 为主干，按拓扑顺序遍历图节点，并执行三条并行策略（§4）：
- **测试驱动的功能生成**：对每个叶子功能节点，交替生成测试用例与实现代码，直至测试通过。
- **图引导的定位与修复**：当集成测试或调试失败时，利用 RPG 中的依赖边和数据流边快速定位相关文件与函数，将搜索步数相较于无图引导降低 30–50%（Table 4）。
- **迭代式扩展与修复**：整个生成过程在最多 30 轮迭代内反复执行“规划—生成—测试—修复”循环，RPG 自身也会随着迭代逐步覆盖更多功能并保持适度的新颖性（Table 3）。

**输出**：一套包含完整目录结构、源代码与测试用例的软件仓库。

三个阶段通过 RPG 紧密耦合：提案级图提供功能的骨架范围，实现级图赋予其可执行的工程细节，而代码生成器则以图遍历的方式有序地将其“实例化”为真实代码。这一设计使得 ZeroRepo 的功能覆盖率与代码行数（LOC）能够随迭代轮次呈近线性增长（拟合斜率约 980 LOC/迭代，R² = 0.97），而自然语言规划基线往往在 3–4K LOC 停滞（Figure 6, §7.1）。消融实验进一步表明，即使移除全局特征树知识库，RPG 的结构本身仍支撑 87.2% 的覆盖率，验证了结构化图是驱动可扩展仓库生成的核心因素（Table 6, Figure 7‑8）。

## 核心模块与公式推导

### 1. 仓库规划图（RPG）结构

零样本仓库生成框架 ZeroRepo 的核心创新在于用**结构化、机器可解析的仓库规划图（RPG）**替代先前方法中的自由文本规划。RPG 将“提案级规划”（功能分解）与“实现级规划”（文件结构、数据流、接口设计）统一为一张显式图，从而消除自然语言规划的歧义和长距依赖追踪难题（§3.1, Figure 2）。

- **节点（Nodes）** 编码层次化的仓库能力，包含功能、文件、类和函数等不同粒度的实体。
- **边（Edges）** 刻画两类关系：
  - 层级与组成（父子功能、文件归属）；
  - 数据流与依赖（模块间/模块内接口、调用顺序）。

这种显式的图结构为后续的代码生成提供了可持久化、可精确定位的规划基础，是扩展性和高覆盖的根本驱动力。

### 2. ZeroRepo 的三阶段框架

框架围绕 RPG 的构建与使用组织为三个关键模块（Figure 1, §3‑4）：

**（A）提案级构建（Proposal-Level Construction）**  
- 利用一个大规模全局特征树（EpiCoder Feature Tree）作为功能本体，通过 **探索–利用（Explore–Exploit）子树选择** 机制（Algorithm 1, Appendix B.1）从用户查询中抽取出候选功能节点。  
- 基于频率概率 $p_i = \frac{f_i}{\sum_{j \in C} f_j}$（$f_i$ 为节点 $i$ 的采样频率，$C$ 为候选集）进行多样性与覆盖率感知的采样，并通过 **目标对齐重构（Refactoring）** 将选中的功能节点组织为初步的功能图。

**（B）实现级构建（Implementation-Level Construction）**  
- **文件骨架编码**：为功能子图分配文件夹/文件命名空间，生成文件‑功能映射，扩充为文件增强图。  
- **数据流与接口编码**：进一步为模块增加类‑函数接口、模块间/模块内数据流（有向无环图），完善为完整的 RPG——该图同时包含高层功能意图和低层实现细节（§3.3, Appendix C.1）。

**（C）图引导代码生成（Graph-Guided Code Generation）**  
- 按拓扑序遍历 RPG，对每个功能单元依次执行：
  1. 测试驱动开发（生成测试 → 生成实现 → 迭代修复）；
  2. **图引导定位**：当测试失败或需要增量开发时，利用 RPG 的依赖关系快速定位相关文件/函数，显著降低搜索步数（消融实验表明步数下降 30–50%，Table 4）；
  3. 图结构本身在迭代中保持稳定，支撑 **近线性的代码行数（LOC）增长**（$y \approx 983x + 2992,\ R^2=0.97$，其中 $x$ 为迭代数，$y$ 为生成的 LOC），而自然语言基线则在 3‑4K LOC 停滞（Figure 6, §7.1）。

### 3. 关键评估公式与变量含义

以下公式用于量化生成仓库的功能覆盖与新颖程度（Appendix E.3.1, §8），并刻画扩展性规律。

**覆盖率（Coverage）**  
$$
\mathrm{Coverage} = \frac{1}{|\mathcal{C}|}\sum_{j=1}^{K} \mathbf{1}\!\left[\,\exists g_i \in \mathcal{G},\ f(g_i) = c_j \right]
$$
- $\mathcal{C}$：参考类别集合，$|\mathcal{C}|$ 为其总数（通常 $K = |\mathcal{C}|$）。  
- $c_j$：第 $j$ 个参考类别。  
- $\mathcal{G}$：生成的特征集合，$g_i$ 为其中第 $i$ 个特征。  
- $f(g_i)$：将特征映射到其所属类别的函数。  
- 指标函数表示：只要存在至少一个生成特征属于 $c_j$，该类别即视为覆盖。  
该指标衡量生成仓库在语义类别级别上的“召回”。

**新颖率（Novelty）**  
$$
\mathrm{Novelty} = \frac{1}{|\mathcal{G}|}\sum_{i=1}^{N} \mathbf{1}\!\left[\,f(g_i) = c_{00\mathrm{D}} \right]
$$
- $c_{00\mathrm{D}}$：代表“分布外”（out‑of‑distribution）的特殊类别质心。  
- 其余符号同前。  
该指标计算生成特征中属于预定义类别体系之外的比例，用于评估规划的创新性而非简单复制。

**概率归一化（节点选择权重）**  
$$
p_i = \frac{f_i}{\sum_{j \in C} f_j}
$$
- $f_i$：节点 $i$ 在全局特征树中被 LLM 采样的原始频率（或启发式得分）。  
- $C$：当前步的候选节点子集。  
- $p_i$ 用于带多样性拒绝机制的子树采样（Algorithm 1，Appendix B.1），以平衡功能覆盖与模块多样性。

**代码行数线性缩放（LOC scaling）**  
- 带全局特征树（EFT）时：$y \approx 983x + 2992,\ R^2 = 0.97$  
- 移除 EFT 时：$y \approx 800x + 989,\ R^2 = 0.98$  
其中 $x$ 为迭代数，$y$ 为累计生成的代码行数。高 $R^2$ 值表明 RPG 驱动的生成能够维持几乎稳定的增量扩展能力，而自然语言基线的 LOC 增长在早期即进入平台期（Figure 7‑8, §8）。即使移除外部的特征树知识库，RPG 本身的图结构依然支撑着强劲的扩展趋势（在 30 轮时仍达到 87.2% 覆盖率和 25,202 LOC，Table 6），这证明结构化图是扩展性的首要因素。

> 注：线性拟合公式为实验后的经验规律，非理论推导；其余指标公式均来自论文附录的正式定义。若需复现，请以原文表述为准。

## 实验与分析

### 主要结果
我们在 RepoCraft 基准（Table 1）上评测了 ZeroRepo 与多种现有 Agent 框架。该基准包含六个匿名化的 Python 仓库，覆盖不同规模与领域，并通过统一自动管线进行评估；该管线的覆盖率与正确率判断与人类标注高度一致（Pearson’s r > 0.87）。

Table 2 汇总了各方法在不同模型后端下的表现：
- **覆盖率**：ZeroRepo (o3‑mini) 达到 **81.5%**，相较最强基线 Claude Code（54.2%）绝对提升 **27.3 pp**；在 Qwen3‑Coder 后端上亦获得 75.1%（+20.9 pp）。
- **通过率（Pass Rate）**：ZeroRepo (o3‑mini) 达 **69.7%**，较 Claude Code 的 33.9% 提升 **35.8 pp**，表明生成代码的正确性大幅提高。
- **代码体量**：ZeroRepo (Qwen3‑Coder) 生成 **36,941** 行有效代码（LOC），约为 Claude Code（10,587 行）的 **3.9 倍**；o3‑mini 后端亦达 23,977 行（~3.5 ×）。

![[assets/figures/papers/iclr26_0013_VAQq3Y8tIF_RPG_A_Repository_Planning_Graph_for_Unified_and/figures/005_Table_2.jpg]]
*Table 2: Performance of agent frameworks and model backbones on RepoCraft. “Nov.” denotes novelty rate; the number in parentheses is Novel/Total, where Novel is the count of novel functionalities and Total the number of planned ones. Gold Projects serve as a confidence ablation for the automatic evaluation pipeline, and per-repository results are reported in Appendix F.2*

RPG 赋予 ZeroRepo 的核心优势在于：通过将功能分解为显式节点、以数据流与接口边编码模块间关系，系统在生成全过程中维持了稳定的设计上下文，从而突破了自然语言规划在规模增长时出现的“实现衰退”。Figure 4 进一步展示了生成仓库中分层依赖与接口协同的存在，证实 RPG 可引导模型产出兼具复杂结构与内部一致性的代码库。

### 可扩展性分析
为揭示 RPG 对持续扩展的支撑能力，我们追踪了迭代过程中的功能节点数量与代码行数。Figure 5 与 Figure 6 显示，ZeroRepo 在 30 轮迭代内实现近乎线性的叶子功能增长与 LOC 增长（o3‑mini 叶子特征数突破 1,100，LOC 超 30,000），LOC‑迭代数线性拟合为 $y \approx 983x + 2992,\;R^2=0.97$。与之形成鲜明对比的是，基于自然语言规划的 Claude Code 等基线在 3–4 K LOC 即陷入停滞，无法持续扩展。

![[assets/figures/papers/iclr26_0013_VAQq3Y8tIF_RPG_A_Repository_Planning_Graph_for_Unified_and/figures/008_Figure_5.jpg]]
*Figure 5: Feature comparison of ZeroRepo (o3-mini) against strong baselines across iterations. Figure 6: Scaling behavior of LOC across iterations on MLKit-Py*

Table 3 揭示了 RPG 在覆盖率与新颖性上的迭代演化规律：在 MLKit‑Py 上，第 5 轮覆盖率仅为 70.2%，至第 30 轮攀升至 **95.7%**，同时新颖性稳定在约 **8%**（即 4.6%→7.9%）。这说明系统在不断引入新功能而非简单重复，得益于 RPG 的子图拓扑使得扩展可局部完成，并通过已有接口无缝融入整体。

### 消融实验
**图引导定位**。Table 4 对比了启用与禁用图引导时，代理在集成测试、增量开发及 Debugging 三种下游任务中的搜索步数。在 o3‑mini 下，**启用图引导可使步数降低 30–50%**。收益源于 RPG 将“功能‑文件‑函数”映射显式化为图拓扑，代理可沿依赖边快速定位，无需盲目扫描仓库全文。

![[assets/figures/papers/iclr26_0013_VAQq3Y8tIF_RPG_A_Repository_Planning_Graph_for_Unified_and/figures/010_Table_4.jpg]]
*Table 4: Ablation results for Graph-Guided Localization on MLKit-Py using o3-mini. Steps (mean ± SD). “- wo/- Graph” denotes ZeroRepo without Graph*

**全局特征树（EpiCoder Feature Tree, EFT）移除**。EFT 在提案阶段为 RPG 提供细粒度功能本体先验。我们将其移除，仅依靠通用 LLM 从用户意图直接构建功能图。Table 6 与 Figure 7‑8 显示，即使不使用 EFT，第 30 轮时 ZeroRepo 仍达到 **87.2%** 覆盖率并生成 **25,202** 行代码，LOC 增长依然保持近线性（$y \approx 800x + 989,\;R^2=0.98$）。相比于完整方案，覆盖率下降约 8 pp，但仍大幅超越基线。该消融直接证明 **RPG 的结构化图本身即为可扩展性的核心驱动因素**，EFT 主要提升初始规划精准度与最终覆盖率天花板。

![[assets/figures/papers/iclr26_0013_VAQq3Y8tIF_RPG_A_Repository_Planning_Graph_for_Unified_and/figures/014_Table_6.jpg]]
*Table 6: Iteration-30 ablation on MLKit-Py (o3-mini)*

### 失败模式与局限性
尽管 ZeroRepo 整体表现突出，实验仍暴露若干现实局限：

1. **评估偏差风险**：自动评估管线依赖 o3‑mini 进行测试适配与判分，虽然与人类判断的 Pearson r > 0.87，但 LLM 评估可能引入系统性偏差（§E.5）。
2. **测试生成随规模退化**：随已生成代码量上升，目标测试覆盖率出现波动并整体下降（Figure 14），暴露出长上下文下测试生成策略仍为瓶颈（§D.5）。
3. **领域先验依赖性**：RPG 初始构建质量受 EFT 影响；消融实验显示移除 EFT 后覆盖率下降 8 pp，当缺乏高质量特征本体时，功能分解的完备性将减弱（§8）。
4. **语言与领域泛化未验证**：当前仅在六个 Python 开源项目上验证，对多语言、企业级或跨平台仓库的适用性尚属未知。
5. **正确性落差**：生成仓库的最高通过率（69.7%）仍明显低于人类编写仓库的参照水平（81.0%，Table 2 中 Gold Projects），在复杂接口实现、边界条件与异常处理等方面仍有较大提升空间。

## 方法谱系与知识库定位

自然语言规划驱动的代码生成近年来涌现出两类代表性基线：一类以 **MetaGPT、ChatDev** 为代表的多智能体框架，依赖自然语言规约进行任务分解与协作；另一类以 **Claude Code CLI、OpenHands、Gemini CLI、Codex CLI** 为代表的“vibe-coding”终端代理，通过自由文本指令迭代编写代码。这些系统在仓库级生成时普遍暴露出一致性瓶颈——自然语言规约的模糊性导致模块划分失准、数据流断裂，且无法追踪长期依赖关系，使生成代码规模在 3–4K LOC 即停滞（Figure 6；Figure 5）。固定工作流系统 **Paper2Code** 虽引入了模板化流水线，但缺乏动态规划能力，同样难以应对跨模块的复杂依赖。

**ZeroRepo** 将规划媒介从自然语言转向结构化、机器可解析的 **仓库规划图（RPG）**，构成一条不同的方法路径。RPG 以节点显式编码功能能力、文件、类与函数，用边标注层级、数据流与接口依赖，将“提案级规划”（功能分解）与“实现级规划”（文件结构、数据流、接口设计）统一为有向图（§3.1，Figure 2）。这一改变使规划阶段不再受自然语言歧义的影响，支撑了后续图引导代码生成的 30–50% 的定位步数缩减（Table 4），并使仓库规模与功能覆盖率实现近线性扩展。消融实验进一步表明，即便移除作为外部知识库的 **EpiCoder Feature Tree**，RPG 结构仍能维持 87.2% 的覆盖率与稳定的 LOC 增长（$y \approx 800x + 989, R^2 = 0.98$），证明结构化图本身是扩展性的主要驱动力（Table 6；Figure 7-8）；知识库的作用更多体现在提升初始规划质量与覆盖率上限。

从与最强基线的对比看，**Claude Code CLI** 使用强大的后端模型（Sonnet）与终端代理范式，在 RepoCraft 上达到 54.2% 覆盖率与 33.9% 通过率，但 ZeroRepo 在同等迭代轮数下分别提升至 81.5% 与 69.7%（o3-mini），代码体量超 3.9 倍（Table 2）。该差异的核心并非模型算力，而是规划方式：自然语言规划在功能数量与代码行数上均呈饱和趋势，而 RPG 持续扩展功能数至 1,100+，LOC 近似线性增长（$y \approx 983x + 2992, R^2 = 0.97$，Figure 6），且同时保持 ~8% 的新颖率（Table 3）。因此，ZeroRepo 与方法谱系中的其他工作构成“规划媒介”维度的根本分叉，其 RPG 范式提供了一种可被下游图遍历、定位和修复算法直接消费的统一规划基座。

**适用边界与局限**  
当前验证仅限于六个 Python 开源参考仓库（scikit-learn、pandas、sympy、statsmodels、requests、django 经过改写后的 RepoCraft 版本，Table 1），对其他编程语言或企业级仓库的泛化性尚未测试。自动评估管道依赖 o3-mini 进行裁判与测试适配，虽与人工判断高度相关（Pearson’s r > 0.87），但仍可能引入系统性偏差（§E.5）。此外，测试生成质量随代码规模波动下降（Figure 14），导致通过率仍仅为 69.7%，远低于人工基准的 81.0%（Table 2）。RPG 的构建本身依赖大规模 LLM 的迭代查询，尽管消融证明结构本身具备鲁棒性，但在低资源或不具备全局特征树的知识库场景下，规划质量与新颖性可能受损。

**开放问题**  
RPG 范式的推广面临若干关键挑战：首先，如何改进测试生成与修复策略，在更大规模代码中维持高覆盖率与正确性；其次，能否将 RPG 扩展至多语言、跨平台的仓库生成，以检验图表示的表达力边界；再者，图构建过程的计算开销较高，研究更高效的规划算法以减少对 LLM 的重复调用是一项工程需求；最后，在长周期迭代或分布式开发中，RPG 的增量更新、合并与一致性维护策略仍有待定义——这些方向为后续工作提供了明确的接口。

## 原文 PDF

![[paperPDFs/ICLR_2026/RPG_A_Repository_Planning_Graph_for_Unified_and_Scalable_Codebase_Generation.pdf]]
