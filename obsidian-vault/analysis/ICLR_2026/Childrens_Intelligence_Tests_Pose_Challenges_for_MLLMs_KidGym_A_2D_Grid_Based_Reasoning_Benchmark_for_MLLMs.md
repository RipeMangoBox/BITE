---
title: "Children's Intelligence Tests Pose Challenges for MLLMs? KidGym: A 2D Grid-Based Reasoning Benchmark for MLLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Childrens_Intelligence_Tests_Pose_Challenges_for_MLLMs_KidGym_A_2D_Grid_Based_Reasoning_Benchmark_for_MLLMs.pdf
openreview_forum_id: Hj8Dc14nk1
aliases:
- Childrens_Intell
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "模型过度依赖语义信息和预训练中的常见模式，缺乏对抽象视觉结构和数量关系的鲁棒表示，导致在非语义任务和组合任务中表现不佳。"
primary_logic: "借鉴儿童智力测验设计多维度、动态、可定制的基准测试，能够有效揭示MLLMs在抽象推理、数量感知和复合能力上的根本性缺陷。"
claims:
- "闭源 MLLMs 在 KIDGYM 上的整体表现显著优于开源模型。"
- "模型在单一能力任务上的表现明显优于复合能力任务。"
- "MLLMs 在抽象、无语义的视觉信息推理上存在严重困难，PU 任务最高成功率仅为 0.30，仅略高于随机水平。"
- "MLLMs 对物品数量不敏感，Counting 任务中最佳模型在 L1 级别成功率也仅有 0.72，远低于人类（1.00）。"
---

# Children's Intelligence Tests Pose Challenges for MLLMs? KidGym: A 2D Grid-Based Reasoning Benchmark for MLLMs

> [!tip] 核心洞察
> 借鉴儿童智力测验设计多维度、动态、可定制的基准测试，能够有效揭示MLLMs在抽象推理、数量感知和复合能力上的根本性缺陷。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 儿童智力测试对MLLMs构成挑战？KidGym：基于2D网格的推理基准测试 |
| 英文题名 | Children's Intelligence Tests Pose Challenges for MLLMs? KidGym: A 2D Grid-Based Reasoning Benchmark for MLLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Hj8Dc14nk1); [Project](https://kidgym.github.io/KidGym-Website/) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | KIDGYM |
| Dataset | KIDGYM Counting (CO) L1, KIDGYM Puzzle (PU) L1, KIDGYM Classification (CL) L1, KIDGYM Filling (FI) L1 |

> [!tip] 效果简介
> - KIDGYM Counting (CO) L1 上，Success Rate 为 0.72 (Gemini-2.5-Pro)，对比 1.00 (Human)，变化 -0.28。
> - KIDGYM Puzzle (PU) L1 上，Success Rate 为 0.30 (GPT-5)，对比 0.25 (Random)，变化 +0.05。
> - KIDGYM Classification (CL) L1 上，Success Rate 为 1.00 (o3)，对比 0.46 (GPT-4o)，变化 +0.54。

## 概述

**问题背景**：当前多模态大语言模型（MLLMs）在真实场景理解和语义任务上取得了显著进展，但它们在抽象推理、数量感知以及多能力复合任务上的表现仍远逊于人类，尤其是儿童智力测试所考察的非语义抽象视觉推理能力，构成了 MLLMs 的根本性短板。

**核心洞察**：本文借鉴韦氏儿童智力量表的设计理念，提出 KIDGYM——一个基于 2D 网格的动态交互式基准，系统性地评估 MLLMs 在**执行、记忆、学习、规划、感知推理**五大核心认知能力上的表现。KIDGYM 的独特价值在于：通过动态场景随机生成、三级难度分层和 Gym API 可扩展架构，有效规避了传统静态基准中数据泄露和模式记忆的风险，从而更真实地揭示模型的推理瓶颈。

**方法定位**：KIDGYM 包含 12 个任务，每个任务至少考察一种核心能力，并支持单一能力与复合能力的组合评估。与现有基准（如 **LogicGame** (Gui et al., 2024)、**EgoPlan** (Chen et al., 2024)、**MileBench** (Song et al., 2024)）相比，KIDGYM 在任务动态性、难度层级、用户可扩展性和评估维度上均实现了关键突破（Table 1）。其高层动作接口和物品标识系统降低了操作粒度，使评估聚焦于目标导向的认知行为。

