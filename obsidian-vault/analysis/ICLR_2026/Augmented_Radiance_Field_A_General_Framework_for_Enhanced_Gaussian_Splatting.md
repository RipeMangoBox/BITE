---
title: "Augmented Radiance Field: A General Framework for Enhanced Gaussian Splatting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Augmented_Radiance_Field_A_General_Framework_for_Enhanced_Gaussian_Splatting_a448d65dd9ee.pdf
project_link: "https://xiaoxinyyx.github.io/augs"
code_link: null
aliases:
- ARF
- ARFGFEGS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入一个受Phong光照模型启发的视角相关不透明度函数，能够控制高斯核的方向性透明性，从而独立建模并叠加多个镜面反射波瓣。
primary_logic: 通过将镜面反射成分建模为视角相关不透明度的叠加高斯核，并利用误差驱动的2D高斯初始化及逆投影策略，在已优化的3DGS场景中自适应插入增强核，实现高质量渲染同时保持参数效率。
claims:
- 在Mip-NeRF 360上，Ours (MCMC, sh=3) 的PSNR达到28.96，优于Zip-NeRF的28.54。
- 在Tanks&Temples上，Ours (MCMC, sh=3) 的PSNR为25.06，优于所有显式和隐式基线。
- 消融实验表明，当增强高斯核占比10%时，渲染质量最优。
- 优化不透明叶的方向和形状能够带来统计显著的渲染质量提升。
---

# Augmented Radiance Field: A General Framework for Enhanced Gaussian Splatting

