---
title: "CLoD-GS: Continuous Level-of-Detail via 3D Gaussian Splatting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/CLoD_GS_Continuous_Level_of_Detail_via_3D_Gaussian_Splatting_36e8ba656c10.pdf
project_link: null
code_link: null
aliases:
- CG
- CLoD-GS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 为每个高斯基元引入一个可学习的距离衰减因子σ_d,i，并结合用户可调的虚拟距离缩放因子s_v，动态控制基元不透明度的衰减速度。
primary_logic: 利用3DGS基元的连续体积特性和可微渲染管线，将细节层次控制建模为距离自适应的基元不透明度衰减，从而在单一模型中实现平滑无缝的连续LOD，同时通过训练策略中的点计数正则化使模型自行学习更紧凑的远距离表示。
claims:
- 每个高斯基元新增一个可学习的距离衰减因子，动态调节不透明度。
- 引入虚拟距离缩放训练策略，渲染来自虚拟距离的图像并配合点计数正则化损失。
- 在BungeeNeRF数据集上仅需一个模型即可实现比3DGS少38%的基元数量，同时PSNR更高。
- 消融实验证明正则化损失、自适应权重和多尺度训练缺一不可，完整模型效果最佳。
---

# CLoD-GS: Continuous Level-of-Detail via 3D Gaussian Splatting

> [!tip] 核心洞察
> 利用3DGS基元的连续体积特性和可微渲染管线，将细节层次控制建模为距离自适应的基元不透明度衰减，从而在单一模型中实现平滑无缝的连续LOD，同时通过训练策略中的点计数正则化使模型自行学习更紧凑的远距离表示。

| 字段 | 内容 |
|------|------|
| 中文题名 | CLoD-GS：基于3D高斯泼溅的连续细节层次 |
| 英文题名 | CLoD-GS: Continuous Level-of-Detail via 3D Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=zgs0L72R4c) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CLoD-GS |
| Dataset | BungeeNeRF, Deep Blending |

> [!tip] 效果简介
> - BungeeNeRF (8 scenes) 上，PSNR 28.05 (CLoD-GS scale=1) vs 27.85 (3DGS) (+0.20)。
> - BungeeNeRF 上，#GS 4.185M (CLoD-GS scale=1) vs 6.733M (3DGS) (-37.9%)。
> - Deep Blending (2 scenes) 上，PSNR 29.93 (CLoD-GS scale=1) vs 29.84 (3DGS) (+0.09)。

## 概要

**核心问题**：传统离散细节层次（DLoD）方法需为同一场景存储多个独立分辨率模型，导致内存开销倍增，且在模型切换边界产生明显的视觉跳变（popping artifacts），严重破坏沉浸式体验的连续性。

**方法定位**：CLoD-GS 在 3D Gaussian Splatting（**3DGS**, Kerbl et al., 2023）框架内引入**连续细节层次（CLoD）** 机制——为每个高斯基元赋予一个可学习的距离衰减因子 $\sigma_{d,i}$，结合用户可控的虚拟距离缩放因子 $s_v$，动态调制基元不透明度的衰减速度。训练时通过虚拟距离缩放策略与点计数正则化损失，使模型在单一表示中自主学习从近景高精度到远景紧凑表示的平滑过渡，无需存储多个模型。

**核心结论**：
- **质量与效率双赢**：在 BungeeNeRF 数据集上，CLoD-GS 仅需单一模型即实现比 3DGS 减少 **38%** 的高斯基元数量（4.185M vs 6.733M），同时 PSNR 提升 **0.20 dB**（28.05 vs 27.85）；在 Deep Blending 数据集上同样以更少基元取得更优质量。
- **平滑连续过渡**：相比 DLoD 在模型切换边界的质量跳变，CLoD-GS 实现了渲染质量随距离的平滑渐进退化，彻底消除视觉跳变。
- **渲染加速显著**：通过调节虚拟距离缩放因子减少活跃基元数量，帧率可从约 60+ FPS 提升至 **87.88 FPS**（$s_v=7$），且质量退化远较基线平缓。
- **组件协同必要**：消融实验证实，距离自适应权重、点计数正则化损失与多尺度训练三者缺一不可，完整模型在所有消融版本中表现最优。

