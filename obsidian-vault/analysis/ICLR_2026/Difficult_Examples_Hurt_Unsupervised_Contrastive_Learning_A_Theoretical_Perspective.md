---
title: "Difficult Examples Hurt Unsupervised Contrastive Learning: A Theoretical Perspective"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Difficult_Examples_Hurt_Unsupervised_Contrastive_Learning_A_Theoretical_Perspective.pdf
openreview_forum_id: 5LMdnUdAoy
aliases:
- DACLFSRMTTSC
- DEHUCLTP
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "困难样本对的相似度权重（可通过直接移除、边际调整和温度缩放进行控制）。"
primary_logic: "通过相似图建模发现，困难样本的存在导致更差的线性探测误差界；移除困难样本、增加边际或缩放温度可以缩小误差界，从而提升性能。"
claims:
- "排除困难样本后，下游分类准确率提升。"
- "混合图像实验：增加困难样本降低性能，移除它们则提升性能。"
- "理论证明困难样本的存在导致更差的线性探测误差界。"
- "直接移除困难样本改善了误差界。"
---

# Difficult Examples Hurt Unsupervised Contrastive Learning: A Theoretical Perspective

> [!tip] 核心洞察
> 通过相似图建模发现，困难样本的存在导致更差的线性探测误差界；移除困难样本、增加边际或缩放温度可以缩小误差界，从而提升性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 困难样本损害无监督对比学习：理论视角 |
| 英文题名 | Difficult Examples Hurt Unsupervised Contrastive Learning: A Theoretical Perspective |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=5LMdnUdAoy) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Difficulty-aware Contrastive Learning Framework (Sample Removal, Margin Tuning, Temperature Scaling, and Combined) |
| Dataset | CIFAR-10, CIFAR-100, STL-10, TinyImagenet |

> [!tip] 效果简介
> - CIFAR-10 上，Accuracy (%) 为 89.03 (SimCLR Removing)，对比 88.26 (SimCLR Baseline)，变化 +0.77。
> - CIFAR-100 上，Accuracy (%) 为 60.31 (SimCLR Removing)，对比 59.95 (SimCLR Baseline)，变化 +0.36。
> - STL-10 上，Accuracy (%) 为 76.10 (SimCLR Removing)，对比 75.98 (SimCLR Baseline)，变化 +0.12。

## 概述

无监督对比学习中的**困难样本**（不同类别但相似度高的样本对）在预训练时容易被错误聚类，从而损害下游分类的泛化性能。本文从理论层面揭示了这一问题的本质机制，并提出了一个系统性的解决框架。

**核心发现**：通过构建相似图（similarity graph）对样本对相似度进行建模，作者推导了有/无困难样本条件下的线性探测误差界（Theorem 3.4）。理论证明，困难样本的存在会导致更差的误差上界，而直接移除困难样本（Corollary 4.1）、引入边际调整（Theorem 4.3）或温度缩放（Theorem 4.5）均可有效缩小该误差界。

**方法定位**：本文提出的**困难感知对比学习框架**（Difficulty-aware Contrastive Learning Framework）位于对比学习的方法谱系中，以 **SimCLR**（Chen et al., ICML 2020）为主要基线，并可泛化至 **MoCo**（He et al., CVPR 2020）等架构。该方法通过三个关键模块实现：

- **困难样本选择**：基于投影器前特征的余弦相似度百分位数识别困难对（Eq. 12）
- **损失调整**：对选定困难对在 InfoNCE 损失中应用移除、边际调整或温度缩放（Eqs. 13–15）
- **组合策略**：将边际调整与温度缩放整合（Eq. 16），实现协同增效

**主要结果**：在 CIFAR-10/100、STL-10 和 TinyImagenet 四个数据集上，困难样本移除使 SimCLR 基线准确率提升 0.12–1.48 个百分点（Table 1）；组合方法在 TinyImagenet 上达到 80.00%，较基线（69.58%）提升 10.42 个百分点（Table 4）；在长尾数据集 TinyImagenet-LT 上同样取得 4.28 个百分点的显著增益（Table 6）。理论误差界的变化趋势在混合图像实验中得到了实证验证（Table 10）。

**局限性**：理论分析依赖于谱对比损失与 InfoNCE 等价的假设，实验验证主要集中在小规模数据集，困难样本选择需引入额外超参数（posHigh, posLow），在极端噪声场景下效果可能受限。

## 背景与动机

无监督对比学习通过拉近正样本对、推远负样本对来学习表征，已成为自监督学习的核心范式之一。然而，现有方法通常平等对待所有样本对，忽视了样本对之间固有的难度差异。一个关键的现象是：**困难样本对**——即来自不同类别但特征相似度高的样本对——在预训练过程中容易被错误聚类，从而损害下游分类任务的泛化性能。

这一问题的直观表现可见于 Figure 1：在 CIFAR-10、CIFAR-100、STL-10 和 TinyImagenet 四个数据集上，排除困难样本后，线性探测准确率均获得提升。进一步的混合图像实验（Figure 2）提供了因果证据：通过像素级混合人为增加困难样本比例，模型性能下降；而移除这些混合样本后，性能回升至接近甚至优于原始数据集的水平。

