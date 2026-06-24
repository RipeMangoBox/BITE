---
title: "PhyGaP: Physically-Grounded Gaussians with Polarization Cues"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PhyGaP_Physically_Grounded_Gaussians_with_Polarization_Cues.pdf
project_link: null
code_link: "https://mitsuba-renderer.org"
aliases:
- PhyGaP
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 引入偏振成像及其物理模型（pBRDF），为表面法线、折射率、粗糙度等物理属性的优化提供额外的监督信号。
primary_logic: 偏振反射包含镜面与漫反射的固有偏振差异，通过建立偏振化延迟渲染（PolarDR）过程，可以利用偏振线索显式解耦物体外观，实现物理正确的逆向渲染与重光照。
claims:
- 消融实验表明，移除PolarDR会导致环境图PSNR大幅下降（Table 2），反照率中混入镜面反射，环境图平滑度降低（Fig. 9）。
- 定量对比中，PhyGaP在多个场景上的PSNR和Cosine Distance整体优于仅依赖RGB的基线方法和PolGS（Table 1）。
- GridMap消融显示，移除后非凸物体的阴影无法被正确处理，反照率出现颜色偏移（Fig. 9, Table 2）。
- 在david场景的重光照测试中，PhyGaP的PSNR达到19.18，SSIM 0.973，LPIPS 0.0255，明显优于仅RGB方法（Table 2）。
---

# PhyGaP: Physically-Grounded Gaussians with Polarization Cues

> [!tip] 核心洞察
> 偏振反射包含镜面与漫反射的固有偏振差异，通过建立偏振化延迟渲染（PolarDR）过程，可以利用偏振线索显式解耦物体外观，实现物理正确的逆向渲染与重光照。

