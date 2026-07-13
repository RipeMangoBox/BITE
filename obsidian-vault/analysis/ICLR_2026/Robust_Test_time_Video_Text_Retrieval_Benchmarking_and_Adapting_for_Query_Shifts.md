---
title: "Robust Test-time Video-Text Retrieval: Benchmarking and Adapting for Query Shifts"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Robust_Test_time_Video_Text_Retrieval_Benchmarking_and_Adapting_for_Query_Shifts.pdf
project_link: null
code_link: https://github.com/bingqingzhang/vtr_tta.git
openreview_forum_id: FRkJ3ehpNN
aliases:
- HVHATTVTR
- RTTVTRBAQS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过直接抑制被放大的hubness——即在相似度空间中降低热门gallery项的支配性——可以使检索分布重新平衡，从而恢复鲁棒性能。"
primary_logic: "在测试时引入Hubness Suppression Memory (HSM)对相似度矩阵进行双侧重标定，并结合多粒度损失（帧间/帧内均匀性和跨模态对齐）保持时序特征一致性，能够从根本上缓解查询偏移引起的hubness问题，大幅提升视频-文本检索的鲁棒性。"
claims:
- "查询偏移使k-occurrence分布从平衡状态变为重尾分布，形成严重的hubness。"
- "HAT-VTR成功恢复了平衡的k-occurrence分布，表明hubness被有效抑制。"
- "在MSRVTT-1kA severity 5的v2t任务上，HAT-VTR平均Recall@1达到26.2%，比最强基线TCR的21.4%高出4.8个百分点。"
- "MSRVTT-1kA (视频扰动, severity=5) 上 v2t R@1 (平均%) = 26.2 (CLIP4Clip) / 30.3 (X-Pool)"
---

# Robust Test-time Video-Text Retrieval: Benchmarking and Adapting for Query Shifts

