---
title: "Cross-View Splatter: Feed-Forward View Synthesis with Georeferenced Images"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Cross_View_Splatter_Feed_Forward_View_Synthesis_with_Georeferenced_Images.pdf
project_link: "https://nianticspatial.github.io/cross-view-splatter/"
code_link: null
aliases:
- CVS
- CVSFFVSGI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过双向交叉注意力将卫星正射特征与地面透视特征对齐，并将卫星视角的几何预测形式化为相对于参考帧的高度图回归（而非深度），利用已知空间分辨率的正射投影将高度图提升为高斯溅射位置。
primary_logic: 利用可公开获取的正射卫星影像作为全局场景结构先验，与 GPS 标记的地面图像在统一坐标系下联合预测高斯溅射，从而在稀疏地面对图像时显著改善场景覆盖和新视图合成质量。
claims:
- 在 Tanks and Temples 数据集上，Combined 模型在所有上下文视图数下的 PSNR/SSIM/LPIPS 均优于仅用地面图像的 Ground 模型以及所有基线方法，例如 3 视图时 Combined PSNR 12.00 vs. Ground PSNR 10.61。
- 分层评估表明，卫星分支在输入图像重叠率较低（IoU ≤ 0.15）时带来的增益最大，验证了卫星先验在稀疏覆盖时的关键作用。
- 消融实验显示，添加卫星分支（Combined）相比仅地面（Ground）在 Metropolis 测试集上 PSNR 从 17.10 提升至 18.63，且一致性损失、天空正则化等设计均对性能有正面贡献。
- Tanks and Temples (3 context views) 上 PSNR↑ = 12.00 (Ours Combined)
---

# Cross-View Splatter: Feed-Forward View Synthesis with Georeferenced Images

