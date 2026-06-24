---
title: "From Sparse to Dense: Spatio-Temporal Fusion for Multi-View 3D Human Pose Estimation with DenseWarper"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/From_Sparse_to_Dense_Spatio_Temporal_Fusion_for_Multi_View_3D_Human_Pose_Estimation_with_DenseWarper.pdf
openreview_forum_id: MLs6ThXmcz
aliases:
- From_Sparse_to_D
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "稀疏交错输入范式与对极几何时空融合模块共同作用，在保持空间精度的同时将输出帧率提升至N倍，并降低计算冗余。"
primary_logic: "通过多视图交错采样实现时空信息的协同融合，利用对极几何约束进行跨视图热图校正，并借助可变形卷积学习时间一致性，将稀疏输入转化为密集高精度输出。"
claims:
- "提出稀疏交错输入范式，仅使用每个视图中单个时间步的图像，即可达到优于传统密集输入的3D姿态估计性能"
- "DenseWarper通过时空融合模块有效纠正稀疏输入中缺失的空间和时间信息，消融实验验证了两个模块的独立作用"
- "该方法在Human3.6M和MPI-INF-3DHP数据集上均取得state-of-the-art结果，且模型效率优于同类方法"
- "Human3.6M (GT 2D) 上 MPJPE (mm) = 21.3"
---

# From Sparse to Dense: Spatio-Temporal Fusion for Multi-View 3D Human Pose Estimation with DenseWarper

