---
title: "SimMotionEdit: Text-Based Human Motion Editing with Motion Similarity Prediction"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Prediction.pdf
aliases:
- SimMotionEdit
tags:
- CVPR_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "引入运动相似性预测作为辅助任务，通过条件Transformer量化运动帧间相似性，使模型在编辑前先识别需要修改的关键帧。"
primary_logic: "编辑任务与相似性预测的多任务联合训练能够促使模型学习语义上有意义的表示，且量化相似性标签优于连续回归，有助于平衡辅助任务与编辑任务并增强泛化能力。"
claims:
- "在MotionFix测试集上，SimMotionEdit在生成-目标检索(R@1)和M-score指标上显著优于所有基线方法。"
- "将运动相似性量化为3类进行交叉熵分类作为辅助损失，相比回归损失取得最佳性能。"
- "滤除低MotionSNR的噪声运动相似性曲线可提升模型性能。"
- "感知研究中，SimMotionEdit的对齐度和合理性评分分别比TMED高0.47和0.38（3分制）。"
---

# SimMotionEdit: Text-Based Human Motion Editing with Motion Similarity Prediction

> [!tip] 核心洞察
> 编辑任务与相似性预测的多任务联合训练能够促使模型学习语义上有意义的表示，且量化相似性标签优于连续回归，有助于平衡辅助任务与编辑任务并增强泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | SimMotionEdit：基于运动相似性预测的文本驱动人体运动编辑 |
| 英文题名 | SimMotionEdit: Text-Based Human Motion Editing with Motion Similarity Prediction |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2503.18211) · [GitHub](https://github.com/lzhyu/SimMotionEdit) |
| Topic |  |
| Method | SimMotionEdit |
| Dataset | MotionFix 测试集 |

> [!tip] 效果简介
> - MotionFix 测试集 上，R@1（生成-目标检索） ↑ 为 25.49，对比 TMED (baseline) 较低，变化 未计算。
> - MotionFix 测试集 上，L2 距离 (m) ↓ 为 0.253，对比 0.278 (TMED)，变化 0.025。
> - MotionFix 测试集 上，FID ↓ 为 0.110，对比 0.167 (TMED)，变化 0.057。

## 概述

**核心问题**：现有文本驱动的人体运动编辑方法在将源运动与文本指令对齐时缺乏精确控制，导致生成运动与语言指令之间出现语义错位——模型难以准确识别源运动中哪些帧需要修改、保留或删除。

**核心思路**：SimMotionEdit 将运动编辑重新表述为一个多任务学习问题，引入**运动相似性预测**作为辅助任务。其关键洞察在于：给定文本编辑指令，源运动与目标编辑运动之间的帧级相似性是可预测的。通过让模型在编辑前先学习预测哪些帧与目标运动相似（需保留）、哪些不相似（需修改），模型获得了对编辑位置的显式感知能力，从而生成语义上更对齐的编辑结果。

**方法定位**：SimMotionEdit 采用双 Transformer 架构——条件 Transformer 负责融合源运动特征与 CLIP 文本特征并预测运动相似性，扩散 Transformer 则基于增强后的条件特征执行去噪编辑生成。辅助任务采用量化分类（将连续相似性值离散化为 K 类）而非回归，实验表明分类损失能更好地平衡辅助任务与主编辑任务，并增强泛化能力。

**主要结果**：在 MotionFix 测试集上，SimMotionEdit 在生成-目标检索（R@1）和 M-score 指标上显著优于所有基线方法（Table 1）。感知研究中，SimMotionEdit 的对齐度和合理性评分分别比主要基线 TMED（Athavale et al., ArXiv 2024）高出 0.47 和 0.38 分（3 分制，Table A.1）。消融实验证实：运动相似性量化分类优于回归（Table 3），滤除低 MotionSNR 的噪声训练样本可进一步提升性能，同时增强文本与运动特征可带来最佳运动真实感（Table 2）。

## 背景与动机

### 问题背景

人体运动编辑旨在根据文本指令对给定的源运动序列进行修改，生成符合语言描述的目标运动。与从零开始的文本驱动运动生成不同，运动编辑要求模型同时理解源运动的时空结构与文本指令的语义意图，并在两者之间建立精确的对齐关系。这一任务在动画制作、虚拟人交互和游戏开发等领域具有广泛的应用前景。

### 现有方法的缺口

当前主流的文本驱动运动编辑方法，如基于扩散模型的**TMED**（Athavale et al., ArXiv 2024），虽然在生成运动的整体质量上取得了进展，但普遍存在一个核心瓶颈：**对源运动与文本指令之间的对齐缺乏精确控制**。具体而言，这些方法在编辑过程中难以准确识别源运动中需要修改的关键帧，导致生成的编辑运动与语言指令之间出现语义错位——模型可能修改了不该修改的动作部分，或未能充分响应文本所要求的编辑程度。

这一瓶颈的根源在于，现有方法将运动编辑建模为单一的条件生成任务，缺乏对“哪些帧需要编辑、编辑程度如何”这一关键信息的显式建模。模型仅通过条件信号隐式地学习编辑映射，缺少结构化的中间监督来引导编辑决策。

### 本文动机

本文的核心洞察在于：给定文本指令后，源运动与编辑运动之间的帧级相似性是可预测的，且这种相似性信息能够为编辑过程提供关键的定位信号。基于此，SimMotionEdit 提出**引入运动相似性预测作为辅助任务**，与运动编辑任务进行多任务联合训练。通过让模型在编辑前先学习识别需要修改的关键帧位置和修改程度，辅助任务为编辑过程提供了显式的结构化引导，从而缓解语义错位问题。

此外，为了有效融合文本与运动两种模态的信息并支持辅助任务的学习，SimMotionEdit 设计了**Motion Diffusion Transformer 架构**，将条件特征增强与扩散生成解耦为条件Transformer和扩散Transformer两个模块，使辅助任务与编辑任务各司其职、协同优化。

## 核心创新

SimMotionEdit的核心创新在于将**运动相似性预测**作为辅助任务引入文本驱动的人体运动编辑框架，从而解决了现有方法中源运动与文本指令对齐不精确、语义错位的瓶颈问题。具体而言，该方法通过以下三个关键设计实现了突破：

### 1. 辅助任务驱动的多任务学习范式

现有基线方法（如**TMED**，Athavale et al., ArXiv 2024）仅依赖单一的扩散模型进行运动编辑，缺乏对“哪些帧需要修改”的显式建模。SimMotionEdit引入运动相似性预测作为辅助任务，使模型在编辑前先识别源运动与目标运动之间的帧级相似性分布。这一设计源于一个直观观察：给定文本指令，源运动与编辑后运动之间的相似性是可预测的（Figure 3）。通过联合训练编辑任务与相似性预测任务，模型被迫学习语义上有意义的运动表示，从而更精确地将文本指令映射到需要修改的运动区域。

### 2. 量化相似性分类损失替代连续回归

与直接回归连续相似性值的朴素方案不同，SimMotionEdit将归一化后的运动相似性 $S_i^N$ 量化到 $K$ 个等长区间，将其转化为 $K$ 类分类问题：

$$\mathfrak{s}_i = \mathcal{Q}(S_i^N) := \begin{cases} 0, & S_i^N < \tau_0 \\ 1, & \tau_0 \leq S_i^N < \tau_1 \\ \vdots & \vdots \\ K-1, & S_i^N \geq \tau_{K-2} \end{cases}$$

辅助损失采用交叉熵形式：

$$\mathcal{L}_{\mathrm{aux}} = -\frac{1}{F} \sum_{i=0}^{F-1} \log p_{i,\mathfrak{s}_i}$$

消融实验（Table 3）表明，分类损失显著优于回归损失，且 $K=3$ 时达到最佳性能。这是因为量化分类降低了辅助任务的难度，使其与编辑主任务更好地平衡，同时避免了过多类别导致的类别间界限模糊。

### 3. MotionSNR滤波机制

并非所有训练样本的运动相似性曲线都具有清晰的语义结构。SimMotionEdit提出**MotionSNR**（运动信噪比）指标来量化相似性曲线的质量：

$$\mathrm{MotionSNR} = \frac{\sum_{x \in \mathbf{T}^R} x}{\sum_{x \in \mathbf{B}^R} x}$$

该指标计算相似性曲线中高值区域（Top-k帧）与低值区域（Bottom-k帧）的比值。高MotionSNR意味着相似性曲线具有明显的峰谷结构，更有利于辅助任务学习。实验证实（Table 1最后一行），滤除低MotionSNR的噪声训练样本可显著提升编辑性能，验证了数据质量对辅助任务有效性的关键影响。

### 4. 解耦的条件-扩散双Transformer架构

SimMotionEdit采用**条件Transformer + 扩散Transformer**的解耦架构（Figure 2），替代了TMED中单一的U-Net扩散模型。条件Transformer负责处理源运动与文本特征，同时输出运动相似性预测和增强后的条件特征；扩散Transformer则专注于接收增强特征进行去噪编辑。这一设计确保了辅助任务的输入与编辑任务解耦，使两个模块各司其职，避免了任务间的干扰。

**证据强度总结**：上述创新点的有效性均通过MotionFix测试集上的定量实验（Table 1, 2, 3）、感知研究（Table A.1）和消融分析得到验证，置信度较高（0.95-0.98）。主要局限在于方法仅在单一数据集上验证，且相似性量化类数 $K$ 和MotionSNR阈值的选择目前依赖经验设定。

## 整体框架

SimMotionEdit 提出了一种双 Transformer 解耦架构——**Motion Diffusion Transformer**，将文本驱动的人体运动编辑任务与运动相似性预测辅助任务统一在一个多任务训练框架中。如 Figure 2 所示，该架构由两个核心模块构成：**条件 Transformer**（Condition Transformer）和**扩散 Transformer**（Diffusion Transformer），二者分别承担条件增强与运动生成的职责。

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SimMotionEdit. (a) The architecture consists of two modules: the condition transformer and the diffusion transformer. The condition transformer performs the auxiliary task of motion similarity prediction and enables the source motion features and the text features to mix. The diffusion transformer takes in the enhanced text features, the embedded diffusion step t as the condition, the noisy edited motion, and the enriched source motion features, and predicts the denoised edited motions. (b) The auxiliary task motion similarity prediction is inspired by the fact that, given the text instructions, the similarity between source and edited motions is predictable. We use blue for the...*

### 输入与输出

系统的输入为一个三元组：源运动序列 $X = [x^0, x^1, ..., x^F]$、文本编辑指令 $L$，以及待编辑的目标运动 $M = [m^0, m^1, ..., m^{F'}]$。输出为与文本指令语义对齐的编辑后运动序列。

### 条件 Transformer：特征增强与相似性预测

条件 Transformer 是整个框架的**条件增强核心**。它同时接收源运动 $X$ 和文本指令 $L$，通过跨模态注意力机制使源运动特征与 CLIP 文本特征充分交互融合，输出增强后的文本特征与运动特征。这两个增强特征随后被送入扩散 Transformer 作为生成条件。

与此同时，条件 Transformer 承担**运动相似性预测**这一辅助任务：在特征融合过程中，模型被训练去预测源运动每一帧与编辑运动之间的相似性程度。具体而言，模型将增强特征映射到 $K$ 类离散相似性标签（通过量化连续相似性值得到），并计算辅助交叉熵损失 $\mathcal{L}_{\mathrm{aux}}$。这一设计的关键洞察在于：给定文本指令后，源运动与编辑运动之间的帧级相似性是可预测的；通过联合学习这一预测任务，模型被迫学习语义上有意义的运动表示，从而更精确地识别需要修改的关键帧。

### 扩散 Transformer：条件运动生成

扩散 Transformer 负责实际的运动生成。它接收三个条件输入——来自条件 Transformer 的**增强文本特征**、**增强源运动特征**，以及**扩散时间步 $t$ 的嵌入**——同时处理加噪后的编辑运动 $M_t$，预测去噪后的干净运动 $M_0$。

扩散过程遵循标准 DDPM 范式：前向过程按 $M_t = \sqrt{\bar{\alpha}_t} M_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$ 逐步向干净运动添加高斯噪声；反向过程则学习条件概率 $p_\theta(M_0 \mid c)$，通过预测原始干净信号来逐步去噪。编辑损失 $\mathcal{L}_e$ 采用均方误差形式：

$$\mathcal{L}_e = \mathbb{E}_{M_0 \sim q(M_0|L,X), t \sim [1,T]} \left[ \| M_0 - \mathcal{E}(M_t, t, L, X) \|_2^2 \right]$$

### 多任务联合训练

整个框架以端到端方式联合优化，总损失为编辑损失与辅助损失的直接相加：

$$\mathcal{L} = \mathcal{L}_{\mathrm{aux}} + \mathcal{L}_{\mathrm{e}}$$

这种解耦设计的核心优势在于：**辅助任务的输入与编辑任务相互解耦**，相似性预测仅依赖条件 Transformer 中的增强特征，不会干扰扩散 Transformer 的去噪过程。消融实验（Table 2）证实，同时增强文本与运动特征（而非仅增强其中一项）能带来最佳的运动真实感；而将相似性量化为 $K=3$ 类进行分类损失（Table 3），相比连续回归损失能显著提升编辑性能——分类损失促使模型学习更具判别力的表示，而过多类别则因类间边界模糊导致性能下降。

此外，框架引入了 **MotionSNR 滤波机制**来净化训练数据：对于相似性曲线噪声过高的训练样本（低 MotionSNR 值），直接滤除不参与辅助任务训练。Table 1 的消融显示，去除该滤波步骤会导致编辑性能明显下降，验证了干净相似性信号对辅助任务学习的重要性。

### 补充图表

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/001_Figure_1.jpg]]
*Figure 1: Text-Based Motion Editing. Our method SimMotionEdit generates edited human motion sequences from text instructions and source motion sequences*

## 核心模块与公式推导

### 扩散建模基础

SimMotionEdit 采用标准 DDPM 扩散范式进行训练与推理。设编辑运动序列为 $M_0 = [m^0, m^1, \dots, m^{F'}]$，前向扩散过程逐步向干净样本添加高斯噪声：

$$M_t = \sqrt{\bar{\alpha}_t} M_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon \quad \text{(Eq. 1)}$$

其中 $\bar{\alpha}_t$ 为累积噪声调度参数，$\epsilon \sim \mathcal{N}(0, I)$。给定条件 $c$（源运动 $X$ 与文本指令 $L$），逆向过程学习去噪以恢复干净运动，其条件概率为：

$$p_\theta(M_0 \mid c) = \int_{M_1}^{M_T} p(m_T) \prod_{u=1}^T p_\theta(m_{u-1} \mid m_u, c) \, \mathrm{d}\mathbf{m} \quad \text{(Eq. 2)}$$

编辑损失通过预测原始干净运动信号来训练扩散模型：

$$\mathcal{L}_e = \mathbb{E}_{M_0 \sim q(M_0|L,X), \, t \sim [1,T]} \left[ \| M_0 - \mathcal{E}(M_t, t, L, X) \|_2^2 \right] \quad \text{(Eq. 3)}$$

其中 $\mathcal{E}$ 为去噪网络，接收加噪运动 $M_t$、扩散步 $t$、文本指令 $L$ 和源运动 $X$，输出对 $M_0$ 的预测。

### 运动相似性预测：辅助任务设计

核心洞察在于：给定文本指令后，源运动与编辑运动之间的帧级相似性是可预测的。SimMotionEdit 将这一预测作为辅助任务，通过量化相似性分类来引导模型学习语义上有意义的表示。

**原始相似性计算。** 在旋转空间中，对源运动第 $i$ 帧 $x^i$，在编辑运动中以 $i$ 为中心的滑动窗口（半径 $W$）内寻找最小距离：

$$S_i^{Rr} = - \min_{|i-j| \leq W} d_r(x^i, m^j) \quad \text{(Eq. 4)}$$

其中 $d_r(\cdot,\cdot)$ 为旋转空间距离度量。该原始曲线 $S^R$ 经归一化至 $[0,1]$ 区间：

$$S_i^N = \frac{S_i^r - \min_j S_j^R}{\max_j S_j^R - \min_j S_j^R} \quad \text{(Eq. 6)}$$

**MotionSNR 滤波。** 并非所有训练样本的相似性曲线都具有清晰的编辑信号。定义运动信噪比来筛选高质量训练对：

$$\mathrm{MotionSNR} = \frac{\sum_{x \in \mathbf{T}^R} x}{\sum_{x \in \mathbf{B}^R} x} \quad \text{(Eq. 9)}$$

其中 $\mathbf{T}^R$ 和 $\mathbf{B}^R$ 分别为归一化相似性曲线中 top-$k$ 和 bottom-$k$ 帧的集合。MotionSNR 越高，表示相似性曲线的峰值与谷值对比越鲜明，编辑信号越清晰。滤除低 MotionSNR 的噪声样本可提升模型性能（参见 Table 1 中 w/o filtering 行的性能下降）。

**相似性量化与辅助损失。** 将连续相似性值 $S_i^N$ 量化到 $K$ 个等长区间，转换为离散类别标签：

$$\mathfrak{s}_i = \mathcal{Q}(S_i^N) := \begin{cases} 0, & S_i^N < \tau_0 \\ 1, & \tau_0 \leq S_i^N < \tau_1 \\ \vdots & \vdots \\ K-1, & S_i^N \geq \tau_{K-2} \end{cases} \quad \text{(Eq. 10)}$$

条件 Transformer 输出每帧的 logits $z_{i,k}$，经 softmax 转换为类概率：

$$p_{i,k} = \frac{\exp(z_{i,k})}{\sum_{l=0}^{K-1} \exp(z_{i,l})} \quad \text{(Eq. 11)}$$

辅助损失采用交叉熵，对全部 $F$ 帧的量化标签进行监督：

$$\mathcal{L}_{\mathrm{aux}} = -\frac{1}{F} \sum_{i=0}^{F-1} \log p_{i,\mathfrak{s}_i} \quad \text{(Eq. 12)}$$

消融实验（Table 3）证实：将相似性量化为 $K=3$ 类并使用分类损失，相比回归损失取得最佳性能；类别数超过 3 时，类别间距过近导致性能下降。

### 总损失函数

总损失由编辑损失与辅助损失直接相加构成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{aux}} + \mathcal{L}_{\mathrm{e}} \quad \text{(Eq. 13)}$$

这种多任务联合训练范式使模型在去噪生成编辑运动的同时，学习帧级相似性结构，从而增强文本指令与源运动之间的语义对齐。

### 双 Transformer 架构

SimMotionEdit 的网络架构由两个解耦的 Transformer 模块组成（Fig. 2）：

- **条件 Transformer**：接收源运动 $X$ 与 CLIP 文本特征，通过自注意力和交叉注意力混合两种模态信息，输出增强后的文本特征与运动特征。同时，其输出的运动特征经过相似性预测头映射为 $K$ 类 logits，用于计算 $\mathcal{L}_{\mathrm{aux}}$。该设计确保辅助任务的输入与编辑任务解耦。
- **扩散 Transformer**：以增强文本特征、扩散步嵌入 $t$ 作为条件，接收加噪编辑运动 $M_t$ 与增强后的源运动特征，预测去噪后的编辑运动 $\hat{M}_0$，由 $\mathcal{L}_e$ 监督。

消融实验（Table 2）表明：同时增强文本与运动特征（而非仅其中一项）可带来最佳运动真实感。

## 实验与分析

### 主实验结果

SimMotionEdit 在 MotionFix 测试集上对文本驱动运动编辑任务进行了系统评估。Table 1 报告了生成-目标检索（R@1、R@2、R@3）和 M-score 指标，SimMotionEdit 在所有指标上均显著优于基线方法 **TMED**（Athavale et al., ArXiv 2024）。其中 R@1 达到 25.49%，表明模型在检索生成运动与目标运动对齐方面具有明显优势。

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/006_Table_1.jpg]]
*Table 1: Comparison of Text-Based Motion Editing on the MotionFix [4] Dataset. Our method outperforms all other baselines on generated-to-target retrieval and M-score. We report R@1, R@2 and R@3 as percentages. ↑ indicates higher values are better, ↓ indicates lower values are better, bold indicates best, and underline indicates second best*

