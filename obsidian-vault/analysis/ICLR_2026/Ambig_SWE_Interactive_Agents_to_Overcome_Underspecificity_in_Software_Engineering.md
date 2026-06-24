---
title: "Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Ambig_SWE_Interactive_Agents_to_Overcome_Underspecificity_in_Software_Engineering.pdf
aliases:
- AS
- Ambig-SWE
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将SWE-Bench问题改写为不明确指令并用交互设置评估修复智能体。"
primary_logic: "Ambig-SWE比较Full、Hidden和Interaction三种设置，再通过用户代理问答和信息增益指标分析澄清行为。"
claims:
- "交互设置在所有评估模型上显著优于不明确且无交互的Hidden设置。"
- "多数模型缺乏主动检测不明确性的能力，强提示会提高检测但也增加误报。"
- "高效交互依赖先探索代码库再提出可回答的针对性澄清问题。"
- "信息提取量和最终任务解决率并不直接等价，模型执行能力仍是关键因素。"
---

# Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering

> [!tip] 核心洞察
> 交互性可以显著提升智能体在不明确指令下的任务完成率（最高提升74%），但模型普遍缺乏主动检测不明确性的能力，且交互效率与模型规模无直接关联；有效的交互依赖于模型提出可回答、有针对性的澄清问题，而非盲目提问。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Ambig-SWE：通过交互式智能体克服软件工程中的指令不明确问题 |
| 英文题名 | Ambig-SWE: Interactive Agents to Overcome Underspecificity in Software Engineering |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=X2yzXtH4wp); [GitHub](https://github.com/sani903/InteractiveSWEAgents) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Ambig-SWE |
| Dataset | Ambig-SWE (基于SWE-Bench Verified) |

> [!tip] 效果简介
> - Ambig-SWE (基于SWE-Bench Verified) 上，解决率 (Resolve rate %) 为 Interaction setting (各模型不同)，对比 Hidden setting (各模型不同)，变化 最高提升74%（Claude Sonnet 3.5）。
> - Ambig-SWE (基于SWE-Bench Verified) 上，解决率 (Resolve rate %) 为 Claude Sonnet 4 Interaction: 41.8%，对比 Claude Sonnet 4 Hidden: 未明确给出，变化 显著提升（p=6.34e-18）。
> - Ambig-SWE (基于SWE-Bench Verified) 上，解决率 (Resolve rate %) 为 Qwen 3 Coder Interaction: 46.0%，对比 Qwen 3 Coder Hidden: 未明确给出，变化 显著提升（p=3.54e-07）。

## 概述

本论文提出 **Ambig-SWE**，一个基于 SWE-Bench Verified 的不明确指令变体基准，专门用于评估 LLM 智能体在指令不明确（underspecification）场景下的行为表现和交互能力。核心发现是：交互性可以显著提升智能体在不明确指令下的任务完成率（最高提升 74%），但模型普遍缺乏主动检测不明确性的能力，且交互效率与模型规模无直接关联。有效的交互依赖于模型提出可回答、有针对性的澄清问题，而非盲目提问。

## 背景与动机

当前 LLM 智能体在软件工程任务中已展现出显著的生产力提升（Peng et al., 2023; Brynjolfsson et al., 2023），但现实场景中的用户指令往往是不明确的（Chowdhury et al., 2024）。现有基准（如 SWE-Bench）假设指令完全明确，忽略了不明确性带来的挑战。不明确的指令可能导致资源浪费和任务偏差（Kim et al., 2024），而交互式智能体有望通过主动提问来缓解这一问题（Figure 1）。

## 核心创新

1. **Ambig-SWE 基准**：使用 GPT-4o 从 SWE-Bench Verified 的完全指定 issue 生成不明确版本，保留关键术语但减少细节内容，用于评估智能体在模糊指令下的行为。
2. **三种实验设置**：Full（完全指定，无交互）、Hidden（不明确，无交互）、Interaction（不明确，启用交互），系统性地隔离了指令明确性和交互机制的影响。
3. **交互提示强度控制**：设计了三种递增的交互鼓励提示（Neutral / Moderate Encouragement / Strong Encouragement），用于评估模型主动检测不明确性的能力。
4. **信息增益量化方法**：使用余弦距离（Cosine Distance）和 LLM-as-Judge 两种互补指标衡量交互带来的信息获取效率。

## 整体框架

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_X2yzXtH4wp_Ambig-S/figures/001_Figure_1.jpg]]
*Figure 1: Interactive agents reduce resource wastage and misalignment in underspecified settings.*

Ambig-SWE 的整体框架包含三个核心组件（Figure 2）：

1. **OpenHands agentic framework**（Wang et al., 2024b）：为 LLM 提供交互式执行环境，包括 bash 终端、文件系统、代码执行等工具。
2. **GPT-4o user proxy**：模拟拥有完整信息的用户，仅回答 issue 中明确包含的信息，避免幻觉。
3. **GPT-4o issue summarizer**：从完全指定的 issue 生成不明确版本。

