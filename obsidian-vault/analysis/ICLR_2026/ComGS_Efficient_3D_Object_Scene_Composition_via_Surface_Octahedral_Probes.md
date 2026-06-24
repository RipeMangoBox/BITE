---
title: "ComGS: Efficient 3D Object-Scene Composition via Surface Octahedral Probes"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ComGS_Efficient_3D_Object_Scene_Composition_via_Surface_Octahedral_Probes_278056e7b7f4.pdf
project_link: "https://nju-3dv.github.io/projects/ComGS/"
code_link: null
aliases:
- ComGS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 表面八面体探针（SOPs）利用插值替代光线追踪，提供快速间接光照与遮挡查询；并将场景光照估计简化为物体放置位置的局部环境图修复问题。
primary_logic: 通过在物体表面附近放置可查询的八面体探针，高效缓存间接照明和遮挡，同时借助微调扩散模型从部分辐射场生成局部高动态范围（HDR）环境光照，从而在保持视觉和谐与合理阴影的同时，将编辑时间缩短至36秒，渲染速度达到约26 FPS。
claims:
- SOPs方案在SynCom数据集上实现24.282 PSNR和4.588和谐评分，编辑时间36秒，渲染26 FPS，大幅超越其他方法。
- 重建阶段训练时间仅需7.93分钟，相比IRGS (21.45 min) 提升超过2倍。
- SOPs通过KNN插值替代光线追踪，使重建效率提升至少2×，并在阴影渲染中保持实时性。
- 采用局部光照修复的扩散模型生成的环境图优于GS-IR和IRGS的全局解离，实现了多视角一致的照明。
---

# ComGS: Efficient 3D Object-Scene Composition via Surface Octahedral Probes

> [!tip] 核心洞察
> 通过在物体表面附近放置可查询的八面体探针，高效缓存间接照明和遮挡，同时借助微调扩散模型从部分辐射场生成局部高动态范围（HDR）环境光照，从而在保持视觉和谐与合理阴影的同时，将编辑时间缩短至36秒，渲染速度达到约26 FPS。

