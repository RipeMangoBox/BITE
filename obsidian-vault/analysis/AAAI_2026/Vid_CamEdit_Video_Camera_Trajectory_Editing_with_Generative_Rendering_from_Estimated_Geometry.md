---
title: "Vid-CamEdit: Video Camera Trajectory Editing with Generative Rendering from Estimated Geometry"
type: paper
paper_level: A
venue: AAAI
year: 2026
pdf_ref: paperPDFs/AAAI_2026/Vid_CamEdit_Video_Camera_Trajectory_Editing_with_Generative_Rendering_from_Estimated_Geometry.pdf
project_link: https://cvlab-kaist.github.io/Vid-CamEdit
code_link: null
aliases:
- VC
- Vid-CamEdit
tags:
- AAAI_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 引入时序一致的几何估计作为先验，将几何信息转化为2D流场，并以此为条件引导视频扩散模型的生成，同时通过分解式微调策略（空间块用多视图图像数据训练，时序块用视频数据训练）消除对4D训练数据的依赖。
primary_logic: 通过将4D动态场景合成问题分解为3D几何估计和1D时序生成，利用预估的时序一致几何计算2D流场，取代直接3D注入，使生成模型能够专注于合成几何不确定区域的真实细节，而分解式微调则进一步打破了4D训练数据瓶颈。
claims:
- 框架将任务分解为时序一致的几何估计和基于估计几何的生成式渲染，消除了对大规模4D训练数据的需求。
- 因子式微调策略允许分别利用多视角图像（3D）数据和视频数据训练，从而避免使用4D多视角视频。
- 在Neu3D和ST-NeRF等动态多视角数据集上，本文方法在LPIPS和帧一致性（CLIP score）指标上均优于所有基线方法。
- "Neu3D 上 LPIPS ↓ = 0.414"
---

# Vid-CamEdit: Video Camera Trajectory Editing with Generative Rendering from Estimated Geometry

