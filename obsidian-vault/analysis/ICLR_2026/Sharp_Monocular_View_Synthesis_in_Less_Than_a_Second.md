---
title: Sharp Monocular View Synthesis in Less Than a Second
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Sharp_Monocular_View_Synthesis_in_Less_Than_a_Second_9ff8519e0fec.pdf
project_link: "https://apple.github.io/ml-sharp"
code_link: "https://github.com/OpenDriveLab/OpenScene"
aliases:
- SMVSLTS
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmarking
core_operator: 通过一个受条件VAE启发的深度调整模块，利用真实深度信息学习一个尺度图来校准预测深度；同时解冻深度编码器进行端到端优化，使深度表示适应视角合成任务。
primary_logic: 将单目深度估计的不确定性建模为可学习的尺度调整，并与图像空间损失（颜色、感知、Gram矩阵）联合优化，迫使网络学习对视角合成最优的深度表示，而非单纯追求深度数值准确。
claims:
- 深度调整模块在ScanNet++和Tanks and Temples上一致提升了DISTS/LPIPS，证明了消除深度歧义对视角合成质量的重要性。
- 解冻单目深度骨干网络显著改善了定量指标和定性结果（边界伪影、反射等）。
- Multiple datasets (Middlebury, Booster, ScanNet++, WildRGBD, Tanks and Temples,... 上 LPIPS = varied per dataset (e.g., Middlebury 0.358, ScanNet++ 0.154)
- Multiple datasets 上 DISTS = varied (e.g., Middlebury 0.097, ScanNet++ 0.071)
---

# Sharp Monocular View Synthesis in Less Than a Second

> [!tip] 核心洞察
> 将单目深度估计的不确定性建模为可学习的尺度调整，并与图像空间损失（颜色、感知、Gram矩阵）联合优化，迫使网络学习对视角合成最优的深度表示，而非单纯追求深度数值准确。

| 字段 | 内容 |
|------|------|
| 中文题名 | 亚秒级单目图像清晰视角合成 |
| 英文题名 | Sharp Monocular View Synthesis in Less Than a Second |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=yx3g4sF70y) · [Project](https://apple.github.io/ml-sharp) · [Code](https://github.com/OpenDriveLab/OpenScene) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmarking |
| Method | SHARP |
| Dataset | Multiple datasets |

> [!tip] 效果简介
> - Multiple datasets (Middlebury, Booster, ScanNet++, WildRGBD, Tanks and Temples,... 上，LPIPS varied per dataset (e.g., Middlebury 0.358, ScanNet++ 0.154) vs Best prior model (Gen3C) (reduction of 25–34%)。
> - Multiple datasets 上，DISTS varied (e.g., Middlebury 0.097, ScanNet++ 0.071) vs Best prior model (Gen3C) (reduction of 21–43%)。

## 概要

从单张二维图像合成新视角下的三维场景是计算机视觉与图形学中长期存在的挑战。该问题的核心瓶颈在于**单目深度估计的固有歧义**——透明/反射表面、弱纹理区域等情形会导致初始化深度不准确，进而在新视角合成时产生几何伪影和模糊。现有方法要么依赖耗时的扩散模型，要么受限于前馈模型的保真度不足，难以同时满足高质量和实时性需求。

SHARP 针对这一问题提出了一个端到端的前馈网络，从单张照片回归出高分辨率的 3D Gaussian 表示。其核心洞察在于：将单目深度估计的不确定性建模为可学习的尺度调整，并与图像空间损失（颜色、感知、Gram 矩阵）联合优化，迫使网络学习对视角合成最优的深度表示，而非单纯追求深度数值准确。

具体而言，SHARP 通过三个关键设计实现突破：(1) 一个受条件 VAE 启发的深度调整模块，利用真实深度信息学习尺度图来校准预测深度；(2) 解冻深度编码器进行端到端优化，使深度表示适应视角合成任务；(3) 精心配置的损失函数组合，包括感知损失和 Gram 矩阵损失，以提升图像清晰度和细节保真度。

在六个数据集上的实验表明，SHARP 相比此前最优的扩散模型 **Gen3C** (Ren et al., 2025)，将 LPIPS 降低了 25–34%，DISTS 降低了 21–43%，同时合成时间不到一秒，渲染速度超过每秒 100 帧，在效率与保真度之间建立了新的权衡前沿。



单目视角合成（Novel View Synthesis, NVS）旨在从单张输入图像生成场景在新相机姿态下的逼真渲染图。这一任务在增强现实、虚拟现实、3D内容创作等领域具有广泛应用前景，但其核心挑战在于从单一2D观测中恢复完整的3D场景表示——这是一个本质上欠约束的逆问题。

### 现有方法及其局限

当前单目视角合成方法大致可分为三类：

**基于扩散模型的方法**（如 **Stable Virtual Camera** (Zhou et al., 2025)、**ViewCrafter** (Yu et al., 2025b)、**Gen3C** (Ren et al., 2025)）利用大规模预训练扩散模型的生成先验来“想象”新视角的内容。这类方法在较大相机运动范围下能产生视觉上合理的输出，但存在两个根本性缺陷：（1）推理速度极慢，通常需要数十秒甚至数分钟才能生成单帧；（2）生成的几何一致性难以保证，在需要精确3D结构的应用中容易产生闪烁和形变。

**基于前馈3D表示的方法**（如 **Flash3D** (Szymanowicz et al., 2025a)）直接从单张图像回归3D高斯参数，推理速度极快（毫秒级），但渲染质量受限于所预测几何的精度。这些方法通常依赖冻结的单目深度估计器提供初始几何，而单目深度估计本身存在固有的尺度歧义和局部误差，导致新视角渲染时产生模糊和几何伪影。

**基于分层图像表示的方法**（如 **TMPI** (Khan et al., 2023)、**LVSM** (Jin et al., 2025)）将场景表示为多层图像平面，通过图像到图像的回归生成新视角。这类方法在速度和质量之间取得了一定平衡，但在处理遮挡区域和视角依赖效果时表现有限。

### 核心瓶颈：单目深度估计的固有歧义

上述方法的共同瓶颈在于单目深度估计的不确定性。如图5所示，对同一张图像进行水平翻转后再预测深度并翻转回来，得到的深度图与原始预测之间存在显著差异——这种不一致性在透明/反射表面、纹理弱区域、重复纹理等区域尤为突出。当这些不准确的深度估计被用于构建3D表示时，新视角渲染不可避免地产生几何伪影、边界模糊和结构扭曲。

更关键的是，即使深度估计在数值上接近真实深度，它也不一定对视角合成任务最优——因为视角合成需要的是能够正确重投影纹理的深度，而非像素级的深度精度。现有方法将深度估计和视角合成解耦处理，使得深度网络无法根据渲染反馈调整其预测。

### 本文动机

本文的核心动机是弥合“快速前馈推理”与“高保真渲染”之间的鸿沟。具体而言，我们希望回答以下问题：

1. **能否将单目深度估计的不确定性建模为可学习的调整机制**，使其在训练过程中根据视角合成损失自适应校准，而非单纯追求深度数值准确？
2. **能否设计一个端到端可训练的前馈网络**，在亚秒级时间内从单张图像直接回归高质量的3D高斯表示，同时保持渲染速度超过100 FPS？
3. **如何配置损失函数**，使其既能有效约束3D几何（抑制浮点、退化高斯等伪影），又能通过感知损失鼓励清晰的纹理修复？

通过解决这些问题，SHARP旨在实现一个在速度-质量帕累托前沿上显著超越现有方法的单目视角合成系统（见图1）。



## 核心方法与创新机理

SHARP的核心创新在于将单目视角合成问题重新定义为“深度歧义感知的3D高斯回归”，通过三个关键机制解决了现有方法的根本瓶颈。

### 深度歧义的显式建模与校准

单目深度估计存在固有歧义——透明表面、反射区域和弱纹理区域会导致深度预测不可靠，进而引发新视角合成中的几何伪影和模糊。SHARP通过一个受条件VAE启发的**深度调整模块**来解决这一问题：训练时，一个小型U-Net接收预测逆深度和真实逆深度，输出一张尺度图$\mathbf{S}$来校准深度；推理时，该模块被替换为恒等映射，无需真实深度即可运行。消融实验表明，该模块在ScanNet++和Tanks and Temples数据集上一致提升了DISTS和LPIPS指标（Table 11, Figure 10），验证了显式处理深度不确定性对视角合成质量的关键作用。

### 双层深度表示

与仅预测单层深度图的方法不同，SHARP输出**两层深度通道**：第一层对应可见表面，第二层负责遮挡区域和视角依赖效果。这一设计使3D高斯表示能够更完整地刻画场景几何，尤其是处理遮挡边界处的信息缺失。

### 端到端可训练的深度骨干

传统方法通常冻结预训练的单目深度编码器，导致深度表示无法适应视角合成任务的需求。SHARP**解冻了深度编码器的低分辨率部分**，使其通过视角合成损失进行端到端优化。这一改变显著改善了边界伪影和反射区域的渲染质量，定量指标也有明显提升（Table 13, Figure 12）。核心洞察在于：视角合成所需的“最优深度”并不等同于几何意义上的“准确深度”——网络需要学习的是对渲染质量最有利的深度表示。

### 感知驱动的损失配置

SHARP引入了精心调校的**感知损失**，结合VGG特征损失和Gram矩阵损失，在新视图上施加约束：

$$\mathcal{L}_{\mathrm{percep}} = \sum_{l=1}^{4} \lambda_{l}^{\mathrm{feat}} \cdot \big\| \phi_{l}(\widehat{\mathbf{I}}_{\mathrm{novel}}) - \phi_{l}(\mathbf{I}_{\mathrm{novel}}) \big\|^2 + \lambda_{l}^{\mathrm{Gram}} \cdot \big\| M_{l}(\widehat{\mathbf{I}}_{\mathrm{novel}}) - M_{l}(\mathbf{I}_{\mathrm{novel}}) \big\|^2$$

其中Gram矩阵损失对提升图像清晰度贡献尤为显著（Table 10）。此外，多个正则化项（总变分、浮子抑制、高斯偏移约束等）虽对定量指标的提升有限，但有效抑制了退化高斯，提升了渲染速度（Table 8, Table 9）。

### 与基线方法的关键差异

| 设计维度 | 基线方法 | SHARP |
|---------|---------|-------|
| 深度层数 | 单层深度图 | 两层深度（可见表面+遮挡/视角依赖） |
| 深度调整 | 无 | C-VAE风格尺度图预测（训练时使用，推理时恒等） |
| 深度骨干 | 冻结的预训练编码器 | 解冻低分辨率编码器，端到端适应 |
| 损失配置 | 通常仅L1颜色损失 | 感知损失（特征+Gram矩阵）+ 多项正则化 |

这些创新协同作用，使SHARP在亚秒级推理时间内实现了25–34%的LPIPS降低和21–43%的DISTS降低（相对于此前最优方法**Gen3C**，Ren et al., 2025），同时在相机基线小于0.5米的近距视角合成中保持一致的领先优势。



SHARP 采用端到端可训练的前馈网络，从单张图像直接回归 3D 高斯表示，整体流程在标准 GPU 上亚秒级完成。网络由四个可学习模块组成（见 Figure 3），输入为单张 RGB 图像 $\mathbf{I} \in \mathbb{R}^{C \times H \times W}$，输出为一组 3D 高斯 $\mathbf{G} \in \mathbb{R}^{K \times N}$，其中 $K=14$ 为每个高斯球的属性数（位置 3 维、尺度 3 维、旋转 4 维、颜色 3 维、不透明度 1 维）。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/003_Figure_3.jpg]]
*Figure 3: Our model consists of four learnable modules (Section 3.1): a pretrained encoder for feature extraction, a depth decoder that produces two distinct depth layers, a depth adjustment module, and a Gaussian decoder that refines all Gaussian attributes. The differentiable Gaussian initializer and composer assemble the Gaussians for the resulting 3D representation. The predicted Gaussians are rendered to the input and novel views for loss computation (Section 3.4)*