在附加性能评估（Table B.1）中，SimMotionEdit 同样表现出色：L2 距离降至 0.253（TMED 为 0.278），FID 降至 0.110（TMED 为 0.167）。这表明生成运动不仅与文本指令对齐更好，在运动真实感上也更接近真实分布。

感知研究（Table A.1）进一步验证了上述结论。在 3 分制 Likert 量表上，SimMotionEdit 的对齐度评分比 TMED 高 0.47 分，合理性评分高 0.38 分。Figure A.2 的评分分布显示，参与者在两项指标上给 SimMotionEdit 打 3 分的比例比 TMED 高出约 40%–50%。**需注意**：感知研究仅包含 15 名参与者，样本规模较小，统计效力有限。

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/004_Figure.jpg]]

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/014_Figure.jpg]]

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/015_Figure.jpg]]

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/013_Figure.jpg]]
*Figure: (a) Upper Part Figure A.1. Perceptual Study Layout. (Upper Part) We show an example of our study layout with one source motion, one edit instruction, and one edited motion. (Lower Part) We show the scoring instructions and scoring area for all the samples in the perceptual study. Figure A.2. Perceptual Evaluation Score Distributions. We show the distributions of aggregate responses from participants on the three versions of edited motions — Ground Truth, SimMotionEdit, and TMED — on the two metrics of Alignment and Plausibility. We observe that participants have marked 3 for SimMotionEdit about 40% to 50% more times than TMED across the two metrics*