> [!tip] 核心洞察
> 通过将4D动态场景合成问题分解为3D几何估计和1D时序生成，利用预估的时序一致几何计算2D流场，取代直接3D注入，使生成模型能够专注于合成几何不确定区域的真实细节，而分解式微调则进一步打破了4D训练数据瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | Vid-CamEdit: 基于估计几何的生成式渲染进行视频相机轨迹编辑 |
| 英文题名 | Vid-CamEdit: Video Camera Trajectory Editing with Generative Rendering from Estimated Geometry |
| 会议/期刊 | AAAI 2026 |
| Links | [paper](https://arxiv.org/abs/2506.13697) · [Project](https://cvlab-kaist.github.io/Vid-CamEdit) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Vid-CamEdit |
| Dataset | Neu3D, ST-NeRF dataset |

> [!tip] 效果简介
> - Neu3D 上，LPIPS ↓ 0.414 vs 0.562 (MonST3R all-frame reprojection) (-0.148)。
> - ST-NeRF dataset 上，Frame-Con. ↑ (CLIP score) 0.917 vs 0.757 (MonST3R all-frame reprojection) (+0.160)。

## 概要

**问题瓶颈**：在野生单目视频上进行大角度相机轨迹编辑面临两难困境。基于重建的方法依赖精确的3D几何重建，难以处理大规模视角变化带来的遮挡区域，导致生成结果出现大面积空洞；基于生成的方法则需要大量4D多视图视频作为训练数据，但真实4D数据极为稀缺，在合成数据上训练的模型存在显著的领域差距，难以泛化到真实场景。

**核心思路**：Vid-CamEdit 将4D动态场景合成问题分解为两个子任务——时序一致的3D几何估计和基于估计几何的1D时序生成。框架利用预估的时序一致几何计算2D流场，并以此为条件引导视频扩散模型的生成过程，使模型能够专注于合成几何不确定区域的真实细节。同时，通过**因子化微调策略**——空间块用多视图图像数据训练、时序块用视频数据训练、二者交替冻结——彻底消除了对4D多视图视频训练数据的依赖。

**方法定位**：Vid-CamEdit 属于几何接地（geometry-grounded）的视频到视频翻译框架。与直接注入3D点云或相机姿态的方法不同，它通过将几何信息转化为2D流场并重新对齐位置编码来实现隐式条件注入。其底层几何估计器基于 MonST3R，生成骨架基于 AnimateDiff（Stable Diffusion 1.5），并通过引入视频编码器（ReferenceNet 风格）将空间块改造为多视图块。

**主要结果**：在动态多视图数据集 Neu3D 和 ST-NeRF 上，Vid-CamEdit 在 LPIPS 和帧一致性（CLIP score）两项指标上均优于所有基线方法，包括基于重建的 MonST3R 重投影、Pseudo-DVS，以及基于生成的 Generative Camera Dolly。在野生视频的 VBench 评估中，该方法在美学质量和成像质量上大幅领先 Generative Camera Dolly。用户研究（59名参与者，双盲设计）进一步验证了其在输入一致性、视频真实感和相机轨迹忠实度上的综合优势。

### 视频相机轨迹编辑的需求与挑战

给定一段野生单目视频，用户常常希望改变其拍摄视角——例如将固定机位镜头变为缓慢推拉，或围绕场景主体进行旋转。这一任务被称为**视频相机轨迹编辑**（Video Camera Trajectory Editing），其核心目标是：输入一段视频 $\mathbf{X}$ 和一条期望的相对相机轨迹 $C_{\mathrm{rel}}$，合成一段新视频 $\mathbf{Y}$，使其既忠实于原始场景的动态内容与结构，又在视觉上真实自然，仿佛由新轨迹下的相机实际拍摄所得。

然而，实现这一目标面临根本性困难。当目标视角与原始视角差异较大时，场景中的大面积区域会因遮挡而变得不可见——这些区域在输入视频中从未出现过，却需要在新视频中被真实地填充。这一问题将视频相机轨迹编辑推向了**动态新视角合成**（Dynamic Novel View Synthesis）的核心挑战：如何在缺乏直接观测的情况下，生成时空一致的逼真内容。

### 现有方法的瓶颈

当前解决该问题的方法可大致分为两类，但各自存在显著局限：

**基于重建的方法**（Reconstruction-based）试图从输入视频中显式恢复场景的4D几何表示（如点云、NeRF或3D高斯），然后从新视角渲染。这类方法依赖精确的几何重建，但当视角变化增大时，遮挡区域缺乏对应观测，重建的几何必然不完整，导致渲染结果出现大面积空洞和失真。典型的基于重建方法如 **Pseudo-DVS**（在动态场景中采用深度重投影）和各类逐场景优化方法（如 **Shape-of-Motion**、**DyniBar**、**HyperNeRF**），在遮挡区域的生成质量上均受到几何重建精度的根本制约。

**基于生成的方法**（Generation-based）则利用生成模型的先验知识来“想象”遮挡区域的内容。例如 **Generative Camera Dolly (GCD)** 尝试直接使用视频扩散模型合成新视角视频。然而，这类方法面临严重的**4D训练数据瓶颈**：要学习动态场景的多视角一致性生成，理想情况下需要大规模的多视角视频数据（即同一动态场景从多个同步相机拍摄的视频），但真实世界中此类数据极为稀缺。现有方法不得不依赖合成数据（如Kubric-4D）进行训练，导致显著的**领域差距**（domain gap）——在合成数据上训练的模型难以泛化到真实野生视频，生成结果常呈现“合成感”外观，无法保持原始视频的真实质感。

### 核心洞察与动机

本文观察到，上述两类方法的困境源于一个共同的根本问题：**将4D动态场景合成视为一个不可分割的整体任务**。重建方法试图一次性解决几何与外观，却因几何不完整而失败；生成方法试图端到端学习4D生成，却受困于4D训练数据匮乏。

本文的核心洞察是：**将4D问题分解为3D几何估计与1D时序生成两个子问题**。具体而言：

- **3D几何估计**：利用现有的视频几何预测模型（如MonST3R）从输入视频中估计时序一致的点云和相机轨迹。这些几何信息虽然不完美（遮挡区域仍无法重建），但为生成模型提供了宝贵的场景结构先验。
- **1D时序生成**：将几何信息转化为2D流场，并以此为条件引导视频扩散模型的生成过程。生成模型不再需要从零开始“想象”场景结构，而是专注于合成几何不确定区域（遮挡区域）的真实细节，同时保持可见区域的几何一致性。

这一分解策略的关键优势在于：**几何估计与生成渲染各司其职**——几何模型提供结构骨架，生成模型填充视觉血肉。更重要的是，它打破了4D训练数据的依赖：通过**因子式微调策略**（Factorized Fine-tuning），模型的**空间块**（负责多视角一致性）可用多视角图像（3D）数据训练，**时序块**（负责运动连续性）可用常规视频数据训练，二者交替冻结、分别优化，从而完全避免了对4D多视角视频数据的需求。

### 方法定位

Vid-CamEdit 并非纯粹的生成方法，也非传统的重建方法，而是**几何接地**（Geometry-grounded）的生成式渲染框架。它利用预估的时序一致几何计算2D流场，通过流条件位置编码重新对齐视频编码器令牌，将几何先验隐式注入扩散模型的生成过程。这种设计使框架能够处理大角度相机轨迹编辑，同时保持生成内容的视觉真实性与时空一致性，在动态多视角数据集和野生视频上均展现出优于现有基线的性能。

## 核心方法与创新机理

Vid-CamEdit 的核心创新在于将4D动态场景的相机轨迹编辑任务分解为**时序一致的几何估计**与**基于估计几何的生成式渲染**两个子任务，并通过两个关键设计突破现有方法的瓶颈。

**创新一：以2D流场替代直接3D注入的几何接地机制**

现有基于重建的方法（如 MonST3R 直接重投影）在视角变化较大时会因遮挡产生大面积空洞和失真；基于生成的方法（如 **Generative Camera Dolly**，GCD）则缺乏几何约束，难以保持场景结构一致性。Vid-CamEdit 的解决方案是：将时序一致的几何估计（MonST3R 点云）投影为2D流场 $f_{\mathrm{rel}}$，并通过重新对齐视频编码器令牌的位置编码来实现隐式几何条件注入：

$$\mathrm{PE}'(u, v, t) = \mathrm{PE}(u + f_{\mathrm{rel}}(u, v, t)_x, v + f_{\mathrm{rel}}(u, v, t)_y, t)$$

这一设计将摄像机位姿、内参和3D几何信息全部隐含于2D流场中，使生成模型无需直接处理3D表示，却能获得精确的像素级对应关系。消融实验证实，该机制显著优于直接注入相机姿态（Plücker坐标嵌入）或重投影+修复的 naive 基线，LPIPS 降低约 0.084（Table 3）。

**创新二：因子化微调策略消除4D训练数据依赖**

现有生成式方法需要大规模4D多视角视频数据进行训练（如 Kubric-4D 合成数据集），但真实4D数据稀缺，合成数据存在显著领域差距。Vid-CamEdit 将视频扩散模型的空间块改造为多视角块（引入 ReferenceNet 风格的视频编码器注入空间注意层），并与时序块分离，采用交替冻结策略：**训练空间块时冻结时序块，使用多视角图像（3D）数据；训练时序块时冻结空间块，使用常规视频数据**。该策略从架构层面打破了4D训练数据瓶颈，使模型能够分别从丰富的3D多视角图像和视频数据中学习空间一致性与时序连贯性。

**两者的协同效应**：2D流场接地为生成提供了精确的几何引导，使模型能够专注于合成几何不确定区域（遮挡区域）的真实细节；因子化微调则确保了模型在不依赖4D数据的前提下，仍能生成时空一致的高质量新视角视频。这种“几何估计负责结构，生成模型负责纹理”的分工，是 Vid-CamEdit 在 LPIPS 和帧一致性（CLIP score）上全面超越所有基线方法（Table 1）的根本原因。

Vid-CamEdit 将视频相机轨迹编辑任务形式化为一个以几何为条件的视频到视频生成问题。给定一段单目输入视频 $\mathbf{X}$、一条用户指定的相对相机轨迹 $C_{\mathrm{rel}}$ 以及共享内参矩阵 $\mathbf{K}$，框架的目标是合成一段新视频 $\mathbf{Y}$，使得该视频在遵循目标相机运动的同时保持原始场景的结构与动态：

$$\mathbf{Y} = \mathcal{F}(\mathbf{X}, C_{\mathrm{rel}}, \mathbf{K}) \tag{1}$$

这一公式化的核心洞察在于：**框架接受自由形式的相机轨迹**，而不局限于预设轨迹类型，从而赋予用户对镜头运动的完全控制权。

### 两阶段分解架构

如图 3 所示，Vid-CamEdit 将上述合成问题分解为两个子任务，形成级联的流水线：

1. **时序一致的几何估计**：从输入视频中恢复动态场景的时序一致三维几何 $\mathcal{G}$ 及相机轨迹。框架默认采用 **MonST3R** 作为几何估计器，因其能够联合估计一致的相机轨迹与点云，且其动态区域分割机制可有效区分场景中的静态与动态元素。

2. **基于估计几何的生成式渲染**：以估计几何为条件，通过视频扩散模型生成符合目标相机轨迹的新视角视频。关键在于，框架并非直接将三维几何注入生成模型，而是将其转化为二维流场 $f_{\mathrm{rel}}$，并以此重新对齐视频特征令牌的位置编码，实现隐式的几何条件注入。

### 几何到生成的信息桥梁：二维流场

框架在几何估计与生成渲染之间建立了一座关键的信息桥梁——**相对二维流场**。对于每个像素 $(u, v)$ 和时刻 $t$，流场定义为：

$$f_{\mathrm{rel}}(u, v, t) = \Pi(C_{\mathrm{rel}}(t) \cdot \mathcal{G}(u, v, t), \mathbf{K}) - (u, v) \tag{3}$$

其中 $\Pi(\cdot)$ 为透视投影，$\mathcal{G}(u, v, t)$ 为估计的三维点云坐标。这一设计将相机位姿、内参和场景几何的全部信息压缩为像素级的二维位移向量，使生成模型仅需以流场为条件：

$$\mathcal{F}(\mathbf{X}, C_{\mathrm{rel}}, \mathbf{K}) := \mathrm{Sample}(p_{\theta}(\mathbf{Y} \mid \mathbf{X}, f_{\mathrm{rel}})) \tag{4}$$

**这一转换的深层动机**在于：直接使用三维几何（如点云重投影）会在遮挡区域产生大面积空洞，而将几何先验转化为流场后，生成模型可以专注于填补几何不确定区域的真实细节，从而规避了对精确完整几何重建的依赖。

### 生成模型中的几何接地机制

框架在视频扩散模型内部实现了两种互补的几何接地策略：

- **流条件位置编码重对齐**：根据流场 $f_{\mathrm{rel}}$ 平移标准正弦位置编码的坐标，使视频编码器提取的特征令牌在空间上与目标视角对齐：

  $$\mathrm{PE}'(u, v, t) = \mathrm{PE}\big(u + f_{\mathrm{rel}}(u, v, t)_x, v + f_{\mathrm{rel}}(u, v, t)_y, t\big) \tag{5}$$

- **视频编码器注入**：采用 ReferenceNet 风格的视频编码器提取输入视频的多尺度特征令牌，并将其注入扩散模型的空间注意层。这使得生成过程能够显式地参考原始视频的外观信息，与流条件形成互补。

### 因子化微调策略：打破4D数据瓶颈

传统生成式新视角合成方法依赖大规模4D多视角视频数据进行训练，但真实4D数据极为稀缺，合成数据训练又存在显著的领域差距。Vid-CamEdit 通过**因子化微调策略**（图 4）从根本上消除了这一依赖：

- 将视频扩散模型的**空间块改造为多视角块**，仅用多视角图像（3D）数据进行训练；
- **时序块**则用常规视频数据独立训练；
- 训练过程中交替冻结：训练多视角图像时冻结时序块，训练视频时冻结多视角块。

这一策略的核心思想是将4D动态场景学习分解为3D空间一致性和1D时序一致性的独立学习，使框架能够分别从丰富得多的多视角图像数据和视频数据中汲取知识，而无需任何4D多视角视频。

### 对纯深度几何模型的兼容性

当底层几何估计器仅输出深度图（如 DepthCrafter、Depth-Anything2）而非完整点云时，框架通过逆内参将深度提升为三维齐次坐标：

$$\mathcal{G} = h(\mathbf{K}^{-1} D_t), \quad \forall t \in [1, T] \tag{6}$$

这保证了框架对各类几何估计模型的广泛兼容性，消融实验（Table 4）也证实了不同几何模型下性能的高度一致性。

Vid-CamEdit 将视频相机轨迹编辑任务形式化为一个条件生成问题，其核心公式为：

$$\mathbf{Y} = \mathcal{F}(\mathbf{X}, C_{\mathrm{rel}}, \mathbf{K}) \tag{1}$$

其中 $\mathbf{X}$ 为输入单目视频，$C_{\mathrm{rel}}$ 表示用户指定的相对相机轨迹，$\mathbf{K}$ 为共享内参矩阵，$\mathbf{Y}$ 为合成的新视角视频。框架 $\mathcal{F}(\cdot)$ 需接受自由形式的相机轨迹，而非仅限预设轨迹。

### 3.1 时序几何估计与2D流场计算

框架将任务分解为两个子任务：**时序一致的几何估计**与**基于估计几何的生成式渲染**。几何估计模块采用 MonST3R，该模型通过联合估计一致的相机轨迹与点云（pointmaps），为后续生成提供时序稳定的3D先验。

为将3D几何信息注入2D视频扩散模型，本文提出以**2D流场**作为几何条件的载体。给定估计的时序一致点云 $\mathcal{G}(u, v, t)$ 和目标相机轨迹 $C_{\mathrm{rel}}(t)$，逐像素的相对流场定义为：

$$f_{\mathrm{rel}}(u, v, t) = \Pi(C_{\mathrm{rel}}(t) \cdot \mathcal{G}(u, v, t), \mathbf{K}) - (u, v) \tag{3}$$

该公式将3D点云经目标相机位姿变换后投影到图像平面，再减去原始像素坐标，得到每个像素从源视角到目标视角的2D位移向量。由此，生成过程被重新表述为仅以输入视频和2D流场为条件：

$$\mathcal{F}(\mathbf{X}, C_{\mathrm{rel}}, \mathbf{K}) := \mathrm{Sample}(p_{\theta}(\mathbf{Y} \mid \mathbf{X}, f_{\mathrm{rel}})) \tag{4}$$

摄像机位姿、内参和3D几何均隐含于流场 $f_{\mathrm{rel}}$ 中，生成模型无需直接处理3D表示。

当底层几何估计器仅输出深度图（如 DepthCrafter、Depth-Anything2）时，通过逆内参将2D像素提升为3D齐次坐标：

$$\mathcal{G} = h(\mathbf{K}^{-1} D_t), \quad \forall t \in [1, T] \tag{6}$$

### 3.2 流条件位置编码注入

为实现2D流场对视频扩散模型的条件引导，本文设计了**流条件位置重对齐**（Flow-Conditioned Positional Re-alignment）机制。具体而言，视频编码器（ReferenceNet风格）提取输入视频的特征令牌后，根据流场 $f_{\mathrm{rel}}$ 重新计算其正余弦位置编码：

$$\mathrm{PE}'(u, v, t) = \mathrm{PE}\big(u + f_{\mathrm{rel}}(u, v, t)_x, \; v + f_{\mathrm{rel}}(u, v, t)_y, \; t\big) \tag{5}$$

其中 $f_{\mathrm{rel}}(u, v, t)_x$ 和 $f_{\mathrm{rel}}(u, v, t)_y$ 分别为流向量在水平和垂直方向的分量。重对齐后的位置编码 $\mathrm{PE}'$ 替代原始位置编码，使扩散模型的空间注意层能够感知像素在新视角下的对应位置，从而隐式地利用几何先验指导遮挡区域的真实细节合成。

### 3.3 多视图空间块与因子化微调

视频扩散模型基于 AnimateDiff（Stable Diffusion 1.5 架构），包含空间块（spatial blocks）和时序块（temporal blocks）。为增强多视图一致性，本文将空间块改造为**多视图块**：引入视频编码器提取的输入视频特征令牌，注入空间注意层（架构细节见 Figure 12）。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2506_13697/figures/016_Figure_12.jpg]]
*Figure 12: Architecture. We provide a more detailed illustration of our architecture. In the video diffusion model, which consists of spatial and temporal blocks, we enhance the spatial block by integrating tokens provided by the video encoder, thereby transforming it into a multi-view block. The tokens encoded by the video encoder are concatenated as key and value inputs within the self-attention layers of the multi-view block in the video diffusion model*