**方法谱系与知识库定位**：CLoD-GS 属于 3DGS 后处理/训练期压缩与连续 LOD 交叉方向。与基于静态重要性排序的连续 LOD 方法（**Fast Rendering**, Milef et al., 2025）、基于八叉树的离散 LOD 方法（**Octree-GS**, Ren et al., 2025）、基于分层数据结构的离散 LOD 方法（**H-3DGS**, Kerbl et al., 2024）以及使用概率掩码进行静态剪枝的压缩方法（**MaskGaussian**, Liu et al., 2025）不同，CLoD-GS 首次将 LOD 控制建模为**距离自适应的可学习连续衰减**，在单一模型内实现无缝过渡，且训练策略可迁移至压缩模型（如 MaskGaussian）赋予其连续 LOD 能力。



### 3D高斯泼溅与细节层次控制的困境

3D高斯泼溅（3D Gaussian Splatting, 3DGS）作为一种显式辐射场表示方法，通过将场景建模为大量具有三维位置、协方差、颜色和不透明度的高斯基元，并利用可微光栅化进行实时渲染，在新视角合成任务中取得了令人瞩目的成绩。其核心渲染方程为：

$$C = \sum_{i \in N} c_i \alpha_i' \prod_{j=1}^{i-1} (1 - \alpha_j')$$

然而，3DGS的高质量渲染建立在密集的高斯基元之上——一个典型场景往往需要数百万个基元。当相机远离物体时，大量基元对最终像素的贡献微乎其微，却依然参与渲染计算，造成严重的计算资源浪费。这一瓶颈催生了对细节层次（Level-of-Detail, LoD）控制的需求：在保证视觉质量的前提下，根据观察距离动态削减冗余基元。

### 离散LOD的固有缺陷

传统方法普遍采用离散LOD（Discrete LoD, DLoD）策略来解决上述问题。其基本思路是为同一场景训练或构建多个不同分辨率的模型，在渲染时根据相机距离切换使用。这一范式存在两个根本性缺陷：

**存储冗余与切换跳变。** DLoD需要为每个场景维护多个独立模型，导致存储开销成倍增长。更严重的是，在模型切换的临界距离处，渲染质量会出现肉眼可见的突变——即所谓的popping artifacts。如Figure 5所示，当使用两个独立模型时，在切换边界（红色虚线处）会产生明显的质量跳跃，严重破坏用户体验的连续性。

**静态剪枝缺乏灵活性。** 部分工作尝试通过静态重要性排序对单一模型进行剪枝，如**MaskGaussian**（Liu et al., 2025）使用概率掩码移除低贡献基元。但这类方法产生的是固定的简化模型，无法在运行时根据观察距离动态调整细节水平，本质上仍是一种“一刀切”的压缩策略，而非真正的LoD控制。

### 从离散到连续：CLoD-GS的动机

上述困境揭示了一个明确的研究缺口：**如何在单一模型中实现平滑、连续的细节层次控制？** 这要求方法具备两个核心能力：

1. **距离自适应的基元调度**：每个基元对渲染的贡献应能根据其与相机的距离连续变化，而非二元地“存在”或“被移除”。
2. **训练阶段的隐式稀疏化**：模型应在训练过程中自主学习远距离下的紧凑表示，而非依赖后处理剪枝。

3DGS的连续体积特性和可微渲染管线为实现这一目标提供了天然基础。CLoD-GS的核心洞察在于：**将LoD控制建模为距离自适应的基元不透明度衰减**。通过为每个高斯基元引入一个可学习的距离衰减因子，并配合虚拟距离缩放训练策略，模型能够在单次训练中学会在不同观察距离下合理分配基元，实现从高质量近景到稀疏远景的无缝过渡。



## 核心方法与创新机理

CLoD-GS的核心创新在于将传统离散LOD（DLoD）中“存储多模型、切换时跳变”的瓶颈，转化为单一模型内的**连续距离自适应基元衰减**机制。其关键洞察是：3D高斯泼溅（3DGS）基元的连续体积特性天然适合建模平滑的细节过渡，只需为每个基元赋予一个可学习的“生命周期”参数，即可在渲染时根据视距动态决定其可见性贡献。

