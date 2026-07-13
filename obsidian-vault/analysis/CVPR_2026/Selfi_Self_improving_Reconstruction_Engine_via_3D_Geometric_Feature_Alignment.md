---
title: "Selfi: Self-improving Reconstruction Engine via 3D Geometric Feature Alignment"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Selfi_Self_improving_Reconstruction_Engine_via_3D_Geometric_Feature_Alignment.pdf
project_link: "https://denghilbert.github.io/selfi"
code_link: null
aliases:
- Selfi
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 提出了一种基于重投影的特征一致性损失函数，利用冻结的VGGT模型的输出（深度图和相机参数）作为伪真值，训练一个轻量级的DPT特征适配器，迫使不同视图中对应于同一三维空间位置的特征具有较高的相似性，从而学习出几何对齐的特征表示。
primary_logic: 利用三维基础模型的自输出作为密集的自监督信号，无需任何外部三维标注或相机真值，即可将基础模型的特征空间转化为几何对齐的特征空间，在此空间中特征相似度同时反映语义内容和三维空间邻近性，从而大幅提升无姿态新视角合成和位姿估计的性能。
claims:
- 在DL3DV和RealEstate10K的所有序列长度与重叠程度设置下，本文方法在PSNR/SSIM/LPIPS上均大幅优于AnySplat、WorldMirror、Flare等无姿态基线，逼近甚至在某些设置下超过使用真值相机参数的3DGS上限。
- 对齐后的特征可直接用于高效的束调整（BA），在DL3DV、MipNeRF360和Tanks&Temples上进一步提升位姿精度和NVS质量，且本文的特征匹配方法在处理大规模图像集时比CoTracker更鲁棒，不会因内存不足而失败。
- 消融实验证实：移除几何特征对齐导致PSNR下降超过2 dB；去除视角依赖的球谐密度或BA后的深度校正也会显著降低渲染质量，证明了每个模块的必要性。
- 在两视图和RayZer设定下，本文方法在SSIM和LPIPS上取得了最优结果，超越了所有需要已知相机姿态的方法，证明了少视图重建下特征对齐的有效性。
---

# Selfi: Self-improving Reconstruction Engine via 3D Geometric Feature Alignment

