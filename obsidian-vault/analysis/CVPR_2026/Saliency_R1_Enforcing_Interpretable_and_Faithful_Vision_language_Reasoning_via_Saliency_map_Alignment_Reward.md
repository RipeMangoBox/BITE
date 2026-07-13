---
title: "Saliency-R1: Enforcing Interpretable and Faithful Vision-language Reasoning via Saliency-map Alignment Reward"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Saliency_R1_Enforcing_Interpretable_and_Faithful_Vision_language_Reasoning_via_Saliency_map_Alignment_Reward.pdf
project_link: null
code_link: "https://github.com/peterant330/Saliency_R1"
aliases:
- SR
- Saliency-R1
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用显著性图与人工标注边界框的对齐分数作为GRPO奖励，引导模型在推理时将注意力聚焦于与问题相关的关键图像区域。
primary_logic: 提出了一种基于logits分解的高效显著性图计算方法，无需额外前向/反向计算；通过以思维令牌为瓶颈的注意力滚动机制，可视化从图像到答案的视觉信息流；并将显著性图对齐度作为GRPO奖励，在强化学习阶段强化模型对相关区域的关注，从而提升推理的忠实性和可解释性。
claims:
- 所提显著性图方法在忠实度指标（删除/插入测试）上达到或超越现有最先进方法（Table 1）。
- Saliency-R1在多个通用VQA基准上显著优于基模型，尤其在视觉中心任务上（如POPE +1.4%, ChartQA +4.2%）（Table 2）。
- 消融研究显示Saliency-R1超越Vision-R1平均1.5%（9个VQA基准），且仅使用显著性奖励的变体性能仅下降0.6%（Figure 4）。
- 可解释性评估（指向游戏）表明Saliency-R1将能量-PG和PG分别提升10.82%和14.14%（Table 3）。
---

# Saliency-R1: Enforcing Interpretable and Faithful Vision-language Reasoning via Saliency-map Alignment Reward

