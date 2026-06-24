---
title: "USTBench: Benchmarking and Dissecting Spatiotemporal Reasoning Capabilities of LLMs as Urban Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/USTBench_Benchmarking_and_Dissecting_Spatiotemporal_Reasoning_Capabilities_of_LLMs_as_Urban_Agents.pdf
openreview_forum_id: ETzBStUFJy
aliases:
- USTBench
tags:
- ICLR_2026
- topic/time_series_dynamical_systems
- topic/time_series_dynamical_systems/time_series_forecasting
core_operator: "通过专项增强时空理解的域适应训练（如后训练 Qwen2.5-7B-ST）可以显著提升预测与规划，说明域特异性时空特征学习是驱动下游性能的关键可控因素。"
primary_logic: "通用推理能力的强化并不总能迁移至城市时空推理；专注于增强时空理解的域适应方法对提升城市代理性能更为关键。"
claims:
- "DeepSeek-R1 在拥堵预测结果指标上略逊于 Llama3.3，揭示推理模型在特定时空趋势分析中的弱点。"
- "通过时空理解后训练，Qwen2.5-7B-ST 在预测与规划任务上显著优于原始模型和推理变体。"
- "消融实验中移除反思组件导致 DeepSeek-R1 性能最大降幅，表明反思对下游任务至关关键。"
- "LLM 在长程空间关系（连通性）和长时间模式（周期性、趋势）上的准确率常低于 70%，暴露其结构化数据推理的不足。"
---

# USTBench: Benchmarking and Dissecting Spatiotemporal Reasoning Capabilities of LLMs as Urban Agents

