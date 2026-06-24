---
title: "Multi-View Encoders for Performance Prediction in LLM-Based Agentic Workflows"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Multi_View_Encoders_for_Performance_Prediction_in_LLM_Based_Agentic_Workflows.pdf
openreview_forum_id: 7oeKDZsmWp
aliases:
- AP
- MVEPPLBAW
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "工作流的多视图表示（图结构、代码语义、提示文本）与跨领域无监督预训练（对比学习配合重建）相结合，能够捕获异构信号并显著降低对标注数据的依赖，是提升预测准确性与泛化能力的关键手段。"
primary_logic: "通过将图、代码和提示融合为统一表示，并利用跨领域无监督预训练学习通用工作流先验，可以在标签极为有限的情况下实现准确的性能预测，从而大幅降低对昂贵试错评估的需求，加速智能体工作流的搜索与优化。"
claims:
- "多视图编码（图、代码、提示）在所有任务中均优于任何单视图表示；消融实验中三视图组合取得最高平均准确率84.38%和实用率81.88%。"
- "跨域无监督预训练（Agentic Predictor+）在标签稀缺场景下效果显著，在所有标签比例下均优于基线，在10%标签时准确率仍高于73%。"
- "预测器可实现与真实执行评估相当的工作流优化性能，同时将搜索成本从$39.83降至0，平均优化得分74.43，高于随机（62.56）、GCN（68.42）和GAT（71.00）。"
- "Overall Average (Code+Math+Reason across GD and AF) 上 Accuracy = 79.97"
---

# Multi-View Encoders for Performance Prediction in LLM-Based Agentic Workflows

> [!tip] 核心洞察
> 通过将图、代码和提示融合为统一表示，并利用跨领域无监督预训练学习通用工作流先验，可以在标签极为有限的情况下实现准确的性能预测，从而大幅降低对昂贵试错评估的需求，加速智能体工作流的搜索与优化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于多视图编码器的LLM智能体工作流性能预测 |
| 英文题名 | Multi-View Encoders for Performance Prediction in LLM-Based Agentic Workflows |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7oeKDZsmWp) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Agentic Predictor |
| Dataset | Overall Average (Code+Math+Reason across GD and AF), Overall Average (same), Workflow Optimization (Average over MATH, GSM8K, MBPP, HumanEval, MMLU) |

> [!tip] 效果简介
> - Overall Average (Code+Math+Reason across GD and AF) 上，Accuracy 为 79.97，对比 78.36 (best baseline, likely One For All)，变化 +1.61 (+2.05%)。
> - Overall Average (same) 上，Utility 为 76.33，对比 73.54 (best baseline)，变化 +2.79 (+3.79%)。
> - Workflow Optimization (Average over MATH, GSM8K, MBPP, HumanEval, MMLU) 上，Accuracy (optimized workflow score) 为 74.43，对比 Random 62.56 / GCN 68.42 / GAT 71.00，变化 vs Random +11.87, vs GCN +6.01, vs GAT +3.43。

## 概述

**核心问题**：LLM 驱动的智能体工作流（agentic workflow）由多个智能体通过有向无环图组织协作，其最终执行性能高度依赖工作流的结构设计、代码实现与提示词配置。然而，获取真实性能标签（如任务成功率）需要反复调用 LLM 进行昂贵评估，导致标注数据极为稀缺。在此设定下，构建一个通用且可靠的性能预测器，以替代高成本的试错执行，成为关键瓶颈。

**核心方法**：本文提出 **Agentic Predictor**，通过**多视图工作流编码器**将图结构、代码语义与系统提示文本融合为统一潜在表示，并引入**跨领域无监督预训练**（对比学习配合多模态重建）来学习通用工作流先验，从而在标签极为有限的情况下实现准确预测。其变体 Agentic Predictor+ 进一步利用大量未标注的异构工作流进行预训练，显著降低对标注数据的依赖。

**核心结论**：
- 在 FLORA-Bench 基准上，Agentic Predictor 相较最强基线平均准确率提升 **2.05%**（79.97 vs. 78.36），实用率提升 **3.79%**（76.33 vs. 73.54）。
- 消融实验证实，三视图组合（图+代码+提示）取得最高平均准确率 **84.38%** 和实用率 **81.88%**，多图视图进一步带来增益。
- 在标签比例仅 **10%** 的极端稀缺场景下，Agentic Predictor+ 的准确率仍高于 **73%**，比所有基线高出逾 10 个百分点。
- 预测器推理仅需 **0.054 ms/样本**，比 LLM 调用快约 4 万倍，且在工作流优化任务中可实现与真实执行评估相当的优化质量（平均优化得分 **74.43**），同时将搜索成本从 $39.83 降至零。

**方法定位**：Agentic Predictor 属于轻量级预测器，区别于基于 LLM 推理或单视图图神经网络的传统方案。其多视图编码与无监督预训练策略使其在标注稀缺、工作流异构的设定下具备显著优势，并可嵌入任意搜索算法以加速智能体工作流的自动优化。

