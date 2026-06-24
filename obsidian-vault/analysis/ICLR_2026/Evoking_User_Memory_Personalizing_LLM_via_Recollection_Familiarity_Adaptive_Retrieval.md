---
title: "Evoking User Memory: Personalizing LLM via Recollection-Familiarity Adaptive Retrieval"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Evoking_User_Memory_Personalizing_LLM_via_Recollection_Familiarity_Adaptive_Retrieval.pdf
aliases:
- RMRFMR
- EUMPLRFAR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "利用探测检索的均值相似度和熵联合估计熟悉度不确定性，通过双阈值门控策略（θ_high, θ_low, τ）自适应选择熟悉度路径（一次top-K）或回忆路径（迭代聚类-α混合查询扩展）。"
primary_logic: "将认知科学中的回忆-熟悉度双过程理论映射为检索器的双路径设计：当熟悉度高时采用快速识别，当熟悉度低或熵高时启动需要线索重构的回忆检索，从而模仿人类记忆的自适应特性。"
claims:
- "RF-Mem 在 PersonaMem 三个记忆规模（32K/128K/1M）上整体准确率均显著优于全上下文和密集检索基线，且平均输入令牌量远低于全上下文，延迟接近一次性检索。"
- "在 PersonaBench 和 LongMemEval 上的 recall 指标上，RF-Mem 在 Recall@5/10 上取得最佳平衡，延迟介于 Familiarity 与 Recollection 之间，同时超越了两种单一路径。"
- "消融分析显示，熟悉度路径擅长事实型查询，回忆路径对上下文密集型任务更强，而 RF-Mem 通过自适应切换集合了两者优势，在多个类别中取得最优。"
- "理论分析证明，基于均值和熵的双阈值策略在单调策略类中最小化检索风险，且门控错误率随探测大小 K 增大呈指数下降，验证了机制的可靠性。"
---

# Evoking User Memory: Personalizing LLM via Recollection-Familiarity Adaptive Retrieval

> [!tip] 核心洞察
> 将认知科学中的回忆-熟悉度双过程理论映射为检索器的双路径设计：当熟悉度高时采用快速识别，当熟悉度低或熵高时启动需要线索重构的回忆检索，从而模仿人类记忆的自适应特性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 唤起用户记忆：基于回忆-熟悉度自适应检索的个性化大语言模型 |
| 英文题名 | Evoking User Memory: Personalizing LLM via Recollection-Familiarity Adaptive Retrieval |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=f7p0F2X6XN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | RF-Mem (Recollection–Familiarity Memory Retrieval) |
| Dataset | PersonaMem (32K), PersonaMem (1M), PersonaBench (MiniLM), LongMemEval-S (BGE) |

> [!tip] 效果简介
> - PersonaMem (32K) 上，Overall Accuracy 为 0.6350 (RF-Mem)，对比 0.6129 (Full Context)，变化 +0.0221。
> - PersonaMem (1M) 上，Overall Accuracy 为 0.4589 (RF-Mem)，对比 0.4518 (Dense Retrieval)，变化 +0.0071。
> - PersonaBench (MiniLM) 上，Recall@10 Overall 为 0.6071 (RF-Mem)，对比 0.5964 (Familiarity)，变化 +0.0107。

## 概述

现有的大语言模型个性化方案普遍依赖单一的相似度检索，难以有效应对模糊查询与长尾记忆：快速检索容易遗漏关键上下文，而将全部用户历史输入模型则带来高昂的延迟和计算开销。针对这一瓶颈，本文提出 **RF-Mem（Recollection–Familiarity Memory Retrieval）**，一种受人类记忆双过程理论启发的自适应检索系统。

RF-Mem 将认知科学中的“熟悉度—回忆”机制映射为两条检索路径：熟悉度路径执行一次性 Top‑K 相似度检索，模拟快速识别；回忆路径通过迭代检索‑聚类‑α混合查询扩展，模拟线索驱动的渐进式重建。系统首先进行一次探测检索，利用归一化相似度的均值和熵联合估计当前查询的熟悉度不确定性，再通过双阈值门控（θ_high, θ_low, τ）动态选择检索路径，从而在“高效”与“深度”之间实现自适应切换。

在 PersonaMem（32K/128K/1M 三种记忆规模）、PersonaBench 和 LongMemEval 三个基准上，RF-Mem 的整体准确率均显著优于全上下文输入和标准密集检索，且平均输入令牌量远低于全上下文、检索延迟接近纯熟悉度检索（Table 1–3）。消融分析进一步表明，熟悉度路径对事实型查询表现优异，回忆路径对上下文密集型任务更强，而 RF-Mem 通过自适应路由将两者优势互补，并在替换聚类方法与混合策略的实验中展现出对实现细节的高度鲁棒性（Table 15, Table 16）。理论分析证明，所提出的基于均值和熵的双阈值策略在单调策略类中可最小化检索风险，门控错误率随探测规模 K 增大呈指数下降，为方法的可靠性提供了形式化支撑（Appendix F.1）。