> [!tip] 核心洞察
> 提出了一种基于logits分解的高效显著性图计算方法，无需额外前向/反向计算；通过以思维令牌为瓶颈的注意力滚动机制，可视化从图像到答案的视觉信息流；并将显著性图对齐度作为GRPO奖励，在强化学习阶段强化模型对相关区域的关注，从而提升推理的忠实性和可解释性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Saliency-R1：通过显著性图对齐奖励增强视觉语言推理的可解释性与忠实性 |
| 英文题名 | Saliency-R1: Enforcing Interpretable and Faithful Vision-language Reasoning via Saliency-map Alignment Reward |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.04500) · [Code](https://github.com/peterant330/Saliency_R1) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Saliency-R1 |
| Dataset | COCO Caption, OpenPSG, POPE, ChartQA |

> [!tip] 效果简介
> - COCO Caption (Deletion 5%) 上，Deletion score ↓ 70.96 vs 76.42 (ATTN-LRP ) (-5.46)。
> - OpenPSG (Deletion 5%) 上，Deletion score ↓ 71.52 vs 84.55 (ATTN-LRP ) (-13.03)。
> - POPE 上，Accuracy 88.1 vs 86.7 (Qwen2.5-VL-7B base) (+1.4)。

## 概要

### 问题与瓶颈

视觉语言模型（VLM）在复杂推理任务中日益依赖思维链（Chain-of-Thought, CoT）机制，但该过程面临一个关键瓶颈：模型生成的推理步骤可能**过度依赖文本线索而忽视视觉证据**，导致思维链不忠实于图像内容，进而引发幻觉和不忠实的推理过程。如图 1 所示，即使最终答案正确，不同的思维过程可能关注图像中截然不同的区域；不忠实的思维过程往往聚焦于与问题无关的区域，或完全未利用图像信息。

### 核心思路

Saliency-R1 提出了一种**基于显著性图对齐奖励的强化学习框架**，其核心因果调节变量是：利用显著性图与人工标注边界框的对齐分数作为 GRPO（Group Relative Policy Optimization）奖励信号，引导模型在推理时将注意力聚焦于与问题相关的关键图像区域。该方法包含三个关键创新：

1. **高效的显著性图生成**：基于 logits 分解，直接计算每个令牌对最终预测的直接贡献，无需额外的前向或反向传播，即可为每个生成令牌产生图像区域的显著性图。
2. **以思维令牌为瓶颈的注意力滚动**：通过将思维令牌（thinking tokens）作为信息瓶颈，聚合视觉令牌到答案令牌的注意力流，可视化从图像到答案的视觉信息传播路径。
3. **显著性对齐奖励驱动的 GRPO**：将显著性图在人工标注框内的召回率作为奖励信号，与准确性奖励和格式奖励共同构成总奖励函数，在强化学习阶段强化模型对相关区域的关注。

### 方法定位

在方法谱系上，Saliency-R1 区别于传统的基于梯度（如 Grad-CAM）或基于扰动（如 ATTN-LRP）的显著性图方法，其 logits 分解方案在忠实度指标（删除/插入测试）上达到或超越现有最先进方法（Table 1）。在训练范式上，相较于仅使用准确性奖励的 Vision-R1（无显著性奖励的 GRPO 训练），Saliency-R1 在 9 个 VQA 基准上平均提升 1.5%（Figure 4）。与仅做监督微调（SFT）冷启动的 Saliency-R1-CI 相比，GRPO 结合显著性奖励的组合带来了更显著的性能增益。该方法在知识库中定位为一种**将可解释性约束直接融入强化学习训练**的视觉推理增强框架，基座模型为 Qwen2.5-VL-3B/7B。

### 主要结果

- **忠实度**：所提显著性图方法在 COCO Caption 和 OpenPSG 的删除测试中显著优于 ATTN-LRP 等基线（Table 1）。
- **VQA 性能**：Saliency-R1 在多个通用 VQA 基准上显著优于基模型，尤其在视觉中心任务上表现突出——POPE 准确率提升 1.4 个百分点（88.1 vs. 86.7），ChartQA 提升 4.2 个百分点（88.2 vs. 84.0），MME 得分提升 83 分（2385 vs. 2302）（Table 2）。
- **可解释性**：在指向游戏（Pointing Game）评估中，能量-PG 和 PG 指标分别提升 10.82% 和 14.14%（Table 3）；人类评估中解释质量评分从基模型的 3.6 显著提升至 4.5（p<0.05）。
- **消融实验**：仅使用显著性奖励的 Saliency-R1-pure 变体平均准确率仅比完整 Saliency-R1 低 0.6%，表明显著性奖励本身即可提供有效训练信号（Figure 4）。



视觉语言模型（VLMs）在复杂推理任务中展现出巨大潜力，近期研究进一步引入思维链（Chain-of-Thought, CoT）机制，使模型能够生成显式的中间推理步骤，从而提升多模态理解的准确性与可解释性。然而，一个关键瓶颈逐渐浮现：**VLMs在推理过程中存在过度依赖文本线索、忽视视觉证据的倾向**。模型生成的CoT可能表面上逻辑自洽，但实际上并不忠实于图像内容——其注意力可能聚焦于与问题无关的图像区域，甚至完全未有效利用视觉信息。这种“不忠实的推理”（unfaithful reasoning）直接导致幻觉现象，削弱了模型在视觉中心任务上的可靠性。

现有可解释性方法试图通过可视化模型的注意力分布来揭示其决策依据，但面临多重缺口。基于梯度的方法（如Grad-CAM）或基于注意力的方法（如Attention Rollout）通常需要额外的反向传播或前向计算，计算开销大，难以集成到大规模训练流程中。更为关键的是，这些方法大多停留在“事后解释”层面，**缺乏将可解释性信号反馈到模型训练中的机制**，无法从根本上约束模型在推理时真正关注视觉证据。

本文的动机源于一个核心观察（Figure 1）：即使模型最终给出了正确答案，其推理过程中关注的图像区域也可能截然不同——忠实的推理聚焦于与问题相关的关键区域，而不忠实的推理则游移于无关背景甚至完全忽略图像。这一洞察驱动了一个自然的问题：**能否设计一种高效的显著性图方法，不仅可视化从视觉到推理再到答案的信息流，更将其作为奖励信号嵌入强化学习过程，从而强制模型在推理时聚焦于正确的视觉证据？**

Saliency-R1正是沿着这一思路展开：通过基于logits分解的高效显著性图计算，以思维令牌为瓶颈的注意力滚动机制，以及将显著性图与人工标注边界框的对齐分数作为GRPO奖励，构建了一个端到端的“可解释性驱动训练”框架，旨在同时提升VLM推理的忠实性与可解释性。



## 核心方法与创新机理

Saliency-R1 的核心创新在于将**显著性图对齐奖励**引入视觉语言模型的强化学习训练，通过三个紧密耦合的技术模块，系统性地解决了模型推理过程中“看错地方”或“不看图像”的忠实性问题。

### 1. 基于 Logits 分解的高效显著性图生成

传统显著性图方法（如 Grad-CAM、ATTN-LRP）依赖梯度计算或额外的前向/反向传播，计算开销大，难以集成到强化学习训练循环中。Saliency-R1 提出了一种**基于 logits 分解的直接贡献计算方法**。

核心思想是：将每个生成令牌对最终预测 logits 的贡献，分解为所有上下文令牌在每一层 Transformer 中的注意力加权值向量的线性叠加。具体而言，令牌 $p$ 对预测下一个令牌的 logits 的直接贡献 $c_p$ 可表示为：

$$c_p = \sum_{l=1}^L \sum_{j=1}^H \alpha_{i,j,p}^l \mathbf{W}_{o,j}^l \mathbf{W}_{v,j}^l \mathbf{h}_p^{l-1} \mathbf{E}_u$$

其中 $\alpha_{i,j,p}^l$ 是第 $l$ 层第 $j$ 个注意力头中令牌 $i$ 对令牌 $p$ 的注意力权重，$\mathbf{W}_{v,j}^l$ 和 $\mathbf{W}_{o,j}^l$ 分别为值投影矩阵和输出投影矩阵，$\mathbf{E}_u$ 是词表嵌入矩阵。

**关键优势**：该方法所需的注意力权重和 KV 缓存项在模型前向推理时已经存在，无需任何额外的计算图构建或反向传播。这使得显著性图生成可以无缝嵌入到 GRPO 训练流程中，而不会显著增加训练成本。

### 2. 以思维令牌为瓶颈的全局显著性图聚合

视觉语言模型的推理过程通常包含“思维链”（Chain-of-Thought），即模型在给出最终答案前会生成一系列推理令牌（`<think>...</think>` 内的内容）。这些思维令牌是视觉信息流向答案的关键中介。

Saliency-R1 提出了一种**以思维令牌为瓶颈的注意力滚动机制**。与直接聚合答案令牌的显著性图不同，该方法通过矩阵乘法将视觉令牌到思维令牌的注意力权重（$\mathcal{A}_{vt}$）与思维令牌到答案令牌的注意力权重（$\mathcal{A}_{ta}$）进行组合：

$$\tilde{\mathcal{A}}_{va}^{l,h} = \mathcal{A}_{vt}^{l,h} \mathcal{A}_{ta}^{l,h}$$

这一操作本质上追踪了“图像区域 → 推理过程 → 最终答案”的完整信息流路径。思维令牌在此充当了**信息瓶颈**，强制模型在推理时聚焦于对答案真正关键的图像区域，从而生成更具可解释性的显著性图。

### 3. 显著性图对齐奖励驱动的 GRPO 训练

前述两个模块提供了生成高质量显著性图的技术基础，但真正的创新在于**将显著性图作为强化学习的奖励信号**。

Saliency-R1 在标准的 GRPO（Group Relative Policy Optimization）框架中，除了准确性奖励 $\mathcal{R}_{\text{accuracy}}$ 和格式奖励 $\mathcal{R}_{\text{format}}$ 之外，引入了第三个奖励项——显著性图对齐奖励 $\mathcal{R}_{\text{saliency}}$：

$$\mathcal{R}_{\text{overall}} = \mathcal{R}_{\text{accuracy}} + \mathcal{R}_{\text{format}} + \mathcal{R}_{\text{saliency}}$$

对齐奖励的计算方式为：显著性图在人工标注边界框内的召回率，即：

$$\mathrm{Alignment.Score} = \frac{\sum_{i \in \mathrm{Bounding~Box}} \mathrm{Saliency.Score}(i)}{\sum_{i \in \mathrm{Image}} \mathrm{Saliency.Score}(i)}$$

通过 GRPO 优化，模型被引导在推理时将其注意力集中到与问题相关的关键图像区域。消融实验表明，仅使用显著性奖励的 Saliency-R1-pure 变体在 9 个 VQA 基准上的平均准确率仅比完整 Saliency-R1 低 0.6%，而替换为原始注意力聚合的 Saliency-R1-attn 或去掉注意力滚动的 Saliency-R1-think 变体均出现性能下降，验证了所提方法的有效性。



Saliency-R1 的整体框架由三个紧密耦合的模块构成，形成一条“显著性感知推理—显著性图聚合—强化学习对齐”的闭环流水线。其核心设计理念是：**通过高效计算模型在推理过程中对图像区域的注意力分布，并将其与人工标注的语义边界框对齐，从而以强化学习的方式引导模型聚焦于与问题相关的视觉证据**。

### 流水线总览

如图 Figure 2 所示，整个框架包含以下三个关键阶段：

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. (a) Illustration of saliency map techniques based on logits decomposition. (b) Illustration of attention rollout for generating saliency maps with thinking tokens as the bottleneck. (c) GRPO with saliency maps alignment reward*

1. **基于 Logits 分解的令牌级显著性图生成**（Section 3.1）：在模型自回归生成过程中，利用注意力权重和 KV 缓存中已有的值投影项，直接计算每个生成令牌对最终 logits 的贡献，并通过 ReLU 过滤得到该令牌对应的图像显著性图。此过程**无需额外的前向或反向传播**，仅依赖简单的矩阵运算，因此可无缝集成到后训练流程中。

2. **以思维令牌为瓶颈的整体显著性图聚合**（Section 3.2）：将推理过程中产生的思维令牌（`<think>...</think>` 内的内容）作为信息瓶颈，通过注意力滚动机制（attention rollout）将视觉令牌到思维令牌的注意力矩阵 $\mathcal{A}_{vt}$ 与思维令牌到答案令牌的注意力矩阵 $\mathcal{A}_{ta}$ 相乘，得到视觉令牌对答案令牌的间接注意力 $\tilde{\mathcal{A}}_{va}$，从而可视化“从图像到最终答案”的视觉信息流。

3. **基于 GRPO 的显著性图对齐奖励训练**（Section 3.3）：将聚合后的显著性图与人工标注边界框的对齐分数（即框内显著性得分的召回率）作为奖励信号 $\mathcal{R}_{\mathrm{saliency}}$，与准确性奖励 $\mathcal{R}_{\mathrm{accuracy}}$ 和格式奖励 $\mathcal{R}_{\mathrm{format}}$ 相加构成总奖励 $\mathcal{R}_{\mathrm{overall}}$，通过 GRPO（Group Relative Policy Optimization）算法优化模型策略。

### 输入输出流

- **输入**：图像 $I$ 与自然语言问题 $q$。
- **推理生成**：模型以自回归方式生成包含思维链（CoT）和最终答案的完整响应。
- **显著性图计算**：在生成过程中同步提取每个令牌对图像区域的注意力贡献，经聚合后得到与答案相关的整体显著性图。
- **奖励计算**：将显著性图与人工标注边界框计算对齐分数，结合答案准确性和格式合规性，形成标量奖励信号。
- **策略更新**：GRPO 根据奖励信号更新模型参数，强化模型在推理时关注正确图像区域的行为。

### 设计动机

如 Figure 1 所示，即使模型最终给出了正确答案，其推理过程（思维链）可能关注的是图像中与问题无关的区域，这种“不忠实”的推理过程容易导致幻觉。Saliency-R1 通过将显著性图对齐度纳入奖励函数，直接作用于模型的推理行为，使其在生成思维链时主动聚焦于视觉证据所在的区域，从而提升推理的忠实性和可解释性。

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/001_Figure_1.jpg]]
*Figure 1: Main motivation of this work. Different thinking processes might focus on distinct regions of an image, even if they arrive at the correct answer. Unfaithful thinking processes either focus on irrelevant parts of the image or fail to consider the image*



