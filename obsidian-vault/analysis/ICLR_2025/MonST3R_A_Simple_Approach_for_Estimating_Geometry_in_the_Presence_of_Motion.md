---
title: "MonST3R: A Simple Approach for Estimating Geometry in the Presence of Motion"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Motion.pdf
aliases:
- MMD
- MonST3R
tags:
- ICLR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "通过在有限的动态、有姿态、有深度标签的视频数据集上进行微调，利用逐时间步点云表示（per-timestep pointmap）来适配DUSt3R架构，从而控制模型对动态场景的几何估计能力。"
primary_logic: "将静态场景的点云表示推广到每帧独立估计，并在同一相机坐标系下表示，通过小规模数据微调即可使模型隐式学习动态场景的几何结构，无需显式运动建模。全局优化中的平滑性和光流一致性损失进一步提升了鲁棒性。"
claims:
- "MonST3R直接估计动态场景每帧的点云图，并能在同一相机坐标系下对齐。"
- "通过混合小数据集微调，相机姿态估计ATE从0.354降至0.108。"
- "视频深度估计（仅尺度对齐）大幅超越DepthCrafter，Abs Rel 0.345 vs 0.692。"
- "添加相机轨迹平滑和光流投影损失提升了姿态估计，且对深度影响极小。"
---

# MonST3R: A Simple Approach for Estimating Geometry in the Presence of Motion