从理论层面看，现有对比学习的分析框架（如谱对比损失与矩阵分解的等价性）尚未系统建模困难样本对表征学习的影响机制。这留下了一个核心问题：**困难样本究竟如何损害无监督对比学习，以及能否通过理论指导下的干预来消除这种损害？**

本文正是围绕这一瓶颈展开。作者首先构建了**相似图**理论框架，将样本对间的相似度建模为三个关键参数——同类样本相似度 α、普通不同类样本相似度 β、以及困难样本对不同类相似度 γ。在此基础上，推导出有无困难样本条件下的线性探测误差界，从理论上证明了困难样本的存在会导致更差的误差上界（Theorem 3.4）。这一理论分析为后续的方法设计提供了明确的因果旋钮：通过控制困难样本对的相似度权重，可以直接缩小误差界。具体而言，移除困难样本（Corollary 4.1）、为困难对增加边际（Theorem 4.3）或缩放温度（Theorem 4.5），均能在理论上改善误差界。

综上，本文的动机源于一个明确的因果链条：困难样本对 → 错误聚类 → 误差界扩大 → 下游性能下降。基于这一认知，作者提出了一个完整的困难感知对比学习框架，包含困难样本选择、样本移除、边际调整和温度缩放等模块，旨在从理论和实践两个层面系统解决困难样本的负面影响。

## 核心创新

本工作的核心创新在于**首次从理论层面揭示了困难样本（高相似度的异类样本对）对无监督对比学习的损害机制**，并基于相似图建模提出了一套统一的困难样本感知对比学习框架。该框架包含三个可独立使用亦可组合的“因果旋钮”：困难样本移除、边际调整和温度缩放，其理论有效性均通过线性探测误差界的严格推导得到保证。

### 理论瓶颈与因果旋钮

**真实瓶颈**：无监督对比学习中，困难样本（不同类但相似度高的样本对）在预训练时容易被错误聚类，从而损害下游分类的泛化性能。这一现象在混合图像实验中得到直观验证（Figure 2）：向 CIFAR-10 数据集中混入像素级混合的困难样本后，线性探测准确率下降；移除这些混合样本后，性能恢复并超越原始基线。

**因果旋钮**：困难样本对的相似度权重。通过以下三种方式控制该旋钮，可直接改变对比学习模型的特征空间结构：
- **直接移除**：将困难样本对的相似度置零（Eq. 13）
- **边际调整**：为困难样本对的相似度增加一个正边际 σ（Eq. 14）
- **温度缩放**：对困难样本对使用缩放后的温度 ρτ（Eq. 15）

### 相似图建模与误差界理论

论文构建了一个**相似图理论框架**，将样本对之间的增强相似度参数化为三类（Figure 3）：
- 同类样本相似度：α
- 异类普通样本相似度：β
- 异类困难样本相似度：γ，满足 β < γ < α < 1

基于该建模，论文推导了谱对比损失下的线性探测误差界。核心理论结果包括：

- **无困难样本时的误差界**（Theorem 3.3）：
  $$\mathcal{E}_{\text{w.o.}} \leq \frac{4\delta}{1 - \frac{1-\alpha}{(1-\alpha) + n\alpha + nr\beta}} + 8\delta$$

- **存在困难样本时的误差界**（Theorem 3.4）：
  $$\mathcal{E}_{\text{w.d.}} \leq \frac{4\delta}{1 - \frac{(1-\alpha) + r(\gamma-\beta)}{(1-\alpha) + n\alpha + nr\beta + n_d r(\gamma-\beta)}} + 8\delta$$

由于 γ > β，存在困难样本时误差界的分母更小，导致上界更大，从理论上解释了困难样本损害性能的原因。

- **移除困难样本后的误差界**（Corollary 4.1）：
  $$\mathcal{E}_{\text{R}} \leq \frac{4\delta}{1 - \frac{1-\alpha}{(1-\alpha) + (n-n_d)\alpha + (n-n_d)r\beta}} + 8\delta$$

该界与无困难样本时的误差界形式一致，仅将样本数从 n 替换为 n - n_d，表明移除困难样本可以恢复理想的误差界。

