---
title: "ELITE: Efficient Gaussian Head Avatar from a Monocular Video via Learned Initialization and Test-time Generative Adaptation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ELITE_Efficient_Gaussian_Head_Avatar_from_a_Monocular_Video_via_Learned_Initialization_and_Test_time_Generative_Adaptation.pdf
project_link: "https://kim-youwang.github.io/elite"
code_link: null
aliases:
- ELITE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过将预训练的3D数据先验模型（Mesh2Gaussian Prior Model）作为前馈初始化，并将退化的高斯化身渲染作为强条件输入，驱动单步扩散增强器生成身份保持的高质量图像，进一步用于测试时适应性微调。这样，3D先验为2D生成提供了可靠的几何与外观基础，2D生成先验则补偿了3D初始化中缺失的视角和表情细节，形成互补协同。
primary_logic: 3D数据先验与2D生成先验具有天然的互补性：(1) 3D渲染（即使质量下降）已包含丰富的结构与外观信息，可以作为扩散模型的强初始化，从而由纯噪声去噪转为渲染增强，大幅降低采样步数、抑制身份漂移并提升速度；(2) 由合成数据提供的测试时生成式适应使得3D先验模型能够泛化到训练集未曾见过的野生姿态与表情。二者的系统耦合是实现高效、高保真、身份一致的头像合成的关键。
claims:
- ELITE在INSTA数据集的自重演任务上全面超越所有基线方法：PSNR=25.220，LPIPS=0.0732，CSIM=0.7396，身份保持明显优于纯2D生成先验方法CAP4D。
- 与全去噪扩散方法CAP4D（每张18秒，CSIM=0.4144）相比，ELITE的渲染引导单步增强不仅将生成速度提升60倍（0.3秒/张），而且身份一致性大幅提升至CSIM=0.9793。
- 消融实验（Table S1）证明，同时使用3D数据先验与2D生成先验的混合系统在自重演（PSNR 28.68，LPIPS 0.0585）和交叉重演中均取得最佳质量和泛化能力，单独使用任一先验都会导致几何坍塌或外观泛化不足。
- ELITE仅用3帧输入视频即可合成完整的高斯化身，并可在20分钟内完成整个测试时适应性过程，速度远快于需要400分钟的CAP4D。
---

# ELITE: Efficient Gaussian Head Avatar from a Monocular Video via Learned Initialization and Test-time Generative Adaptation

> [!tip] 核心洞察
> 3D数据先验与2D生成先验具有天然的互补性：(1) 3D渲染（即使质量下降）已包含丰富的结构与外观信息，可以作为扩散模型的强初始化，从而由纯噪声去噪转为渲染增强，大幅降低采样步数、抑制身份漂移并提升速度；(2) 由合成数据提供的测试时生成式适应使得3D先验模型能够泛化到训练集未曾见过的野生姿态与表情。二者的系统耦合是实现高效、高保真、身份一致的头像合成的关键。

