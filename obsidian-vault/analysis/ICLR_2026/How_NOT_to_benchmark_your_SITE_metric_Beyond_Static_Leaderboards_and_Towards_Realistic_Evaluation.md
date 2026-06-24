---
title: "How NOT to benchmark your SITE metric Beyond Static Leaderboards and Towards Realistic Evaluation"
type: paper
paper_level: B
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/How_NOT_to_benchmark_your_SITE_metric_Beyond_Static_Leaderboards_and_Towards_Realistic_Evaluation.pdf
aliases:
- SRH
- HNBYSMBSLTRE
- HNSBSL
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "用静态排序启发式、加权 Kendall tau 和保真度分析诊断 SITE 基准中的静态模型层级与分数差异失真。"
primary_logic: |
  论文先分析标准 SITE 模型动物园的真实微调排名，发现不同架构家族在多数据集上存在稳定的静态性能层级。
  随后构造不使用目标数据的静态排序启发式，并与 LogME、SFDA、NLEEP、H-Score、GBC、TransRate 等 SITE 指标比较排名相关性。
  最后引入保真度指标和 Meta-Album 改进基准，检验 SITE 分数差异是否能反映真实精度差异，并给出更现实的评估建议。
claims:
- "现有标准 SITE 基准可被不依赖目标数据的静态排序启发式大幅超越，说明基准存在琐碎化风险。"
- "仅报告加权 Kendall tau 不足以评估 SITE 指标，还需要检查分数差异与真实精度差异之间的保真度。"
- "更现实的 SITE 基准应使用性能范围重叠的模型动物园，避免由架构家族静态层级主导结果。"
---

# How NOT to benchmark your SITE metric Beyond Static Leaderboards and Towards Realistic Evaluation

> [!tip] 核心洞察
> 当前SITE基准的模型空间存在静态性能层级，使得一个简单的、不依赖目标数据的静态排序启发式就能超越所有精心设计的SITE指标，从而揭示了基准本身而非指标才是性能评估中的真正瓶颈。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 如何不正确地评测你的SITE指标：超越静态排行榜，迈向现实评估 |
| 英文题名 | How NOT to benchmark your SITE metric Beyond Static Leaderboards and Towards Realistic Evaluation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ZHKVPkJMSI) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | 静态排序启发式（Static Ranking Heuristic） |
| Dataset | Standard Benchmark, Meta-Album Benchmark |

> [!tip] 效果简介
> - 在标准基准上，一个简单的静态排序启发式（不依赖任何目标数据）取得了0.91的加权Kendall's tau，远超所有SITE指标（最佳LogME为0.573），相对提升58.8%。
> - 在改进的Meta-Album基准上，静态排序仍以0.31的加权Kendall's tau领先（最佳SFDA为0.15），相对提升82.4%。
> - SITE指标在保真度（fidelity）上表现极差：平均Pearson相关系数接近零甚至为负（如TransRate为-0.178，GBC为-0.147），表明其分数差异无法反映真实精度差异。

## 概述

本文批判性分析了源无关迁移性估计（SITE）指标的现有评估协议，指出标准基准中的模型动物园存在静态性能层级，使一个不访问目标数据的静态排序启发式即可超过复杂 SITE 指标。论文进一步引入保真度指标，检验 SITE 分数差异是否反映真实精度差异，并用 Meta-Album 构建更现实的模型选择基准，以推动 SITE 评估从静态排行榜转向任务相关、可解释的真实评估。

## 背景与动机

源无关迁移性估计（Source Independent Transferability Estimation, SITE）任务旨在无需访问预训练模型的源数据，仅通过目标数据集上的少量前向传播来预测哪个预训练模型在微调后表现最佳。近年来，研究者提出了多种SITE指标，包括基于最大标签边际似然的LogME、基于自挑战机制的SFDA、基于高斯混合模型的NLEEP、基于信息论的H-Score、基于梯度相关性的GBC以及基于互信息的TransRate。这些方法在标准基准上报告了令人鼓舞的排名相关性（如加权Kendall's tau）。

然而，本文指出当前SITE基准存在根本性缺陷：标准基准中的模型动物园（model zoo）包含来自不同架构家族（如ResNet、ViT等）的模型，但这些模型在不同数据集上表现出**静态性能层级**（static performance hierarchies）——即某些模型家族在所有数据集上始终优于其他家族。这种结构使得一个简单的、不依赖任何目标数据的**静态排序启发式**（static ranking heuristic）——即仅根据模型在历史数据集上的平均表现进行排序——就能取得与复杂SITE指标相当甚至更好的结果。这暴露了现有基准的琐碎性：它们实际上衡量的是模型家族间的固有性能差异，而非SITE指标真正应评估的、针对特定目标任务的迁移性判别能力。

## 核心创新

核心洞察：当前SITE基准的模型空间存在静态性能层级，使得一个简单的、不依赖目标数据的静态排序启发式就能超越所有精心设计的SITE指标，从而揭示了基准本身而非指标才是性能评估中的真正瓶颈。

