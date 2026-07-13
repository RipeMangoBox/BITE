---
title: "FairyGen: Storied Cartoon Video from a Single Child-Drawn Character"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/FairyGen_Storied_Cartoon_Video_from_a_Single_Child_Drawn_Character.pdf
project_link: https://jayleejia.github.io/FairyGen/
code_link: null
aliases:
- FairyGen
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 解耦角色建模与风格化背景生成，引入3D代理重建来提供物理合理且可控的运动先验，并采用两阶段运动定制与偏置时间步采样策略，使得视频扩散模型能够忠实保留角色外观并学习流畅运动。
primary_logic: 通过将风格传播限制在背景区域并利用3D代理的运动先验来微调图像到视频扩散模型，能够有效分离外观、运动与风格，从而在单儿童画输入下生成高质量的故事动画。
claims:
- 在风格对齐度量（CLIP距离）上，FairyGen显著优于B-LoRA、InstantStyle与DreamBooth等基线。
- 在VBench运动平滑度与主题一致性指标上，FairyGen优于深度引导Wan2.1、姿态引导Animate-X等现有视频动画方法。
- 大规模用户研究（3360次评价）一致显示，FairyGen在风格对齐、运动真实感与视觉连贯性方面更受偏好。
- 两阶段运动适配器与时间步移采样策略是获取高质量、自然运动的关键，消融实验证明了其有效性。
---

# FairyGen: Storied Cartoon Video from a Single Child-Drawn Character

> [!tip] 核心洞察
> 通过将风格传播限制在背景区域并利用3D代理的运动先验来微调图像到视频扩散模型，能够有效分离外观、运动与风格，从而在单儿童画输入下生成高质量的故事动画。

