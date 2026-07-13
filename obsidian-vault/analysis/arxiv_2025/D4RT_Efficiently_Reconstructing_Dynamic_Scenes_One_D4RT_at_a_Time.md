---
title: "D4RT: Efficiently Reconstructing Dynamic Scenes One D4RT at a Time"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/D4RT_Efficiently_Reconstructing_Dynamic_Scenes.pdf
project_link: https://d4rt-paper.github.io/
code_link: null
aliases:
- D4RT
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入了一种基于查询的解码器接口，利用全局场景表示，允许模型独立、灵活地按需查询任意时空点的 3D 位置。
primary_logic: 通过将空间坐标 (u, v) 与三个时间索引（源时刻 t_src, 目标时刻 t_tgt, 相机参考帧 t_cam）解耦并共同作为查询条件，一个轻量级的交叉注意力解码器能够从全局场景表示中重建出完整的 4D 信息，统一了点跟踪、深度估计、点云重建与相机位姿估计等多个任务。
claims:
- D4RT 在 TAPVid-3D 基准上取得了最先进的 3D 跟踪结果，在已知相机内参的情况下，所有子集上的性能均显著优于 SpatialTrackerV2。
- D4RT 在相机位姿估计中的速度超过 200 FPS，比 VGGT 快 9 倍，比 MegaSaM 快 100 倍，同时精度更优（Sintel ATE 0.065 vs MegaSaM 0.074）。
- 消融实验表明，局部 RGB patch 嵌入对性能至关重要：移除后深度 AbsRel (S) 从 0.302 上升至 0.366，相机 ATE 从 0.102 上升至 0.122。
- D4RT 是唯一能够重建整个视频中所有像素的完整 4D 场景表示的方法，而 MegaSaM、π³ 等纯重建方法在动态场景中失败，SpatialTrackerV2 因只追踪单帧点而产生间隙。
---

# D4RT: Efficiently Reconstructing Dynamic Scenes One D4RT at a Time

