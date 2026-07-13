---
title: "Relightable Holoported Characters: Capturing and Relighting Dynamic Human Performance from Sparse Views"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Relightable_Holoported_Characters_Capturing_and_Relighting_Dynamic_Human_Performance_from_Sparse_Views.pdf
project_link: null
code_link: null
aliases:
- RHCR
- RHCCRDHPFSV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在UV空间编码物理信息特征（几何、纹理、着色、视角），并通过交叉注意力机制将环境光照与这些特征融合，从而实现单次前馈渲染方程近似。
primary_logic: 将渲染方程的各分量编码为一致的UV空间特征，并利用Transformer交叉注意力模拟光线的空间积分，能够在不显式求解OLAT的情况下，从稀疏视角输入中高效生成动态人体的照片级重光照结果。
claims:
- 我们的方法在所有主体上均显著优于基线方法（表1）。
- 交叉注意力机制使每个纹理像素能够聚合所有方向的光照贡献，类似于渲染方程中的积分。
- 数据捕获策略中对均匀光照跟踪帧和随机环境光照照明的交替，对于学习准确的重光照至关重要（表7）。
- Multi-view Lightstage (5 subjects) 上 PSNR ↑ = 31.49
---

# Relightable Holoported Characters: Capturing and Relighting Dynamic Human Performance from Sparse Views

> [!tip] 核心洞察
> 将渲染方程的各分量编码为一致的UV空间特征，并利用Transformer交叉注意力模拟光线的空间积分，能够在不显式求解OLAT的情况下，从稀疏视角输入中高效生成动态人体的照片级重光照结果。

| 字段 | 内容 |
|------|------|
| 中文题名 | 可重光照全息角色：稀疏视角动态人体重光照 |
| 英文题名 | Relightable Holoported Characters: Capturing and Relighting Dynamic Human Performance from Sparse Views |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.00255) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Relightable Holoported Characters (RHC) |
| Dataset | Multi-view Lightstage |

> [!tip] 效果简介
> - Multi-view Lightstage (5 subjects) 上，PSNR ↑ 31.49 vs 30.29 (R4D+GT Env) (+1.20)；LPIPS ↓ 6.70 vs 9.50 (R4D+GT Env) (-2.80)；SSIM ↑ 89.56 vs 86.77 (R4D+GT Env) (+2.79)。

## 概要

**问题瓶颈**：现有动态人体重光照方法依赖耗时的一次一光（OLAT）捕获与线性组合，或仅限于重放预捕获表演，无法在推理时从稀疏视角输入中高效生成照片级真实感的重光照结果。

**核心洞察**：将渲染方程的各分量（几何、纹理、着色、视角）编码为一致的UV空间物理信息特征，并利用Transformer交叉注意力模拟光线对环境照明的空间积分，能够在单次前馈中近似渲染方程，从而绕过显式OLAT求解。

**方法定位**：本文提出**Relightable Holoported Characters (RHC)**——首个从稀疏RGB图像生成可重光照全息角色的方法。RHC在UV空间提取物理信息特征，通过RelightNet以交叉注意力融合HDR环境图，直接预测附着于粗网格的纹素对齐3D高斯参数，经泼溅渲染输出重光照图像。

**主要结果**：在5名主体的多视角Lightstage基准上，RHC以PSNR 31.49、LPIPS 6.70、SSIM 89.56全面超越最强基线R4D+GT Env（PSNR 30.29、LPIPS 9.50、SSIM 86.77），并在分布外光照（OLAT、近场）下展现出显著的泛化能力。

### 动态人体渲染与重光照的现实需求

将真实人物的动态三维表演无缝置入虚拟环境，是影视制作、混合现实、全息通信等应用的核心技术愿景。这要求系统不仅能从稀疏视角输入中生成自由视点的照片级渲染，还必须支持任意光照条件下的真实感重光照——即人物在新环境光下的外观需与物理世界一致，包含正确的自阴影、镜面反射和材质响应。

当前方法在这两个目标之间存在显著张力。一方面，基于神经渲染的稀疏视角人体重建（如 **Holoported Characters**）能够从4个RGB相机输入生成高质量的新视角图像，但完全不具备重光照能力，只能复现捕获时的固定光照。另一方面，动态人体重光照方法虽然能改变光照，却依赖昂贵的数据采集范式或存在严重的效率瓶颈。

### 现有重光照范式的根本瓶颈

动态人体重光照的主流范式可归结为两类，二者均未实现“稀疏输入 + 任意光照 + 高效推理”的统一。

**第一类是逆渲染方法**，代表工作包括 **Relighting4D (R4D)**、**IntrinsicAvatar (IA)** 和 **MeshAvatar (MA)**。这类方法试图从多视角视频中分解出人体的材质参数（如漫反射率、法线、BRDF），再通过显式物理渲染在新光照下合成图像。其根本瓶颈在于：逆渲染本身是一个高度病态问题，从有限视角中准确恢复空间变化的材质属性极为困难，导致重光照结果模糊、缺乏高频细节。更重要的是，这些方法在训练时通常假设均匀光照或有限照明条件，测试时需额外优化缩放因子，泛化到任意自然光照的能力有限。