| 字段 | 内容 |
|------|------|
| 中文题名 | FairyGen: 基于单个儿童绘角色生成叙事卡通视频 |
| 英文题名 | FairyGen: Storied Cartoon Video from a Single Child-Drawn Character |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2506.21272) · [Project](https://jayleejia.github.io/FairyGen/) · [paper](https://arxiv.org/abs/2503.11647) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FairyGen |
| Dataset |  |

> [!tip] 效果简介
> - 风格评价（自定义儿童画数据集） 上，CLIP风格对齐距离 (Style Align) 0.6580 vs 未明确列出各基线单值，但全面优于StyleDrop、B-LoRA、InstantStyle等 (未明确，由Table 1定性比较)。
> - 用户偏好研究 上，风格质量投票 (Style Quality) 0.5365 vs 次优方法显著低于该值 (未明确，凭用户偏好胜出)。
> - 运动评价 (VBench指标) 上，运动平滑度 (Motion Smooth.) 0.987 vs 未提供具体值，但优于Animate-X、DreamVideo等 (未明确，由Table 2定性比较)。

## 概要

**问题瓶颈**：从单幅儿童手绘角色生成连贯的叙事卡通视频，面临三重根本矛盾——角色风格的高度抽象性与背景风格一致性的冲突、单样本条件下跨镜头角色外观的持久保持、以及结构化电影叙事控制与复杂自然运动生成之间的协调。现有故事视频方法往往将风格、外观与运动耦合建模，导致在儿童画这种极端低资源条件下出现风格泄漏、身份漂移或运动不自然。

**核心方法**：FairyGen 提出一套解耦生成框架，通过三条因果链路分别突破上述瓶颈。其一，引入前景掩码引导的 DoRA 风格传播适配器与 BrushNet 画布补全，将风格学习限制在前景区域、推理时反向传播至背景，实现风格与角色的精确分离。其二，基于 DrawingSpinUp 从二维草图重建三维代理，通过骨骼绑定与运动重定向获取物理可信的运动先验，为视频扩散模型提供结构化运动引导。其三，设计两阶段运动定制策略——先以打乱帧训练身份 LoRA 锁定角色外观，再冻结身份分支、以顺序帧学习运动残差，并辅以偏置时间步采样（晚时步侧重），使视频扩散模型能忠实保留角色特征并习得流畅运动。

**主要结果**：在风格对齐度量（CLIP 距离）上，FairyGen 显著优于 **StyleDrop** (Sohn et al., arXiv 2023)、**B-LoRA** (Frenkel et al., 2025) 与 **InstantStyle** 等风格化基线；在 VBench 运动平滑度与主题一致性指标上，优于深度引导 **Wan2.1** (Wan et al., 2025) 与姿态引导 **Animate-X** (Tan et al., 2024) 等视频动画方法。大规模用户研究（3360 次评价）一致显示，FairyGen 在风格对齐、运动真实感与视觉连贯性方面更受偏好。消融实验证实，两阶段运动适配器与时间步移采样是获取高质量自然运动的关键设计。

**局限与开放问题**：当前方法针对单角色设计，扩展到多角色及交互场景仍面临挑战；受视频扩散模型不可控先验限制，背景运动可能与前景不协调；对于高度抽象的非人形角色，三维代理的绑定与重定向存在局限性。未来方向包括结合更先进的骨骼绑定技术（如 UniRig）提升非人形角色运动质量，以及引入更丰富的相机运动控制增强背景真实感。

视觉叙事生成旨在将一段文本故事转化为连贯的图像或视频序列，这要求系统同时解决角色外观一致性、场景风格统一以及跨镜头的运动连贯性三大挑战。近年来，扩散模型（Diffusion Models）在文本到图像（T2I）和文本到视频（T2V）生成领域取得了显著进展，催生了一系列主体定制与风格化方法。然而，当输入从高质量照片或规范插图变为**儿童手绘角色**时，现有方法的局限性便集中暴露出来。

**核心瓶颈**在于：儿童画具有高度抽象、线条简略、比例失调等特性，现有方法难以在**单一样本**的条件下同时保持风格一致性、跨镜头角色一致性以及复杂自然运动。具体而言，以 **StyleDrop**（Sohn et al., arXiv 2023）和 **B-LoRA**（Frenkel et al., 2025）为代表的风格化定制方法，通常采用全局风格适配器进行微调，容易将前景角色的风格不加区分地“涂抹”到背景上，导致角色细节丢失或背景风格不协调。而以 **DreamBooth**（Ruiz et al., CVPR 2023）为代表的主体定制方法，虽能保留角色外观，却难以将其自然嵌入风格化的叙事场景中。在视频生成侧，基于深度引导的 **Wan2.1**（Wan et al., 2025）和基于姿态引导的 **Animate-X**（Tan et al., 2024）等方法，依赖显式的几何约束（深度图或骨骼姿态）来驱动运动，但这类约束对于抽象手绘角色往往难以精确提取，且无法有效处理角色外观与背景风格的协调问题。此外，端到端的外观与运动联合定制方法如 **DreamVideo**（Wei et al., CVPR 2024），在单样本条件下容易将外观与运动信息纠缠学习，导致角色身份退化或运动不自然。

更深层的缺口在于**结构化的电影叙事控制**。现有方法大多聚焦于单镜头生成或简单的风格迁移，缺乏对故事板（Storyboard）层面的规划——包括场景划分、角色动作描述、镜头视角设计等。这使得生成的动画序列缺乏叙事连贯性与视觉表达力，难以真正实现从“一幅画”到“一部短片”的跨越。

FairyGen 正是在这一背景下提出的，其核心动机在于：**解耦角色建模与风格化背景生成，引入3D代理重建来提供物理合理且可控的运动先验，并采用两阶段运动定制与偏置时间步采样策略，使得视频扩散模型能够忠实保留角色外观并学习流畅运动。** 通过将风格传播限制在背景区域并利用3D代理的运动先验来微调图像到视频扩散模型，FairyGen 有效分离了外观、运动与风格三个维度，从而在单儿童画输入下生成高质量的故事动画。

## 核心方法与创新机理

FairyGen 的核心创新在于**将风格传播、运动生成与角色外观三者解耦**，从而在仅给定单幅高度抽象的手绘角色时，仍能生成风格一致、运动流畅的多镜头叙事视频。这一解耦思想通过三个关键的 **changed slots** 实现，分别对应风格、运动和训练策略的范式转换。

### 1. 从全局风格注入到掩码引导的风格传播

现有风格化方法（如 **StyleDrop**（Sohn et al., arXiv 2023）、**B-LoRA**（Frenkel et al., 2025）、**InstantStyle**）通常对扩散模型进行全局风格微调或注入，难以在保留角色身份的同时将风格准确迁移至背景。FairyGen 提出了一种**前景掩码引导的 DoRA 适配器 + BrushNet 画布补全**机制（Fig. 4），实现了风格的角色-背景分离传播：

- **训练阶段**：通过前景掩码 $m$ 约束 DoRA 适配器仅学习前景区域的风格特征（Eq. 2: $y = W x + P A ( x \cdot m )$）；
- **推理阶段**：将学到的风格适配器作用于背景区域 $(1-m)$，配合 BrushNet 完成风格化背景补全（Eq. 3: $y = W x + P A ( x \cdot ( 1 - m ) )$）。

这一设计使得角色外观得以原样保留，而背景风格与角色高度一致。消融实验（Fig. 8）证实 DoRA 在风格化保真度上显著优于原始 LoRA，Table 1 的定量结果显示 FairyGen 在 CLIP 风格对齐距离（0.6580）和用户风格质量评分（0.5365）上均全面领先基线。

### 2. 从直接视频约束到 3D 代理驱动的物理合理运动

现有图像到视频动画方法（如深度引导 **Wan2.1**（Wan et al., 2025）、姿态引导 **Animate-X**（Tan et al., 2024））直接利用 ControlNet 约束视频扩散模型，但面对复杂运动时容易出现外观漂移和运动不自然。FairyGen 引入了**基于 3D 代理重建的运动生成范式**（Sec. 4.3）：

- 利用 DrawingSpinUp 从单张二维草图重建三维代理模型；
- 通过骨骼绑定与运动重定向，获得物理可信的运动序列作为先验；
- 将该运动序列用于微调 MMDiT 视频扩散模型，而非直接条件约束。

这一范式转换使模型能够从 3D 代理中继承物理合理性，避免了端到端学习中对运动-外观耦合的过拟合。Table 2 显示，FairyGen 在 VBench 运动平滑度（0.987）和用户运动真实感评分（0.780）上均优于现有动画方法。

### 3. 从单阶段混合学习到两阶段解耦 + 偏置时间步采样

传统视频定制方法（如 **DreamVideo**（Wei et al., CVPR 2024））采用单阶段 LoRA 微调，外观与运动信息混合学习，且使用均匀时间步采样，导致角色身份保持与运动质量难以兼得。FairyGen 提出了**两阶段运动适配器**与**时间步移采样**策略（Fig. 5）：

- **Stage 1 — 身份 LoRA**：在时间维度上打乱帧顺序进行训练，迫使模型学习空间外观特征而不引入时序偏差，同时施加 dropout 防止过拟合（Eq. 4: $y = W x + A_{\mathrm{id}} B_{\mathrm{id}} x$）；
- **Stage 2 — 运动 LoRA**：冻结身份适配器，在顺序视频帧上学习运动残差变形（Eq. 5: $y = W x + A_{\mathrm{id}} B_{\mathrm{id}} x + A_{\mathrm{id}} B_{\mathrm{motion}} x$），实现外观与运动的彻底解耦；
- **时间步移采样**：通过 Logistic 变换将高斯分布 $\mathcal{N}(\mu, \sigma^2)$ 映射为晚时步偏置采样（$\mu=6$），使扩散模型更关注动态细节的学习。

消融实验（Fig. 9）表明，两阶段策略显著提升了角色外观一致性；Fig. 12 证实时间步移采样使模型学到更自然流畅的运动，相比均匀采样优势明显。

### 创新总结

| 创新维度 | 基线范式 | FairyGen 范式 | 核心机制 |
|---------|---------|--------------|---------|
| 风格传播 | 全局风格 LoRA / 注入 | 掩码引导 DoRA + BrushNet | 前景学习、背景迁移 |
| 运动生成 | ControlNet 直接约束 | 3D 代理重建 → 微调 | 物理先验注入 |
| 训练策略 | 单阶段 LoRA + 均匀采样 | 两阶段解耦 + 晚时步偏置 | 外观-运动分离学习 |

这三个 changed slots 协同作用，使得 FairyGen 能够在单儿童画输入的极端条件下，同时达成风格一致性、跨镜头角色一致性与复杂自然运动，构成了方法的核心竞争力。

FairyGen 的整体流程围绕“从单幅儿童绘角色到多镜头叙事卡通视频”这一目标，将风格、运动与叙事控制解耦为四个协同阶段：**故事板规划**、**风格传播场景生成**、**三维代理运动重建** 与**两阶段视频运动定制**。图 2 给出了端到端的流水线概览。

### 输入与输出

- **输入**：一幅儿童手绘的角色图像，以及一段简短的故事梗概（例如“一只小猫在花园里玩耍”）。
- **输出**：一段多镜头、风格统一的卡通视频，其中前景角色保持原始手绘外观，背景场景与角色风格一致，且运动自然连贯。

### 流水线模块

1. **MLLM 故事板规划器（Storyboard Planner）**  
   首先，利用多模态大语言模型（MLLM）将用户提供的故事梗概展开为结构化的分镜脚本。该脚本以层级结构组织：全局叙事概览 + 逐镜头的详细描述，涵盖场景、事件、角色动作、背景以及镜头视角（如特写、中景、全景）。这一步骤为后续的视觉生成与剪辑提供了精确的语义指导（参见图 3）。

2. **风格传播适配器（Style Propagation Adapter）**  
   在故事板生成后，系统进入风格化场景生成阶段（参见图 4）。该模块基于预训练的 SDXL 文本到图像扩散模型，引入 **DoRA 风格传播适配器** 与 **BrushNet 画布补全网络**。其核心机制是：训练时，通过前景掩码 $m$ 仅在前景区域学习角色的视觉风格（$y = W x + PA(x \cdot m)$）；推理时，将学习到的风格传播至背景区域（$y = W x + PA(x \cdot (1 - m))$），从而在保留角色身份的同时，生成风格一致的完整场景。

3. **三维代理运动重建（3D Proxy Reconstruction）**  
   为获取物理可信的运动先验，系统利用 **DrawingSpinUp** 从单张二维手绘角色重建三维代理模型，并通过骨骼绑定与运动重定向生成一系列符合物理规律的动作序列。这一步骤有效弥补了二维草图在运动信息上的缺失，为后续视频扩散模型提供了强约束的运动引导。

4. **两阶段运动适配器与时间步移采样（Two-Stage Motion Adapter & Timestep-Shift Sampling）**  
   在图像到视频生成阶段，FairyGen 采用 **MMDiT 视频扩散模型** 并实施两阶段定制训练（参见图 5）：
   - **第一阶段（身份 LoRA）**：在时序打乱的帧上训练身份适配器，学习角色的空间外观特征，避免引入时序偏置（$y = W x + A_{\mathrm{id}} B_{\mathrm{id}} x$）。
   - **第二阶段（运动 LoRA）**：冻结身份 LoRA，在顺序视频帧上学习运动残差变形（$y = W x + A_{\mathrm{id}} B_{\mathrm{id}} x + A_{\mathrm{id}} B_{\mathrm{motion}} x$），实现外观与运动的解耦。
   同时，在运动定制阶段引入 **时间步移采样**（通过 Logistic 变换将高斯分布映射为晚时步偏置），强化扩散模型对动态细节的学习能力，从而生成更自然流畅的运动。

### 模块间关系与数据流

上述模块以串行-反馈的方式协同工作：故事板规划器为风格传播模块提供场景描述；风格传播模块生成风格一致的静态场景后，再根据故事板中的镜头视角进行裁剪与合成；三维代理重建模块独立生成运动序列；最终，两阶段运动适配器将静态场景与运动序列融合，驱动视频扩散模型生成动画。这种解耦设计使得前景角色、背景风格与运动三者互不干扰，从而在单样本条件下实现高质量的故事视频生成。

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2506_21272/figures/002_Figure_1.jpg]]
*Figure 1: We present FairyGen, a visual story generation framework to generate multi-shot cartoon videos from a single child-drawn character with consistent style and motion between the foreground and the background. Project page: https://jayleejia.github.io/FairyGen/*

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2506_21272/figures/003_Figure_2.jpg]]
*Figure 2: The pipeline of the whole FairyGen*

