---
title: "Mono4DGS-HDR: High Dynamic Range 4D Gaussian Splatting from Alternating-exposure Monocular Videos"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Mono4DGS_HDR_High_Dynamic_Range_4D_Gaussian_Splatting_from_Alternating_exposure_8634b557c5bd.pdf
project_link: "https://liujf1226.github.io/Mono4DGS-HDR"
code_link: null
aliases:
- MH
- Mono4DGS-HDR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过正交空间视频高斯表示消除对相机位姿的依赖，获得一致的 HDR 训练视频初始化，从而提供稳定的位姿优化和场景重建基础
primary_logic: 两阶段优化：首先在无位姿正交相机空间学习动态 HDR 视频高斯，然后利用 2D 协方差不变性将其转换为世界空间高斯，同时引入时序亮度正则化（TLR）将良好监督时刻的外观传播到弱监督时刻，保证 HDR 时域一致性
claims:
- 去除视频高斯初始化导致 PSNR 下降超过 1dB
- 去除时序亮度正则化（TLR）使 HDR-TAE 大幅恶化
- HDR 光度重投影损失为相机位姿和场景几何提供密集监督，去除后 PSNR 下降
- Syn-Exp-3 (synthetic, 3 exposures, test frames) 上 HDR PSNR↑ = 37.64
---

# Mono4DGS-HDR: High Dynamic Range 4D Gaussian Splatting from Alternating-exposure Monocular Videos

> [!tip] 核心洞察
> 两阶段优化：首先在无位姿正交相机空间学习动态 HDR 视频高斯，然后利用 2D 协方差不变性将其转换为世界空间高斯，同时引入时序亮度正则化（TLR）将良好监督时刻的外观传播到弱监督时刻，保证 HDR 时域一致性

