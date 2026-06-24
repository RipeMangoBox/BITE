---
title: "Multi-Agent Design: Optimizing Agents with Better Prompts and Topologies"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Multi_Agent_Design_Optimizing_Agents_with_Better_Prompts_and_Topologies.pdf
openreview_forum_id: I05H9RUzHB
aliases:
- MASSM
- MADOABPT
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "MASS框架通过三阶段交错优化（局部提示‘预热’→基于影响力剪枝的拓扑搜索→全局提示联合微调）解耦提示与拓扑的联合搜索空间，从而高效找到高性能多智能体系统。"
primary_logic: "有效的多智能体系统设计需将提示优化与拓扑搜索协同进行：先优化局部智能体提示，再根据验证性能影响筛选有潜力的拓扑结构，最后进行全局微调以提升协作效率。"
claims:
- "在MATH数据集上，通过提示优化可以有效提升token效率，优于增加智能体数量或改变拓扑的方法。"
- "MASS在Gemini 1.5 Pro的8个任务上平均准确率达78.79%，显著优于所有基线（如CoT的65.28%、ADAS的69.72%）。"
- "消融实验表明，MASS的三个优化阶段都能带来累积增益：1PO提升约6%，2PO再提升3%，3PO额外提升~2%。"
- "并非所有拓扑都对MAS有正面影响，仅少数拓扑（如Debate、Summarize）能提升性能。"
---

# Multi-Agent Design: Optimizing Agents with Better Prompts and Topologies

> [!tip] 核心洞察
> 有效的多智能体系统设计需将提示优化与拓扑搜索协同进行：先优化局部智能体提示，再根据验证性能影响筛选有潜力的拓扑结构，最后进行全局微调以提升协作效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 多智能体设计：优化智能体的提示与拓扑结构 |
| 英文题名 | Multi-Agent Design: Optimizing Agents with Better Prompts and Topologies |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=I05H9RUzHB) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Multi-Agent System Search (MASS) |
| Dataset | MATH, DROP, HotpotQA, MuSiQue |

> [!tip] 效果简介
> - MATH 上，准确率 (%) 为 84.67，对比 71.67 (CoT)，变化 +13.00。
> - DROP 上，F1 (%) 为 90.52，对比 70.59 (CoT)，变化 +19.93。
> - HotpotQA 上，F1 (%) 为 69.91，对比 57.43 (CoT)，变化 +12.48。

## 概述

多智能体系统（Multi-Agent System, MAS）通过引入多个大语言模型（LLM）智能体协同工作，在复杂推理、多跳问答和代码生成等任务上展现出超越单智能体的潜力。然而，设计一个高效的多智能体系统面临**组合爆炸**的核心瓶颈：提示（prompt）的敏感性与拓扑（topology）的复杂性相互交织——手工设计的提示难以激发智能体的最佳能力，而固定拓扑（如自一致性、辩论）无法适配不同任务的需求。更关键的是，提示与拓扑并非独立变量：一个拓扑的有效性高度依赖于其内部智能体的提示质量，反之亦然。现有方法要么仅优化提示而忽略拓扑，要么在固定提示下搜索拓扑，导致性能始终处于次优状态。

针对上述问题，本文提出**MASS（Multi-Agent System Search）**框架，其核心洞察是：**有效的多智能体系统设计必须将提示优化与拓扑搜索协同进行**。MASS通过一个三阶段交错优化流程，解耦并高效探索提示与拓扑的联合搜索空间：

1. **块级提示优化（1PO）**：先对单个预测智能体进行提示“预热”，再对每种拓扑模块（聚合、反思、辩论、摘要、工具使用）独立优化其指令和示例提示，使每个构建块达到局部最优。
2. **基于影响力剪枝的拓扑搜索（2TO）**：计算各拓扑模块的增量影响力 $I_{a_i}$，通过Softmax概率剪枝排除无效或有害的模块，在精简空间中随机采样并评估工作流配置，选出最佳拓扑。
3. **工作流级全局提示优化（3PO）**：在最佳拓扑上对所有智能体进行联合提示微调，以适应多智能体协作带来的分布偏移。

在Gemini 1.5 Pro上，MASS在8个任务上的平均准确率达**78.79%**，显著优于所有基线：相比单智能体CoT的65.28%提升13.51个百分点，相比自动化智能体设计框架ADAS的69.72%提升9.07个百分点。消融实验证实三个优化阶段均带来累积增益——1PO提升约6%，2TO再提升约3%，3PO额外贡献约2%——且搜索空间剪枝和前期提示优化对拓扑搜索的效果至关重要。值得注意的是，并非所有拓扑都对多智能体系统有正面影响：在HotpotQA上，仅辩论拓扑带来约3%的性能增益，而其他拓扑甚至导致性能退化，这进一步验证了MASS自动筛选有效拓扑的必要性。