**第二类是一次一光（One-Light-at-a-Time, OLAT）方法**，通过依次点亮光源捕获人体在不同方向光照下的外观基函数，再线性组合得到新光照下的渲染结果。OLAT的致命缺陷在于数据采集成本极高——单次表演需要数百至上千次顺序光照采样，总捕获时间可达数十分钟，完全无法适用于动态表演。此外，线性组合假设材质响应是光照的线性函数，忽略了全局光照效应（如间接反弹光、次表面散射），在复杂光照下会产生累积误差。

### 核心科学问题

上述分析揭示了一个根本性的研究缺口：**能否在不依赖OLAT捕获和显式物理参数估计的前提下，从稀疏视角输入中高效生成动态人体的照片级重光照结果？**

这要求方法同时解决三个相互耦合的子问题：

1. **表示问题**：如何在有限输入下编码足够丰富的物理信息（几何、材质、着色），以支撑任意光照下的外观合成？
2. **光照融合问题**：如何将高维环境光照与局部物理特征有效结合，近似渲染方程中的半球面积分，而不显式求解OLAT基函数？
3. **效率问题**：如何实现单次前馈推理，避免逐光迭代或扩散模型的多次采样，使系统接近实时应用？

### 本文的核心洞察与方法动机

本文的核心洞察在于：**渲染方程的各分量（几何、材质、入射光）可以被编码为一致的UV空间特征，而Transformer的交叉注意力机制天然适合模拟光线在表面上的空间积分过程。** 具体而言，渲染方程描述了表面出射辐射度为入射光在半球面上的加权积分：

$$\rho(\mathbf{x})\int_{\omega_i} f_r(\mathbf{x},\omega_i,\omega_o) \mathbf{L}_i(\mathbf{x},\omega_i) V(\mathbf{x},\omega_i) \langle\omega_i,\mathbf{n}\rangle d\omega_i$$

其中材质项 $f_r$、几何项 $V$ 和 $\langle\omega_i,\mathbf{n}\rangle$ 决定了每个入射方向对最终颜色的贡献权重。交叉注意力机制中，Query来自局部物理特征（编码了几何和材质信息），Key和Value来自环境光照编码，注意力权重的计算过程恰好模拟了“根据局部表面属性选择性地聚合来自不同方向的光照贡献”这一物理过程。

基于这一洞察，本文提出 **Relightable Holoported Characters (RHC)**，核心设计包括：
- 在UV空间中编码几何、纹理、着色、视角等物理信息特征，作为光照融合的条件信号；
- 通过交叉注意力将环境光照与这些特征融合，在单次前馈中预测纹素对齐的3D高斯参数；
- 采用交替均匀光照跟踪帧与随机环境光照照明的数据捕获策略，使模型在训练中暴露于多样化的光照-外观配对。

该方法首次实现了从稀疏视角RGB输入到任意光照下照片级渲染的端到端映射，无需OLAT捕获、显式材质估计或测试时优化，为动态人体的实时全息传送与光照编辑开辟了新路径。

## 核心方法与创新机理

RHC 的核心创新在于将传统渲染方程的各分量编码为 UV 空间内一致的物理信息特征，并利用 Transformer 交叉注意力机制在单次前馈推理中近似光线积分，从而绕过了对耗时的一次一光（OLAT）捕获和线性组合的依赖。这一设计在四个关键维度上实现了对现有方法的系统性改进。

### 从 OLAT 线性组合到单次前馈渲染方程近似

现有动态人体重光照方法（如 **Relighting4D**）依赖 OLAT 捕获：在 Lightstage 中为每个光照方向单独采集图像，推理时通过线性组合 OLAT 基来合成环境光照下的外观。这一范式存在两个根本性瓶颈：OLAT 捕获耗时极长，且线性组合无法建模高光反射、次表面散射等非线性光传输效应。

RHC 的解决方案是将渲染方程的积分过程隐式地交由网络学习。渲染方程描述了表面出射辐射度：

$$\rho(\mathbf{x})\int_{\omega_i} f_r(\mathbf{x},\omega_i,\omega_o) \mathbf{L}_i(\mathbf{x},\omega_i) V(\mathbf{x},\omega_i) \langle\omega_i,\mathbf{n}\rangle d\omega_i$$

RelightNet 通过交叉注意力机制模拟了这一积分：环境图 $\mathbf{E}$ 作为查询（query）与 UV 空间的物理特征进行交互，每个纹素聚合来自所有方向的光照贡献。如原文所述：“The cross-attention formulation is inspired by the rendering equation (Eq. 4), where each UV texel aggregates light contributions from all directions”。这一设计的有效性在消融实验中得到验证：禁用交叉注意力后，PSNR 从 32.07 降至 31.88（Table 2），模型无法建立环境光照与外观之间的正确关联（Figure 13）。

### 物理信息特征：将渲染方程分量编码为 UV 空间先验

RHC 的第二个关键创新在于显式编码渲染方程的物理分量作为网络输入，而非让网络从 RGB 像素中隐式学习。具体而言，RelightNet 的输入特征 $\mathbf{f}$ 包含：

