---
title: "Lyra: Generative 3D Scene Reconstruction via Video Diffusion Model Self-Distillation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Lyra_Generative_3D_Scene_Reconstruction_via_Video_Diffusion_Model_Self_Distillation.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/lyra/
aliases:
- Lyra
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "自蒸馏框架：将预训练相机控制视频扩散模型（教师）的RGB解码器输出作为监督信号，训练一个3D高斯溅射（3DGS）解码器（学生），直接在潜空间中生成显式3D表示，从而消除对真实多视图数据的依赖。"
primary_logic: "视频扩散模型在大量互联网视频上训练，已隐式编码了底层3D世界知识；通过精心设计的教师-学生自蒸馏，可将这种隐式知识提炼为显式3DGS，实现从单张图像/视频前馈式生成几何一致的3D/4D场景，且无需真实多视图监督。"
claims:
- "自蒸馏训练数据足够多样且一致，单独使用自蒸馏（PSNR 24.77）优于仅用真实多视图数据（PSNR 19.08），且联合训练不带来提升（PSNR 24.74）。"
- "提出的方案在所有基准（RealEstate10K, DL3DV, Tanks-and-Temples）上全面超越先前方法，例如在RealEstate10K上PSNR达到21.79，优于Bolt3D的21.54。"
- "多轨迹融合是必要的，移除多视图融合模块后PSNR从24.77骤降至17.73，验证了利用多个相机轨迹信息融合的重要性。"
- "RealEstate10K 上 PSNR = 21.79"
---

# Lyra: Generative 3D Scene Reconstruction via Video Diffusion Model Self-Distillation

