---
title: "Affostruction: 3D Affordance Grounding with Generative Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Affostruction_3D_Affordance_Grounding_with_Generative_Reconstruction.pdf
project_link: "https://chrockey.github.io/Affostruction/"
code_link: null
aliases:
- Affostruction
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 利用多视图RGBD的深度信息进行稀疏体素融合，以恒定计算复杂度实现生成式几何重建；在此基础上通过流匹配模型显式建模可供性分布的多模态性，从而在重建的完整形状上进行精准的可供性定位。
primary_logic: 将生成式3D重建与可供性定位统一在稀疏体素空间，通过流匹配捕捉可供性的多模态分布，并利用预测的热力图引导主动视图选择，持续提升对功能性区域的覆盖。
claims:
- 在Toky4K数据集上，Affostruction的3D重建IoU达到32.67，比最强的RGBD重建方法MCC（21.11）提升54.8%。
- 在完整几何设置下，Affostruction在Affogato上的可供性定位aIoU为19.1，比先前最好的Espresso-3D（13.6）提升40.4%。
- 在仅提供部分观察的条件下，Affostruction达到9.26 aIoU，几乎是两阶段管线MCC+Espresso-3D（4.74）的两倍。
- 随机多视图训练使模型能够有效利用额外视图，重建性能随视图数增加持续提升，而单视图训练模型几乎无法从多视图推理中获益。
---

# Affostruction: 3D Affordance Grounding with Generative Reconstruction

> [!tip] 核心洞察
> 将生成式3D重建与可供性定位统一在稀疏体素空间，通过流匹配捕捉可供性的多模态分布，并利用预测的热力图引导主动视图选择，持续提升对功能性区域的覆盖。

