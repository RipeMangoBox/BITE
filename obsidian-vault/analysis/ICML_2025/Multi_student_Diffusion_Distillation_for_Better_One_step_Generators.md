---
title: "Multi-student Diffusion Distillation for Better One-step Generators"
type: paper
paper_level: A
venue: ICML
year: 2025
pdf_ref: paperPDFs/ICML_2025/Multi_student_Diffusion_Distillation_for_Better_One_step_Generators.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/MSD/
code_link: null
aliases:
- MSDM
- MSDDBOSG
tags:
- ICML_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "通过引入多个学生模型，每个学生专注于条件输入的一个子集，并采用数据分区与多次蒸馏策略，在不增加单次推理延迟的前提下提升整体有效模型容量。"
primary_logic: "将单步扩散蒸馏扩展为多学生框架，通过语义聚类将条件空间划分给多个学生，结合分布匹配与对抗蒸馏的两阶段训练，并为小型学生引入教师分数匹配预训练，可突破单一学生的容量限制，获得优于教师模型的一步生成质量。"
claims:
- "MSD 使用4个同规模学生，在 ImageNet-64x64 上的一步生成 FID 达到 1.20，显著优于单学生基线 DMD2 的 1.28。"
- "MSD 使用4个同规模学生，在零样本 COCO2014 文本生成上取得 FID 8.20，优于 DMD2 的 8.35，且推理延迟保持不变（0.09s）。"
- "在2D玩具实验中，随着学生数量从1增加到8，生成分布与教师分布的 L1 距离持续下降，直观验证了多学生蒸馏的有效性。"
- "MSD 框架可应用于分布匹配蒸馏和一致性蒸馏等多种方法，具有通用性。"
---

# Multi-student Diffusion Distillation for Better One-step Generators