> [!tip] 核心洞察
> 通用推理能力的强化并不总能迁移至城市时空推理；专注于增强时空理解的域适应方法对提升城市代理性能更为关键。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | USTBench：评测与解构大语言模型作为城市智能体的时空推理能力 |
| 英文题名 | USTBench: Benchmarking and Dissecting Spatiotemporal Reasoning Capabilities of LLMs as Urban Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ETzBStUFJy); [GitHub](https://github.com/usail-hkust/USTBench) |
| Topic | #topic/time_series_dynamical_systems #topic/time_series_dynamical_systems/time_series_forecasting |
| Method | USTBench |
| Dataset | Spatiotemporal Understanding (Overall), Spatiotemporal Understanding (Connectivity), Socio-economic Prediction |

> [!tip] 效果简介
> - Spatiotemporal Understanding (Overall) 上，Accuracy 为 o4-mini (0.7924)，对比 GPT-4o (0.7259)，变化 +0.0665。
> - Spatiotemporal Understanding (Connectivity) 上，Accuracy 为 o4-mini (0.7665)，对比 GPT-4o (0.6787)，变化 +0.0878。
> - Socio-economic Prediction 上，MAPE ↓ 为 o4-mini (4.97%)，对比 Classic Method (significantly higher)，变化 ~several-fold improvement (up to 337.31% gain in forecasting accuracy)。

## 概述

城市时空推理要求智能体理解动态演化的空间结构与时间模式，并据此进行预测与决策。当前大语言模型（LLM）作为城市智能体的能力评估尚不系统，尤其缺乏对推理过程的细粒度诊断。**USTBench** 应运而生，首次将城市时空推理显式分解为**时空理解、预测、规划与反思**四个关键过程，并提供 62,466 条结构化 QA 对进行过程级评测。配套的交互式环境 **UAgentEnv** 覆盖九类典型城市任务，支持统一的基准数据采集与下游评估。

核心发现揭示了一个关键瓶颈：**通用推理能力的强化并不总能迁移至城市时空推理**。例如，DeepSeek-R1 在拥堵预测的结果指标上略逊于 Llama3.3（Figure 1），暴露了推理模型在特定时空趋势分析中的弱点。更根本的瓶颈在于，LLM 在长程空间关系（如连通性）和长时间模式（如周期性、趋势）上的准确率常低于 70%（Table 3），表明其对结构化数据的推理能力严重不足。消融实验进一步证实，**反思组件对下游任务至关重要**——移除反思导致 DeepSeek-R1 性能降幅最大（Figure 6）。

然而，因果可控因素同样明确：**通过专项增强时空理解的域适应训练，可以显著提升预测与规划**。Qwen2.5-7B-ST 在后训练后，于预测与规划任务上持续优于原始模型及其推理变体（Figure 4），说明域特异性时空特征学习是驱动下游性能的关键杠杆。这一发现为后续研究指明了方向：与其单纯堆砌通用推理能力，不如聚焦于轻量高效的时空推理范式设计。

## 背景与动机

城市系统是一个由动态时空状态构成的复杂环境，其运行依赖于对交通流、社会经济指标、公共设施布局等多元信息的持续感知与决策。随着大语言模型（LLM）在通用推理任务中展现出强大能力，研究者开始探索将其作为城市智能体的可能性——即让 LLM 理解城市状态、预测未来变化并制定优化决策。然而，这一方向面临一个核心瓶颈：**当前 LLM 在动态城市环境中的长期规划与基于反馈的自适应反思能力严重不足，即使在通用推理模型中该瓶颈依然突出**。

现有的城市 LLM 评测基准（如 STBench、CityBench、CityGPT、UrbanPlanBench）主要关注结果导向的评估，即仅衡量模型最终输出与参考答案的一致性。这种评估方式掩盖了模型在中间推理过程中的深层弱点。以拥堵预测任务为例，**DeepSeek-R1 在结果指标上略逊于 Llama3.3**（Figure 1），这一反直觉的现象揭示：通用推理能力的强化并不总能迁移至城市时空推理场景。更细致的分析表明，LLM 在长程空间关系（如区域连通性）和长时间模式（如周期性、趋势）上的准确率常低于 70%（Table 3），暴露出其对结构化时空数据推理的根本性不足。

上述缺口指向一个关键的科学问题：**专注于增强时空理解的域适应方法，是否比单纯追求通用推理能力的提升更为关键？** 初步证据表明，通过专项后训练增强时空理解能力（如 Qwen2.5-7B-ST），可以在预测与规划任务上显著优于原始模型及其推理变体（Figure 4），说明域特异性时空特征学习是驱动下游性能的可控因素。同时，消融实验显示，移除反思组件会导致 DeepSeek-R1 性能出现最大降幅（Figure 6），进一步证实了反思机制对动态城市任务的必要性。

基于这些观察，本文的动机在于：构建一个能够细粒度解构 LLM 城市时空推理能力的评测框架，不仅衡量最终结果，更深入诊断模型在时空理解、预测、规划和反思四个关键过程中的表现，从而为城市智能体的能力提升提供明确的改进方向。

## 核心创新

USTBench 的核心创新并非提出一种全新的模型架构，而是构建了一套**面向城市智能体的细粒度时空推理评测体系**，并通过可控实验揭示了当前大语言模型（LLM）在城市任务中的关键瓶颈与驱动因素。

### 1. 过程导向的四维推理分解

现有城市 LLM 基准（如 CityBench、CityGPT）多聚焦于最终任务结果的评估，难以诊断模型在推理链中具体环节的失效。USTBench 将城市时空推理**显式分解为四个可独立评测的子过程**：时空理解（Spatiotemporal Understanding）、预测（Forecasting）、规划（Planning）与反思（Reflection）。这一分解构成了评测框架的核心结构变化，使得分析可以从“模型是否做对”深入到“模型在哪一步出错”。基于该框架构建了 62,466 条结构化问答对，其中 40% 用于基础时空理解评测，60% 用于高层推理评测（Table 2）。

### 2. 揭示通用推理能力向城市时空推理迁移的局限

通过对比同参数规模与架构的非推理模型与推理模型（如 Qwen2.5-32B vs. QwQ-32B），USTBench 发现了一个反直觉的关键事实：**通用推理能力的增强并不总能迁移至城市时空推理**。DeepSeek-R1 在拥堵预测的结果指标上略逊于 Llama3.3（Figure 1），且在长时间趋势分析（拥堵、交通 OD 预测）中，非推理基模型常优于其推理变体（Table 4）。这表明推理模型擅长的逻辑链延伸，在面对结构化时空数据的长期依赖时反而可能引入偏差。

### 3. 域适应后训练作为关键可控因素

与推理增强相比，**专注于时空理解的域适应后训练展现出更强的性能驱动力**。Qwen2.5-7B 在经过时空理解专项微调后（Qwen2.5-7B-ST），在预测与规划任务上不仅显著超越其原始基模型，也优于同等规模的推理蒸馏变体 DeepSeek-R1-Distill-Qwen-7B（Figure 4）。这一发现将“域特异性时空特征学习”确立为提升城市代理性能的关键因果杠杆，而非简单地堆叠通用推理能力。

### 4. 反思能力的瓶颈效应

消融实验进一步锁定了当前 LLM 在城市动态环境中的**核心脆弱环节——反思**。移除反思组件导致 DeepSeek-R1 在所有消融项中性能降幅最大（Figure 6），而大多数 LLM 的反思准确率不足 50%（Table 4）。与此同时，对于较弱的基础模型（如 Qwen2.5-7B），中间推理与反思的引入反而可能产生负面影响，说明**推理流程的复杂度需要与模型能力自适应匹配**，否则会引入额外的噪声而非增益。

### 5. 交互式环境与半随机策略的数据支撑

为支撑上述评测，USTBench 配套构建了交互式城市环境 UAgentEnv，覆盖 5 项决策任务与 4 项预测任务。其数据采集采用基于 ε-greedy 策略的半随机启发式智能体：

$$\pi_{g}(o) = \begin{cases} \arg\max_{a \in A} Q(o, a), & \text{with probability } 1-\epsilon \\ \text{random}(A), & \text{with probability } \epsilon \end{cases}$$

该策略通过探索系数 ε 平衡最优与随机动作，保证了观测数据的多样性。规划评估中，最优动作通过仿真搜索最大化期望累积折扣奖励确定：

$$a_i^* = \arg\max_{a_i \in A} \max_{a_{i+1}, \ldots, a_{i+H} \in A} \mathbb{E}\left[ \sum_{j=0}^{H} \gamma^j R(a_{i+j}) \mid a_i \right]$$

这一数据生成与评估框架为城市 LLM 智能体提供了统一的交互与评测接口。

### 创新边界与待验证方向

USTBench 的创新集中在**评测体系与诊断分析**层面，在增强时空推理的方法探索上仍显不足。模型在长程空间连通性与长时间周期性、趋势性模式上的准确率常低于 70%，暴露了结构化数据推理的结构性短板。此外，评估主要基于模拟环境与历史数据集，缺乏真实城市部署验证；部分推理模型（如 DeepSeek-R1）推理过程冗长且计算开销高昂，难以满足实时城市决策需求。这些方向构成了后续方法创新的关键切入点。

## 整体框架

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_ETzBStUFJy/figures/001_Table_1.jpg]]
*Table 1: Comparison of LLM benchmarks in urban tasks*

