---
title: "SmartChunk Retrieval: Query-Aware Chunk Compression with Planning for Efficient Document RAG"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SmartChunk_Retrieval_Query_Aware_Chunk_Compression_with_Planning_for_Efficient_Document_RAG.pdf
openreview_forum_id: Myti1QwL2t
aliases:
- SRQACCPEDR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "查询感知的自适应分块粒度选择（规划器预测的最小/最大块级别范围），直接影响检索召回率、答案准确率与系统成本。"
primary_logic: "通过轻量级规划器预测最优块粒度并结合压缩编码器直接产生高层语义嵌入，避免重复LLM摘要，实现查询感知的高效检索；借助交替RL与SFT的STITCH训练框架稳定多目标优化，解决监督信号缺失与训练不稳定的挑战。"
claims:
- "SMARTCHUNK在保持或提升QA准确率的同时，将货币成本降低至多级基线方法的30%以下。"
- "规划器能够根据查询和文档类型自适应地选择分块大小，验证了动态粒度调整的必要性。"
- "去除规划器或压缩编码器导致成本上升或性能显著下降，证明各个模块的有效性。"
- "STITCH训练框架在规划准确率上达到82.0%，相比最强SFT+RL基线提升约5%，且仅需一半的监督token。"
---

# SmartChunk Retrieval: Query-Aware Chunk Compression with Planning for Efficient Document RAG

> [!tip] 核心洞察
> 通过轻量级规划器预测最优块粒度并结合压缩编码器直接产生高层语义嵌入，避免重复LLM摘要，实现查询感知的高效检索；借助交替RL与SFT的STITCH训练框架稳定多目标优化，解决监督信号缺失与训练不稳定的挑战。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SmartChunk检索：面向高效文档RAG的查询感知分块压缩与规划 |
| 英文题名 | SmartChunk Retrieval: Query-Aware Chunk Compression with Planning for Efficient Document RAG |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Myti1QwL2t) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SMARTCHUNK |
| Dataset | Average across NarrativeQA, QASPER, QuALITY, Natural Questions, Average across datasets, NewsQA (out-of-domain) |

> [!tip] 效果简介
> - Average across NarrativeQA, QASPER, QuALITY, Natural Questions 上，QA Accuracy 为 0.564，对比 0.561 (MAL RAG)，变化 +0.003。
> - Average across datasets 上，Retrieval Recall 为 0.829，对比 0.842 (MAL RAG)，变化 -0.013。
> - Average across datasets 上，Monetary cost ($) 为 0.078，对比 0.301 (MAL RAG)，变化 -0.223 (74% reduction)。

## 概述

**问题瓶颈**：当前检索增强生成（RAG）系统普遍采用固定大小的文档分块与平面检索策略，导致检索质量高度依赖分块粒度选择。单一粒度无法同时适应事实型短查询与需要跨段落综合的长查询，也不匹配异质文档结构（如论文、报告、对话），在引入噪声的同时难以扩展至大规模语料库。

**核心思路**：SMARTCHUNK提出查询感知的自适应多级检索框架，通过两个关键模块解决上述瓶颈：（1）**轻量级规划器**（Planner），根据查询与文档元数据预测应检索的最小与最大块级别，动态约束候选空间；（2）**压缩编码器**（Chunk Compression Encoder），直接聚合细粒度块嵌入生成高层语义表示，避免对每个文档块重复调用大语言模型（LLM）进行摘要。规划器采用**STITCH**训练框架——交替执行强化学习（RL）、提示化RL与模仿学习（SFT）——在缺乏直接监督信号的条件下稳定实现多目标优化。

**主要结果**：在NarrativeQA、QASPER、QuALITY、Natural Questions四个长文档QA基准上，SMARTCHUNK以0.564的平均QA准确率与最强多级基线MAL RAG（0.561）持平，但货币成本仅为后者的约26%（$0.078 vs $0.301），成本降低约74%（Table 2, Figure 1）。在域外数据集NewsQA上，SMARTCHUNK结合小样本提示以$0.032的成本匹配了MAL RAG $0.147成本下的性能（F1 0.906 vs 0.907, Table 3）。消融实验表明，移除规划器导致成本与延迟显著上升，移除压缩编码器则使检索与QA性能明显下降（Table 2）。STITCH仅使用SFT+RL一半的监督token即可达到82.0%的规划准确率，相比最强SFT+RL基线提升约5个百分点（Table 4, Table 5）。

## 背景与动机

### 文档RAG中的分块困境

检索增强生成（RAG）在处理长文档时面临一个根本性的瓶颈：**分块策略与检索质量之间的深层耦合**。现有系统普遍采用固定大小的分块方式——例如按句子切分或按512 token的固定窗口切分——然后进行平面化的单级检索。这种静态策略在两个维度上暴露出结构性缺陷：

