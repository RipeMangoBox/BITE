---
title: "Autoregressive Models Rival Diffusion Models at ANY-ORDER Generation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Autoregressive_Models_Rival_Diffusion_Models_at_ANY_ORDER_Generation.pdf
project_link: null
code_link: https://github.com/PKU-ML/Any-order-Any-subset-AR
aliases:
- AOASAMA
- AMRDMAAOG
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "A3把自回归分解推广为任意token组和任意顺序的组级自回归预测。"
primary_logic: "双流注意力编码已知组并预测当前组，课程训练再从单token自回归过渡到随机组顺序生成。"
claims:
- "A3保留自回归多层依赖建模，同时支持扩散式并行和双向生成灵活性。"
- "三阶段课程学习对任意顺序组级预测的稳定训练是必要的。"
- "A3在条件生成质量和长上下文QA速度质量权衡上相对扩散语言模型有竞争力。"
---

# Autoregressive Models Rival Diffusion Models at ANY-ORDER Generation

> [!tip] 核心洞察
> 通过将标准自回归分解推广到任意token组和生成顺序，A3框架在保留自回归概率严谨性和多层依赖建模的同时，继承了扩散模型在并行和双向生成方面的灵活性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 自回归模型在任意顺序生成中媲美扩散模型 |
| 英文题名 | Autoregressive Models Rival Diffusion Models at ANY-ORDER Generation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=vtDUomlazQ) · [GitHub](https://github.com/PKU-ML/Any-order-Any-subset-AR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Any-order Any-subset Autoregressive modeling (A3) |
| Dataset | TriviaQA, 条件生成 (The Pile), LongBench v1 单文档QA |

> [!tip] 效果简介
> - TriviaQA 上，准确率 (%) 为 22.5 (A3-8B, 10B tokens)，对比 52.1 (AR基线, 15T tokens)，变化 低于AR基线，但A3使用数据量少得多。
> - 条件生成 (The Pile) 上，困惑度 (由Llama-3.1-8B测量) 为 低于Dream和DiffuLlama (动态采样)，对比 Dream和DiffuLlama的困惑度，变化 A3困惑度更低。
> - LongBench v1 单文档QA 上，准确率 (%) 为 27.1 (A3, 组大小=1)，对比 25.4 (Llama-3.1-8B)，变化 +1.7%。

## 概要

本文提出 **Any-order Any-subset Autoregressive modeling (A3)**，一种新的序列建模范式。A3将扩散语言模型的组级预测重新形式化为广义自回归框架，在保留自回归多层依赖结构的同时，支持任意顺序和任意子集的生成。核心思想是将标准自回归分解 `P(x_{1:N}) = ∏_{t=1}^N P(x_t | x_{<t})` 推广到任意token组上的分解 `P(x_{1:N}) = ∏_{k=1}^K P(x_{G_k} | x_{G_{<k}})`，从而在概率严谨性、依赖深度和生成灵活性之间取得平衡。实验表明，A3-8B在条件生成质量上优于Dream和DiffuLlama等扩散模型，并在长上下文QA任务上实现了30%的推理加速。

**真实瓶颈**：扩散语言模型在每一步去噪中仅形成单层依赖结构，限制了模型捕捉深层层次化依赖的能力，导致生成质量和训练稳定性低于自回归模型。

**现有方法的局限**：
- **标准自回归模型**：严格从左到右生成，无法支持并行或双向生成。
- **扩散语言模型**（如Dream、DiffuLlama）：支持任意顺序生成和双向条件化，但每一步预测 `P(x_{G_2} | x_{G_1}) = ∏_{t ∈ G_2} P(x_t | x_{G_1})` 仅形成单层依赖，缺乏自回归模型的多层层次化建模能力。
- **掩码语言模型**（如MaskGIT、MDLM）：同样受限于单步预测的依赖深度。

**核心洞察**：通过将标准自回归分解推广到任意token组和生成顺序，A3框架在保留自回归概率严谨性和多层依赖建模的同时，继承了扩散模型在并行和双向生成方面的灵活性。

## 核心方法与创新机理

**因果旋钮**：将扩散训练中的两组预测扩展为多组预测，通过结构化多组预测过程保留自回归的多层依赖结构，同时支持任意生成顺序。

**主要创新点**：

| 变更模块 | 基线方法 | A3方法 |
|---------|---------|--------|
| 模型分解方式 | 标准自回归分解：`P(x_{1:N}) = ∏_{t=1}^N P(x_t | x_{<t})` | 组级自回归分解：`P(x_{1:N}) = ∏_{k=1}^K P(x_{G_k} | x_{G_{<k}})`，支持任意组划分和顺序 |
| 注意力机制 | 标准decoder-only Transformer的单流因果注意力 | 双流注意力：内容流（编码上下文，可关注本组及之前组）和查询流（位置感知预测，仅关注之前组） |
| 训练策略 | 标准自回归语言模型预训练 | 三阶段渐进式训练：阶段1（AR初始化，单token组）→ 阶段2（组扩展，组大小从1增至4）→ 阶段3（顺序排列，随机排列token到各组） |
| 推理策略 | 标准从左到右逐token自回归解码 | 组级AR采样（支持token级、固定大小组、任务特定组）和动态重采样（基于置信度或熵） |

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vtDUomlazQ_Autoregressive_/figures/001_Figure_1.jpg]]
*Figure 1: Architecture of the A3 model. Blue entries in the attention mask denote 0, and white entries denote −∞. The model employs a two-stream attention module with distinct causal masks. The content stream encodes contextual information and attends to tokens within its own group as well as all preceding groups. The query stream encodes positional conditions and attends only to tokens in preceding groups. The final cross-entropy loss is computed between the input context and the query stream’s output. For illustration, we provide an example grouping with $G _ { 1 } = \{$ 1 , 2 , 3 $\} , \bar { G } _ { 2 } = \{$ 5 , 6 $\} , G _ { 3 } = \{$ 4 $\}$ , showing how the forward process and causal masks...*

