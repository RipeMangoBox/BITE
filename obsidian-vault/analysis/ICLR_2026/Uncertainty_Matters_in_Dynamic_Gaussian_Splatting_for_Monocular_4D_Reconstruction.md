---
title: Uncertainty Matters in Dynamic Gaussian Splatting for Monocular 4D Reconstruction
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Uncertainty_Matters_in_Dynamic_Gaussian_Splatting_for_Monocular_4D_Reconstructio_f0906ec8357c.pdf
project_link: "https://tamu-visual-ai.github.io/usplat4d/"
code_link: null
aliases:
- UMDGSM4R
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 引入时间变化的高斯不确定性估计，构建不确定性感知的时空图，通过可靠高斯传播运动信息，引导整体优化。
primary_logic: 经常被观测到的高斯应作为可靠锚点，利用其运动信息约束观测不足的区域，从而提升4D重建的时空一致性和极端视角下的鲁棒性。
claims:
- 在DyCheck 7场景2x分辨率下，USPLAT4D（以MoSca为基础）的PSNR达到19.63，超越MoSca的19.32。
- "在Objaverse的大视角偏移(120°,180°]下，USPLAT4D（基于SoM）PSNR提升0.58，LPIPS降低0.05。"
- 消融实验中移除关键节点不确定性估计导致PSNR从19.63降至18.86。
- 消融实验中移除UA-kNN（替换为距离基kNN）导致PSNR降至19.50。
---

# Uncertainty Matters in Dynamic Gaussian Splatting for Monocular 4D Reconstruction

