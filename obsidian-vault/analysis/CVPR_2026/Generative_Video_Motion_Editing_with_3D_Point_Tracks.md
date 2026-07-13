---
title: Generative Video Motion Editing with 3D Point Tracks
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Generative_Video_Motion_Editing_with_3D_Point_Tracks.pdf
paper_link: https://openaccess.thecvf.com/content/CVPR2026/html/Lee_Generative_Video_Motion_Editing_with_3D_Point_Tracks_CVPR_2026_paper.html
project_link: https://edit-by-track.github.io
code_link: null
aliases:
- EBT
- GVME3PT
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 以三维点轨迹作为统一运动表示，通过跨注意力机制自适应地从源视频采样上下文并泼溅到目标帧空间，同时注入深度信息实现3D感知控制；辅以两阶段训练策略（合成数据引导+真实数据微调）确保模型对真实视频的泛化能力。
primary_logic: 3D点轨迹提供显式深度线索，使模型能够分辨深度顺序和处理遮挡；将完整源视频与源-目标3D轨迹对作为V2V条件，既保留原始场景上下文，又通过可学习的跨注意力采样-泼溅过程将3D轨迹自适应编码为2D屏幕对齐的token，实现精确的联合运动编辑。
claims:
- 在DyCheck数据集上，联合编辑相机和物体运动时，我们的方法在全帧和掩码指标上均显著优于所有现有方法（PSNR 14.80 vs 最佳13.94）。
- 在真实场景视频（MiraData）上，我们的方法在所有视觉质量和轨迹控制指标上取得最佳，且模型参数量仅1.3B，远超更大的14B模型。
- 消融实验证实，自适应交叉注意力+深度注入的组合以及两阶段训练策略对性能提升至关重要。
- DyCheck (joint camera & object motion) 上 PSNR↑ / SSIM↑ / LPIPS↓ (full-frame) = 14.80 / .424 / .406
---

# Generative Video Motion Editing with 3D Point Tracks

