---
title: "PDCR: Perception-Decomposed Confidence Reward for Vision-Language Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PDCR_Perception_Decomposed_Confidence_Reward_for_Vision_Language_Reasoning.pdf
project_link: null
code_link: "https://github.com/hee-suk-yoon/PDCR"
aliases:
- PPDCR
- PDCR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入无监督技能分解（视觉依赖评分 + Otsu 最优聚类）并在各自技能簇内独立归一化置信度增益，为每种技能提供稳定的、正确标度的训练信号。
primary_logic: 视觉感知和文本推理是功能不同、统计异质的两种技能，必须通过分解的奖励结构进行独立评估，才能真正解决多模态推理中的信用分配问题。
claims:
- 视觉感知步骤仅占全部推理步骤的31.4%，而文本推理步骤占68.6%，形成严重的统计不平衡。
- 朴素的全局归一化（Eq. 5）会压缩和错配视觉步骤的优势分布，而本文提出的分解归一化可提供稳定、良好标度的优势信号。
- 基于Otsu的动态阈值方法实现76.2%的技能分解准确率，显著优于最佳Top-K基线（67.5%），且无超参数。
- 在Qwen2.5-VL-7B上，PDCR在七个基准上的平均准确率达到52.9，超过PACR (52.2) 和GRPO (51.5)。
---

# PDCR: Perception-Decomposed Confidence Reward for Vision-Language Reasoning

