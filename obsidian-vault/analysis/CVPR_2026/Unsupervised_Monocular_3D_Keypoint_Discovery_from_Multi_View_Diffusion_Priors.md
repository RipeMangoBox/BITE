---
title: Unsupervised Monocular 3D Keypoint Discovery from Multi-View Diffusion Priors
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Unsupervised_Monocular_3D_Keypoint_Discovery_from_Multi_View_Diffusion_Priors.pdf
project_link: null
code_link: null
aliases:
- UM3KDFMVDP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 利用预训练多视图扩散模型 (SV3D-p) 中的几何先验：扩散模型生成的多视图图像提供自监督信号，扩散特征的中间表示被提升为显式3D体积特征，从而绕过对标注和多视图校准的依赖。
primary_logic: 将扩散模型的隐式3D几何先验转化为显式3D体积表示：通过聚合多级扩散特征、单向投影构建3D特征网格，并基于体积热力图和积分回归直接预测3D关键点，实现从单张图片的无监督3D关键点发现。
claims:
- 扩散模型生成的多视图图像为无监督训练提供了几何约束，无需标注或多视图校准
- 引入3D特征提取器，将扩散特征中的隐式3D先验转换为显式3D特征体积
- 多视图扩散特征始终优于传统的2D基础网络 (ResNet50, CLIP, DINOv2)
- 在3D空间中明确建模关键点 (体积网络) 比2D检测后三角化更准确且几何一致
---

# Unsupervised Monocular 3D Keypoint Discovery from Multi-View Diffusion Priors

> [!tip] 核心洞察
> 将扩散模型的隐式3D几何先验转化为显式3D体积表示：通过聚合多级扩散特征、单向投影构建3D特征网格，并基于体积热力图和积分回归直接预测3D关键点，实现从单张图片的无监督3D关键点发现。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于多视图扩散先验的无监督单目3D关键点发现 |
| 英文题名 | Unsupervised Monocular 3D Keypoint Discovery from Multi-View Diffusion Priors |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2507.12336) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | KeyDiff3D |
| Dataset | Human3.6M, CUB-align, CUB-all |

> [!tip] 效果简介
> - Human3.6M (单帧，无监督) 上，MPJPE (↓) 121.34 vs 125.73 (Honari et al., 单视图, 32关键点, 2 hid MLP) (-4.39)。
> - Human3.6M 上，N-MPJPE (↓) 118.29 vs 121.04 (Honari et al.) (-2.75)；P-MPJPE (↓) 85.26 vs 89.05 (Honari et al.) (-3.79)。
> - CUB-align (KP=10) 上，L2距离 (归一化↓) 5.16 vs 6.38 (StableKeypoints, 复现结果) (-1.22)。

## 概述

单目3D关键点估计是计算机视觉中的核心难题，其根本瓶颈在于：从单张2D图像恢复3D结构是一个极度欠约束的逆问题，深度歧义和自遮挡使得精确推理异常困难。传统方法依赖手工标注的3D关键点真值或多视图校准数据，获取成本高昂，严重制约了方法的可扩展性。

本文提出 **KeyDiff3D**，一种全新的无监督单目3D关键点发现方法。其核心思路是**将预训练多视图扩散模型中蕴含的隐式3D几何先验转化为显式的3D体积表示**，从而在不依赖任何3D标注或相机校准的条件下，从单张图像直接预测3D关键点。具体而言，KeyDiff3D利用预训练的多视图扩散模型（SV3D-p）生成多视角图像作为自监督信号，同时从扩散U-Net的中间层提取多层级特征，经可学习权重融合后，通过反投影操作提升为3D特征体积，再经由体积卷积网络和积分回归直接估计3D关键点坐标。

方法的核心因果机制体现在三个层面：第一，扩散模型生成的多视图图像为无监督训练提供了几何约束，替代了传统方法对校准多视图数据的依赖；第二，多视图扩散特征在表示能力上显著优于ResNet50、CLIP、DINOv2等传统2D基础网络；第三，在3D空间中显式建模关键点（体积网络+积分回归）比“2D检测后三角化”的策略具有更好的几何一致性和精度。

**主要结果**：在Human3.6M数据集上，KeyDiff3D以MPJPE 121.34 mm的成绩优于现有无监督方法（Honari et al. 的125.73 mm），在CUB-200-2011鸟类数据集上同样取得领先。方法还展现出良好的跨域泛化能力——在Human3.6M上训练的模型可直接应用于DAVIS自然场景和GSO物体数据集，在Stanford Dogs上训练的模型可泛化至AP-10K灵长类数据集。此外，预测的3D关键点结合可学习的邻接矩阵，能够驱动3D模型实现骨骼绑定和动画操控。