| 字段 | 内容 |
|------|------|
| 中文题名 | PhyGaP：结合偏振线索的物理约束高斯泼溅 |
| 英文题名 | PhyGaP: Physically-Grounded Gaussians with Polarization Cues |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.14001) · [Code](https://mitsuba-renderer.org) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | PhyGaP |
| Dataset | PANDORA, Mitsuba3, SMVP (david) - Relighting |

> [!tip] 效果简介
> - PANDORA (owl) 上，PSNR↑ (dB) 28.14 vs Ref-Gaussian: 22.39 (+5.75 dB)。
> - Mitsuba3 (teapot) 上，Cosine Distance↓ 0.0079 vs Ref-Gaussian: 0.0093 (-0.0014 (改善15%))。
> - SMVP (david) - Relighting 上，PSNR↑ 19.18 vs GS-IR: 16.90 (+2.28 dB)。

## 概述

从单目或多视角RGB图像重建物体外观并支持重光照，是计算机视觉与图形学中的核心难题。其瓶颈在于：**普通RGB图像缺乏足够的表面形状与材质信息，导致现有方法难以正确解耦反照率与反射分量**，从而无法实现高保真的逆向渲染。PhyGaP 针对这一瓶颈，引入**偏振成像及其物理模型（pBRDF）**作为额外的监督信号，为表面法线、折射率、粗糙度等物理属性的优化提供关键约束。

PhyGaP 的核心洞察是：**偏振反射中镜面与漫反射具有固有的偏振差异**。通过建立“偏振化延迟渲染”（PolarDR）过程，该方法能够利用偏振线索显式解耦物体外观，实现物理正确的逆向渲染与重光照。此外，针对非凸物体的间接光照建模难题，PhyGaP 提出 **GridMap** 技术——一种基于包围盒锚定相机的局部立方体贴图插值方案，无需学习场景特定参数即可处理自遮挡阴影。

在方法谱系上，PhyGaP 属于**物理约束的3D高斯泼溅（3DGS）方法**，以 2DGS 为几何骨干，在渲染过程、间接光照建模和高斯属性三个关键槽位上对基线方法（如 Ref-Gaussian）进行了实质性改进：将标准延迟渲染替换为 PolarDR；将球谐（SH）间接光照替换为 GridMap；将高斯属性从反照率/金属度/粗糙度/SH颜色替换为反照率/折射率/法线/粗糙度，并利用物理BRDF直接计算颜色。

实验证据表明，PhyGaP 在多项指标上整体优于仅依赖RGB的基线方法（如 R3DG、GS-IR、GIR、3DGS-DR、Ref-Gaussian）以及偏振辅助方法 PolGS（Table 1）。消融实验进一步验证了关键设计的因果效应：移除 PolarDR 会导致环境图 PSNR 大幅下降，反照率中混入镜面反射（Table 2, Fig. 9）；移除 GridMap 则使非凸物体的阴影无法正确处理，反照率出现颜色偏移。在 david 场景的重光照测试中，PhyGaP 的 PSNR 达到 19.18 dB，SSIM 0.973，LPIPS 0.0255，明显优于仅RGB方法（Table 2）。

**局限性方面**，GridMap 依赖包围盒放置锚定相机，在极端自遮挡或极薄/深凹物体上可能失效（Fig. 15）；当前 pBRDF 模型未支持金属表面；GridMap 仅模拟单次弹射的间接光照，无法处理多次互反射。此外，设备要求较高，理想情况需偏振相机或两台配有线性偏振片的RGB相机，标定与拍摄流程相对复杂。

## 背景与动机

真实世界物体的外观由复杂的物理过程共同决定：表面几何、材质属性（反照率、粗糙度、折射率）以及环境光照三者耦合，共同产生我们最终观察到的颜色。从一组二维图像中逆向解耦这些因素——即逆向渲染——是计算机视觉与图形学中长期存在的核心挑战。成功解耦不仅能实现任意光照下的真实感重光照，还可支持材质编辑、虚拟物体插入等下游应用。

近年来，以3D高斯泼溅（3DGS）为代表的神经渲染方法在新视角合成上取得了显著进展，部分工作开始尝试在GS框架中引入物理光照模型以实现反射分解与重光照。然而，这些基于普通RGB图像的方法面临一个根本性瓶颈：**RGB三通道仅记录了总辐射强度，缺乏足够的表面形状与材质信息，导致反照率与镜面反射分量难以正确解耦**。具体而言，镜面高光容易被误认为浅色反照率，而漫反射中的阴影细节则可能在分解过程中丢失，最终损害重光照的物理真实感。

与此同时，偏振成像为这一困境提供了潜在的突破口。光在反射时，其偏振状态会根据表面法线方向、材质折射率和粗糙度发生可预测的变化——镜面反射与漫反射具有截然不同的偏振特性。这一物理规律意味着，**偏振信息可以作为额外的监督信号，显式地约束表面属性与反射分量的优化过程**。然而，现有偏振辅助的重建方法（如基于NeRF的PANDORA、NeRSP以及基于GS的PolGS）要么无法实现反射分解与重光照，要么缺乏对间接光照的有效建模，在处理非凸物体时表现不佳。

另一个关键缺口在于间接光照的建模方式。现有GS逆向渲染方法通常为每个高斯原语学习一组球谐（SH）系数来表示间接光。这种场景特定参数的学习策略存在明显局限：SH系数与训练光照强耦合，难以泛化到新光照条件；更重要的是，它无法正确处理非凸物体的自遮挡阴影，因为单个高斯无法感知来自其他表面区域的遮挡关系。

针对上述问题，本文提出PhyGaP，核心动机在于：**利用偏振线索提供的物理约束，在2DGS框架内实现精确的表面属性估计与反射分解，并通过一种无需学习场景特定参数的间接光照建模方案，将重光照能力扩展到非凸物体**。PhyGaP的偏振化延迟渲染（PolarDR）过程将偏振物理模型（pBRDF）深度嵌入GS渲染管线，使Stokes矢量的计算直接依赖于表面法线、折射率和粗糙度等物理属性，从而在优化过程中形成强约束。同时，GridMap技术通过在物体包围盒上锚定虚拟相机并构建局部立方体贴图，以插值方式计算任意表面点的漫反射辐照度，避免了对场景特定参数的依赖，并自然地捕捉了自遮挡效应。

## 核心创新

PhyGaP 的核心创新在于将**偏振成像的物理模型**与**3D高斯泼溅（3DGS）**深度融合，解决了普通RGB图像在表面形状与材质解耦上的信息不足问题。其关键设计围绕两个“changed slots”展开：**偏振化延迟渲染（PolarDR）**和**自遮挡感知的GridMap环境光照**，并辅以高斯属性的物理化重构。

### 1. 偏振化延迟渲染（PolarDR）

标准延迟渲染（DR）仅输出RGB颜色，缺乏对镜面反射与漫反射的显式区分能力。PhyGaP提出的**PolarDR**过程将渲染方程扩展为偏振形式，利用**pBRDF模型**计算每个像素的**Stokes矢量**，从而为优化提供额外的偏振监督信号。

- **物理属性替代颜色SH**：与Ref-Gaussian等基线方法不同，PhyGaP移除高斯的颜色球谐（SH）系数，改为学习物理属性——反照率 $\lambda$、折射率 $\eta$ (IoR)、法线 $\mathbf{n}$ 和粗糙度 $r$。颜色通过物理BRDF直接计算，使外观分解具有物理可解释性。
- **镜面与漫反射的偏振解耦**：镜面反射的偏振程度（由 $\beta_s(\theta_{\mathbf{n}})$ 调控）远强于漫反射（由 $\beta_d(\theta_{\mathbf{n}})$ 调控）。PolarDR利用这一固有差异，显式分离镜面Stokes矢量 $S_{\omega_o}^s$ 和漫反射Stokes矢量 $S_{\omega_o}^d$（Eq. 7–8），从而在训练中迫使网络正确解耦反照率与反射分量。

### 2. GridMap：自遮挡感知的局部环境光照

现有方法（如Ref-Gaussian）为每个高斯学习一组SH系数来表示间接光照，这不仅引入了场景特定参数，还难以处理非凸物体的自遮挡。PhyGaP的**GridMap**技术通过以下机制解决该问题：

- **锚定相机与局部立方体贴图**：在物体包围盒的每个面划分3×3网格，放置锚定相机。每个锚定相机向所有方向进行光线追踪，将物体颜色与全局环境图混合，构建局部立方体贴图 $\tilde{E}_i$。
- **距离加权插值**：对于表面点 $\mathbf{p}$，通过距离加权平均多个锚定相机的局部漫反射Stokes矢量 $\tilde{S}_d^{(i)}$（Eq. 9），实现平滑、自遮挡感知的间接光照计算。该过程**不学习任何场景特定参数**，因此具备更强的泛化能力。

### 3. 高斯属性的物理化重构

PhyGaP将高斯的可学习属性从“颜色SH + 金属度/粗糙度”替换为“反照率 + 折射率 + 法线 + 粗糙度”。这一改变使得：
- 外观分解结果（反照率、漫反射、镜面反射）直接从物理属性导出，而非从SH系数中后验分离。
- 法线由2DGS的显式几何提供，并通过深度-法线一致性损失 $\mathcal{L}_{\mathrm{depth}}$ 和边缘感知平滑损失 $\mathcal{L}_{\mathrm{smooth}}$ 进行正则化（Eq. 10），确保了几何与材质的协同优化。

### 创新点的因果链条

偏振线索的引入（因果旋钮）→ PolarDR提供镜面/漫反射的偏振差异监督 → 物理属性（$\lambda, \eta, \mathbf{n}, r$）被正确优化 → GridMap处理非凸物体的自遮挡 → 最终实现物理正确的反照率-反射解耦与高保真重光照。消融实验证实了这一链条：移除PolarDR（设 $\lambda_1=0$）后，反照率中残留镜面反射，环境图PSNR大幅下降（Table 2）；移除GridMap后，非凸物体的阴影无法正确处理，反照率出现颜色偏移（Fig. 9）。

## 整体框架

PhyGaP 的整体流程如 **Figure 2** 所示，它建立在 2D 高斯泼溅（2DGS）的几何表示之上，通过两个核心改进——**偏振化延迟渲染（PolarDR）** 和 **GridMap 间接光照建模**——将物理属性与偏振线索深度耦合，实现从多视角偏振图像到可重光照外观的端到端优化。

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the PhyGaP pipeline. We represent physically-grounded attributes such as roughness, albedo, IoR and surface normal with 2DGS, and render them into Stokes values via the PolarDR process. Furthermore, we design the GridMap technique to tackle self-occlusion of nonconvex objects. By utilizing polarization cues, we achieve accurate, explicit and disentangled representation of object albedo, diffuse reflection and specular reflection in PhyGaP*

### 输入与输出

**输入**：一组已标定的多视角图像，每视角包含 RGB 图像和对应的偏振信息（全偏振或部分偏振）。真实数据采用 COLMAP 估计相机位姿，合成数据使用已知位姿。

**输出**：场景的显式物理属性分解，包括：
- 逐像素的反照率（albedo）、漫反射分量、镜面反射分量
- 环境光照图（environment map）
- 表面法线图
- 物理属性图（粗糙度、折射率 IoR）
- 支持任意新环境光照下的重光照渲染

### 核心模块关系

PhyGaP 的 pipeline 由四个关键模块串联构成：

**1. 2DGS Backbone（几何表示层）**  
基于 2D 高斯泼溅（Huang et al.，SIGGRAPH 2024）提供显式的表面几何。每个 2D 高斯原语由中心点 $\mathbf{p}$、切向量 $\mathbf{t}_u, \mathbf{t}_v$ 和缩放因子 $s_u, s_v$ 定义，通过局部切平面坐标 $(u,v)$ 到世界坐标的映射
$$P(u,v) = \mathbf{p} + s_u \mathbf{t_u} \cdot u + s_v \mathbf{t_v} \cdot v = \mathbf{H} \cdot [u, v, 1, 1]^T$$
建立参数化表面。该表示天然提供显式法线和深度，为后续物理渲染提供几何基础。

**2. PolarDR（物理属性渲染层）**  
这是 PhyGaP 的核心创新。与 Ref-Gaussian 等基线方法为每个高斯学习球谐（SH）系数表示颜色的做法不同，PolarDR 将每个 2D 高斯原语的属性替换为物理参数：反照率 $\lambda$、折射率 $\eta$（IoR）、法线 $\mathbf{n}$ 和粗糙度 $r$。这些属性通过光栅化 splat 到材质图（material maps）上，随后利用偏振双向反射分布函数（pBRDF）计算每个像素的 Stokes 矢量：
- 镜面反射偏振：$S_{\omega_o}^s = [ \beta_s(\theta_{\mathbf{n}}) \cos 2\phi_{\mathbf{n}} ] L_s(\omega_o) , -\beta_s(\theta_{\mathbf{n}}) \sin 2\phi_{\mathbf{n}} ]$
- 漫反射偏振：$S_{\omega_o}^d = [ \beta_d(\theta_{\mathbf{n}}) \cos 2\phi_{\mathbf{n}} ] L_d(\omega_o) , -\beta_d(\theta_{\mathbf{n}}) \sin 2\phi_{\mathbf{n}} ]$

