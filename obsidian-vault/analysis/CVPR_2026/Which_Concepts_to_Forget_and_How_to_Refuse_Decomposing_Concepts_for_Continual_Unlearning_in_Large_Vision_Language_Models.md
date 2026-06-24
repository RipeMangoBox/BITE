---
title: Which Concepts to Forget and How to Refuse? Decomposing Concepts for Continual Unlearning in Large Vision-Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Which_Concepts_to_Forget_and_How_to_Refuse_Decomposing_Concepts_for_Continual_Unlearning_in_Large_Vision_Language_Models.pdf
project_link: null
code_link: null
aliases:
- CCAR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将遗忘类别分解为细粒度视觉属性与文本意图的概念组合，并通过概念调制器精炼概念激活以抑制无关语义，再利用概念感知的混合拒绝专家生成定向拒绝，从而将拒绝行为建立在语义概念之上，减少虚假关联。
primary_logic: 概念级分解与精炼使遗忘更精确；概念调制器学习多模态概念组合以隔离遗忘类别，概念驱动的路由复用相关任务的拒绝专家，推理时校准抑制过度拒绝，使得模型能够持续、精确地忘掉特定视觉-指令对。
claims:
- CORE 在 Vicuna-LVLM 上实现了最高的 Last AR 88.02% 和 CRR 90.67%，远超最佳基线 O³（AR 81.76%, CRR 73.03%），证明其精确遗忘和效用保留能力。
- 消融实验表明，去掉概念调制器会使 Last AR 从 97.78% 降至 86.75%，CRR 从 86.19% 降至 71.14%，验证了概念精炼的必要性。
- 概念感知的 refuser 激活和路由使不同任务产生截然不同的 refuser 激活模式，避免了传统方法中少数 refuser 被反复覆盖问题。
- Safety benchmark (QA) + ImageNet-R (classification) - Vicuna 上 AR (Answer Rate) Last = 88.02
---

# Which Concepts to Forget and How to Refuse? Decomposing Concepts for Continual Unlearning in Large Vision-Language Models

> [!tip] 核心洞察
> 概念级分解与精炼使遗忘更精确；概念调制器学习多模态概念组合以隔离遗忘类别，概念驱动的路由复用相关任务的拒绝专家，推理时校准抑制过度拒绝，使得模型能够持续、精确地忘掉特定视觉-指令对。

| 字段 | 内容 |
|------|------|
| 中文题名 | 哪些概念该遗忘、如何拒绝？——面向大型视觉-语言模型持续遗忘的概念分解 |
| 英文题名 | Which Concepts to Forget and How to Refuse? Decomposing Concepts for Continual Unlearning in Large Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.21484) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CORE (COncept-aware REfuser) |
| Dataset | Safety benchmark (QA) + ImageNet-R (classification) - Vicuna |

> [!tip] 效果简介
> - Safety benchmark (QA) + ImageNet-R (classification) - Vicuna 上，AR (Answer Rate) Last 88.02 vs 81.76 (O^3) (+6.26)；CRR (Context-aware Refusal Rate) Last 90.67 vs 73.03 (O^3) (+17.64)；S (Specificity) Last 96.54 vs 92.85 (O^3) (+3.69)。

## 概述

持续遗忘（Continual Unlearning）要求大型视觉-语言模型（LVLM）在序贯任务中精确移除特定视觉-指令对的知识，同时保持其余能力不变。然而，现有方法面临两个核心挑战：**不相关拒绝**（新遗忘任务覆盖先前任务的拒绝模式，导致对遗忘查询产生语义错位的拒绝）和**过度拒绝**（模型错误地拒绝本应保留的查询）。这些问题的根源在于序贯遗忘更新扭曲了LVLM中高度纠缠的共享视觉-语言表示，产生虚假关联，使模型难以精确区分遗忘上下文。

针对上述瓶颈，本文提出 **CORE（COncept-aware REfuser）**，一种面向LVLM的概念感知持续遗忘框架。其核心洞察是：将遗忘类别分解为细粒度视觉属性与文本意图的概念组合，通过概念调制器精炼概念激活以抑制无关语义，再利用概念感知的混合拒绝专家生成定向拒绝，从而将拒绝行为建立在语义概念之上，减少虚假关联。在推理阶段，CORE通过校准机制根据查询与历史遗忘任务的相关性缩放拒绝贡献，有效抑制过度拒绝。

