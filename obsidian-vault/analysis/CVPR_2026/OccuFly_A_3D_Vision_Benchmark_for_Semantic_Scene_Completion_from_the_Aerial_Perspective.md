---
title: "OccuFly: A 3D Vision Benchmark for Semantic Scene Completion from the Aerial Perspective"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/OccuFly_A_3D_Vision_Benchmark_for_Semantic_Scene_Completion_from_the_Aerial_Perspective.pdf
project_link: null
code_link: "https://github.com/markus-42/occufly"
aliases:
- OS
- OccuFly
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 采用纯相机的经典SfM+MVS三维重建，通过少量2D标注图像（<10%）将语义标签提升至密集点云，并引入类别感知的实例视觉外壳雕刻、地物泊松表面重建等模块生成密集语义体素网格。
primary_logic: 通过纯相机数据生成流水线构建首个真实世界航拍SSC基准OccuFly，覆盖多种场景、季节与高度，揭示现有模型在航拍场景下性能严重不足，为航拍三维视觉研究提供关键推动力。
claims:
- DISC模型在OccuFly测试集上的IoU仅29.52、mIoU仅2.04，Symphonies更低（13.68/0.58），表明航拍SSC极具挑战。
- 零样本深度基础模型在OccuFly上表现极差（DepthAnything2 AbsRel 0.729），微调后虽有提升但仍不完美（AbsRel 0.134），证实严重的领域差距。
- 手动标注不到10%的图像即可覆盖超过99%的三维点，验证了2D‑3D标签提升策略的高效性。
- SfM+MVS重建的平均重投影误差仅1.24像素，保证了三维几何精度。
---

# OccuFly: A 3D Vision Benchmark for Semantic Scene Completion from the Aerial Perspective

> [!tip] 核心洞察
> 通过纯相机数据生成流水线构建首个真实世界航拍SSC基准OccuFly，覆盖多种场景、季节与高度，揭示现有模型在航拍场景下性能严重不足，为航拍三维视觉研究提供关键推动力。

