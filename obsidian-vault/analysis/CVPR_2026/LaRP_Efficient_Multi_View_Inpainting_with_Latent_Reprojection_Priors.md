---
title: "LaRP: Efficient Multi-View Inpainting with Latent Reprojection Priors"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LaRP_Efficient_Multi_View_Inpainting_with_Latent_Reprojection_Priors.pdf
project_link: null
code_link: null
aliases:
- LLRP
- LaRP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过3D基础模型估计的显式几何对应将参考视图的外观潜变量重投影至目标视图，在预训练扩散修复模型中进行跨视图条件化。
primary_logic: 将预训练扩散修复模型的生成先验与3D基础模型的显式几何对应相结合，通过潜在空间重投影机制实现高效的多视图一致性修复，消除了对后优化的依赖。
claims:
- LaRP在多视图一致性指标MEt3Rm上达到0.1109，略优于MVInpainter-F的0.1113。
- LaRP训练收敛速度比ControlNet基线快约3.5倍（2,000步 vs 7,000步）。
- LaRP结合NeRF在SPIn-NeRF数据集上FID达到34.84（20分钟训练），优于MVInpainter-F的37.97，且速度快约50倍。
- 消融实验证实潜在空间重投影优于像素空间替代方案，且保留预训练生成先验对性能至关重要。
---

# LaRP: Efficient Multi-View Inpainting with Latent Reprojection Priors

> [!tip] 核心洞察
> 将预训练扩散修复模型的生成先验与3D基础模型的显式几何对应相结合，通过潜在空间重投影机制实现高效的多视图一致性修复，消除了对后优化的依赖。

| 字段 | 内容 |
|------|------|
| 中文题名 | LaRP：基于潜在重投影先验的高效多视图图像修复 |
| 英文题名 | LaRP: Efficient Multi-View Inpainting with Latent Reprojection Priors |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_LaRP_Efficient_Multi-View_Inpainting_with_Latent_Reprojection_Priors_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LaRP (Latent Reprojection Priors) |
| Dataset | SPIn-NeRF, 360-USID, LaRP模型训练 |

> [!tip] 效果简介
> - SPIn-NeRF 上，MEt3Rm↓ (多视图一致性) 0.1109 vs 0.1113 (MVInpainter-F) (-0.0004)；MEt3Rm↓ (结合NeRF) 0.0978 vs 0.1109 (仅LaRP) (-0.0131)。
> - SPIn-NeRF (NVS) 上，FID↓ (20分钟训练) 34.84 vs 37.97 (MVInpainter-F) (-3.13)。
> - 360-USID 上，训练时间（分钟） 27 vs 85 (AuraFusion360) (~3× faster)。

## 概要

### 问题瓶颈

多视图图像修复（multi-view inpainting）要求从不同视角去除目标物体后生成视觉一致、几何连贯的填补内容。现有方法面临一个核心矛盾：**依赖后优化（如 SPIn-NeRF）的方法计算开销巨大，而依赖隐式运动线索（如光流）的方法缺乏显式 3D 几何对应，难以保证跨视图一致性**。这导致修复结果在不同视图间出现纹理错位、语义断裂，且处理效率低下——单场景优化动辄需要数十分钟甚至更长时间。

### 核心方法

**LaRP（Latent Reprojection Priors）** 提出了一种新的解决路径：将预训练扩散修复模型的生成先验与 3D 基础模型估计的显式几何对应相结合。其关键操作是在潜在空间中进行**重投影**——利用 3D 基础模型（VGGT）从参考视图估计的相机位姿和深度，将参考视图的多尺度外观潜变量精确映射到目标视图，再注入到冻结的扩散修复 UNet 中进行条件化去噪。这一设计使得模型无需后优化即可直接输出多视图一致的修复结果。

### 方法定位

LaRP 在方法谱系中处于**单视图扩散修复**与**多视图后优化**的交叉地带。它继承了 **Stable Diffusion Inpainting**（Rombach et al., CVPR 2022）的强生成先验，但通过克隆 UNet 编码器并引入零初始化卷积的特征注入层，实现了跨视图条件化——这与 **ControlNet**（Zhang et al., 2023）在像素空间进行条件化的思路形成鲜明对比。相较于 **MVInpainter-F** 的单阶段多视图修复和 **SPIn-NeRF**（Mirzaei et al., 2023）、**MALD-NeRF**（Lin et al., ECCV 2024）等后优化方案，LaRP 在效率与质量之间取得了显著突破。

