---
title: "SceneMaker: Open-set 3D Scene Generation with Decoupled De-occlusion and Pose Estimation Model"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SceneMaker_Open_set_3D_Scene_Generation_with_Decoupled_De_occlusion_and_Pose_Estimation_Model.pdf
project_link: "https://idea-research.github.io/SceneMaker/"
code_link: null
aliases:
- SceneMaker
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将3D场景生成解耦为去遮挡、物体几何生成和姿态估计三个独立任务，并分别从大规模图像数据集、3D物体数据集和合成场景数据集中学习对应的先验；同时引入统一的扩散姿态估计模型，融合全局与局部自注意力和解耦的交叉注意力机制。
primary_logic: 解耦框架使每个任务能独立最大化其所需的开放集先验，避免任务间数据干扰导致的几何坍塌和姿态偏移；利用图像数据集增强去遮挡能力，并通过设计专门的注意力机制提升姿态估计的准确性和泛化性。
claims:
- 解耦去遮挡模型在10K图像数据集上微调后，PSNR达到15.03，显著优于Flux Kontext的13.91和BrushNet的11.07。
- 在严重遮挡的物体生成任务中，解耦方法在CD、F-Score和Volume IoU上均优于MIDI和Amodal3R。
- 统一姿态估计模型在室内和开放集测试集上均取得SOTA性能，CD-S低至0.0285。
- 全局/局部注意力机制和200K合成场景数据的加入可有效提升模型泛化能力，消融实验验证各模块均有正向贡献。
---

# SceneMaker: Open-set 3D Scene Generation with Decoupled De-occlusion and Pose Estimation Model

> [!tip] 核心洞察
> 解耦框架使每个任务能独立最大化其所需的开放集先验，避免任务间数据干扰导致的几何坍塌和姿态偏移；利用图像数据集增强去遮挡能力，并通过设计专门的注意力机制提升姿态估计的准确性和泛化性。