为消除对4D多视角视频训练数据的依赖，本文提出**因子化微调策略**（Figure 4）：

- **空间块（多视图块）**：使用多视图图像（3D）数据训练，此时冻结时序块；
- **时序块**：使用常规视频数据训练，此时冻结多视图空间块。

通过交替冻结不同模块，模型分别从多视图图像中学习空间对应关系、从视频中学习时序动态，而无需任何4D多视角视频数据。这一设计打破了现有生成式方法（如 Generative Camera Dolly）对合成4D数据集（如 Kubric-4D）的依赖，显著缓解了合成数据到真实场景的领域差距问题。

## 实验与关键发现

### 主实验结果

Vid-CamEdit 在多视角动态数据集 Neu3D 和 ST-NeRF 上进行了定量评估，与几何重投影基线 MonST3R 、基于重建的 Pseudo-DVS 、基于生成的 Generative Camera Dolly (GCD) 以及 naive 的“重投影+视频修复”基线 进行了比较。由于 GCD 不接受移动摄像头视频，评估仅在静态摄像头视频数据集上进行，且相机位姿经过预处理对齐到 Kubric-4D 坐标系以保证公平性。

**Table 1** 展示了主实验结果。在 Neu3D 数据集上，Vid-CamEdit 的 LPIPS 达到 **0.414**，相比 MonST3R 全帧重投影的 0.562 降低了 **0.148**；在 ST-NeRF 数据集上，LPIPS 为 0.386，帧一致性（Frame-Con.，即输入视频与生成视频各帧之间的 CLIP score）达到 **0.917**，相比 MonST3R 的 0.757 提升了 **0.160**。Vid-CamEdit 在 LPIPS 和帧一致性两项指标上均优于所有基线方法。

