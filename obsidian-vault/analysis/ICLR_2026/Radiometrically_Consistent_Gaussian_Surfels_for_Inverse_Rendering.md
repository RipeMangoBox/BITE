---
title: "Radiometrically Consistent Gaussian Surfels for Inverse Rendering"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Radiometrically_Consistent_Gaussian_Surfels_for_Inverse_Rendering.pdf
project_link: https://qbhan.github.io/radiogs-page/
code_link: null
openreview_forum_id: lKqE7UuMvp
aliases:
- RRCGS
- RCGSIR
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入辐射一致性损失（radiometric consistency loss），强制高斯曲面片在未观测方向上的学习辐射与其基于物理渲染的辐射一致，形成一个自校正反馈循环，为间接辐射提供物理监督。"
primary_logic: "通过最小化每个高斯曲面片的辐射与物理渲染辐射之间的残差，可以将相机视点上的强约束经由渲染方程传播到未观测方向，使曲面片辐射满足物理一致性，从而实现准确的全局光照建模。"
claims:
- "辐射一致性损失显著提升了间接光照重构质量，在TensoIR数据集上间接光照PSNR从30.10（无L_rad）提升到32.88（Ours）。"
- "在训练视点数仅有25%的极端情况下，Ours的间接光照PSNR仅下降-0.17dB，而无L_rad的版本下降-2.21dB，证明对未观测方向提供了有效监督。"
- "RadioGS在TensoIR和Synthetic4Relight两个数据集上均取得最优的NVS、材质重建与重光照指标，且训练时间仅1小时（4090 GPU）。"
- "所提出的微调重光照策略在新增2分钟微调后，可实现约5.9ms的渲染速度和极低的VRAM占用（308MB），显著优于基于光线追踪的重光照方法。"
---

# Radiometrically Consistent Gaussian Surfels for Inverse Rendering

