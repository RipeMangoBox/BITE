---
title: "AssoMem: Scalable Memory QA with Multi-Signal Associative Retrieval"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AssoMem_Scalable_Memory_QA_with_Multi_Signal_Associative_Retrieval.pdf
project_link: null
code_link: null
aliases:
- AssoMem
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "构建线索话语关联图并融合相关性、重要性和时序信号检索记忆。"
primary_logic: "AssoMem先从对话抽取线索并建图，再用RITRanker三信号打分和CMI权重融合选择记忆上下文。"
claims:
- "仅靠语义相关性难以区分大规模高相似记忆中的关键话语。"
- "关联记忆图把话语锚定到自动抽取线索，支持重要性感知的图排序。"
- "CMI融合能按查询类型自适应调整相关性、重要性和时序信号权重。"
- "AssoMem在LongMemEval和MeetingQA上提升检索与问答性能且在线延迟低于HippoRAG。"
---

# AssoMem: Scalable Memory QA with Multi-Signal Associative Retrieval

> [!tip] 核心洞察
> 模仿人类联想记忆机制，将对话话语锚定到自动提取的线索（clues）上，形成关联图结构，从而支持重要性感知排序；并利用互信息驱动的融合策略根据查询意图自适应平衡相关性、重要性和时序信号，实现更准确的上下文感知记忆检索。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AssoMem：基于多信号关联检索的可扩展记忆问答 |
| 英文题名 | AssoMem: Scalable Memory QA with Multi-Signal Associative Retrieval |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ZCjWUBwCwE) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | AssoMem |
| Dataset | LongMemEval medium |

> [!tip] 效果简介
> - LongMemEval medium 上，R@1 为 59.73，对比 —，变化 —。
> - LongMemEval medium 上，R@3 为 72.96，对比 —，变化 —。
> - LongMemEval medium 上，R@6 为 80.87，对比 79.14 (Topic Grouping)，变化 +1.73。

## 概要

AssoMem（Associative Memory）是一个面向大规模对话记忆问答的可扩展检索框架。其核心思想是模仿人类联想记忆机制，通过构建关联记忆图（associative memory graph）并引入多维检索信号（相关性、重要性、时序对齐）的自适应融合，解决现有方法在大规模、高相似度记忆库中检索性能严重下降的问题。实验表明，AssoMem在LongMemEval和MeetingQA三个基准上平均超越现有方法24.93%。

现有记忆问答方法（如平面检索、长短期记忆划分、主题分组等）在大规模、高相似度记忆库中面临严重性能瓶颈。根本原因在于：**仅依赖语义相关性（relevance）无法区分大量高度相似的记忆项，也无法捕捉用户对重要记忆的偏好和时序约束**。例如，当用户多次讨论相似话题（如“推荐电影”）时，仅靠语义相似度无法区分哪次对话包含用户最终选择的电影，也无法识别用户反复提及的偏好。

## 核心方法与创新机理

AssoMem的核心创新体现在以下五个关键设计变更：

| 变更维度 | 基线方案 | AssoMem方案 | 证据来源 |
|---------|---------|------------|---------|
| 检索信号维度 | 仅使用语义相关性 | 融合相关性、重要性（Personalized PageRank）和时序对齐（TimeLlaMa）三个维度 | Section 3.2.3 |
| 信号融合策略 | 固定权重或可学习权重 | 基于条件互信息（CMI）的自适应融合，根据查询类型动态调整各维度权重 | Section 3.2.3 |
| 记忆组织方式 | 平面列表或简单分层 | 关联记忆图：话语节点与自动提取的线索节点通过所有权边和相似度边连接 | Section 3.2.1 |
| 候选检索策略 | 直接检索话语或会话 | 两阶段混合检索：先检索相关线索，再对关联话语进行排序 | Section 3.2.2 |
| 生成模型微调 | 标准监督微调 | 多任务去噪微调：混合正负样本 + 仅负样本上下文 + 联合训练问题类型预测和答案生成 | Section 3.3 |

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_ZCjWUBwCwE_AssoMem_Scala/figures/001_Figure_1.jpg]]
*Figure 1: An example showing limitations in relevance solely retrieval. Our AssoMem consistently outperforms SOTA baselines on three datasets.*