综上，RF-Mem 在不增加复杂训练或额外模型的前提下，以轻量、即插即用的方式为个性化大语言模型提供了一种兼顾精度与效率的记忆检索机制。

## 背景与动机

个性化大语言模型能否真正唤起用户的长期记忆，取决于检索系统能否在庞大的历史对话中精准、高效地定位与当前查询相关的片段。随着记忆规模增长，这一挑战变得尤为突出：全量上下文（Full Context）虽能保留完整信息，但输入令牌量随记忆规模线性膨胀，在超出 LLM 上下文窗口（如 128K、1M 记忆）时完全不可用（Table 1 中标为 OOC）；而现有广泛采用的密集检索（Dense Retrieval）仅依靠单次 top‑K 相似度匹配，本质上是一种“熟悉度”驱动的快速识别。当查询模糊、证据稀疏或需要跨多条记忆的推理时，这种单一检索路径便暴露了明确的瓶颈——检索不足则遗漏关键证据，扩大 top‑K 又引入大量噪声，导致生成质量下降（Table 1 中 Dense Retrieval 在 1M 规模的整体准确率仅为 0.4518，远低于全量上下文在 32K 时的表现）。

人类记忆的双过程理论（Yonelinas 2024）为此提供了直接的认知启发：记忆提取并非只有“熟悉感”（familiarity）驱动的快速辨认，还包括需要线索重组的“回忆”（recollection）过程——当熟悉度信号弱或信息熵高时，大脑会主动进行结构化的逐轮重构，以恢复那些未被直接激活的记忆。然而，当前个性化 LLM 的检索模块普遍缺失这一回忆路径，更没有根据检索不确定性在两种过程间自适应切换的机制，导致系统要么浪费计算资源（总是进行深度检索），要么在需要深度联想时力不从心。

本文的核心动机正是填补这一缺口：将回忆‑熟悉度双过程理论映射为检索器的双路径设计，使得模型能够模拟人类记忆的自适应特性——在高熟悉度下采用一次性 top‑K 快速返回证据，在低熟悉度或检索不确定性高时启动迭代聚类与 α‑混合查询扩展的回忆路径（Eq. 3），从而以接近单次检索的延迟实现比肩全量上下文的准确性。这一设计在认知上可解释、在工程上模块化，并在一系列基准上展现出显著的性能‑效率平衡：在 PersonaMem 的 32K 设置下，RF‑Mem 以平均 3566.6 tokens 的输入量取得 0.6350 的整体准确率，优于全量上下文（0.6129，24657.8 tokens）；在 1M 大规模记忆中，同样超越密集检索（0.4589 vs. 0.4518），并在 PersonaBench、LongMemEval 的 Recall@5/10 指标上持续取得最佳或次优结果（Table 1–Table 3）。上述证据表明，补全回忆路径并赋予自适应切换能力，是打破现有检索瓶颈、实现高效深层个性化化的关键杠杆。

## 核心创新

RF‑Mem 的关键创新在于将认知科学中的**回忆‑熟悉度双过程理论**映射为检索器的**自适应双路径架构**，解决了现有个性化 LLM 检索系统缺乏回忆路径和动态切换能力的瓶颈。标准密集检索（Dense Retrieval）仅依赖单次固定的 top‑K 相似度匹配（对应“熟悉度”快速识别），面对模糊查询或长尾知识时要么检索不足，要么因全量输入成本过高而导致噪声；RF‑Mem 通过在一个统一的门控框架中引入回忆路径，并依据探测检索的**熟悉度不确定性**（均值相似度、熵）决定何时启动该路径，从而模仿人类记忆在“知道”与“回想”之间的自适应特性 [Figure 1, Figure 2]。

### 相对基线的变化点（Changed Slots）

| 维度 | 基线值 | RF‑Mem 方案 | 证据锚点 |
|------|--------|-------------|----------|
| **检索模式** | 固定单次 top‑K 相似度检索（Familiarity） | 基于熟悉度不确定性的自适应双路径选择：高熟悉度直接返回 top‑K，低熟悉度或高熵触发回忆检索 | Eq. (3)，Table 1, Table 2 |
| **回忆路径机制** | 无（仅熟悉度） | 多轮检索‑聚类‑α混合查询扩展，逐步重建证据链：在嵌入空间中对候选记忆聚类，将查询、簇质心、原始查询加权混合生成下一轮探针，模拟线索驱动的逐轮回忆 | Eq. (5)–(6)，Algorithm 3，Table 15 |

#### 1. 检索模式：从固定到自适应门控