| 字段 | 内容 |
|------|------|
| 中文题名 | ComGS：基于表面八面体探针的高效三维物体-场景合成 |
| 英文题名 | ComGS: Efficient 3D Object-Scene Composition via Surface Octahedral Probes |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=yXiSPBMrTT) · [Project](https://nju-3dv.github.io/projects/ComGS/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ComGS |
| Dataset | SynCom, TensoIR |

> [!tip] 效果简介
> - SynCom 上，PSNR 24.282 (Ours SOPs) vs 22.877 (GI-GS) (+1.405)；SSIM 0.868 (Ours SOPs) vs 0.849 (GI-GS) (+0.019)；Harmony (MOS) 4.588 (Ours SOPs) vs 2.908 (GI-GS) (+1.680)。
> - TensoIR 上，Training Time 7.93 min vs 21.45 min (IRGS) (-13.52 min (~2.7x faster))；Relighting PSNR 30.474 vs 30.250 (IRGS) (+0.224)。

## 概述

**问题与瓶颈** 将三维物体真实地合成到高斯散射（3DGS）场景中，面临两大核心挑战：一是烘焙在辐射场中的外观与阴影导致合成不一致；二是现有基于高斯反渲染的方法（如 **IRGS**，Gu et al., 2025）依赖逐像素光线追踪来计算间接光照与遮挡，成为效率瓶颈。此外，完整场景的光照估计本身困难且视角不一致。

**核心思路** ComGS 提出 **表面八面体探针（SOPs）**——在物体表面附近自动放置一组可查询的探针，通过 KNN 插值替代昂贵的光线追踪，高效缓存间接照明和遮挡信息。同时，将场景光照估计重新定义为物体放置位置的局部环境图修复问题，利用微调的扩散模型从部分辐射场生成高动态范围（HDR）环境光照。

**方法定位** ComGS 属于三维物体-场景合成方法，与基于高斯反渲染的 **GS-IR**（Liang et al., 2024b）、**GI-GS**（Chen et al., 2025）和 **IRGS**（Gu et al., 2025）直接对标，但通过 SOPs 机制实现了效率与质量的显著突破。在光照估计方面，区别于全局场景解离（如 GS-IR）或单图像学习（如 **DiffusionLight**，Phongthawee et al., 2024），ComGS 聚焦局部环境图修复，获得多视角一致的照明结果。

**主要结果** 在 SynCom 数据集上，ComGS 以 24.282 PSNR 和 4.588 和谐评分大幅领先 GI-GS（22.877 PSNR，2.908 和谐），编辑时间仅需 36 秒，渲染速度达到约 26 FPS。重建阶段训练时间仅 7.93 分钟，相比 IRGS（21.45 分钟）提速超过 2.7 倍。SOPs 的 KNN 插值方案使重建效率至少提升 2 倍，并支持实时阴影计算。

**局限性** 方法假设待插入物体相对场景较小且场景主要为朗伯表面，因此无法处理远距离阴影和镜面反射（Figure 8）。当前不支持多物体同时放置，且依赖多视角输入而非单张图像。

## 背景与动机

### 3D 物体-场景合成的现实需求与核心挑战

在增强现实、虚拟制作和交互式内容创作中，将三维物体无缝融入真实或虚拟场景——即 **3D 物体-场景合成**——是一项基础且高频的需求。理想的合成结果需要同时满足三个条件：**视觉和谐**（物体与场景在光照、色调上自然融合）、**物理合理阴影**（物体向场景投射正确阴影，并接收场景的间接光照），以及**交互式实时性**（编辑后能够以高帧率自由漫游观察）。

近年来，基于高斯散射（3D Gaussian Splatting, 3DGS）的辐射场表示凭借其高保真度和实时渲染能力，成为场景重建与可视化的主流范式。然而，将 3DGS 直接应用于物体-场景合成面临一个根本性瓶颈：**3DGS 在重建过程中将复杂的外观效果（如阴影、间接光照）烘焙进高斯球参数中**，导致场景与物体的光照信息相互纠缠。当把重建好的物体插入新场景时，物体上残留的原始环境光照会与目标场景的光照条件产生冲突，造成视觉不和谐。

### 现有方法的效率与质量困境

为克服烘焙外观带来的合成不一致问题，研究者们将目光投向**基于逆渲染的高斯表示**。这类方法通过分解材质与光照，使物体能够在目标场景中被“重光照”。代表性工作包括：

- **GS-IR**（Liang et al., 2024b）和 **GI-GS**（Chen et al., 2025）：利用光线追踪对高斯点云进行遮挡和间接光照查询，实现物理基础重光照。
- **IRGS**（Gu et al., 2025）：进一步引入全局光照管线，在逆渲染框架下进行更完整的光照解离。

尽管这些方法在合成质量上取得了进展，但它们共享一个关键的效率瓶颈：**依赖逐像素或逐采样点的光线追踪来计算遮挡与间接光照**。在高斯点云中，光线追踪需要与数百万个高斯原语进行求交测试，计算代价极高。这导致两个后果：其一，重建阶段的训练时间长达数十分钟（IRGS 需约 21.45 分钟）；其二，编辑后的渲染帧率极低（GS-IR 仅约 2.11 FPS），远未达到实时交互的门槛。

与此同时，场景光照估计本身也是一个难题。现有方案要么试图对完整场景进行全局逆渲染（如 GS-IR），在复杂场景中往往不稳定；要么依赖单张图像学习光照（如 **DiffusionLight**, Phongthawee et al., 2024），却难以保证多视角一致性。**完整场景的光照估计不仅困难，而且在不同视角下容易产生不一致的结果**，这直接损害了合成物体的视觉和谐度。

### ComGS 的核心动机与突破思路

ComGS 的核心动机在于：**能否在保持物理合理光照与阴影的前提下，将物体-场景合成的效率提升到实时交互级别？**

本文的关键洞察是：**间接光照和遮挡在空间上具有局部平滑性，无需在每个着色点都进行昂贵的光线追踪**。基于这一观察，ComGS 提出了两个核心机制：

1. **表面八面体探针（Surface Octahedral Probes, SOPs）**：在物体表面附近放置一组可查询的探针，以八面体纹理缓存间接光照和遮挡信息。渲染时通过 KNN 插值直接查询，从而完全替代光线追踪，实现至少 2 倍的重建加速和实时阴影计算。

2. **局部光照估计的重构**：将场景光照估计从“完整场景逆渲染”简化为“物体放置位置的局部环境图修复”问题。通过在目标位置进行 360° 全景扫描获取部分辐射场，再借助微调扩散模型生成完整的高动态范围（HDR）环境图。这一策略避免了全局解离的不稳定性，同时保证了多视角光照一致性。

通过上述设计，ComGS 将编辑时间压缩至 **36 秒**，渲染速度达到 **约 26 FPS**，同时在 SynCom 数据集上取得了 **24.282 PSNR** 和 **4.588 和谐评分**，在合成质量与交互效率之间实现了此前方法未能达成的平衡。

## 核心创新

ComGS 针对三维物体-场景合成中的**效率-质量悖论**，提出了一套以**表面八面体探针（Surface Octahedral Probes, SOPs）**为核心的解决方案。其关键创新可归纳为三个相互耦合的 changed slots，分别对应重建、编辑与渲染阶段的瓶颈突破。

### 1. 间接光照与遮挡查询：从光线追踪到探针插值

现有高斯反渲染合成方法（如 **IRGS** (Gu et al., 2025)）在优化过程中依赖逐迭代的光线追踪来查询间接光照与遮挡，这构成了重建阶段的主要效率瓶颈。ComGS 的解决方案是引入 SOPs——在物体表面附近自动放置一组可查询的探针，每个探针以八面体纹理缓存其所在位置的间接光照与遮挡信息。

查询时，对于任意着色点 $\mathbf{x}$，通过 KNN 插值从邻近 SOP 获取间接光照：

$$L _ { i n } ( \mathbf { x } ) = \frac { \sum _ { k } w _ { s } ( k ) w _ { b } ( k ) \cdot L _ { i n } ( k ) } { \sum _ { k } w _ { s } ( k ) w _ { b } ( k ) }$$

SOPs 在优化开始时通过光线追踪初始化，随后在优化过程中作为可学习参数更新，从而**将耗时的光线追踪从每次迭代中剥离**。这一设计直接带来了至少 2 倍的重建加速——在 TensoIR 数据集上，ComGS 的训练时间仅为 7.93 分钟，而 IRGS 需要 21.45 分钟（Table 2）。

### 2. 场景光照估计：从全局逆渲染到局部环境图修复

传统方法（如 **GS-IR** (Liang et al., 2024b)）试图对完整场景进行逆渲染以解离光照，这在复杂场景中极易失败；而单图像学习方法（如 **DiffusionLight** (Phongthawee et al., 2024)）则面临多视角不一致的问题。ComGS 将问题重新表述为：**在物体放置位置，以重建好的三维高斯辐射场为条件，估计局部 HDR 环境图**。

具体而言，ComGS 在指定位置进行 360° 全景扫描，从高斯场景渲染出部分全景图（含 RGB、法线图和重建区域的 alpha 掩膜），然后利用微调后的 Stable Diffusion 模型将不完整的全景图修复为完整的 HDR 环境图。这一策略将光照估计从“理解整个场景”简化为“理解放置位置周围的环境”，显著提升了复杂场景下的光照一致性和质量（Figure 6）。

### 3. 阴影计算：从逐帧光线追踪到探针遮挡缓存

在合成阶段，物体插入场景后需要计算其投射的阴影。传统方法需逐帧对场景进行光线追踪以确定遮挡关系，这严重限制了实时渲染的可能性。ComGS 利用 SOPs 在编辑阶段**预计算并缓存物体诱导的遮挡 $O'$**——在物体放置区域的场景表面放置 SOPs，通过比较放置物体前后的辐射度变化来编码遮挡信息。

渲染时，阴影比率通过下式计算：

$$\mathscr { S } = \frac { L _ { o } ^ { \prime } } { L _ { o } }$$

其中 $L_o'$ 为含遮挡的辐射度，$L_o$ 为原始辐射度。由于遮挡已缓存在场景 SOPs 中，阴影计算退化为高效的插值查询，使得 ComGS 在保持合理阴影质量的同时实现约 26 FPS 的实时渲染，而同期最优的基线方法 GS-IR 仅能达到 2.11 FPS（Table 1）。

### 创新耦合效应

上述三个 changed slots 并非孤立存在，而是形成了正向反馈循环：SOPs 在重建阶段加速了逆渲染，其产出的高质量几何与材质又为编辑阶段的光照估计提供了更准确的条件；编辑阶段估计的环境图与缓存的遮挡信息，最终在渲染阶段通过统一的 SOPs 查询机制实现了实时重光照与阴影合成。整个编辑流程仅需 36 秒即可完成，在 SynCom 数据集上取得了 24.282 PSNR 和 4.588 和谐评分，较最优基线 GI-GS 分别提升 1.405 dB 和 1.680 分（Table 1）。

### 方法局限

需要指出，ComGS 的创新建立在若干假设之上：场景主要为朗伯表面（因此阴影计算采用漫反射近似），且待插入物体相对场景较小（仅影响局部区域）。这些假设使得方法在镜面反射场景和远距离阴影场景中失效（Figure 8），也限制了其对复杂 BRDF 效果的建模能力。

## 整体框架

ComGS 将三维物体-场景合成分解为**重建、编辑、渲染**三个顺序阶段，形成一条端到端的可微分流水线（图2）。其核心设计目标是在保持视觉和谐与物理合理阴影的同时，将编辑时间压缩至 36 秒、渲染帧率提升至约 26 FPS。

### 阶段一：重建

重建阶段对场景和物体采用**非对称处理策略**。对于场景，仅执行第一步——辐射场与几何重建，得到可渲染新视角的 2D 高斯辐射场。对于待插入物体，则完整执行两步：**第一步**从多视角图像重建辐射场与几何，通过可微分多目标渲染在单次前向中生成 G 缓冲区（颜色、深度、法线），其核心是 alpha 合成公式：

$$\mathcal { B } = \sum _ { i = 1 } ^ { N } T _ { i } \alpha _ { i } b _ { i } , \quad T _ { i } = \prod _ { j } ^ { i - 1 } ( 1 - \alpha _ { j } )$$

**第二步**进行材质与光照分解，引入表面八面体探针（SOPs）缓存间接光照与遮挡，结合环境图执行延迟物理基础渲染（PBR），从而获得可重光照的高斯物体。

### 阶段二：编辑

编辑阶段解决两个关键子问题——**场景光照估计**与**遮挡缓存**。光照估计被重新表述为物体放置位置的局部环境图修复问题：在目标位置进行 360° 全景扫描，获取部分 RGB 图像、法线图和 alpha 掩膜，随后利用微调扩散模型推断完整 HDR 环境图（图4）。遮挡缓存则利用场景 SOPs 在物体放置区域的场景表面预计算物体诱导的遮挡 $O'$，避免逐帧光线追踪，为后续实时阴影计算奠定基础。

### 阶段三：渲染

渲染阶段将重光照物体与场景进行深度合成。物体重光照采用蒙特卡洛重要性采样，基于估计的环境图和 SOPs 缓存的间接光照执行渲染方程：

$$L _ { o } ( \omega _ { o } , \mathbf { x } ) = \int _ { \Omega } f ( \omega _ { o } , \omega _ { i } , \mathbf { x } ) L _ { i } ( \omega _ { i } ) ( \omega _ { i } \cdot \mathbf { n } ) d \omega _ { i }$$

阴影计算则通过场景 SOPs 插值查询遮挡信息，利用阴影比率 $\mathscr { S } = \frac { L _ { o } ^ { \prime } } { L _ { o } }$ 对场景像素进行调制，实现实时阴影投射。

### 模块间的因果链路

流水线的效率瓶颈集中在间接光照与遮挡查询环节。现有高斯反渲染方法（如 **IRGS** (Gu et al., 2025)）依赖光线追踪高斯点云，每次优化迭代均需密集追踪，导致重建训练耗时 21.45 分钟。ComGS 的关键突破在于用 **SOPs 的 KNN 插值替代光线追踪**——SOPs 以光线追踪初始化后，在优化过程中通过插值查询间接光照 $L_{in}(\mathbf{x})$：

$$L _ { i n } ( \mathbf { x } ) = \frac { \sum _ { k } w _ { s } ( k ) w _ { b } ( k ) \cdot L _ { i n } ( k ) } { \sum _ { k } w _ { s } ( k ) w _ { b } ( k ) }$$

这一设计将重建训练时间缩短至 7.93 分钟（Table 2），提升超过 2.7 倍，同时使渲染帧率达到 26.14 FPS（Table 1）。SOPs 在场景空间的遮挡缓存可跨视角复用，进一步解耦了编辑效率与渲染质量的权衡。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/002_Figure_2.jpg]]
*Figure 2: Realistic 3D Object–Scene Composition Pipeline. Our approach consists of 3 stages: reconstruction (Sec. 3.1), where we reconstruct the Gaussian scene and relightable Gaussian object from multi-view images; editing (Sec. 3.2), where we estimate scene lighting and cache occlusion using Surface Octahedral Probes; and rendering (Sec. 3.3), where we perform splatting, object relighting, shadow casting, and depth compositing. The pipeline achieves visually harmonious results with realistic shadows and near-real-time performance*

