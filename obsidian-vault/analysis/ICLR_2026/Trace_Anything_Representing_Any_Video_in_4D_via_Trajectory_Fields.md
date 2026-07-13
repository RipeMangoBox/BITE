---
title: "Trace Anything: Representing Any Video in 4D via Trajectory Fields"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Trace_Anything_Representing_Any_Video_in_4D_via_Trajectory_Fields_c3173ca21ca2.pdf
project_link: null
code_link: null
aliases:
- TA
- TARAV4TF
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 将每个像素映射到一组在世界坐标系下的参数化三维轨迹（轨迹场），统一了运动表示和跨帧对应关系，从而无需额外的光流、深度估计器或迭代式全局对齐。
primary_logic: 视频中每个像素作为动态场景的原子单元，本质上沿着空间中的连续三维轨迹运动；因此可以将整个视频建模为一个轨迹场——一种密集映射，为每一帧的每个像素赋予一条连续的三维参数化曲线。
claims:
- Trace Anything 在自建轨迹场基准上的 EPE_mix 为 0.234，较最佳基线 St4RTrack* (0.264) 降低 11%，且推理时间 2.3 秒，比 St4RTrack* 的 21.7 秒快近 10 倍。
- 在图像对输入上，Trace Anything 的 EPE_mix 为 0.135，远超第二名 POMATO* 的 0.175，表明其从稀疏输入重建运动的能力。
- 移除静态正则化项导致 EPE_sta 从 0.218 上升到 0.273，验证了静态区域建模对整个轨迹场一致性的关键作用。
- 在三维跟踪基准 TAPVid-3D 上，Trace Anything 在 ADT 子集的 APD_3D 达到 20.5，超过专用的三维跟踪器 SpaTracker，证明前馈轨迹场能够有效处理遮挡与长序列。
---

# Trace Anything: Representing Any Video in 4D via Trajectory Fields

> [!tip] 核心洞察
> 视频中每个像素作为动态场景的原子单元，本质上沿着空间中的连续三维轨迹运动；因此可以将整个视频建模为一个轨迹场——一种密集映射，为每一帧的每个像素赋予一条连续的三维参数化曲线。

