---
title: "ShapeR: Robust Conditional 3D Shape Generation from Casual Captures"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ShapeR_Robust_Conditional_3D_Shape_Generation_from_Casual_Captures.pdf
project_link: null
code_link: null
aliases:
- ShapeR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 引入稀疏SLAM点云作为全局几何先验，结合多视角图像和文本描述的多模态输入，使模型无需显式分割即可隐式感知目标物体边界；同时通过大规模在机增强和两阶段课程训练（先在合成物体级数据上广泛增强，再在合成场景数据上微调），显著提升对真实世界复杂性的泛化能力。
primary_logic: 稀疏SLAM点云提供的全局几何信息与多视图图像、文本描述互补，校正流变换器可以利用这些多模态线索去噪并生成度量一致且完整的物体形状，而无需显式分割；两阶段训练和复杂增强策略进一步确保了模型对随意采集场景的鲁棒性。
claims:
- 引入稀疏SLAM点云作为互补模态，显著提升重建鲁棒性，Chamfer Distance从无点云的4.514降至2.375。
- 在机点云增强和图像增强对真实场景表现至关重要，移除任一项都会导致性能明显下降。
- 两阶段课程训练显著提升鲁棒性，仅物体级预训练而不进行场景微调CD为3.053。
- 2D点云掩码提示用于引导DINOv2特征，减少了相邻物体混淆，提升重建精度。
---

# ShapeR: Robust Conditional 3D Shape Generation from Casual Captures

> [!tip] 核心洞察
> 稀疏SLAM点云提供的全局几何信息与多视图图像、文本描述互补，校正流变换器可以利用这些多模态线索去噪并生成度量一致且完整的物体形状，而无需显式分割；两阶段训练和复杂增强策略进一步确保了模型对随意采集场景的鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | ShapeR：面向随意采集序列的鲁棒条件三维形状生成 |
| 英文题名 | ShapeR: Robust Conditional 3D Shape Generation from Casual Captures |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.11514) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | ShapeR |
| Dataset | ShapeR Evaluation Dataset, User Study, DTC Active, DTC Passive |

> [!tip] 效果简介
> - ShapeR Evaluation Dataset 上，CD ↓ (×10²) / NC ↑ / F1 ↑ 2.375 / 0.810 / 0.722 vs EFM3D 13.82 / 0.614 / 0.276; LIRM 8.047 / 0.683 / 0.384 (CD 提升 2.7× 以上)。
> - User Study (vs Image-to-3D) 上，ShapeR Win Rate 86.67% (vs TripoSG), 88.33% (vs Direct3DS2), 81.11% (vs Hunyuan3D-2.0), 86.11%... vs 50% (equal preference) (绝对提升 >30%)。
> - DTC Active 上，CD ↓ (×10²) / NC ↑ / F1 ↑ 0.94 / 0.91 / 0.94 vs LIRM 0.90 / 0.94 / 0.92 (相当或略优)。

## 概述

### 问题背景

从真实世界的随意采集图像序列中恢复物体的完整三维形状，是三维视觉领域的核心挑战。现有三维形状生成模型主要依赖干净、无遮挡且精细分割的输入，在室内外随意采集场景中，由于遮挡、杂乱、分辨率低、视角随意等因素，性能急剧下降。此外，这些方法通常需要显式的二维分割掩码作为输入，无法鲁棒地应对非受控条件——即使是交互式分割工具在杂乱场景中也常常失效（图 2）。

### 核心思路

ShapeR 提出了一种全新的度量三维形状生成范式。其核心洞察在于：**稀疏 SLAM 点云提供的全局几何信息与多视图图像、文本描述形成互补**，使模型无需显式分割即可隐式感知目标物体边界。具体而言，ShapeR 利用现成的视觉惯性 SLAM、三维实例检测和视觉语言模型，从输入图像序列中自动提取每个物体的稀疏度量点云、带位姿的多视角图像和机器生成的文字描述。这些多模态条件共同送入一个基于校正流（rectified flow）的变换器，在 VecSet 潜空间中进行去噪，最终解码为物体的完整网格。

### 方法定位

ShapeR 的方法设计围绕三个关键创新点展开：

1. **多模态条件融合**：将稀疏度量 SLAM 点云作为全局几何先验，与带位姿的多视图图像和文本描述协同工作。SLAM 点云通过稀疏三维 ResNet 编码，图像使用冻结的 DINOv2 提取特征并结合二维点投影掩码进行空间提示，文本通过 T5 和 CLIP 编码。这种设计使模型能够隐式学习目标物体的边界，无需显式分割掩码。

2. **两阶段课程训练与大规模在机增强**：第一阶段在 60 万艺术家创建的物体网格上进行预训练，采用大规模组合式在机增强（背景合成、遮挡模拟、噪声注入等）；第二阶段在 Aria Synthetic Environments 合成场景数据上微调，使模型适应真实场景中的遮挡和物体间交互。这一策略显著提升了模型对随意采集场景的泛化能力。

3. **隐式分割机制**：通过二维点投影掩码提示 DINOv2 特征，模型能够区分目标物体与相邻物体，减少混淆，而无需依赖易出错的显式分割工具。

