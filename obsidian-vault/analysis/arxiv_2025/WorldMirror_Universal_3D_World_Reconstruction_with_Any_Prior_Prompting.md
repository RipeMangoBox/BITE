---
title: WorldMirror Universal 3D World Reconstruction with Any-Prior Prompting
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/WorldMirror_Universal_3D_World_Reconstruction_with_Any_Prior_Prompting.pdf
project_link: null
code_link: null
aliases:
- WorldMirror
- HY-World-Recon
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 多模态先验提示（Multi-Modal Prior Prompting）机制，将相机位姿、内参编码为单令牌、深度图编码为密集令牌，通过动态注入训练策略使模型灵活适应任意先验组合，从而显著提升各项几何预测任务的性能。
primary_logic: 通过将异构几何先验统一编码到前馈Transformer主干中，并配合课程学习策略，可以使单一模型同时应对点云、深度、相机、法线和新视图合成五种任务，并且在有先验可利用时进一步提升精度，即使无先验也能达到当前最优水平。
claims:
- 无任何先验输入的WorldMirror在7-Scenes和DTU上的点云重建精度分别比VGGT和π3提升10.4%和17.8%，证明基础多任务架构的优越性。
- 当利用全部三种先验（内参、深度、位姿）时，WorldMirror在7-Scenes和NRGBD上的平均精度分别比无先验基线提升58.1%和53.1%，表明先验信息能大幅增强重建能力。
- 单令牌先验嵌入在ETH3D/DTU上的平均AUC指标优于密集嵌入（位姿：61.06 vs 60.44；内参：68.96 vs 66.58），证实了紧凑全局表示比密集条件嵌入更有效。
- 在新视图合成任务上，WorldMirror大幅超越前馈基线AnySplat，在RealEstate10K（2视图）上将PSNR从17.62提升至20.62（+3.0 dB），验证了统一几何表示对高质量视图合成的有效性。
---

# WorldMirror Universal 3D World Reconstruction with Any-Prior Prompting

> [!tip] 核心洞察
> 通过将异构几何先验统一编码到前馈Transformer主干中，并配合课程学习策略，可以使单一模型同时应对点云、深度、相机、法线和新视图合成五种任务，并且在有先验可利用时进一步提升精度，即使无先验也能达到当前最优水平。

| 字段 | 内容 |
|------|------|
| 中文题名 | WorldMirror：一种支持任意先验提示的通用三维世界重建框架 |
| 英文题名 | WorldMirror Universal 3D World Reconstruction with Any-Prior Prompting |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2510.10726) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | WorldMirror |
| Dataset | 7-Scenes, RealEstate10K, ScanNet |

> [!tip] 效果简介
> - 7-Scenes (scene-level) 上，Accuracy Mean (Acc.↓, lower is better) 0.043 (WorldMirror no prior) vs 0.046 (VGGT) (-6.5% (relative error reduction))。
> - RealEstate10K (camera pose) 上，AUC@30↑ 86.28 (WorldMirror) vs 77.62 (VGGT) (+11.2% (absolute improvement))。
> - ScanNet (surface normal) 上，Mean angular error↓ 13.8 (WorldMirror) vs 16.0 (StableNormal) (-2.2° (absolute reduction))。

## 概要

现有前馈式三维重建方法普遍以原始图像作为唯一输入，无法有效利用相机内参、位姿和深度图等常见的几何先验信息，导致在无纹理或反射区域等困难场景中性能显著下降。同时，多数方法局限于单一几何任务（如仅估计点云或深度），缺乏统一的通用预测框架。

WorldMirror 针对上述瓶颈，提出了一种**多模态先验提示（Multi-Modal Prior Prompting）**机制。其核心思路是将异构几何先验统一编码到前馈 Transformer 主干中：相机位姿和内参因其紧凑特性被编码为单令牌，深度图则被转换为密集令牌并与图像令牌融合。通过动态注入训练策略，模型可灵活适应任意先验组合，即使无先验输入也能达到当前最优水平。配合课程学习策略，单一模型可同时应对点云、深度、相机、法线和新视图合成五种任务。

实验结果表明，在无任何先验输入的条件下，WorldMirror 在 7-Scenes 和 DTU 上的点云重建精度分别比前馈基线 VGGT 和 π3 提升 **10.4%** 和 **17.8%**；当利用全部三种先验（内参、深度、位姿）时，平均精度进一步提升 **58.1%** 和 **53.1%**。在新视图合成任务上，WorldMirror 大幅超越前馈基线 AnySplat，在 RealEstate10K（2 视图）上将 PSNR 从 17.62 提升至 **20.62**（+3.0 dB）。这些结果验证了统一几何表示与多模态先验融合的有效性。

**方法定位**：WorldMirror 属于前馈式通用三维重建框架，与 VGGT、π3、Fast3R、CUT3R 等点云/相机估计方法，以及 AnySplat、FLARE 等前馈 3DGS 新视图合成方法形成对比。其独特之处在于首次将多模态几何先验以提示形式注入统一架构，并覆盖五项几何预测任务。