| 字段 | 内容 |
|------|------|
| 中文题名 | Trace Anything：通过轨迹场对任意视频进行四维表示 |
| 英文题名 | Trace Anything: Representing Any Video in 4D via Trajectory Fields |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=BqaChqppVh) · [paper](https://arxiv.org/abs/2507.13347) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Trace Anything |
| Dataset | Trace Anything benchmark, TAPVid-3D |

> [!tip] 效果简介
> - Trace Anything benchmark (video) 上，EPE_mix 0.234 vs 0.264 (St4RTrack*) (-11.4%)；Runtime 2.3 s vs 21.7 s (St4RTrack*) (10.4× faster)。
> - Trace Anything benchmark (image-pair) 上，EPE_mix 0.135 vs 0.175 (POMATO*) (-22.9%)。
> - TAPVid-3D (3D tracking) 上，APD_3D (ADT subset) 20.5 vs 18.3 (SpaTracker) (+12.0%)。

## 概要

动态场景理解是计算机视觉的核心难题，其关键挑战在于**如何高效、统一地表示视频中每个像素在三维空间中的运动轨迹**。现有主流方法普遍采用“逐帧重建 + 后验对应”的范式：先估计每帧的深度图或三维点云，再借助光流或二维点跟踪器建立跨帧对应关系，最后通过全局优化将各帧对齐到统一坐标系。这一流程不仅步骤繁琐、误差累积严重，而且依赖多个独立模块（深度估计器、光流网络、全局对齐求解器），导致推理效率低下，泛化能力受限。

**Trace Anything** 提出了一种根本性的范式转变：将视频中的每个像素视为沿三维空间连续曲线运动的原子单元，从而将整个视频建模为一个**轨迹场（Trajectory Field）**——一种从帧索引和像素坐标到连续三维轨迹的密集映射。这一表示统一了运动描述与跨帧对应，使得模型无需额外的深度估计、光流或迭代式全局对齐，仅通过**单次前馈推理**即可从视频帧直接输出所有像素的参数化三维运动轨迹。

**核心结论：**
- **精度领先**：在自建轨迹场基准上，Trace Anything 的混合终点误差（EPE_mix）为 0.234，较最强基线 St4RTrack*（0.264）降低约 11%（Table 1）；在图像对输入场景下，EPE_mix 为 0.135，远超第二名 POMATO*（0.175），降幅达 22.9%（Table 2）。
- **效率显著**：视频输入下的推理时间仅 2.3 秒，比 St4RTrack* 的 21.7 秒快近 10 倍（Table 1），得益于其全前馈设计无需在线优化。
- **三维跟踪能力**：在 TAPVid-3D 基准的 ADT 子集上，Trace Anything 的 APD_3D 达 20.5，超过专用三维跟踪器 SpaTracker（18.3），证明前馈轨迹场能有效应对遮挡与长序列（Table E）。

**方法定位：** Trace Anything 处于动态三维重建、点跟踪与运动表示的交叉点。与 **CoTracker3+VGGT**（先二维跟踪再提升至三维）和 **SpaTrackerV2**（前馈式稀疏三维点跟踪）不同，Trace Anything 直接预测密集的、参数化的连续三维轨迹，不依赖外部深度估计或二维跟踪器。相较于 **MonsT3R**、**St4RTrack** 和 **POMATO** 等动态重建方法，它以轨迹场替代逐帧点云加后验对应，从根本上简化了动态场景的表示与推理流程。



### 动态场景建模的核心瓶颈

从视频中恢复三维运动结构是计算机视觉的基础问题，广泛应用于机器人操作、自动驾驶和增强现实。现有的动态场景重建方法普遍采用**逐帧分离的点云表示**：先对每一帧独立估计深度或点云，再通过光流或二维点跟踪建立跨帧对应关系。这一范式存在两个根本性缺陷：

1. **流程复杂且脆弱**：系统依赖多个独立模块（深度估计器、光流估计器、全局对齐优化）的串联，各模块的误差会累积放大，且需要繁琐的后处理与迭代优化。
2. **运动表示割裂**：几何重建与运动跟踪被分解为两个独立阶段，缺乏统一的表示来同时编码场景的三维结构与时间演化，导致对遮挡、非刚体变形等复杂场景的泛化能力有限。

从因果机制上看，问题的根源在于**现有方法未将“运动”作为场景表示的一等公民**——它们先重建静态快照，再“修补”出运动对应关系，而非直接建模动态实体在时空中的连续轨迹。

### 核心洞察：像素即轨迹

Trace Anything 的核心洞察简洁而深刻：**视频中的每个像素，作为动态场景的原子观测单元，本质上沿着空间中的一条连续三维轨迹运动**。因此，整个视频可以被建模为一个**轨迹场**（Trajectory Field）——一种密集映射，为每一帧的每个像素赋予一条参数化的三维曲线：

$$\mathcal { T } : [ N ] \times [ H ] \times [ W ] \to C ( [ 0 , 1 ] , \mathbb { R } ^ { 3 } ) , \quad ( i , u , v ) \mapsto \mathbf { x } _ { i , u , v } ( \cdot )$$

这一表示将几何重建与运动跟踪统一在单个数学框架下：轨迹场同时编码了场景的三维点云（轨迹在特定时刻的采样）和跨帧对应关系（同一物理点在不同帧的轨迹连接），从而从根本上消除了对光流、深度估计器或迭代全局对齐的外部依赖。

### 方法谱系与知识库定位

Trace Anything 处于动态三维重建、点跟踪和视频深度估计三个领域的交汇点，但其设计选择与现有方法形成显著差异：

- **相对于动态三维重建方法**（如 **MonsT3R**, Zhang et al., 2025a; **POMATO**, Zhang et al., 2025b）：这些方法输出逐帧点云，依赖后处理建立对应关系。Trace Anything 直接输出具有跨帧一致性的轨迹场，避免了对应关系的事后推断。
- **相对于三维点跟踪方法**（如 **SpaTrackerV2**, Xiao et al., 2025b; **CoTracker3+VGGT**, Karaev et al., 2024a / Wang et al., 2025a）：这些方法通常需要先进行二维跟踪再提升至三维，或依赖深度估计作为中间表示。Trace Anything 以前馈方式直接预测密集三维轨迹，绕过了二维跟踪和单目深度估计的中间步骤。
- **相对于联合重建与跟踪方法**（如 **St4RTrack**, Feng et al., 2025）：这些方法虽试图统一重建与跟踪，但仍采用多阶段或逐对推理后全局优化的策略。Trace Anything 实现了**所有帧一次前馈通过**的推理方式，在速度上具有数量级优势。

### 本文动机与目标

基于上述洞察，本文提出 **Trace Anything**——一个前馈神经网络，直接从视频帧估计轨迹场。该方法的核心设计目标包括：

1. **统一表示**：以轨迹场作为视频的四维表示，同时编码几何与运动；
2. **高效推理**：单次前馈即可完成所有帧的密集轨迹估计，无需迭代优化；
3. **连续建模**：通过参数化曲线（B样条）实现时间维度的连续表示，支持任意时刻的轨迹查询与外推。

这一设计使得 Trace Anything 在自建轨迹场基准上以 **EPE_mix 0.234** 超越最佳基线 **St4RTrack***（0.264），同时推理时间仅需 **2.3 秒**，比后者的 21.7 秒快近 10 倍（Table 1）。在图像对输入场景下，该方法同样以 **EPE_mix 0.135** 显著优于 **POMATO*** 的 0.175（Table 2），展示了从稀疏观测重建稠密运动的能力。



## 核心方法与创新机理

### 瓶颈与因果杠杆

现有动态场景重建方法（如 **St4RTrack** (Feng et al., 2025)、**POMATO** (Zhang et al., 2025b)）的核心瓶颈在于：它们生成逐帧分离的三维点云，并依赖光流或二维跟踪器来建立跨帧对应关系。这种多阶段流水线不仅流程复杂、效率低下，且泛化能力受限于各独立模块的误差累积。部分方法虽采用前馈设计（如 **Easi3R** (Chen et al., 2025)），但仍需全局对齐或迭代优化来统一运动表示。

Trace Anything 的因果杠杆在于**将运动表示与跨帧对应关系统一为单一可学习映射**：直接为每个像素预测一条在世界坐标系下的参数化三维轨迹（轨迹场），从而彻底绕过了对光流、深度估计器或迭代式全局对齐的依赖。这一设计将“重建-跟踪-对齐”的多阶段问题转化为一次前馈推理即可完成的密集轨迹估计问题。

### 核心洞察

论文的核心洞察可概括为：**视频中每个像素作为动态场景的原子单元，本质上沿着空间中的连续三维轨迹运动；因此整个视频可以被建模为一个轨迹场——一种密集映射，为每一帧的每个像素赋予一条连续的三维参数化曲线。**

这一洞察将视频理解从“逐帧深度图+帧间对应”的离散范式，提升为“连续四维运动场”的统一表示，使得任意时刻的三维位置可以通过曲线求值直接获得。

### 关键 Changed Slots

Trace Anything 相对于现有方法在三个关键维度上实现了范式转变：

| 维度 | 基线方案 | Trace Anything | 证据锚点 |
|------|----------|----------------|----------|
| **场景表示** | 逐帧三维点云，通过光流/二维跟踪建立跨帧对应 | 密集轨迹场，每个像素对应一条参数化三维轨迹，统一全局坐标下的运动 | Section 1, Figure 2 |
| **推理方式** | 多阶段推理（深度估计+跟踪+全局对齐），或逐对推理后全局优化 | 所有帧一次前馈通过，无需额外估计器或迭代优化 | Section 3.2, Figure 3 |
| **时间建模** | 依赖帧间光流或二维轨迹传递运动信息 | 通过控制点样条曲线连续参数化时间维度，可直接查询任意时刻的三维位置 | Section 3.1, Equation (3) |

**场景表示的升级**是最根本的改变。轨迹场 $\mathcal{T} : [N] \times [H] \times [W] \to C([0,1], \mathbb{R}^3)$ 将帧索引和像素坐标映射到连续三维轨迹，而非孤立的点云快照。每个轨迹由 $D$ 组三维控制点 $\mathbf{P}_i \in \mathbb{R}^{D \times H \times W \times 3}$ 参数化，通过三次 B-spline 基函数合成连续曲线：

$$\mathbf{x}_{i,u,v}(t) = \sum_{k=0}^{D-1} \mathbf{P}_{i,u,v}^{(k)} \phi_k(t)$$

这一设计使得模型天然具备跨帧对应能力——轨迹在任意时间戳 $t_j$ 的取值 $\mathbf{X}_{ij}(u,v) = \mathbf{x}_{i,u,v}(t_j)$ 直接给出了像素在帧 $j$ 的三维位置，无需显式跟踪。

**推理方式的简化**带来了显著的效率优势。Trace Anything 采用 Image Encoder → Fusion Transformer → Control Point Head 的纯前馈流水线（Figure 3），所有帧经时空融合后一次性输出控制点图。在自建基准上，Trace Anything 的推理时间仅 2.3 秒，比 **St4RTrack\*** 的 21.7 秒快近 10 倍（Table 1），且精度更优（EPE_mix 0.234 vs. 0.264）。

**时间建模的连续化**使轨迹场具备帧间插值和外推能力。通过 B-spline 的参数化，模型可以查询任意连续时刻的三维位置，而不仅限于离散帧。这为后续应用（如速度外推预测、时空融合）提供了数学基础。

### 与最相关工作的差异化

- **vs. CoTracker3+VGGT**：后者通过 VGGT 将二维跟踪提升至三维，仍依赖独立的二维跟踪器和深度估计模块；Trace Anything 直接从视频预测三维轨迹，避免模块间误差传播。
- **vs. SpaTrackerV2**：后者是前馈式三维点跟踪器，但针对稀疏查询点设计；Trace Anything 输出密集逐像素轨迹场，信息完整度更高。
- **vs. MonsT3R / St4RTrack**：这些方法联合进行三维重建与跟踪，但依赖逐对处理或全局优化；Trace Anything 的一次前馈设计在效率上具有数量级优势。

### 证据强度与注意事项

上述创新点的核心证据（Table 1 的精度与速度对比、Table 3 的消融实验）置信度较高（0.95–0.98），但需注意：Trace Anything 使用自建的合成数据集（10K+ 视频）进行训练，而部分基线使用了额外的 Kubric、ScanNet 或真实标注数据，这可能影响性能对比的公平性。此外，参数曲线受限于控制点数量，对于高频往复运动或极长序列，表达能力可能下降，这是该表示的内在局限。



Trace Anything 的整体流水线遵循“一次前馈，全局推理”的设计原则，将任意长度的视频帧序列直接映射为密集的轨迹场，无需额外的深度估计器、光流计算或迭代式全局对齐。其核心架构由四个级联模块构成：**图像编码器（Image Encoder）**、**融合 Transformer（Fusion Transformer）**、**控制点预测头（Control Point Head）** 以及 **曲线求值模块（Curve Evaluation）**，整体结构见 Figure 3。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/003_Figure_3.jpg]]
*Figure 3: Trace Anything pipeline. Input frames are processed by a geometric backbone consisting of an image encoder and a fusion transformer. The control point head outputs dense control point maps*

