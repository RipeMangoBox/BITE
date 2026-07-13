---
title: "SCoRe: Salience-Coverage Reduction for Vision Token Pruning in Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SCoRe_Salience_Coverage_Reduction_for_Vision_Token_Pruning_in_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- SSCR
- SCoRe
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将令牌剪枝从解耦启发式策略转变为统一的代表性优化框架，通过单一步骤同时优化令牌的显著性(salience)与语义覆盖度(coverage)，从而从根源上避免采样坍缩。
primary_logic: 视觉令牌在语义空间中形成离散聚类，理想的剪枝需确保全局聚类覆盖，同时优先保留高显著性区域。SCoRe将其建模为加权k-中心问题，通过贪婪算法在每一步选取最大化“到已选集最小余弦距离 × 显著性^α”的令牌，实现全局代表性与显著性优先级的内在统一。
claims:
- SCoRe在94.4%剪枝率下仍保持95%基准性能，优于SparseVLM (77.9%)和VisPruner (91.5%)。
- UMAP可视化显示SCoRe选择的令牌覆盖度远高于Top-k策略，有效避免采样坍缩。
- 剪枝问题在理论上等价于经典的加权k-中心问题，为算法提供了坚实的形式化基础。
- 消融实验证明，平衡显著性与覆盖度的完整方法显著优于纯多样性（α=0）或纯显著性（α→∞）。
---

# SCoRe: Salience-Coverage Reduction for Vision Token Pruning in Vision-Language Models

> [!tip] 核心洞察
> 视觉令牌在语义空间中形成离散聚类，理想的剪枝需确保全局聚类覆盖，同时优先保留高显著性区域。SCoRe将其建模为加权k-中心问题，通过贪婪算法在每一步选取最大化“到已选集最小余弦距离 × 显著性^α”的令牌，实现全局代表性与显著性优先级的内在统一。

| 字段 | 内容 |
|------|------|
| 中文题名 | SCoRe: 面向视觉语言模型视觉令牌剪枝的显著性-覆盖度约简 |
| 英文题名 | SCoRe: Salience-Coverage Reduction for Vision Token Pruning in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_SCoRe_Salience-Coverage_Reduction_for_Vision_Token_Pruning_in_Vision-Language_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SCoRe (Salience-Coverage Reduction) |
| Dataset | 10 LVLM benchmarks, LLaVA-1.5-7B average over 10 benchmarks, LLaVA-NeXT-7B average over benchmarks |

> [!tip] 效果简介
> - 10 LVLM benchmarks (LLaVA-1.5-7B, 32 tokens, 94.4% pruning) 上，Relative Performance (%) 95.0 vs 91.5 (VisPruner, best competitor) (+3.5)。
> - LLaVA-1.5-7B average over 10 benchmarks (128 tokens, 77.8% pruning) 上，Relative Performance (%) 100.6 vs 100 (original full tokens) (+0.6)。
> - LLaVA-NeXT-7B average over benchmarks (32 tokens, 94.4% pruning) 上，Relative Performance (%) 93.4 vs 100 (original) (-6.6)。

## 概要

**核心瓶颈。** 视觉语言模型（VLM）在推理时需处理来自视觉编码器的大量视觉令牌，导致Transformer自注意力机制产生 $O(L^2)$ 的计算复杂度，成为大规模部署的关键效率瓶颈。以LLaVA-1.5为例，单张图像可产生576个视觉令牌，其计算开销随序列长度呈平方增长。

**核心洞察。** 视觉令牌在语义空间中天然形成离散聚类——不同聚类对应图像的不同语义区域。理想的令牌剪枝应同时满足两个条件：确保所选子集对全局聚类的**覆盖度**（避免采样坍缩），以及优先保留来自高**显著性**区域（如文本、关键物体）的令牌。现有方法普遍采用解耦的两阶段策略——先按显著性Top-k选取，再通过聚类或合并补偿多样性——缺乏统一的优化目标，难以从根本上协调两者。

**方法定位。** SCoRe（Salience-Coverage Reduction）将视觉令牌剪枝重新定义为**统一代表性优化问题**，形式化等价于经典的**加权k-中心问题**（Weighted k-Center）。其核心创新在于通过单一步骤的贪婪算法，在每一步选择最大化“到已选集最小余弦距离 × 显著性^α”复合分数的令牌，实现覆盖度与显著性的内在统一。SCoRe是训练无关的即插即用模块，置于视觉编码器与模态投影器之间，无需任何微调。