### 消融实验

#### 条件特征增强策略

Table 2 比较了不同条件特征组合对性能的影响。当仅增强文本特征或仅增强运动特征时，模型性能均有所下降；同时增强文本与运动特征可获得最佳运动真实感。这表明条件 Transformer 中的跨模态特征混合机制对编辑质量至关重要。

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/007_Table_2.jpg]]
*Table 2: Performances of SimMotionEdit with Different Combinations of Condition Features. In the “no text feature” setting, the input to the condition transformer is the raw text. Using enhanced features for both text and motion leads to the best overall performance for motion realism*

#### 辅助损失设计

Table 3 展示了辅助损失类型和相似性量化类别数 K 的影响。核心发现：

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/008_Table_3.jpg]]
*Table 3: Performances of SimMotionEdit with Different Auxiliary Losses. Model performance improves when using a classification loss over a regression loss for the auxiliary task, indicating the better learning capacity enabled by classification. However, performance also decreases when increasing the number of classes beyond three, which brings the classes too close to each other*

- **分类损失优于回归损失**：将运动相似性量化为离散类别并使用交叉熵损失，比直接回归连续相似性值取得更好性能。这验证了量化分类有助于模型学习语义上有意义的表示，且能更好地平衡辅助任务与编辑任务。
- **类别数 K=3 最优**：当 K 超过 3 时性能下降，因为过多类别使得相邻类别间差异过小，增加了分类难度，反而削弱了辅助信号的引导作用。