> [!tip] 核心洞察
> 视觉感知和文本推理是功能不同、统计异质的两种技能，必须通过分解的奖励结构进行独立评估，才能真正解决多模态推理中的信用分配问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | PDCR: 面向视觉-语言推理的感知解耦置信度奖励 |
| 英文题名 | PDCR: Perception-Decomposed Confidence Reward for Vision-Language Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.13467) · [Code](https://github.com/hee-suk-yoon/PDCR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PDCR (Perception-Decomposed Confidence Reward) |
| Dataset | MMMU-Pro, MMMU, HallusionBench |

> [!tip] 效果简介
> - MMMU-Pro 上，准确率 42.5 vs 41.5 (PACR) (+1.0)。
> - MMMU 上，准确率 51.5 vs 50.5 (PACR) (+1.0)。
> - HallusionBench 上，准确率 68.4 vs 67.6 (PACR) (+0.8)。

## 概述

视觉-语言（V-L）推理要求模型同时完成两类异构行为：**视觉感知**（从图像中提取证据）与**文本推理**（基于证据进行逻辑推导）。现有密集奖励方法（如PACR）对所有推理步骤施加全局统一的置信度归一化，忽视了这两类技能在统计分布上的本质差异。经实证统计，视觉感知步骤仅占全部推理步骤的31.4%，而文本推理步骤占68.6%——这种严重的不平衡导致全局归一化压缩并扭曲了视觉步骤的优势信号，产生**混合诱导的信号退化**问题。

本文提出 **PDCR（Perception-Decomposed Confidence Reward）**，一种感知解耦的置信度奖励框架。其核心思路是：首先通过无监督技能分解，引入模型内部的**视觉依赖评分（Visual Dependence Score）**量化每个推理步骤对视觉输入的依赖程度，并采用Otsu动态阈值将步骤自动聚类为视觉感知组与文本推理组；随后在各自技能簇内独立进行min-max优势归一化，生成标度稳定、语义正确的步级训练信号。

在Qwen2.5-VL-7B骨干上，PDCR在七个V-L推理基准上取得**52.9的平均准确率**，超过PACR（52.2）和GRPO（51.5）。消融实验表明，有意义的技能分解（而非随机分配）是性能提升的关键；Otsu动态阈值化达到76.2%的分解准确率，显著优于最佳Top-K基线（67.5%）且无需超参数。PDCR的训练额外开销约为GRPO的1.5倍，但推理阶段模型生成更简洁的推理轨迹，实现了训练成本与推理效率的有利权衡。

## 背景与动机

### 多模态推理中的异质技能混合

视觉-语言（V-L）推理任务要求模型同时执行两种功能不同的行为：从图像中提取证据的**视觉感知**（seeing），以及基于该证据进行逻辑推导的**文本推理**（thinking）。如图1所示，一个典型的V-L推理轨迹天然地混合了这两类步骤——模型先“看”图像中的关键信息，再“思考”如何从这些信息出发得到最终答案。然而，现有的过程奖励方法普遍将这两种统计特性迥异的技能视为同质，采用全局统一的奖励信号进行训练，这构成了一个被忽视的根本性问题。

### 现有密集奖励方法的信号退化

为缓解稀疏结果奖励（如GRPO的二元正确/错误信号）带来的信用分配困难，近期工作引入了密集过程奖励。其中代表性方法是**逐步上升置信度奖励（PACR）**，它通过计算模型在每个推理步骤上对真实答案的对数概率增量，为每个步骤提供细粒度的过程优势信号。然而，PACR采用全局min-max归一化（Eq. 5）对所有轨迹的所有步骤进行统一缩放：

$$A_{P,k}^{(i)} = \frac{G_k^{(i)} - \min_{(j,k')} G_{k'}^{(j)}}{\max_{(j,k')} G_{k'}^{(j)} - \min_{(j,k')} G_{k'}^{(j)}}$$

这种全局归一化策略隐含假设所有推理步骤来自同一个统计分布，但这一假设在V-L推理场景下并不成立。

### 核心观察：混合诱导的信号退化

本文通过实证分析揭示了一个关键现象：**视觉感知步骤在数量上仅占全部推理步骤的31.4%，而文本推理步骤占据了压倒性的68.6%**（Figure 3-c）。这种严重的统计不平衡导致全局归一化产生**混合诱导的信号退化**——占多数的文本步骤主导了归一化的尺度和偏移，使得视觉感知步骤的优势分布被压缩和错配（Figure 3-d）。具体而言，视觉步骤的优势值被挤压到一个狭窄且不合理的区间内，模型无法从中获得有效的训练信号来改进其“看”的能力。这本质上是一个**跨异质技能的信用分配失败**问题：朴素的全局奖励信号无法正确地将功劳（或责任）归因到正确的技能类型上。

### 本文动机

上述观察指向一个清晰的问题瓶颈：**视觉感知和文本推理是功能不同、统计异质的两种技能，必须通过分解的奖励结构进行独立评估**。本文的核心动机是设计一种能够自动识别并解耦这两种技能的过程奖励机制，使得每种技能都能在其自身的统计分布内获得稳定、正确标度的训练信号，从而真正解决多模态推理中的信用分配问题。这一思路将过程奖励的设计从“更密集的信号”推进到“结构正确的信号”。

## 核心创新

PDCR 的核心创新在于将视觉-语言推理中的**信用分配问题**重新表述为**异质技能的独立评估问题**，并通过无监督技能分解与分簇优势归一化两个关键机制予以解决。与现有密集奖励方法（如 PACR）将所有推理步骤视为同质序列进行全局归一化不同，PDCR 识别出视觉感知与文本推理是两种统计分布截然不同的技能，必须在其各自的簇内进行独立的奖励标度。

### 创新一：基于视觉依赖评分的无监督技能分解

现有密集奖励基线（GRPO、DAPO、PACR）均未对推理步骤进行技能类型的区分，隐式假设所有步骤服从同一分布。PDCR 引入了**Visual Dependence Score（视觉依赖评分）**来量化每一步对视觉输入的依赖程度，从而为无监督技能聚类提供信号。

具体而言，对于第 $i$ 条轨迹的第 $k$ 步，视觉依赖评分定义为该步骤在真实图像与空白（白色）图像下的对数概率之差：

$$V_{k}^{(i)} = p_{k}^{(i)} - p_{w,k}^{(i)}$$

其中 $p_{k}^{(i)} = \log \pi_{\theta}(h_{k}^{(i)} | \mathbf{I}, \mathbf{q}, H_{<k}^{(i)})$ 为给定真实图像时的步骤对数概率，$p_{w,k}^{(i)}$ 为给定空白图像时的对应值。该评分的直觉在于：视觉感知步骤在图像信息被破坏时会遭受显著的概率下降，而文本推理步骤对视觉输入的依赖较弱，其概率变化较小。

在此基础上，PDCR 采用 **Otsu 动态阈值法**对视觉依赖评分进行最优二分类，将步骤自动划分为视觉感知簇和文本推理簇。Otsu 方法通过最小化簇内平方和（SSE）来寻找最优分割点 $k^{*}$：

$$k^{*} = \arg \min_{k} SSE(k)$$

其中 $SSE(k) = \sum_{i=1}^{k} (v_i - \mu_1(k))^2 + \sum_{i=k+1}^{M} (v_i - \mu_2(k))^2$。该方法的关键优势在于**无超参数**——无需预设视觉步骤的比例或数量，而是根据评分分布自适应地确定阈值。

实证验证表明，Otsu 动态阈值化在技能分解任务上达到 **76.2% 的准确率**，显著优于最佳 Top-K 基线的峰值 67.5%（Figure 5）。Top-K 方法对超参数 $k$ 高度敏感，而 Otsu 方法在不同视觉扰动策略下均表现稳健：使用白图、高斯模糊、高斯噪声等语义破坏策略均可达到 75.8%–76.2% 的分解精度，而仅做空间变换（旋转）则效果较差（65.9%），这验证了破坏语义信息对于测量视觉依赖性的必要性。

### 创新二：分簇归一化的感知解耦优势计算

这是 PDCR 与基线方法最根本的**结构性差异**。在基线 PACR 中，过程优势通过全局 min-max 归一化计算，即对所有 $N$ 条轨迹的所有步骤的折扣回报 $G_{k}^{(i)}$ 进行统一缩放：

$$A_{k}^{(i)} = \frac{G_{k}^{(i)} - \min_{j,k'} G_{k'}^{(j)}}{\max_{j,k'} G_{k'}^{(j)} - \min_{j,k'} G_{k'}^{(j)}} \quad \text{(Eq. 5, 基线)}$$

这种全局归一化在步骤分布异质时会引发**混合诱导的信号退化**：视觉感知步骤仅占全部推理步骤的 31.4%（Figure 3-c），其优势分布被占多数的文本推理步骤（68.6%）压缩和错配，导致视觉步骤的训练信号被扭曲。

PDCR 将全局归一化替换为**簇内独立归一化**。对于视觉感知步骤，优势仅在视觉簇 $\mathbb{Z}_{\text{visual}}$ 内计算：

$$A_{V,k}^{(i)} = \frac{G_{k}^{(i)} - \min_{(j,k') \in \mathbb{Z}_{\text{visual}}} G_{k'}^{(j)}}{\max_{(j,k') \in \mathbb{Z}_{\text{visual}}} G_{k'}^{(j)} - \min_{(j,k') \in \mathbb{Z}_{\text{visual}}} G_{k'}^{(j)}}$$

对于文本推理步骤，同理仅在文本簇 $\mathbb{Z}_{\text{textual}}$ 内计算：

$$A_{T,k}^{(i)} = \frac{G_{k}^{(i)} - \min_{(j,k') \in \mathbb{Z}_{\text{textual}}} G_{k'}^{(j)}}{\max_{(j,k') \in \mathbb{Z}_{\text{textual}}} G_{k'}^{(j)} - \min_{(j,k') \in \mathbb{Z}_{\text{textual}}} G_{k'}^{(j)}}$$

最终的总优势由稀疏结果优势与分解过程优势加权融合：

$$A_{total,k}^{(i)} = \lambda_O A_O^{(i)} + \lambda_P A_{decomposed,k}^{(i)}$$

其中 $A_O^{(i)}$ 为基于答案正确性的组归一化结果优势，$A_{decomposed,k}^{(i)}$ 为根据步骤所属簇选取的 $A_{V,k}^{(i)}$ 或 $A_{T,k}^{(i)}$。

这一设计的因果机制在于：分簇归一化使每种技能的优势分布独立地以零为中心、具有一致的标度，从而为策略梯度提供**稳定、良好标度的训练信号**（Figure 3-d）。消融实验证实了该设计的必要性——将基于视觉依赖评分的分解替换为随机分配后，Qwen2.5-VL-7B 上的七基准平均准确率从 52.9 降至 52.3（Table 2），验证了有意义的技能分解对性能提升至关重要。

### 与基线方法的系统对比

| 设计维度 | GRPO | DAPO | PACR | **PDCR (本文)** |
|---------|------|------|------|-----------------|
| 奖励密度 | 稀疏（仅结果） | 稀疏（仅结果） | 密集（步级置信度增益） | 密集（步级置信度增益） |
| 技能分解 | 无 | 无 | 无（所有步骤同质） | **有（视觉依赖评分 + Otsu 聚类）** |
| 优势归一化 | 组级结果归一化 | 组级结果归一化 | 全局 min-max（跨所有步骤） | **分簇 min-max（视觉/文本独立归一化）** |
| 视觉特异性处理 | 无 | 无 | 无 | **有（空白图像参考基线）** |

综上，PDCR 的创新本质在于将多模态推理的信用分配从“同质序列评估”升级为“异质技能独立评估”，通过无监督分解和分簇归一化两个 changed slots 解决了视觉感知信号在文本推理占优的环境中被压缩和扭曲的核心瓶颈。

## 整体框架

PDCR 的核心动机源于对视觉-语言推理中**混合诱导信号退化**问题的观察：视觉感知步骤仅占总推理步骤的 31.4%，而文本推理步骤占 68.6%（Figure 3-c），这种统计不平衡导致朴素的全局置信度归一化会压缩视觉步骤的优势信号，产生扭曲的训练反馈（Figure 3-d）。为此，PDCR 提出将推理过程分解为两种异质技能，并在各自技能簇内独立评估，从而为每种技能提供稳定、正确标度的训练信号。

### 框架总览

PDCR 的整体流程如 Figure 4 所示，包含四个核心模块，形成两条并行的信号通路：

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/004_Figure_4.jpg]]
*Figure 4: Overview of our PDCR (Perception-Decomposed Confidence Reward) framework. (Top, green path): We compute the standard Process-level Reward*

1. **置信度计算模块**（绿色路径）：对每条推理轨迹的每个步骤，计算模型对真实答案的对数概率，并计算步骤间的置信度增益 $g_k^{(i)}$（即过程奖励），这是所有密集奖励方法的公共基础。

2. **无监督技能分解模块**（粉色路径）：引入模型内部的 **Visual Dependence Score** $V_k^{(i)} = p_k^{(i)} - p_{w,k}^{(i)}$，通过比较步骤在原图与空白（白色）图像下的对数概率来量化该步骤对视觉输入的依赖程度。随后应用 **Otsu 动态阈值法**——寻找使聚类内方差和 $SSE(k)$ 最小的分割点——将所有步骤自动划分为视觉感知簇 $\mathbb{Z}_{\text{visual}}$ 和文本推理簇 $\mathbb{Z}_{\text{textual}}$。该方法无需任何超参数，分解准确率达到 76.2%，显著优于最佳 Top-K 基线的 67.5%（Figure 5）。

3. **感知解耦优势计算模块**（右侧）：在各自技能簇内对折扣回报 $G_k^{(i)}$ 进行独立的 min-max 归一化，生成视觉感知步骤优势 $A_{V,k}^{(i)}$ 和文本推理步骤优势 $A_{T,k}^{(i)}$，从而避免跨簇的统计分布差异导致的信号压缩。

4. **总优势融合模块**：将稀疏的结果优势 $A_O^{(i)}$ 与分解后的过程优势 $A_{\text{decomposed},k}^{(i)}$ 加权求和，形成最终的步级训练信号：
   $$A_{\text{total},k}^{(i)} = \lambda_O A_O^{(i)} + \lambda_P A_{\text{decomposed},k}^{(i)}$$

### 与基线方法的模块级差异

| 模块 | GRPO / DAPO | PACR | PDCR（本文） |
|------|------------|------|-------------|
| 技能分解 | 无（所有步骤同质） | 无（所有步骤同质） | 基于 Visual Dependence Score + Otsu 的无监督二聚类 |
| 过程优势计算 | 无（仅稀疏结果奖励） | 全局 min-max 归一化 | 分簇 min-max 归一化（视觉簇与文本簇独立缩放） |
| 视觉依赖基线 | 不存在 | 不存在 | 空白图像作为参考，计算对数似然比 |

### 输入输出流

- **输入**：一批视觉-语言推理问题（图像 $\mathbf{I}$ + 问题 $\mathbf{q}$），每组采样 $N$ 条推理轨迹。
- **内部状态**：每条轨迹的逐步置信度 $c_k^{(i)}$、置信度增益 $g_k^{(i)}$、Visual Dependence Score $V_k^{(i)}$、以及 Otsu 阈值 $k^*$ 确定的技能簇分配。
- **输出**：每个推理步骤的最终优势信号 $A_{\text{total},k}^{(i)}$，直接用于策略梯度更新。

训练阶段的额外前向传播（计算置信度增益和视觉依赖分数）带来约 1.5 倍于 GRPO 的计算开销，但推理时模型更高效（Figure 6-b,c,d）。所有实验均在单节点 8×NVIDIA A100 80GB GPU 上，使用 EasyR1 框架和统一的超参数集（Table 6）进行，确保比较公平性。

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/012_Table_6.jpg]]
*Table 6: Key hyperparameters standard to the RLVR framework in EasyR1 library [? ] used for training and evaluation*

### 补充图表

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/001_Figure_1.jpg]]
*Figure 1: Multimodal reasoning mixes two distinct behaviors: seeing (visual perception, extracting evidence from the image) and thinking (textual reasoning over that evidence). Our work argues that these heterogeneous skills must be rewarded independently, as a naive, global reward signal fails to properly assign credit to each*

## 核心模块与公式推导

PDCR 框架由三个关键模块构成：**置信度计算模块**、**无监督技能分解模块**和**感知解耦优势计算模块**，最后通过**总优势融合模块**将稀疏结果信号与分解过程信号整合为统一的步级训练信号（Figure 4）。

### 置信度计算模块

该模块为每个推理步骤计算模型对真实答案的对数概率，并推导步骤间的置信度增益，形成过程奖励信号。给定第 $i$ 条轨迹的第 $k$ 步，模型对真实答案 $Y_{gt}$ 的置信度定义为：

$$c_k^{(i)} = \log \pi_\theta(Y_{gt} \mid \mathbf{I}, \mathbf{q}, H_{\leq k}^{(i)})$$

其中 $\mathbf{I}$ 为输入图像，$\mathbf{q}$ 为问题，$H_{\leq k}^{(i)}$ 为截至第 $k$ 步的推理历史。步骤 $k$ 的置信度增益（即过程奖励）为相邻步骤置信度之差：

$$g_k^{(i)} = c_k^{(i)} - c_{k-1}^{(i)}$$

这一增益反映了该步骤对最终答案置信度的边际贡献，是后续所有过程优势计算的基础。

### 无监督技能分解模块

该模块是 PDCR 的核心创新，旨在自动将推理步骤分为**视觉感知**和**文本推理**两个异质技能簇。

**Visual Dependence Score（视觉依赖分数）**：为量化每个步骤对视觉输入的依赖程度，模块引入一个空白（白色）图像作为参考基线，计算步骤在真实图像与空白图像下的对数概率差：

$$V_k^{(i)} = p_k^{(i)} - p_{w,k}^{(i)}$$

其中 $p_k^{(i)} = \log \pi_\theta(h_k^{(i)} \mid \mathbf{I}, \mathbf{q}, H_{<k}^{(i)})$ 为步骤在真实图像下的对数概率，$p_{w,k}^{(i)}$ 为步骤在空白图像下的对应值。视觉依赖分数越高，表明该步骤越依赖图像中的语义信息，即越可能属于视觉感知步骤。

**Otsu 动态阈值聚类**：获得所有步骤的 $V_k^{(i)}$ 后，模块采用 Otsu 方法自动寻找最优分割阈值，将步骤划分为视觉感知簇和文本推理簇。Otsu 方法通过最小化簇内方差和（SSE）来确定最优分割点 $k^*$：

$$SSE(k) = \sum_{i=1}^{k}(v_i - \mu_1(k))^2 + \sum_{i=k+1}^{M}(v_i - \mu_2(k))^2$$

$$k^* = \arg\min_k SSE(k)$$

其中 $v_i$ 为排序后的视觉依赖分数，$\mu_1(k)$ 和 $\mu_2(k)$ 分别为两个簇的均值。该方法无需任何超参数，在人工标注的验证集上达到 **76.2%** 的分解准确率，显著优于最佳 Top-K 基线的 67.5%（Figure 5）。

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/005_Figure_5.jpg]]
*Figure 5: Our dynamic thresholding (Otsu’s method) is more accurate and robust at decomposing reasoning skills than a naive Top-K baseline. The Top-K method is highly sensitive to the k hyperparameter, peaking at 30%. Our parameter-free dynamic method significantly outperforms even the best Top-K, confirming it’s a superior approach for skill decomposition*

**消融验证**：附录实验进一步证实，信息破坏性的视觉扰动（白图、高斯模糊、高斯噪声）均能达到 75.8%–76.2% 的分解精度，而仅做空间变换的旋转策略效果较差（65.9%），证明破坏语义信息对准确测量视觉依赖性至关重要。

### 感知解耦优势计算模块

在技能分解完成后，该模块在各自技能簇内独立进行 min-max 归一化，生成稳定、良好标度的过程优势信号，从根本上解决了朴素全局归一化导致的混合诱导信号退化问题（Figure 3-(d)）。

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/003_Figure_3.jpg]]
*Figure 3: An illustration of our core observations and the mixture-induced signal degradation problem. (a) A V-L reasoning trace is a heterogeneous mix of visual perception steps and textual reasoning steps. (b) We validate this functional distinction by analyzing attention: perception steps attend highly to visual tokens, while reasoning steps do not. (c) These skills are statistically imbalanced: perception steps are sparse (31.4%), while reasoning steps form the dense majority (68.6%). (d) This imbalance causes mixture-induced signal degradation: (i) a naive, global normalization (Eq. 5) compresses and misaligns the advantage distribution for perception steps. (ii) Our proposed decomposed normaliz...*