> [!tip] 核心洞察
> 在测试时引入Hubness Suppression Memory (HSM)对相似度矩阵进行双侧重标定，并结合多粒度损失（帧间/帧内均匀性和跨模态对齐）保持时序特征一致性，能够从根本上缓解查询偏移引起的hubness问题，大幅提升视频-文本检索的鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 鲁棒的测试时视频-文本检索：面向查询偏移的基准测试与自适应 |
| 英文题名 | Robust Test-time Video-Text Retrieval: Benchmarking and Adapting for Query Shifts |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=FRkJ3ehpNN) · [GitHub](https://github.com/bingqingzhang/vtr_tta.git) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | HAT-VTR (Hubness Alleviation for Test-time Video-Text Retrieval) |
| Dataset | MSRVTT-1kA (视频扰动, severity=5), ActivityNet (视频扰动, MSRVTT-1kA (文本扰动, severity=mean), 跨数据集适应 (QGS: MSRVTT→ActivityNet) |

> [!tip] 效果简介
> - MSRVTT-1kA (视频扰动, severity=5) 上，v2t R@1 (平均%) 为 26.2 (CLIP4Clip) / 30.3 (X-Pool)，对比 TCR: 21.4 (CLIP4Clip) / 24.0 (X-Pool)，变化 +4.8 / +6.3。
> - ActivityNet (视频扰动, severity=5) 上，v2t R@1 (平均%) 为 22.28 (CLIP4Clip) / 20.35 (X-Pool)，对比 TCR: 12.86 (CLIP4Clip) / 14.50 (X-Pool)，变化 +9.42 / +5.85。
> - MSRVTT-1kA (文本扰动, severity=mean) 上，t2v R@1 (平均%) 为 33.5 (CLIP4Clip) / 36.5 (X-Pool)，对比 TCR: 31.4 (CLIP4Clip) / 35.0 (X-Pool)，变化 +2.1 / +1.5。

## 概要

视频-文本检索（VTR）模型在标准测试集上表现优异，但在真实场景中面临严峻的测试时查询偏移（query shift）挑战——测试查询因视频退化或文本扰动而与训练分布产生偏差。本文揭示，查询偏移会显著放大检索中的**hubness现象**：少数gallery项成为支配性的“hub”，导致k-occurrence分布从平衡状态变为重尾分布（Fig. 2(b-c)），检索排名严重偏向这些热门项，最终引发性能崩溃（Fig. 2(a)）。

针对这一瓶颈，本文提出**HAT-VTR（Hubness Alleviation for Test-time Video-Text Retrieval）**，一种直接抑制被放大hubness的测试时自适应框架。其核心思路是：在相似度空间中降低热门gallery项的支配性，使检索分布重新平衡。HAT-VTR通过两条并行路径实现这一目标——**Hubness Suppression Memory (HSM)** 利用历史相似度矩阵对当前相似度进行双边重标定，生成去hubness的相似度矩阵；**多粒度损失**（帧间/帧内均匀性和跨模态对齐）则持续更新查询编码器，保持时序特征一致性。

实验表明，HAT-VTR能有效恢复平衡的k-occurrence分布（Fig. 2(f)），并在多个基准上显著超越现有方法。在MSRVTT-1kA severity 5的v2t任务上，HAT-VTR平均Recall@1达到26.2%（CLIP4Clip骨干），比最强基线TCR的21.4%高出4.8个百分点；在ActivityNet上优势更为显著（+9.42个百分点）。该方法在文本扰动、跨数据集适应和零样本适应场景下同样表现稳健。



视频-文本检索（VTR）在视频理解、跨模态搜索等任务中扮演着核心角色。现有VTR模型在标准基准上已取得显著进展，但其鲁棒性评估长期局限于训练-测试数据同分布的理想假设。真实世界的视频和文本查询不可避免地受到采集噪声、压缩伪影、光照变化、语言表达偏移等因素的影响，形成**测试时查询分布偏移（query shift）**。当预训练VTR模型直接部署到此类偏移场景时，检索性能会发生严重退化，甚至完全崩溃（Figure 2(a)），这暴露了当前VTR系统在实际应用中的脆弱性。

### 查询偏移下的Hubness放大现象

为诊断查询偏移导致性能崩溃的根本原因，本文对检索过程中的**k-occurrence分布**进行了分析。k-occurrence衡量每个gallery项被检索为top-k结果的频率：在平衡的检索系统中，该分布应近似均匀，即不存在少数gallery项支配检索排名的现象。然而，实验表明，当查询受到扰动（如高斯噪声）时，k-occurrence分布从平衡状态急剧转变为**重尾分布**（Figure 2(b-c)），少数gallery项成为“hub”，被大量查询重复检索到。这种**hubness放大**效应意味着检索排名严重偏向这些热门项，而真正相关的gallery项被系统性压制，从而导致检索精度的全面崩溃。

上述发现揭示了一个关键瓶颈：**测试时查询分布偏移会显著放大VTR中的hubness现象，这是导致性能退化的核心机制**。因此，若能直接抑制被放大的hubness——即在相似度空间中降低热门gallery项的支配性——就有望使检索分布重新平衡，从而恢复鲁棒性能。

### 现有测试时自适应方法的局限

测试时自适应（Test-Time Adaptation, TTA）提供了一种应对查询偏移的可行范式：在推理阶段利用未标记的测试数据对模型进行在线微调，无需访问源训练数据。然而，现有TTA方法存在明显不足：

- **通用TTA方法**（如TENT、SAR、EATA）主要基于熵最小化原则设计，旨在提升模型在目标域的预测置信度。它们未考虑检索任务中特有的hubness问题，因此在VTR场景下效果有限。
- **面向检索的TCR方法**通过引入表示均匀性损失来处理查询偏移，在一定程度上缓解了hubness（Figure 2(d)），但其仅从表示空间层面施加约束，未能直接作用于相似度矩阵中被放大的hub项，导致抑制效果不彻底。

### 本文动机与核心思路

基于上述分析，本文提出一种直接针对hubness放大的测试时自适应框架——**HAT-VTR (Hubness Alleviation for Test-time Video-Text Retrieval)**。其核心思路是：在测试时引入**Hubness Suppression Memory (HSM)** 对相似度矩阵进行双边重标定，直接降低热门gallery项的支配性；同时结合**多粒度损失**（帧间/帧内均匀性和跨模态对齐）保持时序特征一致性，防止自适应过程中出现表示崩溃。Figure 2(e-g)展示了该方案的整体效果：HAT-VTR成功恢复了平衡的k-occurrence分布，并在检索精度上取得显著提升。

> **注意**：关于查询偏移如何引起不同程度hubness放大的深层理论机制，目前仍缺乏统一的分析框架，这限制了针对性自适应策略的进一步设计。该问题留待后续研究探索。



## 核心方法与创新机理

HAT-VTR的核心创新在于直接瞄准测试时查询偏移引发的**hubness放大**这一根本瓶颈，而非像现有方法那样仅依赖熵最小化或表示均匀性。其关键changed slots体现在三个层面：

### 1. 在线相似度计算：从直接余弦相似度到Hubness Suppression Memory (HSM)

传统测试时自适应方法直接使用查询-图库的余弦相似度矩阵进行检索，当查询偏移导致hubness放大时，少数gallery项成为支配性的“hub”，严重扭曲检索排名。HAT-VTR引入**Hubness Suppression Memory (HSM)**，通过记忆最近的$K$个相似度矩阵构建历史聚合矩阵$\bar{S} = \operatorname{Concat}(S_t, S_{t-1}, \ldots, S_{t-K+1})$，并分别计算**图库中心权重**和**查询中心权重**，对当前相似度进行双边重标定：

$$\hat{S} = m (\bar{S} \odot W_{\mathrm{gallery}}) + (1-m)(\bar{S} \odot W_{\mathrm{query}})$$

这一操作直接降低热门gallery项的支配性，在相似度空间层面抑制hubness，而非仅在表示空间间接缓解。消融实验表明，HSM同时参与目标选择和后验重排时效果最优（平均R@1达30.1），单独使用任一阶段约降低2个百分点（Table 6）。当hubness放大程度较低时（如Temporal Scrambling、Backtranslation），HSM本身即提供主要增益，而TCR训练组件收益微弱甚至产生负优化（Table 38）。

### 2. 自适应监督信号：从单一熵最小化到多粒度损失

现有TTA方法（TENT、TCR等）仅使用熵最小化或添加均匀性损失，未能充分利用视频的时序层次结构。HAT-VTR设计了**三类多粒度损失**：

- **多粒度均匀性损失 ($\mathcal{L}_{\mathrm{MGUNI}}$)**：包含帧间均匀性项$\mathcal{L}_{\mathrm{inter}}$（分散批次中的全局查询表示）和帧内均匀性项$\mathcal{L}_{\mathrm{intra}}$（保持单视频内帧级特征的多样性），防止表示崩溃。
- **多粒度跨模态对齐损失 ($\mathcal{L}_{\mathrm{MGCM}}$)**：包含全局对齐项$\mathcal{L}_{\mathrm{global}}$（批次平均表示与Reliable Memory中稳定目标的对齐）和帧级对齐项（帧级特征的交叉协方差与Reliable Memory对齐），确保视频与文本表示空间的一致性。
- **噪声自适应熵最小化 ($\mathcal{L}_{\mathrm{NA}}$)**：通过Reliable Memory导出的自适应权重$S(\mathbf{p}_i) = \max(1-\eta(\mathbf{p}_i)/E_m,0)$过滤不可靠样本，防止噪声累积。

总损失为$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{MGUNI}} + \mathcal{L}_{\mathrm{MGCM}} + \mathcal{L}_{\mathrm{NA}}$。消融实验证实三项损失均对性能有正向贡献，同时使用达到最优（Table 7）。

### 3. 可靠样本选择：从固定阈值到Hubness感知目标选择

传统方法基于原始相似度或固定阈值选择伪正例，在hubness放大时容易选入偏差样本。HAT-VTR利用**HSM抑制后的相似度**进行“hubness感知目标选择”，从去偏后的相似度矩阵中选取更可靠的query-gallery对更新**Reliable Memory (RM)**。RM存储高可靠对及其特征，为跨模态对齐和熵正则提供稳定的历史目标，缓解灾难性遗忘。

### 核心因果机制

这三个changed slots形成闭环：**HSM在相似度空间直接抑制hubness** → 基于去偏相似度选择可靠样本填充RM → RM为多粒度损失提供稳定目标 → 多粒度损失更新查询编码器 → 更新后的编码器产生更好的表示，进一步降低hubness。这一机制从根本上切断了“查询偏移→hubness放大→检索崩溃”的因果链，实验证据表明HAT-VTR能显著降低hubness指标——在Gaussian噪声场景下，skewness从9.09（无TTA）降至0.97（HAT-VTR），恢复了平衡的k-occurrence分布（Table 39, Fig. 2(f)）。



![[assets/figures/papers/iclr26_0012_FRkJ3ehpNN_Robust_Test-time_Video-Text_Retrieval_Benchmarki/figures/011_Figure_4.jpg]]
*Figure 4: The pipeline of HAT-VTR. It operates via two parallel components: Hubness Suppression Memory (HSM) refines similarity scores to counteract hubness, while the query encoder is continuously updated using multi-granular losses to adapt to the target domain*

HAT-VTR 的整体管道由两条并行分支构成，分别解决查询偏移引发的两个核心问题：相似度空间中的 hubness 放大，以及查询编码器在目标域上的表示退化。

**输入与输出流。** 给定一个未标记的目标域视频查询流 $X^Q$ 和一个固定的图库 $X^G$，预训练的 VTR 双编码器 $f_{\theta^Q}$ 和 $f_{\theta^G}$ 分别提取查询嵌入 $Z^Q$ 和图库嵌入 $Z^G$，形成初始相似度矩阵 $S^{Q,G} = g_\theta(Z^Q, Z^G)$。HAT-VTR 在此基础之上并行运行两个组件：Hubness Suppression Memory（HSM）对相似度矩阵进行双边重标定，输出去 hubness 的相似度矩阵 $\hat{S}$；同时，查询编码器通过多粒度损失持续更新，输出适应目标域的查询表示。最终检索结果由 $\hat{S}$ 重排得到。

**分支一：Hubness Suppression Memory。** HSM 维护一个记忆库，存储最近 $K-1$ 个相似度矩阵。当前矩阵 $S_t$ 与历史矩阵沿行拼接为聚合矩阵 $\bar{S}$。HSM 从 $\bar{S}$ 中分别计算图库中心权重 $W_{\text{gallery}}$ 和查询中心权重 $W_{\text{query}}$，通过加权融合得到 hubness 抑制后的相似度矩阵：

$$\hat{S} = m (\bar{S} \odot W_{\text{gallery}}) + (1-m)(\bar{S} \odot W_{\text{query}})$$

其中 $m$ 为融合系数。这一双边重标定机制直接降低了热门图库项的支配性，使 k-occurrence 分布从重尾恢复为平衡状态（Fig. 2(b-c) vs Fig. 2(f)）。$\hat{S}$ 同时服务于两个下游目的：为分支二提供 hubness 感知的可靠目标选择，以及作为最终检索的相似度矩阵。

**分支二：查询编码器在线自适应。** 查询编码器的可适配参数（仅 Layer Normalization 层）通过三项多粒度损失进行更新：

1. **多粒度均匀性损失 $\mathcal{L}_{\text{MGUNI}}$**：包含帧间均匀性项（将批次中每个查询的全局表示推离批次均值）和帧内均匀性项（保持单视频内帧级特征的多样性），防止表示崩溃。
2. **多粒度跨模态对齐损失 $\mathcal{L}_{\text{MGCM}}$**：包含全局对齐（当前批次查询-图库的模态差距与 Reliable Memory 中的稳定目标差距对齐）和帧级对齐（帧级特征的交叉协方差与 Reliable Memory 对齐），维持视频与文本表示空间的一致性。
3. **噪声自适应熵最小化 $\mathcal{L}_{\text{NA}}$**：对高熵样本赋予低权重甚至零权重，防止不可靠样本污染在线自适应过程。

Reliable Memory 存储通过 HSM 筛选的高可靠 query-gallery 对及其特征，为 $\mathcal{L}_{\text{MGCM}}$ 和 $\mathcal{L}_{\text{NA}}$ 提供稳定的历史目标，缓解灾难性遗忘。

**模块间协作关系。** HSM 和自适应训练并非独立运行，而是通过“hubness 感知目标选择”形成闭环：HSM 输出的 $\hat{S}$ 用于选择可靠的伪正例对，填充 Reliable Memory；Reliable Memory 反过来为自适应损失提供稳定的监督信号。消融实验表明，HSM 同时参与目标选择和最终重排时效果最优（平均 30.1 R@1），单独使用任一角色均会导致约 2 个百分点的下降（Table 6）。三项损失组件同时使用时达到最优性能，移除任一项均造成明显退化（Table 7）。



### 4.1 问题形式化与预备知识

视频-文本检索（VTR）采用双编码器架构，查询编码器 $f_{\theta^Q}$ 和图库编码器 $f_{\theta^G}$ 分别将输入映射到嵌入空间：

$$Z^Q = \{ f_{\theta^Q}(x) \mid x \in X^Q \}, \quad Z^G = \{ f_{\theta^G}(x) \mid x \in X^G \}$$

相似度矩阵由函数 $g_\theta$ 计算（通常为余弦相似度）：

$$S^{Q,G} = g_\theta(Z^Q, Z^G)$$

对于在线测试批次 $X^{Q_b}$，对应概率（软分配）通过温度缩放 softmax 得到：

$$\mathbf{p} = \mathrm{Softmax}(Z^{Q_b}(Z^G)^T / \tau)$$

测试时自适应（TTA）的核心目标是最小化该概率分布的熵 $\eta(\cdot)$：

$$\min_{\theta \in \Theta_s} \mathcal{L}_{\mathrm{TTA}}(\mathbf{p}) = \min_{\theta \in \Theta_s} \eta(\mathbf{p})$$

然而，单纯熵最小化在查询偏移下会加剧 hubness 现象——少数图库项成为支配性"hub"，导致检索排名严重偏向这些项，引发性能崩溃（Fig. 2(a-c)）。

### 4.2 Hubness Suppression Memory (HSM)

HSM 是 HAT-VTR 的核心创新模块，直接在相似度空间抑制被放大的 hubness。其工作机制分为三步：

**历史聚合。** HSM 维护一个记忆库 $\mathcal{M}_{t-1}$，存储最近 $K-1$ 个相似度矩阵。将当前矩阵 $S_t$ 与历史矩阵沿行拼接，形成聚合矩阵：

$$\bar{S} = \operatorname{Concat}(S_t, S_{t-1}, \ldots, S_{t-K+1})$$

**双边权重计算。** 基于 $\bar{S}$，分别计算图库中心权重 $W_{\mathrm{gallery}}$ 和查询中心权重 $W_{\mathrm{query}}$。图库中心权重反映每个图库项在历史中被检索的频率（高频 hub 获得低权重），查询中心权重反映查询侧的分布特性。

**双边重标定。** 将两个权重矩阵分别与 $\bar{S}$ 逐元素相乘，通过混合系数 $m$ 加权融合，得到 hubness 抑制后的相似度矩阵：

$$\hat{S} = m (\bar{S} \odot W_{\mathrm{gallery}}) + (1 - m)(\bar{S} \odot W_{\mathrm{query}})$$

$\hat{S}$ 随后用于两个关键环节：（1）**Hubness 感知目标选择**——从去偏后的相似度中选取更可靠的 query-gallery 对更新 Reliable Memory；（2）**后验重排**——直接作为最终检索排序依据。消融实验证实，HSM 同时参与目标选择和最终重排时效果最优（平均 30.1 R@1），单独移除任一环节约降低 2 个百分点（Table 6）。

### 4.3 多粒度自适应损失

HAT-VTR 通过三类损失函数更新查询编码器的层归一化参数，利用视频的时序层次结构保持特征一致性。

**多粒度均匀性损失 $\mathcal{L}_{\mathrm{MGUNI}}$。** 防止表示崩溃，包含两项：

- **帧间均匀性**：将批次中每个查询的全局表示推离批次均值，促进表示多样性：

$$\mathcal{L}_{\mathrm{inter}} = \frac{1}{B} \sum_{i=1}^{B} \exp(-\|Z_i^{Q_b} - \bar{Z}^{Q_b}\|_2 / t)$$

- **帧内均匀性**：保持单视频内帧级特征的多样性，防止时序信息坍缩：

$$\mathcal{L}_{\mathrm{intra}} = \frac{1}{B} \sum_{i=1}^{B} \left( \frac{1}{T} \sum_{f=1}^{T} \exp(-\|Z_{i,f}^{Q_b} - Z_i^{Q_b}\|_2 / t) \right)$$

**多粒度跨模态对齐损失 $\mathcal{L}_{\mathrm{MGCM}}$。** 对齐视频与文本的表示空间，同样包含两个粒度：

- **全局对齐**：使当前批次查询和伪正例图库的模态差距与 Reliable Memory 中稳定目标的差距对齐：

$$\mathcal{L}_{\mathrm{global}} = (\| \bar{Z}^{Q_b} - \bar{Z}^{G_b} \|_2 - \| \bar{Z}_{\mathcal{RM}}^{Q} - \bar{Z}_{\mathcal{RM}}^{G} \|_2)^2$$

- **帧级对齐**：通过帧级特征的交叉协方差与 Reliable Memory 对齐（具体公式见原文 Eq.10）。

**噪声自适应熵损失 $\mathcal{L}_{\mathrm{NA}}$。** 在提升模型预测置信度的同时，通过自适应权重 $S(\mathbf{p}_i)$ 过滤不可靠样本：

$$\mathcal{L}_{\mathrm{NA}} = \frac{1}{\sum_i \mathbb{I}_{\{S(\mathbf{p}_i)>0\}}} \sum_{i=1}^{B} S(\mathbf{p}_i) \eta(\mathbf{p}_i), \quad S(\mathbf{p}_i) = \max(1 - \eta(\mathbf{p}_i)/E_m, 0)$$

其中 $S(\mathbf{p}_i)$ 对高熵样本给予低权重（甚至零权重），防止噪声样本污染在线自适应过程。

**总损失。** 三项损失的线性组合构成最终优化目标：

$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{MGUNI}} + \mathcal{L}_{\mathrm{MGCM}} + \mathcal{L}_{\mathrm{NA}}$$