实验流程如下：
- **Full setting**：智能体接收完全指定的 GitHub issue 和开发者对话提示。
- **Hidden setting**：智能体仅接收不明确的摘要版本，无交互机会。
- **Interaction setting**：智能体接收不明确的摘要版本，但可以向 GPT-4o user proxy 提问获取信息。

## 核心模块与公式推导

### 5.1 信息增益量化

论文使用两种互补方法衡量交互带来的信息增益：

**余弦距离（Cosine Distance）**：
$$
\mathrm{Cosine\ Distance}(P, Q) = 1 - \frac{P \cdot Q}{\|P\| \|Q\|}
$$

其中 \(P\) 和 \(Q\) 分别是交互前（E_before）和交互后（E_after）的知识嵌入向量，使用 OpenAI 的 text-embedding-3-small 生成。值越大表示信息增益越高。

**LLM-as-Judge**：使用 GPT-4o 对用户回答的信息具体性和新颖性进行 1-5 分评分。

### 5.2 不明确性检测实验

在检测实验中，每个 issue 以 Full 或 Hidden 设置呈现，模型需判断是否需要交互。使用三种递增的交互鼓励提示：
- **Neutral**：告诉智能体如果不清楚可以提问。
- **Moderate Encouragement**：要求智能体仔细检查所有必要信息是否可用，确认清楚后再继续。
- **Strong Encouragement**：强调提问对任务成功至关重要。

### 5.3 统计检验

使用 Wilcoxon Signed-Rank Test 比较不同设置间的性能差异：
- 零假设 \(H_0: \tilde{d} \leq 0\)（中位数差异为零或负）
- 备择假设 \(H_1: \tilde{d} > 0\)（中位数差异为正）

## 实验与分析

### 6.1 主实验结果

Figure 3 展示了各模型在三种设置下的解决率。关键结果如下：

| 模型 | Hidden 设置解决率 | Interaction 设置解决率 | Full 设置解决率 | Hidden vs Interaction p值 |
|------|------------------|----------------------|-----------------|--------------------------|
| Claude Sonnet 4 | - | 41.8% | - | 6.34e-18 |
| Qwen 3 Coder 480B | - | 46.0% | - | 3.54e-07 |
| Claude Sonnet 3.5 | - | 39.6% | - | 8.55e-19 |
| Claude Haiku 3.5 | - | 26.8% | - | 2.18e-14 |
| Deepseek-v2 | - | - | - | 0.0023 |
| Llama 3.1 70B | - | - | - | 0.0023 |

所有模型的 Interaction 设置均显著优于 Hidden 设置（Table 4）。Claude Sonnet 3.5 和 Haiku 3.5 通过交互恢复了 Full 设置下 80% 的性能差距。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_X2yzXtH4wp_Ambig-S/figures/010_Table_4.jpg]]

### 6.2 不明确性检测结果

Table 2 展示了各模型在不同交互鼓励提示下的检测性能：

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_X2yzXtH4wp_Ambig-S/figures/005_Table_2.jpg]]
*Table 2: Model performance in underspecificity detection across prompts with increasing interaction encouragement. FPR: false positive rate (unnecessary interaction); FNR: false negative rate (missed necessary interaction). Ideal models have high accuracy, low FPR, and low FNR.*

| 模型 | 提示类型 | 准确率 | FPR | FNR |
|------|---------|--------|-----|-----|
| Claude Sonnet 4 | Strong Encouragement | 0.89 | 0.18 | - |
| Claude Sonnet 3.5 | Moderate Encouragement | 0.84 | - | - |
| Qwen 3 Coder | 所有提示 | - | 0.00-0.01 | 1.00 |

关键发现：
- Claude Sonnet 4 在 Strong Encouragement 下检测准确率最高（0.89），但 FPR 也最高（0.18）。
- Qwen 3 Coder 在所有提示下均无法检测不明确性（FNR=1.00），且 FPR 极低（0.00-0.01），表明其完全缺乏主动检测能力。

### 6.3 信息增益与提问效率

Figure 5 和 Figure 6 展示了信息增益量化结果：

| 模型 | 余弦距离 | LLM-as-Judge 评分 | 平均提问数 |
|------|---------|-------------------|-----------|
| Qwen 3 Coder | 0.179 | - | 6.02 |
| Claude Sonnet 4 | 0.171 | - | 4.03 |
| Claude Sonnet 3.5 | 0.136 | - | 3.80 |
| Claude Haiku 3.5 | 0.135 | - | 3.49 |
| Deepseek-v2 | - | - | 4.57 |
| Llama 3.1 70B | 0.101 | 3.58/5 | 2.61 |

关键发现：
- Qwen 3 Coder 信息提取量最高（0.179），但提问数量比 Claude Sonnet 4 多 50%（6.02 vs 4.03）。
- Claude Sonnet 3.5 和 Haiku 3.5 提取的信息量几乎相同（0.136 vs 0.135），但任务性能差异巨大（39.6% vs 26.8%），说明信息提取能力与任务执行能力并不直接相关。
- LLM-as-Judge 评分对所有能力较强的模型收敛于 4/5 左右（Figure 6）。

### 6.4 提问策略分析

Figure 4 和 Table 7 展示了不同模型的提问模式：

