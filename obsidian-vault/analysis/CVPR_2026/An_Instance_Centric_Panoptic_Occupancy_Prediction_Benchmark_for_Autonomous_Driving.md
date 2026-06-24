---
title: An Instance-Centric Panoptic Occupancy Prediction Benchmark for Autonomous Driving
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/An_Instance_Centric_Panoptic_Occupancy_Prediction_Benchmark_for_Autonomous_Driving.pdf
project_link: "https://mias.group/CarlaOcc"
code_link: null
aliases:
- AC
- ICPOPBAD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 是否具备大规模高质量 3D 网格库，以及是否采用基于网格的物理一致场景重建与体素化策略，取代传统的 LiDAR 扫描聚合方式。
primary_logic: 通过构建统一的三维网格资源库（ADMesh）并利用网格驱动的场景重建，可生成具有任意分辨率、时空一致性和丰富实例标注的全景占用数据集（CarlaOcc），为视觉感知提供高质量监督信号和标准化评测基准。
claims:
- CarlaOcc 在空间连续性得分（0.996）和时间一致性得分（0.873）上大幅超越现有数据集。
- CarlaOcc 包含超过 10 万帧数据，支持 0.05 米的体素分辨率和实例级标注，远超其他公开数据集。
- 在 CarlaOcc 上预训练可使模型在真实数据集上的 mIoU 提升 0.8%-1.5%，证明其有效的空间推理能力。
- Occupancy Dataset Quality 上 Spatial Continuity Score (s_sc) = 0.996 (CarlaOcc)
---

# An Instance-Centric Panoptic Occupancy Prediction Benchmark for Autonomous Driving