> [!tip] 核心洞察
> 将单步扩散蒸馏扩展为多学生框架，通过语义聚类将条件空间划分给多个学生，结合分布匹配与对抗蒸馏的两阶段训练，并为小型学生引入教师分数匹配预训练，可突破单一学生的容量限制，获得优于教师模型的一步生成质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 多学生扩散蒸馏实现更优一步生成器 |
| 英文题名 | Multi-student Diffusion Distillation for Better One-step Generators |
| 会议/期刊 | ICML 2025 |
| Links | [paper](https://arxiv.org/abs/2410.23274) · [Project](https://research.nvidia.com/labs/toronto-ai/MSD/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Multi-Student Distillation (MSD) |
| Dataset | ImageNet-64x64, MS-COCO2014 |

> [!tip] 效果简介
> - ImageNet-64x64 上，FID 为 1.20 (MSD 4 students, ADM)，对比 1.28 (DMD2, single student)，变化 -0.08。
> - ImageNet-64x64 上，FID 为 2.37 (MSD 4 students, DM only)，对比 2.62 (DMD, single student)，变化 -0.25。
> - ImageNet-64x64 上，FID 为 2.88 (MSD 4 smaller students, ADM)，对比 11.67 (4 smaller students without TSM, ADM)，变化 -8.79。

## 概要

单步扩散蒸馏旨在将多步扩散教师模型压缩为一步生成器，以大幅降低推理延迟。然而，单一学生模型受限于架构容量，难以高质量覆盖所有多样性条件输入，导致生成质量与推理速度之间存在难以调和的权衡。本文提出**多学生蒸馏（Multi-Student Distillation, MSD）**框架，核心思想是将条件空间划分为多个不相交的子集，每个子集由一个独立的学生生成器负责，从而在不增加单次推理延迟的前提下，显著提升整体有效模型容量。

MSD 的关键机制包括三个层面：
1. **条件分区与数据过滤**：将输入条件空间按语义相似性聚类为等大的不相交分区，每个学生仅专注于其对应分区的生成任务。
2. **多阶段蒸馏流程**：每个学生独立经历分布匹配（DM）和对抗分布匹配（ADM）两阶段训练，其中 DM 阶段所有学生共享同一份完整配对数据集以维持模式覆盖，避免模式崩塌。
3. **教师分数匹配预训练（TSM）**：为小型学生模型引入轻量级的分数匹配预训练阶段，使其权重初始化接近教师的去噪输出，从而为后续蒸馏提供良好起点。

实验表明，MSD 在 ImageNet-64×64 类别条件生成上，使用 4 个同规模学生取得 FID 1.20（单步），优于单学生基线 DMD2 的 1.28；在零样本 COCO2014 文本生成上取得 FID 8.20，优于 DMD2 的 8.35，且推理延迟保持 0.09 秒不变。消融研究进一步验证，性能提升源于容量增加而非等效大批量训练，且学生数量从 1 增至 8 时 FID 持续下降。MSD 框架具有通用性，可应用于分布匹配蒸馏和一致性蒸馏等多种单步蒸馏方法。

### 扩散模型的一步生成困境

扩散模型已成为图像生成领域的事实标准，其通过迭代去噪过程逐步将高斯噪声转化为高质量图像。然而，这种多步推理范式带来了显著的推理延迟——典型的多步扩散模型需要数十次甚至上百次网络前向传播才能生成单张图像，严重制约了其在实时交互场景中的应用。

为突破这一瓶颈，**单步扩散蒸馏**应运而生。其核心思想是将预训练的多步扩散教师模型压缩为仅需一次前向传播的学生生成器，从而在保持生成质量的同时大幅降低推理延迟。代表性工作包括**分布匹配蒸馏（DMD）**和**一致性蒸馏（CTM）**等方法，它们通过不同的分布对齐策略，使学生模型的一步输出逼近教师模型的多步采样结果。

### 单一学生的容量瓶颈

尽管单步蒸馏取得了显著进展，但现有方法均采用**单学生范式**——即仅训练一个学生生成器来覆盖教师模型在所有条件输入下的完整生成分布。这一范式面临根本性的容量限制：

- **条件空间的多样性压力**：在类别条件生成中，ImageNet-64×64 包含 1000 个类别，每个类别对应不同的视觉模式；在文本条件生成中，条件空间更是近乎无限。单一学生模型需要在有限的参数量内同时学习所有条件下的高质量生成映射。
- **质量-速度权衡的固化**：当学生模型与教师架构相同时，其容量尚可勉强应对，但 FID 指标的提升空间有限（例如 DMD2 在 ImageNet-64×64 上单步 FID 为 1.28）。当尝试使用更小的学生模型以进一步降低推理延迟时，生成质量会出现显著退化，因为小模型根本无力覆盖完整的条件分布。

这一瓶颈的本质在于：**单步蒸馏中，单一学生模型受限于架构容量，难以高质量覆盖所有多样性条件输入，导致生成质量与推理速度的权衡难以进一步突破**。

### 核心动机：分而治之

本文的核心洞察源于一个朴素的问题：既然单一学生容量有限，能否用多个学生来分担任务？

这一思路的直观类比是**专家混合（Mixture of Experts）**范式——通过多个子模型分别处理输入空间的不同区域，在不增加单次推理开销的前提下提升整体模型容量。然而，将这一思想应用于扩散蒸馏面临两个关键挑战：

1. **如何划分条件空间**：需要设计合理的任务分割策略，使每个学生专注于条件输入的一个子集，同时避免模式崩塌。
2. **如何训练小型学生**：当学生模型架构小于教师时，直接从教师权重初始化不再可行，需要新的预训练策略为小模型提供良好的起点。

基于此，本文提出**多学生蒸馏（Multi-Student Distillation, MSD）**框架，通过引入多个学生模型、条件空间分区与多阶段蒸馏策略，在不增加单次推理延迟的前提下突破单一学生的容量限制，实现更优的一步生成质量。

## 核心方法与创新机理

### 瓶颈洞察：单一学生模型的容量天花板

单步扩散蒸馏的核心矛盾在于**生成质量与推理速度的权衡**。现有蒸馏方法（如 DMD、DMD2）试图将多步教师模型的知识压缩到单个一步生成器中，但单一学生模型的架构容量成为根本性瓶颈——一个固定参数量的生成器难以高质量地覆盖条件空间中所有多样性输入。这一容量限制在以下场景尤为突出：

- **类别条件生成**：ImageNet-64×64 中 1000 个类别的视觉多样性要求生成器具备极强的条件建模能力。
- **文本条件生成**：开放词汇的语义空间远大于封闭类别集合，单一学生更难兼顾所有文本提示。
- **小型学生模型**：当追求更低推理延迟而压缩模型规模时，容量不足的问题急剧恶化——实验显示，4 个小型学生若不采用特殊初始化，FID 高达 11.67，远逊于同规模单学生的理论潜力。

### 核心思路：容量解耦——用“多”换“好”而不换“慢”

MSD 的关键创新在于**将“容量”与“延迟”解耦**：通过引入多个学生模型，每个学生仅负责条件输入的一个子集，在不增加单次推理延迟的前提下提升整体有效模型容量。推理时，根据输入条件的路由机制仅激活对应的单个学生，因此 NFE 保持为 1，延迟与单学生基线完全一致。

这一设计可形式化为：

$$G_k = \mathrm{Distill}\left(\mu_{\mathrm{teacher}}, \mathcal{D}_k = F(\mathcal{D}, \mathcal{V}_k)\right), \quad k = 1, ..., K$$

其中 $\mathcal{V}_k$ 为条件空间的一个分区，$\mathcal{D}_k$ 为对应的过滤后训练数据子集。每个学生 $G_k$ 独立蒸馏，推理时仅激活匹配当前条件的单个学生。

### 关键设计变化（Changed Slots）

相较于单学生蒸馏基线，MSD 在四个关键维度上进行了系统性创新：

**1. 学生模型数量：从 1 到 K**

| 维度 | 基线值 | MSD 方案 |
|------|--------|----------|
| 学生数量 | 单个学生 | K 个学生（K≥2），每个负责条件子集 |

这是 MSD 最核心的架构变化。条件空间按三个原则划分：**不相交**（避免冗余训练）、**等大小**（保证负载均衡）、**语义聚类**（同一分区内条件语义相近）。对于类别条件生成，简单按类别序号顺序分割（每学生 250 类）即可取得与 K-means 语义聚类几乎相同的效果（FID 2.37 vs 2.39），表明即使极简的分区策略也已足够有效。

**2. 训练数据过滤策略：分区过滤 + 共享配对数据**

| 维度 | 基线值 | MSD 方案 |
|------|--------|----------|
| 条件数据 | 使用全部条件对应的数据 | 按条件分区过滤训练条件 |
| 配对数据 | 使用全部配对数据 | **所有学生共享同一份完整配对数据** |

这是 MSD 训练策略中最关键的发现：在分布匹配（DM）阶段，若将配对数据集（教师预先生成的噪声-图像对）也按条件分区过滤，会导致模式崩塌——学生仅学习到局部模式，丧失全局多样性覆盖能力。消融实验（Figure 8）明确验证：共享完整配对数据的学生 FID 显著优于分区过滤配对数据的方案。这一设计确保了每个学生虽专注于自身条件子集，但仍能接触到全局的生成模式信息，从而避免模式崩塌。

**3. 小型学生初始化：TSM 预训练阶段**

| 维度 | 基线值 | MSD 方案 |
|------|--------|----------|
| 小模型初始化 | 仅支持从教师权重初始化（要求同架构） | 引入 TSM 预训练阶段，为任意架构的小型学生提供良好初始化 |

当学生模型架构与教师不同（尤其是更小）时，无法直接从教师权重初始化。MSD 提出**教师分数匹配（TSM）**预训练阶段，使小型学生在多个噪声水平上匹配教师的去噪输出：

$$\mathcal{L}_{\mathrm{TSM}} = \mathbb{E}_t \left[\lambda_t \Vert \pmb{\mu}_{\mathrm{TSM}}^{\varphi}(\pmb{x}_t, t) - \pmb{\mu}_{\mathrm{teacher}}(\pmb{x}_t, t) \Vert_2^2\right]$$

TSM 为后续蒸馏提供了接近教师得分函数的初始化，是小型学生成功蒸馏的必要条件。实验证据极为有力：4 个小型学生（参数量减少 42%）在使用 TSM 后 FID 达到 2.88，而不使用 TSM 时 FID 高达 11.67，差距达 8.79。

**4. 蒸馏流程：从单阶段到多阶段**

| 维度 | 基线值 | MSD 方案 |
|------|--------|----------|
| 蒸馏流程 | 单阶段 DM 或两阶段 DM+ADM（单个学生） | 每个学生独立执行：TSM（可选）→ DM → ADM |

MSD 为每个学生设计了统一的多阶段训练管线（Figure 3）：
- **Stage 0（TSM，可选）**：仅用于与教师不同架构的小型学生，提供权重初始化。
- **Stage 1（DM）**：分布匹配蒸馏，通过最小化反向 KL 散度使学生生成分布逼近教师分布，辅以回归损失（LPIPS）鼓励模式覆盖。
- **Stage 2（ADM）**：对抗分布匹配微调，在 DM 基础上加入对抗损失，以最小计算开销进一步锐化生成质量。

### 方法通用性

MSD 作为“即插即用”的框架升级，其通用性在两类蒸馏方法上得到验证：
- **分布匹配蒸馏**：2D 玩具实验中，学生数量从 1 增加到 8 时，生成分布与教师分布的 L1 距离持续下降（Figure 4），直观验证了多学生蒸馏的有效性。
- **一致性蒸馏**：在一致性蒸馏框架下同样观察到多学生带来的质量提升（Figure 6），表明 MSD 不依赖于特定的蒸馏算法。

### 效果总结

在 ImageNet-64×64 上，MSD 使用 4 个同规模学生（ADM 阶段）取得 FID 1.20，显著优于单学生基线 DMD2 的 1.28；在零样本 COCO2014 文本生成上取得 FID 8.20，优于 DMD2 的 8.35，且推理延迟保持 0.09s 不变。消融研究进一步证实，性能提升源于有效模型容量的增加，而非等效大 batch 效应——4 学生每学生 batch size 32 的 FID（2.53）优于单学生 batch size 128 的 FID（2.60）。

**Multi-Student Distillation (MSD)** 是一个通用的单步扩散蒸馏框架，其核心思想是将一个预训练的多步教师扩散模型蒸馏为 **K 个单步学生生成器**，每个学生仅负责条件输入空间的一个子集，从而在不增加单次推理延迟的前提下提升整体有效模型容量。

### 框架工作流

MSD 的整体 pipeline 包含三个关键阶段，如 Figure 3 所示：

**阶段 0（可选）：教师分数匹配预训练（Teacher Score Matching, TSM）**
当学生模型架构小于教师模型时（例如参数量减少 42% 或更多），直接进行单步蒸馏会导致严重质量下降。TSM 阶段通过让小型学生模型在真实图像的不同噪声水平上匹配教师的去噪输出，为学生提供接近教师得分函数的良好初始化：

$$
\mathcal { L } _ { \mathrm { T S M } } = \mathbb { E } _ { t } [ \lambda _ { t } \Vert \pmb { \mu } _ { \mathrm { T S M } } ^ { \varphi } ( \pmb { x } _ { t } , t ) - \pmb { \mu } _ { \mathrm { t e a c h e r } } ( \pmb { x } _ { t } , t ) \Vert _ { 2 } ^ { 2 } ]
$$

对于与教师同架构的学生，此阶段可跳过，直接从教师权重初始化。

**阶段 1：分布匹配蒸馏（Distribution Matching, DM）**
每个学生独立执行分布匹配蒸馏，通过最小化教师与学生生成分布在扩散时间步上的反向 KL 散度来训练一步生成器：

$$
\mathbb { E } _ { t } D _ { \mathrm { K L } } ( p _ { t , \mathrm { f a k e } } | | p _ { t , \mathrm { r e a l } } )
$$

其梯度更新利用真假得分函数的差值：

$$
\nabla _ { \theta } \mathcal { L } _ { \mathrm { K L } } ( \theta ) \simeq \mathbb { E } _ { z , t , x _ { t } } [ w _ { t } \alpha _ { t } ( s _ { \mathrm { f a k e } } ( { \boldsymbol x } _ { t } , t ) - s _ { \mathrm { r e a l } } ( { \boldsymbol x } _ { t } , t ) ) \nabla _ { \theta } G _ { \theta } ( { \boldsymbol z } ) ]
$$

同时可辅以回归损失 $\mathcal { L } _ { \mathrm { r e g } } ( \theta ) = \mathbb { E } _ { ( z , y ) \sim \mathcal { D } _ { \mathrm { p a i r e d } } } \ell ( G _ { \theta } ( z ) , y )$（使用 LPIPS 距离和教师预先生成的噪声-图像对），以鼓励学生覆盖更多模式。

**阶段 2：对抗分布匹配微调（Adversarial Distribution Matching, ADM）**
在 DM 阶段基础上加入对抗损失，通过最小判别器进一步锐化生成结果。此阶段计算开销极小，可从阶段 1 的检查点直接恢复训练。

### 条件分区与数据过滤

MSD 将条件空间 $\mathcal{Y}$ 划分为 K 个不相交、等大小、语义相似的分区 $\mathcal{V}_k$（Figure 1）。具体策略遵循三个简化原则：

- **不相交性**：避免学生间的冗余训练。
- **等大小**：确保各学生负载均衡。
- **语义聚类**：同一分区内的条件语义相近（例如通过 K-means 对条件嵌入聚类），使每个学生更容易覆盖其负责的条件子空间。

对于每个学生 $G_k$，训练数据按条件分区进行过滤：

$$
G _ { k } = \mathrm { D i s t i l l } ( \mu _ { \mathrm { t e a c h e r } } , \mathcal { D } _ { k } = F ( \mathcal { D } , \mathcal { V } _ { k } ) ) , \ k = 1 , . . . , K
$$

**关键设计选择**：在 DM 阶段，所有学生共享同一份完整的配对数据集 $\mathcal{D}_{\mathrm{paired}}$（即教师预先生成的噪声-图像对），而非按分区过滤配对数据。消融实验（Figure 8）表明，过滤配对数据会导致模式崩塌，因为每个学生需要在回归损失中接触到完整的模式覆盖信息。

### 推理时的路由机制

推理时，给定输入条件，系统仅激活对应分区的单个学生生成器进行一步生成。因此 **NFE 恒为 1**，推理延迟与单学生基线完全相同（例如在 MS-COCO2014 上均为 0.09s），不会因学生数量增加而引入额外计算开销。

### 框架通用性

MSD 是一个 **即插即用框架**，可应用于任意条件单步扩散蒸馏方法。除分布匹配蒸馏（DMD/DMD2）外，论文在 2D 玩具实验中验证了 MSD 同样适用于一致性蒸馏（CTM），随着学生数量从 1 增加到 8，生成分布与教师分布的 L1 距离持续下降（Figure 4, Figure 6），验证了框架的通用性。

### 3.1 分布匹配蒸馏基础

MSD 的蒸馏基础建立在分布匹配蒸馏（Distribution Matching Distillation, DMD）之上。其核心思想是：在扩散模型的不同噪声时间步 $t$ 上，最小化学生生成器输出分布 $p_{t,\mathrm{fake}}$ 与教师模型输出分布 $p_{t,\mathrm{real}}$ 之间的反向 KL 散度。该目标可形式化为：

$$\mathbb { E } _ { t } D _ { \mathrm { K L } } ( p _ { t , \mathrm { f a k e } } | | p _ { t , \mathrm { r e a l } } ) = \mathbb { E } _ { x _ { t } } \left( \log \left( \frac { p _ { t , \mathrm { f a k e } } ( x _ { t } ) } { p _ { t , \mathrm { r e a l } } ( x _ { t } ) } \right) \right)$$

其中 $x_t = \alpha_t x + \sigma_t \epsilon$ 表示在时间步 $t$ 加噪后的样本。该 KL 散度关于学生生成器参数 $\theta$ 的梯度可利用真假得分函数的差值进行近似计算：

$$\nabla _ { \theta } \mathcal { L } _ { \mathrm { K L } } ( \theta ) : = \nabla _ { \theta } \mathbb { E } _ { t } D _ { \mathrm { K L } } \simeq \mathbb { E } _ { z , t , x _ { t } } [ w _ { t } \alpha _ { t } ( s _ { \mathrm { f a k e } } ( { \boldsymbol x } _ { t } , t ) - s _ { \mathrm { r e a l } } ( { \boldsymbol x } _ { t } , t ) ) \nabla _ { \theta } G _ { \theta } ( { \boldsymbol z } ) ]$$

其中 $s_{\mathrm{real}}$ 和 $s_{\mathrm{fake}}$ 分别为真实数据分布和生成数据分布的得分函数，$w_t$ 为自定义权重。这两个得分函数通过教师去噪模型 $\mu_{\mathrm{teacher}}$ 和假去噪模型 $\mu_{\mathrm{fake}}$ 进行近似：

$$s _ { \mathrm { r e a l } } ( \boldsymbol { x } _ { t } , t ) \approx - \frac { \boldsymbol { x } _ { t } - \alpha _ { t } \mu _ { \mathrm { t e a c h e r } } ( \boldsymbol { x } _ { t } , t ) } { \sigma _ { t } ^ { 2 } } , \quad s _ { \mathrm { f a k e } } ( \boldsymbol { x } _ { t } , t ) \approx - \frac { \boldsymbol { x } _ { t } - \alpha _ { t } \mu _ { \mathrm { f a k e } } ( \boldsymbol { x } _ { t } , t ) } { \sigma _ { t } ^ { 2 } }$$

假去噪模型 $\mu_{\mathrm{fake}}$ 通过以下回归损失进行在线训练，使其能准确预测由学生生成器产生的图像在加噪后的原始图像：

$$\mathcal { L } _ { \mathrm { d e n o i s e } } ( \phi ) = \mathbb { E } _ { z , t , x _ { t } } [ \lambda _ { t } \| \pmb { \mu } _ { \mathrm { f a k e } } ^ { \phi } ( \pmb { x } _ { t } , t ) - \pmb { x } \| _ { 2 } ^ { 2 } ]$$

为鼓励学生覆盖更多模式，DMD 还引入了一个回归损失，使用教师预先生成的噪声-图像对 $(\boldsymbol{z}, \boldsymbol{y})$ 和 LPIPS 距离 $\ell$：

$$\mathcal { L } _ { \mathrm { r e g } } ( \theta ) = \mathbb { E } _ { ( z , y ) \sim \mathcal { D } _ { \mathrm { p a i r e d } } } \ell ( G _ { \theta } ( z ) , y )$$

### 3.2 多学生蒸馏框架

MSD 将单学生蒸馏扩展为多学生框架。设条件空间 $\mathcal{Y}$ 被划分为 $K$ 个不相交、等大小的分区 $\mathcal{V}_1, \mathcal{V}_2, ..., \mathcal{V}_K$，每个学生生成器 $G_k$ 负责一个条件子集。蒸馏过程可表示为：

$$G _ { k } = \mathrm { D i s t i l l } ( \mu _ { \mathrm { t e a c h e r } } , \mathcal { D } _ { k } = F ( \mathcal { D } , \mathcal { V } _ { k } ) ) , \ k = 1 , . . . , K$$

其中 $F(\mathcal{D}, \mathcal{V}_k)$ 为数据过滤函数，从完整数据集 $\mathcal{D}$ 中筛选出条件属于 $\mathcal{V}_k$ 的样本。分区遵循三个原则：**不相交性**（避免冗余训练）、**等大小**（保证负载均衡）、**语义聚类**（使分区内条件语义相似，降低单个学生的学习难度）。

### 3.3 两阶段蒸馏流程

每个学生独立执行两阶段蒸馏流程。第一阶段为分布匹配（DM），第二阶段为对抗分布匹配（ADM），可表示为：

$$G _ { k } ^ { ( 1 ) } = \mathrm { D i s t i l l } _ { \mathrm { D M } } \left( \mu _ { \mathrm { t e a c h e r } } , F _ { \mathrm { D M } } ( \mathcal { D } _ { \mathrm { D M } } , \mathcal { V } _ { k } ) \right)$$

$$G _ { k } ^ { ( 2 ) } = \mathrm { D i s t i l l } _ { \mathrm { A D M } } \left( \mu _ { \mathrm { t e a c h e r } } , F _ { \mathrm { A D M } } ( \mathcal { D } _ { \mathrm { A D M } } , \mathcal { V } _ { k } ); G _ { k } ^ { ( 1 ) } \right)$$

第一阶段 DM 使用分布匹配损失，可选配回归损失或 TTUR 策略；第二阶段 ADM 在 DM 基础上加入对抗损失（最小判别器），进一步锐化生成结果，计算开销极小且可从第一阶段检查点恢复训练。关键设计在于：DM 阶段的**配对数据集在所有学生间共享**（不按分区过滤），以确保每个学生获得完整的模式覆盖信息，避免模式崩塌（该设计的必要性由 Figure 8 的消融实验验证）。

### 3.4 小模型预训练：教师分数匹配

当学生模型架构小于教师模型时（如参数量减少 42% 或 83%），直接进行分布匹配蒸馏效果极差。MSD 引入**教师分数匹配**（Teacher Score Matching, TSM）作为预训练阶段，使小型学生的初始权重逼近教师的得分函数：

$$\mathcal { L } _ { \mathrm { T S M } } = \mathbb { E } _ { t } [ \lambda _ { t } \Vert \pmb { \mu } _ { \mathrm { T S M } } ^ { \varphi } ( \pmb { x } _ { t } , t ) - \pmb { \mu } _ { \mathrm { t e a c h e r } } ( \pmb { x } _ { t } , t ) \Vert _ { 2 } ^ { 2 } ]$$

该损失在多个噪声水平上匹配教师模型的去噪输出 $\mu_{\mathrm{teacher}}$，为后续的单步蒸馏提供良好的初始化。完整的三阶段流程（TSM → DM → ADM）如 Figure 3 所示。消融实验表明，4 个小型学生若不经过 TSM 预训练直接进行 ADM，FID 高达 11.67；加入 TSM 后 FID 降至 2.88（Table 1），验证了 TSM 对小模型蒸馏的关键作用。

## 实验与关键发现

### 核心实验设置

MSD 框架在两个代表性任务上验证：ImageNet-64×64 类别条件生成和 MS-COCO2014 零样本文本到图像生成。所有蒸馏方法使用相同的预训练教师模型，FID 计算代码与图像数量保持一致。多学生推理时仅激活对应分区的单个学生，NFE 保持为 1，延迟与单学生基线相同。训练中总 batch size 和迭代次数在消融实验间保持一致，确保计算资源偏差不干扰结论。配对数据在所有学生间共享，使 DM 阶段每个学生获得相同的模式覆盖信息。

### 主要结果

**ImageNet-64×64 类别条件生成。** 如 Table 1 所示，MSD 使用 4 个同规模学生、经 ADM 阶段后取得 FID 1.20，显著优于单学生基线 DMD2 的 1.28（Δ=-0.08）。仅使用 DM 阶段时，MSD 4 学生取得 FID 2.37，同样优于单学生 DMD 的 2.62（Δ=-0.25）。值得注意的是，MSD 的 4 个同规模学生生成质量已略优于多步教师模型（FID 1.20 vs 教师 1.22），首次实现一步生成超越教师。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2410_23274/figures/005_Table_1.jpg]]
*Table 1: Comparing class-conditional generators on ImageNet-64×64. The number of function evaluations (NFE) for MSD is 1 as a single student is used at inference for the given input*

