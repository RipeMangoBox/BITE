---
title: "STAvatar: Soft Binding and Temporal Density Control for Monocular 3D Head Avatars Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/STAvatar_Soft_Binding_and_Temporal_Density_Control_for_Monocular_3D_Head_Avatars_Reconstruction.pdf
project_link: "https://jiankuozhao.github.io/STAvatar/"
code_link: null
aliases:
- STAvatar
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过在UV空间中学习每个高斯体的特征偏移（UV-Adaptive Soft Binding），并结合基于FLAME参数的时间聚类（FTC）和融合感知误差（FPE-AP）的密度控制策略，可以显著提升动态头部化身的重建质量。
primary_logic: 将高斯形变建模从三角面片刚性绑定提升到UV空间可学习偏移，不仅保留了3DGS的自适应密度控制能力，还能有效表达细粒度非刚性形变；同时针对动态序列中的瞬时可见区域，通过时间结构聚类和感知误差驱动的密度增加，克服了传统ADC的欠拟合问题。
claims:
- 在INSTA数据集上PSNR达30.63、SSIM 0.9587、LPIPS 0.0304，显著优于所有对比方法
- 去除软绑定后PSNR下降约1 dB，LPIPS上升约0.009
- FTC使口腔内部高斯数量增加超过400（约17%），改善了该区域的细节重建
- INSTA 上 PSNR↑ = 30.63
---

# STAvatar: Soft Binding and Temporal Density Control for Monocular 3D Head Avatars Reconstruction