> [!tip] 核心洞察
> 通过构建统一的三维网格资源库（ADMesh）并利用网格驱动的场景重建，可生成具有任意分辨率、时空一致性和丰富实例标注的全景占用数据集（CarlaOcc），为视觉感知提供高质量监督信号和标准化评测基准。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向自动驾驶的实例中心全景占用预测基准 |
| 英文题名 | An Instance-Centric Panoptic Occupancy Prediction Benchmark for Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.27238) · [Project](https://mias.group/CarlaOcc) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | 网格驱动的全景占用生成框架（ADMesh 与 CarlaOcc） |
| Dataset | Occupancy Dataset Quality, Panoptic Occupancy Prediction on CarlaOcc, Semantic Occupancy Prediction on CarlaOcc, Sim-to-Real Transfer |

> [!tip] 效果简介
> - Occupancy Dataset Quality 上，Spatial Continuity Score (s_sc) 0.996 (CarlaOcc) vs 0.887 (CarlaSC) (+0.109)；Temporal Consistency Score (s_tc) 0.873 (CarlaOcc) vs 0.775 (CarlaSC) (+0.098)。
> - Panoptic Occupancy Prediction on CarlaOcc 上，PQ 13.5 (Panoptic-FlashOcc) vs 10.3 (SparseOcc) (+3.2)。
> - Semantic Occupancy Prediction on CarlaOcc (0.5m voxel) 上，mIoU 20.7 (GaussianFormer2) vs 14.4 (SparseOcc) (+6.3)。

## 概述

### 问题背景

3D 占用预测已成为自动驾驶感知的核心任务之一，旨在从传感器输入中重建场景的完整三维几何与语义信息。然而，现有公开的占用数据集普遍存在三个根本性瓶颈：**缺乏实例级标注**，无法支撑全景场景理解；**物理一致性差**，基于 LiDAR 扫描聚合与泊松表面重建的真值生成方式导致几何不完整、语义碎片化；**分辨率固定**，通常限制在 0.2–0.5 米，难以满足精细感知需求。这些缺陷直接制约了视觉感知模型的空间推理能力与下游任务性能。

### 核心思路

本文提出了一套以**实例为中心**的全景占用预测基准，核心创新在于用**网格驱动的场景重建**取代传统的点云聚合范式。具体而言，工作包含两个紧密耦合的组成部分：

- **ADMesh**：首个面向自动驾驶的大规模、语义结构化 3D 网格库，整合超过 15,000 个高质量三维模型，覆盖丰富的纹理与语义标注。
- **CarlaOcc**：基于 ADMesh 构建的多模态、高保真全景占用数据集，包含超过 10 万帧训练数据，支持**0.05 米**的体素分辨率，每体素携带语义与实例标识，同时提供深度图、表面法线图等多模态监督信号。

这一设计的关键因果机制在于：拥有大规模高质量 3D 网格资源后，可通过网格直接重建每一帧场景，从根本上避免了 LiDAR 稀疏采样导致的几何缺失与语义不一致问题，从而生成任意分辨率、时空连续且物理准确的占用真值。

### 方法定位

在方法谱系中，CarlaOcc 并非提出新的占用预测模型，而是为现有及未来的感知方法提供**高质量的监督信号与标准化评测平台**。论文在 CarlaOcc 上系统评估了多类代表性基线：全景占用预测方面包括 **SparseOcc**（Liu et al., ECCV 2024）和 **Panoptic-FlashOcc**（Yu et al., arXiv 2024）；语义占用预测方面包括 **Symphonies**（Jiang et al., CVPR 2024）、**GaussianFormer2**（Huang et al., CVPR 2025）和 **OPUS**（Wang et al., arXiv 2024）。与现有数据集（如 Occ3D-nuScenes、CarlaSC）相比，CarlaOcc 在真值生成方式、体素分辨率、实例标注三个关键维度上实现了系统性升级。

### 主要结果

实验从数据集质量、基准性能与迁移能力三个层面验证了 CarlaOcc 的有效性：

- **数据集质量**：CarlaOcc 的空间连续性得分 $s_{sc}$ 达到 0.996，时间一致性得分 $s_{tc}$ 达到 0.873，分别比 CarlaSC 高出 0.109 和 0.098（Table 3），表明其占用标签在几何完整性与时序稳定性上显著优于现有数据集。
- **基准性能**：在 CarlaOcc 上，Panoptic-FlashOcc 的全景质量（PQ）达到 13.5，领先 SparseOcc 3.2 个百分点（Table 4）；GaussianFormer2 在 0.5 米体素分辨率下的语义 mIoU 达到 20.7，领先 SparseOcc 6.3 个百分点（Table 5）。
- **Sim-to-Real 迁移**：在 CarlaOcc 上预训练后，Symphonies 在 KITTI-360 上的 mIoU 从 15.9 提升至 17.4（+1.5%），且 SparseOcc 的实例轮廓完整性明显改善（Table 7, Figure 12），验证了合成数据中学习到的空间推理能力可部分迁移至真实场景。

消融实验进一步揭示，体素分辨率对预测性能影响显著：0.05 米分辨率下的 IoU 比 0.5 米低约 17–20 个百分点（Table 6），表明细粒度占用预测仍是开放挑战。

### 局限与展望

CarlaOcc 的主要局限在于其基于 CARLA 模拟器生成，8 个城镇的环境多样性有限，Sim-to-Real 迁移增益目前仅 0.8%–1.5% mIoU，且尚未在全景占用等更复杂任务上验证迁移效果。实例标注质量依赖于网格资产精细度与骨架运动估计算法的准确性。未来方向包括：在 ≤0.05 米分辨率下提升全景占用预测效率、利用实例级标签设计新型视觉预训练任务，以及探索多模态数据对自监督学习的支撑潜力。

## 背景与动机

### 3D 占用预测的演进与瓶颈

3D 占用预测旨在从视觉输入中重建场景的完整三维几何与语义表示，是自动驾驶感知栈中的关键一环。近年来，该领域在数据集构建和模型设计上取得了显著进展，但其核心瓶颈已从“能否预测占用”转向“占用标注本身是否足够精确、完整且具备实例级语义”。现有公开数据集普遍存在三个结构性缺陷：

1. **缺乏实例级标注**：主流数据集仅提供语义占用标签，无法区分同一语义类别下的不同个体，这直接阻断了全景场景理解与实例感知下游任务的发展。
2. **物理一致性与几何完整性差**：真值生成多依赖 LiDAR 扫描聚合与泊松表面重建，导致标注在空间上存在孤立体素、碎片化区域，在时间上缺乏跨帧一致性。
3. **分辨率固定且粗糙**：体素尺寸通常锁定在 0.2–0.5 米，无法支撑细粒度的几何推理，也难以适配不同感知任务对空间粒度的差异化需求。

这三个缺陷相互耦合：LiDAR 聚合的稀疏性导致几何不完整，几何不完整使实例分割困难，而缺乏实例信息又进一步限制了标注的语义精度。因此，突破这一瓶颈的关键不在于设计更强的预测模型，而在于**重构真值生成的底层范式**。

### 现有数据集的局限性

从数据规模与标注质量两个维度审视，现有公开数据集存在明显落差。以 Occ3D-nuScenes 和 KITTI-360-SSCBench 为代表的真实场景数据集，虽然提供了基于 LiDAR 的语义占用标签，但其体素分辨率粗（≥0.2 米）、感知范围有限，且完全缺失实例标注。CarlaSC 等合成数据集虽具备稠密真值，但其基于 LiDAR 模拟的聚合策略仍会引入空间不连续和时间抖动。**Table 2** 的系统对比揭示了一个清晰的事实：在“实例标注”“多分辨率支持”“感知范围”三个关键维度上，现有数据集均为空白。

更根本的问题在于，LiDAR 扫描聚合的范式本身存在不可逾越的天花板——它只能从离散采样点推断连续表面，注定无法产生物理一致、拓扑完整的占用表示。这构成了该领域的**因果调节旋钮**：是否具备大规模高质量 3D 网格库，以及是否采用基于网格的物理一致场景重建与体素化策略，决定了真值质量的上限。

### 本文动机

上述分析指向一个明确的动机：**构建一个以实例为中心、物理一致、支持任意分辨率的全景占用预测基准**。这需要从两个层面同时发力：

- **资源层**：建立大规模、语义结构化的 3D 网格库，为场景重建提供高质量的几何基元。本文提出的 ADMesh 整合了来自 BuildingNet、Mesh-Fleet、ShapeNetCore 等多个来源的超过 15,000 个高精度 3D 模型，覆盖丰富的纹理与语义标注（**Table 1**），从根本上解决了网格资源匮乏的问题。
- **生成层**：设计一套网格驱动的场景重建与体素化流程，取代传统的 LiDAR 聚合方式。通过直接利用网格进行物理一致的重建，CarlaOcc 能够生成具有空间连续性、时间一致性和实例级标注的全景占用真值，且体素分辨率可低至 0.05 米。

这一双轮驱动的设计使得 CarlaOcc 在数据质量指标上实现了质的飞跃：空间连续性得分达到 0.996，时间一致性得分达到 0.873，远超现有数据集（**Table 3**）。更重要的是，该基准不仅服务于占用预测任务本身的评测，还通过 Sim-to-Real 预训练实验证明了其作为视觉表征学习平台的价值——在 CarlaOcc 上预训练可使模型在真实数据集上的 mIoU 提升 0.8%–1.5%（**Table 7**），验证了其有效的空间推理能力迁移。

## 核心创新

本工作的核心创新并非提出一种新的感知模型架构，而是构建了一套**以实例为中心的数据生成范式**，从根本上解决了现有 3D 占用数据集在标注质量、物理一致性和实例粒度上的结构性缺陷。其创新链条可概括为“资产先行—网格驱动重建—拓扑感知体素化”三步走策略。

### 创新一：从稀疏点云到网格驱动的真值生成

传统占用数据集（如 Occ3D-nuScenes、KITTI-360-SSCBench）的真值生成依赖 LiDAR 扫描聚合与泊松表面重建，存在三个固有瓶颈：体素分辨率固定（通常 0.2–0.5 m）、几何不完整（稀疏扫描导致空洞与碎片化）、且完全缺失实例级标注。本工作将真值生成的“因果旋钮”从传感器数据后处理前移至**基于 3D 网格资源的物理一致场景重建**（Figure 2）。

具体而言，作者首先构建了 **ADMesh**——面向自动驾驶的首个大规模语义结构化 3D 网格库（整合 CARLA 原生资产、BuildingNet、Mesh-Fleet 和 ShapeNetCore，总计超过 15,000 个高质量模型，Table 1）。在每一帧仿真数据中，直接利用 ADMesh 中的静态网格和动态动画序列重建完整的场景几何，而非依赖稀疏 LiDAR 点采样。这一范式转换带来了三个关键改变：

| 改变维度 | 基线方案 | 本工作 | 证据锚点 |
|---------|---------|--------|---------|
| 真值生成方式 | LiDAR 扫描聚合 + 泊松重建 | 网格驱动的物理一致场景重建 | Section 3.2 |
| 体素分辨率 | 固定 0.2–0.5 m | 可低至 0.05 m，支持多分辨率 | Table 2 |
| 实例级标注 | 无 | 有，30 个语义类别，每体素携带语义与实例标识 | Table 2 |

### 创新二：非刚体动态建模与骨架运动分析

动态场景中的行人等非刚体对象是占用预测的难点。现有仿真数据集通常直接使用 CARLA 引擎的骨骼动画输出，缺乏对步态相位的精细化建模。本工作引入**骨架运动分析器（Skeletal Motion Analyzer）**，通过步态周期匹配重建行人的动态网格姿态：

$$d_k = \arg\min_d \mathcal{G}(\delta_k, \delta_d)$$

该公式通过测地线距离匹配当前帧的行人步态描述子 $\delta_k$ 与模板步态描述子 $\delta_d$，估计瞬时步态相位 $d_k$，从而选择对应的模板网格。这一机制确保了非刚体对象在时间维度上的运动连续性和几何一致性（Section 3.2, Appendix A.2）。

### 创新三：拓扑感知体素化与传感器伪影校正

将场景网格转化为体素标签时，直接光栅化容易产生语义重叠和深度歧义。本工作提出**拓扑感知网格排列策略（Topology-aware Mesh Permutation）**：按空间高程对网格进行排序并逐层集成，生成无重叠、物理合理的全景占用体素标签（Section 3.2）。

此外，针对透明物体（如车窗、建筑玻璃）导致的传感器深度和语义错误，设计了**实例引导的传感器伪影校正（Instance-Guided Rectification）**。核心操作为：

$$\hat{\mathbf{D}}(u,v) = \min\big( \mathbf{D}_{\mathrm{raw}}(u,v), \mathbf{D}_{\mathrm{rc}}(u,v) \big)$$

将传感器原始深度图 $\mathbf{D}_{\mathrm{raw}}$ 与射线投射深度图 $\mathbf{D}_{\mathrm{rc}}$ 逐像素取最小值，修复透明物体穿透导致的深度高估和语义错标（Appendix A.3, Figure 5）。

### 创新四：数据集质量度量体系

为量化评估占用标注的质量，本工作提出了两个新型度量指标：

- **空间连续性得分（Spatial Continuity Score）**：衡量同一语义类别体素的空间聚合度，惩罚孤立和碎片化体素：

$$s_{sc} = 1 - \frac{\sum_{t=1}^T \sum_{c=1}^C |\mathcal{T}_t^{(c)}|}{\sum_{t=1}^T \sum_{c=1}^C |\mathcal{V}_t^{(c)}|}$$

其中 $\mathcal{T}_t^{(c)}$ 为第 $t$ 帧中类别 $c$ 的孤立体素集合（6-邻域内无同类体素），$\mathcal{V}_t^{(c)}$ 为该类别的全部占用体素。

- **时间一致性得分（Temporal Consistency Score）**：通过帧间语义交并比评估占用标注的时间稳定性，排除动态目标和新可见区域的影响：

$$s_{tc} = \frac{\sum_{t=1}^{T-1} \sum_{c=1}^C |\widetilde{\mathcal{V}}_t^{(c)} \cap \mathcal{V}_t^{(c)} \cap M_t|}{\sum_{t=1}^{T-1} \sum_{c=1}^C |\widetilde{\mathcal{V}}_t^{(c)} \cup \mathcal{V}_t^{(c)} \cap M_t|}$$

在 CarlaOcc 上，$s_{sc}$ 达到 0.996，$s_{tc}$ 达到 0.873，分别超出基线 CarlaSC 0.109 和 0.098（Table 3），验证了网格驱动真值生成在物理一致性上的显著优势。

### 创新边界与局限

上述创新的有效性受限于以下条件：（1）实例标注质量依赖于 ADMesh 网格资产的精细度和骨架运动估计算法的准确性，在长尾、复杂交互场景下可能出现伪影；（2）基于 CARLA 模拟器的数据无法完全替代真实传感器采集样本，sim-to-real 迁移带来的性能增益有限（0.8%–1.5% mIoU，Table 7）；（3）目前仅在语义占用任务上验证了迁移效果，全景占用等下游任务的 sim-to-real 增益尚未被系统评估。

## 整体框架

本文提出了一种以实例为中心的全景占用预测基准，其核心由两大组件构成：**ADMesh**——面向自动驾驶的大规模语义结构化三维网格库，以及 **CarlaOcc**——基于网格驱动场景重建生成的高保真全景占用数据集。Figure 1 展示了该基准的总体框架。

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the proposed benchmark. ADMesh provides the first large-scale, semantically structured 3D mesh library for autonomous driving. CarlaOcc leverages these assets to construct a multi-modal, high-fidelity, and physically consistent panoptic occupancy dataset, featuring variable voxel resolutions and rich instance-level annotations for comprehensive 3D perception benchmarking*

### 核心瓶颈与设计动机

现有 3D 占用数据集普遍存在三大缺陷：缺乏实例级标注、物理一致性差（源于 LiDAR 扫描聚合与泊松表面重建的体素化流程）、几何不完整且分辨率固定。这些问题直接限制了高精度全景场景理解的发展。本文的因果调控变量在于：**是否具备大规模高质量 3D 网格库**，以及**是否采用基于网格的物理一致场景重建与体素化策略**来替代传统 LiDAR 聚合方式。

### 数据生成 Pipeline

Figure 2 完整呈现了从网格资产到全景占用标签的生成流程，包含四个关键模块：

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the proposed ADMesh library and the CarlaOcc generation pipeline. The ADMesh library is constructed by extracting and organizing diverse 3D assets from multiple sources, which are subsequently used to reconstruct dynamic scenes with both static structures and temporally aligned non-rigid motions. The resulting unified scene meshes are then used to rectify sensor artifacts and further processed with a topology-aware mesh permutation strategy to produce non-overlapping panoptic occupancy labels*

1.  **网格导出工具链 (Mesh Exportation Toolchain)**：从 CARLA 模拟器中自动遍历所有默认场景，系统性提取、重建并组织静态网格资源，构建组件级网格库 ADMesh。该库整合了来自 BuildingNet、Mesh-Fleet、ShapeNetCore 等多个来源的超过 15,000 个高质量三维模型（Table 1），涵盖丰富的语义类别与纹理多样性。

2.  **骨架运动分析器 (Skeletal Motion Analyzer)**：针对行人等非刚体对象，通过步态周期匹配重建动态网格姿态。具体而言，利用测地线距离最小化当前步态描述子 $\delta_k$ 与模板步态描述子 $\delta_d$ 的差异 $d_k = \arg\min_d \mathcal{G}(\delta_k, \delta_d)$，估计瞬时步态相位以选择对应的模板网格，实现时间对齐的非刚体运动重建。

3.  **拓扑感知网格排列策略 (Topology-aware Mesh Permutation)**：将静态背景网格、刚体前景网格与非刚体前景网格在统一世界坐标系下组装为帧级全景场景网格 $\mathcal{M}^{\mathrm{pano}}$，随后按空间高程排序并逐层集成，生成无重叠、物理合理的全景占用体素标签。该策略从根本上避免了传统方法中因点云稀疏和表面重建导致的几何不完整与语义错误。

4.  **实例引导的传感器伪影校正 (Instance-Guided Rectification)**：利用射线投射深度图 $\mathbf{D}_{\mathrm{rc}}$ 与传感器原始深度图 $\mathbf{D}_{\mathrm{raw}}$ 逐像素取最小值 $\hat{\mathbf{D}}(u,v) = \min(\mathbf{D}_{\mathrm{raw}}(u,v), \mathbf{D}_{\mathrm{rc}}(u,v))$，修复透明物体（如车窗、建筑玻璃）导致的深度和语义错误，恢复数据一致性（Figure 5）。

### 输入输出流

-   **输入**：CARLA 模拟器中的城镇场景、传感器配置（多视角 RGB 相机、LiDAR、深度传感器等，见 Figure 6）以及 ADMesh 网格库中的静态与动态资产。
-   **输出**：多模态、多分辨率的全景占用数据集 CarlaOcc，包含超过 10 万帧训练数据，每帧提供实例级语义占用标签（30 个语义类别）、深度图、表面法线图、语义分割图等模态（Figure 4、Figure 8），支持 0.05 m 至 0.5 m 的可变体素分辨率（Figure 7）。

### 质量评估体系

为量化数据集标注质量，本文提出两项新指标：
-   **空间连续性得分** $s_{sc} = 1 - \frac{\sum_{t=1}^T \sum_{c=1}^C |\mathcal{T}_t^{(c)}|}{\sum_{t=1}^T \sum_{c=1}^C |\mathcal{V}_t^{(c)}|}$，衡量语义占用标签中同类体素的空间连续性，避免孤立和碎片化标注。
-   **时间一致性得分** $s_{tc}$，通过帧间语义交并比评估占用标注的时间稳定性，排除动态目标和新可见区域的影响。

CarlaOcc 在空间连续性得分（0.996）和时间一致性得分（0.873）上大幅超越现有数据集（Table 3），验证了网格驱动生成策略的物理一致性与几何完整性优势。

## 核心模块与公式推导

### 3.1 ADMesh 网格资源库构建

CarlaOcc 的真值生成能力根植于 **ADMesh**——一个面向自动驾驶的大规模语义结构化三维网格库。其构建依赖一套自动化网格导出工具链（Mesh Exportation Toolchain），该工具链遍历 CARLA 默认场景，系统性地提取、重建并组织三维资产，最终汇聚了来自 BuildingNet、Mesh-Fleet 和 ShapeNetCore 等来源的超过 15,000 个高质量三维模型（Table 1）。这些模型携带丰富的纹理与语义标注，为后续的物理一致场景重建提供了统一的几何基底。

### 3.2 网格驱动的全景场景重建

CarlaOcc 的核心创新在于用网格驱动的场景重建取代了传统 LiDAR 扫描聚合方式。其管道由四个关键模块串联构成：

**背景网格筛选**。在每帧中，以 LiDAR 传感器为锚点定义占用感兴趣区域 $\mathcal{R}$，筛选与该区域存在空间交集的静态背景网格：

$$S_{\mathrm{bg}} = \{ (\mathcal{M}_i, \mathbf{T}_i) \in \mathcal{S} \mid \mathbf{T}_l^{-1} \mathbf{T}_i (\mathcal{M}_i) \cap \mathcal{R} \neq \emptyset \}$$

其中 $\mathcal{S}$ 为场景静态网格集合，$\mathbf{T}_l$ 为 LiDAR 坐标系到世界坐标系的变换矩阵。该筛选大幅减少了每帧需要处理的网格数量。

**骨架运动分析器（Skeletal Motion Analyzer）**。针对行人等非刚体对象，该模块通过步态周期匹配重建动态网格姿态。具体而言，从骨架关键点中提取步态描述子 $\delta_k$，与预构建的规范行走周期模板 $\delta_d$ 进行测地线距离匹配：

$$d_k = \arg \min_d \mathcal{G}(\delta_k, \delta_d)$$

该公式通过最小化观测描述子与模板描述子之间的测地线差异，估计当前瞬时步态相位 $d_k$，从而选择对应的模板网格姿态。

**全景场景网格装配**。将背景、刚体前景和非刚体前景三类网格在世界坐标系下统一整合，形成帧级全景场景网格：

$$\mathcal{M}^{\mathrm{pano}} = \{ (\mathbf{T}(\mathcal{M}), p) \mid (\mathcal{M}, \mathbf{T}) \in \mathcal{S}_{\mathrm{bg}} \cup \mathcal{S}_{\mathrm{fg}}^{\mathrm{r}} \cup \mathcal{S}_{\mathrm{fg}}^{\mathrm{n}} \}$$

其中 $p$ 为每个网格面片的全景标签（语义类别与实例标识）。

**实例引导的传感器伪影校正（Instance-Guided Rectification）**。CARLA 传感器在渲染透明物体（如车窗、建筑玻璃）时会产生错误的深度和语义值。该模块利用已装配的全景网格进行射线投射（ray casting），生成物理正确的深度图 $\mathbf{D}_{\mathrm{rc}}$，并与原始传感器深度图逐像素取最小值：

$$\hat{\mathbf{D}}(u,v) = \min\big( \mathbf{D}_{\mathrm{raw}}(u,v), \mathbf{D}_{\mathrm{rc}}(u,v) \big)$$

此操作有效修复了透明表面后方的深度错误，同时利用实例网格的语义信息校正对应像素的语义标签（Figure 5）。

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/007_Figure_5.jpg]]
*Figure 5: Visualizations of instance-guided rectification of sensor artifacts: (a) RGB images; (b) and (d) the rendered depth and semantic maps from CARLA; (c) and (e) the corresponding refined results. Regions with incorrect semantics or depth values caused by transparency are highlighted in red, while the instances that lose their categorical labels are highlighted in blue*