| 字段 | 内容 |
|------|------|
| 中文题名 | SceneMaker：基于解耦去遮挡与姿态估计模型的开放集3D场景生成 |
| 英文题名 | SceneMaker: Open-set 3D Scene Generation with Decoupled De-occlusion and Pose Estimation Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.10957) · [Project](https://idea-research.github.io/SceneMaker/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | SceneMaker |
| Dataset | De-occlusion validation set, 3D-Front occluded object test set, Open-set test set, MIDI test set |

> [!tip] 效果简介
> - De-occlusion validation set 上，PSNR 15.03 vs 13.91 (Flux Kontext) (+1.12)；SSIM 0.7566 vs 0.7309 (Flux Kontext) (+0.0257)；CLIP 0.2698 vs 0.2674 (Flux Kontext) (+0.0024)。
> - 3D-Front occluded object test set 上，CD 0.0409 vs 0.0443 (Amodal3R) (-0.0034)；F-Score 0.7454 vs 0.7124 (Amodal3R) (+0.033)；Volume IoU 0.5985 vs 0.5279 (Amodal3R) (+0.0706)。
> - Open-set test set (severe occlusions) 上，CD-S / F-Score-S / CD-O / F-Score-O / IoU-B 0.0285 / 0.6125 / 0.0671 / 0.5948 / 0.7549 vs Best existing method (numbers not listed) (Outperforms all competitors)。

## 概述

从单张RGB图像生成完整的三维场景是一项极具挑战的任务，其核心瓶颈在于**严重遮挡**与**开放场景**的双重压力：现有方法通常将去遮挡、几何生成与姿态估计耦合在有限的场景数据集上联合训练，导致各任务无法获取充足的开放集先验，进而产生几何坍塌与姿态偏移。SceneMaker 提出一种**解耦框架**，将3D场景生成拆分为三个独立任务——去遮挡、3D物体生成和姿态估计，使每个任务能够从最匹配的数据源中最大化其所需先验：去遮挡模型从大规模图像数据集中学习遮挡修复能力，3D生成模型利用多视角扩散先验重建规范空间几何，统一的姿态估计模型则通过全局/局部注意力机制从合成场景数据中学习物体间的空间关系。这一“分而治之”的策略使得框架在室内与开放集场景下均展现出显著的性能优势与泛化能力。

在定量评估中，SceneMaker 的去遮挡模型在10K图像数据集上微调后，PSNR 达到 15.03，优于 Flux Kontext 的 13.91 和 BrushNet 的 11.07；在严重遮挡下的3D物体生成任务中，其 CD、F-Score 和 Volume IoU 均超越 MIDI 与 Amodal3R；统一的姿态估计模型在室内和开放集测试集上取得 SOTA 性能，CD-S 低至 0.0285。消融实验进一步验证了全局/局部注意力机制以及200K合成场景数据对泛化能力的关键贡献。

## 背景与动机

3D场景生成旨在从单张RGB图像或文本描述中重建出包含多个物体的完整三维场景，是计算机视觉与图形学长期追求的目标，并在具身智能、虚拟现实和内容创作等领域具有广泛的应用前景。然而，真实世界的场景往往伴随着严重的物体间遮挡，且物体类别可能超出训练集的封闭词表，使得开放集（open-set）场景生成成为一个极具挑战性的问题。

现有方法在处理遮挡和开放集场景时面临一个根本性瓶颈：**缺乏足够的开放集先验（open-set priors）用于去遮挡（de-occlusion）和姿态估计**。Figure 2 清晰地揭示了这一困境——不同类型的先验（去遮挡先验、物体几何先验、姿态估计先验）需要从不同规模的数据集中获取，而现有方法的训练数据覆盖范围有限，无法同时满足所有先验的需求。具体而言：

- **耦合式方法的数据困境**：以 **MIDI**（Huang et al., arXiv 2024）为代表的端到端场景生成方法，将去遮挡、几何生成和姿态估计耦合在单一模型中，仅在有限的场景数据集（如3D-FRONT）上联合训练。这导致去遮挡能力受限于场景数据的规模，缺乏来自大规模图像数据集的开放集遮挡先验，在严重遮挡下几何质量显著下降。
- **重建式方法的泛化局限**：以 **InstPifu**（Liu et al., ECCV 2022）和 **Amodal3R**（Wu et al., arXiv 2025）为代表的重建方法，虽然可以处理部分遮挡，但其训练数据同样局限于特定域，难以泛化到开放集物体和场景。
- **生成式方法的姿态估计短板**：**DiffuScene**（Tang et al., CVPR 2024）和 **CAST3D**（Yao et al., arXiv 2025）等生成式方法在室内场景合成上取得了进展，但其姿态估计模块通常仅预测旋转和平移，缺少对物体尺寸的联合建模，且注意力机制未针对多物体场景的交互特性进行专门设计，导致姿态预测不够准确。

上述问题的本质在于：**不同任务所需的开放集先验天然存在于不同类型的数据集中**——去遮挡能力可以从大规模图像数据集中习得，物体几何先验蕴含于3D物体数据集，而场景级姿态估计则需要合成场景数据。耦合式的框架迫使所有任务共享同一训练数据分布，不可避免地造成先验获取的相互制约，最终表现为几何坍塌和姿态偏移。

针对这一洞察，SceneMaker 提出了一个**解耦框架**，将3D场景生成划分为三个独立任务：去遮挡、3D物体几何生成和姿态估计。其核心动机是让每个任务能够独立地从最适合的数据源中最大化其所需的开放集先验，从而突破耦合框架的数据瓶颈。具体而言：

1. **去遮挡解耦**：将去遮挡模型从3D生成模型中分离，使其能够基于大规模图像数据集（如Flux Kontext的预训练权重）进行微调，充分利用图像域的开放集遮挡先验。
2. **姿态估计增强**：设计统一的扩散姿态估计模型，联合预测旋转、平移和尺寸，并引入全局/局部自注意力和解耦的交叉注意力机制，使不同姿态变量能够关注最相关的条件信号。
3. **开放集数据扩充**：通过构建包含200K合成开放集场景的训练数据，显著扩展姿态估计模型的泛化能力。

这一解耦设计使得SceneMaker在严重遮挡和开放集场景下均能取得显著优于现有方法的性能，为开放集3D场景生成提供了新的技术路径。

## 核心创新

SceneMaker 的核心创新在于将开放集 3D 场景生成解耦为三个独立任务，并为每个任务设计专门的模型与数据策略，从而最大化各自所需的开放集先验，从根本上解决了现有耦合方法在严重遮挡和开放场景下几何质量差、姿态不准确的瓶颈。

**1. 解耦的去遮挡模型：从图像先验中学习开放集遮挡补全**

现有方法（如 **MIDI** (Huang et al., arXiv 2024)、**Amodal3R** (Wu et al., arXiv 2025)）通常将去遮挡与 3D 生成耦合，并在有限的场景数据集上联合训练，导致模型缺乏足够的开放集遮挡先验。SceneMaker 将去遮挡任务独立出来，基于 **Flux Kontext** (Black Forest Labs, arXiv 2025) 在精心构建的 10K 图像去遮挡数据集上微调，充分利用大规模图像数据集蕴含的丰富遮挡模式与物体外观先验。该数据集设计了三种遮挡模式（见 Figure 5），使模型能够处理从部分遮挡到严重遮挡的多样化场景。解耦后，去遮挡模型输出清晰的物体图像 $I^d$，为下游 3D 生成提供高质量条件，避免了耦合训练中因数据分布受限导致的几何坍塌。

**2. 统一的扩散姿态估计模型：解耦注意力机制与全参数预测**

传统姿态估计方法通常仅预测旋转和/或平移，且采用标准自注意力或交叉注意力，未针对场景生成任务中不同姿态变量的特性进行适配。SceneMaker 提出统一的扩散姿态估计模型，直接预测旋转 $R$、平移 $T$ 和尺寸 $S$ 的完整姿态参数，并引入解耦的注意力机制：
- **全局自注意力（GSA）** 使场景中所有物体的令牌相互交互，捕捉物体间的空间关系与布局约束；
- **局部自注意力（LSA）** 允许每个物体内部令牌独立建模，保持物体几何的局部一致性；
- **全局交叉注意力（GCA）** 使平移和尺寸令牌关注场景级条件（如深度点云、场景图像）；
- **局部交叉注意力（LCA）** 使旋转令牌独立关注物体规范空间条件（如规范几何 $O$、物体图像 $I$）。

这一设计（见 Figure 8）的核心洞察在于：旋转估计应聚焦于物体自身的几何特征，而平移和尺寸估计需要理解场景上下文与多物体交互。消融实验（Table 5）证实，移除 GSA 导致场景级 CD-S 从 0.0242 升至 0.0340，FS-S 从 0.7502 降至 0.6610；移除 LSA 使物体级 CD-O 从 0.0294 升至 0.0901，验证了解耦注意力设计的有效性。

**3. 开放集先验的数据策略：合成场景数据扩展泛化边界**

现有方法（如 **DiffuScene** (Tang et al., CVPR 2024)、**CAST3D** (Yao et al., arXiv 2025)）的姿态估计训练仅依赖有限域内的场景数据集（如 3D-FRONT），难以泛化至开放集物体。SceneMaker 混合 200K 基于 Objavaverse 物体的合成开放集场景与现有场景数据集，大幅扩展训练分布。配合 RoPE 位置编码，模型能够泛化至训练时未见过的 5 个以上物体的场景（Figure 11），在开放集测试集上取得 CD-S 0.0285 的 SOTA 性能（Table 3）。

**4. 解耦框架的系统性优势**

解耦设计的核心价值在于避免任务间数据干扰：去遮挡模型可独立利用图像数据集增强补全能力，3D 生成模型可专注于从清晰图像重建高质量几何，姿态估计模型可专注于从场景上下文中推理空间关系。这一策略使 SceneMaker 在严重遮挡的物体生成任务中，CD、F-Score 和 Volume IoU 均显著优于 MIDI 和 Amodal3R（Table 2），并在室内和开放集场景中一致超越现有方法（Table 3、Table 4）。

## 整体框架

SceneMaker 提出一种解耦的三维场景生成框架，将开放集场景生成分解为三个独立任务：场景感知、遮挡条件下的三维物体生成、以及统一姿态估计。该设计的核心动机在于：现有方法（如 **MIDI** (Huang et al., arXiv 2024)、**CAST3D** (Yao et al., arXiv 2025) 等）将去遮挡、几何重建和姿态估计耦合在有限域的场景数据集上联合训练，导致各任务无法充分获取所需的开放集先验，在严重遮挡和开放场景下几何质量差、姿态不准确。

SceneMaker 的解耦策略（Figure 3）使每个任务能独立最大化其先验来源：去遮挡模型从大规模图像数据集中学习遮挡先验，三维物体生成从三维物体数据集中学习几何先验，姿态估计从合成场景数据集中学习空间布局先验，从而避免任务间数据干扰导致的几何坍塌与姿态偏移。

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/003_Figure_3.jpg]]
*Figure 3: The Framework of SceneMaker. Our framework consists of scene perception, 3D object generation under occlusion, and pose estimation. We decouple the de-occlusion model from 3D object generation. We construct a unified pose estimation model that incorporates both global and local attention mechanisms. GSA, LSA, GCA, LCA, and FFN denote global self-attention, local self-attention, global cross-attention, local cross-attention, and feed-forward network, respectively*