- **边际调整的理论保证**（Theorem 4.3）：当对困难负样本对施加边际 $m_{x,x'} = c_0 / (c_1^2 c_2) \cdot (\gamma - \beta)$ 时，可消除困难样本的负面影响，使误差界回到无困难样本的水平。

- **温度缩放的理论保证**（Theorem 4.5）：通过对困难样本对施加缩放温度，同样可以消除其负面影响。

### 困难样本选择机制

论文提出了一种**简单高效的困难样本选择机制**（Section 5.1），无需标签信息即可在线识别困难样本对。具体而言，在训练批次内计算所有样本对的余弦相似度，按降序排列后，定义两个百分位数阈值 `posHigh` 和 `posLow`：
- 相似度高于 `Sim_posHigh` 的对被视为同类样本
- 相似度介于 `Sim_posLow` 和 `Sim_posHigh` 之间的对被视为困难样本对

选择指示函数为：
$$p_{i,j} := \mathbf{1}_{[Sim_{posLow} \leq s_{ij} < Sim_{posHigh}]}$$

实验表明，训练过程中该区间内来自不同类的样本对比例**趋近于 100%**（Figure 4(c)），验证了选择机制的有效性。此外，该机制对 `posHigh` 和 `posLow` 的具体取值不敏感（Figure 4(a) 和 4(b)），且使用投影器前的特征进行选择优于投影器后的特征（Table 7）。

### 与基线的关键差异

| 维度 | SimCLR 基线 | 本工作 |
|------|-----------|--------|
| 困难样本处理 | 所有样本平等使用 | 显式识别并针对性处理 |
| 成对相似度边际 | 0 | σ（如 0.1） |
| 成对相似度温度 | τ（基础温度） | ρτ（如 ρ=0.7，仅对困难对） |
| 困难对识别 | 无 | 基于余弦相似度百分位数 |

### 组合方法与跨框架泛化

将边际调整和温度缩放与选择机制整合的组合损失（Eq. 16）在多个数据集上取得一致且显著的提升：TinyImagenet 上较 SimCLR 基线提升 +10.42%（Table 4），在长尾数据集 TinyImagenet-LT 上提升 +4.28%（Table 6）。该方法不仅适用于 SimCLR，也可无缝集成到 MoCo 框架中（Table 5），展现出良好的跨架构泛化性。

## 整体框架

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/006_Figure_3.jpg]]
*Figure 3: Modeling of difficult examples. The similarity between same-class samples is α (a), the similarity between different-class difficult samples is $\gamma \left( \mathrm { c } \right$) , and the similarity between other samples is $\beta \left( \mathbf { b } \right$) . The adjacency matrix of a 4-sample subset is shown in (d)

本文提出的困难感知对比学习框架围绕一个核心因果机制展开：**无监督对比学习中，不同类但相似度高的困难样本对在预训练时被错误聚类，从而损害下游分类的泛化性能**。为抑制这一负面影响，框架设计了三个可插拔的损失调整模块，并与一个轻量级的困难样本选择模块协同工作。

### 框架总览

整个 pipeline 以标准的无监督对比学习流程（如 **SimCLR**（Chen et al., ICML 2020）或 **MoCo**（He et al., CVPR 2020））为基础，在 InfoNCE 损失计算前插入两个关键阶段：

1. **困难样本选择模块**：在每批次内，利用投影器之前的特征计算所有样本对的余弦相似度，通过百分位数阈值识别困难对。
2. **损失调整模块**：对识别出的困难对，采用三种策略之一调整其损失贡献——直接移除（相似度置零）、边际调整（增加边际 σ）或温度缩放（使用缩放温度 ρτ）。

三个模块可独立使用，也可组合使用（边际调整与温度缩放叠加），形成统一的困难感知对比学习框架。

### 模块关系与数据流

```
输入批次 (2N 个增强视图)
        │
        ▼
┌─────────────────────────────┐
│  特征提取 (编码器 f + 投影器 g)  │
│  计算投影前特征 f(x) 的余弦相似度  │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  困难样本选择模块 (Section 5.1)  │
│  • 按相似度降序排序              │
│  • 百分位数阈值: posHigh, posLow │
│  • 输出选择矩阵 P:              │
│    p_{i,j}=1 若 s_{ij}∈[Sim_posLow,│
│                    Sim_posHigh) │
│    p_{i,j}=0 其他               │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  损失调整模块 (Sections 5.2-5.5) │
│                              │
│  ① 移除 (Eq.13):             │
│     相似度 s_{ij}×(1-p_{i,j}) │
│                              │
│  ② 边际调整 (Eq.14):          │
│     相似度 s_{ij}+p_{i,j}·σ  │
│                              │
│  ③ 温度缩放 (Eq.15):          │
│     温度 τ→[p_{i,j}·ρ+(1-p_{i,j})]τ│
│                              │
│  ④ 组合 (Eq.16):              │
│     边际+温度联合调整          │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│  InfoNCE 损失计算             │
│  下游线性探测评估              │
└─────────────────────────────┘
```

### 困难样本选择模块

该模块的核心操作是计算批次内所有样本对在**投影器之前特征** $f(x)$ 上的余弦相似度 $s_{ij}$，并按降序排列。引入两个百分位数超参数：

- **posHigh**：高相似度阈值，相似度高于此值的样本对被视为同类对，不参与困难样本处理。
- **posLow**：低相似度阈值，相似度低于此值的样本对被视为简单的不同类对，同样不参与处理。

落在区间 $[Sim_{posLow}, Sim_{posHigh})$ 内的样本对被标记为困难对，其选择指示函数为：

$$p_{i,j} := \mathbf{1}_{[Sim_{posLow} \leq s_{ij} < Sim_{posHigh}]}$$

消融实验（Table 7）表明，使用投影器前特征进行选择优于投影器后特征；Figure 4(c) 显示，训练过程中该区间内来自不同类的样本对比例趋近 100%，验证了选择机制的有效性。