> [!tip] 核心洞察
> 利用可公开获取的正射卫星影像作为全局场景结构先验，与 GPS 标记的地面图像在统一坐标系下联合预测高斯溅射，从而在稀疏地面对图像时显著改善场景覆盖和新视图合成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 跨视角 Splatter：基于地理参考图像的前馈视图合成 |
| 英文题名 | Cross-View Splatter: Feed-Forward View Synthesis with Georeferenced Images |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.19656) · [Project](https://nianticspatial.github.io/cross-view-splatter/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Cross-View Splatter |
| Dataset | Tanks and Temples |

> [!tip] 效果简介
> - Tanks and Temples (3 context views) 上，PSNR↑ 12.00 (Ours Combined) vs 10.61 (Ours Ground-only) (+1.39)；SSIM↑ 0.3855 (Ours Combined) vs 0.3763 (Ours Ground-only) (+0.0092)；PSNR↑ 12.00 (Ours Combined) vs 10.93 (AnySplat) (+1.07)。

## 概要

### 问题与瓶颈

仅依赖地面视角图像进行大规模室外场景重建面临根本性困难：地面视图的视场有限，难以覆盖建筑背面、屋顶等被遮挡区域，导致几何和外观信息严重缺失。而卫星正射影像虽然能提供全局场景结构，却缺乏透视深度信息，传统基于运动恢复结构（SfM）和多视角立体（MVS）的方法无法直接利用这类跨视角数据。**核心瓶颈**在于，如何将具有全局结构先验的卫星正射视图与局部细节丰富的地面透视图像在统一的几何框架下有效融合。

### 核心方法与洞察

**Cross-View Splatter** 提出了一种前馈式跨视角高斯溅射（Gaussian Splatting）方法，其核心洞察是：利用可公开获取的正射卫星影像作为全局场景结构先验，与仅需 GPS 位置标记（无需完整 6DoF 姿态）的地面图像在统一坐标系下联合预测 3D 高斯溅射。方法的关键机制包括：

- **双向交叉注意力特征对齐**：在预训练 3D 重建模型（VGGT）的交替注意力骨干中注入双向交叉注意力层，实现卫星正射特征与地面透视特征的深度融合。
- **高度图回归替代深度预测**：将卫星视角的几何预测形式化为相对于参考帧的高度图回归（而非深度），利用已知空间分辨率的正射投影将高度图提升为高斯溅射位置，从而绕开了卫星视图缺乏透视深度信息的问题。
- **统一坐标框架**：以第一张地面图像相机坐标系为世界原点，卫星正射视图与该参考帧对齐，地面和卫星分支预测的高斯溅射在统一坐标系下合并渲染。

### 方法定位

Cross-View Splatter 属于**前馈式稀疏视图合成**方法，在方法谱系中填补了“地面+卫星跨视角联合重建”的空白。与仅使用地面图像的基线（如 **MVSplat**、**DepthSplat**、**NoPoSplat**、**Long-LRM**）相比，本方法引入了卫星正射影像作为显式全局几何先验；与仅使用卫星图像进行地面视图着色的 **Sat2Density+** 不同，本方法通过高度图回归实现了从卫星视图到 3D 几何的直接预测；与扩散式生成模型 **SEVA** 不同，本方法保持前馈架构，仅基于可见区域预测几何，不进行不可见区域的幻觉式生成。模型初始化利用 **AnySplat** 的预训练权重，并通过卫星特定层进行微调。

### 主要结果

在 **Tanks and Temples** 室外场景稀疏视图合成基准上，Combined（地面+卫星）模型在所有上下文视图数设置下均显著优于仅用地面图像的 Ground 模型及所有对比基线。以 3 视图设置为例，Combined 的 PSNR 达到 12.00，相比 Ground-only 的 10.61 提升 1.39 dB，相比 AnySplat 的 10.93 提升 1.07 dB。分层评估表明，**卫星分支在输入图像重叠率较低（IoU ≤ 0.15）时带来的增益最大**，验证了卫星先验在稀疏覆盖场景下的关键作用。消融实验进一步证实，添加卫星分支使 Metropolis 测试集 PSNR 从 17.10 提升至 18.63，且深度一致性损失、天空正则化等设计均对性能有正面贡献。



### 问题背景：稀疏地面图像的大场景新视图合成

从一组稀疏的地面透视图像合成任意新视角的三维场景，是计算机视觉和空间计算中的核心挑战。传统方法依赖于运动恢复结构（Structure-from-Motion, SfM）和多视角立体匹配（Multi-View Stereo, MVS），通过特征匹配和三角测量重建场景的显式几何。然而，当输入图像数量稀少、视角覆盖不足时，SfM/MVS 面临根本性困难：地面图像仅能捕捉场景的局部透视外观，无法覆盖被遮挡的建筑物背面、屋顶或远处区域，导致重建结果出现大面积的几何空洞和外观缺失。

与此同时，现代地图服务（如 Google Maps、Azure Maps）提供了覆盖全球大部分城市区域的高分辨率正射卫星影像。这些卫星影像以鸟瞰视角（Bird's-Eye View, BEV）捕捉了完整的场景布局——建筑轮廓、道路结构、植被分布——天然具备全局场景结构的先验信息。但卫星正射影像本身缺乏透视深度信息，无法直接转化为三维几何表示。如何在统一的坐标系下，将卫星影像的全局结构先验与地面图像的局部细节外观有效融合，是解决稀疏视图合成问题的关键突破口。

### 现有方法缺口：地面与卫星信息的割裂

当前的前馈式新视图合成方法大致沿两条独立路径发展：

**地面视角路线**：以 **MVSplat**、**DepthSplat**、**NoPoSplat** 为代表的前馈高斯溅射（3D Gaussian Splatting, 3DGS）方法，通过端到端网络从多张地面图像直接预测三维高斯原语的位置、协方差和外观参数。这些方法在密集输入设置下表现优异，但在稀疏视图条件下，由于缺乏对未观测区域的任何先验，几何预测严重退化。**AnySplat** 和 **Long-LRM** 等基于大规模预训练的模型虽提升了泛化能力，仍无法弥补输入覆盖不足带来的根本性信息缺失。

**卫星视角路线**：**Sat2Density+** 等方法尝试从单张卫星图像推断地面视角的密度场或深度图，但卫星影像仅用于着色或风格迁移，缺乏与地面图像在几何层面的显式对齐。这类方法通常将卫星信息作为外观先验而非几何先验使用，未能充分利用正射投影带来的空间分辨率优势。

**核心缺口**：尚无方法将卫星影像的全局几何先验与地面图像的局部细节在统一的三维坐标系下进行前馈式融合。现有工作要么完全忽略卫星信息，要么将其作为孤立的外观条件，缺乏跨视角的几何对齐机制。

### 本文动机：以卫星正射影像为全局几何锚点

本文的核心动机在于回答一个根本性问题：**能否利用公开可获取的正射卫星影像，为稀疏地面图像的新视图合成提供可靠的全局几何先验？**

这一动机建立在以下观察之上：
1. 正射卫星影像具有已知的空间分辨率（如每像素对应 0.1 米），这意味着从卫星视角预测的像素级高度可以直接通过正射投影转换为三维空间中的高斯位置，无需像地面深度那样依赖复杂的透视反投影。
2. 现代 GPS 定位精度（通常 1-5 米误差）足以将地面图像与卫星影像在水平面上粗略对齐，为跨视角特征融合提供了空间基础。
3. 大规模预训练的三维重建基础模型（如 **VGGT**）已具备从地面图像预测深度和相机姿态的强能力，只需增加轻量的卫星分支和跨视角注意力层，即可将卫星先验注入现有管线。

基于上述动机，本文提出 **Cross-View Splatter**——一种前馈式跨视角高斯溅射方法，其设计目标为：在仅需 GPS 标记的地面图像和一张对应区域的正射卫星影像作为输入的条件下，预测统一坐标系下的三维高斯溅射，显著改善稀疏覆盖场景下的几何完整性和新视图合成质量。



## 核心方法与创新机理

Cross-View Splatter 的核心创新在于将一张公开可获取的正射卫星影像作为全局场景结构先验，与 GPS 标记的地面透视图像在统一坐标系下联合预测高斯溅射，从而在稀疏地面覆盖条件下显著改善场景覆盖和新视图合成质量。这一核心思想通过以下关键设计实现：

### 1. 输入模态的跨视角扩展

传统前馈视图合成方法（如 MVSplat、DepthSplat、NoPoSplat、Long-LRM）仅依赖地面透视图像，在输入视图稀疏或重叠率低时面临严重的几何和外观缺失。Cross-View Splatter 将输入扩展为**地面透视图像 + 一张正射卫星图像**（Figure 2），利用卫星影像提供的全局俯视结构信息弥补地面视角的覆盖盲区。这一设计的关键洞察在于：正射卫星影像具有已知的空间分辨率（米/像素），可直接将像素坐标映射到真实世界坐标，从而为 3D 几何预测提供稳定的度量参考。

### 2. 卫星几何表示：从深度回归到高度图回归

现有利用卫星信息的方法（如 Sat2Density+）通常仅将卫星影像用于着色或密度场推断，缺乏对卫星视角几何的显式建模。Cross-View Splatter 将卫星视角的几何预测形式化为**相对于参考帧的高度图回归**（而非深度），利用正射投影的已知空间分辨率 $r^{\mathrm{sat}}$ 将高度图直接转换为高斯溅射的 3D 位置：

$$
\pmb{\mu}_j^{\mathrm{sat}} = \left( \frac{u}{r^{\mathrm{sat}}} \quad \frac{v}{r^{\mathrm{sat}}} \quad h^{\mathrm{sat}}(u, v) \right)^{\top}
$$

这一设计避免了传统透视投影中深度与尺度的模糊性，使卫星分支能够以物理上有意义的方式贡献 3D 几何。

### 3. 双向交叉注意力特征融合

为实现卫星与地面特征的深层对齐，Cross-View Splatter 在 VGGT 的交替注意力骨干中注入了**双向交叉注意力层**（$\operatorname{Attn}_{\mathrm{meta}}$）：

$$
\operatorname{Attn}_{\mathrm{meta}}(t^{\mathrm{sat}}, t^{\mathrm{ground}}) = \mathcal{A}_2(t^{\mathrm{sat}}, \mathcal{A}_1(t^{\mathrm{ground}}, t^{\mathrm{sat}}, t^{\mathrm{sat}}))
$$

该机制通过两个残差交叉注意力层，使卫星 token 和地面 token 在统一的特征空间中交换信息，从而实现跨视角的几何与外观对齐。

### 4. 多层级损失函数设计

相比仅依赖地面深度损失、相机损失和 RGB 损失的传统方法，Cross-View Splatter 引入了多层级监督信号：

- **卫星高度损失**：直接监督卫星分支的高度图预测；
- **组合渲染损失**：将地面和卫星高斯溅射合并后渲染，提供端到端的联合监督；
- **BEV 正交渲染损失**：通过正交投影将组合高斯溅射渲染到卫星平面，提供俯视视角的显式监督；
- **天空正则化损失**：包括天空深度惩罚（将天空区域推向远距）和天空不透明度提升（使天空像素不透明），有效抑制了地面视角中天空区域的伪影。

### 5. 统一的 ℓ2 场景归一化

传统方法仅对地面深度和姿态进行归一化，Cross-View Splatter 将卫星高度图和空间分辨率也纳入统一的 ℓ2 归一化方案，确保了地面分支和卫星分支在空间尺度上的一致性，这对于跨视角几何融合至关重要。

这些创新设计的有效性在消融实验中得到了系统验证：添加卫星分支使 Metropolis 测试集上的 PSNR 从 17.10 提升至 18.63；分层评估进一步表明，卫星分支在输入图像重叠率较低（IoU ≤ 0.15）时带来的增益最大，精确验证了卫星先验在稀疏覆盖场景中的关键作用（Figure 8, Table 4）。



Cross-View Splatter 是一个前馈式模型，其整体 pipeline 以**地理参考的多视角图像**为输入，在统一的 3D 坐标框架内联合预测地面视角和鸟瞰视角的高斯溅射（3D Gaussian Splats）。图 2 给出了方法架构的全貌。

**输入与坐标系统。** 模型接收两类输入：(1) 带有 GPS 标签的地面透视图像 $\{I_i^{\text{ground}}\}_{i=0}^{N-1}$；(2) 一张从地图服务获取的正射校正卫星图像 $I^{\text{sat}}$。坐标系统的原点定义在参考地面帧 $I_0^{\text{ground}}$ 的相机中心，该帧的姿态被设为单位阵；卫星图像 $I^{\text{sat}}$ 的空间位置亦以此为基准，且其 BEV 坐标系与 $I_0^{\text{ground}}$ 的朝向对齐——相机的视线方向 $z_c$ 在卫星视图中指向上方（图 3）。其他地面图像 $I_{i>0}^{\text{ground}}$ 的姿态均相对于 $I_0^{\text{ground}}$ 表达。

**pipeline 信息流。** 整个前向过程可概括为四个阶段：

1. **地面编码与预训练基础模型。** 地面图像首先经过一个强大的预训练 3D 重建基础模型 **VGGT**（Wang et al.）进行编码。VGGT 的交替注意力骨干网络负责提取每张地面图像的 patch token，并预测初始的相机姿态、内参以及像素级深度图。这一步骤继承了 VGGT 在多视角立体任务上的强先验。

2. **卫星编码与跨视角特征融合。** 卫星图像被独立编码为 patch token $t^{\text{sat}}$。关键的跨视角信息交换发生在**双向交叉注意力层**（$\text{Attn}_{\text{meta}}$）中：该模块被注入到 VGGT 的交替注意力骨干内，通过两层残差交叉注意力 $\mathcal{A}_1$ 和 $\mathcal{A}_2$ 在卫星 token 和地面 token 之间进行双向信息流动（式 1）。这使得卫星特征能够感知地面场景的透视结构，同时地面特征也能吸收卫星视角提供的全局场景先验。

3. **几何预测分叉。** 融合后的 token 分别进入两个几何预测分支：
   - **地面分支：** 地面 token 通过 DPT 深度头（$\text{DPT}_{\text{depth}}$）回归每像素深度 $d_j^{\text{ground}}$ 及其置信度 $C_j^{\text{ground}}$。
   - **卫星分支：** 卫星 token 通过 DPT 高度头（$\text{DPT}_{\text{height}}$）回归相对于 $I_0^{\text{ground}}$ 的**高度图** $h^{\text{sat}}(u,v)$ 及其置信度 $C^{\text{sat}}$（式 3）。这一设计是核心创新之一：将 BEV 几何预测形式化为高度图回归而非深度回归，避免了卫星正射投影下深度定义的歧义性。

4. **高斯溅射生成与合并。** 两个分支分别从几何预测生成 3D 高斯溅射：
   - **地面高斯：** 将预测的深度图通过透视反投影得到高斯均值 $\boldsymbol{\mu}_j^{\text{ground}}$，并预测协方差、不透明度和球谐系数。
   - **卫星高斯：** 利用卫星图像已知的空间分辨率 $r^{\text{sat}}$，通过正射投影将高度图转换为高斯均值 $\boldsymbol{\mu}_j^{\text{sat}} = (u/r^{\text{sat}}, v/r^{\text{sat}}, h^{\text{sat}}(u,v))^\top$（式 4），并预测其他高斯属性。
   - 两组高斯溅射在统一的坐标框架下合并，通过近似 alpha 混合（式 14）渲染最终视图。

**损失函数与正则化。** 训练由多分量加权损失驱动（式 13），包括相机参数损失 $\mathcal{L}_{\text{cam}}$、置信度加权深度损失 $\mathcal{L}_{\text{depth}}$、深度一致性损失 $\mathcal{L}_{\text{const}}$、卫星高度损失 $\mathcal{L}_{\text{height}}$、地面渲染损失 $\mathcal{L}_{\text{RGB}}^{\text{ground}}$、组合渲染损失 $\mathcal{L}_{\text{RGB}}^{\text{combined}}$、卫星渲染损失 $\mathcal{L}_{\text{RGB}}^{\text{sat}}$、天空正则化损失 $\mathcal{L}_{\text{sky}}$ 和 BEV 正交渲染损失 $\mathcal{L}_{\text{BEV}}$。其中天空正则化（式 11-12）通过天空分割 mask 对天空区域的深度施加远距惩罚并提升不透明度，有效抑制了天空区域的漂浮伪影。

**场景归一化。** 为保证跨场景的空间一致性，所有度量量（深度、高度、平移向量）均通过基于反投影深度的每批 $\ell_2$ 尺度因子 $s$（式 15）进行归一化。卫星高度图和空间分辨率也被纳入该归一化方案。

**推理阶段。** 值得注意的是，尽管训练时利用了公开高程数据作为高度真值监督，推理阶段仅需地面图像（含 GPS 标签）和卫星图像，无需额外的高度真值。

### 补充图表

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/002_Figure_2.jpg]]
*Figure 2: Method overview: Given geolocalized ground images and a single orthorectified satellite perspective, our model synthesizes 3D Gaussian splats in a shared coordinate frame. Ground views exchange information with satellite views within bidirectional cross-attention layers. Gaussians are predicted separately from ground and satellite branches, which are then combined into a unified coordinate frame. Although public elevation data is leveraged during training, only the satellite image and ground view(s) are necessary for inference*



