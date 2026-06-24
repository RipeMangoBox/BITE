---
title: "Activation Matters: Test-time Activated Negative Labels for OOD Detection with Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Activation_Matters_Test_time_Activated_Negative_Labels_for_OOD_Detection_with_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/YBZh/OpenOOD-VLM"
aliases:
- TTANLT
- AMTTANLODVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过测试时在线估计语料库中每个标签在正（ID）负（OOD）样本上的激活差异，动态选择高激活的负标签，并采用激活感知评分函数隐式增强高激活标签的权重，从而提升OOD检测。
primary_logic: 负标签在OOD数据集上的激活水平是影响检测性能的关键因素；通过测试时自适应挖掘激活更强的负标签，并利用激活信息设计评分函数，可显著提高OOD检测的准确性和鲁棒性。
claims:
- 负标签在OOD数据集上的激活呈长尾分布，许多标签在ID上激活更高，误导检测。
- 移除低激活的负标签可降低FPR95，提高检测性能。
- 所提出的TANL在ImageNet-1k上平均FPR95为9.81%，相比NegLabel的25.40%大幅降低。
- 激活感知评分函数增强了性能，并提高了对负标签数量的鲁棒性。
---

# Activation Matters: Test-time Activated Negative Labels for OOD Detection with Vision-Language Models