**输入与编码。** 给定一段包含 $N$ 帧的 RGB 视频 $\{I_i\}_{i=1}^N$，图像编码器首先将每一帧独立地转换为 token 序列，提取逐帧的视觉特征。该编码器采用几何预训练骨干（如 Fast3R），为后续的时空联合推理提供具有三维结构先验的特征表示。

**时空融合推理。** 融合 Transformer 接收所有帧的 token 序列，通过帧内注意力和全局注意力机制进行联合推理。这一阶段是整个流水线的信息瓶颈——模型在此建立跨帧的时空对应关系，同时整合外观、几何和运动线索。与现有方法依赖光流或二维轨迹传递运动信息不同，融合 Transformer 直接在全局上下文中隐式地为每个像素推断其完整的三维运动轨迹。

**控制点预测。** 控制点头从融合后的特征中为每一帧 $i$ 的每一个像素 $(u,v)$ 输出 $D$ 组三维控制点及其对应的置信度，构成控制点图 $\mathbf{P}_i \in \mathbb{R}^{D \times H \times W \times 3}$。这些控制点并非直接的三维位置序列，而是用于定义一条参数化连续曲线的“锚点”，其数量 $D$ 决定了曲线的表达能力。

**连续轨迹合成。** 曲线求值模块采用三次 B-spline 基函数，根据控制点图计算任意归一化时刻 $t \in [0,1]$ 的三维位置：