1. **查询异质性无法被单一粒度覆盖**：事实型查询（如“某年某事件”）通常只需句子级细粒度块即可回答，而多跳推理或摘要型查询则需要段落级甚至章节级的高层语义块。固定分块迫使系统在所有查询上使用同一粒度，要么引入噪声（块过大），要么丢失上下文（块过小）。

2. **文档结构信息被丢弃**：长文档天然具有层次结构（词→句→段→节→章），但固定分块将文档压平为无差别的块序列，丧失了跨粒度的高层语义信号。

这一困境的直接后果是：**检索质量高度依赖分块大小的选择，且不存在对所有查询和文档都最优的单一粒度**。当系统规模扩展到大规模语料库时，这种不匹配会进一步放大检索噪声和计算成本。

### 现有多级方法的代价瓶颈

为缓解固定分块的局限，近年来出现了构建多级层次结构的方法，主要分为两类：

- **基于树的递归摘要方法**（如 **RAPTOR**, Sarthi et al., 2024）：通过递归嵌入、聚类和LLM摘要构建多级分块树，在检索时可以跨越不同粒度。
- **基于图谱的多级检索方法**（如 **GRAG**, Edge et al., 2024；**MAL RAG**, Zheng et al., 2025）：通过知识图谱或多级抽象检索增强跨粒度推理能力。

这些方法虽然提升了检索质量，但引入了新的代价瓶颈：**高层块的生成依赖LLM摘要**。具体而言，每构建一个高层块都需要调用大语言模型对多个细粒度块进行摘要，然后将摘要文本嵌入为向量。当文档数量增加时，摘要调用的成本呈线性甚至超线性增长，使得这些方法在大规模部署场景下难以承受。

### 核心洞察与本文动机

本文的核心洞察是：**并非所有查询都需要完整的层次结构——查询本身携带了关于所需粒度的信息**。一个轻量级的规划器可以在检索前预测回答特定查询所需的最小和最大块级别，从而约束候选空间，避免构建不必要的层次。同时，高层块的语义嵌入可以通过一个训练好的压缩编码器直接从细粒度块嵌入映射得到，无需反复调用LLM进行摘要。

基于这一洞察，本文提出 **SMARTCHUNK**，目标是在保持或提升问答准确率的前提下，大幅降低多级检索的货币成本和延迟。其设计围绕三个关键机制展开：

- **查询感知的自适应粒度选择**：规划器 $\mathcal{P}$ 根据查询和文档元数据预测 $(level_{min}, level_{max})$，动态约束检索范围，实现“按需构建层次”。
- **压缩编码器替代LLM摘要**：压缩编码器 $\mathcal{E}$ 将一组细粒度块的嵌入直接映射为单一高层语义嵌入，避免昂贵的摘要调用。
- **稳定的规划器训练范式**：提出 **STITCH**（Solve with RL, Then Imitate To Close Holes）训练框架，通过交替执行强化学习、提示化强化学习和模仿学习（SFT），解决监督信号缺失和RL训练不稳定的双重挑战。

实验表明，SMARTCHUNK在四个长文档QA基准上以**不到多级基线方法30%的货币成本**达到了可比甚至更优的问答准确率（Table 2, Figure 1），验证了查询感知分块压缩在效率-准确率折衷中的显著优势。

## 核心创新

SMARTCHUNK 的核心创新在于将传统 RAG 中**固定、被动的分块策略**转变为**查询感知的自适应多级检索**，并通过一套稳定的训练框架实现高效优化。具体而言，其关键创新体现在以下三个相互耦合的维度：

### 1. 查询感知的自适应粒度规划（Planner P）

传统方法（如固定句子级分块、512-token 固定分块、Late Chunking）采用**静态单一粒度**，无法适应异质查询与文档结构的复杂性。SMARTCHUNK 引入一个轻量级规划器 $\mathcal{P}$，根据查询 $q$ 和文档元数据预测应检索的**最小与最大块级别**：

$$\mathcal{P}(q, \text{MetaData}(D)) = (\text{level}_{\text{min}}, \text{level}_{\text{max}})$$

这一设计将检索空间从“全量候选”约束为“查询所需的最优粒度范围”，直接决定了检索召回率、答案准确率与系统成本三个关键指标。实验表明，规划器能够根据数据集和查询类型**自适应地调整分块大小**（Figure 4b）：在 NarrativeQA 上平均选择约 1750 tokens 的大块，而在 QuALITY 上仅需约 175 tokens 的小块，验证了动态粒度调整的必要性。移除规划器（w/o P）会导致总是构建完整分块树，使成本和延迟显著增加（Table 2）。

### 2. 压缩编码器替代 LLM 摘要（Chunk Compression Encoder E）

多级检索的一个关键瓶颈在于**高层块语义表示的生成**。现有方法（如 RAPTOR、MAL RAG）依赖 LLM 对子块进行文本摘要，再将摘要文本嵌入为向量，成本高昂。SMARTCHUNK 提出**压缩编码器 $\mathcal{E}$**，直接将一组细粒度块的嵌入映射为单一高层语义嵌入：