## 背景与动机

### 问题背景：LLM智能体工作流的性能预测困境

基于大语言模型（LLM）的智能体工作流（agentic workflows）通过编排多个LLM调用、工具使用和结构化推理步骤，在代码生成、数学推理和常识问答等复杂任务中展现出显著优势。然而，设计高性能的工作流配置高度依赖反复试错：开发者需要不断调整智能体拓扑、提示词和代码逻辑，并通过昂贵的实际执行来评估每次修改的效果。

这一过程中，**性能标注数据的获取成本极高**。每次评估都需要调用大规模LLM（如GPT-4）执行完整工作流，不仅消耗大量API费用和时间，还难以规模化。以FLORA-Bench基准为例，单次真实执行评估的搜索成本可达$39.83，而实际工作流优化往往需要评估数百甚至数千个候选配置。这种“执行即标注”的范式构成了智能体工作流搜索与优化的核心瓶颈。

### 现有方法的缺口

当前面向智能体工作流的性能预测方法存在三个关键局限：

**第一，表示能力不足。** 现有方法（如G-Designer、AFlow）主要将工作流建模为单一图结构，仅捕获智能体之间的拓扑连接关系。然而，智能体工作流的性能同时取决于代码实现中的控制流逻辑、工具调用模式，以及系统提示中的角色定义和行为规范。单视图图表示无法编码这些异构信号，导致预测器难以区分结构相似但语义迥异的工作流配置。

**第二，标注依赖过强。** 主流基线方法（MLP、GCN、GAT、GCN-II、Graph Transformer、Dir-GNN等）均依赖监督学习，需要大量带标注的（工作流，性能）对进行训练。在标注数据稀缺的现实场景下（例如仅有10%的工作流经过真实执行评估），这些方法的预测准确率急剧下降，难以支撑可靠的工作流筛选。

**第三，跨任务泛化能力弱。** 不同领域（如代码生成、数学推理）的工作流在结构和语义上差异显著，现有方法通常为每个任务独立训练预测器，无法利用跨领域的未标注工作流数据学习通用的性能表征先验，限制了在数据稀疏任务上的表现。

### 核心动机与研究定位

本文的核心动机在于：**能否构建一个预测器，在仅需极少标注数据的情况下，准确估计智能体工作流的执行性能，从而替代昂贵的真实执行评估？**

为实现这一目标，我们提出**Agentic Predictor**框架，其设计围绕两个关键洞察：

- **多视图编码**：将智能体工作流从图结构、代码语义和提示文本三个互补视角联合编码为统一表示，捕获异构信号的全貌。
- **跨领域无监督预训练**：利用大量未标注的跨任务工作流数据，通过对比学习和多模态重建预训练编码器，学习通用的工作流表征先验，从而在标注数据极为有限时仍能实现可靠的性能预测。

这一方法定位在现有工作（如FLORA-Bench的One For All统一预测器）的基础上，首次将多视图表示学习与无监督预训练引入智能体工作流性能预测任务，旨在从根本上缓解标注稀缺带来的预测困难，并为预测器引导的工作流搜索与优化奠定基础。

## 核心创新

### 问题瓶颈

LLM驱动的智能体工作流性能预测面临双重挑战：**工作流本身具有高度异质性**——不同任务（代码生成、数学推理、常识问答）的工作流在图拓扑、代码实现、提示设计上差异巨大；同时，**性能标注数据极其昂贵**，每次评估都需要调用LLM完整执行工作流，导致标注样本稀缺。这两者叠加，使得构建通用且可靠的性能预测器成为难题。

### 关键因果机制

Agentic Predictor 的核心创新可概括为 **“多视图融合捕获异构信号，跨域预训练缓解标注稀缺”**：

1. **多视图编码（Multi-View Encoding）**：将智能体工作流从三个互补视角——**图结构**（代理拓扑与数据流）、**代码语义**（控制逻辑与工具调用模式）、**提示文本**（角色规范与行为约束）——联合编码为统一潜在表示。这改变了基线方法仅依赖单一图视图的局限，使模型能够捕获结构、行为、语义三个维度的信号。

2. **跨域无监督预训练（Cross-Domain Unsupervised Pretraining）**：在大量未标注的跨领域工作流上，通过**重建损失**（迫使编码器保留各模态的关键信息）与**跨模态对比损失**（拉近同一工作流不同视图的表示，推远不同工作流的表示）联合训练编码器。这使模型在接触任何性能标签之前就已习得通用工作流先验，大幅降低了对标注数据的依赖。

3. **轻量预测器与任务注入**：将预训练编码器产出的工作流嵌入与任务描述嵌入拼接，送入轻量MLP预测头，实现毫秒级推理。

### 与基线的关键差异（Changed Slots）