> [!tip] 核心洞察
> 视频扩散模型在大量互联网视频上训练，已隐式编码了底层3D世界知识；通过精心设计的教师-学生自蒸馏，可将这种隐式知识提炼为显式3DGS，实现从单张图像/视频前馈式生成几何一致的3D/4D场景，且无需真实多视图监督。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Lyra：通过视频扩散模型自蒸馏的生成式3D场景重建 |
| 英文题名 | Lyra: Generative 3D Scene Reconstruction via Video Diffusion Model Self-Distillation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.19296); [Project](https://research.nvidia.com/labs/toronto-ai/lyra); [Project](https://research.nvidia.com/labs/toronto-ai/lyra/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Lyra |
| Dataset | RealEstate10K, DL3DV, Tanks-and-Temples |

> [!tip] 效果简介
> - RealEstate10K 上，PSNR 为 21.79，对比 21.54 (Bolt3D) / 17.15 (Wonderland)，变化 +0.25 / +4.64。
> - DL3DV 上，PSNR 为 20.09，对比 16.64 (Wonderland)，变化 +3.45。
> - Tanks-and-Temples 上，PSNR 为 19.24，对比 15.90 (Wonderland)，变化 +3.34。

## 概述

从单张图像或一段单目视频中重建可交互的3D/4D场景是计算机视觉与图形学的核心难题。现有前馈式3D重建方法依赖稀缺且场景多样性有限的真实多视图数据集进行监督训练，导致泛化能力受限；而大规模预训练的视频扩散模型虽蕴含丰富的2D生成先验，却缺乏显式的3D表示，难以直接用于仿真与交互。

Lyra 提出了一种**自蒸馏框架**来解决这一瓶颈。其核心思路是：将预训练的相机控制视频扩散模型（教师）的RGB解码器输出作为监督信号，训练一个3D高斯溅射（3DGS）解码器（学生），该解码器直接在视频潜空间中从前馈生成的多视图潜变量中预测显式3D高斯场。这一框架的关键洞察在于——视频扩散模型在海量互联网视频上训练后，已隐式编码了底层的3D世界知识；通过精心设计的教师-学生蒸馏，可将这种隐式知识提炼为几何一致的显式3D表示，从而**完全消除对真实多视图数据的依赖**。

实验验证了这一范式的有效性。在RealEstate10K、DL3DV和Tanks-and-Temples三个基准上，Lyra全面超越了先前方法（如Bolt3D、Wonderland），在RealEstate10K上PSNR达到21.79。消融实验进一步揭示了几个关键因果机制：（1）单独使用自蒸馏数据训练（PSNR 24.77）显著优于仅用真实多视图数据（PSNR 19.08），且联合训练几乎无额外收益（PSNR 24.74），证明自蒸馏数据已具备足够的多样性与一致性；（2）移除多视图融合模块后PSNR骤降至17.73，验证了跨轨迹注意力融合的必要性；（3）深度损失与LPIPS损失的移除分别导致PSNR下降至24.31和23.86，表明几何正则与高频细节保持对重建质量至关重要。

该方法也面临若干限制：性能高度依赖教师视频扩散模型的3D一致性质量；训练计算成本较高（8张A100训练6天）；动态场景目前仅支持单目视频输入；评估主要依赖教师模型生成的伪真值，缺乏大规模真实动态场景基准。尽管如此，Lyra开创了以视频扩散模型自蒸馏替代真实多视图监督的新范式，为生成式3D重建开辟了数据高效、泛化性强的技术路径。

## 背景与动机

### 3D场景重建的范式转换与数据瓶颈

从稀疏观测中恢复完整的三维场景一直是计算机视觉的核心目标。传统三维重建方法依赖多视图几何原理，通过特征匹配、运动恢复结构（SfM）和多视图立体匹配（MVS）逐步构建场景表示。这类方法在纹理丰富、光照稳定的场景中表现良好，但在遮挡严重、纹理稀疏或光照变化的区域往往产生不完整的重建结果。

近年来，前馈式3D重建方法取得了显著进展。这类方法通过在大规模真实多视图数据集上训练神经网络，学习从少量图像直接推理三维几何，从而绕过了传统重建中繁琐的逐场景优化过程。然而，**现有的前馈重建范式面临一个根本性的数据瓶颈**：真实世界中高质量、多样化的多视图数据获取成本极高。现有的多视图数据集（如RealEstate10K、DL3DV）虽然在数量上达到数万级别，但其场景多样性、相机轨迹覆盖和标注质量仍远不足以支撑通用场景重建模型的训练。这一瓶颈直接限制了前馈方法的泛化能力——模型在训练分布内表现尚可，但面对分布外场景时性能急剧下降。

### 视频扩散模型的隐式3D知识

与此同时，生成式模型领域经历了革命性突破。视频扩散模型在大规模互联网视频数据上训练后，展现出令人瞩目的多视图生成能力。这些模型能够根据单张图像或文本描述生成时间一致、视角连贯的视频序列，其生成质量暗示模型内部已经**隐式编码了丰富的底层3D世界知识**——包括场景几何、遮挡关系和运动动态。

然而，这种隐式3D知识存在一个关键局限：视频扩散模型的输出本质上是二维像素序列，缺乏显式的三维表示（如点云、网格或高斯场）。这使得生成的视频难以直接应用于需要物理交互的下游任务，如机器人仿真、增强现实或游戏引擎集成。用户无法自由操控视角、与场景中的物体进行碰撞检测，或将生成的场景导入标准三维软件中。

### 现有方案的缺口与本文动机

现有方法尝试弥合这一鸿沟，但各有局限：

- **基于真实多视图数据的前馈重建方法**（如**Bolt3D**, Szymanowicz et al., 2025b）受限于训练数据的多样性和规模，泛化能力不足。
- **逐场景优化的生成式重建方法**（如**ZeroNVS**, Sargent et al., 2024；**ViewCrafter**, Yu et al., 2024b；**Wonderland**, Liang et al., 2025a）虽然利用了扩散模型的先验知识，但需要针对每个场景进行耗时的迭代优化，无法实现实时推理。
- **直接使用视频扩散模型进行新视角合成**的方法（如**BTimer**集成**GEN3C**, Liang et al., 2025b）保持了生成质量，但输出仍为二维视频，不具备显式三维结构。

Lyra的核心动机正是填补这一空白：**如何将视频扩散模型中隐式编码的3D世界知识，高效地提炼为显式的、可实时渲染的3D表示，同时摆脱对稀缺真实多视图数据的依赖？** 这一问题的解决将使得从单张图像或单目视频直接生成可交互的3D/4D场景成为可能，从而打通从生成式模型到物理仿真应用的关键链路。

## 核心创新

Lyra 的核心贡献在于提出了一种**自蒸馏框架**，将预训练视频扩散模型中隐式编码的3D世界知识提炼为显式的3D高斯溅射（3DGS）表示，从而彻底绕过了传统前馈重建方法对稀缺真实多视图数据的依赖。以下从几个关键维度剖析其创新点。

### 1. 教师-学生自蒸馏范式

先前方法（如 **Bolt3D** (Szymanowicz et al., 2025b)）直接使用真实世界多视图数据集训练前馈重建网络，受限于数据集的有限多样性，泛化能力成为瓶颈。Lyra 的核心突破在于构建了一个教师-学生框架：

- **教师模型**：冻结的相机条件视频扩散模型 **GEN3C** (Ren et al., 2025) 及其 RGB 解码器，负责从输入图像/视频生成多视角视频帧。
- **学生模型**：可训练的 3DGS 解码器，直接接收教师模型去噪后的多视图潜变量，前馈输出显式 3D 高斯场。
- **监督机制**：学生渲染的 2D 图像与教师生成的 RGB 帧对齐，形成闭环自蒸馏，无需任何真实多视图标注。

这一范式的因果调节变量在于：**用合成数据的多样性与一致性替代真实数据的稀缺性**。消融实验提供了决定性证据——单独使用自蒸馏数据训练（PSNR 24.77）大幅优于仅用真实多视图数据（PSNR 19.08），且联合训练几乎无增益（PSNR 24.74），证实自蒸馏数据已足够多样且一致（Table 2）。

### 2. 潜空间操作：从像素到压缩表示的跨越

传统前馈重建方法在像素空间处理多视图图像，面临分辨率与 GPU 内存的双重瓶颈。Lyra 的关键架构创新是**直接在视频扩散模型的压缩潜空间中操作**：

- 输入经 VAE 编码为潜变量 $Z \in \mathbb{R}^{L' \times C \times h \times w}$，3DGS 解码器在此空间融合多视图信息，避免了像素空间的扩展代价。
- 这使得模型能够处理高达 726 帧的高分辨率输入，支撑密集的多轨迹监督。

### 3. 3DGS 解码器：从潜变量到显式几何的前馈映射

3DGS 解码器 $D_s$ 的设计实现了从多视图潜变量到显式 3D 表示的直接映射：

- **输入**：多视图视频潜变量 $Z$ 与 Plücker 相机嵌入 $E$。
- **架构**：采用 2×2 patchify 后接 16 层 Transformer-Mamba2 混合块，输出逐像素的 14 维高斯参数。
- **多轨迹融合**：跨轨迹注意力机制融合不同相机轨迹的信息，是模型性能的关键支撑——移除该模块后 PSNR 从 24.77 骤降至 17.73（Table 2）。

### 4. 动态场景的数据增强策略

对于 4D 动态场景重建，Lyra 引入了**动态数据增强**来解决早期时间步的低透明度伪影问题：

- 将输入视频反序后再次送入视频模型，为每个时间步生成额外的 6 条监督轨迹。
- 每个时间步获得 12 路监督（正序 6 路 + 反序 6 路），确保近远视点对的全覆盖，消除极端姿态下的监督盲区。

### 5. 损失函数设计

总损失函数综合了多层次的监督信号：

$$\mathcal{L} = \lambda_{mse} \mathcal{L}_{mse} + \lambda_{lpips} \mathcal{L}_{lpips} + \lambda_{depth} \mathcal{L}_{depth} + \lambda_{opacity} \mathcal{L}_{opacity}$$

其中深度损失（基于 ViPE 估计）对几何正则化至关重要——移除后 PSNR 降至 24.31 并出现平坦几何伪影（Figure 11）；LPIPS 损失维持高频细节（移除后 PSNR 降至 23.86）；不透明度 L1 正则化与修剪则提升了表示的紧凑性与渲染效率（Table 2）。

## 整体框架

Lyra 是一个将视频扩散模型的隐式 3D 知识蒸馏为显式 3D 高斯溅射（3DGS）的前馈式生成重建框架。其核心架构由两个关键分支构成一个教师-学生自蒸馏回路（Figure 2, Figure 4）：**冻结的相机条件视频扩散模型作为教师**，通过其 RGB 解码器输出多视角视频帧作为监督信号；**可训练的 3DGS 解码器作为学生**，直接从扩散模型生成的视频潜变量中前馈式推断出显式 3D 高斯场，并通过可微渲染与教师输出对齐。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2509_19296/figures/003_Figure_4.jpg]]
*Figure 4: 3D Generative Reconstruction Framework. Our pipeline builds upon a camera-controlled video diffusion model (Ren et al., 2025) pre-trained on large scale data. We train a 3D Gaussian Splatting (3DGS) decoder by aligning the 2D image renderings of generated 3DGS scenes with the RGB-decoded generations of the pre-trained video model. We only train the 3DGS decoder while freezing the pre-trained autoencoder and diffusion model. At inference time we directly use the 3DGS decoder, without requiring the RGB decoder anymore. Time conditioning within the 3DGS decoder allows us to easily extend our approach from static to dynamic 3D scene generation*