> [!tip] 核心洞察
> 通过多视图交错采样实现时空信息的协同融合，利用对极几何约束进行跨视图热图校正，并借助可变形卷积学习时间一致性，将稀疏输入转化为密集高精度输出。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从稀疏到密集：面向多视图3D人体姿态估计的时空融合方法DenseWarper |
| 英文题名 | From Sparse to Dense: Spatio-Temporal Fusion for Multi-View 3D Human Pose Estimation with DenseWarper |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=MLs6ThXmcz); [GitHub](https://github.com/lingli1724/DenseWarper-ICLR2026) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | DenseWarper |
| Dataset | Human3.6M (GT 2D), Human3.6M (CPN 2D), Human3.6M (SimpleBaseline), MPI-INF-3DHP (SimpleBaseline) |

> [!tip] 效果简介
> - Human3.6M (GT 2D) 上，MPJPE (mm) 为 21.3，对比 23.7 (Adafuse Full)，变化 -2.4。
> - Human3.6M (CPN 2D) 上，MPJPE (mm) 为 33.6，对比 35.8 (Adafuse Full)，变化 -2.2。
> - Human3.6M (SimpleBaseline) 上，P-MPJPE (mm) 为 19.4，对比 20.7 (Adafuse Full)，变化 -1.3。

## 概述

多视图3D人体姿态估计长期依赖**同步密集输入**——每个时间步所有相机同时采集图像，经2D姿态检测、空间融合与三角测量获得3D骨架。这一范式存在三个关键瓶颈：**计算冗余**（所有视图全帧处理）、**时间信息利用不充分**（逐帧独立推理）、**输出帧率受限于单相机帧率**。传统提升帧率的方法依赖关键点插值（如MCC、SLERP），仅在3D骨架层面做线性平滑，无法引入新的空间信息，精度上限受制于原始输入质量。

DenseWarper（ICLR 2026）提出了一种根本性的范式转换：**稀疏交错输入**。其核心思想是让各相机在不同时间步交错采样——例如4相机系统在时间步 $t_1$ 仅相机1采集，$t_2$ 仅相机2采集，以此类推——使得每个时间步都能获得来自某一视图的真实空间信息，同时输出帧率提升至单相机帧率的 $M$ 倍（$M$ 为视角数）。这一范式的可行性建立在两个因果机制上：（1）**对极几何空间融合**：利用多视图间的对极约束，沿对极线搜索其他视图的最大响应来校正当前视图的热图，将稀疏的空间信息扩散为密集的跨视图一致表示；（2）**可变形卷积时序融合（Warper）**：计算空间校正热图与原始稀疏热图之间的差异作为运动特征，通过多尺度扩张卷积预测像素级偏移，对齐并聚合多帧热图以恢复时间一致性。

**核心结论**：在Human3.6M数据集上，DenseWarper以稀疏输入（仅使用每视图单帧）达到21.3 mm MPJPE，优于传统密集全帧输入的Adafuse（23.7 mm）；在MPI-INF-3DHP上达到65.89 mm，超越此前最优方法KTP-Former（67.59 mm）。消融实验表明，空间融合模块使MPJPE从36.06 mm降至31.54 mm，进一步添加Warper模块降至22.28 mm，相对纯复制基线提升38.2%。模型参数量76.51M，单次推理延迟44.51ms，在精度-效率权衡上优于同类多视图方法。

**方法定位**：DenseWarper属于多视图3D姿态估计中的**时空融合**路线，区别于全帧方法（Adafuse, Zhang et al., 2021；PPT, Ma et al., 2022；Sgraformer, Zhang et al., 2024）和插值方法（Adafuse+MCC/Adafuse+SLERP）。其独特贡献在于将输入范式从“空间密集、时间稀疏”反转为“空间稀疏、时间密集”，通过对极几何与可变形卷积实现跨时空的信息补偿，为多视图感知任务提供了“以时间换空间”的新思路。

**局限与开放问题**：方法依赖已知相机参数和较高相机帧率（≥50fps）；当时序间隔显著增大或出现非均匀间隔时性能下降（最大非均匀间隔12帧时MPJPE升至31.58 mm）。该范式能否推广至其他多视图3D任务（物体检测、场景重建）、如何在部分视图失效或严重遮挡下保持鲁棒性、以及能否集成自适应采样策略，仍有待探索。

## 背景与动机

多视图3D人体姿态估计（3D HPE）是计算机视觉领域的核心任务，其目标是从多个同步相机捕获的图像中恢复精确的3D关节点位置。传统方法遵循一个基本假设：**所有相机必须在每个时间步同步采集密集图像**，然后通过三角测量或体积重建获得3D姿态。这一范式虽然在Human3.6M和MPI-INF-3DHP等基准上取得了显著进展，但存在三个深层瓶颈：

**瓶颈一：计算冗余**。密集多视图输入要求每帧处理$M$个视图的全部图像，计算量随视图数线性增长。当相机帧率较高时，相邻帧间的信息高度冗余，但现有方法仍需对每帧执行完整的2D姿态估计和3D重建流程，造成算力浪费。

**瓶颈二：时间信息利用不充分**。传统方法将各时间步视为独立样本，缺乏跨帧的时序建模能力。即便部分工作尝试引入时序融合，也仅在后处理阶段对3D关键点进行插值或平滑，未能从根本上利用多视图间的时间互补性。如Figure 1所示，全帧密集输入（b）和关键点插值输入（c）均未改变“空间同步、时间独立”的底层逻辑。

**瓶颈三：输出帧率受限于单相机帧率**。在密集输入范式下，系统的输出帧率上限等于单个相机的采集帧率$f$。尽管多相机系统在物理上具备更高的时间采样潜力——$M$个相机理论上可提供$M \times f$的时间分辨率——但现有方法无法释放这一潜能。

**现有方法的缺口**。近期的多视图3D HPE工作可分为三类：单视图方法（如**GLA-GCN** (Yu et al., 2023b)、**KTP-Former** (Peng et al., 2024)、**FinePose** (Xu et al., 2024a)）仅利用单一视角，精度受限；多视图全帧方法（如**Adafuse** (Zhang et al., 2021)、**PPT** (Ma et al., 2022)、**Sgraformer** (Zhang et al., 2024)）虽精度较高，但继承了密集输入的计算冗余；关键点插值方法（如**Adafuse+MCC** (Su et al., 2021)、**Adafuse+SLERP** (Chen et al., 2022)）试图提升输出帧率，却依赖线性或球面插值等简单策略，无法恢复复杂运动中的非线性姿态变化。

**本文动机**。针对上述瓶颈，本文提出一个根本性的范式转换：**稀疏交错输入**（Sparse Interleaved Input）。核心思想是打破“空间同步”的约束，让每个视图在不同时间步交错采样，从而将时空信息分散到多个视图中。通过设计专门的时空融合模块，从这些稀疏交错信号中恢复密集、高精度的3D姿态序列，同时将输出帧率提升至$M \times f$。这一范式不仅降低了单帧计算量，更首次将多视图系统的时间分辨率潜力转化为实际性能增益。

## 核心创新

DenseWarper 的核心创新在于用**稀疏交错输入范式**替代传统同步密集多视图输入，并通过**对极几何空间融合**与**可变形时序融合**两个模块，将稀疏输入转化为密集高精度输出，从而同时解决计算冗余、时间信息利用不足和单相机帧率受限三个瓶颈。

### 创新一：稀疏交错输入范式

传统多视图3D人体姿态估计要求所有相机在每一时间步同步采集图像（Figure 1b），导致计算量与视图数线性增长，且输出帧率受限于单相机帧率。DenseWarper 提出稀疏交错采样策略：对于 $M$ 个视角、$N$ 帧总长的序列，仅从每个视角选取一个时间交错帧构成输入组：

$${\bf D} = \{ {\bf I}_i \}_{i=1}^{\lfloor \frac{N}{M} \rfloor}$$

其中第 $i$ 组输入为 ${\bf I}_i = \{ I_{V_1}^{M \cdot (i-1)+1}, I_{V_2}^{M \cdot (i-1)+2}, \dots, I_{V_M}^{M \cdot i} \}$，各视角在不同时间步采样形成对角式激活模式（Figure 1a）。这一范式带来的关键优势是：在保持每个视角仅贡献单帧的条件下，通过多视图时空信息的协同融合，输出帧率可达单相机帧率的 $M$ 倍（Figure 8），同时大幅降低计算冗余。

**证据强度**：Table 1 显示，在 Human3.6M 数据集上，DenseWarper 使用稀疏输入（Ours Sparse）在 GT 2D 条件下达到 21.3 mm MPJPE，优于使用全帧密集输入的 Adafuse Full（23.7 mm）。这表明稀疏范式不仅未损失精度，反而因时空融合机制获得了更优性能。

### 创新二：对极几何空间融合模块

稀疏交错输入导致各视角在目标时刻缺失真实观测，直接复制相邻帧热图会引入空间误差。DenseWarper 的对极几何空间融合模块利用多视图几何约束进行跨视图热图校正：对于当前视图 $v$ 中位置 $x$ 的响应，沿其他视图 $u$ 中对应的对极线 $\mathbf{p}^u(x)$ 搜索最大响应，并加权融合：

$$\hat{\mathbf{H}}_v^n(x) = \lambda \mathbf{H}_v^n(x) + \frac{(1-\lambda)}{M} \sum_{u=1}^M \max_{x' \in \mathbf{p}^u(x)} \mathbf{H}_u^n(x')$$

该公式的核心机制是：若某视图的热图响应因时间错位而不准确，其他视图中沿对极线的最大响应可提供空间校正信号（Figure 3）。与简单的重投影或线性插值不同，该方法显式建模了多视图间的对极约束，使校正过程具有几何可解释性。

**证据强度**：消融实验（Table 5）表明，仅添加空间融合模块即可将 Human3.6M 上 MPJPE 从 36.06 mm（纯复制基线）降至 31.54 mm，验证了对极几何校正的有效性。

### 创新三：Warper 可变形时序融合模块

空间融合后，热图仍缺乏时序一致性。Warper 模块通过可变形卷积学习像素级时序偏移，实现运动感知的热图对齐与聚合。具体流程为：首先计算空间校正热图与原始稀疏热图之间的差异 $\boldsymbol{\Phi}_{V_j}^n(\boldsymbol{x}) = \hat{\mathbf{H}}_{V_j}^n(\boldsymbol{x}) - \mathbf{H}_{V_j}^{M \cdot i + j}$，该差异编码了运动信息；随后通过堆叠的 $3 \times 3$ 残差块和五组膨胀率 $d \in \{3, 6, 12, 18, 24\}$ 的卷积层预测五组偏移量 $o_{V_j}^{(d)}(x)$，对热图进行可变形扭曲并聚合：

$$\tilde{\mathbf{H}}_{V_j}^n = \sum_{d=1}^5 \mathbf{Warper}(\boldsymbol{\Phi}_{V_j}^n, o_{V_j}^{(d)}(x))$$

多尺度膨胀卷积的设计使模块能够捕获不同速度的运动模式，而可变形卷积的偏移学习机制使其能自适应地对齐时序特征，而非依赖固定的插值策略。

**证据强度**：消融实验（Table 5）显示，在空间融合基础上添加 Warper 模块后，MPJPE 进一步降至 22.28 mm，相对于复制基线提升 38.2%。在 MPI-INF-3DHP 上，完整模型达到 65.89 mm，比无校正基线（94.46 mm）降低 30.25%。

### 与基线的关键差异总结

| 设计维度 | 传统方法（Adafuse 等） | DenseWarper |
|---------|----------------------|-------------|
| 输入范式 | 同步密集多视图图像 | 稀疏交错多视图图像 |
| 空间校正 | 无跨视图校正或简单重投影 | 对极几何约束下的热图融合 |
| 时序建模 | 无或线性插值/MCC | 可变形卷积学习像素级运动偏移 |
| 输出帧率 | 等于单相机帧率 | 可达单相机帧率的 $M$ 倍 |

**需要手动验证**：论文未在极端低帧率（如 <10 fps）或无标定条件下验证方法的泛化性，这些场景下的性能边界仍需进一步研究。

## 整体框架

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_MLs6ThXmcz/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the DenseWarper architecture. A sliding window is used to sample sparse interleaved images, with a 2D pose estimation model generating initial heatmaps for each view. Missing information is filled to create uncorrected heatmaps. These are then spatially fused and corrected using an epipolar geometry-based method, yielding a spatially fused heatmap. Deformable convolutions are then applied for temporal fusion. Finally, the resulting spatiotemporally enriched heatmap is processed via triangulation to obtain accurate 3D keypoints*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_MLs6ThXmcz/figures/001_Figure_1.jpg]]
*Figure 1: Common approaches for 3D multi-view pose estimation. (a) Our proposed sparse interleaved input, where each view selects a single temporally interleaved image as input to leverage spatio-temporal information across views fully; (b) illustration of dense, full-frame multi-view input; (c) keypoint interpolation input, which enhances the output frame rate; and (d) illustration of single-view image input*