| 维度 | 基线方法 | Agentic Predictor |
|------|----------|-------------------|
| **工作流表示** | 单视图图（仅结构信息） | 多视图编码（图结构 + 代码语义 + 提示文本） |
| **预训练策略** | 无预训练或仅监督微调 | 跨域无监督预训练（对比学习 + 重建） |
| **图建模粒度** | 单一共享图 | 多图视图（提示图、代码图、运算符图） |
| **任务集成** | 仅工作流特征 | 工作流表示与任务嵌入拼接 F=[Z, T] |
| **预测效率** | 可能需要LLM推理 | 轻量MLP头，推理仅 0.054 ms/样本 |

### 关键证据强度

- **多视图消融**（Table 4）：三视图组合（代码+图+文本）取得最高平均准确率 **84.38%** 和实用率 **81.88%**，显著优于任何单视图或双视图组合，置信度高。
- **预训练效果**（Figure 3）：Agentic Predictor+ 在所有标签比例下均优于全部基线，在仅 **10% 标签**时准确率仍高于 73%，比基线高出超 10 个百分点，置信度高。
- **搜索成本归零**（Table 13）：预测器引导的优化平均得分 **74.43**，显著高于随机（62.56）、GCN（68.42）和 GAT（71.00），同时将搜索成本从真实的 **$39.83 降至 0**，置信度高。

### 局限与待验证点

- 当前仅在 FLORA-Bench 基准上验证，**实际部署中的工作流多样性可能超出覆盖范围**。
- 预测器针对二元成功/失败建模，**对连续性能评分的细粒度捕获能力有限**。
- 跨域预训练依赖大量未标注异构工作流，**并非所有领域都能轻松获取此类数据**。
- 在 HotpotQA 等复杂多跳推理任务上，**迁移表现低于部分基线**，原因待进一步分析。

## 整体框架

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/003_Figure_2.jpg]]
*Figure 2: Overview of our Agentic Predictor framework. A (a) multi-view workflow encoder is designed to encode a set of agentic workflows from graph, code, and prompt aspects into unified representations, which serve as features for training the predictor. In the (b) pretraining phase, the encoder learns these representations on unlabeled workflows spanning diverse tasks and domains, using cross-domain unsupervised pretraining objectives. In the (c) predictor-guided search phase, a performance predictor is trained on a small (workflow configuration, performance) dataset to classify configurations as pass or fail, and subsequently guides the search toward promising configurations*

Agentic Predictor 的整体框架围绕一个核心洞察展开：LLM 驱动的智能体工作流具有高度异质性，其图结构、代码实现和提示文本各自承载互补的语义信号，而性能标注数据（如执行成功率）的获取依赖昂贵的 LLM 评估，导致标注极为稀缺。为解决这一瓶颈，Agentic Predictor 通过**多视图编码**将异构信号融合为统一表示，并借助**跨领域无监督预训练**学习通用工作流先验，从而在标签极为有限的条件下实现准确的性能预测。

### 框架总览

如图 Figure 2 所示，框架由三个关键阶段构成：

1.  **多视图工作流编码器（Multi-View Workflow Encoder）**：将每个智能体工作流 $\mathcal{W} = \{\mathcal{V}, \mathcal{E}, \mathcal{P}, \mathcal{C}\}$ 从**图结构**（智能体拓扑与数据流）、**代码语义**（控制逻辑与工具使用模式）和**提示文本**（角色规范与行为约束）三个视角编码为统一的潜在表示 $\mathbf{Z}$。
2.  **跨领域无监督预训练（Pretraining Phase）**：在大量未标注的异构工作流上，通过**重建损失** $\mathcal{L}_{rec}$ 和**跨模态对比损失** $\mathcal{L}_{con}$ 联合训练编码器-解码器网络，使编码器学习到捕获工作流通用模式的表示，从而大幅降低对下游标注数据的依赖。
3.  **预测器引导的搜索（Predictor-Guided Search）**：在有限的标注数据上训练一个轻量级预测头（MLP），以工作流表示 $\mathbf{Z}$ 与任务嵌入 $\mathbf{T}$ 的拼接 $\mathcal{F} = [\mathbf{Z}, \mathbf{T}]$ 为输入，估计工作流在给定任务上的成功概率 $\hat{e}$，并以极低的计算成本（0.054 ms/样本）替代昂贵的 LLM 试错评估，加速工作流搜索与优化。

### 模块关系与数据流

框架的核心是**多视图编码器**，其内部由三个专用编码器和一个聚合层组成：

-   **图编码器（Graph Encoder）**：采用多图策略，为同一拓扑构建**提示图**、**代码图**和**运算符图**三种视图，通过 GNN 提取节点特征后，依次施加**跨视图自注意力**（CrossGraphAttn）和**视图注意力池化**（ViewAttnPool），最终经图读出得到图表示 $\mathbf{Z}_{\mathcal{G}}$。
-   **代码编码器（Code Encoder）**：使用 $L$ 层 MLP 对工作流代码的全局嵌入进行编码，得到代码表示 $\mathbf{Z}_{\mathcal{C}} = \text{MLP}_{\mathcal{C}}(\mathcal{C})$。
-   **提示编码器（Prompt Encoder）**：使用 $L$ 层 MLP 对全部系统提示的嵌入进行编码，得到提示表示 $\mathbf{Z}_{\mathcal{P}} = \text{MLP}_{\mathcal{P}}(\mathcal{P})$。

