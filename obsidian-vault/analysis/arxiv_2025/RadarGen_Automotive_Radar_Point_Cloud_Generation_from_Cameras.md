---
title: "RadarGen: Automotive Radar Point Cloud Generation from Cameras"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/RadarGen_Automotive_Radar_Point_Cloud_Generation_from_Cameras.pdf
aliases:
- RadarGen
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将雷达数据表示为 BEV 图像，并利用预训练的视觉基础模型提取深度、语义和运动条件作为与控制输入对齐的扩散模型条件，直接调节生成雷达点的空间分布、RCS 和多普勒。
primary_logic: 通过将稀疏雷达点云编码为多通道 BEV 图像，借助预训练图像扩散模型的强大先验与高效架构，并融合视觉基础模型提供的几何与语义 BEV 条件，能够以概率方式生成与视觉场景一致且具有正确物理属性（RCS、多普勒）的雷达点云，实现可扩展的多模态生成式仿真。
claims:
- RadarGen 在几何保真度（CD Loc. 1.68 vs 1.84，IoU@1m 0.31 vs 0.23）和雷达属性保真度（DA F1 0.24 vs 0.14）上显著优于前馈基线。
- 去除 BEV 条件中的语义分割图导致 RCS 分布差异（MMD RCS）从 0.09 上升至 0.12，验证语义线索对雷达属性生成的关键作用。
- 在生成雷达点云上训练的检测器 NDS 为 0.30（真实数据 0.48），而基线生成的点云几乎无法检测（NDS ≈ 0），证明生成数据可被下游感知模型有效利用。
- 基于反卷积（IRL1 LASSO）的稀疏点云恢复方法在覆盖度和密度上均优于随机采样和峰值选择。
---

# RadarGen: Automotive Radar Point Cloud Generation from Cameras

> [!tip] 核心洞察
> 通过将稀疏雷达点云编码为多通道 BEV 图像，借助预训练图像扩散模型的强大先验与高效架构，并融合视觉基础模型提供的几何与语义 BEV 条件，能够以概率方式生成与视觉场景一致且具有正确物理属性（RCS、多普勒）的雷达点云，实现可扩展的多模态生成式仿真。

