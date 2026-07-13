---
title: Motion-Aware Animatable Gaussian Avatars Deblurring
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Motion_Aware_Animatable_Gaussian_Avatars_Deblurring.pdf
project_link: null
code_link: "https://github.com/MyNiuuu/MAD-Avatar"
aliases:
- MAAGADMA
- MAAGAD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 三维运动感知的模糊形成模型与SMPL子帧运动联合优化
primary_logic: 将传统二维模糊形成过程扩展为三维感知的物理模型，结合SMPL人体运动先验对子帧运动和规范头像进行联合优化，从根本上消除运动模糊的歧义，实现从模糊视频直接重建清晰、可动画的3D高斯头像。
claims:
- 在合成和真实数据集上，所提方法显著优于直接训练3DGS头像的基线及先去模糊后重建的两阶段方法，PSNR提升超过2.4 dB。
- 消融实验证实每个组件（子帧插值、姿态形变、LBS优化、形状优化）对最终性能均有贡献。
- 帧间运动正则化损失有效解决了运动方向歧义，大幅提升非中间时刻的渲染质量。
- Synthetic Dataset (ZJU-MoCap) 上 PSNR↑ = 25.546
---

# Motion-Aware Animatable Gaussian Avatars Deblurring

> [!tip] 核心洞察
> 将传统二维模糊形成过程扩展为三维感知的物理模型，结合SMPL人体运动先验对子帧运动和规范头像进行联合优化，从根本上消除运动模糊的歧义，实现从模糊视频直接重建清晰、可动画的3D高斯头像。