在方法谱系中，ShapeR 区别于以下基线：**EFM3D**、**FoundationStereo** 等场景级融合方法需要真值网格裁剪才能评估单物体；**LIRM**、**DP-Recon** 等方法依赖显式二维分割掩码；**TripoSG**、**Direct3DS2**、**Hunyuan3D-2.0** 等图像到三维模型仅使用单视图输入且缺乏度量尺度；**Amodal3R** 虽支持非模态补全，但同样依赖单视图。ShapeR 首次将稀疏 SLAM 点云、多视图图像和文本描述统一到生成式框架中，实现了度量一致且无需分割的鲁棒重建。

### 主要结果

在自建的 ShapeR 评估数据集（包含 7 个随意采集序列、178 个物体）上，ShapeR 取得了 Chamfer Distance 2.375（×10⁻²）、Normal Consistency 0.810、F1-score 0.722 的结果，相比最优基线方法 CD 提升 2.7 倍以上（表 1）。用户研究中，ShapeR 相比图像到三维基础模型的偏好率超过 80%（表 2）。在 ScanNet++ 和 Replica 等真实场景数据集上，ShapeR 同样显著优于 DPRecon（表 3）。消融实验证实：移除 SLAM 点云使 CD 从 2.375 升至 4.514，移除点云增强或图像增强分别使 CD 升至 3.276 和 3.397，跳过两阶段训练使 CD 升至 3.053（表 1），验证了每个设计组件的必要性。

### 局限与开放问题

ShapeR 的局限性包括：低图像质量或可见视角有限时重建可能不完整；堆叠或紧贴物体可能导致网格包含相邻结构；依赖上游三维实例检测，检测遗漏则无法重建（图 15）。开放问题包括：对动态场景或移动物体的处理能力、单目重建的计算开销、合成场景数据类别覆盖有限对开放词汇重建的影响，以及在极端遮挡和低纹理场景下的鲁棒性。

## 背景与动机

三维形状生成与重建是计算机视觉和图形学领域长期关注的核心问题。近年来，基于学习的模型在受控条件下取得了显著进展，能够从单张或多张图像中生成高质量的三维网格。然而，这些模型大多建立在理想化的假设之上：输入图像需要清晰的物体可见性、干净的背景、精细的分割掩码，以及良好的光照和视角条件。一旦将这些模型部署到真实世界的室内外随意采集场景中，其性能便会急剧下降。

随意采集（casual capture）是指用户使用手机或头戴设备在日常环境中自然拍摄的图像序列。这类场景普遍存在**遮挡、杂乱背景、低分辨率、运动模糊、视角随意**等复杂因素（Figure 2）。例如，一张桌子上的马克杯可能被其他物品部分遮挡，或处于低光照条件下难以辨识边界。在这种非受控条件下，现有方法的多个关键假设被逐一打破。

**现有方法的三个核心缺口**构成了本工作的直接动机：

1. **显式分割依赖的脆弱性**。当前主流的基于位姿的多视图重建方法（如 **LIRM**、**DP-Recon**）以及图像到三维的生成模型（如 **TripoSG**、**Direct3DS2**、**Hunyuan3D-2.0**），通常需要显式的二维分割掩码来界定目标物体。在随意采集场景中，即使使用交互式分割工具（如 SAM2），杂乱背景和遮挡也会导致分割失败或不精确，从而严重损害重建质量。

2. **条件模态的单一性**。大多数模型仅依赖图像（含或不含相机位姿）或图像加文本描述作为条件输入。在遮挡严重、视角有限的场景中，单一图像模态无法提供足够的几何信息来推断物体的完整形状。场景级融合方法（如 **EFM3D**、**FoundationStereo + SDF Fusion**）虽然利用多视图信息，但生成的是整体场景的单一网格，难以独立提取和评估单个物体的重建质量。

3. **训练数据与真实场景的分布偏移**。现有模型通常在干净、孤立的物体数据集上进行训练，缺乏对真实世界中遮挡、杂乱和噪声的接触。这导致模型在遇到随意采集序列时缺乏鲁棒性，无法应对训练分布之外的复杂情况。

上述缺口共同指向一个根本性问题：**如何在无需显式分割的前提下，利用多模态互补信号，在随意采集的复杂场景中鲁棒地生成度量一致且完整的物体形状？**

ShapeR 正是围绕这一核心瓶颈展开设计。其核心洞察在于：稀疏 SLAM 点云提供的全局几何先验与多视角图像、文本描述形成互补——校正流变换器可以利用这些多模态线索隐式感知目标物体边界并去噪生成完整形状，而无需任何显式分割掩码。同时，通过大规模在机增强和两阶段课程训练策略，模型得以弥合合成训练数据与真实随意采集场景之间的分布鸿沟。

## 核心创新

ShapeR 的核心创新在于系统性地重构了“随意采集场景下三维形状生成”的条件输入与训练范式，使其从依赖干净分割与受控视角的脆弱流程，转向一种鲁棒、全自动的多模态生成框架。其关键创新点可归纳为以下四个 **changed slots**。

### 1. 隐式物体感知：从显式分割到 SLAM 点云引导的注意力