**主要结果**：
- **闭源模型整体领先**：o3、GPT-5 和 Gemini-2.5-Pro 在所有能力维度上显著优于开源模型，但离人类水平仍有明显差距。
- **单一能力优于复合能力**：多数模型在单一能力任务上的成功率显著高于复合能力任务，表明跨能力整合是当前 MLLMs 的薄弱环节。
- **非语义抽象推理严重困难**：在 Puzzle (PU) 任务中，最佳模型 GPT-5 在 L1 难度的成功率仅为 0.30，仅略高于随机水平（0.25），暴露了模型对无语义视觉结构的推理缺陷。
- **数量感知能力不足**：在 Counting 任务中，表现最好的 Gemini-2.5-Pro 在 L1 级别成功率也仅有 0.72，而人类为 1.00，说明模型对物品数量缺乏鲁棒的感知表征。

**方法谱系与知识库定位**：KIDGYM 处于 MLLM 评估基准与认知能力测试的交叉地带。它继承了强化学习环境（如 **MiniGrid** (Chevalier-Boisvert et al., NeurIPS 2023)）的交互范式，但面向 MLLMs 而非 RL 智能体；同时吸收了视觉推理基准（如 ARC-AGI-2）的抽象推理设计，但通过动态场景和多维能力框架提供了更全面的评估体系。其可扩展的 Gym API 接口使其成为研究 MLLM 认知能力的通用实验平台。

## 背景与动机

多模态大语言模型（MLLMs）在视觉问答、图像描述等语义密集型任务上已取得显著进展，但其在抽象视觉推理、数量感知以及多能力协同方面的表现仍不明朗。现有评估基准多聚焦于静态场景下的单一能力测试，难以系统揭示模型在动态交互环境中整合执行、记忆、学习、规划与感知推理等核心认知能力的真实水平。例如，**Crafter**（Hafner, 2021）和 **MiniGrid**（Chevalier-Boisvert et al., NeurIPS 2023）主要面向强化学习范式，而 **LogicGame**（Gui et al., 2024）、**EgoPlan**（Chen et al., 2024）等基准则缺乏难度层级划分与用户可扩展性（Table 1）。

儿童智力测验通过多维度、分难度的任务设计来评估认知发展，这一思路为诊断 MLLMs 的根本性缺陷提供了启示。本文的核心动机在于：借鉴韦氏智力测验的评估框架，构建一个动态、可定制、覆盖五大核心能力的 2D 网格基准，以揭示 MLLMs 在非语义抽象推理、数量感知及复合能力上的真实瓶颈。

## 核心创新

KIDGYM 的核心创新在于将儿童智力测验范式系统性地迁移至多模态大模型（MLLM）评估，通过四个关键维度突破了现有基准的局限。

**动态交互式任务设计。** 与大多数现有 MLLM 基准的静态评估不同，KIDGYM 要求模型在动态环境中执行连续动作序列以完成任务（Table 1）。这一设计使得评估从“单步问答”转向“多步目标导向行为”，更贴近真实智能体的运作方式。例如，**EgoPlan**（Chen et al., 2024）和 **MileBench**（Song et al., 2024）等现有 MLLM 基准均为静态场景，而 KIDGYM 通过 Gym API 实现了完全动态的交互循环。

**多层级难度体系。** 每个任务均设置 L1/L2/L3 三个难度级别，从易到难递进（Section 1）。实验验证了这一设计的有效性：模型成功率从 L1 到 L3 普遍下降，证实了难度分层的合理性（Table 2）。相比之下，现有基准如 **LogicGame**（Gui et al., 2024）和 **MiniGrid**（Chevalier-Boisvert et al., NeurIPS 2023）缺乏或仅有有限的难度层级支持。

**五维能力覆盖与复合评估。** KIDGYM 借鉴韦氏智力测验的核心指标，定义了执行、记忆、学习、规划、感知推理五大认知能力维度（Section 3），并通过 12 个任务实现单一能力与复合能力的同步评估。这是其与现有基准最本质的区别：**Crafter**（Hafner, 2021）和 **MiniGrid** 主要面向强化学习范式，**ARC-AGI-2** 等基准则侧重单一能力维度，而 KIDGYM 首次在 MLLM 评估中实现了多维度能力的系统解耦与组合测试。