这种设计使得偏振线索可以直接监督物理属性的优化，从根本上解耦反照率与反射分量。

**3. GridMap（自遮挡感知的环境光照层）**  
针对非凸物体的自遮挡问题，GridMap 在物体包围盒表面均匀放置锚定相机（每面 3×3 网格），为每个锚定相机构建局部立方体贴图。对表面任意点 $\mathbf{p}$，其漫反射 Stokes 矢量通过对 $N$ 个锚定相机的局部立方体贴图进行距离加权插值得到：
$$\tilde{S}_d = \frac{\sum_{i=1}^{N} \|\mathbf{p} - \mathbf{c}_i\|_2 \cdot \tilde{S}_d^{(i)}}{\sum_{i=1}^{N} \|\mathbf{p} - \mathbf{c}_i\|_2}$$
与基线方法为每个高斯学习 SH 系数表示间接光的做法不同，GridMap 不学习任何场景特定参数，泛化性更强。

**4. Training Losses（多信号监督层）**  
总损失函数组合五类监督信号：
$$\mathcal{L} = \mathcal{L}_{\mathrm{rgb}} + \lambda_1 \mathcal{L}_{\mathrm{pol}} + \lambda_2 \mathcal{L}_{\mathrm{mask}} + \lambda_3 \mathcal{L}_{\mathrm{depth}} + \lambda_4 \mathcal{L}_{\mathrm{smooth}}$$
其中 $\mathcal{L}_{\mathrm{pol}}$ 是偏振损失，直接约束 Stokes 矢量的重建精度；$\mathcal{L}_{\mathrm{depth}}$ 强制 α 混合法线与深度法线一致；$\mathcal{L}_{\mathrm{smooth}}$ 提供边缘感知的法线平滑正则。