消融实验（Table 7）证实三项损失均对性能有正向贡献，同时使用达到最优（30.1 Avg.），移除任一项均导致性能下降。

### 4.4 Reliable Memory (RM)

Reliable Memory 存储通过 HSM 筛选的高可靠 query-gallery 对及其特征，为跨模态对齐损失和熵正则提供稳定的历史目标。其核心作用是缓解在线自适应中的灾难性遗忘——当新批次数据分布剧烈变化时，RM 中的稳定锚点防止模型过度偏离已学到的有效表示。RM 的更新依赖于 HSM 抑制后的相似度矩阵 $\hat{S}$ 进行 hubness 感知的目标选择，确保存入记忆的样本对不受 hubness 偏差影响。



## 实验与关键发现

### 核心瓶颈验证：查询偏移放大Hubness导致检索崩溃

在MSRVTT-1kA基准上施加高斯噪声扰动后，代表性VTR模型（CLIP4Clip、X-Pool）的v2t Recall@1从正常水平急剧崩溃至约8-10%（Figure 2(a)）。进一步诊断发现，性能崩溃的根源在于**查询偏移显著放大了hubness现象**：k-occurrence分布从平衡状态变为重尾分布（Figure 2(b-c)），少数图库项成为支配性的“hub”，导致检索排名严重偏向这些项。

