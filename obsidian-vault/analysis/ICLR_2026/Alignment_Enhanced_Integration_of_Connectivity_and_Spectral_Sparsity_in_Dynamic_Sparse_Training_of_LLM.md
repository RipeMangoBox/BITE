---
title: "Alignment-Enhanced Integration of Connectivity and Spectral Sparsity in Dynamic Sparse Training of LLM"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Alignment_Enhanced_Integration_of_Connectivity_and_Spectral_Sparsity_in_Dynamic_Sparse_Training_of_LLM.pdf
openreview_forum_id: jZplmg7Ad9
aliases:
- AEICSSDSTL
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "引入对齐损失（alignment loss）和低秩分支的激活调整（activation adjustment）。对齐损失显式惩罚两个分支输出之间的不一致性，激活调整稳定低秩表示，共同减少冲突，促进协作，从而提升极稀疏下的训练效果。"
primary_logic: "提出重叠抵消率（OCR）量化抵消效应，并设计对齐增强的训练方案，在动态稀疏训练中系统融合连通性稀疏与谱稀疏；通过层对齐损失特别缓解注意力Q、K层中的冲突，实现参数高效预训练性能的显著提升。"
claims:
- "对齐增强方案（Act+Align）在所有稀疏度、模型和数据集上均比朴素集成（Naive）显著降低验证困惑度，Wilcoxon符号秩检验p<0.001。"
- "引入对齐损失后，注意力Q和K层的重叠抵消率（OCR）明显下降，表明抵消效应得到有效缓解。"
- "LLaMA-60M, OpenWebText, s_total=0.9 上 PPL↓ = 31.77"
- "LLaMA-130M, C4, s_total=0.7 上 PPL↓ = 26.19"
---

# Alignment-Enhanced Integration of Connectivity and Spectral Sparsity in Dynamic Sparse Training of LLM

> [!tip] 核心洞察
> 提出重叠抵消率（OCR）量化抵消效应，并设计对齐增强的训练方案，在动态稀疏训练中系统融合连通性稀疏与谱稀疏；通过层对齐损失特别缓解注意力Q、K层中的冲突，实现参数高效预训练性能的显著提升。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大语言模型动态稀疏训练中的对齐增强连接-谱稀疏整合 |
| 英文题名 | Alignment-Enhanced Integration of Connectivity and Spectral Sparsity in Dynamic Sparse Training of LLM |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jZplmg7Ad9) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | CHTsL |
| Dataset | LLaMA-60M, OpenWebText, s_total=0.9, LLaMA-130M, C4, s_total=0.7, LLaMA-350M |

> [!tip] 效果简介
> - LLaMA-60M, OpenWebText, s_total=0.9 上，PPL↓ 为 31.77，对比 33.90 (SLTrain)，变化 2.13。
> - LLaMA-130M, C4, s_total=0.7 上，PPL↓ 为 26.19，对比 26.78 (SLTrain)，变化 0.59。
> - LLaMA-350M, OpenWebText, s_total=0.9 上，PPL↓ 为 18.40，对比 18.99 (SLTrain)，变化 0.59。

## 概述

动态稀疏训练是降低大语言模型（LLM）预训练成本的核心路径之一。现有工作分别从**连通性稀疏**（动态剪枝与重生长）和**谱稀疏**（低秩分解）两个维度压缩参数，但简单地将二者叠加时，两个分支的输出会产生方向相反的冲突信号，导致**抵消效应**（cancellation effect），严重削弱模型的表达能力。本文首次通过**重叠抵消率**（Overlap Cancellation Ratio, OCR）量化了这一现象，并揭示注意力层的Q、K投影是冲突最剧烈的部位。

针对上述瓶颈，本文提出**对齐增强的连通性-谱稀疏整合框架 CHTsL**。其核心操控变量包括两项：一是在低秩分支中插入 **SiLU 激活**以稳定表示；二是引入**逐层对齐损失**，显式惩罚稀疏分支与低秩分支输出之间的 Frobenius 距离，迫使二者方向一致、协同学习。该方法以 CHTs（Zhang et al., 2025）作为动态连通性稀疏基础，与低秩分解结合，形成统一的参数高效预训练方案。

实验表明，对齐增强策略（Act+Align）在所有稀疏度、模型规模和数据集上均显著优于朴素求和（Naive），Wilcoxon 符号秩检验 p < 0.001。在 LLaMA-60M 至 350M 参数规模、OpenWebText 和 C4 数据集上，CHTsL 在相同参数预算下一致超越 SLTrain（Han et al., 2024）等现有最优基线。例如，在总稀疏度 0.9 下，LLaMA-60M 的验证困惑度从 SLTrain 的 33.90 降至 31.77（Table 2）。消融分析进一步证实，仅对 Q、K 层施加对齐损失即可取得与全层对齐相当甚至更优的效果，验证了注意力层冲突缓解的关键作用。