### 模块化流水线

1. **特征编码器**：基于 Depth Pro 的 ViT 骨干（Bochkovskii et al., 2025）提取多尺度特征图 $(\mathbf{f}_i)_{i \in \{1,\dots,4\}}$，供后续解码器共享。该编码器在训练初期冻结，后续解冻低分辨率部分以适应视角合成任务。

2. **深度解码器**：基于 Dense Prediction Transformer（DPT）架构，从特征图生成两层深度预测 $\hat{\mathbf{D}} \in \mathbb{R}^{2 \times H \times W}$。第一层对应可见表面深度，第二层建模遮挡或视角依赖区域。这一设计直接回应了单目深度估计的固有歧义——透明/反射表面和纹理弱区域往往导致单一深度层无法准确表达场景几何。

3. **深度调整模块**：一个小型 U-Net，在训练时接受预测逆深度 $\hat{\mathbf{D}}^{-1}$ 和真实逆深度 $\mathbf{D}^{-1}$，输出尺度图 $\mathbf{S} \in \mathbb{R}^{H \times W}$ 来校准深度预测。推理时该模块被恒等映射替代，不增加额外计算开销。该模块的因果机制在于：将单目深度估计的不确定性建模为可学习的尺度调整，使网络能够学习对视角合成最优的深度表示，而非单纯追求深度数值准确。

