---
title: "Plug-and-Play Compositionality for Boosting Continual Learning with Foundation Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Plug_and_Play_Compositionality_for_Boosting_Continual_Learning_with_Foundation_Models.pdf
project_link: null
code_link: https://github.com/liaoweiduo/CompSLOT
openreview_forum_id: 22hBwIf7OC
aliases:
- PPCBCLFM
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "通过无监督对象中心学习（Slot Attention）从预训练 ViT 特征中提取解耦的概念表示（slots），并选择与类别相关的原语（primitives），然后通过对比损失将样本间概念相似度蒸馏到 logits，从而引导分类器基于概念组合进行决策，而不是纯高维特征。"
primary_logic: "引入概念级组合性理解作为方法无关的插件，使得任何基于 FM 的持续学习器在不增加大量参数的情况下，利用概念共享提升稳定性与组合泛化。"
claims:
- "CompSLOT 显著增强了多种持续学习基线的平均准确率，尤其是 ADAM+adapter 在 CGQA 上提升了 7.55 个百分点"
- "Slot Attention 模块在连续组合重建任务中表现出几乎零遗忘，其提取的概念在任务间保持稳定"
- "原语相似度成功模仿了真实概念相似度统计，且对齐损失将概念层面的关系蒸馏到了 logits 中"
- "CGQA (10-10 tasks) 上 AA (%) = 49.480 ± 1.201"
---

# Plug-and-Play Compositionality for Boosting Continual Learning with Foundation Models

