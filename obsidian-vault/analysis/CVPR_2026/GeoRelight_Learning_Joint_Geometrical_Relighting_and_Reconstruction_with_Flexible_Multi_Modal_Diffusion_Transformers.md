---
title: "GeoRelight: Learning Joint Geometrical Relighting and Reconstruction with Flexible Multi-Modal Diffusion Transformers"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GeoRelight_Learning_Joint_Geometrical_Relighting_and_Reconstruction_with_Flexible_Multi_Modal_Diffusion_Transformers.pdf
project_link: "https://yuxuan-xue.com/georelight"
code_link: null
aliases:
- GeoRelight
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过统一的Multi-Modal DiT同时去噪重光照图像、内蕴属性（反射率、法线）和3D几何（iNOD表示），实现几何感知的联合生成，并利用混合训练数据弥合合成-真实域差距。
primary_logic: 重光照与几何重建是互促的任务：精确几何提供遮挡和局部着色线索，而外观中的明暗信息则通过shape-from-shading增强几何细节。通过在潜空间中联合多模态扩散以及设计VAE友好的等距深度表示iNOD，模型可以同时从合成和真实数据中学习物理约束和真实感。
claims:
- 联合建模（Joint Modeling）在重光照PSNR上比w/o Geometry基线高6.3 dB（27.49 vs 21.19），并产生更丰富的几何依赖细节（如阴影和褶皱）。
- 提供重光照图像作为条件可将法线角度误差从12.24降至9.10，验证了shape-from-shading的协同效应。
- 在HumanOLAT和Light Stage真实数据上，GeoRelight的重光照PSNR大幅超越IC-Light、NeuralGaffer等基线（例如合成数据上27.22 vs DiffusionRenderer 19.28）。
- 在几何重建上，GeoRelight的Chamfer Distance为0.766，远低于VGGT的3.37和MoGe2的3.54。
---

# GeoRelight: Learning Joint Geometrical Relighting and Reconstruction with Flexible Multi-Modal Diffusion Transformers

> [!tip] 核心洞察
> 重光照与几何重建是互促的任务：精确几何提供遮挡和局部着色线索，而外观中的明暗信息则通过shape-from-shading增强几何细节。通过在潜空间中联合多模态扩散以及设计VAE友好的等距深度表示iNOD，模型可以同时从合成和真实数据中学习物理约束和真实感。

