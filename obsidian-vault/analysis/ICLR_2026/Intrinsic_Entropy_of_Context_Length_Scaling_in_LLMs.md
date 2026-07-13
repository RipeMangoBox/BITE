---
title: "Intrinsic Entropy of Context Length Scaling in LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Intrinsic_Entropy_of_Context_Length_Scaling_in_LLMs.pdf
project_link: null
code_link: https://github.com/JingzheShi/NLPCtlScalingAndBounds
openreview_forum_id: vnipyA8c9V
aliases:
- IEF
- IECLSL
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "内在熵（Intrinsic Entropy）作为关键变量，其随上下文长度增加而增加，与交叉熵损失呈线性关系，并能解释贝叶斯风险的下降。"
primary_logic: "总损失分解为随上下文长度递减的贝叶斯风险和递增的近似损失；内在熵与贝叶斯风险线性相关，内在维度与近似损失相关；平衡点决定最优上下文长度，该最优长度随训练数据量或模型能力的增强而右移。"
claims:
- "总损失可分解为贝叶斯风险和近似损失，二者对上下文长度的导数符号相反。"
- "交叉熵损失与高斯KDE测量的内在熵之间存在线性关系，跨 Llama-3.1-8B、Qwen3-8B-Base、RecurrentGemma-9B 三种模型均成立。"
- "在合成数据上，交叉熵损失与特征值对数求和测得的内在熵呈良好线性关系（R^2 接近 1）。"
- "对于每个训练语料大小，存在一个最小化预训练验证损失的最优上下文长度，且该最优长度随训练语料增加而增加。"
---

# Intrinsic Entropy of Context Length Scaling in LLMs