在Vicuna-LVLM上的实验表明，CORE在末步遗忘准确率（Last AR）和上下文感知拒绝率（Last CRR）上分别达到 **88.02%** 和 **90.67%**，显著优于最佳基线方法 O³（AR 81.76%, CRR 73.03%），证明了其在精确遗忘和效用保留方面的优势。消融实验进一步验证了概念调制器和概念感知路由的关键作用：移除概念调制器导致Last CRR下降约15个百分点，而去除概念感知激活则使平均CRR从88.14%骤降至54.53%。在遗忘-保留权衡曲线上，CORE始终位于帕累托前沿，展现出优越的持续遗忘能力。

## 背景与动机

大型视觉-语言模型（LVLM）在安全对齐后仍可能保留敏感知识，持续遗忘（continual unlearning）旨在序贯地移除模型对特定视觉-指令对的知识，同时维持模型在保留任务上的通用能力。然而，现有方法面临两个核心挑战：**不相关拒绝**（irrelevant refusal）和**过度拒绝**（over-refusal）。

**瓶颈根源：共享表示中的虚假关联。** LVLM 中的视觉与语言表示高度纠缠，序贯遗忘更新会扭曲这些共享表示，产生虚假关联。当模型学习遗忘新任务时，更新会覆盖之前任务的拒绝模式，导致对遗忘查询产生语义错位的拒绝（不相关拒绝）；同时，被扭曲的表示也会使模型在保留查询上错误触发拒绝行为（过度拒绝）。Figure 1 直观展示了这两种失效模式。

**现有方法缺口。** 传统的持续学习方法（如基于正则化的 **EWC**、基于蒸馏的 **LwF**）和持续遗忘方法（如 **GMM**、**EProj**、**SCRUB**、**O³**）要么直接对模型参数施加约束，要么使用统一的连接模块生成拒绝响应，但都未显式建模遗忘类别背后的细粒度语义概念。这导致它们在序贯遗忘过程中难以精确区分遗忘上下文，拒绝行为缺乏语义基础。

**本文动机：从概念分解到概念感知拒绝。** 本文提出核心洞察：遗忘一个视觉-指令对，本质上是遗忘其背后的视觉属性与文本意图的概念组合。通过将遗忘目标分解为细粒度概念，并对概念激活进行精炼以抑制无关语义，再基于概念相关性路由到专门的拒绝专家，可以将拒绝行为建立在可解释的语义概念之上，从而减少虚假关联，实现精确且持续的遗忘。

## 核心创新

CORE 的核心创新在于将 LVLM 持续遗忘从“直接操作视觉-文本特征”提升为“概念级分解与精炼驱动”的范式。其关键设计围绕以下四个 changed slots 展开：

**1. 遗忘目标表征：从原始特征到概念激活**

传统方法直接使用视觉特征 $x_{\mathrm{img}, i}^{t}$ 和文本 token 表示作为遗忘操作的输入，这种粗粒度表示在序贯更新中容易扭曲共享的视觉-语言表示，产生虚假关联。CORE 将每个遗忘类别分解为一组细粒度的视觉属性与文本意图概念，并通过概念模块（Visual/Textual Concept Module）为每个视觉-语言对生成概念激活 $E_{\mathrm{q}, i}^{t} = \bigoplus_{k \in \mathcal{K}^{1:t}} \pmb{\mathcal{E}}_{\mathrm{q}, k}(\pmb{x}_{\mathrm{q}, i}^{t})$（Equation 1），将遗忘操作锚定在可解释的语义概念上，从而从根本上减少了虚假关联的产生空间。

**2. 概念相关性甄别：从无甄别到概念调制器精炼**

基线方法缺乏对概念相关性的甄别机制，导致无关语义干扰遗忘精度。CORE 引入概念调制器（Concept Modulator）对概念激活进行重加权，输出精炼后的概念激活 $\bar{E}_{\mathfrak{q}, i}^{t} = \bigoplus_{k} m_{k} \cdot \pmb{\mathcal{E}}_{\mathfrak{q}, k}(x_{\mathfrak{q}, i}^{t})$（Equation 3），显式抑制与当前遗忘类别无关的概念。消融实验（Table 3）表明，移除概念调制器会使 Last CRR 从 86.19% 骤降至 71.14%，验证了概念精炼对精确遗忘的必要性。

**3. 拒绝响应生成：从统一模块到概念感知的混合拒绝专家**

传统方法使用统一的连接模块或直接微调来生成拒绝响应，导致不同遗忘任务的拒绝模式互相覆盖（不相关拒绝）。CORE 采用混合拒绝专家（Mixture of Refusers），通过概念感知的路由器（Router）计算各 refuser 的贡献权重 $\alpha_j$，生成概念定向的视觉特征偏移 $\Delta \mathcal{P}(x_{\mathrm{img}, i}^{t}) = \sum_{j=1}^{N_{R}} \alpha_{j} \cdot \mathcal{V}_{j}(x_{\mathrm{img}, i}^{t})$（Equation 4）。概念感知路由使不同任务产生截然不同的 refuser 激活模式（Figure B），避免了少数 refuser 被反复覆盖的问题。