> [!tip] 核心洞察
> 经常被观测到的高斯应作为可靠锚点，利用其运动信息约束观测不足的区域，从而提升4D重建的时空一致性和极端视角下的鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 单目4D重建中动态高斯泼溅的不确定性建模 |
| 英文题名 | Uncertainty Matters in Dynamic Gaussian Splatting for Monocular 4D Reconstruction |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=m3rZ7Fdlst) · [Project](https://tamu-visual-ai.github.io/usplat4d/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | USPLAT4D |
| Dataset | DyCheck, Objaverse |

> [!tip] 效果简介
> - DyCheck 上，mPSNR 19.63 (MoSca base) vs 19.32 (MoSca) (+0.31)；mSSIM 0.716 (MoSca base) vs 0.706 (MoSca) (+0.010)；mLPIPS 0.25 (MoSca base) vs 0.26 (MoSca) (-0.01)。
> - Objaverse 上，PSNR (120°-180°) 17.03 (SoM base) vs 16.45 (SoM) (+0.58)；LPIPS (120°-180°) 0.26 (SoM base) vs 0.31 (SoM) (-0.05)。

## 概要

单目动态场景的4D重建（即从一段视频中恢复随时间变化的3D几何与外观）是计算机视觉中的核心挑战。现有基于**3D高斯泼溅（3D Gaussian Splatting）** 的动态重建方法——如**SoM**（Shape-of-Motion, Wang et al., 2025a）、**MoSca**（Lei et al., 2025）、**SC-GS**（Huang et al., 2024）和**4DGS**（Wu et al., 2024）——在优化过程中对所有高斯点一视同仁，忽略了不同高斯点在不同时刻由于遮挡、视角偏移等因素导致的**观测可靠性差异**。这一“均匀对待”的策略在极端新视角下容易产生运动漂移和合成质量退化（见图1）。

本文提出**USPLAT4D**，一个**不确定性感知的动态高斯泼溅框架**。其核心思想是：经常被稳定观测到的高斯点应作为“可靠锚点”，利用其运动信息约束那些观测不足或不可靠的区域，从而提升整体4D重建的时空一致性和极端视角下的鲁棒性。

具体而言，USPLAT4D引入三个关键模块：
- **动态不确定性估计**：为每个高斯点估计时间变化的各向异性不确定性，量化其在每一帧的可靠性。
- **不确定性编码图构建**：根据不确定性选择高置信度的“关键节点”，并构建不确定性感知的k近邻（UA-kNN）时空图，使可靠节点的运动信息得以有效传播。
- **不确定性感知优化**：通过不确定性加权的损失函数分别优化关键节点与非关键节点，引导整体训练。

**实验效果**：在DyCheck数据集上，以MoSca为基础模型的USPLAT4D在7个场景2倍分辨率下将PSNR从19.32提升至19.63；在Objaverse数据集的大视角偏移（120°~180°）条件下，以SoM为基础模型的USPLAT4D将PSNR从16.45提升至17.03，LPIPS从0.31降至0.26。消融实验证实，移除关键节点的不确定性估计会导致PSNR骤降至18.86，而将UA-kNN替换为普通距离基kNN则使PSNR降至19.50，验证了不确定性建模在图构建与优化中的关键作用。

该方法在无纹理区域、快速运动场景及高度可变形对象上仍存在局限性，但其“不确定性引导运动传播”的范式为动态高斯泼溅的鲁棒优化提供了新的思路。

### 单目动态场景重建的挑战

从单目视频中重建随时间变化的4D场景是计算机视觉中的核心难题。给定一段单目相机拍摄的动态视频，目标是在任意视角和时间戳下合成逼真的新视图。这一任务在增强现实、自由视点视频、电影制作等领域具有重要应用价值，但由于单目输入固有的深度-运动耦合模糊性和观测稀疏性，重建的时空一致性和极端视角下的合成质量始终面临严峻挑战。

近年来，以3D Gaussian Splatting（3DGS）为代表的显式辐射场方法凭借实时渲染和高保真度重建的优势，迅速成为静态场景重建的主流范式。研究者们进一步将其扩展至动态场景，涌现出一系列动态高斯泼溅方法：**4DGS**（Wu et al., 2024）直接将高斯拓展到4D时空域；**SC-GS**（Huang et al., 2024）利用场景流建模运动；**SoM**（Wang et al., 2025a）采用共享规范场和运动基元分解；**MoSca**（Lei et al., 2025）则构建运动脚手架来约束高斯轨迹。这些方法在验证视角（通常靠近训练轨迹）上取得了令人瞩目的重建效果。

### 现有方法的瓶颈：忽视观测可靠性差异

然而，现有动态高斯泼溅方法存在一个共同的盲点：**它们对所有高斯一视同仁地进行均匀优化，完全忽略了不同高斯在观测可靠性上的巨大差异**。在实际的单目视频中，场景的不同区域在不同时刻被观测到的频率和质量极不均衡——某些区域（如始终面向相机的表面）被频繁且清晰地观测，而遮挡区域、背面结构或极端视角下的区域则观测稀少甚至完全不可见。

这种均匀优化策略导致两个严重后果：
1. **遮挡区域的运动漂移**：当高斯在部分帧中被遮挡时，缺乏可靠观测信号约束，其位置和运动参数容易在优化中发生漂移，破坏时空一致性。
2. **极端视角下的合成退化**：对于远离训练轨迹的新视角，由于对应区域的高斯从未被充分观测，渲染质量急剧下降，出现模糊、断裂或几何失真（见图1中SoM在视角1和视角2的失败案例）。

### 核心动机：不确定性建模与可靠运动传播

本文的核心洞察在于：**经常被观测到的高斯应当作为可靠锚点，利用其运动信息约束观测不足的区域**。这一思路将单目4D重建问题重新表述为一个不确定性感知的时空信息传播问题——先识别出哪些高斯是“可信的”，再通过它们将运动线索传递给“不可信的”高斯，从而在全局层面提升重建的时空一致性和鲁棒性。

基于这一动机，我们提出**USPLAT4D**（Uncertainty-aware dynamic Gaussian Splatting for 4D reconstruction），一个不确定性感知的动态高斯泼溅框架。该方法首次为每个高斯显式估计时间变化的各向异性不确定性，并以此为核心构建不确定性编码的时空图，通过可靠高斯引导整体优化，显著改善了遮挡区域和极端视角下的重建质量。

## 核心方法与创新机理

USPLAT4D 的核心创新在于将**时间变化的高斯不确定性估计**引入动态高斯泼溅（Dynamic Gaussian Splatting）框架，并以此构建**不确定性感知的时空运动图**，从根本上改变了现有方法对场景中所有高斯均匀优化的范式。这一设计直接回应了单目 4D 重建中观测可靠性差异的核心瓶颈：在遮挡、极端视角和稀疏观测区域，缺乏可靠性区分会导致运动漂移与合成质量退化。

### 从均匀优化到不确定性加权优化

现有动态高斯泼溅方法（如 **MoSca** (Lei et al., 2025)、**SoM** (Wang et al., 2025a)）在优化过程中对所有高斯一视同仁，未区分其在不同帧中的观测可靠性。USPLAT4D 的核心改变体现在三个紧密耦合的 **changed slots** 上：

| 设计维度 | Baseline 做法 | USPLAT4D 做法 | 关键机制 |
|---------|-------------|-------------|---------|
| **运动优化策略** | 均匀优化所有高斯，无可靠性区分 | 基于不确定性分离关键/非关键节点，不确定性加权优化 | 高置信度高斯作为运动锚点，通过图传播约束低置信度区域 |
| **不确定性建模** | 无或弱辅助信号（如软运动分数） | 逐高斯时间变化各向异性不确定性估计 | 从光度损失推导闭式方差，经相机旋转传播至 3D 空间 |
| **图构建** | 距离基 kNN 或未使用不确定性 | 不确定性感知 kNN、关键节点选择与边构建 | 马氏距离替代欧氏距离，不确定性决定节点间连接强度 |

这三个维度的改变构成了一个完整的因果链条：**不确定性估计**为每个高斯提供逐帧可靠性信号 → **图构建**利用这些信号筛选可靠锚点并建立有意义的时空连接 → **优化策略**通过逆不确定性加权，让高置信度高斯主导运动传播，低置信度高斯受其约束。

### 不确定性估计：从 2D 误差到 3D 各向异性度量

USPLAT4D 的不确定性估计具有明确的物理含义。对于帧 $t$ 中的高斯 $i$，其颜色不确定性方差由混合权重推导的闭式解给出：

$$\sigma_{i,t}^2 = \left( \sum_{h \in \Omega_{i,t}} (T_{i,t}^h \alpha_i)^2 \right)^{-1}$$

这一公式基于局部最小值假设：被多个像素以高混合权重观测到的高斯具有较低的渲染不确定性。为处理未收敛区域，论文引入像素收敛指示函数，将未收敛高斯的不确定性设为一个大常数 $\phi$：

$$u_{i,t} = \mathbb{1}_{i,t} \sigma_{i,t}^2 + (1 - \mathbb{1}_{i,t}) \phi$$

关键的创新在于将 2D 标量不确定性提升为 3D 各向异性形式。通过相机旋转矩阵 $\mathbf{R}_{wc}$ 和轴对齐缩放因子，2D 不确定性被传播到世界坐标系：

$$\mathbf{U}_{i,t} = \mathbf{R}_{wc} \mathbf{U}_c \mathbf{R}_{wc}^{\mathsf{T}}$$

这一设计使得不确定性矩阵能够反映不同空间方向上的观测可靠性差异，而非简单的标量加权。消融实验证实了这一设计的必要性：移除关键节点的不确定性估计导致 PSNR 从 19.63 骤降至 18.86（Table 3），表明各向异性不确定性是运动传播准确性的关键保障。

### 不确定性感知图：从空间邻近到可靠性驱动的连接

图构建的创新体现在两个层面。首先，**关键节点的选择**不再仅依赖空间采样，而是结合了不确定性筛选：通过 3D 体素网格采样候选节点，再以显著周期阈值（≥5 帧）过滤，确保关键节点是时空稳定的可靠高斯。其次，**边构建**采用不确定性加权的马氏距离替代传统欧氏距离：

$$\mathcal{E}_i = k\mathrm{NN}_{j \in \mathcal{V}_k \setminus \{i\}} \left( \lVert \mathbf{p}_{i,\hat{t}} - \mathbf{p}_{j,\hat{t}} \rVert_{(\mathbf{U}_{w,\hat{t},i} + \mathbf{U}_{w,\hat{t},j})} \right)$$

这意味着两个高不确定性高斯之间的连接会被有效削弱，避免不可靠的运动信息在图结构中传播。消融实验中，将 UA-kNN 替换为距离基 kNN 导致 PSNR 降至 19.50（Table 3），验证了不确定性感知的边构建对性能的实质贡献。

### 不确定性引导的优化：分层损失与可靠性加权

优化阶段的分层设计是 USPLAT4D 区别于 baseline 的另一关键。关键节点损失鼓励其接近预优化位置，并按**逆不确定性**加权：

$$\mathcal{L}^{\mathrm{key}} = \sum_{t=0}^{T-1} \sum_{i \in \mathcal{V}_k} \| \mathbf{p}_{i,t} - \mathbf{p}_{i,t}^{\mathrm{o}} \|_{\mathbf{U}_{w,t,i}^{-1}} + \mathcal{L}^{\mathrm{motion,key}}$$

非关键节点损失则同时约束其接近初始位置和 DQB 插值轨迹，同样以逆不确定性加权。这一设计的因果逻辑清晰：高不确定性（不可靠）的高斯被赋予较小的损失权重，允许其灵活调整；低不确定性（可靠）的高斯被严格约束，作为运动传播的稳定锚点。移除训练中的不确定性加权导致 PSNR/SSIM 同时下降（Table 3），证实了加权机制对整体优化的必要性。

### 创新点的协同效应

三个 changed slots 并非孤立改进，而是形成了正向协同：不确定性估计为图构建提供了节点可靠性依据，图构建将可靠性信息编码为空间拓扑结构，优化策略则利用这一结构实现差异化的运动约束。这种协同在极端视角下尤为显著——Objaverse 数据集 (120°, 180°] 视角范围内，USPLAT4D 相较 SoM 的 PSNR 提升 0.58、LPIPS 降低 0.05（Table 2），而小视角偏移下的提升幅度较小，直接印证了不确定性引导的运动传播在观测稀疏区域的核心价值。

USPLAT4D 的整体流程围绕一个核心思想构建：在动态高斯泼溅中，并非所有高斯点具备同等的观测可靠性——经常被稳定观测到的高斯应作为可靠锚点，其运动信息可传播至观测不足的区域，从而约束整体 4D 重建的时空一致性。基于此，方法将动态高斯泼溅的优化过程重构为三个阶段：**动态不确定性估计**、**不确定性编码图构建** 与 **不确定性感知优化**（Figure 2）。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_m3rZ7Fdlst/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed USPLAT4D. We first estimate time-varying uncertainty for each Gaussian (Section 4.1). We then leverage these uncertainties to select reliable Gaussians as key nodes, while others are treated as non-key nodes for graph construction (Section 4.2). Finally, we optimize the spatio-temporal graph with uncertainty-weighted losses, yielding consistent 4D Gaussians (Section 4.3). The right column shows that our approach significantly improves novel view renderings compared to vanilla optimization*

**输入与输出流**：方法以单目动态视频为输入，首先由现有动态高斯泼溅基线（如 **SoM** (Wang et al., 2025a) 或 **MoSca** (Lei et al., 2025)）产生初始的时空高斯场作为先验。随后，USPLAT4D 为每个高斯估计逐帧的时间变化不确定性，利用该不确定性构建时空图，并通过不确定性加权的损失函数对高斯场进行精细优化，最终输出时空一致的 4D 高斯表示，支持任意视角与时间戳的新视图合成。

**模块间关系**：三个模块构成递进依赖关系。不确定性估计模块（Section 4.1）为后续图构建提供每个高斯的可靠性度量；图构建模块（Section 4.2）依据不确定性将高斯划分为关键节点与非关键节点，并建立不确定性感知的图连接；优化模块（Section 4.3）利用图结构与不确定性权重，分别对关键节点和非关键节点施加差异化约束，引导整体高斯场的运动传播与几何收敛。

**不确定性估计模块**：该模块从光度误差出发，为每个高斯 $\mathbf{G}_i$ 在每帧 $t$ 估计一个标量不确定性 $u_{i,t}$。具体而言，在像素收敛假设下，从混合权重推导出闭式方差估计 $\sigma_{i,t}^2 = (\sum_{h \in \Omega_{i,t}} (T_{i,t}^h \alpha_i)^2)^{-1}$（Equation 3），并融合像素收敛指示函数得到最终标量不确定性（Equation 5）。随后，通过摄像机旋转将 2D 不确定性传播至 3D，形成各向异性不确定性矩阵 $\mathbf{U}_{i,t} = \mathbf{R}_{wc} \mathbf{U}_c \mathbf{R}_{wc}^{\mathsf{T}}$（Equation 6），以反映高斯在不同空间方向上的可靠性差异。

**图构建模块**：基于不确定性，模块首先通过 3D 体素网格采样与显著周期阈值（≥5 帧）筛选出高可靠性的关键节点 $\mathcal{V}_k$，其余高斯归为非关键节点 $\mathcal{V}_n$。关键节点之间通过不确定性感知的 kNN 构建边（Equation 7），以马氏距离替代欧氏距离，使高不确定性方向上的距离被有效拉伸。每个非关键节点则附着于序列中与其不确定性加权距离最小的关键节点（Equation 8），从而形成完整的时空传播图。

**优化模块**：最终优化目标由三部分构成——光度损失 $\mathcal{L}^{\mathrm{rgb}}$、关键节点损失 $\mathcal{L}^{\mathrm{key}}$ 与非关键节点损失 $\mathcal{L}^{\mathrm{non-key}}$（Equation 12）。关键节点损失鼓励其接近预优化位置，并按逆不确定性加权，使低不确定性节点受到更强约束（Equation 9）；非关键节点损失同时约束其接近初始位置及基于图的插值轨迹（DQB），同样以逆不确定性加权（Equation 11）。不确定性在此框架中扮演三重角色：重加权关键节点偏差、引导非关键节点插值、以及在总损失中平衡各节点的影响权重。

**设计瓶颈与因果机制**：现有动态高斯泼溅方法（如 SoM、MoSca）对所有高斯均匀优化，忽略了因遮挡、视角偏移等因素导致的观测可靠性差异，这是造成运动漂移与极端视角合成退化的核心瓶颈。USPLAT4D 通过引入时间变化的不确定性估计，将“经常被观测到的高斯”识别为可靠锚点，利用其运动信息通过图结构传播至观测稀疏区域，从而在因果层面改善了时空一致性与极端视角鲁棒性。消融实验证实了这一因果链：移除关键节点的不确定性估计导致 PSNR 从 19.63 降至 18.86（Table 3），移除不确定性感知 kNN 则降至 19.50，验证了不确定性在节点选择与图构建中的关键作用。

USPLAT4D 的核心设计围绕一个中心命题展开：并非所有高斯对 4D 重建的贡献是等价的。经常被多帧观测到的区域应作为“可靠锚点”，其运动信息通过图结构传播至观测稀疏的区域。这一思想通过三个紧密耦合的模块实现：动态不确定性估计、不确定性编码图构建、以及不确定性感知优化。

### 4.1 动态不确定性估计

**动机**：现有动态高斯泼溅方法对所有高斯均匀优化，忽略了各高斯在不同时间帧上观测可靠性的差异。在遮挡或极端视角下，缺乏可靠观测的高斯容易产生运动漂移。

**核心机制**：为每个高斯 $\mathbf{G}_i$ 在每帧 $t$ 估计一个时变不确定性，量化其在该帧的可靠性。该过程分三步完成。

**步骤一：像素级误差建模**。首先计算帧 $t$ 的光度损失：

$$\mathcal{L}_{2,t} = \sum_{h \in \Omega} \| \bar{C}_t^h - C_t^h \|_2^2 \tag{2}$$

其中 $\bar{C}_t^h$ 为渲染颜色，$C_t^h$ 为真值颜色。基于局部最小值假设——即每个像素的颜色可近似由贡献最大的高斯独立解释——从混合权重推导出闭式方差估计：

$$\sigma_{i,t}^2 = \left( \sum_{h \in \Omega_{i,t}} (T_{i,t}^h \alpha_i)^2 \right)^{-1} \tag{3}$$

其中 $T_{i,t}^h$ 为累积透射率，$\alpha_i$ 为不透明度，$\Omega_{i,t}$ 为高斯 $i$ 在帧 $t$ 中有贡献的像素集合。该估计的直觉是：混合权重越大，该高斯对像素颜色的解释力越强，不确定性越低。

**步骤二：像素收敛指示融合**。引入指示函数 $\mathbb{1}_{i,t}$ 标记像素是否已收敛，得到最终标量不确定性：

$$u_{i,t} = \mathbb{1}_{i,t} \sigma_{i,t}^2 + (1 - \mathbb{1}_{i,t}) \phi \tag{5}$$

其中 $\phi$ 为预设的大常数，确保未收敛高斯获得高不确定性，避免其过早主导优化。

**步骤三：2D→3D 各向异性传播**。由于图像空间的不确定性在 3D 空间中具有方向性（沿视线方向不确定性更大），将标量不确定性提升为各向异性矩阵。首先构建相机坐标系下的对角不确定性 $\mathbf{U}_c = \mathrm{diag}(r_x u_{i,t}, r_y u_{i,t}, r_z u_{i,t})$，其中 $r_x, r_y, r_z$ 为轴对齐缩放因子。然后通过相机旋转将其变换到世界坐标系：

$$\mathbf{U}_{i,t} = \mathbf{R}_{wc} \mathbf{U}_c \mathbf{R}_{wc}^{\mathsf{T}} \tag{6}$$

其中 $\mathbf{R}_{wc}$ 为相机到世界的旋转矩阵。注意此处仅需旋转而不需平移，因为不确定性描述的是相对偏差的分布。这一各向异性表示使后续图构建和优化能区分不同方向上的可靠性差异。

### 4.2 不确定性编码图构建

**动机**：直接对所有高斯建立全连接图计算代价过高，且不可靠高斯会污染运动传播。需要基于不确定性筛选可靠节点并建立稀疏连接。

**关键节点选择**。采用两步筛选策略：(1) 通过 3D 体素网格采样获取候选节点，确保空间覆盖；(2) 按“显著周期”阈值过滤，仅保留在至少 5 帧中被持续观测的候选节点作为关键节点 $\mathcal{V}_k$。其余高斯归为非关键节点 $\mathcal{V}_n$。

**不确定性感知 kNN 边构建**。关键节点之间基于马氏距离建立边连接，距离按不确定性加权：

$$\mathcal{E}_i = k\mathrm{NN}_{j \in \mathcal{V}_k \setminus \{i\}} \left( \| \mathbf{p}_{i,\hat{t}} - \mathbf{p}_{j,\hat{t}} \|_{(\mathbf{U}_{w,\hat{t},i} + \mathbf{U}_{w,\hat{t},j})} \right) \tag{7}$$

其中 $\hat{t}$ 为参考帧。马氏距离的核心效果是：在不确定性高的方向上“拉伸”距离度量，使得该方向上即使空间距离较近的节点也不易建立边连接；反之，在不确定性低的方向上“压缩”距离，促进可靠节点间的连接。这确保了运动信息仅沿高置信度路径传播。

**非关键节点附着**。每个非关键节点 $i$ 被分配给使其跨帧不确定性加权距离最小的关键节点 $j$：

$$j = \arg\min_{l \in \mathcal{V}_k} \sum_{t=0}^{T-1} \| \mathbf{p}_{i,t} - \mathbf{p}_{l,t} \|_{(\mathbf{U}_{w,t,i} + \mathbf{U}_{w,t,l})}$$

这一设计的因果逻辑是：非关键节点（通常对应观测稀疏或遮挡区域）的运动应由其最“信任”的关键节点（观测充分且空间邻近）来约束。

### 4.3 不确定性感知优化

**动机**：在联合优化中，不同节点的损失贡献应按其可靠性加权，避免不可靠区域主导梯度。

**关键节点损失**。鼓励关键节点接近其预优化位置 $\mathbf{p}_{i,t}^\mathrm{o}$，并按逆不确定性加权：

$$\mathcal{L}^{\mathrm{key}} = \sum_{t=0}^{T-1} \sum_{i \in \mathcal{V}_k} \| \mathbf{p}_{i,t} - \mathbf{p}_{i,t}^{\mathrm{o}} \|_{\mathbf{U}_{w,t,i}^{-1}} + \mathcal{L}^{\mathrm{motion,key}} \tag{9}$$

逆不确定性加权的效果是：高不确定性方向上的位置偏差惩罚较小（允许在该方向上灵活调整），低不确定性方向上的偏差惩罚较大（强制保持精确）。$\mathcal{L}^{\mathrm{motion,key}}$ 为运动正则项，约束关键节点的轨迹平滑性。

**非关键节点损失**。包含两项：(1) 约束其接近初始位置 $\mathbf{p}_{i,t}^\mathrm{o}$；(2) 约束其接近 DQB（Dynamic Query Ball）插值轨迹 $\mathbf{p}_{i,t}^{\mathrm{DQB}}$——该轨迹由其附着的关键节点的运动插值得到：

$$\mathcal{L}^{\mathrm{non.key}} = \sum_{t=0}^{T-1} \sum_{i \in \mathcal{V}_n} \| \mathbf{p}_{i,t} - \mathbf{p}_{i,t}^{\mathrm{o}} \|_{\mathbf{U}_{w,i}^{-1}} + \sum_{t=0}^{T-1} \sum_{i \in \mathcal{V}_n} \| \mathbf{p}_{i,t} - \mathbf{p}_{i,t}^{\mathrm{DQB}} \|_{\mathbf{U}_{w,i}^{-1}} + \mathcal{L}^{\mathrm{motion,non.key}} \tag{11}$$

第二项是运动传播的核心实现：非关键节点的运动轨迹被“锚定”到其关键节点的运动模式上，从而实现从可靠区域向不可靠区域的运动信息传递。

**总损失函数**。最终优化目标为三项之和：

$$\mathcal{L}^{\mathrm{total}} = \mathcal{L}^{\mathrm{rgb}} + \mathcal{L}^{\mathrm{key}} + \mathcal{L}^{\mathrm{non-key}} \tag{12}$$

不确定性在该框架中扮演三重角色：(1) 重加权关键节点的位置偏差惩罚；(2) 引导非关键节点的插值轨迹；(3) 平衡两类节点在总损失中的影响力。消融实验（Table 3）验证了这一设计的必要性：移除关键节点的不确定性估计导致 PSNR 从 19.63 骤降至 18.86；将不确定性感知 kNN 替换为普通距离基 kNN 导致 PSNR 降至 19.50；移除训练中的不确定性加权同样造成性能退化。

## 实验与关键发现

### 核心实验设计逻辑

实验围绕一个核心假设展开：**观测可靠性差异是制约动态高斯泼溅在遮挡与极端视角下性能的瓶颈**。为验证这一点，实验在两个维度上设计评估：(1) 在不同基线上叠加USPLAT4D的不确定性感知框架，检验其作为即插即用模块的通用性；(2) 在常规验证视图与极端新视图两种条件下分别评估，以区分方法在“内插”与“外推”场景下的表现差异。

数据集选择服务于上述逻辑：**DyCheck**（Gao et al., 2022）提供真实单目动态场景，包含7个场景的2×分辨率评估，其验证视图接近训练轨迹，主要测试重建保真度；**Objaverse** 提供合成多视图数据，按水平视角偏移范围 (0°,60°]、(60°,120°]、(120°,180°] 分层评估，其中 (120°,180°] 区间构成严格的极端新视图合成测试。基线覆盖两类代表性动态高斯方法：基于共享规范场的 **SoM**（Wang et al., 2025a）和基于运动支架的 **MoSca**（Lei et al., 2025），均代表当前最优水平。

---

### 主要定量结果

**DyCheck数据集**（Table 1）上，USPLAT4D以MoSca为基础时，7场景2×分辨率下mPSNR达到 **19.63**，较MoSca的19.32提升 **+0.31**；mSSIM从0.706提升至 **0.716**（+0.010）；mLPIPS从0.26降至 **0.25**（-0.01）。以SoM为基础时，5场景1×分辨率下mPSNR从16.33提升至 **16.85**（+0.52）。这一改进幅度在验证视图（接近训练视角）下相对温和，这与实验预期一致——验证视图本身观测充分，不确定性引导的优势空间有限。

**Objaverse数据集**（Table 2）揭示了更关键的规律：在 (120°,180°] 极端视角偏移区间，USPLAT4D（以SoM为基础）的PSNR从16.45跃升至 **17.03**（**+0.58**），LPIPS从0.31降至 **0.26**（**-0.05**）。而在 (0°,60°] 小偏移区间，提升幅度明显收窄。这一梯度式的性能增益直接验证了核心机制——不确定性估计在观测稀疏的极端视角下发挥最大作用，可靠高斯锚点的运动信息有效约束了不可见区域的重建。

> **公平性说明**：DyCheck验证视图接近训练轨迹，因此改进幅度未能完全反映极端新视图合成的优势；作者在可比训练时间下验证了方法有效性（Table S10）。Objaverse上针对大视角偏移的评估更为严格。部分基线结果来自原始论文，可能存在轻微差异（见Table S3注释）。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_m3rZ7Fdlst/figures/022_Table_S.10.jpg]]
*Table S.10: Ablation for comparable time on DyCheck dataset*