> [!tip] 核心洞察
> 3D点轨迹提供显式深度线索，使模型能够分辨深度顺序和处理遮挡；将完整源视频与源-目标3D轨迹对作为V2V条件，既保留原始场景上下文，又通过可学习的跨注意力采样-泼溅过程将3D轨迹自适应编码为2D屏幕对齐的token，实现精确的联合运动编辑。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于三维点轨迹的生成式视频运动编辑 |
| 英文题名 | Generative Video Motion Editing with 3D Point Tracks |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Lee_Generative_Video_Motion_Editing_with_3D_Point_Tracks_CVPR_2026_paper.html) · [Project](https://edit-by-track.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Edit-by-Track |
| Dataset | DyCheck, In-the-wild |

> [!tip] 效果简介
> - DyCheck (joint camera & object motion) 上，PSNR↑ / SSIM↑ / LPIPS↓ (full-frame) 14.80 /.424 /.406 vs TrajAttn +*: 13.94 /.416 /.549 (+0.86 / +.008 / -.143)；mPSNR↑ / mSSIM↑ / mLPIPS↓ (masked) 15.99 /.747 /.247 vs TrajAttn +*: 14.94 /.741 /.351 (+1.05 / +.006 / -.104)。
> - In-the-wild (MiraData) 上，PSNR↑ / SSIM↑ / LPIPS↓ 19.55 /.657 /.236 vs ATI: 19.07 /.635 /.244 (+0.48 / +.022 / -.008)；FVD↓ / EPE↓ (track control error) 306.44 / 6.12 vs ATI: 268.80 / 11.44 (+37.64 / -5.32)。

## 概要

视频运动编辑的核心挑战在于，如何同时精确控制摄像机运动和场景中物体的独立运动，同时保持原始场景的完整视觉上下文。现有方法在此问题上存在根本性局限：图像到视频（I2V）方法仅以单帧图像为条件，丢失了全场景的空间与外观信息；视频到视频（V2V）方法虽保留源视频，但通常只能处理摄像机视角变化或简单物体位移，缺乏3D感知能力，无法正确处理遮挡和与运动相关的次生效应（如阴影、飞溅等）。

**Edit-by-Track** 提出了一种全新的解决范式：以**三维点轨迹**作为统一的运动表示，将完整的源视频与配对的源-目标3D轨迹共同作为条件，驱动视频生成模型实现联合运动编辑。其核心洞察在于，3D点轨迹天然携带显式深度线索，使模型能够分辨深度顺序并隐式推理遮挡关系；同时，通过一个可学习的**3D轨迹条件器**，以交叉注意力机制自适应地从源视频中采样视觉上下文，并将其“泼溅”（splat）到目标帧空间，从而在保留原始场景全部信息的前提下，实现对摄像机姿态和物体运动的精确、3D感知的编辑控制。

在训练策略上，Edit-by-Track采用**两阶段微调**：先在合成数据上建立基本的运动控制能力，再在真实视频对上微调以弥合领域差异，确保对真实场景的泛化性。

实验结果表明，该方法在联合编辑摄像机与物体运动的**DyCheck**基准上，全帧PSNR达到14.80，掩码PSNR达到15.99，均显著优于所有现有方法；在真实场景视频**MiraData**上，以仅1.3B的模型参数量取得了最优的视觉质量与轨迹控制精度，超越了14B量级的对比模型。消融实验进一步证实，自适应交叉注意力采样/泼溅与深度注入的组合，以及两阶段训练策略，对性能提升至关重要。

**方法定位**：Edit-by-Track属于视频到视频（V2V）编辑范式，但区别于现有V2V方法仅做修复式生成，它通过3D轨迹条件实现了对摄像机与物体运动的联合、精确控制。在知识谱系上，它桥接了3D视觉（点轨迹估计、深度感知）与视频生成（扩散模型、交叉注意力条件注入）两个领域，为可控视频编辑提供了新的方法论基础。

视频运动编辑旨在对已拍摄视频中的运动进行精确修改，包括摄像机视角变化和场景中物体的运动。这一任务在电影制作、增强现实和内容创作等领域具有广泛的应用需求。然而，实现联合控制摄像机运动和物体运动的高质量编辑，仍然是当前生成式视频编辑领域面临的核心挑战。

现有方法在处理运动编辑时存在两个主要范式，但各自存在根本性局限。**图像到视频（I2V）方法**（如 **TrajAttn** (Xiao et al., ICLR 2025)、**ATI** (Wang et al., arXiv 2025) 等）仅以单帧图像作为条件输入，通过点轨迹或光流等运动信号驱动视频生成。这类方法虽然能够实现一定程度的运动控制，但由于丢失了源视频中除第一帧外的全部场景上下文，无法保留原始场景的完整视觉信息，导致生成结果在场景一致性、遮挡处理和时序连贯性方面存在明显不足。

**视频到视频（V2V）方法**（如 **GEN3C** (Ren et al., CVPR 2025)、**TrajCrafter** (Yu et al., ICCV 2025)）则以完整源视频为条件，通过对扭曲后的视频帧进行修复来实现运动编辑。然而，这类方法通常仅处理摄像机视角变化或简单的物体位移，缺乏对全场景三维结构的感知能力。当编辑涉及复杂的物体运动时，与运动相关的次生效应（如阴影、反射、飞溅等）往往无法被正确修正，导致编辑结果在物理合理性上存在缺陷。

上述两类方法的共同瓶颈在于：**缺乏统一的运动表示来同时编码摄像机运动和物体运动，且不具备显式的三维感知与遮挡处理能力**。具体而言，现有方法普遍采用二维点轨迹作为运动表示，通过固定最近邻采样或手工设计的屏幕空间映射来建立运动对应关系。这种二维表示无法提供深度线索，使得模型难以分辨物体的深度顺序，也无法正确处理遮挡关系。此外，I2V方法的单帧条件输入从根本上限制了其对完整场景上下文的理解，而V2V方法的扭曲-修复范式则难以纠正编辑运动引发的次生效应（图2）。

针对上述问题，本文提出 **Edit-by-Track**——一种基于三维点轨迹的生成式视频运动编辑框架。该框架以视频到视频（V2V）为基本范式，将完整的源视频与配对的三维点轨迹作为条件输入，通过可学习的跨注意力机制自适应地从源视频采样视觉上下文，并泼溅（splat）到目标帧空间，从而实现精确的联合运动编辑。三维点轨迹的核心优势在于提供显式的深度线索，使模型能够隐式推理可见性与遮挡关系，从而在编辑过程中保持正确的深度顺序和场景一致性。

## 核心方法与创新机理

Edit-by-Track 的核心创新在于将 **3D 点轨迹作为统一的运动表示**，并设计了一个可学习的 **3D 轨迹条件器**，通过交叉注意力机制实现从源视频到目标帧空间的自适应上下文采样与泼溅。相较于现有方法，这一设计在三个关键维度上实现了结构性突破。

### 1. 运动表示：从 2D 屏幕坐标到 3D 感知轨迹

现有轨迹条件方法（如 **TrajAttn** (Xiao et al., ICLR 2025)、**ATI** (Wang et al., arXiv 2025)）通常使用 2D 点轨迹，并采用固定最近邻采样或手工设计的屏幕空间表示来注入运动信息。这类表示缺乏深度线索，模型无法分辨物体的深度顺序，导致在遮挡场景下产生伪影。

Edit-by-Track 将运动表示升级为 **3D 点轨迹**，包含屏幕坐标 $(x, y)$ 和归一化视差 $z \in [0, 1]$。通过将源视频和目标视频的 3D 轨迹分别投影到各自相机空间，形成配对的投影轨迹 $(\mathcal{T}_{src}^{proj}, \mathcal{T}_{tgt}^{proj}) \in \mathbb{R}^{2 \times F \times N \times 3}$，模型获得了显式的深度信息。这一设计使模型能够隐式推理可见性与遮挡关系——消融实验（Table 3）证实，注入深度嵌入（$z$ embedding）对视觉质量和轨迹控制精度均有显著提升。

### 2. 条件机制：从固定采样到自适应交叉注意力泼溅

传统方法通常使用最近邻采样或固定高斯核将轨迹信息注入视频 token，这种方式假设轨迹点与其周围像素存在固定的空间对应关系，缺乏灵活性。

Edit-by-Track 的 **3D 轨迹条件器**（Figure 4）采用两阶段交叉注意力机制：

- **采样阶段**：以源轨迹坐标嵌入 $\rho_{src}^{xyz}$ 为查询，网格坐标编码 $\mathcal{G}$ 为键，从源视频 token $\nu_{src}$ 中自适应采样视觉上下文，再通过 Transformer 融合时序信息，得到 $\tau_{src}^{sampled}$：
  $$\tau_{src}^{sampled} = \mathrm{Transformer}\left(\mathrm{Attn}\left(\rho_{src}^{xyz}, \mathcal{G}, \nu_{src}\right)\right)$$

- **泼溅阶段**：将携带源视频上下文的采样 token 作为值，以网格坐标 $\mathcal{G}$ 为查询，源/目标坐标嵌入为键，通过交叉注意力泼溅回相应的帧空间：
  $$\tau_{\{src,tgt\}} = \mathrm{Attn}\left(\mathcal{G}, \rho_{\{src,tgt\}}^{xyz}, \tau_{src}^{sampled}\right)$$

这种可学习的采样-泼溅过程使模型能够自适应地确定每个轨迹点应该从源视频的哪些区域获取上下文，以及如何将其映射到目标帧的正确位置。消融实验（Table 3）表明，相较于固定高斯核或仅 2D 输入的方案，自适应交叉注意力配合深度注入在所有指标上均取得最优性能。

### 3. 条件输入范式：从单帧/扭曲帧到完整源视频

现有方法在条件输入上存在根本性局限：

- **I2V + track 方法**（如 TrajAttn、DaS、PaC、ATI）仅以第一帧图像为条件，丢失了全场景的时序上下文，无法处理第一帧不可见区域的内容生成。
- **V2V + inpaint 方法**（如 **GEN3C** (Ren et al., CVPR 2025)、**TrajCrafter** (Yu et al., ICCV 2025)）使用扭曲后的视频帧作为输入，但仅能处理摄像机视角变化或简单物体位移，无法纠正因物体运动改变而产生的次生效应（如阴影、水花等）。

Edit-by-Track 采用 **完整源视频 + 配对的源-目标 3D 轨迹** 作为条件。源视频 token $\nu_{src}$ 与含噪目标视频 token $\nu_{tgt}$ 拼接为 $[\nu_{src}, \nu_{tgt}] \in \mathbb{R}^{2 f h w \times d}$，轨迹 token $[\tau_{src}, \tau_{tgt}]$ 与对应视频 token 逐元素相加后输入 DiT 块。这一设计既保留了原始场景的完整上下文，又通过轨迹 token 建立了源-目标帧之间的稀疏对应关系，使模型能够同时编辑摄像机运动和物体运动，并保持因果一致性（如 Figure 2 所示，本方法正确保留了水花等次生效应）。

### 4. 训练策略：两阶段领域适应

现有方法通常采用单阶段训练，直接在合成数据或混合数据上训练，难以弥合合成数据与真实视频之间的领域差异。

Edit-by-Track 采用 **两阶段训练策略**（Figure 5）：
1. **第一阶段**：在合成数据（含真实点轨迹的人体动画视频对）上训练，建立基本的运动控制能力；
2. **第二阶段**：在真实单目视频的非连续片段对上微调，利用自然运动模拟联合相机和物体运动变化，增强对真实视频的泛化能力。

消融实验（Table 4）证实，两阶段训练在所有指标上均优于仅用合成数据、仅用真实数据或混合训练一阶段的方案，验证了“合成数据学习基本控制 + 真实数据增强泛化性”策略的有效性。

Edit-by-Track 的整体 pipeline 围绕一个核心洞察构建：**3D 点轨迹是统一描述摄像机运动和物体运动的理想中间表示**。现有方法要么仅以单帧图像为条件（I2V），丢失全场景上下文；要么仅对摄像机视角变化或简单物体位移进行修复（V2V），无法处理深度顺序与遮挡。本框架以完整源视频和配对的源-目标 3D 轨迹对作为条件，通过可学习的跨注意力机制将 3D 轨迹自适应编码为 2D 屏幕对齐的 token，实现联合运动编辑。

### 模块关系与数据流

框架由六个模块串联构成，数据流如图 3 所示：

1. **3D 轨迹估计与预处理**：给定源视频 $V_{src}$，利用现成模型估计相机参数、深度图和 3D 点轨迹 $\dot{T}_{src} \in \mathbb{R}^{F \times N \times 3}$。对背景轨迹可进行静态化处理以抑制微小抖动。

2. **运动编辑**：用户编辑相机姿态和 3D 轨迹，生成目标运动参数。将源轨迹和目标轨迹分别通过各自相机参数投影到 2D 屏幕坐标，得到投影轨迹对 $(\bar{\mathcal{T}}_{src}^{proj}, \mathcal{T}_{tgt}^{proj}) \in \mathbb{R}^{2 \times f \times N \times 3}$，其中 $z$ 值归一化到 $[0,1]$ 视差空间，作为显式深度线索。

3. **源视频编码与 Patchify**：通过 VAE 将源视频编码为潜变量，再切分成视频 token $\nu_{src}$。

4. **3D 轨迹条件器**（核心模块）：以投影轨迹对和源视频 token 为输入，通过**采样-泼溅**两阶段交叉注意力（图 4）产生与视频 token 空间对齐的轨迹 token $[\tau_{src}, \tau_{tgt}]$。该模块是方法的核心创新，详见下节。

5. **DiT 去噪模块**：将源视频 token $\nu_{src}$ 与含噪目标视频 token $\nu_{tgt}$ 拼接为 $[\nu_{src}, \nu_{tgt}] \in \mathbb{R}^{2 f h w \times d}$，与轨迹 token $[\tau_{src}, \tau_{tgt}]$ 逐元素相加后输入预训练 Wan-2.1 的 DiT 块，迭代去噪生成目标视频潜变量。

6. **VAE 解码**：将最终干净潜变量解码为目标 RGB 视频 $V_{tgt} \in \mathbb{R}^{F \times H \times W \times 3}$。

### 3D 轨迹条件器

该模块是连接 3D 运动表示与 2D 视频生成的关键桥梁（图 4）。其设计解决了两个核心问题：**如何从源视频中自适应采样相关视觉上下文**，以及**如何将采样到的上下文精确泼溅到目标帧空间以实现运动控制**。

具体而言，条件器首先以源坐标嵌入 $\rho_{src}^{xyz}$ 为查询、网格坐标编码 $\mathcal{G}$ 为键，通过交叉注意力从源视频 token $\nu_{src}$ 中自适应采样视觉上下文，再经 Transformer 融合时序信息，得到采样 token $\tau_{src}^{sampled}$：

$$\tau_{src}^{sampled} = \mathrm{Transformer}\left(\mathrm{Attn}\left(\rho_{src}^{xyz}, \mathcal{G}, \nu_{src}\right)\right)$$

随后，以网格坐标编码 $\mathcal{G}$ 为查询、源/目标坐标嵌入 $\rho_{\{src,tgt\}}^{xyz}$ 为键，通过第二个交叉注意力将携带源视频上下文的采样 token 泼溅回源和目标视频空间：

$$\tau_{\{src,tgt\}} = \mathrm{Attn}\left(\mathcal{G}, \rho_{\{src,tgt\}}^{xyz}, \tau_{src}^{sampled}\right)$$

这一采样-泼溅机制相比固定最近邻采样具有两个关键优势：一是通过可学习注意力自适应选择相关上下文，而非硬性指派；二是显式注入归一化视差 $z$ 的嵌入，使模型能够隐式推理深度顺序和可见性，从而正确处理遮挡。

### 两阶段训练策略

为弥合合成数据与真实视频之间的领域差异，框架采用两阶段训练（图 5）：

- **阶段一**：在合成数据上微调，利用真实 3D 点轨迹学习基本运动控制能力。合成数据对共享相同物体和背景，但物体动作和相机运动不同。
- **阶段二**：在真实单目视频上继续微调，通过采样非连续片段构建异步视频对，利用自然运动模拟联合相机和物体运动变化，增强对真实场景的泛化性。

消融实验（Table 4）证实，两阶段策略在所有指标上均优于仅用合成数据、仅用真实数据或混合训练一阶段的方案，验证了合成数据建立基本控制、真实数据增强泛化性的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Generative_Video_M/figures/003_Figure_3.jpg]]
*Figure 3: Edit-by-Track framework. Given a video*

