---
title: "Agent-X: Evaluating Deep Multimodal Reasoning in Vision-Centric Agentic Tasks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Agent_X_Evaluating_Deep_Multimodal_Reasoning_in_Vision_Centric_Agentic_Tasks.pdf
aliases:
- AX
- Agent-X
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "构建带工具轨迹和细粒度指标的真实多模态智能体评测基准。"
primary_logic: "Agent-X收集六类视觉中心任务并标注工具增强推理轨迹，再从步骤、深度推理和结果三种模式评估LMM。"
claims:
- "Agent-X覆盖828个真实世界多模态任务，包含图像、视频、文本和14个可执行工具。"
- "细粒度指标能够区分 grounding、工具选择、事实性、语义正确性和最终目标达成。"
- "即使最佳模型在Agent-X上的Goal Accuracy也低于50%，显示现有LMM仍难完成全链推理。"
- "错误分析显示规划失败、视觉误解、工具幻觉和JSON格式错误是主要瓶颈。"
---

# Agent-X: Evaluating Deep Multimodal Reasoning in Vision-Centric Agentic Tasks

> [!tip] 核心洞察
> Agent-X是首个将大规模真实世界多模态输入（图像、视频、文本）与工具增强的分步推理评估相结合，覆盖六个不同环境的基准测试。其核心贡献在于提供了一个可解释的、细粒度的评估框架，能够区分真正的逻辑推理与表面上的连贯但实际脱节的推理链，从而揭示当前LMM在规划、适应和工具使用方面的关键局限性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Agent-X：评估视觉中心智能体任务中的深度多模态推理能力 |
| 英文题名 | Agent-X: Evaluating Deep Multimodal Reasoning in Vision-Centric Agentic Tasks |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Vjruxvp1Xd); [GitHub](https://github.com/mbzuai-oryx/Agent-X); [Project](https://huggingface.co/datasets/Tajamul21/Agent-X) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Agent-X |
| Dataset | Agent-X |

> [!tip] 效果简介
> - Agent-X 上，Goal Accuracy (G_acc) 为 o4-mini: 0.45，对比 GPT-4o: 0.37，变化 +0.08。
> - Agent-X 上，Goal Accuracy (G_acc) 为 Gemini-2.5-Pro: 0.40，对比 Gemini-1.5-Pro: 0.04，变化 +0.36。
> - Agent-X 上，Goal Accuracy (G_acc) 为 Qwen2.5-VL-7B: 0.36，对比 InternVL3-8B: 0.20，变化 +0.16。

## 概述

Agent-X是一个大规模基准测试，专门用于评估视觉中心智能体（vision-centric agents）在真实世界多模态环境中的多步推理和深度推理能力。该基准测试包含828个智能体任务，覆盖六个主要环境：通用视觉推理、网页浏览、安防监控、自动驾驶、体育和数学推理。Agent-X的核心贡献在于提出了一个细粒度的、分步评估框架，能够系统性地诊断当前最先进的大多模态模型（LMM）在规划、适应和工具使用方面的关键局限性。

实验结果表明，即使是最佳模型（包括GPT、Gemini和Qwen系列），在Agent-X上的全链成功率也低于50%。o4-mini在Goal Accuracy (G_acc)上表现最佳，达到45%，而大多数开源模型低于30%。

## 背景与动机

当前最先进的大多模态模型（LMM）在需要多步推理和工具调用的视觉中心智能体任务中，全链成功率低于50%。主要瓶颈在于模型无法在真实世界场景中保持逻辑连贯的多步推理、有效使用工具，并避免幻觉和格式错误。

现有基准测试（如GAIA、GTA、ToolBench、APIBench）存在以下不足：
- 仅关注最终答案正确性，缺乏对中间推理步骤的细粒度评估
- 主要为文本或静态图像输入，缺乏真实世界多模态输入
- 任务来源完全合成或人工标注，缺乏可扩展性
- 查询中明确提及所需工具或步骤，无法评估模型的独立规划能力
- 覆盖单一或有限领域，缺乏环境多样性

Agent-X基准测试通过引入细粒度的、分步评估框架（包括Grounding Score、Tool Precision、Faithfulness Accuracy等指标），以及包含14个可执行工具和828个真实世界任务的半自动化构建流程，来系统性地诊断和量化这些推理缺陷。

## 核心创新

Agent-X是首个将大规模真实世界多模态输入（图像、视频、文本）与工具增强的分步推理评估相结合，覆盖六个不同环境的基准测试。其核心贡献在于提供了一个可解释的、细粒度的评估框架，能够区分真正的逻辑推理与表面上的连贯但实际脱节的推理链，从而揭示当前LMM在规划、适应和工具使用方面的关键局限性。

与现有基准测试的关键差异如Table 1和Table 2所示：

**Table 1**: Comparison of Agentic Benchmarks. Columns show key dimensions including scale, realism, modality, reasoning depth, tool interaction, and annotation quality. Our benchmark Agent-X uniquely supports all criteria with 828 diverse, manually verified agentic tasks.

**Table 2**: Task comparison of Agent-X with existing benchmarks. Unlike prior benchmarks, the queries in Agent-X avoid explicit tool references and direct instructions, thus encouraging agents to reason and act independently. Blue indicate explicit task guidance; Red highlights denote explicit tool invocation in prior benchmarks.

## 整体框架

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Vjruxvp1Xd_Agent-X_Evaluat/figures/001_Table_1.jpg]]
*Table 1: Comparison of Agentic Benchmarks. Columns show key dimensions including scale, realism, modality, reasoning depth, tool interaction, and annotation quality. Our benchmark Agent-X uniquely supports all criteria with 828 diverse, manually verified agentic tasks.*