## 背景与动机

大语言模型（LLM）的预训练对计算和存储资源的需求极为庞大，参数高效训练（parameter-efficient training）因此成为降低门槛的关键方向。其中，稀疏训练通过在训练阶段维持稀疏权重矩阵，有望在保持模型能力的同时显著减少计算开销。

现有稀疏训练方法大致可分为两个家族：

- **连通性稀疏（connectivity sparsity）**：通过掩码直接剔除部分权重，使网络仅保留一个稀疏子集。早期方法如 **SET**（Mocanu et al., 2018）采用静态稀疏模式，而 **RigL**（Evci et al., 2020）、**MEST**（Yuan et al., 2021）及更近期的 **CHTs**（Zhang et al., 2025）则引入动态稀疏训练（DST），在训练过程中周期性地调整连接模式，以更灵活地探索稀疏子网络。
- **谱稀疏（spectral sparsity）**：利用矩阵低秩分解，将全秩权重替换为两个低秩矩阵的乘积，从而在参数层面实现压缩。代表性工作如 **CoLA**（Liu et al., 2025）专注于低秩训练，而 **SLTrain**（Han et al., 2024）则尝试将静态稀疏与低秩分解结合，形成混合稀疏训练方案。

然而，将动态连通性稀疏训练与谱稀疏训练简单结合时，存在一个被忽视的根本性问题：**两个分支的输出会产生方向相反的冲突信号，导致抵消效应（cancellation effect）**。具体而言，当连通性稀疏分支的输出 $S^{(l)}$ 与低秩分支的输出 $L^{(l)}$ 在符号上相反时，二者相加后重叠部分相互抵消，削弱了层的整体表达能力，限制了极稀疏条件下混合训练的性能上限。

为量化这一现象，本文定义了**重叠抵消率（Overlap Cancellation Ratio, OCR）**：

$$\mathrm{OCR} = \frac{\sum_i \min(|S_i|, |L_i|) \cdot \mathbf{1}\{S_i L_i < 0\}}{\sum_i \min(|S_i|, |L_i|) + \varepsilon}$$

该指标衡量两个分支输出中因符号相反而被取消的重叠信号占比，取值越接近1表示抵消越严重。

基于上述诊断，本文的核心动机是：**能否通过系统性地缓解抵消效应，实现连通性稀疏与谱稀疏的真正协同？** 为此，本文提出对齐增强的集成框架，在动态稀疏训练中引入显式的分支对齐机制，从而在极稀疏（如仅保留10%~30%参数）条件下显著提升参数高效预训练的性能。

## 核心创新

CHTsL的核心创新在于系统性地诊断并解决了动态连通性稀疏训练与谱稀疏（低秩）训练简单结合时产生的**抵消效应（cancellation effect）**，并通过两个关键机制将二者的冲突转化为协作。

### 瓶颈诊断：重叠抵消率（OCR）

当动态稀疏分支的输出 $S^{(l)}$ 与低秩分支的输出 $L^{(l)}$ 直接求和时，若两者在相同位置产生方向相反的信号，重叠部分将相互抵消，削弱模型的整体表达能力。为量化这一现象，本文定义了**重叠抵消率（Overlap Cancellation Ratio）**：

$$\mathrm{OCR} = \frac{\sum_i \min(|S_i|, |L_i|) \cdot \mathbf{1}\{S_i L_i < 0\}}{\sum_i \min(|S_i|, |L_i|) + \varepsilon}$$

该指标衡量两个分支输出中因符号相反而被抵消的重叠部分占比，取值 $[0,1)$。实验表明，朴素求和策略下注意力层的Q、K矩阵中OCR值显著偏高，这是性能损失的直接根源。

### 关键创新一：对齐损失机制

为解决上述抵消效应，CHTsL引入了**逐层对齐损失（alignment loss）**，显式惩罚稀疏分支与低秩分支输出之间的方向不一致：

$$\mathcal{L}_{\mathrm{align}}^{(l)} = \frac{1}{BN} \|S^{(l)} - L^{(l)}\|_F, \quad \mathcal{L}_{\mathrm{align}} = \sum_l \mathcal{L}_{\mathrm{align}}^{(l)}$$