1. **Claude Sonnet 系列**（3.80-4.03 个问题）：采用"先探索代码库，再提问"的策略，仅询问无法独立发现的信息，实现高效信息获取。
2. **Deepseek-v2**（4.57 个问题）：提出高度具体的实现问题，但往往超出用户知识范围，浪费交互轮次。
3. **Qwen 3 Coder**（6.02 个问题）：信息提取量最高，但存在刚性行为——即使获得导航信息（文件路径）仍会重新探索代码（Table 1），且提问数量显著多于其他模型。

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_X2yzXtH4wp_Ambig-S/figures/004_Table_1.jpg]]

### 6.5 消融实验

- **导航信息影响**（Table 1）：交互设置下，获取导航信息（文件路径）能提升大多数模型的解决率，但 Qwen 3 Coder 在获取后性能反而下降。
- **步骤数变化**：Claude Sonnet 4 在交互设置下平均步骤数从 65 增至 75，而 Qwen 3 Coder 保持 65 步不变，表明后者未有效利用交互信息调整行为。
- **恢复距离分析**（Figure 7）：恢复距离（1 - 完整 issue 与交互后知识的余弦相似度）在各模型间变化极小，无法捕捉信息提取效率差异，而提取式指标（Figure 5）能更好反映这些差异。

### 6.6 公平性说明

- 实验使用 GPT-4o 作为用户代理，其回答仅基于完整 issue 中的信息，可能无法完全模拟真实用户的行为模式。
- 不明确 issue 由 GPT-4o 生成，与自然出现的不明确 issue 在分布上存在差异（自然 issue 包含更多代码片段、错误信息、外部链接等）。
- Qwen 3 Coder 和 Claude Sonnet 4 使用了更多步骤（最多 100 步）和更新的 OpenHands v0.60 框架，可能引入不公平比较。
- Qwen 3 Coder 的交互提示被修改为包含强制澄清步骤，而其他模型未做此修改。

### 补充图表

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_X2yzXtH4wp_Ambig-S/figures/009_Table_3.jpg]]

![[assets/figures/papers/iclr26_representation_self_supervised_transfer__representation_learning__b001_X2yzXtH4wp_Ambig-S/figures/011_Table_3.jpg]]
*Table 3: Quantitative comparison of underspecified summaries against full issues using overlap- and semantics-based metrics.*

## 方法谱系与知识库定位

### 7.1 相关方法对比

| 方法 | 核心思想 | 与本文关系 |
|------|---------|-----------|
| ClarifyGPT (Mu et al., 2023) | 通过澄清问题缓解代码生成中的歧义 | 本文将其扩展到软件工程任务修复场景 |
| Interactive Code Generation (Lahiri et al., 2023) | 测试驱动的交互式代码生成 | 本文关注的是不明确指令下的信息获取而非测试生成 |
| Ambignlg (Niwa & Iso, 2024) | 指令歧义分类与消歧策略 | 本文聚焦于软件工程领域的特定不明确性 |
| CLAMBER (Zhang et al., 2024) | 识别和澄清模糊信息需求的基准 | 本文将其思想应用于代码修复任务 |
| Learning to Ask (Wang et al., 2024a) | LLM 在模糊工具使用指令下的行为 | 本文在更复杂的软件工程环境中验证了类似发现 |

### 7.2 知识库定位

本工作定位于 **LLM 智能体的交互式任务执行** 与 **指令不明确性处理** 的交叉领域。核心贡献包括：
1. 构建了首个针对软件工程任务的不明确指令基准（Ambig-SWE）。
2. 系统性地量化了交互机制对不明确指令下任务性能的影响。
3. 揭示了模型在检测不明确性、提问策略和信息利用效率方面的关键差异。
4. 提出了信息增益的量化方法，为未来研究提供了评估框架。

### 7.3 局限性与开放问题

**局限性**：
- 不明确 issue 由 GPT-4o 生成，与自然出现的不明确 issue 在分布上存在差异。
- 用户代理使用 GPT-4o 模拟，无法完全模拟真实用户行为。
- 实验仅基于 SWE-Bench Verified 数据集（500 个 Python issue），可能无法推广到其他编程语言或更复杂的任务。
- 交互设置下模型被强制要求交互，无法评估模型主动发起交互的能力。

**开放问题**：
1. 如何设计训练方法，使模型能够主动检测不明确性并自适应地发起交互，而非依赖外部提示？
2. Qwen 3 Coder 的刚性行为（即使获得导航信息仍重新探索代码）的根本原因是什么？如何缓解？
3. 交互效率（信息增益/提问数量）与任务性能之间的关系是什么？是否存在最优交互策略？
4. 如何将 Ambig-SWE 框架扩展到多轮交互、多智能体协作或更复杂的软件工程任务（如代码审查、架构设计）？
5. 自然出现的不明确 issue 与生成的不明确 issue 在影响模型行为方面有何差异？如何构建更真实的基准？

## 原文 PDF

![[paperPDFs/ICLR_2026/Ambig_SWE_Interactive_Agents_to_Overcome_Underspecificity_in_Software_Engineering.pdf]]
