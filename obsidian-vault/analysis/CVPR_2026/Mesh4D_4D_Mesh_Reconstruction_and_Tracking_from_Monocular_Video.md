---
title: "Mesh4D: 4D Mesh Reconstruction and Tracking from Monocular Video"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Mesh4D_4D_Mesh_Reconstruction_and_Tracking_from_Monocular_Video.pdf
project_link: "https://mesh-4d.github.io"
code_link: null
aliases:
- Mesh4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用骨架信息引导的变形VAE，将整个序列的变形编码到紧凑的潜在空间，并结合时空注意力捕获全局运动模式，从而为变形扩散模型提供强先验。
primary_logic: 通过将整个动画序列的变形编码到单个紧凑潜在空间，并利用骨架信息（仅训练时）作为先验，模型能够从单目视频中一次性预测出完整且时序一致的4D网格变形。
claims:
- 我们的模型在重建（IoU、P2S、Chamfer）和跟踪（ℓ2-Corr）指标上全面超越先前的最先进方法。
- 在变形VAE中引入骨架信息（蒙皮权重和骨骼）带来了显著的性能提升。
- 去除骨架信息导致刚性变换恢复失败，网格出现扭曲。
- 去除时空注意力导致运动抖动和较大的局部误差。
---

# Mesh4D: 4D Mesh Reconstruction and Tracking from Monocular Video

> [!tip] 核心洞察
> 通过将整个动画序列的变形编码到单个紧凑潜在空间，并利用骨架信息（仅训练时）作为先验，模型能够从单目视频中一次性预测出完整且时序一致的4D网格变形。