MASS的贡献在于首次将多智能体系统的提示优化与拓扑搜索纳入统一的自动化设计框架，通过交错优化和影响力剪枝有效降低了联合搜索的复杂度，为构建高性能多智能体系统提供了一条可复用的方法论路径。

## 背景与动机

### 多智能体系统的设计困境

大语言模型（LLM）驱动的多智能体系统（MAS）在复杂推理、多跳问答和代码生成等任务上展现出超越单智能体的潜力。然而，构建高性能MAS面临一个核心瓶颈：**自动化设计中的组合爆炸问题**。MAS的性能高度依赖于两个相互交织的维度——每个智能体的提示（prompt）设计和智能体间的协作拓扑（topology）结构。提示的微小调整可能改变智能体的输出分布，进而影响整个通信链路的有效性；而拓扑的变更又会改变信息聚合方式，使得为某一拓扑优化的提示在另一拓扑下失效。现有方法往往仅单独优化提示或拓扑，导致性能次优，无法充分利用二者的协同效应。

### 现有方法的局限

当前主流的MAS设计范式可归为三类，各有明显短板：

- **手工设计范式**：如 **Self-Consistency**（多数投票聚合）、**Self-Refine**（迭代反思改进）和 **Multi-Agent Debate**（多轮辩论聚合），依赖人工预设固定的拓扑和提示模板。这类方法忽视了提示敏感性——如 Figure 2 所示，在 MATH 数据集上，经过提示优化的单个智能体在 token 效率上显著优于单纯扩展智能体数量（自一致性、自反思或辩论），说明**提示优化比盲目增加智能体或改变拓扑更具成本效益**。

- **自动化智能体设计范式**：如 **ADAS**（LLM 元智能体迭代生成新智能体），虽能自动搜索智能体配置，但仅聚焦于单个智能体的提示设计，未涉及多智能体拓扑的联合优化。

- **自动化工作流设计范式**：如 **AFlow**（蒙特卡洛树搜索优化拓扑），在预定义算子集合上搜索工作流结构，但忽略了提示与拓扑的交互——为某一拓扑优化的提示无法迁移到另一拓扑，导致搜索效率低下。

这三种范式的共同缺陷在于：**将提示优化与拓扑搜索割裂处理**，无法应对二者交织产生的组合爆炸。更重要的是，并非所有拓扑都对 MAS 性能有正面影响——如 Figure 4 所示，在 LiveCodeBench 上，Reflect 拓扑甚至使性能下降约 15%，而 Execute 拓扑带来约 10% 的提升。这意味着**盲目搜索整个拓扑空间不仅低效，还可能引入有害配置**。

### MASS 的核心洞察

本文的核心洞察是：**有效的多智能体系统设计需将提示优化与拓扑搜索协同进行**。具体而言，应先通过局部提示优化“预热”每个拓扑模块，使其发挥基本功能；再根据各模块在验证集上的增量影响力筛选有潜力的拓扑结构，剪枝无效或有害的模块以压缩搜索空间；最后在选定拓扑上进行全局提示联合微调，使各智能体的提示适配协作上下文。这种从局部到全局、从提示到拓扑的交错优化策略，是突破组合爆炸、高效发现高性能 MAS 的关键。

## 核心创新

MASS的核心创新在于**将多智能体系统的提示优化与拓扑搜索解耦为三阶段交错优化**，通过“局部预热—影响力剪枝—全局微调”的递进策略，有效应对提示敏感性与拓扑复杂性交织导致的组合爆炸问题。相较于仅单独优化提示或拓扑的基线方法，MASS在以下四个关键维度上实现了根本性改进：

### 1. 三阶段交错优化策略

传统自动化设计方法（如ADAS、AFlow）要么仅优化智能体提示，要么仅在固定提示下搜索拓扑，缺乏对二者协同效应的建模。MASS将优化过程拆分为三个递进阶段：

- **块级提示优化（1PO）**：对每个拓扑模块（Predictor、Reflector、Debator等）独立优化指令与示例提示，为后续拓扑搜索提供高质量的局部组件。该阶段相比单智能体APO基线平均提升约6%的性能（Figure 5左）。
- **工作流拓扑优化（2TO）**：在剪枝后的搜索空间中组合拓扑模块，通过随机采样与评估选择最佳工作流配置。该阶段在1PO基础上再带来约3%的提升（Figure 5左）。
- **工作流级全局提示优化（3PO）**：在最佳拓扑上对所有智能体进行联合提示微调，使各模块的提示适应多智能体协作场景，进一步贡献约2%的增益（Figure 5左）。