### 关键改造槽位

CLoD-GS对标准3DGS流水线进行了两个关键改造：

**1. 基元不透明度：从固定值到距离自适应衰减**

标准3DGS中，每个高斯基元的不透明度$\alpha_i$是固定的，仅由优化决定。CLoD-GS为每个基元引入一个可学习的**距离衰减因子**$\sigma_{d,i}$，将渲染时实际使用的不透明度$\alpha_i''$定义为：

$$\alpha_i'' = \alpha_i \cdot \exp\left( - \frac{(d_i' \cdot s_v)^2}{2 \cdot (\mathrm{ReLU}(\sigma_{d,i}))^2 + \epsilon} \right)$$

其中$d_i'$是基元到相机的归一化距离，$s_v$是用户可调的**虚拟距离缩放因子**。这一公式本质上是一个以$\sigma_{d,i}$为标准差的高斯衰减函数：当基元距离增大时，其不透明度以$\sigma_{d,i}$控制的速率平滑衰减，而非被二元地保留或丢弃。

配合动态掩码过滤机制$M_i = (\alpha_i'' > \tau \cdot s_v)$，低于阈值的基元被直接跳过渲染，在保证视觉连续性的同时实现计算量的平滑缩减。每个基元仅额外增加一个浮点参数（约1.6%存储开销），代价极低。

**2. 训练策略：从单一尺度到虚拟距离缩放训练**

仅添加衰减参数不足以让模型学会合理的距离自适应行为。CLoD-GS设计了**虚拟距离缩放训练策略**，在训练时随机采样$s_v \sim U(1, 10)$，模拟从近到远的多尺度观测条件，并配合两项关键设计：

- **点计数正则化损失**：显式鼓励远距离使用更少基元：
  $$L_{\mathrm{reg}} = (s_v - 1.0)^2 \cdot \left( \mathrm{ReLU}(\eta_{\mathrm{actual}} - \eta_{\mathrm{target}}) \right)^2$$
  其中目标基元比率$\eta_{\mathrm{target}} = 1 / s_v^{1.5}$随虚拟距离增大而降低，惩罚力度随$s_v$增大而增强。

- **距离自适应渲染权重**：$w_s = (1 - 0.5 \cdot s_v / \max(s_v))^2$，防止远距离视图的过度剪枝导致训练不稳定。

### 与离散LOD的本质区别

传统DLoD方法（如H-3DGS、Octree-GS）需为同一场景训练多个分辨率模型，切换时产生视觉跳变（popping artifacts）。CLoD-GS通过连续衰减机制，在单一模型内实现**无缝的细节过渡**：基元不会突然出现或消失，而是随距离逐渐“淡出”，从根本上消除了跳变问题。消融实验证实，正则化损失、自适应权重和多尺度训练三个组件缺一不可，完整模型在BungeeNeRF数据集上以比3DGS少38%的基元数量（4.185M vs 6.733M）实现了更高的PSNR（28.05 vs 27.85），验证了连续LOD策略的有效性。



CLoD-GS 的整体流水线建立在标准 3DGS 可微渲染管线之上，通过两个核心改造实现单一模型内的连续细节层次控制：**距离自适应不透明度衰减**和**虚拟距离缩放训练策略**。整个框架的输入为多视角图像及其对应的相机位姿，输出为一个增强的 3DGS 模型，其中每个高斯基元除了原有的位置、协方差、颜色和不透明度参数外，额外携带一个可学习的距离衰减因子 $\sigma_{d,i}$。

流水线可分解为三个关键模块：

1. **距离自适应不透明度衰减模块**：在渲染阶段，对于每个高斯基元 $i$，首先计算其与相机视点的归一化距离 $d_i'$，然后结合可学习的衰减因子 $\sigma_{d,i}$ 和用户可控的虚拟距离缩放因子 $s_v$，通过高斯衰减函数动态计算衰减后的不透明度 $\alpha_i''$：
   $$\alpha_i'' = \alpha_i \cdot \exp\left( - \frac{(d_i' \cdot s_v)^2}{2 \cdot (\mathrm{ReLU}(\sigma_{d,i}))^2 + \epsilon} \right)$$
   该公式的核心机制在于：当 $\sigma_{d,i}$ 较小时，基元的不透明度随距离增加而迅速衰减，使其在远距离视角下自然“隐退”；反之，$\sigma_{d,i}$ 较大的基元则能在更远的距离上保持可见性。$\mathrm{ReLU}$ 函数确保衰减因子非负，$\epsilon$ 防止除零。

2. **动态掩码过滤模块**：基于衰减后的不透明度 $\alpha_i''$，对每个基元施加硬阈值过滤 $M_i = (\alpha_i'' > \tau \cdot s_v)$。只有满足该条件的基元才会被送入后续的 alpha 混合渲染管线。阈值与 $s_v$ 成正比，意味着虚拟距离越大，过滤越激进，从而在远距离视角下自动使用更少的基元。

3. **虚拟距离缩放训练模块**：训练时，随机从均匀分布 $U(1, 10)$ 中采样虚拟距离缩放因子 $s_v$，模拟从近到远的多种观察距离。对于每个采样的 $s_v$，渲染损失按距离自适应权重 $w_s = (1 - 0.5 \cdot s_v / \max(s_v))^2$ 进行衰减，防止远距离过度剪枝导致训练不稳定。同时引入点计数正则化损失：
   $$L_{\mathrm{reg}} = (s_v - 1.0)^2 \cdot \left( \mathrm{ReLU}(\eta_{\mathrm{actual}} - \eta_{\mathrm{target}}) \right)^2$$
   其中 $\eta_{\mathrm{target}} = 1 / s_v^{1.5}$ 为期望的基元渲染比率，$\eta_{\mathrm{actual}}$ 为实际比率。该损失显式惩罚实际渲染基元数超出目标的情况，且惩罚强度随 $s_v$ 增大而增强，促使模型在远距离下学习更紧凑的基元表示。最终训练损失为 $L_{\mathrm{total}} = w_s (L_{\mathrm{render}} + \lambda_{\mathrm{reg}} L_{\mathrm{reg}})$。

**推理阶段的灵活性**：训练完成后，用户只需调整单一的全局参数 $s_v$，即可在渲染时连续控制模型的细节层次——$s_v = 1$ 对应最高质量的原生渲染，$s_v$ 越大则基元数量越少、渲染速度越快，且整个过程平滑无跳变，无需加载或切换多个独立模型。

### 补充图表

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/001_Figure_1.jpg]]
*Figure 1: Framework of the proposed methodology*



### 3DGS渲染基础

3DGS通过alpha混合对投影到像素上的高斯基元进行深度排序渲染。给定按深度排序的基元集合 $N$，像素颜色 $C$ 的计算公式为：

$$C = \sum_{i \in N} c_i \alpha_i' \prod_{j=1}^{i-1} (1 - \alpha_j')$$

其中 $c_i$ 为基元 $i$ 的颜色，$\alpha_i'$ 为经过2D投影协方差调制后的有效不透明度。这是标准3DGS渲染管线的基础（Kerbl et al., 2023），CLoD-GS的所有改进均建立在此框架之上。

### 距离自适应不透明度衰减

传统3DGS中，每个基元的不透明度 $\alpha_i$ 仅由自身参数决定，与相机距离无关。CLoD-GS的核心创新在于为每个高斯基元引入一个额外的可学习参数：**距离衰减因子** $\sigma_{d,i}$。该参数动态调节基元不透明度随相机距离的衰减速度，从而在单一模型中实现连续LOD控制。

具体而言，衰减后的不透明度 $\alpha_i''$ 通过高斯衰减函数计算：

$$\alpha_i'' = \alpha_i \cdot \exp\left( - \frac{(d_i' \cdot s_v)^2}{2 \cdot (\mathrm{ReLU}(\sigma_{d,i}))^2 + \epsilon} \right)$$

**变量含义：**
- $\alpha_i$：基元 $i$ 的原始不透明度。
- $d_i'$：基元 $i$ 到相机的归一化距离（基于场景包围盒归一化）。
- $s_v$：**虚拟距离缩放因子**（virtual distance scale），由用户或系统在推理时设定。$s_v$ 越大，等效距离越远，不透明度衰减越剧烈，渲染使用的基元越少。
- $\sigma_{d,i}$：可学习的距离衰减因子，通过 $\mathrm{ReLU}$ 确保非负。$\sigma_{d,i}$ 越小，该基元对距离越敏感（衰减越快）；$\sigma_{d,i}$ 越大，该基元越能保持可见性。
- $\epsilon$：小常数，防止除零。

**核心机制：** 该公式本质上是将每个基元的不透明度建模为以相机距离为自变量的高斯衰减函数。$\sigma_{d,i}$ 充当了“衰减带宽”的角色——不同基元可以学习不同的 $\sigma_{d,i}$，使得模型在训练过程中自行决定哪些基元应在远距离优先被裁剪，哪些基元应保留以维持结构完整性。

### 动态掩码过滤

基于衰减后的不透明度 $\alpha_i''$，系统通过阈值过滤决定哪些基元参与实际渲染。掩码 $M_i$ 定义为：

$$M_i = (\alpha_i'' > \tau \cdot s_v)$$

其中 $\tau$ 为基础阈值。该设计使得阈值随虚拟距离缩放因子 $s_v$ 自适应调节——距离越远，过滤越严格，仅保留衰减后不透明度足够高的基元。被掩码剔除的基元（$M_i=0$）不参与alpha混合计算，从而在渲染时直接减少计算量。

### 虚拟距离缩放训练策略

训练阶段的核心挑战在于：模型需要在单一训练过程中学会在**不同虚拟距离**下合理分配基元。CLoD-GS通过以下三个组件实现这一目标：

**（1）虚拟距离采样。** 训练时，虚拟距离缩放因子 $s_v$ 从均匀分布中随机采样：$s_v \sim U(1, s_{v,\max})$，其中 $s_{v,\max}$ 为训练时设定的最大虚拟距离缩放范围。这使得模型在训练过程中暴露于从近到远的多尺度距离条件。

**（2）点计数正则化损失。** 为显式鼓励远距离使用更少基元，引入目标基元比率 $\eta_{\mathrm{target}}$ 和正则化损失 $L_{\mathrm{reg}}$：

$$\eta_{\mathrm{target}} = 1 / s_v^{1.5}$$

$$L_{\mathrm{reg}} = (s_v - 1.0)^2 \cdot \left( \mathrm{ReLU}(\eta_{\mathrm{actual}} - \eta_{\mathrm{target}}) \right)^2$$

其中 $\eta_{\mathrm{actual}}$ 为实际渲染基元数与总基元数的比值。该损失仅在 $\eta_{\mathrm{actual}}$ 超出目标比率时激活（通过 $\mathrm{ReLU}$），惩罚因子 $(s_v - 1.0)^2$ 使得约束强度随虚拟距离增大而增强。

**（3）距离自适应损失权重。** 最终训练损失为：

$$L_{\mathrm{total}} = w_s (L_{\mathrm{render}} + \lambda_{\mathrm{reg}} L_{\mathrm{reg}})$$

其中 $w_s = (1 - 0.5 \cdot s_v / \max(s_v))^2$ 为距离自适应权重。该权重在远距离（$s_v$ 较大）时降低渲染损失和正则化损失的总体贡献，防止过度剪枝导致远距离渲染质量崩溃。$\lambda_{\mathrm{reg}}$ 为平衡渲染保真度与稀疏性约束的超参数。

### 模块协同关系

三个核心模块形成闭环：**距离自适应不透明度衰减**提供了连续LOD的数学基础，**动态掩码过滤**将理论衰减转化为实际的计算节省，**虚拟距离缩放训练**通过多尺度暴露和显式正则化引导模型学习合理的 $\sigma_{d,i}$ 分布。三者缺一不可——消融实验（Table 3）证实，移除任意组件均会导致性能下降。



## 实验与关键发现

### 实验设置

为评估CLoD-GS的有效性，实验在三个公开数据集上进行：**BungeeNeRF**（8个多尺度场景）、**Deep Blending**（2个场景）和**Mip-NeRF 360**（9个场景）。所有方法均基于最新公开的3DGS代码库实现，使用相同的训练/测试数据划分和统一的超参数配置。对于可学习的距离衰减因子σ_d,i，学习率设为1e-2。正则化损失权重λ_reg用于平衡重建精度与稀疏性约束之间的权衡。

公平性保障方面，对于3DGS和MaskGaussian等基线方法，实验也应用CLoD-GS提出的不透明度衰减公式（Equation 2）对其训练好的模型进行基元选择，保留衰减后不透明度最高的基元，以确保在基元数量相当时的公平对比。

### 主实验结果

#### 最高质量模型对比

Table 1展示了各方法在最高质量设定下的定量对比。CLoD-GS（scale=1）在BungeeNeRF数据集上取得了**28.05 dB**的PSNR，优于3DGS的27.85 dB（+0.20 dB），同时基元数量从6.733M降至**4.185M**，实现了约**38%的减少**。在Deep Blending数据集上，CLoD-GS同样以29.93 dB的PSNR略优于3DGS的29.84 dB。

值得注意的是，CLoD-GS在减少近40%基元的同时仍能提升渲染质量，这验证了连续LOD机制的有效性——模型学会了将有限的基元预算更合理地分配到对视觉质量贡献更大的区域。

#### 渲染速度分析

Table 2展示了各方法在不同虚拟距离缩放因子下的FPS对比。渲染速度与高斯数量呈强负相关：减少高斯数量能提升所有方法的帧率，但CLoD-GS的提升幅度更为显著。在BungeeNeRF数据集上，CLoD-GS在scale=7时达到**87.88 FPS**，远超3DGS的约60+ FPS。这一优势源于CLoD-GS在单一模型中即可实现连续LOD，无需像离散LOD方法那样切换模型，从而在保持流畅用户体验的同时最大化渲染效率。

#### 质量-基元数量权衡

Figure 3展示了BungeeNeRF和Deep Blending数据集上的质量与基元数量权衡曲线。虚线表示训练期间的最大虚拟缩放范围。CLoD-GS在不同虚拟距离范围（s_v）下表现出**更平缓的质量退化**，而3DGS等基线方法在基元数量减少时质量下降更为剧烈。这表明连续衰减机制使得模型能够在不同细节层次之间平滑过渡，避免了离散LOD中常见的质量跳变。

#### 视觉质量对比

Figure 2展示了在相似基元数量下的视觉对比。CLoD-GS在重复纹理或复杂光照区域产生更清晰的结果，同时通常使用更少的高斯。每张图像右下角标注了使用的高斯数量和对应的PSNR，直观展示了CLoD-GS的效率优势。

### 消融研究

Table 3展示了关键训练组件的消融结果。完整模型在所有消融版本中表现最优，证明**正则化损失、自适应权重和多尺度训练三者缺一不可**。

具体而言（参考Table 8-10的逐场景消融）：

- **移除权重自适应**（Table 9 vs Table 8）：在BungeeNeRF amsterdam场景（scale=5）上，PSNR从27.15降至26.82。这表明距离自适应权重w_s对于防止远距离过度剪枝至关重要。
- **移除正则化损失**（Table 10）：基元数量显著减少但质量大幅下降，说明仅靠渲染损失无法引导模型学习紧凑的远距离表示。
- **同时移除权重自适应和正则化**（Table 11）：amsterdam场景PSNR进一步降至25.93，验证了两个组件的协同作用。

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/016_Table_8.jpg]]
*Table 8: Full Model (scale=5)*

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/017_Table_9.jpg]]
*Table 9: Without Weight Adaptation (scale=5)*

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/018_Table_10.jpg]]
*Table 10: Without Regularization (scale=5)*

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/019_Table_11.jpg]]
*Table 11: Without Weight & Regularization (scale=5)*