### 场景感知

场景感知模块负责从输入场景图像中提取后续任务所需的基础信息。具体而言，利用 **Grounded-SAM** 生成场景中每个物体的分割掩码，并利用 **MoGe** 估计场景深度图，从而获得各物体的遮挡图像和对应的场景点云。这些输出构成去遮挡模型和姿态估计模型的条件输入。

### 遮挡条件下的三维物体生成

该阶段将传统耦合的去遮挡与三维重建拆分为两个序贯步骤：

1. **去遮挡模型**：基于 **Flux Kontext**（Black Forest Labs, arXiv 2025）进行微调，输入为遮挡图像 $I$ 和文本提示，通过扩散过程逐步去噪得到去遮挡后的清晰物体图像 $I^d$：
   $$\epsilon_{\theta}^{d}(I_{t}^{d}; t, I) \to I^{d}$$
   该模型在自行构建的 10K 图像去遮挡数据集上微调，数据集设计了三种精心构造的遮挡模式（Figure 5），以覆盖室内和开放集场景中的典型遮挡情况。由于解耦设计，去遮挡模型可充分利用 Flux Kontext 在大规模图像数据上预训练获得的开放集遮挡先验，这是耦合方法无法实现的。

2. **三维物体生成**：采用现成的多视角扩散模型（如 Step1x-3D），以去遮挡图像 $I^d$ 为条件，生成规范空间下的高质量三维几何 $O$：
   $$\epsilon_{\theta}^{o}(O_{t}; t, I^{d}) \to O$$
   去遮挡图像提供了完整、无遮挡的物体外观信息，使三维生成模型能够恢复更完整和精细的几何结构。