> [!tip] 核心洞察
> 通过最小化每个高斯曲面片的辐射与物理渲染辐射之间的残差，可以将相机视点上的强约束经由渲染方程传播到未观测方向，使曲面片辐射满足物理一致性，从而实现准确的全局光照建模。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 辐射一致的高斯曲面片逆渲染 |
| 英文题名 | Radiometrically Consistent Gaussian Surfels for Inverse Rendering |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=lKqE7UuMvp) · [Project](https://qbhan.github.io/radiogs-page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | RadioGS (Radiometrically Consistent Gaussian Surfels) |
| Dataset | TensoIR, Synthetic4Relight |

> [!tip] 效果简介
> - TensoIR 上，NVS PSNR↑ 为 37.86，对比 36.75 (GI-GS) / 36.71 (SVG-IR) / 35.43 (IRGS)，变化 +1.43 (vs GI-GS)。
> - TensoIR 上，Albedo PSNR↑ 为 31.05，对比 30.62 (IRGS) / 29.94 (GS-IR)，变化 +0.43 (vs IRGS)。
> - TensoIR 上，Relighting PSNR↑ 为 32.09 (ray tracing) / 31.41 (finetuned*)，对比 31.10 (SVG-IR) / 29.91 (IRGS)，变化 +0.99 (ray tracing vs SVG-IR)。

## 概要

**问题瓶颈**：现有基于高斯的逆渲染方法从NVS预训练的高斯基元中查询间接辐射，但这些基元仅在有限的训练视点上被图像重建损失监督，未观测方向的辐射值完全无约束，可任意取值。这导致间接光照建模不准确，材质与光照的分解失败——这是当前高斯逆渲染方法的核心瓶颈。

**核心调控变量**：引入**辐射一致性损失**（radiometric consistency loss），强制高斯曲面片在未观测方向上的学习辐射与其基于物理渲染的辐射一致。该损失通过最小化每个曲面片辐射与物理渲染辐射之间的残差，将相机视点上的强约束经由渲染方程传播到未观测方向，形成一个自校正反馈循环，为间接辐射提供物理监督。

**方法定位**：RadioGS 是一个基于高斯曲面片和可微2D高斯光线追踪的逆渲染框架，其核心贡献在于通过辐射一致性损失为全局光照建模提供物理约束。方法包含四个关键模块：初始化阶段（融入简化辐射一致性）、逆渲染优化阶段（完整蒙特卡洛估计）、2D高斯光线追踪器（动态查询间接辐射与可见性），以及微调重光照策略（新光照下快速适配曲面片辐射）。

**主要结果**：
- 在 TensoIR 数据集上，NVS PSNR 达 37.86（较 GI-GS 提升 +1.43），Albedo PSNR 达 31.05（较 IRGS 提升 +0.43），重光照 PSNR 达 32.09（光线追踪版本）。
- 在 Synthetic4Relight 数据集上，NVS PSNR 达 34.98，重光照 PSNR 达 34.87，均超越现有方法。
- 在间接光照重建的专门评估中，间接光照 PSNR 达 32.88，显著优于 SVG-IR（25.58）和 IRGS（28.86）。
- 训练仅需约 1 小时（单张 RTX 4090），与同类方法相当；微调重光照策略可在额外 2 分钟内适配新光照，渲染速度约 5.9 ms，显存占用仅 308 MB，远优于光线追踪重光照方案。



### 逆渲染中的间接光照瓶颈

从多视角图像中恢复场景的几何、材质与光照——即逆渲染——是视觉计算的核心问题，其成果直接支撑新视角合成、重光照和虚拟物体插入等应用。近年来，基于高斯溅射（Gaussian Splatting）的逆渲染方法凭借其高效的显式表示和可微渲染能力，在重建质量和速度上取得了显著进展。然而，这些方法在**间接光照建模**上存在一个根本性缺陷。

具体而言，现有方法（如 **GS-IR** (Liang et al., 2024)、**GI-GS** (Chen et al., 2024)、**R3DG** (Gao et al., 2024)）通常从经过新视角合成预训练的高斯基元中查询间接辐射。这些基元仅在有限的训练视点上受到图像重建损失的监督，其**未观测方向的辐射值完全不受约束**，可以任意取值。这意味着当场景中的曲面需要从“看不见”的方向获取间接辐射时——例如物体缝隙间的相互反射、被遮挡表面之间的光照传递——现有方法无法提供可靠的辐射估计，导致材质与光照的分解失败，间接光照重建质量低下。

### 核心动机：从未观测方向引入物理监督

上述瓶颈的本质在于：基于图像的监督只能约束相机视角方向上的辐射，而渲染方程要求曲面在**所有入射方向**上的辐射都满足物理一致性。本文的核心动机正是弥合这一监督缺口——能否为高斯基元在未观测方向上的辐射提供物理约束，使其满足渲染方程？

这一思路的关键在于构建一个**自校正反馈回路**：如果强制每个高斯曲面片的学习辐射与基于物理渲染（Physically-Based Rendering, PBR）的辐射保持一致，那么相机视点上的强约束就可以通过渲染方程传播到未观测方向，使曲面片辐射自动满足物理一致性。这不仅能提升间接光照的重建精度，还能改善材质分解和重光照的质量。

### 技术挑战与本文目标

实现上述动机面临两个核心挑战：

1. **如何高效计算物理渲染辐射？** 渲染方程涉及对半球方向的积分，需要动态查询可见性和间接辐射。现有方法或采用预烘焙的辐照度体积，或依赖预计算的可见性，缺乏可微性且无法随几何优化动态更新。

2. **如何将物理约束高效集成到高斯框架中？** 高斯溅射的优势在于快速光栅化渲染，而物理约束需要光线追踪。如何在保持训练效率（约1小时）的前提下，将两者无缝结合？

本文提出 **RadioGS（Radiometrically Consistent Gaussian Surfels）**，通过引入**辐射一致性损失**和**可微2D高斯光线追踪**来解决上述挑战，在TensoIR和Synthetic4Relight两个数据集上均取得最优的NVS、材质重建与重光照指标，同时保持约1小时的训练时间（4090 GPU）。



## 核心方法与创新机理

### 瓶颈：未观测方向的间接辐射缺乏物理约束

现有的基于高斯的逆渲染方法（如 **GS-IR** (Liang et al., 2024)、**GI-GS** (Chen et al., 2024)、**R3DG** (Gao et al., 2024)）普遍遵循一个范式：先从新视角合成（NVS）预训练中获得高斯基元的辐射值，再将这些值作为间接辐射查询使用。然而，NVS预训练仅在有限的训练相机视点上施加图像重建损失 $\mathcal{L}_{recon}$ 进行监督，这意味着每个高斯基元在未观测方向上的辐射值**完全没有约束**，可以取任意值而不影响训练损失。当这些无约束的辐射值被用于渲染方程计算间接光照时，材质与光照的分解必然失败——这是限制该类方法间接光照建模精度的根本瓶颈。

### 核心机制：辐射一致性自校正反馈环

RadioGS 的核心创新是引入**辐射一致性损失**（radiometric consistency loss）$\mathcal{L}_{rad}$，构建一个物理驱动的自校正反馈循环。其原理简洁而关键：

1. **辐射残差定义**：对于每个高斯曲面片 $\mathbf{G}$，定义其学习到的辐射 $L_{\mathbf{G}}(x, \omega_o)$ 与基于物理渲染（PBR）的辐射 $L_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o)$ 之间的残差：

   $$\mathcal{R}_{\mathbf{G}}(x, \omega_o) = L_{\mathbf{G}}(x, \omega_o) - L_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o)$$

   其中 PBR 辐射由渲染方程给出：

   $$L_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o) = \int_{\Omega} f_r(x, \omega_o, \omega_i; \mathbf{G}) \left( V(x, \omega_i; \mathbf{G}) L_{dir}(\omega_i) + L_{ind}(x, \omega_i; \mathbf{G}) \right) (\omega_i \cdot n_x) d\omega_i$$

2. **辐射一致性损失**：对所有高斯曲面片在所有可能方向上的辐射残差取 L1 范数期望：

   $$\mathcal{L}_{rad}(\mathbf{G}) = \mathbb{E}_{j, \omega_o} \left[ \lVert \mathcal{R}_{\mathbf{G}} \rVert_1 \right]$$

3. **自校正反馈环**：$\mathcal{L}_{rad}$ 迫使曲面片的辐射值与物理渲染结果一致。由于 $L_{\mathbf{G}}^{\mathbf{PBR}}$ 本身依赖其他曲面片的辐射（作为间接光照 $L_{ind}$），当某一曲面片的辐射被修正后，它会通过渲染方程将修正传递给所有以它为间接光源的曲面片。这形成了一个**全局自校正循环**：相机视点上的强约束（$\mathcal{L}_{recon}$）经由渲染方程传播到未观测方向，使整个场景的辐射场满足物理一致性。

### 关键设计变更（Changed Slots）

#### Slot 1：未观测方向的间接辐射监督

| 维度 | Baseline | RadioGS |
|------|----------|---------|
| 监督范围 | 仅相机视点方向（$\mathcal{L}_{recon}$） | 相机方向 + 随机采样方向（$\mathcal{L}_{rad}$） |
| 未观测方向约束 | 无约束，辐射可任意取值 | 强制学习辐射与 PBR 辐射一致 |
| 物理先验 | 无 | 渲染方程驱动的物理一致性 |