$$\mathbf{f} = \{\tilde{\mathbf{n}}, \hat{\mathbf{n}}, \mathbf{p}, \hat{\boldsymbol{\rho}}, \mathbf{d}, \gamma\}$$

其中 $\tilde{\mathbf{n}}$ 为高分辨率法线图（来自 Sapiens 估计），$\hat{\mathbf{n}}$ 为粗网格法线，$\mathbf{p}$ 为位置图，$\hat{\boldsymbol{\rho}}$ 为反照率（由 AlbedoNet 从均匀光照图像中估计），$\mathbf{d}$ 为漫反射着色（预积分环境光照与可见性），$\gamma$ 为视角编码。

这一设计的因果逻辑在于：通过提供近似的物理分量，网络只需学习从近似到真实外观的残差，而非从零开始建模完整的光传输。消融实验证实了每个分量的必要性：
- 移除几何特征（法线 + 位置图）使 PSNR 下降 0.34（Table 2），模型无法正确建模姿态相关的褶皱细节和靠近光源时的光照变化（Figure 14）；
- 移除漫反射着色特征使 PSNR 降至 31.59，模型无法捕捉自阴影（Figure 6）；
- 移除反照率特征导致纹理漂移，因为跟踪误差无法被补偿（Figure 6）；
- 移除所有物理信息特征导致渲染质量显著下降（Figure 15）。

### 多样化光照捕获策略：随机环境图与均匀光照交替

训练数据的光照多样性是 RHC 泛化能力的基础。传统方法（如 R4D 原始设置）在均匀光照下训练，测试时需要对环境图进行缩放因子优化。RHC 的捕获策略交替使用两类帧：随机环境图照明的重光照帧和均匀光照的跟踪帧（Figure 2）。

这一策略的因果机制在于：
- 随机环境图提供了多样化的光照条件，迫使模型学习光照与外观之间的泛化映射，而非记忆特定光照模式；
- 均匀光照帧为骨架跟踪和反照率估计提供了稳定的输入，避免了光照变化对几何估计的干扰。

Table 7 的消融实验直接证明了光照多样性的关键作用：当训练光照条件从完整数据集减少到仅 100 种时，PSNR 从 32.07 骤降至 28.79。Figure 12 进一步展示了这一策略对基线方法的提升：R4D 在均匀光照下训练时泛化能力极差，而使用多样化光照和真实环境图重新训练后（R4D + GT Env），泛化能力显著改善。

### 纹素对齐 3D 高斯泼溅：统一几何与外观的输出表示

RHC 将重光照结果表示为附着于粗网格的纹素对齐 3D 高斯泼溅，而非传统的 RGB 图像或隐式场。每个纹素对应一组高斯参数（位置偏移 $\delta\mathbf{p}$、缩放 $\delta\mathbf{s}$、透明度 $o$、颜色 $\mathbf{c}$），RelightNet 在 UV 空间中一次性预测所有参数：

$$\mathbf{g} = \mathscr{F}(\mathbf{f}; \mathbf{E})$$

这一表示选择的优势在于：UV 空间天然与网格拓扑对齐，使得物理特征（法线、反照率、着色）可以在统一的参数域内与光照条件融合；3D 高斯泼溅则提供了高效的可微分渲染，支持自由视角合成。Table 4 的运行时间分解显示，整个流程约 2 FPS，主要瓶颈在 Sapiens 法线估计（244 ms），而 RelightNet 本身仅需约 50 ms。

### 与基线的系统性差异总结

| 设计维度 | 基线方法 | RHC |
|---------|---------|-----|
| 光照条件输入 | 训练时均匀光照或有限照明，测试时优化缩放因子 | 训练时交替随机环境图与均匀光照，测试时直接输入 HDR 环境图 |
| 特征表示 | 隐式光线场或 BRDF 材质参数 | UV 空间物理信息特征（几何、反照率、着色、视角） |
| 重光照架构 | 显式物理渲染或生成式扩散模型 | 2D 卷积 + 自注意力 + 交叉注意力，单次前馈预测 |
| 输出表示 | RGB 图像或隐式场 | 纹素对齐 3D 高斯泼溅 |

这些创新共同使 RHC 在 5 个主体的 Lightstage 基准上，以 PSNR 31.49、LPIPS 6.70、SSIM 89.56 显著优于所有基线方法（Table 1），同时支持分布外光照（OLAT、近场）的合理泛化（Figure 11）。

RHC 的整体设计围绕一个核心洞察展开：将渲染方程的各分量编码为一致的 UV 空间特征，并利用 Transformer 交叉注意力模拟光线的空间积分，从而在单次前馈中从稀疏视角输入生成动态人体的照片级重光照结果。该方法避免了传统 OLAT（一次一光）捕获和线性组合的昂贵开销，也无需在推理时进行迭代优化。

### 输入与输出

系统接收四类输入：
1. **稀疏 RGB 图像**（默认 4 视角）：在均匀光照下拍摄，用于提供外观和几何线索；
2. **骨架运动序列**：驱动角色动画的骨骼姿态参数；
3. **HDR 环境图**：目标光照条件，在训练时交替使用随机环境图和均匀光照，在测试时可直接输入任意环境图；
4. **虚拟相机参数**：指定新视角的观察方向。