> [!tip] 核心洞察
> 总损失分解为随上下文长度递减的贝叶斯风险和递增的近似损失；内在熵与贝叶斯风险线性相关，内在维度与近似损失相关；平衡点决定最优上下文长度，该最优长度随训练数据量或模型能力的增强而右移。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大语言模型上下文长度缩放中的内在熵 |
| 英文题名 | Intrinsic Entropy of Context Length Scaling in LLMs |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=vnipyA8c9V) · [GitHub](https://github.com/JingzheShi/NLPCtlScalingAndBounds) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 内在熵分析框架（Intrinsic Entropy Framework） |
| Dataset | Position-Weighted Multitask Sparse Parity (synthetic) |

> [!tip] 效果简介
> - Position-Weighted Multitask Sparse Parity (synthetic) 上，Cross-Entropy Loss (context length 17) 为 0.4648，对比 0.4643 (theoretical minimum)，变化 -0.0005。
> - Position-Weighted Multitask Sparse Parity (synthetic) 上，Cross-Entropy Loss (context length 50) 为 0.0613，对比 0.0612 (theoretical minimum)，变化 -0.0001。

## 概要

大语言模型（LLM）的上下文长度是决定其性能的关键因素，但上下文长度缩放对模型损失的影响机制长期缺乏统一的理论解释。该论文针对这一瓶颈，提出**内在熵分析框架（Intrinsic Entropy Framework）**，将总交叉熵损失分解为两个随上下文长度变化方向相反的组件：**贝叶斯风险（Bayes Risk）** 和**近似损失（Approximation Loss）**。贝叶斯风险代表给定上下文下最优语言模型所能达到的理论下限，随上下文长度增加而递减；近似损失衡量实际训练模型与贝叶斯最优模型之间的 KL 散度，随上下文长度增加而递增。二者导数符号相反，在特定条件下产生一个使总损失最小的**最优上下文长度**。

框架的核心因果变量是**内在熵（Intrinsic Entropy）**——一种在预训练语言模型隐藏层空间测量的、反映给定上下文长度下可用信息量的度量。论文通过理论推导与实验验证建立了内在熵与交叉熵损失之间的线性关系：贝叶斯风险负线性依赖于内在熵，即 $R_{Bayes} = -k \cdot S(P_l) + Const$。这一线性关系在 Llama-3.1-8B、Qwen3-8B-Base、RecurrentGemma-9B 三种不同架构模型上均得到验证（Figure 2），并在合成数据上通过 PCA 特征值对数求和测得的熵进一步确认（Figure 7）。

实验揭示了最优上下文长度的存在性与变化规律：在预训练场景下，对于每个训练数据量，存在一个最小化验证损失的最优上下文长度，且该最优长度随训练数据量增加而右移（Figure 1、Figure 15）；在下游任务（如 Position-Weighted Ruler-QA1）上，QA 准确率随上下文长度先升后降，最优长度取决于任务对长上下文的依赖程度（Figure 4）。在 RULER 基准的多个子任务上，多数 Qwen-3 模型也表现出类似的最优可见上下文长度现象（Figure 8）。

论文的主要局限在于理论框架依赖若干关于内在空间的假设（如预测一致性、线性熵关系、均匀信息增益等），其普适性有待进一步验证；内在熵的测量方法（Gaussian-KDE 或 PCA）是对真实信息熵的近似，可能引入测量误差。开放问题包括如何从更基本的原则推导线性熵关系、内在熵与内在维度之间的确切数学关联，以及该框架在更大规模模型和更复杂推理任务上的推广等。

大语言模型（LLMs）的上下文窗口正以指数级速度扩展——从初代 GPT 的 512 个 token 到如今动辄百万 token 的超长上下文模型，这一趋势已成为模型竞争的核心维度之一。然而，一个根本性的理论问题始终悬而未决：**更长的上下文是否总是更好？** 实践中，人们观察到模型在极长上下文下的性能并非单调提升，有时甚至出现退化，但缺乏统一的理论框架来解释这一现象的内在机制。

### 现有认知的缺口

当前对上下文长度缩放行为的理解存在三个关键盲区：

1. **缺乏统一的损失分解视角**。总交叉熵损失随上下文长度的变化并非简单的单调递减。直觉上，更长的上下文提供了更多信息，应降低预测不确定性；但与此同时，模型在更长序列上的学习难度也在增加。这两种力量的对抗关系尚未被形式化地刻画。

2. **缺少可测量的内在信息度量**。尽管“上下文包含更多信息”这一直觉广泛存在，但如何在模型表示空间中量化这种“可用信息”一直缺乏有效工具。现有的信息论度量往往停留在理论层面，难以在真实大规模语言模型上直接计算。

3. **最优上下文长度的存在性缺乏理论解释**。实验观察表明，对于给定的训练数据量和模型容量，可能存在一个使验证损失最小化的“最优上下文长度”，且该最优值随训练数据的增加而右移。但这一现象的数学根源尚不明确。

### 本文的核心动机

本文旨在填补上述理论空白，提出一个以**内在熵（Intrinsic Entropy）**为核心变量的分析框架。核心动机可概括为三个递进层次：

- **分解总损失的对抗结构**：将总交叉熵损失 $H(P, Q_l)$ 分解为贝叶斯风险 $R_{Bayes}$ 和近似损失 $L_{Approx}$ 两项（详见 Equation 1）。贝叶斯风险随上下文长度递减，代表“最优可能模型”的损失下限；近似损失随上下文长度递增，反映实际训练模型与最优模型之间的 KL 散度差距。二者的导数符号相反，为最优上下文长度的存在提供了数学基础。

- **引入内在熵作为桥梁变量**：内在熵衡量给定上下文长度下模型表示空间中可用的信息量。本文通过高斯核密度估计（Gaussian-KDE）和 PCA 特征值对数求和两种方法，在预训练语言模型的隐藏层空间测量内在熵，并发现其与交叉熵损失之间存在稳健的线性关系——这一关系在 Llama-3.1-8B、Qwen3-8B-Base 和 RecurrentGemma-9B 三种不同架构的模型上均成立（Figure 2）。

- **推导最优上下文长度的存在条件**：联立贝叶斯风险和近似损失对上下文长度的导数，推导总损失关于上下文长度的导数为零的条件，从而解释最优上下文长度的存在性及其随训练数据量、任务特性变化的规律。这一理论预测在预训练验证损失（Figure 1 Middle）和下游任务准确率（Figure 4 Left）两个层面均得到了实验验证。

### 关键实验现象驱动

本文的理论构建直接受以下实验观察的驱动：

- 在 OpenWebText 子集上，对于每个固定的训练数据量，验证损失随上下文长度先降后升，存在明确的最优上下文长度；且该最优值随训练数据量的增加而增大（Figure 1 Middle, Figure 15）。
- 在 RULER 基准测试中，Qwen-3 系列模型在 qa1、fwe、cwe 等子任务上同样出现最优可见上下文长度，而 vt（变量追踪）子任务则表现为性能持续提升（Figure 8），表明任务对长上下文的依赖程度（以参数 $\gamma$ 刻画）影响最优上下文长度的位置。
- 在 Position-Weighted Ruler-QA1 数据集上，QA 准确率随上下文长度先升后降，且 $\gamma$ 越大（即任务更依赖近距离上下文），最优上下文长度越小（Figure 4 Left）。

这些现象共同指向一个核心假设：**上下文长度对模型性能的影响由贝叶斯风险与近似损失的权衡决定，而内在熵是连接这一权衡与可观测损失的关键变量。**

## 核心方法与创新机理

本文的核心创新在于提出了一套**以“内在熵”（Intrinsic Entropy）为枢轴的统一理论框架**，用以解释大语言模型性能随上下文长度变化的非单调行为。该框架并非提出新的模型架构或训练算法，而是从信息论角度重新理解上下文长度缩放的底层机制，其关键突破可归纳为三个层次。

### 1. 损失分解与内在熵的引入

传统上，上下文长度对模型性能的影响缺乏统一的理论解释。本文通过将总交叉熵损失分解为两项，建立了分析的基础：

$$H(P, Q_l) = R_{\mathrm{Bayes}} + L_{\mathrm{Approx}} = H(P, P_l) + D_{\mathrm{KL}}(P_l, Q_l)$$

其中，**贝叶斯风险** $R_{\mathrm{Bayes}}$ 代表给定上下文长度 $l$ 下最优模型所能达到的理论下限，随 $l$ 增加而递减；**近似损失** $L_{\mathrm{Approx}}$ 衡量实际训练模型与贝叶斯最优模型之间的 KL 散度，随 $l$ 增加而递增。这一分解揭示了上下文长度对性能的双刃剑效应：更长的上下文提供更多信息（降低贝叶斯风险），但也增加了模型拟合的难度（推高近似损失）。

框架的核心变量是**内在熵** $S(P_l)$，它度量了在给定上下文长度下、数据在模型隐藏层所张成的“内在空间”中所蕴含的信息量。论文提出并验证了一个关键假设：贝叶斯风险与内在熵之间存在线性关系 $R_{\mathrm{Bayes}} = -k \cdot S(P_l) + \mathrm{Const}$。这意味着，上下文长度对贝叶斯风险的降低作用，本质上是通过增加内在空间中的信息量来实现的。

### 2. 最优上下文长度的存在性解释

基于上述分解，总损失可表达为：

$$\mathrm{Loss}(l, \theta_t, \theta_m) = R_{\mathrm{Bayes}}(l, \theta_t) + L_{\mathrm{Approx}}(l, \theta_m)$$

由于两项对 $l$ 的导数符号相反（$\partial R_{\mathrm{Bayes}}/\partial l < 0$，$\partial L_{\mathrm{Approx}}/\partial l > 0$），总损失曲线必然存在一个临界点 $l^*$，即**最优上下文长度**。这一推导首次从理论上解释了为何更长的上下文并不总是更好——当近似损失的增长超过贝叶斯风险的下降时，模型性能反而恶化。

论文进一步揭示了最优上下文长度的**动态可移动性**：近似损失对上下文长度的依赖受训练数据量 $D$ 和模型容量 $\theta_m$ 的调控，具体形式为 $L_{\mathrm{Approx}} = C_0 + A(l) / D^{\alpha(l)}$，其中指数 $\alpha(l)$ 随 $l$ 增加而减小。这意味着，增大训练数据量或增强模型能力会降低近似损失对上下文长度的敏感性，从而使最优上下文长度向右移动——这一推论在合成数据实验和 OpenWebText 验证集上均得到实证支持。

### 3. 内在熵与内在维度的双重测量路径

区别于依赖特定模型输出的启发式指标，本文提出了两种模型无关的内在熵估计方法：

- **高斯核密度估计（Gaussian-KDE）**：直接在隐藏层表示空间中对样本分布进行非参数密度估计，计算连续熵。
- **PCA 特征值对数求和**：对隐藏层表示进行主成分分析，以 $\sum_i \log(\lambda_i)$ 作为内在熵的代理量。

在 Llama-3.1-8B、Qwen3-8B-Base、RecurrentGemma-9B 三种架构迥异的模型上，交叉熵损失与 Gaussian-KDE 测量的内在熵均呈现高线性相关性（$|R| > 0.98$）；在合成数据上，PCA 特征值对数求和与交叉熵损失的 $R^2$ 接近 1。两种测量方法之间本身也高度相关（$r = 0.9978$），表明内在熵是模型表示空间中一个稳健且可复现的信息量指标。

此外，论文将**内在维度**（Intrinsic Dimension）作为辅助变量引入，通过 PCA 相对特征值取阈值法测量数据流形的本征维度，发现其与交叉熵损失同样呈线性关系，且对阈值选择不敏感。内在维度为解释近似损失随上下文长度的增长提供了几何直觉：更长的上下文意味着内在空间的维度膨胀，模型需要拟合更复杂的数据流形，从而推高近似损失。

### 与现有工作的本质区别

现有关于上下文长度缩放的研究多从经验拟合（如幂律外推）或特定任务机制（如注意力分布）出发，缺乏对“信息增益-拟合难度”权衡的统一建模。本文的核心差异在于：**将上下文长度的影响归结为内在空间中信息量（熵）和复杂度（维度）的变化，并通过损失分解将预训练验证损失与下游任务准确率的非单调行为纳入同一理论框架**。这使得框架不仅能解释观测现象，还能对最优上下文长度随数据量、模型容量和任务特性的迁移做出可检验的预测。

本文提出**内在熵分析框架（Intrinsic Entropy Framework）**，旨在从信息论角度统一解释上下文长度对大语言模型性能的影响。框架的核心洞察是：总损失可分解为两个随上下文长度变化方向相反的组件——贝叶斯风险与近似损失，二者的平衡点决定了最优上下文长度。

### 框架总览

整个分析框架由四个递进的模块构成，形成从理论分解到实验验证的闭环：

1. **损失分解 (Loss Decomposition)**：将总交叉熵损失拆解为贝叶斯风险与近似损失。
2. **内在熵估计 (Intrinsic Entropy Estimation)**：在隐藏层空间测量数据的内在信息量。
3. **内在维度估计 (Intrinsic Dimension Estimation)**：测量数据流形的内在维度，解释近似损失的行为。
4. **最优上下文长度推导 (Optimal Context Length Deduction)**：联立两项损失的导数关系，推导最优上下文长度的存在条件及其变化规律。

### 模块关系与数据流

框架的输入是经过预训练语言模型处理后的隐藏层表示，输出是对上下文长度缩放行为的理论解释与预测。

**第一步：损失分解。** 给定真实数据分布 $P$、给定上下文长度 $l$ 下的贝叶斯最优模型分布 $P_l$、以及实际训练模型的分布 $Q_l$，总交叉熵损失被分解为（Section 2.1.1, Equation 1）：

$$H(P, Q_l) = R_{\mathrm{Bayes}} + L_{\mathrm{Approx}} = H(P, P_l) + D_{\mathrm{KL}}(P_l, Q_l)$$

其中 $R_{\mathrm{Bayes}} = H(P, P_l)$ 为贝叶斯风险，代表仅依赖上下文长度的最优模型所能达到的损失下界，随 $l$ 增加而递减；$L_{\mathrm{Approx}} = D_{\mathrm{KL}}(P_l, Q_l)$ 为近似损失，衡量实际模型与贝叶斯最优模型之间的 KL 散度，随 $l$ 增加而递增。

**第二步：内在熵估计。** 为解释贝叶斯风险的下降，框架引入内在熵 $S(P_l)$，在模型的隐藏层空间通过高斯核密度估计（Gaussian-KDE）或 PCA 特征值对数求和进行测量（Section 2.2.2, Section 4.3）。理论假设贝叶斯风险与内在熵之间存在负线性关系（Section 2.2.1, Equation 2）：

$$R_{\mathrm{Bayes}} = -k \cdot S(P_l) + \mathrm{Const}$$

内在熵随上下文长度增加而增加，反映了更多上下文为模型提供了更丰富的信息。在 OpenWebText 子集上，Llama-3.1-8B（$k=-0.0038$, $R=-0.9888$）、Qwen3-8B-Base（$k=-0.0026$, $R=-0.9960$）和 RecurrentGemma-9B（$k=-0.0174$, $R=-0.9967$）均验证了这一线性关系（Figure 2）。

**第三步：内在维度估计。** 为解释近似损失的行为，框架通过 PCA 相对特征值取阈值法测量数据流形的内在维度（Appendix K）。近似损失在训练场景下依赖于数据集大小 $D$ 和上下文长度 $l$（Section 2.3, Equation 4）：

$$\mathcal{L}_{\mathrm{Approx}} = C_0 + A(l) / D^{\alpha(l)}, \quad \frac{\partial \alpha}{\partial l} < 0$$

内在维度随 $l$ 增加而增加，导致模型需要更多数据来拟合更复杂的数据分布，从而推高近似损失。

**第四步：最优上下文长度推导。** 将贝叶斯风险和近似损失联立，总损失为（Section 3, Equation 5）：

$$\mathrm{Loss}(l, \theta_t, \theta_m) = R_{\mathrm{Bayes}}(l, \theta_t) + L_{\mathrm{Approx}}(l, \theta_m)$$

由于 $\partial R_{\mathrm{Bayes}} / \partial l < 0$ 且 $\partial L_{\mathrm{Approx}} / \partial l > 0$，总损失存在极小值点 $l^*$，即最优上下文长度。该最优值随训练数据量增大或模型能力增强而右移（Figure 1 Middle, Figure 15），并在下游任务（如 Position-Weighted Ruler-QA1）上表现为准确率先升后降的趋势（Figure 4）。

### 关键假设与适用范围

框架的有效性依赖于三个核心假设（Section 2.2.1）：（1）**预测一致性**：内在空间中的状态足以确定下一个 token 的预测分布；（2）**线性熵关系**：下一 token 预测熵与内在空间熵呈线性关系；（3）**均匀信息增益**：上下文长度增加时，内在熵单调递增。这些假设在合成数据和真实语料上均得到了实验支持，但其在更广泛场景下的普适性仍需进一步验证。

### 损失分解模块

本文的核心起点是将语言模型的交叉熵损失分解为两个性质相反的组成部分。对于上下文长度为 $l$ 的序列，给定真实分布 $P$、贝叶斯最优模型分布 $P_l$ 和训练模型分布 $Q_l$，总损失可写为：

$$H(P, Q_l) = R_{Bayes} + L_{Approx} = H(P, P_l) + D_{KL}(P_l, Q_l)$$

其中 $H(P, P_l)$ 为**贝叶斯风险**（Bayes Risk），代表仅受上下文长度限制的最优模型所能达到的最低损失；$D_{KL}(P_l, Q_l)$ 为**近似损失**（Approximation Loss），衡量训练模型与贝叶斯模型之间的 KL 散度。这两个分量对上下文长度 $l$ 的导数符号相反：贝叶斯风险随 $l$ 增加而递减并趋于常数，近似损失随 $l$ 增加而递增。这一对立关系是后续推导最优上下文长度的理论基石。

### 内在熵估计模块

为解释贝叶斯风险随上下文长度的变化规律，论文引入**内在熵**（Intrinsic Entropy）概念。内在熵 $S(P_l)$ 衡量在给定上下文长度下，数据在语言模型隐藏层所张成的内在空间中可供利用的信息量。其核心假设是贝叶斯风险与内在熵之间存在线性关系：

$$R_{Bayes} = -k \cdot S(P_l) + Const$$

其中 $k > 0$ 为比例系数。该关系的成立依赖于三个关键假设：(1) 内在空间中的预测一致性；(2) 下一 token 预测熵与内在空间熵之间的线性熵关系 $S_{ntp}(P_l) = k \cdot S(P_l) + b$，且 $0 < k < 1$；(3) 内在熵随上下文长度单调递增，即 $l_1 < l_2$ 时 $S(P_{l_1}) < S(P_{l_2})$。

内在熵的测量采用两种互补方法。其一为**高斯核密度估计**（Gaussian-KDE），在预训练语言模型的隐藏层表示上直接估计连续熵；其二为**PCA 特征值对数求和**，即对表示空间协方差矩阵的相对特征值取对数后求和。实验表明，两种测量方式高度相关（Pearson $r = 0.9978$），且均与交叉熵损失呈显著线性关系，跨 Llama-3.1-8B、Qwen3-8B-Base、RecurrentGemma-9B 三种架构均成立。

### 近似损失与内在维度模块

近似损失对上下文长度的依赖通过**内在维度**（Intrinsic Dimension）来刻画。内在维度 $dim(l)$ 由 PCA 相对特征值阈值法测量，反映数据流形在内在空间中的有效维度。在训练场景下，近似损失与训练数据量 $D$ 和上下文长度 $l$ 的关系为：

$$\mathcal{L}_{Approx} = C_0 + \frac{A(l)}{D^{\alpha(l)}}, \quad \frac{\partial \alpha}{\partial l} < 0$$

其中指数 $\alpha(l)$ 随 $l$ 增加而减小，意味着上下文越长，增加训练数据带来的边际收益越低。附录进一步建立了贝叶斯风险与内在维度的线性关系：$R_{Bayes} = -s \cdot dim(l) + Const$，为近似损失的上下文长度依赖提供了几何解释。

### 最优上下文长度推导

将贝叶斯风险和近似损失对上下文长度的依赖联立，总损失可表达为：

$$\mathrm{Loss}(l, \theta_t, \theta_m) = R_{\mathrm{Bayes}}(l, \theta_t) + L_{\mathrm{Approx}}(l, \theta_m)$$

其中 $\theta_t$ 为任务参数（如任务对长上下文的依赖程度 $\gamma$），$\theta_m$ 为模型和数据参数。由于 $\partial R_{Bayes}/\partial l < 0$ 且 $\lim_{l \to \infty} \partial R_{Bayes}/\partial l = 0$，而 $\partial L_{Approx}/\partial l > 0$，总损失在导数零点处取得极小值，该点即**最优上下文长度** $l^*$。该最优值随训练数据量 $D$ 增大或模型能力增强而右移（增大），随任务对长上下文依赖程度 $\gamma$ 增大而左移（减小）。这一推导将上下文长度缩放行为统一到贝叶斯风险与近似损失的权衡框架中。

## 实验与关键发现

### 核心实验发现

本文在合成数据和真实语言模型上系统验证了内在熵框架的核心主张。实验围绕三个层次展开：总损失的分解机制、内在熵与交叉熵损失的线性关系、以及最优上下文长度的存在性与移动规律。

**损失分解与最优上下文长度的存在性。** 理论分析指出，总损失 $H(P, Q_l) = R_{Bayes} + L_{Approx}$ 中，贝叶斯风险随上下文长度递减，近似损失随上下文长度递增，二者导数符号相反，因此在特定条件下存在使总损失最小的最优上下文长度 $l^*$（Section 3, Equation 5）。实验在 OpenWebText 子集上验证了这一预测：对于每个固定的训练数据量，验证损失随上下文长度先降后升，存在一个明确的最优上下文长度（Figure 1 Middle, Figure 15）。更重要的是，该最优长度随训练数据量的增大而右移，这与近似损失对数据量的依赖关系一致——数据量增大降低了近似损失，使得贝叶斯风险的边际收益能在更长的上下文上继续主导总损失的下降。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_vnipyA8c9V/figures/001_Figure_1.jpg]]
*Figure 1: Left: Total loss is decomposed into Bayes Risk (decreasing with context length) and Approximation Loss (increasing with context length), so a critical point can emerge in some scenarios. Middle: Validation Loss Gap (Val Loss - minD(Val Loss) vs. Context Length), measured on subsets of OpenWebText, where we subtract the minimum loss within each dataset-size curve (please refer to Figure 15 for the original figure). For each training dataset size, there exists an optimal context length that minimizes pretraining validation loss, and this optimum increases with dataset size. Right: Error rate of Qwen series models on the CWE task from RulerBench when a certain amount of context is masked. Crit...*