**完全可扩展的开放框架。** 基于标准化 Gym API 构建的环境使得研究人员可以自定义新场景、新任务和新难度级别（Section 1, Section 6.2）。配合场景与物品的随机生成机制——每次交互的布局和物品位置均不同——有效降低了数据泄露和记忆效应的风险。这种用户可扩展性在现有 MLLM 基准中极为罕见。

上述四个 changed slots 共同构成了 KIDGYM 的方法论贡献：它并非简单增加任务数量，而是通过动态性、层级化、多维度和可扩展性四个维度的协同设计，构建了一个能够揭示 MLLM 根本性能力缺陷的评估框架。

## 整体框架

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Hj8Dc14nk1/figures/013_Table_1.jpg]]
*Table 1: Comparison of KIDGYM with existing benchmarks across target paradigm, difficulty-level support, user extensibility, evaluated capabilities, and dynamic vs. static settings*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Hj8Dc14nk1/figures/014_Figure_2.jpg]]
*Figure 2: A KIDGYM task frame comprises a scene map, a backpack, and a hint bar. We provide varied agent skins, backgrounds, and scene-specific items; backpack slots and in-scene items are letter/number-labeled for identification. Resolution and grid layout are specified in Appendix B.1*

KIDGYM 被设计为一个面向多模态大语言模型（MLLM）的交互式、动态化、可扩展的二维网格推理基准。其整体框架围绕“场景生成—状态维护—动作交互—能力评估”四条主线构建，通过标准化的 Gym API 将各模块串联为闭环评测管线。

### 场景与任务生成器

任务场景和物品布局采用完全随机化生成策略，每次交互初始化时，物品位置、智能体出生点等元素均重新随机排列，确保任意两轮测试不存在相同场景。这一设计从机制层面抑制了数据泄露与模型记忆效应，使得性能差异更可能归因于推理能力本身。同时，框架内置了超市、食堂、农场等多种语义场景，进一步降低模型依赖单一视觉模式进行匹配的可能性。

### 背包与提示栏

为帮助模型在多轮交互中维持上下文一致性，每个任务帧除场景地图外，还包含背包（Backpack）和提示栏（Hint Bar）两个状态组件。背包记录智能体已拾取或携带的物品，提示栏则提供当前任务目标或阶段性指引。模型可通过观察这两个组件获取关键信息，而不必完全依赖对历史帧的记忆，从而将评估重心聚焦于目标导向的决策与推理。

### 高层动作接口

KIDGYM 提供宏观动作（如“捡起篮球”、“移动到书架”），而非像素级或底层控制指令。这种高层动作抽象降低了操作粒度，使模型无需处理细粒度运动规划，能够将注意力集中于任务逻辑与策略选择。动作执行后，环境返回更新后的场景图像与状态信息，构成标准的观察—动作—反馈循环。

### 物品标识系统

场景中每个物品均被分配唯一标识（字母或数字标签），在视觉元素与其文本描述之间建立显式映射。该机制使模型能够通过自然语言精确引用特定物品，避免因视觉歧义导致的指令解析错误，同时为评估模型对空间位置与物品属性的感知推理能力提供了可控的测试条件。

### 评估模块与能力维度

评估模块在每轮测试中记录成功率，并以此为基础计算五维能力得分。KIDGYM 将韦氏儿童智力测验的核心指标转化为 MLLM 的五项关键能力：执行（Execution）、记忆（Memory）、学习（Learning）、规划（Planning）和感知推理（Perception Reasoning）。12 个任务各自考察至少一种能力，其中部分任务同时考察多种复合能力。最终得分通过雷达图可视化，直观展示模型在不同能力维度的强弱分布。

### 与现有基准的差异化定位

Table 1 将 KIDGYM 与 10 个现有基准进行了系统性对比。在目标范式上，Crafter 和 MiniGrid 面向强化学习，LogicGame 面向纯文本大语言模型，EgoPlan、MileBench 等面向 MLLM；KIDGYM 同样面向 MLLM，但首次将动态交互、三级难度分层和用户可扩展性集成于同一框架。在评估能力维度上，现有基准通常仅覆盖单一或少量能力，KIDGYM 则同时覆盖执行、记忆、学习、规划、感知推理五大维度及多种复合能力组合。在可扩展性方面，KIDGYM 基于 Gym API 构建，用户可自定义新场景、新任务和新物品，而多数现有基准不具备此类定制化能力。