现有方法（如 **LIRM**、**DP-Recon**）普遍依赖显式的二维分割掩码来界定目标物体边界，但在杂乱、遮挡、低分辨率的真实场景中，即使交互式分割模型（如 SAM2）也频繁失效（见 Figure 2）。ShapeR 彻底摒弃了这一依赖，转而利用稀疏 SLAM 点云作为物体边界的隐式指示器。

具体而言，ShapeR 将每个物体的稀疏 SLAM 点云投影到多视角图像上，生成二维点投影掩码，并通过一个卷积网络将其编码为空间提示，注入到冻结的 DINOv2 图像特征中。这一设计使去噪变换器能够在不需要显式分割的情况下，学会将注意力聚焦于目标物体区域，有效抑制邻近物体的干扰。消融实验（Table 1）证实：移除该点掩码提示机制后，Chamfer Distance 从 2.375 升至 2.568，且模型更容易错误地重建相邻物体（Figure 9c）。

### 2. 多模态条件互补：SLAM 点云 + 多视图图像 + 文本描述

传统方法通常仅依赖多视图图像（带或不带位姿）或单视图图像进行三维重建。ShapeR 引入了三种互补的条件模态：

- **稀疏度量 SLAM 点云**：提供全局几何先验，聚合了整个序列中关于物体形状的结构信息，弥补了单帧图像因遮挡或视角不佳而缺失的几何线索。
- **带位姿的多视图图像**：提供外观和局部几何细节。
- **VLM 生成的文字描述**：提供语义层面的类别和属性信息，辅助模型理解物体类型。

这三种模态的互补性在消融实验中得到了充分验证：移除 SLAM 点云导致 Chamfer Distance 从 2.375 急剧恶化至 4.514，Normal Consistency 从 0.810 降至 0.765，F1 从 0.722 骤降至 0.486（Table 1）。Figure 4 进一步定性展示了 SLAM 点云在遮挡和杂乱场景下对重建鲁棒性的关键贡献。

### 3. 两阶段课程训练与大规模在机增强

ShapeR 的训练策略是其鲁棒性的另一核心支柱。传统方法通常在干净的孤立物体数据集上训练，导致模型对真实场景中的遮挡、杂乱背景和噪声极度敏感。ShapeR 采用两阶段课程训练：

- **第一阶段（物体级预训练）**：在 600K 艺术家创建的网格上，对所有模态施加大规模在机构成式增强——包括图像背景合成、遮挡模拟、SLAM 点云噪声注入、图像扰动等（Figure 5 左）。
- **第二阶段（场景级微调）**：在 Aria Synthetic Environments 的合成场景数据上微调，该数据包含逼真的遮挡、物体间交互和 SLAM 点云噪声（Figure 5 右）。

消融实验表明，跳过第二阶段（仅物体级预训练）会使 CD 升至 3.053；移除点云增强或图像增强分别使 CD 升至 3.276 和 3.397（Table 1）。Figure 9a 和 9b 进一步可视化地展示了增强和场景微调对模型泛化能力的决定性影响。

### 4. VecSet 潜变量 + 校正流变换器

在生成架构层面，ShapeR 采用 Dora VecSet 作为三维 VAE 的潜变量表示，支持变长序列编码，并通过校正流变换器（基于 FLUX DiT 架构）在高斯噪声与潜变量流形之间建立确定性映射。相比于传统的固定维度潜变量，VecSet 提供了更灵活的几何表示能力。校正流模型通过 ODE 定义传输路径：

$$\dot{z}_t = f_\theta(z_t, t, C), \quad t \in [0,1]$$

其训练目标为最小化预测速度与真实传输速度的期望平方误差：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, z_t, C} \left[ ||f_\theta(z_t, t, C) - (z_0 - z_1)||_2^2 \right]$$

这一生成框架使 ShapeR 能够从多模态条件中稳定地采样出高质量、度量一致的三维形状。

## 整体框架

ShapeR 将随意采集序列中的物体重建形式化为一个**多模态条件校正流生成问题**。其核心设计理念是：不依赖显式 2D 分割掩码，而是通过稀疏 SLAM 点云提供的全局几何先验，结合多视角图像和文本描述，隐式地感知目标物体边界并生成度量一致、完整的形状。

### 输入预处理流水线

给定一段随意拍摄的图像序列，ShapeR 首先通过一系列现成方法进行预处理：

1. **SLAM 与位姿估计**：使用现成的视觉惯性 SLAM 方法从序列中提取稀疏度量点云 $P$ 及每帧相机位姿。
2. **3D 实例检测**：在 SLAM 点云和图像上运行实例检测模型，为每个物体生成 3D 包围框。
3. **物体裁剪与 SAM2 精化**：根据包围框裁剪出每个物体的点云子集 $P_i$ 和对应图像区域；同时利用 SAM2 去除邻接物体的干扰点，确保点云子集尽可能纯净。
4. **文本描述生成**：通过视觉语言模型为每个物体生成自动文字描述 $T_i$。