> [!tip] 核心洞察
> 将静态场景的点云表示推广到每帧独立估计，并在同一相机坐标系下表示，通过小规模数据微调即可使模型隐式学习动态场景的几何结构，无需显式运动建模。全局优化中的平滑性和光流一致性损失进一步提升了鲁棒性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MonST3R：面向动态场景的几何估计简单方法 |
| 英文题名 | MonST3R: A Simple Approach for Estimating Geometry in the Presence of Motion |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2410.03825); [Project](https://monst3r-project.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MonST3R (Motion DUSt3R) |
| Dataset | Sintel (video depth, scale-only alignment), Sintel (camera pose estimation), ScanNet (camera pose estimation), Bonn (single-frame depth estimation) |

> [!tip] 效果简介
> - Sintel (video depth, scale-only alignment) 上，Abs Rel 为 0.345，对比 0.692 (DepthCrafter)，变化 -0.347。
> - Sintel (camera pose estimation) 上，ATE 为 0.108，对比 0.141 (DUSt3R)，变化 -0.033。
> - ScanNet (camera pose estimation) 上，ATE 为 0.068，对比 0.078 (LEAP-VO)，变化 -0.010。

## 概述

静态场景几何估计方法（如DUSt3R）在动态场景中面临根本性瓶颈：其训练数据仅包含静态场景，导致模型无法正确对齐运动前景与背景，甚至完全无法估计前景物体的深度。这一失效源于训练数据分布与动态场景的不匹配，而非架构本身的固有限制。

MonST3R的核心洞察在于，点云图表示可以被推广到每帧独立估计，且在同一相机坐标系下表示时，对动态场景依然具有概念合理性。通过将DUSt3R的静态点云扩展为**逐时间步点云图**（per-timestep pointmap），并在有限的动态、有姿态、有深度标签的视频数据集上进行微调，模型能够隐式学习动态场景的几何结构，而无需显式的运动建模。

方法上，MonST3R仅微调解码器与预测头部（冻结编码器），混合使用PointOdyssey、TartanAir、Spring和Waymo四个数据集，采用步幅1–9的线性概率采样策略构建训练帧对。推理阶段，通过PnP+RANSAC恢复相对相机姿态，利用相机运动光流与预计算光流的差异生成静态掩码，并在全局优化中引入相机轨迹平滑损失和光流投影损失以提升鲁棒性。

实验结果表明，MonST3R在多个基准上取得了显著提升：
- **视频深度估计**：Sintel数据集上Abs Rel从DepthCrafter的0.692降至0.345（仅尺度对齐）。
- **相机姿态估计**：Sintel上ATE从DUSt3R的0.141降至0.108，ScanNet上ATE 0.068超越专用方法LEAP-VO（0.078）。
- **单帧深度估计**：Bonn数据集上Abs Rel从DUSt3R的0.141降至0.076，动态场景下保持与静态方法可比性能。

消融实验证实，仅微调解码器优于全模型微调（ATE 0.108 vs 0.118），混合四个数据集将ATE从单数据集的0.174提升至0.108，而平滑损失和光流损失的引入进一步提升了姿态估计精度，对深度影响极小。MonST3R以轻量级全局优化（约1分钟）即可实现上述性能，避免了CasualSAM等方法的昂贵测试时优化。

## 背景与动机

从二维图像恢复三维几何结构是计算机视觉的核心任务，其典型应用涵盖自动驾驶、机器人导航与增强现实等领域。近年来，以 **DUSt3R** (Wang et al., 2024c) 为代表的一类方法取得了显著进展——它们以“几何优先”的范式，直接从图像对中预测稠密的三维点云图（pointmap），并在静态场景中展现出令人瞩目的泛化能力与重建精度。

然而，现实世界是动态的。DUSt3R 等方法的根本瓶颈在于：其训练数据完全由静态场景构成，模型从未学习过如何处理运动物体。当面对包含显著前景运动的动态场景时，这种数据分布的不匹配导致了两种典型的失效模式。其一，模型倾向于将运动前景对齐，从而迫使背景点云发生错位（见图2左）；其二，模型完全无法估计前景物体的深度，将其错误地放置于背景之后（见图2右）。简言之，静态点云表示缺乏时间维度，无法表达场景在不同时刻的几何变化，这是现有方法在动态场景中失效的因果根源。

针对上述缺口，一个直接的思路是引入显式的运动估计或光流模块来补偿动态元素。但此类方案往往将几何重建与运动估计解耦，流程复杂且易受中间表示误差的累积影响。另一类方法如 **CasualSAM** (Zhang et al., ECCV 2022) 虽然能联合估计深度与相机姿态，却依赖昂贵的测试时优化（test-time optimization），难以满足实时或大规模应用的需求。视频深度估计专用方法如 **DepthCrafter** (Hu et al., 2024) 则专注于单任务，无法同时输出相机轨迹与场景几何。

本文的核心动机由此而生：是否能够保留 DUSt3R 简洁的“几何优先”范式，仅通过表示层面的最小改动与有限数据的微调，使其自然泛化至动态场景？核心洞察在于：点云图可以被推广为每时间步独立估计，且在同一相机坐标系下表示依然具有概念上的合理性。这一推广无需显式建模物体运动——模型只需从小规模、有姿态、有深度标签的动态视频数据中隐式学习动态场景的几何结构。本文提出的 **MonST3R (Motion DUSt3R)** 正是基于这一洞察，旨在以简单的架构适配实现动态场景下的几何估计，同时输出视频深度、相机姿态与动静态分割，为下游应用提供统一的几何先验。

## 核心创新

MonST3R 的核心创新在于将 DUSt3R 的静态点云图表示推广到动态场景，其根本思路并非引入显式的运动建模或光流预测模块，而是**重新定义了点云图的时间语义**。在 DUSt3R 中，点云图 $\mathbf{X}$ 描述的是一个静态场景的整体三维结构，没有时间维度。MonST3R 的关键洞察是：点云图可以按时间步独立估计，且将它们表示在同一相机坐标系下对动态场景仍然具有概念上的合理性。这一转变使得模型能够隐式地学习动态场景的几何结构，而无需显式地对物体运动进行建模。

具体而言，MonST3R 在以下维度上对 DUSt3R 进行了系统性改造：

### 1. 点云表示的时间解耦

DUSt3R 从图像对 $(I^1, I^2)$ 中预测两个点云图 $\mathbf{X}^{1;1 2}$ 和 $\mathbf{X}^{2;1 2}$，两者均位于第一个相机的坐标系下，隐含假设场景是静态的。MonST3R 将这一表示推广为**每时间步独立的点云图** $\mathbf{X}^{t} \in \mathbb{R}^{H \times W \times 3}$，每个像素对应其在时刻 $t$ 的三维坐标。当输入帧对 $(I^t, I^{t'})$ 时，网络预测 $\mathbf{X}^{t; t t'}$ 和 $\mathbf{X}^{t'; t t'}$，两者均位于相机 $t$ 的坐标系下。这一改动看似简单，却是后续所有动态处理能力的基础——它使得模型不再强制要求两帧之间的场景一致性，从而能够自然地处理运动前景与静态背景的共存。

### 2. 训练数据分布的根本性扩展

DUSt3R 仅在静态场景的图像对上训练，这导致其在动态场景中出现系统性失效：要么将运动前景对齐而错位背景点云，要么完全无法估计前景物体的深度（将其错误地放置在背景中，见图 2）。MonST3R 通过混合四个动态/静态视频数据集（PointOdyssey、TartanAir、Spring、Waymo，见表 1）进行微调来弥补这一数据分布鸿沟。这些数据集均提供相机姿态和深度真值，且大部分包含动态物体。消融实验（表 5）表明，仅此一项就将 Sintel 上的相机姿态估计 ATE 从 0.354（未微调）降至 0.108（全推理设置），降幅达 69.5%。

### 3. 极简的微调策略

与直觉相反，MonST3R 并未对 DUSt3R 进行全模型微调。实验发现，**仅微调解码器和预测头部，同时冻结 ViT 编码器**，反而取得了最佳性能（ATE 0.108 vs 全模型微调 ATE 0.118，表 5）。这一策略的优势在于：编码器在 DUSt3R 的大规模静态数据上学习到的通用视觉特征得以保留，而解码器和头部则通过少量动态数据学习如何利用这些特征来区分静态与动态区域。此外，训练对采样采用时间步幅 1–9 的线性递增概率策略，使模型既能学习短时帧间的精细对应，也能处理长时跨度下的大幅运动。

### 4. 静态区域推断与动态物体排除

MonST3R 不直接预测运动掩码，而是通过**比较相机运动诱导的光流与现成光流方法估计的光流**来推断静态区域。具体地，利用当前深度估计和相对姿态计算纯相机运动光流场 $\mathbf{F}_{\mathrm{cam}}^{t t'}$，再与现成光流 $\mathbf{F}_{\mathrm{est}}^{t t'}$ 比较，通过 L1 阈值化生成静态掩码 $\mathbf{S}^{t t'}$。这一设计的精妙之处在于：它利用了动态物体在光流残差中自然暴露的特性，无需额外的运动分割网络，且静态区域上的点云对应关系为后续的全局优化提供了高置信度约束。

### 5. 视频感知的全局优化损失

DUSt3R 的全局优化仅使用对齐损失 $\mathcal{L}_{\mathrm{align}}$，这在动态场景中容易因动态物体的干扰而产生不稳定的相机轨迹。MonST3R 引入了两项视频特定的损失函数：**相机轨迹平滑损失** $\mathcal{L}_{\mathrm{smooth}}$ 惩罚相邻帧间旋转和平移的剧烈变化，**光流投影损失** 约束优化后的深度和姿态与观测光流的一致性。消融实验（表 5）证实，这两项损失对姿态估计有显著增益，且对视频深度精度影响极小，体现了“几何优先”的设计哲学——深度估计主要依赖前馈网络的能力，优化仅用于精细化相机轨迹。

## 整体框架

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/004_Figure_3.jpg]]
*Figure 3: Dynamic global point cloud and camera pose estimation. Given a fixed sized of temporal window, we compute pairwise pointmap for each frame pair with MonST3R and optical flow from off-the-shelf method. These intermediates then serve as inputs to optimize a global point cloud and per-frame camera poses. Video depth can be directly derived from this unified representation*

MonST3R 的整体 pipeline 围绕一个核心表示展开：**逐时间步的点云图（per-timestep pointmap）**。与 DUSt3R 为静态场景输出单一全局点云不同，MonST3R 为视频的每一帧独立估计一个点云图 $\mathbf{X}^{t} \in \mathbb{R}^{H \times W \times 3}$，且所有点云均在同一相机坐标系下表示。这一设计的根本动机在于：DUSt3R 的训练数据仅包含静态场景，导致其在动态场景中将运动前景与静态背景错误对齐，且无法正确估计前景物体深度（Figure 2）。MonST3R 通过在有限的动态、有姿态、有深度标签的视频数据集上微调，使模型隐式学习动态场景的几何结构，而无需显式运动建模。

### 模块关系与数据流

整个框架由三个核心阶段构成：**逐帧对点云预测**、**动态/静态解耦与相对姿态估计**、**全局动态点云与相机姿态联合优化**。

**阶段一：逐帧对点云预测。** 给定一个视频序列，MonST3R 采用滑动时间窗口策略（Figure 3 左）选取帧对，以控制计算开销。对于任意帧对 $(I^t, I^{t'})$，共享的冻结 ViT 编码器分别提取两帧的视觉特征，随后交叉注意力解码器融合两帧信息，由 DPT 点云头部输出两个点云图 $\mathbf{X}^{t; t t'}$ 和 $\mathbf{X}^{t'; t t'}$，以及对应的置信度图 $\mathbf{C}^{t; t t'}$ 和 $\mathbf{C}^{t'; t t'}$。两个点云图均位于相机 $t$ 的坐标系下。这一阶段的关键改动在于：仅微调解码器与预测头部，冻结编码器；训练时采用步幅 1–9 的帧对采样，且步幅越大采样概率越高，以覆盖短程与长程时序依赖。

**阶段二：动态/静态解耦与相对姿态估计。** MonST3R 利用现成的光流方法估计帧间光流 $\mathbf{F}_{\text{est}}^{t t'}$，同时根据预测的深度图 $\mathbf{D}^{t; t t'}$ 和相对姿态初值，计算纯相机运动诱导的光流 $\mathbf{F}_{\text{cam}}^{t t'}$。通过比较两者的 L1 差异并阈值化，生成静态区域掩码 $\mathbf{S}^{t t'}$。随后，利用静态区域内的 2D-3D 对应关系，通过 PnP+RANSAC 求解相对相机姿态 $\mathbf{R}^{t t'}, \mathbf{T}^{t t'}$。这一静态掩码推断机制是处理动态物体的核心——它排除了动态前景对姿态估计的干扰，使模型能够依赖“置信静态区域”进行鲁棒对齐。

**阶段三：全局动态点云与相机姿态联合优化。** 在滑动窗口内，将所有帧对预测的点云图、置信度图、光流及静态掩码作为输入，构建全局优化问题（Figure 3 右）。优化变量包括每帧的深度图 $\mathbf{D}^t$、相机外参 $\mathbf{P}^t = [\mathbf{R}^t | \mathbf{T}^t]$ 和内参 $\mathbf{K}^t$。损失函数由三项组成：DUSt3R 的对齐损失 $\mathcal{L}_{\text{align}}$、相机轨迹平滑损失 $\mathcal{L}_{\text{smooth}}$，以及光流投影损失 $\mathcal{L}_{\text{flow}}$。平滑损失惩罚相邻帧间旋转和平移的剧烈变化，光流损失强制优化后的深度与姿态在静态区域与观测光流一致。消融实验表明，平滑损失权重 $w_{\text{smooth}}=0.01$ 时鲁棒性最佳，两项新增损失显著提升姿态估计精度（ATE 从 0.141 降至 0.108），同时对深度估计影响极小（Table 5）。

### 输入输出总结

- **输入**：动态场景视频帧序列。
- **中间表示**：每帧对的点云图、置信度图、光流场、静态掩码。
- **输出**：每帧的深度图（视频深度）、相机内参与外参（相机轨迹）、以及动态/静态分割掩码，这些输出共同构成时间一致的动态点云表示，可直接支持视频深度估计、相机姿态估计和动态场景重建等下游任务。

## 核心模块与公式推导

MonST3R 的核心架构继承自 DUSt3R，由共享权重的 ViT 编码器、交叉注意力解码器和 DPT 点云预测头部构成。关键改造在于将静态点云表示推广为**逐时间步点云图**（per-timestep pointmap），使模型能够隐式学习动态场景的几何结构，而无需显式建模物体运动。

### 逐时间步点云预测

给定时间 $t$ 的单帧图像 $I^t$，网络输出其点云图：

$$\mathbf{X}^{t} \in \mathbb{R}^{H \times W \times 3}$$

其中每个像素对应一个 3D 坐标，表示该点在相机坐标系下的空间位置。与 DUSt3R 的核心差异在于：**每个点云图仅关联单一时刻**，而非整个静态场景的整体表示（Section 3.2）。

对于帧对 $(I^t, I^{t'})$，网络同时预测两个点云图：

$$\mathbf{X}^{t; t t'}, \quad \mathbf{X}^{t'; t t'}$$

两者均位于相机 $t$ 的坐标系下，并伴随对应的置信度图 $\mathbf{C}^{t; t t'}$ 和 $\mathbf{C}^{t'; t t'}$。这一设计使得模型在动态场景中仍能建立跨帧的几何对应关系。

### 相对姿态估计：PnP + RANSAC

利用同一视图内的逐像素 2D-3D 对应关系，通过 PnP 算法恢复两帧间的相对旋转 $\mathbf{R}^*$ 和平移 $\mathbf{T}^*$：

$$\mathbf{R}^*, \mathbf{T}^* = \underset{\mathbf{R}, \mathbf{T}}{\mathrm{argmin}} \sum_{i \in \mathcal{I}} \| \mathbf{x}_i - \pi(\mathbf{K}^{t'}(\mathbf{R} \mathbf{X}_i^{t'; t t'} + \mathbf{T})) \|^2$$

其中 $\mathcal{I}$ 为置信度高于阈值（默认 2.0）的有效对应点集，$\pi(\cdot)$ 为投影函数。采用 RANSAC 增强对离群点的鲁棒性（Equation 1）。

### 静态区域掩码推断

为区分场景中的静态与动态区域，MonST3R 利用现成光流方法（Wang et al., 2024d）计算估计光流 $\mathbf{F}_{\mathrm{est}}^{t t'}$，并与纯相机运动诱导的光流进行比较。相机运动光流通过反投影-变换-重投影计算：

$$\mathbf{F}_{\mathrm{cam}}^{t t'} = \pi(\mathbf{D}^{t; t t'} \mathbf{K}^{t'} \mathbf{R}^{t t'} \mathbf{K}^{t^{-1}} \hat{\mathbf{x}} + \mathbf{K}^{t'} \mathbf{T}^{t t'}) - \mathbf{x}$$

其中 $\mathbf{D}^{t; t t'}$ 为当前深度估计，$\hat{\mathbf{x}}$ 为齐次像素坐标。当两者的 L1 差异小于阈值 $\alpha$ 时，标记为静态：

$$\mathbf{S}^{t t'} = [\alpha > \|\mathbf{F}_{\mathrm{cam}}^{t t'} - \mathbf{F}_{\mathrm{est}}^{t t'}\|_{\mathrm{L}1}]$$

该静态掩码在后续全局优化中用于排除动态物体的干扰（Equation 2, 3）。

### 全局动态点云与相机姿态优化

为获得时序一致的全局几何与相机轨迹，MonST3R 在滑动时间窗口内联合优化多帧深度 $\mathbf{D}^t$、相机外参 $\mathbf{P}^t = [\mathbf{R}^t | \mathbf{T}^t]$ 和内参 $\mathbf{K}^t$。全局点云通过重参数化表示：

$$\mathbf{X}^t = \pi^{-1}(\mathbf{D}^t, \mathbf{K}^t, \mathbf{P}^t)$$

优化目标整合三类损失函数（Equation 7）：

- **对齐损失** $\mathcal{L}_{\mathrm{align}}$：继承自 DUSt3R，将逐对点云估计对齐到全局坐标系，使用单一边缘刚体变换 $\sigma^e \mathbf{P}^{t;e}$。
- **相机轨迹平滑损失** $\mathcal{L}_{\mathrm{smooth}}$：惩罚连续帧间旋转与平移的剧烈变化：

$$\mathcal{L}_{\mathrm{smooth}} = \sum_{t=0}^{N} \left( \| \mathbf{R}^{t^\top} \mathbf{R}^{t+1} - I \|_{\mathrm{f}} + \| \mathbf{T}^{t+1} - \mathbf{T}^t \|_2 \right)$$

- **光流投影损失** $\mathcal{L}_{\mathrm{flow}}$：约束估计深度与相机运动在静态区域的光流一致性。

消融实验表明，$\mathcal{L}_{\mathrm{smooth}}$ 和 $\mathcal{L}_{\mathrm{flow}}$ 的权重均设为 $w=0.01$ 时鲁棒性最佳；过高的平滑权重反而将 ATE 从 0.108 提升至 0.138（Table A2）。光流损失仅在平均误差低于 20 时启用，且在优化过程中动态更新运动掩码（每像素光流损失 > 50 时标记为动态），以自适应处理复杂运动场景。

## 实验与分析

### 核心实验结果

MonST3R 在视频深度估计、相机姿态估计和单帧深度估计三个任务上均取得具有竞争力的结果，尤其在动态场景中展现出显著优势。

**视频深度估计。** 在 Sintel 数据集上，MonST3R 在仅尺度对齐（scale-only）设置下取得 Abs Rel 0.345，大幅领先专用视频深度方法 **DepthCrafter**（Hu et al., 2024）的 0.692，相对提升约 50%（Table 2）。在尺度-偏移对齐（scale-and-shift）设置下，MonST3R 同样保持竞争力。在 Bonn 和 KITTI 数据集上的定性结果（Figure A1、A2）显示，MonST3R 能够更准确地恢复运动前景物体的深度结构，而 DepthCrafter 倾向于将前景物体错误地推至背景。

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/005_Table_2.jpg]]
*Table 2: Video depth evaluation on Sintel, Bonn, and KITTI datasets. We evaluate for both scaleand-shift-invariant and scale-invariant depth. The best and second best results in each category are bold and underlined, respectively*

**相机姿态估计。** 在 Sintel 动态场景上，MonST3R 取得 ATE 0.108，优于 DUSt3R 的 0.141 和联合深度-姿态方法 **CasualSAM**（Zhang et al., ECCV 2022）的 0.183（Table 4）。在静态场景 ScanNet 上，MonST3R 的 ATE 为 0.068，甚至优于 **LEAP-VO**（Chen et al., 2024）的 0.078 和原始 DUSt3R 的 0.081，表明全局优化中的平滑损失和光流一致性损失对静态场景同样有益。在 TUM-dynamic 数据集上，MonST3R 也保持竞争力。值得注意的是，MonST3R 在未使用真实相机内参的情况下取得这些结果，而部分基线方法依赖真实内参。

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/007_Table_4.jpg]]
*Table 4: Evaluation on camera pose estimation on the Sintel, TUM-dynamic, and ScanNet. The best and second best results are bold and underlined, respectively. MonST3R achieves competitive and even better results than pose-specific methods, even without ground truth camera intrinsics*

**单帧深度估计。** 尽管在动态视频数据上微调，MonST3R 在单帧深度估计任务上仍保持与 DUSt3R 相当的性能。在 Bonn 数据集上，MonST3R 的 Abs Rel 为 0.076，优于 DUSt3R 的 0.141（Table 3）；在 KITTI 和 NYU-v2 上分别为 0.101 和 0.091，与 DUSt3R 基本持平。这表明动态场景微调并未损害模型在静态场景上的泛化能力。

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/006_Table_3.jpg]]
*Table 3: Single-frame depth evaluation. We report the performance on Sintel, Bonn, KITTI, and NYU-v2 (static) datasets. MonST3R achieves overall comparable results to DUSt3R*

### 消融实验

Table 5 系统分析了训练数据、微调策略和损失函数对性能的影响，所有消融均在 Sintel 数据集上进行。

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/009_Table_5.jpg]]
*Table 5: Ablation study on Sintel dataset. For each category, the default setting is underlined, and the best performance is bold*

**训练数据贡献。** 未微调的 DUSt3R 在 Sintel 上 ATE 高达 0.354，而使用全部四个动态数据集（PointOdyssey、TartanAir、Spring、Waymo）微调后降至 0.108。单独使用任一数据集均不如混合使用：仅用 PointOdyssey 时 ATE 为 0.174，仅用 TartanAir 时为 0.135。这验证了多源动态数据混合训练的必要性。

**微调策略。** 仅微调解码器和预测头部（冻结编码器）取得最佳 ATE 0.108，优于全模型微调的 0.118。这一反直觉的结果表明，ViT 编码器从静态预训练中习得的视觉表征已足够通用，过度调整反而引入过拟合风险。微调编码器+解码器的 ATE 为 0.119，进一步支持仅微调末端的策略。

**损失函数消融。** 在基础对齐损失之上添加相机轨迹平滑损失（$\mathcal{L}_{\text{smooth}}$）和光流投影损失（$\mathcal{L}_{\text{flow}}$）将 ATE 从 0.136 降至 0.108，而视频深度 Abs Rel 仅从 0.342 微升至 0.345，表明这些损失以极小深度代价显著提升姿态估计。单独移除光流损失导致 ATE 升至 0.117，移除平滑损失升至 0.112，验证了两者的互补性。

**损失权重敏感性。** Table A2 显示，平滑损失权重 $w_{\text{smooth}}=0.01$ 时鲁棒性最佳；当权重增至 0.1 时 ATE 升至 0.138，说明过强的平滑约束会损害姿态估计精度。光流损失权重 $w_{\text{flow}}=0.01$ 为默认设置，权重降至 0.001 时 ATE 升至 0.112。

**窗口与步幅。** Table A1 探索了训练/推理窗口大小和步幅的影响。密集窗口 7（步幅 1）取得 ATE 0.136，而步幅 2 的窗口 7 在降低 33% 内存消耗的同时仅使 ATE 微升至 0.140，是实用的效率-精度权衡点。过小的窗口（如窗口 4）导致 ATE 升至 0.163，表明足够的时序上下文对姿态估计至关重要。

### 动态物体处理的关键发现

实验揭示了一个反直觉的结论：在推理时显式掩码排除动态物体反而会降低姿态估计性能（Sec. 4.3）。这是因为动态物体上的点云预测虽然存在误差，但仍提供了有用的几何约束信息。MonST3R 的策略是在全局优化中通过置信度掩码和静态区域推断隐式处理动态物体，而非粗暴排除，从而保留了更多有效信息。

### 失败模式与局限性

尽管整体性能优异，MonST3R 在以下场景存在局限：

1. **长时遮挡。** 小滑动窗口的全局对齐策略在长时遮挡场景下容易漂移，因为窗口间缺乏有效的跨窗口约束。
2. **动态内参。** 处理可变相机内参时需谨慎调整超参数或施加手动约束，否则优化容易不稳定。
3. **分布外场景。** 在开阔田野等训练数据中罕见的场景，模型估计质量下降，反映了动态视频训练数据覆盖范围的局限。

### 补充图表

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/001_Figure.jpg]]

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/010_Figure.jpg]]
*Figure: Input Frames GT Depth DepthCrafter MonST3R (Ours) Figure A1: Video depth estimation comparison on Bonn dataset. Evaluation protocol is persequence scale & shift. We visualize the prediction result after alignment. Note, in the first row, our depth estimation is more aligned with the GT depth (e.g., the wall) compared to DepthCrafter’s*

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/012_Figure.jpg]]
*Figure: LEAP -VO CasualSAM MonST3R (Ours)*

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/013_Figure.jpg]]
*Figure: A3: Camera pose estimation comparison on the Sintel dataset. The trajectories are plotted along the two axes with the highest variance to capture the most significant motion. The predicted trajectory (solid blue line) is aligned to match the ground truth trajectory (dashed gray line). Our MonST3R is more robust at challenging scenes, “temple 3” and “cave 2” (the last two rows). LEAP-VO CasualSAM MonST3R (Ours) Figure A4: Camera pose estimation comparison on the Scannet dataset. The trajectories are plotted along the two axes with the highest variance to capture the most significant motion*

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/003_Table_1.jpg]]
*Table 1: Training datasets used fine-tuning on dynamic scenes. All datasets provide both camera pose and depth, and most of them include dynamic objects*

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/017_Table.jpg]]
*Table: A1: Ablation study on different training/inference window sizes on the Sintel dataset. Each cell displays two values: ATE ↓ / Abs \mathbf { R e l } \downarrow , , corresponding to camera pose and video depth estimation, respectively. The cells where the inference window size exceeds the training window size are highlighted in grey. The default setup is underlined, and the best results are in bold. GPU memory consumption for each inference setup is listed in the leftmost column*

