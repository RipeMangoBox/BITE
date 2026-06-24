---
title: "AutoLibra: Agent Metric Induction from Open-Ended Human Feedback"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AutoLibra_Agent_Metric_Induction_from_Open_Ended_Human_Feedback.pdf
aliases:
- AutoLibra
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "AutoLibra induces agent evaluation metrics by grounding open-ended feedback to trajectory behaviors and clustering similar behavior aspects."
primary_logic: "It converts feedback into behavior-feedback-sign triples, clusters them into metric definitions, evaluates trajectories with LLM-as-judge, and optimizes metric sets by coverage and redundancy."
claims:
- "The method automates fine-grained metric discovery instead of relying on expert-designed task success metrics."
- "Coverage and redundancy serve as meta-evaluation signals for selecting metric sets."
- "The note reports high human agreement for feedback grounding, judging, and meta-evaluation steps."
---

# AutoLibra: Agent Metric Induction from Open-Ended Human Feedback

> [!tip] 核心洞察
> 通过模拟社会科学主题分析中的编码-主题归纳步骤，将人类反馈中的每个方面（aspect）锚定到智能体轨迹中的具体行为，再将相似行为聚类为指标（metric），并利用覆盖率和冗余度两个元指标进行自验证和优化，可以自动生成比专家设计更具体、更全面的评估指标。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AutoLibra：从开放式人类反馈中归纳智能体评估指标 |
| 英文题名 | AutoLibra: Agent Metric Induction from Open-Ended Human Feedback |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=4BjGVZ7Bxn); [GitHub](https://github.com/ProKil/autolibra); [Project](https://huggingface.co/datasets/ProKil/autolibra) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | AutoLibra |
| Dataset | Sotopia, WebArena, WebVoyager, Baba-Is-AI (GPT-4o) |

> [!tip] 效果简介
> - Sotopia 上，覆盖率 (Coverage) 为 60%，对比 N/A，变化 N/A。
> - WebArena 上，覆盖率 (Coverage) 为 88%，对比 N/A，变化 N/A。
> - WebVoyager 上，覆盖率 (Coverage) 为 88%，对比 N/A，变化 N/A。

## 概述

AutoLibra 是一种从开放式人类反馈中自动归纳可解释、细粒度评估指标的方法，用于评估和优化 AI 智能体。该方法受社会科学主题分析（thematic analysis）的编码-主题归纳步骤启发，通过两个核心步骤——反馈锚定（Feedback Grounding）和行为聚类（Behavior Clustering）——将人类反馈转化为结构化的评估指标。AutoLibra 在多个智能体领域（协作、社交、网页、文本游戏）中展现出高覆盖率和低冗余度，并能通过迭代优化过程显著提升前沿 LLM 在复杂任务中的性能。

## 背景与动机

现有智能体评估主要依赖任务成功率等粗粒度指标，这些指标需要专家手动设计，无法奖励中间涌现行为，也难以捕捉用户关心的细粒度行为维度。例如，在协作、社交、网页导航和文本游戏等多样化场景中，专家设计的评估维度往往遗漏了用户实际关注的关键行为方面。AutoLibra 的核心动机是：能否像人类从开放式指令和反馈中学习技能一样，让评估系统自动从开放式人类反馈中归纳出细粒度、可解释的评估指标？

## 核心创新

AutoLibra 的核心创新在于：

1. **自动指标归纳**：通过模拟社会科学主题分析中的编码-主题归纳步骤，将人类反馈中的每个方面（aspect）锚定到智能体轨迹中的具体行为，再将相似行为聚类为指标（metric）。

2. **自验证机制**：利用覆盖率和冗余度两个元指标进行自验证和优化，无需人工干预即可搜索最优指标集。

3. **迭代发现能力**：可随智能体优化过程迭代地发现新指标，类似于软件开发中持续维护单元测试以防止新功能干扰现有功能。

4. **细粒度可解释性**：归纳出的指标包含正面和负面行为示例，比专家设计的指标更具体，并能发现专家遗漏的指标。

## 整体框架

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_4BjGVZ7Bxn_AutoLibra_Age/figures/001_Figure_1.jpg]]
*Figure 1: AutoLibra induces agent evaluation metrics from human feedback, and uses these metrics to evaluate agents, which can be meta-evaluated via evaluating the coverage on unseen human feedback. Here we show real examples of agent trajectories, human feedback, aspects, induced metrics, evaluation results on WebVoyager (He et al., 2024).*

