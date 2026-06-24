---
title: "SPARTA: Scalable and Principled Benchmark of Tree-Structured Multi-hop QA over Text and Tables"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SPARTA_Scalable_and_Principled_Benchmark_of_Tree_Structured_Multi_hop_QA_over_Text_and_Tables.pdf
aliases:
- SPARTA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "SPARTA converts text-table evidence into a unified SQL-addressable fact database and generates tree-structured QA through executable query synthesis."
primary_logic: "It atomizes textual facts into grounding tables, builds nested SQL query trees with post-order generation and provenance repair, then verbalizes SQL with AST-ICL."
claims:
- "SPARTA reduces table-text QA annotation cost by generating executable SQL before natural-language questions."
- "Why-not provenance repair improves query generation by rewriting predicates that cause empty results."
- "The note reports zero audited annotation errors and large F1 drops for strong HybridQA models on SPARTA."
---

# SPARTA: Scalable and Principled Benchmark of Tree-Structured Multi-hop QA over Text and Tables

> [!tip] 核心洞察
> 将非结构化文本事实原子化并存储为关系型元组（grounding tables），与结构化源表统一为参考事实数据库，使得所有证据均可通过 SQL 统一寻址；结合后序遍历构建查询树和基于 why-not 溯源的谓词精炼，能够自动生成可执行、语义合理且覆盖多种嵌套模式（Type-N, A, J, JA）的多跳 SQL 查询，从而以极低的标注成本（约为 HybridQA 的 1/4）构建大规模、零错误率的基准。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SPARTA：面向文本与表格树结构多跳问答的可扩展原则性基准 |
| 英文题名 | SPARTA: Scalable and Principled Benchmark of Tree-Structured Multi-hop QA over Text and Tables |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=8KE9qvKhM4); [GitHub](https://github.com/pshlego/SPARTA/tree/main) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | SPARTA |
| Dataset | SPARTA (Oracle), SPARTA (Retrieval) |

> [!tip] 效果简介
> - SPARTA (Oracle) 上，F1 为 40.4 (HProPro w/ GPT-5)，对比 70.5 (HProPro on HybridQA)，变化 -30.1。
> - SPARTA (Oracle) 上，F1 为 35.6 (ODYSSEY w/ GPT-5)，对比 69.5 (ODYSSEY on HybridQA)，变化 -33.9。
> - SPARTA (Retrieval) 上，F1 为 22.6 (HELIOS + HProPro w/ GPT-5)，对比 N/A，变化 N/A。

## 概述

SPARTA (Scalable and Principled Benchmark of Tree-Structured Multi-hop QA over Text and Tables) 是一个大规模、高质量、可扩展的 Table-Text QA 基准。其核心贡献在于提出了一种以 SQL 为中心的端到端自动构建框架，能够以极低的标注成本（约为 HybridQA 的 1/4）生成零错误率、覆盖树状多跳推理和分析操作（如聚合、GROUP BY、HAVING）的问答对。实验表明，在 HybridQA 上 F1 超过 70 或在 OTT-QA 上 F1 超过 50 的 SOTA 模型，在 SPARTA 上 F1 下降了超过 30 个点，揭示了现有模型在真实大规模异构数据上深度多跳推理能力的严重不足。

## 背景与动机

现有 Table-Text QA 基准（如 HybridQA、OTT-QA、TAT-QA、FinQA、MultiHiertt）受限于人工标注，存在三个主要问题：

- **问题类型浅薄**：通常不超过两跳，缺乏聚合、分组、HAVING 等分析操作。
- **标注噪声高**：错误率高达 21%-30%（HybridQA 21%, MultiHiertt 26%, TAT-QA 30%, FinQA 17%），如 Table 7 所示。
- **数据规模小**：依赖小型 Web 表格，平均约 15 行（HybridQA 平均 15.7 行），无法有效评估模型在真实大规模异构数据上的深度多跳推理能力。

此外，现有合成基准（如 ERBench、TDBench）或局限于结构化表内推理，或缺乏表-文交互，无法满足 Table-Text QA 的评估需求。

## 核心创新

SPARTA 的核心创新在于：

1. **参考事实数据库构建**：将非结构化文本事实原子化并存储为关系型元组（grounding tables），与结构化源表统一为参考事实数据库，使得所有证据均可通过 SQL 统一寻址。
2. **后序遍历与溯源精炼**：采用后序遍历构建查询树，结合基于 why-not provenance 的谓词精炼，自动生成可执行、语义合理且覆盖多种嵌套模式（Type-N, A, J, JA）的多跳 SQL 查询。
3. **AST-ICL 问题口语化**：使用基于 LLM 的 SQL-to-text 模型（AST-ICL）将可执行的 SQL 查询转换为流畅的自然语言问题。
4. **轻量级人工验证**：仅需验证口语化问题的正确性和自然性，标注时间约为 HybridQA 的 1/4（验证 3,300 个查询约需 1,493 分钟，而 HybridQA 创建相同数量的问题约需 6,600 分钟）。

## 整体框架

![[assets/figures/papers/iclr26_0001_8KE9qvKhM4_SPARTA_Scalable_and_Principled_Benchmark_of_Tree/figures/001_Figure_1.jpg]]

SPARTA 的流水线如图 2 所示，包含三个主要阶段：

1. **参考事实数据库构建**：将源表（S_T）与从文本中提取的原子事实（grounding tables, G_T）合并，形成统一的 SQL 可查询数据库 D = S_T ∪ G_T。
2. **查询生成**：使用 LLM 生成可执行的 SQL 查询，通过后序遍历构建查询树，并通过溯源精炼修复空结果查询。
3. **问题口语化**：使用 AST-ICL 模型将可执行的 SQL 查询转换为流畅的自然语言问题，随后进行轻量级人工验证。

## 核心模块与公式推导

### 5.1 查询图模型

嵌套 SQL 查询被建模为一个查询图 G = (V, E)，其中每个节点 v_i 对应一个不同的查询块（SELECT FROM WHERE ... 子查询，包括最外层语句），每条有向边 e_ij 表示通过共享属性引用关联块 Q_i 和 Q_j 的嵌套谓词。

### 5.2 非嵌套查询生成

对于非嵌套查询，SPARTA 采用 Execution-Guided Generation：LLM 按标准 SQL 顺序逐子句生成语句，并立即执行部分查询；若结果为空，则将执行结果反馈给 LLM 以修正有问题的子句。

### 5.3 嵌套查询生成

对于嵌套查询，SPARTA 采用 Post-Order+Prov 作为默认方法：
- **后序遍历**：LLM 按后序构建查询树，先组合每个叶子子查询，然后逐层包裹更高层级的块。
- **溯源精炼**：当查询返回空结果时，利用 why-not provenance 技术识别导致过滤掉预期元组的谓词，并指示 LLM 仅重写有问题的子句。

### 5.4 问题口语化

对于每个可执行的 SQL 查询 qSQL，使用 AST-ICL 模型生成对应的自然语言问题 qNL。AST-ICL 将 SQL 抽象语法树作为上下文示例，生成语义对齐的流畅问题。

## 实验与分析

### 6.1 基准质量评估

| 数据集 | 标注错误率 | 平均行数 | 平均列数 |
|--------|-----------|---------|---------|
| SPARTA (NBA) | 0% | 3,280.5 | 12.2 |
| SPARTA (Movie) | 0% | 10,054.0 | 4.7 |
| SPARTA (Medical) | 0% | 200.0 | 6.7 |
| HybridQA | 21% | 15.7 | 4.4 |
| MultiHiertt | 26% | - | - |
| TAT-QA | 30% | - | - |
| FinQA | 17% | - | - |

*Table 7: 跨数据集标注审计结果。*

### 6.2 模型性能评估

在 SPARTA (Oracle) 设置下，SOTA 模型性能大幅下降：

| 模型 | SPARTA (Oracle) F1 | HybridQA F1 | 下降幅度 |
|------|-------------------|-------------|---------|
| HProPro (w/ GPT-5) | 40.4 | 70.5 | -30.1 |
| ODYSSEY (w/ GPT-5) | 35.6 | 69.5 | -33.9 |

*Table 4: SPARTA (Oracle) 上的 Table-Text QA 准确率。*

![[assets/figures/papers/iclr26_0001_8KE9qvKhM4_SPARTA_Scalable_and_Principled_Benchmark_of_Tree/figures/008_Table_4.jpg]]
*Table 4: Table-Text QA Accuracy on the SPARTA (Oracle) across multiple domains.*

在 SPARTA (Retrieval) 设置下，最佳方法（HELIOS + HProPro w/ GPT-5）仅达到 22.6 F1（Table 5）。

![[assets/figures/papers/iclr26_0001_8KE9qvKhM4_SPARTA_Scalable_and_Principled_Benchmark_of_Tree/figures/009_Table_5.jpg]]
*Table 5: Table-Text QA Accuracy on the SPARTA (Retrieval) across multiple domains.*

### 6.3 消融实验

**查询生成成本**（Table 3）：
- Post-Order+Prov 是最经济的嵌套查询生成方法，调用次数比 vanilla Post-Order 减少 42.8%，比 One-Shot-k 减少 66.2%。
- Execution-Guided Generation 在非嵌套查询中调用次数比 One-Shot 减少 38.0%。

![[assets/figures/papers/iclr26_0001_8KE9qvKhM4_SPARTA_Scalable_and_Principled_Benchmark_of_Tree/figures/006_Table_3.jpg]]
*Table 3: Generation Cost Comparison of Query Generation Methods.*

**查询自然度**（Figure 4）：
- Execution-Guided Generation 在非嵌套查询中自然度最高，自动评估比 One-shot 高 11.4%，比 Template-based 高 37.5%。
- Post-order+Prov 在嵌套查询中自然度最高，自动评估比 One-shot Nested 高 8.1%，比 Template-based 高 123.2%。

**树结构影响**（Figure 5a）：
- 在固定深度下，将广度从 1 增加到 3，HProPro 和 ODYSSEY 的 F1 分别下降 25.2% 和 27.5%。
- 在固定广度下，将深度从 1 增加到 3，HProPro 和 ODYSSEY 的 F1 分别下降 47.2% 和 49.9%。

**表-文交叉推理**（Table 6）：
- HProPro 在需要表-文交叉推理时 F1 下降 63.9%（从 45.2 降至 16.3）。
- ODYSSEY 在需要表-文交叉推理时 F1 下降 23.0%（从 39.2 降至 28.6）。

**嵌套类型影响**（Table 13）：
- HProPro 在 Type-JA 嵌套类型上表现最差（F1 25.6），比平均值 34.5 低 25.8%。
- Type-N 表现最好（F1 40.0），比平均值高 15.9%。

**否定和范围查询**（Table 14）：
- HProPro 在否定查询上 F1 为 28.7，比 SPARTA 总体得分 40.4 低 28.3%。
- 在范围查询上 F1 为 32.9，低 18.6%。

### 6.4 生成成本分析

**跨 LLM 规模**（Table 11）：
- Post-Order + Prov 在所有 LLM 变体上均是最具成本效益的方法，调用次数比 vanilla Post-Order 减少 18.8%-54.5%，比 One-Shot-k 减少 64.7%-66.2%。

**查询形状和大小**（Figure 8）：
- 对于星型查询，one-shot 生成在 hub 大小达到 3 时膨胀到理想调用次数的 17 倍；post-order 将其降至 3.2 倍；provenance 修复进一步降至 1.6 倍。
- 对于链式查询，provenance 仍能移除 30-40% 的冗余调用。

**访问表数量**（Table 12）：
- 平均 LLM 调用次数随访问表数量增加呈近线性增长：+2.6 次（1 到 2 表），+3.9 次（2 到 3 表），+2.2 次（3 到 4 表）。

### 补充图表

![[assets/figures/papers/iclr26_0001_8KE9qvKhM4_SPARTA_Scalable_and_Principled_Benchmark_of_Tree/figures/002_Figure_1.jpg]]
*Figure 1: Representative examples of our SPARTA benchmark (see Appendix M for more examples). Table 1: Comparison of Table–Text QA benchmarks (see Appendix A for detailed annotation audit results).*

![[assets/figures/papers/iclr26_0001_8KE9qvKhM4_SPARTA_Scalable_and_Principled_Benchmark_of_Tree/figures/005_Table_2.jpg]]
*Table 2: Cost metrics used for benchmark generation.*

## 方法谱系与知识库定位

SPARTA 属于 **合成基准自动构建** 方法谱系，与以下方法形成对比：

| 方法 | 构建方式 | 模态 | 推理深度 | 错误率 | 数据规模 |
|------|---------|------|---------|-------|---------|
| HybridQA | 人工标注 | 表-文 | ≤2 跳 | 21% | 小（~15 行） |
| OTT-QA | 人工标注 | 表-文 | ≤2 跳 | 21% | 小 |
| TAT-QA | 人工标注 | 表-文 | 数值推理 | 30% | 小 |
| FinQA | 人工标注 | 表-文 | 数值推理 | 17% | 小 |
| MultiHiertt | 人工标注 | 表-文 | 数值推理 | 26% | 小 |
| ERBench | 模板填充 | 结构化表 | 多跳 | 低 | 中 |
| TDBench | 模板填充 | 时序表 | 时序推理 | 低 | 中 |
| **SPARTA** | **LLM 驱动自动生成** | **表-文** | **树状多跳（深度≤3，广度≤3）** | **0%** | **大（~10K 行）** |

SPARTA 的核心优势在于：
1. **零错误率**：通过自动化流水线和轻量级人工验证实现 0% 标注错误率。
2. **大规模真实数据**：使用真实数据库（NBA 域平均 3,280.5 行，Movie 域平均 10,054.0 行），远超现有基准。
3. **丰富的推理类型**：覆盖四种嵌套模式（Type-N, A, J, JA）和分析操作（聚合、GROUP BY、HAVING）。
4. **领域无关性**：已在 NBA、电影和医疗三个领域验证，框架可扩展到任意关系数据库。

**局限性**：
- 目前仅关注 Table-Text 设置，尚未扩展到图像、视频等多模态输入。
- 查询生成依赖于 LLM（如 Llama-3.1-70B-Instruct），其生成质量和多样性受限于 LLM 的能力。
- 基准构建需要预先存在结构化的关系数据库，对于完全非结构化的数据源可能不直接适用。
- 目前仅覆盖了四种嵌套模式，可能无法涵盖所有现实世界中的复杂查询模式。

**开放问题**：
- SPARTA 如何扩展到图像、视频等多模态输入？
- 不同嵌套类型（Type-N, A, J, JA）的难度差异根源是什么？为什么模型在 Type-JA 上表现最差？
- SPARTA 的溯源精炼方法在更复杂的查询图（如深度 >3 或广度 >3）上的效果如何？
- SPARTA 基准是否能够有效推动 Table-Text QA 模型在真实世界应用中的改进？

## 原文 PDF

![[paperPDFs/ICLR_2026/SPARTA_Scalable_and_Principled_Benchmark_of_Tree_Structured_Multi_hop_QA_over_Text_and_Tables.pdf]]
