---
title: "Rethinking LLM Evaluation: Can We Evaluate LLMs with 200× Less Data?"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Rethinking_LLM_Evaluation_Can_We_Evaluate_LLMs_with_200_Less_Data.pdf
aliases:
- RLECWEL2LD
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "通过选择同时移除文本相似性和模型排名相似性的关键代表性子集，可以大幅度压缩基准规模，同时保持模型排序稳定性。"
primary_logic: "基准压缩应联合考虑语义重叠与跨模型行为一致性，采用粗到细的三阶段框架：先基于文本与排名冗余过滤近似重复样本，再利用遗传算法与固定代理模型选择分数重建最优子集，最后通过归因引导的分组细化提升覆盖度，从而在极高压缩比下维持评估可靠性。"
claims:
- "在HellaSwag的1万条样本中，EssenceBench仅用50条样本即实现了200倍压缩，且保持了95%的模型排名在5%的偏移范围内。"
- "在GSM8K上，子集大小k=500时，EssenceBench相对于MetaBench降低了60.7%的RMSE。"
- "在ARC和HellaSwag的全套指标上，EssenceBench在所有子集大小下均一致优于MetaBench，尤其在排名保真度（Kendall/Pearson）上达到接近完美的分数。"
- "HellaSwag (10,003 instances) 上 RMSE = 0.419 (k=500)"
---

# Rethinking LLM Evaluation: Can We Evaluate LLMs with 200× Less Data?