USTBench 将城市时空推理系统性地分解为四个核心认知过程：**时空理解 (Spatiotemporal Understanding)**、**预测 (Forecasting)**、**规划 (Planning)** 与**反思 (Reflection)**。这四者构成一个递进且闭环的推理流水线——理解负责解析环境的结构化观测，预测推演未来状态，规划据此选择行动，反思则评估输出并基于环境反馈修正策略。

整个框架的运行依托于 **UAgentEnv**，一个交互式城市环境（Figure 3）。该环境定义了统一的城市智能体交互范式：每个任务首先向智能体提供任务描述、数据模式及相关领域知识；随后，智能体接收实时城市时空动态的观测数据，依次执行理解、预测、规划，生成动作或预测；最后，环境反馈结果，触发反思环节以调整后续决策。这一流水线覆盖了五类典型决策任务与四类预测任务，确保评估的全面性。

在数据构建层面，决策任务的观测通过一个遵循 **ε-greedy 启发式策略** 的智能体与环境交互采集：

$$
\pi_{g}(o) = \begin{cases} \arg\max_{a \in A} Q(o, a), & \text{with probability } 1-\epsilon \\ \text{random}(A), & \text{with probability } \epsilon \end{cases}
$$

其中 $\epsilon \in [0, 1]$ 控制探索系数，以概率 $\epsilon$ 随机选择动作，确保采集场景的多样性。空间观测被口头化为稀疏邻接矩阵（含节点与边属性），时间观测则以离散时间区间上的属性值序列呈现。整个基准最终包含 **62,466 个结构化问答对**（Table 2），其中 40% 用于基础时空理解评估，60% 用于高阶推理评估。