这种“从局部到全局、从提示到拓扑”的递进设计，使得每个阶段都能在前一阶段的基础上聚焦更精确的优化目标，避免了直接联合优化面临的高维搜索空间。

### 2. 基于增量影响力的搜索空间剪枝

MASS的关键洞察在于：并非所有拓扑结构都对多智能体系统有正面贡献。Figure 4的实验表明，在HotpotQA上仅Debate拓扑带来约3%的提升，而其他拓扑（如Reflect）未能改善甚至降低了性能。基于此，MASS引入**增量影响力**指标 $I_{a_i} = \mathcal{E}(a_i^*) / \mathcal{E}(a_0^*)$，衡量每个拓扑模块相对于初始智能体的性能增益比，并通过 $\mathrm{Softmax}(I_a, t)$ 将影响力转化为选择概率，以概率剪枝方式排除无效或有害的模块。消融实验表明，移除剪枝步骤会显著降低2TO的优化效果（Figure 5右），验证了剪枝对搜索效率的关键作用。

### 3. 统一的可配置设计空间

MASS将多智能体系统的设计空间统一为**提示空间**（指令与示例）与**拓扑空间**（Aggregate、Reflect、Debate、Summarize、Tool-use五大构建块及其连接方式）的组合。这一设计空间既保持了足够的表达能力以覆盖主流多智能体协作模式，又通过模块化定义降低了搜索复杂度。Table 3明确了每个拓扑模块的搜索维度（如Aggregate的并行智能体数量 $N_a \in \{1,3,5,7,9\}$、Tool-use的二元决策 $N_T \in \{0,1\}$），使优化过程可操作、可复现。

### 4. 即插即用的优化器兼容性

MASS框架与不同提示优化器（如MIPRO、CoT、Few-shot等）组合均能实现性能提升（Table 9），展示了其作为元优化框架的灵活性。同时，1PO和2TO阶段内的优化可完全并行化，而ADAS和AFlow是迭代式算法，这使得MASS在实际部署中具有更高的计算效率。

## 整体框架

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/002_Figure_1.jpg]]
*Figure 1: Proposed Multi-Agent System Search (MASS) framework discovers effective multiagent system designs (with both optimized topology and optimized prompts, right) via interleaved prompt optimization and topology optimization in a customizable multi-agent design space (key components illustrated on the left)*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/004_Figure_3.jpg]]
*Figure 3: Illustration of the MASS framework with its search space and the optimization. The search space combines both prompts (Instruction, Demo) and configurable agentic building blocks (Aggregate, Reflect, Debate, Summarize, and Tool-use). [1PO: Block-level Prompt Optimization]: we conduct block-level prompt optimization for each agentic module individually (denoted by \</>); [2TO: Workflow Topology Optimization]: conditioned on the best prompts found in Stage 1 on each agent block, MASS samples valid configurations from an influence-weighted design space while fusing the prompts of each building block from Stage 1; [3PO: Workflow-level Prompt Optimization]: conditioned on the best workflow found,...*

MASS（Multi-Agent System Search）是一个多阶段自动化多智能体系统设计框架，其核心在于将**提示优化**与**拓扑搜索**进行交错式协同优化，以解决手工设计MAS时面临的组合爆炸问题。图1展示了该框架的整体流程。

### 设计空间定义

MASS首先定义了一个可定制的多智能体设计空间，该空间包含两个层次的搜索维度：

- **块级设计**：每个智能体模块的提示（指令与示例）可独立优化。
- **工作流级编排**：智能体模块之间的连接拓扑可配置，包含五种基础构建块：**Aggregate**（并行聚合，参数化为智能体数量 $N_a$）、**Reflect**（自我反思）、**Debate**（多智能体辩论）、**Summarize**（摘要）以及**Tool-use**（工具调用，二元决策 $N_T \in \{0, 1\}$）。表3详细列出了各拓扑模块的搜索维度和最小构建块定义。

### 三阶段交错优化流程

MASS的优化流程遵循“从局部到全局、从提示到拓扑”的渐进策略，分为三个顺序阶段（如图3所示）：

**阶段1：块级提示优化（1PO）**
首先对初始预测器进行单智能体提示优化作为预热，随后对每个拓扑模块（如Predictor、Reflector、Debator等）以其最小智能体配置独立优化指令和示例提示，得到各模块的局部最优提示。

