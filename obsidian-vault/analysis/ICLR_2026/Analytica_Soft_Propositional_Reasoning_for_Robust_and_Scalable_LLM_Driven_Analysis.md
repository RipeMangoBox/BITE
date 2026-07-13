---
title: "Analytica: Soft Propositional Reasoning for Robust and Scalable LLM-Driven Analysis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Analytica_Soft_Propositional_Reasoning_for_Robust_and_Scalable_LLM_Driven_Analysis.pdf
project_link: null
code_link: null
aliases:
- Analytica
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "将复杂分析任务分解为软命题树，由 Grounder 估计叶子软真值，再用线性合成递归聚合根命题概率。"
primary_logic: |
  Analyzer 将根命题递归分解为可测试子命题，Grounder 通过搜索、工具或 Jupyter Notebook 评估叶子命题的软真值，Synthesizer 用线性加权规则向上聚合，从偏差-方差分解角度降低估计误差并保持噪声传播有界。
claims:
- "软命题推理把 LLM 分析从自由文本路径选择转为结构化概率估计，使偏差和方差可以分别被分解与控制。"
- "线性合成规则具有恒定噪声灵敏度，在经济、金融和政治预测任务上提升准确率并降低方差。"
---

# Analytica: Soft Propositional Reasoning for Robust and Scalable LLM-Driven Analysis

> [!tip] 核心洞察
> 通过将分析问题形式化为软命题推理（SPR），可以将估计误差分解为偏差和方差，并分别通过问题分解（降低偏差）和线性加权平均（降低方差）来系统性地最小化总误差。线性合成规则具有恒定的噪声灵敏度，确保误差传播稳定且有界。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Analytica：面向鲁棒且可扩展的LLM驱动分析的软命题推理框架 |
| 英文题名 | Analytica: Soft Propositional Reasoning for Robust and Scalable LLM-Driven Analysis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=9cFT6u82uh) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | Analytica |
| Dataset | 经济、金融、政治预测（736个任务） |

> [!tip] 效果简介
> - 经济、金融、政治预测（736个任务） 上，平均准确率 为 71.06%，对比 63.04% (Deep Research alone)，变化 +12.72%。
> - 经济、金融、政治预测（736个任务） 上，方差 为 6.02%，对比 9.28% (Deep Research alone)，变化 -35.1%。
> - 经济、金融、政治预测（736个任务） 上，平均准确率 为 70.11%，对比 61.96% (Jupyter NB alone)，变化 +13.15%。

## 概要

本文提出 **Analytica**，一种基于**软命题推理（Soft Propositional Reasoning, SPR）**的新型LLM智能体架构。该框架将复杂分析任务重构为对结果命题软真值的结构化估计过程，通过分治策略将问题分解为子命题树，利用工具增强的Grounder智能体降低偏差，再通过鲁棒线性合成模型递归聚合叶子节点以降低方差。在736个真实经济、金融和政治预测任务上，Analytica平均准确率提升15.84%，达到71.06%的准确率，方差仅为6.02%。其Jupyter Notebook Grounder在达到接近最高准确率（70.11%）的同时，成本降低90.35%，时间节省52.85%。此外，Analytica能够处理指数级增长的复杂度（54倍节点数），而计算时间仅呈近线性增长（12倍）。

现有LLM推理方法（如Chain-of-Thought、Tree-of-Thoughts、Graph-of-Thoughts、Forest-of-Thought）依赖自由形式的文本推理，缺乏可验证的组合结构，导致随机不稳定性和估计误差（偏差与方差）无法被系统性地控制。这些方法通常通过选择最优推理路径来生成最终答案，但路径选择本身具有随机性，且缺乏对误差传播的理论分析。

本文的核心动机是：**能否将LLM驱动的分析问题形式化为一个可分解、可验证的结构化过程，从而系统性地控制估计误差？** 作者从偏差-方差分解的角度出发，将总估计误差分解为偏差平方和方差，并分别通过问题分解（降低偏差）和线性加权平均（降低方差）来最小化总误差。