| 字段 | 内容 |
|------|------|
| 中文题名 | 运动感知的可动画高斯头像去模糊 |
| 英文题名 | Motion-Aware Animatable Gaussian Avatars Deblurring |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2411.16758) · [Code](https://github.com/MyNiuuu/MAD-Avatar) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Motion-Aware Animatable Gaussian Avatars Deblurring (MAD-Avatar) |
| Dataset | Synthetic Dataset, Real Dataset |

> [!tip] 效果简介
> - Synthetic Dataset (ZJU-MoCap) 上，PSNR↑ 25.546 vs 23.080 (GauHuman) (+2.466)。
> - Synthetic Dataset 上，SSIM↑ 0.8290 vs 0.7660 (GauHuman) (+0.0630)；LPIPS↓ 0.1476 vs 0.2277 (GauHuman) (-0.0801)。
> - Real Dataset 上，PSNR↑ 27.010 vs 25.602 (GauHuman) (+1.408)。

## 概要

从模糊视频中重建清晰、可动画的三维人体头像，面临一个根本性挑战：**运动模糊在几何与运动估计中引入了严重的歧义**。当相机曝光时间内人体发生非刚性运动时，二维图像上的模糊痕迹无法唯一地反推出三维姿态与形状——同一模糊观测可能对应多种截然不同的运动解释（Figure 1）。现有方法要么直接忽略模糊，在退化数据上训练三维高斯泼溅（3DGS）头像，导致纹理失真与几何坍塌；要么采用“先去模糊、后重建”的两阶段策略，但因二维去模糊缺乏多视图一致性，无法从根本上消除歧义。

**MAD-Avatar**（Motion-Aware Animatable Gaussian Avatars Deblurring）提出了一种三维感知的运动去模糊框架，核心思路是将传统的二维模糊形成过程扩展为**物理驱动的三维模糊形成模型**，并与**基于SMPL的子帧运动表示**联合优化。具体而言，该方法将曝光时间内的模糊图像建模为多张虚拟清晰子帧渲染结果的平均，这些子帧由规范空间中的3DGS头像根据估计的子帧SMPL姿态变形生成。通过B样条姿态插值、姿态形变CNN、LBS权重细化和帧间测地距离正则化，框架从粗糙的SMPL初始化出发，联合优化头像表示与运动参数，从根本上消除运动模糊的歧义。

实验表明，MAD-Avatar在合成数据集（ZJU-MoCap）和自建真实多视角数据集上均显著优于直接训练3DGS头像的基线方法（如**GauHuman**，Zhe Li et al., CVPR 2024）以及多种“2D去模糊+3D重建”的两阶段方案（包括**ShiftNet**、**RVRT**、**VRT**、**BSST**与GauHuman的组合）。在合成数据集上，PSNR提升超过2.4 dB（25.546 vs. 23.080），LPIPS降低0.08（0.1476 vs. 0.2277）；在真实数据集上，PSNR达到27.010，LPIPS降至0.1668。消融实验证实，子帧插值、姿态形变、LBS优化、形状优化以及帧间运动正则化每个组件对最终性能均有贡献，其中帧间正则化损失对消除运动方向歧义、提升非中间时刻渲染质量尤为关键。该方法还支持从模糊视频中恢复的清晰头像进行新姿态动画合成（如AMASS数据集驱动的动作），并可在iPhone 16 Pro等消费级设备采集的模糊视频上展示应用潜力。

**方法定位**：MAD-Avatar属于三维感知去模糊与可动画头像重建的交叉领域。与纯二维去模糊方法不同，它在三维规范空间中进行物理建模，利用人体运动先验（SMPL）约束解空间；与标准3DGS头像方法不同，它不假设输入为清晰图像，而是将模糊形成显式纳入渲染管线，实现从模糊观测到清晰表示的端到端联合优化。该方法需要多视角同步相机系统和粗略的SMPL初始化，对极端模糊、宽松服装等超出SMPL建模能力的情况尚未充分验证，单目视频扩展和实时推理是未来方向。



### 问题背景：运动模糊对3D头像重建的挑战

从多视角视频中重建逼真的可动画人体头像，是计算机视觉与图形学领域的核心课题之一。近年来，以3D高斯泼溅（3D Gaussian Splatting, 3DGS）为代表的显式神经表示方法，凭借其高质量实时渲染能力，在静态场景重建中取得了突破性进展。然而，当输入视频帧包含**运动模糊**时，3DGS头像的重建质量会急剧下降。

运动模糊的根源在于相机曝光时间内被摄对象的持续运动。这一物理过程在图像中引入方向性拖影，使得单帧像素值成为曝光周期内多个清晰时刻的累积混合。对于人体而言，四肢的快速摆动、身体的旋转等非刚性运动，会在不同视角下产生高度不一致的模糊模式。如Figure 1所示，当从模糊帧重建清晰的3DGS头像时，运动引发的模糊会引入严重的**运动歧义**：同一模糊观测可能对应完全不同的运动轨迹和几何形状，导致重建结果出现纹理失真、几何塌缩等伪影。

### 现有方法的缺口

当前处理运动模糊的主流策略可分为两类，但均存在根本性局限：

**（1）直接训练法**：将模糊帧直接输入标准3DGS头像模型（如**GauHuman**, Zhe Li et al., CVPR 2024）进行训练。由于模型缺乏对模糊形成过程的显式建模，优化过程无法区分模糊与清晰信号，最终学习到的是模糊化的纹理和错误的几何结构。

**（2）两阶段法**：先使用2D去模糊网络（如**ShiftNet**, Dasong Li et al., CVPR 2023; **RVRT**, Jingyun Liang et al., NeurIPS 2022; **VRT**, Jingyun Liang et al., TIP 2024; **BSST**, Huicong Zhang et al., CVPR 2024）对视频帧逐帧去模糊，再训练3DGS头像。这一策略面临两个致命缺陷：其一，2D去模糊缺乏多视图一致性约束，不同视角的去模糊结果相互矛盾，为后续3D重建引入不可调和的几何冲突；其二，2D去模糊丢失了运动信息，而这些信息恰恰是理解人体动态、优化SMPL姿态参数的关键线索。

此外，现有方法普遍依赖离线估计的固定SMPL参数（如EasyMocap输出），无法在训练过程中修正因模糊导致的姿态估计误差，进一步加剧了几何重建的不准确性。

### 核心瓶颈与本文动机

上述分析揭示了一个根本性瓶颈：**运动模糊在3DGS头像重建中引入了严重的运动歧义，导致几何纹理失真和SMPL参数估计错误，而现有方法无法同时处理去模糊与高质量头像重建**。

这一瓶颈的因果机制在于：模糊图像的形成是一个三维物理过程——曝光时间内人体在三维空间中运动，经相机投影后累积为二维模糊信号。仅在二维层面进行去模糊或完全忽略模糊建模，都无法恢复运动过程中丢失的三维几何与纹理信息。因此，解决问题的关键在于**将模糊形成过程建模为三维感知的物理模型**，并利用人体运动先验对模糊周期内的子帧运动进行合理推断。

基于此，本文提出**MAD-Avatar**（Motion-Aware Animatable Gaussian Avatars Deblurring），核心思路是将传统的二维模糊形成过程扩展为三维感知的物理模型，结合SMPL人体运动先验对子帧运动和规范头像进行联合优化，从根本上消除运动模糊的歧义，实现从模糊视频直接重建清晰、可动画的3D高斯头像。



## 核心方法与创新机理

MAD-Avatar 的核心创新在于将运动模糊从一个二维图像退化问题重新定义为一个**三维运动感知的物理形成过程**，并利用人体运动先验从根本上消除运动歧义。具体而言，该方法在三处关键设计上区别于现有基线。

**1. 三维感知的模糊形成模型**

现有方法（如 GauHuman）直接使用模糊帧训练 3DGS 头像，或采用先二维去模糊再重建的两阶段流水线（如 ShiftNet + GauHuman、RVRT + GauHuman、VRT + GauHuman、BSST + GauHuman），均未在三维空间中建模模糊的物理成因。MAD-Avatar 则引入了一个基于物理的模糊形成模型：将曝光时间内的模糊图像建模为若干虚拟清晰子帧的平均，即

$$\mathbf { I } ^ { B } = \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \mathcal { R } ( \mathcal { W } ( \{ G _ { k } ( \mathbf { x } ) \} _ { k = 0 } ^ { K - 1 } , S _ { t } ) , \mathbf { R } , \mathbf { K } ).$$

该公式将规范空间的 3D 高斯根据子帧时刻的 SMPL 参数 $S_t$ 变形到世界空间，渲染为虚拟清晰图像后再平均，从而合成模糊图像。这一设计使去模糊与三维重建在统一的物理框架下联合优化，避免了二维去模糊因缺乏多视图一致性而导致的性能瓶颈。

**2. 基于 SMPL 的子帧运动联合优化**

基线方法使用 EasyMocap 离线估计的固定 SMPL 参数，无法处理曝光周期内的精细运动。MAD-Avatar 则构建了一个可学习的子帧运动模型，包含三个层次：

- **B 样条姿态插值**：通过 De Boor–Cox 插值矩阵 $\mathcal{M}^P$ 和可学习的控制节点，为曝光周期内的每个子帧生成连续的关节姿态 $\hat{\Theta}_t^j$。
- **姿态形变 CNN**：预测高频非刚性运动位移 $\Delta_t^j$，弥补 B 样条对复杂运动的表达能力不足，最终姿态为 $\Theta_t^j = \hat{\Theta}_t^j + \Delta_t^j$。
- **SMPL 参数联合优化**：在训练过程中同步优化形状参数 $\beta$ 和 LBS 蒙皮权重 $\hat{\pmb{B}} = \tilde{\pmb{B}} + \delta$，而非固定使用预估值。

**3. 帧间运动正则化消除方向歧义**

运动模糊的歧义性不仅体现在单帧内部，更体现在相邻帧之间的运动方向不确定性（如 Figure 1 所示）。MAD-Avatar 引入了帧间测地距离正则化损失 $\mathcal{L}_{reg}$，约束当前曝光周期末帧姿态与下一曝光周期首帧姿态的一致性：

$$\mathcal { L } _ { r e g } = \frac { 1 } { 2 4 \cdot ( N _ { e } - 1 ) } \sum _ { n = 0 } ^ { N _ { e } - 2 } \sum _ { j = 0 } ^ { 2 3 } \left| \hat { \mathbf { \Theta } } _ { n , T - 1 } ^ { j } - \hat { \mathbf { \Theta } } _ { n + 1 , 0 } ^ { j } \right| _ { \mathrm { G } }.$$

消融实验证实，该正则化显著提升了非中间时刻的渲染质量（Table 4, Figure 8），是消除运动方向歧义的关键设计。

**创新总结**

上述三个 changed slot 形成了因果闭环：三维模糊形成模型提供了去模糊的物理基础，子帧运动模型提供了可优化的运动表示，帧间正则化则消除了运动歧义。三者协同使得从模糊视频直接重建清晰、可动画的 3D 高斯头像成为可能，在合成和真实数据集上 PSNR 分别提升超过 2.4 dB 和 1.4 dB（Table 2）。



MAD-Avatar 的核心思路是将二维运动模糊的歧义性问题提升到三维空间，通过物理感知的模糊形成模型与人体运动先验的联合优化，从多视角模糊视频中直接重建清晰、可动画的3D高斯头像。整体管道如图2所示，包含四个紧密耦合的模块。

**输入与输出**：系统输入为多视角同步相机拍摄的模糊视频帧，以及由 EasyMocap 离线估计的粗粒度 SMPL 参数（姿态、形状）。输出是一个规范空间下的清晰 3DGS 头像，以及优化后的子帧级 SMPL 运动序列，可直接驱动新姿态动画。

**管道流程**：

1. **子帧运动建模**（Sec 3.2）：对于每一帧模糊图像，利用 B 样条插值在曝光周期内生成 $T$ 个虚拟子帧时刻的 SMPL 姿态。具体而言，B 样条以 $P$ 个控制节点为基础，通过插值矩阵 $\mathcal{M}^P$ 计算关节 $j$ 在时刻 $t$ 的插值姿态 $\hat{\Theta}_t^j$，再由姿态形变 CNN $G_{disp}$ 预测高频非刚性位移 $\Delta_t^j$，二者相加得到最终子帧姿态 $\Theta_t^j = \hat{\Theta}_t^j + \Delta_t^j$。这一设计解决了独立优化各子帧姿态导致的运动无序问题。

2. **三维模糊形成**（Sec 3.1）：将规范空间下的 3D 高斯集合 $\{G_k(\mathbf{x})\}_{k=0}^{K-1}$ 根据各子帧的 SMPL 参数 $S_t$ 进行线性混合蒙皮（LBS）变形，渲染得到 $T$ 张虚拟清晰图像，再取平均合成模糊图像：
   $$\mathbf{I}^B = \frac{1}{T}\sum_{t=0}^{T-1} \mathcal{R}\big(\mathcal{W}(\{G_k(\mathbf{x})\}_{k=0}^{K-1}, S_t), \mathbf{R}, \mathbf{K}\big)$$
   其中 $\mathcal{R}$ 为可微光栅化渲染器，$\mathbf{R}$、$\mathbf{K}$ 为相机外参和内参。这一物理模型将去模糊问题转化为三维运动估计与重建的联合优化问题。

3. **帧间运动正则化**（Eq 9）：通过测地距离损失 $\mathcal{L}_{reg}$ 约束相邻曝光周期边界姿态的一致性——即前一帧曝光结束时刻（$T-1$）的姿态与后一帧曝光开始时刻（$0$）的姿态应接近，从而消除运动方向的歧义性。消融实验（Table 4, Figure 8）证实，该正则化对非中间时刻的渲染质量至关重要。

4. **SMPL 参数联合优化**（Sec 3.2-3.3）：在训练过程中，不仅优化规范 3DGS 和子帧运动，还同步优化 SMPL 的形状参数 $\hat{\beta}$、姿态控制节点以及 LBS 权重偏移量 $\delta$（Eq 10: $\hat{\mathbf{B}} = \tilde{\mathbf{B}} + \delta$），以修正初始估计的误差。

**优化目标**：总损失函数为 L1 模糊图像重建损失与帧间运动正则化损失之和：
$$\mathcal{L} = ||\hat{\mathbf{I}}^B - \mathbf{I}^B||_1 + \mathcal{L}_{reg}$$
通过端到端可微的渲染管道，梯度可从模糊图像重建误差反向传播至 3D 高斯参数、子帧姿态、形状参数和蒙皮权重，实现所有模块的联合优化。

**与两阶段方法的本质区别**：先去模糊后重建的基线（如 ShiftNet + GauHuman、RVRT + GauHuman 等）在二维图像域独立处理每一帧，缺乏多视图三维一致性约束，导致去模糊结果在视角间不一致，进而损害 3D 重建质量。MAD-Avatar 将模糊形成直接嵌入三维渲染管道，从根本上保证了运动估计与几何重建的协同一致性。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/002_Figure_2.jpg]]
*Figure 2: Brief illustration of the pipeline. The sub-frame motion for each blurry frame is modeled using the SMPL representation, followed by warping the canonical 3DGS according to the estimated motion parameters. The final blurry image is synthesized by averaging the sequence of rendered virtual sharp images*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/001_Figure_1.jpg]]
*Figure 1: The ambiguity brought by motion blur. When reconstructing sharp 3DGS avatars from blurry frames, motion-induced blur introduces challenging ambiguities in motion interpretation*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/005_Figure_5.jpg]]
*Figure 5: Time synchronization of the camera system. ‘TD’ and ‘EX’ stand for “Trigger Delay” and “Exposure”*