### 3.3 拓扑感知体素化

获得全景场景网格后，CarlaOcc 采用拓扑感知的网格排列策略（Topology-aware Mesh Permutation）生成无重叠的体素占用标签。该策略按空间高程对网格进行排序，逐层集成，确保地面、建筑、植被等类别在垂直方向上的物理合理性。由于体素化直接作用于完整的三维网格，CarlaOcc 可支持从 0.05 米到 0.5 米的任意分辨率输出（Figure 7），这是传统基于稀疏点云的方法无法实现的。

### 3.4 数据集质量度量公式

为量化占用标注的物理一致性，本文提出了两个核心评估指标。

**空间连续性得分（Spatial Continuity Score）**。首先定义孤立体素集合——在 6-邻域内无同类体素的占用体素：

$$\mathcal{T}_t^{(c)} = \{ v \in \mathcal{V}_t^{(c)} \mid \forall u \in \mathcal{N}(v), \mathbf{O}(u) \neq c \}$$

其中 $\mathcal{V}_t^{(c)}$ 为第 $t$ 帧中类别 $c$ 的所有占用体素，$\mathcal{N}(v)$ 为体素 $v$ 的 6-邻域。空间连续性得分定义为非孤立体素在所有类别上的占比：

$$s_{sc} = 1 - \frac{\sum_{t=1}^T \sum_{c=1}^C |\mathcal{T}_t^{(c)}|}{\sum_{t=1}^T \sum_{c=1}^C |\mathcal{V}_t^{(c)}|}$$

