---
title: "SymphoMotion: 4D Dynamic and Camera Control for Video Generation"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/SymphoMotion_4D_Dynamic_and_Camera_Control_for_Video_Generation.pdf
aliases:
- SymphoMotion
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 引入相机轨迹控制 (CTC) 和物体动态控制 (ODC) 两个互补模块，CTC 结合显式相机路径与几何感知点云渲染注入3D结构先验，ODC 融合2D视觉锚点与3D轨迹嵌入，实现解耦的3D感知联合运动控制。
primary_logic: 通过将相机姿态与点云渲染结合，为生成提供丰富的3D几何结构上下文；同时利用投影的2D边界框作为空间锚点和3D轨迹嵌入作为深度感知引导，使得模型能够在不混淆相机视差的情况下保持物体运动的精确性和一致性。
claims:
- 在 RealCOD-25K 测试集上，SymphoMotion 在 FID、FVD、相机平移/旋转误差、Box-IoU 指标上均显著优于 CameraCtrl、ViewCrafter、Uni3C 和 MotionCtrl。
- 消融实验表明，移除点云渲染 (w/o Cpcd)、2D 边界框 (w/o 2D boxes) 或 3D 轨迹 (w/o 3D trajectory) 均导致 Box-IoU 明显下降，验证了各组件对物体运动精确性的贡献。
- 用户研究 (1-5分制) 中，SymphoMotion 在视觉质量 (4.87)、文本对齐 (4.02)、相机运动 (4.36)、物体运动 (4.58) 四个维度均获得最高分。
- RealCOD-25K (test set) 上 FID↓ = 70.47
---

# SymphoMotion: 4D Dynamic and Camera Control for Video Generation