MAD-Avatar 的核心思路是将传统二维模糊形成过程扩展为三维感知的物理模型，结合 SMPL 人体运动先验对子帧运动和规范头像进行联合优化，从而从根本上消除运动模糊的歧义。整个流水线（图2）包含三个紧密耦合的关键模块：三维模糊形成模型、子帧运动模型和帧间运动正则化。

### 三维模糊形成模型

传统图像去模糊方法通常在二维像素空间建模，而 MAD-Avatar 将模糊形成过程提升到三维空间。其物理基础是：模糊图像 $`\mathbf { I } ^ { B } ( \mathbf { u } )`$ 由曝光时间 $`\tau`$ 内到达传感器像素 $`\mathbf{u}`$ 的清晰光强积分形成：

$$ \mathbf { I } ^ { B } ( \mathbf { u } ) = \int _ { 0 } ^ { \tau } \mathbf { I } _ { t } ^ { S } ( \mathbf { u } ) \mathrm { d } t \tag{1} $$

实际计算中，该积分被离散化为 $`n`$ 张虚拟清晰图像的平均：

$$ \mathbf { I } ^ { B } ( \mathbf { u } ) \approx \frac { 1 } { n } \sum _ { i = 0 } ^ { n - 1 } \mathbf { I } _ { i } ^ { S } ( \mathbf { u } ) \tag{2} $$