| 字段 | 内容 |
|------|------|
| 中文题名 | ELITE: 基于3D-2D先验协同的单目视频高效高斯头部化身合成 |
| 英文题名 | ELITE: Efficient Gaussian Head Avatar from a Monocular Video via Learned Initialization and Test-time Generative Adaptation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.10200) · [Project](https://kim-youwang.github.io/elite) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ELITE |
| Dataset | INSTA Self Re-enactment, INSTA Synthesis Speed |

> [!tip] 效果简介
> - INSTA Self Re-enactment 上，PSNR 25.220 vs 24.838 (SplattingAvatar) (+0.382)；SSIM 0.8771 vs 0.8831 (SplattingAvatar) (-0.006)；LPIPS 0.0732 vs 0.0893 (SplattingAvatar) (-0.0161 (improved))。
> - INSTA Synthesis Speed 上，总合成时间 20 分钟 vs 400 分钟 (CAP4D) (20× 快)。
> - 生成图像身份保持与速度 上，CSIM / 每张生成时间 0.9793 / 0.3 秒 vs 0.4144 / 18 秒 (CAP4D) (CSIM +0.5649 / 速度 60×)。

## 概要

从一段随手拍摄的单目视频中合成可驱动、照片级真实的三维头部化身，是数字人、VR/AR与远程通信等应用的核心需求。现有方法通常**孤立地依赖单一先验**：基于3D数据先验的方法受限于训练数据的域分布，难以泛化到野生场景中未见过的姿态与表情；基于2D生成先验的方法虽能提供多样化的监督信号，但其全去噪生成过程缓慢、计算成本高昂，且容易出现严重的身份混淆。两种先验各自的短板长期未能得到系统性的互补。

ELITE 的核心洞察在于：**3D数据先验与2D生成先验具有天然的互补性**。3D渲染（即使质量有所下降）已携带着丰富的结构与外观信息，可以作为扩散模型的强条件输入，将生成过程从“纯噪声去噪”转化为“渲染增强”，从而大幅压缩采样步数、抑制身份漂移并提升生成速度；反过来，由合成数据驱动的测试时生成式适应，使3D先验模型能够泛化到训练集中从未出现过的野生姿态与表情。二者的系统耦合，是实现高效、高保真、身份一致的头像合成的关键。

基于这一思想，ELITE 构建了一个**两阶段测试时适应框架**：首先利用预训练的 Mesh2Gaussian Prior Model (MGPM) 进行前馈初始化，为化身提供身份保持的几何与外观基础；随后，以退化的高斯化身渲染作为强条件，驱动单步扩散增强器生成高质量、身份一致的多视角/多表情图像，并以此作为监督信号进行第二阶段的生成式微调。这一设计使得 ELITE 仅需 **3 帧输入视频**即可在 **20 分钟**内完成完整的化身合成，生成速度比全去噪扩散方法快 **60 倍**，同时身份保持指标 CSIM 从 0.4144 跃升至 0.9793。

在 INSTA 数据集的自重演任务上，ELITE 在 PSNR（25.220）、LPIPS（0.0732）和 CSIM（0.7396）等关键指标上全面超越现有基线方法；消融实验进一步证实，同时使用 3D 数据先验与 2D 生成先验的混合系统在自重演与交叉重演中均取得最佳质量与泛化能力，单独使用任一先验都会导致几何坍塌或外观泛化不足。

在方法谱系上，ELITE 区别于三类现有范式：**过拟合方法**（如 FlashAvatar、SplattingAvatar）从模板网格初始化 3D 高斯，仅用真实帧监督，缺乏先验引导；**3D 数据先验方法**（如 SynShot）利用合成数据训练先验模型，但测试时仍仅依赖真实帧，泛化受限；**2D 生成先验方法**（如 CAP4D）使用多视角扩散生成图像作为监督，却从零开始优化且生成缓慢。ELITE 同时继承了 3D 先验的初始化优势与 2D 生成先验的泛化能力，并通过单步扩散增强与两阶段适应策略，实现了速度、保真度与身份一致性的协同提升。

**局限与展望**：ELITE 对异常光照条件敏感，缺乏显式的光照或材质建模；对眼镜等配件的几何结构完全烘焙为纹理，无法进行三维建模；3D 先验训练集仅约 400 个身份，多样性仍有提升空间。未来工作可探索引入光照先验、扩展至附件几何联合建模，以及将该框架推广至全身化身或交互式 VR 场景。



### 问题背景

从单目视频中合成可动画的逼真3D头部化身是计算机视觉与图形学中的一项基础挑战。该任务的目标是仅凭一段日常拍摄的单人讲话或表情视频，重建出一个可以在任意视角、任意表情下驱动的高保真3D头部模型。这一能力在虚拟现实、远程通信、游戏和影视制作等场景中有广泛的应用前景。

近年来，3D高斯泼溅（3D Gaussian Splatting, 3DGS）凭借其高效的渲染速度与出色的视觉质量，成为化身重建的主流表征形式。然而，单目视频本身的信息高度稀疏：输入视频通常只覆盖有限的视角范围和表情变化，这意味着直接从稀疏观测中优化一个完整的3D化身是一个严重的欠定问题。

### 现有方法缺口：3D先验与2D先验各自为战

为弥补单目视频的信息缺失，现有方法分别引入了两类先验，但两者始终未能有效结合：

**（1）3D数据先验方法**：这类方法利用大规模多视角人脸数据集预训练一个3D先验模型，在测试时提供前馈初始化，随后仅用输入视频的真实帧进行微调。代表工作包括 **SynShot** 等。其优势在于初始化的几何结构稳定、身份保持较好；但瓶颈在于——3D先验模型的训练域有限（通常仅覆盖数百个身份、受控的实验室光照），当测试视频的姿态、表情或光照条件超出训练分布时，模型缺乏足够的泛化能力，难以补充缺失的视角和微表情细节。

**（2）2D生成先验方法**：这类方法利用预训练的2D扩散模型（如多视角扩散模型）生成合成图像，为化身优化提供额外的监督信号。代表工作如 **CAP4D**。其优势在于2D扩散模型在海量图像数据上训练，具备丰富的视觉先验，可以生成多样化的视角和表情；但存在三个关键缺陷：一是扩散生成采用从纯噪声开始的全去噪过程，每张图像生成耗时约18秒，速度极慢；二是从零开始优化化身（无3D初始化），收敛不稳定；三是全去噪生成缺乏对目标身份的结构性约束，容易出现**身份混淆**（identity hallucination）——生成的人脸与目标人物长相不一致。

图2系统对比了四类范式：过拟合方法（**FlashAvatar**、**SplattingAvatar**）从模板网格初始化的3D高斯出发，仅用真实帧监督，无任何先验；3D数据先验方法虽提供学习到的初始化，但监督来源仍仅限于真实帧；2D生成先验方法使用扩散生成图像作为监督，却从零优化化身且生成缓慢。**ELITE的核心洞察在于：3D数据先验与2D生成先验具有天然的互补性，但现有工作始终未能将二者系统耦合。**

### 核心动机：3D-2D先验协同

ELITE的出发点是回答一个关键问题：**能否让3D先验为2D生成提供可靠的结构基础，同时让2D生成先验补偿3D先验在泛化性上的不足？**

这一协同的可行性建立在两个关键观察之上：

**观察一：退化渲染是天然的强条件。** 即使3D化身渲染的质量有所下降（例如由于初始化不完美或视角缺失导致的模糊、伪影），该渲染仍然忠实地保留了目标身份的结构、纹理和姿态信息。将其作为扩散模型的输入条件，可以将生成任务从“从纯噪声去噪”转化为“渲染增强”——模型只需修复和细化已有的结构，而非从零想象一张人脸。这大幅降低了生成难度，使得单步去噪成为可能，同时从机制上抑制了身份漂移。

**观察二：生成式适应弥补分布外泛化。** 3D先验模型在训练时未曾见过的野生姿态和表情，恰是2D扩散模型的长项。通过将扩散增强生成的多视角、多表情图像作为测试时监督，可以驱动3D化身向分布外区域泛化，而无需依赖真实采集数据。

基于以上动机，ELITE提出了“3D先验前馈初始化 + 2D生成先验测试时增强”的混合框架，首次实现了两类先验的系统级协同，在效率、保真度和身份一致性三个维度上同时取得突破。



## 核心方法与创新机理

ELITE的核心创新在于**首次系统性地耦合3D数据先验与2D生成先验**，通过“前馈初始化—真实帧对齐—生成式泛化”的三阶段协同，解决了单目视频头部化身合成中长期存在的效率-保真度-泛化性三角矛盾。与现有方法仅单独依赖某一类先验不同，ELITE揭示了二者的天然互补性：3D先验为2D生成提供可靠的几何与外观锚点，2D生成先验则补偿3D初始化中缺失的视角与表情细节。

### 关键设计变更（Changed Slots）

**1. 3D表征初始化：从模板网格到数据驱动前馈预测**

传统过拟合方法（如**FlashAvatar**、**SplattingAvatar**）从FLAME模板网格上的3D高斯原语开始，从零优化，缺乏任何先验引导；3D数据先验方法（如**SynShot**）虽引入了学习的初始化，但仍仅依赖真实帧监督，泛化能力受限于训练数据的域分布。

ELITE设计了**Mesh2Gaussian Prior Model (MGPM)**——一个预训练的U-Net，输入标准空间的FLAME UV纹理图与几何图的拼接以及驱动信号 $\Theta$，前馈输出UV对齐的2D高斯参数图：

$$\mathbf { M } _ { \mathrm { g s } | \Theta } = \mathcal { F } _ { \phi } ( [ \mathbf { M } _ { \mathrm { t e x } } , \mathbf { M } _ { \mathrm { g e o } } ] , \Theta )$$

这一前馈初始化提供了快速、稳定且身份保持的起点，为后续测试时适应奠定了几何与外观基础（见Figure 3、Figure 4）。消融实验证实，MGPM初始化是高质量合成的必要条件——直接去除该模块会导致几何坍塌（Table S1, Figure S2）。

**2. 测试时监督来源：从单一监督到真实-生成混合监督**

现有方法的监督来源存在根本性分裂：3D数据先验方法仅使用真实视频帧，受限于输入视角的稀疏性；2D生成先验方法（如**CAP4D**）仅使用扩散生成的合成图像，虽能提供多视角监督，但从零优化且生成图像存在严重的身份混淆（identity hallucination）。

ELITE采用**两阶段测试时适应性策略**：Stage 1仅用少量真实帧（默认仅3帧）微调MGPM，消除前馈初始化的身份偏移并补充细节（Figure 5）；Stage 2引入单步扩散增强器生成的合成图像作为额外监督，驱动化身泛化到未见过的姿态与表情（Figure 6b）。这一混合监督策略使ELITE成为唯一在交叉重演中同时实现逼真几何与外观泛化的方案（Table S1）。

**3. 合成图像生成方式：从全去噪扩散到渲染引导单步增强**

CAP4D等2D生成先验方法从纯噪声开始全扩散去噪生成监督图像，这不仅速度极慢（每张18秒），更重要的是缺乏对目标身份的结构性约束，导致严重的身份漂移（CSIM仅0.4144，Figure 9）。

ELITE的核心洞察是：**退化的3D化身渲染已经包含丰富的结构与外观信息，可以作为扩散模型的强条件输入**，将生成任务由“从零创造”转化为“渲染增强”。具体而言，ELITE微调单步图像翻译扩散模型SD-Turbo，以退化Avatar渲染 $\mathbf{I}_{\mathrm{gen}}$ 和干净参考帧 $\mathbf{I}_{\mathrm{real}}$ 为输入，通过一次去噪生成高质量、身份保持的图像：

$$\mathbf{I}_{\mathrm{gen}}^\star = \mathcal{D}_\xi([\mathbf{I}_{\mathrm{gen}}, \mathbf{I}_{\mathrm{real}}])$$

这一设计带来双重收益：（1）生成速度提升60倍（0.3秒/张 vs. 18秒/张）；（2）身份一致性从0.4144跃升至0.9793（Figure 9），从根本上抑制了身份混淆。

**4. 适应性阶段数量：从单阶段到两阶段渐进式适应**

大多数现有方法仅进行一次测试时微调或完全从零优化，缺乏对“对齐”与“泛化”两个目标的解耦。ELITE的两阶段设计将二者分离：Stage 1专注于与输入视频的身份对齐（保真度），Stage 2专注于未见视角与表情的泛化（泛化性）。消融实验（Figure 10c）逐步展示了MGPM初始化→Stage 1→Stage 2的质量递进，验证了每个阶段的独立贡献。

### 创新协同的本质

上述四个变更槽位并非孤立改进，而是围绕一个核心机制环环相扣：**3D先验提供锚点→真实帧消除偏差→渲染增强生成监督→生成监督驱动泛化**。正是这一闭环使得ELITE仅需3帧输入、20分钟即可合成完整的高斯化身，而纯2D生成先验方法CAP4D需要400分钟（Table 1）。这种效率-质量-身份一致性的同步突破，根源于对两类先验互补性的深刻利用，而非单一技术的渐进式改进。



ELITE 的整体 pipeline 围绕一个核心洞察构建：**3D 数据先验与 2D 生成先验具有天然的互补性**。现有方法或仅依赖 3D 数据先验（受限于训练域分布，难以泛化至 in-the-wild 场景），或仅依赖 2D 生成先验（全去噪生成缓慢、计算成本高、易出现身份混淆），两者未能协同。ELITE 通过系统耦合这两种先验，使 3D 先验为 2D 生成提供可靠的几何与外观基础，2D 生成先验则补偿 3D 初始化中缺失的视角和表情细节，形成互补闭环。

### 输入与预处理

ELITE 的输入为一段**单目人脸视频**（仅需 3 帧即可完成合成）。系统首先对输入视频进行离线 FLAME 网格跟踪，获得三项关键数据：

1. **标准空间 UV 纹理图** $\mathbf{M}_{\mathrm{tex}}$ 与**UV 几何图** $\mathbf{M}_{\mathrm{geo}}$，描述身份相关的静态几何与纹理信息；
2. **逐帧驱动信号** $\Theta$，包括表情编码、部位旋转（下颌、眼球、颈部）及全局头部旋转。

### 四大核心模块

pipeline 由四个模块串联构成，形成“初始化 → 真实帧适应 → 生成增强 → 生成式适应”的完整链路：

| 模块 | 功能 | 关键机制 |
|------|------|----------|
| **Mesh2Gaussian Prior Model (MGPM)** | 前馈初始化高斯化身 | 将 UV 图与驱动信号映射为 UV 对齐的 2D 高斯参数图 |
| **Stage 1：真实帧测试时适应** | 消除身份偏移、补充细节 | 仅用输入视频帧监督微调 MGPM |
| **单步扩散增强器** | 生成多视角/多表情监督图像 | 以退化 Avatar 渲染为强条件，一次去噪生成 |
| **Stage 2：生成式测试时适应** | 泛化至未见姿态与表情 | 将增强图像加入监督集再次微调 MGPM |

### 数据流与模块关系

Figure 2 对比了 ELITE 与现有范式的差异：过拟合方法（如 **FlashAvatar**、**SplattingAvatar**）从模板网格初始化 3D 高斯，仅用真实帧监督；3D 数据先验方法（如 **SynShot**）虽使用先验初始化，但监督来源仍仅限于真实帧；2D 生成先验方法（如 **CAP4D**）使用全去噪扩散生成图像监督，但从零开始优化且生成缓慢。ELITE 同时享受 3D 先验初始化与 2D 生成监督的双重优势，并以渲染引导的单步增强替代全去噪，实现 60 倍加速。

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of existing avatar synthesis approaches. (a) Overfitting methods [37, 51] optimize avatars from scratch, starting from 3D primitives anchored on a template mesh, and use only the input video frames as supervision. (b) 3D data prior methods [1, 52] use learned avatar initialization, but use only the input video frames as supervision. (c) 2D generative prior methods [40, 41] use diffusiongenerated (full denoising, i.e., slow) images as test-time supervision, but optimize avatars from scratch. (d) Our ELITE enjoys the benefits of (b) and (c), i.e., we use learned avatar initialization and generated images as test-time supervision. We also generate images using a single-step diffusio...*

具体而言，完整流程如下：

1. **MGPM 前馈初始化**（Figure 3）：预训练的 U-Net $\mathcal{F}_{\phi}$ 接收拼接的 UV 纹理/几何图与驱动嵌入，前馈预测 UV 对齐的 2D 高斯参数图 $\mathbf{M}_{\mathrm{gs}|\Theta}$（含位置偏移、颜色、旋转、尺度、不透明度）。该前馈路径提供快速、稳定的身份保持初始化，但仅靠前馈无法达到高保真（Figure 4）。

2. **Stage 1 真实帧适应**（Figure 5）：从输入视频采样 $N_{\mathrm{real}}$ 帧（默认 3 帧），通过渲染损失微调 MGPM，消除前馈初始化的身份偏移并补充细节。此阶段仅使用真实帧，确保鲁棒的对齐基础。

3. **单步扩散增强**（Figure 6a）：以退化 Avatar 渲染 $\mathbf{I}_{\mathrm{gen}}$ 和干净参考帧 $\mathbf{I}_{\mathrm{real}}$ 为输入，通过一次扩散去噪生成高质量、身份保持的图像 $\mathbf{I}_{\mathrm{gen}}^\star = \mathcal{D}_\xi([\mathbf{I}_{\mathrm{gen}}, \mathbf{I}_{\mathrm{real}}])$。关键创新在于：3D 渲染（即使质量下降）已包含丰富的结构与外观信息，作为扩散模型的强初始化，将生成任务从“纯噪声去噪”转化为“渲染增强”，从而大幅降低采样步数、抑制身份漂移。

4. **Stage 2 生成式适应**（Figure 6b）：将单步增强生成的多视角/多表情图像加入监督集，再次微调 MGPM，使化身能够泛化到训练集未曾见过的野生姿态与表情。

### 关键设计决策

- **两阶段适应性**：Stage 1 仅用真实帧保证身份对齐的鲁棒性，Stage 2 引入生成图像提供泛化所需的视角与表情多样性。消融实验（Figure 10c）证明，完整流程逐步提升质量：初始化提供基础结构，真实帧对齐身份，生成图像补充细节和泛化性。
- **渲染引导的单步增强**：与 CAP4D 的全去噪扩散（每张 18 秒）相比，ELITE 的单步增强仅需 0.3 秒/张，速度提升 60 倍，且身份一致性从 CSIM=0.4144 大幅提升至 0.9793（Figure 9）。
- **对监督帧数不敏感**：即使仅用 1 帧输入，ELITE 仍能生成稳定的交叉重演结果，这得益于 3D 先验的强初始化与生成式适应提供的合成多视角监督。

整个 pipeline 从输入视频到最终可动画化身的总合成时间约 **20 分钟**，远快于 CAP4D 的 400 分钟，实现了高效、高保真、身份一致的头像合成。

### 补充图表

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/001_Figure_1.jpg]]
*Figure 1: ELITE synthesizes an animatable photorealistic Gaussian head avatar from a casual monocular video. To compensate for missing views and expressions from the input video, ELITE leverages two complementary priors: (1) 3D data prior for feed-forward Gaussian initialization, and (2) 2D generative prior for augmenting unseen views and expressions for test-time adaptation. Compared to existing methods [37, 41] that utilize no priors or only a 2D generative prior, ELITE achieves superior generalization across unseen views and expressions in the wild. Please refer to the supplementary video for dynamic avatar animation results*