| 字段 | 内容 |
|------|------|
| 中文题名 | RadarGen：基于摄像头生成汽车雷达点云 |
| 英文题名 | RadarGen: Automotive Radar Point Cloud Generation from Cameras |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2512.17897) · [Project](https://radargen.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RadarGen |
| Dataset | MAN TruckScenes |

> [!tip] 效果简介
> - MAN TruckScenes 上，Entire Area: CD Loc. (↓) / IoU@1m (↑) / DA F1 (↑) 1.68±0.39 / 0.31±0.11 / 0.24±0.12 vs 1.84±0.48 / 0.23±0.10 / 0.14±0.09 (-0.16 / +0.08 / +0.10)；Entire Area: MMD Loc. / MMD RCS / MMD Doppler (↓) 0.056±0.062 / 0.09±0.15 / 0.31±0.74 vs 0.368±0.151 / 0.36±0.25 / 0.65±0.64 (-0.312 / -0.27 / -0.34)。
> - MAN TruckScenes (Foreground) 上，Foreground: CD Loc. (↓) / Hit Rate (↑) 0.95±0.65 / 0.66 vs 1.32±0.79 / 0.37 (-0.37 / +0.29)。
> - MAN TruckScenes (Detection) 上，Detection: mAP / NDS 0.11 / 0.30 vs 0.00 / 0.00 (Baseline 生成数据) (+0.11 / +0.30)。

## 概述

自动驾驶感知系统对高质量雷达数据的需求日益增长，但真实雷达点云的采集成本高昂且覆盖场景有限。直接从视觉生成雷达点云面临三重挑战：雷达点云固有的稀疏性与非均匀采样使其难以用传统密集预测建模；雷达反射截面（RCS）与多普勒速度等传感器特有属性的高度随机性；以及缺乏原始射频（RF）数据来约束生成过程。

RadarGen 提出了一条概率生成路径：将稀疏雷达点云编码为三通道鸟瞰（BEV）图像——点密度图、RCS 图与多普勒图，在潜空间内用条件扩散模型学习其联合分布。模型以预训练视觉基础模型（深度估计、语义分割、光流）提取的 BEV 条件图为引导，使生成结果与视觉场景几何及语义保持一致。生成后，通过 L1 正则化非负反卷积从模糊密度图中恢复稀疏点位置，实现从视觉到雷达的端到端可控合成。

在 MAN TruckScenes 数据集上，RadarGen 在几何保真度（CD Loc. 1.68 vs 基线 1.84，IoU@1m 0.31 vs 0.23）和雷达属性保真度（DA F1 0.24 vs 0.14）上均显著优于前馈基线。消融实验证实，BEV 语义条件对 RCS 分布建模至关重要（移除后 MMD RCS 从 0.09 升至 0.12），而外观与运动条件则主要影响多普勒速度的生成质量。更为关键的是，在 RadarGen 生成的点云上训练的目标检测器达到了 NDS 0.30（真实数据为 0.48），而基线生成的点云几乎无法用于检测（NDS ≈ 0），验证了生成数据的下游可用性。

RadarGen 的核心贡献在于：将雷达生成问题转化为 BEV 图像域的潜扩散建模，借助预训练图像扩散模型的强大先验与视觉基础模型的几何语义理解，以概率方式生成与场景一致且具有正确物理属性的雷达点云，为可扩展的多模态生成式仿真提供了新范式。

## 背景与动机

### 问题背景：雷达点云的独特挑战

自动驾驶感知系统长期依赖摄像头与激光雷达的互补，而毫米波雷达作为第三种关键传感器，具备穿透雨雾、直接测量径向速度等独特优势。然而，雷达数据本身存在一系列固有特性，使得从视觉信号生成逼真雷达点云成为一个极具挑战性的问题。

雷达点云是稀疏、无序的三维点集，其采样高度非均匀。与激光雷达不同——后者的回波沿角度维度均匀分布，可被重塑为密集的距离图像——雷达检测源于非线性的 CFAR（恒虚警率）峰值检测过程，导致点的空间分布极不规则。每个雷达点还携带超越三维坐标的传感器特有属性：**雷达散射截面（RCS）** 反映目标的反射率，受材质、几何形状和入射角共同影响；**多普勒速度** 则记录目标相对于传感器的径向速度。这些物理属性蕴含丰富的场景语义，但同时也要求生成模型必须同时捕捉空间结构与物理特性的联合分布。

更为根本的难点在于雷达信号的高度随机性。多径反射、干涉效应以及原始 RF 数据的不可获取性，使得确定性前馈模型难以建模雷达测量的真实分布。这一瓶颈构成了本工作的核心动机：**需要一种能够以概率方式生成雷达点云、同时保持与视觉场景几何和语义一致性的方法**。

### 现有方法缺口

当前从视觉生成雷达点云的研究尚处早期阶段。最具代表性的基线方法是 **RGB2Point**，它采用确定性前馈网络，将多视角图像特征通过 Transformer 映射至点云空间，使用 Chamfer 距离损失直接回归固定数量的三维点坐标。这一范式存在三个根本性局限：

1. **表示失配**：直接输出点坐标忽略了雷达点云的非均匀采样特性，强制模型学习一个本质上确定性的映射，而雷达生成天然需要概率建模。
2. **属性缺失**：仅生成空间位置，未对 RCS 和多普勒速度等雷达特有属性进行建模，生成的“点云”仅具几何形态而无物理语义。
3. **条件贫乏**：仅依赖图像特征作为输入，缺乏对场景深度、语义布局和运动信息的显式利用，导致生成结果在几何精度和物理一致性上均与真实雷达存在显著差距。

这些缺口指向一个明确的研究问题：**如何设计一种生成范式，既能建模雷达点云的概率分布，又能充分利用视觉基础模型提取的丰富场景先验？**

### 本文动机与核心思路

RadarGen 的核心动机源于一个关键洞察：**将稀疏雷达点云编码为多通道鸟瞰（BEV）图像，可以桥接雷达域与图像生成域**。BEV 表示天然适合编码雷达数据的空间结构，而图像扩散模型在高质量生成方面已展现出强大能力。通过将雷达点云转化为密度图、RCS 图和多普勒图三通道 BEV 图像，RadarGen 得以复用高效潜扩散架构的强大先验，同时融合预训练视觉基础模型提供的深度、语义和运动条件，以概率方式生成与视觉场景一致且具有正确物理属性的雷达点云。

这一设计实现了三个层面的突破：在**表示层面**，BEV 图像化编码保留了雷达数据的空间结构与属性信息；在**生成层面**，潜扩散模型捕捉雷达测量的随机性，支持多样本生成；在**条件层面**，深度估计、语义分割和光流网络提供的 BEV 条件图直接调节生成雷达点的空间分布、RCS 和多普勒，实现了从视觉到雷达的可控合成。

## 核心创新

RadarGen 的核心创新在于将**稀疏、非均匀采样的雷达点云生成问题**重新表述为**条件 BEV 图像扩散 + 反卷积恢复**的两阶段范式，从而在表示、生成模型和条件注入三个关键维度实现了对前馈基线（RGB2Point）的系统性突破。

### 创新一：雷达数据的 BEV 图像化表示

传统点云生成模型（如 RGB2Point）直接输出固定数量的三维坐标和属性，难以捕捉雷达点云固有的稀疏性与随机性。RadarGen 将雷达点云编码为三通道 BEV 图像：**点密度图**（Point Density Map）、**RCS 图**和**多普勒图**（Sec. 4.1, Fig. 3）。其中点密度图通过高斯核卷积获得——$M_{p} = K_{\sigma} * \mathcal{P}_{xy}$——将离散的雷达反射点转化为平滑的空间分布信号。这一表示转换的深层动机是：雷达点云的高度随机性使得逐点回归极易陷入均值化预测，而密度图作为概率化中间表示，天然适配扩散模型的分布学习目标，同时保留了 RCS 和多普勒等雷达特有物理属性。

### 创新二：潜空间扩散模型的生成范式切换

基线 RGB2Point 采用确定性前馈网络，以 Chamfer 损失直接回归点坐标，本质上是学习“平均点云”，无法刻画雷达测量的随机性。RadarGen 切换到基于 **SANA DiT 的条件潜扩散模型**（Sec. 4.2），在潜空间对三个雷达图进行联合去噪生成。扩散模型的多步采样机制天然支持一对多映射——同一视觉场景可生成多组符合真实统计分布的雷达点云（Fig. 9），这是确定性前馈模型无法实现的能力。同时，三个雷达图通过共享自注意力与模态特定可学习嵌入联合处理，使密度、RCS 和多普勒在生成过程中相互约束，提升了属性一致性。

### 创新三：视觉基础模型驱动的 BEV 条件注入

基线仅将多视图图像特征通过 Transformer 映射至点云空间，缺乏显式的几何与语义先验。RadarGen 利用三个预训练视觉基础模型提取结构化 BEV 条件（Sec. 4.2, Fig. 2）：**UnidepthV2** 提供深度先验构建 Appearance Map，**Mask2Former** 提供语义分割构建 Semantic Map，**UniFlow** 结合深度信息近似 3D 速度（$v(x) \approx \frac{p^{t+\Delta t}(x) - p^{t}(x)}{\Delta t}$）构建 Radial Velocity Map。这些条件图与雷达 BEV 图在空间上对齐后作为扩散模型的输入通道，直接调节生成雷达点的空间分布、反射强度和径向速度。消融实验证实，移除语义图导致 RCS 分布差异（MMD RCS）从 0.09 恶化至 0.12（Table 2），验证了语义线索对雷达反射特性生成的关键作用。

### 创新四：反卷积驱动的稀疏点云恢复

扩散模型输出的是模糊的密度图，需从中恢复稀疏点位置。RadarGen 采用 L1 正则化非负反卷积（IRL1 LASSO）求解：

$$\operatorname*{min}_{\mathcal{P}_{xy} \geq 0} \frac{1}{2} \| K_{\sigma} * \mathcal{P}_{xy} - M_{p}' \|_{2}^{2} + \lambda \| \mathcal{P}_{xy} \|_{1}$$

该公式在数据保真度与稀疏性之间取得平衡，利用已知的高斯模糊核 $K_{\sigma}$ 进行反演，从生成密度图 $M_{p}'$ 中恢复稀疏点图 $\mathcal{P}_{xy}'$，再从对应位置的 RCS/多普勒图上采样属性值。相比随机采样和峰值选择，反卷积方法在空间覆盖度和点云密度上均显著更优（Fig. 10），且输出点数自适应而非固定，更贴近真实雷达的采样特性。

### 方法优势的结构性来源

上述四个创新形成了因果链条：BEV 图像化表示使雷达数据与成熟图像扩散架构兼容 → 扩散模型提供概率生成能力 → 基础模型条件注入提供几何与语义对齐 → 反卷积恢复保证稀疏性。这一链条的端到端效果在 Table 1 中得到验证：RadarGen 在几何保真度（CD Loc. 1.68 vs 1.84）、空间覆盖（IoU@1m 0.31 vs 0.23）和雷达属性保真度（DA F1 0.24 vs 0.14）上全面超越基线，且 BEV 条件模型相比直接多视图条件在几何指标（CD Loc. 0.95 vs 1.00）和训练效率（2 天 vs 9 天）上均有优势（Table 2）。

## 整体框架

RadarGen 的整体 pipeline 围绕一个核心设计展开：**将稀疏、非均匀的雷达点云转换为多通道 BEV 图像，借助预训练图像扩散模型的强大先验进行生成，再通过反卷积恢复稀疏点云**。这一设计直接回应了雷达数据的两大瓶颈——固有的稀疏性与随机性，以及 RCS/多普勒等传感器特异性属性的建模需求。

### Pipeline 总览

RadarGen 由四个紧密衔接的模块构成，形成“雷达→图像→潜空间生成→点云”的闭环：

1. **BEV Map Generation（雷达图像化）**：将输入的雷达点云转换为三通道 BEV 图像——点密度图（Point Density Map）、RCS 图和多普勒图，作为扩散模型的生成目标。
2. **BEV Scene Conditioning Extraction（视觉条件提取）**：利用预训练基础模型从多视角图像中提取深度、语义和运动信息，投影至 BEV 空间，形成与雷达图空间对齐的条件信号。
3. **Latent Diffusion Denoiser（潜扩散去噪器）**：基于 SANA DiT 架构的潜空间条件扩散模型，以 BEV 条件图为引导，联合生成三个雷达图的潜变量。
4. **Sparse Point Cloud Recovery（稀疏点云恢复）**：通过 L1 正则化非负反卷积从生成的模糊密度图中恢复稀疏点位置，再从对应的 RCS/多普勒图采样属性值，输出最终雷达点云。

Figure 2 展示了完整的数据流：多视角图像经基础模型提取条件 → BEV 编码 → 潜扩散生成 → 反卷积恢复 → 雷达点云输出。

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/002_Figure_2.jpg]]
*Figure 2: Overview of RadarGen. (Left) Multi-view posed images at time t and*