> [!tip] 核心洞察
> 将高斯形变建模从三角面片刚性绑定提升到UV空间可学习偏移，不仅保留了3DGS的自适应密度控制能力，还能有效表达细粒度非刚性形变；同时针对动态序列中的瞬时可见区域，通过时间结构聚类和感知误差驱动的密度增加，克服了传统ADC的欠拟合问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | STAvatar：面向单目3D头部化身重建的软绑定与时间密度控制 |
| 英文题名 | STAvatar: Soft Binding and Temporal Density Control for Monocular 3D Head Avatars Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.19854) · [Project](https://jiankuozhao.github.io/STAvatar/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | STAvatar |
| Dataset | INSTA, PointAvatar, NerFace, HDTF |

> [!tip] 效果简介
> - INSTA 上，PSNR↑ 30.63 vs 28.41 (RGBAvatar) (+2.22)；SSIM↑ 0.9587 vs 0.9493 (RGBAvatar) (+0.0094)；LPIPS↓ 0.0304 vs 0.0508 (FateAvatar) (-0.0204)。
> - PointAvatar 上，PSNR↑ 28.25 vs 28.36 (FateAvatar) (-0.11)；SSIM↑ 0.9337 vs 0.9287 (FateAvatar) (+0.0050)；LPIPS↓ 0.0495 vs 0.0776 (FateAvatar) (-0.0281)。
> - NerFace 上，PSNR↑ 30.08 vs 27.13 (RGBAvatar) (+2.95)。

## 概述

从单目视频重建高保真3D头部化身是数字人领域的核心挑战。现有基于3D高斯泼溅（3DGS）的方法虽在渲染效率上占优，却面临两个关键瓶颈：

**硬绑定限制细粒度形变。** 主流方法如**GaussianAvatars**（Qian et al., CVPR 2024）将高斯体刚性附着于FLAME网格三角面片，仅通过线性混合蒙皮（LBS）驱动。这种硬绑定（hard binding）迫使高斯体在三角面片坐标系内保持相对静止，无法捕捉面部皱纹、牙齿边缘等非刚性细微形变。

**标准自适应密度控制忽略瞬时可见区域。** 原生3DGS的自适应密度控制（ADC）基于位置梯度的视图空间阈值全局统一执行。然而，口腔内部等瞬时可见区域在大部分帧中被遮挡，其平均位置梯度被严重稀释，导致这些区域的高斯体无法有效加密，重建细节缺失。同时，位置梯度仅反映几何不一致性，常丢失纹理细节，难以驱动高频区域的高斯体添加。

针对上述问题，**STAvatar**提出两个核心创新：

1. **UV-Adaptive Soft Binding（UV自适应软绑定）**：在UV空间中学习每个高斯体的特征偏移量，与粗粒度的LBS变换叠加，使高斯体可突破三角面片的刚性约束，灵活表达非刚性形变，同时保留3DGS自适应密度控制的能力。

2. **Temporal Adaptive Density Control（时间自适应密度控制）**：包含FLAME条件时间聚类（FTC）和融合感知误差（FPE-AP）。FTC将视频帧按结构相似性聚类，使密度控制在各簇内独立执行，有效覆盖瞬时可见区域；FPE-AP结合L1与D-SSIM构建感知误差图，并引入峰值误差集合，在平均误差和瞬时尖峰两个维度识别需加密的高斯体。

在INSTA、PointAvatar、NerFace和HDTF四个基准数据集上，STAvatar全面超越现有方法。以INSTA数据集为例，PSNR达30.63（较次优方法RGBAvatar提升+2.22），SSIM达0.9587，LPIPS低至0.0304。消融实验证实，去除软绑定后PSNR下降约1 dB、LPIPS上升约0.009；FTC使口腔内部高斯数量平均增加超过400（约17%），显著改善该区域细节重建。

**方法定位。** STAvatar属于优化式单目头像重建框架，需针对每个受试者单独训练。与单图前馈泛化方法（如GAGAvatar、LAM）相比，身份保真度更高，但无法在单次前向传播中完成重建，在即时应用或数据稀缺场景下适用性受限。

## 背景与动机

### 问题场景：单目视频驱动的3D头部化身重建

从单目RGB视频中重建可驱动的逼真3D头部化身，在虚拟现实、远程呈现和数字人应用中具有重要价值。这项任务的核心挑战在于：仅凭一段受试者说话或表演的二维视频，重建出三维几何结构、恢复高频外观细节（如皱纹、牙齿），并支持对新表情和姿态的准确驱动。

近年来，3D Gaussian Splatting（3DGS）因其高质量实时渲染和显式几何表示的优势，成为该领域的主流技术路线。一系列基于3DGS的头部化身方法——如**GaussianAvatars**（Qian et al., CVPR 2024）、**FlashAvatar**（Xiang et al., CVPR 2024）、**SplattingAvatar**（Shao et al., CVPR 2024）、**MonoGaussianAvatar**（Chen et al., SIGGRAPH 2024）、**FateAvatar**（Zhang et al., CVPR 2025）和**RGBAvatar**（Li et al., CVPR 2025）——通过将高斯原语绑定到参数化头部模型（如FLAME）的三角面片上，实现了可驱动的动态重建。然而，现有方法在形变建模和密度控制两个关键环节仍存在系统性缺陷。

### 瓶颈一：硬绑定限制非刚性细节表达

现有基于3DGS的方法普遍采用**硬绑定（Hard Binding）**策略：每个高斯体刚性附着于FLAME网格的某个三角面片，其动画参数完全由面片的线性混合蒙皮（LBS）变换决定。这种设计虽然保证了动画一致性，却从根本上限制了模型对**非刚性形变**的捕捉能力——面部皱纹、酒窝、眼睑褶皱等细微表情变化无法被LBS驱动的刚性变换所表达。高斯体在三角面片局部坐标系内保持相对静止，导致高频细节区域的几何和纹理重建趋于平滑（见Figure 2a）。

### 瓶颈二：标准自适应密度控制忽略瞬时可见区域

3DGS的标准自适应密度控制（ADC）根据位置梯度和视图空间阈值来决定是否克隆或分裂高斯体，以增加几何复杂度。然而，这一策略在动态头部场景中存在两个关键盲区：

1. **瞬时可见区域欠拟合**：口腔内部、眼睑内侧等区域仅在特定表情下短暂暴露，在绝大多数帧中处于遮挡状态。这些区域的平均位置梯度较低，无法触发标准ADC的增密操作，导致重建时细节严重缺失（见Figure 2b）。
2. **位置梯度无法反映纹理需求**：位置梯度仅捕捉几何不一致性，而高频纹理区域（如唇纹、眉毛）即使几何位置准确，也需要更多高斯体来建模外观细节。仅依赖位置梯度的ADC会遗漏这些区域的密度需求（见Figure 2c）。

### 动机：从刚性绑定到可学习软绑定，从静态ADC到时间感知密度控制

上述分析揭示了一个因果闭环：**硬绑定**使高斯体无法脱离三角面片刚性框架去适应局部非刚性形变，而**标准ADC**又无法为瞬时可见区域和纹理复杂区域分配足够的高斯容量。两个问题叠加，导致现有方法在皱纹、牙齿、口腔内部等关键区域的保真度系统性不足。

本文的**STAvatar**围绕这两个瓶颈提出针对性解决方案：

- **UV-Adaptive Soft Binding**：将形变建模从三角面片刚性绑定提升到UV空间可学习偏移。在保留LBS粗变换兼容性的前提下，通过双分支网络为每个高斯体预测位置、旋转、缩放、颜色和不透明度的特征偏移，使高斯体能够灵活适应非刚性形变，同时保持3DGS自适应密度控制的能力。
- **Temporal Adaptive Density Control（Temporal ADC）**：引入FLAME条件时间聚类（FTC）和融合感知误差（FPE-AP）两项机制。FTC将视频帧按结构相似性聚类，使ADC在簇内计算增密准则时能有效捕获瞬时可见区域；FPE-AP结合L1和D-SSIM构建感知误差图，并增设峰值误差集合，确保纹理复杂区域和瞬态高误差区域均能获得充分的高斯增密。

通过这两个核心模块的协同，STAvatar在保留3DGS高效渲染和显式几何优势的同时，显著提升了动态头部化身在非刚性细节和遮挡区域的保真度，在INSTA、PointAvatar、NerFace和HDTF四个基准数据集上取得了最优重建性能（见Table 1）。

## 核心创新

STAvatar 面向单目视频动态头部化身重建，针对现有 3DGS 方法的两个根本瓶颈提出了两条正交的关键创新：**UV-Adaptive Soft Binding** 和 **Temporal Adaptive Density Control（Temporal ADC）**。二者共同构成了从“刚性绑定 + 全局密度控制”到“软绑定 + 时间感知密度控制”的范式转变。

### 瓶颈一：硬绑定限制非刚性形变表达

现有基于 3DGS 的头部化身方法（如 **GaussianAvatars**（Qian et al., CVPR 2024）、**SplattingAvatar**（Shao et al., CVPR 2024）等）普遍采用**硬绑定（hard binding）**：每个高斯体刚性附着于 FLAME 网格的父三角面片上，仅通过线性混合蒙皮（LBS）驱动其位置与旋转。这种机制下，高斯体在三角面片局部坐标系内保持相对静止，无法主动偏移以捕捉面部皱纹、微表情等**非刚性细粒度形变**。Figure 2(a) 直观展示了这一局限。

### 创新一：UV-Adaptive Soft Binding（Changed Slot 1）

STAvatar 将形变绑定方式从硬绑定升级为**UV 空间中的可学习软绑定**：

- **双分支偏移预测网络**：以固定身份参考图的 UV 位置图 $UV_{pos}'$ 和当前帧相对于参考帧的顶点位移光栅化 UV 图 $UV_{disp}'$ 为输入，构建全局分支 $\Phi_g$ 和局部分支 $\Phi_l$ 的双分支架构（Figure 3(b)）。全局分支捕捉整体形变趋势，局部分支通过四个区域特定头（眼睛、嘴、鼻子、额头）聚焦表情敏感区域，输出为：

  $$\omega_g = \Phi_g(T, UV_{pos}', \beta), \quad \omega_l = \sum_{i=1}^{4} H_i(M_i \odot \Phi_l(T, UV_{disp}', \beta))$$

  二者融合后得到 UV 空间的特征偏移图 $\Delta_{map} = \mathcal{F}(\omega_g, \omega_l)$。