| 字段 | 内容 |
|------|------|
| 中文题名 | Affostruction：基于生成式重建的3D可供性定位 |
| 英文题名 | Affostruction: 3D Affordance Grounding with Generative Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.09211) · [Project](https://chrockey.github.io/Affostruction/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Affostruction |
| Dataset | Toky4K, Affogato |

> [!tip] 效果简介
> - Toky4K (3D reconstruction) 上，IoU 32.67 vs 21.11 (MCC) (+11.56 (+54.8%))；Chamfer Distance 0.2427 vs 0.3299 (MCC) (-0.0872 (-26.4%))。
> - Affogato (complete geometry) 上，aIoU 19.1 vs 13.6 (Espresso-3D) (+5.5 (+40.4%))。
> - Affogato (partial observation) 上，aIoU 9.26 vs 4.74 (MCC + Espresso-3D) (+4.52 (+95.4%))。

## 概述

3D可供性定位（3D affordance grounding）旨在从三维物体上识别出与特定交互功能对应的区域（如“可以抓握的把手”），是机器人理解并操作物体的关键能力。然而，现有方法普遍存在一个根本瓶颈：它们仅能从可见表面预测可供性区域，无法推理被遮挡部分的几何结构与功能。在真实场景中，机器人往往只能获得部分观测，大量功能性区域可能被遮挡，导致现有方法在部分观察条件下的可供性定位能力严重受限。

针对这一问题，本文提出 **Affostruction**，一种基于生成式重建的3D可供性定位框架。其核心洞见是：**将生成式3D重建与可供性定位统一在稀疏体素空间，通过流匹配捕捉可供性的多模态分布，并利用预测的热力图引导主动视图选择，持续提升对功能性区域的覆盖**。具体而言，Affostruction 包含三个紧密耦合的阶段：（1）**生成式多视图重建**——利用多视图RGBD的深度信息进行稀疏体素融合，以恒定计算复杂度实现从部分观察到完整几何的生成式重建；（2）**基于流的可供性定位**——在重建的完整形状上，以自然语言查询为条件，通过流匹配模型显式建模可供性分布的多模态性，生成精确的可供性热力图；（3）**可供性驱动的主动视图选择**——根据预测的热力图计算候选视角的功能可见度得分，自主选择下一最优观察位置，持续提升对功能性区域的覆盖。

实验结果表明，Affostruction 在多项基准上显著超越了现有方法。在 Toky4K 数据集上，其3D重建 IoU 达到 **32.67**，比最强的 RGBD 重建方法 MCC（21.11）提升 **54.8%**；在 Affogato 数据集上，完整几何条件下的可供性定位 aIoU 为 **19.1**，比先前最好的 Espresso-3D（13.6）提升 **40.4%**。更重要的是，在仅提供部分观察的条件下，Affostruction 达到 **9.26** aIoU，几乎是两阶段管线 MCC+Espresso-3D（4.74）的两倍，充分验证了生成式重建对可供性定位的关键增益。此外，随机多视图训练策略使模型能够有效利用额外视图持续提升性能，而可供性驱动的主动视图选择在仅增加一个视图时即达到 9.2 aIoU，相比顺序采样提速约 **2 倍**。

在方法定位上，Affostruction 区别于传统的判别式可供性预测方法（如 **OpenAD**（Nguyen et al., IROS 2023）、**PointRefer**（Li et al., CVPR 2024）），通过流匹配的生成式框架捕获可供性的多模态分布；同时，相较于仅依赖单视图RGB的3D生成模型（如 **TRELLIS**（Xiang et al., CVPR 2025）），Affostruction 创新性地引入多视图RGBD稀疏体素融合，在保持恒定计算复杂度的同时实现了面向真实物体朝向的重建。该方法在仿真数据集上展现了强大的性能，但其在真实机器人操作任务中的有效性、以及在严重遮挡场景下的鲁棒性仍需进一步验证。

## 背景与动机

### 3D可供性定位的核心挑战

可供性（affordance）描述了物体为智能体提供的交互可能性——例如“坐”对应椅面、“抓握”对应把手。在机器人操作场景中，准确识别物体上的功能性区域是执行抓取、放置、推动等操作的前提。然而，真实环境中的感知总是片面的：机器人通常只能从有限视角获得物体的部分观察，大量功能性区域可能处于被遮挡状态。

这一约束暴露了现有3D可供性定位方法的结构性缺陷：**它们仅能在可见表面上预测可供性区域，无法推理被遮挡部分的几何结构与功能属性**。当目标交互区域恰好位于不可见面时，这类方法将完全失效。这一瓶颈的根本原因在于，现有方法缺少从部分观察中恢复完整3D几何的能力，从而将可供性推理限制在了不完整的物体表征之上。

### 现有方法的两个缺口

当前解决3D可供性定位的技术路线可分为两类，但各自存在明显局限：

**判别式可供性预测方法**（如 **OpenAD** (Nguyen et al., IROS 2023)、**PointRefer** (Li et al., CVPR 2024)、**Espresso-3D** (Lee et al., arXiv 2025)）直接从输入的3D几何上输出单一确定性可供性区域。这类方法虽然在完整几何输入下表现良好，但缺乏生成能力，无法处理部分观察场景。更重要的是，它们将可供性建模为确定性映射，忽略了功能性区域天然的多模态性——同一物体可能同时具有多个可抓握位置，单一输出无法捕捉这种分布。

**两阶段管线方法**将3D重建与可供性预测串联，先用重建模型（如 **MCC** (Wu et al., CVPR 2023)）从RGBD观测恢复完整几何，再在重建结果上运行可供性模型。这种方案理论上可以解决遮挡问题，但存在两个深层缺陷：其一，重建误差会直接传播到可供性预测阶段，而两个阶段独立训练，缺乏联合优化；其二，重建模型不具备可供性感知能力，无法根据任务需求优先恢复功能相关区域。

### 本文的核心动机

Affostruction的核心洞察在于：**3D重建与可供性定位不应是割裂的两个阶段，而应统一在同一生成式框架下**。具体而言，本文提出以下关键主张：

1. **生成式重建是解决遮挡问题的必要前提**：只有恢复完整几何，才能在不可见面区域进行可供性推理。这要求重建模型具备从稀疏观察中外推未知结构的能力，而非仅做表面插值。

2. **可供性具有天然的多模态性，需要生成式建模**：一个物体可能拥有多个功能等价区域（如杯子的多个抓握点），判别式模型的单点预测无法刻画这种分布。流匹配（flow matching）框架提供了显式建模可供性热力图分布的数学工具。

3. **可供性信息应反向指导感知过程**：如果已知哪些区域具有功能价值，机器人应主动选择能最大化这些区域可见度的视角。这种可供性驱动的主动视图选择构成了感知-推理-行动的闭环。

基于这些动机，Affostruction将三个模块——生成式多视图重建、基于流的可供性定位、可供性驱动的主动视图选择——整合为统一的稀疏体素空间中的端到端流程，在部分观察条件下实现了显著优于两阶段管线的可供性定位精度。

## 核心创新

Affostruction 的核心创新在于将**生成式3D重建**与**可供性定位**统一在稀疏体素空间，并通过**流匹配**显式建模可供性的多模态分布，从而在部分观察条件下实现对完整物体几何与功能性交互区域的联合推理。与现有方法相比，该方法在四个关键维度上实现了根本性改变。

### 1. 从单视图生成到多视图RGBD重建的输入模态跃迁

现有3D生成方法（如 **TRELLIS** (Xiang et al., CVPR 2025)、**Shap-E** (Jun & Nichol, arXiv 2023)、**InstantMesh** (Xu et al., arXiv 2024)）依赖单视图RGB图像作为输入，缺乏深度信息与多视角几何约束，导致生成结果与真实物体位姿不一致。Affostruction 将输入模态扩展为**多视图RGBD图像**，同时利用深度图与相机内外参数，使重建结果与物体实际朝向对齐。这一改变使得模型能够从部分观察中推断被遮挡的几何结构，而非仅依赖单视图的先验分布进行“猜测”。

### 2. 稀疏体素融合：恒定复杂度的多视图特征聚合

多视图输入面临的核心挑战是计算复杂度随视图数量线性增长。Affostruction 提出**稀疏体素融合**（Sparse Voxel Fusion）策略：将各视图的 DINOv2 特征通过深度投影到3D空间，聚合为恒定大小的稀疏体素表征，并加入3D正弦位置编码，构成重建流变换器的条件输入：

$$\mathbf { C } _ { \mathrm { v o x e l } } = \{ \bar { \mathbf { f } } _ { m } + \mathrm { P E } _ { 3 \mathrm { D } } ( \mathbf { p } _ { m } ) \} _ { m = 1 } ^ { M }$$

与简单的 token 拼接或固定坐标融合相比，该策略在保持恒定计算复杂度的同时，取得了最高的重建 IoU（Table 4 消融实验证实）。这使得模型能够高效利用任意数量的观测视图，而不受显存或计算时间的线性增长限制。

### 3. 随机多视图训练：解锁多视图推理的增益能力

传统单视图训练模型在多视图输入时几乎无法获益——Figure 4 显示，单视图训练的模型在增加输入视图后重建 IoU 几乎无提升。Affostruction 采用**随机多视图训练**策略：每个训练迭代随机采样 1–8 个视图，迫使模型学会利用任意数量的观测信息。这一训练范式的改变使得模型在推理时能够从额外视图中获得持续且稳定的性能提升，是支撑后续主动视图选择的关键基础。

### 4. 从判别式到生成式的可供性预测框架

现有可供性定位方法（如 **Espresso-3D** (Lee et al., arXiv 2025)、**OpenAD** (Nguyen et al., IROS 2023)、**PointRefer** (Li et al., CVPR 2024)）采用判别式模型，输出单一确定性的可供性区域，无法捕捉功能性交互固有的多模态性——同一物体可能在不同位置支持同一功能（如“抓取”可发生在多个把手处）。Affostruction 引入基于**流匹配（rectified flow）的生成式模型**，在重建的稀疏体素上以 CLIP 文本嵌入为条件，生成可供性概率热力图分布：

$$\mathbf { C } _ { \mathrm { t e x t } } = \mathbf { C } \mathbf { L } \mathbf { I } \mathbf { P } _ { \mathrm { t e x t } } ( q )$$

训练目标采用**二值掩码损失**替代传统 MSE，结合二值交叉熵与 Dice 损失，分别提供逐点监督和区域级优化：

$$\mathcal { L } _ { \mathrm { m a s k } } ( \mathbf { A } ^ { \prime } , \mathbf { A } ) = \mathcal { L } _ { \mathrm { B C E } } ( \mathbf { A } ^ { \prime } , \mathbf { A } ) + \mathcal { L } _ { \mathrm { D i c e } } ( \mathbf { A } ^ { \prime } , \mathbf { A } )$$

$$\mathcal { L } _ { \mathrm { C F M } } ( \theta ) = \mathbb { E } _ { t , \mathbf { A } _ { 0 } , \epsilon } \left[ \mathcal { L } _ { \mathrm { m a s k } } ( \epsilon - v _ { \theta } ( \mathbf { A } _ { t } , \mathbf { C } _ { \mathrm { t e x t } } , t ) , \mathbf { A } _ { 0 } ) \right]$$

这一设计使得模型能够显式建模可供性的多模态分布，而非仅输出单一预测。

### 5. 可供性驱动的主动视图选择

传统方法缺乏主动视图选择机制，仅按固定顺序或随机采样下一观测视角。Affostruction 提出**可供性驱动的主动视图选择**策略：根据当前预测的可供性热力图渲染多视角图像，计算每个候选视角的可供性可见度得分：

$$\boldsymbol { S } ( \pi _ { i } , \mathcal { M } ) = \sum _ { u , v } \boldsymbol { A } _ { \mathrm { r e n d e r } } ( u , v )$$

并选择得分最高的视角作为下一观测位置：

$$\pi ^ { * } = \arg \operatorname*{ m a x } _ { \pi _ { i } \in \Pi } S ( \pi _ { i } , { \mathcal { M } } )$$

该策略优先观察高可供性区域，使模型能最快获取与功能性交互相关的几何信息。Figure 5 证实，在仅增加一个视图时，可供性驱动选择即达到 9.2 aIoU，相比顺序采样提升速度快约 2 倍。

### 创新归纳

上述五项创新形成了完整的因果链条：**多视图RGBD输入**提供深度几何约束，**稀疏体素融合**保证恒定计算复杂度，**随机多视图训练**解锁多视图推理增益，**生成式可供性预测**捕获多模态分布，**主动视图选择**持续优化对功能性区域的覆盖。这一链条使得 Affostruction 在部分观察条件下达到 9.26 aIoU，几乎是两阶段管线 MCC+Espresso-3D（4.74）的两倍，从根本上解决了现有方法无法推理被遮挡部分几何与功能的瓶颈。

## 整体框架

Affostruction 的整体流程由三个协同阶段构成，如图2所示：**生成式多视图重建**、**基于流的可供性定位**和**可供性驱动的主动视图选择**。三阶段共享统一的稀疏体素表征空间，使几何推理与功能推理在恒定计算复杂度下紧密耦合。

### 输入与输出流

系统接收多视图 RGBD 图像序列作为输入，每帧附带深度图与相机内、外参数。初始观测通常仅覆盖物体的部分表面，功能性交互区域可能被严重遮挡（图1蓝色相机）。经过三阶段处理后，系统输出：完整的三维几何网格、自然语言查询对应的可供性热力图，以及推荐的下一个最优观测视角（图1绿色相机）。

### 阶段一：生成式多视图重建

该阶段负责从部分 RGBD 观测中生成完整的物体几何。核心操作是**稀疏体素融合**：利用深度图将每帧的 DINOv2 patch 特征投影到三维空间，在稀疏体素网格中聚合为固定大小的条件信号 $C_{\text{voxel}}$（公式2），并附加 3D 正弦位置编码。融合后的体素特征送入流变换器，通过条件流匹配目标（公式1）从噪声中逐步重建出完整的稀疏体素结构。该结构随后由预训练的解码器 **TRELLIS**（Xiang et al., CVPR 2025）解码为密集几何。

关键设计在于**随机多视图训练**：每个训练迭代随机采样 1–8 个视角，迫使模型学会利用任意数量的观测进行推理。这使得推理时增加视图能持续提升重建质量，而单视图训练的模型几乎无法从多视图中获益（图4）。

### 阶段二：基于流的可供性定位

在阶段一重建的完整稀疏体素上，该阶段以自然语言查询为条件，生成可供性概率热力图。文本查询 $q$ 经 CLIP 文本编码器转换为嵌入 $C_{\text{text}}$（公式3），作为新的稀疏流变换器的条件输入。与阶段一不同，该阶段的流匹配目标采用**二值掩码损失**（公式4–5），结合 BCE 与 Dice 损失，分别提供逐点监督和区域级优化，显式建模可供性分布的多模态性。

### 阶段三：可供性驱动的主动视图选择

基于阶段二预测的可供性热力图，系统从候选视角集合中渲染每个视角的可供性网格图像，计算**可供性可见度得分** $S(\pi_i, \mathcal{M})$（公式6）——即渲染图像中所有像素可供性热力值的总和。选择得分最高的相机位姿 $\pi^*$（公式7）作为下一观测视角，优先观察高可供性区域。新增的观测通过多视图融合反馈回阶段一，迭代提升重建与可供性定位质量（图A2）。

### 模块间关系

三个阶段并非简单的线性级联，而是通过**稀疏体素空间**形成紧耦合：阶段一的输出体素直接作为阶段二的输入几何载体；阶段二的预测热力图驱动阶段三的视角选择；阶段三获取的新观测又通过多视图融合更新阶段一的体素表征。这种闭环设计使得几何重建与功能定位相互增强——更完整的几何带来更准确的可供性预测，而可供性引导的视角选择又针对性地补全功能性区域的几何信息。

### 补充图表

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/001_Figure_1.jpg]]
*Figure 1: Affostruction. Given an initial RGBD observation (blue camera) where functional regions for an affordance query (e.g., “attach a light fixture”) are only partially visible or heavily occluded, we reconstruct the complete 3D geometry in a generative manner – estimating unobserved surfaces – and ground an affordance region on the full shape effectively. Building on this, an affordance-driven active view selection strategy identifies the most informative next viewpoint (green camera). The additional observation acquired from this selected view further refines both the 3D reconstruction and the affordance grounding of the target region*

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/002_Figure_2.jpg]]
*Figure 2: Affostruction overview. Our approach consists of three stages. (1) Generative multi-view reconstruction: DINOv2 [30] features from RGBD views are fused into sparse voxels using depth and camera parameters, and a flow transformer extrapolates complete structure from partial observations, decoded via a pretrained decoder [45]. (2) Flow-based affordance grounding: a sparse flow transformer conditioned on CLIP [32]-encoded text generates affordance heatmaps over reconstructed geometry. (3) Affordance-driven active view selection: next-best viewpoints maximize visibility of high-affordance regions, and a mesh decoder [45] produces the final 3D mesh*

