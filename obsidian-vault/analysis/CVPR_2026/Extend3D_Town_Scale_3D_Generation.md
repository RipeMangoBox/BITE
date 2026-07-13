---
title: "Extend3D: Town-Scale 3D Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Extend3D_Town_Scale_3D_Generation.pdf
project_link: null
code_link: null
aliases:
- Extend3D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 沿 x/y 方向扩展潜在空间，并将扩展后的潜在空间划分为重叠块并行去噪，同时引入深度先验初始化和每步优化。
primary_logic: 扩展潜在空间配合重叠块耦合去噪，使对象中心模型能够协同生成大场景的局部细节；单目深度点云先验通过欠噪 SDEdit 初始化并利用 3D 感知优化矫正对象中心模型的偏差，从而实现免训练的大规模 3D 场景生成。
claims:
- 扩展潜在空间并使用重叠块去噪（d=4）可纠正局部结构错误并提升细节。
- 初始化与优化模块组合使所有外观和几何指标大幅提升（LPIPS 从 0.606 降至 0.240，F-score 从 0.261 升至 0.694）。
- 欠噪 SDEdit（t_noise < t_start）能够自然地补全单目深度缺失的遮挡区域。
- 100 diverse images (ChatGPT, Flux, CarlaSC, Google Earth, UrbanScene3D) 上 LPIPS↓ = 0.240
---

# Extend3D: Town-Scale 3D Generation

> [!tip] 核心洞察
> 扩展潜在空间配合重叠块耦合去噪，使对象中心模型能够协同生成大场景的局部细节；单目深度点云先验通过欠噪 SDEdit 初始化并利用 3D 感知优化矫正对象中心模型的偏差，从而实现免训练的大规模 3D 场景生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | Extend3D：城市场景规模的3D生成 |
| 英文题名 | Extend3D: Town-Scale 3D Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.29387) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Extend3D |
| Dataset | 100 diverse images, UrbanScene3D, Human preference |

> [!tip] 效果简介
> - 100 diverse images (ChatGPT, Flux, CarlaSC, Google Earth, UrbanScene3D) 上，LPIPS↓ 0.240 vs Trellis: 0.650 (-0.410)。
> - 100 diverse images 上，SSIM↑ 0.611 vs Trellis: 0.239 (+0.372)。
> - UrbanScene3D (45 image-mesh pairs) 上，F-score (0.05)↑ 0.694 vs EvoScene: 0.498 (+0.196)。

## 概要

**Extend3D** 是一种无需训练的城市场景规模 3D 生成流水线，旨在从单张场景图像生成大规模、多物体的 3D 场景。其核心瓶颈在于：现有的对象中心 3D 生成模型（如 **Trellis** (Xiang et al., CVPR 2025)、**Hunyuan3D-2.1** (Zhao et al., arXiv 2025)）受限于固定的潜在空间尺寸，无法直接处理多物体、大范围的场景结构；而简单地将图像域的高分辨率扩展方法（如 MultiDiffusion）迁移至 3D 域，则会导致地板消失、物体重复等严重伪影。

Extend3D 的核心洞察是：**沿 x/y 方向扩展潜在空间，并将其划分为重叠块进行并行去噪，使对象中心模型能够协同生成大场景的局部细节；同时引入单目深度点云先验，通过欠噪 SDEdit 初始化并利用 3D 感知优化矫正对象中心模型的偏差**。这一设计使得模型无需重新训练，即可将预训练的对象级生成能力泛化至城市场景规模。

在方法谱系上，Extend3D 位于训练无关的大场景生成方法（如 **EvoScene** (Zheng et al., arXiv 2025)、**SynCity** (Zheng et al., arXiv 2025)）与对象中心 3D 生成模型之间，通过“扩展-分块-耦合”的机制桥接两者的能力鸿沟。

实验表明，Extend3D 在 100 张多样化场景图像上的外观指标大幅领先对象中心基线：LPIPS 降至 **0.240**（Trellis 为 0.650），SSIM 提升至 **0.611**（Trellis 为 0.239）。在 UrbanScene3D 的几何评估中，F-score 达到 **0.694**，显著优于 EvoScene 的 0.498。人类偏好评估中，Extend3D 的完整性胜率达到 **87.1%**。消融实验证实，重叠块流、欠噪初始化与每步优化三个模块对最终性能的贡献均不可或缺。

