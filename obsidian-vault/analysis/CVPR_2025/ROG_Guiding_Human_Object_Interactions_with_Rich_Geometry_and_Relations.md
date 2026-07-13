---
title: ROG Guiding Human Object Interactions with Rich Geometry and Relations
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations.pdf
project_link: https://lalalfhdh.github.io/rog
code_link: null
aliases:
- RGHOIRGR
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过构建全面的交互距离场(IDF)并结合扩散关系模型学习时空关系先验，在生成过程中对运动进行引导与校正。
primary_logic: 利用泊松圆盘采样（PDS）与边界点提取24个物体关键点，构建人-物时空距离矩阵（IDF）；并设计视频扩散变换器（VDT）学习距离场先验，在去噪过程中以引导方式优化运动生成，使生成的运动符合真实交互距离分布。
claims:
- 在FullBodyManipulation数据集上，ROG的FID为5.119（优于CHOIS的5.227），MDev降至5.815（CHOIS为13.408），表明运动质量和交互一致性显著提高。
- 消融实验表明，添加物体关键点(obj-kp)使FID从9.775降至7.514，进一步添加IDF损失将R-Precision Top-1从0.547提升至0.666；使用完整距离矩阵D进行引导优于仅用质心C或无引导。
- 跨数据集验证（T2M-BEHAVE）显示ROG的碰撞率(Coll%)为0.195，比HOI-Diff的0.259降低24.6%，且MDev（10.784 vs 24.807）表现更好。
- 定性结果（Figure 3）表明ROG能够生成连贯的多阶段交互，避免了基线方法中常见的空隙、抖动和不自然接触。
---

# ROG Guiding Human Object Interactions with Rich Geometry and Relations

> [!tip] 核心洞察
> 利用泊松圆盘采样（PDS）与边界点提取24个物体关键点，构建人-物时空距离矩阵（IDF）；并设计视频扩散变换器（VDT）学习距离场先验，在去噪过程中以引导方式优化运动生成，使生成的运动符合真实交互距离分布。