> [!tip] 核心洞察
> 通过将空间坐标 (u, v) 与三个时间索引（源时刻 t_src, 目标时刻 t_tgt, 相机参考帧 t_cam）解耦并共同作为查询条件，一个轻量级的交叉注意力解码器能够从全局场景表示中重建出完整的 4D 信息，统一了点跟踪、深度估计、点云重建与相机位姿估计等多个任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | D4RT：一次一个 D4RT 高效重建动态场景 |
| 英文题名 | D4RT: Efficiently Reconstructing Dynamic Scenes One D4RT at a Time |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.08924) · [Project](https://d4rt-paper.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | D4RT |
| Dataset | Sintel, TAPVid-3D, 3D Tracking Throughput @ 60 FPS |

> [!tip] 效果简介
> - Sintel (Video Depth) 上，AbsRel (S) ↓ 0.171 vs 0.241 (π³) / 0.342 (MegaSaM) (较 π³ 降低 29%，较 MegaSaM 降低 50%)。
> - Sintel (Camera Pose) 上，ATE ↓ 0.065 vs 0.074 (MegaSaM) / 0.168 (VGGT) (比 MegaSaM 低 12%，比 VGGT 低 61%)。
> - Sintel (Point Cloud) 上，L1 ↓ 0.768 vs 1.139 (π³) / 1.531 (MegaSaM) (比 π³ 低 33%，比 MegaSaM 低 50%)。

## 概要

动态场景的完整 4D 重建与跟踪是计算机视觉中的核心挑战。现有方法在动态场景中缺乏统一、高效的时空点查询机制：纯重建方法（如 MegaSaM、VGGT、π³）在动态场景中产生明显的失败案例，而点跟踪方法（如 SpatialTrackerV2）虽能捕捉运动，却因仅追踪单帧点而留下重建间隙。这些方法的根本瓶颈在于无法以统一的方式灵活查询任意时空点的 3D 位置，导致计算冗余、任务碎片化。

D4RT 提出了一种根本性的解决思路：**将空间坐标与时间索引解耦，构建统一的查询接口**。模型由一个全局自注意力编码器和一个轻量级交叉注意力解码器组成。编码器将输入视频压缩为全局场景表示 $F = \mathcal{E}(V) \in \mathbb{R}^{N \times C}$，解码器则通过独立查询 $\mathbf{q}$ 从 $F$ 中解码出任意时空点的 3D 位置 $\mathbf{P} = \mathcal{D}(\mathbf{q}, F) \in \mathbb{R}^3$。每个查询携带三个时间索引——源时刻 $t_{src}$、目标时刻 $t_{tgt}$、相机参考帧 $t_{cam}$——以及局部 RGB patch 嵌入，使模型能够同时处理静态和动态对应关系。这一设计将深度估计、3D 点跟踪、点云重建与相机位姿估计统一为同一查询范式的不同实例（Table 1），无需多个任务特定的解码头。

实验结果表明，D4RT 在多个基准上实现了性能与效率的双重突破：

- **3D 跟踪**：在 TAPVid-3D 基准上取得最先进结果，已知相机内参时在所有子集上显著优于 SpatialTrackerV2（如 DriveTrack 上 APD3D 从 0.195 提升至 0.304）；吞吐量方面，在 60 FPS 目标下可处理 550 条轨迹，而 SpatialTrackerV2 仅 29 条，速度提升达 18–300 倍（Table 3, Table 4）。
- **深度与点云估计**：在 Sintel 上深度 AbsRel (S) 为 0.171，较 π³（0.241）降低 29%，较 MegaSaM（0.342）降低 50%；点云 L1 误差为 0.768，较 π³（1.139）降低 33%（Table 5）。
- **相机位姿估计**：速度超过 200 FPS，比 VGGT 快 9 倍，比 MegaSaM 快 100 倍，同时精度更优（Sintel ATE 0.065 vs MegaSaM 0.074）（Figure 3, Table 6）。
- **完整 4D 重建**：D4RT 是唯一能够重建整个视频中所有像素的完整 4D 场景表示的方法，而纯重建方法在动态场景中失败，SpatialTrackerV2 则因稀疏追踪产生间隙（Figure 4）。

消融实验揭示了几个关键设计选择：局部 RGB patch 嵌入对保留细粒度细节至关重要，移除后深度 AbsRel (S) 从 0.302 上升至 0.366，相机 ATE 从 0.102 上升至 0.122（Table 7, Figure 6）；编码器主干从 ViT-B 扩展到 ViT-g 可带来显著性能提升，ATE 从 0.145 降至 0.078（Table 9）；从原图分辨率提取 RGB patch 可获得最低的深度边缘误差（Table 10, Figure 9）。

当前方法的主要局限在于编码器输入分辨率为固定的 256×256，可能限制对极高频细节的感知；长视频处理依赖分段对齐，未包含闭环优化，可能导致长距离漂移。未来的开放问题包括：将查询机制扩展到任意长度的在线视频流、处理高度动态且存在大量镜面反射的场景，以及探索该统一查询范式在多模态融合中的推广。



从视频中恢复场景的完整 4D 表示（3D 几何 + 时间动态）是计算机视觉的核心目标之一，其输出——深度图、3D 点跟踪、相机位姿、点云——是自动驾驶、机器人、增强现实等下游应用的基础。然而，现有方法在统一性、效率和动态场景处理能力上存在根本性缺口。

**碎片化的任务架构**。当前的主流方案将不同几何任务分配给独立的模型或解码器。以 **VGGT**（Wang et al., CVPR 2025）和 **π³**（Wang et al., arXiv 2025）为代表的纯重建方法，依赖密集的每帧解码或多任务输出头，计算冗余且无法灵活处理时空对应关系。**SpatialTrackerV2**（Xiao et al., ICCV 2025）虽然能跟踪动态点，但其多阶段迭代优化的设计仅支持从单帧出发的稀疏追踪，无法生成完整的 4D 场景表示。这种“一任务一模型”的范式导致系统复杂度高、部署成本大，且各任务之间无法共享表征。

**动态场景的盲区**。纯重建方法（如 **MegaSaM**（Li et al., CVPR 2025）、**DUSt3R**（Wang et al., CVPR 2024）、π³）本质上是为静态场景设计的——它们将不同时刻的像素累积到同一坐标系中，在动态场景中会产生重影、错位等灾难性失败（如 Figure 4 所示，天鹅被重复重建，花朵完全无法恢复）。而专用的跟踪方法（如 **CoTracker3 + UniDepthV2**、**DELTA**）虽然能处理运动，却牺牲了全局重建能力，仅输出稀疏轨迹。**没有一种方法能够同时覆盖静态和动态场景的完整 4D 重建。**

**效率瓶颈**。密集的每帧解码或迭代优化使得现有方法在吞吐量上捉襟见肘。在 3D 跟踪任务中，SpatialTrackerV2 在 60 FPS 的目标下仅能处理 29 条轨迹，而实际应用往往需要数百甚至数千条轨迹的实时跟踪。这种效率差距源于一个根本性的设计缺陷：**缺乏一种灵活、按需的时空点查询机制**，使得计算量与任务需求成比例，而非与视频帧数成比例。

**本文动机**。上述缺口指向同一个核心瓶颈：现有方法缺乏统一的、高效的时空点查询接口，导致计算冗余、任务碎片化，且无法同时处理静态和动态场景。D4RT 的提出正是为了填补这一空白——通过引入一种基于查询的解码器接口，利用全局场景表示，允许模型独立、灵活地按需查询任意时空点的 3D 位置，从而用一个轻量架构统一点跟踪、深度估计、点云重建与相机位姿估计，并在效率和精度上同时超越专用方法。



## 核心方法与创新机理

D4RT 的核心创新在于**将动态场景的 4D 重建与跟踪统一为一种基于查询的解码范式**，从根本上改变了现有方法处理时空几何信息的方式。这一设计通过以下几个关键的“changed slots”体现：

### 1. 从多任务分离解码到统一查询接口

现有方法普遍采用**分离式多任务解码器**（如 **VGGT** (Wang et al., CVPR 2025) 和 **π³** (Wang et al., arXiv 2025) 分别设计深度、点云和相机位姿的解码头）或**昂贵的迭代优化**（如 **SpatialTrackerV2** (Xiao et al., ICCV 2025) 需要多阶段迭代更新轨迹）。这种设计导致两个根本性问题：

- **计算冗余**：每个任务独立解码，无法共享场景理解的计算。
- **任务碎片化**：深度估计、点跟踪和相机位姿估计被割裂为独立流程，缺乏统一的几何一致性约束。

D4RT 用一个**单一轻量交叉注意力解码器**替代了这些分离的模块。该解码器接收任意构造的查询 $\mathbf{q}$，与全局场景表示 $F$ 进行一次交叉注意力交互，即可输出对应的 3D 点坐标 $\mathbf{P} = \mathcal{D}(\mathbf{q}, F) \in \mathbb{R}^3$。所有几何任务——深度估计、点云重建、3D 点跟踪、相机内参与外参估计——都被统一为同一解码器的不同查询模式（Table 1），无需任何任务特定的解码头。

### 2. 从静态/稀疏跟踪到统一动态对应处理

现有方法在动态场景处理上存在根本性缺陷：

- **纯重建方法**（**MegaSaM** (Li et al., CVPR 2025)、**VGGT**、**π³**）无法追踪动态点，在运动物体上产生重影或完全失败（Figure 4 中天鹅重复出现、花朵重建失败）。
- **跟踪方法**（**SpatialTrackerV2**）虽能捕获动态，但设计上只能追踪单帧的稀疏点，导致重建存在大量间隙（Figure 4 中天鹅和火车背后的空白区域）。

D4RT 通过**将空间坐标 $(u, v)$ 与三个时间索引解耦**实现了突破：源时刻 $t_{\text{src}}$（查询点所在帧）、目标时刻 $t_{\text{tgt}}$（希望获取 3D 位置的帧）和相机参考帧 $t_{\text{cam}}$。这一设计使得模型可以**独立查询任意像素在任意时刻的 3D 位置**，无论该点属于静态背景还是动态物体。Table 4 的结果验证了这一能力的有效性：D4RT 在 TAPVid-3D 的 DriveTrack 子集上 APD3D 达到 0.304，显著优于 SpatialTrackerV2 的 0.195（提升 56%）。

### 3. 从密集逐帧解码到天然并行的独立查询

传统方法需要**密集的逐帧解码**（如 VGGT 对每帧运行完整前向传播）或**序列依赖的迭代优化**（如 SpatialTrackerV2 的轨迹需要逐帧更新），导致吞吐量极低。

D4RT 的查询机制实现了**天然并行**：每条轨迹由 $T$ 个完全独立的查询组成，每个查询仅需一次交叉注意力前向传播。Table 3 量化了这一优势：在 60 FPS 目标下，D4RT 可处理 550 条轨迹，而 SpatialTrackerV2 仅 29 条，速度提升达 18 倍（与其他方法差距可达 300 倍）。在相机位姿估计中，D4RT 达到 200+ FPS，比 VGGT 快 9 倍，比 MegaSaM 快 100 倍（Figure 3），同时精度更优（Sintel ATE 0.065 vs MegaSaM 0.074）。

### 创新机制的关键支撑

查询的构造是这一范式成功的核心工程细节。每个查询不仅包含傅里叶编码的空间坐标和时间步嵌入，还包含一个从原始视频中提取的 **$9 \times 9$ 局部 RGB patch 嵌入**。消融实验（Table 7, Figure 6）表明，移除该 patch 嵌入会导致深度 AbsRel (S) 从 0.302 上升至 0.366，相机 ATE 从 0.102 上升至 0.122，证实了局部外观信息对于保持细粒度几何细节（如锐利边缘）至关重要。

综上，D4RT 的“changed slots”并非孤立的模块替换，而是一个**系统性的范式转换**：将动态 4D 重建从“为每个任务设计专用解码器”转变为“设计一个通用的查询语言，让模型学会按需回答任意时空点的几何问题”。这一转换同时解决了计算效率、动态对应和任务统一性三个瓶颈。



D4RT 是一个统一的前馈式动态 4D 重建与跟踪框架，其核心设计理念是：**通过单一、轻量级的查询解码器接口，替代传统方法中密集的逐帧解码或多个任务专用解码器**。整个 pipeline 由四个关键模块串联构成：视频标记化 → ViT 编码器 → 交叉注意力解码器 → 投影头，形成从原始视频到任意时空点 3D 坐标的端到端映射。

### 输入输出流

**输入**：一段包含 $T$ 帧的 RGB 视频 $V$。视频首先被下采样到固定分辨率（训练时为 $256 \times 256$）并分块标记化（patchify），同时附加纵横比标记以保留原始宽高比信息。

**全局场景表示**：标记化后的视频通过一个交错局部帧注意力和全局自注意力的 Vision Transformer 编码器 $\mathcal{E}$，生成全局场景表示 $F$：

$$F = \mathcal{E}(V) \in \mathbb{R}^{N \times C}$$

这一表示 $F$ 是整个框架的核心枢纽——它一次性编码了视频中所有帧的时空信息，后续所有任务均通过查询 $F$ 来完成，无需重复编码。

**查询接口**：对于任意给定的 2D 点 $(u, v)$，模型构建一个查询标记 $\mathbf{q}$，其中包含三个时间索引的解耦信息：
- $t_{\text{src}}$：源帧（该点首次出现的时刻）
- $t_{\text{tgt}}$：目标帧（要查询 3D 位置的时刻）
- $t_{\text{cam}}$：相机参考帧（指定坐标系）

查询标记还融合了以 $(u, v)$ 为中心的 $9 \times 9$ 局部 RGB patch 嵌入，为解码器提供精细的空间上下文（消融实验证实这对保留边缘细节至关重要）。

**解码与投影**：轻量级交叉注意力解码器 $\mathcal{D}$ 将查询 $\mathbf{q}$ 与全局场景表示 $F$ 进行交叉注意力交互，输出特征向量，再由投影头映射为 3D 点坐标 $\mathbf{P}$ 及辅助预测：

$$\mathbf{P} = \mathcal{D}(\mathbf{q}, F) \in \mathbb{R}^3$$

辅助输出包括 2D 重投影坐标、可见性、运动向量、法线及置信度等。

### 统一多任务解码

通过灵活组合查询参数，D4RT 将多种几何任务统一到同一接口下（见 Table 1）：
- **深度估计**：查询 $t_{\text{src}} = t_{\text{tgt}} = t_{\text{cam}}$，解码所有像素的 3D 位置即得深度图。
- **点云重建**：对所有帧的所有像素执行上述查询，累积得到完整点云。
- **3D 点跟踪**：固定源帧和源点，遍历目标帧 $t_{\text{tgt}}$ 查询对应 3D 位置，形成跨帧轨迹。
- **相机内参估计**：在帧内采样稀疏网格点，解码其 3D 坐标后，通过针孔模型反推焦距：

$$f_x = \frac{p_z (u - 0.5)}{p_x}, \quad f_y = \frac{p_z (v - 0.5)}{p_y}$$

取所有估计的中值作为最终焦距。
- **相机外参估计**：通过跟踪静态背景点在世界坐标系中的运动，联合优化相机位姿。

### 高效密集跟踪算法

为实现全视频所有像素的完整 4D 重建，D4RT 设计了一种自适应密集跟踪策略：仅从未被访问的像素发起新轨迹，每条完整轨迹在跟踪过程中标记其可见的所有时空像素为“已访问”，从而避免冗余查询。根据视频运动复杂度，这一策略可带来 **5–15 倍的自适应加速**。

### 与基线方法的架构对比

Table 2 系统对比了 D4RT 与现有方法的架构能力差异：
- **纯重建方法**（MegaSaM、VGGT、DUSt3R、π³）：依赖密集逐帧解码或多个任务专用解码器，无法处理动态对应关系，在动态场景中产生重复或失败的重建。
- **跟踪方法**（SpatialTrackerV2）：采用昂贵的多阶段迭代优化，且仅能追踪单帧稀疏点，重建结果存在间隙。
- **D4RT**：单一交叉注意力解码器，支持按需独立查询任意时空点，覆盖静态与动态点，天然支持并行计算，在效率上实现 18–300 倍的吞吐量提升。

### 补充图表

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/019_Figure_9.jpg]]
*Figure 9: Visualizing sub-pixel detail recovery – We propose a visual comparison of the different high-res configurations. Config ⃝4 achieves the highest fidelity, it preserves sharp edges and recovers fine details—such as the hair in the bottom row—without increasing the computational cost or memory requirements of the overall model*