**决定性证据**：消融实验（Table 4）表明，移除 $\mathcal{L}_{rad}$ 后间接光照 PSNR 从 32.88 降至 30.10。在仅用 25% 训练视点的极端条件下（Table 6），完整方法的间接光照 PSNR 仅下降 -0.17 dB，而无 $\mathcal{L}_{rad}$ 的版本下降 -2.21 dB，直接证明了辐射一致性对未观测方向的有效监督。

#### Slot 2：间接辐射的查询与可见性计算

| 维度 | Baseline | RadioGS |
|------|----------|---------|
| 查询方式 | 预烘焙辐照度体积 / 预计算可见性 | 可微 2D 高斯光线追踪器 |
| 可微性 | 不可微或部分可微 | 完全可微，支持联合优化 |
| 动态性 | 静态预计算 | 每步迭代动态追踪 |

RadioGS 部署了来自 **IRGS** (Gu et al., 2024) 的可微 2D 高斯光线追踪器，将追踪到的辐射 $L_{trace}$ 直接作为间接辐射 $L_{ind}$，将透射率的补 $1 - T_{trace}$ 作为可见性 $V$。PBR 辐射通过蒙特卡洛采样估计：

$$I_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o) \approx \frac{2\pi}{N_s} \sum_{i=1}^{N_s} f_r(x, \omega_o, \omega_i; \mathbf{G}) \left( V(x, \omega_i; \mathbf{G}) L_{dir}(\omega_i) + L_{ind}(x, \omega_i; \mathbf{G}) \right) (\omega_i \cdot n_x)$$

消融实验（Table 5）证实，将可微光线追踪替换为 split-sum 近似或预计算间接辐射会显著损害几何、反照率和重光照各项指标，**只有同时采用动态光线追踪和 $\mathcal{L}_{rad}$ 才能达到最佳性能**。

#### Slot 3：重光照流程

| 维度 | Baseline（光线追踪重光照） | RadioGS（微调重光照） |
|------|--------------------------|----------------------|
| 推理方式 | 在新光照下逐像素光线追踪 + split-sum 近似 | 在新光照下微调曲面片辐射后直接光栅化 |
| 推理时间 | 38.6 ms（64 samples） | **5.9 ms** |
| 显存占用 | 1512 MB | **308 MB** |
| 预计算开销 | 无 | 约 2 分钟微调 |

微调重光照策略的核心思想是：在新光照条件下，仅优化 $\mathcal{L}_{rad}$（权重设为 1.0，舍弃其他损失），通过少量迭代使曲面片辐射适应新的光照环境。微调后的曲面片可直接通过标准光栅化渲染，无需在推理时进行昂贵的光线追踪。这一设计将重光照从“在线光线追踪”转变为“离线微调 + 在线光栅化”，在轻微牺牲质量（与光线追踪版本相比）的前提下，实现了数量级的加速和显存压缩。



![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/030_Figure_16.jpg]]
*Figure 16: Ablation study of our initialization method on the “hotdog” scene of TensoIR dataset*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/001_Figure_1.jpg]]
*Figure 1: We introduce RadioGS, a novel inverse rendering framework that models accurate indirect illumination by providing a novel physically-based supervision on unobserved directions. (a) Compared to existing Gaussian-based methods (Gu et al., 2024; Sun et al., 2025), our method provides realistic inter-reflection between the red bulb and the blobs on the yellow lego surface, (b) leading to robust decomposition of scene properties. (c) Our method can also generate realistic indirect illumination on new lighting conditions for real objects from Stanford-ORB dataset (Kuang et al., 2023)*

RadioGS 的逆渲染流程围绕一个核心机制展开：**辐射一致性损失（radiometric consistency loss）** 为高斯曲面片在未观测方向上的辐射值提供物理监督，从而解决现有方法中间接光照建模不准确的根本瓶颈。

### 瓶颈与因果机制

现有基于高斯的逆渲染方法（如 **GS-IR** (Liang et al., 2024)、**GI-GS** (Chen et al., 2024)、**R3DG** (Gao et al., 2024)）从 NVS 预训练的高斯基元中查询间接辐射。然而，这些基元仅在有限的训练视点上被图像重建损失监督，**未观测方向的辐射值完全没有约束，可以取任意值**。这导致间接光照建模不准确，材质与光照分解失败。

RadioGS 的因果调节旋钮是：强制每个高斯曲面片在任意方向上的学习辐射 $L_{\mathbf{G}}$ 与其基于物理渲染的辐射 $L_{\mathbf{G}}^{\mathbf{PBR}}$ 一致。通过最小化二者之间的残差：

$$\mathcal{R}_{\mathbf{G}}(x, \omega_o) = L_{\mathbf{G}}(x, \omega_o) - L_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o)$$

$$\mathcal{L}_{rad}(\mathbf{G}) = \mathbb{E}_{j, \omega_o} \left[ \lVert \mathcal{R}_{\mathbf{G}} \rVert_1 \right]$$

这一约束将相机视点上的强监督经由渲染方程传播到未观测方向，形成一个**自校正反馈循环**：曲面片辐射驱动物理渲染，物理渲染反过来约束曲面片辐射，使所有高斯曲面片的辐射值满足物理一致性。

### Pipeline 模块与数据流

RadioGS 的整体 pipeline 由四个阶段组成，输入为多视角图像和对应的相机参数，输出为场景的几何、材质分解以及新光照下的重光照图像。

