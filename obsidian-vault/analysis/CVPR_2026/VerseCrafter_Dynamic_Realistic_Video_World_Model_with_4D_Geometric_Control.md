---
title: "VerseCrafter: Dynamic Realistic Video World Model with 4D Geometric Control"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VerseCrafter_Dynamic_Realistic_Video_World_Model_with_4D_Geometric_Control.pdf
project_link: "https://sixiaozheng.github.io/VerseCrafter_page/"
code_link: null
aliases:
- VerseCrafter
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 引入4D Geometric Control表示（静态背景点云 + 每对象3D高斯轨迹），将场景抽象为可编辑的4D几何状态，并通过轻量GeoAdapter将多通道4D控制图注入冻结的视频扩散模型。
primary_logic: 通过将动态场景解耦为静态背景点云和每对象3D高斯轨迹，并将它们渲染为背景RGB/深度、轨迹RGB/深度和软合并掩码，形成统一的4D控制图，从而使视频扩散模型能够生成视角一致且精确遵循相机与对象运动的高质量视频。
claims:
- 在VerseControl4D联合控制任务上，VerseCrafter取得VBench-I2V总体88.10的最高分，且旋转误差0.890、平移误差3.103、对象运动控制误差2.507，均大幅优于Perception-as-Control、Uni3C和Yume。
- 在仅相机控制的静态场景测试中，VerseCrafter总体得分86.80，旋转误差0.650，平移误差2.587，显著低于ViewCrafter、Voyager和FlashWorld的最佳基线。
- 消融实验证明3D高斯轨迹在对象运动控制上（ObjMC 2.507）明显优于3D边界框（ObjMC 4.520）和3D点轨迹（ObjMC 6.896）；移除深度信息导致旋转误差从0.890升至1.177，合并背景与前景控制则使ObjMC升至3.726。
- VerseControl4D (联合相机与对象运动控制) 上 VBench-I2V Overall Score = 88.10
---

# VerseCrafter: Dynamic Realistic Video World Model with 4D Geometric Control