## 核心模块与公式推导

ComGS 的流水线围绕三个关键模块展开：**表面八面体探针（SOPs）驱动的逆渲染**、**基于扩散模型的局部光照估计**，以及**基于 SOPs 的遮挡缓存与实时阴影合成**。以下逐一剖析各模块的核心机制与支撑公式。

---

### 3.1 多目标渲染与 G 缓冲区生成

ComGS 采用可微分多目标渲染，在单次前向 splatting 中生成 G 缓冲区（颜色、深度、法线、材质参数），为后续延迟物理基础渲染（PBR）提供输入。其核心为 alpha 合成公式：

$$
\mathcal { B } = \sum _ { i = 1 } ^ { N } T _ { i } \alpha _ { i } b _ { i } , \quad T _ { i } = \prod _ { j } ^ { i - 1 } ( 1 - \alpha _ { j } ) \tag{Eq. 1}
$$

其中 $\mathcal{B}$ 为累积的 G 缓冲区属性，$b_i$ 为第 $i$ 个高斯原语的属性（如法线、反照率），$\alpha_i$ 为不透明度，$T_i$ 为累积透射率。该公式将 2DGS 的 splatting 能力从颜色扩展到多通道属性，实现了几何与材质的统一提取。

---

### 3.2 表面八面体探针（SOPs）与高效间接光照查询