#### MotionSNR 滤波

Table 1 最后一行报告了不使用 MotionSNR 滤波的变体性能。滤除低 MotionSNR 的噪声训练样本可提升编辑性能，验证了数据质量对辅助任务有效性的影响——噪声相似性曲线会引入误导性监督信号，损害模型学习。

### 失败模式与局限性

1. **数据依赖性**：方法依赖带三元组（源运动-文本指令-编辑运动）的标注数据，此类数据获取成本高。当前仅在 MotionFix 数据集上验证，对其他运动编辑场景的泛化能力尚不明确。

2. **相似性量化的适应性**：辅助任务采用等长区间离散化（Eq. 10），阈值选择固定。对于编辑幅度差异较大的指令类型，统一的量化方案可能无法提供最优的监督粒度。

3. **感知研究规模**：15 名参与者的样本量使统计结论的稳定性受限，该部分结果需谨慎解读。

### 关键图表结论总结

| 图表 | 核心结论 |
|------|----------|
| Table 1 | SimMotionEdit 在生成-目标检索和 M-score 上全面超越基线，MotionSNR 滤波有益 |
| Table 2 | 同时增强文本与运动特征带来最佳运动真实感 |
| Table 3 | 量化分类损失（K=3）优于回归损失；类别过多则性能下降 |
| Table A.1 | 感知评分中 SimMotionEdit 对齐度和合理性均显著优于 TMED |
| Table B.1 | L2 距离和 FID 指标进一步验证生成质量优势 |

