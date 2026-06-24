---
title: "How Reliable is Language Model Micro-Benchmarking?"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/How_Reliable_is_Language_Model_Micro_Benchmarking.pdf
openreview_forum_id: cReExMQLiK
aliases:
- MDADMMEM
- HRILMMB
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "用MDAD度量微基准能可靠区分的最小模型性能差异。"
primary_logic: "MDAD 通过衡量微基准测试能够一致正确排序的最小模型性能差异，精确刻画了效率与可靠性之间的权衡，并揭示出在需要区分相近性能模型时，随机抽样在中等样本量下与精心设计的微基准测试方法同样有效。"
claims:
- "当仅选择10个示例时，任何微基准测试方法都无法以超过65%的概率区分全基准上准确率相差2个百分点的模型。"
- "在MMLU-Pro上选择25个示例时，8B参数指令微调模型之间超过一半的成对比较（51%）无法被可靠保留。"
- "当选择250个示例时，所有方法的MDAD均降至2或以下，随机抽样与Anchor Points等特定方法具有竞争力。"
- "Anchor Points在极小样本量下具有最低的MDAD，但在选择1000个示例时表现最差，可能由于k-medoids聚类中集群大小不平衡。"
---

# How Reliable is Language Model Micro-Benchmarking?

> [!tip] 核心洞察
> MDAD 通过衡量微基准测试能够一致正确排序的最小模型性能差异，精确刻画了效率与可靠性之间的权衡，并揭示出在需要区分相近性能模型时，随机抽样在中等样本量下与精心设计的微基准测试方法同样有效。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 语言模型微基准测试的可靠性研究 |
| 英文题名 | How Reliable is Language Model Micro-Benchmarking? |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=cReExMQLiK); [GitHub](https://github.com/dill-lab/micro-benchmarking-reliability) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | Minimum Detectable Ability Difference (MDAD) meta-evaluation measure |
| Dataset | MMLU, MMLU-Pro, MMLU-Pro (8B instruct models) |

> [!tip] 效果简介
> - MMLU 上，MDAD (accuracy difference points) 为 tinyBenchmarks (10 examples) = 12.5，对比 Uniform random sampling (10 examples) = 20，变化 -7.5。
> - MMLU-Pro 上，MDAD 为 Anchor Points (500 examples) ≈ 2，对比 Uniform random sampling (500 examples) ≈ 2，变化 ≈ 0 (competitive)。
> - MMLU-Pro (8B instruct models) 上，pairwise comparison preservation 为 MDAD-based analysis，对比 Aggregate rank correlation，变化 identifies 51% comparisons not preserved vs. not revealed。

## 概述

语言模型评估正面临一个日益突出的矛盾：全量基准测试的计算成本持续攀升，而微基准测试（micro-benchmarking）——通过选取少量示例来近似完整基准——被寄予厚望。然而，一个根本性问题长期被忽视：**当样本量被极端压缩时，微基准测试究竟能在多大程度上可靠地区分模型性能差异？**

本文揭示了现有微基准测试元评估方法的盲区。传统的元评估指标，如平均估计误差（Mean Estimation Error）或 Kendall's τ 排名相关性，仅提供聚合层面的总结，掩盖了微基准测试在细粒度模型比较中的失效模式。例如，在 MMLU-Pro 上仅选取 25 个示例时，即便聚合排名相关性看似可接受，**8B 参数指令微调模型之间超过一半（51%）的成对比较**已无法被可靠保留。

为此，本文提出了 **MDAD（Minimum Detectable Ability Difference，最小可检测能力差异）**——一种细粒度的元评估度量。MDAD 衡量的是：在全量基准上，两个模型的性能差异需要达到多大，微基准测试才能以一致的高概率（默认 ≥80%）正确排序它们。这一度量直接刻画了微基准测试的效率-可靠性权衡：样本越少，能可靠区分的最小性能差异就越大。

核心发现可概括为三点：

1. **极端压缩下的不可靠性**：当仅选择 10 个示例时，任何微基准测试方法都无法以超过 65% 的概率区分在全基准上准确率仅相差 2 个百分点的模型。
2. **随机抽样的竞争力**：当样本量增至中等规模（如 250 个示例），所有方法的 MDAD 均降至约 2 或更低，此时精心设计的微基准测试方法（如 Anchor Points）与均匀随机抽样在可靠性上趋于相当。
3. **方法间的非单调行为**：Anchor Points 在极小样本量下具有最低的 MDAD，但当样本量增至 1000 时反而表现最差——这一反直觉现象可能源于 k-medoids 聚类中集群大小的严重不平衡。

这些发现表明，微基准测试的可靠性评估需要从“聚合排名是否相关”转向“哪些模型比较能被可靠保留”的细粒度视角，而 MDAD 正是为此设计的诊断工具。

## 背景与动机

语言模型评估正面临一个日益突出的效率困境：全量基准测试（如MMLU、MMLU-Pro、BBH等）动辄包含数千道题目，对单个模型进行一次完整评估就需要耗费大量计算资源与时间。为缓解这一压力，研究者提出了多种**微基准测试（micro-benchmarking）**方法——通过从全量基准中精心挑选一个小规模示例子集，以远低于全量评估的成本近似模型的全基准性能。

然而，一个关键问题长期被忽视：**当样本量被极端压缩时，这些微基准测试究竟能多可靠地区分模型之间的性能差异？** 传统的元评估指标，如平均估计误差（mean estimation error）和Kendall's tau排名相关性，虽然能给出宏观的可靠性判断，却无法揭示微基准测试在细粒度上的失效模式。具体而言，一个微基准测试可能在整体排名上表现出高相关性，却在区分性能相近的模型时频繁出错——而这类相近性能的模型比较，恰恰是实际模型评估中最常见也最重要的场景。

图1（左下）直观地展示了这一困境：当仅选择10个示例时，没有任何微基准测试方法能够以超过65%的概率正确排序在全基准上准确率仅相差2个百分点的两个模型。这意味着，在极小样本量下，微基准测试对相近性能模型的排序几乎等同于随机猜测。这一发现揭示了一个此前未被充分量化的瓶颈：**微基准测试的可靠性并非一个单一数值，而是高度依赖于被比较模型之间的性能差异大小。**

更深层的问题在于，传统的元评估范式本身存在结构性盲区。平均估计误差衡量的是单个模型在微基准与全基准上的性能偏差，但它无法捕捉微基准测试是否**一致性地**高估或低估某类模型——这种系统性偏差虽然不影响平均误差，却会严重扭曲模型间的相对排名。Kendall's tau排名相关性虽然关注排名一致性，但它将所有模型对的排名错误等权处理：无论两个模型在全基准上相差20个百分点还是仅差0.5个百分点，一次排名反转对tau的贡献完全相同。这种聚合视角掩盖了一个关键事实：在模型性能分布密集的区域，微基准测试的排名可靠性可能远低于整体tau所暗示的水平。

正是基于这一认识，本文提出了一个全新的元评估视角：不再问“微基准测试的整体排名有多准”，而是问“**微基准测试能可靠区分多大的性能差异**”。这一视角的转变直接催生了MDAD（Minimum Detectable Ability Difference）指标，它精确刻画了给定样本量下微基准测试能够一致正确排序的最小模型性能差异，从而为效率与可靠性之间的权衡提供了可操作的量化依据。

## 核心创新

本文的核心创新在于提出了一种全新的**元评估范式**，将微基准测试的可靠性评估从聚合统计量转向**细粒度的成对排序保真度**分析。这一范式转变通过一个名为 **MDAD（Minimum Detectable Ability Difference）** 的指标实现，其设计逻辑与现有元评估方法存在根本性差异。

### 从聚合指标到条件排序一致性

传统的元评估方法主要依赖两类指标：**平均估计误差**（Mean Estimation Error）衡量微基准测试对单个模型性能的绝对估计偏差，而 **Kendall's tau 秩相关系数**则衡量模型排名在聚合层面的整体一致性。这两种指标的共同缺陷在于，它们无法揭示微基准测试在**哪些性能区间**上能够可靠地区分模型。

MDAD 的核心洞察在于：微基准测试的可靠性不应被笼统地概括为一个标量，而应被表达为**全基准性能差异的条件函数**。具体而言，MDAD 首先定义了一致性概率：

$$\mathrm{agreement}(D_{\mathrm{micro}}, D_{\mathrm{full}}, B) = \operatorname{Pr}_{M_1, M_2 \in \mathcal{T}} \Big( \Delta_{D_{\mathrm{micro}}}(M_1, M_2) > 0 \Big| \Delta_{D_{\mathrm{full}}}(M_1, M_2) \in B \Big)$$

该公式计算的是：对于在全基准上性能差异落入桶 $B$ 的模型对，微基准测试能够正确排序它们的概率。随后，MDAD 通过寻找满足 80% 一致性阈值的最小性能差异桶，将整条一致性曲线压缩为一个可操作的标量：

$$\mathbf{MDAD}(D_{\mathrm{micro}}, D_{\mathrm{full}}) = \underset{S \in B}{\operatorname{argmin}} \left\{ \mathrm{agreement}(D_{\mathrm{micro}}, D_{\mathrm{full}}, B) \right\} \mathrm{s.t.~Pr} \geq 0.8$$

这一指标直接回答了实践者最关心的问题：**“使用这个微基准测试，我能在多大程度上确信两个模型的性能差异是真实的？”** 较低的 MDAD 意味着微基准测试能够可靠地区分性能更接近的模型。

### 与现有元评估指标的本质差异

Table 1 概括了 MDAD 与现有指标的概念性对比。平均估计误差关注的是**点估计的绝对准确性**，但它无法捕捉系统性偏差——即使微基准测试对所有模型都高估了 5 个百分点，只要高估幅度一致，平均估计误差可能很低，但成对排名可能完全正确。Kendall's tau 则走向另一个极端：它衡量**排名的整体正确性**，但对性能差异较小的模型对之间的排序错误不敏感。

MDAD 填补了这一空白。它通过**条件概率**的形式，将元评估的粒度细化到性能差异的每个区间。实验证据充分展示了这种细粒度的价值：

- **相同秩相关，不同可靠性**：在 MMLU-Pro 上选择 10 个示例时，tinyBenchmarks 与均匀随机抽样的 Kendall's tau 几乎相同，但前者的 MDAD 为 12.5，后者高达 20（Figure 4 中点 C 和 D）。这意味着尽管两种方法在聚合排名上表现相似，随机抽样在区分相近性能模型时远不可靠。
- **相同 MDAD，不同秩相关**：在 BBH 和 GPQA 上，Anchor Points 在 10 个示例时的 Kendall's tau 分别为 0.73 和 0.43，但 MDAD 均为 6（Figure 4 中点 G 和 H）。这表明 MDAD 捕捉到了与任务难度无关的、关于排序可靠性的稳定信号。

### 揭示微基准测试的可靠性边界

MDAD 的另一项关键创新在于，它精确刻画了**样本数量与可靠性之间的权衡曲线**，并揭示了现有精心设计的选择策略在中等样本量下的收益递减现象。

当仅选择 10 个示例时，所有微基准测试方法的 MDAD 均高于 12.5（MMLU 上），这意味着它们无法可靠地区分全基准上准确率差异小于 2 个百分点的模型——一致性概率不超过 65%（Figure 1）。当样本量增至 250 时，所有方法的 MDAD 均降至 2 或以下，此时**均匀随机抽样与 Anchor Points 等特定方法具有竞争力**（Figure 4）。这一发现挑战了“精心设计的示例选择策略总是优于随机抽样”的直觉假设。

更值得关注的是 Anchor Points 在极端样本量下的表现反转：它在极小样本量（如 10 个示例）下具有最低的 MDAD，但在选择 1000 个示例时反而表现最差。论文分析指出，这可能是由于 k-medoids 聚类中集群大小的极端不平衡所致——当强制选择大量示例时，某些集群被迫贡献过多代表性不足的样本，反而引入了噪声。

### 从方法论到诊断工具

MDAD 的范式转变还体现在其**解释性价值**上。传统指标只能告诉研究者“这个微基准测试好不好”，而 MDAD 能够诊断“对于特定模型集合，哪些成对比较可能不可靠”。例如，在 MMLU-Pro 上比较 8B 参数指令微调模型时，MDAD 分析揭示：当选择 25 个示例时，超过一半（51%）的成对比较无法被可靠保留（Figure 5）。这是因为这些模型的性能分布极为集中——近半数模型对的准确率差异小于 5 个百分点，而该样本量下所有方法的 MDAD 均大于等于 5。

这种诊断能力直接解释了微基准测试中常见的“排名稳定”现象：当模型性能差异远大于 MDAD 时，排名自然稳定；而当模型性能差异接近或小于 MDAD 时，排名的波动并非方法缺陷，而是**信息论意义上的不可区分性**。

## 整体框架

本文的核心贡献并非提出一种新的微基准测试构建方法，而是引入了一套**元评估框架**，用于精确刻画微基准测试在极端样本缩减下的可靠性边界。该框架围绕一个核心指标——**最小可检测能力差异（Minimum Detectable Ability Difference, MDAD）**——展开，其设计逻辑如下：

### 1. 问题设定与输入输出流

框架的输入包括三个要素：
- **全量基准** $D_{\mathrm{full}}$：待缩减的完整评估数据集。
- **微基准测试** $D_{\mathrm{micro}}$：从全量基准中按某种策略选择的子集，大小为 $n$。
- **目标模型集** $\mathcal{T}$：用于评估微基准测试可靠性的模型集合，这些模型在全量基准和微基准测试上均有预测结果。

框架的输出是一组**一致性曲线（agreement curves）** 和一个标量汇总值 **MDAD**，二者共同回答一个核心问题：在给定的微基准测试规模下，哪些模型间的性能差异能够被可靠地区分？

### 2. 核心模块：一致性概率与 MDAD

框架的核心计算流程分为两步：

**步骤一：计算一致性概率**。对于目标模型集 $\mathcal{T}$ 中的每一对模型 $(M_1, M_2)$，首先计算它们在全量基准 $D_{\mathrm{full}}$ 上的性能差异 $\Delta_{D_{\mathrm{full}}}(M_1, M_2)$，并将其分配到预定义的差异桶 $B$ 中。然后统计在每个桶内，微基准测试 $D_{\mathrm{micro}}$ 上的排名方向与全量基准一致的比例，即一致性概率：

$$\mathrm{agreement}(D_{\mathrm{micro}}, D_{\mathrm{full}}, B) = \operatorname{Pr}_{M_1, M_2 \in \mathcal{T}} \Big( \Delta_{D_{\mathrm{micro}}}(M_1, M_2) > 0 \Big| \Delta_{D_{\mathrm{full}}}(M_1, M_2) \in B \Big)$$

这一概率直接反映了微基准测试在特定性能差异区间内的排名保真度。

**步骤二：汇总为 MDAD**。在所有差异桶中，寻找满足一致性概率不低于预设阈值（本文取 0.8）的最小差异桶，其对应的性能差异值即为 MDAD：

$$\mathbf{MDAD}(D_{\mathrm{micro}}, D_{\mathrm{full}}) = \underset{S \in B}{\operatorname{argmin}} \left\{ \mathrm{agreement}(D_{\mathrm{micro}}, D_{\mathrm{full}}, B) \right\} \quad \mathrm{s.t.} \ \Pr \geq 0.8$$

MDAD 的直观含义是：在全量基准上，微基准测试能够以至少 80% 的概率一致正确排序的**最小模型性能差异**。MDAD 越小，说明微基准测试越可靠。

### 3. 与传统元评估指标的对比定位

表 1 概括了 MDAD 与两种传统元评估指标——**平均估计误差（Mean Estimation Error）** 和 **Kendall's tau 排名相关性**——的本质差异。传统指标在聚合层面汇总微基准测试的表现，无法揭示其在区分性能相近模型时的失效模式。例如，在极端缩减（如仅选择 10 个示例）时，微基准测试可能仍获得较高的 Kendall's tau，但其一致性曲线（Figure 1 左下）显示，对于全量基准上准确率相差不足 4 个百分点的模型对，任何方法都无法以超过 65% 的概率正确排序。MDAD 正是通过将评估粒度从“聚合排名”下沉到“逐对差异”，填补了这一元评估盲区。

### 4. 框架的边界与假设

- **性能度量限定**：当前框架仅适用于分类准确率，MDAD 的计算基于准确率差异桶（分辨率为 0.5 个百分点）。扩展到开放式生成或其他指标仍需进一步研究。
- **模型集依赖**：MDAD 的估计依赖于一组固定的源模型和目标模型划分。当目标模型集发生变化（如出现全新架构的模型）时，MDAD 可能需要重新校准。
- **阈值选择**：一致性阈值 0.8 是预设参数，但消融实验表明，使用 0.7、0.9 或 0.95 等不同阈值时，MDAD 的结果在定性上保持一致（Figure 7）。

## 核心模块与公式推导

### 一致性概率（Agreement Probability）

MDAD 的构建始于一个细粒度的成对排序一致性度量。给定一个微基准测试 $D_{\mathrm{micro}}$、全基准测试 $D_{\mathrm{full}}$ 和一个目标模型集 $\mathcal{T}$，首先定义在特定性能差异区间 $B$ 内，微基准测试与全基准测试的排名一致概率：

$$
\mathrm{agreement}(D_{\mathrm{micro}}, D_{\mathrm{full}}, B) = \operatorname{Pr}_{M_1, M_2 \in \mathcal{T}} \Big( \Delta_{D_{\mathrm{micro}}}(M_1, M_2) > 0 \Big| \Delta_{D_{\mathrm{full}}}(M_1, M_2) \in B \Big)
$$

其中 $\Delta_{D}(M_1, M_2)$ 表示模型 $M_1$ 与 $M_2$ 在数据集 $D$ 上的性能差异。该公式的核心逻辑是：在全基准上性能差异落入特定桶 $B$ 的所有模型对中，计算微基准测试能够正确保留二者相对排序（即微基准上 $M_1$ 优于 $M_2$ 当且仅当全基准上也是如此）的概率。这一度量直接揭示了微基准测试在**不同性能差异水平上的可靠性分布**，而非像传统指标那样仅给出一个聚合标量。

### 最小可检测能力差异（MDAD）

在一致性概率的基础上，MDAD 通过一个条件最优化定义，将整条一致性曲线概括为一个单一数值：

$$
\mathbf{MDAD}(D_{\mathrm{micro}}, D_{\mathrm{full}}) = \underset{S \in B}{\operatorname{argmin}} \left\{ \mathrm{agreement}(D_{\mathrm{micro}}, D_{\mathrm{full}}, B) \right\} \quad \mathrm{s.t.} \quad \mathrm{Pr} \geq 0.8
$$

其含义为：在所有性能差异桶 $B$ 中，找到满足“一致性概率至少为 0.8”这一约束的最小差异区间，该区间的下界即为 MDAD。直观上，MDAD 回答了以下问题：**在全基准上，两个模型至少需要相差多少准确率点，微基准测试才能以 80% 以上的概率一致地正确排序它们？** MDAD 越小，表明微基准测试越可靠——即使在模型性能差异微小时也能保持正确的相对排序。

### 与传统元评估指标的对比

表 1 概括了 MDAD 与两种主流元评估指标的本质差异：

- **平均估计误差**（Mean Estimation Error）：定义为 $ \operatorname{ME}(D_{\mathrm{micro}}, D_{\mathrm{full}}, \mathcal T) = \frac{1}{|\mathcal T|} \sum_{M \in \mathcal T} |\mathsf{perf}_{D_{\mathrm{micro}}}(M) - \mathsf{perf}_{D_{\mathrm{full}}}(M)| $，衡量微基准测试对单个模型性能的绝对估计偏差。其局限在于无法反映**系统性偏差**——即使微基准测试对所有模型一致高估或低估，该指标仍可能较低，而实际排序可能严重失真。

- **Kendall's tau 秩相关系数**：定义为 $ \mathrm{Kendall's} \tau = 1 - \frac{2|C|}{\binom{|T|}{2}} $，其中 $C$ 为不一致对集合。该指标在聚合层面衡量整体排序相关性，但在极端缩减样本量时可能给出误导性结论——即使微基准测试在区分相近性能模型时几乎随机，整体秩相关仍可能较高。