**小型学生蒸馏。** 当使用参数量减少 42% 的小型学生时，MSD 4 学生经 ADM 取得 FID 2.88。作为对比，若不使用 TSM 预训练（Teacher Score Matching），同样的小型学生组合 FID 高达 11.67（Table 1），验证了 TSM 预训练对小模型蒸馏的关键作用。

**零样本文本到图像生成。** 在 MS-COCO2014 上，MSD 4 学生经 ADM 取得 FID 8.20，优于 DMD2 的 8.35（Table 2）。关键的是，推理延迟保持 0.09s 不变，证明多学生框架在不牺牲推理速度的前提下提升生成质量。仅使用 DM 阶段时，MSD 取得 FID 8.80。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2410_23274/figures/006_Table_2.jpg]]
*Table 2: Comparing MSD to other methods on zero-shot text-to-image generation on MS-COCO2014. We measure speed with sampling time per prompt (latency) and quality with FID*

### 消融研究

所有消融实验在 ImageNet-64×64 上仅使用 DM 阶段训练 20k 迭代完成，结果汇总于 Table 3。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2410_23274/figures/008_Table_3.jpg]]
*Table 3: Ablation studies on different components of MSD. All experiments are done on ImageNet-64×64, trained with only the DM stage for 20k iterations, where B is the batch size per student. See App. B.1*