4. **高斯解码器**：$\varphi_{\mathrm{gauss}}$ 以特征图 $(\mathbf{f}_i)$ 和输入图像 $\mathbf{I}$ 为输入，输出所有高斯属性的修正量 $\Delta \mathbf{G} \in \mathbb{R}^{K \times 2 \times H' \times W'}$：

   $$\Delta \mathbf{G} = \varphi_{\mathrm{gauss}}((\mathbf{f}_i)_{i \in \{1, \dots, 4\}}, \mathbf{I})$$

5. **可微分高斯组合器**：将基础高斯 $\mathbf{G}_0$ 与修正量 $\Delta \mathbf{G}$ 组合，使用属性特定的激活函数 $\gamma_{\mathrm{attr}}$ 和尺度因子 $\eta_{\mathrm{attr}}$：

   $$\mathbf{G}_{\mathrm{attr}} = \gamma_{\mathrm{attr}}\left(\gamma_{\mathrm{attr}}^{-1}(\mathbf{G}_{\mathrm{0,attr}}) + \eta_{\mathrm{attr}} \Delta \mathbf{G}_{\mathrm{attr}}\right)$$

   不同属性使用不同的激活函数（如位置使用恒等映射，尺度使用指数函数），确保各属性的数值范围合理。

### 端到端训练与损失设计