| 字段 | 内容 |
|------|------|
| 中文题名 | OccuFly：面向航拍视角的三维语义场景补全基准数据集 |
| 英文题名 | OccuFly: A 3D Vision Benchmark for Semantic Scene Completion from the Aerial Perspective |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.20770) · [Code](https://github.com/markus-42/occufly) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | OccuFly（基于相机数据生成流水线的航拍SSC基准） |
| Dataset | OccuFly |

> [!tip] 效果简介
> - OccuFly (SSC) 上，IoU / mIoU 29.52 / 2.04 (DISC) vs 13.68 / 0.58 (Symphonies) (DISC vs. Symphonies（全部高度）)。
> - OccuFly (深度估计) 上，AbsRel / RMSE 0.134 / 4.844 (DepthAnything2‑OccuFly) vs 0.729 / 28.382 (DepthAnything2 zero‑shot) (微调后大幅提升)。
> - OccuFly (数据生成验证) 上，重投影误差 [px] / 标注占比 / 覆盖 1.24 / 9.17% / 99% vs - (标注少于10%图像覆盖>99%点云)。

## 概述

**问题瓶颈**：三维语义场景补全（Semantic Scene Completion, SSC）旨在从部分观测中推理完整的场景几何与语义，但现有基准与模型严重依赖LiDAR。在无人机航拍场景下，LiDAR因载荷、功耗限制及点云稀疏性难以适用，而现有SSC模型和视觉基础模型无法直接泛化至航拍领域，导致航拍SSC长期缺乏可行的研究基准。

**核心思路**：OccuFly提出了一套纯相机驱动的数据生成流水线，绕过LiDAR依赖。该流水线通过经典的SfM+MVS三维重建获得度量级稠密点云，再将少量2D图像标注（<10%）通过反向投影与多视图一致性投票提升至三维空间，并引入类别感知的实例视觉外壳雕刻与地物泊松表面重建，生成密集的语义体素网格真值。

**方法定位**：OccuFly并非一种新的SSC模型，而是一个**面向航拍视角的SSC基准数据集**。其贡献在于数据生成范式——用纯相机模态替代LiDAR，用高效2D标注替代繁重的3D标注，为航拍SSC提供了首个真实世界基准。

**关键结果**：
- 在OccuFly测试集上，现有SSC模型表现极差：**DISC**的IoU仅29.52、mIoU仅2.04，**Symphonies**更低（13.68/0.58），揭示航拍SSC的巨大挑战（Table 4）。
- 深度基础模型在零样本条件下严重失效：**DepthAnything2**的AbsRel高达0.729；经OccuFly微调后虽大幅改善（AbsRel 0.134），但仍不完美，证实显著的领域差距（Table 5）。
- 数据生成流水线具备高几何精度（平均重投影误差1.24像素）和高标注效率（标注<10%图像覆盖>99%三维点），验证了纯相机路线的可行性（Tab. 8, Tab. 9）。

## 背景与动机

三维语义场景补全（Semantic Scene Completion, SSC）旨在从部分观测中同时推理场景的三维几何与语义类别，是自动驾驶、机器人导航等应用的核心感知能力。然而，现有SSC研究几乎完全围绕地面视角展开，其训练与评估严重依赖LiDAR传感器提供的稠密三维真值。这一范式在无人机航拍场景中面临根本性瓶颈：LiDAR因重量、功耗限制以及高空点云固有的稀疏性而难以部署，导致航拍SSC长期缺乏可行的基准数据集。

从数据生成的角度看，现有SSC基准（如SemanticKITTI、KITTI-360等）均采用LiDAR累积点云作为几何骨架，再辅以繁重的手工三维标注。若将这一流程迁移至航拍领域，不仅硬件成本高昂，点云稀疏性还会严重损害语义标注的完整性与准确性。另一方面，近年来涌现的视觉基础模型（如DepthAnything系列）虽在通用深度估计上表现优异，但其在航拍场景下的零样本泛化能力极为有限——例如DepthAnything3在OccuFly上的平均度量尺度偏差高达526%（Figure 3），揭示了严重的领域鸿沟。

上述双重困境——LiDAR依赖与模型泛化失效——构成了航拍SSC的核心瓶颈：既缺乏可扩展的真值生成手段，又缺乏能应对航拍特性的感知模型。OccuFly正是针对这一缺口提出的首个真实世界航拍SSC基准。其核心思路是摒弃LiDAR，转而利用纯相机数据生成流水线，通过经典SfM+MVS三维重建、高效2D-3D语义标签提升以及类别感知的稠密化与体素化，构建覆盖多场景、多季节、多高度的密集语义体素网格。该基准不仅为航拍SSC提供了可复现的评估平台，更通过系统性的基线实验揭示了现有模型在航拍领域的性能塌陷，为后续研究指明了方向。

## 核心创新

OccuFly的核心创新并非提出一种新的SSC模型，而是构建了一套纯相机驱动的数据生成范式，从根本上绕开了航拍场景下LiDAR难以适用这一瓶颈。该范式的创新性集中体现在三个关键的“changed slots”上，它们共同构成了一个完整的基准生成流水线。

**1. 模态替代：从LiDAR到纯相机（SfM+MVS）**
现有SSC基准（如SemanticKITTI）严重依赖LiDAR提供三维几何真值，但无人机平台受限于LiDAR的载荷、功耗以及航拍点云的天然稀疏性，难以直接沿用这一技术路线。OccuFly的核心突破在于完全摒弃LiDAR，采用经典的多视图几何重建流水线（SfM+MVS）从地理参考图像中恢复度量级稠密点云。这一选择不仅解决了数据获取的可行性问题，还意外地获得了极高的几何精度：在所有场景上的平均重投影误差仅为1.24像素（Table 8），为后续语义标注提供了可靠的几何基础。

**2. 标注范式：从繁重3D标注到高效2D-3D标签提升**
传统三维语义标注需要在点云上进行逐点操作，极为耗时。OccuFly将标注工作流彻底反转：仅需手动标注少量二维图像（每个场景少于10%的图像），然后通过反向投影与多视图多数投票，将语义标签自动提升至三维点云。这一策略的效率由标注覆盖度公式严格保证：

$$\rho(\mathcal{I}) = \frac{ | \{ \mathbf{x} \in \mathcal{P} \mid \exists n \in \mathcal{I}, \exists (u,v) \, \mathrm{s.t.} \, ((u,v),\mathbf{x}) \in \mathcal{A}_n \} | }{ |\mathcal{P}| }$$

实验表明，标注少于10%的图像即可覆盖超过99%的重建三维点（Table 9, Sec. 3.3.2），将人工成本降低了一个数量级。这一机制是OccuFly能够以可负担的成本构建大规模航拍SSC基准的关键。

**3. 点云稠密化：类别感知的实例雕刻与表面重建**
SfM+MVS重建的点云在视觉外壳内部及地面区域存在大量空洞，直接体素化会严重破坏语义网格的完整性。OccuFly引入了一种类别感知的稠密化策略，将21个语义类别划分为实例、地面和其他三个互斥组：

$$\mathcal{C}_{\mathrm{inst}} \cup \mathcal{C}_{\mathrm{gnd}} \cup \mathcal{C}_{\mathrm{oth}} = \mathcal{C}, \quad \mathcal{C}_{\mathrm{inst}} \cap \mathcal{C}_{\mathrm{gnd}} \cap \mathcal{C}_{\mathrm{oth}} = \emptyset$$

对实例类别（如车辆、建筑），采用DBSCAN分离单个实例后，利用虚拟视图剪影进行视觉外壳雕刻，以填充实例内部空洞；对地面类别，则使用泊松表面重建恢复完整的地形表面。最终按实例优先于其他、其他优先于地面的优先级进行场景级语义体素聚合（Eq. 13），生成空间完整的语义占用网格。这一模块是连接稀疏语义点云与密集体素真值之间的桥梁，使得OccuFly能够提供与地面LiDAR基准相媲美的体素级真值。

**创新点的协同效应**
上述三个changed slots并非孤立存在，而是形成了强依赖的因果链条：纯相机重建提供了几何基础，高效2D标注在几何基础上附着语义，类别感知稠密化则将稀疏语义几何转化为密集体素网格。这一流水线的整体创新性在于，它首次证明了在完全无需LiDAR的条件下，仅凭相机数据即可构建出具有挑战性的航拍SSC基准，为航拍三维视觉研究开辟了可行的评估路径。

**证据强度说明**：上述三个changed slots均有定量实验支撑（重投影误差1.24 px、标注覆盖率>99%、稠密化流程的定性验证见Figure 6），证据可信度较高。但需注意，类别感知稠密化的精度评估目前主要依赖于定性观察，缺乏与真值体素的逐体素对比指标，这一点需要读者在评估该模块的绝对精度时保持审慎。

## 整体框架

OccuFly 提出了一套**纯相机、免 LiDAR 的数据生成框架**，旨在为航拍视角的语义场景补全（SSC）构建大规模、高质量的基准数据集。整个流水线以无人机采集的地理参考 RGB 图像为唯一输入，通过四个核心模块依次生成场景级语义体素网格及逐帧真值，其总体流程如 Figure 2 所示。

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/002_Figure_2.jpg]]
*Figure 2: Proposed image-based data generation framework. An overview is provided in Sec. 3.1. Zoom in for the best view*