#### 阶段一：初始化（Initialization）

为避免早期训练不稳定，本阶段使用简化的 split-sum 近似版本辐射一致性损失预训练几何与材质的初始值。总损失函数为：

$$\mathscr{L}_{init} = \mathscr{L}_{recon} + \mathscr{L}_{recon}^{\mathbf{PBR}} + \lambda_{rad} \mathscr{L}_{rad} + \lambda_{dist} \mathscr{L}_{dist} + \lambda_{n} \mathscr{L}_{n} + \lambda_{ns} \mathscr{L}_{ns} + \lambda_{m} \mathscr{L}_{m}$$

其中 $\mathscr{L}_{recon}$ 为标准图像重建损失，$\mathscr{L}_{recon}^{\mathbf{PBR}}$ 为物理渲染图像的重建损失，其余为正则化项（深度畸变、法向平滑等）。

#### 阶段二：逆渲染优化（Inverse Rendering Optimization）

在初始化基础上，启用完整的蒙特卡洛估计辐射一致性损失，联合优化几何、材质（反照率、粗糙度）和光照的分离。总损失扩展为：

$$\mathcal{L}_{inv} = \mathcal{L}_{init} + \lambda_{as} \mathcal{L}_{as} + \lambda_{rs} \mathcal{L}_{rs} + \lambda_{light} \mathcal{L}_{light}$$

新增的反照率平滑损失 $\mathcal{L}_{as}$、粗糙度平滑损失 $\mathcal{L}_{rs}$ 和光照先验损失 $\mathcal{L}_{light}$ 进一步提升分解质量。辐射一致性损失权重设为 $\lambda_{rad}=0.2$。

#### 阶段三：2D 高斯光线追踪（2D Gaussian Ray Tracer）

在每步迭代中，系统为随机采样的 $N_g$ 个高斯曲面片和 $N_s$ 个入射方向追踪光线，动态获取可见性 $V(x, \omega_i; \mathbf{G})$ 和间接辐射 $L_{ind}(x, \omega_i; \mathbf{G})$。物理渲染辐射通过蒙特卡洛积分估计：

$$I_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o) \approx \frac{2\pi}{N_s} \sum_{i=1}^{N_s} f_r(x, \omega_o, \omega_i; \mathbf{G}) \left( V(x, \omega_i; \mathbf{G}) L_{dir}(\omega_i) + L_{ind}(x, \omega_i; \mathbf{G}) \right) (\omega_i \cdot n_x)$$

该模块是可微的，因此辐射一致性损失的梯度可以同时优化光线追踪中的高斯曲面片参数，实现端到端的联合优化。

#### 阶段四：微调重光照（Finetuning-based Relighting）

在新光照条件下，仅需通过少量迭代微调曲面片辐射（仅优化 $\mathcal{L}_{rad}$，权重设为 $\lambda_{rad}=1.0$，丢弃其他损失），即可恢复新光照下的间接光照效果。微调后直接光栅化渲染，无需在推理时进行光线追踪。

### 输入输出总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| 初始化 | 多视角图像、相机参数 | 初始几何、材质参数 |
| 逆渲染优化 | 初始化结果、光线追踪查询 | 分解后的几何、反照率、粗糙度、光照 |
| 2D 高斯光线追踪 | 当前高斯曲面片集合、采样方向 | 可见性、间接辐射 |
| 微调重光照 | 新环境光照、已分解的几何与材质 | 新光照下的重光照图像 |

整个流程在 NVIDIA RTX 4090 上总训练时长约 1 小时（30 分钟初始化 + 30 分钟逆渲染），微调重光照额外仅需约 2 分钟。



### 问题建模：高斯曲面片表示

RadioGS 采用 2D 高斯曲面片（Gaussian surfels）作为场景基元。每个曲面片通过变换矩阵将局部 UV 空间映射到世界空间：

$$
\mathbf{H} = \begin{bmatrix} s_u \mathbf{t}_u & s_v \mathbf{t}_v & \mathbf{0} & \mathbf{p} \\ 0 & 0 & 0 & 1 \end{bmatrix}
$$

其中 $s_u, s_v$ 为缩放因子，$\mathbf{t}_u, \mathbf{t}_v$ 为切向量，$\mathbf{p}$ 为曲面片中心位置。像素颜色通过按深度排序的 alpha 混合计算：

$$
\mathcal{C} = \sum_{j=1}^{N} T_j \alpha_j c_j, \quad T_j = \prod_{k=1}^{j-1} (1 - \alpha_k), \quad c_j = \mathrm{SH}_j(\omega_o)
$$

其中 $c_j$ 为球谐函数编码的视点相关辐射度。

### 核心瓶颈：未观测方向的辐射无约束

渲染方程描述了表面点 $x$ 在方向 $\omega_o$ 的出射辐射度：

$$
L(x, \omega_o) = \int_{\Omega} f_r(x, \omega_o, \omega_i) L_i(x, \omega_i) (\omega_i \cdot n_x) d\omega_i
$$

现有基于高斯的逆渲染方法（如 **GS-IR** (Liang et al., 2024)、**GI-GS** (Chen et al., 2024)）从 NVS 预训练的高斯基元查询间接辐射。但这些基元仅在有限训练视点上通过图像重建损失 $\mathcal{L}_{recon}$ 被监督，**未观测方向的辐射值完全没有约束**，可任意取值。当这些基元作为其他曲面片的间接光源时，不准确的辐射值导致间接光照建模失败，材质与光照分解退化。

### 关键模块一：辐射一致性损失