> [!tip] 核心洞察
> 通过将镜面反射成分建模为视角相关不透明度的叠加高斯核，并利用误差驱动的2D高斯初始化及逆投影策略，在已优化的3DGS场景中自适应插入增强核，实现高质量渲染同时保持参数效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 增强辐射场：提升高斯飞溅的通用框架 |
| 英文题名 | Augmented Radiance Field: A General Framework for Enhanced Gaussian Splatting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IzlaRUHncO) · [Project](https://xiaoxinyyx.github.io/augs) · [paper](https://arxiv.org/abs/2501) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | 增强辐射场 (Augmented Radiance Field) |
| Dataset | Mip-NeRF 360, Tanks&Temples, NeRF Synthetic, Deep Blending |

> [!tip] 效果简介
> - Mip-NeRF 360 上，PSNR 28.96 (Ours MCMC, sh=3) vs 28.54 (Zip-NeRF) (+0.42 dB)；SSIM 0.849 (Ours MCMC, sh=3) vs 0.828 (Zip-NeRF) (+0.021)。
> - Tanks&Temples 上，PSNR 25.06 (Ours MCMC, sh=3) vs 24.79 (DBS) (+0.27 dB)。
> - NeRF Synthetic 上，PSNR 34.35 (Ours MCMC, sh=3) vs 34.64 (DBS) (-0.29 dB)。

## 概要

**问题瓶颈**：3D Gaussian Splatting (3DGS) 在重建复杂真实场景时，其球谐函数 (Spherical Harmonics, SH) 编码难以有效解耦漫反射与镜面反射成分，尤其对于高光表面和视角依赖强烈的材质，渲染质量存在明显短板。单纯提高SH阶数（如从3阶升至4阶）并不能带来实质性的渲染质量提升，反而显著增加内存开销（Table 4）。

**核心方法**：本文提出**增强辐射场 (Augmented Radiance Field)**，一种可无缝嵌入现有3DGS管线的后增强框架。其核心创新在于：受Phong光照模型启发，设计了一种**视角相关不透明度函数**（Eq. 1），使新增的高斯核对不同观察方向呈现差异化的透明性，从而独立建模多个镜面反射波瓣；同时，提出**误差驱动的2D高斯初始化与逆投影策略**，在已优化的3DGS场景中自适应插入增强核，实现高质量渲染与参数效率的平衡。

**方法定位**：该方法属于显式辐射场的后增强范式，可与**3DGS** (Kerbl et al., 2023) 及其改进框架**3DGS-MCMC** (Kheradmand et al., 2024) 灵活结合。区别于**Zip-NeRF** (Barron et al., 2023) 等隐式方法、**DBS** (Liu et al., 2025) 的球形贝塔颜色建模，以及**Spec-Gaussian** (Yang et al., 2024) 等针对高光的专门设计，本文通过不透明叶的视角调制实现了更稳定、灵活的镜面反射重建。

**主要结果**：在Mip-NeRF 360数据集上，Ours (MCMC, sh=3) 达到PSNR 28.96 dB，超越Zip-NeRF的28.54 dB；在Tanks&Temples上达到25.06 dB，优于所有显式与隐式基线（Table 1）。消融实验证实，增强高斯核占比10%时渲染质量最优（Table 2），且优化不透明叶的方向与形状能带来统计显著的增益（Table 3）。值得关注的是，即使仅使用二阶球谐函数 (sh=2)，本方法也能达到与三阶SH相当的性能，同时大幅降低内存占用（Table 1, Table 15）。

**新视角合成**是计算机视觉与图形学中的一项基础任务，其目标是从一组稀疏的输入图像中重建场景的完整三维表示，并能够从任意新视角进行高质量渲染。近年来，以**3D Gaussian Splatting (3DGS)**（Kerbl et al., 2023）为代表的显式辐射场方法，凭借其高保真渲染质量和实时推理速度，已成为该领域的主流范式。3DGS 使用一组各向异性的三维高斯核来表示场景，并通过高效的差分光栅化实现快速渲染。

然而，3DGS 在建模复杂光照效应方面存在根本性局限。其瓶颈在于：**3DGS 中使用的球谐函数 (Spherical Harmonics, SH) 无法有效解耦漫反射与镜面反射成分，且其全局定义导致对复杂反射和视角依赖颜色编码效率低下，尤其对于高光表面。** 具体而言，球谐函数是一种定义在球面上的全局基函数，虽然能够表达低频的视角依赖颜色变化，但在面对高光、镜面反射等高频、局部化的视角依赖效应时，需要极高的阶数才能逼近，这极大地增加了参数量和内存开销。消融实验（Table 4）直接证实了这一点：在 3DGS 中将球谐函数从三阶提升到四阶，渲染质量几乎没有提升（PSNR 仅从 27.47 提升至 27.55），但内存消耗却从 608 MB 急剧膨胀至 887 MB。

这一瓶颈的因果机制在于：**真实世界的表面反射可以分解为漫反射分量（与视角无关或弱相关）和镜面反射分量（强视角依赖，集中在反射方向附近的窄波瓣内）。** 球谐函数作为全局基函数，试图用同一组系数同时编码这两种物理性质迥异的分量，导致其必须“平均地”分配表达能力，对镜面反射波瓣的尖锐峰值建模效率极低。

针对这一问题，现有方法尝试了不同的改进路径。**Spec-Gaussian**（Yang et al., 2024）和 **VoD-3DGS**（Nowak et al., 2025）分别通过引入各向异性球面高斯或视角依赖的不透明度来增强对高光表面的建模，但这些方法本质上仍是对全局颜色表示或全局不透明度的修正，未能从根本上解耦漫反射与镜面反射。**DBS**（Liu et al., 2025）提出了基于球形贝塔函数的颜色建模，通过多个方向性贝塔函数的叠加来逼近视角依赖的出射辐射度，但该方法在数值稳定性和对高斯核排序的敏感性上存在不足（详见 Figure 5 对比分析）。

本文的核心动机源于一个关键的物理洞察：**镜面反射成分天然具有方向性和局部性**——它仅在反射方向附近的狭窄角度范围内显著贡献。这一特性恰好与高斯核在空间上的局部性相呼应。因此，**如果将镜面反射建模为“仅在特定视角范围内可见”的高斯核，就能将漫反射与镜面反射在结构层面解耦**：原始高斯核负责漫反射（使用低阶 SH 即可），而新增的“增强高斯核”专门负责镜面反射，其可见性由视角相关的不透明度函数控制。

基于这一洞察，本文提出**增强辐射场 (Augmented Radiance Field)**——一个通用的后增强框架，能够无缝嵌入现有 3DGS 方法，通过引入受 Phong 光照模型启发的视角相关不透明度函数和误差驱动的自适应高斯核插入策略，在不显著增加参数量的前提下，大幅提升对高光表面和复杂反射场景的渲染质量。

## 核心方法与创新机理

本工作提出**增强辐射场 (Augmented Radiance Field)**，其核心创新在于通过引入**视角相关不透明度函数**，从根本上改变了3DGS对视角依赖外观的建模方式，从而解决了球谐函数在解耦漫反射与镜面反射成分时的固有瓶颈。

### 创新1：视角相关不透明度的增强高斯核

3DGS使用球谐函数 (Spherical Harmonics, SH) 对所有视角依赖的颜色进行统一编码。然而，SH的全局定义特性使其难以有效解耦漫反射与镜面反射成分，尤其在高光表面和复杂反射场景中效率低下。本工作的核心洞察是：镜面反射本质上是一个方向性透明现象——高光仅在特定视角方向可见。

受经典Phong光照模型启发，方法为每个增强高斯核引入一个视角相关的不透明度函数：

$$
\hat{\alpha}(\theta, \beta, T, \alpha) = \alpha \cdot \left( \frac{\cos(\max(0,\min(\theta/T, \pi))) + 1}{2} \right)^{\exp(\beta)}
$$

其中 $\theta$ 是视线方向与不透明叶 (opacity lobe) 朝向的夹角，$T$ 控制角度跨度，$\beta$ 调制波瓣的锐度（Figure 3）。每个增强核仅新增5个可学习参数（叶朝向2自由度、$T$、$\beta$ 和基础不透明度 $\alpha$），即可独立建模一个镜面反射波瓣。

这一设计的关键因果机制在于：**通过将镜面反射建模为多个方向性透明高斯核的叠加，实现了漫反射与镜面反射的隐式解耦**。原始高斯核的SH继续负责漫反射颜色，而增强核通过视角相关不透明度仅在特定方向贡献颜色，从而在不显著增加参数量的前提下，大幅提升了对复杂光照的建模能力。

### 创新2：误差驱动的2D高斯初始化与逆投影策略

传统3DGS的致密化策略基于启发式空间梯度，无法针对性地补充镜面高光区域的图元。本工作提出一种误差驱动的初始化管线：

1. **2D图像空间优化**：在已渲染图像上，根据L1与SSIM混合损失的平方值定义像素级采样概率 $p(u,v) \propto [(1-\lambda_{\mathrm{SSIM}}) \mathcal{L}_1(u,v) + \lambda_{\mathrm{SSIM}} \mathcal{L}_{\mathrm{SSIM}}(u,v)]^2$，在误差大的区域自适应放置2D高斯核，并通过梯度下降优化其参数集 $\{ \mathbf{x}, \alpha, \mathbf{c}, d, r, \mathbf{s} \}_{\mathrm{2D}}$ 以最小化残差。

2. **逆高斯飞溅 (Inverse Gaussian Splatting)**：利用深度图将2D高斯投影回3D世界空间。深度值取光线透射率首次低于0.5的位置。通过加权主成分分析 (WPCA) 确定3D旋转和尺度，并求解最优尺度系数 $k = \sqrt{ \frac{ \Sigma_{ij} Q_{ij} \hat{\Sigma}_{2D_{ij}} }{ ||Q||_F^2 } }$ 以最小化投影协方差与目标协方差的Frobenius范数。

这一策略的关键优势在于：**新核的插入由渲染误差直接驱动，而非空间启发式规则**，从而将计算资源精准投向现有模型难以重建的镜面高光区域。

### 创新3：后增强框架的即插即用设计

方法被设计为对已优化3DGS场景的**后增强 (post-enhancement)** 流程，而非从零开始的替代训练方案。增强核以固定比例（总图元数的10%）替换部分原始高斯核，随后进行联合优化以精修不透明叶参数。这种设计使其可无缝集成到现有高斯飞溅方法（如3DGS和3DGS-MCMC）中，无需修改原始训练管线。

消融实验证实，仅当增强核具备可优化的视角相关不透明度时，才能获得统计显著的渲染质量提升；单纯补充无视角依赖性的高斯核效果不佳（Table 3）。此外，即使仅使用二阶球谐函数（sh=2），方法也能达到与三阶SH相当的性能，同时显著降低内存占用（Table 1, Table 15），进一步验证了视角相关不透明度对SH编码效率的补偿作用。

增强辐射场（Augmented Radiance Field）采用**后增强（post-enhancement）范式**，在已优化的3DGS场景基础上，通过三阶段流水线自适应地插入具备视角相关不透明度的增强高斯核，以恢复原始表示难以捕捉的复杂视角依赖颜色（尤其是镜面高光）。图2概括了该流水线的三个核心模块。

### 模块一：误差驱动的2D高斯图像空间优化

给定已训练的3DGS场景，首先从各训练视角渲染图像并计算残差。基于L1与SSIM损失的混合平方值定义像素级采样概率（Eq. 3），在误差显著区域自适应放置2D高斯图元。每个2D高斯携带参数 $\{ \mathbf{x}, \alpha, \mathbf{c}, d, r, \mathbf{s} \}_{\mathrm{2D}}$（图像坐标、不透明度、颜色、深度、旋转、尺度），通过梯度下降最小化该视角的渲染损失。深度值由3DGS的透射率首次降至0.5处确定，确保几何一致性。

### 模块二：逆高斯飞溅——投影到3D世界空间

优化收敛后，利用深度图将2D高斯反投影至世界空间。该过程包含三步：首先通过点云聚类分离前景与背景；随后使用加权主成分分析（WPCA）确定每个3D高斯核的旋转与尺度；最后通过最小化投影协方差矩阵 $\Sigma_{2D}$ 与目标协方差矩阵 $\hat{\Sigma}_{2D}$ 的Frobenius范数（Eq. 6），求解最优尺度系数 $k$，完成尺度校准。反投影后的高斯核被赋予视角相关不透明度参数：朝向角跨度 $T$ 初始化为 $c \cdot \bar{\theta}_i / \pi$，锐度参数 $\beta$ 初始化为零。

### 模块三：联合优化与视角相关不透明度精修

新增的增强高斯核与原始场景中的高斯图元合并，进行联合优化。增强核的不透明度由视角相关函数 $\hat{\alpha}(\theta, \beta, T, \alpha)$（Eq. 1）控制——该函数受Phong光照模型启发，以余弦加权形式调制高斯核的方向性透明度，其中 $\theta$ 为视线方向与叶朝向的夹角，$T$ 控制角跨度，$\beta$ 调制锐度。每个增强核在标准高斯图元基础上额外引入5个可学习参数。联合优化阶段同时精修不透明叶参数与原始核的不透明度，使场景能解耦漫反射与镜面反射成分。

### 输入输出流

- **输入**：已优化的3DGS场景（含高斯图元参数集与球谐系数）、训练视角图像集。
- **中间产物**：误差驱动的2D高斯优化结果、深度图、反投影后的增强高斯核集。
- **输出**：增强后的辐射场，包含原始高斯核与新增的视角相关不透明度增强核，可渲染出更高质量的视角依赖颜色。

整个流水线作为即插即用的后处理模块，可无缝集成到现有基于高斯飞溅的方法中。增强高斯核数量固定为总图元数的10%，以在渲染质量与内存效率间取得平衡。

### 视角相关不透明度核

本方法的核心创新在于为补充的高斯图元引入一种受经典Phong光照模型启发的视角相关不透明度函数。标准3DGS中的高斯核仅通过全局球谐函数（SH）编码颜色，无法有效解耦漫反射与镜面反射成分。为此，作者定义了一个新的视角相关透明高斯核，其不透明度 $\hat{\alpha}$ 随观察方向与波瓣朝向的夹角 $\theta$ 变化：

$$
\hat{\alpha}(\theta, \beta, T, \alpha) = \alpha \cdot \left( \frac{\cos(\max(0,\min(\theta/T, \pi))) + 1}{2} \right)^{\exp(\beta)}
$$

**变量含义**：
- $\alpha$：基础不透明度，即波瓣峰值处的不透明度
- $\theta$：观察方向与不透明叶中心朝向之间的夹角
- $T$：控制波瓣的角度跨度（角范围）
- $\beta$：调制波瓣的锐度（$\exp(\beta)$ 作为余弦项的指数）

该函数使得高斯核在特定方向上的透明度最高，随角度偏离逐渐降低。每个补充高斯核在默认3DGS配置基础上新增5个可学习参数（不透明叶朝向的3自由度、$T$ 和 $\beta$），从而能够独立建模多个镜面反射波瓣的叠加效果。

### 误差驱动的2D高斯图像空间优化

增强流程的第一步是在已渲染图像上进行2D高斯图元优化。给定一个已优化的3DGS场景，针对每个训练视角渲染图像并计算残差。在像素 $(u,v)$ 处放置新2D高斯核的概率由混合损失驱动：

$$
p(u,v) \propto \left[ (1-\lambda_{\mathrm{SSIM}}) \mathcal{L}_1(u,v) + \lambda_{\mathrm{SSIM}} \mathcal{L}_{\mathrm{SSIM}}(u,v) \right]^2
$$

每个2D高斯图元由参数集 $\{ \mathbf{x}, \alpha, \mathbf{c}, d, r, \mathbf{s} \}_{\mathrm{2D}}$ 定义：
- $\mathbf{x}$：图像空间坐标
- $\alpha$：不透明度
- $\mathbf{c}$：颜色
- $d$：深度（通过光线追踪方式从3D高斯获取，取透射率首次降至0.5以下的深度值）
- $r$：旋转
- $\mathbf{s}$：尺度

通过最小化渲染损失对这些2D高斯进行优化，使其自适应地填补原场景中渲染误差较大的区域。

### 逆高斯飞溅：2D到3D的投影

将优化后的2D高斯投影到世界空间的过程包含三个关键步骤：

1. **前景-背景分离与聚类**：利用深度图进行点云聚类，区分前景与背景区域。
2. **旋转与尺度确定**：通过加权主成分分析（WPCA）确定3D高斯的旋转和尺度。
3. **尺度校准**：最小化投影后的2D协方差矩阵 $\Sigma_{2D}$ 与目标2D协方差矩阵 $\hat{\Sigma}_{2D}$ 之间的Frobenius范数差异。

投影到NDC空间的2D协方差矩阵为：

$$
\Sigma_{2D} = J W R S (J W R S)^T
$$

其中 $J$ 为投影变换的雅可比，$W$ 为视图变换，$R$ 为旋转矩阵，$S$ 为尺度矩阵。尺度校准通过求解最优尺度系数 $k$ 完成：

$$
k = \sqrt{ \frac{ \Sigma_{ij} Q_{ij} \hat{\Sigma}_{2D_{ij}} }{ ||Q||_F^2 } }
$$

### 初始化策略

新增高斯核的参数初始化遵循以下规则：
- $T$ 初始化为 $c \cdot \bar{\theta}_i / \pi$，其中 $\bar{\theta}_i$ 为最小角度
- $\beta$ 采用零初始化
- 不透明叶朝向从2D高斯的局部几何信息推导

投影完成后，新增的增强高斯核与原始高斯核一同进入联合优化阶段，精修不透明叶参数以及原始核的不透明度，最终实现高质量渲染。

## 实验与关键发现

### 主要定量结果

Table 1 汇总了在 Mip-NeRF 360、Tanks&Temples、Deep Blending 和 NeRF Synthetic 四个基准上的全面对比。在 MCMC 框架下，本方法（Ours, MCMC, sh=3）在真实世界数据集上取得了最优渲染质量：

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IzlaRUHncO/figures/004_Table_1.jpg]]
*Table 1: Qualitative comparison across Mip-NeRF 360, Tanks&Temples, Deep Blending, and NeRF Synthetic. All scores for the baseline methods are directly taken from their papers, when available. Note that we use the VoD-3DGS variant with higher memory consumption and the anchor-free Spec-Gaussian, as recommended by the authors; for DBS, we adopted the data stopping at 30k iterations for fairness. Our method consistently outperforms state-of-the-art explicit and implicit approaches under the MCMC framework, whether utilizing second- or third-order spherical harmonics*