**核心瓶颈与解决方案**：传统高斯反渲染方法（如 IRGS）依赖逐迭代光线追踪计算间接光照与遮挡，成为效率瓶颈。ComGS 提出 SOPs 机制，将间接光照与遮挡信息缓存在物体表面附近的八面体探针中，通过 KNN 插值替代光线追踪，使重建效率提升至少 2 倍。

**探针放置与查询**：SOPs 在物体表面附近自动放置，每个探针存储八面体纹理形式的间接光照 $L_{in}$ 和遮挡 $O$。对于着色点 $\mathbf{x}$，间接光照通过邻近探针的加权插值获得：

$$
L _ { i n } ( \mathbf { x } ) = \frac { \sum _ { k } w _ { s } ( k ) w _ { b } ( k ) \cdot L _ { i n } ( k ) } { \sum _ { k } w _ { s } ( k ) w _ { b } ( k ) } \tag{Eq. 9}
$$

其中 $w_s(k)$ 为空间距离权重，$w_b(k)$ 为方向权重，$L_{in}(k)$ 为第 $k$ 个邻近探针在查询方向上的间接光照值。该插值机制避免了逐采样点的光线追踪，是效率提升的关键。

**初始化与优化**：SOPs 纹理通过 2D 光线追踪初始化，随后在逆渲染优化中联合更新。探针沿表面法线偏移物体大小的 1% 以防止光线泄漏（消融实验验证该偏移量最优）。