在评估层面，规划任务通过仿真搜索确定最优动作，以最大化期望累积折扣奖励：

$$
a_i^* = \arg\max_{a_i \in A} \max_{a_{i+1}, \ldots, a_{i+H} \in A} \mathbb{E}\left[ \sum_{j=0}^{H} \gamma^j R(a_{i+j}) \mid a_i \right]
$$

该公式在规划评估中作为 ground truth，与模型输出的动作进行对比。下游任务评估则采用领域特定指标：GDP 预测使用三年窗口的 MAPE，拥堵预测使用准确率与 MAPE，城市规划评估公共服务可达性与生态覆盖率。

值得注意的是，现有城市 LLM 基准（如 CityBench、CityGPT、UrbanPlanBench）在推理能力的覆盖上存在明显缺口（Table 1）：多数基准缺乏对反思能力的评估，且未同时涵盖非推理与推理两类基线模型。USTBench 通过统一的提示模板与执行框架，在相同参数规模与架构的非推理/推理模型间进行公平对比（如 Qwen2.5-32B vs QwQ-32B），从而有效隔离推理能力增益的贡献。

## 核心模块与公式推导

### 城市环境的形式化定义

USTBench 将城市环境形式化为一个交互系统，为后续的推理能力分解提供数学基础：

$$E = \langle \bar{S}, A, O, \bar{T} \rangle$$

其中 $\bar{S}$ 为城市状态空间，$A$ 为动作空间，$O$ 为观测空间，$\bar{T}$ 为状态转移函数。在此框架下，预测任务的目标是预判未来 $\Delta$ 步的城市状态 $\{ s_{i+1}, \dotsc, s_{i+\Delta} \}$，而决策任务则依赖智能体策略 $\pi(o)$ 基于观测生成动作序列。

### 四阶段推理流水线

USTBench 将城市时空推理分解为四个关键过程（Section 4.1），构成统一的评估流水线：

1. **时空理解（Spatiotemporal Understanding）**：解析城市空间结构与时间模式，涵盖距离、邻接、连通性、持续时间、时序、趋势、局部极值、周期性等八类时空模式。
2. **预测（Forecasting）**：基于历史观测 $o_i$ 预测下一时刻的城市状态 $s_{i+1}$。
3. **规划（Planning）**：在决策任务中选择最大化累积奖励的动作序列。
4. **反思（Reflection）**：评估先前输出，基于环境反馈修正策略。

### 数据采集策略

为构建决策任务的问答对，USTBench 采用启发式智能体以半随机策略与环境交互（Section 4.1.1）：

$$\pi_{g}(o) = \begin{cases} \arg\max_{a \in A} Q(o, a), & \text{with probability } 1-\epsilon \\ \text{random}(A), & \text{with probability } \epsilon \end{cases}$$

其中探索系数 $\epsilon \in [0, 1]$ 控制随机动作的选择概率：以 $1-\epsilon$ 概率选择效用函数 $Q(o, a)$ 最大化的动作，以 $\epsilon$ 概率随机选择动作，从而确保采集场景的多样性。空间观测被口头化为稀疏邻接矩阵（含节点与边属性），时间观测则以离散时间间隔的属性值序列呈现。