- **Mip-NeRF 360**：PSNR 达到 28.96，超出此前最优隐式方法 **Zip-NeRF**（Barron et al., 2023）的 28.54 约 0.42 dB；SSIM 为 0.849，领先 Zip-NeRF 的 0.828。这表明增强高斯核对复杂视角依赖颜色的建模能力显著优于纯球谐函数方案。
- **Tanks&Temples**：PSNR 为 25.06，优于所有显式和隐式基线，包括基于球形贝塔的 **DBS**（Liu et al., 2025，24.79）和 **3DGS-MCMC**（Kheradmand et al., 2024，24.59）。
- **Deep Blending**：PSNR 达到 30.22，较 3DGS-MCMC 的 29.67 提升 0.55 dB，证明后增强策略在稀疏视角场景下同样有效。
- **NeRF Synthetic**：PSNR 为 34.35，略低于 DBS 的 34.64（-0.29 dB）。该数据集以漫反射材质为主，镜面反射成分有限，增强核的优势未能充分体现；但本方法仍与最优显式方法保持竞争力。

值得注意的是，即便仅使用二阶球谐函数（sh=2），本方法在 Mip-NeRF 360 上仍达到 28.80 PSNR，与三阶 SH 性能接近，同时显著降低内存占用（Table 15），验证了视角相关不透明度对 SH 编码效率的补偿效应。

