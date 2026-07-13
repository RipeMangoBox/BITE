---
title: "CrowdGaussian: Reconstructing High-Fidelity 3D Gaussians for Human Crowd from a Single Image"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CrowdGaussian_Reconstructing_High_Fidelity_3D_Gaussians_for_Human_Crowd_from_a_Single_Image.pdf
project_link: null
code_link: null
aliases:
- CrowdGaussian
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过自监督教师-学生蒸馏训练遮挡鲁棒的人体重建模型（LORM），以及引入自校准学习（SCL）策略训练单步扩散细化器（CrowdRefiner）自适应增强细节。
primary_logic: 利用大规模预训练人体重建模型的自监督适应，在不依赖3D标注的情况下从严重遮挡输入中恢复完整几何；并借助几何条件（SMPL法线图）引导的单步扩散细化器，通过自校准学习自适应地增强欠恢复区域、保留已恢复区域，生成高保真的伪真值用于蒸馏，从而大幅提升多人三维高斯场景的几何完整性与纹理清晰度。
claims:
- 完整流水线（LORM+CrowdRefiner）在THuman2.1遮挡重建上达到PSNR 18.619，SSIM 0.931，LPIPS 0.914，三项指标均优于所有基线。
- LORM在60%的极高遮挡比下仍保持PSNR 18.116，而基线LHM和IDOL已产生严重退化。
- 自校准学习（SCL）与SMPL法线图条件使细化器生成质量达到PSNR 20.790，显著优于无SCL或无几何条件的变体。
- 在真实场景严重遮挡图像上，本方法能够重建完整的几何与纹理，而网格基线和3DGS基线均出现透明伪影或不完整的几何。
---

# CrowdGaussian: Reconstructing High-Fidelity 3D Gaussians for Human Crowd from a Single Image

> [!tip] 核心洞察
> 利用大规模预训练人体重建模型的自监督适应，在不依赖3D标注的情况下从严重遮挡输入中恢复完整几何；并借助几何条件（SMPL法线图）引导的单步扩散细化器，通过自校准学习自适应地增强欠恢复区域、保留已恢复区域，生成高保真的伪真值用于蒸馏，从而大幅提升多人三维高斯场景的几何完整性与纹理清晰度。

| 字段 | 内容 |
|------|------|
| 中文题名 | CrowdGaussian: 从单张图像重建高保真人群三维高斯 |
| 英文题名 | CrowdGaussian: Reconstructing High-Fidelity 3D Gaussians for Human Crowd from a Single Image |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.17779) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | CrowdGaussian |
| Dataset | THuman2.1 |

> [!tip] 效果简介
> - THuman2.1 (遮挡重建，随机掩膜) 上，PSNR↑ 18.619 (LORM+CrowdRefiner) vs 18.171 (LHM) (+0.448)；SSIM↑ 0.931 vs 0.919 (IDOL) (+0.012)；LPIPS↓ 0.914 vs 0.994 (IDOL) (-0.080)。
> - THuman2.1 (60%遮挡率) 上，PSNR↑ 18.116 (LORM) vs 17.551 (LHM) (+0.565)。
> - 多人大场景合成测试集 (23个场景) 上，PSNR↑ (CrowdRefiner生成质量) 20.790 (SCL + SMPL法线) vs 20.013 (无SCL, 无Normal) (+0.777)。

## 概要

**问题瓶颈**：从单张图像重建密集人群的三维场景面临双重挑战——严重的个体间遮挡使可见信息极度稀疏，低分辨率输入进一步丢失高频细节。现有方法缺乏统一框架，难以同时恢复完整几何和清晰纹理。

**核心思路**：CrowdGaussian 提出两阶段统一框架，通过两个关键机制突破瓶颈：(1) **LORM**（Large Occluded Human Reconstruction Model）采用自监督教师-学生蒸馏，在不依赖任何三维标注的情况下，从严重遮挡的人物裁剪图中恢复完整三维高斯表示；(2) **CrowdRefiner** 是基于 SD-Turbo 的单步扩散细化器，以粗渲染和 SMPL 法线图作为几何条件，通过**自校准学习（SCL）**策略自适应增强欠恢复区域、同时保留已恢复区域的结构完整性，生成高保真伪真值用于蒸馏回三维高斯。

**方法定位**：CrowdGaussian 处于单图多人三维重建与三维高斯泼溅（3DGS）的交汇点。相较基于网格的基线（**PSHuman**、**SyncHuman**）和 3DGS 基线（**LHM**、**IDOL** (Zhuang et al., CVPR 2025)），本方法首次将遮挡鲁棒的人体重建模型与扩散式单步细化器联合优化，形成从粗到精的完整流水线。