**主要结果。** 在LLaVA-1.5-7B上，SCoRe以仅保留32个令牌（剪枝率94.4%）达到基线性能的95%，显著优于SparseVLM（77.9%）和VisPruner（91.5%）。当保留128个令牌（剪枝率77.8%）时，SCoRe在10个基准上的平均相对性能达到100.6%，甚至略超原始全令牌基线。在LLaVA-NeXT-7B和Qwen-VL-7B上的跨架构实验进一步验证了方法的通用性。消融实验证实，平衡覆盖度与显著性的完整方法显著优于纯多样性（α=0）或纯显著性（α→∞）的极端策略。

### 视觉语言模型的推理效率瓶颈

大规模视觉语言模型（LVLM）的核心推理瓶颈在于视觉令牌序列过长。视觉编码器（如ViT）通常将每张图像编码为数百个令牌（例如LLaVA-1.5生成576个令牌），这些令牌与文本令牌拼接后输入LLM解码器。由于Transformer自注意力机制的计算复杂度与序列长度的平方成正比（O(L²)），大量视觉令牌导致推理延迟和显存占用急剧上升，严重制约了LVLM的实际部署效率。

现有应对策略可归为两条技术路径：**令牌剪枝**和**令牌合并**。令牌剪枝直接丢弃冗余令牌以缩减序列长度，令牌合并则将相似令牌逐步聚合。然而，主流剪枝方法普遍采用**解耦启发式策略**——先通过某种显著性指标（如[CLS]注意力分数）进行Top-k选择，再通过聚类或合并操作补偿多样性损失。这种两阶段设计缺乏统一的优化目标，导致两个根本性问题：

1. **采样坍缩**：纯Top-k选择倾向于集中在少数高显著性区域，遗漏语义空间中其他聚类的重要信息，造成信息覆盖度不足。
2. **优化割裂**：显著性与覆盖度的平衡依赖人工设计的后处理步骤，无法从全局最优的角度保证所选令牌的代表性。

### 现有方法的缺口

以三组代表性工作为例：

- **SparseVLM**（Zhang et al., 2024）利用LLM内部的跨模态注意力分数筛选令牌，但仅关注显著性，缺乏对语义覆盖度的显式建模。
- **VisPruner**（Zhang et al., CVPR 2025）引入视觉线索辅助剪枝，但仍采用先显著性选择后多样性补偿的解耦流程。
- **VisionZip**（Yang et al., 2024）和**ToMe**（Bolya et al., 2022）分别采用基于[CLS]注意力的混合策略和逐步合并策略，同样未将剪枝建模为统一的优化问题。

这些方法的共同缺陷在于：**缺乏对“代表性”的形式化定义**。理想的剪枝应确保所选令牌子集能够代表原始令牌全集在语义空间中的分布，同时优先保留高显著性区域。这一目标无法通过解耦启发式实现，需要从优化层面进行统一建模。

### 本文动机与核心思路

SCoRe的动机源于一个关键观察：视觉令牌在语义空间中形成离散聚类（如Figure 2(a)所示），理想的剪枝需确保全局聚类覆盖，同时优先保留高显著性区域。这本质上是一个**代表性优化问题**——从原始令牌集合中选择一个大小为k的子集，使得所有令牌到该子集的最大加权距离最小化。

SCoRe将这一问题形式化为**加权k-中心问题**，并通过贪婪算法在每一步选取最大化“到已选集的最小余弦距离 × 显著性^α”的令牌。这一设计实现了三个关键突破：

- **统一优化**：将显著性与覆盖度耦合为单一复合分数，避免了解耦策略的次优性。
- **即插即用**：SCoRe作为训练无关模块，放置于视觉编码器与模态投影器之间，无需任何微调即可适配不同VLM架构。
- **理论支撑**：剪枝问题与加权k-中心问题的形式等价性（Eq. 3）为算法提供了坚实的理论基础。

Figure 1的雷达图直观展示了SCoRe的动机验证：在94.4%剪枝率（仅保留32个令牌）下，SCoRe（红色区域）在十个LVLM基准上的性能面积显著大于SparseVLM（77.9%相对性能）和VisPruner（91.5%相对性能），证明了统一代表性优化的有效性。