输出为在新视角下、受目标环境图照明的照片级真实感渲染图像。

### 流水线模块

整个流水线由四个核心模块串联构成，其信息流如 Figure 3 所示：

**1. 角色动画模块（Character Animation Module）**

该模块以骨架运动为驱动，将模板网格变形为时域一致的粗网格。具体而言，嵌入图变形网络 $\mathcal{G}_{\mathrm{eg}}$ 从归一化运动序列预测节点的旋转 $\mathbf{a}_{t}$ 和平移 $\mathbf{b}_{t}$，顶点细化网络 $\mathcal{G}_{\mathrm{delta}}$ 预测逐顶点位移 $\mathbf{\Delta}_{t}$，得到规范空间网格 $M_{t}^{c} = T(\bar{M}, \mathbf{a}_{t}, \mathbf{b}_{t}, \Delta_{t})$。随后通过线性混合蒙皮（LBS）施加姿态，获得最终姿态网格 $M_{t} = \mathcal{W}(M_{t}^{c}, \pmb{\theta}_{t}, \pmb{W})$。

**2. 物理信息特征提取（Physics-informed Feature Extraction）**

在姿态网格的 UV 空间中，编码渲染方程各分量的近似值，形成物理信息特征栈 $\mathbf{f} = \{\tilde{\mathbf{n}}, \hat{\mathbf{n}}, \mathbf{p}, \hat{\pmb{\rho}}, \mathbf{d}, \gamma\}$：
- **几何特征**：高频法线 $\tilde{\mathbf{n}}$（来自 Sapiens 法线估计）与低频法线 $\hat{\mathbf{n}}$（来自网格），以及位置图 $\mathbf{p}$，共同编码表面朝向和空间位置；
- **纹理特征** $\hat{\pmb{\rho}}$：由 AlbedoNet 从稀疏视角图像预测的反照率；
- **着色特征** $\mathbf{d}$：在网格上对环境光照进行预积分漫反射着色 $\mathbf{d} = \int_{\omega_{i}} L_{i}(\mathbf{x}, \omega_{i}) \mathbf{V}(\mathbf{x}, \omega_{i}) \langle\omega_{i}, \mathbf{n}\rangle d\omega_{i}$，引导网络关注高频细节而非低频照明；
- **视角编码** $\gamma$：对虚拟相机方向进行位置编码，使网络学习视角相关效果（如镜面反射）。

**3. RelightNet**

RelightNet 是一个 2D 卷积网络，融合自注意力和交叉注意力机制，从物理特征和环境图预测纹素对齐的 3D 高斯参数 $\mathbf{g} = \mathscr{F}(\mathbf{f}; \mathbf{E})$。其架构设计（详见 Table 3）包含下采样、自注意力、交叉注意力和上采样层。交叉注意力层以环境图编码为条件，使每个 UV 纹素能够聚合来自所有方向的光照贡献，这直接对应渲染方程中的积分项（Equation 4），从而隐式学习完整的光传输——包括镜面反射、次表面散射等复杂效果。

**4. 高斯泼溅渲染器（Gaussian Splatting Renderer）**

RelightNet 输出的纹素对齐高斯参数（位置偏移 $\delta\mathbf{p}$、缩放 $\delta\mathbf{s}$、透明度 $o$、颜色 $\mathbf{c}$）与粗网格顶点结合，形成附着于网格表面的 3D 高斯。最终通过高斯泼溅渲染管线，将 3D 高斯投影到图像平面（投影协方差 $\mathbf{\Sigma}_i = \mathbf{J}_i \mathbf{W}_i \mathbf{R}_i \mathrm{diag}(\mathbf{s}_i) \mathrm{diag}(\mathbf{s}_i)^\top \mathbf{R}_i^\top \mathbf{W}_i^\top \mathbf{J}_i^\top$），并沿光线进行 alpha 合成 $\mathbf{C}_p = \sum_{j \in \mathcal{N}} \mathbf{c}_j \alpha_j \prod_{k=1}^{j-1} (1 - \alpha_k)$，得到最终重光照图像。

### 训练策略

训练采用两阶段策略。预热阶段使用正则化损失 $L_{\mathrm{Warmup}}$ 约束高斯参数的缩放、位移、透明度和颜色，确保训练初期稳定。正式训练阶段，交替使用随机环境图光照和均匀光照的捕获帧，使模型学习多样化光照条件下的光传输。消融实验（Table 7）表明，当训练光照条件从完整多样化集合减少到仅 100 种时，PSNR 从 32.07 骤降至 28.79，验证了多样化光照数据对学习准确重光照的关键作用。

RHC 由四个核心模块串联构成：角色动画模块、物理信息特征提取、RelightNet 重光照网络和高斯泼溅渲染器。整体流程为：从稀疏视角均匀光照图像出发，通过骨架运动驱动模板网格变形，在 UV 空间提取编码渲染方程各分量的物理特征，再由 RelightNet 结合环境图预测纹素对齐的 3D 高斯参数，最终经高斯泼溅渲染得到重光照图像。

