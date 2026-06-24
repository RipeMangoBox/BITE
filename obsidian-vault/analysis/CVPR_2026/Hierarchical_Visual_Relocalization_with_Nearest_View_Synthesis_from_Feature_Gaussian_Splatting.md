---
title: Hierarchical Visual Relocalization with Nearest View Synthesis from Feature Gaussian Splatting
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Hierarchical_Visual_Relocalization_with_Nearest_View_Synthesis_from_Feature_Gaussian_Splatting.pdf
project_link: "https://hqitao.github.io/SplatHLoc"
code_link: null
aliases:
- HVRNVSFFGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用特征高斯溅射（FGS）渲染虚拟视图实现自适应视角检索，并采用渲染特征粗匹配与半稠密匹配器细匹配的混合策略，扩充视角覆盖并增强匹配准确性。
primary_logic: 渲染特征具有跨视图一致性，适合patch级粗匹配，但因其与查询特征的域差异难以建模精细几何关系；而从图像提取的半稠密特征在像素级细匹配中精度更高，二者结合可显著提升重定位鲁棒性和效率。
claims:
- "自适应视角检索在弱纹理区域显著提升初始位姿估计鲁棒性（Table 5：启用自适应检索后，R@[5cm,5°] 从77.1%升至91.9%）。"
- 混合匹配策略整体优于纯渲染特征匹配（STDLoc）和纯图像特征匹配（SP+LG）（Table 5, Table 6）。
- 在7-Scenes、12-Scenes、Cambridge Landmarks三个基准上，SplatHLoc在多数场景下取得最优或接近最优的中位平移/旋转误差及召回率。
- 7-Scenes 上 Avg. median translation (cm) / rotation (°) = 0.55 / 0.17
---

# Hierarchical Visual Relocalization with Nearest View Synthesis from Feature Gaussian Splatting