---

### 消融实验：不确定性机制的因果链条

Table 3的消融实验逐项拆解不确定性在USPLAT4D中的三个作用环节，形成清晰的因果链条：

| 消融操作 | PSNR | 变化 | 揭示的机制 |
|---------|------|------|-----------|
| 完整USPLAT4D (MoSca base) | 19.63 | — | 基准 |
| 移除关键节点不确定性估计 | 18.86 | **-0.77** | 不确定性是区分可靠/不可靠高斯的必要条件，移除后关键节点选择退化为随机，运动传播失准 |
| 移除UA-kNN（替换为距离基kNN） | 19.50 | -0.13 | 不确定性感知的图构建通过马氏距离（Equation 7）抑制高不确定性方向上的伪连接，纯欧氏距离无法区分观测质量 |
| 移除训练中不确定性加权 | 下降 | 下降 | 损失函数中逆不确定性加权（Equation 9, 11）使优化聚焦于可靠观测，移除后噪声梯度干扰收敛 |

**最大性能降幅（-0.77 PSNR）出现在移除关键节点不确定性估计时**，这表明不确定性机制的核心价值不在于损失加权本身，而在于**识别可靠锚点**——这是整个运动传播图的基础。UA-kNN的移除造成0.13的降幅，说明图拓扑的质量对最终性能有实质影响但非决定性因素。