### 输入与相机轨迹采样

框架接收单张图像或单目视频作为输入，并采样 V=6 条相机轨迹以最大化对场景的视角覆盖（Figure 3）。这些轨迹定义了后续多视角生成的空间范围，为 3D 重建提供足够的多视图约束。

### 教师分支：相机条件视频扩散模型

教师模型基于 **GEN3C**（Ren et al., 2025）——一个在大规模互联网视频上预训练的相机控制视频扩散模型。其工作流程为：首先根据输入图像/视频和相机轨迹构建时空 3D 缓存，通过渲染函数 $\mathcal{R}$ 将点云投影到各目标视角，生成 RGB 图像 $\mathbf{I}^{t,v}$ 和去遮挡掩膜 $\mathbf{M}^{t,v}$；随后，视频 VAE 编码器 $\mathcal{E}$ 将 RGB 视频帧压缩为潜变量 $\mathbf{z} \in \mathbb{R}^{L' \times C \times h \times w}$，扩散模型在此潜空间中进行去噪，生成多视角一致的视频潜变量 $\mathbf{Z}$。教师模型在整个训练过程中保持冻结，仅作为监督信号的提供者。

### 学生分支：3DGS 解码器

3DGS 解码器 $\mathbf{D}_s$ 是框架中唯一可训练的模块。它直接操作在压缩的视频潜空间上，避免了像素空间处理带来的分辨率和 GPU 内存限制，可支持高达 726 帧的高分辨率输入。解码器接收两个输入：教师模型生成的多视图视频潜变量 $\mathbf{Z}$，以及各视角对应的 Plücker 相机射线嵌入 $\mathbf{E}$。通过基于 Transformer-Mamba 混合块的架构（采用 $2 \times 2$ patchify 和 16 层 Transformer-Mamba2 块），解码器将多视图潜变量融合为每像素 14 维的高斯参数，直接输出显式 3D 高斯场 $\mathbf{G}$。

对于动态场景，解码器 $\mathbf{D}_d$ 额外接收源时间步和目标时间步的时间嵌入，以支持时变 3D 高斯场的生成。

### 自蒸馏回路与损失函数

自蒸馏的核心机制在于：学生解码器生成的 3D 高斯场通过 gsplat 渲染器从任意相机姿态渲染出图像和深度图，这些渲染结果与教师 RGB 解码器 $\mathbf{D}_{rgb}$ 输出的对应帧进行对齐。总损失函数为四项损失的加权组合：

$$\mathcal{L} = \lambda_{mse} \mathcal{L}_{mse} + \lambda_{lpips} \mathcal{L}_{lpips} + \lambda_{depth} \mathcal{L}_{depth} + \lambda_{opacity} \mathcal{L}_{opacity}$$

其中，$\mathcal{L}_{mse}$ 和 $\mathcal{L}_{lpips}$ 分别约束渲染图像与教师 RGB 帧的像素级和感知级一致性；$\mathcal{L}_{depth}$ 为尺度不变的深度损失，利用 ViPE 估计的深度图提供几何正则化，防止产生平坦几何伪影；$\mathcal{L}_{opacity}$ 为基于不透明度的 L1 正则化，结合不透明度修剪（移除最低 80% 不透明度的高斯），提升 3D 表示的紧凑性和渲染效率。

### 动态数据增强

针对动态场景训练中早期时间步因极端视角覆盖不足导致的低透明度伪影问题，框架引入了动态数据增强策略（Figure 5）：将输入视频按帧序反转后再次送入视频模型，生成额外的 6 条多视图序列。这使得每个时间步都能获得来自近距和远距视点的成对监督（共 12 路监督），确保全空间覆盖，有效消除了早期时间步的伪影。

### 输出与应用

框架最终输出紧凑的 3D/4D 高斯场表示，可通过 gsplat 从任意视角实时渲染。生成的 3DGS 场景可转换为 .usdz 格式导入 Isaac Sim 5.0 等仿真平台，支持机器人模拟等下游交互任务（Figure 12）。

## 核心模块与公式推导

### 自蒸馏框架：教师-学生双分支架构

Lyra 的核心是一个教师-学生自蒸馏框架（图 2、图 4）。教师分支由预训练的相机控制视频扩散模型 **GEN3C**（Ren et al., 2025）及其 RGB 解码器 `D_rgb` 构成，负责从输入图像/视频生成多视角 RGB 视频帧；学生分支是一个可训练的 3D 高斯溅射（3DGS）解码器 `D_s`（静态）或 `D_d`（动态），直接从视频扩散模型的潜变量中前馈式输出显式 3D 高斯场 `G`。教师模型完全冻结，仅训练学生解码器，形成“教师生成监督信号 → 学生学习 3D 表示”的自蒸馏闭环。

### 视频扩散模型（教师）与潜空间生成

教师模型 GEN3C 接收单张图像或单目视频作为输入，并采样 V=6 条相机轨迹以最大化视角覆盖（图 3）。其内部构建时空 3D 缓存，通过去噪过程生成多视角视频潜变量：

$$ \mathbf{z} = \mathcal{E}(\mathbf{I}) \in \mathbb{R}^{L' \times C \times h \times w} $$

其中 `E` 为 VAE 编码器，`I` 为输入视频帧，`z` 为压缩后的潜变量。GEN3C 在潜空间中进行扩散去噪，输出多视角一致的潜变量序列 `Z`。随后，教师 RGB 解码器 `D_rgb` 将 `Z` 解码为 RGB 视频帧，作为学生分支的监督目标。

### 3DGS 解码器（学生）：潜空间到显式 3D 的映射

学生 3DGS 解码器 `D_s` 直接操作在压缩的视频潜空间，而非像素空间，从而避免像素空间处理带来的分辨率与 GPU 内存瓶颈。其输入包括：

- **多视图潜变量 Z**：来自 GEN3C 生成的多视角视频潜变量；
- **Plücker 嵌入 E**：编码每条光线的相机姿态信息。

解码器首先对输入进行 2×2 patchify 操作，随后通过 16 层 **Transformer-Mamba2 混合块** 进行跨视角融合，最终输出每像素 14 维高斯参数（包括位置、协方差、颜色、不透明度等），构成显式 3D 高斯场 `G`。动态版本 `D_d` 额外接收源/目标时间嵌入，以支持时变场景建模。

### 渲染与损失函数

从生成的 3D 高斯场 `G`，通过可微渲染器（基于 gsplat）根据任意相机姿态渲染 RGB 图像和深度图：

$$ (\mathbf{I}^{t,v}, \mathbf{M}^{t,v}) = \mathcal{R}(\mathbf{P}^{t,v}, \mathbf{C}^{t}) $$

其中 `P^{t,v}` 为时间步 `t`、视角 `v` 的点云，`C^t` 为相机姿态，`I` 和 `M` 分别为渲染图像和去遮挡掩膜。

训练损失函数由四项加权组合构成：

$$ \mathcal{L} = \lambda_{mse} \mathcal{L}_{mse} + \lambda_{lpips} \mathcal{L}_{lpips} + \lambda_{depth} \mathcal{L}_{depth} + \lambda_{opacity} \mathcal{L}_{opacity} $$

各分量含义：
- **`L_mse`**：渲染 RGB 与教师 RGB 之间的均方误差；
- **`L_lpips`**：感知损失（LPIPS），保持高频细节；
- **`L_depth`**：尺度不变深度损失，使用 ViPE 估计的深度作为监督，防止平坦几何伪影；
- **`L_opacity`**：基于不透明度的 L1 正则化，促进高斯紧凑性。训练后移除不透明度最低的 80% 高斯，将渲染速度从 30ms 提升至 18ms。

### 动态数据增强

针对动态场景训练，Lyra 引入动态数据增强策略（图 5）。将输入视频按帧序反转后再次送入视频模型，生成额外的 6 条多视角序列。这样每个时间步获得 12 路监督信号（原始方向 6 路 + 反序方向 6 路），确保早期时间步也能从全空间覆盖获得监督，消除低透明度伪影。

### 保守渲染掩膜

为处理前景遮挡问题，Lyra 采用保守渲染掩膜策略（附录 A）：

$$ \mathbf{M}^{t,v}(u,v) = \begin{cases} 0 & \text{if } \mathbf{D}_{\mathcal{M}}^{t,v}(u,v) < \mathbf{D}^{t,v}(u,v) - \epsilon \\ \mathbf{M}_{\text{orig}}^{t,v}(u,v) & \text{otherwise} \end{cases} $$

通过比较网格插值深度与点云深度，屏蔽前景遮挡区域，防止背景信息泄露到被遮挡区域（图 8）。

## 实验与分析

### 主实验结果

Lyra在三个标准基准上全面超越先前方法。如**Table 1**所示，在RealEstate10K上，Lyra的PSNR达到21.79，优于**Bolt3D**（Szymanowicz et al., 2025b）的21.54和**Wonderland**（Liang et al., 2025a）的17.15；在DL3DV上，PSNR 20.09对16.64，提升3.45 dB；在Tanks-and-Temples上，PSNR 19.24对15.90，提升3.34 dB。SSIM和LPIPS指标同样全面领先。值得注意的是，Lyra无需任何真实多视图数据即可达到此性能——其训练完全依赖视频扩散模型生成的合成数据（Lyra数据集）。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2509_19296/figures/006_Table_1.jpg]]
*Table 1: State-of-the-art comparisons. We compare our method with previous works for single image to 3D generation using RealEstate10K, DL3DV, and Tanks-and-Temples datasets*