**4. 序贯任务间行为保持：从正则化到概念驱动的复用与校准**

EWC、LwF 等基线依赖正则化项维持旧任务行为，MoEAdapter 则固定新参数，二者均未显式建模任务间的语义关系。CORE 通过任务间概念相关性 $r^{t'} = \sigma\left(\sin(\bar{E}_{\mathrm{img}}^{t}, \bar{E}_{\mathrm{img}}^{t'}) \cdot \sin(\bar{E}_{\mathrm{txt}}^{t}, \bar{E}_{\mathrm{txt}}^{t'})\right)$（Equation 5）驱动 refuser 的复用与抑制：相关任务的 refusers 被复用，无关者被抑制。推理时，校准机制根据查询与历史遗忘任务的相关性 $\beta$ 缩放 refuser 贡献 $\mathcal{P}(\bar{x}_{\mathrm{img}}) + \beta \cdot \Delta \mathcal{P}(\bar{x}_{\mathrm{img}})$（Equation 7），有效抑制过度拒绝。消融实验证实，移除概念感知激活（ACT）使 AVG CRR 从 88.14% 降至 54.53%，移除推理校准（CAL）则导致保留查询上的过度拒绝，印证了该设计的核心作用。

## 整体框架

CORE 将持续遗忘建模为**概念分解 → 概念精炼 → 概念感知拒绝**的三阶段流程，如图 Figure 2 所示。对于第 $t$ 个遗忘任务中的每个视觉-指令对，框架首先将其分解为细粒度视觉属性与文本意图的概念激活，随后通过概念调制器抑制无关语义、增强遗忘相关概念的响应，最后利用概念驱动的混合拒绝专家生成定向拒绝响应，并通过推理时校准抑制过度拒绝。

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/002_Figure_2.jpg]]
*Figure 2: An illustration of the proposed continual unlearning framework. For each vision-language pair to forget in the t-th task, (i) the concept modules produce activations for visual attributes and textual intents accumulated across tasks, and the concept modulator reweights them to emphasize relevant concepts by suppressing irrelevant ones. (ii) Given these concept activations, we compute their similarity with concepts from previous tasks to measure conceptual relevance. Based on this relevance, we leverage refusers associated with conceptually similar previous tasks or activate new ones for guiding the language model to generate concept-aware refusal responses*

### 输入与输出

**输入**：第 $t$ 个遗忘任务 $\mathcal{T}^t = \{x_i^t, q_i^t, a_i^t\}_{i=1}^{N^t}$，包含 $N^t$ 个视觉-指令-拒绝答案三元组。视觉编码器 $\mathcal{F}_v$ 从图像 $x_i^t$ 中提取视觉特征 $x_{\text{img},i}^t$，文本指令 $q_i^t$ 经语言模型的分词器处理为文本 token。

**输出**：经 refuser 混合偏移后的视觉特征 $\mathcal{P}(x_{\text{img},i}^t) + \Delta\mathcal{P}(x_{\text{img},i}^t)$ 被送入语言模型，使其在遗忘查询上生成拒绝响应，在保留查询上维持正常回答。

### 核心模块与数据流

1. **概念模块**（Visual/Textual Concept Module）：对视觉特征和文本 token 分别提取概念激活。对于每个遗忘类别，构建一组描述视觉属性和文本意图的概念集合 $\mathcal{K}$，通过预训练编码器计算输入与该类别概念的相似度，将所有已见任务的概念激活拼接为 $E_{\mathfrak{q},i}^t$（公式 1）。该模块通过概念对齐损失 $\mathcal{L}_{\text{con}}$ 优化，使激活值与预训练编码器的目标相似度一致（公式 2）。

2. **概念调制器**（Concept Modulator）：接收拼接后的概念激活，输出重加权系数 $m_k$，对每个概念维度进行缩放：$\bar{E}_{\mathfrak{q},i}^t = \bigoplus_k m_k \cdot \pmb{\mathcal{E}}_{\mathfrak{q},k}$（公式 3）。调制器抑制与当前遗忘类别无关的概念激活，使后续路由和拒绝生成聚焦于真正相关的语义维度。消融实验证实，移除该模块会导致 Last CRR 从 86.19% 降至 71.14%（Table 3），验证了概念精炼对精确遗忘的关键作用。

