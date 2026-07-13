---
title: "Geo2: Geometry-Guided Cross-view Geo-Localization and Image Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Geo2_Geometry_Guided_Cross_view_Geo_Localization_and_Image_Synthesis.pdf
project_link: "https://fobow.github.io/geo2.github.io/"
code_link: null
aliases:
- Geo2
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将地面和卫星图像分别通过GeoMap嵌入到共享的3D感知潜在空间，利用VGGT提取的几何先验，并通过GeoFlow流匹配模型实现从单方向训练到双向合成的能力。
primary_logic: 通过将几何基础模型的3D先验融入到统一的共享潜在空间中，能够同时改进跨视角地理定位和双向图像合成，两个任务可以相互增强。
claims:
- Geo2在VIGOR同区域上实现R@1 81.59%，显著超过之前最佳模型
- Geo2在CVACT验证集上达到R@1 94.36%，展现卓越定位能力
- Geo2在CVACT地面到卫星合成任务上取得FID 31.72, LPIPS 0.552，优于所有对比方法
- Geo2在CVUSA跨数据集测试中，R@1达到63.17%，泛化能力强
---

# Geo2: Geometry-Guided Cross-view Geo-Localization and Image Synthesis

> [!tip] 核心洞察
> 通过将几何基础模型的3D先验融入到统一的共享潜在空间中，能够同时改进跨视角地理定位和双向图像合成，两个任务可以相互增强。