> [!tip] 核心洞察
> 通过将相机姿态与点云渲染结合，为生成提供丰富的3D几何结构上下文；同时利用投影的2D边界框作为空间锚点和3D轨迹嵌入作为深度感知引导，使得模型能够在不混淆相机视差的情况下保持物体运动的精确性和一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | SymphoMotion：面向视频生成的4D动态与相机控制 |
| 英文题名 | SymphoMotion: 4D Dynamic and Camera Control for Video Generation |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2604.03723) · [Project](https://grenoble-zhang.github.io/SymphoMotion/) · [Code](https://github.com/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SymphoMotion |
| Dataset | RealCOD-25K, User Study |

> [!tip] 效果简介
> - RealCOD-25K (test set) 上，FID↓ 70.47 vs best competitor (see Table 1) (N/A)。
> - RealCOD-25K 上，FVD↓ 332.50 vs best competitor (see Table 1) (N/A)；CamTransErr↓ 0.37 vs best competitor (see Table 1) (N/A)；CamRotErr↓ 0.05 vs best competitor (see Table 1) (N/A)。
> - User Study (1-5 scale) 上，Visual Quality↑ 4.87 vs best competitor (see Table 2) (N/A)。

## 概述

### 问题瓶颈

可控视频生成在动态场景中面临一个核心挑战：**相机运动与物体运动在2D图像平面上的耦合**。现有方法要么仅处理相机运动（如 **CameraCtrl**, He et al., arXiv 2024），要么仅处理物体运动，少数联合控制方法（如 **MotionCtrl**, Wang et al., SIGGRAPH 2024）仍停留在2D轨迹层面，无法解耦由相机视差引起的表观位移与真实的物体运动。这一瓶颈的深层原因在于缺乏真实世界中同时标注相机位姿与3D物体轨迹的数据集，导致模型难以学习3D感知的运动表征。

### 核心方法

SymphoMotion 通过两个互补模块实现**解耦的3D感知联合运动控制**：

- **相机轨迹控制 (Camera Trajectory Control, CTC)**：将显式相机路径与几何感知的点云渲染相结合，为扩散模型注入3D结构先验，使模型在视角变化时保持空间一致性。
- **物体动态控制 (Object Dynamics Control, ODC)**：融合2D视觉锚点（投影边界框）与3D轨迹嵌入，通过跨注意力机制将运动感知的token注入生成过程，使物体运动不被相机视差混淆。

这一设计的关键洞察在于：**点云渲染提供丰富的3D几何上下文，而投影2D边界框作为空间锚点与3D轨迹嵌入的深度感知引导相结合**，使模型能够在不混淆相机视差的情况下保持物体运动的精确性与一致性。方法架构参见 Figure 2。

### 方法谱系与知识库定位

SymphoMotion 建立在视频扩散模型 **Wan-I2V** 的 DiT 架构之上，采用 Flow Matching 范式。在相机控制维度，它从 **ViewCrafter** (Yu et al., arXiv 2024) 的点云视图合成思路中汲取灵感，但将点云从中间表示升级为显式的3D几何先验注入机制；在物体运动维度，它超越了 **MotionCtrl** 的2D轨迹方案，引入3D轨迹嵌入实现深度感知的运动建模。与 **Uni3C** 等基于Transformer的相机控制方案相比，SymphoMotion 首次实现了真实世界数据驱动的、完全解耦的3D感知联合控制。

为支撑这一方法，作者构建了 **RealCOD-25K** 数据集，包含配对的相机位姿与3D物体轨迹标注（数据构建流程见 Figure 4），填补了真实场景联合运动标注数据的空白。

### 主要结果

在 RealCOD-25K 测试集上，SymphoMotion 在五项关键指标上均显著优于现有方法（Table 1）：
- **视觉质量**：FID 70.47，FVD 332.50，均达到最优。
- **相机控制精度**：相机平移误差 (CamTransErr) 0.37，旋转误差 (CamRotErr) 0.05，表明CTC模块对视角变化的精确把控。
- **物体定位准确性**：Box-IoU 61.88，大幅领先最佳基线，验证了ODC模块在动态场景中保持物体运动一致性的能力。

用户研究（Table 2，1-5分制）进一步证实了这些优势：SymphoMotion 在视觉质量 (4.87)、文本对齐 (4.02)、相机运动 (4.36)、物体运动 (4.58) 四个维度均获得最高评分，其中物体运动维度领先幅度最大，凸显了3D轨迹控制的独特价值。

消融实验（Table 3）揭示了各组件的因果贡献：移除点云渲染 (w/o Cpcd) 使 Box-IoU 降至 56.74，移除2D边界框 (w/o 2D boxes) 降至 54.32，而移除3D轨迹条件 (w/o 3D trajectory) 导致最严重的性能退化（Box-IoU 52.16, FVD 343.80），证实了3D轨迹嵌入对物体运动建模的必要性。定性消融结果参见 Figure 7。

## 背景与动机

### 问题背景：视频生成中的运动控制需求

可控视频生成的核心挑战之一，在于同时精确地操纵**相机视角运动**与**场景内物体动态**。给定一张参考图像，用户期望指定“相机如何移动”以及“画面中的物体如何运动”，并生成一段时空一致、忠实反映两种运动信号的视频。这一能力对于电影预演、虚拟制作、增强现实等应用至关重要。

然而，相机运动与物体运动在二维投影平面上天然耦合：相机平移引起的视差变化，与物体自身的三维位移，在图像空间中可能产生相似的像素偏移模式。若生成模型无法区分这两种运动来源，便容易产生物体漂移、几何失真或运动不一致等伪影。

### 现有方法的缺口

当前方法在处理相机与物体运动控制时，存在三个主要瓶颈：

**1. 运动控制的耦合与维度局限。** 多数工作要么仅支持单一运动类型（如仅控制相机或仅控制物体），要么将两种运动统一建模为二维图像平面的光流场或轨迹。例如，**CameraCtrl**（He et al., arXiv 2024）仅通过 Plücker 嵌入控制相机，无法处理物体运动；**MotionCtrl**（Wang et al., SIGGRAPH 2024）虽支持联合控制，但其物体运动表示仍基于 2D 轨迹，缺乏深度感知，难以区分视差与真实物体位移。

**2. 缺乏 3D 几何先验的注入。** 纯 2D 运动表示无法为生成模型提供场景的立体结构信息。当相机发生大幅度平移或旋转时，模型缺乏对遮挡关系、透视变化的显式理解，导致生成结果中出现物体悬浮、边界模糊或空间关系错乱。

**3. 训练数据的根本性缺失。** 现有数据集（如 RealEstate10K、SynFMC）要么仅包含相机运动标注，要么仅提供合成场景中的单一运动类型。真实世界中**配对标注相机位姿与 3D 物体轨迹**的视频数据集几乎空白，严重制约了联合控制模型的训练与评估。

### 本文动机与核心思路

针对上述缺口，SymphoMotion 提出了一种**解耦的 3D 感知联合运动控制框架**。其核心动机在于：将相机控制与物体控制设计为两个互补但独立的模块，并分别注入 3D 几何先验与深度感知的运动表示，使模型能够在理解场景空间结构的前提下，精确解耦并复现两种运动。

具体而言，SymphoMotion 引入两个关键机制：

- **相机轨迹控制（Camera Trajectory Control, CTC）**：将显式相机路径与几何感知的点云渲染相结合，利用深度估计网络（Depth-Pro）从参考图像重建场景点云，并依据相机轨迹投影渲染，为扩散模型提供丰富的 3D 结构上下文。
- **物体动态控制（Object Dynamics Control, ODC）**：将投影到图像平面的 2D 边界框作为空间锚点，同时将 3D 物体轨迹通过专用编码器转化为运动感知 token，经跨注意力注入生成过程，实现深度感知的物体运动引导。

此外，为支撑这一框架的训练与评估，本文构建了 **RealCOD-25K**——首个包含配对相机位姿与 3D 物体轨迹标注的真实世界视频数据集，填补了该领域的数据空白。

## 核心创新

SymphoMotion 的核心创新在于首次实现了**完全解耦的3D感知联合运动控制**——将相机轨迹控制（Camera Trajectory Control, CTC）与物体动态控制（Object Dynamics Control, ODC）设计为两个独立且互补的模块，分别注入3D几何结构先验与3D轨迹嵌入，从而在不混淆相机视差的情况下保持物体运动的精确性和空间一致性。这一设计从根本上改变了现有方法的控制范式，具体体现在以下四个关键维度的突破。

### 从2D平面控制到3D感知控制

现有联合控制方法（如 **MotionCtrl** (Wang et al., SIGGRAPH 2024)）依赖2D轨迹或光流场来表示运动，其根本缺陷在于无法区分图像平面上的表观位移究竟源于相机视差还是真实的物体运动。SymphoMotion 将控制信号提升至3D空间：CTC 模块通过显式相机位姿轨迹与点云渲染相结合，为生成过程提供丰富的几何结构上下文；ODC 模块则将3D物体轨迹嵌入与投影的2D边界框视觉锚点相融合，使模型能够感知深度并精确定位运动物体。这一范式转变是解决动态场景中运动-空间一致性问题的根本因果杠杆。

### 相机控制机制的升级：从 Plücker 嵌入到几何感知注入

传统相机控制方法（如 **CameraCtrl** (He et al., arXiv 2024)）仅使用 Plücker 射线嵌入作为条件信号，缺乏对场景3D结构的显式建模。SymphoMotion 的 CTC 模块借鉴 **ViewCrafter** (Yu et al., arXiv 2024) 的点云视图合成思路，利用 Depth-Pro 从参考图像估计深度并构建点云，结合相机编码器提取的 Plücker 特征与点云渲染的几何特征，通过 Viewpoint Control Module（基于 ControlNet 架构）注入扩散模型。这种“显式相机路径 + 点云几何先验”的双重条件设计，使模型在相机运动时能够保持场景结构的几何一致性，避免了仅依赖 Plücker 嵌入时常见的结构扭曲和漂移。

### 物体运动表示的突破：从2D锚点到3D轨迹嵌入

MotionCtrl 等基线方法使用2D边界框或关键点轨迹来引导物体运动，缺乏深度维度的约束，导致物体在相机运动场景中容易“漂移”或消失。SymphoMotion 的 ODC 模块采用双通路设计：一方面将3D物体轨迹通过轨迹编码器（含时间降采样器）与语义提示融合，生成运动感知 token，经跨注意力注入 DiT 层的特征空间；另一方面将投影的2D边界框直接渲染到点云帧上，作为显式的空间锚点。这种“3D轨迹嵌入 + 2D视觉引导”的组合确保了物体运动在深度感知和平面定位两个层面都得到精确约束，是 Box-IoU 显著提升的关键机制。

### 训练数据与联合控制范式的协同重构

上述控制机制的升级离不开配套数据基础设施的支撑。现有数据集（如 RealEstate10K、SynFMC）或仅含相机运动，或仅含物体运动，缺乏真实世界中联合标注相机位姿与3D物体轨迹的数据。SymphoMotion 构建了 RealCOD-25K 数据集，通过视频筛选与自动标注两个管线，首次提供大规模配对标注。在此基础上，CTC 与 ODC 作为完全解耦的独立分支共享基座模型（Wan-I2V DiT 架构），实现了真正意义上的同步联合控制，而非 MotionCtrl 式的耦合2D运动场或 MotionPrompting 的部分解耦方案。消融实验证实，移除任一控制分支（点云渲染、2D边界框、3D轨迹）均导致 Box-IoU 显著下降（Table 3），验证了各组件对联合控制精度的独立贡献。

### 需手动验证的开放问题

- 轨迹编码器中时间降采样器的具体设计（从 N 帧到 N˜ 帧）在现有材料中未详细披露，其对时序运动平滑性的影响需要进一步确认。
- Object Motion Module 除跨注意力外是否包含额外的 Transformer 块或其他结构，原文未明确说明。
- RealCOD-25K 数据集中每个视频的平均标注物体数量及轨迹分布统计未提供，可能影响对方法泛化能力的判断。

## 整体框架

SymphoMotion 是一个基于扩散模型的视频生成框架，旨在实现对相机运动与物体动态的**解耦、同步且3D感知**的联合控制。其核心设计思路是将两类运动控制任务分配给两个互补且独立的模块，共享一个预训练的视频扩散基座模型，从而避免传统方法中因耦合表示导致的视差混淆与运动不一致问题。

### 输入与输出定义

框架的输入由四部分组成：
- 一张参考图像 $f \in \mathbb{R}^{3 \times h \times w}$，作为视频生成的视觉起点；
- 一段文本提示，描述场景语义；
- 一组相机轨迹 $\{ C^{i} \}_{i=1}^{N}$，定义 $N$ 帧目标视图的相机位姿序列；
- 一组 $M$ 个物体的 3D 运动轨迹 $\{ P_i^{j} \}_{i=1,j=1}^{M,N}$ 及其语义标签 $\{ y_i \}_{i=1}^{M}$。

输出为一段 $N$ 帧视频，其中相机视角严格遵循给定的相机轨迹，同时每个指定物体的运动在3D空间中与输入轨迹保持一致。

### 双分支控制架构

如 Figure 2 所示，SymphoMotion 在 Wan-I2V 扩散模型之上构建了两个并行的控制分支：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/002_Figure_2.jpg]]
*Figure 2: Overview of SymphoMotion. Built on Wan-I2V [45], SymphoMotion introduces two complementary mechanisms for simultaneous control of camera and object motion: Camera Trajectory Control (CTC) and Object Dynamics Control (ODC). Given a reference image, a text prompt, and the specified camera and object trajectories, CTC employs the Viewpoint Control Module (VCM) to integrate 3D geometric priors with camera motion for precise camera trajectory control. In parallel, ODC, powered by the Object Motion Module (OMM), combines 2D visual guidance with 3D motion cues to achieve dynamic and spatially coherent object manipulation*