![[assets/figures/papers/iclr26_0012_FRkJ3ehpNN_Robust_Test-time_Video-Text_Retrieval_Benchmarki/figures/009_Figure_2.jpg]]
*Figure 2: An overview of the motivation, solution, and performance of our proposed HAT-VTR method. (a) We first observe that the performance of representative video-to-text retrieval models collapses under Gaussian perturbations. (b) To diagnose this failure, we analyze the k-occurrence distribution (the number of times a gallery item is retrieved as the top-15 result), which is relatively balanced on original data. (c) When the query is corrupted, the distribution becomes heavy-tailed, highlighting a worsened hubness phenomenon where a few videos dominate retrieval rankings. (d) Applying the existing TTA method (TCR) partially mitigates the hubness problem. (e) To address this root cause, we propose...*

HAT-VTR通过Hubness Suppression Memory (HSM)直接抑制相似度空间中被放大的hubness，成功恢复了平衡的k-occurrence分布（Figure 2(f)），验证了“抑制hubness即可恢复鲁棒检索”的核心因果假设。

### 视频查询偏移下主结果

在MSRVTT-1kA severity 5的v2t任务上，HAT-VTR在CLIP4Clip骨架下平均Recall@1达到**26.2%**，比最强基线TCR的21.4%高出**4.8个百分点**；在X-Pool骨架下达到**30.3%**，比TCR的24.0%高出**6.3个百分点**（Table 1）。在所有12种视频扰动类型（包括Gaussian、Impulse、Fog、Snow、Elastic Distortion、H.264压缩、Motion Blur、Defocus、Main Object Occlusion、Style Transfer、Event Disruption、Temporal Scrambling）上，HAT-VTR均一致优于全部TTA基线（TENT、READ、SAR、EATA、TCR）。