> [!tip] 核心洞察
> 负标签在OOD数据集上的激活水平是影响检测性能的关键因素；通过测试时自适应挖掘激活更强的负标签，并利用激活信息设计评分函数，可显著提高OOD检测的准确性和鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 激活至关重要：面向视觉-语言模型的测试时激活负标签用于OOD检测 |
| 英文题名 | Activation Matters: Test-time Activated Negative Labels for OOD Detection with Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.25250) · [Code](https://github.com/YBZh/OpenOOD-VLM) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Test-time Activated Negative Labels (TANL) |
| Dataset | ImageNet-1k, OpenOOD Near-OOD, OpenOOD Far-OOD, Full-spectrum OOD |

> [!tip] 效果简介
> - ImageNet-1k (4 OOD datasets: iNaturalist, SUN, Places, Textures) 上，Average FPR95 (↓) 9.81 vs 25.40 (NegLabel) (-15.59)。
> - ImageNet-1k (4 OOD datasets) 上，Average AUROC (↑) 97.97 vs 94.21 (NegLabel) (+3.76)。
> - OpenOOD Near-OOD (SSB-hard, NINCO) 上，FPR95 (↓) 60.06 vs 69.45 (NegLabel) (-9.39)。

## 概述

**问题瓶颈**：现有基于负标签的视觉-语言模型 OOD 检测方法（如 NegLabel）从语料库中选取与 ID 标签语义距离最远的词语作为负标签。然而，这些负标签在特定 OOD 测试集上的激活水平呈长尾分布——大量标签激活极低，甚至部分标签在 ID 样本上的激活强于 OOD 样本，从而引入检测噪声、误导 OOD 判别（图 1）。

**核心思路**：本文提出 **测试时激活负标签（Test-time Activated Negative Labels, TANL）**，其关键洞察是：负标签在 OOD 数据上的激活水平是决定检测性能的核心因素。TANL 在测试过程中在线估计语料库中每个候选标签在正（ID）与负（OOD）样本上的激活差异，动态选取高激活负标签，并设计激活感知评分函数（activation-aware score）隐式增强高激活标签的权重。

**方法定位**：TANL 属于训练自由的测试时自适应方法，无需额外训练参数。与直接基线 NegLabel 相比，TANL 在三个关键维度上做出改进：（1）负标签选择标准从“与 ID 标签的余弦距离”转变为“测试时激活差异度量”；（2）评分函数从所有负标签等权求和转变为按激活排序的循环累加，使高激活标签在分母中出现更频繁；（3）引入 FIFO 队列缓存高置信度样本，实现分布自适应与批次自适应，动态更新激活估计。

**主要结果**：在 ImageNet-1k 基准上，TANL 将平均 FPR95 从 NegLabel 的 25.40% 降至 **9.81%**（↓15.59），AUROC 从 94.21% 提升至 **97.97%**（↑3.76）。在 OpenOOD 设置的 Near-OOD 和 Far-OOD 场景下，FPR95 分别降低 9.39 和 6.52 个百分点。消融实验表明，分布自适应、批次自适应和激活感知评分三者均带来显著增益，且方法对负标签数量具有较强鲁棒性。

**局限与开放问题**：方法依赖语料库覆盖 OOD 相关词语且预训练文本编码器能理解这些词语，在医学等专业领域可能受限；测试初期若缓存队列误分类率过高（>80%），自适应可能带来负面影响。后续可探索更精细的显式加权方案、专业领域语料库构建，以及极端数据流下的性能维持能力。

## 背景与动机

### 视觉-语言模型与OOD检测的兴起

分布外（Out-of-Distribution, OOD）检测旨在识别与训练分布不同的测试样本，是保障深度学习模型安全部署的关键技术。近年来，大规模视觉-语言模型（Vision-Language Models, VLMs）如CLIP的涌现，为OOD检测开辟了新的范式。这类模型通过大规模图文对比预训练，获得了强大的开放世界语义理解能力，使得无需在特定ID数据集上进行额外训练即可进行OOD检测成为可能。

### 负标签方法的瓶颈：激活不足与噪声干扰

在众多训练自由的VLM OOD检测方法中，基于负标签（negative labels）的方法展现出了显著优势。其核心思想是：在预定义的语料库中，选取与ID标签语义距离远的词语作为负标签，然后通过计算测试图像与ID标签及负标签的相似度，综合判断样本是否属于ID分布。代表性工作**NegLabel**即采用此范式，通过余弦距离从WordNet等语料库中选取最远的标签作为负标签。

然而，这一看似合理的策略存在一个被忽视的关键缺陷：**负标签在OOD样本上的实际激活水平可能极低，甚至部分标签在ID样本上的激活反而更强**。如Figure 1所示，针对特定OOD数据集，现有方法挖掘的负标签呈现出显著的长尾激活分布——仅有极少部分标签在OOD上被强激活，而相当数量的标签在ID上的激活程度更高，直接误导检测。从机制上看，当负标签在OOD图像上的归一化相似度（即激活分数）低于在ID图像上时，增加这些标签反而会提升误检率（FPR），这与引入负标签的初衷背道而驰。

### 核心洞察与本文动机

上述分析揭示了一个根本性洞见：**负标签的选择不应仅依赖于与ID标签的静态语义距离，而必须考虑其在测试分布上的动态激活水平**。理想的负标签应满足两个条件：在OOD样本上激活强，在ID样本上激活弱。这构成了激活差异（activation difference）的核心度量：

$$
\widehat{Act}_d(\widehat{y_i}) = Act(\mathcal{X}_{neg}, \widehat{y_i}) - Act(\mathcal{X}_{pos}, \widehat{y_i})
$$

其中激活分数定义为标签在样本集上的平均归一化相似度：

$$
Act(\mathcal{X}, \widehat{y}_i) = \frac{1}{|\mathcal{X}|} \sum_{x \in \mathcal{X}} \frac{\exp(\pmb{v} \widehat{t}_i)}{\sum_{j=1}^{C} \exp(\pmb{v} t_j) + \sum_{j=1}^{N} \exp(\pmb{v} \widehat{t}_j)}
$$

基于此，本文提出**测试时激活负标签（Test-time Activated Negative Labels, TANL）**方法。其核心动机是：在测试过程中，通过在线识别高置信度的正（ID）样本和负（OOD）样本，动态估计语料库中每个候选标签的激活差异，从而自适应地选择在当前测试分布下激活最强的负标签。此外，本文进一步设计了激活感知评分函数，按激活强度对负标签排序后循环累加，隐式增强高激活标签的权重，从而充分利用挖掘到的激活知识，提升OOD检测的准确性和鲁棒性。

## 核心创新

TANL 的核心创新在于揭示并利用了一个被现有负标签方法忽视的关键现象：**负标签在 OOD 样本上的激活水平是决定检测性能的瓶颈因素**。基于此洞察，TANL 在三个维度上对 NegLabel 基线进行了系统性改造。

### 创新一：从“语义距离”到“测试时激活差异”的负标签选择范式

NegLabel 采用静态的负标签选择策略——从语料库中选取与 ID 标签余弦距离最远的词语作为负标签。这种选择方式完全依赖 ID 标签的语义空间，与测试时实际遇到的 OOD 分布脱节。TANL 的核心发现是：**许多距离远的负标签在特定 OOD 测试集上激活程度极低，甚至部分标签在 ID 样本上的激活反而更强**（如 Figure 1 所示，负标签激活呈长尾分布，低激活标签会引入检测噪声）。

TANL 将选择标准从“语义距离”替换为“测试时激活差异”：

- **激活度量**：定义标签 $\widehat{y}_i$ 在数据集 $\mathcal{X}$ 上的激活分数为所有样本对该标签的平均归一化相似度（Eq. 5），即标签在数据集上的“软分配概率”。
- **差异选择**：通过在线估计每个候选标签在正（ID）样本和负（OOD）样本上的激活差异 $\widehat{Act}_d(\widehat{y}_i)$（Eq. 8），从语料库中动态选取激活差异最大的 $M$ 个标签作为负标签（Eq. 6）。

这一转变的理论支撑来自 Eq. 16 的推导：增加负标签数量 $M$ 能降低 FPR 的条件是 $p_1 - p_2 < 0$，即负标签在 OOD 上的相似度必须高于在 ID 上的相似度。TANL 通过激活差异选择天然满足这一条件，而 NegLabel 的语义距离选择无法保证。

### 创新二：测试时自适应队列机制实现在线激活估计

由于测试时无法获取真实 OOD 分布，TANL 设计了 **FIFO 队列缓存机制**来在线近似激活差异：

- **队列初始化**（Eq. 10）：使用 ID 标签特征和噪声图像特征分别初始化正样本队列 $\mathcal{X}_{pos}$ 和负样本队列 $\mathcal{X}_{neg}$，保证测试起始阶段的稳定性。
- **动态更新**（Eq. 9）：根据当前激活感知分数 $S_{aa}$ 筛选高置信度样本，持续更新队列。仅需约 20% 的初始精度即可实现正向自适应改进。
- **批次自适应增强**（Eq. 11–14）：融合历史队列和当前批次的激活估计，通过加权混合（Eq. 13）实现更细粒度的标签选择，进一步提升对局部批次分布的适应性。

消融实验（Table 4）验证了这一设计的有效性：仅引入分布自适应（Dis-adapt）就将 Near-OOD FPR95 从 NegLabel 的 69.45 降至 63.55；进一步增加批次自适应（Batch-adapt）降至 61.44。

### 创新三：激活感知评分函数实现隐式加权

NegLabel 的评分函数对所有负标签赋予相同权重，无法区分高激活标签和低激活标签的贡献差异。TANL 提出了 **激活感知评分函数** $S_{aa}$（Eq. 15）：

$$S_{aa}(\pmb{v}) = \frac{1}{M} \sum_{m=1}^{M} \sum_{i=1}^{C} \frac{\exp(\pmb{v} t_i)}{\sum_{j=1}^{C} \exp(\pmb{v} t_j) + \sum_{j=1}^{m} \exp(\pmb{v} \widetilde{t}_j)}$$

其核心机制是：将负标签按激活强度排序后，通过循环累加的方式逐次将更多负标签加入分母。激活越强的标签排序越靠前，在 $M$ 次累加中出现的频次越高，从而在分母中占据更大比重——这实现了对高激活标签的**隐式加权**，无需引入额外参数。

消融实验（Table 4）表明，加入激活感知评分（AAScore）后，Near-OOD FPR95 进一步降至 60.06。同时，该评分函数显著增强了对负标签数量 $M$ 的鲁棒性——在较大范围内性能保持稳定（Fig. 3a），而 NegLabel 对 $M$ 的选择较为敏感。

### 创新总结

| 改造维度 | NegLabel（基线） | TANL（本文） | 关键机制 |
|---------|-----------------|-------------|---------|
| 负标签选择标准 | 基于 ID 标签余弦距离 | 基于测试时激活差异 | Eq. 6–8，满足 $p_1-p_2<0$ 条件 |
| 测试时适应性 | 无（固定标签） | FIFO 队列 + 批次自适应 | Eq. 9–14，在线更新激活估计 |
| 评分函数 | 等权 softmax 求和 | 激活感知循环累加 | Eq. 15，隐式增强高激活标签权重 |

三项创新协同作用，使 TANL 在 ImageNet-1k 上将平均 FPR95 从 NegLabel 的 25.40% 大幅降至 9.81%，AUROC 从 94.21 提升至 97.97（Table 1）。

## 整体框架

TANL 的整体工作流围绕一个核心闭环展开：**测试时在线估计候选负标签的激活差异 → 动态选取高激活负标签 → 激活感知评分 → 缓存高置信度样本以更新激活估计**。该闭环使得负标签的选择不再依赖静态的 ID 距离，而是持续适配当前测试分布的真实激活模式。

### 框架总览

整个 pipeline 由六个功能模块串联而成，其输入输出关系如 Figure 2 所示：

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of TANL. We dynamically explore activated negative labels from the corpus dataset in the testing process, where the activation information is measured based on the similarity between texts and the mined positive/negative images. The activation-aware score is illustrated as a simplified example of Eq. 15 with M = 2 and C = 2*

1. **语料库构建模块**：预先定义候选负标签集合 $\mathcal{Y}^{cor}$（如 WordNet 名词集），作为标签搜索空间。
2. **特征提取模块**：使用冻结的 CLIP 图像编码器和文本编码器，分别提取测试图像特征 $\mathbf{v}$、ID 标签文本特征 $\mathbf{t}_i$ 以及语料库标签文本特征 $\widehat{\mathbf{t}}_i$。
3. **激活估计模块**：维护两个固定长度的 FIFO 队列 $\mathcal{X}_{pos}$ 和 $\mathcal{X}_{neg}$，分别缓存高置信度的 ID 和 OOD 图像特征。对每个候选标签 $\widehat{y}_i$，在线计算其在正/负队列上的激活分数 $Act(\mathcal{X}_{pos}, \widehat{y}_i)$ 和 $Act(\mathcal{X}_{neg}, \widehat{y}_i)$，进而得到近似激活差异 $\widehat{Act}_d(\widehat{y}_i)$（式 8）。
4. **自适应标签选择模块**：根据 $\widehat{Act}_d(\widehat{y}_i)$ 对语料库中所有候选标签排序，选取 top-$M$ 个激活差异最大的标签作为当前测试批次的负标签集 $\mathcal{V}^-$（式 6）。批次自适应变体进一步融合当前批次的高置信度样本激活（式 11–14）。
5. **激活感知评分模块**：将选取的负标签按激活从高到低排序后，通过循环累加方式计算激活感知分数 $S_{aa}(\mathbf{v})$（式 15）——高激活标签在更多累加步中出现于分母，从而隐式获得更高权重。
6. **队列更新模块**：依据当前 $S_{aa}$ 分数筛选高置信度样本，更新 $\mathcal{X}_{pos}$ 和 $\mathcal{X}_{neg}$ 队列（式 9），为后续批次的激活估计提供更准确的统计基础。

### 关键设计要点

**冷启动处理**：测试初期队列为空，TANL 使用 ID 标签特征和随机噪声图像特征分别初始化正/负队列（式 10），保证起始阶段即可进行有效的标签选择。

**双级自适应机制**：
- *分布自适应（Dis-adapt）*：仅依赖历史队列的累积激活统计，适合稳定数据流。
- *批次自适应（Batch-adapt）*：通过加权融合历史队列和当前批次的高置信度样本激活（式 13），对分布偏移更敏感。

**激活感知评分的理论支撑**：推导表明（式 16），增加负标签数量 $M$ 能降低 FPR 的前提是 $p_1 - p_2 < 0$，即负标签在 OOD 上的归一化相似度高于在 ID 上。激活差异度量正是对这一条件的直接近似，从而为标签选择提供了原则性依据。

## 核心模块与公式推导

### 3.1 问题形式化与基线回顾

给定一张测试图像，其CLIP图像特征为 $\pmb{v}$，ID类别文本特征为 $\{t_i\}_{i=1}^{C}$，候选语料库标签文本特征为 $\{\widehat{t}_i\}_{i=1}^{N}$。零样本分类下，图像属于ID类别 $i$ 的概率为：

$$p_i^{id} = \frac{\exp(\pmb{v} t_i)}{\sum_{j=1}^{C} \exp(\pmb{v} t_j)}$$

NegLabel基线方法在此基础上引入负标签：从语料库中选取与所有ID标签余弦距离最远的 $M$ 个标签作为负标签集合 $\mathcal{V}^{-}$，然后计算OOD检测分数：

$$S(\pmb{v}) = \sum_{i=1}^{C} \frac{\exp(\pmb{v} t_i)}{\sum_{j=1}^{C} \exp(\pmb{v} t_j) + \sum_{j=1}^{M} \exp(\pmb{v} \widetilde{t}_j)}$$

其中 $\widetilde{t}_j \in \mathcal{V}^{-}$。该分数的核心逻辑是：若图像为ID样本，其与ID标签的相似度较高，分母中加入负标签后影响有限；若为OOD样本，与所有ID标签相似度均低，负标签的加入会显著压低分数。

**瓶颈分析**：NegLabel的负标签选择仅依赖与ID标签的距离，完全忽略测试分布。如Figure 1所示，许多被选中的负标签在特定OOD测试集上激活程度极低，甚至部分标签在ID样本上的激活更强，反而引入噪声、误导检测。

### 3.2 激活度量与自适应标签选择

TANL的核心创新在于用**激活差异**替代**语义距离**作为负标签选择标准。

**定义1（激活分数）**：标签 $\widehat{y}_i$ 在图像集合 $\mathcal{X}$ 上的激活分数为该标签在所有图像上的平均归一化相似度（软分配概率）：

$$Act(\mathcal{X}, \widehat{y}_i) = \frac{1}{|\mathcal{X}|} \sum_{x \in \mathcal{X}} \frac{\exp(\pmb{v} \widehat{t}_i)}{\sum_{j=1}^{C} \exp(\pmb{v} t_j) + \sum_{j=1}^{N} \exp(\pmb{v} \widehat{t}_j)}$$

**定义2（理想激活差异）**：标签 $\widehat{y}_i$ 的判别力由其OOD激活与ID激活之差度量：

$$Act_d(\widehat{y}_i) = Act(\mathcal{X}_{ood}, \widehat{y}_i) - Act(\mathcal{X}_{id}, \widehat{y}_i)$$

该差异越大，表明标签在OOD样本上响应越强、在ID样本上响应越弱，越有利于区分两类样本。

**测试时近似**：由于测试时无法获取真实的 $\mathcal{X}_{id}$ 和 $\mathcal{X}_{ood}$，TANL使用FIFO队列缓存高置信度样本进行在线估计：

$$\widehat{Act}_d(\widehat{y}_i) = Act(\mathcal{X}_{neg}, \widehat{y}_i) - Act(\mathcal{X}_{pos}, \widehat{y}_i)$$

其中 $\mathcal{X}_{pos}$ 和 $\mathcal{X}_{neg}$ 分别为缓存的正样本（高置信ID）和负样本（高置信OOD）特征队列。最终按 $\widehat{Act}_d$ 降序从语料库中选取Top-$M$标签：

$$\mathcal{V}^{-} = Top(\{\widehat{Act}_d(\widehat{y}_i)\}_{i=1}^{N}, \mathcal{Y}^{cor}, M)$$

### 3.3 FIFO队列更新机制

队列的维护是自适应能力的关键。对于每个测试批次 $\mathcal{B}$，根据当前激活感知分数 $S_{aa}(\pmb{v})$ 筛选高置信样本：

$$\mathcal{X}_{pos} = \mathrm{Update}(\mathcal{X}_{pos}, \{ \pmb{v} \in \mathcal{B} \mid S_{aa}(\pmb{v}) \geq \gamma + (1-\gamma)g \}, L)$$

其中 $\gamma$ 为OOD检测阈值，$g$ 为当前批次中分数超过 $\gamma$ 的比例，$L$ 为队列容量。该设计使队列能动态适应数据流中的分布变化。

**队列初始化**：测试启动时队列为空，TANL使用ID标签文本特征作为正队列初始值、随机噪声图像特征作为负队列初始值，保证冷启动阶段的稳定性。

### 3.4 批次自适应增强

为进一步利用当前批次的细粒度信息，TANL提出批次自适应变体，将历史队列激活与当前批次激活进行融合：

$$Act_b(\mathcal{X}_{pos}, \widehat{y}_i) = \alpha Act(\mathcal{X}_{pos}, \widehat{y}_i) + (1-\alpha) Act(\mathcal{X}_{pos}^b, \widehat{y}_i)$$

$$Act_b(\mathcal{X}_{neg}, \widehat{y}_i) = \alpha Act(\mathcal{X}_{neg}, \widehat{y}_i) + (1-\alpha) Act(\mathcal{X}_{neg}^b, \widehat{y}_i)$$

其中 $\mathcal{X}_{pos}^b$ 和 $\mathcal{X}_{neg}^b$ 为当前批次中筛选的高置信正/负样本，$\alpha \in [0,1]$ 控制历史信息的权重。融合后的激活差异为：

$$\widehat{Act}_b(\widehat{y}_i) = Act_b(\mathcal{X}_{neg}, \widehat{y}_i) - Act_b(\mathcal{X}_{pos}, \widehat{y}_i)$$

### 3.5 激活感知评分函数

选定负标签后，TANL不采用等权求和，而是设计激活感知评分函数以隐式增强高激活标签的影响。将选定的负标签按激活差异降序排列为 $\widetilde{t}_1, \widetilde{t}_2, \ldots, \widetilde{t}_M$（即 $\widehat{Act}(\widetilde{t}_1) \geq \widehat{Act}(\widetilde{t}_2) \geq \cdots$），评分函数定义为：

$$S_{aa}(\pmb{v}) = \frac{1}{M} \sum_{m=1}^{M} \sum_{i=1}^{C} \frac{\exp(\pmb{v} t_i)}{\sum_{j=1}^{C} \exp(\pmb{v} t_j) + \sum_{j=1}^{m} \exp(\pmb{v} \widetilde{t}_j)}$$

**机制解析**：该函数通过循环累加排序后的负标签实现隐式加权——激活最强的标签 $\widetilde{t}_1$ 出现在所有 $M$ 项的分母中，而激活最弱的标签 $\widetilde{t}_M$ 仅出现在最后一项。这种设计使高激活标签对分数的压制作用更强，且无需引入额外可学习参数。

### 3.6 理论支撑

TANL从理论上分析了增加负标签数量 $M$ 对FPR的影响。在独立同分布假设下，FPR对 $M$ 的偏导数为：

$$\frac{\partial FPR_{\lambda}}{\partial M} = \frac{e^{-z^2}}{2\sqrt{2\pi}} \cdot \frac{p_1 - p_2}{\sqrt{M p_2 (1-p_2)}}$$

其中 $p_1$ 和 $p_2$ 分别表示负标签在OOD和ID样本上的期望相似度。**降低FPR的充要条件为 $p_1 - p_2 < 0$**，即负标签在OOD上的相似度高于在ID上。这从理论上解释了为何应选择激活差异大的标签：$Act_d(\widehat{y}_i)$ 正是对 $p_1 - p_2$ 的经验估计，选择高 $Act_d$ 标签等价于最大化FPR下降的幅度。

### 补充图表

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/001_Figure_1.jpg]]
*Figure 1: Activation analyses with negative labels mined in [29]. (a) Negative labels on a specific OOD dataset exhibit a long-tailed activation score distribution. Some labels activate more strongly on the ID dataset than on OOD, potentially misleading OOD detection. (b) A small subset of negative labels strongly activates on OOD, enabling effective detection. Most labels respond similarly across ID and OOD, slightly harming detection, while some activate higher on ID, significantly degrading performance. The FPR95 results are obtained with negative labels of top activations via Eq. 4. These analyses use ground truth labels from ImageNet (ID) and Places (OOD) datasets*