**主要结果**（Table 1, THuman2.1 遮挡重建测试集）：
- 完整流水线（LORM + CrowdRefiner）达到 **PSNR 18.619**，SSIM 0.931，LPIPS 0.914，三项指标均优于所有基线。
- LORM 在 60% 极高遮挡比下仍保持 **PSNR 18.116**，而基线 LHM 和 IDOL 已严重退化（Table 2）。
- 自校准学习与 SMPL 法线图条件使细化器生成质量达到 **PSNR 20.790**，显著优于无 SCL 或无几何条件的变体（Table 3）。
- 在真实场景严重遮挡图像上，本方法能重建完整几何与纹理，而网格基线和 3DGS 基线均出现透明伪影或不完整几何（Figure 7）；对 2× 和 4× 下采样输入，本方法仍能恢复锐利纹理（Figure 8）。

**局限性**：流水线依赖现成的姿态估计器（PromptHMR），严重的初始化错误（尤其是手部）会传播至最终几何；极端低分辨率下，扩散细化器可能生成与身份不一致的细节，且遮挡区域的复原细节未必忠实于真实值。

从单张图像重建三维人体是计算机视觉与图形学中的核心问题，在虚拟现实、增强现实、数字人建模等领域具有广泛的应用前景。近年来，基于三维高斯溅射（3D Gaussian Splatting, 3DGS）的人体重建方法取得了显著进展，能够从单视图或多视图输入中恢复出具有精细纹理的三维表示。然而，当场景从单人扩展到**密集人群**时，现有方法面临两个关键挑战。

**第一，严重的个体间遮挡导致几何不完整。** 在人群场景中，人与人之间的相互遮挡使得每个个体的可见区域大幅减少。传统的网格重建方法（如PSHuman、SyncHuman）和3DGS重建方法（如LHM、**IDOL** (Zhuang et al., CVPR 2025)）通常假设输入图像中的人物是完整可见的，当面对严重遮挡时，它们往往产生透明伪影、不连贯的纹理或完全缺失的几何结构。如图7所示，这些基线方法在真实场景的遮挡图像上无法恢复完整的几何与纹理。问题的本质在于，现有方法缺乏从部分观测中“补全”不可见区域几何的能力，且没有针对遮挡场景进行专门的训练设计。

**第二，低分辨率输入导致细节丢失。** 人群图像中，单个个体通常占据较小的像素区域，导致输入分辨率不足。现有方法在处理低分辨率输入时，输出往往模糊且带有边界伪影，无法恢复锐利的纹理细节。如图8所示，在2×和4×下采样条件下，基线的重建质量急剧退化。

从方法论层面看，当前的人体重建研究存在一个显著缺口：**缺乏一个统一高效的处理框架，能够同时应对密集人群场景中的遮挡补全和细节增强问题。** 具体而言，现有工作要么专注于单人场景的精细重建但无法处理遮挡，要么依赖2D修复作为预处理步骤，但这往往导致几何失真和伪影（如图13所示）。此外，大规模预训练的人体重建模型虽然具备强大的先验知识，但尚未被有效适配到遮挡场景中。

针对上述瓶颈，**CrowdGaussian**提出了一个统一的两阶段框架。其核心动机在于：通过自监督的教师-学生蒸馏训练，使大规模人体重建模型能够从严重遮挡输入中恢复完整几何；并借助几何条件引导的单步扩散细化器，通过自校准学习策略自适应地增强欠恢复区域的细节，同时保留已恢复区域的结构完整性。这一设计使得从单张人群图像重建高保真三维高斯场景成为可能。

## 核心方法与创新机理

CrowdGaussian 的核心创新并非提出全新的网络架构，而是针对**密集人群场景中个体严重遮挡与低分辨率输入**这一瓶颈，构建了一套**自监督适应与自校准生成**相耦合的两阶段流水线。其关键 changed slots 体现在两个层面：遮挡鲁棒的三维人体重建模型 LORM，以及自适应细节增强的单步扩散细化器 CrowdRefiner。

### 1. 自监督教师-学生蒸馏：从遮挡输入恢复完整几何

现有大型人体重建模型（如 LHM）在直接处理遮挡图像时缺乏专门的遮挡感知能力，导致被遮挡区域的几何严重退化。CrowdGaussian 提出 **LORM**，通过**自监督教师-学生框架**赋予预训练模型遮挡鲁棒性，且无需任何外部三维标注。