**容量增益 vs 等效 batch size。** MSD 使用 4 个学生、每学生 batch size 32 取得 FID 2.53，优于单学生 batch size 128 的 2.60。这直接证明性能提升来自多学生引入的有效模型容量增加，而非等效的大 batch 效应。

**学生数量的影响。** 学生数量从 1 增加到 8 时，FID 持续下降（2.60 → 2.32），验证了更多学生带来更大容量增益的趋势。这一规律在 2D 玩具实验中同样得到直观验证（Figure 4）：随着学生数量从 1 增加到 8，生成分布与教师分布的 L1 距离持续下降。

**条件分割策略。** 使用 K-means 语义聚类进行任务分割与简单顺序分割性能相当（FID 2.39 vs 2.37），表明简单的等分策略已十分有效，语义聚类带来的额外增益有限。

**配对数据过滤策略。** 在 DM 阶段，保持所有学生共享同一份完整配对数据集优于按分区过滤配对数据（Figure 8）。后者导致模式崩塌，原因是每个学生仅看到其负责条件对应的配对样本，缺乏对其他模式的覆盖信号。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2410_23274/figures/013_Figure_8.jpg]]
*Figure 8: Comparison of paired dataset filtering strategies for MSD4-DM. Partitioning the paired dataset for each student discourages mode coverage, which results in worse terminal performance. In comparison, keeping the same paired dataset for each student achieves better performance without impairing the convergence speed*