---

### 极端视角下的定性分析

Figure 4展示了DyCheck上手动采样的极端新视图（红色相机位姿，无真值）。在“haru-sit”场景中，基线方法在狗头部区域产生模糊和几何失真，USPLAT4D保留了更清晰的细粒度结构；在“spin”场景中，手部区域因自遮挡严重，基线出现断裂，USPLAT4D通过不确定性引导的图传播维持了运动连贯性。

Figure 6在Objaverse上的对比进一步验证：在大视角偏移（红色视图）下，SoM和MoSca均出现明显的形状收缩和纹理模糊，USPLAT4D保持了更准确的几何形态。这与Figure 2中“Camel”序列的观察一致——无深度感知不确定性时，骆驼身体出现不自然的收缩，而完整方法保留了正确形状。

---

### 失败模式与边界条件

实验揭示了三个明确的失败模式：

1. **无纹理区域**（Figure S4）：当视觉基础模型产生的轨迹不可靠时，不确定性引导的图无法完全恢复缺失结构。这是方法对上游轨迹质量依赖的固有边界。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_m3rZ7Fdlst/figures/024_Figure_S.4.jpg]]
*Figure S.4: Failure of tracking on textureless surface. The input camera moves in a circular trajectory around a chick that remains quasi-static. We show the tracking and reconstruction results at frame 32 for both SoM and USPLAT4D (ours). Because the chick’s surface lacks texture, the tracks sampled at the initial frame (t = 0) drift and accumulate incorrect motion under SoM, eventually causing the reconstruction to collapse. In contrast, our method is able to partially recover the geometry and produce more stable tracking*