$$e(c_5) = \mathcal{E}(c_1, c_2, \ldots, c_4) \in \mathbb{R}^d$$

压缩编码器通过最小化其输出与 LLM 摘要嵌入之间的 L2 距离进行训练：

$$\mathcal{L}_{\text{comp}}(S) = \| e_{\text{comp}} - e_{\text{gt}} \|_2^2$$

这一设计在推理时**完全避免了重复调用 LLM 进行摘要**，大幅降低成本。消融实验（Table 2）证实了这一创新的价值：使用 GPT 摘要生成高层嵌入的变体（w/o ε summarize）虽然取得了最高的检索召回率 0.861，但成本高达 $0.204；而压缩编码器以极低成本实现了可比的检索与 QA 性能，凸显其高性价比优势。

### 3. STITCH 训练框架：交替 RL 与 SFT 的稳定优化

规划器的训练面临**监督信号缺失**与**多目标优化不稳定**的双重挑战。纯 RL 训练效果极差（规划准确率仅 0.356），而 SFT+RL 在监督 token 减半时性能崩溃（准确率从 0.763 降至 0.544）。SMARTCHUNK 提出 **STITCH（Solve with RL, Then Imitate To Close Holes）** 训练框架，交替执行三个步骤：

1. **Vanilla RL rollout**：无提示的强化学习探索
2. **Hinted RL rollout**：带提示的强化学习，引导策略向高质量解靠近
3. **Imitation Learning**：对 RL 成功案例进行模仿学习（SFT），稳定训练并防止遗忘

策略更新采用基于 GRPO 的目标函数，结合剪切优势与 KL 散度惩罚：

$$\mathcal{T}_{\mathrm{STITCH}}(\theta) = \mathbb{E} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|o_i|} \sum_{t=1}^{|\alpha_i|} \left( \min\left( r_{i,t}(\theta) \hat{A}_{i,t}, \mathrm{clip}\left( r_{i,t}(\theta), 1-\varepsilon, 1+\varepsilon \right) \hat{A}_{i,t} \right) - \beta D_{\mathrm{KL}}(\pi_{\theta}||\pi_{\mathrm{ref}}) \right) \right]$$

其中重要性采样比率与组归一化优势为：

$$r_{i,t}(\theta) = \frac{\pi_{\theta}(o_{i,t}|q, \rho, o_{i<t})}{\pi_{\text{old}}(o_{i,t}|q, \rho, o_{i<t})}, \quad \hat{A}_{i,t} = \frac{R_i - \text{mean}(\{R_i\})}{\text{std}(\{R_i\})}$$

多目标奖励综合了答案正确性、块使用成本、输出格式和推理长度：

$$R = R_{\mathrm{QA}} + R_{\mathrm{Cost}} + R_{\mathrm{Format}} + R_{\mathrm{Length}}$$

STITCH 仅需 SFT+RL 一半的监督 token（418k vs 795k），即达到 **82.0% 的规划准确率**，比最强 SFT+RL 基线提升约 5%，同时 QA 准确率达到 0.564，成本仅 $0.078（Table 5）。训练动态曲线（Figure 7）显示训练奖励逐步上升，测试规划准确率稳定收敛至约 80%，验证了 STITCH 的稳定性。

---

**创新总结**：上述三个创新形成了完整的“感知—压缩—优化”闭环。规划器提供查询感知的粒度选择，压缩编码器消除 LLM 摘要的推理开销，STITCH 则解决了规划器训练中监督信号稀缺与多目标冲突的核心瓶颈。三者协同使得 SMARTCHUNK 在保持或提升 QA 准确率的同时，将货币成本降至多级基线方法的 30% 以下（Table 2, Figure 1）。

## 整体框架

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/002_Figure_2.jpg]]
*Figure 2: Left: Overview of the SMARTCHUNK framework. Compared to vanilla RAG, which uses fixed chunking and flat retrieval, SmartChunk introduces two key modules: (1) a planner P that predicts the smallest and largest chunk sizes per query, enabling adaptive multi-level retrieval, and (2) a Chunk Compression Encoder E that produces compact, high-level embeddings for aggregated chunks, lowering the cost of the multi-level representation. These additions allow SMARTCHUNK to adapt to different query complexity and document structure, balancing accuracy and efficiency. Modules added by SmartChunk are shown in blue, while modules from vanilla RAG are shown in black. The figure distinguishes between text...*

SMARTCHUNK 的核心设计理念是**用查询感知的自适应分块替代传统 RAG 的固定粒度分块与平面检索**，从而在不牺牲答案质量的前提下大幅压缩检索成本。其整体 pipeline 由四个关键模块串联构成，并在训练阶段引入 STITCH 循环来稳定优化规划器。

### Pipeline 架构

Figure 2（左）给出了框架的全貌。给定查询 $q$ 和文档 $D$，系统按以下流程执行：