## 实验与分析

### 主实验结果

TANL 在多个 OOD 检测基准上均展现出显著优于现有方法的性能。在 ImageNet-1k 作为 ID 数据集的经典设置下，采用 ViT-B/16 CLIP 编码器，TANL 在四个 OOD 数据集（iNaturalist、SUN、Places、Textures）上取得了平均 **9.81% FPR95** 和 **97.97% AUROC**（Table 1）。相比直接基线 **NegLabel** 的 25.40% FPR95，TANL 将误检率降低了 15.59 个百分点；相比训练自由的 SOTA 方法 **CSP**，FPR95 降低了 7.7 个百分点。这一提升的核心机制在于：传统 NegLabel 仅依据与 ID 标签的余弦距离选取负标签，忽略了这些标签在 OOD 测试数据上的实际激活水平——大量距离远的标签在 OOD 图像上激活极低，甚至部分标签在 ID 图像上激活更强，从而引入检测噪声（Figure 1）。TANL 通过测试时在线估计激活差异，动态筛选在 OOD 上高激活、在 ID 上低激活的标签，从根本上解决了这一瓶颈。

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/003_Table_1.jpg]]
*Table 1: OOD detection results with ImageNet-1k, where a VITB/16 CLIP encoder is adopted*

在更具挑战性的 OpenOOD 设置下（Table 2），TANL 同样保持领先：Near-OOD（SSB-hard、NINCO）FPR95 为 60.06%，较 NegLabel 的 69.45% 降低 9.39 个百分点；Far-OOD（iNaturalist、Textures、OpenImage-O）FPR95 为 17.21%，较 NegLabel 的 23.73% 降低 6.52 个百分点。在全谱 OOD 检测中（Table 3），将 ImageNet-1k、ImageNet-C、ImageNet-R、ImageNet-V2 同时作为 ID 数据集时，TANL 的 Near-OOD FPR95 降至 68.71%，显著优于 NegLabel 的 76.25%。

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/004_Table_2.jpg]]
*Table 2: OOD detection results under OpenOOD setting, where ImageNet-1k is adopted as ID dataset. Full results are available in Tab. A7*

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/005_Table_3.jpg]]
*Table 3: Full-spectrum OOD detection results under the OpenOOD setting, where ImageNet-1k, ImageNet-C, ImageNet-R, ImageNet-V2 are used as ID datasets. Full results are shown in Tab. A8*