**主要局限**：模型在动态场景和自动驾驶环境中的性能欠佳，且当前实现受限于输入视图数量和分辨率（300–700 像素），难以处理数千视图的极端情况。



### 问题背景

从多视角图像中恢复三维几何结构是计算机视觉的核心任务，涵盖点云重建、深度估计、相机位姿估计、表面法线预测以及新视图合成等多个子方向。近年来，前馈式三维重建方法凭借其推理速度快、无需逐场景优化的优势，逐渐成为该领域的研究热点。然而，现有方法在输入灵活性和任务覆盖范围上存在明显局限，制约了其在复杂场景下的泛化能力。

### 现有方法的瓶颈

当前前馈重建方法面临两个关键瓶颈。

**第一，几何先验利用不足。** 大多数方法仅以原始图像作为唯一输入，无法有效利用相机内参、位姿和深度图等常见的几何先验信息。这些先验在实际应用中往往可以轻易获取——例如，智能手机通常提供校准后的内参，SLAM系统可输出粗糙的相机位姿和深度图——但现有模型缺乏统一的机制来吸收这些异构信息。当场景包含无纹理区域、反射表面或透视畸变时，纯视觉输入的模型往往产生不可靠的几何估计。

**第二，任务覆盖碎片化。** 现有方法通常局限于单一或少数几何任务：**VGGT**（Wang et al., 2025a）和 **π3**（Wang et al., 2025c）专注于点云和相机估计，**AnySplat**（Jiang et al., 2025）仅处理新视图合成，**StableNormal**（Ye et al., 2024b）和 **DSine**（Bae & Davison, 2024）则分别聚焦于表面法线预测。这种碎片化导致不同任务之间无法共享几何理解，也难以通过多任务协同提升整体重建质量。

### 本文动机与核心思路

针对上述瓶颈，WorldMirror 提出两个核心设计原则：

1. **多模态先验提示（Multi-Modal Prior Prompting）**：将异构几何先验统一编码为令牌序列，注入前馈Transformer主干。具体而言，相机位姿和内参因其紧凑性被编码为单令牌，深度图因其空间丰富性被编码为密集令牌并与图像令牌对齐。通过动态注入训练策略，模型可灵活适应任意先验组合——从零先验到全部三种先验。

2. **通用几何预测框架**：在单一模型中同时支持点云、深度图、相机参数、表面法线和三维高斯泼溅（3DGS）五种几何输出。这使得不同任务之间可以共享底层几何表征，并通过组合损失函数实现端到端联合优化。

这一设计实现了双重优势：在无可利用先验时，多任务架构本身已能提供具有竞争力的几何预测；当先验可用时，模型可进一步吸收这些信息以显著提升精度。实验表明，无先验的 WorldMirror 在 7-Scenes 和 DTU 上的点云重建精度分别比 VGGT 和 π3 提升 10.4% 和 17.8%；当利用全部三种先验时，平均精度进一步提升 58.1%（7-Scenes）和 53.1%（NRGBD），验证了框架的有效性。



## 核心方法与创新机理

### 问题瓶颈：前馈重建中的先验信息缺失与任务割裂

现有前馈式3D重建方法面临两个核心瓶颈。第一，**先验信息利用率极低**：大多数方法仅以原始图像作为输入，无法有效利用相机内参、位姿和深度图等在实际采集流程中极易获取的几何先验。当场景包含无纹理区域、反射表面或透视畸变时，纯视觉信号不足以支撑精确的几何推理，导致重建质量显著下降。第二，**任务覆盖范围碎片化**：现有工作通常局限于单一几何任务——例如 **VGGT**（Wang et al., 2025a）仅处理点云、相机和深度估计，**AnySplat**（Jiang et al., 2025）仅做新视图合成——缺乏一个统一的框架来同时完成点云重建、深度估计、相机位姿估计、表面法线预测和新视图合成。

### 因果调控旋钮：多模态先验提示机制

WorldMirror的核心创新在于提出了**多模态先验提示**（Multi-Modal Prior Prompting）机制，作为统一框架的因果调控旋钮。该机制将异构的几何先验信息编码为统一的令牌表示，注入前馈Transformer主干：

- **紧凑全局编码**：相机位姿经场景归一化后转换为7维向量（四元数+归一化平移），通过两层MLP投影为单个令牌 $T_i^{cam}$；相机内参（焦距和主点，经图像宽高归一化）同样经MLP投影为单个令牌 $T_i^{intr}$。消融实验证实，这种单令牌嵌入方案在ETH3D/DTU上的平均AUC指标优于密集嵌入方案（位姿：61.06 vs 60.44；内参：68.96 vs 66.58），表明紧凑的全局表示比密集条件嵌入更有效（Table 5）。

- **密集空间编码**：深度图保留空间结构，经浅层卷积网络转换为密集令牌 $T_i^{depth}$，与图像令牌 $T_i^{img}$ 逐元素相加，形成空间对齐的融合特征。

