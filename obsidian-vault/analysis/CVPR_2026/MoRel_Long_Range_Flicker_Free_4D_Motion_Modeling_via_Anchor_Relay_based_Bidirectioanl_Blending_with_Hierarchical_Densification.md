---
title: "MoRel: Long-Range Flicker-Free 4D Motion Modeling via Anchor Relay-based Bidirectioanl Blending with Hierarchical Densification"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MoRel_Long_Range_Flicker_Free_4D_Motion_Modeling_via_Anchor_Relay_based_Bidirectioanl_Blending_with_Hierarchical_Densification.pdf
project_link: "https://cmlab-korea.github.io/MoRel/"
code_link: null
aliases:
- MoRel
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 关键帧锚点（Key-frame Anchor, KfA）的周期性放置与可学习时间不透明度引导的双向变形混合机制。通过将长序列划分为以KfA为中心的局部规范空间，学习双向变形，并利用可学习的衰减权重实现相邻锚点影响的无缝过渡，从而打破了块间不连续性，在限定内存下恢复了时间一致性。
primary_logic: 将长距离动态场景建模分解为“锚点接力”与“双向混合”两个阶段：首先训练全局规范锚点（GCA）以提供一致初始化，然后派生周期性的KfA作为各段时间的局部规范空间，并通过渐进式窗口化双向变形训练（PWD）独立优化每个KfA的变形场，最后在中间帧混合（IFB）阶段学习可学习的时间不透明度控制，使相邻锚点的影响平滑过渡，彻底消除块边界的闪烁。此外，利用特征方差指导的分层密度化（FHD）根据频率特性智能控制锚点增长，在高频区保留细节并在低频区抑制冗余，从而在保持重建质量的同时显著降低内存占用。
claims:
- MoRel在SelfCapLR数据集上取得了最低的tOF得分（0.203），远优于全量训练和分块方法，证明了其出色的时间一致性。
- MoRel在PSNR/SSIM/LPIPS指标上全面超越对比方法，在长序列上实现了最佳的重建质量。
- MoRel的训练内存占用恒定（约6 GB），而全量方法随帧数增加而内存爆炸；渲染时仅需126 MB，支持按需加载。
- 定性对比（图6）显示MoRel在快速运动、遮挡区域和长距离场景下均能保持无闪烁的视觉质量，而其他方法产生模糊或伪影。
---

# MoRel: Long-Range Flicker-Free 4D Motion Modeling via Anchor Relay-based Bidirectioanl Blending with Hierarchical Densification

> [!tip] 核心洞察
> 将长距离动态场景建模分解为“锚点接力”与“双向混合”两个阶段：首先训练全局规范锚点（GCA）以提供一致初始化，然后派生周期性的KfA作为各段时间的局部规范空间，并通过渐进式窗口化双向变形训练（PWD）独立优化每个KfA的变形场，最后在中间帧混合（IFB）阶段学习可学习的时间不透明度控制，使相邻锚点的影响平滑过渡，彻底消除块边界的闪烁。此外，利用特征方差指导的分层密度化（FHD）根据频率特性智能控制锚点增长，在高频区保留细节并在低频区抑制冗余，从而在保持重建质量的同时显著降低内存占用。