三个视图的表示随后被拼接并通过一个聚合 MLP 融合为最终的潜在表示：

$$\mathbf{Z} = \text{MLP}([\mathbf{Z}_{\mathcal{G}}, \mathbf{Z}_{\mathcal{C}}, \mathbf{Z}_{\mathcal{P}}])$$

在**预训练阶段**，解码器网络从 $\mathbf{Z}$ 重建各模态的嵌入 $\hat{\mathcal{G}}, \hat{\mathcal{C}}, \hat{\mathcal{P}}$，与原始嵌入计算均方误差作为重建损失；同时，以同一工作流的不同视图对为正样本、同批次其他工作流为负样本，计算跨模态对比损失。总损失为两者之和：

$$\mathcal{L}_{enc} = \mathcal{L}_{rec} + \mathcal{L}_{con}$$

预训练完成后，解码器被丢弃，编码器参数被冻结或微调。在**预测阶段**，任务编码器将自然语言任务描述编码为嵌入 $\mathbf{T}$，与工作流表示 $\mathbf{Z}$ 拼接形成联合表示 $\mathcal{F}$，送入轻量级预测头 $\mathcal{M}_{\Theta}$ 进行二元成功/失败分类，损失函数为标准二元交叉熵：

$$\mathcal{L}_{pred} = -\frac{1}{N}\sum_{i=1}^{N}[e_i\log\hat{e}_i + (1-e_i)\log(1-\hat{e}_i)]$$

### 框架特性

与现有预测框架相比，Agentic Predictor 在四个维度上具有独特优势（Table 1）：同时具备多视图表示、无监督预训练、轻量级预测器和搜索算法无关性。消融实验证实，三视图组合（代码+图+提示）在所有任务中均优于任何单视图或双视图组合（Table 4），而跨域无监督预训练策略使模型在仅使用 10% 标注数据时，准确率仍高于 73%，比所有基线高出超过 10 个百分点（Figure 3）。

## 核心模块与公式推导

### 问题形式化

智能体工作流被定义为一个有向无环图 $\mathcal{W} = \{\mathcal{V}, \mathcal{E}, \mathcal{P}, \mathcal{C}\}$，其中 $\mathcal{V}$ 为智能体节点集，$\mathcal{E}$ 为通信边集，$\mathcal{P}$ 为各节点的系统提示集，$\mathcal{C}$ 为各节点的代码实现集。给定任务描述 $T$，目标是学习一个预测模型 $\mathcal{M}_\Theta$，在不调用LLM的情况下估计工作流在任务上的执行性能 $e$（如成功/失败）。学习目标为最小化期望损失：

$$\min_{\Theta} \mathbb{E}_{(\mathcal{W},T)} [\mathcal{L}(e, \hat{e})]$$

### 多视图工作流编码器

编码器从三个互补视角捕获工作流的异构信号，最终融合为统一潜在表示 $\mathbf{Z}$。

**图编码器** 采用多图方法，在同一节点集和边集上构建提示图、代码图和运算符图三种视图。节点嵌入经跨视图自注意力（CrossGraphAttn）和视图注意力池化（ViewAttnPool）后，通过图读出得到图表示：

$$\mathbf{Z}_{\mathcal{G}} = G_{\text{pool}}(\text{ViewAttnPool}(\text{CrossGraphAttn}(\mathbf{X})))$$

**代码编码器** 通过 $L$ 层MLP提取整个工作流代码的全局语义、控制逻辑和工具使用模式：

$$\mathbf{Z}_{\mathcal{C}} = \text{MLP}_{\mathcal{C}}(\mathcal{C})$$

**提示编码器** 同样通过 $L$ 层MLP编码系统提示中的角色规范和行为约束：

$$\mathbf{Z}_{\mathcal{P}} = \text{MLP}_{\mathcal{P}}(\mathcal{P})$$

**聚合层** 将三个视图的表示拼接后经MLP融合为最终潜在表示：

$$\mathbf{Z} = \text{MLP}([\mathbf{Z}_{\mathcal{G}}, \mathbf{Z}_{\mathcal{C}}, \mathbf{Z}_{\mathcal{P}}])$$

消融实验证实，三视图组合（代码+图+文本）在所有任务中均优于任何单视图或双视图变体，取得最高平均准确率84.38%和实用率81.88%（Table 4）；多图视图相比单图进一步提升准确率，尤其在代码生成任务中（84.44% vs. 82.58%，Table 5）。

### 跨领域无监督预训练

为解决性能标注稀缺问题，编码器在大量未标注的跨领域工作流上进行无监督预训练。预训练包含两个目标：