### 角色动画模块

该模块将骨架运动转换为时域一致的粗网格，作为后续特征提取和高斯放置的几何载体。给定模板网格 $\bar{M}$ 和归一化运动序列 $\tilde{\pmb\theta}_t$，首先通过嵌入图变形网络和顶点细化网络预测规范空间网格：

$$M_{t}^{c} = T(\bar{M}, \mathbf{a}_{t}, \mathbf{b}_{t}, \Delta_{t})$$

其中 $\mathbf{a}_{t}, \mathbf{b}_{t} = \mathcal{G}_{\mathrm{eg}}(\bar{M}, \tilde{\pmb\theta}_{t})$ 为嵌入图节点的旋转和平移，$\Delta_{t} = \mathcal{G}_{\mathrm{delta}}(\bar{M}, \tilde{\pmb\theta}_{t})$ 为逐顶点偏移。随后通过线性混合蒙皮（LBS）得到姿态空间网格：

$$M_{t} = \mathcal{W}(M_{t}^{c}, \pmb\theta_{t}, \pmb{W})$$

其中 $\pmb{W}$ 为蒙皮权重。该粗网格为后续所有 UV 空间操作提供几何基准。

### 物理信息特征提取

本模块的核心洞察是将渲染方程各分量编码为一致的 UV 空间特征，使网络无需显式求解 OLAT 即可隐式学习光传输。渲染方程描述表面在方向 $\omega_o$ 上的出射辐射度：

$$\rho(\mathbf{x})\int_{\omega_i} f_r(\mathbf{x},\omega_i,\omega_o) \mathbf{L}_i(\mathbf{x},\omega_i) V(\mathbf{x},\omega_i) \langle\omega_i,\mathbf{n}\rangle d\omega_i$$

RHC 将方程中的几何、材质、光照和视角分量分别编码为以下 UV 空间特征：

- **几何特征**：包含高频法线 $\tilde{\mathbf{n}}$（来自 Sapiens 法线估计）和低频法线 $\hat{\mathbf{n}}$（来自粗网格），以及位置图 $\mathbf{p}$。高频法线捕捉皱纹等细节，位置图提供空间上下文以建模近场光照效应。
- **纹理特征**：通过 AlbedoNet 从稀疏视角图像预测反照率 $\hat{\pmb\rho}$，为网络提供材质先验。
- **着色特征**：在粗网格上计算仅考虑直接环境光照的预积分漫反射着色：

$$\pmb{d} = \int_{\omega_i} L_i(\pmb{x}, \omega_i) \pmb{V}(\pmb{x}, \omega_i) \langle\omega_i, \pmb{n}\rangle d\omega_i$$

该物理着色使网络专注于高频外观而非低频光照，消融实验证实移除该特征后模型无法正确捕捉自阴影（PSNR 降至 31.59）。
- **视角特征**：编码虚拟相机视角 $\gamma$，使网络能够学习视角相关效应（如镜面反射）。

### RelightNet 重光照网络

RelightNet 是本方法的核心创新，其设计灵感直接来源于渲染方程中的积分形式。网络将物理特征 $\pmb{f}$ 和环境图 $\pmb{E}$ 映射为重光照纹理 $\pmb{g}$：

$$\pmb{g} = \mathscr{F}(\pmb{f}; \pmb{E}), \quad \pmb{f} = \{\tilde{\pmb{n}}, \hat{\pmb{n}}, \pmb{p}, \hat{\pmb\rho}, \pmb{d}, \gamma\}$$

架构上，RelightNet 是一个 2D 卷积网络，集成了自注意力和交叉注意力机制。交叉注意力使每个 UV 纹素能够聚合来自所有方向的光照贡献，模拟渲染方程中入射光在半球上的积分过程。消融实验表明，禁用交叉注意力后 PSNR 从 32.07 降至 31.88，验证了该机制对环境光照融合的关键作用。

网络预测的输出是纹素对齐的 3D 高斯参数，包括位置偏移 $\delta\pmb{p}_i$、缩放因子 $\delta\pmb{s}_i$、透明度 $o_i$ 和颜色 $\pmb{c}_i$。最终高斯参数通过与粗网格上的均值参数结合得到：

$$\pmb{p}_i = \bar{\pmb{p}}_i + \delta\pmb{p}_i, \quad \pmb{s}_i = \bar{\pmb{s}}_i \odot \delta\pmb{s}_i$$

### 高斯泼溅渲染器

预测的 3D 高斯通过标准泼溅管线渲染为最终图像。每个 3D 高斯投影到图像平面的 2D 协方差矩阵为：

$$\boldsymbol\Sigma_i = \mathbf{J}_i \mathbf{W}_i \mathbf{R}_i \mathrm{diag}(\mathbf{s}_i) \mathrm{diag}(\mathbf{s}_i)^\top \mathbf{R}_i^\top \mathbf{W}_i^\top \mathbf{J}_i^\top$$

其中 $\mathbf{J}_i$ 为投影变换的雅可比矩阵，$\mathbf{W}_i$ 为视角变换矩阵，$\mathbf{R}_i$ 为旋转矩阵。像素颜色通过沿光线的 alpha 合成得到：