**相机轨迹控制（Camera Trajectory Control, CTC）** 负责精确的相机视角控制。该分支接收相机轨迹与参考图像，首先利用 Depth-Pro 估计单帧深度并重建场景点云，随后将显式相机路径与几何感知的点云渲染特征相结合，通过 Viewpoint Control Module（基于 ControlNet 结构）注入扩散模型的去噪过程。点云提供的 3D 结构先验使模型能够区分由相机运动引起的视差变化与真实的物体位移，从而在动态场景中维持空间一致性。

**物体动态控制（Object Dynamics Control, ODC）** 负责细粒度的物体运动建模。该分支采用双重引导策略：一方面将 3D 物体轨迹投影为 2D 边界框，直接渲染在点云帧上作为显式的空间锚点，为模型提供逐帧的物体定位参考；另一方面通过轨迹编码器将 3D 轨迹与语义提示融合为运动感知 token，经跨注意力机制注入 DiT 的每一层 Transformer 块中，赋予模型深度感知的运动理解能力。

### 信息流与联合优化

两个控制分支的信息流在基座扩散模型中交汇。CTC 通过 ControlNet 的残差连接修改去噪网络的特征表示，ODC 则通过跨注意力直接调制 DiT 层的隐变量。整个框架以端到端方式联合训练，优化目标为 Flow Matching 的速度预测损失，同时覆盖相机控制参数 $\phi_{\theta}$ 和物体动态控制参数 $\psi_{\theta}$：