Edit-by-Track 的核心运动控制由 **3D 轨迹条件器（3D Track Conditioner）** 实现，其设计目标是：以源视频的完整视觉上下文为素材库，通过三维点轨迹建立稀疏对应关系，自适应地采样并泼溅（splat）上下文信息到目标帧空间，同时注入深度线索以实现 3D 感知的遮挡推理。

### 3D 轨迹投影与深度注入

给定源视频的 3D 点轨迹 $\dot{T}_{src} \in \mathbb{R}^{F \times N \times 3}$（$F$ 帧，$N$ 个轨迹点）和用户编辑后的目标 3D 轨迹 $\dot{T}_{tgt}$，首先通过各自对应的相机参数将其投影到 2D 屏幕空间：

$$
\left(\mathcal{T}_{src}^{proj}, \mathcal{T}_{tgt}^{proj}\right) \in \mathbb{R}^{2 \times F \times N \times 3}
$$

每个投影点的三个通道分别为屏幕坐标 $(x, y)$ 和归一化视差 $z \in [0, 1]$。$z$ 值显式编码了深度排序信息，使模型能够隐式推理可见性与遮挡关系——这是本方法区别于纯 2D 轨迹条件方法的关键设计。消融实验（Table 3）证实，移除深度嵌入会导致视觉质量和轨迹控制精度显著下降。

