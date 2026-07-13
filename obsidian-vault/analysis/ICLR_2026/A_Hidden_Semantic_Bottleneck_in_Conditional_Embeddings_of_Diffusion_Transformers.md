---
title: "A Hidden Semantic Bottleneck in Conditional Embeddings of Diffusion Transformers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Hidden_Semantic_Bottleneck_in_Conditional_Embeddings_of_Diffusion_Transformers.pdf
project_link: null
code_link: null
aliases:
- CEP
- HSBCEDT
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/interpretability_and_visualization
core_operator: "通过剪枝低幅度的尾部维度（最多移除66%的维度），可以在保持甚至提升生成质量的同时，揭示出条件嵌入的过度参数化本质。"
primary_logic: "扩散Transformer通过AdaLN全局注入条件，其条件嵌入向量呈现出极端对齐（余弦相似度>99%）和极度稀疏（有效维度仅1-2%）的特性，表明语义编码远比预期更紧凑，为设计更高效的条件机制提供了新视角。"
claims:
- "类条件嵌入在ImageNet-1K上表现出超过99%的极端余弦相似度。"
- "连续条件任务（如姿态引导图像生成和视频到音频生成）的余弦相似度超过99.9%。"
- "语义信息集中在少数维度（约10-20个），头部维度承载主要信号，尾部维度贡献极小。"
- "剪枝低幅度维度（移除多达三分之二的嵌入空间）后，生成质量和保真度基本不受影响，甚至在某些情况下有所提升。"
---

# A Hidden Semantic Bottleneck in Conditional Embeddings of Diffusion Transformers

> [!tip] 核心洞察
> 扩散Transformer通过AdaLN全局注入条件，其条件嵌入向量呈现出极端对齐（余弦相似度>99%）和极度稀疏（有效维度仅1-2%）的特性，表明语义编码远比预期更紧凑，为设计更高效的条件机制提供了新视角。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散Transformer条件嵌入中的隐藏语义瓶颈 |
| 英文题名 | A Hidden Semantic Bottleneck in Conditional Embeddings of Diffusion Transformers |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=FetaeuGsEs) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/interpretability_and_visualization |
| Method | 条件嵌入剪枝（Conditional Embedding Pruning） |
| Dataset | ImageNet-1K |

> [!tip] 效果简介
> - ImageNet-1K 上，FID 为 7.1690 (τ=0.01, t0)，对比 7.1694 (REPA)，变化 -0.0004。
> - ImageNet-1K 上，FID 为 7.1598 (τ=0.01, t_{n-k,n})，对比 7.1694 (REPA)，变化 -0.0096。
> - ImageNet-1K 上，FID 为 9.2202 (τ=0.02, ti)，对比 7.1694 (REPA)，变化 +2.0508。

## 概要

该研究揭示了一个存在于扩散Transformer（DiT）条件嵌入中的隐藏语义瓶颈。通过对ImageNet-1K类条件生成任务及连续条件任务（姿态引导图像生成、视频到音频生成）的系统分析，论文发现当前主流扩散Transformer（如REPA、MDT、LightningDiT、MG、SiT等）的条件嵌入向量存在两个极端特性：**极高的类间余弦相似度**（ImageNet-1K上超过99%，连续条件任务超过99.9%）和**极度的维度稀疏性**（有效语义维度仅占总维度的1-2%，约10-20个头部维度承载了绝大部分信号，而剩余98%的尾部维度贡献极小）。

核心方法为**条件嵌入剪枝（Conditional Embedding Pruning）**：通过设定幅度阈值，将低幅度的尾部维度置零。实验表明，即使移除多达66%（甚至更高比例）的尾部维度，生成质量（FID、CLIP分数）基本不受影响，甚至在部分剪枝策略下（如仅在去噪后期步骤剪枝）还能获得小幅提升。这一发现揭示了当前条件嵌入的**过度参数化本质**——语义编码远比预期更紧凑，大量维度是冗余的。

论文定位为对扩散Transformer条件机制的基础性分析研究，而非提出新的生成架构。其主要贡献在于：1）首次系统量化了条件嵌入中的极端对齐与稀疏性；2）通过剪枝实验证明了语义信息被压缩在极少数维度中；3）为设计更高效、更紧凑的条件注入机制（如稀疏条件向量、混合条件策略）提供了实证依据和新的理论视角。