D4RT 的核心架构由三个关键模块构成：视频标记化与全局场景编码、查询构建、以及交叉注意力解码与投影。整个流程遵循“一次编码，按需查询”的设计哲学，将视频理解与几何重建解耦为编码器-解码器范式。

### 全局场景表示

给定输入视频 $V$，编码器 $\mathcal{E}$ 将其映射为一个全局场景表示：

$$F = \mathcal{E}(V) \in \mathbb{R}^{N \times C}$$

其中 $N$ 为 token 数量，$C$ 为特征维度。编码器基于 Vision Transformer，采用交错的局部帧内窗口自注意力和全局自注意力层，使每一帧的局部信息与跨帧的时空上下文充分交互。最终产生的 $F$ 是整个视频的压缩潜在表征，包含了所有帧的几何与外观线索。

### 查询构建

查询是 D4RT 统一接口的核心。对于任意一个待解码的时空点，查询 $\mathbf{q}$ 由三部分信息拼接而成：

1. **傅里叶坐标特征**：对空间坐标 $(u, v)$ 进行位置编码，提供连续的亚像素定位能力。
2. **时间步嵌入**：三个时间索引——源时刻 $t_{\text{src}}$、目标时刻 $t_{\text{tgt}}$、相机参考帧 $t_{\text{cam}}$——分别编码为可学习的嵌入向量。这种三时间解耦设计是 D4RT 处理动态对应关系的因果开关：它允许模型独立地指定“从哪一帧的哪个像素出发”“查询哪一时刻的 3D 位置”“在哪个相机坐标系下表达结果”。
3. **局部 RGB patch 嵌入**：以 $(u, v)$ 为中心的 $9 \times 9$ 局部图像块经过线性投影后作为外观线索注入查询。消融实验证实该模块对性能至关重要：移除后深度 AbsRel (S) 从 0.302 上升至 0.366，相机 ATE 从 0.102 上升至 0.122（Table 7, Figure 6），表明局部纹理信息对精细几何推理不可或缺。