方法的主要局限包括：对单目深度估计器精度的依赖、欠噪 SDEdit 迭代次数在几何完整性与细节保留间的权衡，以及街景图像中 x/y 坐标显著尺度不匹配时的处理困难。



### 对象中心 3D 生成模型的固有局限

近年来，以 **Trellis** (Xiang et al., CVPR 2025)、**Hunyuan3D-2.1** (Zhao et al., arXiv 2025) 为代表的对象中心 3D 生成模型取得了显著进展，能够从单张图像或文本生成高质量的三维物体。然而，这些模型的潜在空间尺寸是固定的（稀疏结构为 $N \times N \times \tilde{N}$，结构化潜变量为 $[M]^3$），这一设计从根本上限制了它们对多物体、大范围场景的表达能力。当面对城市场景规模的生成需求时，固定潜在空间无法容纳足够的几何与纹理细节，导致生成结果出现物体缺失、结构破碎等问题。

### 图像域扩展方法的直接迁移失败

在 2D 图像生成领域，**MultiDiffusion** 等方法通过将大画布划分为重叠块并独立去噪，成功实现了高分辨率图像生成。然而，直接将这一范式迁移到 3D 域会遭遇严重失败：地板消失、物体重复出现、块间不一致等伪影频繁发生。其根本原因在于 3D 生成的潜在空间具有更强的空间耦合性——每个局部区域的几何结构必须与相邻区域保持物理一致性，而对象中心模型在独立处理各块时缺乏这种全局协调能力。

### 现有大场景生成方法的不足

当前免训练的大场景 3D 生成方法如 **EvoScene** (Zheng et al., arXiv 2025) 和 **SynCity** (Zheng et al., arXiv 2025) 试图绕过对象中心模型的限制，但它们各自存在明显短板。EvoScene 依赖多视图扩散模型进行逐视图生成与融合，难以保证跨视图的几何一致性；SynCity 虽支持文本条件生成，但在块间纹理衔接和整体结构完整性上表现不佳。定量对比显示，EvoScene 在 UrbanScene3D 基准上的 F-score (0.05) 仅为 0.498，与理想的大场景生成质量仍有显著差距。

### 核心动机：扩展而非替换

本文的核心动机在于：**不重新训练大场景 3D 生成模型，而是通过扩展对象中心模型的潜在空间来突破其规模限制**。这一思路的关键洞察是——对象中心模型已经学会了丰富的 3D 先验知识，问题不在于模型能力不足，而在于其潜在空间的物理尺寸限制了输入范围。因此，沿 x/y 方向扩展潜在空间，并将扩展后的空间划分为重叠块进行耦合去噪，能够在保留对象中心模型强大先验的同时，实现城市场景规模的协同生成。此外，引入单目深度估计提供的点云先验进行欠噪 SDEdit 初始化，可以弥补对象中心模型对遮挡区域和大范围结构的感知偏差，从而在免训练的条件下实现大规模 3D 场景的高质量生成。



## 核心方法与创新机理

Extend3D 的核心创新在于通过**扩展潜在空间**与**重叠块耦合去噪**，使原本只能处理单个物体的 3D 生成模型能够生成城市场景规模的大范围 3D 内容。其关键设计围绕三个“changed slots”展开：潜在空间尺寸、初始化方式、以及去噪过程中的优化机制。

### 1. 扩展潜在空间与重叠块流

对象中心 3D 生成模型（如 **Trellis**, Xiang et al., CVPR 2025; **Hunyuan3D-2.1**, Zhao et al., arXiv 2025）的潜在空间尺寸是固定的，这直接限制了其表达多物体、大范围场景的能力。Extend3D 将稀疏结构潜变量从固定的 $N \times N \times \tilde{N}$ 扩展为 $aN \times bN \times N$，将结构化潜变量（SLAT）从 $[M]^3$ 扩展为 $[aM] \times [bM] \times [M]$，从而在 $x$ 和 $y$ 方向上获得更大的空间容量。