| 字段 | 内容 |
|------|------|
| 中文题名 | Geo2: 几何引导的跨视角地理定位与图像合成 |
| 英文题名 | Geo2: Geometry-Guided Cross-view Geo-Localization and Image Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_Geo2_Geometry-Guided_Cross-view_Geo-Localization_and_Image_Synthesis_CVPR_2026_paper.html) · [Project](https://fobow.github.io/geo2.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Geo2 |
| Dataset | VIGOR Same-Area, VIGOR Cross-Area, CVACT Val, CVACT Test |

> [!tip] 效果简介
> - VIGOR Same-Area 上，R@1 81.59 vs 77.86 (Sample4Geo) (+3.73)。
> - VIGOR Cross-Area 上，R@1 66.71 vs 61.70 (Sample4Geo) (+5.01)。
> - CVACT Val 上，R@1 94.36。

## 概要

跨视角地理空间学习（cross-view geo-spatial learning）的两大核心任务——跨视角地理定位（CVGL）与跨视角图像合成（CVIS）——长期面临一个共同瓶颈：地面全景图像与俯视卫星图像之间存在巨大的视角差异，导致现有方法难以在统一的表示空间中有效对齐两类模态。直接应用几何基础模型（Geometric Foundation Models, GFMs），如 VGGT，虽能提供丰富的 3D 几何先验，却因跨视角图像的严重畸变与视点偏移而无法提取准确的几何特征（见 Figure 1），这构成了本工作的核心动机。

针对上述瓶颈，Geo2 提出了一条因果路径：**将几何基础模型的 3D 先验融入一个共享的 3D 感知潜在空间，从而同时驱动 CVGL 与双向 CVIS，并使两个任务相互增强**。具体而言，Geo2 通过 GeoMap 双分支模块将地面与卫星特征映射到统一的几何感知嵌入空间，并利用 GeoFlow 流匹配（flow matching）模型实现仅需单方向训练即可完成双向图像合成。这一设计使得几何定位的判别性特征与图像生成的生成能力在共享表示中形成正向反馈。

在实验验证层面，Geo2 在多个标准基准上取得了显著优势：
- 在 VIGOR 同区域设置下，R@1 达到 **81.59%**，较此前最佳模型 Sample4Geo（Deuser et al., ICCV 2023）提升 **+3.73 个百分点**；跨区域设置下 R@1 达到 **66.71%**（+5.01 个百分点）。
- 在 CVACT 验证集上，R@1 达到 **94.36%**，展现出卓越的定位精度。
- 在 CVACT 地面到卫星合成任务上，FID 降至 **31.72**，LPIPS 为 **0.552**，均优于所有对比方法。
- 跨数据集泛化测试中（CVUSA→CVACT），R@1 达到 **63.17%**，表明框架具备较强的域迁移能力。

在方法谱系与知识库定位上，Geo2 区别于现有工作的关键点在于其**统一性与双向性**。传统 CVGL 方法（如 **SAFA**（Shi et al., NeurIPS 2019）、**TransGeo**（Zhu et al., CVPR 2022）、**GeoDTR+**（Zhang et al., TPAMI 2024））仅聚焦于定位任务，缺乏对几何先验的显式建模；CVIS 方法（如 **CDE**（Toker et al., CVPR 2021）、**Sat2Density**（Qian et al., ICCV 2023）、**SkyDiffusion**（Ye et al., ECCV 2024））则通常将定位与生成割裂，或仅支持单向合成。Geo2 首次将几何基础模型、流匹配双向生成与联合训练策略整合为单一框架（见 Table 1），在任务覆盖与几何先验利用两个维度上均形成代际差异。

值得注意的是，Geo2 仍存在若干局限：对严重畸变或极端视角变化的地面图像，E2P 变换可能无法完全恢复精准几何关系；框架性能依赖于 VGGT 等预训练几何基础模型的覆盖能力；当前尚未探讨大规模地理数据库下的检索效率与扩展性。这些开放问题为后续研究指明了方向。



跨视角地理空间学习（Cross-View Geo-Spatial Learning）旨在建立地面全景图像与高空卫星/航空图像之间的对应关系。该领域的两个核心任务是**跨视角地理定位（CVGL）**——给定一张地面查询图像，从卫星图像数据库中检索最匹配的地理位置——和**跨视角图像合成（CVIS）**——在地面视角与卫星视角之间进行双向图像生成。这两个任务在自动驾驶、机器人导航、增强现实和城市建模中具有广泛的应用前景。

当前方法面临一个根本性瓶颈：**地面和航空图像之间存在巨大的视角差异**。地面全景图通常是以等距柱状投影（Equirectangular）捕获的360°球形视图，而卫星图像是俯视正交投影。这种几何上的不匹配使得直接应用几何基础模型（Geometric Foundation Models, GFMs）——如 VGGT——来提取跨视角图像的几何特征时，往往得到错误的3D重建结果（见 Figure 1），导致CVGL和CVIS的性能受到严重制约。

从方法谱系来看，现有工作大致可分为两类。在CVGL方面，**SAFA**（Shi et al., NeurIPS 2019）引入空间感知特征聚合，**TransGeo**（Zhu et al., CVPR 2022）采用Transformer架构，**GeoDTR+**（Zhang et al., TPAMI 2024）设计了几何布局提取器，而**Sample4Geo**（Deuser et al., ICCV 2023）通过困难负样本采样提升定位精度。在CVIS方面，**CDE**（Toker et al., CVPR 2021）将GAN与CVGL骨干网络结合但仅支持单方向合成，**RGCIS**（Yang et al., arXiv 2024）利用冻结的CVGL模型引导生成，**Sat2Density**（Qian et al., ICCV 2023）借助体密度估计，**SkyDiffusion**（Ye et al., ECCV 2024）则采用扩散模型与鸟瞰图（BEV）范式。然而，这些方法存在两个共同缺陷：一是缺乏对3D几何先验的系统性利用，二是将CVGL和CVIS视为独立任务分别优化，未能发掘两个任务之间的协同增益。

Geo2的**核心洞察**在于：通过将几何基础模型的3D先验融入到统一的共享潜在空间中，能够同时改进跨视角地理定位和双向图像合成——两个任务可以相互增强，而非彼此孤立。这一设计理念使得Geo2成为一个几何引导的统一框架，从方法层面填补了“几何先验缺失”和“任务割裂”两个关键缺口。



## 核心方法与创新机理

Geo2 的核心创新在于将几何基础模型（Geometry Foundation Model, GFM）的 3D 先验系统性地注入跨视角学习，构建了一个统一的框架，同时解决跨视角地理定位（CVGL）和双向跨视角图像合成（CVIS）两个任务，并使二者相互增强。与现有方法相比，Geo2 在四个关键环节实现了实质性突破。

### 1. 从失败中提炼动机：几何先验的跨视角适配

直接将 VGGT 等 GFM 应用于跨视角图像对时，由于地面全景与卫星俯视图之间存在巨大的视角差异和畸变模式，模型无法提取准确的几何特征，导致 3D 重建失败（Figure 1）。这一观察揭示了核心瓶颈：**GFM 的几何先验是有价值的，但必须通过适当的视角归一化才能释放其潜力**。Geo2 正是围绕这一瓶颈展开设计，而非简单地将 GFM 作为即插即用的特征提取器。

### 2. 地面特征提取：E2P 变换替代直接输入

**Changed Slot**：地面图像特征提取

- **Baseline 做法**：直接将全景图输入 VGGT 或使用简单变换（如极线变换），忽略了等距柱状投影的严重畸变。
- **Geo2 方案**：引入等距柱状到透视（E2P）变换，将地面全景图 $I^g$ 分解为 $V$ 个透视裁剪视图 $\{IP^i\}_{i=1}^V = \mathrm{E2P}(I^g)$，再分别输入 VGGT 提取几何特征（Eq. 1, Figure 3）。每个透视裁剪图对应一个局部视场，有效缓解了全景畸变对 GFM 的干扰，使得 VGGT 能够输出具有强几何对齐性的特征（如建筑物轮廓和整体布局）。

这一设计的深层逻辑是：GFM 在透视图像上训练，E2P 将全景图“翻译”回 GFM 熟悉的表示空间，从而激活其几何理解能力。

### 3. 跨视角特征对齐：GeoMap 构建共享 3D 感知潜在空间

**Changed Slot**：跨视角特征对齐

- **Baseline 做法**：采用极线变换或独立处理两个任务，缺乏统一的共享表示，CVGL 和 CVIS 通常分离训练。
- **Geo2 方案**：提出 GeoMap 双分支模型，将地面和卫星特征分别映射到共享的 3D 感知潜在空间（Section 3.2, Figure 4）。在卫星分支中，语义令牌作为查询，通过交叉注意力聚合几何特征令牌的信息：$out^s = \mathrm{Attn}(q^s, t^{s'}, t^{s'})$（Eq. 2）。这一设计使得几何与语义信息在统一的潜在空间中深度融合，为下游的定位和生成任务提供一致的表示基础。

GeoMap 的关键洞察在于：**共享的 3D 感知潜在空间消除了地面与卫星特征之间的域间隙**，使得 CVGL 的检索目标 $b = \mathrm{argmin}_i \|f_q^g - f_i^s\|_2$ 能够在几何对齐的嵌入空间中高效执行。

### 4. 图像合成模型：GeoFlow 实现单方向训练、双向生成

**Changed Slot**：图像合成模型

- **Baseline 做法**：使用 GAN 或扩散模型，且需要分别训练地面→卫星和卫星→地面两个方向（如 **CDE** (Toker et al., CVPR 2021) 仅支持单向，**SkyDiffusion** (Ye et al., ECCV 2024) 需 BEV 范式辅助）。
- **Geo2 方案**：采用流匹配（Flow Matching）框架 GeoFlow，仅需训练地面→卫星（G2S）单一方向，即可在推理时通过反转积分方向实现双向合成（Section 3.3, Figure 5）。具体而言：
  - 定义隐空间插值路径 $x_t = (1-t) \times x^g + t \times x^s$（Eq. 3），训练网络预测向量场 $v = x^s - x^g$，损失为 $\mathcal{L}_{IG} = \|G_\theta(x_t, t, c) - v\|_2$（Eq. 4）。
  - 前向积分 $x^s = x^g + \int_0^1 G_\theta(x_t, t, c) dt$ 实现 G2S 生成（Eq. 5）。
  - 反向积分 $x^g = x^s - \int_0^1 G_\theta(x_t, t, c) dt$ 实现 S2G 生成（Eq. 6），即便模型从未在该方向训练。

这一设计的核心优势在于：**流匹配的向量场天然支持方向反转**，无需训练两个独立的生成器，显著降低了训练开销，同时保证了双向合成的一致性。

### 5. 训练策略：联合优化与 KL 一致性损失

**Changed Slot**：训练策略

- **Baseline 做法**：CVGL 和 CVIS 分开训练，或使用固定的 CVGL 模型辅助生成（如 **RGCIS** (Yang et al., arXiv 2024)）。
- **Geo2 方案**：联合训练 GeoMap 和 GeoFlow，引入 KL 一致性损失 $\mathcal{L}_{KL} = \mathrm{KL}(f^g \parallel f^s) + \mathrm{KL}(f^s \parallel f^g)$（Eq. 8），惩罚地面与卫星嵌入分布的差异，实现双向对齐（Section 3.4）。联合训练使得定位和生成任务相互增强：更准确的定位提供更好的生成条件，而高质量的生成反过来正则化特征空间，提升定位鲁棒性。

### 创新总结

Geo2 的创新链条清晰且因果紧密：**E2P 变换**解决了 GFM 在跨视角场景下的适配问题，**GeoMap** 将适配后的几何特征融入共享潜在空间，**GeoFlow** 利用流匹配的可逆性实现高效双向生成，**联合训练**则通过一致性损失将定位与生成耦合为相互增强的整体。这一设计使得 Geo2 在 VIGOR 同区域上达到 R@1 81.59%（+3.73% vs. Sample4Geo），在 CVACT G2S 合成上取得 FID 31.72，均显著优于此前最佳方法。



Geo2 是一个统一框架，将跨视角地理定位（CVGL）与双向跨视角图像合成（CVIS）耦合在共享的3D感知潜在空间中，使两个任务相互增强。

### 动机与核心瓶颈

直接对跨视角图像对应用几何基础模型（GFM）会失效。如 Figure 1 所示，将 VGGT 分别应用于卫星图和地面全景图时，由于两者之间存在极大的视角差异，GFM 无法提取准确的几何对应关系，导致重建结果严重错位。这一瓶颈驱动 Geo2 设计专门的几何特征提取与对齐策略。

### 框架总览

Geo2 的完整流水线如 Figure 2 所示，由四个核心模块串联：

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the Geo2 framework. We first extract geometric features from ground and satellite images using VGGT. These dense features are then embedded into a shared geometry-aware latent space as detailed in Sec. 3.2. The resulting embeddings*

1. **VGGT 几何特征提取**：以预训练的 VGGT 作为几何基础模型，分别从地面图像和卫星图像中提取稠密几何先验特征。对于地面全景图，先通过 E2P（Equiangular-to-Perspective）变换将其投影为多个透视裁剪视图，再输入 VGGT，以缓解全景畸变对几何重建的干扰。

2. **GeoMap 共享嵌入**：双分支模块将地面和卫星的几何特征映射到统一的3D感知潜在空间。地面分支和卫星分支各自独立处理，通过交叉注意力机制融合语义令牌与几何特征令牌，最终输出几何感知的嵌入向量 $f^g$ 和 $f^s$（详见 Figure 4）。

3. **GeoFlow 双向合成**：基于流匹配（Flow Matching）框架，GeoFlow 以 GeoMap 输出的潜在表示 $f^g$ 或 $f^s$ 作为条件 $C$，在预训练自编码器（RAE）的隐空间中学习地面与卫星之间的最优传输位移。关键特性在于：模型仅需训练地面到卫星（G2S）单一方向，推理时通过反转积分方向即可实现卫星到地面（S2G）的合成（详见 Figure 5）。

4. **联合优化**：GeoMap 与 GeoFlow 联合训练，引入 KL 一致性损失 $\mathcal{L}_{KL}$ 对齐 $f^g$ 与 $f^s$ 的分布，使定位任务和双向合成任务共享统一的几何感知表示空间，形成相互增强的耦合框架。

### 输入输出流

- **CVGL 任务**：输入地面查询图像 $I^g$ 和候选卫星图像集 $\{I^s_i\}_{i=1}^N$，通过 GeoMap 分别提取 $f^g_q$ 和 $\{f^s_i\}$，以 L2 距离最小化检索最佳匹配索引 $b = \operatorname{argmin}_i \|f^g_q - f^s_i\|_2$。
- **CVIS 任务（G2S）**：输入地面图像 $I^g$，经 GeoMap 得到 $f^g$ 作为 GeoFlow 的条件，从 RAE 编码的地面隐空间 $x^g$ 出发，沿学习到的向量场前向积分生成卫星隐空间 $x^s = x^g + \int_0^1 G_\theta(x_t, t, c) dt$，再经 RAE 解码得到合成卫星图像。
- **CVIS 任务（S2G）**：输入卫星图像 $I^s$，以 $f^s$ 为条件，从 $x^s$ 出发反向积分 $x^g = x^s - \int_0^1 G_\theta(x_t, t, c) dt$，解码得到合成地面图像。此方向无需额外训练。



Geo2 的核心技术路线是将几何基础模型（GFM）的 3D 先验注入统一的跨视角潜在空间，并以此驱动地理定位（CVGL）与双向图像合成（CVIS）的联合优化。整个框架由三个关键模块构成：**VGGT 几何特征提取**、**GeoMap 共享嵌入**以及 **GeoFlow 流匹配合成**。

### 1. 几何先验提取与 E2P 变换

直接对跨视角图像对应用 VGGT 等几何基础模型会因巨大的视角差异而失效（见 Figure 1）。Geo2 的解决方案是对地面全景图施加 **E2P（Equiangular-to-Perspective）变换**，将其投影为多个透视裁剪视图，再输入 VGGT 提取几何特征：

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of directly using VGGT on satellite (a) and ground (c) images, leading to incorrect reconstructed shown in (b)*

$$
\{ I P ^ { i } \} _ { i = 1 } ^ { V } = \mathrm { E 2 P } ( I ^ { g } )
$$

其中 $I^g$ 表示地面等距柱状图像，$\{IP^i\}$ 为生成的 $V$ 个透视裁剪图。这一变换解决了全景图的畸变问题，使 VGGT 能够输出准确的深度与点云重建（见 Figure 3）。卫星图像则直接输入 VGGT，无需额外预处理。

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/004_Figure_3.jpg]]
*Figure 3: Illustration of VGGT reconstructions for (a) the ground view and (b) the satellite view, showing strong geometric alignment (e.g., buildings and overall layout). The ground view reconstruction is obtained from four perspective crops, illustrated in (c)*

