---
title: Physically Inspired Gaussian Splatting for HDR Novel View Synthesis
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Physically_Inspired_Gaussian_Splatting_for_HDR_Novel_View_Synthesis.pdf
project_link: "https://huimin-zeng.github.io/PhysHDR-GS/"
code_link: null
aliases:
- PG
- PIGSHNVS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将场景颜色建模为内在反射率与可调环境光照的乘积，并引入双分支：图像曝光（IE）分支调制 2D 曝光时间 t，高斯光照（GI）分支调制 3D 环境光照 L_a，通过交叉分支 HDR 一致性损失提供显式 HDR 自监督，同时利用光照引导的梯度缩放缓解极端曝光区域的梯度饥饿。
primary_logic: 物理启发的双分支机制解耦了相机曝光与环境光照，使 IE 和 GI 分支联合覆盖更宽的动态范围；交叉分支 HDR 一致性损失使 HDR 内容可直接监督，而不依赖真实 HDR 标签；光照偏差驱动的梯度放大策略防止过/欠曝区域的高斯欠分裂，从而提升细节重建。
claims:
- 跨分支 HDR 一致性损失提供了显式 HDR 监督，无需真值。
- 光照引导的梯度缩放根据光照偏差放大高斯梯度，防止极端曝光区域欠致密。
- IE 和 GI 分支联合提供互补的动态范围细节。
- HDR-NeRF-Real (LDR-OE, exp3) 上 PSNR↑ = 36.32 (Ours)
---

# Physically Inspired Gaussian Splatting for HDR Novel View Synthesis