基线方法对所有查询无差别地执行一次 top‑K 相似度检索，完全依赖嵌入相似度的单峰值匹配，无法区分“有把握识别”与“需要深层回想”的场景。RF‑Mem 首先通过一次探测检索得到候选记忆列表，计算归一化相似度分布 $p_i$ 及其熵 $H(p)$（Eq. (1)–(2)），联合均值相似度 $\bar{s}$ 一同作为熟悉度的不确定性度量。随后，一个**双阈值门控策略**（Eq. (3)）根据 $\bar{s}$ 与 $\theta_{\text{high}}$、$\theta_{\text{low}}$ 的比较，以及当 $\bar{s}$ 处于中间区域时用熵阈值 $\tau$ 进行二次判别，动态选择熟悉度路径（直接 top‑K，Eq. (4)）或回忆路径。这一设计使得检索深度由查询与记忆的实际匹配质量驱动，避免了不必要的深度检索，实现了精度‑效率的平衡。实验数据表明：RF‑Mem 在 PersonaMem 三个记忆规模上的整体准确率均显著优于全上下文和密集检索基线（Table 1），同时平均输入令牌量远低于全上下文（32K 下 3 566 vs 24 658 tokens），且检索延迟接近单次熟悉度检索（32K 下 5.09 ms vs 4.09 ms），佐证了自适应切换的有效性。

#### 2. 回忆路径：迭代聚类‑混合查询的线索重构

当门控判定需要回忆时，RF‑Mem 不再仅依赖一次 top‑K 返回，而是启动一个**多轮检索‑聚类‑α混合**过程（Section 2.3）。该路径将前一轮检索到的候选记忆进行 KMeans 聚类，计算各簇的质心作为记忆分支点（Eq. (5)），然后将当前查询向量、簇质心向量和原始查询向量按 $\alpha$ 比例混合并归一化，生成下一轮检索的探针（Eq. (6)）。这一“线索‑重构”循环相当于在嵌入空间中沿着语义相关的记忆链条逐步展开证据，能够找回单次相似度检索遗漏的上下文关联记忆。最终选取所有轮次中的 top‑K 记忆片段构成的并集作为回忆证据。消融实验表明，仅使用回忆路径在上下文密集型问题上更强，而熟悉度路径在事实型问题上占优；RF‑Mem 通过门控整合两者，在不同问题类型上均取得最优（Appendix D.1, Figure 18–19）。此外，当替换聚类方法或混合策略时，RF‑Mem 仍持续优于单一路径，验证了α‑混合和自适应框架的鲁棒性（Table 15）。

### 支撑创新的关键证据

- **整体性能优势**：在 PersonaMem 32K/128K/1M 上，RF‑Mem 的整体准确率分别为 0.6350（vs Full Context 0.6129）、0.5394（vs Dense Retrieval 0.5286）和 0.4589（vs Dense Retrieval 0.4518），且平均输入令牌和检索延迟接近最轻量的熟悉度检索（Table 1）。在 LongMemEval‑S 上 Recall@5 达到 0.8186，超越 Familiarity 的 0.7924（Table 3），在保持高召回的同时平衡了效率。
- **自适应切换的有效性**：理论分析证明，基于均值和熵的双阈值策略在单调策略类中能够最小化检索风险，且门控错误概率随探测大小 $K$ 呈指数下降（Theorem 1, Proposition 2）。实践中，学习型门控分类器仅用 128K 训练样本即可达到与手动阈值接近的准确率（0.5175 vs 0.5199），说明熟悉度信号本身携带了足够的路径区分信息（Table 14）。
- **模块化与鲁棒性**：RF‑Mem 可作为在线检索层叠加在 MemoryBank 等异构记忆索引之上，此时整体准确率仍达到 0.5314，且在各种聚类策略和混合超参数下的 Recall 保持稳定（Table 4, Table 15, Figure 14），表明该自适应框架对外部索引和实现细节不敏感，便于迁移部署。

RF‑Mem 的核心贡献在于提出了首个基于回忆‑熟悉度双过程的自适应检索机制，通过不确定度门控将“快速识别”与“深层回忆”无缝衔接，在个性化对话场景中实现了检索深度与计算开销的精细化权衡。该方法不仅突破了单一次数检索的性能上限，还为长时记忆系统提供了一种可解释、可扩充的认知启发检索范式。

## 整体框架

![[assets/figures/papers/iclr26_0016_f7p0F2X6XN_Evoking_User_Memory_Personalizing_LLM_via_Recoll/figures/002_Figure_2.jpg]]
*Figure 2: The overall architecture of RF-Mem. A dual-process memory retrieval system dynamically switches between the Familiarity and the Recollection paths*

RF-Mem 的设计源于认知科学中的回忆‑熟悉度双过程理论：人类面对熟悉信息时依靠快速的熟悉度识别，而面对模糊或低频线索时则启动需要持续线索重构的回忆过程。对应地，RF-Mem 将记忆检索系统组织为两条路径——快速单次的 Familiarity 路径与多轮迭代的 Recollection 路径——并由一个基于检索不确定性的门控模块实现自适应切换。系统整体以对话历史或用户记忆库的嵌入向量为索引，对每个用户查询动态输出一组最相关的记忆片段，最终将片段原文与查询拼接后送入大语言模型（LLM）生成回答（图 Figure 2）。