### 自适应交叉注意力采样

条件器的核心操作分为两步交叉注意力。第一步从源视频 token $\nu_{src}$ 中自适应采样视觉上下文。具体地，将投影后的源轨迹坐标 $(x, y, z)$ 通过傅里叶编码生成坐标嵌入 $\rho_{src}^{xyz}$，作为查询（query）；将网格位置编码 $\mathcal{G}$ 作为键（key）；$\nu_{src}$ 作为值（value）：

$$
\tau_{src}^{sampled} = \mathrm{Transformer}\left(\mathrm{Attn}\left(\rho_{src}^{xyz}, \mathcal{G}, \nu_{src}\right)\right)
$$

这一设计的核心优势在于：不同于传统方法采用的固定最近邻采样，交叉注意力允许模型根据当前轨迹点的语义需求，自适应地聚合不同空间位置的视觉信息。随后的 Transformer 层进一步沿时序维度融合上下文，使每个轨迹 token 携带其对应点在整个视频中的外观和运动历史。

### 交叉注意力泼溅

第二步将携带源视频上下文的采样 token $\tau_{src}^{sampled}$ 泼溅回源帧和目标帧的屏幕空间，生成与视频 token 空间对齐的轨迹 token：

$$
\tau_{\{src,tgt\}} = \mathrm{Attn}\left(\mathcal{G}, \rho_{\{src,tgt\}}^{xyz}, \tau_{src}^{sampled}\right)
$$