### 消融实验：各组件的独立贡献

Table 4 的消融实验系统拆解了 TANL 三个核心组件的增益。以 OpenOOD 设置下的 Near-OOD FPR95 为指标：

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/006_Table_4.jpg]]
*Table 4: Ablation analyses, where results (FPR95↓) are reported with ImageNet ID dataset under the OpenOOD setup. “Dis-adapt”, “Batch-adapt”, and “AAScore” represent the distribution-adaptive activated score in Eq. 8, batch-adaptive variant in Eq. 11, and activation-aware score in Eq. 15, respectively*

- **分布自适应激活标签（Dis-adapt，Eq. 8）**：仅引入基于 FIFO 队列的激活差异估计来替换 NegLabel 的静态标签选择，FPR95 从 69.45% 降至 63.55%，贡献了最主要的性能提升。这验证了“负标签在 OOD 上的激活水平是检测性能的关键因素”这一核心洞察。
- **批次自适应增强（Batch-adapt，Eq. 11-14）**：在分布自适应基础上融合当前批次的高置信样本信息，FPR95 进一步降至 61.44%。这表明结合局部批次统计可以更精细地捕捉测试数据的瞬时分布特性。
- **激活感知评分函数（AAScore，Eq. 15）**：在标签选择和批次自适应之上，将普通 softmax 求和替换为循环累加排序负标签的激活感知评分，最终 FPR95 达到 60.06%。该评分函数通过让高激活标签在分母中更频繁出现，隐式增强了其权重，无需引入额外可学习参数。

