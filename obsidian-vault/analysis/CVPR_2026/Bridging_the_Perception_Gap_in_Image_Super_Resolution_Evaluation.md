---
title: Bridging the Perception Gap in Image Super-Resolution Evaluation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Bridging_the_Perception_Gap_in_Image_Super_Resolution_Evaluation.pdf
project_link: "http://color.cvc.uab.cat/rqi/"
code_link: null
aliases:
- RQIR
- BPGISRE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将SR评估从绝对质量预测转变为相对质量比较任务：训练时，不再仅以原始参考图像为标准，而是从任意失真图像中构建密集配对，以MOS差值作为监督信号，让模型学习有序的非对称相对质量差异。评估时，固定输入顺序（SR输出在前，GT在后），模型输出单个相对质量分数，从而使得评价既利用参考又对GT质量鲁棒，且能区分细微差异。
primary_logic: 通过构造任意失真图像之间的相对质量差异训练（而非仅与理想参考比较），并采用Huber损失的回归学习，无需专门收集SR数据或设计新架构，即可使现有IQA模型获得与人类感知高度一致的SR评估能力，并可进一步作为感知损失优化SR模型。
claims:
- 在涵盖7种SOTA SR模型和5个基准的用户研究中，RQI在DIV2K、RealSR、DRealSR、Set5&Set14上的SRCC、PLCC和Win Rate全面优于或可比肩现有最佳指标（Table 1）。
- 在三个IQA模型（AHIQ, MANIQA, TOPIQ）和三个训练集上，使用RQI框架训练相比传统FR训练一致提升SRCC，在DRealSR上平均提升达0.146（Table 2）。
- RQI在四个公共IQA基准（含SR-IQA和通用IQA）上零样本泛化性能稳定，且在多个基准上取得最佳或次佳一致性（Table 3）。
- 定性比较中，RQI正确应对了现有指标在失真偏好、缺乏参考、GT质量不佳和细微差异等四种挑战场景下的失败案例（Figure 3, Figure 8-10）。
---

# Bridging the Perception Gap in Image Super-Resolution Evaluation

