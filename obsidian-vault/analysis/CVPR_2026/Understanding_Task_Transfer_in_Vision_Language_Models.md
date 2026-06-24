---
title: Understanding Task Transfer in Vision-Language Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Understanding_Task_Transfer_in_Vision_Language_Models.pdf
project_link: "https://aka.ms/task-transfer-vlms"
code_link: null
aliases:
- UTTVLM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过在某个感知任务上微调VLM，改变其内部表示，再利用完美差距因子（PGF）来衡量这种表示变化相对于目标任务性能天花板的影响，从而量化源任务到目标任务的迁移效果。
primary_logic: 通过定义完美差距因子（PGF）以及任务的迁移性（transferability）和可塑性（malleability）指标，可以系统刻画VLM在不同感知任务间的迁移图谱：低层视觉任务具有最高的正向迁移性，任务可以聚集成相互促进或抑制的团簇，并可按迁移角色分为捐赠者、海盗、海绵和筛子，这些规律能够指导数据选择，以实现更高效的微调并减轻负迁移。
claims:
- 底层感知任务（相对深度、相对反射率等）的平均正向迁移性和可塑性最高，图像层任务的正向迁移性也较高。
- 使用PGF指导的数据选择在所有测试目标上均优于随机混合，甚至在某些任务上超过直接使用目标数据进行微调。
- 语义对应（Semantic Correspondence）在所有模型规模上都是统计显著的捐赠任务（p<0.01），而功能对应（Functional Correspondence）在小模型上是显著的海盗任务（p<0.05）。
- 在Qwen‑2.5‑VL 32B中涌现出一个包含9个任务的正向团簇，这些任务之间均表现出正向迁移。
---

# Understanding Task Transfer in Vision-Language Models

> [!tip] 核心洞察
> 通过定义完美差距因子（PGF）以及任务的迁移性（transferability）和可塑性（malleability）指标，可以系统刻画VLM在不同感知任务间的迁移图谱：低层视觉任务具有最高的正向迁移性，任务可以聚集成相互促进或抑制的团簇，并可按迁移角色分为捐赠者、海盗、海绵和筛子，这些规律能够指导数据选择，以实现更高效的微调并减轻负迁移。