与基于逐场景优化的**BTimer**（集成GEN3C，Liang et al., 2025b）的对比见**Table 4**：在静态Lyra数据集上，Lyra以PSNR 24.77显著优于BTimer的20.39；在动态数据集上，Lyra同样以24.30对20.05领先。需注意，由于BTimer运行在像素空间无法处理全部726帧，评估时对GEN3C帧进行了均匀下采样（静态12帧，动态12帧），这可能导致BTimer的性能被低估。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2509_19296/figures/014_Table_4.jpg]]
*Table 4: Quantitative results on static and dynamic Lyra datasets*

**Figure 6**展示了从单张图像生成的3DGS场景在五个新视角下的渲染效果，验证了前馈式生成的高视觉质量与几何一致性。

### 消融实验

**Table 2**在Lyra数据集上进行了系统消融，揭示了各组件的关键贡献：

**自蒸馏数据的必要性与充分性。** 仅用真实多视图数据训练（无自蒸馏）导致PSNR从24.77骤降至19.08，降幅达5.69 dB，证明真实数据集的多样性远不足以支撑泛化能力强的重建模型。而在自蒸馏基础上添加真实数据联合训练几乎无收益（PSNR 24.77 vs 24.74），表明自蒸馏数据已足够多样且一致。

**多视图融合的关键作用。** 移除多视图融合模块后PSNR降至17.73（降幅7.04 dB），这是所有消融中降幅最大的项，验证了跨轨迹注意力融合对于整合不同相机轨迹信息至关重要。