![[assets/figures/papers/iclr26_0012_FRkJ3ehpNN_Robust_Test-time_Video-Text_Retrieval_Benchmarki/figures/012_Table_1.jpg]]
*Table 1: Comparisons v2t results on the MSRVTT-1kA with severity degree 5, regarding the Recall@1 (%) metric. The best results are in bold, and ours are highlighted*

在ActivityNet severity 5的v2t任务上，HAT-VTR在CLIP4Clip骨架下平均Recall@1达到**22.28%**，比TCR的12.86%高出**9.42个百分点**（Table 2），增益更为显著，表明方法对不同数据集和视频分布具有泛化性。

![[assets/figures/papers/iclr26_0012_FRkJ3ehpNN_Robust_Test-time_Video-Text_Retrieval_Benchmarki/figures/013_Table_2.jpg]]
*Table 2: Comparisons on v2t R@1 on the ActivityNet dataset with the highest severity degree*

### 文本查询偏移下主结果

在MSRVTT-1kA的文本扰动下（15种扰动覆盖字符、词、句三个粒度），HAT-VTR在CLIP4Clip骨架下t2v平均Recall@1达到**33.5%**，比TCR的31.4%高出**2.1个百分点**；在X-Pool骨架下达到**36.5%**，比TCR的35.0%高出**1.5个百分点**（Table 3）。文本侧的性能增益虽小于视频侧，但仍一致领先，表明HSM和多粒度损失对跨模态偏移均有效。