### 1. 输入与索引
系统的输入为一个查询向量 $\mathbf{x}_t$（通常由用户问题经嵌入模型编码得到）以及一个静态的记忆嵌入索引 $\{\mathbf{z}_i\}_{i=1}^{M}$，其中 $M$ 为记忆片段总数。记忆索引可以来自原始对话分块、摘要索引或其它异构记忆库，RF-Mem 作为检索层叠加在索引之上，本身不修改索引构建方式。

### 2. 探测检索与不确定性估计
查询首先进入**探测检索（Probe Retrieval）**模块：在嵌入空间中计算 $\mathbf{x}_t$ 与所有记忆向量 $\mathbf{z}_i$ 的余弦相似度，取 top‑$K$ 作为初始候选列表 $\{(m_i, s_i)\}$。为了量化“当前查询对记忆库的熟悉程度”，系统对 $K$ 个相似度进行温度 $\lambda$ 的 softmax 归一化：

$$ p_i = \frac{\exp(\lambda (s_i - \max_j s_j))}{\sum_{j=1}^{K} \exp(\lambda (s_j - \max_j s_j))}, \quad i = 1, \ldots, K \tag{Eq. (1)} $$

并计算该分布的**熵** $H(p) = -\sum_{i=1}^{K} p_i \log p_i$（Eq. (2)），同时记录均值相似度 $\bar{s}$。熵高意味着证据分散、不确定性大；均值低则表明整体相似度弱，二者共同构成了熟悉度不确定性的代理信号。

### 3. 策略门控
**策略门控（Strategy Gate）**根据 $\bar{s}$ 和 $H(p)$ 执行双阈值决策（Eq. (3)）：

$$ \mathrm{Strategy}(q) = \begin{cases}
   \mathrm{Familiarity}, & \bar{s} \geq \theta_{\mathrm{high}} \\
   \mathrm{Recollection}, & \bar{s} \leq \theta_{\mathrm{low}} \\
   \begin{cases}
       \mathrm{Familiarity}, & H(p) \leq \tau \\
       \mathrm{Recollection}, & H(p) > \tau
   \end{cases}, & \theta_{\mathrm{low}} < \bar{s} < \theta_{\mathrm{high}}
\end{cases} $$

当查询高度熟悉（$\bar{s}$ 足够高）时直接启用熟悉度路径；当查询明显陌生（$\bar{s}$ 足够低）时直接启用回忆路径；中间情形则由熵 $\tau$ 决定：低熵意味着候选分布集中，仍走熟悉度路径；高熵意味着证据冲突或分散，触发更深入的回忆检索。该策略在理论上被证明是单调策略类中检索风险最小的方案，且门控错误率随探测规模 $K$ 呈指数衰减。

### 4. 熟悉度路径（Familiarity Retrieval）
若选择熟悉度路径，系统直接将探测检索得到的 top‑$K$ 候选作为最终记忆证据：

$$ \mathcal{C}_t = \mathrm{Top-}K \big( \{ (m_i, \langle \mathbf{x}_t, \mathbf{z}_i \rangle) \}_{i=1}^{M} \big) \tag{Eq. (4)} $$

该路径仅需一次全库相似度检索，延迟极低，适合事实记忆或高度匹配的简单查询。

### 5. 回忆路径（Recollection Retrieval）
回忆路径模拟线索驱动的逐步重建。其核心是一个多轮“检索‑聚类‑$\alpha$混合查询生成”循环（Algorithm 3）：

1. **检索**：以当前探针 $\mathbf{x}^{(r)}$（首轮 $\mathbf{x}^{(0)} = \mathbf{x}_t$）从记忆库中检索 top‑$K$ 候选；
2. **聚类**：对候选记忆的嵌入向量执行 $B$ 类 K‑Means 聚类，得到簇质心 $\mathbf{g}_b^{(r)}$（Eq. (5)）；
3. **查询扩展**：对每个簇，将原始查询、当前探针与质心按 $\alpha$ 混合并归一化，生成下一轮的探针：

$$ \mathbf{x}_b^{(r+1)} = \mathrm{norm}\big( \alpha \mathbf{x}^{(r)} + (1-\alpha) \mathbf{g}_b^{(r)} + \mathbf{x}_t \big), \quad \alpha \in [0,1] \tag{Eq. (6)} $$

4. 返回步骤 1，以每个混合探针并行进入下一轮检索，直至达到预设的轮次上限 $R$ 或提前停止条件（例如簇内相似度过高）。

所有轮次中收集的候选集经合并与去重后，取最终 top‑$K$ 作为回忆证据：