### 3.1 Mesh2Gaussian 先验模型 (MGPM)

ELITE 的核心创新之一是构建了一个前馈式的 **Mesh2Gaussian Prior Model (MGPM)**，它作为 3D 数据先验，为测试时适应性提供快速、稳定的身份保持初始化。

**输入与输出**：MGPM 接收标准空间下的 FLAME 网格 UV 纹理图与几何图的拼接张量 $[\mathbf{M}_{\mathrm{tex}}, \mathbf{M}_{\mathrm{geo}}] \in \mathbb{R}^{H \times W \times (3+3)}$，以及驱动信号 $\Theta$（包含表情编码、部位旋转、全局旋转等）。模型通过 U-Net 架构 $\mathcal{F}_{\phi}$ 将这些输入翻译为 UV 对齐的 2D 高斯参数图：

$$\mathbf{M}_{\mathrm{gs} | \Theta} = \mathcal{F}_{\phi}([\mathbf{M}_{\mathrm{tex}}, \mathbf{M}_{\mathrm{geo}}], \Theta)$$

输出的 2D 高斯参数图包含每个 UV 位置对应的高斯基元属性：位置偏移、颜色、旋转、尺度与不透明度。这种 UV 对齐的结构化设计使得高斯化身能够直接继承 FLAME 网格的拓扑结构，从而在动画驱动时保持几何一致性。