对于第 $i$ 条轨迹的第 $k$ 步，其折扣回报定义为：

$$G_k^{(i)} = \sum_{t=k}^{K_i} \gamma^{t-k} g_t^{(i)}$$

其中 $\gamma$ 为折扣因子，$K_i$ 为轨迹总步数。

**视觉感知步骤优势**：仅在视觉感知步骤簇 $\mathbb{Z}_{\text{visual}}$ 内进行归一化：

$$A_{V,k}^{(i)} = \frac{G_k^{(i)} - \min_{(j,k') \in \mathbb{Z}_{\text{visual}}} G_{k'}^{(j)}}{\max_{(j,k') \in \mathbb{Z}_{\text{visual}}} G_{k'}^{(j)} - \min_{(j,k') \in \mathbb{Z}_{\text{visual}}} G_{k'}^{(j)}}$$

**文本推理步骤优势**：仅在文本推理步骤簇 $\mathbb{Z}_{\text{textual}}$ 内进行归一化：

$$A_{T,k}^{(i)} = \frac{G_k^{(i)} - \min_{(j,k') \in \mathbb{Z}_{\text{textual}}} G_{k'}^{(j)}}{\max_{(j,k') \in \mathbb{Z}_{\text{textual}}} G_{k'}^{(j)} - \min_{(j,k') \in \mathbb{Z}_{\text{textual}}} G_{k'}^{(j)}}$$

分簇归一化的关键优势在于：视觉感知步骤仅占全部推理步骤的 **31.4%**，而文本推理步骤占 **68.6%**（Figure 3-(c)），形成严重的统计不平衡。朴素的全局归一化（如 PACR 的 Eq. 5）会压缩视觉步骤的优势分布，使其信号被占多数的文本步骤淹没；而分簇归一化使每种技能在各自统计分布内得到公平的比较和正确的标度。

### 总优势融合模块

最终的步级训练信号由稀疏的结果优势与分解的过程优势加权求和得到：

$$A_{total,k}^{(i)} = \lambda_O A_O^{(i)} + \lambda_P A_{decomposed,k}^{(i)}$$

其中 $A_O^{(i)}$ 为基于最终答案正确性的稀疏结果优势（组内 z-score 归一化），$A_{decomposed,k}^{(i)}$ 为分簇归一化后的过程优势（视觉步骤使用 $A_{V,k}^{(i)}$，文本步骤使用 $A_{T,k}^{(i)}$）。$\lambda_O$ 和 $\lambda_P$ 为控制两类信号权重的超参数，用于平衡稀疏终端奖励与密集过程奖励的贡献。

### 补充图表

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/002_Figure_2.jpg]]
*Figure 2: The baseline dense reward pipeline. For N rollouts, a sparse Outcome Reward*

## 实验与分析

### 主要实验结果

PDCR在Qwen2.5-VL-7B骨干上对七个视觉-语言推理基准进行了系统评估。如表1所示，PDCR以**52.9**的平均准确率超过所有基线方法，包括稀疏奖励GRPO（51.5）、稳定化稀疏奖励DAPO（51.7）和朴素密集奖励PACR（52.2），实现了**+0.7**的平均提升。在Qwen2.5-VL-3B骨干上，PDCR同样以**45.2**的平均准确率保持领先，验证了该方法在不同模型规模下的一致性。

具体到各基准，PDCR在MMMU-Pro上达到**42.5**（+1.0 vs PACR），在MMMU上达到**51.5**（+1.0 vs PACR），在HallusionBench上达到**68.4**（+0.8 vs PACR），在MathVista上达到**62.3**（+0.6 vs PACR）。这些基准覆盖了学科知识推理、幻觉检测和数学推理等异构任务，PDCR的全面改进表明分解式奖励结构对不同任务类型具有普遍增益。在Qwen3-VL-8B-Instruct骨干上（Table 3），PDCR平均准确率达到**57.0**，进一步验证了方法在更强基础模型上的有效性。

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/009_Table_3.jpg]]
*Table 3: Experimental results on the Qwen3-VL-8B-Instruct backbone. We report the accuracy across seven evaluation benchmarks. We compare our method, PDCR (ours), against strong baselines, including sparse-reward (GRPO), stabilized (DAPO), and naive dense-reward (PACR) methods. The best score in each column is in bold, and the second-best is underlined*

### 消融实验

#### 技能分解的必要性

为验证有意义的技能分解对性能的贡献，我们进行了随机分解消融实验（Table 2）。将基于Visual Dependence Score的无监督聚类替换为随机分配后，Qwen2.5-VL-7B上的平均准确率从**52.9**下降至**52.3**，Qwen2.5-VL-3B上从**45.2**下降至**44.7**。这一退化明确证明：仅仅在统计上实施簇内归一化并不足够，**基于视觉依赖性的语义分解**才是性能提升的关键来源。

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/007_Table_2.jpg]]
*Table 2: Ablation study on the efficacy of skill decomposition. We compare our full PDCR method against a Random Decomposition baseline. This baseline randomly assigns steps to the visual or textual cluster before applying decomposed normalization. The clear performance gap validates that our data-driven Visual Dependence Score provides a meaningful decomposition, and that simply decomposing the reward is not sufficient*