## 核心方法与创新机理

### 问题瓶颈：视觉令牌冗余与采样坍缩

视觉语言模型（VLM）的推理效率瓶颈源于视觉编码器产生的大量视觉令牌序列，其自注意力计算复杂度为 $O(L^2)$，严重制约大规模部署。现有剪枝方法普遍采用**两阶段解耦启发式策略**：先通过Top‑k选择高显著性令牌，再借助聚类或合并补偿多样性。这种“先选后补”的范式存在结构性缺陷——显著性选择与覆盖度补偿相互独立，缺乏统一的优化目标，容易导致**采样坍缩**（sampling collapse），即保留的令牌高度集中在少数显著性区域，丢失全局语义信息。

### 核心洞察：从解耦启发式到统一代表性优化

SCoRe 的根本创新在于将视觉令牌剪枝从工程化的两阶段策略**重新定义为统一的代表性优化问题**。其核心洞察是：视觉令牌在语义空间中天然形成离散聚类，理想的剪枝必须同时满足两个条件——（1）**全局聚类覆盖**，确保每个语义聚类至少有一个代表令牌被保留；（2）**显著性优先级**，在覆盖约束下优先保留对下游任务更关键的高显著性令牌。

SCoRe 将这一直觉形式化为**加权k‑中心问题**（Weighted k‑Center Problem），目标函数为：

$$S^{*} = \operatorname*{argmin}_{S \subset V, |S| = k} \left( \max_{v_i \in V} \left( w_i \cdot d(v_i, S) \right) \right)$$

其中 $w_i$ 为令牌 $v_i$ 的显著性权重，$d(v_i, S)$ 为令牌到已选子集的最小距离。该目标最小化所有令牌的最大加权距离，本质上要求所选子集在语义空间中对全体令牌形成“覆盖”，且高权重令牌获得更严格的覆盖精度。

### 关键机制：单步统一选择

基于上述形式化，SCoRe 设计了**单一步骤的贪婪选择算法**，在每轮迭代中直接基于统一的复合分数选取令牌：

$$s_t = \operatorname*{argmax}_{v_i \in V \setminus S_{t-1}} \left( d_{\cos}(v_i, S_{t-1}) \cdot (\operatorname{score}(v_i))^{\alpha} \right)$$

该公式将**覆盖度**（当前令牌到已选集的最小余弦距离）与**显著性**（经超参数 $\alpha$ 调节的注意力分数）融合为单一乘积项，一步完成选择。$\alpha$ 控制两者的平衡：$\alpha=0$ 退化为纯多样性策略，$\alpha \to \infty$ 退化为纯Top‑k显著性策略。这种设计从根源上避免了“先选显著性再补多样性”带来的次优性和采样坍缩。

### 架构创新：训练无关的即插即用设计

SCoRe 作为**训练无关**模块，被置于视觉编码器与模态投影器之间，无需任何微调即可集成到现有VLM流水线中。其显著性权重直接复用视觉编码器的[CLS]注意力分数，无需额外训练或引入可学习参数。这一设计使其与FlashAttention等高效注意力实现完全兼容，且计算开销极低（仅涉及余弦距离计算与排序），在保持模型原有能力的同时实现即插即用的推理加速。

### 与基线方法的本质差异

| 方法 | 剪枝策略 | 优化目标 | 集成位置 |
|------|----------|----------|----------|
| **SparseVLM** (Zhang et al., 2024) | 基于LLM内部注意力的两阶段选择 | 无显式全局优化目标 | LLM内部 |
| **VisPruner** (Zhang et al., CVPR 2025) | 利用视觉线索的解耦启发式 | 无显式全局优化目标 | 视觉编码器内部 |
| **FastV** (Chen et al., 2024) | 基于LLM早期层跨模态注意力的剪枝 | 无显式全局优化目标 | LLM内部 |
| **ToMe** (Bolya et al., 2022) | 逐步合并相似令牌 | 最小化合并损失（局部贪心） | Transformer层间 |
| **SCoRe** | **单步统一代表性优化** | **最小化最大加权距离（加权k‑中心）** | **视觉编码器与投影器之间** |