![[assets/figures/papers/paper_list_l2_MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Mot/figures/018_Table.jpg]]
*Table: A2: Ablation study on loss weight sensitivity. The table shows the effect of varying the loss weights w _ { \mathrm { s m o o t h } } and { w } _ { \mathrm { f l o w } } on camera pose and video depth estimation. The default setup is underlined, and the best results are in bold*

## 方法谱系与知识库定位

### 静态几何估计方法的动态扩展

MonST3R 的核心定位是对 DUSt3R（Wang et al., 2024c）的“动态泛化”。DUSt3R 开创性地将成对图像映射为统一坐标系下的点云图（pointmap），但其训练数据仅包含静态场景，导致在动态场景中出现两种系统性失效（Figure 2）：（1）将运动前景对齐后，背景点云发生错位；（2）无法估计运动前景的深度，将其错误地放置在背景之后。MonST3R 的根本突破在于认识到**点云图可以按时间步独立定义，且在同一相机坐标系下表示对动态场景仍具有概念合理性**。这一洞察使得仅需在有限的动态、有姿态、有深度标签的视频数据集上微调，即可将 DUSt3R 的静态几何估计能力迁移至动态场景，无需显式建模物体运动或光流。

### 与视频深度估计方法的对比

在视频深度估计任务上，MonST3R 与专用方法 DepthCrafter（Hu et al., 2024）形成直接竞争。DepthCrafter 专门针对视频深度估计设计，而 MonST3R 以统一的点云图表示同时处理深度和相机姿态。在 Sintel 数据集上，仅使用尺度对齐（scale-only）时，MonST3R 的 Abs Rel 达到 0.345，大幅优于 DepthCrafter 的 0.692（Table 2）。这一优势源于 MonST3R 的逐帧点云图表示能够隐式捕捉动态场景的几何结构，而无需依赖显式的时序建模或测试时优化。值得注意的是，即使在 Bonn 和 KITTI 等数据集上使用尺度-偏移对齐（scale-and-shift），MonST3R 仍保持竞争力，表明其几何估计的鲁棒性不依赖于特定的后处理协议。