MDAD 通过**细粒度的成对排序一致性条件概率**克服了上述局限：它能够揭示微基准测试在哪些性能差异区间上可靠、哪些区间上不可靠，从而为评估者提供可操作的决策依据——例如，当目标模型集的全基准准确率差异普遍小于 MDAD 时，该微基准测试的排序结果不可信。

## 实验与分析

### 微基准测试方法的整体表现

本研究在 MMLU、MMLU-Pro、BBH 和 GPQA 四个基准上系统评估了六种微基准测试方法：**Anchor Points**（Vivek et al., 2024）、**tinyBenchmarks (IRT)**（Polo et al., 2024）、**Stratified sampling by confidence**（Fogliato et al., 2024b）、**Diversity-based sampling**、**Uniform random sampling** 及 **Subtask-stratified random sampling**。核心评估工具为 MDAD（最小可检测能力差异），辅以平均估计误差和 Kendall's tau 秩相关系数。

图 3 展示了各方法在 MMLU 和 MMLU-Pro 上的一致性曲线及 MDAD 汇总。关键发现如下：

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/004_Figure_3.jpg]]
*Figure 3: Comparing six micro-benchmarking approaches on two benchmarks. y-axis shows agreement (Equation 4), the probability that a micro-benchmark agrees with the full benchmark when comparing two models, as a function of how much those models differ on the full benchmark (x-axis). The rightmost column summarizes agreement curves using MDAD (Equation 5). For small microbenchmarks, all methods struggle to compare models that differ by fewer than 4 points of accuracy on the full benchmark. Anchor Points does best, followed by tinyBenchmarks. Error bars show 95% bootstrap confidence intervals over 50 trials. Figure 9 (Appendix G) shows all benchmarks*