| 字段 | 内容 |
|------|------|
| 中文题名 | Mesh4D：从单目视频进行4D网格重建与跟踪 |
| 英文题名 | Mesh4D: 4D Mesh Reconstruction and Tracking from Monocular Video |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.05251) · [Project](https://mesh-4d.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Mesh4D |
| Dataset | Objaverse子集基准 |

> [!tip] 效果简介
> - Objaverse子集基准 上，IoU↑ 0.3949 vs 0.3071 (HY3D 2.1) (+0.0878)；P2S↓ 0.0261 vs 0.0345 (GVFD) (-0.0084)；Chamfer↓ 0.0243 vs 0.0378 (GVFD) (-0.0135)。

## 概要

从单目视频中恢复动态物体的完整三维形状与运动，是计算机视觉中长期存在的挑战。核心瓶颈在于，单目输入天然存在遮挡和视角限制，使得大量表面不可见；同时，整个视频序列的变形信息需要被一次性编码，才能保证时序一致性。现有方法要么逐帧独立重建导致姿态抖动，要么将运动建模为高斯泼溅（3D‑GS）而缺乏显式几何约束，无法同时获得高质量几何与精确的对应关系。

Mesh4D 提出了一条前馈式单目4D网格重建路径。其核心洞察是：将整个动画序列的变形编码到一个紧凑的潜在空间中，并利用骨架信息（仅在训练时作为特权先验）引导变形VAE学习，从而为变形扩散模型提供强先验。这一设计使得模型能够从单目视频中一次性预测出完整且时序一致的4D网格变形。

在 Objaverse 子集基准上，Mesh4D 在几何重建（IoU 0.3949 vs. HY3D 2.1 的 0.3071）和跟踪精度（ℓ2‑Corr 0.0338 vs. GVFD 的 0.0514）上全面超越先前最优方法。消融实验证实，骨架信息的注入对刚性变换恢复至关重要，去除骨架会导致网格扭曲；而时空注意力的移除则引发运动抖动和局部误差显著增大。同时，预训练扩散模型权重的加载对性能有决定性影响，从头训练会导致指标急剧下降。值得注意的是，分类器自由引导（CFG）并未提升重建质量，反而使性能略有下降。

在方法谱系上，Mesh4D 区别于 **Hunyuan3D 2.1**（Tencent Hunyuan3D Team, 2025）的逐帧静态重建、**L4GM**（Ren et al., NeurIPS 2024）的前馈4D高斯重建，以及 **GVFD**（Zhang et al., ICCV 2025）的视频到4D高斯生成。它通过三个关键设计实现突破：（1）将变形编码从逐帧或两帧扩展到整个视频序列的联合时空注意力编码；（2）在变形VAE中引入蒙皮权重和骨骼作为特权训练先验；（3）在变形扩散模型中添加时空嵌入和规范网格交叉注意力，以视频和网格为条件生成变形潜码。

当前方法仍存在明确局限：假设网格拓扑在动画过程中保持不变，无法处理拓扑变化场景；规范网格重建的错误会传播到后续帧；泛化能力受限于预训练3D重建模型的训练数据分布。此外，训练依赖每帧对应的顶点数据，对于非合成视频难以获取。

从单目视频重建动态物体的完整三维形状与运动，是计算机视觉与图形学中长期存在的核心挑战。该任务要求模型同时恢复物体的几何外观和时序变形，而输入仅为一个视角的RGB图像序列。这种极端的欠定问题使得传统多视图几何方法难以适用，因为遮挡、视角限制和运动模糊会严重破坏观测信息的一致性。

近年来，单目三维重建领域取得了显著进展。以**Hunyuan3D 2.1**（Tencent Hunyuan3D Team, 2025）为代表的大规模预训练模型，能够从单张图像生成质量可观的静态网格。然而，当将这些逐帧独立重建的方法直接应用于视频时，它们完全忽视了时序信息，导致各帧之间的姿态和形状估计不一致，无法形成连贯的运动序列。

针对动态场景，一些工作转向了4D表示学习。**L4GM**（Ren et al., NeurIPS 2024）和**GVFD**（Zhang et al., ICCV 2025）分别探索了前馈4D高斯重建和视频到4D高斯的生成。这些基于3D高斯泼溅的方法在渲染质量上表现出色，但其核心局限在于：它们不显式定义物体的内外表面，因此难以进行精确的几何重建和表面跟踪。此外，这些方法往往缺乏对时序运动模式的深层建模，导致姿态估计不准确。

从更根本的层面看，现有方法面临一个共同瓶颈：**如何一次性编码整个视频序列的变形信息，并引入足够的3D和物理先验以补全因遮挡和视角限制而不可见的表面**。逐帧独立处理丢失了运动连续性，而仅依赖几何监督又难以约束高度非刚性的变形空间。

Mesh4D的提出正是为了弥合这一缺口。其核心动机在于：通过将整个动画序列的变形编码到单个紧凑的潜在空间，并利用骨架信息作为训练时的特权先验，模型可以从单目视频中一次性预测出完整且时序一致的4D网格变形。这一思路将静态重建的精度优势与动态建模的时序一致性相结合，为单目4D重建开辟了新的技术路径。

## 核心方法与创新机理

Mesh4D 的核心创新在于将**整个视频序列的变形信息一次性编码到紧凑的潜在空间**，并利用**骨架信息作为训练时的特权先验**，从而从单目视频中直接预测完整且时序一致的 4D 网格变形。这一设计解决了现有方法的两大瓶颈：逐帧独立重建导致时序断裂，以及缺乏 3D 先验导致不可见表面补全失败。

### 1. 序列级变形编码：从逐帧到全局

现有方法或逐帧独立重建（如 **Hunyuan3D 2.1**，Tencent Hunyuan3D Team, 2025），或仅编码两帧间的局部运动（如 Motion2VecSet），无法捕获长程时序依赖。Mesh4D 的变形 VAE 通过 **8 层时空注意力（spatio-temporal attention）** 将整个 $T$ 帧序列的变形场压缩为单个潜码 $z^d$（见 Figure 2）。该注意力机制交替执行时间注意力、全局注意力和空间注意力，使模型能够关联不同帧间对应点的运动轨迹，从而消除逐帧预测固有的抖动问题。

消融实验证实了这一设计的必要性：**去除时空注意力后，模型出现明显的运动抖动和较大的局部变形误差**（Table 3, Figure 6）。定量上，完整模型在 Objaverse 子集基准上达到 IoU 0.3949、P2S 0.0261、Chamfer 0.0243，全面超越 GVFD（Zhang et al., ICCV 2025）和 L4GM（Ren et al., NeurIPS 2024）等前馈 4D 重建方法（Table 1）。

### 2. 骨架引导的变形先验：仅在训练时注入

Mesh4D 在变形 VAE 编码器中引入**蒙皮权重和骨骼信息作为特权先验**，通过两种掩码注意力机制实现：

- **蒙皮偏置自注意力**：以蒙皮权重相似度 $M^s$ 作为注意力掩码，使模型关注受同一骨骼影响的点：

$$\hat{h}_t = \mathrm{softmax}\left(\frac{h_t h_t^\top + M^s}{\sqrt{c}}\right)h_t + h_t$$

- **骨骼交叉注意力**：点特征与骨骼特征之间通过蒙皮权重掩码 $M^b$ 约束的交叉注意力，显式建模骨骼-顶点关系：

$$h_t' = \mathrm{softmax}\left(\frac{\hat{h}_t h_t^{b\top} + M^b}{\sqrt{c}}\right)h_t^b + \hat{h}_t$$

这一设计的关键在于**推理时无需骨架信息**——骨架仅作为训练时的辅助信号，帮助 VAE 学习更紧凑、更具物理意义的变形潜空间。消融实验表明，去除骨架信息会导致**刚性变换恢复失败和网格扭曲**（Figure 6），定量上几何和跟踪指标均显著下降（Table 3）。这验证了骨架先验对于从单目视频中解耦刚体运动与局部变形的核心作用。

### 3. 条件变形扩散：视频与网格双条件生成

与基于静态 3D 扩散模型的方法不同，Mesh4D 的变形扩散模型在 **Hunyuan3D 2.1 形状扩散模型**基础上，新增**时空嵌入和规范网格交叉注意力层**（Figure 3）。该模型以视频特征和规范网格 $\mathcal{M}_1$ 为条件，通过流匹配（flow matching）从噪声中恢复变形潜码 $z^d$：

$$\min_\theta \mathbb{E}_{(z^s, I), t, \epsilon^s \sim \mathcal{N}(0, 1)} \left\| v^s - v_\theta^s(z_t^s, t, I) \right\|_2^2$$

这种双条件设计使得扩散模型能够同时利用视频中的外观线索和网格的几何结构，生成与输入视频时序对齐的变形序列。实验表明，**使用预训练扩散模型权重对性能至关重要**，从头训练会导致指标大幅下降（Table 5）；而分类器自由引导（CFG）在此任务中反而略微降低重建质量（Table 4），说明变形潜空间已足够紧凑，无需额外引导。

### 4. 方法定位与差异总结

| 设计维度 | 先前方法 | Mesh4D |
|---------|---------|--------|
| 变形编码范围 | 逐帧独立或两帧局部 | 全序列联合编码至单潜码 |
| 时序建模 | 无或弱时序关联 | 8 层时空注意力交替 |
| 训练先验 | 纯几何监督 | 骨架信息（蒙皮权重+骨骼）作为特权先验 |
| 变形生成条件 | 静态图像或单帧 | 视频特征 + 规范网格双条件 |

这些 changed slots 共同构成了 Mesh4D 相对于前馈 4D 重建基线的核心优势：通过序列级编码和骨架引导的变形 VAE 学习强运动先验，再通过双条件扩散模型将该先验与单目视频观测对齐，实现一次性、时序一致的完整 4D 网格重建。

Mesh4D 是一个前馈式单目 4D 网格重建模型。给定一段动态物体的单目 RGB 视频，模型一次性输出完整的动画 3D 网格及其变形场。其核心架构由三个关键模块串联构成：**规范网格重建模块**、**变形 VAE** 和**变形扩散模型**。

### 任务定义

设输入视频为 $\mathcal{T}$，模型 $\Phi$ 将其映射为第一帧的静态网格 $\mathcal{M}_1$ 和一系列变形场 $\{\mathcal{T}_{1t}\}_{t=1}^T$：

$$\Phi : \mathcal{T} \mapsto \mathcal{M}_1, \{\mathcal{T}_{1t}\}_{t=1}^T$$

其中变形场 $\mathcal{T}_{1t}$ 将规范网格 $\mathcal{M}_1$ 的顶点从时间 $1$ 变形到时间 $t$。模型假设网格拓扑在动画过程中保持不变——这是整个框架得以工作的前提条件，也是其核心局限之一。

### 模块关系与数据流

下图概括了整个 pipeline 的输入输出关系：

**Figure 3** 展示了变形扩散模型的完整流程，该模型以视频特征和规范网格为条件，通过流匹配生成变形潜码。

整个推理过程分为三个阶段：

1. **规范网格重建**：利用预训练的 **Hunyuan3D 2.1**（HY3D）从视频第一帧重建静态网格 $\mathcal{M}_1$，同时可选地生成 PBR 纹理。这一步决定了后续所有帧的拓扑基础，因此规范网格的质量对整体性能至关重要——若第一帧重建错误，该误差将传播至整个序列。

2. **变形潜码生成**：变形扩散模型以输入视频特征和规范网格 $\mathcal{M}_1$ 为条件，通过流匹配生成变形 VAE 的潜码 $z^d$。该扩散模型基于 HY3D 2.1 的形状扩散模型构建，额外添加了时空嵌入和交叉注意力层，使其能够感知视频时序信息和网格几何结构。

3. **变形场解码**：变形 VAE 解码器接收潜码 $z^d$ 和规范网格顶点 $\mathcal{V}_1$，通过时空注意力和交叉注意力重建逐顶点的变形场序列，得到每一帧的完整变形网格。

### 核心设计决策

与逐帧独立重建或仅编码两帧的基线方法（如 **Motion2VecSet**）不同，Mesh4D 的关键创新在于**将整个视频序列的变形信息编码到单个紧凑潜在空间**。这一设计使得模型能够捕获长程时序依赖，从而生成时序一致的变形序列。

变形 VAE 在训练时引入了骨架信息（蒙皮权重和骨骼）作为特权先验，帮助模型学习更好的运动表征。消融实验表明，去除骨架信息会导致刚性变换恢复失败、网格出现扭曲（Figure 6），而加入骨架偏置的自注意力机制（Eq. 4）和骨骼交叉注意力（Eq. 5）则使模型能够关注同一骨骼影响的点，显著提升变形精度。**推理时不需要骨架信息**，这保证了模型在实际应用中的可用性。

此外，变形 VAE 编码器通过最远点采样（FPS）在空间维度压缩潜码，再经过 8 层时空注意力（依次执行时间注意力、全局注意力和空间注意力）来捕获全局运动模式。消融实验证实，去除时空注意力会导致运动抖动和较大的局部误差（Figure 6, Table 3）。

Mesh4D 的核心架构由三个紧密耦合的模块组成：规范网格重建模块、变形 VAE 模块和变形扩散模型模块。整个系统的任务定义为将输入单目视频映射到第一帧网格和变形场序列：

$$\Phi : \mathcal{T} \mapsto \mathcal{M}_1, \{\mathcal{T}_{1t}\}_{t=1}^T$$

其中 $\mathcal{T}$ 为输入视频，$\mathcal{M}_1$ 为第一帧的静态网格，$\mathcal{T}_{1t}$ 表示从时刻 1 到时刻 $t$ 的变形场。

**规范网格重建模块**直接复用预训练的 Hunyuan3D 2.1（Tencent Hunyuan3D Team, 2025）从输入视频的第一帧重建静态网格 $\mathcal{M}_1$，并可选地生成 PBR 纹理。该模块为后续变形预测提供了拓扑不变的规范空间锚点。

**变形 VAE 模块**是整个方法的关键创新所在。其核心设计是将整个视频序列的变形信息编码到单个紧凑的潜在空间中，而非逐帧独立编码。编码器首先在网格表面均匀采样对应点序列，并将时刻 1 和时刻 $t$ 的对应点及其法线拼接后投影到高维特征空间：

$$\pmb{h}_t = f_l(\mathrm{PE}(\mathcal{P}_1) \oplus \pmb{n}_1 \oplus \mathrm{PE}(\mathcal{P}_t) \oplus \pmb{n}_t)$$

其中 $\mathcal{P}_1$、$\mathcal{P}_t$ 为对应点坐标，$\pmb{n}_1$、$\pmb{n}_t$ 为法线向量，$\mathrm{PE}$ 表示位置编码。

为注入骨架先验，编码器在训练时使用蒙皮权重和骨骼信息作为特权信息。具体通过两种注意力机制实现：
- **骨架偏置的自注意力**：以蒙皮权重相似度作为掩码，使模型关注受同一骨骼影响的点：

$$\hat{h}_t = \mathrm{softmax}\left(\frac{h_t h_t^\top + M^s}{\sqrt{c}}\right) h_t + h_t$$

其中 $M^s$ 为基于蒙皮权重的掩码矩阵。

- **骨骼交叉注意力**：在点特征与骨骼特征之间进行交叉注意力，同样用蒙皮权重掩码约束：

$$\pmb{h}_t' = \mathrm{softmax}\left(\frac{\hat{h}_t \pmb{h}_t^{b\top} + M^b}{\sqrt{c}}\right) \pmb{h}_t^b + \hat{\pmb{h}}_t$$

随后通过最远点采样（FPS）在空间维度压缩特征，再经过 8 层时空注意力（交替执行时间注意力、全局注意力和空间注意力）捕获全局运动模式。解码器则通过时空注意力和交叉注意力从潜码 $\pmb{z}^d$ 重建逐顶点变形场。变形 VAE 的训练损失为：

$$\mathcal{L}_{\mathrm{VAE}} = \sum_{t=1}^T \left\| (\mathcal{V}_t - \mathcal{V}_1) - \mathcal{D}_t^d(\mathcal{V}_1; \pmb{z}^d) \right\|_2^2 + \lambda L_{\mathrm{KL}}$$

即最小化顶点位移的 L2 重建误差，并施加 KL 散度正则化。需注意，骨架信息仅在训练变形 VAE 时使用，推理阶段不需要。

**变形扩散模型**基于 HY3D 2.1 的形状扩散模型构建，在其基础上添加了时空嵌入和规范网格交叉注意力层，以视频特征和规范网格为条件生成变形潜码。模型采用流匹配（flow matching）训练目标：

$$\min_{\pmb{\theta}} \mathbb{E}_{(\pmb{z}^s, \pmb{I}), t, \epsilon^s \sim \mathcal{N}(\mathbf{0}, \mathbf{1})} \left\| \pmb{v}^s - \pmb{v}_{\pmb{\theta}}^s\left(\pmb{z}_t^s, t, \pmb{I}\right) \right\|_2^2$$

其中 $\pmb{v}^s$ 为真实速度场，$\pmb{v}_{\pmb{\theta}}^s$ 为模型预测的速度场，$\pmb{I}$ 为输入视频条件。扩散模型生成的变形潜码随后送入变形 VAE 解码器，得到完整的时序变形场序列。

## 实验与关键发现

### 4D重建与跟踪主结果

Mesh4D在Objaverse子集基准上对几何重建和跟踪任务进行了全面评估，与三类代表性基线方法进行对比：静态图像到3D重建方法**HY3D 2.1**（Tencent Hunyuan3D Team, 2025，逐帧应用）、前馈4D高斯重建方法**L4GM**（Ren et al., NeurIPS 2024），以及视频到4D高斯生成方法**GVFD**（Zhang et al., ICCV 2025）。

如Table 1所示，Mesh4D在所有几何与跟踪指标上均显著超越先前最优方法。在体积IoU上，Mesh4D达到0.3949，相比HY3D 2.1的0.3071提升了28.6%（+0.0878）；在点到表面距离（P2S）上，Mesh4D取得0.0261，较GVFD的0.0345降低了24.4%；在Chamfer距离上，Mesh4D为0.0243，相比GVFD的0.0378降低了35.7%。在跟踪精度方面，Mesh4D的ℓ2-Corr误差仅为0.0338，较GVFD的0.0514降低了34.2%。

值得注意的是，3D-GS类方法（L4GM、GVFD）由于未显式定义内外表面，无法计算体积IoU指标，这进一步凸显了网格表示在几何评估完整性上的优势。

定性结果（Figure 4）揭示了各方法的典型失败模式：HY3D 2.1因缺乏时序信息，在姿态和形状估计上出现明显偏差；而L4GM和GVFD虽然能生成视觉上可接受的结果，但因忽视几何监督，姿态估计不准确（Figure 5）。相比之下，Mesh4D凭借时空注意力机制，能够同时保持几何精度和时序一致性。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2601_05251/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results on geometry reconstruction. We show both the normal map and the error map (the bluer the better). HY3D 2.1 [45] suffers from inaccurate pose and shape estimation due to the lack of temporal information. Thanks to the spatio-temporal attention, our method manages to reconstruct the mesh that follows the given input frames with accurate pose and similar shape*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2601_05251/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results on novel view synthesis. All the state-of-the-art methods suffer from inaccurate pose estimation, either due to lack of temporal attention (HY3D [45]) or neglect the importance of geometric supervision (GVDF [71], L4GM [41]). 3D-GS based methods occasionally exhibit ghost artifacts because they lack topology constraints during deformation, while the frame-wise reconstruction method produce inconsistent shape and texture. Moreover, by leveraging a large reconstruction method, we avoid predicting extremely incorrect canonical mesh. Thanks to the skeleton information and spatio-temporal attention, Mesh4D is able to reconstruct accurate pose and geometry, and produces tempor...*

在新视角合成任务上（Table 2），Mesh4D在PSNR、SSIM、LPIPS和FVD等帧级质量和视频一致性指标上均达到最优，仅在CLIP分数上略逊于部分基线——这是因为Mesh4D的纹理仅从第一帧生成，而非利用完整视频信息。

### 消融实验

为验证核心设计选择的有效性，研究者在变形VAE上进行了系统的消融实验（Table 3）。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2601_05251/figures/009_Table_3.jpg]]
*Table 3: Quantitative ablation study for our deformation VAE on our proposed benchmark, a subset of Objaverse. We demonstrate the effectiveness of our key designs*