| 字段 | 内容 |
|------|------|
| 中文题名 | ROG：利用丰富几何与关系引导人-物交互生成 |
| 英文题名 | ROG Guiding Human Object Interactions with Rich Geometry and Relations |
| 会议/期刊 | CVPR 2025 |
| Links | [Project](https://lalalfhdh.github.io/rog) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ROG |
| Dataset | FullBodyManipulation |

> [!tip] 效果简介
> - FullBodyManipulation 上，FID 5.119 vs 5.227 (CHOIS) (-0.108)；R-Precision Top-1 0.706 vs 0.630 (CHOIS) (+0.076)；MDev 5.815 vs 13.408 (CHOIS) (-7.593)。

## 概要

**问题瓶颈**：现有的人-物交互（HOI）生成方法普遍将物体几何过度简化为质心或最近点，忽略了物体的整体几何细节。这一简化导致复杂交互中的空间关系建模不足，生成的运动常出现穿透、悬空、抖动等不真实现象，语义对齐度也受到严重影响。

**核心思路**：ROG 提出以**交互距离场（Interactive Distance Field, IDF）**为核心的关系感知生成框架。该方法首先利用 AABB 边界点与泊松圆盘采样（PDS）提取 24 个物体表面关键点，构建人-物关键点对在时间维度上的距离矩阵，从而全面捕获交互过程中的空间关系动态。在此基础上，设计了一个基于视频扩散变换器（VDT）的关系模型来学习 IDF 的先验分布，并在推理阶段通过梯度优化将生成的运动引导至符合真实交互距离分布的状态。

**方法定位**：ROG 属于扩散生成 + 关系引导范式，其基础运动生成模型基于 **MDM**（Tevet et al., ICLR 2023）架构。与 **CHOIS**（Li et al., ECCV 2024）、**HOI-Diff**（Peng et al., arXiv 2023）等同期方法相比，ROG 的核心差异在于：将空间关系建模从隐式特征学习或固定接触点约束，显式地提升为可学习的 IDF 先验与去噪引导机制。

**主要结果**：在 FullBodyManipulation 数据集上，ROG 的 FID 达到 5.119，运动偏差 MDev 降至 5.815（对比 CHOIS 的 13.408），R-Precision Top-1 提升至 0.706。跨数据集验证（T2M-BEHAVE）显示碰撞率仅为 0.195，较 HOI-Diff 降低 24.6%。消融实验证实，物体关键点表示、IDF 损失和关系引导三个组件各自对运动质量和交互一致性均有显著贡献。



人-物交互（Human-Object Interaction, HOI）生成旨在根据文本描述合成人与物体协同运动的序列，在虚拟现实、机器人学习和动画制作中具有重要应用。然而，该任务面临一项核心瓶颈：**现有方法过度简化物体的几何表示**，通常仅使用物体质心或最近点来表征物体，忽略了物体的整体几何细节。这种简化导致复杂交互（如环绕物体操作、多阶段接触切换）中的空间关系建模不足，进而影响生成交互的真实感与语义对齐。

具体而言，基于扩散模型的方法如 **MDM**（Tevet et al., ICLR 2023）、**InterGen** 和 **HOI-Diff**（Peng et al., arXiv 2023）虽然在人体运动生成上取得了进展，但在HOI场景中，它们对物体几何的粗糙表示使得运动生成模型难以感知人与物体之间的精确空间关系。**CHOIS**（Li et al., ECCV 2024）引入了接触概率图，但仍依赖于简化的物体表示，在复杂交互中容易出现空隙、抖动和不自然接触等问题（Figure 3）。

上述方法在以下三个维度上存在系统性不足：

1. **物体几何表达不充分**：质心或最近点无法刻画物体的形状、轮廓和表面细节，导致生成的运动缺乏对物体整体结构的感知。
2. **空间关系建模缺失**：现有方法缺乏对人与物体之间时空距离分布的显式建模，难以捕捉交互过程中的动态关系变化。
3. **生成过程缺乏关系引导**：在去噪生成过程中，没有机制基于学习到的交互关系先验来校正运动预测，使得生成结果容易偏离真实的交互模式。

针对这些缺口，ROG 提出了一种基于丰富几何与关系引导的HOI生成框架。其核心洞察是：通过构建全面的**交互距离场（Interactive Distance Field, IDF）**，并利用扩散关系模型学习时空关系先验，可以在生成过程中对运动进行引导与校正，使生成的运动符合真实的交互距离分布。这一设计从根本上改变了HOI生成中“物体如何被表示”和“关系如何被利用”的方式，为提升交互真实感和语义对齐提供了新的技术路径。



## 核心方法与创新机理

ROG的核心创新在于将人-物交互（HOI）生成从“稀疏几何近似”推进到“密集几何关系场引导”的范式。现有方法（如**CHOIS** (Li et al., ECCV 2024)、**HOI-Diff** (Peng et al., arXiv 2023)）普遍将物体简化为质心或最近点，这种过度简化在复杂交互（如双手环抱、多阶段操作）中丢失了关键的几何约束，导致生成的运动出现穿透、抖动或语义不对齐。

ROG通过三个递进的“changed slots”系统性解决了上述瓶颈：

**1. 物体几何表示：从单点到密集关键点**

ROG摒弃了质心表示，提出了一种基于轴对齐包围盒（AABB）顶点与泊松圆盘采样（PDS）的混合关键点提取策略，为每个物体生成24个表面关键点（Section 3.2）。AABB的8个顶点捕获物体的全局轮廓，PDS采样的16个点则均匀覆盖物体表面，共同构成对物体几何的紧凑且全面的描述。这一表示使得模型能够感知物体的整体形状，而不仅仅是其空间位置。

**2. 空间关系表达：交互距离场（IDF）**

基于密集关键点，ROG构建了交互距离场（IDF）——一个维度为 $24 \times 24 \times N$ 的时空矩阵，其中元素 $\mathbf{D}_{i,j,n} = \left\| \mathbf{q}_{i,n} - \mathbf{p}_{j,n} \right\|_2^2$ 记录了第 $n$ 帧时第 $i$ 个人体关节与第 $j$ 个物体关键点之间的欧氏距离（Eq. 4）。IDF将人-物交互编码为高维时空关系张量，相比仅使用质心距离或接触概率图的基线方法，保留了丰富的局部几何交互信息。

**3. 关系建模与生成引导：扩散关系模型 + IDF引导**

ROG的核心因果机制在于引入了一个独立的**扩散关系模型**（Relation Model, R），该模型基于视频扩散变换器（VDT）架构，融合空间-时间自注意力机制，专门学习IDF的时空分布先验（Section 3.3）。在推理阶段，关系模型对运动生成模型（G）的初始预测IDF进行重建，输出精炼的IDF $\tilde{\mathbf{D}}$，并通过引导损失 $L_{\mathrm{guidance}} = \| \mathbf{D} - \tilde{\mathbf{D}} \|_2^2$ 对运动预测进行梯度优化（Eq. 11）。这一“生成-校验-修正”的闭环机制确保生成的运动在交互距离分布上与真实数据一致。消融实验证实，该引导仅在最后10个去噪步骤（$t \leq 0.01T$）应用且迭代次数 $k=10$ 时效果最佳（Supplementary Table 1, 2），全程引导反而导致性能下降。

**训练阶段的双重监督**

ROG在训练阶段直接将IDF损失 $\mathcal{L}_{\mathrm{IDF}}$ 引入运动生成模型的总损失 $\mathcal{L}_{\mathrm{m}} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{IDF}} \mathcal{L}_{\mathrm{IDF}}$（$\lambda_{\mathrm{IDF}}=5.0$，Eq. 8），使模型在训练过程中就内化了交互距离约束。这一设计使得即使不依赖推理时的引导，模型也能生成更合理的交互运动，而引导机制则在此基础上进一步精炼。