### 2. GeoMap：共享 3D 感知潜在空间

GeoMap 是一个双分支模型，将地面和卫星图像分别映射到共享的几何感知潜在空间。其核心设计在于**语义令牌与几何令牌的交叉注意力融合**：

$$
out^s = \mathrm { A t t n } ( q^s , t^{s'}, t^{s'} )
$$

其中 $q^s$ 为卫星分支的语义令牌（可学习查询），$t^{s'}$ 为 VGGT 提取的密集几何特征令牌。语义令牌作为查询，从几何令牌中聚合 3D 结构信息，使最终嵌入 $f^g$ 和 $f^s$ 同时编码语义内容与几何先验。

对于 CVGL 任务，检索通过最小化地面查询嵌入与候选卫星嵌入的 L2 距离完成：

$$
b = \mathrm { a r g m i n } _ { i \in \{ 1 , . . . , N \} } \| f _ { q } ^ { g } - f _ { i } ^ { s } \| _ { 2 }
$$

其中 $b$ 为最佳匹配卫星图像的索引。

### 3. GeoFlow：基于流匹配的双向合成

GeoFlow 将 CVIS 建模为域翻译问题，采用流匹配（Flow Matching）框架。其关键优势在于**仅需单方向训练即可实现双向合成**。

首先定义地面隐空间 $x^g$ 与卫星隐空间 $x^s$ 之间的最优传输插值路径：

$$
x _ { t } = ( 1 - t ) \times x ^ { g } + t \times x ^ { s }
$$

网络 $G_\theta$ 被训练以预测该路径上的向量场 $v = x^s - x^g$，损失函数为：

$$
\mathcal { L } _ { I G } = \| G _ { \theta } ( x _ { t } , t , c ) - v \| _ { 2 }
$$

其中 $c$ 为条件信号（对应 GeoMap 输出的 $f^g$ 或 $f^s$）。推理时，地面到卫星的生成通过对向量场正向积分实现：

$$
x^s = x^g + \int_0^1 G_\theta(x_t, t, c) dt
$$

卫星到地面的生成则仅需反转积分方向，无需额外训练：

$$
x^g = x^s - \int_0^1 G_\theta(x_t, t, c) dt
$$

合成图像由预训练自编码器（RAE）从隐空间 $x^s$ 或 $x^g$ 解码得到，重建损失为标准 L2 损失：

$$
\mathcal { L } _ { \mathrm { r e c } } = \| \hat { I } - I \| _ { 2 }
$$

### 4. 联合优化与一致性约束

Geo2 对 GeoMap 和 GeoFlow 进行联合微调，并引入 **KL 一致性损失** 对齐地面与卫星嵌入的分布：

$$
\mathcal { L } _ { K L } = \mathrm { K L } ( f ^ { g } \parallel f ^ { s } ) + \mathrm { K L } ( f ^ { s } \parallel f ^ { g } )
$$

这一对称 KL 散度惩罚使两个方向的潜在分布相互靠近，促使 CVGL 的判别性嵌入与 CVIS 的生成性隐空间相互增强，形成耦合优化闭环。

### 补充图表

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/005_Figure_4.jpg]]
*Figure 4: Overview of GeoMap pipeline. Ground and satellite images are individually processed via two separate branches*

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/006_Figure_5.jpg]]
*Figure 5: Overview of our GeoFlow pipeline. The latent representation*