| 字段 | 内容 |
|------|------|
| 中文题名 | 视觉语言模型中的任务迁移理解 |
| 英文题名 | Understanding Task Transfer in Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.18787) · [Project](https://aka.ms/task-transfer-vlms) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | 基于完美差距因子（PGF）的任务可迁移性与可塑性分析框架 |
| Dataset | BLINK, Jigsaw, Object Localisation |

> [!tip] 效果简介
> - BLINK (13 tasks) 上，平均正向可迁移性 低层任务 (Relative Depth, Relative Reflectance, Visual Correspondence) vs 中/高层任务 (低层任务的平均正向可迁移性和可塑性明显更高)。
> - BLINK, 多模型规模 上，平均正向可迁移性 Qwen‑2.5‑VL 32B vs Qwen‑2.5‑VL 3B / 7B (模型规模越大，平均正向可迁移性和可塑性越强)。
> - Jigsaw, Object Localisation (BLINK subset) 上，目标准确率 PGF‑based data selection vs Random mixture / Direct supervised finetuning (PGF指导的数据选择在所有目标上均优于随机混合，并在两个任务上超过直接微调)。

## 概述

视觉语言模型（VLM）在零样本视觉感知任务上的表现仍远落后于人类和专用模型——例如，在BLINK基准上，GPT-4o仅达60.04%，而人类可达95%。当对VLM进行参数高效微调以提升某一感知任务时，其对其他感知任务的零样本性能会产生未知且不可预测的影响，缺乏系统的迁移规律指导，这构成了当前的核心瓶颈。

针对这一问题，本文提出**基于完美差距因子（PGF）的任务可迁移性与可塑性分析框架**。PGF的核心思想是：将微调带来的性能变化，归一化到目标任务当前性能与性能天花板之间的剩余差距上，从而公平地量化不同难度任务间的迁移效果。在此基础上，定义任务的可迁移性（transferability）和可塑性（malleability）指标，系统刻画VLM在不同感知任务间的迁移图谱。

核心发现包括：
- **低层视觉任务具有最高的正向迁移性**：相对深度、相对反射率等低层任务在微调后对其他任务的促进效果最强，且自身也最容易被其他任务正向影响（Figure 3, Figure 4）。
- **任务聚集成相互促进或抑制的团簇**：在Qwen‑2.5‑VL 32B中涌现出一个包含9个任务的正向团簇，这些任务之间均表现出正向迁移（Figure 6）。
- **任务可按迁移角色分类**：根据迁移性与可塑性，任务可分为捐赠者（Donor）、海盗（Pirate）、海绵（Sponge）和筛子（Sieve）四类——例如，语义对应是统计显著的捐赠任务，而功能对应在小模型上是显著的海盗任务。
- **PGF可指导数据选择以提升微调效率**：利用PGF选择对目标任务最有益的源任务数据混合进行微调，在所有测试目标上均优于随机混合，甚至在某些任务上超过直接使用目标数据进行微调（Figure 8）。

在方法谱系上，该工作区别于传统的**原始准确率增益（raw accuracy gain）**度量，后者未考虑任务难度和性能天花板的差异；相较于标准的**LoRA微调**（Hu et al., 2021）流程，本文框架引入了归一化的迁移度量与系统化的任务间影响建模。其分析流程涵盖：任务选择与数据准备、独立源任务LoRA微调、零样本跨任务评估、PGF矩阵构建、迁移性与可塑性计算、任务图与团簇分析、任务角色分类，以及PGF指导的数据选择等模块。

主要实验基于**BLINK基准的13个视觉感知任务**，在**Qwen‑2.5‑VL系列（3B/7B/32B）**上展开，关键结论包括：模型规模越大，平均正向可迁移性和可塑性越强（Figure 5）；PGF指导的数据选择在Jigsaw和Object Localisation任务上甚至超越直接监督微调。

## 背景与动机

视觉语言模型（VLM）在零样本视觉感知任务上的表现仍显著落后于人类水平。以BLINK基准为例，当前表现最佳的GPT-4o仅达到60.04%的平均准确率，GPT-4V为51.14%，而人类可达95%（BLINK leaderboard数据）。这一性能缺口表明，VLM在底层视觉感知能力上存在系统性不足，亟需通过微调来弥补。

然而，对VLM进行任务特定的参数高效微调面临一个关键困境：**在某一感知任务上微调模型，会以未知且不可预测的方式影响其他感知任务的零样本性能**。这种跨任务影响的规律尚未被系统揭示，导致实践中缺乏指导微调策略的理论依据。传统的迁移度量方法仅依赖原始准确率增益（raw accuracy gain），忽略了不同任务之间的难度差异和性能天花板差异，无法提供可比较的归一化度量，使得跨任务的迁移效果难以公平评估和预测。

本文的核心动机正是填补这一空白：**建立一套系统化的分析框架，量化VLM在不同视觉感知任务间的迁移关系，揭示任务间相互促进或抑制的结构化规律**。为此，作者引入完美差距因子（Perfection Gap Factor, PGF）作为归一化迁移度量，并基于此定义任务的可迁移性（transferability）与可塑性（malleability），从而构建从单一源任务到多个目标任务的迁移图谱。该框架不仅能够刻画任务间的正向与负向迁移模式，还能将任务按迁移角色分类（捐赠者、海盗、海绵、筛子），并发现任务间形成的正向或负向团簇结构，最终为指导数据选择和高效微调提供实证依据。

## 核心创新

本文的核心创新在于提出了一套**系统量化视觉语言模型（VLM）任务间迁移效应的分析框架**，其关键洞察是：传统基于原始准确率增益的迁移度量方法无法公平比较不同难度任务间的迁移效果，必须通过归一化来消除任务难度和模型基线差异。

### 关键创新点一：完美差距因子（PGF）

传统方法直接使用微调后的准确率变化量作为迁移度量，但这忽略了不同任务固有的难度差异和性能天花板。例如，一个基线准确率已达90%的任务，其剩余提升空间远小于基线准确率仅为30%的任务，同等的准确率增益在二者间具有完全不同的意义。

本文提出的**完美差距因子（Perfection Gap Factor, PGF）** 解决了这一问题。对于源任务 $T_i$ 到目标任务 $T_j$ 的迁移，PGF定义为：

$$\mu_{ij} = \frac{\text{Acc}(\mathcal{M}(T_i), T_j) - \text{Acc}(\mathcal{M}, T_j)}{U_j - \text{Acc}(\mathcal{M}, T_j) + \epsilon}$$

其中分子是微调带来的准确率增益，分母是目标任务当前性能与天花板 $U_j$ 之间的差距。这一归一化使得PGF能够衡量“剩余提升空间被填补（或扩大）了多少比例”，从而在不同任务间具有可比性。Table 1通过三个难度不同的示例任务直观展示了PGF相对于原始增益的归一化特性。

### 关键创新点二：可迁移性与可塑性指标

在PGF矩阵的基础上，本文进一步定义了**任务可迁移性（Transferability）** 和**可塑性（Malleability）** 两个聚合指标，分别从“源任务对他人影响”和“目标任务受他人影响”两个维度刻画任务在迁移网络中的行为。

正向可迁移性 $\Delta(i)^+$ 综合了源任务 $i$ 对所有目标的正向PGF值，同时通过指数项 $(1 - e^{-p/N})/p$ 对受影响任务的比例进行加权，使得影响广泛且幅度大的源任务获得更高分数。负向可迁移性 $\Delta(i)^-$ 同理度量负向影响。正向可塑性 $\Theta(j)^+$ 和负向可塑性 $\Theta(j)^-$ 则从目标任务的视角度量其受其他源任务正向或负向影响的综合程度。这一设计同时考虑了**影响幅度**和**影响广度**两个维度，相较于仅观察平均准确率变化的传统做法，提供了更丰富的迁移结构信息。

### 关键创新点三：任务迁移图谱与角色分类

基于PGF矩阵，本文构建了VLM感知任务间的**结构化迁移图谱**，并从中提取出具有统计显著性的**正向团簇**和**负向团簇**。例如，在Qwen‑2.5‑VL 32B中涌现出一个包含9个任务的正向团簇，这些任务之间均表现出正向迁移（Figure 6）。

更进一步，本文根据任务在迁移网络中的可迁移性与可塑性特征，将任务分为四类角色：
- **捐赠者（Donor）**：高正向可迁移性、低负向可迁移性，对其他任务有净正向贡献
- **海盗（Pirate）**：高负向可迁移性，微调后会损害其他任务性能
- **海绵（Sponge）**：高正向可塑性，容易从其他任务的微调中获益
- **筛子（Sieve）**：高负向可塑性，容易受到其他任务微调的负面影响

实验发现，**语义对应（Semantic Correspondence）** 在所有模型规模上都是统计显著的捐赠任务（p<0.01），而**功能对应（Functional Correspondence）** 在小模型上是显著的海盗任务（p<0.05）。这种角色分类为理解任务间的相互影响机制提供了可操作的分析框架。

### 关键创新点四：PGF指导的数据选择

作为框架的应用验证，本文提出了**PGF指导的数据选择策略**：当目标任务缺乏训练数据时，利用PGF矩阵选择对该任务正向迁移最强的源任务数据混合进行微调。实验表明，这一策略在所有测试目标上均优于随机混合，甚至在某些任务上超过了直接使用目标数据进行监督微调的性能（Figure 8）。这证明PGF不仅是一个分析工具，更可以直接指导实际的微调数据策展，为减轻负向迁移提供了量化依据。

## 整体框架

本研究提出了一套系统化的分析框架，用于量化视觉语言模型（VLM）在感知任务间的迁移行为。该框架的核心目标并非提出一种新的微调算法，而是建立一套度量标准和分析工具，以揭示“在一个感知任务上微调VLM会如何影响其在其他感知任务上的零样本表现”这一根本问题。

整体流程由八个模块组成，形成一条从数据准备到应用验证的完整链路。

### 1. 任务选择与数据准备

框架的输入是来自 **BLINK** 基准的13个视觉感知任务，这些任务按感知层次（低层/中层/高层）和粒度（像素级/裁剪级/图像级）进行分类（Table 2）。每个任务配有独立的训练集和验证集，用于后续的独立微调和跨任务评估。

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/001_Figure_1.jpg]]
*Figure 1: One finetune, many fates: Finetuning Qwen-2.5-VL 32B on perception tasks creates a structured map of transfer capabilities. (The list of perception tasks considered can be found in Table 2.)*