> [!tip] 核心洞察
> 基准压缩应联合考虑语义重叠与跨模型行为一致性，采用粗到细的三阶段框架：先基于文本与排名冗余过滤近似重复样本，再利用遗传算法与固定代理模型选择分数重建最优子集，最后通过归因引导的分组细化提升覆盖度，从而在极高压缩比下维持评估可靠性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 重新思考LLM评估：能否用200倍更少的数据评估LLM？ |
| 英文题名 | Rethinking LLM Evaluation: Can We Evaluate LLMs with 200× Less Data? |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=lZlZjSxdio); [GitHub](https://github.com/gszfwsb/EssenceBench); [Project](https://huggingface.co/datasets/open-llm-leaderboard-old/results) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | EssenceBench |
| Dataset | HellaSwag (10,003 instances), ARC, GSM8K, HellaSwag (ranking preservation) |

> [!tip] 效果简介
> - HellaSwag (10,003 instances) 上，RMSE 为 0.419 (k=500)，对比 0.836 (MetaBench, k=500)，变化 -49.9%。
> - ARC 上，Kendall correlation 为 0.983 (k=500)，对比 0.961 (MetaBench, k=500)，变化 +0.022。
> - GSM8K 上，RMSE 为 0.86 (k=200)，对比 0.96 (MetaBench, k=500)，变化 -0.10 (with 60% fewer samples)。

## 概述

当前大语言模型（LLM）的基准评估依赖大量人工标注或模型评分，评估成本高昂。研究发现，许多基准数据集中存在严重的文本相似性与模型排名冗余（Figure 1），大量样本仅提供了微弱的额外信息，却推高了计算开销。为此，本文将基准压缩形式化为一个子集优化问题：从原始数据集 $D$ 中选取 $k$ 个代表性样本，以最小化子集评分与全量评分之间的重建误差，同时保持模型排序的稳定性。

核心思路是联合考量语义重叠与跨模型行为一致性，以远少于原始数量的样本维持评估可靠性。基于此，文中提出 **EssenceBench**，一个粗到细的三阶段压缩框架（Figure 3）：
1. **粗过滤**：利用文本冗余（提示词嵌入的余弦相似度）和排名冗余（模型得分向量的 Pearson 相关系数）双信号，滤除近似重复的实例；
2. **子集搜索**：在过滤后的集合上，以固定代理模型（GAM）为评价器，通过遗传算法搜索使重建 RMSE 最小的 $k$ 样本子集；
3. **归因精炼**：借助可解释提升机（EBM）估计样本对精英子集的归因贡献，将样本划分为高/低/随机组，并在各组内再次运行遗传算法以提升覆盖度和多样性。

相较于先前方法（如 MetaBench 的单一文本过滤或 K‑means 聚类选择），EssenceBench 的核心差异在于同时消除文本与排名冗余、采用代理损失驱动的搜索，以及在紧凑预算下引入归因引导的多样性保持。

主要实验结果表明：
- 在 HellaSwag 上，仅需 **50 个样本**（约 200 倍压缩）即可保持 **95% 的模型排名在 5% 的偏移范围内**；
- 在 GSM8K 上，当 $k=500$ 时 EssenceBench 的 RMSE 为 0.419，比 MetaBench 的 0.836 降低 **49.9%**；甚至在 $k=200$ 时（RMSE 0.86）即已超过 MetaBench $k=500$ 的表现（RMSE 0.96）；
- 在 ARC 和 HellaSwag 的所有子集大小下，EssenceBench 在排名保真度（Kendall、Pearson 等）上均显著优于 MetaBench，例如 ARC 上 $k=500$ 时 Kendall 相关性达到 0.983 vs. 0.961；
- 消融实验证实，粗过滤对小子集尺寸至关重要，而归因引导的分组在数据预算紧张（$k < 400$）时明显优于随机选择。

综上，EssenceBench 能够在极大降低评估成本的同时，高度保持评分重建精度与模型排序稳定性，为高效 LLM 评估提供了可行方案。

## 背景与动机

大规模语言模型（LLM）的涌现能力使其在广泛任务上展现出令人瞩目的性能，然而，系统性地评估这些模型仍面临严峻的成本挑战。现有主流基准（如HellaSwag、GSM8K、ARC等）包含数万甚至数十万条测试样本，加之模型尺寸不断膨胀，导致全量评估的计算开销极高。更关键的是，这些基准数据集中普遍存在两类冗余——**文本冗余**（样本语义高度重叠）和**排名冗余**（不同样本的模型表现向量高度相关，即行为冗余），大量样本事实上无法提供额外的判别信息，造成了不必要的算力浪费（Figure 1，Definition 3 & 4）。

为缓解这一问题，已有若干基准压缩方法被提出，如TinyBenchmark、MetaBench等。这些方法试图通过文本层面的过滤或聚类筛选代表性样本，以降低评估成本。然而，它们大多存在以下共性缺口：(1) 仅侧重文本相似性或简单分层，未能**同步利用模型行为（排序）冗余**，小子集下排序保真度退化明显；(2) 压缩过程通常依赖启发式或一次性选择，难以在极高压缩比（如200×）下稳定重建全量基准的模型排序；(3) 压缩时间复杂度随基准规模线性增长，对于大型基准（如HellaSwag）的计算开销依然可观（Figure 2）。上述局限使得现有方法在面对严格的数据预算时（如k=50-200）容易出现排序反转或分数重构误差剧增。

针对上述瓶颈，本文提出**EssenceBench**，一个粗到细的三阶段基准压缩框架。其核心动机在于：通过**联合考虑语义重叠与跨模型行为一致性**，在剧烈压缩的同时保障模型评估的可靠性。EssenceBench 首先定义并同时滤除文本冗余和排名冗余，以去除近似重复样本；随后，利用固定代理模型与遗传算法搜索分数重建最优的子集，直接优化排序保真度；最后，通过归因引导的分组细化提升子集的多样性与覆盖度。这一设计从根本上改变了基准压缩的范式——不再单纯依赖文本去重，而是直接将“排名保真度”作为优化目标。在初步实验中，EssenceBench仅用50条样本（200倍压缩）即可保持HellaSwag上95%的模型排名在5%的偏移范围内，并且在GSM8K上以更少样本实现了较MetaBench降低60.7%的RMSE，这充分验证了该动机的有效性。

## 核心创新

现有基准压缩方法（如MetaBench、SMART）仅依赖文本相似度过滤或启发式子集选择，导致在极高压缩比下无法同时维持分数重建精度与模型排序保真度。根本瓶颈在于**没有联合考虑语义冗余与跨模型行为一致性**，因此在移除冗余样本时可能丢失对模型区分而言关键但语义差异大的样本。EssenceBench通过三个关键“变更槽”（changed slots）系统性地解决该问题，其粗到细的三阶段框架从冗余定义到搜索策略再到小预算多样性保持均进行了重新设计。

### 1. 冗余去除策略：从纯文本过滤到联合文本‑排名双冗余过滤
- **基线做法**：SMART等方法仅基于文本嵌入的余弦相似度识别近似重复样本，忽视了一对样本在语义上虽不重复但在模型能力刻画上高度一致的情形（即行为冗余）。
- **创新设计**：EssenceBench同时引入**文本冗余**（`Definition 3`，基于BGE-M3嵌入的平均余弦相似度）与**排名冗余**（`Definition 4`，两样本的模型得分向量的Pearson相关系数）。在粗过滤阶段（Step 1）用二元阈值 `τ_text` 和 `τ_ranking` 联合判定是否保留样本，只有当两者均未超过阈值时才保留该实例（`Eq. (7)` 形式的渐进过滤）。这使得不仅能去除语义重复，还能移除那些对模型排名贡献几乎相同的冗余样本，从而在后续小子集搜索中降低搜索空间噪声。
- **因果机制**：文本冗余过滤降低语义重叠带来的过采样偏差；排名冗余过滤则直接针对评估效用的重复性，确保压缩后的子集在模型行为空间上的代表性不会被人为冗余膨胀。消融实验（Figure 5(a)）显示，在小预算（k<400）下移除粗过滤会导致RMSE显著上升，表明该策略对于实现高压缩比是必要条件。
- **证据强度**：Figure 1 可视化了多个基准中存在的双重冗余现象，表明这一创新并非凭空假设；实验数据显示在GSM8K上，EssenceBench以k=200即超过MetaBench的k=500表现（RMSE 0.86 vs 0.96），部分归因于该冗余去除。

### 2. 子集选择机制：从启发式聚类到遗传算法+固定代理评估器
- **基线做法**：MetaBench等采用K‑means等聚类方法选取中心点作为代表子集，其选择过程未显式优化分数重建误差，对高度非线性的评分矩阵鲁棒性不足。
- **创新设计**：EssenceBench将基准压缩形式化为**掩码上的组合优化问题**（`Definition 2`），并在Stage 2 采用**遗传算法（GA）**搜索最优掩码 `m`。核心适应度函数为**负RMSE**（`Eq. (9)`），但直接计算需评估全部模型，计算不可行。为此，引入一个**固定代理预测器——广义可加模型（GAM）**，将子集准确率向量映射回全基准准确率预测，仅需在GA前训练一次；GA过程中适应度评估仅需通过GAM前向传播，避免重复实例化真实模型。
- **因果机制**：GA能够探索子集组合间的非线性交互，代理评估器解耦了搜索效率与评估成本，使得在有限计算资源下可执行大规模候选子集筛选，从而找到在分数重建上最优的 k 个样本。该方法克服了启发式方法无法保证全局最优的缺陷，尤其在高压缩比时，RMSE下降显著。
- **证据强度**：Table 1 显示 EssenceBench 在所有5个标准基准和所有子集大小（50~500）上RMSE均低于所有基线（Random, PPL, GraNd, MetaBench）。在HellaSwag上，MetaBench的RMSE为0.836（k=500），EssenceBench降至0.419（‑49.9%）。Table 6 和 Table 7 进一步表明在HellaSwag与ARC上排名保真度（Kendall τ, Pearson ρ）接近完美（如ARC上Kendall 0.983 vs 0.961），证明了GA搜索的有效性。

### 3. 小预算多样性保持：归因引导分组+组内遗传精炼
- **基线做法**：多数方法未专门处理极小k下的覆盖度问题，或采用简单分层；MetaBench等也无专门机制确保压缩子集涵盖多样化的样本类型。
- **创新设计**：EssenceBench在Stage 3引入**归因引导的分组精炼**（Attribution‑guided Refinement）。首先对若干GA得到的精英子集训练**可解释提升机（EBM）** 估计每个样本对预测性能的归因分数；接着将剩余样本按归因分数分为高贡献组（G_High）、低贡献组（G_Low）和随机组（G_Rand）（`Eq. (12)` 相关分组策略）。最后在各组内重新运行小规模遗传算法，从每组选取部分样本补充进子集，确保子集既包含对分数重建至关重要的高影响力样本，也覆盖低影响但维持分布多样性的样本，从而在极小子集下防止评估退化。
- **因果机制**：极小子集（如HellaSwag上的k=50）极易丢失一部分模型行为模式，导致排名偏移。归因分组通过显式按重要性分层采样，将搜索约束在可控区域，避免纯随机或均匀采样可能错失关键样本的风险。消融实验（Figure 5(c)）证实，数据预算紧张（k < 400）时，归因引导分组显著优于随机选择；且增加精炼轮次持续降低RMSE（如GSM8K上从2.77降至2.47）。
- **证据强度**：摘要中报道HellaSwag上只用50个样本（200×压缩）即可保持95%的模型排名在5%偏移内，这在小预算下若无该精炼机制难以实现。同时，Table 1/Table 2等结果表明EssenceBench在极小k（50/100）时仍大幅领先基线，间接验证了该设计的价值。

综上，EssenceBench的核心创新并非孤立模块，而是沿着“**粗过滤去冗余→全局优化重构建→局部归因补覆盖**”的粗到细链条，系统性地置换baseline的三个关键设计槽位，从而在高压缩比下同时达成分数重建误差最小化与排名保真度最大化。这一框架具有模块化可替换性：粗过滤阶段可与SMART等现有方法结合（Table 5显示替换后依然有效），遗传算法可适配不同代理模型，归因分组可灵活调整分组策略，体现出良好的可扩展性。

## 整体框架

![[assets/figures/papers/iclr26_0015_lZlZjSxdio_Rethinking_LLM_Evaluation_Can_We_Evaluate_LLMs_w/figures/009_Figure_3.jpg]]
*Figure 3: The pipeline of EssenceBench. (I) Coarse Filtering. By extracting the binary score matrix for each benchmark and computing both text-level and ranking-level redundancies, samples that exceed thresholds are removed. (II) Subset Selection. A genetic algorithm (GA) searches over subsets. Fitness is evaluated by the error of predicted performance, and subsets are optimized via tournament selection, crossover, mutation, and adjustment. (III) Sample Selection. Sample attributions are estimated from top-performing subsets and used to build candidate groups. GA is then reapplied within each group to identify the most representative and informative subset*

EssenceBench 采用一种**由粗到细的三阶段框架**，将 LLM 基准压缩形式化为一个在极度有限样本预算下同时重建分数与保持模型排名的子集优化问题。该框架的核心思路是：联合利用文本语义的冗余性与模型行为的一致性，先快速删除近似重复样本，再通过全局搜索找到分数重建最优的候选子集，最后借助归因引导的分组策略提升覆盖度，从而在 200 倍压缩下仍可保持评估可靠性。

### 框架总览与输入输出流

EssenceBench 的输入由两部分构成：①从公开排行榜提取的**二元评分矩阵**  $\mathbf{S} \in \{0,1\}^{N_{\mathrm{LLM}} \times M}$，记录每个模型在每个样本上的正确/错误信号；②原始样本的文本，经 BGE‑M3 嵌入后用于计算语义相似度。输出是一个大小为 $k$ 的代表性子集 $\tilde{\mathcal{D}}$，用于替代完整基准进行评估。整体流水线（图 Figure 3）依次经历三个关键模块：

1. **粗过滤（Coarse Filtering）**  
   基于**文本冗余**（样本嵌入对的余弦相似度）与**排名冗余**（样本上模型表现向量的 Pearson 相关性）双信号，按阈值 $\tau_{\text{text}}$ 和 $\tau_{\text{ranking}}$ 移除近似重复的样本，大幅降低后续优化空间的规模与噪声。这一阶段的本质是**廉价剪枝**，仅保留那些在语义和模型行为上都带来了增量信息的样本（$\S$ 3.2–3.3）。

2. **遗传算法子集选择（Subset Selection）**  
   将筛选后的评分矩阵送入一个**固定的代理评估器**——广义可加模型（GAM），该模型学会从子集准确率 $\mathbf{S}_{\mathrm{filtered}} \cdot \mathbf{m} / k$ 映射回完整基准的准确率向量 $\mathbf{y}$。然后，通过遗传算法（锦标赛选择、交叉、变异及调整算子）搜索二进制掩码 $\mathbf{m}$，以**负 RMSE** 作为适应度函数（Eq. (9)），迭代进化出 $k$ 个最能重建全基准分数的实例。这一阶段实现了**全局优化**的分数重建子集选择（$\S$ 3.3 Step 2，Algorithm 1）。

3. **归因引导的分组精炼（Attribution‑guided Refinement）**  
   为避免极度压缩下的覆盖盲区，框架在上一步得到的精英子集上训练可解释提升机（EBM），估计每个样本对预测准确率的**归因贡献**，并将候选集划分为高归因组（$G_{\text{High}}$）、低归因组（$G_{\text{Low}}$）和随机组（$G_{\text{Rand}}$）。随后在各组内再次运行遗传算法，确保最终子集既具备分数重建能力，又维持了语义与行为上的多样性（$\S$ 3.3 Step 3，Algorithm 2）。这一阶段相当于**局部纠偏**，使框架在极小预算下（$k<400$）依然显著优于随机选择或全量全局搜索（消融实验 Fig. 5）。

### 关键模块关系与设计动机

上述三阶段呈现出清晰的**粗粒度→精粒度**递进关系：粗过滤利用廉价的双冗余信号快速压缩候选空间，为后续昂贵的组合搜索提供干净输入；遗传算法在全局尺度上通过代理模型高效评估子集质量，避免每次搜索都重新运行 LLM；归因引导的分组再将全局最优解向高多样性和覆盖度方向微调。这一设计根植于对基准冗余现象的观察：大量样本在文本和模型排名上高度重叠（Fig. 1），且现有方法仅依赖文本相似性过滤（如 SMART）或聚类选择（如 MetaBench），未能同时兼顾行为冗余与极端压缩下的多样性保持。EssenceBench 通过联合建模文本与排名信号，并将代理模型与归因分组嵌入搜索循环，显著压缩了评估成本，同时保持了模型排序的稳定性。

## 核心模块与公式推导

EssenceBench 将基准压缩形式化为一个子集优化问题：从原始基准 $\mathcal{D}$（含 $N$ 个样本）中选出一个大小为 $k$ 的子集 $\tilde{\mathcal{D}}^*$，使得基于子集重建出的模型全基准得分与真实得分之间的差异最小。该目标可用二值掩码 $\mathbf{m}\in\{0,1\}^N$ 表达为

$$
\operatorname*{min}_{\mathbf{m}\in\{0,1\}^N}\; \mathcal{L}\bigl(\mathbf{y},\, g(\mathbf{S}_{\mathbf{m}})\bigr) \quad\mathrm{s.t.}\ \sum_{j=1}^{N} m_j = k,
$$

其中 $\mathbf{S}$ 是从公开排行榜抽取的二元评分矩阵（每个元素表示某模型在某样本上的正确与否），$\mathbf{y}$ 是各模型在全基准上的准确率向量，$g$ 是评分函数（通常为准确率聚合），$\mathcal{L}$ 为损失函数（实践取 RMSE）。该定义（见原文章定义 1 与 定义 2）将压缩转化为掩码选择问题，为后续搜索提供明确优化目标。

### 粗过滤：联合文本与排名冗余

大量基准样本在语义和模型行为上高度重复。EssenceBench 首先使用两类冗余信号剔除近似重复样本。

- **文本冗余**（原文定义 3）：样本对 $i,j$ 的文本冗余为提示词嵌入的余弦相似度

  $$
  \mathcal{R}_{\mathrm{text}}(i,j) = \langle \mathrm{Emb}(x_i), \mathrm{Emb}(x_j) \rangle,
  $$

  其中 $\mathrm{Emb}(\cdot)$ 由 BGE‑M3 等语义编码器生成。整个数据集的平均文本冗余则定义为

  $$
  \mathcal{R}_{\mathrm{text}}(\mathcal{D}) = \frac{1}{N}\sum_{i=1}^{N}\mathcal{R}_{\mathrm{text}}(i).
  $$

- **排名冗余**（原文定义 4）：两个样本在多个模型上的表现向量 $\mathbf{s}_i,\mathbf{s}_j$ 之间的皮尔逊相关系数

  $$
  \mathcal{R}_{\mathrm{rank}}(i,j) = \rho(\mathbf{s}_i,\mathbf{s}_j) = \frac{\mathrm{Cov}(\mathbf{s}_i,\mathbf{s}_j)}{\sigma_{\mathbf{s}_i}\sigma_{\mathbf{s}_j}}.
  $$

粗过滤按顺序扫描样本，仅当样本 $i$ 与所有先前保留的样本 $j$ 的文本冗余和排名冗余均低于各自阈值时才予以保留。保留指示符为

$$
\epsilon_i = \prod_{j=1}^{i-1} \mathbf{1}\bigl( \mathcal{R}_{\mathrm{text}}(j,i) \le \tau_{\mathrm{text}} \;\wedge\; \mathcal{R}_{\mathrm{rank}}(j,i) \le \tau_{\mathrm{rank}} \bigr).
$$

其中 $\tau_{\mathrm{text}}$ 和 $\tau_{\mathrm{rank}}$ 分别为文本冗余和排名冗余的阈值。该步骤以极低成本过滤掉过度冗余的样本，为后续搜索提供精简的候选池。

### 子集选择：遗传算法与代理模型

在过滤后的二值评分矩阵 $\mathbf{S}_{\mathrm{filtered}}$ 上，EssenceBench 通过遗传算法搜索使代理误差最小的 $k$ 样本子集。为避免在搜索过程中反复评估真实 LLM，框架预先训练一个广义可加模型（GAM）作为固定的代理评估器。对于掩码 $\mathbf{m}$ 定义的子集，该子集上的模型 $i$ 准确率定义为

$$
s_i(\mathbf{m}) = \frac{1}{k}\sum_{j=1}^{M} \mathbf{S}_{\mathrm{filtered}}[i,j] \cdot m_j,
$$

代理模型据此预测模型 $i$ 在全基准上的准确率 $\hat{y}_i = g(s_i(\mathbf{m}))$。遗传算法的适应度取验证模型集合 $\mathcal{V}$ 上的负 RMSE

$$
\mathrm{fitness}(\mathbf{m}) = - \sqrt{\frac{1}{|\mathcal{V}|}\sum_{i\in\mathcal{V}}\bigl(\hat{y}_i - y_i\bigr)^2},
$$

其中 $y_i$ 为真实全基准准确率。搜索过程采用锦标赛选择、交叉、变异和调整算子，迭代寻优使适应度最大的掩码，即恢复全基准排名能力最强的子集。

### 归因引导的精炼

当目标子集大小极度有限（$k<400$）时，单纯依靠全局遗传算法容易遗漏部分能力维度。EssenceBench 引入归因引导的分组精炼步骤：先用可解释提升机（EBM）估计已得到精英子集中每个样本对重建误差的归因贡献，然后根据归因分数将过滤后的全体样本划分为高归因组 $G_{\mathrm{High}}$、低归因组 $G_{\mathrm{Low}}$ 和随机组 $G_{\mathrm{Rand}}$。各组内部再独立执行上述遗传算法，最终合并各组最优解。该策略在保证分数重建精度的同时，显著提升了子集的语义多样性和能力覆盖度，且未引入额外评估开销。

## 实验与分析

实验部分围绕两个核心问题展开：(i) EssenceBench在各种基准和子集预算下能否在分数重建和排名保真度上超越现有压缩方法；(ii) 粗过滤、遗传算法搜索与归因引导等各模块的实际贡献如何。所有实验均遵循MetaBench的预处理协议，采用基于模型性能分层的9:1训练/测试划分，并复用相同的公开排行榜评分矩阵，保证对比的公平性（各方法均使用相同的模型表现信号）。

### 主结果：分数重建与排名保真度

在5个标准基准（GSM8K、ARC、HellaSwag、WinoGrande、MMLU）上，EssenceBench在所有子集大小下一致实现了最低的RMSE（Table 1）。尤其在极小子集预算下，优势更加突出：在GSM8K上，仅需200条样本，EssenceBench的RMSE降至0.86，而MetaBench在500条样本下仍为0.96；在WinoGrande上，200条样本的RMSE（0.78）已媲美MetaBench 500条样本的水平（0.79）。这一现象源于联合去除文本与排名冗余的粗过滤步骤，它在预算受限时剔除了大量语义和行为上近似重复的样本，为后续搜索保留了更高质量的基础集。

![[assets/figures/papers/iclr26_0015_lZlZjSxdio_Rethinking_LLM_Evaluation_Can_We_Evaluate_LLMs_w/figures/010_Table_1.jpg]]
*Table 1: Prediction error (RMSE ↓) on 5 standard benchmarks using subset size N $\in {50, 100, . . . , 500}$. EssenceBench achieves lower error than all baselines across subset sizes*

在8个更具挑战性的基准（如MathVista、GPQA、IFEval等）上，EssenceBench同样表现出最低的RMSE（Table 2）。尤其是在MathVista上，300条样本即实现了近乎无损的分数重建（RMSE = 0.001），表明该方法在需要细粒度推理或多模态能力的评估场景中仍然有效。

![[assets/figures/papers/iclr26_0015_lZlZjSxdio_Rethinking_LLM_Evaluation_Can_We_Evaluate_LLMs_w/figures/011_Table_2.jpg]]
*Table 2: Prediction error (RMSE ↓) on 8 more challenging benchmarks using subset size k $\in {50, 150, 300}$2. EssenceBench yields the lowest error across diverse evaluation settings*

排名保真度是衡量压缩子集能否可靠反映模型排序的重要指标。Table 3显示，在GSM8K上，EssenceBench仅需150条样本便达到完美的Pearson和Kendall相关系数（1.000与0.999），而MetaBench需要400条以上才能接近同等水平。在ARC上，k=500时EssenceBench的Kendall相关性达到0.983，MetaBench为0.961（Table 7）。HellaSwag上，k=500时EssenceBench的RMSE降至0.419，仅为MetaBench（0.836）的一半（49.9%降幅），且排名误差（Top‑50 Acc、Rank Err within 10%）全面占优（Table 6）。最具极端压缩场景下，仅使用50条样本（200×压缩），EssenceBench仍能使95%的模型排名偏移控制在5%以内（排名变化分布见图4）。这一能力直接源自遗传算法以RMSE最小化为目标的全局搜索，以及归因引导对多样性的保障——这两个机制共同防止了少数高区分度样本的意外丢失。

![[assets/figures/papers/iclr26_0015_lZlZjSxdio_Rethinking_LLM_Evaluation_Can_We_Evaluate_LLMs_w/figures/015_Table_3.jpg]]
*Table 3: Ranking Fidelity on GSM8K. EssenceBench achieves superior correlation by fewer samples*

![[assets/figures/papers/iclr26_0015_lZlZjSxdio_Rethinking_LLM_Evaluation_Can_We_Evaluate_LLMs_w/figures/021_Table_6.jpg]]
*Table 6: Full Results on HellaSwag. Comparison of MetaBench vs. EssenceBench across all metrics. Highlighted rows indicate our method*

### 消融分析：各模块的因果贡献

利用GSM8K进行消融实验，结果汇总于Figure 5与Table 4、Table 5。

![[assets/figures/papers/iclr26_0015_lZlZjSxdio_Rethinking_LLM_Evaluation_Can_We_Evaluate_LLMs_w/figures/018_Figure_5.jpg]]
*Figure 5: Ablation results on GSM8K, evaluating the effect of (a) coarse filtering, (b) attributionbased selection, and (c) grouping strategies*

**粗过滤的必要性。** 移除粗过滤步骤后，尤其在小k值下RMSE显著上升（Figure 5a）。原因是冗余样本在小子集中占据宝贵配额，挤掉真正有信息量的实例；联合文本冗余（嵌入余弦相似度）和排名冗余（模型表现向量的Pearson相关）的双信号过滤，比单一文本去重（如SMART）更能提升后继搜索的质量。Table 5进一步证明，若将粗过滤替换为SMART，MMLU上的RMSE在k=500时由EssenceBench的0.12升至0.90，说明仅靠文本多样性不足以保证评估有效性。

**遗传算法搜索与代理评估的作用。** 与K‑means和MLP等优化基线相比，EssenceBench的遗传算法在GSM8K上（k=400）的RMSE仅为0.454，远低于K‑means的2.757和MLP的1.573（Table 4左）。这是因为固定代理预测器（GAM）提供了快速而可靠的适应度评估，使搜索过程能够直接朝着全基准准确率的最小RMSE方向优化，从而绕过了直接运行LLM进行在线评估的巨大计算开销。

**归因引导分组的有效性。** 当数据预算紧张（k<400）时，基于EBM归因的样本分组（高贡献、低贡献、随机）后再运行GA，明显优于对全体样本直接运行GA或随机选择（Figure 5c）。该策略确保了代表性子集不仅分数重建准确，还在语义与难度层面具有足够的覆盖度。同时，增加精炼轮次持续降低RMSE（例如从2.77降至2.47），说明群体迭代有助于跳出局部最优，进一步提升子集质量。

**超参数敏感性。** 对τ_text和τ_ranking的网格搜索表明，方法对这些阈值的敏感性较低：在GSM8K上，RMSE变化范围仅为2.56–2.80（Table 8），说明粗过滤阶段不需要精细调参即可稳定工作。

### 失败模式与局限性讨论

论文未专门章节讨论失败模式或局限性，但由消融实验可推断两类潜在风险：第一，当子集大小k极低（例如k<20）时，粗过滤和归因引导虽能缓解信息损失，但分数重建误差可能急剧上升，导致排名保真度退化；第二，对于主题分布高度偏斜且语义多样性与模型行为解耦的基准（如某些数学推理测试），仅依赖粗过滤和拟合代理模型可能无法充分捕获长尾实例，需要更为先验的领域分组策略。这些猜测尚无定量验证，有待未来工作探索。

### 关键图表证据总结

- **Figure 1**（冗余现象）：量化展示了HellaSwag等基准上高文本和排名冗余（相似度均超过0.7），为200倍压缩提供了数据基础。
- **Table 1、Table 2**（主结果）：跨越13个基准的RMSE对比，EssenceBench全面且一致地超越Random、PPL、GraNd、MetaBench等基线，尤其在困难基准上优势扩大。
- **Table 3**（排名保真度）：GSM8K上EssenceBench以更少样本实现更高的Pearson/Kendall/排名误差指标，证明压缩不会牺牲相对排序。
- **Figure 5**（消融）：粗过滤、归因选择和分组策略各自对性能的独立增益可视化，揭示了“筛选‑搜索‑精炼”三阶段的因果必要性。
- **Table 6、Table 7**（附录全指标）：HellaSwag和ARC上跨k值的全部五项指标对比进一步夯实EssenceBench的鲁棒性与泛化能力。

## 方法谱系与知识库定位

EssenceBench处于LLM基准压缩方法谱系中一个关键转折点：它将前人工作普遍采用的“单一冗余信号+启发式选择”范式，推进到“文本‑排名联合冗余感知+代理引导搜索+归因驱动精炼”的粗到细框架。理解这一谱系位置及其适用边界、内在局限和开放问题，有助于判断该方法何时可用、何时需要替代方案，以及未来可能的演进方向。

### 与基线及后续工作的关系

在EssenceBench之前，基准压缩主要沿两条线索发展。其一是**冗余过滤**，例如SMART（Gupta et al., 2025）仅基于文本相似性移除近似重复样本，但忽略了跨模型行为的一致性，导致排名破坏性样本被错误保留。其二是**聚类或统计选取**，TinyBenchmark（Polo et al., 2024）和MetaBench（Kipnis et al., 2025）分别采用IRR和K‑means聚类选择代表性样本，但这些方法未能显式优化分数重建误差，在受限数据预算下排名保真度不足。EssenceBench针对上述瓶颈进行了三处关键修改（见方法 §3.2‑3.3）：

1. **冗余建模从“文本”扩展为“文本+排名”**：定义双阈值过滤，同时考虑语义重叠（Definition 3: $\mathcal{R}_{\mathrm{text}}$）与模型行为一致性（Definition 4: $\mathcal{R}_{\mathrm{rank}}$）。实验表明，这一粗过滤对小子集尺寸至关重要，移除冗余可使质量显著提升（Figure 5(a)）。
2. **子集选择从“启发式”转变为“代理引导的遗传算法”**：替代MetaBench的K‑means，采用GA以负RMSE为适应度在解空间中搜索，并固定GAM作为代理评估器（Algorithm 1）。这直接对齐压缩目标（Definition 2: $\operatorname*{min}_{\mathbf{m}}\mathcal{L}(\mathbf{y}, g(\mathbf{S_m}))$），使分数重建误差系统性地降低（例如GSM8K上k=500时RMSE 0.86 vs. MetaBench 0.96）。
3. **多样性保真从“全或无”进化为“归因分组”**：在数据预算紧张（k<400）时，纯GA容易陷入局部多样性的缺失。EssenceBench利用EBM估计样本归因贡献，构建高/低/随机三组，再分组运行GA精炼（Step 3, Algorithm 2）。这一归因引导的分组策略在消融中展现出明显优势（Figure 5(c)）。

从知识库定位看，EssenceBench并非后处理式的子集筛选，而是**联合优化分数重建与排名保真**的主动压缩范式。它统一了过滤、搜索与覆盖度增强，使得压缩比高达200倍的极端情况下仍能维持95%的模型排名在5%偏移内（HellaSwag, k=50）。与同期或后续方法相比，它不是简单的模块堆叠，而是将评估可靠性的信息瓶颈从样本数量转移到了冗余消除与代理模型的质量上。

### 适用边界

EssenceBench的设计隐含若干工作假设，决定了其生效的前提条件：

- **可用排行榜数据**：压缩依赖于从公开排行榜提取的二值评分矩阵 $\mathbf{S}\in\{0,1\}^{N_{\mathrm{LLM}}\times M}$（Definition 2）。因此，该方法适用于已积累大量模型评估记录的成熟基准（如GSM8K、HellaSwag、ARC），对于新发布或模型评估数据稀疏的基准，构建 $\mathbf{S}$ 的前提不具备。
- **二值正确性信号**：框架目前仅处理正确/错误的评分模式。实验所用基准（数学推理、常识问答、多任务语言理解）均为选择或短答案形式，天然适合二值化。对于开放式生成或需要BLEU/ROUGE等连续评分的任务，代理模型和RMSE需要重新设计，否则泛化受限。
- **待评估模型与训练模型分布相近**：压缩过程中GAM和GA均基于分层9:1划分的模型训练集，因此压缩子集的质量在隐式绑定于训练模型的行为模式上。虽然留出模型测试表现仍优异（Table 1‑2），但若新模型架构或训练范式产生截然不同的错误分布，排名重建误差可能升高——这一点尚缺乏极端分布外（OOD）的专项测试。
- **基准规模与压缩比**：EssenceBench在中高压缩比（k ≤ 500）且原始基准规模中等（≈10k样本）时效益最显著。当k本身极大（如接近全量），或基准中冗余度极低时，粗过滤和GA搜索的边际收益会递减。MMLU实验显示，即使在2000子集下仍保留了良好的主题分布（偏差比<2%，Table 15），但压缩比相比小基准有所下降。

值得注意的是，粗过滤和归因分组在k<400时增益最大，意味着EssenceBench特别适用于“**严苛数据预算下的核心评估**”场景，而非追求全量复制的一切万灵药。

### 局限与开放问题

尽管EssenceBench在多项指标上一致超越MetaBench等基线，但方法及评估仍有以下内在局限和待探索的前沿：

**内在限制**

- **代理模型的偏差放大**：子集搜索的适应度完全由固定的GAM提供。若GAM未能捕获非线性交互或对某些模型估计偏差较大，GA可能选出偏好这些模型的子集，引入系统误差。文中虽对比了K‑means和MLP替代方案（Table 4），但并未探讨GAM本身的容量瓶颈。
- **遗传算法的随机性与开销**：EA搜索是随机化的非凸优化，依赖于锦标赛选择、交叉、变异等算子。虽然搜索开销远小于完整评估（加速比最高49×，Table 16），但对于超大规模基准（如MMLU），GA迭代仍需要一定的计算预算，且存在次优收敛的风险。超参数（种群大小、精炼轮次）的敏感性仅在部分消融中验证（Figure 5, RMSE随轮次下降），跨基准的调参普适性尚未系统阐述。
- **文本嵌入与语义多样性的表征**：文本冗余过滤使用BGE‑M3提取嵌入，多样性评分 $\mathcal{D}$（Eq. 13）衡量平均成对余弦相似度。该方法对表面语义敏感，可能误判形式不同但语义等价的提示为“多样性高”，或漏掉基于知识粒度的冗余。此外，多样性仅由嵌入距离来体现，未考虑难度、推理链长度等影响评估质量的因素。
- **二值评估框架的单一性**：限于准确率评估，无法直接评估模型在生成质量、校准、不确定性等其他维度的表现。对于需要细粒度打分或多维度评测的场景，压缩目标需重新定义。

**开放问题**

1. **动态评估与增量压缩**：当新模型持续上线时，静态压缩子集会逐渐过时。能否设计轻量的增量更新机制，在新增少量模型评分后微调子集，而非重新运行整个GA流程？这涉及子集的可持续维护问题。
2. **跨模态与多语言基准的压缩**：当前实验全部基于英文NLP基准。多模态或多语言基准的冗余模式显著不同（例如图像相似性与语言重叠），EssenceBench的粗过滤和代理模型能否直接迁移，仍需实证。
3. **模型分布偏移的鲁棒性**：论文在训练/测试划分中采用了分层抽样，但同基准内不同模型族的偏移是渐进的。若未来模型通过RLHF等方式从根本上改变了错误模式，压缩子集的泛化上界在哪里？是否需要引入不确定性量化，而非仅仅点估计RMSE？
4. **个性化样本选择**：目前所有模型共享同一压缩子集。一个可能的延伸是根据待评估模型的个体作答模式（例如在线学习其错误分布）自适应选择样本，用更少的样本实现个体化排名精度的提升。
5. **隐私与去中心化数据**：公开排行榜假设了所有模型对同一基准的完整评分矩阵可获取。当模型评估结果因隐私或商业原因不能公开时，如何在不集中收集数据的前提下实现基准压缩（例如联邦学习或差分隐私框架），是落地应用的关键挑战。

上述局限与开放问题的部分论断需要人工进一步核实，因为论文未在局限或未来工作中明确展开讨论。它们主要源于对方法假设的严格审视以及实验未覆盖的边缘情况推断。在实际部署决策时，建议结合具体任务的数据特性、允许的评估误差容限以及可获取的模型评估数据规模，审慎评估EssenceBench的适用性。

## 原文 PDF

![[paperPDFs/ICLR_2026/Rethinking_LLM_Evaluation_Can_We_Evaluate_LLMs_with_200_Less_Data.pdf]]
