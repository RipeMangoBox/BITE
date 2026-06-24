---
title: "GeoMotion: Rethinking Motion Segmentation via Latent 4D Geometry"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GeoMotion_Rethinking_Motion_Segmentation_via_Latent_4D_Geometry.pdf
project_link: null
code_link: "https://github.com/zjutcvg/GeoMotion"
aliases:
- GeoMotion
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入预训练4D重建模型π³的潜在几何特征与相机姿态信息，通过自注意力机制隐式学习物体运动与相机运动的解耦，将运动分割转化为从几何表示中直接解码的前馈任务。
primary_logic: 绕开显式对应估计和迭代优化，直接利用潜在4D几何先验融合光流与相机姿态特征，以端到端前馈方式完成运动分割，在保持高精度的同时大幅提升推理效率。
claims:
- GeoMotion在多个运动分割基准上取得最先进性能：DAVIS2016-M上J&F达83.9，DAVIS2016上达84.7，DAVIS2017上J达81.1，SegTrackV2上J达77.3。
- 相比迭代优化方法，GeoMotion以0.31秒/帧的速度实现单次前馈推理，消除了显式运动估计和逐场景迭代细化。
- 特征聚合消融实验表明，融合4D几何、光流和相机姿态三种模态可将DAVIS2017的J&F提升至81.4，验证了多模态时空特征融合的有效性。
- 与3D/4D重建方法相比，GeoMotion在DAVIS数据集上的I_M指标领先Easi3R_monst3r达+13.8、+16.2和+11.7个百分点。
---

# GeoMotion: Rethinking Motion Segmentation via Latent 4D Geometry