> [!tip] 核心洞察
> 渲染特征具有跨视图一致性，适合patch级粗匹配，但因其与查询特征的域差异难以建模精细几何关系；而从图像提取的半稠密特征在像素级细匹配中精度更高，二者结合可显著提升重定位鲁棒性和效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于特征高斯溅射的近邻视图合成的层次化视觉重定位 |
| 英文题名 | Hierarchical Visual Relocalization with Nearest View Synthesis from Feature Gaussian Splatting |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.29185) · [Project](https://hqitao.github.io/SplatHLoc) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SplatHLoc |
| Dataset | 7-Scenes, 12-Scenes, Cambridge Landmarks |

> [!tip] 效果简介
> - 7-Scenes 上，Avg. median translation (cm) / rotation (°) 0.55 / 0.17 vs 0.76 / 0.24 (STDLoc); 0.61 / 0.20 (RAP_ref) (-0.21 cm / -0.07° vs STDLoc)。
> - 12-Scenes 上，Avg. median translation (cm) / rotation (°) & R@[2cm,2°] 0.3 / 0.14 & ≈97% (scene-dependent, up to 100%) vs 0.7 / 0.26 & 97.2% (ACE) (Lower translation/rotation errors; R@[2cm,2°] slightly below ACE+GS-CPR (1.4% l...)。
> - Cambridge Landmarks 上，Median translation (cm) / rotation (°) per scene Competitive with STDLoc (e.g., College 10/0.39 vs STDLoc 10/0.43, Church 5/0.11... vs STDLoc (Comparable, with slight improvements on some scenes)。

## 概述

### 问题与瓶颈

视觉重定位是计算机视觉与机器人领域的核心任务，其目标是根据查询图像估计精确的 6‑DoF 相机位姿。经典的层次化重定位方法（如 **HLoc**，Sarlin et al., CVPR 2019）遵循“图像检索‑特征匹配‑位姿估计”的级联流程，但受限于数据库图像视角稀疏与特征匹配质量不足，尤其在弱纹理区域，初始位姿估计的鲁棒性显著下降。这构成了本文的核心瓶颈：**稀疏视角覆盖导致检索到的参考图像与查询图像之间共视区域有限，进而使后续特征匹配和位姿估计缺乏足够的内点支撑**。

### 核心方法定位

针对上述瓶颈，本文提出 **SplatHLoc**——一种基于**特征高斯溅射（Feature Gaussian Splatting, FGS）** 的层次化视觉重定位框架。其核心思路是将场景表示为可渲染颜色、深度及特征图的 FGS 地图，并围绕该表示设计两个关键机制：

1. **自适应粗‑细视角检索**：当粗检索的几何验证内点不足时，在检索位姿附近随机扰动并渲染虚拟视图，再执行二次检索，从而扩充视角覆盖。
2. **混合特征匹配**：粗匹配阶段利用渲染特征图的内积与互最近邻建立 patch 级粗对应；细匹配阶段采用半稠密匹配器（JamMa）对渲染 RGB 图像与查询图像进行像素级精化。

这种“渲染特征粗匹配 + 图像特征细匹配”的混合策略，充分利用了渲染特征的跨视图一致性进行高效粗定位，同时借助从真实图像提取的半稠密特征实现高精度几何对齐，在鲁棒性与效率之间取得了平衡。

### 主要结果

在三个公开基准数据集上，SplatHLoc 取得了领先或接近领先的性能：

- **7-Scenes（室内）**：平均中位平移误差 0.55 cm、旋转误差 0.17°，优于 STDLoc（0.76 cm / 0.24°）和 RAP_ref（0.61 cm / 0.20°）。
- **12-Scenes（室内）**：平均中位误差约 0.3 cm / 0.14°，R@[2cm, 2°] 召回率接近 100%（多数场景），略低于 ACE+GS-CPR 但优于 Marepo+GS-CPR。
- **Cambridge Landmarks（室外）**：与 STDLoc 性能相当，部分场景略有提升。

消融实验进一步验证了两个关键设计的作用：自适应视角检索将弱纹理场景（如 Stairs）的 R@[5cm, 5°] 召回率从 77.1% 提升至 91.9%；混合匹配器在所有指标上均优于纯渲染特征匹配（FGS-Matcher）和纯稀疏匹配（SP+LG）。

## 背景与动机

视觉重定位（Visual Relocalization）是三维视觉与机器人领域的基础任务，其目标是根据查询图像精确估计相机在已知场景中的 6-DoF 位姿。该任务在增强现实、自动驾驶和机器人导航等应用中扮演关键角色。近年来，层次化重定位（Hierarchical Localization）范式因其效率与精度平衡而成为主流路线：先在数据库图像中检索与查询视角最接近的参考图像，再通过特征匹配建立 2D-2D 或 2D-3D 对应关系，最终利用 PnP 求解位姿。

然而，**传统层次化重定位方法存在一个核心瓶颈**：数据库图像的视角覆盖天然稀疏且离散，当查询图像与所有数据库图像之间存在显著的视角差异时，检索到的参考图像与查询之间的共视区域有限，导致特征匹配阶段的内点数量不足，进而使初始位姿估计精度急剧下降。这一问题在弱纹理区域（如白墙、楼梯）尤为严重——稀疏的纹理信息本身已使特征提取与匹配困难，视角偏差进一步压缩了有效匹配的空间。

现有方法尝试从两个方向缓解上述问题。**基于结构的方法**（如 **HLoc**，Sarlin et al., CVPR 2019）依赖 SfM 稀疏点云和图像检索，但受限于数据库图像的离散视角覆盖，无法主动生成缺失的观察角度。**基于渲染的方法**（如 **STDLoc** 和 **LoGS**）利用神经渲染或高斯溅射（3D Gaussian Splatting）从任意视角合成视图，为视角扩充提供了可能；但这类方法通常渲染 RGB 图像后再提取特征进行匹配，渲染-查询之间的域差异（domain gap）在像素级精细匹配中引入噪声，限制了位姿估计的上限精度。

更深层的问题在于**特征匹配策略与渲染表示之间的不匹配**。渲染特征（rendered features）具有跨视图一致性，适合在粗粒度上建立 patch 级对应；但由于渲染质量在训练稀疏区域下降，以及渲染特征与真实图像特征之间的域差异，它们难以精确建模像素级的几何关系。相反，从真实图像提取的半稠密特征在细粒度匹配中精度更高，但缺乏视角泛化能力。如何将二者的优势有机融合，是提升重定位鲁棒性与精度的关键。

本文的动机由此明确：**构建一种新的层次化重定位框架，利用可渲染的特征高斯溅射（Feature Gaussian Splatting, FGS）场景表示，实现自适应视角检索与混合特征匹配的协同设计**。具体而言，本文提出三个核心思路：

1. **以 FGS 为统一场景表示**：同时渲染颜色、深度和可解码的特征图，为视角合成与特征匹配提供共享基础。
2. **自适应粗-细视角检索**：当粗检索几何验证失败时，在检索位姿邻域渲染虚拟视图并执行二次检索，主动扩充视角覆盖。
3. **混合粗-细特征匹配**：粗匹配利用渲染特征的内积相似度建立 patch 级对应，细匹配切换至半稠密匹配器对渲染 RGB 与查询图像进行像素级精化，规避渲染特征的域差异在细粒度上的局限。

通过上述设计，SplatHLoc 旨在同时提升弱纹理区域的初始位姿鲁棒性，以及整体重定位的精度与效率。

## 核心创新

SplatHLoc 针对传统层次化视觉重定位中**数据库视角稀疏**与**弱纹理区域特征匹配不可靠**两大瓶颈，提出了三个相互协同的 changed slots，形成从场景表示到匹配策略的系统性创新。

### 1. 场景表示：从稀疏点云到特征高斯溅射（FGS）地图

传统层次化重定位方法（如 **HLoc** (Sarlin et al., CVPR 2019)）依赖稀疏 SfM 点云作为场景表示，仅能检索离散的数据库图像，无法覆盖查询视角与数据库视角之间的连续视点空间。基于渲染的基线 **STDLoc** 虽引入高斯溅射，但仅渲染 RGB 图像，后续仍需提取特征进行匹配，割裂了场景几何与特征表示。

SplatHLoc 提出以**特征高斯溅射（Feature Gaussian Splatting, FGS）** 统一场景表示。每个高斯原语同时编码辐射场与特征场，可渲染颜色图、深度图及低维可解码的特征图 $F_r^{\mathrm{low}}$。通过引入轻量卷积解码器 $d$ 对低维渲染特征上采样至高维，得到与查询特征维度对齐的 $F_r^{\mathrm{high}}$（Equation 2），训练时以光度损失与特征损失的加权组合联合优化（Equation 3）。这一设计使得**渲染、检索、匹配三阶段共享同一表征**，为后续自适应视角合成与渲染特征匹配奠定基础。

### 2. 视角检索：从被动检索到自适应粗-细虚拟视图合成

HLoc 等传统方法直接检索数据库图像，当查询视角与数据库视角偏差较大或场景纹理稀疏时，检索到的参考图像与查询之间的共视区域有限，导致几何验证内点数不足，初始位姿估计失败。

SplatHLoc 提出**自适应粗-细视角检索（Adaptive Coarse-to-Fine Viewpoint Retrieval）** 策略（Algorithm 1）。其核心机制为：
- **粗检索**：采用 MixVPR 全局描述子检索 top-$k_1$ 候选图像，随后以 SuperPoint + LightGlue 进行几何验证；
- **自适应触发**：若几何验证内点数低于阈值，则判定粗检索位姿与查询视角偏离较大；
- **细检索**：在粗检索位姿附近随机扰动（范围 $a^\circ$ 角度、$b$ 米平移），渲染 $k_2$ 张虚拟视图，再次执行检索与几何验证，从中选取内点数最多的候选。

这一策略将检索空间从离散的数据库图像**扩展至连续的位姿邻域**，在弱纹理场景（如楼梯）中效果尤为显著——消融实验（Table 5）表明，启用自适应检索后，R@[5cm,5°] 从 77.1% 跃升至 91.9%，提升幅度达 14.8 个百分点。

### 3. 特征匹配：从单一特征源到渲染-图像混合粗-细匹配

STDLoc 等渲染基线在渲染 RGB 图像后提取特征进行匹配，本质上将渲染仅作为数据增强手段，未充分利用 FGS 渲染特征的独特性质。SplatHLoc 识别出渲染特征与查询图像特征之间存在**域差异**——渲染特征具有跨视图一致性，适合 patch 级粗匹配；但因其合成特性，难以建模像素级精细几何关系。

据此提出**混合特征匹配器 $\mathcal{M}_{\mathrm{hybrid}}$**（Equation 11），分两阶段运作：
- **粗匹配阶段**：直接使用渲染特征图 $F_r^{\mathrm{high}}$ 与查询特征 $F_t$ 计算内积相似度矩阵 $S_c$（Equation 6），经双向 Softmax 与互最近邻筛选（Equation 7-8）建立粗对应。渲染特征的跨视图一致性在此阶段提供稳定、稠密的粗匹配。
- **细匹配阶段**：对渲染 RGB 图像与查询图像分别提取半稠密特征，采用预训练匹配器 **JamMa** 在粗对应窗口内进行像素级精化（Equation 10）。半稠密特征来自真实/渲染 RGB 图像，能更准确地建模精细几何关系。

消融实验（Table 6）有力验证了分工的合理性：纯渲染特征匹配（FGS-Matcher）在室内场景的 R@[2cm,2°] 仅 76.8%，而混合匹配器（M + I_fine）达到 91.5%；反之，若粗匹配也使用图像特征（I_coarse + I_fine），室内召回率反而下降，表明渲染特征在粗匹配阶段的不可替代性。

三个 changed slots 形成闭环：FGS 地图提供统一的渲染能力，自适应检索利用渲染合成虚拟视角以扩充检索覆盖，混合匹配器则充分发挥渲染特征与图像特征在粗、细阶段各自的优势。三者协同使得 SplatHLoc 在 7-Scenes、12-Scenes、Cambridge Landmarks 三个基准上均取得最优或接近最优的中位平移/旋转误差（Table 1-3）。

## 整体框架

SplatHLoc 的整体管线遵循**层次化视觉重定位**范式，以**特征高斯溅射（Feature Gaussian Splatting, FGS）** 作为统一的场景表示核心，将建图、检索、匹配与位姿估计串联为一个端到端可优化的流程（Figure 2）。其设计动机源于传统层次化重定位方法的两大瓶颈：（1）数据库图像视角稀疏导致初始检索位姿与查询图像间缺乏足够的共视区域；（2）弱纹理或重复纹理区域中，纯图像特征或纯渲染特征的匹配均难以同时兼顾鲁棒性与精度。SplatHLoc 通过三个关键模块的协同设计——FGS 地图构建、自适应粗‑细视点检索、混合特征匹配——系统性地缓解了上述问题。

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the proposed SplatHLoc framework. Starting from a database of reference images, we build an SfM model to initialize the Gaussian primitives, and then training the FGS map, see Section 3.1. SplatHLoc follows a hierarchical relocalization pipeline. (a) In the retrieval stage, we propose an adaptive coarse-to-fine viewpoint retrieval strategy. We first perform the coarse retrieval to obtain retrieved images and then use a lightweight feature matcher to perform geometric verification for each query–retrieved image pair. If geometric verification yields fewer inliers than a threshold, we perform the fine viewpoint retrieval to get a fine retrieved pose, see Section 3.2. (b) In the...*

### 管线总览

整个框架的输入为场景的参考图像数据库，输出为查询图像的 6‑DoF 相机位姿。管线可分为**离线建图**与**在线定位**两个阶段：

1. **离线建图**：从参考图像出发，利用运动恢复结构（SfM）构建稀疏点云以初始化高斯原语，随后联合优化辐射场与特征场，得到可渲染颜色、深度及低维可解码特征图的 FGS 地图（Section 3.1）。
2. **在线定位**：对每帧查询图像，依次执行（a）自适应粗‑细视点检索，获取与查询视角高度对齐的参考图像或渲染视图（Section 3.2）；（b）混合特征匹配，建立查询图像与参考图像/渲染视图之间的鲁棒 2D‑2D 对应关系（Section 3.3）；（c）利用渲染深度图将 2D‑2D 匹配提升为 2D‑3D 对应，通过 RANSAC+PnP 估计初始位姿，并从估计位姿重新渲染、迭代精化（Section 3.4）。

Figure 2 直观展示了上述流程：从参考图像数据库出发，经 SfM 初始化和 FGS 训练得到场景地图后，查询图像首先经过全局检索与几何验证获取粗检索位姿；若几何验证内点数不足，则在粗检索位姿邻域内扰动生成虚拟视图并执行精细检索；随后，混合匹配器利用渲染特征图完成 patch 级粗匹配，再由半稠密匹配器在粗对应窗口内精化至像素级匹配；最终通过 2D‑3D 提升与迭代位姿优化输出精确定位结果。

### 模块间关系与数据流

各模块之间的数据依赖关系清晰且解耦，便于独立分析与消融验证：

- **FGS 地图构建**为下游所有模块提供基础能力：渲染的颜色图 $I_r$ 和深度图 $D_r$ 用于视点检索中的几何验证、细匹配阶段的半稠密特征提取以及 2D‑3D 提升；渲染的低维特征图 $F_r^{\mathrm{low}}$ 经解码器 $d$ 上采样后得到高维特征图 $F_r^{\mathrm{high}}$，专用于粗匹配阶段的相似度计算。
- **自适应粗‑细视点检索**的输出是经过几何验证的参考图像或渲染虚拟视图，作为混合特征匹配的输入。该模块不依赖匹配模块的具体实现，仅通过轻量级特征匹配器（SuperPoint + LightGlue）进行几何验证，保证了检索阶段的效率。
- **混合特征匹配**接收查询图像 $I_q$ 与检索阶段输出的参考图像/渲染视图 $I_r$，分别提取查询特征 $F_t$ 和渲染特征 $F_r^{\mathrm{high}}$ 用于粗匹配，再对 $I_q$ 和 $I_r$ 提取半稠密特征用于细匹配。粗匹配为细匹配提供空间先验窗口，细匹配在窗口内精化对应点，二者形成互补。
- **位姿估计与迭代优化**将细匹配的 2D 对应点经渲染深度图提升为 2D‑3D 对应，输入 RANSAC+PnP 求解初始位姿；随后从该位姿重新渲染颜色与深度图，再次执行混合匹配与位姿估计，形成迭代精化闭环。

### 关键设计决策

SplatHLoc 在模块设计上做出了若干关键取舍，直接决定了系统的性能边界：

- **渲染特征用于粗匹配而非细匹配**：渲染特征 $F_r^{\mathrm{high}}$ 具备跨视图一致性，适合通过内积相似度快速建立 patch 级粗对应；但其与真实图像特征之间存在域差异，难以精确建模像素级几何关系。因此，细匹配阶段转而使用从渲染 RGB 图像和查询图像中提取的半稠密特征（JamMa），在粗对应窗口内完成高精度对齐。消融实验（Table 6）证实，这一混合策略在所有指标上均优于纯渲染特征匹配（FGS‑Matcher）和纯图像特征匹配（SP+LG）。
- **自适应视点检索而非固定检索**：当粗检索返回的参考图像与查询图像共视区域不足时，传统方法直接导致初始位姿估计失败。SplatHLoc 在粗检索位姿邻域内随机扰动并渲染虚拟视图，再对这些虚拟视图执行二次检索与几何验证，显著增加了弱纹理区域的有效匹配内点数（Figure IV）。该设计在 Stairs 场景上将 R@[5cm,5°] 从 77.1% 提升至 91.9%（Table 5）。
- **迭代位姿精化而非单次估计**：初始位姿估计后，从估计位姿重新渲染视图并与查询图像再次匹配，可进一步缩小视角差异、提升匹配质量。实验表明，经过 4 轮迭代精化后，7‑Scenes 上的平均中位平移/旋转误差从初始的 2.36 cm / 0.64° 降至 0.55 cm / 0.17°（Table 1）。

### 已知局限

尽管 SplatHLoc 在多个基准上取得了领先性能，其管线仍存在若干结构性局限：FGS 地图在训练视角稀疏的区域渲染质量下降，可能导致定位失败（Figure VI）；场景中的高度重复纹理（如走廊、楼梯）易引发错误匹配；FGS 训练依赖 COLMAP 提供的 SfM 初始点云，当 SfM 重建失败时建图受阻；此外，地图存储仍需额外保存 VPR 特征（例如 Chess 场景需 62.5 MB），限制了在资源受限设备上的部署。这些局限为后续研究指明了方向，如探索基于 3D 基础模型的初始化替代方案、场景分块扩展策略以及更紧凑的特征表示。

### 补充图表

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/001_Figure_1.jpg]]
*Figure 1: SplatHLoc: a novel hierarchical visual relocalization framework based on Feature Gaussian Splatting (FGS). FGS renders color, depth, and feature maps from novel views, which our method exploits to improve the image retrieval and feature matching process. Upon retrieving a reference image, we match it to the query to estimate an initial pose (initial relocalization). We then render views from the estimated pose and iteratively match them to the query to refine the pose (refined relocalization)*

## 核心模块与公式推导

### 3.1 特征高斯溅射（FGS）地图构建

SplatHLoc 以**特征高斯溅射（Feature Gaussian Splatting, FGS）** 作为场景表示，在 3DGS 的基础上引入一个额外的特征场。每个高斯原语除颜色和几何属性外，还携带一个低维特征向量，使得地图能够同时渲染颜色、深度和特征图。

**训练流程**：首先使用 COLMAP 对参考图像数据库进行运动恢复结构（SfM），得到稀疏点云和相机位姿，以此初始化高斯原语的位置。随后联合优化辐射场和特征场，训练目标为加权组合的光度损失与特征损失：

$$ \mathcal{L} = \mathcal{L}_{\mathrm{rgb}} + \gamma \mathcal{L}_{\mathrm{feat}} \tag{3} $$

**特征编码与解码**：对于每张训练图像 $I$，使用预训练编码器 $e$ 提取密集特征并调整尺寸：

$$ F_{t} = \mathrm{Resize}(e(I)), \quad F_{t} \in \mathbb{R}^{C \times H' \times W'} \tag{1} $$

渲染时，FGS 先输出低维特征图 $F_{r}^{\mathrm{low}}$，再通过可学习的卷积解码器 $d$ 上采样至高维，以匹配目标特征维度：

$$ F_{r}^{\mathrm{high}} = \mathsf{Resize}(d(F_{r}^{\mathrm{low}})), \quad F_{r}^{\mathrm{high}} \in \mathbb{R}^{C \times H' \times W'} \tag{2} $$

这种“低维存储、解码上采样”的设计（见 Figure 3）有效降低了地图存储开销和渲染计算量。

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of the FGS training process. Feature decoder d is introduced to reduce the dimensionality of the rendered feature*

---

### 3.2 自适应粗‑细视点检索

传统层次化重定位直接检索数据库图像，在弱纹理区域常因视角覆盖不足导致几何验证内点数过低。SplatHLoc 提出**自适应粗‑细视点检索**（Adaptive C2F Viewpoint Retrieval），利用 FGS 的视图合成能力动态扩充候选视角。

**流程**（见 Algorithm 1）：

1. **粗检索**：使用 MixVPR 全局描述子从参考图像库中检索 top-$k_1$ 候选图像。
2. **几何验证**：对每个候选图像与查询图像，使用 SuperPoint + LightGlue 进行特征匹配和几何验证，统计内点数。
3. **自适应判断**：若最大内点数低于阈值，说明粗检索候选与查询视角差异过大，触发**细检索**：
   - 选取粗检索最优候选的相机位姿 $p_c^c$，在其邻域内随机扰动（扰动范围 $a^\circ$ 角度、$b$ 米平移），生成 $k_2$ 个虚拟视点；
   - 利用 FGS 从这些虚拟视点渲染颜色图，再次执行全局检索和几何验证，得到视角更接近查询的细检索位姿。

该策略的核心价值在于：当数据库图像无法提供与查询足够共视的参考帧时，FGS 渲染的虚拟视图填补了视角空白，显著提升了初始位姿估计的鲁棒性（消融实验证实，在弱纹理的 Stairs 场景上 R@[5cm,5°] 从 77.1% 提升至 91.9%）。

---

### 3.3 混合粗‑细特征匹配

SplatHLoc 的匹配模块采用**混合粗‑细匹配器** $\mathcal{M}_{\mathrm{hybrid}}$，将渲染特征的跨视图一致性与半稠密匹配器的像素级精度相结合。

**粗匹配阶段**（使用渲染特征图）：

首先计算查询特征 $F_t$ 与渲染特征 $F_{r}^{\mathrm{high}}$ 的内积相似度矩阵，并除以温度系数 $\tau$：

$$ S_{c} = \frac{1}{\tau} \cdot \langle F_{t}, F_{r}^{\mathrm{high}} \rangle \tag{6} $$

对 $S_c$ 分别按行和列计算 Softmax，得到双向匹配概率：

$$ P_{q \to r} = \mathrm{Softmax}_{\mathrm{row}}(S_{c}), \quad P_{r \to q} = \mathrm{Softmax}_{\mathrm{col}}(S_{c}) \tag{7} $$

通过**互最近邻**（Mutual Nearest Neighbor）和置信度阈值 $\theta$ 筛选可靠粗对应点：

$$ \mathcal{C}_{q,r}^{c} = \{ (i,j) \mid P_{i,j}^{qr} = \max_{k} P_{i,k}^{qr}, P_{i,j}^{qr} \geq \theta \} \cap \{ (i,j) \mid P_{i,j}^{rq} = \max_{k} P_{k,j}^{rq}, P_{i,j}^{rq} \geq \theta \} \tag{8} $$

**细匹配阶段**（使用半稠密匹配器）：

在粗对应点 $\mathcal{C}_{q,r}^{c}$ 确定的局部窗口内，使用半稠密匹配器 **JamMa** 对渲染 RGB 图像与查询图像提取的半稠密特征进行像素级精化匹配。细匹配概率由裁剪窗口内的双向 Softmax 相乘得到：

$$ P_{f} = \operatorname{Softmax}_{\mathrm{row}}(S_{f}) \cdot \operatorname{Softmax}_{\mathrm{col}}(S_{f}) \tag{10} $$

最终，混合匹配器输出精化的 2D‑2D 对应点集：

$$ \mathcal{C}_{q,r}^{f} = \mathcal{M}_{\mathrm{hybrid}}(F_{t}, F_{r}^{\mathrm{high}}, I_{q}, I_{r}) \tag{11} $$

**设计动机**：渲染特征在 patch 级别具有跨视图一致性，适合粗匹配阶段的区域对应；但其与真实图像特征存在域差异，难以建模像素级精细几何关系。因此细匹配阶段转而使用从 RGB 图像提取的半稠密特征，精度更高。消融实验（Table 6）证实，粗阶段用渲染特征、细阶段用图像特征的组合（M + I_fine）在所有指标上均优于纯渲染特征匹配（FGS-Matcher）和纯稀疏匹配（SP+LG）。

---

### 3.4 2D‑2D 到 2D‑3D 提升与位姿估计

利用 FGS 渲染的深度图 $D_r$ 和已知相机内参 $K$，将细匹配得到的 2D 像素坐标 $\mathbf{x}_r$ 提升为 3D 点 $\mathbf{X}_r$：

$$ \mathbf{X}_{r} = T \cdot \left( D_{r}(\mathbf{x}_{r}) \cdot K^{-1} [\mathbf{x}_{r}] \right) \tag{12} $$

其中 $T$ 为参考帧的相机外参矩阵。得到 2D‑3D 对应点后，使用 **RANSAC + PnP** 估计查询图像的 6‑DOF 初始位姿。

**迭代位姿精化**：从估计位姿重新渲染颜色和深度图，再次执行混合匹配（Eq. 11）和 2D‑3D 提升（Eq. 12），重复匹配与估计过程，逐次求精。该迭代机制使得位姿估计能够收敛到更高精度。

## 实验与分析

### 主实验结果

SplatHLoc 在三个公开基准数据集上进行了系统评估，涵盖室内小场景（7-Scenes）、室内大场景（12-Scenes）和室外场景（Cambridge Landmarks），并与基于结构的方法、基于回归的方法以及基于高斯溅射的渲染方法进行了全面对比。

**7-Scenes 数据集。** 如 Table 1 所示，SplatHLoc 在所有七个场景上均取得了最优或次优的中位平移/旋转误差，平均中位误差为 **0.55 cm / 0.17°**，显著优于渲染基线 STDLoc（0.76 cm / 0.24°）和回归方法 RAP_ref（0.61 cm / 0.20°）。仅使用初始位姿估计的 SplatHLoc_init 即可达到 2.36 cm / 0.64° 的平均误差，叠加迭代精化后性能大幅跃升，验证了“渲染-匹配-估计”闭环迭代的有效性。

**12-Scenes 数据集。** Table 2 显示，SplatHLoc 在中位平移/旋转误差上达到 **0.3 cm / 0.14°**，优于 ACE（0.7 cm / 0.26°）和 Marepo 等回归方法。在 R@[2cm, 2°] 召回率上，SplatHLoc 达到约 97%（场景相关，最高 100%），略低于 ACE+GS-CPR（低约 1.4 个百分点），但高于 Marepo+GS-CPR。这一结果表明，在大范围室内场景中，层次化检索-匹配框架与回归方法具有竞争力，且在中位误差上更具优势。

**Cambridge Landmarks 数据集。** Table 3 的室外场景结果显示，SplatHLoc 与 STDLoc 性能相当，在部分场景上有轻微改进（如 College 场景平移误差 10 cm vs 10 cm，旋转误差 0.39° vs 0.43°；Church 场景 5 cm / 0.11° vs 5 cm / 0.10°）。需要指出的是，该数据集的对比结论置信度为 0.8，部分场景的差异较小，建议结合具体场景需求进行验证。

Figure 4 和 Figure 5 提供了定性可视化——Figure 4 以对角线拼接方式对比查询图像与估计位姿渲染图像的结构对齐程度，红色虚线框标出了视觉差异显著区域；Figure 5 展示了 SplatHLoc 与 HLoc（Sarlin et al., CVPR 2019）在 7-Scenes 五个场景上的轨迹误差对比，轨迹颜色编码位置误差，色条指示旋转误差，直观体现了 SplatHLoc 在轨迹一致性上的改进。

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/005_Figure_4.jpg]]
*Figure 4: Visualization of the relocalization errors. Each subfigure is divided by a diagonal: the top-right part shows the query image in grayscale, while the bottom-left part shows the rendered image from the estimated pose. The red dashed boxes highlight regions with pronounced visual differences in each column. More visualizations and details are in the supplementary material*

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison of camera pose estimation errors between HLoc [48] and our proposed SplatHLoc across five scenes from the 7-Scenes dataset. Visualizations of the remaining two scenes and more details are provided in the supplementary material. For each scene, we visualize the reconstructed point cloud map together with the trajectory of query images. Trajectory colors denote position error, while the color bar below shows rotation errors, with numbers indicating image indices*