DenseWarper 的整体架构围绕一个核心思想展开：将稀疏交错的多视图输入转化为具有高时空一致性的密集三维姿态输出。图 2 给出了完整的端到端流程。

**输入范式**。传统多视图姿态估计要求每个时间步所有相机同步采集一帧图像，形成密集的全帧输入。DenseWarper 采用稀疏交错采样策略：在 M 个视角、总帧数为 N 的视频序列中，第 i 个输入组仅包含每个视角的一帧图像，但各视角的帧索引相互交错——

$$
\mathbf{I}_i = \left\{ I_{V_1}^{M \cdot (i-1)+1}, I_{V_2}^{M \cdot (i-1)+2}, \dots, I_{V_M}^{M \cdot i} \right\}
$$

这意味着任意时刻只有单个视角贡献当前帧，其他视角提供的是相邻时间步的信息。图 1 对比了稀疏交错输入与密集全帧输入、关键点插值输入及单视图输入的差异：稀疏交错输入在保持空间多视图约束的同时，将有效输出帧率提升至相机原始帧率的 M 倍。

**滑动窗口与缓存机制**。系统采用滑动窗口遍历输入序列，一旦任一个视角完成采样即可立即处理，无需等待所有视角同步。已计算的热图被缓存复用，显著降低了冗余计算。