### 2. 独立源任务微调

对于每个选定的源任务 $T_i$，框架使用 **LoRA**（秩=8，α=16）在8×A100 GPU上对VLM进行参数高效微调。训练采用DeepSpeed ZeRO‑2/3和余弦学习率调度。微调后的模型记为 $\mathcal{M}(T_i)$，表示在任务 $T_i$ 上特化的模型变体。

### 3. 零样本跨任务评估

将每个微调后的模型 $\mathcal{M}(T_i)$ 在所有13个目标任务 $T_j$ 上进行零样本评估，记录准确率 $\operatorname{Acc}(\mathcal{M}(T_i), T_j)$。同时记录未微调的基础模型 $\mathcal{M}$ 在各任务上的基线准确率 $\operatorname{Acc}(\mathcal{M}, T_j)$。

### 4. PGF矩阵构建

对于每一对源-目标任务 $(T_i, T_j)$，计算完美差距因子（Perfection Gap Factor, PGF）：

$$\mu_{ij} = \frac{\operatorname{Acc}(\mathcal{M}(T_i), T_j) - \operatorname{Acc}(\mathcal{M}, T_j)}{U_j - \operatorname{Acc}(\mathcal{M}, T_j) + \epsilon}$$

其中 $U_j$ 是任务 $T_j$ 的性能天花板（本框架中固定为100%），$\epsilon$ 是防止除零的小常数。PGF的核心设计在于：它将微调带来的性能变化归一化到“剩余改进空间”中，从而在不同难度和基线水平的任务之间实现公平比较。PGF为正表示正向迁移（微调后更接近天花板），为负则表示负向迁移（性能下降）。

由此形成一个 $13 \times 13$ 的PGF矩阵，矩阵的第 $i$ 行第 $j$ 列表示从源任务 $T_i$ 到目标任务 $T_j$ 的迁移效果。

### 5. 迁移性与可塑性计算

基于PGF矩阵，框架定义了四个聚合指标，分别从源任务和目标任务两个视角刻画迁移行为：