---

### 3.3 延迟物理基础渲染

从 G 缓冲区出发，ComGS 采用延迟着色计算 PBR 颜色。着色点 $\mathbf{x}$ 的出射辐射度由渲染方程描述：

$$
L _ { o } ( \omega _ { o } , \mathbf { x } ) = \int _ { \Omega } f ( \omega _ { o } , \omega _ { i } , \mathbf { x } ) L _ { i } ( \omega _ { i } ) ( \omega _ { i } \cdot \mathbf { n } ) d \omega _ { i } \tag{Eq. 6}
$$

其中 $f$ 为 BRDF，$L_i(\omega_i)$ 为入射辐射度，$\mathbf{n}$ 为表面法线。实际计算采用蒙特卡洛重要性采样：

$$
\mathcal { C } _ { p b r } ( \mathbf { x } ) = \frac { 2 \pi } { S _ { r } } \sum _ { i } ^ { S _ { r } } f ( \omega _ { o } , \omega _ { i } , \mathbf { x } ) L _ { i } ( \omega _ { i } ) ( \omega _ { i } \cdot \mathbf { n } )
$$

其中 $S_r$ 为采样数。入射辐射度 $L_i(\omega_i)$ 由直接光照与环境图、间接光照（来自 SOPs 插值）和遮挡调制组合而成：

$$
L _ { i } ( \omega _ { i } ) = ( 1 - O ( \omega _ { i } ) ) L _ { d i r } ( \omega _ { i } ) + L _ { i n } ( \omega _ { i } ) \tag{Eq. 8}
$$

该分解将光照解耦为直接项（受遮挡调制）与间接项，分别由环境图和 SOPs 纹理提供。

---

### 3.4 基于扩散模型的局部光照估计

**问题重定义**：完整场景光照估计本身困难且视角不一致。ComGS 将其简化为物体放置位置的局部环境图修复问题——在指定位置进行 360° 全景扫描，获得部分 RGB 图像、法线图和 alpha 掩膜，然后利用微调的 Stable Diffusion 模型补全为完整 HDR 环境图。

**关键设计**：八面体纹理作为环境图表示，具有低畸变和近似均匀的纹素面积，便于定义重要性采样的概率密度函数（PDF）。消融实验表明，引入法线图作为扩散模型的几何引导可进一步降低光照估计的尺度不变 RMSE 和角度误差。

---

### 3.5 遮挡缓存与实时阴影合成

**阴影计算瓶颈**：传统方法需逐帧光线追踪计算物体投射的阴影。ComGS 在编辑阶段将物体诱导的遮挡 $O'$ 缓存到放置区域附近的场景 SOPs 中，渲染时通过插值查询遮挡值。

**阴影合成公式**：在朗伯假设下，放置物体前后的出射辐射度之比即为阴影比率：

$$
\mathscr { S } = \frac { L _ { o } ^ { \prime } } { L _ { o } } \tag{Eq. 17}
$$

其中 $L_o' = f_d \int L_i(\omega_i) (1 - O'(\omega_i)) (\omega_i \cdot \mathbf{n}) d\omega_i$ 为含遮挡的出射辐射度，$L_o \approx f_d \int L_i(\omega_i) (\omega_i \cdot \mathbf{n}) d\omega_i$ 为原始辐射度。该比率直接乘到场景渲染结果上，实现实时阴影效果。消融实验显示，10k 个 SOPs 配合 16×16 纹理分辨率即可提供视觉可接受的阴影质量。