### 损失调整模块

三种调整策略共享同一个选择矩阵 $P$，但在损失函数中施加不同的干预：

- **样本移除**（Section 5.2, Eq.13）：将困难对的相似度乘以 $(1-p_{i,j})$，本质上是将其相似度置零，阻止它们参与梯度更新。这是最直接的干预方式，在 TinyImagenet 上带来 +1.48% 的提升（Table 1）。

- **边际调整**（Section 5.3, Eq.14）：为困难对的相似度增加一个正边际 $\sigma$（如 0.1），使它们在损失中被“推远”。理论分析（Theorem 4.3）证明，适当选择的边际可以消除困难样本的负面影响。在 TinyImagenet 上，边际调整结合选择机制带来 +9.56% 的显著提升（Table 2）。

- **温度缩放**（Section 5.4, Eq.15）：对困难对使用缩放温度 $\rho\tau$（$\rho<1$，如 0.7），降低其 softmax 分布的尖锐度，从而减弱其在对比损失中的权重。理论分析（Theorem 4.5）表明，这等价于对相似图进行元素级加权矩阵分解。消融实验（Table 9）证实 $\rho=0.7$ 的针对性缩放优于极大温度（等同于丢弃困难样本）和基础温度。

- **组合方法**（Section 5.5, Eq.16）：将边际调整和温度缩放叠加，在 TinyImagenet 上达到 80.00% 的最高准确率，较 SimCLR 基线提升 +10.42%（Table 4）。

### 理论支撑

整个框架的理论基础建立在**相似图建模**（Section 3）之上。论文将样本对相似度抽象为三个参数：同类相似度 $\alpha$、简单不同类相似度 $\beta$、困难不同类相似度 $\gamma$（$\beta < \gamma < \alpha < 1$）。通过谱对比损失与矩阵分解的等价性，推导出有无困难样本时的线性探测误差界（Theorem 3.3 和 3.4），并证明三种干预策略均可缩小误差界（Corollary 4.1, Theorems 4.3, 4.5）。混合图像实验（Table 10）进一步验证了 $\alpha$、$\beta$、$\gamma$ 及特征值随混合比例的变化趋势与理论预测一致。

> **注意**：理论分析依赖于谱对比损失与 InfoNCE 等价的假设，以及标签可从增强中恢复的假设。实验验证主要在小规模数据集上进行，大规模场景下的效果尚需更多证据。

## 核心模块与公式推导

### 3.1 理论建模：相似图与误差界

论文首先构建了一个**相似图（Similarity Graph）**理论框架，用以刻画不同样本对之间的相似性关系。该框架将样本对的增强相似度归纳为三类参数：

- **α**：同类样本间的相似度（Figure 3(a)）
- **β**：不同类“简单”样本间的相似度（Figure 3(b)）
- **γ**：不同类“困难”样本间的相似度，满足 β < γ < α < 1（Figure 3(c)）

基于此建模，论文采用谱对比损失（Spectral Contrastive Loss）作为 InfoNCE 损失的代理进行理论分析：

$$
\mathcal { L } _ { \operatorname { S p e c } } ( f ) : = - 2 \cdot \mathbb { E } _ { x , x ^ { + } } \big [ f ( x ) ^ { \top } f ( x ^ { + } ) \big ] + \mathbb { E } _ { x , x ^ { \prime } } \Big [ \big ( f ( x ) ^ { \top } f ( x ^ { \prime } ) \big ) ^ { 2 } \Big ]
$$

该损失等价于矩阵分解损失，仅相差一个常数：

$$
\mathcal { L } _ { \mathrm { m f } } ( F ) : = \| \bar { \pmb { A } } - F \boldsymbol { F } ^ { \top } \| _ { F } ^ { 2 } = \mathcal { L } _ { \mathrm { S p e c } } ( f ) + c o n s t .
$$

其中 $\bar{\pmb{A}}$ 为归一化邻接矩阵，$F$ 为样本表征矩阵。

**核心理论结果**：在标签可恢复性假设下，推导出两种场景的线性探测误差界。

- **无困难样本**时（Theorem 3.3）：

$$
\mathcal { E } _ { \mathrm { w . o . } } \leq \frac { 4 \delta } { 1 - \frac { 1 - \alpha } { ( 1 - \alpha ) + n \alpha + n r \beta } } + 8 \delta .
$$

- **存在困难样本**时（Theorem 3.4），每类有 $n_d$ 个困难样本，误差界变为：

$$
\mathcal { E } _ { \mathrm { w . d . } } \leq \frac { 4 \delta } { 1 - \frac { ( 1 - \alpha ) + r ( \gamma - \beta ) } { ( 1 - \alpha ) + n \alpha + n r \beta + n _ { d } r ( \gamma - \beta ) } } + 8 \delta .
$$

**因果机制**：比较两式可知，困难样本通过引入 $\gamma - \beta > 0$ 项，增大了误差界的分母偏移量，导致更差的线性探测性能。当 $\gamma$ 显著大于 $\beta$ 或 $n_d$ 较大时，负面影响尤为严重。这一理论结论在所有数据集上得到统计验证：$\gamma$ 显著大于 $\beta$（t 检验 p 值接近零，Table 11）。