Saliency-R1 方法由三个核心模块构成，分别解决显著性图生成、全局聚合和强化学习对齐问题。

### 3.1 基于 Logits 分解的令牌级显著性图生成

传统显著性图方法依赖梯度计算或输入扰动，需要额外的前向/反向传播。Saliency-R1 提出了一种基于 logits 分解的直接贡献计算方法，其核心思想是将模型预测下一个令牌的对数概率（logits）分解为所有上下文令牌的一阶贡献。

具体而言，Transformer 第 $l$ 层的输出可分解为：

$$h_i^l = h_i^{l-1} + A_i^l + F_i^l$$

其中 $h_i^{l-1}$ 为前一层的隐藏状态，$A_i^l$ 为自注意力输出，$F_i^l$ 为前馈网络输出。注意力输出进一步按注意力头展开：

$$A_i^l = \sum_{j=1}^H \sum_{p=1}^i \alpha_{i,j,p}^l W_{o,j}^l W_{v,j}^l h_p^{l-1}$$

基于此分解，令牌 $p$ 对最终预测令牌的对数概率的直接贡献 $c_p$ 可计算为：

$$c_p = \sum_{l=1}^L \sum_{j=1}^H \alpha_{i,j,p}^l W_{o,j}^l W_{v,j}^l h_p^{l-1} E_u$$