**创新性验证**

消融实验（Table 2）系统验证了各组件的因果贡献：添加物体关键点（obj-kp）使FID从9.775降至7.514；进一步添加IDF损失将R-Precision Top-1从0.547提升至0.666；使用完整距离矩阵 $\mathbf{D}$ 进行引导（FID 5.119）显著优于仅用质心 $\mathbf{C}$（FID 5.902）或无引导（FID 5.726）。跨数据集验证（Table 4）显示ROG的碰撞率（Coll% 0.195）比HOI-Diff（0.259）降低24.6%，证实了方法的鲁棒性与泛化能力。



ROG 的整体流程围绕“利用丰富几何信息构建交互距离场（IDF）以引导运动生成”这一核心思想展开。系统由三个关键模块构成：**运动生成模型 G**、**关系模型 R**，以及连接二者的 **IDF 计算与引导机制**。

### 输入与数据流

给定一个物体网格、一段文本描述和扩散时间步 $t$，ROG 首先从物体表面提取一组能全面表征其几何形状的关键点。具体而言，系统计算物体的轴对齐包围盒（AABB），选取其 8 个顶点，再通过泊松圆盘采样（PDS）在物体表面采样 16 个点，共获得 24 个物体关键点 $P = \{p_1, p_2, \dots, p_{24}\}$。同时，从 SMPL-X 人体模型中选取 24 个骨骼关键点 $Q = \{q_1, q_2, \dots, q_{24}\}$。这些关键点连同文本提示和扩散时间步，一并输入运动生成模型。

### 运动生成模型 G

运动生成模型 G 基于运动扩散模型（MDM, Tevet et al., ICLR 2023）构建。在去噪过程的每一步，G 预测出当前噪声状态对应的干净运动 $\tilde{\mathbf{m}}_0 = \{\tilde{\mathbf{m}}_{\mathrm{hm}}, \tilde{\mathbf{m}}_{\mathrm{obj}}\}$，包含人体运动和物体运动两部分。训练时，G 的优化目标由两部分组成：

$$
\mathcal{L}_{\mathrm{m}} = \mathcal{L}_{\mathrm{rec}} + \lambda_{\mathrm{IDF}} \mathcal{L}_{\mathrm{IDF}}
$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 为运动重建损失（预测运动与真实运动的 MSE），$\mathcal{L}_{\mathrm{IDF}}$ 为 IDF 损失（预测 IDF 与真实 IDF 的 MSE），权重 $\lambda_{\mathrm{IDF}} = 5.0$。IDF 损失在训练阶段直接监督 G，使其生成的运动不仅在关节层面准确，而且在人-物空间关系上符合真实分布。

### 交互距离场 IDF

IDF 是 ROG 的核心中间表示，它是一个 $24 \times 24 \times N$ 的三维矩阵（$N$ 为帧数），矩阵元素定义为：

$$
\mathbf{D}_{i,j,n} = \|\mathbf{q}_{i,n} - \mathbf{p}_{j,n}\|_2^2
$$

即第 $n$ 帧中第 $i$ 个人体关键点与第 $j$ 个物体关键点之间的欧氏距离。IDF 将人-物交互的空间关系编码为结构化的张量，为后续的关系建模和引导优化提供了统一的数学接口。