### 运行时与存储开销

Figure 6 对比了 SplatHLoc 与 STDLoc 在 7-Scenes 上的平均每查询重定位耗时，分为初始位姿估计和迭代精化两部分（两者均执行四轮精化）。Table 4 以 Chess 场景为例报告了 FGS 地图的存储大小、建图时间和峰值 GPU 显存占用。需要注意的是，FGS 地图仍需额外保存 VPR 特征（Chess 场景约 62.5 MB），这是当前方案的存储开销之一。

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/011_Table_4.jpg]]
*Table 4: Mapping analysis. We report the FGS map size, mapping time and peak GPU memory on the Chess scene*

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/009_Figure_6.jpg]]
*Figure 6: Runtime analysis. We report the average relocalization time per query on the 7-Scenes dataset for STDLoc versus our proposed SplatHLoc. The runtime is divided into two parts: initial pose estimation and iterative pose refinement. Both methods perform four rounds of pose refinement*

### 消融实验

**消融 I：自适应视角检索与混合匹配。** Table 5 通过四组设置系统剥离了两个核心模块的贡献：
- **自适应视角检索（AVR）的增益**：在纯稀疏匹配管线中，启用 AVR 使 R@[5cm, 5°] 从 77.1% 提升至 91.9%（Setup I → II）；在完整 SplatHLoc 管线中，AVR 同样带来显著提升（Setup III → IV）。这一定量证据直接支撑了核心瓶颈分析——弱纹理区域（如 Stairs 场景）的初始位姿估计鲁棒性因虚拟视图合成而大幅改善。
- **混合匹配器的增益**：Setup IV（完整 SplatHLoc）在所有指标上均优于 Setup III（无混合匹配器），平均误差从 1.03 cm / 0.30° 降至最优水平，R@[5cm, 5°] 达到 91.9%。

