---
title: "FISHuman: Fine-grained Single-image 3D Human Reconstruction via Multi-view 4D Remeshing"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FISHuman_Fine_grained_Single_image_3D_Human_Reconstruction_via_Multi_view_4D_Remeshing.pdf
project_link: null
code_link: "https://github.com/jpcy/xatlas"
aliases:
- FISHuman
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 提出3D感知的双流视频扩散Transformer，生成跨模态对齐的密集多视角RGB和法线序列；并引入4D重网格化模块，将像素级漂移转换为视角依赖的顶点变形，解耦全局规范网格与动态细节的学习，进而建立统一的UV表示融合外观信息。
primary_logic: 通过两项核心设计弥合单图像与显式3D表示的鸿沟：(1) 向视频扩散模型中注入3D感知微调和跨模态注意力，生成空间一致且强耦合的多模态多视角引导；(2) 将不一致的多视图监督转化为动态顶点变形，在保持拓扑一致性的前提下优化共享规范几何，并利用该拓扑统一纹理，从多个视角整合有效外观。
claims:
- 在2K2K和Sizer数据集上，FISHuman在所有几何和外观指标上均显著优于PSHuman、Human3Diffusion等前沿方法，例如在2K2K上CD由1.133降至0.817，PSNR由23.03提升至24.49。
- 消融实验证实撤除跨模态对齐或4D重网格化均导致PSNR/SSIM/LPIPS明显下降，验证了两模块对重建质量的关键作用。
- 在包含人物与物体交互、罕见背视等挑战场景下，FISHuman借助3D感知视频模型生成连贯新视角，几何与纹理均优于PSHuman，后者产生明显畸变。
- 2K2K 上 CD(cm)↓ = 0.817
---

# FISHuman: Fine-grained Single-image 3D Human Reconstruction via Multi-view 4D Remeshing

> [!tip] 核心洞察
> 通过两项核心设计弥合单图像与显式3D表示的鸿沟：(1) 向视频扩散模型中注入3D感知微调和跨模态注意力，生成空间一致且强耦合的多模态多视角引导；(2) 将不一致的多视图监督转化为动态顶点变形，在保持拓扑一致性的前提下优化共享规范几何，并利用该拓扑统一纹理，从多个视角整合有效外观。