### 规划评估的最优动作定义

在规划评估中，通过仿真搜索确定最大化期望累积折扣奖励的最优动作（Section 4.1.4）：

$$a_i^* = \arg\max_{a_i \in A} \max_{a_{i+1}, \ldots, a_{i+H} \in A} \mathbb{E}\left[ \sum_{j=0}^{H} \gamma^j R(a_{i+j}) \mid a_i \right]$$

其中 $H$ 为规划视界，$\gamma$ 为折扣因子，$R(\cdot)$ 为奖励函数。该公式通过遍历未来 $H$ 步的动作序列，计算从当前动作 $a_i$ 出发的期望累积折扣奖励，以此判定规划动作的优劣。

### 模块间的因果依赖

消融实验（Figure 6）揭示了各模块对下游性能的差异化影响：移除反思组件导致 DeepSeek-R1 性能降幅最大，表明反思对于动态城市任务的必要性；移除时空理解模块则显著增加预测误差并降低规划准确率。值得注意的是，对于较弱模型 Qwen2.5-7B，中间推理与反思可能产生负面影响，提示模块组合需与模型能力相匹配。

## 实验与分析

### 核心发现：推理能力迁移的边界与时空理解的瓶颈

实验揭示了一个核心矛盾：通用推理能力的强化并不总能迁移至城市时空推理。**DeepSeek-R1** 在拥堵预测的结果指标上略逊于 **Llama3.3-70B**（Figure 1），表明推理模型在特定时空趋势分析中存在弱点。这一发现与直觉相悖——通常认为更强的推理链（Chain-of-Thought）应带来全面提升，但城市时空数据的高度结构化特征（稀疏邻接矩阵、离散时间序列）可能使通用推理策略失效。

真正的性能瓶颈集中在两个维度：**长程空间关系（连通性）** 与 **长时间模式（周期性、趋势）**。如表 3 所示，即使是最优模型在这些子能力上的准确率也常低于 70%。这暴露了 LLM 对结构化时空数据内在规律的理解不足——模型擅长捕捉局部共现模式，但在需要跨时空跨度进行因果推断时表现急剧下降。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_ETzBStUFJy/figures/006_Table_3.jpg]]
*Table 3: Performances on spatiotemporal understanding*

### 时空理解评估：推理模型的相对优势与绝对短板

表 3 给出了时空理解八类子能力的详细评估。推理模型整体优于非推理模型 7–20%，其中 **o4-mini** 以 0.7924 的总体准确率领先，**GPT-4o** 为 0.7259。但在连通性（Connectivity）子任务上，o4-mini 也仅达 0.7665，GPT-4o 为 0.6787——这意味着即便是最强模型，在判断空间节点间的间接可达性时仍有近四分之一的错误率。

值得注意的是，**Figure 2** 的雷达图直观展示了模型间的能力分化：推理模型（**QwQ-32B**、**DeepSeek-R1**）在反思（Reflection）和规划（Planning）维度上拉开明显差距，但在基础时空理解维度上的优势相对收敛。这暗示推理能力的增益主要体现在高层认知过程，而非底层模式识别。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_ETzBStUFJy/figures/003_Figure_2.jpg]]
*Figure 2: The performance of leading LLMs in urban spatiotemporal reasoning*

### 预测与规划：预测尚可，规划堪忧

表 4 的结果呈现出鲜明的任务难度梯度。多数 LLM 在预测任务上能达到 70% 以上的准确率，但在规划任务上表现大幅下滑。这一落差揭示了当前 LLM 的核心缺陷：**单步预测可依赖历史模式的统计外推，而多步规划需要构建并维护长程目标导向的因果链**。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_ETzBStUFJy/figures/007_Table_4.jpg]]
*Table 4: Performance of LLMs in forecasting, planning, and reflection abilities*