### 补充图表

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/016_Figure.jpg]]
*Figure: C.1. More Qualitative Results*

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/003_Figure_3.jpg]]
*Figure 3: Raw Motion Similarity. We translate the global positions of sampled poses of the source motion and the edited motion for a clear view*

![[assets/figures/papers/paper_list_l23_SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Pre/figures/009_Table.jpg]]
*Table: A.1. Perceptual Evaluation Mean Statistics. We report the mean scores achieved by all three candidates in the perceptual study, averaging the aggregated responses across all the participants and sample sets. SimMotionEdit achieves scores that are 0.3 to 0.5 points higher than TMED on a 3-point Likert Scale*

## 方法谱系与知识库定位

### 任务定位与核心差异

SimMotionEdit 面向**文本驱动的人体运动编辑**任务：给定一段源运动序列和一条自然语言编辑指令，生成与指令语义一致、同时保留源运动无关部分的编辑后运动。该任务与无条件运动生成（如 MDM、MLD）和文本到运动生成（如 T2M-GPT、MotionDiffuse）有本质区别——后者仅需从文本生成运动，而编辑任务必须同时满足“对齐文本指令”和“保持未编辑部分不变”的双重约束。

在文本驱动运动编辑这一子领域中，SimMotionEdit 最直接的基线是 **TMED**（Athavale et al., ArXiv 2024），后者基于扩散模型实现运动编辑，但在对齐源运动与文本指令时缺乏精确的帧级控制，导致生成运动与语言指令之间出现语义错位。SimMotionEdit 的核心突破在于引入**运动相似性预测**作为辅助任务，使模型在编辑前先“识别需要修改的关键帧”，从而缩小编辑动作的搜索空间，缓解语义错位问题。