### 关系模型 R 与引导机制

关系模型 R 是一个扩散模型，采用视频扩散变换器（VDT）架构，融合空间自注意力和时间自注意力来捕获 IDF 中的时空模式。给定加噪后的 IDF 矩阵 $\mathbf{D}_t$，R 学习重建干净的真实 IDF $\mathbf{D}_0$，其训练损失为：

$$
\mathcal{L}_{\mathrm{D}} = \mathbb{E}_{\mathbf{D}_0, t} \|\mathbf{D}_0 - \tilde{\mathbf{D}}_0\|_2^2
$$

在推理阶段，G 首先生成初始运动 $\tilde{\mathbf{m}}_0$，据此计算当前 IDF $\mathbf{D}$。关系模型 R 以 $\mathbf{D}$ 为输入，输出一个“理想”的 IDF $\tilde{\mathbf{D}}$，代表学到的交互距离先验。随后，系统通过最小化引导损失来修正运动预测：

$$
L_{\mathrm{guidance}} = \|\mathbf{D} - \tilde{\mathbf{D}}\|_2^2
$$

该优化仅在去噪的最后 10 步（$t \leq 0.01T$）执行，使用 L-BFGS 优化器迭代 10 次更新 $\tilde{\mathbf{m}}_0$，使生成的交互运动在空间关系上趋近于真实分布。

### 模块协作关系

整个 pipeline 的协作逻辑可概括为：**G 负责生成候选运动，IDF 将运动转化为空间关系表征，R 提供关系先验以引导 G 的生成方向**。训练阶段，IDF 损失直接嵌入 G 的优化目标，使 G 初步具备关系感知能力；推理阶段，独立训练的关系模型 R 进一步细化 IDF，通过梯度引导使最终输出在语义对齐、物理合理性和交互自然性上达到更优平衡。这种“生成-关系建模-引导优化”的三段式设计，使得 ROG 在不显著增加训练成本的前提下（关系模型仅在推理时介入），实现了对复杂人-物交互的精细控制。

### 补充图表

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/001_Figure_1.jpg]]
*Figure 1: Our proposed ROG begins by leveraging rich geometric information to construct an Interactive Distance Field (IDF), effectively capturing the relational dynamics of Human-Object Interactions (HOI). It then utilizes the learned IDF prior to refine the generated motion’s IDF, guiding the motion generation process to produce movements that are both relation-aware and semantically aligned. For clarity, we simplify the visualization by displaying only four key points for each object*



ROG 的核心架构由三个关键模块构成：**运动生成模型**、**交互距离场（IDF）构建与监督**、以及**扩散关系模型与引导机制**。三者协同工作，形成“生成—评估—校正”的闭环。

### 运动生成模型

运动生成模型 $G$ 基于 **MDM**（Tevet et al., ICLR 2023）的扩散框架构建，负责根据文本描述和物体几何信息生成人-物运动序列。其扩散前向过程定义为：

$$q \left( \mathbf { m } _ { t } \mid \mathbf { m } _ { t - 1 } \right) = \mathcal { N } \left( \sqrt { \alpha _ { t } } \mathbf { m } _ { t - 1 } , \mathbf { \beta } ( 1 - \alpha _ { t } ) \mathbf { I } \right)$$

其中 $\mathbf{m}_t$ 表示扩散步 $t$ 时刻的噪声运动数据，$\alpha_t$ 控制噪声调度。模型通过预测去噪后的运动 $\tilde{\mathbf{m}}_0$ 来学习逆向过程，其基础重建损失为：

$$\mathcal { L } _ { \mathrm { r e c } } = \mathbb { E } _ { \mathbf { m } _ { 0 } , t } \left\| \mathbf { m } _ { 0 } - \tilde { \mathbf { m } } _ { 0 } \right\| _ { 2 } ^ { 2 }$$

该损失仅约束运动本身的数值精度，缺乏对交互空间关系的显式建模。

### 交互距离场（IDF）

为弥补上述不足，ROG 引入交互距离场（Interactive Distance Field, IDF）作为人-物空间关系的结构化表征。具体构建过程分为两步：