## 实验与关键发现

### 核心性能瓶颈与因果机制

Geo2 解决的核心瓶颈在于：几何基础模型（GFM）如 VGGT 虽然能从单张图像提取丰富的 3D 几何先验，但直接将其应用于跨视角图像对时，地面全景图与卫星俯视图之间的巨大视角差异会导致几何特征提取严重失准（见 Figure 1）。这一瓶颈同时制约了跨视角地理定位（CVGL）和跨视角图像合成（CVIS）两个任务的性能上限。

Geo2 的核心因果调节变量是将地面和卫星图像分别通过 **GeoMap** 嵌入到共享的 3D 感知潜在空间。具体而言，地面全景图先经过 **E2P（Equiangular-to-Perspective）变换** 分解为多个透视裁剪图（Eq. 1），再输入 VGGT 提取几何特征；卫星图像则直接输入 VGGT。GeoMap 双分支模型通过交叉注意力机制（Eq. 2）融合几何令牌与语义令牌，生成共享的几何感知嵌入 $f^g$ 和 $f^s$。在此基础上，**GeoFlow** 流匹配模型利用最优传输路径 $x_t = (1 - t) x^g + t x^s$（Eq. 3），仅需单方向（地面→卫星）训练即可实现双向合成（Eq. 5-6），并通过 KL 一致性损失（Eq. 8）对齐两个方向的嵌入分布，使 CVGL 与 CVIS 相互增强。