## 核心方法与创新机理

Analytica的核心创新在于将分析问题形式化为**软命题推理（SPR）**，并基于此设计了一个三阶段分治架构。具体创新点包括：

1. **推理范式转变**：从自由形式文本推理（如CoT、ToT）转变为软命题推理（SPR），将分析重构为对命题软真值的结构化估计。
2. **递归分治策略**：将根命题递归分解为子命题树，终止于可测试的叶子节点，通过简化叶子命题降低偏差。
3. **工具增强的Grounder智能体**：包括一个新颖的Jupyter Notebook智能体，用于数据驱动的分析，帮助验证和评分事实。
4. **鲁棒线性合成模型**：递归聚合叶子节点的软真值，通过加权平均消除随机噪声，具有恒定的噪声灵敏度，确保误差传播稳定有界。
5. **可扩展性与交互性**：支持递归扩展（Analytican）和“what-if”场景分析（Resynthesis）。

Analytica采用高度并行的三阶段分治策略，如Figure 1和Figure 3所示：

**阶段一：分析（Analysis）** — Analyzer智能体（A_A）将根命题递归分解为子命题树，直到达到最大叶子数或收到完成信号。每个子命题应独立且可测试。

**阶段二：接地（Grounding）** — Grounder智能体（A_G）并行评估所有叶子命题，通过搜索、实验和工具使用（如Jupyter Notebook）估计软真值并生成报告。论文研究了三种Grounder变体：Basic Search、OpenAI Deep Research和Jupyter Notebook。

**阶段三：合成（Synthesis）** — Synthesizer智能体（A_S）基于子命题的软真值，使用线性合成规则递归计算父命题的软真值并生成报告，最终得到根命题的鲁棒估计。

Figure 1: 整体流程图

### 1 偏差-方差分解

总估计误差可分解为偏差平方和方差（Equation 1）：

$$\mathbf{MSE}(p_{true}) = E[(p_{true} - p_{true}^{gt})^2] = (E[p_{true}] - p_{true}^{gt})^2 + E[(p_{true} - E[p_{true}])^2]$$

### 2 线性合成规则

非叶子命题的软真值是子命题软真值的线性组合（Equation 2）：

$$\rho_i.p_{true} = \beta_0 + \sum_j \beta_j \cdot \bar{\rho}_{ij}.p_{true}$$

其中β₀是截距项，βⱼ是权重系数。该规则具有**恒定灵敏度**（Proposition 1）：

$$\frac{\partial P}{\partial C_j} = \beta_j$$

这意味着线性合成规则对每个子命题输入的灵敏度是常数，等于其权重，确保误差传播稳定有界。相比之下，AND逻辑门的灵敏度是状态依赖的（∂P/∂C₁ = C₂），可能导致噪声放大。

### 3 偏差与方差传播

根估计的偏差是各个叶子估计偏差的加权和：

$$\mathrm{Bias}(p_{true}) = \sum_{i=1}^k \beta_i' \mathrm{Bias}(l_{i,true})$$

偏差通过两种方式降低：1）简化叶子命题；2）使用强大的Grounder。

根估计的方差是叶子方差及其协方差的函数：

$$\operatorname{Var}(p_{true}) = \sum_{i=1}^k \beta'_i^2 \operatorname{Var}(l_{i,true}) + \sum_{i \neq j} \beta_i' \beta_j' \operatorname{Cov}(l_{i,true}, l_{j,true})$$

方差通过粒度分解和最小化子命题间协方差来最小化。

### 4 可扩展性

递归Analytica（Analytican）具有上下文局部性：每个Grounder调用是O(1)，每个Analyzer/Synthesizer调用是O(K)，与递归深度无关。并行时间复杂度为：

$$T_P(n) = O\left(n + \frac{K^n}{P} \cdot T_G\right)$$