与二维方法的关键区别在于，MAD-Avatar 的虚拟清晰图像并非来自图像域插值，而是从三维规范空间渲染得到。具体而言，给定规范空间中的 $`K`$ 个三维高斯 $`\{ G _ { k } ( \mathbf { x } ) \} _ { k = 0 } ^ { K - 1 }`$，在曝光周期内的 $`T`$ 个等间隔时刻 $`t`$，利用 SMPL 参数 $`S_t`$ 将规范高斯变形到当前姿态，再通过相机外参 $`\mathbf{R}`$ 和内参 $`\mathbf{K}`$ 进行可微渲染 $`\mathcal{R}`$，最终平均得到模糊图像：

$$ \mathbf { I } ^ { B } = \frac { 1 } { T } \sum _ { t = 0 } ^ { T - 1 } \mathcal { R } ( \mathcal { W } ( \{ G _ { k } ( \mathbf { x } ) \} _ { k = 0 } ^ { K - 1 } , S _ { t } ) , \mathbf { R } , \mathbf { K } ) \tag{3} $$

其中 $`\mathcal{W}`$ 表示基于 SMPL 的变形函数。这一设计的因果机制在于：**将模糊的歧义从二维像素空间转移到三维运动空间，利用多视图几何约束和人体运动先验来消解歧义**。当三维运动被正确估计时，渲染出的虚拟清晰图像序列自然能平均出与输入一致的模糊图像，同时规范空间的高斯头像保持清晰。