### 参数鲁棒性与选择标准分析

Figure 3 进一步揭示了方法的关键性质：

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/008_Figure_3.jpg]]
*Figure 3: Analyses on (a) number M of selected negative labels, (b) selection criterion of negative labels, (c) α values, and (d) batch size under OpenOOD setting*

- **对负标签数量 M 的鲁棒性（Fig. 3a）**：NegLabel 在 M 增大时性能显著下降，而 TANL 的激活感知评分函数使性能在较大 M 范围内保持稳定。这源于理论分析（Eq. 16）揭示的条件：增加负标签数量 M 能降低 FPR 的前提是 $p_1 - p_2 < 0$，即负标签在 OOD 上的相似度高于在 ID 上。TANL 通过激活差异筛选确保了所选标签满足这一条件。
- **选择标准的有效性（Fig. 3b）**：仅使用负样本激活 $\text{Act}(\mathcal{X}_{neg})$ 作为选择标准，其性能已接近完整的差分标准 $\text{Act}_d$。这说明在 OOD 检测中，标签在 OOD 数据上的绝对激活水平本身已具有强判别力，差分项主要起到进一步抑制 ID 上高激活噪声标签的作用。
- **混合系数 α 与批次大小（Fig. 3c, 3d）**：方法对 α 和批次大小的变化表现出良好的稳定性，无需精细调参即可获得接近最优的性能。

