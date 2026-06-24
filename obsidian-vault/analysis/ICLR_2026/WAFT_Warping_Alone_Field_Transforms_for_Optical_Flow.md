---
title: "WAFT: Warping-Alone Field Transforms for Optical Flow"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WAFT_Warping_Alone_Field_Transforms_for_Optical_Flow.pdf
openreview_forum_id: HTqGE0KcuF
aliases:
- WAFT
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "用高分辨率特征扭曲（warping）完全替代代价体，并采用视觉Transformer架构处理全局依赖性。"
primary_logic: "扭曲操作仅获取对应像素特征，结合Transformer的注意力机制可隐式建模大位移，极大降低内存开销，从而允许直接在高分辨率特征上进行索引与更新，提升精度和效率。"
claims:
- "WAFT移除代价体依赖，显著降低内存消耗。"
- "在高分辨率特征图上进行扭曲索引显著提升性能。"
- "视觉Transformer架构对迭代扭曲方法至关重要，替换为CNN导致性能剧降。"
- "WAFT在Spring基准的所有指标上排名第一。"
---

# WAFT: Warping-Alone Field Transforms for Optical Flow

> [!tip] 核心洞察
> 扭曲操作仅获取对应像素特征，结合Transformer的注意力机制可隐式建模大位移，极大降低内存开销，从而允许直接在高分辨率特征上进行索引与更新，提升精度和效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | WAFT：基于纯翘曲场变换的光流估计方法 |
| 英文题名 | WAFT: Warping-Alone Field Transforms for Optical Flow |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=HTqGE0KcuF); [GitHub](https://github.com/princeton-vl/WAFT) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | WAFT |
| Dataset | Spring, Sintel (final, w/o Ambush 1), KITTI (train, zero-shot) |

> [!tip] 效果简介
> - Spring 上，EPE 为 0.325 (WAFT-DINOv3-a2)，对比 0.340 (DPFlow)，变化 -0.015。
> - Spring 上，WAUC 为 95.051 (WAFT-DINOv3-a2)，对比 94.980 (DPFlow)，变化 +0.071。
> - Sintel (final, w/o Ambush 1) 上，EPE 为 1.639 (WAFT-Twins-a2)，对比 1.750 (Flowformer++)，变化 -0.111。

## 概述

光流估计是计算机视觉中的基础任务，旨在预测视频帧之间像素级的稠密运动场。以**RAFT**（Teed & Deng, ECCV 2020）为代表的迭代优化方法长期占据主导地位，但其核心组件——代价体（cost volume）——存在根本性瓶颈：在高分辨率下内存消耗呈二次增长，迫使方法在低分辨率特征图上构建匹配代价，导致运动边界模糊和精细结构丢失。部分代价体方法（如**SEA-RAFT**，Wang et al., ECCV 2024）通过限制搜索范围缓解了内存压力，但本质上仍受限于局部匹配的折中。

本文提出**WAFT（Warping-Alone Field Transforms）**，以极简的纯翘曲场变换范式彻底替代代价体。其核心洞察在于：利用当前光流估计在高分辨率特征图上执行像素级翘曲索引，仅获取对应点的特征向量，而非构建全局或局部的显式代价体。这一操作的内存开销极低，使得方法可以直接在1/2甚至全分辨率特征上进行匹配与迭代更新，从而获得更锐利的运动边界和更高的精度。同时，WAFT移除了RAFT类架构中标准的上下文编码器，进一步简化了流程。

为弥补代价体移除后全局匹配能力的缺失，WAFT的循环更新模块采用基于视觉Transformer的架构（修改的DPT-Small），利用自注意力机制隐式建模大位移依赖关系。消融实验表明，该设计对方法至关重要：若将Transformer替换为CNN，性能会出现断崖式下降。

在实验验证上，WAFT在Spring基准测试的所有指标上排名第一，在Sintel和KITTI上也达到领先水平，同时展现出优异的零样本跨数据集泛化能力。效率方面，WAFT比**Flowformer++**（Shi et al., CVPR 2023）快1.3倍，比**CCMR+**快4.1倍，训练内存消耗显著低于基于代价体的方法——在1/2分辨率下，WAFT仅需9.2 GiB，而SEA-RAFT则直接超出显存上限。

## 背景与动机

### 光流估计中的代价体瓶颈

光流估计旨在计算两帧图像间逐像素的稠密运动场。当前主流的迭代光流方法——以 **RAFT**（Teed & Deng, ECCV 2020）为代表——普遍依赖**代价体（cost volume）** 来显式编码帧间像素的视觉相似度。代价体通过计算特征向量的点积构建：

$$V_{p, p'} = F(I_1)_p \cdot F(I_2)_{p'}$$

然而，全代价体的计算复杂度与空间分辨率呈平方关系，导致极高的内存开销。为缓解这一问题，后续工作如 **SEA-RAFT**（Wang et al., ECCV 2024）和 **Flowformer++**（Shi et al., CVPR 2023）引入了**部分代价体**，将搜索范围限制在当前光流估计的局部邻域 $r$ 内：

$$V_{par}(f_{cur}; r)_p = \mathrm{concat}( \{ V_{p, p'} | \forall p' \in I_2, \mathrm{s.t.} \| p + (f_{cur})_p - p' \|_{\infty} \leq r \} )$$

尽管部分代价体降低了计算量，但这些方法仍存在两个根本性缺陷：

1. **高内存消耗**：即使在 1/8 分辨率下构建代价体，训练时仍需要大量显存（例如 SEA-RAFT 在 RTX A6000 上以 batch size 1 运行需 14.1 GiB，升至 1/4 分辨率则飙升至 25.8 GiB，1/2 分辨率直接内存溢出）。
2. **低分辨率导致的精度损失**：受限于内存约束，代价体通常在低分辨率特征图上操作，导致运动边界模糊和细节误差（见 Figure 3 中低分辨率方法的边界模糊现象）。

### 扭曲操作的潜力与未充分利用

与代价体不同，**特征扭曲（warping）** 是一种轻量级操作，仅根据当前光流估计从第二帧特征图上索引对应像素的特征向量：

$$\mathsf{Warp}(f_{cur})_p = F(I_2)_{p + (f_{cur})_p}$$

如 Figure 2 所示，扭曲仅使用单个对应像素的信息，而非邻域内所有像素的相似度，因此在时间和内存效率上具有天然优势。这一效率优势使得**高分辨率特征索引**成为可能——直接在高分辨率特征图上进行扭曲和更新，有望获得更清晰的运动边界和更低的误差。

然而，在 WAFT 之前，纯扭曲方法并未在迭代光流框架中取得竞争力。原因在于：扭曲操作仅提供点对点的特征匹配，缺乏代价体所隐含的局部搜索和歧义消解能力，在处理大位移、遮挡或模糊区域时容易失效。

### 核心动机：用高分辨率扭曲替代代价体

WAFT 的核心动机基于以下观察：如果能够有效处理全局依赖性，那么**高分辨率扭曲**可以完全替代代价体，同时获得以下收益：

- **大幅降低内存开销**：移除代价体后，内存消耗不再随分辨率急剧膨胀，使得在 1/2 甚至全分辨率上进行特征索引和更新成为可能。
- **提升边界精度**：高分辨率处理直接带来更锐利的运动边界和更低的整体误差（Figure 3 提供了定性证据）。
- **简化架构**：代价体的移除也使得上下文编码器（context encoder）——RAFT 类方法中为更新模块提供额外特征的标准组件——变得冗余，可被安全移除，进一步精简流程。

为弥补扭曲操作缺乏显式搜索能力的不足，WAFT 在循环更新模块中采用**视觉Transformer架构**（修改的 DPT-Small），利用自注意力机制隐式建模大位移和全局上下文，从而在纯扭曲范式下仍能保持对大运动的鲁棒性。

## 核心创新

WAFT 的核心创新在于对迭代光流估计框架的结构性简化——**用高分辨率特征扭曲（warping）完全替代代价体（cost volume），并移除了上下文编码器（context encoder）**，同时将更新模块升级为视觉 Transformer 架构。这一设计直击当前迭代方法的两个关键瓶颈：代价体的高内存消耗和低分辨率特征导致的边界模糊。

### 代价体 → 高分辨率特征扭曲

传统迭代光流方法（如 **RAFT**，Teed & Deng, ECCV 2020；**SEA-RAFT**，Wang et al., ECCV 2024）依赖代价体来编码帧间像素的视觉相似度。全代价体计算两帧所有像素对的特征点积：

$$V_{p, p'} = F(I_1)_p \cdot F(I_2)_{p'}$$

其内存随搜索范围平方增长；部分代价体虽将搜索限制在当前估计的局部邻域内：

$$V_{par}(f_{cur}; r)_p = \mathrm{concat}( \{ V_{p, p'} | \forall p' \in I_2, \mathrm{s.t.} \| p + (f_{cur})_p - p' \|_{\infty} \leq r \} )$$

仍无法从根本上解决内存问题。WAFT 的选择是**仅索引对应像素的特征向量**：

$$\mathsf { W a r p } ( f _ { \mathrm { c u r } } ) _ { p } = F ( I _ { 2 } ) _ { p + ( f _ { \mathrm { c u r } } ) _ { p } }$$

这一操作的内存开销极低。Table 1 的实测数据显示：在 RTX A6000 上以 batch size 1 训练时，SEA-RAFT 在 1/8 分辨率下需 14.1 GiB，1/4 分辨率下升至 25.8 GiB，1/2 分辨率直接显存溢出；而 WAFT-Twins-a2 在三个分辨率下分别仅需 7.0、7.6、9.2 GiB。**内存效率的质变使得 WAFT 可以直接在 1/2 甚至全分辨率特征图上进行扭曲索引**，从而获得更清晰的运动边界和更低的误差（Figure 3 的 Spring 可视化结果佐证了这一点）。

### 上下文编码器的移除

RAFT 及其衍生方法普遍引入一个独立的上下文编码器，为更新模块提供额外特征。WAFT 的消融实验（Table 5）表明，**加入上下文编码器并未带来显著性能提升**（Sintel clean EPE：w/ Context 为 1.22，WAFT-DAv2-a1 为 1.18），却增加了额外的计算开销。因此 WAFT 将其彻底移除，进一步简化了元架构。

### 更新模块：ConvGRU/CNN → 视觉 Transformer

此前的迭代方法多采用 ConvGRU 或 CNN 作为循环更新单元。WAFT 将其替换为**修改的 DPT-Small**（Ranftl et al., 2021），将 patch size 设为 8，位置编码分辨率设为 $224 \times 224$。这一替换的因果逻辑在于：**扭曲操作仅获取单个对应像素的特征，缺乏对全局上下文的显式建模**，而 Transformer 的自注意力机制可以隐式处理大位移依赖，弥补了代价体移除后全局匹配能力的缺失。

Table 5 的消融实验提供了强因果证据：将 DPT-based 更新模块替换为 Res18 时，Sintel clean EPE 从 1.18 急剧恶化至 7.23；替换为 ConvGRU 时也升至 2.79。这表明**视觉 Transformer 架构对纯扭曲迭代方法的有效性是不可或缺的**——在缺乏代价体提供的显式匹配信息时，CNN 有限的感受野无法有效处理大位移场景。

### 创新点的因果链条

上述三个 changed slots 构成了一条清晰的因果链：

1. **扭曲替代代价体** → 内存开销大幅降低 → 允许高分辨率特征索引；
2. **高分辨率索引** → 运动边界更清晰，Spring 的 1px 错误率从 1.82 降至 1.43（Table 5）；
3. **Transformer 更新模块** → 隐式建模全局依赖 → 弥补代价体缺失后的大位移匹配能力，CNN 替代会导致性能崩溃；
4. **移除上下文编码器** → 在性能无损的前提下进一步简化架构。

这一设计使 WAFT 在 Spring 基准的所有指标上排名第一（Table 3），同时在 KITTI 零样本泛化中将误差降低 11%（Table 4），验证了该元架构的有效性。

## 整体框架

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_HTqGE0KcuF/figures/001_Figure_1.jpg]]
*Figure 1: The meta-architecture of WAFT consists of an input encoder and a recurrent update module. We first extract image features from the input encoder, and then use these features to iteratively update the flow estimate for T steps. At each step, we perform feature indexing through a lightweight backward warping on the feature of frame 2, removing the dependency on expensive cost volume used by previous work*

WAFT 的整体元架构由两个核心模块串联构成：**输入编码器**和**循环更新模块**，二者协同完成从原始图像到最终光流场的端到端映射。该架构在概念上承袭了 RAFT 的迭代优化范式，但在关键组件上做了两项根本性简化——完全移除代价体和上下文编码器，代之以高分辨率特征扭曲（warping）操作。

**输入编码器**负责从两帧输入图像 $I_1$、$I_2$ 中独立提取多尺度视觉特征 $F(I_1)$ 和 $F(I_2)$。编码器采用冻结的预训练骨干网络，支持三种适配方案：ImageNet 预训练的 **Twins-SVT-Large**、深度预训练的 **DAv2-S** 以及无监督预训练的 **DINOv3-ViT-S**。与 RAFT 等传统方法不同，WAFT 不额外设置独立的上下文编码器来提供辅助特征——消融实验表明，加入上下文编码器仅将 Sintel clean EPE 从 1.18 变为 1.22，提升微乎其微，却引入了额外计算开销，因此可以安全移除。

**循环更新模块**是整个 pipeline 的核心推理引擎。它以迭代方式预测光流残差，每次迭代的输入由三部分拼接而成：帧 1 的特征 $F(I_1)$、根据当前光流估计从帧 2 特征图上扭曲索引得到的对应特征 $\mathsf{Warp}(f_{\mathrm{cur}})$（公式如下），以及当前的隐藏状态 $\mathrm{Hidden}_t$。该模块内部采用经过修改的 **DPT-Small**（视觉 Transformer）架构，将 patch size 设为 8、位置嵌入分辨率设为 $224 \times 224$，利用 Transformer 的自注意力机制隐式处理大位移依赖，从而无需显式构建搜索范围受限的代价体。

特征扭曲操作定义简洁：
$$\mathsf{Warp}(f_{\mathrm{cur}})_p = F(I_2)_{p + (f_{\mathrm{cur}})_p}$$
即对于帧 1 中的每个像素 $p$，直接使用当前光流估计 $f_{\mathrm{cur}}$ 将 $p$ 映射到帧 2 的对应位置，然后从高分辨率特征图 $F(I_2)$ 上索引出该位置的特征向量。与全代价体（需要计算所有像素对的点积相似度）和部分代价体（在局部邻域内构建）相比，扭曲操作仅访问单一对应像素的信息，内存消耗极低——这使得 WAFT 能够直接在 1/2 甚至全分辨率特征图上进行索引，而基于代价体的方法在 1/2 分辨率下已面临显存溢出（Table 1）。

**预测头**位于循环更新模块之后，从最终隐藏状态生成混合拉普拉斯分布的参数，并通过凸上采样恢复至原始图像分辨率的光流场。训练与推理均固定 $T=5$ 次迭代。

整个流程可概括为：输入两帧图像 → 冻结编码器提取多尺度特征 → 循环更新模块在特征空间内迭代扭曲索引并更新隐藏状态（5 次）→ 预测头输出全分辨率光流。这一设计将内存瓶颈从代价体的二次复杂度中解放出来，使高分辨率特征索引成为可能，进而带来边界精度和整体性能的显著提升。

## 核心模块与公式推导

### 代价体与扭曲操作的对比

传统迭代光流方法的核心瓶颈在于代价体（cost volume）的构建。给定两帧特征图 $F(I_1)$ 和 $F(I_2)$，全代价体通过特征向量的点积计算所有像素对之间的视觉相似度：

$$V_{p, p'} = F(I_1)_p \cdot F(I_2)_{p'}$$

该操作的内存复杂度与特征图分辨率的平方成正比，严重限制了可用的特征分辨率。为缓解此问题，部分代价体方法（如SEA-RAFT）仅在当前光流估计 $f_{cur}$ 定义的局部邻域 $r$ 内构建代价体：

$$V_{par}(f_{cur}; r)_p = \mathrm{concat}( \{ V_{p, p'} \mid \forall p' \in I_2, \mathrm{s.t.} \| p + (f_{cur})_p - p' \|_{\infty} \leq r \} )$$

WAFT 的核心创新在于完全抛弃代价体，转而使用高分辨率特征扭曲（warping）。扭曲操作仅根据当前光流估计从第二帧特征图上索引对应像素的特征向量：

$$\mathsf { Warp } ( f _ { \mathrm { cur } } ) _ { p } = F ( I _ { 2 } ) _ { p + ( f _ { \mathrm { cur } } ) _ { p } }$$

**关键差异**：全代价体计算所有像素对的相似度，部分代价体限制搜索范围，而扭曲操作仅获取单个对应像素的特征。这种极简设计使得内存开销与分辨率线性相关，从而允许在 1/2 甚至全分辨率特征图上进行索引，而基于代价体的方法在 1/2 分辨率时即面临显存溢出（见 Table 1）。

### 循环更新模块

WAFT 的元架构由输入编码器和循环更新模块两部分组成。在第 $t$ 步迭代中，更新模块接收三部分输入：帧1的特征 $F(I_1)$、经当前光流 $f_{cur}$ 扭曲的帧2特征 $\mathsf{Warp}(f_{cur})$，以及当前的隐藏状态 $\mathrm{Hidden}_t$。三者拼接后送入修改的 DPT-Small 架构。

更新模块采用视觉 Transformer（DPT）而非传统的 ConvGRU 或 CNN，这是方法成立的**必要条件**。消融实验表明，将 DPT-based 更新模块替换为 CNN（ResNet-18 或 ConvGRU）会导致 Sintel clean EPE 从 1.18 分别飙升至 7.23 和 2.79（Table 5），证实 Transformer 的全局注意力机制是隐式处理大位移、弥补代价体缺失的关键。

### 预测头与上采样

更新模块输出的隐藏状态通过预测头生成混合拉普拉斯分布（Mixture-of-Laplace, MoL）的参数，随后通过凸上采样（convex upsampling）恢复至原始图像分辨率的光流场。整个训练和推理过程固定使用 $T = 5$ 次迭代。

### 架构简化

相较于 RAFT 类方法，WAFT 移除了两个光流特化设计：
- **代价体**：被高分辨率扭曲完全替代。
- **上下文编码器**：消融实验表明其引入额外计算开销但未带来显著性能增益（w/ Context: 1.22 vs WAFT-DAv2-a1: 1.18），可安全移除。

这使得 WAFT 的架构显著简化，仅保留输入编码器与循环更新模块两个核心组件。

## 实验与分析

### 核心性能验证

WAFT 在多个主流光流基准上取得领先或具有竞争力的结果。在 Spring 基准上，WAFT-DINOv3-a2 在所有指标上排名第一，EPE 达到 0.325，WAUC 达到 95.051，分别比此前最优的 DPFlow 降低 0.015 和提高 0.071（Table 3）。在 Sintel 基准上，WAFT-DINOv3-a2 在 clean 分上取得 0.94 EPE 的最优结果，在 final 分上取得 2.02 EPE（Table 2）。在 KITTI 基准上，WAFT-DAv2-a2 在非遮挡像素上排名第一（Fl 2.03），在所有像素上排名第二（Fl 3.31）（Table 2）。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_HTqGE0KcuF/figures/006_Table_3.jpg]]
*Table 3: WAFT ranks 1st on Spring (Mehl et al., 2023) on all metrics. We highlight all SOTA performance. denotes the submissions from the Spring team*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_HTqGE0KcuF/figures/007_Table_2.jpg]]
*Table 2: We report endpoint-error (EPE) on Sintel (Butler et al., 2012), Fl on KITTI (Geiger et al., 2013), and highlight all SOTA performance. On KITTI, WAFT ranks first on non-occluded pixels and second on all pixels. It also achieves state-of-the-art performance on Sintel (clean). We measure the latency on an RTX3090 with batch size 1 and 540p input*

值得注意的是，作者在 Table 6 中明确指出 Sintel 的 “Ambush 1” 序列为异常值——该序列包含极端运动模糊和强遮挡场景。剔除该序列后，WAFT-Twins-a2 在 final 分上的平均 EPE 为 1.639，优于 Flowformer++ 的 1.750。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_HTqGE0KcuF/figures/010_Table_6.jpg]]
*Table 6: We report the endpoint-error (EPE) on all sequences of Sintel (Butler et al., 2012), shown in the format “final-epe (clean-epe)”. We highlight the best result on each sequence*

### 零样本跨数据集泛化

WAFT 展现出优异的零样本泛化能力。在 KITTI(train) 上的跨数据集评估中，WAFT-DAv2-a1 取得 1.00 EPE，WAFT-Twins-a2 取得 1.02 EPE，相比 DPFlow 的 3.37 降低约 70%，相比 Flowformer++ 的 3.37 降低约 70%（Table 4）。这一结果表明，纯翘曲机制在域迁移场景下具有更强的鲁棒性，可能源于其不依赖数据集特定的代价体分布假设。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_HTqGE0KcuF/figures/008_Table_4.jpg]]
*Table 4: WAFT achieves the best cross-dataset generalization on KITTI(train), reducing the error by 11%. We highlight all SOTA performance*