**证据强度说明**：上述模块关系与输入输出流均基于论文第 4 节（Mechanics）和第 6.2 节（实验设置）的明确描述，置信度较高。Table 1 的对比结论来自原文表格的直接呈现。需注意，框架内部各模块的具体实现细节（如随机种子管理、API 调用频率限制）未在论文中完整披露，若需复现应参考其开源代码仓库。

## 核心模块与公式推导

KIDGYM 本身是一个基准测试框架，不涉及模型架构层面的公式推导。其核心设计体现在环境构建与任务生成的工程化模块中，以下梳理支撑该基准的关键组件。

### 环境与任务生成模块

KIDGYM 通过五个核心机制确保任务的多样性与评估的公平性：

- **场景与任务生成器**：根据任务类型和难度层级（L1/L2/L3）随机生成网格布局与物品分布。每次初始化时，物品位置、智能体出生点等元素均随机排列，确保任意两轮任务不完全相同（Section 4: Randomness）。这一随机化策略有效降低了模型记忆特定模式的风险。
- **多语义场景**：设计了超市、食堂、农场等多种环境背景，通过语义多样性缓解数据泄露或污染问题（Section 4: Diverse Semantic Scenes）。
- **背包与提示栏**：作为任务状态组件，背包记录已收集物品，提示栏提供当前任务目标或线索。二者共同帮助模型在多轮交互中维持上下文一致性（Section 4: Backpack and Hint Bar）。
- **高层动作接口**：提供宏观动作（如“捡起篮球”），降低操作粒度，使评估聚焦于目标导向的推理与决策，而非底层控制精度（Section 4: High-level Actions）。
- **物品标识系统**：为场景中每个物品分配唯一的字母/数字标签，将视觉元素与文本描述精确关联，便于模型进行指代与操作（Section 4: Identification）。

### 评估与能力量化模块

KIDGYM 的能力评分体系借鉴韦氏儿童智力量表的核心指标，将评估维度映射为五个可量化能力：

- **执行（Execution）**：通过 Classification（CL）任务显式测量，CL 分数提供执行就绪度的最清晰参考（Section 6.4）。
- **感知推理（Perception Reasoning）**：通过 Puzzle（PU）、Counting（CO）等任务中的视觉结构理解与数量感知表现间接评估。
- **记忆（Memory）**：通过 Memory Maze、Memory Filling 等需要跨轮次信息保留与整合的任务测量。
- **学习（Learning）**：通过 Placement（PL）等需要从示例中归纳规则的任务评估。
- **规划（Planning）**：通过 Maze、Counting 等需要多步决策的任务体现。

各维度能力分数汇总后通过五维雷达图（Figure 3）进行可视化对比，直观展示闭源与开源模型在不同能力轴上的差异。

### 公式说明

本基准测试不涉及模型内部公式。评估指标仅为成功率（Success Rate），定义如下：

$$ \text{Success Rate} = \frac{\text{成功完成的任务轮数}}{\text{总评估轮数}} $$

其中，每项任务在固定随机种子上运行 100 轮，以真实最优解为参照标准，结果保留两位小数（Table 2）。该指标直接反映模型在给定难度下完成目标导向任务的能力，但未考虑效率、泛化等其他维度。

> 注：本文未提供任何模型架构或损失函数相关的数学公式，因此本节不进行额外推导。

## 实验与分析

### 主实验结果

KIDGYM 在零样本设定下对 9 个前沿 MLLM 进行了系统评估，包含 6 个闭源模型（**o3**、**GPT-5**、**GPT-4o**、**Gemini-2.5-Pro**、**Gemini-2.5-Flash**、**Claude-3.7-Sonnet**）和 3 个开源模型（**DeepSeekVL-2**、**QwenVL-2.5**、**InternVL-3**）。所有模型在相同随机种子上进行 100 轮评估，封闭模型通过官方 API 调用，开源模型使用 NVIDIA RTX A6000 运行，确保可比性。

**总体性能格局**：闭源 MLLM 在 KIDGYM 上的整体表现显著高于开源模型（Table 2），其中 **o3**、**GPT-5** 和 **Gemini-2.5-Pro** 在所有能力维度上占据主导地位。然而，即便是最强模型，在特定任务上仍与人类水平存在巨大差距。