### 可视化分析

Figure 4 展示了排序后的语料库标签可视化。高激活得分的候选标签被优先选用，这些标签通常与 OOD 数据的语义内容高度相关（如针对 Places 场景，高激活标签包含“outdoor”、“landscape”等场景描述词），直观印证了激活估计机制的有效性。

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/011_Figure_4.jpg]]
*Figure 4: Visualization of ranked corpus dataset, where candidate labels with higher activation scores are utilized*

### 效率分析

Table 5 的时间复杂度分析表明，TANL 无需训练（Training 时间为 0）、无可学习参数（Param. 为 0）。在推理速度方面，虽然相比 MCM 等简单基线有所下降（因需要在线维护队列和计算激活），但在批次大小为 256 时仍保持实用的 FPS 水平，且显著优于需要训练的竞争方法。

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/012_Table_5.jpg]]
*Table 5: Time complexity analyses. ‘Training’ measures the training time, and ‘Param.’ presents the number of learnable parameters. ‘FPS’ reflects the inference speed with a batch size of 256*

### 失败模式与局限

尽管 TANL 在通用视觉基准上表现优异，其有效性依赖于两个前提假设：① 语料库覆盖与 OOD 分布相关的词语；② 预训练文本编码器能够理解这些词语。在特定领域（如医学影像）中，通用语料库可能缺乏领域特异性术语，导致激活估计的判别力下降，性能提升有限。此外，测试初期的队列质量对自适应效果有影响：当初始模型的误分类率超过 80% 时，测试时自适应可能带来负面影响；但实验表明，方法在实际中具有较强的鲁棒性，仅需约 20% 的初始精度即可实现正向改进。