**方法定位**：KeyDiff3D属于无监督3D关键点发现方法，与BKinD-3D（需校准多视图）、KeypointNet（多视图训练+单帧推理）等工作的根本区别在于，它完全摆脱了对多视图校准数据的依赖，转而利用扩散模型的生成能力提供几何监督。在2D无监督关键点检测方法（如StableKeypoints、AutoLink）的基础上，KeyDiff3D首次将扩散先验成功扩展至3D空间。

**局限性**：方法仍存在左右歧义问题（无法区分对称部位），且当扩散模型生成质量下降（如遮挡区域、多视图不一致）时，预测精度会受到影响。此外，扩散模型前传带来的计算开销（约7787 GFLOPs）限制了实时应用场景。

## 背景与动机

### 单目3D关键点估计的核心困境

从单张二维图像恢复三维关键点位置是计算机视觉中的一个基础性难题。其根本瓶颈在于：单目观测本身是极度欠约束的——同一个二维投影可能对应无穷多个三维解，而遮挡和深度歧义进一步加剧了这种不确定性。传统的有监督方法依赖大量手工标注的三维关键点真值，但精确的三维标注成本极高，尤其对于非刚性、多关节的物体（如人体、动物），需要昂贵的动作捕捉系统或繁琐的人工校准。无监督方法试图摆脱标注依赖，但多数现有工作仍需**校准的多视图图像**作为训练监督（如 **BKinD-3D** 在训练和推理阶段均需多视图输入；**Honari et al.** 和 **KeypointNet** 虽支持单帧推理，但仍需多视图训练数据）。这些方法面临一个共同的扩展性瓶颈：多视图校准数据的采集与处理成本限制了它们在大规模、非受限场景下的应用。

### 现有无监督方法的缺口

无监督3D关键点发现的现有路线大致可分为两类，各自存在明显局限：

1. **基于多视图几何约束的方法**：利用校准相机从不同视角拍摄的同一场景图像，通过几何一致性（如对极约束、三角化）来发现关键点。这类方法对采集条件要求苛刻，难以泛化到自然图像或野外场景。
2. **基于2D先验的方法**：在二维图像上检测关键点（如 **StableKeypoints** 利用扩散特征、**AutoLink** 基于自连接图、**GANSeg** 通过GAN分割），再通过后处理（如三角化）提升到三维。然而，如表3(b)所示，2D检测后三角化的策略（MPJPE 172.74）远逊于直接在三维空间中建模（MPJPE 121.34），暴露了“先2D后3D”路线的几何不一致性。

此外，现有方法普遍使用通用2D基础网络（如ResNet50、CLIP、DINOv2）作为特征提取器。但消融实验（表3a）表明，这些单视图特征缺乏足够的3D几何线索——ResNet50的MPJPE高达172.25，CLIP为192.46，DINOv2为155.12——远不能满足精确3D定位的需求。

### 本文动机：从扩散先验中挖掘几何约束

近年来，预训练多视图扩散模型（如SV3D）展示了从单张图像生成一致多视图的惊人能力。这意味着扩散模型的内部表示已经编码了关于三维几何的隐式先验。本文的核心动机正是**将这种隐式几何先验转化为显式的三维理解能力**：

- **监督信号的解放**：扩散模型可从单张图像生成多个新视角图像，这些生成视图可作为自监督信号，替代传统方法所需的校准多视图数据或手工标注。
- **特征表示的升级**：扩散U-Net的中间层特征蕴含丰富的多视图几何线索，通过可学习的聚合和三维提升，可以构建出比传统2D主干网络更具几何判别力的特征表示。
- **端到端3D建模**：直接在三维体积空间中预测关键点，避免“2D检测→三角化”带来的信息损失和几何不一致。

简言之，本文探索一个根本性问题：**能否仅凭预训练扩散模型中的多视图生成能力，从单张图片中无监督地发现几何一致的三维关键点？** 这一思路若成功，将大幅降低3D关键点估计的数据门槛，使其可泛化至缺乏标注和多视图校准的任意对象类别。

## 核心创新

KeyDiff3D 的核心贡献在于**将预训练多视图扩散模型中的隐式3D几何先验转化为显式3D体积表示**，从而在无需任何3D标注或校准多视图数据的条件下，从单张图片直接预测3D关键点。这一思路在四个关键维度上形成了对现有方法的系统性改进：

### 1. 监督源：从校准多视图到扩散生成视图

传统无监督3D关键点方法（如 **BKinD-3D**、**Honari et al.**）依赖校准的多视图图像提供几何约束，数据采集成本高且场景受限。KeyDiff3D 将监督信号完全替换为预训练多视图扩散模型 SV3D-p 生成的合成视图：给定单张输入图像，扩散模型生成包括输入视图在内的 $K=4$ 张多视图图像，这些生成视图为模型训练提供自监督几何线索，**彻底消除了对多视图校准和手工3D标注的依赖**。