A3的整体框架包含三个核心模块：

1. **双流注意力模块**：支持任意顺序预测的核心架构组件，包含内容流和查询流，借鉴自XLNet（Yang et al., 2019）的双流注意力机制。
2. **渐进式训练策略**：将预训练AR模型逐步适应任意顺序预测的三阶段课程学习。
3. **组级解码策略**：支持组级AR采样和动态重采样的灵活推理方法。

### 5.1 组级自回归分解

A3将标准自回归分解推广到任意token组：

**标准自回归分解**：
`P(x_{1:N}) = ∏_{t=1}^N P(x_t | x_{<t})`

**A3组级分解**：
`P(x_{1:N}) = ∏_{k=1}^K P(x_{G_k} | x_{G_{<k}})`

其中 `G_k` 是序列索引 `{1, ..., N}` 的一个划分，支持任意组大小和生成顺序。

### 5.2 双流注意力机制

A3采用双流注意力架构，分别处理内容编码和位置感知预测：

**内容流注意力**（编码上下文信息）：
`H_c^{(l)}(i) = Attn(Q = H_c^{(l-1)}(i), K = H_c^{(l-1)}(≤G_k), V = H_c^{(l-1)}(≤G_k))`

内容流中，token i 可以关注本组及之前所有组的token。

**查询流注意力**（位置感知预测）：
`H_q^{(l)}(i) = Attn(Q = H_q^{(l-1)}(i), K = H_c^{(l-1)}(<G_k), V = H_c^{(l-1)}(<G_k))`

查询流中，每个查询向量仅关注严格早于本组的内容token。查询流使用一个共享的可学习查询向量注入到每个位置，键和值矩阵与内容流共享。

**最终预测分布**：
`p(x_i | X_{<G_k}) = Softmax(W · H_q^{(L)}(i))`

### 5.3 渐进式训练策略

A3采用三阶段课程学习，逐步从标准自回归过渡到任意顺序预测：

- **阶段1：AR初始化** — 使用单token组（组大小=1），完全复现标准自回归分解。
- **阶段2：组扩展** — 允许组大小大于1（从1逐步增至4），学习组内并行预测。
- **阶段3：顺序排列** — 引入随机排列，将token随机分配到各组，学习任意顺序预测。

## 实验与关键发现

### 6.1 主要实验结果

**条件生成质量比较**（Table 2）：A3-8B在使用基于置信度或熵的动态重采样时，在困惑度指标上始终优于Dream和DiffuLlama扩散模型。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vtDUomlazQ_Autoregressive_/figures/005_Table_1.jpg]]
*Table 1: Comprehensive evaluation of different language models. There are 4 types of these models: AR for autoregressive, DD for discrete diffusion, CD for continuous diffusion and A3 for our proposed model. For the infilling task, we use ROUGE-1/2/L score; for other tasks, we use the accuracy (%) metric. * refers to the results reported in DiffuLlama (Gong et al., 2025). Table 2: Conditional generation quality (measured by perplexity using Llama-3.1-8B) of previous diffusion models with A3 using different dynamic sampling strategy.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vtDUomlazQ_Autoregressive_/figures/006_Table_2.jpg]]