- **动态注入训练策略**：训练过程中随机组合不同先验模态的子集，使模型学会灵活适应任意先验组合——从无先验的纯视觉推理到全部三种先验同时可用的情况。这一策略赋予模型“有则用，无则通”的能力。

### 核心洞察：统一几何表示下的多任务协同

WorldMirror的深层洞察在于：**将点云、深度、相机、法线和3D高斯五种几何属性统一到一个前馈框架中，不仅能实现“一模型多任务”，还能让不同任务之间产生正向协同**。具体而言：

- **共享表征的跨任务增益**：实验表明，添加单一模态的先验不仅改善对应任务的预测，还能提升其他几何任务的性能（Figure 6）。这说明多模态先验促使模型形成更全面的场景几何理解，而非孤立的单任务优化。

- **混合法线监督突破数据瓶颈**：表面法线标注数据稀缺，WorldMirror采用混合监督策略——在有标注的数据集上使用真值监督，同时利用深度图通过平面拟合生成伪法线标签进行补充训练。这使得模型在ScanNet上达到13.8°的平均角度误差，优于扩散模型 **StableNormal**（Ye et al., 2024b）的16.0°（Table 3）。

- **端到端3D高斯预测替代后优化**：与先估计深度再转换高斯位置的两阶段方案不同，WorldMirror使用专用的DPT头直接预测高斯属性，配合体素化剪枝和可微光栅化渲染进行端到端监督。消融实验表明，移除GS DPT头会导致新视图合成质量显著下降，验证了端到端预测框架的必要性。

### 与Baseline的关键差异

| 创新维度 | Baseline做法 | WorldMirror方案 | 证据强度 |
|---------|-------------|----------------|---------|
| **先验输入** | 仅原始图像或单一先验（如UniDepth仅用内参） | 多模态先验提示：位姿/内参→单令牌，深度→密集令牌，动态注入任意组合 | 强（Table 1, 5） |
| **任务覆盖** | 1-2项几何任务 | 点云、深度、相机、法线、3DGS五项任务统一预测 | 强（Table 1-4, 7） |
| **法线监督** | 依赖真值标注（数据稀缺） | 混合监督：标注法线+深度伪法线 | 中强（Table 3） |
| **训练策略** | 固定任务顺序的联合训练 | 课程学习：任务序列、数据调度、分辨率渐进+动态先验注入 | 中（Section A.2） |

### 待验证的开放问题

课程学习策略中任务序列、数据调度和分辨率渐进的具体配比细节尚未完全公开，其对最终性能的贡献量级需要进一步实验验证。此外，单令牌嵌入在极端旋转或大尺度场景下是否会产生全局位置信息的歧义，仍需深入分析。



WorldMirror 的核心设计理念是将异构几何先验统一编码到前馈 Transformer 主干中，使单一模型能够灵活接受任意先验组合，并同时输出点云、深度、相机参数、表面法线和三维高斯（3DGS）五种几何表示。其整体流水线如图 2 所示，包含三个关键阶段：**多模态先验嵌入**、**视觉 Transformer 聚合**和**通用几何预测**。

### 输入与先验嵌入

模型接收多视图图像 $\{I_i\}_{i=1}^N$ 及可选的几何先验——相机位姿、标定内参和深度图。这些先验按模态特性被编码为不同粒度的令牌（Section 3.1）：

- **相机位姿**：将场景缩放到单位立方体后，旋转矩阵转为四元数并与归一化平移向量拼接为 7 维向量，经两层 MLP 投影为**单令牌** $T_i^{cam}$。
- **标定内参**：提取焦距和主点坐标，按图像宽高 $W,H$ 归一化后，同样经两层 MLP 投影为**单令牌** $T_i^{intr}$。
- **深度图**：作为空间信息丰富的模态，被转换为与图像令牌空间对齐的**密集令牌** $T_i^{depth}$，直接与图像令牌 $T_i^{img}$ 相加。

最终，每帧的提示令牌集为：

$$T_i^{prompt} = [T_i^{cam},\; T_i^{intr},\; T_i^{img} + T_i^{depth}], \quad T_i^{prompt} \in \mathbb{R}^{(1+1+H_p \times W_p) \times D}$$

这种设计的关键优势在于：紧凑的全局表示（单令牌）比密集条件嵌入更有效地编码位姿和内参信息。消融实验证实，单令牌位姿嵌入在 ETH3D/DTU 上的平均 AUC 优于密集 Plücker 射线嵌入（61.06 vs 60.44），单令牌内参嵌入同样优于密集 raymap 嵌入（68.96 vs 66.58），且参数量更少（Table 5）。

### 视觉 Transformer 主干

所有视图的提示令牌集被送入视觉 Transformer 主干网络，通过自注意力机制跨视图聚合特征。主干输出增强后的图像令牌 $\hat{T}_i^{img}$ 和相机令牌 $\hat{T}_i^{cam}$，作为下游预测头的基础表示。

### 通用几何预测头

聚合后的特征被分配到五个并行的预测头（Section 3.2）：