### 统一姿态估计模型

姿态估计模型以场景图像 $X$、物体掩码 $M$、物体图像 $I$、场景点云 $C$ 和规范几何 $O$ 为条件，通过扩散过程统一预测每个物体的旋转 $R$、平移 $T$ 和尺寸 $S$：
$$\epsilon_{\theta}^{p}(P_{t}; t, X, M, I, C, O) \to P, \quad P = \{R, T, S\}$$

该模型的核心创新在于引入全局与局部注意力机制（Figure 8）：
- **全局自注意力（GSA）**：使场景中所有物体的姿态令牌相互交互，捕获物体间的空间关系与布局约束。
- **局部自注意力（LSA）**：对单个物体内部的令牌进行独立建模，保持物体级几何一致性。
- **解耦交叉注意力**：旋转令牌通过局部交叉注意力关注物体规范空间条件，平移和尺寸令牌通过全局交叉注意力关注场景级条件，实现不同姿态变量与对应条件信息的精准对齐。

训练数据方面，除现有场景数据集外，还混合了基于 **Objaverse** 物体构建的 200K 合成开放集场景数据，以扩展模型对开放集物体的泛化能力。训练时对输入网格的俯仰角进行随机化处理，以更好地对齐三维物体生成模块的输出分布。

### 场景合成

最终，将生成的三维几何与估计的姿态参数组合，得到完整且一致的三维场景。整个框架从单张场景图像出发，通过解耦的模块化设计，实现了从二维感知到三维场景的端到端重建。

### 补充图表

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/002_Figure_2.jpg]]
*Figure 2: The analysis of prior sources in different methods. The table shows that the availability of required open-set priors (column) varies across different datasets (row). Paths in different colors represent various scene generation methods. Existing methods (yellow path and green path) lack sufficient open-set priors for de-occlusion and pose estimation due to the limited datasets. We further leverage image datasets for de-occlusion and collect new scene datasets for pose estimation to achieve better open-set performance(red path)*

## 核心模块与公式推导

SceneMaker 将开放集 3D 场景生成解耦为三个独立任务：去遮挡、3D 物体生成和姿态估计。这一解耦设计的核心动机在于，不同任务所需的开放集先验来源截然不同——去遮挡需要大规模图像先验，3D 物体生成需要规范空间的几何先验，而姿态估计需要场景级的多物体交互先验。耦合训练会迫使模型在有限且单一的数据分布中同时学习所有先验，导致几何坍塌和姿态偏移。解耦后，每个模块可独立从最匹配的数据集中最大化其先验学习，从而在严重遮挡和开放场景下获得更强的泛化能力。