> [!tip] 核心洞察
> 物理启发的双分支机制解耦了相机曝光与环境光照，使 IE 和 GI 分支联合覆盖更宽的动态范围；交叉分支 HDR 一致性损失使 HDR 内容可直接监督，而不依赖真实 HDR 标签；光照偏差驱动的梯度放大策略防止过/欠曝区域的高斯欠分裂，从而提升细节重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | 物理启发的 HDR 新视角合成高斯泼溅 |
| 英文题名 | Physically Inspired Gaussian Splatting for HDR Novel View Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.28020) · [Project](https://huimin-zeng.github.io/PhysHDR-GS/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PhysHDR-GS |
| Dataset | HDR-NeRF-Real, HDR-NeRF-Syn |

> [!tip] 效果简介
> - HDR-NeRF-Real (LDR-OE, exp3) 上，PSNR↑ 36.32 (Ours) vs 34.87 (HDR-GS) (+1.45 dB)；PSNR↑ 36.91 (Ours†) vs 36.32 (GaussHDR†) (+0.59 dB)。
> - HDR-NeRF-Syn (LDR-NE, exp3) 上，PSNR↑ 43.19 (Ours†) vs 42.74 (GaussHDR†) (+0.45 dB)。
> - HDR-NeRF-Syn (HDR, exp3) 上，PSNR↑ 39.21 (Ours†) vs 39.08 (GaussHDR†) (+0.13 dB)。

## 概要

HDR 新视角合成（HDR-NVS）旨在从一组不同曝光的 LDR 图像中重建场景的完整高动态范围辐射场，并支持任意曝光下的新视角渲染。该任务面临三大结构性瓶颈：**场景外观纠缠**——材质反射率与环境光照不可解耦，简单的曝光缩放无法刻画光照依赖的外观变化；**隐式 HDR 监督**——现有方法仅通过色调映射后的 LDR 图像进行约束，缺乏对 HDR 内容的直接监督信号，难以有效纠正异常 HDR 值；**曝光偏差的梯度饥饿**——色调映射曲线在过曝/欠曝区域斜率极小，导致高斯原语在这些区域的梯度微弱，密度化机制无法正常触发，形成欠致密的几何表达。

针对上述瓶颈，本文提出 **PhysHDR-GS**，一个物理启发的 HDR-NVS 框架。其核心思想是将场景颜色建模为**内在反射率**与**可调环境光照**的乘积，并引入双分支互补机制：**图像曝光（IE）分支**在 2D 图像层面调制曝光时间，**高斯光照（GI）分支**在 3D 高斯原语层面调制环境光照。两分支联合覆盖更宽的动态范围，并通过**交叉分支 HDR 一致性损失**提供显式的 HDR 自监督——无需真实 HDR 标签即可约束 HDR 内容的正确性。此外，**光照引导的梯度缩放**策略根据光照偏差自适应放大高斯梯度，有效缓解极端曝光区域的欠分裂问题，从而提升细节重建质量。

在 HDR-NeRF-Real、HDR-Plenoxels-Real 和 HDR-NeRF-Syn 三个基准上的实验表明，PhysHDR-GS 在 LDR 和 HDR 视图上均一致优于现有方法（包括 **HDR-NeRF**（Huang et al., CVPR 2022）、**HDR-GS** 和最新的 **GaussHDR**（Liu et al., CVPR 2025）），同时保持实时渲染速度（最高 76 FPS）。消融实验进一步验证了 GI 分支、HDR 一致性损失和光照引导梯度缩放各组件的独立贡献。

**方法定位**：PhysHDR-GS 属于 3D Gaussian Splatting 框架下的物理建模增强方法，通过显式的反射率-光照分解和双分支自监督机制，将 HDR-NVS 从隐式 LDR 约束推进到显式 HDR 自监督范式。

### 问题背景：HDR 新视角合成

高动态范围（HDR）新视角合成（Novel View Synthesis, NVS）的目标是从一组多曝光低动态范围（LDR）图像中重建场景的完整辐射信息，并能够渲染出任意视角、任意曝光下的高质量图像。与标准 LDR-NVS 不同，HDR-NVS 要求模型不仅恢复场景的几何结构，还要准确捕捉跨越数个数量级的光照强度变化。这一任务在计算摄影、虚拟现实和自动驾驶仿真等领域具有重要应用价值。

近年来，3D 高斯泼溅（3D Gaussian Splatting, 3DGS）以其实时渲染能力和高保真重建质量，成为 NVS 领域的主流范式。然而，将 3DGS 直接应用于 HDR 场景面临独特挑战——场景的外观由材质反射率与环境光照共同决定，且训练信号仅来自经过色调映射的 LDR 图像，缺乏对 HDR 内容的直接监督。

### 现有方法及其局限性

**NeRF 系方法**以 **HDR-NeRF**（Huang et al., CVPR 2022）为代表，通过隐式神经表示建模场景辐射场，利用多曝光 LDR 图像进行训练。这类方法在 HDR 重建质量上取得了可观进展，但受限于 NeRF 的体积渲染机制，渲染速度极慢，难以满足实时应用需求。

**3DGS 系方法**则试图将高斯泼溅的高效渲染优势引入 HDR-NVS。**HDR-GS** 首次将 3DGS 框架适配到多曝光场景，通过图像平面的曝光缩放实现 HDR-LDR 转换。最新的 **GaussHDR**（Liu et al., CVPR 2025）进一步引入双分支色调映射架构，在 LDR 域进行融合。然而，这些方法共享三个根本性瓶颈：

1. **场景外观纠缠**：现有方法将高斯原语的颜色视为单一属性，无法解耦材质反射率与环境光照。简单的曝光缩放只能实现全局亮度调整，无法刻画光照条件变化引起的局部外观改变（如高光位移、阴影变化）。如 Figure 1 所示，相机曝光变化 $\Delta t$ 产生全局的 HDR 信号缩放 $\Delta I_{\text{HDR}}$，而环境光照变化 $\Delta L_a$ 则引发局部的辐射度变化 $\Delta \hat{I}_{\text{HDR}}$——这两种响应模式揭示了互补的动态范围信息，但现有方法无法同时建模。

2. **隐式 HDR 监督**：训练过程仅通过色调映射后的 LDR 图像施加重建损失。色调映射是一个不可逆的非线性压缩过程，大量 HDR 信息在映射中丢失。由于缺乏对 HDR 内容的直接监督，模型在过曝或欠曝区域的 HDR 值估计容易出现严重偏差，表现为饱和区域的细节丢失和错误的亮度恢复（见 Figure 5、Figure 6）。

3. **曝光偏差的梯度饥饿**：色调映射曲线在过曝和欠曝区域斜率极小（见 Figure 4）。这意味着这些区域的 LDR 重建损失对高斯原语参数的梯度近乎为零，导致 3DGS 的密度化（densification）机制无法在这些区域有效分裂高斯原语，形成欠致密（under-densified）表达，最终导致纹理失真和几何缺陷。

### 核心动机与研究思路

针对上述瓶颈，PhysHDR-GS 的核心动机是：**通过物理启发的场景分解与双分支互补机制，解耦曝光与光照效应，并为 HDR 内容提供显式自监督信号**。

具体而言，该方法将场景颜色建模为**内在反射率**（intrinsic reflectance）与**可调环境光照**（adjustable ambient illumination）的乘积，并引入两个互补分支：

- **图像曝光（Image-Exposure, IE）分支**：遵循相机成像管线，在 2D 图像层面调制曝光时间 $t$，实现全局 HDR 信号缩放。
- **高斯光照（Gaussian-Illumination, GI）分支**：在 3D 高斯原语层面调制环境光照 $L_a$，通过光照调制器 $\varphi$ 产生重光照后的高斯原语，捕捉光照依赖的局部外观变化。

两个分支的 HDR 输出在物理上应保持一致——这构成了**交叉分支 HDR 一致性损失**的理论基础，使模型能够在无需真实 HDR 标签的条件下获得显式的 HDR 自监督。同时，**光照引导的梯度缩放**策略利用光照偏差自适应放大高斯梯度，缓解极端曝光区域的梯度饥饿问题，确保密度化机制的正常运作。

这种设计使 IE 和 GI 分支能够联合覆盖更宽的动态范围：IE 分支擅长恢复全局曝光信息，GI 分支则补充光照变化带来的局部细节，二者形成互补。通过这一物理启发的双分支框架，PhysHDR-GS 在保持 3DGS 实时渲染优势的同时，显著提升了 HDR 细节的重建质量。

## 核心方法与创新机理

PhysHDR-GS 的核心创新在于通过**物理启发的双分支解耦机制**，系统性地解决了 HDR 新视角合成中长期存在的三大瓶颈：场景外观纠缠、隐式 HDR 监督缺失、以及极端曝光区域的梯度饥饿问题。其关键 changed slots 如下：

### 1. 高斯颜色表征：内在反射率与可调环境光照的因子化

传统 3DGS 及其 HDR 变体（如 HDR-GS、GaussHDR）通常以球谐函数或 MLP 直接编码高斯颜色，无法显式区分材质与光照。PhysHDR-GS 将高斯颜色因子化为**内在反射率 $H_r$** 与**可调环境光照 $L_a$** 的乘积，并通过一个 MLP 辐射度组合器 $g$ 生成最终颜色：

$$\mathbf{c} = g( L_a, H_r )$$

这一因子化使场景外观的曝光响应与光照响应得以解耦，为后续双分支互补建模奠定了物理基础。

### 2. 曝光/光照调制：IE 与 GI 双分支互补架构

此前的 HDR-NVS 方法（如 HDR-NeRF、GaussHDR）仅通过图像平面的曝光缩放（IE）来覆盖动态范围，无法刻画光照依赖的局部外观变化。PhysHDR-GS 引入了**互补的双分支机制**：

- **图像曝光（IE）分支**：在 2D 图像空间对渲染的 HDR 信号施加全局曝光缩放 $t$，模拟相机曝光变化。
- **高斯光照（GI）分支**：在 3D 高斯原语层面，通过光照调制器 $\varphi$ 调整环境光照 $L_a$，生成重光照高斯并渲染出重光照 HDR 图像 $\hat{I}_{HDR}$：

$$\hat{L}_a = \varphi( L_a, l )$$

IE 分支提供全局动态范围缩放，GI 分支则实现局部辐射度重缩放以避免饱和——两者联合覆盖更宽的动态范围，这是单一分支无法达成的。

### 3. HDR 监督：交叉分支 HDR 一致性损失

现有方法仅通过色调映射后的 LDR 图像进行隐式监督，无法直接约束 HDR 内容。PhysHDR-GS 提出**交叉分支 HDR 一致性损失** $\mathcal{L}_{\mathrm{cons}}$，在 IE 与 GI 分支的 HDR 输出之间施加显式自监督：

$$\mathcal{L}_{\mathrm{cons}} = \big\| \mathcal{G}( I_{HDR} \times t ) - \mathcal{G}( \hat{I}_{HDR} ) \big\|_1$$

其中 $\mathcal{G}$ 为高斯模糊操作，用于对齐低频结构。这一设计使网络无需真实 HDR 标签即可获得显式 HDR 监督信号，直接纠正异常 HDR 值。

### 4. 梯度致密化控制：光照引导的梯度缩放（I-GS）

3DGS 的致密化依赖于屏幕空间梯度阈值 $\tau_p$，但色调映射曲线在过曝/欠曝区域斜率极小，导致这些区域的高斯梯度不足，形成欠致密表达。PhysHDR-GS 提出**光照引导的梯度缩放策略**，根据光照偏差 $\Delta L_a = |L_a - \hat{L}_a|$ 自适应放大每高斯梯度：

$$s_a = s \cdot \sigma( | L_a - \hat{L}_a | ) + 1$$

修订后的致密化判据将缩放因子 $s_a$ 纳入梯度平均，使极端曝光区域的高斯原语获得足够的梯度驱动分裂，有效防止纹理失真和细节丢失。

### 5. 色调映射器架构：交叉融合双分支 LDR

与 GaussHDR 的双分支色调映射不同，PhysHDR-GS 的色调映射器 $f$ 由两个轻量 MLP 组成：$f_{tm}$ 从 IE 和 GI 分支的 HDR 输入中分别预测全局和局部 LDR 对，$f_{mix}$ 则对这两组全局-局部对进行**交叉融合**，生成最终 LDR 结果。这一设计使两个分支的互补信息在色调映射阶段得到充分整合，进一步提升了饱和区域的细节保留能力。

---

**创新因果链总结**：因子化颜色表征（Slot 1）使场景解耦成为可能 → 双分支架构（Slot 2）分别从曝光和光照两个维度覆盖动态范围 → 交叉分支 HDR 一致性损失（Slot 3）填补了 HDR 监督的空白 → 光照引导梯度缩放（Slot 4）解决了极端曝光区域的欠致密问题 → 交叉融合色调映射器（Slot 5）整合双分支互补信息，最终形成完整的物理启发 HDR-NVS 框架。

PhysHDR-GS 的整体设计围绕一个核心物理动机展开：**场景外观由内在反射率与可调环境光照共同决定**。基于此，框架将 3D 高斯原语的颜色建模为两个可解耦因子的乘积，并构建了双分支架构来分别模拟相机曝光变化与环境光照变化对 HDR 信号的不同响应模式。

### 架构总览

如图 2 所示，PhysHDR-GS 的 pipeline 包含以下关键模块：

1. **内在反射率与环境光照分解**：每个 3D 高斯原语的颜色不再直接存储为球谐系数或 MLP 输出，而是被分解为**内在反射率** $H_r$（与视角相关的半球面反射特性）和**环境光照** $L_a$（场景级可调参数）。两者通过一个轻量 MLP **辐射度组合器** $g$ 融合为高斯颜色 $\mathbf{c} = g(L_a, H_r)$。

2. **图像曝光（IE）分支**：遵循相机成像管线，在 2D 渲染图像上对 HDR 信号施加全局曝光缩放 $t$，产生曝光调整后的 HDR 图像 $I_{HDR} \times t$。该分支模拟相机曝光时间变化对整幅图像的均匀调制。

3. **高斯光照（GI）分支**：在 3D 高斯原语层面，通过**光照调制器** $\varphi$ 将环境光照 $L_a$ 映射为虚拟光照 $\hat{L}_a = \varphi(L_a, l)$，其中 $l$ 为目标光照水平。重新着色后的高斯原语渲染出重光照 HDR 图像 $\hat{I}_{HDR}$。该分支模拟环境光照变化引起的**局部**辐射度响应——例如图 1 所示的“招财猫”铭牌区域的非均匀亮度变化。

4. **交叉融合色调映射器** $f$：由两个轻量 MLP 组成——$f_{tm}$ 对 IE 和 GI 分支的 HDR 输入分别预测全局-局部 LDR 对，$f_{mix}$ 将两组全局-局部对交叉融合为最终 LDR 输出 $I_{LDR}$（图 3）。

### 输入输出流

- **输入**：多曝光 LDR 图像集合（训练时 18 个视角，测试时 17 个视角），每张图像关联一个曝光水平。
- **训练时前向传播**：
  1. 从当前视角渲染 HDR 图像 $I_{HDR}$；
  2. IE 分支对 $I_{HDR}$ 施加曝光 $t$，GI 分支通过 $\varphi$ 调制 $L_a$ 后渲染 $\hat{I}_{HDR}$；
  3. 两个 HDR 信号送入色调映射器 $f$ 生成 LDR 预测；
  4. 计算 LDR 重建损失 $\mathcal{L}_{rec}$ 与交叉分支 HDR 一致性损失 $\mathcal{L}_{cons}$。
- **训练时梯度回传**：在 3DGS 的密度化阶段，根据光照偏差 $\Delta L_a = |L_a - \hat{L}_a|$ 计算缩放因子 $s_a = s \cdot \sigma(\Delta L_a) + 1$，对每高斯的屏幕空间梯度进行放大后再执行密度化判定，以缓解过曝/欠曝区域的梯度饥饿。
- **推理时**：给定目标曝光水平，IE 和 GI 分支联合生成 HDR 信号，经 $f$ 映射为 LDR 新视角图像，渲染速度可达 76 FPS（400×400 分辨率，单张 NVIDIA A6000）。

### 双分支互补机制

IE 分支和 GI 分支覆盖动态范围的方式本质不同（图 1）：曝光变化 $\Delta t$ 引起 HDR 信号的**全局缩放** $\Delta I_{HDR}$，而光照变化 $\Delta L_a$ 引起**局部辐射度变化** $\Delta \hat{I}_{HDR}$。这种互补性使双分支能够联合覆盖更宽的动态范围——IE 分支擅长处理全局亮度调整，GI 分支擅长捕捉光照依赖的局部外观细节（如高光反射、阴影纹理），两者结合避免了单一分支在极端曝光区域的饱和与信息丢失。

![[assets/figures/papers/paper_list_l2568_https_arxiv_org_abs_2603_28020/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed PhysHDR-GS, where Gaussian color is modeled from intrinsic reflectance and ambient illumination. The image–exposure (IE) branch modulates exposure t on 2D images, while the Gaussian–illumination (GI) branch modulates ambient illumination*

PhysHDR-GS 的核心设计围绕三个瓶颈展开：场景外观纠缠、隐式 HDR 监督缺失、以及极端曝光区域的梯度饥饿。以下按模块拆解其因果机制与关键公式。

### 高斯颜色分解：内在反射率与可调环境光照

传统 3DGS 将高斯原语的颜色直接建模为球谐系数或 MLP 输出，无法区分材质与光照。PhysHDR-GS 将每个高斯原语的颜色分解为**内在反射率** $H_r$ 与**可调环境光照** $L_a$ 的乘积，并由一个轻量 MLP **辐射度组合器** $g$ 合成最终颜色：

$$\mathbf{c} = g(L_a, H_r)$$

其中 $H_r$ 是视角相关的半球面反射率，$L_a$ 是场景级环境光照参数。这一分解使得后续可以通过独立调节 $L_a$ 来模拟光照变化，而无需改变材质属性。

### 双分支架构：图像曝光（IE）与高斯光照（GI）

PhysHDR-GS 引入两个互补分支，分别从 2D 图像层面和 3D 高斯层面调制动态范围：

- **IE 分支**：遵循相机成像管线，对渲染得到的 HDR 图像 $I_{HDR}$ 施加全局曝光缩放 $t$，得到 $I_{HDR} \times t$。这模拟了相机曝光时间变化引起的全局亮度调整。
- **GI 分支**：通过**光照调制器** $\varphi$ 对每个高斯的 $L_a$ 进行重照明，产生虚拟光照 $\hat{L}_a$：

$$\hat{L}_a = \varphi(L_a, l)$$

其中 $l$ 为目标光照水平。重照明后的高斯集合 $\hat{G}_{HDR}^{3D}$ 经泼溅渲染得到重照明 HDR 图像 $\hat{I}_{HDR}$。

两分支的 LDR 像素形成过程可统一为广义形式：

$$I_{LDR}(\mathbf{p}; t, L_a) = f\big(t \cdot g(L_a(\mathbf{x}), H_r(\mathbf{x}, \omega_o))\big)$$

其中 $f$ 为色调映射函数（相机响应函数的可学习近似）。

### 交叉融合色调映射器

色调映射器 $f$ 由两个轻量 MLP 组成：

- **$f_{tm}$**：对 IE 和 GI 分支的 HDR 输入分别预测全局和局部 LDR 输出对。
- **$f_{mix}$**：将两组全局-局部 LDR 对进行交叉融合，产生最终 LDR 结果。

这种设计使得两分支的信息可以在 LDR 域互补融合，而非简单叠加。

### 交叉分支 HDR 一致性损失

由于训练时仅有色调映射后的 LDR 监督，HDR 内容缺乏直接约束。PhysHDR-GS 利用 IE 和 GI 分支输出之间的内在一致性，构建显式 HDR 自监督：

$$\mathcal{L}_{\mathrm{cons}} = \big\| \mathcal{G}(I_{HDR} \times t) - \mathcal{G}(\hat{I}_{HDR}) \big\|_1$$

其中 $\mathcal{G}$ 为高斯模糊算子，用于对齐两分支的低频结构，避免高频差异导致的错误惩罚。该损失使 HDR 内容在无需真值的情况下获得有效监督。

### 光照引导的梯度缩放（I-GS）

色调映射曲线在过曝/欠曝区域斜率极小（Figure 4），导致这些区域的高斯原语梯度微弱，无法触发密度化，形成欠致密表达。PhysHDR-GS 根据每个高斯的光照偏差 $\Delta L_a = |L_a - \hat{L}_a|$ 自适应放大其梯度：

$$s_a = s \cdot \sigma(|L_a - \hat{L}_a|) + 1$$

其中 $\sigma$ 为 sigmoid 函数，$s$ 为缩放强度超参数。修正后的密度化判据为：

$$\mathbb{I}_i(s_a) \frac{1}{M_i} \sum_{k=1}^{M_i} \Big\| \frac{\partial \mathcal{L}_k}{\partial \pmb{\mu}_{i,k}^{\mathrm{ndc}}} \Big\|_2 > \tau_p$$

其中 $\mathbb{I}_i(s_a)$ 为缩放因子 $s_a$ 的指示函数，$M_i$ 为可见视图数，$\tau_p$ 为密度化阈值。光照偏差越大（即过曝/欠曝越严重），梯度被放大越多，从而补偿梯度饥饿，确保极端曝光区域也能充分分裂。

### 总训练损失

$$\mathcal{L}_{\mathrm{total}} = \lambda_1 \mathcal{L}_{\mathrm{rec}} + \lambda_2 \mathcal{L}_{\mathrm{cons}} + \lambda_3 \mathcal{L}_{\mathrm{unit}}$$

其中 $\mathcal{L}_{\mathrm{rec}}$ 为 LDR 重建损失，$\mathcal{L}_{\mathrm{cons}}$ 为 HDR 一致性损失，$\mathcal{L}_{\mathrm{unit}}$ 为可选的均匀曝光正则化（仅用于合成数据集）。实际训练中 $\lambda_1=1$，$\lambda_2=0.5$，$\lambda_3$ 在真实场景为 0、合成场景为 0.5。

**因果链条总结**：高斯颜色分解（解耦材质与光照）→ 双分支架构（IE 覆盖全局曝光、GI 覆盖局部光照）→ 交叉分支 HDR 一致性（显式 HDR 自监督）→ 光照引导梯度缩放（补偿极端曝光梯度饥饿）。四个模块形成闭环，共同突破 HDR-NVS 的三大瓶颈。

## 实验与关键发现

### 核心瓶颈与因果机制回顾

PhysHDR-GS 针对 HDR-NVS 的三重瓶颈设计了因果干预：场景外观纠缠（材质与光照无法解耦）、隐式 HDR 监督（仅通过色调映射后的 LDR 约束）、以及曝光偏差的梯度饥饿（色调映射曲线在过/欠曝区域斜率极小，导致高斯原语梯度不足、欠致密）。其核心机制是将高斯颜色分解为内在反射率 $H_r$ 与可调环境光照 $L_a$，引入图像曝光（IE）分支与高斯光照（GI）分支联合覆盖更宽动态范围，并通过交叉分支 HDR 一致性损失提供显式 HDR 自监督，同时以光照引导的梯度缩放（I-GS）缓解极端曝光区域的梯度饥饿。

### 主结果：与基线方法的定量对比

**Table 1** 报告了在真实数据集 HDR-NeRF-Real 和 HDR-Plenoxels-Real 上的全面对比。在 HDR-NeRF-Real 的 LDR-OE（exp3）设定下，PhysHDR-GS 取得 PSNR 36.32 dB，较 HDR-GS 提升 +1.45 dB；其 Scaffold-GS 变体（PhysHDR-GS†）进一步达到 36.91 dB，较同期最强基线 GaussHDR†（Liu et al., CVPR 2025）提升 +0.59 dB。在 LDR-NE 设定下，PhysHDR-GS† 以 34.15 dB 同样取得最优。

**Table 2** 展示了合成数据集 HDR-NeRF-Syn 上的结果。在 LDR-NE（exp3）设定下，PhysHDR-GS† 以 43.19 dB 领先 GaussHDR† 的 42.74 dB（+0.45 dB）；在 HDR 指标上，PhysHDR-GS† 达到 39.21 dB，略优于 GaussHDR† 的 39.08 dB（+0.13 dB）。值得注意的是，HDR 真值仅用于评估，任何方法在训练期间均不可见——PhysHDR-GS 的 HDR 优势完全来自交叉分支一致性损失提供的自监督信号。

**Table 3** 的效率分析显示，PhysHDR-GS 在单张 NVIDIA A6000 GPU 上以 400×400 分辨率达到 76 FPS 的实时渲染吞吐量，在保持高质量重建的同时继承了 3DGS 的实时渲染优势。

### 定性分析：饱和区域细节保留与光照估计

**Figure 5** 展示了 LDR 视图上的定性对比与残差图。竞争方法在饱和区域出现明显的内容缺失（如第一行屏幕反射），表明色调映射后信息丢失；而 PhysHDR-GS 有效保留了精细结构和细节。**Figure 6** 进一步展示了 HDR 视图对比：HDR-NeRF 和 HDR-GS 因训练中缺乏 HDR 监督，难以复现正确的光照水平，导致亮度不准和细节丢失；PhysHDR-GS 通过交叉分支 HDR 一致性损失，忠实估计了场景光照并重建了精细结构（如第一行篮子边缘）。

### 消融实验：各组件的定量贡献

**Table 4** 系统验证了 GI 分支、HDR 一致性损失（HDR-cons）和 I-GS 三个组件的贡献。以仅含 IE 分支的模型为基线：

- **添加 GI 分支**：在 HDR-NeRF-Real LDR-OE 上带来 +0.57 dB 的显著提升，验证了双分支联合覆盖更宽动态范围的核心假设。
- **启用 HDR 一致性损失**：在 GI 分支基础上进一步带来 +0.14 dB 增益，证明显式 HDR 自监督的有效性。
- **引入 I-GS**：带来最大幅度的提升——在 HDR-NeRF-Real 上高达 +0.48 dB，在 HDR-Plenoxels-Real 上 +0.31 dB，证实了光照偏差驱动的梯度放大策略对缓解欠致密问题的关键作用。

**Figure 7** 通过残差图可视化了消融的定性效果：逐步加入 GI 分支有效捕捉了光照依赖的外观变化（如第一行桌面反射），减少颜色失真；引入 HDR-cons 和 I-GS 进一步细化了结构细节。I-GS 特别有效地减少了阴影区域的纹理失真，通过防止高斯原语在过/欠曝区域的欠分裂来实现（**Figure 7** 与 Sec. 5.5 的分析一致）。

### 梯度饥饿的机制验证

**Figure 4** 提供了梯度饥饿问题的定量分析依据：过/欠曝像素位于色调映射曲线的平坦区域，产生极小的梯度；实验观察到梯度大小与光照偏差的倒数 $1/\Delta L_a$ 呈正相关。这直接支撑了 I-GS 的设计动机——基于光照偏差 $|L_a - \hat{L}_a|$ 自适应放大梯度，使极端曝光区域的高斯原语获得足够的密度化信号。

### 失败模式与局限性

尽管 PhysHDR-GS 在多个基准上取得最优，仍存在以下限制：

1. **多曝光依赖**：框架需要多曝光输入，无法直接从单曝光 LDR 图像进行 HDR 重建。
2. **低光照噪声场景的漂浮物**：在低光照、高噪声的 LDR 视图中，仍可能出现漂浮物（floaters），需要额外的噪声先验正则化或更强的几何骨架（如 Scaffold-GS）来抑制。
3. **数据集覆盖有限**：仅在三种中等规模数据集上验证，尚未在大规模、高动态范围的野外场景中测试。
4. **均匀光照假设**：光照调制器 $\varphi$ 仅模拟均匀环境光照变化，无法处理复杂的方向性光照或重光照任务。

### 公平性说明

所有方法在相同的多曝光划分（训练 18/27 视图，测试 17/13 视图）下训练和评估，曝光设定（exp3、exp1）遵循 GaussHDR 协议。HDR 真值仅用于评估，训练期间任何方法均不可见。同时测试了 vanilla 3DGS 和 Scaffold-GS 两种骨干，Scaffold-GS 变体以 † 标记。

![[assets/figures/papers/paper_list_l2568_https_arxiv_org_abs_2603_28020/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on realistic HDR-NeRF-Real [12] and HDR-Plenoxels-Real [15] datasets, where the best and second-best results are highlighted in red and yellow , respectively. † indicates variants built on Scaffold-GS [27]. The proposed method achieves the overall best performance, demonstrating its effectiveness in synthesizing high-quality novel views across different exposure levels*

![[assets/figures/papers/paper_list_l2568_https_arxiv_org_abs_2603_28020/figures/006_Table_2.jpg]]
*Table 2: Quantitative results on the synthetic HDR-NeRF-Syn [12] dataset, where the best and second-best results are highlighted in red and yellow , respectively. † indicates variants built on Scaffold-GS [27]. Our method consistently outperforms baselines on both LDR and HDR scenarios, demonstrating its effectiveness in reconstructing HDR details and preserving information during tonemapping*

![[assets/figures/papers/paper_list_l2568_https_arxiv_org_abs_2603_28020/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative comparisons on LDR views. For each method, we show the reconstructed LDR image and the residual map w.r.t. the ground truth. Competing methods exhibit noticeable missing content in saturated regions (e.g., screen reflections in the 1st row), indicating information loss after tone mapping, whereas our method effectively preserves fine structures and details*

![[assets/figures/papers/paper_list_l2568_https_arxiv_org_abs_2603_28020/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparisons on HDR views, where we include residual maps between the results and GT to highlight the difference. HDR-NeRF and HDR-GS struggle to reproduce correct illumination levels due to the absence of HDR supervision during training, leading to inaccurate brightness and lost details. By imposing cross-branch HDR consistency, our method faithfully estimates scene lighting and reconstructs fine structures (e.g., basket edges in the 1st row)*

![[assets/figures/papers/paper_list_l2568_https_arxiv_org_abs_2603_28020/figures/011_Table_4.jpg]]
*Table 4: Ablation studies on HDR-NeRF-Real and HDR-Plenoxels-Real dataset, with the best and second-best results highlighted in red and yellow . IE branch indicates the baseline containing only the image-exposure branch. GI branch, HDR-cons and I-GS denote Gaussian-illumination branch, self-consistent HDR learning and illumination-guided gradient scaling, respectively*

## 定位与知识库关联

### 1. 方法谱系：从 NeRF 到 3DGS 的 HDR-NVS 演进

PhysHDR-GS 处于 HDR 新视角合成（HDR-NVS）从隐式神经表示向显式高斯泼溅（3DGS）过渡的关键节点，其核心贡献在于将物理启发的场景解耦引入 3DGS 框架。

**前身一：NeRF-based HDR 重建。** 早期工作以 **HDR-NeRF**（Huang et al., CVPR 2022）为代表，在 NeRF 框架内引入曝光条件的光线采样与色调映射，首次实现了从多曝光 LDR 图像重建 HDR 辐射场。然而，这类方法受限于 NeRF 的体积渲染开销，无法达到实时渲染，且其隐式表示难以显式建模材质与光照的纠缠关系。

**前身二：3DGS-based HDR 重建。** 3DGS 的实时渲染能力催生了 HDR-NVS 的显式化尝试。**HDR-GS** 将曝光调制引入 3DGS 的颜色表示，但仅通过图像平面的曝光缩放（IE-only）来模拟动态范围变化，缺乏对场景光照的显式建模。**GaussHDR**（Liu et al., CVPR 2025）进一步引入双分支色调映射，但仍依赖隐式的 LDR 监督，HDR 内容缺乏直接约束。

**PhysHDR-GS 的突破点。** 本文在上述谱系中完成了三个关键跨越：

1. **从曝光缩放到光照解耦**：将高斯颜色因式分解为内在反射率 $H_r$ 与可调环境光照 $L_a$，使得场景外观变化可归因于物理上不同的机制（相机曝光 vs. 场景光照），而非简单的像素级缩放。
2. **从隐式到显式 HDR 监督**：通过 IE 与 GI 双分支间的交叉分支 HDR 一致性损失 $\mathcal{L}_{\mathrm{cons}}$，首次在无真值条件下对 HDR 内容提供显式自监督信号。
3. **从固定到自适应梯度控制**：光照引导的梯度缩放策略 $s_a$ 根据光照偏差放大过/欠曝区域的高斯梯度，解决了 3DGS 原生致密化在极端曝光区域的梯度饥饿问题。

### 2. 与同期/后续工作的关系

**与 GaussHDR 的对比。** GaussHDR（Liu et al., CVPR 2025）是 PhysHDR-GS 最直接的同期基线。两者均采用双分支架构，但存在本质差异：

| 维度 | GaussHDR | PhysHDR-GS |
|------|----------|------------|
| 场景建模 | 双分支色调映射，无显式物理分解 | 反射率-光照因子分解，物理可解释 |
| HDR 监督 | 隐式（仅 LDR 重建损失） | 显式（交叉分支 HDR 一致性损失） |
| 梯度控制 | 无特殊处理 | 光照引导梯度缩放 |
| 色调映射 | 双分支融合 | 交叉融合 $f_{tm} + f_{mix}$ |

在 Scaffold-GS 骨干下，PhysHDR-GS† 在 HDR-NeRF-Real 的 LDR-OE/exp3 上相较 GaussHDR† 提升 0.59 dB PSNR，在 HDR-NeRF-Syn 的 LDR-NE/exp3 上提升 0.45 dB，验证了物理解耦与显式 HDR 监督的增益。

**与其他 3DGS 变体的兼容性。** PhysHDR-GS 的物理分解模块（$g(L_a, H_r)$、$\varphi(L_a, l)$）与 3DGS 骨干解耦，可即插即用于 Scaffold-GS 等增强几何骨架。论文已验证 Scaffold-GS 变体（†）在多个基准上持续优于对应的 GaussHDR†，表明该框架具有良好的扩展性。

### 3. 适用边界与局限

**输入依赖性。** PhysHDR-GS 需要多曝光 LDR 图像作为训练输入，无法从单曝光图像进行 HDR 重建。这限制了其在缺乏多曝光数据的场景（如野外单张照片）中的应用。

**光照建模的简化假设。** 光照调制器 $\varphi$ 仅模拟均匀环境光照变化 $\hat{L}_a = \varphi(L_a, l)$，无法处理：
- 方向性光照（如点光源、平行光）
- 复杂的光源遮挡与间接光照
- 重光照任务中的任意光照条件编辑

因此，该方法本质上是一个“曝光-光照联合估计”框架，而非完整的逆向渲染管线。

**噪声鲁棒性。** 在低光照、高噪声的 LDR 视图中，仍可能出现漂浮物（floaters）。论文指出需要额外的噪声先验正则化或更强的几何骨架（如 Scaffold-GS）来抑制，但未给出具体的噪声建模方案。

**数据集覆盖范围。** 当前验证仅限于三个中等规模数据集（HDR-NeRF-Real、HDR-Plenoxels-Real、HDR-NeRF-Syn），尚未在大规模、高动态范围的野外场景（如夜景街拍、强逆光室外）中测试泛化能力。

### 4. 开放问题

1. **单曝光/动态光照扩展**：如何将该框架扩展到单曝光输入或动态光照场景？可能的路径包括引入光照先验网络或与时序一致性约束结合。

2. **噪声先验引导的正则化**：论文提及但未实现的噪声先验正则化具体如何设计？其在极端噪声条件下的鲁棒性如何？这是从受控数据集走向真实应用的关键一步。

3. **与先进 3DGS 变体的深度结合**：能否将物理分解模块与 2DGS、Mip-Splatting 等改进的几何表示结合，进一步提升薄结构和高频细节的重建质量？

4. **HDR 自监督的可靠性边界**：交叉分支 HDR 一致性损失 $\mathcal{L}_{\mathrm{cons}}$ 依赖亮度匹配，当 IE 与 GI 分支的光照差异极大（如极端欠曝与过曝配对）时，模糊后的 L1 匹配是否仍能提供可靠的自监督信号？是否需要引入感知损失或结构相似性约束作为补充？

5. **从 HDR 重建到 HDR 编辑**：当前框架已实现反射率与光照的初步解耦，是否可进一步发展为支持材质编辑、重光照的完整逆向渲染管线？这需要更精细的 BRDF 建模和光源估计能力。

## 原文 PDF

![[paperPDFs/CVPR_2026/Physically_Inspired_Gaussian_Splatting_for_HDR_Novel_View_Synthesis.pdf]]