$$\mathbf{x}_{i,u,v}(t) = \sum_{k=0}^{D-1} \mathbf{P}_{i,u,v}^{(k)} \phi_k(t)$$

这一设计将离散的视频帧观测转化为连续的三维轨迹场 $\mathcal{T} : [N] \times [H] \times [W] \to C([0,1], \mathbb{R}^3)$，使得模型可以在任意时刻查询每个像素的三维坐标。特别地，当 $t = t_i$（帧 $i$ 的采集时刻）时，$\mathbf{x}_{i,u,v}(t_i)$ 即恢复该帧的三维点云；当 $t = t_j$ 时，$\mathbf{x}_{i,u,v}(t_j)$ 则给出该像素在帧 $j$ 时刻的三维对应位置，从而天然建立了跨帧对应关系。

**推理效率。** 整个流水线仅需一次前馈传播即可完成所有帧的轨迹场估计。Table 1 显示，Trace Anything 的推理时间仅为 2.3 秒，比基于多阶段优化的最佳基线 St4RTrack*（21.7 秒）快近 10 倍。Figure 6 进一步揭示了各阶段推理时间随帧数的变化规律，表明融合 Transformer 的计算开销随帧数呈亚线性增长，体现了架构的可扩展性。

> **需注意**：论文未详细披露融合 Transformer 的具体层数、注意力头数及 token 维度等架构超参数，上述描述基于 Section 3.2 和 Figure 3 的公开信息。如需完整的网络规格，建议查阅补充材料或代码仓库。



