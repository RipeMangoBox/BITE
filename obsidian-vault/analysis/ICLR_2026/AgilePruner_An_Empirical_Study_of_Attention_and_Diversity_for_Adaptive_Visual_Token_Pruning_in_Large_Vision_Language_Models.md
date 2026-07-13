---
title: "AgilePruner: An Empirical Study of Attention and Diversity for Adaptive Visual Token Pruning in Large Vision-Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AgilePruner_An_Empirical_Study_of_Attention_and_Diversity_for_Adaptive_Visual_Token_Pruning_in_Large_Vision_Language_Models.pdf
project_link: https://cvsp-lab.github.io/AgilePruner
code_link: null
aliases:
- AgilePruner
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "根据图像复杂度指标 erank 与注意力熵，自适应调节注意力选择和多样性保留的视觉令牌剪枝。"
primary_logic: |
  先用 erank 与注意力熵分析图像复杂度和不同剪枝策略的行为差异，再依据简单图像偏好注意力剪枝、复杂图像偏好多样性剪枝的观察，设计按输入 erank 调整相似性阈值的 AgilePruner，并在 LVLM 多基准中验证速度、性能和幻觉指标。
claims:
- "基于注意力的剪枝在低 erank、低注意力熵图像上更有效，基于多样性的剪枝在高 erank、高注意力熵图像上更有效。"
- "AgilePruner 通过自适应阈值保留少量视觉令牌，在多基准上维持接近全令牌性能并显著降低 FLOPs。"
---

# AgilePruner: An Empirical Study of Attention and Diversity for Adaptive Visual Token Pruning in Large Vision-Language Models