其中P是并行工作器数量，T_G是Grounder时间。

## 实验与关键发现

### 1 主要结果

Table 2: 主要性能对比

Table 3: 高级Grounder消融实验

| 方法 | 准确率 | 方差 | 成本降低 | 时间节省 |
|------|--------|------|----------|----------|
| Deep Research + Analytica-L | **71.06%** | **6.02%** | - | - |
| Jupyter NB + Analytica-L | 70.11% | 7.28% | 90.35% | 52.85% |
| Deep Research alone | 63.04% | 9.28% | - | - |
| Jupyter NB alone | 61.96% | 12.28% | - | - |

Analytica-L在Deep Research Grounder上达到最高准确率71.06%，方差仅为6.02%。Jupyter Notebook Grounder在显著降低成本（90.35%）和时间（52.85%）的同时，保持了接近的准确率（70.11%）。

### 2 合成规则消融

线性合成规则在准确率、稳定性和抗噪性方面均优于Vanilla和Simple Logic规则。Simple Logic规则对噪声高度敏感，而线性规则表现出高鲁棒性。将线性规则退化为随机权重或无权重平均会降低性能，表明学习到的权重提供了信息性的证据集成。

### 3 可扩展性

Table 1: 可扩展性数据

| 递归深度 | 平均时间（秒） | 节点数 | Token数 |
|----------|----------------|--------|---------|
| Basic | 0.5 | 1 | 3.6K |
| Analytica | 5.3 | 19.9 | 58.6K |
| Analytica² | 16.4 | 68.1 | 169.4K |
| Analytica³ | 33.3 | 359.5 | 929.0K |
| Analytica⁴ | 63.5 | 1075.3 | 2.8M |

Figure 4: 准确率与节点数关系

随着递归深度增加，节点数和Token数呈指数增长，而平均计算时间仅呈近线性增长。准确率与节点数呈正相关。

### 4 模型选择分析

Figure 13: 模型选择的边际影响

Grounder模型的选择是成本和整体性能的最重要决定因素。Analytica框架对同一模型族内的模型选择表现出相当大的鲁棒性。Analytica的有效性仅弱依赖于模型大小，主要受预训练和后训练过程影响。

### 5 小模型与开源模型

Table 6: 小模型和开源模型评估

| 模型 | 基线准确率 | +Analytica-L | 相对提升 |
|------|-----------|--------------|----------|
| OpenAI-OSS-20B | 55.58% | 64.24% | +15.59% |
| o4-mini | 62.63% | 66.11% | +5.56% |
| DeepSeek-v3.1 | 60.95% | 64.25% | +5.42% |

最大的相对增益出现在紧凑的蒸馏模型中，例如OpenAI-OSS-20B增强后达到与671B参数的DeepSeek-v3.1基线相当的性能。

### 6 科学声明验证

| 模型 | 基线 | +Analytica-Linear |
|------|------|-------------------|
| GPT-5.1 | 62% | 70% |
| GPT-5-mini | 71% | 73% |

在Matter-of-Fact基准上，Analytica展示了跨领域适应性。

### 7 统计显著性

Figure 10: 统计显著性矩阵

Analytica-L与Deep Research Grounder的组合与所有基线（包括Deep Research、Tree of Thoughts、Forest of Thoughts）相比，p值均为0.00，表明改进具有高度统计显著性。

### 8 公平性说明

- 实验主要基于经济、金融和政治预测任务，这些任务具有高不确定性和数据丰富性，但可能不代表所有分析领域。
- 科学声明验证实验显示了跨领域适应性，但仅测试了有限的一组模型。
- Jupyter Notebook Grounder在显著降低成本的同时保持了高准确率，有助于更广泛地使用高级分析能力。

## 定位与知识库关联

Analytica在LLM推理方法谱系中占据独特位置：

**与结构化推理方法的关系**：不同于CoT（线性路径）、ToT（树搜索）、GoT（图推理）和FoT（多树聚合）等依赖自由形式文本推理的方法，Analytica将推理重构为对命题软真值的结构化估计，具有可验证的组合结构。