其中 $L$ 为总层数，$H$ 为注意力头数，$\alpha_{i,j,p}^l$ 为第 $l$ 层第 $j$ 个注意力头中令牌 $i$ 对令牌 $p$ 的注意力权重，$W_{o,j}^l$ 和 $W_{v,j}^l$ 分别为输出投影和值投影矩阵，$E_u$ 为词表嵌入矩阵中对应预测令牌的向量。对图像令牌计算 $c_p$ 后，应用 ReLU 过滤负贡献，即可得到每个生成令牌对应的图像区域显著性图。

**效率优势**：该方法无需额外前向/反向计算，因为注意力权重和 KV 缓存中的 $W_{v,j}^l h_p^{l-1}$ 项在正常推理过程中已经可用，仅需简单的矩阵运算即可完成显著性图生成。

### 3.2 以思维令牌为瓶颈的全局显著性图聚合

单个令牌的显著性图仅反映该令牌对图像区域的关注，无法展现从视觉输入到最终答案的完整信息流。为此，Saliency-R1 提出以思维令牌为瓶颈的注意力滚动机制。

该方法利用视觉令牌（$v$）到思维令牌（$t$）的注意力矩阵 $\mathcal{A}_{vt}^{l,h}$，以及思维令牌到答案令牌（$a$）的注意力矩阵 $\mathcal{A}_{ta}^{l,h}$，通过矩阵乘法构建视觉到答案的间接注意力：

$$\tilde{\mathcal{A}}_{va}^{l,h} = \mathcal{A}_{vt}^{l,h} \mathcal{A}_{ta}^{l,h}$$

这一操作将思维令牌作为信息传播的瓶颈，聚合了从视觉区域经由推理过程最终到达答案的注意力流。对所有层和注意力头进行平均后，即可得到全局显著性图，可视化驱动推理和最终答案的关键图像区域。

### 3.3 显著性图对齐奖励驱动的 GRPO 训练

在强化学习阶段，Saliency-R1 在标准 GRPO（Group Relative Policy Optimization）框架中引入显著性图对齐奖励，引导模型在推理时聚焦与问题相关的图像区域。