Trace Anything 的核心思想是将视频建模为一个**轨迹场（Trajectory Field）**——一种从帧索引与像素坐标到连续三维轨迹的密集映射。该映射由四个关键模块串联实现：图像编码器、融合 Transformer、控制点预测头以及 B 样条曲线求值器。以下逐一展开其设计逻辑与关键公式。

### 3.1 轨迹场的形式化定义

轨迹场将视频中的每个像素视为动态场景的原子单元，赋予其一条在世界坐标系下连续的三维参数化曲线：

$$\mathcal { T } : [ N ] \times [ H ] \times [ W ] \to C ( [ 0 , 1 ] , \mathbb { R } ^ { 3 } ) , \quad ( i , u , v ) \mapsto \mathbf { x } _ { i , u , v } ( \cdot )$$

其中 $i$ 为帧索引，$(u,v)$ 为像素坐标，$\mathbf{x}_{i,u,v}(t)$ 是定义在归一化时间 $t \in [0,1]$ 上的连续三维轨迹函数。这一设计统一了运动表示与跨帧对应关系——轨迹本身即是对应关系，无需额外的光流或二维跟踪器来桥接帧间信息。

### 3.2 控制点参数化：B 样条曲线

为在有限参数下表达连续轨迹，每条轨迹被建模为 $D$ 个三维控制点的三次 B 样条曲线。对于第 $i$ 帧，模型预测一张**控制点图**：

$$\mathbf { P } _ { i } \in \mathbb { R } ^ { D \times H \times W \times 3 }$$

其含义是：每个像素 $(u,v)$ 拥有 $D$ 个三维控制点 $\mathbf{P}_{i,u,v}^{(k)} \in \mathbb{R}^3$（$k=0,\dots,D-1$）。任意时刻 $t$ 的三维位置由控制点与 B 样条基函数 $\phi_k(t)$ 的线性组合给出：

$$\mathbf { x } _ { i , u , v } ( t ) = \sum _ { k = 0 } ^ { D - 1 } \mathbf { P } _ { i , u , v } ^ { ( k ) } \phi _ { k } ( t )$$

该参数化具有两个关键性质：**（1）时间连续性**——可在任意 $t$ 处求值，支持运动插值与外推；**（2）局部控制**——每个控制点仅影响曲线的局部区间，有利于学习稳定的运动表示。消融实验证实，$D=10$ 的三次 B 样条能以优化拟合 RMSE 0.200 的精度逼近真实世界的复杂三维轨迹（Table G），表明曲线容量并非性能瓶颈。

### 3.3 流水线模块

**Image Encoder（图像编码器）**。将每帧图像独立编码为 token 序列，提取逐帧视觉特征。该模块与融合 Transformer 共同构成几何骨干网络，消融实验表明使用 Fast3R 预训练骨干可取得最佳精度，无预训练时模型难以收敛（EPE_mix 0.472，Table F）。

**Fusion Transformer（融合 Transformer）**。对多帧 token 序列执行帧内注意力与全局注意力，联合推理时空上下文。该模块使模型在单次前馈中完成所有帧的信息融合，无需迭代优化或逐对处理。

**Control Point Head（控制点预测头）**。从融合特征中为每帧每个像素输出 $D$ 组三维控制点及其置信度 $\hat{\Sigma}_{i \to j}(u,v)$。置信度用于后续损失加权，使模型能够自主表达预测不确定性。

**Curve Evaluation（曲线求值器）**。根据控制点与 B 样条基函数，按上述公式计算任意时刻的连续三维位置。两个重要特例：
- 将轨迹在帧 $j$ 的采集时刻 $t_j$ 求值，得到像素 $(u,v)$ 从帧 $i$ 到帧 $j$ 的预测三维位置 $\mathbf{X}_{ij}(u,v) = \mathbf{x}_{i,u,v}(t_j)$；
- 在自身时刻 $t_i$ 求值，恢复帧 $i$ 的三维点图 $\mathbf{X}_i(u,v) = \mathbf{x}_{i,u,v}(t_i)$。

### 3.4 核心训练目标

训练的核心损失是**置信度加权的轨迹均方误差**，同时包含对数正则项以抑制过自信预测：