> [!tip] 核心洞察
> 利用三维基础模型的自输出作为密集的自监督信号，无需任何外部三维标注或相机真值，即可将基础模型的特征空间转化为几何对齐的特征空间，在此空间中特征相似度同时反映语义内容和三维空间邻近性，从而大幅提升无姿态新视角合成和位姿估计的性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | Selfi：基于三维几何特征对齐的自改进重建引擎 |
| 英文题名 | Selfi: Self-improving Reconstruction Engine via 3D Geometric Feature Alignment |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.08930) · [Project](https://denghilbert.github.io/selfi) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | Selfi |
| Dataset | DL3DV-10K Short, RealEstate10K Short, RealEstate10K Two-View, DL3DV-10K |

> [!tip] 效果简介
> - DL3DV-10K Short (6 frames) 上，PSNR ↑ 24.94 vs 21.76 (WorldMirror) (+3.18)。
> - RealEstate10K Short (6 frames) 上，PSNR ↑ 28.34 vs 25.54 (WorldMirror) (+2.80)。
> - RealEstate10K Two-View 上，PSNR ↑ 29.01 vs 26.82 (NoPoSplat) (+2.19)。

## 概要

从一组无姿态（unposed）的二维图像直接合成高质量的新视角，是三维视觉领域的一项核心挑战。现有的前馈式重建方法通常依赖已知的相机参数，或虽能处理无姿态输入，但其底层三维基础模型（如 **VGGT**，Wang et al., CVPR 2025）所提取的特征缺乏显式的多视图几何一致性——同一三维空间点在不同视图中的特征可能差异巨大，这严重限制了高保真新视角合成的质量。

本文提出 **Selfi**（Self-improving Reconstruction Engine），一种**自改进的三维重建引擎**。其核心思想是：利用冻结的三维基础模型自身的输出（深度图和相机参数）作为密集的自监督信号，训练一个轻量级的特征适配器，迫使不同视图中对应于同一三维位置的特征具有高度相似性，从而将基础模型的特征空间转化为**几何对齐的特征空间**。在此空间中，特征相似度同时反映语义内容和三维空间邻近性，为后续的高斯泼溅（3D Gaussian Splatting）渲染和位姿优化提供了坚实的基础。

Selfi 的完整流水线包含三个关键模块：
1. **几何特征对齐**：在冻结的 VGGT 骨干上附加 DPT 适配器，通过重投影一致性损失进行自监督训练，学习出几何对齐的密集特征。
2. **高斯参数预测**：基于对齐特征预测每像素的高斯基元参数，并引入**视角依赖的球谐密度**（spherical harmonics on opacity）作为置信度评分，有效抑制远离目标视角的输入帧带来的渲染错误。
3. **密集束调整与深度校正**：利用对齐特征进行帧间匹配并执行束调整（BA）以优化相机位姿，再通过从稀疏点估计的仿射变换对密集深度和高斯位置进行校正，实现渲染的无缝对齐。

实验结果表明，Selfi 在多个基准数据集上大幅超越了现有的无姿态新视角合成方法。在 DL3DV 和 RealEstate10K 的所有序列长度与重叠程度设置下，Selfi 在 PSNR/SSIM/LPIPS 上均显著优于 **AnySplat**（Jiang et al., ACM TOG 2025）、**WorldMirror**（Liu et al., arXiv 2025）和 **Flare**（Zhang et al., CVPR 2025）等基线，逼近甚至在某些设置下超过使用真值相机参数的 **3DGS**（Kerbl et al., ACM TOG 2023）上限。在两视图和 RayZer 设定下，Selfi 同样取得了最优的 SSIM 和 LPIPS 结果，超越了所有需要已知相机姿态的方法。消融实验进一步证实，移除几何特征对齐会导致 PSNR 下降超过 2 dB，验证了特征对齐对渲染质量的决定性影响。此外，对齐后的特征可直接用于高效的束调整，在大规模图像集上比 **CoTracker**（Karaev et al., ECCV 2024）更鲁棒，不会因内存不足而失败。

Selfi 的局限性主要体现在：VGGT 在天空、远距离区域的深度预测可能不准确；模型在动态场景上可能失效；训练需要大量计算资源（128 块 H100 GPU）。未来工作将聚焦于动态场景的特征匹配、更精细的深度预测，以及将自提升的特征对齐思想推广到其他三维基础模型和下游任务。

### 三维重建与无姿态新视角合成的技术瓶颈

新视角合成（Novel View Synthesis, NVS）是三维视觉的核心任务之一。以**3DGS**（Kerbl et al., ACM TOG 2023）为代表的逐场景优化方法虽能生成高保真渲染结果，却高度依赖精确的相机位姿参数和密集的输入视图，限制了其在非受控场景中的实用性。近年来，前馈式重建方法试图从稀疏图像直接预测三维表示，但多数方法（如**pixelNeRF**、**PixelSplat**、**MVSplat**、**GS-LRM**）仍假设相机参数已知，无法处理真实世界中常见的无姿态（unposed）图像输入。

面向无姿态设定的方法（如**AnySplat**、**WorldMirror**、**Flare**、**NoPoSplat**）开始涌现，它们通常借助三维视觉基础模型（如VGGT）来估计相机位姿和深度图，再基于这些预测构建三维场景表示。然而，这些方法面临一个根本性瓶颈：**现有三维视觉基础模型所提取的特征缺乏显式的多视图几何一致性**。具体而言，VGGT等模型虽然能输出合理的深度图和相机参数，但其内部特征空间中，对应于同一三维空间位置的不同视图像素特征并不具有足够的相似性。这种特征层面的几何不一致性严重限制了从无姿态图像进行高保真新视角合成的质量。

### 现有方法的缺口

当前无姿态NVS方法的核心缺口体现在三个层面：

1. **特征空间的几何失准**：VGGT等基础模型的特征是面向通用任务训练的，并未显式约束跨视图的几何一致性。直接将这些特征输入高斯解码器预测三维基元时，不同视图中对应同一物理点的特征差异会导致预测的高斯位置和外观不一致，进而产生模糊或错位的渲染结果。

2. **自监督信号的匮乏**：在无外部标注的条件下，如何获取可靠的跨视图对应关系作为训练监督是一个开放问题。传统方法依赖光流或特征匹配，但这些信号本身在无姿态设定下难以保证精度和密度。

3. **位姿估计与渲染的割裂**：多数方法将位姿估计和场景重建视为两个独立步骤，缺乏反馈机制。即使后续通过束调整（Bundle Adjustment）优化了相机位姿，初始预测的高斯几何也无法随之自适应调整，导致渲染出现明显错位。

### 本文动机与核心思路

针对上述瓶颈，Selfi提出了一种**自改进（self-improving）**的重建范式。其核心洞察在于：**利用三维基础模型的自输出作为密集的自监督信号，无需任何外部三维标注或相机真值，即可将基础模型的特征空间转化为几何对齐的特征空间**。在此对齐空间中，特征相似度同时反映语义内容和三维空间邻近性，从而大幅提升无姿态新视角合成和位姿估计的性能。

具体而言，Selfi冻结VGGT作为骨干网络，在其上附加一个轻量级的DPT特征适配器，通过重投影一致性损失进行自监督训练。该损失利用VGGT预测的深度图和相机参数作为伪真值，将源视图中的查询点重投影到目标视图，并约束两个视图中对应位置的特征具有高相似度。这一设计使得适配器学会输出几何对齐的特征表示，为后续的高斯预测和束调整提供了统一且鲁棒的基础。

在此基础上，Selfi进一步引入两个关键组件以提升渲染质量：（1）**视角依赖的球谐密度**，作为置信度评分抑制远离目标视角的输入帧中的错误高斯；（2）**束调整后的仿射深度校正**，将稀疏三维点的深度变化传播到所有密集高斯上，实现渲染的无缝对齐。整个流水线构成一个闭环的自改进系统：对齐特征 → 高斯预测 → 束调整优化位姿 → 深度校正更新几何 → 最终渲染，每一步的输出都为下一步提供了更优的初始条件。

## 核心方法与创新机理

### 问题瓶颈：三维基础模型特征缺乏多视图几何一致性

现有的三维视觉基础模型（如 **VGGT**，Wang et al., CVPR 2025）能够从无姿态图像中提取通用特征并预测深度图和相对相机参数，但这些特征并未显式地编码多视图几何一致性——即不同视图中对应于同一三维空间位置的像素，其特征向量在特征空间中并不一定相近。这种不一致性严重限制了从无姿态图像进行高保真新视角合成（NVS）的质量，因为下游的高斯预测器无法依赖特征相似度来判断不同视图中的像素是否源于同一表面点。

### 核心洞察：利用三维基础模型的自输出作为密集自监督信号

Selfi 的核心洞察在于：**三维基础模型自身输出的深度图和相机参数虽然不够精确，但足以构成密集的“伪真值”监督信号**。通过将这些自标注的伪真值用于特征对齐训练，可以在无需任何外部三维标注或相机真值的情况下，将基础模型的特征空间转化为一个**几何对齐的特征空间**。在该空间中，特征相似度同时反映语义内容和三维空间邻近性，从而大幅提升无姿态新视角合成和位姿估计的性能。

### 关键创新槽位（Changed Slots）

相较于直接使用 VGGT 原始特征进行高斯预测的基线方法（如 **AnySplat**，Jiang et al., ACM TOG 2025；**WorldMirror**，Liu et al., arXiv 2025），Selfi 在以下四个关键维度上进行了根本性改进：

#### 1. 特征表示与对齐策略：从原始特征到几何对齐特征

- **基线做法**：直接使用 VGGT 输出的原始图像令牌或特征图，未进行任何几何对齐训练。这些特征在跨视图对应点上缺乏相似性保证。
- **Selfi 创新**：在冻结的 VGGT 骨干网络上附加一个轻量级的 **DPT 特征适配器**，通过重投影一致性损失 $\mathcal{L}_{\mathrm{align}}$ 进行自监督训练。具体而言，利用 VGGT 预测的深度图和相机参数，将源视图中的查询像素反投影到三维空间，再变换并投影到目标视图，生成 2D-2D 伪真值对应点；训练目标是使预测对应点与伪真值对应点之间的 L2 距离最小化，从而迫使特征适配器学习出几何对齐的特征表示。
- **证据强度**：消融实验（Table 7）显示，移除几何特征对齐后 PSNR 从 24.88 骤降至 22.53（-2.35 dB），验证了该模块对渲染质量的决定性影响。

#### 2. 对应点预测方式：从对比学习到全局加权平均

- **基线做法**：CLIP 风格的对比学习目标仅鼓励正确匹配点的特征相似度高于错误匹配点，但在本任务中会导致特征坍塌为常量，所有查询点匹配到相同的目标点（Figure 8）。
- **Selfi 创新**：在目标图像的所有像素上计算余弦相似度，并通过温度参数 $\tau=100$ 的 softmax 转换为概率权重，最终以加权平均的方式预测对应点位置。这一策略提供了更密集、更鲁棒的监督信号，避免了特征坍塌问题。
- **证据强度**：Figure 8 直接展示了对比学习目标导致的匹配失败，而本文的全局加权平均策略成功恢复出准确的对应关系。

#### 3. 高斯密度建模：从静态不透明度到视角依赖的球谐密度

- **基线做法**：标准 3DGS 使用单一的标量不透明度，与观察视角无关。
- **Selfi 创新**：引入**视角依赖的球谐密度（spherical harmonics on opacity）**，作为每个高斯基元的置信度评分。对于远离目标新视角的输入帧，其预测的高斯会被赋予接近零的密度，从而有效抑制因视角差异过大而产生的错误渲染。这一设计使得模型能够自动“信任”更接近目标视角的源视图。
- **证据强度**：消融实验（Table 7）和 Figure 6 的可视化证实，移除视角依赖密度后渲染质量明显下降，尤其是在处理遮挡和远距离区域时。

#### 4. BA 后的几何校正：从直接渲染到仿射深度校正

- **基线做法**：束调整（BA）优化相机位姿后，直接使用新位姿渲染原始高斯，导致渲染结果与图像内容出现明显错位（Figure 4a）。
- **Selfi 创新**：利用 BA 过程中稀疏三维点的深度变化估计一个仿射变换 $\phi$，将该变换传播到所有密集预测的高斯深度和位置上，并对高斯尺度进行相应的缩放调整。这一操作实现了 BA 后渲染的无缝对齐，使得位姿优化的收益能够无损地转化为渲染质量的提升。
- **证据强度**：Table 7 显示移除深度校正后 PSNR 下降；Figure 4 直观对比了有无深度校正的渲染差异，并展示了稀疏点深度的线性拟合关系。

### 创新总结

Selfi 的四项创新构成了一个完整的**自改进重建引擎**：几何特征对齐为所有下游任务提供了高质量的特征基础；全局加权平均确保了特征学习的稳定性；视角依赖密度增强了多视图融合的鲁棒性；BA 后的深度校正则打通了位姿优化到渲染提升的“最后一公里”。这些创新协同作用，使得 Selfi 在无姿态新视角合成任务上大幅超越现有前馈方法，逼近甚至在某些设置下超越使用真值相机参数的 3DGS 上限。

Selfi 是一个**自改进的三维重建引擎**，其核心设计理念是：利用冻结的三维基础模型（VGGT）的自输出作为密集的自监督信号，将基础模型的特征空间转化为几何对齐的特征空间，并在此基础上预测三维高斯基元，最终通过束调整（BA）和深度校正实现渲染质量的二次提升。整个 pipeline 由三个关键阶段串联而成，形成“特征对齐 → 高斯预测 → 自改进优化”的闭环。

### Pipeline 总览

如 Figure 1 所示，Selfi 的输入为一组**无姿态的稀疏多视图图像**，输出为目标新视角的渲染图像。整体流程可概括为以下步骤：

![[assets/figures/papers/paper_list_l2094_https_arxiv_org_abs_2512_08930/figures/001_Figure_1.jpg]]
*Figure 1: Self Improving Reconstruction Engine. We introduce Selfi, a self-improving pipeline for novel view synthesis from unposed images. We start by learning geometrically aligned features using consistency losses and self-labelled pseudo ground truths from a 3D foundation model (e.g., VGGT [54]). These features can be used to predict Gaussian primitives [23], and also refine initial poses via bundle adjustment. The improved poses are used to further adjust the initial 3D representation, resulting in an even higher quality final rendering*

1. **初始几何估计**：将输入图像送入冻结的 VGGT 骨干网络，获得图像令牌（image tokens）、逐像素深度图、相机内参和帧间相对位姿。这些输出作为后续所有模块的初始化信号和伪真值监督源。
2. **几何特征对齐**：在 VGGT 图像令牌之上附加一个轻量级的 DPT 特征适配器，通过重投影一致性损失训练该适配器，迫使不同视图中对应于同一三维空间位置的像素特征具有高相似度。此阶段产出的几何对齐特征图是后续高斯预测和特征匹配的基础。
3. **高斯参数预测与渲染**：将对齐特征与原始输入图像拼接后送入 U-Net 解码器，预测每个像素对应的高斯参数（包括位置残差、四元数旋转、尺度、球谐颜色以及视角依赖的球谐密度）。根据 VGGT 预测的相对位姿，将所有源视图的高斯基元栅格化到目标新视点，得到初始渲染图像。
4. **自改进优化（可选）**：利用对齐特征进行帧间密集匹配，执行束调整（BA）以精化相机位姿。BA 后，通过从稀疏三维点深度变化估计的仿射变换，对密集预测的高斯深度和位置进行校正，使高斯几何与更新后的位姿保持一致，从而获得更高质量的最终渲染。

### 模块关系与数据流

三个核心模块之间的依赖关系和数据流如下：

- **VGGT 骨干（冻结）** → 提供图像令牌 $`\mathbf{T}_i`$、深度图 $`\mathbf{D}_i`$、相机内参 $`\mathbf{K}`$ 和相对位姿 $`(\mathbf{R}, \mathbf{t})`$。该模块在整个训练过程中保持冻结，不参与梯度更新。
- **DPT 特征适配器** → 接收图像令牌 $`\mathbf{T}_i`$，输出 $C=24$ 维的像素对齐特征图 $`\mathbf{F}_i`$。其训练完全依赖 VGGT 预测的深度和相机参数构建的重投影伪真值，无需任何外部标注。
- **U-Net 高斯解码器** → 接收对齐特征 $`\mathbf{F}_s`$ 和源图像 $`I_s`$ 的拼接，输出解码特征 $`\mathbf{F}_s^{\text{dec}}`$，进而通过多个预测头分别输出高斯的位置残差 $`\Delta\mathbf{D}_s`$、旋转四元数、尺度、球谐系数和视角依赖密度。
- **束调整与深度校正模块** → 利用对齐特征进行帧间匹配，构造 BA 优化问题；BA 收敛后，从稀疏匹配点的深度变化拟合仿射变换 $`\phi`$，将其传播到所有密集高斯位置和尺度上，实现无缝的几何一致性。

### 关键设计决策

Selfi 的 pipeline 设计体现了三个核心洞察：

1. **自监督特征对齐替代外部标注**：传统方法依赖 COLMAP 等外部工具获取相机真值和稀疏对应点，而 Selfi 直接复用 VGGT 的自输出（深度图和相机参数）作为伪真值，通过重投影构建密集的 2D-2D 对应监督信号。这使得整个 pipeline 完全摆脱了对任何外部三维标注或相机真值的依赖。

2. **视角依赖密度作为置信度机制**：不同于标准 3DGS 的单一标量不透明度，Selfi 为每个高斯预测视角依赖的球谐密度。该密度隐式地学习为一种“置信度评分”——当某个输入帧的拍摄视角远离目标渲染视角时，从该帧预测的高斯密度趋近于零，从而自动抑制遮挡和远距离区域引入的错误几何。Figure 6 的可视化清晰地展示了这一机制的效果。

3. **BA 后的仿射深度校正**：束调整仅优化了稀疏匹配点的三维位置和相机位姿，若直接用新位姿渲染原始高斯，会产生明显的几何错位（Figure 4a）。Selfi 通过从稀疏点深度变化估计一个全局仿射变换，将其应用于所有密集预测的高斯深度（Figure 4b），以极小的计算代价实现了 BA 后渲染的无缝对齐。实验表明该仿射拟合已足够（Figure 4c），无需更复杂的逐像素校正。

### 训练策略

训练分为两个独立阶段：
- **阶段一（特征对齐）**：采样 11 帧序列，以中间帧为源视图、其余帧为目标视图，使用重投影一致性损失 $`\mathcal{L}_{\text{align}}`$ 训练 DPT 适配器。峰值学习率为 $1 \times 10^{-4}$，在 128 块 H100 GPU 上约需 2 天。
- **阶段二（高斯预测器）**：混合 DL3DV 和 RealEstate10K 数据集，采样 6 个源帧和 5 个插值目标帧，使用 L1 渲染损失 $`\mathcal{L}_{\text{RGB}}`$ 训练 U-Net 解码器。学习率为 $2 \times 10^{-4}$，在 128 块 H100 GPU 上约需 1.5 天。

两个阶段均使用 VGGT 的冻结权重，确保基础模型的通用三维先验不被破坏，仅通过轻量级适配器实现任务特定的特征转化。

### 3.1 几何特征对齐

Selfi的核心创新在于将冻结的VGGT基础模型的特征空间转化为几何对齐的特征空间。整体流程由三个关键子模块构成：DPT特征适配器、伪真值重投影、以及重投影一致性损失。

**DPT特征适配器**。在预训练的VGGT骨干网络之上，附加一个轻量级的DPT空间特征适配器，将VGGT输出的图像令牌转化为像素对齐的几何特征图：

$$\mathbf{F}_i = \mathrm{DPT}_{\mathrm{adapter}}(\mathbf{T}_i)$$

其中 $\mathbf{T}_i$ 为VGGT对第 $i$ 帧输出的图像令牌，$\mathbf{F}_i$ 为适配器输出的 $C=24$ 维特征图。训练期间VGGT骨干完全冻结，仅更新DPT适配器参数。

**伪真值重投影**。对齐训练所需的监督信号完全来自VGGT自身的输出，无需任何外部标注。具体而言，利用VGGT预测的深度图 $\mathbf{D}$、相机内参 $\mathbf{K}$ 及帧间相对位姿 $(\mathbf{R}_{ts}, \mathbf{t}_{ts})$，将源视图中的查询像素 $\mathbf{p}_s^n$ 反投影到三维空间，再变换至目标视图坐标系，最后投影回二维像素平面：

$$\mathbf{P}_t^n = \mathbf{R}_{ts} \mathbf{D}_s^n \pi_{\mathbf{K}}^{-1} \mathbf{p}_s^n + \mathbf{t}_{ts}$$

$$\mathbf{p}_t^n = \pi_{\mathbf{K}} \mathbf{P}_t^n$$

由此获得源视图与目标视图之间的2D-2D伪真值对应点。为过滤被遮挡的点，引入可见性掩码：

$$\mathbf{V}_t^n = \left[ \left| \mathbf{P}_t^n \cdot [0\ 0\ 1]^T - \mathbf{D}_t^n \right| < \alpha \right]$$

其中 $\alpha=0.05$ 为深度一致性阈值：若重投影点的深度与目标视图深度图的差异超过阈值，则认为该点被遮挡，不参与损失计算。

**对应点预测与对齐损失**。区别于标准对比学习仅鼓励正确匹配点特征相似的做法（实验表明该策略会导致特征坍塌为常量，所有查询点匹配至同一目标点），Selfi采用全局加权平均策略预测对应点位置。首先计算源视图查询点 $n$ 的特征 $\mathbf{F}_s^n$ 与目标视图所有位置 $(u,v)$ 的特征之间的余弦相似度：

$$S^n(u,v) = \frac{\mathbf{F}_s^n \cdot \mathbf{F}_t(u,v)}{\|\mathbf{F}_s^n\|_2 \|\mathbf{F}_t(u,v)\|_2}$$

再通过带温度参数 $\tau=100$ 的softmax将相似度转化为概率权重：

$$w^n(u,v) = \frac{\exp(S^n(u,v)/\tau)}{\sum_{u',v'}\exp(S^n(u',v')/\tau)}$$

最终以加权平均得到预测的2D对应点：

$$\hat{\mathbf{p}}_t^n = \sum_{u,v} w^n(u,v) [u,v]$$

这一策略提供了更密集、更鲁棒的监督信号。对齐损失定义为预测对应点与伪真值之间的L2距离，由可见性掩码加权：

$$\mathcal{L}_{\mathrm{align}} = \frac{1}{TN} \sum_{t=1}^T \sum_{n=1}^N \mathbf{V}_t^n \big\| \hat{\mathbf{p}}_t^n - \mathbf{p}_t^n \big\|_2^2$$

其中 $T$ 为目标视图数量，$N$ 为每个源视图的查询点数量。该损失迫使特征空间中对应同一三维点的像素特征具有高相似度，从而学习出几何对齐的表示。

### 3.2 高斯参数预测

获得几何对齐特征后，Selfi通过U-Net解码器预测每个像素对应的高斯基元参数。解码器接收对齐特征 $\mathbf{F}_s$ 与源图像 $I_s$ 的拼接作为输入，输出解码特征 $\mathbf{F}_s^{\mathrm{dec}}$。

**高斯位置**。以VGGT预测的深度图 $\mathbf{D}_s$ 为基础，加上U-Net预测的深度残差 $\Delta\mathbf{D}_s$，反投影得到每个高斯的中心位置：

$$\pmb{\mu}_s = (\mathbf{D}_s + \Delta\mathbf{D}_s) \pi_{\mathbf{K}}^{-1} \mathbf{p}_s$$

此外，解码器还预测每个高斯的旋转四元数、各向异性尺度、球谐颜色系数。

**视角依赖的球谐密度**。区别于标准3DGS的单一标量不透明度，Selfi引入视角依赖的球谐密度（spherical harmonics on opacity）。该密度作为置信度评分：对远离目标渲染视角的输入帧，其高斯密度趋近于零，从而有效抑制因深度预测误差或遮挡导致的错误高斯贡献。消融实验表明，移除该模块会导致渲染质量明显下降。

**渲染与RGB损失**。将所有源视图的高斯基元根据VGGT预测的相对位姿栅格化至目标新视点，得到渲染图像 $\hat{I}_t$。高斯预测器的训练目标为L1重建损失：

$$\mathcal{L}_{\mathrm{RGB}} = \frac{1}{T} \sum_{t=1}^T \big\lVert \hat{I}_t - I_t \big\rVert_1$$

### 3.3 束调整与深度校正

对齐后的特征可直接用于帧间稠密匹配，进而执行束调整（BA）优化相机位姿。然而，BA更新位姿后，若直接使用原高斯位置渲染，会出现明显的几何错位。Selfi的解决方案是：利用BA过程中稀疏三维点的深度变化，估计一个仿射变换 $\phi$，将其传播至所有密集预测的高斯深度：

$$\pmb{\mu}_s' = \phi(\mathbf{D}_s + \Delta\mathbf{D}_s) \pi_{\mathbf{K}'}^{-1} \mathbf{p}_s$$