2. **快速运动区域**（Section E.2）：重建继承输入视频的卷帘快门失真，且快速运动对多视图一致性保存构成挑战。不确定性估计本身无法纠正传感器层面的失真。

3. **高度可变形区域**（Section E.3）：当先验严重不准确或观测极度稀疏时，即使不确定性加权也无法弥补信息缺失，重建质量仍然受限。

这些失败模式共同指向一个深层限制：USPLAT4D通过重新分配观测置信度来优化信息传播，但**不能创造新信息**——当所有高斯在某一区域均不可靠时，方法退化为基线水平。

---

### 关键图表结论速查

- **Table 1**：USPLAT4D在DyCheck 7场景2×分辨率上以MoSca为基础达到19.63 mPSNR，超越所有高斯基线。
- **Table 2**：Objaverse (120°,180°] 区间PSNR提升0.58，验证极端视角下的核心优势。
- **Table 3**：移除关键节点不确定性估计导致PSNR骤降0.77，确认识别可靠锚点是方法的核心机制。
- **Figure 4**：极端新视图下USPLAT4D保留细粒度结构（狗头、手部），基线出现模糊或断裂。
- **Figure 7**：关键节点权重矩阵呈块对角结构，表明不确定性引导的图自然形成语义分组，不同块间无连接。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_m3rZ7Fdlst/figures/005_Table_1.jpg]]
*Table 1: Quantitative results on DyCheck. We report results on 5 scenes at 1× resolution and 7 scenes at 2× resolution, following existing protocols. USPLAT4D consistently outperforms state-of-the-art Gaussian Splatting based methods. See Figure 3 for qualitative results on validation views and Figure 4 for extreme views*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_m3rZ7Fdlst/figures/010_Table_3.jpg]]
*Table 3: Ablation study on uncertainty usage and key node selection. We assess the impact of uncertainty estimation and key node selection strategy by removing them from key components in USPLAT4D individually*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_m3rZ7Fdlst/figures/006_Figure_5.jpg]]
*Figure 5: Qualitative results on extreme novel views from DAVIS. For each case, we show an input-view rendering and compare the baseline (SoM (Wang et al., 2025a) or MoSca (Lei et al., 2025)) with our USPLAT4D on an extreme novel view (red). USPLAT4D yields clearer reconstructions under challenging conditions*