### 方法谱系：从扩散生成到多任务条件建模

从方法演进角度看，SimMotionEdit 位于以下三条技术路线的交汇点：

1. **扩散模型在运动生成中的应用**：SimMotionEdit 沿用了 DDPM（Ho et al., 2020）的标准扩散范式，前向过程逐步加噪，反向过程以源运动和文本为条件去噪生成编辑运动。这与 MDM（Tevet et al., ICLR 2023）、MotionDiffuse（Zhang et al., TPAMI 2024）等基于扩散的运动生成方法共享技术基础，但 SimMotionEdit 将扩散模型从“无条件/文生运动”迁移到了“条件运动编辑”场景。

2. **Transformer 架构对运动序列的建模**：SimMotionEdit 采用 **Motion Diffusion Transformer** 架构，由条件 Transformer 和扩散 Transformer 两个模块组成。这种双 Transformer 解耦设计在运动生成领域尚不多见——多数方法（如 TMED）使用 U-Net 作为去噪骨干。条件 Transformer 负责文本-运动特征融合与相似性预测，扩散 Transformer 专注于去噪编辑，这种分工与多模态 Transformer（如 CLIP 的双塔结构）的设计理念一脉相承。

3. **辅助任务驱动的表示学习**：将辅助任务与主任务联合训练以学习更好表示，是自监督学习和多任务学习中的经典策略。SimMotionEdit 的创新在于为运动编辑任务专门设计了**运动相似性预测**这一辅助任务——通过量化源运动与编辑运动之间的帧级相似性为 K 个类别，以交叉熵分类损失作为辅助信号。这种“先识别差异区域再编辑”的范式，在图像编辑领域（如 InstructPix2Pix 的隐式注意力引导）有类似思想，但在运动编辑中属于首次明确建模。