| 字段 | 内容 |
|------|------|
| 中文题名 | Mono4DGS-HDR: 基于交替曝光单目视频的高动态范围 4D 高斯溅射 |
| 英文题名 | Mono4DGS-HDR: High Dynamic Range 4D Gaussian Splatting from Alternating-exposure Monocular Videos |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=9ZrjgzlAuh) · [Project](https://liujf1226.github.io/Mono4DGS-HDR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Mono4DGS-HDR |
| Dataset | Syn-Exp-3, Real-Exp-2, Real-Exp-3 |

> [!tip] 效果简介
> - Syn-Exp-3 (synthetic, 3 exposures, test frames) 上，HDR PSNR↑ 37.64 vs 36.89 (MoSca-HDR) (+0.75)。
> - Syn-Exp-3 (test frames) 上，HDR TAE↓ 0.057 vs 0.059 (MoSca-HDR) (-0.002)。
> - Real-Exp-2 (real, 2 exposures, train frames) 上，HDR-TAE↓ 0.046 vs 0.054 (MoSca-HDR) (-0.008)。

## 概要

从单目视频中重建动态场景（4D 重建）是计算机视觉的核心挑战之一。当输入视频由**交替曝光**的 LDR 帧组成时，问题进一步复杂化：帧间亮度不一致使得标准光度重投影误差无法用于相机位姿优化，同时缺乏直接的 HDR 监督导致恢复的 HDR 外观在时域上不稳定。Mono4DGS-HDR 针对这一瓶颈，提出了一种**两阶段高斯溅射优化框架**，无需已知相机位姿即可从交替曝光单目视频中重建高质量的 4D HDR 场景。

**核心思路**：在第一阶段，于正交相机坐标空间中训练动态 HDR **视频高斯**（Video Gaussian），消除对相机位姿的依赖，获得亮度一致的 HDR 训练视频初始化；第二阶段通过**视频-世界高斯变换**（含动态/静态分离与基于 2D 协方差不变性的缩放重拟合）将视频高斯转换为世界空间高斯，并联合优化相机位姿与场景表示。同时引入**时序亮度正则化**（TLR）和 **HDR 光度重投影损失**，分别保证 HDR 外观的时域一致性和为位姿优化提供密集监督。

**主要结果**：在合成数据集 Syn-Exp-3 上，HDR PSNR 达到 37.64 dB，较最优基线 MoSca-HDR 提升 0.75 dB；在真实数据集 Real-Exp-3 上，LDR 观测曝光 PSNR 达到 27.65 dB（+0.42 dB），HDR 时域一致性指标 HDR-TAE 在真实场景中降至 0.046（-0.008）。消融实验证实：去除视频高斯初始化使 PSNR 下降超过 1 dB，去除 TLR 导致 HDR-TAE 大幅恶化，去除 HDR 光度重投影损失同样造成性能显著下降。

**方法定位**：Mono4DGS-HDR 属于无位姿单目 4D HDR 重建方法，区别于需要已知位姿的静态 HDR 方法 **GaussHDR**（Liu et al., 2025a）和多相机动态 HDR 方法 **HDR-HexPlane**（Wu et al., 2024a）。与 **MoSca-HDR**（Lei et al., 2025）、**SplineGS-HDR**（Park et al., 2025）、**GFlow-HDR**（Wang et al., 2025b）等无位姿方法的 HDR 扩展相比，其关键差异在于用视频高斯初始化替代传统的轨迹/深度提升初始化，并引入了 TLR 与 HDR 光度重投影损失来解决交替曝光带来的独特挑战。

### 问题背景：从交替曝光单目视频重建 4D HDR 场景

高动态范围（HDR）场景重建旨在恢复场景的真实辐照度分布，超越普通低动态范围（LDR）成像有限的亮度捕捉能力。当场景同时包含动态内容——即 4D HDR 重建——且输入仅为**单目视频**时，问题变得尤为困难。更进一步，若该单目视频采用**交替曝光**（alternating exposures）策略拍摄——即相邻帧的曝光时间不同——则引入了帧间亮度剧烈波动的额外挑战。

交替曝光在消费级设备中广泛用于扩大动态范围，但它给 4D 重建带来了两个核心障碍：

1. **相机位姿估计失效**：标准的位姿优化依赖光度重投影误差，即假设同一 3D 点在相邻帧中的亮度一致。交替曝光打破了这一假设——同一场景点在相邻帧中因曝光时间不同而呈现截然不同的像素值，使得光度一致性约束不再成立，导致位姿估计不可靠甚至发散。

2. **HDR 外观时域不一致**：由于缺乏直接的 HDR 监督信号（输入仅为 LDR 帧），模型需要在不同曝光帧之间推断 HDR 辐照度。交替曝光意味着某些时刻的像素仅由短曝光（欠曝）或长曝光（过曝）帧监督，监督强度在时域上极不均匀，容易导致恢复的 HDR 外观随时间抖动或漂移。

### 现有方法缺口

现有工作可大致分为以下几类，但均无法有效应对上述挑战：

- **静态 HDR 新视角合成方法**（如 **GaussHDR**，Liu et al., 2025a）：假设场景静止、相机位姿已知，无法处理动态内容，且依赖精确的相机参数输入。
- **动态 HDR 新视角合成方法**（如 **HDR-HexPlane**，Wu et al., 2024a）：支持动态场景，但需要多相机设置提供已知位姿，不适用于无位姿单目视频。
- **无位姿单目 4D 重建方法**（如 **SplineGS**，Park et al., 2025；**MoSca**，Lei et al., 2025；**GFlow**，Wang et al., 2025b）：能够从单目视频联合优化相机位姿和动态场景表示，但其设计针对 LDR 输入。若简单扩展至 HDR 模式（添加色调映射 MLP），它们仍面临交替曝光导致的位姿优化失败和 HDR 时域不一致问题。如 Figure 1(b) 所示，这些扩展版本的重建质量显著低于本文方法。

### 核心瓶颈与本文动机

综上，该问题的**真实瓶颈**在于：交替曝光导致帧间亮度不一致，使得无法通过标准光度重投影误差优化相机位姿；同时缺失直接 HDR 监督，导致恢复的 HDR 外观随时间不稳定。

本文的核心洞察是：**若能在不依赖相机位姿的前提下，首先获得一个亮度一致、时域稳定的 HDR 视频初始化，则可反过来为相机位姿和场景几何提供可靠的监督信号，从而打通“位姿-场景”联合优化的闭环。**

基于此，本文提出 **Mono4DGS-HDR**，一种基于高斯溅射（Gaussian Splatting）的两阶段优化方法，通过正交空间视频高斯表示解除对相机位姿的依赖，并引入时序亮度正则化（TLR）保证 HDR 时域一致性，最终实现从交替曝光单目视频的高质量 4D HDR 重建。

## 核心方法与创新机理

Mono4DGS-HDR 的核心创新在于通过**两阶段高斯优化**破解了交替曝光单目视频 4D HDR 重建的两个根本瓶颈：**帧间亮度不一致导致相机位姿无法估计**，以及**缺失直接 HDR 监督导致时域外观不稳定**。其关键洞察是：先在无位姿的正交相机空间学习动态 HDR 视频高斯，获得一致的 HDR 训练视频初始化，再将其转换为世界空间高斯，为位姿优化和场景重建提供稳定基础。

### 方法谱系与知识库定位

本文处于**无位姿单目动态场景重建**与**HDR 新视角合成**的交叉点。基线方法可分为两类：（1）静态 HDR 方法如 **GaussHDR**（Liu et al., 2025a），依赖已知相机位姿，无法直接处理无位姿单目视频；（2）动态 HDR 方法如 **HDR-HexPlane**（Wu et al., 2024a），需要多相机设置。将无位姿单目 4D 重建方法——**SplineGS**（Park et al., 2025）、**MoSca**（Lei et al., 2025）、**GFlow**（Wang et al., 2025b）——直接扩展至 HDR 模式（添加色调映射 MLP）后，由于缺乏对交替曝光和时域一致性的专门处理，重建质量显著低于本文方法（Figure 1b）。

### 关键改进槽位（Changed Slots）

#### 槽位一：场景初始化方式

**基线做法**：基于轨迹/深度提升（track/depth lifting）直接初始化世界空间高斯，在交替曝光条件下缺乏可靠的几何与外观先验。

**本文创新**：第一阶段在正交相机坐标空间训练**视频高斯**（Video Gaussian），为第二阶段提供位置、旋转、缩放、不透明度与颜色的强先验。这一设计消除了对相机位姿的依赖，使 HDR 训练视频能够在亮度一致的条件下恢复。

**因果机制**：交替曝光导致标准光度重投影误差不可用，相机位姿无法通过常规方式优化。视频高斯在无位姿空间中学习，绕过了这一死锁，为后续世界空间优化提供了“干净”的初始化。消融实验（Table 3a）表明，去除视频高斯初始化使 PSNR 下降超过 1dB，验证了该槽位的决定性作用。

#### 槽位二：高斯变换与缩放初始化

**基线做法**：无专门变换策略，直接继承缩放参数。

**本文创新**：设计了**视频-世界高斯变换策略**（Figure 3a），包含三个关键子模块：
1. **遮挡感知的动态/静态分离**：利用动态掩码和深度信息，统计每个视频高斯在动态区域且未被遮挡的帧次数 $N_d$（Eq. 1），将 $N_d$ 超过阈值的归为动态高斯，其余归为静态高斯。去除遮挡处理（Table 3b）使 HDR PSNR 下降约 0.3dB，且动态/静态分离不准确（Figure 3c）。
2. **位置与旋转变换**：利用光束平差获得的初始相机参数，将视频高斯变换到世界空间。
3. **基于 2D 协方差不变性的缩放重拟合**：核心洞察是视频高斯与世界高斯在图像平面上的 2D 协方差应保持一致。通过最小化二者 2D 协方差矩阵的 L2 差异（Eq. 2），重新拟合世界高斯的缩放参数，避免直接继承缩放导致的不合理尺度（Figure 3d）。消融实验（Table 3c）证实去除该机制使性能下降。

#### 槽位三：时序一致性正则化

**基线做法**：无专门处理，导致恢复的 HDR 外观随时间不稳定。

**本文创新**：提出**时序亮度正则化（TLR）**，利用光流将相邻帧的 HDR 渲染对齐，约束逐像素 HDR 辐照度的一致性（Eq. 3）：

$$\mathcal{L}_{\mathrm{tlr}} = \Big| V_{t\,t-1} \odot \frac{\widetilde{H}_{t-1\,t} - \widetilde{H}_t}{\widetilde{H}_{t-1\,t} + \widetilde{H}_t} \Big|_1$$

其中分子通过归一化消除辐照度绝对尺度的影响，使正则化聚焦于相对亮度变化。

**因果机制**：交替曝光意味着某些时刻的 HDR 外观受到强监督（曝光良好的帧），而其他时刻监督较弱。TLR 将强监督时刻学习到的动态内容传播到弱监督时刻，确保 HDR 外观的时域一致性（Figure 4）。消融实验（Table 3e）表明，去除 TLR 使 HDR-TAE 大幅恶化，时域一致性显著降低。

#### 槽位四：相机位姿与场景联合优化

**基线做法**：交替曝光使标准光度重投影误差不可用，无法有效优化相机位姿。

**本文创新**：利用第一阶段恢复的 HDR 训练视频，计算**HDR 光度重投影损失**，在第二阶段联合优化相机位姿与世界高斯。该损失为相机位姿和场景几何提供了密集的 HDR 域监督，突破了交替曝光对位姿估计的限制。消融实验（Table 3d）表明，去除该损失使 HDR PSNR 和 TAE 均恶化。

### 创新总结

Mono4DGS-HDR 的四个改进槽位构成了一条完整的因果链：**视频高斯初始化**（槽位一）在无位姿空间中恢复一致的 HDR 视频 → **高斯变换与缩放重拟合**（槽位二）将其转换为高质量的世界空间初始化 → **HDR 光度重投影损失**（槽位四）使相机位姿得以在 HDR 域中优化 → **时序亮度正则化**（槽位三）保证 HDR 外观的时域稳定性。这一链条的核心驱动力在于：通过解耦位姿估计与 HDR 外观学习，将交替曝光的“障碍”转化为“约束”，实现了从单目交替曝光视频到 4D HDR 场景的端到端重建。

Mono4DGS-HDR 采用**两阶段高斯优化范式**，核心思路是将相机位姿估计与 HDR 场景重建解耦，从而规避交替曝光视频中帧间亮度不一致对位姿优化的致命干扰。整体流程如图 2 所示，可概括为三个关键环节：

**（1）2D 先验提取**  
输入交替曝光单目 LDR 视频，首先利用现成的视觉基础模型提取逐帧深度、轨迹、光流及动态掩码。这些 2D 先验为后续阶段提供场景初始化线索和正则化约束，但其质量直接影响最终重建精度——在无纹理区域或快速运动场景中，光流和深度的不准确会成为瓶颈。

**（2）第一阶段：视频高斯训练（Video Gaussian Training）**  
在正交相机坐标空间训练全动态 HDR 视频高斯。由于正交投影消除了对相机位姿的依赖，系统可以在没有位姿先验的情况下直接学习一致亮度的 HDR 视频表示。这一阶段的关键产出是：位置、旋转、缩放、不透明度及颜色的先验，为第二阶段提供强初始化。消融实验表明，去除视频高斯初始化会导致 PSNR 下降超过 1dB（Table 3a），验证了该阶段对整体性能的决定性贡献。

**（3）第二阶段：世界高斯精修（World Gaussian Refinement）**  
通过**视频-世界高斯变换**（Video-to-World Gaussian Transformation）将第一阶段的高斯从正交空间转换到世界空间，包含三个子步骤：
- **动态/静态识别与遮挡处理**：利用动态掩码和深度信息统计每个高斯在动态区域且未被遮挡的帧次数 $N_d$（Eq. 1），据此分类动态与静态高斯；去除遮挡处理会使 HDR PSNR 下降约 0.3dB（Table 3b）。
- **属性变换与缩放重拟合**：将高斯位置和旋转通过初始相机参数变换到世界空间，并利用 **2D 协方差不变性**重新拟合缩放（Eq. 2），确保变换后的世界高斯与视频高斯在图像平面保持视觉一致。直接继承缩放而不做重拟合会导致 PSNR 下降（Table 3c）。
- **联合优化**：在世界空间联合优化静态与动态高斯及相机参数，损失函数（Eq. 整体损失）整合了 RGB 损失、深度损失、轨迹损失、ARAP 运动正则化、速度/加速度平滑、**时序亮度正则化（TLR）** 和 **HDR 光度重投影损失**。其中 TLR（Eq. 3）利用光流对齐相邻帧的逐像素 HDR 辐照度，将良好监督时刻的动态外观传播到弱监督时刻，是保障时域一致性的核心机制——去除 TLR 会导致 HDR-TAE 大幅恶化（Table 3e, Figure 6）。HDR 光度重投影损失则基于第一阶段恢复的 HDR 视频为相机位姿和场景几何提供密集监督，去除后 PSNR 同样下降（Table 3d）。

整个 pipeline 的因果链路可归纳为：**正交空间视频高斯消除位姿依赖 → 获得一致 HDR 训练视频 → 视频-世界变换提供强初始化 → TLR 与 HDR 重投影损失协同保障时域稳定与位姿精度**。这一设计使 Mono4DGS-HDR 在无需已知位姿的条件下，从交替曝光单目视频中重建出高质量的 4D HDR 场景。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_9ZrjgzlAuh/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Mono4DGS-HDR. (a) We infer vision foundation models on the input alternating-exposure video to extract 2D priors, which provide scene initialization and regularization. (b) We propose a novel two-stage Gaussian optimization procedure, which includes video Gaussian training in the first stage, world Gaussian fine-tuning in the second stage, and a videoto-world Gaussian transformation strategy. The HDR Gaussians are optimized through 2D prior supervision, Gaussian motion regularization, temporal luminance regularization and HDR photometric reprojection loss*

Mono4DGS-HDR 的核心架构围绕两阶段高斯优化展开，包含五个关键模块：2D 先验提取、视频高斯训练（第一阶段）、视频-世界高斯变换、世界高斯精炼（第二阶段）以及时序亮度正则化。以下逐一剖析各模块的设计逻辑与关键公式。

### 2D 先验提取

系统首先利用现成的视觉基础模型从交替曝光输入视频中提取四类 2D 先验，为后续场景初始化和正则化提供约束：

- **深度图**：通过单目深度估计模型获取每帧的深度先验 `\widetilde{D}_t`。
- **轨迹**：利用点跟踪模型获取跨帧的 2D 轨迹对应关系。
- **光流**：计算相邻帧间的光流 `V_{t, t-1}`，用于时序对齐。
- **动态掩码**：基于极线误差图生成动态区域掩码 `M_t`，标记运动像素。

这些先验的质量直接影响最终重建效果——消融实验表明，去除深度损失或光流/轨迹损失会导致 PSNR 显著下降（Table 8）。

### 视频高斯训练（第一阶段）

第一阶段的核心思想是**在正交相机坐标空间训练全动态 HDR 视频高斯**，从而消除对相机位姿的依赖。这一设计直击交替曝光场景的根本瓶颈：帧间亮度不一致使得标准光度重投影误差无法用于位姿优化。通过在无位姿的正交空间中获得一致的 HDR 训练视频，系统为后续的位姿优化和场景重建提供了稳定初始化。

每个视频高斯由位置 `(x^v, y^v, z^v)`、旋转 `R^v`、缩放 `S^v`、不透明度 `α^v` 和颜色 `c^v` 参数化。HDR 颜色通过色调映射 MLP 与对数曝光值 `e_t` 耦合，将 HDR 辐照度映射为 LDR 像素值以匹配输入帧。消融实验证实，去除视频高斯初始化使 PSNR 下降超过 1dB（Table 3a），验证了该阶段的关键作用。

### 视频-世界高斯变换

该模块将第一阶段训练的视频高斯转换为世界空间中的静态/动态高斯初始化，包含三个子步骤：

**1. 动态/静态识别与遮挡处理**

将每个视频高斯的轨迹投影到图像平面，统计其落入动态区域且未被遮挡的帧次数 `N_d`：

$$N_d = \sum_{t=1}^{N_f} \mathcal{Z}[M_t(x_t^v, y_t^v) \cdot (1 - o_t) = 1], \quad o_t = \mathcal{Z}[z_t^v > \widetilde{D}_t(x_t^v, y_t^v)]$$

其中 `\mathcal{Z}[\cdot]` 为指示函数，`o_t` 通过比较高斯深度 `z_t^v` 与深度先验 `\widetilde{D}_t` 判断遮挡。若 `N_d` 超过阈值，该高斯被分类为动态；否则为静态。去除遮挡处理会导致动态/静态分离不准确（Figure 3c），HDR PSNR 下降约 0.3dB（Table 3b）。

**2. 位置与旋转变换**

利用光束平差得到的初始相机内参 `\hat{K}` 和外参 `\{[\hat{R}_t|\hat{T}_t]\}`，将视频高斯变换到世界空间：

- 静态高斯：通过首帧相机位姿直接变换。
- 动态高斯：对轨迹的每个控制点应用对应时刻的相机变换。

颜色与不透明度直接继承，无需重新学习。

**3. 基于 2D 协方差不变性的缩放重拟合**

直接继承视频高斯的缩放会导致世界高斯尺度不合理（Figure 3d）。为此，利用投影后 2D 协方差应保持一致的约束，通过优化问题重新拟合缩放：

$$\Sigma_t^{\prime v} = [J_{\mathrm{ortho}} W_t^v R_t^v S^v (J_{\mathrm{ortho}} W_t^v R_t^v S^v)^\top]_{2\times2}$$

$$\Sigma_t^{\prime w} = [J W_t^w R_t^w S^w (J W_t^w R_t^w S^w)^\top]_{2\times2}$$

最小化 `\sum_{t=1}^{N_f} ||\Sigma_t^{\prime v} - \Sigma_t^{\prime w}||_2` 求解世界高斯缩放 `S^w`，确保变换前后在图像平面上的视觉外观一致。去除该步骤导致 HDR PSNR 下降（Table 3c）。

### 世界高斯精炼（第二阶段）

第二阶段联合优化静态与动态世界高斯及相机参数，损失函数为多项加权组合：

$$\mathcal{L} = \lambda_{\mathrm{rgb}} \mathcal{L}_{\mathrm{rgb}} + \lambda_{\mathrm{ue}} \mathcal{L}_{\mathrm{ue}} + \lambda_{\mathrm{dep}} \mathcal{L}_{\mathrm{dep}} + \lambda_{\mathrm{track}} \mathcal{L}_{\mathrm{track}} + \lambda_{\mathrm{arap}} \mathcal{L}_{\mathrm{arap}} + \lambda_{\mathrm{vel}} \mathcal{L}_{\mathrm{vel}} + \lambda_{\mathrm{acc}} \mathcal{L}_{\mathrm{acc}} + \lambda_{\mathrm{tlr}} \mathcal{L}_{\mathrm{tlr}} + \lambda_{\mathrm{pr}} \mathcal{L}_{\mathrm{pr}}$$

其中各损失项的作用：

- **`\mathcal{L}_{\mathrm{rgb}}`**：结合 DSSIM 与 L1 损失的 LDR RGB 损失，约束渲染图像与输入帧一致。
- **`\mathcal{L}_{\mathrm{ue}}`**：单位曝光损失 `||\phi(0) - C_0||_2^2`，将零对数曝光映射到已知参考颜色 `C_0`，固定 HDR 辐照度尺度。
- **`\mathcal{L}_{\mathrm{dep}}`、`\mathcal{L}_{\mathrm{track}}`**：深度与轨迹先验监督，约束场景几何。
- **`\mathcal{L}_{\mathrm{arap}}`、`\mathcal{L}_{\mathrm{vel}}`、`\mathcal{L}_{\mathrm{acc}}`**：ARAP 刚性正则化、速度与加速度平滑约束，规范动态高斯运动。
- **`\mathcal{L}_{\mathrm{tlr}}`**：时序亮度正则化（见下文）。
- **`\mathcal{L}_{\mathrm{pr}}`**：HDR 光度重投影损失，利用第一阶段恢复的 HDR 视频为相机位姿和场景几何提供密集监督。去除该损失使 PSNR 和 TAE 恶化（Table 3d）。

### 时序亮度正则化（TLR）

TLR 是保证 HDR 时域一致性的关键创新。其核心机制是利用光流将相邻帧的 HDR 渲染对齐，约束逐像素 HDR 辐照度在时域上保持稳定：

$$\mathcal{L}_{\mathrm{tlr}} = \Big| V_{t, t-1} \odot \frac{\widetilde{H}_{t-1, t} - \widetilde{H}_t}{\widetilde{H}_{t-1, t} + \widetilde{H}_t} \Big|_1$$

其中 `\widetilde{H}_t` 为时刻 `t` 的 HDR 渲染，`\widetilde{H}_{t-1, t}` 为时刻 `t-1` 的渲染经光流 `V_{t, t-1}` 扭曲到时刻 `t` 的结果。分母归一化消除了 HDR 辐照度绝对尺度的影响，使正则化聚焦于相对亮度一致性。这一设计使良好监督时刻的外观传播到弱监督时刻，确保 HDR 时域稳定性。消融实验表明，去除 TLR 使 HDR-TAE 大幅恶化（Table 3e，Figure 6），时域一致性显著降低。

## 实验与关键发现

### 主实验结果

Mono4DGS-HDR 在合成与真实数据集上均取得最优性能。表 1 和表 2 分别报告了 Syn-Exp-3（合成，3 曝光）与 Real-Exp-2/Real-Exp-3（真实，2/3 曝光）场景的定量对比。

在 Syn-Exp-3 的测试帧上，Mono4DGS-HDR 的 HDR PSNR 达到 **37.64 dB**，较最优基线 MoSca-HDR（36.89 dB）提升 +0.75 dB；HDR-TAE 降至 0.057，优于 MoSca-HDR 的 0.059。在 LDR 观测曝光（LDR-OE）和新曝光（LDR-NE）指标上同样全面领先，且渲染速度达到 161 FPS（864×480 分辨率），显著快于 HDR-HexPlane（0.2 FPS）和 GaussHDR（2 FPS）。

在 Real-Exp-2 训练帧上，Mono4DGS-HDR 的 HDR-TAE 为 **0.046**，较 MoSca-HDR（0.054）降低 0.008，表明其时域一致性优势在真实场景中更为显著。在 Real-Exp-3 测试帧上，LDR-OE PSNR 为 27.65 dB，领先 MoSca-HDR 0.42 dB。

**公平性说明**：对于需要已知相机位姿的 GaussHDR 和 HDR-HexPlane，使用本文光束平差获得的初始相机参数作为输入；对于 SplineGS、MoSca 和 GFlow，扩展其颜色表示并添加相同的色调映射 MLP 以支持 HDR 模式；所有方法均训练相同的 15K 迭代次数。

图 5 和图 8 的定性对比进一步验证：Mono4DGS-HDR 在训练帧和测试帧上均能恢复更清晰、更稳定的 HDR 外观，而基线方法在弱光或过曝区域往往出现细节丢失或伪影。

### 消融实验

表 3 系统消融了各核心组件的贡献，所有实验均在 Real-Exp-3 和 Syn-Exp-3 测试帧上进行 15K 迭代。

**视频高斯初始化**：去除视频高斯初始化（w/o video Gaussian init.）导致 HDR PSNR 下降超过 1 dB，证实第一阶段在正交空间学习到的位置、旋转、缩放、不透明度与颜色先验对后续世界空间优化至关重要。

**遮挡处理**：去除遮挡感知的动态/静态分离（w/o occlusion handling）使 HDR PSNR 下降约 0.3 dB。图 3(c) 定性显示，无遮挡处理时动态/静态高斯分类出现明显错误。

**2D 协方差不变性**：直接继承视频高斯的缩放（w/o 2D covariance invariance）导致世界高斯尺度不合理（图 3(d)），HDR PSNR 随之下降。通过最小化视频与世界高斯投影协方差的 L2 差异重新拟合缩放，可有效保持视觉一致性。

**HDR 光度重投影损失**：去除该损失（w/o HDR photometric reproj. loss）使 HDR PSNR 和 TAE 均恶化。该损失利用第一阶段恢复的 HDR 训练视频，为相机位姿和场景几何提供密集监督，是第二阶段联合优化的关键约束。

**时序亮度正则化（TLR）**：去除 TLR（w/o temporal luminance reg.）导致 HDR-TAE 大幅增加，时域一致性显著降低。图 6 的定性消融可视化直观展示了 TLR 对抑制 HDR 外观随时间闪烁的作用。TLR 的核心机制是通过光流将良好监督时刻的动态内容传播到弱监督时刻（图 4），从而保证 HDR 时域稳定性。

**控制点采样间隔**：表 4 显示，三次 Hermite 样条的控制点采样间隔 $N_s$ 大于 4 时性能开始下降，表明过稀疏的采样无法充分表达动态高斯的运动轨迹。

**深度与光流/轨迹损失**：表 8 表明，去除深度损失或光流/轨迹损失均导致 PSNR 显著下降，验证了 2D 先验监督对场景几何与运动建模的必要性。

**曝光调度鲁棒性**：表 6 和表 7 分别验证了方法在不同曝光调度（随机 3 曝光、随机曝光值）和不同随机曝光扰动范围下的鲁棒性，性能波动较小。

### 失败模式与局限性

尽管 Mono4DGS-HDR 在多数场景下表现优异，仍存在若干典型失败案例（图 15）：

1. **2D 先验依赖**：方法深度依赖视觉基础模型提取的深度、光流和轨迹质量。在无纹理区域，光流估计不准确会导致动态/静态高斯分离错误。
2. **运动模糊**：快速相机或物体运动引起的运动模糊超出了当前方法的处理能力。
3. **非刚性运动**：由于 ARAP 约束的限制，难以建模复杂的非刚性运动（如火焰）。
4. **极低光/高噪声场景**：当前 LDR 域表示在极端光照条件下可能不足，结合 RAW 域表示或许是未来方向。

### 开放问题

- 是否可结合 RAW 域表示以更好地处理极低光/高噪声场景？
- 如何进一步放宽对成对光流计算的曝光一致性要求，以适应更任意的曝光调度？

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_9ZrjgzlAuh/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons on the test frames of Syn-Exp-3 scenes. Metrics are averaged over all scenes. LDR-OE and LDR-NE denote the LDR results with observed and novel exposures, respectively. HDR denotes the HDR results. FPS is measured at 864 × 480 resolution. † We use our initial camera parameters from bundle adjustment as the required camera inputs for GaussHDR (Liu et al., 2025a) and HDR-HexPlane (Wu et al., 2024a). ‡ We extend SplineGS (Park et al., 2025) and MoSca (Lei et al., 2025) to HDR mode for fair comparison*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_9ZrjgzlAuh/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparisons on the train frames of Real-Exp-2 scenes and the test frames of Real-Exp-3 scenes. Metrics are averaged over all scenes. OE denotes the observed-exposure results. † We use our initial camera parameters from bundle adjustment as camera inputs for GaussHDR (Liu et al., 2025a) and HDR-HexPlane (Wu et al., 2024a). ‡ We extend GFlow (Wang et al., 2025b), SplineGS (Park et al., 2025) and MoSca (Lei et al., 2025) to HDR mode for fair comparison*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_9ZrjgzlAuh/figures/007_Figure_5.jpg]]
*Figure 5: HDR visual comparisons on train/test frames. Our method achieves superior quality*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_9ZrjgzlAuh/figures/008_Table_3.jpg]]
*Table 3: Quantitative ablation results on the test frames of Real-Exp-3 and Syn-Exp-3 scenes. V2W denotes the video-to-world Gaussian transformation. All experiments are trained for 15K iteration. All the metrics listed here represent PSNR except HDR-TAE*

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_9ZrjgzlAuh/figures/021_Table_8.jpg]]
*Table 8: Ablation results about depth and flow/track losses on the test frames of Syn-Exp-3 scenes. Metrics are averaged over all scenes. LDR-OE and LDR-NE denote the LDR results with observed and novel exposures, respectively. HDR denotes the HDR results*