最终，每个物体 $i$ 获得一个完整的多模态条件集 $C_i = \{P_i, I_i, \Pi_i, M_i, T_i\}$，其中 $I_i$ 为选定的代表性视角图像，$\Pi_i$ 为对应相机位姿，$M_i$ 为 SLAM 点云在图像上的 2D 投影掩码。值得注意的是，整个流程**不使用任何分割掩码**，目标物体的边界通过 3D 点云标记和 2D 投影掩码信息隐式学习。

### 生成核心：校正流变换器

ShapeR 的生成主干由三个紧密耦合的模块构成：

**3D VAE（Dora VecSet）**：采用 Dora 变体的 VecSets 作为潜变量自编码器，将网格编码为变长潜变量序列 $z$，并解码为有符号距离场（SDF）。训练目标为重建 SDF 值的平方误差与 KL 散度正则化的组合：

$$\mathcal{L}_{\mathrm{VAE}} = ||s - s_{GT}||_2^2 + \beta \mathcal{L}_{\mathrm{KL}}\Big(q(z|S) || \mathcal{N}(0,I)\Big)$$

**校正流变换器（FLUX DiT）**：基于 FLUX.1 的双单流变换器架构，从高斯噪声出发，通过确定性 ODE $\dot{z}_t = f_\theta(z_t, t, C)$ 将噪声逐步映射到潜变量流形。训练目标为流匹配损失：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, z_t, C} \left[ ||f_\theta(z_t, t, C) - (z_0 - z_1)||_2^2 \right]$$

**多模态条件编码器**：变换器的条件输入通过四个并行的编码器处理：
- **SLAM 点云**：使用 3D 稀疏 ResNet 编码，捕获全局几何结构
- **多视角图像**：冻结的 DINOv2 提取视觉特征，结合 Plücker 位姿编码；同时将 2D 点投影掩码通过 2D 卷积网络编码后与 DINOv2 特征融合，提供物体特定的空间提示，减少与邻近物体的混淆
- **文本描述**：使用 T5 和 CLIP 编码语义信息

### 推理与度量重建

推理时，从高斯噪声 $z_1 \sim \mathcal{N}(0,I)$ 出发，使用中点法沿 ODE 积分采样：

$$z_{t-\Delta t} = z_t + \Delta t f_\theta(z_t, t, C_i)$$

得到去噪潜变量 $z_0$ 后，通过 VAE 解码器 $D$ 恢复有符号距离场，经 Marching Cubes 提取网格，最终利用原始 SLAM 点云 $P_i$ 重缩放回度量坐标系：

$$\hat{S}_i = \mathrm{Rescale}\big(\mathrm{MarchingCubes}(D(z_0)), P_i\big)$$

### 两阶段课程训练策略

ShapeR 的鲁棒性关键依赖于其训练策略，而非单纯的模型架构创新：

1. **第一阶段——物体级预训练**：在 60 万个艺术家创建的网格上训练，对所有模态施加大规模在机组合增强，包括背景合成、遮挡模拟、点云噪声和图像退化等，迫使模型学习从退化信号中恢复完整形状。
2. **第二阶段——场景级微调**：在 Aria Synthetic Environments 的合成场景数据上微调，该数据包含逼真的遮挡、点云噪声和物体间交互，使模型适应真实场景的复杂性。

消融实验证实了这一策略的有效性：仅物体级预训练而不进行场景微调，Chamfer Distance 从 2.375 升至 3.053；移除点云增强或图像增强也分别导致 CD 升至 3.276 和 3.397，验证了在机增强对真实场景泛化的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/002_Figure_2.jpg]]
*Figure 2: (Top) Objects captured in casual settings pose challenges like clutter, poor viewpoints, low resolution, noise, motion blur, and occlusions that are difficult to segment, even interactively. (Bottom) State-of-the-art 3D models often fail in these scenarios, while ShapeR remains robust and effective*

## 核心模块与公式推导

ShapeR 将面向物体的三维形状生成建模为一个校正流（rectified flow）过程，在由三维变分自编码器（3D VAE）学到的潜空间中进行去噪。整个流程的关键模块和公式如下。

### 3D VAE：潜空间编码与解码

ShapeR 采用 **Dora VecSet** 变体作为潜空间自编码器，将物体网格编码为可变长度的潜变量集合，并解码为有符号距离场（SDF）。

**VAE 训练目标**：
$$
\mathcal{L}_{\mathrm{VAE}} = ||s - s_{GT}||_2^2 + \beta \mathcal{L}_{\mathrm{KL}}\Big(q(z|S) || \mathcal{N}(0,I)\Big)
$$

其中 $s$ 为解码器预测的有符号距离值，$s_{GT}$ 为真实值，第一项为重建误差，第二项为 KL 散度正则化，约束潜变量分布 $q(z|S)$ 接近标准正态分布。

### 校正流变换器：多模态条件去噪

潜变量生成采用基于 **FLUX DiT** 架构的双单流变换器，从高斯噪声出发，在条件 $C$ 的引导下沿确定性流路径去噪。

**校正流常微分方程**：
$$
\dot{z}_t = f_\theta(z_t, t, C), \quad t \in [0,1]
$$