$$ \mathcal{C}_t = \mathrm{Top-K}\Big( \bigcup_{r=0}^{R} \mathcal{C}^{(r)} \Big) $$

聚类旨在将相关记忆聚拢并围绕各“记忆分支”生成新探针，$\alpha$‑混合在保留原始意图、当前焦点与聚类上下文之间进行插值，使得系统能逐步捞出长尾、模糊但上下文相关的记忆片段。

### 6. 记忆文本提取与生成
无论走哪条路径，最终得到的记忆索引集合 $\mathcal{C}_t$ 均映射回对应的原始文本片段（对话轮次或文档块）。这些文本按相似度或轮次顺序拼接，作为上下文附在用户查询之后，输入 LLM 完成生成。此步骤完全与检索解耦，不引入额外 LLM 调用。

### 7. 自适应效率与模块化
框架的默认参数（例如 $\lambda = 20$, $B = 3$, $\theta_{\mathrm{high}} = 0.6$, $\theta_{\mathrm{low}} = 0.3$）在实践中无需精细调整，就能在宽泛的 $\alpha \in [0.3, 0.7]$、$\tau \in [0.1, 0.3]$ 范围内保持稳定的检索性能。由于绝大多数查询由低延迟的 Familiarity 路径处理，RF-Mem 的平均检索时延接近一次性密集检索，显著低于全上下文或全时回忆策略，但通过按需深度检索，又在长尾和模糊问题上显著提高了证据覆盖（Recall）与生成准确性。整个系统以模块化方式设计，可作为检索层叠加在任意静态或动态记忆索引之上，不依赖索引的具体构造方式。

## 核心模块与公式推导

RF-Mem 将认知科学中的“回忆-熟悉度”双过程理论映射为检索器的双路径设计，其核心架构由五个模块串联构成（见图2）。以下按数据流顺序逐一阐述各模块的功能及其关键公式。

### 2.1 探测检索与熟悉度不确定性
给定用户查询嵌入 $\mathbf{x}_t$，系统首先执行一次轻量级的探测检索（Probe Retrieval），从记忆库 $\{(\mathbf{z}_i, m_i)\}_{i=1}^M$ 中返回 Top-$K$ 个候选记忆片段及其余弦相似度 $s_i = \langle \mathbf{x}_t, \mathbf{z}_i \rangle$。为了将原始分数转化为可比较的概率分布，对相似度进行温度 softmax 归一化：

$$ p_i = \frac{\exp\big(\lambda (s_i - \max_j s_j)\big)}{\sum_{j=1}^{K} \exp\big(\lambda (s_j - \max_j s_j)\big)}, \quad i = 1, \ldots, K  \tag{1} $$

其中 $\lambda$ 为温度系数（默认 $\lambda = 20$），$\max_j s_j$ 保证数值稳定性。基于该分布，计算检索不确定性的熵：

$$ H(p) = -\sum_{i=1}^{K} p_i \log p_i \tag{2} $$

$H(p)$ 衡量证据在候选记忆之间的分散程度——熵越低表示查询与某类记忆高度匹配（高熟悉度），熵越高则暗示查询模糊或记忆组织混杂。

### 2.2 策略门控与双路径选择
利用探测检索的均值相似度 $\bar{s} = \frac{1}{K}\sum_{i=1}^K s_i$ 和熵 $H(p)$，策略门控（Strategy Gate）通过双阈值控制器决定后续走“熟悉度路径”还是“回忆路径”：

$$ \mathrm{Strategy}(q) = \begin{cases} \mathrm{Familiarity}, & \bar{s} \geq \theta_{\mathrm{high}} \\ \mathrm{Recollection}, & \bar{s} \leq \theta_{\mathrm{low}} \\ \begin{cases} \mathrm{Familiarity}, & H(p) \leq \tau \\ \mathrm{Recollection}, & H(p) > \tau \end{cases}, & \theta_{\mathrm{low}} < \bar{s} < \theta_{\mathrm{high}} \end{cases} \tag{3} $$

其决策逻辑为：当 $\bar{s}$ 高于高门限 $\theta_{\mathrm{high}}$ 时，熟悉度占优；低于低门限 $\theta_{\mathrm{low}}$ 时，必须启动回忆构建；处于中间模糊带时，则额外依据熵 $\tau$ 判定——若 $H(p)$ 仍低于阈值，说明分布足够尖锐，可沿用熟悉度路径，否则判定为熟悉度不足，转入回忆路径。实验默认采用 $\theta_{\mathrm{high}}=0.6,\ \theta_{\mathrm{low}}=0.3,\ \tau=0.2$，在多个基准上表现出稳定的门控效果（图6，图14）。值得注意的是，学习型门控分类器在 128K 样本上可达到与手工阈值相近的准确率（0.5175 vs 0.5199），验证熟悉度信号已携带充足的路径区分信息（Table 14）。