扩展后的潜在空间被划分为重叠的块（patch），每个块独立通过预训练模型计算向量场，随后在重叠区域进行平均合并：

$$
\pmb { v } ( \mathbf { Z } _ { t } , \mathcal { T } , t ) = \sum _ { i , j } \phi _ { i , j } ^ { - 1 } \big ( \pmb { v } _ { i , j } \big ) \ \oslash \ \sum _ { i , j } \mathbf { 1 } _ { \mathbb { W } _ { i , j } }
$$

这一“重叠块流”（overlapping patch-wise flow）机制实现了块间的耦合去噪动力学，使得局部细节能够在大场景中协同生成。消融实验证实，分割因子 $d$ 越大（即块间重叠越多），外观和几何指标越好：当 $d=8$ 时，LPIPS 降至 0.237，F-score 升至 0.699（Table 4）。若移除该机制，场景会出现地板消失、物体重复等典型失败模式——这正是直接将图像域多扩散方法（如 MultiDiffusion）应用于 3D 域时遇到的瓶颈。

### 2. 欠噪 SDEdit 初始化

传统对象中心模型从纯高斯噪声开始生成，缺乏对场景全局结构的先验。Extend3D 利用单目深度估计器（MoGe-2）从输入图像提取点云，将其体素化后作为初始结构。关键创新在于采用**欠噪 SDEdit**（under-noised SDEdit）策略：

$$
\mathbf { Z } _ { t _ { \mathrm { s t a r t } } } = ( 1 - t _ { \mathrm { n o i s e } } ) \cdot \mathbf { Z } _ { 0 } ^ { ( g ) } + t _ { \mathrm { n o i s e } } \cdot \boldsymbol \epsilon , \quad \epsilon \sim \mathcal { N } ( \mathbf 0 , I )
$$

其中 $t_{\mathrm{noise}} < t_{\mathrm{start}}$，即添加的噪声少于标准 SDEdit 所需的噪声量。这一设计的动机在于：单目深度估计无法获取被遮挡区域的信息，若按常规 SDEdit 加噪，模型会将遮挡区域视为需要“去噪”的噪声并胡乱填补；而欠噪策略使模型将遮挡部分视为额外噪声，从而更自然地补全缺失结构。消融实验表明，欠噪 SDEdit 在几何指标上取得最佳 F-score（0.680），显著优于常规 SDEdit 或过噪策略（Table 6, Figure 7(B)）。

### 3. 去噪过程中的先验优化

即使有了初始化和重叠块流，扩展后的潜变量在去噪过程中仍可能偏离输入图像和点云先验。Extend3D 在每一步去噪时对潜变量施加两类优化损失：

- **稀疏结构损失** $\mathcal{L}_{\mathrm{SS}}$：以点云先验构建二值交叉熵样损失，防止已初始化的体素在去噪中消失：

$$
\mathcal { L } _ { \mathrm { S S } } = - \frac { 1 } { | \mathbb { P } | } \sum _ { p \in \mathbb { P } } \log \sigma \big ( \big ( \mathcal { D } ( \mathbf { Z } _ { t } ^ { \mathrm { S S } } - t \cdot \hat { \pmb { v } } _ { t } ) \big ) _ { p } \big )
$$

- **结构化潜变量损失** $\mathcal{L}_{\mathrm{SLAT}}$：通过可微渲染将生成的 3D 表示投影为图像，与输入图像计算 LPIPS 和负 SSIM，从而优化纹理细节并消除块间边界：

$$
\mathcal { L } _ { \mathrm { S L A T } } = \mathrm { L P I P S } ( \hat { \mathcal { T } } , \mathcal { T } ) - \mathrm { S S I M } ( \hat { \mathcal { T } } , \mathcal { T } )
$$

这一“每步优化”机制是 Extend3D 区别于基线方法的关键——基线方法在去噪过程中不对潜变量施加任何外部优化。消融实验表明，移除初始化或优化模块会导致场景破碎或地板消失，定量指标严重恶化（Table 5）；而两者组合使用时，LPIPS 从 0.606 降至 0.240，F-score 从 0.261 升至 0.694，实现了外观和几何指标的大幅提升。