- **点云预测**：$\hat{P}_i = \text{DPT}_p(\hat{T}_i^{img})$
- **深度预测**：$\hat{D}_i = \text{DPT}_d(\hat{T}_i^{img})$
- **相机参数预测**：$\hat{E}_i = \text{Transformer}(\hat{T}_i^{cam})$
- **表面法线预测**：$\hat{N}_i = \text{DPT}_n(\hat{T}_i^{img}) / \|\text{DPT}_n(\hat{T}_i^{img})\|_2$
- **三维高斯预测**：$\hat{\boldsymbol{D}}_g, \boldsymbol{F}_g = \text{DPT}_g(\hat{\boldsymbol{T}}^{img})$，随后经卷积网络生成完整高斯属性 $\hat{\boldsymbol{G}} = \text{Conv}(\boldsymbol{F}_g, \boldsymbol{I})$

其中 DPT 头（Ranftl et al., 2021）负责密集回归任务，Transformer 层处理相机参数的全局预测。3D 高斯模块进一步通过体素化剪枝和可微光栅化渲染器生成新视图，实现端到端的几何与外观联合建模。

### 动态先验注入与课程学习

训练时采用**动态先验注入**策略：随机选择可用先验的子集（从无先验到全部三种），使模型学会适应任意先验组合。这配合系统性的**课程学习**策略——逐步调度任务序列、数据配比和分辨率——使单一模型在无先验时达到当前最优水平，而在有先验可利用时进一步提升精度（Section A.2）。

### 训练损失

总损失为五项任务的未加权和：

$$\mathcal{L} = \mathcal{L}_{points} + \mathcal{L}_{depth} + \mathcal{L}_{cam} + \mathcal{L}_{normal} + \mathcal{L}_{3dgs}$$

其中 $\mathcal{L}_{points}$ 包含基于梯度和不确定性的监督，$\mathcal{L}_{cam}$ 为 Huber 损失，$\mathcal{L}_{normal}$ 为角度损失，$\mathcal{L}_{3dgs}$ 包含 RGB 渲染损失（L1 + LPIPS）和梯度一致性损失以抑制浮动点（详见 Appendix A.1）。表面法线监督采用混合策略，同时利用标注数据集和从深度图通过平面拟合生成的伪法线标签，克服了真值法线标注数据稀缺的限制。

### 补充图表

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/002_Figure_2.jpg]]
*Figure 2: Overview of WorldMirror. Given multi-view images with optional priors (depths, calibrated intrinsics, camera poses) as input, our framework encodes each prior modality into tokens and integrates them with image tokens. The composite tokens are subsequently processed by a visual transformer backbone to effectively aggregate multi-view features. The consolidated representations are then passed to multi-task heads to generate comprehensive geometric outputs, including point maps, camera parameters, multi-view depth maps, surface normals, and 3D Gaussians*



WorldMirror的核心架构由两个关键模块构成：**多模态先验提示（Multi-Modal Prior Prompting）** 和 **通用几何预测（Universal Geometric Prediction）**，二者共同实现从任意先验组合到统一几何输出的前馈推理。

### 多模态先验提示

该模块将异构几何先验统一编码为Transformer可处理的令牌序列。针对不同先验的信息密度差异，采用差异化的编码策略：

- **相机位姿**：首先将场景尺度归一化至单位立方体，将旋转矩阵转为四元数并与归一化平移向量拼接为7维向量，经两层MLP投影为单一令牌 $T_i^{cam}$。
- **相机内参**：提取焦距和主点，按图像宽高归一化后经两层MLP投影为单一令牌 $T_i^{intr}$。
- **深度图**：作为密集空间信号，经Patch Embedding转换为与图像令牌空间对齐的密集令牌 $T_i^{depth}$，直接与图像令牌相加融合。

最终形成的多模态提示令牌序列为：

$$T _ { i } ^ { p r o m p t } = [ T _ { i } ^ { c a m } , T _ { i } ^ { i n t r } , T _ { i } ^ { i m g } + T _ { i } ^ { d e p t h } ] , \quad T _ { i } ^ { p r o m p t } \in \mathbb { R } ^ { ( 1 + 1 + H _ { p } \times W _ { p } ) \times D }$$

其中 $H_p \times W_p$ 为图像Patch数量，$D$ 为特征维度。该序列随后输入**视觉Transformer主干**进行多视图特征聚合。

训练时采用**动态先验注入策略**：以固定概率随机丢弃部分先验模态，使单一模型适应从无先验到全先验的任意组合，无需针对每种配置单独训练。

### 通用几何预测

聚合后的多视图特征通过多任务头并行输出五种几何属性：

**点云、深度与相机参数**：采用DPT架构（Ranftl et al., 2021）回归密集输出，相机参数由Transformer层从相机令牌预测：

$$\hat { P } _ { i } = \mathrm { D P T } _ { p } ( \hat { T } _ { i } ^ { i m g } ) , \quad \hat { D } _ { i } = \mathrm { D P T } _ { d } ( \hat { T } _ { i } ^ { i m g } ) , \quad \hat { E } _ { i } = \mathrm { T r a n s f o r m e r } ( \hat { T } _ { i } ^ { c a m } )$$