- **正向可迁移性 $\Delta(i)^+$**：源任务 $T_i$ 对所有目标任务的正向迁移效果的综合度量，同时考虑影响幅度和受影响任务的比例。
- **负向可迁移性 $\Delta(i)^-$**：源任务 $T_i$ 对所有目标任务的负向迁移效果的综合度量。
- **正向可塑性 $\Theta(j)^+$**：目标任务 $T_j$ 受到其他源任务正向影响的综合度量。
- **负向可塑性 $\Theta(j)^-$**：目标任务 $T_j$ 受到其他源任务负向影响的综合度量。

这些指标均采用指数衰减加权，以平衡影响幅度（PGF值的大小）和影响广度（受影响任务的数量）。

### 6. 任务图与团簇分析

将PGF矩阵转化为有向任务迁移图，其中节点代表任务，边的权重和方向由PGF值决定。在此图上，框架提取统计显著的**正向团簇**（团簇内所有任务对之间均存在正向迁移）和**负向团簇**。团簇的显著性通过Wilcoxon检验验证。

### 7. 任务角色分类

基于每个任务的迁移性和可塑性特征，框架将任务分为四种角色：
- **捐赠者（Donor）**：高正向可迁移性，能普遍促进其他任务。
- **海盗（Pirate）**：高负向可迁移性，会损害其他任务的性能。
- **海绵（Sponge）**：高正向可塑性，容易从其他任务中获益。
- **筛子（Sieve）**：高负向可塑性，容易受到其他任务的负面影响。

### 8. PGF指导的数据选择

框架的输出可应用于实际微调场景：当目标任务的训练数据不可用时，利用PGF矩阵选择对该目标最有益的源任务数据混合进行微调。具体而言，选择PGF值超过一定阈值的源任务数据，按比例混合后微调模型。这一策略在初步实验中已展现出优于随机混合的效果，甚至在某些任务上超过直接使用目标数据微调的性能。

整个框架的输入是13个感知任务的训练/验证数据和一个预训练VLM，输出是PGF迁移矩阵、任务迁移图谱、任务角色标注以及可操作的数据选择建议。框架的设计使其原则上可扩展到任意数量的任务和不同的VLM架构。

## 核心模块与公式推导

### 完美差距因子（Perfection Gap Factor, PGF）

本工作的核心度量工具是完美差距因子（PGF），它解决了传统原始准确率增益（raw accuracy gain）无法归一化不同任务难度和模型基线水平的问题。PGF 衡量的是：在源任务上微调后，目标任务上剩余的性能差距（与天花板之间的差距）被缩小（或扩大）的比例。

设 $\mathcal{M}$ 为预训练 VLM，$T_i$ 为源任务，$T_j$ 为目标任务，$\mathcal{M}(T_i)$ 为在 $T_i$ 上微调后的模型。PGF 定义为：

$$\mu _ { i j } = \frac { \operatorname { A c c } ( \mathcal { M } ( T _ { i } ) , T _ { j } ) - \operatorname { A c c } ( \mathcal { M } , T _ { j } ) } { U _ { j } - \operatorname { A c c } ( \mathcal { M } , T _ { j } ) + \epsilon }$$

其中 $U_j$ 为任务 $T_j$ 的性能天花板（本文统一设为 100%），$\epsilon$ 为防止分母为零的小常数。PGF > 0 表示正向迁移，PGF < 0 表示负向迁移。

PGF 的一个关键理论边界是负向迁移的幅度可以远大于正向迁移。给定 $m$ 个评估问题，PGF 的理论最小值为：

$$\mathrm { P G F } _ { \mathrm { m i n } } = - ( m - 1 )$$

这意味着负向迁移在幅度上具有天然的不对称优势，该特性在 Figure 9 中得到系统分析。

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/012_Figure_9.jpg]]
*Figure 9: Behavior of PGF as a function of baseline accuracy (x) and change after finetuning (k)*

### 任务可迁移性（Task Transferability）

为综合度量一个源任务对所有目标任务的整体迁移影响，本文定义了正向和负向可迁移性指标。这两个指标同时考虑迁移效应的幅度和影响广度（即受影响的负向任务比例）。

**正向可迁移性** $\Delta ( i ) ^ { + }$ 聚合源任务 $i$ 对所有目标的正向 PGF 值，并以受正向影响的任务比例 $p/N$ 为权重：

$$\Delta ( i ) ^ { + } = \left( \frac { 1 - e ^ { - \frac { p } { N } } } { p } \right) \sum _ { j = 1 } ^ { N } \mu _ { i \to j } \mathbf { 1 } _ { \{ \mu _ { i \to j } > 0 \} }$$

**负向可迁移性** $\Delta ( i ) ^ { - }$ 以对称方式定义：

$$\Delta ( i ) ^ { - } = \left( \frac { 1 - e ^ { - \frac { n } { N } } } { n } \right) \sum _ { j = 1 } ^ { N } \mu _ { i \to j } \mathbf { 1 } _ { \{ \mu _ { i \to j } < 0 \} }$$