### 去遮挡扩散模型

去遮挡模块的目标是从被遮挡的物体图像中恢复出完整的清晰物体外观。给定场景感知阶段获得的遮挡图像 $I$（由 Grounded-SAM 提取的物体掩码与原始场景图像合成），去遮挡模型通过扩散过程逐步去噪，生成去遮挡后的清晰图像 $I^d$：

$$
\epsilon_{\theta}^{d}(I_{t}^{d}; t, I) \to I^{d}
$$

其中 $\epsilon_{\theta}^{d}$ 为去遮挡扩散模型的噪声预测网络，$I_{t}^{d}$ 为时间步 $t$ 处的带噪潜变量，$I$ 为输入的遮挡图像条件。该模型基于 **Flux Kontext**（Black Forest Labs, 2025）进行微调，训练数据为专门构建的 10K 图像去遮挡数据集，包含三种精心设计的遮挡模式（随机遮挡、物体间遮挡和场景边界遮挡）。通过在图像层面独立处理去遮挡，模型得以充分利用 Flux Kontext 在大规模图像数据上习得的开放集遮挡先验，而非受限于 3D 场景数据集的有限分布。

### 3D 物体生成

获得去遮挡图像 $I^d$ 后，3D 物体生成模块以该清晰图像为条件，在规范空间中生成高质量的 3D 几何 $O$：

$$
\epsilon_{\theta}^{o}(O_{t}; t, I^{d}) \to O
$$

其中 $\epsilon_{\theta}^{o}$ 为 3D 生成扩散模型，$O_{t}$ 为时间步 $t$ 处的带噪 3D 表示。该模块采用现成的多视角扩散模型（如 Step1x-3D），以去遮挡图像作为条件输入。这一设计的优势在于：去遮挡模型已将遮挡区域的视觉信息补全，3D 生成模型无需同时处理遮挡推理和几何重建，只需专注于从完整外观到规范几何的映射，从而显著降低任务难度并提升几何质量。

### 统一姿态估计扩散模型

姿态估计模块以场景级条件为输入，同时预测所有物体的旋转 $R$、平移 $T$ 和尺寸 $S$。其扩散过程可统一表述为：

$$
\epsilon_{\theta}^{p}(P_{t}; t, X, M, I, C, O) \to P, \quad P = \{R, T, S\}
$$

其中 $P_t$ 为时间步 $t$ 处的带噪姿态参数，条件包括：场景图像 $X$、物体掩码 $M$、去遮挡后的物体图像 $I$、场景点云 $C$（由 MoGe 深度估计获得）以及规范空间的物体几何 $O$。模型直接对旋转、平移和尺寸施加 L2 损失，各分量等权重优化。

该模型的核心创新在于引入了**全局与局部解耦的注意力机制**（见 Figure 8）：
- **全局自注意力（GSA）** 使场景中所有物体的姿态令牌相互交互，建模物体间的空间关系约束；
- **局部自注意力（LSA）** 在每个物体内部独立建模，保持单物体姿态的内部一致性；
- **局部交叉注意力（LCA）** 使旋转令牌仅关注物体规范空间的条件（如物体图像和规范几何），确保旋转预测与物体自身几何对齐；
- **全局交叉注意力（GCA）** 使平移和尺寸令牌关注场景级条件（如场景图像和点云），确保物体在场景中的位置和尺度合理。

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/009_Figure_8.jpg]]
*Figure 8: Attention mechanisms in the pose estimation model. The global self-attention module enables tokens of all objects in the scene to interact with each other. The local cross-attention module enables rotation tokens independently interact with conditions in the object canonical space. The global cross-attention module enables translation and size tokens attend to scene-level conditions*

这种解耦的注意力设计使不同姿态变量能够聚焦于最相关的条件信号：旋转依赖物体自身几何，平移和尺寸依赖场景上下文。此外，模型采用 RoPE 位置编码，使其能够泛化至训练时未见过的多物体场景（超过 5 个物体），消融实验证实了这一设计的有效性。

## 实验与分析

### 瓶颈定位与因果机制

SceneMaker 的核心实验设计围绕一个明确瓶颈展开：现有方法在严重遮挡和开放场景下，缺乏足够的开放集先验用于去遮挡和姿态估计，导致几何质量差、姿态不准确。因果上，论文通过将 3D 场景生成解耦为去遮挡、3D 物体几何生成和姿态估计三个独立任务，使每个任务能独立最大化其所需的开放集先验，避免任务间数据干扰导致的几何坍塌和姿态偏移。实验部分通过去遮挡评估、遮挡下物体生成评估、姿态估计评估和完整场景生成评估，逐环节验证了这一因果链条。

