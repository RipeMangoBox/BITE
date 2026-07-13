---
title: "A Dense Subset Index for Collective Query Coverage"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Dense_Subset_Index_for_Collective_Query_Coverage.pdf
project_link: null
code_link: https://github.com/structlearning/DISCo
aliases:
- DDISC
- DSICQC
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_dialog
core_operator: "将检索目标从独立项的最大化 MaxSim 分数，转变为最大化一个单调子模的覆盖目标函数 F(S,Q)，该函数衡量子集 S 对查询原子向量的集体覆盖程度。"
primary_logic: "通过将边际增益表示为提升向量空间中点积的 hinge 函数之和，并利用随机投影将 hinge 函数近似为可索引的点积形式，从而将子模覆盖的贪心选择过程转化为一系列近似最近邻（ANN）检索问题，实现亚线性时间的高覆盖子集检索。"
claims:
- "DISCO 在覆盖率和查询延迟之间取得了最佳权衡，匹配贪心基线的覆盖率，同时速度提升超过 100 倍。"
- "在 HotpotQA 数据集上，DISCO 在 Error(F) 和 MAP 指标上均优于所有基线。"
- "DISCO 能在 2-3 轮内检索到几乎所有相关项，与确定性贪心变体相似。"
- "即使使用少量随机超平面（R=5），近似边际增益的覆盖率也与精确贪心算法匹配。"
---

# A Dense Subset Index for Collective Query Coverage