Cross-View Splatter 的核心技术路线可概括为：**在统一坐标系下，通过双向交叉注意力融合地面透视特征与卫星正射特征，分别预测地面深度与卫星高度图，并利用正射投影将高度图提升为高斯溅射位置，最终合并两组高斯进行渲染。** 以下按模块展开关键公式与设计逻辑。

### 3.1 双向交叉注意力（Attn_meta）

模型以 VGGT 的交替注意力骨架为基础，在其内部注入双向交叉注意力层，使卫星 patch tokens $t^{\mathrm{sat}}$ 与地面 patch tokens $t^{\mathrm{ground}}$ 之间交换信息：

$$
\operatorname{Attn}_{\mathrm{meta}}(t^{\mathrm{sat}}, t^{\mathrm{ground}}) = \mathcal{A}_2\big(t^{\mathrm{sat}}, \mathcal{A}_1(t^{\mathrm{ground}}, t^{\mathrm{sat}}, t^{\mathrm{sat}})\big)
$$

该机制由两层残差交叉注意力 $\mathcal{A}_1$、$\mathcal{A}_2$ 串联构成：第一层以地面 token 为 query、卫星 token 为 key/value；第二层以卫星 token 为 query、第一层输出为 key/value。这种**双向信息流**使地面视角获得全局场景结构先验，卫星视角获得局部细节约束，是实现跨视角几何对齐的核心操作。