### 2.3 熟悉度检索路径
当策略门输出 $\mathrm{Familiarity}$ 时，系统直接执行单次 Top-$K$ 检索，相当于人类记忆中的快速识别过程：

$$ \mathcal{C}_t = \mathrm{Top-}K \Big( \big\{ (m_i, \langle \mathbf{x}_t, \mathbf{z}_i \rangle) \big\}_{i=1}^{M} \Big) \tag{4} $$

所选记忆片段 $\mathcal{C}_t$ 即作为最终证据输入后续生成阶段。该路径计算开销极低，仅在门控判定高置信度时启用。

### 2.4 回忆检索路径
当策略门输出 $\mathrm{Recollection}$ 时，系统进入多轮线索重构的回忆检索。其核心是一组“检索–聚类–α‑混合查询更新”的迭代过程（Algorithm 3），模拟人类在模糊记忆下通过不同线索逐步重建上下文的过程。

设第 $r$ 轮已召回候选记忆集 $\mathcal{C}^{(r)}$，系统对其嵌入向量进行 KMeans 聚类，得到 $B$ 个记忆簇（默认 $B=3$），并计算各簇的质心：

$$ \mathbf{g}_b^{(r)} = \frac{1}{|G_b^{(r)}|} \sum_{m_i \in G_b^{(r)}} \mathbf{z}_i, \quad b = 1, \ldots, B \tag{5} $$

随后，对每个分支 $b$，以 α‑混合方式生成下一轮的查询向量，同时引入原始查询 $\mathbf{x}_t$ 以锚定用户意图：

$$ \mathbf{x}_b^{(r+1)} = \mathrm{norm}\Big( \alpha \mathbf{x}^{(r)} + (1-\alpha) \mathbf{g}_b^{(r)} + \mathbf{x}_t \Big), \quad \alpha \in [0,1] \tag{6} $$

其中 $\alpha$ 控制当前查询与记忆质心的混合比例，$\mathrm{norm}(\cdot)$ 将混合向量重新归一化。以这些新探针再进行下一轮检索，从而拓展记忆搜索的广度。

回忆迭代以受限束搜索（beam $B$, depth $F$）形式展开，并应用提前停止策略：当某分支新召回记忆与既往证据的重合度过高时，终止该分支的扩展，以避免冗余计算。最终，回忆证据取所有轮次簇的并集，并用 Top‑$K$ 截断形成输出：

$$ \mathcal{C}_t = \mathrm{Top-}K\Big( \bigcup_{r=0}^{R} \mathcal{C}^{(r)} \Big) $$

回忆路径通过逐步重构证据链，有效提升了面向长尾或上下文密集型查询的检索覆盖度。但在效率上，计算量仅随模糊查询比例触发，整体延迟仍接近熟悉度检索水平（32K→128K→1M 检索耗时分别为 5.09→4.27→6.28 ms，对比全回忆路径 7.09→7.86→8.12 ms；Table 1）。消融实验进一步表明，α‑混合与自适应切换的组合是取得鲁棒性能的关键，且该设计对聚类方法（KMeans 可替换为 DBSCAN、Spectral）和混合策略（可替换为 Gated mixing 等）具有良好鲁棒性（Table 15, Table 16）。

## 实验与分析

### 主结果：生成准确率与检索效率的双重提升
RF-Mem 在三个核心基准上均实现了领先的准确率-效率权衡。在 **PersonaMem** 评估中（Table 1），RF-Mem 在三个记忆规模（32K、128K、1M）上均取得最高整体准确率：32K 下达到 0.6350，显著优于全上下文（0.6129，平均输入 24,657.8 token）和密集检索（0.6337，平均 3,566.6 token），且自身仅消耗约 3,566.6 token，延迟（5.09 ms）远低于全上下文，并接近单次密集检索（4.27 ms）。在 1M 规模下，RF-Mem（0.4589）仍以微弱优势超越密集检索（0.4518），证明双路径检索在超长记忆中保持有效性。同时，在 **PersonaBench** 上（Table 2），RF-Mem 在多种嵌入模型下均取得较优的 Recall@10：MiniLM 上总体 Recall 0.6071，高于熟悉度路径（0.5964）和回忆路径（0.5950）。在 **LongMemEval** 小/中规模版本中（Table 3），RF-Mem 在 BGE 嵌入下 Recall@5 达到 0.8186，对比熟悉度路径的 0.7924 有明显提升。这些结果表明，RF-Mem 通过自适应门控（Eq. 3）在“快速识别”与“深度回忆”之间动态切换，有效克服了单一路径在模糊查询或长尾知识上的瓶颈。


![[assets/figures/papers/iclr26_0016_f7p0F2X6XN_Evoking_User_Memory_Personalizing_LLM_via_Recoll/figures/003_Table_1.jpg]]
*Table 1: Performance comparison over the PersonaMem across different memory corpus sizes. Columns are grouped by question type, rows by retrieval strategy. “NA” indicates the method does not need retrieval. “OOC” means out-of-context of the LLM input window. The best results are in bold, and the second-best results are underlined. “*” indicates the statistically significant improvements (i.e., two-sided t-test with p \< 0.05) over the best baseline*