**对齐分数**定义为显著性图在人工标注边界框内的召回率：

$$\mathrm{Alignment.Score} = \frac{\sum_{i \in \mathrm{Bounding~Box}} \mathrm{Saliency.Score}(i)}{\sum_{i \in \mathrm{Image}} \mathrm{Saliency.Score}(i)}$$

**总奖励函数**由三部分组成：

$$\mathcal{R}_{\mathrm{overall}} = \mathcal{R}_{\mathrm{accuracy}} + \mathcal{R}_{\mathrm{format}} + \mathcal{R}_{\mathrm{saliency}}$$

其中 $\mathcal{R}_{\mathrm{accuracy}}$ 通过 LLM-as-judge 计算（正确为 1，错误为 0），$\mathcal{R}_{\mathrm{format}}$ 检查推理过程是否包含在 `<think></think>` 标签内（符合格式为 1，否则为 0），$\mathcal{R}_{\mathrm{saliency}}$ 即为上述对齐分数。

**GRPO 优化目标**为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{[q \sim \mathcal{D}, \{o_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}(\cdot|q)]} \frac{1}{G} \sum_{i=1}^G \left( M_i - \beta \mathbb{D}_{\mathrm{KL}}(\pi_\theta \| \pi_{\mathrm{ref}}) \right)$$

其中 $G$ 为每组采样数量，$M_i$ 为截断优势函数，$\beta$ 控制 KL 散度惩罚强度，$\pi_{\mathrm{ref}}$ 为参考策略。通过联合优化准确性、格式规范性和显著性对齐，模型在保持答案正确性的同时，显著提升推理过程的忠实性和可解释性。



## 实验与关键发现

### 4.1 实验设置简述

Saliency‑R1 以 **Qwen2.5‑VL‑3B/7B‑Instruct** 为基础模型，冷启动阶段使用约 8 k 条带边界框标注的 VQA 数据做监督微调（Saliency‑R1‑CI），随后在相同数据上应用 **GRPO** 强化学习，奖励函数由三项组成：

$$
\mathcal{R}_{\mathrm{overall}} = \mathcal{R}_{\mathrm{accuracy}} + \mathcal{R}_{\mathrm{format}} + \mathcal{R}_{\mathrm{saliency}}
$$

其中准确率奖励由 LLM‑as‑judge 给出（0/1），格式奖励要求推理过程包裹在 `<think></think>` 标签内，显著性对齐奖励 $\mathcal{R}_{\mathrm{saliency}}$ 定义为显著性图在人工标注框内的召回率。训练中未引入额外视觉编码器或梯度计算，显著性图通过 logits 分解与注意力滚动在线生成。

### 4.2 显著性图忠实度评估

忠实度实验在 **COCO Caption** 和 **OpenPSG** 上采用删除/插入测试（Deletion ↓ / Insertion ↑）。以 Qwen2.5‑VL‑3B‑Instruct 为骨干，将所提方法与 **Raw Attention**、**Attention Rollout**、**Grad‑CAM**、**ATTN‑LRP**、**TAM** 等基线对比。

**Table 1** 的核心结论：
- **COCO Caption (Deletion 5%)**：Saliency‑R1 的删除分数为 **70.96**，显著优于 ATTN‑LRP（76.42）和 TAM（73.51），在 15% 删除比例下同样保持领先（59.45 vs 62.79）。
- **OpenPSG (Deletion 5%)**：Saliency‑R1 达到 **71.52**，相比 ATTN‑LRP（84.55）降低 13.03 点，优势更为明显。
- 在插入测试（Insertion ↑）上，所提方法在多数设置下与 SOTA 持平或略优。

这一结果的关键在于：logits 分解直接建模每个 token 对最终预测的贡献，避免了梯度近似或启发式聚合带来的偏差；同时 ReLU 过滤抑制了负贡献噪声，使显著性图更聚焦于真正驱动模型决策的图像区域。此外，该方法仅依赖注意力权重和 KV‑cache 中已有的中间量，**无需额外前向/反向计算**，在效率上天然适合嵌入训练管线。

### 4.3 VQA 基准主结果

**Table 2** 报告了 Saliency‑R1‑7B 在 9 个通用 VQA 基准上的性能，对比对象包括同等规模的 Qwen2.5‑VL‑7B、InternVL2‑8B、LLaVA‑OneVision‑7B 等开源模型，以及 GPT‑4o、Claude‑3.5 Sonnet 等闭源模型。

核心发现：
- **视觉中心任务提升显著**：POPE（幻觉检测）从基模型的 86.7 提升至 **88.1**（+1.4%），ChartQA 从 84.0 提升至 **88.2**（+4.2%），MME‑RealWorld 从 58.7 提升至 **62.9**（+4.2%）。这表明显著性奖励有效引导模型在推理时将注意力聚焦于与问题相关的图像区域，减少了依赖文本偏置导致的幻觉。
- **通用能力保持或小幅提升**：MME 得分从 2302 提升至 **2385**（+83），MMStar、MMBench 等基准上亦保持稳定或略有增益，说明显著性约束未损害模型的通用对话能力。
- **冷启动 SFT 的作用有限**：Saliency‑R1‑CI 在部分基准上甚至出现退化（如 POPE 下降 0.6%），凸显 GRPO + 显著性奖励才是性能提升的核心驱动力。

