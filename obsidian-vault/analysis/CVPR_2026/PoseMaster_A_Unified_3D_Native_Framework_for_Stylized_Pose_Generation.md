---
title: "PoseMaster: A Unified 3D Native Framework for Stylized Pose Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PoseMaster_A_Unified_3D_Native_Framework_for_Stylized_Pose_Generation.pdf
project_link: null
code_link: null
aliases:
- PoseMaster
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 直接使用3D骨架作为控制信号，通过密集点云编码显式的空间坐标和拓扑关系，彻底消除2D投影歧义。
primary_logic: 将姿态风格化与3D原生生成统一在单一端到端框架中，用3D骨架提供精确的几何先验，避免级联误差，实现高保真度身份保持和严格姿态对齐。
claims:
- 级联管线中2D生成阶段的误差会直接传播并在3D重建中被放大。
- 3D骨架提供显式的空间坐标和拓扑关系，优于有歧义的2D骨架投影。
- PoseMaster在姿态规范化任务中MAE 4.59，大幅领先所有对比方法。
- VRoid (姿态规范化) 上 MAE↓ = 4.59
---

# PoseMaster: A Unified 3D Native Framework for Stylized Pose Generation

> [!tip] 核心洞察
> 将姿态风格化与3D原生生成统一在单一端到端框架中，用3D骨架提供精确的几何先验，避免级联误差，实现高保真度身份保持和严格姿态对齐。

| 字段 | 内容 |
|------|------|
| 中文题名 | PoseMaster：统一的三维原生风格化姿态生成框架 |
| 英文题名 | PoseMaster: A Unified 3D Native Framework for Stylized Pose Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.21076) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | PoseMaster |
| Dataset | VRoid |

> [!tip] 效果简介
> - VRoid (姿态规范化) 上，MAE↓ 4.59 (显著优于所有baseline)；SIM↑ 0.938 (显著优于所有baseline)；Uni3D-I↑ 0.402 (显著优于所有baseline)。
> - VRoid (任意姿态风格化) 上，MAE↓ 5.28 (显著优于所有baseline)；SIM↑ 0.935 (显著优于所有baseline)；Uni3D-I↑ 0.313 (显著优于所有baseline)。
> - VRoid (任意姿态风格化，Qwen-Image编辑输入) 上，MAE↓ 5.28 vs 8.15 (Hunyuan3D 2.1) (-2.87)。

## 概述

**问题瓶颈**：现有3D角色姿态风格化方法普遍采用级联管线——先通过2D扩散模型操控图像中的人物姿态，再将结果提升为3D表示。这一范式存在根本性缺陷：2D生成阶段引入的伪影、遮挡和不一致性会直接传播至3D重建阶段并被放大，同时2D骨架投影丧失深度信息，造成几何歧义，难以实现高保真度的身份保持与姿态对齐。

**核心洞察**：PoseMaster提出直接以3D骨架作为控制信号，通过密集点云编码显式的空间坐标和拓扑关系，彻底消除2D投影歧义，并将姿态风格化与3D原生生成统一在单一端到端框架中，从根本上避免级联误差。

**方法定位**：
- **控制信号革新**：从传统的2D骨架图像（如OpenPose骨架图）切换为3D骨架密集点云表示，包含3D坐标与骨骼方向向量，提供精确的几何先验。
- **架构统一**：摒弃“独立2D姿态编辑+独立3D重建”的级联范式，构建端到端的3D VAE + 3D DiT + 骨架编码器联合框架，以Hunyuan3D 2.1为backbone实现3D原生生成。
- **数据扩展**：设计可扩展的数据引擎，融合动态和静态3D资产，构造超过50万对象的“图像-骨架-网格”三元组，突破传统方法依赖少量可动画资产（如VRoid）的局限。

**主要结果**：在VRoid姿态规范化任务上，PoseMaster取得MAE 4.59、SIM 0.938，大幅领先所有对比方法；在任意姿态风格化任务上同样保持显著优势，且推理速度优于CharacterGen、StdGen等典型级联方案。消融实验证实，密集骨架表示和骨架引导对生成质量具有关键作用。

## 背景与动机

### 3D角色资产生成的范式演进