SCoRe 是首个将覆盖度与显著性统一到单一优化框架中的方法，其理论基础（加权k‑中心）为算法提供了坚实的形式化保证，而贪婪实现则在理论优雅性与计算效率之间取得了实际可用的平衡。

SCoRe 采用**即插即用**的模块化设计，放置于视觉编码器与模态投影器之间，无需任何额外训练或微调。其整体流水线由四个模块串联构成：

1. **Vision Encoder（视觉编码器）**：接收输入图像，提取视觉令牌特征 $\{v_1, v_2, \dots, v_N\}$ 以及 `[CLS]` 令牌对应的自注意力权重，作为后续显著性评分的依据。
2. **SCoRe Module（SCoRe 剪枝模块）**：这是方法的核心。它接收完整的视觉令牌集合，通过统一的代表性优化算法，迭代选取 $k$ 个代表性令牌。每一步选择最大化“到已选集的最小余弦距离 $\times$ 显著性$^\alpha$”的令牌，从而在单一复合分数中同时优化语义覆盖度与显著性优先级。
3. **Modality Projector（模态投影器）**：将 SCoRe 保留的 $k$ 个视觉令牌投影到与大语言模型对齐的文本语义空间。
4. **LLM Decoder（大语言模型解码器）**：接收由投影后的视觉令牌与文本令牌拼接而成的多模态序列，生成最终回答。

这一设计的关键在于**剪枝发生在跨模态融合之前**：SCoRe 在视觉编码器输出端即完成令牌筛选，使得后续的投影器和 LLM 仅需处理极少量令牌。这不仅从根源上削减了 Transformer 自注意力机制的 $O(L^2)$ 计算复杂度，还天然兼容 FlashAttention 等高效注意力实现，因为剪枝后的序列长度已大幅缩短。

### 问题形式化：从剪枝到代表性优化

SCoRe 将视觉令牌剪枝形式化为一个**代表性优化问题**（Representativeness Optimization Problem）。给定原始视觉令牌集合 $V = \{v_1, v_2, \ldots, v_n\}$，每个令牌 $v_i$ 携带一个显著性权重 $w_i$，目标是选取一个大小为 $k$ 的子集 $S \subset V$，使其对全集 $V$ 的代表性损失最小化：

$$S^{*} = \operatorname*{argmin}_{S \subset V, |S| = k} \mathcal{R}(S, V)$$

其中代表性损失 $\mathcal{R}(S, V)$ 定义为所有令牌到已选子集 $S$ 的最大加权距离：

$$\mathcal{R}(S, V) = \max_{v_i \in V} \left( w_i \cdot d(v_i, S) \right)$$

这里 $d(v_i, S) = \min_{s \in S} d(v_i, s)$ 表示令牌 $v_i$ 到子集 $S$ 中最近代表点的距离。该目标的核心直觉是：**任何一个高显著性令牌若远离所有已选代表点，都会对代表性损失产生惩罚**，从而迫使算法在覆盖全局聚类的同时优先照顾重要区域。

### 理论等价性：加权 k-中心问题

上述优化目标在形式上与经典的**加权 k-中心问题**（Weighted k-Center Problem）完全等价：

$$S^{*} = \operatorname*{argmin}_{S \subset V, |S| = k} \biggl( \max_{v_i \in V} \left( w_i \cdot d(v_i, S) \right) \biggr)$$

这一等价性为 SCoRe 提供了坚实的理论基础（Section 4.1）。加权 k-中心问题是组合优化中的经典 NP-hard 问题，但存在高效的贪婪近似算法。SCoRe 正是基于该问题的贪婪求解策略，将剪枝从现有的解耦启发式（先 Top-k 显著性选择，再聚类补偿多样性）提升为**单一统一优化步骤**。

### SCoRe 贪婪选择公式

SCoRe 采用迭代贪婪策略构建代表性子集。第一步，选择显著性分数最高的令牌作为初始代表点 $s_1$。此后每一步 $t$，从剩余令牌中选取一个令牌 $s_t$，使其最大化**到已选集的最小余弦距离**与**显著性分数 $\alpha$ 次幂**的乘积：

$$s_t = \operatorname*{argmax}_{v_i \in V \setminus S_{t-1}} \left( d_{\cos}(v_i, S_{t-1}) \cdot (\operatorname{score}(v_i))^{\alpha} \right)$$