扩散Transformer（DiT）及其后续变体（MDT、SiT、LightningDiT、REPA等）通过自适应层归一化（AdaLN）将条件信息（类别标签、时间步等）编码为紧凑的全局向量，并以此调制模型各层的隐藏激活。这一范式已被证明在图像、视频和音频生成中取得了优异效果。然而，条件嵌入的内部表示结构及其效率边界尚未被系统性地审视。

本文的核心观察是，当前扩散Transformer的条件嵌入存在一个隐藏的语义瓶颈：**条件向量呈现出极端对齐与极度稀疏的双重特性**。具体而言，在ImageNet-1K类条件生成任务上，不同类别的条件嵌入向量之间的余弦相似度超过99%（Figure 1, Figure 3）；在连续条件任务（如姿态引导图像生成X-MDPT、视频到音频生成MDSGen）中，该相似度甚至超过99.9%。与此同时，这些高维向量（如1152维）的有效信息仅集中在极少数头部维度上。通过参与率（Participation Ratio, PR）分析发现，归一化参与率（nPR）仅为1–2%，意味着语义信息被压缩到约10–20个维度中，而剩余约98%的尾部维度贡献极小（Table 1, Figure 5, Figure 9）。这种结构在DiT、MDT、LightningDiT、MG、SiT、REPA等多种模型中一致出现，表明其并非个别模型的偶然现象，而是AdaLN条件注入机制下的普遍行为。

这一发现揭示了现有条件嵌入设计中的根本性矛盾：尽管模型使用了完整的高维向量，但其语义编码远比预期更紧凑。现有方法通过AdaLN将条件信息全局注入所有层，却未意识到嵌入空间已被过度参数化——大量维度几乎不携带语义信号，仅起到极微弱的调节作用。这构成了一个**语义瓶颈**：条件信息被不必要地分散到大量冗余维度中，而非被高效地压缩到少数关键维度上。该瓶颈不仅造成了计算浪费，也可能限制了条件编码的表达效率。

本文的动机正是基于这一观察，提出两个核心问题：（1）扩散Transformer的条件嵌入为何会自发地形成这种极端对齐与稀疏的结构？（2）能否通过显式剪枝冗余的尾部维度，在保持甚至提升生成质量的同时，揭示条件嵌入的过度参数化本质？通过系统的剪枝实验，本文展示了移除多达66%的低幅度维度后，生成质量几乎不受影响，甚至在某些指标上有所提升（如REPA-XL在ImageNet-1K上的FID从7.1694降至7.1598，CLIP分数从29.746升至29.807）（Table 2）。这有力地证明了当前条件嵌入存在显著的冗余，并为设计更高效、更紧凑的条件机制提供了新的视角。



## 核心方法与创新机理

本文的核心创新在于**揭示并实证了扩散Transformer（DiT）条件嵌入向量中存在的隐藏语义瓶颈**，并提出了一种基于此发现的高效剪枝策略。与以往将条件嵌入视为稠密、高维语义表征的假设不同，该工作通过系统性分析，指出当前最先进的扩散Transformer模型（如DiT、MDT、SiT、LightningDiT、MG、REPA）的条件嵌入向量 `~c` 存在两个被忽视的极端特性：**极高的类间余弦相似度**和**极度的维度稀疏性**。

**关键发现与因果机制：**

1.  **极端对齐（Extreme Alignment）**：在ImageNet-1K的1000类条件下，不同类别的条件嵌入向量间的余弦相似度普遍超过99%（Figure 3）。在连续条件任务（如姿态引导图像生成X-MDPT、视频到音频生成MDSGen）中，该相似度甚至超过99.9%（Figure 4c）。这意味着，尽管语义截然不同，这些嵌入在向量空间中的方向几乎完全一致，形成了一个**隐藏的语义瓶颈**——绝大多数维度无法有效区分不同条件。