近年来，3D原生生成模型（如 **Trellis** 、**CraftsMan** 、**Hunyuan3D 2.1** ）在从单张图像重建高质量3D资产方面取得了显著进展。这些方法通常以A-pose（标准姿态）图像作为输入，通过3D VAE将几何编码为潜表示，再经由扩散Transformer进行生成。然而，当输入图像中的角色呈现任意复杂姿态时，这些模型往往难以保持身份一致性和几何精度，暴露出对姿态变化缺乏鲁棒控制的根本缺陷。

### 级联管线的结构性缺陷

为应对姿态操控需求，现有主流方案普遍采用级联架构：先通过独立的2D扩散模型对图像进行姿态编辑，再将编辑后的图像提升为3D表示。典型代表包括 **CharacterGen** 、**StdGen** 和 **SKDream**。这一范式存在两个致命弱点：

**误差传播与放大。** 2D生成阶段引入的伪影、遮挡和不一致性，在后续3D重建过程中会被直接放大，导致最终网格出现几何扭曲和身份漂移。正如原文所指出：“error propagation is inevitable; artifacts, occlusions, or inconsistencies introduced during the 2D generation phase are directly amplified in the 3D reconstruction”（置信度0.95）。

**2D投影的几何歧义。** 2D骨架图像（如OpenPose骨架图）本质上是3D姿态在特定视角下的投影，丧失了深度信息。同一2D骨架可能对应多种不同的3D姿态，这使模型难以获取精确的空间约束。原文强调：“Unlike 2D representations which suffer from projection ambiguity, 3D skeletons provide explicit spatial coordinates and topological relationships”（置信度0.95）。

### 数据瓶颈与泛化困境

级联方法的训练数据通常依赖少量可动画3D资产（如VRoid），其风格和数量均受限制，难以覆盖真实世界中丰富多样的角色外观和姿态。这进一步制约了模型的泛化能力，使其在面对开放式场景时表现脆弱。

### 本文动机

针对上述问题，PoseMaster提出了一种根本性的范式转换：**将姿态风格化与3D原生生成统一在单一端到端框架中**。核心动机包括：

1. **消除级联误差**：通过直接在3D潜空间中进行姿态条件生成，彻底绕过2D中间表示，避免误差传播。
2. **引入3D骨架作为无歧义控制信号**：利用密集点云编码显式的空间坐标和拓扑关系，为生成提供精确的几何先验。
3. **构建可扩展数据引擎**：融合动态和静态3D资产，构造超50万对象的“图像-骨架-网格”三元组，突破数据规模和多样性限制。

这一设计使PoseMaster在姿态规范化任务中取得MAE 4.59的指标，大幅领先所有对比方法（Table 1，置信度0.95），验证了3D原生姿态控制范式的有效性。

## 核心创新

PoseMaster 的核心创新在于将姿态风格化与三维原生生成统一为单一的端到端框架，彻底摒弃了传统级联管线中“先 2D 操控姿态、再 3D 重建”的范式。这一架构变革围绕三个关键的 **changed slots** 展开。

### 控制信号：从 2D 投影到 3D 骨架

传统方法（如 **CharacterGen** 、**StdGen** 、**SKDream** ）依赖 2D 骨架图像（如 OpenPose 骨架图）作为姿态控制信号。这类 2D 投影存在根本性缺陷：骨架投影丧失深度信息，同一 2D 骨架可对应多种不同的 3D 姿态，造成几何歧义。更严重的是，2D 生成阶段引入的伪影、遮挡和不一致性会直接传播到后续的 3D 重建阶段，并被不可逆地放大——这是级联管线固有的误差累积瓶颈（error propagation is inevitable; artifacts, occlusions, or inconsistencies introduced during the 2D generation phase are directly amplified in the 3D reconstruction）。

PoseMaster 直接使用 **3D 骨架密集点云** 作为控制信号（Figure 4）。与 2D 骨架投影不同，3D 骨架提供了显式的空间坐标和拓扑关系（unlike 2D representations which suffer from projection ambiguity, 3D skeletons provide explicit spatial coordinates and topological relationships），从根本上消除了投影歧义。具体而言，骨架被表示为一组密集采样点，包含 3D 坐标 $P_c$ 和骨骼方向向量 $P_f$，经位置编码和两层点 Transformer 块编码为姿态条件 $c_p$：

$$c_p = \phi_2(\phi_1(\tau([PE(P_c), P_f])))$$