---

### 3.6 模块协同与效率闭环

三个核心模块形成效率闭环：SOPs 将间接光照与遮挡查询从光线追踪转为插值（重建加速 2 倍以上），扩散模型将光照估计从全局逆渲染简化为局部修复（编辑时间 36 秒），遮挡缓存使阴影计算从逐帧光线追踪转为插值查询（渲染达 26 FPS）。这一协同设计是 ComGS 在保持视觉和谐的同时实现近实时性能的根本原因。

### 补充图表

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/003_Figure_3.jpg]]
*Figure 3: Inverse Rendering with Surface Octahedral Probes (SOPs). We utilize trained relightable 2D Gaussians to generate GBuffers via splatting, followed by deferred physically based rendering for a render image. Illumination is split into direct lighting from environment map, indirect lighting and occlusion captured by textures in SOPs. Both the environment map and textures are stored as octahedral textures. Low-discrepancy ray sampling with random rotation is used to compute illumination at shading point, with indirect light and occlusion derived via KNN interpolation from nearby probes. SOPs are initialized with ray tracing and optimized under its guidance, avoiding intensive ray tracing per opt...*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/004_Figure_4.jpg]]
*Figure 4: Lighting Estimation. At a given location, we create a partial panoramic view via a*

## 实验与分析

### 核心性能对比

ComGS 在 SynCom 合成数据集上进行了全面的定量与定性评估，对比方法涵盖图像合成方法（**DiffHarmony** (Zhou et al., 2024)、**ZeroComp** (Zhang et al., 2025)）、三维物体合成方法（**MV-CoLight** (Ren et al., 2025)）以及高斯反渲染合成方法（**GS-IR** (Liang et al., 2024b)、**GI-GS** (Chen et al., 2025)、**IRGS** (Gu et al., 2025)）。

Table 1 汇总了 SynCom 上的合成性能。ComGS 的 SOPs 方案在客观指标上达到 24.282 PSNR 和 0.868 SSIM，分别比次优方法 **GI-GS**（22.877 / 0.849）提升 +1.405 dB 和 +0.019。在主观指标上，SOPs 的和谐评分（Harmony MOS）达到 4.588，显著高于 GI-GS 的 2.908（提升 +1.680），3D 一致性评分 4.563 同样领先。效率方面，SOPs 方案以 26.14 FPS 的渲染帧率大幅超越所有对比方法（GS-IR 为 2.11 FPS），编辑时间仅需 36.12 秒。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/005_Table_1.jpg]]
*Table 1: Composition Performance on SynCom Dataset. Objective metrics (PSNR, SSIM), subjective metrics (3D consistency, Con.; harmony, Harm.), and efficiency metrics (editing time, FPS) are reported*

ComGS 同时报告了基于光线追踪的变体 Ours (Trace)，其 PSNR 略高（24.567），但渲染帧率降至 4.02 FPS，体现了 SOPs 以微小质量代价换取约 6.5 倍渲染加速的权衡。

### 重建效率与精度

在 TensoIR 数据集上的重建性能对比（Table 2）显示，ComGS 以 7.93 分钟完成训练，相较于 **IRGS** 的 21.45 分钟实现约 2.7 倍加速，验证了 SOPs 替代光线追踪带来的效率提升。重光照 PSNR 达到 30.474，与 IRGS（30.250）持平，新视角合成 PSNR 为 35.822，反照率 PSNR 为 31.683。在 SynCom-Obj 物体重建数据集上（Table 4），ComGS 同样以超过 2 倍的效率优势达到与 SOTA 相当的精度。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/008_Table_2.jpg]]
*Table 2: Reconstruction performance on TensoIR. Our method achieves accuracy comparable to SOTA approaches with at least 2× efficiency improvement*

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/023_Table_4.jpg]]
*Table 4: Quantitative results on the SynCom-Obj dataset. Our method achieves accuracy comparable to the state of the art while delivering over 2× higher efficiency*

### 光照估计消融

Table 6 展示了光照估计模块的关键消融结果：

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/033_Table_6.jpg]]
*Table 6: Ablations on Lighting Estimation. Performance improves with higher mask coverage, and incorporating the normal map enhances lighting estimation by providing explicit geometric cues*

- **场景覆盖度**：掩膜有效区域从 40–60% 提升至 80–100% 时，尺度不变 RMSE 从 0.066 降至 0.052，角度误差同步减小。这表明更完整的场景重建为扩散模型提供了更充分的几何与外观先验。
- **法线图输入**：在扩散模型中引入法线图后，RMSE 和角度误差均有小幅改善，验证了几何线索对光照估计的正向引导作用。