**损失函数各组分贡献。** 移除LPIPS损失使PSNR降至23.86，高频细节保持能力下降；移除深度损失降至24.31，且**Figure 11**显示出现平坦几何伪影，证明基于ViPE估计的尺度不变深度监督对几何正则化不可或缺；不进行不透明度修剪使PSNR略降至24.55，但渲染速度从18ms增至30ms，表明基于L1正则化的修剪策略在提升紧凑性的同时改善了视觉质量。

### 失败模式与局限性

1. **教师模型依赖。** Lyra的性能高度依赖教师视频扩散模型（GEN3C）的生成质量与3D一致性。若教师模型在遮挡区域或极端视角下产生不一致内容，3DGS解码器会继承这些瑕疵，表现为漂浮高斯或几何扭曲。

2. **动态场景的早期时间步伪影。** 在未使用动态数据增强时，早期时间步的极端视角区域出现低透明度伪影（见**Figure 5**）。本文通过反向视频生成额外多视图序列（12路监督）缓解此问题，但该增强策略增加了训练复杂度。

3. **训练计算成本。** 完整训练需8张A100运行6天，采用渐进式训练策略（**Table 3**），这限制了快速实验迭代。

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2509_19296/figures/011_Table_3.jpg]]
*Table 3: Progressive training setup*