| 字段 | 内容 |
|------|------|
| 中文题名 | GeoRelight：基于灵活多模态扩散变换器的几何重光照与重建联合学习 |
| 英文题名 | GeoRelight: Learning Joint Geometrical Relighting and Reconstruction with Flexible Multi-Modal Diffusion Transformers |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.20715) · [Project](https://yuxuan-xue.com/georelight) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | GeoRelight |
| Dataset | 合成数据（Synthetic）, Light Stage数据, HumanOLAT |

> [!tip] 效果简介
> - 合成数据（Synthetic） 上，PSNR (Relighting) ↑ 27.22 vs 19.28 (DiffusionRenderer) (+7.94)。
> - Light Stage数据 上，PSNR (Relighting) ↑ 25.87 vs 21.09 (DiffusionRenderer) (+4.78)。
> - HumanOLAT 上，PSNR (Relighting) ↑ 21.17 vs 20.77 (NeuralGaffer) (+0.40)。

## 概要

单目图像的人物重光照与三维重建是视觉计算中的一对核心任务，但传统方法通常将二者解耦处理：先估计几何或内蕴属性，再执行重光照，导致误差累积，且缺乏显式几何约束，难以生成物理上逼真的阴影与高光。**GeoRelight** 将这一问题重新定义为联合的条件多模态生成任务，核心洞察在于——重光照与几何重建是互促的：精确几何为遮挡和局部着色提供线索，而外观中的明暗信息则通过 shape-from-shading 增强几何细节。

为实现这一联合建模，GeoRelight 构建了一个统一的 **Multi-Modal Diffusion Transformer (DiT)**，在潜空间中同时去噪重光照图像、内蕴属性（反射率、法线）以及三维几何。其关键设计包括：将视频扩散模型的时间维度重新用作模态维度，并通过可学习的模态类型嵌入与开关掩码实现灵活的条件机制；提出 **iNOD（等距归一化正射深度）** 表示，以 VAE 友好且无失真的方式编码三维形状；采用战略性混合训练策略，融合合成数据、光照舞台数据与自动标注的自然图像数据，弥合合成-真实域差距。

实验表明，联合建模在重光照 PSNR 上相比无几何基线提升 **6.3 dB**（27.49 vs 21.19），并产生更丰富的几何依赖细节；同时，提供重光照图像作为条件可将法线角度误差从 12.24 降至 **9.10**，验证了 shape-from-shading 的协同效应。在 HumanOLAT 和 Light Stage 真实数据上，GeoRelight 的重光照 PSNR 大幅超越 **IC-Light**（Zhang et al., ICLR 2025）、**NeuralGaffer**（Jin et al., NeurIPS 2024）等基线；在三维重建上，其 Chamfer Distance 为 **0.766**，远低于 **VGGT**（Wang et al., CVPR 2025）的 3.37 和 **MoGe2**（Wang et al., 2025）的 3.54。用户研究中，93.8% 的参与者偏好 GeoRelight 的重光照结果，93.4% 偏好其三维重建，体现了显著的主观质量优势。

**方法定位**：GeoRelight 属于基于扩散模型的几何感知重光照方法，区别于仅输出重光照图像的端到端像素映射方法（如 IC-Light、NeuralGaffer）和依赖辐射提示的 ControlNet 方法（如 **DiLightNet**, Zeng et al., SIGGRAPH 2024）。其核心创新在于将重光照、内蕴分解与三维重建统一于单一扩散框架，并以 iNOD 表示和混合数据策略支撑多任务联合学习。



### 问题背景

图像重光照旨在将单张图像中的人物置于全新的光照环境下，生成逼真的外观。这一任务在电影制作、增强现实和虚拟试穿等应用中具有重要价值。然而，真实感重光照不仅需要改变全局色调，还要求精确再现与三维几何紧密耦合的局部光照效应——包括阴影投射、褶皱高光和遮挡关系。这些效应本质上由物体的三维形状决定，因此高质量的几何重建与重光照是相互依存的任务。

### 现有方法缺口

当前的重光照方法普遍存在一个核心瓶颈：将几何估计与重光照分离为顺序管道。这种分离导致两个层面的问题。一方面，**误差累积**——几何估计阶段的误差会直接传播到后续的重光照步骤，且后续步骤缺乏修正几何的机制。另一方面，**几何信息利用不足**——端到端的像素映射方法虽然避免了显式的几何重建，但无法有效利用三维形状线索来生成物理上逼真的阴影和高光，导致结果缺乏几何依赖的细节。

从具体基线来看：

- **IC-Light**（Zhang et al., ICLR 2025）基于扩散模型进行光照协调，但未显式建模三维几何。
- **NeuralGaffer**（Jin et al., NeurIPS 2024）采用端到端扩散重光照，同样缺乏对几何结构的显式约束。
- **DiLightNet**（Zeng et al., SIGGRAPH 2024）利用辐射提示的ControlNet进行重光照，但未同时输出三维形状。
- **DiffusionRenderer**（Liang et al., CVPR 2025）使用视频扩散模型进行内蕴/正向渲染，虽涉及内蕴属性分解，但未将几何重建作为联合任务。

在几何重建方面，专业单任务方法如 **VGGT**（Wang et al., CVPR 2025）和 **MoGe2**（Wang et al., 2025）虽在各自领域表现优异，但缺乏与外观生成的协同。

### 核心动机

GeoRelight的出发点是打破上述分离范式，其核心洞察为：**重光照与几何重建是互促的任务**。精确的几何提供遮挡边界和局部表面朝向，为光照传输计算提供物理约束；而外观中的明暗变化则通过shape-from-shading机制为几何细节提供反向监督。通过在统一框架中联合建模两者，模型可以从多模态信号中提取互补信息，同时从合成数据和真实数据中学习物理约束与真实感。

此外，现有方法在训练数据策略上也存在局限：纯合成数据虽提供完美标签，但缺乏真实感；而真实光照舞台数据虽保真度高，却存在照明偏压（如LED阵列导致的暗偏压）。GeoRelight通过战略性混合训练数据弥合这一合成-真实域差距，使得模型在保持物理精度的同时生成自然均衡的光照效果。



## 核心方法与创新机理

GeoRelight 的核心创新在于将传统的“先估计几何，再进行重光照”的顺序管道重构为一个**统一的联合生成框架**，从根本上解决了误差累积与几何-外观割裂的瓶颈。其关键创新点体现在以下四个维度：

### 1. 几何与重光照的联合多模态扩散

传统方法将几何估计与重光照视为独立任务，导致几何误差直接传递至光照渲染阶段，且重光照模型缺乏显式的3D遮挡与局部着色约束。GeoRelight 将问题重新定义为**条件多模态生成任务**：给定单张人物图像和目标环境光照，模型同时去噪生成重光照图像、内蕴属性（反射率、法线、分割掩码）以及3D几何。

这一设计利用了重光照与几何之间的**双向协同效应**：精确的几何提供遮挡边界和局部表面朝向，使重光照能产生物理上可信的阴影与褶皱；而外观中的明暗变化则通过 shape-from-shading 机制反向增强几何细节。消融实验验证了这一协同作用：联合建模在重光照 PSNR 上比“无几何模式”（w/o Geometry）高出 **6.3 dB**（27.49 vs 21.19），并生成了几何依赖的细节（如阴影、衣物褶皱）；反之，提供真实重光照图像作为条件可将法线角度误差从 12.24 降至 **9.10**（Table 2, Figure 5）。

### 2. 视频 DiT 的时间轴重定义为模态轴

GeoRelight 构建于**视频潜空间扩散变换器（Video Latent DiT）**之上，但其核心改造在于将视频模型的时间维度 $T$ **重新定义为模态维度** $M$。具体而言，不同目标模态（重光照图像、反射率、法线等）沿“模态轴”拼接，共享同一去噪骨干网络。这一设计使得模型能够利用 DiT 强大的跨帧注意力机制来实现跨模态信息交互，而无需为每个模态设计独立的编码器-解码器或专门的融合模块。

为区分不同模态，框架引入了两个关键机制：
- **可学习的模态类型嵌入** $\mathbf{c}_{\mathrm{modal}} \in \mathbb{R}^{M \times C_{\mathrm{type}}}$：为每个模态位置分配唯一的嵌入向量，使 DiT 感知当前处理的是何种模态。
- **模态开关掩码** $\mathbf{c}_{\mathrm{switch}} \in \mathbb{R}^{H \times W \times 1}$：二值掩码指示每个模态是条件（1）还是待生成目标（0），赋予框架极大的灵活性——同一架构可支持不同的输入-输出组合，支撑了后续混合数据训练中的多模式切换（Table 1）。

### 3. iNOD：面向VAE的无失真3D几何表示

将3D几何纳入潜空间扩散模型面临一个关键挑战：标准几何表示（点图、归一化深度图）在VAE编码-解码过程中会引入严重失真或噪声。点图经VAE压缩后变得嘈杂，而各向异性归一化深度图则严重扭曲3D形状（Figure 2）。

GeoRelight 提出了**等距归一化正射深度图（iNOD, isotropic Normalized Orthographic Depth）**，一种简单而有效的表示方法：
1. **等距3D归一化**：将整个3D几何体基于最长边缩放至 $[-1, 1]$ 的边界框内，保持各向同性，避免形状畸变。
2. **正射投影**：将归一化后的几何体沿 Z 轴正射投影至 XY 平面，取每个点的 Z 值作为深度。

iNOD 的核心优势在于：作为密集的2D图像表示，天然兼容VAE的卷积结构；等距归一化确保了3D相对几何的忠实保留；正射投影避免了透视投影带来的远距离压缩。实验表明，iNOD 在 VAE 压缩后能更忠实地保留几何边界（Figure 2），为联合生成中的几何感知提供了可靠的基础表示。

### 4. 战略性混合数据训练弥合合成-真实域差距

纯合成数据虽提供完美标签，但缺乏真实感；光照舞台数据具有真实外观，但光照条件受限且存在暗偏压。GeoRelight 采用**三源混合数据策略**（Figure 4）：
- **合成数据**：提供全标注标签（几何、内蕴属性、多光照配对），用于预训练基础物理约束。
- **光照舞台数据**：提供真实人物外观与配对光照，增强真实感。
- **In-the-Wild 数据**：大规模自然图像，通过合成数据预训练模型自动标注内蕴属性，用于纠正光照舞台数据特有的亮度偏压（Figure 9）。

训练采用两阶段策略：先在合成数据上训练 30K 步以建立物理先验，再进行 10K 步混合数据训练以弥合域差距。模态开关掩码使得模型可在不同数据源上灵活切换训练模式（如对 In-the-Wild 数据仅监督重光照和几何，不监督反射率），实现了多源数据的有效联合利用（Table 1）。



GeoRelight 将单目人像的重光照与几何重建统一建模为一个**条件多模态生成任务**，其核心架构建立在视频潜扩散变换器（Video Latent Diffusion Transformer, DiT）之上。模型接收一幅在未知光照下拍摄的输入图像 $\tilde{\mathbf{I}}$ 和目标环境光照 $\mathbf{E}$，同时生成重光照图像 $\mathbf{I}$、内蕴反射率 $\mathbf{a}$、法线图 $\mathbf{n}$、语义分割掩码 $\mathbf{s}$ 以及 3D 几何表示——等距归一化正射深度图（iNOD）。框架的关键设计是将视频扩散模型中的时间维度重新赋予语义，改造为模态维度 $M$，使同一 DiT 骨干能够并行处理多种异质输出。

### 条件机制与多模态流

输入图像并非作为待去噪的目标模态，而是作为**全局条件**拼接到所有目标模态的潜变量序列中。具体而言，模型为每个模态槽位引入两类控制信号：

- **模态类型嵌入** $\mathbf{c}_{\mathrm{modal}} \in \mathbb{R}^{M \times C_{\mathrm{type}}}$：可学习的嵌入向量，用于区分当前槽位承载的是重光照图像、反射率、法线、分割还是 iNOD 深度图。
- **模态开关掩码** $\mathbf{c}_{\mathrm{switch}} \in \mathbb{R}^{H \times W \times 1}$：二值掩码，标记该槽位是作为条件（值为 1）还是待生成的去噪目标（值为 0）。这一机制使得同一框架可以灵活切换训练模式——例如在合成数据上同时生成所有模态，而在真实数据上仅以重光照为目标、其余模态作为伪标签条件。

环境光照 $\mathbf{E}$ 通过专用的**光照条件模块**注入：HDR 环境图首先被分解为 LDR 兼容的表示，再编码为光照潜变量 $\mathbf{z}^{\mathbf{E}}$，与图像条件 $\mathbf{z}^{\tilde{\mathbf{I}}}$ 共同引导去噪过程。所有模态共享 2D 旋转位置编码（RoPE），确保空间一致性的跨模态注意力。

### iNOD：VAE 友好的几何表示

传统几何表示在潜扩散框架中存在根本性缺陷：点图经 VAE 编码后产生噪声伪影，而各向异性归一化深度图则严重扭曲 3D 形状。GeoRelight 提出 **iNOD（等距归一化正射深度图）** 来解决这一问题：

1. **等距 3D 归一化**：将整个 3D 几何体沿其最长边缩放至 $[-1, 1]$ 的包围盒，保持各向同性。
2. **正射投影**：沿 Z 轴正射投影至 XY 平面，直接取每个点的 z 值作为深度。
3. **逆投影恢复**：从潜变量解码 iNOD 后，通过逆正射投影重建完整的 3D 点云。

iNOD 既是稠密的 2D 图像表示（天然适配 VAE 压缩），又完美保留了相对 3D 几何结构，无失真地传递遮挡边界和局部曲率信息。

### 混合数据训练策略

GeoRelight 采用两阶段训练，以弥合合成数据与真实场景之间的域差距：

- **第一阶段**：在纯合成数据上训练 30K 步，利用合成数据提供的完备真值标签（重光照图像、反射率、法线、深度、分割）建立初始的物理约束。
- **第二阶段**：混合合成数据、Light Stage 真实数据和自动标注的 In-the-Wild 数据，继续训练 10K 步。其中，Light Stage 数据提供配对的真实光照变化，In-the-Wild 数据则通过第一阶段模型自动标注内蕴属性后参与训练。每个训练批次包含 128 个样本，分辨率为 $832 \times 1280$ 像素。

模态开关掩码在此发挥关键作用：对于缺乏完整真值的真实数据，模型仅将可用模态设为条件（掩码为 1），而将重光照图像作为唯一的去噪目标（掩码为 0），从而在统一的架构下灵活利用多源异构数据。

### 补充图表

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/003_Figure_3.jpg]]
*Figure 3: The GeoRelight Pipeline. GeoRelight processes up to five target modalities, using cswitch to signal which ones are targets and conditions (the figure shows one specific usecase). It is guided by a global image condition*