> [!tip] 核心洞察
> 绕开显式对应估计和迭代优化，直接利用潜在4D几何先验融合光流与相机姿态特征，以端到端前馈方式完成运动分割，在保持高精度的同时大幅提升推理效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | GeoMotion：基于潜在4D几何的运动分割反思 |
| 英文题名 | GeoMotion: Rethinking Motion Segmentation via Latent 4D Geometry |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.21810) · [Code](https://github.com/zjutcvg/GeoMotion) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | GeoMotion |
| Dataset | DAVIS2016-Moving, DAVIS2016, DAVIS2017, SegTrackV2 |

> [!tip] 效果简介
> - DAVIS2016-Moving 上，J&F 83.9 vs 78.5 (OCLR-TTA) (+5.4)。
> - DAVIS2016 上，J&F 84.7 vs 78.5 (RCF-Stage1) (+6.2)。
> - DAVIS2017 上，J 81.1 vs 74.6 (ABR) (+6.5)。

## 概述

运动分割旨在从视频中分离出独立运动的物体区域，是视频理解、自动驾驶与机器人导航的基础任务。传统方法依赖显式运动估计（光流、点对应匹配或长程轨迹提取）与多阶段迭代优化，在动态场景中易受噪声干扰，导致误差累积与高昂的计算成本，难以实现高效泛化。

GeoMotion 提出了一种范式转换：**绕开显式对应估计与逐场景迭代优化，直接利用预训练4D重建模型π³中编码的潜在几何先验，将运动分割转化为从几何表示中前馈解码的任务**。核心思路是：4D几何特征已隐式编码了物体运动与相机运动的解耦信息，配合光流提供的局部像素运动线索与相机姿态提供的全局运动上下文，通过自注意力机制即可直接推理运动掩码，无需显式建模对应关系。

在多个运动分割基准上，GeoMotion 以单次前馈推理（0.31秒/帧）取得了最先进性能：DAVIS2016-M 上 J&F 达 83.9，DAVIS2016 上达 84.7，DAVIS2017 上 J 达 81.1，SegTrackV2 上 J 达 77.3。相比迭代优化方法（如 RoMo、SegAnyMotion），推理效率提升一个数量级以上；相比基于3D/4D重建的方法（如 Easi3R、MonST3R），在 DAVIS 各子集上的 I_M 指标领先 11.7–16.2 个百分点。消融实验进一步证实，融合4D几何、光流与相机姿态三种模态是多模态时空特征聚合的关键，而核心方法在不依赖 SAM2 后处理时仍优于经过精细化的重建方法，表明几何先验是性能的主要驱动力。

该方法在方法谱系中位于**前馈几何感知运动分割**这一新兴范式，区别于基于2D光流的前馈方法（如 OCLR-flow、ABR）和基于重建的迭代方法（如 Easi3R、VGGT4D）。其知识库定位融合了4D重建（π³的交替注意力主干与相机姿态解码器）、2D运动估计（RAFT光流）与视觉基础模型（DINOv2 图像编码器、SAM2 掩码细化），通过冻结预训练模块与轻量运动解码器的组合，在保持泛化性的同时实现高效推理。

## 背景与动机

### 运动分割的核心瓶颈：显式对应估计的困境

运动分割旨在从视频中分离出与背景运动不一致的动态物体区域，是视频理解、自动驾驶和机器人感知中的基础任务。传统方法的主流范式可概括为“显式运动估计→迭代优化”两阶段流水线：首先通过光流估计、点对应匹配或长程轨迹提取获得像素级运动线索，随后利用聚类、图割或条件随机场等迭代优化手段将运动信息转化为分割掩码。

这一范式面临两个结构性缺陷。**第一，误差累积问题**：显式运动估计（如光流、点对应）在动态场景中极易受噪声干扰——运动模糊、遮挡、纹理缺失区域会产生不可靠的对应关系，这些噪声在后续迭代优化中被逐阶段放大，导致分割质量退化。**第二，计算效率瓶颈**：迭代优化方法（如基于极线约束的逐场景姿态精细化、基于SAM2的提示式迭代细化）需要数秒至数十秒处理单帧，难以满足实时应用需求。

### 现有方法的局限与缺口

近年来，运动分割领域涌现出多条技术路线，但均未从根本上突破上述瓶颈：

- **前馈2D运动分割方法**（如**OCLR** (Xie et al., NeurIPS 2022)、**ABR** (Xie et al., ECCV 2024)）通过单次推理输出运动掩码，效率较高，但依赖显式光流或分层运动表示作为输入，在复杂动态场景下精度受限。
- **迭代优化方法**（如**RoMo**、**SegAnyMotion**）通过多阶段精细化获得更优的分割质量，但以高昂的计算成本为代价，且对初始化敏感。
- **3D/4D重建方法**（如**MonST3R** (Zhang et al., arXiv 2024)、**Easi3R**、**DAS3R** (Xu et al., arXiv 2024)）从动态场景中估计几何结构，可间接提取运动线索，但其核心目标是重建而非分割，运动掩码质量受限于几何估计精度，且同样依赖迭代优化。

上述方法的共同症结在于：**运动信息始终通过显式中间表示（光流场、点对应、重建残差）进行传递**，这一“瓶颈”既引入了噪声，又割裂了从原始视频到运动掩码的端到端学习路径。

### 本文动机：从潜在4D几何中直接解码运动

一个关键观察是：近年来4D场景几何重建模型（如**π³**）的突破，使得从视频中隐式编码丰富的时空几何先验成为可能。这些模型通过大规模预训练，在其内部特征表示中蕴含了关于场景结构、相机运动和物体运动的深层知识——但这些知识在传统运动分割流水线中从未被直接利用。

GeoMotion的核心动机由此产生：**能否绕开显式运动估计和迭代优化，直接从预训练4D重建模型的潜在几何特征中解码运动掩码？** 这一思路将运动分割重新定义为从几何表示中“读取”运动信息的前馈任务，而非从噪声对应关系中“推断”运动的优化问题。其潜在优势是双重的：在精度上，4D几何先验提供了比局部光流更全局、更鲁棒的运动线索；在效率上，单次前馈推理消除了迭代优化的计算开销。

这一动机驱动了GeoMotion框架的设计——通过融合预训练4D几何特征、光流特征与相机姿态信息，以端到端前馈方式完成运动分割，在保持高精度的同时将推理速度提升至0.31秒/帧，为运动分割的实用化部署开辟了新路径。

## 核心创新

GeoMotion的核心创新在于**将运动分割从显式运动估计与迭代优化的范式，重新定义为基于潜在4D几何先验的前馈解码任务**。这一转变由四个关键的changed slots支撑，共同构成了方法的技术骨架。

### 运动线索来源：从显式对应到隐式几何编码

传统运动分割方法依赖显式光流估计、点对应匹配或长程运动轨迹提取作为运动线索。这些中间表示在动态场景中易受噪声干扰，且误差会在多阶段流水线中累积。GeoMotion绕过了这一瓶颈，直接从预训练4D重建模型π³的潜在几何特征中隐式编码运动信息。如Figure 3所示，π³交替注意力层的浅层保留语义级物体特征，深层编码高层全局几何，两者的融合形成了鲁棒的潜在4D表征。这一设计消除了对显式对应估计的依赖，从根源上切断了噪声传播路径。

### 优化范式：从多阶段迭代到单次前馈

迭代优化方法（如RoMo、SegAnyMotion）需要逐场景进行姿态细化或掩码精细化，推理时间通常为数秒至数十秒每帧。GeoMotion以端到端前馈方式完成推理，在DAVIS2017上J指标达81.1的同时，推理速度仅为0.31秒/帧（Table 1）。这一效率提升的本质原因在于：运动解码被建模为从融合特征表示中直接应用自注意力的单次前向传播，而非逐场景的优化循环。

### 特征表示：从单一2D运动到多模态时空融合

传统方法通常仅使用单一2D运动特征（光流场或运动轨迹）。GeoMotion构建了融合三种模态的时空表征：

$$
\mathbf{F}_{\mathrm{fuse}} = \mathrm{MLP}([\mathbf{F}_{\mathrm{geo}}; \mathbf{F}_{\mathrm{flow}}; \mathbf{F}_{\mathrm{cam}}])
$$

其中$\mathbf{F}_{\mathrm{geo}}$为潜在4D几何特征，$\mathbf{F}_{\mathrm{flow}}$为光流特征，$\mathbf{F}_{\mathrm{cam}}$为相机姿态嵌入。Table 3的特征聚合消融实验验证了这一设计的必要性：逐步加入相机姿态特征、光流特征和浅层几何特征后，DAVIS2017的J&F最终提升至81.4。这证明了三者具有互补性——几何先验提供全局结构约束，光流捕捉局部像素运动，相机姿态则帮助解耦物体运动与相机自运动。

### 运动解码器初始化：从随机初始化到几何预训练迁移

GeoMotion的运动解码器并未随机初始化，而是复用了π³置信度解码器的预训练权重。π³的置信度解码器原本训练用于基于重建残差预测逐像素可靠性，这一任务与运动分割在“识别不可靠/异常区域”上存在语义关联。Figure 5的消融实验表明，该初始化策略相比随机初始化收敛更快、IoU更高，验证了大规模几何预训练的迁移价值。这一设计使运动解码器在训练初期即具备对几何异常区域的感知能力，加速了向运动掩码解码的适配。

## 整体框架

GeoMotion 提出了一种**端到端前馈运动分割框架**，其核心设计理念是绕开显式运动估计与迭代优化，直接从预训练4D重建模型中提取的潜在几何先验中解码运动掩码。整个流水线由三个主要阶段构成：多模态特征提取、时空特征聚合和前馈运动解码。

### 输入输出规范

给定一段包含 $N$ 帧的输入视频，框架首先通过 **DINOv2** 提取逐帧图像特征。这些特征随后进入**视觉几何主干（Visual Geometry Backbone, VGB）**——该模块采用 π³ 的标准交替注意力结构（36层），从图像特征中提取潜在4D几何特征 $\mathbf{F}_{\mathrm{geo}}$。具体而言，$\mathbf{F}_{\mathrm{geo}}$ 由经验筛选的第5、15、35和36层交替注意力输出拼接而成：浅层保留语义级物体特征，深层编码高层全局几何信息，二者的融合构成了鲁棒的潜在4D表征。

与此同时，两条并行分支分别提取运动线索：
- **光流编码器**：采用 **RAFT** 计算帧间光流，经 CNN 变换后获得局部光流特征 $\mathbf{F}_{\mathrm{flow}}$；
- **相机姿态解码器**：利用 π³ 预训练的相机姿态解码器，从 VGB 深层特征中解码相机姿态嵌入 $\mathbf{F}_{\mathrm{cam}}$。

### 特征聚合与运动解码

三种模态的特征通过**特征聚合模块**融合为统一的时空表征：

$$\mathbf{F}_{\mathrm{fuse}} = \mathrm{MLP}([\mathbf{F}_{\mathrm{geo}}; \mathbf{F}_{\mathrm{flow}}; \mathbf{F}_{\mathrm{cam}}])$$

该融合表征同时编码了场景的全局4D几何结构、局部像素级运动和相机自身运动信息，为后续的运动-相机运动解耦提供了完备的信息基础。

融合特征随后送入**运动解码器**——一个由5层自注意力层和轻量MLP头部组成的模块。自注意力机制在融合特征上直接感知动态物体，以单次前馈方式输出低分辨率运动掩码。值得注意的是，运动解码器的参数由 π³ 置信度解码器的预训练权重初始化，这一迁移策略显著加快了收敛速度并提升了分割精度。

### 测试时细化

在测试阶段，预测的低分辨率粗掩码被送入 **SAM2** 进行细化，恢复全分辨率精细边界。消融实验表明，SAM2 主要提升边界质量（DAVIS2017 上 JM 从 75.38 提升至 81.13），但即使不使用 SAM2，GeoMotion 的原始输出仍优于经过精细化的重建方法（如 Easi3R w/ SAM2），证明几何先验而非后处理是性能的主要驱动力。

### 关键设计特点

整个框架具有三个显著特点：
1. **冻结主干网络**：VGB、DINOv2 和 RAFT 在训练期间均被冻结，仅训练特征聚合 MLP 和运动解码器，大幅降低了训练成本；
2. **单次前馈推理**：无需逐场景迭代优化，推理速度达 0.31 秒/帧，与需要数秒至数十秒的迭代方法形成鲜明对比；
3. **隐式运动解耦**：通过融合相机姿态特征，自注意力机制隐式学习物体运动与相机运动的分离，无需显式的极线约束或运动补偿。

### 补充图表

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/001_Figure_1.jpg]]
*Figure 1: Overview of GeoMotion. Given an input video, our framework integrates 4D geometric priors from a pretrained reconstruction model (π3) and local pixel-level motion from optical flow to infer dynamic object masks. By leveraging 4D geometric priors, the proposed GeoMotion disentangles object motion from camera motion in a single feed-forward manner*