## 定位与知识库关联

### 任务定位与问题独特性

Mono4DGS-HDR 处于**无位姿单目动态场景重建**与**高动态范围新视角合成（HDR NVS）**的交叉地带。与已有工作相比，其核心独特之处在于同时处理三个耦合挑战：**（1）交替曝光导致的帧间亮度不一致**，使得标准光度重投影误差无法用于相机位姿优化；**（2）缺失直接 HDR 监督**，难以从稀疏的 LDR 观测中恢复稳定的 HDR 外观；**（3）单目无位姿设定**，需要同时估计相机轨迹与动态场景几何。

在方法谱系上，本文沿袭了基于 3D Gaussian Splatting（3DGS）的动态场景重建路线，但与以下工作形成明确区分：

- **静态 HDR NVS 方法**（如 **GaussHDR**，Liu et al., 2025a）：依赖已知相机位姿，无法处理动态场景和无位姿输入。
- **动态 HDR NVS 方法**（如 **HDR-HexPlane**，Wu et al., 2024a）：需要多相机设置，不适用于单目视频。
- **无位姿单目 4D 重建方法**（如 **MoSca**，Lei et al., 2025；**SplineGS**，Park et al., 2025；**GFlow**，Wang et al., 2025b）：原生不支持 HDR 重建。本文将其扩展至 HDR 模式（添加色调映射 MLP 和相同的颜色表示）作为基线，但实验表明简单扩展无法解决交替曝光带来的亮度不一致与位姿优化困难，Mono4DGS-HDR 在 HDR PSNR 上领先 **+0.75 dB**（Syn-Exp-3，Table 1），在 HDR 时域一致性（HDR-TAE）上亦有显著优势。