定性比较如 **Figure 6** 所示，Vid-CamEdit 在合成视觉逼真图像的同时更好地保持了原始几何结构。MonST3R 重投影在大视角变化下产生大面积空洞，Pseudo-DVS 和 GCD 则分别因重建精度不足和合成数据训练的领域差距而产生模糊或合成感过强的结果。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2506_13697/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparisons with MonST3R [107], video inpainting [112] w/MonST3R, GCD (Generative Camera Dolly) [87], and Pseudo-DVS [110]. Ours is best in synthesizing visually realistic images while maintaining the original geometry*

在野生视频上的评估采用 VBench 基准，如 **Figure 8** 所示，Vid-CamEdit 在美学质量和成像质量上均大幅优于 Camera Dolly。这一性能差距主要源于 Camera Dolly 依赖合成数据（Kubric-4D）训练，在真实场景中产生明显的合成感输出，而 Vid-CamEdit 通过几何接地消除了这一领域差距。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2506_13697/figures/009_Figure_8.jpg]]
*Figure 8: Quantitative comparisons on Vbench [38] with Camera Dolly [87] on uncurated in-the-wild videos. Our approach substantially outperforms Camera Dolly in both aesthetic and imaging quality. The large performance gap comes from Camera Dolly’s synthetic-looking outputs*