### 3.2 缓解策略的理论基础

基于上述误差界分析，论文从理论上证明了三种缓解策略的有效性。

**策略一：直接移除困难样本**（Corollary 4.1）。移除所有困难样本后，误差界恢复为无困难样本形式，仅将样本量从 $n$ 替换为 $n - n_d$：

$$
\mathcal { E } _ { \mathrm { R } } \leq \frac { 4 \delta } { 1 - \frac { 1 - \alpha } { ( 1 - \alpha ) + ( n - n _ { d } ) \alpha + ( n - n _ { d } ) r \beta } } + 8 \delta .
$$

**策略二：边际调整（Margin Tuning）**（Theorems 4.2, 4.3）。在损失函数中对困难样本对的相似度增加边际 $\sigma$，等价于从归一化相似矩阵中减去归一化边际矩阵：

$$
\mathcal { L } _ { \operatorname* { m f } - \mathrm { M } } ( F ) : = \| ( \bar { A } - \bar { M } ) - F F ^ { \top } \| _ { F } ^ { 2 }
$$

当边际值取 $m_{x,x'} = c_0 / (c_1^2 c_2) \cdot (\gamma - \beta)$ 时，可消除困难样本的负面影响。

**策略三：温度缩放（Temperature Scaling）**（Theorems 4.4, 4.5）。对困难样本对使用缩放温度 $\rho\tau$，等价于元素级温度缩放的加权矩阵分解：

$$
\mathcal L _ { \operatorname* { m f } - \mathrm { T } } ( F ) : = \| \pmb { T } \odot \bar { \pmb { A } } - F \boldsymbol { F } ^ { \top } \| _ { w F } ^ { 2 }
$$

适当选择 $\rho$ 可降低困难样本在损失中的权重，从而缩小误差界。

### 3.3 实践模块：困难样本选择与损失调整

为实现上述理论策略，论文设计了三个核心实践模块。

**模块一：困难样本选择（Section 5.1）**

基于投影器前特征 $f(x)$ 的余弦相似度进行百分位数筛选。定义 $Sim_{posHigh}$ 和 $Sim_{posLow}$ 为降序排列后相似度的两个百分位阈值，困难对指示函数为：

$$
p _ { i , j } : = \mathbf { 1 } _ { [ S i m _ { p o s L o w } \leq s _ { i j } < S i m _ { p o s H i g h } ] }
$$

其中 $s_{ij}$ 为样本 $i$ 与 $j$ 的余弦相似度。该选择机制的合理性在于：训练过程中，落入该区间的样本对几乎完全来自不同类（Figure 4(c)），且对端点参数 $posHigh$、$posLow$ 不敏感（Figure 4(a)(b)）。消融实验表明，使用投影器前特征选择优于投影器后特征（Table 7）。

**模块二：损失调整（Sections 5.2–5.4）**

将选择矩阵 $P$ 集成到 InfoNCE 损失中，实现三种调整方式：

- **移除（Removing）**：将困难对的相似度置零（Eq. 13）：

$$
\ell_{\mathrm{R}}(i,j) := -\log \frac{\exp{((s_{i,j}(1-p_{i,j}))/\tau)}}{\sum_{k=1}^{2N} \mathbf{1}_{[k\neq i]} \exp{((s_{i,k}(1-p_{i,k}))/\tau)}}
$$

- **边际调整（Margin Tuning）**：为困难对增加边际 $\sigma$（Eq. 14）：

$$
\ell_{\mathrm{M}}(i,j) := -\log \frac{\exp\left(\left(s_{i,j}+p_{i,j}\sigma\right)/\tau\right)}{\sum_{k=1}^{2N} \mathbf{1}_{[k\neq i]} \exp\left(\left(s_{i,k}+p_{i,k}\sigma\right)/\tau\right)}
$$

- **温度缩放（Temperature Scaling）**：对困难对使用缩放温度 $\rho\tau$（Eq. 15）：

$$
\ell_{\mathrm{T}}(i,j) := -\log \frac{\exp\big(\frac{s_{i,j}}{[p_{i,j}\rho+(1-p_{i,j})]\tau}\big)}{\sum_{k=1}^{2N} \mathbf{1}_{[k\neq i]} \exp\big(\frac{s_{i,k}}{[p_{i,k}\rho+(1-p_{i,k})]\tau}\big)}
$$

**模块三：组合方法（Section 5.5）**

将边际调整与温度缩放结合，形成统一的损失函数（Eq. 16）：

$$
\ell(i,j) := -\log \frac{\exp\big(\frac{s_{i,j}+p_{i,j}\sigma}{[p_{i,j}\rho+(1-p_{i,j})]\tau}\big)}{\sum_{k=1}^{2N} \mathbf{1}_{[k\neq i]} \exp\big(\frac{s_{i,k}+p_{i,k}\sigma}{[p_{i,k}\rho+(1-p_{i,k})]\tau}\big)}
$$

**超参数设置**：边际因子 $\sigma = 0.1$ 在 CIFAR-100 上取得最佳性能（Figure 5(a)）；温度缩放因子 $\rho = 0.7$ 在 CIFAR-100 上取得最佳性能（Figure 5(b)），且显著优于极大温度（等同于丢弃困难样本）和基础温度（Table 9）。

## 实验与分析

### 核心发现：困难样本的系统性损害与修复

本文通过受控实验和消融研究，系统验证了“困难样本损害无监督对比学习”的核心主张，并量化了三种干预策略的效果。实验覆盖 CIFAR-10、CIFAR-100、STL-10、TinyImagenet 四个标准数据集，所有比较均使用相同的数据增强、优化器（SGD）、批量大小和线性评估协议，确保公平性。

**直接移除困难样本的基线提升。** 在 SimCLR 框架下，仅通过困难样本选择机制将识别出的困难对相似度置零（Eq. 13），即可在所有数据集上获得一致的准确率增益：CIFAR-10 上从 88.26% 提升至 89.03%（+0.77%），CIFAR-100 上从 59.95% 提升至 60.31%（+0.36%），STL-10 上从 75.98% 提升至 76.10%（+0.12%），TinyImagenet 上从 69.58% 提升至 71.06%（+1.48%）（Table 1）。TinyImagenet 上的增益尤为显著，暗示该数据集中困难样本的密度或强度更高。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/010_Table_1.jpg]]
*Table 1: Classification accuracy with or without removing difficult examples on CIFAR-10, CIFAR-100, STL-10 and TinyImagenet dataset using SimCLR. Results are averaged over three runs*

