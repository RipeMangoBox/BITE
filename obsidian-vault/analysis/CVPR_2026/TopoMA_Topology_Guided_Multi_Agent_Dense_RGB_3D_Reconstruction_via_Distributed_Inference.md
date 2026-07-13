---
title: "TopoMA: Topology-Guided Multi-Agent Dense RGB 3D Reconstruction via Distributed Inference"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TopoMA_Topology_Guided_Multi_Agent_Dense_RGB_3D_Reconstruction_via_Distributed_Inference.pdf
project_link: null
code_link: null
aliases:
- TopoMA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过显式建模场景的拓扑骨架（拓扑结构），并将其与端到端表征学习紧耦合，以联合解决智能体间空间对齐和子图融合等核心挑战。
primary_logic: 拓扑骨架总结了不同智能体子图之间的连通性和几何关系，并直接引导注意力分配、信息融合和位姿优化，在分布式架构下仅需轻量拓扑通信即可实现全局一致重建。
claims:
- TOPOMA通过拓扑骨架建模与优化，显著缓解了尺度漂移和累积误差，在KITTI数据集上取得最低RMSE ATE（Avg. 22.51 m）。
- 消融实验表明，完整的拓扑引导回环闭合与残差传输设计是达到最佳精度和资源效率的关键，其中完整方法在Replica上获得最低ATE（10.48 cm）和最高效的GPU/CPU占用。
- KITTI Odometry 上 RMSE ATE (m) = Avg. 22.51
- ScanNet 上 Depth L1 (cm) / Acc (cm) = 优于所有对比方法
---

# TopoMA: Topology-Guided Multi-Agent Dense RGB 3D Reconstruction via Distributed Inference

> [!tip] 核心洞察
> 拓扑骨架总结了不同智能体子图之间的连通性和几何关系，并直接引导注意力分配、信息融合和位姿优化，在分布式架构下仅需轻量拓扑通信即可实现全局一致重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | TopoMA：拓扑引导的多智能体密集RGB三维重建分布式推理框架 |
| 英文题名 | TopoMA: Topology-Guided Multi-Agent Dense RGB 3D Reconstruction via Distributed Inference |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_TopoMA_Topology-Guided_Multi-Agent_Dense_RGB_3D_Reconstruction_via_Distributed_Inference_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | TOPOMA |
| Dataset | KITTI Odometry, ScanNet, Replica |

> [!tip] 效果简介
> - KITTI Odometry 上，RMSE ATE (m) Avg. 22.51 vs VGGT-Long (次优) (更低)。
> - ScanNet 上，Depth L1 (cm) / Acc (cm) 优于所有对比方法 vs VGGT-Long, TTT3R, SLAM3R 等 (显著改善)。
> - Replica (多智能体设置) 上，RMSE (cm) 优于单智能体和多智能体基线 vs VGGT-SLAM, MAGiC-SLAM 等 (更佳)。

## 概要

### 问题瓶颈

现有端到端三维重建方法（如 **VGGT-Long** (Deng et al., arXiv 2025)、**TTT3R** (Chen et al., arXiv 2025)、**SLAM3R** (Liu et al., CVPR 2025)）在单智能体场景中已展现出较强能力，但直接扩展至多智能体协作时，面临三个核心瓶颈：

1. **跟踪不稳定**：多智能体间缺乏全局空间约束，位姿估计易产生尺度漂移和累积误差。
2. **内存消耗过高**：现有方案需传输原始点云或稠密特征，通信量和存储开销随智能体数量线性增长。
3. **回环闭合频繁失败**：基于外观或局部几何的回环检测在跨智能体、长序列场景中缺乏全局拓扑约束，导致虚假回环或漏检。

这些瓶颈使得现有方法难以满足实时、大规模多智能体部署的需求。

### 核心方法

**TOPOMA** 提出以**场景级拓扑骨架**（topology skeleton）为核心表征，将多智能体重建问题转化为拓扑引导的分布式优化问题。其核心洞察在于：拓扑骨架总结了不同智能体子图之间的连通性和几何关系，可直接引导注意力分配、信息融合和位姿优化。

方法由三个拓扑驱动的组件构成，形成全分布式架构：

- **拓扑骨架构建**：利用持久同调计算视图间拓扑相似度，构建最大生成树与候选回边，形成场景级骨架（Figure 2, Section 3.1）。
- **去中心化回环闭合**：基于拓扑骨架的门控机制，利用外观得分与测地距离联合筛选可信回环，驱动位姿修正（Figure 3, Section 3.2）。
- **拓扑引导残差传输**：压缩多模态残差为边描述子，沿骨架传播至锚定智能体，实现轻量通信与低内存占用（Figure 4, Section 3.3）。