FairyGen 的核心设计围绕一个关键矛盾展开：如何在仅有一张高度抽象、风格鲜明的儿童手绘角色的条件下，生成风格一致、运动自然且叙事连贯的多镜头视频。为此，框架通过三个相互解耦的模块——**故事板规划器**、**风格传播适配器**与**基于3D代理的运动定制器**——分别解决叙事结构缺失、风格一致性难以保持、运动生成不可控这三个瓶颈，并通过精心设计的训练策略与采样机制将它们统一到一个端到端的生成管线中。

### 故事板规划器：从叙事到镜头描述

故事板规划器利用多模态大语言模型（MLLM）将用户提供的简短故事梗概转化为结构化的电影分镜描述。其输出包含两个层级：全局叙事概览与逐镜头的详细故事板，每个镜头明确指定场景、事件、角色动作、背景描述以及相机镜头视角（如特写、中景、全景）。这一层级化结构为后续的视觉生成提供了明确的语义约束，使得风格化场景生成与运动定制能够针对每个镜头的具体需求进行适配，而非盲目生成。

### 风格传播适配器：解耦前景身份与背景风格

风格传播适配器是解决“风格一致性”瓶颈的核心模块。其关键洞察在于：儿童手绘角色的视觉风格（如笔触、色彩、纹理）应当被精确学习，但仅传播到背景区域，而前景角色的身份特征必须被完整保留。为此，该模块基于预训练的文本到图像扩散模型 SDXL，引入了一个**传播适配器（Propagation Adapter，PA）**，并通过前景掩码 $m$ 实现训练与推理阶段的不对称操作。