**消融 II：混合匹配器中粗/细贡献分离。** Table 6 进一步拆分了渲染特征与图像特征在粗匹配和细匹配阶段的作用：
- **M + I_fine**（渲染特征粗匹配 + 图像半稠密特征细匹配）在所有指标上取得最优，验证了核心洞察：渲染特征具有跨视图一致性，适合 patch 级粗匹配；而半稠密特征（JamMa）在像素级细匹配中精度更高。
- **I_coarse + I_fine**（纯图像特征粗+细匹配）在室内场景的 R@[2cm, 2°] 召回率上出现退化，表明渲染特征在粗匹配阶段对召回率的贡献不可替代。
- **FGS-Matcher**（纯渲染特征粗+细匹配，即 STDLoc 方案）性能明显低于混合方案，说明渲染特征与查询特征之间的域差异使其难以建模精细几何关系。

### 自适应检索的超参数与扰动策略

Supplementary Table I 列出了自适应检索过程中的关键超参数。Table II 对比了 Uniform、Normal 和 Random 三种扰动策略，报告了初始定位的平均耗时。Figure I 和 Figure II 分别展示了扰动角度 a 和扰动距离 b 对 R@[5cm, 5°] 精度的影响曲线，为参数选择提供了经验依据。Figure III 展示了 k2（虚拟视图数量）对精度和初始定位耗时的权衡关系。Figure IV 定性可视化了自适应检索过程：粗检索候选视图与查询的共视区域有限、内点数不足（绿色线为通过几何验证的内点，蓝色为其他匹配）；通过合成位姿扰动虚拟视图并进行精细检索后，共视性显著增加，内点数大幅提升。