### 消融实验：架构设计的因果验证

Table 5 的系统消融揭示了 WAFT 架构中各组件的因果贡献，所有实验均在零样本设置下进行。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_HTqGE0KcuF/figures/009_Table_5.jpg]]
*Table 5: We report the zero-shot ablation results on Sintel(train) (Butler et al., 2012) and Spring(sub-val) (Mehl et al., 2023; Wang et al., 2024). The effect of changes can be identified through comparisons with the first row. See Section 5.5 for details*

**特征空间翘曲 vs. 图像空间翘曲**：在特征空间执行翘曲不仅精度略优，而且显著降低计算开销。图像空间翘曲需要在每次迭代中重新提取翘曲后图像的特征，而特征空间翘曲直接索引已提取的特征图，避免了重复编码（Section 5.5）。

**高分辨率索引的关键作用**：将特征索引分辨率从 1/8 提升至 1/2，Spring(sub-val) 的 1px 异常率从 1.82 大幅降至 1.43（Table 5）。作为对照，在 1/8 分辨率下使用相关代价体仅得到 1.74，表明高分辨率扭曲索引比低分辨率代价体更有效。这一发现直接支撑了论文的核心主张——内存效率使高分辨率处理成为可能，进而提升精度。

**迭代更新 vs. 直接回归**：在相同元架构下，迭代更新（WAFT-DAv2-a1，Sintel clean EPE 1.18）显著优于单次直接回归（Direct DPT-S，EPE 2.36），验证了循环更新模块的必要性（Table 5）。