## 核心模块与公式推导

GeoMotion 的核心架构由**特征聚合模块**和**运动解码器**两大组件构成，其设计目标是将运动分割转化为从潜在4D几何表示中直接解码的前馈任务，从而绕开传统方法中显式运动估计与迭代优化的瓶颈。

### 特征聚合模块

该模块负责将多模态时空信息融合为统一的特征表示。具体而言，系统并行提取三类互补特征：

- **潜在4D几何特征** $\mathbf{F}_{\mathrm{geo}}$：由视觉几何主干（Visual Geometry Backbone, VGB）从DINOv2提取的逐帧图像特征中生成。VGB采用π³中的标准交替注意力模块（36层），经验性地选取第5、15、35、36层的输出进行拼接，以同时保留浅层的语义物体级特征和深层的全局几何结构信息。
- **光流特征** $\mathbf{F}_{\mathrm{flow}}$：通过RAFT提取帧间光流，再经CNN编码为局部运动特征。
- **相机姿态特征** $\mathbf{F}_{\mathrm{cam}}$：由π³的相机姿态解码器从VGB深层特征中解码得到，显式建模相机自运动信息。

三者通过拼接与MLP投影融合为统一的时空特征：

$$\mathbf{F}_{\mathrm{fuse}} = \mathrm{MLP}([\mathbf{F}_{\mathrm{geo}}; \mathbf{F}_{\mathrm{flow}}; \mathbf{F}_{\mathrm{cam}}])$$