- **极小样本量下的共同瓶颈**：当仅选择 10 个示例时，所有方法都无法以超过 65% 的概率可靠区分在全基准上准确率相差 2 个百分点的模型（图 1 左下）。在 MMLU 上，没有任何方法的 MDAD 低于 3 个准确率点；在 BBH 上，Anchor Points 表现最优，MDAD 为 6。
- **Anchor Points 在极小样本量下领先**：该方法通过源模型置信度相关性构建嵌入空间，再以 k-medoids 聚类选取簇中心作为微基准示例。在 10–25 个示例的极端缩减下，Anchor Points 的 MDAD 始终最低，是唯一在所有指标上持续优于随机抽样的方法。
- **样本量增加后随机抽样的竞争力**：当选择 250 个示例时，所有方法的 MDAD 均降至 2 或以下，随机抽样与精心设计的微基准测试方法（如 Anchor Points）表现出相当的可靠性。在 MMLU-Pro 上选择 500 个示例时，Anchor Points 与均匀随机抽样的 MDAD 均约为 2，差异可忽略。
- **tinyBenchmarks 的快速改善**：在 BBH 上，tinyBenchmarks 的 MDAD 从 10 个示例时的 16 降至 100 个示例时的 4，再降至 1000 个示例时的 1，显示出随样本量增加可靠性迅速提升的特征。