3. **混合拒绝专家**（Mixture of Refusers）：$N_R$ 个 refuser 子网络 $\mathcal{V}_j$ 对视觉特征产生偏移，最终偏移量为路由权重的加权和：$\Delta\mathcal{P}(x_{\text{img},i}^t) = \sum_{j=1}^{N_R} \alpha_j \cdot \mathcal{V}_j(x_{\text{img},i}^t)$（公式 4）。每个 refuser 可视为一种专门的“拒绝模式”，不同任务激活不同的 refuser 组合，避免了传统方法中少数 refuser 被反复覆盖的问题（Figure B 的热图可视化佐证了这一点）。

4. **概念感知路由**（Router）：利用精炼后的视觉和文本概念激活，计算当前任务与历史任务 $t'$ 的概念相关性 $r^{t'}$（公式 5）。路由通过对比损失 $\mathcal{L}_{\text{ref}}$（公式 6）进行训练：相关任务的 router 输出被拉近，无关任务的输出被推远。这使得概念相似的任务可以复用已有 refusers，概念不同的任务则激活新的 refusers，从而在序贯遗忘中维持拒绝行为的一致性。移除概念感知激活会导致 AVG CRR 从 88.14% 骤降至 54.53%，表明概念驱动的路由是维持持续遗忘能力的核心机制。

5. **推理校准**（Refusal Calibration）：推理时，计算查询与所有历史遗忘任务的最大相关性 $\beta$，将 refuser 偏移缩放为 $\beta \cdot \Delta\mathcal{P}(\bar{x}_{\text{img}})$（公式 7）。当查询与遗忘任务无关时，$\beta$ 趋近于 0，refuser 贡献被抑制，从而避免在保留查询上产生过度拒绝。消融实验表明，移除校准会降低 AR，因为 refuser 混合持续激活导致保留查询上的误拒。

### 关键设计逻辑

整个框架的核心瓶颈在于：序贯遗忘更新会扭曲 LVLM 中纠缠的共享视觉-语言表示，产生虚假关联，导致不相关拒绝（新任务覆盖旧任务的遗忘模式）和过度拒绝（误拒保留查询）。CORE 的应对策略是将遗忘行为建立在**语义概念层面**而非原始特征层面——概念调制器精炼出与遗忘类别真正相关的语义维度，概念感知路由基于语义相关性决定 refuser 的复用或新建，推理校准则根据查询与遗忘任务的概念距离动态调节拒绝强度。三者协同，使得模型能够持续、精确地忘掉特定视觉-指令对，同时最大限度保留通用能力。

### 补充图表

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/001_Figure_1.jpg]]
*Figure 1: Challenges in continual unlearning of large visionlanguage models emerge as sequential unlearning updates distort entangled visual-language representations, making it difficult to preserve contextually appropriate refusal behavior across tasks. (a) Irrelevant refusal: Learning new forget tasks overwrites prior refusal patterns, generating contextually misaligned refusals. (b) Over-refusal: The model inappropriately refuses retain queries*

## 核心模块与公式推导

CORE 框架围绕“概念分解—概念精炼—概念感知拒绝”三条主线构建，其核心由四个功能模块组成：视觉/文本概念模块、概念调制器、混合拒绝专家与路由器，以及推理校准模块。整体流程如 Figure 2 所示。

### 3.1 遗忘任务形式化与特征提取

在第 $t$ 个遗忘任务中，给定 $N^t$ 个视觉-指令-拒绝答案三元组：

$$T^{t} = \{ x_{i}^{t}, q_{i}^{t}, a_{i}^{t} \}_{i=1}^{N^{t}}$$

其中 $x_i^t$ 为输入图像，$q_i^t$ 为对应指令，$a_i^t$ 为期望的拒绝回答。视觉编码器 $\mathcal{F}_v$ 首先提取图像特征：

$$x_{\mathrm{img}, i}^{t} = \mathcal{F}_{v}(x_{i}^{t})$$

该特征将作为后续概念提取和拒绝变换的基础输入。

### 3.2 概念分解与精炼

#### 3.2.1 概念模块与概念激活

CORE 为每个遗忘类别预定义一组细粒度概念描述，涵盖视觉属性（如颜色、纹理、形状）和文本意图（如问题类型、语义倾向）。对于第 $t$ 个任务中的输入，视觉概念模块和文本概念模块分别计算输入与所有历史任务累积的概念集合 $\mathcal{K}^{1:t}$ 中每个概念的激活值，并拼接为统一的概念激活向量：

$$E_{\mathrm{q}, i}^{t} = \bigoplus_{k \in \mathcal{K}^{1:t}} \pmb{\mathcal{E}}_{\mathrm{q}, k}(\pmb{x}_{\mathrm{q}, i}^{t})$$