## 定位与知识库关联

### 与现有动态高斯泼溅方法的关系

USPLAT4D 的核心贡献不在于提出全新的表示或运动建模范式，而是在现有动态高斯泼溅（Dynamic Gaussian Splatting）框架上引入了**不确定性感知的优化策略**。该方法可与多种基线架构结合，论文中验证了其在两类代表性方法上的有效性：

- **基于共享规范场的动态高斯**：以 **SoM**（Shape-of-Motion，Wang et al., 2025a）为代表，该类方法通过共享规范空间和变形场实现4D重建。USPLAT4D 在 SoM 基础上引入不确定性估计和加权优化，在 Objaverse 数据集的大视角偏移（120°, 180°] 范围内，PSNR 从 16.45 提升至 17.03（+0.58），LPIPS 从 0.31 降至 0.26（-0.05），验证了不确定性建模对规范场方法的增强效果。

- **基于运动脚手架（Motion Scaffold）的动态高斯**：以 **MoSca**（Lei et al., 2025）为代表，该类方法通过显式运动结构约束高斯运动。USPLAT4D 以 MoSca 为基础，在 DyCheck 7场景 2× 分辨率下将 mPSNR 从 19.32 提升至 19.63，mSSIM 从 0.706 提升至 0.716，mLPIPS 从 0.26 降至 0.25，表明不确定性引导的图优化可进一步增强运动脚手架的时空一致性。