该损失以Frobenius范数度量两个分支输出的差异，加权后加入总训练目标：

$$\mathcal{L} = \mathcal{L}_{\mathrm{task}} + \lambda \mathcal{L}_{\mathrm{align}}$$

其中 $\lambda$ 为对齐损失系数（LLaMA-60M在OpenWebText及LLaMA-130M上取0.5，LLaMA-60M在C4上取0.3）。对齐损失引导两个分支产生方向一致的输出，从根本上缓解抵消效应。**Figure 2** 的可视化证实，引入对齐损失后，注意力Q、K层的OCR值随训练步数显著下降。

### 关键创新二：低秩分支激活调整

在朴素方案中，低秩分支的输出仅为两个低秩矩阵的乘积 $B^{(l)} A^{(l)} x$（恒等映射），训练稳定性不足。CHTsL在低秩分解矩阵之间插入非线性激活函数，将低秩输出修改为：

$$L^{(l)} = B^{(l)} \sigma(A^{(l)} x)$$

其中 $\sigma(\cdot)$ 采用SiLU（Swish）激活。这一调整稳定了低秩表示，为对齐机制提供了更可靠的协作基础。消融实验（Table 10）表明，SiLU在多数配置下优于ReLU和GeLU。

### 与基线方法的差异

| 对比维度 | 基线方法 | CHTsL |
|---------|---------|-------|
| 分支融合方式 | 简单求和（如SLTrain, Han et al., 2024） | 对齐损失引导的协作融合 |
| 低秩分支激活 | 恒等映射 | SiLU非线性激活 |
| 冲突处理 | 无显式机制 | OCR量化 + 对齐损失显式约束 |

消融实验（**Table 1**）提供了决定性证据：对齐增强方案（Act+Align）在所有12组实验（模型×数据集×稀疏度）上均显著优于朴素求和（Naive），Wilcoxon符号秩检验 $p < 0.001$。仅施加激活调整（Act）虽有一定改善，但远不及完整对齐方案。值得注意的是，**Table 7** 进一步揭示，仅对注意力层的Q、K投影施加对齐损失即可取得与全层对齐相当甚至更优的效果，这与OCR分析中Q、K层抵消效应最严重的发现高度一致。

该对齐增强框架具有通用性：**Table 13** 表明，将其应用于静态稀疏、SET（Mocanu et al., 2018）等不同连通性稀疏方法及不同初始化策略时，均能一致降低困惑度。

## 整体框架

CHTsL 是一个将动态连通性稀疏训练与谱稀疏（低秩）训练进行对齐增强整合的统一框架。其核心设计动机源于一个关键发现：当简单地将动态稀疏分支的输出与低秩分支的输出相加时，两分支会产生方向相反的冲突信号，导致**抵消效应（cancellation effect）**，削弱模型的整体表达能力。为此，CHTsL 通过引入对齐损失和低秩分支的激活调整，系统性地缓解这一冲突，促进两分支的协作学习。

框架由四个核心模块构成，其整体工作流如 Figure 1 所示：

**1. 动态连通性稀疏分支**

该分支采用 CHTs（Zhang et al., 2025）作为动态稀疏训练算法，维持并持续更新非结构化稀疏连接模式。对于每一层的输入 $x$，该分支输出连通性稀疏表示 $S^{(l)}$，其可训练参数量由稀疏度 $s$ 控制。

**2. 谱稀疏（低秩）分支**

该分支通过低秩分解矩阵 $B^{(l)} A^{(l)}$ 对层权重进行参数化，并在两矩阵之间插入 SiLU（Swish）非线性激活函数：

$$L^{(l)} = B^{(l)} \sigma(A^{(l)} x)$$

这一激活调整（activation adjustment）的设计旨在稳定低秩表示的训练动态，防止低秩分支输出退化。消融实验证实，SiLU 在多数配置下优于 ReLU 和 GeLU（Table 10）。

**3. 对齐损失模块**

该模块是框架的核心创新。它逐层计算稀疏分支输出 $S^{(l)}$ 与低秩分支输出 $L^{(l)}$ 之间的 Frobenius 范数距离：

$$\mathcal{L}_{\mathrm{align}}^{(l)} = \frac{1}{BN} \|S^{(l)} - L^{(l)}\|_F, \quad \mathcal{L}_{\mathrm{align}} = \sum_l \mathcal{L}_{\mathrm{align}}^{(l)}$$

该损失显式惩罚两分支输出之间的不一致性，引导它们产生方向一致的信号，从而减少抵消效应。对齐损失的加权系数 $\lambda$ 在不同配置下设为 0.5 或 0.3（Section 4.5）。