值得注意的是，Saliency‑R1‑7B 在 ChartQA 上已接近 GPT‑4o（88.4），而参数量仅为后者的数十分之一，显示出强化学习阶段注入视觉对齐信号的巨大潜力。

### 4.4 可解释性评估

可解释性实验从定量和定性两个维度展开。

**定量评估（Table 3）**：在 saliency‑r1‑8k 测试集上计算能量‑PG 和 PG 指标（指向游戏变体，衡量显著性图与人工标注框的一致性）。Saliency‑R1 将能量‑PG 从基模型的 62.31 提升至 **73.13**（+10.82%），PG 从 55.42 提升至 **69.56**（+14.14%）。冷启动模型 Saliency‑R1‑CI 的提升幅度远小于完整方法（能量‑PG +5.15%，PG +7.33%），再次验证 GRPO 阶段的关键作用。

**定性评估（Figure 3）**：可视化对比显示，基模型的显著性图常散落在无关背景区域，而 Saliency‑R1 的显著性图高度集中于人工标注框内，且推理链中引用的视觉证据与显著性高亮区域一致。附录 E.5 的人类评估进一步表明，Saliency‑R1 的解释质量评分（4.5/5）显著高于基模型（3.6/5），p < 0.05。

### 4.5 消融研究

**Figure 4** 和 **Table 9** 提供了系统的消融分析。

- **显著性奖励的贡献**：Vision‑R1（仅使用准确率+格式奖励，无显著性奖励）在 9 个 VQA 基准上的平均准确率低于 Saliency‑R1 约 **1.5%**。而 Saliency‑R1‑pure（仅使用显著性奖励，无准确率奖励）的平均准确率仅比完整 Saliency‑R1 低 **0.6%**，说明显著性对齐奖励本身已能提供强有力的学习信号，且与准确率奖励形成互补。
- **显著性图生成方法的影响**：将 logits 分解替换为原始注意力聚合（Saliency‑R1‑attn）导致性能明显下降，验证了所提直接贡献建模的有效性。替换为直接聚合思维令牌显著性图（Saliency‑R1‑think，无注意力滚动）同样性能不佳，证实了以思维令牌为瓶颈的必要性——该机制强制模型通过推理过程传递视觉信息，而非直接从图像跳跃至答案。
- **冷启动的影响**：Saliency‑R1‑CI 在部分基准上指标下降（如 POPE、MME），说明简单的 SFT 冷启动可能损害原模型的某些能力，需要更精细的课程设计。

### 4.6 鲁棒性与反事实测试

**Table 5** 的反事实实验中，对图像前景/背景分别注入不同 σ 的高斯噪声。Saliency‑R1 在噪声干扰下的性能衰减幅度始终小于基模型，尤其在前景噪声场景下优势明显，表明模型确实学会依赖正确的图像区域进行推理，而非记忆文本-答案的统计关联。

**Table 6** 的鲁棒性基准测试进一步显示，在 POPE 和 MME 图像上注入噪声后，Saliency‑R1 的准确率下降幅度更小，验证了方法的泛化性和鲁棒性。

### 4.7 效率分析

**Table 7** 的吞吐量分析表明，生成单张显著性图的平均耗时在可接受范围内（具体数值需查阅原文）。由于方法复用前向传播中已有的注意力权重和 KV‑cache，**不引入额外的前向/反向计算**，相比 Grad‑CAM 等需要梯度回传的方法具有显著的效率优势，适合嵌入大规模 RL 训练管线。

### 4.8 失败模式与局限性

尽管 Saliency‑R1 在多数基准上表现优异，仍存在以下局限：

1. **冷启动退化**：SFT 冷启动在部分基准上导致指标下降，说明直接微调可能损害原模型的某些能力，未来需探索渐进式课程学习或数据配比优化。
2. **间接贡献的忽略**：当前 logits 分解仅考虑每个 token 对最终 logits 的直接贡献，忽略了跨层、跨头的间接交互效应，在需要细粒度归因的场景下可能不够精确。
3. **边界框标注依赖**：奖励信号依赖人工标注的边界框，限制了训练数据的可扩展性。结合自动分割模型（如 SAM）或弱标注策略是潜在的改进方向。
4. **架构泛化性未验证**：当前实验仅在 Qwen2.5‑VL 系列上开展，在其他 VLM 架构（如 LLaVA‑OneVision、InternVL）上的有效性尚待验证。

### 4.9 与幻觉消除基线的对比

**Table 8** 将 Saliency‑R1 与专门设计的幻觉消除方法（如 **MFP‑3B**）进行对比。Saliency‑R1 在 POPE 等幻觉检测基准上达到或超越专用方法的性能，同时保持通用 VQA 能力不退化，体现了显著性对齐奖励在“治本”层面的优势——通过强化正确的视觉关注模式，而非仅仅抑制幻觉输出。