### 相机轨迹难度分析

**Figure 9** 展示了不同相机轨迹难度下的性能比较。遵循 的评估方法，以输入视频与目标视频之间的 LPIPS 为“难度”（Difficulty），以生成视频与目标视频之间的 LPIPS 为“失真”（Distortion），绘制 Distortion-Difficulty 曲线。Vid-CamEdit 在所有难度级别上一致取得最优性能，表明框架对不同幅度的相机轨迹编辑均具有鲁棒性。

### 用户研究

如 **Figure 7** 所示，用户研究邀请了 59 名参与者，采用双盲设计（结果顺序随机打乱并匿名化），从三个维度评估：（a）与输入视频的一致性，（b）视频真实感，（c）对相机轨迹的忠实度。Vid-CamEdit 在所有三个维度上均显著优于对比方法。

### 应用：逐场景 4D 重建

作为下游应用，Vid-CamEdit 生成的视频可集成到基于优化的逐场景重建框架中。**Table 2** 展示了在 DyCheck 数据集上的 4D 逐场景重建结果。将 Vid-CamEdit 的输出整合到现有优化框架后，重建质量得到提升（∗ 表示在遮挡区域评估的复现结果）。与 Shape-of-Motion 、DyniBar 、HyperNeRF 等逐场景优化方法相比，Vid-CamEdit 辅助的重建在遮挡区域表现出更好的质量。**Figure 13** 提供了相应的定性结果。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2506_13697/figures/008_Table_2.jpg]]
*Table 2: Quantitative results of 4D per-scene reconstruction on DyCheck [20]. Employing our method to the existing per-scene reconstruction method yield better reconstruction quality. ∗ indicates the reproduced results for evaluation in occluded regions*

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2506_13697/figures/017_Figure_13.jpg]]
*Figure 13: Qualitative results of per-scene reconstruction with our method on DyCheck [20]. As an application, the outputs generated by our method can be integrated into optimization-based frameworks for per-scene reconstruction. This helps reduce artifacts in challenging novel views of dynamic 3D representations*