![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Hj8Dc14nk1/figures/015_Table_2.jpg]]
*Table 2: Zero-shot performance comparison of MLLMs across 12 KIDGYM tasks. “L” denotes the task level. Performance is measured by the success rate over 100 rounds under the ground-truth optimal solution, rounded to two decimal places*

**单能力 vs. 复合能力**：大多数模型在单一能力任务上的表现明显优于复合能力任务。这一趋势表明，MLLM 在需要同时整合多种认知能力时面临显著困难，复合任务构成了当前模型能力的核心瓶颈。

**难度层级验证**：成功率从 L1 到 L3 普遍递减，验证了任务难度分级的合理性。这一递减趋势在不同模型和任务类型上表现一致。

### 关键任务瓶颈分析

**抽象视觉推理的严重缺陷**：Puzzle（PU）任务揭示了 MLLM 在非语义、抽象视觉信息推理上的根本性短板。该任务要求模型从纯几何图案中识别整体结构，无法依赖语言描述。最佳模型 **GPT-5** 在 PU-L1 上的成功率仅为 0.30，仅比随机水平（0.25）高出 5 个百分点。这一结果表明，当前 MLLM 过度依赖语义信息和预训练中的常见模式，缺乏对抽象视觉结构的鲁棒表示。

**数量感知的显著不足**：Counting（CO）任务暴露了模型对物品数量的不敏感性。即便是表现最好的 **Gemini-2.5-Pro**，在 L1 级别成功率也仅有 0.72，而人类成功率为 1.00。模型倾向于依赖高分辨率视觉线索进行计数，而非形成真正的数量表征，这在高难度级别表现更为明显。

**任务间表现分化**：Classification（CL）任务上，**o3** 在 L1 级别达到 1.00 的成功率，而 **GPT-4o** 仅为 0.46，模型间差异显著。Filling（FI）任务上，**o3** 以 0.83 的成功率领先于 **GPT-4o** 的 0.66。这些差异反映了不同模型在执行基础能力和感知推理上的结构性强弱。

### 推理方法的差异化影响

推理方法对不同模型和任务的影响存在显著差异。**Gemini-2.5-Flash** 在使用 Chain-of-Thought（CoT）方法后，相比零样本有显著提升，表明显式推理步骤对部分模型有益。然而，**o3** 由于内部已集成 CoT 机制，在零样本和 CoT 设定之间未表现出实质性差异。这一发现揭示了推理方法的效果高度依赖模型架构，通用推理策略可能无法对所有模型产生一致的增益。

此外，In-Context Learning（ICL）在随机场景下可能引入干扰，在某些记忆和学习任务中甚至劣于零样本。这一反直觉现象的机理和适用范围仍有待进一步研究。

### 五维能力雷达图分析

通过计算五个维度的能力分数并生成雷达图（Figure 3），可以更直观地比较模型的能力轮廓：


![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Hj8Dc14nk1/figures/016_Figure_3.jpg]]
*Figure 3: Five-dimensional capability radar chart. The chart on the left shows the capability scores of the closed-source models, while the chart on the right shows those of the open-source models*

- **闭源模型的优势领域**：o3、GPT-5 和 Gemini-2.5-Pro 在学习和记忆维度表现相对较好，但仍与人类水平存在实质性差距。
- **通用短板**：所有被评估的 MLLM 在感知推理（Perception Reasoning）和规划（Planning）能力上普遍得分较低。这一发现与 Puzzle 和 Counting 任务的低成功率相互印证，确认了当前模型在需要深层视觉理解和策略规划时的系统性不足。
- **执行能力的基准参考**：Classification（CL）任务被用作执行能力的显式度量，其得分提供了模型执行就绪度的最清晰参考。

### 消融与鲁棒性分析

**图像分辨率的影响**：提高图像分辨率可提升多个模型在 Counting 任务上的准确率，但这种提升主要源于对高分辨率视觉线索的更好利用，而非数量表征能力的质变。模型仍未形成对数量的抽象理解。

**随机化设计的有效性**：任务场景和物品布局的完全随机生成有效降低了数据泄露和记忆效应的风险。由于每轮初始化时元素排列均被随机化，模型无法通过记忆特定布局模式来作弊，这使得成功率能够更真实地反映模型的推理能力。

### 失败模式总结

综合实验结果，MLLM 在 KIDGYM 上的主要失败模式可归纳为三类：