### 交叉注意力解码与投影

轻量级交叉注意力解码器 $\mathcal{D}$ 将查询 $\mathbf{q}$ 与全局场景表示 $F$ 进行交互，输出解码特征，再通过投影头得到 3D 点坐标：

$$\mathbf{P} = \mathcal{D}(\mathbf{q}, F) \in \mathbb{R}^3$$

解码器由若干交叉注意力 Transformer 层组成，每个查询独立地与 $F$ 中的所有 token 进行注意力计算。这种“查询-场景”交互模式天然支持并行化：任意数量、任意时空位置的查询可以批量处理，无需按帧顺序解码。投影头从解码特征中同时输出辅助预测（2D 坐标、法线、可见性、运动向量、置信度），用于多任务损失监督。

### 相机内参估计

D4RT 无需单独的内参估计模块。对于视频帧 $i$，在归一化图像平面上采样一个粗网格 $(u, v)$，构建查询并解码得到对应 3D 点 $\mathbf{P} = (p_x, p_y, p_z)$。假设针孔相机模型且主点位于 $(0.5, 0.5)$，焦距可通过下式逐点估计：

$$f_x = \frac{p_z (u - 0.5)}{p_x}, \quad f_y = \frac{p_z (v - 0.5)}{p_y}$$

对所有网格点的估计取中值作为该帧的最终焦距。这种从几何一致性中隐式恢复内参的方式，使 D4RT 无需显式标定即可处理任意视频。