### 模块关系与数据流

1. **三维重建（Sec. 3.3.1）**  
   利用标定后的相机内参 $\mathcal{K}$ 和地理参考位姿 $\mathcal{T}$，通过 **SfM（Structure-from-Motion）与 MVS（Multi-View Stereo）** 从多视角图像 $\mathcal{I}$ 中恢复度量级稠密点云 $\mathcal{P}$、逐帧深度图集 $\mathcal{D}$ 以及 2D‑3D 对应关系集 $\mathcal{A}$：
   $$(\mathcal{P}, \mathcal{D}, \mathcal{A}) = \Psi_{\mathrm{SfM+MVS}}(\mathcal{I}, \mathcal{K}, \mathcal{T})$$
   其中 2D‑3D 对应关系 $\mathcal{A}_n$ 满足透视投影方程，为后续语义标签提升提供几何桥梁。该模块的平均重投影误差仅为 **1.24 像素**（Table 8），保证了三维几何的高保真度。

2. **语义标注（Sec. 3.3.2）**  
   仅需手动标注 **少于 10% 的图像**（$\mathcal{J} \subset \mathcal{I}$），通过反向投影将 2D 语义标签提升至点云 $\mathcal{P}$。多视图证据通过**无加权多数投票**融合，平局时以类别先验频率排序裁决。未覆盖的稀疏点采用**逆距离加权 kNN 传播**，随后以第二轮 kNN 去噪。实验表明，该策略可覆盖 **超过 99% 的稠密点云**（Table 9），极大降低了人工标注成本。

3. **类别感知稠密化与体素化（Sec. 3.3.3）**  
   将语义类别划分为三个互斥组——实例类 $\mathcal{C}_{\mathrm{inst}}$、地物类 $\mathcal{C}_{\mathrm{gnd}}$ 和其他类 $\mathcal{C}_{\mathrm{oth}}$——并采用差异化处理：
   - **实例类**：通过类特定 DBSCAN 分离单个实例，再基于虚拟视图剪影进行**视觉外壳雕刻**，生成实例占据集 $\mathcal{O}_{\mathrm{inst}}$。
   - **地物类**：采用 **Poisson 表面重建** 填充空洞，生成地物占据集 $\mathcal{O}_{\mathrm{gnd}}$。
   - **其他类**：直接体素化得 $\mathcal{O}_{\mathrm{oth}}$。
   最终按 $\mathrm{inst} \succ \mathrm{oth} \succ \mathrm{gnd}$ 的优先级融合，解决标签冲突，得到完整的场景级语义体素网格 $\mathbf{Y}$。