**内在熵与交叉熵损失的线性关系。** 这是全文最核心的经验发现。在 Llama-3.1-8B、Qwen3-8B-Base 和 RecurrentGemma-9B 三个架构不同的模型上，使用高斯核密度估计（Gaussian-KDE）在隐藏层空间测量的内在熵与交叉熵损失之间呈现高度线性关系（Figure 2）。具体而言，Llama-3.1-8B 的 Pearson 相关系数 $R = -0.9888$，Qwen3-8B-Base 为 $R = -0.9960$，RecurrentGemma-9B 为 $R = -0.9967$（排除 3 个高 CE 损失的离群点后）。这一线性关系跨模型架构成立，为“贝叶斯风险负线性依赖于内在熵”的理论假设（$R_{Bayes} = -k \cdot S(P_l) + Const$）提供了强有力的实证支撑。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_vnipyA8c9V/figures/002_Figure_2.jpg]]
*Figure 2: Cross Entropy loss vs. Gaussian-KDE measured Intrinsic Entropy (in nats) for three Language Models on a subset of OpenWebText: Llama-3.1-8B (left, k = - 0 . 0 0 3 8 , R = - 0 . 9 8 8 8 ) ), Qwen3-8B-Base (middle, k = - 0 . 0 0 2 6 . R = - 0 . 9 9 6 0 ) , and RecurrentGemma-9B (right, k = - 0 . 0 1 7 4 R = - 0 . 9 9 6 7 , with 3 outlier points at high CE loss excluded from regression). The linear relationship between CE loss and Intrinsic Entropy holds across different model architectures*