#### 动态阈值 vs Top-K基线

Figure 5对比了Otsu动态阈值方法与Top-K固定比例方法的分解准确率。Top-K方法在最佳K值下达到峰值**67.5%**，而Otsu方法达到**76.2%**，且无需任何超参数调优。这一显著差距说明，推理步骤中视觉感知与文本推理的比例在不同问题间存在较大差异，固定比例假设无法适应这种异质性，而数据驱动的动态阈值能够自适应地捕获每个轨迹的技能边界。

#### 视觉扰动策略的影响

附录中的扰动消融（Section 17）揭示了视觉依赖性测量的关键设计原则。白图、高斯模糊和高斯噪声三种信息破坏策略均达到**75.8%–76.2%**的分解精度，而空间变换（旋转）仅达到**65.9%**。这一结果表明，**破坏语义信息**是测量视觉依赖性的必要条件——旋转虽然改变了视觉输入，但保留了大部分语义内容，导致模型仍能从中提取有用信息，从而低估了步骤的真实视觉依赖性。

### 训练动态与效率分析

Figure 6(a)展示了训练曲线对比：PDCR（粉色）不仅收敛速度更快，而且最终达到更高的准确率平台。这一加速收敛特性源于分解式优势信号为视觉步骤提供了更稳定、更准确的梯度方向。

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/008_Figure_6.jpg]]
*Figure 6: Training dynamics, cost, and efficiency comparison. (a) Our PDCR method (pink) converges faster and to a higher final accuracy than all baselines. (b) This improved performance comes at an expected, higher computational cost per training step. (c) & (d) This training cost is offset by a significant gain in inference-time efficiency (c). As shown in (d), this efficiency gain is driven by the fact that both PDCR and PACR learn to produce substantially shorter and more concise reasoning traces over time compared to GRPO*