RadioGS 的核心创新是引入**辐射一致性损失**（radiometric consistency loss），强制高斯曲面片在未观测方向上的学习辐射与其基于物理渲染的辐射一致，形成自校正反馈循环。

**物理渲染辐射**：对每个高斯曲面片，根据渲染方程计算其物理渲染辐射度：

$$
L_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o) = \int_{\Omega} f_r(x, \omega_o, \omega_i; \mathbf{G}) \left( V(x, \omega_i; \mathbf{G}) L_{dir}(\omega_i) + L_{ind}(x, \omega_i; \mathbf{G}) \right) (\omega_i \cdot n_x) d\omega_i
$$

其中 $f_r$ 为 BRDF，$V$ 为可见性，$L_{dir}$ 为直接光照，$L_{ind}$ 为间接辐射。

**辐射残差**：学习到的曲面片辐射 $L_{\mathbf{G}}$ 与物理渲染辐射 $L_{\mathbf{G}}^{\mathbf{PBR}}$ 之间的差异：

$$
\mathcal{R}_{\mathbf{G}}(x, \omega_o) = L_{\mathbf{G}}(x, \omega_o) - L_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o)
$$

**辐射一致性损失**：对所有高斯曲面片在所有可能方向上的辐射残差取 L1 范数期望：

$$
\mathcal{L}_{rad}(\mathbf{G}) = \mathbb{E}_{j, \omega_o} \left[ \lVert \mathcal{R}_{\mathbf{G}} \rVert_1 \right]
$$

**工作机制**：$\mathcal{L}_{rad}$ 将相机视点上的强约束（图像重建损失）通过渲染方程传播到未观测方向。当曲面片作为间接光源向其他曲面片投射辐射时，其辐射值必须满足物理一致性，否则会在 $\mathcal{L}_{rad}$ 中产生惩罚。这为间接辐射提供了物理监督，使未观测方向不再自由取值。

### 关键模块二：可微 2D 高斯光线追踪

为实现 $\mathcal{L}_{rad}$ 中的可见性 $V$ 和间接辐射 $L_{ind}$ 计算，RadioGS 部署了可微的 2D 高斯光线追踪器（基于 **IRGS** (Gu et al., 2024)）。在每步迭代中，对采样的曲面片和入射方向追踪光线，获取光线追踪辐射 $L_{trace}$ 和透射率 $T_{trace}$，并直接用作间接辐射和可见性：$D_{ind}(x, \omega_i; \mathbf{G}) = L_{trace}$，$V(x, \omega_i; \mathbf{G}) = 1 - T_{trace}$。

物理渲染积分的蒙特卡洛估计为：

$$
I_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o) \approx \frac{2\pi}{N_s} \sum_{i=1}^{N_s} f_r(x, \omega_o, \omega_i; \mathbf{G}) \left( V(x, \omega_i; \mathbf{G}) L_{dir}(\omega_i) + L_{ind}(x, \omega_i; \mathbf{G}) \right) (\omega_i \cdot n_x)
$$

其中 $N_s$ 为入射方向采样数。该模块与辐射一致性损失联合优化，使光线追踪器在训练中持续改进可见性和间接辐射估计。

### 关键模块三：两阶段训练与微调重光照

**初始化阶段**：使用简化的 split-sum 近似版本辐射一致性损失预训练几何和材质初始值，避免早期训练不稳定。总损失为：

$$
\mathscr{L}_{init} = \mathscr{L}_{recon} + \mathscr{L}_{recon}^{\mathbf{PBR}} + \lambda_{rad} \mathscr{L}_{rad} + \lambda_{dist} \mathscr{L}_{dist} + \lambda_{n} \mathscr{L}_{n} + \lambda_{ns} \mathscr{L}_{ns} + \lambda_{m} \mathscr{L}_{m}
$$

其中包含图像重建、物理渲染重建、辐射一致性（split-sum 版本）及距离、法向、法向平滑、掩码正则化项。

**逆渲染优化阶段**：利用完整蒙特卡洛估计的辐射一致性损失优化几何、材质和光照分离：

$$
\mathcal{L}_{inv} = \mathcal{L}_{init} + \lambda_{as} \mathcal{L}_{as} + \lambda_{rs} \mathcal{L}_{rs} + \lambda_{light} \mathcal{L}_{light}
$$

新增反照率平滑 $\mathcal{L}_{as}$、粗糙度平滑 $\mathcal{L}_{rs}$ 和光照先验 $\mathcal{L}_{light}$ 损失。

**微调重光照**：在新光照条件下，仅通过最小化 $\mathcal{L}_{rad}$（设 $\lambda_{rad}=1.0$，丢弃其他损失）对曲面片辐射进行少量迭代微调（约 2 分钟），恢复新光照下的间接光照效果。微调后可直接光栅化渲染，实现约 5.9ms 的渲染速度和极低 VRAM 占用（308 MB），显著优于光线追踪重光照方法（38.6ms @64 samples, 1512 MB）。

### 证据强度说明

- **辐射一致性损失的有效性**：Table 4 显示移除 $\mathcal{L}_{rad}$ 后间接光照 PSNR 从 32.88 降至 30.10；Table 6 显示在仅 25% 训练视点下，含 $\mathcal{L}_{rad}$ 的模型间接光照 PSNR 仅下降 -0.17dB，而无 $\mathcal{L}_{rad}$ 版本下降 -2.21dB——直接证明 $\mathcal{L}_{rad}$ 对未观测方向提供了有效监督。
- **可微光线追踪的必要性**：Table 5 显示将动态光线追踪替换为 split-sum 近似或预计算间接辐射会明显损害各项指标，只有同时采用动态光线追踪和 $\mathcal{L}_{rad}$ 才能达到最佳性能。