> [!tip] 核心洞察
> 通过构造任意失真图像之间的相对质量差异训练（而非仅与理想参考比较），并采用Huber损失的回归学习，无需专门收集SR数据或设计新架构，即可使现有IQA模型获得与人类感知高度一致的SR评估能力，并可进一步作为感知损失优化SR模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | 弥合图像超分辨率评价中的感知差距 |
| 英文题名 | Bridging the Perception Gap in Image Super-Resolution Evaluation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2503.13074) · [Project](http://color.cvc.uab.cat/rqi/) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Relative Quality Index (RQI) |
| Dataset | User Study, SRIQA-Bench, BSD-SR |

> [!tip] 效果简介
> - User Study (DIV2K) 上，SRCC 0.744 (RQI) vs 0.613 (DeQA-Score, best existing) / 0.554 (MANIQA original) (+0.131 / +0.190)。
> - User Study (RealSR) 上，SRCC 0.504 vs 0.452 (DeQA-Score) / 0.187 (MANIQA original) (+0.052 / +0.317)。
> - User Study (DRealSR) 上，SRCC 0.529 vs 0.437 (DeQA-Score) / 0.284 (MANIQA original) (+0.092 / +0.245)。

## 概要

### 问题背景

图像超分辨率（SR）模型的评价长期依赖图像质量评价（IQA）指标，然而现有指标在评估现代SR模型时暴露出与人类感知判断的显著不一致。这一“感知差距”源于四个结构性瓶颈：

1. **失真导向的全参考指标（PSNR、SSIM）偏好平滑输出**：这类指标通过回归到多个可行解的平均值来评估质量，导致其天然偏好模糊但像素误差小的结果，与人类对纹理细节的偏好相悖。
2. **感知导向的全参考指标（LPIPS、DISTS）对真实参考质量敏感**：当真实参考（GT）图像本身质量欠佳时，这些指标会做出矛盾评价——惩罚那些生成比GT感知质量更高的SR模型。
3. **无参考指标缺乏可靠参照**：NIQE、PI、Clip-IQA等指标在没有参考图像的情况下，无法有效评估纹理和结构保真度，尤其在语义细微变化时容易失效。
4. **高质量图像的细微差异难以区分**：随着SR输出质量不断提升，指标在区分高质量图像的细微感知差异方面能力不足。

### 核心方法：相对质量指数（RQI）

本文提出**相对质量指数（Relative Quality Index, RQI）**框架，将SR评估从绝对质量预测转变为相对质量比较任务。其核心创新体现在三个设计维度：

- **训练范式转换**：不再仅以原始参考图像为标准，而是从任意失真图像中构建密集配对，以MOS差值作为监督信号，让模型学习有序的非对称相对质量差异。
- **非对称架构**：RQI输出取决于输入顺序，满足 $f_{RQI}(I_i, I_j) = -f_{RQI}(I_j, I_i)$，评估时固定SR输出在前、GT在后，输出单个相对质量分数。
- **损失函数设计**：采用Huber损失拟合相对质量差异，提供平滑梯度以适应正负值及小差值场景。

该框架无需专门收集SR数据或设计新架构，仅利用已有IQA数据集训练，即可使现有IQA模型获得与人类感知高度一致的SR评估能力，并可作为感知损失优化SR模型。

### 方法谱系与知识库定位

RQI在图像质量评价领域的方法谱系中占据独特位置：

- **相对于失真导向全参考指标**（**PSNR**、**SSIM** (Wang et al., TIP 2004)）：RQI通过相对质量比较避免了回归到平均解导致的平滑偏好，在感知一致性上显著超越。
- **相对于感知导向全参考指标**（**LPIPS** (Zhang et al., CVPR 2018)、**DISTS** (Ding et al., TIP 2020)）：RQI通过允许参考图像包含失真，解决了GT质量不佳时的评价失效问题。
- **相对于无参考指标**（**NIQE** (Mittal et al., SPL 2013)、**Clip-IQA** (Wang et al., AAAI 2023)、**MANIQA** (Yang et al., CVPRW 2022)）：RQI保留了参考信息以评估保真度，同时不假设参考图像为理想质量。
- **相对于非对称全参考指标**（**AFINE**）：RQI无需专门收集SR数据，训练数据来源更广泛，框架更轻量。
- **相对于基于LLM的评价模型**（**DeQA-Score**）：RQI在多数场景下取得更优或可比的一致性，且计算成本更低。

### 主要结果

RQI在涵盖7种SOTA SR模型和5个基准的用户研究中表现出色（Table 1）：

| 数据集 | RQI SRCC | 最佳现有指标 SRCC | 提升幅度 |
|--------|----------|-------------------|----------|
| DIV2K | 0.744 | 0.613 (DeQA-Score) | +0.131 |
| RealSR | 0.504 | 0.452 (DeQA-Score) | +0.052 |
| DRealSR | 0.529 | 0.437 (DeQA-Score) | +0.092 |
| Set5&Set14 | 0.664 | 0.699 (DeQA-Score) | -0.035 |

在三个IQA模型（AHIQ、MANIQA、TOPIQ）和三个训练集上，RQI框架训练相比传统FR训练一致提升SRCC，在DRealSR上平均提升达0.146（Table 2）。在四个公共IQA基准（含SR-IQA和通用IQA）上，RQI零样本泛化性能稳定，在多个基准上取得最佳或次佳一致性（Table 3）。定性比较中，RQI正确应对了现有指标在失真偏好、缺乏参考、GT质量不佳和细微差异四种挑战场景下的失败案例（Figure 3）。

### 局限性与开放问题

RQI分数仅在共享同一参考图像时才有意义，无法用于跨内容质量比较；其主要衡量感知质量而非像素级保真度；在极低分辨率数据集上性能略逊于基于大规模预训练LLM的DeQA-Score。未来方向包括：将RQI框架泛化到其他图像恢复任务、设计更原则性的保真度度量、探索MOS差值的非线性建模，以及研究其在扩散模型训练中的应用。



### 图像超分辨率评估的感知鸿沟

图像超分辨率（SR）领域在过去十年取得了显著进展，从早期的卷积网络到如今的扩散模型和生成式方法，模型输出的视觉质量持续提升。然而，一个关键问题长期被忽视：**现有的图像质量评价（IQA）指标是否仍能准确区分现代SR模型的感知性能？**

答案是否定的。一项覆盖7种SOTA SR模型和5个基准数据集的用户研究表明，传统指标与人类感知判断之间存在显著且系统性的不一致。这种不一致并非随机误差，而是根植于现有指标设计中的结构性缺陷，具体体现在四个维度：

**挑战一：失真导向指标偏好平滑输出。** PSNR和SSIM（Wang et al., TIP 2004）等全参考（FR）指标以像素级保真度为目标，但SR是一个病态逆问题——单个低分辨率输入对应多个可行的高分辨率解。失真导向指标倾向于回归到这些可行解的平均，从而系统性地偏好平滑、模糊的输出，与人类对纹理丰富度和细节真实感的偏好背道而驰。用户研究数据证实，PSNR和SSIM在多个SR测试集上呈现与人类感知的**负相关**。

**挑战二：感知全参考指标在GT质量不佳时失效。** LPIPS（Zhang et al., CVPR 2018）和DISTS（Ding et al., TIP 2020）等感知导向的FR指标通过深度特征比较来衡量感知距离，在一定程度上缓解了平滑偏好问题。然而，它们隐含地假设参考图像（GT）具有理想质量。在真实世界SR场景中，GT图像本身可能包含噪声、模糊或压缩伪影。此时，一个能生成比GT更清晰、更真实纹理的SR模型，反而会被这些指标判定为质量更差——因为它们将GT视为不可逾越的上限（Figure 10）。

**挑战三：无参考指标缺乏可靠参照。** NIQE（Mittal et al., SPL 2013）、PI、Clip-IQA（Wang et al., AAAI 2023）和MANIQA（Yang et al., CVPRW 2022）等无参考（NR）指标试图在不依赖参考图像的情况下评估质量。但当SR模型仅引入细微的语义结构变化（如纹理模式的微小偏移）时，这些指标因缺乏参照而无法做出正确判断（Figure 9）。它们可以识别明显的失真，却难以区分高质量输出之间的精细感知差异。

**挑战四：高质量输出的细微差异难以区分。** 随着SR模型质量的整体提升，不同SOTA方法之间的感知差异变得越来越细微。现有指标在区分这些“高质量区间”内的细微差别时表现乏力——它们要么将所有高质量输出赋予相似的分数，要么做出与人类偏好不一致的排序。

### 现有方法的局限与本文动机

上述四个挑战揭示了现有IQA范式在SR评估中的根本瓶颈：**绝对质量预测的框架假设与SR任务的实际需求之间存在错配。** 无论是FR还是NR方法，都试图为单张图像赋予一个绝对的质量分数，而该分数的标定依赖于一个理想化的参考标准（FR中的完美GT，NR中的统计先验）。当这个参考标准本身不可靠，或者待评估图像的质量差异超出了指标的判别粒度时，绝对预测框架就会失效。

已有工作尝试解决部分问题。AFINE提出了非对称FR评估，但其训练需要专门收集SR特定的比较数据，成本高昂且泛化性受限。DeQA-Score利用大规模预训练LLM的视觉理解能力，在部分场景下表现优异，但其性能依赖于模型规模和预训练数据，且在低分辨率场景外的优势并不稳定。

本文的核心动机在于：**能否设计一种通用且轻量的评估框架，在不依赖SR特定数据采集的前提下，系统性地弥合SR评估中的感知差距？** 关键洞察是：与其让模型学习“这张图像有多好”的绝对判断，不如让模型学习“这两张图像中哪一个更好”的相对比较——这正是人类感知判断的基本运作方式。



## 核心方法与创新机理

RQI框架的核心创新在于将图像超分辨率评价从**绝对质量预测**范式转变为**相对质量比较**范式。这一转变通过三个关键的“changed slots”实现，直接回应了现有指标与人类感知之间的根本性不一致。

### 从绝对评分到相对差异：训练样本构造的重构

传统全参考图像质量评价（FR-IQA）指标的训练范式存在一个隐含假设：参考图像是理想无失真的，模型学习的是目标图像相对于该理想参考的绝对质量分数 $q_i$。这一假设在SR场景下暴露出两个致命缺陷：其一，当真实参考（GT）本身质量欠佳时（如RealSR、DRealSR中的模糊或噪声GT），模型被迫将低质量GT视为“满分标准”，导致评分失真；其二，随着SR模型输出质量普遍提升，绝对分数难以捕捉不同模型输出之间的细微感知差异。

RQI从根本上解构了这一范式。其训练样本构造策略可概括为：

- **密集配对**：对于同一场景下的 $n$ 张失真图像（包括GT在内），不再仅以原始参考图像为中心构造 $n-1$ 个图像对 $\{I_0, I_i\}$，而是从任意两张失真图像中构造多达 $n(n-1)$ 个有序对 $\{I_i, I_j\}, i \neq j$。
- **相对差异作为监督信号**：训练标签不再是单一的MOS值 $q_i$，而是两张图像MOS值的差值 $q_i - q_j$。这一差值可正可负，天然编码了“目标图像相对于参考图像更好还是更差”的相对关系。
- **参考图像质量无关性**：由于训练时允许任意失真图像（包括质量较差的图像）充当参考，模型学会的是“相对质量差异”这一通用判断能力，而非对特定参考图像质量的依赖。这使得RQI在评估时天然对GT质量不佳的场景具有鲁棒性。

这一设计使得RQI无需专门收集SR训练数据即可获得对SR评估的强泛化能力——论文强调，RQI仅使用现有IQA数据集（如Kadid-10K、PIPAL）进行训练，而无需像**AFINE**那样专门构建SR数据集。

### 非对称架构：打破对称性约束

传统FR-IQA指标（如SSIM、LPIPS、DISTS）在架构上通常是对称的：$f(I_i, I_{ref}) = f(I_{ref}, I_i)$。这种对称性在衡量“两张图像之间的相似度”时是自然的，但在评估“$I_i$ 是否比 $I_{ref}$ 更好”时则成为障碍——它无法区分输入顺序所隐含的比较方向。

RQI明确引入了**非对称性**：$RQI(I_i, I_j) = -RQI(I_j, I_i)$。这意味着模型的输出取决于输入顺序，从而能够回答“第一张图像相对于第二张图像的质量如何”这一方向性问题。在评估推理阶段，RQI固定输入顺序为 $(I_{HR}, I_{GT})$，输出标量分数 $s_i = f_{RQI}(I_{HR}, I_{GT})$，分数越高表示SR输出相对于GT的感知质量越好。这一设计使得RQI既能利用参考图像提供结构保真度信息，又不会因为GT质量不佳而产生矛盾评价——当SR输出质量确实优于GT时，RQI可以输出正值。

### Huber损失：适配相对差异的回归目标

传统IQA训练通常采用L1或L2损失拟合绝对质量分数。然而，当训练目标变为可正可负的相对质量差异 $q_i - q_j$ 时，损失函数的选择变得至关重要。RQI采用Huber损失：

$$L = \left\{ \begin{array} { l l } { \frac { 1 } { 2 } \left( \hat { y } _ { i j } - ( q _ { i } - q _ { j } ) \right) ^ { 2 } , \mathrm { i f ~ } | \hat { y } _ { i j } - ( q _ { i } - q _ { j } ) | \leq \delta , } \\ { \delta \left( | \hat { y } _ { i j } - ( q _ { i } - q _ { j } ) | - \frac { 1 } { 2 } \delta \right) , \mathrm { o t h e r w i s e } . } \end{array} \right.$$

Huber损失的核心优势在于：对于较小的预测误差（$\leq \delta$），它表现为平滑的L2损失，提供稳定梯度；对于较大的误差，它退化为线性L1损失，避免离群值对训练的主导。这一特性恰好适配RQI的训练场景——密集配对产生的相对差异标签中存在大量小差值样本（两张质量相近的图像），Huber损失的平滑梯度有助于模型精细区分这些细微差异。消融实验（Table 6）证实，Huber损失在RQI训练中一致优于L1和L2损失。

### 创新定位：轻量、通用、即插即用

RQI并非一个全新的IQA模型，而是一个**训练框架**。它可以应用于任意现有的双输入IQA架构（论文验证了AHIQ、MANIQA、TOPIQ三种架构），仅需移除最后的激活层以允许输出正负值，并改用Huber损失进行相对差异回归。这一“即插即用”的特性使得RQI具有高度通用性——Table 2显示，在三个IQA模型和三个训练集上，RQI框架相比传统FR训练一致提升SRCC，在DRealSR上平均提升达0.146，在Set5&Set14上平均提升达0.138。



### 核心思路：从绝对评分到相对比较的范式转换

RQI 框架的核心洞察在于将图像超分辨率（SR）评价从**绝对质量预测**转变为**相对质量比较**任务。传统全参考图像质量评价（FR-IQA）方法训练时仅以原始无失真参考图像（$I_0$）为标准，学习预测失真图像 $I_i$ 的绝对质量分数 $q_i$。这一范式存在三个根本性局限：其一，回归到多个可行解的平均导致偏好平滑/模糊输出，与人类感知偏好相悖；其二，假设参考图像为理想质量，当真实参考（GT）图像本身质量欠佳时评价失效；其三，难以区分高质量 SR 输出之间的细微感知差异。

RQI 通过两项关键设计打破上述限制：

1. **任意失真图像均可作为参考**：训练时不再假设参考图像无失真，而是“大胆地”将任意失真图像（包括严重失真的图像）作为参考，使模型学习任意图像对之间的相对质量关系。
2. **以 MOS 差值作为监督信号**：对于同一场景下的任意两个失真图像 $I_i$ 和 $I_j$，直接使用其平均主观意见分（MOS）的差值 $q_i - q_j$ 作为训练标签，该差值可正可负，完整刻画了图像对之间的有序质量关系。

### 模块架构与数据流

RQI 框架由四个核心模块构成，形成完整的训练-评估-应用闭环：

**模块一：训练数据构造模块**

从已有 IQA 数据集（如 Kadid-10K、PIPAL）中，为每个场景构造所有失真图像之间的成对组合 $\{I_i, I_j\}, i \neq j$，并计算对应的 MOS 差值标签 $q_i - q_j$，随后归一化到 $[-1, 1]$ 区间。与传统 FR-IQA 仅使用 $n$ 个 $\{I_0, I_i\}$ 对相比，RQI 在每个场景中构造了 $n(n-1)$ 个密集配对（见 Figure 2），覆盖了更复杂的质量比较情形，迫使模型学习更精细的相对质量判别能力。

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/003_Figure_2.jpg]]
*Figure 2: The proposed RQI training scheme differs from traditional FR-IQA training scheme in three aspects: 1. RQI is asymmetric. 2. RQI calculates relative discrepancy. 3. Denser image pairs are constructed to facilitate challenging predictions*