$$
\min_{\theta} \mathbb{E}_{z_0,t,\epsilon,c_y,c_f,c_{cam},c_{pcd}} [\| v_{\theta}(z_t, t, c_y, c_f, \phi_{\theta}(c_{cam}, c_{pcd}), \psi_{\theta}(\{P_i^{j}\}_{i=1,j=1}^{M,N},\{y_i\}_{i=1}^{M})) - v_t \|^2]
$$

这种解耦设计使得相机运动与物体运动可以独立指定、任意组合——用户可以仅控制相机、仅控制物体、或同时控制两者，而无需重新训练或切换模型。Figure 3 展示了推理阶段的交互流程：用户通过界面输入相机运动参数并交互式绘制物体的 3D 轨迹，系统即可生成符合双重约束的视频。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/003_Figure_3.jpg]]
*Figure 3: Inference pipeline of SymphoMotion. Users can specify camera motion and interactively draw 3D trajectories of selected objects through our interface, and the system generates videos that align with the user-defined camera and object motion*

### 关键设计决策

框架中有两个关键的结构选择值得注意。其一，**点云渲染**的引入（受 ViewCrafter 启发）是 CTC 区别于仅使用 Plücker 嵌入方法（如 CameraCtrl）的核心——它为扩散模型提供了显式的 3D 几何上下文，使相机控制不再仅依赖2D图像平面的隐式线索。其二，ODC 中**2D边界框与3D轨迹嵌入的融合**解决了纯2D轨迹方法（如 MotionCtrl）在相机运动场景下无法区分物体真实位移与视差变化的根本缺陷——2D锚点提供像素级定位，3D嵌入提供深度感知的运动语义，二者协同工作。