### 损失函数

训练使用复合多任务损失，对每个查询的预测进行监督：

$$\mathcal{L} = \frac{1}{N} \sum_{i=1}^{N} \left( c \lambda_{3D} \mathcal{L}_{3D} - \lambda_{\mathrm{conf}} \log c + \lambda_{2D} \mathcal{L}_{2D} + \lambda_{\mathrm{vis}} \mathcal{L}_{\mathrm{vis}} + \dots \right)_i$$

其中 $\mathcal{L}_{3D}$ 为 3D 坐标的 Huber 损失，$\mathcal{L}_{2D}$ 为 2D 重投影损失，$\mathcal{L}_{\mathrm{vis}}$ 为可见性二分类损失，$c$ 为模型预测的置信度标量。置信度项通过拉普拉斯似然的形式实现自适应加权：高置信度时 $\mathcal{L}_{3D}$ 权重增大，同时 $-\log c$ 项惩罚过度自信。消融实验表明，移除置信度损失会使 ATE 增加 0.126，移除 2D 位置损失会使深度 AbsRel (S) 增加 0.071（Table 8），验证了各辅助损失对整体性能的贡献。

### 补充图表

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/006_Figure_4.jpg]]
*Figure 4: Reconstruction results across methods – Pure reconstruction methods (MegaSaM and $\pi ^ { 3 }$ ) are only able to accumulate point clouds of all pixels; exhibiting clear failure cases in dynamic scenes. For example, the swan is repeated in MegaSaM’s reconstruction, and $\pi ^ { 3 }$ is failing entirely to reconstruct the flower. SpatialTrackerV2, a state-of-the-art tracking method, successfully captures dynamics, however its design only allows tracking points from one frame, leaving gaps in the reconstruction (behind the swan and train). D4RT is the only method that successfully reconstructs a full 4D representation of the scene including all pixels of the video



## 实验与关键发现

### 核心实验设计逻辑

D4RT 的实验体系围绕一个中心命题展开：**统一的查询式解码器能否在动态场景的多个几何任务上同时达到最优，并且保持极高的计算效率？** 为此，作者在四个维度上进行了系统性验证：(1) 动态场景下的 4D 重建与跟踪能力，(2) 视频深度与点云估计精度，(3) 相机位姿估计的精度-速度权衡，(4) 各设计选择的因果贡献。所有实验均在公开基准上使用标准评估协议进行，速度测试统一在单张 A100 GPU 上完成，消除了硬件差异带来的偏差。

### 4D 重建与 3D 跟踪

这是 D4RT 最核心的能力验证。在 TAPVid-3D 基准上（Table 4），D4RT 在已知相机内参的设置下全面超越 **SpatialTrackerV2**（Xiao et al., ICCV 2025）。以最具挑战性的 DriveTrack 子集为例，D4RT 的 APD3D 达到 0.304，较 SpatialTrackerV2 的 0.195 提升 56%；在 ADT 和 PStudio 子集上同样保持显著优势。即便在需要同时估计相机参数的世界坐标系跟踪任务中，D4RT 仍然表现最优。

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/009_Table_4.jpg]]
*Table 4: 4D reconstruction and tracking – We evaluate 3D tracking capability on dynamic videos, with tracks predicted in both local camera coordinates (left) and world coordinates (right). Our model achieves superior performance compared to the prior state-of-the-art*