$$\mathbf{C}_p = \sum_{j \in \mathcal{N}} \mathbf{c}_j \alpha_j \prod_{k=1}^{j-1} (1 - \alpha_k)$$

其中 $\alpha_j$ 由高斯权重和透明度 $o_j$ 共同决定。

### 训练损失与预热机制

训练初期采用预热损失稳定优化，约束高斯参数偏离初始值：

$$L_{\mathrm{Warmup}} = \frac{1}{N_G}\sum_{i=1}^{N_G} \big( \lambda_{\mathrm{s}} \| s_i - 1 \|_2^2 + \lambda_{\mathrm{t}} \| \delta \mathbf{p}_i \|_2^2 + \lambda_{\mathrm{o}} \| o_i - o_0 \|_2^2 + \lambda_{\mathrm{c}} \| \mathbf{c}_i - \mathbf{c}_i^{\mathrm{tem}} \|_2^2 \big)$$

该损失约束高斯缩放接近 1、位置偏移接近零、透明度接近初始值、颜色接近模板颜色，确保网络在早期阶段稳定收敛。

![[assets/figures/papers/paper_list_l2137_https_arxiv_org_abs_2512_00255/figures/013_Table_3.jpg]]
*Table 3: Illustration of the RelightNet architecture. In the operation column, ”C” denotes a convolution layer, ”SA” denotes a selfattention layer, ”CA” denotes a cross-attention layer, ”DS” and ”US” denote down-sampling and up-sampling layers with scale factors equal to 2*

![[assets/figures/papers/paper_list_l2137_https_arxiv_org_abs_2512_00255/figures/009_Figure_6.jpg]]
*Figure 6: Ablation of key design components. Removing our diffuse Truth geometry features hinders the learning of pose-dependent effects and also leads to reduced wrinkle fidelity due to missing highfrequency geometry. Excluding the albedo feature causes texture drift from tracking errors. Without diffuse shading, the model fails to capture self-shadows correctly*

## 实验与关键发现

### 核心实验结果

RHC 在 5 名主体的多视角 Lightstage 基准上全面超越现有方法。Table 1 显示，平均 PSNR 达到 31.49，较最强基线 **Relighting4D**（R4D + GT Env）的 30.29 提升 +1.20；感知损失 LPIPS 从 9.50 降至 6.70（降幅 2.80）；结构相似度 SSIM 从 86.77 升至 89.56（+2.79）。值得注意的是，R4D、**IntrinsicAvatar**（IA）和 **MeshAvatar**（MA）等逆渲染方法均在训练时额外提供了真实环境图（GT Env）以进行公平比较，而 RHC 仍显著领先，表明其单次前馈重光照策略在精度和泛化性上的双重优势。

![[assets/figures/papers/paper_list_l2137_https_arxiv_org_abs_2512_00255/figures/006_Table_1.jpg]]
*Table 1: Quantitative evaluation. We compare our method to prior methods for human performance relighting from uncalibrated lighting conditions (R4D [4]) as well as a variant (R4D + GT Env), where we provide the ground truth environment maps for training. We further extend this training strategy to state-of-the-art methods IA [56] and MA [3]. Moreover, we compare to non-relightable sparse free-view rendering methods (HPC [51]) and a variant where we employ a recent foundational model [22] for image-based relighting (HPC + NG). Note that we outperform all competing methods across subjects and metrics*

定性对比（Figure 5）进一步揭示差距的本质：基于隐式场的方法（IA、MA）在复杂姿态下产生模糊渲染，而 R4D 在细节保留和光照一致性上存在不足。非重光照的 **Holoported Characters**（HPC）及后处理重光照变体（HPC + Neural Gaffer）则无法正确响应环境光变化，产生不自然的着色。RHC 在所有主体和环境图下均生成照片级细节和物理一致的光照效果。

### 消融实验

Table 2 系统拆解了各设计组件的贡献。移除几何特征（包含法线和位置图）导致 PSNR 从 32.07 降至 31.73（-0.34），Figure 6 和 Figure 14 显示这主要损害了褶皱细节和近光源时的重光照准确性。移除漫反射着色特征使 PSNR 降至 31.59，模型无法正确捕捉自阴影（Figure 6），验证了物理信息着色对解耦低频光照与高频外观的关键作用。禁用交叉注意力机制后 PSNR 降至 31.88，Figure 13 显示模型丧失了与环境光照的正确关联，无法学习完整的光线传输。

![[assets/figures/papers/paper_list_l2137_https_arxiv_org_abs_2512_00255/figures/007_Table_2.jpg]]
*Table 2: Ablation study. We ablate different design choices of our method. Removing individual components degrades metrics, confirming their importance. Skeleton tracking from sparse views shows minimal decrease, mainly due to hand tracking errors. Fewer input views also degrade results because of increased occlusion. Finally, OLAT data capture accumulates errors from each OLAT rendering*