**合成数据上的精确验证。** 在 Position-Weighted Multitask Sparse Parity 合成任务上，训练模型的交叉熵损失与理论最小损失（贝叶斯模型）几乎一致：上下文长度为 17 时，模型损失为 0.4648，理论最小值为 0.4643；上下文长度为 50 时，模型损失为 0.0613，理论最小值为 0.0612（Table 1）。这表明模型在合成任务上接近贝叶斯最优。同时，PCA 特征值对数求和测得的内在熵与交叉熵损失呈良好线性关系，$R^2$ 接近 1（Figure 7），进一步验证了内在熵作为信息度量的有效性。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_vnipyA8c9V/figures/011_Table_1.jpg]]
*Table 1: Comparison between trained model and Bayes Model (minimum CE Loss) for Synthetic Data*

### 消融与稳健性分析

**内在熵测量方法的稳健性。** 高斯-KDE 测量的内在熵与 PCA 测量的内在熵高度相关（$r = 0.997756$），且二者均与交叉熵损失线性相关（Figure 9）。这表明内在熵的线性关系对具体测量方法不敏感，无论是基于密度的估计还是基于特征谱的估计，都能捕捉到相同的信息结构。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_vnipyA8c9V/figures/010_Figure_9.jpg]]
*Figure 9: Gaussian-KDE measured Entropy (10000 samples, auto bandwidt 1 = 0 . 9 9 7 7 5 6 ) vs. PCAmeasured Entropy (left), Measrued ID (middle) and Cross Entropy Loss (right)*