定性对比（Figure 4）揭示了更深层的差异。纯重建方法 **MegaSaM**（Li et al., CVPR 2025）和 **π³**（Wang et al., arXiv 2025）在动态场景中出现明显的失败模式：MegaSaM 将运动的天鹅重复叠加在点云中，π³ 则完全无法重建动态的花朵。**SpatialTrackerV2** 虽然能捕捉动态，但其设计仅支持从单帧追踪点，导致重建结果中存在大量间隙（如天鹅和火车背后）。D4RT 是唯一能够为视频中所有像素重建完整 4D 场景表示的方法。

### 吞吐量：18-300 倍的效率优势

效率是 D4RT 区别于迭代式方法的关键护城河。Table 3 展示了在给定 FPS 目标下各方法能处理的最大全视频 3D 轨迹数。在 60 FPS 的实时目标下，D4RT 可处理 550 条轨迹，而 SpatialTrackerV2 仅能处理 29 条——速度差距达 18 倍。当 FPS 要求放宽至 1 FPS 时，D4RT 可追踪超过 40,000 条轨迹，与其他方法的差距扩大至 300 倍。这一优势源于 D4RT 的解码器设计：每条轨迹由 T 次独立查询组成，天然支持并行化，无需迭代优化或多阶段流水线。

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/007_Table_3.jpg]]
*Table 3: 3D tracking throughput – We measure the maximum number of full-video 3D point tracks that different model can produce while maintaining a given FPS target on a single A100 GPU. Note that for D4RT, each track consists of T independent queries processed by the decoder. D4RT is 18–300× faster than others*

### 视频深度与点云估计

在 Sintel、ScanNet、Re10K 和 KITTI 四个基准上（Table 5），D4RT 的深度估计在仅尺度对齐（S）和尺度-偏移对齐（SS）两种协议下均达到顶尖水平。以 Sintel 为例，D4RT 的 AbsRel (S) 为 0.171，较 **π³** 的 0.241 降低 29%，较 **MegaSaM** 的 0.342 降低 50%。点云估计同样显著领先：L1 误差 0.768，比 π³ 的 1.139 低 33%，比 MegaSaM 的 1.531 低 50%。

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/010_Table_5.jpg]]
*Table 5: Video depth and point map estimation – Quantitative results for both video depth and point map estimation across four benchmarks. D4RT achieves top-tier performance on the depth estimation task under both scale-only (S) and scale-and-shift (SS) alignments*

### 相机位姿估计：200+ FPS 的精度-速度双优

Figure 3 的散点图直观展示了 D4RT 在相机位姿估计上的压倒性优势。在 Sintel 和 ScanNet 上，D4RT 以超过 200 FPS 的吞吐量实现最优精度（ATE 0.065），比 **VGGT**（Wang et al., CVPR 2025）快 9 倍，比 **MegaSaM** 快 100 倍，同时精度更高（Table 6）。在静态室内场景（ScanNet、Re10K）和动态室外场景（Sintel）上的一致性表现，证明该方法对场景动态性具有鲁棒性。

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/011_Table_6.jpg]]
*Table 6: Camera pose estimation – We evaluate D4RT against state-of-the-art methods on static indoor scenes (ScanNet, Re10K) and dynamic outdoor scenes (Sintel)*

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/005_Figure_3.jpg]]
*Figure 3: Pose accuracy vs. speed – We compare pose accuracy vs. throughput against recent state-of-the-art methods. Pose accuracy is 1 – error, averaged over ATE/RTE/RPE on Sintel and Scan-Net. Throughput is measured in FPS on an A100 GPU. D4RT achieves 200+ FPS pose estimation, 9× faster than VGGT, and 100× faster than MegaSaM, while delivering superior accuracy*

### 消融实验：关键设计的因果验证

消融实验系统地拆解了 D4RT 各组件的贡献：

**局部 RGB patch 嵌入**（Table 7, Figure 6）是保持细节保真度的关键。移除查询中的 9×9 局部 RGB patch 后，Sintel 深度 AbsRel (S) 从 0.302 恶化至 0.366，相机 ATE 从 0.102 上升至 0.122。Figure 6 的深度图可视化进一步表明，RGB patch 帮助模型保留细粒度细节并产生更锐利的物体边界。

**辅助损失函数**（Table 8）各自贡献明确。移除置信度损失使 ATE 增加 0.126；移除 2D 位置损失使深度 AbsRel (S) 增加 0.071。深度估计与相机位姿之间存在轻微的权衡关系，但所有辅助损失对整体性能均有正向贡献。

**编码器主干缩放**（Table 9）呈现清晰的单调提升趋势：从 ViT-B 扩展到 ViT-g，ATE 从 0.145 降至 0.078，AbsRel (S) 从 0.319 降至 0.191。这表明全局场景表示的质量是性能的上限。

**高分辨率解码策略**（Table 10, Figure 9）中，从原始分辨率提取 RGB patch 的 Config 4 获得最低的深度边缘误差（PDBE acc 降至 2.185），在不增加模型整体计算开销的前提下恢复了亚像素级细节（如发丝结构）。

### 已知局限与失败模式

尽管整体表现优异，D4RT 存在三个明确局限：(1) 编码器输入分辨率固定为 256×256，可能限制对极高频纹理的感知；(2) 长视频处理依赖分段 Umeyama 对齐，缺乏闭环优化，存在长距离漂移风险；(3) 训练数据以驾驶、室内和合成场景为主，极端环境（水下、严重遮挡）的泛化能力未经验证。这些局限在论文中均有明确讨论，而非事后推断。