**骨架信息的作用。** 移除变形VAE中的骨架信息（蒙皮权重和骨骼）后，模型性能出现严重退化：Chamfer距离从0.0243升至0.0286（相对增加17.7%），ℓ2-Corr误差从0.0338升至0.0394（相对增加16.6%）。定性可视化（Figure 6）进一步表明，缺乏骨架先验时，模型无法正确恢复刚性变换，导致网格出现扭曲变形。这一现象的根本原因在于，蒙皮权重为自注意力和交叉注意力提供了强结构偏置，使得模型能够将属于同一骨骼的点关联起来，从而更准确地捕捉关节运动模式。

**时空注意力的作用。** 将时空注意力替换为简单的逐帧编码后，模型输出出现明显的运动抖动和局部误差增大（Figure 6），定量指标亦全面下降。这表明，仅靠逐帧独立编码无法捕获全局运动一致性，时空注意力对于平滑变形预测至关重要。

**预训练权重的影响。** 在变形扩散模型上，使用预训练权重对性能至关重要（Table 5）。从零开始训练扩散模型会导致所有指标大幅下降，验证了利用大规模预训练3D扩散模型作为先验的必要性。这一发现与核心洞察一致：变形潜码的生成需要强3D先验，而预训练模型恰好提供了这一基础。