### 消融实验

#### 设计选择消融

**Table 3** 消融了框架的核心设计选择。完整框架（Ours）在 LPIPS（0.414）和 SSIM（0.358）上均取得最优结果。关键发现：

- **移除几何接地**（w/o geometry grounding）：仅保留视频编码器的空间注意机制但不使用 2D 流场重新对齐位置编码，LPIPS 显著恶化，表明几何接地是框架性能的核心贡献因素。
- **Plücker 坐标嵌入替代**：将 2D 流场条件替换为直接的 Plücker 坐标嵌入 来注入相机姿态信息，性能明显下降，验证了通过 2D 流场进行隐式几何条件注入优于直接 3D 注入。
- **重投影+视频修复基线**：naive 的“先重投影再修复”策略性能最差，说明简单地将几何估计与生成模型串联无法有效处理遮挡区域的真实感合成。

#### 几何估计模型消融

**Table 4** 消融了底层几何估计模型的选择。分别使用 MonST3R、DepthCrafter、Depth-Anything2 和 DepthAnyVideo 作为几何估计器 g，框架在 LPIPS 和 SSIM 上均表现出最小的性能差异。这表明 Vid-CamEdit 对几何估计模型的选择具有鲁棒性——只要提供时序一致的几何先验，框架就能有效利用。对于纯深度模型（DepthCrafter 等），通过逆内参将 2D 像素提升到 3D 齐次坐标获得几何 $\mathcal{G} = h(K^{-1} D_t)$（Eq. 6）。

### 失败模式与局限性