> [!tip] 核心洞察
> 引入概念级组合性理解作为方法无关的插件，使得任何基于 FM 的持续学习器在不增加大量参数的情况下，利用概念共享提升稳定性与组合泛化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 即插即用的组合性提升基于基础模型的持续学习 |
| 英文题名 | Plug-and-Play Compositionality for Boosting Continual Learning with Foundation Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=22hBwIf7OC) · [GitHub](https://github.com/liaoweiduo/CompSLOT) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | CompSLOT |
| Dataset | CGQA (10-10 tasks), COBJ (10-10 tasks) |

> [!tip] 效果简介
> - CGQA (10-10 tasks) 上，AA (%) 为 49.480 ± 1.201，对比 41.930 ± 1.141，变化 7.550。
> - CGQA (10-10 tasks) 上，AA (%) 为 48.537 ± 0.427，对比 46.753 ± 0.570，变化 1.784。
> - CGQA (10-10 tasks) 上，AA (%) 为 66.753 ± 0.867，对比 65.810 ± 0.802，变化 0.943。

## 概要

**问题瓶颈**：现有基于基础模型（FM）的持续学习方法普遍依赖高维视觉特征（如 ViT 的 [CLS] token）进行类别比较或提示匹配，却忽略了图像中跨任务共享的底层概念组合。这一缺失导致两个关键后果：灾难性遗忘难以根本缓解，以及对未见概念组合的泛化能力薄弱。随着任务序列增长，模型倾向于记忆表观特征而非理解概念构成，持续学习性能迅速退化。

**核心思路**：CompSLOT 提出以**概念级组合性理解**作为方法无关的即插即用插件，在不显著增加参数的前提下，为任意基于 FM 的持续学习器注入概念共享与组合泛化能力。其因果机制分为三层：

1. **概念提取**：通过 Slot Attention 模块从冻结 ViT 的语义 patch 特征中迭代提取一组解耦的低维概念表示（slots），每个 slot 绑定图像中的一个独立视觉概念。
2. **原语选择**：利用可学习的注意力机制从多个 slot 中聚合出与类别相关的概念表示（primitives），并通过对比损失强制类内原语一致性。
3. **概念-逻辑蒸馏**：计算样本间原语相似度分布，以 KL 散度将其蒸馏到分类器输出的 logits 相似度上，使分类器在决策时具备概念组合的感知能力。

**方法定位**：CompSLOT 位于持续学习方法谱系中的**通用增强层**位置。它不替代现有持续学习算法（如基于提示的 **CPrompt**（Gao et al., 2024）、基于表示的 **ADAM+adapter**（Zhou et al., 2025）和 **RanPAC**（McDonnell et al., 2023）、基于模型混合的 **FOSTER***（Wang et al., 2022a）等），而是通过统一的原语-逻辑对齐损失 $L_a$ 对其进行正则化。概念学习阶段（Slot Attention + Primitive Selection）作为一个可离线训练的共享模块，独立于具体持续学习算法，仅与基准数据集相关。

**主要结果**：在组合泛化基准 CGQA 的 10-10 任务设置下，CompSLOT 显著提升了多种基线的平均准确率（AA）：ADAM+adapter 提升 **7.55 个百分点**（41.930 → 49.480），CPrompt 提升 1.78 个百分点，RanPAC 提升 0.94 个百分点。在组合目标基准 COBJ 上，ADAM+adapter 提升 4.40 个百分点。在 ImageNet-R 的 20-20 任务上，FOSTER* 提升 2.95 个百分点。同时，CompSLOT 在组合稳定性指标 Hn 上也带来 5.69 个百分点的增益（ADAM+adapter 上 68.649 → 74.335）。初步实验（Figure 2）表明，Slot Attention 模块在连续组合重建任务中表现出几乎零遗忘，其提取的概念表示在任务间保持高度稳定。

**证据强度与局限**：上述增益在多次试验中具有统计显著性，且通过参数计数匹配消融实验排除了容量扩充的混淆效应。然而，CompSLOT 在组合泛化的 substitutivity（属性替换）维度上改进不显著，提示 ViT 特征在应对属性变化时存在固有限制。此外，当前概念学习阶段与持续学习分类目标为分离式训练，尚未实现端到端联合优化，可能限制整体潜力。

持续学习（Continual Learning, CL）的核心挑战在于，模型在顺序学习新任务时如何避免灾难性遗忘。近年来，大规模预训练基础模型（Foundation Models, FMs）为持续学习提供了强大的特征表示能力，催生了一批基于提示（prompt-based）和基于表示（representation-based）的持续学习方法。然而，这些方法存在一个共同的深层瓶颈：**它们依赖高维特征空间中的直接比较进行分类，忽略了图像中跨任务共享的底层概念组合**。

具体而言，现有方法——无论是基于提示的 **CPrompt**（Gao et al., 2024），还是基于原型分类器的 **ADAM+adapter**（Zhou et al., 2025）与随机投影分类器 **RanPAC**（McDonnell et al., 2023）——均将图像编码为单一的全局表示（如 ViT 的 [CLS] token），并在该高维空间中度量类别相似性。这种策略虽然利用了预训练特征的判别力，却无法显式建模图像中不同视觉概念（如物体部件、纹理、形状）的解耦组合关系。当新任务引入与旧任务共享底层概念但组合方式不同的类别时，模型缺乏对概念级共享的感知，导致两个后果：一是灾难性遗忘加剧，因为分类边界仅在高维流形上被覆盖而非基于可迁移的概念单元；二是组合泛化能力弱，模型难以将已知概念重组以识别未见过的概念组合。

这一问题的根源在于，**预训练 ViT 的语义 patch 特征中已经蕴含了丰富的概念信息，但现有持续学习范式未能将其显式提取和利用**。ViT 将图像切分为多个 patch 并产生对应的语义特征，这些特征天然地对应着图像中的局部概念区域。然而，无论是基于提示的方法（通过可学习 prompt 调整特征分布）还是基于表示的方法（通过分类器直接映射全局特征），都绕过了对 patch 级概念的解耦与重组。

本文的核心动机正是填补这一空白：**能否引入概念级组合性理解作为方法无关的插件，使任何基于 FM 的持续学习器在不显著增加参数的前提下，利用跨任务的概念共享来同时提升稳定性和组合泛化能力？** 为此，我们提出 CompSLOT，通过无监督对象中心学习（Slot Attention）从冻结或微调的 ViT 特征中提取解耦的概念表示，并将样本间概念相似度蒸馏到分类器的 logits 中，引导模型基于概念组合而非纯高维特征进行决策。

初步实验（Figure 2）验证了这一动机的可行性：在连续组合重建任务中，Slot Attention 模块提取的概念表示在任务间几乎不发生遗忘，其重建损失矩阵在不同任务上保持高度一致，表明概念提取本身对任务序列不敏感，为后续的概念引导持续学习奠定了基础。

## 核心方法与创新机理

现有基于基础模型的持续学习方法，无论是基于提示的 **CPrompt**（Gao et al., 2024）还是基于表示的 **ADAM+adapter**（Zhou et al., 2025）、**RanPAC**（McDonnell et al., 2023），其分类决策本质上都依赖于高维视觉特征（如全局 `[CLS]` token 或提示特征）之间的相似性比较。这一范式忽略了一个关键瓶颈：**跨任务共享的底层视觉概念组合**。当新任务引入已知概念的未知组合时，仅凭高维特征匹配无法有效复用已学知识，导致灾难性遗忘与组合泛化能力薄弱。

CompSLOT 的核心创新在于引入**概念级组合性理解作为方法无关的即插即用插件**，使任意基于基础模型的持续学习器在不显著增加参数的前提下，具备基于概念组合进行决策的能力。这一创新通过三个相互耦合的机制实现，对应三个关键的 changed slots：

### 1. 概念提取：从高维特征到解耦概念表示

传统方法直接将 ViT 输出的语义 patch 特征或全局特征送入分类器，未对其中蕴含的底层概念进行显式建模。CompSLOT 提出 **Slot Attention 模块**，以无监督对象中心学习的方式，从冻结的预训练 ViT 语义 patch 特征 $\pmb{E} \in \mathbb{R}^{N \times D}$ 中迭代提取一组低维、解耦的概念表示（slots）$\pmb{S} \in \mathbb{R}^{K \times D_s}$。每个 slot 绑定图像中的一个语义区域（即“概念”），并通过轻量 MLP 解码器 $d(\cdot|\theta_d)$ 重建原始特征：

$$\tilde{\pmb{E}} = \pmb{A}^\top d(\pmb{S}' | \theta_d), \quad L_{re} = ||\pmb{E} - \tilde{\pmb{E}}||_2$$

该模块在连续组合重建任务中表现出**几乎零遗忘**的特性（Figure 2）：即使经过多个任务训练，同一图像在不同时刻提取的 slots 仍保持高度一致的余弦相似性，验证了概念表示在任务间的稳定性。这是后续概念共享与组合泛化的基础。

### 2. 原语选择：从等权特征到类别相关概念聚合

传统方法对所有视觉特征等权处理，未区分类别相关与类别无关的概念。CompSLOT 提出**基于可学注意力机制的原语选择模块**，通过一个可学习的原语键（primitive key）$K^p$ 计算每个 slot 的相似度权重，并加权求和得到单一的原语表示 $s^p$：

$$\bar{S} = \operatorname{tanh}(\operatorname{Linear}(\operatorname{LN}(S))), \quad w_p = \sigma(\tau_t \bar{S} K^p), \quad s^p = w_p^\top \bar{S}$$

为进一步确保原语表示的类内一致性，引入**对比原语损失 $L_p$**，利用标签信息构建样本间相似度分布，通过 KL 散度约束原语相似度分布与之对齐。消融实验（Table 2）表明，移除 $L_p$ 会导致性能显著下降，证实了类内概念一致性对原语选择至关重要。

### 3. 概念-逻辑知识蒸馏：从孤立分类到概念关系感知

这是 CompSLOT 最具方法通用性的创新。传统持续学习器的输出 logits 不包含显式的样本间概念关系监督。CompSLOT 提出**原语-逻辑对齐损失 $L_a$**，通过计算样本间原语相似度分布 $d^s$ 与 logits 相似度分布 $d^l$，以 KL 散度将概念层面的关系蒸馏到分类器输出中：

$$d_{i,j}^s = \frac{\sin_+(s_i^p, s_j^p)}{\sum_{x_k \in B} \sin_+(s_i^p, s_k^p)}, \quad d_{i,j}^l = \frac{\exp(\tau_a \sin(l_i, l_j))}{\sum_{x_k \in B} \exp(\tau_a \sin(l_i, l_k))}, \quad L_a = \sum_{x_i, x_j \in B} d_{i,j}^s \log \frac{d_{i,j}^s}{d_{i,j}^l}$$

最终训练损失为 $L_{tr} = L_{ce} + \beta L_a$，其中 $\beta$ 控制对齐强度。可视化证据（Figure 4/9）表明，学习到的原语相似度矩阵成功模仿了真实概念相似度统计，且 $L_a$ 有效将这种成对概念相似性蒸馏到了 logits 中——而未经 CompSLOT 增强的基线方法（如 ADAM+adapter）则无法捕获这种概念共享统计。

### 方法无关的即插即用特性

上述三个模块中，概念提取与原语选择阶段（Slot Attention + Primitive Selection）作为独立的概念学习前端，对所有持续学习算法开放共享，无需针对特定方法调整。原语-逻辑对齐模块仅需访问基线的输出 logits，以正则化项形式注入训练目标。实验覆盖了基于提示（CPrompt）、基于表示（ADAM+adapter、RanPAC、EASE）、基于模型混合（CoFiMA）及基于回放（FOSTER\*、DER\*、MEMO\*）等多种范式的持续学习方法，CompSLOT 均带来一致的性能增益（Table 1, Table 7, Table 8），其中 ADAM+adapter 在 CGQA 上 AA 提升达 +7.55 个百分点，验证了其方法无关的通用性。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_22hBwIf7OC/figures/027_Figure_12.jpg]]
*Figure 12: Line charts of different hyperparameters in slot attention architecture. (a) Alignment Coeff*