**分类器自由引导（CFG）的意外发现。** 与文本到图像/3D生成中的常见做法不同，在变形扩散模型中引入CFG并未提升重建质量，反而导致性能略微下降（Table 4）。研究者推测，这是因为变形生成任务更依赖精确的几何条件而非多样性，CFG的引导尺度可能干扰了条件信号的忠实传递。

### 失败模式分析

Mesh4D存在以下几类典型失败场景（Figure 8）：

1. **拓扑变化失效。** 模型假设网格拓扑在动画过程中保持不变。当物体发生显著拓扑变化（如部件分离、孔洞出现）时，基于固定拓扑的变形场无法表达此类变化，导致重建失败。这是方法设计的根本性限制。

2. **规范网格重建误差传播。** 由于变形场以第一帧的规范网格为基础，若HY3D 2.1在第一帧的重建出现错误（如形状估计偏差），该误差会通过变形场传播至所有后续帧，造成系统性偏差。

3. **分布外泛化受限。** 模型依赖在Objaverse合成数据上预训练的3D重建模型，其泛化能力受限于该预训练数据的分布。对于训练分布外的物体类别或运动模式，规范网格质量和变形预测精度均可能下降。

4. **训练数据需求。** 变形VAE的训练需要每帧对应的顶点数据及骨架标注，这限制了在非合成视频上的扩展应用。推理阶段虽无需骨架信息，但训练数据的制作成本仍构成实际部署的瓶颈。

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2601_05251/figures/003_Table_1.jpg]]
*Table 1: Quantitative evaluation for geometry and tracking on our proposed benchmark, a subset of Objaverse. All instantiations of our model outperform previous state-of-the-art models. 3D-GS based methods do not explicitly define inner or outer surface, so it is not applicable for volumatric IoU evaluation. Besides, HY3D [45] and L4GM [41] predict independent mesh or points per-frame, which do not support tracking evaluation directly*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2601_05251/figures/010_Table_4.jpg]]
*Table 4: Ablation study for classifier-free guidance (CFG). The one without using CFG get slightly better results*