### 3.2 地面深度预测

经过交叉注意力增强后的地面 tokens $t_i^{\mathrm{ground}}$ 送入 DPT 解码头，回归每像素深度与置信度：

$$
d_j^{\mathrm{ground}}, C_j^{\mathrm{ground}} = \mathrm{DPT}_{\mathrm{depth}}(t_i^{\mathrm{ground}})
$$

其中 $d_j^{\mathrm{ground}}$ 为像素 $j$ 的预测深度，$C_j^{\mathrm{ground}}$ 为对应的置信度。深度图通过相机内参反投影得到地面高斯的位置 $\pmb{\mu}_j^{\mathrm{ground}}$，同时预测协方差、不透明度与球谐系数等高斯属性。

### 3.3 卫星高度预测与正射投影

与地面分支不同，卫星视角的几何被形式化为**高度图回归**而非深度回归。卫星 tokens $t^{\mathrm{sat}}$ 经 DPT 头预测相对于参考帧 $I_0^{\mathrm{ground}}$ 的高度图与置信度：

$$
h^{\mathrm{sat}}, C^{\mathrm{sat}} = \mathrm{DPT}_{\mathrm{height}}(t^{\mathrm{sat}})
$$

利用已知的卫星影像空间分辨率 $r^{\mathrm{sat}}$（单位：米/像素），通过正射投影将高度图直接转换为高斯均值：