其中 $[\cdot;\cdot;\cdot]$ 表示通道维度拼接操作。这一融合策略的动机在于：光流提供像素级局部运动线索，相机姿态提供全局观测视角变化，而潜在4D几何特征则编码了场景的三维结构与时空一致性先验——三者的互补使模型能够隐式解耦物体运动与相机运动，无需显式进行对应点匹配或极线约束计算。

### 运动解码器

运动解码器由**5层自注意力层**和一个轻量MLP分类头组成，直接从前述融合特征 $\mathbf{F}_{\mathrm{fuse}}$ 中前馈解码运动掩码。其关键设计在于：

- **多帧自注意力机制**：自注意力在时空维度上操作，使模型能够跨帧聚合运动线索，感知物体的持续运动模式而非单帧外观变化。
- **预训练权重初始化**：解码器参数使用π³置信度解码器的预训练权重进行初始化。π³的置信度解码器原用于基于重建残差预测逐像素可靠性，该任务与运动区域识别具有内在关联——不可靠的重建区域往往对应动态物体。消融实验（Figure 5）证实，相比随机初始化，该策略带来更快的收敛速度和更高的IoU，验证了大规模几何预训练的迁移价值。

### 训练损失函数

模型在 $N$ 帧序列上进行端到端训练，损失函数为Focal Loss与Dice Loss的加权组合：