此处网格坐标 $\mathcal{G}$ 作为查询，源/目标坐标嵌入作为键，$\tau_{src}^{sampled}$ 作为值。泼溅过程本质上是采样的逆操作：对于每个空间网格位置，模型查询与其最相关的轨迹点，并将该点携带的上下文信息分配到该位置。通过在源帧和目标帧分别执行泼溅，条件器建立了稀疏的帧间对应关系，使 DiT 去噪模块能够理解“源视频中的哪些区域应该移动到目标视频的哪些位置”。

### 与 DiT 主干的集成

条件器输出的轨迹 token $[\tau_{src}, \tau_{tgt}] \in \mathbb{R}^{2 f h w \times d}$ 与对应的视频 token $[\nu_{src}, \nu_{tgt}]$ 逐元素相加后，输入预训练的 Wan-2.1 DiT 模块进行迭代去噪。其中 $\nu_{src}$ 为源视频经 VAE 编码和 patchify 后的潜变量 token，$\nu_{tgt}$ 为含噪目标视频潜变量。这种拼接-相加的设计使运动控制信号与视觉内容在统一的潜空间中进行交互，既保留了源视频的完整场景上下文，又通过 3D 轨迹条件实现了精确的联合运动编辑。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Generative_Video_M/figures/004_Figure_4.jpg]]
*Figure 4: 3D track conditioner. Given N track pairs*

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Generative_Video_M/figures/005_Figure_5.jpg]]
*Figure 5: Training data. (a) Our model is first fine-tuned on the synthetic data with ground-truth point tracks to learn motion control. Each video pair shares the same objects and background scenes but differs in object actions and camera motions. (b) We continue fine-tuning on real data by sampling two non-contiguous clips from a monocular video, leveraging its natural motion to scalably simulate joint camera and object motion changes*

## 实验与关键发现

### 核心瓶颈与因果机制