2.  **极度稀疏（Extreme Sparsity）**：语义信息被压缩到极少数“头部维度”（head dimensions）中。通过参与率（Participation Ratio, PR）分析，归一化参与率（nPR）显示，如MDT、LightningDiT、MG、REPA等模型仅依赖不到2%的维度（Table 1）。具体而言，在1152维的嵌入中，仅有约10-20个维度的幅度显著（~5-8），其余98%的“尾部维度”（tail dimensions）幅度极小（~10^-3–10^-1），贡献可忽略（Figure 5, Figure 9）。方差分析进一步证实，几乎所有的方差都集中在这15-20个头部维度上（Figure 9b）。

**核心创新点：条件嵌入剪枝（Conditional Embedding Pruning）**

基于上述发现，本文提出的核心创新方法并非设计新的条件注入模块，而是**直接剪枝现有预训练模型中的冗余尾部维度**。其核心思想是：既然尾部维度几乎不携带语义信息，将其置零（pruning）不会损害生成质量。

*   **Changed Slot**：条件嵌入向量 `~c` 从完整的1152维（或1024/768维）被剪枝为仅保留头部维度的稀疏向量。
*   **实现方式**：通过设定幅度阈值 `τ`，将向量 `~c` 中绝对值低于 `τ` 的维度置零，保留头部维度。该过程无需重新训练模型，可直接应用于预训练权重。
*   **关键证据**：实验证明，即使移除高达66%的尾部维度（`τ=0.01`），生成质量（FID, CLIP）不仅不受影响，甚至在部分设置下略有提升（Table 2）。例如，在REPA模型上，剪枝38%的尾部维度（`τ=0.01, t0`）后，FID从7.1694降至7.1690，CLIP从29.746提升至29.807。相反，移除仅0.69%的头部维度（8/1152，`τ=1.0`）会导致生成质量灾难性下降（FID从7.17飙升至523.76）（Table 2, Figure 7）。t-SNE可视化也证实，仅保留头部维度即可保持清晰的类别聚类，而仅保留尾部维度则导致聚类坍塌（Figure 13）。

**与Baseline的对比本质：**

该工作的创新不在于提出一个性能更强的模型，而在于**对现有模型架构（AdaLN条件注入范式）进行了一次彻底的“诊断”和“瘦身”**。它揭示了当前扩散Transformer模型在条件编码上存在严重的过度参数化（over-parameterization）问题，为设计更高效、更紧凑的条件机制提供了新的视角和可操作的方案。其提出的剪枝策略，本质上是对现有模型隐含冗余的直接利用和验证。



该研究的核心发现围绕扩散Transformer（DiT）中条件嵌入向量存在的隐藏语义瓶颈展开，并基于此提出了一种轻量级的剪枝方法。整体框架可概括为：**观察瓶颈 → 量化瓶颈 → 验证因果性 → 提出剪枝方法**。

**1. 条件注入机制与输入输出流**
扩散Transformer通过自适应层归一化（AdaLN）将条件信息注入模型。其流程为：类别标签 $y$ 和时间步嵌入 $t$ 相加，生成一个全局紧凑的条件向量 $\vec{c} = y + t$。随后，该向量通过线性投影 $W_\gamma$ 和 $W_\beta$ 分别生成缩放参数 $\gamma$ 和偏移参数 $\beta$，用于调制所有层的隐藏激活（AdaLN($h|c$) = $\gamma(c) \odot (h - \mu(h))/\sigma(h) + \beta(c)$）。这是一个全局注入过程，条件向量 $\vec{c}$ 是整个生成流程中唯一的条件信息载体。

**2. 瓶颈的发现与量化（核心观察）**
研究首先通过分析多个SOTA扩散Transformer模型（如DiT, MDT, SiT, LightningDiT, MG, REPA）的条件向量，发现两个关键现象：
- **极端对齐**：不同类别的条件向量 $\vec{c}$ 之间的余弦相似度极高。在ImageNet-1K上，类条件嵌入的余弦相似度超过99%（Figure 3）；在连续条件任务（如姿态引导图像生成X-MDPT、视频到音频生成MDSGen）中，该相似度甚至超过99.9%（Figure 4）。
- **极度稀疏**：语义信息高度集中在极少数维度上。通过参与率（Participation Ratio, PR）量化，发现有效维度仅占全部维度的1-2%（例如，1152维中仅有约10-20个头部维度承载主要信号），而剩余98%的尾部维度贡献极小，其幅度接近零（Table 1, Figure 5）。方差分析（Figure 9）也证实，方差集中在15-20个头部维度（<2%）。