### 模块间关系与数据流

各模块之间的依赖关系体现了 RadarGen 的核心洞察——**通过 BEV 表示实现视觉条件与雷达生成目标的空间对齐，使扩散模型能够以概率方式建模雷达测量的随机性**。

**输入流**：系统接收两类输入——(1) 时刻 $t$ 和 $t+\Delta t$ 的多视角相机图像，用于提取视觉条件；(2) 目标雷达点云（仅训练时），用于监督 BEV 图的生成。

**条件提取与对齐**：视觉基础模型（UnidepthV2、Mask2Former、UniFlow）分别提取深度、语义分割和光流，投影至 BEV 后构建三类条件图——Appearance Map（外观）、Semantic Map（语义）和 Radial Velocity Map（径向速度）。这些条件图与雷达 BEV 图在空间上严格对齐，作为扩散模型的 conditioning 输入。Figure 2 中部展示了这一对齐过程。

**潜空间生成**：雷达点云首先经 BEV Map Generation 转换为三张单通道 BEV 图像（Figure 3 详细展示了这一转换过程：点云栅格化 → 高斯核卷积 → 三通道复制以适配 AE 的 RGB 输入空间）。每张图被独立编码为潜变量 $z_p$、$z_r$、$z_d$，作为扩散模型的监督目标。在去噪过程中，三个潜变量被拼接为统一 token 序列，通过共享自注意力机制处理，同时注入模态特定的可学习嵌入以区分密度、RCS 和多普勒三种模态。