### 数据流与优化逻辑

训练时，多视角偏振图像输入后，2DGS Backbone 生成几何与物理属性，PolarDR 将其渲染为 Stokes 矢量并与真实偏振测量比较，GridMap 同步提供自遮挡感知的环境光照估计。所有损失信号联合反向传播，同时优化高斯几何参数和物理属性。推理时，给定新的环境光照图，可直接通过 PolarDR 和 GridMap 渲染出物理正确的重光照结果。

### 关键设计决策与瓶颈突破

PhyGaP 的设计直接回应了核心瓶颈：**普通 RGB 图像缺乏足够的表面形状与材质信息，导致现有方法难以正确解耦反照率与反射分量**。通过引入偏振成像及其物理模型（pBRDF），PolarDR 为表面法线、折射率、粗糙度等物理属性的优化提供了额外的监督信号。GridMap 则解决了非凸物体的间接光照建模难题，避免了基线方法中 SH 间接光表示的场景过拟合问题。消融实验（**Table 2, Fig. 9**）证实：移除 PolarDR（$\lambda_1=0$）会导致环境图 PSNR 大幅下降，反照率中混入镜面反射；移除 GridMap 则使非凸物体的阴影处理失败，反照率出现颜色偏移。

### 补充图表

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/001_Figure_1.jpg]]
*Figure 1: We propose PhyGaP, a physically-grounded 3DGS method that (a) takes full or partial polarization information as input, (b) accurately reconstructs the shape and physical attributes of glossy object, (c) achieves decomposed rendering of object appearance (top), diffuse reflection (mid), and specular reflection (bottom), as well as (d) enables robust and realistic relighting with natural reflection. Results in this visualization are from our captured buddha scene*

## 核心模块与公式推导

PhyGaP 的核心架构建立在 **2DGS 几何表示**之上，并引入两个关键改进：**PolarDR（偏振化延迟渲染）** 与 **GridMap（自遮挡感知环境光照）**。以下逐一阐述各模块的公式、变量含义及设计逻辑。

---

### 2DGS 几何基础

PhyGaP 采用 2D Gaussian Splatting 作为底层几何表示，每个高斯基元定义在局部切平面上，通过以下映射变换到世界坐标系（Eq. 1）：