**核心模块链**。整体管线由四个模块串联构成：

1. **2D 姿态估计器**：对稀疏交错图像逐帧生成初始热图。此时每个视角仅拥有自身时间步的热图，其余帧的热图缺失。
2. **缺失填充**：将每视角的原始热图复制 M−1 份，填充到该视角的其他时间步位置，形成未校正的密集热图集合。此步骤为后续空间融合提供初始值。
3. **对极几何空间融合**：利用已知的相机参数和对极几何约束，沿对极线搜索其他视图中的最大响应，对复制填充的热图进行跨视图校正，消除因简单复制引入的空间误差。
4. **Warper 时序融合**：计算空间校正后热图与原始稀疏热图之间的时序差异，通过可变形卷积预测像素级偏移，对多帧热图进行扭曲对齐与聚合，生成时空增强的密集热图。

**输出**。最终将时空矫正后的热图通过三角测量（triangulation）转换为三维关键点坐标，得到高精度、高帧率的 3D 姿态序列。

整个框架的因果机制可概括为：稀疏交错采样打破了同步密集输入的帧率瓶颈 → 对极几何空间融合利用多视图几何约束补偿空间信息损失 → Warper 通过可变形时序对齐补偿时间信息损失 → 二者协同将稀疏输入“稠密化”为高时空一致性的输出。

## 核心模块与公式推导

### 3.1 稀疏交错输入范式

DenseWarper的核心创新始于输入范式的改变。传统多视图方法要求所有相机在每一帧同步采集图像，而本方法提出**稀疏交错采样**：设共有 $M$ 个视角，总帧数为 $N$，则稀疏交错多视图图像集合定义为：

$${\bf D} = \{ {\bf I}_i \}_{i=1}^{\lfloor \frac{N}{M} \rfloor}$$

其中第 $i$ 组输入 ${\bf I}_i$ 包含每个视角在交错时间步上采集的单帧图像：

$${\bf I}_i = \left\{ I_{V_1}^{M \cdot (i-1) + 1}, I_{V_2}^{M \cdot (i-1) + 2}, \dots, I_{V_M}^{M \cdot i} \right\}$$

这一设计的因果机制在于：当 $M$ 个相机以固定帧率 $f$ 独立采样时，交错排列使得等效输出帧率达到 $M \times f$，从而突破了单相机帧率的物理上限。同时，每个时间步仅需处理 $M$ 帧图像，而非传统密集方案的 $M \times N$ 帧，显著降低了计算冗余。