### 去遮挡模型评估

解耦去遮挡模型在 10K 图像数据集上微调后，在去遮挡验证集上取得 PSNR 15.03，显著优于 Flux Kontext 的 13.91（+1.12）和 BrushNet 的 11.07（+3.96）（Table 1）。SSIM 达到 0.7566，CLIP 相似度达到 0.2698，均优于所有基线。定性结果（Figure 6）表明，在严重遮挡条件下，解耦模型能够恢复更完整的物体纹理和结构，尤其在开放集物体上优势明显。这一结果验证了核心洞察：利用大规模图像数据集（而非有限的场景数据集）学习去遮挡先验，是提升遮挡鲁棒性的关键因果旋钮。

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/006_Figure_6.jpg]]
*Figure 6: Qualitative comparison of de-occlusion models. Our model has better performance on both indoor and open-set objects, especiallt under severe occlusion*

### 遮挡下 3D 物体生成评估

在 3D-Front 遮挡物体测试集上，SceneMaker 在 CD（0.0409）、F-Score（0.7454）和 Volume IoU（0.5985）上均优于 **Amodal3R**（Wu et al., arXiv 2025）和 **MIDI**（Huang et al., arXiv 2024）（Table 2）。Volume IoU 提升最为显著（+0.0706），表明解耦去遮挡后生成的几何体在体积完整性上有实质改善。定性对比（Figure 7）显示，SceneMaker 生成的物体几何更完整、细节更丰富，尤其在室内和开放集物体的严重遮挡场景下。

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/008_Figure_7.jpg]]
*Figure 7: Qualitative comparison of object generation under occlusion. Our model has more complete and detailed geometry on both indoor and open-set objects*

### 统一姿态估计模型评估

统一姿态估计模型在室内和开放集测试集上均取得 SOTA 性能（Table 3）。在开放集测试集（严重遮挡）上，CD-S 低至 0.0285，F-Score-S 达到 0.6125，IoU-B 达到 0.7549，全面超越现有方法。在 MIDI 测试集上（Table 4），SceneMaker 同样取得最优结果（CD-S 0.051，F-Score-S 0.5642，IoU-B 0.671）。这些结果表明，引入全局/局部自注意力和解耦交叉注意力机制，使模型能够有效建模多物体交互并精确估计旋转、平移和尺寸，是实现开放集泛化的关键设计。

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/014_Table_4.jpg]]
*Table 4: Quantitative comparison on MIDI test set [22]*

### 消融实验

消融实验（Table 5）系统验证了各模块的因果贡献：

- **移除全局自注意力（GSA）**：CD-S 从 0.0242 升至 0.0340，FS-S 从 0.7502 降至 0.6610，表明物体间交互对姿态估计至关重要。
- **移除局部自注意力（LSA）**：CD-O 从 0.0294 升至 0.0901，FS-O 从 0.8121 降至 0.7142，说明独立物体建模直接影响几何精度。
- **移除局部交叉注意力（LCA）**：各项指标小幅下降（CD-S 0.0274，FS-S 0.7368），但仍支持解耦设计的有效性。
- **使用完整点云（+Complete points）**：性能接近上界（CD-S 0.0064，FS-S 0.9197），揭示当前点云质量（来自 MoGe 深度估计）是系统的主要瓶颈。
- **物体数量泛化**（Figure 11）：得益于 RoPE 位置编码，姿态估计模型能够泛化至训练时未见过的 5 个以上物体的场景。

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/015_Figure_11.jpg]]
*Figure 11: Ablation on the number of objects in the scene*

### 失败模式与局限性

尽管实验结果整体积极，但存在若干值得注意的失败模式：

1. **点云质量瓶颈**：消融实验中完整点云带来的巨大性能提升表明，当前使用的 MoGe 深度估计在遮挡严重区域可能失效，直接限制了姿态估计的上限。
2. **物理合理性缺失**：当前框架尚未处理物体间的物理交互（如穿透、力的作用），生成的场景可能存在物理不协调。
3. **3D 生成模型上限**：3D 物体生成的质量受限于底层生成模型（如 Step1x-3D），在面对极度复杂或罕见物体时可能出现几何缺陷。
4. **域迁移风险**：合成数据集虽能提升泛化能力，但与真实世界图像分布存在差距，可能导致域迁移问题。部分基线（如 **CAST3D**，Yao et al., arXiv 2025）缺乏公开的预训练模型和代码，可能影响部分指标的公平对比。