- **UV 自适应采样与参数修正**：对每个高斯体 $g_i$，根据其 UV 坐标从 $\Delta_{map}$ 中采样偏移量 $\delta_i = \{\delta_\mu, \delta_c, \delta_\alpha, \delta_s, \delta_r\}$，叠加到粗 LBS 估计的动画参数 $\tilde{\theta}$ 上得到最终参数 $\theta^*$：

  $$\mu^* = \tilde{\mu} + \delta_{\mu},\; c^* = \tilde{c} + \delta_c,\; \alpha^* = \tilde{\alpha} + \delta_{\alpha},\; s^* = \tilde{s} \odot \delta_s,\; r^* = q(\tilde{r}, \delta_r)$$

  其中位置偏移通过 $\delta_{\mu} = 0.1 \cdot \tanh(x)$ 约束在 $[-0.1, 0.1]$，缩放偏移 $\delta_s = \exp(x)$ 保证正值，旋转偏移角度归一化到 $[-\pi, \pi]$。

**因果机制**：软绑定将形变建模从三角面片刚体变换提升为 UV 空间逐高斯体的可学习偏移，既保留了 3DGS 自适应密度控制（ADC）的兼容性，又赋予了高斯体主动适应非刚性细节的能力。消融实验（Table 2, Figure 7）表明，去除软绑定后 PSNR 下降约 1 dB，LPIPS 上升约 0.009，牙齿和皱纹等细节明显丢失。

### 瓶颈二：标准 ADC 忽略时间维度的瞬时可见区域

3DGS 的标准自适应密度控制（vanilla ADC）基于**位置梯度**和视图空间尺度阈值全局统一执行克隆与分裂。然而在动态头部序列中，口腔内部等区域仅在特定表情下瞬时可见，平均位置梯度极低（Figure 2(b)），导致这些区域的高斯体密度不足，重建空洞或模糊。此外，位置梯度仅反映几何不一致性，对纹理细节不敏感（Figure 2(c)），进一步加剧了高纹理区域的欠拟合。

### 创新二：Temporal Adaptive Density Control（Changed Slot 2）

STAvatar 提出时间自适应密度控制策略，包含两个耦合组件：

- **FLAME 条件时间聚类（FTC）**：对视频帧的 FLAME 参数（姿态、表情、形状）经 PCA 降维后进行 K-means 聚类，将结构相似的帧归入同一簇（Figure 4）。ADC 在每个簇内独立执行，使得瞬时可见区域在其所属簇中获得充分且有针对性的密度增加计算。Figure 8 定量验证：FTC 使口腔内部高斯数量平均增加超过 400（约 17%），显著改善了该区域的细节重建。

- **融合感知误差与峰值准则（FPE-AP）**：替代位置梯度作为克隆判据。首先构建逐像素融合感知误差图：

  $$E = (1 - \lambda_1) |\mathcal{L}_1| + \lambda_1 \mathcal{L}_{\mathrm{d-ssim}}$$

  对每个高斯体 $g_i$，通过总和面积表（SAT）在常数时间内计算其屏幕投影矩形区域内的**平均融合感知误差** $\bar{E}_i$（Equation 9），并追踪所有训练迭代中的**峰值融合感知误差** $E_i^{\mathrm{peak}}$（Equation 10）。克隆条件为：

  $$\bar{E}_i > \tau_{\mathrm{avg}} \quad \mathrm{or} \quad i \in \mathcal{S}_{\mathrm{peak}}$$

  即平均误差超过阈值 $\tau_{\mathrm{avg}}=10^{-3}$，或属于前 3% 峰值误差集合。这一双重准则同时捕获持续欠拟合区域和瞬态尖峰误差区域。

**因果机制**：FTC 将密度控制从“全局时间平均”解耦为“结构相似帧内计算”，使瞬时可见区域不再被常可见区域的平均梯度淹没；FPE-AP 以感知误差替代纯几何梯度，直接定位纹理和几何重建不佳的区域，并通过峰值集合机制捕获短时出现的极端误差。消融实验（Table 2, Figure 7）证实，去除 ADC 后 LPIPS 显著升高，牙齿区域过于平滑；用位置梯度替换 FPE-AP 则牙齿细节变模糊；去除 FTC 后口腔内部重建不完整。

### 创新协同效应

软绑定与 Temporal ADC 并非孤立改进，二者形成协同：软绑定提供的非刚性形变自由度会产生更丰富的几何-纹理误差信号，为 FPE-AP 提供更精确的密度控制指引；Temporal ADC 增加的瞬时区域高斯密度则为软绑定的细粒度偏移提供了足够的表达容量。在 INSTA 数据集上，完整方法达到 PSNR 30.63、SSIM 0.9587、LPIPS 0.0304（Table 1），显著优于所有对比方法，且训练效率最高（Figure 9），6 个 epoch 内快速收敛至最优水平。

## 整体框架

STAvatar 的整体 pipeline 围绕两个核心创新展开：**UV-Adaptive Soft Binding（UV 自适应软绑定）** 和 **Temporal Adaptive Density Control（时间自适应密度控制）**，旨在从单目视频中重建高保真 3D 头部化身。整个框架的输入为一段单目人脸视频，输出为一个可驱动的 3D 高斯化身，其架构可划分为四个串联模块。