$$P(u,v) = \mathbf{p} + s_u \mathbf{t_u} \cdot u + s_v \mathbf{t_v} \cdot v = \mathbf{H} \cdot [u, v, 1, 1]^T$$

其中 $\mathbf{H} = \begin{bmatrix} s_u \mathbf{t}_u & s_v \mathbf{t}_v & 0 & \mathbf{p} \\ 0 & 0 & 0 & 1 \end{bmatrix}$，$\mathbf{p}$ 为基元中心，$\mathbf{t}_u, \mathbf{t}_v$ 为切平面正交基，$s_u, s_v$ 为缩放因子。

对于相机像素 $(x,y)$ 发出的光线，其与高斯切平面的交点由 Eq. 2 给出：

$$[xz, yz, z, 1]^T = \mathbf{W} \mathbf{H} \cdot [u, v, 1, 1]^T$$

其中 $\mathbf{W}$ 为世界到裁剪空间的变换矩阵。每个 2D 高斯在像素上的影响权重通过 Eq. 3 定义：

$$\mathcal{G}(u,v) = \exp\left(-\frac{u^2+v^2}{2}\right)$$

该权重用于后续的 $\alpha$ 混合渲染。2DGS 的优势在于提供了显式的表面法线，这是物理渲染不可或缺的几何先验。

---

### PolarDR：偏振化延迟渲染

PolarDR 是 PhyGaP 的核心创新，将标准延迟渲染扩展为偏振形式。其关键操作是**将高斯的物理属性光栅化为材质图**：反照率 $\lambda$、折射率 $\eta$（IoR）、法线 $\mathbf{n}$、粗糙度 $r$，然后利用 pBRDF 模型计算每个像素的出射 Stokes 矢量。

**物理渲染方程**（Eq. 4）给出出射方向 $\omega_o$ 的总辐射度：

$$L(\omega_o) = \int_{\Omega} L_i(\omega_i) f_r(\omega_i, \omega_o) \langle \boldsymbol{\omega}_i \cdot \mathbf{n} \rangle \mathrm{d}\omega_i$$

该方程分解为漫反射与镜面反射两部分。在偏振域中，PhyGaP 分别对两者建模（假设入射光为非偏振光）：

**镜面反射的 Stokes 矢量**（Eq. 7）：

$$S_{\omega_o}^s = [ \beta_s(\theta_{\mathbf{n}}) \cos 2\phi_{\mathbf{n}} ] L_s(\omega_o) , -\beta_s(\theta_{\mathbf{n}}) \sin 2\phi_{\mathbf{n}} ]$$

**漫反射的 Stokes 矢量**（Eq. 8）：

$$S_{\omega_o}^d = [ \beta_d(\theta_{\mathbf{n}}) \cos 2\phi_{\mathbf{n}} ] L_d(\omega_o) , -\beta_d(\theta_{\mathbf{n}}) \sin 2\phi_{\mathbf{n}} ]$$

其中 $\beta_s, \beta_d$ 分别为镜面与漫反射的偏振度函数，$\theta_{\mathbf{n}}$ 为法线与视线夹角，$\phi_{\mathbf{n}}$ 为法线在像平面内的方位角。**漫反射的偏振程度远弱于镜面反射**，这一物理差异正是 PolarDR 能够解耦反照率与反射分量的关键——偏振损失为分离镜面高光提供了额外的监督信号。

---

### GridMap：自遮挡感知的间接光照

GridMap 解决了非凸物体的间接光照问题。其核心思想是**在物体包围盒上放置锚定相机**，为每个锚定相机构建局部立方体贴图，再通过距离加权插值计算表面点的漫反射 Stokes。

具体而言，包围盒每个面划分为 $3\times 3$ 网格，在每个网格点放置一个锚定相机 $\mathbf{c}_i$。对于每个锚定相机，向所有方向进行光线追踪，将物体颜色与全局环境图混合，得到局部立方体贴图 $\tilde{S}_d^{(i)}$。

对于表面点 $\mathbf{p}$，其漫反射 Stokes 由 $N$ 个锚定相机的局部立方体贴图通过**距离加权平均**得到（Eq. 9）：

$$\tilde{S}_d = \frac{\sum_{i=1}^{N} \|\mathbf{p} - \mathbf{c}_i\|_2 \cdot \tilde{S}_d^{(i)}}{\sum_{i=1}^{N} \|\mathbf{p} - \mathbf{c}_i\|_2}$$

这一设计的优势在于**无需学习场景特定的间接光照参数**（如球谐系数），避免了过拟合，并提高了对非凸几何的泛化能力。消融实验证实，移除 GridMap 后非凸物体（如 david 雕像）的阴影无法正确处理，反照率出现颜色偏移（Fig. 9, Table 2）。

---

### 训练损失函数

PhyGaP 的总训练损失由五项加权组成（Eq. 10）：

