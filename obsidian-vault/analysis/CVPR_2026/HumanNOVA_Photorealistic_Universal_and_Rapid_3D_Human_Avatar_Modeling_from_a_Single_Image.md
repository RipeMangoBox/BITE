---
title: "HumanNOVA: Photorealistic, Universal and Rapid 3D Human Avatar Modeling from a Single Image"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/HumanNOVA_Photorealistic_Universal_and_Rapid_3D_Human_Avatar_Modeling_from_a_Single_Image.pdf
project_link: "https://HumanNOVA.github.io"
code_link: null
aliases:
- HumanNOVA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 论文的核心杠杆在于（1）设计了一套可扩展的数据生成管线，通过合成动画和真实多视图拟合将训练资产规模扩大20倍至10万，以及（2）将预估计的简化人体网格（SMPL）作为额外先验，通过交叉注意力融入基于Transformer的前馈三平面重建框架，从而实现快速、通用且高质量的三维人体重建。
primary_logic: 将大规模数据生成与类别特定先验（SMPL网格）相结合，使得通用重建模型（LRM）能够以单次前向传播实现高保真度、快速且通用的三维人体重建，无需测试时优化，从而打破通用物体重建模型与专用人体重建方法的边界。
claims:
- HumanNOVA在三个基准（CustomHuman、THuman2、2K2K）上相对于最强基线SiTH分别实现了41.8%、37.0%和43.3%的相对LPIPS提升。
- 引入网格先验使得LPIPS相对提升2.3%，证明即使在大规模数据下，人体结构先验仍能提供关键细节。
- 将我们的生成数据用于微调Real3D，其在CustomHuman上的PSNR从17.13提升到20.97，验证了数据的有效性和可迁移性。
- CustomHuman 上 LPIPS = 42.42
---

# HumanNOVA: Photorealistic, Universal and Rapid 3D Human Avatar Modeling from a Single Image

> [!tip] 核心洞察
> 将大规模数据生成与类别特定先验（SMPL网格）相结合，使得通用重建模型（LRM）能够以单次前向传播实现高保真度、快速且通用的三维人体重建，无需测试时优化，从而打破通用物体重建模型与专用人体重建方法的边界。