Figure 6 的定性对比进一步表明，**GS-IR** 和 **IRGS** 在复杂场景中估计的环境图出现明显偏差，**DiffusionLight** (Phongthawee et al., 2024) 在不同视角间缺乏一致性，而 ComGS 的局部光照修复策略产生了多视角一致的 HDR 环境图。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/007_Figure_6.jpg]]
*Figure 6: Environment Maps Comparison. GS-IR and IRGS fail in complex scenes, DiffusionLight is viewpointinconsistent, while our method yields superior and consistent results*

### SOPs 配置与阴影质量

SOPs 数量与纹理分辨率直接影响阴影渲染质量（Figure 15）。16×16 的纹理分辨率可提供视觉可接受的结果，而 8×8 分辨率因角度采样过粗导致明显方向误差。SOPs 数量超过 10k 后可进一步减少锯齿。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/019_Figure_15.jpg]]
*Figure 15: Influence of the Number of SOPs and Texture Resolution. A resolution of 16 provides visually acceptable results, while a resolution of 8 causes significant directional errors due to coarse angular sampling. Increasing the number of SOPs beyond 10k further reduces aliasing*

SOPs 初始化偏移的消融（Table 5、Figure 20）揭示了光线泄漏问题的敏感性：偏移设为物体大小的 0% 时出现显著光线泄漏，1% 的设置则可获得干净稳定的反照率、渲染和重光照结果。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/031_Figure_20.jpg]]
*Figure 20: Comparison of relighting and ambient occlusion (AO) under different SOPs initialization offsets. The 0% offset introduces noticeable light leakage, while the 1% setting produces clean and stable results*

GPU 显存占用方面（Table 3），SOPs 数量从约 2k 增至 10k 时，显存开销增长可控，验证了该方案在实时渲染场景下的部署可行性。

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/018_Table_3.jpg]]
*Table 3: GPU memory usage comparison under different numbers of SOPs*

### 失败模式与适用边界

ComGS 存在以下明确失败模式（Figure 8）：

![[assets/figures/papers/paper_list_l27_https_openreview_net_forum_id_yXiSPBMrTT/figures/010_Figure_8.jpg]]
*Figure 8: Failure cases. We failed to cast remote shadow and model mirrorlike reflections*

1. **远距离阴影缺失**：当物体放置位置远离场景表面时，SOPs 缓存的局部遮挡无法覆盖远距离阴影投射，导致阴影不完整。
2. **镜面反射不支持**：场景重建基于 2DGS，缺乏镜面光照模型，无法建模镜面反射和类镜面效果。

这些失败根源于方法的核心假设：待插入物体相对场景较小、仅影响局部区域，且场景表面近似为朗伯面。在镜面反射场景或需要远距离阴影的合成任务中，需手动验证替代方案。

## 方法谱系与知识库定位

### 1. 任务定位与核心挑战

ComGS 定位于**三维物体-场景合成**（3D object–scene composition）这一任务：从多视角图像出发，将可重光照的物体自然地插入到已重建的场景辐射场中，并生成视角一致、光照和谐且带有合理阴影的合成结果。该任务的核心瓶颈在于：高斯散射（Gaussian Splatting, GS）辐射场中烘焙的外观与阴影在物体-场景合成时会产生不一致；现有基于高斯反渲染的方法依赖耗时的光线追踪进行遮挡与间接光照计算，成为效率瓶颈；而完整场景光照估计本身困难且视角不一致。

### 2. 方法谱系与基线对比

ComGS 的基线方法覆盖了从二维图像合成到三维高斯反渲染的多种技术路线，可归纳为以下四类：

#### 2.1 图像域合成方法
此类方法在二维图像空间进行物体-场景融合，不涉及三维表示的重建与重光照。代表性工作包括 **DiffHarmony**（Zhou et al., 2024）和 **ZeroComp**（Zhang et al., 2025）。它们的优势在于无需三维重建，但难以保证多视角一致性，且无法处理场景光照变化与物体阴影的物理正确性。

#### 2.2 三维物体合成方法
**MV-CoLight**（Ren et al., 2025）将合成问题提升至三维空间，尝试在物体插入时联合优化光照一致性。然而，该方法仍受限于光照估计的精度与计算效率，难以在复杂场景中生成物理可信的阴影。

#### 2.3 高斯反渲染合成方法
这是与 ComGS 最直接相关的技术路线，通过在 GS 框架内进行逆渲染来解耦材质与光照，进而实现物体重光照与场景合成：