**输出恢复**：扩散模型生成的是模糊的点密度图 $M_p'$，而非直接的点坐标。这是因为扩散模型擅长生成平滑的连续分布，而雷达点云本质上是稀疏的。因此，Sparse Point Cloud Recovery 模块通过求解 L1 正则化非负反卷积问题：

$$\operatorname*{min}_{\mathcal{P}_{xy} \geq 0} \frac{1}{2} \| K_{\sigma} * \mathcal{P}_{xy} - M_{p}' \|_{2}^{2} + \lambda \| \mathcal{P}_{xy} \|_{1}$$

从模糊密度图中恢复稀疏点位置 $\mathcal{P}_{xy}'$。随后，从生成的 RCS 图和多普勒图中采样对应位置的属性值，形成完整的雷达点云 $(x, y, z, \text{RCS}, \text{Doppler})$。

### 设计决策的关键影响

消融实验（Table 2）验证了各模块设计的必要性：BEV 条件模型相比直接多视图条件模型，在几何指标（CD Loc. 0.95 vs 1.00）和训练效率（2 天 vs 9 天）上均有显著优势，证实了 BEV 对齐对扩散模型训练的关键作用。移除语义分割条件导致 RCS 分布差异（MMD RCS）从 0.09 升至 0.12，验证了语义线索对雷达反射特性生成的必要性。点云恢复中的反卷积方法在空间覆盖和点密度上均优于随机采样和峰值选择（Figure 10），证实了基于已知模糊核的正则化反演优势。

> **需要手动验证**：论文未明确说明潜扩散模型的具体去噪步数、DiT 的层数/头数配置，以及 AE 的具体架构来源。这些细节对复现工作至关重要，建议查阅论文附录或代码仓库（https://radargen.github.io/）确认。

### 补充图表

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/001_Figure_1.jpg]]
*Figure 1: Controllable radar synthesis from vision. (Top) Given multi-view camera images, RadarGen generates realistic radar point clouds that align with real-world radar statistics and can be consumed by downstream perception models. (Bottom) The generation is semantically consistent: modifying the input scene with an off-the-shelf image editing tool (e.g., replacing a distant car with a closer truck) updates the radar response, removing returns from newly occluded regions and reflecting the new object geometry*

## 核心模块与公式推导

RadarGen 的核心设计围绕一个关键矛盾展开：雷达点云本质上是稀疏、非均匀采样的点集，而现代扩散模型擅长生成结构化的密集图像。为解决这一矛盾，RadarGen 将整个生成流程分解为四个紧密协作的模块。

