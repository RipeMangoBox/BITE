---
title: NeoVerse Enhancing 4D World Model with in-the-wild Monocular Videos
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/NeoVerse_Enhancing_4D_World_Model_with_in_the_wild_Monocular_Videos.pdf
project_link: https://neoverse-4d.github.io
code_link: null
aliases:
- NE4WMWMV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过提出无姿态前馈式4DGS重建和在线退化模拟，使得训练流程可扩展到多样化的野生单目视频，从而提升泛化性和多功能性。
primary_logic: 将高效的前馈式4D重建与在线退化模式模拟相结合，使得视频生成模型能够从大规模野生单目视频中学习如何从退化渲染条件生成高质量、时空一致的视频，避免了传统方法的重计算预处理和有限数据问题。
claims:
- 静态重建性能：在VRNeRF基准上，PSNR达到20.73，超过AnySplat (18.02) 2.71
- 动态重建性能：在ADT基准上，PSNR达到32.56，显著优于4DGT (30.09) 和MonST3R (17.42)
- 新视图生成质量：VBench主观一致性得分88.43，显著高于TrajectoryCrafter (83.02)，保持精确相机控制
- 完整流程（重建+生成）在DyCheck上将PSNR从纯重建的11.56提升至14.59
---

# NeoVerse Enhancing 4D World Model with in-the-wild Monocular Videos

> [!tip] 核心洞察
> 将高效的前馈式4D重建与在线退化模式模拟相结合，使得视频生成模型能够从大规模野生单目视频中学习如何从退化渲染条件生成高质量、时空一致的视频，避免了传统方法的重计算预处理和有限数据问题。