其中 $p$ 和 $n$ 分别为受正/负向影响的任务数量，$N$ 为总任务数。权重因子 $(1 - e^{-p/N})/p$ 的设计使得：当仅影响少量任务时，即使 PGF 值较高，综合得分也会被抑制，从而避免稀疏异常值主导排名。

### 任务可塑性（Task Malleability）

可塑性指标从目标任务的视角出发，度量该任务受到其他源任务微调影响的综合程度。

**正向可塑性** $\Theta ( j ) ^ { + }$ 聚合所有源任务对目标 $j$ 的正向 PGF：

$$\Theta ( j ) ^ { + } = \left( \frac { 1 - e ^ { - \frac { p } { N } } } { p } \right) \sum _ { i = 1 } ^ { N } \mu _ { i \to j } \mathbf { 1 } _ { \{ \mu _ { i \to j } > 0 \} }$$

**负向可塑性** $\Theta ( j ) ^ { - }$ 以对称方式定义：

$$\Theta ( j ) ^ { - } = \left( \frac { 1 - e ^ { - \frac { n } { N } } } { n } \right) \sum _ { i = 1 } ^ { N } \mu _ { i \to j } \mathbf { 1 } _ { \{ \mu _ { i \to j } < 0 \} }$$

可塑性指标揭示了哪些任务最容易从其他任务的微调中获益（或受损），为理解任务间的依赖关系提供了量化基础。

### 分析流水线模块

整个分析框架由以下核心模块串联构成：

1. **任务选择与数据准备**：从 BLINK 基准中选择 13 个视觉感知任务，按感知层次（低/中/高）和粒度（像素/裁剪/图像）分类（Table 2），构建训练/验证集。

2. **独立源任务微调**：使用 LoRA（秩=8，$\alpha$=16）在 8×A100 GPU 上分别对每个源任务微调 VLM，采用 DeepSpeed ZeRO‑2/3 和余弦学习率调度。

3. **零样本跨任务评估**：将每个微调后的模型在所有 13 个目标任务上进行零样本评估，记录准确率。

4. **PGF 矩阵构建**：对每一对源‑目标任务，计算 PGF 值，形成 $13 \times 13$ 的迁移矩阵（Figure 2）。

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/002_Figure_2.jpg]]
*Figure 2: PGF Heatmaps for Qwen-2.5-VL model family (3B, 7B, 32B)*

5. **迁移性与可塑性计算**：聚合 PGF 矩阵的行与列，按上述定义计算正/负迁移性和可塑性指标。

6. **任务图与团簇分析**：根据 PGF 构建任务迁移图，提取统计显著的团簇。任务团簇（Task Clique）定义为：团簇内任意两个任务之间的 PGF 均超过预设阈值，且通过 Wilcoxon 检验验证统计显著性。

7. **任务角色分类**：基于迁移性与可塑性，将任务分为四类角色：
   - **捐赠者（Donor）**：高正向可迁移性，低负向可迁移性
   - **海盗（Pirate）**：高负向可迁移性，低正向可迁移性
   - **海绵（Sponge）**：高正向可塑性，低负向可塑性
   - **筛子（Sieve）**：高负向可塑性，低正向可塑性

8. **PGF 指导的数据选择**：在缺乏目标任务训练数据时，利用 PGF 选择对该任务最有益的源任务数据混合进行微调，作为负迁移缓解策略的初步概念验证。

### 补充图表

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/003_Table_1.jpg]]
*Table 1: Illustration of the Perfection Gap Factor (PGF) across three target tasks*

## 实验与分析

### 核心指标：完美差距因子（PGF）的归一化特性

传统迁移度量使用原始准确率增益（raw accuracy gain）直接比较微调前后的性能变化，但该方法忽略了不同任务在难度和性能天花板上的固有差异——一个从40%提升到50%的10%增益，与一个从80%提升到90%的10%增益，在语义上截然不同。为解决此问题，本文提出**完美差距因子（Perfection Gap Factor, PGF）**：

$$\mu_{ij} = \frac{\text{Acc}(\mathcal{M}(T_i), T_j) - \text{Acc}(\mathcal{M}, T_j)}{U_j - \text{Acc}(\mathcal{M}, T_j) + \epsilon}$$

其中 $U_j$ 为目标任务 $T_j$ 的性能天花板（实验中统一设为100%），$\epsilon$ 为防止除零的小常数。PGF衡量的是“微调后性能变化占原始剩余可提升空间的比例”——PGF=1表示微调完全填补了与天花板之间的差距，PGF<0则表示性能出现了退化。Table 1通过三个难度不同的示例任务展示了PGF相比原始增益的归一化优势：同一微调操作在不同任务上产生相同的原始增益，但PGF值因其基线准确率和剩余空间的差异而显著不同。

### 实验设置与基准