### 子帧运动模型：B样条插值与姿态形变

曝光周期内的连续人体运动是模糊形成的根源。MAD-Avatar 采用基于 SMPL 的 B 样条轨迹表示来建模这一子帧运动，避免了逐时刻独立优化姿态导致的运动无序问题（即图1(b)所示的歧义情形）。

对于每个关节 $`j`$，曝光周期内 $`T`$ 个时刻的姿态由 $`P`$ 个控制节点 $`\tilde{\Theta}^j`$ 通过 B 样条插值得到。时间基向量定义为：

$$ { \bf B } ( t ) = [ 1 , \frac { t } { T } , ( \frac { t } { T } ) ^ { 2 } , \dots , ( \frac { t } { T } ) ^ { P - 1 } ] \tag{4} $$

时刻 $`t`$ 的插值姿态为：

$$ \hat { \Theta } _ { t } ^ { j } = \mathbf { B } ( t ) \cdot \mathcal { M } ^ { P } \cdot \tilde { \Theta } ^ { j } \tag{5} $$

其中 $`\mathcal{M}^P`$ 是 De Boor–Cox B 样条插值矩阵：

$$ \mathcal { M } _ { i , j } ^ { P } = C _ { P - 1 - i } ^ { P - 1 } \sum _ { s = j } ^ { P - 1 } ( - 1 ) ^ { s - j } C _ { s - j } ^ { P } ( P - s - 1 ) ^ { P - 1 - i } \tag{6} $$

B 样条插值保证了运动轨迹的光滑性，但仅靠插值难以捕捉高频的非刚性运动（如衣物褶皱）。为此，引入一个轻量 CNN $`G_{disp}`$ 预测姿态位移 $`\Delta_t^j`$：

$$ \Delta _ { t } ^ { j } = G _ { d i s p } ( \hat { \Theta } _ { t } ^ { j } ; \theta _ { d i s p } ) \tag{7} $$

最终关节姿态为插值姿态与位移之和：

$$ \Theta _ { t } ^ { j } = \hat { \Theta } _ { t } ^ { j } + \Delta _ { t } ^ { j } \tag{8} $$

消融实验证实，去除 B 样条插值（w/o interp.）会导致无序运动估计、性能明显下降；去除姿态形变 CNN（w/o pose deform）则使 B 样条无法充分表达复杂运动，产生额外伪影（Table 3）。此外，B 样条轨迹表示在 PSNR/SSIM/LPIPS 上均优于线性插值和 Slerp（Table 5），控制节点数 $`P=4`$ 时取得最佳性能（Table 6）。

### 帧间运动正则化