## 核心模块与公式推导

SymphoMotion 以 Wan-I2V 作为基座视频扩散模型，采用 Flow Matching 框架。给定参考图像 $f \in \mathbb{R}^{3 \times h \times w}$ 和文本提示，模型通过两个互补的控制模块实现解耦的 4D 动态与相机控制：**相机轨迹控制 (Camera Trajectory Control, CTC)** 和 **物体动态控制 (Object Dynamics Control, ODC)**。整体架构如 Figure 2 所示。

### 3.1 基座模型与 Flow Matching 目标

基座模型基于 DiT 架构，接受文本嵌入（umT5）和图像嵌入（CLIP）作为条件。在 Flow Matching 框架下，潜变量通过线性插值构建：

$$z_t = t z_1 + (1 - t) z_0$$

其中 $t$ 从 logit-normal 分布采样。模型预测真实速度 $v_t = z_1 - z_0$，训练目标为：

$$\min_{\theta} \mathbb{E}_{z_0, t, \epsilon, c_y, c_f} \left[ \| v_{\theta}(z_t, t, c_y, c_f) - v_t \|^2 \right]$$

其中 $c_y$ 为文本条件，$c_f$ 为图像条件。

### 3.2 相机轨迹控制 (CTC)

CTC 模块通过显式相机路径与几何感知点云渲染注入 3D 结构先验。具体而言，首先利用 Depth-Pro 从参考图像估计深度图并生成点云，随后结合相机编码器提取的 Plücker 特征与点云渲染特征，通过 Viewpoint Control Module (VCM，基于 ControlNet 结构) 注入扩散模型。CTC 模块的训练目标为：

$$\min_{\theta} \mathbb{E}_{z_0, t, \epsilon, c_y, c_f, c_{cam}, c_{pcd}} \left[ \| v_{\theta}(z_t, t, c_y, c_f, \phi_{\theta}(c_{cam}, c_{pcd})) - v_t \|^2 \right]$$

其中 $c_{cam}$ 为相机轨迹特征，$c_{pcd}$ 为点云几何特征，$\phi_{\theta}$ 表示 VCM 的可学习参数。这一设计与 **ViewCrafter** (Yu et al., arXiv 2024) 的点云视图合成思路同源，但 SymphoMotion 将其融入联合控制框架，而非独立使用。

### 3.3 物体动态控制 (ODC)

ODC 模块融合 2D 视觉锚点与 3D 轨迹嵌入，实现深度感知的物体运动控制。其核心包含两个子组件：

**2D 视觉引导**：将每帧投影的 2D 边界框直接渲染到点云帧上，作为显式的空间锚点，引导模型在帧间定位每个物体。这一设计与 **MotionCtrl** (Wang et al., SIGGRAPH 2024) 的纯 2D 轨迹表示形成对比——后者无法解耦相机视差与真实物体运动。