### 失败模式与局限分析

Figure VI 系统展示了 SplatHLoc 的两类典型失败案例：
1. **稀疏观测区域的渲染质量退化**：在训练视角覆盖不足的区域，高斯地图的渲染质量下降，导致匹配失败和位姿估计误差增大。
2. **重复纹理场景的误匹配**：高度重复的结构（如走廊、楼梯）使特征匹配产生歧义，即使渲染质量良好也可能导致错误对应。

此外，方法还存在以下已知局限：
- FGS 训练依赖 COLMAP 提供的 SfM 初始点云，当 SfM 重建失败时建图受阻。
- 目前仅支持单 GPU 训练，地图存储需额外保存 VPR 特征。
- 所有实验在单张 NVIDIA RTX 3090 GPU 上进行，对比方法结果取自原论文或使用作者提供的模型复现，FGS 训练使用统一的 30,000 步与默认超参数，公平性得到一定保障。

### 补充图表

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/004_Table_1.jpg]]
*Table 1: Relocalization results on 7-Scenes dataset. We report the median translation (cm) and rotation (°) errors for each scene. The best and second-best results are bolded and underlined, respectively*

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/007_Table_2.jpg]]
*Table 2: Relocalization results on the 12-Scenes dataset. We report the median translation (cm) and rotation errors (°), and the percentage of query images below 2 cm, 2° pose error*

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/008_Table_3.jpg]]
*Table 3: Relocalization results on Cambridge Landmarks dataset. We report the median translation (cm) and rotation (°) errors of different methods*

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/012_Table_5.jpg]]
*Table 5: Ablation study I. We investigate the impact of the proposed Adaptive C2F Retrieval and Hybrid C2F Matching*

