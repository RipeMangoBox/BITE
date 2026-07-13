---
title: "Layered 4D-Rotor Gaussian Splatting: A Compressed Representation for Long Dynamic Scenes"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Layered_4D_Rotor_Gaussian_Splatting_A_Compressed_Representation_for_Long_Dynamic_Scenes.pdf
project_link: "https://m1sak1-mei.github.io/layered-4d-rotor/"
code_link: null
aliases:
- L4RGSL
- L4RGSCRLDS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过分层-分桶的时间组织结构（layer-bucket）控制每帧可见高斯子集，并设计因子化协方差量化、分层压缩和残差码本量化的协同压缩管线。
primary_logic: 基于4D高斯的时间跨度将其按层和桶组织，利用各层不同的时域分布特性实施感知压缩，能够在保持高视觉质量的同时将存储压缩20倍以上并实现超500 FPS的实时渲染，突破了长视频动态场景建模的内存与存储瓶颈。
claims:
- 在N3DV数据集上，压缩变体Ours Large取得PSNR 32.06，而存储仅13.8 MB，对比DyNeRF的29.58 PSNR有明显提升
- 消融实验表明因子化协方差量化(FCQ)将PSNR从直接量化时的11.35提升至22.09，并降低存储
- 60秒长序列实现20×以上压缩且在RTX 5090上达到超过900 FPS的实时渲染
- N3DV (平均6场景) 上 PSNR↑ = 32.06 (Ours Large)
---

# Layered 4D-Rotor Gaussian Splatting: A Compressed Representation for Long Dynamic Scenes