其中 $z_t$ 为时刻 $t$ 的潜变量，$f_\theta$ 为去噪变换器，$C$ 为多模态条件集合。

**流匹配损失**：
$$
\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, z_t, C} \left[ ||f_\theta(z_t, t, C) - (z_0 - z_1)||_2^2 \right]
$$

该损失最小化模型预测的速度向量 $f_\theta(z_t, t, C)$ 与真实传输速度 $(z_0 - z_1)$ 之间的期望平方误差，其中 $z_0$ 为干净潜变量，$z_1 \sim \mathcal{N}(0,I)$ 为噪声。

### 多模态条件编码器

条件集合 $C_i = \{P_i, I_i, \Pi_i, M_i, T_i\}$ 包含五种互补信号，各自由专用编码器处理：

- **SLAM 点云 $P_i$**：通过稀疏 3D ResNet 编码，提供全局几何先验。
- **多视角图像 $I_i$**：使用冻结的 DINOv2 骨干网络提取特征，并与 Plücker 位姿编码 $\Pi_i$ 融合。
- **2D 点投影掩码 $M_i$**：将 SLAM 点投影到图像平面，经 2D 卷积网络编码后与 DINOv2 特征结合，形成物体特定的空间提示，隐式引导模型关注目标物体。
- **文本描述 $T_i$**：由视觉语言模型（VLM）生成，经 T5 和 CLIP 编码。

值得注意的是，整个流程**不使用显式分割掩码**；目标物体的边界通过 3D 点令牌和 2D 投影掩码隐式学习。

### 推理采样与度量重建

推理时，从高斯噪声出发，采用中点法沿流路径逐步去噪：

**流采样**：
$$
z_1 \sim \mathcal{N}(0,I), \quad z_{t-\Delta t} = z_t + \Delta t f_\theta(z_t, t, C_i)
$$

**度量网格重建**：
$$
\hat{S}_i = \mathrm{Rescale}\big(\mathrm{MarchingCubes}(D(z_0)), P_i\big)
$$

去噪后的潜变量 $z_0$ 经解码器 $D$ 生成有符号距离场，通过 Marching Cubes 提取等值面得到网格，最后利用 SLAM 点云 $P_i$ 的度量信息将网格缩放回原始坐标系，确保重建结果具有度量一致性。

### 补充图表

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/003_Figure_3.jpg]]
*Figure 3: The ShapeR denoising transformer, built on the FLUX DiT architecture, denoises latent VecSets by conditioning on multiple modalities: posed images, SLAM points, captions, and the 2D projections of SLAM points observed in those input images. SLAM points are encoded with a sparse 3D ResNet, images using a frozen DINOv2 backbone, poses using Plucker encodings, and ¨ projection masks via a 2D convolutional network. The denoised latent is decoded into a SDF, from which the final object shape is extracted using marching cubes*

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/005_Figure_5.jpg]]
*Figure 5: (Left) We pretrain on 600K object meshes with extensive, compositional augmentations across all modalities, simulating realistic backgrounds via image compositing, and introducing diverse occlusions and noise in both images and SLAM points. (Right) We then fine-tune on object-centric crops from Aria Synthetic Environment scenes, which feature realistic image occlusions, SLAM point cloud noise, and inter-object interactions*

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/004_Figure_4.jpg]]
*Figure 4: Incorporating SLAM points significantly enhances robustness. These points provide a complementary geometric signal to posed images, encoding aggregated shape information across the entire sequence*

## 实验与分析

### 评估设置

为系统衡量 ShapeR 在真实随意采集场景下的鲁棒性，作者构建了 **ShapeR Evaluation Dataset**，包含 7 段随意采集序列、共 178 个物体，覆盖桌椅、电器、箱包等多种室内外类别。每段序列通过将物体单独取出、在无遮挡条件下拍摄高质量图像、利用图像到 3D 模型生成几何、再经人工对齐回原序列的方式获取伪真值网格（Figure 12）。该数据集的核心特点是：**遮挡、杂乱、低分辨率、运动模糊和非受控视角**，远超市面现有 3D 重建基准的难度（Figure 10, Figure 13）。

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/018_Figure_12.jpg]]
*Figure 12: To obtain pseudo-ground truth geometry for an object in the sequence (left), we first place the object in isolation to avoid clutter and occlusion, and capture a high-quality, uncluttered image. We then apply segmentation and image-to-3D modeling to generate the object’s geometry (mid). This geometry is manually aligned and inserted back into the original casual sequence using a web annotation interface, verified by matching 2D projections to image silhouettes and by checking alignment with the sequence’s point cloud (right)*

评估指标采用双向 **Chamfer Distance (CD↓)**、**Normal Consistency (NC↑)** 和 **F1-score (F1↑)**。对比方法涵盖三类：

- **多视图到 3D 方法**：EFM3D（整体网格融合）、FoundationStereo + SDF Fusion（深度融合）、LIRM 和 DP-Recon（依赖显式 2D 分割掩码）。为公平起见，对场景级方法使用真值网格裁剪物体评估；对依赖分割的方法，提供以边界框为提示的 SAM2 分割掩码。
- **图像到 3D 基础模型**：TripoSG、Direct3DS2、Hunyuan3D-2.0、Amodal3R。人工挑选最佳视角并提供交互式 SAM2 分割，确保其输入最优。
- **场景级方法**：MIDI3D（单图）、SceneGen（四视图），均使用人工分割。