整个流水线端到端训练，损失在输入视图和新视图上同时计算。损失函数经过精心配置以优先视角合成质量，同时维持训练稳定性并抑制常见视觉伪影：

- **颜色损失** $\mathcal{L}_{\mathrm{color}}$：输入视图和新视图上的 L1 渲染损失。
- **感知损失** $\mathcal{L}_{\mathrm{percep}}$：在新视图上结合 VGG 特征损失和 Gram 矩阵损失，鼓励清晰的纹理修复。
- **深度损失**：约束预测深度与真实深度的一致性，减少几何变形。
- **正则化项**：包括总变分（TV）、浮子抑制、高斯偏移量约束、尺度正则化等，虽然对定量指标提升不大，但改善了渲染质量并提升了渲染速度（减少退化高斯）。

消融实验（Table 8, Table 10）表明，感知损失（特别是 Gram 矩阵分量）对图像清晰度提升最为显著；深度调整模块（Table 11）和解冻深度骨干（Table 13）均一致地改善了 DISTS/LPIPS 指标，验证了消除深度歧义对视角合成质量的重要性。



SHARP 的整体架构由四个可学习的核心模块组成（Figure 3），其设计目标是从单张图像直接回归出高分辨率 3D 高斯表示，并通过端到端训练优化视角合成保真度。

### 特征编码器（Feature Encoder）

特征编码器基于 **Depth Pro** 的 ViT 骨干网络（Bochkovskii et al., 2025），负责从输入图像 $\mathbf{I} \in \mathbb{R}^{C \times H \times W}$ 中提取四个多尺度特征图 $(\mathbf{f}_i)_{i \in \{1, \dots, 4\}}$。这些特征图被后续所有解码器模块共享使用。

### 深度解码器（Depth Decoder）

深度解码器基于 Dense Prediction Transformer (DPT) 架构构建。与标准单目深度估计不同，SHARP 将 DPT 解码器的最后一层卷积复制为双通道输出，从而预测两层深度图 $\hat{\mathbf{D}} \in \mathbb{R}^{2 \times H \times W}$：第一层对应可见表面，第二层用于建模遮挡区域或视角依赖效果。这种双层深度设计为后续的高斯初始化提供了更丰富的几何先验。

### 深度调整模块（Depth Adjustment Module）

