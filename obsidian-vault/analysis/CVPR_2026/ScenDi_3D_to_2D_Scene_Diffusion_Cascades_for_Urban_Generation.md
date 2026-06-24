---
title: "ScenDi: 3D-to-2D Scene Diffusion Cascades for Urban Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ScenDi_3D_to_2D_Scene_Diffusion_Cascades_for_Urban_Generation.pdf
project_link: "https://xdimlab.github.io/ScenDi"
code_link: null
aliases:
- ScenDi
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将场景生成解耦为3D几何与粗外观阶段（Voxel-to-3DGS VQ-VAE + 3D潜在扩散生成粗3D高斯）和2D细节增强阶段（以粗渲染RGB图像为条件的视频扩散模型），并通过渲染图像建立信息纽带。
primary_logic: 3D生成应主导几何与粗外观先验的建立，而2D扩散专注于细节细化和远距离区域合成，从而兼顾高保真外观与精确相机控制。
claims:
- 在KITTI-360数据集上，ScenDi（WAN变体）在3D生成方法中取得了最佳的FID (22.9)、KID (0.016) 和 FVD (262.6)。
- 在2D精细化的条件消融中，使用粗渲染RGB图像作为条件（FID 36.9）显著优于使用深度图（FID 78.6）。
- 由于先通过3D扩散生成显式3DGS，ScenDi的相机控制精度与纯3D生成方法相当。
- KITTI-360 上 FID ↓ = 22.9 (ScenDi-WAN)
---

# ScenDi: 3D-to-2D Scene Diffusion Cascades for Urban Generation