![[assets/figures/papers/iclr26_0012_FRkJ3ehpNN_Robust_Test-time_Video-Text_Retrieval_Benchmarki/figures/014_Table_3.jpg]]
*Table 3: Comparisons on t2v Recall@1 (%) on the MSRVTT-1kA dataset under text perturbations*

### 跨数据集与零样本适应

在跨数据集适应场景（QGS: MSRVTT→ActivityNet）中，HAT-VTR的v2t Recall@1达到**36.10%**，比TCR的34.21%高出**1.89个百分点**（Table 4）。在零样本适应场景（QGS: MSRVTT）中，HAT-VTR达到**35.40%**，比TCR的33.90%高出**1.50个百分点**（Table 5）。这表明方法在无源数据和未见目标域下仍能稳定提升检索鲁棒性。

### 消融研究：HSM集成策略

HSM在**目标选择（Target Selection）和后验重排（Posterior Reranking）**两个阶段同时集成时效果最佳，平均Recall@1达到**30.1%**。仅在目标选择阶段集成（去除重排）或仅在重排阶段集成（去除目标选择），性能分别下降约2个百分点（Table 6），证明HSM在这两个关键环节均发挥不可替代的作用。

### 消融研究：多粒度损失组件

三项损失组件均对性能有正向贡献（Table 7）：
- **多粒度均匀性损失**（L_MGUNI）：帧间均匀性项防止批次内查询表示崩溃，帧内均匀性项保持单视频内帧级特征的多样性。
- **多粒度跨模态对齐损失**（L_MGCM）：全局对齐使批次查询与伪正例图库的模态差距逼近可靠记忆中的稳定目标，帧级对齐保持细粒度跨模态一致性。
- **噪声自适应熵最小化**（L_NA）：利用可靠记忆导出的自适应权重过滤不可靠样本，防止高熵噪声污染在线自适应。