这是 SHARP 应对单目深度估计固有歧义的关键创新。该模块采用一个小型 U-Net 网络，训练时同时接收预测的逆深度 $\hat{\mathbf{D}}^{-1}$ 和真实逆深度 $\mathbf{D}^{-1}$，输出一个尺度图 $\mathbf{S} \in \mathbb{R}^{H \times W}$，用于校准预测深度。该设计受条件 VAE 启发，将深度不确定性建模为可学习的逐像素尺度调整。推理阶段，深度调整模块被替换为恒等映射（即 $\mathbf{S} = \mathbf{1}$），使网络完全基于单张图像运行。

### 高斯解码器与组合器

高斯解码器 $\varphi_{\mathrm{gauss}}$ 从特征图和输入图像中预测所有高斯属性的修正量：

$$\Delta \mathbf{G} = \varphi_{\mathrm{gauss}}((\mathbf{f}_i)_{i \in \{1, \dots, 4\}}, \mathbf{I})$$

其中 $\Delta \mathbf{G} \in \mathbb{R}^{K \times 2 \times H' \times W'}$，$K=14$ 对应 14 个高斯属性通道（位置 3、尺度 3、旋转 4、颜色 3、不透明度 1）。双层输出分别对应两层深度图各自的高斯修正。

高斯组合器通过属性特定的激活函数将基础高斯与修正量融合：

$$\mathbf{G}_{\mathrm{attr}} = \gamma_{\mathrm{attr}}\left(\gamma_{\mathrm{attr}}^{-1}(\mathbf{G}_{\mathrm{0,attr}}) + \eta_{\mathrm{attr}} \Delta \mathbf{G}_{\mathrm{attr}}\right)$$

各属性的激活函数 $\gamma_{\mathrm{attr}}$ 及对应尺度因子 $\eta_{\mathrm{attr}}$ 详见 Table（Activation Functions），例如位置使用恒等映射、尺度使用 softplus、旋转使用归一化、颜色使用 sigmoid、不透明度使用 sigmoid。

### 损失函数体系

SHARP 采用精心调校的多项损失组合，总损失为各损失项的加权和：

$$\mathcal{L} = \sum_{\mathrm{d} \in \mathcal{D}} \lambda_{d} \mathcal{L}_{d} + \sum_{r \in \mathcal{R}} \lambda_{r} \mathcal{L}_{r} + \sum_{\mathrm{s} \in \mathcal{S}} \lambda_{s} \mathcal{L}_{s}$$

其中 $\mathcal{D} = \{\mathrm{color}, \mathrm{alpha}, \mathrm{depth}, \mathrm{percep}\}$ 为核心损失，$\mathcal{R}$ 为正则化项集合，$\mathcal{S}$ 为尺度相关损失。

**颜色损失** 在输入视图和新视图上同时施加 L1 渲染损失：

$$\mathcal{L}_{\mathrm{color}} = \sum_{\mathrm{view} \in \{\mathrm{input}, \mathrm{novel}\}} \mathbb{E}_{p \sim \Omega} \left[ | \hat{\mathbf{I}}_{\mathrm{view}}(p) - \mathbf{I}_{\mathrm{view}}(p) | \right]$$

**感知损失** 在新视图上结合特征损失和 Gram 矩阵损失，是提升图像清晰度的关键：

$$\mathcal{L}_{\mathrm{percep}} = \sum_{l=1}^{4} \lambda_{l}^{\mathrm{feat}} \cdot \big\| \phi_{l}(\widehat{\mathbf{I}}_{\mathrm{novel}}) - \phi_{l}(\mathbf{I}_{\mathrm{novel}}) \big\|^2 + \lambda_{l}^{\mathrm{Gram}} \cdot \big\| M_{l}(\widehat{\mathbf{I}}_{\mathrm{novel}}) - M_{l}(\mathbf{I}_{\mathrm{novel}}) \big\|^2$$

其中 $\phi_l$ 为 VGG 网络第 $l$ 层的特征图，$M_l$ 为对应的 Gram 矩阵。消融实验（Table 8, Table 10）表明，感知损失（尤其是 Gram 矩阵项）对图像质量提升贡献显著。

**深度损失** 在预测深度与真实深度之间施加约束，减少几何变形。

**正则化项** 包括总变分正则化、浮子抑制损失、高斯偏移量约束等，虽然对定量指标提升不大，但可减少退化高斯数量并提升渲染速度（Table 9）。