**3D 轨迹嵌入**：给定 $M$ 个物体的 3D 轨迹 $\{P_i^{j}\}_{i=1,j=1}^{M,N}$ 和语义提示 $\{y_i\}_{i=1}^{M}$，轨迹编码器 $\psi_{\theta}$ 将其融合为运动感知 token：

$$c_{obj} = \psi_{\theta} \left( \{P_i^{j}\}_{i=1,j=1}^{M,N}, \{y_i\}_{i=1}^{M} \right)$$

这些 token 随后通过跨注意力注入 DiT 的每一层：

$$Z_i' = Z_i + \mathrm{CrossAttn}(Q=Z_i, K=c_{obj}, V=c_{obj})$$

其中 $Z_i$ 为第 $i$ 层 DiT 的特征表示。该机制使得物体运动信息以深度感知的方式参与特征更新，而不干扰相机控制分支。

### 3.4 联合训练目标

CTC 和 ODC 共享基座模型参数，通过端到端联合训练实现解耦控制。整体训练目标为：

$$\min_{\theta} \mathbb{E}_{z_0, t, \epsilon, c_y, c_f, c_{cam}, c_{pcd}} \left[ \| v_{\theta}(z_t, t, c_y, c_f, \phi_{\theta}(c_{cam}, c_{pcd}), \psi_{\theta}(\{P_i^{j}\}, \{y_i\})) - v_t \|^2 \right]$$

训练配置为 32 块 NVIDIA H100 GPU，总 batch size 32，使用 AdamW 优化器，学习率 $1 \times 10^{-5}$。

### 3.5 关键设计对比

| 控制维度 | 基线方案 | SymphoMotion 方案 |
|---------|---------|-----------------|
| 相机运动 | Plücker 嵌入 (CameraCtrl) 或光流场 (MotionCtrl) | 显式相机轨迹 + 点云渲染的几何感知特征 |
| 物体运动 | 2D 边界框/关键点/光流 (MotionCtrl) | 3D 轨迹嵌入 + 投影 2D 边界框视觉引导 |
| 联合范式 | 耦合的 2D 运动场或部分解耦但仅 2D | 完全解耦的 3D 感知控制：CTC 与 ODC 独立分支 |

> **待验证**：轨迹编码器中时间降采样器（从 $N$ 帧到 $\tilde{N}$ 帧）的具体设计细节，以及 Object Motion Module 是否包含跨注意力之外的额外结构（如 Transformer 块），在现有材料中未明确说明，需查阅完整论文或代码确认。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/001_Figure_1.jpg]]
*Figure 1: Joint Control of Camera and Object Motion. Given a reference image, a set of 3D object trajectories, and a camera trajectory, SymphoMotion generates videos that are spatially consistent and faithfully reflect both object and camera motion*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/005_Figure_5.jpg]]
*Figure 5: Independent camera motion control*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/006_Figure_6.jpg]]
*Figure 6: Simultaneous control over camera and object motions. MotionCtrl struggles to generate realistic object dynamics, causing objects to disappear from view, whereas SymphoMotion achieves high-quality simultaneous control*

## 实验与分析

### 核心性能对比

SymphoMotion 在 RealCOD-25K 测试集上与四个代表性基线进行了全面比较：纯相机控制方法 **CameraCtrl** (He et al., arXiv 2024)、**ViewCrafter** (Yu et al., arXiv 2024)、**Uni3C**，以及联合相机-物体运动控制方法 **MotionCtrl** (Wang et al., SIGGRAPH 2024)。所有方法均使用官方发布的预训练模型或按原设置微调，在统一协议下评估。

如 Table 1 所示，SymphoMotion 在所有指标上均取得最优结果。视觉质量方面，FID 达到 70.47，FVD 为 332.50，显著优于其他方法。相机运动控制精度上，相机平移误差 (CamTransErr) 仅 0.37，旋转误差 (CamRotErr) 仅 0.05，表明 CTC 模块的几何感知点云渲染有效提供了 3D 结构先验。物体运动定位方面，Box-IoU 达到 61.88，大幅领先 MotionCtrl 等基线，验证了 ODC 模块中 2D 边界框空间锚点与 3D 轨迹嵌入联合引导的有效性。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/008_Table_1.jpg]]
*Table 1: Quantitative comparison of our method SymphoMotion with CameraCtrl, ViewCrafter, Uni3C and MotionCtrl*