**模块二：双输入相对质量回归模型**

基于现有 IQA 架构（如 MANIQA、AHIQ、TOPIQ）进行改造：将模型修改为接受目标图像和参考图像的双输入结构，移除最后的激活层以允许输出正负值。训练目标为使用 Huber 损失拟合预测的相对质量差异 $\hat{y}_{ij}$ 与真实 MOS 差值：

$$L = \left\{ \begin{array} { l l } { \frac { 1 } { 2 } \left( \hat { y } _ { i j } - ( q _ { i } - q _ { j } ) \right) ^ { 2 } , \mathrm { i f ~ } | \hat { y } _ { i j } - ( q _ { i } - q _ { j } ) | \leq \delta , } \\ { \delta \left( | \hat { y } _ { i j } - ( q _ { i } - q _ { j } ) | - \frac { 1 } { 2 } \delta \right) , \mathrm { o t h e r w i s e } . } \end{array} \right.$$

Huber 损失的选择（消融实验 Table 6 验证其优于 L1/L2）提供了平滑梯度，对正负值及小差值均具有鲁棒性。模型本身是**非对称**的，即 $f_{RQI}(I_i, I_j) = -f_{RQI}(I_j, I_i)$，输出严格依赖于输入顺序，这一性质使得模型能够捕捉有序的相对质量差异。

**模块三：评估推理模块**

评估时固定输入顺序：SR 输出图像 $I_{HR}$ 在前，GT 图像 $I_{GT}$ 在后，模型输出标量分数：

$$s _ { i } = f _ { R Q I } ( I _ { H R } , I _ { G T } )$$

分数 $s_i$ 越高表示 SR 图像相对于 GT 的感知质量越好。对高分辨率图像，采用多尺度随机裁剪并取平均的策略（消融实验 Table 5 验证多尺度评估在 DIV2K 和 DRealSR 上带来明显增益），以同时捕捉纹理细节和结构语义。

**模块四：SR 训练辅助损失模块（可选）**

将 RQI 分数作为额外的感知损失项集成到 SR 模型训练中：

$$\mathcal { L } = \mathcal { L } _ { o r i } + \lambda \cdot s$$

其中 $\lambda$ 取负值（如 -0.1），鼓励模型生成更高感知质量的输出。该模块以端到端方式引导 SR 模型优化，在 SwinIR、SeeSR、PiSA-SR 等模型上均验证了有效性（Table 4, Figure 4）。

### 框架的关键性质

RQI 框架的设计赋予其三个区别于传统指标的关键性质：

1. **利用参考同时对 GT 质量鲁棒**：评估时使用 GT 作为参考，保留了保真度评估能力；但训练时模型已见过大量失真图像作为参考的情形，因此当 GT 质量欠佳时不会产生矛盾评价（Figure 10 对比了 LPIPS/DISTS 在此场景下的失败）。
2. **细粒度感知差异区分能力**：密集配对训练使模型接触到大量质量差异微小的图像对，从而具备区分高质量 SR 输出之间细微差异的能力。
3. **架构无关的通用性**：RQI 是一种训练方案而非特定架构，可直接适配于多种现有 IQA 模型。Table 2 显示在 AHIQ、MANIQA、TOPIQ 三个模型和多个训练集上，使用 RQI 框架训练相比传统 FR 训练一致提升 SRCC，在 DRealSR 上平均提升达 0.146。

### 重要使用约束

RQI 分数仅在**共享同一参考图像**时才有意义，无法用于不同内容图像之间的跨图像质量比较。此外，RQI 主要衡量感知质量而非像素级保真度，对于纹理精细重建的绝对保真度评估仍有待探索。



### 训练数据构造模块

RQI的核心创新在于将SR评估从绝对质量预测转变为相对质量比较任务。传统FR-IQA训练方案仅使用原始参考图像与失真图像构成图像对 $\{I_0, I_i\}$，训练标签为绝对质量分数 $q_i$。RQI则从已有IQA数据集（如Kadid-10K、PIPAL）中，为每个场景构造所有成对失真图像的相对质量标签——即任意两个失真图像 $I_i$ 与 $I_j$（$i \neq j$）均可构成图像对，训练标签为MOS差值 $q_i - q_j$，并可正可负。这一设计使得训练样本数量从 $n$ 对扩展到 $n(n-1)$ 对，覆盖更复杂的质量比较场景，同时允许参考图像本身包含失真，从而在评估时对GT质量不高的情况具有鲁棒性。

### 双输入相对质量回归模型

RQI基于现有IQA架构（如MANIQA、AHIQ、TOPIQ）进行改造：模型接受目标图像和参考图像双输入，移除最后的激活层以输出正负值，直接回归预测相对质量差异。训练目标采用Huber损失：

$$L = \left\{ \begin{array} { l l } { \frac { 1 } { 2 } \left( \hat { y } _ { i j } - ( q _ { i } - q _ { j } ) \right) ^ { 2 } , \mathrm { i f ~ } | \hat { y } _ { i j } - ( q _ { i } - q _ { j } ) | \leq \delta , } \\ { \delta \left( | \hat { y } _ { i j } - ( q _ { i } - q _ { j } ) | - \frac { 1 } { 2 } \delta \right) , \mathrm { o t h e r w i s e } . } \end{array} \right.$$

其中 $\hat{y}_{ij}$ 为模型预测的相对质量差异，$q_i - q_j$ 为真实MOS差值，$\delta$ 为平滑阈值。Huber损失相比L1和L2损失提供更平滑的梯度，对小误差具有鲁棒性，且能适应正负值及小差值场景。消融实验（Table 6）验证了Huber损失在RQI训练中优于L1和L2损失。

### 评估推理模块

评估时，固定输入顺序——SR输出 $I_{HR}$ 在前，GT图像 $I_{GT}$ 在后——模型输出标量分数：

$$s _ { i } = f _ { R Q I } ( I _ { H R } , I _ { G T } )$$

分数 $s_i$ 表示SR图像相对于GT的感知质量，分数越高感知质量越好。由于RQI的非对称性（$f(I_i, I_j) = -f(I_j, I_i)$），固定输入顺序是保证评估一致性的关键。对于高分辨率图像，采用多尺度随机裁剪并取平均的策略，以同时捕捉纹理细节和结构语义。消融实验（Table 5）表明，多尺度评估相比单尺度评估在DIV2K和DRealSR等高分辨率数据集上带来明显增益。

### SR训练辅助损失模块（可选）

RQI分数可进一步作为感知损失项，以端到端方式引导SR模型生成更高质量的输出：

$$\mathcal { L } = \mathcal { L } _ { o r i } + \lambda \cdot s$$

其中 $\mathcal{L}_{ori}$ 为原始SR训练损失（如L1或GAN损失），$s$ 为RQI评估分数，$\lambda$ 取负值（如-0.1）以鼓励模型朝更高感知质量方向优化。实验表明，将RQI作为辅助损失训练SwinIR、SeeSR、PiSA-SR，在DeQA-Score等指标上均获得最佳感知质量，且视觉对比显示结构保真度和细节真实感均有提升（Table 4, Figure 4）。

### 方法核心差异总结

RQI训练方案与传统FR-IQA训练方案存在三个本质差异（Figure 2）：
1. **非对称性**：输出取决于输入顺序，$f(I_i, I_j) \neq f(I_j, I_i)$；
2. **相对差异**：训练标签为MOS差值而非绝对质量分数；
3. **密集配对**：任意两个失真图像均可构成训练对，覆盖更复杂的质量比较场景。

### 补充图表

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/002_Figure_1.jpg]]
*Figure 1: Visual illustration of how SR evaluation challenges current metrics in different aspects. Zoom in for better comparison*