**DPT 架构的不可替代性**：将基于 DPT 的循环更新模块替换为 CNN 架构导致灾难性性能下降——Res18 变体在 Sintel clean 上的 EPE 从 1.18 飙升至 7.23，ConvGRU 变体升至 2.79（Table 5）。这表明视觉 Transformer 的全局注意力机制对于处理大位移光流至关重要，CNN 的局部感受野无法有效替代。

**上下文编码器可安全移除**：添加上下文编码器后，Sintel clean EPE 为 1.22，与基线 WAFT-DAv2-a1 的 1.18 相比无显著差异（Table 5）。这验证了 WAFT 相比 RAFT 类架构的简化是合理的——上下文编码器引入额外计算开销但未带来性能增益。

### 效率分析

WAFT 的内存效率优势在 Table 1 中量化呈现。在 RTX A6000 上以 batch size 1 进行训练时，WAFT-Twins-a2 在 1/8、1/4、1/2 分辨率下的内存消耗分别为 7.0 GiB、7.6 GiB、9.2 GiB。相比之下，基于部分代价体的 SEA-RAFT 在 1/8 分辨率下即消耗 14.1 GiB，在 1/4 分辨率下升至 25.8 GiB，在 1/2 分辨率下直接显存溢出。这一差距源于代价体构建的计算复杂度随分辨率二次增长，而翘曲操作仅在对应像素位置进行单点索引。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_HTqGE0KcuF/figures/004_Table_1.jpg]]
*Table 1: We profile the training memory cost with batch size 1 on an RTX A6000. Our warping method significantly reduces the cost*