1. **规划器 $\mathcal{P}$** 首先接收查询 $q$ 和文档元数据 $\text{MetaData}(D)$，预测一个粒度区间：
   $$ \mathcal{P}(q, \text{MetaData}(D)) = (\text{level}_{\text{min}}, \text{level}_{\text{max}}) $$
   该区间约束了后续检索的候选空间——只检索介于最细粒度（$\text{level}_{\text{min}}$）和最粗粒度（$\text{level}_{\text{max}}$）之间的块，避免构建完整的层级树。

2. **压缩编码器 $\mathcal{E}$** 负责构建多级块层次结构。它将一组细粒度块的嵌入直接映射为单一高层语义嵌入：
   $$ e(c_5) = \mathcal{E}(c_1, c_2, \ldots, c_4) \in \mathbb{R}^d $$
   这意味着高层块嵌入编码了整个子块簇的语义，而无需显式调用 LLM 生成摘要文本再嵌入，从根本上避免了重复的摘要成本。

3. **检索器 $\mathcal{R}$** 在规划器指定的粒度范围内，利用压缩嵌入和多级层次结构检索与查询最相关的块。

4. **生成器 $\mathcal{G}$**（通常为 GPT-4o 等 LLM）基于检索到的块生成最终答案。

### 模块间的因果链路

这一 pipeline 的效率瓶颈与因果机制可概括为：
- **规划器是成本控制的总开关**：若移除规划器（w/o P），系统被迫构建完整的分块树，成本与延迟显著上升（Table 2）。规划器的预测质量直接决定候选空间的大小，进而影响检索成本与召回率。
- **压缩编码器是效率的关键杠杆**：若用 GPT 摘要生成高层嵌入（w/o ε summarize），检索召回率虽可达 0.861，但货币成本飙升至 $0.204；若直接编码原始文本（w/o ε direct encode），检索与 QA 性能则明显下降（Table 2）。压缩编码器在“语义保真度”与“计算开销”之间取得了平衡。
- **训练范式决定规划器的上限**：规划器并非简单分类器，而是通过 STITCH 训练循环（见下节）学习在元数据与查询意图上进行推理，从而实现数据集自适应的粒度选择（Figure 4b, Figure 5）。

### 优化目标

整个框架的优化目标形式化为准确率-成本的加权折衷：
$$ \max_\pi \mathbb{E}_{(q, D, \hat{a}) \sim \mathcal{D}} \left[ \text{Acc}(\mathcal{G}(q, \pi(q, C))), \hat{a}) - \lambda \tau((\mathcal{G}, \pi \mid q, D)) \right] $$
其中 $\lambda$ 控制准确率与效率的相对权重，$\tau$ 度量系统的货币成本与延迟。这一目标贯穿规划器的 RL 奖励设计与压缩器的训练损失，确保各模块协同朝向“高性价比检索”收敛。

> **证据强度**：上述模块关系与因果声明由 Table 2 的消融实验（w/o P, w/o ε direct encode, w/o ε summarize）及 Figure 4b 的规划器自适应行为直接支撑，置信度 0.9–0.95。

## 核心模块与公式推导

SMARTCHUNK框架在标准RAG流水线中引入了两个关键模块——**规划器（Planner）** 与**分块压缩编码器（Chunk Compression Encoder）**，并配套设计了**STITCH训练框架**来稳定地训练规划器。以下逐一阐述其核心设计与关键公式。

### 规划器 P：查询感知的自适应粒度选择

规划器是SMARTCHUNK实现查询感知检索的核心。其输入为查询 $q$ 和文档的元数据 $\text{MetaData}(D)$（如文档标题、章节结构、篇幅统计等），输出为一个二元组：

$$\mathcal{P}(q, \text{MetaData}(D)) = (\text{level}_{\text{min}}, \text{level}_{\text{max}})$$

其中 $\text{level}_{\text{min}}$ 和 $\text{level}_{\text{max}}$ 分别表示能够回答查询 $q$ 所需的最小和最大分块级别。这一约束直接限定了后续检索器需要搜索的候选空间：检索器仅需在 $[\text{level}_{\text{min}}, \text{level}_{\text{max}}]$ 范围内检索相关块，避免了构建完整多级分块树所带来的冗余计算与存储开销。

规划器的设计动机源于一个关键观察：不同查询对信息粒度的需求差异巨大。例如，事实型查询可能仅需句子级细粒度块，而摘要型查询则需要段落乃至章节级的高层语义块。通过让规划器根据查询类型和文档结构自适应地预测粒度范围，SMARTCHUNK在保持检索质量的同时大幅降低了成本（Table 2, Figure 4b）。

### 分块压缩编码器 E：免摘要的高层语义嵌入