![[assets/figures/papers/paper_list_l32_https_arxiv_org_abs_2601_05251/figures/002_Figure_2.jpg]]
*Figure 2: Overall Deformation VAE pipeline. (Left) Given a sequence of 3D meshes as input, we first uniformly sample a sequence of corresponding points. We inject the skeleton information by using masked self- and cross-attention. Then, a Farthest Point Sampling (FPS) at spatial dimension is performed to compress the latent, followed by 8 layers of spatio-temporal attention. The deformation field is decoded by layers of spatio-temporal attention, followed by a cross attention where canonical vertices serve as query points. (Right) Each of our spatio-temporal attention layers sequentially performs temporal attention, global attention, and spatial attention. For temporal and global attention, we additi...*

## 定位与知识库关联

**Mesh4D** 处于单目视频到4D重建这一前沿线上，其设计思路与现有工作形成了清晰的对比与继承关系。

### 与基线方法的关系

**相对于逐帧静态重建的突破。** 最直接的基线是 **Hunyuan3D 2.1 (HY3D)**（Tencent Hunyuan3D Team, 2025），将其逐帧应用于视频序列。该方法缺乏时序信息，导致姿态和形状估计不准确（Figure 4）。Mesh4D 的核心改进在于：通过时空注意力将整个视频序列的变形信息编码到单个紧凑潜在空间，使模型能够利用全局运动模式约束每一帧的重建。定量上，Mesh4D 在 IoU 指标上从 HY3D 的 0.3071 提升至 0.3949（Table 1），验证了时序建模的关键作用。