**训练损失**：MGPM 在多视角人脸捕捉数据集上进行监督训练，损失函数由四项组成：

$$\mathcal{L}_{\mathrm{MGPM}} = \mathcal{L}_{\ell 1} + \lambda_{\mathrm{lpips}} \mathcal{L}_{\mathrm{LPIPS}} + \lambda_{\mathrm{d}} \mathcal{L}_{\mathrm{depth}} + \lambda_{\mathrm{n}} \mathcal{L}_{\mathrm{normal}}$$

其中 $\mathcal{L}_{\ell 1}$ 为光度 L1 损失，$\mathcal{L}_{\mathrm{LPIPS}}$ 为感知损失，$\mathcal{L}_{\mathrm{depth}}$ 为深度畸变正则项，$\mathcal{L}_{\mathrm{normal}}$ 为法线一致性正则项。后两项正则化对于约束 3D 高斯在不可见区域的几何合理性至关重要。

### 3.2 测试时适应性两阶段微调

纯前馈初始化虽然能提供视觉上合理的初始化身，但无法达到高保真度（见 Figure 4）。因此 ELITE 引入测试时适应性微调，本质上是利用观测到的测试视频帧对 MGPM 进行微调。为兼顾计算效率，默认仅采样 $N_{\mathrm{real}} = 3$ 帧真实视频帧作为监督。

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/003_Figure_4.jpg]]
*Figure 4: Why need test-time avatar adaptation? (a) Our learned Gaussian initialization provides a visually reasonable initial, but synthesizing a high-fidelity avatar from only a feed-forward path is challenging at test time. (b) After the test-time adaptation of the avatar prior model, we obtain a high-fidelity, authentic avatar*