具体而言，标准基准中的模型（如ResNet-50、ResNet-101、ViT-B/16等）在不同数据集上表现出高度一致的性能排序：例如，ViT-B/16几乎总是在所有6个数据集上表现最佳，而ResNet-50则始终垫底。这种结构使得任何能够捕捉到模型家族间固有差异的指标（包括静态排序）都能获得高排名相关性，但无法为实际模型选择提供有意义的指导——因为在实际场景中，用户需要的是在性能相近的模型之间做出区分。

本文的核心贡献不在于提出新的SITE指标，而在于：
1. 通过静态排序启发式暴露了现有基准的琐碎性；
2. 引入**保真度**（fidelity）作为新的评估维度，衡量SITE分数差异与真实精度差异之间的相关性；
3. 提出了构建更现实、更有意义的SITE基准的最佳实践。

## 整体框架

本文不提出新的SITE方法或框架，而是构建了一个**基准评估框架**，用于系统性地诊断现有SITE基准的缺陷。该框架包含以下核心组件：

1. **模型动物园分析**：对标准基准中的模型进行排序分布可视化（![[assets/figures/papers/e7bdcb2e-34f4-4257-a7a9-cb582373753d/figures/009_Figure_3.jpg]]
*Figure 3: Visualization of the ranking distribution of models in the standard benchmark(ordered by fine tuned performance). The models at the top occupy the first ranks in most datasets. Table 1: Comparison of transferability estimations, computed by weighted Kendall’s tau, for a static ranking versus SITE metrics on the standard benchmark. The static ranking achieves the highest $\tau _ { w }$ overall*

），揭示静态性能层级的存在。
2. **静态排序启发式**：定义一个不依赖目标数据的基线方法，仅根据模型在多个数据集上的历史平均性能进行排序，作为基准琐碎性的探针。
3. **排名评估**：使用加权Kendall's tau（τ_w）衡量预测排名与真实微调性能排名之间的一致性。
4. **保真度评估**：引入分数差异与精度差异之间的Pearson相关性作为新的评估维度，衡量SITE指标在区分性能相近模型时的可靠性。
5. **改进基准构建**：基于Meta-Album的15个数据集构建一个更现实的基准，确保模型空间具有重叠的性能范围，消除静态层级。

## 核心模块与公式推导

本文的核心在于评估框架，而非方法本身。关键公式如下：

**排名相关性（加权Kendall's tau）**：
$$
\tau_w = \frac{2}{M(M-1)} \sum_{i<j} \text{sgn}(G_i - G_j) \, \text{sgn}(T_i - T_j) \, w(\rho(i), \rho(j))
$$
其中 \(G_i\) 和 \(T_i\) 分别是模型 \(i\) 的真实微调性能和SITE分数，\(\rho(i)\) 是模型 \(i\) 在真实排名中的位置，\(w\) 是基于排名位置的权重函数。该指标衡量预测排名与真实排名之间的一致性，对顶部排名给予更高权重。

**保真度评估**：
$$
\Delta_{\text{Acc}}(X, Y; D) = \text{Acc}(X, D) - \text{Acc}(Y, D)
$$
$$
\Delta_T(X, Y) = T(X) - T(Y)
$$
保真度定义为所有模型对 \((X, Y)\) 上 \(\Delta_{\text{Acc}}\) 与 \(\Delta_T\) 之间的Pearson相关系数。理想情况下，SITE指标应满足：
$$
\forall A,B,C,D \in \mathcal{M}, \quad \Delta_{\text{Acc}}(A,B;D) > \Delta_{\text{Acc}}(C,D;D) \Rightarrow \Delta_T(A,B) > \Delta_T(C,D)
$$
即分数差异应保持精度差异的序关系。

**静态排序启发式**：
静态排序不依赖任何目标数据，而是根据模型在多个数据集上的平均微调性能进行排序。形式上，对于模型 \(X\)，其静态分数为：
$$
S_{\text{static}}(X) = \frac{1}{|\mathcal{D}|} \sum_{D \in \mathcal{D}} \text{Acc}(X, D)
$$
其中 \(\mathcal{D}\) 是用于构建排序的历史数据集集合。

## 实验与分析

**标准基准上的排名结果**：
![[assets/figures/papers/e7bdcb2e-34f4-4257-a7a9-cb582373753d/figures/011_Table_2.jpg]]
*Table 2: $\tau _ { w }$ performance on 15 benchmark datasets from Meta-Album, showing the performance of LogME, SFDA,HScore,GBC, NLEEP, TransRate and Static Ranker*

展示了在标准基准（6个数据集）上的加权Kendall's tau结果。静态排序启发式以0.91的τ_w大幅领先所有SITE指标，最佳SITE指标LogME仅为0.573，相对差距达58.8%。其他指标如SFDA（0.448）、NLEEP（0.553）、H-Score（0.552）、GBC（0.007）和TransRate（0.195）均远低于静态排序。这一结果直接证明了标准基准的琐碎性：一个不依赖任何目标数据的简单启发式就能取得最佳性能。