AutoLibra 的整体流程如 Figure 1 所示，包含以下步骤：

1. **收集人类反馈**：从最终用户（如 CoGym 中的用户评论）或专家（观察智能体轨迹后提供反馈）收集开放式反馈。每个轨迹仅收集一条反馈，注释过程快速（每条轨迹不到 5 分钟）。

2. **反馈锚定**：将人类反馈中的每个方面锚定到智能体轨迹中的具体行为，输出为 (behavior, feedback, sign) 三元组。

3. **行为聚类**：将锚定后的方面聚类为 N 个指标，每个指标包含定义、正面行为示例和负面行为示例。

4. **LLM-as-a-Judge 评估**：使用归纳出的指标对智能体轨迹进行评分，输出 {+1, -1, N/A}。

5. **元评估**：将 LLM-as-a-Judge 检测到的特质与人类反馈中的方面进行匹配，计算覆盖率和冗余度。

6. **指标优化**：通过最大化覆盖率、最小化冗余度来搜索最优指标集。

Figure 1 展示了 AutoLibra 的整体流程：从人类反馈到指标归纳，再到评估和元评估。

Figure 2 展示了指标优化过程：通过最大化覆盖率、最小化冗余度来优化归纳过程。

## 核心模块与公式推导

### 5.1 反馈锚定 (Feedback Grounding)

使用 GPT-4o 将人类反馈分解为要点，并为每个要点找到轨迹中对应的行为部分。输出定义为三元组 (behavior, feedback, sign)，其中 sign 表示该行为是正面还是负面。

### 5.2 行为聚类 (Behavior Clustering)

使用 o3-mini high 将方面聚类为 N 个指标。聚类指令要求：分组粒度应最小化，仅将非常相似的行为分组在一起，但不限于特定网站或特定角色。

### 5.3 LLM-as-a-Judge 评估

使用 o3-mini medium 对智能体轨迹进行评分，输出 {+1, -1, N/A}。

### 5.4 元评估 (Meta-Evaluation)

使用 GPT-4o 将 LLM-as-a-Judge 检测到的特质与人类反馈中的方面进行匹配。核心公式如下：

**覆盖率 (Coverage)**：
$$\text{Coverage} = \frac{\text{有匹配特质的方面数}}{\text{总方面数}}$$

衡量归纳出的指标覆盖人类反馈中行为方面的比例。

**冗余度 (Redundancy)**：
$$\text{Redundancy} = \frac{\text{未与任何方面匹配的特质数}}{\text{总特质数}}$$

衡量 LLM-as-a-Judge 检测到的特质中未被人类反馈提及的比例。

### 5.5 指标优化 (Metric Optimization)

生成 N 从 4 到 13 的 20 个不同指标集，选择覆盖率不低于最高覆盖率减 1% 且冗余度最低的指标集。迭代调整 N 的范围（所选指标数 ±2），直至收敛（通常在 3 次迭代内）。

### 5.6 迭代指标归纳 (Iterative Metric Induction)

在智能体优化过程中，修改行为聚类步骤：向 LLM 提供现有指标和定义，要求不改变现有指标的定义，仅向现有指标添加新行为，必要时添加新指标。

## 实验与分析

### 6.1 人类验证一致率

Table 1 展示了 AutoLibra 各步骤与人类判断的一致率。对于每个步骤和每个任务，随机采样 40 个实例进行人工验证。各步骤的平均一致率均显著高于 0.85。

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_4BjGVZ7Bxn_AutoLibra_Age/figures/005_Table_1.jpg]]
*Table 1: The ratio of instances marked as fully correct in human validation. For each step and each task, we randomly sample 40 instances to reach a relatively small confidence interval of 0.04 and ask human annotators to label them as completely correct or not. Although the agreement scores vary across tasks and steps, the average agreement for each step and dataset is above 0.85 significantly.*