**与概率逻辑的关系**：线性合成规则可以等价地表示为贝叶斯网络或概率逻辑程序（PLP），与noisy-or推理风格相关。这种形式化连接使得Analytica可以借鉴概率图模型和概率逻辑编程中的成熟技术。

**与工具增强智能体的关系**：Analytica的Grounder智能体（特别是Jupyter Notebook Grounder）代表了从纯LLM推理向工具增强推理的转变，通过外部数据源和计算环境降低偏差。

**与偏差-方差权衡的关系**：Analytica是首个系统性地从偏差-方差分解角度设计LLM推理框架的工作，通过分治降低偏差、通过线性聚合降低方差，实现了更好的偏差-方差权衡。

**局限性**：
- 当前框架未实现自适应Grounder选择。
- 线性合成规则假设子命题之间相互独立，在复杂现实场景中可能存在相关性。
- 实验主要集中在经济、金融和政治预测领域。
- Jupyter Notebook Grounder依赖于预定义的API库。
- 分解质量高度依赖于Analyzer LLM的能力。

**开放问题**：
- 如何自动学习或优化线性合成规则中的权重βⱼ和截距β₀？
- 当子命题之间存在强相关性时，如何扩展线性合成规则？
- Analytica框架能否扩展到多模态数据分析任务？
- 如何设计自适应机制，根据任务难度和可用预算动态选择Grounder模型？
- 在更广泛的应用领域（如医疗诊断、法律推理）中，Analytica的性能和适用性如何？

### 整体框架

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_9cFT6u82uh_Analytica_Sof/figures/001_Figure_1.jpg]]
*Figure 1: Given a complex query (e.g., forecasting $NVDA), Analytica selects the most plausible outcome by estimating the “soft truth value” of each provided competing proposition (Green box). The analysis process begins when an analyzer agent decomposes a proposition into a tree of subpropositions (Orange box), terminating is a set of testable leaf nodes. Next, grounder agents, such as a Jupyter Notebook agent mimicking a human analyst, evaluate the leaves (Purple box) and assign soft scores that reflect the evidence for each leaf. Finally, a synthesis stage recursively aggregates these scores up the tree (middle) to compute a final score for the root proposition.*

### 实验与分析

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_9cFT6u82uh_Analytica_Sof/figures/004_Table_1.jpg]]
*Table 1: Scalability of recursive Analytica. As the recursion depth increases, the number of nodes and tokens grows exponentially, while the average computation time increases near-linearly.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_9cFT6u82uh_Analytica_Sof/figures/005_Table_2.jpg]]
*Table 2: Performance, stability, and efficiency results across different Analytica setups and comparisons with structured reasoning approaches. Bold/underline indicates best/second. “Imp.” means improvement. $\mathbf { \partial } ^ { \ast } \mathrm { V } ^ { \ast } , \mathbf { \partial } ^ { \ast } \mathrm { S } ^ { \ast }$ , and ‘L’ denote the vanilla, simple logic, and linear rules, respectively.

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_9cFT6u82uh_Analytica_Sof/figures/006_Table_3.jpg]]
*Table 3: Ablation on the advanced grounders and comparison to Deep Research.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_9cFT6u82uh_Analytica_Sof/figures/017_Table_4.jpg]]
*Table 4: The library of external data APIs available to the Jupyter Notebook Grounder. Each proxy provides access to a suite of specific endpoints for quantitative analysis. “#” means the number of endpoints.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_9cFT6u82uh_Analytica_Sof/figures/019_Table_5.jpg]]
*Table 5: Model accuracy (Accu. %) breakdown by task category.*

## 原文 PDF

![[paperPDFs/ICLR_2026/Analytica_Soft_Propositional_Reasoning_for_Robust_and_Scalable_LLM_Driven_Analysis.pdf]]