### 鲁棒性分析

CLoD-GS的存储开销极低：每个高斯基元仅额外增加一个浮点参数（σ_d,i），在标准3DGS实现（每基元约248字节）中仅增加**1.6%的存储开销**，这在工程上是完全可接受的。

此外，将CLoD-GS应用于MaskGaussian模型（Figure 7）的实验表明，该方法可成功为已压缩模型赋予连续LOD能力——增大虚拟距离缩放范围同样能实现更平滑的简化曲线，验证了方法的通用性和即插即用特性。

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/010_Figure_7.jpg]]
*Figure 7: Robustness analysis. Our CLoD-GS training strategy is applied to a MaskGaussian model on Bungeenerf dataset, successfully enabling continuous LoD on a compressed representation*

### 离散LOD与连续LOD对比

Figure 5和Figure 6直观对比了离散LOD（DLoD）与连续LOD（CLoD）策略。DLoD方法使用两个独立模型，在边界处（红色虚线标注）产生可见的质量跳变；而CLoD策略在三个距离区间内均表现出平滑的质量过渡。度量曲线进一步证实：DLoD策略呈现尖锐的、不连续的质量跳变，而CLoD策略实现了平滑渐进的质量变化，有效消除了popping artifacts。

### 失败模式与局限性

尽管CLoD-GS在多个数据集上表现优异，但仍存在以下局限：