在训练阶段，适配器仅在前景区域学习风格特征，其更新公式为：

$$y = W x + P A ( x \cdot m )$$

其中 $W$ 为原始模型权重，$PA$ 为传播适配器，$m$ 为前景二值掩码。这意味着适配器仅从前景角色的视觉信息中提取风格表征。

在推理阶段，适配器将学习到的风格作用于背景区域，公式切换为：

$$y = W x + P A ( x \cdot ( 1 - m ) )$$

此时，前景区域 $(m)$ 保持原始角色身份，背景区域 $(1-m)$ 接收风格迁移。此外，该模块采用 **DoRA**（Weight-Decomposed Low-Rank Adaptation）替代传统 LoRA 作为适配器的参数化形式，以增强风格传播的保真度。同时，引入 **BrushNet** 作为画布补全模块，确保生成的背景与前景在语义和视觉上无缝融合。

### 基于3D代理的运动定制器：从物理先验到视频扩散

运动定制器解决的是“复杂自然运动与角色外观一致性”的双重挑战。其核心思路是：不直接从二维图像学习运动，而是先通过 **DrawingSpinUp** 从单张二维草图重建角色的三维代理模型，再进行骨骼绑定与运动重定向，从而获得物理合理、可控的运动序列。这一3D代理提供了强先验，避免了纯二维方法在面对高度抽象角色时容易产生的形变与身份漂移。

