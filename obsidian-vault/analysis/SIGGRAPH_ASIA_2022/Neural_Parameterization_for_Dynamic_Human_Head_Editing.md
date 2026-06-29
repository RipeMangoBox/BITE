---
title: Neural Parameterization for Dynamic Human Head Editing
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2022/Neural_Parameterization_for_Dynamic_Human_Head_Editing.pdf
project_link: null
code_link: null
aliases:
- NPN
- NPDHHE
tags:
- SIGGRAPH_ASIA_2022
- topic/graphics_geometry_processing
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 在隐式MLP中引入显式几何变形层（由稀疏语义关键点控制的线性变形混合）和显式共享纹理图，使模型同时具备隐式的高保真重建与显式的直观编辑能力。
primary_logic: 将动态3D辐射场解耦为密度体、UV体与2D纹理，并通过显式模块（控制点变形场、显式纹理图）与隐式模块（UV/密度MLP、视角/时间残差MLP）的级联，在保持高质量视图合成的同时，允许用户直接操纵关键点或修改纹理图来实现一致的几何与外观编辑。
claims:
- NeP将动态人头分解为密度体、UV体和2D纹理三个组件，实现了几何与外观的解耦。
- 显式几何层被建模为受语义关键点控制的时间变化3D变形场，支持直观编辑。
- 在面部区域，NeP取得了PSNR 30.62、SSIM 0.7998、LPIPS 0.03382的重建指标，在保持编辑性的前提下接近非编辑型NeRF方法。
- 消融实验证明，稀疏损失 L_sparsity 和角度损失 L_angle（权重0.05）对于平衡重建质量与编辑性至关重要。
---

# Neural Parameterization for Dynamic Human Head Editing