4. **真值采样（Sec. 3.3.4）**  
   对每帧图像，依据其相机参数进行**视锥体裁剪与栅格化**，从场景级体素网格 $\mathbf{Y}$ 中提取逐帧语义体素网格，并同步生成三类二元掩码——无效、表面与遮挡——以支持标准化的 SSC 评估协议。

### 输入输出

- **输入**：无人机采集的多视角 RGB 图像、相机内参、地理参考位姿，以及少量（<10%）手动标注的 2D 语义图像。
- **输出**：场景级语义体素网格、逐帧语义体素网格、度量深度图及对应的评估掩码，构成 OccuFly 基准数据集的核心真值。

该框架的核心优势在于**完全摆脱对 LiDAR 的依赖**，以纯相机模态克服航拍场景下 LiDAR 点云稀疏、设备能耗高等瓶颈，同时通过高效的 2D‑3D 标签提升策略将人工标注从繁重的 3D 标注转变为轻量级 2D 标注，为航拍三维场景理解提供了可扩展的数据生成范式。

## 核心模块与公式推导

OccuFly 数据生成流水线由四个核心模块串联构成：**三维重建** → **语义标注** → **类别感知稠密化与体素化** → **真值采样**（见 Figure 2）。以下逐模块展开关键公式与设计逻辑。

### 三维重建（SfM + MVS）

给定地理参考图像集 $\mathcal{T}$、内参集 $\mathcal{K}$ 及位姿集 $\mathcal{T}$，通过经典 Structure‑from‑Motion 与 Multi‑View Stereo 获得度量级稠密点云 $\mathcal{P}$、逐帧深度图集 $\mathcal{D}$ 以及 2D‑3D 对应关系集 $\mathcal{A}$：

$$( \mathcal { P } , \mathcal { D } , \mathcal { A } ) = \Psi_{\mathrm{SfM+MVS}} ( \mathcal{T}, \mathcal{K}, \mathcal{T} ) \tag{1}$$

其中第 $n$ 帧的 2D‑3D 对应关系由透视投影约束给出：

$$\mathcal{A}_n = \{ ( (u,v), \mathbf{x} ) \mid (u,v,1)^\top \sim \mathbf{K}_n [ \mathbf{R}_n \mid \mathbf{t}_n ] [ \mathbf{x}^\top 1 ]^\top \} \tag{2}$$

**设计意图**：该模块完全规避 LiDAR，仅依赖相机图像生成度量三维几何，为后续语义提升提供精确的 2D‑3D 映射基础。实验表明，SfM+MVS 重建的平均重投影误差仅为 1.24 像素（Table 8），保证了三维几何精度。

### 语义标注（2D‑3D 标签提升）

该模块将少量手动标注的 2D 图像标签提升至三维点云，大幅降低人工成本。

**标注覆盖度**：设 $\mathcal{I}$ 为已标注图像子集，覆盖度 $\rho(\mathcal{I})$ 定义为被至少一张已标注图像观察到的三维点占比：

$$\rho(\mathcal{I}) = \frac{ | \{ \mathbf{x} \in \mathcal{P} \mid \exists n \in \mathcal{I}, \exists (u,v) \, \mathrm{s.t.} \, ((u,v),\mathbf{x}) \in \mathcal{A}_n \} | }{ |\mathcal{P}| } \tag{3}$$

实验证实，手动标注不到 10% 的图像即可覆盖超过 99% 的重构点云（Table 9, Sec. 3.3.2），验证了该策略的高效性。

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/016_Table_9.jpg]]
*Table 9: Scene-wise manual semantic annotation ratios for UAV platforms DJI Phantom 4 RTK (P4) [15] and DJI Mavic 3 Enterprise Series (M3-ES) [16]. Note that the number of acquired images marginally differs from the number of images finally provided in the dataset, as we remove images at the border of each reconstructed scene to ensure high geometric fidelity (see Sec. 8)*

**多视图证据融合**：对每个三维点，收集所有观察该点的已标注图像中的标签，通过无权多数投票确定最终标签；平局时按类别先验频率顺序打破僵局。未标注点通过 k‑近邻（kNN）以逆距离加权传播标签，随后再施加一轮 kNN 去噪，消除孤立误标点。

### 类别感知稠密化与体素化

语义点云仍存在稀疏和不完整问题，尤其对于实例和地物类别。该模块将语义类别划分为三个互斥组，分别采用差异化策略生成稠密占据集：