其中 $\mathbf{K}'$ 为BA后更新的内参。同时，按深度缩放比例调整高斯尺度以保持渲染一致性：

$$\mathbf{s}_s' = \frac{\phi(\mathbf{D}_s + \Delta\mathbf{D}_s)}{\mathbf{D}_s + \Delta\mathbf{D}_s} \cdot \mathbf{s}_s$$

实验表明，该仿射深度校正操作对于BA后渲染质量至关重要：移除该步骤会导致PSNR显著下降，渲染结果出现明显错位。

## 实验与关键发现

### 核心实验设计

实验围绕三个递进维度展开，验证几何特征对齐在无姿态新视角合成中的因果作用。第一层评估前馈式无姿态NVS质量（Table 1–4），第二层验证对齐特征对位姿估计的增强能力（Table 5–6），第三层通过消融实验确认每个模块的必要性（Table 7）。

![[assets/figures/papers/paper_list_l2094_https_arxiv_org_abs_2512_08930/figures/005_Table_1.jpg]]
*Table 1: Novel View Synthesis with Varying Sequence Length. We compare our method against several baselines on the RealEstate10K [79] and DL3DV [27] datasets. As the number of input frames increases, the performance of all feed-forward methods degrades, as it becomes more challenging to predict consistent 3D Gaussians from a greater number of views. In contrast, 3DGS [23] with GT camera parameters, which we include as an upper bound, improves with more views as it can better optimize for consistency*