> [!tip] 核心洞察
> 基于4D高斯的时间跨度将其按层和桶组织，利用各层不同的时域分布特性实施感知压缩，能够在保持高视觉质量的同时将存储压缩20倍以上并实现超500 FPS的实时渲染，突破了长视频动态场景建模的内存与存储瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | 分层4D旋量高斯泼溅：面向长动态场景的压缩表示 |
| 英文题名 | Layered 4D-Rotor Gaussian Splatting: A Compressed Representation for Long Dynamic Scenes |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_Layered_4D-Rotor_Gaussian_Splatting_A_Compressed_Representation_for_Long_Dynamic_CVPR_2026_paper.html) · [Project](https://m1sak1-mei.github.io/layered-4d-rotor/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | Layered 4D-Rotor Gaussian Splatting (L4DRotorGS) |
| Dataset | N3DV, SelfCap, N3DV Flame Salmon |

> [!tip] 效果简介
> - N3DV (平均6场景) 上，PSNR↑ 32.06 (Ours Large) vs 29.58 (DyNeRF) (+2.48)；PSNR / Storage / FPS 31.84 / 8.8 MB / 660.79 (Ours Small) vs 29.58 / 28 MB / 0.015 (DyNeRF) (PSNR +2.26，存储减少~70%，FPS提升~44000x)。
> - SelfCap (6个长序列) 上，PSNR 24.49 (Ours Large) / 24.41 (Ours Small) vs TGH (详见Table 2) (保持与未压缩模型相近的质量)。
> - N3DV Flame Salmon (60s, 3600帧) 上，压缩比 / FPS >20× 压缩，>900 FPS (RTX 5090) vs 未压缩4D高斯 (>500 MB, <60 FPS 估计) (存储压缩>20×，帧率提升>10×)。

## 概要

**问题瓶颈**：长动态场景建模中，4D高斯表示的数量随视频时长急剧增长，导致GPU显存与存储需求过大，难以实现实时渲染与轻量部署。

**核心思路**：提出**分层4D旋量高斯泼溅（Layered 4D-Rotor Gaussian Splatting, L4DRotorGS）**，通过“分层-分桶”的时间组织结构控制每帧可见高斯子集，并设计因子化协方差量化、分层压缩与残差码本量化的协同压缩管线，在保持高视觉质量的同时实现大幅度存储压缩与实时渲染。

**方法定位**：该方法建立在**4D-Rotor Gaussian Splatting**（Duan et al., SIGGRAPH 2024）的动态表示基础上，借鉴**Temporal Gaussian Hierarchy**（Xu et al., TOG 2024）的分层思想，但将固定时间分段改进为基于时间跨度的层-桶结构，并引入感知压缩策略，区别于**DyNeRF**（Li et al., CVPR 2022）等NeRF类方法在渲染速度上的数量级劣势。

**关键结果**：
- 在**N3DV数据集**上，压缩变体Ours Large取得PSNR 32.06，存储仅13.8 MB，渲染速度超过660 FPS（RTX 3090），相比DyNeRF的29.58 PSNR和0.015 FPS有显著提升。
- 在**60秒长序列**（3600帧）上实现超过20×的存储压缩，并在RTX 5090上达到超过900 FPS的实时渲染。
- 消融实验表明，**因子化协方差量化**是压缩质量的关键使能组件——直接对4D协方差进行矢量量化会导致PSNR骤降至11.35，而FCQ将其恢复至22.09，同时将存储从29.03 MB降至16.22 MB。

**主要局限**：压缩过程仍然耗时，当前框架不支持在线训练，限制了其在流式捕捉场景中的适应性。

### 动态场景新视角合成的存储与实时性困境

三维场景的新视角合成（Novel View Synthesis, NVS）在虚拟现实、增强现实、影视制作和自由视点视频等领域具有广泛的应用前景。近年来，以 **3D Gaussian Splatting (3DGS)**（Kerbl et al., TOG 2023）为代表的显式点基表示方法在静态场景渲染中取得了突破性进展，实现了高质量与高帧率的兼顾。然而，将此类方法扩展到**长动态场景**时，面临一个根本性的瓶颈：4D 高斯数量随视频时长急剧增长，导致 GPU 显存与存储需求过大，无法实现实时渲染和实际部署。

具体而言，对于一段 60 秒、3600 帧的动态序列，未经压缩的 4D 高斯表示可能需要超过 500 MB 的存储空间，且渲染帧率远低于实时交互所需的 60 FPS。这一矛盾在长视频场景中尤为突出——用户既希望保留精细的时空细节，又要求模型足够轻量以支持流畅的实时浏览。现有的动态 NeRF 方法（如 **DyNeRF**，Li et al., CVPR 2022）虽然能够生成高质量渲染结果，但其推理速度极慢（约 0.015 FPS），完全无法满足实时应用需求。

### 现有压缩方法的局限

针对 4D 高斯表示的存储膨胀问题，学界已提出若干压缩方案，但均存在明显不足：

- **直接矢量量化（VQ）**：将 4D 协方差矩阵作为一个整体进行矢量量化，会导致严重的质量退化。实验表明，直接 VQ 后 PSNR 从 30+ 骤降至 11.35，几乎丧失可用性。其根本原因在于，4D 协方差矩阵内部各分量（空间旋转、时间演化、各向异性尺度）的数值分布特性差异极大，统一量化无法有效保留几何结构。

- **固定时间分段（TGH 方案）**：**Temporal Gaussian Hierarchy (TGH)**（Xu et al., TOG 2024）采用固定时间片段划分，在片段边界处裁剪高斯。这种方式虽然实现了分层管理，但刚性边界导致跨片段的高斯被强行截断，造成时间边界处的渲染不连续和细节丢失。

- **全局码本压缩**：对所有层共用同一套矢量量化码本，忽略了不同时间跨度的高斯层在尺度因子、旋转分量等属性上的分布差异，压缩效率受限。

### 核心动机与解决思路

本文的核心动机在于：**设计一种既能保持高视觉质量，又能将存储压缩 20 倍以上并实现超 500 FPS 实时渲染的长动态场景表示方法**。这一目标要求同时解决三个相互耦合的子问题：

1. **高效的时间组织结构**：如何让每帧渲染时仅加载必要的高斯子集，避免全量数据驻留 GPU 显存？
2. **感知压缩策略**：如何利用不同时间跨度高斯层的分布特性，对几何与外观属性实施差异化、高保真的量化压缩？
3. **训练稳定性**：如何在压缩约束下保证静态区域的细节保真度，避免纹理过平滑？

针对上述问题，本文提出了 **Layered 4D-Rotor Gaussian Splatting (L4DRotorGS)**，其核心洞察在于：**基于 4D 高斯的时间跨度将其按“层”和“桶”组织，利用各层不同的时域分布特性实施感知压缩**。具体而言，方法引入以下关键设计：

- **层-桶结构（Layer-Bucket Structure）**：根据高斯的时间跨度将其分配到不同层（长跨度高斯位于高层，短跨度高斯位于低层），每层再划分为时间桶。渲染时仅加载当前桶及其邻桶的高斯数据，实现稀疏访问。与 TGH 的刚性分段不同，本方法允许高斯跨越桶边界，消除了时间边界 artifact。

- **因子化协方差量化（Factorized Covariance Quantization, FCQ）**：将 4D 协方差矩阵分解为尺度因子、归一化尺度、转子空间分量和转子时间分量四部分，分别采用标量量化（SQ）或矢量量化（VQ）。这一分解使得各分量的量化策略可以独立优化，避免直接 VQ 造成的灾难性质量损失。

- **分层压缩与残差码本量化**：对分布差异大的属性（如尺度因子、转子分量）采用层专属码本，对分布一致的属性（如球谐系数、不透明度）采用全局量化。进一步引入残差码本量化（Residual Codebook Quantization, RCQ），在层内分块用轻量残差码本修正层全局码本，提升压缩上限。

- **动态感知旋转学习率（Dynamic-Aware Rotor Learning Rate, DARLR）**：对时间跨度大的高斯分配更小的旋转学习率，稳定静态区域的训练，保留精细纹理。

实验结果表明，该方法在 N3DV 数据集上以仅 8.8 MB 的存储（Ours Small）取得 31.84 PSNR，渲染速度达 660.79 FPS；在 60 秒长序列上实现超过 20 倍压缩和超过 900 FPS 的实时渲染（RTX 5090），突破了长视频动态场景建模的内存与存储瓶颈。

## 核心方法与创新机理

本文的核心创新在于构建了一套**感知驱动的分层-分桶时间组织结构**与**因子化协方差量化管线**，协同解决长动态场景中4D高斯数量急剧膨胀导致的存储与渲染瓶颈。其关键创新点可归纳为以下五个“changed slots”，均围绕“时间组织方式”与“压缩粒度”两个核心维度展开。

### 1. 时间组织方式：从固定分段到层-桶跨越结构

**基线方法**（如TGH, Xu et al., TOG 2024）采用固定时间分段，在片段边界处强制裁剪高斯，破坏了时间连续性。**本文提出**基于高斯有效时间跨度 $\tau = 2\sqrt{16/\lambda}$ 的层-桶结构：将每个TGH片段进一步划分为左右两个时间桶，同时**允许高斯跨越桶边界**。每帧渲染时仅加载当前桶及其相邻桶的高斯子集。这一设计将每帧可见高斯数量从与视频总长相关的 $O(N)$ 降至与局部时间窗口相关的常数级，从根本上解耦了场景时长与渲染内存需求。

### 2. 协方差量化：从直接矢量量化到因子化分解量化

**基线方法**（如C3DGS）直接对4D协方差矩阵 $\pmb{\Sigma}_{4D}$ 进行矢量量化（VQ）。**本文提出因子化协方差量化（FCQ）**：将协方差矩阵按物理意义分解为四个独立分量——
- **尺度因子**（scalar scale factor）
- **归一化尺度**（normalized scale）
- **转子空间分量**（rotor spatial component）
- **转子时间分量**（rotor temporal component）

——并分别采用标量量化（SQ）或矢量量化（VQ）。消融实验（Table 4）表明，FCQ将直接VQ的PSNR从11.35提升至22.09，同时存储从29.03 MB降至16.22 MB，证明了**按物理属性分解量化**对几何压缩的决定性作用。

### 3. 压缩粒度：从全局码本到分层压缩

不同时间层的高斯具有显著不同的属性分布特征（如长时层高斯尺度大、分布稀疏，短时层高斯密集且细节丰富）。**本文提出分层压缩策略**：对分布差异大的属性分量（尺度因子、转子分量）采用**层专属码本**进行量化，而外观属性（球谐系数、不透明度）仍使用全局量化。这一感知驱动的差异化压缩在保持视觉质量的同时大幅提升压缩效率，Table 4显示分层压缩将PSNR进一步提升至28.90。

### 4. 码本精炼：残差码本量化（RCQ）

为进一步提升压缩上限，**本文在分层压缩基础上引入残差码本量化（RCQ）**：在每层内部将高斯按桶分块，用轻量残差码本对层全局码本进行**块级修正**，量化“块专属码本”与“层全局码本”之间的差异。Table 5消融表明，RCQ码本尺寸在64–1024范围内对存储和PSNR影响极小，方法具有强鲁棒性。

### 5. 训练稳定性：动态感知旋转学习率（DARLR）

**基线方法**使用统一的旋转学习率，导致静态区域纹理过平滑。**本文提出动态感知旋转学习率（DARLR）**：对时间跨度大的高斯分配更小的旋转学习率，抑制静态区域的过度更新。Figure 7定性结果表明，DARLR能有效保留静态区域的高频纹理细节，显著减少artifacts。

**创新协同效应**：上述五个changed slots并非孤立改进。层-桶结构提供了时间局部性，使得分层压缩和RCQ能针对各层分布特性实施感知量化；FCQ将协方差分解为独立分量，为分层压缩提供了可分离的优化维度；DARLR则在训练阶段稳定了几何属性，为后续压缩管线提供了更高质量的初始表示。三者共同构成了从训练到压缩再到实时渲染的完整高效管线。

L4DRotorGS 的整体框架围绕**分层时间组织—训练—压缩—实时渲染**四个阶段构建，形成一条从长视频输入到高压缩比实时渲染的完整管线。其核心设计目标是在保持视觉质量的前提下，将4D高斯的存储需求压缩20倍以上，同时实现超500 FPS的实时渲染。

### 分层表示与时间组织

框架的第一步是将所有4D高斯按时间跨度组织为**层–桶（layer–bucket）结构**。每个4D高斯由其时间中心 $\mu_t$ 和有效时间跨度 $\tau = 2\sqrt{16/\lambda}$ 共同决定所属的层级。层数 $L = \lceil\log_2 n\rceil + 1$ 由视频总帧数 $n$ 自动确定：时间跨度越大的高斯被分配到越高的层，每层内部再按 $\mu_t$ 划分为离散的时间桶。与 **TGH**（Xu et al., TOG 2024）的固定时间分段不同，本方法允许高斯跨越桶边界，从而避免硬边界处的高斯截断伪影。在查询任意时刻 $t$ 时，系统仅加载当前桶及其相邻桶的高斯子集，使得每帧活跃高斯数量与视频总时长解耦——这是实现长视频实时渲染的关键瓶颈突破。

### 训练阶段：三缓冲策略

训练框架针对分层表示进行了深度定制。由于层–桶结构导致高斯数据在 GPU 显存与 CPU 内存之间频繁迁移，本文提出了**三缓冲策略（Triple-buffer Strategy）**：GPU 端维护双缓冲，CPU 端维护桶缓冲。在自适应密度控制（克隆、分裂、剪枝）与前向/反向传播过程中，高斯的加载与卸载被组织为流水线操作，显著降低了 CPU–GPU 内存拷贝开销。此外，训练阶段引入了**动态感知旋转学习率（DARLR）**：对时间跨度大的高斯分配更小的旋转学习率，以稳定静态区域的训练，保留精细纹理并减少过平滑伪影（见 Figure 7）。

### 压缩阶段：三组件协同量化管线

训练完成后，模型进入压缩阶段。压缩管线由三个递进组件构成，对应 Figure 2(b) 所示的整体结构：

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Layered_4D_Rotor_Ga/figures/003_Figure_2.jpg]]
*Figure 2: Layered Representation Overview. As shown in (a), we seperate 4D Gaussians into layers and buckets according to their temporal extents and*