![[assets/figures/papers/paper_list_l2520_https_arxiv_org_abs_2603_29185/figures/010_Table_6.jpg]]
*Table 6: Ablation study II. We ablate the hybrid matcher by isolating rendered features’ coarse and fine contributions. FGS-Matcher is adopted from STDLoc, which uses rendered features in both coarse and fine matching stages*

## 方法谱系与知识库定位

### 1. 在层次化视觉重定位谱系中的位置

SplatHLoc 属于**基于结构的层次化重定位**（structure-based hierarchical relocalization）方法，其直接前身是 **HLoc**（Sarlin et al., CVPR 2019）。HLoc 建立了“全局检索 → 局部特征匹配 → PnP 位姿估计”的标准流水线，但受限于数据库图像视角稀疏与弱纹理区域匹配质量不足两个核心瓶颈。

SplatHLoc 沿袭 HLoc 的层次化框架，但在三个关键环节进行了根本性改造：

| 环节 | HLoc（基线） | SplatHLoc（本文） |
|------|-------------|-------------------|
| 场景表示 | 稀疏 SfM 点云 | 特征高斯溅射（FGS）地图，可渲染颜色、深度及低维可解码特征 |
| 视角检索 | 直接检索数据库图像 | 粗-细自适应检索：在检索位姿邻域渲染虚拟视图并二次检索 |
| 特征匹配 | 纯图像特征匹配（SP+LG） | 混合粗-细匹配：渲染特征做粗匹配，半稠密匹配器做细匹配 |