**4. 输出融合**

每一层的最终输出为两分支输出的直接求和：

$$O^{(l)} = S^{(l)} + L^{(l)}$$

整体训练目标为语言建模任务损失与加权对齐损失之和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{task}} + \lambda \mathcal{L}_{\mathrm{align}}$$

在参数预算方面，组合方法的总稀疏度定义为：

$$s_{\mathrm{total}} = 1 - d_{\mathrm{connectivity}} - d_{\mathrm{spectral}}$$

其中 $d_{\mathrm{connectivity}}$ 和 $d_{\mathrm{spectral}}$ 分别为连通性稀疏分支和谱稀疏分支的密度。所有对比方法在相同的 $s_{\mathrm{total}}$ 约束下进行公平比较，通过网格搜索分配两分支的参数比例并报告最佳配置结果。

值得注意的是，后续分析（Table 7）表明，仅对注意力层的 Q、K 投影施加对齐损失，即可取得与对所有线性层施加对齐相当甚至更优的困惑度，且显著优于仅对齐其他层（胜率 0.42 vs 0.08），这揭示了抵消效应主要集中在注意力机制的查询和键计算中的现象。

## 核心模块与公式推导

### 问题量化：重叠抵消率（OCR）

简单将动态连通性稀疏分支与谱稀疏（低秩）分支的输出相加时，两个分支可能产生方向相反的信号，导致相互抵消。为量化这一抵消效应，论文定义了重叠抵消率（Overlap Cancellation Ratio, OCR）：

$$\mathrm{OCR} = \frac{\sum_i \min(|S_i|, |L_i|) \cdot \mathbf{1}\{S_i L_i < 0\}}{\sum_i \min(|S_i|, |L_i|) + \varepsilon}$$

其中 $S_i$ 和 $L_i$ 分别为稀疏分支与低秩分支输出向量中的对应元素。OCR 衡量的是：在两个分支输出重叠（即两者均非零）的部分中，因符号相反而被抵消的比例，取值范围为 $[0,1)$。OCR 越高，说明抵消效应越严重，两分支的协同越差。

### 核心模块一：低秩分支的激活调整

朴素低秩分解 $L = BAx$ 在极端稀疏条件下训练不稳定。论文在低秩矩阵 $A$ 和 $B$ 之间插入非线性激活函数 $\sigma(\cdot)$：

$$L^{(l)} = B^{(l)} \sigma(A^{(l)} x)$$

其中 $A^{(l)} \in \mathbb{R}^{r \times d_{\text{in}}}$、$B^{(l)} \in \mathbb{R}^{d_{\text{out}} \times r}$ 为第 $l$ 层的低秩分解矩阵，$r$ 为秩。论文选用 **SiLU**（Swish）作为激活函数，实验表明其在多数配置下优于 ReLU 和 GeLU（Table 10），有效稳定了低秩表示的学习。

### 核心模块二：层对齐损失

为缓解两分支输出的抵消效应，论文引入逐层对齐损失，显式惩罚稀疏输出 $S^{(l)}$ 与低秩输出 $L^{(l)}$ 之间的 Frobenius 距离：

$$\mathcal{L}_{\mathrm{align}}^{(l)} = \frac{1}{BN} \|S^{(l)} - L^{(l)}\|_F, \quad \mathcal{L}_{\mathrm{align}} = \sum_l \mathcal{L}_{\mathrm{align}}^{(l)}$$

其中 $B$ 为批次大小，$N$ 为输出维度。该损失引导两个分支产生方向一致的输出信号，从而减少 OCR。消融实验表明，仅对注意力层的 **Q、K 投影**施加对齐损失即可取得与全层对齐相当甚至更优的困惑度（Table 7），说明抵消效应主要集中在 Q、K 层。

### 核心模块三：输出融合与整体训练目标

每层的最终输出为稀疏分支与低秩分支的直接求和：

$$O^{(l)} = S^{(l)} + L^{(l)}$$

整体训练目标为语言建模任务损失与加权对齐损失之和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{task}} + \lambda \mathcal{L}_{\mathrm{align}}$$

其中 $\lambda$ 为对齐损失系数。对于 LLaMA-60M 在 OpenWebText 及 LLaMA-130M 上的实验，$\lambda=0.5$；对于 LLaMA-60M 在 C4 上的实验，$\lambda=0.3$（Section 4.5）。

### 稀疏度与参数预算约束

论文在统一的参数预算下比较各方法。连通性稀疏的稀疏度 $s$ 和低秩分支的秩 $r$ 共同决定总稀疏度：