$$\mathcal{C}_{\mathrm{inst}} \cup \mathcal{C}_{\mathrm{gnd}} \cup \mathcal{C}_{\mathrm{oth}} = \mathcal{C}, \quad \mathcal{C}_{\mathrm{inst}} \cap \mathcal{C}_{\mathrm{gnd}} \cap \mathcal{C}_{\mathrm{oth}} = \emptyset \tag{4}$$

- **实例类别** ($\mathcal{C}_{\mathrm{inst}}$)：首先用类特定参数的 DBSCAN 将实例点云 $\mathcal{P}_{\mathrm{inst}}$ 分解为 $J$ 个实例：

$$\mathbb{S} = \mathrm{DBSCAN}(\mathcal{P}_{\mathrm{inst}}, \varepsilon_c, \mathrm{minPts}_c) = \{ S_j \subset \mathcal{P}_{\mathrm{inst}} \}_{j=1}^J \tag{8}$$

随后对每个实例 $S$，从多视图剪影反向投影构造视觉外壳锥体：

$$\mathcal{R}_k := \{ \mathbf{x} \in \mathbb{R}^3 : \pi_k(\mathbf{x}) \in \Omega_k \} \tag{9}$$

并取视觉外壳内部且位于包围盒内的体素作为实例占据集：

$$\mathcal{O}_{\mathrm{inst}}(S) = \{ \mathbf{v} \in \mathcal{G} \mid \operatorname{center}(\mathbf{v}) \in \mathcal{B}(S) \cap \mathcal{H}(S) \} \tag{10}$$

- **地物类别** ($\mathcal{C}_{\mathrm{gnd}}$)：对地面点云执行泊松表面重建，获得连续表面后体素化。
- **其他类别** ($\mathcal{C}_{\mathrm{oth}}$)：直接对点云进行体素化。

最终按 $\mathrm{inst} \succ \mathrm{oth} \succ \mathrm{gnd}$ 优先级解决标签冲突，聚合为场景级语义体素网格 $\mathbf{Y}$：

$$\mathbf{Y}(\mathbf{v}) = \begin{cases} \text{label from } \mathcal{O}_{\mathrm{inst}}, & \mathbf{v} \in \mathcal{O}_{\mathrm{inst}}, \\ \text{label from } \mathcal{O}_{\mathrm{oth}}, & \mathbf{v} \in \mathcal{O}_{\mathrm{oth}} \setminus \mathcal{O}_{\mathrm{inst}}, \\ \text{label from } \mathcal{O}_{\mathrm{gnd}}, & \mathbf{v} \in \mathcal{O}_{\mathrm{gnd}} \setminus (\mathcal{O}_{\mathrm{inst}} \cup \mathcal{O}_{\mathrm{oth}}), \\ 0, & \text{otherwise} \end{cases} \tag{13}$$

**设计意图**：实例类别通过视觉外壳雕刻恢复完整空间范围，地物类别通过泊松重建填补大面积空洞，其他类别直接体素化保持效率。优先级策略确保实例边界清晰、不被地面体素侵蚀。

### 真值采样（视锥体裁剪与栅格化）

给定场景级语义体素网格 $\mathbf{Y}$ 和每帧相机参数，通过视锥体裁剪和栅格化生成逐帧语义体素网格真值。同时构造三种二元掩码（类似 SemanticKITTI 的设计）：无效掩码 $M_n^{\mathrm{inv}}$、表面掩码 $M_n^{\mathrm{surf}}$ 和遮挡掩码 $M_n^{\mathrm{occ}}$，用于后续模型训练与评估中的有效区域约束。

**跨高度真值生成**：40 m 和 30 m 高度的真值通过对 50 m 场景级语义网格进行视锥体裁剪获得（Sec. 4.2），无需为每个高度重新运行完整流水线，保证了跨高度数据的一致性与生成效率。

### 补充图表

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/015_Table_8.jpg]]
*Table 8: Scene-wise root mean square (RMS) reprojection error after 3D reconstruction (Sec. 3.3.1)*

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/012_Table_6.jpg]]
*Table 6: Class-wise DBSCAN [20] parameters for instance separation, discussed in Sec. 3.3.3*

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/011_Table_7.jpg]]
*Table 7: Semantic class frequencies, group assignments (Sec. 3.3.3), and semantic color table of the OccuFly dataset*

## 实验与分析

### 基准实验设计