## 核心模块与公式推导

Affostruction 由三个级联模块构成：生成式多视图重建、基于流的可供性定位，以及可供性驱动的主动视图选择。前两个模块共享稀疏体素表征，第三个模块则利用预测的可供性热力图指导下一最优视角的选取。

### 生成式多视图重建

该模块以 **TRELLIS**（Xiang et al., CVPR 2025）的流变换器为骨干，将其从单视图 RGB 生成扩展为多视图 RGBD 重建。核心改造在于稀疏体素融合策略：对每帧 RGBD 观测，先提取 DINOv2 patch 特征，再利用深度图和相机外参将 2D 特征反投影到 3D 空间。落入同一体素的所有特征取均值，形成该体素的聚合特征 $\bar{\mathbf{f}}_m$，并叠加上 3D 正弦位置编码 $\mathrm{PE}_{3\mathrm{D}}(\mathbf{p}_m)$，构成恒定大小的条件信号：

$$\mathbf{C}_{\mathrm{voxel}} = \{\bar{\mathbf{f}}_m + \mathrm{PE}_{3\mathrm{D}}(\mathbf{p}_m)\}_{m=1}^{M}$$

其中 $M$ 为非空体素数，$\mathbf{p}_m$ 为体素中心坐标。该融合策略的计算复杂度仅取决于稀疏体素数量，与输入视图数无关，从而在多视图场景下保持恒定开销。

