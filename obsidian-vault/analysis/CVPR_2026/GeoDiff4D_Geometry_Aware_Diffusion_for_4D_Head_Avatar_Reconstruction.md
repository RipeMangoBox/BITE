---
title: "GeoDiff4D: Geometry-Aware Diffusion for 4D Head Avatar Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/GeoDiff4D_Geometry_Aware_Diffusion_for_4D_Head_Avatar_Reconstruction.pdf
project_link: "https://lyxcc127.github.io/geodiff4d/"
code_link: null
aliases:
- GeoDiff4D
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过联合预测RGB图像与表面法线，引入几何感知扩散先验，并结合姿势无关的隐式表情编码，为3D高斯泼溅提供强几何约束。
primary_logic: 联合建模RGB与法线分布，使扩散模型学习3D感知先验而非纯2D外观统计，从而在生成阶段即蕴含丰富几何信息，有效提升后续3D重建的保真度和视角一致性。
claims:
- 移除跨视角配对策略导致最大性能下降，PSNR降低1.691，AKD增加1.351，验证了多视角几何约束的关键作用。
- 移除联合表示学习后，模型的表情传递能力明显减弱，表明3D一致性对于解耦身份、姿态和表情至关重要。
- 层次化优化和法线正则化对减少极端姿态下的伪影和提升自由视角渲染质量贡献显著。
- NeRSemblev2 self-reenactment 上 PSNR ↑ = 19.951 (GeoDiff4D)
---

# GeoDiff4D: Geometry-Aware Diffusion for 4D Head Avatar Reconstruction