### 2. 特征提取：从通用2D主干到多视图扩散特征

现有方法通常采用 ResNet50、CLIP、DINOv2 等通用2D基础网络作为特征提取器。KeyDiff3D 的消融实验（Table 3a）表明，这些单视图主干在3D关键点任务上表现显著不足——ResNet50 的 MPJPE 为 172.25，CLIP 为 192.46，DINOv2 为 155.12，而**多视图扩散U-Net的中间层特征经可学习权重融合后，MPJPE 降至 121.34**。这一差距的根源在于扩散模型的去噪U-Net在生成多视图一致图像的过程中内化了3D几何先验，其多层特征蕴含了比2D预训练特征更丰富的空间结构信息。

### 3. 3D推理策略：从2D检测后三角化到体积热力图积分回归

传统管线通常先检测2D关键点，再通过多视图三角化恢复3D坐标。KeyDiff3D 采用了一条根本不同的路径：将多视图2D扩散特征通过反投影（unprojection）提升为3D体积特征，经3D卷积网络处理后，在体积热力图上使用积分回归直接预测3D关键点坐标。消融实验（Table 3b）证实了这一设计的关键性——**3D体积特征→3D关键点路径的 MPJPE 为 121.34，而2D关键点→三角化路径高达 172.74**，说明在3D空间中显式建模关键点比后处理三角化具有更强的几何一致性和抗噪能力。

### 4. 拓扑表示：从独立关键点到可学习结构图

KeyDiff3D 引入可学习的邻接矩阵 $\mathcal{A} \in \mathbb{R}^{N \times N}$，将关键点组织为软边图结构。在自监督训练中，投影后的关键点通过可微分高斯线构建边图，邻接矩阵作为乘法门控提供结构先验。这一设计使模型不仅能定位关键点，还能捕捉关键点之间的拓扑关系，为下游的骨骼绑定和可驱动3D模型生成（Figure 6）提供了直接支持。

### 创新链条总结

上述四个 changed slots 构成了一个紧密耦合的创新链条：扩散生成视图（新监督源）→ 多视图扩散特征（新特征提取器）→ 体积反投影与积分回归（新3D推理策略）→ 可学习结构图（新拓扑表示）。消融实验表明，**仅使用输入视图（$K=1$）时 MPJPE 退化为 166.29**（Table 3c），验证了多视图扩散先验是整个方法有效性的基础；而扩散时间步 $\tau=500$ 的最优选择（Table 5b）进一步说明，适中的去噪阶段能最好地平衡几何先验的丰富性与特征的判别力。

## 整体框架

KeyDiff3D 的整体流水线如图2所示，由三个核心模块串联构成：**扩散特征聚合**、**3D关键点提取**和**自监督训练**。给定单张输入图像 $I$，系统输出一组 $N$ 个3D关键点 $\mathbf{S} = \{\mathbf{s}_n\}_{n=1}^N$ 以及一个可学习的邻接矩阵 $\mathcal{A} \in \mathbb{R}^{N \times N}$，后者编码了关键点之间的拓扑关系。

**模块间的数据流与因果链路**如下：

1. **多视图扩散先验的生成**：输入图像首先经过前景分割（Grounded SAM）提取目标掩码，随后送入预训练的多视图扩散模型SV3D-p。该模型在去噪过程中同时生成 $K=4$ 张新视角图像（含输入视图和3张合成视图），并从U-Net的多个层级提取中间扩散特征。这一步是整个框架的**因果枢纽**——扩散模型内嵌的隐式3D几何先验被显式化为可操作的多视图2D特征，从而绕过了对人工标注和多视图校准的依赖。

2. **扩散特征聚合**：来自U-Net各层的多级特征 $\mathbf{f}_l$ 通过可学习瓶颈层 $B_l$ 投影后，以加权求和方式融合为聚合特征 $\mathbf{F}_{\mathrm{agg}} = \sum_{l=1}^{L} w_l \cdot B_l(\mathbf{f}_l)$。随后经变换网络 $\phi_{\mathrm{kp}}$ 得到各视图的关键点特征 $\mathbf{F}_{\mathrm{kp}}$。这一轻量级聚合网络将扩散模型的隐式几何先验压缩为统一的多视图表示，是连接扩散模型与3D重建的关键桥梁。

3. **2D→3D特征提升**：聚合后的多视图2D特征通过反投影（unprojection）被提升为显式3D体积表示。具体而言，对体素网格 $\Omega$ 中的每个体素中心 $\mathbf{x}$，通过投影坐标在各视图特征图上双线性采样，再以跨视图软注意力加权融合，得到3D体积特征 $\mathbf{V}(\mathbf{x})$。这一步将扩散模型的**隐式3D先验转化为显式3D特征体积**，是方法的核心创新。