### 3.1 多模态扩散Transformer框架

GeoRelight将联合重光照与几何重建问题形式化为一个**条件多模态生成任务**：给定单张人物图像，同时生成新光照下的重光照图像、内蕴反射率（albedo）、法线图、分割掩码以及3D几何。该框架构建于视频潜在扩散Transformer（Video Latent DiT）之上，其核心设计是将视频模型的时间维度T重新定义为**模态维度M**，使得单个DiT能够并行处理并去噪多达五种目标模态。

**条件机制**：输入图像并非作为待去噪的目标模态，而是作为全局条件拼接到所有目标模态的潜变量序列中。具体而言，输入图像经VAE编码后得到潜变量 $\mathbf{z}^{\tilde{\mathbf{I}}}$，与目标模态的噪声潜变量沿模态维度串联，共同送入DiT进行去噪。为区分不同模态，框架引入两个关键组件：

- **模态类型嵌入**（modality type embedding）：一个可学习的嵌入矩阵 $\mathbf{c}_{\mathrm{modal}} \in \mathbb{R}^{M \times C_{\mathrm{type}}}$，为每个模态位置注入类型标识，使模型感知当前处理的是重光照图像、法线还是深度等。
- **模态开关掩码**（modality switch mask）：二值掩码 $\mathbf{c}_{\mathrm{switch}} \in \mathbb{R}^{H \times W \times 1}$，指示每个模态是作为条件（值为1）还是待生成目标（值为0）。这一设计使得同一框架可灵活切换训练模式——例如，当仅有真实重光照图像作为监督时，可将其他模态标记为条件，仅对重光照模态执行去噪损失。