$$\mathcal { L } _ { \mathrm { t r a j - c o n f } } = \frac { 1 } { | \Omega | } \sum _ { ( i , j ) } \sum _ { ( u , v ) \in \Omega } \Big [ \hat { \Sigma } _ { i \to j } ( u , v ) \ell _ { i \to j } ( u , v ) + \alpha \log \hat { \Sigma } _ { i \to j } ( u , v ) \Big ]$$

其中 $\ell_{i \to j}(u,v)$ 为预测位置与真值之间的欧氏距离平方，$\hat{\Sigma}_{i \to j}(u,v)$ 为预测的逆方差权重，$\alpha$ 控制正则化强度。整体损失还包含时间一致性、静态正则化、刚性保持和对应关系四项辅助损失，共同约束轨迹场的物理合理性。消融实验表明，移除静态正则化项 $\mathcal{L}_{\text{static}}$ 会导致静态区域误差显著上升（EPE_sta 从 0.218 升至 0.273，Table 3），验证了其对动静区域分离的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/011_Figure.jpg]]
*Figure: A: 2D Example illustrating D control points and N frame evaluations. A parametric curve (blue) defined by D = 4 control points (black squares) is evaluated at N = 6 timestamps corresponding to video frames (red dots)*



## 实验与关键发现

### 核心性能：视频轨迹场估计

Trace Anything 在自建轨迹场基准上全面超越现有方法。**Table 1** 汇总了视频输入下的量化对比：本方法在混合误差 **EPE_mix** 上达到 **0.234**，较最佳基线 **St4RTrack\***（Feng et al., 2025）的 0.264 降低约 11.4%。同时，在静态区域误差 EPE_sta（0.218）、动态区域误差 EPE_dyn（0.249）、一致性精度 CA 和形状偏差 SDD 等全部指标上均取得最优。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on video-based trajectory field estimation. CA is reported in*

推理效率方面，Trace Anything 的前馈设计带来数量级优势：单次推理耗时仅 **2.3 秒**，而 St4RTrack\* 需要 21.7 秒（约 10.4 倍加速）。该优势源于方法无需逐帧深度估计、光流计算或迭代式全局对齐，所有帧一次前馈即可输出完整轨迹场。

**Figure 4** 在 DAVIS 数据集上的定性结果表明，Trace Anything 能够从视频中重建出动态点云序列和密集三维轨迹，对复杂非刚体运动和遮挡保持鲁棒。

### 图像对输入下的运动重建

当仅提供初始帧和目标帧（图像对）时，Trace Anything 仍能推断隐含的时空动态并插值中间运动。**Table 2** 显示，本方法在图像对基准上的 EPE_mix 为 **0.135**，显著优于第二名 **POMATO\***（Zhang et al., 2025b）的 0.175（降幅约 22.9%），证明轨迹场表示能够从稀疏观测中有效重建连续运动。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/007_Table_2.jpg]]
*Table 2: Quantitative results on image-pair-based trajectory field estimation. CA is reported in*

**Figure 5** 在 Bridge 机器人操作数据集上的定性结果展示了目标条件操作场景：给定初始和目标图像，Trace Anything 预测的轨迹场能够同时插值机械臂和被操作物体的三维运动。

### 三维跟踪能力

在 TAPVid-3D 基准的 ADT 子集上（**Table E**），Trace Anything 的 APD_3D 达到 **20.5**，超过专用三维跟踪器 **SpaTracker**（Xiao et al., 2025b）的 18.3。这表明前馈轨迹场能够有效处理遮挡与长序列跟踪，尽管本方法并非专门为稀疏点跟踪设计。

### 消融研究：损失函数设计

**Table 3** 系统消融了各损失项的贡献。关键发现如下：

- **静态正则化至关重要**：移除静态损失 L_static 导致 EPE_sta 从 0.218 急剧上升至 0.273，验证了静态区域建模对维持轨迹场整体一致性的关键作用。
- **多目标正则化协同作用**：同时移除刚性损失 L_rigid 和对应损失 L_corr 会普遍降低所有指标，表明多目标约束共同提升轨迹的时空一致性。
- **置信度加权机制有效**：轨迹-置信度损失 L_traj-conf 中的对数正则项抑制了过自信预测，对不确定性建模有正面贡献。

### 骨干网络与曲线参数化

**Table F** 对比了不同骨干网络和曲线类型。使用 **Fast3R 预训练骨干**结合 **三次 B-spline（D=10 控制点）** 取得最佳整体精度。无预训练时模型难以收敛（EPE_mix 高达 0.472），表明几何先验对轨迹场学习至关重要。