其中 $\mathrm{q} \in \{\mathrm{img}, \mathrm{txt}\}$ 分别表示视觉和文本模态，$\pmb{\mathcal{E}}_{\mathrm{q}, k}$ 为第 $k$ 个概念的概念编码器，$\oplus$ 表示拼接操作。为训练概念编码器使其激活与预训练语义空间对齐，引入概念对齐损失：

$$\mathcal{L}_{\mathrm{con}} = - \sum_{\mathrm{q}} \sum_{i} \mathrm{sim}(E_{\mathrm{q}, i}^{t}, \hat{E}_{\mathrm{q}, i})$$

该损失最大化概念激活 $E_{\mathrm{q}, i}^{t}$ 与预训练编码器目标相似度 $\hat{E}_{\mathrm{q}, i}$ 之间的余弦相似度，使概念模块学会提取与遗忘类别语义一致的概念表征。

#### 3.2.2 概念调制器

原始概念激活可能包含与当前遗忘类别无关的语义噪声。概念调制器通过可学习的调制权重 $m_k$ 对每个概念激活进行重加权：

$$\bar{E}_{\mathfrak{q}, i}^{t} = \bigoplus_{k} m_{k} \cdot \pmb{\mathcal{E}}_{\mathfrak{q}, k}(x_{\mathfrak{q}, i}^{t})$$

调制器的作用是**抑制无关概念、放大相关概念**，从而精炼出与当前遗忘任务高度相关的概念组合。消融实验证实，移除概念调制器会导致 Last CRR 下降约 15 个百分点（Table 3），验证了概念精炼对精确遗忘的关键作用。

### 3.3 概念感知的混合拒绝专家

#### 3.3.1 Refuser 混合与路由

CORE 维护一组可学习的拒绝专家（refusers）$\{\mathcal{V}_j\}_{j=1}^{N_R}$，每个 refuser 以图像特征为输入，输出一个视觉特征偏移量。第 $t$ 个任务的 refuser 混合输出为所有 refuser 的加权和：

$$\Delta \mathcal{P}(x_{\mathrm{img}, i}^{t}) = \sum_{j=1}^{N_{R}} \alpha_{j} \cdot \mathcal{V}_{j}(x_{\mathrm{img}, i}^{t})$$

其中权重 $\alpha_j$ 由路由器根据当前任务的概念激活与历史任务概念激活的相似度动态计算。具体而言，当前任务 $t$ 与历史任务 $t'$ 之间的概念相关性定义为：

$$r^{t'} = \sigma\left(\sin(\bar{E}_{\mathrm{img}}^{t}, \bar{E}_{\mathrm{img}}^{t'}) \cdot \sin(\bar{E}_{\mathrm{txt}}^{t}, \bar{E}_{\mathrm{txt}}^{t'})\right)$$

该公式通过图像概念激活和文本概念激活的平均余弦相似度的乘积，经 sigmoid 函数 $\sigma$ 映射为 $[0,1]$ 区间的相关性分数。**概念相关性高的历史任务，其关联的 refusers 被复用；相关性低的任务，其 refusers 被抑制**，从而避免传统方法中少数 refuser 被反复覆盖的问题（Figure B 热图验证了这一点）。

路由器的训练通过 refuser 激活损失实现：

$$\mathcal{L}_{\mathrm{ref}} = \sum_{t'=1}^{t-1} \left[ r^{t'} \cdot \ell_{+}(F^{t}, F^{t'}) + (1 - r^{t'}) \cdot \ell_{-}(F^{t}, F^{t'}) \right]$$

其中 $F^t$ 为第 $t$ 个任务的路由器输出，$\ell_{+}$ 鼓励相关任务的输出相似，$\ell_{-}$ 鼓励无关任务的输出相异。这种对比学习机制使路由器学会基于概念语义进行精确的 refuser 分配。

#### 3.3.2 推理校准

在推理阶段，为防止 refuser 混合持续激活导致保留查询上的过度拒绝，CORE 引入自适应校准。对于推理查询 $\bar{x}_{\mathrm{img}}$，计算其与所有历史遗忘任务的最大概念相关性 $\beta \in [0,1]$，并按比例缩放 refuser 贡献：

$$\mathcal{P}(\bar{x}_{\mathrm{img}}) + \beta \cdot \Delta \mathcal{P}(\bar{x}_{\mathrm{img}})$$

当查询与任何遗忘任务的概念相关性较低时，$\beta$ 趋近于 0，refuser 贡献被抑制，模型正常回答；当查询与遗忘任务高度相关时，$\beta$ 趋近于 1，refuser 完全激活，模型产生拒绝响应。消融实验表明，移除校准模块会导致 AR 下降（Section 4.3），印证了校准对抑制过度拒绝的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/011_Figure.jpg]]
*Figure: B. Visualization of refuser activation frequency for each task (a) with and (b) without relevance guided refuser activation*

## 实验与分析

### 主实验结果

CORE 在两个主流 LVLM 架构和两类下游任务上均展现出显著的性能优势。Table 1 报告了基于 Vicuna-LVLM 的主要结果。在反映最终遗忘效果与效用保留的 Last 指标上，CORE 的 Answer Rate（AR）达到 88.02%，Context-aware Refusal Rate（CRR）达到 90.67%，分别超出最强基线 **O³** 6.26 和 17.64 个百分点。这一差距的根源在于：序贯遗忘更新会扭曲 LVLM 中高度纠缠的视觉-语言共享表示，O³ 等基线方法直接对连接模块施加更新，导致先前任务的遗忘模式被覆盖（不相关拒绝）以及保留查询被误拒（过度拒绝）。CORE 通过将遗忘目标分解为概念组合，并利用概念感知路由复用相关任务的拒绝专家，从根本上缓解了这两类失效模式。在 Specificity（S）指标上，CORE 达到 96.54%，表明其拒绝响应高度聚焦于目标遗忘上下文，几乎不产生语义错位的拒绝。

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/003_Table_1.jpg]]
*Table 1: Results of the proposed and compared methods using the Vicuna-based LVLM. The performance is reported in terms of Avg and Last. (↑) and (↓) indicate that higher and lower values are better, respectively*