现有视频运动编辑方法面临一个根本性矛盾：图像到视频（I2V）方法仅以单帧图像为条件，丢失了全场景上下文，无法生成与源视频一致的背景和次生效应；视频到视频（V2V）方法虽然保留了视频输入，但主流方案仅能处理摄像机视角变化或简单物体位移，缺乏对全场景3D感知和遮挡关系的建模能力。这导致在联合编辑摄像机运动和物体运动时，现有方法要么丢失背景上下文，要么无法纠正运动编辑引发的次生效应（如阴影、飞溅等）。

Edit‑by‑Track的核心因果机制在于将**3D点轨迹**作为统一的运动表示，通过**跨注意力采样‑泼溅**过程将3D运动信息自适应地编码为与视频token对齐的2D条件信号。具体而言，3D轨迹的归一化视差分量 $z$ 为模型提供了显式的深度线索，使其能够分辨深度顺序并隐式推理遮挡关系；而跨注意力机制从完整源视频中自适应采样视觉上下文，再通过泼溅操作将上下文分配到源和目标帧空间，从而在保留原始场景信息的同时实现精确的运动控制。两阶段训练策略——先在合成数据上建立基本运动控制能力，再在真实视频对上微调以弥合领域差异——进一步确保了模型对真实场景的泛化性。

### 主实验结果

#### DyCheck联合运动编辑基准

Table 1展示了在DyCheck数据集上联合编辑摄像机与物体运动的定量对比。该数据集包含12个场景，评估指标分为全帧（full‑frame）和掩码（masked，仅共视区域）两类，分别衡量整体视觉质量和运动编辑区域的重建精度。

在全帧指标上，Edit‑by‑Track取得了PSNR 14.80、SSIM 0.424、LPIPS 0.406，相比最佳对比方法TrajAttn*（PSNR 13.94、SSIM 0.416、LPIPS 0.549）在PSNR上提升+0.86，LPIPS大幅降低‑0.143。在掩码指标上，本方法同样全面领先：mPSNR 15.99（+1.05）、mSSIM 0.747（+0.006）、mLPIPS 0.247（‑0.104）。值得注意的是，TrajAttn*等方法使用了目标视频的真实光流来扭曲输入帧，而Edit‑by‑Track仅依赖现成模型估计的3D轨迹，不访问任何真实运动信息，设置更为严格且更贴近实际应用场景。

#### 真实场景视频泛化性

Table 2报告了在MiraData真实场景视频上的对比结果。该测试集从MiraData中随机采样100段视频，评估视觉质量（PSNR、SSIM、LPIPS、FVD）和轨迹控制精度（EPE）。Edit‑by‑Track在所有视觉质量指标上均取得最优：PSNR 19.55（vs. ATI的19.07）、SSIM 0.657（vs. 0.635）、LPIPS 0.236（vs. 0.244）。在轨迹控制精度上，本方法的EPE仅为6.12，远优于ATI的11.44，表明3D轨迹条件器能够更精确地将运动控制信号传递到生成过程中。尤为突出的是，Edit‑by‑Track的模型参数量仅1.3B，远小于ATI的14B，却取得了全面的性能优势，证明了方法设计的有效性而非单纯依赖模型规模。

### 消融实验

#### 3D轨迹条件模块设计

Table 3系统消融了3D轨迹条件器的关键设计选择。完整方法采用自适应跨注意力采样/泼溅并注入深度嵌入（$z$），相比以下消融配置均有显著提升：

- **固定高斯核采样**：将自适应跨注意力替换为固定高斯核的最近邻采样，视觉质量和轨迹控制精度均明显下降，说明自适应采样能够更灵活地从源视频中提取与轨迹相关的上下文信息。
- **仅2D坐标输入**：移除归一化视差 $z$ 和深度嵌入，仅使用2D屏幕坐标 $(x, y)$，模型失去了深度感知能力，在遮挡区域和深度顺序判断上表现恶化，验证了深度线索对3D感知控制的关键作用。
- **无泼溅操作**：仅将采样后的轨迹token直接注入目标帧空间，而不通过泼溅同时更新源和目标帧的对应关系，导致源‑目标运动对应性减弱，编辑精度降低。

#### 两阶段训练策略

Table 4对比了不同训练方案的效果。完整的两阶段策略（合成数据引导 + 真实数据微调）在所有指标上均优于以下替代方案：

- **仅合成数据**：模型学习了基本的轨迹控制能力，但对真实视频的纹理、光照和复杂运动分布泛化不足。
- **仅真实数据**：由于真实视频中难以获取精确配对的运动变化样本，模型未能建立稳健的运动控制基础。
- **混合训练一阶段**：将合成数据和真实数据混合后单阶段训练，性能介于两者之间，但不及两阶段策略，表明分阶段训练有助于模型先掌握核心运动控制技能，再适应真实域分布。