### 方法谱系与知识库定位

Extend3D 属于**免训练的大规模 3D 场景生成**方法，其核心思路是将对象中心 3D 生成模型的能力“扩展”到场景尺度，而非重新训练场景级模型。与之对比：

- **对象中心基线**（**Trellis**, Xiang et al., CVPR 2025; **Hunyuan3D-2.1**, Zhao et al., arXiv 2025）：潜在空间固定，无法处理多物体场景；Extend3D 通过扩展潜在空间和重叠块流突破了这一限制。
- **训练无关的场景生成方法**（**EvoScene**, Zheng et al., arXiv 2025; **SynCity**, Zheng et al., arXiv 2025）：同样免训练，但 EvoScene 依赖迭代式物体放置，SynCity 面向文本条件生成；Extend3D 则从单张图像出发，通过欠噪 SDEdit 初始化和每步优化实现了更精确的图像条件对齐与几何保真度。



Extend3D 是一个免训练的大规模 3D 场景生成流水线，其核心目标是解决对象中心 3D 生成模型在城市场景规模下的根本瓶颈：固定潜在空间尺寸无法容纳多物体、大范围场景的细节表达。该流水线由两个级联阶段构成——**稀疏结构生成**与**结构潜变量生成**，二者共享一个关键机制：将潜在空间沿 x 和 y 方向扩展，并通过重叠块耦合去噪实现局部细节的协同生成。

### 流水线总览

整个流水线以单张场景图像为输入，输出完整的 3D 场景表示。如图 2 所示，流程分为两个阶段：

1. **稀疏结构生成**：从输入图像提取场景的宏观几何布局，生成扩展的稀疏结构潜变量 $\mathbf{Z}_t^{\mathrm{SS}} \in \mathbb{R}^{aN \times bN \times N}$，经去噪解码后获得占据体素坐标集合 $\{\pmb{p}_i\} = \{\pmb{p} : \mathcal{D}(\mathbf{Z}_0^{\mathrm{SS}})_{\pmb{p}} > 0\}$。

2. **结构潜变量生成**：以稀疏结构为条件，生成扩展的结构化潜变量 $\mathbf{Z}_t^{\mathrm{SLAT}} \in \mathbb{R}^{aM \times bM \times M}$，经解码得到最终的纹理化 3D 场景。

两个阶段的去噪过程均采用**重叠块流**机制，并引入**先验初始化**与**每步优化**来矫正对象中心模型的固有偏差。

### 核心机制：重叠块流

扩展后的潜在空间被滑动窗口划分为重叠的块，每个块独立通过预训练的对象中心模型计算向量场 $\pmb{v}_{i,j}$，随后在重叠区域进行平均合并：

$$\pmb{v}(\mathbf{Z}_t, \mathcal{T}, t) = \sum_{i,j} \phi_{i,j}^{-1}\big(\pmb{v}_{i,j}\big) \ \oslash \ \sum_{i,j} \mathbf{1}_{\mathbb{W}_{i,j}}$$

其中 $\phi_{i,j}$ 为块提取操作，$\oslash$ 表示逐元素除法。这一设计使得各块在保持局部细节生成能力的同时，通过重叠区域的耦合避免了块间不一致——直接应用 MultiDiffusion 等图像域扩展方法会导致地板消失、物体重复等 3D 域特有的失败模式。

### 先验注入：初始化与优化

为矫正对象中心模型在大场景下的偏差，Extend3D 引入了双重先验：

- **欠噪 SDEdit 初始化**：利用单目深度估计器 MoGe-2 提取点云先验，将其体素化后通过迭代欠噪 SDEdit 初始化潜变量。欠噪策略（$t_{\mathrm{noise}} < t_{\mathrm{start}}$）使模型将被遮挡区域视为额外噪声，从而自然地补全单目深度缺失的部分。

- **每步去噪优化**：在去噪的每个时间步，利用点云先验和输入图像对潜变量进行优化。稀疏结构阶段使用 $\mathcal{L}_{\mathrm{SS}}$ 防止已初始化体素消失；结构潜变量阶段使用 $\mathcal{L}_{\mathrm{SLAT}} = \mathrm{LPIPS}(\hat{\mathcal{T}}, \mathcal{T}) - \mathrm{SSIM}(\hat{\mathcal{T}}, \mathcal{T})$ 通过可微渲染对齐纹理并消除块边界。