### 通用性验证

MSD 框架的通用性在一致性蒸馏（Consistency Distillation）上得到验证。在 2D 玩具实验中（Figure 6），将一致性蒸馏扩展为多学生版本后，更多学生同样提升蒸馏质量，证明 MSD 作为“即插即用”框架可应用于多种蒸馏方法。

### 失败模式与局限

1. **小模型质量瓶颈。** 参数量减少 83% 的学生图像质量仍有明显下降，训练未完全收敛。Figure 9 显示，学生规模减小和覆盖类别数增加均导致单学生性能下降，尽管 TSM 预训练显著缓解了这一问题，但小模型在极端压缩下的质量边界仍需进一步突破。

2. **计算开销。** 小模型蒸馏需要较长的 TSM 预训练和多阶段蒸馏（TSM → DM → ADM），计算开销较大。Table 6 对比了各蒸馏方法的训练效率，MSD 在训练总开销上高于单学生方法，但推理效率保持不变。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2410_23274/figures/014_Table_6.jpg]]
*Table 6: Comparison of various aspects of single-step distillation methods*

3. **静态分区的局限性。** 当前仅研究基于静态分区的多学生路由。部署时若 GPU 内存不足以容纳所有学生，模型切换会引入额外延迟；用户请求分布随时间变化时，静态分区可能导致负载不均。

