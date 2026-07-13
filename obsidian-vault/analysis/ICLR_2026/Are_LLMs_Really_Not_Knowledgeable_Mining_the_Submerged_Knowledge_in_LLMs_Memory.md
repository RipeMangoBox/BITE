---
title: "Are LLMs Really Not Knowledgeable? Mining the Submerged Knowledge in LLMs' Memory"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Are_LLMs_Really_Not_Knowledgeable_Mining_the_Submerged_Knowledge_in_LLMs_Memory.pdf
project_link: null
code_link: https://github.com/taoxj2001/Hits_at_k
aliases:
- HK
- ALRNKMSKLM
- Hits@k
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "Hits@k通过检查LLM输出logits前k候选来度量被最终解码掩蔽的潜藏知识。"
primary_logic: "方法先比较最终答案与token级候选知识，再过滤无信息token以分析知识存储和表达之间的差距。"
claims:
- "LLM错误输出并不等价于参数中缺少对应知识。"
- "Hits@k揭示DBpedia等数据集中大量正确答案存在于高排名logit候选中。"
- "“unsure”等无信息响应会掩蔽低置信度正确知识，过滤解码可恢复部分答案。"
---

# Are LLMs Really Not Knowledgeable? Mining the Submerged Knowledge in LLMs' Memory

> [!tip] 核心洞察
> 通过检查token级输出分布（logits）而非仅看最终输出，可以揭示模型潜藏的知识；提出的Hits@k指标能独立于表面答案正确性量化这种潜藏知识保留程度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大语言模型真的缺乏知识吗？挖掘LLM记忆中的潜藏知识 |
| 英文题名 | Are LLMs Really Not Knowledgeable? Mining the Submerged Knowledge in LLMs' Memory |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=gvUufgeJvV) · [GitHub](https://github.com/taoxj2001/Hits_at_k) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | Hits@k |
| Dataset | DBpedia-Head, IMDB-Head |

> [!tip] 效果简介
> - DBpedia-Head 上，Hits@100 为 92.1，对比 70.5，变化 +21.6。
> - DBpedia-Head 上，Hits@5 为 57.9，对比 17.2，变化 +40.7。
> - DBpedia-Head 上，Hits@50 为 83.4，对比 17.2，变化 +66.2。

## 概要

本文提出一个核心论点：大语言模型（LLM）在知识密集型问答任务中的失败，并非源于其参数中知识的缺失，而是源于**知识存储与表达之间的系统性差距**。作者通过检查token级输出分布（logits）而非仅看最终输出，揭示了模型潜藏的知识。为此，论文提出了 **Hits@k** 指标，用于独立于表面答案正确性量化这种潜藏知识保留程度。实验表明，在DBpedia数据集上，LLAMA3-8B的标准准确率（Hits@1）仅为17.2%，但Hits@5达到57.9%，Hits@50达到83.4%，证明模型存储了远超传统指标所反映的事实知识。此外，论文发现解码时允许输出“unsure”的提示设计会抑制低置信度但正确的知识表达，导致记忆掩蔽效应；通过过滤无信息token，可以恢复大量被掩蔽的正确回答。

传统观点认为，LLM在知识密集型任务中的表现不佳主要归因于其参数化知识不足。然而，作者通过分析模型输出发现，即使模型生成错误答案，其词汇概率分布中往往仍保留着正确答案。这一观察引出了本文的核心问题：**LLM真的缺乏知识，还是知识被掩蔽了？**

论文指出，解码时对高概率候选token的选择策略（尤其是允许输出“unsure”的提示设计）会抑制低置信度但正确的知识表达，导致记忆掩蔽效应。例如，Figure 1展示了一个场景：模型拥有正确的记忆，但最终输出了错误答案。这种知识存储与表达之间的差距，正是本文试图量化和解决的瓶颈。

## 核心方法与创新机理

本文的核心创新包括：