在分布式架构下，各智能体仅交换轻量拓扑信息即可实现全局一致重建。

### 关键发现

**定量验证**（置信度均≥0.95）：

- 在 **KITTI Odometry** 数据集上，TOPOMA 取得最低平均 RMSE ATE（22.51 m），优于 VGGT-Long 等端到端方法（Table 1）。
- 在 **ScanNet** 室内数据集上，深度 L1 和 Accuracy 指标均显著优于所有对比方法（Table 2）。
- 在 **Replica** 多智能体设置中，跟踪精度优于单智能体和多智能体基线（Table 3）。

**消融实验揭示的因果机制**：

- 完整拓扑回环闭合方案在 Replica apartment-00 场景的 ATE 为 10.45 cm，比无回环设置降低 48%，且优于朴素回环、ICP 和单智能体回环（Table 4）。
- 完整残差传输方案取得 ATE 10.48 cm、FPS 6.23、GPU 5.90 GB、CPU 9.93 GB，相比于不传输（NoTrans-Single）精度提升 43%，且资源占用低于中心化方案（Table 5）。这表明**密集、拓扑感知的残差传输与频繁轻量融合**是实现精度-效率平衡的关键。

### 方法定位

TOPOMA 在方法谱系中处于**端到端表征学习**与**显式拓扑约束**的交汇点。不同于依赖中心化计算或局部几何的协作式 SLAM 方法（如 **CP-SLAM** (Hu et al., NeurIPS 2023)、**MAGiC-SLAM** (Yugay et al., CVPR 2025)、**MNE-SLAM** (Deng et al., CVPR 2025)），TOPOMA 通过拓扑骨架实现了全分布式架构下的全局空间对齐与融合，为多智能体三维重建提供了新的范式。

### 局限与展望

当前框架主要面向静态或近静态场景，强动态物体干扰会导致性能下降。未来工作方向包括：将显式动态物体建模融入拓扑骨架和残差传输中，以及在更大规模或异构智能体集群中验证拓扑骨架的实时构建与通信效率。

多智能体三维重建是机器人协作、自动驾驶和增强现实等领域的核心技术，其目标是通过多个独立移动的传感器平台，协同构建全局一致的三维场景模型。然而，将该任务从单智能体扩展至多智能体场景时，面临一系列根本性挑战。

现有端到端三维重建方法（如 **VGGT-Long**、**TTT3R**、**SLAM3R** 等）在单智能体设定下已展现出强大性能，但在多智能体分布式部署中暴露出三个关键瓶颈：**跟踪不稳定**——不同智能体的局部轨迹在缺乏全局约束时易产生尺度漂移和累积误差；**内存消耗过高**——传输稠密点云或完整特征图导致通信和存储开销随智能体数量与序列长度急剧增长；**回环闭合频繁失败**——仅依赖外观或局部几何的检测机制难以在视角差异大、场景重复纹理多的条件下可靠识别跨智能体的空间重合。

这些问题的根源在于，现有方法缺乏对场景全局空间结构的显式建模。多智能体系统本质上形成了一个稀疏、异质的观测网络，各智能体的子图之间既存在拓扑连通性（谁与谁相邻、何处形成回环），又蕴含几何约束（相对位姿、尺度一致性）。忽略这一结构，仅依靠局部优化或中心化融合，必然导致信息传递低效和全局不一致。

**TopoMA** 正是针对上述缺口提出。其核心动机在于：通过显式构建并持续更新场景级拓扑骨架，将多智能体重建问题重新表述为拓扑引导的分布式推理过程。该拓扑骨架总结了不同智能体子图之间的连通性和几何关系，并直接引导注意力分配、信息融合和位姿优化。在这一框架下，各智能体仅需交换轻量拓扑信息即可实现全局一致重建，从根本上缓解了通信压力、尺度漂移和回环不可靠等瓶颈。

## 核心方法与创新机理

TOPOMA 的核心创新在于将**显式的场景拓扑骨架**与端到端的表征学习紧耦合，从而在分布式多智能体架构下联合解决空间对齐、子图融合与回环闭合等关键挑战。相较于现有方法，TOPOMA 在四个关键维度上实现了根本性的设计转变：

### 1. 从中心化建图到全分布式拓扑协作架构