然而，这种性能提升伴随着可预期的训练成本增加（Figure 6(b)）。PDCR需要额外的前向传播来计算置信度增益和Visual Dependence Score，导致每训练步的计算开销约为GRPO的**1.5倍**。值得注意的是，Figure 6(c,d)显示PDCR训练出的模型在推理阶段反而更高效——在达到相同准确率时，PDCR模型生成的推理链更短、推理速度更快，表明分解式奖励训练有助于模型学习更精准的推理策略。

### 技能分解的定性验证

Table 5提供了技能分解的定性示例。被标注为视觉感知的步骤通常涉及直接从图像中提取实体、属性和空间关系（如“The image shows a red car on the left”），而被标注为文本推理的步骤则涉及基于已提取信息的逻辑推演（如“Since the car is red and on the left, the answer must be...”）。Table 4报告了标注者间一致性评分（Cohen's κ > 0.75），验证了人工标注标签的可靠性，为Otsu方法的评估提供了可信的参考标准。

### 失败模式与局限性

尽管PDCR在整体上表现优异，仍存在以下已知局限：

1. **混合步骤处理不足**：PDCR假设每个步骤可被硬分类为视觉感知或文本推理，但实际中存在同时需要密集视觉检查和复杂逻辑推理的混合步骤（如复杂空间关系推理）。当前二元聚类无法为这类步骤提供精细化的奖励标度。