$$\mathcal{L} = \mathcal{L}_{\mathrm{rgb}} + \lambda_1 \mathcal{L}_{\mathrm{pol}} + \lambda_2 \mathcal{L}_{\mathrm{mask}} + \lambda_3 \mathcal{L}_{\mathrm{depth}} + \lambda_4 \mathcal{L}_{\mathrm{smooth}}$$

各项含义如下：
- $\mathcal{L}_{\mathrm{rgb}}$：RGB 重建损失
- $\mathcal{L}_{\mathrm{pol}}$：偏振重建损失（**$\lambda_1=0$ 等价于移除 PolarDR**）
- $\mathcal{L}_{\mathrm{mask}}$：掩码损失
- $\mathcal{L}_{\mathrm{depth}}$：深度-法线一致性损失，强制 $\alpha$ 混合后的高斯法线与深度法线一致
- $\mathcal{L}_{\mathrm{smooth}}$：边缘感知的法线平滑损失，在图像边缘处减弱正则化强度

超参数 $\lambda$ 的消融实验（Fig. 14）表明论文汇报值接近最优。

### 补充图表

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/003_Figure_3.jpg]]
*Figure 3: Overview of GridMap. (a) We sample a set of anchor cameras on the object bounding box. (b) For each anchor camera, we ray trace in all directions to blend object color with the global environment map. (c) The resulting local environment map enables more accurate diffuse irradiance computation*

## 实验与分析

### 核心发现与定量结果

PhyGaP 在多个基准上实现了对新视角合成、表面法线重建、反射分解及重光照的全面改进，其性能增益直接源于偏振物理模型（PolarDR）与自遮挡感知的环境光照模块（GridMap）的协同作用。

**新视角合成与法线重建（Table 1）**。在 PANDORA 数据集的 owl 场景上，PhyGaP 取得 **PSNR 28.14 dB**，较仅依赖 RGB 的 Ref-Gaussian（22.39 dB）提升 **+5.75 dB**；在 Mitsuba3 的 teapot 场景上，表面法线的 Cosine Distance 降至 **0.0079**，相比 Ref-Gaussian（0.0093）改善约 15%。这些收益验证了偏振线索对几何与外观解耦的强监督作用：偏振信号直接约束了法线方向与镜面/漫反射分量的物理一致性，缓解了 RGB-only 方法中常见的模糊性。

**环境图重建与重光照（Table 2）**。在 SMVP 的 david 场景上，PhyGaP 重光照结果达到 **PSNR 19.18 dB、SSIM 0.973、LPIPS 0.0255**，显著优于 GS-IR（PSNR 16.90 dB、SSIM 0.957、LPIPS 0.0359）。这一优势源于 PolarDR 对反照率与反射分量的显式解耦：重光照仅需替换环境图并重新计算光照传输，而无需重新训练或引入额外的场景特定参数。

### 消融实验：PolarDR 与 GridMap 的因果贡献

消融实验揭示了两个核心模块的独立与联合效应（Table 2, Fig. 9）。

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/008_Table_2.jpg]]
*Table 2: Quantitative evaluation of environment map reconstruction and relighting. Left: PSNR of optimized envmaps for different methods on the Mitsuba-rendered dataset. Right: Polarimetric evaluation of david relighted with the sunset envmap. Ablation results are also included. “No PDR” is realized by setting λ1 = 0*

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/011_Figure_9.jpg]]
*Figure 9: Ablation results with and without PolarDR (PDR) and/or GridMap (GM). We observe visible differences in color correctness, albedo quality, and environment map smoothness*

**移除 PolarDR（λ₁=0）** 导致环境图 PSNR 大幅下降，重光照 PSNR 从 19.18 dB 降至 17.81 dB（保留 GridMap）或 15.56 dB（同时移除 GridMap）。定性结果（Fig. 9）显示，反照率中混入了镜面反射残留，环境图平滑度显著降低。这表明，仅靠 RGB 损失无法有效分离漫反射与镜面反射分量——偏振信号提供的物理约束是解耦的关键瓶颈。

**移除 GridMap** 后，非凸物体（如 david 雕像）的自遮挡区域出现明显的阴影处理错误与反照率颜色偏移（Fig. 9）。定量上，环境图 PSNR 同步下降（Table 2）。GridMap 的核心机制在于：通过包围盒锚定相机的局部立方体贴图插值，为每个表面点提供遮挡感知的漫反射辐照度估计，从而避免了学习场景特定的间接光照参数（如 SH 系数）所引入的过拟合风险。消融结果表明，对于具有复杂自遮挡的物体，GridMap 是正确反照率估计的必要条件。

**超参数敏感性**。λ 选择的消融曲线（Fig. 14）显示，论文汇报值接近 Cosine Distance 与 PSNR 的 Pareto 最优区域，表明方法对损失权重具有一定鲁棒性。

### 失败模式与局限性