更令人警惕的是，在部分长期趋势分析任务（拥堵预测、交通 OD 预测）中，非推理基模型反而优于其推理变体——例如 **Qwen2.5-32B** 在拥堵预测上超过 **QwQ-32B**，**Llama3.3-70B** 在交通 OD 预测上超过 **DeepSeek-R1**。这进一步证实了通用推理增强可能引入与领域规律相悖的归纳偏置。

### 域适应后训练：因果操纵的关键证据

最有力的因果证据来自时空理解增强实验（Section 5.2.3）。对 **Qwen2.5-7B** 进行专项时空理解后训练得到的 **Qwen2.5-7B-ST**，在预测与规划任务上不仅显著优于原始基模型，也超越了其推理蒸馏变体（**DeepSeek-R1-Distill-Qwen-7B**），如 Figure 4 所示。这一结果直接验证了核心假说：**域特异性时空特征学习是驱动下游性能的关键可控因素**，其效果甚至优于通用推理能力的注入。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_ETzBStUFJy/figures/008_Figure_4.jpg]]
*Figure 4: The performance of the model with enhanced spatiotemporal understanding abilities*

### 反思能力：关键但脆弱

反思（Reflection）是表现最差的维度——多数模型准确率不足 50%（Table 4）。消融实验（Figure 6）进一步揭示了反思的双刃剑特性：

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_ETzBStUFJy/figures/011_Figure_6.jpg]]
*Figure 6: The ablation of each reasoning ability on the task performance*

- 对于 **DeepSeek-R1**，移除反思组件导致性能降幅最大，表明强推理模型确实依赖反思来修正策略。
- 对于 **Qwen2.5-7B**，引入中间推理与反思反而产生负面影响——弱模型可能因推理链中的错误累积而偏离正确方向。
- 对于 **Qwen2.5-32B**，绕过预测直接规划反而带来轻微提升，暗示其中间预测步骤可能引入噪声。

这一模式表明：**推理流程的设计必须与模型能力匹配**，盲目堆叠推理组件对弱模型有害。

### 下游任务综合表现：LLM 对经典方法的超越与局限

表 5 汇总了下游任务的全面对比。LLM 在预测与决策任务上普遍优于经典方法，预测准确率提升最高达 337.31%，决策有效性提升最高达 53.48%。但这一优势需要审慎解读：经典方法通常针对单一任务优化，而 LLM 的跨任务泛化能力是其核心价值。

**o4-mini** 在社会经济预测上取得 4.97% 的 MAPE，相比经典方法有数量级的改善。然而，这一结果基于历史数据模拟，缺乏真实城市部署的验证——这是当前评估框架的根本局限。

### 失败模式总结

综合所有实验结果，可归纳出三类系统性失败模式：

1. **结构化数据推理缺陷**：LLM 在需要精确数值计算和长程依赖追踪的时空模式（连通性、周期性、趋势）上持续表现不佳，准确率常低于 70%。
2. **规划能力严重不足**：从单步预测到多步规划的跨越构成当前 LLM 的最大能力断层，反映了长期目标导向推理的根本性困难。
3. **推理增强的领域不兼容**：通用推理模型在城市时空任务中并不总能超越非推理模型，甚至可能因推理偏置而表现更差——这挑战了“更强推理即更好智能体”的朴素假设。

**需人工核实**：部分下游任务（如 POI 放置、路线规划）的经典方法基线具体配置在提供的分析材料中未充分展开，其与 LLM 的可比性需查阅原文确认。

## 方法谱系与知识库定位

### 1. 与现有城市LLM基准的关系

USTBench 是首个将城市时空推理显式分解为**时空理解、预测、规划、反思**四个可评估过程的基准。Table 1 将其与 STBench、CityBench、CityGPT、UrbanPlanBench 等现有基准进行了系统对比。差异主要体现在三方面：其一，现有基准多仅覆盖部分推理能力（如 CityBench 侧重理解与规划），而 USTBench 首次将反思纳入评估体系；其二，现有工作多采用基于结果的单一评估，USTBench 同时提供基于过程与基于结果的评估框架；其三，USTBench 构建了交互式城市环境 UAgentEnv，统一了九类城市任务的评估接口，而非依赖静态数据集。