### 输入输出流

- **输入**：单张场景图像 $\mathcal{T}$
- **中间产物**：稀疏结构占据体素 $\{\pmb{p}_i\}$（作为第二阶段的条件 $C_{\mathcal{T}}$）
- **输出**：完整的纹理化 3D 场景，支持从任意视角渲染

该流水线无需针对场景数据进行额外训练，仅依赖预训练的对象中心 3D 生成模型（如 Trellis 的稀疏结构生成器和 Hunyuan3D-2.1 的 SLAT 生成器），通过潜在空间扩展和先验引导实现了从对象到城市场景的规模跨越。

### 补充图表

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/002_Figure_2.jpg]]
*Figure 2: An overall pipeline of our Extend3D. Extend3D consists of two parts: sparse structure generation and structured latent generation. In the denoising part of both steps, an overlapping patch-wise flow was used (Sec. 4.1 and Fig. 3). In sparse structure generation, iterative SDEdit is used to initialize the structure (Sec. 4.2). Vector fields in both steps are optimized with priors (Sec. 4.3)*



Extend3D 的核心由四个模块构成，它们共同解决了将对象中心 3D 生成模型扩展至城市场景规模的核心瓶颈：固定潜在空间无法容纳多物体、大范围场景的细节。

### 重叠块流（Overlapping Patch-wise Flow）

这是 Extend3D 实现潜在空间扩展的关键机制。首先，将稀疏结构潜在 $\mathbf{Z}_t^{\mathrm{SS}} \in \mathbb{R}^{aN \times bN \times N}$ 和结构化潜在 $\mathbf{Z}_t^{\mathrm{SLAT}} \in \mathbb{R}^{[aM] \times [bM] \times [M]}$ 沿 x 和 y 方向扩展，扩展因子为 $a$ 和 $b$。然后，用滑动窗口将扩展后的潜在空间划分为重叠的块，对每个块独立计算向量场：

$$v_{i,j}(\mathbf{Z}_t, \mathcal{T}, t) = v^{\downarrow}\big(\phi_{i,j}(\mathbf{Z}_t), C_{\psi_{i,j}(\mathcal{T})}, t\big)$$

其中 $\phi_{i,j}$ 是从扩展潜在空间到第 $(i,j)$ 个块的映射，$\psi_{i,j}$ 是对输入图像 $\mathcal{T}$ 的对应裁剪，$v^{\downarrow}$ 是预训练对象中心模型的向量场。

各块的向量场通过逆映射合并回扩展潜在空间，并在重叠区域做元素级平均：

$$\pmb{v}(\mathbf{Z}_t, \mathcal{T}, t) = \sum_{i,j} \phi_{i,j}^{-1}\big(\pmb{v}_{i,j}\big) \ \oslash \ \sum_{i,j} \mathbf{1}_{\mathbb{W}_{i,j}}$$

其中 $\oslash$ 表示逐元素除法，$\mathbf{1}_{\mathbb{W}_{i,j}}$ 是指示函数，分母统计每个位置被多少块覆盖。这一合并操作使得相邻块在去噪动力学中相互耦合，从而纠正局部结构错误并提升细节一致性。消融实验（Table 4）表明，分割因子 $d$ 越大（即块越小、重叠越多），所有外观和几何指标越好，$d=8$ 时达到 LPIPS 0.237、F-score 0.699。

### 欠噪 SDEdit 初始化（Under-noised SDEdit Initialization）

为给扩展后的潜在空间提供结构先验，Extend3D 利用单目深度估计器（MoGe-2）从输入图像提取点云，将其体素化后作为初始结构。但单目深度存在遮挡区域缺失的问题。为此，引入欠噪 SDEdit 策略：

$$\mathbf{Z}_{t_{\mathrm{start}}} = (1 - t_{\mathrm{noise}}) \cdot \mathbf{Z}_0^{(g)} + t_{\mathrm{noise}} \cdot \boldsymbol\epsilon, \quad \epsilon \sim \mathcal{N}(\mathbf{0}, I)$$