**重建损失** 要求解码器从潜在表示 $\mathbf{Z}$ 重建各模态嵌入：

$$\mathcal{L}_{rec} = \frac{1}{M}\sum_{i=1}^{M}\left[\|\mathcal{G}_i - \hat{\mathcal{G}}_i\|^2 + \|\mathcal{C}_i - \hat{\mathcal{C}}_i\|^2 + \|\mathcal{P}_i - \hat{\mathcal{P}}_i\|^2\right]$$

**对比损失** 以同一工作流的不同视图为正样本，同批次其他工作流为负样本，在 $(\mathcal{G},\mathcal{C})$、$(\mathcal{G},\mathcal{P})$、$(\mathcal{C},\mathcal{P})$ 三对视图上对称计算：

$$\mathcal{L}_{con} = \frac{1}{M}\sum_{i=1}^{M} -\log \frac{\exp(\text{sim}(\mathbf{Z}_i, \mathbf{Z}_j^{+})/\tau)}{\sum_{k=1}^{M}\exp(\text{sim}(\mathbf{Z}_i, \mathbf{Z}_k)/\tau)}$$

**编码器总损失** 为两者之和：

$$\mathcal{L}_{enc} = \mathcal{L}_{rec} + \mathcal{L}_{con}$$

预训练后的模型（Agentic Predictor+）在标签稀缺场景下效果显著：在所有标签比例下均优于基线，在仅10%标签时准确率仍高于73%，比所有基线高出超过10个百分点（Figure 3）。

### 性能预测器

预测阶段，将工作流嵌入 $\mathbf{Z}$ 与任务嵌入 $\mathbf{T}$ 拼接形成联合表示：

$$\mathcal{F} = [\mathbf{Z}, \mathbf{T}]$$

预测头采用轻量级MLP，推理时间仅0.054 ms/样本（Table 6）。对于二元成功/失败标签，使用交叉熵损失：

$$\mathcal{L}_{pred} = -\frac{1}{N}\sum_{i=1}^{N}[e_i\log\hat{e}_i + (1-e_i)\log(1-\hat{e}_i)]$$

对于连续性能评分，则使用均方误差损失。

## 实验与分析

### 核心瓶颈与验证逻辑

LLM智能体工作流性能预测的核心瓶颈在于：工作流本身具有高度异质性（图结构、代码实现、提示文本差异极大），而获取可靠的性能标注（如执行成功率）需要昂贵的LLM评估，导致标注数据严重稀缺。Agentic Predictor通过两个关键机制应对这一挑战：**多视图编码**将图结构、代码语义和提示文本融合为统一表示，捕获异构信号；**跨领域无监督预训练**（对比学习+重建）利用大量未标注工作流学习通用先验，大幅降低对标注数据的依赖。实验设计围绕三个核心问题展开：(1) 多视图融合是否优于单视图？(2) 无监督预训练在标签稀缺场景下是否有效？(3) 预测器能否替代真实执行评估来优化工作流？

---

### 主要结果：多视图编码与预训练的协同优势

**Table 3** 展示了Agentic Predictor与7个基线方法在FLORA-Bench上的全面对比。基线包括MLP、GCN、GAT、GCN-II、Graph Transformer、Dir-GNN等图神经网络方法，以及统一多任务预测框架**One For All**（Zhang et al., 2025c）。Agentic Predictor在所有任务领域（代码生成、数学问题、常识推理）和两个工作流生成系统（G-Designer和AFlow）上均取得最优或次优结果：

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/005_Table_3.jpg]]
*Table 3: Performance comparison between Agentic Predictor and baselines. The best and second-best results are highlighted in bold and underlined, respectively. GD is G-Designer, and AF is AFlow*

- **平均准确率**：79.97%，较最佳基线（78.36%）提升**+1.61个百分点（+2.05%）**。
- **平均实用率**：76.33%，较最佳基线（73.54%）提升**+2.79个百分点（+3.79%）**。

实用率衡量的是预测排名前k的工作流与真实高排名工作流的重叠程度，该指标的提升表明Agentic Predictor不仅能准确判断单个工作流的成败，还能有效区分工作流之间的相对优劣——这对于后续的搜索优化至关重要。值得注意的是，One For All作为统一多任务预测框架表现强劲，但Agentic Predictor的多视图编码和预训练策略仍带来一致且显著的增益，验证了方法设计的有效性。

---

### 消融实验：多视图融合的决定性作用

**Table 4** 的输入视图消融实验是全文最具决定性的证据。实验比较了7种视图组合（仅代码、仅图、仅文本、代码+图、代码+文本、图+文本、代码+图+文本）：

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/006_Table_4.jpg]]
*Table 4: Results of ablation study on different input view variations*

- **三视图组合（代码+图+文本）取得最高平均准确率84.38%和实用率81.88%**，显著优于任何单视图或双视图组合。
- 单视图表现中，**代码视图**单独使用时准确率最高（82.08%），说明代码语义是性能预测的最强单信号；图视图次之（79.89%），文本视图最弱（78.46%）。
- 双视图组合中，**代码+图**（83.93%）优于**代码+文本**（82.78%）和**图+文本**（80.50%），表明结构信息与语义信息的互补性最强。