这种密集表示（256 点）比稀疏关节包含更丰富的结构信息，消融实验（Figure 7）定性表明其能更准确地控制复杂姿态。

### 框架架构：从级联到端到端统一

传统级联管线由两个独立模型串行组成：2D 姿态编辑模型 + 3D 重建模型。这种解耦设计使得两个阶段的优化目标不一致，误差无法被联合修正。PoseMaster 将其统一为 **3D VAE + 3D DiT + 骨架编码器** 的端到端架构（Figure 2），所有模块在条件流匹配目标下联合优化：

$$\mathbb{E}_{t, x_0, x_1, c_i, c_p} \| v_\theta(x, t, c_i, c_p) - (x_1 - x_0) \|_2^2$$

其中 $c_i$ 由 DINOv2-Large（分辨率 518）从参考图像提取身份特征，$c_p$ 由骨架编码器从 3D 骨架提取姿态条件。推理时通过无分类器引导（CFG）融合骨架条件和图像条件：

$$\hat{v}_\theta = v_\theta(x_t, t, c_p, \emptyset) + \lambda \cdot (v_\theta(x_t, t, c_p, c_i) - v_\theta(x_t, t, c_p, \emptyset))$$

端到端设计使姿态约束和身份保持可以在潜空间中协同优化，避免了级联误差。

### 训练数据：可扩展的数据引擎

传统方法依赖少量可动画 3D 资产（如 VRoid），风格和数量均受限。PoseMaster 引入了一个可扩展的数据引擎，融合动态铰接网格和静态几何体，构造了超过 **50 万** 个独特人形对象的“图像-骨架-网格”三元组数据集（Figure 3）。这一规模优势使得模型能够学习到更丰富的身份-姿态联合分布，是端到端框架得以有效训练的基础保障。

### 创新效果的实证支撑

上述三个 changed slots 的协同作用在姿态规范化任务上得到了充分验证：PoseMaster 在 VRoid 测试集上取得 MAE 4.59、SIM 0.938、Uni3D-I 0.402、ULIP-I 0.161，大幅领先所有对比方法（Table 1）。消融实验进一步证实，带有骨架引导的生成在 MAE（4.82）和 SIM（0.946）上均显著优于无骨架引导的 baseline（Table 3），直接证明了 3D 骨架作为控制信号的核心价值。

## 整体框架

PoseMaster 将姿态风格化与三维原生生成统一在单一端到端框架中，其核心设计动机在于消除传统级联管线的误差传播瓶颈——二维扩散模型在操控图像姿态时产生的伪影、遮挡和不一致性，在后续三维重建阶段被直接放大，同时二维骨架投影丧失深度信息导致几何歧义。PoseMaster 通过直接使用三维骨架作为控制信号，以密集点云编码显式的空间坐标和拓扑关系，从根源上规避了二维投影歧义。

### 输入与输出

框架接收两类输入：一张参考图像（提供身份信息）和一个三维骨架（定义目标姿态）。输出为与参考图像保持身份一致、且严格对齐目标骨架姿态的高质量三维网格资产。Figure 2 展示了从输入到输出的完整数据流。

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/002_Figure_2.jpg]]
*Figure 2: OverallpipelineofourPoseMaster.Givenasingleimageanda3Dskeleton,ourPoseMaster integrates themintoaunifedD native generation framework to achieve precise pose stylization under 3D generation*

### 核心模块

流水线由四个核心模块构成，各模块职责明确、协同工作：

1. **图像编码器（Image Encoder）**：采用 DINOv2-Large 在分辨率 518 下从参考图像 $I_i$ 提取身份特征 $c_i$，作为生成过程中的外观条件。
2. **骨架编码器（Skeleton Encoder）**：对密集骨架点云（256 点）提取姿态条件 $c_p$。其处理流程为：对三维坐标 $P_c$ 施加位置编码（PE），与骨骼方向特征 $P_f$ 拼接后经线性投影至 1024 维，再通过两层点 Transformer 块进行特征聚合，最终输出姿态条件：
   $$c_p = \phi_2(\phi_1(\tau([PE(P_c), P_f])))$$