1. **因子化协方差量化（FCQ）**：将4D协方差矩阵 $\Sigma_{4D} = \mathbf{R}_{4D} \mathbf{S}_{4D} \mathbf{S}_{4D}^T \mathbf{R}_{4D}^T$ 分解为尺度因子、归一化尺度、转子空间分量和转子时间分量四个独立成分，分别进行标量量化（SQ）或矢量量化（VQ）。这一分解是压缩的关键使能器——消融实验表明，直接对4D协方差进行VQ会导致 PSNR 骤降至 11.35，而 FCQ 将其提升至 22.09，同时存储从 29.03 MB 降至 16.22 MB（Table 4）。

2. **分层压缩（Layered Compression）**：对于各层间分布差异显著的几何属性（尺度因子、转子分量），采用层专属码本进行量化；外观属性（球谐系数 SH、不透明度）则仍使用全局量化。此步骤将 PSNR 进一步提升至 28.90（Table 4），有效保留了跨层的高频细节。

3. **残差码本量化（RCQ）**：在每层内部将高斯按桶分块，引入轻量残差码本对层全局码本进行块级修正，量化的是块专属码本与层全局码本之间的残差。RCQ 在保持压缩率的同时提供额外的质量增益，且对码本尺寸（64–1024）不敏感（Table 5），表现出良好的鲁棒性。