$s_{sc}$ 越接近 1，说明语义占用标签越连续，碎片化程度越低。CarlaOcc 在该指标上达到 0.996，远超 CarlaSC 的 0.887（Table 3）。

**时间一致性得分（Temporal Consistency Score）**。通过帧间语义交并比评估标注的时间稳定性：

$$s_{tc} = \frac{\sum_{t=1}^{T-1} \sum_{c=1}^C |\widetilde{\mathcal{V}}_t^{(c)} \cap \mathcal{V}_t^{(c)} \cap M_t|}{\sum_{t=1}^{T-1} \sum_{c=1}^C |\widetilde{\mathcal{V}}_t^{(c)} \cup \mathcal{V}_t^{(c)} \cap M_t|}$$

其中 $\widetilde{\mathcal{V}}_t^{(c)}$ 为第 $t+1$ 帧的占用标签经自车运动补偿后投影到第 $t$ 帧坐标系的结果，$M_t$ 为掩码，用于排除动态目标和新可见区域。CarlaOcc 在该指标上达到 0.873，显著优于 CarlaSC 的 0.775，验证了网格驱动重建在时间维度上的优势。

## 实验与分析

### 数据集质量评估

为量化占用标注的物理一致性，本文提出两个专用质量指标：**空间连续性得分**（Spatial Continuity Score, $s_{sc}$）和**时间一致性得分**（Temporal Consistency Score, $s_{tc}$）。