CompSLOT 是一个即插即用的概念组合增强框架，其核心目标是让任意基于基础模型的持续学习器在决策时额外考虑低维概念组合，而非仅依赖高维特征。该框架由三大模块构成，形成“概念提取—原语选择—概念-逻辑蒸馏”的级联管线。

### 输入与骨干网络

框架的输入为来自预训练 ViT 的语义 patch 特征 $\pmb{E} \in \mathbb{R}^{N \times D}$，其中 $N$ 为 patch 数量，$D$ 为特征维度。ViT 骨干在所有任务间保持冻结，不参与持续学习的参数更新，从而避免灾难性遗忘在底层表示中的积累。Slot Attention 模块和原语选择模块在所有任务间全局共享，仅分类器部分随任务增量扩展。

### 概念提取：Slot Attention 模块

Slot Attention 模块从语义 patch 特征中迭代提取一组解耦的概念表示（slots）。具体而言，该模块维护 $K$ 个可学习的 slot 向量 $\pmb{S} \in \mathbb{R}^{K \times D_s}$，通过交叉注意力机制与 patch 特征交互，并经 GRU 迭代细化。每次迭代中，slot 通过注意力权重 $\pmb{A}$ 聚合 patch 信息，随后由轻量 MLP 解码器 $d(\cdot|\theta_d)$ 重建原始特征：