### 补充图表

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/007_Figure.jpg]]
*Figure: (a) Number of negative labels (b) Selection criterion (c) α values (d) Batch size*

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/010_Table.jpg]]
*Table: Ranked Corpus Dataset*

![[assets/figures/papers/paper_list_l2758_https_arxiv_org_abs_2603_25250/figures/013_Table.jpg]]
*Table: A6. Complete OOD detection results with ImageNet-1k, where a VITB/16 CLIP encoder is adopted*

## 方法谱系与知识库定位

### 与基线方法的关系

TANL 直接建立在 **NegLabel** 的负标签范式之上，但对其两个核心组件进行了根本性改造。NegLabel 从语料库中选取与 ID 标签余弦距离最远的词语作为负标签（式 3），并使用统一的 softmax 求和作为 OOD 检测分数（式 4），所有负标签在评分函数中权重相同。TANL 揭示了这一范式的关键瓶颈：距离远的负标签在特定 OOD 测试集上的激活程度往往很低，甚至部分标签在 ID 样本上激活更强，反而引入检测噪声（Figure 1）。因此，TANL 将负标签选择标准从“与 ID 的距离”改为“在 OOD 上的激活强度”，并通过激活感知评分函数隐式增强高激活标签的权重，从选择机制和评分机制两个层面同时改进。

