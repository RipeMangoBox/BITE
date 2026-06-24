---
title: "A Comprehensive Information-Decomposition Analysis of Large Vision-Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Comprehensive_Information_Decomposition_Analysis_of_Large_Vision_Language_Models.pdf
aliases:
- PL
- CIDALVLM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "通过部分信息分解（PID）将决策相关信息分解为冗余（R）、视觉唯一（U1）、语言唯一（U2）和协同（S）四个非负分量，从而定量刻画模型的信息处理策略。"
primary_logic: "LVLM存在两种任务模式（协同驱动 vs. 知识驱动）和两种稳定的家族级策略（融合中心 vs. 语言中心）。层间处理呈现一致的三阶段模式，视觉指令微调是解锁协同（S）的关键阶段。"
claims:
- "MMBench和POPE属于协同驱动任务，Reefknot和PMC-VQA属于知识驱动任务"
- "在协同驱动任务上，准确率与协同S的Spearman相关系数显著（MMBench: ρ=0.750, p<0.001; POPE: ρ=0.742, p<0.001）"
- "在知识驱动任务上，准确率与语言唯一U2的Spearman相关系数显著（PMC-VQA: ρ=0.406, p=0.040）"
- "图像移除干预的准确率下降D_vision与协同S在协同驱动基准上强相关（MMBench: ρ=0.809, p<0.001; POPE: ρ=0.744, p<0.001）"
---

# A Comprehensive Information-Decomposition Analysis of Large Vision-Language Models