**边际调整与温度缩放的独立效果。** 两种基于理论的干预策略——边际调整（MT）和温度缩放（TS）——在选择性应用于困难对时，均显著优于对所有样本统一处理的朴素版本。以 TinyImagenet 为例，MT（Selected）达到 79.14%，较基线 69.58% 提升 9.56 个百分点（Table 2）；TS（Selected）达到 78.52%，提升 8.94 个百分点（Table 3）。这表明**精准定位困难对是干预有效性的前提**，盲目对所有样本施加边际或温度调整反而可能引入噪声。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/011_Table_2.jpg]]
*Table 2: Classification accuracy with or without margin tuning on CIFAR-10, CIFAR-100, STL-10 and TinyImagenet dataset. Results are averaged over three runs*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/012_Table_3.jpg]]
*Table 3: Classification accuracy with or without temperature scaling on CIFAR-10, CIFAR-100, STL-10 and TinyImagenet dataset. Results are averaged over three runs*

**组合方法的协同效应。** 将边际调整与温度缩放整合（Eq. 16）后，组合方法在 TinyImagenet 上达到 80.00%，较基线提升 10.42 个百分点，且在所有数据集上均优于单独使用任一组分（Table 4）。该协同效应可迁移至其他对比学习框架：在 MoCo 架构上，组合方法将 CIFAR-10 准确率从 85.84% 提升至 86.82%（Table 5）。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/013_Table_4.jpg]]
*Table 4: Classification accuracy with or without combined method on CIFAR-10, CIFAR-100, STL-10 and TinyImagenet dataset. Results are averaged over three runs*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/014_Table_5.jpg]]
*Table 5: The results of incorporating the Combined method with different architectures on CIFAR-10*

### 困难样本选择机制的有效性

**选择区间的鲁棒性。** 困难对识别依赖于余弦相似度的两个百分位数阈值 `posLow` 和 `posHigh`。参数敏感性分析表明，最终准确率对这两个阈值不敏感（Figure 4(a)(b)），说明方法不需要精细调参即可稳定工作。

**选择精度的动态提升。** 训练过程中，落入 `(Sim_posLow, Sim_posHigh)` 区间的样本对中，来自不同类的比例随训练推进迅速趋近 100%（Figure 4(c)）。这意味着选择机制本身在训练中不断自我校准，最终几乎完全捕获跨类困难对，验证了基于投影器前特征的余弦相似度作为困难度代理的有效性。

**特征层级的消融。** 使用投影器前特征 `f(x)` 进行困难样本选择，优于使用投影器后特征 `g(f(x))`：在 CIFAR-10 上准确率分别为 89.68% 和 88.86%，在 CIFAR-100 上分别为 63.89% 和 62.31%（Table 7）。这与理论直觉一致——投影器后的表示已针对对比损失优化，可能模糊了类别边界的困难信号。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/018_Table_7.jpg]]
*Table 7: Classification accuracy by using Combined method on CIFAR-10 and CIFAR-100. Features before projector means that we use f ( x ) for difficult examples selection and features after projector means that we use g ( f ( x ) ) for difficult examples selection*

### 超参数分析与理论一致性验证

**边际因子 σ 的最优值。** 在 CIFAR-100 上，边际调整因子 σ=0.1 取得最佳性能（Figure 5(a)）。过大的 σ 会导致性能下降，表明过度惩罚困难对可能破坏表示学习的语义结构。