关键设计在于 $t_{\mathrm{noise}} < t_{\mathrm{start}}$：初始化的引导潜在 $\mathbf{Z}_0^{(g)}$ 添加的噪声小于目标起始时间步的噪声水平。这使得被遮挡部分被模型视为额外噪声，在迭代去噪过程中被自然补全（Figure 7 (B) 与 Table 6 验证了欠噪策略在几何补全上的优势，F-score 达 0.680）。该过程通过算法 $O_n = \mathrm{SDEdit}(O_{n-1})$ 迭代执行。

### 稀疏结构优化（Sparse Structure Optimization）

点云先验初始化的体素可能在去噪过程中消失。为防止此问题，引入稀疏结构损失，对解码后的体素占用施加二值交叉熵样约束：

$$\mathcal{L}_{\mathrm{SS}} = -\frac{1}{|\mathbb{P}|} \sum_{p \in \mathbb{P}} \log \sigma\big(\big(\mathcal{D}(\mathbf{Z}_t^{\mathrm{SS}} - t \cdot \hat{\pmb{v}}_t)\big)_p\big)$$

其中 $\mathbb{P}$ 是点云先验中的体素坐标集合，$\mathcal{D}$ 是稀疏结构解码器，$\sigma$ 是 sigmoid 函数。该损失强制已初始化的体素保持激活状态。

### 结构化潜在优化（Structured Latent Optimization）

为提升纹理细节并消除块边界伪影，对结构化潜在进行每步优化。通过可微渲染从结构化潜在生成图像 $\hat{\mathcal{T}}$，并与输入图像 $\mathcal{T}$ 计算损失：

$$\mathcal{L}_{\mathrm{SLAT}} = \mathrm{LPIPS}(\hat{\mathcal{T}}, \mathcal{T}) - \mathrm{SSIM}(\hat{\mathcal{T}}, \mathcal{T})$$

该损失结合感知相似度 LPIPS 和负的结构相似度 SSIM，在去噪的每一步对向量场进行梯度更新，使生成结果忠实于输入图像的外观。

消融实验（Table 5）表明，初始化与优化模块的组合使所有指标大幅提升：LPIPS 从 0.606 降至 0.240，F-score 从 0.261 升至 0.694。移除任一模块会导致场景破碎或地板消失（Figure 7 (C)）。



## 实验与关键发现

### 主实验结果

Extend3D 在人类偏好研究和定量指标上均显著优于现有方法。人类偏好研究（Table 1）邀请 10 名参与者对 14 个场景进行评分，Extend3D 在几何合理性（Geometry）、图像忠实度（Faithfulness）、外观质量（Appearance）和场景完整性（Completeness）四个维度上均取得最高胜率。与最强的训练无关大场景生成方法 **EvoScene**（Zheng et al., arXiv 2025）相比，Extend3D 在完整性维度上胜率达到 87.1%，在几何维度上同样为 87.1%；与对象中心方法 **Trellis**（Xiang et al., CVPR 2025）和 **Hunyuan3D-2.1**（Zhao et al., arXiv 2025）相比，优势更为显著（Table 1）。

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/005_Table_1.jpg]]
*Table 1: Human preference win rate (%) of our method*

定量评估（Table 2）在 100 张多样化输入图像（来源包括 ChatGPT、Flux、CarlaSC、Google Earth 和 UrbanScene3D）上进行。Extend3D 在所有外观指标上取得最佳结果：LPIPS 降至 0.240（Trellis 为 0.650，降幅达 0.410），SSIM 升至 0.611（Trellis 为 0.239，提升 0.372），PSNR 达到 20.4。在 UrbanScene3D 的 45 对图像-网格数据上评估几何质量，Extend3D 的 F-score（阈值 0.05）达到 0.694，远超 EvoScene 的 0.498（提升 0.196）。

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/006_Table_2.jpg]]
*Table 2: Quantitative results*