Table 2 展示了基于 Llama-2-LVLM 的结果，CORE 同样保持一致的领先趋势，验证了方法对不同语言模型骨干的鲁棒性。Figure 3 进一步揭示了各方法在序贯遗忘步骤中的性能退化轨迹：基线方法（如 EWC、LwF、GMM）在步骤推进过程中，保留数据的通用能力持续下滑，而 CORE 的曲线几乎持平，说明概念分解与精炼机制有效隔离了遗忘更新对共享表示的侵蚀。

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/006_Table_2.jpg]]
*Table 2: Results of using the Llama-2-based LVLM*

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/004_Figure_3.jpg]]
*Figure 3: Performance across sequential unlearning steps. We report average performance on the LVLM benchmarks and retain data (top) and the forget data (bottom) after each unlearning step*

Figure 4 绘制了 AR 与 CRR 的权衡曲线。CORE 在两个骨干上均位于帕累托前沿，意味着在同等遗忘精度下，CORE 能保留更高的回答能力；或在同等保留率下，实现更彻底的遗忘。这一前沿位置直接源于概念调制器对无关语义的抑制——传统方法在遗忘某一类别时，不可避免地抑制了与之共享视觉或语言概念的保留类别，而 CORE 通过精炼概念激活将更新约束在目标概念子空间内。

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/007_Figure_4.jpg]]
*Figure 4: Trade-off between AR on the retain data and CRR on the forget data using Vicuna (left) and Llama-2 (right)*

### 消融实验

Table 3 的系统消融揭示了各组件的因果贡献：

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/005_Table_3.jpg]]
*Table 3: Ablation results with different component combinations*

**概念调制器（MOD）**：移除调制器后，Last CRR 从 86.19% 骤降至 71.14%，Last AR 从 97.78% 降至 86.75%。调制器的作用是双重的：一方面，它通过重加权概念激活，将遗忘更新聚焦于真正贡献于目标类别的视觉属性和文本意图；另一方面，它抑制了无关概念的激活扩散，防止虚假关联的形成。Figure 6 的可视化直接佐证了这一点——无调制器时，top-5 概念激活中频繁出现与遗忘类别无关的描述（红色标注），而有调制器时激活高度集中于目标类别相关概念。

**概念感知路由激活（ACT）**：当用无概念引导的均匀路由替代概念感知路由时，Average CRR 从 88.14% 暴跌至 54.53%。这一降幅远超其他消融项，揭示了概念感知路由是维持持续遗忘能力的核心机制。其因果链条为：无概念引导时，路由无法区分当前遗忘任务与历史任务的概念相似性，导致不相关任务的 refuser 被错误激活，覆盖了先前建立的拒绝模式。Figure B 的热图直观展示了这一差异——有概念引导时，每个任务的 refuser 激活呈现截然不同的模式，而无引导时少数 refuser 被反复激活，形成灾难性覆盖。