### 雷达 BEV 图像化

雷达点云首先被投影到鸟瞰图（BEV）平面，形成三个单通道图像：

- **点密度图（Point Density Map）**：将雷达点的 BEV 坐标投影为稀疏二值图 $\mathcal{P}_{xy}$，再与高斯核 $K_\sigma$ 卷积，得到平滑的密度估计：

$$M_p = K_\sigma * \mathcal{P}_{xy}$$

- **RCS 图（RCS Map）**：对每个 BEV 网格单元内的雷达点，取雷达截面（Radar Cross Section）的最大值，编码目标的反射强度。

- **多普勒图（Doppler Map）**：对每个网格单元取径向多普勒速度的最大绝对值，编码场景中的运动信息。

为适配预训练图像自编码器的 RGB 输入空间，每个单通道 BEV 图被复制为三通道后，独立编码为潜变量 $z_p$、$z_r$、$z_d$，作为扩散模型的监督目标。这一表示转换是 RadarGen 能够利用成熟图像扩散架构的关键前提。

### BEV 场景条件提取

该模块从多视角摄像头图像中提取几何、语义和运动先验，投影至 BEV 空间形成三类条件图：

- **外观条件（Appearance Map）**：利用深度估计基础模型（UnidepthV2）生成 BEV 深度图，提供场景的几何结构线索。

- **语义条件（Semantic Map）**：利用语义分割基础模型（Mask2Former）生成 BEV 语义分割图，编码物体类别和空间布局。

- **径向速度条件（Radial Velocity Map）**：利用光流基础模型（UniFlow）从 $t$ 和 $t+\Delta t$ 两帧图像估计像素位移，结合深度信息近似 3D 速度：

$$v(x) \approx \frac{p^{t+\Delta t}(x) - p^{t}(x)}{\Delta t}$$

再将 3D 速度投影为径向分量，形成与多普勒图对齐的运动条件。这三类条件图被拼接后注入扩散模型，作为控制生成的核心信号。

### 潜空间扩散去噪器

去噪器基于 SANA DiT 架构，在潜空间对三个雷达图进行联合生成。每个去噪步骤中，$z_p$、$z_r$、$z_d$ 的潜变量被拼接为统一 token 序列，通过共享自注意力层处理，同时引入模态特定的可学习嵌入 $m_i$ 以区分不同雷达图。条件 BEV 图被编码后作为条件 token 注入，使去噪过程受几何、语义和运动信号的共同约束。

### 稀疏点云恢复

扩散生成的点密度图 $M_p'$ 是经过高斯模糊的平滑图像，需要恢复为稀疏点坐标。RadarGen 将其建模为 L1 正则化非负反卷积问题：

$$\operatorname*{min}_{\mathcal{P}_{xy} \geq 0} \frac{1}{2} \| K_{\sigma} * \mathcal{P}_{xy} - M_p' \|_{2}^{2} + \lambda \| \mathcal{P}_{xy} \|_{1}$$

其中第一项为数据保真度（要求卷积结果逼近生成的密度图），第二项为 L1 稀疏正则项（鼓励点云稀疏性），非负约束 $\mathcal{P}_{xy} \geq 0$ 保证物理合理性。该 LASSO 问题通过迭代重加权 L1（IRL1）结合 FISTA 算法求解。恢复出稀疏点位置后，从生成的 RCS 图和多普勒图中回采对应位置的属性值，最终输出完整的雷达点云。

消融实验（Table 2）证实，反卷积恢复方法在空间覆盖和点云密度上均优于随机采样和峰值选择，验证了基于已知模糊核的正则化反演在稀疏点云重建中的优势。

### 补充图表

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/003_Figure_3.jpg]]
*Figure 3: Overview of representing radar as images (Sec. 4.1). Constructing radar maps from a radar point cloud requires first rasterizing each point to BEV. The point locations are then convolved with a Gaussian kernel*

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/014_Figure_11.jpg]]
*Figure 11: BEV conditioning maps. Visualization of the BEV appearance, semantic, and relative radial velocity maps produced from inputs at times t and t+∆t. The appearance map retains the camera image colors. Semantic classes are color-coded as: Road, Sidewalk, Building, Vegetation, Car, and Person. For the velocity map, lighter colors indicate positive velocity while darker colors indicate negative velocity*

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/013_Figure_10.jpg]]
*Figure 10: Recovery methods. Comparison of Random, Peak, and Deconvolution sparse point cloud recovery methods. Random sampling exhibits inconsistent density characterized by clustering and empty regions. Peak recovery fills the space uniformly but suffers from low density. Our Deconvolution method achieves coverage while maintaining density where necessary. RadarGen uses inputs t and t + ∆t. Ground truth bounding boxes are highlighted in color*

## 实验与分析

### 核心实验结果