| 字段 | 内容 |
|------|------|
| 中文题名 | HumanNOVA：从单张图像生成逼真、通用且快速的三维人体化身模型 |
| 英文题名 | HumanNOVA: Photorealistic, Universal and Rapid 3D Human Avatar Modeling from a Single Image |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Hu_HumanNOVA_Photorealistic_Universal_and_Rapid_3D_Human_Avatar_Modeling_from_CVPR_2026_paper.html) · [Project](https://HumanNOVA.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HumanNOVA |
| Dataset | CustomHuman, THuman2, 2K2K |

> [!tip] 效果简介
> - CustomHuman 上，LPIPS 42.42 vs 72.94 (-41.8% (相对))。
> - THuman2 上，LPIPS 42.13 vs 66.90 (-37.0% (相对))。
> - 2K2K 上，LPIPS 41.72 vs 73.55 (-43.3% (相对))。

## 概要

从单张二维图像重建逼真的三维人体化身，是数字人、虚拟现实与视觉内容创作等领域的核心需求。然而，现有方法面临两大瓶颈：其一，高质量、多样化的三维人体训练数据严重不足，导致前馈重建模型的泛化能力受限；其二，通用物体重建模型（如基于LRM的方法）未能有效利用人体结构先验，重建质量不佳，而专用人体重建方法又往往依赖耗时的测试时优化或扩散先验，推理速度过慢，难以实用。

针对上述问题，**HumanNOVA** 提出了一条“大规模数据生成 + 类别特定先验融入前馈框架”的技术路线，核心洞察在于：**将可扩展的数据生成管线与人体结构先验（SMPL简化网格）相结合，使得通用重建模型能够以单次前向传播实现高保真度、快速且通用的人体三维重建，无需任何测试时优化，从而打破了通用物体重建与专用人体重建方法之间的边界。**

具体而言，HumanNOVA 的核心杠杆体现在两个层面：
- **数据层面**：设计了一套可扩展的数据生成管线，通过合成资产动画（利用AMASS动作序列驱动已绑定的三维人体资产）与真实多摄像头数据拟合（基于3D Gaussian Splatting），将训练资产规模从约5千扩展至10万，扩大了20倍。
- **模型层面**：采用基于PointInfinity的Transformer架构，将预估计的SMPL简化网格作为额外先验，通过双向交叉注意力与输入图像特征融合，共同条件化三平面令牌的生成，从而在保持快速推理（小于1秒）的同时，显著提升重建的几何与外观精度。

实验结果表明，HumanNOVA 在三个基准数据集上取得了显著优势：相较于此前最强的专用方法 **SiTH**（Ho et al., CVPR 2024），在 CustomHuman、THuman2 和 2K2K 上分别实现了 **41.8%、37.0% 和 43.3% 的相对 LPIPS 提升**。消融实验进一步验证了合成数据与真实数据均贡献显著（Table 1），数据规模与性能呈正相关（Table 2），而网格先验的引入即使在大规模数据下仍能带来2.3%的相对LPIPS增益（Table 3）。此外，将HumanNOVA的生成数据用于微调通用模型 **Real3D**（Jiang et al., ICCV 2025），可使其PSNR提升3–4 dB（Table 4），证明了数据的有效性与可迁移性。

HumanNOVA 的主要局限在于对遮挡区域和挑战性服装（如连衣裙、背带裤）背面的纹理推断仍存在困难（Figure 4），未来工作可进一步探索遮挡处理与人物-物体交互场景的扩展。

### 问题背景

从单张二维图像重建逼真的三维人体化身是计算机视觉与图形学中长期存在的挑战，在虚拟现实、增强现实、数字人交互等领域具有广泛的应用前景。近年来，基于扩散先验的方法和通用三维重建模型（Large Reconstruction Models, LRMs）取得了显著进展，但要将这些技术推向实际部署，仍面临两个相互关联的关键瓶颈。

**瓶颈一：高质量三维人体训练数据的严重匮乏。** 现有公开的三维人体扫描数据集规模极为有限，通常仅包含约5000个资产。这一数据瓶颈直接限制了前馈重建模型的泛化能力——模型在训练中见到的服装款式、体型、姿态多样性不足，导致在真实世界输入上的重建质量大幅下降。相比之下，二维图像生成领域受益于数十亿级别的训练样本，其泛化能力远超三维领域，这反衬出三维人体数据扩展的迫切性。

**瓶颈二：通用重建模型与人体专用方法的割裂。** 一方面，以 **Real3D**（Jiang et al., ICCV 2025）、**SF3D**（Boss et al., CVPR 2025）为代表的通用LRM方法虽然推理速度快（秒级），但未有效利用人体结构先验，导致重建的人体在几何完整性和纹理保真度上表现不佳。另一方面，以 **PaMIR**（Zheng et al., TPAMI 2021）、**SiFU**（Zhang et al., CVPR 2024）、**SiTH**（Ho et al., CVPR 2024）为代表的专用人体重建方法虽然借助人体参数化模型获得了更好的结构约束，但普遍依赖扩散先验和测试时优化，推理时间长达数分钟甚至小时级，难以满足实时应用需求。

### 现有方法缺口

上述瓶颈导致了当前方法在两个维度上的系统性折衷：

- **速度与质量的折衷**：扩散+优化的专用方法质量相对较好但速度过慢；通用LRM方法速度快但缺乏人体专属设计，重建细节不足。没有方法能在亚秒级推理的同时实现高保真度的人体重建。
- **泛化性与专用性的折衷**：通用模型在各类物体上均可工作，但对人体这一特殊类别的结构特性利用不足；专用模型虽利用了人体先验，但往往依赖特定数据分布，对服装、姿态的泛化能力受限。

此外，即使是当前最强基线 **SiTH**，在 CustomHuman、THuman2、2K2K 等基准上的 LPIPS 指标仍高达 66–73（数值越低越好），这表明重建结果与真实图像之间存在显著的感知差距，尤其在服装纹理、面部细节等区域。

### 本文动机

面对上述缺口，本文的核心洞察是：**将大规模数据生成与类别特定先验（SMPL网格）相结合，可以使通用重建模型以单次前向传播实现高保真度、快速且通用的三维人体重建，从而打破通用物体重建模型与专用人体重建方法的边界。**

具体而言，本文提出 **HumanNOVA**，其动机源于两个关键杠杆：

1. **可扩展的数据生成管线**：通过合成动画（利用AMASS动作捕捉数据驱动资产动画）和真实多视图拟合（基于3D Gaussian Splatting从多摄像头数据重建），将训练资产规模扩大20倍至约10万个，从根本上缓解数据匮乏问题。
2. **人体结构先验的有效注入**：始终将预估计的简化人体网格（SMPL）作为额外条件输入，通过交叉注意力机制融入基于Transformer的前馈三平面重建框架，使模型在拥有大规模数据的同时仍能从人体结构先验中获益，无需任何测试时优化即可在不到1秒内完成重建。

这一设计旨在实现“鱼与熊掌兼得”：既保留通用LRM的快速前馈推理能力，又获得专用人体方法的结构保真度，最终在多个基准上相对最强基线实现超过40%的LPIPS相对提升。

## 核心方法与创新机理

HumanNOVA 的核心创新在于将**大规模数据生成**与**类别特定结构先验**相结合，使通用前馈重建框架（LRM）能够以单次前向传播实现高保真、快速且通用的人体三维重建，从而打破通用物体重建模型与专用人体重建方法之间的边界。

### 关键改进维度

#### 1. 训练数据规模：从数千到十万的跨越

现有单视图人体重建方法依赖公开的三维人体扫描数据集，资产总量仅约 5000 个，严重限制了前馈模型的泛化能力。HumanNOVA 设计了一套可扩展的数据生成管线，将训练资产规模扩大 **20 倍至 100k**：

- **合成动画数据**：从 AMASS 数据集中采样 SMPL-X 姿态参数，驱动已绑定的角色资产进行动画化，再围绕重新居中后的对象设置多相机视角进行渲染（见 Eq. (7)），生成大规模、多样化的合成训练样本。
- **真实多视图拟合数据**：基于 3D Gaussian Splatting（3DGS）对多摄像头捕捉的真实数据进行光度拟合（见 Eq. (8)–(9)），生成可任意新视角渲染的高质量真实数据。

消融实验（Table 1）表明，合成数据与真实数据均贡献显著，单独使用任一部分均会导致 PSNR 下降约 0.23–0.31。数据规模与性能呈正相关：仅使用 25% 生成数据时 LPIPS 为 50.14，全量数据时降至 45.18（Table 2）。此外，将 HumanNOVA 的生成数据用于微调通用模型 **Real3D**（Jiang et al., ICCV 2025），使其在 CustomHuman 上的 PSNR 从 17.13 提升至 20.97（Table 4），验证了数据的有效性和可迁移性。

#### 2. 人体结构先验：SMPL 网格作为显式条件

通用物体重建模型（如 Real3D、SF3D）未利用人体结构先验，导致重建质量不佳；专用人体方法（如 PaMIR、SiTH）则依赖耗时的测试时优化。HumanNOVA 始终将预估计的简化人体网格（SMPL）作为额外输入，通过交叉注意力机制与图像特征深度融合：

- 使用 DINOv2 编码输入图像，使用 PTv3 编码估计的 SMPL 网格，生成特征 token。
- 在基于 PointInfinity 的 Transformer 模块中，通过双向交叉注意力将图像 token 和网格 token 融合并更新可学习的三平面 token（见 Eq. (1)–(3)），实现 2D 到 3D 的映射。

消融实验（Table 3）显示，移除网格先验后 LPIPS 从 45.18 升至 46.26，相对恶化 **2.3%**，证明即使在大规模数据下，人体结构先验仍能提供关键的细节补充。

#### 3. 推理速度：从小时级到亚秒级

依赖扩散先验的方法（如 SiTH）需要小时级的推理时间，难以实用。HumanNOVA 采用纯前馈设计，单次前向传播即可完成重建，推理时间**小于 1 秒**，同时无需任何测试时优化或微调，实现了速度与质量的双重突破。

#### 4. 模型容量保障

HumanNOVA 使用三平面空间尺寸为 96 的表示（通用 LRM 通常设为 32）。Table 3 显示，将三平面尺寸降至 32 时 LPIPS 恶化至 48.33，表明充足的模型容量对细节重建至关重要。

### 创新总结

| 改进维度 | 基线状况 | HumanNOVA 方案 | 证据强度 |
|---------|---------|---------------|---------|
| 训练数据规模 | ~5k 资产 | 100k 资产（合成+真实） | 强（Table 1, 2, 4） |
| 人体先验 | 无或需测试时优化 | SMPL 网格交叉注意力融合 | 强（Table 3） |
| 网络架构 | 通用 LRM 或扩散+优化 | Transformer 双向交叉注意力 | 中强（Section 3.1） |
| 推理速度 | 小时级或秒级 | <1 秒单次前馈 | 强（Abstract） |

这一组合创新使 HumanNOVA 在三个基准（CustomHuman、THuman2、2K2K）上相对于最强基线 **SiTH**（Ho et al., CVPR 2024）分别实现了 **41.8%、37.0% 和 43.3%** 的相对 LPIPS 提升（Table 5），同时保持了通用性——无需针对不同个体进行测试时适应。

HumanNOVA 采用前馈式、令牌条件化的化身建模框架，在单次前向传播中完成三维人体重建，推理时间小于一秒，无需任何测试时优化。其整体流程可概括为：**输入图像与预估计的简化人体网格 → 多模态编码 → 2D‑到‑3D 映射 → 三平面渲染**。

### 输入与预处理

给定一张真实世界的人物图像，系统首先利用现成的 SMPL‑X 估计器预测对应的简化人体网格 **M**(β, θ, ψ)。该网格仅提供粗糙的姿态与形状先验，不包含任何细节几何或外观信息（如服装褶皱、纹理）。图像与网格构成框架的双模态输入。

### 多模态编码器

图像和网格分别由两个专用编码器处理：
- **图像分支**：采用 DINOv2 提取视觉特征，生成一组图像令牌 **fᵢ**。
- **网格分支**：使用 PTv3 对估计的 SMPL 网格进行编码，生成网格令牌 **fₘ**。

两组令牌在特征维度上对齐后，共同作为后续映射网络的条件信号。

### 2D‑到‑3D 映射网络

映射网络的核心是一个基于 PointInfinity 的 Transformer 架构，其目标是学习从二维条件令牌到三维三平面表示的映射。网络维护一组可学习的**三平面令牌** **T**^l，并通过双向交叉注意力机制逐步融合多模态条件信息。具体而言，每一层执行以下三个步骤：

1. **条件注入**：将图像令牌与网格令牌拼接后作为查询（Query），与当前三平面令牌进行交叉注意力，得到融合特征 **L**^l：
   $$
   \mathbf{L}^{l} = \operatorname{CrossAttn}(\mathbf{Q} = \mathbf{f_i} \parallel \mathbf{f_m},\ \mathbf{KV} = \mathbf{T}^{l})
   $$

2. **特征增强**：以上一步得到的融合特征为查询，再次与原始图像和网格令牌交互，增强条件信号的表示能力：
   $$
   \mathbf{L}^{l} = \operatorname{CrossAttn}(\mathbf{Q} = \mathbf{L}^{l},\ \mathbf{KV} = \mathbf{f_i} \parallel \mathbf{f_m})
   $$

3. **三平面更新**：以当前三平面令牌为查询，与增强后的特征进行交叉注意力，更新三平面表示：
   $$
   \mathbf{T}^{l+1} = \operatorname{CrossAttn}(\mathbf{Q} = \mathbf{T}^{l},\ \mathbf{KV} = \mathbf{L}^{l})
   $$

经过多层迭代后，三平面令牌被重塑为显式的三平面表示，编码了人体的三维几何与外观信息。消融实验表明，将三平面空间尺寸从通用 LRM 常用的 32 提升至 96 对细节重建至关重要——若缩减至 32，LPIPS 将从 45.18 显著恶化至 48.33（Table 3）。

### 渲染与训练目标

从三平面表示出发，框架采用光线行进法（ray marching）渲染任意给定相机视角下的二维图像。训练时，联合损失函数对 N 个渲染视图求平均，同时优化外观与形状：
$$
\mathcal{L} = \frac{1}{N} \sum_{n=1}^{N} \left( \mathcal{L}_{r}^{n} + \lambda_{m} \mathcal{L}_{m}^{n} + \lambda_{p} \mathcal{L}_{p}^{n} \right)
$$
其中 L_r 为 RGB 损失，L_m 为掩码损失，L_p 为 LPIPS 感知损失。

### 数据生成管线

支撑上述框架的关键是论文提出的大规模数据生成管线，将训练资产从约 5000 个扩展至 10 万个（20 倍），包含两条互补路径：

- **合成动画数据**：从 AMASS 数据集中随机采样 SMPL‑X 姿态参数，驱动已绑定的资产角色进行动画，再经重新居中后在预设的规范视角下渲染多视图图像。
- **真实多视图拟合数据**：基于 3D Gaussian Splatting（3DGS）对多摄像头捕获的真实数据进行光度拟合，最小化捕获图像与可微渲染图像之间的 L2 损失：
  $$
  \mathcal{L} = \left\| I_i - f(V(\theta), \pi_i) \right\|^2
  $$
  拟合后的 3DGS 表示可渲染任意新视角图像，作为训练数据源。

消融实验证实两条数据路径缺一不可：单独使用任一部分均会导致 PSNR 下降约 0.23–0.31（Table 1），且性能与数据规模呈正相关——仅用 25% 生成数据时 LPIPS 为 50.14，全量数据时为 45.18（Table 2）。更关键的是，该生成数据具备可迁移性：将其用于微调通用 LRM 模型 **Real3D**（Jiang et al., ICCV 2025），在 CustomHuman 上 PSNR 从 17.13 提升至 20.97（Table 4），验证了数据本身的有效性。

### 网格先验的角色

即使在大规模数据训练下，人体结构先验仍能提供关键增益。移除网格先验（即仅使用图像令牌作为条件）后，LPIPS 从 45.18 上升至 46.26，相对恶化 2.3%（Table 3）。这表明将 SMPL 网格作为额外条件信号，通过交叉注意力融入 Transformer，能够引导模型更好地捕捉人体结构约束，从而提升重建精度。

![[assets/figures/papers/paper_list_l1027_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_HumanNOVA_Photoreal/figures/001_Figure_1.jpg]]
*Figure 1: Photorealistic, universal and rapid 3D human avatar modeling from a single image by the proposed approach, HumanNOVA. It benefits from both our generated large-scale data and feed-forward model design. Our data generation pipeline expands training data by 20 times (top-left for visualization). With this data, HumanNOVA achieves superior performance while maintaining rapid inference among existing methods (top-right). Once trained, it is universal without the need for test-time fine-tuning or adaptation. Qualitative results show that HumanNOVA produces more precise photorealistic reconstructions compared to the state-of-the-art SiTH method [19] (bottom)*

HumanNOVA 的前馈重建框架由三个核心模块串联构成：多模态编码、2D到3D映射网络、以及三平面渲染。其设计目标是将单张RGB图像与一个仅含粗略姿态/形状的简化人体网格（通过现成SMPL估计器获得）作为输入，在单次前向传播中直接输出目标视角的逼真渲染结果。

**多模态编码器。** 输入图像由冻结的 DINOv2 编码，估计的 SMPL 网格由 PTv3 编码，分别生成图像特征 token 与网格特征 token。这两种模态的 token 共同作为后续映射网络的条件信号。

**2D到3D映射网络。** 这是整个框架的因果核心。该模块基于 PointInfinity 的 Transformer 架构，维护一组可学习的三平面 token $\mathbf{T}^l$（初始化为可训练参数），并通过双向交叉注意力逐步将 2D 条件特征注入 3D 表示空间。具体而言，每一层 $l$ 执行三个连续的交叉注意力操作：

1. **多模态条件融合**——将图像特征 $\mathbf{f_i}$ 与网格特征 $\mathbf{f_m}$ 沿序列维度拼接后作为查询（Query），以当前三平面 token $\mathbf{T}^l$ 作为键值（Key-Value），使三平面信息回流至条件表示：
   $$\mathbf{L}^l = \operatorname{CrossAttn}(\mathbf{Q} = \mathbf{f_i} \,||\, \mathbf{f_m},\; \mathbf{KV} = \mathbf{T}^l)$$

2. **条件特征增强**——以融合后的特征 $\mathbf{L}^l$ 作为查询，重新与原始的图像-网格拼接特征进行交叉注意力，强化条件信号本身的表征能力：
   $$\mathbf{L}^l = \operatorname{CrossAttn}(\mathbf{Q} = \mathbf{L}^l,\; \mathbf{KV} = \mathbf{f_i} \,||\, \mathbf{f_m})$$

3. **三平面令牌更新**——以当前三平面 token $\mathbf{T}^l$ 为查询，以增强后的条件特征 $\mathbf{L}^l$ 为键值，完成 2D 条件到 3D 表示的映射更新：
   $$\mathbf{T}^{l+1} = \operatorname{CrossAttn}(\mathbf{Q} = \mathbf{T}^l,\; \mathbf{KV} = \mathbf{L}^l)$$

经过若干层迭代后，输出的三平面 token 被重塑为显式的三平面表示。

**渲染与训练目标。** 给定目标相机视角，从三平面表示通过光线行进法直接渲染 2D 图像。训练时对 $N$ 个渲染视图联合优化外观与形状，损失函数为：
$$\mathcal{L} = \frac{1}{N} \sum_{n=1}^{N} \left( \mathcal{L}_r^n + \lambda_m \mathcal{L}_m^n + \lambda_p \mathcal{L}_p^n \right)$$
其中 $\mathcal{L}_r^n$ 为 RGB 的 L2 损失，$\mathcal{L}_m^n$ 为掩码损失，$\mathcal{L}_p^n$ 为 LPIPS 感知损失，$\lambda_m$、$\lambda_p$ 为平衡权重。

**设计要点。** 消融实验（Table 3）揭示了两项关键设计选择：(1) 移除网格先验（即不使用 $\mathbf{f_m}$）会使 LPIPS 从 45.18 升至 46.26，表明即使在大规模数据下，人体结构先验仍能提供约 2.3% 的相对增益；(2) 将三平面空间尺寸从 96 缩减至 32（通用 LRM 的常见设置）导致 LPIPS 恶化至 48.33，证明充足的模型容量对细节重建至关重要。

![[assets/figures/papers/paper_list_l1027_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_HumanNOVA_Photoreal/figures/002_Figure_2.jpg]]
*Figure 2: HumanNOVA network architecture. Given a real-world input image, we first estimate its corresponding simplified human mesh. Image and mesh are fed into the multi-modal encoder to extract features which are utilized as the condition for the following mapping network. After that, a Transformer-based mapping network directly maps the features to the 3D triplane representation. From this triplane representation, our framework can render the 2D image given a camera viewpoint*

## 实验与关键发现

### 核心性能突破：HumanNOVA在三个基准上全面领先

HumanNOVA在CustomHuman、THuman2和2K2K三个基准上，对包括专用人体重建方法和通用三维生成模型在内的七类基线实现了全面超越。在渲染质量的核心感知指标LPIPS上，HumanNOVA相对于此前最强的专用方法**SiTH**（Ho et al., CVPR 2024）取得了显著提升：CustomHuman上LPIPS从72.94降至42.42（相对提升41.8%），THuman2上从66.90降至42.13（相对提升37.0%），2K2K上从73.55降至41.72（相对提升43.3%）。在PSNR指标上同样表现优异，以CustomHuman正面视图为例，HumanNOVA达到22.29，较SiTH的19.13提升了3.16 dB。这些结果验证了论文的核心主张：将大规模数据生成与类别特定先验相结合，使前馈重建模型在保真度上超越了依赖测试时优化的专用方法。

在几何质量方面，Table 6报告了Chamfer Distance（CD）、Normal Consistency（NC）和F-Score三项指标。HumanNOVA在所有指标上均优于所有基线方法，表明模型不仅在外观渲染上表现出色，在底层几何结构重建上也具备显著优势。

### 数据生成管线的因果验证

论文通过两组消融实验系统验证了数据生成管线中两个关键组件的独立贡献。

**Table 1** 拆解了合成数据（资产动画）与真实数据（多摄像头拟合）的作用。单独使用合成数据时PSNR为21.84，单独使用真实数据时PSNR为21.76，两者结合后PSNR提升至22.07。这表明两类数据提供了互补的信息：合成数据通过AMASS姿态驱动多样化的人体姿态变化，而真实数据通过3DGS拟合保留了高保真的外观细节。单独使用任一部分都会导致PSNR下降约0.23–0.31，证实了两者缺一不可。

**Table 2** 进一步验证了数据规模的因果效应。将生成数据的使用比例从25%逐步提升至100%，LPIPS从50.14单调下降至45.18，PSNR从21.37单调上升至22.07。这一单调趋势排除了“性能提升仅来自模型架构改进”的替代解释，直接证明了数据规模是性能提升的关键杠杆。

### 数据可迁移性：跨模型验证

为排除“生成数据仅对HumanNOVA自身有效”的可能性，论文设计了关键的外部验证实验。**Table 4** 显示，将HumanNOVA的生成数据用于微调通用重建模型**Real3D**（Jiang et al., ICCV 2025），使其在CustomHuman上的PSNR从17.13提升至20.97（+3.84 dB），在THuman2上从17.57提升至20.80（+3.23 dB），在2K2K上从17.29提升至20.51（+3.22 dB）。这一跨模型迁移效果不仅验证了数据本身的质量和泛化价值，也暗示了HumanNOVA的优越性能并非仅由数据驱动——其架构设计同样关键。

![[assets/figures/papers/paper_list_l1027_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_HumanNOVA_Photoreal/figures/004_Table_4.jpg]]
*Table 4: Effectiveness of our generated data. It is validated via fine-tuning another method (Real3D [25]) with our generated data*

### 模型设计的消融：网格先验与容量

**Table 3** 揭示了两个重要发现。第一，移除网格先验后LPIPS从45.18上升至46.26（相对恶化2.3%）。考虑到HumanNOVA已在大规模数据上训练，这一结果说明即使数据充足，人体结构先验仍能提供数据难以覆盖的几何约束，尤其在遮挡区域和极端姿态下。第二，将三平面空间尺寸从96降至32（通用LRM的常见设置），LPIPS急剧恶化至48.33，PSNR从22.07降至21.33。这表明人体重建对表示容量的需求显著高于通用物体重建，较小的三平面无法编码人体所需的细粒度几何和纹理细节。

### 失败模式与局限性

尽管HumanNOVA在整体指标上表现优异，论文坦诚地展示了典型失败案例（Figure 4底部）。主要失败模式集中在**背面纹理推断**上：对于连衣裙、背带裤等具有复杂背面结构的挑战性服装，网络有时无法生成合理的背面纹理。这一失败模式的根源在于单视图输入的固有信息缺失——正面图像无法提供背面的任何观测信号，模型必须依赖从训练数据中学习到的先验进行推断，而当服装类型与训练分布差异较大时，推断结果可能出现失真。此外，论文指出输入图像存在遮挡时重建质量可能下降，这是单视图重建方法的共性瓶颈。

### 评估公平性说明

论文在评估协议上做了细致的对齐工作，确保与输出网格的基线方法（如SiTH、SiFU、Trellis、Hunyuan2）的公平比较。具体而言，首先将重建网格的尺度与真值对齐，再运用ICP进行进一步几何对齐，最后渲染比较。这一流程同时保证了几何和渲染两个维度的公平性，排除了因尺度或位姿偏差导致的指标失真。

![[assets/figures/papers/paper_list_l1027_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_HumanNOVA_Photoreal/figures/003_Table_1.jpg]]
*Table 1: Ablation on the generated data type on the CustomHuman dataset*

![[assets/figures/papers/paper_list_l1027_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_HumanNOVA_Photoreal/figures/005_Table_5.jpg]]
*Table 5: Comparison with previous state-of-the-art methods on rendering quality. These include Real3D, SF3D, Trellis, Hunyuan2, PaMIR, SiFU and SiTH, on the CustomHuman, THuman2 and 2K2K datasets. We outperform all previous methods across all evaluated metrics with a notable gain. ↑ and ↓ represent the higher the better, and the lower the better, respectively*

![[assets/figures/papers/paper_list_l1027_https_openaccess_thecvf_com_content_CVPR2026_html_Hu_HumanNOVA_Photoreal/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative evaluation of our approach with in-thewild images as input. We also show some typical failure cases (bottom), e.g., inferring the plausible back texture of challenging clothes like dresses and overalls. (Best viewed in color.)*

## 定位与知识库关联

### 1. 在单视图三维人体重建谱系中的位置

单视图三维人体重建方法可沿两条轴线划分：**是否依赖测试时优化**，以及**是否利用人体结构先验**。HumanNOVA 处于这两条轴线的交汇点——它同时继承了通用前馈重建模型（LRM）的快速推理能力和专用人体重建方法的结构先验优势，从而在谱系中开辟了一个“通用且专用”的新位置。

- **测试时优化范式**：以 **PaMIR**（Zheng et al., TPAMI 2021）、**SiFU**（Zhang et al., CVPR 2024）、**SiTH**（Ho et al., CVPR 2024）为代表，这类方法在推理阶段对隐式表示（如 NeRF、SDF）进行逐样本优化，通常需要数分钟至数小时。它们能获得较高质量，但速度慢、难以规模化部署。HumanNOVA 以单次前向传播（<1秒）彻底消除了这一瓶颈，同时将 LPIPS 相对 SiTH 降低 40% 以上（Table 5），证明前馈模型在质量上同样可以超越优化范式。

- **通用前馈重建范式**：以 **Real3D**（Jiang et al., ICCV 2025）、**SF3D**（Boss et al., CVPR 2025）为代表的 LRM 方法，以及 **Trellis**（Xiang et al., CVPR 2025）、**Hunyuan2**（Zhao et al., arXiv 2025）等大规模 3D 生成模型，均采用前馈架构，推理速度快。但它们面向通用物体设计，缺乏人体专属建模能力。HumanNOVA 的消融实验（Table 3）表明，即使在大规模数据下，移除 SMPL 网格先验仍导致 LPIPS 相对恶化 2.3%，说明通用架构直接迁移至人体场景存在系统性性能损失。

- **数据驱动范式的关键转折**：现有方法受限于训练数据规模（约 5,000 个公开人体扫描资产），HumanNOVA 通过合成动画与多摄像头拟合管线将资产规模扩大 20 倍至 100k，从根本上改变了这一约束。Table 4 的迁移验证——用 HumanNOVA 生成数据微调 Real3D 使其 PSNR 从 17.13 提升至 20.97——进一步表明，**数据瓶颈的突破对通用模型同样有效**，数据本身具有跨架构的可迁移性。

### 2. 与基线方法的技术差异

| 维度 | 测试时优化方法（SiTH/SiFU/PaMIR） | 通用 LRM（Real3D/SF3D） | HumanNOVA |
|------|------|------|------|
| 推理机制 | 逐样本优化（分钟-小时级） | 单次前馈（秒级） | 单次前馈（<1秒） |
| 人体先验 | 隐式（通过优化约束） | 无 | 显式（SMPL 网格作为交叉注意力条件） |
| 训练数据规模 | ~5k（公开扫描） | ~5k（公开扫描） | 100k（合成+真实拟合） |
| 架构设计 | NeRF/SDF + 优化 | Transformer + 三平面 | Transformer + 双向交叉注意力融合多模态 token |
| 泛化能力 | 需测试时适配 | 通用物体，人体质量不佳 | 人体通用，无需适配 |

核心架构差异在于 HumanNOVA 的**双向交叉注意力融合机制**（Eq. 1-3）：图像特征 $\mathbf{f_i}$ 与网格特征 $\mathbf{f_m}$ 拼接后作为查询与三平面 token $\mathbf{T}^l$ 交互，随后反向将融合特征 $\mathbf{L}^l$ 作为查询与原始多模态 token 再次交互，最终更新三平面表示。这种设计使网格先验不仅作为附加输入，而是深度嵌入 2D 到 3D 的映射过程。消融实验（Table 3）中，将三平面空间尺寸从 96 降至 32（LRM 常用设置）导致 LPIPS 从 45.18 恶化至 48.33，表明**人体细节重建对模型容量有更高要求**，通用 LRM 的默认配置不足以承载。

### 3. 适用边界与局限

**适用场景**：
- 输入为单张包含完整人体的 RGB 图像，人物主体清晰可见
- 支持多样化服装、姿态和体型，无需针对特定身份或服装类型进行微调
- 适用于需要实时推理的应用场景（推理 <1 秒）

**已知局限**（Figure 4 失败案例）：
- **背面纹理推断困难**：对于连衣裙、背带裤等遮挡严重的挑战性服装，网络难以准确推断人物背面的纹理。这是单视图重建的固有歧义性——输入图像仅提供正面信息，背面完全依赖模型从数据中学习的先验。当前大规模数据虽缓解了这一问题，但尚未根本解决。
- **遮挡场景退化**：输入图像中存在遮挡时，重建质量可能下降。该问题在论文中被列为待解决方向，但未提供定量评估，需手动验证具体退化程度。

### 4. 开放问题

1. **遮挡鲁棒性**：如何使模型在输入图像存在部分遮挡（如手持物品、他人遮挡、自遮挡）时仍保持高质量重建？可能的路径包括引入多视图推理或显式遮挡建模，但当前框架仅依赖单视图输入，架构层面缺乏处理机制。

2. **人物-物体交互扩展**：当前方法仅重建孤立人体，如何将重建能力扩展至人物与物体的交互场景（如手持工具、坐在椅子上）？这需要同时推理人体、物体及其空间关系，对数据生成管线和模型架构均提出新挑战。

3. **动态化身建模**：HumanNOVA 目前重建静态三维人体。若能结合 AMASS 姿态序列的时间连续性，将前馈重建扩展为动态化身（即输入单张图像，输出可驱动的三维人体），将显著拓展应用范围。这需要在三平面表示中编码姿态依赖的变形信息。

4. **数据规模与质量的权衡**：合成动画数据（AMASS 驱动）提供了姿态多样性，但渲染保真度受限于资产质量；多摄像头 3DGS 拟合数据提供了高保真度外观，但姿态多样性受限于采集设置。Table 1 显示单独使用任一部分均导致 PSNR 下降 0.23-0.31，说明两者互补。是否存在更高效的混合策略，或是否需要引入新的数据模态（如视频），仍需探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/HumanNOVA_Photorealistic_Universal_and_Rapid_3D_Human_Avatar_Modeling_from_a_Single_Image.pdf]]