核心机制如下：教师模型以完整人体图像为输入，生成干净的三维高斯表示，并在多个新视角下渲染出干净伪真值：

$$R _ { \mathrm { c l e a n } } ^ { ( v ) } = \operatorname { R e n d e r } ( \mathcal { G } _ { \mathrm { f u l l } } , \theta _ { v } )$$

学生模型 LORM 则以合成的遮挡图像为输入，预测三维高斯并在相同视角下渲染粗结果：

$$R _ { \mathrm { c o a r s e } } ^ { ( v ) } = \mathrm { R e n d e r } ( \operatorname { L O R M } ( I _ { \mathrm { o c c } } , \theta ) , \theta _ { v } )$$

通过自蒸馏损失约束粗渲染逼近干净渲染，迫使 LORM 学会从严重遮挡的输入中“幻觉”出完整的几何：

$$\mathcal { L } _ { \mathrm { s e l f - d i s t i l l } } = \sum _ { v = 1 } ^ { V } \Bigg ( \lambda _ { \mathrm { r g b } } \| R _ { \mathrm { c l e a n } } ^ { ( v ) } - R _ { \mathrm { c o a r s e } } ^ { ( v ) } \| _ { 2 } + \lambda _ { \mathrm { s s i m } } ( 1 - \mathrm { S S I M } ( R _ { \mathrm { c l e a n } } ^ { ( v ) } , R _ { \mathrm { c o a r s e } } ^ { ( v ) } ) ) \Bigg )$$

为保留预训练视觉先验并实现高效适应，LORM 冻结 Sapiens 编码器和高斯解码器，仅在 MBHT Transformer 中注入可训练的 **LoRA** 模块。

**证据强度**：在 THuman2.1 遮挡重建基准上，LORM 在 60% 极高遮挡比下仍保持 PSNR 18.116，而基线 LHM 和 IDOL 已产生严重退化（Table 2），证实了该训练策略对遮挡鲁棒性的因果作用。

### 2. 自校准学习与几何条件引导的单步扩散细化

第一阶段生成的粗三维高斯场景在欠恢复区域（如面部、手部、衣物纹理）仍缺乏高频细节。CrowdGaussian 引入 **CrowdRefiner**——一个基于 SD-Turbo 微调的单步扩散模型，将粗渲染提升为高保真伪真值。其关键创新包含两个 changed slots：

**（1）自校准学习策略**。标准监督训练仅使用“退化-清洁”图像对，容易导致模型过度增强，在已恢复良好的区域产生面部扭曲和伪影。CrowdRefiner 采用 **SCL** 策略：在训练时混合身份保持样本，使模型学会自适应地保留已恢复区域、仅细化欠恢复区域，从而维持结构完整性。

**（2）SMPL 法线图作为几何条件**。CrowdRefiner 同时接收粗 RGB 渲染和对应的 SMPL 法线图作为输入，法线图提供显式的三维几何先验，防止结构歧义导致的手部塌陷和面部失真。

细化器的复合训练损失融合像素级 L2、感知 LPIPS、结构 SSIM 和纹理 Gram 损失：

$$\mathcal { L } _ { \mathrm { d i f f } } = \lambda _ { L 2 } \mathcal { L } _ { \mathrm { L } 2 } + \lambda _ { \mathrm { l p i p s } } \mathcal { L } _ { \mathrm { L P I P S } } + \lambda _ { \mathrm { s s i m } } \mathcal { L } _ { \mathrm { S S I M } } + \lambda _ { \mathrm { g r a m } } \mathcal { L } _ { \mathrm { G r a m } }$$

生成的高保真伪真值随后通过可微分渲染蒸馏回三维高斯表示，优化损失为：

$$\mathcal { L } _ { \mathrm { o p t i m } } = \| R _ { \mathrm { r e f i n e d } } ^ { ( v ) } - R _ { \mathrm { c o a r s e } } ^ { ( v ) } \| _ { 1 } + \lambda _ { \mathrm { s s i m } } ( 1 - \mathrm { S S I M } ( R _ { \mathrm { r e f i n e d } } ^ { ( v ) } , R _ { \mathrm { c o a r s e } } ^ { ( v ) } ) )$$

**证据强度**：消融实验（Table 3）表明，SCL 策略使细化器 PSNR 从 20.130 提升至 20.790；移除 SMPL 法线图条件则导致 PSNR 降至 20.382，并出现手部塌陷和面部失真（Figure 10）。完整流水线（LORM + CrowdRefiner）在 THuman2.1 上达到 PSNR 18.619、SSIM 0.931、LPIPS 0.914，三项指标均优于所有基线（Table 1）。