空间连续性得分衡量同一语义类别体素的空间连贯性，核心思想是统计孤立体素（6-邻域内无同类体素）在全部体素中的占比：

$$s_{sc} = 1 - \frac{\sum_{t=1}^T \sum_{c=1}^C |\mathcal{T}_t^{(c)}|}{\sum_{t=1}^T \sum_{c=1}^C |\mathcal{V}_t^{(c)}|}$$

其中 $\mathcal{T}_t^{(c)}$ 为第 $t$ 帧中类别 $c$ 的孤立体素集合，$\mathcal{V}_t^{(c)}$ 为该类别的全部占据体素。分数越接近 1，标注的空间连续性越好。

时间一致性得分通过帧间语义交并比评估标注的时间稳定性，排除动态目标和新可见区域的影响：

$$s_{tc} = \frac{\sum_{t=1}^{T-1} \sum_{c=1}^C |\widetilde{\mathcal{V}}_t^{(c)} \cap \mathcal{V}_t^{(c)} \cap M_t|}{\sum_{t=1}^{T-1} \sum_{c=1}^C |\widetilde{\mathcal{V}}_t^{(c)} \cup \mathcal{V}_t^{(c)} \cap M_t|}$$

其中 $\widetilde{\mathcal{V}}_t^{(c)}$ 是将第 $t+1$ 帧的标注通过自车运动变换到第 $t$ 帧坐标系后的结果，$M_t$ 为有效掩码区域。