![[assets/figures/papers/paper_list_l2094_https_arxiv_org_abs_2512_08930/figures/010_Table_5.jpg]]
*Table 5: BA for Joint Pose Estimation and NVS. Using the aligned features, we refine the camera poses using BA and further adjust the predicted Gaussian positions to be consistent with the BA output. This self-refinement operation yields further improvements over the initial NVS without BA, which we demonstrate on DL3DV and apply zero-shot to MipNeRF360 and Tanks&Temples*

![[assets/figures/papers/paper_list_l2094_https_arxiv_org_abs_2512_08930/figures/012_Table_7.jpg]]
*Table 7: Ablation Studies on DL3DV [27]. We quantify the benefits of geometric feature alignment, SH prediction, and depth correction after BA. For ablations, we use a smaller batch size of 32 for training and 6 inputs with a stride of 2 for evaluation*

**训练与评估配置**：几何特征对齐阶段采样11帧（中间帧为源视图，其余为目标视图），在128块H100 GPU上训练约2天，峰值学习率 $1 \times 10^{-4}$。高斯预测器（U-Net解码器）联合DL3DV与RealEstate10K训练，采样6源帧加5目标帧，学习率 $2 \times 10^{-4}$，训练约1.5天。多视图评估使用294×518分辨率，两视图评估统一为256×256。消融实验使用较小批大小（32）以确保公平对比。