1. **Hits@k指标**：提出一种新的评估指标，检查正确答案是否出现在模型logits的前k个token中，独立于最终输出。公式为：
   \[
   \mathrm{Hits@}k = \frac{N_{correct}^k}{N}
   \]
   其中 \(N_{correct}^k\) 是正确答案出现在前k个logits中的样本数，\(N\) 是总样本数。

2. **无信息token过滤解码（分析性探针）**：设计一种解码策略，从top-k token中移除无信息token集合U（如“unsure”、空字符串、短token、停用词等），然后选择剩余token中概率最高的作为候选答案。公式为：
   \[
   a^* = \arg\max_{t \in T_k \setminus U} P(t \mid q)
   \]
   该策略被明确声明为分析性探针，而非可直接部署的推理方法。

3. **记忆掩蔽效应的量化**：通过对比标准解码和过滤解码的答案恢复率，系统性地量化了“unsure”输出对正确知识的掩蔽程度。

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_gvUufgeJvV_Are_LLMs_Real/figures/001_Figure_1.jpg]]
*Figure 1: An example illustrating a scenario where a model possesses potentially correct memories yet fails to provide the correct answer.*

论文的整体框架分为三个主要阶段：

1. **知识存储评估**：使用Hits@k指标，通过检查模型logits的前k个token，量化模型参数中潜藏的知识量，而不依赖于最终输出是否正确。

2. **记忆掩蔽效应分析**：分析模型输出类型分布（无信息、正确、错误），识别“unsure”等无信息响应在多大程度上掩蔽了正确知识。

3. **知识恢复实验**：通过过滤无信息token的解码策略，尝试恢复被掩蔽的正确回答，从而验证知识存储与表达之间的差距。

### 5.1 Hits@k指标

Hits@k是本文的核心评估指标，用于量化模型潜藏知识保留程度。其计算方式为：
\[
\mathrm{Hits@}k = \frac{N_{correct}^k}{N}
\]
其中，\(N_{correct}^k\) 表示正确答案出现在模型logits前k个token中的样本数。匹配策略使用至少三个连续字符的字符串匹配，以应对子词分词带来的问题。

### 5.2 无信息token过滤解码

该模块作为分析性探针，旨在揭示被“unsure”输出掩蔽的正确知识。其核心步骤为：

1. 获取模型在词汇表上的概率分布（logits）。
2. 选择前k个最高概率的token，构成集合 \(T_k\)。
3. 从 \(T_k\) 中移除无信息token集合 \(U\)（包括“unsure”、空字符串、短token、停用词等）。
4. 从剩余token中选择概率最高的作为候选答案：
   \[
   a^* = \arg\max_{t \in T_k \setminus U} P(t \mid q)
   \]

### 5.3 评估协议

- 使用贪心解码（temperature=0.0）以最小化随机性，确保结果可重复。
- 数据集按实体流行度分为Head（前10%）、Torso、Tail，以分析流行度对知识存储的影响。
- 使用字符串匹配（至少三个连续字符）来应对子词分词带来的匹配问题。

## 实验与关键发现

### 6.1 主要实验结果

Table 1展示了不同模型在Head/Torso/Tail子集上的Hits@100结果。关键发现包括：

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_gvUufgeJvV_Are_LLMs_Real/figures/011_Table_1.jpg]]
*Table 1: Experimental results (Hits@k, k = 100) for models of varying sizes were obtained by testing different popularity subsets of the head-to-tail dataset.*

| 模型 | DBpedia-Head | DBpedia-Torso | DBpedia-Tail | IMDB-Head | GoodReads-Head |
|------|-------------|---------------|--------------|-----------|----------------|
| LLAMA3-70B | 92.1 | 89.3 | 87.5 | 69.7 | 67.8 |
| LLAMA3-8B | 90.5 | 87.9 | 85.8 | 69.7 | 67.8 |
| LLAMA2-70B | 70.5 | 65.2 | 60.1 | 44.8 | 36.5 |

Figure 4展示了不同k值下LLAMA3-8B在DBpedia上的Hits@k：当k=1时准确率仅17.2%，但k=5时达到57.9%，k=50时达到83.4%，k=100时超过90%。这表明模型存储了远超传统指标所反映的事实知识。