获得运动序列后，FairyGen 采用**两阶段运动适配器**对图像到视频扩散模型（基于 MMDiT 架构）进行微调，显式解耦外观学习与运动学习：

**阶段一：身份LoRA。** 将视频帧顺序打乱后训练，迫使模型仅学习角色的空间外观特征，消除时间相关性。其适配特征为：

$$y = W x + A_{\mathrm{id}} B_{\mathrm{id}} x$$

其中 $A_{\mathrm{id}} B_{\mathrm{id}}$ 为身份低秩适配矩阵。训练中还对 $B_{\mathrm{id}}$ 施加 dropout，进一步抑制时序模式的残留。

**阶段二：运动LoRA。** 冻结身份LoRA，使用顺序视频帧训练运动残差变形。此时特征更新为：

$$y = W x + A_{\mathrm{id}} B_{\mathrm{id}} x + A_{\mathrm{id}} B_{\mathrm{motion}} x$$

运动适配矩阵 $B_{\mathrm{motion}}$ 被约束为在身份特征 $A_{\mathrm{id}}$ 的基础上学习残差，而非独立建模。这种设计使得运动学习不会破坏已建立的角色外观，同时允许复杂动态（如跑步、跳跃）被自然嵌入。

### 时间步移采样：强化动态细节学习

在运动定制阶段，FairyGen 进一步引入**时间步移采样**策略，以增强扩散模型对动态细节的建模能力。其动机在于：扩散模型的早期去噪步骤主要决定全局结构，晚期步骤则负责细节生成；运动细节（如肢体摆动、衣物飘动）更依赖晚期步骤的建模精度。因此，FairyGen 采用 Logistic 变换将高斯分布映射为偏置采样：

$$t = \sigma(z) = \frac{1}{1 + e^{-z}}, \quad z \sim \mathcal{N}(\mu, \sigma^2)$$

其中 $\mu=6$ 使采样集中在较晚的时间步。消融实验证实，这一策略相比均匀采样能显著提升生成视频的运动平滑度与自然度。

### 模块间的因果关联

三个核心模块并非孤立运作，而是通过信息流形成因果链：故事板规划器提供镜头级语义约束 → 风格传播适配器生成风格一致的静态场景 → 3D代理提供物理运动先验 → 两阶段运动适配器将静态场景与运动序列融合为动态视频。这种解耦设计使得每个模块可以独立优化，同时通过明确的接口（掩码、运动序列、适配器权重）实现端到端的协同。

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2506_21272/figures/004_Figure_3.jpg]]
*Figure 3: The pipeline of the storyboard generation. We first plan the whole story using the M-LLM and build a storyboard containing the scenes, events, character action, background, and camera shots. Then, we crop the stylized image using different camera shot and generate final shot images*

## 实验与关键发现

### 主实验结果

#### 风格化质量评估

FairyGen 在风格对齐、文本对齐与用户偏好上均展现出显著优势。Table 1 汇总了风格化方法的定量对比。在基于 CLIP 的风格对齐距离（Style Align）上，FairyGen 取得 **0.6580**，全面优于 **StyleDrop**（Sohn et al., arXiv 2023）、**B-LoRA**（Frenkel et al., 2025）与 **InstantStyle** 等基线方法。用户偏好研究进一步验证了这一优势：在风格质量投票（Style Quality）中，FairyGen 获得 **0.5365**，远高于次优方法。