3. **三维变分自编码器（3D VAE）**：负责几何的编码与解码。编码器将三维几何压缩为 VecSet 潜表示，解码器从潜变量重建截断符号距离场（TSDF），进而提取显式网格。
4. **三维扩散 Transformer（3D DiT）**：在潜空间中进行基于流匹配的条件去噪。以 VAE 编码的几何潜变量为生成目标，融合图像条件 $c_i$ 和骨架条件 $c_p$，通过条件流匹配目标进行训练：
   $$\mathbb{E}_{t, x_0, x_1, c_i, c_p} \| v_\theta(x, t, c_i, c_p) - (x_1 - x_0) \|_2^2$$
   推理时采用无分类器引导（CFG），以骨架条件 $c_p$ 为必选条件、图像条件 $c_i$ 为可选条件，引导尺度 $\lambda$ 控制身份保持强度：
   $$\hat{v}_\theta = v_\theta(x_t, t, c_p, \emptyset) + \lambda \cdot (v_\theta(x_t, t, c_p, c_i) - v_\theta(x_t, t, c_p, \emptyset))$$

### 与级联管线的架构差异

传统方法（如 **CharacterGen** 、**StdGen** 、**SKDream** ）采用级联架构：独立的二维姿态编辑模型首先将输入图像操控至目标姿态，再由独立的三维重建模型提升为三维表示。这一分离式设计导致二维阶段的误差不可逆地传播至三维输出。PoseMaster 将控制信号从二维骨架图像替换为三维骨架密集点云，并将姿态操控与三维生成统一在 3D VAE + 3D DiT 的端到端框架中，联合优化，彻底消除了级联误差。

### 数据引擎支撑

为支撑统一框架的训练，PoseMaster 构建了可扩展的数据引擎（见 Figure 3），融合动态可动画资产与静态几何体，生成超 50 万对象的“图像-骨架-网格”严格对齐三元组，解决了传统方法依赖少量可动画资产导致的风格和数量受限问题。

### 补充图表

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/001_Figure_1.jpg]]
*Figure 1: Givenasingleimageandarbitraryposesrepresentedbya3Dskeleton,PoseMastercangenerateahighquality3Dsetthat maintains theidentityoftheimage whileahering totheposedfiedbytheskeleton,enablingrichand precise3Dposestylzation*

## 核心模块与公式推导

PoseMaster 的生成流水线由四个核心模块构成，围绕“3D 原生潜空间生成”这一主轴协同工作。

### 3D 变分自编码器（VAE）

3D VAE 负责几何的压缩与重建。它将输入的 3D 网格编码为 **VecSet 潜表示**，并在生成完成后将潜码解码为截断符号距离函数（TSDF），最终通过 Marching Cubes 提取显式网格。这一模块使得扩散过程可以在紧凑的潜空间中进行，大幅降低计算开销。

### 3D 扩散 Transformer（DiT）

DiT 是生成过程的核心引擎，采用**条件流匹配**范式在潜空间中运作。其训练目标为：

$$\mathbb{E}_{t, x_0, x_1, c_i, c_p} \| v_\theta(x, t, c_i, c_p) - (x_1 - x_0) \|_2^2$$

其中：
- $x_0$ 和 $x_1$ 分别为初始噪声和真实潜码；
- $x = t x_1 + (1-t) x_0$ 为线性插值路径上的中间状态；
- $v_\theta$ 是 DiT 预测的速度场；
- $c_i$ 为图像身份条件，$c_p$ 为姿态条件。

DiT 通过融合图像和骨架两种条件信号，引导去噪过程从随机噪声走向与参考身份一致且严格遵循目标姿态的几何潜码。

### 图像编码器

身份条件 $c_i$ 由 **DINOv2-Large** 在分辨率 518 下从参考图像中提取：

$$c_i = \text{DINOv2}(I_i)$$

该编码器提供语义级身份特征，确保生成网格的外观与输入人物保持一致。

### 骨架编码器

姿态条件 $c_p$ 是整个框架的差异化核心。骨架编码器接收**密集骨架点云**（默认 256 点），每点包含 3D 坐标 $P_c$ 和骨骼方向向量 $P_f$，通过以下流水线计算条件嵌入：

$$c_p = \phi_2(\phi_1(\tau([PE(P_c), P_f])))$$

具体流程为：
1. **位置编码** $PE(\cdot)$ 对 3D 坐标进行高频映射；
2. 将编码后的坐标与方向特征 $P_f$ 拼接，经线性投影 $\tau$ 映射至 1024 维；
3. 通过两层 **Point Transformer 块** $\phi_1, \phi_2$ 提取结构化的姿态条件。