## 实验与关键发现

### 核心瓶颈与因果机制

现有基于高斯的逆渲染方法（如 **GS-IR**（Liang et al., 2024）、**GI-GS**（Chen et al., 2024））从NVS预训练的高斯基元查询间接辐射，但这些基元仅在有限的训练视点上受图像重建损失监督，**未观测方向的辐射值完全没有约束**，可任意取值。这导致间接光照建模不准确，材质与光照分解失败。

RadioGS 通过引入**辐射一致性损失**（radiometric consistency loss）解决了这一瓶颈。其因果机制是一个自校正反馈循环：

1. 对每个高斯曲面片，计算其学习辐射 $L_{\mathbf{G}}$ 与物理渲染辐射 $L_{\mathbf{G}}^{\mathbf{PBR}}$ 之间的残差：
   $$\mathcal{R}_{\mathbf{G}}(x, \omega_o) = L_{\mathbf{G}}(x, \omega_o) - L_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o)$$
2. 通过最小化该残差的 L1 期望 $\mathcal{L}_{rad}(\mathbf{G}) = \mathbb{E}_{j, \omega_o} [ \lVert \mathcal{R}_{\mathbf{G}} \rVert_1 ]$，将相机视点上的强约束经由渲染方程传播到未观测方向。
3. 物理渲染辐射 $L_{\mathbf{G}}^{\mathbf{PBR}}$ 通过可微的2D高斯光线追踪动态计算，提供间接辐射和可见性，使整个反馈循环可端到端优化。

### 主实验结果

**TensoIR 数据集**（Table 1）：RadioGS 在 NVS、反照率重建和重光照三项核心指标上均取得最优。


![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/003_Table_1.jpg]]
*Table 1: Quantitative comparisons on TensoIR dataset (Jin et al., 2023). The results are colored in rank as 1st, 2nd, and 3rd. Our method surpasses existing Gaussian-based methods and a NeRF-based method in most metrics, while maintaining the computational efficiency with the average training time of 1 hour. We report our relighting metric using Gaussian ray tracing (Ours) and finetuningbased method (Ours*)*

| 指标 | RadioGS (Ours) | 最佳基线 | 提升 |
|------|---------------|---------|------|
| NVS PSNR↑ | **37.86** | 36.75 (GI-GS) | +1.11 |
| Albedo PSNR↑ | **31.05** | 30.62 (IRGS) | +0.43 |
| Relighting PSNR↑ | **32.09** (光线追踪) / 31.41 (微调*) | 31.10 (SVG-IR) | +0.99 |

训练总时长约1小时（30分钟初始化 + 30分钟逆渲染），与 **IRGS**（0.9h）和 **SVG-IR**（1.1h）相当，所有实验均在 NVIDIA RTX 4090 上进行。

**Synthetic4Relight 数据集**（Table 2）：RadioGS 同样全面领先。


![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparisons on Synthetic4Relight dataset*

| 指标 | RadioGS (Ours) | 最佳基线 | 提升 |
|------|---------------|---------|------|
| NVS PSNR↑ | **34.98** | 34.44 (IRGS) | +0.54 |
| Albedo PSNR↑ | **30.69** | 30.50 (IRGS) | +0.19 |
| Relighting PSNR↑ | **34.87** | 34.35 (IRGS) | +0.52 |

**定性分析**：在“lego”场景（Figure 3）中，RadioGS 在高几何复杂度区域（如铲斗）展现出明显更鲁棒的分解效果。在“hotdog”场景（Figure 5）中，RadioGS 自然建模了香肠与面包之间的相互反射，而 **IRGS** 的间接光照偏亮且波动，导致反照率偏暗；**SVG-IR** 的间接光照偏暗，导致反照率偏亮。

### 间接光照专项评估

为直接验证辐射一致性对间接光照建模的提升，作者构建了专门数据集（Table 4）。


![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/019_Table_4.jpg]]
*Table 4: Quantitative comparison against baselines (IRGS, SVG-IR) and our ablation model on our new dataset. Our method significantly outperforms all baselines in indirect illumination reconstruction*

| 方法 | 间接光照 PSNR↑ |
|------|----------------|
| **RadioGS (Ours)** | **32.88** |
| Ours w/o $\mathcal{L}_{rad}$ | 30.10 |
| IRGS | 28.86 |
| SVG-IR | 25.58 |

移除辐射一致性损失后，间接光照 PSNR 下降 2.78 dB，证明该损失是间接光照建模的核心驱动力。RadioGS 相比 **SVG-IR** 的提升高达 +7.30 dB。

### 消融研究

**辐射一致性损失的核心作用**（Figure 6, Table 4）：移除 $\mathcal{L}_{rad}$ 不仅损害间接光照，还导致反照率和重光照质量同步下降。定性结果显示，无 $\mathcal{L}_{rad}$ 时缝隙等未观测方向的辐射缺乏引导，反照率重建出现明显伪影。


![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/009_Figure_6.jpg]]
*Figure 6: Ablation studies on our radiometric consistency. The left sub-figure demonstrates how our radiometric consistency loss $\mathcal { L } _ { r a d }$ provides guidance on radiances towards unobserved views such as the interstices, leading to enhanced albedo reconstruction (red box). Also, our method guides the generation of inter-reflections between the ketchup and the plate (yellow box). The right table contains PSNR metrics for the ablation studies*