### 核心技术贡献的知识增量

本文的知识增量可归纳为三个相互依赖的机制，共同解决了上述耦合挑战：

**1. 正交空间视频高斯初始化（Stage 1）**

核心洞察：在无位姿条件下，交替曝光使标准光度重投影误差失效，导致相机位姿和场景几何的联合优化陷入困境。本文借鉴 SaV（Sun et al., 2024）的思路，在正交相机坐标空间训练全动态 HDR 视频高斯，完全消除对相机位姿的依赖。这一阶段输出的 HDR 视频具有一致亮度，为后续位姿优化和场景重建提供了**稳定的监督信号源**。消融实验（Table 3a）证实：去除视频高斯初始化导致 PSNR 下降超过 1 dB，验证了该阶段对整体系统的关键支撑作用。

**2. 视频-世界高斯变换（V2W Transformation）**

该模块将第一阶段的正交空间高斯转换为世界空间初始化，包含三个子机制：
- **遮挡感知的动态/静态分离**：通过统计视频高斯在动态区域且未被遮挡的帧次数 $N_d$（Eq. 1），实现鲁棒的动静分类。去除遮挡处理使 HDR PSNR 下降约 0.3 dB（Table 3b）。
- **基于 2D 协方差不变性的缩放重拟合**：利用视频高斯与世界高斯在图像平面上的 2D 协方差约束（Eq. 2），通过优化求解世界高斯的初始缩放，保持视觉一致性。直接继承缩放会导致不合理的尺度（Table 3c，Figure 3d）。
- **属性变换**：将位置、旋转、不透明度与颜色从正交空间映射到世界空间。

