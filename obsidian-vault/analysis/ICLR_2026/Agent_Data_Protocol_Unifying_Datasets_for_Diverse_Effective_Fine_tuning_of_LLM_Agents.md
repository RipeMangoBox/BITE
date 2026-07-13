---
title: "Agent Data Protocol: Unifying Datasets for Diverse, Effective Fine-tuning of LLM Agents"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Agent_Data_Protocol_Unifying_Datasets_for_Diverse_Effective_Fine_tuning_of_LLM_Agents.pdf
project_link: null
code_link: null
aliases:
- ADPA
- ADPUDDEFTLA
- "Agent Data Protocol (ADP)"
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "ADP standardizes agent trajectories into action and observation objects that bridge heterogeneous raw datasets and SFT formats."
primary_logic: "Raw datasets are converted once into ADP trajectories, then converted from ADP into framework-specific SFT formats through a hub-and-spoke pipeline."
claims:
- "ADP reduces conversion cost from O(DxA) pairwise adapters to O(D+A) dataset and agent adapters."
- "The protocol represents diverse agent interactions with API, code, and message actions plus text and web observations."
- "ADP Dataset V1 combines 1.3M trajectories and improves agent benchmarks after fine-tuning."
---

# Agent Data Protocol: Unifying Datasets for Diverse, Effective Fine-tuning of LLM Agents

> [!tip] 核心洞察
> 尽管表面形式多样，大多数智能体交互都可以分解为智能体执行的动作序列和从环境接收的观察序列。通过标准化这些基本组件，ADP 能够统一来自不同领域（编码、软件工程、API/工具使用、网页浏览）的数据集，同时保留原始数据的丰富语义。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Agent数据协议：统一数据集以实现LLM智能体的多样化高效微调 |
| 英文题名 | Agent Data Protocol: Unifying Datasets for Diverse, Effective Fine-tuning of LLM Agents |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=tG6301ORHd) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | Agent Data Protocol (ADP) |
| Dataset | SWE-Bench (Verified), WebArena |

> [!tip] 效果简介
> - SWE-Bench (Verified) 上，Accuracy 为 20.2%，对比 0.4%，变化 +19.8%。
> - SWE-Bench (Verified) 上，Accuracy 为 34.4%，对比 2.0%，变化 +32.4%。
> - SWE-Bench (Verified) 上，Accuracy 为 40.3%，对比 2.2%，变化 +38.1%。

## 概要

本文提出 **Agent Data Protocol (ADP)**，一种轻量级表示语言，旨在解决大规模智能体监督微调中的数据碎片化问题。ADP 充当异构智能体数据集与统一训练流程之间的“中间语言”，通过标准化动作和观察的表示，将数据转换成本从二次方 O(D×A) 降低为线性 O(D+A)。基于 ADP，作者构建并发布了目前最大的公开智能体训练数据集 ADP Dataset V1，包含 130 万条轨迹，覆盖编码、软件工程、API/工具使用和网页浏览四大领域。实验表明，ADP 微调在 SWE-Bench Verified、WebArena、AgentBench 和 GAIA 等多个基准上平均提升约 20% 的性能，并在跨任务迁移中显著优于单一领域数据微调。



大规模智能体监督微调的主要瓶颈并非缺乏底层数据源，而是大量数据因异构的格式、工具和接口而碎片化，导致难以有效组合和利用。现有智能体训练数据集（如 SWE-Gym、CodeActInstruct、Mind2Web、AgentInstruct 等）各自使用独立的格式（HTML、accessibility tree、自定义 JSON 等），每个数据集需要为每个智能体框架编写自定义的 Raw→SFT 转换器，总成本为 O(D × A)。这种碎片化现状严重阻碍了跨领域数据融合和智能体能力的泛化。



## 核心方法与创新机理

ADP 的核心洞察在于：尽管表面形式多样，大多数智能体交互都可以分解为智能体执行的动作序列和从环境接收的观察序列。通过标准化这些基本组件，ADP 能够统一来自不同领域的数据集，同时保留原始数据的丰富语义。

ADP 的设计围绕三个核心原则：
- **简洁性 (Simplicity)**：最小化模式复杂度，降低采用门槛
- **标准化 (Standardization)**：统一动作和观察的表示，消除格式异构
- **表达力 (Expressiveness)**：保留原始数据的丰富语义，支持多种智能体交互模式