$$s_{\mathrm{total}} = 1 - d_{\mathrm{connectivity}} - d_{\mathrm{spectral}}$$

其中 $d_{\mathrm{connectivity}} = 1 - s$ 为连通性稀疏分支的密度，$d_{\mathrm{spectral}}$ 为低秩分支相对于稠密矩阵的参数密度。实验通过网格搜索分配两分支的参数比例，并报告最佳配置下的结果（Table 4, Table 5）。

### 方法流程概览

CHTsL 的整体流程（Figure 1）可概括为四个模块的协同：

1. **动态连通性稀疏分支**：采用 CHTs（Zhang et al., 2025）动态稀疏训练算法，维持并更新稀疏连接模式，生成输出 $S^{(l)}$。
2. **谱稀疏（低秩）分支**：通过低秩分解 $B^{(l)}\sigma(A^{(l)}x)$ 生成稳定低秩输出 $L^{(l)}$。
3. **对齐损失模块**：逐层计算 $S^{(l)}$ 与 $L^{(l)}$ 的 Frobenius 距离并加权求和，引导方向一致。
4. **输出融合**：$O^{(l)} = S^{(l)} + L^{(l)}$，两分支输出直接相加。

该框架具有通用性：对齐增强训练方案在结合不同连通性稀疏方法（静态稀疏、SET、CHTs）及不同初始化策略时均能一致降低困惑度（Table 13）。

## 实验与分析

### 核心瓶颈：朴素集成的抵消效应

简单地将动态连通性稀疏分支（CHTs）与谱稀疏分支（低秩分解）的输出直接相加（Naive策略）存在根本性问题：两个分支产生的信号方向相反，导致重叠部分相互抵消。论文引入**重叠抵消率（Overlap Cancellation Ratio, OCR）** 来量化这一现象：

$$\mathrm{OCR} = \frac{\sum_i \min(|S_i|, |L_i|) \cdot \mathbf{1}\{S_i L_i < 0\}}{\sum_i \min(|S_i|, |L_i|) + \varepsilon}$$

OCR 衡量两个分支输出中因符号相反导致重叠部分被取消的比例，取值范围为 $[0, 1)$。实验表明，注意力层的 Query 和 Key 投影矩阵是抵消效应的重灾区——这正是模型表达能力受损的关键位置。

### 方案有效性验证：对齐增强集成策略

Table 1 报告了三种集成策略在 LLaMA-60M 和 LLaMA-130M 两个模型、OpenWebText 和 C4 两个数据集、以及 0.7/0.8/0.9 三种总稀疏度下的验证困惑度（PPL↓）。策略对比如下：

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/002_Table_1.jpg]]
*Table 1: Comparison between different integration strategies. The table consists of two parts: a. The performance of different integration strategies, reported in terms of validation perplexity (PPL↓). The Naive strategy corresponds to a simple sum of CHTs and low-rank factorization. The Act strategy applies activation adjustment to the low-rank factorization branch. The Act+Align strategy combines activation adjustment with the alignment loss. The coefficient of the alignment loss λ is reported in Section 4.5. The sparsity configuration is set such that the sparse branch and the low-rank branch have the same number of trainable parameters $\begin{array} { r } { \frac { { d _ { c o n n e c t i v i t...$

- **Naive**：CHTs 与低秩分支简单求和，无任何对齐机制。
- **Act**：仅在低秩分支中引入 SiLU 激活调整（$L^{(l)} = B^{(l)} \sigma(A^{(l)} x)$），无对齐损失。
- **Act+Align**：同时使用 SiLU 激活调整和层对齐损失 $\mathcal{L}_{\mathrm{align}}^{(l)} = \frac{1}{BN} \|S^{(l)} - L^{(l)}\|_F$，总损失为 $\mathcal{L} = \mathcal{L}_{\mathrm{task}} + \lambda \mathcal{L}_{\mathrm{align}}$。

**Act+Align 在所有 12 组实验配置上均取得最低困惑度**。以 LLaMA-60M 在 OpenWebText 上 $s_{\mathrm{total}}=0.9$ 为例，Naive 为 34.25，Act 降至 32.49，Act+Align 进一步降至 31.77。Wilcoxon 符号秩检验显示，Act+Align 对 Naive 和 Act 的改进均具有统计显著性（$p=0.00049$），置信度极高。

Figure 2 从机制层面解释了这一改进：引入对齐损失后，注意力 Q 和 K 层的 OCR 随训练步数显著下降，表明抵消效应得到有效缓解。这直接验证了对齐损失的核心作用——不是简单的正则化，而是通过显式惩罚分支输出差异来促进方向一致。

### 主流对比：CHTsL 超越现有稀疏训练方法

Table 2 在相同总参数预算约束下，将 CHTsL 与稠密训练、纯连通性稀疏方法（SET、RigL、MEST、CHTs）、纯谱稀疏方法（CoLA）以及混合稀疏方法（SLTrain）进行全面对比。关键结果：

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/004_Table_2.jpg]]
*Table 2: Validation perplexity of different methods. Validation perplexity (PPL↓) is reported in this table for different methods on different datasets under the same constraint of total sparsity stotal. Bold values are the best performance out of all sparse methods*

- **LLaMA-60M, OpenWebText, $s_{\mathrm{total}}=0.9$**：CHTsL 取得 31.77 PPL，比最优基线 SLTrain（33.90）降低 2.13，比纯动态稀疏 CHTs（35.20）降低 3.43。
- **LLaMA-130M, C4, $s_{\mathrm{total}}=0.7$**：CHTsL 取得 26.19 PPL，优于 SLTrain（26.78）和 CHTs（27.11）。
- **LLaMA-350M, OpenWebText, $s_{\mathrm{total}}=0.9$**（Table 9）：CHTsL 取得 18.40 PPL，优于 SLTrain（18.99）。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/017_Table_9.jpg]]
*Table 9: Validation perplexity of different methods on LLaMA-350M. Validation perplexity (PPL↓) is reported in this table for different methods on different datasets under the same constraint of total sparsity s _ { t o t a l } . Bold values are the best performance out of all sparse methods*