其中：
- $d_{\cos}(v_i, S_{t-1}) = \min_{s \in S_{t-1}} (1 - \cos(v_i, s))$ 是令牌 $v_i$ 到当前已选集 $S_{t-1}$ 的最小余弦距离，度量**覆盖度增益**——距离越大，说明该令牌所在的语义区域尚未被现有代表点覆盖；
- $\operatorname{score}(v_i)$ 是从视觉编码器最后一层的 `[CLS]` 注意力中提取的**显著性权重**，反映该令牌对下游任务的重要性；
- $\alpha$ 是控制覆盖度与显著性之间权衡的超参数：$\alpha=0$ 退化为纯多样性算法，$\alpha \to \infty$ 退化为纯 Top-k 显著性选择。

### 流水线集成位置

SCoRe 作为一个**即插即用、训练无关**的模块，位于视觉编码器与模态投影器之间（Figure 3）。具体流程为：
1. **视觉编码器**提取图像的视觉令牌特征及 `[CLS]` 注意力显著性权重；
2. **SCoRe 模块**基于上述贪婪公式从 $n$ 个令牌中迭代选取 $k$ 个代表性子集；
3. 保留的 $k$ 个令牌经**模态投影器**映射到 LLM 的文本语义空间；
4. **LLM 解码器**接收多模态输入序列并生成最终回答。

由于剪枝发生在 LLM 之前，SCoRe 天然兼容 FlashAttention 等高效注意力实现，无需修改 LLM 内部结构。

![[assets/figures/papers/paper_list_l781_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SCoRe_Salience_Cove/figures/002_Figure_2.jpg]]
*Figure 2: UMAP-based visualization: (a) Original tokens after UMAP dimensionality reduction and DBSCAN clustering with coloring; (b) Tokens retained by the Top-k attention score strategy, where sampling collapse occurs; (c) Tokens retained by the SCoRe algorithm, which achieves higher coverage*

## 实验与关键发现

### 主实验结果

SCoRe 在多个视觉语言模型和剪枝比率下均展现出显著的性能优势。在 LLaVA-1.5-7B 上，当仅保留 32 个视觉令牌（剪枝率 94.4%）时，SCoRe 维持了基准性能的 95%，远超主流方法 **SparseVLM**（Zhang et al., 2024）的 77.9% 和 **VisPruner**（Zhang et al., CVPR 2025）的 91.5%（Figure 1）。在保留 128 个令牌（剪枝率 77.8%）的宽松设置下，SCoRe 甚至实现了 100.6% 的相对性能，略高于原始全令牌基准（Table 1）。

![[assets/figures/papers/paper_list_l781_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SCoRe_Salience_Cove/figures/001_Figure_1.jpg]]
*Figure 1: Performance comparison across ten LVLM benchmarks. All methods are evaluated under the identical setting of retaining 32 tokens (i.e., a 94.4% pruning rate). SCoRe (red) achieves comprehensive superiority over previous SOTA methods on key benchmarks such as VQAText, GQA, and MMBench. The performance area of SCoRe (red region) is the largest, verifying the superiority of its unified optimization framework. While pruning 94.4% of tokens, it maintains 95% of the baseline performance, outperforming mainstream methods: SparseVLM [49] (77.9%), VisPruner [47] (91.5%)*

![[assets/figures/papers/paper_list_l781_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SCoRe_Salience_Cove/figures/004_Table_1.jpg]]
*Table 1: Performance comparison of different pruning methods on LLaVA-1.5-7B. Here, Acc. denotes the average accuracy across 10 benchmarks, and Rel. represents the average percentage of performance maintained at the corresponding reduction ratio*

在更强的基础模型 LLaVA-NeXT-7B 上，SCoRe 在 94.4% 剪枝率下保持了 93.4% 的原始性能（Table 2），验证了方法的跨架构泛化能力。在 Qwen-VL-7B 上的实验同样证明了 SCoRe 的即插即用特性（Table 3）。此外，SCoRe 在视频理解任务上也表现有效：在 Video-LLaVA 框架下，SCoRe 在三个常用视频问答基准上均取得了有竞争力的结果（Table 4）。

![[assets/figures/papers/paper_list_l781_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SCoRe_Salience_Cove/figures/005_Table_2.jpg]]
*Table 2: Performance comparison of different pruning methods on LLaVA-NeXT-7B. Acc. denotes the average accuracy across benchmarks, and Rel. represents the average percentage of performance maintained at the corresponding reduction ratio*