### 失败模式与局限性

尽管Edit‑by‑Track在联合运动编辑上取得了显著进展，仍存在以下局限：

1. **3D估计依赖性**：方法依赖现成模型进行相机参数、深度和3D轨迹估计。当估计不准确时——尤其是静态背景区域的微小抖动——编辑结果可能出现伪影或运动不一致。这一瓶颈需要更鲁棒的3D感知前端来缓解。

2. **密集小物体与强自遮挡**：对于包含大量小物体或高度自遮挡的场景，3D轨迹的估计和条件编码可能不够鲁棒，导致部分区域的运动控制失效或视觉质量下降。

3. **物理次生效应的不一致**：模型生成的编辑结果可能不完全符合物理规律。例如，当物体运动改变时，阴影、反射、飞溅等与运动因果相关的次生效应可能未被正确修正（如Figure 9中GEN3C未能纠正的阴影问题，本方法虽有所改善但仍存在不足）。

4. **合成数据的类别局限**：两阶段训练中的合成数据目前仅包含人体动画，这可能限制了模型对非人体物体（如车辆、动物）进行精细运动控制的能力。扩展合成数据覆盖的物体类别是一个重要的工程方向。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Generative_Video_M/figures/002_Figure_2.jpg]]
*Figure 2: Limitations of existing methods. We demonstrate joint camera and object motion editing on an input video (first row)—changing both the camera viewpoint and the person’s falling location—using frames warped by the edited motion as reference (second row). The prior camera-controlled V2V approach [86] inpaints from the warped input video but fails to correct secondary effects (e.g., splashes) caused by the edited object motion. The track-conditioned I2V method [101] loses input scene context by conditioning only on the first frame. In contrast, our approach edits both camera and object motion while preserving the input context and maintaining coherent causal effects (third row)*

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Generative_Video_M/figures/009_Table_1.jpg]]
*Table 1: Quantitative comparison on joint camera and object motion on DyCheck [24]. We report full-frame and masked (covisible areas only [24]) metrics, averaged across 12 scenes. The best and second-best scores are highlighted. Some methods use ground-truth (GT) information for their inputs. GT 1st frame denotes using the first frame of the target GT video. Methods marked with ∗ use the estimated flow to the GT video to warp the input. ∗TrajAttn [120] takes warped video input using the extension of NVS-Solver [128]*

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Generative_Video_M/figures/010_Table_2.jpg]]
*Table 2: Quantitative comparison on in-the-wild videos. We compare with track-conditioned methods on a test set of 100 videos randomly sampled from MiraData [43]. We report PSNR, SSIM, LPIPS, FVD for visual quality, and EPE for track control*

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Generative_Video_M/figures/012_Table_3.jpg]]
*Table 3: Ablation study on 3D track conditioning. Our method (bottom) adaptively handles 3D tracks using cross-attentional sampling/splatting and injects depth embeddings for 3D-aware control. Ablation configurations are detailed in Sec. 4.4*

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Generative_Video_M/figures/013_Table_4.jpg]]
*Table 4: Ablation study on training scheme. Our method (bottom) first learns track control on synthetic data, then fine-tunes on real data for generalizability, outperforming all ablated settings*

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Generative_Video_M/figures/006_Figure_6.jpg]]
*Figure 6: Joint camera and object motion editing. Our method enables the editing of camera and/or object motion using edited camera poses and 3D point tracks (visualized in corner insets)*

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Generative_Video_M/figures/011_Figure_9.jpg]]
*Figure 9: Visual comparisons on video editing. We edit a DAVIS [82] video with a 3D object rotation, using the target motion-warped as reference. I2V methods [28, 101] lose context outside of the input first frame (corner insets). GEN3C [86] inputs the warped video but fails to correct the shadow of the edited object (red arrow). See SM for additional in-the-wild results*

![[assets/figures/papers/paper_list_l8_https_openaccess_thecvf_com_content_CVPR2026_html_Lee_Generative_Video_M/figures/008_Figure_8.jpg]]
*Figure 8: Handling partial tracks. By specifying only the body motion (moving right) via a bounding box and removing leg tracks, our model synthesizes correct leg motion without explicit controls on the legs. Background tracks are hidden for clarity*

## 定位与知识库关联

### 与现有工作的关系

**Edit-by-Track** 在视频运动编辑领域占据了一个独特的位置：它既不同于图像到视频（I2V）方法，也不同于仅处理摄像机运动的视频到视频（V2V）方法，而是通过**3D点轨迹作为统一运动表示**，实现了对摄像机运动和物体运动的联合精确控制。

#### 相对于I2V+轨迹方法