**内在维度测量的鲁棒性。** 使用不同阈值（0.002–0.25）对 PCA 相对特征值取阈值来测量内在维度时，所有测量结果均与交叉熵损失保持线性关系（Figure 16, Section K.2）。这意味着内在维度与损失之间的线性关系对阈值选择具有鲁棒性，支持了“近似损失通过内在维度依赖于上下文长度”的理论推导。

**最优上下文长度的任务依赖性。** 在 Position-Weighted Ruler-QA1 任务上，QA 准确率随上下文长度先升后降，且最优上下文长度取决于任务对长上下文的依赖程度（参数 $\gamma$）。$\gamma$ 越大（即任务更依赖近距离上下文），最优上下文长度越小（Figure 4 Left）。同时，内在熵随上下文长度的变化趋势与准确率曲线在大 $\gamma$ 任务上高度相似（Figure 4 Right），表明内在熵能够部分解释下游任务性能的上下文长度缩放行为。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_vnipyA8c9V/figures/004_Figure_4.jpg]]
*Figure 4: Measured results on Position-Weighted Ruler-QA1 dataset. Left: QA accuracy vs. number of tokens input to the Language Model, for different tasks with different γ values. We observe that: (1) each curve shows a trend to increase and then decrease with context length; and (2) the critic point corresponds to a smaller optimal context length for tasks with larger γ (i.e. tasks requiring less long context abilities). Right: Intrinsic Entropy measured on samples truncated to certain context lengths. The Intrinsic Entropy shows increment of intrinsic information when increasing context length, and resembles acc-ctl curves for larger γ*