### 关键设计决策与消融证据

SimMotionEdit 的几个关键设计选择均有消融实验支撑，构成了方法有效性的因果链条：

- **运动相似性量化优于连续回归**：Table 3 显示，将相似性量化为 3 类并使用分类损失，性能显著优于回归损失。原因在于量化将连续相似性值映射到粗粒度语义类别（“高度相似”“部分相似”“需要修改”），降低了辅助任务的学习难度，同时避免了回归损失与编辑损失之间的尺度冲突。当类别数超过 3 时性能下降，说明过细的量化使类别间边界模糊，反而引入噪声。

- **MotionSNR 滤波提升训练质量**：Table 1 中“w/o filtering”变体的性能下降表明，滤除低 MotionSNR 的噪声训练样本对模型性能至关重要。MotionSNR（Eq. 9）定义为相似性曲线中 Top-k 帧与 Bottom-k 帧的比值，低 MotionSNR 意味着该训练样本的相似性曲线缺乏清晰的“需要编辑”信号，使用这类样本训练辅助任务会引入误导性梯度。

- **文本与运动特征的双向增强**：Table 2 的消融表明，同时增强文本特征和运动特征（而非仅增强其中一项）可获得最佳运动真实感。这验证了条件 Transformer 中跨模态信息融合的必要性——文本特征需要运动上下文来定位编辑目标，运动特征需要文本语义来理解编辑意图。