> [!tip] 核心洞察
> 将动态3D辐射场解耦为密度体、UV体与2D纹理，并通过显式模块（控制点变形场、显式纹理图）与隐式模块（UV/密度MLP、视角/时间残差MLP）的级联，在保持高质量视图合成的同时，允许用户直接操纵关键点或修改纹理图来实现一致的几何与外观编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向动态人头编辑的神经参数化 |
| 英文题名 | Neural Parameterization for Dynamic Human Head Editing |
| 会议/期刊 | SIGGRAPH ASIA 2022 |
| Links | [paper](https://arxiv.org/abs/2207.00210) |
| Topic | #topic/graphics_geometry_processing #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Neural Parameterization (NeP) |
| Dataset | Face region, Full head |

> [!tip] 效果简介
> - Face region 上，PSNR↑ 30.62 vs 32.61 (DyNeRF) (-1.99)；SSIM↑ 0.7998 vs 0.8381 (DyNeRF) (-0.0383)；LPIPS↓ 0.03382 vs 0.02633 (DFNRMVS) (+0.00749)。
> - Full head 上，PSNR↑ 28.38 vs 29.53 (DyNeRF) (-1.15)；SSIM↑ 0.7964 vs 0.8313 (DyNeRF) (-0.0349)。

## 概要

动态人头编辑面临一个核心矛盾：隐式神经辐射场（NeRF）虽能实现高保真视图合成，但其场景信息完全编码在网络参数中，难以进行直观的细粒度几何与外观编辑。本文提出 **Neural Parameterization (NeP)**，一种混合显式-隐式表示，将动态3D辐射场解耦为三个组件：密度体、UV体与共享的2D纹理。几何端引入由96个语义控制点驱动的显式线性变形混合场，级联隐式UV/密度场；外观端由显式纹理图与视角-时间相关的隐式残差（经稀疏损失约束）相乘构成。该方法在保持接近纯NeRF方法的重建质量（面部区域PSNR 30.62，SSIM 0.7998，LPIPS 0.03382）的同时，允许用户直接操纵控制点或编辑纹理图，实现几何与外观的一致编辑。消融实验表明，稀疏损失和角度保持损失的权重配置对平衡重建质量与可编辑性至关重要。

## 核心方法与创新机理

### 问题瓶颈与设计动机

隐式神经辐射场（NeRF）在动态人头重建中取得了高保真结果，但其场景信息完全编码在MLP网络参数中，形成“黑箱”表示。用户无法直观地编辑几何形状（如改变鼻梁高度）或外观纹理（如添加纹身），因为任何局部修改都需要重新训练整个网络，且缺乏明确的编辑入口。这一根本性矛盾——高保真重建与可编辑性之间的对立——构成了本工作的核心瓶颈。

NeP的解决方案在于**引入混合显式-隐式表示**：在保持隐式模块高表达能力的同时，插入可被用户直接操纵的显式组件。具体而言，NeP将动态辐射场解耦为几何表示$V$和外观表示$T$两个独立模块，并在几何表示中嵌入由稀疏语义控制点驱动的显式变形场，在外观表示中引入所有帧共享的显式2D纹理图。这一设计使得用户可以通过拖动控制点来编辑几何，通过修改纹理图来编辑外观，而无需触及隐式网络参数。

### 核心表示架构

NeP将传统NeRF的单一映射$( \mathbf { c } , \sigma ) = F ( \mathbf { x } , \mathbf { d } , t )$解耦为两个级联的映射：

$$( \mathbf { u } , \sigma ) = V ( \mathbf { x } , t ) , \quad \mathbf { c } = T ( \mathbf { u } , \mathbf { d } , t )$$

其中几何表示$V$将3D空间点$\mathbf{x}$和时间$t$映射到2D纹理坐标$\mathbf{u}$和体积密度$\sigma$；外观表示$T$根据纹理坐标$\mathbf{u}$、视角方向$\mathbf{d}$和时间$t$输出RGB颜色$\mathbf{c}$。这一解耦的关键意义在于：**UV坐标$\mathbf{u}$成为几何与外观之间的桥梁**，使得对几何的编辑（改变$\mathbf{u}$的映射关系）和对纹理的编辑（修改$T$的像素值）可以独立进行，同时保持时空一致性。

### 几何表示：显式变形场级联隐式UV/密度场

几何表示$V$由两个级联的子模块组成：显式变形场$V_E$和隐式UV/密度场$V_I$。

$$V = V _ { I } ( \mathbf { x } ^ { \prime } , t ) , \quad \mathbf { x } ^ { \prime } = V _ { E } ( \mathbf { x } , t )$$

**显式变形场$V_E$** 采用线性变形混合（Linear Blend Skinning）的简化形式，由96个具有语义含义的控制点驱动（如图3所示，控制点分布在眉毛、鼻翼、嘴唇、下颌等关键面部区域）。对于每个控制点$i$，定义其在规范空间中的位置$\bar{\mathbf{s}}_i$和变形后的位置$\bar{\mathbf{z}}_i$，则任意空间点$\bar{\mathbf{x}}$的变形由高斯RBF加权插值得到：

$$V _ { E } ( \mathbf { x } ) = \bar { \mathbf { x } } + \frac { \sum _ { i } \psi _ { i } ( \bar { \mathbf { x } } ) ( \bar { \mathbf { z } } _ { i } - \bar { \mathbf { s } } _ { i } ) } { \sum _ { i } \psi _ { i } ( \bar { \mathbf { x } } ) }$$

其中权重函数为：

$$\psi _ { i } ( \bar { \mathbf { x } } ) = \exp \left( - ( \bar { \mathbf { x } } - \bar { \mathbf { s } } _ { i } ) ^ { 2 } / r _ { i } ^ { 2 } \right)$$

$r_i$为控制点$i$的影响半径。这一设计的核心优势在于：**用户只需拖动控制点的3D位置$\bar{\mathbf{z}}_i$，即可实现局部、平滑的几何编辑**，变形通过高斯权重自然衰减，避免了不连续的边界伪影。

为防止控制点在优化过程中漂移到无意义位置，NeP引入语义损失约束控制点与预跟踪的3D人脸网格顶点保持一致：

$$\mathcal { L } _ { s e m a n t i c } = \sum _ { i } \sum _ { t } \| \mathbf { s } _ { i } ^ { ( t ) } - \hat { \mathbf { s } } _ { i } ^ { ( t ) } \| _ { 2 }$$

**隐式UV/密度场$V_I$** 接收经$V_E$变形后的规范空间坐标$\mathbf{x}'$和时间$t$，通过MLP输出UV坐标$\mathbf{u}$和体积密度$\sigma$。该MLP继承了NeRF的高表达能力，能够捕捉显式变形无法覆盖的细节几何（如皱纹、皮肤微结构）。值得注意的是，消融实验（Figure 13）表明，显式变形层$V_E$不仅实现了编辑功能，还**意外地提升了辐射场的重建清晰度**——作者推测这是因为$V_E$提供了一个有效的几何先验，减轻了隐式MLP的优化负担。

### 外观表示：显式纹理图与隐式残差的双层结构

外观表示$T$采用双层设计，兼顾编辑性与表达能力：

$$T(\mathbf{u}, \mathbf{d}, t) = T_E(\mathbf{u}) * \exp(T_I(\mathbf{u}, \mathbf{d}, t))$$

**显式纹理图$T_E(\mathbf{u})$** 是一个所有帧共享的2D图像，存储了人头的基础外观（皮肤颜色、眉毛、静态纹理等）。用户可以直接在$T_E$上绘制或修改像素，实现纹身添加、肤色改变等外观编辑。

**隐式纹理残差$T_I(\mathbf{u}, \mathbf{d}, t)$** 是一个MLP，建模视角相关的光照效果（如高光）和时间相关的动态细节（如眨眼时的眼睑褶皱）。$T_I$的输出经过指数映射后与$T_E$相乘，使得残差以乘性方式调制基础纹理。这一设计的精妙之处在于：**通过稀疏损失强制$T_I$大部分为零**，使$T_E$在多数区域和时刻占主导地位，从而保证编辑的一致性：

$$\mathcal{L}_{sparsity} = \sum_{k} |T_I(\mathbf{u}_k, \mathbf{d}_k, t)|$$

当用户在$T_E$上绘制时，修改会通过乘法传递到所有帧，而$T_I$仅在必要时（如高光区域）提供微小调制，不会覆盖用户的编辑。

### 训练策略与正则化

NeP的训练涉及多个损失函数的联合优化，其中三个正则化项对编辑性至关重要：

**UV引导损失** 利用预跟踪的3D人脸网格提供的UV坐标作为粗先验，防止UV映射崩溃：

$$\mathcal { L } _ { u v } = \sum _ { i } ^ { P } \| V ( \mathbf { p } _ { i } , t ) - \mathbf { u } _ { i } \| _ { 2 }$$

**循环一致性损失** 通过逆向映射网络$V_I^{-1}$将UV坐标映射回3D空间，约束正向和逆向映射的一致性，保证UV空间与3D表面之间的双射性：

$$\mathcal { L } _ { c y c l e } = \sum _ { i } ^ { B } \| \mathbf { x } _ { i } ^ { \prime } - \hat { \mathbf { x } } _ { i } ^ { \prime } \| _ { 2 }$$

**角度保持损失** 约束UV映射在表面切平面上的梯度正交，实现共形参数化，避免纹理拉伸扭曲：

$$\mathcal { L } _ { a n g l e } = \sum _ { i } ^ { B } \frac { \left| \nabla _ { \mathbf { x } } \mathbf { u } _ { \perp } \cdot \nabla _ { \mathbf { x } } \mathbf { v } _ { \perp } \right| } { \left\| \nabla _ { \mathbf { x } } \mathbf { u } _ { \perp } \right\| \left\| \nabla _ { \mathbf { x } } \mathbf { v } _ { \perp } \right\| }$$

消融实验（Figure 10）表明，$\lambda_{angle}=0.05$实现了重建质量与编辑性的最佳权衡：更小的权重导致UV映射噪声，更大的权重则导致模型发散。

![[assets/figures/papers/paper_list_l70_https_arxiv_org_abs_2207_00210/figures/008_Figure_10.jpg]]
*Figure 10: Visualizations under different settings of*

**两阶段训练策略** 进一步提升了时序一致性：第一阶段固定$T_I$为常数（仅学习时间无关的外观），第二阶段再优化$T_I$捕捉时序变化。这一策略有效减少了动态纹理的时序抖动，尤其在眼睛和嘴部区域改善显著。

### 体渲染与端到端优化

最终的像素颜色通过标准体渲染方程合成：

$$\hat{\mathbf{c}} = \sum_{i=1}^{N} T_i (1 - \exp(-\sigma_i \delta_i)) \mathbf{c}_i, \quad T_i = \exp\left(-\sum_{j=1}^{i-1} \sigma_j \delta_j\right)$$

采用两层分层采样策略（粗采样64点+重要性采样64点），并通过MSE损失监督RGB和alpha遮罩：

$$\mathcal{L}_{MSE} = \sum_{i}^{B} \left( \lVert \mathbf{c}_i - \hat{\mathbf{c}}_i \rVert_2 + \lVert \alpha_i - \hat{\alpha}_i \rVert_2 \right)$$

整个系统端到端可微，训练在3块V100 GPU上约需一天。

### Changed Slots 总结

相对于纯隐式NeRF基线，NeP在两个关键表示槽位上进行了替换：

1. **几何表示槽位**：从“纯隐式MLP”替换为“显式变形场（96个语义控制点驱动的线性变形混合）级联隐式UV/密度场”，赋予模型直观的几何编辑能力，同时意外提升了重建清晰度。

2. **外观表示槽位**：从“隐式MLP直接输出颜色”替换为“显式纹理图（所有帧共享）与视角/时间相关的隐式残差（经稀疏损失约束）的乘性组合”，使纹理编辑成为可能，同时通过残差保留必要的动态细节。

这两个槽位的改变通过UV坐标$\mathbf{u}$的桥梁作用实现协同：几何编辑改变$\mathbf{u}$的映射，外观编辑改变$T_E(\mathbf{u})$的像素值，二者独立操作却统一在同一个辐射场框架下，最终通过体渲染产生一致的编辑结果。

![[assets/figures/papers/paper_list_l70_https_arxiv_org_abs_2207_00210/figures/017_Figure_17.jpg]]
*Figure 17: Results of a challenging mouth example. The inset visualizes the reconstructed depth map of the mouth region. Our method tends to model the mouth interior using coarse geometry and view dependent textures*

## 实验与关键发现

### 主结果：重建质量与编辑性的权衡

Table 1 给出了多视角动态人头重建的定量评估。由于 NeP 为保持编辑性引入了显式几何层、稀疏纹理残差和角度保持损失等正则化项，其重建指标相比纯隐式 NeRF 方法存在一定差距，但下降幅度可控。在面部区域，NeP 取得 **PSNR 30.62 / SSIM 0.7998 / LPIPS 0.03382**，对比 DyNeRF 的 PSNR 32.61 / SSIM 0.8381，PSNR 下降约 1.99 dB，SSIM 下降约 0.038；LPIPS 相比最好的 DFNRMVS（0.02633）增加约 0.0075。在全头区域，NeP 的 PSNR 为 28.38，较 DyNeRF（29.53）低 1.15 dB。这些差距主要来源于强制将隐式残差限制为稀疏、以及显式 UV 映射的共形约束，二者共同牺牲了部分高频细节以换取直观编辑能力。

![[assets/figures/papers/paper_list_l70_https_arxiv_org_abs_2207_00210/figures/005_Table_1.jpg]]
*Table 1: Reconstruction and texture temporal alignment. Our approach is slightly inferior to the NeRF-based methods due to the regularization for improving editability. Overall, our method achieves the best trade-off between reconstruction and editability. (Invalid cells are denoted as −. ↑ means higher values are better.) 一 1 F Fullhe*

值得注意的是，NeP 在牙齿等细节区域的重建略逊于 NeRF 方法，但在其他区域由于显式变形层的引入反而更清晰（见 Figure 5 和消融分析）。总体而言，NeP 在重建质量与编辑性之间实现了最佳权衡：所有纯 NeRF 方法完全不可编辑，而可编辑的 DFNRMVS 方法在重建指标和时序一致性上均弱于 NeP。

![[assets/figures/papers/paper_list_l70_https_arxiv_org_abs_2207_00210/figures/006_Figure_5.jpg]]
*Figure 5: Novel view synthesis results. Each row shows the results of one subject. Ours enables editing of the full head while achieving similar rendering results to NeRF-based methods. Some regions of ours, such as the teeth are less detailed, while other regions often outperform NeRF-based methods due to the use of the explicit deformation field*

### 时序纹理对齐评估

Table 1 同时报告了纹理时序对齐指标。NeP 通过两阶段训练策略（先固定显式纹理为时间无关、后联合优化动态隐式残差）显著减少了动态纹理中的时序变化，尤其在眼睛和嘴部区域实现了更好的时序对齐。Figure 6 的 UV checker 叠加可视化进一步验证了这一点：在连续帧中，标注点（红色箭头）在 UV 空间的位置保持高度一致，表明 NeP 的 UV 映射具有优越的时序稳定性。

![[assets/figures/papers/paper_list_l70_https_arxiv_org_abs_2207_00210/figures/007_Figure_6.jpg]]
*Figure 6: Visualizations of UV checker overlay. In each column, we show a frame of the same sequence. We highlight an equivalent point on the UV checker with a red arrow. Our UV mapping achieves better temporal consistency*

### 关键消融实验

**稀疏损失 L_sparsity 的权重选择。** 核心设计意图是将时序变化建模为隐式残差 T_I，使显式纹理 T_E 保持稳定以便编辑。消融实验（Figure 8）表明：λ_sparsity 过小会导致 T_I 承载过多时序信息，编辑 T_E 后时序一致性下降；λ_sparsity 过大则会消除重要的时序变化（如眨眼、微表情），导致重建失真。实验确定 λ_sparsity = 0.05 为最优值。

**角度保持损失 L_angle 的权重选择。** L_angle 约束 UV 映射在表面切平面上的梯度正交，以实现共形参数化，这对纹理编辑的自然性至关重要。Figure 10 的消融显示：λ_angle 过小（如 0.01）时重建质量虽好，但 UV 映射噪声大，纹理编辑时出现拉伸伪影；λ_angle 过大（如 0.1）则导致训练发散。λ_angle = 0.05 实现了重建质量与编辑性的最佳权衡。

**两阶段训练策略。** 第一阶段固定 T_E 为时间无关，仅优化 T_I 的时序残差；第二阶段联合优化二者。消融表明，该策略有效减少了动态纹理中的时序变化，改善了嘴部和眼部区域的对齐精度，是保证编辑一致性的关键设计。

**显式变形层 V_E 的贡献。** 虽然 V_E 的设计初衷是使能几何编辑，但消融实验（Figure 13）揭示了一个额外收益：移除 V_E 后，辐射场的重建趋于模糊。这表明显式变形层通过提供结构化的几何先验，实际上提升了隐式场的重建清晰度，形成了编辑性与重建质量的正向协同而非单纯权衡。

### 编辑能力验证

NeP 支持三种编辑模式：

- **外观编辑**（Figure 11）：用户直接修改显式纹理图 T_E（如添加纹身、改变妆容），修改自动传播到所有帧，隐式残差 T_I 保持原有的视角和时序变化。由于 T_E 为所有帧共享，编辑结果具有天然的一致性。
- **几何编辑**（Figure 14）：用户拖拽控制点（96 个语义关键点，见 Figure 3），显式变形场 V_E 通过高斯 RBF 加权的线性变形混合将编辑传播到局部区域。编辑后的几何通过级联的隐式 UV/密度场保持拓扑一致性。
- **联合编辑**（Figure 15）：同时修改纹理和控制点，实现几何与外观的协同编辑。Figure 18 展示了表情和头发编辑的扩展案例，通过增加额外控制点来编辑头发区域。

![[assets/figures/papers/paper_list_l70_https_arxiv_org_abs_2207_00210/figures/003_Figure_3.jpg]]
*Figure 3: A visualization of the 96 control points. The control points are manually selected and have rich semantic meaning*

### 失败模式与适用边界

**口腔内部等复杂区域。** Figure 17 揭示了 NeP 的一个典型失败模式：口腔内部被建模为粗糙的几何和视角相关的纹理，深度图过平滑。这是因为训练视角有限（11 个训练视图），口腔内部的多视角覆盖不足，导致隐式场倾向于用视角相关的颜色变化来补偿几何精度的缺失，而非学习精确的内部几何。

**拓扑变化限制。** 显式变形场采用线性变形混合，本质上是控制点位移的平滑插值，无法处理拓扑变化（如张嘴时口腔从闭合到开放的拓扑改变）。这限制了表情编辑的能力范围，使其更适用于面部表面变形而非大幅度拓扑改变。

**光照与材质不可分离。** 外观表示将光照效果烘焙到视角相关的隐式残差 T_I 中，无法独立编辑材质属性和光照条件。这意味着用户无法直接修改皮肤反射率或重新打光，所有外观编辑必须在当前烘焙光照的约束下进行。

**训练效率。** 在 3 块 V100 GPU 上训练约需一天，限制了在需要快速迭代的实时应用场景中的实用性。

### 证据强度评估

主结果中的定量指标（PSNR、SSIM、LPIPS）来自 Table 1，置信度 0.98，数据可靠。消融实验的结论（λ_sparsity、λ_angle 的最优值、两阶段训练效果、V_E 对重建质量的提升）均有对应可视化（Figure 8、10、13）和定性分析支撑，置信度 0.95。失败模式中的口腔内部问题有 Figure 17 的深度图可视化作为直接证据；拓扑变化限制和光照不可分离性来自方法设计的固有约束，属于结构性限制而非实验发现。训练时间数据仅提及“约一天”，缺少精确计时和与其他方法的对比，需手动验证。

## 定位与知识库关联

### 相对于已有方法的本质差异

NeP 的核心定位是在**高保真动态人头重建**与**直观可编辑性**之间建立一个可操作的折中方案。已有方法在这两个目标上通常只能取其一：

- **纯隐式动态 NeRF 方法**（如 **HyperNeRF** 与 **DyNeRF**）将场景的所有几何和外观信息完全编码在 MLP 的网络权重中。这类方法在视图合成质量上处于领先地位（Table 1 中 DyNeRF 在面部区域 PSNR 达 32.61），但用户无法对重建结果进行任何有意义的几何变形或外观修改——编辑入口根本不存在。
- **可编辑的多视图立体 / 3D 人脸重建方法**（如 **DFNRMVS** 与 **HiFi3D**）虽然提供了基于网格或参数化模型的编辑接口，但其重建保真度受限于显式几何表示的表达能力，难以捕捉头发、皮肤微几何等复杂结构。

NeP 改变的**关键 slot** 是**几何表示与外观表示的耦合方式**：将原本完全隐式的 `(c, σ) = F(x, d, t)` 映射，替换为**显式变形场 + 隐式 UV/密度场 + 显式纹理图 + 隐式纹理残差**的级联解耦结构。这一改变使得模型在保持体渲染管线高保真重建能力的同时，将编辑操作锚定在用户可直接操纵的显式组件上——移动语义控制点即可变形几何，修改 2D 纹理图即可改变外观。

### 知识库挂载点

NeP 可挂载到知识库的以下节点：

1. **可编辑神经辐射场（Editable NeRF）**  
   与现有的基于隐式编码编辑的方法（如通过修改 latent code 或条件输入来改变 NeRF 输出）不同，NeP 提供了一种**显式参数化接口**：通过 96 个语义控制点驱动的线性变形混合（Linear Blending Skinning with Gaussian RBF weights）实现局部几何编辑，通过共享的 2D 纹理图实现外观编辑。这种设计将编辑操作从“黑盒优化”转变为“直接操纵”，降低了编辑门槛。

2. **动态场景的 UV 参数化**  
   NeP 将动态 3D 辐射场映射到一致的 2D UV 空间，并通过角度保持损失 $\mathcal{L}_{angle}$ 约束 UV 映射的共形性、通过循环一致性损失 $\mathcal{L}_{cycle}$ 保证 UV 空间与 3D 空间的双射性。这为“在 2D 域编辑、在 3D 域渲染”的范式提供了动态场景下的可行方案。

3. **神经纹理（Neural Texture）的稀疏化**  
   外观表示 $T(\mathbf{u}, \mathbf{d}, t) = T_E(\mathbf{u}) \cdot \exp(T_I(\mathbf{u}, \mathbf{d}, t))$ 将时间/视角变化建模为乘性残差，并通过稀疏损失 $\mathcal{L}_{sparsity}$ 迫使 $T_I$ 趋近于零。这确保了显式纹理 $T_E$ 承载了大部分外观信息，使得纹理编辑的“所见即所得”成为可能——编辑 $T_E$ 后，残差 $T_I$ 仅需补偿少量视角/时间效应即可保持一致性。

### 适用边界

NeP 的适用性存在以下明确边界：

- **训练时间成本**：在 3 块 V100 GPU 上约需一天，限制了其在需要快速迭代的场景中的实用性。这一瓶颈来自体渲染管线和多个损失项的联合优化，而非网络规模本身。
- **拓扑变化的处理能力有限**：显式变形场 $V_E$ 基于线性变形混合，本质上是一种保持拓扑的变形。对于张嘴等涉及拓扑变化的动作，口腔内部被建模为粗糙几何 + 视角相关纹理（Figure 17 显示深度图过平滑），无法产生真实的内部结构。
- **材质与光照不可分离**：外观表示将光照效果烘焙到视角相关的隐式残差 $T_I$ 中，无法独立编辑材质属性或重新打光。这意味着 NeP 的编辑能力停留在“纹理绘制”层面，而非物理可解释的材质编辑。
- **依赖于多视图同步视频输入**：训练需要 11 个同步相机视角，数据采集门槛较高，限制了其在消费级场景中的直接应用。

### 后续启发与延伸方向

NeP 的设计决策揭示了几个值得关注的后续方向：

1. **可变形神经表示的拓扑扩展**  
   当前线性变形混合无法处理拓扑变化，一个自然的延伸是将显式变形模块替换或增强为可处理拓扑变化的表示（如基于 cage 的变形、隐式曲面变形或神经隐式变形场），以支持张嘴等更丰富的表情编辑。

2. **物理光照与材质的解耦**  
   将外观表示中的视角/时间依赖残差替换为基于物理的渲染（PBR）模型，使 $T_I$ 输出的是法线、粗糙度、镜面反射等物理参数而非直接的颜色残差。这将使 NeP 的编辑能力从“纹理绘制”升级为“材质编辑 + 重打光”。

3. **加速训练与推理**  
   利用现有的 NeRF 加速技术（如多分辨率哈希编码、张量分解、蒸馏到显式网格等）来缩短训练时间，是提升实用性的直接路径。但需要注意这些加速方案是否与显式变形层和 UV 参数化的约束兼容。

4. **控制点的自动选取与泛化**  
   当前 96 个控制点是手动选取的，且语义损失 $\mathcal{L}_{semantic}$ 依赖预训练的 3D 人脸跟踪器提供的网格顶点约束。如何在不同人物、不同头部拓扑上自动确定控制点位置和影响半径 $r_i$，是将该方法泛化到更大规模数据集的关键。

5. **作为神经资产管线的中间表示**  
   NeP 输出的 UV 体和纹理图天然适合导入传统 CG 管线（如游戏引擎、3D 建模软件），可视为从多视图视频到可编辑 3D 资产的“神经烘焙”步骤。这一角色使 NeP 在虚拟人制作、影视后期等领域具有潜在的流程嵌入价值。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2022/Neural_Parameterization_for_Dynamic_Human_Head_Editing.pdf]]