RadarGen 在 MAN TruckScenes 数据集上进行了全面评估，与基线方法 **RGB2Point**（前馈式图像到点云模型）相比，在几何保真度、雷达属性保真度和分布相似性三个维度均展现出显著优势。

**Table 1** 的全区域评估显示：RadarGen 的几何定位 Chamfer 距离（CD Loc.）为 1.68±0.39，优于基线的 1.84±0.48；1 米范围内的交并比（IoU@1m）从 0.23 提升至 0.31。在雷达属性保真度上，多普勒属性 F1 分数（DA F1）从 0.14 提升至 0.24，提升幅度达 71%。分布相似性指标上，RadarGen 在定位分布（MMD Loc. 0.056 vs 0.368）、RCS 分布（MMD RCS 0.09 vs 0.36）和多普勒分布（MMD Doppler 0.31 vs 0.65）上均大幅降低，表明生成数据的整体统计特性更接近真实雷达。

前景区域评估进一步验证了 RadarGen 对关键目标的建模能力：前景 CD Loc. 为 0.95（基线 1.32），Hit Rate 达 0.66（基线仅 0.37），说明 RadarGen 生成的点云在目标存在性和空间位置上与真实数据高度一致。

### 消融研究

**Table 2** 的消融实验系统性地验证了各 BEV 条件通道的贡献：

- **移除语义分割图（W/o Semantic map）** 导致 RCS 分布差异（MMD RCS）从 0.09 上升至 0.12，证实语义线索对雷达反射特性的生成至关重要——不同材质和几何形状的物体具有不同的雷达反射截面，语义信息为模型提供了关键的物理先验。
- **移除外观图（W/o Appearance map）** 和 **移除速度图（W/o Velocity map）** 主要影响多普勒分布（MMD Doppler 分别升至 0.35 和 0.34），说明细粒度外观特征和运动信息是速度生成的核心条件。
- **多视图直接条件（MV Camera Cond.）** 与 BEV 条件模型的对比揭示了表示选择的重要性：MV 条件模型在几何指标上略逊（CD Loc. 1.00 vs 0.95），且训练时间从 2 天延长至 9 天。这表明将多视图特征投影到与雷达图对齐的 BEV 空间，不仅提升了生成质量，还大幅降低了扩散模型的学习难度。

### 下游感知验证

**Table 3** 的检测兼容性实验是 RadarGen 实用价值的关键证明：在 RadarGen 生成的点云上训练的检测器达到 NDS 0.30、mAP 0.11，而基线生成数据训练的检测器几乎无法检测（NDS ≈ 0, mAP ≈ 0）。与真实数据训练的检测器（NDS 0.48）相比仍存在差距，但这 0.30 的 NDS 已证明生成数据可被下游感知模型有效利用，为仿真数据驱动的感知模型训练提供了可行路径。

### 点云恢复策略分析

**Figure 10** 对比了三种从模糊密度图恢复稀疏点云的方法：随机采样（Random）、峰值选择（Peak）和基于 L1 正则化的反卷积（Deconvolution/IRL1 LASSO）。反卷积方法在空间覆盖度和点云密度上均优于前两者，证实了利用已知高斯模糊核进行正则化反演的显著优势。该方法通过求解优化问题：

$$\operatorname*{min}_{\mathcal{P}_{xy} \geq 0} \frac{1}{2} \| K_{\sigma} * \mathcal{P}_{xy} - M_{p}' \|_{2}^{2} + \lambda \| \mathcal{P}_{xy} \|_{1}$$

在数据保真度和稀疏性之间取得平衡，有效恢复了雷达点云固有的稀疏分布特性。

### 公平性说明

在解读上述结果时需注意以下公平性因素：基线 RGB2Point 仅使用当前时刻 t 的图像，而 RadarGen 额外使用 t+Δt 的光流信息，可能赋予本方法更多运动线索；基线输出固定 1024 个点，RadarGen 输出数量自适应，两者在密度相似度等指标上的比较基础不同；RadarGen 的 BEV 条件依赖外部预训练基础模型（UnidepthV2、Mask2Former、UniFlow）的精度，基线不依赖这些模型，性能差异可能部分源于基础模型的质量。

### 失败模式与局限性

**Figure 12** 揭示了 RadarGen 在低光夜间场景下的典型失败模式：底层基础模型难以准确识别车辆并估计速度，导致生成的雷达点云出现不合理的空间分布和属性值。模型未在低光/夜间数据上训练，在这些视觉条件下可能产生不符合物理规律的雷达模式。此外，在未观测或被遮挡区域，模型可能产生“幻觉”雷达点，尽管图像编辑实验（Figure 5）显示模型能部分处理遮挡关系。