![[assets/figures/papers/paper_list_l781_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SCoRe_Salience_Cove/figures/007_Table_3.jpg]]
*Table 3: Performance of SCoRe on Qwen-VL-7B. Acc. denotes the average accuracy across benchmarks, Rel. represents the average percentage of performance maintained*

资源效率方面，Table 5 显示 SCoRe 在 FLOPs、GPU 内存占用和推理延迟上均实现显著降低，且无需额外存储开销，优于需要维护键值缓存的 **FastV**（Chen et al., 2024）等方法。

### 消融实验

消融实验系统验证了统一优化框架的必要性。Figure 4 展示了三种策略的对比：纯多样性策略（α = 0）、纯显著性策略（α → ∞）以及 SCoRe 的平衡策略。在多个基准上，SCoRe 的完整方法均显著优于两种极端策略，证明单一复合分数同时优化覆盖度与显著性的设计是性能提升的根本原因。

![[assets/figures/papers/paper_list_l781_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_SCoRe_Salience_Cove/figures/009_Figure_4.jpg]]
*Figure 4: Ablation study on the balance between diversity and salience. All experiments retain 32 visual tokens. Diverse corresponds to SCoRe with α = 0 (degrading to a pure diversity-based algorithm), Important corresponds to SCoRe with a sufficiently large α (degrading to a pure salience-based algorithm), and SCoRe represents our full method that balances both properties*

超参数敏感性分析（Figure 5）进一步揭示，在 TextVQA 任务上，α 的最优取值区间为 0.6–1.0。过小的 α 导致覆盖度过度优先而忽略显著性，过大的 α 则退化为 Top-k 选择并引发采样坍缩，二者均会造成性能下降。这一发现为实际部署中的超参数选择提供了明确指导。

### 失败模式与局限性

尽管 SCoRe 在整体基准上表现优异，但需注意以下边界情况：

1. **细粒度文本感知的潜在退化**：在 TextVQA 等需要精确 OCR 能力的任务上，SCoRe 的剪枝策略可能丢弃包含关键文本信息的令牌。虽然 α 的调节可部分缓解此问题，但在极高剪枝率下，文本区域的覆盖度仍可能不足。这一影响需通过更细粒度的令牌级分析来量化。

2. **固定剪枝比率的限制**：SCoRe 当前需要预设保留令牌数 k，无法根据输入图像的复杂度自适应调整。对于简单图像，固定 k 可能保留冗余令牌；对于复杂场景，k 可能不足以覆盖所有关键语义区域。

3. **贪婪算法的次优性**：SCoRe 的贪婪选择策略虽在实践中表现优异，但加权 k-中心问题的理论近似比尚未在该特定设置下严格证明。是否存在更优的组合优化方法可进一步提升代表性质量，仍是一个开放问题。

## 定位与知识库关联

### 视觉令牌压缩方法谱系

视觉语言模型（VLM）的令牌剪枝与合并研究可大致分为三条技术路线：**基于显著性的剪枝**、**基于相似度的合并**，以及**混合解耦策略**。SCoRe 的贡献在于将这三条路线的核心矛盾——显著性与覆盖度的权衡——统一到一个形式化优化框架中。

**基于显著性的剪枝方法**以令牌的重要性分数为唯一选择依据。**FastV**（Chen et al., 2024）利用 LLM 早期层的跨模态注意力图识别关键视觉令牌，在 LLM 内部进行剪枝。这类方法的核心缺陷在于高显著性令牌往往在语义空间中高度聚集，导致“采样坍缩”（sampling collapse）——大量语义区域完全丢失代表性令牌（参见 Figure 2b 的 UMAP 可视化）。

**基于相似度的合并方法**以 **ToMe**（Bolya et al., 2022）为代表，通过逐步合并余弦相似度最高的令牌对来减少序列长度。该方法天然有利于维持语义覆盖度，但完全忽略了令牌的重要性差异，可能将关键细节合并到无关背景令牌中。