**间接光照处理策略对比**（Table 5）：将可微光线追踪替换为 split-sum 近似或预计算间接辐射，会明显损害几何、反照率和重光照各项指标。只有同时采用动态光线追踪和 $\mathcal{L}_{rad}$ 才能达到最佳性能，说明物理精确的间接辐射估计和辐射一致性监督缺一不可。


![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/022_Table_5.jpg]]
*Table 5: Ablation study on radiometric consistency strategies. We compare our method with baselines using different indirect illumination handling. Best results are highlighted in bold*

**训练视点稀缺性**（Table 6）：在仅用 25% 训练视点的极端情况下，RadioGS 的间接光照 PSNR 仅下降 -0.17 dB，而无 $\mathcal{L}_{rad}$ 的版本下降 -2.21 dB。这直接证明了辐射一致性损失对未观测方向提供了有效监督，使模型在稀疏视点下仍能保持物理一致性。


![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/023_Table_6.jpg]]
*Table 6: Ablation study on training view scarcity. We report NVS and Indirect PSNR metrics across different subsets of training views. Values in parentheses denote the performance drop relative to the 100% setting*

**超参数分析**：增加采样的曲面片数量 $N_g$ 可连续提升重建质量而不影响推理成本（Table 7）。入射采样数 $N_s$ 增至 64 后性能饱和，128 反而略有下降（Table 8），表明 64 是性价比最优选择。


![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/024_Table_7.jpg]]
*Table 7: Ablation study on the number of surfels ( N _ { g } ) for radiometric consistency. We vary N _ { g } while fixing N _ { s } = 6 4 . Increasing N _ { g } improves quality without affecting rendering cost*

**初始化策略**（Table 11）：与标准的 NVS 初始化相比，RadioGS 的初始化策略（融入简化的辐射一致性）能实现更快收敛和更优的材质分离。从训练伊始便施加物理约束对最终性能至关重要。

### 微调重光照的效率优势

**渲染速度与内存对比**（Table 12）：

| 方法 | 渲染时间 | 显存占用 |
|------|---------|---------|
| **RadioGS 微调版** | **5.9 ms** | **308 MB** |
| 光线追踪重光照 (N=64) | 38.6 ms | 1512 MB |
| 光线追踪重光照 (N=16) | 14.2 ms | 630 MB |

微调重光照策略仅需约 2 分钟预计算，之后可直接光栅化渲染，在保持接近光线追踪质量（Table 1 中 Ours* 31.41 vs Ours 32.09）的同时，实现了约 6.5 倍的渲染加速和约 5 倍的显存节省。

### 局限性与失败模式

1. **材质范围受限**：当前建模主要针对电介质材质，各向异性或高反射表面的复杂 BRDF 尚未纳入辐射一致性框架。
2. **微调重光照的误差累积**：微调版本在预计算阶段会因几何和材质的估计误差累积，导致渲染质量轻微下降（与光线追踪版本相比约 -0.68 dB）。
3. **大规模场景的渲染成本**：渲染成本随 $N_s$ 线性增加。在 MipNeRF360 场景扩展实验中（Table 9, Table 10），虽然可通过调整 $N_g$/$N_s$ 平衡效率，但在极高分辨率或动态场景下仍有挑战。
4. **光照大幅变化时的适应速度**：微调虽收敛快（约 2 分钟），但离真正的实时在线重光照仍有距离。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/015_Figure.jpg]]

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/033_Figure_19.jpg]]
*Figure 19: Illustrative figure on how our finetuning-based relighting adapts surfel radiances for new lighting conditions*

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_lKqE7UuMvp/figures/010_Table_3.jpg]]
*Table 3: Relighting Performance and Rendering cost during relighting on TensoIR dataset*




## 定位与知识库关联

### 逆渲染中的间接光照瓶颈

基于高斯泼溅的逆渲染方法近年来快速发展，但其在间接光照建模上存在一个共同的结构性缺陷。以 **GS-IR**（Liang et al., 2024）、**GI-GS**（Chen et al., 2024）、**R3DG**（Gao et al., 2024）为代表的方法，均从经过新视角合成（NVS）预训练的高斯基元中查询间接辐射。然而，NVS预训练仅在有限的训练相机视点上提供监督——这些视点通常只覆盖场景的部分观察角度。对于高斯曲面片在未观测方向上的辐射值，图像重建损失完全无法施加约束，导致这些方向的辐射可以取任意值而不受惩罚。

这一问题的因果链条是清晰的：当某个高斯曲面片作为其他曲面片的间接光源时，其向未观测方向发射的辐射被用于计算其他曲面片的入射光照。如果这些辐射值缺乏物理约束，间接光照的估计就会产生系统性偏差，进而导致材质（反照率、粗糙度）与光照的分解失败。**TensoIR**（Jin et al., 2023）作为NeRF-based的代表方法，通过隐式神经表示绕开了这一问题，但其计算开销显著更高。

### RadioGS的核心机制：辐射一致性反馈循环

RadioGS的关键创新在于引入**辐射一致性损失**（radiometric consistency loss），从根本上改变了间接辐射的监督范式。其核心洞察可以概括为：

> 通过最小化每个高斯曲面片的学习辐射 $L_{\mathbf{G}}$ 与其基于物理渲染的辐射 $L_{\mathbf{G}}^{\mathbf{PBR}}$ 之间的残差，可以将相机视点上的强约束经由渲染方程传播到未观测方向，使曲面片辐射满足物理一致性。

具体而言，辐射残差定义为：

$$\mathcal{R}_{\mathbf{G}}(x, \omega_o) = L_{\mathbf{G}}(x, \omega_o) - L_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o)$$