## 实验与关键发现

### 用户感知一致性主实验

为系统评估RQI框架的有效性，作者在DIV2K、RealSR、DRealSR、Set5&Set14四个基准上组织了大规模用户研究，涵盖7种SOTA SR模型（包括基于GAN、扩散模型和自回归模型的方法）的生成结果。Table 1报告了各指标与人类主观评分的SRCC、PLCC和Win Rate三项一致性指标。

**整体表现。** RQI在绝大多数场景下取得了最优或次优的一致性。在DIV2K上，RQI的SRCC达到0.744，较此前最佳指标DeQA-Score（0.613）提升0.131；在更具挑战性的真实场景数据集RealSR和DRealSR上，RQI分别取得0.504和0.529的SRCC，均显著优于所有现有指标（Table 1）。在Set5&Set14上，RQI的SRCC为0.664，略低于DeQA-Score（0.699），但仍大幅领先其他指标——这一差距可能与RQI输入分辨率限制及DeQA-Score的大规模预训练优势有关。

**现有指标的失效模式。** Table 1的结果清晰揭示了论文提出的四个核心挑战：失真导向的全参考指标（PSNR、SSIM）在所有数据集上与人类感知呈负相关或弱相关，验证了其偏好平滑/模糊输出的固有问题；感知导向指标LPIPS和DISTS在GT质量较差的RealSR和DRealSR上性能急剧下降；无参考指标（NIQE、PI、Clip-IQA、MANIQA）虽在部分场景表现尚可，但因缺乏可靠参考，在结构保真度评估上存在系统性偏差。