在推理延迟方面，所有测量均在 RTX3090 上以 batch size 1、540p 输入进行。WAFT 比 Flowformer++ 快 1.3 倍，比 CCMR+ 快 4.1 倍（Abstract）。

### 失败模式与局限性

尽管整体性能优异，WAFT 在特定困难场景下暴露出纯翘曲机制的局限性。在 Sintel 的 “Ambush 1” 序列（极端运动模糊）上，WAFT 的表现不如部分基于代价体的方法（Table 6）。这说明当对应像素的特征因模糊而严重退化时，单一对应点索引可能不足以消除匹配歧义——代价体提供的局部邻域信息在此类场景下仍具有互补价值。此外，WAFT 高度依赖视觉 Transformer 架构，若缺乏大规模预训练，CNN 变体的性能急剧下降（Table 5），这限制了该方法在计算资源受限场景下的直接部署。

## 方法谱系与知识库定位

### 从代价体到纯扭曲：一条被忽视的路径

迭代光流方法长期由代价体（cost volume）范式主导。以 **RAFT** (Teed & Deng, ECCV 2020) 为里程碑，其核心设计是：在固定低分辨率（通常1/8）特征图上构建4D代价体，通过ConvGRU循环单元迭代查询该代价体以更新光流。后续工作沿着两条路径改进：（1）提高效率，如 **SEA-RAFT** (Wang et al., ECCV 2024) 在局部邻域内动态构建部分代价体，以降低内存开销；（2）引入Transformer，如 **Flowformer++** (Shi et al., CVPR 2023) 用掩码代价体替代全代价体以适配注意力机制。然而，这些方法始终未脱离“显式构建视觉相似度矩阵”这一基本假设。