AssoMem的整体框架如Figure 2所示，包含以下五个流水线模块：

1. **关联记忆图构建**（离线）：为每个会话提取线索，合并相似线索，构建包含线索节点和话语节点、所有权边和相似度边的图结构。
2. **候选检索**（在线）：根据查询检索Top-K相关线索，收集关联话语作为候选集。
3. **RITRanker评分**：对每个候选话语计算相关性分数、重要性分数（PPR）和时序分数（TimeLlaMa）。
4. **CMI自适应融合**：基于条件互信息计算每个维度的权重，加权求和得到最终分数，选择Top-K话语。
5. **多任务去噪微调生成**：使用微调后的LLM，基于检索到的记忆上下文生成答案。

### 5.1 关联记忆图构建

图包含两类节点：线索节点（clue nodes）和话语节点（utterance nodes）。两类边：
- **所有权边**：连接话语与其关联线索
- **相似度边**：当两个线索节点或两个话语节点的嵌入相似度超过阈值γ时创建

相似度边条件：
$$\sin(v_i, v_j) > \gamma, \quad v_i, v_j \in \mathcal{C}' \mathrm{or} v_i, v_j \in \mathcal{U}$$

### 5.2 候选检索

采用两阶段混合检索：先检索与查询q相关的Top-K线索，再对关联话语进行排序。最终检索集通过最大化候选话语分数之和来选择：
$$\dot{\mathcal{E}}^* = \operatorname*{argmax} \sum_{u \in \mathcal{E}} \mathrm{Score}(q, u)$$

### 5.3 RITRanker：多维信号评分

**相关性分数**：使用查询和话语的语义嵌入之间的余弦相似度：
$$s_u^{(rel)} = \text{sim}(e_q, e_u)$$

**重要性分数**：通过个性化PageRank（PPR）在关联记忆图上迭代计算：
$$\mathbf{r}^{(k+1)} = d M \mathbf{r}^{(k)} + (1-d) \mathbf{t}$$
其中M是邻接矩阵，t是个性化传送向量（话语单元设为查询-话语相似度，线索单元设为0），d是阻尼因子。

**时序分数**：使用TimeLlaMa提取时序嵌入，计算查询和话语的时序相似度：
$$s_u^{(temp)} = \text{sim}(e_q^{(temp)}, e_u^{(temp)})$$

### 5.4 CMI自适应融合

最终分数为加权和：
$$\operatorname{Score}(q,u) = w^{(rel)}(q) \tilde{s}_u^{(rel)} + w^{(imp)}(q) \tilde{s}_u^{(imp)} + w^{(temp)}(q) \tilde{s}_u^{(temp)}$$

权重通过条件互信息（CMI）自适应计算：
$$CMI_d(q) = I(\tilde{s}_u^{(d)(b)}; \lambda | q) = \sum_{\tilde{s}_x^{(d)(b)}} \sum_{\lambda} p(\tilde{s}_u^{(d)(b)}, y_m^{\lambda}) \log \frac{p(\tilde{s}_u^{(d)(b)}, y_m^{\lambda} | q)}{p(\tilde{s}_u^{(d)(b)} | q) p(y_m^{\lambda} | q)}$$

该公式衡量在给定查询类型q的条件下，分箱后的维度分数与有用性标签之间的条件互信息，从而动态调整各维度权重。

## 实验与关键发现

### 6.1 主实验结果

Table 1展示了AssoMem在LongMemEval medium、large和MeetingQA上的检索和QA性能：

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_ZCjWUBwCwE_AssoMem_Scala/figures/003_Table_1.jpg]]
*Table 1: Retrieval and QA performance on LongMemEval medium m (the top table), large l (the middle table), MeetingQA (the bottom table).*

| 数据集 | R@1 | R@3 | R@6 | R@10 | nDCG@3 | nDCG@6 | nDCG@10 | Acc@6 |
|-------|-----|-----|-----|------|--------|--------|---------|-------|
| LongMemEval medium | 59.73 | 72.96 | 80.87 | 84.96 | 75.36 | 81.30 | 82.93 | 64.01 |
| LongMemEval large | 43.56 | 59.60 | 64.93 | 69.33 | 62.61 | 65.87 | 66.31 | 52.59 |
| MeetingQA | 41.63 | 64.72 | 85.17 | 92.96 | 66.06 | 86.93 | 94.17 | 69.41 |