$$
\pmb{\mu}_j^{\mathrm{sat}} = \begin{pmatrix} \mu_x \\ \mu_y \\ \mu_z \end{pmatrix} = \begin{pmatrix} \frac{u}{r^{\mathrm{sat}}} \\ \frac{v}{r^{\mathrm{sat}}} \\ h^{\mathrm{sat}}(u, v) \end{pmatrix}
$$

这一设计的核心优势在于：**正射投影天然避免了透视深度估计中的尺度模糊问题**，且高度图可直接利用公开高程数据（如 USGS LiDAR）作为训练监督信号。

### 3.4 组合渲染与损失函数

地面高斯与卫星高斯在统一坐标系下合并，通过近似 alpha 混合进行渲染：

$$
C_{\mathrm{3DGS}}^{\mathrm{combined}} \approx C_{\mathrm{3DGS}}^{\mathrm{ground}} + (1 - \alpha_{\mathrm{ground}}) C_{\mathrm{3DGS}}^{\mathrm{sat}}
$$

该近似将两次前向渲染合并为一次，在保持精度的同时降低计算开销。

总损失函数为多任务加权组合：

$$
\begin{aligned}
\mathcal{L}_{\mathrm{total}} = &\lambda_{\mathrm{cam}} \mathcal{L}_{\mathrm{cam}} + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{const}} \mathcal{L}_{\mathrm{const}} + \lambda_{\mathrm{height}} \mathcal{L}_{\mathrm{height}} \\
&+ \lambda_{\mathrm{ground}} \mathcal{L}_{\mathrm{RGB}}^{\mathrm{ground}} + \lambda_{\mathrm{combined}} \mathcal{L}_{\mathrm{RGB}}^{\mathrm{combined}} + \lambda_{\mathrm{sat}} \mathcal{L}_{\mathrm{RGB}}^{\mathrm{sat}} \\
&+ \lambda_{\mathrm{sky}} \mathcal{L}_{\mathrm{sky}} + \lambda_{\mathrm{bev}} \mathcal{L}_{\mathrm{BEV}}
\end{aligned}
$$