如 Table 3 所示，CarlaOcc 在两项指标上均大幅领先现有数据集：空间连续性得分达到 **0.996**（对比 CarlaSC 的 0.887），时间一致性得分达到 **0.873**（对比 CarlaSC 的 0.775）。这一优势源于网格驱动的场景重建策略——直接使用完整的 3D 网格进行体素化，避免了 LiDAR 扫描聚合引入的稀疏性和噪声。

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/008_Table_3.jpg]]
*Table 3: Comparison between CarlaOcc and other public occupancy prediction datasets on occupancy quality metrics*

### 全景占用预测基准

在 CarlaOcc 上评估了两个全景占用预测基线方法：**SparseOcc**（Liu et al., ECCV 2024）和 **Panoptic-FlashOcc**（Yu et al., arXiv 2024）。Table 4 的结果显示，Panoptic-FlashOcc 以 **13.5 PQ** 优于 SparseOcc 的 10.3 PQ，在分割质量（SQ: 49.1 vs 48.8）和识别质量（RQ: 27.5 vs 21.1）上均有提升。然而，两者的 PQ 绝对值均较低，表明在 0.5m 体素分辨率下的全景占用预测仍极具挑战性——尤其是实例识别（RQ）是主要瓶颈。

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/009_Table_4.jpg]]
*Table 4: Comparison of panoptic occupancy prediction methods on the CarlaOcc dataset*

### 语义占用预测基准

在语义占用预测任务上，本文评估了 **SparseOcc**、**Symphonies**（Jiang et al., CVPR 2024）、**GaussianFormer2**（Huang et al., CVPR 2025）和 **OPUS**（Wang et al., arXiv 2024）四个代表性方法。Table 5 和 Table 8 的结果表明，在 0.5m 体素分辨率下，GaussianFormer2 以 **20.7 mIoU** 取得最优性能，显著优于 SparseOcc 的 14.4 mIoU。值得注意的是，所有方法的 mIoU 值普遍偏低，揭示出 CarlaOcc 丰富的语义类别（30 类）和完整的几何标注对现有方法构成严峻挑战。

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/010_Table_5.jpg]]
*Table 5: Comparison of semantic occupancy prediction methods on the CarlaOcc dataset*

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/019_Table_8.jpg]]
*Table 8: Semantic occupancy prediction results on the CarlaOcc dataset*