WAFT的定位是**彻底放弃代价体，回归纯扭曲（warping）操作**。这一选择并非全新——经典的 **PWC-Net** (Sun et al., CVPR 2018) 也曾使用扭曲，但仅作为代价体构建前的预处理步骤，而非替代品。WAFT的独特之处在于将扭曲提升为唯一的特征匹配机制：通过当前光流估计从第二帧特征图中直接索引对应像素的特征向量（$\mathsf{Warp}(f_{\mathrm{cur}})_p = F(I_2)_{p + (f_{\mathrm{cur}})_p}$），完全跳过显式相似度计算。这意味着匹配信息是“隐式”的——网络必须从单个对应点的特征差异中推断位移修正量，而非从预计算的相似度分布中读取。

### 架构简化的因果链条

WAFT的简化并非表面工程，而是一条因果链条的结果。代价体的移除直接消除了训练时的内存瓶颈：在RTX A6000上以batch size 1测试，WAFT-Twins-a2在1/2分辨率下仅需9.2 GiB显存，而SEA-RAFT在1/4分辨率下已达25.8 GiB，在1/2分辨率下直接内存溢出（Table 1）。这一内存释放使得**高分辨率特征索引**成为可能——这是WAFT性能提升的关键因果旋钮。消融实验（Table 5）表明，将索引分辨率从1/8提升至1/2，Spring子验证集的1px异常率从1.82骤降至1.43，边界清晰度显著改善（Figure 3）。