![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_tG6301ORHd_Agent_Data_Pr/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the Agent Data Protocol (ADP). Raw data from diverse sources such as SWE-Gym are converted into a standardized ADP format. ADP unifies data into Trajectory objects, which include two core components: Actions (API action, code action, message action) and Observations (text observation, web observation), enabling seamless integration with various agent SFT formats. Example conversions show how heterogeneous raw data is normalized for training agentic models.*

ADP 的整体框架如 Figure 1 所示，采用中心辐射式 (hub-and-spoke) 管道架构：

如 Figure 2 所示，ADP 将多对多转换简化为中心辐射式管道：

Table 1 列出了 ADP 所涵盖的现有智能体训练数据集概览：



### 5.1 ADP 架构

每个 ADP 标准化智能体轨迹表示为 **Trajectory** 对象，包含：
- **id**：轨迹标识符
- **content**：交替的动作和观察序列，表示智能体与用户/环境的交互
- **details**：灵活的元数据字典，用于存储数据集特定信息（如数据集源 URL）

**动作 (Actions)** 分为三类：
- **APIAction**：API 调用，包括工具名称、参数和结果
- **CodeAction**：代码执行，包括代码内容、语言和执行结果
- **MessageAction**：消息交互，包括用户消息和助手回复

**观察 (Observations)** 分为两类：
- **TextObservation**：文本观察，包括用户输入、环境输出等
- **WebObservation**：网页观察，包括 HTML、accessibility tree 和截图

### 5.2 转换管道

ADP 转换管道包含三个阶段：

1. **Raw to Standardized 转换器**：将原始数据集格式映射到 ADP 标准化模式，将数据集特定的动作和观察转换为 ADP 的标准动作和观察空间。

2. **Standardized to SFT 转换器**：将 ADP 标准化轨迹转换为特定智能体框架（如 OpenHands、SWE-Agent、AgentLab）的 SFT 格式，处理上下文管理、系统提示和对话格式化。

3. **质量保证模块**：通过自动化验证确保数据正确性和一致性，包括验证工具调用格式、确保工具调用与英文思考配对、检查对话是否正常结束等。

### 5.3 成本分析

无 ADP 时的转换成本：
$$Cost_{no-ADP}(A, D) ≈ A · Σ_{i=0}^D LOC_{i,Raw→ADP}$$

有 ADP 时的转换成本：
$$Cost_{ADP}(A, D) ≈ Σ_{i=0}^D LOC_{i,Raw→ADP} + Σ_{j=0}^A LOC_{ADP→SFT,j}$$

其中 D 为数据集数量，A 为智能体框架数量。ADP 将总成本从二次方 O(D × A) 降低为线性 O(D + A)。

### 5.4 数据采样

为平衡各领域数据，采用采样乘数公式：
$$m_d = \lceil w_d n_d \rceil$$

其中 w_d 是每个数据集的乘数，n_d 是原始轨迹数。若 w_d < 1 则无放回采样（降采样），若 w_d > 1 则有放回采样（升采样）。

Table 2 展示了 13 个 ADP 标准化数据集的统计信息和轨迹分析：



## 实验与关键发现

### 6.1 主要结果

ADP 微调在多个基准上带来显著性能提升。Table 3、Table 4 和 Table 5 分别展示了 7-8B、13-14B 和 32B 模型的结果：

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_tG6301ORHd_Agent_Data_Pr/figures/005_Table_3.jpg]]
*Table 3: Comparison of SOTA and our Best 7–8B ADP-trained agents’ results across benchmarks. Shaded rows are our ADP-tuned models. Other rows are collected from previous works.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_tG6301ORHd_Agent_Data_Pr/figures/006_Table_4.jpg]]
*Table 4: Comparison of SOTA and our Best 13–14B ADP-trained agents’ results across benchmarks. Shaded rows are our ADP-tuned models. Other rows are collected from previous works.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_tG6301ORHd_Agent_Data_Pr/figures/007_Table_5.jpg]]
*Table 5: Comparison of SOTA and our Best 32B ADP-trained agents’ results across benchmarks. Shaded rows are our ADP-tuned models. Other rows are collected from previous works.*

**7-8B 模型结果 (Table 3)**：

关键结果：
- **SWE-Bench (Verified)**：Qwen-2.5-7B-Coder-Instruct + SWE-Agent 从 0.4% 提升至 20.2% (+19.8%)
- **WebArena**：7B 模型从 4.5% 提升至 21.0% (+16.5%)
- **AgentBench OS**：7B 模型从 3.5% 提升至 27.1% (+23.6%)
- **GAIA**：7B 模型从 7.3% 提升至 9.1% (+1.8%)

**13-14B 模型结果 (Table 4)**：

关键结果：
- **SWE-Bench (Verified)**：Qwen-2.5-14B-Coder-Instruct + SWE-Agent 从 2.0% 提升至 34.4% (+32.4%)
- **WebArena**：14B 模型从 5.5% 提升至 22.2% (+16.7%)
- **AgentBench OS**：14B 模型从 2.8% 提升至 20.8% (+18.0%)