**推理校准（CAL）**：移除推理时的 β 缩放机制后，AR 明显下降，因为 refuser 混合持续激活导致保留查询被过度拒绝。校准模块通过计算推理查询与历史遗忘任务的概念相关性 β，自适应地缩放 refuser 贡献，从而在不牺牲遗忘精度的前提下恢复保留查询的正常响应。

**概念数量的影响**：Table B 显示，每个遗忘类别使用 4-8 个概念描述即可达到性能饱和，更多概念带来的增益边际递减，验证了概念分解的高效性。Table C 进一步表明，使用不同 LLM（GPT、Gemini、Claude）生成的概念描述，性能波动极小，说明 CORE 对概念描述的来源风格不敏感，框架具有实际部署的鲁棒性。

### 定性分析

Figure 5 展示了序贯遗忘过程中的响应变化。对于遗忘样本（上图），基线方法在后续任务更新后，对早期遗忘样本的拒绝响应变得语义错位（如对“暴力内容”的拒绝变成了对“隐私信息”的拒绝），这正是不相关拒绝的典型表现；而 CORE 始终保持上下文一致的合适拒绝。对于保留样本（中、下图），基线方法出现误拒（红色框标注），CORE 则持续给出恰当回答。Figure C 进一步展示了最高和最低概念激活与对应拒绝响应的关联：高激活概念与拒绝响应的语义高度一致，低激活概念几乎不影响响应生成，验证了概念精炼的有效性。

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/008_Figure_5.jpg]]
*Figure 5: Response changes during sequential unlearning for randomly selected forget (top) and retain (middle and bottom) samples. Comparison methods often produce semantically misaligned refusals for forget queries or mistakenly reject retain queries (red boxes), whereas ours consistently yields appropriate refusals for forget samples and suitable responses for retain samples*

### 失败模式与局限性

尽管 CORE 在多数场景下表现优异，但分析中仍存在需要手动验证的潜在边界。首先，概念描述的质量依赖于预定义的概念集合（Table E），若遗忘类别涉及高度抽象或跨模态的复合概念，人工构建的概念描述可能无法充分覆盖其语义空间，导致遗忘不彻底。其次，概念调制器的训练依赖于预训练编码器提供的目标相似度 $\hat{E}_{\mathrm{q}, i}$，若该编码器对特定领域（如医学影像）的语义理解不足，调制器的精炼效果可能退化。最后，当前实验在 12 个序贯遗忘任务的设定下验证，更长时间尺度（如数十个任务）下的概念激活漂移和 refuser 容量饱和问题尚未被充分探索，需在实际部署中进一步评估。

### 补充图表

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/010_Figure.jpg]]
*Figure: A. Results of a different task order using Vicuna-based LVLM*

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/012_Table.jpg]]
*Table: B. Additional results with varying numbers of concept descriptions for each forget category*

![[assets/figures/papers/paper_list_l811_https_arxiv_org_abs_2603_21484/figures/009_Figure_6.jpg]]
*Figure 6: Visualization of the visual and textual concept descriptions corresponding to the top-5 activations from the concept modules for each vision-language pair in forget categories. The blue and gray boxes represent descriptions from CORE with and without the concept modulator, respectively. Descriptions that do not belong to the forget category of the given sample are shown in red*

## 方法谱系与知识库定位

### 问题定义与基线谱系

CORE 面向大型视觉-语言模型（LVLM）中的**持续遗忘**（continual unlearning）任务：模型需序贯地遗忘多个任务中的特定视觉-指令对，同时保持对保留查询的正常响应能力。该问题处于持续学习与机器遗忘的交叉地带，现有基线可归为三条技术路线：

**正则化路线**通过约束参数更新来减轻灾难性遗忘，如 **EWC** 对重要参数施加二次惩罚，**LwF** 利用知识蒸馏保持旧任务输出分布。这两种方法在持续遗忘场景下表现有限，因为它们缺乏对遗忘目标的精确语义锚定——当遗忘任务在视觉或语义上重叠时，参数约束无法区分哪些表示应该被擦除、哪些应该保留，导致 AR 和 CRR 均显著低于 CORE（Table 1）。

**直接遗忘路线**将遗忘视为逆向优化问题，如 **GMM** 通过高斯混合建模遗忘数据分布以引导参数更新，**EProj** 将遗忘投影到参数空间的特定方向，**SCRUB** 则结合遗忘损失与保留损失进行对抗训练。这些方法在单任务遗忘中有效，但在序贯场景下，遗忘更新会逐渐扭曲共享的视觉-语言表示，产生虚假关联——新任务的遗忘模式覆盖旧任务的拒绝模式（不相关拒绝），或使模型对保留查询也变得过度谨慎（过度拒绝），这正是 Figure 1 揭示的核心瓶颈。