定性对比（Figure 5）进一步验证了上述结论：Trellis 和 Hunyuan3D-2.1 等对象中心方法因潜在空间尺寸固定，无法生成完整的大范围场景，常出现地板消失或物体缺失；EvoScene 虽能生成较大场景，但细节保真度不足。Extend3D 则能同时保持场景完整性和局部细节。

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative result of our Extend3D. Our 3D scene generation result (with a = b = 2) is compared to the results of state-ofthe-art 3D generative models. While previous methods may not accurately represent the image or lose scene details, our method effectively expresses the image condition in 3D. The input image is generated using Flux.1 [dev] [15]. We provide additional results in Sec. A.7*

与文本条件方法 **SynCity**（Zheng et al., arXiv 2025）的对比（Table 3）显示，Extend3D 在文本一致性和块间一致性上均占优。Figure 6 的定性结果表明，SynCity 生成的场景存在明显的块边界伪影，而 Extend3D 通过结构化潜变量优化有效消除了此类伪影。

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison with SynCity. The results are generated from the text prompt, medieval market*

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/010_Table_3.jpg]]
*Table 3: Comparison between 3D scene generation methods*

### 消融实验

**重叠块流的分割因子**（Table 4）：分割因子 $d$ 控制重叠块的大小（块尺寸为 $N/d \times N/d$）。$d$ 越大，块越小、重叠区域占比越高，耦合去噪效果越好。实验表明，$d=8$ 时 LPIPS 降至 0.237，F-score 升至 0.699，均优于 $d=4$ 和 $d=2$。Figure 7 (A) 的定性结果显示，不使用重叠块流（等效于独立处理各块）会导致明显的块边界和结构错误。

**初始化与优化模块**（Table 5）：移除点云初始化或每步优化均导致性能严重退化。完全移除初始化和优化时，LPIPS 从 0.240 飙升至 0.606，F-score 从 0.694 骤降至 0.261。Figure 7 (C) 显示，无初始化时场景结构破碎，无优化时地板消失。单独移除初始化（保留优化）或单独移除优化（保留初始化）均造成中间程度的性能损失，证明两个模块具有互补作用。

**欠噪 SDEdit 策略**（Table 6）：对比欠噪（$t_{\text{noise}} < t_{\text{start}}$）、常规 SDEdit（$t_{\text{noise}} = t_{\text{start}}$）和过噪（$t_{\text{noise}} > t_{\text{start}}$）三种策略，欠噪在几何指标上取得最佳 F-score（0.680），验证了其补全遮挡区域的有效性。Figure 7 (B) 显示，欠噪能够自然地填补单目深度估计无法观测的遮挡区域，而常规 SDEdit 则会破坏已有的结构信息。

**迭代次数**（Table 8）：欠噪 SDEdit 的迭代次数在几何补全与细节保留之间存在权衡。迭代次数过少则遮挡区域补全不足，过多则可能导致已有细节被平滑。

### 计算成本

Table 7 报告了各方法的计算成本。Extend3D 作为免训练方法，无需针对场景生成进行额外训练，计算开销主要来自推理阶段的扩展潜在空间去噪和每步优化。具体数值需查阅原文 Table 7。

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/014_Table_7.jpg]]
*Table 7: Computational costs of 3D generation methods*

### 失败模式与局限性

1. **深度估计依赖**：Extend3D 依赖单目深度估计器（MoGe-2）获取点云先验，深度估计的误差会直接传播到初始化和优化阶段，影响最终几何质量。
2. **尺度不匹配**：对于街景等含有显著 x/y 方向尺度不匹配的输入图像，扩展潜在空间的均匀缩放策略可能导致某一维度的信息密度不足或冗余。
3. **迭代权衡**：欠噪 SDEdit 的迭代次数需要在几何补全和纹理保真之间进行折中，目前缺乏自适应的迭代终止准则。

### 大规模场景生成

Figure 17 展示了 Extend3D 生成的大规模场景结果，验证了方法在城市场景规模（town-scale）下的可扩展性。通过调整扩展因子 $a$ 和 $b$，用户可以根据输入图像的宽高比灵活控制生成场景的空间范围。

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/027_Figure_17.jpg]]
*Figure 17: The large scale result of Extend3D. We generated large scale*