训练采用随机多视图策略：每个迭代从 1–8 个视图中随机采样，迫使模型学习利用任意数量的部分观测进行生成式重建。基础流变换器通过条件流匹配（CFM）目标训练：

$$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, \mathbf{X}_0, \epsilon}\left[||v_\theta(\mathbf{X}_t, \mathbf{C}, t) - (\epsilon - \mathbf{X}_0)||_2^2\right]$$

其中 $\mathbf{X}_t = t\mathbf{X}_0 + (1-t)\epsilon$ 在干净结构 $\mathbf{X}_0$ 与噪声 $\epsilon$ 之间插值，$v_\theta$ 预测速度场，$\mathbf{C}$ 为上述稀疏体素条件。推理时通过 ODE 求解器从噪声逐步去噪生成完整几何。

### 基于流的可供性定位

在重建的稀疏体素上，该模块以自然语言查询为条件生成可供性概率热力图。文本查询 $q$ 通过预训练 CLIP 文本编码器转换为嵌入：

$$\mathbf{C}_{\mathrm{text}} = \mathrm{CLIP}_{\mathrm{text}}(q)$$

随后，一个新的稀疏流变换器以 $\mathbf{C}_{\mathrm{text}}$ 为条件，在重建体素上生成可供性热力图分布。与结构生成阶段不同，此处将 CFM 中的 MSE 损失替换为二值掩码损失，以更好地优化空间定位精度：