这一结果直接验证了核心假设：智能体工作流的异构性使得任何单一视图都难以完整表征其性能潜力，多视图融合是必要的。

**Table 5** 进一步消融了图视图的内部设计。Agentic Predictor采用多图方法，分别为提示、代码和运算符构建独立的图视图（共享节点和边集），而非使用单一共享图。实验表明：

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/007_Table_5.jpg]]
*Table 5: Results of ablation study on different input graph variations*

- **多图视图在所有任务上均优于单图**，在代码生成任务上尤为显著（准确率84.44% vs. 82.58%，提升+1.86个百分点）。
- 这验证了不同类型边（提示语义边、代码调用边、运算符数据流边）承载不同性质的交互信息，分开建模有助于GNN捕获更丰富的结构模式。

---

### 标签效率：无监督预训练的关键价值

**Figure 3** 展示了在不同标签比例（10%至100%）下，Agentic Predictor与基线的准确率对比。这是验证预训练策略有效性的核心证据：

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/008_Figure_3.jpg]]
*Figure 3: Accuracy comparison between Agentic Predictor and the baselines across varying label ratios*

- **Agentic Predictor+（含预训练）在所有标签比例下均一致优于所有基线**。
- 在**10%标签**的极端稀缺场景下，Agentic Predictor+的准确率仍**高于73%**，比最佳基线高出超过10个百分点。
- 随着标签比例增加，所有方法的性能均提升，但Agentic Predictor+的优势保持稳定，表明预训练学到的通用工作流先验具有持久的价值。

这一结果直接回应了标注稀缺这一核心瓶颈：跨领域无监督预训练通过重建损失和跨模态对比损失，从未标注的异构工作流中提取了可迁移的结构和语义模式，使得下游预测器仅需极少标注即可达到实用水平。

---

### 计算效率：从LLM调用到轻量预测的跨越

**Table 6** 的计算成本对比揭示了Agentic Predictor的工程价值：

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/009_Table_6.jpg]]
*Table 6: Computation cost comparison*

- **推理时间**：Agentic Predictor仅需**0.054 ms/样本**，而LLM预测（如GPT-4.1）需要约2秒/样本（按API调用估算），**速度提升约4万倍**。
- **训练成本**：Agentic Predictor的训练时间约为0.195–6.140秒/epoch（取决于GNN骨干），显存占用仅0.033–0.087 GB，可在单GPU上轻松完成。
- **搜索成本**：在后续的工作流优化实验中（Table 13），使用预测器替代真实执行评估，将搜索成本从**$39.83降至0**。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/024_Table_13.jpg]]
*Table 13: Workflow optimization performance based on the selected workflow across methods*

这种效率优势使得Agentic Predictor可以嵌入到需要大量候选评估的工作流搜索和优化流程中，而不会产生高昂的LLM调用成本。

---

### 鲁棒性分析：编码器无关的框架设计

**Table 8** 展示了Agentic Predictor在不同GNN骨干（GCN、GAT、GCN-II、Graph Transformer、Dir-GNN）下的表现。结果表明：

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/011_Table_8.jpg]]
*Table 8: Results on different GNN backbones of Agentic Predictor*

- **所有GNN骨干的预测准确率差异很小**，验证了多视图编码框架的编码器无关性。
- 这意味着Agentic Predictor可以灵活适配不同的图神经网络架构，其性能增益主要来自多视图融合和预训练策略，而非特定的GNN设计。

**Table 7** 进一步测试了不同LLM骨干（GPT-4.1、Claude 4 Sonnet、Gemini 2.5 Flash）驱动的智能体工作流上的预测性能。Agentic Predictor在不同LLM骨干间表现稳定，表明其学到的表示具有跨LLM的泛化能力。

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/010_Table_7.jpg]]
*Table 7: Results on different backbones driven agentic workflows*

---

### 工作流优化：预测器替代真实评估的可行性

**Table 13** 是最具应用价值的实验结果。实验设置如下：在AFlow生成的候选工作流池中，使用不同方法（随机选择、GCN预测器、GAT预测器、Agentic Predictor）选择最优工作流，并与真实执行评估选出的最优工作流（Ground Truth）对比：

- **Agentic Predictor的平均优化得分74.43**，显著高于随机选择（62.56）、GCN（68.42）和GAT（71.00）。
- 在数学问题（MATH、GSM8K）和代码生成（MBPP、HumanEval）任务上，Agentic Predictor选出的工作流性能接近Ground Truth。
- **搜索成本为零**（仅需预测器推理），而Ground Truth需要$39.83的LLM评估成本。

这一结果直接证明了核心主张：**预测器可以替代昂贵的真实执行评估来指导工作流搜索，在显著降低成本的同时保持优化质量**。