$$\tilde{\pmb{E}} = \pmb{A}^\top d(\pmb{S}' | \theta_d) \in \mathbb{R}^{N \times D}, \quad L_{re} = ||\pmb{E} - \tilde{\pmb{E}}||_2$$

重建损失 $L_{re}$ 约束 slot 编码足够信息以还原输入，从而迫使每个 slot 绑定到图像中一个解耦的视觉概念区域。这一设计使得 Slot Attention 模块在跨任务学习中表现出近乎零遗忘的特性（Figure 2），为后续持续学习提供了稳定的概念基础。

### 原语选择：Primitive Selection 模块

并非所有 slot 都与当前分类任务相关。原语选择模块通过可学习的键向量 $K^p$ 计算每个 slot 与类别相关性的注意力权重，并以加权求和方式聚合为单一原语表示 $s^p$：

$$\bar{S} = \operatorname{tanh}(\operatorname{Linear}(\operatorname{LN}(S))), \quad w_p = \sigma(\tau_t \bar{S} K^p), \quad s^p = w_p^\top \bar{S}$$

其中 $\tau_t$ 为温度系数，控制 slot 选择的稀疏性。为进一步确保类内概念一致性，框架引入对比原语损失 $L_p$，通过 KL 散度约束同类样本的原语相似度分布与标签相似度分布对齐。Slot Attention 模块的训练损失为 $L_{slot} = L_{re} + \alpha L_p$，该阶段可离线完成，与下游持续学习算法解耦。

### 概念-逻辑蒸馏：Primitive-Logit Alignment 模块

这是 CompSLOT 实现方法无关性的关键模块。对于每个训练批次，计算样本间原语相似度分布 $d^s$ 和 logits 相似度分布 $d^l$，并通过 KL 散度将前者蒸馏到后者：

$$d_{i,j}^s = \frac{\sin_+(s_i^p, s_j^p)}{\sum_{x_k \in B} \sin_+(s_i^p, s_k^p)}, \quad d_{i,j}^l = \frac{\exp(\tau_a \sin(l_i, l_j))}{\sum_{x_k \in B} \exp(\tau_a \sin(l_i, l_k))}, \quad L_a = \sum_{x_i, x_j \in B} d_{i,j}^s \log \frac{d_{i,j}^s}{d_{i,j}^l}$$

最终训练损失为 $L_{tr} = L_{ce} + \beta L_a$，其中 $L_{ce}$ 为标准交叉熵分类损失。该模块不修改任何基线的网络结构或推理逻辑，仅通过正则化项将概念层面的样本关系注入 logits，使得分类器隐式感知跨样本的概念共享与组合关系。

### 管线总结

整个框架的数据流可概括为：输入图像经冻结 ViT 提取 patch 特征 → Slot Attention 分解为 $K$ 个解耦 slot → Primitive Selection 加权聚合为类别相关原语 → 原语相似度通过 $L_a$ 蒸馏至分类器 logits。概念学习阶段（前两步）独立于持续学习算法，原语-逻辑对齐阶段（第三步）以即插即用方式嵌入任意基线的训练损失中。

### 概念提取：Slot Attention 模块

CompSLOT 的概念学习建立在 Slot Attention 机制之上。该模块接收预训练 ViT 骨干网络输出的语义 patch 特征 $\pmb{E} \in \mathbb{R}^{N \times D}$（$N$ 为 patch 数量，$D$ 为特征维度），通过迭代注意力分组将其解耦为一组低维的 slot 表示 $\pmb{S} \in \mathbb{R}^{K \times D_s}$，其中 $K$ 为 slot 数量，每个 slot 绑定图像中的一个解耦区域（即概念）。

Slot Attention 的核心迭代更新遵循标准流程：在每一步中，slot 作为 query 与 patch 特征作为 key/value 计算交叉注意力，随后通过 GRU 聚合信息：

$$A = \sigma\left(\frac{q(S) k(E)^\top}{\sqrt{D_s}}\right), \quad A_{i,n} \gets \frac{A_{i,n}}{\sum_{i=1}^{N} A_{i,j}}, \quad S \gets \mathrm{GRU}(S, A v(E))$$

经过 $N_s$ 次迭代细化后，得到最终的 slot 表示 $\pmb{S}'$。为驱动无监督分解学习，模块使用轻量 MLP 解码器 $d(\cdot|\theta_d)$ 从 slot 重建原始 patch 特征，并施加重建损失：

$$\tilde{\pmb{E}} = \pmb{A}^\top d(\pmb{S}' | \theta_d) \in \mathbb{R}^{N \times D}, \quad L_{re} = ||\pmb{E} - \tilde{\pmb{E}}||_2$$

其中 $\pmb{A}$ 为最后一次迭代的注意力权重矩阵。该重建目标迫使 slot 捕获图像中具有语义一致性的区域，为后续概念组合奠定基础。

### 原语选择模块

并非所有 slot 都与分类目标相关。CompSLOT 引入可学习的原语选择机制，通过注意力加权将 $K$ 个 slot 聚合为单一的类别相关原语表示 $s^p$：

$$\bar{S} = \operatorname{tanh}(\operatorname{Linear}(\operatorname{LN}(S))), \quad w_p = \sigma(\tau_t \bar{S} K^p), \quad s^p = w_p^\top \bar{S}$$

其中 $\operatorname{LN}$ 为 Layer Normalization，$K^p \in \mathbb{R}^{D_s}$ 是可学习的原语键（primitive key），$\tau_t$ 为温度系数（实践中设为 $100/\sqrt{D_s}$），控制 slot 选择的稀疏度。softmax 函数 $\sigma$ 确保权重 $w_p$ 构成凸组合，使原语表示保持在适当范围内，这对训练稳定性至关重要。

为约束同类样本的原语表示具有一致性，引入对比原语损失 $L_p$。给定 batch $B$ 中的样本对 $(x_i, x_j)$，首先基于标签构建样本间相似度分布 $d^y$，再基于原语余弦相似度构建分布 $d^s$，通过 KL 散度对齐二者：

$$d_{i,j}^y = \frac{\sin(\mathbb{I}_i, \mathbb{I}_j)}{\sum_{x_k \in B} \sin(\mathbb{I}_i, \mathbb{I}_k)}, \quad d_{i,j}^s = \frac{\exp(\tau_p \sin(s_i^p, s_j^p))}{\sum_{x_k \in B} \exp(\tau_p \sin(s_i^p, s_k^p))}, \quad L_p = \sum_{x_i, x_j \in B} d_{i,j}^y \log \frac{d_{i,j}^y}{d_{i,j}^s}$$

其中 $\mathbb{I}_i$ 为样本 $x_i$ 的 one-hot 标签向量，$\tau_p$ 为温度超参数。Slot Attention 模块的总训练损失为 $L_{slot} = L_{re} + \alpha L_p$。

### 原语-逻辑对齐模块

该模块是 CompSLOT 实现方法无关性的关键：它将概念层面的样本间相似度蒸馏到分类器的输出 logits 中，使任何基于 FM 的持续学习器都能感知概念组合关系。具体而言，对 batch 中的样本对，计算基于原语的相似度分布 $d^s$（使用 min-max 归一化后的余弦相似度 $\sin_+$）和基于 logits 的相似度分布 $d^l$，通过 KL 散度将前者蒸馏到后者：

$$d_{i,j}^s = \frac{\sin_+(s_i^p, s_j^p)}{\sum_{x_k \in B} \sin_+(s_i^p, s_k^p)}, \quad d_{i,j}^l = \frac{\exp(\tau_a \sin(l_i, l_j))}{\sum_{x_k \in B} \exp(\tau_a \sin(l_i, l_k))}, \quad L_a = \sum_{x_i, x_j \in B} d_{i,j}^s \log \frac{d_{i,j}^s}{d_{i,j}^l}$$

其中 $l_i$ 为样本 $x_i$ 的 logits 向量，$\tau_a$ 为温度超参数。最终训练损失由交叉熵分类损失与对齐损失加权组合：

$$L_{tr} = L_{ce} + \beta L_a$$

$\beta$ 控制概念知识蒸馏的强度。消融实验表明，$\beta$ 在适中范围内（CPrompt 上 $\beta \approx 2$）提升准确率，但过大会导致性能下降；min-max 归一化在计算 $d^s$ 时优于 softmax 归一化，能提供更清晰的监督信号。

## 实验与关键发现

### 主要结果：CompSLOT 作为通用插件提升持续学习性能

CompSLOT 在多个基准和基线方法上均展现出稳定且显著的性能增益。Table 1 展示了 CGQA（10-10 任务）上的核心结果：所有基线方法在集成 CompSLOT（以“†”标记）后，平均准确率（AA）均得到提升。其中，基于表示的 **ADAM+adapter**（Zhou et al., 2025）增益最为突出，AA 从 41.930% 跃升至 49.480%，绝对提升 **+7.55 个百分点**。基于提示的 **CPrompt**（Gao et al., 2024）和基于随机投影的 **RanPAC**（McDonnell et al., 2023）也分别获得了 +1.784 和 +0.943 个百分点的提升。在组合泛化指标 Hn 上，ADAM+adapter† 达到 74.335%，较基线的 68.649% 提升了 **+5.686 个百分点**，表明 CompSLOT 显著增强了模型对组合概念的捕获能力。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_22hBwIf7OC/figures/003_Table_1.jpg]]
*Table 1: Main result on CGQA. Methods with CompSLOT are denoted with a postfi$x ^ { 6 6 } \dag ^ { 5 }$ . Methods rehearse old samples are denoted with a postfix “*”. We report results over 3 trials with (mean ± 95% confidence interval). We replace the backbones of all methods to Imagenet-21K-pretrained ${ \mathrm { V i T } } { \mathrm { - B } }$ / 1 6