### 1. FLAME 跟踪与初始化

首先，对输入视频的每一帧进行 FLAME 参数估计，获取姿态、表情和形状系数，并生成对应的 FLAME 网格。以中性表情帧为参考网格，将 3D 高斯原语初始化于网格三角面片上。规范空间中的高斯参数通过父三角面的重心映射变换到动画空间（公式 (2)），得到粗估计参数 $\tilde{\theta}$，为后续的软绑定提供基础形变场。

### 2. UV-Adaptive Soft Binding 框架

这是 STAvatar 的核心形变模块。与现有方法将高斯体刚性地绑定于三角面片（hard binding）不同，STAvatar 在 UV 空间中学习每个高斯体的特征偏移量。具体而言，该模块构建一个**双分支网络**：全局分支 $\Phi_g$ 接收 UV 位置图和表情系数，预测全局特征 $\omega_g$（公式 (4)）；局部分支 $\Phi_l$ 则通过四个区域特定头（眼睛、嘴、鼻子、额头）对 UV 位移图进行局部特征提取，输出 $\omega_l$（公式 (5)）。两者融合后得到 UV 空间的特征偏移图 $\Delta_{map}$（公式 (6)）。随后，通过 UV 自适应采样为每个高斯体 $g_i$ 分配一个偏移量 $\delta_i$，将其叠加到粗估计参数 $\tilde{\theta}$ 上，得到最终的高斯参数 $\theta^*$（公式 (7)），包括位置、颜色、不透明度、缩放和旋转的精细调整。

该设计的关键优势在于：保留了 3DGS 的自适应密度控制能力，同时通过可学习的 UV 空间偏移有效表达面部皱纹、牙齿边缘等非刚性细粒度形变，克服了硬绑定下高斯体随三角面片刚性运动而无法捕捉微表情的瓶颈。

### 3. Temporal Adaptive Density Control

针对标准 ADC 在动态场景中的两个缺陷——瞬时可见区域（如口腔内部）因平均位置梯度低而难以增密，以及位置梯度无法反映纹理误差——STAvatar 提出时间自适应密度控制策略，包含两个子组件：

- **FLAME-Conditioned Temporal Clustering (FTC)**：利用 FLAME 参数对视频帧进行 PCA 降维后 K-means 聚类，将结构相似的帧归入同一簇，并在每个簇内独立执行 ADC。这使得瞬时可见区域在其所属簇中获得充分的密度增加机会，实验表明 FTC 使口腔内部高斯数量平均增加超过 400（约 17%）。
- **Fused Perceptual Error with Average-Peak (FPE-AP)**：构建融合感知误差图 $E$（公式 (8)），结合 L1 和 D-SSIM 误差，并引入峰值误差集合机制。克隆条件（公式 (11)）同时考虑平均误差超过阈值 $\tau_{\text{avg}}$ 和属于前 3% 峰值集合的高斯体，从而在高频纹理区域和几何误差区域均能有效增密。

### 4. 可微分渲染与损失优化

最终高斯参数通过 3D Gaussian Splatting 渲染为图像，并与真实帧计算复合损失函数（公式 (14)）：包含 L1、D-SSIM 和可选 VGG 感知损失的 RGB 损失 $\mathcal{L}_{\text{rgb}}$（公式 (12)），约束缩放和颜色偏移的正则项 $\mathcal{L}_{\text{offset}}$（公式 (13)），以及位置和尺度正则项。整个框架端到端训练，在 6 个 epoch 内即可快速收敛。

**Figure 3** 给出了完整的架构总览，清晰展示了从输入准备、双分支偏移预测、UV 采样到融合感知误差计算的数据流。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/003_Figure_3.jpg]]
*Figure 3: Overview of STAvatar. (a) In addition to a fixed identity reference image and its UV position map, we further rasterize the vertex offsets between reference mesh and control mesh to obtain a UV displacement map as input. (b) We construct a dual-branch network to predict a feature offset map in UV space, from which an offset δi is sampled for each Gaussian gi. This offset is added to the coarsely estimated parameters ˜θ to get final parameters*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/001_Figure_1.jpg]]
*Figure 1: STAvatar proposes a Soft Binding framework and a Temporal Adaptive Density Control strategy to reconstruct highfidelity 3D head avatars from monocular videos*

## 核心模块与公式推导

STAvatar 的核心管线由四个模块构成，其设计直指现有 3DGS 头部化身方法的两大瓶颈：硬绑定无法捕捉非刚性形变，以及标准 ADC 忽视瞬时可见区域。以下按信息流顺序展开。

---

### 3.1 FLAME 跟踪与高斯体初始化

给定单目视频，首先利用现成的 FLAME 跟踪器估计每帧的姿态、表情和形状参数，生成对应的 FLAME 网格。随后，在规范空间的网格三角面片上初始化一组 3D 高斯原语，每个原语由其位置 $\pmb{\mu}$、缩放 $\pmb{s}$、旋转 $\pmb{r}$、不透明度 $\alpha$ 和颜色 $\pmb{c}$ 定义，密度函数为：

$$
G(\pmb{x}) = e^{-\frac{1}{2} (\pmb{x} - \pmb{\mu})^{T} \Sigma^{-1} (\pmb{x} - \pmb{\mu})}
\tag{1}
$$

动画时，通过父三角面的重心映射将规范空间参数粗变换到动画空间：

$$
\tilde{r} = r R,\ \tilde{\mu} = k r \mu + t,\ \tilde{s} = k s,\ \tilde{\alpha} = \alpha,\ \tilde{c} = c
\tag{2}
$$