- **GS-IR**（Liang et al., 2024b）：采用全局场景逆渲染估计环境光照，但光照解离的精度在复杂场景中下降明显，且渲染效率有限。
- **GI-GS**（Chen et al., 2025）：引入全局光照近似，在合成质量上有所提升，但编辑时间与渲染帧率仍远低于实时要求。
- **IRGS**（Gu et al., 2025）：通过光线追踪高斯点云来计算间接光照与遮挡，在 TensoIR 数据集上取得了当时最优的重光照精度，但**光线追踪成为效率瓶颈**——其重建训练时间高达 21.45 分钟，且编辑阶段的光照查询无法满足实时渲染需求。

ComGS 针对 IRGS 的效率瓶颈进行了**因果性干预**：将间接光照与遮挡查询从昂贵的光线追踪替换为**表面八面体探针（SOPs）的 KNN 插值**，在保持可比精度的同时实现了 2 倍以上的效率提升。

#### 2.4 学习式光照估计方法
**DiffusionLight**（Phongthawee et al., 2024）利用扩散模型从单张图像估计全景 HDR 环境图，但该方法**视角不一致**——不同视角的估计结果差异显著，无法直接用于多视角一致的三维合成。

ComGS 继承了扩散模型的光照先验，但将问题重新表述为：**在物体放置位置，以已重建的三维高斯辐射场为条件，进行局部环境图修复**。这一重新表述将全局光照估计简化为局部补全问题，并通过微调 Stable Diffusion 实现了多视角一致的 HDR 环境光照估计。

#### 2.5 逆渲染重建方法
在重建阶段，ComGS 与经典逆渲染方法形成对比：**NeRFactor**、**InvRender**、**TensoIR**（Jin et al., 2023）和 **R3DG**（Gao et al., 2024）等基于神经辐射场或高斯散射的逆渲染方法，通常需要完整的光线追踪或体积渲染来解耦材质、几何与光照。ComGS 在重建阶段采用两阶段策略——先进行辐射场与几何重建，再进行材质与光照解耦——并在第二阶段引入 SOPs 替代光线追踪，从而在 TensoIR 数据集上以 7.93 分钟完成训练（对比 IRGS 的 21.45 分钟），同时重光照 PSNR 达到 30.474，与 IRGS 的 30.250 可比。

### 3. 关键设计决策与因果机制

ComGS 的四个关键设计决策构成了其性能优势的因果链：

| 设计决策 | 被替代的基线方案 | 因果效应 |
|---------|----------------|---------|
| SOPs KNN 插值替代光线追踪 | IRGS 的光线追踪高斯点云 | 重建效率提升 ≥2×，渲染达 26 FPS |
| 局部环境图修复替代全局光照估计 | GS-IR 的全局解离 / DiffusionLight 的单图估计 | 多视角一致光照，和谐评分 +1.68 |
| SOPs 缓存物体诱导遮挡 | 逐帧光线追踪阴影计算 | 实时阴影渲染 |
| 八面体纹理环境图替代低阶球谐 | 球谐光照 / 简单环境图 | 高动态范围与重要性采样支持 |

### 4. 适用边界与局限性

ComGS 的方法论建立在以下假设之上，这些假设划定了其适用边界：

1. **局部影响假设**：待插入物体相对场景较小，仅影响场景的局部区域。这一假设使得 SOPs 的放置与遮挡缓存策略可行，但也导致**无法处理远距离阴影**（如物体远离场景表面时的投影）。
2. **朗伯表面假设**：场景表面被近似为朗伯反射，以简化阴影计算中的渲染方程。这使得 ComGS **无法支持镜面反射场景**，也不适用于需要精确模拟复杂 BRDF 效果的场景。
3. **单物体顺序插入**：当前方法不支持同时放置多个物体；多物体放置需顺序重建，可能增加耗时。此外，物体材质编辑需手工调整。
4. **多视角重建依赖**：方法依赖于多视角图像输入进行场景与物体的重建，不直接支持单张图像输入。

### 5. 开放问题与未来方向

ComGS 框架为后续研究留下了若干明确的改进空间：

- **自适应 SOP 放置**：当前采用启发式均匀放置策略。探索自适应策略有望以更少的探针达到更高保真度，并降低内存占用。
- **增量 SOP 更新**：对于移动物体，设计高效的增量 SOP 更新策略仍具挑战性，是动态场景合成的重要方向。
- **单图像三维合成**：将方法扩展至仅用单张图像进行三维合成，将大幅降低数据获取门槛。
- **放宽朗伯假设**：引入更复杂的 BRDF 模型和间接光照效果（如镜面反射、散焦模糊），可提升物理真实感。
- **实时全局光照集成**：结合实时全局光照技术，有望进一步提升镜面反射和复杂光传输的保真度。

## 原文 PDF

![[paperPDFs/ICLR_2026/ComGS_Efficient_3D_Object_Scene_Composition_via_Surface_Octahedral_Probes_278056e7b7f4.pdf]]