各损失项含义：
- **$\mathcal{L}_{\mathrm{cam}}$**：相机姿态与内参的 L1 损失，$\mathcal{L}_{\mathrm{cam}} = \|\hat{\pmb{T}} - \pmb{T}\|_1 + \|\hat{\pmb{K}} - \pmb{K}\|_1$
- **$\mathcal{L}_{\mathrm{depth}}$**：置信度加权深度损失，$\mathcal{L}_{\mathrm{depth}} = \sum_j (\|\hat{d}_j^{\mathrm{ground}} - d_j^{\mathrm{ground}}\|_2 - \alpha \log C_j)$
- **$\mathcal{L}_{\mathrm{height}}$**：卫星高度图的置信度加权损失，结构与深度损失对称
- **$\mathcal{L}_{\mathrm{const}}$**：地面深度与卫星高度在重叠区域的几何一致性损失
- **$\mathcal{L}_{\mathrm{RGB}}^{\mathrm{ground}}$、$\mathcal{L}_{\mathrm{RGB}}^{\mathrm{sat}}$、$\mathcal{L}_{\mathrm{RGB}}^{\mathrm{combined}}$**：分别对地面渲染、卫星视角渲染、合并渲染施加的 RGB 损失
- **$\mathcal{L}_{\mathrm{sky}}$**：天空正则化损失，由天空深度惩罚 $\mathcal{L}_{\mathrm{sky-depth}}$ 与不透明度提升 $\mathcal{L}_{\mathrm{sky-alpha}}$ 组成，其中 $\mathcal{L}_{\mathrm{sky-alpha}} = \sum_j M_j \cdot \|1 - o_j\|_1$，$M_j$ 为天空分割掩码
- **$\mathcal{L}_{\mathrm{BEV}}$**：将组合高斯通过正交投影渲染到卫星平面，与真实卫星图像对比的 BEV 监督损失

### 3.5 场景归一化

为保证地面深度与卫星高度在统一尺度下训练，采用基于反向投影深度的批归一化方案：

$$
s = \frac{1}{M} \sum_{j=1}^{M} \|\pmb{\mu}_j\|_2
$$

其中 $s$ 为每批样本的 ℓ2 尺度因子，所有度量量（深度、高度、平移向量）均除以 $s$ 进行归一化。该方案将卫星高度图与空间分辨率统一纳入归一化框架，保证跨视角空间一致性。

### 补充图表

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/003_Figure_3.jpg]]
*Figure 3: Coordinate conventions. We consider camera*

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/004_Figure_4.jpg]]
*Figure 4: Example reconstruction outputs on scenes not seen during training. Left to right: input ground images, input satellite image, predicted height map, predicted height confidence (black: low, red: high), predicted ground Gaussians, predicted combined Gaussians*



## 实验与关键发现

### 主干实验：稀疏视图合成

Cross-View Splatter 在两个经地理对齐的室外基准上进行了稀疏视图合成评估：**Tanks and Temples**（10 个场景）和 **DL3DV**（40 个场景）。评估时，每个场景使用 1、2 或 3 张上下文图像作为输入，目标视图为场景内剩余图像。所有方法均使用公开预训练权重，并在新对齐的场景上按各自推荐协议重新运行，以确保对比公平性。

**Tanks and Temples 结果（Table 2）**：Combined 模型在所有上下文视图数下均取得最优 PSNR/SSIM/LPIPS。以 3 视图为例，Combined 的 PSNR 达到 12.00，显著优于 Ground-only 的 10.61（+1.39）以及最强基线 AnySplat 的 10.93（+1.07）。在 1 视图和 2 视图设置下，Combined 同样保持领先，且卫星分支的增益在输入视图更稀疏时更为突出。值得注意的是，仅使用卫星高度图（Terrain-only）即可获得与部分地面基线可比的结果，验证了卫星几何先验的独立价值。

**DL3DV 结果（Table 3）**：在更大规模的 40 场景基准上，Combined 模型在 1/2/3 视图设置下均优于所有对比方法。Ground-only 变体本身已具备竞争力，而加入卫星分支后进一步提升，表明跨视角融合策略在不同场景类型下具有一致的增益。

**与扩散模型 SEVA 的对比（Table 5, Figure 14）**：SEVA 作为生成式扩散模型，能够“幻觉”出不可见区域的内容，在部分指标上表现接近。但 Cross-View Splatter 作为前馈方法，仅从可见区域预测几何，在几何一致性上更具优势，且推理速度远快于扩散采样。

### 分层评估：卫星增益的边界条件

为量化卫星分支的实际贡献边界，论文按输入视图间的图像重叠率（IoU）对 Tanks and Temples 测试样本进行分桶（Figure 8）。结果清晰表明：**当 IoU ≤ 0.15 时，Combined 相比 Ground-only 的 PSNR 增益最大**；随着重叠率升高，地面图像本身的覆盖已较充分，卫星信息的边际增益递减。这一发现直接支持了核心主张——卫星正射影像作为全局结构先验，在稀疏覆盖场景下发挥关键作用。

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/011_Figure_8.jpg]]
*Figure 8: Stratified evaluation. Bucketed PSNR performance (5% bins) vs. image overlap on our geolocalized Tanks & Temples dataset*

### 消融实验

在 Metropolis 数据集上进行的消融实验（Table 4）逐项验证了各设计组件的贡献：

