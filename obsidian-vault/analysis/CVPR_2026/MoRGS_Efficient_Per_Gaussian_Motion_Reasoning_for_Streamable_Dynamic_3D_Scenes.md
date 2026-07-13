---
title: "MoRGS: Efficient Per-Gaussian Motion Reasoning for Streamable Dynamic 3D Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MoRGS_Efficient_Per_Gaussian_Motion_Reasoning_for_Streamable_Dynamic_3D_Scenes.pdf
project_link: null
code_link: null
aliases:
- MoRGS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入稀疏光流作为运动正则化信号，与可学习的运动偏移场和运动置信度结合，使高斯运动遵循真实场景动力学。
primary_logic: 通过稀疏视角光流引导高斯运动、运动偏移场补偿视图不一致、运动置信度选择性更新动态高斯，可以在线重建高保真动态场景，显著提升渲染质量、运动保真度和时间一致性。
claims:
- MoRGS在N3DV数据集上以32.53 dB (MoRGS-l)的PSNR达到在线方法最优。
- 光流引导运动学习使N3DV的PSNR提升+0.52 dB，Meet Room提升+1.15 dB。
- 运动偏移场仅用4个监督视图的PSNR（31.82）超过无偏移时8个视图的PSNR（32.07），证实稀疏运动线索的有效利用。
- MoRGS在静态区域达到最低mTV，表明时间一致性大幅优于3DGStream和QUEEN。
---

# MoRGS: Efficient Per-Gaussian Motion Reasoning for Streamable Dynamic 3D Scenes

> [!tip] 核心洞察
> 通过稀疏视角光流引导高斯运动、运动偏移场补偿视图不一致、运动置信度选择性更新动态高斯，可以在线重建高保真动态场景，显著提升渲染质量、运动保真度和时间一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoRGS：面向可流式动态3D场景的高效逐高斯运动推理 |
| 英文题名 | MoRGS: Efficient Per-Gaussian Motion Reasoning for Streamable Dynamic 3D Scenes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.25042) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MoRGS |
| Dataset | N3DV, Meet Room |

> [!tip] 效果简介
> - N3DV 上，PSNR (dB)↑ 32.53 (MoRGS-l) vs 所有在线基线 (最优 QUEEN) (最高)。
> - Meet Room 上，PSNR (dB)↑ 31.79 vs 所有在线基线 (最优 QUEEN-l†) (最高)。

## 概要

**问题瓶颈**：在线动态3D场景重建方法通常仅依赖光度损失驱动高斯更新，缺乏显式运动监督。这导致高斯运动追逐像素残差而非真实三维动态——动态高斯运动被低估，静态高斯产生冗余运动，严重损害时间一致性。

**核心洞察**：引入稀疏视角光流作为轻量运动正则化信号，结合可学习的逐高斯运动偏移场与运动置信度，使高斯运动遵循真实场景动力学，从而实现在线高保真动态重建。

**方法定位**：MoRGS 是一种面向可流式动态场景的在线框架，在现有在线基线（**3DGStream** Sun et al., CVPR 2024；**HiCoM** Gao et al., NeurIPS 2024；**QUEEN** Girish et al., NeurIPS 2024；**4DGC** Hu et al., CVPR 2025）基础上，首次显式建模逐高斯运动推理。其核心改造包括三个关键机制：
- **稀疏光流运动监督**：在少量关键视图上计算帧间光流，为高斯运动提供2D正则化信号，替代纯光度损失的隐式运动学习；
- **运动偏移场**：学习每高斯可微偏移量，补偿稀疏流信号在不同视图间的不一致性，增强三维几何一致性；
- **运动置信度**：利用SAM2细化的运动掩膜监督逐高斯置信度，选择性加权属性残差更新，抑制静态区域冗余运动。

**主要结果**：在N3DV数据集上，MoRGS-l 以 32.53 dB PSNR 达到在线方法最优（Tab. 1）；在Meet Room数据集上同样取得最高PSNR 31.79 dB（Tab. 2）。消融实验表明，光流引导贡献 +0.52 dB（N3DV）和 +1.15 dB（Meet Room），运动偏移场进一步贡献 +0.36 dB 和 +0.66 dB，运动置信度再贡献 +0.32 dB 和 +0.58 dB（Tab. 4）。在静态区域的时间一致性指标 mTV 上，MoRGS 显著优于 3DGStream 和 QUEEN（Tab. 3）。