在 COBJ（10-10 任务）数据集上，CompSLOT 同样表现出色（Table 7）：ADAM+adapter† 的 AA 达到 50.150%，较基线的 45.750% 提升了 **+4.400 个百分点**。在更具挑战性的 ImageNet-R（20-20 任务）上（Table 8），基于回放的 **FOSTER\***（Wang et al., 2022a）在集成 CompSLOT 后 AA 从 76.001% 提升至 78.950%，增益 **+2.949 个百分点**。这些跨数据集、跨方法的一致性提升证实了 CompSLOT 作为方法无关插件的有效性。

学习曲线（Figure 3）进一步揭示了 CompSLOT 的作用机制：在 CGQA 的 10-10 和 5-5 任务设置下，集成 CompSLOT 的方法在每个任务训练后的即时准确率和最终平均准确率均持续高于对应基线。这表明 CompSLOT 不仅缓解了对旧任务的灾难性遗忘，还保持了对新任务的强正向适应能力。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_22hBwIf7OC/figures/005_Figure_3.jpg]]
*Figure 3: Learning curves and histograms of methods with and without CompSLOT on CGQA a) 10-10 tasks and b) 5-5 tasks. Slot is the case directly using the primitive representation and a cosine similarity classifier for the continual tasks*

### 消融实验：关键设计选择验证