实验基于**BLINK基准**的13个视觉感知任务，按感知层次（低层/中层/高层）和粒度（像素级/裁剪级/图像级）进行分类（详见Table 2）。微调采用LoRA（秩=8，α=16）在8×A100 GPU上进行，使用DeepSpeed ZeRO‑2/3和余弦学习率调度。每个源任务独立微调后，在所有13个目标任务上进行零样本评估，构建13×13的PGF迁移矩阵。主要模型为Qwen‑2.5‑VL系列（3B/7B/32B），并在LLaVA等架构上进行了有限验证。

### 主实验结果

#### 低层感知任务具有最强的正向迁移性

Figure 3和Figure 4展示了不同感知层次和粒度下的平均正向可迁移性（$\Delta^+$）与可塑性（$\Theta^+$）趋势。核心发现是：**低层视觉任务（相对深度、相对反射率、视觉对应等）的平均正向可迁移性和可塑性显著高于中/高层任务**，图像级任务的正向迁移性也较高。这意味着在低层感知任务上微调VLM，对其他任务产生的正向溢出效应最为广泛和强烈；同时，低层任务本身也最容易从其他任务的微调中获益。

#### 模型规模扩大增强正向迁移

Figure 5展示了Qwen‑2.5‑VL系列中模型规模对迁移性的影响。随着模型从3B扩展到7B再到32B，平均正向可迁移性单调增加。这表明**更大规模的VLM拥有更强的跨任务知识共享能力**，微调某一任务时能更有效地激活相关能力。消融实验（Figure A.25–A.27）进一步表明，随着训练步数从25%增加到100%，平均正向可迁移性单调增加，但任务间的定性迁移模式保持稳定，说明迁移结构在训练早期即已形成。

#### 任务迁移图谱与团簇结构

Figure 1展示了Qwen‑2.5‑VL 32B上微调13个感知任务后形成的结构化迁移图谱，直观呈现了正/负迁移关系。基于PGF矩阵，本文定义了**任务团簇（Task Clique）**——一组任务之间均存在正向迁移的子集。Figure 6展示了从32B模型中提取的一个包含9个任务的正向团簇，这些任务之间相互促进。通过Wilcoxon检验验证的统计显著团簇表明，正向团簇的大小和置信度随模型规模增大而增加（Table A.3）。Figure 10则展示了一个大小为4的负向团簇，体现了任务间的消极相互影响。

#### 任务角色分类

基于迁移性（transferability）和可塑性（malleability）两个维度，任务被分为四类角色：
- **捐赠者（Donor）**：高迁移性、低可塑性——对其他任务贡献大，但自身不易被影响。**语义对应（Semantic Correspondence）**在所有模型规模上都是统计显著的捐赠任务（p<0.01）。
- **海盗（Pirate）**：低迁移性、高可塑性——从其他任务获益多，但对其他任务贡献少或产生负影响。**功能对应（Functional Correspondence）**在小模型上是显著的海盗任务（p<0.05）。
- **海绵（Sponge）**：高迁移性、高可塑性——双向受益。
- **筛子（Sieve）**：低迁移性、低可塑性——双向隔离。

#### PGF指导的数据选择

Figure 8展示了PGF指导的数据选择策略的实际效果。在无目标任务训练数据的情况下，利用PGF选择对该任务最有益的源任务数据混合进行微调。结果显示：**PGF指导的数据选择在所有测试目标上均优于随机混合，甚至在某些任务上超过直接使用目标数据进行微调**。这一发现为数据高效微调提供了实用指导——通过少量源任务数据的智能组合，可以接近甚至超越全量目标任务微调的效果。

#### 跨模态迁移验证

Figure 7展示了在VSI视频基准上的PGF热力图，证实了感知任务到视频任务的跨模态迁移。与图像感知任务一致，相对反射率（Relative Reflectance）在视频任务中表现为捐赠任务，而取证检测（Forensic Detection）表现为海盗任务，表明迁移角色具有一定的跨模态稳定性。

### 消融与表示分析

LoRA权重的余弦相似性分析（Figure A.28–A.30）显示，Visual Similarity、Art Style和Jigsaw任务之间的表示相似性最高，且32B模型的整体相似性最强，表明大模型拥有更强的跨任务对齐能力。PGF的理论分析（Figure 9）揭示了其不对称性：在给定m个评估问题时，PGF的理论最小负值为 $\text{PGF}_{\min} = -(m-1)$，意味着负向迁移的幅度可能远大于正向迁移（正向迁移上限为1），这一特性需要在数据选择策略中予以考虑。

### 局限性与失败模式

本研究存在以下局限需要关注：（1）分析主要基于多项选择题形式的BLINK基准，这种输出格式可能限制模型的失败模式，无法完全反映开放式生成场景下的迁移行为；（2）实验仅在Qwen‑2.5‑VL系列上进行了全面测试，其他VLM架构（如LLaVA）仅做了少量验证，结论的普适性尚需进一步检验；（3）PGF指导的数据选择实验仅为初步概念验证，未进行全面的超参数搜索和混合比例优化；（4）天花板性能固定为100%，未采用数据驱动的最佳天花板，可能在某些任务上引入偏差。