曝光周期边界的运动连续性对消除运动方向歧义至关重要。MAD-Avatar 设计了帧间运动正则化损失 $`\mathcal{L}_{reg}`$，约束相邻曝光周期边界姿态的测地距离：

$$ \mathcal { L } _ { r e g } = \frac { 1 } { 2 4 \cdot ( N _ { e } - 1 ) } \sum _ { n = 0 } ^ { N _ { e } - 2 } \sum _ { j = 0 } ^ { 2 3 } \left| \hat { \mathbf { \Theta } } _ { n , T - 1 } ^ { j } - \hat { \mathbf { \Theta } } _ { n + 1 , 0 } ^ { j } \right| _ { \mathrm { G } } \tag{9} $$

其中 $`N_e`$ 为曝光周期总数，$`|\cdot|_G`$ 表示测地距离。该损失强制当前帧曝光结束时刻的姿态与下一帧曝光起始时刻的姿态一致，从而消除图1(b)中“正向运动”与“反向运动”的歧义。消融实验表明，$`\mathcal{L}_{reg}`$ 显著提升非中间时刻的渲染质量（Table 4, Figure 8），在真实数据集上模型9的 PSNR 从 23.198 提升至 24.605。

### LBS 权重细化与形状优化

标准 SMPL 的 LBS 权重 $`\tilde{\pmb{B}}`$ 是固定模板，难以精确建模个体差异。MAD-Avatar 通过 CNN 预测一个偏移量 $`\delta`$ 进行细化：

$$ \hat { \pmb { { B } } } = \tilde { \pmb { { B } } } + \delta \tag{10} $$

同时，SMPL 的形状参数 $`\hat{\beta} \in \mathbb{R}^{10}`$ 从粗估计初始化后在训练过程中联合优化。消融实验证实，省略 LBS 优化（w/o LBS opt.）和形状优化（w/o shape opt.）均导致性能下降（Table 3）。

### 总损失函数

最终优化目标为 L1 模糊图像重建损失与运动正则化损失之和：

$$ \mathcal { L } = | | \hat { \mathbf { I } } ^ { B } - \mathbf { I } ^ { B } | | _ { 1 } + \mathcal { L } _ { r e g } \tag{11} $$

其中 $`\hat{\mathbf{I}}^B`$ 为式(3)预测的模糊图像，$`\mathbf{I}^B`$ 为输入模糊帧。该损失同时驱动规范高斯头像的清晰重建和子帧运动的准确估计，实现端到端的联合优化。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/014_Figure_9.jpg]]
*Figure 9: Visualization of the initial estimated SMPL by EasyMocap and optimized SMPL sequence by the proposed model*



## 实验与关键发现

### 主要定量结果

MAD-Avatar 在合成数据集（ZJU-MoCap）和自采的真实数据集上均显著优于所有基线方法。Table 2 汇总了与五类方法的对比：直接使用模糊帧训练 **GauHuman**（Zhe Li et al., CVPR 2024）的一阶段基线，以及四种“先2D去模糊，再训练 GauHuman”的两阶段基线——**ShiftNet + GauHuman**（Dasong Li et al., CVPR 2023）、**RVRT + GauHuman**（Jingyun Liang et al., NeurIPS 2022）、**VRT + GauHuman**（Jingyun Liang et al., TIP 2024）和 **BSST + GauHuman**（Huicong Zhang et al., CVPR 2024）。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison results on two datasets. We colorize results as best , second best , and third best*

在合成数据集上，MAD-Avatar 取得 PSNR 25.546 dB，较 GauHuman 的 23.080 dB 提升 **+2.466 dB**；SSIM 从 0.7660 提升至 0.8290（+0.0630）；LPIPS 从 0.2277 降至 0.1476（-0.0801）。在真实数据集上，PSNR 从 25.602 dB 提升至 27.010 dB（+1.408 dB），SSIM 从 0.8044 提升至 0.8271（+0.0227），LPIPS 从 0.2380 降至 0.1668（-0.0712）。两阶段基线因2D去模糊缺乏多视图一致性，性能普遍受限——这一对比直接验证了三维感知模糊建模的必要性。

### 消融实验

Table 3 系统拆解了各模块的贡献，所有消融变体均导致性能下降：

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/008_Table_3.jpg]]
*Table 3: Quantitative ablation results on two datasets. We colorize results as best , second best , and third best*

- **去除B样条插值（w/o interp.）**：独立优化每个子帧姿态导致无序运动估计，PSNR 显著跌落，印证了连续运动先验对消除歧义的关键作用。
- **去除姿态形变CNN（w/o pose deform）**：B样条无法充分表达高频非刚性运动，产生额外伪影。
- **省略LBS优化（w/o LBS opt.）**与**去除形状优化（w/o shape opt.）**：分别导致蒙皮精度下降和体型拟合偏差，指标小幅但一致恶化。