值得注意的是，SLTrain 本身已是静态稀疏与低秩的组合方法，CHTsL 相对于它的优势表明**动态连通性稀疏与对齐增强机制的协同作用**超越了静态组合方案。

### 消融实验：关键设计选择的因果贡献

**1. 对齐损失的层粒度选择（Table 7）**

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/015_Table_7.jpg]]
*Table 7: Validation perplexity of models based on alignment to different components. Align qk refers to CHTsL with alignment only to Q, K layers, while Align all refers to the original CHTsL with alignment to all linear layers. Validation perplexity (PPL↓) is reported in this table for different methods on different datasets under the same constraint of total sparsity s _ { t o t a l } . Bold values are the best performance*

实验对比了仅对注意力 Q、K 层施加对齐损失（Align qk）与对所有线性层施加对齐损失（Align all）的效果。结果表明，**仅对齐 Q、K 层即可取得与全层对齐相当甚至更优的困惑度**，且显著优于仅对齐其他层（如 V、O 层，胜率 0.42 vs 0.08）。这验证了抵消效应主要集中在 Q、K 投影矩阵的观察，也为实际部署提供了更轻量的对齐方案。

**2. 低秩分支激活函数选择（Table 10）**

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/018_Table_10.jpg]]
*Table 10: Validation perplexity of CHTsL based on different activation function. SiLU is the default one used in the main text. Validation perplexity (PPL↓) is reported in this table for different methods on different datasets under the same constraint of total sparsity s _ { t o t a l } . Bold values are the best performance*

对比 SiLU、ReLU、GeLU 三种激活函数，SiLU 在多数配置下取得最优困惑度。这验证了 SiLU 的平滑非单调特性对稳定低秩训练的重要性——ReLU 的硬截断可能破坏低秩表示的信息传递。

**3. 对齐方案的通用性（Table 13）**

将 Act+Align 方案应用于不同的连通性稀疏方法（静态稀疏、SET、CHTs）及不同初始化策略（随机、BRF），在所有组合下 Act+Align 均一致降低困惑度。这表明对齐增强框架是独立于具体稀疏算法的通用集成策略。

### 失败模式：极端配置下的性能崩溃

Figure 3 展示了 $s_{\mathrm{total}}=0.7$ 时不同稀疏配置 $(s, r)$ 下的敏感性分析。当连通性稀疏分支的稀疏度 $s$ 超过 0.9（即低秩分支占据绝大多数参数预算）时，模型在 OpenWebText 上的性能出现崩溃（PPL 急剧上升，图中红色异常点）。论文分析认为，这是因为 OpenWebText 相对简单，过度依赖低秩分支导致模型表达能力不足。相比之下，在更复杂的 C4 数据集上，较高的低秩参数占比反而有益。

这一发现具有实践指导意义：**组合稀疏方法的总稀疏度分配需要根据数据复杂度进行调优**，不能简单套用固定比例。