- **卫星分支**：加入卫星分支后，PSNR 从 Ground-only 的 17.10 提升至 Combined 的 18.63（+1.53），SSIM 和 LPIPS 同步改善。
- **深度一致性损失与天空正则化**：在 VGGT+3DGS 基线上依次添加这两项，PSNR 从 14.20 提升至 17.10，表明它们对地面分支几何质量的基础性作用。
- **BEV 渲染损失**：提供正交投影下的显式监督，进一步稳定了卫星高度图的学习。

定性消融（Figure 9）在 2 张输入图像的极端稀疏设置下展示了卫星分支的填补能力：Ground-only 模型在建筑背面和屋顶区域产生明显空洞或模糊，而 Combined 模型利用卫星高度图有效填充了这些地面视图不可见的结构。

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/012_Figure_9.jpg]]
*Figure 9: Qualitative ablation of model with 2 input images*

### 失败模式与局限性

1. **视角覆盖盲区**：当目标相机朝向天空或正下方地面等卫星视图中不存在的方向时，模型无法可靠推断几何，因为两个分支均缺乏对应信息源。
2. **无卫星覆盖场景**：室内、隧道、高架桥下等无卫星影像或严重遮挡的环境不在方法适用范围内。
3. **高重叠下的边际增益**：如分层评估所示，当输入地面图像重叠充分时，卫星分支的贡献有限，此时计算开销可能不划算。
4. **地理泛化受限**：训练数据主要来自美国城市区域（Metropolis、VIGOR），向不同地理特征和建筑风格的区域泛化能力未经充分验证。
5. **卫星图像时差问题**：卫星影像与地面图像的采集时间可能相差数年，导致建筑改建或景观变化（Figure 15），此时高度图预测可能产生系统性错误。

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/020_Figure_15.jpg]]
*Figure 15: Limitations of satellite imagery. Notice how a building has been rebuilt and expanded in the right frame compared to the left taken a few years ago. This is Family scene in Tanks and Temples*

### GPS 灵敏度分析

Table 6 报告了在 1 视图设置下对 GPS 定位精度的灵敏度。当向 GPS 坐标添加不同量级的高斯噪声时，Combined 模型的 PSNR 呈缓慢下降趋势，但在合理噪声范围内（数米级）性能退化有限，表明方法对定位误差具有一定鲁棒性。这得益于卫星正射影像本身的空间覆盖范围较大，对精确对齐的容忍度较高。

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/019_Table_6.jpg]]
*Table 6: GPS sensitivity analysis results for the 1-context view setting for Combined (Cross-View Splatter) method on Tanks & Temples*

### 补充图表

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/007_Table_2.jpg]]
*Table 2: Outdoor Tanks and Temples sparse-view synthesis. Metrics are averaged over 10 scenes. For Cross-View Splatter, we report ground-only, terrain-only, and combined (ground+terrain) reconstructions. Methods marked with * use ground-truth intrinsics. Methods marked with * require multi-view input and were given one additional adjacent frame during testing. Sat2Density† takes a single satellite image stylized with one context image (see Fig. 6)*

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/008_Table_3.jpg]]
*Table 3: Outdoor DL3DV sparse-view synthesis results. Results are averaged over 40 scenes*

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/013_Table.jpg]]

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/017_Figure_14.jpg]]
*Figure 14: Qualitative comparison to SEVA. SEVA is a generative based model capable of hallucinating unseen areas whereas our Cross-View Splatter is a feed-forward approach that predicts geometry only for visible regions in ground images and satellite image*

![[assets/figures/papers/paper_list_l2456_https_arxiv_org_abs_2605_19656/figures/018_Table_5.jpg]]
*Table 5: Comparison to diffusion based SEVA model on our geoaligned Tanks and Temples benchmark*



## 定位与知识库关联

### 与前馈视图合成方法的继承与突破

Cross-View Splatter 的方法骨架直接继承自 **VGGT**（Weinzaepfel et al., 2024）的交替注意力架构，并采用 **AnySplat**（InternRobotics）的预训练权重进行模型初始化。与 MVSplat、DepthSplat、NoPoSplat 等仅依赖地面透视图像的前馈高斯溅射方法不同，本工作在输入端引入了可公开获取的正射卫星影像作为全局场景结构先验，这是方法谱系中的核心分叉点。

在几何表示层面，传统前馈方法（如 MVSplat、DepthSplat）将场景几何建模为逐像素深度图，通过透视投影反投影得到高斯位置。Cross-View Splatter 保留了地面分支的深度预测，但将卫星视角的几何预测重新形式化为**相对于参考帧的高度图回归**，利用已知空间分辨率的正射投影将高度图提升为三维高斯位置。这一设计规避了传统 SfM/MVS 无法直接利用卫星正射影像的瓶颈——正射影像缺乏透视深度信息，但具备精确的空间尺度。

与 **Sat2Density+** 等卫星到地面密度场方法相比，Cross-View Splatter 的关键差异在于：Sat2Density+ 仅使用卫星影像进行着色或密度场估计，而本方法通过双向交叉注意力层（Attn_meta）将卫星与地面特征在统一特征空间中显式对齐，使两分支的几何预测相互增强。