---

### 跨视角地理定位（CVGL）主实验结果

Geo2 在三个标准数据集上均取得了最优或次优的定位精度，验证了几何先验嵌入策略的有效性。

**VIGOR 数据集**（Table 2）：在 Same-Area 设置下，Geo2 的 R@1 达到 **81.59%**，较此前最佳模型 **Sample4Geo**（Deuser et al., ICCV 2023）的 77.86% 提升 **+3.73** 个百分点；在更具挑战性的 Cross-Area 设置下，R@1 达到 **66.71%**，较 Sample4Geo 的 61.70% 提升 **+5.01** 个百分点。这一跨区域泛化增益（+5.01）明显大于同区域增益（+3.73），表明 3D 感知的共享潜在空间对空间偏移具有更强的鲁棒性。

**CVUSA 和 CVACT 数据集**（Table 3）：在 CVACT 验证集上，Geo2 的 R@1 达到 **94.36%**；在 CVACT 测试集上为 **75.08%**。在 CVUSA 上同样表现优异。对比基线中，**GeoDTR+**（Zhang et al., TPAMI 2024）和 **TransGeo**（Zhu et al., CVPR 2022）分别代表几何布局提取和 Transformer 架构路线，Geo2 在两个数据集上均实现超越，证明 VGGT 提供的密集 3D 先验优于手工设计的几何描述子。