**极端自遮挡与薄结构**。GridMap 依赖包围盒放置锚定相机，在处理极深凹区域或极薄物体时可能失效。Fig. 15 展示了 david 雕像底座与身体交界处的失败案例：GridMap 重建的反照率出现偏红色伪影；若将锚点放置于近表面位置，颜色偏移更为严重（锚点可能落入物体内部）。这揭示了 GridMap 的几何假设——锚点应位于物体外部以正确采样环境光照——在复杂拓扑下的脆弱性。

**金属表面与多次弹射**。当前 pBRDF 模型仅支持电介质材质，未纳入金属的偏振反射特性（金属的偏振相移与电介质不同）。同时，GridMap 仅模拟单次弹射的间接光照，无法处理多次互反射。这些限制意味着在包含金属部件或强互反射的场景中，反射分解与重光照质量可能下降。

**设备依赖与真实数据鲁棒性**。理想采集需偏振相机或两台配有线性偏振片的 RGB 相机，标定流程相对复杂。在部分偏振信息条件下（如仅有两个线性偏振片），偏振角度标定的精度直接影响法线重建质量——这是真实场景应用的主要工程瓶颈。

### 方法对比的公平性说明

需注意，NeRF 类基线（PANDORA、NeRSP）在 NVIDIA V100 上训练 15 万/5 万次迭代，而高斯泼溅方法在 RTX 4090D 上训练 3 万次迭代，且训练视点数量不同，可能导致不公平比较。此外，部分基线（如 Ref-Gaussian）不显式建模反照率，其分解结果不具可比性；PhyGaP 通过物理模型直接输出分离后的反照率，在反射分解任务上具有天然优势。

### 补充图表

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/004_Table_1.jpg]]
*Table 1: Quantitative results of different methods on novel view synthesis (left) and surface normal reconstruction (right). Best results are highlighted as 1st , 2nd , and 3rd . This visualization applies to all following quantitative assessments*

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/009_Figure_7.jpg]]
*Figure 7: Relighting results from different methods. The environment maps are presented at the top. Note that R3DG suffers severe overexposure in the rightmost Brown Photostudio environment*

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/005_Figure_4.jpg]]
*Figure 4: Visualization of reconstructed surface normal for synthetic (snail) and real-world (frog) objects*

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative comparison on estimated environment maps*

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/007_Figure_6.jpg]]
*Figure 6: Comparison on reflection decomposition. Note that PolGS and Ref-Gaussian do not explicitly model object albedo*

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/020_Figure_14.jpg]]
*Figure 14: Cosine distance (CD↓, left axis) and PSNR↑ (right axis) across λ choices. The reported values are indicated by triangles*

![[assets/figures/papers/paper_list_l2134_https_arxiv_org_abs_2603_14001/figures/021_Figure_15.jpg]]
*Figure 15: Left ground-truth colors for object body and stand. Mid albedo reconstructed using GridMap. Object concavity and selfocclusion result in reddish artifacts. Right albedo reconstructed using near-surface anchor placement. More severe color shifts are observed due to anchors being placed inside the object*

## 方法谱系与知识库定位

### 核心瓶颈与因果杠杆

现有基于3D高斯泼溅（3DGS）的逆向渲染方法（如 **Ref-Gaussian**、**GS-IR**、**GIR**、**3DGS-DR**）普遍依赖普通RGB图像作为输入。这类方法的根本瓶颈在于：RGB三通道信息对表面形状和材质的约束不足，导致优化过程中反照率（albedo）与镜面反射分量高度耦合，无法正确解耦外观的物理成分，进而难以支持高保真的重光照（relighting）。

PhyGaP的因果杠杆在于引入**偏振成像及其物理模型（pBRDF）**。偏振反射中，镜面分量与漫反射分量具有固有的偏振差异——镜面反射保持或增强入射光的偏振度，而漫反射则高度消偏。通过在延迟渲染管线中显式计算每个像素的Stokes矢量（即PolarDR过程），偏振线索为表面法线、折射率（IoR）、粗糙度等物理属性的优化提供了额外的、正交于RGB的监督信号，从而驱动外观的解耦。

### 方法谱系定位

PhyGaP处于**物理约束3DGS**与**偏振辅助逆向渲染**的交叉点，其相对位置可从以下维度界定：

**1. 相对于RGB-only 3DGS方法**

| 方法 | 物理属性建模 | 反射分解 | 重光照支持 |
|------|-------------|---------|-----------|
| **Ref-Gaussian** | 反照率、金属度、粗糙度 | 隐式（SH颜色混合） | 受限（SH间接光） |
| **GS-IR** | 法线、BRDF参数 | 部分分离 | 支持 |
| **GIR** | 法线、BRDF参数 | 部分分离 | 支持 |
| **3DGS-DR** | 延迟渲染管线 | 显式分解 | 支持 |
| **R3DG** | 法线、BRDF参数 | 部分分离 | 支持（但易过曝，见Fig. 7） |
| **PhyGaP (本文)** | 反照率、IoR、法线、粗糙度 | **显式、物理正确解耦** | **鲁棒支持，含非凸物体** |