### 补充图表

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/004_Table_1.jpg]]
*Table 1: Quantitavie evaluation. RadarGen broadly outperforms the baseline on geometric fidelity (CD, IoU, Density Similarity, Hit Rate), radar attribute fidelity (DA Recall, Precision, F1), and distribution similarity (MMD)*

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/007_Table_2.jpg]]
*Table 2: Ablation Study. We demonstrate the importance of each RadarGen condition and compare against a model conditioned directly on multi-view (MV) camera images. Evaluation covers geometric fidelity (CD, IoU, Density Similarity, Hit Rate), radar attribute fidelity (DA Recall, Precision, F1), and distribution similarity (MMD)*

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/009_Table_3.jpg]]
*Table 3: Detection metrics comparison. Evaluation of a trained detector on GT versus generated samples from RadarGen and Baseline*

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results. Our model generates point clouds with higher geometric and attribute fidelity to the ground truth compared to the baseline. RadarGen uses inputs t and t + ∆t, while the baseline uses only t. Ground truth bounding boxes are highlighted in color*

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/015_Figure_12.jpg]]
*Figure 12: Qualitative analysis of limitations. Visual comparison of RadarGen against the ground truth radar in a low-light night scene. In this setting, the underlying foundation models struggle to accurately recognize vehicles and estimate velocities. RadarGen was not trained on such scenarios. Ground truth bounding boxes are highlighted in color*

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/006_Figure_5.jpg]]
*Figure 5: Scene editing. Modifying the input images using an offthe-shelf image editing tool updates the radar response, demonstrating object removal (left) and insertion (right)*

![[assets/figures/papers/paper_list_l72_https_arxiv_org_abs_2512_17897/figures/012_Figure_9.jpg]]
*Figure 9: Additional seeds. Our model can generate multiple sets of point clouds for a single scene by replacing the diffusion process seed. RadarGen uses inputs t and t + ∆t. Ground truth bounding boxes are highlighted in color*

## 方法谱系与知识库定位

### 与基线方法的关系

RadarGen 与现有工作的核心差异在于**雷达数据的表示形式**和**生成模型的范式选择**。基线方法 **RGB2Point** 采用确定性前馈网络，直接从多视图图像回归固定数量（1024 个）的三维点坐标与属性，训练目标为 Chamfer 距离损失。这种直接回归策略面临两个根本性困难：（1）雷达点云的稀疏性和非均匀采样使得固定基数输出难以匹配真实分布；（2）雷达信号固有的高度随机性（受多径反射、干涉、材料反射特性等影响）无法被确定性映射捕捉。

RadarGen 通过三个关键设计突破了上述瓶颈：

- **BEV 图像表示替代直接点集回归**：将稀疏雷达点云编码为三通道 BEV 图像——点密度图（Point Density Map，由 $M_{p} = K_{\sigma} * \mathcal{P}_{xy}$ 生成）、RCS 图和 Doppler 图。这一表示将非结构化的点云转化为结构化的图像域，使得成熟的图像生成架构可直接复用。
- **条件扩散模型替代确定性前馈**：基于 SANA DiT 的潜空间扩散模型，以概率方式建模雷达 BEV 图的联合分布，天然适配雷达测量的随机性。扩散过程在潜空间对三个雷达图进行联合去噪，通过共享自注意力和模态特定的可学习嵌入（learnable embeddings）保持跨通道一致性。
- **反卷积稀疏恢复替代直接坐标输出**：生成阶段不直接输出点坐标，而是先生成模糊的密度图，再通过 L1 正则化非负反卷积（IRL1 LASSO）恢复稀疏点位置：
  $$\operatorname*{min}_{\mathcal{P}_{xy} \geq 0} \frac{1}{2} \| K_{\sigma} * \mathcal{P}_{xy} - M_{p}' \|_{2}^{2} + \lambda \| \mathcal{P}_{xy} \|_{1}$$
  这一策略将“生成多少点、点在哪里”的联合决策解耦为密度估计与稀疏反演两步，显著提升了空间覆盖度和点云密度（见 Figure 10）。

### 视觉条件注入策略的演进

RadarGen 的 BEV 条件提取管线代表了从“端到端隐式学习”到“显式物理先验注入”的范式转变。基线 RGB2Point 仅将多视图图像特征通过 Transformer 映射至点云空间，缺乏对三维几何和语义的显式建模。RadarGen 则利用预训练视觉基础模型构建三类 BEV 条件图：

- **Appearance Map**：由深度估计网络（UnidepthV2）提供的深度先验投影至 BEV，编码场景几何结构；
- **Semantic Map**：由语义分割网络（Mask2Former）提供的语义标签投影至 BEV，编码物体类别与材料线索；
- **Radial Velocity Map**：由光流网络（UniFlow）结合深度信息近似三维速度 $v(x) \approx \frac{p^{t+\Delta t}(x) - p^{t}(x)}{\Delta t}$，编码运动先验。