其中 $R$、$k$、$t$ 由三角面的刚性变换导出。这一粗变换构成了后续软绑定的基座。

---

### 3.2 UV-Adaptive Soft Binding 框架

核心创新在于将形变建模从三角面片刚性绑定提升为 UV 空间可学习偏移。框架包含三个子步骤：

**输入准备。** 除固定的身份参考图像及其 UV 位置图 $UV_{pos}$ 外，还额外将参考网格与控制网格之间的顶点偏移光栅化，得到 UV 位移图 $UV_{disp}$，为网络提供显式的几何变化先验。

**双分支网络预测特征偏移图。** 网络以 FLAME 参数 $T$、$UV_{pos}'$、$UV_{disp}'$ 和身份编码 $\beta$ 为输入，分两支处理：

- **全局分支** 输出全局特征 $\omega_g$：
  $$
  \omega_g = \Phi_g(T, UV_{pos}', \beta)
  \tag{4}
  $$

- **局部分支** 通过四个区域特定头（眼睛、嘴、鼻子、额头）输出局部特征 $\omega_l$，并由区域掩码 $M_i$ 加权：
  $$
  \omega_l = \sum_{i=1}^{4} H_i(M_i \odot \Phi_l(T, UV_{disp}', \beta))
  \tag{5}
  $$

两支输出经融合函数 $\mathcal{F}$ 得到最终的特征偏移图：

$$
\Delta_{map} = \mathcal{F}(\omega_g, \omega_l)
\tag{6}
$$

**UV 自适应采样与参数合成。** 对每个高斯体 $g_i$，在其 UV 坐标处从 $\Delta_{map}$ 采样得到偏移量 $\delta_i = \{\delta_{\mu}, \delta_c, \delta_{\alpha}, \delta_s, \delta_r\}$，叠加到粗估计上获得最终参数：

$$
\mu^* = \tilde{\mu} + \delta_{\mu},\ c^* = \tilde{c} + \delta_c,\ \alpha^* = \tilde{\alpha} + \delta_{\alpha},\ s^* = \tilde{s} \odot \delta_s,\ r^* = q(\tilde{r}, \delta_r)
\tag{7}
$$

其中各偏移量通过激活函数约束范围：位置偏移经 $0.1 \cdot \tanh(x)$ 限制在 $[-0.1, 0.1]$，缩放偏移经 $\exp(x)$ 保证正值，旋转角度经 $\pi \cdot \tanh(x)$ 归一化至 $[-\pi, \pi]$，不透明度偏移经 $0.5 \cdot \tanh(x)$ 约束在 $[-0.5, 0.5]$，颜色偏移经 $0.7 \cdot \tanh(x)$ 限制在每通道 $[-0.7, 0.7]$。

---

### 3.3 Temporal Adaptive Density Control

标准 ADC 在动态场景中存在两个致命缺陷：一是瞬时可见区域（如口腔内部）因大部分时间被遮挡而平均位置梯度极低，无法触发克隆；二是位置梯度仅反映几何不一致，丢失纹理细节。STAvatar 的 Temporal ADC 通过两个机制解决：

**FLAME 条件时间聚类（FTC）。** 先对 FLAME 参数做 PCA 降维，再以 KMeans 将视频帧聚为 $K$ 个结构相似的簇。ADC 在每个簇内独立执行，确保瞬时可见区域在其所属簇中获得充分的密度增加机会。消融实验显示，FTC 使口腔内部高斯数量平均增加超过 400（约 17%），直接验证了其在瞬时区域的有效性（Figure 8）。

**融合感知误差-平均/峰值准则（FPE-AP）。** 首先构建逐像素的融合感知误差图，结合 L1 和 D-SSIM（$\lambda_1 = 0.2$）：

$$
E = (1 - \lambda_1) |\mathcal{L}_1| + \lambda_1 \mathcal{L}_{\mathrm{d-ssim}}
\tag{8}
$$

对每个高斯体 $i$，利用记录属性估计其 2D 投影区域 $\mathcal{P}_i$，计算该区域内的加权平均误差 $\bar{E}_i$ 和所有训练迭代中的峰值误差 $E_i^{\mathrm{peak}}$：

$$
\bar{E}_i = \frac{A_i}{C_i} \sum_{p \in \mathcal{P}_i} E(p)
\tag{9}
$$

$$
E_i^{\mathrm{peak}} = \max_t \left( \frac{A_i^{(t)}}{C_i^{(t)}} \sum_{p \in \mathcal{P}_i^{(t)}} E^{(t)}(p) \right)
\tag{10}
$$

其中 $A_i$ 为投影面积，$C_i$ 为覆盖像素数。克隆条件为：

$$
\bar{E}_i > \tau_{\mathrm{avg}} \quad \mathrm{or} \quad i \in \mathcal{S}_{\mathrm{peak}}
\tag{11}
$$

即平均误差超过阈值 $\tau_{\mathrm{avg}} = 10^{-3}$，或属于前 3% 的峰值误差集合。为高效计算矩形区域内的误差总和，采用总和面积表（SAT）将查询降至常数时间。消融实验证实，用原始位置梯度替换 FPE-AP 会导致牙齿细节变模糊（Table 2, Figure 7）。

---

### 3.4 可微分渲染与损失优化

最终图像通过深度排序后的 α 混合渲染：

$$
C = \sum_{i=1}^{N} c_i^* \alpha_i' \prod (1 - \alpha_j')
\tag{3}
$$

训练损失由四部分构成：

**RGB 损失** 组合 L1、D-SSIM 和可选的 VGG 感知损失（$\gamma$ 为开关）：

$$
\mathcal{L}_{\mathrm{rgb}} = (1 - \lambda_1) \mathcal{L}_1 + \lambda_1 \mathcal{L}_{\mathrm{d-ssim}} + \gamma \lambda_2 \mathcal{L}_{\mathrm{vgg}}
\tag{12}
$$

**偏移正则化损失** 约束缩放和颜色偏移的幅度：

$$
\mathcal{L}_{\mathrm{offset}} = \lambda_3 |\delta_s - 1| + \lambda_4 \delta_c
\tag{13}
$$

加上位置正则 $\mathcal{L}_{\mathrm{position}}$ 和尺度正则 $\mathcal{L}_{\mathrm{scale}}$，总损失为：

$$
\mathcal{L} = \mathcal{L}_{\mathrm{rgb}} + \mathcal{L}_{\mathrm{offset}} + \lambda_p \mathcal{L}_{\mathrm{position}} + \lambda_s \mathcal{L}_{\mathrm{scale}}
\tag{14}
$$

---

**小结。** STAvatar 以 UV 空间可学习偏移解耦了形变建模与三角面片刚性绑定，使 3DGS 的自适应密度控制能力得以保留；同时通过 FTC 和 FPE-AP 双管齐下，将密度控制从全局均匀策略升级为时间感知、误差驱动的精细化策略。这两个模块的协同，是其在口腔内部、皱纹等挑战区域取得显著提升的根本原因。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/004_Figure_4.jpg]]
*Figure 4: FLAME-Conditioned Temporal Clustering. We cluster video frames into K clusters and conduct ADC within each cluster’s training*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/002_Figure_2.jpg]]
*Figure 2: Limitations of existing research. (a) Hard binding forces Gaussians to remain relatively static within the triangle coordinate frames, thereby limiting their ability to capture fine-grained details. (b) Transiently visible regions, such as mouth interiors, often exhibit low average positional gradients, which impedes effective Gaussian densification. (c) The positional gradient only reflects geometric inconsistencies and often loses texture details, which hinders the addition of Gaussians in high-frequency regions*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/016_Figure_4.jpg]]
*Figure 4: Visualization of learned UV attribute offset maps. Larger magnitudes are primarily observed in high-frequency and highly deformable regions, such as hair and expression-related areas*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/013_Figure_3.jpg]]
*Figure 3: t-SNE visualization of different identities after applying FTC. Each color represents a distinct video frame cluster*