所有模态共享2D旋转位置编码（RoPE）进行空间注意力，确保跨模态的空间对齐。

### 3.2 环境光照条件模块

为实现对新光照条件的精确控制，GeoRelight设计了专门的环境光照条件模块。HDR环境图首先被分解为LDR兼容的表示形式（包括漫反射和镜面反射分量），随后经专用编码器映射为光照潜变量 $\mathbf{z}^{\mathbf{E}}$。该光照潜变量通过交叉注意力机制注入DiT的各层，引导生成过程朝向目标光照分布。

### 3.3 iNOD：等距归一化正射深度表示

3D几何的潜在空间编码是联合建模的关键瓶颈。标准点图（Point Map）经VAE压缩后产生噪声伪影，而各向异性归一化深度（Anisotropic Normalized Depth）则严重扭曲3D形状。为此，GeoRelight提出**等距归一化正射深度**（isotropic NDC-Orthographic Depth，iNOD）：

1. **等距归一化**：将整个3D几何体沿最长边等比例缩放至 $[-1, 1]$ 的包围盒内，确保三个轴向的缩放因子一致，避免形状畸变。
2. **正射投影**：将归一化后的几何体沿Z轴正射投影到XY平面，直接取每个像素对应点的Z值作为深度，形成密集的2D深度图。