### 关键图表结论

- **Table 1 & Figure 6**：解耦去遮挡模型在定量和定性上均优于耦合基线，验证了大规模图像先验的有效性。
- **Table 2 & Figure 7**：遮挡下物体生成质量显著提升，Volume IoU 改善最为突出。
- **Table 3 & Table 4**：统一姿态估计模型在多个测试集上取得 SOTA，开放集泛化能力得到验证。
- **Table 5**：消融实验确认了全局/局部注意力和解耦交叉注意力的正向贡献，同时揭示了点云质量的瓶颈效应。
- **Figure 11**：RoPE 使模型能够泛化至更多物体的场景，验证了位置编码设计的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/001_Figure_1.jpg]]
*Figure 1: Our method not only achieves superior performance in both indoor and open-set scenarios but also demonstrates stronger generalization across synthetic and real-world captured images*

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/012_Figure_10.jpg]]
*Figure 10: Qualitative comparison with scene generation methods*

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/017_Figure_13.jpg]]
*Figure 13: Qualitative comparison with scene generation methods on indoor scenes*

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/005_Figure_5.jpg]]
*Figure 5: The occlusion patterns of de-occlusion datasets*

![[assets/figures/papers/paper_list_l2589_https_arxiv_org_abs_2512_10957/figures/010_Figure_9.jpg]]
*Figure 9: The samples of collected open-sest dataset*

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

现有的3D场景生成方法可大致分为两类路径：一类以 **MIDI** (Huang et al., arXiv 2024) 为代表，直接在有限的3D场景数据集上联合学习场景布局和物体几何；另一类以 **CAST3D** (Yao et al., arXiv 2025) 为代表，尝试在开放集中生成场景，但将去遮挡、几何生成和姿态估计耦合在统一的框架内。这两种路径面临一个共同的瓶颈：**严重遮挡和开放场景下缺乏足够的开放集先验**。具体而言，去遮挡任务需要理解物体在各类遮挡模式下的完整外观，而姿态估计任务需要感知多物体间的空间交互和场景级上下文。当这些任务被耦合训练于规模有限的场景数据集（如3D-FRONT）时，模型难以获得泛化到开放世界所需的丰富先验，导致几何坍塌和姿态偏移。

SceneMaker 的核心洞察在于：**不同的子任务所需的最优先验来源是异构的**。去遮挡的先验天然存在于大规模图像数据集中，3D几何的先验存在于3D物体数据集中，而姿态估计的先验则需要从包含丰富物体交互的场景数据中习得。将这三个任务解耦，使每个任务能独立最大化其所需的开放集先验，是突破上述瓶颈的关键因果杠杆。

### 2. 与基线方法的关系与差异化

#### 2.1 去遮挡：从耦合到解耦

在耦合框架中，去遮挡能力受限于场景数据集的规模和多样性。SceneMaker 将去遮挡模型从3D生成流程中完全解耦，基于 **Flux Kontext** (Black Forest Labs, arXiv 2025) 在大规模图像数据上预训练的开放集先验，并在自行构建的10K图像去遮挡数据集上微调。该数据集设计了三种遮挡模式（见 Figure 5），覆盖室内和开放集物体。Table 1 的定量结果显示，解耦后的去遮挡模型在PSNR上达到15.03，显著优于Flux Kontext的13.91和 **BrushNet** (Ju et al., ECCV 2024) 的11.07，验证了“图像先验+针对性微调”策略的有效性。

#### 2.2 姿态估计：从分离预测到统一扩散

现有方法通常仅预测旋转和/或平移，缺少尺寸预测，或未针对场景生成任务进行适配。SceneMaker 提出**统一的扩散姿态估计模型**，将旋转 $R$、平移 $T$ 和尺寸 $S$ 联合建模为扩散过程的去噪目标：

$$\epsilon_{\theta}^{p}(P_{t}; t, X, M, I, C, O) \to P, \quad P = \{R, T, S\}$$