2. **训练成本瓶颈**：额外前向传播带来的1.5倍训练开销限制了PDCR在更大规模训练中的应用。能否通过内部激活近似方法获取置信度分数，从而避免额外前向传播，是一个重要的开放问题。

3. **分解粒度的限制**：当前方法仅支持两类技能分解。对于更细粒度的技能类型（如视觉定位、属性识别、数值推理、常识推理等），软聚类或多类分解可能进一步提升奖励质量，这有待未来工作探索。

### 补充图表

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/006_Table_1.jpg]]
*Table 1: Main results on V-L reasoning benchmarks. We report the accuracy across seven evaluation benchmarks. We compare our method, PDCR (ours), against strong baselines, including sparse-reward (GRPO), stabilized (DAPO), and naive dense-reward (PACR) methods. The best score in each column is in bold, and the second-best is underlined*

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/011_Table_5.jpg]]
*Table 5: Qualitative Examples of Skill Decomposition. We show examples of steps that we labeled as Visual Perception or Textual Reasoning. This separation illustrates the heterogeneous nature of the V-L reasoning task*

![[assets/figures/papers/paper_list_l2661_https_arxiv_org_abs_2605_13467/figures/017_Figure_7.jpg]]
*Figure 7: Visual Perturbation Strategies Evaluated for Skill Decomposition. To calculate the Visual Dependence Score (V (i)k , Eq. 7) , we compare the model’s probability on the (a) Original image against four baselines: (b) White (Strategy adopted in main text), (c) Gaussian Blur, (d) Gaussian Noise, and (e) Rotate. Our analysis confirms that strategies which effectively destroy semantic information (b, c, d) yield high decomposition accuracy, whereas simple spatial transformation (e) preserves the visual content, leading to poor separation*