值得注意的是，在视觉印象（Visual Impression）指标上，FairyGen 得分为 **0.3251**，略低于 B-LoRA 的 0.3429（差距 -0.0178）。这一差异可归因于 B-LoRA 倾向于生成照片级真实感图像，而 FairyGen 的目标是保持手绘卡通风格的一致性——这恰恰是任务需求所在，而非方法缺陷。

定性比较（Fig. 7）直观展示了 FairyGen 的优势：StyleDrop 与 B-LoRA 在背景风格化时容易出现前景角色外观失真或风格不协调，而 FairyGen 的前景掩码引导风格传播机制能够精确地将角色风格迁移至背景，同时完整保留角色的视觉身份。

#### 运动定制质量评估

Table 2 展示了运动定制方法的定量对比。在 VBench 运动平滑度（Motion Smoothness）上，FairyGen 达到 **0.987**，显著优于深度引导 **Wan2.1**（Wan et al., 2025）、姿态引导 **Animate-X**（Tan et al., 2024）以及外观与运动联合定制方法 **DreamVideo**（Wei et al., CVPR 2024）。在用户研究中，FairyGen 的运动真实感（Motion Realness）得分高达 **0.780**，体现了基于 3D 代理的运动先验对物理合理性的关键贡献。

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2506_21272/figures/011_Figure_9.jpg]]
*Figure 9: Ablation on two-stage Motion Adapter. We ablated the twostage adapters in our proposed motion customization in image-to-video generation. Here, the first stage of training improves the identity similarity. 24 stylized image sets, each set contains 4 different methods, and needs to be evaluated from two aspects. As for motion, we utilize 12 video sets using 3 different methods, and the users need to be evaluated from two aspects. Finally, we obtain 3360 opinions. As shown in tables, the users consistently prefer our method in terms of style alignment, motion realism, and visual coherence. As shown in Tab. 1, our method achieves the highest score in style similarity, surpassing B-LoRA, Instan...*

Fig. 6 的定性对比揭示了各方法的典型失败模式：深度引导 Wan2.1 在处理复杂运动时，角色外观容易发生形变或与背景融合模糊；姿态引导 Animate-X 虽能跟随骨骼运动，但难以保持手绘角色的风格化纹理细节。FairyGen 通过两阶段运动适配器（先身份后运动）与时间步移采样，在保留角色外观的同时生成了与原运动序列高度一致的流畅动画。

#### 多事件视频生成

FairyGen 的前背景解耦建模策略在多事件、长时序视频生成中展现出独特优势（Fig. 10）。与端到端方法相比，分离前景角色与背景场景的建模使得跨镜头的风格一致性更易维持，且支持更灵活的镜头切换与场景变化。与 DreamVideo 的全面对比（Fig. 11）显示，FairyGen 在风格化质量、运动自然度与整体视觉质量上均显著领先。

### 消融实验

#### 风格传播适配器：DoRA vs. LoRA

Fig. 8 对比了 DoRA 与原始 LoRA 在风格传播任务上的表现。实验表明，DoRA 的风格化传播效果明显优于 LoRA：LoRA 在将前景风格迁移至背景时，常出现风格不完整或纹理模糊的问题，而 DoRA 能够更精确地捕获并传播角色的视觉风格特征，在不同文本提示下均生成风格一致的背景场景。

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2506_21272/figures/012_Figure_8.jpg]]
*Figure 8: Ablation Study on Style Customization. Compared with the baseline LoRA [Hu et al. 2021] and DoRA [Liu et al. 2024b], the proposed method can successfully propagate the foreground style to the background with different prompts. Best viewed with zoom in*

#### 两阶段运动适配器

Fig. 9 消融了两阶段训练策略的有效性。仅采用单阶段直接训练（外观与运动混合学习）时，生成视频中的角色身份一致性显著下降，尤其在复杂运动下容易出现外观漂移。引入第一阶段身份 LoRA（打乱帧训练）后，角色外观保持能力大幅提升；在此基础上冻结身份权重、仅学习运动残差的第二阶段训练，进一步保证了运动的流畅性与自然度。

#### 时间步移采样

Fig. 12 验证了时间步移采样策略对运动质量的提升效果。采用均匀时间步采样时，扩散模型倾向于学习静态外观特征，对动态细节的捕捉不足，导致生成的运动僵硬、不自然。引入偏置时间步采样（μ=6 的 Logistic 变换分布）后，模型在晚时步（高噪声阶段）获得更多训练信号，从而学会了更自然、流畅的运动表示。