外观属性的压缩策略为：不透明度经 sigmoid 激活后天然落在 $[0,1]$，直接采用标量量化（SQ）；SH 系数则采用矢量量化（VQ），其码本尺寸对质量–存储权衡影响最大（Figure 4、Figure 5）。

### 实时渲染阶段

渲染时，给定查询时间戳 $t$，系统从各层中仅加载当前桶及相邻桶的压缩高斯数据。经 FCQ 解码恢复完整协方差后，通过时间切片公式 $G_{3D}(\mathbf{x}, t) = e^{-\frac{1}{2}\lambda(t-\mu_t)^2} e^{-\frac{1}{2}[\mathbf{x}-\boldsymbol{\mu}(t)]^T \Sigma_{3D}^{-1} [\mathbf{x}-\boldsymbol{\mu}(t)]}$ 将4D高斯投影为3D高斯，再执行标准3D高斯泼溅渲染。整个框架以 C++/CUDA 实现，训练、渲染与压缩均在 GPU 上加速。

### 输入输出流总结

- **输入**：多视角视频（N3DV 为 300 帧/场景，SelfCap 最长 3600 帧/场景），含标定相机参数。
- **输出**：压缩后的分层4D高斯表示文件，以及任意新视角、任意时刻的实时渲染图像。
- **中间产物**：训练阶段产出未压缩的层–桶结构4D高斯；压缩阶段产出量化后的紧凑表示。