这一设计使得骨架编码器能够显式捕获骨骼的空间坐标和拓扑关系，从根本上避免 2D 投影带来的几何歧义。

### 无分类器引导（CFG）

推理时，PoseMaster 采用无分类器引导来增强条件控制强度。速度预测公式为：

$$\hat{v}_\theta = v_\theta(x_t, t, c_p, \emptyset) + \lambda \cdot (v_\theta(x_t, t, c_p, c_i) - v_\theta(x_t, t, c_p, \emptyset))$$

其中 $\lambda$ 为引导尺度，$\emptyset$ 表示空条件。该公式在骨架条件始终生效的前提下，通过调节 $\lambda$ 控制图像身份条件的影响力度，在身份保持与姿态对齐之间取得平衡。

### 补充图表

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/004_Figure_4.jpg]]
*Figure 4: The skeleton representation of sparse joints and ours. We propose a distance-weighted interpolation scheme to densify the skeletal graph.Furthermore,explicit bone directional vectors are embedded into all interpolated points belonging to the same skeletal segment*

## 实验与分析

### 核心指标与主实验结果

PoseMaster 在两个核心任务上均显著超越级联式方案与三维原生基线：**姿态规范化**（将任意姿态图像转为 A‑pose 三维资产）与**任意姿态风格化**（输入任意姿态图像和目标骨架，生成姿态对齐的三维网格）。

**姿态规范化**（Table 1）。以 VRoid 测试集为基准，PoseMaster 在几何精度与身份保持方面全面领先。几何误差 MAE 低至 **4.59**，余弦相似度 SIM 达 **0.938**；三维语义一致性 Uni3D‑I 和 ULIP‑I 分别达到 **0.402** 和 **0.161**。作为对比，基于 2D 骨架操控再加三维重建的级联方法（如 CharacterGen 、StdGen 、SKDream ）因 2D 阶段引入的伪影和遮挡被直接放大到三维重建中，误差显著更高。即便将三维原生生成器 Trellis 和 CraftsMan 通过 StdGen 生成的 A‑pose 图像作为公平输入，其几何对齐与身份保持仍明显弱于 PoseMaster。这一差距的根源在于：级联管线中 2D 生成误差不可避免地向三维传播，而 PoseMaster 直接在三维潜空间中以 3D 骨架为条件进行生成，消除了投影歧义和误差累积。

**任意姿态风格化**（Table 2）。PoseMaster 的 MAE 为 **5.28**，SIM 为 **0.935**，Uni3D‑I 和 ULIP‑I 分别为 **0.313** 和 **0.172**，在所有指标上均优于对比方法。值得注意的是，当使用 Qwen‑Image 编辑的目标姿态图像作为基线输入时（Table 4），PoseMaster 的 MAE（5.28）比 Hunyuan3D 2.1 的 8.15 降低了 **2.87**，SIM 从 0.874 提升至 0.935。这说明即使为基线提供更“干净”的目标姿态图像，PoseMaster 直接以 3D 骨架为控制信号的优势依然突出。

定性结果（Figure 5、Figure 6）进一步印证了定量结论：PoseMaster 生成的网格在复杂姿态下仍能保持精确的骨骼对齐和身份一致性，而级联方法容易出现肢体错位、表面塌陷和身份漂移。

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/009_Figure_6.jpg]]
*Figure 6: Qualitativecomparisonofarbitrary-pose stylization.Forbaseies,weutilzethetarget-poseimages (GTmage)astheinput*

### 消融实验

消融实验围绕两个关键设计展开：**骨架引导的必要性**和**密集骨架表示的作用**。

**骨架引导的重要性**（Table 3、Figure 8）。移除骨架条件后，生成模型退化为纯图像到三维的映射。在 VRoid 测试集上，有骨架引导的 PoseMaster 取得 MAE **4.82**、SIM **0.946**，而无骨架引导的基线 MAE 和 SIM 均显著恶化。Figure 8 的定性对比显示，缺乏骨架约束时，生成的网格无法对齐目标姿态，出现严重的姿态漂移和几何失真。这直接验证了 3D 骨架作为显式空间先验的核心价值。