### 消融实验

**增强高斯核占比**（Table 2）：在总图元数保持不变的前提下，增强高斯核占比为 10% 时取得最优渲染质量。占比过低（5%）无法充分覆盖镜面反射区域，占比过高（20%）则挤占了原始高斯核的表达空间，导致漫反射区域质量下降。

**不透明叶组件的贡献**（Table 3）：完整优化不透明叶的方向和形状参数，相比仅增加无视角依赖性的高斯核，在 Mip-NeRF 360 上带来统计显著的 PSNR 提升。移除不透明叶优化后，方法退化为简单的空间致密化，无法有效建模高光表面的视角变化。

**球谐函数阶数**（Table 4）：在 3DGS 中将 SH 从三阶提升至四阶，渲染质量几乎无提升，却显著增加了内存消耗。这从反面印证了本工作的核心洞察：单纯提高 SH 阶数无法有效解耦漫反射与镜面反射成分，而视角相关不透明度提供了更参数高效的替代方案。

**高光场景对比**（Table 5）：在合成的高光数据集上，本方法优于使用球形贝塔（Spherical Beta）建模颜色的 DBS。Figure 5 揭示了机理差异：球形贝塔函数对高斯核的叠加顺序敏感，且数值稳定性较差；而本方法的不透明叶通过独立的透明度调制，能更稳定地重建出射辐射度。