### 补充图表

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/004_Table_2.jpg]]
*Table 2: BLINK tasks with abbreviation and classification by Perceptual Level and Granularity*

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/005_Figure_3.jpg]]
*Figure 3: Average positive transferability trends across granular and perceptual levels. We observe that positive transferability increases with model size and generally low-level and image-level are highly transferable. Detailed category-wise heatmaps are provided in the supplementary material*

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/006_Figure_4.jpg]]
*Figure 4: Average positive malleability trends across granular and perceptual levels. We observe that positive malleability increases with model size and generally low-level benefit the most from finetuning. Detailed category-wise heatmaps are provided in the supplementary material*

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/007_Figure_5.jpg]]
*Figure 5: Task transferability trends across model sizes in Qwen-2.5-VL. As expected, as model size increases, the average positive transferability increases*

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/008_Figure_6.jpg]]
*Figure 6: Positive clique of size 9 from Qwen-2.5-VL 32B*

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/009_Figure_7.jpg]]
*Figure 7: PGF heatmaps for Qwen-2.5-VL 3B (left) and 7B (right) models across the VSI benchmark. Consistent with previous findings, Relative Reflectance and Forensic Detection emerge as donor task and pirate task, respectively*

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/010_Figure_8.jpg]]
*Figure 8: Performance comparison under different dataset selection strategies. PGF-informed mixtures consistently outperform random mixtures and even surpass direct supervision in two cases*

![[assets/figures/papers/paper_list_l2065_https_arxiv_org_abs_2511_18787/figures/011_Figure_10.jpg]]
*Figure 10: A negative clique of size 4 from Qwen-2.5-VL 32B*

## 方法谱系与知识库定位

### 1 核心贡献与差异化定位

本研究提出的**基于完美差距因子（PGF）的任务可迁移性与可塑性分析框架**，其核心贡献不在于提出一种新的微调算法，而在于构建了一套**测量与诊断工具**，用以系统揭示视觉语言模型（VLM）内部的任务迁移规律。该方法与既有工作的关系可从两个维度定位：度量方式的改进与分析范式的转变。

#### 1.1 度量方式的改进：从原始增益到归一化因子

传统任务迁移研究通常直接使用**原始准确率增益（Raw Accuracy Gain）** 作为迁移效果的度量。这种方法的根本缺陷在于忽视了不同任务之间的难度差异和性能天花板差异——一个从40%提升到60%的增益，与一个从80%提升到90%的增益，其含义截然不同。

本文提出的**完美差距因子（PGF）** 通过归一化解决了这一问题：

$$\mu_{ij} = \frac{\text{Acc}(\mathcal{M}(T_i), T_j) - \text{Acc}(\mathcal{M}, T_j)}{U_j - \text{Acc}(\mathcal{M}, T_j) + \epsilon}$$

其核心设计意图在于：度量微调所“弥合”的剩余性能差距的比例，而非绝对增益。这一设计使得跨任务、跨模型的迁移效果具有可比性。Table 1通过三个难度差异显著的示例任务，直观展示了PGF相较于原始增益的优势：当基线准确率较高时，相同的绝对增益对应更高的PGF值，反映了“在接近天花板的区域取得进展更为困难”这一现实。

#### 1.2 分析范式的转变：从单任务观察到系统图谱

现有的参数高效微调方法——如**LoRA**（Hu et al., 2021）和**Llama-Adapter**——聚焦于如何在单任务上高效适配模型，但并未提供理解任务间相互影响的框架。这些方法构成了本文的**微调基础设施**（本文使用LoRA秩=8、α=16进行所有微调实验），而非分析对象本身。

本文的分析范式转变体现在：将VLM视为一个**任务生态系统**，通过构建完整的13×13 PGF迁移矩阵，系统刻画每对源-目标任务之间的正/负向影响。基于此矩阵，进一步定义了**任务可迁移性（Task Transferability）** 和**任务可塑性（Task Malleability）** 两个聚合指标：

$$\Delta(i)^{+} = \left(\frac{1 - e^{-\frac{p}{N}}}{p}\right) \sum_{j=1}^{N} \mu_{i \to j} \mathbf{1}_{\{\mu_{i \to j} > 0\}}$$

$$\Theta(j)^{+} = \left(\frac{1 - e^{-\frac{p}{N}}}{p}\right) \sum_{i=1}^{N} \mu_{i \to j} \mathbf{1}_{\{\mu_{i \to j} > 0\}}$$

这两个指标的设计兼顾了**影响幅度**（PGF值的大小）和**影响广度**（受影响任务的比例），通过指数衰减权重避免少数极端值主导聚合结果。这种“矩阵构建→行/列聚合→图结构分析”的流水线，与此前仅观察平均准确率变化的做法形成了根本性的方法论差异。

### 2 方法适用边界