$$\mathcal{L}_{\mathrm{mask}}(\mathbf{A}', \mathbf{A}) = \mathcal{L}_{\mathrm{BCE}}(\mathbf{A}', \mathbf{A}) + \mathcal{L}_{\mathrm{Dice}}(\mathbf{A}', \mathbf{A})$$

其中 $\mathcal{L}_{\mathrm{BCE}}$ 提供逐体素的二值交叉熵监督，$\mathcal{L}_{\mathrm{Dice}}$ 提供区域级优化。最终可供性流变换器的训练目标为：

$$\mathcal{L}_{\mathrm{CFM}}(\theta) = \mathbb{E}_{t, \mathbf{A}_0, \epsilon}\left[\mathcal{L}_{\mathrm{mask}}(\epsilon - v_\theta(\mathbf{A}_t, \mathbf{C}_{\mathrm{text}}, t), \mathbf{A}_0)\right]$$

这里 $\mathbf{A}_0$ 为真值二值可供性掩码，$\mathbf{A}_t$ 为加噪版本。流匹配框架使模型能够显式建模可供性区域的多模态分布——同一物体上“可抓取”的区域可能有多处，判别式方法只能输出单一确定解，而生成式方法可捕获这种内在歧义。

### 可供性驱动的主动视图选择

给定当前重建网格 $\mathcal{M}$ 及其预测可供性热力图，该模块从候选相机位姿集合 $\Pi$ 中选择下一最优视角。对每个候选位姿 $\pi_i$，渲染可供性网格得到图像 $\mathbf{A}_{\mathrm{render}}$，计算其可供性可见度得分：

$$\boldsymbol{S}(\pi_i, \mathcal{M}) = \sum_{u,v} \mathbf{A}_{\mathrm{render}}(u,v)$$

即渲染图像中所有像素的可供性热力值之和。下一最优视角选取为使该得分最大化的位姿：

$$\pi^* = \arg\max_{\pi_i \in \Pi} S(\pi_i, \mathcal{M})$$

该策略优先观察高可供性区域，从而以更少的新增视图快速提升可供性定位质量。消融实验表明，在仅增加一个视图时，可供性驱动选择即达到 9.2 aIoU，相比顺序采样提升速度快约 2 倍（Figure 5）。

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/008_Figure_5.jpg]]
*Figure 5: Quantitative results of active view selection. Affordance grounding quality (aIoU) as views are incrementally added from minimal affordance visibility. Affordance-driven selection (red) achieves the fastest improvement, sequential sampling (blue) improves slowest due to its fixed trajectory, and random sampling (green) converges with active selection given more views*