**跨数据集泛化**（Table 4）：在 CVUSA→CVACT 设置下，Geo2 的 R@1 达到 **63.17%**；在 CVACT→CVUSA 设置下为 **55.14%**。跨数据集性能衰减幅度明显小于纯外观学习方法，验证了几何先验对数据域偏移的缓解作用。

---

### 跨视角图像合成（CVIS）主实验结果

Geo2 在双向合成任务上均显著优于现有方法，且仅需单方向训练即可实现双向生成。

**地面→卫星合成**（Table 5）：在 CVACT 上，Geo2 取得 FID **31.72**、LPIPS **0.552**、PSNR **14.62**，全面优于 **SkyDiffusion**（Ye et al., ECCV 2024）、**Sat2Density**（Qian et al., ICCV 2023）和 **RGCIS**（Yang et al., arXiv 2024）等专用合成基线。在 VIGOR 上，FID 达到 **30.09**。值得注意的是，**CDE**（Toker et al., CVPR 2021）等早期方法需要分别训练两个方向的 GAN，而 Geo2 的流匹配框架天然支持双向推理。

**卫星→地面合成**（Table 6）：在 VIGOR 上，Geo2 的 FID 达到 **22.90**，显著低于地面→卫星方向的 30.09，表明从结构化的卫星视图生成复杂的地面全景在分布匹配上更具挑战，但 Geo2 仍大幅领先对比方法。

---

### 消融实验与组件分析

消融实验验证了三个关键设计的因果贡献：

1. **VGGT 几何先验**：移除 VGGT 特征提取分支后，定位和合成指标均出现显著下降，证实 GFMs 提供的密集 3D 信息是不可替代的性能驱动因素。
2. **E2P 变换**：将地面全景图直接输入 VGGT（不经过 E2P 分解）会导致几何特征提取质量恶化，说明透视裁剪对于缓解等距柱状投影畸变至关重要。
3. **联合训练与 KL 一致性损失**：单独训练 CVGL 和 CVIS（无联合优化）时，两个任务的性能均低于联合训练方案，验证了共享潜在空间的双向增强效应。

*注：具体消融数值需查阅原文 Ablation Studies 部分，本分析基于已验证声明综合推断。*

---

### 失败模式与局限性

1. **极端畸变场景**：当地面图像存在严重畸变或极端视角倾斜时，E2P 变换可能无法完全恢复精准的几何对应关系，导致特征提取质量下降。
2. **GFM 依赖**：整个框架依赖 VGGT 等几何基础模型的预训练权重。若 GFM 在训练数据覆盖不足的场景（如密集植被、非结构化地形）中性能退化，Geo2 的整体表现将受传导性影响。
3. **检索效率未评估**：当前实验聚焦于精度指标，未探讨 GeoMap 嵌入在大规模地理数据库上的检索效率与可扩展性。