$$\mathcal{L} = \sum_{t=1}^{N} \left( \lambda_{1} \mathcal{L}_{\mathrm{focal}}(M^{t}, M_{\mathrm{gt}}^{t}) + \lambda_{2} \mathcal{L}_{\mathrm{dice}}(M^{t}, M_{\mathrm{gt}}^{t}) \right)$$

其中 $M^{t}$ 和 $M_{\mathrm{gt}}^{t}$ 分别为第 $t$ 帧的预测掩码与真值掩码，$\lambda_{1}$ 和 $\lambda_{2}$ 均设为0.5。Focal Loss聚焦困难样本（如运动边界和细小物体），Dice Loss缓解前景-背景类别不平衡问题。两者联合使用，配合运动解码器中的多帧注意力机制和π³提供的4D几何先验，使模型能够在复杂动态场景下实现鲁棒的运动分割。

### 测试时细化

测试阶段，预测的低分辨率粗掩码被送入视觉分割模型SAM2以恢复全分辨率精细掩码。消融实验（Table 5）表明，SAM2主要提升边界质量（JM从75.38提升至81.13），而核心方法在无SAM2时已优于经过精细化的重建方法（如Easi3R w/SAM2），证明几何先验是性能的主要驱动力而非后处理。

### 补充图表

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/002_Figure_2.jpg]]
*Figure 2: Architecture of the proposed GeoMotion framework. The model comprises a feature aggregation module and a motion decoder. The former fuses latent 4D features, optical flow features, and camera pose embeddings, while the latter employs multi-head self-attention to decode motion masks. The design enables end-to-end feed-forward motion segmentation without iterative refinement*

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of*

## 实验与分析

### 主实验结果

GeoMotion在多个运动分割基准上取得了最优性能，同时保持了显著的计算效率优势。Table 1汇总了与各类方法的定量对比。

在DAVIS2016-Moving基准上，GeoMotion取得**83.9 J&F**，相比前馈基线**OCLR-TTA**（Xie et al., NeurIPS 2022）提升+5.4个百分点，相比基于光流的**RCF-Stage1**提升+6.6个百分点。在DAVIS2016全量基准上，方法达到**84.7 J&F**，超越RCF-Stage1达+6.2个百分点。在更具挑战性的DAVIS2017多物体分割任务上，GeoMotion取得**81.1 J**，相比**ABR**（Xie et al., ECCV 2024）的74.6 J提升+6.5个百分点。在SegTrackV2基准上，方法取得**77.3 J**，进一步验证了跨数据集的泛化能力。

效率方面，GeoMotion以**0.31秒/帧**的速度完成单次前馈推理，而迭代优化方法如RoMo、SegAnyMotion等通常需要数秒至数十秒。这一效率优势源于方法绕过了显式运动估计和逐场景迭代细化，直接从潜在4D几何表示中解码运动掩码。