同时使用全部组件达到最优（30.1%），移除任一项均导致性能下降，验证了多粒度监督信号的互补性。

### 失败模式分析

**低Hubness放大场景下训练组件收益有限**。当扰动类型不引起严重hubness放大时（如Temporal Scrambling、Backtranslation），TCR训练组件的收益微弱甚至产生负优化，而HSM本身提供主要增益。在Table 38中，去除训练组件后性能持平或略优（如33.4 vs 33.1），说明多粒度损失的设计主要面向hubness放大场景，在hubness不严重时其正则化可能引入不必要的约束。这揭示了一个关键局限：**方法缺乏根据在线检测到的hubness严重程度动态调整损失权重的机制**。

### Hubness抑制效果量化

HAT-VTR能显著降低hubness指标（Table 39）。以Gaussian噪声扰动为例，skewness从无TTA时的**9.09**降至HAT-VTR的**0.97**，接近无偏移的平衡分布。这从定量角度验证了HSM对hubness放大的直接抑制效果，且该效果与检索性能提升高度一致。

![[assets/figures/papers/iclr26_0012_FRkJ3ehpNN_Robust_Test-time_Video-Text_Retrieval_Benchmarki/figures/070_Table_39.jpg]]
*Table 39: Hubness analysis across challenging perturbation types for HAT-VTR. Skewness values indicate the degree of hubness amplification, with higher values representing more severe hubness issues*

### 效率分析

HAT-VTR的每查询推理延迟为**32.27ms**（RTX 4090，batch size=16），其中HSM模块仅占总运行时间的**13.0%**（4.2ms）（Table 8, Table 9）。考虑到其带来的显著性能增益，这一计算开销在实际部署中是可接受的。

### 稳定性与超参数敏感性

HAT-VTR在不同随机种子下表现稳定（Table 11）。HSM的超参数α和β在MSRVTT和ActivityNet上均表现出合理的鲁棒性（Table 12），所有实验采用固定值（α=100, β=10, m=0.5），未针对不同扰动单独调优，说明方法对超参数选择不敏感。

> **注意**：部分扰动（如Elastic Distortion）存在非单调的严重度表现（Figure 13），需要更精确的跨数据集严重度参数校准。部分扰动类型（Main Object Occlusion依赖Qwen2.5-VL、Style Transfer依赖AdaIN）严重依赖辅助模型，可能影响基准仿真真实世界视频退化的能力，相关结论需结合具体应用场景审慎解读。



## 定位与知识库关联

### 与现有TTA方法的关系

HAT-VTR 建立在测试时自适应（Test-Time Adaptation, TTA）的通用范式之上，但其设计逻辑与现有方法存在根本性差异。

**与熵最小化方法的对比。** TENT、SAR、EATA 等经典 TTA 方法的核心驱动信号是熵最小化——通过降低模型在目标域上的预测熵来适应分布偏移。然而，在视频-文本检索中，熵最小化本身并不足以应对查询偏移引发的 hubness 放大问题。如 Fig. 2(b-c) 所示，查询偏移使 k-occurrence 分布从平衡状态变为重尾分布，少数图库项成为支配性的“hub”，此时单纯降低预测熵反而可能强化这些 hub 的支配地位。HAT-VTR 保留了熵最小化作为自适应信号之一（$L_{NA}$），但通过噪声自适应权重 $S(\mathbf{p}_i) = \max(1 - \eta(\mathbf{p}_i)/E_m, 0)$ 过滤不可靠样本，防止误差累积。

**与 TCR 的直接继承与超越。** TCR 是首个面向图像-文本检索的 TTA 方法，通过表示均匀性损失处理查询偏移。HAT-VTR 在以下维度上继承并扩展了 TCR：
- *继承*：多粒度均匀性损失（$L_{MGUNI}$）和跨模态对齐损失（$L_{MGCM}$）沿用了 TCR 的表示均匀性思想，但将其从图像域扩展到视频域，增加了帧内均匀性项（$L_{intra}$）以保持时序特征的多样性。
- *超越*：HAT-VTR 引入了 TCR 所不具备的 Hubness Suppression Memory (HSM) 模块。HSM 直接在相似度空间进行双边重标定，通过公式 $\hat{S} = m (\bar{S} \odot W_{gallery}) + (1-m)(\bar{S} \odot W_{query})$ 降低热门图库项的支配性。实验表明，当 hubness 放大不严重时（如 Temporal Scrambling 或 Backtranslation），HSM 单独提供了主要增益，而 TCR 的训练组件收益微弱甚至产生负优化（Table 38：w.o. Training 在部分场景下取得 33.4 vs 33.1 的可比或更优结果）。这揭示了 HSM 与 TCR 式训练组件之间的功能互补性：HSM 直接抑制 hubness，而训练组件在 hubness 严重时进一步巩固表示质量。