**相对于4D高斯方法的优势。** **L4GM**（Ren et al., NeurIPS 2024）和 **GVFD**（Zhang et al., ICCV 2025）代表了基于3D高斯泼溅（3D-GS）的前馈4D重建路线。这类方法虽然在渲染质量上有优势，但存在两个根本性局限：一是3D-GS不显式定义内外表面，无法计算体积IoU；二是缺乏几何监督，导致姿态估计不准确（Figure 5）。Mesh4D 以显式网格为输出，在几何重建指标上全面超越：Chamfer距离从 GVFD 的 0.0378 降至 0.0243，P2S 从 0.0345 降至 0.0261（Table 1）。更重要的是，Mesh4D 的网格输出保证了拓扑一致性，而3D-GS方法难以维持跨帧的顶点对应关系，这直接体现在跟踪精度 ℓ2-Corr 从 0.0514 降至 0.0338 的显著提升上。

**变形编码范式的升级。** 传统方法如 Motion2VecSet 仅编码两帧之间的变形，缺乏对长序列全局运动模式的建模。Mesh4D 的变形VAE采用8层时空注意力，交替执行时间注意力、全局注意力和空间注意力（Figure 2），将整个动画序列的变形压缩到单个潜码中。这一设计使得扩散模型能够以视频特征和规范网格为条件，一次性生成完整的时序变形场，而非逐帧独立预测。