1. **几何估计依赖**：当底层几何估计出现严重错误时，生成结果的视觉质量可能下降。如 **Figure 15** 所示，MonST3R 的动态区域分割能有效捕捉主要动态物体，但可能遗漏细微的动态元素（如背景中其他人的运动）。本文通过扩散模型的隐式时序聚合部分缓解了这一限制，但并未完全解决。该问题与几何估计模型正交，随着几何估计技术的进步有望持续改善。

2. **生成长度限制**：当前模型一次仅生成 12 帧，对于更长时间的视频尚未验证。

3. **动态场景的隐式区分**：在含有大量动态物体的野生视频中，视频扩散模型的隐式时序聚合是否总能正确区分动静态区域仍是一个开放问题。当几何估计彻底失效时，框架缺乏显式的 fallback 机制来避免生成崩溃。

![[assets/figures/papers/paper_list_l13_https_arxiv_org_abs_2506_13697/figures/011_Figure_9.jpg]]
*Figure 9: Comparison on various camera trajectory. Following [71], we measure LPIPS between generated videos and target videos (Distortion) over LPIPS between input videos and target videos (Difficulty). Ours consistently achieves best performance*

## 定位与知识库关联

### 任务定位与核心瓶颈

Vid-CamEdit 解决的是**单目视频相机轨迹编辑**（video camera trajectory editing）问题：给定一段用户拍摄的单目视频 $\mathbf{X}$、一个目标相对相机轨迹 $C_{\mathrm{rel}}$ 和共享内参 $\mathbf{K}$，合成一段新视频 $\mathbf{Y}$，使其看起来像是从目标轨迹拍摄的同一动态场景。该问题的核心瓶颈在于：基于重建的方法（如重投影）依赖精确几何，但无法处理大规模视角变化带来的遮挡区域，导致生成结果出现大空洞；基于生成的方法（如 Generative Camera Dolly）需要大量 4D 多视图视频训练数据，而真实 4D 数据稀缺，合成数据训练存在显著的领域差距，难以泛化到真实场景。

Vid-CamEdit 的核心洞察是将 4D 动态场景合成问题**分解为 3D 几何估计和 1D 时序生成**：利用预估的时序一致几何计算 2D 流场，取代直接 3D 注入，使生成模型能够专注于合成几何不确定区域的真实细节；同时通过**因子式微调**（factorized fine-tuning）打破 4D 训练数据瓶颈。

### 方法谱系与基线关系

#### 基于重建的动态新视角合成

这类方法依赖精确的几何重建或逐场景优化来实现新视角渲染，但在大角度相机运动下受限于遮挡和几何估计误差。

- **MonST3R**（Zhang et al.）作为几何估计基线，通过对输入视频进行全局对齐，估计时序一致的点云和相机轨迹。其 all-frame reprojection 变体利用所有帧的点云和动态掩码进行重投影，在 Neu3D 上的 LPIPS 为 0.562，ST-NeRF 上的帧一致性 CLIP score 为 0.757（Table 1）。Vid-CamEdit 直接以 MonST3R 作为几何估计器，但其生成质量远超单纯重投影（LPIPS 降低约 0.148），说明**生成式渲染对几何估计的缺陷具有显著的补偿能力**。

- **Pseudo-DVS**（Kasten et al.）是一种基于重建的动态新视角合成方法，在定性比较中（Figure 6）其生成结果在遮挡区域出现明显伪影和结构失真，而 Vid-CamEdit 能合成视觉逼真的遮挡内容。

- **Shape-of-Motion**（Wang et al.）、**DyniBar**（Li et al.）和 **HyperNeRF**（Park et al.）均为基于优化的逐场景 4D 重建方法。在 DyCheck 数据集的 4D 逐场景重建实验中（Table 2），Vid-CamEdit 的输出被集成到现有优化框架后，在遮挡区域的 PSNR 和 SSIM 均优于这些方法，表明**生成先验可以有效补充优化重建在遮挡区域的不足**。

#### 基于生成的动态新视角合成

这类方法利用生成模型直接合成新视角，但受限于 4D 训练数据的稀缺和领域差距。

- **Generative Camera Dolly (GCD)**（Wang et al.）是基于生成的方法代表，使用 Kubric-4D 合成数据集训练。其核心局限在于：(1) 不接受移动摄像头视频输入，因此定量比较仅在静态摄像头数据集（Neu3D、ST-NeRF）上进行；(2) 合成数据训练导致严重的领域差距，在 VBench 真实视频上（Figure 8）的美学质量和成像质量远低于 Vid-CamEdit，表现为合成感强、细节丢失严重。Vid-CamEdit 通过几何接地和因子式微调，**消除了对 4D 合成数据的依赖**，从根本上解决了领域差距问题。