### 效率分析

Table 6 和 Table 7 报告了后增强阶段的时间开销和整体资源消耗。2D 高斯优化阶段可在多 GPU 上并行处理（每张图像独立训练），显著加速整体流程。在 Mip-NeRF 360 上，总训练时间（原始重建 + 后增强）约为 3DGS-MCMC 的 1.5 倍，但渲染 FPS 保持在实时水平。内存方面，增强核仅增加约 10% 的参数量，且使用 sh=2 时可进一步压缩内存占用。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IzlaRUHncO/figures/009_Table_6.jpg]]
*Table 6: The time consumption for the post-enhancement stage on the Mip-NeRF 360 and NeRF Synthetic datasets is reported as follows. It should be noted that using multiple GPUs can significantly accelerate this process, as the 2D-stage training operates independently on each image*

### 失败模式与局限性

1. **深度图精度不足**：反投影 2D 高斯到世界空间依赖训练视角的深度图，但本工作未使用几何约束或深度网络生成精细深度图，导致投影后的高斯核未能精确贴合物体表面。这在几何结构复杂的区域（如细薄结构、深度不连续边界）可能引入伪影。
2. **固定增强比例**：增强高斯核占比固定为 10%，在主要为漫反射材质的场景（如 NeRF Synthetic 的部分场景）中可能引入冗余参数，甚至略微降低质量。
3. **两阶段训练开销**：后增强策略延长了场景重建总时间，且 2D 阶段与 3D 联合优化阶段分离，未能实现端到端训练。