4. **3D关键点估计**：3D卷积网络在体积特征上预测每个关键点的体积热力图 $\mathbf{H}_n$，再通过积分回归 $\mathbf{s}_n = \sum_{\mathbf{x} \in \Omega} \mathbf{x} \cdot \mathrm{softmax}(\mathbf{H}_n(\mathbf{x}))$ 得到可微分的3D关键点坐标。消融实验证实，这种在3D空间中显式建模关键点的策略，显著优于先检测2D关键点再三角化的传统方案（MPJPE 121.34 vs 172.74，Table 3b）。

5. **自监督训练闭环**：预测的3D关键点被投影到扩散生成的各新视角图像上，构建软边图作为结构线索，通过VGG感知损失和边缘掩码损失驱动重建网络。训练无需任何3D真值标注或相机校准参数，完全依赖扩散模型提供的多视图几何一致性信号。

**关键设计决策**：默认配置使用 $N=18$ 个关键点、体素分辨率 $M=72$、扩散时间步 $\tau=500$。消融实验表明，引入随机仿射变换对输入图像的扰动可防止重建网络走捷径（MPJPE从134.54降至121.34），而跨视图特征聚合采用softmax加权优于基于可见性的聚合（121.34 vs 127.12），后者易受深度估计误差影响。

### 补充图表

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/002_Figure_2.jpg]]
*Figure 2: The overall pipeline of KeyDiff3D. From a single image, (1) a pretrained multi-view diffusion model provides novel views and multi-view features, (2) which are aggregated and lifted into a 3D feature volume for keypoint prediction, and (3) the predicted 3D keypoints are projected to the generated views to provide structural cues for self-supervised reconstruction*

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/001_Figure_1.jpg]]
*Figure 1: KeyDiff3D enables 3D keypoint prediction and object manipulation from a single image using multi-view diffusion priors. It generalizes effectively to in-the-wild and out-of-domain scenarios across diverse categories, including both human and animal domains*

## 核心模块与公式推导

KeyDiff3D 的核心设计围绕一个因果链条展开：**将扩散模型的隐式3D几何先验转化为显式3D体积表示，并在该体积空间中直接预测3D关键点**。整个流水线由三个紧密耦合的模块构成。

### 扩散特征聚合 (Diffusion Feature Aggregation)

预训练的多视图扩散模型 SV3D-p 在生成新视图的过程中，其 U-Net 的中间层特征蕴含了丰富的多视图几何线索。然而，这些特征分布在不同的去噪层级和不同的视图中，需要有效的融合机制。

给定输入图像，扩散模型在去噪时间步 $\tau = 500$（共 $T = 1000$ 步）处，从 U-Net 的所有 $L$ 层提取中间特征 $\mathbf{f}_l$。每一层特征首先通过一个轻量瓶颈层 $B_l(\cdot)$ 进行投影，然后以可学习的混合权重 $w_l$ 进行加权求和，得到聚合特征：

$$
\mathbf{F}_{\mathrm{agg}} = \sum_{l=1}^{L} w_l \cdot B_l(\mathbf{f}_l)
$$

这一设计使得网络能够自适应地选择对3D几何推理最关键的扩散层级。消融实验（Table 3a）表明，这种多视图扩散特征在 MPJPE 指标上（121.34）大幅优于传统的单视图基础主干网络，如 ResNet50（172.25）、CLIP（192.46）和 DINOv2（155.12），验证了扩散模型中蕴含的几何先验远强于通用视觉特征。

### 3D关键点提取 (3D Keypoint Extraction)

这是方法的核心创新——将2D多视图特征“提升”为显式3D体积表示，并在3D空间中直接预测关键点。

**2D→3D特征提升。** 聚合特征 $\mathbf{F}_{\mathrm{agg}}$ 首先经过变换 $\phi_{\mathrm{kp}}$ 得到多视图关键点特征 $\mathbf{F}_{\mathrm{kp}}$：

$$
\mathbf{F}_{\mathrm{kp}} = \phi_{\mathrm{kp}}(\mathbf{F}_{\mathrm{agg}})
$$

随后，对于一个预定义的3D体素网格 $\Omega$（默认分辨率 $M = 72$），每个体素中心 $\mathbf{x}$ 被投影到各个视图的像平面上，通过双线性插值采样对应的2D特征：

$$
\mathbf{f}_k(\mathbf{x}) = \mathrm{bilinear\_sample}(\mathbf{F}_{\mathrm{kp}}^{(k)}, u_k(\mathbf{x}))
$$

其中 $u_k(\mathbf{x})$ 是体素中心在第 $k$ 个视图上的投影坐标。跨视图的特征通过软注意力机制进行融合，得到每个体素的最终特征 $\mathbf{V}(\mathbf{x})$：