### 补充图表

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/008_Figure_5.jpg]]
*Figure 5: Ambiguity in depth estimation. We demonstrate the inherent ambiguity in monocular depth estimation by (a) taking an original image, (b) predicting its depth using Depth Pro, (c) horizontally flipping the image, applying Depth Pro, and flipping the result back, and (d) computing the relative absolute error between the two predictions to generate an uncertainty map. Higher values (brighter regions) indicate greater inconsistency between predictions*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/025_Figure_10.jpg]]
*Figure 10: The effect of learned depth adjustment*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/027_Figure_12.jpg]]
*Figure 12: The effect of unfreezing the monodepth backbone*



## 实验与关键发现

### 评估协议与指标选择

SHARP 在六个公开数据集上进行评估：Middlebury、Booster、ScanNet++、WildRGBD、Tanks and Temples 和 ETH3D。所有方法均在完整分辨率下评估；对于具有固定宽高比的扩散方法，将其输出填充或裁剪以匹配原始分辨率，确保公平对比。

评估指标以 **LPIPS** 和 **DISTS** 为主要依据，因为 PSNR 和 SSIM 对微小平移过度敏感。如 Figure 4 和 Table 2 所示，仅 1% 的图像平移即可使 PSNR 降至 11.2、SSIM 降至 0.375，而 DISTS 在此条件下表现出更强的稳定性。PSNR/SSIM 数字在 Table 5 中提供完整性参考，但不作为主要结论依据。

### 主要定量结果

Table 1 展示了六大数据集上的综合对比。SHARP 在所有数据集的所有指标上均达到最优，相比此前最强的扩散式方法 **Gen3C**（Ren et al., 2025），LPIPS 降低 25–34%，DISTS 降低 21–43%。具体而言：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/004_Table_1.jpg]]
*Table 1: Quantitative evaluation. Lower is better. Best , second-best , and third-best in each column are highlighted*

- **Middlebury**：DISTS 0.097，LPIPS 0.358
- **Booster**：DISTS 0.119，LPIPS 0.270
- **ScanNet++**：DISTS 0.071，LPIPS 0.154
- **WildRGBD**：DISTS 0.069，LPIPS 0.190
- **Tanks and Temples**：DISTS 0.122，LPIPS 0.421
- **ETH3D**：DISTS 0.258，LPIPS 0.554

Figure 1 进一步展示了合成时间与图像保真度的权衡关系：SHARP 在不到一秒的单次前馈中完成 3D 高斯场回归，渲染速度超过 100 FPS（Table 6），在速度-质量 Pareto 前沿上显著优于所有对比方法。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/001_Figure_1.jpg]]
*Figure 1: Synthesis time on a single GPU versus image fidelity on the ScanNet++ dataset*

### 运动范围分析

Figure 7 分析了相机基线大小对 DISTS 指标的影响。SHARP 在基线小于 0.5 米的范围内一致最优；在 0.5–3 米范围内仍保持第一或第二的位置，与扩散式方法相比具有竞争力。超过 3 米后，由于单目深度估计的固有歧义和缺乏远距离内容生成机制，质量下降明显。这一分析揭示了 SHARP 的核心适用边界：近距离高保真视角合成。

### 消融实验

#### 损失函数组件

Table 8 和 Figure 9 展示了损失函数的消融结果。着色损失和 Alpha 损失构成基础；添加深度损失可减少几何变形；引入感知损失（特别是 Gram 矩阵损失）显著提升图像清晰度和定量指标。Table 10 进一步验证了 Gram 矩阵损失的独立贡献。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/015_Table_8.jpg]]
*Table 8: Ablation study on loss components. The perceptual loss significantly enhances image quality; regularizer losses*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/024_Figure_9.jpg]]
*Figure 9: The effect of different loss terms*

正则化项（总变分、浮子抑制、偏移量限制等）对定量指标提升有限，但改善了渲染质量并提升了渲染速度——Table 9 显示，添加正则化项后中位渲染延迟降低，原因是减少了退化高斯。

#### 深度调整模块

Table 11 和 Figure 10 验证了深度调整模块的有效性。该模块在 ScanNet++ 和 Tanks and Temples 上一致提升了 DISTS/LPIPS，证明通过 C-VAE 风格的尺度图预测来校准单目深度估计的不确定性，对视角合成质量至关重要。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/018_Table_11.jpg]]
*Table 11: Ablation study on depth adjustment. Using the learned depth adjustment module consistently improves image quality. See also Figure 10*