Table 2 的消融实验系统验证了 CompSLOT 各组件的必要性：

- **原语损失 L_p 的关键作用**：移除 L_p 后，RanPAC 和 CPrompt 的 AA 分别下降至 65.080% 和 46.300%，显著低于完整模型。这证实了通过对比损失约束类内原语一致性，是实现可靠原语选择和概念级类别理解的核心机制。

- **Softmax 加权选择的稳定性**：与硬选择（hard selection）或无选择（直接使用所有 slots）相比，基于 softmax 的原语聚合（如公式 2 所示）在 RanPAC 和 CPrompt 上均取得了最优的 AA 和组合泛化比 R。Softmax 通过凸组合将原语表示约束在适当范围内，确保了训练的稳定性。

- **对齐损失系数 β 的敏感度**：Table 6 显示，在 CPrompt 上，AA 随 β 增大而提升，但在 β≈2 附近达到峰值后开始下降。这表明适度的原语-逻辑知识蒸馏是有益的，但过强的对齐约束会干扰分类器对任务特定特征的学习。

- **相似度归一化策略**：Figure 13c 表明，在计算原语相似度时，min-max 归一化优于 softmax 归一化，能够提供更清晰的监督信号，从而获得更高的 AA。

- **Slot 数量与迭代次数**：Figure 12a 显示，slot 数量 K 从 1 增加到 10 时性能持续提升，但超过 10 后增益递减——冗余 slot 仅复制已有表示。Figure 12b 表明，Slot Attention 的 3 次细化迭代在精度与效率之间达到最佳平衡。

### 概念学习可视化与原语-逻辑蒸馏效果

Figure 4 提供了概念学习和知识蒸馏效果的直接证据。左侧可视化展示了在 COBJ 上完成 T0 和 T1 任务后，Slot Attention 成功将图像分解为与底层概念对应的解耦区域（红色高亮表示高注意力值）。中间的原语余弦相似度矩阵显示，学习到的原语表示成功模仿了真实概念相似度统计——同类样本的原语高度相似，不同类样本的原语则明显区分。右侧的 logits 余弦相似度矩阵对比表明，集成 CompSLOT 的 ADAM+adapter† 在 T0 任务上的 logits 相似度模式与原语相似度高度一致，而原始 ADAM+adapter 则未能捕获这种概念共享统计。这证实了 L_a 成功将样本间概念级关系蒸馏到了分类器的输出空间中。