在LongMemEval medium上，AssoMem的R@6=80.87，Acc@6=64.01，优于所有基线方法。在LongMemEval large上，AssoMem在R@6和R@10上分别比最佳基线（topic grouping）提升7.04%和3.81%。

### 6.2 消融实验

Table 3的消融实验揭示了各组件的关键作用：
- **去除线索节点**：检索性能下降1.12%
- **使用固定权重分配**：性能下降4.08%
- **去除重要性信号**：单用户偏好类问题性能显著下降
- **去除时序信号**：时序推理类问题性能显著下降

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_ZCjWUBwCwE_AssoMem_Scala/figures/005_Table_3.jpg]]

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_ZCjWUBwCwE_AssoMem_Scala/figures/007_Table_3.jpg]]
*Table 3: Ablation on components and dimensions. w/o denotes without the component compared to AssoMem.*

Figure 3的雷达图进一步展示了AssoMem在不同问题类型上的性能优势，特别是在偏好推理和时序推理类问题上。

### 6.3 融合策略对比

Table 14显示，CMI融合策略在Recall@6上比非自适应固定权重高7.7%（82.64 vs 76.70），在Acc@6上高8.1%（64.20 vs 59.38）。信息驱动融合策略整体优于可学习融合策略（逻辑回归、随机森林、线性网络、SVM），因为记忆证据稀疏，难以训练有效的可学习模型。

### 6.4 错误分析

Table 4的错误分析显示，AssoMem实现了最高的检索保真度（Correct rate=64.01%），超过Topic Grouping 4.06%和LST Memory 13.05%，同时检索错误率最低（19.13%）。

### 6.5 延迟与成本

Table 13显示，关联记忆图的构建（~1949秒）是离线过程，但增量更新仅需0.01秒/节点。在线查询平均延迟1.30秒，比HippoRAG低3.5倍，比A-Mem低1.9倍。平均每次查询仅消耗1,846个token，约为HippoRAG和A-Mem的1/4.6。

### 6.6 长上下文对比

Table 15显示，长上下文方法（Llama-3.3-70B，128k窗口）仅达到21.93% Acc@6，远低于最弱的RAG基线（HippoRAG，48.61%）。AssoMem达到64.01% Acc@6，是长上下文基线的2.9倍。

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_ZCjWUBwCwE_AssoMem_Scala/figures/004_Table_2.jpg]]

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_ZCjWUBwCwE_AssoMem_Scala/figures/006_Table_2.jpg]]
*Table 2: Generation results of different LLMs using AssoMem recall@10 retrieval as context.*

## 定位与知识库关联

AssoMem属于**检索增强生成（RAG）**范式下的**记忆问答**子领域，其方法谱系可定位如下：

- **检索粒度演进**：从平面话语检索 → 会话级检索 → 多粒度检索（会话-话语、主题-话语、MemGAS的四种粒度）→ **关联图结构检索**（AssoMem）
- **信号维度扩展**：从单一语义相关性 → **多维信号融合**（相关性 + 重要性 + 时序对齐）
- **融合策略升级**：从固定权重 → 可学习权重（SVM、逻辑回归）→ **信息驱动自适应融合**（CMI）

与现有方法的关键区别：
- **HippoRAG**：基于RAG但仅使用相关性信号，AssoMem通过PPR和TimeLlaMa引入额外维度
- **MemGAS**：使用四种粒度和熵引导加权，但缺乏重要性感知和时序对齐
- **Topic Grouping**：按主题分组但无法区分同一主题内的重要记忆

**局限性**：
1. 关联记忆图构建（~1949秒）是离线过程，计算成本较高
2. 未报告在百万级话语上的性能，可扩展性有待验证
3. MeetingQA为合成数据集，真实世界代表性有限
4. CMI融合策略需要有用性标签，在无标签场景下可能无法直接应用
5. 检索性能在k=10附近饱和（~0.85），但QA准确率在k=6附近即达到平台期（~0.66），表明存在利用瓶颈（utilization bottleneck）

## 原文 PDF

![[paperPDFs/ICLR_2026/AssoMem_Scalable_Memory_QA_with_Multi_Signal_Associative_Retrieval.pdf]]