### 3.2 基于对极几何的空间热图融合

稀疏交错采样导致每个视角在每个输出时间步上仅有部分帧拥有真实的2D姿态热图，其余位置需要通过**复制填充**来补全。然而，直接复制会引入空间偏差——不同视角的同一关节在图像平面上的位置受相机位姿影响而不同。

该模块的核心操作是沿对极线搜索并融合其他视图的响应信息。对于待校正视图 $v$ 在位置 $x$ 处的热图值，校正公式为：

$$\hat{\mathbf{H}}_v^n(x) = \lambda \mathbf{H}_v^n(x) + \frac{(1-\lambda)}{M} \sum_{u=1}^M \max_{x' \in \mathbf{p}^u(x)} \mathbf{H}_u^n(x')$$

其中：
- $\mathbf{H}_v^n(x)$ 为视图 $v$ 在帧 $n$、位置 $x$ 处的原始热图响应；
- $\mathbf{p}^u(x)$ 表示位置 $x$ 在视图 $u$ 中的对极线；
- $\max_{x' \in \mathbf{p}^u(x)} \mathbf{H}_u^n(x')$ 沿对极线搜索最大响应值；
- $\lambda$ 为平衡原始响应与跨视图融合信息的权重参数。

该公式的因果逻辑是：若某视图的热图响应存在偏差，其他视图中对应关节的真实位置必然落在该点的对极线上。通过取对极线上的最大响应并加权融合，可以有效抑制噪声并矫正空间位置偏差。

### 3.3 Warper：基于可变形卷积的时序融合

空间融合仅矫正了跨视图的空间不一致性，但复制填充引入的时序错位问题仍未解决。Warper模块通过可变形卷积学习像素级的时序偏移，实现热图在时间维度上的对齐与聚合。

首先计算空间校正后热图与原始稀疏输入热图之间的**时序差异**：

$$\boldsymbol{\Phi}_{V_j}^n(\boldsymbol{x}) = \hat{\mathbf{H}}_{V_j}^n(\boldsymbol{x}) - \mathbf{H}_{V_j}^{M \cdot i + j}$$

该差异特征编码了目标帧与真实采样帧之间的运动信息，是后续可变形卷积的输入。

Warper的核心操作是预测多组偏移量并对热图进行可变形扭曲与聚合：

$$\tilde{\mathbf{H}}_{V_j}^n = \sum_{d=1}^5 \mathbf{Warper}(\boldsymbol{\Phi}_{V_j}^n, o_{V_j}^{(d)}(x))$$

其中：
- $o_{V_j}^{(d)}(x)$ 为第 $d$ 组预测的像素级偏移量，共5组；
- $\mathbf{Warper}(\cdot)$ 利用偏移量对热图进行空间重采样；
- 5组偏移量对应5个不同膨胀率（$d \in \{3, 6, 12, 18, 24\}$）的卷积层输出，以捕获多尺度的时序运动模式。

最终，经过空间融合和时序融合的热图通过三角测量转换为3D关键点坐标。整个框架的映射关系可表示为 $f: \mathcal{T}(\mathcal{D}, \Phi, \phi) = S$，即将稀疏交错数据 $\mathcal{D}$、模型参数 $\Phi$ 和相机参数 $\phi$ 映射为3D骨架序列 $S$。

### 3.4 滑动窗口与缓存机制

为支持实时增量处理，DenseWarper采用滑动窗口机制。任意视角完成采样后即可立即处理，通过缓存已计算的热图避免重复推理。这一设计使得系统延迟不随窗口长度线性增长，保证了实际部署中的效率。

## 实验与分析

### 主实验结果

DenseWarper在Human3.6M和MPI-INF-3DHP两个标准基准上均取得了state-of-the-art性能，且仅使用稀疏交错输入——每个视图仅需单个时间步的图像——即可超越传统密集多视图全帧方法。