### 6.2 记忆掩蔽效应分析

Figure 7展示了LLAMA3-8B在开放域和特定域数据集上的响应类型分布。在DBpedia上，超过一半的响应为无信息响应（如“unsure”或空字符串），且随着数据流行度降低，无信息响应比例增加。

Table 2展示了从“unsure”响应中恢复答案的比率。在DBpedia上应用“Unsure”过滤解码后：

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_gvUufgeJvV_Are_LLMs_Real/figures/014_Table_2.jpg]]
*Table 2: Answer recovery rates from “unsure” responses on DBPedia (left) and IMDB (right) datasets. Filtering uninformative tokens reveals a substantial portion of correct answers masked during initial decoding.*

- LLAMA3-70B：Head上从11.2%提升至23.0%，Torso上从8.7%提升至18.1%，Tail上从6.0%提升至12.7%。
- LLAMA2-13B：Head上从15.7%提升至21.9%，Torso上从11.1%提升至17.6%，Tail上从0.0%提升至2.0%。

Figure 6的案例研究进一步证实，当LLAMA3-8B输出“unsure”或空白时，正确答案往往出现在第2或第3个logit位置。

### 6.3 模型规模与流行度的影响

- 新模型（LLaMA3）的Hits@k显著高于旧模型（LLaMA2），但模型规模增大并不必然带来更高的Hits@k（如LLAMA2-13B和LLAMA2-70B在DBpedia-Head上的Hits@k相似）。
- 开放域数据集（DBpedia）的Hits@k高于特定域数据集（IMDB、GoodReads）。
- 流行度差异对DBpedia的Hits@k影响较小，但对IMDB影响较大。

### 6.4 公平性说明

- 所有实验使用贪心解码（temperature=0.0）以最小化随机性。
- 数据集按实体流行度分为Head、Torso、Tail，确保分析覆盖不同知识流行度。
- 使用至少三个连续字符的字符串匹配，以应对子词分词问题。

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_gvUufgeJvV_Are_LLMs_Real/figures/015_Table_3.jpg]]

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_gvUufgeJvV_Are_LLMs_Real/figures/016_Table_3.jpg]]
*Table 3: Experimental results (Hits@k, k = 5) for models of varying sizes were obtained by testing different popularity subsets of the head-to-tail dataset.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_gvUufgeJvV_Are_LLMs_Real/figures/017_Table_4.jpg]]
*Table 4: Experimental results (Hits@k, k = 10) for models of varying sizes were obtained by testing different popularity subsets of the head-to-tail dataset.*

## 定位与知识库关联

本文的方法谱系可追溯至以下工作：

- **知识存储与表达**：Petroni et al. (2019) 的“Language Models as Knowledge Bases?”首次提出将预训练语言模型视为知识库，本文在此基础上进一步区分了知识存储与表达。
- **数据集划分**：Sun et al. (2023) 的“Head-to-tail”数据集划分策略被本文采用，用于分析实体流行度对知识存储的影响。
- **评估方法**：本文的Hits@k指标与信息检索中的Recall@k概念类似，但首次将其应用于LLM内部知识存储的量化评估。
- **幻觉分析**：Huang et al. (2023) 和 Tonmoy et al. (2024) 的工作分析了LLM幻觉的挑战，本文从知识掩蔽的角度提供了新的解释。

本文的核心贡献在于揭示了LLM知识存储与表达之间的差距，并提供了量化和缓解这一差距的方法。然而，Hits@k指标依赖于字符串匹配，可能无法完美处理子词分词问题；“Unsure”过滤解码策略被明确声明为分析性探针，而非可直接部署的推理方法；实验仅覆盖了三个数据集，可能无法完全泛化到所有知识领域。未来工作可探索更精确的匹配策略、将过滤解码改进为实用的推理增强方法，以及研究知识存储与表达差距在其他任务中的表现。

## 原文 PDF

![[paperPDFs/ICLR_2026/Are_LLMs_Really_Not_Knowledgeable_Mining_the_Submerged_Knowledge_in_LLMs_Memory.pdf]]