### 补充图表

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/004_Table_2.jpg]]
*Table 2: Effective Performance Compared to the SOTA Model. Our models are based on Qwen2.5-VL-7B-Instruct and Qwen2.5-VL-BB-Instruct. The reported performance of the base models are evaluated by lmms-eval [89]*

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/003_Table_1.jpg]]
*Table 1: Faithfulness experiment results. We use Qwen2.5-VL-3B-Instruct for experiments. Our saliency map technique achieves comparable or better faithfulness to SOTA methods regarding the deletion and insertion metrics. We leave the results on GranDf dataset in the Appendix. The best metric is bold and the second best metric is underlined*

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/012_Table_3.jpg]]
*Table 3: Evaluation of Interpretability. We calculate the energy-PG and PG metric on the test set of saliency-r1-8k dataset*

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/011_Figure_4.jpg]]
*Figure 4: Ablation Studies. Top: Average metrics on 9 VQA benchmarks. Bottom: Metrics on MME*

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/024_Table_9.jpg]]
*Table 9: Full Results of Ablation Studies. The best metric is bold and the second best is underlined*

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/014_Table_5.jpg]]
*Table 5: Counterfactual test results. We inject Gaussian noise with different σ to the foreground and background of the images, and prompt the model to answer visual questions*

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/015_Table_6.jpg]]
*Table 6: Robustness Benchmark. We compare Saliency-R1 with base model on several benchmarks that show the robustness and generalizability of the method. We inject Gaussian noise with different σ to the images of POPE and MME*

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/017_Table_8.jpg]]
*Table 8: Comparison with hallucination-reduction baselines*

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/013_Table_4.jpg]]
*Table 4: Faithfulness experiment results. We use Qwen2.5-VL-3B-Instruct for experiments. Our saliency map technique achieves comparable or better faithfulness to SOTA methods regarding the deletion and insertion metrics. The best metric is bold and the second best metric is underlined*

![[assets/figures/papers/paper_list_l2665_https_arxiv_org_abs_2604_04500/figures/016_Table_7.jpg]]
*Table 7: Throughput analysis. We report the average time to generate one saliency map using the saliency-r1-8k dataset*



## 定位与知识库关联

### 核心瓶颈与设计动机

视觉语言模型（VLM）在生成思维链（CoT）推理时，存在一个根本性缺陷：模型可能过度依赖文本线索而忽视视觉证据，导致推理过程不忠实于图像内容。即使最终答案正确，思维过程也可能关注无关区域或完全忽略图像信息（Figure 1）。这一瓶颈直接导致幻觉和不忠实的推理，尤其在视觉中心任务（如ChartQA、POPE）上表现受限。

Saliency-R1 的核心洞察在于：**将显著性图与人工标注边界框的对齐度作为强化学习的奖励信号，可以引导模型在推理时将注意力聚焦于问题相关的关键图像区域**。这一设计将“模型在看哪里”从被动解释升级为主动训练目标，实现了可解释性与任务性能的联合提升。

### 方法谱系中的定位

#### 相对于显著性图方法的演进

传统显著性图方法可大致分为三类：基于梯度的方法（如 **Grad-CAM** ）、基于注意力传播的方法（如 **Attention Rollout** 、**ATTN-LRP** ）以及基于扰动的方法（如 **TAM** ）。这些方法通常需要额外的梯度计算、前向/反向传播或多次推理，计算开销较大，难以集成到训练管线中。

Saliency-R1 提出的**基于logits分解的直接贡献计算方法**（Eq. 1）在以下方面形成突破：

1. **零额外计算**：利用推理过程中已有的注意力权重和KV缓存项，无需任何额外前向/反向计算。如原文所述，“Many attention implementations naturally support returning attention weights, and the term $\mathbf{W}_{v,j}^l \mathbf{\bar{h}}_p^{l-\bar{1}}$ is also available within KV cache”——这一设计使其天然适合集成到后训练管线中。

2. **忠实度达到或超越SOTA**：在COCO Caption和OpenPSG数据集上的删除/插入测试中，所提方法在多个指标上达到最优或次优（Table 1）。例如，在COCO Caption的5%删除测试中，Saliency-R1得分为70.96，显著优于ATTN-LRP的76.42（越低越好）；在OpenPSG上优势更为明显（71.52 vs. 84.55）。

3. **思维令牌瓶颈机制**：传统方法通常直接聚合答案令牌的注意力或显著性图，而Saliency-R1引入以思维令牌为瓶颈的注意力滚动机制（$\tilde{\mathcal{A}}_{va}^{l,h} = \mathcal{A}_{vt}^{l,h} \mathcal{A}_{ta}^{l,h}$），显式建模从视觉令牌到答案令牌的信息流路径。消融实验（Table 9）表明，替换为直接聚合（Saliency-R1-attn）或去除瓶颈设计（Saliency-R1-think）均导致性能下降，验证了该设计的必要性。

#### 相对于VLM推理增强方法的定位

在VLM推理增强领域，Saliency-R1与以下工作形成对比：