![[assets/figures/papers/iclr26_0016_f7p0F2X6XN_Evoking_User_Memory_Personalizing_LLM_via_Recoll/figures/004_Table_2.jpg]]
*Table 2: Performance comparison over the PersonaBench dataset across multiple question types. The best results are in bold, and the second-best results are underlined*

![[assets/figures/papers/iclr26_0016_f7p0F2X6XN_Evoking_User_Memory_Personalizing_LLM_via_Recoll/figures/005_Table_3.jpg]]
*Table 3: Performance comparison over the LongMemEval under small (S) and medium (M) memory versions. The best results are in bold, and the second-best results are underlined*

### 自适应效率与路由行为
RF-Mem 的延迟优势源于其将熟悉度作为默认路径，仅当探测检索的不确定性较高时才激活回忆路径。根据 Eq. 3 的阈值策略：当平均相似度 $\bar{s} \geq \theta_{\text{high}}$ 时直接走熟悉度；$\bar{s} \leq \theta_{\text{low}}$ 时进入回忆；中间区域则由熵 $H(p)$ 决定。Table 1 的检索时间显示，RF-Mem 在 128K 和 1M 上的延迟（4.27 ms、6.28 ms）显著低于常开回忆路径（7.86 ms、8.12 ms），且准确率未降。路由统计（Table 17）进一步揭示，嵌入模型质量影响门控行为：强检索器（BGE）下，更多查询被可靠地分配至熟悉度，从而进一步降低平均开销；弱检索器下，更多查询触发回忆以补偿检索不足。该自适应机制使 RF-Mem 的检索成本始终与查询难度匹配，实现“按需深入”。

### 消融分析：机制贡献与鲁棒性
**路径解耦**：Table 11 的分类目标准确率表明，熟悉度路径在事实型问题上表现强劲，而回忆路径在上下文密集的推理类问题上更具优势；RF-Mem 通过自适应融合两者，在 17 个类别中的多数取得最优或次优，证明集合两者优势的因果效应。

**门控策略**：学习型门控分类器（Table 14）在 128K 训练样本上达到与手动阈值相近的准确率（0.5175 vs 0.5199），说明由 $\bar{s}$ 和 $H(p)$ 构成的熟悉度不确定性信号已承载足够的路径区分信息，不必依赖复杂黑盒模型。理论分析（Theorem 1, Proposition 2）进一步证明，所提单调解空间中的双阈值策略最小化检索风险，且门控错误率随探测大小 $K$ 指数下降，验证了机制的可靠性。

**回忆路径实现**：替换聚类方法（DBSCAN、Spectral）或混合策略（Gated mixing、Graph+BFS）时（Table 15、Table 16），RF-Mem 仍持续优于单一熟悉度或回忆路径，验证了 α-混合（Eq. 6）和迭代聚类框架的鲁棒性。全探索变体（不设提前停止）在 Recall 上略有提高但伴随更高延迟（Table 16），说明提前停止策略实现了精度-成本的良好折中。


![[assets/figures/papers/iclr26_0016_f7p0F2X6XN_Evoking_User_Memory_Personalizing_LLM_via_Recoll/figures/071_Table_15.jpg]]
*Table 15: Retrieval performance comparison under different recollection strategies*

**超参数敏感性**：对混合系数 α 和熵阈值 τ 的网格搜索（Figure 14）表明，RF-Mem 的 Recall@5 和 Recall@10 在 α ∈ [0.3, 0.7] 和 τ ∈ [0.1, 0.3] 的宽泛范围内保持稳定，无需精细调参即可在多数场景下工作。


![[assets/figures/papers/iclr26_0016_f7p0F2X6XN_Evoking_User_Memory_Personalizing_LLM_via_Recoll/figures/053_Figure_14.jpg]]
*Figure 14: Hyperparameter sensitivity study on PersonaBench. Heatmaps report Recall@5 and Recall@10 across different retrievers, varying α (query–centroid mixing) and τ (entropy threshold). To examine the robustness of RF-Mem, we conduct a systematic study varying two key hyperparameters, α and τ , across different retrievers (MiniLM, MPNet, BGE) and evaluation metrics (Recall@5/10). Figure 14 visualizes the results as heatmaps, where warmer colors indicate higher retrieval performance. This setup allows us to directly assess how query mixing (α) and entropy thresholding (τ ) interact to balance efficiency and coverage*