**32B 模型结果 (Table 5)**：

关键结果：
- **SWE-Bench (Verified)**：Qwen-2.5-32B-Coder-Instruct + SWE-Agent 从 2.2% 提升至 40.3% (+38.1%)
- **WebArena**：32B 模型从 10.9% 提升至 22.9% (+12.0%)
- **AgentBench OS**：32B 模型从 27.8% 提升至 34.7% (+6.9%)

Figure 3 和 Figure 4 展示了 ADP 微调在所有模型规模上带来一致的性能提升，且提升幅度随模型规模增大而保持单调增长：

### 6.2 跨任务迁移实验

Table 6 展示了跨任务迁移实验结果，ADP 多样化数据训练在目标任务上始终优于仅使用单一任务数据的微调：

关键结果：
- **SWE-Bench**：ADP 训练达到 10.4%，而仅使用 SWE-smith 数据仅为 1.0%
- **GAIA**：ADP 训练达到 9.1%，而仅使用 AgentInstruct 数据仅为 0.6%

### 6.3 等数据量比较

Table 10 展示了等数据量比较实验，证明 ADP 的优势来自数据多样性和统一结构而非数据量：

关键结果：
- **SWE-smith (升采样)**：11.0%
- **ADP**：16.6%

### 6.4 成本分析

Table 7 和 Table 8 展示了转换所需的代码行数 (LOC)：

ADP 格式平均每个数据集仅需 77 LOC，ADP→SFT 转换器平均每个框架仅需 1631 LOC。当扩展到 100 个智能体框架时，有 ADP 的总成本约为 12,592 LOC，而无 ADP 的成本约为 489,200 LOC。

### 6.5 数据采样乘数

Table 9 展示了每个数据集的采样乘数 w_d：

### 6.6 公平性说明

- 所有实验均使用相同的基座模型 Qwen2.5-Coder-Instruct 和相同的 LLaMA-Factory SFT 管道进行微调，确保公平比较。
- 跨任务迁移实验中，ADP 训练和单任务训练使用相同的数据规模（约 30K 样本），以排除数据量差异的影响。
- 对于不同的智能体框架（OpenHands CodeActAgent、SWE-Agent、AgentLab），根据其评估重点使用了不同的数据子集（非网页部分或仅网页部分），以确保训练数据与评估任务的相关性。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_tG6301ORHd_Agent_Data_Pr/figures/002_Table_1.jpg]]
*Table 1: Overview of Existing Agent Training Datasets. C=Coding, S=Software Engineering, T=API/Tool Use, W=Web Browsing.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_tG6301ORHd_Agent_Data_Pr/figures/004_Table_2.jpg]]
*Table 2: Dataset Stats and Trajectory Analysis. A=APIAction, C=CodeAction, M=MessageAction.*



## 定位与知识库关联

ADP 属于智能体数据标准化与统一训练方法谱系。与现有方法的关系如下：

- **AgentInstruct (Zeng et al., 2023)**：合成智能体数据集，覆盖 API/工具使用、编码和网页浏览，但格式异构
- **SWE-Gym (Pan et al., 2025)** 和 **SWE-smith (Yang et al., 2025b)**：软件工程领域的智能体 rollout 数据，格式特定
- **Mind2Web (Deng et al., 2023)**：网页浏览领域的手工演示数据，使用 HTML 格式
- **CodeActInstruct**：编码领域的智能体交互数据，使用代码执行格式

ADP 的创新在于提供了一种轻量级“中间语言”，将上述异构数据统一为标准化格式，同时保持数据来源和语义结构。与 Agent-FLAN (Chen et al., 2024) 和 AgentTuning (Zeng et al., 2023) 等专注于特定数据设计的方法不同，ADP 关注的是数据格式的标准化和转换效率，而非数据生成方法本身。

ADP 的局限性包括：
- 当前设计主要关注动作和观察的标准化，对于更复杂的智能体交互模式（如多智能体协作、长期记忆管理）的支持尚不明确
- ADP Dataset V1 的质量受限于原始数据集的质量，特别是合成数据和 rollout 数据可能存在噪声和偏差
- 实验主要基于 Qwen2.5-Coder-Instruct 模型系列，在其他基座模型上的泛化效果有待进一步验证
- 对于网页浏览任务，标准化可能带来信息损失

Table 11 列出了 ADP 所用数据集的许可信息：



## 原文 PDF

![[paperPDFs/ICLR_2026/Agent_Data_Protocol_Unifying_Datasets_for_Diverse_Effective_Fine_tuning_of_LLM_Agents.pdf]]