### 补充图表

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/007_Figure_4.jpg]]
*Figure 4: Impact of multi-view training. Reconstruction IoU as a function of input views. Single-view trained models (left) show minimal gains from additional views at inference, while stochastic multi-view training (right) enables consistent improvement. Our sparse voxel fusion achieves the best performance in both settings*

## 实验与分析

### 核心定量结果

Affostruction在3D重建与可供性定位两个核心任务上均显著超越先前方法，验证了生成式重建与可供性定位在统一稀疏体素空间中的协同优势。

**3D重建任务**（Toky4K数据集，Table 1）：在仅利用RGBD多视图输入的设定下，Affostruction取得了32.67的体素IoU，相比最强的RGBD重建方法**MCC**（Wu et al., CVPR 2023）的21.11提升了54.8%；Chamfer Distance从0.3299降至0.2427，降幅达26.4%。值得注意的是，Affostruction甚至大幅超越了基于RGB的生成式方法**TRELLIS**（Xiang et al., CVPR 2025）的19.49 IoU（提升67.6%），表明深度条件与稀疏体素融合为生成式重建提供了比纯RGB生成更强的几何先验。

**完整几何可供性定位**（Affogato数据集，Table 2）：在给定真值完整几何的设定下，Affostruction取得了19.1的aIoU，比此前最优方法**Espresso-3D**（Lee et al., arXiv 2025）的13.6提升40.4%。这一提升归因于流匹配模型对可供性多模态分布的显式建模能力——同一物体上“可抓取”区域可能存在多个合理位置，判别式模型难以捕捉这种一对多映射。

**部分观察可供性定位**（Affogato数据集，Table 3）：这是最能体现方法核心价值的设定。当仅提供单视图RGBD部分观测时，Affostruction达到9.26 aIoU，几乎是两阶段管线**MCC + Espresso-3D**（4.74）的两倍。无重建能力的**OpenAD**（Nguyen et al., IROS 2023）和**PointRefer**（Li et al., CVPR 2024）仅能在可见表面上预测可供性，aIoU分别仅为4.13和3.99。这一对比直接验证了核心瓶颈假设：仅从可见表面预测可供性严重限制了机器人在部分观察下的交互理解能力，而生成式重建能够推理被遮挡区域的几何与功能。

### 消融实验

**随机多视图训练的关键作用**（Figure 4）：在单视图训练模式下，模型在推理时即使获得额外视图，重建IoU几乎无增益，甚至出现性能退化。而采用随机多视图训练（每迭代随机采样1–8个视图）后，模型能够有效利用额外观测，重建IoU随视图数量增加持续提升。这一发现表明，多视图融合能力需要通过显式的训练策略来习得，而非模型架构的固有属性。

**稀疏体素融合的恒定复杂度优势**（Figure 4, Table 4）：与token拼接和固定坐标融合两种替代策略相比，稀疏体素融合在多视图条件下保持恒定计算复杂度，同时取得了最高的重建IoU。这一设计使得Affostruction在单张RTX A6000上的总运行时间仅为7.20秒，远低于两阶段管线MCC+Espresso-3D的12.16秒（Table 4）。

**采样步数消融**（Figure A1）：重建质量在5个采样步数时趋于饱和，继续增加步数几乎不再提高IoU。5步采样仅需0.25秒，比TRELLIS默认的25步（1.29秒）快约5倍，为实际部署提供了显著的效率优化空间。

**可供性驱动的主动视图选择**（Figure 5）：在初始仅提供最小可供性可见度的设定下，可供性驱动的选择策略仅需增加1个视图即可达到9.2 aIoU，相比顺序采样提升速度快约2倍。随机采样在足够多视图后也能收敛到相近水平，但效率明显低于主动策略。这验证了基于预测热力图引导视图选择的有效性：系统能够主动观察高可供性区域，从而更快地提升功能性定位精度。

### 失败模式分析