### 适用边界与局限

尽管 SimMotionEdit 在 MotionFix 测试集上取得了显著优于 TMED 的性能（R@1 达 25.49，感知评价对齐度高出 0.47 分），其适用边界和局限同样值得关注：

1. **数据依赖性**：方法依赖带三元组（源运动、文本指令、编辑运动）标注的数据集，此类数据获取成本高。当前仅在 MotionFix 上验证，该数据集的编辑指令类型和运动风格覆盖范围有限，方法在更大规模、更多样化编辑场景下的泛化能力尚未得到验证。

2. **相似性量化的固定阈值**：辅助任务采用等长区间量化（Eq. 10），阈值 τ₀, τ₁, ... 由归一化后的相似性范围均匀划分。这种固定划分可能无法适应所有编辑类型——例如，“大幅改变动作”与“微调手臂角度”的最优量化粒度可能不同。论文未探讨自适应阈值或学习式量化策略。

3. **感知研究规模有限**：感知评价仅包含 15 名参与者，虽在 Table A.1 和 Figure A.2 中显示出 SimMotionEdit 相对于 TMED 的一致优势（对齐度 +0.47，合理性 +0.38，3 分制），但小样本量限制了统计结论的稳健性，且参与者群体的代表性未详细说明。

4. **单帧编辑粒度的局限**：运动相似性预测以帧为单位计算相似性，隐含假设编辑操作在时间上是局部且连续的。对于涉及全局时序结构调整的编辑（如“将整个动作加快一倍”或“交换两个动作片段的顺序”），帧级相似性可能无法提供有效的辅助信号。

### 开放问题与未来方向

基于上述分析，SimMotionEdit 开启的研究方向包括：

- **运动相似性预测的泛化能力**：该辅助任务能否推广到更复杂的文本指令（如多步编辑、条件编辑）和多人物交互场景？相似性预测的“先定位后编辑”范式是否为运动编辑的通用框架？

- **自适应相似性量化**：如何根据编辑指令的语义自动确定最优的量化类别数 K 和滤波阈值？是否可以通过元学习或基于指令的条件量化来实现？

- **双 Transformer 架构的通用性**：条件 Transformer 与扩散 Transformer 的解耦设计在其他多模态生成任务（如视频编辑、语音驱动手势生成）中是否同样有效？这种架构分离是否有利于模块化的预训练与微调？

- **数据效率与弱监督扩展**：能否利用大规模文本-运动对数据（无编辑三元组）进行预训练，仅用少量编辑数据微调？运动相似性预测任务本身是否可以作为自监督信号，从无标注的运动对中自动挖掘编辑关系？

## 原文 PDF

![[paperPDFs/CVPR_2025/SimMotionEdit_Text_Based_Human_Motion_Editing_with_Motion_Similarity_Prediction.pdf]]