用户研究 (Table 2) 进一步从感知层面验证了上述结论。在 1-5 分制评分中，SymphoMotion 在视觉质量 (4.87)、文本对齐 (4.02)、相机运动 (4.36) 和物体运动 (4.58) 四个维度均获最高分，表明该方法在主观体验上也具备明显优势。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/009_Table_2.jpg]]
*Table 2: User study on visual quality, text alignment, camera motion, and object motion (scores range from 1 to 5, higher is better)*

### 消融实验：各组件的因果贡献

Table 3 通过系统消融揭示了各模块的独立贡献，所有实验均在相同设置下进行：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/010_Table_3.jpg]]
*Table 3: Quantitative results in ablation study*

- **移除点云渲染 (w/o Cpcd)**：Box-IoU 从 61.88 降至 56.74，FVD 升至 344.49。这证实了 CTC 中引入的 3D 几何先验不仅提升相机轨迹下的空间一致性，还间接改善了物体定位精度——缺乏深度结构上下文时，模型难以区分视差与真实物体运动。
- **移除 2D 边界框 (w/o 2D boxes)**：Box-IoU 进一步降至 54.32。投影到点云帧上的 2D 边界框作为显式空间锚点，为模型提供了逐帧的物体位置引导，其缺失导致物体运动建模严重退化。
- **移除 3D 轨迹 (w/o 3D trajectory)**：造成最严重的性能下降，Box-IoU 跌至 52.16，FVD 升至 343.80。3D 轨迹嵌入是 ODC 的核心条件信号，提供深度感知的运动方向与幅度信息；仅依赖 2D 视觉引导无法补偿这一缺失，证明了 3D 运动表示对精确物体控制的必要性。

定性结果 (Figure 7) 与定量趋势一致：完整模型生成的视频中物体运动轨迹准确、空间位置稳定，而各消融变体均出现不同程度的物体漂移或消失。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/007_Figure_7.jpg]]
*Figure 7: Results of different settings in the ablation study*

### 定性分析与失败模式

在独立相机运动控制场景 (Figure 5) 中，CameraCtrl 和 ViewCrafter 虽能大致跟随相机轨迹，但在大视角变化时出现几何失真；SymphoMotion 借助点云渲染保持了更稳定的空间结构。同步控制场景 (Figure 6) 的对比更为显著：MotionCtrl 在同时处理相机与物体运动时，物体常从画面中消失或产生不真实的动态，而 SymphoMotion 实现了高质量的解耦控制——相机视角平滑变化的同时，物体运动保持精确和一致。

需要指出的是，当前评估主要基于 RealCOD-25K 数据集，该数据集的物体和相机轨迹分布特性可能影响结论的泛化性。此外，论文未报告该方法在更长视频（超过 16 帧）或多物体交互场景下的表现，这些场景下的控制精度和一致性需要进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/011_Figure_8.jpg]]
*Figure 8: Interactive Panel Interface. The panel offers a unified interface for specifying motion inputs to SymphoMotion. (a) An input image is uploaded, and SAM2 extracts the mask of the target object for subsequent control. (b) The Camera Control Panel allows users to configure camera movement through rotational and translational adjustments for viewpoint specification. (c) The Object Control Panel provides interactive editing of 3D object trajectories using the automatically fitted bounding box*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/012_Figure_10.jpg]]
*Figure 10: Independent camera control for static object*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2604_03723/figures/004_Figure_4.jpg]]
*Figure 4: RealCOD-25K dataset construction pipeline*

## 方法谱系与知识库定位

SymphoMotion 的核心贡献在于将相机控制与物体运动控制解耦为两个感知 3D 结构的独立分支，从而解决了此前方法在动态场景中因视差与真实运动混淆而产生的空间一致性问题。本节从方法谱系的角度，将其与相关基线进行对比，并讨论其适用边界与开放问题。

### 与基线方法的关系