| 步骤 | 平均一致率 |
|------|-----------|
| 反馈锚定 | 0.95 |
| LLM-as-a-Judge | 0.92 |
| 元评估 | 0.90 |

### 6.2 覆盖率与冗余度

Figure 3 展示了四个数据集上不同指标数量下的覆盖率和冗余度。主要结果如下：

- **Sotopia**：最佳覆盖率为 60%，是四个数据集中最低的，可能由于任务多样性较高。
- **WebArena** 和 **WebVoyager**：覆盖率最高，均为 88%。
- **CoGym**：覆盖率介于中间水平。

消融实验表明，从指标中移除正面和负面行为示例会导致 CoGym 上的覆盖率下降高达 30%，证明了具体行为示例的关键性。

### 6.3 与专家设计指标的对比

Table 2 比较了 AutoLibra 归纳的指标与专家设计的评估维度和失败类别：

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_4BjGVZ7Bxn_AutoLibra_Age/figures/006_Table_2.jpg]]
*Table 2: AutoLibra-induced metrics and expert-proposed evaluation dimensions and failure categories. (Percentage %) denotes failure frequency or score from AutoLibra or the original papers.*

- **CoGym**：AutoLibra 归纳出 9 个指标，对应 5 个专家失败类别，失败率大致匹配（如 Responsiveness and Efficiency 75%，Communication Clarity 8%）。
- **Sotopia**：AutoLibra 恢复了 Goal Completion 和 Believability 的 3 个子维度，并额外归纳出 4 个被专家忽略的指标（如 Conversational Naturalness 5%，Personality Consistency 2%）。
- **WebVoyager**：AutoLibra 发现了 Access Barrier Handling、Error Recovery 等指标，以及被专家遗漏的 Query and Search Strategy Efficiency（7%）和 Final Output Quality（18%）。

### 6.4 智能体优化实验

#### Baba-Is-AI 实验

Figure 4 展示了在 Baba-Is-AI 游戏中，AutoLibra 如何迭代地归纳指标并改进智能体提示。Table 3 显示了具体结果：

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_4BjGVZ7Bxn_AutoLibra_Age/figures/014_Table_3.jpg]]
*Table 3: Baba-is-ai Scores and Average Environment Steps*

| 模型 | Iteration 0 | Iteration 1 | Iteration 2 | Iteration 3 | 基线 |
|------|-------------|-------------|-------------|-------------|------|
| GPT-4o 成功率 | 30% | 40% | 43% | 55% | 33% |
| GPT-4o (仅保留任务) | 33% | 40% | 44% | 53% | 33% |
| Claude 3.5 Sonnet 成功率 | 35% | 40% | 45% | 55% | 37% |
| Claude 3.5 Sonnet (仅保留任务) | 38% | 42% | 47% | 58% | 33% |
| 平均环境步数 | 79 | 63 | 60 | 51 | - |

尽管未针对成功率进行优化，智能体的成功率持续提升，直到 Stage 3 开始出现过度思考。Table 4 展示了各迭代的指标性能：

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_4BjGVZ7Bxn_AutoLibra_Age/figures/015_Table_4.jpg]]
*Table 4: Metric Performance for baba-is-ai AutoLibra Iterations 0–3, Across Full (40) Environment Tasks*

| 指标 | Iteration 0 | Iteration 1 | Iteration 2 | Iteration 3 |
|------|-------------|-------------|-------------|-------------|
| Win Condition Recognition | 35.0% | 55.0% | 87.5% | 87.5% |
| Rule Modification | 0.0% | 10.0% | 37.5% | 61.9% |
| Coverage | 65.0% | 83.0% | 85.0% | 92.0% |

#### MiniHack 实验

Table 5 展示了 MiniHack 实验中的得分和平均环境步数：

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_4BjGVZ7Bxn_AutoLibra_Age/figures/016_Table_5.jpg]]