**Human3.6M数据集。** 表1和表2分别报告了MPJPE和P-MPJPE指标。在GT 2D姿态设定下，DenseWarper（Sparse）达到平均MPJPE **21.3 mm**，相比Adafuse全帧基线（23.7 mm）降低2.4 mm，相对提升约10.1%。在使用CPN检测的2D姿态时，DenseWarper取得33.6 mm MPJPE，优于Adafuse全帧的35.8 mm和Adafuse稀疏输入的36.9 mm。值得注意的是，Adafuse在稀疏输入条件下性能显著退化（36.9 mm vs. 35.8 mm全帧），而DenseWarper在相同稀疏条件下反而超越全帧基线，验证了时空融合模块对缺失信息的有效补偿。在P-MPJPE指标上，DenseWarper达到平均**19.4 mm**，优于Sgraformer（19.9 mm）和Adafuse全帧（20.7 mm）。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_MLs6ThXmcz/figures/005_Table_1.jpg]]
*Table 1: MPJPE Comparison with state-of-art pose estimation methods on Human3.6M (mm) using ground-truth and detected 2Dposes. Input types: Single-view (Single), Multi-view full-frame (Full), Multi-view interpolated (Interp). Best in bold. Note: Complete version with all baseline comparisons. Gray rows highlight our method. Action abbreviations: Directions (Dir), Discussion (Disc), Sitting Down (SitD), Walking Dog (WalkD), Walking Together (WalkT). Time frames (T=243) are shown where applicable. For the 2D pose estimation, we utilize ground truth, CPN (Cascaded Pyramid Network), and SimpleBaseline to obtain the corresponding 2D pose sequences. T represents the number of input time frames. MCC (Motio...*

**MPI-INF-3DHP数据集。** 表3显示，DenseWarper以**65.89 mm** MPJPE取得最优结果，优于单视图方法KTP-Former（67.59 mm）和多视图全帧方法Adafuse（78.57 mm）。该数据集包含更多室外场景和复杂动作，DenseWarper的优势表明时空融合策略在更具挑战性的条件下仍保持鲁棒。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_MLs6ThXmcz/figures/007_Table_3.jpg]]
*Table 3: Reconstruction Error (MPJPE in mm) on the MPI-INF-3DHP Dataset. Input 2D pose sequences are obtained using a SimpleBaseline detector. T denotes the number of input frames. Best results are highlighted in bold*

**模型效率。** 表4报告了参数量与推理效率。DenseWarper参数量为76.51M，平均推理延迟44.51 ms，性能效率指标（MPJPE/mm per MB）为0.291。相比FinePose（T=243）的0.117，DenseWarper效率并非最优，但FinePose需243帧输入且为单视图方法；在多视图方法中，DenseWarper在精度-效率权衡上具有竞争力。需注意该延迟仅指单次模型推理时间，不含2D检测器开销。

### 消融实验

表5通过逐步添加模块验证了空间融合与时间融合的独立贡献。在Human3.6M上使用SimpleBaseline 2D检测器：

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_MLs6ThXmcz/figures/009_Table_5.jpg]]
*Table 5: Ablation study results. We conducted ablation studies on the Human3.6M and MPI-INF-3DHP datasets to validate the effectiveness of the proposed space fusion module based on epipolar geometry and the temporal fusion module Warper. We use SimpleBaseline as 2D baseline model. We have bolded the best results*

- **纯复制基线（无校正）：** 36.06 mm MPJPE。该配置仅将稀疏热图复制填充至所有时间步，不进行任何融合。
- **+ 对极几何空间融合：** MPJPE降至**31.54 mm**，降低4.52 mm（12.5%）。该模块通过沿对极线搜索其他视图的最大响应来校正复制热图中的空间误差，验证了对极几何约束在多视图校正中的有效性。
- **+ Warper时序融合（完整DenseWarper）：** MPJPE进一步降至**22.28 mm**，相比纯复制基线提升38.2%。Warper通过可变形卷积学习时序偏移并聚合多帧热图，有效恢复了交错采样造成的时间信息缺失。

在MPI-INF-3DHP上趋势一致：无校正基线94.46 mm → 加空间融合88.63 mm → 加Warper达到65.89 mm，完整模型相对基线降低30.25%。两个数据集上，时序融合模块的增益均大于空间融合模块，表明在稀疏交错输入范式下，时间信息恢复是更关键的瓶颈。

### 采样间隔与非均匀性分析

表8和表9分析了采样间隔对性能的影响。在Human3.6M数据集（相机采样间隔50 ms）上，随着帧间隔从1帧增大到12帧，空间融合后的热图质量逐渐下降（Figure 5），但DenseWarper仍能保持合理的校正效果。

表9进一步考察了非均匀间隔场景。在均匀20 ms间隔下，MPJPE为22.3 mm；当最大非均匀间隔扩展至160 ms时，MPJPE退化至31.58 mm。性能下降幅度随非均匀程度增加而加剧，但模型未出现崩溃性失效，表明Warper模块对时序不规则性具有一定容忍度。这一定量结果为实际部署中相机帧率不稳定场景提供了参考边界。

### 关键图表结论