**相机控制方法。** 早期的相机控制方法主要依赖 2D 条件信号。**CameraCtrl**（He et al., arXiv 2024）使用 Plücker 嵌入编码相机位姿，通过 ControlNet 注入视频扩散模型，能够实现较为精确的相机轨迹控制，但其缺乏对场景 3D 结构的显式建模，在面对复杂几何结构时容易产生畸变。**ViewCrafter**（Yu et al., arXiv 2024）则从点云视图合成的角度出发，利用显式 3D 几何先验来增强新视角生成的保真度，但其设计目标为静态场景的视角外推，不涉及物体运动控制。**Uni3C** 采用基于 Transformer 的架构进行相机控制，但在联合运动控制场景下的表现未见详细报告。SymphoMotion 的 CTC 模块吸收了 ViewCrafter 的点云渲染思路，将其与 CameraCtrl 的 Plücker 嵌入相结合，通过 Viewpoint Control Module 将 3D 结构先验与相机轨迹信号统一注入扩散模型，从而在保持相机控制精度的同时提升了几何一致性。

**联合运动控制方法。** **MotionCtrl**（Wang et al., SIGGRAPH 2024）是目前最具代表性的联合相机与物体运动控制方法，其核心思路是将相机运动和物体运动统一表示为 2D 轨迹场，并通过运动提示（MotionPrompting）注入模型。然而，2D 轨迹场无法区分由相机视差引起的表观位移与物体自身的真实运动，导致在相机大幅移动时物体定位出现漂移甚至消失（参见 Figure 6 的定性对比）。SymphoMotion 的 ODC 模块从根本上改变了这一范式：它使用 3D 轨迹嵌入来显式编码物体在世界坐标系中的真实运动，同时将投影的 2D 边界框作为视觉空间锚点，使得模型能够在相机运动的前提下保持物体运动的精确性。这种“3D 感知 + 2D 引导”的双重机制是 SymphoMotion 相较于 MotionCtrl 的核心改进。

**数据集层面。** 此前的联合控制方法多依赖合成数据（如 SynFMC）或仅含单一运动类型的数据集（如 RealEstate10K 仅含相机运动），缺乏真实世界中配对标注的相机位姿与 3D 物体轨迹数据。SymphoMotion 构建的 RealCOD-25K 数据集填补了这一空白，为解耦式的 3D 感知联合控制提供了训练与评估基础。

### 适用边界与局限

SymphoMotion 在 RealCOD-25K 测试集上取得了全面的最优结果（Table 1），用户研究也在视觉质量、文本对齐、相机运动和物体运动四个维度上均获得最高评分（Table 2）。然而，其适用边界存在以下约束：

1. **物体数量与交互。** 当前框架的设计面向单个或多个独立运动物体的控制，但论文未明确验证其在多物体交互场景（如碰撞、遮挡、协同运动）下的鲁棒性。ODC 模块中每个物体的轨迹编码是独立进行的，跨物体的交互建模能力尚待检验。

2. **视频时长限制。** 实验设置中生成的视频帧数有限（基于 Wan-I2V 的默认配置），对于需要长时间一致性的应用场景（如超过 16 帧的连续运动），模型的累积误差和漂移问题需要进一步评估。

3. **点云质量依赖。** CTC 模块使用 Depth-Pro 进行单目深度估计以生成点云，其精度直接影响几何先验的质量。在纹理缺失、透明物体或极端光照条件下，深度估计的失效会传导至相机控制效果。

4. **轨迹编码器的设计细节。** 论文提到轨迹编码器包含时间降采样器（从 N 帧降至 N˜ 帧），但其具体实现方式未详细披露，这可能影响对长轨迹的建模能力和计算效率。

### 开放问题

以下问题需要在后续工作中进一步探索，或需通过查阅代码仓库进行验证：

- 轨迹编码器中的时间降采样器如何平衡时序精度与计算开销？其降采样策略是均匀采样、注意力池化还是可学习的聚合？
- Object Motion Module 是否包含除跨注意力之外的额外结构（如额外的 Transformer 块或门控机制），以增强运动感知 token 的表达能力？
- RealCOD-25K 数据集中每个视频平均标注的物体数量是多少？相机和物体轨迹的分布特征（如运动幅度、速度范围）如何影响模型的泛化能力？
- 该方法能否扩展到更长时间的视频生成？Flow Matching 框架下的长视频一致性保持策略是什么？
- 在多物体交互场景中，是否需要引入物体间的关系建模（如相对位置编码或图神经网络）来避免碰撞和穿透伪影？

## 原文 PDF

![[paperPDFs/arxiv_2026/SymphoMotion_4D_Dynamic_and_Camera_Control_for_Video_Generation.pdf]]