1. **关键点提取**：对物体，利用 AABB 包围盒的 8 个顶点结合泊松圆盘采样（PDS）在物体表面采样 16 个点，共获得 24 个物体关键点 $\mathbf{P} = \{\mathbf{p}_1, \dots, \mathbf{p}_{24}\}$；对人体，从 SMPL-X 模型中选取 24 个骨骼关键点 $\mathbf{Q} = \{\mathbf{q}_1, \dots, \mathbf{q}_{24}\}$。

2. **距离矩阵计算**：在每一帧 $n$，计算所有人-物关键点对之间的欧氏距离，构成一个 $24 \times 24 \times N$ 的三维矩阵：

$$\mathbf { D } _ { i , j , n } = \left\| \mathbf { q } _ { i , n } - \mathbf { p } _ { j , n } \right\| _ { 2 } ^ { 2 }$$

其中 $i, j$ 分别索引人体和物体关键点，$N$ 为总帧数。IDF 矩阵完整编码了交互过程中所有关键点对的时空距离演化。

在训练阶段，ROG 直接监督运动生成模型输出的 IDF 与真实 IDF 之间的一致性，定义 IDF 损失为：

$$\mathcal { L } _ { \mathrm { I D F } } = \mathbb { E } _ { \mathbf { m } _ { 0 } , t } \Vert \mathbf { D } _ { \mathrm { p r } } - \mathbf { D } _ { \mathrm { g t } } \Vert _ { 2 } ^ { 2 }$$

运动生成模型的最终训练损失为重建损失与 IDF 损失的加权和：

$$\mathcal { L } _ { \mathrm { m } } = \mathcal { L } _ { \mathrm { r e c } } + \lambda _ { \mathrm { I D F } } \mathcal { L } _ { \mathrm { I D F } }$$

其中 $\lambda_{\mathrm{IDF}} = 5.0$，确保交互空间约束在训练中具有足够的影响力。

### 扩散关系模型与引导机制

IDF 损失虽然提供了训练监督，但推理时模型缺乏对 IDF 先验分布的显式利用。为此，ROG 额外训练一个扩散关系模型 $R$，专门学习 IDF 矩阵的时空分布。

关系模型以扩散框架运作：输入加噪的 IDF 矩阵 $\mathbf{D}_t$，输出重建的干净 IDF $\tilde{\mathbf{D}}_0$。其训练损失为：

$$\mathcal { L } _ { \mathrm { D } } = \mathbb { E } _ { { \bf D } _ { 0 } , t } \left\| { \bf D } _ { 0 } - \tilde { \bf D } _ { 0 } \right\| _ { 2 } ^ { 2 }$$

模型架构采用视频扩散变换器（VDT），融合空间自注意力和时间自注意力机制，以高效捕获人-物关键点对在时空维度上的关系模式。

在推理阶段，引导机制将关系模型作为“交互合理性检验器”：从运动生成模型当前预测的运动中提取 IDF 矩阵 $\mathbf{D}$，输入关系模型获得精炼的 IDF $\tilde{\mathbf{D}}$，然后通过最小化引导损失来优化运动预测：

$$L _ { \mathrm { g u i d a n c e } } = \| \mathbf { D } - \tilde { \mathbf { D } } \| _ { 2 } ^ { 2 }$$

优化采用 L-BFGS 算法，仅在扩散去噪的最后 10 步（$t \leq 0.01T$）执行，每次引导迭代 $k=10$ 次。消融实验证实，这一选择性应用策略至关重要：全程引导反而导致性能下降，而仅在最后 10 步引导取得了 R-Precision top-3 0.902 的最佳结果。

### 物理一致性评估指标

为量化交互的物理合理性，ROG 引入运动偏差指标 MDev，衡量接触窗口内手部与物体顶点运动方向的一致性：

$$\mathrm { M D e v } = \frac { 1 } { n - m } \sum _ { t = m + 1 } ^ { n } \left\| \left( \hat { \mathbf { h } } _ { i } ^ { t } - \hat { \mathbf { h } } _ { i } ^ { t - 1 } \right) - \left( \hat { \mathbf { o } } _ { j } ^ { t } - \hat { \mathbf { o } } _ { j } ^ { t - 1 } \right) \right\|$$

其中 $\hat{\mathbf{h}}_i^t$ 和 $\hat{\mathbf{o}}_j^t$ 分别表示接触帧窗口 $[m, n]$ 内手部顶点和物体顶点的位置。MDev 值越低，表明手与物体的运动越协调，交互越自然。