iNOD的核心优势在于：等距缩放保留了相对3D几何关系，正射投影产生的深度图具有平滑的梯度分布，天然适配VAE的卷积编码-解码过程。解码后，通过逆正射投影即可恢复完整的3D点云。

### 3.4 战略性混合数据训练

为弥合合成数据与真实数据的域差距，GeoRelight采用三阶段混合训练策略（见Table 1）：首先在**合成数据**上预训练30K步，利用其完美的全模态标注学习物理约束；随后引入**光照舞台数据**（Light Stage）和自动标注的**自然场景数据**（In-the-Wild），通过模态开关掩码灵活选择各数据源可用的监督信号——例如，自然场景数据仅有输入图像而无配对光照，则仅对重光照模态施加损失。这种设计使模型同时从合成数据的物理精确性和真实数据的视觉真实感中获益。

### 补充图表

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/002_Figure_2.jpg]]
*Figure 2: iNOD: A Distortion-Free and VAE-Friendly Geometry Representation. Standard Point Maps (top-left) become noisy when VAE-encoded, and anisotropically Normalized Depth (topright) severely distorts the 3D shape*

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/004_Figure_4.jpg]]
*Figure 4: Our Strategic Mixed-Data Training Sources. We combine (a) fully-labeled Synthetic data, (b) Light Stage data with paired lighting, and (c) In-the-wild data. We use our synthetic data pre-trained model to auto-label intrinsics for (b) and (c)*

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/016_Figure_11.jpg]]
*Figure 11: Processed Environment Illumination from Light-Stage. From the 3-dimensional LED positions, we project it to a latlong image to model the environement map*

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/018_Figure_13.jpg]]
*Figure 13: Limitation of Point Map in Latent Space. As a popular geometry representation [33, 36] in image sapce, point map shows strong limitation in latent space. Although visually the point map looks similar before and after VAE, the boundary lost huge precision (please zoom in) and it contains much noise after VAE*



## 实验与关键发现

### 核心实验设置

GeoRelight的训练分为两个阶段：首先在纯合成数据上训练30K步，然后采用战略性混合数据训练（见Table 1）再训练10K步。每个训练批次包含128个样本，分辨率为832×1280像素。模型以**DiffusionRenderer**（Liang et al., CVPR 2025）的预训练权重进行初始化。

### 重光照性能：主结果

GeoRelight在多个基准上取得了最优的重光照性能，定量结果汇总于Table 3。在合成数据上，GeoRelight的PSNR达到**27.22 dB**，相比最强基线DiffusionRenderer（19.28 dB）提升**+7.94 dB**。在Light Stage真实数据上，模型同样以25.87 dB的PSNR显著超越DiffusionRenderer的21.09 dB（+4.78 dB）。在HumanOLAT数据集上，GeoRelight以21.17 dB略优于**NeuralGaffer**（Jin et al., NeurIPS 2024）的20.77 dB。