### 推理效率的实际限制

Table 12 报告了不同方法的推理内存和吞吐量。尽管 CHTsL 在参数效率上优势显著，但由于当前软件框架和 GPU 硬件对非结构化稀疏操作的支持有限，其理论推理加速未能完全实现，实际吞吐量受限于算子效率。这是方法从研究走向部署需要解决的关键工程瓶颈。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/020_Table_12.jpg]]
*Table 12: Inference memory and throughput of different methods. For each model, inference was conducted for 5000 steps, with maximum memory and average throughput reported. Experiments are conducted on 1 x NVIDIA A100-80GB, with dummy input of batch size 128 and sequence length 256*

### 补充图表

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/006_Table_3.jpg]]
*Table 3: Common hyperparameter settings for experiments on LLaMA-60M and LLaMA-130M. The settings align with previous research*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/007_Table_4.jpg]]
*Table 4: The best sparsity-configuration for SLTrain under different total sparsity. s _ { t o t a l } refers to total sparsity, s refers to sparsity in the connectivity sparse branch, r refers to the rank in lowrank branch. The last column reports the proportion of parameters in connectivity sparse branch compared with spectral sparse (low-rank) branch*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/008_Table_5.jpg]]
*Table 5: The best sparsity-configuration for CHTsL under different total sparsity. s _ { t o t a l } refers to total sparsity, s refers to sparsity in the connectivity sparse branch, r refers to the rank in lowrank branch. The last column reports the proportion of parameters in connectivity sparse branch compared with spectral sparse (low-rank) branch*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/011_Table_6.jpg]]
*Table 6: Comparison between different integration strategies for ”Static + Low-rank” Combination. The table consists of two parts: a. The performance of different integration strategies, reported in terms of validation perplexity (PPL↓). The Naive strategy corresponds to a simple sum of static sparse and low-rank factorization. The Act strategy applies activation adjustment to the low-rank factorization branch. The Act+Align strategy combines activation adjustment with the alignment loss. The coefficient of the alignment loss λ is 0.3. The sparsity configuration is set such that the sparse branch and the low-rank branch have the same number of trainable parameters $\begin{array} { r } { \frac { { d _...$

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/016_Table_8.jpg]]
*Table 8: Common hyperparameter settings for experiments on LLaMA-350M and LLaMA-1B. The settings align with previous research*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_jZplmg7Ad9/figures/019_Table_11.jpg]]
*Table 11: Zero-shot results on downstream tasks. CHTsL, SLTrain, and CHTs are evaluated under a total sparsity of 0.9. Results are reported in terms of accuracy (Acc), with the best-performing value in each row highlighted in bold. Note that if two or more methods achieve the same accuracy, all corresponding values are bolded and counted toward the win rate*

## 方法谱系与知识库定位

### 1. 方法定位与核心贡献

CHTsL 的核心贡献在于首次系统揭示并解决了动态连通性稀疏训练与谱稀疏（低秩）训练在简单集成时产生的**抵消效应**（cancellation effect），并提出了对齐增强的集成框架。该工作的独特定位是：**不引入新的稀疏训练算法本身，而是在现有稀疏训练分支之上构建协作机制**。具体而言，CHTsL 以动态稀疏训练方法 **CHTs**（Zhang et al., 2025）作为连通性稀疏分支，以标准的低秩分解作为谱稀疏分支，通过两个关键改造——低秩分支的激活调整（SiLU）和分支间的对齐损失——实现二者的协同学习。

与现有工作的关键区别在于：
- 相对于纯动态稀疏训练方法（**SET** Mocanu et al., 2018; **RigL** Evci et al., 2020; **MEST** Yuan et al., 2021），CHTsL 融合了谱稀疏分支，在同等参数预算下提升了表示容量。
- 相对于纯低秩训练方法（**CoLA** Liu et al., 2025），CHTsL 保留了连通性稀疏分支对细粒度连接模式的探索能力。
- 相对于已有的混合稀疏-低秩方法 **SLTrain**（Han et al., 2024），CHTsL 的关键差异在于：SLTrain 采用静态稀疏与低秩的简单求和，而 CHTsL 引入了对齐损失和激活调整，显式解决了分支间的冲突信号问题。实验证据（Table 2）表明，这一差异在极端稀疏度下（如 90% 总稀疏度）尤为显著——CHTsL 在 LLaMA-60M 上较 SLTrain 降低了 2.13 的验证困惑度。

### 2. 方法谱系中的位置