$$
\mathbf{V}(\mathbf{x}) = \sum_{k=1}^{K} \omega_k \cdot \mathbf{f}_k(\mathbf{x}), \quad \omega_k = \mathrm{softmax}_k(\{\mathbf{f}_k\}_{k=1}^{K})
$$

这种软注意力聚合（softmax）被消融实验（Table 5f）证明优于基于可见性的硬聚合（visibility-based），后者因深度估计误差导致性能下降（MPJPE 127.12 vs 121.34）。

**体积热力图与积分回归。** 构建好的3D特征体积 $\mathbf{V}$ 通过一个3D卷积网络处理，为每个关键点 $n$ 输出一个体积热力图 $\mathbf{H}_n$。最终，每个关键点的3D坐标 $\mathbf{s}_n$ 通过积分回归以可微分的方式获得：

$$
\mathbf{s}_n = \sum_{\mathbf{x} \in \Omega} \mathbf{x} \cdot \mathrm{softmax}(\mathbf{H}_n(\mathbf{x}))
$$

这种“3D体积特征 → 3D热力图 → 3D关键点”的显式3D建模策略，相比“2D关键点检测 → 三角化”的传统方案，在 MPJPE 上实现了质的飞跃（121.34 vs 172.74，Table 3b），证明了在3D空间中端到端建模对几何一致性至关重要。

### 自监督训练管线 (Self-Supervised Training Pipeline)

训练过程无需任何3D标注，完全依赖扩散模型生成的多视图图像作为监督信号。默认使用 $K = 4$ 个视图（1个输入视图 + 3个生成视图）。

**结构线索的提供。** 预测的3D关键点 $\mathbf{S}$ 被投影到各生成视图的像平面上：

$$
\mathbf{S}_{\mathrm{hom}}^{(k)} = [\mathbf{S} \ \mathbf{1}] \cdot \mathbf{P}_k^{\top}
$$

基于投影后的2D关键点，利用可学习的邻接矩阵 $\mathcal{A} \in \mathbb{R}^{N \times N}$ 作为软边门控，在图像上绘制可微分的高斯线条，构建软边图（soft edge map）。该边图为后续的重建网络提供了显式的结构线索——骨架般的几何约束。

**重建损失。** 一个轻量重建网络以软边图作为条件，尝试重建对应的生成视图。训练损失为多视图 VGG 感知损失和边缘掩码损失的加权组合：

$$
\mathcal{L} = \frac{1}{K} \sum_{k=1}^{K} \left( \lambda_{\mathrm{vgg}} \cdot \mathcal{L}_{\mathrm{vgg}}^{(k)} + \lambda_{\mathrm{mask}} \cdot \mathcal{L}_{\mathrm{mask}}^{(k)} \right)
$$

消融实验揭示了两个关键设计选择：(1) 生成视图数量 $K$ 从1增加到3时性能大幅提升，在 $K \geq 3$ 后趋于饱和（Table 3c），默认 $K = 4$；(2) 对输入图像施加随机仿射变换（random affine）可防止重建网络走“捷径”（如直接记忆像素位置），显著提升性能（MPJPE 134.54 → 121.34，Table 5d）。

### 辅助约束：视角一致性损失

为进一步增强3D几何的一致性，方法在特征空间施加随机3D旋转扰动，约束关键点投影的跨视角一致性（详见附录D.1）：

$$
\mathcal{L}_{\mathrm{vic}} = \frac{1}{N} \sum_{i=1}^{N} \left\| \mathbf{S}_i - \mathbf{S}_{\mathrm{rot},i} \right\|_2^2
$$

该损失鼓励模型对同一物体在不同3D旋转下的关键点预测保持一致，从而隐式地学习视角不变的表征。

### 关键设计选择的因果解释

综合消融实验，KeyDiff3D 的性能提升可归因于以下因果链条：

1. **扩散特征优于传统特征**：SV3D-p 的多视图扩散特征蕴含了通过大规模数据学到的隐式3D几何先验，这是 ResNet/CLIP/DINOv2 等单视图2D预训练特征所不具备的。
2. **3D显式建模优于2D后处理**：直接在3D体积空间中预测关键点，避免了2D检测后三角化带来的误差累积和几何不一致。
3. **多视图监督不可或缺**：单视图自监督（$K = 1$）无法提供足够的几何约束，而少量生成视图（$K \geq 3$）即可显著改善性能。
4. **软边图提供有效结构先验**：可学习的邻接矩阵和可微分高斯线条为重建网络提供了类骨架的结构线索，使其能够更有效地利用重建损失来优化关键点位置。

## 实验与分析

### 一、核心定量结果

#### 1.1 Human3.6M 3D关键点估计