---

### 失败模式与局限性

尽管整体表现优异，实验也揭示了若干值得关注的失败模式：

1. **HotpotQA上的低迁移表现**：在跨领域OOD测试（Table 12）中，Agentic Predictor在HotpotQA（多跳推理）上的准确率仅为13.37%，低于某些基线方法。这可能是因为多跳推理工作流的结构和语义模式与预训练数据中的其他推理任务差异过大，预训练先验未能有效迁移。具体原因需要进一步分析。

2. **跨系统OOD的波动**：在AFlow上训练、G-Designer上测试（Table 10）和反向设置（Table 11）中，Agentic Predictor的表现优于基线但仍存在一定性能下降，表明不同工作流生成系统产生的候选分布差异对预测器构成挑战。

3. **二元预测的粒度限制**：当前预测器主要针对二元成功/失败设定，对连续性能评分（如准确率数值）的建模能力有限。这可能在需要精细区分工作流质量的场景中丢失信息。

4. **静态文本嵌入的局限**：任务编码器和提示编码器使用静态预训练语言模型（T5、BERT）提取特征，未利用执行过程中的动态追踪或工具调用日志，可能遗漏运行时行为模式。

---

### 开放问题

基于上述分析，以下问题值得后续探索：

- 如何将Agentic Predictor扩展至多目标优化（如同时平衡准确率与推理成本）？
- 纳入执行时间追踪、工具调用日志等动态信息能否进一步提升预测精度，特别是在HotpotQA等复杂推理任务上？
- 预测器引导的搜索能否与蒙特卡洛树搜索或进化算法结合，提升优化质量？
- 不同预训练语言模型（T5 vs. BERT）的选择对任务编码器的影响机制是什么？

### 补充图表

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/002_Table_1.jpg]]
*Table 1: Comparison between ours and existing frameworks for prediction-based workflow generation*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/004_Table_2.jpg]]
*Table 2: Summary of benchmark statistics*

![[assets/figures/papers/paper_list_l41_https_openreview_net_forum_id_7oeKDZsmWp/figures/012_Table_9.jpg]]
*Table 9: Comparison between Agentic Predictor and LLM-based few-show classification*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

Agentic Predictor 并非在真空中提出，而是针对现有智能体工作流性能预测方法的两大结构性缺陷——**表示单一化**与**标注依赖**——进行系统性改进。表1（Table 1）明确对比了其与 MAS-GPT、FLORA-Bench 等框架的差异：Agentic Predictor 是唯一同时具备多视图表示、无监督预训练、轻量预测器和搜索算法无关性的方案。

具体而言，基线方法可划分为两个技术代际：

**第一代：基于图结构的方法。** MLP、GCN、GAT、GCN-II、Graph Transformer、Dir-GNN 等基线（Table 3）仅利用工作流的图拓扑信息进行预测，完全忽略了代码语义和提示文本中蕴含的丰富信号。这些方法在标注充足时表现尚可，但面对标签稀缺场景时性能急剧退化（Figure 3），其根本瓶颈在于**单视图表示无法捕获工作流的异质性特征**。

**第二代：统一多任务预测方法。** One For All（Zhang et al., 2025c）作为 FLORA-Bench 中的最强基线，试图通过统一架构处理多任务预测，但其仍然依赖单视图图表示，且缺乏无监督预训练机制。Table 3 显示，Agentic Predictor 在平均准确率上超越 One For All 达 1.61 个百分点（79.97% vs. 78.36%），在实用率上领先 2.79 个百分点（76.33% vs. 73.54%），证明多视图编码与预训练的组合带来了实质性的增益。

**与基于LLM的预测方法的关系。** Table 9 对比了 Agentic Predictor 与 GPT-4.1、Claude 4 Sonnet、Gemini 2.5 Flash 等LLM的少样本分类性能。LLM预测器虽然在部分任务上表现可接受，但其推理成本高昂（单次调用约 $0.01–$0.05），且无法在搜索循环中规模化使用。Agentic Predictor 的推理时间仅为 0.054 ms/样本（Table 6），比LLM推理快约 4 万倍，同时避免了API调用费用，使其在实际工作流优化中具备可部署性。

### 2. 核心改进槽位

Agentic Predictor 相对于基线的方法论改进可归纳为五个关键槽位：

| 改进槽位 | 基线取值 | Agentic Predictor 取值 | 证据锚点 |
|---------|---------|----------------------|---------|
| 工作流表示 | 单视图图（仅结构） | 多视图编码（图结构 + 代码语义 + 提示文本） | Table 4：三视图组合准确率 84.38%，显著优于任何单视图 |
| 预训练策略 | 无预训练或仅监督微调 | 跨领域无监督预训练（对比学习 + 重建） | Figure 3：10% 标签下准确率仍高于 73%，领先基线超 10 个百分点 |
| 图建模粒度 | 单一共享图 | 多图视图（提示图、代码图、运算符图） | Table 5：多图在代码生成任务上准确率 84.44% vs. 单图 82.58% |
| 任务集成方式 | 仅工作流特征 | 工作流表示与任务嵌入拼接 $\mathcal{F} = [\mathbf{Z}, \mathbf{T}]$ | Section 3.5 |
| 预测效率 | 需LLM推理或高计算开销 | 轻量级MLP预测头，推理 0.054 ms/样本 | Table 6 |