- **Figure 1** 阐明了稀疏交错输入范式的核心思想：各视图在不同时间步交错采样，利用多视图空间冗余换取时间分辨率提升，输出帧率可达单相机帧率的M倍（M为视图数）。
- **Figure 2** 展示了DenseWarper的端到端流水线：滑动窗口采样→2D姿态估计→复制填充→对极几何空间校正→可变形卷积时序融合→三角测量输出3D关键点。
- **Figure 3** 详细说明了对极几何空间融合机制：对于待校正热图中的点q，在其他视图中计算其对极线，沿对极线搜索最大响应值，加权融合回q的原始响应。
- **Figure 4** 展示了Warper模块结构：计算空间校正热图与原始稀疏热图的差值，通过残差块和5个不同膨胀率（d∈{3,6,12,18,24}）的卷积层预测像素级偏移，对热图进行可变形扭曲并聚合。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_MLs6ThXmcz/figures/003_Figure_3.jpg]]
*Figure 3: Epipolar geometry-based spatial heatmap fusion architecture. (a) Geometric interpretation of the point-line relationship for keypoints across different views; (b) the pipeline for spatial heatmap fusion based on epipolar geometry. For an inaccurate heatmap point q, we use accurate points $q ^ { \prime }$ from other views to correct it. First, we compute the corresponding epipolar lines in the other two heatmaps. Then, we identify the maximum response along the line associated with q and add these values to the original response at q in its heatmap. This process yields a spatially corrected heatmap. In the figure, non-diagonal heatmaps with masking represent the target heatmaps for correction,...*

### 失败模式与局限性

1. **大时序间隔退化。** 当帧间隔增大时，空间融合的热图质量下降（Figure 5），非均匀间隔场景下MPJPE从22.3 mm升至31.58 mm（Table 9），表明模型在极低帧率或高度不规则采样下性能受限。
2. **2D检测器依赖。** 所有实验均基于给定的2D检测器（GT/CPN/SimpleBaseline），未探讨单视图2D检测失败或严重遮挡场景下的鲁棒性。若某视图的2D热图完全错误，对极几何校正可能引入噪声而非修正。
3. **标定依赖。** 方法依赖已知相机参数计算对极几何约束，未在无标定条件下验证。

## 方法谱系与知识库定位

### 输入范式的根本转变

传统多视图3D人体姿态估计遵循“同步密集输入”范式：每个时间步所有相机同时采样，将所有帧图像送入2D姿态估计器，再通过三角测量或体积融合获得3D骨架。这一范式存在三个结构性瓶颈：

1. **计算冗余**：所有视图的所有帧均需处理，计算量与视图数M和帧数N的乘积成正比。
2. **时间信息利用不足**：各帧独立处理，缺乏跨时间步的信息协同。
3. **帧率受限**：输出帧率严格等于单相机采样帧率，无法突破硬件限制。

DenseWarper通过**稀疏交错输入范式**从根本上改变了这一格局。在M个视角、N个总帧的序列中，每个视角仅选取单个时间步的图像，形成交错采样模式：

$${\bf D} = \{ {\bf I}_i \}_{i=1}^{\lfloor N/M \rfloor}, \quad {\bf I}_i = \{ I_{V_1}^{M(i-1)+1}, I_{V_2}^{M(i-1)+2}, \dots, I_{V_M}^{M \cdot i} \}$$

这一设计的关键效应是：输入数据量降至传统方法的1/M，但输出帧率理论上可提升至M倍（Figure 8）。因果机制在于，交错采样将时间信息编码到空间多视图中，为后续的时空协同融合创造了信息基础。

### 与现有方法的关系定位

DenseWarper在方法谱系中处于一个独特位置：它既不同于单视图时序方法，也不同于传统多视图全帧方法，更不同于简单的关键点插值方案。

**单视图基线**方面，**GLA-GCN**（Yu et al., 2023b）、**KTP-Former**（Peng et al., 2024）和**FinePose**（Xu et al., 2024a）均依赖单视角时序建模，缺少多视图几何约束，在遮挡和深度模糊场景下精度受限。DenseWarper通过多视图对极几何校正弥补了这一缺陷。

**多视图全帧基线**方面，**Adafuse**（Zhang et al., 2021）、**PPT**（Ma et al., 2022）和**Sgraformer**（Zhang et al., 2024）均假设所有视图同步密集采样。DenseWarper在仅使用1/M输入数据的条件下，在Human3.6M数据集上以GT 2D姿态取得了21.3mm MPJPE，优于Adafuse全帧的23.7mm（Table 1），证明稀疏输入在信息充分融合后可以超越密集输入的性能上界。

**关键点插值基线**方面，**Adafuse+MCC**（Zhang et al., 2021; Su et al., 2021）和**Adafuse+SLERP**（Zhang et al., 2021; Chen et al., 2022）试图通过插值提升输出帧率，但缺乏对缺失空间信息的几何校正和对时间运动模式的显式建模。DenseWarper的空间融合模块（基于对极几何的热图校正）和时间融合模块（Warper可变形卷积）分别针对这两个缺陷提供了系统性解决方案。