与3D/4D重建方法的对比（Table 2）进一步凸显了几何先验的威力。在DAVIS三个子集上，GeoMotion的I_M指标分别领先**Easi3R_monst3r**（Zhang et al., arXiv 2024）+13.8、+16.2和+11.7个百分点，领先**VGGT4D**和**DAS3R**（Xu et al., arXiv 2024）的幅度更大。值得注意的是，即使不使用SAM2后处理，GeoMotion的原始输出（JM 75.38）仍优于Easi3R w/SAM2等经过精细化的重建方法，证明核心几何感知范式的有效性不依赖于后处理。

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/006_Table_2.jpg]]
*Table 2: Comparison with 3D/4D reconstruction-based methods. The best and second-best results are labeled in bold and underlined, respectively*

### 消融实验

**特征聚合消融（Table 3）。** 逐步加入不同模态特征可稳定提升DAVIS2017上的分割精度。仅使用深层几何特征时J&F为78.3；加入相机姿态特征后提升至79.6；进一步融合光流特征后达到80.8；最终融合浅层几何特征（第5、15层）后，完整模型取得**81.4 J&F**。该消融验证了多模态时空特征融合的必要性：潜在4D几何提供全局场景结构，光流捕获局部像素运动，相机姿态嵌入帮助解耦物体运动与相机运动。

**训练数据规模消融（Table 4）。** 在五个公开数据集（HOI4D、Dynamic Replica、YouTubeVOS2018-motion、OmniWorld-motion、GOT-Motion）上联合训练可获得最佳性能，DAVIS2016-M上J达83.5、F达84.3，DAVIS2017上J达81.1、F达81.8。随着训练数据规模和多样性的增加，性能单调提升，证明模型具有良好的可扩展性。

**解码器初始化消融（Figure 5）。** 使用π³置信度解码器的预训练权重初始化运动解码器，相比随机初始化收敛速度更快、IoU更高。π³的置信度解码器原本训练用于基于重建残差预测逐像素可靠性，该任务与运动分割共享对“异常区域”的感知能力，因此预训练权重提供了有效的迁移先验。

**SAM2消融（Table 5）。** SAM2后处理主要提升边界质量：JM从75.38提升至81.13（+5.75），边界F从73.66提升至81.76（+8.10），而区域J的提升相对温和（75.38→80.51）。定性对比（Figure 6、Figure 7）显示，SAM2细化后的掩码边界更精细，但核心几何感知方法在无SAM2时已能产生干净、紧凑的运动掩码，背景误检显著少于Easi3R和VGGT4D。

### 失败模式与局限性

尽管GeoMotion在主流基准上表现优异，仍存在若干值得关注的局限：

1. **SAM2依赖。** 测试阶段需借助SAM2将低分辨率粗掩码细化为全分辨率精细掩码，增加了推理流水线的步骤和对外部模型的依赖。完全端到端的高分辨率输出尚未实现。

2. **冻结主干的限制。** 视觉几何主干（π³交替注意力层和相机姿态解码器）、DINOv2和RAFT在训练期间均被冻结，无法针对运动分割任务进行联合端到端优化，可能限制了任务自适应表征学习的上限。

3. **极端场景泛化。** 训练数据总量和场景多样性仍受限（如OmniWorld-motion仅9个序列），对剧烈光照变化、严重运动模糊、高度动态遮挡等极端情形的泛化性有待进一步验证。

4. **实例级分割缺失。** 当前方法输出二值运动掩码，不支持多运动物体的实例级分割，且无法区分不同运动物体的运动模式（如刚体运动、非刚体形变）。

### 补充图表

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with motion segmentation methods on popular benchmarks. The proposed model obtains state-of-the-art performance. It achieves an excellent trade-off between segmentation quality and computational efficiency*

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison on multiple benchmarks. Visual comparison with state-of-the-art methods including OCLR-Flow [44], SegAnyMotion [11], and RoMo [7]. The proposed method produces geometrically complete and visually coherent motion masks, preserving fine object details and boundaries under complex scenes*

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/007_Table_4.jpg]]
*Table 4: Ablation study on dataset scale. Training on progressively larger and more diverse datasets consistently improves segmentation performance, demonstrating the strong scalability and generalization ability of the proposed method*

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/008_Table_3.jpg]]
*Table 3: Ablation study on feature aggregation. Adding the camera pose, optical flow, and shallow-layer features progressively enhances performance on DAVIS2017. The full model, which combines all three modalities, achieves the best overall accuracy, validating the effectiveness of spatio-temporal feature fusion*

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/009_Figure_5.jpg]]
*Figure 5: Initialization comparison for the motion decoder. Initializing with*

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/010_Table_5.jpg]]
*Table 5: Ablation for SAM2 on DAVIS-2017*

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative ablation results for SAM2*