### 主要结果

在 SPIn-NeRF 数据集上，LaRP 的多视图一致性指标 MEt3Rm 达到 **0.1109**，略优于 MVInpainter-F 的 0.1113（Tab. 1）。结合 NeRF 进行新颖视图合成时，仅需 **20 分钟训练**即可达到 FID **34.84**，优于 MVInpainter-F 的 37.97，且速度提升约 **50 倍**（Tab. 2, Fig. 1）。在训练效率方面，LaRP 仅需 **14 小时（单张 RTX 4090）**，而 MVInpainter-F 需要 3 天（8×A100），收敛步数也快约 **3.5 倍**（Tab. 4）。消融实验进一步证实：潜在空间重投影显著优于像素空间替代方案，且保留预训练生成先验对性能至关重要（Tab. 5）。

![Figure 1]()

![Figure 2]()

![Figure 3]()

### 问题背景：多视图修复中的一致性与效率困境

在3D场景编辑、物体移除和内容补全等应用中，多视图图像修复（multi-view inpainting）要求从多个视角对同一场景的缺失区域进行填充，且修复结果必须在不同视图间保持几何与外观一致性。传统方法通常采用“先修复后优化”的范式：先对单张视图独立进行2D修复，再通过后优化（如NeRF训练）来弥合视图间的不一致。然而，这种策略面临两个根本性挑战：

1. **一致性不可靠**：单视图修复模型（如**LaMa**（Suvorov et al., WACV 2022）或**Stable Diffusion Inpainting**（Rombach et al., CVPR 2022））缺乏跨视图感知能力，独立修复必然产生语义冲突和纹理错位，后优化只能事后弥补，无法从根本上保证一致性。
2. **效率低下**：后优化方法（如**SPIn-NeRF**（Mirzaei et al., 2023）、**MALD-NeRF**（Lin et al., ECCV 2024））通常需要数小时的逐场景优化，限制了实际部署的可行性。

### 现有方法缺口：缺乏显式几何引导的生成先验融合

近年来，研究者尝试将扩散模型的生成先验引入多视图修复。**MVInpainter-F** 等单阶段方法试图在修复过程中隐式学习跨视图一致性，但其依赖大规模多视图训练数据（需3天×8张A100 GPU训练），且缺乏对显式3D几何对应的利用。另一类方法则依赖光流等隐式运动线索进行视图间信息传递，但这些线索在遮挡或纹理缺乏区域往往不可靠。

核心瓶颈在于：**现有方法未能将预训练扩散修复模型的生成先验与3D基础模型提供的显式几何对应有效结合**。扩散模型拥有强大的图像生成能力，3D基础模型（如VGGT）可估计可靠的相机姿态和几何结构，但二者在现有工作中处于割裂状态——要么仅使用扩散先验而忽略几何约束，要么依赖几何优化而牺牲生成质量。

### 本文动机：潜在空间重投影驱动的跨视图条件化

本文提出**LaRP（Latent Reprojection Priors）**，其核心动机是回答一个关键问题：**能否利用显式3D几何对应，在扩散模型的潜在空间中直接实现跨视图外观信息传递？**

这一思路的因果逻辑在于：如果能在预训练修复UNet的去噪过程中，将参考视图的多尺度外观潜变量通过3D几何关系重投影至目标视图，则可以将生成先验与几何一致性统一在同一个前向推理框架内，从而消除对后优化的依赖。具体而言，LaRP通过以下机制实现突破：

- **显式几何引导**：利用3D基础模型估计的相机姿态和深度信息，将参考视图潜变量构建为3D特征点云，再根据目标视图像素坐标进行重投影，确保跨视图信息传递的几何正确性。
- **生成先验保留**：通过克隆预训练UNet编码器处理参考视图，并在潜在空间（而非像素空间）进行重投影，最大程度保留扩散模型的生成能力，避免了像素空间重投影带来的信息损失。
- **高效训练范式**：设计可扩展的数据流水线，从视频数据集中自动生成两视图训练对，使LaRP可在单张RTX 4090 GPU上约14小时完成训练，较MVInpainter-F提速约5倍。