### 方法适用边界与局限

**拓扑不变性假设是根本约束。** Mesh4D 假设网格拓扑在动画过程中保持不变，这直接排除了处理拓扑变化场景的可能性（Figure 8 展示了典型失败案例）。当物体发生显著的拓扑变化（如物体分裂、融合或出现新的孔洞）时，变形场无法表达此类不连续变化，模型必然失败。

**规范帧重建质量构成性能上限。** 整个变形管线建立在第一帧重建的静态网格之上，规范网格的错误会传播到所有后续帧。模型依赖 **Hunyuan3D 2.1** 作为规范网格重建器，其泛化能力受限于该预训练模型的训练数据分布。当输入视频中的物体类别或外观显著偏离 Objaverse 数据分布时，初始网格的质量下降将成为瓶颈。

**训练数据需求限制了可扩展性。** 变形VAE的训练需要每帧对应的顶点数据和骨架信息（蒙皮权重和骨骼），这些标注在非合成视频中极难获取。虽然推理时不需要骨架信息（仅作为训练时的特权先验），但训练数据本身的制作成本限制了模型向真实世界视频的迁移。

**纹理生成的时序一致性未充分验证。** 纹理模块仅基于第一帧生成PBR纹理，并假设其在动画过程中保持不变。对于存在显著光照变化或非刚性外观变化的场景（如衣物褶皱导致的阴影变化），这一简化假设可能导致渲染结果不够真实。

### 开放问题

1. **规范帧的自适应选择。** 当前方法固定使用第一帧作为规范帧，但当第一帧存在严重遮挡或非典型姿态时，重建质量会显著下降。如何自动选择最优规范帧，或融合多帧信息构建规范网格，是一个有待探索的方向。

2. **相机运动与背景变化的处理。** 现有方法假设相机固定或运动已知，且背景相对简单。在真实场景中，同时估计相机运动、物体变形和背景变化是一个更具挑战性的联合优化问题。

3. **长序列与多物体扩展。** 变形VAE的潜码维度固定，对视频长度的扩展性有限。同时，当前方法仅处理单个物体，多物体场景的交互建模需要全新的架构设计。

4. **减少对骨架标注的依赖。** 能否通过自监督或弱监督学习（如利用光流、深度估计等辅助信号）替代昂贵的骨架标注，是降低训练成本、提升方法实用性的关键方向。消融实验已证明骨架信息对性能至关重要（去除后指标大幅下降，Figure 6），但这是否意味着骨架是唯一有效的运动先验，仍需进一步研究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Mesh4D_4D_Mesh_Reconstruction_and_Tracking_from_Monocular_Video.pdf]]