#### 解冻深度骨干网络

Table 13 和 Figure 12 显示，解冻单目深度骨干网络（低分辨率图像编码器）显著改善了边界伪影和反射区域的渲染质量，定量指标也有明显提升。这验证了端到端优化使深度表示适应视角合成任务的核心设计选择。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/020_Table_13.jpg]]
*Table 13: Ablation study on unfreezing the monodepth backbone. See also Figure 12*

#### 输出高斯数量

Table 14 和 Figure 13 表明，增加输出高斯的数量（如从 192×192 到 768×768）持续提升性能，说明细粒度 3D 表示对高保真渲染的重要性。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/028_Figure_13.jpg]]
*Figure 13: The effect of the number of output Gaussians*

#### 自监督精调

Table 12 和 Figure 11 显示，自监督精调（SSFT）在定量指标上未产生一致提升，但在定性研究中有所帮助，表明其在特定场景下可能改善视觉质量。

### 特权深度信息分析

Table 7 和 Figure 14 展示了使用真实深度作为特权信息时的结果。SHARP 在此设置下进一步扩大了与基线方法的差距，表明深度估计质量是当前性能瓶颈之一。Figure 7(b) 显示，特权深度信息使 SHARP 在更大运动范围内保持竞争力。

### 失败模式与局限性

Figure 8 展示了典型失败案例：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_yx3g4sF70y/figures/023_Figure_8.jpg]]
*Figure 8: Depth failures in challenging edge cases*

1. **强景深场景**（如微距照片）：深度模型无法正确估计大幅离焦区域的几何结构。
2. **复杂反射和透明表面**：单目深度估计的固有歧义导致错误的 3D 几何，产生不可修复的失真。
3. **重复纹理或星空纹理**：深度模型可能将夜空纹理误解为曲面，造成严重几何伪影。
4. **大基线运动**：超过 0.5 米的相机运动导致渲染质量显著下降，无法合成远距离无重叠的新视角。

这些失败模式根源于单目深度估计的固有歧义——如 Figure 5 所示，对同一图像进行水平翻转后预测深度，再翻转回来，与原始预测之间存在显著不一致，特别是在透明/反射区域和纹理弱区域。

### 数据质量公平性验证

Table 4 展示了在内部合成数据上重新训练 **Flash3D**（Szymanowicz et al., 2025a）的结果，证明训练数据质量并非 SHARP 性能优势的主导因素，核心增益来自架构设计和损失配置。



## 定位与知识库关联

### 方法谱系

SHARP 处于单目新视角合成（Novel View Synthesis, NVS）的前馈式方法分支，其核心思路是将单张图像的3D理解问题转化为一次性回归3D高斯场（3D Gaussian Splatting）参数的任务。与现有方法相比，SHARP 在方法谱系中的定位体现在以下关键差异上：

**与扩散式方法的对比。** 当前单目NVS的领先方法多基于扩散模型，如 **Gen3C**（Ren et al., 2025）、**Stable Virtual Camera (SVC)**（Zhou et al., 2025）和 **ViewCrafter**（Yu et al., 2025b）。这些方法通过迭代去噪过程生成新视角，虽然能够处理较大的相机运动范围，但合成速度慢（通常需要数十秒至数分钟），且容易产生内容幻觉。SHARP 选择了一条截然不同的路径：通过单次前馈网络直接预测3D高斯表示，在不到一秒内完成合成，同时以超过100 FPS的速度支持高分辨率渲染。定量结果表明，SHARP 在六个数据集上将 LPIPS 降低了 25–34%、DISTS 降低了 21–43%（相对于此前最优的 Gen3C），在保真度与速度之间取得了显著突破（Figure 1, Table 1）。

**与同类前馈方法的对比。** 在前馈式方法中，**Flash3D**（Szymanowicz et al., 2025a）同样从单张图像直接预测3D高斯，但 SHARP 在架构设计上做出了几项关键改进。作者通过内部合成数据重新训练 Flash3D 的消融实验（Table 4）证明，SHARP 的性能优势并非来自训练数据的差异，而是源于架构和损失函数的设计选择。**TMPI**（Khan et al., 2023）基于平铺多层图像表示，**LVSM**（Jin et al., 2025）采用图像到图像回归，两者在保真度和泛化能力上均弱于 SHARP（Table 1）。