OccuFly基准覆盖9个真实航拍场景，包含城市、工业与乡村三类环境，采集于春、夏、秋、冬四季，飞行高度设定为30 m、40 m和50 m三个层级。数据集按场景划分训练集与测试集，确保跨场景泛化评估的公平性。每个样本提供RGB图像、度量深度图与语义占据网格，总计超过20 000个样本，涵盖21个语义类别（Table 1）。评估协议沿袭SemanticKITTI的设定，采用无效、表面与遮挡三种二元掩码，分别处理超出视锥体范围、位于场景边界表面和被前景遮挡的体素。

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/003_Table_1.jpg]]
*Table 1: OccuFly dataset statistics, discussed in Sec. 4.2*

### 语义场景补全评估

在OccuFly测试集上，我们评估了两个代表性SSC方法——**Symphonies**和**DISC**的跨高度性能（Table 4）。DISC在全高度上的IoU仅为29.52，mIoU低至2.04；Symphonies表现更差，IoU仅13.68，mIoU为0.58。这一结果揭示了航拍SSC的极端挑战性：现有模型在室内或地面驾驶场景中尚可运作，但在大范围、高空俯视的航拍领域几乎完全失效。按高度细分来看，模型在50 m高度上的性能略优于30 m和40 m，这可能是由于更高视角下场景几何结构更为规整，但整体性能仍然远未达到实用水平。

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/007_Table_4.jpg]]
*Table 4: Altitude-wise quantitative SSC evaluation for DISC [53] and Symphonies [36] on the OccuFly test set, discussed in Sec. 5.2*

定性结果（Figure 4）进一步印证了定量结论。DISC在车辆、建筑物等大尺寸类别上偶尔能产生合理的占据预测，但对于细小结构（如杆状物、围栏）和语义模糊区域（如植被与地面的边界）几乎完全失败。模型倾向于将大部分体素预测为地面或空类别，严重缺乏对实例级目标的感知能力。

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/009_Figure_4.jpg]]
*Figure 4: Visual SSC examples and qualitative SSC evaluation for DISC [53] on the OccuFly test set, discussed in Sec. 5.3*

### 深度估计评估

单目度量深度估计是航拍SSC的重要前置任务。我们在OccuFly测试集上评估了多个深度基础模型的零样本与微调性能（Table 5）。零样本设置下，所有模型均表现出严重的领域差距：**DepthAnything-v2**的AbsRel高达0.729，RMSE为28.382；**Metric3D-v2**和**Map-Anything-v1.1**同样表现不佳。这一现象的根本原因在于，现有深度基础模型几乎完全基于地面视角数据训练，缺乏对航拍几何先验（如绝对尺度、俯视透视）的建模能力。

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/008_Table_5.jpg]]
*Table 5: Depth estimation evaluation, comparing zero-shot vs. finetuned foundation models on the OccuFly test set (see Sec. 5.2)*

在OccuFly训练集上微调后，DepthAnything-v2的性能大幅提升，AbsRel降至0.134，RMSE降至4.844，但仍未达到完美水平。定性对比（Figure 5）显示，零样本模型在建筑边缘和细长结构处产生严重的深度畸变，而微调后模型能够恢复合理的场景几何，但在远距离区域和语义边界处仍存在系统性偏差。这表明，航拍度量深度估计需要专门的模型设计与训练策略，简单的领域微调只能部分缓解问题。

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative evaluation of zero-shot and fine-tuned depth estimation for DepthAnything2 [89] on OccuFly test set (Sec. 5.3)*

### 数据生成流水线验证

OccuFly的核心贡献之一是基于纯相机数据的高质量真值生成流水线。我们从三个维度验证了流水线的可靠性：

**几何精度**：SfM+MVS重建在9个场景上的平均重投影误差仅为1.24像素（Table 8），各场景的RMS误差均控制在1.5像素以内。这一精度水平与地面LiDAR重建相当，为后续语义标注提供了可靠的几何基础。相比之下，零样本深度基础模型DepthAnything-v3在OccuFly上的平均度量尺度偏差高达526%（Figure 3），进一步证实了经典SfM+MVS在航拍场景下的不可替代性。

**标注效率**：手动标注不到10%的图像即可覆盖超过99%的三维重建点（Table 9与Sec. 3.3.2）。具体而言，各场景的标注图像比例在6.5%到9.2%之间，对应的三维点覆盖率均超过99%。这一高效性源于航拍图像的高重叠率（通常>90%，Figure 11），使得少量标注即可通过多视图几何传播至绝大多数三维点。此外，手动标注与RTK渲染语义点云的逐像素一致性达到92%（Sec. 4.3），验证了标注质量。

