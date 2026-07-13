---
title: "LaVR: Scene Latent Conditioned Generative Video Trajectory Re-Rendering using Large 4D Reconstruction Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LaVR_Scene_Latent_Conditioned_Generative_Video_Trajectory_Re_Rendering_using_Large_4D_Reconstruction_Models.pdf
project_link: "https://lavr-4d-scene-rerender.github.io"
code_link: null
aliases:
- LaVR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将预训练4D重建模型(CUT3R)的隐式潜变量作为几何条件信号注入视频扩散模型，替代传统基于点云渲染的显式几何条件。
primary_logic: 利用大型4D重建模型潜在空间中蕴含的隐式几何知识作为软约束，使预训练视频扩散模型能够利用其强大的运动与场景先验来校正小的几何不一致，从而在不需要精确深度估计的情况下，生成既具有高视觉质量又保持几何一致性的新视角视频。
claims:
- 在量化指标上，本方法在循环一致性（PSNR 20.74，LPIPS 22.47，CLIP 98.07）和姿态重建精度（Abs(t) 14.39 mm，Rel(R) 0.411°）上全面优于所有基线方法。
- 消融实验表明，CUT3R潜变量条件是性能提升的主要驱动因素，移除后导致Cycle PSNR从20.74降至17.90，Multi-View从17.11降至6.832，而姿态条件仅提供额外较小的增益。
- 定性结果展示，本方法避免了点云条件方法中的非自然扭曲伪影以及无条件方法的幻觉内容，生成结果更自然且几何上更一致。
- Cycle Consistency 上 PSNR↑ = 20.74
---

# LaVR: Scene Latent Conditioned Generative Video Trajectory Re-Rendering using Large 4D Reconstruction Models

> [!tip] 核心洞察
> 利用大型4D重建模型潜在空间中蕴含的隐式几何知识作为软约束，使预训练视频扩散模型能够利用其强大的运动与场景先验来校正小的几何不一致，从而在不需要精确深度估计的情况下，生成既具有高视觉质量又保持几何一致性的新视角视频。