### 补充图表

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/002_Figure_2.jpg]]
*Figure 2: Overview of ROG. Given an object, ROG first extracts key points that comprehensively represent the object’s geometry. These object key points, along with human key points, a text prompt, and the diffusion step t, are then input into ROG to generate human-object interactions that are semantically aligned with the text prompt. During each denoising step, the motion generation model initially produces movements*

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/014_Figure_3.jpg]]
*Figure 3: Our model generates semantically accurate and consistent human-object interactions across various objects*



## 实验与关键发现

### 主实验：FullBodyManipulation 数据集上的定量比较

ROG 在 FullBodyManipulation 数据集上与四个基线方法进行了系统比较，涵盖运动分布质量、文本对齐精度和物理合理性三个维度。Table 1 报告了核心结果。

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparisons on the FullBodyManipulation dataset [14]. We evaluate our model (ROG) by comparing it with four baseline models, as well as with real motions from the test set. The symbol ‘→’ means results closer to those of the real motions are considered better*

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/010_Table_1.jpg]]
*Table 1: Quantitative results showing the impact of guidance timesteps on generation performance during diffusion. Initiating IDF Guidance during the final 10 timesteps*

**运动质量与文本对齐。** ROG 取得了最低的 FID（5.119），略优于此前最优的 **CHOIS**（Li et al., ECCV 2024，FID 5.227）。在文本-运动对齐方面，ROG 的 R-Precision Top-1 达到 0.706，较 CHOIS 的 0.630 提升了 7.6 个百分点（相对提升 12.1%），表明 IDF 引导的生成运动与文本描述的语义一致性显著增强。

**物理合理性。** 运动偏差（MDev）是衡量接触窗口内手部与物体运动方向一致性的关键指标。ROG 的 MDev 仅为 5.815，而 CHOIS 为 13.408，降幅达 56.6%。这意味着 ROG 生成的交互中，手部运动与物体运动高度耦合，避免了“手滑脱”或“物体漂浮”等典型失败模式。接触率（Contact%）从 0.444 提升至 0.466，碰撞率（Collision%）从 0.208 微降至 0.200，两者均向真实运动（Real）的分布靠拢。

**跨数据集泛化验证。** 在 T2M-BEHAVE 数据集上的跨基准测试（Table 4）进一步验证了 ROG 的鲁棒性。尽管该数据集规模紧凑，ROG 的碰撞率仅为 0.195，相比 **HOI-Diff**（Peng et al., arXiv 2023）的 0.259 降低了 24.6%；MDev 为 10.784，远优于 HOI-Diff 的 24.807。这表明基于 IDF 的关系引导机制在不同数据分布下仍能有效约束空间合理性。

### 消融实验：各组件的因果贡献

Table 2 通过逐步叠加组件的方式，揭示了物体关键点、IDF 损失和引导机制各自的因果效应。

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/005_Table_2.jpg]]
*Table 2: Ablation study on the FullBodyManipulation dataset [14]. Starting with the baseline, we incrementally incorporate three components to evaluate their individual impact on HOI synthesis. ‘C’ denotes using a distance matrix that contains only the object centroid and human joints, while ‘D’ represents using a full distance matrix that includes both object key points and human joints (our proposed setting)*

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/008_Table_2.jpg]]
*Table 2: Effect of guidance iterations (k) on generation performance during the final 10 denoising steps. Increasing k enhances performance, with k = 10 achieving the best results*

**物体关键点（obj-kp）的作用。** 在基线模型（仅使用重建损失 $L_{rec}$）基础上引入物体关键点表示，FID 从 9.775 骤降至 7.514，R-Precision Top-1 从 0.538 提升至 0.547。这一改进验证了核心洞察：用 24 个 AABB 边界点与泊松圆盘采样点替代单一质心，能够更完整地捕捉物体几何，为空间关系建模提供更丰富的信息基础。

**IDF 损失的贡献。** 在物体关键点基础上添加 IDF 损失（$L_{IDF}$，权重 5.0），R-Precision Top-1 从 0.547 跃升至 0.666（提升 21.8%），接触率从 0.424 提升至 0.453。这表明直接监督交互距离场的重建，使运动生成模型在训练阶段就学会了维护合理的人-物空间关系，而非仅依赖事后引导。