| 指标 | Turn 0 | Turn 1 | Turn 2 | 基线 |
|------|--------|--------|--------|------|
| MiniHack Score | 0% | 12.5% | 25% | 10% |
| 平均环境步数 | 85 | 91 | 88 | 1 |

Table 6 展示了 MiniHack 各迭代的指标性能：

| 指标 | Iteration 0 | Iteration 1 | Iteration 2 |
|------|-------------|-------------|-------------|
| Target Navigation Effectiveness | 16.67% | 8.33% | 41.67% |
| Efficient Exploration and Map Memory Utilization | 16.67% | 0.00% | 25.00% |
| Spatial Awareness and Interpretation | 16.67% | 16.67% | 58.33% |
| Combat Engagement and Survival | 8.33% | 8.33% | 25.00% |
| Coverage | 82.89% | 81.82% | 87.84% |
| Redundancy | 61.11% | 65.63% | 71.30% |

在 Iteration 1 中，代码更改导致性能下降 8.3%，表明过于简化的策略和示例可能混淆智能体。Iteration 2 中，目标意识和目标到达效率显著提升，智能体成功完成了大多数 MazeWalk 和 Corridor Fight 任务。

### 6.5 公平性说明

- 人类反馈来自两类群体：最终用户（CoGym）和专家（其他环境，由五位作者提供）。
- 对于每个轨迹，仅收集一条反馈，以避免过度负担注释者。
- 注释过程快速：人类注释者每条轨迹花费不到 5 分钟。
- 对于 Sotopia、WebArena 和 WebVoyager，每个数据集注释了 100 条基于 GPT-4 的智能体轨迹。
- 对于 §5 中的实验，每个数据集每次迭代注释 18 条轨迹。
- 在 §4 中，随机保留 20% 的轨迹用于验证。

## 方法谱系与知识库定位

AutoLibra 在智能体评估方法谱系中占据独特位置：

1. **与基于任务成功率的评估对比**：传统方法依赖粗粒度的任务成功率或专家手动设计的评估维度，AutoLibra 则从开放式人类反馈中自动归纳细粒度、可解释的指标。

2. **与 LLM-as-a-Judge 对比**：AutoLibra 不仅使用 LLM-as-a-Judge 进行评估，还通过元评估步骤优化归纳的指标，形成完整的评估闭环。

3. **与程序化评估对比**：与 SWE-Bench 等使用人工编写的单元测试作为评估指标的方法不同，AutoLibra 是纯数据驱动的任务无关方法，无需预定义的失败分类。

4. **与奖励模型对比**：与 AgentRewardBench 等构建奖励模型的方法不同，AutoLibra 生成可解释的指标，既可用于评估也可用于智能体微调。

5. **与观测工具对比**：与 Galileo、Vertex AI Gen AI Evaluation Service 等提供用户界面可视化智能体失败模式的工具不同，AutoLibra 自动从反馈中归纳指标，无需人工分析。

**局限性**：
- AutoLibra 的指标归纳过程依赖于 LLM（GPT-4o, o3-mini），其输出可能存在偏差或错误。
- 行为聚类步骤由于需要处理大量方面，难以进行人工验证。
- 在 Sotopia 等任务多样性高的数据集上，覆盖率相对较低（60%）。
- 在 MiniHack 的 Boxoban 和 Quest 任务中，由于环境的高随机性和复杂性，简单的提示和示例改进不足以提升性能。
- 在 Baba-Is-AI 实验中，Stage 3 出现了过度思考现象。

**开放问题**：
- AutoLibra 归纳的指标是否能够直接用于强化学习的奖励函数设计？
- 如何进一步降低冗余度，同时保持高覆盖率？
- AutoLibra 是否能够扩展到更复杂的多模态智能体环境？
- 如何自动生成用于评估归纳指标的程序化评估器，以减少对 LLM-as-a-Judge 的依赖？
- AutoLibra 的迭代优化过程是否可能引入过拟合，如何缓解？

## 原文 PDF

![[paperPDFs/ICLR_2026/AutoLibra_Agent_Metric_Induction_from_Open_Ended_Human_Feedback.pdf]]