![[assets/figures/papers/paper_list_l2507_https_arxiv_org_abs_2602_21810/figures/012_Figure_8.jpg]]
*Figure 8: More visual examples of dynamic masks predicted by GeoMotion on the DAVIS benchmark. Odd rows show the RGB input frames, while even rows present the corresponding predicted dynamic masks*

## 方法谱系与知识库定位

### 1. 技术范式定位

GeoMotion 代表了运动分割领域从**显式运动估计+迭代优化**向**隐式几何感知+前馈推理**的范式迁移。传统方法依赖光流场、点对应或长程轨迹作为中间表示，再通过多阶段优化（逐场景姿态估计、掩码精细化）完成分割。GeoMotion 的核心突破在于绕开这些噪声敏感且计算昂贵的中间步骤，直接从预训练4D重建模型 π³ 的潜在几何特征中解码运动信息。

这一设计将运动分割重新定义为一个**从几何表示中直接解码的前馈任务**，而非传统的运动估计后处理任务。其因果杠杆在于：π³ 的交替注意力层在4D重建预训练中已经隐式编码了场景几何、相机运动和物体运动的耦合关系，GeoMotion 通过自注意力机制学习从中解耦出物体运动掩码，从而消除了显式对应估计带来的误差累积。

### 2. 与已有工作的关系

#### 2.1 相对于2D运动分割方法

GeoMotion 与两类2D运动分割方法形成对比：

- **前馈基线方法**：**OCLR** (Xie et al., NeurIPS 2022) 基于分层光流表示，**ABR** (Xie et al., ECCV 2024) 在此基础上引入外观细化。这些方法仍依赖显式光流作为唯一运动线索，缺乏对相机运动和场景几何的显式建模。GeoMotion 在 DAVIS2016-M 上以 83.9 J&F 超越 OCLR-TTA 的 78.5（+5.4 点），在 DAVIS2017 上以 81.1 J 超越 ABR 的 74.6（+6.5 点），证明了融合4D几何先验的显著增益。

- **迭代优化方法**：**RoMo** 结合光流与极线约束进行逐场景迭代，**SegAnyMotion** 基于长程轨迹和 SAM2 迭代提示。这些方法虽能取得有竞争力的精度，但推理时间通常在数秒至数十秒/帧。GeoMotion 以 0.31 秒/帧的单次前馈推理实现了精度与效率的双重优势，在 DAVIS2016-M 上领先 RCF-Stage1 达 +6.6 点。

#### 2.2 相对于3D/4D重建方法

GeoMotion 与从重建角度处理运动分割的方法存在本质差异：

- **Easi3R** 和 **VGGT4D** 从静态重建模型中提取运动线索，**MonST3R** (Zhang et al., arXiv 2024) 和 **DAS3R** (Xu et al., arXiv 2024) 面向动态场景进行几何估计。这些方法通常需要复杂的后处理（如 SAM2 精细化）才能获得可用的运动掩码。GeoMotion 在 DAVIS 数据集上的 I_M 指标领先 Easi3R_monst3r 达 +13.8、+16.2 和 +11.7 个百分点，且即使不使用 SAM2 后处理，其原始输出（JM 75.38）仍优于 Easi3R w/SAM2 等经过精细化的方法。

GeoMotion 的关键区分点在于：重建方法的目标是恢复场景的3D/4D几何，运动掩码是其副产品；而 GeoMotion 直接将运动分割作为学习目标，利用几何先验服务于分割任务，实现了更紧凑、更少背景误检的输出。

#### 2.3 知识继承与迁移

GeoMotion 的知识继承链清晰：