Figure 7揭示了两个典型的失败模式：

1. **严重遮挡下的误差传播**：当初始视角存在严重遮挡时，重建阶段无法准确推断被遮挡部分的几何结构，导致可供性预测在错误的重建几何上进行，定位精度显著下降。这暴露了重建与可供性预测之间的强耦合依赖性——重建不完整时可能漏掉被遮挡的关键交互区域。

2. **错误可供性定位误导视图选择**：错误的初始可供性定位会误导主动视图选择策略，使后续观察偏离真实目标区域，形成误差的级联放大。这一失败模式揭示了当前方法缺乏自我纠错机制——系统无法识别不可靠的预测并主动调整策略。

### 扩展到多物体场景

Figure 6展示了Affostruction结合**SAM3D**进行多物体场景处理的流程：首先通过SAM3D对场景进行对象分割与独立重建，然后在每个分割出的物体上独立施加可供性定位。这一扩展验证了方法的模块化设计，但也暴露了其对预分割模块的依赖性——在无需预分割的复杂场景中直接工作仍是待解决的问题。

### 效率对比

Table 4汇总了各方法在单张RTX A6000上的运行时间与显存占用。Affostruction以7.20秒的总运行时间实现了最快的推理速度，同时保持与基线方法相当的显存占用。两阶段管线MCC+Espresso-3D因需要分别运行重建和可供性预测两个独立模型，总耗时达到12.16秒。这一效率优势源于稀疏体素空间中的统一处理——重建与可供性定位共享3D表征，避免了显式的数据转换开销。

### 补充图表

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/003_Table_1.jpg]]
*Table 1: 3D reconstruction results on Toky4K [37]. We compare RGB-to-3D generation models and MCC [44], an RGBD-to-3D reconstruction model. Since MCC does not produce mesh outputs, rendering-based metrics (PSNR, LPIPS) are not available*

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/004_Table_2.jpg]]
*Table 2: Complete 3D affordance grounding results on Affogato [15]. All methods receive ground-truth complete geometry as input. aIoU is the primary metric for spatial localization*

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/005_Table_3.jpg]]
*Table 3: Partial 3D affordance grounding results on Affogato [15]. Methods without reconstruction predict affordances only on observed surfaces. Two-stage pipelines pair a reconstruction model with a pretrained affordance model*

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative results on partial 3D affordance grounding. Affostruction reconstructs complete geometry and grounds affordances throughout entire objects from single RGBD views. Despite limited observations, our method predicts affordances on occluded regions, demonstrating the ability to reason about 3D functional interactions even when large portions of objects are unobserved*

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/009_Figure_6.jpg]]
*Figure 6: Extension to multi-object scenes. Given a multi-object scene, SAM3D [34] reconstructs and segments individual objects, and our method grounds affordances on each object independently*

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/011_Table_4.jpg]]
*Table 4: Runtime and memory comparison. Average runtime (sec) and peak memory (GB) on Affogato [15], measured on a single RTX A6000 GPU*

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/014_Table.jpg]]
*Table: 3D Reconstruction loU Heatmap Figure A1. Sampling step ablation across different number of views. We evaluate volumetric IoU for varying sampling steps (1, 5, 10, 15, 20) with 1–6 input views. Reconstruction quality saturates at 5 steps across all view configurations, achieving 5× faster sampling (0.25s) compared to the default 25 steps in TRELLIS *

![[assets/figures/papers/paper_list_l2438_https_arxiv_org_abs_2601_09211/figures/010_Figure_7.jpg]]
*Figure 7: Failure cases. (top) Challenging views with severe occlusion lead to reconstruction errors that propagate to affordance predictions. (bottom) Incorrect initial affordance grounding misleads active view selection away from the target region*

## 方法谱系与知识库定位

### 1. 技术脉络与基线关系

Affostruction 处于**3D生成式重建**与**可供性定位**两个领域的交汇点，其核心设计吸收了多个方向的前沿成果，并通过关键改造形成了统一框架。

**重建基线的继承与改造。** 在3D生成式重建方面，Affostruction 直接构建于 **TRELLIS**（Xiang et al., CVPR 2025）的流变换器架构之上，但进行了三项关键改造：（1）将输入模态从单视图RGB扩展为多视图RGBD，引入深度图与相机内、外参数作为显式几何约束；（2）将TRELLIS的单视图DINOv2 patch特征替换为稀疏体素融合方案，利用深度将多视图特征投影到3D空间并聚合为恒定大小的表征；（3）将TRELLIS的固定单视图训练改为随机多视图训练，每个迭代随机采样1–8个视图，使模型学会利用任意数量的观测。这些改造使得Affostruction在Toky4K数据集上的重建IoU达到32.67，相比TRELLIS（19.49）提升67.6%，相比最强的RGBD重建方法 **MCC**（Wu et al., CVPR 2023，21.11）提升54.8%（Table 1）。