传统多级检索方法（如RAPTOR、MAL RAG）通常依赖LLM对细粒度块进行摘要，再将摘要文本嵌入为高层表示。这一过程在每次查询时都需调用LLM，成本高昂。SMARTCHUNK用一个轻量级的压缩编码器 $\mathcal{E}$ 替代了这一范式。

给定一组细粒度块 $\{c_1, c_2, \ldots, c_m\}$，压缩编码器将其嵌入直接映射为单个压缩高层嵌入：

$$e(c_{\text{high}}) = \mathcal{E}(c_1, c_2, \ldots, c_m) \in \mathbb{R}^d$$

该嵌入捕获了这些细粒度块聚合后的高层语义，而无需生成任何显式文本摘要。压缩编码器的训练目标是使其输出逼近LLM摘要的嵌入。具体而言，设LLM对同一组块生成的摘要为 $\hat{s}$，其嵌入为 $e_{\text{gt}} = \epsilon(\hat{s})$，则压缩损失定义为：

$$\mathcal{L}_{\text{comp}}(S) = \| e_{\text{comp}} - e_{\text{gt}} \|_2^2$$

其中 $S$ 为可训练的压缩模型，$e_{\text{comp}} = S(\epsilon(c_1), \dots, \epsilon(c_m))$。通过最小化这一L2距离，压缩编码器学会了在嵌入空间中直接“模拟”摘要的语义表征，从而在推理时完全避免LLM调用，显著降低了高层块生成的成本（Section 4.3）。

消融实验验证了这一设计的价值：使用GPT摘要生成高层嵌入的变体（w/o $\mathcal{E}$ summarize）虽然取得了最高的检索召回率0.861，但其货币成本高达$0.204；而压缩编码器以$0.078的成本实现了0.829的召回率，展现了极高的性价比（Table 2）。

### STITCH训练框架：稳定多目标优化的RL↔SFT循环

规划器面临一个具有挑战性的多目标优化问题：需要同时平衡答案准确率、检索成本和推理效率。此外，直接使用强化学习（RL）训练规划器面临稀疏奖励和训练不稳定的困境，而纯监督微调（SFT）又需要大量高质量标注数据。STITCH（Solve with RL, Then Imitate To Close Holes）框架通过交替执行三种训练阶段来解决这些问题。

**多目标优化目标**。整个SMARTCHUNK系统的优化目标可形式化为：

$$\max_\pi \mathbb{E}_{(q, D, \hat{a}) \sim \mathcal{D}} \left[ \text{Acc}(\mathcal{G}(q, \pi(q, C))), \hat{a}) - \lambda \tau((\mathcal{G}, \pi \mid q, D)) \right]$$

其中 $\pi$ 为规划器策略，$\mathcal{G}$ 为答案生成器，$\text{Acc}$ 衡量答案准确率，$\tau$ 为成本函数，$\lambda$ 控制准确率与效率的折衷（Section 3）。

**策略更新目标**。STITCH采用基于GRPO（Group Relative Policy Optimization）的策略更新目标。对于每个查询，采样 $G$ 条轨迹，策略参数 $\theta$ 的优化目标为：

$$\mathcal{T}_{\mathrm{STITCH}}(\theta) = \mathbb{E}_{(q, \rho, a) \sim \mathcal{D}, \{\sigma_i\}_{i=1}^G \sim \pi_{\mathrm{add}}(\cdot|(q, \rho))} \left[ \frac{1}{G} \sum_{i=1}^G \frac{1}{|o_i|} \sum_{t=1}^{|\alpha_i|} \left( \min\left( r_{i,t}(\theta) \hat{A}_{i,t}, \mathrm{clip}\left( r_{i,t}(\theta), 1-\varepsilon, 1+\varepsilon \right) \hat{A}_{i,t} \right) - \beta D_{\mathrm{KL}}(\pi_{\theta}||\pi_{\mathrm{ref}}) \right) \right]$$

其中重要性采样比率和组归一化优势分别定义为：

$$r_{i,t}(\theta) = \frac{\pi_{\theta}(o_{i,t}|q, \rho, o_{i<t})}{\pi_{\text{old}}(o_{i,t}|q, \rho, o_{i<t})}, \quad \hat{A}_{i,t} = \frac{R_i - \text{mean}(\{R_i\})}{\text{std}(\{R_i\})}$$

该目标结合了剪切优势（clip）以稳定更新，以及KL散度惩罚项（系数 $\beta$）以防止策略偏离参考策略过远（Section 4.2, Eq. 1-2）。

**多目标奖励设计**。每条轨迹的奖励 $R$ 由四个分量加权组成：

$$R = R_{\mathrm{QA}} + R_{\mathrm{Cost}} + R_{\mathrm{Format}} + R_{\mathrm{Length}}$$

其中 $R_{\mathrm{QA}}$ 衡量答案正确性，$R_{\mathrm{Cost}}$ 惩罚过度的块使用，$R_{\mathrm{Format}}$ 和 $R_{\mathrm{Length}}$ 分别约束输出格式和推理长度，并包含伪标签对齐奖励（Section 4.2, Section G.2）。