从方法谱系看，SplatHLoc 处于**稀疏 SfM 检索**与**端到端回归方法**之间：它保留了检索-匹配-几何估计的可解释流水线，同时通过 3DGS 渲染能力弥补了检索方法视角覆盖不足的缺陷。

### 2. 与基于 3DGS 的重定位方法的关系

近年来，3D Gaussian Splatting（3DGS）被引入重定位任务，形成了两条主要技术路线：

**（1）渲染-匹配路线**：以 **STDLoc** 为代表，利用 3DGS 渲染新视角的 RGB 图像，再从中提取特征进行匹配。SplatHLoc 与 STDLoc 共享“渲染虚拟视图辅助匹配”的核心思想，但存在本质差异：STDLoc 仅渲染 RGB 图像，匹配时仍依赖从渲染图像中提取的特征；SplatHLoc 则直接渲染 FGS 地图中的特征场，获得具有跨视图一致性的渲染特征，用于粗匹配阶段。消融实验（Table 6）表明，SplatHLoc 的混合匹配器（M + I_fine）在所有指标上均优于 STDLoc 的 FGS-Matcher（纯渲染特征匹配），验证了渲染特征与图像特征分工协作的有效性。

**（2）渲染-优化路线**：以 **LoGS** 为代表，通过可微渲染直接优化查询图像的位姿，将重定位转化为迭代渲染与梯度下降问题。这类方法的优势在于无需显式匹配，但对初始化敏感且计算开销较大。SplatHLoc 保留了匹配机制，但在位姿精化阶段引入了“渲染-匹配-重估计”的迭代循环（Section 3.4），吸收了渲染-优化路线的“从估计位姿重新渲染”思想，同时避免了可微渲染优化的高计算成本。