**Stage 1: 真实帧适应性微调**：仅使用输入视频帧的渲染损失微调 MGPM，消除前馈初始化的身份偏移并补充细节。此阶段确保化身与输入视频的身份严格对齐。

**Stage 2: 生成式适应性微调**：引入单步扩散增强器生成的合成图像作为额外监督，使化身能够泛化到输入视频中未出现的新颖姿态与表情。

### 3.3 单步扩散增强器

传统 2D 生成先验方法（如 CAP4D）从纯噪声全去噪生成图像，速度慢且易产生身份混淆。ELITE 的关键洞察在于：**退化的 3D 化身渲染已包含丰富的结构与外观信息，可以作为扩散模型的强条件输入**，从而将生成任务从“全去噪”转化为“渲染增强”。

单步扩散增强器 $\mathcal{D}_{\xi}$ 以退化化身渲染 $\mathbf{I}_{\mathrm{gen}}$ 和干净参考帧 $\mathbf{I}_{\mathrm{real}}$ 作为输入，仅需一次去噪即可生成高质量、身份保持的图像：

$$\mathbf{I}_{\mathrm{gen}}^{\star} = \mathcal{D}_{\xi}([\mathbf{I}_{\mathrm{gen}}, \mathbf{I}_{\mathrm{real}}])$$

该增强器通过微调单步图像翻译扩散模型 SD-Turbo 训练得到，训练数据为精心构建的三元组（退化化身渲染、干净参考图像、干净真值图像）。由于渲染提供了强几何与外观先验，扩散过程仅需补偿缺失的细节，从而大幅降低采样步数（从多步降至单步），并有效抑制身份漂移。

### 3.4 模块协同机制

ELITE 的完整流程体现了 3D 数据先验与 2D 生成先验的系统性互补：