该框架的整体流程可概括为：**视频 → 分层4D高斯初始化 → 三缓冲训练（含 DARLR） → FCQ + 分层压缩 + RCQ 压缩管线 → 压缩表示 → 按需解码渲染**。

### 4D高斯表示与时间切片

L4DRotorGS继承4D-Rotor Gaussian Splatting（**4DGS**, Duan et al., SIGGRAPH 2024）的4D高斯核定义。一个4D高斯由4D中心 $\pmb{\mu}_{4D} \in \mathbb{R}^4$ 和4D协方差矩阵 $\pmb{\Sigma}_{4D} \in \mathbb{R}^{4 \times 4}$ 参数化：

$$G_{4D}(\mathbf{x}) = e^{-\frac{1}{2}(\mathbf{x} - \pmb{\mu}_{4D})^{T} \pmb{\Sigma}_{4D}^{-1} (\mathbf{x} - \pmb{\mu}_{4D})}$$

协方差矩阵进一步分解为4D旋转矩阵 $\mathbf{R}_{4D}$ 和各向异性缩放矩阵 $\mathbf{S}_{4D}$：

$$\pmb{\Sigma}_{4D} = \mathbf{R}_{4D} \mathbf{S}_{4D} \mathbf{S}_{4D}^{T} \mathbf{R}_{4D}^{T}$$

其中旋转以4D旋量（rotor）表示，缩放由尺度因子 $s$、归一化3D尺度 $\hat{\mathbf{s}}_{3D}$ 和时间尺度 $\sigma_t$ 构成。

给定查询时间戳 $t$，将4D高斯沿时间维度切片，得到用于渲染的3D高斯：

$$G_{3D}(\mathbf{x}, t) = e^{-\frac{1}{2}\lambda(t-\mu_t)^2} e^{-\frac{1}{2}[\mathbf{x}-\pmb{\mu}(t)]^{T} \pmb{\Sigma}_{3D}^{-1} [\mathbf{x}-\pmb{\mu}(t)]}$$

其中 $\lambda = 1/\sigma_t^2$ 为时间精度，$\pmb{\mu}(t)$ 是时间 $t$ 处的高斯中心在3D空间中的投影位置。切片后，时间维度退化为一个标量衰减因子 $e^{-\frac{1}{2}\lambda(t-\mu_t)^2}$，与3D高斯核相乘。

**可见性裁剪**：当 $\lambda(t - \mu_t)^2 > 16$ 时，高斯对当前帧的贡献可忽略，直接裁剪。等效地，每个高斯的有效时间跨度为：

$$\tau = 2\sqrt{16/\lambda}$$

$\tau$ 是高斯分配层和桶的核心依据——时间跨度越大的高斯被分配到越高层，时间跨度小的静态高斯则留在底层。

---

### 分层-分桶时间组织结构

这是本文区别于**TGH**（Xu et al., TOG 2024）的核心设计。给定总帧数 $n$，自动确定层数：

$$L = \lceil\log_2{n}\rceil + 1$$

**层分配逻辑**：第 $l$ 层（$l = 0, 1, \dots, L-1$）容纳时间跨度 $\tau$ 满足特定区间的高斯。底层（$l=0$）包含时间跨度最小的高斯，高层包含跨越更大时间范围的高斯。

**桶划分**：每层进一步将TGH片段划分为左右两个时间桶，但允许高斯跨越桶边界。渲染时仅加载当前桶及其直接邻居桶中的高斯，实现按需加载。

**因果机制**：层-桶结构将“每帧可见高斯子集”作为可控旋钮——通过高斯的 $\tau$ 和 $\mu_t$ 预先分配，查询时按时间戳快速检索，将渲染所需的高斯数量与视频总时长解耦。这是实现长视频实时渲染和存储压缩的前提。

---

### 因子化协方差量化（FCQ）

直接对4D协方差矩阵进行矢量量化（**C3DGS**方式）会导致严重质量退化。FCQ将协方差分解为四个独立分量分别量化：

