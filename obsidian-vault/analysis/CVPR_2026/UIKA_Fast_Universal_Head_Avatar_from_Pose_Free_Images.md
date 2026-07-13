---
title: "UIKA: Fast Universal Head Avatar from Pose-Free Images"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UIKA_Fast_Universal_Head_Avatar_from_Pose_Free_Images.pdf
project_link: "https://zijian-wu.github.io/uika-page/"
code_link: null
aliases:
- UIKA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过预测像素级面部UV坐标并利用UV空间作为统一表示，引入UV注意力机制实现结构化的跨视图信息交互和融合。
primary_logic: 将屏幕空间特征与UV空间特征通过双分支注意力结合，利用UV空间的对应独立性消除姿态歧义，并通过自适应融合动态平衡全局预测与局部观测，实现高质量、可驱动的3D头部化身重建。
claims:
- Monocular自重建中，所提方法在所有指标上均优于SOTA基线（如PSNR 21.69 vs 21.03，LPIPS 0.105 vs 0.134）。
- Multi-view自重建中，所提方法显著优于基线，PSNR达到22.50，远超DiffusionRig的16.97和GPAvatar的17.11。
- 移除UV注意力分支导致PSNR从22.61降至22.21，并出现明显的细节丢失。
- 移除自适应颜色融合和UV聚合图导致颜色不一致和细节退化。
---

# UIKA: Fast Universal Head Avatar from Pose-Free Images