在Human3.6M数据集上，KeyDiff3D以单张RGB图像为输入，在完全无监督的设置下取得了具有竞争力的3D关键点估计精度。如 **Table 1** 所示，在默认配置（N=18关键点、2层MLP回归）下，本方法达到MPJPE 121.34 mm、N-MPJPE 118.29 mm、P-MPJPE 85.26 mm，全面超越同类单视图无监督基线 **Honari et al.**（MPJPE 125.73 mm，32关键点）。当关键点数量增至32时，MPJPE进一步降至119.07 mm。

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparison of 3D keypoint on the Human3.6M dataset. * denotes results on a simplified subset with six actions*

值得注意的是，KeyDiff3D仅使用单帧图像推理，其P-MPJPE（85.26 mm）甚至优于使用2个校准视图的多视图方法 **BKinD-3D**（P-MPJPE 89.05 mm），表明从扩散先验中提取的隐式3D几何信息具有强大的表征能力，能够部分弥补显式多视图几何约束的缺失。

#### 1.2 CUB-200-2011 2D关键点估计

在鸟类数据集CUB-200-2011上，本方法在2D关键点检测任务中也展现出优势。如 **Table 2** 和 **Table 4** 所示，在CUB-align子集（KP=10）上，KeyDiff3D的归一化L2距离为5.16，显著优于 **StableKeypoints**（6.38，复现结果）和 **AutoLink**（6.7）等2D无监督方法；在更具挑战性的CUB-all子集上，本方法（5.5）同样优于StableKeypoints（6.0）。需要指出的是，为确保公平比较，**Table 4** 中所有复现结果均使用相同的预处理数据、训练/测试划分及原作者提供的官方代码。

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison of unsupervised 2D keypoints on CUB-200-2011 [61] dataset. We report the*

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/010_Table_4.jpg]]
*Table 4: Reproduced results on CUB-align and CUB-all dataset. For fair comparison, reproduced results are obtained using the identical preprocessed dataset with same train/test splits, and official source codes provided by the authors. We report reproduced results for CUB-all*

### 二、消融实验：设计选择的因果验证

消融实验系统性地验证了KeyDiff3D各核心设计选择对性能的因果贡献，所有消融均在Human3.6M上以2层MLP回归进行评估。

#### 2.1 扩散特征 vs. 传统2D主干网络

**Table 3 (a)** 揭示了特征源的选择对性能的决定性影响。将多视图扩散特征（SV3D-p）替换为传统单视图2D基础网络后，性能急剧下降：ResNet50的MPJPE为172.25 mm（+50.91），CLIP为192.46 mm（+71.12），DINOv2为155.12 mm（+33.78）。这一巨大差距表明，扩散U-Net中间层蕴含的隐式多视图几何先验远非通用视觉特征所能替代——扩散模型在去噪过程中被迫维护多视图一致性，其内部特征自然编码了3D结构信息。

#### 2.2 3D体积建模 vs. 2D检测+三角化

**Table 3 (b)** 对比了两种3D关键点获取策略：本方法的“3D特征→体积热力图→积分回归”与传统的“2D关键点检测→多视图三角化”。结果显示，显式3D体积建模（MPJPE 121.34 mm）远优于2D检测后三角化（MPJPE 172.74 mm）。这一发现的核心原因在于：2D检测器在各视图上独立预测，缺乏跨视图的几何一致性约束，导致三角化对检测误差高度敏感；而3D体积网络在融合阶段即已隐式建模了多视图几何关系，输出的热力图天然具备3D一致性。

#### 2.3 生成视图数量的影响

**Table 3 (c)** 考察了训练时使用的扩散生成视图数量K对性能的影响。仅使用输入视图（K=1）时MPJPE高达166.29 mm，验证了多视图监督的必要性。引入生成视图后性能持续提升：K=2时降至133.06 mm，K=3时进一步降至124.90 mm，K=4（默认配置）达到121.34 mm。K≥3后收益递减，表明3-4个互补视图已能提供足够的多视图几何约束，更多视图带来的边际增益有限。

#### 2.4 关键点数量与扩散时间步

**Table 5 (a)** 显示，增加关键点数量可稳定提升回归精度：N=18（默认）时MPJPE为121.34 mm，N=32时为119.07 mm，N=48时为116.45 mm。作者选择N=18作为默认配置是为了兼顾可解释性——更少的关键点更易形成语义清晰的对应关系。

**Table 5 (b)** 表明扩散时间步τ=500为最优选择（MPJPE 121.34 mm），τ=300时升至126.97 mm，τ=700时升至130.16 mm。τ过小时扩散特征尚未充分融合全局结构，τ过大时特征趋于纯噪声，均不利于几何信息的提取。

#### 2.5 训练策略消融

**Table 5 (d)** 揭示了输入增强的关键作用：移除随机仿射变换后MPJPE从121.34 mm升至134.54 mm（+13.20）。随机仿射变换迫使重建网络不能依赖像素位置的简单记忆，从而学习到更具泛化性的几何表征。