与RGB-to-3D生成模型（**Shap-E** Jun & Nichol, arXiv 2023; **InstantMesh** Xu et al., arXiv 2024; **LGM** Tang et al., ECCV 2024）相比，Affostruction通过深度条件与流匹配生成相结合，提供了更强的几何先验，其重建IoU显著优于这些仅依赖RGB的方法（Table 1）。这验证了“深度+生成”的互补性：深度提供可靠的可见表面约束，流匹配则从部分观察中推断被遮挡的完整结构。

**可供性定位基线的突破。** 在可供性定位方面，Affostruction 与判别式方法形成了根本性差异。**OpenAD**（Nguyen et al., IROS 2023）和 **PointRefer**（Li et al., CVPR 2024）均输出单一确定性可供性区域，无法捕捉交互区域的多模态性（例如，一把椅子既可以从座面“坐”，也可以从靠背“倚靠”）。当前最强的 **Espresso-3D**（Lee et al., arXiv 2025）在完整几何条件下达到13.6 aIoU，而Affostruction以19.1 aIoU超越其40.4%（Table 2），核心原因在于其基于流匹配的生成式框架能够显式建模可供性分布的多模态性。

**两阶段管线的统一。** 在部分观察场景下，传统方案通常采用“先重建后定位”的两阶段管线（如MCC+Espresso-3D），但两个阶段在独立空间中运行，信息传递受限，仅能达到4.74 aIoU。Affostruction将生成式重建与可供性定位统一在稀疏体素空间，使两者共享几何表征，在相同条件下达到9.26 aIoU，几乎是两阶段管线的两倍（Table 3）。这一结果揭示了“统一表征空间”对跨任务协同的关键作用。

### 2. 适用边界

**有效范围。** Affostruction 在以下条件下表现出显著优势：（1）输入为1–8个带有深度和相机参数的RGBD视图，视图数量越多，重建和可供性定位质量越高（Figure 4右）；（2）目标物体具有明确的几何结构和功能性区域，可供性查询以自然语言形式给出；（3）场景中物体已被分割或可借助外部分割模块（如SAM3D）进行实例级分离（Figure 6）。

**效率边界。** 在单张RTX A6000 GPU上，Affostruction的总推理时间为7.20秒（Table 4），其中重建采样在5步时即趋于饱和，仅需0.25秒（Figure A1）。这一效率使其在离线分析场景中具有实用价值，但尚未在真实机器人闭环操作中验证实时性。

**数据依赖。** 方法在Toky4K和Affogato两个仿真数据集上进行训练和评估，其泛化能力受限于训练数据的物体类别和场景多样性。在真实世界的传感器噪声、光照变化和动态遮挡条件下，性能可能下降，这一点尚未被实验覆盖。

### 3. 局限与开放问题

**错误传播机制。** Affostruction 存在一条关键的误差传播链：当初始视角存在严重遮挡时，生成式重建会产生几何错误，这些错误进一步导致可供性预测偏离真实功能区域（Figure 7 top）。更严重的是，错误的初始可供性定位会误导主动视图选择，使后续观察偏离目标区域，形成正反馈式的误差放大（Figure 7 bottom）。这一现象揭示了“生成-定位-选择”闭环中的脆弱性：系统缺乏对自身预测不确定性的感知和纠正机制。

**多物体场景的依赖。** 当前方法假设输入为单个物体的观测，在多物体复杂场景中需要依赖SAM3D等外部分割模块进行预处理（Figure 6）。稀疏体素融合和主动视图选择策略尚未扩展到无需预分割的多物体场景，这限制了其在非结构化环境中的直接应用。

**从预测到执行的鸿沟。** 虽然Affostruction能够生成高质量的可供性热力图，但如何将这些热力图直接转化为机器人的操作策略（如抓取位姿、接触力规划）仍是一个开放问题。当前工作止步于感知层面，尚未在真实机器人的交互任务中验证其有效性。

**开放研究方向。** 基于上述局限，以下几个方向值得关注：（1）将半监督学习中的误差检测策略融入流程，使系统能够自动识别并纠正不可靠的预测，从而切断错误传播链；（2）利用可供性文本查询作为重建的条件提示，在严重遮挡情况下引导模型优先恢复功能相关区域的几何结构；（3）进一步压缩模型或减少推理采样步数，以满足真实机器人应用中的实时性要求；（4）将稀疏体素融合与主动视图选择扩展到无需预分割的多物体场景，实现端到端的场景级可供性推理。

## 原文 PDF

![[paperPDFs/CVPR_2026/Affostruction_3D_Affordance_Grounding_with_Generative_Reconstruction.pdf]]