4. **评估基准局限。** 由于基线方法未公开源代码，无法在自行构建的分布外评估集上测试它们，主要依赖论文报道的定量结果进行比较。此外，Lyra数据集本身由教师模型生成，缺乏大规模真实动态场景的独立基准。

5. **物理交互的中间转换。** 生成的3D高斯场需通过`.ply`到`.usdz`格式转换才能导入仿真平台（如Isaac Sim 5.0，见**Figure 12**），当前仅在仿真环境中进行了初步验证，尚未在真实机器人平台上测试闭环交互。

### 补充图表

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2509_19296/figures/001_Figure_1.jpg]]
*Figure 1: Feed-Forward 3D and 4D Scene Generation. From a single image (top), Lyra infers a 3D Gaussian Splatting (3DGS) representation in a feed-forward fashion, through self-distilling a video diffusion model without requiring real-world multi-view data. With a video input (bottom), Lyra infers a dynamic 3DGS that offers interactive control in both time (rows) and viewpoint (columns)*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2509_19296/figures/012_Figure_9.jpg]]
*Figure 9: Dynamic data augmentation videos. We augment the supervision data with a motionreversed video, ensuring that each timestep is observed from the full spatial coverage, thereby preventing low opacity artifacts in the early timesteps. We show two example trajectories, i.e., zoom-out and zoom-in, and visualize their corresponding augmented videos. The augmented videos are flipped in their camera motion*