### MDAD 与现有元评估指标的对比

图 4 系统比较了 MDAD、平均估计误差和 Kendall's tau 在相同实验条件下的表现，揭示了 MDAD 的独特诊断能力：

- **细粒度区分力**：在 MMLU-Pro 上选择 10 个示例时，tinyBenchmarks 与均匀随机抽样的 Kendall's tau 完全相同，但均匀随机抽样的 MDAD 远高于 tinyBenchmarks（图 4 中点 C 和 D）。这表明聚合秩相关掩盖了关键差异——两种方法在整体排名上看似等价，但随机抽样在区分相近性能模型时明显更不可靠。
- **不同秩相关可映射到相同 MDAD**：Anchor Points 在 BBH 和 GPQA 上选择 10 个示例时，Kendall's tau 分别为 0.73 和 0.43，但 MDAD 均为 6（图 4 中点 G 和 H）。这说明 MDAD 捕捉的是微基准测试在特定性能差异区间内的一致性，而非全局排名质量。
- **对一致偏差的鲁棒性**：平均估计误差衡量单个模型的绝对性能偏差，无法区分微基准测试是否对某些模型存在系统性高估或低估。MDAD 通过成对比较框架天然规避了此问题——只要偏差在不同模型间保持一致，排名关系就不会被破坏。