**3. 因果性验证：维度剪枝方法**
为验证尾部维度的冗余性并揭示瓶颈的因果机制，研究提出**条件嵌入剪枝（Conditional Embedding Pruning）**方法。该方法基于幅度阈值 $\tau$，将条件向量 $\vec{c}$ 中绝对值低于阈值的尾部维度置零。稀疏率定义为 $s_{\text{tail}(\tau)} = \frac{1}{d} \#\{i : |c_i| < \tau\}$。实验表明，剪枝低幅度尾部维度（最多可移除66%的维度）对生成质量（FID, CLIP）影响极小，甚至在部分情况下略有提升（Table 2, Figure 8）。相反，剪枝极少数的头部维度（如仅移除0.69%的维度）会严重破坏生成质量（FID从7.17升至523.76）（Table 2, Figure 7）。这证明了头部维度承载了必要的语义信息，而尾部维度是冗余的。

**4. 模块关系与剪枝策略**
剪枝模块作用于整个条件向量 $\vec{c}$ 上。实验探索了三种剪枝时序策略（Table 2）：
- **$t_i$**: 每一步去噪时都进行剪枝。
- **$t_0$**: 仅在初始步骤剪枝。
- **$t_{n-k,n}$**: 仅在去噪的最后 $k$ 步剪枝。
结果表明，在去噪后期进行剪枝（$t_{n-k,n}$）通常能获得最大的FID改善（如REPA模型，FID从7.1694降至7.1598），这暗示尾部维度可能在早期起到稳定优化的作用，而在后期则引入噪声。

**5. 与基线方法的关系**
该研究并未提出一个新的生成模型，而是对现有SOTA模型（DiT, MDT, SiT, LightningDiT, MG, REPA, X-MDPT, MDSGen）的**条件嵌入模块**进行后验分析与剪枝。其核心论点是：这些模型的条件嵌入空间存在严重的过度参数化，其有效语义维度远低于其实际维度。



### 条件注入机制：自适应层归一化 (AdaLN)

扩散Transformer通过全局紧凑的条件向量调制模型行为。如图2所示，条件向量 $\vec{c}$ 通过自适应层归一化注入到每一层。给定隐藏激活 $h \in \mathbb{R}^d$，AdaLN的计算方式为：

$$
\mathrm{AdaLN}(h \mid c) = \gamma(c) \odot \frac{h - \mu(h)}{\sigma(h)} + \beta(c)
$$

其中缩放参数 $\gamma(c)$ 和偏移参数 $\beta(c)$ 是条件向量 $c$ 的线性投影：

$$
\gamma(c) = W_\gamma c, \quad \beta(c) = W_\beta c
$$

这里 $W_\gamma$ 和 $W_\beta$ 是可学习的投影矩阵。条件向量 $c$ 通常由类别标签嵌入 $y$ 和时间步嵌入 $t$ 相加得到：$\vec{c} = y + t$。

### 语义瓶颈的量化指标

论文提出了两个核心指标来量化条件嵌入的语义瓶颈：

**参与率 (Participation Ratio, PR)**：用于估计向量中承载大部分总幅度的坐标数量。

$$
\alpha = \mathrm{PR}(v) = \frac{(\sum_{i=1}^d v_i)^2}{\sum_{i=1}^d v_i^2}, \quad \alpha_{\mathrm{norm}} = \frac{\alpha}{d}
$$

其中 $d$ 是向量维度，$v_i$ 是向量第 $i$ 个分量的绝对值。$\alpha$ 表示有效维度数，$\alpha_{\mathrm{norm}}$ 是归一化后的参与率。例如，表1显示REPA-XL模型的 $\alpha_{\mathrm{norm}}$ 仅为1.60%，意味着1152维的嵌入中实际有效维度仅约18个。