---

### 关键图表结论汇总

- **Table 1**：系统对比了代表性跨视角学习方法在支持任务（CVGL/CVIS）和几何先验利用上的差异，Geo2 是首个同时支持 CVGL 和双向 CVIS 的统一框架。
- **Table 2-4**：Geo2 在 VIGOR、CVUSA/CVACT 及跨数据集设置下均取得最优 CVGL 性能，尤其在跨区域和跨数据集场景下优势更为突出。
- **Table 5-6**：Geo2 在双向 CVIS 任务上全面超越专用合成方法，验证了流匹配框架和共享潜在空间的有效性。
- **Figure 6-8**：可视化结果表明 Geo2 生成的卫星图像能准确还原道路布局和建筑结构，生成的地面全景在几何一致性和语义保真度上均优于基线方法。

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/002_Table_1.jpg]]
*Table 1: Comparison of representative cross-view geo-spatial learning methods on supported tasks and geometric priors*

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/007_Table_2.jpg]]
*Table 2: Comparison of cross-view geo-localization performance on the VIGOR dataset under same-area and cross-area settings. We report recall rates (%) and hit rate (%) at different top-K retrieval thresholds. The best results are shown in bold and the second-best results are underlined*

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/010_Table_5.jpg]]
*Table 5: Comparison of Ground-to-Satellite image synthesis performance on CVUSA, CVACT, and VIGOR datasets. We report FID [9], LPIPS [49], PSNR and SSIM scores. The best results are shown in bold*

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/013_Figure_6.jpg]]
*Figure 6: Visualization of Generated images from*

### 补充图表

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/008_Table_3.jpg]]
*Table 3: Comparison of cross-view geo-localization performance on CVUSA and CVACT datasets in recall at top-K retrieves (R@K). The best results are shown in bold and the second-best results are underlined. † indicates Polar Transformation is applied*

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/009_Table_4.jpg]]
*Table 4: Comparison of cross-view geo-localization performance on cross-dataset benchmarks. CVUSA CVACT stands for training on CVUSA and testing on CVACT. CVACT CVUSA stands for training on CVACT and testing on CVUSA. The best results are shown in bold and the second-best results are underlined*

![[assets/figures/papers/paper_list_l2504_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_Geo2_Geometry_Gu/figures/011_Table_6.jpg]]
*Table 6: Comparison of Satellite-to-Ground image synthesis performance on CVUSA, CVACT, and VIGOR datasets. We report FID [9], LPIPS [49], PSNR and SSIM scores. The best results are shown in bold*



## 定位与知识库关联

### 1. 问题定位：几何先验在跨视角任务中的缺失

跨视角地理空间学习（cross-view geo-spatial learning）长期面临一个核心瓶颈：地面图像（通常为等距柱状全景图）与卫星/航空图像之间存在巨大的视角差异和几何畸变，导致特征对齐困难。已有工作主要依赖语义特征匹配或手工设计的几何变换（如极线变换、Polar Transformation）来缓解这一问题，但始终未能将**可泛化的3D几何先验**系统性地引入跨视角表示学习。

Geo2 的核心洞察在于：直接应用几何基础模型（Geometry Foundation Models, GFMs）到跨视角图像对时，由于视角差异过大，GFM 无法提取准确的几何特征（Figure 1 展示了 VGGT 直接应用于卫星和地面图像时的失败重建案例）。因此，问题的关键不是“是否使用几何先验”，而是“如何将几何先验适配到跨视角场景中”。Geo2 通过 E2P（Equirectangular-to-Perspective）变换和 GeoMap 双分支嵌入，将 GFM 的 3D 几何先验融入共享的潜在空间，从而同时服务于跨视角地理定位（CVGL）和双向图像合成（CVIS）。

### 2. 与 CVGL 基线方法的关系

Geo2 在 CVGL 任务上对比了多个代表性基线，这些方法代表了跨视角地理定位的不同技术路线：

- **SAFA**（Shi et al., NeurIPS 2019）：采用空间感知特征聚合，是早期基于 CNN 的经典方法，但缺乏显式几何建模。
- **TransGeo**（Zhu et al., CVPR 2022）：引入 Transformer 架构增强全局特征交互，但仍以语义匹配为主。
- **GeoDTR+**（Zhang et al., TPAMI 2024）：通过几何布局提取器（geometric layout extractor）引入部分几何信息，是几何感知方法的代表。
- **Sample4Geo**（Deuser et al., ICCV 2023）：通过硬负样本采样策略提升判别能力，在 VIGOR 上曾是最佳方法。