动态3D场景的流式重建在虚拟现实、增强现实和沉浸式通信等应用中需求迫切。在线方法需要从连续的视频帧中增量式地构建和更新场景表示，同时兼顾渲染质量、训练速度和存储开销。3D高斯泼溅（3D Gaussian Splatting, 3DGS）凭借其显式点基表示和高效可微光栅化，为快速、高质量的静态场景重建提供了新范式，其像素颜色通过深度排序的Alpha混合渲染：

$$C ( \boldsymbol x ) = \sum _ { i = 1 } ^ { N } T _ { i } c _ { i } \alpha _ { i } , \qquad T _ { i } = \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } )$$

训练损失通常结合L1和D-SSIM项：

$$\mathcal { L } _ { \mathrm { r e c o n } } = ( 1 - \lambda ) \mathcal { L } _ { 1 } + \lambda \mathcal { L } _ { \mathrm { D - S S I M } }$$

将3DGS扩展到动态场景，现有在线方法（如**3DGStream**（Sun et al., CVPR 2024）、**HiCoM**（Gao et al., NeurIPS 2024）、**QUEEN**（Girish et al., NeurIPS 2024）、**4DGC**（Hu et al., CVPR 2025）等）通常采用逐帧微调高斯属性（位置、颜色、不透明度等）的策略，通过可学习残差更新：

$$\mathcal { A } _ { t } = \mathcal { A } _ { t - 1 } + \mathcal { R } _ { t }$$

然而，这种纯粹依赖光度损失的更新机制存在根本性缺陷：**缺乏显式运动监督导致高斯运动追逐像素残差而非真实三维动态**。具体而言，动态高斯因缺乏运动先验而被低估位移量，静态高斯则可能产生冗余运动以拟合光照变化或视差效应，严重损害时间一致性。这一瓶颈在稀疏视角或复杂运动场景下尤为突出。

现有在线基线（如**Dynamic3DGS**（Luiten et al., 3DV 2024））尝试通过简单的运动启发式规则缓解该问题，但未能从根本上解决运动与外观的耦合困境。离线方法（如**Swift4D**（Wu et al., ICLR 2025））虽能获得更高重建精度，却牺牲了流式处理的实时性要求。

MoRGS的核心动机在于：**引入轻量但显式的运动信号，使高斯更新遵循真实场景动力学**。其关键洞察是：稀疏视角上的光流可作为运动正则化信号，通过可学习的运动偏移场补偿视图间的不一致性，并利用运动置信度选择性更新动态高斯，从而在保持在线效率的同时，显著提升渲染质量、运动保真度和时间一致性。



## 核心方法与创新机理

现有在线动态场景重建方法（如 **3DGStream** (Sun et al., CVPR 2024)、**QUEEN** (Girish et al., NeurIPS 2024) 等）仅依赖光度损失驱动高斯属性更新，缺乏显式的运动监督信号。这导致一个根本性瓶颈：高斯运动追逐像素残差而非真实三维动态——动态高斯运动被低估，静态高斯产生冗余运动，严重损害时间一致性。

MoRGS 的核心创新在于引入**稀疏运动线索引导的逐高斯运动推理**，通过三个紧密耦合的机制改变上述因果链路：

### 1. 运动监督类型：从纯光度损失到稀疏光流正则化

基线方法仅使用光度损失 $\mathcal{L}_{\mathrm{recon}}$ 隐式驱动运动学习。MoRGS 改为在少量关键视图上引入稀疏光流作为显式运动监督信号：利用预训练的 SEA-RAFT 计算关键视图帧间光流 $F_{\hat{v}}^{\mathrm{flow}}(x)$，并将每高斯 3D 位移 $\Delta\mu_{i,t}$ 投影渲染为高斯运动图 $F_{\hat{v}}^{G}(x)$，通过端点误差损失 $\mathcal{L}_{\mathrm{flow}}$ 直接对齐。这使高斯运动从“追逐残差”转向“遵循真实场景动力学”，在 N3DV 上带来 **+0.52 dB** PSNR 提升，Meet Room 上提升 **+1.15 dB**（Tab. 4）。

### 2. 运动细化机制：可学习的逐高斯运动偏移场