论文同时与 **SC-GS**（Huang et al., 2024，基于场景流的动态高斯）和 **4DGS**（Wu et al., 2024，直接4D高斯泼溅）进行了对比，USPLAT4D 在 DyCheck 基准上均取得更优或可比的结果。

### 方法谱系中的定位

从技术路线上看，USPLAT4D 属于**优化策略层面的改进**，而非表示层面或运动建模层面的创新。其方法谱系可归纳为：

1. **不确定性来源**：不同于依赖额外不确定性预测网络的方法，USPLAT4D 从渲染过程中的混合权重（blending weights）出发，基于局部最小值假设推导出**闭式方差估计**（Equation 3），并通过相机旋转将其从2D传播到3D，形成各向异性不确定性矩阵（Equation 6）。这种估计方式无需额外训练参数，计算开销低，且与高斯泼溅的渲染管线自然兼容。

2. **图构建策略**：现有动态高斯方法多采用距离基 kNN 构建时空图（如 MoSca），或完全不使用图结构。USPLAT4D 提出**不确定性感知 kNN（UA-kNN）**，以马氏距离替代欧氏距离进行关键节点间的边构建（Equation 7），使连接倾向于在低不确定性方向上延伸。消融实验显示，将 UA-kNN 替换为距离基 kNN 会导致 PSNR 从 19.63 降至 19.50，验证了不确定性在拓扑构建中的关键作用。