### RQI框架有效性验证

Table 2通过将三种不同IQA架构（AHIQ、MANIQA、TOPIQ）分别在传统FR训练和RQI训练方案下进行对比，隔离了框架本身的增益。核心发现如下：

- **一致且显著的提升。** 在所有模型-数据集组合中，RQI训练（下标R）均带来SRCC提升。跨数据集平均提升为：DIV2K +0.077，RealSR +0.085，DRealSR +0.146，Set5&Set14 +0.138。DRealSR上的最大增益（+0.146）表明，RQI对GT质量不佳的真实场景尤为有效——这正是传统FR训练假设“参考图像为理想质量”所无法处理的。
- **数据集的互补效应。** 在PIPAL上训练的MANIQA_RQI取得了最优整体一致性（DIV2K 0.744，RealSR 0.504，DRealSR 0.529），验证了PIPAL中丰富的失真类型和精细的MOS标注对学习复杂相对质量关系的重要性。Kadid-10K训练的模型在Set5&Set14上表现最佳（0.664），可能与Kadid-10K包含更多传统失真类型有关。
- **架构无关性。** RQI框架在AHIQ、MANIQA、TOPIQ三种架构上均有效，表明其核心思想——将绝对质量预测转化为相对质量比较——具有通用性，不依赖于特定网络设计。