ShapeR 完全自动化，**无需任何人工干预或显式分割掩码**。

### 主实验结果

**Table 1** 展示了在 ShapeR Evaluation Dataset 上的定量对比。ShapeR 在所有指标上全面超越现有方法：

| 方法 | CD ↓ (×10²) | NC ↑ | F1 ↑ |
|------|-------------|------|------|
| EFM3D | 13.82 | 0.614 | 0.276 |
| FoundationStereo | 4.990 | 0.704 | 0.445 |
| LIRM | 8.047 | 0.683 | 0.384 |
| DP-Recon | 4.881 | 0.688 | 0.461 |
| **ShapeR** | **2.375** | **0.810** | **0.722** |

ShapeR 的 CD 相比次优的 FoundationStereo 提升约 **2.1 倍**，相比依赖分割的 LIRM 提升约 **3.4 倍**。F1 分数从 0.461 提升至 0.722，表明生成形状的完整性和准确性显著提高。定性对比（Figure 6）显示，场景融合方法在杂乱背景下难以分离物体边界，而依赖分割的方法在低分辨率或遮挡区域频繁失败；ShapeR 则能从稀疏 SLAM 点云和多视图图像中隐式感知物体轮廓，生成完整且度量一致的网格。

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative comparison on the ShapeR evaluation dataset against posed multiview-to-3D methods. For scene-centric fusion approaches (EVL, Foundation Stereo), ground-truth meshes are used to segment individual object shapes. For methods relying on image segmentation masks (DP-Recon, LIRM), we employ SAM2, prompted with bounding boxes, to generate input image masks*

**用户研究**（Table 2）进一步验证了感知质量优势。在 660 次成对比较中，ShapeR 对 TripoSG 的偏好率为 **86.67%**，对 Direct3DS2 为 **88.33%**，对 Hunyuan3D-2.0 为 **81.11%**，对 Amodal3R 为 **86.11%**。图像到 3D 方法受限于单视图输入，在遮挡和视角不佳时容易产生幻觉或缺失几何，而 ShapeR 利用多视图互补信息显著提升了重建可信度（Figure 7）。

**跨数据集泛化**：在 DTC Active 受控场景上，ShapeR 与 LIRM 性能相当（CD 0.94 vs 0.90）；但在 DTC Passive 更自由的采集条件下，ShapeR 的 CD 降至 0.95，而 LIRM 升至 1.37（Table 4），表明 ShapeR 对采集随意度的敏感度更低。在 ScanNet++ 和 Replica 真实场景上，ShapeR 的召回率分别达到 0.91 和 0.82，远超 DP-Recon 的 0.45 和 0.57（Table 3），且生成的网格在遮挡区域比真值扫描更完整（Figure 18）。

### 消融实验

Table 1 下半部分揭示了各组件的因果贡献：

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/006_Table_1.jpg]]
*Table 1: Comparison on ShapeR evaluation dataset against posed multiview to 3D approaches, and an ablation of components*

**1. SLAM 点云是关键互补模态。** 移除 SLAM 点云后，CD 从 2.375 急剧升至 4.514，F1 从 0.722 降至 0.486。稀疏点云为模型提供了跨帧聚合的全局几何先验，弥补了单帧图像在遮挡区域的不足（Figure 4）。即使图像中物体被部分遮挡，点云仍能传递其空间范围信息。

**2. 在机增强策略不可或缺。** 移除点云增强（加噪、随机丢弃、扰动）使 CD 升至 3.276；移除图像增强（背景合成、遮挡模拟、颜色抖动）使 CD 升至 3.397，NC 降至 0.778。Figure 9(a) 显示，无点云增强时模型过拟合于点输入，在无点区域缺失几何；无图像增强时模型对遮挡和裁剪不完整敏感，容易产生残缺网格。背景合成增强的移除则迫使模型依赖预分割，引入噪声掩码导致预测错误。

**3. 两阶段课程训练显著提升鲁棒性。** 仅使用物体级预训练而不进行场景微调，CD 升至 3.053，NC 降至 0.801。Figure 9(b) 表明，场景微调使模型学会处理真实场景中的物体间交互和复杂遮挡，而纯物体训练无法泛化到这些情况。

**4. 2D 点云掩码提示减少相邻物体混淆。** 移除该提示后，CD 升至 2.568，F1 降至 0.701。Figure 9(c) 显示，当场景中存在多个紧邻物体时，无掩码提示的模型容易错误重建相邻物体的几何。将 SLAM 点的 2D 投影作为空间提示注入 DINOv2 特征，使模型能明确区分目标物体与背景杂物。

### 失败模式与局限性

Figure 15 系统总结了 ShapeR 的三类主要失败模式：

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/021_Figure_15.jpg]]
*Figure 15: ShapeR limitations. (a) Low image fidelity or limited views lead to incomplete or low-detail reconstructions. (b) Closely stacked or attached objects can cause meshes to include parts of adjacent structures, even when the point associated with these structures are not in the input (c) ShapeR relies on upstream 3D detection; missed or inaccurate detections result in unrecoverable objects*