## 实验与分析

### 定量主结果

Table 1 汇总了 STAvatar 与 6 种代表性优化式方法在 INSTA、PointAvatar、NerFace 和 HDTF 四个基准上的全面对比。STAvatar 在所有数据集上均取得最优或次优的 LPIPS，并在 INSTA、NerFace 和 HDTF 上达到最高 PSNR 与 SSIM。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/005_Table_1.jpg]]
*Table 1: Comparison of quantitative results with state-of-the-art methods. The best and second are highlighted, respectively*

在 INSTA 数据集上，STAvatar 的 PSNR 达 **30.63**，相较次优方法 **RGBAvatar**（Li et al., CVPR 2025）的 28.41 提升 **+2.22 dB**；SSIM 为 **0.9587**，提升 **+0.0094**；LPIPS 降至 **0.0304**，较 **FateAvatar**（Zhang et al., CVPR 2025）的 0.0508 降低 **-0.0204**。在 NerFace 上，PSNR 领先次优方法 **+2.95 dB**，LPIPS 降低 **-0.0239**。在 HDTF 上，PSNR 较 FateAvatar 提升 **+0.81 dB**，LPIPS 较 **FlashAvatar**（Xiang et al., CVPR 2024）降低 **-0.0232**。仅在 PointAvatar 的 PSNR 上略低于 FateAvatar（28.25 vs 28.36，-0.11 dB），但 LPIPS 仍大幅领先（0.0495 vs 0.0776，-0.0281），表明 STAvatar 在感知质量上具有一致优势。

Table 3 和 Table 4 提供了逐身份（per-identity）的完整结果，进一步验证了上述跨身份泛化性。与单图前馈式方法 GAGAvatar 和 LAM 的对比（Table 2 supp）显示，STAvatar 在身份保真度上显著优于这些泛化方法，尽管其优化式框架需要逐受试者训练。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/008_Table_2.jpg]]
*Table 2: Ablation quantitative results on the INSTA dataset*

### 训练效率

Figure 9 展示了各方法在训练过程中的 PSNR 收敛曲线。STAvatar 在仅 **6 个 epoch** 内即达到最高 PSNR，训练效率在所有对比方法中最高。相比之下，**MonoGaussianAvatar**（Chen et al., SIGGRAPH 2024）需要 100 个 epoch，**SplattingAvatar**（Shao et al., CVPR 2024）需要 30 个 epoch，而 STAvatar 的快速收敛得益于 UV-Adaptive Soft Binding 提供了更强的形变先验，减少了优化负担。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/011_Figure_9.jpg]]
*Figure 9: Comparison of PSNR performance across different methods during training. STAvatar exhibits the highest training efficiency among all compared approaches*

### 消融实验

Table 2 和 Figure 7 系统消融了 STAvatar 各核心组件在 INSTA 数据集上的贡献。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative results of the ablation study on marcel case. Our full method produces more realistic textures and geometric structures in transiently visible regions, such as the mouth interior, and captures more fine details*

**软绑定（Soft Binding）**：去除软绑定后退化为硬绑定，PSNR 从 30.63 降至约 **29.66**（下降约 **1 dB**），LPIPS 从 0.0304 升至约 **0.0398**（上升约 **0.009**）。Figure 7 显示牙齿边缘和面部皱纹等细粒度非刚性细节明显丢失，验证了 UV 空间可学习偏移对表达细微形变的关键作用。