**表面法线**：由DPT头预测并经L2归一化确保单位长度：

$$\hat { N } _ { i } = \mathbb { D P T } _ { n } ( \hat { T } _ { i } ^ { i m g } ) / \lVert \mathbb { D P T } _ { n } ( \hat { T } _ { i } ^ { i m g } ) \rVert _ { 2 }$$

**3D高斯属性**：DPT头首先生成高斯特征图 $\boldsymbol{F}_g$ 和位置图 $\hat{\boldsymbol{D}}_g$，再由卷积网络融合原始图像预测完整高斯属性（协方差、不透明度、颜色）：

$$\hat { \pmb { G } } = \mathrm { C o n v } (  { \boldsymbol { F } } _ { g } , \pmb { I } ) , \qquad \hat { \pmb { D } } _ { g } ,  { \boldsymbol { F } } _ { g } = \mathrm { D P T } _ { g } ( \hat { \pmb { T } } ^ { i m g } )$$

预测的高斯点云经体素化剪枝后，通过可微光栅化器渲染新视图。

### 训练损失

总损失为五项任务损失的加权和：

$$\mathcal{L} = \lambda_{\mathrm{points}} \mathcal{L}_{\mathrm{points}} + \lambda_{\mathrm{depth}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{cam}} \mathcal{L}_{\mathrm{cam}} + \lambda_{\mathrm{normal}} \mathcal{L}_{\mathrm{normal}} + \lambda_{\mathrm{3dgs}} \mathcal{L}_{\mathrm{3dgs}}$$

其中权重设置为 $\lambda_{\mathrm{points}}=1.0,\ \lambda_{\mathrm{depth}}=1.0,\ \lambda_{\mathrm{cam}}=5.0,\ \lambda_{\mathrm{normal}}=1.0,\ \lambda_{\mathrm{3dgs}}=1.0$。各子损失的具体形式如下：

- **点云损失**（基于梯度和不确定性）：

  $$\mathcal{L}_{\mathrm{point}} = \sum_{i=1}^{N} \| \Sigma_{i}^{P} \odot (\hat{P}_{i} - P_{i}) \| + \| \Sigma_{i}^{P} \odot (\nabla \hat{P}_{i} - \nabla P_{i}) \| - \alpha \log \Sigma_{i}^{P}$$

- **相机损失**（Huber损失）：$\mathcal{L}_{\mathrm{cam}} = \sum_{i=1}^{N} \| E_{i} - \hat{E}_{i} \|_{\epsilon}$

- **法线损失**（角度度量）：$\mathcal{L}_{\mathrm{normal}} = \sum_{i=1}^{N} \alpha_{l} \cdot (1 - |\hat{N_{i}} \cdot N_{i}|)$

- **RGB渲染损失**（L1+LPIPS，仅对可见像素）：$\mathcal{L}_{rgb} = \sum_{i=1}^{N} \| I_{i}[M_{i}] - \hat{I}_{i}[M_{i}] \| + \lambda_{\mathrm{lpips}} \mathrm{LPIPS}(I_{i}[M_{i}], \hat{I}_{i}[M_{i}])$

- **梯度一致性损失**（约束GS渲染深度与伪深度一致，抑制浮动点）：$\mathcal{L}_{\mathrm{consis}} = \sum_{i=1}^{N} \| \nabla \hat{D}_{i}[\hat{M}_{i}] - \nabla \tilde{D}_{i}[\hat{M}_{i}] \|$

### 关键设计要点

1. **单令牌 vs 密集嵌入**：消融实验证实，相机位姿和内参采用单令牌嵌入优于密集嵌入（如Plücker射线或raymap），在ETH3D/DTU上平均AUC分别提升0.62和2.38个百分点，且参数量更少（Table 5）。这表明紧凑的全局表示比空间密集的条件嵌入更有效。

2. **动态先验注入**：配合课程学习策略（任务顺序、数据调度、渐进分辨率），使模型在无先验时已达最优水平，有先验时进一步大幅提升——全先验配置在7-Scenes和NRGBD上平均精度分别比无先验基线提升58.1%和53.1%。

3. **混合法线监督**：由于法线标注数据稀缺，除标注数据集外，还通过平面拟合从真值深度图生成伪法线进行监督，扩展了训练信号来源。

### 补充图表

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/010_Figure_5.jpg]]
*Figure 5: Geometric Priors Unlock Enhanced Scene Reconstruction of WorldMirror. (Top) Camera poses help the model to capture relative view positions accurately. (Middle) Calibrated intrinsic enhances the reconstruction by enabling precise projection modeling and geometry alignment. (Bottom) Depth guidance enables the network to better handle challenging reconstruction scenarios, like perspective distortion, unusual geometric configurations, or partial occlusions*

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/011_Figure_6.jpg]]
*Figure 6: Geometric Priors Boosts Model’s Feed-Forward Performance across All Tasks. Incorporating a single modality not only enhances predictions for its corresponding task but also improves performance across other tasks. This suggests that modal information enables the model to develop a more comprehensive understanding of the overall geometry*

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/001_Figure_1.jpg]]
*Figure 1: WorldMirror is a large feed-forward 3D reconstruction model that takes raw images along with optional priors (depth, calibrated intrinsics, camera pose) as input and produces high-quality geometric attributes in seconds, including point clouds, 3DGS, cameras, depth, and normal maps*