帧间运动正则化 $\mathcal{L}_{reg}$ 的消融（Table 4, Figure 8）揭示了其独特价值：去除该损失后，模型在非中间时刻的渲染质量大幅下降，误差图显示运动方向估计错误——这正是 Figure 1 所揭示的运动模糊歧义的直接体现。$\mathcal{L}_{reg}$ 通过约束相邻曝光周期边界姿态的测地距离一致性，有效消除了这一歧义。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/012_Table_4.jpg]]
*Table 4: Quantitative ablation results for the inter-frame motion regularization loss*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/010_Figure_8.jpg]]
*Figure 8: Qualitative ablation results for*

超参数敏感性分析进一步明确了最优配置：
- **轨迹表示方式**（Table 5）：B样条在 PSNR/SSIM/LPIPS 上全面优于线性插值和 Slerp。
- **控制节点数**（Table 6）：$P=4$ 时性能最优。
- **虚拟清晰图像数**（Table 7）：$T=5$ 为最佳，更少的子帧不足以近似模糊积分，更多子帧则引入冗余优化负担。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/016_Table_5.jpg]]
*Table 5: Qualitative ablation results on trajectories representations. We colorize result as best , second best , and third best*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/017_Table_6.jpg]]
*Table 6: Ablation results for control knot number P*

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/015_Table_7.jpg]]
*Table 7: Ablation results for virtual sharp image number T*

### SMPL 初始化的鲁棒性与优化必要性

Table 8 展示了对 SMPL 初始姿态施加不同程度扰动后的性能变化，结果表明方法对粗初始化具有一定容忍度。然而，Table 9 显示完全冻结 SMPL 参数（不进行联合优化）会导致性能明显下降，Figure 9 可视化了 EasyMocap 初始估计与模型优化后 SMPL 序列的差异——优化后的姿态序列更平滑、更符合物理运动规律。这证实了 **SMPL 子帧运动联合优化**作为核心因果调控变量的有效性。

![[assets/figures/papers/paper_list_l14_https_arxiv_org_abs_2411_16758/figures/018_Table_8.jpg]]
*Table 8: Quantitative results with different perturbations*

### 失败模式与局限性

尽管 MAD-Avatar 在受控多视角场景下表现优异，仍存在若干边界条件：

1. **多视角依赖**：方法需要同步多视角相机系统和粗略的 SMPL 初始化，无法直接应用于野外单目视频。Table 13-14 显示视角数减少会降低性能，但降幅可控。
2. **极端模糊**：Table 10-11 表明在不同模糊程度 $K_{blur}$ 下方法仍优于基线，但对长时间曝光或极快运动等极端情况的验证尚不充分。
3. **SMPL 建模边界**：宽松服装、手持物体等超出 SMPL 表达能力的非刚性运动会引入几何失真——这是人体先验模型的固有局限，而非本方法特有。
4. **计算效率**：训练和渲染仍需 GPU 加速，尚未达到实时水平。



## 定位与知识库关联

### 任务定位与瓶颈分析

MAD-Avatar 解决的核心问题是**从模糊视频中重建清晰、可动画的3D高斯头像**。该任务处于三维重建、运动去模糊和人体先验建模的交叉点。其真实瓶颈在于：运动模糊在人脸/人体三维高斯重建中引入严重的**运动歧义**——同一张模糊图像可能对应多种不同的子帧运动轨迹，导致几何纹理失真和SMPL参数估计错误。现有方法无法同时处理去模糊与高质量头像重建。

### 与基线方法的关系

论文将所提方法与两类基线进行了系统对比：

**第一类：直接使用模糊帧训练的标准3DGS头像模型。**
- **GauHuman** (Zhe Li et al., CVPR 2024)：直接输入模糊图像训练，无任何去模糊机制。在合成数据集上PSNR仅为23.080 dB，而MAD-Avatar达到25.546 dB（+2.466 dB）。该基线的失败直接验证了“运动模糊歧义会严重破坏3DGS重建”这一核心动机。

**第二类：先2D去模糊、再训练3DGS的两阶段方法。**
- **ShiftNet + GauHuman** (Dasong Li et al., CVPR 2023; Zhe Li et al., CVPR 2024)
- **RVRT + GauHuman** (Jingyun Liang et al., NeurIPS 2022; Zhe Li et al., CVPR 2024)
- **VRT + GauHuman** (Jingyun Liang et al., TIP 2024; Zhe Li et al., CVPR 2024)
- **BSST + GauHuman** (Huicong Zhang et al., CVPR 2024; Zhe Li et al., CVPR 2024)