**阶段2：工作流拓扑优化（2TO）**
基于阶段1的优化结果，计算各拓扑模块的**增量影响力** $I_{a_i} = \mathcal{E}(a_i^*) / \mathcal{E}(a_0^*)$，即该模块相对于初始智能体的性能增益比。随后通过Softmax概率 $p_a = \mathrm{Softmax}(I_a, t)$ 对搜索空间进行剪枝——仅保留影响力显著的模块维度，排除无效或有害的拓扑组合。在剪枝后的空间内，通过拒绝采样随机生成多个工作流候选，按规则构建完整工作流并评估，选择验证性能最优的拓扑配置 $\mathcal{W}_c^*$。

**阶段3：工作流级全局提示优化（3PO）**
在阶段2选出的最佳拓扑 $\mathcal{W}_c^*$ 上，对所有智能体进行联合提示微调，以适应多智能体协作场景下的交互动态，进一步提升整体系统性能。

### 关键设计决策

- **剪枝机制的必要性**：图4的实验证据表明，并非所有拓扑都对MAS有正面影响——在HotpotQA上仅Debate拓扑带来约3%的提升，其他拓扑（如Reflect）反而可能导致性能退化。基于增量影响力的剪枝有效降低了拓扑搜索的复杂度。
- **阶段顺序的不可替代性**：消融实验（图5右）显示，移除搜索空间剪枝或跳过前期提示优化（1PO）会显著降低拓扑优化（2TO）的效果，验证了三阶段递进设计的必要性。
- **并行化能力**：阶段1和阶段2内部的优化过程可完全并行化，这是MASS相对于ADAS和AFlow等迭代式自动化设计方法的重要效率优势。

## 核心模块与公式推导

MASS框架将多智能体系统（MAS）的自动化设计分解为三个交错执行的优化阶段，其核心在于通过**影响力剪枝**降低搜索空间复杂度，并实现提示与拓扑的协同优化。

### 工作流拓扑优化目标

MASS将拓扑搜索形式化为一个优化问题：在预定义的搜索空间 $\mathcal{A}$ 中寻找最优工作流配置 $a$，使期望性能最大化：

$$\mathcal{W}^{*}(a) = \underset{a \sim \mathcal{A}}{\arg \max} \mathbb{E}_{(x,y) \sim \mathcal{D}} [f(\mathcal{W}(a(x)), y)]$$

其中 $(x, y)$ 为数据集 $\mathcal{D}$ 中的输入-输出对，$f$ 为性能评估函数，$\mathcal{W}(a(x))$ 表示按配置 $a$ 构建的工作流对输入 $x$ 的输出。

### 增量影响力与搜索空间剪枝

搜索空间剪枝是MASS高效搜索的关键机制。对于每个拓扑搜索维度 $a_i$（如Aggregate、Debate、Reflect等），定义其**增量影响力** $I_{a_i}$：

$$I_{a_i} = \mathcal{E}(a_i^{*}) / \mathcal{E}(a_0^{*})$$

其中 $\mathcal{E}(a_i^{*})$ 为经过块级提示优化后该拓扑模块的验证性能，$\mathcal{E}(a_0^{*})$ 为初始单智能体的验证性能。该比值量化了集成该搜索维度相对于基础智能体的性能增益。

基于增量影响力，通过Softmax函数计算各维度的**选择概率**：

$$p_a = \mathrm{Softmax}(I_a, t)$$

其中温度参数 $t$ 控制概率分布的锐度（实验中设为 $t = 0.05$）。在拓扑搜索阶段，对每个维度 $a_i$ 采样均匀分布 $u \sim \text{Uniform}(0,1)$，若 $u > p_{a_i}$ 则将该维度从搜索空间中剔除。这一机制有效排除了Figure 4所揭示的无效或有害拓扑（如Reflect在部分任务上导致性能退化），将搜索集中在有潜力的模块上。

### 工具使用决策

对于代码类任务，MASS引入二元决策变量 $N_T \in \{0, 1\}$，决定是否将工具使用（如代码执行器Executor）插入到预测器中，构成任务特定的拓扑扩展。

### 三阶段优化成本

MASS各阶段的计算成本具有不同的缩放特性：

- **块级提示优化（1PO）成本**：$C(\mathrm{1PO}) = \sum_{j}^{J} \mathcal{N}(a_{j}) \times M \times K$，与拓扑块数量 $J$、候选提示数 $M$ 和评估轮次 $K$ 成正比。
- **工作流拓扑优化（2TO）成本**：$C(2\mathrm{TO}) = \sum_{n}^{N} \mathcal{N}(\mathcal{W}_{n})$，为 $N$ 个拓扑候选的智能体总数之和。
- **工作流级提示优化（3PO）成本**：$C(3\mathrm{PO}) = N(\mathscr{W}^{*}) \times M \times K$，仅对最佳工作流 $\mathscr{W}^{*}$ 中的智能体进行联合优化，成本与智能体数量成线性关系。