### 补充图表

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/003_Table_1.jpg]]
*Table 1: Unified decoding – A diverse set of geometry-related tasks can be inferred by querying the Cartesian product of the respective entries. Note that for intrinsics and extrinsics, we only query a coarse ( h , w ) grid for faster inference*

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/004_Table_2.jpg]]
*Table 2: Model capabilities – We highlight both the tasks our model executes but also its comprehensive functionality and simple model architecture*

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/014_Table_8.jpg]]
*Table 8: Auxiliary losses – We remove auxiliary losses individually to evaluate their impact on model performance. A slight tradeoff between depth and camera estimation pose is observed, though we find that all auxiliary losses improve overall performance. Table 9. Backbone size – We examine how D4RT’s performance scales with the size of the pretrained ViT encoder backbone, evaluating video depth and camera pose estimation performance on Sintel. We observe a clear improvement as the backbone size increases from ViT-B to ViT-g*

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/015_Figure_6.jpg]]
*Figure 6: Preservation of low-level details – We ablate the effect of including local patch information into the model’s queries, visualizing the resulting depth maps on an example from the Sintel dataset. We find that the local RGB patches help preserve finegrained details and produce sharper object boundaries. Table 7. Local RGB patch – We evaluate a ViT-L model, trained with and without the appearance patch as input to the decoder, on Sintel video depth and camera pose estimation*

![[assets/figures/papers/D4RT_Efficiently_Reconstructing_Dynamic_Scenes_876123b49484/figures/018_Table_10.jpg]]
*Table 10: Quantitative impact of query density and patch fidelity – Feeding RGB patches from the high-resolution video into the decoder (Config ⃝4 ) yields significantly sharper edges in depth maps as measured by ϵaccPDBE*



## 定位与知识库关联

### 1. 核心瓶颈与因果杠杆

现有动态场景理解方法面临一个根本性瓶颈：**缺乏统一、高效的时空点查询机制**。这导致了两类系统性问题——纯几何重建方法（如 MegaSaM、VGGT、π³）无法处理动态对应关系，而专门的跟踪方法（如 SpatialTrackerV2）则依赖多阶段迭代优化，计算冗余且只能追踪稀疏的单帧点。两者都无法同时完成静态与动态场景的完整 4D 重建，任务碎片化严重。

D4RT 引入的因果杠杆是一个**基于查询的解码器接口**：将空间坐标 $(u, v)$ 与三个时间索引——源时刻 $t_{\text{src}}$、目标时刻 $t_{\text{tgt}}$、相机参考帧 $t_{\text{cam}}$——解耦并共同作为查询条件。这使得一个轻量级交叉注意力解码器能够从全局场景表示 $F = \mathcal{E}(V)$ 中独立、灵活地解码任意时空点的 3D 位置 $\mathbf{P} = \mathcal{D}(\mathbf{q}, F) \in \mathbb{R}^3$，从而将点跟踪、深度估计、点云重建与相机位姿估计统一为同一接口的不同查询模式（Table 1）。

### 2. 与基线方法的本质差异

**纯几何重建方法（MegaSaM, VGGT, DUSt3R, π³）** 的核心局限在于它们将视频帧视为独立或成对的静态快照，缺乏对动态对应关系的建模能力：
- **MegaSaM**（Zhengqi Li et al., CVPR 2025）和 **VGGT**（Jianyuan Wang et al., CVPR 2025）均采用密集的每帧解码策略，在动态场景中会产生重复的静态点云伪影（如天鹅被重复重建，Figure 4）。
- **π³**（Yifan Wang et al., arXiv 2025）虽引入置换等变性，但在动态场景中完全失效（花朵重建失败，Figure 4）。
- **DUSt3R**（Shuzhe Wang et al., CVPR 2024）仅处理成对图像，不具备视频级时序理解能力。

D4RT 通过统一的时空查询机制，天然支持动态对应关系：查询目标时刻 $t_{\text{tgt}}$ 可任意指定，使模型能追踪同一点在任意未来或过去帧中的 3D 位置，这是上述方法在架构层面无法实现的。

**3D 跟踪方法（SpatialTrackerV2）** 虽然能处理动态点，但其设计存在根本性效率瓶颈：
- **SpatialTrackerV2**（Yuxi Xiao et al., ICCV 2025）采用多阶段迭代优化，每条轨迹需要密集的帧间传播，导致吞吐量极低——在 60 FPS 目标下仅能处理 29 条轨迹，而 D4RT 可处理 550 条（Table 3），速度提升达 18–300 倍。
- 更关键的是，SpatialTrackerV2 只能追踪来自单帧的点，在重建中留下大量间隙（天鹅后方、火车后方，Figure 4），无法生成完整的 4D 场景表示。

**组合式方法（CoTracker3 + UniDepthV2）** 将 2D 跟踪与单目深度估计拼接，缺乏端到端的 3D 一致性约束。DELTA 虽支持密集长程跟踪，但其架构仍属于分离式多任务范式，无法像 D4RT 一样通过单一解码器同时输出深度、点云、相机参数和 3D 轨迹。