### 8B 指令微调模型案例：MDAD 的解释力

图 5 展示了 MDAD 在解释实际模型比较场景中的价值。当评估 MMLU-Pro 上的一组 8B 参数指令微调模型时：

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/006_Figure_5.jpg]]
*Figure 5: When comparing 8B-parameter instruction-tuned models on MMLU-Pro: model accuracies are in a narrow range, so nearly half of pairwise accuracy differences are less than 5 points (left), which is less than the MDAD for micro-benchmarks at small dataset sizes (right)*

- 模型准确率分布极为集中，51% 的成对准确率差异小于 5 个百分点（图 5 左）。
- 在仅选择 25 个示例时，所有微基准测试方法的 MDAD 均 ≥ 5（图 5 右），意味着超过一半的成对比较无法被可靠保留。
- 这一发现直接解释了为何在极端缩减下微基准测试的排名可能误导：不是因为方法设计不佳，而是因为目标模型之间的真实性能差异本身就低于微基准测试的可检测阈值。

### 消融实验

#### 一致性阈值与分桶分辨率

MDAD 的定义依赖于两个超参数：一致性概率阈值（默认 0.8）和准确率差异的分桶分辨率（默认 0.5 个点）。图 7 展示了使用 0.7、0.8、0.9、0.95 等不同阈值时的 MDAD 结果，图 8 展示了使用 0.25、0.5、1.0 等不同分辨率时的结果。两种情况下，MDAD 的相对趋势和方法间的排序在定性上保持一致，表明指标对这些超参数选择具有较好的鲁棒性。