定性比较（Figure 6）进一步验证了上述结论。GeoRelight生成的重光照结果在物理合理性上明显优于**IC-Light**（Zhang et al., ICLR 2025）、**DiLightNet**（Zeng et al., SIGGRAPH 2024）和NeuralGaffer等基线方法，尤其在阴影投射和高光反射等几何依赖效应上表现突出。在用户研究中，93.8%的参与者在双选一被迫选择（2AFC）中偏好GeoRelight的重光照结果，体现了其主观质量优势。

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison on relighting. Our model (right) produces more physically-plausible results compared to baselines on both the HumanOLAT dataset [32] and challenging in-the-wild images. Please refer to our supplementary for more results1*

### 几何重建性能

GeoRelight在几何重建上同样超越了专用的单任务最先进方法。如Table 4所示，在合成数据上，GeoRelight的Chamfer Distance仅为**0.766**，远低于**VGGT**（Wang et al., CVPR 2025）的3.37和**MoGe2**（Wang et al., 2025）的3.54。定性结果（Figure 8）显示，联合建模使GeoRelight能够重建出细粒度的3D形状，而单任务基线则产生相对粗糙的几何。在三选一强制选择的用户研究中，93.4%的参与者偏好GeoRelight的3D重建结果。

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/011_Figure_8.jpg]]
*Figure 8: Qualitative comparison on geometry reconstruction. Our joint model (right) reconstructs fine-grained 3D shapes. In contrast, specialized geometry estimators like VGGT [33] and MoGe2 [35] produce distorted or over-smoothed point clouds on these in-the-wild images, demonstrating the superior performance of high-frequency details modeling of our iNOD with latent generative models*

### 内蕴属性解耦

GeoRelight同时输出反射率（albedo）和法线（normal）等内蕴属性。如Table 5所示，模型在反射率PSNR上达到28.07 dB，法线角度误差为8.64°，均达到最优水平。法线估计的定性比较（Figure 7）表明，GeoRelight在眼睛、皮肤和头发等区域能捕获更清晰的高频细节，优于**Sapiens**（Khirodkar et al., arXiv 2024）和**RGB-X**（Zeng et al., SIGGRAPH 2024）等专用基线。

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/010_Figure_7.jpg]]
*Figure 7: Qualitative comparison of estimated normal. Our model outperforms all baselines and consistently achieves sharper and high-frequency details such as eyes, skin, and hair. Please zoom in for details*

### 消融研究：几何与重光照的协同效应

消融实验（Table 2, Figure 5）验证了联合建模的核心假设——几何与重光照之间存在双向协同。

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/007_Figure_5.jpg]]
*Figure 5: (a) Geometry is essential for relighting. Our full "Joint Modeling" (right) (b) Relighting provides shape-from-shading. Given a uniformly lit input captures 3D-dependent effects (wrinkles, shadows) absent in the "w/o Geom- (left), a smooth normal is produced (middle). A relit as condition provides etry" baseline (left). novel shading cues and enhances high-frequency normal generation (right). Figure 5. Ablation studies validating the synergy of joint modeling. Figure 5. Ablation studies validating the synergy of joint modeling*

**几何对重光照的贡献**：将几何模态从联合建模中移除（"w/o Geometry"模式），重光照PSNR从27.49骤降至21.19（**-6.3 dB**），SSIM从0.985降至0.976，LPIPS从0.0149升至0.0286。定性结果（Figure 5a）显示，无几何模式下模型无法捕捉阴影、衣物褶皱等3D依赖效应，而联合建模则能产生这些细粒度细节。这证实了几何信息为重光照提供了关键的遮挡和局部着色线索。

**重光照对几何的反哺**：当以真实重光照图像作为条件输入时，法线角度误差从12.24°降至9.10°（Table 2）。Figure 5b展示了这一效应：给定均匀光照输入时，模型仅能生成平滑的法线；而提供重光照图像后，模型能从明暗中推断出更详细、更准确的法线。这验证了shape-from-shading的协同机制——外观中的明暗信息有效增强了几何细节。

### 混合数据训练策略的有效性