- **低质量输入**：当物体可见视角极少或图像分辨率过低时，重建结果不完整或缺乏细节（Figure 15a）。这本质上是信息瓶颈——多视图互补信号不足，流模型无法凭空推断缺失几何。
- **紧贴/堆叠物体**：对于堆叠或紧贴的物体（如桌上物品相互接触），生成网格有时会包含相邻物体的部分结构（Figure 15b）。尽管 2D 点云掩码提示缓解了该问题，但当物体边界在 3D 空间中高度模糊时，隐式分割仍有局限。
- **上游检测依赖**：ShapeR 依赖 3D 实例检测的召回率；若检测遗漏或包围框不准确，对应物体无法重建（Figure 15c）。这是级联系统的固有弱点，而非生成模型本身的问题。

### 鲁棒性趋势分析

Figure 13 揭示了采集条件从受控到随意的性能退化趋势：DTC Active（严格环绕采集）→ DTC Passive（自由移动）→ ShapeR Evaluation（真实随意场景），挑战性非线性增长。基线方法（如 LIRM）在 DTC Passive 上已有明显退化，在 ShapeR Evaluation 上崩溃；ShapeR 的指标退化相对平缓，验证了多模态条件与增强训练策略对分布外场景的泛化能力。

### 补充图表

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/009_Figure_7.jpg]]
*Figure 7: Qualitative comparison against foundation image-to-3D models. For these baselines, we manually select a view with clear object visibility and use interactive SAM2-based segmentations to provide optimal input. In contrast, ShapeR operates fully automatically on multiple posed views and preprocessed inputs, requiring no manual intervention*

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/008_Table_2.jpg]]
*Table 2: Percentage of users who prefer our method over the image-to-3d baselines over 660 responses. Our generated meshes are preferred significantly more often*

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/025_Table_4.jpg]]
*Table 4: Reconstruction results on the DTC [23] Active and Passive datasets, each with approximately 100 sequences, compared against LIRM [44]. ShapeR achieves comparable performance to LIRM on the highly controlled Active sequences, and surpasses LIRM on the more challenging Passive sequences*

![[assets/figures/papers/paper_list_l2267_https_arxiv_org_abs_2601_11514/figures/011_Figure_9.jpg]]
*Figure 9: Ablations of components. (a) Without point augmentations, the model overfits to point inputs, missing geometry in regions without points. Image augmentations address occlusions and incomplete objects crops. Omitting background composition requires presegmentation, which can introduce noisy masks and prediction errors. (b) Fine-tuning on scene-centric crops improves robustness in challenging scenarios over object-centric training alone. (c) Prompting DINO features with 2D point projections clarifies which object to reconstruct in cluttered scenes, reducing confusion from nearby objects and improving reconstruction accuracy*

## 方法谱系与知识库定位

### 1. 问题定位与基线谱系

ShapeR 所解决的核心问题——从随意采集的图像序列中鲁棒地重建度量级三维物体形状——横跨了多个已有技术路线，但这些路线在真实非受控场景下均存在显著瓶颈。现有基线可归纳为以下谱系：

**（1）基于位姿的多视图三维重建（Posed Multi-View Reconstruction）**

此类方法假设已知相机位姿，通过多视图几何或神经场融合重建场景或物体。代表性工作包括：

- **EFM3D**：生成整体式场景网格，但在杂乱场景中无法区分单个物体，需用真值网格裁剪才能评估单个物体形状。
- **FoundationStereo + SDF Fusion**：基于深度估计和符号距离场融合，同样输出场景级网格，缺乏物体级感知能力。
- **LIRM**：依赖显式二维分割掩码进行物体级重建，在遮挡、低分辨率等随意采集条件下分割质量急剧下降。
- **DP-Recon**：同样需要分割掩码作为输入，在真实场景中分割失效时性能严重退化。

ShapeR 与此类方法的**根本差异**在于：ShapeR 不需要显式的二维分割掩码，而是通过稀疏 SLAM 点云及其二维投影掩码隐式地引导模型关注目标物体。这一设计使得 ShapeR 在分割困难的随意采集场景中仍能保持鲁棒性。

**（2）图像到三维生成（Image-to-3D Generation）**

此类方法从单张图像生成三维形状，代表模型包括 **TripoSG**、**Direct3DS2**、**Hunyuan3D-2.0** 和 **Amodal3R**。它们通常假设输入图像中物体清晰可见且已分割，在随意采集场景中面临三个关键挑战：① 单视角信息不足以恢复完整几何，尤其是被遮挡部分；② 缺乏度量尺度信息，生成结果尺度任意；③ 需要人工挑选最佳视角并提供交互式分割才能获得可接受的结果。ShapeR 利用多视角位姿图像和稀疏 SLAM 点云，天然具备多视图互补性和度量尺度，无需人工干预。

**（3）图像到场景布局与重建（Image-to-Scene Reconstruction）**