1. **LOD控制维度单一**：当前方法仅依赖距离度量控制细节层次，未整合纹理复杂度、语义信息等感知显著性指标，在特定场景下可能产生次优的细节分配。
2. **训练收敛速度**：虽然训练耗时仅为训练两个独立模型的一半，但单次训练需覆盖更宽的虚拟距离范围，收敛速度可能稍慢。
3. **大规模场景集成**：方法尚未与octree等chunk-based加载方案深度集成，在超大规模场景中可能面临视锥体内基元总数过高的问题。
4. **参数压缩未探索**：σ_d,i仅占1.6%存储开销，但未进一步探索与该参数相关的压缩或量化策略。

### 补充图表

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/002_Table_1.jpg]]
*Table 1: Quantitative comparison of highestquality models. Best results are bold, second best are underlined. The fifth and sixth columns indicate the number of Gaussian primitives (#GS) and memory consumption (Mem). ‘↓’ indicates that lower is better*

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/003_Table_2.jpg]]
*Table 2: Comparison of FPS on various datasets. Best results are bold, second best are underlined. Higher is better (↑)*

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/004_Figure_2.jpg]]
*Figure 2: Visual comparison at similar primitive counts. The number of Gaussians used and the corresponding PSNR are annotated in the bottom-right corner of each image*

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/007_Table_3.jpg]]
*Table 3: Ablation study on our key training components. The full model outperforms all ablated versions*

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/008_Figure_5.jpg]]
*Figure 5: Visual comparison of DLoD vs. CLoD strategies. The DLoD approach (the second column) uses two separate models, causing a visible quality jump at the boundary (red dashed line). Our CLoD approach (the left three columns) uses a single model with varying scale factors, resulting in a smooth, artifact-free transition*