**长上下文QA任务**（Table 8）：

| 方法 | 准确率 (%) | 平均时间 |
|------|-----------|---------|
| Llama-3.1-8B (AR基线) | 25.4 | 1.0× |
| A3 (组大小=1) | 27.1 | - |
| A3 (组大小=2) | 22.5 | 0.7× |

A3在组大小=1时准确率提升1.7%，在组大小=2时实现30%的推理加速。

**数据规模扩展**（Table 4）：A3在TriviaQA上的准确率随训练数据量增加而稳步提升：6B tokens时为16.2，8B时为19.4，10B时为22.5。同时log困惑度从2.9降至2.3。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vtDUomlazQ_Autoregressive_/figures/010_Table_4.jpg]]
*Table 4: Performance of A3 with different training data Table 5: Model loss of A3 across context on TriviaQA and perplexity measured by Llama-3.1-8B. lengths, which is stably small.*

### 6.2 消融实验

**训练课程计划**（Table 3）：跳过早期训练阶段（阶段1和2）会在多个基准上导致4-6个百分点的性能下降，验证了三阶段渐进式训练的必要性。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vtDUomlazQ_Autoregressive_/figures/009_Table_3.jpg]]
*Table 3: Performance with different training curriculum schedule. We evaulate two variants trained on 2B tokens: 1. original curriculum and, 2. skipping stage 1 and 2 (directly training on stage 3: order permutations).*

**解码策略比较**（Figure 3）：
- 动态重采样方法在困惑度上始终优于组级AR采样。
- 基于置信度和基于熵的准则性能相近，置信度在小组大小时略优。
- 所有策略的困惑度都随组大小增加而上升。
- 组级AR采样在相同组大小下速度最快。

**上下文长度稳定性**（Table 5）：A3模型损失在不同上下文长度（512、1024、2048）下保持稳定。

### 6.3 与推测解码的比较

Table 7显示，推测解码达到更低的困惑度（1.9 vs 2.1），但计算成本更高（1.2× vs 1×）。A3通过改变模型分解本身，与推测解码和多token预测等方法正交。

### 6.4 公平性说明

- A3-8B的训练数据量（最多10B tokens）远小于AR基线（15T tokens），但仍在多个任务上取得了有竞争力的性能。
- 与扩散模型Dream和DiffuLlama的比较中，A3使用了更少的训练数据。
- A3的推理速度与组大小相关，组大小越大速度越快但困惑度越高，存在速度-质量权衡。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_vtDUomlazQ_Autoregressive_/figures/011_Table_6.jpg]]
*Table 6: The hyperparameter list*

## 定位与知识库关联

A3位于自回归模型和扩散模型的交叉点，其方法谱系包括：

- **自回归模型**：继承自标准AR分解（如GPT系列），但推广到组级分解。
- **排列语言模型**：借鉴XLNet（Yang et al., 2019）的双流注意力和排列目标。
- **扩散语言模型**：借鉴组级预测思想（如Dream、DiffuLlama），但用多步自回归替代单步去噪。
- **多token预测**：与Gloeckle et al. (2024)的多token预测正交，A3改变的是模型分解本身而非仅解码策略。

**局限性**：
- A3在组大小增大时困惑度上升，存在速度-质量权衡。
- A3-8B在TriviaQA上的准确率（22.5%，10B tokens）仍低于使用15T tokens训练的AR基线（52.1%），表明数据规模差距仍需弥合。
- A3在长上下文（8k）下组大小=2时准确率下降（22.5% vs 基线25.4%），并行解码可能带来精度损失。
- A3的训练需要三阶段渐进式课程，跳过早期阶段会导致性能下降，增加了训练复杂性。

**开放问题**：
- A3在更大模型规模（如70B）和更多训练数据下的表现如何？
- A3的组级分解是否能在推理时与推测解码或多token预测等加速方法正交结合？
- A3在更长的上下文（如32k或128k）下是否仍能保持稳定性和效率优势？
- A3的组划分策略是否可以自适应学习，而非随机或固定大小？
- A3在机器翻译、代码生成等其他任务上的泛化能力如何？

## 原文 PDF

![[paperPDFs/ICLR_2026/Autoregressive_Models_Rival_Diffusion_Models_at_ANY_ORDER_Generation.pdf]]