Geo2 相对于上述方法的本质差异在于：**Geo2 的几何先验来源于预训练的 GFM（VGGT），而非任务特定的几何模块**。VGGT 提供了稠密的 3D 感知特征，GeoMap 通过交叉注意力机制将这些几何特征与语义令牌融合，形成几何-语义联合表示。这一设计使得 Geo2 在 VIGOR Same-Area 上达到 R@1 81.59%（超过 Sample4Geo 的 77.86%），在 Cross-Area 上达到 66.71%（超过 61.70%），在 CVACT Val 上达到 94.36%。跨数据集泛化测试中，CVUSA→CVACT 的 R@1 达到 63.17%，进一步验证了几何先验对泛化能力的提升。

### 3. 与 CVIS 基线方法的关系

在跨视角图像合成方面，Geo2 对比了以下代表性基线：

- **CDE**（Toker et al., CVPR 2021）：将 GAN 与 CVGL 骨干网络结合，但仅支持单一方向（地面→卫星）合成，且两个任务独立训练。
- **Sat2Density**（Qian et al., ICCV 2023）：利用体密度估计进行跨视角合成，隐式建模 3D 结构，但计算开销较大。
- **RGCIS**（Yang et al., arXiv 2024）：使用冻结的 CVGL 模型指导生成过程，但 CVGL 和 CVIS 之间缺乏双向增强。
- **SkyDiffusion**（Ye et al., ECCV 2024）：采用扩散模型和 BEV 范式，是近期较强的 CVIS 方法。

Geo2 的 GeoFlow 模块在以下方面形成差异化优势：
1. **双向合成**：基于流匹配（flow matching）框架，仅需训练地面→卫星方向，推理时反转积分方向即可实现卫星→地面合成（Eq. 5, 6），避免了分别训练两个方向模型的开销。
2. **联合优化**：通过 KL 一致性损失（Eq. 8）对齐地面与卫星嵌入的分布，使 CVGL 和 CVIS 相互增强，而非像 RGCIS 那样单向依赖。
3. **性能优势**：在 CVACT 地面→卫星合成任务上，Geo2 取得 FID 31.72、LPIPS 0.552，优于所有对比方法；在 VIGOR 卫星→地面合成上，FID 降至 22.90。

### 4. 适用边界与局限

Geo2 的适用性依赖于以下前提条件：

1. **全景图依赖**：地面分支需要等距柱状全景图作为输入，通过 E2P 变换生成多个透视裁剪图。对于仅提供单张透视地面图像（如街景截图）的场景，E2P 变换无法直接适用，需要额外的视角补全或适配模块。
2. **GFM 预训练质量**：Geo2 的几何特征提取完全依赖 VGGT 的预训练权重。若 VGGT 在特定场景（如极端天气、非城市场景、低分辨率图像）下性能下降，整个框架的特征质量将受到级联影响。
3. **畸变残差**：E2P 变换虽然解决了全景图的畸变问题，但对于存在严重畸变或极端视角变化的地面图像，变换后的透视裁剪图可能仍残留几何误差，影响后续特征提取的精度。
4. **检索效率未验证**：当前实验聚焦于中小规模数据集（VIGOR、CVUSA、CVACT），未探讨在大规模地理数据库上的检索效率与扩展性。

### 5. 开放问题

Geo2 为跨视角地理空间学习开辟了“几何基础模型 + 任务联合优化”的新范式，但仍存在以下待探索方向：

1. **非全景地面图像的适配**：能否在仅使用单张透视地面图像（而非全景图）的情况下，通过几何推理或视角补全实现同等级别的跨视角对齐？这将显著扩展方法的适用场景。
2. **E2P 畸变残差的进一步消除**：当前 E2P 变换是固定的几何投影，是否可以通过可学习的变形模块或自适应的裁剪策略进一步减小畸变残差？
3. **非城市场景的泛化**：VGGT 的训练数据以城市场景为主，Geo2 在自然地形、荒漠、海洋等非城市场景下的几何先验质量与任务性能尚待验证。
4. **更轻量化的几何适配方案**：GeoMap 需要为地面和卫星分别运行 VGGT 特征提取，计算开销较大。是否存在更高效的几何先验注入方式，如轻量级几何适配器或知识蒸馏方案？



## 原文 PDF

![[paperPDFs/CVPR_2026/Geo2_Geometry_Guided_Cross_view_Geo_Localization_and_Image_Synthesis.pdf]]