### 泛化性评估

Table 3展示了RQI在四个公共IQA基准上的零样本泛化性能，包括三个SR-IQA数据集（BSD-SR、QADS、SRIQA-Bench）和一个通用IQA数据集（Kadid-10K）。RQI在所有基准上表现稳定，在SRIQA-Bench上取得最佳SRCC_all（0.733），在BSD-SR上取得最佳SRCC_mean（0.901）。值得注意的是，尽管RQI仅通过相对质量差异训练，其在通用IQA任务上也展现了竞争性的泛化能力，表明相对质量比较的学习范式捕捉到了跨任务的感知质量判别能力。

### 定性鲁棒性分析

Figure 3通过四个典型挑战场景的案例对比，直观展示了RQI相对于现有指标的鲁棒性：

1. **失真偏好问题。** 当SR输出纹理丰富但包含轻微伪影时，PSNR/SSIM偏好平滑的模糊结果，而RQI正确识别了感知质量更高的输出。
2. **缺乏参考问题。** 无参考指标（NIQE、PI、Clip-IQA）在语义细微变化时无法给出正确评价（另见Figure 9），RQI通过引入参考图像有效解决了这一局限。
3. **GT质量不佳。** 当GT图像本身存在模糊或噪声时，LPIPS/DISTS将超越GT质量的SR输出错误地判定为低质量（另见Figure 10），而RQI通过非对称相对比较避免了这一陷阱。
4. **细微差异区分。** 对于两个高质量SR输出之间的细微感知差异，RQI能够给出与人类判断一致的相对排序，而多数现有指标难以区分。