#### 源模型数量的影响

图 13 检验了增加源模型数量对 MDAD 的改善效果。结果表明，允许微基准测试方法访问更多源模型的完整预测数据，对 MDAD 的降低远不如增加评估样本数量有效。在几乎所有面板中，源模型数量的增加带来的 MDAD 变化几乎呈水平线，而样本量的轻微增加即可使 MDAD 显著下降。这一发现对实践具有直接指导意义：在预算有限时，优先增加微基准测试的示例数量，而非收集更多源模型的预测。

#### Anchor Points 在大样本量下的退化

一个值得注意的失败模式是：Anchor Points 在选择约 1000 个示例时，MDAD 反而升高，成为所有方法中表现最差的。论文分析认为，这可能源于 k-medoids 聚类中出现的极端集群大小不平衡——当强制选择大量簇中心时，某些簇可能仅包含极少数示例，导致所选中心缺乏代表性。相比之下，tinyBenchmarks 使用 k-means 和不同的嵌入空间，未出现类似退化。

#### 泛化到新任务划分

图 11 和图 6 检验了微基准测试在泛化到任务的保留出划分时的表现。在 MMLU、MMLU-Pro 和 BBH 上，MDAD 在保留出划分上最多增加约 0.5 个点，表明基于训练划分构建的微基准测试对同任务的新示例具有较好的泛化性。但在 GPQA（一个规模小得多的数据集）上，性能差距更为显著，提示小数据集上的微基准测试泛化风险更高。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/017_Table_5.jpg]]
*Table 5: Changes in mean estimation error and Kendall’s tau rank correlation for MMLU-Pro when generalizing to new draws of the task, as averaged across all selected micro-benchmark sizes (corresponding to the MDADs in Figure 6, which are included here for reference)*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/007_Figure_6.jpg]]
*Figure 6: Percent of subtask selected for micro-benchmark Micro-benchmark on full dataset used to construct it Micro-benchmark on new draw of the task Figure 6: MDAD is modestly higher on MMLU-Pro when predicting relative model performance on a held-out draw of the task (dashed lines) than when predicting relative performance on the full dataset used to select the micro-benchmarks (solid lines). See Appendix J for results on other datasets*