**温度缩放因子 ρ 的最优值。** 温度缩放因子 ρ=0.7 在 CIFAR-100 上取得最佳准确率 61.67%（Figure 5(b)）。关键消融显示，将温度因子设为极大值（1e9，等价于丢弃困难样本）仅得到 60.31%，低于针对性缩放（Table 9）。这证明**困难样本并非应被完全丢弃的噪声，而是需要适度降权的有价值信号**。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/021_Table_9.jpg]]
*Table 9: Classification accuracy with various temperature scaling factors on CIFAR-100 datasets. Setting the Temperature Scaling Factor to 0.7 represents using our proposed theoretical framework to specifically address difficult samples, while setting the Temperature Scaling Factor to 1e9 means discarding these difficult samples. Results are averaged over three runs*

**理论误差界的实证验证。** 混合图像实验中，随着混合比例 ω 增加（即引入更多困难样本），相似图参数 α、β、γ 及特征值的变化趋势与理论预测一致（Table 10）。在所有数据集上，γ（困难跨类相似度）显著大于 β（普通跨类相似度），t 检验 p 值接近零（Table 11），直接验证了理论建模中 γ > β 的核心假设。

### 长尾分布与大规模数据的泛化

**长尾场景。** 在 TinyImagenet-LT 长尾数据集上，组合方法将 SimCLR 基线从 43.34% 提升至 47.62%（+4.28%）（Table 6），表明困难样本处理对尾部类别的表示学习具有额外价值——长尾分布中尾部类别样本天然更容易成为其他类别的“困难样本”。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/015_Table_6.jpg]]
*Table 6: Classification accuracy by using Combined method on TinyImagenet-LT. We also use SimCLR as the baseline method*

**ImageNet-1k 验证。** 组合方法在 ImageNet-1k 上同样有效（Table 8），但需注意该实验的详细配置和增益幅度在提供的片段中未完整呈现，建议手动核实原文以确认大规模场景下的具体提升幅度。

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/020_Table_8.jpg]]
*Table 8: Classification accuracy on Imagenet-1k*

### 失败模式与局限性

1. **理论等价性假设的限制。** 理论推导依赖于谱对比损失与 InfoNCE 等价的假设，以及标签可从增强中恢复的假设。当这些假设在实际数据上不严格成立时，误差界的紧致性可能下降。

2. **额外计算开销。** 困难样本选择需要计算批次内所有样本对的余弦相似度，计算复杂度为 O(B²)，在大批量场景下可能成为瓶颈。

3. **极端噪声场景。** 在困难样本比例极高或类别边界完全模糊的场景下，选择机制的精度可能退化，方法的有效性尚需进一步检验。

4. **超参数自适应。** 虽然 `posLow` 和 `posHigh` 在测试范围内表现鲁棒，但在更大规模数据和不同任务分布下的自适应性仍需探索。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/001_Figure_1.jpg]]
*Figure 1: Excluding difficult examples improves unsupervised contrastive learning*

![[assets/figures/papers/paper_list_l39_https_openreview_net_forum_id_5LMdnUdAoy/figures/002_Figure_1.jpg]]
*Figure 1: (mixed) difficult examples improves performance*

## 方法谱系与知识库定位

### 理论基座：谱对比损失与矩阵分解的等价性

本工作的理论分析建立在谱对比损失（Spectral Contrastive Loss）之上，该损失由 HaoChen et al.（2021）提出，被证明是广泛使用的 InfoNCE 损失的一个有效性能代理。谱对比损失定义为：

$$\mathcal { L } _ { \operatorname { S p e c } } ( f ) : = - 2 \cdot \mathbb { E } _ { x , x ^ { + } } \big [ f ( x ) ^ { \top } f ( x ^ { + } ) \big ] + \mathbb { E } _ { x , x ^ { \prime } } \Big [ \big ( f ( x ) ^ { \top } f ( x ^ { \prime } ) \big ) ^ { 2 } \Big ]$$

其核心等价性在于，该损失与矩阵分解损失仅相差一个常数：

$$\mathcal { L } _ { \mathrm { m f } } ( F ) : = \| \bar { \pmb { A } } - F \boldsymbol { F } ^ { \top } \| _ { F } ^ { 2 } = \mathcal { L } _ { \mathrm { S p e c } } ( f ) + c o n s t .$$

这一等价关系使得作者能够将对比学习的表征学习问题转化为对归一化相似矩阵 $\bar{A}$ 的矩阵分解问题，从而在相似图框架下进行严格的误差界推导。论文进一步沿用了 HaoChen et al.（2021）的标签可恢复性假设（label recoverability，以标注误差 $\delta$ 刻画）和可实现性假设（realizability），为线性探测误差界的推导提供了公理化基础。

### 与基线方法的差异化定位

论文以 **SimCLR**（Chen et al., ICML 2020）为主要实验基线，同时以 **MoCo**（He et al., CVPR 2020）作为替代框架进行泛化性检验。与这两类方法的根本区别在于对训练样本的“难度意识”：