**Table 5 (f)** 比较了视图聚合方式：softmax注意力聚合（121.34 mm）优于基于可见性的硬聚合（127.12 mm）。可见性聚合受深度估计误差影响，容易在遮挡边界处引入噪声；softmax机制通过学习自适应权重，能够更鲁棒地融合多视图信息。

### 三、计算开销分析

**Table 6** 报告了推理时的计算开销对比。KeyDiff3D的关键点提取模块（不含扩散模型前传）计算量为291.10 GFLOPs，与 **BKinD-3D**（296.27 GFLOPs）相当，远低于 **KeypointNet**（700.83 GFLOPs）。然而，扩散模型前传本身需要约7787 GFLOPs，使得整体推理开销显著高于传统方法，这是本方法当前的主要效率瓶颈。

### 四、跨域泛化能力

如 **Figure 5** 所示，在Human3.6M上训练的模型可直接泛化至自然场景（DAVIS）和跨域数据（GSO），在Stanford Dogs上训练的模型可泛化至AP-10K灵长类数据集。这种跨域泛化能力源于：扩散先验提供的是类别无关的通用3D几何线索，而非人体特化的骨架结构约束，使得学到的关键点提取机制具有类别通用性。

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/007_Figure_5.jpg]]
*Figure 5: Out-of-domain generalization results. (a) In-the-wild DAVIS results and (b) out-of-domain GSO results using a model trained on Human3.6M. (c) AP-10K results using a model trained on Stanford Dogs*

### 五、失败模式与局限性

**Figure 8** 揭示了本方法的两个典型失败模式：

1. **左右歧义**：模型无法可靠区分人体的左右对称部位（如左手与右手），这是单目无监督方法的固有问题——在缺乏时序或显式语义先验的情况下，对称部位在几何上完全等价。
2. **扩散生成质量依赖**：当预训练扩散模型（SV3D-p）无法生成合理内容时——例如严重遮挡区域或生成视图间存在不一致——关键点预测质量显著下降。这表明本方法的性能上限受限于底层扩散模型的生成能力。

### 六、关键图表结论速览

| 图表 | 核心结论 |
|------|----------|
| **Table 1** | KeyDiff3D在Human3.6M上全面超越单视图无监督基线，单帧推理即可媲美多视图方法 |
| **Table 2 / Table 4** | 在CUB-200-2011的2D关键点检测中优于StableKeypoints等专用2D方法 |
| **Table 3 (a)** | 扩散特征远优于ResNet50/CLIP/DINOv2，验证了扩散先验的独特价值 |
| **Table 3 (b)** | 3D体积建模显著优于2D检测+三角化，验证了显式3D表征的必要性 |
| **Table 3 (c)** | 3-4个生成视图即可提供充分的多视图约束 |
| **Table 5 (d)** | 随机仿射增强对防止过拟合至关重要（+13.20 MPJPE） |
| **Table 6** | 关键点模块计算量与传统方法相当，但扩散前传是效率瓶颈 |
| **Figure 8** | 左右歧义和扩散生成质量是当前的主要失败模式 |

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/009_Table_3.jpg]]
*Table 3: Ablation results on (a) 2D feature backbones, (b) 3D lifting strategies, and (c) the number of virtual viewpoints. All results are reported using 2-layer MLP regression*

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/013_Table_5.jpg]]
*Table 5: Additional ablation results on the Human3.6M dataset. ‘default’ indicates the default configuration used in our main experiments*

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/015_Table_6.jpg]]
*Table 6: Comparison of inference-time computational cost on an NVIDIA A6000 GPU*

### 补充图表

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/008_Figure_6.jpg]]
*Figure 6: Animatable 3D model results*

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results on the (a) CUB-200-2011 and (b) Stanford Dogs datasets*

![[assets/figures/papers/paper_list_l2620_https_arxiv_org_abs_2507_12336/figures/014_Figure_9.jpg]]
*Figure 9: Keypoint prediction results according to the number of keypoints*

## 方法谱系与知识库定位

### 1. 问题域定位

单目3D关键点发现的核心瓶颈在于：**单张图像到3D结构的映射是极度欠约束的**——深度歧义与自遮挡使得同一2D投影可对应无穷多种3D配置。传统解决方案依赖两类代价高昂的监督源：一是手工标注的3D关键点真值，二是校准的多视图图像。这两者均严重限制了方法的可扩展性与跨域泛化能力。

**KeyDiff3D** 在此问题域中占据了一个独特位置：它既不需要3D标注，也不需要校准的多视图数据，而是从预训练多视图扩散模型（SV3D-p）中"蒸馏"几何先验。这使其区别于现有工作的两条主线。

### 2. 与现有基线的谱系关系

#### 2.1 无监督3D关键点发现

现有无监督3D关键点方法可依监督形式分为两类：