从技术路线看，CHTsL 属于**多分支稀疏集成训练**这一新兴方向。该方向的核心挑战在于：不同稀疏范式产生的输出信号可能存在方向性冲突，简单求和会导致信号抵消。CHTsL 的解决方案——通过 Frobenius 范数对齐损失强制两分支输出方向一致——为这一问题提供了可量化的分析工具（OCR 指标）和有效的干预手段。

在方法组件的谱系上，CHTsL 的连通性稀疏分支继承了 CHTs 的动态生长-剪枝机制，低秩分支继承了标准矩阵分解的谱稀疏思想，对齐损失则借鉴了知识蒸馏中输出对齐的思路，但将其应用于同一模型内不同分支之间的协作，而非师生模型之间。

### 3. 适用边界与关键约束

根据实验证据，CHTsL 的适用边界如下：

**有效范围**：
- 在 LLaMA-60M 至 LLaMA-350M 参数规模上验证有效，总稀疏度覆盖 0.7 至 0.9。
- 在 OpenWebText 和 C4 两个数据集上均表现一致，但对不同数据集的最优稀疏配置存在差异：C4 上低秩分支可承担更高参数占比，而 OpenWebText 上低秩分支占比过高会导致性能崩溃（Figure 3）。
- 对齐损失加权系数 λ 的最佳取值与数据集和模型规模相关：LLaMA-60M 在 OpenWebText 上为 0.5，在 C4 上为 0.3。

**已知局限**：
1. **推理加速未实现**：由于当前软件框架和 GPU 硬件对非结构化稀疏操作的支持有限，CHTsL 的理论推理加速未能完全转化为实际吞吐量提升。这是一个工程层面的瓶颈，而非方法本身的缺陷。
2. **极端配置下的脆弱性**：在总稀疏度 0.9 以上且低秩分支参数占比过高的配置下，模型性能可能崩溃，尤其在相对简单的数据集 OpenWebText 上。Figure 3 的敏感性分析中，当连通性稀疏分支的稀疏度超过 0.9 时，部分配置的验证困惑度出现异常飙升（以红色标注）。
3. **规模验证有限**：实验主要在 60M 至 350M 参数的 LLaMA 模型上进行，尚未在更大规模（如 7B+）及更多样架构上验证。

### 4. 消融发现的关键洞察

消融实验揭示了几个对后续研究具有指导意义的发现：

- **对齐损失对注意力 Q、K 层特别关键**：Table 7 显示，仅对 Q、K 投影层施加对齐损失即可取得与全层对齐相当甚至更优的困惑度，而仅对齐其他层（V、O 及 FFN）的性能显著较差（胜率 0.42 vs 0.08）。这表明抵消效应在注意力机制的查询-键交互中尤为严重，是未来优化可以聚焦的瓶颈。
- **激活调整的作用独立于对齐损失**：Table 1 显示，仅添加 SiLU 激活（Act 策略）已在多数配置下优于朴素求和，但与 Act+Align 的完整方案之间仍存在统计显著的差距（Wilcoxon p=0.00049），说明激活调整和对齐损失是两个互补的改进维度。
- **方案具有通用性**：Table 13 表明，对齐增强方案在与不同连通性稀疏方法（静态稀疏、SET、CHTs）及不同初始化策略结合时均能一致降低困惑度，说明该框架不依赖于特定的动态稀疏算法。

### 5. 开放问题与未来方向

基于论文的分析和已知局限，以下问题值得后续探索：

1. **硬件-算法协同设计**：能否设计专门的 GPU 内核或编译器优化，充分释放 CHTsL 中非结构化稀疏与低秩计算的推理潜力？这是将理论加速转化为实际加速的关键工程挑战。
2. **缩放特性验证**：在更大规模（>1B）和生成式任务上，CHTsL 的缩放特性及零样本/少样本能力是否依然保持优势？当前在 350M 规模上的验证（Table 9）虽显示趋势一致，但尚不足以推断大规模行为。
3. **与其他压缩技术的结合**：该对齐增强框架能否与结构化稀疏、量化、或现代混合精度训练有效结合，进一步降低端到端资源消耗？对齐损失的形式是否可推广到其他多分支压缩场景？
4. **对齐损失的理论分析**：当前对齐损失的设计基于经验观察，缺乏对损失函数形式（如 Frobenius 范数 vs 余弦相似度）与训练动力学之间关系的理论刻画，这一方向值得深入。

## 原文 PDF

![[paperPDFs/ICLR_2026/Alignment_Enhanced_Integration_of_Connectivity_and_Spectral_Sparsity_in_Dynamic_Sparse_Training_of_LLM.pdf]]