> [!tip] 核心洞察
> 通过将边际增益表示为提升向量空间中点积的 hinge 函数之和，并利用随机投影将 hinge 函数近似为可索引的点积形式，从而将子模覆盖的贪心选择过程转化为一系列近似最近邻（ANN）检索问题，实现亚线性时间的高覆盖子集检索。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向集体查询覆盖的稠密子集索引 |
| 英文题名 | A Dense Subset Index for Collective Query Coverage |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=cUdODCFjUM) · [GitHub](https://github.com/structlearning/DISCo) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_dialog |
| Method | DISCO (Dense Index for Set Coverage) |
| Dataset | MS-Marco, HotpotQA, 2WikiMultihopQA |

> [!tip] 效果简介
> - MS-Marco 上，平均覆盖率 F̄_K vs 效率（速度提升） 为 DISCO，对比 Exact Greedy，变化 覆盖率匹配，速度提升 >100×。
> - HotpotQA 上，Error(F) (K=2) 为 0.68，对比 Exact Greedy: 0.00，变化 DISCO 的 Error(F) 最低（除贪心变体外）。
> - HotpotQA 上，MAP (K=2) 为 0.84，对比 Exact Greedy: 0.86，变化 DISCO 的 MAP 最高（除贪心变体外）。

## 概要

传统稠密检索（如 ColBERT）的核心瓶颈在于其独立地对每个语料项进行评分，忽略了多跳问答等场景中多个语料项必须协作才能覆盖查询的需求。独立 top-K 检索会引入冗余，无法保证对查询的集体覆盖。针对此问题，本文提出 DISCO（Dense Index for Set Coverage），将检索目标从独立项的最大化 MaxSim 分数，转变为最大化一个单调子模的集体覆盖目标函数 $F(S,Q) = \sum_{\mathbf{q} \in Q} \max_{\mathbf{x} \in \cup_{c \in S} X_c} \mathbf{q}^\top \mathbf{x}$。

DISCO 的核心方法创新在于：通过将边际增益表示为提升向量空间中点积的 hinge 函数之和，并利用随机投影将 hinge 函数近似为可索引的点积形式，从而将子模覆盖的贪心选择过程转化为一系列近似最近邻（ANN）检索问题，实现亚线性时间的高覆盖子集检索。具体地，该方法将查询向量和语料项向量分别提升为 $\widehat{\mathbf{q}}_S := [\mathbf{q}; F(S,\mathbf{q})]$ 和 $\widehat{\mathbf{x}} := [\mathbf{x}; -1]$，并使用 $R$ 个随机超平面构建多副本 IVF 索引，通过迭代式 ANN 检索近似边际增益最大的项。

主要实验结果表明：DISCO 在覆盖率和查询延迟之间取得了最佳权衡，匹配精确贪心基线的覆盖率，同时速度提升超过 100 倍（Figure 2）。在 HotpotQA 数据集上，DISCO 在 Error(F) 和 MAP 指标上均优于所有非贪心基线（Table 3）。消融实验显示，即使仅使用少量随机超平面（$R=5$），近似边际增益的覆盖率也与精确贪心算法匹配（Figure 5）。此外，早期池化（Early Pooling）策略在检索效率和最终覆盖率上均优于晚期池化（Figure 6）。

DISCO 的主要局限性在于：索引内存消耗显著高于 PLAID 等基线（需维护 $R=8$ 个副本索引），当前覆盖目标函数未考虑公平性和多样性，且尚未设计用于处理动态演变的语料库。

传统稠密检索系统（如 ColBERT）的核心瓶颈在于其**独立评分假设**：每个语料项被孤立地评估与查询的相关性（通过 MaxSim 分数），然后返回全局 top-K 结果。这种范式在需要多个文档协同覆盖查询信息的多跳问答（如 HotpotQA）、事实验证（FEVER）等场景中暴露出根本性缺陷。独立 top-K 检索不可避免地引入冗余——多个高分文档可能覆盖相同的查询子空间，而查询中未被覆盖的原子向量（如多跳问题中的中间实体或关系）则被忽略，导致**集体覆盖**能力缺失。

现有方法的缺口在于：检索目标函数 $\operatorname{MaxSim}(Q,X) = \sum_{\mathbf{q} \in Q} \max_{\mathbf{x} \in X} \mathbf{q}^\top \mathbf{x}$ 仅衡量单个文档对查询的匹配程度，无法建模子集 $S$ 对查询原子向量的联合覆盖。虽然理论上可以通过子模函数最大化（贪心算法具有 $(1-1/e)$ 近似保证）来解决此问题，但精确贪心每轮需遍历整个语料库计算边际增益，在大规模场景下计算成本不可接受。现有的贪心变体（Lazy Greedy、Stochastic Greedy）虽有一定加速，但仍需多次扫描语料，延迟远高于可索引的检索方法。

本文的动机是：**能否将子模覆盖的贪心选择过程转化为可索引的近似最近邻（ANN）检索问题，从而在保持贪心算法覆盖率保证的同时，实现亚线性时间的集体覆盖检索？** 核心洞察在于：边际增益 $F(c \mid S,Q) = \sum_{\mathbf{q} \in Q} \max_{\mathbf{x} \in X_c} [\mathbf{q}^\top \mathbf{x} - \max_{u \in S} \max_{\mathbf{x}' \in X_u} \mathbf{q}^\top \mathbf{x}']_+$ 可以表示为提升向量空间中点积的 hinge 函数之和。通过随机投影（random hyperplane projection）将 hinge 函数近似为可索引的点积形式，贪心的每轮选择等价于在 $R$ 个投影空间中查询与当前状态依赖的提升查询向量最相似的语料项。基于此，本文提出 DISCO（Dense Index for Set Coverage）系统，通过构建 $R$ 个 IVF 索引副本，将迭代式贪心选择转化为一系列 ANN 检索，在覆盖率匹配精确贪心的同时实现超过 100 倍的加速。

## 核心方法与创新机理

DISCO 的核心创新在于将检索目标从独立项评分转变为集体覆盖最大化，并通过一系列技术手段将这一理论上复杂的目标转化为可高效索引的近似最近邻（ANN）检索问题，从而在亚线性时间内实现高覆盖子集的检索。

**根本瓶颈与因果开关**：传统稠密检索（如 ColBERT）的瓶颈在于其独立地对每个语料项评分，忽略了多跳问答等场景中多个语料项必须协作才能覆盖查询的需求。独立 top-K 检索会引入冗余，无法保证集体覆盖。DISCO 的因果开关是将检索目标从最大化独立项的 MaxSim 分数之和（$\max_{S:|S|=K} \sum_{c \in S} \operatorname{MaxSim}(Q, X_c)$），转变为最大化一个单调子模的覆盖目标函数 $F(S,Q) = \sum_{\mathbf{q} \in Q} \max_{\mathbf{x} \in \cup_{c \in S} X_c} \mathbf{q}^\top \mathbf{x}$（Eq. (2)）。该函数衡量子集 $S$ 对查询原子向量的集体覆盖程度。

**核心洞察与实现机制**：核心洞察是将贪心选择中计算边际增益的过程，转化为可索引的 ANN 检索。具体分为三步：
1.  **边际增益的 hinge 函数表示**：将项 $c$ 的边际增益 $F(c \mid S,Q)$ 表示为一系列 hinge 函数之和（Eq. (3)），每个 hinge 函数对应一个查询原子向量 $\mathbf{q}$ 与语料项原子向量 $\mathbf{x}$ 的点积，减去当前集合 $S$ 已覆盖的最大值。
2.  **提升向量与随机投影**：通过构造提升向量（augmented vectors）$\widehat{\mathbf{q}}_S := [\mathbf{q}; F(S,\mathbf{q})]$ 和 $\widehat{\mathbf{x}} := [\mathbf{x}; -1]$（Eq. (4)），将 hinge 函数中的减法运算编码为点积形式。随后，利用随机投影特征映射 $\Phi_{\mathbf{w}}(\mathbf{u}) \triangleq [\mathbf{u}; \operatorname{sign}(\mathbf{w}^\top \mathbf{u}) \cdot \mathbf{u}] / \sqrt{2}$（Eq. (6)），将 hinge 函数近似为可索引的点积形式。该映射以至少 0.5 的概率保证 $\Phi_{\mathbf{w}}(\mathbf{u})^\top \Phi_{\mathbf{w}}(\mathbf{v}) = [\mathbf{u}^\top \mathbf{v}]_+$。
3.  **迭代式 ANN 检索**：通过 $R$ 个随机超平面 $\mathbf{w}_{1:R}$ 的副本，将近似后的边际增益 $G_{\mathbf{w}_{1:R}}(c; S, Q) = \sum_{\mathbf{q} \in Q} \max_{r \in [R]} \max_{\mathbf{x} \in X_c} \Phi_{\mathbf{w}_r}(\widehat{\mathbf{q}}_S)^\top \Phi_{\mathbf{w}_r}(\widehat{\mathbf{x}})$（Eq. (8)）转化为 $R$ 个独立索引上的最大点积检索问题。因此，贪心算法的每轮选择（Algorithm 2）可以通过 $R$ 次并行的 ANN 查询高效完成。

**改变的组件（Changed Slots）**：与基线方法相比，DISCO 在多个关键组件上做出了改变：
- **检索目标函数**：从独立项 MaxSim 分数求和（baseline）变为集体覆盖目标 $F(S,Q)$（proposed）。
- **检索算法**：从独立 top-K 检索（baseline）变为迭代式贪心选择，每轮通过 ANN 检索近似边际增益最大的项（proposed）。
- **查询表示**：从静态查询向量集 $Q$（baseline）变为状态依赖的提升查询向量 $\widehat{\mathbf{q}}_S$（proposed），该向量编码了当前覆盖状态。
- **语料项表示**：从静态语料项向量集 $X_c$（baseline）变为提升语料项向量 $\widehat{\mathbf{x}}$（proposed）。
- **相似度计算**：从 MaxSim 分数（baseline）变为随机投影后的近似边际增益 $G_{\mathbf{w}_{1:R}}$（proposed）。
- **索引结构**：从单个 IVF 索引（如 PLAID）（baseline）变为 $R$ 个副本索引（$R=8$），每个副本对应一个随机投影，并使用提升后的语料项向量（proposed）。

**证据强度与性能表现**：实验证据有力地支持了这些创新的有效性。
- **覆盖率-效率权衡**：DISCO 在覆盖率和查询延迟之间取得了最佳权衡，匹配贪心基线的覆盖率，同时速度提升超过 100 倍（Figure 2）。该证据置信度为 0.95。
- **金标签评估**：在 HotpotQA 数据集上，DISCO 在 Error(F) 和 MAP 指标上均优于所有非贪心基线（Table 3）。该证据置信度为 0.95。
- **检索效率**：DISCO 能在 2-3 轮内检索到几乎所有相关项，与确定性贪心变体相似（Figure 4）。该证据置信度为 0.95。
- **近似质量**：即使使用少量随机超平面（$R=5$），近似边际增益的覆盖率也与精确贪心算法匹配（Figure 5）。该证据置信度为 0.95。

**理论保证**：Algorithm 2 享有理论上的最优性保证，其期望覆盖率至少为最优覆盖率的 $(1 - 1/e - \delta)$ 倍（Theorem 4, Eq. (9)）。

DISCO（Dense Index for Set Coverage）是一个面向集体查询覆盖的稠密子集检索系统，其核心动机在于解决传统稠密检索（如 ColBERT）独立评分每个语料项、忽略多跳问答等场景中多个语料项必须协作覆盖查询需求的根本瓶颈。独立 top-K 检索会引入冗余，无法保证对查询的集体覆盖。

**核心因果机制**：DISCO 将检索目标从独立项的最大化 MaxSim 分数转变为最大化一个单调子模的覆盖目标函数 $F(S,Q) = \sum_{\mathbf{q} \in Q} \max_{\mathbf{x} \in \cup_{c \in S} X_c} \mathbf{q}^\top \mathbf{x}$（Eq. (2)），该函数衡量子集 $S$ 对查询原子向量的集体覆盖程度。通过将边际增益表示为提升向量空间中点积的 hinge 函数之和（Eq. (3)），并利用随机投影（Eq. (6)）将 hinge 函数近似为可索引的点积形式，从而将子模覆盖的贪心选择过程转化为一系列近似最近邻（ANN）检索问题，实现亚线性时间的高覆盖子集检索。

**整体 Pipeline**：DISCO 的架构包含两个阶段（参见 Figure 1 系统框图）：

1. **索引构建阶段**（Algorithm 3）：
   - **随机向量采样**：采样 $R$ 个标准正态随机向量 $\mathbf{w}_1, \ldots, \mathbf{w}_R$。
   - **语料项提升与投影**：将每个语料项原子向量 $\mathbf{x}$ 提升为 $\widehat{\mathbf{x}} := [\mathbf{x}; -1] \in \mathbb{R}^{d+1}$（Eq. (4)），然后对每个副本 $r$ 计算投影 $\Phi_{\mathbf{w}_r}(\widehat{\mathbf{x}})$（Eq. (6)）。
   - **多副本 IVF 索引构建**：对每个 $r$，将投影后的向量聚类为 $B$ 个簇，构建 IVF 索引，每个质心关联一个包含文档 ID 的倒排列表。

2. **查询处理阶段**（Algorithm 4）：
   - **迭代式 ANN 检索**：进行 $K$ 轮迭代。在第 $k$ 轮，基于当前已选集合 $S_{k-1}$，计算提升查询向量 $\widehat{\mathbf{q}}_S := [\mathbf{q}; F(S,\mathbf{q})] \in \mathbb{R}^{d+1}$（Eq. (4)），其中 $F(S,\mathbf{q})$ 编码了当前覆盖状态。
   - **跨副本 ANN 搜索**：对每个副本 $r$，使用提升查询向量 $\widehat{\mathbf{q}}_S$ 在对应索引中执行 ANN 检索。
   - **早期池化（Early Pooling）**：在 ANN 检索阶段跨副本池化候选结果（而非在最终评分阶段），合并后选择边际增益最大的项 $c_k$。
   - **输出**：经过 $K$ 轮迭代后输出集合 $S_K$。

**模块关系与输入输出流**：系统由四个关键模块组成：
- **随机向量采样模块**：输出 $R$ 个随机向量，是近似计算的随机性来源。
- **语料项提升与投影模块**：将原始语料项向量转换为提升后的投影表示，输入到索引构建模块。
- **多副本 IVF 索引模块**：维护 $R$ 个独立索引（每个对应一个随机投影），存储投影后的语料项向量及其聚类结构。
- **查询处理模块**：接收查询 $Q$，通过迭代式 ANN 检索逐步构建覆盖子集 $S$，每轮依赖索引模块和当前覆盖状态。

**关键设计决策**：DISCO 将检索目标从独立项的最大化转变为集体覆盖最大化，通过提升向量表示编码覆盖状态，利用随机投影将边际增益近似为可索引的点积形式，并通过多副本索引和早期池化实现高效检索。这种设计使得 DISCO 能够在亚线性时间内检索到高覆盖子集，在覆盖率和查询延迟之间取得最佳权衡（Figure 2），匹配贪心基线的覆盖率同时速度提升超过 100 倍。

本节聚焦 DISCO 方法的核心技术模块，包括问题形式化、边际增益的近似表示、以及基于近似最近邻检索（ANN）的高效贪心选择算法。

### 问题形式化与瓶颈

传统稠密检索（如 ColBERT）使用 MaxSim 分数独立评估每个语料项与查询的相关性：
$$
\operatorname{MaxSim}(Q,X) = \sum_{\mathbf{q} \in Q} \max_{\mathbf{x} \in X} \mathbf{q}^\top \mathbf{x}
$$
该方式忽略了多跳问答等场景中多个语料项必须协作才能覆盖查询的需求，独立 top-K 检索会引入冗余，无法保证集体覆盖。

DISCO 将检索目标重新定义为最大化一个**单调子模覆盖目标函数**：
$$
F(S,Q) = \sum_{\mathbf{q} \in Q} \max_{\mathbf{x} \in \cup_{c \in S} X_c} \mathbf{q}^\top \mathbf{x}
$$
其中 $S$ 是选中的语料项子集，$Q$ 是查询的原子向量集，$X_c$ 是语料项 $c$ 的原子向量集。该函数衡量子集 $S$ 对查询原子向量的集体覆盖程度。由于 $F(S,Q)$ 是单调子模函数，贪心算法能保证 $(1-1/e)$ 的近似比（Theorem 5, Section F.1）。

但精确贪心每轮需评估所有 $\Theta(|C|)$ 个语料项的边际增益，在大规模语料上不可行。核心瓶颈在于：**如何将边际增益计算转化为可索引的 ANN 检索问题**。

### 边际增益的 hinge 函数表示

将项 $c$ 添加到当前集合 $S$ 后的边际增益可表示为 hinge 函数之和（Proposition 1）：
$$
F(c \mid S,Q) = \sum_{\mathbf{q} \in Q} \max_{\mathbf{x} \in X_c} \left[ \mathbf{q}^\top \mathbf{x} - \max_{u \in S} \max_{\mathbf{x}' \in X_u} \mathbf{q}^\top \mathbf{x}' \right]_+
$$
其中 $[z]_+ = \max(0, z)$。该形式的关键洞察是：边际增益仅依赖于每个查询原子 $\mathbf{q}$ 在 $S$ 中已获得的最大分数 $F(S,\mathbf{q}) = \max_{u \in S} \max_{\mathbf{x}' \in X_u} \mathbf{q}^\top \mathbf{x}'$。

### 提升向量表示与随机投影

为将 hinge 函数转化为点积形式，引入**提升向量**：
$$
\widehat{\mathbf{q}}_S := [\mathbf{q}; F(S,\mathbf{q})] \in \mathbb{R}^{d+1}, \quad \widehat{\mathbf{x}} := [\mathbf{x}; -1] \in \mathbb{R}^{d+1}
$$
查询原子向量附加当前覆盖值，语料项原子向量附加 -1。此时，$[\mathbf{q}^\top \mathbf{x} - F(S,\mathbf{q})]_+ = [\widehat{\mathbf{q}}_S^\top \widehat{\mathbf{x}}]_+$（需手动验证，原论文未显式给出此等式，但该等式是后续推导的基础）。

然而，点积的 hinge 函数仍无法直接索引。DISCO 使用**随机投影特征映射**将其近似为点积形式：
$$
\Phi_{\mathbf{w}}(\mathbf{u}) \triangleq [\mathbf{u}; \operatorname{sign}(\mathbf{w}^\top \mathbf{u}) \cdot \mathbf{u}] / \sqrt{2}
$$
其中 $\mathbf{w} \sim \mathcal{N}(0, I_{d+1})$。该映射满足（Theorem 2）：
$$
\Phi_{\mathbf{w}}(\mathbf{u})^\top \Phi_{\mathbf{w}}(\mathbf{v}) = [\mathbf{u}^\top \mathbf{v}]_+ \quad \text{with probability } p \geq 0.5
$$
即单个随机超平面能以至少 50% 的概率精确恢复 hinge 函数。

### 近似边际增益与 ANN 检索

为提升近似质量，使用 $R$ 个独立随机超平面，对每个查询原子取最大近似值：
$$
G_{\mathbf{w}_{1:R}}(c; S, Q) = \sum_{\mathbf{q} \in Q} \max_{r \in [R]} \max_{\mathbf{x} \in X_c} \Phi_{\mathbf{w}_r}(\widehat{\mathbf{q}}_S)^\top \Phi_{\mathbf{w}_r}(\widehat{\mathbf{x}})
$$
该近似将每轮贪心选择转化为：对每个副本 $r$，在 $\{\Phi_{\mathbf{w}_r}(\widehat{\mathbf{x}})\}$ 构成的向量空间中进行 ANN 检索，找到与 $\Phi_{\mathbf{w}_r}(\widehat{\mathbf{q}}_S)$ 最相似的语料项原子，然后跨副本取最大值后按查询原子求和。

算法 2（Section 3.3）使用该近似替换精确边际增益，并具有理论保证（Theorem 4）：
$$
\mathbb{E}_{\mathbf{w}_{1:R}}[F(S_K,Q)] \geq (1 - 1/e - \delta) \cdot F(S^*,Q)
$$
其中 $S_K$ 是算法 2 选出的 $K$ 个项，$S^*$ 是最优解，$\delta$ 由超平面数量 $R$ 和采样策略控制。

### 索引结构与查询执行

**索引阶段**（Algorithm 3）：对每个副本 $r$，将提升后的语料项向量 $\widehat{\mathbf{x}}$ 映射为 $\Phi_{\mathbf{w}_r}(\widehat{\mathbf{x}})$，然后构建 IVF 索引（聚类 + 倒排列表）。

**查询阶段**（Algorithm 4）：迭代 $K$ 轮。每轮 $k$：
1. 根据当前集合 $S_{k-1}$ 计算每个查询原子的 $F(S_{k-1}, \mathbf{q})$，构建 $\widehat{\mathbf{q}}_S$。
2. 对每个副本 $r$，使用 $\Phi_{\mathbf{w}_r}(\widehat{\mathbf{q}}_S)$ 进行 ANN 检索，得到候选语料项。
3. **早期池化**：跨副本合并候选结果，而非在最终评分阶段才合并（Figure 6 消融实验证实早期池化更优）。
4. 对候选集计算精细化的近似边际增益（使用存储的质心向量），选择增益最大的项 $c_k$。

该流程将贪心算法的复杂度从 $\Theta(K|C|)$ 降低到 $\Theta(K \cdot (R \cdot n' + |\text{candidates}|))$，其中 $n'$ 是每 token 探测的质心数，$|\text{candidates}|$ 是 ANN 返回的候选集大小，通常远小于 $|C|$。

## 实验与关键发现

### 主要结果：覆盖率与效率的权衡

DISCO 的核心贡献在于将子模覆盖的贪心选择过程转化为可索引的近似最近邻（ANN）检索问题，从而在保持高覆盖率的同时实现了显著的加速。图 2 展示了在四个数据集（MS-Marco, HotpotQA, Fever, Pooled）上，DISCO 与所有基线的覆盖率-效率权衡。DISCO 始终占据帕累托前沿的最优区域，在覆盖率上匹配精确贪心（Exact Greedy）变体，同时查询速度提升超过 100 倍（尤其在 MS-Marco 上）。相比之下，所有基于独立项检索的基线（如 ColBERTv2, PLAID, MUVERA, WARP, SPLADE）均因无法建模项间协作而显著落后于贪心基线的覆盖率上界，且其效率优势不足以弥补这一差距。

### 基于金标签的定量评估

为了严格衡量 DISCO 检索到真正相关子集的能力，实验在 HotpotQA 上使用了人工标注的金标签集合（|S_gold|=2）。表 3 报告了 Error(F)（检索集合与金标签集合的覆盖率偏差）和 MAP（平均精度均值）。结果中，DISCO 的 Error(F)=0.68 和 MAP=0.84 均显著优于除贪心变体外的所有基线。这一结果的关键在于：贪心变体（Exact/Lazy/Stochastic）本身是求解覆盖目标的最优近似算法，而 DISCO 通过随机投影近似边际增益，在保持近似保证的前提下实现了亚线性时间检索。图 4 进一步揭示了这一机制：在 HotpotQA 上，DISCO 在 2-3 轮迭代内即可检索到所有金标签相关项，其排名分布与确定性贪心变体高度相似，说明其近似边际增益的质量足以在极少的轮次内收敛到高覆盖解。

![[assets/figures/papers/iclr26_0002_cUdODCFjUM_A_Dense_Subset_Index_for_Collective_Query_Covera/figures/006_Table_3.jpg]]
*Table 3: Comparison of DISCO with baselines on gold labels of HotpotQA ( | $S _ { \mathrm { g o l d } }$ | = 2 ) , in terms of Error $\begin{array} { r } { ( F ) = \sum _ { Q \in \hat { \boldsymbol { \mathcal { Q } } } } \vert F ( S _ { \mathrm { g o l d } } , Q ) - F ( S _ { K } , Q ) \vert / \vert \boldsymbol { \mathcal { Q } } \vert } \end{array}$ with K = 2 and Mean Average Precision (MAP). Green (Blue) shows the (second) best performer

### 消融研究：近似边际增益的质量

DISCO 的核心近似在于使用 R 个随机超平面将 hinge 函数形式的边际增益转化为可索引的点积。图 5 在 NFCorpus 和 Writing 数据集上验证了这一近似的有效性。结果显示，即使仅使用 R=5 个随机超平面，DISCO 的覆盖率曲线已与精确贪心算法几乎重合。随着 R 增大（至 8），近似误差进一步收敛（见附录表 29-31 的边际增益误差分析）。这一结论的因果机制是：每个随机超平面提供的 hinge 函数近似以概率 p≥0.5 保持符号一致性（Theorem 2），而通过 R 个独立副本取最大值（max_{r∈[R]}）显著提高了近似精度，使得少量副本即可达到近最优的贪心选择效果。

### 架构消融：早期池化 vs 晚期池化

图 6 的消融研究对比了两种跨副本池化策略。早期池化（Early Pooling）在 ANN 检索阶段即跨 R 个副本的候选结果进行合并，而晚期池化（Late Pooling）则先独立检索再在最终评分阶段合并。实验结果表明，早期池化在所有数据集上均取得了更优的覆盖率-效率权衡。其瓶颈在于：晚期池化在每个副本上独立执行 top-K 检索，导致候选集冗余且无法在检索阶段利用跨副本信息；而早期池化通过合并候选列表，使后续的精细评分（fine-grained filtering）能够基于更全面的候选集进行，从而在相同效率下获得更高覆盖率。

### 参数敏感性：每 token 探测质心数 n'

图 17 展示了 IVF 索引中每 token 探测的质心数 n' 对 DISCO 性能的影响。增加 n' 会提高覆盖率（因为检索到了更多候选），但线性增加了查询延迟。默认设置（n'=1）在效率和覆盖率之间取得了最佳平衡，验证了论文实验配置的合理性。

### 下游任务与内存开销

在多跳 QA 任务（2WikiMultihopQA, Musique）上，DISCO 检索的集合经 LLM 处理后，其 Exact Match 和 F1 分数（表 27-28）表明其在复杂推理场景中仍有改进空间——尤其是在 Musique 上，下游性能较低，提示当前覆盖目标可能不足以捕获支撑复杂逻辑链所需的全部信息。此外，表 12 显示 DISCO 的索引内存消耗显著高于 PLAID、MUVERA 和 WARP，原因在于需要维护 R=8 个副本索引（每个副本对应一个随机投影）。这是实现亚线性时间检索所付出的存储代价，在内存受限场景下可能成为瓶颈。

![[assets/figures/papers/iclr26_0002_cUdODCFjUM_A_Dense_Subset_Index_for_Collective_Query_Covera/figures/016_Table_12.jpg]]
*Table 12: In Table 12, we provide statistics on index construction and memory consumption for each of the indexing based methods. We note that the memory consumption reported for DISCO is higher than for other methods due to the construction of R = 8 different replica indices, each housing corpus vectors that have been augmented to approximate the maximum marginal gain. Table 12: Index memory consumption across methods and datasets, in gigabytes (GB)*

### 补充图表

![[assets/figures/papers/iclr26_0002_cUdODCFjUM_A_Dense_Subset_Index_for_Collective_Query_Covera/figures/011_Table_2.jpg]]
*Table 2: In the table below, the aggregate contractual principal amount of loans on nonaccrual status and/or more than 90 days past due (which excludes loans carried at zero fair value and considered uncollectible) exceeds the related fair value primarily because the firm regularly purchases loans, such as distressed loans, at values significantly below the contractual principal amounts*

![[assets/figures/papers/iclr26_0002_cUdODCFjUM_A_Dense_Subset_Index_for_Collective_Query_Covera/figures/014_Table_4.jpg]]
*Table 4: BEIR. BEIR comprises heterogeneous retrieval tasks spanning multiple domains. We use the following large-corpus subsets*

![[assets/figures/papers/iclr26_0002_cUdODCFjUM_A_Dense_Subset_Index_for_Collective_Query_Covera/figures/015_Table_11.jpg]]
*Table 11: LoTTE. LoTTE targets out-of-domain generalization with six topic-stratified corpora constructed from Stack Exchange communities. Each corpus provides two query sets (search and forum); we use the forum queries derived from question titles. Table 11: LoTTE dataset. The fraction column is the proportion of queries with | $S _ { \mathrm { g o l d } }$ ( Q ) | > 1*

## 定位与知识库关联

DISCO 的提出直接针对传统稠密检索（如 ColBERTv2、PLAID）在**多跳问答与证据协作场景下的结构性缺陷**。传统方法（如 MaxSim 分数）独立地对每个语料项评分，忽略了多个语料项必须协作才能覆盖查询的需求，导致独立 top-K 检索引入冗余，无法保证集体覆盖。DISCO 将检索目标从独立项的最大化 MaxSim 分数（`max_{S:|S|=K} Σ_{c∈S} MaxSim(Q, X_c)`）转变为最大化一个单调子模的覆盖目标函数 `F(S,Q) = Σ_{q∈Q} max_{x∈∪_{c∈S} X_c} q^T x`（Eq. 2），该函数衡量子集 S 对查询原子向量的集体覆盖程度。

**因果机制的核心**在于：通过将边际增益表示为提升向量空间中点积的 hinge 函数之和（`F(c|S,Q) = Σ_{q∈Q} max_{x∈X_c} [q^T x - max_{u∈S} max_{x'∈X_u} q^T x']_+`，Eq. 3），并利用随机投影（`Φ_w(u) = [u; sign(w^T u)·u]/√2`，Eq. 6）将 hinge 函数近似为可索引的点积形式，从而将子模覆盖的贪心选择过程转化为一系列近似最近邻（ANN）检索问题。具体地，查询表示被提升为状态依赖的 `q̂_S = [q; F(S,q)] ∈ ℝ^{d+1}`（编码当前覆盖状态），语料项表示被提升为 `x̂ = [x; -1] ∈ ℝ^{d+1}`，使得近似边际增益 `G_{w_{1:R}}(c; S, Q) = Σ_{q∈Q} max_{r∈[R]} max_{x∈X_c} Φ_{w_r}(q̂_S)^T Φ_{w_r}(x̂)`（Eq. 8）可以通过 R=8 个副本的 IVF 索引高效计算。

**与基线的对比**：在覆盖率-效率权衡（Figure 2）上，DISCO 在四个数据集（MS-Marco、HotpotQA、Fever、Pooled）上均取得了最佳权衡，匹配精确贪心基线的覆盖率，同时速度提升超过 100 倍。在 HotpotQA 的金标签评估（Table 3）中，DISCO 在 Error(F)（0.68）和 MAP（0.84）上均优于所有非贪心基线。消融实验（Figure 5）表明，即使仅使用 R=5 个随机超平面，近似边际增益的覆盖率也能与精确贪心算法匹配。早期池化（Early Pooling）在检索效率和最终覆盖率上均优于晚期池化（Figure 6）。

**适用边界与局限**：DISCO 的索引内存消耗显著高于 PLAID、MUVERA 和 WARP（Table 12），因为需要维护 8 个副本索引。当前覆盖目标函数**未考虑公平性概念**（如群体公平性或个体公平性），且仅关注覆盖率最大化，未显式建模多样性。DISCO 目前未设计用于处理动态演变的语料库。在 Musique 等复杂多跳 QA 数据集上，下游 LLM 的 Exact Match 和 F1 分数较低（Table 27, 28），表明检索到的集合可能仍不足以支持复杂推理。

**开放问题**包括：(1) 如何将公平性约束纳入覆盖目标函数？(2) 如何在模型中显式引入多样性？(3) 如何将 DISCO 适配到动态演变的语料库？(4) 如何提高 LLM 在复杂多跳 QA 数据集上利用检索集合的性能？(5) 如何为 MSMarco 和 Fever 等非 QA 数据集生成高质量的伪标签以进行金标签评估？

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Dense_Subset_Index_for_Collective_Query_Coverage.pdf

![[paperPDFs/ICLR_2026/A_Dense_Subset_Index_for_Collective_Query_Coverage.pdf]]