值得注意的是，1PO和2TO阶段内的优化可完全并行化，而ADAS和AFlow等基线方法是迭代式的，这赋予了MASS在实践中的效率优势。

## 实验与分析

### 核心瓶颈验证：提示优化 vs. 拓扑扩展

MASS 的设计动机源于一个关键观察：在多智能体系统（MAS）中，**提升单个智能体的提示质量，往往比单纯增加智能体数量或改变拓扑结构更具 token 效率**。Figure 2 在 MATH 数据集上对此进行了量化验证：经过提示优化的智能体（prompt-optimized agents）在消耗相同总 token 量的情况下，准确率显著高于通过自一致性（Self-Consistency, SC）、自反思（Self-Refine）或多智能体辩论（Multi-Agent Debate）扩展的基线。这一发现直接支撑了 MASS 将提示优化置于优先地位的设计决策——先“磨刀”再“砍柴”，而非盲目堆砌智能体。


![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/003_Figure_2.jpg]]
*Figure 2: Accuracy vs. total token counts for prompt-optimized agents per question on MATH by Gemini 1.5 Pro compared to scaling agents with self-consistency (SC), self-refine (reflect), and multi-agent debate (debate) only. The error bar indicates 1 standard deviation. We show that by utilizing more compute, better accuracy can be obtained via more effective prompting*

### 主实验结果

Table 1 汇总了 MASS 在 Gemini 1.5 Pro 和 Gemini 1.5 Flash 两个模型规模上、覆盖推理、多跳问答和代码生成三类共 8 个任务的全面评估结果。


![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/007_Table_1.jpg]]
*Table 1: Results on the evaluation set with Gemini 1.5 Pro and Gemini 1.5 Flash. We report the mean and standard deviation for all results with 3 runs of evaluations. We report the accuracy (%) for MATH and the test-output-prediction subtask of LiveCodeBench (LCB), F1 score for DROP, HotpotQA, MuSiQue, and 2WikiMQA, and pass@1 for MBPP and HumanEval. We note that the meta-prompt of AFlow* only works properly with Claude 3.5 Sonnet. Therefore, we reproduce AFlow with Gemini 1.5 Pro as the executor and Claude 3.5 Sonnet as the optimizer, where * indicates the results are only for reference. The inference cost is controlled comparably as shown in Table 7*


![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/018_Table_7.jpg]]
*Table 7: The training and inference cost for running MASS and baselines, where we show the training cost and the actual run-time of MASS is comparable to the training cost of auto-agent baselines. We note that the performance of self-consistency, self-refine, and multi-agent debate is already saturated, and further scaling the inference cost of these baselines only brings marginal gains, whereas the MASS-found MAS outperforms the baseline substantially at a comparable inference token cost*

**Gemini 1.5 Pro 上的表现**：MASS 取得 **78.79% 的平均准确率**，在所有任务上均显著超越各基线方法。具体而言：
- **推理任务**：MATH 上达到 84.67%（CoT 为 71.67%，提升 +13.00 个百分点）；DROP 上 F1 达 90.52%（CoT 为 70.59%，提升 +19.93 个百分点）。
- **多跳问答任务**：HotpotQA（F1 69.91% vs. CoT 57.43%）、MuSiQue（F1 51.40% vs. 37.81%）、2WikiMQA（F1 73.34% vs. 63.39%）均有两位数百分点的提升。
- **代码任务**：MBPP pass@1 达 86.50%（CoT 68.33%）、HumanEval pass@1 达 91.67%（CoT 86.67%）、LiveCodeBench 准确率 82.33%（CoT 66.33%）。

与自动化设计基线对比，MASS 同样优势明显：ADAS 平均 69.72%，AFlow* 平均 73.49%（*标注因 AFlow 的元提示仅适配 Claude 3.5 Sonnet，结果供参考）。值得注意的是，所有方法均控制了每次查询的推理成本可比，且最大智能体数量设为 10，排除了“堆算力换性能”的解释。

**Gemini 1.5 Flash 上的迁移表现**：MASS 在 Flash 模型上平均 74.30%，同样领先所有基线（CoT 为 60.98%，ADAS 为 66.10%），表明 MASS 发现的提示和拓扑在模型规模缩放时仍保持有效性。