## 实验与关键发现

### 瓶颈突破验证：多模态先验提示的因果效应

WorldMirror的核心主张是多模态先验提示（Multi-Modal Prior Prompting）机制能够成为性能提升的因果旋钮。实验设计从三个层次验证了这一主张：

**无先验基线的SOTA水平。** 即使不注入任何几何先验，WorldMirror的多任务统一架构本身已超越先前最优方法。在7-Scenes和DTU数据集上，点云重建的平均精度（Accuracy Mean）分别比**VGGT**（Wang et al., 2025a）和**π3**（Wang et al., 2025c）提升10.4%和17.8%（Table 1）。这表明统一的几何预测框架——同时学习点云、深度、相机、法线和3D高斯——产生了正向的跨任务知识迁移，即使在没有额外先验的条件下也能建立更强的场景理解。

**单模态先验的递增增益。** 当注入单一模态先验时，性能进一步提升，且增益不仅局限于对应任务。Figure 6的跨任务分析显示，添加深度先验不仅改善深度估计，还提升点云重建和相机位姿估计的精度；添加相机位姿先验同样惠及法线预测和新视图合成。这一现象表明，多模态先验促使模型形成了更完整的几何理解，而非简单的任务特定特征增强。

**全先验组合的最优效果。** 同时利用相机内参、深度图和相机位姿三种先验时，性能达到峰值：在7-Scenes和NRGBD上，平均精度分别比无先验基线提升58.1%和53.1%（Table 1）。这证实了先验信息之间存在互补性——内参提供投影几何约束，深度提供局部表面信息，位姿提供全局视图关系，三者协同作用使重建精度大幅跃升。

### 主要任务性能对比

**点云重建（Table 1）。** 在7-Scenes、NRGBD和DTU三个数据集上，WorldMirror在全先验配置下均取得最优结果。值得注意的是，在DTU这类包含大量无纹理区域的物体级数据集上，仅使用深度先验即可获得显著增益，说明密集深度令牌有效补偿了视觉特征的不足。

**相机位姿估计（Table 2）。** 在RealEstate10K的零样本测试中，WorldMirror的AUC@30达到86.28，远超VGGT的77.62（+11.2%绝对提升）。在TUM-dynamics动态场景数据集上，绝对轨迹误差（ATE）低至0.010。这些结果验证了单令牌位姿嵌入在提供全局视图关系方面的有效性。

**表面法线估计（Table 3）。** 在ScanNet上，WorldMirror的平均角度误差为13.8°，优于扩散式方法**StableNormal**（Ye et al., 2024b）的16.0°和回归式方法**DSine**（Bae & Davison, 2024）。混合监督策略——结合标注法线和从深度图通过平面拟合生成的伪法线——有效缓解了法线标注数据稀缺的问题。

**新视图合成（Table 4）。** 在RealEstate10K的2视图稀疏设定下，WorldMirror的PSNR达到20.62 dB，比前馈基线**AnySplat**（Jiang et al., 2025）的17.62 dB提升3.0 dB。这一显著增益来源于统一的几何表示：3D高斯的位置和属性由DPT头直接从多视图特征中预测，而非依赖后处理优化。Figure 4的定性对比显示，WorldMirror在保持外观保真度的同时，几何感知能力明显更强，尤其在遮挡边界和细结构区域。

### 关键消融实验

**先验嵌入策略（Table 5）。** 在ETH3D和DTU上的平均结果表明，单令牌嵌入在相机位姿（AUC 61.06 vs 60.44）和相机内参（AUC 68.96 vs 66.58）上均优于密集嵌入方案（如Plücker射线或raymap）。单令牌方案不仅精度更高，还减少了参数和计算开销。这验证了紧凑的全局表示比像素对齐的密集条件嵌入更适合编码相机级先验——密集嵌入可能引入空间偏差，干扰图像特征的正常流动。

**新视图合成组件（Table 6）。** 移除新视图监督（仅使用上下文视图损失）导致PSNR从20.29骤降至18.51，说明双视图渲染监督对学习正确的3D高斯分布至关重要。直接用GS DPT头预测高斯属性优于用深度头估计位置后再转换的方案，验证了端到端预测框架避免了中间表示的误差累积。

**几何先验的跨任务溢出（Figure 6）。** 该图量化了单一模态先验对其他任务的提升幅度。例如，仅添加深度先验即可将相机位姿估计的AUC提升约2个百分点。这种跨任务增益表明，多模态先验提示并非简单的特征拼接，而是通过Transformer的自注意力机制实现了不同几何线索的深度融合与互补。