现有协作式三维重建方法（如 **CP-SLAM** (Hu et al., NeurIPS 2023)、**MAGiC-SLAM** (Yugay et al., CVPR 2025)）通常依赖中心化服务器进行全局优化或稠密特征融合，这在大规模部署中面临通信瓶颈和单点故障风险。TOPOMA 采用**全分布式架构**：每个智能体独立存储局部子图、执行前端重建和增量优化，智能体之间仅交换轻量级的拓扑骨架信息，无需传输原始点云或稠密特征。这一设计使得系统能够自然地扩展至多智能体场景，同时保持低通信开销和高鲁棒性。

### 2. 从局部几何对齐到拓扑骨架引导的全局一致性优化

传统方法依赖局部几何特征（如点云配准）或集中式优化进行空间对齐，容易产生尺度漂移和累积误差，尤其在长序列和异构轨迹下问题更为突出。TOPOMA 的核心洞察在于：**拓扑骨架总结了不同智能体子图之间的连通性和几何关系**，可作为全局对齐的强先验。

具体而言，TOPOMA 通过计算持久同调（persistent homology）得到视图间的拓扑相似度矩阵 $\mathcal{D}^{\mathrm{topo}}$，并据此构建最大生成树与候选回边，形成场景级拓扑骨架 $\mathcal{T} = (\mathcal{V}, \mathcal{E}_T)$。在后端优化中，注意力权重被拓扑距离显式正则化：