- **Reproj. + Inpainting**（视频修复基线）是一个朴素的两阶段方法：先用 MonST3R 重投影，再用视频修复模型填充空洞。Table 3 的消融实验表明，该基线的 LPIPS 远高于 Vid-CamEdit 的完整框架（差距约 0.084），说明**将几何信息通过 2D 流场隐式注入扩散模型的去噪过程**，比显式的“先投影再修复”策略更有效。

#### Vid-CamEdit 的关键技术差异

与上述方法相比，Vid-CamEdit 在三个关键设计槽位上做出了根本性改变：

1. **几何信息的注入方式**：基线方法直接使用估计的 3D 点云或深度图进行重投影，产生空洞和失真；Vid-CamEdit 将时序一致的几何投影为 2D 流场 $f_{\mathrm{rel}}$，并以此重新对齐视频编码器令牌的位置编码 $\mathrm{PE}'(u,v,t) = \mathrm{PE}(u + f_{\mathrm{rel}}(u,v,t)_x, v + f_{\mathrm{rel}}(u,v,t)_y, t)$，实现**隐式几何条件注入**。Table 3 的消融表明，这种流条件策略显著优于直接注入 Plücker 坐标嵌入。

2. **训练数据需求**：GCD 等方法依赖 4D 多视角视频数据（如 Kubric-4D）进行训练；Vid-CamEdit 通过因子式微调，仅需多视角图像（3D）和常规视频数据，**不依赖任何 4D 多视角视频**。具体而言，空间块（改造为多视图块）用多视角图像数据训练，时序块用视频数据训练，两者交替冻结。

3. **模型架构**：标准视频扩散模型（如 AnimateDiff）仅含文本条件；Vid-CamEdit 引入 ReferenceNet 风格的视频编码器，将输入视频特征令牌注入空间注意层，将空间块改造为多视图块，实现**输入视频条件与几何流条件的联合建模**。

### 适用边界与失效模式

#### 已知局限

1. **几何估计依赖性**：当底层几何估计出现严重错误时，生成结果的视觉质量可能下降。Table 4 的消融表明框架对几何模型选择具有一定鲁棒性（MonST3R、DepthCrafter、Depth-Anything2、DepthAnyVideo 均取得相近的 LPIPS 和 SSIM），但当几何估计彻底失效时，框架缺乏明确的 fallback 机制来避免生成崩溃。

2. **动态区域分割不精细**：MonST3R 的动态区域估计能捕获主要动态物体，但可能遗漏细微的动态元素（Figure 15 展示了此类失败案例）。Vid-CamEdit 通过扩散模型的隐式时序聚合部分缓解了这一限制，但在含有大量动态物体的复杂场景中，模型是否能始终正确区分动静态区域仍是开放问题。

3. **生成长度限制**：当前模型一次仅生成 12 帧（$T=12$），对于更长时间的视频尚未验证。扩展到数百帧的长视频生成需要解决时序一致性和计算效率的双重挑战。

#### 评估边界

- 定量比较仅在静态摄像头视频数据集（Neu3D、ST-NeRF）上进行，因为基线 GCD 不接受移动摄像头视频。在移动摄像头野生视频上的定量评估仍不充分。
- 用户研究（Figure 7）采用双盲设计，59 名参与者评估输入一致性、视频真实感和相机轨迹忠实度，但用户研究的规模和环境生态效度有限。

### 开放问题

1. **几何误差的量化影响**：如何量化几何估计误差对最终视频生成质量的影响？是否存在一个误差阈值，超过该阈值生成质量会急剧下降？

2. **动静态区域解耦**：在含有大量动态物体的野生视频中，视频扩散模型的隐式时序聚合是否总是能正确区分动静态区域？是否需要显式的动态区域建模？

3. **因子式微调的最优策略**：当前因子化微调中，空间块与时间块的交替冻结比例是固定的，是否可以进一步调整以获得更优性能？是否可以在微调后期进行联合微调？

4. **长视频扩展**：该方法是否能扩展到更长的视频生成（如数百帧）？需要什么样的时序建模机制来维持长程一致性？

5. **与其他几何估计器的协同进化**：本方法与几何估计模型正交，随着几何估计技术的进步（如更强的单目深度估计或 4D 重建模型），性能有望持续提升。但如何设计一个统一的接口，使得框架可以即插即用地适配未来的几何估计器，仍需进一步探索。

## 原文 PDF

![[paperPDFs/AAAI_2026/Vid_CamEdit_Video_Camera_Trajectory_Editing_with_Generative_Rendering_from_Estimated_Geometry.pdf]]