### 计算成本

表 2 报告了各方法单次试验的平均运行时间。随机抽样最快，而 tinyBenchmarks 等基于 IRT 的方法需要训练项目反应理论模型，计算开销显著更大。这一成本差异在需要多次重复试验以估计置信区间时会被放大。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/009_Table_2.jpg]]
*Table 2: Average time (seconds) for completion of one trial*

### 补充图表

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/019_Figure.jpg]]

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/020_Figure_14.jpg]]
*Figure 14: When comparing 8B-parameter instruction-tuned models on MMLU-Pro: per-model agreement with the full benchmark is lower for the models in the middle of the accuracy distribution that have more similar accuracies to many models*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/021_Figure.jpg]]
*Figure: (b) BIG-bench Hard, 7B-parameter instruct models. (c) BIG-bench Hard, 70B-parameter instruct models*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/022_Figure.jpg]]
*Figure: (a) MMLU-Pro, 70B-parameter instruct models*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/003_Table_1.jpg]]
*Table 1: Summary of differences between MDAD and existing meta-evaluation measures*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/010_Table_3.jpg]]
*Table 3: MDADs with 95% confidence intervals for up to 100 trials for uniform random sampling, Anchor Points, and tinyBenchmarks when selecting 50 and 100 examples from MMLU-Pro*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_cReExMQLiK/figures/014_Table_4.jpg]]
*Table 4: Results for the BenTo micro-benchmarking method*

## 方法谱系与知识库定位

### 微基准测试方法的谱系

本文系统评估了六种微基准测试构建方法，它们代表了当前主流的示例选择策略谱系：

**基于源模型信息的方法：**
- **Anchor Points** (Vivek et al., 2024)：通过源模型信心相关性计算示例间距离，使用 k-medoids 聚类选择簇中心作为微基准示例。其核心假设是信心模式相似的示例在区分模型能力上具有相似作用。
- **tinyBenchmarks (IRT)** (Polo et al., 2024)：基于项目反应理论，选择能最小化源模型准确率预测误差的示例子集。该方法使用 k-means 聚类，但嵌入空间与 Anchor Points 不同。
- **Stratified sampling by confidence** (Fogliato et al., 2024b)：基于源模型信心对示例聚类后进行分层随机抽样。

**不依赖源模型的方法：**
- **Uniform random sampling**：从全基准中均匀随机选择固定数量示例，公式为 $D_{\mathrm{micro}} \sim \mathrm{Unif}(\{R \subseteq D_{\mathrm{full}} | |R| = n\})$。
- **Subtask-stratified random sampling**：从每个预定义子任务中均匀随机抽取等量示例，公式为 $D_{\mathrm{micro}} = \bigcup_{i=1}^{t} R_i \mathrm{~where~} R_i \sim \mathrm{Unif}(\{R_i \subseteq D_i \big| |R_i| = \lfloor n/t \rfloor\})$。
- **Diversity-based sampling**：在源模型嵌入空间中选取均匀分散的示例。

### 元评估范式的关键转变

本文的核心贡献在于元评估范式的转变，Table 1 对此进行了概念性对比：