| 字段 | 内容 |
|------|------|
| 中文题名 | LaVR：基于大型4D重建模型的场景潜在条件生成式视频轨迹重渲染 |
| 英文题名 | LaVR: Scene Latent Conditioned Generative Video Trajectory Re-Rendering using Large 4D Reconstruction Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.14674) · [Project](https://lavr-4d-scene-rerender.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | LaVR |
| Dataset | Cycle Consistency, VBench Consistency, Pose Reconstruction |

> [!tip] 效果简介
> - Cycle Consistency 上，PSNR↑ 20.74 vs Gen3C 20.62 (+0.12)；LPIPS↓ 22.47 (×10⁻²) vs Gen3C 23.23 (-0.76)。
> - VBench Consistency 上，Subject↑ 95.22 vs ReCamMaster 94.95 (+0.27)；Multi-view↑ 17.11 vs TrajectoryCrafter 15.57 (+1.54)。
> - Pose Reconstruction 上，Abs(t)↓ (mm) 14.39 vs TrajectoryCrafter 16.53 (-2.14)。

## 概要

**核心问题**：从单目源视频生成几何一致的新视角视频轨迹时，现有方法在视觉质量与空间一致性之间存在根本性权衡。无几何条件的方法（如 **ReCamMaster**，Bai et al., arXiv 2025）缺乏空间感知能力，在大视角变化下易产生漂移和幻觉；而基于点云渲染的显式几何条件方法（如 **Gen3C**，Ren et al., CVPR 2025；**TrajectoryCrafter**，Yu et al., ICCV 2025）高度依赖深度估计精度，深度误差会直接导致渲染视图的形状扭曲、视差不一致及空洞伪影。

**核心洞察**：利用预训练4D重建模型（CUT3R）潜在空间中蕴含的隐式几何知识作为软约束，替代显式点云条件。这一设计使预训练视频扩散模型能够借助其强大的运动与场景先验来校正小的几何不一致，从而在不依赖精确深度估计的情况下，同时获得高视觉质量与几何一致性。

**方法定位**：LaVR 在几何条件范式中引入第三类方案——**潜变量几何条件**（图2）。通过轻量级 CUT3R 适配器将帧级4D潜变量令牌转换为与扩散模型对齐的空间几何特征，并以流匹配损失训练，仅微调 DiT 的投影层与自注意力层。

**主要结果**：
- **循环一致性**：PSNR 20.74（vs. Gen3C 20.62），LPIPS 22.47（vs. Gen3C 23.23），CLIP 98.07，全面领先。
- **姿态重建精度**：平移误差 Abs(t) 14.39 mm，旋转误差 Rel(R) 0.411°，均优于所有基线。
- **VBench 一致性**：多视角一致性 17.11（vs. TrajectoryCrafter 15.57），主题一致性 95.22（vs. ReCamMaster 94.95）。
- **消融实验**：移除 CUT3R 潜变量条件后，Cycle PSNR 从 20.74 骤降至 17.90，Multi-View 从 17.11 降至 6.832，验证了潜变量几何条件是性能提升的核心驱动因素。

**局限**：对透明物体（如被举起的玻璃杯）的几何估计仍存在困难；CUT3R 条件机制引入额外计算开销。



### 问题定义：单目视频的几何一致新轨迹渲染

给定一段单目源视频，生成同一场景在任意新相机轨迹下的视频，这一任务在3D内容创作、虚拟现实和视频编辑等领域具有广泛的应用前景。该任务的核心挑战在于，生成的新视角视频必须同时满足两个相互制约的需求：**视觉质量**（生成帧的自然度与细节保真度）和**几何一致性**（场景结构在新视角下的空间连贯性）。

### 现有方法的两难困境

当前主流方法可归为两类范式，二者在视觉质量与几何一致性之间存在根本性的权衡（Figure 2）：

**无几何条件方法**（如 **ReCamMaster** (Bai et al., arXiv 2025)）仅依赖视频扩散模型的生成先验来推断新视角。这类方法能够产生高视觉质量的输出，但由于缺乏对场景空间结构的显式感知，在大视角变化或遮挡场景下容易产生漂移、变形甚至幻觉内容——例如生成不存在的物体或错误的人体部位。

**基于点云渲染的几何条件方法**（如 **Gen3C** (Ren et al., CVPR 2025)、**TrajectoryCrafter** (Yu et al., ICCV 2025)）试图通过将源视频重建为4D点云，再渲染到目标视角作为条件信号来解决一致性问题。然而，这一管线将生成质量与深度估计精度深度绑定：深度尺度模糊、内参估计误差、点云空洞与未对齐等缺陷会直接导致条件图像产生非自然扭曲（Figure 7），进而使生成结果出现形状畸变、视差不一致及细节丢失等问题。

### 核心瓶颈

上述困境的根源在于：**显式几何条件（点云渲染图像）对深度估计误差高度敏感，而完全无几何条件则缺乏空间约束**。这构成了一个根本性的瓶颈——如何在避免显式几何重建误差的同时，为视频扩散模型注入足够的空间感知能力？

### 本文动机与核心思路

本文提出 **LaVR**，其核心动机是打破上述权衡。关键洞察在于：大型4D重建模型（如CUT3R）在其隐式潜变量空间中已经编码了丰富的场景几何知识，这些知识可以作为“软约束”直接注入视频扩散模型，从而绕开显式点云重建的误差累积问题。

具体而言，LaVR将预训练4D重建模型的潜变量作为几何条件信号，通过轻量适配器与视频VAE潜变量对齐后送入扩散模型。这种设计允许预训练视频扩散模型利用其强大的运动与场景先验来**校正小的几何不一致**，在不需要精确深度估计的前提下，同时实现高视觉质量与几何一致性（Figure 1）。



## 核心方法与创新机理

### 问题根因：几何一致性与视觉质量的本质权衡

现有视频轨迹重渲染方法面临一个根本性瓶颈：**几何条件信号的精度与生成视觉质量之间存在不可调和的矛盾**。具体而言：

- **无几何条件方法**（如 **ReCamMaster**，Bai et al., arXiv 2025）完全依赖视频扩散模型的生成先验来推断新视角内容。这类方法虽然能产出高视觉质量的帧，但缺乏空间感知能力，在大视角变化下会产生漂移、变形和幻觉内容——例如人物与桌子重叠、物体在遮挡后消失或形态改变（Figure 8）。
- **显式几何条件方法**（如 **Gen3C**，Ren et al., CVPR 2025；**TrajectoryCrafter**，Yu et al., ICCV 2025）通过深度估计→点云重建→点云渲染的管线为扩散模型提供几何引导。然而，这一管线高度依赖深度估计精度：深度尺度模糊、内参估计误差、点云空洞和对齐错误会直接导致渲染条件图像出现扭曲（Figure 7），进而在生成结果中表现为非自然的拉伸伪影和细节丢失（Figure 6, Figure 9）。

核心矛盾在于：**显式几何条件将深度估计的误差硬编码为不可修正的约束，而无几何条件则完全放弃了空间一致性保障**。

### 核心洞察：隐式几何知识作为软约束

LaVR 的核心洞察是：**利用预训练大型4D重建模型潜在空间中蕴含的隐式几何知识作为软约束**，使预训练视频扩散模型能够利用其强大的运动与场景先验来校正小的几何不一致，从而在不需要精确深度估计的情况下，同时实现高视觉质量和高几何一致性。

这一设计的因果机制可概括为：

> 将预训练4D重建模型（CUT3R）的隐式潜变量作为几何条件信号注入视频扩散模型，替代传统基于点云渲染的显式几何条件。

与点云条件方法的“硬约束”不同，CUT3R潜变量提供的是一种“软几何条件”——它编码了场景的空间结构信息，但不强制像素级的精确对应。扩散模型在去噪过程中既受此条件引导，又保留了一定的自由度来利用自身先验平滑几何不一致性，从而避免了点云误差导致的扭曲伪影。

### Changed Slots：相对基线的关键设计变更

LaVR 相对于现有基线方法的核心变更体现在三个维度：

| 设计维度 | 基线方法 | LaVR 方案 | 证据锚点 |
|---------|---------|----------|---------|
| **几何条件信号** | 无条件（ReCamMaster）或点云渲染图像（Gen3C, TrajectoryCrafter） | CUT3R潜变量经适配器对齐后的空间特征 | Figure 3: "To ensure geometric consistency, we condition the model on latents from CUT3R, a pretrained 4D reconstruction model." |
| **姿态注入方式** | 未使用或简单拼接 | 通过独立MLP适配器分别注入源相机姿态与目标相机姿态至DiT各层 | Figure 3: "The source camera poses come from CUT3R and are added to the DiT’s intermediate activations after passing through a small MLP-based adapter. Another MLP processes the target poses..." |
| **训练策略** | 端到端训练或完全冻结骨干 | 仅微调DiT的投影层与自注意力层，冻结VAE及其他参数；CUT3R适配器使用3倍学习率 | Section 3.3: "Only the projection and self-attention layers of the DiT are trainable... a 3× higher learning rate for the CUT3R adapter" |

**几何条件信号的变更**是方法的核心贡献。CUT3R的每帧潜变量令牌 $\{\ell^i \in \mathbb{R}^d\}_{i=1}^{s}$ 通过一个轻量级适配器（MLP + Query Transformer，Figure 4）转换为与VAE潜变量空间对齐的几何感知特征，使扩散模型能够在不接触显式深度或点云的情况下获取场景几何信息。

**双路姿态注入**设计将源相机姿态（来自CUT3R）和目标相机路径姿态分别通过独立MLP适配器注入DiT的中间激活层，实现了对源视角几何上下文和目标渲染视角的分离控制。

**选择性微调策略**仅训练DiT的投影层和自注意力层，冻结VAE编解码器及其他参数，同时对CUT3R适配器施加3倍学习率以加速几何特征的对齐学习。这一策略在保持预训练视频扩散模型强大生成先验的同时，以最小参数代价引入了几何条件能力。

### 消融验证：CUT3R潜变量是性能核心驱动

消融实验（Table 3）提供了关键因果证据：

- **移除CUT3R潜变量条件**（仅保留源姿态）导致Cycle PSNR从20.74骤降至17.90，VBench Multi-View从17.11崩溃至6.832，姿态误差显著上升。这证明CUT3R潜变量是几何一致性的**主要驱动因素**。
- **完整模型**相较于无几何条件且无姿态的基线（ReCamMaster等价设置），Cycle PSNR提升2.99（20.74 vs 17.75），姿态误差大幅降低，验证了潜变量条件+姿态注入的整体设计有效性。
- 源姿态条件单独提供的增益相对较小，表明其扮演的是**补充性角色**——在潜变量条件的基础上进一步增强时序一致性。

定性结果（Figure 6, Figure 9）进一步佐证：LaVR生成的视频避免了点云条件方法的非自然扭曲伪影（如拉伸、细节丢失）以及无条件方法的幻觉内容（如凭空出现第三条手臂），在视觉自然性和几何一致性之间取得了现有方法无法达到的平衡。



LaVR 的核心设计思路是用**预训练4D重建模型的隐式几何潜变量替代显式点云渲染**作为几何条件信号，注入到预训练视频扩散模型中。这一设计绕开了现有方法在几何一致性与视觉质量之间的根本性权衡：无几何条件的方法（如 **ReCamMaster**，Bai et al., arXiv 2025）缺乏空间感知能力，在大视角变化下产生漂移和幻觉；而基于点云渲染的几何条件方法（如 **Gen3C**，Ren et al., CVPR 2025；**TrajectoryCrafter**，Yu et al., ICCV 2025）高度依赖深度估计精度，深度误差会直接导致渲染视图的形状扭曲和空洞（见 Figure 7）。

### 输入输出与数据流

给定一段单目源视频，LaVR 生成同一场景在任意目标相机轨迹下的新视角视频。系统从源视频中提取四类信号，经过适配后并行注入扩散模型（见 Figure 3）：

![[assets/figures/papers/paper_list_l2534_https_arxiv_org_abs_2601_14674/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline overview. Given a monocular source video, our method generates a novel video of the same scene at a target camera trajectory using a video diffusion model. To ensure geometric consistency, we condition the model on latents from CUT3R [35], a pretrained 4D reconstruction model. We use four signals from the source video: the standard video VAE latents, CUT3R’s 4D latents, source camera poses, and an encoded text description of the scene. A novel adapter architecture aligns the CUT3R and VAE latents and allows these to be fed to the model in a computationally feasible manner. The source camera poses come from CUT3R and are added to the DiT’s intermediate activations after passing thro...*

1. **视频VAE潜变量**：由冻结的Video VAE Encoder将源视频编码为标准视频潜变量，作为扩散模型的主要内容信号。
2. **CUT3R 4D潜变量**：由预训练的CUT3R Encoder逐帧提取。CUT3R内部维护一组可学习的潜状态令牌，每帧由ViT编码的帧特征更新这些令牌，形成蕴含隐式几何信息的4D状态集合 $\mathcal{S} = \{ \{ \ell_{t}^{i} \in \mathbb{R}^{d} \}_{i=1}^{s}, t=1,2,\ldots,T \}$。这些令牌经过**CUT3R适配器**转换为与VAE潜变量空间对齐的几何特征。
3. **源相机姿态**：由CUT3R估计的逐帧源相机外参，通过独立的MLP适配器注入DiT各层的中间激活。
4. **目标相机轨迹**：用户指定的目标相机路径姿态，通过另一个MLP适配器注入DiT。

### 核心模块与管线架构

**CUT3R适配器**（Figure 4）是整个框架的关键桥梁模块。它由MLP和Query Transformer组成，将CUT3R的逐帧潜变量令牌转换为几何感知的空间特征，使其在形状和语义上与扩散模型使用的VAE潜变量表示对齐。这一轻量设计使得预训练扩散模型能够在不需要重新训练的情况下消费来自4D重建模型的隐式几何知识。

**姿态注入**采用双通道设计：源姿态MLP适配器将CUT3R估计的源相机姿态注入DiT中间激活层，为目标姿态MLP适配器提供空间参考基准；目标姿态MLP适配器则注入用户指定的目标相机路径，控制生成视频的视角变化。

**扩散骨干**采用冻结的DiT（Denoising Diffusion Transformer），仅微调其投影层和自注意力层，VAE编解码器及其他参数保持冻结。训练目标为标准条件流匹配损失：

$$\mathcal{L}_{\mathrm{FM}} = \mathbb{E}_{t, z_{0}, \epsilon} \left[ \| v_{\theta}(z_{t}, t, Z_{c}, Z_{s}) - (\epsilon - z_{0}) \|_{2}^{2} \right]$$

其中 $Z_{c}$ 为CUT3R几何条件，$Z_{s}$ 为源姿态条件。

### 训练策略

模型在 **ReCamMaster** 的合成数据集 MultiCamVideo 上进行训练，使用8张H200 GPU，总计约15K次迭代，批次大小为8。CUT3R适配器使用3倍于其他可训练参数的学习率，以加速几何条件的对齐学习。模型总参数量约1.3B，其中绝大部分来自冻结的预训练组件，实际可训练参数规模较小。

### 补充图表

![[assets/figures/papers/paper_list_l2534_https_arxiv_org_abs_2601_14674/figures/002_Figure_2.jpg]]
*Figure 2: Architecture comparison. (a) Unconditioned methods for novel trajectory generation achieve high visual quality but lack geometric awareness, leading to inconsistencies. (b) Conditioning on 4D point cloud renders provides consistency but reduces quality because the depth estimation and point cloud generation stages are sensitive to errors. (c) Our proposed architecture utilizes the implicit geometric knowledge of a pre-trained large 4D reconstruction model (LRM) to achieve both high quality and consistency*

![[assets/figures/papers/paper_list_l2534_https_arxiv_org_abs_2601_14674/figures/001_Figure_1.jpg]]
*Figure 1: Our method addresses the problem of rendering geometrically consistent novel trajectories from a monocular source video. We propose to utilize the geometric knowledge of a pretrained large reconstruction model (LRM) by conditioning the trajectory generation process on the latent state of a 4D LRM. Compared to prior methods that are conditioned on error-prone point cloud re-renderings of the source video, our method achieves state-of-the-art visual quality while maintaining a high level of geometric fidelity to the original scene*



LaVR 的核心设计思路是将预训练 4D 重建模型 CUT3R 的隐式几何知识注入预训练视频扩散模型，从而在不依赖显式深度估计或点云渲染的条件下实现几何一致的新视角视频生成。系统由以下关键模块构成。

### 3.1 CUT3R 潜变量提取

CUT3R 是一种基于 ViT 的 4D 重建模型，在逐帧处理源视频时维护一组可学习的潜变量令牌（latent state tokens）。对于每一帧，ViT 编码的图像特征通过交叉注意力更新这些令牌，使其逐步积累场景的隐式几何与外观信息。

形式化地，每个时间步的潜变量令牌集合定义为：

$$\{ \ell ^ { i } \in \mathbb { R } ^ { d } \} _ { i = 1 } ^ { s }$$

其中 $s$ 为令牌数量，$d$ 为每个令牌的维度。对于长度为 $T$ 帧的源视频，完整的状态令牌集合为：

$$\mathcal { S } = \{ \{ \ell _ { t } ^ { i } \in \mathbb { R } ^ { d } \} _ { i = 1 } ^ { s } , t = 1 , 2 , \ldots , T \}$$

这些令牌 $\mathcal{S}$ 即为后续注入扩散模型的几何条件信号。与点云条件方法不同，CUT3R 的潜变量编码的是场景的隐式几何表征，而非显式的深度图或三维坐标，这使得系统对深度估计误差具有天然的鲁棒性。

### 3.2 CUT3R 适配器

CUT3R 输出的逐帧潜变量令牌在语义空间和形状上与视频 VAE 编码的潜变量不兼容，无法直接输入 DiT 骨干网络。为此，LaVR 设计了一个轻量级 CUT3R 适配器，将帧级令牌转换为与 VAE 潜变量对齐的几何感知空间特征。

适配器由两部分组成（Figure 4）：
- **MLP 投影层**：将每帧的 $s$ 个 $d$ 维令牌独立映射到与 VAE 潜变量通道数匹配的特征空间。
- **Query Transformer**：以 VAE 编码的视频潜变量作为查询，对投影后的 CUT3R 特征进行交叉注意力操作，生成最终的空间几何条件特征 $Z_c$。这一设计使得几何条件能够自适应地与视频内容对齐，而非简单的拼接或相加。

![[assets/figures/papers/paper_list_l2534_https_arxiv_org_abs_2601_14674/figures/004_Figure_4.jpg]]
*Figure 4: Proposed CUT3R Adapter. Our lightweight adapter embeds CUT3R’s per-frame latent tokens into geometry-aware features that align with the representation used by the diffusion model. The shape of features at each stage is shown in brackets*

适配器输出的 $Z_c$ 在空间维度上与 VAE 潜变量保持一致，可直接沿通道维度拼接后送入 DiT 进行去噪。

### 3.3 姿态注入与训练目标

除 CUT3R 潜变量条件外，LaVR 还通过两个独立的 MLP 适配器分别注入源相机姿态与目标相机路径姿态。源姿态来自 CUT3R 的估计结果，经 MLP 处理后加至 DiT 各层的中间激活；目标姿态同样经独立 MLP 处理后注入 DiT，为去噪过程提供目标视角的空间引导。

训练采用条件流匹配（Conditional Flow Matching）损失函数。给定干净视频潜变量 $z_0$、噪声 $\epsilon \sim \mathcal{N}(0, I)$ 和时间步 $t$ 构造的噪声潜变量 $z_t$，模型 $v_\theta$ 以 CUT3R 几何条件 $Z_c$ 和源姿态条件 $Z_s$ 为输入，预测速度场：

$$\mathcal { L } _ { \mathrm { F M } } = \mathbb { E } _ { t , z _ { 0 } , \epsilon } \left[ \| v _ { \theta } ( z _ { t } , t , Z _ { c } , Z _ { s } ) - ( \epsilon - z _ { 0 } ) \| _ { 2 } ^ { 2 } \right]$$

其中 $v_\theta(z_t, t, Z_c, Z_s)$ 为模型预测的速度向量，目标速度 $\epsilon - z_0$ 指向从噪声到干净数据的直线路径。该损失函数驱动模型学习在几何条件与姿态条件的约束下，将随机噪声逐步转化为与目标轨迹一致的视频潜变量。

### 3.4 训练策略

为保留预训练扩散模型的强大运动与场景先验，LaVR 采用高度受限的微调策略：
- **冻结模块**：Video VAE 的编码器与解码器、CUT3R 编码器、DiT 的多数参数均保持冻结。
- **可训练模块**：仅微调 DiT 的投影层与自注意力层；CUT3R 适配器与两个姿态 MLP 适配器从零开始训练。
- **差异化学习率**：CUT3R 适配器使用 3 倍于其他可训练参数的学习率，以加速几何条件信号的对齐。

这一策略确保模型在获得几何感知能力的同时，不会灾难性遗忘预训练阶段习得的视频生成先验。消融实验（Table 3）证实，CUT3R 潜变量条件是性能提升的主要驱动因素——移除该条件后，Cycle PSNR 从 20.74 骤降至 17.90，VBench Multi-View 从 17.11 降至 6.832；而姿态条件仅提供较小的额外增益。



## 实验与关键发现

### 核心瓶颈与因果机制

现有视频轨迹重渲染方法在几何一致性与视觉质量之间存在根本性权衡。**无几何条件方法**（如ReCamMaster）缺乏空间感知能力，在大视角变化下产生漂移和幻觉内容——例如Figure 8中台灯腿消失、纸箱在被遮挡后重新出现时变形；Figure 9中甚至出现“第三条手臂”的幻觉。**基于点云显式几何条件的方法**（如Gen3C、TrajectoryCrafter）虽然提供几何约束，但其效果高度依赖深度估计精度。如Figure 7所示，深度尺度模糊、经验估计的内参误差、点云中的空洞或未对齐问题，会生成扭曲的条件图像，进而导致渲染视图出现非自然拉伸伪影和细节缺失。

LaVR的核心因果机制在于：将预训练4D重建模型CUT3R的**隐式潜变量**作为软几何约束注入视频扩散模型，替代显式点云条件。这一设计的深层洞察是：大型4D重建模型的潜在空间蕴含丰富的隐式几何知识，当作为条件信号时，预训练视频扩散模型能够利用其强大的运动与场景先验来**校正小的几何不一致**，从而在不需要精确深度估计的情况下，同时实现高视觉质量和几何一致性。

### 主实验结果

#### 一致性评估

Table 1展示了各方法在循环一致性（Cycle Consistency）和VBench一致性指标上的量化对比。LaVR在循环一致性的三个指标上全面领先：PSNR达20.74（Gen3C为20.62），LPIPS降至22.47×10⁻²（Gen3C为23.23），CLIP得分98.07×10⁻²。在VBench评估中，LaVR取得多视角一致性（Multi-view）17.11、主体一致性（Subject）95.22、背景一致性（Background）97.21的最优结果。Figure 5的雷达图直观展示了这一全维度优势——LaVR在所有一致性指标上均无显著短板。

值得注意的是，基于点云条件的Gen3C虽然在循环一致性上接近LaVR（PSNR仅差0.12），但在视觉质量上存在明显差距。Figure 6的定性对比显示，Gen3C和TrajectoryCrafter均产生非自然扭曲伪影，而LaVR的生成结果更自然且几何上更一致。

#### 姿态重建精度

Table 2评估了各方法对目标相机轨迹的跟踪精度。LaVR在平移误差Abs(t)上取得14.39 mm，旋转误差Rel(R)仅0.411°，均优于所有基线方法。相比之下，无几何条件的ReCamMaster无法紧密跟踪目标轨迹，其平移和旋转误差显著更高。这表明CUT3R潜变量提供的隐式几何约束有效引导了生成视频的相机姿态精度。

### 消融实验：条件信号的贡献分解

Table 3的消融实验揭示了不同条件信号的贡献权重：

- **移除CUT3R潜变量条件**（仅保留源姿态条件）导致性能急剧下降：Cycle PSNR从20.74降至17.90，VBench Multi-View从17.11骤降至6.832，姿态误差显著上升。这证实CUT3R潜变量是性能提升的**主要驱动因素**。
- **源姿态条件**提供额外但较小的增益：完整模型相比无姿态条件配置，Cycle PSNR提升约0.5，姿态误差进一步降低。
- **完整模型**相比无几何条件且无姿态的基线（等价于ReCamMaster的设置），Cycle PSNR提升2.99（20.74 vs 17.75），姿态误差大幅降低，验证了整体设计的有效性。

### 失败模式与局限性

LaVR目前存在两个已知局限：

1. **透明/非朗伯体物体处理不足**：当场景中包含移动的透明物体（如被人拿起的玻璃杯）时，方法表现下降。这很可能源于CUT3R对此类场景的几何估计能力有限，导致潜变量条件信号质量下降。该问题指向4D重建模型在透明、反射等材质上的固有短板。

2. **额外计算开销**：CUT3R条件机制引入额外计算成本。虽然适配器设计已考虑轻量化（仅MLP+Query Transformer），但相比无条件或简单点云条件方法，仍存在效率差距。这为后续工作留下了模型蒸馏或更高效适配器设计的优化空间。

### 4D重建下游验证

Figure 10展示了将各方法生成的视频输入BA-Track进行4D重建后的点云可视化结果。LaVR生成的视频重建出的4D点云幻觉最少，从下游任务角度进一步验证了其几何一致性优势。这一实验设计巧妙地将生成质量评估与重建精度验证相结合，为几何一致性提供了独立于像素级指标的佐证。

### 补充图表

![[assets/figures/papers/paper_list_l2534_https_arxiv_org_abs_2601_14674/figures/007_Figure_6.jpg]]
*Figure 6: Qualitative evaluation of novel views. We compare frames from new camera trajectories rendered by redirecting the source video. Both Gen3C [26] and TrajectoryCrafter [46] are conditioned on re-rendered point clouds and suffer from unnatural warping artifacts. ReCamMaster [4] is not geometrically conditioned and hallucinates implausible content in unseen regions (top: man overlaps with table; middle: cat’s tail; bottom: haystacks in the background). Compared to baselines, our results look natural and geometrically consistent*

![[assets/figures/papers/paper_list_l2534_https_arxiv_org_abs_2601_14674/figures/005_Figure_5.jpg]]
*Figure 5: Evaluation on the VBench [14, 50] metrics. We highlight relative differences by normalizing each metric over all baselines. Our method shows all-around high performance, achieving the best results for multi-view, subject, and background consistency*

![[assets/figures/papers/paper_list_l2534_https_arxiv_org_abs_2601_14674/figures/008_Table_2.jpg]]
*Table 2: Target pose reconstruction accuracy. We evaluate the absolute Abs(·) and relative Rel(·) errors in camera translation t (in millimeters) and rotation R (in degrees). While we achieve consistently high rotational and translational accuracy, the unconditioned ReCamMaster [4] fails to follow the target trajectory closely. We highlight the metrics in blue, proportional to their percentile*

![[assets/figures/papers/paper_list_l2534_https_arxiv_org_abs_2601_14674/figures/009_Table_3.jpg]]
*Table 3: Effect of Source Pose Conditioning. Performance gains over baseline are predominantly driven by CUT3R conditioning, with source pose conditioning having a relatively minor impact*

![[assets/figures/papers/paper_list_l2534_https_arxiv_org_abs_2601_14674/figures/010_Figure_7.jpg]]
*Figure 7: Disadvantages of geometric conditioning via re-rendered point clouds. Visualizing the point cloud renders of TrajectoryCrafter, we see that depth scale ambiguity, empirically estimated intrinsics, and holes or misalignment errors in the point cloud can create warped conditioning images that lead to unnatural outputs. Our results do not suffer from such artifacts*


![[assets/figures/papers/paper_list_l2534_https_arxiv_org_abs_2601_14674/figures/012_Figure_9.jpg]]
*Figure 9: Qualitative evaluation of novel trajectories across frames. Baseline methods conditioned on re-rendered point clouds suffer from unnatural stretching artifacts and missing details (Row 1, Col. 4; Row 3, Col. 4). The unconditioned baseline hallucinates a third arm (Row 2, Col. 4). We avoid these pitfalls by using the latent state of a pretrained 4D reconstruction model as a soft geometric condition*

![[assets/figures/papers/paper_list_l2534_https_arxiv_org_abs_2601_14674/figures/013_Figure_10.jpg]]
*Figure 10: Qualitative Results on 4D Reconstruction. We run BA-Track [7] on re-rendered videos and visualize the 4D point clouds from a novel view. Ours has the the least amount of hallucination*



## 定位与知识库关联

### 核心瓶颈与设计动机

现有视频轨迹重渲染方法面临一个根本性的权衡困境：**几何一致性与视觉质量难以兼得**。无几何条件的方法（如 **ReCamMaster**，Bai et al., arXiv 2025）缺乏空间感知能力，在大视角变化下容易产生漂移、变形和幻觉内容；而基于点云渲染的显式几何条件方法（如 **Gen3C**，Ren et al., CVPR 2025；**TrajectoryCrafter**，Yu et al., ICCV 2025）虽然提供了几何约束，却高度依赖深度估计精度——深度尺度模糊、空洞、未对齐等误差会直接传导为渲染视图的形状扭曲、视差不一致和非自然伪影（Figure 7 揭示了这一因果链）。

LaVR 的核心洞察在于：**将预训练 4D 重建模型的隐式潜变量作为“软几何约束”注入视频扩散模型**，替代对精确深度估计的硬依赖。这一设计允许预训练视频扩散模型的强大运动与场景先验来“校正”小的几何不一致，从而在保持高视觉质量的同时实现几何一致性。

### 方法谱系定位

从几何条件范式来看，LaVR 开创了第三条路径，与现有两类方法形成清晰对比：

| 范式 | 代表方法 | 几何信号 | 优势 | 缺陷 |
|------|----------|----------|------|------|
| 无几何条件 | ReCamMaster (Bai et al., arXiv 2025) | 无 | 高视觉质量 | 空间感知缺失，大视角下产生幻觉 |
| 显式几何条件 | Gen3C (Ren et al., CVPR 2025), TrajectoryCrafter (Yu et al., ICCV 2025) | 点云渲染图像 | 几何一致性较好 | 深度估计误差导致扭曲伪影 |
| 隐式几何条件 | **LaVR (本文)** | CUT3R 潜变量令牌 | 视觉质量与几何一致性兼得 | 额外计算开销 |

LaVR 的技术路线可追溯到两条脉络：（1）**4D 重建模型的潜变量表征**——CUT3R 作为预训练大型 4D 重建模型，其潜变量令牌 $\{\ell^i \in \mathbb{R}^d\}_{i=1}^s$ 蕴含了场景的隐式几何知识，无需显式深度图或点云即可编码空间结构；（2）**扩散模型的适配器注入范式**——通过轻量级适配器（MLP + Query Transformer）将 CUT3R 令牌转换为与 VAE 潜变量对齐的空间几何特征，配合独立的源姿态和目标姿态 MLP 适配器注入 DiT 各层，实现了对冻结骨干网络的最小侵入式改造。

### 消融实验揭示的因果机制

消融实验（Table 3）清晰地揭示了各组件的贡献权重：
- **CUT3R 潜变量条件是性能提升的主要驱动因素**：移除后 Cycle PSNR 从 20.74 骤降至 17.90，VBench Multi-View 从 17.11 暴跌至 6.832，姿态误差显著上升。
- **源姿态条件仅提供额外的小幅增益**：完整模型相较于无几何条件且无姿态的基线（等价于 ReCamMaster 设置），Cycle PSNR 提升 2.99（20.74 vs 17.75），其中 CUT3R 潜变量贡献了绝大部分增益。
- 这一结果验证了核心假设：**隐式几何知识本身足以提供强约束，姿态信号更多扮演辅助对齐角色**。

### 适用边界与局限

LaVR 的适用边界受限于以下因素：

1. **透明/非朗伯体物体**：方法在包含移动透明物体（如被人拿起的玻璃杯）的场景中表现不佳，这很可能源于 CUT3R 对此类物体几何估计能力的固有限制。这是 4D 重建模型上游能力的瓶颈传导。

2. **计算开销**：CUT3R 条件机制引入了额外计算成本（模型参数量约 1.3B，在 8 张 H200 GPU 上训练 15K 迭代），相比纯无条件方法存在效率差距。

3. **训练数据依赖**：模型在 ReCamMaster 的合成数据集 MultiCamVideo 上训练，对真实场景的泛化能力需要进一步验证。

4. **长序列与大视角变化**：论文未系统评估在更长视频序列或更大视角变化下的性能退化情况，这仍是开放问题。

### 开放问题

- 能否通过改进上游 4D 重建模型或引入专门的透明物体处理模块，提升对非朗伯体物体的几何估计与生成一致性？
- 潜变量适配带来的额外计算开销能否通过模型蒸馏、适配器剪枝或更高效的设计进一步降低？
- 该方法在更长视频序列或更大视角变化下的泛化边界如何？是否存在潜变量漂移累积的问题？
- 隐式几何条件是否可推广到其他需要空间一致性的视频生成任务（如视频编辑、视角插值）？



## 原文 PDF

![[paperPDFs/CVPR_2026/LaVR_Scene_Latent_Conditioned_Generative_Video_Trajectory_Re_Rendering_using_Large_4D_Reconstruction_Models.pdf]]