### 主实验结果

**多视图无姿态NVS**：Table 1展示了不同序列长度下的对比。在DL3DV Short（6帧）设定下，Selfi取得PSNR 24.94 / SSIM 0.8442 / LPIPS 0.1566，较最强基线**WorldMirror**（Liu et al., arXiv 2025）的PSNR 21.76提升 **+3.18 dB**；在RealEstate10K Short下达到PSNR 28.34，领先WorldMirror **+2.80 dB**。值得注意的是，随着输入帧数增加，所有前馈方法性能均下降（因多视图一致性预测难度增大），但Selfi始终显著优于**AnySplat**（Jiang et al., ACM TOG 2025）和**Flare**（Zhang et al., CVPR 2025）等无姿态基线，并在某些设置下逼近甚至超过使用真值相机参数的**3DGS**上限（Kerbl et al., ACM TOG 2023）。

Table 2进一步考察视图重叠程度的影响：采样步长越小（重叠越高），所有方法性能均提升，Selfi在所有重叠设置下均最优，在DL3DV上平均PSNR 22.30，RealEstate10K上平均PSNR 24.47。

**两视图设定**：Table 3遵循**PixelSplat**（Charatan et al., CVPR 2024）的两视图惯例评估。Selfi取得PSNR 29.01 / SSIM 0.942 / LPIPS 0.053，超越所有无姿态方法，且在SSIM和LPIPS上优于多数需要已知相机姿态的方法（如**pixelNeRF**、**MVSplat**、**GS-LRM**），证明几何对齐特征在极稀疏视图下的强健性。Table 4的RayZer设定（16输入/8目标）中，Selfi在SSIM和LPIPS上超过RayZer，且场景表示可直接栅格化渲染，无需额外网络传递。