![[assets/figures/papers/paper_list_l78_https_openreview_net_forum_id_zgs0L72R4c/figures/009_Figure_6.jpg]]
*Figure 6: Metric curves for the DLoD vs. CLoD comparison. The DLoD strategy exhibits a sharp, discontinuous jump in quality, whereas our CLoD strategy shows a smooth progression*



## 定位与知识库关联

### 核心瓶颈与因果机制

传统离散细节层次（DLoD）方法需要为同一场景存储多个独立分辨率模型，导致内存开销线性增长，且在模型切换边界产生显著的视觉跳变（popping artifacts）。CLoD-GS 的核心洞察在于：**3DGS 基元的连续体积特性天然适合连续 LOD 建模**，无需额外模型副本。其因果控制机制是为每个高斯基元引入一个可学习的距离衰减因子 σ_d,i，结合用户可调的虚拟距离缩放因子 s_v，通过高斯衰减函数动态调制基元不透明度：

$$\alpha_i'' = \alpha_i \cdot \exp\left( - \frac{(d_i' \cdot s_v)^2}{2 \cdot (\mathrm{ReLU}(\sigma_{d,i}))^2 + \epsilon} \right)$$

该公式将 LOD 控制从“选择哪个模型”转化为“每个基元贡献多少”，实现了单一模型内的平滑连续退化。训练时通过虚拟距离缩放策略（s_v ~ U(1,10)）和点计数正则化损失 L_reg 显式鼓励远距离使用更少基元，使模型自行学习紧凑的远距离表示。

### 与基线方法的关系

**3DGS**（Kerbl et al., 2023）作为原始高质量基线，通过密集高斯集合实现逼真渲染，但缺乏 LOD 机制，计算成本随基元数量线性增长。CLoD-GS 在其基础上仅增加每个基元一个浮点参数（约 1.6% 存储开销），赋予模型连续 LOD 能力：在 BungeeNeRF 数据集上，CLoD-GS 以比 3DGS 少 37.9% 的基元数量（4.185M vs 6.733M）取得更高 PSNR（28.05 vs 27.85）。

**MaskGaussian**（Liu et al., 2025）使用概率掩码进行静态剪枝以实现压缩，但剪枝后的模型不具备动态 LOD 能力。CLoD-GS 的训练策略可应用于 MaskGaussian 的压缩模型，成功为其赋予连续 LOD 能力（见 Figure 7），表明该方法具有跨模型架构的泛化性。

**Octree-GS**（Ren et al., 2025）和 **H-3DGS**（Kerbl et al., 2024）均采用分层数据结构实现离散 LOD，本质上是 DLoD 的变体。CLoD-GS 与之根本不同：不依赖空间层级结构，而是通过逐基元的连续衰减实现 LOD。实验表明，DLoD 策略在模型切换边界产生尖锐的质量跳变，而 CLoD-GS 的质量退化曲线平滑连续（Figure 5、Figure 6）。

**Fast Rendering**（Milef et al., 2025）基于静态重要性排序实现连续 LOD，但其重要性分数在训练后固定，无法根据运行时距离动态调整。CLoD-GS 的衰减因子 σ_d,i 在训练中与渲染损失联合优化，能够学习场景自适应的衰减模式。

### 适用边界与局限

**适用场景**：需要单一模型覆盖多距离范围的新视角合成任务，尤其适合内存受限或需要平滑 LOD 过渡的应用（如移动端渲染、Web 可视化）。在 BungeeNeRF 多尺度数据集上表现突出，在 Deep Blending 数据集上也保持了轻微质量优势。

**主要局限**：

1. **感知特征单一**：当前 LOD 控制仅依赖距离度量，未整合纹理复杂度、语义显著性等感知指标。在重复纹理或复杂光照区域虽然表现优于基线，但仍可能产生次优的细节分配。

2. **训练收敛速度**：虽然训练耗时仅为训练两个独立模型的一半，但单次训练需覆盖更宽的虚拟距离范围（s_v ∈ [1,10]），收敛速度可能稍慢于标准 3DGS。

3. **大规模场景扩展受限**：方法尚未与 chunk-based 加载方案（如 Octree-GS）深度集成。在超大规模场景中，即使远距离基元数量减少，视锥体内总基元数仍可能因场景范围增大而膨胀。

4. **压缩策略未充分探索**：σ_d,i 参数本身仅占 1.6% 存储，但未进一步探索与该参数相关的压缩或量化策略，也未利用衰减因子进行更激进的基元复用。

### 开放问题

- 如何将距离衰减扩展为多模态感知特征（注视方向、运动速度、GPU 负载）驱动的自适应 LOD？
- 能否将 σ_d,i 与基于梯度的基元重要性联合优化，在训练中实现更彻底的基元复用与剪枝？
- 在超大规模场景中，如何结合 octree 等空间层级结构减少视锥体内基元总数，同时保持连续 LOD 的灵活性？
- 连续衰减机制是否可以反向用于近视野超分辨（提升近处基元的细节表现），实现双向连续 LOD？



## 原文 PDF

![[paperPDFs/ICLR_2026/CLoD_GS_Continuous_Level_of_Detail_via_3D_Gaussian_Splatting_36e8ba656c10.pdf]]