这些两阶段基线在合成和真实数据集上均显著弱于MAD-Avatar（Table 2）。其根本局限在于：二维去模糊缺乏多视图一致性，各视角独立处理，无法利用三维运动先验消除歧义。MAD-Avatar通过**三维感知的模糊形成模型**将去模糊与重建统一在单阶段优化中，从根本上避免了这一缺陷。

### 方法谱系中的关键创新

MAD-Avatar在现有技术栈上做出了以下核心改变（changed slots）：

| 组件 | 基线做法 | MAD-Avatar做法 | 证据锚点 |
|------|---------|---------------|---------|
| 模糊形成模型 | 假设输入为清晰图像，无模糊建模 | 基于物理的3D感知模糊形成模型，通过平均曝光时间内子帧的渲染虚拟清晰图像合成模糊图像 | Sec 3.1, Eq (3) |
| 子帧运动表示 | 不适用（无子帧概念） | 基于SMPL的B样条姿态插值 + 姿态形变CNN + 帧间测地距离正则化 | Sec 3.2, Eq (4)-(9) |
| SMPL参数优化 | 使用EasyMocap离线估计的固定SMPL参数 | 在训练过程中联合优化姿态控制节点、形状参数和LBS权重 | Sec 3.2, Sec 3.3 |
| 损失函数 | 仅L1光度损失 | L1模糊图像重建损失 + 帧间运动正则化损失L_reg | Eq (11) |

核心洞察在于：将传统二维模糊形成过程扩展为**三维感知的物理模型**，结合SMPL人体运动先验对子帧运动和规范头像进行联合优化，从根本上消除运动模糊的歧义。

### 消融实验揭示的因果机制

消融实验（Table 3, Table 4, Figure 8）揭示了各组件的因果贡献：

1. **去除B样条插值（w/o interp.）**：导致无序运动估计，性能明显下降。这验证了时间连续性先验对消除歧义的必要性。
2. **去除姿态形变CNN（w/o pose deform）**：B样条无法充分表达复杂运动，产生额外伪影。说明纯插值不足以捕捉高频非刚性运动。
3. **省略LBS优化（w/o LBS opt.）**：蒙皮权重细化对提升重建精度有实质贡献。
4. **去除形状优化（w/o shape opt.）**：指标小幅恶化，表明形状参数的联合优化是必要的。
5. **帧间正则化L_reg**：这是消除运动方向歧义的关键组件。去除后，非中间时刻的渲染质量大幅下降（Figure 8），因为模型可能估计出方向错误的运动轨迹。

### 适用边界与局限

尽管MAD-Avatar在受控环境下取得了显著性能提升，其适用边界存在明确限制：

1. **多视角依赖**：需要多视角同步相机系统和粗略的SMPL初始化，限制了在野外单目视频中的应用。论文展示了iPhone 16 Pro的拍摄结果（Figure 14），但未见系统性的单目评估。
2. **极端模糊未充分验证**：对长时间曝光、极快运动等极端情况，线性平均模糊模型可能不够准确。
3. **SMPL建模能力边界**：人体运动模型依赖SMPL，可能无法很好地处理宽松服装、手持物体等超出SMPL建模能力的非刚性运动。
4. **计算效率**：训练和渲染仍需GPU加速，尚难以实时完成。

### 开放问题

论文引申出以下待探索方向：

- **单目扩展**：如何将该框架扩展到单目视频场景，消除对多视角和相机外参的依赖？
- **跨域泛化**：能否将该方法应用于其他动态场景（如动物、通用物体）的去模糊重建？
- **实时化**：如何进一步提升计算效率，实现实时或接近实时的渲染？
- **非线性模糊模型**：对于高对比度区域，线性平均模糊模型是否足够？是否需要非线性累积模型？

### 在知识库中的定位

MAD-Avatar在3DGS头像重建领域首次引入**三维感知的运动去模糊**机制，填补了“模糊视频→清晰可动画3DGS头像”这一技术空白。其核心贡献——基于SMPL子帧运动的物理模糊形成模型与联合优化框架——为后续工作在动态场景去模糊重建、单目视频扩展、以及更通用物体类别的去模糊重建方面提供了明确的技术路线图。代码已开源（https://github.com/MyNiuuu/MAD-Avatar），为社区复现和后续改进提供了基础。



## 原文 PDF

![[paperPDFs/CVPR_2026/Motion_Aware_Animatable_Gaussian_Avatars_Deblurring.pdf]]