**密集骨架表示 vs. 稀疏关节**（Figure 7）。将骨架从稀疏关节替换为本文提出的密集点云表示（含骨骼方向向量）后，复杂姿态下的生成质量明显提升。稀疏关节表示在肢体扭转、关节旋转等场景下容易产生几何模糊，而密集表示通过距离加权插值和方向嵌入提供了更丰富的局部几何信息，使生成器能更准确地推断表面形变。该消融的定量对比原文以定性展示为主，建议查阅 Figure 7 的详细对比图以确认具体差异程度。

### 推理效率

Table 5 报告了推理速度对比。PoseMaster 的单阶段 3D 原生生成在推理时间上具有竞争力，具体数值需参阅原文表格。相较于级联方案需要依次运行 2D 姿态编辑和 3D 重建两个模型，PoseMaster 的端到端架构避免了中间结果的存储与传递开销。

### 失败模式与局限性

尽管 PoseMaster 在姿态对齐和身份保持方面表现优异，但分析揭示了两个主要局限：

1. **高频几何细节不足**。当前单阶段 512 分辨率生成在精细几何（如复杂手势、飘动的裙摆、发型）上仍面临挑战，生成质量落后于多阶段精炼方法。这源于单阶段潜空间解码的容量限制，难以同时捕捉全局姿态和局部高频细节。
2. **纹理与几何解耦**。PoseMaster 将几何生成与纹理生成分离为独立任务，纹理需借助外部编辑和纹理模型后处理。这种解耦导致纹理与几何之间可能出现姿态不一致，例如纹理中的阴影方向与生成几何的法线不匹配。

### 评估公平性说明

评估体系针对三维生成任务的特点做了两项重要设计：① 几何质量采用渲染法线图的平均角度误差（MAE）和余弦相似度（SIM），在 36 个方位角（间隔 10°）渲染并取最佳匹配分数，有效规避了生成网格与真实网格空间未对齐带来的评估偏差；② 对于不支持姿态操控的三维原生模型，使用 StdGen 生成的 A‑pose 图像作为公平输入，确保所有方法在同一 VRoid 测试集上评价。

### 补充图表

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/006_Table_1.jpg]]
*Table 1: The quantitative comparison for pose canonicalization onan arbitrary-pose image from the VRoid[7] test dataset.“*" denotes that these methods leverage the image-based pose canonicalization method to obtain the A-pose image input*

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/008_Figure_7.jpg]]
*Figure 7: The qualitative comparison between different pose representations in terms of joints and bones of the skeleton*

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/010_Figure_8.jpg]]
*Figure 8: The ablation study for the importance of skeleton guidance in 3D generation*

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/012_Table_3.jpg]]
*Table 3: Quantitative comparison for skeleton guidance.With the skeleton guidance,our method achieves better performance in the task of image-to-3D generation*

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/014_Table_4.jpg]]
*Table 4: The quantitative comparison for arbitrary pose stylization by using the target-pose images edited from Qwen-Image [55] as the baselines’input*

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/011_Figure_9.jpg]]
*Figure 9: The application of our PoseMaster for animation.Our method can generate the skeleton-body alignment mesh,which can be easily used to animate by introducing a skinning model*

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/019_Figure_14.jpg]]
*Figure 14: The system of 3D printing based on our PoseMaster. PoseMaster can customize the pose of a character from a single image for figure printing*

![[assets/figures/papers/paper_list_l2573_https_arxiv_org_abs_2506_21076/figures/003_Figure_3.jpg]]
*Figure 3: ．Overview of the dataset construction pipeline.Our approach integrates both dynamic articulated meshes and static geometries to curate a large-scale dataset consisting of strictly aligned image-skeleton-mesh triplets*

## 方法谱系与知识库定位

### 方法谱系：从级联2D操控到3D原生生成

PoseMaster的核心突破在于**将姿态风格化从“2D投影操控+3D重建”的级联范式迁移到统一的3D原生生成框架**。理解这一迁移的关键在于识别级联范式的根本性瓶颈。