### 失败模式与局限性

论文明确指出了三个主要局限：

1. **动态场景退化。** 模型在自动驾驶等动态场景中性能欠佳，因为训练数据中此类场景的代表性不足。这是数据驱动方法的共性瓶颈，需要扩展数据集或引入时序建模。

2. **分辨率与视图数限制。** 当前实现支持300至700像素的输入分辨率，无法处理数千张视图的极端情况，尤其在消费级GPU上存在内存瓶颈。这限制了在长视频序列重建和大规模场景中的应用。

3. **伪法线监督的精度边界。** 混合监督策略中的伪法线来自深度图的平面拟合，在曲面、细结构或深度噪声较大的区域可能出现退化。该点的定量影响需要进一步验证。

### 重要图表结论速览

- **Figure 6**：单模态先验产生跨任务溢出增益，证明多模态提示机制促成了统一的几何理解。
- **Table 5**：单令牌嵌入优于密集嵌入，紧凑全局表示是编码相机级先验的更优策略。
- **Table 6**：双视图渲染监督和端到端高斯预测是新视图合成性能的关键组件。
- **Figure 4**：定性对比显示WorldMirror在稀疏视图设定下显著改善了外观保真度和几何一致性。
- **Table 8**：WorldMirror预测的点云可作为3DGS优化的初始化，优于随机初始化，验证了前馈预测的几何质量对后优化的正向作用。

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/012_Table_5.jpg]]
*Table 5: Prior Embedding Ablation. Results are averaged over ETH3D and DTU datasets with 10 views as input. ‘Single token’ offers both superior performance and high efficiency*

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/013_Table_6.jpg]]
*Table 6: Novel View Synthsis Ablation. Results are from RealEstate10K, DL3DV, and VR-NeRF*

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/016_Table_8.jpg]]
*Table 8: Novel View Synthesis with 3DGS Optimization on RealEsate10K, DL3DV, and VRNeRF. In Post-Optimization, the random point cloud refers to initializing Gaussian positions randomly, whereas the predicted point cloud uses the point cloud estimated by our method as the initialization of Gaussian positions*

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative Comparisons of Novel View Synthesis. We compare with FLARE and AnySplat on RealEstate10K and DL3DV. The first four columns correspond to the sparse-view setting, while the latter three correspond to the dense-view setting. Our approach surpasses baselines in both appearance fidelity and geometric perception*

### 补充图表

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/004_Table_1.jpg]]
*Table 1: Point map Reconstruction on 7-Scenes, NRGBD, and DTU. We report the performance of WorldMirror under different input configurations. The best results are bold*

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/005_Table_2.jpg]]
*Table 2: Camera Pose Estimation on RealEstate10K, Sintel, and TUM-dynamics. All datasets are excluded from the training set, except that RealEstate10K was included for CUT3R training*

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/006_Table_3.jpg]]
*Table 3: Surface Normal Estimation on ScanNet, NYUv2, and iBims-1. We compare with both regression-based and diffusion-based surface normal estimation approaches. EESNU is trained on ScanNet, thus its in-domain performance is omitted*

![[assets/figures/papers/WorldMirror_Universal_3D_World_Reconstruction_with_Any-Prior_Prompting_f8b2dfa3e8ff/figures/007_Table_4.jpg]]
*Table 4: Novel View Synthesis on RealEstate10K and DL3DV. We compare with feed-forward 3DGS methods under sparse and dense-view settings. FLARE focuses on sparse views NVS and thus its performance under dense-view settings is omitted*



## 定位与知识库关联

### 1. 方法继承与差异定位

WorldMirror 的核心架构建立在 Dense Prediction Transformer（DPT）主干之上，但其关键创新在于将多模态先验提示（Multi-Modal Prior Prompting）机制引入前馈三维重建框架。与现有方法的本质差异体现在以下维度：

**（1）输入范式的根本转变。** 现有前馈方法如 **VGGT**（Wang et al., 2025a）和 **π3**（Wang et al., 2025c）仅以原始图像作为输入，无法利用相机内参、位姿或深度图等常见几何先验。WorldMirror 通过将相机位姿和内参编码为单令牌（single token）、深度图编码为密集令牌（dense token），并采用动态注入训练策略，使单一模型能够灵活适应任意先验组合——从零先验到全部三种先验均可处理。这一设计直接回应了现有方法在无纹理区域或反射表面等困难场景中性能下降的瓶颈。

**（2）任务覆盖的广度突破。** 基线方法普遍局限于1-2项几何任务：VGGT 覆盖点云、相机和深度估计，但不支持法线估计和新视图合成；**AnySplat**（Jiang et al., 2025）专注于前馈3D高斯泼溅的新视图合成；**StableNormal**（Ye et al., 2024b）和 **GeoWizard**（Fu et al., 2024）仅处理表面法线估计。WorldMirror 首次在单一前馈模型中统一支持点云重建、深度估计、相机位姿估计、表面法线预测和3D高斯新视图合成五项任务，实现了真正的通用几何预测。