**引导机制的关键性。** 使用完整距离矩阵 $D$（包含物体关键点与人体关节的全部配对距离）进行引导，FID 为 5.119；若仅使用质心距离 $C$ 进行引导，FID 升至 5.902；完全无引导时 FID 为 5.726。这证明引导信号的空间分辨率直接影响优化效果——完整的 24×24 IDF 矩阵比单一质心距离提供了更细粒度的空间约束。

**引导时机与迭代次数的敏感性。** 补充实验（Supplementary Table 1-2）揭示了两个关键超参数：
- **引导时机**：仅在最后 10 步去噪步骤（$t \leq 0.01T$）应用引导取得最佳性能（R-Precision Top-3 0.902），全程引导反而导致性能下降。这暗示早期去噪阶段运动结构尚未稳定，过早施加空间约束可能限制生成多样性。
- **引导迭代次数**：$k=10$ 时 L-BFGS 优化达到饱和，R-Precision Top-3 为 0.902，MDev 为 5.815。继续增加迭代不再带来增益。

### 定性分析与失败模式

Figure 3 的定性比较直观展示了各方法的差异。HOI-Diff 和 CHOIS 等基线方法在复杂交互中常出现以下失败模式：
- **空隙**：手部与物体表面之间留有明显空隙，表现为“悬空抓取”。
- **抖动**：接触帧间手部位置不稳定，产生高频抖动。
- **不自然接触**：手部穿透物体或接触点与文本语义不符（如“握住把手”时手部却在杯身）。

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative comparisons. We use circles to highlight incorrect interactions, illustrating that our method can generate more realistic and physically plausible interactions that align with the given text*

ROG 通过 IDF 引导有效缓解了上述问题，生成的运动在接触阶段手-物距离分布更接近真实数据。Figure 4 的消融可视化进一步证实：逐步添加物体关键点、IDF 损失和引导机制后，生成交互的连贯性和物理合理性递进改善。

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/006_Figure_4.jpg]]
*Figure 4: Ablation visual results. We systematically assemble the model, starting from a basic baseline and incrementally adding our innovative components*

### 效率与局限性

Table 5 报告了模型复杂度与推理效率。ROG 总参数量为 47.34M，推理时间 8.1 秒，相比 CHOIS（2.3 秒）和 MDM（Tevet et al., ICLR 2023，1.8 秒）明显更慢。额外开销主要来自关系模型的前向传播和 L-BFGS 迭代优化。这限制了 ROG 在实时交互场景中的直接部署。

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/012_Table_5.jpg]]
*Table 5: Comparison of model complexity and inference efficiency*

此外，当前框架仅生成全身粗粒度运动，未包含手指运动合成。这一局限源于 FullBodyManipulation 数据集缺乏手-物交互的细粒度标注。在具备手部细节的数据集上，将 IDF 扩展至手指关键点是一个自然的延伸方向，但需验证关系模型在更高维度距离场上的可扩展性。

### 补充图表

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/007_Table_4.jpg]]
*Table 4: T2M-BEHAVE [7] cross-benchmark tests: 24.6% lower collisions vs HOI-Diff (0.195 vs 0.259), despite dataset’s compact scale*

![[assets/figures/papers/paper_list_l1747_ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations/figures/013_Figure_2.jpg]]
*Figure 2: User study. We generated HOIs for 15 captions using 4 methods and asked 20 users to rank them by text alignment and realism. Our method outperforms others in both aspects*



## 定位与知识库关联

**ROG** 的核心贡献在于将人-物交互（HOI）生成中的物体几何表示从粗糙的质心/最近点提升为基于泊松圆盘采样（PDS）和边界点的24个关键点，并以此构建交互距离场（IDF）作为空间关系表达。该方法直接回应了现有基线方法在复杂交互中空间关系建模不足的瓶颈。

### 1. 与现有工作的关系

**ROG** 的运动生成基础模型基于 **MDM**（Tevet et al., ICLR 2023）的扩散框架，但在三个关键维度上进行了实质性扩展：

- **物体几何表示**：基线方法 **InterGen**、**HOI-Diff**（Peng et al., arXiv 2023）和 **CHOIS**（Li et al., ECCV 2024）普遍使用物体质心或最近点作为空间参考，忽略了物体的整体几何细节。ROG 通过提取 AABB 边界点与 PDS 采样点共24个关键点，实现了对物体几何的全面表征（Section 3.2）。消融实验（Table 2）证实，仅添加物体关键点（obj-kp）即可使 FID 从 9.775 降至 7.514。