### 创新本质总结

CrowdGaussian 的创新本质在于**将“遮挡补全”和“细节增强”解耦为两个可独立优化的阶段**，并通过自监督蒸馏和自校准学习两个核心 knob 解决了各自的瓶颈：LORM 利用大规模预训练模型的自监督适应，在不依赖三维标注的情况下赋予其遮挡鲁棒性；CrowdRefiner 借助几何条件引导和 SCL 策略，实现了对欠恢复区域的自适应增强，同时避免了对已恢复区域的过度修改。这种“粗恢复-自适应细化-蒸馏回三维”的闭环设计，使得从单张人群图像重建高保真多人三维高斯场景成为可能。

CrowdGaussian 提出一个**统一的两阶段框架**，从单张自然场景人群图像中重建多人的完整三维形状与外观。流水线的核心设计思路是：先“补全”被遮挡的个体几何，再“细化”粗糙的渲染结果，最终将高保真细节蒸馏回三维高斯表示。Figure 2 给出了完整的数据流。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2603_17779/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed CrowdGaussian framework. Our pipeline operates in two stages. In Stage 1, we first estimate SMPL-X parameters and segment individuals from the input image. These occluded crops are processed by our LORM to hallucinate complete geometries, assembling an initial coarse multi-person 3DGS scene. In Stage 2, we render this coarse scene into RGB images and normal maps. Our CrowdRefiner leverages these cues to generate high-fidelity pseudo-ground truths, which are then distilled back into the 3D Gaussians via differentiable rendering, significantly enhancing local details and overall sharpness*

### 阶段一：粗粒度人群补全

输入为单张多人图像。首先通过现成的多人 HMR 估计每个人的 SMPL-X 姿态、形状与相机位置，同时用 SAM 将每个个体从图像中分割出来，得到可能带有严重遮挡的人物裁剪图。这些裁剪图随后送入 **LORM**（Large Occluded Human Reconstruction Model），该模型从遮挡输入中“幻觉”出完整的几何，输出每个个体的三维高斯表示。将所有个体的高斯拼合，即得到初始的粗粒度多人 3DGS 场景。

### 阶段二：扩散式人群细化

阶段一的粗场景在多个新视角下渲染，得到粗 RGB 渲染图及其对应的 SMPL 法线图。**CrowdRefiner** 是一个基于 SD-Turbo 微调的单步扩散模型，它以粗渲染和法线图作为联合条件，生成高保真的伪真值图像。这些伪真值随后通过可微分渲染，以 L1 和 SSIM 损失蒸馏回三维高斯，显著提升几何锐度和局部纹理保真度。

### 关键模块关系

| 模块 | 功能 | 输入 → 输出 |
|------|------|-------------|
| Multi-Person HMR + SAM | 姿态估计与个体分割 | 人群图像 → 单人裁剪图 + SMPL-X 参数 |
| LORM | 遮挡鲁棒的三维人体重建 | 遮挡裁剪图 → 完整 3D 高斯 |
| CrowdRefiner | 单步扩散细化 | 粗渲染 + SMPL 法线图 → 高保真伪真值 |
| 3DGS 蒸馏 | 细节迁移 | 伪真值 + 粗高斯 → 精化后的 3D 高斯场景 |

### 设计瓶颈与因果机制

整个框架围绕两个核心因果旋钮展开：

1. **遮挡鲁棒重建**：LORM 通过自监督教师-学生蒸馏训练获得遮挡鲁棒性——教师模型从完整图像生成干净的伪真值渲染，学生模型从遮挡图像预测的高斯渲染与之对齐，从而在不依赖任何三维标注的条件下学会补全被遮挡的几何。这一设计直接回应了密集人群中严重个体间遮挡导致几何不完整的瓶颈。

2. **自适应细节增强**：CrowdRefiner 采用**自校准学习**策略，将身份保持样本与退化-清洁样本混合训练，使模型能够自适应地判断哪些区域需要增强、哪些区域应当保留，避免标准监督训练中常见的过度细化（如面部扭曲和伪影）。同时，SMPL 法线图作为几何先验条件输入，防止结构歧义导致的手部塌陷和纹理错位。

这种“先补全几何、再增强纹理、最后蒸馏回三维”的流水线设计，使得 CrowdGaussian 能够在严重遮挡和低分辨率输入下，仍然恢复出完整且高保真的多人三维高斯场景。

### 3D高斯场景表示

CrowdGaussian 采用 3D Gaussian Splatting（3DGS）作为统一的场景表示。一组 3D 高斯定义为：