![[assets/figures/papers/paper_list_l92_https_arxiv_org_abs_2506_21272/figures/015_Figure_12.jpg]]
*Figure 12: Ablation Study on timestep shift. The proposed timestep shift strategy in the motion customization can learn to represent the motion better*

### 失败模式与局限性

尽管 FairyGen 在整体性能上表现优异，但仍存在以下已知局限：

1. **背景运动不协调**：受视频扩散模型不可控生成先验的限制，当前景角色执行跑动等大范围运动时，背景可能保持静止（Fig. 13），导致视觉不协调。这一问题源于图像到视频模型对背景运动的生成缺乏显式约束。

2. **单角色限制**：当前方法针对单角色场景设计，扩展到多角色及其交互场景仍面临挑战。多角色需要多个 3D 代理的协同重建与运动规划，且角色间的遮挡与交互会显著增加风格传播与运动定制的复杂度。

3. **非人形角色的运动生成**：方法依赖 3D 代理重建与骨骼绑定来获取运动先验，对于高度抽象、非人形的手绘角色，骨骼绑定与运动重定向可能存在局限性，需要更先进的绑定技术（如 UniRig）来提升泛化能力。

---

*注：部分定量对比的基线具体数值在现有材料中未明确列出，上述分析基于 Table 1 与 Table 2 的定性比较结论及用户研究数据。如需精确的逐基线数值对比，建议查阅原始论文表格。*

## 定位与知识库关联

### 1. 问题定位与核心瓶颈

FairyGen 锚定于**单样本、高度抽象手绘角色的叙事视频生成**这一前沿交叉问题。该问题横跨三个子领域——风格化定制、主体驱动生成与运动动画，但现有方法各自为战，无法在单儿童画输入的极端条件下协同工作。核心瓶颈在于：

- **风格一致性与角色保真度的冲突**：全局风格化方法（如 **StyleDrop**, Sohn et al., arXiv 2023）在迁移风格时容易侵蚀角色的视觉身份；而主体定制方法（如 **DreamBooth**, Ruiz et al., CVPR 2023）虽能保留角色，却难以将风格扩展至背景。
- **运动自然性与外观一致性的张力**：基于深度或姿态引导的图像到视频方法（如深度引导 **Wan2.1**, Wan et al., 2025；姿态引导 **Animate-X**, Tan et al., 2024）依赖外部结构先验，但对抽象手绘角色的泛化能力有限，且缺乏对运动风格的结构化控制。
- **叙事连贯性缺失**：现有方法缺乏从故事文本到电影化镜头的结构化规划，导致多镜头动画缺乏叙事逻辑与视觉连贯性。

FairyGen 的核心洞察在于：**通过解耦角色建模与风格化背景生成，并引入3D代理重建提供物理合理且可控的运动先验，能够有效分离外观、运动与风格三大要素**，从而在单儿童画输入下生成高质量的故事动画。

### 2. 方法谱系与关键创新

FairyGen 在以下三个维度上对现有方法谱系进行了系统性改进：

#### 2.1 风格化定制：从全局迁移到掩码引导的传播

传统风格化方法可大致分为两类：一类以 **StyleDrop** 为代表，通过全局 LoRA 微调学习风格，但无法区分前景角色与背景；另一类以 **InstantStyle** 为代表，试图通过注意力注入实现风格迁移，但对角色身份的保持能力有限。**B-LoRA** (Frenkel et al., 2025) 通过分离风格与内容块实现了一定程度的解耦，但在抽象手绘风格下仍存在前景-背景混淆。

FairyGen 提出的**风格传播适配器**（Sec. 4.2, Fig. 4）在机制上实现了根本性突破：

- **训练-推理不对称设计**：训练时通过前景掩码 $m$ 仅学习前景区域的风格特征（$y = W x + P A ( x \cdot m )$）；推理时将学习到的风格作用于背景区域（$y = W x + P A ( x \cdot (1 - m) )$），实现精确的风格迁移而不污染角色身份。
- **DoRA 增强的适配器**：采用 DoRA（而非原始 LoRA）作为低秩适配器，消融实验（Fig. 8）证实其在风格化保真度上优于 LoRA。
- **BrushNet 画布补全**：结合预训练修复扩散模型，确保背景生成与前景风格一致。

这一设计使 FairyGen 在风格对齐度量上显著优于所有基线（Table 1，CLIP 距离 0.6580），用户偏好研究（3360次评价）也一致显示其在风格质量上胜出（风格质量得分 0.5365）。

#### 2.2 运动生成：从端到端学习到3D代理驱动的物理先验

运动生成领域的主流范式可分为两类：一是基于 ControlNet 的约束方法（如深度引导 **Wan2.1**、姿态引导 **Animate-X**），二是端到端的外观-运动联合定制方法（如 **DreamVideo**, Wei et al., CVPR 2024）。