- **视觉几何主干**：继承自 **VGGT** 和 **π³** 的交替注意力架构，利用其在4D重建预训练中习得的场景几何理解能力。关键设计选择包括：冻结主干参数以保持几何知识的稳定性，拼接第5、15、35、36层的多层特征以融合语义级和全局几何级表示。
- **运动解码器初始化**：复用 π³ 置信度解码器的预训练权重。π³ 的置信度解码器原本预测逐像素的重建可靠性，这种对“几何不确定性”的感知能力被迁移到“运动区域识别”任务中。消融实验（Figure 5）证实，该初始化相比随机初始化带来更快的收敛速度和更高的 IoU。
- **光流编码**：采用 **RAFT** 提取光流，通过 CNN 编码为局部运动特征 F_flow，作为对潜在几何特征中全局运动信息的补充。

### 3. 适用边界与局限

#### 3.1 架构层面的固有限制

- **冻结主干的表征上限**：DINOv2 编码器、π³ 交替注意力层、相机姿态解码器和 RAFT 在训练期间均被冻结，无法针对运动分割任务进行联合端到端优化。这可能限制了任务自适应表征学习的潜力，特别是在几何预训练数据分布与运动分割场景存在差异时。
- **SAM2 后处理的依赖**：测试阶段需借助 SAM2 将低分辨率粗掩码细化为全分辨率掩码，增加了推理流水线的步骤和对外部模型的依赖。尽管消融实验表明核心方法在无 SAM2 时已具竞争力，但完全端到端的高分辨率输出尚未实现。
- **二值掩码输出的局限性**：当前方法仅输出二值运动掩码，不支持多运动物体的实例级分割，也无法区分不同运动模式（刚体运动、非刚体形变、流体运动等）。

#### 3.2 数据与泛化边界

- **训练数据规模受限**：尽管联合使用了五个公开数据集（HOI4D、Dynamic Replica、YouTubeVOS2018-motion、OmniWorld-motion、GOT-Motion），但部分数据集规模极小（如 OmniWorld-motion 仅9个序列），场景多样性有限。对极端动态场景（剧烈光照变化、严重运动模糊、高度动态遮挡）的泛化性有待验证。
- **零样本评估的覆盖范围**：现有评估集中在 DAVIS、SegTrackV2 和 FBMS-59 等标准基准，这些数据集以中等运动复杂度为主，可能不足以充分测试方法在快速相机运动、密集遮挡和非刚性形变场景下的鲁棒性。

### 4. 开放问题与未来方向

#### 4.1 架构演进

- **去后处理化**：能否完全去除 SAM2 后处理步骤，通过可学习的上采样模块或高分辨率解码器直接输出全分辨率运动掩码，实现真正意义的全端到端推理？这需要在特征分辨率和计算效率之间取得平衡。
- **参数高效微调**：冻结的 π³ 几何主干是否可以通过 LoRA 等参数高效微调方法进行任务适配，在保持预训练几何知识稳定性的同时提升运动分割性能？这涉及“稳定性-可塑性”困境的权衡。
- **实例级扩展**：如何将二值掩码输出扩展为实例级运动分割？可能的路径包括引入运动嵌入聚类或基于查询的实例解码器。

#### 4.2 能力边界拓展

- **极端场景鲁棒性**：当前方法在多目标密集遮挡、快速相机运动和非刚性物体形变场景下的鲁棒性如何？需要构建更具挑战性的测试基准来系统评估这些边界情形。
- **运动模式识别**：潜在4D几何特征中是否编码了足够的运动模式信息（刚体 vs. 非刚体 vs. 流体），以支持更细粒度的运动分类？这可能需要引入物理先验或运动基元分解。
- **跨任务迁移**：GeoMotion 验证了4D几何先验对运动分割的有效性，这一范式能否迁移到其他下游任务？潜在方向包括：动态3D重建（用运动掩码引导动态区域建模）、运动预测（从几何特征中预测未来帧的运动场）、视频插帧（利用几何一致性约束中间帧生成）。这指向一个更宏大的目标——构建统一的4D场景理解基础模型。

## 原文 PDF

![[paperPDFs/CVPR_2026/GeoMotion_Rethinking_Motion_Segmentation_via_Latent_4D_Geometry.pdf]]