稀疏光流仅在有限视图上提供 2D 约束，存在视图间不一致和投影歧义。MoRGS 引入每高斯可学习的运动偏移场 $O_{i,t}$，将最终运动修正为 $\Delta\hat{\mu}_{i,t} = \Delta\mu_{i,t} + O_{i,t}$，并用 L1 损失 $\mathcal{L}_{\mathrm{off}}$ 约束偏移幅度。该设计使模型能自动补偿流引导运动的误差，增强三维几何一致性。消融实验表明，运动偏移场在 N3DV 上进一步带来 **+0.36 dB** 增益，Meet Room 上 **+0.66 dB**（Tab. 4）；更关键的是，仅使用 **4 个监督视图加偏移场**的 PSNR（31.82）已超过**无偏移场时 8 个视图**的 PSNR（32.07），证实偏移场有效利用了稀疏运动线索（Tab. 5）。

### 3. 更新选择性：运动置信度加权属性更新

基线方法对所有高斯统一更新，导致静态区域产生冗余运动。MoRGS 学习每高斯的运动置信度 $m_i$，通过光流阈值掩膜与 SAM2 细化掩膜联合监督，使置信度反映真实动态区域。最终属性更新变为 $\mathcal{A}_{i,t} = \mathcal{A}_{i,t-1} + m_i \odot \mathcal{R}_{i,t}$，抑制静态高斯更新、集中学习资源于动态区域。该机制在 N3DV 上再提升 **+0.32 dB**，Meet Room 上 **+0.58 dB**（Tab. 4）；在静态区域的 mTV 指标达到最低，时间一致性显著优于 3DGStream 和 QUEEN（Tab. 3）。

三者的协同效应可通过 Fig. 3 直观验证：无流引导时高斯运动完全偏离真实动态；仅加稀疏流虽恢复方向一致性，但运动仍错误传播到无关高斯；加入偏移场后运动精准定位；再加入置信度后静态区域更新被彻底抑制。



MoRGS 提出了一种在线动态场景重建框架，其核心思路是在逐帧增量更新高斯属性的同时，显式建模每高斯的三维运动，从而将高斯更新与真实场景动力学对齐。框架由四个紧密协作的模块构成一个闭环流水线。

**流水线总览**。给定 $t-1$ 时刻的高斯场，对于 $t$ 时刻的新帧，系统首先在稀疏的关键视图上计算帧间光流作为运动先验；随后将每高斯的 3D 位移投影到图像平面，与光流信号对齐以引导运动学习；为补偿稀疏流信号在不同视图间的不一致性，引入可学习的运动偏移场对每高斯运动进行校正；最后，通过运动置信度机制选择性更新动态高斯，抑制静态区域的冗余变化，从而维持时间一致性。整体流程如 **Figure 2** 所示。

**属性增量更新**。基础 3DGS 在每帧独立优化，而 MoRGS 采用在线残差更新策略：$\mathcal{A}_{t} = \mathcal{A}_{t-1} + \mathcal{R}_{t}$（Eq. 3），其中 $\mathcal{A}$ 为高斯属性集合，$\mathcal{R}_{t}$ 为可学习的帧间残差。这一设计使得模型能够以流式方式处理序列帧，避免了每帧重新初始化的开销。

**稀疏运动线索注入**。与仅依赖光度损失的在线方法（如 **3DGStream** (Sun et al., CVPR 2024)、**QUEEN** (Girish et al., NeurIPS 2024)）不同，MoRGS 在 4 个指定的关键视图 $\hat{v}$ 上利用预训练的 SEA-RAFT 估计光流 $F_{\hat{v}}^{\mathrm{flow}}$（Eq. 4），作为显式运动正则化信号。每高斯的帧间位移 $\Delta\mu_{i,t}$ 被投影并 alpha 混合为渲染运动图 $F_{\hat{v}}^{G}$（Eq. 5-6），通过端点误差损失 $\mathcal{L}_{\mathrm{flow}}$（Eq. 7）与观测光流对齐。这一机制直接回应了核心瓶颈：**缺乏显式运动监督时，高斯运动会追逐像素残差而非真实三维动态**。