| 字段      | 内容                                                                                                                     |
| ------- | ---------------------------------------------------------------------------------------------------------------------- |
| 中文题名    | NeoVerse：利用野生单目视频增强4D世界模型                                                                                              |
| 英文题名    | NeoVerse Enhancing 4D World Model with in-the-wild Monocular Videos                                                    |
| 会议/期刊   | CVPR 2026 (Highlight)                                                                                                  |
| Links | [paper](https://arxiv.org/abs/2601.00393) · [Project](https://neoverse-4d.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method  | NeoVerse                                                                                                               |
| Dataset | VRNeRF, Scannet++, ADT, DyCheck                                                                                        |

> [!tip] 效果简介
> - VRNeRF 上，PSNR↑ 20.73 vs AnySplat 18.02 (+2.71)；SSIM↑ 0.766 vs AnySplat 0.705 (+0.061)；LPIPS↓ 0.352 vs AnySplat 0.366 (-0.014)。
> - Scannet++ 上，PSNR↑ 25.34 vs AnySplat 22.79 (+2.55)；SSIM↑ 0.834 vs AnySplat 0.773 (+0.061)；LPIPS↓ 0.195 vs AnySplat 0.217 (-0.022)。
> - ADT 上，PSNR↑ 32.56 vs 4DGT 30.09 (+2.47)。

## 概要

### 问题与瓶颈

4D世界模型旨在从视频输入中重建动态三维场景并支持新视角生成，其核心瓶颈在于**数据可扩展性**与**训练可扩展性**的双重制约。现有方法要么依赖昂贵的多视图数据采集，要么需要繁重的离线预处理（如深度估计、已知相机姿态），难以有效利用互联网上大量存在的野生单目视频。这一瓶颈直接限制了模型的泛化能力与多功能性。

### 核心洞察

NeoVerse的核心洞察在于：将**高效的前馈式4D重建**与**在线退化模式模拟**相结合，使视频生成模型能够从大规模野生单目视频中学习如何从退化渲染条件生成高质量、时空一致的视频。具体而言，该方法通过无姿态前馈式4D高斯泼溅（4DGS）快速重建粗糙的4D场景表示，并将其在新视角下的退化渲染作为条件信号输入生成模型；训练时则直接从野生视频在线模拟遮挡、飞点像素和几何失真等退化模式，避免了对离线预处理和精确多视图数据的依赖。

### 方法定位

NeoVerse在方法谱系中处于**重建引导的视频生成**范式，其关键设计包括：

- **无姿态前馈式4DGS重建**：基于VGGT骨干网络，以稀疏关键帧为输入，直接预测4D高斯场的全部参数（位置、不透明度、旋转、尺度、球谐系数、寿命及双向速度/角速度），无需已知相机姿态。
- **双向运动建模**：区别于4DGT（Xu et al., arXiv 2025）的单向时间建模，NeoVerse同时预测前向与后向速度场，支持任意时间点的插值渲染。
- **在线单目退化模拟**：通过高斯剔除（Gaussian Culling）和平均几何滤波（Average Geometry Filter）等策略，在训练过程中实时生成退化渲染条件，使生成模型学会抑制伪影并补全缺失区域。
- **退化条件编码生成**：将退化渲染的RGB、深度、掩码及Plücker嵌入作为控制分支输入生成模型（基于Wan-T2V），以校正流（Rectified Flow）目标进行训练。

### 主要结果

在静态重建基准VRNeRF上，NeoVerse的PSNR达到**20.73**，较AnySplat的18.02提升2.71 dB（Table 1）。在动态重建基准ADT上，PSNR达到**32.56**，显著优于4DGT（30.09）和MonST3R（17.42）（Table 2）。在新视图生成任务中，VBench主观一致性得分**88.43**，超过TrajectoryCrafter（83.02），同时推理时间仅需20秒（11个关键帧），远低于TrajectoryCrafter的146秒（Table 3）。完整的重建-生成流程在DyCheck上将PSNR从纯重建的11.56提升至**14.59**（Table 4），验证了退化条件生成策略的有效性。

### 局限性

NeoVerse对缺乏3D结构的2D内容（如卡通）处理能力有限，可能生成错误的3D轮廓；与多数视频扩散模型类似，偶尔难以生成清晰文字；其高斯插值依赖线性运动假设，在高度非线性运动场景下可能偏离实际（见Figure S1及附录讨论）。

4D世界建模旨在从视觉输入中重建动态3D场景并支持自由视点渲染，是计算机视觉与图形学交叉领域的核心挑战。近年来，以3D高斯泼溅（3DGS）和视频扩散模型为代表的生成式方法取得了显著进展，但其实际部署仍受制于两个根本性瓶颈。

**数据可扩展性瓶颈。** 现有4D重建与生成方法大多依赖昂贵的多视图数据或需要已知相机姿态的离线预处理流程。例如，基于NeRF或3DGS的方法通常需要从多视角图像或RGB-D序列中离线重建场景表示，再以此作为生成模型的条件输入。这类管线不仅计算开销大，更关键的是难以利用互联网上巨量的野生单目视频——这些视频天然包含丰富的动态场景先验，却因缺乏姿态标注和多视图约束而被现有方法排除在外。

**训练可扩展性瓶颈。** 即便部分方法尝试利用单目视频，其训练流程仍依赖繁重的离线预处理步骤（如深度估计、光流计算、逐场景优化等），导致训练无法规模化。同时，从单目视频重建的4D表示在渲染到新视点时不可避免地产生遮挡空洞、飞点像素、几何失真等退化伪影，而现有生成模型缺乏系统性的机制来学习从这些退化条件中恢复高质量、时空一致的视频。

上述瓶颈共同指向一个核心问题：**如何构建一个能够从大规模野生单目视频中高效学习的4D世界模型，使其既具备可扩展的训练范式，又能在退化渲染条件下生成高质量的新视点视频？**

NeoVerse正是针对这一问题提出。其核心洞察在于：将高效的前馈式4D重建与在线退化模式模拟相结合，使得视频生成模型能够直接从野生单目视频中学习“退化→高质量”的映射，从而绕开传统方法的重计算预处理和有限数据约束。这一设计使得模型能够从约1M视频片段的训练数据中学习丰富的动态场景先验，在静态重建、动态重建和新视图生成三个任务上均取得显著提升。

## 核心方法与创新机理

NeoVerse 的核心创新在于通过**无姿态前馈式4DGS重建**与**在线退化模拟**两项关键设计，将4D世界模型的训练数据来源从昂贵的多视图采集彻底转向大规模野生单目视频，从而突破了现有方法在数据可扩展性和训练可扩展性上的双重瓶颈。

### 1. 无姿态前馈式4DGS重建

传统方法在从单目视频重建4D表示时，通常依赖离线优化（如 COLMAP 估计相机姿态）或需要已知姿态的多视图数据作为输入，计算开销大且难以规模化。NeoVerse 提出了一种**无需相机姿态的前馈式4DGS重建模型**，以 VGGT 为骨干网络，直接从稀疏关键帧一次性推理出完整的4D高斯场，避免了繁重的离线预处理。

与同样面向动态场景的 **4DGT**（Xu et al., arXiv 2025）相比，NeoVerse 在运动建模上做出了关键改进：引入**双向运动编码分支**，同时预测前向速度 $\boldsymbol{v}_i^+$ 和后向速度 $\boldsymbol{v}_i^-$，以及对应的角速度 $\boldsymbol{\omega}_i^+$、$\boldsymbol{\omega}_i^-$。这一设计使得高斯场可以在任意查询时间点 $t_q$ 进行插值——当 $t_q \geq t$ 时使用前向运动参数，当 $t_q < t$ 时使用后向运动参数（见 Eq. 3-4）。相比之下，4DGT 仅采用单向时间建模，无法支持从稀疏关键帧到密集帧的高效插值。消融实验证实，去除双向运动建模后，DyCheck 上的 PSNR 从 11.56 下降至 11.27（Table 4），验证了该设计的贡献。

### 2. 在线单目退化模拟

传统视频生成方法在构建训练对时，通常需要离线运行深度估计、光流计算等预处理步骤来生成条件信号，流程繁琐且难以利用海量野生视频。NeoVerse 的核心洞察在于：**将训练对生成过程完全在线化**，在训练时对原始单目视频进行“退化模拟”，以退化渲染作为生成模型的条件输入，原始视频本身作为生成目标。

具体而言，NeoVerse 设计了三类退化模式（Figure 3）：
- **遮挡模拟**：通过随机丢弃部分高斯原语来模拟新视角下的遮挡区域；
- **飞点像素模拟**：引入孤立的高斯噪声点来模拟重建中的离群渲染；
- **几何滤波**：使用平均几何滤波器（Average Geometry Filter）对深度图进行平滑，模拟重建几何不精确导致的失真。

这些退化渲染与 RGB 图像、深度图、二值化掩码以及 Plücker 嵌入一同输入生成模型的控分支。由于退化模拟完全在线执行，训练流程可以直接消费大规模野生单目视频，无需任何离线标注或预处理。Figure 7 的定性结果表明，经过退化模拟训练的模型能够学会抑制渲染伪影，并在遮挡或失真区域“幻觉”出逼真的细节。

### 3. 创新点的协同效应

上述两项创新并非孤立存在，而是形成了正向协同：双向运动建模使得从稀疏关键帧插值到任意时间点成为可能，从而为在线退化模拟提供了灵活的渲染时间点选择；在线退化模拟则使得生成模型能够从野生视频中学习到“从退化到高质量”的映射，反过来降低了对重建精度的苛刻要求。这一协同最终体现为完整流程（重建 + 生成）在 DyCheck 上将 PSNR 从纯重建的 11.56 提升至 14.59（Table 4），提升幅度达 3.03 dB。

### 4. 与 baseline 的 slot 级对比

| 设计维度 | 现有方法 | NeoVerse |
|---------|---------|----------|
| 重建方式 | 离线优化或需已知姿态的多视图数据 | 无姿态前馈式4DGS，从稀疏关键帧在线重建 |
| 运动建模 | 4DGT 采用单向时间建模 | 双向运动建模，区分前向/后向速度，支持插值 |
| 训练数据生成 | 离线预处理（深度估计等）或静态多视图数据 | 在线单目退化模拟，直接从野生视频创建训练对 |

这些 slot 级别的改变共同构成了 NeoVerse 的方法论突破：将4D世界模型的训练范式从“重计算、小数据”转向“轻计算、大数据”，从而在静态重建（VRNeRF PSNR 20.73 vs AnySplat 18.02）、动态重建（ADT PSNR 32.56 vs 4DGT 30.09）和新视图生成（VBench 主观一致性 88.43 vs TrajectoryCrafter 83.02）三个任务上均取得显著提升。

NeoVerse 的整体流程由两大核心阶段构成：**无姿态前馈式 4DGS 重建** 与 **退化渲染条件引导的视频生成**。系统输入为一段野生单目视频，输出为在新视角下时空一致的高质量视频。

### 重建阶段：前馈式 4DGS 与双向运动建模

重建阶段旨在从稀疏关键帧中高效恢复场景的 4D 高斯场表示。该阶段以 **VGGT** 为主干网络，在此基础上进行“高斯化”改造，并引入了**双向运动编码分支**，使得模型能够同时预测每个高斯原语的前向速度 $v^+$ 与后向速度 $v^-$，以及对应的角速度 $\omega^+$ 与 $\omega^-$。这一双向设计区别于 4DGT 的单向时间建模，为后续的帧间插值提供了运动基础。

具体而言，给定一段 $N$ 帧的视频，系统仅选取 $K$ 个关键帧作为重建输入（$K \ll N$），通过前馈网络直接输出 4D 高斯场参数：

$$\{ (\mu_i, \alpha_i, r_i, s_i, sh_i, \tau_i, v_i^+, v_i^-, \omega_i^+, \omega_i^-) \}_{i=1}^{T \times H \times W}$$

每个高斯原语包含位置、不透明度、旋转、尺度、球谐系数、寿命，以及双向线速度与角速度。重建模型的多任务损失函数为：

$$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{\mathrm{rgb}} + \lambda_{1} \mathcal{L}_{\mathrm{camera}} + \lambda_{2} \mathcal{L}_{\mathrm{depth}} + \lambda_{3} \mathcal{L}_{\mathrm{motion}} + \lambda_{4} \mathcal{L}_{\mathrm{regular}}$$

该损失联合优化光度一致性、相机姿态、深度、运动以及正则化项，确保重建的几何与运动准确性。

### 插值与退化渲染

得益于双向运动建模，系统可将关键帧处的 4D 高斯场插值到任意非关键帧时刻 $t_q$。位置插值依据查询时间与关键帧时间的关系，分别使用前向或后向速度进行线性外推：

$$\pmb{\mu}_i(t_q) = \begin{cases} \pmb{\mu}_i + \pmb{v}_i^+ |t_q - t|, & t_q \geq t \\ \pmb{\mu}_i + \pmb{v}_i^- |t_q - t|, & t_q < t \end{cases}$$

旋转则通过轴角角速度与四元数转换进行插值：

$$r_i(t_q) = \begin{cases} r_i \cdot \phi(\omega_i^+ |t_q - t|), & t_q \geq t \\ r_i \cdot \phi(\omega_i^- |t_q - t|), & t_q < t \end{cases}$$

同时，不透明度按归一化时间距离与寿命参数 $\tau_i$ 进行指数衰减，实现高斯原语的自然消隐。

将插值后的 4D 高斯场在新视角下渲染，得到的渲染结果并非最终输出，而是作为**退化条件**输入到生成阶段。这些渲染结果由于稀疏关键帧重建和线性运动假设的局限性，通常存在遮挡、飞点像素、几何失真等退化模式。

### 在线单目退化模拟

在训练阶段，系统通过**在线单目退化模拟**直接从原始视频中构建训练对，避免了传统方法所需的离线深度估计等繁重预处理。具体而言，系统模拟三种典型退化模式：遮挡（通过高斯剔除实现）、飞点像素（通过平均几何滤波实现）以及更广泛的几何失真。这些退化后的渲染作为条件输入，原始视频帧作为目标，使生成模型学会从退化条件中恢复高质量画面。

### 生成阶段：退化渲染条件引导

生成阶段以 **Wan-T2V** 视频扩散模型为骨干，在其基础上添加控分支。控分支的输入为多模态条件，包括退化渲染的 RGB 图像、深度图、从不透明度图二值化得到的掩码（指示空白区域），以及原始轨迹的 Plücker 嵌入。生成模型的训练目标为校正流损失：

$$\mathcal{L}_{\mathrm{gen}} = \mathbb{E}_{x_{1}, x_{0}, c_{\mathrm{render}}, c_{\mathrm{text}}, t} \lVert f_{\theta}(x_{t}, t, c_{\mathrm{render}}, c_{\mathrm{text}}) - v_{t} \rVert_{2}^{2}$$

训练时，生成模型的骨干网络被冻结，仅训练控分支，以确保预训练的视频生成先验不被破坏。

### 训练流程

NeoVerse 的训练分为两个阶段：
1. **重建模型训练**：使用多源数据集（包括静态与动态场景）训练前馈式 4DGS 重建模型，使其具备从稀疏关键帧恢复 4D 高斯场的能力。
2. **生成模型训练**：在重建模型的基础上，进行在线重建与退化模拟，将退化渲染作为条件输入生成模型，原始视频作为目标，训练控分支。

推理时，系统对输入视频进行稀疏关键帧重建、插值、新视角退化渲染，最终通过生成模型输出时空一致的高质量新视角视频。整个流程的总推理时间约 20 秒（11 个关键帧），显著快于 TrajectoryCrafter 的 146 秒（Table 3）。

### 3.1 无姿态前馈式4DGS重建

NeoVerse的重建模块以**VGGT**为基础骨干，将其改造为前馈式4D高斯泼溅（4DGS）模型。该模块从稀疏关键帧直接预测4D高斯场，无需离线相机姿态估计，从而消除了传统方法中繁重的预处理瓶颈。

**双向运动编码分支**是该模块的核心创新。与4DGT（Xu et al., arXiv 2025）的单向时间建模不同，NeoVerse显式区分前向速度（$t \to t+1$）和后向速度（$t \to t-1$），通过交叉注意力机制计算双向运动特征：

**前向运动特征：**
$$\{ \boldsymbol{F}_t^{\mathrm{fwd}} \}_{t=1}^{T-1} = \mathrm{CrossAttn}(\boldsymbol{q}=\{ \boldsymbol{F}_t \}_{t=1}^{T-1}; \boldsymbol{k},\boldsymbol{v}=\{ \boldsymbol{F}_t \}_{t=2}^{T})$$

**后向运动特征：**
$$\{ \boldsymbol{F}_t^{\mathrm{bwd}} \}_{t=2}^{T} = \mathrm{CrossAttn}(\boldsymbol{q}=\{ \boldsymbol{F}_t \}_{t=2}^{T}; \boldsymbol{k},\boldsymbol{v}=\{ \boldsymbol{F}_t \}_{t=1}^{T-1})$$

其中 $\boldsymbol{F}_t$ 为第 $t$ 帧的特征表示，交叉注意力以当前帧特征作为查询，相邻帧特征作为键和值，分别捕获前向和后向的运动信息。

每个4D高斯由以下参数完整描述：
$$\{ (\mu_i, \alpha_i, r_i, s_i, sh_i, \tau_i, v_i^+, v_i^-, \omega_i^+, \omega_i^-) \}_{i=1}^{T \times H \times W}$$

其中 $\mu_i$ 为3D中心位置，$\alpha_i$ 为不透明度，$r_i$ 为旋转四元数，$s_i$ 为尺度，$sh_i$ 为球谐系数，$\tau_i$ 为寿命参数，$v_i^+ / v_i^-$ 分别为前向/后向线速度，$\omega_i^+ / \omega_i^-$ 分别为前向/后向角速度（轴角表示）。双向速度的设计使得高斯场可以在时间轴上进行前向和后向插值，支持非关键帧时刻的渲染。

### 3.2 稀疏关键帧插值与退化模拟

给定包含 $N$ 帧的长视频，重建模块仅使用 $K$ 个关键帧作为输入（$K \ll N$），但需要在所有 $N$ 帧上进行渲染以生成训练对。双向运动建模使得高斯场可以插值到非关键帧的查询时间 $t_q$：

**位置插值：**
$$\pmb{\mu}_i(t_q) = \begin{cases} \pmb{\mu}_i + \pmb{v}_i^+ |t_q - t|, & t_q \geq t, \\ \pmb{\mu}_i + \pmb{v}_i^- |t_q - t|, & t_q < t \end{cases}$$

**旋转插值：**
$$r_i(t_q) = \begin{cases} r_i \cdot \phi(\omega_i^+ |t_q - t|), & t_q \geq t, \\ r_i \cdot \phi(\omega_i^- |t_q - t|), & t_q < t \end{cases}$$

其中 $\phi(\cdot)$ 将轴角角速度转换为四元数旋转变换。不透明度则通过寿命参数 $\tau_i$ 进行衰减：

$$\pmb{\alpha}_i(t_q) = \pmb{\alpha}_i \exp(-\gamma \cdot d(t_q, t)^{\frac{1}{1-\tau_i}})$$

$d(t_q, t)$ 为归一化时间距离，$\gamma$ 为衰减系数。该衰减函数使高斯在远离其所属关键帧时自然淡出，保证时间过渡的平滑性。

**在线单目退化模拟**是训练可扩展性的关键。由于从稀疏关键帧重建的4DGS在新视角下渲染时会产生遮挡空洞、飞点像素和几何失真等退化伪影，NeoVerse直接在原始单目视频上模拟这些退化模式，无需离线预处理。具体策略包括：（1）**高斯剔除（Gaussian Culling）**模拟遮挡导致的缺失区域；（2）**平均几何滤波（Average Geometry Filter）**引入飞点像素和失真。这些退化渲染与原始视频帧配对，构成生成模型的训练数据。

### 3.3 损失函数

重建模型的训练采用多任务损失：

$$\mathcal{L}_{\mathrm{recon}} = \mathcal{L}_{\mathrm{rgb}} + \lambda_{1} \mathcal{L}_{\mathrm{camera}} + \lambda_{2} \mathcal{L}_{\mathrm{depth}} + \lambda_{3} \mathcal{L}_{\mathrm{motion}} + \lambda_{4} \mathcal{L}_{\mathrm{regular}}$$

其中 $\mathcal{L}_{\mathrm{rgb}}$ 为光度损失，$\mathcal{L}_{\mathrm{camera}}$ 为相机姿态损失，$\mathcal{L}_{\mathrm{depth}}$ 为深度损失，$\mathcal{L}_{\mathrm{motion}}$ 为运动损失，$\mathcal{L}_{\mathrm{regular}}$ 为正则化项（包含不透明度正则化，防止模型学习输出透明基元以匹配预定义背景色的捷径）。

生成模型基于**Wan-T2V**视频扩散模型，采用校正流（Rectified Flow）损失进行训练：

$$\mathcal{L}_{\mathrm{gen}} = \mathbb{E}_{x_{1}, x_{0}, c_{\mathrm{render}}, c_{\mathrm{text}}, t} \lVert f_{\theta}(x_{t}, t, c_{\mathrm{render}}, c_{\mathrm{text}}) - v_{t} \rVert_{2}^{2}$$

其中 $x_1$ 为目标视频，$x_0$ 为噪声，$c_{\mathrm{render}}$ 为退化渲染条件（包含RGB、深度图、掩码和Plücker嵌入），$c_{\mathrm{text}}$ 为文本条件，$v_t$ 为校正流速度场。训练时仅训练新增的控制分支，冻结生成模型主干。

## 实验与关键发现

### 核心性能验证

#### 静态场景重建

NeoVerse 在静态场景重建上展现出显著优势，即使不依赖真实相机姿态（测试时仅进行姿态对齐），其性能仍大幅超越现有前馈式方法。在 VRNeRF 基准上，NeoVerse 取得 **PSNR 20.73**，比 **AnySplat** 的 18.02 高出 2.71 dB（Table 1）；在 Scannet++ 上同样以 **PSNR 25.34** 领先 AnySplat 2.55 dB。SSIM 和 LPIPS 指标在两个基准上均一致优于 **NoPoSplat**（Ye et al., ICLR 2024）、**Flare**（Zhang et al., CVPR 2025）和 AnySplat，验证了无姿态前馈式 4DGS 重建的有效性。

![[assets/figures/papers/NeoVerse_Enhancing_4D_World_Model_with_in-the-wild_Monocular_Videos_full_rerun_20260609/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with other static reconstruction models*

定性对比（Figure 5）进一步揭示，现有方法因姿态预测不准确会产生不一致的渲染边缘（红色边界标注），而 NeoVerse 的重建结果在几何一致性和细节保真度上明显更优。

![[assets/figures/papers/NeoVerse_Enhancing_4D_World_Model_with_in-the-wild_Monocular_Videos_full_rerun_20260609/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative comparison with state-of-the-art methods in static scenes. Red boundaries indicate inconsistent renderings due to inaccurate pose prediction. Yellow boxes indicate artifacts*

#### 动态场景重建

在动态场景上，NeoVerse 同样表现出色。在 ADT 基准上，NeoVerse 取得 **PSNR 32.56**，显著优于需要已知姿态的 **4DGT**（30.09, Xu et al., arXiv 2025）和 **MonST3R**（17.42, Zhang et al., arXiv 2024），SSIM 达到 0.927，LPIPS 低至 0.120（Table 2）。在更具挑战性的 DyCheck 基准上，NeoVerse 以 **PSNR 11.56** 超过 MonST3R 2.24 dB。值得注意的是，4DGT 需要真实相机姿态作为输入（Table 2 中以 † 标注），而 NeoVerse 完全无需姿态信息，在此约束下仍取得领先，凸显了双向运动建模对动态场景理解的增益。

![[assets/figures/papers/NeoVerse_Enhancing_4D_World_Model_with_in-the-wild_Monocular_Videos_full_rerun_20260609/figures/004_Table_2.jpg]]
*Table 2: Quantitative comparison with other dynamic reconstruction models. †: indicate the method takes camera poses as input*

定性结果（Figure 6）表明，NeoVerse 预测中的黑色区域并非错误，而是由输入帧的部分观测导致——这反而说明模型对可见区域的几何重建是可靠的。

![[assets/figures/papers/NeoVerse_Enhancing_4D_World_Model_with_in-the-wild_Monocular_Videos_full_rerun_20260609/figures/012_Figure_6.jpg]]
*Figure 6: Qualitative comparison with state-of-the-art methods in dynamic scenes. Yellow boxes indicate artifacts. Note that the black regions in our prediction are not error but mainly caused by partial observations of input frames*

#### 新视图生成质量

NeoVerse 在新视图视频生成任务上实现了质量与效率的双重突破。在 VBench 基准的 400 个测试案例（100 个未见野生视频 × 4 种相机轨迹）上，NeoVerse 使用 11 个关键帧即取得 **主体一致性 88.43**，比 **TrajectoryCrafter**（YU et al., ICCV 2025）的 83.02 高出 5.41；**背景一致性 92.27**，领先 3.69（Table 3）。在美学质量（44.55 vs. **ReCamMaster** 44.29）和成像质量（59.75 vs. ReCamMaster 58.87）上也保持优势。

更关键的是推理效率：NeoVerse 总耗时仅 **20 秒**（A800 GPU, 336×560 分辨率），而 TrajectoryCrafter 需要 146 秒，加速约 7.3 倍。这得益于前馈式重建避免了昂贵的逐场景优化，以及稀疏关键帧策略大幅降低了渲染计算量。Figure 4 的定性对比显示，在大相机运动（“左摇”、“右移”）下，NeoVerse 在保持精确相机控制的同时生成质量更高，黄色框标注的伪影明显少于对比方法。

### 消融实验

Table 4 在 DyCheck 数据集上的消融实验揭示了各模块的因果贡献：

![[assets/figures/papers/NeoVerse_Enhancing_4D_World_Model_with_in-the-wild_Monocular_Videos_full_rerun_20260609/figures/008_Table_4.jpg]]
*Table 4: Ablation experiments on DyCheck. “w/. Generation” indicates our full pipeline, which gains significant performance improvements over the pure reconstruction part*

- **双向运动建模**：去除后 PSNR 从 11.56 降至 11.27，验证了区分前向/后向速度对插值精度的必要性。
- **不透明度正则化**：去除后 PSNR 骤降至 10.86，证实该正则项有效防止模型学习“输出透明基元以匹配背景色”的捷径。
- **生成阶段增益**：完整流程（重建 + 生成）将 PSNR 从纯重建的 11.56 提升至 **14.59**（+3.03），SSIM 从 0.293 提升至 0.323，LPIPS 从 0.558 降至 0.501。这直接证明了退化渲染条件生成策略的有效性——生成模型学会从粗糙的 4DGS 渲染中恢复高质量、时空一致的视频。

- **在线退化模拟**：Figure 7 的可视化表明，通过 Gaussian Culling 和 Average Geometry Filter 模拟遮挡、飞点像素和失真，模型学会了抑制这些伪影并在遮挡或扭曲区域“幻觉”出逼真细节。这是 NeoVerse 能够利用野生单目视频进行训练的关键机制。

![[assets/figures/papers/NeoVerse_Enhancing_4D_World_Model_with_in-the-wild_Monocular_Videos_full_rerun_20260609/figures/010_Figure_7.jpg]]
*Figure 7: Effectiveness of degradation simulation. The model learns to suppress artifacts and hallucinate realistic details in occluded or distorted regions through degradation simulation*

### 失败模式与局限性

Figure S1 展示了 NeoVerse 的两类典型失败案例：

1. **2D 内容处理**：对于卡通等缺乏真实 3D 结构的 2D 数据，模型可能生成错误的 3D 轮廓。这是因为前馈式 4DGS 重建依赖从单目视频中推断几何结构，而 2D 内容不提供有效的深度线索。
2. **文字生成**：与多数视频扩散模型类似，NeoVerse 偶尔难以生成清晰正确的文字，这是当前生成模型的共性瓶颈。

此外，高斯插值依赖线性运动假设，在高度非线性运动场景下可能偏离实际轨迹。训练数据规模因计算资源限制仅约 1M 视频片段（Table S1），更大规模训练可能进一步提升性能。当前生成模型仅冻结主干并训练控制分支，可能限制了对极端退化情况的适应能力。

## 定位与知识库关联

### 一、核心问题与因果机制

当前4D世界建模面临双重可扩展性瓶颈：**数据可扩展性**受限于对昂贵多视图数据的依赖，**训练可扩展性**受限于繁重的离线预处理（如深度估计、多视图匹配）。NeoVerse 的核心因果杠杆在于将两个关键设计耦合——**无姿态前馈式4DGS重建**与**在线单目退化模拟**——使得训练流程能够直接从大规模野生单目视频中学习，避免了传统方法的重计算预处理和有限数据问题。

具体而言，NeoVerse 的因果链条为：前馈式重建模型从稀疏关键帧在线重建4D高斯场 → 双向运动建模支持时间插值，使高斯场可渲染到任意新视角 → 在线退化模拟（Gaussian Culling、Average Geometry Filter）从单目视频直接生成含遮挡、飞点像素和失真的退化渲染 → 退化渲染作为条件输入视频生成模型，原始视频作为目标 → 生成模型学会从退化条件中恢复高质量、时空一致的视频。这一设计使得 NeoVerse 在静态重建（VRNeRF PSNR 20.73 vs. AnySplat 18.02）、动态重建（ADT PSNR 32.56 vs. 4DGT 30.09）和新视图生成（VBench 主观一致性 88.43 vs. TrajectoryCrafter 83.02）三个维度均取得显著提升，同时将总推理时间从 TrajectoryCrafter 的 146 秒压缩至 20 秒（Table 3）。

### 二、方法谱系定位

NeoVerse 处于**前馈式场景重建**、**4D高斯泼溅**与**视频生成模型**三条技术路线的交汇点。

**在静态重建谱系中**，NeoVerse 的前馈式4DGS重建模型构建于 **VGGT**（无姿态前馈重建基线）之上，并通过“高斯化”VGGT 的深度和点图预测，将其扩展为显式4D高斯场。与此前的前馈式高斯泼溅方法相比：**NoPoSplat**（Ye et al., ICLR 2024）和 **Flare**（Zhang et al., CVPR 2025）同样追求无姿态前馈重建，但 NeoVerse 在 VRNeRF 和 Scannet++ 两个基准上均显著超越（Table 1），核心差异在于 NeoVerse 引入了双向运动建模和不透明度正则化，避免了模型学习“输出透明基元”的捷径。**AnySplat** 作为另一静态重建对比方法，在 VRNeRF 上 PSNR 为 18.02，NeoVerse 领先 2.71 dB。

**在动态重建谱系中**，NeoVerse 的直接竞争对手是 **4DGT**（Xu et al., arXiv 2025）和 **MonST3R**（Zhang et al., arXiv 2024）。4DGT 采用单向时间建模，而 NeoVerse 的双向运动编码分支区分前向速度 $\boldsymbol{v}_i^+$ 和后向速度 $\boldsymbol{v}_i^-$，支持从稀疏关键帧向任意中间时间点的高斯场插值（Eq. 3-5）。这一设计使 NeoVerse 在 ADT 基准上 PSNR 达到 32.56，显著优于 4DGT 的 30.09。MonST3R 在 DyCheck 上仅取得 9.32 PSNR，NeoVerse 的纯重建部分即达到 11.56（+2.24），完整流程（重建+生成）更进一步提升至 14.59（Table 4），表明生成阶段对重建质量的补充作用显著。

**在新视图生成谱系中**，NeoVerse 与 **TrajectoryCrafter**（YU et al., ICCV 2025）和 **ReCamMaster** 形成对比。TrajectoryCrafter 同样追求相机可控的视频生成，但 NeoVerse 在 VBench 主观一致性上领先 5.41 分（88.43 vs. 83.02），且推理速度快 7 倍以上（20s vs. 146s）。这一优势源于 NeoVerse 将重建与生成解耦：前馈式重建提供显式3D/4D结构作为条件，生成模型仅需“修复”退化渲染，而非从零生成新视图内容。

### 三、关键设计决策与消融证据

消融实验（Table 4, DyCheck 基准）揭示了三个关键设计的因果贡献：

1. **双向运动建模**：去除后 PSNR 从 11.56 降至 11.27，降幅 0.29 dB。双向设计使模型能同时编码前向和后向瞬时速度，支持从稀疏关键帧向任意中间帧的高斯场插值，是稀疏重建效率的核心保障。

2. **不透明度正则化**：去除后 PSNR 降至 10.86，降幅 0.70 dB。该正则化防止模型在背景颜色相近区域输出透明基元的捷径行为，是重建质量的关键约束。

3. **生成阶段**：完整流程（w/ Generation）将 PSNR 从纯重建的 11.56 提升至 14.59，提升 3.03 dB。在线退化模拟训练使生成模型学会抑制遮挡区域的伪影并生成逼真细节（Figure 7），这是 NeoVerse 超越纯重建方法的核心增益来源。

### 四、适用边界与局限

NeoVerse 的适用边界由以下假设和约束定义：

1. **3D结构依赖**：方法假设输入视频包含可重建的3D场景结构。对于2D卡通等缺乏3D信息的数据，可能生成错误的3D轮廓（Figure S1），这是前馈式重建模型的内在局限。

2. **线性运动假设**：高斯插值依赖线性运动模型（Eq. 3-4），在高度非线性运动场景下可能偏离实际。双向建模缓解了单向建模的局限性，但未从根本上解决非线性运动问题。

3. **训练数据规模**：受计算资源限制，训练数据集仅约 1M 视频片段（Table S1），更大规模可能进一步提升性能。生成模型仅冻结主干并训练控分支，可能限制对极端退化情况的适应能力。

4. **文本生成能力**：与多数视频扩散模型类似，偶尔难以生成清晰正确的文字（Figure S1），这是当前视频生成模型的共性局限。

### 五、开放问题

1. **2D内容扩展**：如何将 NeoVerse 扩展到完全缺乏3D信息的2D内容（如卡通、平面动画），可能需要引入额外的几何先验或域适应策略。

2. **非线性运动建模**：线性运动假设能否通过高阶插值或学习式插值放宽，是提升极端动态场景重建质量的关键方向。

3. **掩码丢弃策略**：当前训练中的掩码丢弃（mask drop）策略对非退化输入生成质量的影响尚需系统评估，这可能影响模型在实际部署中的鲁棒性。

4. **数据筛选与增强**：如何更有效地利用大规模野生视频，是否需要更好的数据筛选和增强策略以提升训练效率，是进一步扩展数据规模的前提。

5. **生成模型微调**：当前仅训练控分支的策略是否限制了生成质量上限，未来是否应在更大规模数据上微调生成模型主干以进一步提升相机控制精度和生成质量。

## 原文 PDF

![[paperPDFs/CVPR_2026/NeoVerse_Enhancing_4D_World_Model_with_in_the_wild_Monocular_Videos.pdf]]