4. **任务覆盖范围。** 实验主要在 ImageNet-64×64 和 COCO 上验证，对于更高分辨率或更多样化的生成任务尚未全面评估。如何将基于语义聚类的分区策略自动扩展到开放文本条件生成仍是开放问题。

![[assets/figures/papers/paper_list_l23_https_arxiv_org_abs_2410_23274/figures/016_Table_7.jpg]]
*Table 7: Hyperparameter details for different sized student models of the ADM architecture. Unspecified hyperparameters remain the same as the teacher. Latency is measured on a single NVIDIA RTX 4090 GPU*

## 定位与知识库关联

### 方法谱系：从单学生蒸馏到多学生容量扩展

MSD 的核心创新是将一步扩散蒸馏从“单教师→单学生”范式升级为“单教师→多学生”范式。其直接技术谱系可追溯至两类基础蒸馏方法：

- **分布匹配蒸馏（DMD/DMD2）**：MSD 的单学生蒸馏流程直接继承自 DMD 系列方法。DMD 通过最小化教师与学生生成分布在扩散时间步上的反向 KL 散度来训练一步生成器，并引入回归损失鼓励模式覆盖；DMD2 在此基础上加入对抗损失以锐化生成质量。MSD 将这套 DM→ADM 两阶段流程原样应用于每个学生，仅改变训练数据的条件过滤策略（Eq. 7, Eq. 9），因此可视为 DMD 系列在“多学生”维度上的框架级扩展。Table 1 中 DMD（FID 2.62）与 DMD2（FID 1.28）作为单学生基线，直接量化了 MSD 带来的增益（MSD4-DM FID 2.37, MSD4-ADM FID 1.20）。