**3. 时序亮度正则化（TLR）与 HDR 光度重投影损失**

这是本文在优化层面最具原创性的贡献：
- **TLR**（Eq. 3）：利用光流将相邻帧的 HDR 辐照度对齐，通过归一化消除辐照度尺度影响，使良好监督时刻的外观传播到弱监督时刻。去除 TLR 导致 HDR-TAE 大幅恶化（Table 3e，Figure 6），证实其对时域一致性的关键作用。
- **HDR 光度重投影损失**：基于第一阶段恢复的 HDR 视频，计算密集的光度重投影误差，同时优化相机位姿和世界高斯。这解决了交替曝光下标准 LDR 重投影误差不可用的瓶颈。去除该损失使 PSNR 下降（Table 3d）。

### 适用边界与局限性

本文通过定量消融和定性分析揭示了若干适用边界：

1. **对 2D 先验质量的依赖**：方法依赖深度、光流、轨迹等视觉基础模型的输出进行初始化和正则化。去除深度损失或光流/轨迹损失导致 PSNR 显著下降（Table 8）。在无纹理区域，光流估计不准确会影响动态/静态高斯分离（Figure 15 典型失败案例）。

2. **运动建模能力受限**：由于采用 ARAP（as-rigid-as-possible）约束，方法难以建模复杂的非刚性运动（如火焰）。快速相机或物体运动引起的运动模糊也会导致次优结果。

3. **曝光调度假设**：光流计算要求相邻帧曝光一致（成对对齐），这限制了输入视频的曝光调度模式。Table 6 和 Table 7 分别探索了不同曝光调度和随机曝光扰动范围下的鲁棒性，表明方法对曝光变化有一定容忍度，但极端情况仍需进一步验证。

### 开放问题

1. **RAW 域扩展**：当前方法在 sRGB 域操作，是否可结合 RAW 域表示以更好地处理极低光/高噪声场景？
2. **更任意的曝光调度**：如何进一步放宽对成对光流计算的曝光一致性要求，使方法适用于完全任意的逐帧曝光变化？
3. **运动建模泛化**：能否引入更灵活的运动先验（如可变形高斯）替代 ARAP 约束，以扩展对非刚性运动的建模能力？

## 原文 PDF

![[paperPDFs/ICLR_2026/Mono4DGS_HDR_High_Dynamic_Range_4D_Gaussian_Splatting_from_Alternating_exposure_8634b557c5bd.pdf]]
