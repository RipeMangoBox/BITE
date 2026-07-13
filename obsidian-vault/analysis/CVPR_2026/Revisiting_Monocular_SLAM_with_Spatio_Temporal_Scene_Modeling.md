---
title: Revisiting Monocular SLAM with Spatio-Temporal Scene Modeling
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Revisiting_Monocular_SLAM_with_Spatio_Temporal_Scene_Modeling.pdf
project_link: "https://merl.com/research/highlights/slam-mer"
code_link: null
aliases:
- SM
- RMSSTSM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 时空联合的3D点查询机制：通过维护近期帧的时序缓冲区和基于3D单元网格的空间查询，为每帧提供更丰富的3D-2D对应点，减少对稠密推断和过多关键帧的依赖。
primary_logic: 仅对关键帧使用前馈深度估计模型生成局部3D点，结合稀疏关键点跟踪实现实时定位，并利用锚点机制构建半稠密地图；这种混合设计将帧率提升至80 FPS以上，同时保持或提高定位精度。
claims:
- SLAM-MER 在 7-Scenes 的 office 序列上达到 100 FPS，并生成半稠密地图。
- 在 TUM RGB-D 和 7-Scenes 数据集上，SLAM-MER 的平均 ATE 分别为 0.056 m 和 0.059 m，帧率达到 86.6 FPS 和 103.2 FPS，效率远高于 MASt3R-SLAM 和 VGGT-SLAM。
- 7-Scenes (Dense Reconstruction) 上 RMSE (m) = 0.034
- TUM RGB-D (Uncalibrated Monocular) 上 相对帧率（FPS） = 86.6 FPS
---

# Revisiting Monocular SLAM with Spatio-Temporal Scene Modeling