辐射一致性损失则对所有高斯曲面片在所有可能方向上的残差取L1范数期望：

$$\mathcal{L}_{rad}(\mathbf{G}) = \mathbb{E}_{j, \omega_o} \left[ \lVert \mathcal{R}_{\mathbf{G}} \rVert_1 \right]$$

这一机制形成了一个**自校正反馈循环**：曲面片辐射 $L_{\mathbf{G}}$ 通过渲染方程影响其他曲面片的物理渲染辐射 $L_{\mathbf{G}}^{\mathbf{PBR}}$，而 $L_{\mathbf{G}}^{\mathbf{PBR}}$ 又反过来约束 $L_{\mathbf{G}}$。这种循环传播使得即使在训练视点从未观测的方向上，曲面片辐射也必须与物理渲染结果一致，从而为间接光照提供了可靠的物理监督。

### 与现有方法的差异化对比

RadioGS与同类高斯逆渲染方法的关键差异体现在三个维度：

**1. 未观测方向的间接辐射监督**

| 方法 | 监督策略 | 未观测方向约束 |
|------|---------|---------------|
| GS-IR, GI-GS | 仅图像重建损失监督相机视点方向 | 无约束，辐射可任意取值 |
| R3DG | 逐高斯可学习残差项 | 残差仅受稀疏视点约束 |
| **RadioGS** | 辐射一致性损失 $\mathcal{L}_{rad}$ 对随机方向和相机方向施加物理约束 | 通过渲染方程传播，强制物理一致性 |

**2. 间接辐射的查询与可见性计算**

**IRGS**（Gu et al., 2024）和 **SVG-IR**（Sun et al., 2025）已引入可微光线追踪来查询间接辐射，但二者均未对未观测方向的辐射提供物理约束。RadioGS在IRGS的2D高斯光线追踪器基础上，将其与辐射一致性损失联合优化：在每步迭代中为采样的曲面片和入射方向追踪光线，动态获取可见性 $V(x, \omega_i; \mathbf{G})$ 和间接辐射 $L_{ind}(x, \omega_i; \mathbf{G})$，并通过蒙特卡洛采样估计物理渲染积分：

$$I_{\mathbf{G}}^{\mathbf{PBR}}(x, \omega_o) \approx \frac{2\pi}{N_s} \sum_{i=1}^{N_s} f_r(x, \omega_o, \omega_i; \mathbf{G}) \left( V(x, \omega_i; \mathbf{G}) L_{dir}(\omega_i) + L_{ind}(x, \omega_i; \mathbf{G}) \right) (\omega_i \cdot n_x)$$

消融实验证实，将可微光线追踪替换为split-sum近似或预计算间接辐射会明显损害几何、反照率和重光照指标（Table 5）；只有同时采用动态光线追踪和 $\mathcal{L}_{rad}$ 才能达到最佳性能。

**3. 重光照流程**

传统高斯逆渲染方法（如IRGS、SVG-IR）在新光照下通过光线追踪结合split-sum近似重新着色，需要存储入射辐射信息，推理慢且显存占用高。RadioGS提出了一种**微调重光照策略**：在新光照条件下，仅用辐射一致性损失对曲面片辐射进行少量迭代微调（约2分钟），之后可直接通过光栅化渲染。这一策略将渲染时间从光线追踪的38.6 ms（64采样）降至5.9 ms，显存占用从1512 MB降至308 MB（Table 12）。

### 适用边界与局限

**材质覆盖范围**：当前RadioGS主要针对电介质材质建模，其BRDF模型未涵盖各向异性或高反射表面。将辐射一致性框架扩展到复杂BRDF需要进一步工作。

**微调重光照的精度折损**：微调策略在预计算阶段会因几何和材质的估计误差累积，导致渲染质量相比光线追踪版本略有下降（Table 1中Ours* vs Ours的重光照PSNR差异）。在光照条件大幅变化时，微调虽然收敛快，但离实时在线重光照仍有距离。

**计算成本的可扩展性**：渲染成本随入射光线采样数 $N_s$ 线性增加。虽然可通过调整曲面片采样数 $N_g$ 和 $N_s$ 平衡效率，但在极高分辨率或动态场景下仍有挑战。消融实验表明，$N_s$ 增至64后性能饱和，128反而略有下降（Table 8）；$N_g$ 的增加可持续提升重建质量而不影响推理成本（Table 7）。

**训练视点依赖性**：在仅用25%训练视点的极端情况下，RadioGS的间接光照PSNR仅下降-0.17 dB，而无 $\mathcal{L}_{rad}$ 的版本下降-2.21 dB（Table 6），证明辐射一致性对稀疏视点具有强鲁棒性。但这并不意味着该方法可以完全摆脱对多视点覆盖的需求——几何重建质量仍然依赖于足够的视点覆盖。

### 开放问题

1. **复杂材质的辐射一致性**：能否将辐射一致性机制与各向异性BRDF、多层BSDF或高反射材质模型结合，扩展方法的材质适用范围？
2. **多弹射全局光照**：当前方法主要处理单次弹射的间接光照。辐射一致性机制是否可与路径追踪结合，支持多次弹射的全局光照建模？
3. **实时重光照**：微调阶段能否通过模型蒸馏或预计算策略进一步加速，实现秒级甚至帧级的新光照适应？
4. **动态场景扩展**：该方法在动态场景或移动视点下的实时逆渲染和重光照潜力如何？辐射一致性损失在时域上的传播机制尚待探索。



## 原文 PDF

![[paperPDFs/ICLR_2026/Radiometrically_Consistent_Gaussian_Surfels_for_Inverse_Rendering.pdf]]