### 场景级分析

Table 8 和 Table 11 提供了 Mip-NeRF 360 上逐场景的渲染质量及增强前后的增量指标。在包含大量镜面反射的场景（如 `counter`、`kitchen`）中，增强带来的 PSNR 提升最为显著（>1 dB）；而在以漫反射为主的室外场景（如 `stump`）中，提升幅度较小。Table 9 和 Table 10 分别给出了 Tanks&Temples、Deep Blending 和 NeRF Synthetic 的逐场景详细结果。

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IzlaRUHncO/figures/013_Table_8.jpg]]
*Table 8: Quantitative results of rendering quality per scene on Mip-NeRF 360 dataset*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IzlaRUHncO/figures/018_Table_9.jpg]]
*Table 9: Quantitative results of rendering quality per scene on Tanks and Temples and Deep Blending dataset*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IzlaRUHncO/figures/019_Table_10.jpg]]
*Table 10: Quantitative results of rendering quality per scene on NeRF synthetic dataset*

![[assets/figures/papers/paper_list_l29_https_openreview_net_forum_id_IzlaRUHncO/figures/007_Table_3.jpg]]
*Table 3: Ablation study on Mip-NeRF 360 dataset. Optimizing the orientation and shape of the opacity lobe achieves render quality unattainable by solely supplementing with Gaussians without view-dependent opacity*