**RULER 基准上的跨任务验证。** 在 RULER 基准的多个子任务上，Qwen-3 系列模型（非思考模式的对话模型）表现出不同的上下文长度缩放模式（Figure 8, Section A.1）。在 qa1、fwe、cwe 子任务上，多数模型出现最优可见上下文长度，准确率先升后降；而在 vt（变量追踪）子任务上，性能持续随上下文长度提升，未观察到最优长度。这验证了理论预测：最优上下文长度的存在与否取决于任务特性（$\theta_t$）。此外，较大模型（如 Qwen3-8B 相对于 Qwen3-4B）在 cwe 子任务上不仅性能更好，最优上下文长度也更大，表明模型能力增强会右移最优上下文长度。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_vnipyA8c9V/figures/008_Figure_8.jpg]]
*Figure 8: Acc vs. Visible Context Length of Qwen-3 series models (non-thinking chat models) on 4 representative subsets of the RULER dataset: qa 1 (document qa, upper-left), fwe (frequent word extraction, upper-right), cwe (common words extraction, lower-left), and vt (variable tracking, lower-right), for a fixed max context length and a varying visible fraction of the input context. Most models show an optimal context length for qa 1, fwe and cwe subtask, while the vt subtask shows increased performance with respect to context length. Moreover, larger model tends to perform better and have a larger optimal context length, represented by the performance comparison between Qwen3-4B and Qwen3-8B on cwe...*