**语义体素化完整性**：类别感知的稠密化与体素化流程（Sec. 3.3.3）有效提升了实例和地物类别的空间完整性。对于车辆、建筑等实例类别，视觉外壳雕刻能够填补因遮挡或MVS失败造成的点云空洞；对于地面、道路等地物类别，泊松表面重建提供了连续的水密表面。Figure 6展示了9个场景的完整流水线输出，从RGB点云到语义点云再到语义体素网格，验证了从稀疏语义点到密集占据网格的转换质量。

### 消融与敏感性分析

**标注比例与覆盖率关系**：Table 9的数据表明，标注比例从6.5%增加到9.2%时，覆盖率始终维持在99%以上，说明标注效率对具体比例不敏感。这一特性源于航拍图像的高重叠率设计，使得标注策略具有良好的鲁棒性。

**类别分组策略的影响**：将21个语义类别划分为实例组（如车辆、建筑）、地面组（如道路、草地）和其他组（如天空、植被）是稠密化流程的关键设计（Table 7）。实例组采用视觉外壳雕刻，能够有效恢复被遮挡的完整目标形状；地面组采用泊松重建，保证了地形的连续性。若将所有类别统一处理（例如全部直接体素化），则会导致实例目标内部空洞和地面表面断裂，严重影响真值质量。

**DBSCAN参数敏感性**：实例分离依赖类特定的DBSCAN参数（Table 6）。不同类别的空间分布差异显著——车辆类点云密集且聚类半径小（ε=0.3 m），建筑类则需要更大的邻域半径（ε=1.0 m）以适应稀疏的墙面点云。参数选择对最终实例分割质量有直接影响，但论文未提供系统的参数敏感性实验，这一点需要读者在实际使用中根据自身数据特性进行调优。

### 失败模式与局限性

尽管OccuFly在航拍SSC基准构建上取得了突破，数据生成流水线仍存在若干已知局限：

1. **静态场景假设**：流水线假设场景在采集期间保持静态，因此动态物体（如移动车辆、行人）会被抑制或产生伪影。在城市场景中，这可能导致部分车辆的语义标注不完整或位置偏移。

2. **时序不一致性**：跨高度采集时，不同高度层次的图像可能在不同时间拍摄，导致光照变化、植被生长和物体位移等问题。这种时序不一致性在30 m和40 m的真值中表现为局部几何与语义的不匹配。

3. **标注自动化程度**：当前流程仍需约6%–9%的手动精细标注。虽然相比全3D标注已大幅降低人工成本，但完全自动化的标注方案（如基于鲁棒二维伪标签的零人工标注）仍有待探索。

4. **模型性能的极端低下**：SSC模型在OccuFly上的mIoU仅约2%，说明现有方法几乎无法处理航拍场景。这既是基准的挑战性所在，也意味着当前的评估指标可能对模型改进不够敏感——需要更细粒度的类别级和实例级评估来指导算法研发。

### 补充图表

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/006_Figure_3.jpg]]
*Figure 3: Evaluation of our classical 3D reconstruction compared to DepthAnything3 [51] foundation model, detailed in Sec. 4.3*

![[assets/figures/papers/paper_list_l2048_https_arxiv_org_abs_2512_20770/figures/013_Figure_6.jpg]]
*Figure 6: Scene-level outputs of our proposed data generation framework for all scenes 1-9 of the OccuFly dataset. Left: RGB pointcloud from 3D reconstruction (Sec. 3.3.1). Center: Semantic point cloud from semantic annoation (Sec. 3.3.2). Right: Semantic voxel grid from densification and voxelization (Sec. 3.3.3). Zoom in for best view*

## 方法谱系与知识库定位

### 任务定位与领域瓶颈

OccuFly解决的是**航拍视角下的三维语义场景补全（SSC）**任务。传统SSC的研发与评估严重依赖车载LiDAR构建的真值（如SemanticKITTI），但无人机平台因载荷、功耗和点云在远距离的稀疏性，几乎无法获得可用的LiDAR真值。与此同时，现有的SSC模型（如Symphonies、DISC）和视觉基础模型（如DepthAnything系列）均在驾驶场景或地面视角数据上训练，直接零样本迁移至航拍领域时遭遇严重的领域差距。OccuFly正是在这一双重空白上建立的首个真实世界航拍SSC基准，其核心贡献在于**数据生成范式**而非SSC模型本身。

### 数据生成范式：从LiDAR依赖到纯相机流水线

OccuFly的数据生成流水线实现了三个关键范式转换，构成其方法学上的主要创新：

| 设计维度 | 传统SSC基准（如SemanticKITTI） | OccuFly |
|---------|-------------------------------|---------|
| 三维重建模态 | LiDAR点云累积 | 纯相机SfM+MVS（平均重投影误差1.24像素） |
| 语义标注方式 | 繁重的3D点云逐点标注 | 少量2D图像标注（<10%）+多视图标签提升至3D（覆盖>99%点云） |
| 点云稠密化策略 | LiDAR多帧累积 | 类别感知的实例视觉外壳雕刻+地物泊松表面重建 |