## 定位与知识库关联

### 1. 在显式辐射场演进中的坐标

**增强辐射场**（Augmented Radiance Field）处于3D高斯飞溅（3D Gaussian Splatting）范式的后增强分支，其核心设计动机源于对**3DGS**（Kerbl et al., 2023）中球谐函数（Spherical Harmonics, SH）颜色编码瓶颈的系统性诊断：SH的全局定义使其无法有效解耦漫反射与镜面反射成分，对高光表面和复杂视角依赖颜色的编码效率低下。本工作并非推翻3DGS框架，而是提出一个即插即用的后处理增强模块，可在已优化的3DGS场景上叠加视角相关不透明度的高斯核来建模镜面反射波瓣。

从方法谱系来看，该工作与以下几条演进脉络直接对话：

- **3DGS的致密化与初始化改进线**：**3DGS-MCMC**（Kheradmand et al., 2024）通过马尔可夫链蒙特卡洛采样改进高斯图元的分布策略，本工作选择以其为默认骨架框架，并在此基础上引入误差驱动的2D高斯采样与逆投影致密化，替代原始3DGS的启发式空间致密化。

- **视角依赖外观建模线**：**VoD-3DGS**（Nowak et al., 2025）直接在高斯图元上建模视角依赖效应，**Spec-Gaussian**（Yang et al., 2024）针对高光场景优化高斯表示。本工作与之不同的是，将视角依赖性限定在新增加的增强高斯核的不透明度上，而非修改所有图元的颜色编码，从而在保持原始场景结构完整性的同时精准追加镜面反射建模能力。

- **球形函数颜色建模线**：**DBS**（Liu et al., 2025）使用球形贝塔（Spherical Beta）函数替代SH来建模各向异性反射。本工作通过Figure 5的系统对比揭示了球形贝塔方法的一个关键缺陷：当多个高斯核叠加时，其渲染结果对核的排列顺序敏感，且数值稳定性不足。视角相关不透明度函数通过将镜面反射建模为透明度的方向性调制而非颜色的方向性加权，规避了这一问题。

- **隐式NeRF基线**：在渲染质量上，本工作直接对标**Zip-NeRF**（Barron et al., 2023）和**Mip-NeRF 360**（Barron et al., 2021），在Mip-NeRF 360数据集上以28.96 PSNR超越Zip-NeRF的28.54，标志着显式方法在该基准上首次系统性超越最新隐式方法。