#### 2.1 适用条件

本框架的适用依赖于以下条件的同时满足：

- **封闭式评估格式**：当前分析基于多项选择题形式的基准（BLINK），因为PGF的计算依赖于明确的准确率数值。对于开放式生成任务（如图像描述、视觉推理），缺乏直接可比的标量性能度量，PGF框架的扩展需要额外的适配层。
- **可定义性能天花板**：本文统一设定天花板$U_j = 100\%$，这一假设在多项选择题场景下合理，但在更复杂的视觉任务中可能引入偏差——某些任务的“完美性能”可能无法达到100%，或需要数据驱动的方式估计。
- **参数高效微调设置**：所有实验均采用LoRA进行微调，结论对其他PEFT方法（如Adapter、Prefix Tuning）的迁移性尚缺乏验证。

#### 2.2 已观察到的规律边界

实验证据表明以下规律具有统计显著性（置信度0.9以上），但其边界值得关注：

- **低层视觉任务的正向迁移优势**：相对深度（Relative Depth）、相对反射率（Relative Reflectance）和视觉对应（Visual Correspondence）等低层任务表现出最高的平均正向可迁移性和可塑性（Figure 3, Figure 4）。这一规律在Qwen-2.5-VL系列中稳定成立，但在其他架构上的验证有限。
- **模型规模的单调效应**：从3B到7B到32B，平均正向可迁移性单调增加（Figure 5），且32B模型中涌现出包含9个任务的正向团簇（Figure 6）。这表明更大规模的VLM具有更强的跨任务表示对齐能力，但该结论的架构依赖性尚需检验。
- **任务角色的跨模型一致性**：语义对应（Semantic Correspondence）在所有模型规模上均为统计显著的捐赠任务（p<0.01），而功能对应（Functional Correspondence）在小模型上为显著的海盗任务（p<0.05）。这种角色分配的跨规模稳定性为PGF指导的数据选择提供了基础。

### 3 局限性与开放问题

#### 3.1 已确认的局限

本研究明确指出的局限包括：

- **基准格式限制**：分析仅限于多项选择题形式的基准，开放式生成场景下的迁移模式可能截然不同，这一局限在fairness notes中被明确标注。
- **架构覆盖不足**：主要实验基于Qwen-2.5-VL系列，对其他VLM架构（如LLaVA）仅做了少量验证，结论的普适性需要进一步研究。
- **数据选择策略的初步性**：PGF指导的数据选择实验（Figure 8）仅为概念验证，未进行超参数搜索和混合比例优化，其性能上限可能被低估。
- **天花板假设的简化**：统一使用100%作为天花板，未采用数据驱动的最佳天花板估计，可能在某些任务上引入系统性偏差。

#### 3.2 理论层面的开放问题

PGF的理论行为揭示了任务迁移中的**不对称性**：正向迁移的PGF上限为1（完全弥合性能差距），而负向迁移的理论下限为$-(m-1)$（其中$m$为评估问题数量），如Figure 9所示。这意味着负向迁移的幅度可能远超正向迁移，这一理论性质的实际影响值得深入探索。

此外，任务团簇的形成机制尚不明确。LoRA权重的余弦相似性分析（附录A.7）提供了初步线索——Visual Similarity、Art Style和Jigsaw任务之间的表示相似性最高，且32B模型的整体相似性最强——但表示相似性与PGF迁移效果之间的因果关系尚未建立。

#### 3.3 实践层面的开放问题

- **多任务联合微调策略**：如何利用已发现的任务团簇和角色分类（捐赠者、海盗、海绵、筛子）设计多任务联合微调策略，以最大化正向迁移、最小化负向干扰？
- **自动混合比例确定**：PGF指导的数据选择目前依赖阈值截断，是否存在理论上的最优混合比例？能否通过优化方法自动确定？
- **跨模态迁移的深入理解**：Figure 7展示了感知任务到视频任务的跨模态迁移，但底层机制尚待探索。
- **新架构上的规律演化**：随着VLM架构的快速演进（如GPT-4V类模型），本文发现的迁移规律是会保持稳定还是发生质变？

### 4 与知识库的关系

本工作在以下知识脉络中定位：

- **上游依赖**：以LoRA（Hu et al., 2021）为代表的参数高效微调方法提供了实验基础设施；以BLINK基准为代表的多任务感知评估提供了标准化测试平台。
- **并行关系**：与任务向量（Task Vector）和模型合并（Model Merging）方向的研究共享“理解模型内部任务表示关系”的目标，但本文侧重零样本迁移的系统测量而非权重空间的算术操作。
- **下游拓展**：PGF框架可为多任务学习中的任务采样策略、持续学习中的灾难性遗忘缓解、以及VLM的指令微调数据配比提供理论指导——这些方向目前尚处于开放问题阶段。

## 原文 PDF

![[paperPDFs/CVPR_2026/Understanding_Task_Transfer_in_Vision_Language_Models.pdf]]