### 与联合深度与姿态估计方法的对比

在联合深度与相机姿态估计领域，MonST3R 与 CasualSAM（Zhang et al., ECCV 2022）和 Robust-CVD（Kopf et al., 2021）等方法存在根本性差异。CasualSAM 依赖昂贵的测试时优化，在推理阶段需要大量计算资源；而 MonST3R 以**前馈方式为主**，仅在轻量级全局优化阶段（约 1 分钟）进行多帧对齐。这种设计使得 MonST3R 在效率上具有显著优势，同时在精度上达到甚至超越专用方法：在 Sintel 数据集上，MonST3R 的相机姿态估计 ATE 达到 0.108，优于 DUSt3R 的 0.141；在 ScanNet 静态场景上，ATE 达到 0.068，超越基于学习的视觉里程计方法 LEAP-VO（Chen et al., 2024）的 0.078（Table 4）。

### 动态场景处理的独特机制

MonST3R 的动态处理策略与现有方法形成鲜明对比。传统方法通常试图显式检测和掩码动态物体，但 MonST3R 的实验表明，**在推理阶段掩码动态物体反而会降低姿态估计性能**（Section 4.3）。相反，MonST3R 采用“隐式学习 + 静态区域推断”的策略：通过微调使模型在动态数据上学会区分静态与动态区域，然后在全局优化阶段利用置信度掩码和静态区域推断（Equation 2-3）来排除动态物体的干扰。具体而言，通过比较相机运动诱导的光流 $\mathbf{F}_{\mathrm{cam}}^{t t'}$ 与现成光流方法估计的光流 $\mathbf{F}_{\mathrm{est}}^{t t'}$，当 L1 差异小于阈值 $\alpha$ 时标记为静态区域 $\mathbf{S}^{t t'}$。这种设计使得动态物体自然地从姿态优化中排除，同时保留其对深度估计的贡献。

### 适用边界与局限

MonST3R 的适用边界主要由以下几个因素定义：

**训练数据分布约束**：MonST3R 在四个动态/静态视频数据集（PointOdyssey, TartanAir, Spring, Waymo）上微调，这些数据集均提供相机姿态和深度标签（Table 1）。对于与训练分布显著不同的场景（如开阔田野），模型可能表现出性能下降。消融实验证实，混合使用全部四个数据集将 ATE 从单数据集的 0.174 提升至 0.108（Table 5），表明数据多样性对泛化能力至关重要。

**动态内参的处理挑战**：当相机内参在视频中动态变化时，需要仔细的超参数调优或手动约束。这是全局优化框架的内在限制，因为内参优化与深度、姿态优化存在耦合。

**长时序遮挡的脆弱性**：全局对齐采用滑动窗口策略，虽然降低了计算量（窗口大小为 7 时内存降低 33%，ATE 仅从 0.136 变为 0.140，见 Table A1），但在长时序遮挡场景下，小窗口可能无法建立足够的跨帧约束，导致轨迹漂移。

**对现成光流方法的依赖**：静态掩码推断依赖现成的光流方法（Wang et al., 2024d）作为中间表示。虽然该方法在实验中表现良好，但 MonST3R 未针对特定光流模型调优，在光流估计失败的情况下，静态掩码的质量可能受到影响。

### 开放问题与未来方向

1. **动态相机内参的鲁棒处理**：当前全局优化框架对动态内参的敏感性需要更系统的解决方案，可能涉及内参先验的引入或解耦优化策略。

2. **长视频的全局一致性**：滑动窗口策略在计算效率与长程一致性之间存在权衡，如何在不显著增加计算成本的前提下建立更长的时序依赖是一个开放问题。

3. **训练数据规模的扩展**：尽管 MonST3R 证明了小规模动态数据微调的有效性，但更大规模、更多样化的动态视频数据可能进一步释放模型潜力，特别是在处理极端运动或复杂遮挡场景时。

4. **动态物体的显式建模**：当前方法隐式处理动态物体，未来工作可能探索将显式的物体运动估计与场景几何估计相结合，以同时输出场景流或物体轨迹。

5. **与生成式模型的结合**：MonST3R 的逐帧点云图表示为视频生成、新视角合成等任务提供了几何先验，探索其在生成式模型中的应用是一个有前景的方向。

## 原文 PDF

![[paperPDFs/ICLR_2025/MonST3R_A_Simple_Approach_for_Estimating_Geometry_in_the_Presence_of_Motion.pdf]]