这种设计使得LaRP在多视图一致性和新视图合成质量上达到或超越现有最优方法，同时将逐场景处理速度提升约50倍（见图1），显著推进了质量-效率的帕累托前沿。

## 核心方法与创新机理

LaRP 的核心创新在于**将预训练扩散修复模型的生成先验与 3D 基础模型的显式几何对应深度融合**，通过潜在空间重投影机制实现高效的多视图一致性修复。与现有方法相比，LaRP 在以下关键维度实现了突破：

### 1. 显式几何引导替代隐式运动线索

现有方法（如基于光流的隐式运动线索或后优化策略）缺乏利用显式 3D 几何对应直接引导多视图一致性修复的能力。LaRP 引入 3D 基础模型（VGGT）估计的相对相机姿态，将参考视图的外观潜变量**几何重投影**至目标视图，为跨视图条件化提供了可靠、可解释的显式引导信号。这一设计消除了对后优化的依赖，从根本上改变了多视图修复的范式。

### 2. 潜在空间重投影机制

LaRP 的关键架构创新在于**克隆 UNet 编码器提取参考视图的多尺度外观潜变量**，并在潜在空间而非像素空间执行重投影。具体而言：
- 参考视图通过冻结参数的预训练 UNet 输入卷积层直接编码为潜变量（$t=0$），充分复用预训练生成先验；
- 将参考视图的 3D 点坐标与对应多尺度潜变量特征组成特征点云：$\{ (\mathbf{P}_{\mathrm{ref}}(p), \mathcal{F}_{\mathrm{ref}}(p)) \mid p \in \Omega \}$；
- 利用估计的相机姿态将特征点云重投影至目标视图坐标：$p' \sim \mathbf{K} (\mathbf{R} P_{p} + \mathbf{t})$；
- 重投影后的多尺度特征通过零初始化卷积层注入主 UNet 解码器，实现跨视图条件化。

消融实验证实，潜在空间重投影显著优于像素空间替代方案，且保留预训练生成先验对最佳性能至关重要（Table 5）。

### 3. 与 ControlNet 类架构的本质差异

相比朴素 ControlNet 跨视图条件化方案，LaRP 做出了两项关键改进（Figure 3）：
- **复用预训练输入卷积层**：ControlNet 使用额外的零卷积层处理重投影图像，而 LaRP 直接复用预训练扩散模型的输入卷积层，使参考视图编码从一开始就具备有意义的特征表示；
- **注入前重投影**：LaRP 仅在将跨视图信息注入修复模型之前执行重投影，避免了在像素空间进行冗余的编解码操作。

这些设计差异带来了显著的训练效率提升：LaRP 收敛仅需约 2,000 步，而 ControlNet 基线需要约 7,000 步，速度提升约 3.5 倍（Table 4）。

### 4. 可扩展的两视图训练数据流水线

针对现有数据集缺乏大规模两视图修复训练数据的问题，LaRP 提出了一套可扩展的数据生成流水线：
- 基于视频 3D 物体检测数据集（Objectron），通过**最远点采样（FPS）视角选择**自动选取基线合适的视角对；
- 配合**3D 感知掩膜生成**策略，产生部分遮挡掩膜以保留上下文信息。

该流水线使 LaRP 能够在单张 RTX 4090 GPU 上仅用 14 小时完成训练，而 MVInpainter-F 需要 8 张 A100 GPU 训练 3 天——训练效率提升约 5 倍，且所需计算资源大幅降低（Table 4）。

### 创新总结

LaRP 的创新本质在于**将 3D 几何显式建模与 2D 生成先验在潜在空间深度融合**，通过“克隆编码器—几何重投影—零初始化特征注入”的架构设计，实现了多视图修复在一致性、效率和质量三个维度的同步突破。这一设计使 LaRP 在帕累托前沿上显著推进了质量-效率的平衡边界（Figure 1），在 SPIn-NeRF 数据集上结合 NeRF 仅需 20 分钟训练即可达到 FID 34.84，优于 MVInpainter-F 的 37.97，且速度快约 50 倍。

