---
title: "Any4D: Unified Feed-Forward Metric 4D Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Any4D_Unified_Feed_Forward_Metric_4D_Reconstruction.pdf
project_link: "https://any-4d.github.io"
code_link: null
aliases:
- Any4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 采用因式化的4D场景表示（自我中心的深度与相机内参，以及分配中心的场景流与相机姿态），使模型能在部分标注的混合数据上训练，并实现单次前馈推理多帧度量4D重建。
primary_logic: 直接预测分配中心场景流（而非其他运动表示）是最优的4D运动参数化方式，同时允许灵活融合多模态输入进一步提升精度。
claims:
- Any4D在4个3D跟踪基准上均取得最低的EPE和最高的APD，同时推理速度比SpatialTrackerV2快15倍以上
- 分配中心场景流在稠密场景流和稀疏点跟踪任务上均优于其他表示（如3D点后运动或反向投影2D流）
- 加入几何和雷达多普勒等多模态输入能持续提升Any4D的4D运动估计性能
- DriveTrack 上 Dynamic Points EPE↓ = 3.89
---

# Any4D: Unified Feed-Forward Metric 4D Reconstruction

> [!tip] 核心洞察
> 直接预测分配中心场景流（而非其他运动表示）是最优的4D运动参数化方式，同时允许灵活融合多模态输入进一步提升精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | Any4D：统一的前馈度量4D重建 |
| 英文题名 | Any4D: Unified Feed-Forward Metric 4D Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.10935) · [Project](https://any-4d.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Any4D |
| Dataset | DriveTrack, Dynamic Replica, Kubric-4D Dynamic Camera, Kubric-4D Static Camera |

> [!tip] 效果简介
> - DriveTrack 上，Dynamic Points EPE↓ 3.89 vs 5.45 (SpatialTrackerV2) (-1.56)。
> - Dynamic Replica 上，Dynamic Points APD↑ 93.44 vs 62.34 (SpatialTrackerV2) (+31.10)。
> - Kubric-4D Dynamic Camera 上，Scene Flow EPE↓ 0.17 vs 1.70 (St4RTrack) (-1.53)。

## 概要

4D重建——从多帧视频中同时恢复稠密几何与运动——是自动驾驶、增强现实和机器人操作等应用的基础感知任务。然而，现有方法普遍存在三个瓶颈：**（1）无法统一处理多帧稠密几何与运动预测**，通常只能输出稀疏点跟踪或独立的两帧场景流/深度；**（2）输出缺乏度量尺度**，只能得到尺度模糊或归一化后的结果；**（3）难以利用多模态传感器数据**（如深度图、IMU位姿、雷达多普勒），限制了在真实部署场景中的精度与鲁棒性。此外，大规模高质量4D标注数据的稀缺进一步加剧了这些挑战。

针对上述问题，本文提出 **Any4D**——一个统一的前馈度量4D重建模型。Any4D 的核心洞察是：**直接预测分配中心场景流（allocentric scene flow）是4D运动的最优参数化方式**，同时允许灵活融合多模态输入以进一步提升精度。具体而言，Any4D 采用因式化的4D场景表示，将输出分解为全局度量尺度、每视图的自我中心因素（光线方向与归一化深度）以及分配中心因素（前向场景流与相机姿态）。这种因式化设计使得模型能够在部分标注的混合数据上训练，并在单次前馈推理中从任意 N 帧输入生成度量尺度的稠密4D重建。

Any4D 在多个基准上取得了领先性能。在稀疏3D点跟踪任务上，Any4D 在 DriveTrack 和 Dynamic Replica 等4个基准上均取得最低的端点误差（EPE）和最高的平均点距离内比例（APD），同时推理速度比 **SpatialTrackerV2** 快 15 倍以上（Table 1）。在稠密场景流估计上，Any4D 在 Kubric-4D 数据集上的 EPE 仅为 0.17，较 **St4RTrack** 降低 1.53，且内点比例 τ 从 20.51 提升至 87.51（Table 2）。消融实验证实，分配中心场景流作为运动表示在稠密场景流和稀疏点跟踪任务上均优于其他表示（如3D点后运动或反向投影2D流），而加入几何与雷达多普勒等多模态输入能持续提升4D运动估计性能（Table 4, Table 5）。

在方法谱系上，Any4D 属于**前馈多视图Transformer**家族，与 **VGGT** 等前馈几何方法共享类似的多视图注意力骨干，但其关键创新在于将几何与运动统一到因式化度量空间中，并支持多模态传感器输入。相较于需要后处理优化或多次前馈的基线（如 **MonST3R+CoTracker3** 的组合方案），Any4D 实现了真正的单次前馈推理，在效率与精度之间取得了显著突破。

从多帧视频中同时恢复稠密的3D几何与运动——即度量4D重建——是计算机视觉的核心目标之一，其应用涵盖自动驾驶、机器人导航、AR/VR以及动态场景理解。尽管近年来单目深度估计、多视图立体和运动结构恢复（SfM）各自取得了长足进步，但将这些能力统一到一个前馈框架中，并在度量尺度下输出稠密、时域一致的4D表示，仍然是一个开放难题。

### 现有方法的缺口

当前4D重建领域存在三个关键瓶颈：

**1. 能力碎片化。** 现有模型通常只解决4D重建的部分子任务，缺乏统一性。例如，**SpatialTrackerV2** 仅输出稀疏的3D点跟踪，无法提供逐像素的稠密运动场；**St4RTrack** 虽然预测稠密场景流，但其运动估计在物体边界和背景区域存在严重噪声（见 Figure 4）。将几何重建与2D跟踪组合的流水线（如 **MonST3R + CoTracker3** 或 **VGGT + CoTracker3**）则引入多阶段误差累积，且无法在统一的度量空间内联合优化几何与运动。

**2. 尺度模糊与传感器利用不足。** 绝大多数方法仅以RGB图像为输入，输出缺乏真实的度量尺度——深度和运动要么是尺度模糊的，要么需要后处理归一化对齐。这严重限制了在机器人、自动驾驶等需要精确物理尺度的场景中的实用性。同时，现有方法无法灵活融合多模态传感器数据（如深度图、IMU位姿、雷达多普勒速度），而这些信号在真实系统中往往可用，并能显著提升运动估计精度。

**3. 数据稀缺与泛化困难。** 大规模、高质量的稠密4D标注数据（同时包含逐像素深度、场景流和3D点跟踪真值）极度稀缺。现有方法通常在单一数据集上训练，难以泛化到不同场景、不同帧数和不同传感器配置。此外，多数模型仅支持2帧输入，无法有效利用更长时序信息。

### 本文动机

针对上述缺口，Any4D 提出了一个统一的前馈框架，旨在实现以下目标：

- **统一预测**：从任意N帧视频中，单次前馈即输出稠密的度量尺度4D重建，包括相机姿态、逐像素深度（几何）和场景流（运动）。
- **度量尺度**：显式预测全局度量尺度因子，使输出可直接用于下游物理任务，无需后处理对齐。
- **多模态融合**：架构原生支持RGB图像、深度图、相机内参/姿态、雷达多普勒等多种输入模态，灵活组合以提升精度。
- **高效推理**：相比需要迭代优化或多次前馈的基线方法，Any4D 在保持甚至超越其精度的同时，实现数量级的速度提升（见 Table 1，约15–23倍快于 SpatialTrackerV2）。

核心洞察在于，通过因式化的4D场景表示——将自我中心因素（深度、光线方向）与分配中心因素（场景流、相机姿态）分离——模型可以在部分标注的混合数据上训练，并实现鲁棒的多帧泛化。其中，**分配中心场景流**被证明是最优的4D运动参数化方式，相比3D点后运动或反向投影2D流等表示，能产生更干净的物体边界和背景运动估计（见 Table 5 和 Figure 5）。

## 核心方法与创新机理

Any4D 的核心创新在于通过**因式化的度量4D场景表示**与**单次前馈多模态架构**，突破了现有4D重建方法在表示能力、传感器融合和推理效率上的根本瓶颈。其关键设计可归纳为以下五个维度的 changed slots：

### 1. 因式化度量4D输出：统一几何、运动与尺度

现有方法通常将几何重建、运动估计和尺度恢复视为独立或松耦合的任务，导致输出缺乏度量一致性。Any4D 将4D重建因式化为一个全局度量尺度因子与每视图的自我中心因素（光线方向、归一化深度）和分配中心因素（前向场景流、相机姿态）：

$$( \tilde { s } , \{ \tilde { R } _ { i } , \tilde { D } _ { i } , \tilde { T } _ { i } , \tilde { F } _ { i } \} _ { i = 1 } ^ { N } ) = \mathrm { A n y 4 D } ( \mathbf { I } , \mathbf { O } )$$

这种因式化设计使得模型能够在**部分标注的混合数据**上训练——不同数据集可能只提供深度、姿态或场景流中的部分真值——从而缓解了大规模高质量4D标注数据稀缺的瓶颈。最终通过组合因子恢复度量尺度点云 $\tilde { \mathbf { G } } _ { i } = \tilde { s } \cdot \tilde { T _ { i } } \cdot \tilde { R } _ { i } \cdot \tilde { D } _ { i }$ 和度量场景流 $\tilde { M } _ { i } = \tilde { s } \cdot \tilde { F } _ { i }$，实现了输出从“尺度模糊”到“全局度量”的跃迁。

### 2. 分配中心场景流：最优的4D运动参数化

运动表示的选取是4D重建的核心因果旋钮。Any4D 通过消融实验（Table 5）系统比较了多种运动表示——包括3D点后运动（如 St4RTrack 所采用）、反向投影2D流等——并证明**直接预测分配中心前向场景流**在稠密场景流和稀疏点跟踪任务上均取得最优的 EPE 和 τ 指标。Figure 5 进一步从定性角度揭示：分配中心流产生的运动边界最为清晰，而3D点后运动在物体边缘和背景区域会产生严重噪声。这一发现构成了 Any4D 运动预测精度领先的关键基础。

### 3. 多模态传感器灵活融合

Any4D 将输入空间从单一的 RGB 图像扩展至**RGB + 深度图 + 相机姿态 + 雷达多普勒**等多模态信号。架构层面，通过模态特定的编码器将异构输入映射到统一特征空间，再由交替注意力 Transformer 进行跨视点聚合。Table 4 的消融实验证实：加入几何信息（深度、内参、姿态）和多普勒速度可一致提升稠密场景流和稀疏3D跟踪的性能。Figure S.3 的定性案例显示，纯图像变体在场景流边缘处偶有偏移，而引入稀疏几何和多普勒标注后预测质量显著改善。这种多模态灵活性使 Any4D 能够利用自动驾驶等场景中日益丰富的传感器配置，突破了传统方法仅依赖 RGB 的限制。

### 4. 单次前馈推理任意帧数

与需要后处理优化或多次前馈的基线（如 SpatialTrackerV2）不同，Any4D 实现了**单次前馈**即可处理任意 N 帧输入。Table 1 显示，在 50 帧输入下，Any4D 的推理时间仅为 0.50 秒（H100 GPU），比 SpatialTrackerV2 快约 23 倍。这一效率优势源于因式化表示避免了帧间迭代优化，同时 N 视点 Transformer 架构天然支持可变帧数。Figure S.1 的消融进一步揭示了关键训练策略：**4视点训练**对于多帧泛化至关重要——仅用 2 视点训练的模型在输入帧数增加时 EPE 显著升高，而 4 视点模型在高达 64 帧时仍保持稳定。

### 5. 稠密且精确的运动估计

现有方法在运动估计上呈现两极分化：SpatialTrackerV2 等提供可靠但稀疏的跟踪（受限于 GPU 内存，最多均匀查询约 2500 个点），而 St4RTrack 等虽输出稠密运动但精度不足（尤其在物体边界和背景区域）。Any4D 通过直接预测逐像素场景流，实现了**稠密且精确**的运动估计（Figure 4），无需依赖预计算的分割掩码，仅通过阈值化场景流输出即可获得高质量的二值运动掩码。这一能力使 Any4D 在 4 个 3D 跟踪基准上均取得最低的 EPE 和最高的 APD（Table 1-2），同时保持稠密输出。

**需要手动验证的点**：部分 baseline 方法（如 SpatialTrackerV2、St4RTrack、MonST3R+CoTracker3 等）的具体作者/年份/出处未在提供的分析材料中明确标注，如需在正式论文中引用，建议查阅原文确认完整元数据。

Any4D 是一个统一的前馈 Transformer 模型，其核心设计目标是用**单次前馈推理**从任意 N 帧输入中直接输出**度量尺度稠密 4D 重建**。整体 pipeline 采用因式化表示策略，将复杂的 4D 场景解耦为全局尺度因子、自我中心（egocentric）因素和分配中心（allocentric）因素三个层次，使模型能在部分标注的混合数据上联合训练。

### 输入与输出流

模型的输入包括 RGB 图像序列 $\mathbf{I}$ 和可选的多模态观测 $\mathbf{O}$（如深度图、相机内参/姿态、雷达多普勒速度等）。输出为一个全局度量尺度因子 $\tilde{s}$ 以及每视图的因式化因素：

$$( \tilde { s } , \{ \tilde { R } _ { i } , \tilde { D } _ { i } , \tilde { T } _ { i } , \tilde { F } _ { i } \} _ { i = 1 } ^ { N } ) = \mathrm { A n y 4 D } ( \mathbf { I } , \mathbf { O } )$$

其中 $\tilde{R}_i$ 为光线方向、$\tilde{D}_i$ 为归一化深度、$\tilde{T}_i$ 为相机姿态、$\tilde{F}_i$ 为前向分配中心场景流（公式 1）。这些因素通过简单的代数组合即可恢复度量尺度的几何与运动：

- **度量点云**：$\tilde{\mathbf{G}}_i = \tilde{s} \cdot \tilde{T}_i \cdot \tilde{R}_i \cdot \tilde{D}_i$（公式 2）
- **度量场景流**：$\tilde{M}_i = \tilde{s} \cdot \tilde{F}_i$（公式 3）
- **运动后点云**：$\tilde{\mathbf{G}}'_i = \tilde{\mathbf{G}}_i + \tilde{M}_i$（公式 4）

### 模块关系

Any4D 的 pipeline 由五类功能模块串联构成（见 Figure 3）：

1. **多模态输入编码器**：将 RGB 图像、深度、多普勒、相机内参和姿态等异构输入映射到统一的 token 特征空间，实现灵活的传感器融合。

2. **交替注意力 Transformer 骨干网络**：采用多视点 Transformer 架构，通过交替注意力机制聚合 N 个视图的 token，产生上下文感知的补丁嵌入。该骨干网络是信息融合的核心，使几何和运动线索在视图间充分交互。

3. **几何密集预测头（Geometry DPT Head）**：基于 DPT 架构，从 Transformer 输出 token 中预测每视图的光线方向 $\tilde{R}_i$、归一化深度 $\tilde{D}_i$ 和置信度掩码。

4. **运动密集预测头（Motion DPT Head）**：另一个独立的 DPT 头，专门预测每视图的前向分配中心场景流 $\tilde{F}_i$——这是论文论证的最优 4D 运动参数化方式。

5. **姿态解码器与度量尺度解码器**：姿态解码器预测每视图的平移和四元数姿态 $\tilde{T}_i$；度量尺度解码器预测全局尺度因子 $\tilde{s}$，使输出具有真实的物理尺度。

### 设计要点

- **因式化表示**：将 4D 重建分解为自我中心因素（深度、光线方向）和分配中心因素（场景流、相机姿态），使得模型可以在仅有部分标注的数据集上训练（例如某些数据集只提供深度真值，另一些只提供场景流真值）。
- **分配中心场景流**：直接预测分配中心场景流而非其他运动表示（如 3D 点后运动或反向投影 2D 流），是 Any4D 在运动估计上取得优势的关键设计选择（Table 5 消融实验证实该表示在稠密场景流和稀疏点跟踪任务上均最优）。
- **多模态融合**：模型原生支持 RGB 之外的深度、姿态、多普勒等输入，且消融实验表明加入几何和雷达多普勒输入能持续提升 4D 运动估计性能（Table 4）。

整体框架的突出优势在于：单次前馈即可完成从任意帧数到度量 4D 重建的端到端映射，无需后处理优化或多步推理，在推理速度上比 SpatialTrackerV2 快 15 倍以上（Table 1）。

![[assets/figures/papers/paper_list_l2441_https_arxiv_org_abs_2512_10935/figures/001_Figure_1.jpg]]
*Figure 1: Any4D is a flexible feed-forward model capable of producing dense metric 4D reconstructions using N frames as input. Any4D is up to 15× faster and 3× better than prior state-of-the-art, where performance can be further boosted by using diverse sensors as input. Note that Any4D produces dense 3D tracking vectors, but here we visualize the sparse 3D motion tracks for simplicity*

Any4D 的核心设计是将稠密度量 4D 重建分解为一组可联合预测的因子，并通过一个多视点 Transformer 在单次前馈中统一输出。其整体映射关系为：

$$( \tilde { s } , \{ \tilde { R } _ { i } , \tilde { D } _ { i } , \tilde { T } _ { i } , \tilde { F } _ { i } \} _ { i = 1 } ^ { N } ) = \mathrm { A n y 4 D } ( \mathbf { I } , \mathbf { O } )$$

其中 $\mathbf{I}$ 为 $N$ 帧 RGB 图像，$\mathbf{O}$ 为可选的多模态输入（深度图、相机姿态、雷达多普勒等）。输出包括一个全局度量尺度因子 $\tilde{s}$，以及每帧 $i$ 的自我中心因子（光线方向 $\tilde{R}_i$、尺度归一化深度 $\tilde{D}_i$）和分配中心因子（前向场景流 $\tilde{F}_i$、相机姿态 $\tilde{T}_i$）。

### 多模态输入编码器与交替注意力骨干

模型首先通过模态特定编码器将异构输入映射到统一特征空间。RGB 图像、深度图、多普勒速度、相机内参和姿态分别经过独立编码后，与可学习的位置嵌入一同送入交替注意力 Transformer 骨干网络。该骨干在多视点令牌之间执行交替的 self-attention 和 cross-attention，生成上下文感知的补丁嵌入，作为后续各预测头共享的中间表示。

### 几何密集预测头（Geometry DPT Head）

几何头采用 Dense Prediction Transformer（DPT）结构，从共享令牌中预测每视图的三项输出：
- **光线方向** $\tilde{R}_i$：每个像素对应的相机射线方向。
- **尺度归一化深度** $\ddot{D}_i$：缺乏度量尺度的相对深度值。
- **置信度掩码**：指示每个像素深度预测的可靠性。

### 运动密集预测头（Motion DPT Head）

第二个 DPT 头专门预测每视图的**前向分配中心场景流** $\tilde{F}_i$。这是 Any4D 的核心运动表示——直接预测从当前帧到下一帧的 3D 位移向量，而非预测运动后的 3D 点位置或反向投影 2D 光流。消融实验（Table 5）表明，这种参数化方式在稠密场景流和稀疏点跟踪任务上均优于其他表示（如 3D 点后运动），能产生更干净的物体边界和背景运动估计。

### 姿态解码器与度量尺度解码器

- **姿态解码器**：从全局令牌中回归每帧的平移向量和四元数 $\tilde{T}_i$（含旋转分量）。
- **度量尺度解码器**：预测一个全局标量 $\tilde{s}$，将归一化的几何与运动输出恢复为度量尺度。

### 度量尺度恢复公式

获得所有因子后，通过以下组合恢复度量尺度的几何与运动：

**度量尺度点云**：
$$\tilde { \mathbf { G } } _ { i } = \tilde { s } \cdot \tilde { T _ { i } } \cdot \tilde { R } _ { i } \cdot \tilde { D } _ { i }$$

该式将全局尺度 $\tilde{s}$、相机姿态 $\tilde{T}_i$、光线方向 $\tilde{R}_i$ 和归一化深度 $\tilde{D}_i$ 组合，得到当前帧的度量尺度点云 $\tilde{\mathbf{G}}_i$。

**度量尺度场景流**：
$$\tilde { M } _ { i } = \tilde { s } \cdot \tilde { F } _ { i }$$

将归一化的前向场景流 $\tilde{F}_i$ 乘以全局尺度因子，恢复真实的度量尺度运动向量。

**运动后点云**：
$$\tilde { \mathbf { G } } ^ { \prime } { } _ { i } = \tilde { \mathbf { G } } _ { i } + \tilde { M } _ { i }$$

将场景流施加到当前点云上，得到下一帧的点云预测，用于与真值比较计算跟踪误差。

### 关键设计决策

1. **因式化表示的因果作用**：将自我中心（深度、光线）与分配中心（场景流、姿态）因素分离，使模型能在部分标注的混合数据上训练——例如某些数据集仅有深度标注，另一些仅有场景流标注，Any4D 可分别监督对应因子，从而利用更大规模的多源数据。

2. **分配中心场景流的最优性**：相比预测运动后 3D 点位置或反向投影 2D 流，直接预测前向场景流在物体边界和背景区域产生显著更少的噪声（Figure 5），这是 Any4D 在多个基准上取得领先性能的关键因果机制。

3. **4 视点训练对多帧泛化的必要性**：补充实验（Figure S.1）表明，仅使用 2 视点训练的模型在输入帧数增加时 EPE 显著升高，而 4 视点训练的模型在高达 64 帧输入时仍保持稳定性能。

## 实验与关键发现

### 主实验结果

Any4D 在稀疏 3D 点跟踪、稠密场景流估计和视频深度估计三个核心任务上均取得最优性能，同时保持单次前馈的高推理效率。

**稀疏 3D 点跟踪。** 在 DriveTrack、Dynamic Replica、LSFOdyssey 和 PointOdyssey 四个基准上，Any4D 在所有指标上均超越此前最优方法 SpatialTrackerV2（Table 1）。具体而言，在 DriveTrack 上动态点 EPE 从 5.45 降至 3.89（降低 28.6%），在 Dynamic Replica 上 APD 从 62.34 跃升至 93.44（提升 31.1 个百分点）。在推理速度方面，以 50 帧输入在 H100 GPU 上测算，Any4D 仅需 0.50 秒，而 SpatialTrackerV2 需要 11.56 秒，加速超过 23 倍。值得注意的是，SpatialTrackerV2 仅能均匀查询最多 2500 个稀疏点，而 Any4D 直接输出稠密逐像素运动估计（Figure 4）。

**稠密场景流估计。** 在 Kubric-4D 和 LSFOdyssey 数据集上，Any4D 显著优于基线方法（Table 2）。在 Kubric-4D Dynamic Camera 设置下，Any4D 的场景流 EPE 为 0.17，St4RTrack 为 1.70，误差降低约 9 倍；在 Static Camera 设置下，τ 指标（小于 0.1m 的内点比例）从 St4RTrack 的 20.51 提升至 87.51，提升 67 个百分点。与 MonST3R+CoTracker3 和 VGGT+CoTracker3 等组合式方案相比，Any4D 统一预测几何与运动的范式在精度上同样具有明显优势。

**视频深度估计。** 作为辅助任务，Any4D 在单步前馈方法中达到最优水平，且与迭代优化方法或专门针对深度估计训练的方法相比也具有竞争力（Table 3）。

### 消融实验

**分配中心场景流是最优运动表示。** 在 Kubric 稠密场景流和 LSFOdyssey 稀疏点跟踪两个基准上，Any4D 比较了四种运动输出表示：分配中心场景流（本文采用）、3D 点后运动（St4RTrack 提出）、反向投影 2D 流、以及 3D 点后运动与 3D 点运动的组合（Table 5）。结果表明，分配中心场景流在所有指标上均取得最优 EPE、APD 和 τ。Figure 5 的定性可视化进一步揭示，3D 点后运动表示在物体边界和背景区域会产生严重的噪声，而分配中心场景流则能提供最干净的重建结果。

**多模态输入持续提升性能。** Table 4 展示了不同辅助输入组合对 4D 运动估计的影响。仅使用 RGB 图像作为输入时，模型已具备较强基线性能；加入几何信息（深度图、相机内参和姿态）可一致降低 EPE 并提升 APD/τ；进一步加入雷达多普勒速度后，性能继续改善。Figure S.3 的定性结果显示，纯图像输入在边缘处有时会产生场景流偏移，而几何和多普勒信息的引入能有效修正这些误差。

**4 视点训练是多帧泛化的关键。** 补充实验（Figure S.1）表明，仅用 2 视点训练的 Any4D 在推理时输入帧数增加后 EPE 显著升高；而使用 4 视点训练的模型即使在 64 帧输入下仍保持稳定性能。这验证了多视点训练对于模型泛化到任意帧数输入的必要性。

### 失败模式与局限性

Any4D 在以下场景中重建质量会显著下降（Figure S.4）：

1. **大相机运动导致背景无视觉重叠。** 当相机运动幅度过大，前后帧之间背景区域几乎没有视觉对应时，模型难以建立可靠的多视点关联。
2. **场景运动占据图像大部分区域。** 当运动物体覆盖画面主体时，静态背景线索不足，模型对运动和几何的解耦能力受限。

论文指出，这些失败模式的根本原因在于训练数据中稠密场景流和 3D 跟踪标注的规模与多样性有限。作者认为，引入大规模稠密标注数据集并结合实时优化（如 BA 或在线 SLAM）是克服这些局限性的关键方向。

### 关键图表结论

- **Figure 4**：Any4D 提供稠密且精确的运动估计，仅需对场景流输出做阈值化即可获得高质量二值运动掩码；相比之下，SpatialTrackerV2 仅能输出可靠但稀疏的跟踪点，St4RTrack 虽能输出稠密运动但精度不足，尤其在物体边界和背景区域。
- **Table 1**：Any4D 在 4 个 3D 跟踪基准上均取得最低 EPE 和最高 APD，同时推理速度比最优基线快一个数量级。
- **Table 5**：分配中心场景流在所有运动表示中取得最优结果，验证了其作为 4D 运动参数化的设计选择。
- **Table 4**：几何和雷达多普勒等多模态输入的加入能持续提升 4D 运动估计精度。

![[assets/figures/papers/paper_list_l2441_https_arxiv_org_abs_2512_10935/figures/005_Table_1.jpg]]
*Table 1: Any4D showcases state-of-the-art sparse 3D point tracking, while providing dense motion predictions and being an order of magnitude faster than the closest performing baseline. We report end-point error (EPE), average points within delta (APD) and inlier ratio at 0.1m (τ ) for dynamic points in the benchmark. The runtime is computed on a H100 using 50 frames as input. Best results are bold*

![[assets/figures/papers/paper_list_l2441_https_arxiv_org_abs_2512_10935/figures/009_Table_5.jpg]]
*Table 5: Allocentric scene flow is the optimal output representation for 4D motion. We compare different representation types on dense scene flow (Kubric) and sparse 3D point tracking (LSFOdyssey) using end-point error (EPE), average points within delta (APD) and inlier ratio at 0.1m (τ ). Best results are bold*

![[assets/figures/papers/paper_list_l2441_https_arxiv_org_abs_2512_10935/figures/010_Table_4.jpg]]
*Table 4: Auxiliary inputs improve the 4D motion estimation performance of Any4D. We compare different inputs on both dense scene flow (Kubric) and sparse 3D point tracking (LSFOdyssey) benchmarks using end-point error (EPE), average points within delta (APD) and inlier ratio at 0.1m (τ ), where best is bold. “Geometry” indicates use of depth, intrinsics and poses*

![[assets/figures/papers/paper_list_l2441_https_arxiv_org_abs_2512_10935/figures/004_Figure_4.jpg]]
*Figure 4: Any4D provides dense and precise motion estimation, where on the other hand, state-of-the-art baselines either produce reliable but sparse motion (SpatialTrackerV2 [87]) or dense per-pixel motion that is not accurate (St4RTrack [16]). For SpatialTrackerV2, we are only able to uniformly query a maximum of 2500 points with a H100 GPU using 80 gigabytes of GPU memory. Note that we don’t use any pre-computed segmentation mask but purely threshold our scene flow output to get a binary motion mask. St4RTrack cannot produce good binary motion masks due to incorrect scene flow predictions on object boundaries and the background*

![[assets/figures/papers/paper_list_l2441_https_arxiv_org_abs_2512_10935/figures/015_Figure_S.4.jpg]]
*Figure S.4: Qualitative visualizations of Any4D limitations. Videos with large camera motion inducing no visual overlap of background or scene motion dominating the image space are common failure modes for Any4D. We believe that the availability of large-scale dense scene flow and 3D tracking datasets and integrating real-time optimization is key to overcoming these limitations*

## 定位与知识库关联

### 1. 与现有工作的关系

Any4D 在 4D 重建领域填补了“统一前馈度量重建”的空白。现有方法在能力上呈现碎片化格局（Figure 2）：一部分方法专注于稀疏 3D 点跟踪，如 **SpatialTrackerV2**（对比基线），能提供可靠的稀疏运动估计但无法输出稠密几何；另一类方法如 **St4RTrack**（对比基线）尝试预测逐像素稠密运动，但在物体边界和背景区域产生显著噪声（Figure 4）。还存在将几何重建与 2D 跟踪组合的流水线方案，如 **MonST3R + CoTracker3** 和 **VGGT + CoTracker3**（对比基线），但它们需要多阶段推理且缺乏统一的度量尺度。

Any4D 的核心差异化在于五个关键维度的统一提升：

| 维度 | 现有方法典型取值 | Any4D 的改进 | 证据锚点 |
|------|-----------------|-------------|---------|
| 输入帧数 | 通常 2 帧 | 任意 N 帧，支持 4-64 帧推理 | Section 3 |
| 输出表示 | 稀疏点跟踪或独立场景流/深度 | 因式化稠密度量 4D 重建（自我中心 + 分配中心因素） | Section 3 |
| 传感器模态 | 仅 RGB 图像 | RGB + 深度图 + 相机姿态 + 雷达多普勒等 | Section 1, 3.1 |
| 尺度 | 尺度模糊或归一化 | 预测全局度量尺度因子 | Section 3 |
| 推理方式 | 需要后处理优化或多次前馈 | 单次前馈 | Section 1, 3 |

这种统一能力使 Any4D 在 4 个 3D 跟踪基准上均取得最低的 EPE 和最高的 APD，同时推理速度比 SpatialTrackerV2 快 15 倍以上（Table 1）。在稠密场景流估计上，Any4D 在 Kubric-4D 数据集上相比 St4RTrack 的 EPE 降低 1.53（动态相机场景），τ 指标提升 67 个百分点（静态相机场景）（Table 2）。

### 2. 方法谱系中的定位

从技术路线看，Any4D 继承了多视图 Transformer 架构的设计范式（Section 3.1 提及类似 的结构），但其核心创新在于**因式化的 4D 场景表示**：将重建分解为全局度量尺度、每视图自我中心因素（光线方向与归一化深度）和每视图分配中心因素（前向场景流与相机姿态）。这种因式化设计使得模型能够在部分标注的混合数据上训练——不同数据集可能只提供深度、姿态或场景流的部分真值——从而缓解大规模高质量 4D 标注数据稀缺的瓶颈。

在运动表示层面，Any4D 通过消融实验（Table 5）证明**直接预测分配中心场景流是最优的 4D 运动参数化方式**，其在稠密场景流和稀疏点跟踪任务上均优于其他表示（如 3D 点后运动或反向投影 2D 流）。Figure 5 的定性可视化进一步显示，分配中心场景流能提供最干净的 4D 重建结果，而其他参数化方式在物体边界和背景区域产生极端噪声。

### 3. 适用边界与局限

尽管 Any4D 展现了强大的统一重建能力，其适用边界受以下因素制约：

1. **大相机运动场景失效**：当相机运动过大导致背景无视觉重叠，或场景运动占据图像大部分区域时，重建质量显著下降（Figure S.4）。这是前馈方法在缺乏迭代优化机制时的共性局限。

2. **训练数据依赖**：模型的鲁棒性受制于训练数据中稠密场景流与 3D 跟踪标注的规模与多样性。当前训练使用了多个数据集（Table S.1），但大规模高质量 4D 标注数据仍然稀缺。

3. **多帧泛化的训练条件**：消融实验（Figure S.1）表明，4 视点训练对于多帧泛化至关重要——仅用 2 视点训练的模型在输入帧数增加时 EPE 显著升高，而 4 视点模型在高达 64 帧时仍保持稳定。这意味着模型的扩展能力依赖于训练时的视点覆盖。

### 4. 开放问题

Any4D 的工作为以下方向留下了探索空间：

1. **实时优化集成**：如何将 BA（Bundle Adjustment）或在线 SLAM 等迭代优化机制集成入前馈框架，以解决大运动/无重叠场景下的失效问题？这是将方法推向实际部署的关键一步。

2. **长序列扩展**：能否将 Any4D 扩展到数百帧的长序列而保持前馈效率？当前验证的上限为 64 帧，更长序列可能面临计算和内存瓶颈。

3. **传感器受限场景的增强**：在没有雷达或深度传感器的通用平台上，能否通过自监督信号（如光度一致性、时序平滑性）进一步增强 4D 重建质量？Table 4 显示多模态输入能持续提升性能，但纯 RGB 变体在边缘区域仍存在偏移（Figure S.3）。

4. **数据瓶颈的突破路径**：模型性能的进一步提升是依赖于更大规模的混合 4D 数据集，还是可以通过更好的数据增强或生成式模拟来弥补？这关系到整个领域的发展方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Any4D_Unified_Feed_Forward_Metric_4D_Reconstruction.pdf]]