- **Vision-R1**（无显著性奖励的GRPO训练）：作为直接消融基线，Saliency-R1在9个VQA基准上平均超越Vision-R1约1.5%（Figure 4），证明显著性对齐奖励的独立贡献。

- **LLaVA-CoT-11B**：作为大型推理模型对比，Saliency-R1以更小的参数量（7B）在多个视觉中心基准上展现竞争力（Table 2）。

- **MFP-3B**：作为幻觉消除基线，Saliency-R1在幻觉敏感的POPE基准上达到88.1%，体现了通过注意力对齐抑制幻觉的有效性（Table 8）。

- 商业闭源模型（**GPT-4o** 、**Claude-3.5 Sonnet** ）：Saliency-R1在部分基准上接近甚至超越这些大规模商业模型，展示了开源路线在可解释推理上的潜力。

#### 相对于强化学习训练范式的定位

Saliency-R1采用GRPO（Group Relative Policy Optimization）作为训练算法，其奖励函数设计具有独创性：

$$\mathcal{R}_{\mathrm{overall}} = \mathcal{R}_{\mathrm{accuracy}} + \mathcal{R}_{\mathrm{format}} + \mathcal{R}_{\mathrm{saliency}}$$

其中$\mathcal{R}_{\mathrm{saliency}}$定义为显著性图在人工标注边界框内的召回率：

$$\mathrm{Alignment.Score} = \frac{\sum_{i \in \mathrm{Bounding~Box}} \mathrm{Saliency.Score}(i)}{\sum_{i \in \mathrm{Image}} \mathrm{Saliency.Score}(i)}$$

这一设计将可解释性目标直接编码为优化信号，区别于仅依赖准确性奖励的标准GRPO。消融实验（Figure 4）揭示了一个关键发现：仅使用显著性奖励的Saliency-R1-pure变体在9个基准上的平均准确率仅比完整Saliency-R1低0.6%，而纯准确性奖励的Vision-R1则低1.5%。这表明**显著性对齐本身对任务性能有强正向迁移作用**，而非仅仅是可解释性的附加目标。

### 适用边界与条件

1. **架构依赖**：当前方法仅在Qwen2.5-VL-3B/7B模型上验证，其logits分解方法依赖于Transformer架构的注意力权重和KV缓存可获取性。对于使用其他注意力机制（如线性注意力、稀疏注意力）或非Transformer架构的VLM，需要重新设计贡献计算方法。

2. **标注依赖**：奖励信号依赖人工标注的边界框，这限制了训练数据的可扩展性。当前使用saliency-r1-8k数据集进行训练，标注成本是规模化应用的主要瓶颈。

3. **直接贡献假设**：logits分解仅考虑令牌对最终logits的直接贡献（一阶泰勒展开），忽略了间接贡献路径。虽然原文指出这提高了计算效率，但在需要多跳视觉推理的复杂场景中可能遗漏关键信息流。

4. **冷启动敏感性**：SFT冷启动阶段（Saliency-R1-CI）在某些基准上导致指标下降（Table 2），说明直接微调可能损害原模型的某些能力，需要更精细的课程学习策略。

### 局限性与开放问题

#### 已识别的局限性

1. **间接贡献的忽略**：当前方法仅考虑直接贡献，虽然效率高，但在某些需要多步视觉推理的场景中可能不够全面，影响解释的精确性。

2. **标注可扩展性**：人工边界框标注成本高，限制了训练数据规模。原文也指出未来可结合自动分割（如SAM 3）或弱标注来降低成本。

3. **架构泛化性未验证**：仅在Qwen2.5-VL系列上实验，对其他主流VLM架构（如InternVL、LLaVA系列）的适用性未知。

4. **冷启动退化**：SFT冷启动在某些基准上导致性能下降，需要更仔细的课程设计以避免灾难性遗忘。

#### 开放研究问题

1. **更精细的对齐粒度**：能否利用更精细的分割标签（如SAM 3的像素级掩码）替代边界框，进一步提升显著性对齐的粒度和性能？

2. **奖励权重平衡**：显著性奖励与准确性奖励之间的平衡如何影响模型行为？是否存在最优权重？当前消融显示纯显著性奖励已接近完整奖励的性能，暗示可能存在更优的奖励组合策略。

3. **替代对齐指标**：除了边界框召回率，是否还有其他更有效的显著性对齐评价指标？例如考虑显著性分布的形状匹配或信息论指标。

4. **规模化扩展**：该方法如何扩展到更大规模的视觉语言模型（如Qwen-VL-30B或闭源模型）？计算效率优势在大模型上是否依然成立？

5. **多模态推理泛化**：该方法是否能有效泛化到多轮对话、视频理解或具身交互等更复杂的视觉推理场景？思维令牌瓶颈机制在这些场景中是否需要重新设计？



## 原文 PDF

![[paperPDFs/CVPR_2026/Saliency_R1_Enforcing_Interpretable_and_Faithful_Vision_language_Reasoning_via_Saliency_map_Alignment_Reward.pdf]]