**Table G** 验证了曲线容量：三次 B-spline 以 D=10 控制点优化拟合真实三维轨迹的 RMSE 仅 0.200，证明曲线表达能力并非性能瓶颈。

### 公平性说明

需注意训练数据差异：Trace Anything 使用自建合成数据集（10K+ 视频）训练，而部分基线额外使用了 Kubric、ScanNet 或真实标注数据（**Table A**）。这可能影响性能对比的绝对公平性。此外，Trace Anything 的前馈设计在运行时对比中具有固有优势，但基于在线优化的方法在特定困难场景下可能保有精度竞争力。

### 已知局限与失败模式

1. **域差异**：合成数据训练导致模型与真实场景间存在域间隙，在低纹理、运动模糊或极端视角变化下性能可能下降。
2. **曲线容量限制**：对于高频往复运动或极长序列，固定控制点数的 B-spline 可能表达能力不足，需裁剪窗口或下采样，性能随之衰减。
3. **密集预测的精度边界**：作为首次密集逐像素轨迹场估计尝试，其精度可能不如专门设计的稀疏三维跟踪方法；结合稀疏跟踪的精细化估计是未来方向。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/008_Table_3.jpg]]
*Table 3: Ablation study on loss terms. CA is reported in*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/004_Figure_4.jpg]]
*Figure 4: Video-based trajectory field estimation on DAVIS (Perazzi et al., 2016). Trace Anything predicts trajectory fields that can yield dynamic point cloud sequences and dense 3D trajectories, while remaining robust to complex non-rigid motion and occlusions*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/006_Figure_5.jpg]]
*Figure 5: Image-pair-based trajectory field estimation (goal-conditioned manipulation) on Bridge (Walke et al., 2023). Given an initial and a goal image, Trace Anything predicts a trajectory field that interpolates the 3D motion of both the robot arm and manipulated objects. We further show the projected 2D trajectories (see Section E.3 and Figure J for details)*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/009_Figure_6.jpg]]
*Figure 6: Stage-wise runtime vs. number of input frames*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/026_Table.jpg]]
*Table: E: Quantitative results on 3D tracking. Best in bold, second-best underlined*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/027_Table.jpg]]
*Table: F: Ablation study on Trace Anything benchmark. CA is reported in 1 $0 ^ { - 2 }$ and SDD in 10−3. Best in bold, second-best underlined*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/031_Table.jpg]]
*Table: G: Curve-fitting accuracy. Optimal fitting of various parametric curves (linear, Bezier, B- ´ spline) to complex real-world 3D trajectories from TAPVid-3D (Koppula et al., 2024). A cubic B-spline with D=10 control points achieves the lowest error, outperforming state-of-the-art 3D tracking methods, indicating that curve capacity is not the limiting factor*

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_BqaChqppVh/figures/010_Figure_8.jpg]]
*Figure 8: Spatio-temporal fusion. The trajectory field can be leveraged to fuse observations of the dynamic entity across different frames into a canonical frame*



## 定位与知识库关联

### 1. 与现有工作的关系

Trace Anything 的核心创新在于将视频表示从“逐帧点云+后验对应”转变为“统一的密集轨迹场”，这一转变使其在方法谱系中占据了独特位置。以下从三个维度梳理其与现有工作的关系。

**与动态三维重建方法的关系。** 传统动态重建方法（如 **MonsT3R** (Zhang et al., 2025a)、**Easi3R** (Chen et al., 2025)）通常先估计每帧的三维点云，再通过光流或二维跟踪建立跨帧对应关系，形成多阶段流水线。Trace Anything 改变了这一范式：它直接输出每个像素在世界坐标系下的参数化三维轨迹，使点云重建与跨帧对应在单一前馈过程中同时完成。与 **POMATO** (Zhang et al., 2025b) 等动态点云重建方法相比，Trace Anything 不依赖逐对推理后的全局优化，而是对所有帧进行一次联合推理，从根本上简化了处理流程。

**与三维跟踪方法的关系。** 现有三维跟踪方法大致分为两类：一类是“2D跟踪+深度提升”的混合方案，如 **CoTracker3+VGGT** (Karaev et al., 2024a; Wang et al., 2025a)，依赖独立的深度估计器和二维跟踪器；另一类是前馈式三维点跟踪器，如 **SpaTrackerV2** (Xiao et al., 2025b)。Trace Anything 与后者共享前馈推理的理念，但关键区别在于：它不跟踪稀疏的查询点，而是为每一帧的每一个像素估计完整的连续三维轨迹，从而实现了“密集轨迹场”而非“稀疏点跟踪”。在 TAPVid-3D 基准的 ADT 子集上，Trace Anything 的 APD_3D 达到 20.5，超过专用三维跟踪器 SpaTracker 的 18.3（Table E），证明密集轨迹场范式在遮挡和长序列场景下具有竞争力。