| 字段 | 内容 |
|------|------|
| 中文题名 | MoRel：基于锚点接力的双向混合与分层精化实现长程无闪烁4D运动建模 |
| 英文题名 | MoRel: Long-Range Flicker-Free 4D Motion Modeling via Anchor Relay-based Bidirectioanl Blending with Hierarchical Densification |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Kwak_MoRel_Long-Range_Flicker-Free_4D_Motion_Modeling_via_Anchor_Relay-based_Bidirectioanl_CVPR_2026_paper.html) · [Project](https://cmlab-korea.github.io/MoRel/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MoRel |
| Dataset | SelfCapLR |

> [!tip] 效果简介
> - SelfCapLR (五个长序列，超3500帧) 上，平均 PSNR↑ / SSIM↑ / LPIPS↓ 21.00 / 0.664 / 0.355 vs 最佳对比方法（见表1） (在所有序列中均取得最优或次优)。
> - SelfCapLR 上，tOF (↓) 0.203 vs 其他方法（无具体数值） (最低（最佳时间一致性）)；训练峰值内存 (MB) ~6,000 vs 全量方法（OOM 或更高） (有界恒定，不随帧数增长)；渲染内存 (MB) 126 vs 未报告 (低内存占用，支持随机访问)。

## 概述

长序列动态场景的4D重建是沉浸式媒体与视觉计算的核心挑战。现有基于**4D Gaussian Splatting (4DGS)**（Wu et al., CVPR 2024）的方法在建模长距离动态视频时面临三个结构性瓶颈：（1）全量联合训练（all-at-once）需将所有帧加载至GPU，内存随序列长度线性增长直至溢出；（2）分块训练（chunk-based）虽缓解了内存压力，却破坏了时间连续性，在块边界产生闪烁伪影与外观突变；（3）每个块仅能观测有限时间窗口，无法重建新出现的遮挡区域，导致场景完整性下降。这些瓶颈共同构成了长程4D运动建模中“内存-时间一致性-重建质量”的不可能三角。

针对上述困境，MoRel提出了**锚点接力双向混合（Anchor Relay-based Bidirectional Blending, ARBB）**机制。其核心洞察是将长序列动态建模分解为“接力”与“混合”两个协同阶段：首先训练全局规范锚点（Global Canonical Anchor, GCA）为整个序列提供一致初始化，随后在关键帧时间索引处派生周期性的关键帧锚点（Key-frame Anchor, KfA），形成各段时间的局部规范空间；每个KfA在其时间邻域内独立学习前向与后向双向变形场，最后通过可学习的时间不透明度控制，使相邻锚点的影响平滑过渡，从根本上消除块边界的闪烁。此外，**特征方差引导的分层密度化（Feature-variance-guided Hierarchical Densification, FHD）**根据GCA特征方差将锚点分配至不同频率级别，在训练早期优先稳定低频区域，后期逐步细化高频细节，从而在保持重建质量的同时显著抑制锚点冗余，降低内存占用。

在实验层面，MoRel在自建的长序列基准**SelfCapLR**（超3500帧）上取得了全面的领先表现：平均PSNR/SSIM/LPIPS达到21.00 dB / 0.664 / 0.355，在所有序列中均为最优或次优（Table 1）；时间一致性指标tOF降至0.203，为所有对比方法中最低（Table 2）；训练内存恒定维持在约6 GB，不随帧数增长，渲染时仅需126 MB并支持按需加载（Table 2, Table 3）。定性对比进一步显示，MoRel在快速运动、遮挡区域和长距离场景下均能保持无闪烁的视觉质量，而全量训练与分块训练方法则分别遭遇内存溢出与块边界伪影（Figure 6）。消融实验证实，KfA局部规范空间的引入、双向变形与可学习不透明度混合、以及FHD分层密度化策略，三者各自对区域一致性、时间平滑性和内存效率产生了决定性贡献（Table 3）。

综上，MoRel通过ARBB与FHD的协同设计，在限定内存下首次实现了长序列4D运动建模的时间一致性与高保真重建，为长视频动态场景表示提供了新的基线范式。

## 背景与动机

### 长程4D动态场景建模的兴起与瓶颈

从多视角视频中重建随时间变化的三维场景——即4D动态场景建模——是计算机视觉与图形学领域的前沿课题。近年来，以**4D Gaussian Splatting (4DGS)** (Wu et al., CVPR 2024) 为代表的方法将3D Gaussian Splatting的高效渲染能力拓展到时域，通过为每个高斯点学习时变属性（如变形场或时空特征）来实现动态场景的逼真重建。然而，这些方法在设计之初主要面向**短序列**（通常数百帧）场景，当面对**长距离动态视频**（数千帧甚至更长）时，其核心假设与工程实现暴露出根本性的局限。

现有方法在处理长序列时，主要面临三条路径的困境，这在Figure 1和Figure 2中得到了直观的对比：

1. **全量联合训练的“内存爆炸”**：最直接的方式是将所有帧的数据同时加载到GPU中进行联合优化（Figure 1a）。这种方法虽然能保持全局时间一致性，但其GPU内存占用随序列长度**线性增长**。对于超过3500帧的长序列，即便高端GPU也会遭遇**内存溢出（OOM）**，导致训练根本无法完成。此外，单一全局模型对长序列中复杂多变的运动模式的表达能力也趋于饱和。

2. **分块独立训练的“时间撕裂”**：为缓解内存压力，分块策略（chunk-based）将长序列切分为若干短片段独立训练（Figure 1b），如**GIFStream** (Li et al., CVPR 2025) 和**V3** (Wang et al., TOG 2024)。这虽然控制了单次训练的内存开销，却引入了一个致命缺陷：**块间时间连续性的断裂**。由于每个块仅在其局部时间窗口内优化，相邻块在边界帧上缺乏协调，导致渲染视频在块切换处产生明显的**闪烁伪影（temporal flickering）**和外观突变，严重损害视觉体验。

3. **遮挡区域的“重建盲区”**：无论是全量还是分块方法，在长序列中都面临一个更深层的几何挑战。随着相机和场景中物体的持续运动，大量原本被遮挡的区域会逐渐显露。分块训练中，单个块观察到的视角极其有限，无法积累足够的多视图线索来重建这些新出现的表面，导致场景完整性下降，产生空洞或模糊。

### 核心矛盾与本文动机

上述困境揭示了长程4D运动建模中的一对核心矛盾：**如何在严格有界的内存开销下，实现跨越数千帧的无闪烁时间一致性重建？** 全量方法追求一致性却牺牲了可扩展性，分块方法追求可扩展性却牺牲了一致性。现有工作在二者之间缺乏一个有效的平衡机制。

此外，即使某些分块方法尝试通过重叠窗口或后处理平滑来缓解边界闪烁，它们仍然面临**随机访问能力缺失**的问题——即无法高效地独立渲染任意时刻的帧，而必须顺序加载整个块。这限制了其在交互式应用中的潜力。

### MoRel的破局思路

针对上述瓶颈，MoRel提出了一种根本性的范式转换：**不再将长序列视为一个整体或一组孤立的片段，而是将其建模为一组周期性放置的“锚点”之间的接力与平滑过渡。** 这一思想被具体化为**锚点接力双向混合（Anchor Relay-based Bidirectional Blending, ARBB）**机制（Figure 1c, Figure 2e）。

其核心动机在于：
- **用“锚点接力”打破内存壁垒**：通过在关键帧位置设置可动态加载/卸载的局部规范锚点（Key-frame Anchor, KfA），使训练和渲染时的内存占用始终有界，与序列总长度解耦。
- **用“双向混合”缝合时间裂缝**：学习相邻锚点之间的双向变形场，并通过**可学习的时间不透明度控制**实现相邻锚点影响的平滑过渡，从机制上根除块边界闪烁。
- **用“分层密度化”平衡效率与细节**：引入**特征方差引导的分层密度化（FHD）**，根据场景的频率特性智能分配锚点生长预算，在高频区保留细节、在低频区抑制冗余，进一步压缩内存占用而不牺牲重建质量。

通过这些设计，MoRel旨在首次实现长程4D动态场景的**内存有界、时间一致、支持随机访问**的高质量建模。

## 核心创新

MoRel 的核心创新在于将长距离动态场景建模分解为“锚点接力”与“双向混合”两个阶段，通过四个关键设计打破了现有 4DGS 方法在内存效率与时间一致性之间的根本矛盾。以下从四个 changed slots 展开分析。

### 1. 训练策略与时间建模：锚点接力双向混合（ARBB）

现有方法面临两难困境：全量联合训练（如 **4D Gaussian Splatting** (Wu et al., CVPR 2024)、**Deformable 3D Gaussians** (Yang et al., CVPR 2024)）将全部帧加载至 GPU，导致内存随序列长度线性增长并最终溢出；分块训练（如 **GIFStream** (Li et al., CVPR 2025)、**V3** (Wang et al., TOG 2024)）虽缓解了内存压力，却破坏了时间连续性，在块边界产生闪烁伪影和外观突变。

MoRel 提出的 ARBB 策略从根本上改变了这一范式：它将长序列划分为以关键帧锚点（Key-frame Anchor, KfA）为中心的局部规范空间，每个 KfA 仅负责其时间邻域内的变形建模，相邻 KfA 的影响通过可学习的时间不透明度平滑过渡。这一设计使训练内存有界（约 6 GB 恒定，不随帧数增长），同时彻底消除了块间不连续性。

### 2. 变形方向与混合机制：双向变形 + 可学习时间不透明度

传统方法通常采用单向变形或无显式跨块混合，难以处理遮挡区域的时域连续性。MoRel 的核心机制体现在两个层面：

**渐进窗口双向变形（PWD）**：每个 KfA 在其双向变形窗口（BDW）内独立学习前向和后向变形场，以滑动窗口方式渐进训练，防止块间干扰。这使得每个锚点能够从两个时间方向理解运动，为后续混合提供互补的变形信息。

**中间帧混合（IFB）与可学习时间不透明度**：在变形场固定后，IFB 阶段学习每个锚点的时间不透明度控制参数。具体而言，第 $n$ 个 KfA 中锚点 $k$ 在方向 $\mathrm{dir}$ 上的混合权重由下式给出：

$$w _ { n , k } ^ { \mathrm { d i r } } = \exp [ - \lambda _ { \mathrm { d e c a y } } \cdot d _ { n , k } ^ { \mathrm { d i r } } \cdot \vert \tau _ { n } - o _ { n , k } ^ { \mathrm { d i r } } \vert ]$$

其中 $\lambda_{\mathrm{decay}}$ 为基础衰减系数，$d_{n,k}^{\mathrm{dir}}$ 为锚点特有的衰减速度，$o_{n,k}^{\mathrm{dir}}$ 为时间偏移。这一机制使相邻 KfA 的影响随帧索引自然衰减与过渡，从数学上保证了混合的平滑性。

### 3. 内存管理：按需动态加载/卸载

MoRel 的内存效率不仅源于分阶段训练，更依赖于精细的按需加载策略。在训练和渲染过程中，系统仅同时保留最多两个 KfA 及其对应的变形场，其余锚点按需动态加载与卸载。这一设计使得渲染时仅需 126 MB 内存，且支持随机访问任意帧，解决了现有方法在长序列部署中的实用性问题。

### 4. 密度化策略：特征方差引导的分层密度化（FHD）

传统均匀梯度驱动的密度化策略在高频区域易产生冗余锚点，在低频区域则可能不稳定。MoRel 的 FHD 策略通过两个步骤实现质量与效率的平衡：

**方差基分级**：在 GCA 训练后，根据每个锚点的特征方差 $\sigma_k^2$ 和分位数阈值 $\tau_1, \tau_2$ 将其分为三个频率级别：

$$L _ { a _ { k } ^ { \mathrm { G l o b a l } } } = \left\{ \begin{array} { l l } { 0 , } & { \sigma _ { k } ^ { 2 } < \tau _ { 1 } } \\ { 1 , } & { \tau _ { 1 } \leq \sigma _ { k } ^ { 2 } < \tau _ { 2 } } \\ { 2 , } & { \sigma _ { k } ^ { 2 } \geq \tau _ { 2 } } \end{array} \right.$$

**层级密度化权重**：在 KfA 和 PWD 训练期间，对级别 $L$ 的锚点施加时间调制权重：

$$w _ { L } ^ { j _ { n } ^ { s } } = \left\{ \begin{array} { l l } { 1 , } & { L = 0 } \\ { \lambda _ { L } + ( 1 - \lambda _ { L } ) \eta _ { t } , } & { L \geq 1 } \end{array} \right.$$

低频级别（$L=0$）始终获得完整梯度更新，确保早期稳定；高频级别（$L \geq 1$）的权重从 $\lambda_L$ 线性增长至 1，在训练后期才充分细化。消融实验证实，FHD 将渲染内存从高水平降至 126 MB，同时不损害重建质量。

### 创新点之间的因果关联

上述四个创新并非孤立存在，而是形成了一条因果链条：ARBB 的锚点接力架构为双向变形和混合提供了结构基础；PWD+IFB 的双向混合机制是消除闪烁的直接手段；FHD 通过频率感知的密度化进一步压缩了内存，使整个系统在长序列上可部署；按需加载则确保了训练和推理的内存有界性。这一系统性设计使得 MoRel 在 SelfCapLR 数据集上取得了最低的 tOF 得分（0.203）和最优的重建质量，同时保持恒定的训练内存占用。

## 整体框架

MoRel 的整体框架围绕“锚点接力–双向混合”（Anchor Relay–based Bidirectional Blending, ARBB）策略构建，将长序列动态场景建模分解为两个阶段、四个训练步骤，在恒定内存预算下实现时间一致的 4D 运动重建。

### 两阶段流水线

如图 3 所示，MoRel 的训练流程分为 **锚点接力阶段（Anchor Relay Phase）** 和 **双向混合阶段（Bidirectional Blending Phase）**。两个阶段串行执行，前一阶段的输出作为后一阶段的初始化，形成从全局一致到局部精细的递进式建模路径。

**锚点接力阶段** 负责构建一组在时间轴上周期性分布的局部规范空间。首先，利用全部帧训练一个 **全局规范锚点（Global Canonical Anchor, GCA）**，以单一全局点云为整个序列提供一致的几何与外观初始化，并基于锚点的特征方差为其分配频率级别。随后，从级别分配后的 GCA 出发，在关键帧时间索引处派生 **关键帧锚点（Key-frame Anchor, KfA）**，每个 KfA 在其时间邻域内优化形成局部规范空间，同时应用特征方差引导的分层密度化（FHD）进行精细化。

**双向混合阶段** 解决相邻锚点影响域之间的过渡问题。该阶段包含两个训练步骤：**渐进窗口化双向变形训练（Progressive Windowed Deformation, PWD）** 和 **中间帧混合训练（Intermediate Frame Blending, IFB）**。PWD 在每个 KfA 的双向变形窗口内独立学习前向和后向变形场，以滑动窗口方式渐进训练，防止跨块干扰；IFB 则固定锚点几何与变形场，仅训练可学习的时间不透明度控制参数，使相邻 KfA 的渲染结果在重叠区域平滑过渡，从根本上消除块边界闪烁。

### 模块间数据流与依赖关系

框架中各模块之间存在严格的输入输出依赖，形成一条从粗到细的信息流：

1. **GCA 训练 → KfA 训练**：GCA 训练完成后，其输出的级别分配锚点集 $\widetilde{\mathcal{A}}^{\text{Global}}$ 作为所有 KfA 的统一初始化。这一设计确保了不同 KfA 之间在几何结构和外观特征上的全局一致性，避免分块训练中常见的区域割裂。

2. **KfA 训练 → PWD 训练**：每个 KfA 经 FHD 细化后，其锚点位置与特征被冻结，作为 PWD 阶段学习双向变形场的局部规范空间。PWD 在每个 KfA 的双向变形窗口内独立运行，各窗口之间无梯度交互，从而将内存占用限制在单个窗口规模。

3. **PWD 训练 → IFB 训练**：PWD 完成后，所有 KfA 的变形场被固定。IFB 阶段每次加载相邻的两个 KfA 及其变形场，仅训练时间不透明度控制参数（包括每个锚点的衰减速度 $d_{n,k}^{\text{dir}}$ 和时间偏移 $o_{n,k}^{\text{dir}}$），不更新锚点属性或变形网络。这种“冻结–微调”策略保证了混合训练不会破坏已学到的运动表征。

4. **FHD 的跨阶段嵌入**：FHD 并非独立阶段，而是嵌入在 KfA 训练和 PWD 训练过程中。它利用 GCA 阶段预分配的频率级别，在密度化时对梯度施加层级权重 $w_L^{j_n^s}$——低频级别（$L=0$）始终保留完整梯度，高频级别（$L \geq 1$）的权重从 $\lambda_L$ 线性增长至 1。这一机制使训练早期优先稳定低频结构，后期逐步细化高频细节，在控制锚点数量的同时保持重建质量。

### 内存管理机制

MoRel 实现有界内存的核心在于按需动态加载/卸载策略。训练和渲染时，系统仅在 GPU 显存中同时保留最多两个 KfA 及其关联的变形场。当训练窗口滑动或渲染时间戳跨越 KfA 边界时，系统卸载不再需要的锚点并加载新的锚点。这一设计使训练峰值内存恒定在约 6 GB，渲染内存仅需 126 MB，且支持任意时间戳的随机访问渲染。

### 与现有范式的对比定位

图 2 从概念层面比较了 MoRel 与现有 4DGS 方法的长程建模能力。全量训练方法（如 **4D Gaussian Splatting** (Wu et al., CVPR 2024)、**Deformable 3D Gaussians** (Yang et al., CVPR 2024)）需将所有帧同时加载到内存，导致显存随序列长度线性增长直至溢出。分块训练方法（如 **GIFStream** (Li et al., CVPR 2025)、**V3** (Wang et al., TOG 2024)）通过独立训练各块缓解内存压力，但破坏了时间连续性，在块边界产生闪烁伪影。MoRel 的 ARBB 策略通过 KfA 接力与双向不透明度混合，在保持有界内存的同时恢复了跨块的时间一致性，并天然支持随机访问——这是分块方法难以实现的系统特性。

### 补充图表

![[assets/figures/papers/paper_list_l34_https_openaccess_thecvf_com_content_CVPR2026_html_Kwak_MoRel_Long_Range/figures/003_Figure_3.jpg]]
*Figure 3: Overview of MoRel framework. To efficiently model long-range 4D motion with bounded memory and temporal consistency, MoRel adopts the Anchor Relay-based Bidirectional Blending (ARBB) strategy composed of four training stages which are organized into two phases. In the Anchor Relay phase (Sec. 3.2), a GCA is first trained on entire frames with a single point cloud. Next, each KfA is derived around its key-frame time index, while its spatial detail is enhanced through FHD (Sec. 3.4). In the Bidirectional Blending phase (Sec. 3.3), PWD training stage is executed to learn bidirectional deformation fields within local temporal windows to ensure robust motion modeling of each anchor. Finally, in...*

![[assets/figures/papers/paper_list_l34_https_openaccess_thecvf_com_content_CVPR2026_html_Kwak_MoRel_Long_Range/figures/001_Figure_1.jpg]]
*Figure 1: Approaches for modeling long-range 4D Motion. (a) The all-at-once training experiences memory overflow and even suffers 14 from limited representational capacity. (b) The chunk-based training mitigates the memory overflow but causes temporal flickering at chunk boundaries, substantially degrading visual quality. In contrast, (c) our Anchor Relay-based Bidirectional Blending (ARBB) approach successfully maintains both representation quality and temporal consistency by smoothly transiting the influence of each Key-frame Anchor (KfA). The rendered patches, frame-wise tOF [2], and temporal profile provide strong evidence for the effectiveness of our method*

![[assets/figures/papers/paper_list_l34_https_openaccess_thecvf_com_content_CVPR2026_html_Kwak_MoRel_Long_Range/figures/002_Figure_2.jpg]]
*Figure 2: Conceptual comparison of existing 4DGS methods in modeling long-range 4D motion. (a) All-at-once approaches suffer from high memory usage, while (b) chunk-based methods inevitably fail to maintain temporal consistency. Even advanced variants struggle with system applicability such as a random accessibility. Our ARBB framework resolves all these issues, achieving bounded memory and temporally coherent long-range modeling*

## 核心模块与公式推导

MoRel 的核心架构由四个训练阶段构成，分别解决长程 4D 运动建模中的初始化一致性、局部规范空间构建、变形场学习与跨块混合问题。以下按训练流程逐一解析关键模块及其数学机制。

### 3.1 全局规范锚点（GCA）训练

**动机**：若直接为每个关键帧独立初始化锚点，各局部空间将缺乏全局一致性，导致后续混合阶段难以对齐。GCA 训练阶段的目标是以极低的计算代价为整个序列提供一个统一的锚点初始化。

**机制**：使用 COLMAP 从所有帧提取的稀疏点云构建单一全局点云，作为全局规范锚点 $A^{\mathrm{Global}}$ 的初始位置。GCA 在全部帧上进行轻量训练，仅优化锚点的位置、特征与不透明度等属性，不涉及时间变形。训练完成后，每个锚点 $a_k^{\mathrm{Global}}$ 获得一个特征向量 $\hat{f}_k$，其方差 $\sigma_k^2$ 将作为后续分层密度化的依据（见 3.4 节）。

**设计意图**：GCA 提供的是“场景平均”表示，虽无法捕捉精细时变细节，但为所有后续 KfA 提供了共享的几何与外观先验，是锚点接力机制的基础。

### 3.2 关键帧锚点（KfA）训练

**动机**：单一 GCA 无法表达长序列中的大幅运动与遮挡变化。KfA 训练阶段将长序列划分为以关键帧时间索引 $\tau_n$ 为中心的局部段，每个段拥有独立的锚点集 $\bar{A}_n^{\mathrm{Key}}$，形成局部规范空间。

**初始化**：所有 $\bar{A}_n^{\mathrm{Key}}$ 均从已完成频率级别分配的全局锚点 $\widetilde{A}^{\mathrm{Global}}$ 初始化，确保各局部空间之间具有结构对应性。关键帧的间隔由 GOP（Group of Pictures）参数控制，决定了锚点接力密度与内存占用的权衡。

**训练**：每个 KfA 在其时间邻域内独立优化，仅观察属于该邻域的帧。此阶段的密度化受 FHD 策略调制（见 3.4 节），在保持全局一致性的前提下逐步增强局部细节。

### 3.3 渐进窗口化双向变形（PWD）训练

**瓶颈分析**：若对每个 KfA 的变形场进行全窗口联合训练，相邻 KfA 的变形窗口会产生重叠区域，导致梯度冲突与块间干扰，破坏时间连续性。

**PWD 策略**：如图 4(c) 所示，每个 KfA 在其双向变形窗口（Bidirectional Deformation Window, BDW）内独立优化前向和后向变形场。训练以滑动窗口方式渐进进行：先训练早期 KfA 的变形场，待其收敛后再推进至下一 KfA，相邻窗口之间无梯度交互。这从根本上消除了块间干扰，同时确保训练内存仅需容纳单个 KfA 及其变形场。

**变形方向**：每个 KfA 学习两个方向的变形——前向变形（从 $\tau_n$ 向未来帧映射）和后向变形（从 $\tau_n$ 向过去帧映射）。双向设计使得每个时间点的渲染可同时参考前后两个锚点空间，为后续混合提供冗余信息。

### 3.4 中间帧混合（IFB）训练

**核心问题**：PWD 训练后，每个 KfA 的变形场在其 BDW 内是准确的，但在窗口边界处，相邻 KfA 的渲染结果直接切换会产生闪烁伪影。IFB 阶段通过可学习的时间不透明度控制实现相邻锚点影响的平滑过渡。

**混合机制**：对于时间 $\tau$ 处的渲染，IFB 联合加载两个相邻 KfA（$\bar{A}_n^{\mathrm{Key}}$ 和 $\bar{A}_{n+1}^{\mathrm{Key}}$），分别通过各自的变形场渲染，再按时间不透明度加权混合。关键公式为：

$$w_{n,k}^{\mathrm{dir}} = \exp\left[-\lambda_{\mathrm{decay}} \cdot d_{n,k}^{\mathrm{dir}} \cdot \left|\tau_n - o_{n,k}^{\mathrm{dir}}\right|\right]$$

其中：
- $w_{n,k}^{\mathrm{dir}}$：第 $n$ 个 KfA 中锚点 $k$ 在方向 $\mathrm{dir} \in \{\mathrm{fwd}, \mathrm{bwd}\}$ 上的时间衰减权重
- $\lambda_{\mathrm{decay}}$：全局基础衰减系数
- $d_{n,k}^{\mathrm{dir}}$：锚点 $k$ 特有的可学习衰减速度，控制该锚点影响随时间的衰减快慢
- $o_{n,k}^{\mathrm{dir}}$：锚点 $k$ 特有的可学习时间偏移，决定该锚点影响力峰值的时间位置
- $\tau_n$：第 $n$ 个 KfA 的关键帧时间索引

**训练细节**：IFB 阶段冻结所有锚点的几何、外观与变形场参数，仅优化每个锚点的 $d_{n,k}^{\mathrm{dir}}$ 和 $o_{n,k}^{\mathrm{dir}}$。这种解耦设计使得混合权重的学习不会干扰已建立的变形场质量。

**效果**：通过为每个锚点赋予独立的时间偏移和衰减速度，相邻 KfA 的影响力可在时间轴上形成平滑的接力过渡，彻底消除块边界的视觉闪烁。

### 3.5 特征方差引导的分层密度化（FHD）

**动机**：标准 3DGS 的梯度驱动密度化策略在 4D 场景中存在两难：高频区域（如运动边界、精细纹理）需要密集锚点以恢复细节，但全局统一密度化会导致低频平坦区域产生冗余锚点，浪费内存并可能引入不稳定。

**方差分级**：GCA 训练完成后，计算每个锚点 $a_k^{\mathrm{Global}}$ 的特征方差 $\sigma_k^2$，并基于分位数阈值 $\tau_1, \tau_2$ 分配层级：

$$L_{a_k^{\mathrm{Global}}} = \begin{cases}
0, & \sigma_k^2 < \tau_1 \quad \text{(低频)} \\
1, & \tau_1 \leq \sigma_k^2 < \tau_2 \quad \text{(中频)} \\
2, & \sigma_k^2 \geq \tau_2 \quad \text{(高频)}
\end{cases}$$

直觉上，特征方差反映了该锚点所在局部区域的外观变化复杂度——纹理丰富或运动剧烈的区域方差高，平坦均匀区域方差低。

**层级调制密度化**：在 KfA 和 PWD 训练的第 $j_n^s$ 次迭代中，层级 $L$ 的锚点梯度累积被加权：

$$w_L^{j_n^s} = \begin{cases}
1, & L = 0 \\
\lambda_L + (1 - \lambda_L)\eta_t, & L \geq 1
\end{cases}$$

其中 $\eta_t \in [0,1]$ 为训练进度（从 0 线性增长至 1），$\lambda_L$ 为层级特定的初始权重（高频层级 $\lambda_L$ 较小）。该设计的效果是：
- **低频锚点**（$L=0$）：权重始终为 1，早期即可充分密度化以稳定场景主体结构
- **高频锚点**（$L \geq 1$）：早期权重低（$\approx \lambda_L$），抑制密度化以避免噪声干扰；后期权重逐渐增至 1，在结构稳定后精细化高频细节

**内存收益**：FHD 通过抑制低频区域的冗余锚点生成，显著降低了最终锚点总数。消融实验（Table 3）表明，FHD 将渲染内存从无 FHD 变体的高水平降至 126 MB，同时保持重建质量不降。

### 3.6 内存管理策略

MoRel 的内存有界性源于两个层面的设计：
- **训练阶段**：通过动态加载/卸载机制，任意时刻仅保留最多两个 KfA 及其变形场在 GPU 内存中，训练峰值内存约 6 GB，不随序列帧数增长
- **渲染阶段**：按需加载目标时间点所需的 KfA 和变形场，渲染内存仅 126 MB，支持随机时间点访问

### 补充图表

![[assets/figures/papers/paper_list_l34_https_openaccess_thecvf_com_content_CVPR2026_html_Kwak_MoRel_Long_Range/figures/004_Figure_4.jpg]]
*Figure 4: Comparison of training strategies for modeling longrange 4D motion with bidirectional deformation. (a) All-at-53 once training suffers from memory overflow. (b) Chunk-wise training reduces memory cost but causes inter-chunk interference. (c) Our Bidirectional Blending (PWD + IFB) maintains bounded memory and prevents inter-chunk interference*

![[assets/figures/papers/paper_list_l34_https_openaccess_thecvf_com_content_CVPR2026_html_Kwak_MoRel_Long_Range/figures/005_Figure_5.jpg]]
*Figure 5: Overview of Feature-variance-guided Hierarchical Densification. (a) Variance-based Leveling: After GCA training, we assign a level to each anchor-point guided by the featurevariance. (b) Level-wise Densification: During the KfA and PWD trainings, gradients for KfA densification are modulated by levelspecific weights, enabling early low-frequency stabilization and late high-frequency refinement*

## 实验与分析

### 实验设置

MoRel 在作者构建的 **SelfCapLR** 数据集上进行评估。该数据集包含 5 个长序列，总计超过 3500 帧，平均运动幅度显著大于现有基准，专门用于检验方法在长程 4D 运动建模中的能力。评估指标涵盖重建质量与时间一致性两个维度：PSNR、SSIM、LPIPS 衡量逐帧渲染保真度，**tOF**（连续帧间光流差异）衡量时序一致性。

对比方法分为两组：
- **全量训练方法**：4D Gaussian Splatting（Wu et al., CVPR 2024）、Deformable 3D Gaussians（Yang et al., CVPR 2024）、Spacetime Gaussian Feature Splatting（Li et al., CVPR 2024）。
- **分块训练方法**：GIFStream（Li et al., CVPR 2025）、V3（Wang et al., TOG 2024）。

所有方法使用相同的训练/测试序列划分和评价指标。需注意，全量方法由于内存溢出无法处理完整长序列，评估可能在某些序列上受限（原文未详细说明，需手动核实）。

### 主实验结果

#### 重建质量

Table 1 展示了 SelfCapLR 上的定量对比。MoRel 在所有序列上取得了最优或次优的 PSNR/SSIM/LPIPS 指标（平均 21.00 dB / 0.664 / 0.355），全面超越全量训练与分块训练方法。全量方法因 GPU 内存限制无法扩展到完整长序列，而分块方法虽然缓解了内存问题，但在块边界引入了视觉伪影，导致重建质量下降。

![[assets/figures/papers/paper_list_l34_https_openaccess_thecvf_com_content_CVPR2026_html_Kwak_MoRel_Long_Range/figures/006_Table_1.jpg]]
*Table 1: Quantitative results comparison on our newly composed SelfCapLR. Group denotes (a) all-at-once training methods, (b) chunk-based approaches including our unidirectional deformation variant, and (c) our MoRel model. Red and blue denote the best and second-best performances, respectively. Each block element of 3-performance denotes (PSNR (dB)↑ / SSIM↑ / LPIPS↓)*

#### 时间一致性与内存效率

Table 2 聚焦于长程运动建模的关键瓶颈指标。MoRel 取得了最低的 **tOF 得分 0.203**，远优于全量训练和分块方法，证明了 ARBB 机制在消除块边界闪烁方面的有效性。在内存方面，MoRel 的训练峰值内存保持恒定约 6 GB，不随序列长度增长；而全量方法随帧数增加内存爆炸甚至溢出。渲染时 MoRel 仅需 **126 MB**，支持按需动态加载，实现了随机访问能力。

![[assets/figures/papers/paper_list_l34_https_openaccess_thecvf_com_content_CVPR2026_html_Kwak_MoRel_Long_Range/figures/008_Table_2.jpg]]
*Table 2: Metrics critical to long-range motion modeling. We highlight the key factors that determine a model’s capability in long-range motion handling*

#### 定性分析

Figure 6 的定性对比显示，MoRel 在快速运动、遮挡区域和长距离场景下均能保持无闪烁的视觉质量，而其他方法在这些挑战性区域产生模糊或伪影。ARBB 机制通过可学习时间不透明度控制实现了相邻 KfA 影响的无缝过渡，从根本上避免了分块方法中常见的块边界突变。

![[assets/figures/papers/paper_list_l34_https_openaccess_thecvf_com_content_CVPR2026_html_Kwak_MoRel_Long_Range/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison on SelfCapLR. Our MoRel demonstrates superior visual fidelity in long-range motion modeling compared to existing SOTA methods, thanks to its ARBB mechanism that effectively handles long-range 4D motion*

### 消融实验

Table 3 系统验证了 MoRel 各组件的贡献：

![[assets/figures/papers/paper_list_l34_https_openaccess_thecvf_com_content_CVPR2026_html_Kwak_MoRel_Long_Range/figures/007_Table_3.jpg]]
*Table 3: Ablation studies on MoRel components. Each row evaluates the impact of a specific design choice. Yellow-green cells highlight configurations with substantial gain*

**锚点接力机制（ARBB）**：引入 KfA 形成局部规范空间（变体 b vs 基线 a）显著提升了区域一致性和运动保真度。这验证了将长序列分解为以关键帧锚点为中心的局部建模单元的有效性。

**双向变形与可学习不透明度混合**：将双向变形与 IFB 混合（变体 d/e）与单向变形变体（变体 c）对比，前者有效消除了块边界的闪烁，tOF 指标大幅改善。公式 $w _ { n , k } ^ { \mathrm { d i r } } = \exp [ - \lambda _ { \mathrm { d e c a y } } \cdot d _ { n , k } ^ { \mathrm { d i r } } \cdot \vert \tau _ { n } - o _ { n , k } ^ { \mathrm { d i r } } \vert ]$ 中的可学习参数（衰减速度 $d$ 和时间偏移 $o$）使每个锚点能自适应控制混合程度，这是消除块间不连续性的关键。

**特征方差引导的分层密度化（FHD）**：变体 e（含 FHD）与无 FHD 变体对比，FHD 在不损害重建质量的前提下将渲染内存从高水平降至 126 MB。FHD 通过 GCA 特征方差将锚点分为三个频率级别（低频/中频/高频），并在训练过程中对不同级别施加时间调制权重 $w _ { L } ^ { j _ { n } ^ { s } }$——低频级别始终为 1 以早期稳定，高频级别从 $\lambda_L$ 线性增加至 1 以后期细化，从而在保持高频细节的同时抑制低频区域的冗余锚点增长，实现了质量与效率的平衡。

### 失败模式与局限

原文未明确报告失败案例。以下为基于方法设计的潜在局限，需手动验证：
- FHD 依赖基于分位数阈值 $\tau_1, \tau_2$ 的全局方差分级，不同场景可能需要调整阈值以获得最优密度化效果。
- 方法需要 COLMAP 进行相机参数估计和稀疏点云初始化，在无已知相机或相机估计失败的长视频场景下适用性受限。
- 当前评估限于 SelfCapLR 数据集（超 3500 帧），在更长视频（如数小时）或极端相机运动下的泛化性尚未验证。

## 方法谱系与知识库定位

### 1. 在4D动态场景建模谱系中的位置

MoRel锚定在**基于高斯泼溅（Gaussian Splatting）的动态场景新视角合成**这一快速发展的技术线上。该线路上承3D Gaussian Splatting（3DGS）的显式点云表示，下接时间维度的变形建模，核心挑战在于如何在有限计算资源下捕捉长距离、大范围的运动。

**全量训练范式**的代表性工作包括：
- **4D Gaussian Splatting (4DGS)** (Wu et al., CVPR 2024)：将3D高斯推广到4D时空域，联合优化所有帧的表示。其根本性瓶颈在于GPU内存随序列长度线性增长，在长序列（如超过3500帧）上必然触发内存溢出（OOM），丧失了处理长程运动的基本能力。
- **Deformable 3D Gaussians** (Yang et al., CVPR 2024) 与 **Spacetime Gaussian Feature Splatting** (Li et al., CVPR 2024)：采用规范空间加变形场的方式建模动态，同样受限于全量加载策略，内存瓶颈未解。

**分块训练范式**试图通过将长序列切分为独立训练的块来绕过内存限制，代表性工作包括：
- **GIFStream** (Li et al., CVPR 2025)：流式处理动态场景，分块独立优化。
- **V3** (Wang et al., TOG 2024)：视频体积表示的分块训练。

这类方法的致命缺陷在于**破坏了时间连续性**：每个块仅观察其局部时间窗口，块与块之间缺乏任何信息交互或约束，导致块边界处产生显著的**闪烁伪影（temporal flickering）**和外观突变。此外，每个块无法感知其时间窗口之外的场景变化，对于新出现的遮挡区域完全无法重建，场景完整性受损。

MoRel的**锚点接力双向混合（Anchor Relay-based Bidirectional Blending, ARBB）** 策略在两者之间开辟了第三条路径：它既不像全量方法那样将所有帧同时驻留在内存中，也不像分块方法那样粗暴地割裂时间轴。其核心洞见是将长序列建模分解为“锚点接力”与“双向混合”两个协同阶段——首先训练全局规范锚点（GCA）为整个序列提供一致的初始化，然后派生周期性的关键帧锚点（KfA）作为各段的局部规范空间，通过渐进式窗口化双向变形训练（PWD）独立优化每个KfA的变形场，最后在中间帧混合（IFB）阶段学习可学习的时间不透明度控制，使相邻锚点的影响平滑过渡。这一设计在保持内存有界的同时，从机制层面消除了块边界的闪烁。

### 2. 方法适用边界

**适用条件**：
- 需要已知相机参数和稀疏点云初始化（依赖COLMAP），目前无法直接处理无相机标定的野外视频。
- 训练和推理均假设场景动态可被周期性的KfA局部规范空间所覆盖，即运动在相邻KfA之间具有可变形性，而非完全拓扑变化。
- 长序列中的关键帧间隔（GOP大小）需要手动设定，不同场景可能需要不同的最佳设置。

**不适用或需谨慎使用的场景**：
- 极端的相机运动（如快速旋转、剧烈抖动）可能超出COLMAP的稳健估计能力，导致初始化失败。
- 数小时级别的超长视频：虽然内存有界，但KfA数量和变形场的累积存储量仍会线性增长，且GOP设置与训练效率之间的权衡需要进一步探索。
- 场景拓扑发生剧烈变化（如物体频繁出现/消失、大范围遮挡-去遮挡），FHD的频率级别分配基于GCA特征方差，可能无法自适应地捕捉这些突变。

### 3. 局限与开放问题

**已知局限**：
- 特征方差引导的分层密度化（FHD）依赖全局分位数阈值 $\tau_1, \tau_2$ 来划分频率级别，这些阈值可能需要针对不同场景进行调参，缺乏自适应的阈值选择机制。
- 方法整体依赖COLMAP的稀疏重建质量，在纹理稀疏或运动模糊严重的区域，初始化点云可能不足，影响后续锚点优化。

**开放问题**：
1. **更极端的运动与更长视频**：MoRel能否处理更极端的相机运动或更长的视频（如数小时），以及在这种场景下GOP的最佳设置策略是什么？是否存在自适应的GOP选择机制？
2. **阈值自适应**：FHD的频率级别划分阈值是否可以通过场景统计量自动确定，而非依赖手动调参？
3. **无相机场景扩展**：能否将ARBB框架与自监督的相机位姿估计方法（如DUSt3R、MASt3R等）结合，扩展到无需已知相机的场景？
4. **跨任务迁移**：学习到的双向变形场和可学习时间不透明度控制机制，能否应用于其他需要时间一致性的任务，如视频插帧、视频压缩或动态场景的语义编辑？
5. **渲染效率**：当前渲染时仅需126 MB内存，支持按需加载和随机访问，但渲染速度（FPS）是否满足实时应用需求，原文未提供详细数据，需要进一步验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/MoRel_Long_Range_Flicker_Free_4D_Motion_Modeling_via_Anchor_Relay_based_Bidirectioanl_Blending_with_Hierarchical_Densification.pdf]]