1. **抽象视觉推理失败**：在缺乏语义锚点的纯几何图案任务中，模型无法有效提取空间结构和关系，表现接近随机。
2. **数量感知偏差**：模型依赖视觉启发式而非精确计数，在物品密集或布局复杂的场景中错误率显著上升。
3. **复合能力整合困难**：当任务需要同时调动多种认知能力（如记忆+规划、学习+感知推理）时，模型表现明显下降，表明能力模块之间的协同机制尚未建立。

### 补充图表

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Hj8Dc14nk1/figures/006_Figure_6.jpg]]
*Figure 6: (f) Puzzle*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_Hj8Dc14nk1/figures/008_Figure_8.jpg]]
*Figure 8: (h) Counting*


## 方法谱系与知识库定位

KIDGYM 的定位介于传统强化学习环境与静态多模态语言模型基准之间，其核心贡献在于将儿童智力测验范式转化为一个动态、可交互、多维度的评估框架。与现有工作相比，KIDGYM 在以下四个关键维度上形成了差异化。

**范式转换：从静态到动态交互。** 大多数面向 MLLM 的基准测试（如 **EgoPlan** (Chen et al., 2024)、**MileBench** (Song et al., 2024)）采用静态任务设计，模型仅需在单轮内给出回答。KIDGYM 则引入连续动作序列，要求模型在多轮交互中完成目标，这使其更接近 **Crafter** (Hafner, 2021) 和 **MiniGrid** (Chevalier-Boisvert et al., NeurIPS 2023) 等 RL 环境的交互范式，但将评估对象从 RL agent 转向了 MLLM。这一转变的关键瓶颈在于：MLLM 需要同时处理视觉感知、上下文记忆和序列决策，而非单一能力的孤立测试。

**能力覆盖的广度与结构化分层。** 现有 MLLM 基准通常聚焦于单一或少量能力维度：**LogicGame** (Gui et al., 2024) 侧重逻辑推理，**ARC-AGI-2** 侧重抽象模式识别。KIDGYM 则系统性地覆盖了执行、记忆、学习、规划、感知推理五大核心能力，并通过 12 个任务（含 6 个单一能力任务和 6 个复合能力任务）构建了能力矩阵。更重要的是，每个任务设置了 L1/L2/L3 三个难度层级，成功率的递减趋势验证了难度分层的有效性。这种结构化设计使得研究者可以定位模型在特定能力维度和难度层级上的精确短板。

**非语义抽象推理的独特探测价值。** KIDGYM 中 Puzzle 任务的设计尤为关键：它剥离了语义信息，仅保留纯视觉结构，直接探测模型对抽象视觉模式的感知推理能力。实验结果显示，最强模型 GPT-5 在 PU-L1 上的成功率仅为 0.30，仅比随机水平（0.25）高 5 个百分点。这一证据揭示了当前 MLLM 的根本性缺陷——过度依赖语义先验，缺乏对视觉结构和空间关系的鲁棒表征。相比之下，语义丰富的 Classification 任务中 o3 可达 1.00 成功率，这种强烈反差进一步强化了上述结论。

**适用边界与局限。** KIDGYM 的适用边界受限于三个因素：（1）2D 网格环境的抽象性使其无法完全反映真实世界多模态任务的复杂性和噪声特征；（2）评估指标仅为成功率，未考虑效率、泛化能力或错误类型分析；（3）部分封闭模型通过 API 评估，内部推理过程不透明，难以深入诊断失败机制。此外，尽管任务场景和物品布局完全随机生成以降低数据泄露风险，但在有限的任务类型下，模型仍可能通过记忆特定模式而非真正推理来获得高分。

**开放问题。** 本基准揭示的瓶颈指向四个关键研究方向：（1）如何提升模型对非语义、抽象视觉信息和数量特征的鲁棒处理能力，而非依赖高分辨率视觉线索的捷径；（2）如何设计训练策略使 MLLM 在复合能力任务中有效整合多种认知能力，而非各能力间的简单叠加；（3）ICL 在某些记忆和学习任务中劣于零样本的机理尚不明确，需进一步研究其适用范围和失效条件；（4）如何将 KIDGYM 的评估范式扩展到三维或真实世界环境，同时保持任务的可控性和可复现性。

## 原文 PDF

![[paperPDFs/ICLR_2026/Childrens_Intelligence_Tests_Pose_Challenges_for_MLLMs_KidGym_A_2D_Grid_Based_Reasoning_Benchmark_for_MLLMs.pdf]]