**自适应密度控制（ADC）**：完全去除 ADC 后，LPIPS 显著升高，牙齿区域的重建变得过于平滑，缺乏纹理细节。这表明在动态头部化身中，标准 3DGS 的密度控制对捕捉高频信息不可或缺。

**融合感知误差（FPE-AP）**：将 FPE-AP 替换为原始位置梯度准则后，牙齿细节变模糊。FPE-AP 结合了 L1 和 D-SSIM 误差图（$\lambda_1=0.2$），能同时感知几何和纹理误差，而位置梯度仅反映几何不一致性（Figure 2(c)），对纹理区域的欠拟合不敏感。

**时间聚类（FTC）**：去除 FTC 后，瞬时可见区域（如口腔内部）的重建不完整。Figure 8 定量表明，FTC 使口腔内部高斯原语数量平均增加 **超过 400 个**（约 **17%**），有效提升了常被遮挡区域的密度。FTC 通过 FLAME 参数聚类将结构相似的帧分组（Figure 4），使 ADC 在簇内独立进行，避免瞬时可见帧的密度信号被大量常规帧淹没。

**局部分支与 VGG 损失**：去除双分支网络中的局部分支（负责眼、嘴、鼻、额头区域）或 VGG 感知损失均导致细节退化，但影响程度小于上述核心组件。

### 超参数分析

Table 1 (supp) 给出了关键超参数的消融结果。FPE 中 D-SSIM 权重 $\lambda_1=0.2$、FTC 随机训练轮数 $M=1$、聚类权重 $(0.3, 0.6, 0.1)$ 的配置在 PSNR/SSIM/LPIPS 上综合最优。偏离这些值会导致性能下降，但整体波动较小，表明方法对超参数选择具有较好的鲁棒性。

### 失败模式与局限性

尽管 STAvatar 在主流基准上表现优异，其优化式框架存在以下局限：

1. **需逐受试者训练**：与 GAGAvatar、LAM 等单图前馈式方法相比，STAvatar 需要单目视频序列和针对每个身份的单独训练，无法在单一前向传播中完成重建，限制了其在即时应用或数据稀缺场景下的适用性。
2. **推理开销**：训练完成后虽可实时渲染，但每身份的训练过程（约 6 epochs）仍存在时间成本。如何进一步压缩训练时间同时保持对瞬时区域的高保真重建，是尚未解决的问题。
3. **聚类数 K 的选择**：FTC 中的聚类数 K 目前需人工设定，其最优值可能因序列长度和表情复杂度而异。是否能以自适应方式确定 K 仍需探索。
4. **FPE 超参数的通用性**：融合感知误差中的 $\lambda_1$ 在当前任务上经消融确定，但其在其他动态场景（如全身化身、着装人体）中的通用性尚待验证。

### 补充图表

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/010_Figure_8.jpg]]
*Figure 8: Comparison of Gaussian primitive counts within the mouth interior between the vanilla training strategies and FTC*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2511_19854/figures/014_Figure_2.jpg]]
*Figure 2: Inclusion–exclusion principle*

## 方法谱系与知识库定位

### 1. 在3D头部化身重建谱系中的位置

STAvatar属于**基于3D高斯泼溅（3DGS）的可驱动头部化身重建**这一技术路线，该路线近年来由一系列工作共同推进。理解STAvatar的贡献，需要先厘清其与同谱系方法在核心设计选择上的差异。

**硬绑定范式及其局限。** 早期将3DGS引入头部化身的工作普遍采用“硬绑定”（hard binding）策略：高斯原语刚性附着于FLAME网格的三角面片上，通过线性混合蒙皮（LBS）驱动变形。代表性方法包括：

- **GaussianAvatars**（Qian et al., CVPR 2024）：将高斯体绑定到三角面片，通过面片刚体变换驱动。
- **FlashAvatar**（Xiang et al., CVPR 2024）：在参数化网格上嵌入高斯体，利用网格变形传递运动。
- **SplattingAvatar**（Shao et al., CVPR 2024）：将高斯体作为网格顶点的属性，通过顶点变换驱动。

这些方法的共同瓶颈在于：高斯体只能跟随面片做刚性运动，无法表达面部皱纹、微表情等非刚性形变（见Figure 2(a)）。此外，硬绑定使3DGS原生的自适应密度控制（ADC）难以有效运作——因为高斯体的位置梯度与面片刚性变换耦合，无法独立反映几何与纹理的重建误差。

**软绑定路线的出现。** 为突破硬绑定的限制，后续工作开始探索更灵活的绑定方式：

- **MonoGaussianAvatar**（Chen et al., SIGGRAPH 2024）：在规范空间学习每个高斯体的可变形偏移，但仍依赖全局MLP预测，缺乏UV空间的结构化先验。
- **FateAvatar**（Zhang et al., CVPR 2025）：引入可学习的逐高斯偏移，但偏移预测网络未充分利用面部结构的局部性。
- **RGAvatar**（Li et al., CVPR 2025）：通过残差图网络预测形变，在UV空间操作，但形变建模仍以网格顶点为锚点，高斯体与面片的关系未完全解耦。

STAvatar的**UV-Adaptive Soft Binding**在这一谱系中做出了关键推进：它通过双分支网络在UV空间直接预测每个高斯体的特征偏移图（见Figure 3(b)），将形变建模从“三角面片刚性绑定”提升为“UV空间可学习偏移 + 粗LBS”的两阶段框架。这一设计的核心优势在于：

1. **保留ADC兼容性**：软绑定使高斯体可以独立于面片运动，位置梯度能真实反映重建误差，从而使原生ADC策略得以有效复用。
2. **结构化先验注入**：UV空间操作天然适配面部结构的局部性——全局分支捕捉整体形变趋势，局部分支（针对眼、嘴、鼻、额头四个区域）精细建模表情相关的高频形变（见公式4-6）。
3. **非刚性形变表达**：学习到的偏移量图在头发、嘴眼等高形变区域呈现大幅值（见Supplementary Figure 4），证明网络成功捕捉了硬绑定无法表达的细粒度非刚性运动。