> [!tip] 核心洞察
> 联合建模RGB与法线分布，使扩散模型学习3D感知先验而非纯2D外观统计，从而在生成阶段即蕴含丰富几何信息，有效提升后续3D重建的保真度和视角一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | GeoDiff4D：面向四维头部化身重建的几何感知扩散模型 |
| 英文题名 | GeoDiff4D: Geometry-Aware Diffusion for 4D Head Avatar Reconstruction |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.24161) · [Project](https://lyxcc127.github.io/geodiff4d/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | GeoDiff4D |
| Dataset | NeRSemblev2 self-reenactment, Cross-reenactment, Self-reenactment |

> [!tip] 效果简介
> - NeRSemblev2 self-reenactment 上，PSNR ↑ 19.951 (GeoDiff4D) vs 19.295 (CAP4D) (+0.656)；LPIPS ↓ 0.195 (GeoDiff4D) vs 0.195 (CAP4D) (0.000)。
> - Cross-reenactment (mixed) 上，CSIM ↑ 0.671 (Our VGM) vs 0.655 (CAP4D) (+0.016)。
> - Self-reenactment (full pipeline) 上，JOD ↑ 6.720 (GeoDiff4D) vs 6.561 (CAP4D) (+0.159)。

## 概要

**问题瓶颈**：现有单视角4D头部化身重建方法主要依赖2D外观先验，缺乏3D几何一致性约束，导致在新视角下渲染质量显著下降，且难以捕捉皱纹、睫毛等细微表情细节。同时，表情编码与头部姿态的解耦不充分，进一步限制了跨视角动画的保真度。

**核心思路**：GeoDiff4D提出以**联合生成RGB图像与表面法线**为突破口，将3D几何感知引入扩散模型先验。具体而言，通过一个姿势无关的隐式表情编码器提取视点一致的表情特征，再以该特征为条件，使扩散模型同时预测多视角肖像帧及其对应的表面法线图。这一联合建模迫使扩散模型学习3D感知先验而非纯2D外观统计，从而在生成阶段即蕴含丰富的几何信息。随后，以生成的RGB帧、法线图及表情隐变量为三重监督，结合层次化网格优化，驱动3D高斯泼溅重建可动画化的4D头部化身。

**方法定位**：GeoDiff4D属于**扩散先验驱动的3D重建**范式，与现有工作的关键差异在于：(1) 扩散生成目标从单一RGB扩展为RGB-法线联合分布，赋予生成过程几何感知能力；(2) 表情编码器通过跨视角配对训练实现姿势无关的视点一致性，区别于依赖3DMM参数或隐式运动表示的传统方案；(3) 重建阶段同时利用生成的图像、法线和表情隐变量进行多模态监督，并引入可学习FLAME参数残差、U-Net顶点变形和MLP高斯属性细化三层递进优化，补偿单目跟踪误差。

**主要结果**：在NeRSemblev2自重建任务上，GeoDiff4D以PSNR 19.951、JOD 6.720超越CAP4D等基线方法；消融实验表明，移除跨视角配对策略导致PSNR下降1.691，AKD增加1.351，验证了多视角几何约束的核心作用。联合表示学习和法线正则化的移除同样造成明显的几何感知退化和重建质量下降。

### 问题背景：单视角4D头部化身重建

从单张肖像图像重建可动画化的4D头部化身，是计算机视觉与图形学交叉领域的核心挑战，直接支撑虚拟现实、远程临场、数字人交互等应用。其目标在于：给定一张参考图像，生成一个能够被任意表情和头部姿态驱动的三维头部模型，且在新视角下保持逼真渲染。这一任务要求模型同时解决身份保持、表情解耦、几何重建与视角泛化四个子问题。

近年来，3D高斯泼溅（3D Gaussian Splatting, 3DGS）凭借其高质量实时渲染能力，成为头部化身表示的主流范式。然而，从单张2D图像推断完整的3D几何与外观，本质上是高度病态的逆问题——单视角观测丢失了深度、遮挡区域和视角相关的细节信息。

### 现有方法缺口：2D先验的几何盲区

当前主流方法可大致分为两类：**前馈式方法**（如 **GAGAvatar**）通过编码器-解码器结构直接从单图回归3D高斯属性，速度快但泛化能力受限于训练数据规模；**优化式方法**（如 **Portrait4D-v2**、**CAP4D**）则利用预训练的2D生成模型（扩散模型或GAN）合成多视角伪真值，再以此监督3D重建。两类方法的共同瓶颈在于：**它们依赖的生成先验本质上是2D外观统计，缺乏对三维几何结构的显式感知**。

具体而言，现有扩散驱动的重建流水线仅生成RGB肖像帧，其学习目标局限于像素级颜色分布。这导致两个关键缺陷：

1. **视角一致性的脆弱性**：纯2D先验无法保证不同视角下生成的图像在几何上自洽，在新视角或极端姿态下容易产生纹理漂移、身份失真等伪影。
2. **细微几何的丢失**：表情变化涉及眼周、嘴角等区域的精细表面变形，RGB信号对这些几何细节的约束力不足，使得重建结果趋于平滑，缺乏表现力。

此外，表情编码的视角敏感性也是隐性问题。现有方法通常从单张驱动图像提取表情特征，但未显式保证该特征在不同相机视角下的不变性，导致驱动同一表情时，不同视角的渲染结果出现表情不一致。

### 本文动机：注入几何感知的扩散先验

针对上述缺口，本文提出一个核心洞察：**若扩散模型在生成阶段即蕴含丰富的几何信息，则下游3D重建可获得更强的结构约束，从而突破2D先验的瓶颈**。这一洞察驱动了GeoDiff4D框架的设计——通过联合建模RGB图像与表面法线的分布，使扩散模型学习3D感知先验，而非纯2D外观统计。

表面法线是稠密的几何信号，直接编码物体表面的局部朝向，与人脸的三维结构高度相关。将法线作为生成目标引入扩散模型，迫使模型在去噪过程中同时推理颜色与几何，从而内化视角一致的结构知识。进一步地，为解耦表情与姿态，本文设计姿势无关的隐式表情编码器，并通过跨视角配对训练策略强制学习视角不变的表情表示。

综上，GeoDiff4D的动机可归纳为：**以几何感知扩散先验替代纯2D外观先验，从生成源头为4D头部化身重建注入3D一致性，提升新视角渲染的保真度与表情传递的准确性**。

## 核心方法与创新机理

GeoDiff4D 的核心创新在于将**3D几何感知先验**注入扩散生成过程，从而弥合2D生成与3D重建之间的鸿沟。相较于现有方法仅依赖2D外观统计进行肖像生成，GeoDiff4D通过三个关键模块的协同设计，实现了从单张肖像图像到可动画化4D头部化身的端到端重建。

### 姿势无关的隐式表情编码

传统方法通常使用3DMM参数或隐式运动表示来编码表情，但这些表示往往与头部姿态耦合，缺乏跨视角一致性。GeoDiff4D提出了一种**姿势无关的表情编码器**（Pose-Free Expression Encoder），将驱动图像压缩为低维隐式特征 $f_{\text{mot}}$，该特征仅捕获面部动态细节而丢弃空间外观信息（Section 3.1）。

为确保编码器的视角不变性，作者设计了**跨视角配对训练策略**（Cross-View Pairing）：对于同一身份和时刻，将不同视角下的帧进行配对，使其共享一致的表情但具有不同的头部姿态。这一策略强制编码器学习视点无关的表达表示，从而在后续生成和重建中保持3D一致性（Figure 3）。

### 联合RGB-法线扩散生成

现有扩散驱动方法（如X-NeMo、LivePortrait）仅生成RGB肖像帧，缺乏显式的几何信息。GeoDiff4D首次提出**联合建模RGB图像与表面法线的扩散模型**，将生成目标从单一外观分布扩展为联合概率分布：

$$P ( I _ { r g b } , I _ { n o r m } | I _ { r e f } , M _ { r e f } , I _ { e x p } , M _ { d r v } )$$

这一设计的核心洞察在于：法线图编码了物体表面的3D几何结构，联合生成迫使扩散模型学习3D感知先验而非纯粹的2D纹理统计。为实现RGB域与法线域的有效交互，模型将传统2D自注意力替换为**3D域-空间注意力模块**（Domain-Spatial Attention），通过合并域维度和批次维度进行卷积处理，再将不同域的潜变量沿宽度维度拼接以执行联合注意力计算（Section 3.2）。

### 双监督3D高斯泼溅重建

在4D化身重建阶段，GeoDiff4D突破了仅使用生成RGB图像作为监督信号的局限，同时引入**生成法线图和表情隐变量**作为额外监督。具体而言，模型以3D高斯泼溅为表示，通过层次化优化策略补偿单目FLAME跟踪的误差：

- **可学习FLAME参数残差**：对姿态、表情等参数引入可学习偏移量
- **U-Net顶点变形预测**：以表情隐变量为条件，通过交叉注意力预测逐顶点变形
- **MLP高斯属性残差**：轻量级MLP预测逐基元的高斯属性细化

在此基础上，引入**表面法线正则化损失**：

$$\mathcal{L}_{n} = \lambda_{n} \mathcal{L}_{1}(\hat{n}, \alpha n)$$

该损失在前景区域计算渲染法线与伪真值法线之间的L1距离，为几何优化提供强约束（Section 3.3）。消融实验表明，移除层次化优化或法线正则化会导致极端姿态下伪影增加、自由视角渲染质量显著下降（Figure 9, 10）。

### 创新总结

GeoDiff4D相对于基线的关键改变可归纳为以下四个维度：

| 改变维度 | 基线方法 | GeoDiff4D |
|---------|---------|-----------|
| 表情编码 | 3DMM参数或隐式运动表示，未考虑视角一致性 | 姿势无关编码器 + 跨视角配对训练 |
| 扩散目标 | 仅生成RGB肖像帧 | 联合生成RGB + 表面法线，3D域-空间注意力 |
| 重建监督 | 仅RGB图像 | RGB + 法线 + 表情隐变量，法线正则化 |
| 几何优化 | 标准3DMM跟踪，无残差优化 | 层次化优化：参数残差 + U-Net变形 + MLP属性细化 |

消融实验的**决定性证据**表明：跨视角配对策略的移除导致PSNR下降1.691、AKD增加1.351，是性能影响最大的单一模块（Table 2）；联合表示学习的移除则显著削弱了模型的表情传递能力，验证了3D一致性对于解耦身份、姿态和表情的关键作用（Section 5.4）。

GeoDiff4D 的整体流水线由三个核心模块串联构成，形成“表达编码 → 几何感知生成 → 3D 化身重建”的端到端流程（Figure 2）。系统输入为一张参考肖像、驱动表情序列及对应的头部姿态，输出为可动画化的 4D 头部化身，支持实时自由视角渲染。

![[assets/figures/papers/paper_list_l966_https_arxiv_org_abs_2602_24161/figures/004_Figure_2.jpg]]
*Figure 2: Overall architecture. Our system takes a reference image, driving expressions, and head poses as input. Specifically, the reference image is encoded into hierarchical identity embeddings using a pretrained VAE and UNet-based reference network. Driving expressions are compressed into low-dimensional latents via a pose-free expression encoder. Both embeddings are injected into the diffusion model through cross-attention, while head pose maps concatenated with noise serve as inputs. The model then jointly predicts portrait images and surface normals. For 3D reconstruction, a UNet refines FLAME meshes using expression latents through cross-attention, and an MLP captures Gaussian dynamics. Final...*

**模块关系与数据流**：首先，参考图像通过预训练的 VAE 与基于 UNet 的参考网络编码为层次化身份嵌入（hierarchical identity embeddings），为后续生成提供多尺度身份先验。与此同时，驱动表情图像送入**姿势无关的表情编码器**，压缩为低维隐式表情潜变量 $f_{mot}$，该潜变量仅保留面部动态细节而丢弃空间外观信息，并通过跨视角配对训练策略确保视角一致性（Section 3.1）。随后，身份嵌入与表情潜变量通过交叉注意力注入**几何感知视频生成模型**；头部姿态图（由 FLAME 网格顶点法线光栅化得到，表情参数置零以最小化身份泄漏）与噪声拼接后作为扩散模型的输入。该模型联合预测多视角肖像帧及其对应的表面法线图，其核心在于用 3D 域-空间注意力（Domain-Spatial Attention）替代普通 2D 自注意力，实现 RGB 与法线两个域之间的跨域交互（Section 3.2）。最后，生成的图像、法线及表情潜变量共同作为监督信号，驱动**3D 高斯泼溅重建模块**与**层次化网格优化模块**：UNet 以表情潜变量为条件通过交叉注意力细化 FLAME 网格顶点变形，MLP 预测逐高斯原语的属性残差，同时引入表面法线正则化损失 $\mathcal{L}_n$ 在前景区域约束渲染法线与伪真值法线的一致性（Section 3.3）。

**关键设计逻辑**：整个流水线的因果枢纽在于“联合 RGB-法线生成”。传统方法仅依赖 2D 外观先验，缺乏几何约束，导致新视角下伪影严重。GeoDiff4D 通过让扩散模型学习 $P(I_{rgb}, I_{norm} | I_{ref}, M_{ref}, I_{exp}, M_{drv})$ 的联合分布，使生成阶段即蕴含丰富的 3D 几何信息，从而为后续 3D 高斯泼溅提供强几何先验，有效提升重建保真度与视角一致性。消融实验证实，移除跨视角配对策略导致 PSNR 下降 1.691、AKD 增加 1.351（Table 2），而移除联合表示学习则使几何感知能力显著退化（Section 5.4），验证了各模块在因果链中的必要性。

GeoDiff4D 由三个关键组件构成：姿势无关的表情编码器、几何感知视频生成模型、以及基于3D高斯泼溅的4D化身重建模块。下面逐一剖析各模块的设计机理与核心公式。

### 姿势无关的表情编码器

该模块从单张驱动图像中提取一个低维隐式表情特征 $f_{mot}$，其核心设计目标是**视点一致性**——即同一表情在不同相机视角下应映射到相近的隐变量，而非混入姿态或外观信息。

为实现这一目标，编码器架构采用卷积网络将输入图像压缩为一维向量，**刻意丢弃空间外观信息**，仅保留面部动态特征。训练策略上，引入**跨视角配对**（cross-view pairing）：对同一身份在同一时刻、相同表情但不同视角的帧进行配对，强制编码器学习视点无关的表达表征（Figure 3）。消融实验表明，移除跨视角配对导致PSNR下降1.691、AKD增加1.351，验证了多视角一致性约束对整体性能的关键作用（Table 2）。

### 几何感知视频生成模型

该模块是GeoDiff4D的核心创新——**首次将扩散模型从纯2D外观生成拓展到联合RGB-法线生成**，使模型学习3D感知先验而非单纯的纹理统计。

**联合分布建模**：给定参考图像 $I_{ref}$、参考法线图 $M_{ref}$、驱动表情图像 $I_{exp}$ 和驱动法线图 $M_{drv}$，模型学习生成RGB帧 $I_{rgb}$ 与对应表面法线图 $I_{norm}$ 的联合条件分布：

$$P ( I _ { r g b } , I _ { n o r m } \mid I _ { r e f } , M _ { r e f } , I _ { e x p } , M _ { d r v } )$$

**3D域-空间注意力**：为实现RGB域与法线域之间的有效交互，模型将标准2D自注意力替换为3D域-空间注意力模块。具体而言，域维度和批次维度在卷积处理前合并，在注意力模块前分离；不同域的隐变量沿宽度维度拼接，形成统一的令牌序列进行注意力计算，从而实现跨域信息融合。

**条件注入**：参考图像经预训练VAE和UNet参考网络编码为层次化身份嵌入，通过交叉注意力注入扩散模型；表情隐变量同样经交叉注意力注入；头部姿态则以法线图形式（从FLAME网格顶点法线光栅化得到，表情参数置零以最小化身份泄露）与噪声拼接作为模型输入。

### 4D化身重建与层次化优化

生成阶段产出的多视角RGB帧和法线图，共同作为3D高斯泼溅重建的监督信号。

**表面法线正则化损失**：除了标准RGB重建损失外，引入法线正则化项，计算渲染法线 $\hat{n}$ 与伪真值法线 $n$ 在前景区域（由alpha掩码 $\alpha$ 控制）的L1距离：

$$\mathcal{L}_{n} = \lambda_{n} \mathcal{L}_{1}(\hat{n}, \alpha n)$$

这一损失为3D高斯泼溅提供了显式的几何约束，有效抑制极端姿态下的伪影。

**层次化网格优化**：为补偿单目FLAME跟踪的误差，采用三级细化策略：(1) 为FLAME参数引入可学习残差；(2) 使用U-Net预测逐顶点变形，以表情隐变量经交叉注意力驱动；(3) 轻量MLP预测逐高斯原语的属性残差（颜色、不透明度等）。消融实验证实，层次化优化和法线正则化对恢复精细面部细节和自由视角渲染质量贡献显著（Figure 9, 10）。

### 模块间因果链路

表情编码器提取的视点一致隐变量同时注入扩散模型和重建模块，形成统一的表情控制信号；扩散模型联合生成的RGB-法线对为3D高斯泼溅提供双模态监督，其中法线监督直接约束表面几何，弥补了纯RGB监督在3D一致性上的不足；层次化优化则从网格几何层面进一步修正跟踪误差，三者协同构成了从2D生成先验到3D重建的完整因果链。

## 实验与关键发现

### 实验设置

GeoDiff4D 的实验分为两个阶段：视频生成模型（VGM）训练和4D化身重建。VGM 训练分两阶段进行，均使用 AdamW 优化器，学习率 1e-5，在 4 张 A800 GPU 上分别训练 80K 和 20K 次迭代，总耗时约 3-4 天。化身重建阶段在单张 RTX 3090 上运行 100K 步，约需 3 小时。数据生成方面，使用训练好的 VGM 以 25 步 DDIM 调度合成 12 个视角、约 200 帧的肖像视频作为重建监督。

评估采用 NeRSemblev2 数据集的 self-reenactment（自重建）子集，该子集包含大量极端头部姿态的参考图像和驱动序列，能全面检验模型性能。Cross-reenactment（跨重建）评估则混合了 NeRSemblev2 子集与 in-the-wild 运动数据，涵盖真实和卡通身份，以测试泛化能力。指标涵盖图像质量（PSNR、SSIM、LPIPS）、身份保持（CSIM、JOD）和时序一致性（AKD、AED）。

### 主实验结果

**Table 1** 汇总了自重建与跨重建的定量结果。在自重建任务上，GeoDiff4D 的完整视频生成模型（VGM Ours）在所有图像质量指标上均取得最优：PSNR 达 21.586，SSIM 0.831，LPIPS 0.174，CSIM 0.754，JOD 7.127，AKD 4.016，AED 2.340。经 3D 高斯泼溅重建后的 GeoDiff4D 在多数指标上位列第二，PSNR 为 19.951，较最强基线 CAP4D 的 19.295 提升 0.656 dB，JOD 从 6.561 提升至 6.720。LPIPS 与 CAP4D 持平（均为 0.195），表明感知质量相当。

跨重建任务上，GeoDiff4D 的 VGM 在 CSIM 指标上达到 0.671，优于 CAP4D 的 0.655，验证了模型在跨身份驱动场景下的身份保持优势。

**Figure 4** 展示了自重建的定性对比。在极端姿态下，GeoDiff4D 生成的法线图准确捕捉了面部几何结构，渲染结果在嘴部、眼部等细节区域保持了更高的保真度，而基线方法在类似条件下出现明显的纹理模糊和几何失真。

**Figure 5** 的跨重建结果表明，GeoDiff4D 在真实人脸和卡通风格身份上均能生成一致的动画效果，展现了良好的域泛化能力。

### 消融实验

**Table 2** 系统消融了视频生成模型和化身重建两个阶段的关键设计。对 VGM 而言，**跨视角配对策略**被证明最为关键——移除后 PSNR 从 21.586 骤降至 19.895（-1.691），AKD 从 4.016 恶化至 5.367（+1.351），AED 从 2.340 升至 3.113（+0.773），表明多视角一致性训练对学习视点无关的表情表征至关重要。移除联合表示学习后，PSNR 降至 20.809，CSIM 从 0.754 降至 0.743，验证了 RGB-法线联合建模对几何感知能力的贡献。移除 Domain-Spatial 注意力模块同样导致各项指标全面下降，说明跨域特征交互对生成质量有显著增益。合成数据的移除主要影响法线生成的高频细节（**Figure 7**），对整体指标影响相对温和。

对化身重建阶段，**层次化优化**和**法线正则化**的贡献在 **Figure 9** 和 **Figure 10** 中清晰可见。移除层次化优化后，重建结果在嘴部、眼部等细节区域出现明显伪影，自由视角渲染质量显著下降。移除法线正则化后，几何结构在极端姿态下出现扭曲，验证了法线监督对维持 3D 一致性的关键作用。

![[assets/figures/papers/paper_list_l966_https_arxiv_org_abs_2602_24161/figures/013_Figure_9.jpg]]
*Figure 9: Ablation on 4D reconstruction. We ablate hierarchical refinement and normal regularization to evaluate their contributions to reconstruction quality*

![[assets/figures/papers/paper_list_l966_https_arxiv_org_abs_2602_24161/figures/014_Figure_10.jpg]]
*Figure 10: Ablations on hierarchical refinement and normal regularization for free-view rendering*

**Figure 11** 对比了使用 GeoDiff4D 生成法线与使用单目法线估计器 DAViD 的法线作为监督的差异。生成法线在几何细节和时序一致性上均优于 DAViD 估计结果，证明了联合扩散生成策略相对于后处理估计的优越性。

### 与更多基线的对比

**Table 3** 和 **Figure 12** 将 GeoDiff4D 与 GAGAvatar、Portrait4D-v2、LAM、CAP4D 等单视角4D头部化身重建方法进行了定量和定性比较。GeoDiff4D 在自重建场景下取得了最优或次优的整体性能，尤其在极端姿态下的几何保真度方面优势明显。与 X-NeMo、LivePortrait 等 2D 动画方法的定性对比显示，GeoDiff4D 在自由视角渲染中保持了更好的 3D 结构一致性。

### 扩散采样步数分析

**Table 4** 消融了 DDIM 采样步数对生成质量的影响。25 步在质量与速度间取得最佳平衡（2.74 秒/帧），减少步数会导致质量下降，增加步数则收益递减。

### 失败模式与局限性

尽管整体性能优异，GeoDiff4D 仍存在以下失败模式：

1. **3DMM 跟踪依赖**：系统严重依赖单目 FLAME 跟踪进行头部姿态估计，该问题本身具有不适定性。在极端遮挡或快速运动场景下，跟踪误差会传播至生成和重建阶段，导致姿态偏差。

2. **舌头运动缺失**：虽然视频生成模型能够合成舌头运动，但受限于 FLAME 模型缺乏细粒度舌头参数化，最终化身无法准确重建舌头动态，在张嘴说话等表情中可能出现口腔区域模糊。

3. **推理速度瓶颈**：25 步 DDIM 采样需 2.74 秒/帧，难以满足实时交互需求。这是扩散模型固有的速度限制，需要通过蒸馏或高效求解器进一步优化。

4. **合成-真实域差异**：训练依赖合成数据提供法线真值，合成到真实的域差异可能限制在极端真实场景下的泛化性能，尤其在皮肤纹理细节和光照复杂的情况下。

### 关键图表结论速览

| 图表 | 核心结论 |
|------|---------|
| **Table 1** | GeoDiff4D 在自重建和跨重建任务上全面超越现有基线，PSNR 提升 0.656 dB |
| **Table 2** | 跨视角配对是最大贡献因子，移除后 PSNR 下降 1.691，AKD 增加 1.351 |
| **Figure 4** | 极端姿态下，GeoDiff4D 生成的法线图和渲染结果保持高几何保真度 |
| **Figure 9/10** | 层次化优化和法线正则化对减少伪影、提升自由视角渲染质量至关重要 |
| **Figure 11** | 生成法线优于 DAViD 单目估计法线，验证了联合扩散策略的优势 |
| **Table 4** | 25 步 DDIM 采样在质量-速度权衡中最优 |

![[assets/figures/papers/paper_list_l966_https_arxiv_org_abs_2602_24161/figures/007_Table_1.jpg]]
*Table 1: Quantitative results of self-reenactment on the NeRSemblev2 dataset and cross-reenactment on a mixture of NeRSemblev2 subset and in-the-wild motion data. Bold and underlined indicate the best and second-best results, respectively*

![[assets/figures/papers/paper_list_l966_https_arxiv_org_abs_2602_24161/figures/009_Table_2.jpg]]
*Table 2: Ablation study. For video generation model, we ablate joint representation, Domain-Spatial attention module, cross-view pairing strategy and synthetic data. For avatar reconstruction, we ablate hierarchical refinement, normal regularization and generated normal(vs. normal from DAViD)*

![[assets/figures/papers/paper_list_l966_https_arxiv_org_abs_2602_24161/figures/015_Figure_11.jpg]]
*Figure 11: Ablations on our normals versus DAViD normals*

> **注意**：部分基线方法（如 GAGAvatar、Portrait4D-v2）的具体引用元数据未在分析中提供，建议查阅原文参考文献列表进行核实。

## 定位与知识库关联

### 在头部化身重建领域中的位置

GeoDiff4D 处于**单视角4D头部化身重建**这一活跃研究线，其核心贡献在于首次将**几何感知扩散先验**引入该任务，突破了现有方法主要依赖2D外观统计的瓶颈。从方法范式上，可将其与以下代表性工作形成对比：

**前馈式重建方法**（如 **GAGAvatar**）以单次前向推理生成3D/4D化身，速度优势明显，但缺乏对复杂表情和极端姿态的精细建模能力。GeoDiff4D 采用“生成-优化”两阶段流水线，以额外的优化时间为代价，换取显著提升的几何保真度和视角一致性。

**优化式重建方法**（如 **Portrait4D-v2**）通过逐样本优化获得高质量化身，但其监督信号通常仅来自生成的RGB图像，缺少显式的3D几何约束。GeoDiff4D 的关键改进在于**联合生成RGB与表面法线**，并在优化阶段引入法线正则化损失 $\mathcal{L}_{n} = \lambda_{n} \mathcal{L}_{1}(\hat{n}, \alpha n)$，使3D高斯泼溅的优化同时受外观和几何双重监督，从而有效抑制新视角下的伪影。

**通用框架方法**（如 **LAM**）和**两阶段流水线**（如 **CAP4D**）虽支持单视角输入，但表情编码通常依赖3DMM参数或隐式运动表示，未显式建模跨视角一致性。GeoDiff4D 提出的**姿势无关隐式表情编码器**配合跨视角配对训练策略，从机制上解耦了表情与头部姿态，使提取的表达特征在多个视点下保持一致——消融实验表明，移除该策略导致PSNR下降1.691、AKD增加1.351，验证了多视角几何约束对重建质量的关键作用。

### 与扩散驱动生成方法的关联

GeoDiff4D 的视频生成模块（VGM）借鉴了扩散模型在肖像动画领域的成功经验。与纯2D的扩散驱动动画方法（如 **X-NeMo**）相比，GeoDiff4D 的扩散模型输出从RGB扩展到RGB-法线联合空间，通过3D域-空间注意力实现跨域特征交互，使扩散过程本身即蕴含3D感知先验。与基于GAN的动画方法（如 **LivePortrait**）和视频生成式方法（如 **Wan-Animate**）相比，GeoDiff4D 的生成结果直接服务于下游3D重建，而非止于2D像素级逼真度。

### 适用边界

1. **输入模态**：单张参考肖像 + 驱动表情序列 + 头部姿态序列。参考图像需包含清晰的面部特征，驱动表情需由FLAME模型可表达的表情空间覆盖。
2. **身份泛化**：在NeRSemblev2数据集内及混合in-the-wild数据上均展现出良好的身份保持能力（CSIM 0.671），但对训练分布外的大跨度身份变化，泛化性仍需进一步验证。
3. **姿态鲁棒性**：受益于姿势无关的表情编码器，模型对驱动姿态变化具有较强鲁棒性；但极端姿态下的重建质量仍受限于单目3DMM跟踪的精度。
4. **舌头运动**：视频生成模型可合成舌头运动，但最终3D化身无法准确重建舌头，受限于FLAME模型缺乏细粒度舌头参数化。

### 局限与开放问题

**已知局限**（论文明确承认）：
- 严重依赖单目3DMM跟踪进行头部姿态估计，该问题本身具有不适定性，可能引入级联误差。
- 扩散模型采样速度较慢（25步DDIM需2.74秒/帧），难以满足实时应用需求。
- 训练依赖多视角和合成数据，合成到真实的域差异可能限制极端真实场景下的泛化性。

**开放问题**（论文未解决但自然引出）：
- 如何减少对单目3DMM跟踪的依赖？探索自监督姿态估计或端到端联合优化可能是可行方向。
- 几何感知扩散框架能否扩展到全身或通用物体的4D重建？联合RGB-法线生成的思路在理论上具有通用性，但需解决更大空间尺度下的几何一致性挑战。
- 如何进一步加速扩散采样？蒸馏、一致性模型或高效常微分方程求解器（如DPM-Solver++）是值得探索的加速路径。
- 合成数据的利用策略是否可进一步优化？例如通过域自适应或真实-合成混合训练，缩小域差异并提升真实场景性能。

> **注意**：上述基线方法的具体作者、会议和年份信息在提供的分析材料中未完整给出，建议查阅原文参考文献列表进行补充验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/GeoDiff4D_Geometry_Aware_Diffusion_for_4D_Head_Avatar_Reconstruction.pdf]]