关键差异点：
- **移除颜色SH**：PhyGaP不再为每个高斯学习球谐（SH）系数来表示颜色，而是通过物理BRDF直接计算颜色。这消除了SH对镜面反射的隐式编码，使反照率与镜面反射在表示层面即被强制分离。
- **PolarDR渲染过程**：将标准延迟渲染扩展为偏振化形式，使用pBRDF模型计算Stokes矢量。这一改变使得优化目标从单纯的RGB匹配扩展为RGB+偏振匹配，为物理属性提供了更强的约束。
- **GridMap间接光照**：替代了Ref-Gaussian中为每个高斯学习SH系数表示间接光的方式。GridMap基于包围盒锚定相机的局部立方体贴图插值，不学习场景特定参数，从而将重光照能力扩展到非凸物体。

**2. 相对于偏振辅助方法**

| 方法 | 表示 | 物理渲染 | 重光照 |
|------|------|---------|--------|
| **PANDORA** (NeRF) | 隐式神经辐射场 | pBRDF | 不支持 |
| **NeRSP** (NeRF) | 隐式神经辐射场 | pBRDF | 不支持 |
| **PolGS** (3DGS) | 3D高斯 | 简化偏振模型 | 不支持 |
| **PhyGaP (本文)** | 2D高斯（2DGS） | **完整pBRDF + PolarDR** | **首个支持重光照的偏振方法** |

PhyGaP是**首个将偏振重建与重光照能力统一**的方法。相比PolGS，PhyGaP的PolarDR过程显式建模了镜面与漫反射的偏振差异（Eq. 7, Eq. 8），而非使用简化的偏振表示。相比基于NeRF的PANDORA和NeRSP，PhyGaP继承了3DGS的实时渲染优势和2DGS的显式几何（法线、深度），使得物理属性的优化更加直接。

### 适用边界与局限

**适用场景：**
- 光滑电介质物体（glossy dielectric objects）的逆向渲染与重光照
- 需要显式反射分解（反照率、漫反射、镜面反射、环境图）的应用
- 可接受偏振成像硬件（偏振相机或双线性偏振片RGB相机）的场景

**已知局限：**

1. **金属表面不支持**：当前pBRDF模型仅针对电介质，金属的偏振特性（复数折射率导致的相位延迟）未被纳入。扩展到金属需要修改偏振反射模型。

2. **GridMap的几何敏感性**：GridMap依赖包围盒放置锚定相机，在处理极端自遮挡或极薄/深凹物体时可能失效，导致反照率出现颜色偏移（Fig. 15）。将锚点放置在物体内部会加剧这一问题。

3. **单次弹射限制**：GridMap仅模拟单次弹射的间接光照，无法处理多次互反射（inter-reflection），对于强相互反射场景（如凹面镜）存在理论误差。

4. **设备与标定要求**：理想情况需偏振相机或两台配有线性偏振片的RGB相机，标定和拍摄流程相对复杂。在仅有两个线性偏振片（部分偏振信息）的条件下，偏振角度标定精度可能影响重建质量。

5. **环境图学习稳定性**：对于大场景或复杂光照，环境图的学习可能不稳定。GridMap更新频率固定（每300次迭代），可能滞后于几何优化。

6. **训练开销**：GridMap增加约24.1%的训练时间和26.8%的推理时间（Sec. 9.4），相比纯RGB方法存在额外计算成本。

### 开放问题

1. **金属表面扩展**：如何将pBRDF模型扩展以纳入金属的偏振反射特性（复数折射率、相位延迟）？

2. **多次弹射互反射**：能否在PolarDR框架内高效地建模多次弹射的互反射，同时保持训练的稳定性？

3. **环境表示升级**：是否可以利用深度感知的环境表示（如GaussProbe）替代GridMap，以提高对真实数据中复杂几何和光照的鲁棒性？

4. **部分偏振信息利用**：在仅有两个线性偏振片（0°和45°或0°和90°）的条件下，如何进一步提升偏振角度标定的精度和重建质量？

5. **动态场景适应**：对于动态场景或移动光源，PhyGaP框架如何适应？GridMap的锚定相机策略是否需要动态调整？

6. **与物理渲染器的深度整合**：目前环境图优化与3DGS训练交替进行，是否可以实现端到端的联合优化，使环境光照与物体属性在统一的物理渲染框架（如Mitsuba 3）中协同收敛？

## 原文 PDF

![[paperPDFs/CVPR_2026/PhyGaP_Physically_Grounded_Gaussians_with_Polarization_Cues.pdf]]