现有的轨迹条件I2V方法——如 **TrajAttn**（Xiao et al., ICLR 2025）、**DaS**、**PaC** 和 **ATI**（Wang et al., arXiv 2025）——仅以单帧图像为条件生成视频。这种设计的根本局限在于：当摄像机运动剧烈时，第一帧无法提供全场景的视觉上下文，导致生成内容丢失原始场景信息（如Figure 2第三行所示）。Edit-by-Track 将条件输入从单帧扩展为**完整源视频**，通过V2V框架保留了原始场景的全部上下文，从根本上解决了这一瓶颈。

#### 相对于V2V+修复方法

**GEN3C**（Ren et al., CVPR 2025）和 **TrajCrafter**（Yu et al., ICCV 2025）等V2V方法虽然使用了完整视频输入，但其运动控制仅限于摄像机视角变化或简单的物体位移。当同时编辑摄像机和物体运动时，这些方法依赖运动扭曲后的视频帧进行修复，但**无法纠正由物体运动变化引起的次生效应**（如飞溅、阴影等，见Figure 2第二行）。Edit-by-Track 通过3D轨迹条件器直接学习源运动到目标运动的映射，避免了这种中间扭曲带来的信息损失。

#### 相对于IV2V+轨迹+修复方法

**ReVideo**（Mou et al., NeurIPS 2024）结合了轨迹条件和修复，但仍缺乏显式的3D感知能力。Edit-by-Track 的关键突破在于：**3D点轨迹提供显式深度线索**（归一化视差 $z$），使模型能够分辨深度顺序并隐式推理遮挡关系。这是现有方法均未实现的能力。

### 适用边界与条件

1. **依赖第三方估计质量**：Edit-by-Track 的3D轨迹和深度来自现成模型（如 [119, 131]）。当这些估计不准确时（尤其是静态背景的微小抖动），编辑效果会受影响。这意味着方法的鲁棒性与上游估计器的性能强耦合。

2. **合成数据覆盖范围**：两阶段训练的第一阶段依赖合成数据（目前仅包含人体动画，如 Mixamo ）。这限制了模型对**非人体物体的精细运动控制**能力——对于车辆、流体等类别，模型可能缺乏足够的运动先验。

3. **密集小物体与高度自遮挡场景**：当场景中存在大量密集小物体或严重自遮挡时，3D轨迹的估计和条件编码可能不够鲁棒。这是点轨迹表示本身的固有限制。

4. **物理合理性的边界**：模型学习的是视觉层面的运动编辑，而非物理模拟。因此，与运动相关的次生效应（阴影、反射、飞溅）可能不完全符合物理规律。用户需对此有合理预期。

### 局限与开放问题

#### 已明确的局限

- **次生效应的物理一致性**：如Figure 2所示，现有V2V方法无法修正编辑后的次生效应，Edit-by-Track 虽有改善，但并未声称完全解决该问题。阴影、反射等效果的正确生成仍是一个开放挑战。
- **部分轨迹输入的泛化性**：Figure 8展示了仅用边界框指定身体运动时模型能合成合理腿部运动，但这依赖于模型对人体运动先验的学习。对于训练数据中未见的物体类别，这种泛化能力可能显著下降。
- **计算开销**：相比I2V方法，V2V框架需要编码完整源视频，且在3D轨迹条件器中进行交叉注意力采样-泼溅，增加了计算负担。

#### 开放问题

1. **多物体交互与长期遮挡**：当前方法处理的是相对独立的物体运动编辑。对于复杂的多物体交互（如碰撞、抓取）和长期遮挡场景，模型是否能在不依赖外部运动模型的情况下保持一致性，尚待验证。

2. **任意物体类别的扩展**：两阶段训练策略要求合成数据与目标域相关。能否设计一种**类别无关的运动控制机制**，使模型无需针对每个新类别重新设计合成数据，是一个重要的研究方向。

3. **物理合理性的量化评估**：目前评估依赖PSNR、SSIM、LPIPS等感知质量指标和EPE等轨迹控制精度指标，但缺乏对编辑后视频**物理合理性**的量化度量——尤其是在非刚性变形和动力学效果方面。这需要新的评估基准和指标设计。

4. **用户输入的进一步简化**：当前方法要求用户编辑3D轨迹或相机参数。如何降低交互门槛——例如**仅用自然语言描述运动编辑意图**，或通过更直观的界面操作——是推动方法实际应用的关键问题。

5. **与大规模预训练模型的融合**：Edit-by-Track 基于 Wan-2.1（1.3B）构建，参数量远小于部分对比方法（如ATI 14B）。如何将3D轨迹条件机制融入更大规模的视频生成模型，以进一步提升生成质量和运动控制精度，值得探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/Generative_Video_Motion_Editing_with_3D_Point_Tracks.pdf]]