**与通用3D高斯方法的对比。** SHARP 继承了3D Gaussian Splatting 的显式表示框架，但将其从多视角重建场景迁移到了单目前馈预测场景。与传统3DGS需要多张标定图像和逐场景优化不同，SHARP 通过一个端到端训练的网络直接从单张图像推断完整的3D高斯场参数（包括位置、尺度、旋转、颜色和不透明度共14个属性），实现了泛化能力与推理效率的统一。

### 知识库定位

**核心贡献。** SHARP 的核心贡献在于揭示了单目深度估计的固有歧义是制约单目NVS质量的关键瓶颈，并提出了一个系统性的解决方案：通过条件VAE启发的深度调整模块将深度不确定性建模为可学习的尺度调整，同时解冻深度编码器使其通过视图合成损失进行端到端适应。这一设计迫使网络学习对视角合成最优的深度表示，而非单纯追求深度数值的准确。消融实验（Table 11, Table 13）一致证实了这两个设计的有效性。

**技术栈定位。** SHARP 的技术栈融合了三个关键组件：（1）基于 **Depth Pro**（Bochkovskii et al., 2025）ViT骨干的特征编码器；（2）受DPT（Dense Prediction Transformer）启发的深度解码器，创新性地输出两层深度图以分别建模可见表面和遮挡/视角依赖区域；（3）精心设计的损失函数体系，包括颜色损失、Alpha损失、深度损失、感知损失（含特征损失和Gram矩阵损失）以及多个正则化项（总变分、浮子抑制、高斯方差约束等）。消融实验（Table 8, Table 10）表明，感知损失（特别是Gram矩阵损失）对图像清晰度提升最为显著，而正则化项虽对定量指标提升有限，但有效减少了退化高斯并提升了渲染速度（Table 9）。

**评估体系贡献。** SHARP 对评估体系也做出了重要贡献。作者系统性地揭示了PSNR和SSIM对微小平移的过度敏感性（1%平移使PSNR降至11.2，SSIM降至0.375），而DISTS表现出更强的稳定性（Figure 4, Table 2）。这一发现为单目NVS领域的评估标准选择提供了有价值的参考。

### 适用边界

SHARP 的设计和训练针对的是**近距离相机运动**场景。运动范围分析（Figure 7）表明，SHARP 在相机基线小于0.5米时表现最优，在0.5–3米范围内仍保持竞争力（通常为最优或次优），但超过3米后质量下降明显。这一特性源于其前馈式设计的本质局限：网络只能从单张图像推断可见表面的3D信息，无法生成远距离无重叠区域的内容。

### 局限与开放问题

**已知局限。** SHARP 存在以下已验证的局限：

1. **深度估计的长尾失效。** 对于具有强烈景深效果（如微距照片）、复杂反射/透明表面、重复纹理或星空纹理的场景，深度模型容易失效，导致不可修复的3D几何错误（Figure 8）。即使解冻深度骨干也无法完全恢复这些由深度预测错误导致的失真。

2. **运动范围受限。** 仅适用于短距离相机运动（<0.5米最优），无法合成远距离无重叠的新视角。这是前馈式方法相对于扩散式方法的根本性权衡：速度与泛化范围之间的取舍。

3. **输出格式限制。** 目前不支持可变的纵横比输出，渲染的视角范围有限。

**开放问题。** 作者明确提出了以下值得探索的方向：

1. **前馈与扩散的融合。** 如何将SHARP的快速前馈3D表示能力与扩散模型的远距离内容生成能力相结合，实现既支持近距离高保真渲染又能生成远距离视角的统一方法。

2. **深度模型的鲁棒性提升。** 如何进一步改进深度模型以应对长尾场景（透明、反射、强景深），可能的路径包括利用扩散模型提供的丰富先验或进行更大规模的重训练。

3. **多视角扩展。** 是否可以将方法扩展到多视角或视频输入，以利用多帧信息提升几何一致性。

4. **视角依赖效果的建模。** 如何系统性地处理视角依赖效果和体积渲染，以进一步提升画质。



## 原文 PDF

![[paperPDFs/ICLR_2026/Sharp_Monocular_View_Synthesis_in_Less_Than_a_Second_9ff8519e0fec.pdf]]