Agent-X基准测试的构建遵循半自动化流水线（如Figure 2所示），包含以下关键模块：

**Figure 2**: Overview of the Agent-X benchmark construction pipeline. Starting from multimodal data and a predefined toolset, an LMM generates initial queries, which are refined by annotators for realism and correctness. The LMM then produces step-by-step reasoning, which is refined to create a high-quality tool-augmented reasoning trace.

**Figure 3**: Overview of the Agent-X benchmark. (a) Key data statistics. (b) Overall frequency of tool usage and number of steps. (c) Distribution of tasks across six environments.

**Figure 1**: Agent-X Snapshot: Example tasks from our benchmark illustrating multimodal queries that require step-by-step reasoning, tool use, and visual understanding across images and video. Each task includes structured thoughts, tool invocations, and a ground-truth answer with justification. The detailed annotations in Agent-X enable thorough evaluation of existing agentic pipelines.

## 核心模块与公式推导

### 5.1 任务形式化定义

每个任务被形式化定义为结构化元组：

${ \cal { S } } _ { i } = ( \bar { \mathcal { V } _ { i } } , \bar { \mathcal { Q } _ { i } } , \mathcal { T } _ { i } , \mathcal { R } _ { i } , \bar { \mathcal { A } _ { i } } , \mathcal { T } _ { i } )$

其中包含多模态上下文、查询、工具子集、推理轨迹、最终答案和理由。

### 5.2 推理轨迹

推理轨迹是一个由m个步骤组成的序列：

$\mathscr { R } _ { i } = \{ ( t _ { j } , a _ { j } , r _ { j } ) \} _ { j = 1 } ^ { m }$

每个步骤包含工具t_j、输入参数a_j和结果输出r_j。

### 5.3 工具子集

工具子集T_i是包含N个工具的完整工具集T_c的子集：

$\mathcal { T } _ { i } \subseteq \dot { \mathcal { T } _ { c } } = \{ t _ { k } \} _ { k = 1 } ^ { N }$

### 5.4 评估框架

Agent-X使用三个评估模式（Step-by-Step、Deep Reasoning、Outcome）和10个细粒度指标，如Table 3所示：