**与图像域 TTA 方法的差异。** READ 等方法针对图像分类设计，其核心假设（如类别先验稳定）在视频-文本检索的跨模态匹配场景中不成立。视频检索的“类别”是动态的 query-gallery 对应关系，而非固定的分类标签，因此直接迁移图像域 TTA 方法效果有限。

### 适用边界

**有效场景。** HAT-VTR 在以下条件下表现出显著优势：
- **查询偏移引发严重 hubness 放大**：如 Gaussian 噪声、Impulse 噪声等低层像素扰动会显著放大 hubness（Table 39：Gaussian 场景下 skew 从 9.09 降至 0.97），此时 HSM 的双边重标定和多粒度损失的联合作用最为明显。
- **视频域时序特征可利用**：帧间/帧内均匀性损失依赖视频的时序层次结构，因此在视频-文本检索中比图像-文本检索方法（如 TCR）有额外增益。
- **在线流式设置**：HSM 仅需维护最近 K 个相似度矩阵的历史记忆，无需访问源数据或完整测试集，适合在线部署。

**效果减弱场景。** 以下条件下 HAT-VTR 的提升幅度有限：
- **hubness 放大程度低**：Temporal Scrambling 和 Backtranslation 等扰动不会显著改变 k-occurrence 分布，此时 HSM 的重标定效果减弱，TCR 训练组件甚至可能产生负优化（Table 38）。
- **非查询偏移的分布变化**：如果测试时变化主要影响图库侧而非查询侧，HSM 的图库中心权重计算可能引入偏差。论文未系统评估此类场景，需手动验证。

### 局限分析

**理论层面。** HAT-VTR 缺乏对不同扰动类型如何引起不同程度 hubness 放大的深层理论分析。Table 39 展示了不同扰动下的 skew 值差异（Gaussian 9.09 → 0.97，而 Temporal Scrambling 的 skew 变化较小），但未解释这种差异的因果机制。这阻碍了针对特定扰动类型设计更精细的自适应策略。

**架构层面。** Hubness 抑制仅用于后期重排（Posterior Reranking）和目标选择（Target Selection），未直接集成到梯度优化目标中。当前设计将 HSM 作为独立的后处理模块，与查询编码器的在线更新形成双路径并行架构（Fig. 4），但两条路径之间缺乏直接的梯度交互。这可能错失联合优化的潜力——如果 hubness 抑制信号能直接指导表示学习，或许能进一步提升鲁棒性。

**基准层面。** MLVP 基准存在以下局限：
- 部分扰动（如 Main Object Occlusion 依赖 Qwen2.5-VL、Style Transfer 依赖 AdaIN）严重依赖辅助模型，可能影响基准仿真真实世界视频退化的能力。
- 某些扰动（如 Elastic Distortion）存在非单调的严重度表现（Fig. 13），需要更精确的跨数据集严重度参数校准。

**计算效率。** HSM 模块占总运行时的 13.0%（4.2ms，Table 9），虽在可接受范围内，但在极端低延迟场景下仍需优化。整体每查询延迟为 32.27ms（Table 8），相比无 TTA 的基线有明显增加。

### 开放问题

1. **统一理论框架**：如何建立统一的理论框架，解释不同扰动类型与 hubness 放大之间的机制关系？当前仅通过 skew 等指标进行现象描述，缺乏从表示几何或信息论角度的深入分析。

2. **动态自适应机制**：能否设计动态自适应机制，根据在线检测到的 hubness 严重程度自动激活不同模块或调整损失权重？例如，在检测到低 hubness 时减少训练组件的权重，在高 hubness 时增强 HSM 的抑制强度。

3. **端到端 hubness 感知学习**：将 hubness 抑制直接整合进梯度优化目标是否可行？如何设计端到端的 hubness 感知学习损失，使得表示学习本身就能主动避免 hub 的形成？

4. **跨数据集严重度标定**：如何为多模态视频基准制定一套跨数据集泛化的严重度等级标定方法？当前 MLVP 的严重度参数在不同数据集间缺乏统一的校准标准。

5. **减少辅助模型依赖**：如何设计更贴近真实应用场景的视频检验扰动，减少对 Qwen2.5-VL、AdaIN 等辅助大模型的依赖？这直接影响基准的生态效度和可复现性。

6. **多骨干泛化验证**：虽然论文覆盖了 CLIP4Clip、X-Pool、CLIP-ViT-B/32、BLIP、LanguageBind 五个骨干，但在更近期的大规模视频-语言模型（如 Video-LLaMA、InternVideo2）上的表现尚待验证。



## 原文 PDF

![[paperPDFs/ICLR_2026/Robust_Test_time_Video_Text_Retrieval_Benchmarking_and_Adapting_for_Query_Shifts.pdf]]