**混合解耦策略**试图先后解决两个目标。**SparseVLM**（Zhang et al., 2024）先基于 LLM 内部注意力选择高显著性令牌，再通过聚类补偿多样性；**VisPruner**（Zhang et al., CVPR 2025）利用视觉线索进行剪枝，同样采用两阶段设计；**VisionZip**（Yang et al., 2024）则混合使用基于 [CLS] 注意力的选择和令牌合并。这些方法的共同瓶颈在于：显著性与覆盖度的优化被解耦为两个独立步骤，第一阶段的选择偏差无法在第二阶段完全纠正，导致全局最优性无法保证。

### SCoRe 的方法定位

SCoRe 将视觉令牌剪枝重新定义为**加权 k-中心问题**（Weighted k-Center Problem），在理论上等价于经典的设施选址问题（Hochbaum & Shmoys, 1985）。这一形式化带来的根本性突破在于：显著性和覆盖度不再是两个需要先后处理的独立目标，而是统一在同一个目标函数中——

$$\mathcal{R}(S, V) = \max_{v_i \in V} \left( w_i \cdot d(v_i, S) \right)$$

其中 $w_i$ 编码显著性权重，$d(v_i, S)$ 衡量令牌到已选集合的最小余弦距离（即覆盖度缺口）。SCoRe 的贪婪选择准则——

$$s_t = \operatorname*{argmax}_{v_i \in V \setminus S_{t-1}} \left( d_{\cos}(v_i, S_{t-1}) \cdot (\operatorname{score}(v_i))^{\alpha} \right)$$

——在每一步同时优化两个维度：距离项鼓励探索未被覆盖的语义区域，显著性项确保高重要性区域被优先保留。超参数 $\alpha$ 控制两者的平衡（Figure 5 显示在 TextVQA 上最优区间为 0.6–1.0）。

从架构集成角度看，SCoRe 作为**即插即用模块**放置于视觉编码器与模态投影器之间（Figure 3），这一设计使其：（1）完全训练无关，无需任何微调；（2）与下游 LLM 的解码器架构解耦，兼容 FlashAttention 等高效注意力实现；（3）对视觉编码器的选择不敏感，可泛化到不同的 VLM 架构（LLaVA-1.5、LLaVA-NeXT、Qwen-VL）。

### 适用边界与局限

**适用场景。** SCoRe 在中等剪枝率（77.8%–88.9%）下表现最优，甚至在 LLaVA-1.5-7B 上以 128 令牌（77.8% 剪枝）实现了 100.6% 的相对性能（Table 1），略超原始完整令牌的基准性能。在极高剪枝率（94.4%，仅保留 32 令牌）下，SCoRe 仍保持 95% 的基准性能，显著优于 VisPruner（91.5%）和 SparseVLM（77.9%）（Figure 1）。在视频理解任务上，SCoRe 同样展示了跨模态泛化能力（Table 4）。

**已知局限。** 首先，SCoRe 需要预设剪枝比率 $k$，无法根据输入图像的复杂度自适应调整——对于简单图像可能保留了冗余令牌，而对于信息密集的图像（如包含大量文本的文档）可能丢失关键细节。其次，贪婪算法虽然高效，但与全局最优解之间的理论近似比尚未在论文中严格证明；作者仅通过实验表明贪婪解在实践中足够接近最优。第三，在极高剪枝率下（如 LLaVA-NeXT-7B 上 32 令牌时相对性能降至 93.4%，Table 2），性能损失开始显现，表明存在一个覆盖度与显著性无法同时满足的下界。

### 开放问题

1. **自适应剪枝比率。** 如何根据输入图像的语义复杂度（如文本密度、物体数量）动态决定 $k$，使简单图像进一步压缩而复杂图像保留更多令牌？
2. **理论近似比。** SCoRe 的贪婪算法与加权 k-中心问题的全局最优解之间的近似比是否可证？能否通过局部搜索或线性规划松弛进一步提升解的质量？
3. **极端场景下的退化。** 在长视频或高分辨率图像中，视觉令牌空间呈数量级增长，显著性权重的估计噪声和覆盖度计算的稀疏性问题如何应对？
4. **细粒度感知的量化评估。** SCoRe 剪枝是否系统性地损害模型对 OCR 文本、小物体等细粒度细节的感知能力？现有的基准测试（如 TextVQA）提供了初步信号，但缺乏细粒度的归因分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/SCoRe_Salience_Coverage_Reduction_for_Vision_Token_Pruning_in_Vision_Language_Models.pdf]]