1. **尺度因子 $s$**：标量，控制高斯整体大小。
2. **归一化3D尺度 $\hat{\mathbf{s}}_{3D}$**：3维向量，描述空间各向异性。
3. **转子空间分量**：编码3D旋转。
4. **转子时间分量**：编码时间-空间耦合旋转。

**量化策略**：尺度因子 $s$ 和归一化尺度 $\hat{\mathbf{s}}_{3D}$ 使用标量量化（SQ）；转子空间和时间分量使用矢量量化（VQ）。这种分解使各分量的量化粒度与其在渲染中的敏感度匹配——旋转分量的微小误差对视觉质量影响大，需用VQ精细保留；尺度因子的容错性较高，SQ即可。

**证据强度**：消融实验（Table 4）显示，FCQ将PSNR从直接VQ的11.35提升至22.09，同时存储从29.03 MB降至16.22 MB，证明因子化分解是几何属性压缩的关键使能技术。

---

### 分层压缩与残差码本量化（RCQ）

**分层压缩**：不同层的高斯属性分布差异显著——高层高斯时间跨度大、数量少，底层高斯密集但时间局部性强。对分布差异大的分量（尺度因子、转子分量）采用层专属码本量化，外观属性（球谐系数SH、不透明度）仍使用全局量化。

**不透明度压缩**：对sigmoid激活后的值做SQ，因其自然落在 $[0, 1]$ 有界区间。

**RCQ**：在每层内将高斯按桶分块，引入轻量残差码本量化块专属码本与层全局码本之间的差异。这在不显著增加存储的前提下提升了压缩上限。Table 5表明RCQ码本尺寸在64-1024范围内对PSNR和存储影响很小，方法鲁棒。

---

### 训练优化策略

**三缓冲训练**：GPU双缓冲 + CPU桶缓冲。自适应密度控制（克隆/分裂/剪枝）期间，高斯在GPU双缓冲和CPU缓冲间异步传输，显著减少CPU-GPU内存拷贝开销。这是训练框架适配分层结构的关键工程优化。

**动态感知旋转学习率（DARLR）**：对时间跨度大的高斯分配更小的旋转学习率，稳定静态区域训练。消融实验（Figure 7）证实DARLR保留静态区域精细纹理，无此策略时纹理过度平滑、高频结构丢失。

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Layered_4D_Rotor_Ga/figures/008_Figure_7.jpg]]
*Figure 7: Ablation of Dynamic-Aware Rotor Learning Rate (DARLR). DARLR preserves fine detail in static regions; without it, textures appear over-smoothed and lose high-frequency structure*

## 实验与关键发现

### 主要结果：N3DV与SelfCap数据集

L4DRotorGS在N3DV多视角动态视频数据集上进行了全面评测，与NeRF基方法和3D/4D高斯基方法进行了对比。**Table 1**展示了主要定量结果。

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Layered_4D_Rotor_Ga/figures/009_Table_1.jpg]]
*Table 1: Evaluation on N3DV Dataset. We compare our method with both NeRF-based and Gaussian-based approaches on an NVIDIA RTX 3090. *: Compression time included. †: Evaluated on the Flame Salmon scene only. ‡: Evaluated using a different LPIPS protocol in the original paper*

**Ours Large**变体在N3DV六个场景上取得了平均PSNR **32.06**，显著优于**DyNeRF**（Li et al., CVPR 2022）的29.58 dB（+2.48 dB），同时存储仅需**13.8 MB**，实现了**13.1×**的存储压缩。**Ours Small**变体以**8.8 MB**存储（**20.5×**压缩比，码率低于1 MB/s）取得PSNR **31.84**，相比DyNeRF仍有2.26 dB的提升。在渲染速度方面，两种压缩变体在RTX 3090上均超过**660 FPS**，而DyNeRF仅约0.015 FPS，帧率提升约44000倍。

在SelfCap长视频数据集（6个场景，序列时长显著长于N3DV）上，**Table 2**显示Ours Large取得平均PSNR **24.49**，Ours Small取得**24.41**，与未压缩模型保持相近的视觉质量，同时大幅降低存储需求。对于60秒（3600帧）的长序列，系统在RTX 5090上实现**超过20×**的压缩比和**超过900 FPS**的实时渲染，突破了长视频动态场景建模的存储与实时性瓶颈。

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Layered_4D_Rotor_Ga/figures/012_Table_2.jpg]]
*Table 2: Quantitative results on the full SelfCap dataset. We evaluate our method and its compressed variants across all 6 scenes. All metrics are computed over the complete sequences and evaluated on an NVIDIA RTX 5090 GPU*

**Table 3**进一步验证了方法对不同视频时长的鲁棒性：随着序列长度增加，训练保持稳定，压缩质量未出现显著退化。