$$\mathcal { G } = \{ ( \pmb { \mu } _ { i } , \pmb { \Sigma } _ { i } , \alpha _ { i } , \mathbf { c } _ { i } ) \} _ { i = 1 } ^ { N }$$

其中 $\pmb{\mu}_i$ 为高斯中心，$\pmb{\Sigma}_i$ 为协方差矩阵，$\alpha_i$ 为不透明度，$\mathbf{c}_i$ 为视角相关的颜色（通过球谐函数编码）。该表示可通过可微分光栅化从任意视角高效渲染。

### LORM：大遮挡人体重建模型

LORM 是第一阶段的核心模块，负责从被遮挡的单人裁剪图中重建完整的 3D 人体高斯。其设计遵循两个原则：**保留大规模预训练模型的视觉先验**，同时**高效适应遮挡输入**。

**架构设计**：LORM 基于预训练的大规模人体重建模型构建，冻结 Sapiens 编码器和 3D 高斯解码器，仅在 MBHT（Multi-Branch Hybrid Transformer）中注入可训练的 LoRA（Low-Rank Adaptation）模块。这种设计最小化了对预训练先验的扰动，同时保持训练效率。

**自监督教师-学生蒸馏**：训练 LORM 的核心挑战在于缺乏遮挡-完整人体的 3D 真值配对。CrowdGaussian 采用自蒸馏策略解决此问题：
- **教师分支**：将完整图像输入预训练教师模型，渲染干净伪真值：

$$R _ { \mathrm { c l e a n } } ^ { ( v ) } = \operatorname { R e n d e r } ( \mathcal { G } _ { \mathrm { f u l l } } , \theta _ { v } )$$

- **学生分支**：将合成遮挡图像输入 LORM，渲染粗重建结果：

$$R _ { \mathrm { c o a r s e } } ^ { ( v ) } = \mathrm { R e n d e r } ( \operatorname { L O R M } ( I _ { \mathrm { o c c } } , \theta ) , \theta _ { v } )$$

- **自蒸馏损失**：约束粗渲染逼近干净渲染，融合 L1、感知损失和 SSIM：

$$\mathcal { L } _ { \mathrm { s e l f - d i s t i l l } } = \sum _ { v = 1 } ^ { V } \Bigg ( \lambda _ { \mathrm { r g b } } \| R _ { \mathrm { c l e a n } } ^ { ( v ) } - R _ { \mathrm { c o a r s e } } ^ { ( v ) } \| _ { 2 } + \lambda _ { \mathrm { s s i m } } ( 1 - \mathrm { S S I M } ( R _ { \mathrm { c l e a n } } ^ { ( v ) } , R _ { \mathrm { c o a r s e } } ^ { ( v ) } ) ) \Bigg )$$

通过该自监督框架，LORM 无需任何外部 3D 标注即可从严重遮挡输入中恢复完整几何。

### CrowdRefiner：单步扩散细化器

第二阶段引入 CrowdRefiner，将第一阶段生成的粗渲染提升为高保真伪真值，再通过可微分渲染蒸馏回 3D 高斯。

**几何条件注入**：与标准扩散模型仅接受 RGB 输入不同，CrowdRefiner 同时接收粗 RGB 渲染和对应的 SMPL 法线图作为几何先验。法线图提供显式的 3D 结构线索，防止细化过程中的结构歧义（消融实验表明，移除法线图条件导致 PSNR 从 20.790 降至 20.382，并出现手部塌陷和面部失真）。

**自校准学习（SCL）**：标准监督训练（仅使用退化-清洁图像对）会导致过度细化，产生面部扭曲和伪影（如 Figure 5 所示）。SCL 策略通过混合两类样本解决此问题：
- **身份保持样本**：清洁图像自身作为输入和目标，教导模型保留已恢复良好的区域
- **退化-清洁对**：粗渲染与对应清洁渲染配对，教导模型修复欠恢复区域

该策略使细化器自适应地平衡结构保持与细节增强。消融实验证实，禁用 SCL 导致 PSNR 从 20.790 降至 20.130。

**训练损失**：CrowdRefiner 基于 SD-Turbo 微调，采用复合损失：

$$\mathcal { L } _ { \mathrm { d i f f } } = \lambda _ { L 2 } \mathcal { L } _ { \mathrm { L } 2 } + \lambda _ { \mathrm { l p i p s } } \mathcal { L } _ { \mathrm { L P I P S } } + \lambda _ { \mathrm { s s i m } } \mathcal { L } _ { \mathrm { S S I M } } + \lambda _ { \mathrm { g r a m } } \mathcal { L } _ { \mathrm { G r a m } }$$