> [!tip] 核心洞察
> LVLM存在两种任务模式（协同驱动 vs. 知识驱动）和两种稳定的家族级策略（融合中心 vs. 语言中心）。层间处理呈现一致的三阶段模式，视觉指令微调是解锁协同（S）的关键阶段。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大型视觉语言模型的信息分解综合分析 |
| 英文题名 | A Comprehensive Information-Decomposition Analysis of Large Vision-Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=6WsBGk4Iag); [GitHub](https://github.com/RiiShin/pid-lvlm-analysis) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | 基于部分信息分解（PID）的LVLM分析框架 |
| Dataset | MMBench, POPE, Reefknot, PMC-VQA |

> [!tip] 效果简介
> - MMBench 上，Spearman ρ (S vs. Acc) 为 0.750，对比 N/A，变化 p<0.001。
> - POPE 上，Spearman ρ (S vs. Acc) 为 0.742，对比 N/A，变化 p<0.001。
> - Reefknot 上，Spearman ρ (S vs. Acc) 为 0.357，对比 N/A，变化 p=0.073。

## 概述

大型视觉语言模型（LVLM）的内部决策过程不透明，现有可解释性方法难以定量区分模型预测的成功究竟源于真正的多模态融合，还是仅依赖单模态先验（如语言偏见）。本文提出一个基于**部分信息分解**（Partial Information Decomposition, PID）的分析框架，将模型决策相关的总互信息分解为四个非负原子：冗余（R）、视觉唯一（U₁）、语言唯一（U₂）和协同（S）。其中，协同S代表仅从视觉与语言组合中涌现的信息，是衡量多模态融合程度的核心指标。

研究在四个多项选择VQA基准（MMBench、POPE、Reefknot、PMC-VQA）上分析了26个开源LVLM，覆盖多个模型家族和规模。核心发现包括：（1）任务呈现两种模式：MMBench和POPE属于**协同驱动**任务（准确率与S的Spearman ρ分别为0.750和0.742，p<0.001），Reefknot和PMC-VQA属于**知识驱动**任务（PMC-VQA上准确率与U₂的ρ=0.406，p=0.040）；（2）模型家族呈现两种稳定策略：**融合中心型**（如Qwen2.5-VL、InternVL3）在协同驱动任务上S中位数高，**语言中心型**（如Gemma3）U₂占比大；（3）层间PID分析揭示一致的三阶段信息处理模式：信息涌现、表示构建、最终融合事件；（4）视觉指令微调（Stage 2）是解锁协同S的关键阶段。方法通过图像移除干预验证了PID结果的因果有效性：准确率下降D_vision与S在协同驱动基准上强相关（MMBench: ρ=0.809, p<0.001）。

## 背景与动机

大型视觉语言模型（LVLM）在多项视觉问答基准上取得了显著性能，但其内部决策过程仍是一个“黑箱”。一个根本性的开放问题是：模型给出的正确答案，究竟源自对视觉信号与文本指令的**真正多模态融合**，还是主要依赖从训练数据中学到的**单模态先验**（尤其是语言先验）？传统的可解释性方法（如注意力可视化、特征归因）缺乏理论支撑，无法在过程层面定量分离视觉、语言及两者交互对预测的各自贡献。

现有分析手段的瓶颈在于：它们通常仅使用准确率等聚合指标评估模型性能，无法刻画模型在“如何”利用信息上的差异。例如，两个模型在同一个任务上准确率相同，但一个可能通过真正的跨模态协同（synergy）作答，另一个则可能完全依赖语言先验（language prior）猜对答案。这种过程级的信息使用差异，对理解模型行为、指导模型改进至关重要，但现有方法无法揭示。

针对这一缺口，本文引入**部分信息分解（Partial Information Decomposition, PID）** 作为核心分析工具。PID将两个源（视觉 $X_1$、语言 $X_2$）到目标 $Y$ 的总互信息 $I(X_1, X_2; Y)$ 分解为四个非负分量：冗余 $R$（两源共享的信息）、视觉唯一 $U_1$、语言唯一 $U_2$，以及协同 $S$（仅从两源组合中涌现的信息）。这种分解为分析LVLM的信息处理策略提供了理论支撑：通过量化 $S$ 和 $U_2$ 的相对大小，可以直接判断模型是依赖真正的多模态融合（高 $S$）还是语言先验（高 $U_2$）。

本文的动机是：利用PID框架，系统性地分析26个主流LVLM家族在四个多样化的多项选择VQA基准（MMBench、POPE、Reefknot、PMC-VQA）上的信息处理模式。具体而言，本文旨在回答三个核心问题：(1) 不同模型家族和不同任务之间，信息使用策略存在怎样的差异？(2) LVLM内部的层间信息处理呈现何种动态模式？(3) 训练过程（特别是视觉指令微调）如何影响模型的信息处理策略？通过回答这些问题，本文期望为LVLM的可解释性提供一种新的、理论驱动的定量视角，并为模型设计（如架构选择、训练策略）提供可操作的诊断信号。

## 核心创新

本文的核心创新在于将**部分信息分解（Partial Information Decomposition, PID）**引入大型视觉语言模型（LVLM）的可解释性分析，从而将传统的聚合性能评估（如准确率）替换为对模型信息处理策略的**过程级定量描述**。与现有依赖辅助投影头或手动聚类的单模态探针不同，本文在嵌入层使用校准噪声掩码另一模态来估计单模态条件分布，避免了引入额外组件。此外，针对候选集过置信问题，引入了置信度阈值和软聚合边际分布估计，保证了PID原子计算的稳健性。

**关键创新点与changed slots：**

1.  **信息度量方式的根本转变**：从仅使用准确率等聚合指标（baseline）转向使用PID将决策相关信息分解为四个非负分量——冗余R（视觉和语言共享）、视觉唯一U1、语言唯一U2和协同S（仅从两者组合中涌现）。这一转变使得分析能够揭示模型成功是源于真正的多模态融合（高S）还是依赖单模态先验（高U2），如Figure 2所示。

2.  **单模态条件分布估计的工程创新**：传统方法需要训练辅助投影头或手动聚类开放答案，本文直接在嵌入层用校准噪声（从N(μ, diag(σ²))中i.i.d.采样）替换另一模态的完整嵌入序列，避免了训练额外组件带来的偏差。

3.  **输出分布正则化**：针对受限候选集导致的过置信问题，引入置信度阈值τ（公式5），当总得分低于阈值时使用均匀分布；同时采用软聚合（公式6）估计边际分布，避免argmax引入的伪影。消融实验（Table 4, Table 5）表明，τ∈{0.2, 0.3, 0.4}和不同特征汇总方法对主要结论的影响可忽略。

**核心发现与因果机制：**

- **任务模式二分**：MMBench和POPE属于**协同驱动任务**（高S），准确率与S的Spearman相关系数显著（MMBench: ρ=0.750, p<0.001; POPE: ρ=0.742, p<0.001）；Reefknot和PMC-VQA属于**知识驱动任务**（高U2），准确率与U2显著相关（PMC-VQA: ρ=0.406, p=0.040）。图像移除干预（D_vision）进一步验证了这一划分：在协同驱动基准上D_vision与S强相关（MMBench: ρ=0.809; POPE: ρ=0.744），而在知识驱动基准上相关性较弱。

- **家族级策略**：Figure 3揭示了两种稳定的家族级策略——**融合中心型**（如LLaVA-ov, Qwen2.5-VL, InternVL3）在两种任务模式下均保持较高S；**语言中心型**（如Gemma3, LLaVA-1.5, Instruct-BLIP）始终依赖语言唯一U2。

- **层间三阶段模式**：Figure 4展示了跨模型、跨数据集一致的层间PID动态——信息涌现、表示构建、最终融合事件（S尖峰伴随U2下降）。值得注意的是，InternVL3-2B缺乏最终融合事件，这是一个待解释的异常。

- **训练动态**：Figure 5表明视觉指令微调（Stage 2）是解锁协同S的关键阶段，而Stage 1（预训练对齐）主要影响U2。这一发现直接指导了训练策略的优化方向。

**证据强度评估**：上述核心发现均基于26个LVLM在四个基准上的系统实验，Spearman相关性检验和消融实验提供了强定量证据（置信度1.0）。唯一的弱点是PID本质上是相关性的，不能直接推断因果关系——这一点在论文局限性中已明确承认。

## 整体框架

![[assets/figures/papers/iclr26_0002_6WsBGk4Iag_A_Comprehensive_Information-Decomposition_Analys/figures/001_Figure_1.jpg]]
*Figure 1: (1). Proposed framework for PID estimation in LVLM scenario (2). 3-dimentional information-decomposition analysis*

该论文提出了一个基于部分信息分解（PID）的大型视觉语言模型（LVLM）分析框架，其整体pipeline由四个核心模块串联而成，旨在从信息论角度定量刻画模型的多模态决策过程。

**1. 输入表示提取模块**：给定图像-文本对，从LVLM内部提取视觉和文本token的嵌入表示，并分别通过均值池化得到两个源变量——视觉源 $X_1$ 和语言源 $X_2$。该步骤为后续所有分析提供统一的特征空间。

**2. 单模态条件估计模块**：为了获得视觉和语言各自的独立贡献，该模块通过嵌入层掩码来近似单模态条件分布。具体做法是将另一模态的整个嵌入序列替换为校准噪声（噪声从 $\mathcal{N}(\mu, \text{diag}(\sigma^2))$ 中独立同分布采样），从而得到 $P(Y|X_1)$ 和 $P(Y|X_2)$。这种方法避免了训练额外的投影头或手动聚类，但论文也承认这是一种近似，可能无法完全消除另一模态的影响。

**3. 置信度阈值与重归一化模块**：由于多项选择VQA任务的候选集有限，模型可能产生过置信的预测分布。该模块引入置信度阈值 $\tau$：当候选集总得分低于 $\tau$ 时，将预测分布替换为均匀分布 $\mathcal{U}(K)$（公式5）。消融实验显示，$\tau \in \{0.2, 0.3, 0.4\}$ 对主要PID分量（如MMBench上的协同S和PMC-VQA上的语言唯一U2）的影响可忽略，表明该设计对阈值选择稳健。

**4. 软聚合边际分布与BATCH估计器**：为避免argmax引入的伪影，该模块通过平均所有样本的正则化预测分布来估计边际输出分布 $P(Y)$（公式6）。随后，BATCH估计器使用神经网络参数化联合分布，并通过Sinkhorn算法施加边际匹配约束，最终计算出四个非负PID原子值：冗余R、视觉唯一U1、语言唯一U2和协同S。这四个分量满足一致性关系 $I(X_1, X_2; Y) = R + U_1 + U_2 + S$，共同构成对模型决策信息的完整分解。

**输入输出流**：整个pipeline的输入是图像-文本对和LVLM模型，输出是四个PID原子值。这些原子值随后被用于三个分析维度：（1）跨模型和跨任务比较，揭示任务模式（协同驱动 vs. 知识驱动）和家族级策略（融合中心 vs. 语言中心）；（2）层间信息动态，揭示一致的三阶段处理模式；（3）训练过程中的学习动态，揭示视觉指令微调是解锁协同S的关键阶段。

## 核心模块与公式推导

### 3.1 部分信息分解（PID）框架

本文的核心分析方法是将决策相关信息分解为四个非负原子，从而定量分离视觉和语言模态各自的贡献及其交互。对于两个源变量 $X_1$（视觉嵌入）和 $X_2$（语言嵌入）与目标变量 $Y$（预测答案），PID 通过优化一组保持源-目标边际分布的联合分布 $Q \in \Delta_P$ 来定义四个原子：

- **冗余原子** $R = \max_{Q \in \Delta_P} I_Q(X_1; X_2; Y)$：视觉和语言源共享的信息。
- **视觉唯一原子** $U_1 = \min_{Q \in \Delta_P} I_Q(X_1; Y \mid X_2)$：视觉源独有的信息。
- **语言唯一原子** $U_2 = \min_{Q \in \Delta_P} I_Q(X_2; Y \mid X_1)$：语言源独有的信息。
- **协同原子** $S = I(X_1, X_2; Y) - \min_{Q \in \Delta_P} I_Q(X_1, X_2; Y)$：仅从两者组合中涌现的信息。

这些原子满足一致性关系：总互信息 $I(X_1, X_2; Y) = R + U_1 + U_2 + S$，单源互信息 $I(X_1; Y) = R + U_1$，共信息 $I(X_1; X_2; Y) = R - S$。这些关系确保了分解的完备性和可解释性。

### 3.2 面向LVLM的PID估计框架

为将PID应用于大型视觉语言模型（LVLM），本文设计了专门针对多项选择视觉问答（MC-VQA）任务的估计流程，包含四个关键模块：

**输入表示提取**：从LVLM内部提取视觉和文本token嵌入，分别使用均值池化作为源变量 $X_1$ 和 $X_2$。消融实验（Table 4, Table 5）表明，均值池化、最后隐藏层、最大池化三种汇总方法对关键PID原子（协同S和语言唯一U2）的影响可忽略，验证了该选择的稳健性。

**单模态条件估计**：通过嵌入层掩码近似单模态条件分布。具体地，将另一模态的整个嵌入序列替换为从 $\mathcal{N}(\mu, \text{diag}(\sigma^2))$ 中独立同分布采样的校准噪声，从而获得 $P(Y|X_1)$ 和 $P(Y|X_2)$。这种方法避免了训练辅助投影头或手动聚类，减少了额外组件引入的偏差。

**置信度阈值与重归一化**：针对候选集受限导致的过置信问题，引入置信度阈值 $\tau$。正则化预测分布定义为：

$$
\hat{P}(Y|\cdot) = \left\{ \begin{array}{ll} P(Y|\cdot) & \mathrm{if~} \sum_{y \in \mathcal{Y}} S_{\mathrm{orig}}(Y=y|\cdot) \geq \tau \\ \mathcal{U}(K) & \mathrm{otherwise} \end{array} \right.
$$

当候选集总得分低于阈值时，使用均匀分布 $\mathcal{U}(K)$ 替代。消融实验（Table 4, Table 5）显示 $\tau \in \{0.2, 0.3, 0.4\}$ 对主要结论无显著影响。

**软聚合边际分布**：为避免argmax引入的伪影，通过平均所有 $N$ 个样本的正则化预测分布估计边际输出分布：

$$
P(Y) = \frac{1}{N} \sum_{i=1}^N \hat{P}_i(Y)
$$

**BATCH估计器**：最终使用神经网络参数化联合分布，通过Sinkhorn算法施加边际匹配约束，从连续嵌入中计算PID原子值。该估计器适用于高维连续表示和大规模数据集，是框架的计算核心。

### 3.3 干预验证：图像移除

为验证PID分解的行为有效性，设计了图像移除干预实验。通过移除图像获得纯文本基线，测量准确率下降 $D_{\text{vision}}$。该指标与协同S在协同驱动基准上强相关（MMBench: $\rho=0.809, p<0.001$; POPE: $\rho=0.744, p<0.001$），而在知识驱动基准上相关性较弱（Reefknot: $\rho=0.459, p=0.018$; PMC-VQA: $\rho=0.400, p=0.043$）。这一模式验证了协同S确实捕获了视觉信息对决策的关键贡献，而非仅反映模型架构的统计特性。

## 实验与分析

**任务模式与信息分解**。对26个大型视觉语言模型（LVLM）在四个基准上的分析揭示了两种截然不同的信息处理模式。如Figure 2所示，MMBench和POPE构成一个簇，其显著特征是协同S的份额高；而Reefknot和PMC-VQA构成另一个簇，其协同S明显更低、语言唯一U2更高。这一定性划分得到了定量相关性的支持：在MMBench和POPE上，准确率与协同S的Spearman相关系数分别为ρ=0.750 (p<0.001)和ρ=0.742 (p<0.001)；而在PMC-VQA上，准确率与语言唯一U2的相关系数为ρ=0.406 (p=0.040)，与协同S的相关系数仅为ρ=0.432 (p=0.027)。这表明MMBench和POPE属于协同驱动任务，模型需要真正融合视觉和语言信息；Reefknot和PMC-VQA属于知识驱动任务，性能主要受限于语言先验知识。

**行为验证：图像移除干预**。为验证PID分解的行为意义，作者设计了图像移除干预实验：移除图像后测量准确率下降D_vision。在协同驱动基准上，D_vision与协同S强相关（MMBench: ρ=0.809, p<0.001; POPE: ρ=0.744, p<0.001），说明高协同的模型确实更依赖视觉信息。在知识驱动基准上，相关较弱但仍显著（Reefknot: ρ=0.459, p=0.018; PMC-VQA: ρ=0.400, p=0.043），符合预期——这些任务中语言先验主导，移除图像的影响较小。

**家族级策略**。Figure 3按模型家族聚合展示了每个家族在两种任务模式下的中位数S与中位数U2。两个任务模式内均存在两种稳定的家族级策略：融合中心策略（如Llama-3.2-vision、Qwen2.5-VL）在协同驱动任务上产生更高的协同S，同时在知识驱动任务上也产生非平凡协同；语言中心策略（如Gemma3）则在两种任务上都高度依赖语言唯一U2，协同S接近零。这一区分在模型家族层面稳定存在，与模型规模无关。

**缩放效应**。Table 3展示了在协同驱动任务上缩放模型的效果。对于融合中心家族（Llama-3.2-vision、Qwen2.5-VL），从S→M和M→VL的缩放均带来协同S份额增加和语言唯一U2份额下降，同时准确率提升。例如Qwen2.5-VL从7B到72B，协同S增加0.045，语言唯一U2下降0.052，准确率提升0.077。而对于语言中心模型Gemma3，缩放仅带来微小的协同增加（0.006）和语言唯一下降（0.009），准确率提升有限（0.006）。这揭示了一个关键瓶颈：融合中心模型通过缩放更有效地解锁协同能力，而语言中心模型的缩放收益受限于其固有的语言先验依赖。

![[assets/figures/papers/iclr26_0002_6WsBGk4Iag_A_Comprehensive_Information-Decomposition_Analys/figures/008_Table_3.jpg]]
*Table 3: Scaling on synergy-driven tasks: changes in accuracy (∆Acc) and PID shares (∆S, ∆U2) for S→M and M→VL within representative families*

**层间信息动态**。Figure 4展示了代表性模型在协同驱动任务（MMBench）和知识驱动任务（PMC-VQA）上的层间PID动态。所有模型和数据集上一致呈现三阶段模式：
- **阶段1（早期层，约前1/3层）**：信息涌现阶段。协同S和语言唯一U2从零开始快速上升，视觉唯一U1和冗余R也出现，但各分量尚未稳定。
- **阶段2（中间层）**：表示构建阶段。各PID分量趋于稳定，语言唯一U2逐渐成为主导（知识驱动任务）或与协同S共存（协同驱动任务）。
- **阶段3（后期层，约后1/3层）**：最终融合事件。在协同驱动任务上，所有模型均出现一个显著的协同S尖峰和对应的语言唯一U2下降，表明模型在最后层完成视觉-语言的深度融合。在知识驱动任务上，这一融合事件较弱或不存在。

一个值得注意的异常是InternVL3-2B（Figure 12）：该模型缺乏阶段3的最终融合事件，其协同S在后期层持续下降而非上升。这一发现需要手动验证，但暗示了该模型架构或训练策略可能限制了其多模态融合能力。

**训练动态**。Figure 5展示了LLaVA-1.5两阶段训练过程中协同S和语言唯一U2的演化。关键发现是：视觉指令微调（Stage 2）是协同S显著增加的关键阶段。在Stage 1（视觉-语言对齐预训练）中，协同S保持低水平且变化不大；进入Stage 2后，协同S迅速上升并达到峰值，随后略有下降但保持在高位。同时，语言唯一U2在Stage 2中先下降后回升。这表明视觉指令微调不仅教会模型遵循指令，更重要的是解锁了视觉与语言的协同融合能力。这一模式在7B和13B模型上一致，说明其具有可扩展性。

**消融实验**。Table 4和Table 5分别展示了在MMBench上对协同S、在PMC-VQA上对语言唯一U2的消融结果。两种消融均表明主要结论稳健：
- **特征汇总方法**：均值池化、最后隐藏层、最大池化三种方法对S和U2的影响可忽略。例如Qwen2.5-VL-7B的S在所有方法上均为1.112，Qwen2.5-VL-72B均为1.088。
- **置信度阈值τ**：τ∈{0.2, 0.3, 0.4}对S和U2的影响可忽略。例如Gemma3-4B的S在所有τ值上均为0.167。

![[assets/figures/papers/iclr26_0002_6WsBGk4Iag_A_Comprehensive_Information-Decomposition_Analys/figures/011_Table_4.jpg]]
*Table 4: S on MMBench for four chosen models under two ablations (feature summarization and confidence threshold)*

![[assets/figures/papers/iclr26_0002_6WsBGk4Iag_A_Comprehensive_Information-Decomposition_Analys/figures/012_Table_5.jpg]]
*Table 5: U2 on PMC-VQA for four chosen models under two ablations (feature summarization and confidence threshold)*

**案例研究**。Figure 6和Figure 7分别展示了协同驱动任务和知识驱动任务的PID案例分析。在协同驱动任务上（Figure 6），所有模型均回答正确，但PID分解揭示了两种截然不同的解决方案：Llama-3.2-vision和Qwen2.5-VL通过高协同S（1.47和1.48）实现正确回答，而Gemma3-4B的协同S为零，其正确回答是通过视觉证据纠正一个强且错误的语言先验（U2=1.73）实现的。在知识驱动任务上（Figure 7），所有模型均高度依赖语言唯一U2，但融合中心模型（Llama-3.2-vision、Qwen2.5-VL）同时产生非平凡协同（0.33和0.95），而语言中心模型Gemma3的协同S为零。这印证了家族级策略在个体样本层面的体现。

**失败模式**。分析揭示了两种主要失败模式：
1. **语言中心模型的过置信失败**：在协同驱动任务上，语言中心模型（如Gemma3）依赖强语言先验（高U2），当视觉证据与语言先验冲突时，如果视觉证据不足以纠正（低S），模型会错误地坚持语言先验。
2. **融合不足的缩放瓶颈**：语言中心模型在缩放时协同S增长有限，其性能提升主要来自语言先验的改善而非多模态融合能力的增强，这限制了其在需要真正融合的任务上的上限。

**开放问题**。分析还识别出几个需要进一步研究的问题：InternVL3-2B为何缺乏最终融合事件？LLaVA-1.5后期层中非零的冗余R和视觉唯一U1的成因是什么？视觉证据覆盖语言偏见的“纠正”机制如何随模型规模扩展？这些问题超出了当前分析范围，需要手动验证或后续研究。

### 补充图表

![[assets/figures/papers/iclr26_0002_6WsBGk4Iag_A_Comprehensive_Information-Decomposition_Analys/figures/003_Table_1.jpg]]
*Table 1: Details of the datasets used for evaluation. The listed training and test splits are not for LVLM fine-tuning; they are created by randomly partitioning each dataset (3:1 ratio) for the PID estimation, as the BATCH estimator requires separate sets to train networks and estimate PID values*

![[assets/figures/papers/iclr26_0002_6WsBGk4Iag_A_Comprehensive_Information-Decomposition_Analys/figures/005_Table_2.jpg]]
*Table 2: Spearman correlations ( $\rho$ ) and p-values across datasets*

## 方法谱系与知识库定位

### 与基线方法的关系

该工作提出的基于部分信息分解（PID）的LVLM分析框架，在方法论上并非替代现有评估指标，而是提供了**过程级描述**，弥补了仅使用准确率等聚合指标无法揭示模型内部信息处理策略的不足。其核心创新在于将决策相关信息分解为冗余（R）、视觉唯一（U1）、语言唯一（U2）和协同（S）四个非负分量，从而定量刻画模型是依赖单模态先验还是真正的多模态融合。

与行为验证基线（图像移除干预）的关系是互补验证：图像移除干预测量准确率下降D_vision，而PID框架将其分解为可解释的因果机制。实验证据显示，在协同驱动基准（MMBench、POPE）上，D_vision与协同S的Spearman相关系数分别为0.809和0.744（均p<0.001），说明PID的S分量能够解释模型对视觉输入的依赖程度；而在知识驱动基准（Reefknot、PMC-VQA）上，相关系数降至0.459和0.400，表明此时模型的视觉依赖较弱且与协同的关联性降低。

### 适用边界

该框架的适用边界由三个关键假设定义：

1. **离散目标空间假设**：PID估计要求目标变量Y为离散值，因此当前框架仅适用于多项选择视觉问答（MC-VQA）任务，无法直接处理开放生成任务。这是该框架最根本的局限性，也直接决定了其不能泛化到图像描述、对话生成等场景。

2. **双源变量假设**：分析仅限于视觉和语言两个源变量（X1和X2），未考虑其他模态（如音频、视频）或更复杂的多源交互。对于多模态大模型来说，这一简化可能忽略了跨更多模态的协同效应。

3. **单模态条件近似**：通过嵌入层掩码模拟单模态条件（将另一模态的嵌入序列替换为校准噪声），可能无法完全消除另一模态的影响。尽管消融实验表明特征汇总方法（均值池化、最后隐藏层、最大池化）和置信度阈值（τ∈{0.2, 0.3, 0.4}）对主要PID分量（S和U2）影响可忽略，但这一近似的偏差在理论上未被严格量化。

### 局限

1. **相关性而非因果性**：PID本质上是相关性的，不能直接推断因果关系。虽然图像移除干预提供了行为层面的因果验证，但PID分量本身描述的是信息结构而非因果机制。

2. **BATCH估计器的超参数敏感性**：BATCH估计器使用神经网络参数化联合分布并通过Sinkhorn算法施加边际匹配约束，其性能可能受学习率、网络架构等超参数影响。尽管消融实验表明对主要结论稳健，但不同模型家族的最优超参数可能不同，这一风险未被系统评估。

3. **输出分布正则化的潜在偏差**：引入置信度阈值τ和软聚合边际分布是为了避免过置信问题，但均匀分布替代低置信度预测的做法可能引入新的偏差，特别是在模型对候选集外答案有合理置信度时。

### 开放问题

1. **开放生成场景的扩展**：如何开发适用于开放生成场景和更多模态的PID估计器和输出编码？这是将该框架从分析工具升级为通用诊断工具的关键。

2. **PID分量的工程应用**：如何将（U1, U2, S）作为诊断信号用于模型缩放和指令微调，并可能作为辅助目标来平衡融合和语言先验？例如，是否可以通过优化S来强制模型进行真正的多模态融合？

3. **基准设计指导**：如何利用基于PID的分析来指导构建明确需要高协同S或隔离语言先验U2的基准？当前基准（如MMBench）的协同驱动特性可能是偶然的，而非有意设计的。

4. **未解释的层间现象**：InternVL3-2B为何缺乏最终融合事件（S尖峰和U2下降）？LLaVA-1.5后期层中非零的冗余R和视觉唯一U1的成因是什么？这些现象暗示了模型架构和训练策略对信息处理模式的深层影响。

5. **纠正机制的扩展规律**：视觉证据覆盖语言偏见的“纠正”机制（如Gemma3在协同驱动任务中的表现）如何随模型规模扩展？当前数据仅覆盖有限规模范围，缺乏系统性缩放分析。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Comprehensive_Information_Decomposition_Analysis_of_Large_Vision_Language_Models.pdf

![[paperPDFs/ICLR_2026/A_Comprehensive_Information_Decomposition_Analysis_of_Large_Vision_Language_Models.pdf]]