### 3. 与回归方法的关系

端到端场景坐标回归方法（如 **DSAC\***, Brachmann et al., TPAMI 2021；**ACE**，Brachmann et al., CVPR 2023）直接从图像像素回归 3D 坐标，在训练充分的场景中效率极高。然而，它们缺乏显式的几何验证机制，在视角变化剧烈或弱纹理区域容易出现系统性偏差。

**ACE+GS-CPR**（Liu et al., ICLR 2025）将回归方法与 3DGS 位姿优化结合，在 12-Scenes 的 R@[2cm,2°] 指标上略优于 SplatHLoc（约高 1.4%，见 Table 2）。但 SplatHLoc 在平移/旋转中位误差上表现更优（0.3 cm / 0.14° vs ACE 的 0.7 cm / 0.26°），表明混合匹配策略在精度-召回率权衡上与回归-优化路线各有侧重。

### 4. 适用边界

**适合的场景**：
- 室内外中小规模环境（7-Scenes、12-Scenes、Cambridge Landmarks 级别）
- 数据库图像视角覆盖有限但 SfM 可成功重建的场景
- 弱纹理区域占比较高的场景（自适应视角检索对此类场景提升显著）

**不适合/需要谨慎的场景**（来自 limitations 分析）：
- **训练视角稀疏区域**：FGS 地图渲染质量下降，导致匹配失败（Figure VI 第一行）
- **高度重复纹理**：如走廊、楼梯等场景，渲染特征可能产生错误匹配（Figure VI 第二行）
- **SfM 初始化失败**：FGS 训练依赖 COLMAP 提供的初始点云，当 SfM 无法收敛时建图受阻
- **超大规模环境**：当前不支持场景分块，地图存储（如 Chess 场景需 62.5 MB）和单 GPU 训练限制其可扩展性

### 5. 局限与开放问题

**已确认的局限**：
1. FGS 地图在训练视角稀疏区域渲染质量下降，直接导致定位失败。
2. 对重复纹理场景的鲁棒性不足，渲染特征的判别力在相似外观区域退化。
3. 建图流程强依赖 COLMAP SfM，在无纹理或动态场景中可能中断。
4. 地图存储需额外保存 VPR 特征，存储开销高于纯 3DGS 表示。

**待探索的开放问题**：
1. 能否用最新的 3D 重建基础模型（如 DUSt3R、MASt3R）替代 COLMAP 初始化高斯原语，降低对传统 SfM 的依赖？
2. 如何通过场景分块策略将方法扩展至城市级或建筑群级的大规模环境？
3. 训练图像数量对 FGS 地图质量和最终定位性能的影响边界是什么？是否存在“足够好”的临界点？
4. 能否在保持精度的同时，进一步压缩每高斯原语的特征维度（当前通过特征解码器 d 降维），以降低地图存储开销？

### 6. 与更广泛知识库的关联

SplatHLoc 的核心思想——**渲染特征与图像特征的混合匹配**——与更广泛的“神经渲染辅助视觉定位”趋势一致。它将 3DGS 从单纯的视图合成工具提升为**特征场表示**，使得渲染结果不仅用于视觉对齐，更直接参与特征匹配过程。这一思路与 NeRF-based 定位方法（如 NeRF-Loc）中“从辐射场渲染特征”的做法一脉相承，但 SplatHLoc 受益于 3DGS 的实时渲染能力，在效率上具有显著优势（Figure 6：平均每查询定位时间低于 STDLoc）。

此外，自适应视角检索策略与“主动视角规划”和“检索增强”领域存在潜在交叉：通过扰动初始检索位姿生成虚拟候选视图，本质上是一种在 SE(3) 空间中进行局部稠密采样的检索增强策略，这一思想可推广至其他需要视角覆盖的任务。

## 原文 PDF

![[paperPDFs/CVPR_2026/Hierarchical_Visual_Relocalization_with_Nearest_View_Synthesis_from_Feature_Gaussian_Splatting.pdf]]