![[assets/figures/papers/paper_list_l40_https_arxiv_org_abs_2509_19296/figures/009_Table_2.jpg]]
*Table 2: Ablation study on Lyra dataset*

## 方法谱系与知识库定位

### 1. 问题定位：从数据稀缺到先验迁移

前馈式3D重建方法长期受制于一个核心瓶颈：**多样化真实多视图数据的稀缺性**。传统方法（如GS-LRM系列）依赖RealEstate10K、DL3DV等真实世界多视图数据集进行监督训练，但这些数据集的场景多样性和视角覆盖范围有限，导致模型在分布外场景上的泛化能力不足。Lyra的突破性洞察在于：**视频扩散模型在大规模互联网视频上预训练时，已隐式编码了丰富的底层3D世界知识**——这些知识体现为对几何一致性、遮挡关系和视角变换的隐式理解。问题由此转化为：如何将这种隐式2D先验“蒸馏”为显式3D表示，从而完全绕过真实多视图数据的依赖。

### 2. 方法谱系：自蒸馏框架的定位

Lyra在方法谱系中占据一个独特位置，其核心创新可概括为**教师-学生自蒸馏范式**在3D重建中的首次系统性应用。与相关工作对比：

**与多视图重建方法的区别**：先前的前馈重建方法（如**Bolt3D** (Szymanowicz et al., 2025b)）直接在真实多视图图像上训练重建网络，受限于数据多样性和覆盖范围。Lyra将监督信号从“真实多视图”替换为“视频扩散模型生成的合成多视图”，消除了对真实多视图数据的依赖。Table 2的消融实验提供了决定性证据：仅用真实多视图数据训练时PSNR仅19.08，而纯自蒸馏训练达到24.77，验证了合成数据的多样性和一致性已超越真实数据集的训练价值。

**与单图像到3D生成方法的区别**：**ZeroNVS** (Sargent et al., 2024)、**ViewCrafter** (Yu et al., 2024b)、**Wonderland** (Liang et al., 2025a)等方法通常采用逐场景优化或两阶段生成策略，缺乏前馈式效率。Lyra实现了从单张图像到显式3DGS的直接前馈映射，在RealEstate10K上PSNR达到21.79，显著优于Wonderland的17.15。

**与视频扩散模型直接应用的区别**：**BTimer** (Liang et al., 2025b)集成了GEN3C视频扩散模型，但运行在像素空间，受限于GPU内存无法处理高分辨率多帧输入。Lyra的关键架构决策是**直接在视频潜空间中操作**，使得单次前馈可处理726帧高分辨率输入，避免了像素空间的缩放瓶颈。