### 压缩组件消融

**Table 4**系统性地消融了各压缩组件的贡献。若直接对4D协方差矩阵进行矢量量化（Cov4D），PSNR仅**11.35** dB，存储高达29.03 MB，几何属性完全失效。引入**因子化协方差量化（FCQ）**后，PSNR跃升至**22.09** dB，同时存储降至**16.22 MB**——这是单组件中收益最大的改进，证明将协方差分解为尺度因子、归一化尺度、转子空间分量和转子时间分量分别量化是几何压缩的关键。叠加**分层压缩**后，PSNR进一步提升至**28.90** dB，细粒度结构得以保留。最后加入**残差码本量化（RCQ）**将PSNR推至**29.47** dB，存储微增至16.90 MB。

**Figure 6**从视觉上印证了这一递进式改进：直接VQ协方差（a）导致严重质量退化；FCQ（b）使几何压缩可行；分层结构（c）恢复更多细节；RCQ（d）提供额外增益。

### 码本尺寸与阈值消融

**Figure 4**展示了各VQ码本尺寸（1024至16384）对PSNR和存储的影响。存储随码本增大而增长，但**SH VQ码本**的扩大对质量-存储权衡（PSNR per MB）的收益最为显著，表明外观属性的精细量化对视觉保真度至关重要。**Figure 5**的VQ阈值消融显示，降低阈值会增加存储但提升保真度，同样SH VQ的阈值调整对质量-存储折中影响最大。

**Table 5**验证了RCQ码本尺寸在64至1024范围内的鲁棒性：PSNR和存储变化极小，说明残差码本的设计对超参数不敏感，方法具有较好的稳定性。

### 动态感知旋转学习率（DARLR）

**Figure 7**的定性对比揭示了DARLR策略的关键作用。在静态区域，不使用DARLR时纹理出现过平滑，高频结构丢失；启用DARLR后，静态区域的精细纹理得以保留，artifacts显著减少。其机理在于：对时间跨度大的高斯分配更小的旋转学习率，防止静态区域在训练中被过度扰动。

### 失败模式与局限性

尽管L4DRotorGS在压缩率和渲染速度上取得突破，论文明确指出**压缩过程仍然耗时**（compression process is still time-consuming），且当前框架**不支持在线训练**（online training），限制了其在流式捕捉场景（streaming capture）中的适应性。此外，该方法在更大规模场景或更复杂运动（如流体、烟雾）上的泛化性尚未验证，属于待探索的开放问题。

### 公平性说明

需注意以下评测差异：N3DV评测统一使用RTX 3090单卡，而SelfCap使用RTX 5090，硬件环境不同可能影响FPS对比。DyNeRF等NeRF方法训练时间极长（如DyNeRF需1344小时），而本文方法仅需约30分钟，但FPS对比存在数量级差距。部分早期方法（如†标注）仅在N3DV的Flame Salmon单场景上评测，全面性有限。

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Layered_4D_Rotor_Ga/figures/013_Table_3.jpg]]
*Table 3: Quantitative Results on diffenent video duration. Quantitative results across varying sequence lengths show that our training remains stable as duration increases*

![[assets/figures/papers/paper_list_l29_https_openaccess_thecvf_com_content_CVPR2026_html_Xu_Layered_4D_Rotor_Ga/figures/014_Table_4.jpg]]
*Table 4: Ablation of compression components. Quality improves progressively as components are added, with the largest gains from FCQ and the layered structure. The RCQ codebook size is set to 256*

## 定位与知识库关联

### 1. 沿革与基线关系

**L4DRotorGS** 处于动态神经视图合成（Dynamic NVS）从隐式辐射场向显式高斯泼溅演进的关键节点，其技术路线可沿两条主线追溯：

**动态 NeRF 基线。** 以 **DyNeRF**（Li et al., CVPR 2022）为代表的隐式方法在 N3DV 数据集上取得 PSNR 29.58，但需约 1344 小时训练，渲染帧率仅 0.015 FPS——这一性能瓶颈直接催生了动态场景的显式表示探索。

**动态高斯泼溅基线。** **4D-Rotor Gaussian Splatting**（4DGS, Duan et al., SIGGRAPH 2024）首次将 4D 旋转矩阵引入高斯泼溅框架，将 4D 协方差分解为 $\mathbf{R}_{4D} \mathbf{S}_{4D} \mathbf{S}_{4D}^T \mathbf{R}_{4D}^T$，实现了高质量动态建模。然而其 4D 高斯数量随视频时长线性增长，对长序列（如 60 秒 3600 帧）存储超 500 MB，无法实时渲染。