**Table 3**: Evaluation Metrics. This table outlines the full suite of metrics used in Agent-X benchmark, organized by Step-by-Step, Deep Reasoning, and Outcome modes.

## 实验与分析

### 6.1 主要结果

Table 4展示了多个模型在Agent-X上的核心评估结果：

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Vjruxvp1Xd_Agent-X_Evaluat/figures/009_Table_4.jpg]]
*Table 4: Overall results on Agent-X. We report performance across three evaluation modes: Step-by-Step, Deep Reasoning, and Outcome. Metrics include: $\mathbf { G _ { s } }$ (Grounding Score), $\mathbf { T _ { p } }$ (Tool Precision), $\mathbf { T _ { a c c } }$ (Tool Accuracy), $\mathbf { F _ { a c c } }$ (Faithfulness Accuracy), $\mathbf { C _ { s } }$ (Context Score), $\mathbf { F _ { p } }$ (Factual Precision), $\mathbf { S _ { a c c } }$ (Semantic Accuracy), $\mathbf { G } _ { \mathbf { a c c } }$ (Goal Accuracy), $\mathbf { \dot { G } } _ { \mathbf { a } } ^ { * }$ (Goal Accuracy/ImgGen), and $\mathbf { T _ { a c c } ^ { s } }$ (Toolset Accuracy). The best results are highlighted in bold, and second-best...

**Table 4**: Overall results on Agent-X. We report performance across three evaluation modes: Step-by-Step, Deep Reasoning, and Outcome. Metrics include: G_s (Grounding Score), T_p (Tool Precision), T_acc (Tool Accuracy), F_acc (Faithfulness Accuracy), C_s (Context Score), F_p (Factual Precision), S_acc (Semantic Accuracy), G_acc (Goal Accuracy), G_a^* (Goal Accuracy/ImgGen), and T_acc^s (Toolset Accuracy).

关键发现：
- o4-mini在Goal Accuracy (G_acc)上表现最佳，达到0.45
- GPT-4o达到0.37，Gemini-2.5-Pro达到0.40
- 大多数开源模型低于0.30
- Gemini-1.5-Pro仅达到0.04，表现最差

### 6.2 错误分析

Table 5展示了主要模型的错误分类：

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Vjruxvp1Xd_Agent-X_Evaluat/figures/011_Table_5.jpg]]
*Table 5: Error Breakdown Across Models. Common planning, formatting, and reasoning errors on Agent-X across GPT-4o, Gemini-1.5-Pro, and InternVL3-8B. Formatting errors are counted alongside planning and reasoning errors. Extended details in Appendix §F.1.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Vjruxvp1Xd_Agent-X_Evaluat/figures/012_Table_5.jpg]]

**Table 5**: Error Breakdown Across Models. Common planning, formatting, and reasoning errors on Agent-X across GPT-4o, Gemini-1.5-Pro, and InternVL3-8B. Formatting errors are counted alongside planning and reasoning errors.

关键发现：
- Gemini-1.5-Pro的44.5%错误是JSON格式错误，34.3%是视觉误解
- GPT-4o有17.6%的无响应错误和18.5%的视觉误解
- InternVL3-8B有33.8%的JSON错误和16.4%的最终格式错误

### 6.3 定性分析

**Figure 4**: Qualitative comparison of GPT-4o and VideoLLaMA3-7B on Agent-X visual reasoning tasks. GPT-4o hallucinates tool use and gives incorrect justifications; VideoLLaMA3-7B lacks temporal reasoning and frame alignment.

**Figure 5**: Qualitative comparison of InternVL on visual reasoning tasks from Agent-X. InternVL generally follows the correct step structure but exhibits internal inconsistencies in final answers and justifications.

**Figure 6**: Qualitative comparison of Qwen2.5 on visual reasoning tasks from Agent-X. Qwen2.5 often hallucinates tool behavior and produces overconfident justifications without numerical evidence.