## 方法谱系与知识库定位

### 1. 方法定位：从稀疏奖励到感知解耦的密集奖励

PDCR 处于**多模态推理的过程奖励优化**这一研究脉络中，其直接前身是稀疏奖励的 GRPO 和密集奖励的 PACR。现有方法的核心瓶颈在于：视觉-语言推理步骤天然由功能异质、统计分布不同的两类技能构成——视觉感知步骤仅占全部步骤的 31.4%（Figure 3-c），而文本推理步骤占 68.6%。朴素的全局归一化（如 PACR 的 Eq. 5）将所有步骤的置信度增益在同一尺度下进行 min-max 缩放，导致少数派视觉步骤的优势信号被多数派文本步骤压缩和错配，产生**混合诱导的信号退化**（Figure 3-d）。

PDCR 的关键创新在于**技能分解 + 分簇归一化**的双阶段设计：
1. **无监督技能分解**：引入模型内部的 Visual Dependence Score（Eq. 7: $V_k^{(i)} = p_k^{(i)} - p_{w,k}^{(i)}$），通过对比原图与空白图像下的对数概率来量化每个步骤对视觉输入的依赖程度，再结合 Otsu 动态阈值实现无超参数的最优二分类。
2. **感知解耦优势计算**：仅在视觉感知簇或文本推理簇内部进行 min-max 归一化（Eq. 12, 13），确保每种技能获得稳定、正确标度的训练信号。