> [!tip] 核心洞察
> 将屏幕空间特征与UV空间特征通过双分支注意力结合，利用UV空间的对应独立性消除姿态歧义，并通过自适应融合动态平衡全局预测与局部观测，实现高质量、可驱动的3D头部化身重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | UIKA：基于无姿态图像的快速通用头部化身 |
| 英文题名 | UIKA: Fast Universal Head Avatar from Pose-Free Images |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.07603) · [Project](https://zijian-wu.github.io/uika-page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | UIKA |
| Dataset | VFHQ + NeRSemble-v2, NeRSemble-v2 |

> [!tip] 效果简介
> - VFHQ + NeRSemble-v2 (Monocular) 上，PSNR↑ 21.69 vs 21.03 (Portrait4D-v2) (+0.66)；LPIPS↓ 0.105 vs 0.134 (Portrait4D-v2) (-0.029)。
> - NeRSemble-v2 (Multi-view) 上，PSNR↑ 22.50 vs 17.11 (GPAvatar) (+5.39)；LPIPS↓ 0.120 vs 0.313 (GPAvatar) (-0.193)。
> - NeRSemble-v2 (Monocular) 上，CSIM↑ (Cross) 0.649 vs 0.678 (GAGAvatar) (-0.029)。

## 概要

UIKA 是一个前馈式（feed-forward）3D 头部化身重建框架，旨在从**任意数量的无姿态（pose-free）输入图像**中重建高保真、可实时驱动的3D高斯头部化身，无需相机参数或表情标注。该工作解决了现有方法在多视图信息聚合中对显式跨帧对应的依赖缺失这一核心瓶颈。

**核心思路**：UIKA 通过面部对应估计器预测像素级UV坐标，将屏幕空间颜色重投影至共享UV空间，从而建立跨视图的显式对应关系。在此基础上，方法引入**UV-屏幕双注意力机制**，在UV空间中进行结构化的全局特征交互，同时保留屏幕空间的局部细节，最终通过自适应颜色融合生成高质量化身。

**主要结果**：
- **单目自重建**：在VFHQ与NeRSemble-v2数据集上，UIKA的PSNR达到21.69，LPIPS降至0.105，均优于现有最优方法（如Portrait4D-v2的21.03/0.134）。
- **多视图自重建**：PSNR达到22.50，大幅领先DiffusionRig（16.97）和GPAvatar（17.11），LPIPS优势超过0.19。
- **消融实验**：移除UV注意力分支使PSNR下降0.40，移除颜色聚合模块下降0.22，验证了各组件的关键作用。
- **用户研究**：在渲染质量、运动一致性和身份保持三个维度上，UIKA评分（4.37）显著超过基线最高分（3.54）。

**方法定位**：如表1所示，UIKA兼具前馈推理、无姿态输入和实时动画（≥30 FPS）三大特性，填补了现有头部化身方法在灵活性与效率之间的空白。与GAGAvatar、LAM等单目前馈方法相比，UIKA支持任意数量输入视图；与GPAvatar等多视图方法相比，UIKA无需相机标注；与InvertAvatar等优化式方法相比，UIKA无需测试时优化。

**局限与展望**：受FLAME模型表达能力限制，精细面部动态（如微表情、舌头动作）仍无法捕捉；训练数据存在人口统计偏差；计算开销随视图数增长而性能提升趋于饱和。未来工作可探索更丰富的面部表示、偏差缓解策略以及高效的视图选择机制。

### 问题背景

创建逼真、可驱动的3D头部化身是计算机视觉与图形学领域的核心挑战，其应用涵盖虚拟现实、远程呈现、影视制作和数字人交互等场景。近年来，基于3D Gaussian Splatting（3DGS）的方法因其高效的渲染能力和灵活的场景表示，逐渐成为该任务的主流范式。然而，现有方法在输入灵活性与重建质量之间仍存在显著矛盾。

一方面，**优化式方法**（如InvertAvatar）能够从少量图像中重建高保真头部化身，但需要针对每个身份进行耗时的测试时优化（per-identity optimization），难以满足实时应用需求。另一方面，**前馈式方法**（如GAGAvatar、LAM、Portrait4D-v2）通过训练通用模型实现单次前向推理即可完成重建，大幅提升了效率，但它们通常依赖精确的相机姿态和表情参数作为输入条件。在实际场景中，获取这些标注需要复杂的多视图标定流程或额外的参数估计网络，这引入了误差累积风险，并限制了方法的易用性。

更关键的是，当输入图像数量不固定且缺乏显式标注时，**多视图信息聚合**成为一个根本性瓶颈。在无姿态标注的条件下，不同视角的图像之间缺乏可靠的对应关系，导致模型难以有效融合互补的观测信息。这一问题在极端表情和极端视角下尤为突出——此时面部自遮挡严重，单视图信息高度不足，而跨视图信息的错误匹配会直接导致重建细节丢失或几何畸变。

### 现有方法缺口

Table 1 系统对比了UIKA与现有代表性方法在三个关键维度上的能力：是否前馈（FF）、是否无姿态输入（PF）、是否支持实时动画（RTA）。从该对比中可以清晰识别出现有方法的功能性缺口：

- **GAGAvatar**、**LAM**等单目前馈方法虽然实现快速重建，但需要相机和表情标注，且仅支持单视图输入，无法利用多视图互补信息。
- **Portrait4D-v2**作为条件生成式方法，同样依赖标注输入，且生成结果的身份保持能力有限。
- **DiffusionRig**和**GPAvatar**支持多视图输入，但前者基于扩散模型，推理效率低且不支持实时动画；后者虽为前馈架构，但仍需姿态标注，且在无标注场景下性能急剧下降（多视图PSNR仅17.11，见Table 3）。
- **InvertAvatar**等优化式方法虽然支持无姿态输入，但需要逐身份优化，不具备前馈能力。

综合来看，**同时满足“前馈推理”“无姿态输入”“多视图灵活输入”和“实时动画”四个条件的方法在UIKA之前尚属空白**。这一缺口的核心技术障碍在于：缺乏一种既能在无标注条件下建立可靠跨视图对应，又能高效融合多视图信息，并最终输出可驱动3D表示的通用机制。

### 本文动机

针对上述缺口，UIKA的核心动机是：**能否利用面部固有的结构化先验——UV空间——作为统一的对应桥梁，从而在无姿态标注的条件下实现鲁棒的多视图信息聚合？**

这一动机基于一个关键洞察：人脸具有高度结构化的几何拓扑，其表面点与UV坐标之间存在天然的双射关系。如果能为每个输入图像的像素预测其对应的面部UV坐标，那么来自不同视角、不同表情的像素颜色就可以被重投影到一个共享的UV空间中。在这个空间里，对应关系不再依赖于相机姿态或表情参数，而是由UV坐标本身隐式确定——这从根本上消除了姿态歧义。

基于这一动机，UIKA设计了一条完整的UV引导建模流水线：首先通过面部对应估计器预测像素级UV坐标并完成颜色重投影与聚合；然后引入双空间（屏幕空间+UV空间）编码器和UV-屏幕双注意力Transformer，实现结构化跨视图特征交互；最后通过自适应融合机制平衡全局预测与局部观测，输出可驱动的高斯头部化身。这一设计使得UIKA成为首个同时实现前馈推理、无姿态输入、多视图灵活输入和实时动画的统一框架。

## 核心方法与创新机理

UIKA 的核心创新在于通过 **UV 空间作为统一中间表示**，将无姿态标注的多视图输入显式关联起来，从而解决现有前馈头部化身方法在跨视图信息聚合时的根本性瓶颈。其关键创新点可归纳为三个“changed slots”，分别对应跨视图对应建立、特征交互空间和颜色确定方式的范式转变。

### 1. 从隐式编码到显式 UV 对应：跨视图对应的建立

现有前馈方法（如 **GAGAvatar**、**LAM**、**GPAvatar**）通常将多视图输入分别编码后直接融合，缺乏显式的跨帧对应机制。当输入图像缺乏相机姿态和表情标注时，这种隐式编码方式难以可靠地判断不同视图中的像素是否属于面部的同一语义区域，导致多视图信息聚合不可靠，尤其在极端表情和视角下重建质量下降。

UIKA 将这一过程转变为**像素级面部 UV 坐标估计**（Sec. 3.1）。具体而言，给定 $N$ 张无姿态输入图像 $\{I_s^i\}_{i=1}^N$，面部对应估计器 $\mathcal{U}$ 为每张图像预测像素级 UV 坐标：

$$U^i = \mathcal{U}(I_s^i), \quad i \in [1,N]$$

随后，利用预测的 UV 坐标将屏幕空间颜色重投影至共享 UV 空间：

$$I_{uv}^i = \mathrm{Reproj}(I_s^i, U^i)$$

这一重投影操作的关键在于：**UV 空间独立于相机姿态和角色表情**，因此不同视图的同一语义区域（如鼻尖、眼角）会被映射到 UV 空间的相同位置。这为后续的多视图信息聚合提供了结构化、可对齐的表示基础。多个重投影图像进一步通过聚合模块生成 UV 观察图 $I_{aggr}$ 和置信度图 $\gamma_{aggr}$：

$$I_{aggr}, \gamma_{aggr} = \mathrm{Aggr}(I_{uv}^1, \ldots, I_{uv}^N)$$

这一设计将原本“无对应”的多视图融合问题转化为“有对应”的 UV 空间融合问题，是 UIKA 在无姿态设定下取得显著性能提升的核心因果机制。

### 2. 从单空间注意力到 UV-屏幕双注意力：特征交互空间的拓展

传统方法通常仅在屏幕空间使用注意力机制进行特征交互，这有利于保留局部高频细节，但缺乏对全局面部结构的感知能力。UIKA 引入了 **UV 注意力分支**，与屏幕注意力并行工作，形成双空间特征交互架构（Sec. 3.2）。

具体而言，可学习的 UV 令牌 $\mathcal{Z}$ 在 Transformer 层中同时接收来自屏幕空间和 UV 空间的注意力更新：

$$\mathcal{Z}' = \mathcal{Z} + \mathrm{MLP}(\mathcal{Z} + \Delta \mathcal{Z}_s + \Delta \mathcal{Z}_{uv})$$

其中 $\Delta \mathcal{Z}_s$ 来自屏幕空间注意力，负责捕获局部纹理和细节；$\Delta \mathcal{Z}_{uv}$ 来自 UV 空间注意力，利用 UV 空间的对应独立性提供全局结构约束。这种双分支设计的优势在于：**屏幕注意力提供局部观测的保真度，UV 注意力提供跨视图的结构一致性**，两者互补，避免了单一空间注意力在无姿态条件下的歧义性问题。

消融实验（Table 4）验证了这一创新的决定性作用：移除 UV 注意力分支后，PSNR 从 22.61 降至 22.21，LPIPS 从 0.082 升至 0.091，且出现明显的细节丢失（Figure 5(c)）。

### 3. 从直接预测到自适应融合：颜色确定方式的改进

现有方法通常由网络直接预测最终颜色，或仅使用单一来源的颜色信息。UIKA 提出**自适应颜色融合机制**（Sec. 3.3），将全局预测颜色与局部观测颜色进行动态加权组合。

UV 解码器从 UV 令牌和聚合图中解码出 Gaussian 属性，包括预测颜色 $\hat{c}_k$ 和融合权重 $w_k$。最终 Gaussian 颜色 $c_k$ 由预测颜色与聚合颜色 $c_k^{aggr}$ 自适应融合得到：

$$c_k = w_k \hat{c}_k + (1 - w_k) c_k^{aggr}$$

其中 $w_k$ 是每个 Gaussian 学习到的融合权重。这一设计的精妙之处在于：**在观测充分的区域（如正面、中性表情），模型可以更多地依赖重投影的局部颜色，保证纹理保真度；在遮挡或观测稀疏的区域，模型则更多地依赖全局预测，保证颜色一致性**。消融实验表明，用固定权重代替自适应融合权重会导致重建细节偏差（Figure S8(d)），而移除颜色聚合模块则使 PSNR 降至 22.39（Table 4）。

### 创新总结

上述三个 changed slots 构成了一个完整的因果链条：**显式 UV 对应**为多视图信息提供了结构化对齐基础 → **双空间注意力**利用这一基础实现局部细节与全局结构的互补融合 → **自适应颜色融合**根据观测质量动态平衡预测与观测。这一设计使得 UIKA 在无姿态标注的任意数量输入图像设定下，能够实现高质量、可驱动的 3D Gaussian 头部化身重建，在单目自重建（PSNR 21.69 vs. 21.03）和多视图自重建（PSNR 22.50 vs. 17.11）中均显著超越现有基线。

UIKA 是一个前馈式（feed-forward）可驱动 3D 高斯头部化身重建框架，其核心设计目标是：**在无需相机姿态或表情标注的条件下，从任意数量（单张或多张）的输入图像中一次性推理出高保真、可动画化的头部模型**。该框架将这一挑战分解为三个紧密耦合的阶段——面部对应估计与颜色重投影、双空间特征编码与交互、以及 UV 解码与自适应融合——最终输出一个基于 FLAME 模型驱动的经典 3D Gaussian 表示。

### 输入与输出规范

**输入**：$N$ 张无姿态标注的人脸图像 $\{I_s^i\}_{i=1}^N$，$N$ 可从 1 变化至任意数量（例如单张自拍、多视角采集）。输入图像无需提供相机内/外参或表情参数，这使 UIKA 在实用场景中具有显著的应用灵活性。

**输出**：一个规范空间下的可动画化 3D Gaussian 头部化身，包含每个 Gaussian 的位置偏移 $\Delta \mu_k$、颜色 $c_k$、不透明度 $o_k$、缩放 $s_k$ 和旋转 $r_k$ 等属性。该化身可通过标准线性混合蒙皮（Linear Blend Skinning, LBS）基于 FLAME 模型参数实现实时驱动，渲染速度达到 220 FPS。

### 流水线总览

如图 Figure 2 所示，UIKA 的完整流水线由以下功能模块串联构成：

![[assets/figures/papers/paper_list_l1083_https_arxiv_org_abs_2601_07603/figures/003_Figure_2.jpg]]
*Figure 2: Pipeline Overview. Given a set of pose-free input images, our pipeline begins with a facial correspondence estimator that predicts UV coordinates for valid facial pixels, and the corresponding colors are reprojected onto the shared UV space. The source images (screen space) and reprojected images (UV space) are encoded through two dedicated encoders, producing multi-scale features from both screen space and UV space. We then apply screen attention and UV attention to inject these into learnable UV tokens, which are then decoded into UV Gaussian attribute maps while incorporating the aggregated color and confidence map. The resulting canonical Gaussian head avatar supports animation via stan...*

**1. 面部对应估计器（Facial Correspondence Estimator）**
对每张输入图像 $I_s^i$，该模块预测像素级的面部 UV 坐标 $U^i = \mathcal{U}(I_s^i)$，仅覆盖有效面部像素。这一步骤建立了屏幕空间像素与规范 UV 空间之间的显式映射，是后续跨视图信息聚合的基础。

**2. 颜色重投影与聚合（Color Reprojection & Aggregation）**
利用预测的 UV 坐标，将屏幕空间颜色重投影至共享 UV 空间：$I_{uv}^i = \mathrm{Reproj}(I_s^i, U^i)$。多张图像的重投影结果通过聚合模块融合为 UV 观察图 $I_{aggr}$ 和置信度图 $\gamma_{aggr}$，后者编码了每个 UV 像素位置在不同视图中被观测到的可靠程度。

**3. 双空间编码器（Dual-Space Encoders）**
框架同时维护两条并行的特征提取路径：屏幕空间编码器（基于冻结的 DINOv3）从原始输入图像中提取局部细节特征；UV 空间编码器（轻量 CNN）从重投影聚合图中提取全局结构特征。两者输出多尺度特征图，分别服务于后续的屏幕注意力和 UV 注意力分支。

**4. UV-屏幕双注意力 Transformer（UV-Screen Dual-Attention Transformer）**
这是框架的核心信息交互枢纽。一组可学习的 UV 令牌 $\mathcal{Z}$ 通过两个并行的交叉注意力分支与双空间特征进行交互：屏幕注意力分支捕获视角相关的局部纹理细节，UV 注意力分支利用 UV 空间的对应独立性实现结构化的跨视图信息匹配。令牌更新遵循 $\mathcal{Z}' = \mathcal{Z} + \mathrm{MLP}(\mathcal{Z} + \Delta \mathcal{Z}_s + \Delta \mathcal{Z}_{uv})$，其中 $\Delta \mathcal{Z}_s$ 和 $\Delta \mathcal{Z}_{uv}$ 分别来自两个注意力分支的输出。

**5. UV 解码器与自适应融合（UV Decoder & Adaptive Fusion）**
更新后的 UV 令牌与聚合图 $I_{aggr}$、置信度图 $\gamma_{aggr}$ 一同送入 UV 解码器，预测每个 Gaussian 的规范空间属性，包括预测颜色 $\hat{c}_k$。最终 Gaussian 颜色通过自适应融合机制确定：$c_k = w_k \hat{c}_k + (1 - w_k) c_k^{aggr}$，其中 $c_k^{aggr}$ 是从聚合图中采样的观测颜色，融合权重 $w_k$ 由网络自主学习。这一设计使模型能够在全局预测与局部观测之间动态平衡，在遮挡或极端视角下优先信赖预测颜色，在充分观测区域则保留高保真细节。

**6. 动画驱动（Animation）**
重建的规范空间 Gaussian 化身通过线性混合蒙皮与 FLAME 模型的姿态和表情参数绑定，实现实时动画驱动。值得注意的是，FLAME 参数仅在动画阶段使用，重建过程本身完全不依赖这些标注。

### 关键设计决策

UIKA 在架构层面的核心创新在于 **UV 空间作为统一的跨视图对应中介**。与现有前馈方法（如 **GAGAvatar**、**LAM** 等仅在屏幕空间操作）或优化式方法（如 **InvertAvatar** 依赖测试时迭代）不同，UIKA 通过预测像素级 UV 坐标，将多视图信息聚合问题转化为 UV 空间内的结构化融合问题。这一设计的因果机制是：UV 坐标天然独立于相机姿态和表情变化，因此在 UV 空间中建立的对应关系消除了姿态歧义，使得即使输入图像的视角和表情差异极大，跨视图信息交互仍然可靠。消融实验证实，移除 UV 注意力分支会导致 PSNR 从 22.61 降至 22.21，并出现明显的细节丢失（Table 4, Figure 5(c)），验证了该设计的关键作用。

UIKA 的整体流水线（Figure 2）由五个关键模块构成，其核心设计围绕“UV空间作为统一表示”展开，以解决无姿态标注下的跨视图信息聚合难题。

### 3.1 面部对应估计与颜色重投影

该模块是整个流水线的入口，负责建立跨视图的显式对应。给定一组姿态自由的输入图像 $\{I_s^i\}_{i=1}^N$，面部对应估计器 $\mathcal{U}$ 为每张图像预测像素级的面部UV坐标：

$$U^i = \mathcal{U}(I_s^i), \quad i \in [1,N]$$

其中 $U^i \in \mathbb{R}^{H \times W \times 2}$ 表示每个有效面部像素在共享UV空间中的坐标。利用该对应关系，可将屏幕空间颜色重投影至UV空间：

$$I_{uv}^i = \mathrm{Reproj}(I_s^i, U^i), \quad i \in [1,N]$$

由于UV空间独立于相机姿态和表情，所有输入图像的重投影结果天然对齐。随后，通过聚合模块 $\mathrm{Aggr}$ 将多张重投影图像融合为单一的UV观察图 $I_{aggr}$ 和置信度图 $\gamma_{aggr}$：

$$I_{aggr}, \gamma_{aggr} = \mathrm{Aggr}(I_{uv}^1, \ldots, I_{uv}^N)$$

置信度图记录了每个UV像素位置被有效观测的频率，为后续解码器提供观测可靠性信号。

### 3.2 双空间编码与UV-屏幕双注意力Transformer

为同时利用屏幕空间的局部细节和UV空间的全局结构，UIKA设计了双空间编码器：冻结的DINOv3编码器提取屏幕空间多尺度特征，轻量CNN编码器提取UV空间多尺度特征，得到两组特征图 $\{F_s^j\}$ 和 $\{F_{uv}^j\}$。

Transformer的核心操作是通过双分支注意力将上述特征注入一组可学习的UV令牌 $\mathcal{Z}$。每个Transformer块中，UV令牌的更新公式为：

$$\mathcal{Z}' = \mathcal{Z} + \mathrm{MLP}(\mathcal{Z} + \Delta \mathcal{Z}_s + \Delta \mathcal{Z}_{uv})$$

其中 $\Delta \mathcal{Z}_s$ 是屏幕注意力分支的输出——UV令牌作为Query，屏幕空间特征作为Key和Value，捕捉局部纹理细节；$\Delta \mathcal{Z}_{uv}$ 是UV注意力分支的输出——UV令牌与UV空间特征交互，利用UV空间的对应独立性建立跨视图的结构化信息匹配。两个分支的注意力输出相加后，经MLP残差更新令牌。屏幕空间特征也同步更新：

$$F_j' = F_j + \mathrm{MLP}(F_j + \Delta F_j)$$

### 3.3 UV解码器与自适应颜色融合

更新后的UV令牌 $\mathcal{Z}^l$ 与UV聚合图 $I_{aggr}$、置信度图 $\gamma_{aggr}$ 一起送入UV解码器 $\mathcal{D}$，预测每个Gaussian的属性：

$$\{\hat{c}_k, w_k, o_k, \Delta \mu_k, s_k, r_k\} = \mathcal{D}(\mathcal{Z}^l; I_{aggr}, \gamma_{aggr})$$

其中 $\hat{c}_k$ 是网络预测的全局颜色，$w_k \in [0,1]$ 是自适应融合权重，$o_k$ 是不透明度，$\Delta \mu_k$ 是相对于FLAME模型顶点的偏移量，$s_k$ 和 $r_k$ 分别是缩放和旋转参数。

最终Gaussian颜色 $c_k$ 通过自适应融合预测全局颜色与局部聚合颜色得到：

$$c_k = w_k \hat{c}_k + (1 - w_k) c_k^{aggr}$$

其中 $c_k^{aggr}$ 是从 $I_{aggr}$ 中采样得到的局部观测颜色。该机制允许网络在全局预测（鲁棒但可能模糊）与局部观测（精确但可能不完整）之间动态平衡：在观测充分的区域，$w_k$ 趋近于0，优先信任局部颜色；在遮挡或观测稀疏区域，$w_k$ 趋近于1，依赖全局预测。

### 3.4 动画驱动

生成的经典3D Gaussians绑定在FLAME模型的顶点上，通过标准的线性混合蒙皮（LBS）实现实时动画驱动，渲染帧率达到220 FPS。

## 实验与关键发现

### 实验设置与评估协议

UIKA在**VFHQ**和**NeRSemble-v2**两个数据集上进行训练与评估，覆盖单目与多视图两种输入模式。训练目标为加权损失函数：

$$\mathcal{L} = \lambda_{\mathrm{l1}} \mathcal{L}_{\mathrm{l1}} + \lambda_{\mathrm{lpips}} \mathcal{L}_{\mathrm{lpips}} + \lambda_{\mathrm{ssim}} \mathcal{L}_{\mathrm{ssim}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}$$

其中 $\lambda_{\mathrm{l1}}$ 和 $\lambda_{\mathrm{lpips}}$ 设为1.0，$\lambda_{\mathrm{ssim}}$ 和 $\lambda_{\mathrm{reg}}$ 设为0.1。偏移正则化项 $\mathcal{L}_{\mathrm{reg}} = \frac{1}{N} \sum_{i=1}^{N} \left\| \Delta \mu_i - \epsilon \right\|_2$ 约束Gaussian偏移量接近零，防止形变过度。

评估指标包括自重建（self reenactment）和跨重建（cross reenactment）两种协议下的PSNR、SSIM、LPIPS，以及跨重建专用的身份相似度CSIM、平均表情距离AED、平均关键点距离AKD和平均姿态距离APD。此外，还通过用户研究（Table S4）评估渲染质量、运动一致性和身份保持的主观感受。

### 主实验结果

#### 单目自重建

在VFHQ和NeRSemble-v2的单目自重建任务上，UIKA在所有指标上均优于现有前馈方法（Table 2）。PSNR达到**21.69**，较Portrait4D-v2的21.03提升0.66 dB；LPIPS降至**0.105**，较Portrait4D-v2的0.134降低0.029。SSIM为0.867，同样领先。值得关注的是，在跨重建任务中，UIKA的CSIM为0.649，略低于GAGAvatar的0.678（-0.029），表明身份保持能力仍有提升空间。

![[assets/figures/papers/paper_list_l1083_https_arxiv_org_abs_2601_07603/figures/005_Table_2.jpg]]
*Table 2: Quantitative results on the monocular setting in VFHQ and NeRSemble-v2 datasets*

#### 多视图自重建

多视图设置下，UIKA的优势更为显著（Table 3）。PSNR达到**22.50**，远超DiffusionRig的16.97（+5.53 dB）和GPAvatar的17.11（+5.39 dB）。LPIPS为**0.120**，较GPAvatar的0.313降低0.193，降幅超过60%。AED和AKD分别为0.064和3.437，也大幅领先所有基线。这些结果表明，UIKA的UV空间跨视图信息聚合机制在多视图场景下具有决定性优势。

![[assets/figures/papers/paper_list_l1083_https_arxiv_org_abs_2601_07603/figures/006_Table_3.jpg]]
*Table 3: Quantitative results on the multi-view setting in NeRSemble-v2 datasets*

#### 跨重建表现

在跨重建协议下，UIKA同样保持领先。多视图跨重建的CSIM为0.666，APD为0.153，均优于GPAvatar（CSIM 0.648，APD 0.178）和InvertAvatar（CSIM 0.543，APD 0.199）。单目跨重建中，UIKA的CSIM为0.649，虽略低于GAGAvatar的0.678，但综合考虑PSNR和LPIPS的优势，整体重建质量仍占优。

### 消融实验

消融实验在NeRSemble-v2单目自重建设置下进行（Table 4），系统验证了各核心组件的贡献：

![[assets/figures/papers/paper_list_l1083_https_arxiv_org_abs_2601_07603/figures/007_Table_4.jpg]]
*Table 4: Quantitative results for ablation study on the monocular setting in NeRSemble-v2 datasets for self reenactment*

- **UV注意力分支**：移除后PSNR从22.61降至22.21（-0.40 dB），LPIPS从0.082升至0.091。定性结果（Figure 5(c)）显示细节明显丢失，证实UV空间的结构化跨视图交互对高质量重建至关重要。
- **颜色聚合模块**：移除后PSNR降至22.39（-0.22 dB），细节准确性下降，表明多视图颜色信息的显式融合优于隐式学习。
- **合成数据集训练**：移除后PSNR降至21.86，且在极端视角下出现重建崩溃（Figure S3），说明合成数据的多样性对模型鲁棒性不可或缺。
- **自适应融合权重**：用固定权重替代学习权重导致重建细节偏差（Figure S8(d)），验证了每Gaussian独立学习融合权重对平衡全局预测与局部观测的必要性。

![[assets/figures/papers/paper_list_l1083_https_arxiv_org_abs_2601_07603/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative results for ablation study in the monocular settings in NeRSemble-v2 dataset*

### 失败模式与局限性

1. **FLAME表达能力的上限**：UIKA依赖FLAME模型进行动画驱动，无法捕捉精细的面部动态，如细微皱纹、微表情和舌头动作。这在高保真重建场景下构成根本性限制。
2. **训练数据偏差**：训练数据（VFHQ、NeRSemble-v2及合成数据）可能存在人口统计学偏差，对少数群体的重建性能可能下降或失败，需要在实际部署中谨慎评估。
3. **计算冗余**：计算和内存消耗随输入视图数线性增长，但性能提升在超过一定视图数后逐渐饱和。Table S2的延迟分析揭示了视图依赖模块的计算瓶颈，提示需要更高效的视图选择或压缩机制。

### 用户研究

用户研究（Table S4）要求参与者对渲染质量、运动一致性和身份保持进行1-5分评分。UIKA综合评分**4.37**，显著超过第二名的3.54分，在三个维度上均获最高评价，与定量指标的优势一致。

### 关键图表结论

- **Table 1**：UIKA是唯一同时满足前馈推理、无姿态输入和实时动画（≥30 FPS）的方法，在实用性和效率上具有明确优势。
- **Figure 3**：定性对比显示，UIKA在唇部细节、眼部区域和面部轮廓的重建上明显优于GAGAvatar、Portrait4D-v2和GPAvatar，尤其在多视图设置下优势更为突出。
- **Figure 4**：随输入视图数增加，重建质量和3D一致性持续提升，验证了UV空间聚合机制对多视图信息的有效利用。
- **Figure 5**：消融可视化直观展示了移除UV注意力、颜色聚合等模块后出现的颜色不一致和细节退化，与定量结果相互印证。

![[assets/figures/papers/paper_list_l1083_https_arxiv_org_abs_2601_07603/figures/009_Figure_4.jpg]]
*Figure 4: Qualitative results of different numbers of input views in VFHQ and NeRSemble-v2 dataset*

## 定位与知识库关联

### 1. 问题定位与技术断点

3D头部化身重建领域长期面临一个核心矛盾：**高保真重建通常依赖精确的相机姿态与表情参数，而灵活的前馈方法又难以处理任意数量和视角的输入图像**。现有方法大致分为两条路线：

- **优化式方法**：通过测试时优化（如GAN逆推）实现高质量重建，但耗时且依赖姿态标注。代表性工作如 **InvertAvatar**（优化式GAN逆推head avatar）。
- **前馈式方法**：追求推理效率，但多数仍需要姿态信息或仅支持单目输入。例如 **GAGAvatar**、**LAM** 等单目前馈Gaussian方法，以及 **Portrait4D-v2** 等条件生成式方法，在跨视角泛化上存在明显瓶颈。

UIKA的技术断点在于：**在无姿态标注的任意数量输入图像中，缺乏显式的跨帧对应机制，导致多视图信息聚合不可靠，尤其在极端表情和视角下重建质量下降**。这一断点的本质是屏幕空间特征缺乏结构化的对应关系——不同图像中的同一面部区域在像素空间中位置各异，直接进行特征交互极易引入噪声。

### 2. 核心因果杠杆

UIKA的解决方案围绕一个关键因果杠杆展开：**通过预测像素级面部UV坐标并利用UV空间作为统一表示，引入UV注意力机制实现结构化的跨视图信息交互和融合**。

这一杠杆的有效性源于UV空间的核心性质：**对应独立性**。无论相机视角或表情如何变化，面部同一语义点（如鼻尖、眼角）在UV空间中的坐标是固定的。因此，将屏幕空间颜色重投影至UV空间后，不同视图的信息天然对齐，消除了姿态歧义。

在此基础上，UIKA设计了三个关键机制：

1. **显式跨视图对应**：通过面部对应估计器预测像素级UV坐标，将屏幕颜色重投影至共享UV空间并聚合，建立显式的多视图对应关系。这与基线方法（如 **GPAvatar** 的隐式编码、**DiffusionRig** 的扩散先验）形成根本差异。

2. **双空间注意力交互**：引入UV注意力分支，与屏幕空间注意力并行工作。屏幕注意力捕获局部纹理细节，UV注意力利用全局结构对应，两者联合更新可学习UV令牌，实现信息互补。

3. **自适应颜色融合**：每个Gaussian学习融合权重 $w_k$，动态平衡网络预测的全局颜色 $\hat{c}_k$ 与重投影的局部观测颜色 $c_k^{aggr}$，公式为 $c_k = w_k \hat{c}_k + (1 - w_k) c_k^{aggr}$。这避免了单一颜色来源导致的细节偏差或颜色不一致。

### 3. 方法谱系与知识库定位

#### 3.1 与前馈Gaussian化身的对比

| 维度 | **GAGAvatar / LAM** | **UIKA** |
|------|---------------------|----------|
| 输入灵活性 | 单目 | 任意数量（1至多视图） |
| 姿态需求 | 需要相机/表情参数 | 完全无姿态 |
| 跨视图对应 | 隐式编码 | 显式UV坐标对应 |
| 特征交互空间 | 仅屏幕空间 | 屏幕+UV双空间注意力 |

GAGAvatar和LAM作为单目前馈方法，在推理速度上有优势，但受限于单目输入的固有歧义，在极端视角下的重建质量下降明显。UIKA通过UV空间的显式对应，将多视图信息有效聚合，在相同单目设置下PSNR达到21.69（vs GAGAvatar的20.51），在多视图设置下PSNR更是达到22.50，远超 **GPAvatar**（前馈多视图NeRF-style avatar）的17.11。

#### 3.2 与扩散/生成式方法的对比

**DiffusionRig** 和 **Portrait4D-v2** 等基于扩散或条件生成的方法，依赖强大的生成先验来补全缺失信息。但这带来了两个问题：一是推理速度较慢，难以实现实时动画（UIKA渲染速度达220 FPS）；二是生成结果的身份保持不稳定。在跨重建任务中，UIKA的CSIM达到0.649，虽略低于GAGAvatar的0.678，但结合PSNR和LPIPS的显著优势，表明其在保真度与身份保持之间取得了更好的平衡。

#### 3.3 在知识库中的定位

UIKA在3D头部化身重建知识库中的定位可概括为：

- **输入灵活性**：首个同时支持单目和多视图、完全无姿态标注的前馈方法（Table 1中唯一同时满足FF、PF、RTA三项特性的方法）。
- **表示创新**：将UV空间从传统的纹理映射角色提升为跨视图信息交互的核心媒介，开辟了UV引导的化身建模新范式。
- **技术融合**：结合了Gaussian Splatting的实时渲染优势、Transformer的跨注意力机制、以及UV空间的几何先验，形成了一套完整的前馈重建-动画流水线。

### 4. 适用边界与局限

#### 4.1 已知局限

1. **FLAME表达能力的上限**：UIKA的动画驱动依赖FLAME模型的线性混合蒙皮，无法捕捉精细的面部动态，如细微皱纹、微表情和舌头动作。这是参数化模型的固有限制，非UIKA特有。

2. **计算复杂度与视图数的权衡**：计算和内存消耗随输入视图数增长，而性能提升在超过一定视图数后饱和。消融实验显示，从单视图到多视图的PSNR提升显著，但超过16视图后的边际收益递减，存在计算冗余。

3. **训练数据偏差**：训练数据（VFHQ、NeRSemble-v2及合成数据）可能存在人口统计学偏差，对少数群体的重建性能可能下降。论文明确指出这一风险，但未量化偏差的具体表现。

#### 4.2 适用场景边界

- **最适场景**：拥有1-16张任意视角人脸图像，需要快速生成可驱动3D头部的应用（如视频会议、虚拟社交、游戏角色创建）。
- **谨慎场景**：需要极端微表情捕捉（如影视级面部动画）、或输入对象与训练数据分布差异较大时。
- **不适用场景**：需要捕捉舌头、牙齿细节等FLAME模型未建模的区域；对计算资源极度敏感的移动端部署（需权衡视图数与推理成本）。

### 5. 开放问题与后续方向

1. **视图数饱和点的精确刻画**：当视图数继续增加（>16）时，重建质量的饱和点具体在何处？能否设计更高效的视图选择或压缩机制，在保持质量的同时降低计算开销？

2. **人口统计偏差的量化与缓解**：训练数据中的偏差具体表现在哪些属性（肤色、年龄、面部特征）上？能否通过数据增强或公平性约束来缓解？

3. **超越FLAME的表达能力**：能否将UV对应引入更丰富的面部表示（如动态纹理、神经细节场），以捕捉FLAME预定义拓扑之外的微细动态？

4. **大规模部署的效率优化**：在前馈推理效率与日益增长的视图带来的计算开销之间，如何设计自适应计算分配策略（如根据视图质量动态选择关键帧）？

5. **跨模态扩展**：UV空间的对应独立性使其天然适合融合多模态信息（如深度图、红外图），未来可探索将UIKA框架扩展到RGB之外的输入模态。

## 原文 PDF

![[paperPDFs/CVPR_2026/UIKA_Fast_Universal_Head_Avatar_from_Pose_Free_Images.pdf]]