这些改进槽位之间存在**因果协同关系**：多视图编码提供了更丰富的输入信号，但同时也增加了模型对标注数据的需求——这正是跨领域无监督预训练所要解决的核心矛盾。预训练通过重建损失 $\mathcal{L}_{rec}$ 和跨模态对比损失 $\mathcal{L}_{con}$（Section 3.4）在未标注数据上学习通用工作流先验，使得下游预测器在仅需极少标注的情况下即可达到竞争性性能。

### 3. 适用边界

**已知有效场景：**
- 二元成功/失败预测：Agentic Predictor 的设计核心是分类预测头配合二元交叉熵损失 $\mathcal{L}_{pred}$（Section 3.5），在 FLORA-Bench 的代码生成、数学推理和常识推理三大领域均表现优异。
- 标签稀缺场景：跨领域无监督预训练（Agentic Predictor+）在 10%–50% 标签比例下持续优于所有基线（Figure 3），证明其在标注成本高昂的现实场景中具有实用价值。
- 工作流优化：Table 13 表明预测器引导的搜索可在零搜索成本下达到平均优化得分 74.43，优于随机搜索（62.56）和基于GNN的预测器（GCN 68.42, GAT 71.00）。
- GNN骨架鲁棒性：Table 8 显示多视图编码器对 GCN、GAT、GCN-II、Graph Transformer、Dir-GNN 等不同GNN骨架均表现稳定，性能差异很小。

**已知局限与失效模式：**
- 连续性能评分的建模能力有限：当前预测器主要针对二元成功/失败设定，对任务准确率等细粒度连续指标的预测未做深入探索（Section 3.5 虽提及MSE损失，但实验部分未充分验证）。
- 跨系统迁移存在性能衰减：Table 10 和 Table 11 的跨系统OOD实验（在AFlow上训练、在G-Designer上测试，或反之）显示性能有所下降，表明预测器对工作流生成系统的特征分布仍有一定敏感性。
- HotpotQA 上的低表现：在复杂多跳推理任务 HotpotQA 上，Agentic Predictor 的迁移准确率仅为 13.37%，显著低于部分基线方法。这一失效模式的具体原因尚未被充分分析，可能与多跳推理工作流的图结构复杂性或提示文本的语义稀疏性有关。
- 数据依赖性：跨领域无监督预训练依赖大量未标注的异构工作流数据，对于新兴领域或小众应用场景，这类数据的获取可能存在困难，限制了方法的即插即用性。
- 动态特征缺失：当前仅使用静态文本嵌入（T5、BERT）作为任务和提示的特征，未利用执行时间追踪、工具调用日志或用户反馈等动态信息，可能遗漏了部分与性能相关的时序模式。

### 4. 开放问题

1. **多目标优化扩展**：如何将 Agentic Predictor 从单一性能预测扩展至多目标优化场景（如同时平衡任务准确率与推理成本、延迟等），需要重新设计预测头和搜索策略。

2. **动态信息融合**：纳入执行时间追踪、工具调用日志或用户反馈等动态信息是否能进一步提升预测精度？这可能需要设计时序编码器或注意力机制来捕获工作流执行过程中的状态变化。

3. **搜索算法升级**：当前工作流优化采用简单的随机搜索+预测器排序策略。预测器引导的搜索能否与蒙特卡洛树搜索、进化算法或贝叶斯优化等更先进的搜索方法结合，以提升优化质量与搜索效率？

4. **语言模型选择的影响**：任务编码器使用不同预训练语言模型（T5 vs. BERT）会如何影响最终的性能预测？这一消融实验尚未在论文中报告。

5. **HotpotQA 失效诊断**：Agentic Predictor 在 HotpotQA 上的低表现（13.37%）原因是什么？是否与多跳推理工作流的图结构特性、提示文本的语义密度或跨领域预训练数据的覆盖偏差有关？如何针对性提升其在复杂推理任务上的迁移能力？

6. **工具集泛化**：预测器是否能够推广至未见过的新工具集或动态变化的工作流范式（例如需要在线插入/删除智能体的场景）？这涉及对图结构动态性和节点特征分布偏移的鲁棒性研究。

7. **连续性能预测**：将预测目标从二元成功/失败扩展至连续性能评分（如准确率、F1值等）时，当前的编码器-预测器架构需要哪些调整？多视图表示是否仍能提供有效的信息增益？

## 原文 PDF

![[paperPDFs/ICLR_2026/Multi_View_Encoders_for_Performance_Prediction_in_LLM_Based_Agentic_Workflows.pdf]]