| 字段 | 内容 |
|------|------|
| 中文题名 | FISHuman：基于多视角4D重网格化的细粒度单图像三维人体重建 |
| 英文题名 | FISHuman: Fine-grained Single-image 3D Human Reconstruction via Multi-view 4D Remeshing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Liu_FISHuman_Fine-grained_Single-image_3D_Human_Reconstruction_via_Multi-view_4D_Remeshing_CVPR_2026_paper.html) · [Code](https://github.com/jpcy/xatlas) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FISHuman |
| Dataset | 2K2K, Sizer |

> [!tip] 效果简介
> - 2K2K 上，CD(cm)↓ 0.817 vs 1.133 (PSHuman) (-0.316)；P2S(cm)↓ 0.778 vs 1.062 (PSHuman) (-0.284)；NC↑ 0.858 vs 0.828 (PSHuman) (+0.030)。
> - Sizer 上，CD(cm)↓ 1.243 vs 1.570 (PSHuman) (-0.327)；PSNR↑ 20.38 vs 19.61 (PSHuman) (+0.77)。

## 概要

从单张自然图像重建细粒度三维人体，是数字人建模的核心难题。现有方法多借助2D多视图扩散模型生成辅助视角作为重建先验，但这些生成视图缺乏3D一致性，在自遮挡区域和复杂姿态下尤为严重。将不一致的多视图直接用于静态3D重建，会引入几何扭曲与纹理模糊，且泛化能力受限。

FISHuman针对上述瓶颈，提出两条核心思路弥合单图像与显式3D表示之间的鸿沟。第一，设计**3D感知的双流视频扩散Transformer**，通过注入3D感知微调和跨模态注意力，生成空间一致且强耦合的多模态多视角RGB与法线序列。第二，引入**4D重网格化模块**，将像素级不一致转化为视角依赖的顶点变形，解耦全局规范网格与动态细节的学习，并建立**统一UV表示**，在共享拓扑上整合所有视角的有效外观。

在2K2K和Sizer数据集上，FISHuman在所有几何与外观指标上均显著优于PSHuman、Human3Diffusion等前沿方法。例如，在2K2K上CD由1.133降至0.817，PSNR由23.03提升至24.49。消融实验证实，跨模态对齐和4D重网格化两个模块对重建质量具有关键作用。在人物与物体交互、罕见背视等挑战场景下，FISHuman借助3D感知视频模型生成连贯新视角，几何与纹理均优于PSHuman，后者则产生明显畸变。

### 问题背景：单图像三维人体重建的挑战

从单张自然图像中重建细粒度、可动画化的三维人体化身，是计算机视觉与图形学领域的长期目标。该任务要求从极度稀疏的输入中同时恢复高保真几何与逼真外观，其核心困难在于：单张图像仅捕获某一视角下的二维投影，而人体表面高度非刚性、自遮挡严重、且服装与配饰形态千变万化，使得从二维到三维的逆映射本质上高度病态。

近年来，基于扩散模型的生成式方法为这一难题带来了突破性进展。通过利用大规模图像/视频生成先验，研究者能够从单张参考图中“想象”出不可见区域的外观，从而为后续三维重建提供密集的多视角引导信号。然而，这一范式仍面临一个关键瓶颈。

### 现有方法缺口：多视图生成缺乏三维一致性

当前主流方法通常借助二维多视图扩散模型生成辅助视图，并将其作为三维重建的先验。典型代表包括 **PSHuman**（Li et al., arXiv 2024）基于跨尺度多视图扩散与显式重网格化的重建框架，以及 **Human3Diffusion**（Xue et al., NeurIPS 2024）等显式三维一致扩散模型。

但这些方法存在一个共同缺陷：**生成的辅助视图之间缺乏三维空间一致性**。具体表现为：

1. **自遮挡区域的歧义性**：当人体处于复杂姿态时，被遮挡的身体部位（如交叉的手臂、背向的躯干）在不同生成视图中可能呈现相互矛盾的几何与纹理信息。
2. **跨视角几何漂移**：独立生成的各帧之间缺少显式的三维几何约束，导致同一表面区域在不同视角下发生位置偏移或形态扭曲。
3. **纹理融合退化**：将此类不一致的多视图直接用于静态三维重建（如可微渲染管线）时，逐视角的监督信号相互冲突，最终导致几何扭曲、表面裂纹和纹理模糊。

这一瓶颈在人物与物体交互、罕见背视姿态等挑战场景下尤为突出——此时输入图像提供的信息极度有限，模型对生成先验的依赖更强，不一致性带来的危害也更大。

### 本文动机：弥合单图像与显式三维表示的鸿沟

针对上述问题，FISHuman 的核心动机在于**通过两项关键设计弥合单图像输入与显式三维表示之间的鸿沟**：

1. **生成端**：不再依赖独立的多视图生成，而是构建一个**三维感知的双流视频扩散Transformer**，在视频生成过程中注入跨模态注意力机制，强制RGB与法线序列在全局布局和局部细节上对齐，从而产出空间一致且强耦合的多模态多视角引导信号。

2. **重建端**：不将多视图监督直接用于静态重建，而是提出**4D重网格化模块**，将像素级的不一致转化为视角依赖的顶点变形——在保持拓扑一致性的前提下联合优化全局规范网格与动态变形场，并利用该拓扑建立统一的UV表示，从多个视角整合有效外观信息，避免纹理平均导致的模糊。

通过这一“生成-重建”协同设计，FISHuman 旨在突破现有方法在几何精度、纹理保真度和泛化能力上的上限，实现从单张自然图像到可直接动画、可编辑的高质量三维化身。

## 核心方法与创新机理

FISHuman 的核心创新在于针对单图像三维人体重建中“多视图先验不一致”这一瓶颈，构建了一套从生成到重建的完整解耦方案。其关键思路可归纳为两个递进层面。

**瓶颈诊断：多视图扩散先验的 3D 不一致性。** 现有方法（如 **PSHuman** (Li et al., arXiv 2024)、**Human3Diffusion** (Xue et al., NeurIPS 2024)）普遍利用 2D 多视图扩散模型生成辅助视角作为重建先验，但这些生成视图缺乏 3D 一致性，尤其在自遮挡区域和复杂姿态下。将此类不一致的多视图直接用于静态 3D 重建，会导致几何扭曲和纹理模糊，且泛化能力受限。

**创新一：3D 感知双流视频扩散 Transformer。** FISHuman 将多视图生成从“单流、模态割裂”改造为“双流、跨模态对齐”架构。具体而言，它采用双流 DiT（Diffusion Transformer），在每 4 个共享块中替换 1 个为跨模态注意力模块，强制 RGB 与法线在全局布局和细节上对齐（Figure 3）。同时，向视频扩散模型注入 3D 感知微调，使生成的多视角序列具备空间一致性，有效抑制头发、衣物等区域的浮动动态。训练策略上采用两阶段渐进方案：先建立单模态 3D 一致性，再引入跨模态对齐，并以 30% 概率随机屏蔽跨模态注意力以防止质量退化。

**创新二：4D 重网格化与统一 UV 表示。** 传统方法将多视图法线直接用于静态可微渲染重建，相当于对不一致监督信号做“硬平均”，容易产生表面裂纹和拓扑错误。FISHuman 提出 4D 重网格化模块，将规范网格优化与视角相关的动态变形场解耦：全局共享的规范几何通过连续显式重网格化更新，而各视角的像素级不一致被转化为顶点变形偏移（$\delta x_i = \Psi_d(\gamma(x_c), \gamma(i))$），由 MLP 预测。这使模型能够跟踪同一顶点在不同视角下的位置变化，将“监督冲突”转化为“几何弹性”，从而在保持拓扑一致性的前提下重建精确、无裂纹的几何。在此基础上，统一 UV 表示利用变形网格间的拓扑一致性，在规范 UV 空间整合所有视角的外观信息，辅以总变分平滑，消除逐视角纹理平均带来的模糊。

**创新三：跨模态对齐与几何重建的协同。** 这两个模块并非孤立运作，而是形成正向反馈：跨模态对齐的 RGB-法线序列为 4D 重网格化提供了强耦合、结构一致的多模态监督；4D 重网格化产出的干净几何又为统一 UV 纹理学习提供了可靠的投影基础。消融实验（Table 2）证实，移除跨模态对齐（w/o CMA）导致 PSNR 从 24.49 降至 23.14，移除 4D 重网格化（w/o 4DR）则降至 23.87，且在夸张姿态下出现表面裂纹和面部细节模糊（Figure 8），验证了两模块对重建质量的关键作用。

FISHuman 的整体流程以单张自然场景人体图像为输入，输出具有精细几何与逼真纹理的可驱动三维化身。框架由两大核心组件串联构成：**3D感知双流视频扩散Transformer** 与 **动态三维人体雕刻方法**（含4D重网格化模块和统一UV表示学习），如图2所示。

### 输入与多模态先验生成

给定一张参考图像，系统首先利用现成的法线估计器与姿态预测器提取参考法线图和相机姿态序列，构成条件信号。随后，**3D感知双流视频扩散Transformer** 以该条件信号为引导，联合生成跨模态对齐的多视角RGB序列与法线序列。该生成器通过跨模态注意力机制强制RGB与法线在全局布局和局部细节上保持一致，为下游重建提供密集且空间连贯的多视角先验。

### 动态三维人体雕刻

生成的多视角序列直接进入几何重建阶段。与现有方法将多视图监督直接用于静态三维重建不同，FISHuman 提出 **4D重网格化模块**，将规范网格优化与视角相关的动态变形场显式解耦：一个全局共享的规范网格通过可微渲染在法线监督下持续更新拓扑，同时一个MLP预测每个顶点在不同视角下的偏移量，将像素级不一致转化为视角依赖的几何变形。这一设计使得模型能够在保持拓扑一致性的前提下，从存在冲突的多视图法线中提取精确、无裂纹的几何。

### 统一UV纹理学习

几何优化完成后，系统在所有视角共享拓扑的变形网格上优化单一纹理图。由于变形网格间保持顶点对应关系，各视角的有效外观信息可被统一投影到规范UV空间，并通过总变分平滑损失抑制纹理噪声，最终聚合为高保真的外观表示。

### 数据流总结

整个管线的数据流可概括为：**单张RGB图像 → 条件信号提取 → 双流视频扩散生成多视角RGB+法线 → 4D重网格化联合优化规范几何与视角变形 → 统一UV纹理优化 → 带纹理的可驱动三维化身**。两阶段设计将“生成空间一致的多视角引导”与“从不一致监督中恢复一致几何和纹理”解耦，使得模型在复杂姿态和自遮挡场景下仍能保持鲁棒的重建质量。

![[assets/figures/papers/paper_list_l1023_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_FISHuman_Fine_grai/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. Given a single-view human image, FISHuman reconstructs the corresponding fine-grained 3D avatar by generating cross-modally aligned RGB and normal frames using the proposed 3D-aware dual-stream video diffusion transformer. With the generated sequences, we perform 4D Remeshing that explicitly decouples the optimization of the 3D canonical mesh and view-dependent per-vertex deformation field, effectively mitigating 3D inconsistencies of the multi-view guidance. A unified UV representation is updated on the deformed meshes to integrate valid appearance across all perspectives*

FISHuman通过三个紧密协作的模块弥合单图像与显式三维表示之间的鸿沟：**3D感知双流视频扩散Transformer**生成空间一致的多模态多视角先验；**4D重网格化模块**将像素级不一致转化为视角依赖的顶点变形；**统一UV表示学习**在共享拓扑上聚合所有视角的有效外观。

### 3D感知双流视频扩散Transformer

该模块以单张参考图像为输入，同时生成跨模态对齐的密集多视角RGB和法线序列。其核心设计包含两个关键创新：

**双流DiT架构与跨模态注意力**：模型采用双流Diffusion Transformer，分别处理RGB和法线两个模态。在每4个共享Transformer块中替换1个为跨模态DiT块（Cross-modal DiT block），通过跨模态注意力机制强制RGB与法线在全局布局和局部细节上实现对齐，如图3所示。模型学习的目标分布为：

$$p ( \mathcal { F } _ { 1 : T } ^ { r g b } , \mathcal { F } _ { 1 : T } ^ { n o r m } | \mathbf { c } _ { r e f } ^ { r g b } , \mathbf { c } _ { r e f } ^ { n o r m } , \mathbf { c } ^ { p o s e } )$$

其中$\mathcal{F}_{1:T}^{rgb}$和$\mathcal{F}_{1:T}^{norm}$分别为生成的RGB和法线序列，条件包括参考图像的RGB $\mathbf{c}_{ref}^{rgb}$、法线$\mathbf{c}_{ref}^{norm}$及目标姿态$\mathbf{c}^{pose}$。

**两阶段渐进训练策略**：第一阶段先建立单模态的3D一致性，第二阶段再引入跨模态对齐。训练时以30%概率随机屏蔽跨模态注意力，防止直接端到端训练导致的质量退化。消融实验表明，该策略相比直接端到端训练能生成更逼真的新视角和高频表面细节，避免未见过区域出现噪声外观和法线图模糊（Figure 7）。

### 4D重网格化模块

该模块是FISHuman处理多视图不一致性的核心机制，将规范网格优化与视角相关的动态变形场解耦。

**动态变形场建模**：给定规范网格顶点坐标$x_c$，一个MLP网络$\Psi_d$根据规范顶点位置和视角索引$i$预测当前视图下的顶点偏移：

$$\delta x _ { i } = \Psi _ { d } ( \gamma ( x _ { c } ) , \gamma ( i ) )$$

其中$\gamma(\cdot)$为位置编码。变形后的顶点坐标为：

$$x _ { d } ^ { i } = x _ { c } + \delta x _ { i }$$

这一设计将多视图法线帧之间的像素级不一致转化为视角依赖的顶点变形，而非直接平均监督信号，从根本上避免了静态重建中的几何扭曲。

**几何优化目标**：重建损失结合渲染法线与目标法线的L1损失，以及渲染剪影与前景掩码的L1损失：

$$L _ { r e c } = | | \hat { \mathcal { N } } _ { i } - \mathcal { F } _ { i } ^ { n o r m } | | _ { 1 } + | | \hat { S } _ { i } - \mathcal { S } _ { i } | | _ { 1 }$$

为促进表面均匀性，对规范网格和变形网格施加拉普拉斯平滑损失：

$$L _ { l a p } = \frac { 1 } { n } \sum _ { i = 1 } ^ { n } | | \sigma _ { i } | | _ { 2 } , \quad \sigma _ { i } = x _ { i } - \frac { 1 } { | N ( i ) | } \sum _ { j \in N ( i ) } x _ { j }$$

为鼓励近刚性变形，引入ARAP（As-Rigid-As-Possible）约束，在两个随机视角下保持对应顶点间的边长度：

$$L _ { a r a p } = \sum _ { i = 1 } ^ { n } \sum _ { j \in N ( i ) } \left| | | x _ { i } - x _ { j } | | _ { 2 } - | | x _ { i } ^ { \prime } - x _ { j } ^ { \prime } | | _ { 2 } \right|$$

几何总损失为三项加权组合：

$$L _ { g e o } = L _ { r e c } + \lambda _ { l a p } L _ { l a p } + \lambda _ { a r a p } L _ { a r a p }$$

训练中权重设置为$\{\lambda_{lap}, \lambda_{arap}\} = \{0.4, 0.03\}$。规范网格在优化过程中通过连续显式重网格化（基于xatlas ）更新拓扑，确保网格质量。

### 统一UV表示学习

利用变形网格在所有视角下共享拓扑的特性，在规范UV空间优化单一纹理图，有效聚合各视角的有效外观特征。

**纹理优化目标**：基于变形网格渲染彩色图像，与目标RGB帧计算加权L2损失（仅计算前景区域）：

$$L _ { r g b } = w _ { i } | | \hat { C } _ { i } \cdot S _ { i } - \mathcal { F } _ { i } ^ { r g b } \cdot S _ { i } | | _ { 2 }$$

其中$\hat{C}_i$为渲染彩色图像，$S_i$为前景剪影掩码，$w_i$为视角权重。纹理优化总损失加入全变分平滑项：

$$L _ { t e x } = L _ { r g b } + \lambda _ { t v } L _ { t v }$$

其中$\lambda_{tv}$默认设置为0.5。该策略避免了逐视角烘焙纹理后平均导致的模糊问题，从多个视角整合有效外观信息，生成高保真纹理。

### 模块间协同机制

三个模块形成闭环协作：双流视频扩散模型生成空间一致的多模态多视角引导（RGB+法线序列）；4D重网格化利用法线序列优化规范几何，同时将视角不一致转化为顶点变形；统一UV表示在变形网格上整合RGB序列的外观信息，反馈提升纹理质量。消融实验证实，移除跨模态对齐（w/o CMA）导致PSNR从24.49降至23.14，移除4D重网格化（w/o 4DR）使PSNR降至23.87且在夸张姿态下出现表面裂纹（Table 2, Figure 8），验证了各模块对重建质量的关键作用。

![[assets/figures/papers/paper_list_l1023_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_FISHuman_Fine_grai/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of model architecture. (a) Dual-stream diffusion transformer. (b) Cross-modal DiT block*

## 实验与关键发现

### 主要结果：任意姿态重建

FISHuman 在 2K2K 和 Sizer 两个数据集上对所有几何与外观指标均取得最优，且优势幅度显著。Table 1 报告了与前沿方法的全面对比，其中最强基线为 **PSHuman**（Li et al., arXiv 2024）。在 2K2K 数据集上，FISHuman 的倒角距离（CD）由 PSHuman 的 1.133 cm 降至 0.817 cm（↓0.316），点面距离（P2S）由 1.062 cm 降至 0.778 cm（↓0.284），法线一致性（NC）由 0.828 提升至 0.858（↑0.030）；外观方面，PSNR 由 23.03 提升至 24.49（↑1.46），SSIM 由 0.906 提升至 0.917，LPIPS 由 0.105 降至 0.086。在 Sizer 数据集上，CD 由 1.570 cm 降至 1.243 cm（↓0.327），PSNR 由 19.61 提升至 20.38（↑0.77）。这些结果表明，3D 感知双流视频扩散 Transformer 生成的跨模态对齐多视图先验，结合 4D 重网格化对不一致监督的转化能力，在几何精度和纹理保真度两个维度上均形成了实质性的性能增益。

![[assets/figures/papers/paper_list_l1023_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_FISHuman_Fine_grai/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on arbitrary-pose reconstruction from single images. We compare our method with SOTA methods on the 2K2K and Sizer datasets. Our method surpasses all the baselines on both geometry and appearance metrics. Note that the training sets of Human3Diffusion include 2K2K data. ↑ and ↓ denote if higher or lower is better, respectively*

值得注意的是，**Human3Diffusion**（Xue et al., NeurIPS 2024）的训练集包含 2K2K 数据，可能使其在该数据集上的指标偏高，但 FISHuman 仍全面超越该基线，说明方法增益并非来自数据泄露。

### 消融实验

Table 2 的消融实验系统验证了跨模态对齐（CMA）与 4D 重网格化（4DR）两个核心模块的贡献：

![[assets/figures/papers/paper_list_l1023_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_FISHuman_Fine_grai/figures/007_Table_2.jpg]]
*Table 2: Ablation study on cross-modal alignment and 4D remeshing. Results verify the effectiveness of the proposed modules*

- **移除跨模态对齐（w/o CMA）**：PSNR 从完整模型的 24.49 降至 23.14，降幅达 1.35 dB。这表明仅靠独立生成 RGB 与法线序列无法保证两者在结构与细节层面的空间一致性，跨模态注意力模块对高质量重建不可或缺。
- **移除 4D 重网格化（w/o 4DR）**：退化为静态重建方案，PSNR 降至 23.87。在夸张姿态下，静态重建无法处理多视图法线间的冲突信号，导致表面出现裂纹、复杂拓扑区域重建失败以及面部细节模糊（见 Figure 8）。
- **两阶段渐进训练 vs. 直接端到端训练**：Figure 7 的视觉对比显示，渐进训练策略能更好地生成逼真新视角和高频表面细节，而直接端到端训练在未见区域产生噪声外观和模糊法线图。训练时以 30% 概率随机屏蔽跨模态注意力是防止质量退化的关键技巧。
- **3D 感知微调的必要性**：Figure 6 表明，在基础视频模型上进行 3D 感知微调可有效抑制头发、衣物等区域的浮动伪影，建立跨帧空间一致性；未微调的模型在连续帧之间产生剧烈漂移，无法为后续重建提供可靠先验。

![[assets/figures/papers/paper_list_l1023_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_FISHuman_Fine_grai/figures/009_Figure_7.jpg]]
*Figure 7: Ablation on the two-stage progressive training scheme*

### 挑战场景分析

Figure 5 展示了人物-物体交互和罕见背视等挑战性场景下的对比。PSHuman 在这些场景中产生明显的几何畸变和纹理撕裂，而 FISHuman 借助 3D 感知视频模型生成的连贯新视角，保持了合理的几何结构和外观一致性。这归因于双流 DiT 在全局布局上的跨模态对齐能力，以及 4D 重网格化将像素级不一致转化为顶点级变形的机制——即使在自遮挡严重的背视角度，变形场仍能追踪到合理的顶点偏移。

![[assets/figures/papers/paper_list_l1023_https_openaccess_thecvf_com_content_CVPR2026_html_Liu_FISHuman_Fine_grai/figures/006_Figure_5.jpg]]
*Figure 5: Comparison with PSHuman on challenging cases including human-object interactions and rare back-view poses*

### 局限性

尽管 FISHuman 在主流基准上表现优异，仍存在以下局限需注意：

1. **生成器的 2D 监督瓶颈**：视频扩散 Transformer 仅依赖 2D 像素级损失，缺少显式 3D 约束。在极端复杂场景（如严重遮挡、罕见服饰）下可能产生空间不对齐的多视图输出。4D 重网格化可部分缓解该问题，但无法从根本上消除生成阶段的 3D 不一致。
2. **推理效率**：完整流程耗时约 7 分钟（视频模型约 5 分钟 + 4D 重网格化约 2 分钟），远未达到实时应用要求。
3. **数据覆盖范围**：训练数据仅包含 1559 个高质量扫描，在极端人物风格或稀有着装上的泛化能力有待进一步验证。

## 定位与知识库关联

### 1. 领域位置与核心差异

FISHuman 处于单图像三维人体重建的交叉地带，其上游依赖两条技术脉络：

**多视图扩散先验。** 以 **PSHuman** (Li et al., arXiv 2024)、**Human3Diffusion** (Xue et al., NeurIPS 2024) 为代表的方法利用2D多视图扩散模型生成辅助视角作为重建引导。这类方法的根本瓶颈在于：生成的多视图缺乏3D一致性，尤其在自遮挡区域和复杂姿态下，不同视角的几何/纹理线索相互矛盾。直接将此类不一致的监督信号馈入静态3D重建（如可微渲染）会导致几何扭曲和纹理模糊，且泛化能力受限。

**可微渲染与隐式重建。** **SIFU** (Zhang et al., CVPR 2024) 基于隐式函数进行多视角纹理精炼，**SiTH** 采用稀疏多视图扩散重建。这些方法或依赖隐式表示难以显式控制拓扑，或受限于稀疏视角的信息量。

FISHuman 的关键突破在于**改变了对多视图不一致的处理方式**：不再试图让生成器输出完美一致的视图，而是通过4D重网格化将像素级漂移转化为视角依赖的顶点变形，在共享规范几何框架下吸收各视角的有效信息。这一思路与 **PSHuman** 的显式重网格化有表面相似性，但本质差异在于 FISHuman 引入了动态变形场解耦，而 PSHuman 仍属于静态重建范式。

### 2. 方法谱系中的槽位变化

| 技术槽位 | 基线方案 | FISHuman 方案 | 证据锚点 |
|---------|---------|--------------|---------|
| 多视角生成架构 | 单流扩散模型或未对齐的多模态生成 | 双流 DiT + 跨模态注意力（每4个共享块替换1个），强制 RGB 与法线在全局布局和细节上对齐 | Section 3.1, Fig. 3 |
| 3D重建方法 | 静态重建，直接平均各帧监督信号 | 4D重网格化：联合优化全局规范网格与视角相关动态变形场 | Section 3.2.1, Fig. 2 |
| 纹理融合策略 | 逐视角烘焙并平均，易导致模糊 | 统一UV表示优化：利用变形网格间的拓扑一致性在规范UV空间整合外观 | Section 3.2.2 |
| 训练策略 | 直接端到端训练多模态对齐 | 两阶段渐进训练：先建立单模态3D一致性，再引入跨模态对齐（30%概率随机屏蔽跨模态注意力） | Section 3.1 |

### 3. 与关键基线的关系

**vs. PSHuman (Li et al., arXiv 2024)。** 两者均采用显式网格重建，但 PSHuman 的跨尺度多视图扩散缺乏跨模态对齐机制，且其重网格化为静态过程。定量对比（Table 1）显示，FISHuman 在 2K2K 数据集上将 CD 从 1.133 降至 0.817，P2S 从 1.062 降至 0.778；在 Sizer 数据集上 CD 从 1.570 降至 1.243。在人物-物体交互和罕见背视等挑战场景下（Figure 5），PSHuman 产生明显畸变，FISHuman 则借助 3D 感知视频模型生成连贯新视角。

**vs. Human3Diffusion (Xue et al., NeurIPS 2024)。** 该方法引入显式3D一致扩散，但其训练集包含 2K2K 数据（Table 1 注释），可能使其在 2K2K 上的指标偏高。FISHuman 在未使用该数据集训练的情况下仍全面超越，表明 4D 重网格化的几何处理能力具有更强的泛化性。

**vs. 通用资产生成方法。** **Hunyuan3D 2.0** (Zhao et al., arXiv 2025) 面向通用高分辨率3D资产生成，**StdGen** 专注于标准姿态角色生成。FISHuman 的细粒度人体重建在任意姿态下保持拓扑一致性和纹理真实感，与这些通用方法形成互补而非直接竞争。

### 4. 适用边界与局限

**推理效率边界。** 完整流程耗时约7分钟（视频扩散模型5分钟 + 4D重网格化2分钟），不适合实时或交互式应用场景。这是当前视频扩散模型推理成本的固有限制。

**2D监督的固有局限。** 视频扩散生成器仅依赖2D像素级监督，缺少显式3D约束。在极端复杂场景下可能产生空间不对齐，尽管4D重网格化模块可部分缓解这一问题，但无法从根本上消除生成阶段的误差传播。

**训练数据覆盖范围。** 模型在1559个高质量扫描上训练，在极端人物风格（如高度风格化角色）或稀有着装（如特殊民族服饰）上的泛化能力有待验证。此点需手动验证：论文未提供在非真实感角色或极端服饰上的系统评估。

**多模态对齐的鲁棒性。** 跨模态注意力模块在训练中以30%概率随机屏蔽以防止质量退化，这一策略的有效性依赖于训练数据的多样性。当输入图像的RGB与法线域存在严重域偏移时，对齐质量可能下降——该结论来自消融实验的间接证据，论文未提供域外测试的定量数据。

### 5. 开放问题与后续方向

1. **显式3D约束的引入。** 当前框架的生成阶段缺乏3D几何监督，未来可探索将4D重网格化的几何一致性信号反向传播至扩散模型，形成闭环优化。

2. **效率优化。** 视频扩散模型的推理时间是主要瓶颈，模型蒸馏、步数压缩或基于一致性模型的方法可能显著缩短生成时间。

3. **动态场景扩展。** 4D重网格化模块天然支持视角依赖的变形建模，理论上可扩展至时序动态人体重建（如视频输入），但论文未探索这一方向。

4. **跨域泛化验证。** 在非真实感渲染角色、极端体型（如儿童、特殊身材比例）上的性能缺乏系统评估，这是实际部署前需要填补的空白。

## 原文 PDF

![[paperPDFs/CVPR_2026/FISHuman_Fine_grained_Single_image_3D_Human_Reconstruction_via_Multi_view_4D_Remeshing.pdf]]