### 体素分辨率消融实验

为探究体素尺寸对预测性能的影响，Table 6 展示了在 0.5m、0.1m 和 0.05m 三种分辨率下的语义占用预测结果。关键发现是：**体素分辨率从 0.5m 提升至 0.05m 时，IoU 下降约 17-20 个百分点**。以 SparseOcc 为例，其 IoU 从 0.5m 下的 14.4 骤降至 0.05m 下的约 -3（负值表明模型预测精度低于随机猜测水平）。这一结果揭示了细粒度占用预测的巨大挑战：更高分辨率意味着体素数量呈立方级增长，且需要更精确的空间定位能力。当前基于视觉的方法在 0.05m 尺度下几乎失效，亟需新的模型架构或训练策略。

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/016_Table_6.jpg]]
*Table 6: Ablation study on voxel size for semantic occupancy prediction on the CarlaOcc dataset*

### Sim-to-Real 迁移实验

为验证 CarlaOcc 作为预训练数据集的实用价值，Table 7 展示了在 CarlaOcc 上预训练后在真实数据集（KITTI-360、SemanticKITTI）上微调的结果。Symphonies 在 KITTI-360 上经过 CarlaOcc 预训练后，mIoU 从 15.9 提升至 **17.4**（+1.5）；SparseOcc 在 SemanticKITTI 上获得 0.8 mIoU 的提升。Figure 12 的定性结果显示，经 CarlaOcc 预训练的 SparseOcc 在真实场景中展现出更完整的实例轮廓（见黄色圆圈标注区域），表明合成数据中物理一致的几何监督有助于模型学习更鲁棒的空间推理能力。

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/017_Table_7.jpg]]
*Table 7: Sim-to-real evaluation results of representative baselines pretrained on CarlaOcc and finetuned on real-world datasets*

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/021_Figure_12.jpg]]
*Figure 12: Visualizations of sim-to-real experiment. As shown in yellow circles, SparseOcc exhibits more complete instance contours after pretraining on CarlaOcc compared to official results*

然而，Sim-to-Real 迁移的性能增益有限（0.8%-1.5% mIoU），主要受限于以下因素：（1）真实数据集真值的稀疏性和噪声；（2）CarlaOcc 与目标数据集在传感器配置、场景分布上的差异；（3）当前仅验证了语义占用任务，全景占用的迁移效果尚未评估。

### 深度估计基准

Table 9 展示了在 CarlaOcc 上的深度估计基准结果。由于 CarlaOcc 提供了基于网格渲染的高精度深度真值（无 LiDAR 噪声和遮挡伪影），该基准可更准确地评估单目深度估计方法的几何推理能力。具体数值需查阅原文表格。

### 失败模式与局限性

综合实验分析，当前方法在 CarlaOcc 上的主要失败模式包括：

1. **细粒度分辨率的退化**：在 0.05m 体素下，所有方法的性能急剧下降，表明现有模型缺乏处理高分辨率空间推理的能力。
2. **实例识别困难**：全景占用预测中 RQ 指标普遍偏低，反映模型难以在密集的三维空间中准确区分不同实例，尤其是小目标和部分遮挡的物体。
3. **Sim-to-Real 迁移瓶颈**：尽管 CarlaOcc 预训练带来一致但有限的提升，真实场景中的域差异（纹理、光照、传感器噪声）仍然是主要障碍。实例标注的质量依赖于网格资产的精细度和骨架运动估计的准确性，对于复杂交互场景可能存在偏差。

### 补充图表

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/004_Table_2.jpg]]
*Table 2: Comparison between CarlaOcc and other public occupancy prediction datasets*

![[assets/figures/papers/paper_list_l814_https_arxiv_org_abs_2603_27238/figures/002_Table_1.jpg]]
*Table 1: Overview of data sources and statistics of ADMesh*

## 方法谱系与知识库定位

### 1. 问题瓶颈与核心因果杠杆

现有 3D 占用预测数据集（如 Occ3D-nuScenes、KITTI-360-SSCBench、CarlaSC）普遍存在三个结构性缺陷：**缺乏实例级标注**，无法支撑全景场景理解；**物理一致性差**，真值依赖 LiDAR 扫描聚合与泊松表面重建，导致几何不完整与语义碎片化；**体素分辨率固定**（通常 0.2–0.5 米），难以适应细粒度感知需求。这些瓶颈直接限制了视觉感知模型的空间推理能力上限。

本工作的核心因果杠杆在于：**是否具备大规模高质量 3D 网格库，以及是否采用基于网格的物理一致场景重建与体素化策略，取代传统的 LiDAR 扫描聚合方式**。这一杠杆的扭动同时解决了上述三个缺陷——网格资产天然携带实例标识，网格驱动的场景重建保证了物理一致性，而网格到体素的转换过程支持任意分辨率输出。

### 2. 关键方法槽位对比

本文提出的网格驱动全景占用生成框架在三个关键方法槽位上与现有基线形成系统性差异：