**位姿估计与自改进**：Table 5验证了利用对齐特征进行束调整（BA）后的自改进效果。在DL3DV上，BA将PSNR从24.88提升至25.13（+0.25 dB），且该改进零样本泛化至MipNeRF360和Tanks&Temples。Table 6的位姿估计评估显示，在40帧输入下，Selfi的AUC@30°达0.9846，优于VGGT直接预测（0.9716）和**CoTracker**（Karaev et al., ECCV 2024）；关键的是，当图像数量超过40张时CoTracker因内存不足而失败，而Selfi的特征匹配方法保持鲁棒。

### 消融实验

Table 7的消融结果揭示了三个关键模块的因果效应：

1. **几何特征对齐**：移除特征对齐（w/o feature alignment）导致PSNR从24.88骤降至22.53（**-2.35 dB**），这是所有消融项中降幅最大的，直接证明了特征对齐是渲染质量的决定性因素。
2. **视角依赖球谐密度**：移除SH密度（w/o SH density）同样造成明显下降。Figure 6可视化展示了其机制——该模块作为置信度评分，对远离目标视角的输入帧的高斯赋予接近零的密度，有效抑制了遮挡和远距离区域的错误渲染。
3. **BA后深度校正**：移除深度偏移校正（w/o depth shift）使BA后渲染出现明显错位（见Figure 4(a)）。该模块通过从BA稀疏点深度变化估计仿射变换，传播至所有密集高斯位置（Figure 4(c)显示线性拟合足够），实现无缝的渲染对齐。