代价体的移除还带来第二个连锁效应：**上下文编码器（context encoder）变得冗余**。在RAFT类架构中，上下文编码器为ConvGRU提供场景先验以辅助代价体查询；当查询操作被扭曲替代后，消融实验显示上下文编码器的加入（Sintel clean EPE 1.22）与移除（1.18）相比无显著差异，反而增加计算开销。WAFT因此成为当前主流迭代方法中架构最简洁的设计之一。

### 视觉Transformer的不可替代性

WAFT的纯扭曲策略有一个硬性前提：更新模块必须具备全局感受野以处理大位移。扭曲仅提供单点对应信息，缺乏代价体固有的邻域搜索能力，因此网络必须通过注意力机制隐式建模长程依赖。实验证据极为明确：将DPT-Small更新模块替换为ResNet-18时，Sintel clean EPE从1.18暴增至7.23；替换为ConvGRU时升至2.79（Table 5）。这表明纯扭曲+CNN的组合无法收敛到有效解，视觉Transformer是该方法成立的**必要条件**。

WAFT采用的DPT-Small（patch size 8，位置嵌入分辨率224×224）在计算开销与全局建模能力之间取得平衡。这一设计与 **DPFlow** 等双金字塔方法形成对比：后者通过多尺度金字塔显式处理大位移，而WAFT依赖Transformer的隐式全局注意力。