### 拓扑有效性的选择性

并非所有拓扑结构都对 MAS 性能有正面贡献。Figure 4 在 HotpotQA 和 LiveCodeBench 上对比了经过 APO 优化的不同拓扑模块的性能：

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/006_Figure_4.jpg]]
*Figure 4: The performance of different topologies with Gemini 1.5 Pro compared to the base agent with each topology being optimized with APO, where Sum. (Summarize) and Exe. (Executor) are task-specific topologies as illustrated in Fig. 3. We observe that not all topologies have a positive influence on the MAS design*

- 在 HotpotQA 上，仅 **Debate 拓扑** 带来约 3% 的增益，而其他拓扑（如 Reflect）甚至导致性能退化。
- 在 LiveCodeBench 的 test-output-prediction 子任务上，**Executor（含工具使用的执行器）** 和 **Self-Consistency** 表现突出，而 Reflect 同样表现不佳。

这一发现直接支撑了 MASS 的**基于影响力的搜索空间剪枝**策略：通过计算各拓扑模块的增量影响力 $I_{a_i} = \mathcal{E}(a_i^*) / \mathcal{E}(a_0^*)$，将无效或有害的模块从搜索空间中剔除，从而显著降低拓扑搜索的组合复杂度。

### 三阶段优化的累积增益

Figure 5（左）的消融实验清晰地展示了 MASS 三个优化阶段的**累积贡献**：

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/010_Figure_5.jpg]]
*Figure 5: Left: average performance per optimization stage of MASS over 8 evaluation tasks on Gemini 1.5 Pro. We compare MASS with a single agent (CoT) starting point as the reference and an APO baseline that optimizes over the single agent by MIPROv2 (Opsahl-Ong et al., 2024). Refer to App. §D for the detailed ablation per task. Right: a comparative ablation study on topology optimization (2TO) without pruning and without the former stage of prompt optimization (1PO) evaluated on HotpotQA. Figure 6: The optimization trajectories of MASS compared to agent design baselines per validation round on DROP. We note that, as a distinct advantage of MASS, the optimization within stages (1) & (2) of MASS can...*

1. **块级提示优化（1PO）**：相比单智能体 APO 基线，平均提升约 **6%**。该阶段独立优化每个拓扑模块的指令和示例提示，为后续的拓扑搜索提供了高质量的“积木块”。
2. **工作流拓扑优化（2TO）**：在 1PO 基础上再提升约 **3%**。该阶段在剪枝后的搜索空间中组合有潜力的拓扑模块，发现更优的智能体协作模式。
3. **工作流级全局提示优化（3PO）**：进一步带来约 **2%** 的增益。该阶段在最佳拓扑上对所有智能体进行联合提示微调，使各智能体的提示适配多智能体协作的上下文。

三个阶段合计带来约 11% 的性能提升，且每个阶段都提供了不可替代的增益。Figure 5（右）进一步揭示了各阶段之间的**依赖关系**：若移除搜索空间剪枝和前期提示优化（1PO），直接进行拓扑优化（2TO）的效果会显著下降，验证了 MASS “先局部优化、再全局搜索、最后联合微调”这一交错策略的必要性。

### 优化轨迹分析

Figure 6 在 DROP 验证集上对比了 MASS 与自动化基线（ADAS、AFlow）的优化轨迹。MASS 呈现出明显的**阶梯式上升**特征：在第 1 轮 1PO 阶段发现 Aggregate 拓扑和更优提示后，性能从约 78% 跃升至约 84%；第 15 轮进入 2TO 阶段后进一步升至约 85%；第 25 轮 3PO 阶段达到收敛约 86%。相比之下，ADAS 和 AFlow 的优化曲线上升缓慢且存在较大波动，体现了 MASS 交错优化策略在样本效率上的优势。

Figure 7 以 MATH 任务为例展示了 MASS 的具体优化路径：
- **阶段 1**：从零样本 CoT 智能体（62%）出发，块级优化发现 **Debate 拓扑** 表现最佳（79%），并优化了辩手的提示（如“作为数学专家审查学生解答”）。
- **阶段 2**：拓扑搜索发现，**聚合更多并行智能体（Aggregate）** 的效果反而优于多智能体辩论，将性能推至 83%。
- **阶段 3**：全局提示优化为聚合拓扑中的预测器找到了最佳提示，最终收敛。

这一轨迹揭示了一个反直觉的发现：尽管 Debate 在单模块评估中表现优异，但在完整工作流中，Aggregate 拓扑的组合效果更佳——这恰好说明了将拓扑搜索与提示优化交错进行的必要性。