**三阶段训练循环**。STITCH的核心训练流程（Algorithm 2）包括：
1. **Vanilla RL rollout**：标准RL探索，收集成功轨迹；
2. **Hinted RL rollout**：为RL中失败的案例提供提示（hint），引导策略学习正确行为；
3. **Imitation learning**：将前两阶段收集的成功轨迹用于监督微调，巩固学习成果。

这一设计的关键在于“先解后仿”：RL负责探索和发现有效策略，而模仿学习负责稳定和泛化这些策略。实验表明，纯RL训练的规划准确率仅为0.356，SFT+RL在监督token减半时性能崩溃（从0.763降至0.544），而STITCH仅用一半的监督token（418k）即达到82.0%的规划准确率和0.564的QA准确率，相比最强SFT+RL基线提升约5个百分点（Table 4, Table 5）。

## 实验与分析

### 主要结果：高性价比的检索-问答权衡

SMARTCHUNK 的核心优势在于以显著降低的成本达到匹配或超越最先进基线的问答准确率。表 2 汇总了各方法在 NarrativeQA、QASPER、QuALITY 和 Natural Questions 四个基准上的平均表现。SMARTCHUNK 取得了 **0.564 的 QA 准确率**，与最强基线 MAL RAG（Zheng et al., 2025）的 0.561 基本持平，同时检索召回率达到 **0.829**（MAL RAG 为 0.842）。然而，成本差异是决定性的：SMARTCHUNK 的货币成本仅为 **$0.078**，不到 MAL RAG（$0.301）的 30%，延迟也从 5.44 秒降至 **3.62 秒**。这一结果直接验证了查询感知分块压缩策略的有效性——系统无需为每个查询构建完整的递归摘要树，而是通过规划器预测的最小/最大级别精准约束检索空间。

图 1 的散点图直观展示了这一权衡：SMARTCHUNK 位于左上角区域，即高准确率-低成本区间，与 RAPTOR（Sarthi et al., 2024）、GRAG（Edge et al., 2024）等基于树/图的多级方法形成鲜明对比。单级固定分块方法（如 512 token 分块、句子级分块）虽然成本极低（约 $0.007），但 QA 准确率仅约 0.25–0.36，暴露了固定粒度无法适应异质查询的根本瓶颈。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/001_Figure_1.jpg]]
*Figure 1: QA accuracy vs. Monetary cost across methods. SMARTCHUNK achieves higher accuracy with lower cost compared to state-of-the-art baselines*

图 4a 进一步展示了 SMARTCHUNK 在各基准上相对基线的性能差距（正值表示 SMARTCHUNK 更优）。在 NarrativeQA 上，SMARTCHUNK 比 GRAG 高出近 8 个百分点；在 Natural Questions 上同样保持正向优势。这表明规划器能够针对不同文档类型和查询复杂度自适应调整检索粒度。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/006_Figure_4.jpg]]
*Figure 4: (a) Performance gaps of SmartChunk over competing methods on four benchmarks—NarrativeQA (ROUGE), QASPER (F1), QuALITY (Accuracy), and Natural Questions (F1); positive bars mean SmartChunk outperforms the baseline. (b) Average chunk sizes (tokens) selected by our planner across datasets, illustrating dataset-/query-adaptive behavior*

### 域外泛化：NewsQA 实验

为验证方法的泛化能力，论文在域外数据集 NewsQA 上进行了评估（表 3）。SMARTCHUNK 结合小样本提示（few-shot prompting）取得 **0.906 的 F1 分数**，与 MAL RAG 的 0.907 几乎一致，但成本仅为 **$0.032**，约为 MAL RAG（$0.147）的 22%。这一结果表明，规划器学习到的自适应分块策略并非过拟合于训练域，而是捕捉到了可迁移的查询-文档粒度匹配规律。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/009_Table_3.jpg]]
*Table 3: Performance on out-of-domain dataset NewsQA*

### 成本分析：训练开销与推理扩展性

图 3 展示了总成本（训练+推理）随查询量变化的曲线。SMARTCHUNK 因规划器和压缩编码器训练产生约 $15 的固定前期成本，但其测试时成本增长极为缓慢。当查询量超过约 2000 条时，SMARTCHUNK 的总成本开始低于 MAL RAG，且差距随规模扩大而持续拉大。这一特性使 SMARTCHUNK 在大规模部署场景中具有显著的工程价值。

### 消融实验：各模块的必要性

表 2 的消融变体揭示了规划器和压缩编码器的各自贡献：

- **移除规划器（w/o P）**：系统退化为始终构建完整分块树，成本显著增加，验证了规划器对检索空间约束的关键作用。
- **移除压缩编码器并直接编码原始文本（w/o ε direct encode）**：检索与 QA 性能明显下降，说明压缩编码器生成的高层语义嵌入比直接编码原始文本更有效。
- **使用 GPT 摘要生成高层嵌入（w/o ε summarize）**：该变体取得了最高的检索召回率 **0.861**，但成本高达 **$0.204**，凸显了压缩编码器的高性价比优势——以微小的召回率损失换取约 62% 的成本降低。