> [!tip] 核心洞察
> 通过将动态场景解耦为静态背景点云和每对象3D高斯轨迹，并将它们渲染为背景RGB/深度、轨迹RGB/深度和软合并掩码，形成统一的4D控制图，从而使视频扩散模型能够生成视角一致且精确遵循相机与对象运动的高质量视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | VerseCrafter：具有4D几何控制的动态逼真视频世界模型 |
| 英文题名 | VerseCrafter: Dynamic Realistic Video World Model with 4D Geometric Control |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.05138) · [Project](https://sixiaozheng.github.io/VerseCrafter_page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | VerseCrafter |
| Dataset | VerseControl4D |

> [!tip] 效果简介
> - VerseControl4D (联合相机与对象运动控制) 上，VBench-I2V Overall Score 88.10 vs 83.66 (Perception-as-Control) / 85.47 (Yume) / 83.55 (Uni3C) (+4.44 相对于 Perception-as-Control)。
> - VerseControl4D (联合控制) 上，旋转误差 RotErr 0.890 vs 5.006 (Perception-as-Control) / 7.560 (Yume) / 1.361 (Uni3C) (-4.116 相对于 Perception-as-Control)；平移误差 TransErr 3.103 vs 8.767 (Perception-as-Control) / 8.735 (Yume) / 7.731 (Uni3C) (-5.664 相对于 Perception-as-Control)；对象运动控制误差 ObjMC 2.507 vs 6.556 (Perception-as-Control) / 7.959 (Yume) / 5.883 (Uni3C) (-4.049 相对于 Perception-as-Control)。
> - VerseControl4D 静态场景 (仅相机控制) 上，VBench-I2V Overall Score 86.80 vs 84.04 (ViewCrafter) / 85.33 (FlashWorld) / 78.12 (Voyager) (+1.47 相对于最佳基线 FlashWorld)。

## 概要

**核心问题**：现有视频世界模型缺乏统一的4D几何表示，难以在共享世界坐标系下同时精确控制相机运动与多对象运动。主流控制信号（如2D边界框、光流、深度图）具有视点依赖性和非刚性，而3D边界框或参数化模型（如SMPL-X）则过于刚硬或类别受限，无法兼顾通用性与精度。

**核心方法**：VerseCrafter 提出 **4D Geometric Control** 表示——将动态场景解耦为**静态背景点云**与**每对象3D高斯轨迹**，在共享世界坐标系中统一描述相机与多对象运动。通过将这一可编辑的4D几何状态渲染为多通道控制图（背景RGB/深度、轨迹RGB/深度、软合并掩码），并经轻量 **GeoAdapter** 以残差调制方式注入冻结的 Wan2.1-14B 视频扩散主干，实现视角一致且精确遵循几何控制的高质量视频生成。

**核心结果**：
- 在联合相机与对象运动控制的 VerseControl4D 基准上，VerseCrafter 取得 VBench-I2V 总体 **88.10** 分，旋转误差 **0.890**、平移误差 **3.103**、对象运动控制误差 **2.507**，全面优于 Perception-as-Control、Uni3C 和 Yume。
- 在仅相机控制的静态场景测试中，总体得分 **86.80**，旋转误差 **0.650**、平移误差 **2.587**，显著超越 ViewCrafter、Voyager 和 FlashWorld 等最佳基线。
- 消融实验证实：3D高斯轨迹在对象运动控制上明显优于3D边界框和3D点轨迹；深度信息的引入对恢复正确遮挡关系至关重要；解耦的背景与前景控制是维持静态背景稳定性的关键。

视频世界模型旨在从给定输入（如图像、文本或动作指令）生成逼真且可控的动态视频，其核心挑战在于如何在统一的几何框架下同时精确控制相机运动与多对象运动。近年来，基于扩散模型的视频生成取得了显著进展，涌现出两类主要的控制范式：**仅相机控制**与**仅对象运动控制**。然而，将二者统一到一个共享世界坐标系中的方法仍然缺失，这构成了当前视频世界模型的核心瓶颈。

**仅相机控制方法**（如 ViewCrafter、Voyager、FlashWorld）通常假设场景为静态，通过估计或给定的相机轨迹生成新视角视频。这类方法在静态场景下表现良好，但无法处理场景中独立运动的前景对象。**仅对象运动控制方法**则依赖 2D 边界框、光流、稀疏点轨迹或参数化人体模型（如 SMPL-X）来驱动对象运动。例如，Uni3C 使用 SMPL-X 参数模型控制人体运动，但受限于单一人类类别且缺乏相机控制；Yume 通过文本描述粗略引导对象运动，但无法精确控制相机轨迹；Perception-as-Control 采用 2D 边界框作为控制信号，但 2D 信号本质上是视点依赖且非刚性的，难以在相机运动时保持几何一致性。

这些方法的根本局限在于**缺乏统一的 4D 几何表示**。具体而言：
- **2D 控制信号**（边界框、掩码、光流）随视点变化，无法在相机运动时维持对象运动的几何一致性；
- **3D 边界框**过于刚硬，无法刻画对象的形状、大小与朝向随时间的变化；
- **参数化模型**（如 SMPL-X）类别受限，难以泛化到任意对象类别；
- **稀疏 3D 点轨迹**缺乏对对象空间范围和朝向的显式建模，容易导致尺度漂移和运动失准。

上述缺口导致现有方法在**联合相机与多对象运动控制**任务上表现不佳：要么牺牲相机精度以迁就对象运动，要么在对象运动控制中丧失几何一致性。因此，亟需一种能够在共享世界坐标系下统一表示静态背景与动态前景、支持视点无关精确控制的 4D 几何表示。

VerseCrafter 针对这一瓶颈，提出**4D Geometric Control** 表示——将动态场景解耦为**静态背景点云**和**每对象 3D 高斯轨迹**，并在共享世界坐标系中联合建模。这一表示具有三个关键特性：
1. **视点无关**：所有几何实体定义在世界坐标系中，相机运动通过重投影自然处理，无需逐帧调整控制信号；
2. **类别无关**：3D 高斯轨迹仅需从对象点云拟合，不依赖任何类别先验，适用于任意刚性或近似刚性对象；
3. **紧凑可编辑**：每个对象由一系列 3D 高斯分布（均值+协方差）描述，编码位置、形状、大小与朝向的时变信息，支持直观的轨迹编辑。

通过将 4D Geometric Control 渲染为多通道 4D 控制图（背景 RGB/深度、轨迹 RGB/深度、软合并掩码），并经由轻量 GeoAdapter 注入冻结的视频扩散主干（Wan2.1-14B），VerseCrafter 实现了视角一致且精确遵循相机与对象运动的高质量视频生成。这一设计从几何表示层面解决了联合控制的根本矛盾，为视频世界模型走向统一 4D 可控生成提供了新路径。

## 核心方法与创新机理

VerseCrafter 的核心创新在于，它首次为视频世界模型引入了一套统一的 **4D几何控制（4D Geometric Control）** 表示，将相机运动与多对象运动纳入同一个共享世界坐标系中进行精确控制。这一设计直击现有方法的瓶颈：2D 控制信号（如边界框、掩码、光流）视点依赖且非刚性，而 3D 边界框或参数化模型（如 SMPL-X）又过于刚硬或类别受限，无法在保持视觉质量的同时，实现视角一致的相机与多对象联合控制。

### 关键 changed slots

| 设计维度 | 现有基线方法 | VerseCrafter 的改进 | 证据锚点 |
|---|---|---|---|
| **对象运动表示** | 3D 边界框、稀疏 3D 点轨迹、SMPL-X 参数模型 | 每对象 **3D 高斯轨迹**（均值 + 协方差），编码位置、形状、大小与朝向随时间演化 | Section 3.1, Figure 6, Table 3 |
| **控制信号形式** | 2D 边界框/掩码/光流/深度图 | **多通道 4D 控制图**（背景 RGB/深度、3D 高斯轨迹 RGB/深度、软合并掩码），通过 3D 渲染生成 | Section 3.1–3.2, Figure 2 |
| **背景建模方式** | 静态场景假设或无显式背景模型 | **静态背景点云**，支持相机运动时的显式重投影与解耦控制 | Section 3.1, Figure 2 |
| **条件注入机制** | 文本嵌入或简单控制信号拼接 | 轻量 **GeoAdapter**（DiT 风格分支），以残差调制方式将 4D 几何特征注入冻结的 Wan-DiT 块 | Section 3.2, Figure 9 |

### 核心机制解析

**1. 4D 几何控制表示：将场景抽象为可编辑的几何状态**

VerseCrafter 将动态场景解耦为两个互补的几何组件：

- **静态背景点云** $P^{\mathrm{bg}}$：从输入图像通过单目深度估计（MoGe-2）和像素反投影构建（Eq. 1），作为场景的“几何支架”，在相机运动时通过重投影保持背景的视角一致性。
- **每对象 3D 高斯轨迹** $\{\mathcal{G}_o^t\}_{t=1}^T$：对每个用户指定的前景对象，从第一帧的对象点云拟合全协方差 3D 高斯（Eq. 5），并用一系列时变高斯分布描述其位置与空间范围的演化（Eq. 4）。这种表示天然编码了对象的平移、缩放和旋转，且类别无关、无需参数化人体模型。

两者被统一在共享世界坐标系中，形成可独立编辑的 4D 几何场景状态——用户可以分别操控相机轨迹和每个对象的运动路径，而无需担心 2D 投影空间的歧义性。

**2. 多通道 4D 控制图：将几何知识“翻译”为扩散模型可理解的条件**

4D 几何控制本身是抽象的数学表示，无法直接输入视频扩散模型。VerseCrafter 的关键设计是将它们渲染为多通道的 2D 控制图序列：

- **背景 RGB 与深度图**：从背景点云渲染，提供静态场景的几何与外观参考。
- **3D 高斯轨迹 RGB 与深度图**：从每个对象的高斯轨迹渲染，明确编码前景对象的运动与深度排序。
- **软合并掩码**：将背景与前景控制图融合为统一的逐帧条件，同时保留解耦信息。

消融实验证实，**深度信息的引入对恢复正确的遮挡关系至关重要**：移除深度后，旋转误差从 0.890 升至 1.177，对象运动控制误差 ObjMC 从 2.507 恶化至 4.929（Table 3, Figure 7）。同样，**解耦的背景与前景控制**对维持静态背景和稳定对象运动必不可少：将两者合并为单一控制图后，ObMC 升至 3.726，并出现明显运动退化（Table 3, Figure 8）。

**3. GeoAdapter：零初始化残差调制实现稳定条件注入**

VerseCrafter 采用冻结的 Wan2.1-14B 作为视频扩散主干，仅训练一个轻量的 GeoAdapter 分支。GeoAdapter 的每个块从对应 Wan-DiT 块的权重初始化，并通过零初始化的投影矩阵 $\mathbf{W}_0^{(m)}$ 将几何特征作为残差调制叠加到主干特征上（Section B）：

$$x_{n+1} = \mathcal{B}_n(x_n) + \mathcal{G}_m(\mathbf{g}) \mathbf{W}_0^{(m)}$$

这种设计确保训练初期几何条件的影响为零，模型从预训练的视频先验平稳过渡到几何感知生成，避免了条件注入导致的训练不稳定。

### 对象运动表示的选择：为什么是 3D 高斯轨迹？

消融实验（Table 3, Figure 6）给出了清晰的答案：在相同的模型架构和训练设置下，3D 高斯轨迹在对象运动控制误差 ObjMC 上取得 2.507，显著优于 3D 边界框的 4.520 和 3D 点轨迹的 6.896。定性结果进一步显示，3D 点轨迹容易导致尺度漂移，3D 边界框则产生运动错位，而 3D 高斯轨迹能更好地保持对象形状并遵循目标运动路径。这是因为高斯分布同时编码了对象的位置（均值）和空间范围/朝向（协方差），为扩散模型提供了更丰富的几何先验。

### 创新边界与局限

尽管 4D 几何控制实现了相机与多对象运动的统一操控，当前的对象表示仍限于单个 3D 高斯的椭圆体级别控制，无法实现精细的 6D 姿态或部件级关节控制。背景点云基于第一帧重建，作为近似静态的几何支架，难以处理大规模非刚性背景变形。此外，生成过程中未施加显式物理约束，可能导致物理直觉上不合理的运动。这些局限为未来工作指明了方向：引入多部分组成的高斯或骨架驱动变形以实现精细关节控制，显式建模动态背景的非刚性变形，以及融入物理先验提升复杂交互的合理性。

VerseCrafter 的整体设计遵循“显式4D几何状态构建—多通道控制图渲染—冻结视频扩散主干条件注入”的三阶段范式。其核心思路是：将动态场景抽象为共享世界坐标系下的**4D几何控制表示**，再通过渲染将其转化为扩散模型可消费的控制信号，从而在保持强视频先验的同时，实现相机运动与多对象运动的精确、解耦控制。

### 输入与预处理

给定一张输入图像和一段文本提示，框架首先调用两个现成模块完成场景的几何与语义初始化：

- **单目深度估计**：使用 MoGe-2 估计逐像素深度 $D_1(\mathbf{u})$ 及相机内参 $\mathbf{K}$，为后续反投影提供3D几何基础。
- **对象掩码生成**：由 Grounded SAM2 根据用户指定的对象类别或文本描述，自动输出每个对象的二值掩码 $\{M_o\}$。

### 4D几何控制构建

这是 VerseCrafter 的核心创新环节，将2D观测提升为可编辑的4D几何场景状态。该过程分为三步：

1. **背景点云重建**：利用第一帧的相机位姿（设为世界坐标系原点），将每个像素 $\mathbf{u}$ 按其深度值反投影到3D世界空间：
   $$\mathbf{p}(\mathbf{u}) = \mathbf{R}_1^{\top} \big( D_1(\mathbf{u}) \mathbf{K}^{-1} \mathbf{u} - \mathbf{t}_1 \big)$$
   所有不属于任何对象的像素反投影点构成**静态背景点云** $P^{\mathrm{bg}}$，作为场景的几何支架。

2. **每对象点云划分**：对每个对象 $o$，利用其掩码 $M_o$ 从完整点云中提取对应的点集：
   $$P_o = \big\{ \mathbf{x}_{o,k} \mid \mathbf{x}_{o,k} = \mathbf{p}(\mathbf{u}_k), \mathbf{u}_k \in M_o \big\}$$

3. **3D高斯轨迹拟合**：对每个对象点云 $P_o$，从第一帧拟合一个全协方差3D高斯作为其初始空间分布：
   $$\pmb{\mu}_o = \frac{1}{N_o} \sum_{k} \mathbf{x}_{o,k}, \quad \pmb{\Sigma}_o = \frac{1}{N_o} \sum_{k} (\mathbf{x}_{o,k} - \pmb{\mu}_o)(\mathbf{x}_{o,k} - \pmb{\mu}_o)^{\top}$$
   该高斯随时间演化的均值和协方差序列 $\{\mathcal{G}_o^t\}_{t=1}^T$ 构成了**每对象3D高斯轨迹**，编码了对象的位置、形状、大小与朝向变化。

至此，场景被抽象为“静态背景点云 + 每对象3D高斯轨迹”的4D几何控制表示，所有几何实体共享同一世界坐标系，使得相机轨迹与对象运动可以在此统一框架下联合编辑。

### 4D控制图渲染

在给定目标相机轨迹后，系统从4D几何控制中逐帧渲染出多通道的**4D控制图**，作为扩散模型的条件信号。渲染输出包括：

- **背景RGB图与深度图**：从背景点云重投影得到，提供静态场景的几何与外观参考。
- **3D高斯轨迹RGB图与深度图**：从各对象的3D高斯渲染得到，编码前景对象的运动与形状信息。
- **软合并掩码**：将背景与前景渲染结果融合为统一的帧级控制图，同时保留前景/背景的解耦边界。

这种渲染策略的关键优势在于：控制信号在3D空间中生成，天然具有视角一致性，且背景与前景的解耦渲染为后续的条件注入提供了结构化的几何引导。

### GeoAdapter条件注入

渲染得到的4D控制图通过一个轻量的**GeoAdapter**分支注入冻结的视频扩散主干。具体流程为：

1. **几何特征编码**：背景RGB/深度图和轨迹RGB/深度图分别由冻结的 Wan Encoder 编码为潜在空间特征；软合并掩码被重排为与潜在空间对齐的通道，所有几何潜在特征沿通道维度拼接，形成统一的时空几何张量。
2. **DiT风格条件分支**：GeoAdapter 是一个轻量的 DiT 风格网络，对该几何张量进行分块标记化处理后，提取多尺度的几何条件特征。
3. **残差调制注入**：在选定的 Wan-DiT 块（每隔 $k=5$ 层），GeoAdapter 的输出通过零初始化的线性投影层，以残差形式叠加到主干网络的令牌上：
   $$x_{n+1} = \mathcal{B}_n(x_n) + \mathcal{G}_m(\mathbf{g}) \mathbf{W}_0^{(m)}$$
   零初始化确保了训练初期几何条件的影响从零开始平滑增长，不会破坏预训练的视频先验。

### 训练与推理配置

整个框架基于 **Wan2.1-14B** 的潜在视频扩散主干构建，该主干在训练期间保持完全冻结，仅更新 GeoAdapter 分支的参数。每个 GeoAdapter 块由其配对的 Wan-DiT 块权重初始化，以稳定训练过程。推理时，用户可通过编辑4D几何控制表示（如修改对象高斯轨迹或相机路径）来交互式地控制生成视频的运动行为，而背景点云和3D高斯轨迹可在同一场景的多次编辑中复用，降低重复计算开销。

### 补充图表

![[assets/figures/papers/paper_list_l2624_https_arxiv_org_abs_2601_05138/figures/002_Figure_2.jpg]]
*Figure 2: Framework of VerseCrafter. Given an input image and a text prompt, we estimate depth and obtain user-specified object masks to construct 4D Geometric Control consisting of a static background point cloud and per-object 3D Gaussian trajectories in a shared world coordinate frame. A camera trajectory is specified in the shared frame, and together with the 4D Geometric Control, rendered into per-frame background RGB/depth, 3D Gaussian trajectory RGB/depth, and a soft merged mask, forming multi-channel 4D control maps. The 4D control maps are encoded and fed into the proposed GeoAdapter, which conditions a frozen Wan2.1-14B backbone together with text embeddings from umT5, enabling geometry-con...*

VerseCrafter 的核心由两个紧密耦合的模块构成：**4D几何控制表示**（4D Geometric Control）和**GeoAdapter条件注入分支**。前者将动态场景抽象为共享世界坐标系下的显式4D几何状态，后者将渲染得到的多通道控制图编码后注入冻结的视频扩散模型，实现精确的相机与多对象运动控制。

### 4D几何控制表示

给定输入图像，首先使用 MoGe-2 估计单目深度 $D_1(\mathbf{u})$ 和相机内参 $\mathbf{K}$，并利用 Grounded SAM2 获取用户指定的对象掩码 $\{M_o\}$。将第一帧的每个像素反投影到世界坐标系，构建场景点云：

$$
\mathbf{p}(\mathbf{u}) = \mathbf{R}_{1}^{\top} \big( D_{1}(\mathbf{u}) \mathbf{K}^{-1} \mathbf{u} - \mathbf{t}_{1} \big) \tag{1}
$$

其中 $\mathbf{R}_1$ 和 $\mathbf{t}_1$ 为第一帧的相机外参，$\mathbf{u} = (u, v, 1)^{\top}$ 为像素齐次坐标。通过对象掩码将完整点云划分为每对象点云和背景点云：

$$
P_{o} = \big\{ \mathbf{x}_{o,k} \big| \mathbf{x}_{o,k} = \mathbf{p}(\mathbf{u}_k), \mathbf{u}_k \in M_{o} \big\} \tag{2}
$$

$$
P^{\mathrm{bg}} = \left\{ \mathbf{p}(\mathbf{u}) \vert \mathbf{u} \not\in \bigcup_{o} M_{o} \right\} \tag{3}
$$

背景点云 $P^{\mathrm{bg}}$ 被视作静态几何支架，在相机运动过程中通过显式重投影维持视角一致性。对每个对象 $o$，从第一帧的点云 $P_o$ 拟合一个全协方差 3D 高斯，作为其初始空间分布：

$$
\pmb{\mu}_{o} = \frac{1}{N_{o}} \sum_{k} \mathbf{x}_{o,k}, \quad \pmb{\Sigma}_{o} = \frac{1}{N_{o}} \sum_{k} (\mathbf{x}_{o,k} - \pmb{\mu}_{o}) (\mathbf{x}_{o,k} - \pmb{\mu}_{o})^{\top} \tag{5}
$$

其中 $N_o$ 为对象点云的点数，$\pmb{\mu}_o$ 编码 3D 位置，$\pmb{\Sigma}_o$ 编码空间范围与朝向。随时间演化的对象运动由一系列 3D 高斯轨迹表示：

$$
\{ \mathcal{G}_{o}^{t} \}_{t=1}^{T}, \quad \mathcal{G}_{o}^{t}(\mathbf{x}) = \mathcal{N}(\mathbf{x} \mid \pmb{\mu}_{o}^{t}, \pmb{\Sigma}_{o}^{t}) \tag{4}
$$

在共享世界坐标系中指定相机轨迹后，将背景点云和每对象 3D 高斯轨迹渲染为逐帧的多通道 4D 控制图：背景 RGB/深度图、轨迹 RGB/深度图，以及软合并掩码。软合并掩码用于在后续扩散生成中平滑融合前景与背景区域。

### GeoAdapter 条件注入

4D 控制图首先被冻结的 Wan Encoder 编码为潜在特征，软合并掩码被重排为与潜在空间对齐的通道，所有几何潜在沿通道维度拼接形成统一的时空几何张量。该张量被切块（patchify）为 token 序列，送入轻量 DiT 风格的 GeoAdapter 分支处理。

GeoAdapter 的每个模块从对应 Wan-DiT 块的权重初始化，以稳定训练。在选定的 Wan-DiT 层（每 5 层插入一个，即 $k=5$），GeoAdapter 的输出通过零初始化的线性投影层作为残差调制叠加到主干 token 上：

$$
x_{n+1} = \mathcal{B}_n(x_n) + \mathcal{G}_m(\mathbf{g}) \mathbf{W}_0^{(m)}
$$

其中 $\mathcal{B}_n$ 为 Wan-DiT 的第 $n$ 个块，$\mathcal{G}_m$ 为第 $m$ 个 GeoAdapter 块，$\mathbf{g}$ 为几何特征，$\mathbf{W}_0^{(m)}$ 为零初始化的投影矩阵。零初始化确保训练初期几何条件从零开始逐步注入，避免破坏预训练的视频先验。整个 Wan2.1-14B 主干保持冻结，仅更新 GeoAdapter 参数，从而以较低的训练代价赋予模型精确的 4D 几何控制能力。

### 补充图表

![[assets/figures/papers/paper_list_l2624_https_arxiv_org_abs_2601_05138/figures/013_Figure_9.jpg]]
*Figure 9: Detailed architecture of VerseCrafter. Background RGB & depth maps and 3D Gaussian trajectory RGB & depth maps are first encoded by the frozen Wan Encoder. The soft merged mask is rearranged into latent-aligned channels, and all geometry latents are then concatenated along the channel dimension to form a unified spatio-temporal geometry feature. This feature is patchified into tokens and processed by the GeoAdapter branch. At selected Wan-DiT blocks, GeoAdapter outputs are passed through zero-initialized linear layers and added to the backbone tokens as residual modulations, enabling geometry-consistent control over camera motion and multi-object motion*

## 实验与关键发现

### 实验设置与评估基准

VerseCrafter基于冻结的**Wan2.1 T2V-14B**潜在视频扩散主干构建，仅训练轻量GeoAdapter分支。每个GeoAdapter块从对应Wan-DiT块的权重初始化以稳定训练，注入间隔k=5（每5个DiT块配对一个GeoAdapter块）。训练数据为自建的**VerseControl4D**数据集，包含35,000个训练样本和1,000个验证样本，其中26%来自Sekai-Real-HQ、74%来自SpatialVID-HQ。所有对比方法均在VerseControl4D的相同训练/验证划分上评估，使用统一的自动标注流程重新计算相机轨迹和3D高斯轨迹，以确保控制指标对齐。

评估采用两类指标：（1）**VBench-I2V**总体得分衡量生成视频的视觉质量；（2）三项3D控制指标——旋转误差（RotErr）、平移误差（TransErr）和对象运动控制误差（ObjMC），分别量化相机姿态精度和对象运动遵循度（详见公式11、12、15）。实验分为联合相机与对象运动控制、仅相机运动控制（静态场景）两个子任务。

### 联合相机与对象运动控制

在VerseControl4D联合控制任务上，VerseCrafter在所有指标上均显著优于基线方法（Table 1）。

![[assets/figures/papers/paper_list_l2624_https_arxiv_org_abs_2601_05138/figures/006_Table_1.jpg]]
*Table 1: Joint camera and object motion control on VerseControl4D. We report VBench-I2V scores and 3D control metrics (RotErr, TransErr, ObjMC). VerseCrafter achieves the best overall video quality and the most accurate joint control of camera and object motion*

| 方法 | VBench-I2V ↑ | RotErr ↓ | TransErr ↓ | ObjMC ↓ |
|------|-------------|----------|------------|---------|
| Perception-as-Control | 83.66 | 5.006 | 8.767 | 6.556 |
| Yume | 85.47 | 7.560 | 8.735 | 7.959 |
| Uni3C | 83.55 | 1.361 | 7.731 | 5.883 |
| **VerseCrafter** | **88.10** | **0.890** | **3.103** | **2.507** |

**Table 1: 联合相机与对象运动控制定量结果。** VerseCrafter在VBench-I2V总体得分上达到88.10，较最佳基线Yume（85.47）提升2.63分，较Perception-as-Control提升4.44分。在3D控制精度上，旋转误差0.890（Perception-as-Control为5.006，降低82.2%），平移误差3.103（降低64.6%），对象运动控制误差2.507（降低61.8%）。Uni3C虽在旋转误差上表现次优（1.361），但其依赖SMPL-X参数模型，局限于单人场景；Yume仅通过文本粗略描述运动，缺乏精确的相机控制。

定性对比（Figure 4）进一步揭示：Perception-as-Control和Uni3C出现明显的人体形变，Yume虽大致遵循文本描述的运动但相机控制不精确，而VerseCrafter更忠实地同时遵循相机轨迹和多对象运动，并保持清晰外观和几何一致的背景。

![[assets/figures/papers/paper_list_l2624_https_arxiv_org_abs_2601_05138/figures/004_Figure_4.jpg]]
*Figure 4: Qualitative comparison of joint camera and object motion control. Perception-as-Control and Uni3C exhibit noticeable human deformation, while Yume roughly follows the text-described motion but lacks precise camera control. Uni3C is also limited to single human. In contrast, VerseCrafter more faithfully follows both the camera trajectory and multi-object motion while maintaining sharp appearance and geometrically consistent backgrounds*

### 仅相机运动控制（静态场景）

在VerseControl4D的静态场景子集上，仅评估相机运动控制能力（Table 2）。

| 方法 | VBench-I2V ↑ | RotErr ↓ | TransErr ↓ |
|------|-------------|----------|------------|
| Voyager | 78.12 | 3.557 | 3.880 |
| ViewCrafter | 84.04 | 2.101 | 9.868 |
| FlashWorld | 85.33 | 1.792 | 3.257 |
| **VerseCrafter** | **86.80** | **0.650** | **2.587** |

**Table 2: 仅相机运动控制定量结果。** VerseCrafter总体得分86.80，旋转误差0.650（较FlashWorld的1.792降低63.7%），平移误差2.587（降低20.6%）。ViewCrafter和Voyager出现立面扭曲、结构漂移或相机运动不准确，FlashWorld倾向于产生模糊的场景边界，而VerseCrafter更好地遵循目标相机轨迹，同时保持清晰细节和全局一致的3D几何（Figure 5）。

### 消融实验

消融实验（Table 3）验证了三个核心设计选择。

![[assets/figures/papers/paper_list_l2624_https_arxiv_org_abs_2601_05138/figures/010_Table_3.jpg]]
*Table 3: Ablation study on 3D representation, depth, and decoupled controls. We compare different variants of VerseCrafter using VBench-I2V and 3D control metrics (RotErr, TransErr, ObjMC). Our full model with 3D Gaussian trajectories, depth-aware rendering, and decoupled background/foreground controls achieves the best visual quality and the most accurate camera and object motion control*

**Table 3: 消融实验定量结果。** 完整模型（3D高斯轨迹 + 深度感知渲染 + 解耦背景/前景控制）在所有指标上取得最优。

**（1）3D对象运动表示。** 将3D高斯轨迹替换为3D边界框或3D点轨迹均导致性能下降：3D边界框的ObjMC升至4.520（+80.3%），3D点轨迹的ObjMC升至6.896（+175.1%），且视觉质量下降。定性结果（Figure 6）显示，3D点轨迹和边界框常导致尺度漂移和运动不对齐，而3D高斯轨迹更好地遵循目标对象运动并保持合理形状。

**（2）深度感知控制。** 移除控制图中的深度信息（仅RGB）导致旋转误差从0.890升至1.177（+32.2%），ObjMC从2.507恶化至4.929（+96.6%）。定性结果（Figure 7）表明，无深度时模型产生错误的前后遮挡关系（如灯柱被拉到远景建筑前方），遮挡边界随时间漂移；引入RGB+depth后模型恢复一致的视差和遮挡关系。

**（3）解耦背景与前景控制。** 将背景和前景控制合并为单一控制图导致ObjMC从2.507升至3.726（+48.6%），出现明显的运动退化（Figure 8）。解耦设计（独立渲染背景地图和轨迹地图）对维持静态背景稳定和精确对象运动至关重要。

### 失败模式与边界案例分析

**（1）精细姿态与关节控制不足。** 当前对象表示仅通过单个3D高斯提供椭圆体级别的控制，无法实现精细的6D姿态或部件级关节控制。Figure 15a展示了对刚性各向异性物体的两个成功案例和一个人形物体的失败案例——人形对象的非刚性形变超出了单高斯椭球体的表达能力。

**（2）动态背景建模受限。** 背景点云主要依据第一帧重建，作为近似静态的几何支架。Figure 15b显示，对于中等程度的背景动态（如摇曳的树木），模型尚能处理；但对于大规模非刚性背景变形（如瀑布），模型失效。

**（3）物理合理性不足。** 生成过程中未施加显式物理约束，可能导致物理直觉上不合理的运动。

**（4）单目深度估计鲁棒性。** 单目深度估计误差可能引起点云噪声。Figure 16b分析表明，即使深度估计噪声较大、点云存在扭曲，生成视频仍保持视觉相似性和主要场景结构，说明模型具有一定鲁棒性，但在极端视角下仍可能出现几何扭曲。

### 推理效率分析

**Table 6: 推理内存-时间权衡。** 在50步扩散采样设置下，基础配置峰值显存90 GB。使用FSDP可降至70 GB（降低22.2%），FSDP+CPU offload进一步降至57 GB（降低36.7%），仅小幅增加推理时间。

**Table 7: 端到端推理延迟分解。** 在8×96GB GPU上生成81帧720P视频总耗时约1152秒。其中，4D几何场景状态可跨相同场景的重复编辑复用，模型加载为一次性启动成本，而4D控制图渲染和扩散采样在编辑控制变化时需重新运行。

### 补充图表

![[assets/figures/papers/paper_list_l2624_https_arxiv_org_abs_2601_05138/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative comparison of camera-only motion control on static scenes. ViewCrafter and Voyager exhibit distorted facades, drifting structures, or inaccurate camera motion, while FlashWorld tends to produce blurred scene boundaries and imprecise camera motion. In contrast, VerseCrafter better follows the target camera trajectory while preserving sharp details and globally consistent 3D geometry*

![[assets/figures/papers/paper_list_l2624_https_arxiv_org_abs_2601_05138/figures/008_Figure_6.jpg]]
*Figure 6: Ablation on 3D representations for object motion control. We compare object control using 3D point trajectory (top), 3D bounding box (middle), and 3D Gaussian trajectory (bottom). 3D point trajectory and 3D bounding box often cause scale drift and misaligned motion (red boxes), whereas 3D Gaussian trajectory better follows the intended object motion while preserving plausible shapes and background interactions*

![[assets/figures/papers/paper_list_l2624_https_arxiv_org_abs_2601_05138/figures/009_Figure_7.jpg]]
*Figure 7: Ablation on depth-aware control. We compare VerseCrafter without depth inputs (Ours (w/o depth), top) and with RGB+depth inputs (middle) under the same camera trajectory. Without depth, the model often produces incorrect foregroundbackground ordering, e.g., lampposts are pulled in front of distant buildings, and occlusion boundaries drift over time (red boxes). With RGB+depth, the model recovers consistent parallax and occlusion, producing geometry much closer to the ground truth*

![[assets/figures/papers/paper_list_l2624_https_arxiv_org_abs_2601_05138/figures/011_Figure_8.jpg]]
*Figure 8: Ablation on decoupled background and foreground controls. We compare a variant that merges background and foreground controls into a single map (Ours (BG & FG Merged), top) with our default decoupled design (middle). When the controls are merged, object motion control degrades significantly (red boxes), whereas the decoupled design better preserves the static background and produces more accurate and stable object motion*

![[assets/figures/papers/paper_list_l2624_https_arxiv_org_abs_2601_05138/figures/003_Figure_3.jpg]]
*Figure 3: Construction pipeline of VerseControl4D. Starting from Sekai-Real-HQ and SpatialVID-HQ, we extract 81-frame clips and apply quality filtering. For each retained clip, Qwen2.5- VL-72B, Grounded-SAM2, and MegaSAM provide captions, object masks, depth, and camera trajectory, which are lifted into background/object point clouds, from which 3D Gaussian trajectories are fitted, and then rendered into background/trajectory maps and a soft merged mask that constitute our 4D control maps*

## 定位与知识库关联

### 1. 问题定位：视频世界模型的4D几何控制缺口

VerseCrafter 瞄准的是**视频世界模型（Video World Model）中联合相机运动与多对象运动精确控制**这一尚未闭合的缺口。现有方法在控制粒度与几何一致性上存在结构性局限：

- **2D控制范式**：**Perception-as-Control** 等基线依赖2D边界框、掩码或光流作为控制信号，这类信号本质上是视点依赖且非刚性的——当相机运动时，2D控制信号本身就会发生透视变形，难以在共享世界坐标系下同时精确约束相机与对象运动。
- **3D参数化模型**：**Uni3C** 依赖SMPL-X等类别受限的参数化人体模型，只能处理单一人体的关节运动，无法泛化到任意类别对象。
- **文本驱动生成**：**Yume** 通过文本描述粗略引导对象运动，缺乏对相机轨迹和对象空间位置的精确几何控制。

VerseCrafter 的核心判断是：**缺乏统一的4D几何表示**是上述方法无法实现联合精确控制的根本瓶颈。因此，该方法引入了一个可编辑的4D几何场景状态，将动态场景解耦为静态背景点云与每对象3D高斯轨迹，在共享世界坐标系下统一表达场景几何与运动。

### 2. 方法谱系中的位置

#### 2.1 与视频扩散控制方法的对比

| 维度 | 2D控制方法（Perception-as-Control等） | 3D参数化方法（Uni3C） | **VerseCrafter** |
|------|--------------------------------------|----------------------|------------------|
| 控制信号形式 | 2D边界框/掩码/光流 | SMPL-X参数模型 | 多通道4D控制图（背景RGB/深度+高斯轨迹RGB/深度+软合并掩码） |
| 对象表示 | 2D区域 | 类别受限的3D参数模型 | 类别无关的3D高斯轨迹（均值+全协方差） |
| 相机-对象解耦 | 弱（2D信号视点耦合） | 部分解耦 | 完全解耦（共享世界坐标系） |
| 适用对象类别 | 任意（但控制粗糙） | 仅人体 | 任意类别 |
| 几何一致性 | 低（缺乏3D约束） | 中（受限于参数模型） | 高（显式4D几何状态） |

VerseCrafter 在方法谱系中处于**从"2D/参数化控制"向"通用4D几何控制"跃迁**的位置。其关键创新在于将3D高斯表示从静态场景重建（如3D Gaussian Splatting）拓展为**动态对象运动的控制原语**，并通过渲染将其桥接到冻结的视频扩散模型。

#### 2.2 与仅相机控制方法的对比

在仅相机控制的静态场景子任务上，VerseCrafter 与 **ViewCrafter**、**Voyager**、**FlashWorld** 等基线形成直接对比。这些方法虽然能实现一定程度的相机运动控制，但普遍存在以下问题：

- **ViewCrafter** 和 **Voyager**：在定性结果中表现出立面扭曲和结构漂移，说明其缺乏对场景3D几何的显式建模。
- **FlashWorld**：倾向于产生模糊的场景边界和不精确的相机运动，反映其控制信号可能过于稀疏或缺乏几何约束。

VerseCrafter 通过静态背景点云提供显式的场景几何支架，在相机运动时通过重投影保持背景的几何一致性，因此在旋转误差（0.650 vs FlashWorld的1.792）和平移误差（2.587 vs FlashWorld的3.257）上均取得显著优势。

### 3. 适用边界与关键设计约束

#### 3.1 对象表示的粒度上限

当前的对象表示采用**单个3D高斯**（均值+全协方差）描述整个对象，这提供了椭圆体级别的空间范围与朝向控制，但存在明确的上限：

- **无法实现部件级关节控制**：对于人体等铰接对象，单个高斯无法表达肢体间的相对运动。论文在Figure 15(c)中展示了两个铰接/非刚体对象的成功案例，但同时承认这是"粗粒度的对象级控制"，并非精细的6D姿态控制。
- **刚性假设的局限**：3D高斯轨迹通过协方差矩阵的演化隐式编码了对象的缩放与旋转，但本质上假设对象保持近似刚体运动。对于高度非刚体变形（如旗帜飘动），该表示可能失效。

#### 3.2 背景建模的静态假设

背景点云主要依据第一帧的单目深度估计重建，并假设在整个视频序列中保持静态。这一设计约束带来两个后果：

- **中等背景动态可容忍**：论文在Figure 15(b)中展示了两个中等背景动态（如树叶轻微晃动）的成功案例，说明模型对小幅背景运动具有一定鲁棒性。
- **大规模非刚性背景变形失败**：同一图中的失败案例显示，当背景包含高度非刚性运动（如瀑布）时，静态点云假设被打破，生成质量下降。这是该方法的一个明确适用边界。

#### 3.3 单目深度估计的噪声传播

VerseCrafter 依赖 MoGe-2 进行单目深度估计，深度误差会通过反投影传播到背景点云和对象高斯拟合中。论文在Figure 16(b)中展示了模型对深度噪声的鲁棒性——即使点云存在明显扭曲，生成的视频仍能保持视觉相似性和主要场景结构。然而，在极端视角或深度歧义区域（如镜面反射表面），几何扭曲的风险仍然存在。

#### 3.4 物理合理性的缺失

生成过程中未施加显式物理约束（如碰撞检测、动力学方程），这意味着：

- 对象运动轨迹在几何上遵循控制信号，但可能违反物理直觉（如物体穿模、不合理的加速度）。
- 论文将此列为明确局限，并指出引入物理先验是未来方向。

### 4. 知识库贡献

#### 4.1 4D几何控制表示

VerseCrafter 向视频生成领域引入了**4D Geometric Control**这一概念：将动态场景抽象为可编辑的4D几何状态（静态背景点云 + 每对象3D高斯轨迹），在共享世界坐标系下统一表达相机与多对象运动。这一表示的关键特性包括：

- **类别无关**：不依赖任何对象类别先验，适用于任意前景对象。
- **可编辑**：用户可通过修改相机轨迹或高斯轨迹参数来编辑场景运动。
- **可渲染**：通过3D渲染生成多通道4D控制图，桥接到2D扩散模型。

#### 4.2 GeoAdapter条件注入机制

轻量GeoAdapter的设计提供了一种**将4D几何特征注入冻结视频扩散模型**的通用范式：

- 采用DiT风格的网络分支处理几何特征。
- 通过零初始化投影矩阵实现从零开始的残差调制（$x_{n+1} = \mathcal{B}_n(x_n) + \mathcal{G}_m(\mathbf{g}) \mathbf{W}_0^{(m)}$），避免破坏预训练先验。
- 每5个Wan-DiT块插入一个GeoAdapter块（k=5），在控制精度与计算开销间取得平衡。

#### 4.3 VerseControl4D数据集

论文构建了VerseControl4D数据集（35,000训练样本 + 1,000验证样本），提供统一的4D几何标注（深度、相机轨迹、对象掩码、3D高斯轨迹），为视频世界模型的几何控制研究提供了标准化基准。数据来源为Sekai-Real-HQ（26%）和SpatialVID-HQ（74%），涵盖动态场景（联合相机与对象运动）和静态场景（仅相机运动）两类。

### 5. 开放问题与未来方向

基于论文明确列出的局限和未解决问题，以下方向值得后续工作关注：

1. **精细对象表示**：如何引入多部分组成的高斯或骨架驱动的变形场，实现铰接对象的部件级关节控制？这需要突破当前"单高斯/对象"的表示瓶颈。

2. **动态背景建模**：如何将静态背景点云扩展为逐帧可变形几何，以处理大规模非刚性背景运动（如水体、烟雾），同时保持全局几何一致性？

3. **物理先验融合**：如何将碰撞检测、刚体动力学等物理约束融入生成过程？可能的路径包括在训练目标中添加物理一致性损失，或在推理时引入物理模拟器作为后处理。

4. **推理效率优化**：当前生成81帧720P视频需约1152秒且占用高达90 GB显存。论文在Table 6中展示了FSDP+CPU offload可将峰值显存降至57 GB（降低36.7%），但延迟优化空间仍然巨大。如何进一步降低推理成本以支持实时交互？

5. **多视角几何扩展**：论文在Figure 16(a)中展示了多视角输入可改善几何覆盖和新视角保真度。如何自动利用多视角信息扩展背景点云，以支持更大幅度的相机运动？

6. **控制精度与生成质量的权衡**：消融实验（Table 3）显示，更强的几何约束（如深度信息、解耦控制）在提升控制精度的同时，可能对视觉质量产生轻微影响。如何在这一trade-off中找到更优的平衡点？

## 原文 PDF

![[paperPDFs/CVPR_2026/VerseCrafter_Dynamic_Realistic_Video_World_Model_with_4D_Geometric_Control.pdf]]