### 局限与失败模式
尽管 RF-Mem 在多个基准上表现突出，其当前设计仍存在以下局限，需在未来工作中解决：1 评估局限于单模态对话文本记忆，尚未拓展至多模态或跨领域（如包含图像、表格的企业记忆），泛化性待验证。2 采用列表熵作为不确定性的唯一代理，无法捕捉任务真实难度或用户意图中的深层模糊性，可能导致回忆路径被误触发或漏触发。3 不确定性信号完全依赖相似度分布，未整合语义歧义、校准置信度或用户反馈等更丰富的不确定性量度。4 记忆索引为静态向量，未建模时间演变（如记忆衰退）、冲突检测或遗忘机制，限制了长期交互场景中的时效性。5 增强长期记忆回忆可能无意中放大隐私风险，需要配套的敏感信息过滤与遗忘策略。以上问题为后续研究提供了明确方向。

## 方法谱系与知识库定位

现有个性化大语言模型（LLM）的记忆检索普遍采用固定的单次 Top‑K 相似度检索（即“Familiarity”识别式检索），这等价于依赖浅层熟悉度的快速判断。然而，面对模糊查询、长尾个人事件或需要上下文整合的问题时，单一的相似度信号难以捕捉深层语义关联，极易造成检索不足或噪声过多。全量输入记忆（Full Context）虽可避免检索遗漏，但其高昂的令牌消耗（例如 32K 记忆规模下平均需 24 657 个令牌）和可扩展性瓶颈，使其难以实用。纯回忆路径（“Recollection (ours)”消融基线）通过迭代聚类‑α混合查询扩展（Eq. 6）模拟线索驱动的逐步重构，能在复杂问题上获得召回提升，但在熟悉查询上浪费计算资源，且延迟显著高于一次性检索（Table 1）。

RF‑Mem 的核心贡献在于将认知科学的回忆‑熟悉度双过程理论映射为检索器的双路径设计：引入基于探测检索的熟悉度不确定性估计（Eq. 1‑2），并利用双阈值门控策略（Eq. 3）根据均值相似度和熵自适应切换熟悉度路径（快速 Top‑K）或回忆路径（迭代聚类‑α混合查询扩展）。这一机制填补了现有检索系统缺乏自适应深度调节的空白，使得 RF‑Mem 在保留快速识别优势的同时，能对陌生或困难问题自动触发深层重建。相比基线，RF‑Mem 在 PersonaMem 三个记忆规模（32K/128K/1M）上的整体准确率均为最优（Table 1），并且在 PersonaBench 和 LongMemEval 上的 Recall@5/10 指标上同时超越了单独使用熟悉度或回忆路径（Table 2, 3），其检索延迟介于两者之间，令牌消耗显著低于全量输入。消融分析进一步证实：熟悉度路径擅长事实型查询，回忆路径对上下文密集型任务更强，而 RF‑Mem 的自适应切换能叠加二者优势，在多项子类别中取得最优（见 Appendix D.1，Figure 18‑19）。

RF‑Mem 并非要替代现有的记忆索引结构，而是作为一种通用、不确定性感知的双过程检索层，可以与异构记忆构建方式协同工作。实验表明，它既可叠放在原始对话块索引上，也能在 MemoryBank 摘要索引上取得一致性提升（Table 4），甚至能在 HyDE 查询扩展或 Search‑o1 迭代 RAG 等框架中保持增益（Table 5‑6），显示出良好的模块化适配能力。

**适用边界**：RF‑Mem 对熟悉查询的表现趋近快速熟悉度路径，而在陌生查询上能自动深入回忆，因此适用于那些查询难度分布不均、记忆规模大且要求效率的场景，例如长时间线个人助手。但其门控信号仅依赖归一化相似度分布的均值和熵，对于因语义歧义（同一词不同意图）造成的深层不确定性可能不够敏感。此外，RF‑Mem 的理论保证（门控错误率随探测规模 K 呈指数下降，见 Appendix F.1 Theorem 1）依赖于嵌入质量，当底层嵌入模型对相关性区分力弱时，路径分配可能失准。目前所有评估均局限于对话文本记忆，尚未在跨模态或跨领域记忆中验证，因此在这一边界外的性能需要进一步考察。

**局限与开放问题**：本文自述的局限包括：未建模记忆的时间动态（如近因效应、冲突与遗忘），这会导致静态索引难以处理用户偏好演变；采用列表熵作为不确定性代理，可能忽视任务难度或用户真实意图的细粒度信号；增强长期记忆的可访问性隐含隐私风险，可能在输出中重现敏感信息。对应的开放方向包括：将 RF‑Mem 扩展到多模态跨域场景；引入校准度量、用户反馈或上下文语义等更丰富的不确定性信号；在记忆索引中整合时序加权与冲突消解机制；探索检索‑生成的联合优化（例如使熵阈值与LLM的解码置信度协同调整）；以及设计配套的隐私保护和敏感内容抑制策略，确保安全部署。

## 原文 PDF

![[paperPDFs/ICLR_2026/Evoking_User_Memory_Personalizing_LLM_via_Recollection_Familiarity_Adaptive_Retrieval.pdf]]