1. **MGPM 前馈初始化**为 2D 生成提供了可靠的几何与外观基础，使扩散增强器能够以渲染为锚点进行条件生成，而非从噪声出发；
2. **单步扩散增强**补偿了 3D 初始化中缺失的视角和表情细节，生成的多视角/多表情图像反过来监督 Stage 2 的微调；
3. **两阶段适应性**解耦了身份对齐（Stage 1）与泛化增强（Stage 2），避免直接混合真实帧与生成图像监督可能导致的优化冲突。

### 补充图表

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/004_Figure_3.jpg]]
*Figure 3: Training Mesh2Gaussian Prior Model (MGPM). We train a 3D avatar prior model, MGPM, that takes mesh UV maps and 3D face driving signals, e.g., expression codes, poses (jaw, eyes, neck, head), as inputs and outputs a Gaussian avatar, structured in the form of UV-aligned 2D Gaussian primitives. We supervise the MGPM training using images from the face capture dataset [14] that spans diverse identities across different expressions and viewpoints*

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/006_Figure_6.jpg]]
*Figure 6: Single-step diffusion enhancer & Test-time “generative” adaptation. (a) We design a single-step diffusion enhancer that takes a degraded avatar rendering and a clean reference image as inputs, and efficiently generates a detail-enhanced and identity-preserving avatar rendering, within 0.3 seconds. (b) Using the generated images as test-time supervision, we conduct the stage 2 test-time avatar adaptation. After stage 2 adaptation, we obtain a final identity-specific avatar that generalizes across diverse poses, expressions, and viewpoints*

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/005_Figure_5.jpg]]
*Figure 5: Stage 1: Test-time adaptation w/ real images. Given input video frames and offline-tracked head mesh UV maps, we obtain 2D Gaussian UV maps by Mesh2Gaussian Prior Model’s (MGPM) feed-forward avatar initialization. We fine-tune MGPM by minimizing the rendering loss between the animated Gaussian avatar images and the sampled image frames within the input video*



## 实验与关键发现

### 核心实验设计

ELITE 的评估围绕一个核心问题展开：**3D 数据先验与 2D 生成先验的协同能否在单目视频输入下，同时实现高效率、高保真度与强泛化能力？** 实验从自重演（self re-enactment）、交叉重演（cross re-enactment）、生成图像质量与速度、以及消融分析四个维度进行验证。

**数据集与基线选择：** 自重演任务在 INSTA 数据集上进行，对比方法覆盖三类范式：
- **过拟合基线**：**FlashAvatar** 与 **SplattingAvatar**——从 FLAME 模板网格初始化的 3D 高斯，仅用真实帧监督，无任何先验；
- **3D 数据先验基线**：**SynShot**——使用合成数据训练先验模型，测试时仅用真实帧微调；
- **2D 生成先验基线**：**CAP4D**——使用多视角扩散模型从纯噪声全去噪生成合成图像，从零开始优化 3D 高斯化身。

**评估指标：** PSNR、SSIM、LPIPS（重建质量）；CSIM（身份保持）；总合成时间（效率）。

---

### 主要结果

**Table 1** 汇总了自重演任务的定量对比。ELITE 在多项指标上达到最优：

| 方法 | PSNR ↑ | SSIM ↑ | LPIPS ↓ | CSIM ↑ | 合成时间 ↓ |
|------|--------|--------|---------|--------|------------|
| SplattingAvatar | 24.838 | **0.8831** | 0.0893 | — | — |
| CAP4D | — | — | — | 0.7064 | ~400 分钟 |
| **ELITE (Ours)** | **25.220** | 0.8771 | **0.0732** | **0.7396** | **~20 分钟** |

ELITE 以 **PSNR 25.220、LPIPS 0.0732** 取得最优重建质量，身份保持指标 **CSIM 0.7396** 显著超越纯 2D 生成先验方法 CAP4D（0.7064）。在效率维度，ELITE 仅需约 **20 分钟**完成整个测试时适应性过程，相比 CAP4D 的约 400 分钟实现了 **20 倍加速**。

**交叉重演泛化能力**（Figure 8）进一步揭示方法间的本质差异：纯 3D 先验方法（SynShot）在训练分布内的姿态下表现尚可，但对未见过的极端姿态和微表情（如单眼眨眼、视线偏转）泛化不足；纯 2D 生成先验方法（CAP4D）虽能生成多样视角，但存在严重的身份混淆（identity hallucination），如虹膜颜色错误、发型失真。ELITE 凭借 3D 先验提供的身份锚定与 2D 生成先验提供的视角-表情补偿，在交叉重演中同时保持了**几何真实性**与**外观泛化性**。

---

### 单步增强 vs. 全去噪生成：速度与身份保持的权衡

Figure 9 对比了 ELITE 的渲染引导单步增强与 CAP4D 的全去噪扩散生成。结果揭示了一个关键的因果机制：

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/018_Figure_9.jpg]]
*Figure 9: Comparison of ID preservation of generated images. CAP4D severely hallucinates IDs and slow (18 secs./image). Our rendering-guided single-step enhancement leads to significantly better ID preservation, with 60× faster image generation speed*

- **CAP4D** 从纯噪声出发进行全去噪生成，每张图像需 **18 秒**，且由于缺乏 3D 结构约束，生成图像的 CSIM 仅 **0.4144**，身份漂移严重；
- **ELITE 的单步增强器**以退化化身渲染为强条件输入，仅需一次去噪，每张图像生成仅 **0.3 秒**（**60 倍加速**），同时 CSIM 高达 **0.9793**。