- **SimCLR 和 MoCo 的默认设定**：所有样本对在 InfoNCE 损失中被平等对待，成对相似度边际为 $0$，温度统一为基础温度 $\tau$，不存在显式的困难样本识别机制。
- **本工作提出的 Difficulty-aware 框架**：引入三个可操作的“因果旋钮”——困难样本移除（将相似度置零）、边际调整（为困难对增加边际 $\sigma$）和温度缩放（对困难对使用缩放温度 $\rho\tau$）——对困难样本对进行差异化处理。

从方法谱系来看，该工作处于“无监督对比学习的样本难度感知”这一新兴子方向。与侧重于正样本增强策略或负样本采样策略的既有工作不同，本文从相似图的理论视角出发，揭示了困难样本（不同类但高相似度的样本对）通过增大归一化邻接矩阵中非对角块的相似度 $\gamma$，从而恶化线性探测误差界的因果机制。这一理论框架将“是否处理困难样本”从一个经验性选择提升为具有误差界保证的设计原则。

### 方法模块与知识库定位

论文提出的完整框架包含三个可组合的方法模块：

1. **困难样本选择模块**：基于投影器前特征 $f(x)$ 的余弦相似度百分位数进行识别。定义 $Sim_{posLow}$ 和 $Sim_{posHigh}$ 为降序排列相似度的下界和上界百分位数值，困难对指示函数为：

   $$p _ { i , j } : = \mathbf { 1 } _ { [ S i m _ { p o s L o w } \leq s _ { i j } < S i m _ { p o s H i g h } ] }$$

   消融实验（Table 7）表明，使用投影器前特征进行选择优于投影器后特征，这与此前部分工作使用投影器后特征的做法形成对比。

2. **损失调整模块**：对选定的困难对在 InfoNCE 损失中应用三种策略之一：
   - **移除**：将困难对的相似度置零，对应损失 $\ell_{\mathrm{R}}(i,j)$（Eq. 13）；
   - **边际调整**：为困难对增加边际 $\sigma$，对应损失 $\ell_{\mathrm{M}}(i,j)$（Eq. 14），理论上等价于从归一化相似矩阵中减去归一化边际矩阵 $\bar{M}$（Theorem 4.2）；
   - **温度缩放**：对困难对使用缩放温度 $\rho\tau$，对应损失 $\ell_{\mathrm{T}}(i,j)$（Eq. 15），理论上等价于元素级温度缩放的加权矩阵分解（Theorem 4.4）。

3. **组合方法**：将边际调整和温度缩放整合为统一损失（Eq. 16），在 TinyImagenet 上取得 $80.00\%$ 的准确率，较 SimCLR 基线提升 $+10.42$ 个百分点（Table 4）。

### 适用边界与局限

**理论假设的约束**：
- 理论分析依赖于谱对比损失与 InfoNCE 等价的假设，以及标签可从数据增强中恢复的假设。当这些假设在特定数据分布或增强策略下不成立时，误差界结论的适用性需要审慎评估。
- 相似图建模采用了简化的块结构假设（同类相似度 $\alpha$、异类简单相似度 $\beta$、异类困难相似度 $\gamma$），实际数据中的相似度分布可能更为复杂。

**实验验证的范围**：
- 主要实验在中小规模数据集（CIFAR-10/100、STL-10、TinyImagenet）上进行。虽然在 ImageNet-1k 上也有初步验证（Table 8），但大规模场景下的效果和计算开销需要更多证据支撑。
- 困难样本选择需要额外计算批次内的成对余弦相似度，并引入超参数 $posHigh$ 和 $posLow$。尽管参数敏感性分析（Figure 4(a)(b)）表明性能对区间端点不敏感，但在不同数据分布和批次大小下的自适应性仍需进一步研究。

**困难样本定义的局限性**：
- 当前方法基于余弦相似度百分位数定义困难样本，在极端噪声或类别边界高度模糊的场景下，所选区间可能包含大量同类样本对，从而削弱方法效果。

### 开放问题

1. **理论框架的扩展性**：当前的相似图分析和误差界推导基于谱对比损失的矩阵分解等价性，如何将该框架扩展至其他对比学习范式（如 BYOL、SimSiam 等非对称架构）仍是一个开放问题。

2. **困难样本与长尾分布的关系**：论文在 TinyImagenet-LT 上的实验（Table 6）初步表明组合方法对长尾分布有效（$+4.28$ 个百分点），但困难样本与尾部类别之间的深层关系——例如尾部类别是否天然构成困难样本，以及能否利用困难样本处理机制缓解尾部类别坍塌——尚未被充分探索。

3. **超参数的自适应机制**：当前 $posHigh$ 和 $posLow$ 作为固定百分位数超参数，在跨数据集和跨任务迁移时需要手动调节。开发基于数据统计特性或训练动态的自适应选择机制是一个有价值的方向。

4. **困难样本影响的更细粒度刻画**：当前理论将困难样本的影响统一建模为 $\gamma - \beta$ 的差异，但不同困难样本对下游任务的损害程度可能存在异质性。如何识别和处理“最有危害”的困难样本子集，值得进一步研究。

## 原文 PDF

![[paperPDFs/ICLR_2026/Difficult_Examples_Hurt_Unsupervised_Contrastive_Learning_A_Theoretical_Perspective.pdf]]