Figure 9 进一步对比了概念、原语、特征和 logits 四种表示的相似度矩阵：学习到的原语在无概念监督的情况下成功模仿了真实概念统计，且 L_a 的蒸馏效应不仅体现在 logits 层面，还反向影响了特征表示，使其更贴合概念结构。在 ImageNet-R 上（Figure 10），CompSLOT 甚至发现了隐含的概念关系——原语相似度矩阵揭示了模型捕获到的细粒度概念共享模式，而基线 FOSTER 则完全缺失这种统计结构。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_22hBwIf7OC/figures/015_Figure_9.jpg]]
*Figure 9: Visualization of a) concept; b) primitive; c) feature; d) logit cosine similarity matrices on sampled images (three images for each class in the first task T0 and second task T1 of the 10-10 tasks) on COBJ. a) Left: Multi-hot concept cosine similarity matrix of 30 images for T0; right: Multi-hot concept cosine similarity of 60 images (from the first-2 tasks T0 and T1). b) The primitive cosine similarity of the corresponding images. We use the learned pair-wise primitive similarity to mimic the statistics of the pair-wise concept similarity and regularize logits. c) Left: The learned feature cosine similarity matrix of 30 images in T0 for ADAM + adapter; right: The learned feature cosine sim...*

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_22hBwIf7OC/figures/017_Figure_10.jpg]]
*Figure 10: Visualization of a) images related to red box; b) primitive; c) feature; d) logit cosine similarity matrices on sampled images (three images for each class in the first task T0 and second task T1 of the 20-20 tasks) on ImageNet-R. a) Six images from two classes in T0 which corresponding to the red box. b) The primitive cosine similarity of the corresponding images. c) Left: The learned feature cosine similarity matrix of 60 images in T0 for FOSTER; right: The learned feature cosine similarity matrix of 60 images in T0 for FOSTER †. d) The logit cosine similarity of the corresponding images as in c). Takeaway: The learned primitives show that CompSLOT discovers hidden relationships based on...*

### 组合泛化与遗忘分析

Figure 2 的连续组合重建实验揭示了 CompSLOT 抵抗遗忘的深层原因。在 COBJ 的连续任务训练中，Slot Attention 模块在完成第 1、2、3 个任务后，对首个任务图像提取的 slots 保持高度一致的余弦相似度（通过匈牙利匹配算法分组验证），验证重建损失矩阵也显示几乎零遗忘。这表明 Slot Attention 学到的概念表示在组合相关任务间是稳定且可迁移的，为持续学习中的概念共享提供了坚实基础。

### 公平性验证

所有对比实验均在 PILOT 平台上统一实现，使用相同的 ImageNet-21K 预训练 ViT-B/16 骨干网络和默认超参数。参数计数匹配消融实验（Table 11）进一步证实，即使为基线方法故意增加参数以匹配 CompSLOT 模型规模，性能增益仍源自增强的组合泛化能力，而非简单的容量扩充。概念学习阶段（Slot Attention 与 Primitive Selection）作为独立离线训练模块对所有持续学习算法开放共享，避免了方法特定的优化差异。

### 失败模式与局限

尽管 CompSLOT 在多数组合泛化维度上表现优异，但在 substitutivity（属性替换）维度上改进不显著。这揭示了 ViT 特征在应对属性变化时的固有限制——即使通过概念分解，模型仍难以灵活重组属性以应对未见组合。此外，当前概念学习阶段与持续学习分类目标是分离训练的，尚未实现端到端联合优化，这可能限制了整体潜力的充分释放。

![[assets/figures/papers/paper_list_l11_https_openreview_net_forum_id_22hBwIf7OC/figures/008_Table_3.jpg]]
*Table 3: Detail hyperparameters for concept learning stage in our main experiments*

## 定位与知识库关联

### 核心瓶颈与动机

当前基于基础模型（FM）的持续学习方法——无论是基于提示的（如 **CPrompt**, Gao et al., 2024）、基于表示的（如 **ADAM+adapter**, Zhou et al., 2025; **RanPAC**, McDonnell et al., 2023; **EASE**, Zhou et al., 2024b）、基于模型混合的（如 **CoFiMA**, Marouf et al., 2024），还是基于回放的（如 **FOSTER***, Wang et al., 2022a; **DER***, Yan et al., 2021; **MEMO***, Zhou et al., 2023）——均直接依赖高维特征（如 ViT 的 [CLS] token 或提示特征）进行类别比较。这种设计忽略了跨任务共享的底层概念组合，导致两个关键瓶颈：（1）灾难性遗忘加剧，因为新任务覆盖了旧任务的高维特征分布；（2）组合泛化能力弱，模型无法利用已学概念的重新组合来识别未见过的属性-对象配对。

### CompSLOT 的定位：方法无关的概念组合插件

CompSLOT 并非一个独立的持续学习算法，而是一个**即插即用的概念组合性增强框架**，可叠加于任何基于 FM 的持续学习器之上。其核心干预点在于分类器输入端和训练目标两个层面：