战略性混合数据训练是弥合合成-真实域差距的关键。Figure 9展示了数据混合的渐进效果：仅使用合成数据（Synth）时，模型缺乏混合色胡须等真实世界特征；加入Light Stage数据（Dome）填补了这一空白，但由于光照舞台中LED激活模式不自然（要么极稀疏、要么全亮），产生了不真实的亮度偏压；引入大规模In-the-Wild数据（ITW）后，这一偏压得到纠正，生成了均衡自然的真实光照。Table 1中的模态开关掩码和混合训练模式是实现这一灵活训练策略的技术支撑。

### 失败模式与局限性

尽管GeoRelight展现了强大的性能，仍存在以下局限：

1. **纹理-几何歧义**：小物体（如纽扣、徽章）可能被模型误认为纹理而非独立3D结构，导致在法线和几何输出中消失，重光照时表现为平面图案。这一问题源于单目输入固有的深度歧义性。

2. **时间不一致性**：作为单帧生成模型，GeoRelight在处理动态光照序列时需要多次独立前向传递，可能产生帧间闪烁，缺乏时序一致的重光照结果。这限制了其在视频重光照场景中的直接应用。

3. **分布外主体**：极端姿态、严重遮挡或高度非朗伯材质（如镜面、金属衣物）可能导致性能下降或伪影。模型在合成数据上训练，对真实世界中复杂材质的泛化能力仍有提升空间。

### 补充图表

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/005_Table_1.jpg]]
*Table 1: Strategic training for mixing synthetic and real data*

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/012_Table_5.jpg]]
*Table 5: Albedo and Normal disentanglement evaluation. Geo-Relight achieves state-of-the-art albedo and normal estimation*

![[assets/figures/papers/paper_list_l2508_https_arxiv_org_abs_2604_20715/figures/014_Figure_9.jpg]]
*Figure 9: Benefit of In-the-Wild Data. Using only Synth uncovers gaps in the data like the lack of mixed colored beards. Adding Dome data fixes that but produces unrealistic brightness (middle) due to the unnatural LED activation (either very sparse or fully lit) in light stage captures. Adding large-scale ITW data corrects this bias, yielding balanced and realistic lighting (right)*



## 定位与知识库关联

### 1. 方法定位：从顺序管道到联合多模态生成

传统人物重光照方法遵循一个分阶段的顺序管道：首先估计输入图像的几何（如法线、深度）和内蕴属性（如反射率），然后基于这些中间表示进行物理渲染或神经重光照。这一范式存在根本性的瓶颈——**几何估计误差会直接累积到重光照阶段**，导致阴影错位、高光失真等物理不一致性。

GeoRelight 的方法论转向体现在两个层面：

**（1）任务关系的重新定义。** 与将几何视为重光照前置条件的传统观点不同，GeoRelight 将重光照与几何重建建模为**互促的联合生成任务**。核心洞察在于：精确几何提供遮挡和局部着色线索，而外观中的明暗信息则通过 shape-from-shading 机制增强几何细节。这一双向协同关系在消融实验中得到了量化验证：联合建模（Joint Modeling）相比无几何模式（w/o Geometry）在重光照 PSNR 上提升 **6.3 dB**（27.49 vs 21.19，Table 2）；反之，提供重光照图像作为条件可将法线角度误差从 12.24 降至 9.10（Table 2），证实了重光照对几何估计的反馈增益。

**（2）生成范式的统一。** GeoRelight 将视频潜空间扩散变换器（Video Latent DiT）的时间维度重新定义为模态维度 $M$，使得单次前向传递即可同时去噪重光照图像、反射率、法线、分割和 3D 几何共五种模态。这一设计区别于两类现有工作：

- **纯重光照扩散模型**（如 **IC-Light**, Zhang et al., ICLR 2025；**NeuralGaffer**, Jin et al., NeurIPS 2024；**DiLightNet**, Zeng et al., SIGGRAPH 2024）仅输出重光照图像，缺乏显式几何约束，难以生成物理上逼真的阴影和高光。
- **内蕴分解与正向渲染方法**（如 **DiffusionRenderer**, Liang et al., CVPR 2025；**RGB-X**, Zeng et al., SIGGRAPH 2024）虽涉及内蕴属性估计，但未将 3D 几何纳入统一的扩散框架中进行联合推理。

GeoRelight 的联合建模策略在定量指标上展现出显著优势：在合成数据上重光照 PSNR 达 **27.22**，远超 DiffusionRenderer 的 19.28（+7.94 dB，Table 3）；在 Light Stage 真实数据上达 25.87（+4.78 dB）；在几何重建上，Chamfer Distance 为 **0.766**，远低于单任务几何估计器 **VGGT**（Wang et al., CVPR 2025）的 3.37 和 **MoGe2**（Wang et al., 2025）的 3.54（Table 4）。

### 2. 关键技术贡献：iNOD 几何表示