### 消融实验

**失真配对策略。** Table 5对比了RQI_full（跨失真类型配对）和RQI_single（仅同类型失真配对）的性能。单一失真类型训练导致所有数据集上SRCC显著下降，验证了多样化失真配对对学习复杂质量关系的关键作用——仅学习同类型失真间的比较无法泛化到真实场景中不同SR模型产生的多样化伪影。

**多尺度评估。** Table 5同时报告了单尺度评估的消融结果。多尺度随机裁剪并取平均的策略在DIV2K和DRealSR等高分辨率数据集上带来明显增益，表明多尺度有助于同时捕捉纹理细节（小尺度）和结构语义（大尺度），但对低分辨率的Set5&Set14提升有限。

**损失函数选择。** Table 6对比了Huber损失、L1损失和L2损失对RQI训练的影响。Huber损失在所有数据集上一致优于L1和L2，归功于其平滑梯度特性：对小误差的二次惩罚保证了稳定收敛，对大误差的线性惩罚降低了对异常MOS差值的敏感性。这一特性对于拟合正负值范围较广的相对质量差异尤为重要。

### RQI作为感知损失的应用

Table 4展示了将RQI作为辅助感知损失（$ \mathcal{L} = \mathcal{L}_{ori} + \lambda \cdot s $，$\lambda=-0.1$）训练SR模型的效果。在SwinIR、SeeSR、PiSA-SR三个代表性SR模型上，RQI辅助训练在DeQA-Score、DISTS、LPIPS等感知指标上均取得最佳结果，同时保持了可接受的PSNR/SSIM水平。Figure 4的视觉对比进一步表明，RQI损失能够引导模型生成更真实的纹理细节，同时有效保持结构保真度（另见Figure 11和Figure 12的补充对比）。

### 局限性与失效模式

尽管RQI在感知一致性上表现优异，但其存在以下边界条件：

1. **跨内容不可比。** RQI分数仅在共享同一参考图像时才有意义，无法用于不同内容图像之间的质量比较——这是相对质量框架的内在约束。
2. **保真度与感知的权衡。** RQI主要衡量感知质量，对像素级保真度（如不可逆丢失的纹理细节）的评估能力有限。在需要精确重建的应用场景中，仍需结合失真导向指标。
3. **低分辨率场景。** 在Set5&Set14等极低分辨率数据集上，RQI的SRCC略逊于DeQA-Score，可能与输入分辨率限制及大规模预训练差距有关。
4. **训练数据依赖。** RQI依赖已有IQA数据集中的MOS差值标注，尚未探索在无MOS标注情况下的自适应训练方案。

### 补充图表

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/001_Table_1.jpg]]
*Table 1: Consistency evaluations of quality metrics with human perception. SRCC, PLCC and winning rate are reported*

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/004_Table_2.jpg]]
*Table 2: The effectiveness of the proposed RQI framework. We train different IQA models across multiple datasets following the traditional FR-IQA setting and the RQI scheme (with subscript ‘R’). SRCC consistency with user opinions are reported*

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/005_Table_3.jpg]]
*Table 3: Consistency evaluations of image metrics on four IQA benchmarks. BSD-SR [30], QADS [61] and SRIQA-Bench [9] are SR-IQA datasets, and Kadid-10K [28] is a general IQA dataset. The best and second best performances are in bold and underscore*

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/006_Figure_3.jpg]]
*Figure 3: We show different cases where existing metrics fail. As a comparison, RQI handles all the cases correctly. All scores are normalized to [0,1] for easier comparisons. Please zoom in for better view*

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/007_Figure_4.jpg]]
*Figure 4: Visual comparison of training advancing SR models with RQI metric as an auxiliary loss. Please zoom in for a better view*

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/008_Table_4.jpg]]
*Table 4: Quantitative comparisons between baseline SR methods, training them using AFINE [9], and using RQI as auxiliary loss*

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/012_Table_5.jpg]]
*Table 5: Ablation study of the RQI scheme*

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/013_Table_6.jpg]]
*Table 6: SRCCs results for selecting different losses under RQI*

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/015_Figure_9.jpg]]
*Figure 9: NR-IQA metrics PI [5], NIQE [31], Clip-IQA [36] and MANIQA [48] can fail on cases where subtle structure of semantics are changed, due to the lack of proper references*

![[assets/figures/papers/paper_list_l740_https_arxiv_org_abs_2503_13074/figures/016_Figure_10.jpg]]
*Figure 10: Perception-based FR-IQA metrics LPIPS [58] and DISTS [14] can fail when GT quality is relatively lower. They make contradictory evaluations for models that output perceptually higher results than GTs*



## 定位与知识库关联

### 1. 全参考评价方法的演进与RQI的定位

RQI的核心贡献在于将超分辨率评价从“绝对质量预测”范式切换为“相对质量比较”范式，这一转变直接回应了现有全参考（FR）评价指标的深层矛盾。

**失真导向的FR指标**（如 **PSNR**、**SSIM**（Wang et al., TIP 2004））长期作为SR评价的事实标准，但其根本缺陷在于：回归到多个可行解的平均值会导致对平滑/模糊输出的系统性偏好，与人类感知判断相悖。RQI通过引入非对称的相对质量差异训练，使模型不再将GT视为唯一理想解，从而解耦了这一矛盾。