### 规划器训练策略对比：STITCH 的有效性

表 4 的消融分析了微调和推理组件对规划器性能的影响。完整的“微调+推理”方案达到 **82.0% 的规划准确率**，推理延迟为 0.848 秒。去除微调后，即使使用 LLM 加小样本提示，准确率也仅为 42.6%；去除推理组件改用 MLP 分类器，准确率降至 60.9%，尽管延迟极低（0.0003 秒）。这表明规划器需要同时具备推理能力和任务特定的微调。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/011_Table_4.jpg]]
*Table 4: Ablation study showing the effect of planner, finetuning, and reasoning components on planning accuracy, cost, QA accuracy, and latency. Our full system achieves the best performance across all metrics. Table 5: Comparison of training strategies for the planner. The details of baselines are shown in Section E*

表 5 对比了不同训练策略。纯强化学习（RL）训练的规划器准确率仅 **0.356**，几乎失效；SFT+RL 在监督 token 减半时性能从 0.763 崩溃至 0.544。相比之下，STITCH 仅使用一半的监督 token（418k vs 795k）即达到 **0.820 的规划准确率**和 **0.564 的 QA 准确率**，验证了其“RL 先行探索、模仿学习填补漏洞”的稳定训练机制。

图 7 展示了 STITCH 的训练动态：训练奖励逐步上升，测试规划准确率收敛至约 80%，表明训练过程稳定且未出现灾难性遗忘。

### 自适应粒度选择的实证证据

图 4b 和图 5 共同验证了规划器的自适应行为。图 4b 显示，规划器在不同数据集上选择的平均块大小差异显著：NarrativeQA 约 1750 token，QASPER 约 250 token，QuALITY 约 175 token，Natural Questions 约 800 token。图 5 的小提琴图进一步展示了最小/最大块级别在各数据集上的分布差异，证实查询对粒度的需求高度异质，固定分块策略无法满足这一需求。

### 与其他 RAG 改进的兼容性

图 6 显示，将 SMARTCHUNK 与延迟分块（late chunking）和混合搜索（hybrid search）结合后，QA 准确率进一步提升。这说明 SMARTCHUNK 的规划器-压缩编码器架构是模块化的，可与正交的检索增强技术叠加使用。

### 失败模式与局限性

尽管整体表现优异，SMARTCHUNK 在某些场景下并非最优：

- **事实匹配型数据集**：在 QuALITY 等主要依赖直接实体/事实匹配的数据集上，GRAG 等基于图谱的方法可能表现更好，因为层次推理的优势在此类任务中有限。
- **规划器依赖伪标签质量**：STITCH 的训练依赖伪标签生成管道，当监督信号质量不足时，规划器性能可能受影响（此点需结合具体伪标签生成细节进行手动验证）。
- **压缩编码器的语义保真度**：压缩编码器以 LLM 摘要嵌入为训练目标，可能无法完美捕捉所有文档类型的高层语义，尤其在高度专业化或结构化文档中。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/004_Table_1.jpg]]
*Table 1: Dataset statistics used in our evaluation. The datasets span diverse domains and query types, with NewsQA serving as an out-of-domain benchmark. Table 2: Comparison of different chunking and retrieval strategies. Our method achieves competitive QA accuracy and retrieval recall while significantly reducing monetary cost and latency*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/003_Table_1.jpg]]

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/010_Table_4.jpg]]

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/013_Table_6.jpg]]
*Table 6: The monetary cost of each model*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/016_Table_7.jpg]]
*Table 7: Trace diversity We also demonstrate the importance of using diverse reasoning trace for finetuning planner. Table 7: Comparison of planner training methods. STITCH achieves the highest planning accuracy while using fewer tokens*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/018_Table_8.jpg]]
*Table 8: SMARTCHUNK outperforms other baselines and nearly reaches the accuracy of DeepSeek-R1-Distill, which has the benefit of vast training data. There is no DeepSeek-R1-Distill for Qwen-3B provided by (Guo et al. (2025)), so its cells are left blank*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_Myti1QwL2t/figures/019_Table_9.jpg]]
*Table 9: QA performance for each dataset separately*

## 方法谱系与知识库定位

### 与现有方法的谱系关系

SMARTCHUNK 位于文档检索增强生成（RAG）方法谱系中“多级自适应检索”分支，其核心设计直接回应了固定分块与平面检索的两大瓶颈：**单一粒度无法适应异质查询与文档结构**，以及**多级表示构建成本过高**。

**上游基线对比。** 论文将现有方法分为两大类进行系统对比：