| 维度 | 传统元评估指标 | MDAD |
|------|---------------|------|
| 评估粒度 | 聚合级别的平均估计误差或 Kendall's τ 排名相关性 | 成对排名一致性作为全基准性能差异的函数 |
| 信息类型 | 单一标量总结 | 完整的 agreement 曲线及其 MDAD 概括 |
| 核心问题 | “微基准测试的平均误差是多少？” | “微基准测试能可靠区分多大性能差异的模型？” |

传统指标存在结构性盲区：Kendall's τ 在聚合层面可能显示高相关性，但无法揭示在极端缩减样本量时，微基准测试无法可靠区分性能相近模型的根本局限。Figure 1 的底部面板清晰展示了这一现象——当仅选择 10 个示例时，任何方法都无法以超过 65% 的概率区分全基准上准确率相差 2 个百分点的模型，尽管此时 Kendall's τ 在聚合层面仍表现良好。

### 适用边界与关键发现

**样本量的临界阈值：**
- 在极小样本量（≤25 示例）下，所有方法均面临根本性局限。在 MMLU-Pro 上选择 25 个示例时，8B 参数指令微调模型之间超过一半的成对比较（51%）无法被可靠保留（Figure 5）。
- 当样本量增至 250 示例时，所有方法的 MDAD 均降至 2 或以下，随机抽样开始与精心设计的方法具有竞争力（Figure 4）。
- 当样本量达到 500-1000 示例时，多种方法均能以超过 90% 的概率区分相差 2 个准确率点的模型。

**方法间的性能反转：**
Anchor Points 在极小样本量下具有最低的 MDAD，但在选择 1000 个示例时表现最差。这一反直觉现象的可能原因是 k-medoids 聚类中集群大小的极端不平衡——当要求选择大量示例时，某些大簇可能被过度代表，而小簇中的关键示例被忽略。相比之下，tinyBenchmarks 使用 k-means 聚类且嵌入空间不同，在大样本量下表现更稳定。

**源模型数量的边际收益递减：**
增加源模型数量对 MDAD 的改进远不如增加评估样本数量显著（Figure 13）。这一发现对实际微基准测试构建具有重要指导意义：在预算有限时，优先增加评估示例数量而非扩充源模型集合。

### 局限性与开放问题

**当前局限：**
1. **指标适用范围受限**：MDAD 目前仅适用于分类准确率，尚未扩展到开放式生成任务或 F1、文本生成质量等其他性能指标。这是该元评估框架最显著的适用边界。
2. **模型分布依赖性**：评估依赖一组固定的源模型和目标模型划分，可能无法完全代表未来新模型的性能特征。当模型架构或训练范式发生根本性变化时，现有 MDAD 估计可能需要重新校准。
3. **构建成本不对称**：不同微基准测试方法的构建成本差异显著。随机抽样最快，而 tinyBenchmarks 需要训练 IRT 模型，计算开销较大（Table 2）。
4. **泛化到新任务划分**：当微基准测试泛化到任务的保留出划分时，MDAD 最多增加约 0.5 个点（Figure 11），表明存在适度的过拟合风险，在 GPQA 等较小数据集上该差距更大。
5. **极小样本量的根本局限**：当微基准测试大小过小时，MDAD 较高，此时只能区分性能差异极大的模型，无法支持细粒度的模型比较。

**开放问题：**
1. 如何将 MDAD 扩展到准确率以外的评估指标（如 F1、文本生成质量）？这需要重新定义“性能差异”的度量方式。
2. MDAD 能否被用作微基准测试构建时的直接优化目标，以提升可靠性？当前方法均未以成对排名一致性为优化目标。
3. 在更动态的模型发布环境中，如何持续更新微基准测试以保持 MDAD 稳定性？随着新模型不断涌现，源模型集的代表性可能逐渐衰减。
4. 对于开放式生成任务，是否存在类似于 MDAD 的细粒度元评估方法？这需要解决生成质量评估本身的主观性和多维度问题。
5. 除了增加样本数量，还可以通过哪些方式降低 MDAD？例如，是否可以通过更好的示例选择策略在固定样本量下显著降低 MDAD？

**鲁棒性验证：**
本文通过多项消融实验验证了 MDAD 的稳健性：使用 0.7、0.8、0.9、0.95 等不同一致性阈值得到的 MDAD 结果在定性上相似（Figure 7）；不同的分桶分辨率（0.25, 0.5, 1.0）对 MDAD 的影响较小（Figure 8）；50 次试验已能提供稳定的置信区间（Table 3）。

## 原文 PDF

![[paperPDFs/ICLR_2026/How_Reliable_is_Language_Model_Micro_Benchmarking.pdf]]