**MIDI3D**（单图像）和 **SceneGen**（四视图）尝试从图像恢复场景布局和物体形状，但均需要人工物体分割，且在物体尺度和空间排列上容易出错。ShapeR 以物体为中心独立重建每个实例，再组合为度量一致的场景，避免了全局布局推理的不稳定性。

**（4）交互式三维重建**

**SAM 3D Objects** 通过交互式分割从单张图像生成非度量三维形状，可能产生幻觉（如预测错误数量的物体）且物体放置不准确。ShapeR 利用序列位姿信息生成度量准确的几何和一致的空间位置。

### 2. 核心机制差异：四个关键设计空间

ShapeR 相对于上述基线在四个关键设计维度上做出了不同的选择：

| 设计维度 | 基线主流做法 | ShapeR 的做法 | 因果作用 |
|---------|-------------|--------------|---------|
| **物体分割** | 显式二维分割掩码（如 SAM2），在杂乱场景中易失效 | 隐式分割：通过物体 SLAM 点云和二维投影点掩码引导注意力，无需人工掩码 | 避免分割错误级联传播，提升杂乱场景鲁棒性 |
| **条件模态** | 多视图图像（含或不含位姿）或图像+文本 | 稀疏度量 SLAM 点云 + 位姿多视图图像 + 机器生成文本描述 | 点云提供全局几何先验，与图像纹理互补，文本提供语义锚定 |
| **训练策略** | 在干净孤立物体数据集上训练 | 两阶段课程：① 60万艺术家创作网格上的大规模在机增强预训练；② Aria Synthetic Environments 场景数据微调 | 增强策略覆盖背景合成、遮挡、噪声等真实世界复杂性，场景微调进一步弥合 sim-to-real 差距 |
| **图像特征条件** | 标准图像特征提取 | DINOv2 特征与二维点投影掩码通过卷积编码器融合，提供物体特异性空间提示 | 减少与邻近物体的混淆，提升重建精度 |

### 3. 适用边界与局限

ShapeR 的设计决定了其适用边界和已知局限：

**（1）上游依赖的级联失效风险**

ShapeR 依赖三个上游模块：视觉惯性 SLAM 提取稀疏点云和位姿、三维实例检测生成包围框、VLM 生成文本描述。其中三维实例检测是关键单点故障——若检测遗漏或包围框不准确，对应物体无法重建（Figure 15c）。在极端遮挡、低纹理或动态场景下，SLAM 点云本身可能稀疏或噪声严重，模型对此类退化的鲁棒性尚需进一步验证。

**（2）物体分离的边界模糊**

对于堆叠或紧贴的物体（如桌上堆放的物品），即使输入点云中不包含相邻物体的点，生成的网格有时仍会包含相邻结构的部分几何（Figure 15b）。这表明模型在物体边界模糊时仍存在“渗透”问题，二维点掩码提示机制虽能缓解但未能根除。

**（3）图像质量和视角覆盖的敏感性**

当物体可见视角非常有限或图像质量低（低分辨率、运动模糊严重）时，重建可能不完整或缺乏精细细节（Figure 15a）。这是多视图方法的固有约束，但 ShapeR 通过 SLAM 点云提供的聚合几何信息在一定程度上缓解了单视角信息不足的问题。

**（4）类别覆盖与开放词汇泛化**

两阶段训练中的合成场景数据（Aria Synthetic Environments）覆盖的物体类别有限，其开放词汇泛化能力受限于预训练数据的类别分布。对于完全未见过的物体类别，模型性能可能下降，这一点在论文中尚未充分评估。

### 4. 开放问题

以下问题超出论文验证范围，构成未来的研究方向：

1. **动态场景与移动物体**：ShapeR 假设场景静态，SLAM 点云和位姿估计在动态场景中可能失效。如何扩展至包含移动物体的随意采集序列？
2. **单目重建的计算开销**：论文展示了使用 MapAnything 进行单目度量重建的可能性（Figure 14），但未报告该配置下的推理时间和计算成本。
3. **极端退化条件下的鲁棒性边界**：在严重遮挡、低纹理、极端光照等条件下，SLAM 点云质量下降，模型的鲁棒性下限在哪里？
4. **非刚体物体的扩展**：当前框架假设物体为刚体，能否扩展至可变形物体的重建？
5. **与大规模三维基础模型的整合**：ShapeR 的校正流变换器架构与新兴的三维基础模型（如基于大规模三维数据训练的生成模型）之间存在潜在的互补性，如何整合两者的优势？

### 5. 知识库定位

ShapeR 在三维视觉知识库中的定位可概括为：**连接多视图几何重建与三维生成建模的桥梁性工作**。它从多视图几何中继承了度量尺度和多视角互补性（通过 SLAM 和位姿），从生成建模中继承了处理模糊性和补全遮挡区域的能力（通过校正流变换器），并通过隐式分割机制摆脱了对显式掩码的依赖。其两阶段课程训练策略为将合成数据上训练的生成模型迁移至真实非受控场景提供了一套可复用的范式。

## 原文 PDF

![[paperPDFs/CVPR_2026/ShapeR_Robust_Conditional_3D_Shape_Generation_from_Casual_Captures.pdf]]