- **单级固定分块方法**：包括句子级分块（Kamradt 2024; LangChain team 2023）、512-token 固定分块（Lewis et al., 2020）以及延迟分块（Late Chunking, Günther et al., 2024）。这类方法检索召回率极低（平均约 0.25–0.36），因为固定粒度无法同时捕捉细粒度事实和跨段落推理线索。SMARTCHUNK 相对这些方法在 QA 准确率上实现了**最高约 30% 的提升**（Section 5.2）。

- **多级树/图方法**：包括 RAPTOR（Sarthi et al., 2024）的递归嵌入-聚类-摘要树、MAL RAG（Zheng et al., 2025）的多级抽象检索，以及 GRAG（Edge et al., 2024）的图谱增强检索。这些方法虽然通过多粒度表示提升了检索质量，但**依赖 LLM 生成摘要文本再嵌入**来构建高层表示，导致高昂的 API 成本。SMARTCHUNK 的核心差异化在于：用**压缩编码器直接聚合细粒度块嵌入**替代 LLM 摘要，同时引入**规划器预测查询所需的最优块级别范围**，避免构建完整的层级树。

**性能-效率权衡的重新定义。** 在四个基准数据集上的平均结果显示：SMARTCHUNK 以 **$0.078 的货币成本**（MAL RAG 的 26%）和 **3.62s 的延迟**，达到了 **0.564 的 QA 准确率**和 **0.829 的检索召回率**，与 MAL RAG（0.561 / 0.842 / $0.301）性能可比但成本大幅降低（Table 2）。Figure 1 的散点图直观展示了这一“高性价比”定位：SMARTCHUNK 位于准确率-成本 Pareto 前沿。

**训练范式的创新。** 规划器的训练面临双重挑战：缺乏直接监督信号（没有“正确块级别”的标注），以及纯强化学习训练的不稳定性。STITCH 框架通过**交替执行普通 RL、提示化 RL 和模仿学习（SFT）**，在仅使用 SFT+RL 基线一半监督 token 的情况下，将规划准确率从 0.763 提升至 **0.820**（Table 5）。纯 RL 训练的规划准确率仅 0.356，而 SFT+RL 在监督 token 减半时性能崩溃至 0.544，这验证了 STITCH 在稳定多目标优化中的关键作用。

### 适用边界与局限

尽管 SMARTCHUNK 在长文档 QA 场景展现了显著的成本优势，其适用边界存在以下约束：

1. **事实匹配型数据集的劣势**：在 QuALITY 等主要依赖直接实体/事实匹配的数据集上，GRAG 等基于图谱的方法可能表现更优。这是因为此类问题不需要层次推理，SMARTCHUNK 的自适应粒度规划反而可能引入不必要的复杂性（Section 5.3, Figure 4a）。

2. **规划器对伪标签质量的依赖**：STITCH 训练的伪标签生成管道（通过 LLM 回溯最优块级别）是规划器性能的上限。若伪标签质量不足，规划器可能学到次优策略。论文通过使用多种 LLM 生成多样化推理轨迹来缓解此问题（Table 7），但未完全消除该风险。

3. **压缩编码器的语义保真度限制**：压缩编码器通过最小化与 LLM 摘要嵌入的 L2 距离来训练（$\mathcal{L}_{\text{comp}}(S) = \| e_{\text{comp}} - e_{\text{gt}} \|_2^2$，Section 4.3）。消融实验显示，直接使用 GPT 摘要生成高层嵌入的变体（w/o ε summarize）取得了最高检索召回率 **0.861**，但成本高达 $0.204（Table 2）。这表明压缩编码器在语义保真度上存在可量化的折衷——以约 3.7% 的召回率下降换取 62% 的成本降低。

4. **任务泛化性待验证**：当前评估集中在 NarrativeQA、QASPER、QuALITY、Natural Questions 四个长文档 QA 基准，以及 NewsQA 作为域外测试。在对话式检索、事实验证、多跳推理等其他知识密集型任务上的表现尚未系统评估。

### 开放问题与未来方向

论文明确指出了两个值得探索的方向：

- **复杂推理场景的扩展**：将 SMARTCHUNK 应用于深度研究（deep research）、多跳开卷问答等需要更长推理链的场景，验证规划器在更大搜索空间中的有效性。

- **多模态文档检索**：在共享嵌入空间中结合 STITCH 进行图像-文本联合理解，实现多模态文档的自适应分块与检索。这要求压缩编码器能够处理跨模态的语义聚合。

此外，从方法谱系角度看，以下问题值得关注：规划器当前仅预测最小/最大块级别，未显式建模文档内部的结构异质性（如某些段落需要细粒度、某些需要粗粒度）；压缩编码器的训练目标（模仿 LLM 摘要嵌入）可能限制了其发现比文本摘要更优的检索表示的可能性。

## 原文 PDF

![[paperPDFs/ICLR_2026/SmartChunk_Retrieval_Query_Aware_Chunk_Compression_with_Planning_for_Efficient_Document_RAG.pdf]]