**Meta-Album基准上的排名结果**：
![[assets/figures/papers/e7bdcb2e-34f4-4257-a7a9-cb582373753d/figures/015_Table_3.jpg]]
*Table 3: Average Pearson correlation between accuracy differences and metric score differences across datasets*

展示了在改进的Meta-Album基准（15个数据集）上的结果。静态排序仍以0.31的τ_w领先，最佳SITE指标SFDA为0.15，相对提升82.4%。尽管所有方法的绝对τ_w值均显著低于标准基准（表明Meta-Album更具挑战性），但静态排序的持续优势表明，即使在没有明显静态层级的基准中，SITE指标的整体预测能力仍然有限。

**保真度分析**：
![[assets/figures/papers/e7bdcb2e-34f4-4257-a7a9-cb582373753d/figures/016_Table_4.jpg]]
*Table 4: Original results from LogME NLP Experiments*

报告了保真度评估结果——即分数差异与精度差异之间的平均Pearson相关性。所有SITE指标均表现极差：GBC为-0.147，SFDA为0.43，LogME为0.047，NLEEP为0.299，H-Score为0.101，TransRate为-0.178。这些接近零甚至为负的相关性表明，SITE指标的分数差异几乎无法反映模型之间的真实性能差异，即它们无法可靠地指导用户选择性能相近的模型。

**可视化分析**：
![[assets/figures/papers/e7bdcb2e-34f4-4257-a7a9-cb582373753d/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of Source Independent Transferability Estimation (SITE): Given a set of pretrained models (on the left), a SITE metric computes a score T _ { m } based on extracted features on a target dataset. The scores T _ { m } are used to rank the pre-trained models according to their transferability*

展示了标准基准中模型的排序分布，清晰地揭示了静态层级：ViT-B/16始终占据顶部位置，而ResNet-50始终位于底部。![[assets/figures/papers/e7bdcb2e-34f4-4257-a7a9-cb582373753d/figures/010_Figure_4.jpg]]
*Figure 4: Heatmap correlation of $\Delta _ { A c c }$ and $\Delta _ { T }$

的热力图进一步展示了Δ_Acc与Δ_T之间的弱相关性。相比之下，![[assets/figures/papers/e7bdcb2e-34f4-4257-a7a9-cb582373753d/figures/012_Figure_5.jpg]]
*Figure 5: Visualization of the ranking distribution of models in the improved benchmark. Most of the models share top spots and no model is always top or bottom rank*

显示Meta-Album基准的排序分布更加分散，模型性能范围有重叠，因此更具挑战性。![[assets/figures/papers/e7bdcb2e-34f4-4257-a7a9-cb582373753d/figures/013_Figure_6.jpg]]
*Figure 6: Heatmap correlation of $\Delta _ { A c c }$ and $\Delta _ { T }$ for Top-4 Models

和![[assets/figures/papers/e7bdcb2e-34f4-4257-a7a9-cb582373753d/figures/014_Figure_7.jpg]]
*Figure 7: Heatmap correlation of $\Delta _ { A c c }$ and $\Delta _ { T }$ for Bottom-4 models

分别展示了顶部4个和底部4个模型的Δ热力图，进一步证实了保真度问题。

**消融实验**：
![[assets/figures/papers/e7bdcb2e-34f4-4257-a7a9-cb582373753d/figures/002_Figure_2.jpg]]
*Figure 2: (a) CIFAR10*

展示了逐步移除同一架构家族模型后各指标性能的变化。当移除ViT家族模型后，所有SITE指标的τ_w均显著下降，而静态排序的下降幅度较小，进一步证实了静态层级对指标性能的贡献。

## 方法谱系与知识库定位

本文属于**SITE任务评估方法论**的批判性分析工作，而非提出新的SITE指标。其方法谱系定位如下：

- **任务归属**：Source Independent Transferability Estimation (SITE) —— 预训练模型选择任务。
- **方法家族**：基准评估与诊断方法。本文不提出新的SITE指标，而是引入**静态排序启发式**作为探针，用于暴露现有基准的缺陷。
- **父方法/基线关系**：本文系统性地对比了6个主流SITE指标（LogME, SFDA, NLEEP, H-Score, GBC, TransRate），这些方法均属于SITE任务中的直接基线。
- **改变的槽位**：
  1. **评估协议**（evaluation_protocol）：从仅使用加权Kendall's tau评估排名一致性，扩展为同时评估**保真度**（分数差异与精度差异的Pearson相关性）。
  2. **模型动物园组成**（model_zoo_composition）：从包含静态性能层级的模型集合，改进为具有重叠性能范围的多样化模型集合。
- **后续定位**：本文为SITE评估提供了新的标准，未来的SITE指标应在更现实的基准上同时报告排名相关性和保真度。研究者应避免使用存在静态层级的模型动物园，并应验证其指标在区分性能相近模型时的可靠性。本文的发现也呼应了Agostinelli等人（2022）关于迁移性指标稳定性的工作，以及Chaves等人（2024）关于预测迁移性能基础问题的研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/How_NOT_to_benchmark_your_SITE_metric_Beyond_Static_Leaderboards_and_Towards_Realistic_Evaluation.pdf]]