**（3）法线监督策略的创新。** 现有法线估计方法依赖真实标注数据集，但标注数据稀缺。WorldMirror 提出混合监督策略：同时利用标注法线和通过平面拟合从深度图派生的伪法线（pseudo normals），有效扩展了训练信号来源。这一策略在方法论上具有可迁移性，可为其他需要密集几何监督的任务提供参考。

**（4）训练策略的系统性改进。** 相较于标准联合训练，WorldMirror 引入了课程学习策略，在任务序列、数据调度和渐进分辨率三个维度上进行系统优化，配合动态先验注入机制，使模型在训练效率和最终性能上均获得提升。具体课程细节在附录中说明，但其核心思想是逐步增加任务复杂度和数据多样性。

### 2. 适用边界与能力范围

**输入灵活性。** WorldMirror 支持2至64张多视图图像作为输入，并可选择性接受相机内参、位姿和深度图三种先验的任意子集。模型在无先验条件下已超越现有最优方法，在有先验可利用时性能进一步提升——当全部三种先验输入时，7-Scenes 和 NRGBD 上的平均精度分别提升58.1%和53.1%。

**任务输出范围。** 单一模型可同时输出：点云（point maps）、多视图深度图、相机参数、表面法线图和3D高斯属性（用于新视图合成）。这种多任务统一输出的能力使 WorldMirror 适用于需要多种几何表示的流水线场景。

**分辨率限制。** 当前实现支持300至700像素的输入分辨率，无法有效处理数千张输入视图的极端情况，在消费级GPU上运行时存在显存限制。这是前馈Transformer架构的固有瓶颈，也是未来扩展方向。

**场景泛化边界。** 模型在静态室内外场景（7-Scenes、NRGBD、DTU、RealEstate10K）上表现出色，但在动态场景和自动驾驶环境（如KITTI）中性能欠佳，因为训练数据中这类场景的代表性不足。对于包含大量运动物体的视频序列，模型缺乏时序建模能力，可能导致几何一致性下降。

### 3. 局限性与开放问题

**（1）动态场景建模缺失。** WorldMirror 假设输入视图来自静态场景，缺乏对动态物体的显式建模。在包含行人、车辆等运动物体的场景中，多视图几何一致性假设被破坏，可能导致重建伪影。未来工作需要引入时序建模或运动分割机制。

**（2）单令牌嵌入的表示能力边界。** 实验表明单令牌嵌入优于密集嵌入（位姿：61.06 vs 60.44 AUC；内参：68.96 vs 66.58 AUC），但这种紧凑表示是否会导致旋转歧义或全局位置信息丢失，仍需进一步验证。尤其是在大基线或极端视角变化场景下，单令牌可能无法充分编码复杂的相机配置。

**（3）课程学习策略的透明度。** 论文指出课程学习在任务序列、数据调度和分辨率三个维度上进行，但具体平衡细节未在正文中充分展开。这一策略对最终性能的贡献程度、各维度的敏感性分析以及在不同规模模型上的可迁移性，是需要手动验证的开放问题。

**（4）伪法线监督的精度退化风险。** 混合法线监督中的伪标签通过深度图平面拟合生成，在曲面、细薄结构或深度不连续区域可能出现系统性偏差。这些场景下伪法线的精度退化是否会影响模型对真实几何的理解，论文未提供详细的失败案例分析。

**（5）计算效率与扩展性。** 当前架构在数千张视图的极端场景下存在显存瓶颈。如何将多模态先验机制扩展到长序列输入并实现实时推理，是前馈重建方法走向实际应用的关键挑战。可能的路径包括稀疏注意力机制、分块处理策略或层次化特征聚合。

**（6）与其他前馈方法的公平比较。** 论文在点云和相机位姿评估中采用了统一的测试序列ID映射（Wang et al., 2025c），并在新视图合成中遵循 AnySplat 的测试时相机位姿对齐协议，确保了比较的公平性。但不同方法在训练数据规模、数据配方的差异仍可能影响结论的稳健性，建议读者在复现时关注这些因素。

### 4. 知识库定位

WorldMirror 处于前馈三维重建、多任务几何预测和视觉提示学习的交叉点。其方法论贡献——将异构几何先验统一编码到Transformer主干并通过课程学习联合优化——为后续研究提供了可复用的技术范式。在知识库中，该方法可作为以下方向的基线或对比对象：

- **前馈多视图重建**：与 VGGT、π3、Fast3R、CUT3R 构成方法谱系
- **前馈新视图合成**：与 AnySplat、FLARE 对比
- **统一几何预测**：作为首个覆盖五项几何任务的通用模型，为后续多任务统一框架提供参考
- **先验引导的视觉学习**：多模态先验提示机制可迁移至其他需要融合异构输入的视觉任务



## 原文 PDF

![[paperPDFs/arxiv_2025/WorldMirror_Universal_3D_World_Reconstruction_with_Any_Prior_Prompting.pdf]]