| 方法槽位 | 基线方案 | 本文方案 | 证据锚点 |
|---------|---------|---------|---------|
| **真值生成方式** | 基于 LiDAR 扫描聚合与泊松表面重建的体素化 | 基于 3D 网格资源的物理一致场景重建与拓扑感知体素化 | Section 3.2 |
| **体素分辨率** | 固定 0.2–0.5 米 | 可低至 0.05 米，支持多分辨率 | Table 2 |
| **实例级标注** | 无 | 有，涵盖 30 个语义类别，每体素携带语义与实例标识 | Table 2 |

真值生成方式的转变是根本性的：传统方法从稀疏点云反推几何表面，不可避免地引入空洞和噪声；本文方法直接从完整的网格场景出发进行体素化，并通过拓扑感知网格排列策略（按空间高程排序、逐层集成）消除重叠伪影，辅以实例引导的传感器伪影校正（利用射线投射修复透明物体导致的深度和语义错误），最终生成无重叠、物理合理的全景占用标签。

### 3. 方法谱系定位

本文工作处于**模拟器驱动的数据集构建**与**全景占用预测基准**的交叉节点。

**上游依赖**：
- **CARLA 模拟器**：提供基础场景与传感器仿真能力。
- **外部 3D 网格资源**：BuildingNet、Mesh-Fleet、ShapeNetCore 等，合计超过 15,000 个高质量模型（Table 1），构成 ADMesh 网格库的核心资产。
- **网格导出工具链**（Section 3.1）：从 CARLA 环境中自动提取、重建并组织静态网格资源，构建组件级网格库。

**下游基线覆盖**：
- 全景占用预测：**SparseOcc**（Liu et al., ECCV 2024）、**Panoptic-FlashOcc**（Yu et al., arXiv 2024）
- 语义占用预测：**Symphonies**（Jiang et al., CVPR 2024）、**GaussianFormer2**（Huang et al., CVPR 2025）、**OPUS**（Wang et al., arXiv 2024）

CarlaOcc 为这些方法提供了首个具备实例级标注的全景占用评测基准。在 0.5 米体素分辨率下，Panoptic-FlashOcc 取得 PQ 13.5，GaussianFormer2 取得 mIoU 20.7，均显著优于 SparseOcc 的 PQ 10.3 和 mIoU 14.4（Table 4, Table 5），但绝对性能仍处于较低水平，揭示全景占用预测任务本身的巨大挑战空间。

**与 CarlaSC 的关系**：CarlaSC 同样是基于 CARLA 的语义占用数据集，但采用传统 LiDAR 聚合方式生成真值。CarlaOcc 在空间连续性得分（0.996 vs. 0.887）和时间一致性得分（0.873 vs. 0.775）上大幅超越 CarlaSC（Table 3），验证了网格驱动重建策略在真值质量上的决定性优势。

### 4. 适用边界与局限

**适用边界**：
- 数据集基于 CARLA 模拟器的 8 个城镇环境生成，场景多样性受限于模拟器内置地图，无法完全覆盖真实世界的长尾分布。
- 实例级标签的质量依赖于网格资产的精细度以及骨架运动估计算法（步态相位匹配）的准确性，对于复杂交互场景（如人群密集、遮挡严重）可能存在伪影。
- Sim-to-real 迁移实验目前仅验证了语义占用任务（mIoU 提升 0.8%–1.5%，Table 7），全景占用及其他下游任务的实际迁移增益尚未被系统评估。

**性能增益的局限性**：CarlaOcc 预训练在真实数据集（KITTI-360）上带来的 mIoU 提升有限（0.8%–1.5%），主要受限于：真实世界真值的稀疏性与噪声、CarlaOcc 与目标数据集之间的传感器配置差异、以及模拟到真实领域的固有分布偏移。Figure 12 的定性结果显示预训练后实例轮廓更完整，但定量增益的幅度表明网格驱动真值的监督信号尚未被现有模型架构充分利用。

**体素分辨率的挑战**：消融实验（Table 6）表明，当体素尺寸从 0.5 米细化到 0.05 米时，语义占用 IoU 下降约 17–20 个百分点，揭示细粒度预测的显著困难——现有模型在超高分辨率下的空间推理能力严重不足。

### 5. 开放问题

1. **细粒度全景占用预测**：如何在 ≤0.05 米体素分辨率下同时提升全景占用预测的准确率和计算效率？当前方法的性能衰减表明需要新的模型架构或训练策略。

2. **实例感知预训练**：CarlaOcc 的实例级标签为设计新型视觉预训练任务提供了可能——例如实例完整性预测、实例间空间关系建模等——这些任务能否显著增强模型的空间推理能力？

3. **自监督/半监督学习**：CarlaOcc 的多模态数据（RGB、深度、法向量、语义分割）和物理一致性真值，是否为减少对大量真实标注数据的依赖提供了自监督或半监督学习的理想试验场？

4. **极端条件下的鲁棒性**：网格驱动的真值生成方法在更复杂的动态场景（如交通事故、异常行为）和极端天气条件下，如何保持其物理一致性和标注准确性？

5. **Sim-to-real 迁移的深层机制**：当前迁移增益有限，需要进一步研究模拟数据与真实数据之间的哪些差异（纹理、光照、几何精度、传感器噪声模型）是迁移瓶颈的关键因素，以及如何通过域适应或数据增强来弥合这些差距。

## 原文 PDF

![[paperPDFs/CVPR_2026/An_Instance_Centric_Panoptic_Occupancy_Prediction_Benchmark_for_Autonomous_Driving.pdf]]