LaRP 的整体设计围绕一个核心洞察展开：**将预训练扩散修复模型的生成先验与 3D 基础模型的显式几何对应相结合**，通过潜在空间重投影机制实现高效的多视图一致性修复，从而消除对后优化的依赖。其 pipeline 由两条并行的信息流构成，最终在去噪 UNet 的解码器中汇合。

### 信息流架构

**目标视图流**：待修复的目标视图经过 VAE 编码后，与掩膜 $\mathbf{M}$ 和噪声潜变量 $\mathbf{Z}_{t}$ 通道级联，形成基础修复模型的输入 $\mathbf{X}_{t} \in \mathbb{R}^{H \times W \times 9}$（Eq. 1）。该输入进入参数冻结的预训练修复 UNet 进行去噪。

**参考视图流**：参考视图同样经 VAE 编码，与零掩膜 $\mathbf{M}_{0}$ 和干净潜变量 $\mathbf{Z}_{0}$ 级联为 $\mathbf{X}_{\mathrm{ref}}$（Eq. 2），送入一个**克隆的 UNet 编码器**。该编码器从预训练修复 UNet 中复制权重而来，作为可训练的副本，且始终在时间步 $t=0$ 下运行，以提取参考视图的干净外观潜变量。此设计的关键在于：它直接复用了预训练扩散模型的输入卷积层和编码器权重，使得参考特征从一开始就具备有意义的语义表示，而非从零学习。

### 潜在重投影与特征注入

克隆编码器提取的多尺度潜变量特征与 3D 基础模型（VGGT）估计的相机位姿和深度共同构成**3D 特征点云**（Eq. 3）。对于参考视图中的每个像素 $p$，其 3D 坐标 $\mathbf{P}_{\mathrm{ref}}(p)$ 与对应的多尺度潜变量 $\mathcal{F}_{\mathrm{ref}}(p)$ 绑定。随后，利用相对相机位姿 $[\mathbf{R} \mid \mathbf{t}]$ 和内参 $\mathbf{K}$，将这些 3D 点重投影至目标视图像素坐标 $p'$（Eq. 4），从而将参考视图的外观潜变量精确地映射到目标视图的对应位置。

重投影后的特征通过**零初始化卷积层**注入到主 UNet 解码器的各个尺度。这种注入方式确保了训练初期重投影特征不会干扰预训练模型的生成先验，随着训练推进逐步学习有效的跨视图融合。

### 与 ControlNet 的关键差异

Fig. 3 明确对比了 LaRP 与朴素 ControlNet 在跨视图条件化上的概念差异。ControlNet 将重投影后的图像作为额外条件，通过独立的零卷积编码器分支处理；而 LaRP 则在**潜在空间**而非像素空间进行重投影，且重投影发生在特征注入之前。这意味着 LaRP 充分利用了预训练扩散模型已有的编码能力，避免了对重投影图像的二次编码，从而保留了更完整的生成先验。

### 数据流水线

训练 LaRP 需要大规模的两视图修复对，而现有数据集缺乏此类数据。为此，作者提出了一个可扩展的数据流水线（Fig. 2b），从视频 3D 目标检测数据集中自动生成训练对。该流水线包含两个关键组件：

1. **FPS 视角选择**：通过最远点采样（Eq. 5）从视频轨迹中选取空间均匀的相机帧子集，确保参考视图与目标视图之间具有合理的基线。
2. **3D 感知掩膜生成**：利用 3D 标注信息生成部分遮挡掩膜，在保留足够上下文的同时创建有意义的修复任务。

整个训练在单张 NVIDIA RTX 4090 GPU 上完成，仅需约 14 小时，相比 MVInpainter-F 的 3 天（8×A100）训练效率提升约 5 倍。