1. **输入端**：在 ViT 特征与分类器之间插入 Slot Attention 模块和 Primitive Selection 模块，将高维 patch 特征解耦为一组低维、解耦的概念表示（slots），并通过可学注意力机制聚合出类别相关的原语（primitives）。这一过程是任务共享且参数冻结的，不随任务数增长而膨胀。

2. **目标端**：通过原语-逻辑对齐损失 $L_a$，将样本间基于概念组合的相似度分布蒸馏到 logits 相似度分布中，迫使分类器在决策时感知概念层面的关系，而非仅依赖高维特征相似度。

### 与现有概念学习方法的关系

CompSLOT 与两类直接操作概念的持续学习工作形成对比：

- **SACK**（Kundargi et al., 2025）作为概念知识插件与 CODA-Prompt 结合，但其概念来源于外部知识库或人工标注，而非从视觉特征中无监督学习。CompSLOT 的概念提取完全无监督，仅依赖 Slot Attention 的重建损失和原语对比损失，不引入额外标注成本。

- **CLG-CBM**（Yu et al., 2025）使用概念瓶颈模型进行持续学习，但概念瓶颈层通常需要概念标注或预定义概念集。CompSLOT 的原语选择机制通过可学键 $K^p$ 和 softmax 加权自动发现类别相关概念，避免了概念集的人工定义。

### 适用边界与局限

**适用场景**：
- 基于 ViT 骨干的持续学习任务，尤其是涉及组合泛化的场景（如 CGQA、COBJ 数据集上的属性-对象组合识别）。
- 需要在不显著增加参数的前提下提升稳定性和可塑性的场景——CompSLOT 的 Slot Attention 和 Primitive Selection 模块仅增加约 1-2M 参数，且在所有任务间共享。

**已知局限**：
1. **属性替换（substitutivity）改进不显著**：在组合泛化的 substitutivity 维度上，CompSLOT 的提升有限，揭示 ViT 特征在应对属性变化时存在固有限制。这暗示更强的视觉编码器（如 DINOv2）可能成为突破该瓶颈的必要条件。
2. **离线概念学习与端到端优化的割裂**：当前 Slot Attention 和 Primitive Selection 是独立于下游持续学习任务离线训练的，尚未与分类目标进行端到端联合优化。这限制了概念学习对特定任务分布的适应性。
3. **Slot 数量的收益递减**：当 slot 数量 $K$ 超过 10 后，性能增益趋于饱和，冗余 slot 仅复制已有表示，造成计算浪费。这表明模型的概念表示能力存在上限，与 slot 数量的简单线性扩展并非正相关。
4. **对齐损失系数的敏感性**：原语-逻辑对齐损失系数 $\beta$ 需要谨慎调节——在 CPrompt 上 $\beta \approx 2$ 时达到最优，过大则导致性能下降（Table 6, Figure 13a）。这增加了跨方法和跨数据集的超参数搜索成本。

### 开放问题

1. **端到端集成**：如何将概念学习（Slot Attention + Primitive Selection）与持续学习分类目标进行端到端联合优化，以进一步释放性能？这需要解决概念学习阶段的稳定性和持续学习阶段的灾难性遗忘之间的平衡。

2. **与其他正则化方法的联合效应**：CompSLOT 通过 $L_a$ 直接操作 logits，与现有的知识蒸馏、权重正则化等同样操作 logits 的持续学习方法结合时，会产生协同增益还是冲突？目前缺乏系统研究。

3. **更强编码器的潜力**：能否通过 DINOv2、更深的 ViT 或改进的 slot attention 机制（如引入迭代次数 $N_s$ 的自适应调节）来突破 substitutivity 属性上的性能瓶颈？Figure 12b 显示 $N_s=3$ 已是最优，暗示当前机制可能已接近 ViT-B/16 特征的信息上限。

4. **替代概念提取范式**：除 Slot Attention 之外，是否存在更有效或更高效的无监督概念提取方法（如基于 DINO 特征聚类、扩散模型特征分解），适用于长期持续学习场景？这关系到 CompSLOT 框架的概念学习模块是否可替换。

5. **开放世界与跨域泛化**：CompSLOT 的概念组合泛化能力在真实世界开放集、跨域持续学习场景下的表现如何？当前验证仅限于 CGQA、COBJ、ImageNet-R 等受控基准，未见域偏移或开放类别的实验证据。

6. **概念可解释性的量化**：Figure 4 和 Figure 9 提供了概念学习的可视化证据，但缺乏系统性的概念纯度、概念解耦度等量化指标。如何客观度量学到的 slots 是否真正对应语义概念，而非仅仅是空间分割的产物？

## 原文 PDF

![[paperPDFs/ICLR_2026/Plug_and_Play_Compositionality_for_Boosting_Continual_Learning_with_Foundation_Models.pdf]]