### 2. 基线模型谱系

论文评估了覆盖非推理与推理两大范式的代表性 LLM，包括：

| 类型 | 模型 | 规模 | 来源 |
|------|------|------|------|
| 非推理 LLM | **Qwen2.5** | 7B / 32B | Yang et al., 2024 |
| 非推理 LLM | **GLM4** | 9B / 32B | GLM et al., 2024 |
| 非推理 LLM | **Llama3.3** | 70B | Grattafiori et al., 2024 |
| 非推理 LLM | **GPT-4o** | 闭源 | Hurst et al., 2024 |
| 推理 LLM | **DeepSeek-R1 系列** | Distill 7B/70B 及完整版 | Guo et al., 2025 |
| 推理 LLM | **QwQ** | 32B | Team, 2025 |
| 推理 LLM | **GLM-Z1 系列** | 9B / 32B | GLM et al., 2024 |
| 推理 LLM | **o4-mini** | 闭源 | Jaech et al., 2024 |

实验设计通过控制参数规模与架构（如 Qwen2.5-32B vs QwQ-32B）来隔离推理能力的增益，同时采用统一的提示模板与执行框架以减少实现偏差。

### 3. 知识库定位：域适应 vs 通用推理

USTBench 的核心发现是**通用推理能力的强化并不总能迁移至城市时空推理**。Figure 1 显示 DeepSeek-R1 在拥堵预测的结果指标上略逊于 Llama3.3，揭示了推理模型在特定时空趋势分析中的弱点。更关键的证据来自域适应实验：对 Qwen2.5-7B 进行时空理解后训练得到的 **Qwen2.5-7B-ST**，在预测与规划任务上不仅显著优于原始模型，也优于其推理变体 DeepSeek-R1-Distill-Qwen-7B（Figure 4）。这表明**域特异性时空特征学习**是驱动下游性能的关键可控因素，其效果超过通用推理能力的增强。

### 4. 适用边界与局限

**模型规模与推理复杂度的适配边界**：消融实验（Figure 6）显示，对于弱模型 Qwen2.5-7B，中间推理与反思可能产生负面影响；而 DeepSeek-R1 移除反思组件后性能降幅最大。这说明反思等高级推理能力仅在模型具备足够基础能力时才产生正向增益，存在明确的能力阈值。

**结构化数据推理的薄弱地带**：LLM 在长程空间关系（连通性准确率常低于 70%）和长时间模式（周期性、趋势准确率常低于 70%）上表现不佳（Table 3），暴露了其在结构化数值数据推理上的根本性不足。

**真实部署的验证缺失**：评估主要基于模拟环境和历史数据集，缺乏对真实城市应用部署的验证。此外，部分推理模型（如 DeepSeek-R1）推理过程冗长，推理耗时可达 97.33 s/batch（Table 8），不适用于实时城市决策场景。

### 5. 开放问题

1. **轻量级时空推理范式设计**：受 o4-mini 在低计算开销下取得领先性能的启发，如何设计高效的城市时空推理范式？
2. **推理模型的领域退化问题**：DeepSeek-R1 在拥堵预测等任务中表现不及非推理模型，其重复生成问题如何缓解？
3. **工具与代码建模整合**：如何更好地整合工具调用和代码建模以支撑更深层次的时空模式解析？
4. **自适应推理流程**：不同城市任务与模型规模应如何自适应组合推理流程，以避免弱模型因复杂推理而受损？

## 原文 PDF

![[paperPDFs/ICLR_2026/USTBench_Benchmarking_and_Dissecting_Spatiotemporal_Reasoning_Capabilities_of_LLMs_as_Urban_Agents.pdf]]