融合像素级 L2、感知 LPIPS、结构 SSIM 和纹理 Gram 损失，从多层级约束细化质量。

### 细节蒸馏回 3D 高斯

CrowdRefiner 生成的高保真伪真值最终通过优化损失蒸馏回 3D 高斯表示：

$$\mathcal { L } _ { \mathrm { o p t i m } } = \| R _ { \mathrm { r e f i n e d } } ^ { ( v ) } - R _ { \mathrm { c o a r s e } } ^ { ( v ) } \| _ { 1 } + \lambda _ { \mathrm { s s i m } } ( 1 - \mathrm { S S I M } ( R _ { \mathrm { r e f i n e d } } ^ { ( v ) } , R _ { \mathrm { c o a r s e } } ^ { ( v ) } ) )$$

该损失结合 L1 和 SSIM，在多视角下将细化后的 2D 细节有效地传递回 3D 表示，显著提升人群场景的几何锐度和局部保真度。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2603_17779/figures/003_Figure_3.jpg]]
*Figure 3: The Large Occluded Human Reconstruction Model (LORM). (a) Architecture. LORM takes an occluded image and a template to reconstruct a complete 3D human. To preserve priors while enabling efficient adaptation, we freeze pre-trained backbones and inject trainable LoRA exclusively into the transformer. (b) Self-Supervised Training. We employ a Teacher-Student framework where the teacher generates clean pseudo-GTs from complete images. These signals guide the student to hallucinate complete geometries from occluded inputs via selfdistillation, achieving robustness without external 3D supervision*

## 实验与关键发现

CrowdGaussian 的评估围绕三个核心问题展开：遮挡鲁棒的人体重建能力、扩散细化器的生成质量增益，以及整体流水线在真实场景下的泛化性。以下从定量主结果、遮挡鲁棒性、消融分析和定性对比四个维度进行梳理。

### 定量主结果：遮挡人体重建

在 THuman2.1 测试集上，采用随机掩膜模拟遮挡，统一使用 24 视点渲染并计算 PSNR、SSIM、LPIPS。完整流水线（LORM + CrowdRefiner）在三项指标上均优于所有基线方法（Table 1）。具体而言，本方法取得 PSNR 18.619，相较最强基线 **LHM** 的 18.171 提升 +0.448；SSIM 达到 0.931，优于 **IDOL**（Zhuang et al., CVPR 2025）的 0.919；LPIPS 降至 0.914，而 IDOL 为 0.994，降幅达 −0.080。这一结果表明，**LORM 的遮挡补全与 CrowdRefiner 的细节增强形成了有效的级联增益**——仅靠粗重建模型无法弥合与完整流水线的差距。

### 遮挡鲁棒性分析

为剥离遮挡程度的影响，Table 2 报告了在 20% 至 60% 递增遮挡率下的性能。LORM 在 60% 的极高遮挡比下仍保持 PSNR 18.116，而基线 LHM 已降至 17.551，IDOL 同样出现严重退化。**因果机制**在于 LORM 的自监督教师-学生蒸馏框架：教师模型从完整图像生成干净伪真值，学生模型仅以遮挡图像为输入，通过多视角渲染损失（L1 + 感知 + SSIM）学习从残缺观测中恢复完整几何。这一训练范式使模型内化了“遮挡-完整”的映射，而非简单记忆可见区域。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2603_17779/figures/013_Table_2.jpg]]
*Table 2: Quantitative comparison under increasing occlusion ratios (20%–60%) on THuman2.1*

### 消融实验：自校准学习与几何条件

CrowdRefiner 的性能增益来自两个关键设计：**自校准学习（SCL）策略**和 **SMPL 法线图几何条件**。Table 3 的消融表明，完整配置（SCL + 法线图）在多人合成测试集（23 个场景）上达到 PSNR 20.790。禁用 SCL（即仅用退化-清洁对进行标准监督训练）使 PSNR 降至 20.130，且 Figure 5 显示此时模型倾向于**过度细化**，产生面部扭曲和伪影。SCL 的核心机制在于训练时混合身份保持样本，迫使细化器学会自适应判断：对已恢复良好的区域保持原样，仅对欠恢复区域施加增强。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2603_17779/figures/015_Table_3.jpg]]
*Table 3: Ablation study on the SCL strategy and geometric conditioning inputs for the refiner. Results demonstrate that both SCL and the additional normal map input contribute to consistent improvements in generation quality, providing higher-fidelity supervision for the subsequent stage*