这一对比验证了论文的核心洞察：**3D 渲染（即使质量下降）已蕴含丰富的结构与外观信息，作为扩散模型的强初始化，将生成任务从“从零创造”转化为“渲染增强”，从而大幅降低采样步数、抑制身份漂移并提升速度。**

---

### 消融实验：双先验协同的必要性

**Table S1 与 Figure S2** 提供了最关键的消融证据，系统拆解了 3D 数据先验与 2D 生成先验各自的贡献：

| 配置 | 自重演 PSNR | 自重演 LPIPS | 交叉重演几何 | 交叉重演外观 |
|------|------------|-------------|-------------|-------------|
| 仅 3D 数据先验（无生成式适应） | 较低 | 较高 | 可接受 | 模糊/缺乏细节 |
| 仅 2D 生成先验（无从零初始化） | 较低 | 较高 | 坍塌/失真 | 身份混淆 |
| **混合系统（ELITE 完整流程）** | **28.68** | **0.0585** | **逼真** | **身份一致** |

单独使用任一先验都会导致系统性失效：纯 3D 先验缺乏对未见视角与表情的监督，外观泛化不足；纯 2D 生成先验缺乏可靠的几何初始化，导致几何坍塌与身份混淆。**二者的耦合是唯一能同时在自重演与交叉重演中取得高质量结果的方案。**

**模块贡献的阶段性分析**（Figure 10c）进一步表明：MGPM 前馈初始化提供了基本的结构框架；Stage 1 真实帧适应消除了身份偏移并补充细节；Stage 2 生成式适应则赋予化身对新颖姿态与表情的泛化能力。三个阶段呈递进关系，缺一不可。

**数据规模与监督帧数的影响**（Figure 10a, 10b）：
- 增加 MGPM 训练身份数量可单调提升测试时泛化质量，验证了 3D 先验对数据多样性的依赖；
- 使用更多真实视频帧监督可提高保真度，但线性增加合成时间，存在明确的质量-速度权衡。ELITE 默认使用 **仅 3 帧**即可取得强竞争力结果，且对帧数不敏感（Figure S3），即使仅用 1 帧也能生成稳定的交叉重演结果——这得益于 3D 先验的强初始化与生成式适应提供的合成多视角监督。

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/022_Figure_S.3.jpg]]
*Figure S.3: Effect of the number of real frames*

---

### 失败模式与局限性

尽管 ELITE 在整体性能上表现优异，论文明确指出了三类失败模式：

1. **异常光照敏感**：ELITE 缺乏显式的光照建模或基于物理的材质纹理建模，在极端光照（如强逆光、单侧强光）下可能产生伪影，渲染质量下降。这是 3D 数据先验训练域光照分布有限的直接后果。

2. **附件几何建模缺失**：眼镜等配件的几何结构完全被烘焙为纹理，法线图显示没有对应的 3D 结构。这意味着化身无法实现配件的拆卸或交互操作，限制了在 AR/VR 等场景中的应用潜力。

3. **建模范围与数据多样性受限**：头化身未覆盖全身或复杂服饰，仅建模头部及躯干上段；3D 先验训练集仅约 400 个身份，多样性仍有提升空间，可能影响对极端面部特征或少数族裔的泛化能力。

这些失败模式本质上指向同一瓶颈：**3D 数据先验的质量受限于训练数据的域覆盖范围**，而 ELITE 的 2D 生成先验虽能补偿视角与表情缺失，却无法弥补光照、几何拓扑等结构性先验的不足。

### 补充图表

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/009_Table_1.jpg]]
*Table 1: Self re-enactment comparison. We compare the visual quality of the avatars for INSTA identities [51]. ELITE (Ours) shows superior reconstruction quality and ID preservation*

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/020_Table_S.1.jpg]]
*Table S.1: Ablation on the 3D data prior and the 2D generative prior (Self Re-enactment). Our hybrid 3D data & 2D generative prior approach achieves the highest reconstruction performance on self re-enactment task, and achieves the most plausible appearance and geometry results on cross re-enactment (Fig. S2-right)*

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/017_Figure_10.jpg]]
*Figure 10: Ablation Study. (a) Scaling up the number of training identities for MGPM leads to better quality and generalization at test time. (b) Using more video frames for supervision improves quality but sacrifices the synthesis speed. (c) Our proposed modules, learned 3D avatar initialization & test-time generative adaptation, enable high-fidelity and generalizable avatar synthesis*

![[assets/figures/papers/paper_list_l958_https_arxiv_org_abs_2601_10200/figures/021_Figure_S.2.jpg]]
*Figure S.2: Ablation on the 3D data prior and the 2D generative prior. Self re-enactment (left) shows that methods without the 3D prior ((a),(b)) overfit and produce unrealistic geometry, while (c) and (d) preserve plausible structure. Cross re-enactment (right) highlights generalization differences: (a) fails in both geometry and appearance, (b) improves appearance but not geometry, (c) maintains geometry but lacks appearance generalization, and (d) (our proposed method) achieves both*



## 定位与知识库关联

### 1. 问题定位：3D先验与2D生成先验的割裂

单目视频驱动的可动画头部化身合成存在一条清晰的方法演化路径，ELITE的贡献在于首次系统性地耦合了此前相互独立的两种先验范式：

**过拟合基线**（**FlashAvatar**、**SplattingAvatar**）从FLAME模板网格初始化的3D高斯集出发，仅用输入视频帧进行逐身份优化。这类方法没有任何先验知识，完全依赖测试时的少量真实帧监督，因此在未见视角和表情上泛化能力极弱——输入视频未覆盖的姿态会导致几何坍塌和纹理模糊（见Figure 2a）。