### 6.4 消融实验

- 包含推理步骤可将整体Goal Accuracy (G_acc)从0.33提升至0.43，相对提升约30%
- Qwen2.5-VL-7B在简单查询上的Goal Accuracy为39%，在困难查询上降至31%
- InternVL3-8B在简单查询上的Goal Accuracy为28%，在困难查询上降至14%

### 6.5 工具调用分析

- GPT系列模型在总工具调用中成功率最高，达到83.8%
- Qwen2.5-VL-8B在2241次调用中仅有109次失败，显示出最高的工具调用精度
- o4-mini是最激进的模型，发出3374次调用，但失败率也最高（1038次）

### 6.6 人类评估验证

人类评估证实了自动评估的排名：Gemini-2.5-Pro > Qwen2.5-VL-7B > InternVL3-8B > VideoLLaMA3-7B。人类评分与自动评分高度相关，残余差异均匀分布，确认不存在系统性偏好。

**Table 10**: Results on Agent–X with human evaluation. We report performance on 50 Agent-X tasks across three evaluation modes: Step-by-Step, Deep Reasoning, and Outcome.

### 6.7 公平性保障

- 所有预测结果均经过多个评判者（GPT-4o、Qwen-14B和人类）交叉检查，模型排名在不同设置下保持一致
- 评估指标明确具有偏差感知能力（将语法与语义解耦，标准化工具参数）
- 任务种子经过严格的质量保证（QA）重写，以避免数据泄露；种子与最终提示之间的token重叠率低于7%

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Vjruxvp1Xd_Agent-X_Evaluat/figures/003_Table_2.jpg]]
*Table 2: Task comparison of Agent-X with existing benchmarks. Unlike prior benchmarks, the queries in Agent-X avoid explicit tool references and direct instructions, thus encouraging agents to reason and act independently. Blue indicate explicit task guidance; Red highlights denote explicit tool invocation in prior benchmarks.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Vjruxvp1Xd_Agent-X_Evaluat/figures/008_Table_3.jpg]]
*Table 3: Evaluation Metrics. This table outlines the full suite of metrics used in Agent-X benchmark, organized by Step-by-Step, Deep Reasoning, and Outcome modes.*

## 方法谱系与知识库定位

Agent-X在智能体评估基准测试谱系中占据独特位置。与GAIA、GTA、ToolBench和APIBench等现有基准测试相比，Agent-X是首个同时支持大规模真实世界多模态输入、工具增强的分步推理评估、以及跨六个多样化环境评估的基准测试。

**局限性**：
- Agent-X目前是单语的，可能继承某些分布偏差
- 半自动化的查询和工具链生成方法虽然提高了效率，但偶尔会产生质量较低的样本
- 基准测试目前仅覆盖六个环境，可能无法完全代表所有现实世界的智能体任务
- 评估指标（如G_s）在不同评判者之间的一致性较低，表明高级主观目标的标准化仍然困难
- 基准测试主要关注视觉中心任务，对纯文本或音频模态的覆盖有限

**开放问题**：
- 如何扩展Agent-X以支持多语言和多文化背景下的智能体评估？
- 如何进一步提高半自动化流水线生成样本的质量和一致性？
- 如何设计更鲁棒的评估指标，以更好地捕捉高级推理目标和主观判断？
- Agent-X中观察到的模型失败模式（如格式错误、工具幻觉）的根本原因是什么？如何通过模型架构或训练策略来解决？
- 如何将Agent-X的评估框架扩展到包含更多模态（如音频、触觉）和更复杂的交互环境？
- 当前最佳模型（如o4-mini, Gemini-2.5-Pro）在Agent-X上的性能上限是什么？需要哪些突破才能实现更高的全链成功率？

## 原文 PDF

![[paperPDFs/ICLR_2026/Agent_X_Evaluating_Deep_Multimodal_Reasoning_in_Vision_Centric_Agentic_Tasks.pdf]]