### 3. 知识库定位：统一查询范式的贡献

D4RT 在知识库中的核心贡献不是提出新的网络模块，而是**重新定义了动态场景理解的接口范式**：

1. **从“密集解码”到“按需查询”**：传统方法（VGGT、π³）需要为每帧的每个像素执行解码，计算量与视频长度和分辨率线性耦合。D4RT 的查询接口使每条轨迹仅需 $T$ 次独立解码器前向传播，且查询之间天然可并行。这种“查询即服务”的设计使得模型可以按需灵活分配计算资源——对于相机位姿估计仅需查询粗粒度网格（Table 1），对于密集跟踪则可自适应地仅从未访问像素发起新轨迹，实现 5–15 倍的自适应加速。

2. **时空坐标解耦的表示能力**：将 $t_{\text{src}}$、$t_{\text{tgt}}$、$t_{\text{cam}}$ 三个时间索引显式解耦是 D4RT 的关键设计选择。这不仅使模型能追踪动态点的运动轨迹（$t_{\text{src}} \neq t_{\text{tgt}}$），还支持跨相机坐标系的查询——这对于需要将局部跟踪结果对齐到世界坐标系的 4D 重建至关重要。Table 4 显示，D4RT 在世界坐标 3D 跟踪上同样大幅领先 SpatialTrackerV2。

3. **局部 RGB patch 嵌入的关键作用**：消融实验（Table 7）揭示了查询中 9×9 局部 RGB patch 嵌入的重要性——移除后深度 AbsRel (S) 从 0.302 升至 0.366，相机 ATE 从 0.102 升至 0.122。这表明解码器不仅依赖全局场景表示 $F$，还需要局部纹理信息来恢复精细几何细节（Figure 6），这一发现为未来查询式方法的设计提供了重要参考。

### 4. 适用边界与局限

尽管 D4RT 在统一性和效率上取得了显著突破，其适用边界仍需明确：

**分辨率瓶颈**：编码器输入分辨率固定为 256×256（训练时），虽然解码器支持从原图分辨率提取 RGB patch（Table 10, Config 4），但全局场景表示 $F$ 的分辨率限制了对极高频细节的直接感知。高分辨率解码实验表明，从原图提取 patch 可将深度边缘误差（PDBE acc）降至 2.185，但编码器本身的低分辨率特征可能成为进一步精细化的瓶颈。

**长视频漂移**：对于超过编码器窗口长度的视频，当前方案依赖分段预测后通过 Umeyama 算法对齐（Figure 8），未包含闭环检测与全局优化。在 KITTI 长序列测试中，D4RT 的对齐结果优于 VGGT 和 π³，但长距离累积漂移问题仍未根本解决。这是查询范式的固有局限——每个查询独立于 $F$，而 $F$ 本身受限于编码器的感受野。

**场景泛化未验证**：训练数据主要覆盖驾驶、室内和合成场景（Sintel、ScanNet、KITTI、Re10K 等），在极端环境（水下、严重遮挡、镜面反射/折射）下的泛化能力尚未经过系统验证。Table 11 显示 VideoMAE 预训练权重对性能有显著提升，暗示模型对训练数据分布仍有较强依赖。

**计算复杂度的线性增长**：虽然单条轨迹的查询是并行的，但查询范式的计算复杂度随查询数量线性增长。对于超密集重建任务（如所有像素的全视频跟踪），即使有自适应加速，极端情况下的内存和计算需求仍需关注。Table 3 中 1 FPS 目标下可处理 40,180 条轨迹，但距离“所有像素跟踪”仍有数量级差距。

### 5. 开放问题

D4RT 开启的统一查询范式引出了若干值得探索的方向：

1. **在线流式扩展**：当前模型依赖离线编码的全局表示 $F$，能否将查询机制扩展到任意长度的在线视频流，无需分割和后处理对齐？这可能需要增量式的场景表示更新机制。

2. **跨模态泛化**：查询接口的抽象性（时空坐标 + 局部特征 → 3D 位置）使其天然适合扩展到其他模态，如 LiDAR 点云查询、多传感器融合查询。能否用同一架构处理 RGB-D 或事件相机的输入？

3. **表示可解释性**：全局场景表示 $F$ 的内部结构是否具备可解释性？能否从中直接提取语义信息（如物体分割、运动边界）而不需要额外的解码头？这关系到模型是否真正“理解”了场景的动态结构。

4. **极端动态场景**：在存在大量镜面反射、折射或非刚性形变的场景中，当前查询机制（假设点在不同时刻的可见性可被建模为可见性预测）是否仍然有效？Table 8 显示可见性损失对性能有贡献，但其在极端情况下的鲁棒性尚未验证。

5. **查询效率的理论极限**：当前的自适应跟踪策略通过可见性标记避免了重复查询，但能否从信息论角度分析查询的冗余度，进一步设计主动查询选择策略，以最小查询次数实现给定精度的 4D 重建？



## 原文 PDF

![[paperPDFs/arxiv_2025/D4RT_Efficiently_Reconstructing_Dynamic_Scenes.pdf]]