### 特征融合与跨视角对齐机制

特征融合的“因果旋钮”在于在 VGGT 的交替注意力骨干中注入双向交叉注意力层：

$$
\operatorname { A t t n } _ { \operatorname { m e t a } } ( t ^ { \mathrm { s a t } } , t ^ { \mathrm { g r o u n d } } ) = \mathcal { A } _ { 2 } ( t ^ { \mathrm { s a t } } , \mathcal { A } _ { 1 } ( t ^ { \mathrm { g r o u n d } } , t ^ { \mathrm { s a t } } , t ^ { \mathrm { s a t } } ) )
$$

该机制使卫星 patch tokens 与地面 tokens 在两个方向上交换信息，卫星分支从地面特征中获得局部细节线索，地面分支从卫星特征中获得全局空间上下文。这一设计是方法区别于所有仅地面基线（Ground-only、MVSplat、DepthSplat、NoPoSplat）的根本架构差异。

### 损失函数设计的增量贡献

在损失函数层面，本方法在 VGGT 原有的深度损失、相机损失、RGB 渲染损失基础上，增加了四个关键组件：

1. **卫星高度损失**：监督卫星分支的高度图回归；
2. **组合渲染损失**：对合并后的高斯溅射进行端到端渲染监督；
3. **BEV 正交渲染损失**：将组合高斯通过正交投影渲染到卫星平面，提供鸟瞰视角的显式监督；
4. **天空正则化损失**：包括天空深度惩罚（将天空像素推向远距）和天空不透明度提升（使天空高斯不透明），解决地面视图中的天空区域在 3D 重建中常被错误建模为近距几何的问题。

消融实验（Table 4）表明，深度一致性损失和天空正则化将 VGGT+3DGS 基线的 PSNR 从 14.20 提升至 17.10，而加入卫星分支后进一步提升至 18.63，验证了各损失组件的独立贡献。

### 与扩散式新视图合成方法的关系

与 **SEVA** 等扩散式生成方法相比，Cross-View Splatter 采用前馈预测范式，仅对地面图像和卫星图像中的可见区域进行几何预测，不进行内容幻觉。Figure 14 的定性对比显示，SEVA 能够生成不可见区域的合理内容但缺乏几何一致性，而本方法在几何保真度上更优但无法填补完全不可见区域。Table 5 的定量对比确认了这一权衡关系。

### 适用边界与条件约束

方法的适用边界由以下条件严格定义：

1. **场景类型限制**：仅适用于室外场景，要求存在可获取的正射卫星影像。室内、隧道、高架桥下、密集树冠遮挡等场景因卫星影像不可用或严重遮挡而无法工作；
2. **视角方向限制**：当目标相机看向天空或正下方地面等未在卫星视图中出现的区域时，几何无法可靠推断；
3. **输入稀疏度条件**：分层评估（Figure 8）表明，卫星分支在输入图像重叠率较低（IoU ≤ 0.15）时增益最大，当输入视图重叠度较高时卫星信息的边际增益减弱；
4. **地理泛化限制**：训练数据主要源于美国城市区域（Metropolis、VIGOR），向不同地理特征、建筑风格、植被类型的区域泛化能力受限；
5. **时间一致性要求**：卫星图像与地面图像之间可能存在采集时间差异（如建筑改建），导致高度图预测错误（Figure 15 展示了此类失败案例）。

### 开放问题与未来方向

1. **多时相与高分辨率卫星影像**：当前方法仅使用单张正射卫星图像，能否结合多时相或更高分辨率的非正射卫星影像以缓解时间不一致问题并提升细节还原能力？
2. **复杂垂直结构**：如何将方法扩展到具有复杂垂直结构（如立交桥、多层建筑）或动态场景（车辆、行人）的情形？当前高度图表示假设场景为 2.5D 结构，无法处理垂直重叠；
3. **自监督几何学习**：当前训练依赖外部高度真值（USGS LiDAR），在不依赖额外高度真值的情况下，仅利用卫星图像自监督地学习精确的全局几何先验是否可行？
4. **GPS 精度依赖**：Table 6 的 GPS 灵敏度分析表明方法对定位精度有一定容忍度，但在极端 GPS 误差下的行为尚需进一步表征。

### 知识库定位总结

Cross-View Splatter 在方法谱系中占据“前馈跨视角高斯溅射”的独特位置：它既不是纯粹的 ground-only 前馈方法（如 MVSplat/DepthSplat），也不是卫星-only 的密度场方法（如 Sat2Density+），更不是扩散式生成方法（如 SEVA）。其核心知识贡献在于证明了**通过双向交叉注意力将公开可获取的正射卫星影像与地面图像在统一坐标系下联合预测高斯溅射**，能够在稀疏地面图像条件下显著改善场景覆盖和新视图合成质量。这一思路为利用免费地理空间数据增强 3D 场景重建开辟了新方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Cross_View_Splatter_Feed_Forward_View_Synthesis_with_Georeferenced_Images.pdf]]