移除 SMPL 法线图条件使 PSNR 进一步降至 20.382，Figure 10 的定性结果显示手部塌陷和面部结构失真。法线图作为显式 3D 几何先验，有效约束了扩散模型在增强纹理时的结构一致性，防止生成与底层姿态矛盾的细节。

### 真实场景定性对比

Figure 7 展示了在真实严重遮挡图像上的重建结果。基于网格的方法（**PSHuman**、**SyncHuman**）无法恢复被遮挡区域的完整几何；基于 3DGS 的基线（IDOL、LHM）则产生透明伪影或不连贯纹理。相比之下，本方法能够重建完整的几何与纹理，验证了 LORM 的遮挡幻觉能力并非仅在合成掩膜上有效，而是可迁移至真实分布外遮挡。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2603_17779/figures/012_Figure_7.jpg]]
*Figure 7: Qualitative comparison on occluded in-the-wild images. Mesh-based methods (PSHuman, SyncHuman) fail to recover complete geometry. 3DGS-based approaches (IDOL, LHM) produce transparency artifacts or incoherent and distorted textures in missing regions. In contrast, our method reconstructs complete 3D geometry and texture, demonstrating robustness to real-world occlusion*

Figure 8 进一步揭示了方法对**输入分辨率降质的鲁棒性**。在 2× 和 4× 下采样输入下，本方法仍能恢复锐利纹理，而基线的输出则模糊且带有边界伪影。这一优势源于 CrowdRefiner 以单步扩散方式从粗渲染中恢复高频细节，其训练数据覆盖了不同程度的降质模式。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2603_17779/figures/014_Figure_8.jpg]]
*Figure 8: Robustness to resolution degradation. The leftmost column shows the original image, followed by inputs downsampled by 2× and 4×. Subsequent columns compare reconstructions from IDOL, LHM, and Ours. Even from significantly downsampled inputs, our approach consistently recovers high-fidelity geometry and sharp textures, demonstrating superior robustness to input resolution degradation compared to baselines*

### 失败模式与局限

尽管整体性能优异，方法存在两个已知脆弱点。首先，**姿态估计误差会传播**：流水线依赖现成的多人 HMR 和分割模型，若手部或肢体初始化严重错误，后续 LORM 和 CrowdRefiner 无法修正基础结构错位。其次，在极端低分辨率下，扩散细化器可能生成**与身份不一致的细节**，且遮挡区域的复原内容（如衣物徽标）未必忠实于真实值——这是生成式先验的固有风险，需要在实际部署中通过人工校验或置信度估计加以控制。

## 定位与知识库关联

### 与前驱工作的关系

CrowdGaussian 处于“单图多人三维重建”这一交叉地带，其设计同时回应了基于网格的重建、基于三维高斯泼溅（3DGS）的重建、以及扩散式图像增强三条技术路线的固有限制。

**相对于基于网格的重建方法。** **PSHuman** 和 **SyncHuman** 等网格基线在真实遮挡场景下暴露出根本性缺陷：它们无法恢复被遮挡区域的完整几何，输出中出现大面积缺失或塌陷（Figure 7）。这源于网格表示对拓扑连续性的强依赖——当输入图像缺乏对应区域的视觉证据时，模型缺乏“幻觉”完整几何的机制。CrowdGaussian 用 LORM 的自蒸馏训练策略填补了这一空白：教师模型从完整图像生成干净的伪真值三维高斯，学生模型被迫从遮挡输入中重建与之匹配的完整几何，从而在无需三维标注的条件下习得遮挡补全能力。

**相对于 3DGS 重建基线。** **LHM** 和 **IDOL**（Zhuang et al., CVPR 2025）代表了直接从单图回归三维高斯的路线。它们在遮挡场景下的主要失效模式是透明伪影和不连贯纹理（Figure 7）——高斯云在不可见区域缺乏足够的密度和颜色约束，导致渲染时出现空洞或模糊。CrowdGaussian 的改进并非来自更强的单图回归器，而是引入了**两阶段细化范式**：先用 LORM 生成粗高斯场景，再用 CrowdRefiner 在二维渲染域生成高保真伪真值，最后通过可微渲染将细节蒸馏回三维高斯。这一“二维生成—三维蒸馏”的迂回策略绕开了直接三维回归对遮挡区域建模能力不足的瓶颈。

**相对于 2D 修复 + 重建的级联方案。** 一个直观的替代方案是先对遮挡图像进行二维修复，再将修复结果输入重建模型。论文在补充材料中对比了“2D inpainting + LHM”流水线（Figure 13），结果表明该方案会导致几何失真和伪影。根本原因在于二维修复模型缺乏三维几何约束，修复结果在纹理上看似合理，但在三维一致性上存在隐式错位。CrowdGaussian 通过 SMPL 法线图条件将粗粒度几何先验注入细化器，使二维生成过程受三维结构引导，从而保持了跨视角的几何一致性。