### 补充图表

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/011_Figure_7.jpg]]
*Figure 7: Ablation study. All the images, except for the ablation of under-noising, are taken from the input image camera viewpoint. We set*

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/012_Table_5.jpg]]
*Table 5: Ablation study on prior initialization and optimization*

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/013_Table_4.jpg]]
*Table 4: Ablation study for varying division factor d*

![[assets/figures/papers/paper_list_l2482_https_arxiv_org_abs_2603_29387/figures/015_Table_8.jpg]]
*Table 8: Ablation study on varying number of iterations*



## 定位与知识库关联

### 与对象中心 3D 生成模型的关系

Extend3D 并非提出新的 3D 生成模型，而是将预训练的对象中心 3D 生成模型（如 **Trellis** (Xiang et al., CVPR 2025) 和 **Hunyuan3D-2.1** (Zhao et al., arXiv 2025)）通过潜在空间扩展和先验注入，适配到城市场景规模的生成任务中。其核心创新在于一个免训练的流水线：沿 x 和 y 方向扩展潜在空间（从 $N \times N \times \tilde{N}$ 扩展到 $aN \times bN \times N$），将扩展后的潜在空间划分为重叠块并行去噪，并通过单目深度点云先验进行欠噪 SDEdit 初始化和每步优化，从而克服对象中心模型固定潜在空间尺寸对多物体、大范围场景的表达瓶颈。

对象中心模型通常将场景表示为单个紧凑的潜在编码，这导致在生成包含多个建筑、道路和自然元素的城市场景时，细节丢失严重、物体重复或地板消失。Extend3D 通过重叠块流（overlapping patch-wise flow）将大场景分解为耦合的子区域，每个子区域由预训练模型独立处理，再通过重叠区域的平均合并实现全局一致性。这一策略与图像域中的 MultiDiffusion 等拼接方法思路相似，但 Extend3D 针对 3D 域的特殊性（深度歧义、几何一致性要求更高）引入了深度先验初始化和可微渲染优化，避免了直接迁移图像域方法时的失败。

### 与大场景生成方法的对比

在训练无关的大场景生成方法中，Extend3D 与 **EvoScene** (Zheng et al., arXiv 2025) 和 **SynCity** (Zheng et al., arXiv 2025) 形成直接对比。EvoScene 同样面向从单张图像生成 3D 场景，但 Extend3D 在 UrbanScene3D 基准上以 F-score 0.694 显著优于 EvoScene 的 0.498（Table 2），表明先验注入和优化策略对几何精度的提升至关重要。在文本条件下的场景生成中，Extend3D 与 SynCity 的对比显示，Extend3D 在文本一致性和块间一致性上均占优（Table 3），这得益于重叠块流的耦合机制和可微渲染损失对块边界的消除。

### 适用边界与局限

Extend3D 的适用性受以下因素制约：

1. **深度估计依赖**：初始化阶段依赖单目深度估计器（MoGe-2）获取点云先验。深度估计误差会直接传导至稀疏结构初始化，影响后续去噪和优化的质量。对于深度歧义严重的场景（如大面积水面、玻璃幕墙），初始化质量可能显著下降。

2. **欠噪 SDEdit 的迭代权衡**：欠噪 SDEdit 的迭代次数在几何补全和细节保留之间存在权衡（Table 8）。迭代过少则遮挡区域补全不足，迭代过多则可能模糊已有结构的纹理细节。

3. **尺度不匹配问题**：街景图像等含有显著 x-y 尺度不匹配的输入可能导致处理不佳。这是因为潜在空间扩展假设 x 和 y 方向具有相似的场景分布，而街景中纵深方向（y）的尺度变化远大于横向（x），打破了这一假设。

### 开放问题

论文明确指出了两个待解决的问题：一是如何处理街景图像中 x 和 y 坐标的显著尺度不匹配，二是如何进一步改善遮挡区域的补全质量。前者可能需要引入非均匀的潜在空间扩展策略或自适应分块机制，后者则可能通过更强的几何先验（如多视图深度估计）或更精细的优化策略来解决。



## 原文 PDF

![[paperPDFs/CVPR_2026/Extend3D_Town_Scale_3D_Generation.pdf]]