**密度控制策略的演进。** 在动态场景中，原生ADC存在两个被STAvatar识别并解决的关键缺陷（见Figure 2(b)(c)）：

- **瞬时可见区域欠拟合**：口腔内部等区域仅在少数帧可见，平均位置梯度低，原生ADC无法为其分配足够的高斯体。
- **位置梯度信息缺失**：位置梯度仅反映几何不一致性，无法捕捉纹理细节的欠拟合。

STAvatar提出的**Temporal ADC**策略——包含FLAME条件时间聚类（FTC）和融合感知误差（FPE-AP）——是对动态3DGS密度控制机制的直接改进。FTC将视频帧按FLAME参数结构相似性聚类为K个簇（见Figure 4），在每个簇内独立执行ADC，确保瞬时可见区域获得充分的密度增加机会。FPE-AP则用融合了L1和D-SSIM的感知误差（公式8-11）替代位置梯度作为克隆判据，同时引入峰值误差集合捕获瞬态尖峰。

### 2. 与单图泛化方法的关系

STAvatar属于**优化式**方法（per-subject optimization），需要目标受试者的单目视频序列进行单独训练。与之平行的技术路线是**前馈式单图泛化方法**，代表工作包括**GAGAvatar**和**LAM**——它们从单张图像通过单次前向传播即可生成可驱动化身。

这两种路线存在本质的适用边界差异：

| 维度 | STAvatar（优化式） | GAGAvatar / LAM（前馈式） |
|------|---------------------|---------------------------|
| 输入需求 | 单目视频序列（约数千帧） | 单张图像 |
| 推理开销 | 每受试者需完整训练（约6 epochs） | 单次前向传播 |
| 身份保真度 | 高（PSNR 30.63 on INSTA） | 较低（见Supplementary Table 2） |
| 瞬时区域重建 | FTC策略有效增强 | 受限于单图信息 |

在INSTA数据集上的定量对比（Supplementary Table 2）显示，STAvatar在PSNR、SSIM、LPIPS上均显著优于GAGAvatar和LAM，但这是以更高的计算开销为代价的。因此，STAvatar更适用于对**重建质量要求高、可接受离线训练**的场景（如影视级数字人、虚拟主播），而前馈方法更适合**即时应用**（如实时视频通话化身）。

### 3. 适用边界与局限

基于论文提供的证据和消融分析，STAvatar的适用边界可归纳如下：

**有效适用场景：**
- 单目视频输入、受试者配合录制（覆盖多表情、多视角）
- 需要高保真面部细节（皱纹、牙齿、眼睑）和瞬时区域（口腔内部）重建
- 可接受约6个epoch的per-subject训练时间
- 跨身份重现场景（Figure 6显示准确的表情传递与身份保持）

**已知局限：**
1. **优化式框架的固有限制**：需要单目视频序列和per-subject训练，无法像前馈方法那样即时生成化身。在数据稀缺（如仅有一张照片）或需要即时响应的场景下不适用。
2. **聚类超参数依赖**：FTC的聚类数K和聚类权重（0.3, 0.6, 0.1）需要人工设定（见Supplementary Table 1）。论文未提供自适应选择K的机制，不同受试者或数据集可能需要调参。
3. **感知误差权重通用性未验证**：FPE-AP中的λ1=0.2在当前任务上表现最优，但该超参数在非头部化身任务（如全身化身、通用动态场景）上的通用性未经检验。

**需要人工验证的边界：**
- 论文未报告在极端表情（如最大张口、歪嘴）或大角度侧脸下的定量表现，这些场景下软绑定的偏移预测是否稳定需要进一步确认。
- 对光照剧烈变化或遮挡严重的视频，FLAME跟踪可能失败，进而影响整个管线的初始化质量——论文未讨论这一失效模式。

### 4. 开放问题

基于STAvatar的设计选择和实验边界，以下开放问题值得后续研究关注：

1. **训练效率的进一步提升**：STAvatar在6个epoch内收敛（Figure 9），但每身份仍需完整训练。是否可以通过元学习或hypernetwork预训练软绑定网络，使新身份仅需少量微调步骤？

2. **全身化身的扩展可行性**：软绑定网络在UV空间操作，天然适配面部参数化模型（FLAME）。对于全身化身（如SMPL-X），UV空间不再连续，双分支网络的区域特定头设计如何迁移？FTC的FLAME条件聚类能否替换为更通用的姿态-形状条件聚类？

3. **自适应聚类机制**：当前FTC的聚类数K为固定超参数。是否可以利用轮廓系数或肘部法则在训练过程中自动确定最优K？或者采用层次聚类动态调整簇的粒度？

4. **感知误差权重的自适应调节**：λ1=0.2的设置在多大程度上是任务特定的？在纹理丰富区域（如头发）和纹理稀疏区域（如脸颊），最优的L1/D-SSIM混合比例可能不同——空间自适应的λ1是否值得探索？

5. **与基于NeRF的方法的深度对比**：论文主要与3DGS系方法对比，但NeRF系方法（如PointAvatar）在特定指标上仍有竞争力（PointAvatar数据集上FateAvatar的PSNR略高于STAvatar）。软绑定思想能否反向迁移到基于NeRF的化身框架中？

## 原文 PDF

![[paperPDFs/CVPR_2026/STAvatar_Soft_Binding_and_Temporal_Density_Control_for_Monocular_3D_Head_Avatars_Reconstruction.pdf]]