**多视图训练方法**：
- **BKinD-3D** 在训练和推理阶段均依赖校准多视图图像，通过多视图一致性约束学习3D关键点。KeyDiff3D 在推理时仅需单张图像，且训练时使用扩散生成的合成视图替代校准多视图，从根本上解除了对物理多视图采集设备的依赖。
- **Honari et al.** 与 **KeypointNet** 虽支持单帧推理，但训练仍需校准多视图数据。KeyDiff3D 在 Table 1 中以单帧输入取得 MPJPE 121.34，优于 Honari et al. 的 125.73（32关键点，2层MLP回归），验证了扩散先验替代校准多视图的可行性。

**单目无监督人体姿态估计**：
- **Sosa et al.** 使用不成对的2D位姿，**Kundu et al. (unpaired 3D)** 使用不成对的3D数据，**Kundu et al. (kinematic)** 引入运动链约束，**Yang et al.** 结合多视图与骨架先验。这些方法的共同特点是依赖人体特定的结构先验（骨架拓扑、骨骼长度比例）。KeyDiff3D 不引入任何类别特定的结构先验，其关键点拓扑完全通过可学习邻接矩阵自适应发现，这使得同一框架可直接泛化至鸟类（CUB-200-2011）和犬类（Stanford Dogs），无需修改。

#### 2.2 2D无监督关键点检测

与 **StableKeypoints**、**AutoLink**、**GANSeg**、**Lorenz et al.** 等2D无监督方法相比，KeyDiff3D 的核心差异在于直接在3D空间中建模关键点。Table 3(b) 的消融实验表明：3D体积特征→3D关键点（MPJPE 121.34）远优于2D关键点检测→三角化（MPJPE 172.74），证明了显式3D建模对几何一致性的关键作用。

#### 2.3 扩散先验利用

KeyDiff3D 与 **StableKeypoints** 均利用扩散特征进行关键点检测，但存在本质区别：
- StableKeypoints 使用单视图扩散特征进行2D关键点检测；
- KeyDiff3D 利用多视图扩散模型（SV3D-p）同时生成多视图图像和多视图特征，并将这些特征提升为显式3D体积表示。

Table 3(a) 的消融实验量化了这种差异：多视图扩散特征（SV3D, MPJPE 121.34）大幅优于单视图基础主干（ResNet50 172.25, CLIP 192.46, DINOv2 155.12），表明多视图扩散模型蕴含的跨视角几何一致性是性能提升的关键来源。

### 3. 方法适用边界

**适用场景**：
- 单张RGB图像输入，无需相机参数、深度图或多视图；
- 适用于人体和动物等可形变对象，无需类别特定的骨架先验；
- 支持跨域泛化：Human3.6M训练的模型可直接应用于DAVIS自然场景和GSO合成对象，Stanford Dogs训练的模型可迁移至AP-10K灵长类数据。

**不适用或需谨慎使用的场景**：
- **左右歧义**：模型无法区分语义对称部位（如左手与右手），Figure 8 展示了此类失败案例。这是因为无监督学习缺乏语义标签来打破对称性。
- **扩散模型生成质量瓶颈**：当预训练SV3D模型无法生成合理内容时（如严重遮挡区域、多视图不一致），关键点预测质量随之下降。方法的性能上界受限于扩散先验的质量。
- **实时应用受限**：完整推理需执行扩散模型前传（约7787 GFLOPs），加上关键点模块（约291 GFLOPs），总计算开销远超传统检测器（Table 6），不适合对延迟敏感的场景。

### 4. 开放问题

1. **对称性消歧**：如何在不引入语义标签的前提下消除左右歧义？可能的路径包括引入时序运动信息（光流约束左右肢的运动模式差异）或几何自监督（如基于非对称纹理的隐式语义发现）。

2. **扩散先验的轻量化**：当前推理依赖完整扩散去噪过程（T=1000步），能否通过单步扩散蒸馏或一致性模型将扩散特征提取压缩至可实时运行的水平？这是方法走向实用的关键瓶颈。

3. **多对象与遮挡场景**：当前方法假设输入为单个前景对象（使用Grounded SAM提取掩码），如何扩展到多对象交互场景及部分遮挡情形？这需要解决实例级3D关键点分配和遮挡区域的几何补全。

4. **跨类别语义对齐**：当N=18时，人体和鸟类的关键点语义天然不同。能否通过跨类别联合训练，使关键点在不同类别间建立语义对应（如"头部""肢体末端"）？这将推动通用3D对象理解。

5. **视频序列的无监督3D理解**：当前方法逐帧独立处理，未利用时序一致性。将KeyDiff3D扩展到视频输入，利用时序平滑约束，可能同时提升精度和消除左右歧义。

## 原文 PDF

![[paperPDFs/CVPR_2026/Unsupervised_Monocular_3D_Keypoint_Discovery_from_Multi_View_Diffusion_Priors.pdf]]