**合成数据上内在维度估计的精度。** 在合成任务上，PCA 估计的内在维度与理论任务数高度一致，且存在一个通用阈值可准确估计所有上下文长度下的内在维度（Figure 18, Section K.3）。这为内在维度作为数据流形复杂度的有效度量提供了直接证据，也支撑了近似损失通过内在维度与上下文长度关联的理论框架。

### 失败模式与局限

尽管实验证据整体支持理论框架，仍需注意以下局限：

- **离群点问题。** RecurrentGemma-9B 在 Figure 2 的回归分析中排除了 3 个高 CE 损失的离群点。这些离群点可能对应模型在特定上下文长度下出现表征退化或分布偏移的情况，提示内在熵测量在极端条件下可能不够稳定。
- **最优上下文长度的可观测性依赖于最大上下文长度设置。** 在 RULER 的 cwe 子任务上，当最大上下文长度设为 8k 时，最优上下文长度难以观测；但当最大上下文长度扩展到 16k 时，最优长度变得清晰可见（Figure A.3-2）。这表明实验设置中的上下文长度范围需要足够大，才能覆盖近似损失显著增长的区域。
- **理论假设的验证范围有限。** 内在熵与交叉熵损失的线性关系、内在维度与近似损失的关联等核心假设，目前仅在有限模型（Llama-3.1-8B、Qwen3-8B-Base、RecurrentGemma-9B）和特定数据集（OpenWebText 子集、合成任务、RULER）上得到验证。推广到更大规模模型和更多样化数据分布仍需进一步实验。

### 关键图表结论汇总

- **Figure 1：** 损失分解机制的可视化锚点，同时展示训练数据量对最优上下文长度的调节作用，以及下游任务（CWE）中临界点的存在。
- **Figure 2：** 跨模型验证内在熵与交叉熵损失线性关系的核心证据。
- **Figure 4：** 下游任务中上下文长度缩放的任务依赖性，以及内在熵对性能曲线的解释力。
- **Figure 7：** 合成数据上 PCA 特征值熵与交叉熵损失线性关系的精确验证。
- **Figure 8：** RULER 基准上跨任务、跨模型规模的上下文长度缩放模式差异。
- **Table 1：** 合成任务上训练模型接近贝叶斯最优的定量证据。

## 定位与知识库关联

### 核心贡献定位

本文提出的**内在熵分析框架（Intrinsic Entropy Framework）**并非一种新的模型架构或训练算法，而是一套用于理解和预测上下文长度缩放行为的理论工具。其核心贡献在于：将总交叉熵损失分解为**贝叶斯风险**（随上下文长度递减）与**近似损失**（随上下文长度递增）两个对抗性分量，并通过引入**内在熵**这一可测量变量，建立了从数据流形信息结构到模型性能的因果链条。

该框架的方法论定位可以从三个维度理解：

1. **损失分解维度**：延续了统计学习理论中将泛化误差分解为逼近误差与估计误差的经典范式，但在大语言模型的上下文长度缩放这一具体场景中，将分解锚定在贝叶斯最优模型与训练模型之间的KL散度上，使得分解具有可操作的测量路径。

2. **信息度量维度**：通过内在熵将上下文长度与可用信息量直接挂钩，并通过实验验证了交叉熵损失与内在熵之间的线性关系（跨 Llama-3.1-8B、Qwen3-8B-Base、RecurrentGemma-9B 三种架构均成立，Pearson相关系数绝对值均大于0.98）。这一线性关系构成了框架的经验基石。

3. **最优性预测维度**：从贝叶斯风险与近似损失对上下文长度的导数符号相反这一事实出发，推导出最优上下文长度的存在条件，并预测该最优值随训练数据量增加而右移——这一预测在 OpenWebText 子集和合成数据上均得到验证。

### 与已有工作的关系

本文的理论构建建立在多个研究线索的交叉点上，但与现有工作存在明确的边界和推进：