### 跨模型迁移与局限性

MASS 在 Claude 3.5 Sonnet（Table 4）和 Mistral-Nemo-12B（Table 5）上的迁移实验表明，其发现的提示和拓扑在跨模型时仍能保持一致的性能优势，但**并非零成本迁移**：原有拓扑在某些情况下可能导致性能退化，需要重新运行优化流程。此外，MASS 的搜索空间目前仍限于预定义的拓扑模块序列，尚未探索更灵活的图结构（如树形拓扑、动态路由），这是未来可扩展的方向。


![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/015_Table_4.jpg]]
*Table 4: Results on the evaluation set with Claude 3.5 Sonnet. We keep the same experimental setup as Table 1. Since Claude 3.5 Sonnet does not support the same context window as Gemini, we report the standard HotpotQA instead of the LongBench. As we transfer the prompt template for each agent from Gemini to Claude, it is noticeable that the basic topology on some tasks may result in severe degradation of performance, and MASS successfully recovers the performance and brings significant improvements over the initial agent*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/016_Table_5.jpg]]
*Table 5: Results on the evaluation set with the open-source model, Mistral-Nemo-12B. We keep the same experimental setup as Table 4 and evaluate a subset of representative coding tasks to save resources. MASS demonstrate consistent improvements over the baselines on Mistral Nemo*

### 成本分析

Table 7 显示，MASS 的训练成本约 **$5.09**（24M 输入 token、11M 输出 token），与 ADAS、AFlow 等自动化基线相当，但推理成本（$0.0014/查询）与 CoT 等简单基线处于同一量级，且性能大幅领先。此外，MASS 的阶段 1 和阶段 2 内部可完全并行化，实际运行时间可进一步压缩。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/012_Table_2.jpg]]
*Table 2: The specification of evaluation tasks: dataset split, topology search space, and the MASSoptimized MAS (on Gemini 1.5 Pro)*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/014_Table_3.jpg]]
*Table 3: The search dimension for each topology. The minimum topology defines the building block that MASS Stage (1) optimized. We refer the definition of search space to Sec.2.2*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_I05H9RUzHB/figures/017_Table_6.jpg]]
*Table 6: The detailed ablation results per optimization stage of MASS. Practical gains can be obtained by further conducting workflow-level prompt optimization (3PO) on the best-found topology*



## 方法谱系与知识库定位

### 核心瓶颈与设计动因

多智能体系统（MAS）的自动化设计面临一个根本性的组合爆炸问题：提示（prompt）的敏感性与拓扑（topology）的复杂性相互交织。手工设计的MAS（如Self-Consistency、Multi-Agent Debate）通常固定拓扑结构，仅通过增加智能体数量来扩展性能，而忽略了提示优化与拓扑选择之间的协同效应。已有的自动化方法——如**ADAS**（基于LLM元智能体的迭代式智能体设计）和**AFlow**（基于蒙特卡洛树搜索的预定义算子拓扑优化）——仅单独优化提示或拓扑，未能联合搜索，导致性能次优。

MASS的核心洞察在于：有效的MAS设计必须将提示优化与拓扑搜索协同进行。具体而言，先优化局部智能体提示以释放单个模块的潜力，再根据验证性能的增量影响力筛选有潜力的拓扑结构，最后进行全局微调以提升多智能体协作效率。这一“局部→全局、提示→拓扑”的交错优化策略，是MASS区别于所有现有方法的关键因果机制。

### 在MAS自动化设计谱系中的位置

从方法谱系来看，MAS自动化设计可分为三条主线：

1. **固定拓扑 + 手工提示**：如**Chain-of-Thought (CoT)**（Kojima et al., 2022）、**Self-Consistency (SC)**（Wang et al., 2023）、**Self-Refine**和**Multi-Agent Debate**。这些方法依赖人工编写的固定提示和预定义的拓扑结构，性能受限于设计者的先验知识。

2. **自动提示优化 + 固定拓扑**：如**ADAS**，通过LLM元智能体基于历史评估迭代生成新智能体，但拓扑结构在优化过程中保持不变。其搜索空间局限于提示层面，无法探索不同拓扑组合带来的协作增益。

3. **自动拓扑搜索 + 手工提示**：如**AFlow**，在预定义算子集合上使用蒙特卡洛树搜索优化工作流拓扑，但提示保持固定。其瓶颈在于，即使找到了好的拓扑，次优的提示仍会限制每个模块的性能上限。