该模型的核心创新在于**注意力机制的解耦设计**（见 Figure 8）：
- **全局自注意力（GSA）**：使场景中所有物体的token相互交互，捕捉多物体间的空间关系。
- **局部自注意力（LSA）**：在每个物体内部独立建模，保持物体级表示的完整性。
- **解耦的交叉注意力**：旋转token通过局部交叉注意力关注物体规范空间条件（物体图像、规范几何），而平移和尺寸token通过全局交叉注意力关注场景级条件（场景图像、掩码、点云）。

Table 3 和 Table 4 的结果表明，该模型在室内和开放集测试集上均取得SOTA性能，开放集场景下的CD-S低至0.0285。消融实验（Table 5）进一步证实：移除GSA导致CD-S从0.0242升至0.0340，移除LSA使CD-O从0.0294升至0.0901，验证了注意力解耦设计的必要性。

#### 2.3 数据策略：合成数据驱动的开放集泛化

与仅使用有限域内场景数据集训练姿态估计的基线方法不同，SceneMaker 混合了200K基于Objaverse物体构建的合成开放集场景数据。这一策略显著扩展了模型在开放词表物体和多样化场景布局上的泛化能力。此外，模型采用RoPE位置编码，使其能够泛化至训练时未见过的5个以上物体的场景（见 Figure 11）。

### 3. 适用边界与局限

尽管SceneMaker在多项指标上取得了显著提升，其方法仍存在以下适用边界和局限：

1. **物理合理性缺失**：当前框架尚未处理物体间的物理交互（如穿透、力的相互作用），生成的场景可能存在物理不协调。这是一个系统级局限，而非单一模块的缺陷。

2. **点云质量瓶颈**：姿态估计模型严重依赖输入点云的质量。当前使用的MoGe深度估计在严重遮挡区域可能失效，限制了整体性能上限。Table 5 中“使用完整点云”的实验（CD-S 0.0064, FS-S 0.9197）揭示了点云质量是当前系统的主要瓶颈。

3. **3D生成模型的上限约束**：3D物体生成的质量受限于底层多视角扩散模型（如Step1x-3D），在面对极度复杂或罕见物体时可能出现几何缺陷。SceneMaker的解耦设计虽能最大化去遮挡先验，但无法超越生成模型本身的固有能力边界。

4. **合成-真实域迁移**：合成数据集（Objaverse）虽能提升泛化能力，但与真实世界图像分布存在差距，可能导致域迁移问题。Table 3 和 Table 4 的跨数据集评估部分缓解了这一担忧，但尚未完全解决。

5. **控制粒度有限**：对控制信号和自然语言交互的支持有限，需要进一步发展以支持更细粒度的场景编辑。

### 4. 开放问题与未来方向

1. **高层场景理解**：如何在生成的3D场景上进行关系推理、功能识别等高层理解任务，并将其应用于具身智能体的决策制定？

2. **多视图/视频输入融合**：能否通过多视图或视频输入进一步提升去遮挡和姿态估计的鲁棒性，特别是在极端遮挡条件下？

3. **端到端联合优化**：在解耦框架下，能否实现端到端的联合优化，以进一步减小任务间信息损失？当前各模块独立训练，可能存在信息传递的次优性。

4. **物理属性扩展**：除旋转、平移和尺寸外，能否引入更丰富的物理属性（如质量、材质）以实现更真实的场景仿真？

5. **极端泛化边界**：对于类别极度不平衡或新颖物体，当前模型的泛化边界在哪里？如何安全地扩展到任意开放词表？这需要更系统的分布外评估协议。

### 5. 知识库定位

SceneMaker 的核心贡献在于**方法论的解耦范式和注意力机制的针对性设计**，而非单一模块的颠覆性创新。其去遮挡模型建立在Flux Kontext的预训练基础之上，3D生成模型沿用现有多视角扩散框架，姿态估计模型采用扩散范式但引入了新颖的全局/局部注意力解耦机制。该工作在以下知识节点上具有参考价值：

- **3D场景生成的解耦范式**：为后续研究提供了“按先验来源拆解任务”的方法论参考。
- **扩散模型在姿态估计中的应用**：展示了扩散模型在联合预测旋转、平移和尺寸方面的有效性，以及注意力解耦对多变量预测的增益。
- **合成数据增强策略**：基于Objaverse构建开放集场景数据的pipeline（见 Figure 9）可作为相关任务的数据增强参考。

## 原文 PDF

![[paperPDFs/CVPR_2026/SceneMaker_Open_set_3D_Scene_Generation_with_Decoupled_De_occlusion_and_Pose_Estimation_Model.pdf]]