**运动偏移场补偿**。稀疏光流仅在少数视图上提供监督，其信号在不同视角间存在不一致性。为此，MoRGS 为每个高斯学习一个运动偏移 $O_{i,t}$，与流引导运动相加得到最终位移 $\Delta\hat{\mu}_{i,t} = \Delta\mu_{i,t} + O_{i,t}$（Eq. 8），并用 L1 正则 $\mathcal{L}_{\mathrm{off}}$ 约束偏移幅度。消融实验证实，**运动偏移场仅用 4 个监督视图的 PSNR（31.82 dB）即超过无偏移时 8 个视图的 PSNR（32.07 dB）**（Tab. 5），表明偏移场有效利用了稀疏运动线索。

**运动置信度选择性更新**。为区分动态与静态高斯，框架首先通过光流幅值阈值生成二值运动掩膜 $M_{\hat{v},k}^{\mathrm{flow}}$（Eq. 9），再周期性（每 5 帧）在关键帧上使用 SAM2 进行掩膜细化与融合（Eq. 10），获得视图一致的伪真值掩膜。每高斯的运动置信度 $m_i$ 通过掩膜损失 $\mathcal{L}_{\mathrm{mask}}$（Eq. 11）学习，并加权属性残差更新 $\mathcal{A}_{i,t} = \mathcal{A}_{i,t-1} + m_i \odot \mathcal{R}_{i,t}$（Eq. 12）。这一设计使静态高斯的更新被抑制，动态高斯获得更多优化资源，显著提升了时间一致性——在静态区域的 mTV 指标上，MoRGS 大幅优于 3DGStream 和 QUEEN（Tab. 3）。

**总损失联合优化**。最终训练目标为 $\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{mask}}\mathcal{L}_{\mathrm{mask}} + \lambda_{\mathrm{flow}}\mathcal{L}_{\mathrm{flow}} + \lambda_{\mathrm{off}}\mathcal{L}_{\mathrm{off}}$（Eq. 13），其中 $\mathcal{L}_{\mathrm{recon}}$ 沿用 3DGS 的 L1+D-SSIM 组合损失（Eq. 2）。四个损失项分别对应渲染质量、运动区域识别、运动方向引导和偏移幅度约束，共同驱动高斯场在在线设定下实现高保真动态重建。

### 补充图表