### 3. 技术贡献的因果机制

Lyra的效能提升可归因于三个相互关联的技术决策：

**潜空间操作**：通过VAE压缩将视频帧映射到低维潜空间，使得3DGS解码器能够高效融合多视图信息。这一设计使模型能够处理V=6条相机轨迹、每条121帧的完整多视图序列，为多轨迹融合提供了信息基础。

**多轨迹融合的必要性**：Table 2的消融实验表明，移除多视图融合模块后PSNR从24.77骤降至17.73，降幅超过7 dB。这验证了跨轨迹注意力机制在整合不同视角信息中的关键作用——单一轨迹的信息不足以恢复完整的3D几何。

**深度监督的几何正则化**：移除深度损失后PSNR降至24.31，且出现平坦几何伪影（Figure 11）。深度监督（通过ViPE估计的伪深度）为3DGS解码器提供了显式的几何约束，防止其退化为仅依赖外观匹配的“纸片模型”。

### 4. 适用边界与局限

**教师模型依赖瓶颈**：Lyra的性能高度耦合于GEN3C视频扩散模型的质量。若教师模型在特定场景（如高度非朗伯表面、复杂光照变化）上生成不一致的多视图内容，3D重建将继承这些瑕疵。这一依赖关系意味着Lyra的上限由视频扩散模型的3D一致性决定。

**训练计算成本**：渐进式训练策略（Table 3）需要8张A100 GPU训练6天，包括从256分辨率到512分辨率的逐步提升、从短序列到长序列的扩展。这种复杂的训练流程限制了快速迭代和社区复现的可行性。

**动态场景的局限性**：动态场景生成目前仅扩展至单目视频输入，依赖动态数据增强（反向视频生成额外监督）来缓解早期时间步的低透明度伪影。这一策略虽然有效（Figure 5, Figure 9），但本质上是对单视频轨迹的增强，尚未探索多摄像机动态输入或复杂运动建模。

**评估基准的偏差**：主要评估依赖Lyra数据集（由GEN3C生成的伪真值），缺乏大规模真实动态场景的独立基准。Table 1的RealEstate10K等真实数据集评估仅覆盖静态场景，动态场景的定量比较（Table 4）仍以教师模型输出为参考，存在循环验证的风险。

**物理交互的间接性**：生成的3D高斯场需要转换为`.usdz`格式才能导入Isaac Sim 5.0进行机器人仿真（Figure 12），且高斯表示本身不直接支持碰撞检测和物理约束。这一转换步骤引入了表示精度的损失，且当前仅在仿真平台进行了初步验证。

### 5. 开放问题与未来方向

**视频扩散模型的进一步扩展**：当前自蒸馏框架的性能上限受限于GEN3C的3D一致性。如何训练更大规模、更几何感知的视频扩散模型，以支持更复杂场景（如大规模室外环境、密集遮挡场景）的一致合成，是提升重建质量的根本路径。

**自回归场景生成**：Lyra目前生成固定范围的3D场景。将自回归生成机制引入框架，允许逐步扩展场景边界（如沿相机轨迹增量生成新的高斯区域），将使得大范围场景的连续重建成为可能。

**运动与跟踪的显式建模**：动态场景的视觉运动质量仍有提升空间。在3DGS解码器内部显式建模运动场或跟踪信息（而非仅依赖时间嵌入），可能改善动态场景的时间一致性和运动自然度。

**闭环物理仿真**：将生成的3D高斯场直接集成到实时物理引擎中，需要解决高斯表示的碰撞检测效率问题。探索更紧凑的高斯剪枝策略或混合表示（高斯+网格），可能使Lyra的输出直接适用于机器人操作的闭环仿真。

**自蒸馏范式的泛化**：自蒸馏框架的核心思想——用生成模型监督重建模型——是否可推广至其他生成模型架构？例如，用3D原生扩散模型替代视频扩散模型作为教师，可能进一步消除2D-3D领域差异，提升重建精度。

## 原文 PDF

![[paperPDFs/ICLR_2026/Lyra_Generative_3D_Scene_Reconstruction_via_Video_Diffusion_Model_Self_Distillation.pdf]]