**模块化路线**通过为每个任务分配独立参数来隔离干扰，如 **MoEAdapter** 引入 Mixture of Experts 适配器，**O³** 则专门针对持续遗忘设计了正交投影机制。O³ 是现有最强基线，在 Vicuna-LVLM 上达到 Last AR 81.76% 和 CRR 73.03%（Table 1），但其参数隔离策略仍基于任务索引而非语义内容，当不同遗忘任务共享底层概念时（如“暴力”与“武器”），独立的参数模块无法复用已学到的拒绝模式，导致遗忘效率和保留率之间存在明显折衷。

### CORE 的方法论定位

CORE 的核心创新在于将遗忘目标从“任务-参数”映射转变为“概念-拒绝”映射，形成了一条不同于上述三条路线的**概念驱动路线**。其关键设计可分解为三个层次：

**概念分解与精炼**：CORE 将遗忘类别分解为细粒度视觉属性（如“红色液体”“金属管状物”）和文本意图（如“询问制作方法”“请求识别物品”）的概念集合，并通过概念模块产生激活。概念调制器进一步对这些激活进行重新加权，抑制与遗忘目标无关的语义（Equation 3），从而将粗粒度的类别标签精炼为可解释的概念组合。这一设计与现有工作形成鲜明对比——EWC、LwF 等方法直接操作参数空间，SCRUB 等方法直接操作输出空间，而 CORE 在中间的语义概念空间进行干预，使遗忘更新更加精准。

**概念感知的拒绝路由**：CORE 引入混合拒绝专家（Mixture of Refusers），每个 refuser 学习对视觉特征施加特定偏移以触发拒绝响应。Router 根据当前任务与历史任务的概念相关性（Equation 5）计算 refuser 的贡献权重，使得概念相似的任务可以复用已有的 refusers，而概念无关的任务则激活新的 refusers。这一机制直接回应了 Figure 1 中的不相关拒绝问题——传统方法中少数 refuser 被反复覆盖（Figure B），而 CORE 的概念路由使不同任务产生截然不同的 refuser 激活模式，避免了拒绝模式的相互干扰。

**推理时校准**：在推理阶段，CORE 根据查询与所有历史遗忘任务的最大概念相关性 $\beta$ 缩放 refuser 的贡献（Equation 7），相关性越低则抑制越强。这一设计直接针对过度拒绝问题——当查询与任何遗忘任务都不相关时，$\beta$ 趋近于 0，refuser 几乎不产生偏移，模型正常响应。

### 适用边界与局限

从实验设置反推，CORE 的适用边界可归纳为：

**适用条件**：CORE 假设遗忘类别可以被一组预定义的概念描述所覆盖。实验中使用 GPT/Gemini/Claude 生成概念描述，并在不同描述风格下验证了性能稳定性（Table C），表明该方法对概念描述的来源和风格具有一定鲁棒性。同时，CORE 冻结视觉编码器和语言模型，仅训练连接模块和新增参数，因此适用于黑盒或资源受限的 LVLM 部署场景。

**潜在局限**（需手动验证）：论文未报告概念描述的质量对极端长尾类别或高度抽象概念（如“讽刺”“隐喻”）的覆盖能力。当遗忘类别的视觉和文本概念难以用有限描述词捕捉时，概念模块的激活可能不够精确，进而影响调制器和路由的性能。此外，概念模块的数量随遗忘任务线性增长，在大量任务场景下的计算开销和概念冗余问题未在论文中深入讨论（Table B 仅验证了不同概念数量的影响，未给出扩展性分析）。

### 开放问题

1. **概念描述的自动化与质量保证**：CORE 依赖外部 LLM 生成概念描述，但论文未探讨描述质量的自动评估机制。当遗忘类别涉及主观或文化依赖的概念时（如“冒犯性内容”），概念描述的偏差可能引入新的公平性问题。

2. **跨模态概念冲突**：CORE 通过视觉和文本概念激活的联合相似度计算任务相关性（Equation 5），但当视觉概念与文本意图存在冲突时（如同一图像在不同文本上下文中应被遗忘或保留），当前的路由机制可能无法正确处理这种模态间的条件依赖。

3. **遗忘的不可逆性验证**：论文通过 AR 和 CRR 衡量遗忘效果，但未进行成员推理攻击等更严格的遗忘验证实验，无法确认模型是否真正“忘记”了遗忘数据，还是仅仅学会了拒绝特定的查询模式。

## 原文 PDF

![[paperPDFs/CVPR_2026/Which_Concepts_to_Forget_and_How_to_Refuse_Decomposing_Concepts_for_Continual_Unlearning_in_Large_Vision_Language_Models.pdf]]