![[assets/figures/papers/paper_list_l978_https_arxiv_org_abs_2603_25042/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the MoRGS framework. (a) We incrementally update Gaussian attributes at each time step while jointly modeling per-Gaussian motion between frames. (b) Per-Gaussian motion is guided by sparse motion cues and refined by a per-Gaussian motion offset field to compensate for discrepancies in the sparse motion cues. (c) To identify dynamic Gaussians, we obtain motion masks by thresholding the motion cues and then apply a segmentation model for view consistency. The per-Gaussian motion confidence is learned from these masks to suppress redundant background motion, improve temporal consistency, and concentrate learning on large motions*

![[assets/figures/papers/paper_list_l978_https_arxiv_org_abs_2603_25042/figures/001_Figure_1.jpg]]
*Figure 1: The proposed MoRGS framework for streamable dynamic scene reconstruction achieves superior rendering quality by explicitly modeling per-Gaussian motion. The left figures ((a),(b)) show the high-quality rendering and the corresponding Gaussian motion updates compared to [7, 24]. The right figure (c) is the performance comparison with previous state-of-the-art methods [6–8, 13, 24, 30]*



MoRGS 的核心创新在于为在线动态场景重建引入**显式的逐高斯运动推理**，通过三个紧密协作的模块——流引导运动学习、运动偏移场、运动置信度——解决纯光度损失下高斯运动追逐像素残差而非真实三维动态的根本瓶颈。

### 在线高斯属性更新框架

MoRGS 继承 3DGS 的渲染管线。给定深度排序的 $N$ 个高斯，像素颜色通过 Alpha 混合得到：

$$C ( \boldsymbol x ) = \sum _ { i = 1 } ^ { N } T _ { i } c _ { i } \alpha _ { i } , \qquad T _ { i } = \prod _ { j = 1 } ^ { i - 1 } ( 1 - \alpha _ { j } ) \tag{1}$$

初始帧使用组合损失优化：

$$\mathcal { L } _ { \mathrm { r e c o n } } = ( 1 - \lambda ) \mathcal { L } _ { 1 } + \lambda \mathcal { L } _ { \mathrm { D - S S I M } } \tag{2}$$

在线阶段，每帧高斯属性通过可学习残差增量更新：

$$\mathcal { A } _ { t } = \mathcal { A } _ { t - 1 } + \mathcal { R } _ { t } \tag{3}$$

这一朴素更新缺乏运动先验，动态高斯可能欠更新，静态高斯可能产生冗余运动。

### 流引导运动学习

为引入运动正则化，MoRGS 在稀疏关键视图 $\hat{v}$ 上估计帧间光流：

$$F _ { \hat { v } } ^ { \mathrm { f l o w } } ( x ) = F ^ { \mathrm { f l o w } } ( I _ { \hat { v } , t } , I _ { \hat { v } , t - 1 } ) \tag{4}$$

定义逐高斯的 3D 位移：

$$\Delta \mu _ { i , t } = ( \mu _ { i , t } - \mu _ { i , t - 1 } ) \tag{5}$$

将该位移投影到图像平面，通过 Alpha 混合渲染为**高斯运动图**：

$$F _ { \hat { v } } ^ { G } ( x ) = \sum _ { i = 1 } ^ { N } w _ { i } ( x ) \pi _ { \hat { v } } ( \Delta \mu _ { i , t } ) \tag{6}$$

以光流为监督信号，构建端点误差损失：

$$\mathcal { L } _ { \mathrm { f l o w } } = \sum _ { \hat { v } } \| F _ { \hat { v } } ^ { \mathrm { f l o w } } ( x ) - F _ { \hat { v } } ^ { G } ( x ) \| _ { 2 } \tag{7}$$

该损失使高斯运动在 2D 投影上逼近观测光流，为 3D 运动提供稀疏但有效的正则化。

### 运动偏移场

稀疏光流仅覆盖少量视图，存在视图间不一致性。为补偿这一缺陷，MoRGS 为每个高斯学习一个可微调的**运动偏移** $O_{i,t}$，与流引导运动相加得到最终位移：

$$\Delta \hat { \mu } _ { i , t } = \underbrace { \Delta \mu _ { i , t } } _ { \mathrm { f l o w - g u i d e d } } + \underbrace { O _ { i , t } } _ { \mathrm { l e a r n a b l e \ o f f s e t } } \tag{8}$$

偏移场受 L1 正则化约束 $\mathcal{L}_{\mathrm{off}} = \| O_{i,t} \|_1$，使校正量保持在较小范围。消融实验（Tab. 5）表明，引入偏移场后仅用 4 个监督视图的 PSNR（31.82 dB）即可超过无偏移时 8 个视图的 PSNR（32.07 dB），证实其有效利用稀疏运动线索。

### 运动置信度与选择性更新

为抑制静态区域的高斯冗余更新，MoRGS 构建运动掩膜作为置信度学习的目标。首先通过光流幅度阈值生成二值掩膜：

$$M _ { \hat { v } , k } ^ { \mathrm { f l o w } } = \| F ^ { \mathrm { f l o w } } ( I _ { \hat { v } , k } , I _ { \hat { v } , k - 1 } ) \| > \lambda ^ { \mathrm { f l o w } } \tag{9}$$

使用 SAM2 对关键帧上的流掩膜进行视图一致性细化并融合：

$$M _ { \hat { v } , k } ^ { \mathrm { s a m } } = F ^ { \mathrm { s a m } } ( I _ { \hat { v } , k } , M _ { \hat { v } , k } ^ { \mathrm { f l o w } } ) , \quad M _ { \hat { v } , k } = M _ { \hat { v } , k } ^ { \mathrm { f l o w } } \cup M _ { \hat { v } , k } ^ { \mathrm { s a m } } \tag{10}$$

渲染的运动置信度图 $\tilde{M}_{\hat{v},k}$ 与真值掩膜计算 L1 损失：

$$\mathcal { L } _ { \mathrm { m a s k } } = \sum _ { \hat { v } } \lVert \tilde { M } _ { \hat { v } , k } - M _ { \hat { v } , k } \rVert _ { 1 } \tag{11}$$

学到的逐高斯运动置信度 $m_i$ 用于加权属性残差更新：

$$\mathcal { A } _ { i , t } = \mathcal { A } _ { i , t - 1 } + m _ { i } \odot \mathcal { R } _ { i , t } \tag{12}$$

置信度接近 0 的高斯几乎不更新，使模型集中计算资源于真正动态区域，显著提升时间一致性。

### 总损失

联合优化总损失为：

$$\mathcal { L } _ { \mathrm { t o t a l } } = \mathcal { L } _ { \mathrm { r e c o n } } + \lambda _ { \mathrm { m a s k } } \mathcal { L } _ { \mathrm { m a s k } } + \lambda _ { \mathrm { f l o w } } \mathcal { L } _ { \mathrm { f l o w } } + \lambda _ { \mathrm { o f f } } \mathcal { L } _ { \mathrm { o f f } } \tag{13}$$

三个模块的消融实验（Tab. 4）验证了各自的独立贡献：光流引导在 N3DV 上提升 +0.52 dB，运动偏移场再提升 +0.36 dB，运动置信度进一步提升 +0.32 dB，三者协同实现了从像素残差追逐到真实场景动力学的转变。

### 补充图表

![[assets/figures/papers/paper_list_l978_https_arxiv_org_abs_2603_25042/figures/003_Figure_3.jpg]]
*Figure 3: Per-Gaussian Motion Visualization. We visualize per-Gaussian motion under (a) no flow guidance, (b) sparse flow guidance only, (c) sparse flow guidance with motion offset, and (d) sparse flow guidance with both motion offset and motion confidence, while (e) and (f) show the learned motion confidence map and motion offset map, respectively*



## 实验与关键发现

### 核心定量结果

MoRGS 在两个主流动态场景基准上均取得在线方法中最优的渲染质量。在 **N3DV** 数据集上，MoRGS-l 以 **32.53 dB** 的 PSNR 超越所有在线基线（Tab. 1）；在更具挑战的 **Meet Room** 数据集上，MoRGS 达到 **31.79 dB** PSNR 与 **0.957** SSIM（Tab. 2）。相比次优在线方法 QUEEN，MoRGS 在 N3DV 上领先 **+0.34 dB**，而训练时间仅增加约 1.1 秒/帧——这一代价换来了显著的质量提升。

值得注意的是，MoRGS 在仅使用 **4 个稀疏运动监督视图** 时，PSNR 已达 31.82 dB，优于无运动偏移场时使用 8 个视图的 32.07 dB（Tab. 5），表明运动偏移场能高效利用有限运动线索，降低对密集多视图运动信号的依赖。

### 时间一致性与运动保真度

除渲染质量外，MoRGS 在静态区域的时间一致性上表现出色。在 N3DV 两个场景的静态掩膜区域上，MoRGS 的 **mTV（mean Temporal Variation）指标均为最低**（Tab. 3），显著优于 3DGStream 和 QUEEN。这与方法设计一致：运动置信度机制通过抑制静态高斯的属性更新，避免了冗余的背景抖动，从而在视觉上产生更平滑的时间序列（Fig. 6 的时空切片可视化佐证了这一点）。

![[assets/figures/papers/paper_list_l978_https_arxiv_org_abs_2603_25042/figures/007_Figure_6.jpg]]
*Figure 6: Temporal Consistency Comparison. A visualization of spatiotemporal images from a fixed vertical scanline over time*

### 消融实验：各组件的因果贡献

Tab. 4 的系统消融揭示了三个核心组件的独立增益：

1. **光流引导运动学习**：在仅光度损失的基础上加入稀疏光流监督，N3DV 的 PSNR 提升 **+0.52 dB**，Meet Room 提升 **+1.15 dB**。Meet Room 场景中更大的增益说明，当场景动态更复杂时，纯光度信号对运动的欠约束问题更严重，光流先验的补偿作用更关键。

2. **运动偏移场**：在光流引导的基础上引入可学习的逐高斯运动偏移，N3DV 再提升 **+0.36 dB**，Meet Room 再提升 **+0.66 dB**。偏移场的作用是校正光流投影与真实三维运动之间的视图不一致——Fig. 3(f) 显示偏移量集中在光流监督误导高斯的区域，验证了其“按需补偿”的行为。

3. **运动置信度**：加入置信度加权更新后，N3DV 再提升 **+0.32 dB**，Meet Room 再提升 **+0.58 dB**。置信度机制通过选择性抑制静态区域更新（Fig. 3(e)），使优化资源集中于真正动态的高斯，同时提升了渲染质量和时间一致性。

### 定性可视化：运动学习的行为演变

Fig. 3 的逐高斯运动可视化清晰地呈现了运动学习从“盲目追逐像素残差”到“遵循真实场景动力学”的演变过程：
- **(a) 无光流引导**：高斯运动方向杂乱，与场景动态无关，呈现典型的“残差追逐”模式。
- **(b) 仅稀疏光流引导**：运动方向恢复一致性，但错误地将运动传播到不应移动的高斯上，产生“运动泄漏”。
- **(c) 加入运动偏移场**：运动泄漏得到抑制，偏移场补偿了稀疏流的不一致信号。
- **(d) 加入运动置信度**：运动更新被限制在真正动态的区域，静态背景保持稳定。

### 公平性与局限说明

所有方法在相同数据集划分和评估协议下进行，每场景评估固定 300 帧。需注意以下实验依赖：
- 光流由预训练的 **SEA-RAFT** 在 4 个指定稀疏视图上计算，该网络是额外的计算依赖。
- 关键帧掩膜使用 **SAM2** 细化，但仅在每 5 帧时执行一次，以控制推理开销。
- 方法假设相机静态，对相机运动场景的适用性未经验证；复杂动作与遮挡场景下，稀疏光流监督可能仍存在欠约束问题，需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l978_https_arxiv_org_abs_2603_25042/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on the N3DV dataset. For each scene, all metrics are averaged over 300 frames. Storage and training time both include the initial frame size and time. Red and orange highlight the best and second-best results in each category, respectively*

![[assets/figures/papers/paper_list_l978_https_arxiv_org_abs_2603_25042/figures/005_Table_2.jpg]]
*Table 2: Quantitative comparison on Meet Room dataset. QUEEN-l† refers to our re-implementation result through official code in the same experimental environment*

![[assets/figures/papers/paper_list_l978_https_arxiv_org_abs_2603_25042/figures/008_Table_4.jpg]]
*Table 4: Ablation on main components of our MoRGS framework*

![[assets/figures/papers/paper_list_l978_https_arxiv_org_abs_2603_25042/figures/009_Table_5.jpg]]
*Table 5: Ablation on number of motion supervision and offset in N3DV dataset*

![[assets/figures/papers/paper_list_l978_https_arxiv_org_abs_2603_25042/figures/010_Table_3.jpg]]
*Table 3: Analysis of rendering quality and temporal consistency on two N3DV scenes. mTV is computed only in static regions defined by predefined masks*

![[assets/figures/papers/paper_list_l978_https_arxiv_org_abs_2603_25042/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Results. A visualization of various scenes in N3DV and Meet Room dataset. We include additional video results in the supplementary material*



## 定位与知识库关联

### 1. 在线动态3DGS重建方法谱系

MoRGS 定位于**在线（逐帧流式）动态场景重建**这一细分方向，其直接对话的基线方法构成了该领域近两年的发展轨迹：

- **Dynamic3DGS**（Luiten et al., 3DV 2024）是该方向早期代表性工作，首次将3D Gaussian Splatting扩展到动态场景的在线重建，但仅依赖光度损失进行帧间优化，缺乏显式的运动建模。
- **3DGStream**（Sun et al., CVPR 2024）提出了基于变换场的在线更新策略，通过可学习的残差更新高斯属性，但仍未引入显式运动监督，导致动态高斯运动追逐像素残差而非真实三维动态。
- **HiCoM**（Gao et al., NeurIPS 2024）探索了层次化运动建模，但在运动解耦的精细度上仍有不足。
- **QUEEN**（Girish et al., NeurIPS 2024）是当前在线方法中性能最强的基线之一，在N3DV上达到32.19 dB PSNR，但其运动推理同样受限于光度损失的固有模糊性。
- **4DGC**（Hu et al., CVPR 2025）是同期工作，进一步探索了4D高斯表示的高效在线更新。

MoRGS 与上述方法的**核心分水岭**在于：它首次将稀疏光流作为显式运动正则化信号引入在线3DGS框架，从根本上改变了高斯运动的学习机制——从“追逐像素残差”转向“遵循真实场景动力学”。这一设计使得MoRGS-l在N3DV上以32.53 dB PSNR超越所有在线基线（Tab. 1），在Meet Room上以31.79 dB PSNR达到最优（Tab. 2）。

### 2. 与离线方法的边界

离线动态场景方法（如**Swift4D**，Wu et al., ICLR 2025）通常需要完整的视频序列进行全局优化，可获得更高的重建质量，但无法满足流式传输和实时交互的需求。MoRGS在保持在线推理能力的同时，通过运动偏移场和运动置信度机制，在仅使用4个稀疏监督视图的条件下，PSNR（31.82 dB）已超过无偏移时8个视图的结果（32.07 dB），表明其稀疏运动线索利用效率极高（Tab. 5），缩小了在线与离线方法之间的质量差距。

### 3. 适用边界与关键假设

MoRGS 的有效性建立在以下前提之上，这些前提也划定了其适用边界：

- **静态相机假设**：方法假定相机在场景重建过程中保持静止。对于包含相机运动的场景（如手持拍摄、移动机器人视角），当前框架可能失效，因为光流将混合相机自运动与场景动态，无法直接作为运动监督信号。
- **外部模型依赖**：方法依赖预训练的SEA-RAFT进行光流估计，以及SAM2进行运动掩膜细化。这两个外部模型引入了额外的计算负担和领域依赖性——光流网络在训练域外的泛化能力直接影响运动监督质量，SAM2的推理时间（尽管仅在每5帧的关键帧上执行）也影响在线训练速度。
- **稀疏视图监督的欠约束问题**：光流和掩膜监督仅在4-8个稀疏视图上提供。对于复杂动作（如快速旋转、严重遮挡、非刚性形变），稀疏视角的光流可能无法充分约束三维运动，导致运动偏移场需要补偿过大的误差，此时重建质量可能下降。这一局限在当前实验中尚未被充分压力测试。

### 4. 局限与开放问题

**已确认的局限**：

1. **相机运动场景不适用**：如上述，静态相机假设是当前框架的硬性约束，限制了其在自由视角视频、移动拍摄等场景中的应用。
2. **外部模型计算负担**：SEA-RAFT和SAM2的推理时间虽被周期性调用所缓解，但仍构成在线系统的额外延迟瓶颈。论文未报告光流估计和掩膜细化的具体耗时，这一开销在资源受限设备上可能不可忽视。
3. **训练效率权衡**：MoRGS在N3DV上的训练时间（每帧约1.5秒，Tab. 1）虽与QUEEN相当（−1.1秒），但QUEEN以略低的PSNR（−0.34 dB）换取了更快的训练速度。对于极端实时性要求的应用，MoRGS的训练效率仍有优化空间。

**需人工验证的开放问题**：

1. **光流质量对最终性能的敏感性**：论文未系统分析光流估计误差如何传播到高斯运动学习。若光流网络在特定场景（如低纹理、运动模糊）下失效，MoRGS的鲁棒性需进一步验证。
2. **运动置信度与偏移场的耦合效应**：Tab. 4显示运动置信度在N3DV上单独贡献+0.32 dB，运动偏移场贡献+0.36 dB，但二者是否存在协同效应或相互制约，论文未深入讨论。
3. **扩展到多相机动态场景**：当前框架假设稀疏视图来自同一时刻的多相机捕获（如N3DV的20相机设置）。对于更稀疏的相机配置（如2-3个视角），光流引导的有效性是否会急剧下降，尚待验证。
4. **长期序列的漂移累积**：在线方法固有地面临误差累积问题。论文评估每场景300帧，但未分析更长时间序列下运动估计的漂移情况。

### 5. 知识库定位总结

MoRGS 在动态3DGS重建的知识谱系中占据**“显式运动引导的在线流式重建”**这一节点。其核心贡献——稀疏光流运动正则化、运动偏移场、运动置信度选择性更新——构成了一个完整的运动推理闭环，解决了在线方法中“运动学习缺乏物理约束”这一瓶颈问题。该方法为后续工作提供了两个可扩展的方向：（1）将运动监督信号从稀疏光流扩展到更丰富的运动先验（如深度、场景流）；（2）将运动偏移场和置信度机制推广到相机运动场景的运动解耦。



## 原文 PDF

![[paperPDFs/CVPR_2026/MoRGS_Efficient_Per_Gaussian_Motion_Reasoning_for_Streamable_Dynamic_3D_Scenes.pdf]]