GeoRelight 提出的**等距归一化正射深度（iNOD, isotropic Normalized Orthographic Depth）**是连接扩散模型与 3D 几何的关键桥梁。其设计动机源于一个实践瓶颈：标准点图在 VAE 编码后会产生噪声伪影，而各向异性归一化深度则严重扭曲 3D 形状（Figure 2）。

iNOD 通过两步操作解决这一问题：
1. **等距 3D 归一化**：基于几何体的最长边，将整个 3D 形状等比缩放至 $[-1, 1]$ 包围盒内，保留各向相对比例；
2. **正射投影**：沿 Z 轴取深度值，生成密集且无失真的深度图。

这一表示与 VAE 的压缩特性天然兼容，在潜空间中忠实地保留了 3D 边界信息，为联合扩散建模提供了可靠的几何监督信号。相比直接使用点图或标准深度图，iNOD 在 VAE 压缩-重建后能更好地保持几何细节，这是 GeoRelight 在几何重建上超越单任务专用模型（如 VGGT、MoGe2）的重要使能因素。

### 3. 数据策略与域适应

GeoRelight 的混合数据训练策略是弥合合成-真实域差距的关键设计。训练分两阶段进行：首先在合成数据上预训练 30K 步，然后进行 10K 步的混合数据训练（Section 4.1）。混合数据包含三个来源（Figure 4）：

- **合成数据（Synthetic）**：提供完备的多模态标注（重光照真值、反射率、法线、深度），但缺乏真实感；
- **光照舞台数据（Light Stage/Dome）**：提供配对的真实光照条件，但存在 LED 激活模式导致的亮度偏压（要么极稀疏，要么全亮）；
- **In-the-Wild 数据（ITW）**：大规模自然图像，通过合成数据预训练模型自动标注内蕴属性。

训练模式通过**模态开关掩码** $\mathbf{c}_\mathrm{switch} \in \mathbb{R}^{H \times W \times 1}$ 实现灵活的条件-目标切换（Table 1），使得不同数据源可根据其标注完整性参与不同子任务的训练。消融实验表明，仅使用合成数据会导致对混合色胡须等特征的覆盖缺失；加入 Dome 数据虽能修复此问题，但会引入不自然的亮度偏压；而大规模 ITW 数据的加入有效纠正了这一偏差，产生均衡且真实的光照效果（Figure 9）。

### 4. 适用边界与局限

尽管 GeoRelight 在定量指标和用户研究中表现突出（2AFC 用户研究中 93.8% 参与者偏好其重光照结果），其适用边界仍受以下因素制约：

**（1）纹理-几何歧义。** 小尺度物体可能被模型误认为纹理图案而非独立 3D 结构，导致其在法线和几何输出中消失，重光照时表现为平面贴图。这一问题源于单目输入的固有歧义性，联合建模并未完全解决。

**（2）时间不一致性。** 作为单帧生成模型，GeoRelight 对动态光照序列需执行多次独立前向传递，可能产生帧间闪烁。这与视频重光照方法（如 **Lux Post Facto**, Mei et al., CVPR 2025）形成对比，后者通过时序建模保证帧间一致性，但通常以牺牲单帧几何精度为代价。

**（3）分布外主体。** 极端姿态、严重遮挡或高度非朗伯材质（如镜面反射衣物、金属配饰）可能导致性能下降或伪影。模型主要在人物数据上训练，对非人物物体的泛化能力未经充分验证。

### 5. 开放问题与未来方向

GeoRelight 的框架设计为以下方向留下了探索空间：

- **时序一致性重光照**：如何将 3D RoPE 从空间域扩展至时间域，实现视频级联合重光照与几何重建，避免帧间闪烁？这涉及对更长时序建模能力和 3D RoPE 在视频场景下有效性的深入验证。
- **材质与物体类别的泛化**：当前框架聚焦于人物主体，能否扩展至包含非朗伯材料和复杂几何的广泛物体类别？这需要更大规模、更多样化的多模态标注数据。
- **替代传感模态的融合**：能否利用事件相机等替代传感模式，在保持时域一致性的同时提升对快速运动和极端光照的鲁棒性？
- **模态扩展的灵活性**：框架的模态开关掩码机制理论上支持任意模态的组合，未来可探索加入材质参数（如粗糙度、金属度）或语义分割等额外模态，进一步提升物理一致性。



## 原文 PDF

![[paperPDFs/CVPR_2026/GeoRelight_Learning_Joint_Geometrical_Relighting_and_Reconstruction_with_Flexible_Multi_Modal_Diffusion_Transformers.pdf]]