输入视角数从 4 减至 2 时 PSNR 降至 32.00，模型开始生成幻觉细节（Figure 9），主要源于遮挡增加和跟踪精度下降。将骨架跟踪和图像输入同时限制为 2 视角时性能进一步恶化（Table 6），但主要瓶颈在于跟踪误差而非渲染网络本身。

![[assets/figures/papers/paper_list_l2137_https_arxiv_org_abs_2512_00255/figures/011_Figure_9.jpg]]
*Figure 9: Effect of the number of input views for our model. As the number of input views decrease, we note the model begins to hallucinate details*

### 光照多样性与数据策略

训练光照多样性对模型性能具有决定性影响。Table 7 显示，将训练光照条件从完整集减少至 100 种时，PSNR 从 32.07 骤降至 28.79，模型严重过拟合。Figure 10 可视化了这一退化趋势。这验证了论文的核心数据策略——交替使用随机环境图光照和均匀光照跟踪帧——对于学习通用重光照能力至关重要。相比之下，端到端学习 OLAT 并线性组合的方法（Figure 7）不仅速度慢，且累积各 OLAT 渲染的误差，导致质量下降。

### 失败模式与局限性

尽管 RHC 在分布内测试中表现优异，但存在明确的失效边界：

1. **跨主体泛化**：模型为特定人物定制，需为每个主体单独训练。Table 6 的小样本适应实验显示，跨主体微调会引入材质和 UV 偏差导致的明显伪影（Figure 15），表明物理特征编码仍与原始主体强绑定。

2. **推理速度**：完整管线约 2 FPS，主要瓶颈为 Sapiens 表面法线估计（244 ms，Table 4），离实时应用距离较远。Table 5 显示 RHC 在速度上优于部分基线但仍需优化。

3. **拓扑与材质限制**：无法处理拓扑变化（如脱掉外套）、半透明材质和配饰（眼镜等），在极端姿态和剧烈光照变化下可能出现伪影。

4. **分布外泛化**：Figure 11 显示模型在未见过的 OLAT 环境图和近场光照（人体平移 35 cm）下仍能生成合理结果，但质量低于分布内测试，说明对物理特征近似的依赖限制了极端光照条件下的精度。

![[assets/figures/papers/paper_list_l2137_https_arxiv_org_abs_2512_00255/figures/014_Figure_11.jpg]]
*Figure 11: OOD comparison. Here, we compare our method on out-of-distribution lighting conditions, i.e. OLAT environment maps. Notably the model never saw OLAT environment maps during training. Nonetheless, it can generate plausible results while competing methods either produce blurry renderings or completely fail. Moreover, we illustrate that our method can reproduce near field lighting effects by translating the human by 35cm, i.e. modifying the positional map and diffuse shading, and we can observe a plausible change in illumination*

## 定位与知识库关联

### 1. 任务定位与核心问题

**Relightable Holoported Characters (RHC)** 解决的核心任务是从稀疏视角（4个RGB相机）的均匀光照输入中，实时生成动态人体的照片级真实感重光照渲染。该任务位于三维视觉、神经渲染与计算摄影的交叉点，其核心瓶颈在于：现有动态人体重光照方法要么依赖耗时的一次一光（One-Light-at-a-Time, OLAT）捕获和线性组合，要么仅限于重放预捕获的表演，无法在推理时从稀疏视角输入中高效生成照片级真实感的重光照结果。

RHC 的核心洞察是将渲染方程的各分量编码为一致的UV空间物理信息特征，并利用Transformer交叉注意力模拟光线的空间积分，从而在不显式求解OLAT的情况下，从稀疏视角输入中高效生成动态人体的照片级重光照结果。这一设计将重光照问题从“物理求解”转化为“数据驱动的特征融合与残差学习”。

### 2. 方法谱系与基线关系

RHC 的方法设计处于以下几条技术路线的交汇处：

#### 2.1 逆渲染动态人体重光照

这类方法试图从图像中恢复人体材质（如BRDF）和几何信息，再通过物理渲染进行重光照。代表性工作包括：

- **Relighting4D (R4D)**：从非标定光照条件下进行人体表演重光照的代表性方法。其原始设置在训练时仅使用均匀光照，测试时需要优化缩放因子来匹配目标光照。RHC的实验表明，当为R4D提供真实环境图进行训练（R4D + GT Env），其性能有显著提升，但仍不及RHC（Table 1: PSNR 30.29 vs 31.49）。这揭示了纯逆渲染管线在稀疏视角下的固有局限——材质与几何的歧义性难以通过有限视角完全消除。

- **IntrinsicAvatar (IA)**：基于隐式场的逆渲染方法，同样受益于真实环境图训练策略。在Table 1中，IA + GT Env的PSNR为29.04，显著低于RHC的31.49。

- **MeshAvatar (MA)**：基于网格的逆渲染方法，在相同训练策略下PSNR为28.48。RHC相对于这类方法的优势在于：不试图显式分解材质参数，而是让RelightNet端到端地学习从物理特征到重光照外观的残差映射，避免了逆渲染中常见的材质-光照歧义问题。

#### 2.2 稀疏视角三维人体渲染