**感知导向的FR指标**（如 **LPIPS**（Zhang et al., CVPR 2018）、**DISTS**（Ding et al., TIP 2020））虽然通过深度特征空间的距离度量缓解了上述问题，但在真实场景下暴露了新的脆弱性：当GT图像本身质量欠佳时（如RealSR、DRealSR数据集中的情况），这些指标会给出与人类感知相矛盾的评估。RQI的训练策略——允许任意失真图像作为参考、学习MOS差值而非绝对分数——使其天然具备对GT质量波动的鲁棒性，这是其区别于LPIPS/DISTS的关键机制。

**非对称FR指标**方面，**AFINE**是直接相关的前驱工作，它同样尝试了非对称评价思路，但需要专门收集SR数据来训练。RQI的突破在于：仅利用现有IQA数据集（Kadid-10K、PIPAL）的MOS标注即可完成训练，无需SR特定数据的采集，显著降低了应用门槛。这一数据效率优势在Table 2中得到了充分验证——在多个IQA架构和训练集组合下，RQI训练方案均一致地提升了SRCC。

### 2. 无参考评价方法的局限与RQI的互补性

**传统NR指标**（**NIQE**（Mittal et al., SPL 2013）、**PI**）和**深度NR指标**（**Clip-IQA**（Wang et al., AAAI 2023）、**MANIQA**（Yang et al., CVPRW 2022））面临的根本瓶颈是缺乏可靠参考，导致无法评估纹理/结构保真度。Figure 9展示了这一失败模式：当SR输出出现细微的语义结构变化时，NR指标无法给出正确判断。

RQI并未试图替代NR指标，而是通过固定输入顺序（$I_{HR}$在前，$I_{GT}$在后）的评估推理，在保留参考信息的同时避免了NR指标的上述缺陷。值得注意的是，RQI框架可以直接应用于MANIQA等NR架构的改造（通过修改为双输入模式），Table 2中MANIQA_RQI相比原始MANIQA在DRealSR上SRCC提升达+0.245，证明了该框架对现有NR模型的兼容性和增强能力。

**基于LLM的评价模型**（如 **DeQA-Score**）代表了另一条技术路线，其在Set5&Set14等低分辨率数据集上表现出微弱优势（SRCC 0.699 vs RQI 0.664）。这一差距可能与RQI模型输入分辨率的限制及预训练规模有关，而非方法本质缺陷。在更高分辨率的数据集（DIV2K、RealSR、DRealSR）上，RQI均实现了对DeQA-Score的超越。

### 3. 适用边界与关键约束

RQI的设计隐含以下适用边界，使用时需严格注意：

**参考共享约束**：RQI分数仅在共享同一参考图像时才有意义，无法用于跨内容图像的质量比较。这是相对评价范式的固有特性，而非实现缺陷。

**感知质量偏向**：RQI主要衡量感知质量，而非像素级保真度。对于超分辨率中不可逆丢失的纹理细节，RQI无法提供像素级的保真度评估。这一偏向在作为SR训练辅助损失时表现为：模型倾向于生成视觉吸引力更强但可能与GT存在结构性偏差的输出（尽管Figure 11显示结构保真度得到了较好保持）。

**训练数据依赖**：RQI的训练依赖已有IQA数据集中的MOS差值标签，尚未探索在无MOS标注情况下的自适应训练方案。Table 5的消融实验表明，单一失真类型的训练会导致性能显著下降，说明多样化失真配对对学习复杂质量关系至关重要，这也意味着训练数据的多样性直接影响RQI的泛化能力。

**分辨率敏感性**：多尺度块评估相比单尺度在高分辨率数据集上带来明显增益（Table 5），表明RQI的性能与输入分辨率策略相关。在极低分辨率场景下，性能可能受限。

### 4. 局限与开放问题

**跨任务泛化**：RQI框架目前仅在SR评价和训练中得到验证。其核心机制——相对质量差异学习——理论上适用于去模糊、去噪、去雨等其他图像恢复任务，但缺乏实验证据。这是最直接的延伸方向。

**保真度与感知的权衡**：RQI作为辅助损失训练SR模型时（Table 4），在DeQA-Score等感知指标上取得最佳结果，但对像素级保真度的影响尚未系统量化。设计一种既能保持感知对齐、又能可靠评估纹理重建准确性的原则性保真度度量，仍是开放挑战。

**MOS差值的线性假设**：当前RQI直接使用MOS差值（$q_i - q_j$）作为监督信号，隐含假设了质量差异与感知差异之间的线性关系。这一假设是否最优、是否存在更符合人类感知的非线性映射，值得深入探究。

**扩散模型的适配**：将RQI损失用于扩散模型训练时，是否会对采样多样性或模式覆盖产生影响，目前尚无研究。考虑到扩散模型在SR领域的快速增长，这一问题的解答具有现实紧迫性。

**无MOS标注的自适应训练**：RQI对MOS标注的依赖限制了其在无标注数据上的应用。能否通过自监督或弱监督方式构建相对质量关系，是提升框架通用性的关键方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Bridging_the_Perception_Gap_in_Image_Super_Resolution_Evaluation.pdf]]