> [!tip] 核心洞察
> 基于注意力的剪枝在简单图像（低erank、低注意力熵）上更有效，而基于多样性的剪枝在复杂图像（高erank、高注意力熵）上表现更好；更高的保留多样性与更高的幻觉频率相关。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AgilePruner：面向大型视觉语言模型中自适应视觉令牌剪枝的注意力与多样性实证研究 |
| 英文题名 | AgilePruner: An Empirical Study of Attention and Diversity for Adaptive Visual Token Pruning in Large Vision-Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=2NLkhPex1M) · [Project](https://cvsp-lab.github.io/AgilePruner) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | AgilePruner（自适应阈值剪枝方法） |
| Dataset | GQA, SQAIMG, POPE, MME |

> [!tip] 效果简介
> - GQA 上，Accuracy 为 57.4，对比 57.0 (LLaVA-1.5-7B full)，变化 +0.4。
> - SQAIMG 上，Accuracy 为 68.6，对比 70.2 (LLaVA-1.5-7B full)，变化 -1.6。
> - POPE 上，Accuracy 为 84.1，对比 85.9 (LLaVA-1.5-7B full)，变化 -1.8。

## 概要

本文《AgilePruner: An Empirical Study of Attention and Diversity for Adaptive Visual Token Pruning in Large Vision-Language Models》对大型视觉语言模型（LVLM）中视觉令牌剪枝的两种主流范式——基于注意力的剪枝与基于多样性的剪枝——进行了系统的实证研究。通过引入有效秩（erank）和注意力熵两个可量化的图像复杂度指标，论文揭示了不同剪枝策略在不同图像类型上的性能偏好，并发现保留令牌的多样性与幻觉频率之间存在正相关关系。基于这些发现，作者提出了AgilePruner，一种自适应阈值剪枝方法，能够根据图像复杂度动态调节注意力选择与多样性保留之间的平衡。在LLaVA-1.5-7B上，该方法在保留64个令牌时平均相对性能达到96.76%，在保留128个令牌时达到98.04%，同时将计算量降低约89%。



大型视觉语言模型（LVLM）通常由视觉编码器（vision encoder）、模态投影器（modality projector）和大语言模型（LLM）组成。视觉编码器将输入图像转换为大量视觉令牌（例如LLaVA-1.5-7B使用576个令牌），这些令牌随后通过投影器与LLM的词嵌入空间对齐。处理大量视觉令牌带来了显著的计算开销，因此视觉令牌剪枝成为提升LVLM推理效率的关键技术。

现有视觉令牌剪枝方法可分为三类：基于注意力的方法（如FasterVLM、PyramidDrop、SparseVLM）优先保留注意力分数高的令牌，但可能导致选择集中且重复；基于多样性的方法（如DivPrune、FPSPruner）基于特征相似性减少冗余，鼓励更广泛的覆盖，但可能忽略重要令牌；混合方法（如VisPruner、BAT、PruMerge+）尝试结合两种策略。

然而，现有方法的实际行为缺乏系统表征。具体而言，以下关键问题尚未得到充分研究：不同剪枝方法在特征多样性保留程度上的差异；保留令牌的属性与幻觉倾向之间的关系；以及不同图像类型对不同剪枝策略的偏好。本文旨在填补这些空白。



## 核心方法与创新机理

本文的核心创新在于：

1. **系统性实证分析**：首次通过有效秩（erank）和注意力熵两个指标，系统量化了不同剪枝方法在特征多样性保留上的差异，并建立了保留多样性与幻觉频率之间的关联。

2. **图像复杂度驱动的自适应剪枝**：基于实证发现——基于注意力的剪枝在简单图像（低erank、低注意力熵）上更有效，而基于多样性的剪枝在复杂图像（高erank、高注意力熵）上表现更好——提出了自适应调节注意力与多样性权重的机制。

3. **自适应阈值剪枝模块**：设计了一种基于图像复杂度的动态相似性阈值公式，能够根据输入图像的erank自适应调整剪枝的激进程度。

4. **跨模型架构的泛化验证**：在LLaVA-1.5-7B、LLaVA-1.5-13B、LLaVA-NeXT-7B和Qwen2.5-VL-7B等多种模型架构上验证了方法的有效性。



AgilePruner的整体框架包含以下核心模块：

1. **视觉编码器（Vision Encoder）**：将输入图像转换为视觉令牌嵌入。典型LVLM架构包含视觉编码器、模态投影器和LLM。

2. **erank计算模块**：计算视觉令牌嵌入矩阵的有效秩，量化特征多样性。Token embedding diversity via erank. ... erank(A) = exp(-∑ q_i log q_i).

3. **注意力熵计算模块**：计算[CLS]令牌注意力分数的香农熵，量化注意力集中程度。Attention concentration via attention entropy. ... H(p) = -∑ p_i log p_i.

4. **自适应阈值剪枝模块**：根据erank动态调整相似性阈值，迭代选择高注意力令牌并剪枝相似邻居。Our method iteratively selects high-attention tokens and prunes similar neighbors, thereby modulating the diversity of the final token set based on the chosen threshold.

5. **模态投影器（Modality Projector）**：将视觉令牌与LLM词嵌入空间对齐。The vision encoder converts input images into visual tokens, and the projector aligns these tokens with the LLM's word-embedding space.

6. **大语言模型（LLM）**：处理剪枝后的视觉令牌与文本令牌，生成响应。the LLM can effectively interpret and process visual information.



### 1 注意力熵（Attention Entropy）

对[CLS]令牌注意力分数进行重归一化后计算的香农熵，用于量化注意力在视觉令牌上的集中程度：

$$p_i = \frac{\alpha_i}{\sum_{j \neq CLS} \alpha_j}, \quad \sum_i p_i = 1. \quad H(p) = -\sum_i p_i \log p_i.$$

较低的熵值表示[CLS]令牌强烈关注少数区域，较高的熵值表示注意力在多个视觉令牌上更均匀分布。

### 2 有效秩（Effective Rank, erank）

基于奇异值归一化后熵的指数，衡量令牌嵌入矩阵有效利用的维度数，范围在1到L之间：

$$L = \min(N, d_l), \quad q_i = \frac{\sigma_i}{\sum_{j=1}^L \sigma_j}, \quad \text{erank}(A) = \exp\left(-\sum_{i=1}^L q_i \log q_i\right).$$

### 3 CHAIR幻觉指标

实例级幻觉指标C_I和句子级幻觉指标C_S分别定义为：

$${\cal C}_I = \frac{|\{\mathrm{hallucinated\ objects}\}|}{|\{\mathrm{all\ mentioned\ objects}\}|}$$

$${\cal C}_S = \frac{|\{\mathrm{captions\ with\ hallucinated\ objects}\}|}{|\{\mathrm{all\ captions}\}|}$$

### 4 自适应阈值公式

基于令牌顺序和归一化图像复杂度的动态相似性阈值：

$$\tau_i = \mathrm{order}_i \times \left( \frac{\mathrm{erank}_{\mathrm{input}}}{\mathrm{erank}_{\mathrm{avg}}} \times 0.01 \right)$$

其中order_i是令牌的注意力排序位置，erank_input是输入图像的erank值，erank_avg是数据集的平均erank值。

### 5 erank快速协方差形式

通过协方差矩阵特征值谱计算的有效秩，降低计算复杂度：

$$C = X X^\top, \quad S = \sqrt{\lambda(C)}, \quad p_i = \frac{S_i}{\sum_j S_j}, \quad \operatorname{erank}(X) = \exp\left(-\sum_i p_i \log p_i\right)$$



## 实验与关键发现

### 1 主要结果

在LLaVA-1.5-7B上的9个多模态基准测试结果（Table 7）显示：

| 基准 | 指标 | 提出方法 | 全令牌基线 | 差值 |
|------|------|----------|------------|------|
| GQA | Accuracy | 57.4 | 57.0 | +0.4 |
| SQAIMG | Accuracy | 68.6 | 70.2 | -1.6 |
| POPE | Accuracy | 84.1 | 85.9 | -1.8 |
| MME | Score | 1703 | 1771 | -68 |
| TextVQA | Accuracy | 56.0 | 58.2 | -2.2 |
| 平均（9基准，64令牌） | 归一化 | 96.76% | 100% | -3.24% |
| 平均（9基准，128令牌） | 归一化 | 98.04% | 100% | -1.96% |

### 2 幻觉分析

CHAIR数据集上的评估结果（Table 2, Table 8）揭示了保留多样性与幻觉之间的关键关系：

- DivPrune（基于多样性）在CHAIR上C_S=57.4，C_I=18.0，而FasterVLM（基于注意力）C_S=45.4，C_I=13.5，表明多样性方法幻觉更高。
- 增加注意力选择比例R从0到0.75，C_S从57.4降至45.2，C_I从18.0降至14.1，幻觉显著降低（Table 3）。
- 提出方法在64令牌时达到C_S=52.2，C_I=15.9，Recall=75.7，在幻觉与召回之间取得平衡。

### 3 图像复杂度分析

Table 4显示简单图像（OCR）的注意力熵为4.61，erank为78；复杂图像（POPE）的注意力熵为4.87，erank为106。在简单图像上，基于注意力的剪枝得分140 vs 基于多样性的130；在复杂图像上，基于多样性的剪枝得分86.0 vs 基于注意力的77.4。

### 4 消融实验

- **自适应规则有效性**：将自适应规则应用于VisPruner和BAT，在128和64令牌设置下均带来一致的准确率提升（Table 5）。
- **反向自适应验证**：反向自适应（对高erank图像分配更多注意力令牌）导致性能明显下降。
- **基于熵的自适应**：基于熵的自适应与基于erank的自适应性能趋势高度一致，差异仅约0.13（Table 11）。
- **自适应数量剪枝**：自适应数量剪枝（平均85.5令牌）优于固定数量剪枝（88令牌），相对性能96.0% vs 95.4%（Table 13）。
- **相似性阈值影响**：增加相似性阈值τ直接增加所选令牌的多样性（erank）（Table 12）。

### 5 效率分析

在TextVQA数据集上（Table 9），提出方法在64令牌时达到56.0准确率，0.48 T FLOPs，115 ms延迟，13.30 GB GPU内存，相比全令牌基线（58.2准确率，3.14 T FLOPs，172 ms延迟）实现了约89%的FLOPs减少。erank计算平均耗时3.4 ms，仅占总推理时间的约3.2%（Table 10）。

### 6 跨模型泛化

在LLaVA-1.5-13B上，提出方法在128令牌时达到97.6%相对性能（Table 14）；在LLaVA-NeXT-7B上，640令牌时达到99.64%相对性能（Table 15）；在Qwen2.5-VL-7B上也验证了有效性（Table 16）。

### 7 erank鲁棒性

在COCO-C的15种图像损坏类型下，erank表现出高度稳定性，平均偏差在严重度1时为2.78，严重度3时为4.11（Table 17）。改变全局空间结构的损坏（如zoom blur、frost、snow、elastic transform）产生中等偏大的erank偏差（4-7点），而局部像素级失真（如brightness、pixelation、JPEG compression）的偏差最小（1-2.5点）。



## 定位与知识库关联

本文在视觉令牌剪枝方法谱系中占据独特位置。现有方法可分为三类：基于注意力的方法（FasterVLM、PyramidDrop、SparseVLM、VisionZip）优先保留高注意力令牌；基于多样性的方法（DivPrune、FPSPruner）最大化令牌间的几何分散度；混合方法（VisPruner、BAT、PruMerge+）尝试结合两种策略但使用固定比例。

AgilePruner的核心贡献在于：它不是提出一种全新的剪枝算子，而是通过系统的实证分析揭示了注意力与多样性之间的互补关系，并基于图像复杂度（erank和注意力熵）实现了自适应的策略选择。这一思路使得该方法可以作为一种通用框架应用于现有混合方法（如VisPruner和BAT），带来一致的性能提升。

论文的局限性包括：自适应方法在低erank图像中物体分散时，集中选择无法捕捉全局空间布局，导致计数错误；在高erank图像中关键证据高度局部化时，广泛分散的令牌选择会稀释重要区域的注意力；erank计算虽然高效（约3.4ms），但仍引入约3.2%的额外推理时间开销；自适应阈值公式中的超参数（如erank_avg）可能需要针对不同模型或数据集进行校准。

开放问题包括：自适应方法在更广泛的LVLM架构上的表现；将erank和注意力熵的联合分析扩展到视频输入的多帧令牌剪枝；自适应阈值公式中erank_avg的在线动态更新；对于同时包含简单和复杂区域的混合图像，设计更精细的区域自适应剪枝策略；以及探索更优的单一或组合图像复杂度指标（erank与注意力熵的皮尔逊相关系数为0.63）。

### 整体框架

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2NLkhPex1M_AgilePruner_An_/figures/001_Figure_1.jpg]]