**MASS属于第四条主线——联合提示与拓扑的自动化协同优化**。它通过三阶段交错优化（1PO→2TO→3PO）将提示优化与拓扑搜索解耦为可并行化的子问题，同时通过基于增量影响力的剪枝机制压缩搜索空间，从而高效找到高性能MAS配置。这一设计使其在搜索效率（阶段内可完全并行化）和最终性能（8任务平均78.79%，显著优于ADAS的69.72%和AFlow*的73.10%）上均优于迭代式基线。

### 关键设计选择与消融证据

MASS的三个优化阶段各自贡献累积增益（Figure 5左）：

- **块级提示优化（1PO）**：相比单智能体APO基线平均提升约6%。这一阶段的核心作用是“预热”——为每个拓扑模块（Predictor、Reflector、Debator等）独立优化指令和示例，释放单个模块的潜力。证据表明，跳过此阶段直接进行拓扑优化会导致2TO效果显著下降（Figure 5右）。
- **工作流拓扑优化（2TO）**：在1PO基础上再提升约3%。关键设计是基于增量影响力 $I_{a_i} = \mathcal{E}(a_i^*) / \mathcal{E}(a_0^*)$ 的搜索空间剪枝——并非所有拓扑都对MAS有正面影响（Figure 4），仅少数拓扑（如Debate、Summarize）能提升性能，而Reflect等模块甚至可能导致退化。通过Softmax概率 $p_a = \mathrm{Softmax}(I_a, t)$ 剪枝无效模块，2TO将搜索聚焦于有潜力的拓扑组合。
- **工作流级全局提示优化（3PO）**：进一步带来约2%的增益。此阶段在最佳拓扑上对所有智能体进行联合提示微调，适应多智能体协作中的交互动态，使各模块的提示相互协调而非独立优化。

### 适用边界与局限

尽管MASS在8个任务上展现了显著的性能优势，其设计仍存在明确的适用边界：

1. **拓扑表达能力的上限**：当前搜索空间限于预定义的拓扑模块序列（Aggregate、Reflect、Debate、Summarize、Tool-use），未探索更灵活的图结构、树形拓扑或动态路由。这意味着MASS无法发现超出其设计空间的新型协作模式。

2. **跨模型迁移的脆弱性**：MASS优化的拓扑和提示是针对特定模型（如Gemini 1.5 Pro）定制的。当迁移到其他模型时（如Claude 3.5 Sonnet或Mistral-Nemo-12B），原有拓扑可能导致性能退化，需要重新运行完整的优化流程。这限制了MASS在模型快速迭代场景中的即插即用性。

3. **计算成本与样本效率**：MASS的训练成本约$5.09（附录D.3），虽可通过并行化改善，但对资源受限场景仍不低。成本主要由三部分组成：$C(\mathrm{1PO}) = \sum_{j}^{J} \mathcal{N}(a_{j}) \times M \times K$（与拓扑块数量J、候选提示数M和评估轮次K成正比）、$C(2\mathrm{TO}) = \sum_{n}^{N} \mathcal{N}(\mathcal{W}_{n})$（与N个拓扑候选的智能体总数之和成正比）、$C(3\mathrm{PO}) = N(\mathscr{W}^{*}) \times M \times K$（与最佳工作流中的智能体数量成线性关系）。提示优化器依赖模型自举的示例和候选，其样本效率可进一步提高。

4. **搜索算法的局限**：当前2TO采用随机采样+拒绝采样的方式搜索拓扑，未使用贝叶斯优化或进化策略等更高效的搜索算法，可能在复杂搜索空间中错过更优解。

### 开放问题

1. **拓扑空间扩展**：纳入图结构、树形分解、动态路由等更丰富的拓扑类型，是否能突破当前序列化拓扑的性能上限？这需要重新设计搜索空间和剪枝策略。

2. **通信冗余剪枝**：在多智能体协作中，并非所有智能体间的通信都有价值。剪枝冗余通信或合并功能相似的智能体，能否在保持精度的同时显著降低推理成本？

3. **搜索效率提升**：采用贝叶斯优化或基于梯度的可微分搜索（如可微分NAS的变体）替代随机采样，能否提高拓扑搜索的样本效率？这需要将离散的拓扑选择转化为可优化的连续表示。

4. **反馈信号增强**：将错误日志、推理轨迹等文本反馈集成到提示优化器中，是否能提供比标量性能指标更丰富的优化信号，从而加速收敛？

5. **跨模型泛化**：是否存在一种模型无关的拓扑表示，使得在一个模型上优化的MAS可以直接迁移到其他模型而不损失性能？这涉及提示与模型能力的解耦问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Multi_Agent_Design_Optimizing_Agents_with_Better_Prompts_and_Topologies.pdf]]