- **Holoported Characters (HPC)**：从稀疏视角进行非重光照三维人体渲染的方法。RHC将其作为基线，并进一步测试了HPC + Neural Gaffer (NG)的组合——即在HPC渲染结果上应用基于图像的重光照后处理网络。Table 1显示，HPC + NG的PSNR仅为25.44，远低于RHC的31.49。这表明简单的后处理重光照无法正确处理复杂的光传输效应（如自阴影、镜面反射），而RHC在特征层面融合光照信息的设计更为有效。

#### 2.3 技术组件的谱系定位

RHC的各个技术组件可追溯到以下技术传统：

- **3D高斯泼溅（3D Gaussian Splatting）**：RHC采用纹素对齐的3D高斯作为输出表示，继承了3DGS的高效可微渲染优势。与原始3DGS不同，RHC的高斯参数由RelightNet从物理特征和环境图预测，而非从多视图图像优化得到。

- **UV空间特征编码**：将几何、纹理、着色等物理信息编码到一致的UV空间，这一设计借鉴了纹理空间表示在人体渲染中的成功经验，但RHC的创新在于将这些特征作为Transformer的输入，而非直接用于渲染。

- **交叉注意力与渲染方程**：RelightNet中的交叉注意力机制直接受渲染方程启发——每个UV纹素通过交叉注意力聚合来自所有方向的光照贡献，模拟渲染方程中的积分过程（Equation 4）。这一设计将物理先验以网络结构的形式注入学习过程，是RHC方法的核心创新点。

### 3. 关键设计选择与消融证据

消融实验（Table 2）揭示了各设计组件的因果作用：

| 消融条件 | PSNR | 关键发现 |
|---------|------|---------|
| 完整模型 | 32.07 | 基线性能 |
| 移除几何特征 | 31.73 | 丢失姿态相关效果和高频褶皱细节 |
| 移除漫反射着色 | 31.59 | 无法正确捕捉自阴影（Figure 6） |
| 禁用交叉注意力 | 31.88 | 环境光照融合失败，无法学习正确的光照-外观关联 |
| 仅2个输入视角 | 32.00 | 遮挡增加导致幻觉细节 |
| 仅100种光照训练 | 28.79 | 光照多样性不足导致严重过拟合 |

这些消融结果验证了RHC设计的因果逻辑：物理信息特征提供几何和材质的先验约束，交叉注意力实现光照的全局融合，而多样化的光照训练数据则是泛化能力的基础。

### 4. 适用边界与局限

RHC的适用边界由以下限制定义：

1. **主体特异性**：模型为每个主体单独训练，跨主体泛化能力差。小样本跨主体适应（Table 6）存在明显的材质和UV偏差，导致伪影（Figure 15）。这限制了RHC在“为每个用户构建个性化虚拟化身”场景之外的应用。

2. **推理速度瓶颈**：推理速度约2 FPS，主要瓶颈为Sapiens表面法线估计（244 ms，Table 4），离实时应用（>30 FPS）有显著差距。法线估计的加速（如模型蒸馏或轻量网络）是工程化的关键路径。

3. **拓扑与材质限制**：无法处理拓扑变化（如脱掉外套）、半透明材质和配饰（眼镜等）。这源于方法对固定模板网格和UV参数化的依赖。

4. **极端条件伪影**：在极端姿态和剧烈光照变化下可能出现伪影，这与稀疏视角输入的固有信息不足有关。

5. **分布外光照**：虽然RHC在未见过的OLAT环境图和近场光照下展现出一定的泛化能力（Figure 11），但这是定性结果，缺乏定量评估。在极端分布外光照条件下的鲁棒性仍需进一步验证。

### 5. 开放问题与未来方向

基于RHC的局限和方法设计，以下开放问题值得关注：

1. **跨主体可重光照角色模型**：如何利用大规模生成式先验（如扩散模型或多模态大模型）实现主体无关的重光照？这需要解决不同主体间几何拓扑、材质属性和UV参数化的对齐问题。

2. **实时推理**：能否通过模型蒸馏、轻量法线估计或专用推理硬件将推理速度提升至实时？法线估计模块（244 ms）是当前最显著的加速目标。

3. **动态拓扑与复杂材质**：如何扩展方法以处理宽松衣物、动态拓扑变化和半透明材质？可能需要引入动态UV参数化或隐式表示来替代固定模板网格。

4. **极稀疏视角鲁棒性**：在仅有2个视角输入的条件下，如何通过更强的姿态先验或时序信息保持渲染质量？当前2视角结果（PSNR 32.00 vs 32.07）的下降主要源于跟踪误差。

5. **实时交互式全息传送**：如何将RHC集成到完整的全息传送系统中，实现实时交互与动态场景光照编辑？这涉及端到端延迟优化、网络传输和用户交互设计等系统工程问题。

6. **光照多样性的理论边界**：Table 7显示光照条件数量从5000降至100时PSNR从32.07降至28.79，但光照多样性的最优策略（如环境图的采样分布、动态范围覆盖）仍缺乏理论指导。

## 原文 PDF

![[paperPDFs/CVPR_2026/Relightable_Holoported_Characters_Capturing_and_Relighting_Dynamic_Human_Performance_from_Sparse_Views.pdf]]