- **一致性蒸馏（Consistency Distillation）**：MSD 的多学生思想同样被验证可应用于一致性蒸馏框架。Figure 6 的 2D 玩具实验显示，在一致性蒸馏中增加学生数量同样持续降低生成分布与教师分布的 L1 距离，表明 MSD 是一种通用的蒸馏方法升级策略，而非仅绑定于分布匹配范式。

在一步生成方法的更广谱系中，MSD 与以下方法形成对比：

- **StyleGAN-XL**：非扩散一步生成方法，通过 GAN 架构直接生成，在 ImageNet-64 上 FID 为 1.52（Table 1），低于 MSD-ADM 的 1.20，但不需要教师扩散模型。
- **CTM（Consistency Trajectory Model）**：一致性模型蒸馏方法，在 ImageNet-64 上单步 FID 为 1.92（Table 1），同样低于 MSD-ADM。

### 适用边界与条件依赖

MSD 的有效性建立在以下前提之上：

1. **条件空间可分区性**：MSD 要求输入条件空间可被划分为不相交、等大小的子集。对于类别条件生成（如 ImageNet 1000 类），每个学生负责 250 个连续类别即可工作；对于文本条件生成，通过 SD v1.5 文本编码器提取嵌入后沿四象限划分（Sec. 5.3）。当条件空间缺乏自然聚类结构或分区后子集语义差异过大时，性能增益可能减弱。