FairyGen 的**3D代理重建**（Sec. 4.3）引入了全新的运动先验来源：

- 通过 **DrawingSpinUp** 从单张二维草图重建三维代理，再通过骨骼绑定与运动重定向获得物理可信的运动序列。
- 相比直接使用深度图或姿态骨架，3D代理提供了更丰富的几何与运动学约束，对抽象手绘角色的泛化能力更强。

在运动质量评估中（Table 2），FairyGen 在 VBench 运动平滑度（0.987）和用户运动真实感（0.780）上均优于现有方法。与 **DreamVideo** 的定性比较（Fig. 11）进一步显示，FairyGen 在风格化、运动质量和整体质量上均有显著优势。

#### 2.3 视频定制训练：从单阶段到两阶段解耦与时间步偏置

现有视频定制方法多采用单阶段 LoRA 微调，同时学习外观与运动特征，这导致两个问题：一是外观信息容易被时序模式污染，二是扩散模型的均匀时间步采样不利于运动细节的学习。

FairyGen 的**两阶段运动适配器**（Sec. 4.4, Fig. 5）从根本上解决了这一耦合：

- **Stage 1：身份 LoRA**——在时序打乱的帧上训练，通过 dropout 机制强制学习空间身份特征，避免时序偏差（$y = W x + A_{\mathrm{id}} B_{\mathrm{id}} x$）。
- **Stage 2：运动 LoRA**——冻结身份适配器，在时序连续的帧上学习运动残差（$y = W x + A_{\mathrm{id}} B_{\mathrm{id}} x + A_{\mathrm{id}} B_{\mathrm{motion}} x$）。

消融实验（Fig. 9）证实，两阶段策略显著提升了角色外观一致性，优于单阶段直接训练。

此外，FairyGen 提出的**时间步移采样**（Timestep-Shift Sampling）通过 Logistic 变换（$t = \sigma(z), z \sim N(\mu, \sigma^2)$）将高斯分布映射为晚时步偏置，使扩散模型更关注运动细节的学习。消融实验（Fig. 12）表明，$\mu=6$ 的设置使模型学到更自然、流畅的运动，相比均匀采样优势明显。

### 3. 适用边界与局限性

尽管 FairyGen 在单角色场景下表现优异，其适用边界仍需明确：

- **单角色假设**：当前方法针对单角色设计，扩展到多角色及交互场景仍面临挑战。这需要多个3D代理的协同重建与运动规划，以及更复杂的风格-身份解耦机制。
- **背景运动受限**：受视频扩散模型不可控先验的限制，背景运动可能与前景不协调——例如前景角色跑动时背景可能保持静止（Fig. 13）。这是当前图像到视频生成模型的共性局限。
- **角色形态依赖**：3D代理重建依赖骨骼绑定与运动重定向，对于高度抽象、非人形角色的适用性可能存在局限。更先进的绑定技术（如 UniRig）可能缓解这一问题。

### 4. 开放问题与未来方向

FairyGen 开辟了若干值得深入探索的方向：

- **多角色叙事生成**：如何将方法拓展至多角色及其交互，同时保持风格与运动一致性？这需要在3D代理层面引入多角色空间关系建模，并在风格传播中处理角色间的风格协调。
- **非人形角色的运动生成**：能否通过更先进的骨骼绑定技术（如 UniRig）进一步提升非人形角色的运动生成质量？这涉及计算机图形学与生成模型的交叉。
- **相机运动与背景动态**：如何结合更丰富的相机运动控制，利用不同的图像到视频模型提升背景运动真实感？这将增强叙事视频的电影化表现力。
- **长视频叙事一致性**：随着视频长度增加，如何维持跨镜头的角色外观与运动风格一致性，仍是一个开放挑战。

### 5. 知识库定位总结

FairyGen 在方法谱系中占据了一个独特的交叉位置：它既非纯粹的风格化方法，也非单纯的运动生成方法，而是通过**解耦-重建-定制**的三阶段框架，将风格传播、3D运动先验与视频扩散模型微调有机整合。其核心贡献在于证明了：**在单样本、高度抽象输入的极端条件下，通过结构化的解耦设计与物理先验的引入，可以实现风格一致、运动自然、叙事连贯的视频生成**。这一方法论对未来的少样本视频生成、交互式叙事创作以及儿童教育工具等应用具有重要的参考价值。

## 原文 PDF

![[paperPDFs/arxiv_2025/FairyGen_Storied_Cartoon_Video_from_a_Single_Child_Drawn_Character.pdf]]