### 方法谱系中的位置

从方法设计角度，CrowdGaussian 的核心贡献可定位于以下坐标：

| 维度 | 所属谱系 | 创新点 |
|------|---------|--------|
| 三维表示 | 3D Gaussian Splatting（Kerbl et al., SIGGRAPH 2023） | 将 3DGS 扩展到多人场景，并通过蒸馏实现细节增强 |
| 人体先验 | SMPL-X 参数化模型 | 利用 SMPL 法线图作为扩散模型的几何条件输入 |
| 遮挡处理 | 自监督教师-学生蒸馏 | 在重建模型内部构建遮挡-完整自蒸馏回路，无需外部三维标注 |
| 细节增强 | 单步扩散模型（SD-Turbo 微调） | 提出自校准学习（SCL）策略，防止过度细化 |
| 训练策略 | LoRA 高效微调 | 仅在 MBHT transformer 中注入可训练低秩适配器，冻结视觉编码器与高斯解码器 |

这一设计使得 CrowdGaussian 既区别于“纯重建”路线（LHM、IDOL），也不同于“纯生成”路线（如先修复再重建）。它实质上构建了一个**重建-生成-蒸馏的闭环**：重建提供三维一致的粗结构，生成补充高频细节，蒸馏将二维生成质量固化到三维表示中。

### 适用边界

CrowdGaussian 的有效性受以下边界条件约束：

1. **姿态估计依赖。** 流水线第一阶段依赖现成的多人 HMR 估计器获取 SMPL-X 参数和相机位置。当姿态估计出现严重初始化错误（尤其是手部姿态），该误差将直接传播到 LORM 的输入模板和 CrowdRefiner 的法线图条件中，且流水线未设计联合优化或纠错机制来修正基础结构错位。这意味着在极端姿态或罕见视角下，方法的鲁棒性受限于上游估计器的性能天花板。

2. **身份一致性的分辨率边界。** 对于严重低分辨率输入（如 4× 下采样），CrowdRefiner 的生成过程可能产生与原始身份不一致的细节。论文明确指出，遮挡区域的复原细节可能并不忠实于真实值——例如特定徽标或纹理图案（见 limitations）。这表明细化器在缺乏足够身份信息时倾向于“合理想象”而非“精确重建”。

3. **场景规模与计算代价。** 方法针对多人场景设计，但流水线中的逐人裁剪、独立 LORM 推理、以及 CrowdRefiner 的多视角细化均随人数线性扩展计算量。论文未讨论在密集人群（如数十人）场景下的效率表现，需要在实际部署中进行验证。

### 局限与开放问题

**已知局限。** 除上述边界条件外，论文自述的局限包括：(a) 依赖现成姿态估计器，严重初始化错误可能传播至最终几何；(b) 低分辨率下可能生成身份不一致的细节，遮挡区域虚构细节可能不忠实于真实值。

**开放问题。**

1. **姿态估计误差的联合优化。** 当前流水线中，姿态估计与重建是解耦的。一个自然的问题是：能否通过可微渲染将重建损失反向传播至姿态参数，实现端到端的联合优化以减小误差传播？这需要解决 SMPL-X 参数在高斯渲染管线中的可微性问题。

2. **极端低分辨率下的身份保持。** 扩散细化器在低分辨率下的“合理想象”能力是一把双刃剑。如何在保持细节增强能力的同时约束身份一致性，是一个尚未解决的问题。可能的路径包括引入人脸/身份识别损失作为额外的监督信号，或在推理时通过交叉注意力机制注入身份嵌入。

3. **遮挡区域虚构细节的语义验证。** 论文未提供系统的方法来验证遮挡区域生成细节的语义正确性。对于服装纹理、配饰等身份相关属性，当前方法缺乏真值对齐的评估机制。这在实际应用（如数字人重建）中可能构成可靠性风险。

4. **多人交互建模。** 当前方法独立处理每个个体，未显式建模人与人之间的遮挡关系、接触约束或相对深度排序。在密集交互场景（如拥抱、握手）中，独立重建可能导致个体间的穿插或深度错位。

## 原文 PDF

![[paperPDFs/CVPR_2026/CrowdGaussian_Reconstructing_High_Fidelity_3D_Gaussians_for_Human_Crowd_from_a_Single_Image.pdf]]