**缩放定律研究**：已有的神经语言模型缩放定律工作主要关注模型参数量、训练数据量与损失之间的幂律关系。本文的独特之处在于将上下文长度作为独立的缩放维度引入，并揭示了其影响损失的内在机制——不是简单的单调递减，而是贝叶斯风险下降与近似损失上升的权衡。附录D中，作者在比 Bahri et al. (2024) 更弱的假设下重新推导了近似损失的数据缩放形式，表明该框架在理论上具有更广的适用范围。

**长上下文能力评估**：RULER基准等工作关注模型在长上下文场景下的性能表现，但多停留在现象描述层面。本文通过修改 Position-Weighted Ruler-QA1 数据集（引入参数γ控制任务对长上下文的依赖程度），发现QA准确率随上下文长度先升后降，且最优上下文长度随γ增大而左移——这为长上下文能力的任务依赖性提供了定量解释框架。

**内在维度研究**：已有工作通过PCA等方法测量神经网络表示流形的内在维度，但多用于理解模型容量或泛化能力。本文将内在维度与近似损失相关联（通过PCA相对特征值取阈值法测量），并发现内在维度与交叉熵损失之间同样存在线性关系，且该关系对阈值选择具有鲁棒性（阈值从0.002到0.25范围内均成立）。

**信息论方法**：本文的内在熵概念与信息瓶颈理论等存在精神上的关联，但不同之处在于：内在熵是在预训练语言模型的隐藏层空间中进行操作化测量（通过高斯核密度估计或PCA特征值对数求和），而非从理论上下界推导。这种操作化使得框架可以直接应用于现有的黑盒模型。

### 适用边界与局限

尽管该框架在多个实验设置下展现出良好的解释力和预测力，其适用边界和局限同样需要明确：

**理论假设的依赖性**：框架的推导依赖于若干关键假设，包括预测一致性（Prediction Consistency）、线性熵关系（Linear Entropy Relationship）和均匀信息增益（Uniform Information Gain）。这些假设在本文的实验范围内得到了支持，但其在更广泛场景下的普遍性仍有待验证。特别是，线性熵关系假设内在空间熵与下一token预测熵之间存在稳定的线性映射，这一映射是否在分布外数据或对抗性输入下保持稳定尚不可知。

**测量方法的近似性**：内在熵的测量（无论是高斯KDE还是PCA特征值法）都是对真实信息熵的近似。高斯KDE的带宽选择、PCA的阈值设定都可能引入系统偏差。尽管消融实验显示不同测量方法之间高度相关（r=0.997756），且线性关系对参数选择不敏感，但测量误差在极端上下文长度下可能被放大。

**实验覆盖的有限性**：最优上下文长度的存在和变化规律主要在以下实验范围内得到验证：
- 预训练验证损失：OpenWebText子集，训练数据量从约1M到约100M tokens
- 下游任务：Position-Weighted Ruler-QA1和RULER的qa1、fwe、cwe子任务
- 模型：Llama-3.1-8B、Qwen3-8B-Base、RecurrentGemma-9B、Qwen-3系列

对于更大规模的数据集（如万亿token级别）、更大参数的模型（如百亿参数以上）、以及需要跨越极长距离的复杂推理任务（如RULER的vt子任务，其性能随上下文长度持续提升而未出现最优值），框架的预测能力尚需进一步检验。

**指标覆盖的局限性**：本文主要关注预训练交叉熵损失和下游任务准确率，但未深入探讨其他关键指标（如生成质量、事实一致性、推理链完整性）下的最优上下文长度行为。交叉熵损失的降低是否必然转化为这些更复杂指标的改善，是一个开放问题。

### 开放问题

基于本文的理论框架和实验发现，以下开放问题值得后续研究关注：

**理论深化方向**：
- 能否从更基本的原理（如数据生成过程的统计特性）出发，不依赖当前假设，推导内在熵与交叉熵损失的线性关系？
- 内在熵与内在维度之间的确切数学关系是什么？是否总是可以通过指数衰减特征值谱来关联？当特征值衰减偏离指数形式时，线性关系是否仍然成立？
- 在附录E中提出的最近邻距离上界中，当ε恰好等于(d+1)/d时，界的紧致性如何？能否去除或优化低密度区域的log D因子？

**实证扩展方向**：
- 在更大规模的数据集和模型上，最优上下文长度是否仍然遵循本文推导的规律？缩放行为是否会出现相变？
- 对于需要跨越极长距离的复杂推理任务（如RULER vt子任务），上下文长度缩放行为为何偏离框架预测？是否存在额外的补偿机制？
- 是否能够提出不依赖于特定神经网络表示空间的、更加模型无关的内在熵定义？例如，是否可以直接从token序列的统计特性中估计内在熵？

**应用前景**：
- 该框架能否用于指导实际的预训练数据配比和上下文长度选择？能否在训练前预测给定数据量下的最优上下文长度？
- 内在熵的实时监测能否作为训练过程中的早停信号或数据质量指标？

## 原文 PDF

![[paperPDFs/ICLR_2026/Intrinsic_Entropy_of_Context_Length_Scaling_in_LLMs.pdf]]