- **空间关系表达**：现有方法依赖质心距离或接触概率图，而 ROG 构建了 $24 \times 24 \times N$ 的交互距离场（IDF）矩阵，完整捕获所有人-物关键点对在时间序列上的距离变化（Eq. 4）。这种表达方式将空间关系从标量/向量提升为结构化张量，为关系学习提供了更丰富的信息基础。

- **关系建模与引导**：ROG 引入基于视频扩散变换器（VDT）的扩散关系模型，学习 IDF 的先验分布，并在推理时通过梯度优化（L-BFGS）对运动预测进行引导校正。这种“生成-关系-引导”的三阶段架构在现有方法中未见先例。消融实验（Table 2）表明，使用完整距离矩阵 $\mathbf{D}$ 进行引导（FID 5.119）优于仅用质心 $\mathbf{C}$（FID 5.902）或无引导（FID 5.726）。

### 2. 适用边界

**ROG** 的设计适用于以下场景：
- 全身人-物交互生成，物体为刚体且具有明确的几何形状。
- 交互类型以操纵、搬运等粗粒度运动为主，文本描述可提供语义约束。
- 数据集需包含人体关节和物体运动的同步标注（如 FullBodyManipulation）。

**不适用或受限的场景**：
- 细粒度手指操作：当前框架仅生成全身粗粒度运动，未包含手指关节的合成。这受限于现有 HOI 数据集缺乏手-物交互的精细标注。
- 非刚体或可变形物体的交互：IDF 依赖固定的物体关键点，难以适应形状变化的物体。
- 实时应用：引导机制在推理时增加了额外计算量（总参数 47.34M，推理时间 8.1 秒），相比基线方法较慢。

### 3. 局限

1. **手指运动缺失**：当前框架未包含细粒度手指运动合成，仅生成全身粗粒度运动。这是方法层面的主动简化，而非数据限制的被动结果——即使未来有手指标注数据，框架也需要扩展 IDF 以包含手指关键点。

2. **推理效率**：引导机制在推理时通过 L-BFGS 迭代优化运动预测，增加了计算开销。尽管消融实验（Supplementary Table 2）表明 k=10 次迭代即可达到最佳性能，但整体推理时间仍显著高于无引导的基线。

3. **数据集依赖性**：方法在 FullBodyManipulation 数据集上训练和验证，该数据集包含有限的物体类别和交互类型。跨数据集验证（Table 4）在 T2M-BEHAVE 上展示了泛化能力，但该数据集规模紧凑，更广泛场景下的性能仍有待验证。

4. **物体关键点数量的敏感性**：论文固定使用 24 个物体关键点（8 个 AABB 边界点 + 16 个 PDS 采样点），未系统探讨关键点数量对性能的影响。对于几何复杂度差异大的物体（如球体 vs. 复杂工具），固定数量的关键点可能不是最优选择。

### 4. 开放问题

1. **手指交互的扩展**：如何将 IDF 扩展至包含手指关键点，以在适当数据集上支持手部操作生成？这需要重新设计关键点选择和 IDF 矩阵结构，以及可能的关系模型架构调整。

2. **大规模手物交互数据的适应**：当有大规模且包含手部细节的数据集可用时，当前框架能否无缝适应并生成高保真手物交互？关系模型对高维 IDF 的扩展能力是关键瓶颈。

3. **计算成本优化**：能否通过模型蒸馏或轻量化设计进一步降低关系模型和引导过程的计算成本？引导仅在最后 10 步去噪步骤（t ≤ 0.01T）应用（Supplementary Table 1），暗示关系模型的能力存在冗余，可能通过更紧凑的架构实现类似效果。

4. **泛化能力**：方法在更多样化的物体类别、动态场景和多主体交互任务中的泛化能力如何？IDF 的表达能力和关系模型的先验学习是否能够覆盖更广泛的交互模式，仍需进一步验证。

5. **与物理仿真的结合**：当前方法通过 IDF 引导隐式地改善物理合理性（如碰撞率降低），但未显式结合物理约束。将 IDF 引导与物理仿真器结合，可能进一步提升交互的物理真实感。



## 原文 PDF

![[paperPDFs/CVPR_2025/ROG_Guiding_Human_Object_Interactions_with_Rich_Geometry_and_Relations.pdf]]