**稀疏率 (Sparsity Ratio)**：用于衡量条件向量中低幅度维度的比例。

$$
s_{\mathrm{tail}(\tau)} = \frac{1}{d} \#\{i : |c_i| < \tau\}
$$

其中 $\tau$ 是幅度阈值，$\#\{i : |c_i| < \tau\}$ 表示幅度低于阈值的维度数量。相应地，头部维度比例定义为 $s_{\mathrm{head}(\tau)} = \frac{1}{d} \#\{i : |c_i| > \tau\}$。

### 条件嵌入的结构分解

基于上述量化分析，论文将条件嵌入分解为两个分量：

$$
c_y = c_{y,\mathrm{head}} + c_{y,\mathrm{tail}}, \quad \|c_{y,\mathrm{head}}\| \gg \|c_{y,\mathrm{tail}}\|
$$

其中 $c_{y,\mathrm{head}}$ 是高幅度的头部维度（约10-20个，占1-2%），承载主要的语义信号；$c_{y,\mathrm{tail}}$ 是低幅度的尾部维度（约98%），贡献极小。不同类别条件嵌入之间的余弦相似度极高：

$$
\mathrm{cosine}(c_y, c_{y'}) \approx 0.99 \quad \forall y \neq y'
$$

这一极端对齐性表明，尽管类别语义不同，其条件嵌入在方向上的差异极小，语义信息被压缩到极少数维度中。

### 维度剪枝策略

基于上述发现，论文提出条件嵌入剪枝方法：根据幅度阈值 $\tau$，将条件向量 $c$ 中低于阈值的尾部维度置零，保留头部维度。实验表明，剪枝尾部维度（移除38%-66%的维度）对生成质量影响很小甚至略有提升（表2：REPA基线FID 7.1694 vs. $\tau=0.01, t_0$ 剪枝后FID 7.1690），而移除头部维度（仅0.69%）会严重破坏生成质量（FID从7.17升至523.76）。



## 实验与关键发现

### 主结果：条件嵌入的极端对齐与维度稀疏性

核心实验发现揭示了一个隐藏的语义瓶颈：扩散Transformer的条件嵌入向量在ImageNet-1K类条件生成任务上表现出超过99%的极端余弦相似度（Figure 3），而连续条件任务（如姿态引导图像生成X-MDPT、视频到音频生成MDSGen）的余弦相似度甚至超过99.9%（Figure 4c）。这一现象并非个别模型的异常，而是跨DiT、MDT、LightningDiT、MG、SiT、REPA等多个SOTA模型的普遍特征（Figure 5-6）。

参与率（PR）分析进一步量化了维度稀疏性（Table 1）：MDT、LightningDiT、MG、REPA等模型的归一化参与率（nPR）仅为1.60%-2.28%，意味着语义信息被压缩到约1-2%的头部维度（约10-20个维度），而剩余98%的尾部维度贡献极小。连续条件任务的nPR略高（X-MDPT为13.57%，MDSGen为48.42%），但仍远低于全维度容量。方差分析（Figure 9）确认了这一结论：仅15-20个头部维度承载了大部分方差（<2%），而剩余98%的尾部维度变化极小，表明语义信息被限制在一个极小子空间中。

![[assets/figures/papers/iclr26_0002_FetaeuGsEs_A_Hidden_Semantic_Bottleneck_in_Conditional_Embe/figures/020_Table_1.jpg]]
*Table 1: Participation Ratio (PR) in learned conditional embeddings of state-of-the-art models on Imagenet-1K generation (discrete) and DeepFashion/VGGSound (continuous)*

### 剪枝实验：尾部维度冗余性的因果验证

为验证尾部维度的冗余性，作者提出了条件嵌入剪枝策略——根据幅度阈值τ将低幅度尾部维度置零。核心结果（Table 2）表明：

![[assets/figures/papers/iclr26_0002_FetaeuGsEs_A_Hidden_Semantic_Bottleneck_in_Conditional_Embe/figures/022_Table_2.jpg]]
*Table 2: Performance and semantic metrics under sparsification. ti: prune every step, t0: prune only at start, $t _ { n - k , n } \colon$ prune during last k steps. following sections. Next, we examine in detail how head dimensions influence generation quality and clarify how their role differs from that of the tail dimensions*

- **剪枝尾部维度对生成质量影响极小**：在REPA-XL上，以τ=0.01剪枝（移除38%的维度，仅在初始步骤t0执行），FID从基线7.1694降至7.1690（改善-0.0004），CLIP从29.746提升至29.807（+0.061）。在去噪后期步骤剪枝（t_{n-k,n}）获得更大的FID改善（7.1598），表明后期剪枝可能抑制了残差噪声。
- **移除头部维度会严重破坏生成**：仅移除0.69%的头部维度（τ=1.0，ti策略），FID从7.17飙升至523.76，图像质量完全崩溃（Figure 7）。这直接证实了头部维度承载了关键的语义信号。
- **剪枝策略的鲁棒性**：类似结果在MG和LightningDiT上得到复现（Table 3）。MG基线FID 7.2478，在τ=0.01剪枝后为7.2791（微小退化）；LightningDiT基线FID 7.0802，剪枝后降至7.0130（改善）。剪枝尾部维度有时能提升生成质量，这一反直觉现象可能与去除尾部维度中的噪声信号有关。

![[assets/figures/papers/iclr26_0002_FetaeuGsEs_A_Hidden_Semantic_Bottleneck_in_Conditional_Embe/figures/071_Table_3.jpg]]
*Table 3: More baselines. Performance and semantic metrics under sparsification. $t _ { i } { \mathrm { : } }$ prune every step, t0: prune only at start, $t _ { n - k , n } \colon$ prune during last k steps

### 消融与机制分析

**头部 vs 尾部维度的语义角色**：t-SNE可视化（Figure 13）提供了直观证据——仅保留头部维度能保持清晰的类别聚类（与完整嵌入几乎一致），而仅保留尾部维度则导致聚类坍塌为纠缠点，表明尾部维度几乎不包含可区分的语义结构。

**剪枝时机的影响**：Table 2显示，在去噪后期步骤剪枝（t_{n-k,n}）比在初始步骤（t0）或每一步（ti）剪枝获得更大的FID改善。这支持了假设：早期步骤需要完整条件信息进行粗粒度生成，而后期步骤中尾部维度可能引入残差噪声，剪枝后反而提升质量。

**连续条件任务的验证**：在DeepFashion姿态引导图像生成任务上（Table 7），X-MDPT基线FID为18.6372，剪枝40%的尾部维度（τ=0.1）后FID为18.6692（仅+0.032），几乎无退化。Figure 10视觉展示即使剪枝50-75%的维度，生成的人物图像仍保持高质量，只要关键头部维度被保留。

### 失败模式与边界

**极端剪枝的失效**：当剪枝阈值过高（如τ=0.02移除66%维度），FID开始退化（9.2202 vs 7.1694），表明虽然尾部维度冗余，但完全移除仍会损失部分信息。当剪枝阈值达到0.1时，FID显著恶化至18.5616。

**DiT模型的异质性**：DiT的类间余弦相似度最低约为88%（Figures 14-19），低于其他模型（>99%）。这一差异是否与DiT较弱的生成性能相关，仍是一个开放问题。

**计算效率的初步分析**：Figure 42展示了稀疏向量比稠密向量具有更快的运行时间，但该分析仅提供了初步结果，未进行全面的速度或内存基准测试。

### 证据强度评估

核心发现（极端对齐、维度稀疏性、剪枝尾部维度的无害性）的置信度均为1.0，因为它们在多个模型（DiT, MDT, LightningDiT, MG, SiT, REPA）、多个数据集（ImageNet-1K, DeepFashion, VGGSound）和多种条件类型（离散类、连续姿态、视频到音频）上被一致复现。剪枝时机对FID改善的影响（t_{n-k,n}优于t0）的置信度为0.9，因为差异较小（7.1598 vs 7.1690），可能受随机性影响。剪枝提升生成质量的机制解释（抑制残差噪声）仍需进一步的理论验证。

### 补充图表

![[assets/figures/papers/iclr26_0002_FetaeuGsEs_A_Hidden_Semantic_Bottleneck_in_Conditional_Embe/figures/095_Table_4.jpg]]
*Table 4: Separate timestep (t) and conditions (y). Participation Ratio (PR) in learned conditional embeddings of state-of-the-art models on Imagenet-1K class-conditioned generation. With 1 denotes the methods used: AdaLN, and 2 denotes the method used: concatenation*

![[assets/figures/papers/iclr26_0002_FetaeuGsEs_A_Hidden_Semantic_Bottleneck_in_Conditional_Embe/figures/096_Table_5.jpg]]
*Table 5: Separate timestep (t) and conditions (y). Participation Ratio (PR) in learned conditional embeddings of state-of-the-art models on text or video-conditioned generation. With 1 denotes the methods used: AdaLN, and 3 denotes the method used: cross-attention*

![[assets/figures/papers/iclr26_0002_FetaeuGsEs_A_Hidden_Semantic_Bottleneck_in_Conditional_Embe/figures/097_Table_6.jpg]]
*Table 6: Precision and Recall with previous metrics: FID, IS, and CLIP*



## 定位与知识库关联

该工作位于扩散Transformer条件机制研究的核心位置，其发现直接挑战了当前主流架构中条件嵌入的设计假设。与基线模型（DiT, Peebles & Xie, 2023; MDT, Gao et al., 2023; SiT, Ma et al., 2024; LightningDiT, Yao et al., 2025; MG, Tang et al., 2025; REPA, Yu et al., 2025）相比，该研究并非提出新的生成框架，而是揭示了这些模型共享的隐藏瓶颈：条件嵌入向量~c = y + t存在极端的语义稀疏性和对齐性。

**适用边界与核心发现。** 该发现适用于所有通过AdaLN全局注入条件的扩散Transformer模型。在ImageNet-1K类条件生成任务上，不同类别的条件嵌入余弦相似度超过99%（Figure 3），而语义信息仅集中在约1-2%的头部维度中，归一化参与率（nPR）低至1.60%-2.28%（Table 1）。连续条件任务（如X-MDPT的姿态引导图像生成、MDSGen的视频到音频生成）虽使用更多维度（nPR为13-48%），但余弦相似度反而更高（>99.9%），表明该现象具有跨任务普遍性。

**与基线的关系。** 该研究将多个SOTA模型作为分析对象，而非改进对象。通过维度剪枝实验（移除38%-66%的低幅度尾部维度），证明这些模型的条件嵌入存在严重的过度参数化：剪枝后FID和CLIP分数基本不变甚至略有提升（Table 2: REPA基线FID 7.1694，τ=0.01剪枝后FID 7.1598）。移除头部维度（仅0.69%）则会导致生成质量崩溃（FID升至523.76），证实了头部维度的语义承载作用。

**局限。** 主要局限在于分析深度和泛化性。第一，对高余弦相似度和稀疏性的理论解释仍为假设（Section 6.2），缺乏严格的数学证明。第二，实验集中在ImageNet-1K类条件生成，连续条件任务的分析相对有限。第三，剪枝仅在预训练模型上进行，未探索其对训练过程的影响。第四，未验证该冗余模式是否出现在GANs或自回归模型等其他生成框架中。第五，计算效率分析（Figure 42）仅展示了初步结果，缺乏全面的速度或内存基准测试。

**开放问题。** 核心未解问题包括：（1）连续条件嵌入为何使用更多维度（13-48%）但余弦相似度却更高（99.99% vs 90-99.4%）？（2）剪枝尾部维度有时提升生成质量的确切机制是什么？（3）全局AdaLN机制如何驱动观察到的稀疏性和高相似性？（4）DiT模型为何表现出较低的余弦相似度（最低约88%），这是否与其较弱的生成性能有关？（5）这种冗余模式是否也出现在其他生成框架中？（6）未来架构如何从压缩或混合条件策略中受益，以在保持语义保真度的同时降低计算开销？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Hidden_Semantic_Bottleneck_in_Conditional_Embeddings_of_Diffusion_Transformers.pdf

![[paperPDFs/ICLR_2026/A_Hidden_Semantic_Bottleneck_in_Conditional_Embeddings_of_Diffusion_Transformers.pdf]]