相较于其他训练自由的 VLM-based OOD 检测方法，**MCM** 仅使用 ID 标签相似度进行零样本检测，未引入负标签机制，性能上限较低。**CSP** 作为训练自由的 SOTA 方法之一，在 ImageNet-1k 基准上的平均 FPR95 为 17.5%，而 TANL 进一步降至 9.81%（Table 1）。**AdaNeg** 同样采用测试时适应策略，但使用自适应负代理（adaptive negative proxies），其适应机制与 TANL 基于激活估计的标签选择有本质区别。

### 方法适用边界

TANL 的核心假设是：（1）语料库覆盖与 OOD 分布相关的词语；（2）预训练文本编码器能够理解这些词语。在通用视觉场景（如 ImageNet 及其 OOD 变体）中，使用 WordNet 等大规模语料库可以较好地满足这一假设。然而，在特定领域（如医学影像），语料库可能缺乏领域特异性词汇，且 CLIP 等通用 VLM 的文本编码器对这些术语的语义理解有限，导致激活估计的可靠性下降，性能提升受限（原文明确指出的限制）。

方法对初始模型精度具有较强鲁棒性：仅需约 20% 的初始分类精度即可实现正向改进。但当缓存队列中误分类样本比例超过 80% 时，测试时自适应可能带来负面影响，性能退化至 NegLabel 基线以下。

### 局限与开放问题

**已知局限：**

1. **语料库依赖性**：方法性能受限于语料库对 OOD 分布的词汇覆盖能力。在专业领域（如医学、遥感）中，需要人工构建领域语料库并可能需要对文本编码器进行领域微调，这增加了部署成本。

2. **冷启动风险**：测试初期队列为空时，依赖噪声图像初始化的正队列和 ID 标签特征初始化的负队列（式 10）。若初始批次包含大量困难样本，队列质量可能影响早期检测性能。

3. **计算开销**：TANL 在推理时需维护 FIFO 队列、计算语料库标签的激活得分并进行排序选择，相比 NegLabel 等静态方法增加了测试时计算量（Table 5 给出了时间复杂度分析）。

**开放问题：**

1. **显式加权策略的设计空间**：当前激活感知评分函数（式 15）通过循环累加实现隐式加权，使高激活标签在分母中出现更频繁。是否存在更精细的显式权重方案（如直接对相似度进行加权）能够匹配或超越当前的隐式策略？

2. **领域自适应语料库构建**：如何为医学、工业检测等专业领域自动化构建合适的语料库，并结合轻量级文本编码器微调，以进一步发挥激活感知机制的潜力？

3. **极端数据流下的稳定性**：在长时间仅出现 ID 或仅出现 OOD 样本的极端测试流下，FIFO 队列将逐渐被单一类别样本填充，激活估计的可靠性如何维持？方法是否需要引入遗忘机制或队列重置策略？

4. **激活感知评分的理论最优性**：当前隐式加权方案的有效性已在实验中得到验证，但其是否为激活信息利用的理论最优形式？是否存在其他变体（如基于激活得分的直接加权归一化）能够进一步提高检测性能？

## 原文 PDF

![[paperPDFs/CVPR_2026/Activation_Matters_Test_time_Activated_Negative_Labels_for_OOD_Detection_with_Vision_Language_Models.pdf]]