### 实验与分析

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2NLkhPex1M_AgilePruner_An_/figures/002_Table_1.jpg]]
*Table 1: Mean erank of retained 64 tokens on POPE.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2NLkhPex1M_AgilePruner_An_/figures/004_Table_2.jpg]]
*Table 2: Comparison on CHAIR. †FPSPruner is based on farthest point sampling (FPS), which iteratively selects the farthest token to guarantee diversity.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2NLkhPex1M_AgilePruner_An_/figures/006_Table_3.jpg]]
*Table 3: Effect of attention-based selection ratio R on CHAIR metrics. Higher attention-based selection reduces hallucination ( $\overbar { C _ { S } } , \overbar { C _ { I } }$ ) but lowers recall.

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2NLkhPex1M_AgilePruner_An_/figures/007_Table_4.jpg]]
*Table 4: (a) Results on datasets with simple images. (b) Results on datasets with complex images.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_2NLkhPex1M_AgilePruner_An_/figures/008_Table_4.jpg]]
*Table 4: Attention entropy and erank on simple and complex image datasets. Simple images exhibit lower entropy and erank, while complex images show higher values, and the two pruning methods show contrasting performance between simple and complex images.*



## 原文 PDF

![[paperPDFs/ICLR_2026/AgilePruner_An_Empirical_Study_of_Attention_and_Diversity_for_Adaptive_Visual_Token_Pruning_in_Large_Vision_Language_Models.pdf]]