**级联范式的误差传播瓶颈**。CharacterGen、StdGen、SKDream等代表性方法遵循相同的两阶段逻辑：首先通过2D扩散模型（如ControlNet类架构）对输入图像进行姿态编辑，生成目标姿态的2D图像；然后将该图像送入3D重建模型（如LRM系列或Hunyuan3D）提升为3D表示。这一级联设计的致命缺陷在于：2D生成阶段引入的伪影、遮挡和不一致性会**直接传播并在3D重建阶段被放大**（error propagation is inevitable; artifacts, occlusions, or inconsistencies introduced during the 2D generation phase are directly amplified in the 3D reconstruction）。此外，2D骨架图像本质上是3D姿态在特定视角下的投影，丧失了深度信息，导致几何歧义——同一2D骨架可以对应多种3D姿态，级联管线对此缺乏约束能力。

**3D原生生成器的姿态操控缺失**。另一类方法如Trellis、CraftsMan、Hunyuan3D 2.1直接在3D潜空间中进行生成，避免了2D-3D提升的误差，但它们以A-pose等规范姿态图像为输入，本身不具备任意姿态操控能力。当需要姿态风格化时，仍需借助外部2D姿态编辑模型（如StdGen）先生成目标姿态图像再输入，实质上退化回级联范式。PoseMaster选择Hunyuan3D 2.1作为backbone，正是基于其成熟的3D原生生成能力，但关键改造在于**将3D骨架作为原生控制信号注入生成过程**，使姿态操控与3D生成在单一端到端模型中联合优化。

**控制信号的本质升维**。从2D骨架图像到3D骨架密集点云的转变不是简单的输入替换，而是控制信号从“有歧义的投影”到“显式空间约束”的质变。3D骨架提供显式的空间坐标和拓扑关系（Unlike 2D representations which suffer from projection ambiguity, 3D skeletons provide explicit spatial coordinates and topological relationships），使网络能够直接获取骨骼关节在三维空间中的精确位置和骨骼段的方向向量，从根本上消除了投影歧义。这种设计使得姿态条件从“图像层面的风格参考”变为“几何层面的硬约束”，是PoseMaster在姿态精度指标上大幅领先的因果机制。

### 适用边界与局限性

**精细几何细节的生成瓶颈**。PoseMaster当前采用单阶段512分辨率生成，在处理复杂手势、飘动的裙摆、发型等高频几何细节时保真度不足。这与多阶段精炼方法（如使用超分辨率模块或神经隐式表面精炼）形成对比，后者通过级联精炼可以捕捉更细粒度的几何特征，但代价是管线复杂度和推理时间增加。PoseMaster选择单阶段设计优先保证了端到端的一致性和推理效率，但精细细节的缺失是其明确的适用边界。

**几何-纹理解耦带来的不一致风险**。当前框架将几何生成与纹理生成分离为独立任务，纹理需借助外部编辑和纹理模型后处理。这种解耦设计虽然简化了训练目标，但引入了姿态不一致的风险——纹理映射可能无法准确跟随3D骨架驱动的几何变形，尤其在极端姿态下可能出现纹理拉伸或错位。联合优化几何与纹理以消除这种不一致，是框架进一步完善的开放方向。

**复杂拓扑结构的泛化挑战**。PoseMaster的训练数据以类人骨架结构为主，对于非标准骨架（如多臂、尾部附着）或宽松衣物（如斗篷、长袍）等复杂拓扑的泛化能力尚未验证。骨架密集点云表示依赖骨骼长度和空间间隔参数（如0.005），这些超参数在非标准拓扑下可能需要重新标定。

### 开放问题

1. **高分辨率几何精炼的集成**：如何在保持端到端一致性的前提下，引入高分辨率几何精炼模块（如级联的神经隐式表面优化或可微分网格细分），以提升输出网格的细节真实度，同时避免重蹈级联误差的覆辙？

2. **通用拓扑的姿态风格化**：如何将3D骨架控制信号扩展到非标准骨架和宽松衣物等复杂拓扑结构，使框架具备更通用的姿态风格化能力？这可能需要骨架表示的自适应稠密化策略或拓扑感知的条件编码。

3. **几何-纹理联合优化**：如何在统一框架内实现几何与纹理的联合生成或联合优化，从根本上消除姿态不一致问题？这涉及到将纹理生成纳入流匹配目标，或在潜空间中建立几何-纹理的耦合表示。

## 原文 PDF

![[paperPDFs/CVPR_2026/PoseMaster_A_Unified_3D_Native_Framework_for_Stylized_Pose_Generation.pdf]]