该流水线由四个串行模块构成（参见Figure 2）：（1）**三维重建**——利用地理参考图像经SfM与MVS生成度量稠密点云$\mathcal{P}$、逐帧深度图集$\mathcal{D}$和2D-3D对应关系集$\mathcal{A}$；（2）**语义标注**——手动标注少量图像，通过反向投影将2D标签提升至3D点，并以无加权多数投票融合多视图证据，未标注点通过kNN传播并去噪；（3）**类别感知稠密化与体素化**——将语义类别划分为实例（$\mathcal{C}_{\mathrm{inst}}$）、地面（$\mathcal{C}_{\mathrm{gnd}}$）和其他（$\mathcal{C}_{\mathrm{oth}}$）三组，对实例类采用DBSCAN分离后视觉外壳雕刻，对地物类采用泊松表面重建，按实例≻其他≻地面的优先级融合为场景级语义体素网格$\mathbf{Y}$；（4）**真值采样**——通过视锥体裁剪和栅格化生成每帧的语义体素网格，并构造无效、表面和遮挡三种二元掩码。

### 与现有工作的关系

**相对于SSC基准数据集**：OccuFly与SemanticKITTI、KITTI-360等地面SSC基准形成互补而非替代关系。前者针对驾驶场景、LiDAR真值、近距离感知；后者面向航拍场景、纯相机真值、远距离俯视感知。Table 2系统对比了二者在传感器模态、场景规模、类别数、高度变化等维度的差异。

**相对于SSC方法**：论文将**Symphonies**和**DISC**作为基线在OccuFly上评估，结果（Table 4）表明二者性能均极低——DISC的IoU仅29.52、mIoU仅2.04，Symphonies更低（13.68/0.58）。这一结果并非否定这些方法的设计，而是揭示了**训练数据领域差异**带来的根本性泛化障碍。OccuFly为未来航拍SSC方法提供了必要的训练和评估平台。

**相对于单目深度估计基础模型**：论文评估了**DepthAnything-v2**、**DepthAnything-v3**、**Metric3D-v2**和**Map-Anything-v1.1**等模型在OccuFly上的零样本与微调性能。零样本下，DepthAnything-v2的AbsRel高达0.729，DepthAnything-v3的平均度量尺度偏差达526%（Figure 3），证实了严重的领域差距。微调后DepthAnything-v2的AbsRel降至0.134，但仍不完美，说明航拍深度估计本身构成了独立的研究挑战。

### 适用边界与局限

1. **静态场景假设**：数据生成流水线假设场景为静态，因此抑制了真正的动态物体（如移动车辆、行人）。这限制了OccuFly在动态场景理解任务上的直接适用性。
2. **时序一致性风险**：跨高度（30 m、40 m、50 m）采集时可能使用不同时间拍摄的图像，引入时序不一致问题，影响多高度真值的几何一致性。
3. **标注自动化程度**：当前仍需少量人工2D标注（<10%图像），尽管已大幅降低人工成本，但完全自动化标注（如通过鲁棒的二维伪标签）尚未实现，制约了数据生成规模的进一步扩展。
4. **场景与平台覆盖**：OccuFly覆盖城市、工业、乡村三类环境与春夏秋冬四季，但场景总数（9个）和无人机平台种类（Phantom 4 RTK与Mavic 3 Enterprise Series）仍有限，向更多样化的地理区域和传感器配置的泛化能力有待验证。

### 开放问题与后续方向

1. **动态目标处理**：如何集成动态三维重建方法（如4D Gaussian Splatting）以在数据生成流水线中保留和处理动态对象，是扩展OccuFly适用场景的关键。
2. **时序一致性缓解**：如何通过图像选择策略或时空联合优化来缓解跨高度数据采集带来的时序不一致性，需要进一步研究。
3. **全自动标注流水线**：使用鲁棒的二维伪标签（如基于Segment Anything等基础模型的自动分割）完全替代人工标注，有望将数据生成成本降至接近零，使大规模航拍SSC数据构建成为可能。
4. **航拍SSC方法设计**：现有SSC模型在OccuFly上的极低性能表明，需要针对航拍视角的独特特性（大范围场景、俯视视角、尺度变化剧烈）设计专门的SSC架构与训练策略，这是一个开放的研究方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/OccuFly_A_3D_Vision_Benchmark_for_Semantic_Scene_Completion_from_the_Aerial_Perspective.pdf]]