$$\alpha_{ij} = \frac{\exp\left(\frac{Q_i^{\top}K_j}{\sqrt{d}} - \lambda d_{ij}^{\mathrm{topo}}\right)}{\sum_{j'}\exp\left(\frac{Q_i^{\top}K_{j'}}{\sqrt{d}} - \lambda d_{ij'}^{\mathrm{topo}}\right)}$$

这一机制迫使模型关注拓扑相近的点云区域，从而在全局优化中抑制由视角变化和智能体间信息不一致引入的误差。

### 3. 从外观驱动回环检测到拓扑门控的去中心化回环闭合

现有回环闭合方法（如 **MASt3R-SLAM** 的朴素回环检测）主要依赖外观相似度或局部几何匹配，缺乏全局拓扑约束，容易产生虚假回环。TOPOMA 提出**去中心化回环闭合**机制，在拓扑骨架上引入双重门控条件：

$$s_{(m,t),(n,s)} \geq \tau_{\mathrm{loop}} \quad \mathrm{and} \quad d_{(m,t),(n,s)}^{\mathrm{topo}} \leq \delta_{\mathrm{topo}}$$

回环边必须同时满足外观得分阈值和拓扑骨架上的测地距离约束，从而有效过滤跨智能体的虚假回环。回环一旦被接受，将驱动位姿修正 $\Delta T_{m,t}$ 并传播至全局点云对齐：

$$\mathbf{P}^{\mathrm{global}} = \sum_{m,t} w_{m,t} T_{m,t}^{\mathrm{new}} \mathbf{P}_{m,t}$$

消融实验（Table 4）证实，该完整方案在 Replica apartment-00 上取得 ATE 10.45 cm，相比无回环设置降低 48%，且优于朴素回环、ICP 和单智能体回环等变体。

### 4. 从稠密特征传输到拓扑引导的轻量残差传播

传统多智能体系统常需传输原始点云或稠密特征，导致通信量大、资源消耗高。TOPOMA 设计了**拓扑引导的残差传输**模块：首先将每个边上的深度、颜色、点云和拓扑多模态残差压缩为单一边描述子 $\mathbf{r}_e$，再沿拓扑骨架进行消息传递，将全局残差集中到锚定智能体。传输损失约束了残差的一致性与位姿修正的对齐：

$$E_{\mathrm{trans}} = \sum_{v=(m,t)\in\mathcal{V}} \|\tilde{\mathbf{u}}_v - \mathbf{u}_v\|_2^2 + \mu \|h_\theta(\tilde{z}_{k(m,t)}) - g_\theta(\tilde{\mathbf{u}}_v)\|_2^2$$

消融实验（Table 5）表明，完整残差传输方案在保持 ATE 10.48 cm 的同时，GPU 占用仅 5.90 GB、CPU 占用 9.93 GB，相比完全不传输的独立智能体设置精度提升 43%，且资源效率优于中心化方案。这证明了**密集、拓扑感知的残差传输与频繁轻量融合**是平衡精度与效率的关键设计。

### 创新总结

上述四个 changed slots 并非孤立改进，而是围绕“拓扑骨架”这一核心表征形成的**协同创新体系**：拓扑骨架既是空间对齐的几何先验，又是回环筛选的全局约束，还是残差传播的高效通道。这种紧耦合设计使得 TOPOMA 在仅需轻量拓扑通信的条件下，实现了多智能体场景下的全局一致重建。

TOPOMA 提出了一种**全分布式、拓扑引导的多智能体密集三维重建框架**，其核心设计目标是在通信受限、轨迹异构的条件下实现全局一致的位姿估计与场景重建。框架的输入为多个独立智能体采集的 RGB 图像序列，输出为各智能体的精确相机位姿以及全局对齐的稠密点云。

### 核心设计理念

现有端到端重建方法在多智能体扩展时面临三重瓶颈：**跟踪不稳定、内存消耗过高、回环闭合频繁失败**。TOPOMA 的关键洞察在于：不同智能体子图之间的连通性和几何关系可以被抽象为一个**场景级拓扑骨架（topology skeleton）**，该骨架以轻量形式总结了全局结构信息，可直接引导注意力分配、信息融合和位姿优化，从而仅需交换拓扑信息即可实现全局一致重建。

### 三大拓扑驱动组件

框架由三个紧密耦合的拓扑驱动组件构成，形成完整的分布式推理管线：

1. **拓扑骨架构建（Topology Skeleton Construction）**：通过计算持久同调（persistent homology）拓扑相似度，构建最大生成树与候选回边，形成场景级拓扑骨架。该骨架同时编码了智能体间的空间连通性和几何关系。

2. **去中心化回环闭合（Decentralized Loop Closure）**：基于拓扑骨架的门控机制，利用令牌对预测回环得分，仅当外观得分和拓扑测地距离同时满足阈值条件（见 Eq. (12)）时才接受回环边，有效过滤虚假回环。回环检测与修正在各智能体本地去中心化执行。

3. **拓扑引导残差传输（Topology-Guided Residual Transport）**：将深度、颜色、点云、拓扑等多模态残差压缩为边描述子，沿拓扑骨架进行消息传递，将全局残差集中到锚定智能体，实现轻量通信与低内存占用。

### 前端-后端双阶段架构

每个智能体内部采用**前端/后端拓扑Transformer**的双阶段处理流程：

- **前端（Frontend）**：使用因果注意力（causal attention）进行局部顺序更新，从 RGB 图像生成局部点云和映射令牌，并利用 KV 缓存加速推理（Eq. (1)）。
- **后端（Backend）**：使用全局注意力并融合拓扑正则化，注意权重由查询-键相似度与拓扑距离共同决定（Eq. (6)），迫使模型关注拓扑相近的点云，进行全局优化与位姿修正。

### 分布式协作与通信模式

与传统的中心化计算或独立建图方案不同，TOPOMA 采用**完全分布式架构**：每个智能体独立存储、重建和增量优化本地子图，智能体之间仅交换轻量拓扑信息（骨架结构与压缩残差），而非传输原始点云或稠密特征。这种设计从根本上降低了通信带宽需求和内存消耗，使得框架能够部署于大规模、资源受限的多智能体场景。

### 全局优化目标

框架的全局优化目标综合了深度、颜色、点云和拓扑等多模态残差（Eq. (17)），确保回环边和拓扑边的一致性。残差传输损失（Eq. (23)）则约束传输后的残差与原始残差一致，并与全局令牌预测的位姿修正对齐，保证残差传输的有效性。

> 图 2 展示了 TOPOMA 的完整系统概览，涵盖建图（Mapping）与跟踪（Tracking）两大分支的交互流程。

![[assets/figures/papers/paper_list_l2648_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_TopoMA_Topology/figures/002_Figure_2.jpg]]
*Figure 2: Overview of TOPOMA. Mapping: RGB observations are tokenized and aggregated to build a topology-aware skeleton, which is unified with geometric cues to recover consistent structure and scale. Tracking: Agents perform local loop detection, update topology constraints, and apply topology-consistent loop closures through frontend/back-end topology transformers, ensuring coherent multi-agent pose estimation.The system runs fully distributed, allowing each agent to maintain local submaps while progressively achieving global topological consistency*

TOPOMA 围绕三个拓扑驱动的核心模块构建全分布式多智能体重建管线：**拓扑骨架构建**、**去中心化回环闭合**和**拓扑引导残差传输**。这三个模块共享一个统一的拓扑表征，并通过前端/后端拓扑 Transformer 实现局部顺序更新与全局一致性优化。

### 3.1 拓扑骨架构建

每个智能体独立地从 RGB 序列中提取局部点云和映射令牌。前端采用因果注意力机制，利用 KV 缓存实现增量式生成：

$$(P_{m,t}, F_{m,t}) \gets f_{\theta}^{\mathrm{causal}}(X_{m,t}; C_m) \quad \text{(Eq. 1)}$$

其中 $X_{m,t}$ 为智能体 $m$ 在时刻 $t$ 的 RGB 观测，$C_m$ 为缓存的上下文，$P_{m,t}$ 为局部点云，$F_{m,t}$ 为映射令牌。

为建立跨智能体的空间关联，TOPOMA 计算持久同调拓扑相似度，构建成对拓扑距离矩阵：

$$\mathcal{D}^{\mathrm{topo}} = \{ d_{mn}^{\mathrm{topo}} \}_{m,n=1}^{M}$$

基于该矩阵，系统提取最大生成树作为场景级拓扑骨架 $\mathcal{T} = (\mathcal{V}, \mathcal{E}_T)$，并保留候选回边 $\mathcal{E}_{\mathrm{loop}}$ 以捕捉潜在的循环结构。

后端采用全局注意力进行拓扑正则化优化。注意力权重由查询-键相似度与拓扑距离联合决定，迫使模型关注拓扑相近的点云：

$$\alpha_{ij} = \frac{\exp\left(\frac{Q_i^{\top}K_j}{\sqrt{d}} - \lambda d_{ij}^{\mathrm{topo}}\right)}{\sum_{j'}\exp\left(\frac{Q_i^{\top}K_{j'}}{\sqrt{d}} - \lambda d_{ij'}^{\mathrm{topo}}\right)} \quad \text{(Eq. 6)}$$

其中 $\lambda$ 控制拓扑约束的强度，$d_{ij}^{\mathrm{topo}}$ 为节点 $i$ 和 $j$ 在拓扑骨架上的测地距离。

### 3.2 去中心化回环闭合

回环闭合模块利用拓扑骨架的门控机制筛选可信回环。对于任意候选回边 $(m,t) \leftrightarrow (n,s)$，其接受条件为：

$$s_{(m,t),(n,s)} \geq \tau_{\mathrm{loop}} \quad \mathrm{and} \quad d_{(m,t),(n,s)}^{\mathrm{topo}} \leq \delta_{\mathrm{topo}} \quad \text{(Eq. 12)}$$

即回环边必须同时满足外观得分阈值 $\tau_{\mathrm{loop}}$ 和拓扑测地距离上限 $\delta_{\mathrm{topo}}$，从而有效过滤由视觉模糊或局部几何相似引起的虚假回环。

接受回环后，系统计算位姿修正量并更新智能体位姿：

$$T_{m,t}^{\mathrm{new}} = \Delta T_{m,t} \circ T_{m,t}^{\mathrm{old}}$$

最终通过加权融合获得全局对齐的点云：

$$\mathbf{P}^{\mathrm{global}} = \sum_{m,t} w_{m,t} T_{m,t}^{\mathrm{new}} \mathbf{P}_{m,t}$$

### 3.3 拓扑引导残差传输

为在通信约束下实现全局一致优化，TOPOMA 将多模态残差压缩为边描述子。对于每条边 $e$ 上的采样点集 $\Omega_e$，使用置换不变聚合器压缩深度、颜色、点云和拓扑残差：

$$\mathbf{r}_e = g_{\mathrm{edge}}\left(\{r_{e,j}^{\mathrm{depth}}, r_{e,j}^{\mathrm{color}}, r_{e,j}^{\mathrm{pointmap}}, r_{e,j}^{\mathrm{topo}}\}_{j\in\Omega_e}\right)$$

节点级残差描述子通过聚合其所有关联边的描述子得到：

$$\mathbf{u}_v = g_{\mathrm{node}}(\{\mathbf{r}_e \mid e \in \mathcal{E}_T \cup \mathcal{E}_{\mathrm{loop}}, e \ni v\})$$

残差沿拓扑骨架进行消息传递，最终汇聚到锚定智能体。全局优化目标综合所有模态残差：

$$E_{\mathrm{pose}} = \sum_{e \in \mathcal{E}_T \cup \mathcal{E}_{\mathrm{loop}}} \sum_{j \in \Omega_e} \left(\lambda_{\mathrm{depth}} \| r_{e,j}^{\mathrm{depth}} \|_2^2 + \lambda_{\mathrm{color}} \| r_{e,j}^{\mathrm{color}} \|_2^2 + \lambda_{\mathrm{pointmap}} \| r_{e,j}^{\mathrm{pointmap}} \|_2^2 + \lambda_{\mathrm{topo}} \| r_{e,j}^{\mathrm{topo}} \|_2^2\right) \quad \text{(Eq. 17)}$$

为保证残差传输的有效性，训练时约束传输后的残差与原始残差一致，并与全局令牌预测的位姿修正对齐：

$$E_{\mathrm{trans}} = \sum_{v=(m,t)\in\mathcal{V}} \|\tilde{\mathbf{u}}_v - \mathbf{u}_v\|_2^2 + \mu \|h_\theta(\tilde{z}_{k(m,t)}) - g_\theta(\tilde{\mathbf{u}}_v)\|_2^2 \quad \text{(Eq. 23)}$$

其中 $\tilde{\mathbf{u}}_v$ 为传输后的节点残差，$\tilde{z}_{k(m,t)}$ 为全局令牌，$h_\theta$ 和 $g_\theta$ 分别为位姿预测头和残差编码头。该设计使得各智能体仅需交换轻量拓扑信息和压缩残差描述子，即可实现与中心化方案相当的全局一致性，同时显著降低通信开销与内存占用。

## 实验与关键发现

### 核心实验设置

TOPOMA在KITTI里程计、ScanNet和Replica三个数据集上进行评估，覆盖室外大规模驾驶、室内多房间重建等场景。轨迹精度采用RMSE和Mean ATE（米/厘米）衡量，重建质量采用Depth L1和Accuracy（厘米）衡量。所有方法遵循相同的序列分割和全局Sim(3)对齐协议，每个序列评估5次取均值，确保公平比较。多智能体设置中，各智能体独立运行前端，仅通过拓扑骨架交换轻量级信息。

### 主实验结果

#### 室外大规模跟踪（KITTI）

在KITTI里程计数据集上，TOPOMA取得了最低的平均RMSE ATE（22.51 m）和Mean ATE（18.32 m），显著优于次优方法VGGT-Long（Kai Deng et al., arXiv 2025）及其他基线。如表1所示，TOPOMA在KITTI-07子序列上RMSE仅3.95 m、Mean 3.67 m，而VGGT-Long在多个序列上出现跟踪丢失（[TL]标记）。论文将此归因于拓扑骨架建模与优化通过全局拓扑一致性有效缓解了尺度漂移和累积误差（Section 4.2）。

#### 室内重建精度（ScanNet）

在ScanNet数据集上，TOPOMA在Depth L1和Accuracy两项指标上均优于VGGT-Long、TTT3R（Xingyu Chen et al., arXiv 2025）、SLAM3R（Yuzheng Liu et al., CVPR 2025）等所有对比方法（表2）。定性结果（图6）显示，TOPOMA重建的场景几何结构更完整、表面更平滑，尤其在纹理稀疏和视角变化剧烈区域，拓扑一致性优化有效减少了视角变化和智能体间信息不一致带来的误差。

#### 多智能体跟踪（Replica）

在Replica数据集的多智能体设置中，TOPOMA的RMSE优于单智能体基线VGGT-SLAM（Dominic Maggio et al., 2025）和多智能体基线MAGiC-SLAM（Vladimir Yugay et al., CVPR 2025）等（表3）。这表明分布式拓扑骨架通信在保持低通信开销的同时，能够实现跨智能体的有效空间对齐与融合。

### 消融实验

消融实验在Replica的apartment-00场景上进行，所有结果取5次运行均值。

#### 回环闭合消融

表4对比了五种回环闭合设置：NoLoop（无回环）、NaiveLoop（采用MASt3R的回环方法）、ICP（子图ICP融合）、Single-Loop（单智能体使用TOPOMA回环）和Ours（完整多智能体拓扑回环）。完整方案的ATE为10.45 cm，比NoLoop降低48%，且优于所有消融变体。NaiveLoop和ICP因缺乏拓扑约束，在复杂场景中易引入误匹配；Single-Loop虽使用拓扑门控，但缺少跨智能体信息，精度低于完整方案。这验证了去中心化回环闭合中外观得分与拓扑测地距离双重门控条件的必要性。

#### 残差传输消融

表5对比了五种残差传输设置：NoTrans-Center（中心化融合无传输）、NoTrans-Single（完全独立智能体）、MNE-SLAM（Tianchen Deng et al., CVPR 2025的全分布式神经SLAM）、Trans-500（每500帧传输一次）和Ours（完整拓扑引导残差传输）。完整方案取得ATE 10.48 cm、FPS 6.23、GPU 5.90 GB、CPU 9.93 GB的最佳综合表现。相比NoTrans-Single精度提升43%，且资源占用低于中心化方案NoTrans-Center。Trans-500因传输频率过低导致精度显著下降，表明频繁的轻量拓扑残差传输对维持全局一致性至关重要。

### 失败模式与局限性

论文明确指出，当前框架主要面向静态或近静态场景。在强动态物体干扰下（如高度动态的行人、车辆密集场景），拓扑骨架的构建和残差传输的可靠性会下降，导致性能退化。这一局限性源于拓扑骨架基于静态场景假设进行建模，动态物体会引入虚假的拓扑连接和噪声残差。

### 关键图表结论

- **图1**：大规模真实世界多智能体实验中，四个智能体在卫星地图上覆盖不同区域，重建的点云和三维场景展示了TOPOMA在室外大规模部署中的全局一致性。
- **图3**：回环闭合效果示意清晰展示了漂移重建、拓扑骨架上的多智能体回环检测和修正后全局对齐结果的对比。
- **图4**：残差传输模块的GPU/CPU内存占用随输入帧数增长保持高效，验证了轻量通信设计的可扩展性。
- **表1**：KITTI跟踪精度定量结果，TOPOMA在平均RMSE和Mean ATE上均为最优。
- **表4/5**：消融实验定量验证了拓扑引导回环闭合和残差传输各自对精度和资源效率的关键贡献。

![[assets/figures/papers/paper_list_l2648_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_TopoMA_Topology/figures/006_Table_1.jpg]]
*Table 1: Tracking results on the KITTI odometry dataset [15], evaluated using RMSE and Mean ATE (meters). All methods follow identical sequence-splitting and global Sim(3) alignment. Each sequence is evaluated five times, and all reported values are averaged over these runs. The final “Average” column is computed across all sequences. [TL] indicates tracking lost. All other quantitative tables in this paper follow the same evaluation protocol unless otherwise specified. Best results are highlighted as first , second , and third*

![[assets/figures/papers/paper_list_l2648_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_TopoMA_Topology/figures/008_Table_2.jpg]]
*Table 2: Reconstruction accuracy on ScanNet[6]. We evaluate per-scene and averaged Depth L1[cm] and Accuracy (Acc)[cm] metrics. Lower is better*

![[assets/figures/papers/paper_list_l2648_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_TopoMA_Topology/figures/010_Table_3.jpg]]
*Table 3: Tracking accuracy on the Replica[28] dataset measured by RMSE [cm] for single-agent and multi-agent settings. Averages are computed across all scenes*

![[assets/figures/papers/paper_list_l2648_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_TopoMA_Topology/figures/011_Table_4.jpg]]
*Table 4: Ablation on Loop Closure. We conduct experiments on apartment-00 of Replica [28] to verify the effectiveness of our method, and all reported values are averaged over 5 runs*

![[assets/figures/papers/paper_list_l2648_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_TopoMA_Topology/figures/009_Table_5.jpg]]
*Table 5: Ablation on residual transport.We conduct experiments on apartment-00 of Replica [28] to verify the effectiveness of our method, and all reported values are averaged over 5 runs*

## 定位与知识库关联

### 与现有基线方法的关系

TOPOMA 处于端到端三维重建与多智能体 SLAM 的交叉点上，其核心贡献在于将**显式拓扑骨架**引入分布式重建管线，从而区别于现有的各类基线。

**相对于端到端单目/长序列重建方法**：VGGT-Long（Deng et al., arXiv 2025）、TTT3R（Chen et al., arXiv 2025）和 SLAM3R（Liu et al., CVPR 2025）代表了近期端到端重建的前沿，它们在单智能体、短/中序列场景下表现优异。然而，当直接扩展至多智能体长序列时，这些方法面临跟踪不稳定、内存消耗过高、回环闭合频繁失败等瓶颈。TOPOMA 的差异化在于：它不依赖单一模型端到端处理所有输入，而是通过拓扑骨架显式建模场景的连通性和几何关系，将全局一致性问题分解为拓扑引导的分布式优化。在 KITTI 数据集上，TOPOMA 取得平均 RMSE ATE 22.51 m，优于 VGGT-Long 等次优方法（Table 1），这验证了拓扑建模对缓解尺度漂移和累积误差的关键作用。

**相对于实时密集 SLAM 方法**：MASt3R-SLAM（Murai et al., 2024）和 VGGT-SLAM（Maggio et al., 2025）将三维先验融入实时 SLAM，但在多智能体场景下仍依赖局部几何或集中式优化，难以保证全局拓扑一致性。TOPOMA 通过全分布式架构，每个智能体独立存储、重建和增量优化地图，仅交换轻量拓扑信息，在 Replica 多智能体设置中取得了优于 VGGT-SLAM 和 MAGiC-SLAM 的跟踪精度（Table 3），证明了拓扑引导的空间对齐与融合策略的有效性。

**相对于协作式多智能体 SLAM**：CP-SLAM（Hu et al., NeurIPS 2023）、MAGiC-SLAM（Yugay et al., CVPR 2025）和 MNE-SLAM（Deng et al., CVPR 2025）分别探索了神经点云、高斯表征和全分布式架构下的多智能体协作。TOPOMA 与这些工作的根本区别在于：它不传输原始点云或稠密特征，而是通过**拓扑引导残差传输**机制，将多模态残差压缩为边描述子并沿骨架传播，实现轻量通信和低内存占用。消融实验（Table 5）表明，完整残差传输方案在 Replica 上取得 ATE 10.48 cm、GPU 5.90 GB、CPU 9.93 GB，精度比不传输方案提升 43%，且资源占用低于中心化方案，这为多智能体系统的大规模部署提供了新的效率-精度平衡点。

### 适用边界与局限性

TOPOMA 的设计假设场景具有**稳定的拓扑结构**，因此其适用边界主要受限于场景的动态程度：

1. **静态或近静态场景**：论文的核心实验在 KITTI（室外驾驶）、ScanNet（室内扫描）和 Replica（室内重建）上进行，这些场景的动态物体相对较少或可控。在此类场景中，拓扑骨架能够准确总结不同智能体子图之间的连通性和几何关系，引导注意力分配、信息融合和位姿优化，取得全局一致的重建结果。

2. **强动态物体干扰**：论文已明确指出，当前框架在强动态物体干扰下会导致性能下降。这是因为动态物体会破坏拓扑骨架的稳定性——持久同调拓扑相似度计算假设场景结构在观测间保持一致性，而动态物体的出现会引入虚假的拓扑特征，进而影响回环闭合的门控决策和残差传输的可靠性。

3. **通信约束下的可扩展性**：TOPOMA 的全分布式架构仅需交换轻量拓扑信息，理论上适用于通信带宽受限的场景。但论文未在大规模异构智能体集群（如数十个智能体）上进行验证，拓扑骨架的实时构建与通信效率是否依旧保持较高水平，仍需进一步实验确认。

### 开放问题

1. **动态物体的显式建模**：如何将动态物体的检测、跟踪与分割融入拓扑骨架的构建与更新中？一个可能的方向是学习动态感知的拓扑不变量，或引入时序注意力机制来区分静态结构与动态前景，从而在高度动态环境下保持鲁棒性。

2. **异构智能体集群的扩展**：在更大规模或异构智能体（如不同传感器配置、不同运动模式）集群中，拓扑骨架的构建需要处理不同粒度和噪声水平的观测。如何设计统一的拓扑表示和自适应门控阈值，以维持全局一致性和通信效率，是一个开放挑战。

3. **拓扑骨架的在线学习与自适应**：当前拓扑骨架的构建依赖于预定义的持久同调计算和最大生成树提取。是否可以通过端到端学习的方式，直接从数据中学习拓扑骨架的构建策略，使其更好地适应特定场景类型和任务需求？

4. **与语义理解的融合**：拓扑骨架目前仅编码几何连通性，若能融合语义信息（如房间类型、物体类别），可能进一步提升回环闭合的判别能力和全局优化的语义一致性，这为后续研究提供了潜在方向。

### 知识库定位

TOPOMA 可被定位为**拓扑感知的分布式多智能体三维重建**这一新兴方向的代表性工作。它在知识库中的位置如下：

- **上游依赖**：端到端三维重建（VGGT, MASt3R 系列）、持久同调拓扑数据分析、图神经网络消息传递机制、分布式 SLAM 架构。
- **核心贡献**：首次将显式拓扑骨架建模与端到端表征学习紧耦合，形成拓扑引导的分布式重建管线，包括拓扑骨架构建、去中心化回环闭合和拓扑引导残差传输三大模块。
- **下游影响**：为多智能体系统中的轻量通信、全局一致性和资源效率提供了新的方法论框架，可启发后续工作在动态场景建模、异构集群扩展和语义拓扑融合等方向上的研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/TopoMA_Topology_Guided_Multi_Agent_Dense_RGB_3D_Reconstruction_via_Distributed_Inference.pdf]]