**3D数据先验方法**（如**SynShot**）通过在合成多视角数据集上预训练先验模型来提供更好的初始化，但测试时监督仍仅限于真实视频帧。其核心瓶颈在于：合成训练数据的域分布有限（约400个身份），预训练先验无法覆盖测试身份的所有视角-表情组合，导致在wild场景下的泛化仍然不足（见Figure 2b）。

**2D生成先验方法**（以**CAP4D**为代表）利用多视角扩散模型从纯噪声生成合成图像来监督3D高斯的从零优化。这类方法虽然能提供多样化的监督信号，但存在三个致命缺陷：（1）全去噪生成极为缓慢（每张图像18秒）；（2）从纯噪声出发缺乏结构锚点，极易产生身份混淆（identity hallucination），CSIM仅0.4144；（3）从零开始优化3D高斯进一步放大了身份漂移风险（见Figure 2c）。

### 2. ELITE的谱系定位：互补耦合

ELITE的核心洞见是：**3D数据先验与2D生成先验具有天然的互补性**，而非替代关系。这一判断建立在以下因果链条上：

1. **3D渲染（即使质量退化）已包含丰富的结构与外观信息**，可以作为扩散模型的强条件输入，将生成任务从“纯噪声→图像”的全去噪转化为“退化渲染→高质量图像”的单步增强。这不仅将采样步数从多步压缩至一步（速度提升60倍），更重要的是以渲染中的身份结构为锚点，从根本上抑制了身份漂移（CSIM从0.4144跃升至0.9793，见Figure 9）。

2. **由合成数据训练的3D先验模型为2D生成提供可靠的几何与外观基础**，使得扩散增强器只需补偿细节和视角泛化，而非从零重建身份。这种分工使得整个系统对输入帧数极不敏感：即使仅用1帧真实图像，3D先验的强初始化加上生成式适应提供的合成多视角监督，仍能产生稳定的交叉重演结果（见Supple. Fig. S3）。

3. **两阶段测试时适应性设计**（Stage 1真实帧微调 + Stage 2生成图像增强）是耦合的关键机制：Stage 1消除前馈初始化的身份偏移并补充真实细节，Stage 2利用扩散增强器生成的未见视角/表情图像进行泛化增强。消融实验（Table S1, Fig. S2）证明，同时使用两种先验的混合系统在自重演（PSNR 28.68, LPIPS 0.0585）上显著优于单独使用任一先验的变体，且是唯一在交叉重演中同时实现逼真几何与外观泛化的方案。

### 3. 技术栈溯源

ELITE的技术组件可追溯至以下知识节点：

- **3D Gaussian Splatting (3DGS)** 提供可微渲染基础，ELITE将其组织为UV对齐的2D高斯（2DGS），使得高斯参数图可通过U-Net前馈预测。
- **FLAME参数化模型** 提供标准空间UV映射与驱动信号（表情编码、部位旋转等），是MGPM输入表示的基础。
- **SD-Turbo** 作为单步图像翻译扩散模型的骨干，ELITE在其上进行LoRA微调，将任务特化为“退化渲染→身份保持增强”的条件生成。
- **NerSemble-V2** 多视角面部捕捉数据集作为MGPM的训练数据源，提供约400个身份的多表情、多视角监督。

### 4. 适用边界与局限

ELITE的适用边界由其技术设计直接决定：

- **光照敏感性**：方法缺乏显式的光照建模或基于物理的材质纹理建模，在异常光照条件（如室外逆光、极端阴影）下会产生伪影。这是因为单步扩散增强器虽能补偿部分光照变化，但缺乏对场景光照的显式解耦。
- **附件几何建模缺失**：眼镜、耳机等配件的几何结构完全被烘焙为纹理，法线图显示没有对应的3D结构。这源于MGPM的训练数据中附件多样性不足，且UV对齐的2D高斯表示难以表达脱离面部表面的独立几何。
- **建模范围受限**：仅覆盖头部及躯干上段，未涉及全身或复杂服饰。这是当前3D数据先验训练集（仅头部捕捉数据）的直接约束。
- **训练身份多样性有限**：MGPM仅使用约400个身份训练，虽然消融实验（Figure 10a）表明增加训练身份数可提升泛化质量，但当前规模仍可能对极端面部特征或罕见表情的泛化构成瓶颈。

### 5. 开放问题

从ELITE的技术框架出发，以下方向值得进一步探索：

1. **光照先验的引入**：是否可以通过引入基于物理的渲染（PBR）材质建模或光照先验（如环境光照估计网络），将光照与反照率显式解耦，从而提升在室外、逆光等条件下的鲁棒性？

2. **附件几何的联合建模**：能否将3D数据先验扩展至人脸附件几何（眼镜、耳机、帽子）的联合建模，使化身支持附件的可拆卸或交互式编辑？这需要在UV表示之外引入额外的几何通道。

3. **数据多样性的高效扩展**：是否可以利用合成数据管道（如基于生成模型的无限身份采样）来进一步扩大MGPM的训练域，从而减少对测试时生成式适应的依赖，甚至实现纯前馈的高质量化身合成？

4. **框架的跨域推广**：该“3D先验初始化 + 2D生成增强”的耦合范式是否可以推广至全身化身或动态场景（如交互式VR），在保持实时性和身份一致性的前提下处理更复杂的几何与外观变化？



## 原文 PDF

![[paperPDFs/CVPR_2026/ELITE_Efficient_Gaussian_Head_Avatar_from_a_Monocular_Video_via_Learned_Initialization_and_Test_time_Generative_Adaptation.pdf]]