### 2. 核心因果机制：从Phong光照模型到视角相关不透明度

本工作的核心因果旋钮（causal knob）是将经典Phong光照模型中的镜面反射波瓣概念迁移到高斯图元的不透明度域。具体而言，每个增强高斯核在标准3DGS参数基础上新增5个可学习参数，定义视角相关不透明度函数：

$$
\hat{\alpha}(\theta, \beta, T, \alpha) = \alpha \cdot \left( \frac{\cos(\max(0,\min(\theta/T, \pi))) + 1}{2} \right)^{\exp(\beta)}
$$

其中 $\theta$ 是视线方向与不透明叶朝向的夹角，$T$ 控制波瓣的角跨度，$\beta$ 调制波瓣的锐度（Figure 3）。这一设计的洞察在于：镜面高光本质上是特定观察角度下表面反射率的急剧增强，用不透明度的角度选择性来建模，比用SH系数去拟合这种尖锐的角度变化更为参数高效。消融实验（Table 3）证实，完全优化不透明叶的朝向和形状带来的渲染质量提升，是仅添加无视角依赖性的高斯核所无法企及的。

### 3. 适用边界与失效模式

**适用场景**：
- 包含显著镜面反射和高光表面的真实捕获场景（Mip-NeRF 360、Tanks&Temples数据集上的增益最为显著）
- 需要在保持参数效率的前提下提升3DGS渲染质量的场景——即使仅使用二阶SH（sh=2），本方法也能达到与三阶SH相当的性能，且内存占用显著降低（Table 15）
- 作为已训练3DGS场景的后增强模块，无需重新训练原始场景

**失效模式与局限**：
1. **逆投影的几何精度不足**：2D高斯反投影到世界空间的过程依赖训练视角的深度图，但本工作未使用几何约束或深度网络来生成精细深度图，导致投影后的增强高斯核未能精确贴合物体表面。这在高频几何细节区域可能导致伪影。
2. **两阶段策略的时间开销**：后增强阶段引入了额外的训练时间（Table 6），尽管多GPU可并行加速2D阶段训练，但总体重建时间仍长于单阶段方法。
3. **增强核数量固定**：当前方案将增强高斯核占比固定为10%（Table 2验证了该比例的最优性），但在主要为漫反射材质的场景中可能引入冗余图元，在极端镜面反射场景中可能不足。
4. **NeRF Synthetic数据集上的表现**：在该合成数据集上，本方法（PSNR 34.35）略低于DBS（34.64），表明在受控合成光照条件下，球形贝塔方法的颜色建模优势仍存。

### 4. 开放问题与未来方向

1. **自适应增强核数量**：如何根据场景的镜面反射复杂度自适应决定需新增的增强高斯核数量，而非固定10%的比例，是提升参数效率的直接方向。
2. **端到端联合训练**：当前的两阶段策略（先训练原始3DGS，再后增强）可融合为端到端的联合优化过程，将2D高斯初始化嵌入原始场景训练循环，以减少总重建时间。
3. **深度几何约束**：引入单目深度估计网络或多视图立体几何约束来改善逆投影的几何精度，有望进一步提升增强核的定位准确性。
4. **动态场景扩展**：视角相关不透明度函数在动态场景中的镜面反射时变建模潜力尚未探索。

### 5. 知识库定位

本工作在方法论层面建立了**“不透明度域视角依赖性建模”**这一新的设计维度，区别于现有的颜色域视角依赖性建模（SH、球形贝塔等）和几何域视角依赖性建模（如反射方程显式求解）。其核心贡献在于证明：对于镜面反射这一特定外观现象，在透明度而非颜色通道上建模角度选择性，可以获得更好的参数效率、数值稳定性和渲染质量。这一洞察可泛化至其他需要建模方向性外观现象的显式辐射场方法中。

## 原文 PDF

![[paperPDFs/ICLR_2026/Augmented_Radiance_Field_A_General_Framework_for_Enhanced_Gaussian_Splatting_a448d65dd9ee.pdf]]