此外，Figure 8揭示了对比学习策略的失败模式：CLIP风格的对比目标导致特征坍塌为常量，所有查询点匹配到同一目标点；本文的全局加权平均策略通过在所有目标像素上计算相似度加权平均，提供了更密集的监督信号，避免了此问题。

### 失败模式与局限性

1. **深度预测失效**：VGGT在天空、远距离区域等场景下深度预测不准确（因其训练使用归一化尺度），导致重投影伪真值质量下降。视角依赖密度可部分缓解，但根本问题依然存在。
2. **曝光不一致**：输入图像与目标图像之间的曝光差异可能影响渲染指标，因为Selfi会模仿输入图像的曝光，与未对齐曝光的目标图像产生色彩差异。
3. **动态场景失效**：VGGT和特征对齐均在静态场景上训练，动态区域可能被错误匹配到被遮挡的静态背景部分。
4. **计算资源需求大**：需要128块H100 GPU，特征对齐约2天，高斯预测器约1.5天。

### 关键图表结论速览

- **Table 1**：Selfi在所有序列长度下大幅领先无姿态基线，逼近3DGS上限。
- **Table 3**：两视图设定下超越多数需要已知相机的方法，验证极稀疏视图下的有效性。
- **Table 5–6**：对齐特征使BA有效提升位姿精度和NVS质量，且比CoTracker更可扩展。
- **Table 7**：几何特征对齐是最大贡献因子（-2.35 dB），SH密度和深度校正各自贡献显著。
- **Figure 4**：BA后深度校正是渲染对齐的必要条件。
- **Figure 6**：视角依赖密度通过置信度机制抑制远距离输入帧的干扰。
- **Figure 8**：对比学习导致特征坍塌，全局加权平均策略是关键设计选择。

![[assets/figures/papers/paper_list_l2094_https_arxiv_org_abs_2512_08930/figures/008_Table_3.jpg]]
*Table 3: Quantitative Comparison with the Two-View Convention. We follow the two-view convention previously used by PixelSplat [5] on RealEstate10K [79]. Except for Flare [77], No-PoSplat [70], and our method, all other methods require calibrated images as input. Our method remains competitive even against those that require ground-truth camera parameters*