3. **节点角色分离**：USPLAT4D 将高斯显式划分为**关键节点**（高可靠性、经常被观测）和**非关键节点**（观测稀疏或遮挡区域），并赋予不同的损失函数。关键节点损失约束其接近预优化位置（Equation 9），非关键节点损失则约束其接近初始位置及动态查询基（DQB）插值轨迹（Equation 11）。这种分离优化策略使可靠区域的运动信息可通过图结构传播至不可靠区域。

### 适用边界与局限

尽管 USPLAT4D 在多个基准上展现了有效性，其适用边界受以下因素制约：

- **无纹理区域的退化**：不确定性估计依赖于渲染过程中的混合权重，当场景存在大面积无纹理区域时，视觉基础模型产生的轨迹不可靠，不确定性引导的图无法完全恢复缺失结构（见 Figure S4）。这是所有基于光度信号的方法共有的瓶颈。

- **快速运动与卷帘快门失真**：快速运动区域的重建会继承输入视频的卷帘快门（rolling shutter）失真，且快速运动对多视图一致性保存构成挑战（见 Section E.2）。不确定性估计本身无法纠正输入信号的几何失真。

- **高度可变形对象**：当先验信息严重不准确或观测极度稀疏时，即使在不确定性加权下，高度可变形区域的重建仍然困难（见 Section E.3）。关键节点选择策略在这些区域可能失效，因为缺乏可靠的锚点高斯。

- **纯旋转相机运动的失效风险**：在纯旋转相机运动下，深度不确定性缩放因子 $r_x, r_y, r_z$ 可能失效，因为2D不确定性向3D传播时缺乏深度方向的约束信号。论文未提供该场景下的自适应调整机制。

### 开放问题

1. **卷帘快门与多视图一致性的联合处理**：如何将不确定性建模与卷帘快门校正、多视图一致性约束统一到一个框架中，是处理消费级视频输入的关键问题。

2. **自适应深度不确定性缩放**：在纯旋转或退化相机运动下，如何自适应调整深度方向的不确定性缩放因子，避免不确定性估计的退化？

3. **极端可变形区域的先验增强**：当先验轨迹极度稀疏或不可靠时，是否可以通过引入语义先验或物理约束来补充不确定性引导的优化？

4. **不确定性估计的理论紧致性**：闭式方差估计基于局部最小值假设，该假设在遮挡边界和深度不连续区域的紧致性如何？是否存在更精确且计算可行的替代方案？

## 原文 PDF

![[paperPDFs/ICLR_2026/Uncertainty_Matters_in_Dynamic_Gaussian_Splatting_for_Monocular_4D_Reconstructio_f0906ec8357c.pdf]]