2. **教师模型预训练质量**：MSD 的蒸馏质量上限由教师模型决定。Table 1 中教师（ADM 架构）的 FID 为 1.36，MSD-ADM 的 1.20 甚至超越了教师，但这依赖于教师本身已具备足够的生成质量。若教师模型质量较低，多学生蒸馏无法弥补教师缺陷。

3. **计算资源与训练时间**：小模型蒸馏需要额外的 TSM 预训练阶段（Eq. 8），且三阶段流程（TSM→DM→ADM）显著增加了训练开销。Table 1 中 71% 参数减少的学生（FID 11.67 无 TSM vs 2.88 有 TSM）证明了 TSM 的必要性，但也意味着更长的训练周期。

4. **部署内存约束**：推理时仅激活单个学生，NFE=1，延迟不变（Table 2, 0.09s）。但若 GPU 显存不足以同时容纳所有 K 个学生，模型切换将引入额外 I/O 延迟。此外，静态分区在用户请求分布随时间变化时可能导致负载不均。

### 局限性与开放问题

**已识别的局限**：

- **分区策略的简单性**：当前采用静态、不相交、等大小的分区（Sec. 4.1），消融实验表明 K-means 语义聚类与简单顺序分割性能相当（Table 3, FID 2.39 vs 2.37），说明更复杂的分区策略尚未带来显著增益。这可能是当前实验规模有限所致，在更大规模或开放文本条件下，语义分区的重要性可能上升。
- **小模型质量天花板**：83% 参数减少的学生图像质量仍有明显下降（Figure 2），训练未完全收敛。TSM 预训练虽能大幅改善初始化（Table 1, FID 从 11.67 降至 2.88），但小模型的容量极限仍需进一步探索。
- **任务覆盖范围有限**：实验主要在 ImageNet-64×64 和 MS-COCO 2014 上验证，对于更高分辨率、视频生成、3D 生成等任务尚未评估。
- **学生间无协作**：当前每个学生独立训练，无权重共享、损失共享或动态路由机制。当学生数量极大时（K → ∞），独立训练的效率问题和训练稳定性问题尚不明确。

**开放问题**：

1. **文本条件的自动分区**：如何将基于语义聚类的分区策略自动扩展到开放文本条件生成，而无需依赖预训练文本编码器的启发式划分？
2. **动态路由与负载均衡**：在分布式部署中，如何根据实时请求分布动态调整学生模型的资源分配，避免静态分区导致的负载不均？
3. **架构协同进化**：将 MSD 与更高效的扩散架构（如 ViT 主干）结合，是否能进一步突破速度-质量边界？
4. **大规模学生极限**：当 K → ∞ 时，是否存在新的训练稳定性问题或收敛性瓶颈？独立训练策略是否仍有效？
5. **学生间知识共享**：是否可以通过权重共享、联合训练或知识蒸馏在学生间传递知识，进一步提升整体生成质量？

## 原文 PDF

![[paperPDFs/ICML_2025/Multi_student_Diffusion_Distillation_for_Better_One_step_Generators.pdf]]