> [!tip] 核心洞察
> 仅对关键帧使用前馈深度估计模型生成局部3D点，结合稀疏关键点跟踪实现实时定位，并利用锚点机制构建半稠密地图；这种混合设计将帧率提升至80 FPS以上，同时保持或提高定位精度。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于时空场景建模的单目SLAM重思考 |
| 英文题名 | Revisiting Monocular SLAM with Spatio-Temporal Scene Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Piedade_Revisiting_Monocular_SLAM_with_Spatio-Temporal_Scene_Modeling_CVPR_2026_paper.html) · [Project](https://merl.com/research/highlights/slam-mer) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SLAM-MER |
| Dataset | 7-Scenes, TUM RGB-D |

> [!tip] 效果简介
> - 7-Scenes (Dense Reconstruction) 上，RMSE (m) 0.034 vs 0.052 (best baseline from VGGT-SLAM) (-34.6%)。
> - TUM RGB-D (Uncalibrated Monocular) 上，相对帧率（FPS） 86.6 FPS vs DPV-SLAM++ / DROID-SLAM (约 3× (DPV-SLAM++) / >5× (DROID-SLAM) 更快)。

## 概要

单目视觉SLAM长期面临一个核心瓶颈：**缺乏显式的时空连续性建模**。传统方法依赖稀疏关键点与共视图，3D点检索效率低，导致关键帧数量膨胀；新兴的基于前馈深度估计的稠密方法（如MASt3R-SLAM、VGGT-SLAM）虽能生成丰富的几何先验，但每帧执行深度推断，计算量极大，难以在未标定条件下实现实时运行。

SLAM-MER 针对这一瓶颈提出了**时空联合的3D点查询机制**：通过维护近期帧的时序缓冲区保留短期跟踪连接，同时基于3D单元网格进行空间查询以获取可见地图点，从而为每帧提供更丰富的3D-2D对应点。这一设计减少了对稠密推断和过多关键帧的依赖。

其核心洞察在于**混合架构**：仅对关键帧使用前馈深度估计模型（如MASt3R）生成局部3D点，结合稀疏关键点跟踪实现实时定位，并利用锚点机制构建半稠密地图。深度推断在并行线程中按需触发，而非逐帧执行。

在 **TUM RGB-D** 和 **7-Scenes** 数据集上，SLAM-MER 平均 ATE 分别达到 **0.056 m** 和 **0.059 m**，帧率高达 **86.6 FPS** 和 **103.2 FPS**，效率远超 MASt3R-SLAM 和 VGGT-SLAM（在同一硬件上公平比较）。在 7-Scenes 的 office 序列上，系统运行速度达到 **100 FPS**，并生成半稠密地图。稠密重建方面，7-Scenes 上的 RMSE 为 **0.034 m**，相比最佳基线 VGGT-SLAM（0.052 m）降低 **34.6%**。

SLAM-MER 以模块化 C++ 框架实现，定位、图优化、回环闭合、深度推断和重定位模块可灵活替换，为未标定单目SLAM提供了一种高效、可扩展的新范式。

### 单目SLAM的效率瓶颈：从稠密推断到关键帧膨胀

视觉SLAM在机器人、增强现实和自动驾驶等领域扮演着基础性角色。近年来，基于深度学习的稠密方法（如 **MASt3R-SLAM** (Murai et al., CVPR 2025) 和 **VGGT-SLAM** (Maggio et al., NeurIPS 2025)）在定位精度上取得了显著进展，但其每帧均需执行深度推断的计算范式带来了沉重的算力负担，难以在未标定条件下实现实时运行。与此同时，传统稀疏方法（如 **ORB-SLAM3**）虽然效率较高，却缺乏对场景的显式时空连续性建模——3D点的检索仅依赖共视图，导致在视点变化时需要创建大量关键帧来维持跟踪，造成地图规模膨胀。

**核心矛盾在于**：现有系统要么牺牲效率换取精度（稠密推断），要么牺牲时空连贯性换取速度（稀疏跟踪），缺少一种能同时兼顾两者的中间方案。

### 时空建模的缺失与混合设计的契机

问题的症结可归结为两个层面。在**时间维度**上，传统系统仅依赖最新关键帧的2D关键点跟踪，丢失了短期时序信息，导致帧间对应点稀疏、跟踪脆弱。在**空间维度**上，缺乏高效的3D空间索引机制，无法根据当前相机位姿快速检索附近的地图点，使得定位过度依赖关键帧的覆盖密度。

本文的动机正是填补这一空白：通过引入**时空联合的3D点查询机制**，为每帧提供更丰富的3D-2D对应点，从而减少对稠密推断和过多关键帧的依赖。在此基础上，采用**混合设计**——仅对关键帧使用前馈深度估计模型（如MASt3R）生成局部3D点，结合稀疏关键点跟踪实现实时定位，并利用锚点机制构建半稠密地图。这一设计有望将帧率提升至80 FPS以上，同时保持或提高定位精度，为未标定单目SLAM提供一种新的效率-精度平衡范式。

## 核心方法与创新机理

SLAM-MER 的核心创新在于通过**时空联合的 3D 点查询机制**，重构了未标定单目 SLAM 中定位与建图的效率-精度平衡。相比于现有方法，其关键改进体现在四个维度：

### 1. 深度推断频率解耦

现有稠密 SLAM 方法——如 **MASt3R-SLAM**（Murai et al., CVPR 2025）和 **VGGT-SLAM**（Maggio et al., NeurIPS 2025）——对每帧图像均执行前馈深度模型推断，这成为实时性的主要瓶颈。SLAM-MER 的策略是：**仅在关键帧创建时，于并行线程中触发深度推断**。这一设计将昂贵的深度计算从定位主循环中剥离，使每帧定位仅依赖稀疏 2D 关键点提取与 3D-2D 匹配，从而将帧率提升至 80 FPS 以上。

### 2. 时序缓冲区延长跟踪窗口

传统稀疏 SLAM（如 ORB-SLAM3）主要依赖最新关键帧的共视图进行匹配，缺乏短期时序连续性。SLAM-MER 维护一个包含最近 $N$ 帧的时序缓冲区 $\mathcal{B}$，这些帧在定位时与地图建立连接，其对应的 3D 地图点被保留并用于后续帧的查询。这使得每帧可获得的 3D-2D 对应点数量显著增加，减少了对过多关键帧的依赖。消融实验（Table 2）表明，缓冲区大小 $|\mathcal{B}|=100$ 实现了最佳的精度-效率平衡。

### 3. 基于 3D 单元网格的空间查询

SLAM-MER 在地图中维护 3D 单元集合 $\mathcal{C}$，每个单元存储其包含的地图点。定位时，利用上一帧的位姿进行光栅化，筛选出可见的 3D 单元，并按距离排序后从中获取候选地图点。最终查询集为时序查询与空间查询的并集：

$$\mathcal{Q}_{3D} = \mathcal{Q}_{T} \cup \mathcal{Q}_{S}$$

这种显式的空间索引机制避免了遍历整个地图的开销，同时保证即使在新视角下也能获取足够的匹配点。消融实验中，单元大小 $|\mathcal{C}|=32$ cm 被验证为效率最优配置。

### 4. 自适应位姿求解器切换

未标定场景下，需同时估计焦距与位姿。SLAM-MER 采用一种自适应策略：**初期使用 P4Pf 求解器估计焦距，处理一定帧数后，取历史焦距估计值的中位数作为固定焦距，切换至更快的 P3P 求解器**。这一设计在不牺牲精度的前提下，进一步降低了每帧定位的计算成本。

### 混合设计的内核逻辑

上述四个 changed slots 共同支撑了一种**混合架构**：稀疏 3D 点用于实时定位，前馈深度模型仅在关键帧处介入以生成局部 3D 点并构建半稠密地图。这种设计使得 SLAM-MER 在 TUM RGB-D 和 7-Scenes 数据集上分别达到 86.6 FPS 和 103.2 FPS 的帧率，同时将平均 ATE 控制在 0.056 m 和 0.059 m，效率远超 MASt3R-SLAM 和 VGGT-SLAM（Table 1）。在 7-Scenes 的 office 序列上，帧率可达 100 FPS（Figure 1），充分验证了时空联合查询机制在实时性上的优势。

SLAM-MER 是一个面向**未标定单目实时 SLAM** 的模块化 C++ 框架，其核心设计理念是“混合式”架构：将稀疏 3D 点用于实时定位，同时借助前馈深度估计模型为关键帧生成几何先验，并在后处理阶段通过锚点机制构建半稠密地图。该设计使得系统在保持或超越现有方法定位精度的同时，将帧率推至 80 FPS 以上，在 7-Scenes 的 office 序列上可达 100 FPS（Figure 1）。

![[assets/figures/papers/paper_list_l42_https_openaccess_thecvf_com_content_CVPR2026_html_Piedade_Revisiting_Mon/figures/001_Figure_1.jpg]]
*Figure 1: We propose a new pipeline for uncalibrated monocular SLAM, called SLAM-MER. Our pipeline uses a hybrid approach that combines sparse 3D points for real-time localization with feed-forward models for computing geometric priors. This figure shows our spatial modeling of the scene for the office sequence of 7-Scenes [49]. Over the semi-dense 3D reconstructed map, we show a cell-grid representation of the scene, where the red cells indicate those selected when spatially querying 3D points. For this sequence, our method runs at 100 FPS*

### 系统架构与模块关系

SLAM-MER 的流水线由五个核心模块协同构成，其整体架构如 Figure 2 所示：

![[assets/figures/papers/paper_list_l42_https_openaccess_thecvf_com_content_CVPR2026_html_Piedade_Revisiting_Mon/figures/002_Figure_2.jpg]]
*Figure 2: Our SLAM-MER pipeline. New frames are localized based on two-way correspondences between 2D image keypoints and 3D map-points from the current map estimate: (1) temporal ones from previous frames and (2) spatial ones directly from the map via 3D cells. When a keyframe is created, 3D map-points are obtained from monocular depth inference using, e.g., MASt3R [42]. Each new keyframe and its 3D map-points add constraints to the covisibility graph, which is updated from the incremental solver in ISAM2 [24]. To correct drift in the trajectory, we have a loop closure functionality that only adds new constraints to the covisibility graph when a loop is detected, but does not perform any optimizatio...*

1. **定位模块（Localization Module）**：负责每帧的实时相机位姿估计。该模块首先提取 2D 关键点，随后通过时空联合查询机制获取 3D-2D 对应点，最终利用 P4Pf/P3P 自适应求解器估计绝对位姿。该模块是整个系统实时性的关键保障。

2. **调整模块（Adjustment Module）**：基于 ISAM2 求解器增量更新共视图中的关键帧位姿和 3D 地图点。该模块在并行线程中运行，持续监控共视图的结构变化，每当新关键帧或回环约束加入时触发增量优化。

3. **回环闭合模块（Loop Closure Module）**：采用先进的图像检索技术 MegaLoc 进行回环检测，经几何验证后向共视图添加回环约束。值得注意的是，该模块本身不执行全局优化——位姿修正由调整模块在下一次增量更新中自然完成。

4. **深度推断模块（Depth Inference Module）**：仅在关键帧创建时在并行线程中调用前馈深度估计模型（默认使用 MASt3R），生成局部 3D 点云并估计尺度因子。这一“按需推断”策略是 SLAM-MER 实现高帧率的核心决策——与 MASt3R-SLAM 和 VGGT-SLAM 等每帧均执行深度推断的方法形成鲜明对比。

5. **重定位模块（Relocalization Module）**：当定位模块的时序缓冲区中无任何帧具有有效参考关键帧时触发，借助图像检索和位姿验证恢复定位。

### 数据流与关键设计决策

系统维护一个统一的地图表示 $\mathcal{M} = (K, \mathcal{P}^{w}, \mathcal{C})$，其中 $K$ 为关键帧集合，$\mathcal{P}^{w}$ 为世界坐标系下的 3D 地图点集合，$\mathcal{C}$ 为 3D 单元网格集合。各模块通过共视图 $\mathcal{G} = (\{\mathcal{K} \cup \mathcal{P}^{w}\}, \{\mathcal{E}_{KK} \cup \mathcal{E}_{KP}\})$ 进行状态同步。

**时空联合查询**是定位模块的核心创新。对于每一帧，系统从两个来源获取 3D-2D 对应点：
- **时序查询 $\mathcal{Q}_T$**：从最近 $N$ 帧的时序缓冲区中提取与当前帧关键点匹配的地图点；
- **空间查询 $\mathcal{Q}_S$**：利用上一帧的位姿，通过光栅化筛选可见的 3D 单元网格，获取附近的地图点。

最终的查询集为二者的并集 $\mathcal{Q}_{3D} = \mathcal{Q}_T \cup \mathcal{Q}_S$。这种设计有效延长了跟踪窗口，减少了对过多关键帧和稠密推断的依赖。

**自适应位姿求解器**进一步优化了效率。系统初期使用 P4Pf 估计焦距，当累积足够帧数后，将焦距固定为历史估计值的中位数，并切换到更快的 P3P 求解器。这一策略在保持未标定条件下定位精度的同时显著降低了计算开销。

**关键帧创建**基于 KL 散度判据：计算当前帧与前一帧中关键点直方图的 KL 散度 $D_{KL}(\mathbf{H}_k || \mathbf{H}_{k-1})$，当视点变化超过阈值时创建新关键帧。新关键帧触发深度推断模块生成 3D 地图点，并将其与关键帧一同加入共视图，由调整模块异步优化。

**半稠密地图构建**在后处理阶段完成：以稀疏地图点为锚点，从深度推断产生的稠密点云中采样邻近点，形成可视化效果更好的半稠密重建结果（Figure 5）。

> **注意**：SLAM-MER 的框架设计强调模块可替换性——深度估计器、视觉地点识别（VPR）、特征检测器等均可灵活替换，具体示例见补充材料。

### 3.1 地图表示与共视图结构

SLAM-MER 将环境建模为一个三元组地图：

$$\mathcal{M} = (K, \mathcal{P}^{w}, \mathcal{C})$$

其中 $K$ 为关键帧集合，$\mathcal{P}^{w}$ 为世界坐标系下的 3D 地图点集合，$\mathcal{C}$ 为 3D 单元网格集合。这一表示是系统实时定位与增量建图的基础数据结构。3D 单元网格 $\mathcal{C}$ 是空间查询机制的核心载体，它将场景空间离散化为固定大小的体素单元，每个单元存储其内部的地图点索引。

在此地图之上，系统维护一个共视图（covisibility graph）：

$$\mathcal{G} = (\{\mathcal{K} \cup \mathcal{P}^{w}\}, \{\mathcal{E}_{KK} \cup \mathcal{E}_{KP}\})$$

该图的节点包含所有关键帧和 3D 地图点；边分为两类：$\mathcal{E}_{KK}$ 表示关键帧之间的共视关系，$\mathcal{E}_{KP}$ 表示关键帧与其观测到的地图点之间的连接。共视图是调整模块（Adjustment Module）进行增量图优化的拓扑基础——当新关键帧创建时，其与地图点的观测约束被添加到图中，由 ISAM2 求解器持续更新关键帧位姿和地图点位置。

### 3.2 时空联合的 3D 点查询机制

定位模块的核心创新在于从地图中高效检索当前帧所需的 3D-2D 对应点。查询集由两部分并集构成：

$$\mathcal{Q}_{3D} = \mathcal{Q}_{T} \cup \mathcal{Q}_{S}$$

**时序查询 $\mathcal{Q}_{T}$**：系统维护一个包含最近 $N$ 帧的时序缓冲区 $B$，保留这些帧与地图关键帧的 2D 关键点跟踪连接。当新帧到达时，通过光流跟踪将缓冲区中帧的 2D 关键点传播到当前帧，从而间接获取其关联的 3D 地图点。这一机制将有效跟踪窗口延长至 $N$ 帧，弥补了仅依赖最新关键帧时短期对应点不足的缺陷。

**空间查询 $\mathcal{Q}_{S}$**：利用上一帧的估计位姿 $\mathbf{T}_k$，通过光栅化确定当前相机视锥内可见的 3D 单元。系统异步地按单元中心到相机光心的距离对可见单元排序，优先选取最近邻的单元，从中提取存储的地图点。这一机制直接利用地图的 3D 空间结构，无需依赖共视图的间接索引，大幅提升检索效率。

### 3.3 自适应位姿估计与焦距处理

在未标定单目设定下，系统使用 P4Pf 求解器在 RANSAC 框架中同时估计相机位姿和焦距。为提升效率，系统采用自适应切换策略：在处理一定数量帧后，将焦距固定为历史所有估计值的中位数，随后切换至更快的 P3P 求解器仅估计位姿。这一设计在保证未标定初始化灵活性的同时，将稳态运行的计算开销降至最低。

### 3.4 基于 KL 散度的关键帧决策

关键帧的创建时机通过当前帧与前驱关键帧之间关键点分布直方图的 KL 散度判定：

$$D_{KL}(\mathbf{H}_k || \mathbf{H}_{k-1})$$

直方图 $\mathbf{H}_k$ 统计当前帧中跟踪到的 2D 关键点分别来自哪些历史关键帧。当相机观察到场景的新区域时，直方图会向右倾斜——因为只有最近的关键帧与当前帧共享匹配点，而较早的关键帧不再有贡献。KL 散度超过预设阈值即触发新关键帧的创建。这一判据直接响应视点变化，避免了固定帧间隔策略在缓慢运动时产生冗余关键帧的问题。

## 实验与关键发现

SLAM-MER 在定位精度与运行效率两个维度上均展现出显著优势，其核心实验结论可概括为：**以稀疏特征实现实时定位，在帧率远超稠密基线的前提下，达到甚至超越后者的轨迹精度**。

**主实验结果（定位精度与效率）**

Table 1 汇总了在 TUM RGB-D 和 7-Scenes 两个标准数据集上的相机位姿估计结果。在未标定单目设定下，SLAM-MER 在两个数据集上的平均 ATE 分别为 **0.056 m** 和 **0.059 m**，帧率分别达到 **86.6 FPS** 和 **103.2 FPS**。这一速度优势在与同为未标定方案的 **MASt3R-SLAM**（Murai et al., CVPR 2025）和 **VGGT-SLAM**（Maggio et al., NeurIPS 2025）的对比中尤为突出——后两者需对每一帧执行深度推断，计算开销极大。为公平比较，作者在同一硬件（Intel Core i9-14900K + NVIDIA GeForce RTX 4090）上测量了这些基线的运行速度，SLAM-MER 的效率领先幅度达到数量级差异。

![[assets/figures/papers/paper_list_l42_https_openaccess_thecvf_com_content_CVPR2026_html_Piedade_Revisiting_Mon/figures/006_Table_1.jpg]]
*Table 1: Camera pose estimation results on TUM RGB-D and 7-Scenes datasets. Baseline Absolute Trajectory Error (ATE) (m) values are taken from [37]. For a fair FPS comparison with MASt3R-SLAM and VGGT-SLAM, we report their runtime measured on our machine. “Sparse Loc.” indicates the use of sparse features for localization, “Dense map” denotes methods producing denser point clouds, and “Uncalib.” specifies methods handling uncalibrated SLAM. The best and second-best results are highlighted separately for calibrated (in gray) and uncalibrated settings*

在标定设定下，SLAM-MER 同样具备竞争力：与经典的稀疏特征点系统 **ORB-SLAM3** 以及基于稠密光流的 **DROID-SLAM**（Teed & Deng, NeurIPS 2021）相比，SLAM-MER 在保持高帧率的同时，ATE 指标处于同一水平或更优。值得注意的是，SLAM-MER 的“稀疏定位”属性使其关键帧数量远少于稠密方法，这直接压缩了后端优化和深度推断的计算负担。

**稠密重建精度**

Table 3 报告了 7-Scenes 数据集上的稠密重建 RMSE。SLAM-MER 取得了 **0.034 m** 的平均 RMSE，较最佳基线 VGGT-SLAM 的 0.052 m 降低了 **34.6%**。这一结果说明，即便深度推断仅在关键帧上执行，通过锚点机制（anchor-point–based densification）仍能构建出高质量的半稠密地图。Figure 5 以 TUM 的 room 序列为例，对比了用于定位的稀疏 3D 地图点（左）与以这些点为锚点稠密化后的场景表示（右），直观展示了混合表示的有效性。

![[assets/figures/papers/paper_list_l42_https_openaccess_thecvf_com_content_CVPR2026_html_Piedade_Revisiting_Mon/figures/005_Figure_5.jpg]]
*Figure 5: Reconstructed scene for the room sequence of TUM [50]. The left side of the figure shows the sparse 3D map-points used for localization. The right side displays the densified representation of the scene using the sparse mappoints as anchors*

![[assets/figures/papers/paper_list_l42_https_openaccess_thecvf_com_content_CVPR2026_html_Piedade_Revisiting_Mon/figures/007_Table_3.jpg]]
*Table 3: RMSE (m) dense reconstruction results on 7-Scenes [49]. Baseline values were taken from [37]. “@n” indicates a keyframe every n frames. Best and second-best results are highlighted*

**消融实验：时序缓冲与空间查询的贡献**

Table 2 的消融实验量化了两个核心设计选择的影响：
- **时序缓冲区大小 |B|**：当 |B| = 100 时，系统在 ATE 与关键帧数量之间取得最佳平衡。过小的缓冲区会削弱时序连续性，导致更多关键帧被创建以弥补跟踪质量下降；过大的缓冲区则引入冗余信息，对精度增益有限。
- **空间单元网格大小 |C|**：设定为 32 cm 以兼顾查询效率与覆盖充分性。空间查询机制（Figure 3）通过光栅化筛选当前位姿下的可见 3D 单元，并按距离排序，为每帧提供额外的 3D-2D 对应点，减少了对过多关键帧的依赖。

![[assets/figures/papers/paper_list_l42_https_openaccess_thecvf_com_content_CVPR2026_html_Piedade_Revisiting_Mon/figures/008_Table_2.jpg]]
*Table 2: Ablation study on the temporal buffer size |B| and spatial query of 3D points (cell size |C|). We measure ATE (m), number of keyframes (|K|), number of 3D map-points*

**失败模式与局限性**

分析中明确指出的失效场景包括：
1. **大漂移下的空间查询失效**：当轨迹漂移过大时，基于当前位姿的光栅化可能无法命中正确的 3D 单元，此时空间查询贡献归零，系统需依赖回环闭合模块（基于 MegaLoc 图像检索）来恢复正确位姿。
2. **深度估计泛化瓶颈**：半稠密地图的质量受限于所集成的前馈模型（默认采用 MASt3R）。在域外场景（未见过的环境类型）上，深度估计误差会通过锚点机制传播到地图中。
3. **未验证的长序列鲁棒性**：当前实验集中在室内中小规模数据集（TUM RGB-D、7-Scenes），系统在大规模室外长序列上的尺度漂移和鲁棒性尚缺乏实证。

**关键图表结论速览**

| 图表 | 核心结论 |
|------|----------|
| Table 1 | 未标定单目设定下，ATE 0.056/0.059 m，帧率 86.6/103.2 FPS，效率远超 MASt3R-SLAM 和 VGGT-SLAM |
| Table 2 | |B|=100、|C|=32 cm 为精度-效率最优配置 |
| Table 3 | 稠密重建 RMSE 0.034 m，较 VGGT-SLAM 降低 34.6% |
| Figure 1 | office 序列达 100 FPS，红色单元展示空间查询的可视化效果 |
| Figure 5 | 稀疏定位点与锚点半稠密地图的对比，验证混合表示的有效性 |

## 定位与知识库关联

### 1. 方法谱系：从稀疏特征点到混合时空建模

SLAM-MER 处于**经典几何 SLAM 与数据驱动稠密 SLAM 的交汇点**，其设计哲学可追溯至两条主线：

**稀疏特征点 SLAM 谱系。** 以 **ORB-SLAM3** 为代表的传统方法依赖手工特征提取与共视图优化，在标定条件下能实现稳健定位，但面临关键帧膨胀和未标定场景适应性不足的问题。SLAM-MER 继承了稀疏特征点跟踪与增量图优化的核心框架（基于 ISAM2 的 Adjustment Module），但通过两个关键改造突破了传统范式的瓶颈：(1) 引入时空联合的 3D 点查询机制，将跟踪窗口从单一关键帧扩展到时序缓冲区与空间单元网格的并集 $\mathcal{Q}_{3D} = \mathcal{Q}_{T} \cup \mathcal{Q}_{S}$；(2) 将深度推断从每帧必做改为仅在关键帧创建时并行执行，从根本上解耦了定位频率与稠密推断的算力耦合。

**稠密/半稠密深度 SLAM 谱系。** 近年来，**DROID-SLAM** (Teed & Deng, NeurIPS 2021) 通过稠密光流与 BA 层实现了高精度定位，但计算代价高昂；**DPV-SLAM++** (Lipson et al., ECCV 2024) 以深度补丁匹配提升稀疏方法的鲁棒性；**MASt3R-SLAM** (Murai et al., CVPR 2025) 和 **VGGT-SLAM** (Maggio et al., NeurIPS 2025) 则直接利用前馈模型（MASt3R/VGGT）逐帧推断深度与位姿，精度突出但帧率受限于模型推理开销。SLAM-MER 的独特定位在于：**仅将前馈模型作为关键帧的几何先验注入器，而非逐帧定位的依赖项**。这种“稀疏定位 + 按需稠密化”的混合策略使其在保持与 MASt3R-SLAM/VGGT-SLAM 可比甚至更优定位精度的同时，帧率提升一个数量级（86.6–103.2 FPS vs. 前述方法的个位数 FPS，Table 1）。

### 2. 核心差异槽位与因果机制

SLAM-MER 相对于上述基线的关键设计差异可归纳为四个“槽位”：

| 设计槽位 | 基线策略 | SLAM-MER 策略 | 因果效应 |
|:---|:---|:---|:---|
| **深度推断频率** | 每帧执行（MASt3R-SLAM, VGGT-SLAM） | 仅关键帧创建时并行执行 | 消除逐帧模型推理瓶颈，帧率提升 10× 以上 |
| **时序 3D 点查询** | 仅依赖最新关键帧的 2D 跟踪 | 维护最近 N 帧的时序缓冲区，保留与关键帧的 3D-2D 连接 | 延长有效跟踪窗口，减少因短期遮挡或快速运动导致的跟踪丢失 |
| **空间 3D 点查询** | 无显式空间索引，依赖共视图遍历 | 基于 3D 单元网格的光栅化空间查询 | 将 3D 点检索复杂度从图遍历降为常数级单元查找，支撑高帧率下的实时定位 |
| **位姿求解器** | 固定 P3P（标定）或 P4Pf（未标定） | 自适应切换：P4Pf 估计焦距 → 取历史中值固定 → 切换 P3P | 兼顾未标定初始化灵活性与稳态运行效率 |

这些设计的**因果传导链**为：时空查询增加了每帧可用的 3D-2D 对应点数量 → 提高了位姿估计的冗余度和鲁棒性 → 降低了对稠密深度推断和过多关键帧的依赖 → 关键帧数量减少（Table 2 消融显示关键帧数 |K| 随缓冲区增大而下降）→ 深度推断总次数减少 → 整体帧率突破 80 FPS。

### 3. 知识库定位与适用边界

**方法归属。** SLAM-MER 属于**未标定单目视觉 SLAM** 中的**混合稀疏-半稠密方法**。其知识贡献不在于提出全新的深度估计器或位姿求解器，而在于**系统架构层面的创新**——通过时空查询机制和按需深度推断策略，重新分配了定位、建图与深度推断之间的算力预算，证明了“稀疏定位 + 前馈先验 + 锚点稠密化”这一组合在效率-精度 Pareto 前沿上的竞争力。

**适用边界。** 基于论文提供的实验证据与局限声明，SLAM-MER 的适用边界可归纳如下：

- **强适用场景：** 室内中小规模环境（如 7-Scenes、TUM RGB-D 规模的房间/办公场景），需要高帧率实时定位且可接受半稠密地图质量。未标定单目设置下表现尤为突出。
- **边界条件：** 当轨迹漂移过大时，空间查询的光栅化可能失效（可见单元判断依赖当前位姿估计），此时需依赖回环闭合模块纠正——这意味着在缺乏回环的长走廊或重复纹理场景中，系统可能退化。
- **已知局限：**
  1. 深度估计精度受限于所集成的前馈模型（论文使用 MASt3R），在未见过的场景分布上泛化能力有限；
  2. 未在大规模室外长序列（如 KITTI、EuRoC 室外部分）上验证鲁棒性和尺度漂移问题；
  3. 回环闭合仅向共视图添加约束而不执行独立优化，依赖 ISAM2 的增量更新来吸收回环信息——这可能在大回环场景下导致收敛速度较慢。

### 4. 开放问题与后续方向

1. **开源与可复现性。** 论文声称 SLAM-MER 是模块化 C++ 框架，支持灵活替换深度估计器、VPR 和特征检测器，但未明确是否开源。这对社区验证和后续改进至关重要。
2. **位姿表示的改进空间。** VGGT-SLAM 采用的 SL(4) 流形位姿表示在回环闭合后展现出更好的全局一致性。SLAM-MER 能否集成此类表示以进一步提升大回环后的优化效果，是一个自然的研究延伸。
3. **深度估计器的升级路径。** 论文在消融中展示了替换深度估计器的可行性（如用 VGGT 替代 MASt3R），但未系统评估不同前馈模型对定位精度的影响。更强的未标定深度估计器能否在不牺牲帧率的前提下缩小与标定方法的精度差距，值得探索。
4. **室外大规模验证。** 当前实验局限于室内数据集，室外长序列下的尺度漂移、光照变化和动态物体对时空查询机制的冲击尚未评估——这是从“室内实时 SLAM”走向“通用实时 SLAM”必须跨越的验证鸿沟。

## 原文 PDF

![[paperPDFs/CVPR_2026/Revisiting_Monocular_SLAM_with_Spatio_Temporal_Scene_Modeling.pdf]]