![[assets/figures/papers/paper_list_l2094_https_arxiv_org_abs_2512_08930/figures/013_Figure_6.jpg]]
*Figure 6: View-dependent Density. Given six input views (top row), we render the Gaussians from each individual input to a target camera at the midpoint of the two center views. This process is shown for models trained without (middle row) and with (bottom row) view-dependent density. The view-dependent density serves as a confidence score that learns to downweight input views that are farther from the target view*

## 定位与知识库关联

### 无姿态新视角合成的方法谱系

Selfi 处于**无姿态前馈三维重建与新视角合成**这一快速发展的研究线路上。传统的前馈方法（如 pixelNeRF、PixelSplat、MVSplat、GS-LRM）均需要已知的相机参数作为输入，这在实际应用中构成了显著限制。近年来，一系列工作开始探索从无姿态图像直接进行三维重建：

- **NoPoSplat**（Ye et al., ICLR 2025）是早期尝试从稀疏无姿态图像进行三维高斯泼溅的方法之一，但在两视图设定下，Selfi 在 PSNR 上领先其 2.19 dB（29.01 vs 26.82, Table 3）。
- **AnySplat**（Jiang et al., ACM TOG 2025）和 **WorldMirror**（Liu et al., arXiv 2025）均直接基于 VGGT 的原始特征进行高斯解码，但缺乏显式的几何特征对齐。Selfi 在 DL3DV Short 设定下相比 WorldMirror 提升 3.18 dB PSNR（24.94 vs 21.76, Table 1）。
- **Flare**（Zhang et al., CVPR 2025）联合估计几何、外观和相机参数，是同期较有竞争力的无姿态方法，但 Selfi 在所有序列长度和重叠程度设定下均保持显著优势。

### 与基于 VGGT 的方法的关系

Selfi 的核心创新在于**将 VGGT 从直接的特征提供者转变为自监督信号源**。与 AnySplat 和 WorldMirror 直接使用 VGGT 原始特征不同，Selfi 冻结 VGGT 骨干，在其上附加轻量级 DPT 适配器，利用 VGGT 预测的深度图和相机参数作为伪真值，通过重投影一致性损失训练出几何对齐的特征。这一策略的本质区别在于：

| 方法 | 特征来源 | 几何对齐 | 监督信号 |
|------|---------|---------|---------|
| AnySplat / WorldMirror | VGGT 原始特征 | 无 | 仅 RGB 重建损失 |
| **Selfi** | VGGT + DPT 适配器 | **有（重投影一致性）** | RGB 损失 + 对齐损失 |

消融实验（Table 7）证实，移除几何特征对齐导致 PSNR 从 24.88 骤降至 22.53（-2.35 dB），验证了这一设计决策的决定性作用。

### 与逐场景优化方法的对比

**3DGS**（Kerbl et al., ACM TOG 2023）使用真值相机参数进行逐场景优化，通常被视为性能上限。Selfi 作为前馈方法，在无需任何测试时优化的前提下，在多个设定下逼近甚至达到 3DGS 的性能水平（Table 2），这标志着前馈方法与优化式方法之间差距的实质性缩小。

### 知识库定位：自监督几何特征学习

从更广泛的视角看，Selfi 提出了一种**利用三维基础模型的自输出作为密集自监督信号**的范式。这一思路与以下方向形成对话：

- **自监督深度估计**：传统方法依赖光度一致性，Selfi 则利用冻结模型的深度预测作为伪真值，避免了光度一致性的局部最优问题。
- **特征匹配与束调整**：Selfi 的对齐特征可直接用于帧间匹配和束调整，在 DL3DV 40 帧设定下 AUC@30° 达到 0.9846，优于 VGGT 直接预测（0.9716）和 CoTracker（Karaev et al., ECCV 2024），且在处理大规模图像集时不会因内存不足而失败（Table 6）。

### 适用边界与局限

1. **深度预测质量依赖**：VGGT 在天空、远距离区域等深度预测可能不准确，因为其训练使用了归一化尺度，导致极大的深度差异无法表示。尽管视角依赖的球谐密度可在一定程度上缓解此问题，但根本限制依然存在。

2. **曝光不一致敏感**：输入图像与目标图像之间的曝光差异可能影响渲染指标，因为 Selfi 会模仿输入图像的曝光，导致与未对齐曝光的目标图像产生色彩差异。

3. **动态场景失效**：VGGT 和特征对齐均在静态场景上训练，动态区域可能被错误匹配到被遮挡的静态背景部分。改进动态场景的特征匹配是明确的未来方向。

4. **计算资源需求高**：训练需要 128 块 H100 GPU，特征对齐阶段约 2 天，高斯预测器约 1.5 天，限制了快速复现和轻量化部署的可能性。

### 开放问题

- 如何将这种自提升的特征对齐思想推广到其他三维基础模型和下游任务（如三维分割、目标检测）？
- 能否通过更精细的深度预测或自适应曝光校正来进一步缩小与逐场景优化式方法的差距？
- 本方法对室外大规模场景（如城市级重建）的适应性和效率如何？
- 动态场景下的特征匹配和重建性能提升是否可以通过引入时序建模或运动分割来实现？

## 原文 PDF

![[paperPDFs/CVPR_2026/Selfi_Self_improving_Reconstruction_Engine_via_3D_Geometric_Feature_Alignment.pdf]]