![[assets/figures/papers/paper_list_l891_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_LaRP_Efficient_M/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our contributions. (a) LaRP effectively combines priors from both a cross-view reference and a diffusion-based inpainting model by feeding the inpainting model with multi-scale appearance latents reprojected according to the 3D attributes estimated by a 3D foundation model. (b) Training LaRP requires a corpus of two-view image pairs that current datasets lack, we propose a scalable data pipeline to provide such image pairs by repurposing an existing video 3D object detection dataset. We use a FPS-based view selection heuristic with a 3D-aware mask generation process to prepare two-view image pairs with reasonable baselines and plausible masks*

LaRP 的核心架构由四个紧密协作的模块构成，其设计哲学在于**最大化复用预训练扩散模型的生成先验**，同时通过显式几何对应实现跨视图信息的高效注入。

### 基础修复模型输入

基础修复模型采用预训练的 Stable Diffusion Inpainting UNet（参数冻结），其输入由三部分通道级联构成：

$$\mathbf{X}_{t} = [\mathbf{I}, \mathbf{M}, \mathbf{Z}_{t}] \in \mathbb{R}^{H \times W \times 9}$$

其中 $\mathbf{I}$ 为掩膜图像的潜变量（4 通道），$\mathbf{M}$ 为下采样后的二值掩膜（1 通道），$\mathbf{Z}_{t}$ 为时间步 $t$ 的噪声潜变量（4 通道）。三者沿通道维度拼接，形成 9 通道输入张量。

### 克隆 UNet 编码器与参考视图编码

LaRP 的核心创新在于**克隆预训练 UNet 的编码器**作为可训练的参考视图特征提取器，而非引入全新的条件化网络。该克隆编码器接收参考视图的对应输入：

$$\mathbf{X}_{\mathrm{ref}} = [\mathbf{I}_{\mathrm{ref}}, \mathbf{M}_{0}, \mathbf{Z}_{0}] \in \mathbb{R}^{H \times W \times 9}$$

关键设计点如下：

- **时间步固定为零**：克隆编码器始终在 $t = 0$ 运行，使用干净潜变量 $\mathbf{Z}_{0}$ 和全零掩膜 $\mathbf{M}_{0}$，确保提取的是参考视图的完整外观信息。
- **复用预训练输入卷积层**：与 ControlNet 使用额外的零卷积层处理重投影图像不同，LaRP 直接复用预训练扩散模型的输入卷积层（Fig. 3 左侧），使得参考视图编码从一开始就享有良好的特征初始化。
- **参数冻结策略**：原始 UNet 的所有参数被锁定，仅克隆编码器和后续的零初始化卷积注入层参与训练，保护了预训练生成先验不被破坏（消融实验证实解锁 UNet 解码器会导致性能退化）。

### 潜在重投影模块

这是 LaRP 实现跨视图一致性的**因果机制核心**。具体流程如下：

1. **3D 特征点云构建**：克隆编码器提取参考视图的多尺度外观潜变量 $\mathcal{F}_{\mathrm{ref}}$，结合 3D 基础模型（VGGT）估计的像素级深度，将每个像素 $p$ 提升为 3D 点，形成特征点云：

   $$\{ (\mathbf{P}_{\mathrm{ref}}(p), \mathcal{F}_{\mathrm{ref}}(p)) \mid p \in \Omega \}$$

   其中 $\mathbf{P}_{\mathrm{ref}}(p)$ 为参考视图坐标系下的 3D 点坐标，$\Omega$ 为参考视图的有效像素域。

2. **几何重投影**：利用 VGGT 估计的相对相机姿态 $(\mathbf{R}, \mathbf{t})$ 和内参 $\mathbf{K}$，将 3D 点投影至目标视图像素坐标：

   $$p' \sim \mathbf{K} (\mathbf{R} P_{p} + \mathbf{t})$$

   此过程在潜在空间执行，而非像素空间。消融实验（Tab. 5）证实，**潜在空间重投影显著优于像素空间替代方案**，因为前者保留了预训练 VAE 的紧凑表示能力，避免了像素域重投影带来的信息损失和模糊。

3. **多尺度特征注入**：重投影后的多尺度潜变量通过零初始化卷积层注入主 UNet 的解码器各层级。零初始化确保训练初期注入信号为零，使模型平稳地从单视图修复过渡到跨视图条件化修复。

### 训练数据流水线

LaRP 的训练需要大规模两视图图像对，现有数据集缺乏此类标注。为此，作者提出可扩展的数据流水线（Fig. 2b），包含两个关键组件：

- **FPS 视角选择**：从视频序列的相机轨迹 $\mathcal{T}$ 中，通过最远点采样迭代选取空间分布均匀的帧子集：

  $$\mathbf{T}_{i+1} = \underset{\mathbf{T}_{j} \in \mathcal{T} \setminus \mathcal{S}_{i}}{\arg \max} \left( \underset{\mathbf{T}_{k} \in \mathcal{S}_{i}}{\min} d(\mathbf{T}_{j}, \mathbf{T}_{k}) \right)$$

  其中 $d(\cdot, \cdot)$ 为相机位姿间的距离度量，$\mathcal{S}_{i}$ 为已选帧集。该策略确保训练对具有合理的基线宽度和足够的视图重叠。

- **3D 感知掩膜生成**：利用 3D 物体标注生成部分遮挡掩膜，保留足够上下文信息以供模型学习跨视图对应关系。消融实验（Tab. 5f）表明，去除 FPS 视角选择导致一致性指标 MEt3Rm 从 0.1109 退化至 0.1245，验证了该组件的重要性。

### 与 ControlNet 的关键差异

Fig. 3 揭示了 LaRP 与朴素 ControlNet 在跨视图条件化上的两个根本区别：

1. **特征提取位置**：ControlNet 在像素空间对重投影图像使用额外的零卷积层编码；LaRP 则在潜在空间直接复用预训练模型的输入卷积层，充分利用已有的生成先验。
2. **重投影时机**：ControlNet 先重投影后编码；LaRP 先编码后重投影，使得重投影操作在紧凑的潜在特征空间进行，避免了像素域插值带来的伪影。

这种设计使 LaRP 的训练收敛速度比 ControlNet 基线快约 3.5 倍（2,000 步 vs 7,000 步，Tab. 4），同时取得了更优的修复质量。

## 实验与关键发现

### 多视图一致性评估

LaRP在SPIn-NeRF数据集上进行了多视图一致性评估，指标MEt3Rm和MEt3RR在所有可能的60张修复图像对上取平均。如表1所示，LaRP在MEt3Rm上达到0.1109，略优于单阶段方法MVInpainter-F的0.1113；结合NeRF进行后优化后，LaRP+NeRF进一步将MEt3Rm降至0.0978，体现了显式几何对应引导对跨视图一致性的增益。定性结果（图4）展示了3个场景中6个视图的直接修复效果：非参考方法LaMa和LDM在修复区域产生明显的不一致纹理，而LaRP借助两个参考视图的潜在重投影，在关键区域（黄色放大框）保持了清晰且一致的细节。

### 新颖视图合成质量与效率

将修复后的图像用于NeRF训练以合成新颖视图时，LaRP展现出显著的质量-效率优势。在SPIn-NeRF数据集上（表2），LaRP仅需20分钟NeRF训练即可达到FID 34.84，优于MVInpainter-F的37.97，且比先前最佳方法MALD-NeRF（Lin et al., ECCV 2024）快约50倍。在LPIPS指标上，LaRP同样具备竞争力。图5的定性对比显示，LaRP合成的新颖视图在细节保留和一致性方面与耗时更长的SOTA方法相当，而训练时间从数十分钟级降至20分钟。在360-USID数据集上（表3），LaRP以27分钟完成训练，相比AuraFusion360（Wu et al., CVPR 2025）的85分钟实现了约3倍加速。

### 训练效率

LaRP的训练效率优势显著（表4）。在单个NVIDIA RTX 4090 GPU上，LaRP仅需14小时完成训练，而MVInpainter-F需要3天（8×A100 GPU），实际加速比超过5倍且GPU需求大幅降低。与标准的ControlNet跨视图条件化架构相比，LaRP收敛仅需约2,000步，而ControlNet基线需要约7,000步（约3.5倍加速）。这一效率增益源于LaRP复用了预训练UNet的输入卷积层和编码器参数，使得参考视图特征在训练伊始即具有语义意义。

### 消融实验

表5的系统消融揭示了架构和数据流水线各组件的贡献：

**跨视图条件化架构**：跨注意力变体（b）无法有效学习，MEt3Rm高达0.1735，表明在潜在空间进行显式几何重投影比依赖注意力学习跨视图对应更为可靠。像素空间重投影替代方案（c）性能显著下降，证实了在潜在空间保留预训练生成先验对修复质量至关重要。解锁UNet解码器参数（d）导致性能退化，说明冻结原始UNet参数是维持生成先验完整性的关键设计选择。

**数据流水线组件**：去除FPS视角选择（f）使MEt3Rm从0.1109退化至0.1245，验证了基于最远点采样的视角选择策略对生成合理基线训练对的重要性。值得注意的是，仅使用单类别数据训练（h）即可达到MEt3Rm 0.1174，接近全量数据的0.1109，表明LaRP的几何引导机制对类别变化具有一定鲁棒性。

### 失败模式与局限性

尽管LaRP在多数场景中表现优异，但分析揭示了若干边界情况。首先，基础扩散模型（Stable Diffusion）的VAE在处理密集文本图案等细粒度纹理时存在编码瓶颈，可能导致修复区域纹理模糊或失真。其次，性能受限于3D基础模型VGGT的估计精度：在遮挡严重或纹理缺乏的场景中，几何估计误差会通过重投影传播至修复结果。此外，当前训练数据仅来自Objectron数据集的物体类别，泛化到全新场景类别时可能面临领域偏移。方法要求至少两个具有足够重叠的输入视图，极端宽基线场景下的表现仍需进一步验证。

![[assets/figures/papers/paper_list_l891_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_LaRP_Efficient_M/figures/001_Figure_1.jpg]]
*Figure 1: Quality to efficiency comparison among SOTA multiview inpainting methods. LaRP significantly advances the Pareto front. Reported times reflect per-scene process time, excluding one-time generalizable 2D model pre-training*

![[assets/figures/papers/paper_list_l891_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_LaRP_Efficient_M/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison of multi-view consistency. Metrics are averaged over all possible pairs among 60 inpainted images across all scenes from the SPIn-NeRF dataset*

![[assets/figures/papers/paper_list_l891_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_LaRP_Efficient_M/figures/008_Table_2.jpg]]
*Table 2: Quantitative comparison of novel view synthesis on the SPIn-NeRF dataset. LaRP achieves state-of-the-art performance on FID metrics and is highly competitive on LPIPS, while being significantly faster than the prior best-performing method MALD-NeRF [38]. ■ Best results. ■ Second-best results*

![[assets/figures/papers/paper_list_l891_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_LaRP_Efficient_M/figures/010_Table_5.jpg]]
*Table 5: Ablations on architecture design and data pipeline components. Please refer to Sec. 4.3 for detailed discussions*

![[assets/figures/papers/paper_list_l891_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_LaRP_Efficient_M/figures/011_Table_4.jpg]]
*Table 4: Training efficiency comparison. LaRP is significantly more efficient than prior SOTA and standard baselines*

## 定位与知识库关联

### 多视图修复方法谱系

LaRP 处于多视图图像修复（multi-view inpainting）这一交叉领域，其设计同时触及二维扩散修复、三维感知场景补全和基于先验的新视图合成三条技术路线。

**二维修复基线**。在最底层，LaRP 继承并冻结了预训练扩散修复模型 **Stable Diffusion Inpainting (LDM)**（Rombach et al., CVPR 2022）的生成先验。与之对比的单视图方法 **LaMa**（Suvorov et al., WACV 2022）仅依赖单帧上下文，缺乏跨视图一致性机制，在多视图场景中不同视角的修复结果彼此独立，无法保证三维连贯性。

**后优化路线**。**SPIn-NeRF**（Mirzaei et al., 2023）代表了一类重要的技术路径：先对每个视图独立修复，再通过 NeRF 训练过程中的后优化（post-hoc optimization）强制多视图一致性。这条路线的问题在于效率——后优化计算开销大，且独立修复阶段产生的 artifacts 难以在后优化中完全消除。**MALD-NeRF**（Lin et al., ECCV 2024）将扩散先验引入 NeRF 优化过程，在质量上取得进展，但效率瓶颈依然存在。LaRP 的因果调节变量——显式几何对应的潜在重投影——使得多视图一致性可以在单次前向传播中实现，从而绕过了后优化的计算开销。实验表明，LaRP 结合 NeRF 在 SPIn-NeRF 数据集上仅需 20 分钟训练即达到 FID 34.84，优于 MVInpainter-F 的 37.97，且比 MALD-NeRF 快约 50 倍（Tab. 2, Fig. 1）。

**单阶段多视图修复路线**。**MVInpainter-F** 是直接与 LaRP 竞争的单阶段方法，通过隐式运动线索实现跨视图信息传递。LaRP 在多视图一致性指标 MEt3Rm 上达到 0.1109，略优于 MVInpainter-F 的 0.1113（Tab. 1），同时在训练效率上具有数量级优势——LaRP 在单张 RTX 4090 上训练 14 小时，而 MVInpainter-F 需要 8 张 A100 训练 3 天（Tab. 4）。

**360 度场景修复**。**AuraFusion360**（Wu et al., CVPR 2025）专注于 360 度场景修复，在 360-USID 数据集上，LaRP 以 27 分钟训练时间达到竞争性能，比 AuraFusion360 的 85 分钟快约 3 倍（Tab. 3）。

### 跨视图条件化架构的定位

LaRP 与 **ControlNet**（Zhang et al., 2023）在跨视图条件化架构设计上形成关键差异。ControlNet 的朴素应用是将重投影后的图像作为额外条件，通过零卷积层注入主 UNet，这需要从零开始学习将像素空间的重投影图像映射到有意义的特征表示。LaRP 的核心设计选择在于：1）复用预训练扩散模型的输入卷积层和编码器来编码参考视图，而非使用独立的零卷积层；2）在潜在空间而非像素空间执行重投影，仅在注入前进行几何变换。这一设计保留了预训练生成先验的完整性，使得训练收敛速度比 ControlNet 基线快约 3.5 倍（2,000 步 vs 7,000 步，Tab. 4）。消融实验进一步证实潜在空间重投影优于像素空间替代方案，且解锁 UNet 解码器参数会导致性能退化（Tab. 5, Sec. 4.3）。

### 适用边界与局限

LaRP 的有效性依赖于以下前提条件，这些条件界定了其适用边界：

1. **几何估计精度**。潜在重投影的质量受限于 3D 基础模型（VGGT）的估计精度。在遮挡严重或纹理缺乏的场景中，几何估计误差会通过重投影传播，导致跨视图特征注入出现偏移。这是方法的内在瓶颈，而非实现细节问题。

2. **VAE 编码瓶颈**。基础扩散模型（Stable Diffusion）的 VAE 在处理密集文本图案等细粒度纹理时存在编码-解码瓶颈，可能导致修复后的纹理模糊或失真。这一问题继承自预训练模型，非 LaRP 架构本身所能解决。

3. **训练数据领域偏移**。当前训练数据来自 Objectron 数据集，覆盖特定物体类别。消融实验表明使用单类别数据即可接近全量数据性能（MEt3Rm 0.1174 vs 0.1109，Tab. 5h），说明模型对类别变化具有一定鲁棒性，但泛化到全新场景类别时性能可能下降。

4. **视图重叠要求**。方法需要至少两个有足够重叠的视图输入。FPS 视角选择策略（Eq. 5）旨在确保合理的基线距离，但对于稀疏或极端宽基线场景，重投影覆盖区域不足，修复质量受限。Fig. 6 展示了宽基线场景下的定性结果，LaRP 仍具竞争力但性能差距收窄。

### 开放问题

1. **精细纹理的编码瓶颈**。如何解决基础 VAE 对密集文本图案等精细纹理的编码失真？可能的路径包括微调 VAE 解码器或引入高频残差补偿机制，但需避免破坏预训练先验。

2. **更先进的 3D 基础模型集成**。当前依赖 VGGT 进行几何估计，集成更先进的模型如 MASt3R 或 Fast3R 是否能进一步提升几何精度和修复质量？这需要评估模型替换对重投影误差和最终修复指标的影响。

3. **开放域场景泛化**。如何将 LaRP 推广到更广泛的开放域场景，减少对特定物体类别数据集的依赖？数据流水线的可扩展性（Sec. 3.2）提供了基础，但需要更大规模、更多样化的视频数据源。

4. **不确定区域的自适应处理**。重投影过程中存在几何不确定区域（如遮挡边界、深度不连续处），是否可以通过在线优化或自适应机制动态调整这些区域的特征融合权重？当前方法对所有重投影特征等同对待，缺乏不确定性感知能力。

## 原文 PDF

![[paperPDFs/CVPR_2026/LaRP_Efficient_Multi_View_Inpainting_with_Latent_Reprojection_Priors.pdf]]