最终的总优势信号（Eq. 14: $A_{total,k}^{(i)} = \lambda_O A_O^{(i)} + \lambda_P A_{decomposed,k}^{(i)}$）融合了稀疏结果优势和分解过程优势，形成步级信用分配。

### 2. 与相关工作的关系

#### 2.1 稀疏奖励基线：GRPO 与 DAPO

**GRPO**（Group Relative Policy Optimization）是稀疏奖励的代表方法，仅在轨迹终点根据答案正确性给出二元奖励（$R^{(i)} \in \{0, 1\}$），并通过组内归一化计算优势（$A_O^{(i)}$）。其根本局限在于缺乏过程监督，导致信用分配困难——模型无法区分推理链中哪些步骤对最终结果有贡献。

**DAPO** 在 GRPO 基础上引入动态采样策略以缓解奖励方差消失问题，但本质上仍属于稀疏奖励范式，未解决过程信用分配问题。PDCR 在 DAPO 的稳定化基础上叠加了密集过程奖励，形成互补。

#### 2.2 密集奖励基线：PACR

**PACR**（Progressively Ascending Confidence Reward）是 PDCR 最直接的对比基线。PACR 通过计算模型对真实答案的对数概率的逐步增益（Eq. 4: $g_k^{(i)} = c_k^{(i)} - c_{k-1}^{(i)}$）来构造步级密集奖励，但其全局 min-max 归一化（Eq. 5）将所有步骤视为同质，这正是 PDCR 要解决的核心问题。

PDCR 对 PACR 的改进是结构性的：保留置信度增益的计算框架，但将归一化操作从全局空间迁移到技能簇内部。这一改动使得视觉感知步骤的优势不再被文本步骤的分布淹没。

#### 2.3 技能分解的独特性

PDCR 的技能分解策略与传统的基于注意力或梯度的可解释性方法不同：
- **无需外部标注**：Visual Dependence Score 完全基于模型内部的前向传播计算，不依赖人工标注的技能标签。
- **信息破坏是关键**：消融实验（Appendix Section 17）表明，有效破坏视觉语义的扰动策略（白图、高斯模糊、高斯噪声）均能达到 75.8%–76.2% 的分解精度，而仅做空间变换（旋转）效果显著下降（65.9%），证明测量视觉依赖性需要语义层面的信息破坏，而非简单的空间扰动。
- **无超参数**：Otsu 动态阈值化在分解准确率上达到 76.2%，显著优于最佳 Top-K 基线的峰值 67.5%（Figure 5），且无需手动调节 k 值。

### 3. 适用边界与局限

#### 3.1 计算开销

PDCR 在训练阶段需要额外的前向传播来计算置信度增益和 Visual Dependence Score，导致单步训练成本约为 GRPO 的 1.5 倍（Figure 6-b）。尽管推理时模型更高效（Figure 6-c, d），这一训练开销在资源受限场景下可能成为瓶颈。

#### 3.2 硬二分类假设

PDCR 假设视觉-语言推理步骤可硬分为视觉感知和文本推理两类。对于既需要密集视觉感知又包含复杂逻辑推理的混合步骤（如复杂空间推理），二元聚类的刚性划分可能导致部分步骤被错误归类，影响奖励质量。当前方法不支持软聚类或细粒度多类分解。

#### 3.3 对空白图像参考的依赖

Visual Dependence Score 的计算依赖空白（白色）图像作为视觉基线。虽然实验表明多种信息破坏策略均有效，但在实际部署中需要为每个样本额外执行一次带空白图像的前向传播，增加了计算开销。不同视觉扰动策略在不同任务上的泛化性仍需进一步验证。

### 4. 开放问题

1. **内部激活近似**：能否通过分析模型内部激活模式（如注意力分布或隐藏状态）来近似 Visual Dependence Score，从而完全避免额外的前向传播，缩小与 GRPO 的训练成本差距？

2. **软聚类与多类分解**：对于混合型步骤，引入软聚类机制或扩展到多于两类的技能分解（如区分低级视觉特征提取、高级语义理解、逻辑推理等）能否进一步提升奖励质量和训练效果？

3. **跨架构泛化**：PDCR 当前在自回归 VLM（Qwen2.5-VL、Qwen3-VL）上验证，其在非自回归架构、更大规模模型以及其他多模态任务（如视频理解、文档解析）上的泛化能力尚待探索。

4. **技能分解的动态性**：随着 RL 训练的推进，模型的技能分布可能发生变化——某些步骤的视觉依赖性可能减弱或增强。静态的 Otsu 阈值是否需要在训练过程中动态更新，以适应模型能力的演变？

5. **与过程奖励模型（PRM）的关系**：PDCR 使用模型自身的置信度作为过程奖励，而 PRM 方法训练独立模型来评估步骤质量。两者在信用分配精度和计算成本上的权衡关系值得深入研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/PDCR_Perception_Decomposed_Confidence_Reward_for_Vision_Language_Reasoning.pdf]]