消融实验（Table 2）揭示了各条件的作用机制：移除 Semantic Map 导致 MMD RCS 从 0.09 上升至 0.12，验证语义信息对雷达反射特性（RCS 与材质、几何形状相关）生成的关键作用；移除 Appearance Map 或 Velocity Map 主要影响 Doppler MMD（分别升至 0.35 和 0.34），说明细粒度几何和运动信息对速度生成的必要性。此外，BEV 条件模型相比直接多视图条件（MV Camera Cond.）在几何指标（CD Loc. 0.95 vs 1.00）和训练效率（2 天 vs 9 天）上均有显著优势，证明 BEV 空间的对齐简化了跨模态映射的学习难度。

### 在知识库中的定位

RadarGen 处于**视觉驱动的雷达仿真**这一新兴交叉领域，其方法论贡献可沿以下维度定位：

- **相对于 LiDAR 仿真方法**：现有视觉到 LiDAR 的生成方法（如基于深度估计的投影或点云生成网络）可利用 LiDAR 的均匀角采样特性构造密集深度图，而雷达点云的非均匀采样和 RCS/Doppler 属性使得这些方法无法直接迁移。RadarGen 的 BEV 密度图表示和反卷积恢复策略为这一差异提供了系统性解决方案。
- **相对于雷达感知中的生成方法**：现有工作多聚焦于雷达数据增强（如对现有雷达点云进行 dropout、扰动或插值），而非从视觉模态生成全新雷达数据。RadarGen 首次实现了仅从摄像头输入生成具有物理一致性的完整雷达点云。
- **相对于扩散模型在多模态生成中的应用**：RadarGen 将图像潜扩散模型（SANA DiT）适配到雷达域，通过 BEV 图像桥接和条件注入机制，展示了预训练图像扩散先验向非标准传感器模态迁移的可行路径。

### 适用边界与局限

**依赖外部基础模型的精度**。RadarGen 的 BEV 条件提取完全依赖 UnidepthV2、Mask2Former 和 UniFlow 三个预训练网络的输出质量。在低光、强烈反射或摄像头遮挡等挑战性场景下，深度估计、语义分割和光流估计均可能失效，导致生成的雷达点云出现几何错位或属性偏差。Figure 12 展示了低光夜间场景下的退化案例，模型在此类未训练条件下可能产生不合理的雷达模式。这一局限的本质是：RadarGen 的上限受限于其条件提取器在目标场景中的泛化能力，而当前训练数据（MAN TruckScenes）未充分覆盖极端光照和天气条件。

**生成数据与真实数据的感知差距**。尽管在生成雷达点云上训练的检测器达到了 NDS 0.30（真实数据为 0.48），显著优于基线生成数据的近乎零检测性能（Table 3），但这一差距表明生成数据仍缺少真实雷达中某些被下游感知模型利用的精细统计特性。可能原因包括：扩散模型的平滑效应导致点云边缘模糊；反卷积恢复的稀疏模式与真实雷达的 CFAR 检测统计特性存在偏差；RCS 和 Doppler 的联合分布未完全匹配真实物理过程。

**未观测区域的幻觉问题**。扩散模型的生成式本质可能导致雷达点出现在被遮挡或不可见的区域。尽管图像编辑实验（Figure 5）显示模型能响应场景修改（如移除车辆后对应雷达回波消失），但在复杂遮挡或视野边界处仍可能出现不一致。

**时序与模态扩展的局限性**。当前框架仅支持固定双帧（$t$ 和 $t+\Delta t$）输入，未扩展到视频流或文本/语义引导的可控生成。雷达生成的质量受限于时序窗口的长度和光流估计的精度。

### 开放问题

1. **低光和恶劣天气条件下的鲁棒生成**：能否通过域适应、数据增强或联合微调基础模型来提升条件输入在挑战性场景下的质量？是否需要引入雷达自监督信号来校正视觉条件的失效？

2. **检测性能差距的系统诊断**：生成雷达与真实雷达之间 NDS 差距（0.30 vs 0.48）的具体来源是什么？是点云几何精度、属性分布偏差、还是稀疏模式的统计特性差异？是否可以通过对抗训练或感知损失（perceptual loss）来弥补？

3. **视频级时序扩展**：如何将双帧条件扩展为视频流输入，利用时序一致性约束提升生成质量？时序扩散模型（video diffusion）在该场景下的适用性和计算成本如何？

4. **反卷积恢复的理论边界**：IRL1 LASSO 方法假设已知高斯模糊核 $K_{\sigma}$，在更复杂的噪声模型或非高斯模糊下是否仍然有效？是否可以学习自适应模糊核以匹配不同雷达传感器的点扩散函数？

5. **文本/语义可控生成**：当前框架仅支持图像条件，能否引入文本描述或语义布局作为额外控制信号，实现“在指定区域生成特定反射特性的雷达回波”等细粒度可控生成？

## 原文 PDF

![[paperPDFs/arxiv_2025/RadarGen_Automotive_Radar_Point_Cloud_Generation_from_Cameras.pdf]]