**长视频组织基线。** **Temporal Gaussian Hierarchy**（TGH, Xu et al., TOG 2024）率先采用固定时间分段方式将 4D 高斯分层，在段边界强制裁剪高斯，缓解了长视频的内存问题。但该方案存在两个结构性缺陷：段边界裁剪导致时域不连续，且所有层共用全局矢量量化（VQ）码本，忽略了不同时间跨度高斯的分布差异。

**L4DRotorGS 的核心改进**可概括为“继承-重构-压缩”三层递进：
- **继承**：沿用 4DGS 的 4D 旋量协方差参数化和 TGH 的分层组织思想；
- **重构**：将 TGH 的固定分段改为基于时间跨度的层-桶结构（layer-bucket），允许高斯跨越桶边界，每帧仅加载当前桶及邻桶，从根本上解耦了组织粒度与渲染开销；
- **压缩**：设计因子化协方差量化（FCQ）、分层压缩与残差码本量化（RCQ）三级压缩管线，将存储压缩 20 倍以上。

### 2. 关键技术差异（Changed Slots）

| 设计维度 | 基线方案 | L4DRotorGS 方案 | 因果机制 |
|---------|---------|----------------|---------|
| **时间组织** | TGH 固定分段，段边界裁剪高斯 | 层-桶结构：按时间跨度分层，桶内允许跨边界高斯 | 消除段间不连续，每帧可见高斯子集可控，实现 O(1) 帧级加载 |
| **协方差量化** | 直接对 4D 协方差矩阵 VQ（C3DGS 方式） | FCQ：分解为尺度因子、归一化尺度、转子空间分量、转子时间分量，分别 SQ/VQ | 将高维矩阵量化分解为四个低维子问题，PSNR 从 11.35 提升至 22.09（Table 4） |
| **压缩粒度** | 所有层共用全局码本 | 分层压缩：分布差异大的属性（尺度、转子分量）用层专属码本 | 利用各层高斯属性分布差异，PSNR 进一步提升至 28.90 |
| **码本精炼** | 每层单个 VQ 码本 | RCQ：层内分桶块，用轻量残差码本修正层全局码本 | 块级自适应修正提升压缩上限，码本尺寸在 64-1024 内鲁棒（Table 5） |
| **训练内存管理** | TGH 单 GPU 缓冲，频繁 CPU-GPU 传输 | 三缓冲策略：GPU 双缓冲 + CPU 桶缓冲 | 显著减少 CPU-GPU 拷贝开销，支撑自适应密度控制 |
| **旋转学习率** | 统一旋转学习率 | DARLR：时间跨度大的高斯分配更小旋转学习率 | 稳定静态区域训练，保留高频纹理（Figure 7） |

### 3. 适用边界与局限

**适用场景。** 方法在以下条件下表现最优：
- 长视频动态场景（10 秒至 60 秒以上），场景包含静态区域与局部运动；
- 需要高压缩率（>20×）与实时渲染（>500 FPS）的部署场景；
- 离线训练-在线推理模式（如已录制视频的自由视点回放）。

**已知局限。**
1. **压缩过程耗时**：论文明确指出“compression process is still time-consuming”，当前框架不支持在线训练（online training），限制了在流式捕捉场景（streaming capture）中的适应性。
2. **运动类型泛化性未验证**：实验集中在 N3DV（多视角捕捉的日常动作）和 SelfCap（自拍视频），对流体、烟雾等复杂非刚体运动的压缩性能缺乏定量证据。
3. **DARLR 手动调参**：动态感知旋转学习率依赖时间跨度启发式映射，缺乏自适应调整机制，可能在极端动静混合场景中需要手动干预。

### 4. 开放问题

1. **压缩加速与在线化**：能否通过渐进式量化或蒸馏策略将压缩过程加速至训练时间量级，实现在线训练？这是流式捕捉场景落地的关键瓶颈。
2. **大规模场景泛化**：层-桶结构在更大规模场景（如城市场景、多主体交互）中，层数 $L = \lceil\log_2 n\rceil + 1$ 的自动确定策略是否仍有效？压缩率上限是否会因场景复杂度提升而显著下降？
3. **DARLR 自适应化**：是否存在基于梯度统计或高斯时间跨度分布的自适应学习率调度方案，替代当前的手动映射？
4. **跨模态扩展**：FCQ 的因子化思想是否可迁移至 4D 高斯的外观属性（SH 系数）压缩，形成统一的因子化量化框架？

## 原文 PDF

![[paperPDFs/CVPR_2026/Layered_4D_Rotor_Gaussian_Splatting_A_Compressed_Representation_for_Long_Dynamic_Scenes.pdf]]