### 适用边界与失效模式

WAFT在Spring基准上以全部指标排名第一（1px 3.182, EPE 0.325, WAUC 95.051），在KITTI非遮挡像素上排名第一、全部像素排名第二，在Sintel clean上达到SOTA。然而，其适用边界同样清晰：

1. **极端模糊与强遮挡**：在Sintel的“Ambush 1”序列（高速运动模糊+强遮挡）上，WAFT-Twins-a2的final EPE为32.89，显著劣于Flowformer++的26.93（Table 6）。作者明确指出该序列为异常值。这表明当单点对应完全不可靠时，纯扭曲缺乏代价体提供的邻域备选匹配信息来消除歧义。

2. **预训练依赖**：WAFT的性能高度依赖输入编码器的预训练质量。论文测试了三种骨干：ImageNet预训练的Twins-SVT-Large、深度预训练的DAv2-S、无监督预训练的DINOv3-ViT-S，性能随预训练强度递增。若缺乏强预训练，CNN变体的灾难性失败暗示纯扭曲方法可能不适用于小数据场景。

3. **任务泛化未验证**：当前仅在光流任务上验证。向立体匹配、场景流等任务的迁移需要回答：扭曲的单点索引在无时序信息的双目几何约束下是否仍然充分？

### 开放问题

1. **鲁棒性边界**：在严重遮挡、无纹理区域或高速运动模糊场景下，是否需要引入轻量级不确定性估计或辅助代价信息作为“安全网”？当前Ambush 1的失效表明纯扭曲存在系统性盲区。

2. **架构扩展性**：进一步扩展DPT的规模（如DPT-Base/Large）或采用光流自监督预训练目标，能否继续解锁更高精度？当前固定5次迭代是否为最优？动态终止策略可能进一步平衡效率与精度。

3. **跨任务迁移**：WAFT的元架构（输入编码器+Transformer循环更新模块+扭曲索引）是否可直接迁移到立体视差估计或多视角立体，并保持高效与高精度？这需要验证扭曲操作在无时序线索的双目/多目几何中是否足以替代代价体的显式匹配。

4. **与经典理论的对齐**：论文提及Brox et al. (2004) 将扭曲与循环更新的组合框架化为不动点迭代算法，但未深入展开。这一理论视角可能为理解纯扭曲方法的收敛性和误差传播提供更严格的分析工具。

## 原文 PDF

![[paperPDFs/ICLR_2026/WAFT_Warping_Alone_Field_Transforms_for_Optical_Flow.pdf]]