> [!tip] 核心洞察
> 3D生成应主导几何与粗外观先验的建立，而2D扩散专注于细节细化和远距离区域合成，从而兼顾高保真外观与精确相机控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | ScenDi: 面向城市场景生成的3D到2D场景扩散级联模型 |
| 英文题名 | ScenDi: 3D-to-2D Scene Diffusion Cascades for Urban Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.15221) · [Project](https://xdimlab.github.io/ScenDi) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ScenDi |
| Dataset | KITTI-360 |

> [!tip] 效果简介
> - KITTI-360 上，FID ↓ 22.9 (ScenDi-WAN) vs 33.0 (UrbanGen) (-10.1)；TransErr ↓ 0.06 (ScenDi-WAN) vs 0.21 (UrbanGen) (-0.15)。

## 概述

城市场景生成面临一个根本性瓶颈：**3D生成模型受限于分辨率，难以产生高频细节且无法有效建模远距离区域；而纯2D生成模型虽能产出逼真图像，却缺乏显式3D结构，导致相机控制能力薄弱**。ScenDi 通过一种**3D到2D的扩散级联框架**来打破这一僵局——将场景生成解耦为两个阶段，让3D扩散主导几何与粗外观先验的建立，再由2D扩散专注于细节细化和远距离区域合成，从而兼顾高保真外观与精确相机控制。

具体而言，ScenDi 首先训练一个 **Voxel-to-3DGS VQ-VAE**，将来自现成深度估计器的彩色体素网格映射为3D高斯原语；随后在VQ-VAE的潜空间中训练一个**3D潜在扩散模型**生成粗粒度的3D场景，可选地接受道路布局或文本等条件信号以实现可控生成；最后，以粗3D场景渲染的RGB视频片段为条件，微调一个**2D视频扩散模型**来增强前景细节并补全远景区域。这一设计的关键创新在于，将粗渲染RGB图像而非深度图或语义图作为2D精细化的条件信号——消融实验表明，这一选择在KITTI-360上将FID从78.6大幅降至36.9。

在KITTI-360和Waymo两个真实自动驾驶数据集上，ScenDi 在视频生成质量与相机控制精度上均表现出显著优势：其WAN变体在KITTI-360上取得了 **FID 22.9**、**KID 0.016** 和 **FVD 262.6** 的3D生成方法最佳成绩，同时平移误差仅0.06，与纯3D生成方法保持同等的相机控制精度。该框架还展现出灵活的场景修复与可控合成能力，支持通过布局和文本提示对生成内容进行显式引导。

## 背景与动机

自动驾驶仿真与城市数字孪生等应用对高质量、可自由操控相机的城市场景生成提出了迫切需求。现有方法大致分为两条技术路线，但各自存在结构性短板：

**纯3D生成方法的瓶颈。** 以**UrbanGen**（Yang et al., TPAMI 2025）、**GaussianCity**（Xie et al., CVPR 2025）等为代表的3D生成方法，通过体素网格、语义占据或3D高斯原语（3DGS）显式建模场景几何，天然具备精确的相机控制能力。然而，受限于3D表征的分辨率与模型容量，这类方法生成的场景普遍缺乏高频纹理细节，且难以有效建模远距离区域的外观——这些区域在训练数据中往往因距离过远而采样稀疏，导致生成质量下降。

**纯2D生成方法的不足。** 以**Vista**、**Gen3C**（Ren et al., CVPR 2025）等为代表的图像/视频生成方法，借助大规模预训练视频扩散模型的丰富先验，能够合成高度逼真的外观。但由于缺乏显式的3D场景表征，这类方法对相机位姿的控制精度有限，难以满足需要精确视点操控的下游任务需求。

**核心矛盾。** 上述困境揭示了一个根本性张力：3D生成提供几何先验与相机可控性，但牺牲外观保真度；2D生成提供逼真外观，但丧失显式3D结构与精确相机控制。如何在一个统一框架中同时获得二者的优势，是城市场景生成领域的核心挑战。

**本文动机。** ScenDi 提出将场景生成解耦为“3D几何与粗外观建立”和“2D细节增强”两个阶段，通过3D到2D的扩散级联（3D-to-2D Diffusion Cascades）来调和上述矛盾。其核心洞察是：让3D扩散模型主导几何与粗外观先验的建立，再以粗渲染的RGB图像为信息纽带，驱动2D视频扩散模型专注于细节细化和远距离区域合成，从而在高保真外观与精确相机控制之间取得平衡。

## 核心创新

ScenDi 的核心创新在于将城市场景生成任务解耦为**3D几何与粗外观先验建立**和**2D细节增强**两个阶段，并通过渲染图像在二者之间建立信息纽带。这一设计直接回应了当前3D与2D生成模型各自的瓶颈：纯3D方法受限于分辨率而缺乏高频细节，纯2D方法则因缺乏显式3D结构而难以实现精确的相机控制。

### 关键Changed Slots

**1. 3D场景表示：从体素网格到3D高斯原语**

传统3D城市场景生成方法多依赖语义占据体素网格（如 **UrbanGen**, Yang et al., TPAMI 2025）或神经辐射场作为场景表示。ScenDi 提出 **Voxel-to-3DGS VQ-VAE**，将彩色体素网格 $\mathcal{V}$ 编码为低维潜变量 $z_q^{\mathcal{V}}$，并解码为一组3D高斯原语 $\mathcal{G}$：

$$z^{\mathcal{V}} = \mathcal{E}_\theta^{3D}(\mathcal{V}), \quad z_q^{\mathcal{V}} = \mathcal{Q}_\theta^{3D}(z^{\mathcal{V}}), \quad \mathcal{G} = \mathcal{D}_\theta^{3D}(z_q^{\mathcal{V}})$$

每个高斯原语的特征向量 $\mathbf{f}$ 通过MLP预测颜色 $\mathbf{c}$ 和不透明度 $\alpha$：
$$\mathbf{c} = f_\theta^{\mathrm{color}}(\mathbf{f}), \quad \alpha = f_\theta^{\mathrm{opa}}(\mathbf{f})$$

该VQ-VAE的总重建损失结合了3D占用损失与多帧2D外观损失：
$$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{3D} + \sum_{m=1}^{M} \mathcal{L}_{2D}^{m}$$

消融实验（Table 2, Waymo数据集）表明，引入BCE损失有助于学习准确的场景占用，略微提升重建质量；每个体素增加高斯数量（$G=6$）仅带来微小改善。

**2. 2D精细化条件输入：从深度/语义图到粗渲染RGB图像**

这是ScenDi最具决定性的设计选择。此前的3D-to-2D级联工作（如UniScene、Infinicube）通常使用深度图或语义图作为2D增强阶段的条件信号。ScenDi则直接使用由3D高斯渲染的**粗RGB图像**作为条件。

KITTI-360上的消融实验（Table 3）给出了强证据：使用粗渲染RGB作为条件（FID 36.9）显著优于使用深度图（FID 78.6），在Waymo数据集上同样观察到一致趋势（FID 41.3 vs 77.4）。从训练效率看，RGB条件信号也展现出更快的收敛速度（Figure 4）。作者分析认为，RGB条件信号与2D扩散模型的输入域天然对齐，能更有效地利用预训练视频扩散模型中的丰富先验知识。

**3. 长视频推理策略：Diffusion Forcing替代Repaint**

在推理长视频时，传统方法（如Repaint策略）在相邻片段边界处可能产生背景突变。ScenDi采用**Diffusion Forcing策略**，为每帧独立采样噪声水平，从而改善片段间背景一致性。Figure 6的消融实验显示，使用Diffusion Forcing（w/ DF）显著提升了相邻片段背景区域的连贯性，避免了Repaint策略（w/o DF）下的突变现象。

### 创新机制的内在逻辑

上述三个changed slots共同支撑了ScenDi的因果调控逻辑：**3D扩散主导几何与粗外观先验的建立，2D扩散专注于细节细化和远距离区域合成**。由于首先生成了显式3DGS，ScenDi的相机控制精度与纯3D生成方法相当（Table 1, TransErr 0.06, RotErr 0.23），同时借助2D视频扩散模型的先验知识，在视觉质量上大幅超越纯3D基线（FID 22.9 vs UrbanGen 33.0）。

> **注意**：当前分析基于arXiv预印本，部分baseline方法（如CC3D、Vista）的完整引用信息需手动核实。本文提出的级联框架中，2D扩散的生成质量依赖于前级3D LDM的输出——若3D生成效果不佳，可能导致后续伪影，这是该架构的固有局限。

## 整体框架

ScenDi 的核心设计是将城市场景生成解耦为两个级联阶段：**3D 粗生成** 与 **2D 精细化**。这一 3D-to-2D 扩散级联架构的动机源于一个根本性瓶颈：纯 3D 生成模型受限于分辨率，难以捕捉高频细节和远距离区域；而纯 2D 生成模型虽能产出高保真外观，却缺乏显式 3D 结构，导致相机控制能力薄弱。ScenDi 的因果调节旋钮在于，让 3D 扩散主导几何与粗外观先验的建立，再让 2D 视频扩散专注于细节细化和远景合成，从而兼顾高保真外观与精确相机控制。

整个 pipeline 由四个核心模块串联而成，数据流自上而下贯通（参见 Figure 2）：

![[assets/figures/papers/paper_list_l2588_https_arxiv_org_abs_2601_15221/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview. ScenDi leverages 3D and 2D diffusion cascades to generate high-quality urban scenes. Top: We first build a Voxel-to-3DGS VQ-VAE to reconstruct scenes in a feed-forward manner. The input is a colored voxel grid V constructed based on off-the-shelf metric depth estimator, whereas the output is a set of 3D Gaussian primitives G. Then, we train a 3D diffusion model*

1. **输入体素网格构建**：利用现成的度量深度估计器（off-the-shelf metric depth estimator）从多视角图像融合生成彩色体素网格 $\mathcal{V} \in \mathbb{R}^{H \times W \times D \times 3}$，作为后续 3D 处理的统一输入表示。
2. **Voxel-to-3DGS VQ-VAE**：将体素网格 $\mathcal{V}$ 编码为低维潜变量 $z_q^{\mathcal{V}}$，再解码为一组 3D 高斯原语 $\mathcal{G}$（见 Eq. (1)）。该模块以端到端方式重建场景，将离散体素表示转化为可微渲染的连续 3D 高斯场，从而建立了从几何先验到可渲染表示的桥梁。
3. **3D 潜在扩散模型**：在 VQ-VAE 的潜空间 $\mathbf{z}^{\nu}$ 上训练去噪扩散过程，从随机噪声生成粗粒度的 3D 场景。该阶段可选地接受条件信号（如道路布局图或文本提示），以控制生成内容的语义布局。生成的高斯原语可通过可微渲染器投影为任意视角的粗渲染 RGB 图像，这些图像成为连接两阶段的**信息纽带**。
4. **2D 视频扩散精细化**：以粗渲染 RGB 视频片段为条件，微调预训练的视频扩散模型（如 WAN2.1），对前景外观细节进行增强，并合成远距离区域——这些区域在原始 3D 高斯中往往因分辨率限制而缺失或模糊。

这种级联设计的核心洞察在于：3D 扩散负责“结构正确性”，2D 扩散负责“外观真实感”，二者通过渲染图像实现信息传递，而非在 3D 空间中直接追求高分辨率。在推理时，长视频生成采用 **Diffusion Forcing** 策略——为每帧独立采样噪声水平，避免简单替换或 Repaint 方法带来的片段间背景突变（参见 Figure 6）。

**关键方法差异**：与 UniScene、Infinicube 等先前工作使用深度图或语义图作为 2D 精细化条件不同，ScenDi 创新性地使用由 3D 高斯渲染的**粗 RGB 图像**作为条件信号。消融实验表明，这一选择对最终视觉质量至关重要——在 KITTI-360 上，RGB 条件（FID 36.9）显著优于深度条件（FID 78.6）（Table 3），因为 RGB 图像携带了更丰富的纹理和结构先验，使 2D 扩散模型能更有效地利用其预训练先验。

### 补充图表

![[assets/figures/papers/paper_list_l2588_https_arxiv_org_abs_2601_15221/figures/001_Figure_1.jpg]]
*Figure 1: ScenDi generates high-quality urban scenes using a 3D-to-2D Scene Diffusion cascade, with optional condition signals like text and layout for controllable 3D space generation. Our method provides flexible camera control, even though our training data primarily consists of forward-moving trajectories*

## 核心模块与公式推导

ScenDi 的核心架构由三个级联模块构成，形成“3D 几何先验 → 2D 外观精细化”的生成管线。

**模块一：Voxel-to-3DGS VQ-VAE**

该模块负责将场景的显式体素表示压缩为 3D 高斯原语。输入为利用现成度量深度估计器从多视角图像融合构建的彩色体素网格 $\mathcal{V} \in \mathbb{R}^{H \times W \times D \times 3}$。编码器 $\mathcal{E}_\theta^{3D}$ 将体素网格映射为低维潜变量，经量化器 $\mathcal{Q}_\theta^{3D}$ 离散化后，由解码器 $\mathcal{D}_\theta^{3D}$ 解码为一组 3D 高斯原语 $\mathcal{G}$：

$$z^{\mathcal{V}} = \mathcal{E}_\theta^{3D}(\mathcal{V}), \quad z_q^{\mathcal{V}} = \mathcal{Q}_\theta^{3D}(z^{\mathcal{V}}), \quad \mathcal{G} = \mathcal{D}_\theta^{3D}(z_q^{\mathcal{V}})$$

每个 3D 高斯的颜色 $\mathbf{c}$ 和不透明度 $\alpha$ 通过 MLP 从其关联的特征向量 $\mathbf{f}$ 预测：

$$\mathbf{c} = f_\theta^{\mathrm{color}}(\mathbf{f}), \quad \alpha = f_\theta^{\mathrm{opa}}(\mathbf{f})$$

VQ-VAE 的总重建损失结合了 3D 占用损失与多帧 2D 外观损失：

$$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{3D} + \sum_{m=1}^{M} \mathcal{L}_{2D}^{m}$$

消融实验（Table 2）表明，引入 BCE 损失有助于学习准确的场景占用，略微提升重建质量；而增加每体素的高斯数量（$G=6$）仅带来微小改善。

**模块二：3D 潜在扩散模型**

在 VQ-VAE 的潜空间 $\mathbf{z}^{\nu}$ 上训练扩散模型，生成粗粒度的 3D 场景表示。前向扩散过程对干净潜变量 $\mathbf{z}_0^{\nu}$ 按噪声调度添加噪声：

$$\mathbf{z}_t^{\nu} = \sqrt{\bar{\alpha}_t} \mathbf{z}_0^{\nu} + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, 1)$$

模型采用 v-prediction 参数化，从带噪潜变量与预测噪声中估计原始干净潜变量：

$$\hat{\mathbf{z}}_0^{\nu} = \sqrt{\bar{\alpha}_t} \mathbf{z}_t^{\nu} - \sqrt{1 - \bar{\alpha}_t} \epsilon_\theta^{3D}(\mathbf{z}_t^{\nu}; t, c)$$

训练损失为干净潜变量与预测值之间的 MSE：

$$\mathcal{L}_{\mathrm{diff}}^{3D} = ||\mathbf{z}_0^{\nu} - \hat{\mathbf{z}}_0^{\nu}||^2$$

条件信号（如道路布局图或文本提示）通过将下采样后的 one-hot 语义体素与噪声潜变量沿通道维度拼接实现可控生成。

**模块三：2D 视频扩散精细化**

以粗 3D 高斯渲染的 RGB 视频片段 $\tilde{\mathcal{C}}$ 作为条件，微调预训练的 2D 视频扩散模型 $\epsilon_\phi^{2D}$，增强前景细节并合成远距离区域。训练损失同样为 MSE：

$$\mathcal{L}_{\mathrm{diff}}^{2D} = ||\mathbf{z}_0^{\mathcal{C}} - \hat{\mathbf{z}}_0^{\mathcal{C}}||^2$$

该阶段的关键设计在于条件信号的选择：消融实验（Table 3）表明，使用粗渲染 RGB 图像作为条件（KITTI-360 上 FID 36.9）显著优于使用深度图（FID 78.6），因为 RGB 条件携带了更丰富的场景上下文信息，有助于视频扩散模型更高效地学习精细化映射。

## 实验与分析

### 主实验结果

ScenDi 在两个真实世界自动驾驶数据集 **KITTI-360** 和 **Waymo** 上进行了评估。Table 1 报告了 KITTI-360 上的定量对比，涵盖视频生成质量（FID ↓、KID ↓、FVD ↓）与相机控制精度（TransErr ↓、RotErr ↓）两个维度。

![[assets/figures/papers/paper_list_l2588_https_arxiv_org_abs_2601_15221/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparison about video quality and camera controllability on KITTI-360*

**视频生成质量。** ScenDi 在所有 3D 生成基线中取得了最优的视频质量指标。以 WAN2.1-1.3B 为 2D 精细化骨干的 ScenDi-WAN 变体达到 FID 22.9、KID 0.016、FVD 262.6，相比表现最好的 3D 生成基线 **UrbanGen**（Yang et al., TPAMI 2025）的 FID 33.0 降低了 10.1。这一优势源于级联框架的核心设计：3D 扩散建立粗几何与外观先验，2D 视频扩散利用其丰富的视觉先验知识对前景细节与远景区域进行精细化合成。

**相机控制精度。** ScenDi 的 TransErr 为 0.06、RotErr 为 0.23，与纯 3D 生成方法处于同一精度水平。这是因为 ScenDi 首先通过 3D 潜在扩散模型生成显式的 3D 高斯原语（3DGS），再从中渲染图像——相机姿态的精确控制由 3D 渲染过程天然保证，2D 精细化阶段不会破坏这一几何约束。

**与图像到视频方法的比较。** 需要指出的是，与图像到视频（I2V）方法（如 **Vista**、**Gen3C**）的定量比较并不完全公平：I2V 方法以真实图像为起点逐帧生成，而 ScenDi 从纯噪声生成完整场景，且生成帧可能与 GT 帧存在重叠（见 Sec. 4.3 公平性说明）。

### 消融实验

#### Voxel-to-3DGS VQ-VAE 组件消融

Table 2 在 Waymo 数据集上消融了 VQ-VAE 的关键设计。引入 BCE 损失有助于学习更准确的场景占用，略微提升重建质量；将每个体素的高斯原语数量从默认值增加到 G=6 仅带来微小改善，表明当前表示容量已接近饱和。

![[assets/figures/papers/paper_list_l2588_https_arxiv_org_abs_2601_15221/figures/006_Table_2.jpg]]
*Table 2: Ablation on Voxel-to-3DGS VQ-VAE on Waymo dataset. G denotes to number of Gaussians per voxel*

#### 2D 精细化条件信号消融

Table 3 和 Figure 4 展示了 2D 增强阶段条件信号的关键消融。在 KITTI-360 上，使用粗渲染 RGB 图像作为条件（FID 36.9）显著优于使用深度图（FID 78.6）；Waymo 上趋势一致（FID 41.3 vs 77.4）。RGB 条件不仅提供了几何线索，还传递了颜色与语义信息，使 2D 扩散模型能更高效地学习精细化映射，同时训练收敛速度也更快。这一发现直接支持了论文的核心洞察：粗渲染 RGB 图像是连接 3D 生成与 2D 精细化的最优信息纽带。

![[assets/figures/papers/paper_list_l2588_https_arxiv_org_abs_2601_15221/figures/007_Table_3.jpg]]
*Table 3: Ablation on Conditional Signals. Both models are trained in the same way for the same number of steps*

![[assets/figures/papers/paper_list_l2588_https_arxiv_org_abs_2601_15221/figures/005_Figure_4.jpg]]
*Figure 4: Ablation on Conditional Signal for 2D augmentation. We show samples generated by different conditional signals on KITTI-360 after same training steps*

#### 推理策略消融

Figure 6 对比了 Diffusion Forcing 与 Repaint 两种长视频推理策略。Diffusion Forcing 为每帧独立采样噪声水平，有效改善了相邻片段间的背景一致性，避免了 Repaint 策略下出现的突变伪影。这一设计对长距离相机轨迹的生成质量至关重要。

![[assets/figures/papers/paper_list_l2588_https_arxiv_org_abs_2601_15221/figures/010_Figure_6.jpg]]
*Figure 6: Ablation on Inference Strategy. We visualize neighboring frames obtained from two clips. Using the diffusion forcing strategy (w/ DF) significantly improves the consistency of background regions compared with the repaint strategy (w/o DF)*

### 可控场景生成

Figure 5 展示了 ScenDi 的条件生成能力。通过将语义布局（如道路、车辆、建筑的 one-hot 体素标签）或文本提示作为 3D 扩散模型的条件输入，ScenDi 能够生成与条件信号高度一致的城市场景。这验证了 3D 扩散阶段对显式空间控制的响应能力。

![[assets/figures/papers/paper_list_l2588_https_arxiv_org_abs_2601_15221/figures/008_Figure_5.jpg]]
*Figure 5: Controllable Scene Synthesis on Waymo and KITTI360. The visualization of conditional signals and corresponding synthesized images confirms the adherence of the generated content to diverse conditional guidance*

### 失败模式与局限性

论文明确指出了两个主要挑战：

1. **级联依赖问题。** 2D 视频扩散的生成质量高度依赖于前级 3D LDM 的输出质量。若 3D 扩散生成的粗场景存在严重几何或外观缺陷，2D 精细化阶段可能引入或放大伪影，而非修复它们。

2. **极端视角退化。** 在训练数据以向前运动轨迹为主的情况下，3D LDM 在极端视角变化（如大幅度旋转）下可能出现质量下降，进而影响整体级联效果。这是当前 3D 生成模型泛化能力的普遍瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2588_https_arxiv_org_abs_2601_15221/figures/003_Table.jpg]]

## 方法谱系与知识库定位

### 1. 方法谱系：从纯3D生成到3D-2D级联

ScenDi的提出根植于城市场景生成领域中两类主流范式的固有局限。**纯3D生成方法**——包括基于3D GAN的**DiscoScene**（Xu et al., arXiv 2022）、**CC3D**、**UrbanGen**（Yang et al., TPAMI 2025），基于3D Gaussian Splatting的**GaussianCity**（Xie et al., CVPR 2025），以及基于扩散模型蒸馏的**Urban Architect**（Lu et al., arXiv 2024）——虽然能够提供精确的相机控制，但受限于3D表示的分辨率瓶颈，难以生成高频外观细节，且无法有效建模远距离区域。**纯2D生成方法**（如图像到视频模型**Vista**和3D-aware视频生成模型**Gen3C**（Ren et al., CVPR 2025））虽然借助大规模预训练获得了丰富的视觉先验，但缺乏显式的3D结构，导致相机控制能力薄弱。

ScenDi的核心方法贡献在于将场景生成解耦为两个级联阶段，通过信息纽带实现优势互补。这一设计的关键“因果旋钮”在于：**3D扩散主导几何与粗外观先验的建立，2D扩散专注于细节细化和远距离区域合成**。具体而言，第一阶段通过Voxel-to-3DGS VQ-VAE将体素网格映射为3D高斯原语，并在其潜空间中训练3D扩散模型生成粗3D场景；第二阶段以粗3D高斯渲染的RGB图像为条件，微调预训练视频扩散模型来增强外观细节。这种级联策略使得ScenDi在KITTI-360数据集上取得了3D生成方法中最佳的FID（22.9）、KID（0.016）和FVD（262.6），同时保持了与纯3D方法相当的相机控制精度（TransErr 0.06，RotErr 0.23）（Table 1）。

### 2. 关键设计选择与知识库定位

ScenDi的几项设计选择在城市场景生成的知识谱系中具有明确的定位意义：

**2D精细化条件输入的选择**：与先前工作（如UniScene、Infinicube）使用深度图或语义图作为条件信号不同，ScenDi采用粗3D高斯渲染的RGB图像作为2D扩散的条件输入。消融实验表明，这一选择具有决定性影响——在KITTI-360上，RGB条件相比深度条件将FID从78.6大幅降至36.9（Table 3），同时提高了训练效率。其深层原因在于，RGB条件与预训练视频扩散模型的输入域天然对齐，能够更充分地激活模型内部的视觉先验。

**3D场景表示的选择**：ScenDi选择3D高斯原语而非体素网格或神经辐射场作为中间表示。这一选择使得从3D扩散输出到2D精细化输入的信息传递变得自然高效——仅需渲染操作即可建立纽带，无需额外的域转换。

**长视频推理策略**：针对多片段拼接时的背景一致性问题，ScenDi采用Diffusion Forcing策略为每帧独立采样噪声水平，相比传统的Repaint方法显著改善了片段间的背景连贯性（Figure 6）。

### 3. 适用边界与局限

ScenDi的级联设计引入了上游依赖风险：**2D扩散的生成质量从根本上受限于前级3D LDM的输出**。若3D扩散生成的粗场景存在严重几何错误或外观偏差，后续2D精细化阶段可能产生伪影或无法有效纠正。论文明确指出，在极端视角变化（如大幅度旋转）下，3D LDM的质量可能下降，进而影响整体效果。

此外，与图像到视频方法的定量比较存在公平性隐患——生成帧可能与真实帧存在重叠（Sec. 4.3），这提示读者在解读相关指标时需保持审慎。

### 4. 开放问题

ScenDi为城市场景生成开辟了两条值得探索的后续路径：

- **规模扩展的潜力**：扩大训练数据和模型规模能否进一步提升原生3D场景生成的视觉质量，从而减轻对2D精细化阶段的依赖？当前的级联设计本质上是对3D生成能力不足的补偿策略，更强的3D基础模型可能改变这一架构权衡。

- **3D表征的进化空间**：如何将更强大的3D表征或生成模型整合到级联框架中？Voxel-to-3DGS VQ-VAE作为信息压缩的中间环节，其重建质量（受BCE损失、每体素高斯数量等因素影响，Table 2）直接决定了整个流程的性能上限，更优的3D表征有望系统性提升最终生成质量。

## 原文 PDF

![[paperPDFs/CVPR_2026/ScenDi_3D_to_2D_Scene_Diffusion_Cascades_for_Urban_Generation.pdf]]