### 核心模块的因果机制

DenseWarper的性能优势源于两个核心模块的协同作用，消融实验（Table 5）清晰揭示了各自的独立贡献：

**对极几何空间融合模块**将复制填充产生的粗糙热图进行跨视图校正。其核心操作是：对于当前视图的每个像素位置x，在其他视图中沿对应极线搜索最大响应值，并加权融合：

$$\hat{\mathbf{H}}_v^n(x) = \lambda \mathbf{H}_v^n(x) + \frac{(1-\lambda)}{M} \sum_{u=1}^M \max_{x' \in \mathbf{p}^u(x)} \mathbf{H}_u^n(x')$$

这一校正的因果逻辑是：当某个视图中关键点位置不准确时，其他视图中沿极线的真实关键点响应可提供几何约束，将错误响应“拉回”正确位置。在Human3.6M上，仅添加此模块使MPJPE从36.06mm降至31.54mm（Table 5），验证了对极几何约束在跨视图信息融合中的有效性。

**Warper时序融合模块**进一步处理时间维度上的信息缺失。它首先计算空间校正后热图与原始稀疏输入热图之间的差异：

$$\boldsymbol{\Phi}_{V_j}^n(\boldsymbol{x}) = \hat{\mathbf{H}}_{V_j}^n(\boldsymbol{x}) - \mathbf{H}_{V_j}^{M \cdot i + j}$$

该差异编码了从其他时间步“借用”的空间信息与当前视图真实观测之间的运动偏移。随后，通过5组不同膨胀率（d ∈ {3, 6, 12, 18, 24}）的可变形卷积预测像素级偏移量，对热图进行扭曲对齐并聚合：

$$\tilde{\mathbf{H}}_{V_j}^n = \sum_{d=1}^5 \mathbf{Warper}(\boldsymbol{\Phi}_{V_j}^n, o_{V_j}^{(d)}(x))$$

添加Warper后，Human3.6M MPJPE进一步降至22.28mm，相对纯复制基线提升38.2%（Table 5）。膨胀率的多尺度设计使模型能同时捕捉局部抖动和大幅运动，这是简单线性插值无法实现的。

### 适用边界与局限性

DenseWarper的性能建立在几个关键前提之上，这些前提定义了其适用边界：

1. **相机参数已知且帧率较高**：对极几何校正依赖精确的投影矩阵和基础矩阵，且交错采样的有效性要求相机帧率足够高（Human3.6M为50fps），以保证相邻交错帧之间的运动幅度在可变形卷积的捕捉范围内。当帧间隔增大时，Table 8和Table 9显示性能逐渐下降（22.3→31.58mm），Figure 5的可视化也证实了空间校正在大间隔下效果减弱。

2. **2D姿态检测器质量依赖**：整个流程以2D热图为基础，若单视图2D检测失败或存在严重遮挡，对极几何校正和时序融合的输入质量将受到根本性影响。论文未探讨在这些极端条件下的鲁棒性。

3. **均匀采样假设**：标准实验设定采用均匀交错间隔。Table 9的非均匀间隔实验表明，随着最大非均匀间隔增加，性能有所退化，但模型仍保持可接受的准确度。然而，在极低帧率或无标定条件下，方法尚未经过验证。

### 开放问题

稀疏交错输入范式的提出为多视图3D感知开辟了若干值得探索的方向：

- **跨任务泛化**：该范式能否推广到其他多视图3D任务，如物体检测、场景重建或多人姿态估计？对极几何校正和可变形时序融合在这些任务中可能需要针对性的结构调整。

- **极端条件下的鲁棒性**：当部分视图完全失败或存在长期遮挡时，当前的对极几何校正策略可能失效。如何设计更鲁棒的跨视图信息融合机制，是一个开放挑战。

- **自适应采样策略**：能否根据运动速度动态调整交错间隔？在运动缓慢时增大间隔以降低计算量，在快速运动时缩小间隔以保证精度，这种自适应机制可进一步优化效率-精度权衡。

- **无标定场景拓展**：当前方法依赖已知相机参数。若能结合自标定或弱标定技术，将稀疏交错输入范式拓展到野外场景，将大幅扩展其应用范围。

## 原文 PDF

![[paperPDFs/ICLR_2026/From_Sparse_to_Dense_Spatio_Temporal_Fusion_for_Multi_View_3D_Human_Pose_Estimation_with_DenseWarper.pdf]]