**与联合重建-跟踪方法的关系。** **St4RTrack** (Feng et al., 2025) 是最近的联合三维重建与跟踪方法，在 Trace Anything 自建基准上以 EPE_mix 0.264 排名第二。Trace Anything 以 0.234 的 EPE_mix 超越 St4RTrack*（降低 11.4%），且推理时间仅 2.3 秒，比后者的 21.7 秒快近 10 倍（Table 1）。这一优势源于轨迹场表示本身蕴含了跨帧对应关系，无需额外的全局对齐或迭代优化步骤。

### 2. 适用边界

Trace Anything 的适用边界由其设计选择和技术特性共同决定。

**输入模态的灵活性。** 该方法支持两种输入模式：多帧视频输入和图像对输入。在视频输入模式下，模型利用多帧时空上下文进行联合推理；在图像对输入模式下，模型从首末帧推断中间运动，EPE_mix 达到 0.135，显著优于第二名 POMATO* 的 0.175（Table 2）。这种灵活性使轨迹场可同时服务于视频重建和目标条件操作等不同场景。

**运动复杂度的上限。** 轨迹场使用三次 B-spline 曲线（D=10 控制点）参数化连续运动。曲线拟合分析（Table G）表明，该配置能以优化拟合 RMSE 0.200 高保真地拟合真实世界的复杂三维轨迹，说明曲线容量本身并非瓶颈。然而，对于高频往复运动或极长帧序列，固定数量的控制点可能表达能力不足，需要裁剪窗口或下采样，性能随之下降。

**静态与动态区域的统一处理。** 消融实验（Table 3）表明，移除静态正则化项 L_static 导致 EPE_sta 从 0.218 升至 0.273，验证了静态区域建模对整个轨迹场一致性的关键作用。轨迹场通过统一的参数化同时处理静态背景和动态前景，但这一能力依赖于训练数据中动静区域的充分覆盖。

### 3. 局限与开放问题

**合成-真实域差异。** Trace Anything 使用自建的合成数据集（10K+ 视频）训练，与真实场景之间存在域差异。论文明确指出，引入实景部分标注有望弥合这一差距，但当前尚未实现。这一局限可能影响模型在低纹理、运动模糊或极端视角变化等真实挑战场景下的鲁棒性。

**参数曲线的表达能力边界。** 尽管三次 B-spline 在常规运动中表现良好，但参数曲线受限于控制点数量，对于快速往复运动或极长序列可能表达能力不足。当前解决方案（裁剪窗口或下采样）是工程折中，而非根本性突破。

**密集估计与稀疏精度的权衡。** 作为密集逐像素轨迹场估计的首次尝试，Trace Anything 的精度可能不如专门设计的稀疏三维跟踪方法。论文将“结合稀疏跟踪的精细化估计”列为未来方向，暗示当前密集输出在局部精度上仍有提升空间。

**开放问题。** 基于上述局限，以下问题值得进一步探索：（1）如何有效融入真实数据的部分标注或其他先验，以减小合成训练的域差异？（2）如何处理高频往复运动或极长序列，使参数曲线保持表达能力又不损失精度？（3）能否将轨迹场与神经渲染（如动态 3DGS）结合，实现高质量的视图合成与运动建模的统一？（4）密集轨迹场能否驱动机器人操作中的长期规划，并有效处理物体变形和遮挡？（5）模型在低纹理、运动模糊或极端视角变化下的鲁棒性如何？这些问题构成了轨迹场范式从当前验证走向广泛部署的关键路径。

### 4. 知识库定位

Trace Anything 在知识库中的定位可概括为：**首次将密集轨迹场确立为视频的四维表示原语**。它连接了三个原本相对独立的研究方向——动态三维重建、三维点跟踪和参数曲线建模——并在交叉点上提出了统一的解决方案。其核心贡献不在于单项技术的突破，而在于表示范式的转换：将“重建后跟踪”的多阶段流水线压缩为“轨迹即表示”的单阶段前馈推理。这一转换使 Trace Anything 成为后续研究（如轨迹场驱动的神经渲染、机器人操作规划）的基础设施级工作，其自建基准和开源代码（如有）将为该方向的标准化评估提供支撑。



## 原文 PDF

![[paperPDFs/ICLR_2026/Trace_Anything_Representing_Any_Video_in_4D_via_Trajectory_Fields_c3173ca21ca2.pdf]]
