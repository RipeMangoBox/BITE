---
title: Taming Video Models for 3D and 4D Generation via Zero-Shot Camera Control
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Taming_Video_Models_for_3D_and_4D_Generation_via_Zero_Shot_Camera_Control.pdf
project_link: "https://worldforge-agi.github.io"
code_link: null
aliases:
- TVM34GZSCC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 在每个去噪步骤中，通过注入轨迹引导（IRR）并选择性更新运动相关潜在通道（FLF），同时利用双路径自校正引导（DSG）矫正因轨迹扭曲导致的伪影，从而在保留预训练先验的前提下实现精确的相机控制。
primary_logic: 通过光学流相似性识别和融合潜在空间中与运动高度相关的通道，解耦运动与外观，并利用引导路径与非引导路径之间的正交分量进行自适应校正，能够在无需任何重新训练的情况下平衡轨迹准确性与生成质量。
claims:
- IRR在每一个去噪步内部嵌入预测-校正循环，将观测区域替换为轨迹对应区域，实现细粒度轨迹注入。
- FLF通过光学流相似性得分识别并选择性更新高运动相关通道，通道8从不被过滤而通道13最常被过滤，证实了通道角色分化。
- DSG处理引导路径与非引导路径之间50°–70°的大角度差异，用正交分量代替直接CFG，消除严重伪影。
- 3D Static Scenes (LLFF, Tanks and Temples, MipNeRF 360, etc.) 上 FID = 96.08
---

# Taming Video Models for 3D and 4D Generation via Zero-Shot Camera Control

> [!tip] 核心洞察
> 通过光学流相似性识别和融合潜在空间中与运动高度相关的通道，解耦运动与外观，并利用引导路径与非引导路径之间的正交分量进行自适应校正，能够在无需任何重新训练的情况下平衡轨迹准确性与生成质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 驯服视频模型：通过零样本相机控制实现3D和4D生成 |
| 英文题名 | Taming Video Models for 3D and 4D Generation via Zero-Shot Camera Control |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.15130) · [Project](https://worldforge-agi.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | WorldForge |
| Dataset | 3D Static Scenes, 4D Dynamic Scenes |

> [!tip] 效果简介
> - 3D Static Scenes (LLFF, Tanks and Temples, MipNeRF 360, etc.) 上，FID 96.08 vs 123.26 (See3D) (-27.18)。
> - 3D Static Scenes 上，CLIP_sim 0.948 vs 0.941 (See3D) (+0.007)；ATE 0.077 vs 0.091 (See3D) (-0.014)；RPE-T 0.086 vs 0.089 (See3D) (-0.003)。
> - 4D Dynamic Scenes (DAVIS, movie clips, VDM generations) 上，FVD 93.17 vs N/A。

## 概要

现有视频扩散模型（Video Diffusion Models, VDMs）在生成动态内容方面展现出强大的时空先验，但当任务转向精确的三维场景重建与四维动态重渲染时，一个根本性瓶颈浮现：**模型缺乏对6-DoF相机轨迹的精确控制能力**。场景运动与相机运动高度纠缠，导致生成结果出现时空不一致、几何破碎和视觉伪影。已有的训练依赖方法（如**See3D**、**ViewCrafter**、**TrajectoryCrafter**）需要针对特定任务进行微调，代价高昂且泛化能力有限；而基于扭曲-修补（warp-and-inpaint）的训练自由方法（如**NVS-Solver**、**ViewExtrapolator**）对分布外输入敏感，容易引入噪声和结构失真。

本文提出 **WorldForge**，一个完全无需训练的框架，通过零样本相机控制驯服预训练视频扩散模型，使其能够同时胜任静态3D场景生成与动态4D场景重渲染。核心洞察在于：**通过光学流相似性识别并选择性融合潜在空间中与运动高度相关的通道，解耦运动与外观，并利用双路径引导的正交分量进行自适应校正，能够在无需任何重新训练的前提下，平衡轨迹准确性与生成质量**。

WorldForge 由三个关键模块构成：
- **Intra-Step Recursive Refinement (IRR)**：在每个去噪步骤内部嵌入微预测-校正循环，将观测区域的预测内容替换为轨迹对应区域，实现细粒度的轨迹注入。
- **Flow-Gated Latent Fusion (FLF)**：基于光流相似性得分和动态阈值，选择性更新高运动相关性通道，保留外观通道不受污染，从而实现运动与外观的解耦。
- **Dual-Path Self-Corrective Guidance (DSG)**：利用引导路径与非引导路径之间的正交差异进行自适应校正，处理两条路径间50°–70°的大角度差异，消除标准分类器自由引导（CFG）在此场景下产生的严重伪影。

实验结果表明，WorldForge 在多个基准上显著超越现有方法。在静态3D场景生成任务上，FID 降至 **96.08**（See3D 为 123.26），CLIP相似度达到 **0.948**，轨迹精度指标 ATE 降至 **0.077**。在动态4D场景重渲染任务上，FVD 达到 **93.17**，CLIP-V相似度为 **0.938**。消融实验验证了三个组件的互补性：移除 IRR 导致模型退化为无约束生成；移除 FLF 使运动噪声污染所有通道；移除 DSG 或用标准 CFG 替代则因大角度差异产生严重伪影。该框架具有良好的模型无关性，可无缝迁移至 **SVD**、**Wan 2.1**、**LongCat** 等不同架构的视频扩散模型。



### 问题域：视频扩散模型在空间任务中的相机控制困境

大规模预训练视频扩散模型（Video Diffusion Models, VDMs）在文本驱动的视频生成中展现出强大的时空先验，然而将其应用于3D场景生成、4D动态场景重渲染、新视角合成等空间任务时，面临一个根本性瓶颈：**缺乏精确的6自由度（6-DoF）相机轨迹控制能力**。现有模型在生成过程中，场景内容与相机运动高度纠缠——模型无法区分“物体自身运动”与“观测视角变化”，导致输出视频出现时空不一致、几何破碎和视觉伪影。

这一困境的根源在于：预训练视频扩散模型仅从海量视频数据中隐式学习运动模式，并未显式建模相机参数与场景几何之间的关系。当用户需要沿着指定轨迹（如环绕物体旋转、推拉镜头）生成新视角时，模型缺乏将轨迹约束注入生成过程的机制。

### 现有方法的局限

当前解决该问题的方案可归为三类，各自存在显著缺陷：

**训练依赖方法**（如See3D、ViewCrafter、ReCamMaster、TrajectoryCrafter）通过在特定数据集上微调或重新训练来嵌入相机控制能力。这类方法代价高昂——需要大量多视角标注数据和GPU算力，且泛化能力差：一旦切换到新的视频扩散模型骨干网络（如从SVD迁移到Wan 2.1），往往需要重新训练。

**训练自由的扭曲-修补方法**（如ViewExtrapolator、NVS-Solver）利用深度估计和相机姿态将源帧投影到目标视角，再通过修补网络填充缺失区域。这类方法对分布外输入极为敏感：当深度估计误差较大或相机运动幅度超出训练分布时，扭曲产生的引导帧含有大量噪声和几何破碎，修补网络难以有效修复，导致输出质量急剧下降。

**轨迹注意力方法**（如TrajectoryAttention）试图在注意力机制中直接注入相机轨迹编码，但仍需训练支持，且对复杂轨迹的控制精度有限。

### 核心科学问题

从控制论角度看，该问题的本质是：**如何在保留预训练视频扩散模型丰富时空先验的前提下，实现精确的、零样本的相机轨迹控制？** 这需要同时解决三个子问题：

1. **轨迹注入机制**：如何将外部指定的6-DoF相机轨迹转化为生成过程中的有效约束，而不破坏模型原有的去噪动力学？
2. **运动-外观解耦**：如何分离潜在空间中的运动相关通道与外观相关通道，使轨迹控制仅作用于前者，避免污染场景内容？
3. **伪影自校正**：当扭曲产生的引导帧含有噪声和几何误差时，如何利用模型先验自动纠正这些伪影，而非简单地将噪声传播到生成结果中？

### 本文动机与核心思路

WorldForge的提出正是为了系统性解决上述三个子问题。其核心洞察是：**通过光学流相似性识别潜在空间中与运动高度相关的通道，实现运动与外观的解耦；在此基础上，利用引导路径与非引导路径之间的正交分量进行自适应校正，能够在无需任何重新训练的情况下平衡轨迹准确性与生成质量。**

具体而言，WorldForge引入三个协同组件：**Intra-Step Recursive Refinement (IRR)** 在每个去噪步内嵌入微预测-校正循环，将观测区域的预测内容替换为轨迹对应区域，实现细粒度轨迹注入；**Flow-Gated Latent Fusion (FLF)** 通过光流相似性得分动态识别并选择性更新高运动相关性通道，保留外观通道不受污染；**Dual-Path Self-Corrective Guidance (DSG)** 利用引导路径与非引导路径之间的正交差异（通常50°–70°大角度差）进行自适应校正，消除因轨迹扭曲引入的伪影。三者协同，使WorldForge成为一个完全训练自由、模型无关的框架，可适配SVD、Wan 2.1、LongCat等多种视频扩散模型骨干网络。



## 核心方法与创新机理

WorldForge 的核心创新在于**无需任何重新训练或微调**，仅通过对预训练视频扩散模型去噪过程的三个关键“插槽”进行改造，便实现了对任意用户指定 6-DoF 相机轨迹的精确控制。这三个改造点分别解决了轨迹注入、运动-外观解耦以及引导伪影抑制三个递进瓶颈，共同构成了一个完整的零样本控制范式。

### 创新一：去噪步内的递归轨迹注入（IRR）

**改造插槽**：去噪中间变量更新方式。传统 DDIM 采样仅依赖网络预测的清洁估计 $\hat{\mathbf{x}}_0$ 进行下一步更新，完全不感知外部轨迹约束。IRR 在每个去噪步内部嵌入一个微预测-校正循环：先计算当前步的清洁估计，再将其与来自深度变形（Depth-based Warping）的轨迹潜变量 $\mathbf{x}_{\mathrm{traj}}$ 融合，最后重新加噪以重新进入去噪调度：

$$\mathbf{x}_t^{\prime} = \left(1 - w(\sigma)\right) \mathbf{F}(\hat{\mathbf{x}}_0^{(t)}, \mathbf{x}_{\mathrm{traj}}) + w(\sigma) \cdot \boldsymbol{\epsilon}$$

其中 $w(\sigma)$ 为噪声调度权重，$\mathbf{F}$ 为融合算子。这一改造使得轨迹信息以“逐步注入”的方式渗透进生成过程，而非一次性覆盖，从而在保持预训练先验的同时实现细粒度轨迹控制。消融实验证实，移除 IRR 后模型退化为纯文本到视频的自由生成，完全丧失轨迹跟随能力，且后续的 FLF 和 DSG 组件也无法应用（Table 3, Fig. 5）。

### 创新二：基于光流门控的潜在通道选择性融合（FLF）

**改造插槽**：潜在通道融合策略。基线方法（如直接全通道覆盖）将轨迹信息粗暴地写入所有潜在通道，导致运动与外观信息高度纠缠，产生噪声和几何破碎。FLF 的核心洞察是：**潜在空间中的不同通道对运动与外观的编码存在天然分化**。通过计算每个通道的光流相似性得分 $S^{(t,c)}$——该得分综合了 M-EPE、M-AE 和 Fl-all 三个归一化光流指标——FLF 可以动态识别高运动相关性通道：

$$S^{(t,c)} = \sum_{k \in \{ \mathrm{E}, \mathrm{A}, \mathrm{F} \}} \gamma_k \Big( 1 - \mathrm{Norm}_k^{(t,c)} \Big)$$

随后，FLF 依据动态阈值 $\delta^{(t)}$ 进行选择性融合：仅对得分高于阈值的通道写入轨迹信息，而保留低运动相关性通道（即外观通道）不变。这一机制等价于在潜在空间中解耦运动与外观，从根本上避免了轨迹噪声对外观质量的污染。统计证据（Fig. 4）强有力地支持了通道角色分化假说：通道 8 从未被过滤（高运动相关性），而通道 13 最常被过滤（低运动相关性），且这一模式在 40+ 静态场景和 30+ 动态场景中保持稳定。消融实验表明，移除 FLF 导致运动/外观分离失败，输出质量大幅下降（Table 3, Fig. 5）。

### 创新三：双路径自校正引导（DSG）

**改造插槽**：引导方式。标准分类器自由引导（CFG）假设条件预测与无条件预测之间的角度差异较小，适用于文本到图像的语义引导。然而，在轨迹控制场景中，引导路径（遵循变形轨迹）与非引导路径（依赖模型先验的自由生成）之间的速度场角度差异可达 50°–70°，直接套用 CFG 会产生严重的结构伪影和视觉错误（Fig. 1 supplementary）。DSG 通过引入正交分量校正来解决这一问题：

$$\mathbf{v}_t^{\mathrm{corr}} = \mathbf{v}_t^{\mathrm{traj}} + \rho \cdot \beta_t \big( \mathbf{v}_t^{\mathrm{traj}} - \alpha_t \cdot \mathbf{v}_t^{\mathrm{ori}} \big)$$

其中 $\beta_t$ 为基于两路径夹角正弦的自适应权重，$\alpha_t$ 为投影系数。DSG 的核心机制是：利用引导路径与非引导路径的差异中与引导方向正交的分量，对引导路径进行“自校正”，使其在保持轨迹精度的同时向高视觉质量的非引导路径靠拢。消融实验证实，移除 DSG 或替换为标准 CFG 均导致严重伪影和结构破损（Table 3, Fig. 5, Fig. 1 supplementary）。

### 创新协同与范式意义

三个改造点形成递进依赖关系：IRR 提供轨迹注入的基础设施，FLF 在注入过程中实现运动-外观解耦以保护视觉质量，DSG 则在采样层面进一步矫正因轨迹变形引入的伪影。这种“注入-解耦-矫正”的三阶段设计使得 WorldForge 成为**完全训练自由且模型无关**的框架——它不需要任何相机标注数据进行微调，可直接适配 SVD、Wan 2.1、LongCat 等多种视频扩散骨干网络（Fig. 6, Table 4 supplementary），在 3D 静态场景生成（FID 96.08 vs. See3D 123.26）和 4D 动态场景重渲染（FVD 93.17）上均取得最优结果。



WorldForge 是一个完全无需训练的框架，其核心思想是将预训练视频扩散模型（VDM）的丰富时空先验“驯服”为精确的相机轨迹控制，从而实现高质量的 3D 场景生成与 4D 动态场景重渲染。整个 pipeline 由三个关键模块串联构成：**Intra-Step Recursive Refinement (IRR)**、**Flow-Gated Latent Fusion (FLF)** 和 **Dual-Path Self-Corrective Guidance (DSG)**。它们共同解决了一个核心瓶颈——如何在保留预训练模型视觉质量的前提下，将精确的 6-DoF 相机轨迹约束注入到生成过程中，同时抑制因深度估计误差和扭曲操作引入的视觉伪影。

### 输入输出流与模块关系

框架的输入可以是一张单图或一段视频的第一帧，以及用户指定的相机轨迹。处理流程如下（参见 Figure 2）：

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/002_Figure_2.jpg]]
*Figure 2: Overview of WorldForge. Given a single image or video frames, a vision foundation model reconstructs a scene point cloud, which is warped and rendered along a user-specified trajectory to produce a guidance video. The input image (or first frame) is also converted into a textual prompt and latent representation for an image-to-video diffusion model. Trajectory control is injected through a training-free strategy comprising IRR, FLF, and DSG (detailed in Sec. 3.2–3.4), enabling precise control and high-quality synthesis without additional training*

1. **视觉基础模型预处理**：首先利用深度/姿态估计网络（兼容 VGGT、UniDepth、Mega-SaM、DepthCrafter 等多种选择）从输入图像或视频帧中重建场景的点云，并估计相机姿态与深度图。随后，一个基于深度的扭曲算子 $\mathcal{W}$ 将源帧沿用户指定的目标轨迹进行投影，生成部分可见的引导帧序列与对应的有效性掩码。这一步骤为后续的轨迹注入提供了“地面真值”式的空间约束，但其质量受限于深度估计的精度。

2. **图像到视频扩散模型编码**：输入图像（或视频首帧）同时被转换为文本提示和潜在表示，送入预训练的 I2V 扩散模型（如 Wan 2.1、SVD）作为生成的起点。模型自身的去噪过程在 DDIM 采样框架下进行，每一步都会产生一个清洁估计 $\hat{\mathbf{x}}_0(\mathbf{x}_t, t)$。

3. **IRR：步内递归细化**：IRR 在每个去噪步内部嵌入一个微预测-校正循环。具体而言，它将当前步的清洁估计 $\hat{\mathbf{x}}_0^{(t)}$ 与轨迹潜变量 $\mathbf{x}_{\mathrm{traj}}$ 通过融合函数 $\mathbf{F}$ 进行混合，然后重新加噪：

   $$\mathbf{x}_t^{\prime} = \left(1 - w(\sigma)\right) \mathbf{F}(\hat{\mathbf{x}}_0^{(t)}, \mathbf{x}_{\mathrm{traj}}) + w(\sigma) \cdot \boldsymbol{\epsilon}$$

   这一操作将轨迹约束“注入”到去噪中间状态，使模型在后续采样步中能够持续遵循目标路径。IRR 仅在去噪过程的前约 35–45% 步中应用（例如 Wan 2.1 使用 UniPC 采样器 50 步时，IRR 作用于前 20 步），以在早期建立轨迹骨架，同时为后期细节生成留出自由度。

4. **FLF：光流门控潜在融合**：IRR 中的融合函数 $\mathbf{F}$ 在 FLF 中被替换为更精细的通道选择性更新机制。FLF 通过计算每个潜在通道的光流相似性得分 $S^{(t,c)}$（基于 M-EPE、M-AE 和 Fl-all 三个归一化指标的加权和），识别出与运动高度相关的通道，并仅对这些通道进行轨迹信息融合：

   $$\mathbf{FLF}(\hat{\mathbf{x}}_0^{(t)}, \mathbf{x}_{\mathrm{traj}}) = \begin{cases} \mathbf{M}^{(c)} \mathbf{x}_{\mathrm{traj}}^{(c)} + \big(1 - \mathbf{M}^{(c)}\big) \hat{\mathbf{x}}_0^{(t,c)}, & \text{if } S^{(t,c)} \geq \delta^{(t)} \\ \hat{\mathbf{x}}_0^{(t,c)}, & \text{otherwise} \end{cases}$$

   这一设计解耦了运动与外观——高运动相关性通道（如通道 8，从未被过滤）承载轨迹控制信号，而低运动相关性通道（如通道 13，最常被过滤）保留模型的原始外观先验。动态阈值 $\delta^{(t)}$ 使得框架在深度估计不稳定时自动放宽约束，确保输出不会比无引导生成更差。

5. **DSG：双路径自校正引导**：由于扭曲操作引入的轨迹引导路径与模型自身的非引导路径之间存在较大的角度差异（50°–70°），直接使用标准分类器自由引导（CFG）会产生严重伪影。DSG 通过计算两条路径速度场的正交分量进行自适应校正：

   $$\mathbf{v}_t^{\mathrm{corr}} = \mathbf{v}_t^{\mathrm{traj}} + \rho \cdot \beta_t \big( \mathbf{v}_t^{\mathrm{traj}} - \alpha_t \cdot \mathbf{v}_t^{\mathrm{ori}} \big)$$

   其中自适应权重 $\beta_t$ 基于两条路径速度场夹角的正弦值动态调节，使得校正强度与路径分歧程度成正比。这一机制在保证轨迹精度的同时，有效抑制了扭曲伪影，维持了高视觉保真度。

### 因果机制总结

三个模块形成了一条清晰的因果链：**IRR** 提供了轨迹注入的基础机制，使模型在去噪过程中持续受到空间约束；**FLF** 通过通道选择性融合解决了全通道更新带来的外观退化问题，实现了运动与外观的解耦；**DSG** 则在引导层面矫正了因轨迹扭曲引入的噪声，用正交分量替代直接 CFG，处理了引导路径与非引导路径之间的大角度差异。三者协同作用，使得 WorldForge 能够在零样本、无训练的条件下，将预训练视频扩散模型转化为精确的 3D/4D 生成引擎。

### 补充图表

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/019_Figure_7.jpg]]
*Figure 7: Robustness in challenging scenarios. Our framework maintains structural integrity even under fast motion and complex occlusions*



WorldForge 在预训练视频扩散模型的去噪过程中嵌入三个训练自由的轨迹控制模块，构成一个从粗到精的注入–解耦–校正管线。

### 3.1 轨迹潜变量构建

给定源图像 $\mathbf{I}_{src}$ 及其估计深度图 $\mathbf{D}_{src}$，视觉基础模型（深度/姿态估计网络）重建场景点云并估计相机姿态。对于用户指定的目标轨迹 $\{\mathbf{P}_{tar}\}$，扭曲算子 $\mathcal{W}$ 将源帧投影到每个目标视角：

$$(\mathbf{I}_{tar}^{\prime}, \mathbf{M}_{tar}) = \mathcal{W}(\mathbf{I}_{src}, \mathbf{D}_{src}, \mathbf{P}_{src}, \mathbf{P}_{tar})$$

其中 $\mathbf{I}_{tar}^{\prime}$ 为部分可见的目标视图，$\mathbf{M}_{tar}$ 为有效区域掩码。该扭曲视频经VAE编码后与对应掩码共同构成轨迹潜变量 $\mathbf{x}_{traj}$，作为后续控制的观测信号。

### 3.2 步内递归精炼（IRR）

IRR 在每个去噪步内部嵌入一个微预测–校正循环，将轨迹约束注入去噪中间变量。首先，利用DDIM一步去噪估计从当前噪声状态 $\mathbf{x}_t$ 恢复清洁估计：

$$\hat{\mathbf{x}}_0(\mathbf{x}_t, t) = \frac{\mathbf{x}_t - \sqrt{1 - \bar{\alpha}_t} \epsilon_\theta(\mathbf{x}_t, t)}{\sqrt{\bar{\alpha}_t}} \tag{1}$$

随后，IRR 将该清洁估计与轨迹潜变量融合并重新加噪，使下一步采样携带轨迹信息：

$$\mathbf{x}_t^{\prime} = \left(1 - w(\sigma)\right) \mathbf{F}(\hat{\mathbf{x}}_0^{(t)}, \mathbf{x}_{\mathrm{traj}}) + w(\sigma) \cdot \boldsymbol{\epsilon} \tag{5}$$

其中 $\mathbf{F}$ 为融合算子（初始为直接替换有效区域），$w(\sigma)$ 为噪声调度权重，$\boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I})$。这一预测–校正循环确保每个去噪步的中间变量始终锚定在轨迹约束上。IRR 通常作用于前 35%–45% 的去噪步（例如 UniPC 50 步采样中的前 20 步），在早期建立轨迹骨架后交由模型先验完成细节生成。

### 3.3 流控门潜变量融合（FLF）

直接替换所有通道会破坏预训练模型的外观先验，导致内容漂移。FLF 通过光流相似性识别潜在空间中与运动高度相关的通道，实现选择性注入。

首先计算每个潜在通道 $c$ 在时间步 $t$ 的运动相似性得分：

$$S^{(t,c)} = \sum_{k \in \{\mathrm{E}, \mathrm{A}, \mathrm{F}\}} \gamma_k \Big( 1 - \mathrm{Norm}_k^{(t,c)} \Big) \tag{6}$$

其中 $\mathrm{E}$、$\mathrm{A}$、$\mathrm{F}$ 分别为光流的端点误差（M-EPE）、角度误差（M-AE）和Fl-all指标的归一化值，$\gamma_k$ 为加权系数。得分越高，通道与运动的相关性越强。

基于动态阈值 $\delta^{(t)}$，FLF 选择性融合轨迹信息：

$$\mathbf{FLF}(\hat{\mathbf{x}}_0^{(t)}, \mathbf{x}_{\mathrm{traj}}) = \begin{cases} \mathbf{M}^{(c)} \mathbf{x}_{\mathrm{traj}}^{(c)} + \big(1 - \mathbf{M}^{(c)}\big) \hat{\mathbf{x}}_0^{(t,c)}, & \text{if } S^{(t,c)} \geq \delta^{(t)} \\ \hat{\mathbf{x}}_0^{(t,c)}, & \text{otherwise} \end{cases} \tag{7}$$

关键证据：在 40+ 静态场景和 30+ 动态场景的统计中，通道 13 最常被过滤（运动相关性低），而通道 8 从未被过滤（运动相关性高），证实了潜在通道的角色分化（Figure 4）。4D 动态场景的得分分布比 3D 场景更为分散，反映了更高的运动复杂度。

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/004_Figure_4.jpg]]
*Figure 4: FLF channel-wise flow statistics. The Y-axis shows filtering frequency; a “filtered out” channel has a low optical flow score (poor motion correlation). Statistics were gathered by tracking indices at each step across 40+ static and 30+ dynamic scenes. The results confirm distinct, stable roles: channel 13 is most frequently filtered out (low motion relevance), while channel 8 is never filtered out (high motion relevance). 4D dynamic scenes show more diverse scores than 3D scenes, reflecting greater motion complexity. This validates our selective guidance approach*

### 3.4 双路径自校正引导（DSG）

扭曲轨迹不可避免地引入噪声和伪影，直接使用标准分类器自由引导（CFG）会因引导路径与非引导路径之间 50°–70° 的大角度差异而产生严重伪影。DSG 利用两条并行去噪路径的正交分量进行自适应校正。

在每一步，DSG 同时运行一条依赖模型先验的非引导路径（速度场 $\mathbf{v}_t^{\mathrm{ori}}$）和一条遵循扭曲轨迹的引导路径（速度场 $\mathbf{v}_t^{\mathrm{traj}}$），并计算校正后的速度：

$$\mathbf{v}_t^{\mathrm{corr}} = \mathbf{v}_t^{\mathrm{traj}} + \rho \cdot \beta_t \big( \mathbf{v}_t^{\mathrm{traj}} - \alpha_t \cdot \mathbf{v}_t^{\mathrm{ori}} \big) \tag{8}$$

其中 $\alpha_t = \frac{\langle \mathbf{v}_t^{\mathrm{traj}}, \mathbf{v}_t^{\mathrm{ori}} \rangle}{\|\mathbf{v}_t^{\mathrm{ori}}\|^2}$ 为投影系数，$\beta_t$ 为基于两速度场夹角正弦的自适应权重，$\rho$ 为全局引导强度。该公式提取引导路径中与非引导路径正交的分量进行校正，在保持轨迹精度的同时抑制扭曲引入的噪声。

消融实验证实：移除 DSG 或替换为标准 CFG 均导致显著伪影和结构破损（Figure 5, supplementary Figure 1）；移除自适应权重 $\beta_t$ 则破坏引导稳定性。

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/016_Figure_5.jpg]]
*Figure 5: Large camera movements (e.g., 180◦). Single-pass generation of large angles often suffers from poor quality. Our method effectively resolves this problem via iterative generation*



## 实验与关键发现

### 评估设置与公平性说明

实验覆盖静态3D场景与动态4D场景两大任务。3D场景生成以单张RGB图像为输入，在LLFF、Tanks and Temples、MipNeRF 360等基准上评估；4D动态场景重渲染以DAVIS、电影片段及VDM生成视频为输入。由于静态场景缺乏真实多视图监督，不使用PSNR等重建指标，而是采用**FID**和**CLIP相似度**衡量生成质量；轨迹精度统一采用**ATE**、**RPE-T**、**RPE-R**三项指标。所有对比方法均使用官方代码与相同输入，确保公平性。

### 静态3D场景生成

Table 1给出了3D静态场景上的定量对比。WorldForge在生成质量与轨迹精度上均取得最优：

- **FID**达到96.08，相比See3D的123.26降低27.18，表明生成分布更接近真实场景。
- **CLIP相似度**为0.948，略高于See3D的0.941，语义一致性更好。
- 轨迹精度方面，**ATE**从0.091降至0.077，**RPE-R**从0.250降至0.221，相机姿态控制更精确。

这一优势源于IRR在每个去噪步内嵌入的预测-校正循环：将一步去噪估计$\hat{\mathbf{x}}_0^{(t)}$与轨迹潜变量$\mathbf{x}_{\mathrm{traj}}$融合后重新加噪，使得轨迹约束被持续注入生成过程，而非仅在初始条件中体现。

### 动态4D场景重渲染

Table 2展示了4D动态场景的结果。WorldForge在无任何训练的条件下，**FVD**为93.17，**CLIP-V相似度**为0.938，验证了框架对动态内容的泛化能力。值得注意的是，4D场景中光流相似性得分分布比3D场景更分散（Figure 4），反映更高的运动复杂度，而FLF的动态阈值机制$\delta^{(t)}$能够自适应调整通道选择，在运动剧烈时自动放宽约束，避免因过度注入轨迹噪声导致质量退化。

### 核心组件消融

Figure 5和Table 3系统验证了三个核心组件的必要性：

**移除IRR**：模型退化为纯文本到视频生成，完全无法遵循目标轨迹。IRR是轨迹注入的基础载体——它在每个去噪步内将观测区域替换为轨迹对应区域，形成微预测-校正循环；没有IRR，FLF和DSG均无法接入生成管线。

**移除FLF**：运动与外观的通道解耦失效，扭曲帧中的噪声污染所有潜在通道，输出出现不自然的纹理漂移和几何破碎。FLF通过光流相似性得分$S^{(t,c)}$识别高运动相关性通道（如通道8从不被过滤），仅对这些通道进行选择性更新，保留外观相关通道的预训练先验，是质量保真的关键。

**移除DSG或替换为标准CFG**：引导路径与非引导路径之间存在50°–70°的大角度差异，标准CFG针对的是条件预测与无条件预测之间的小角度差，在此场景下完全失效，产生严重的视觉伪影和结构错误。DSG利用正交分量$\mathbf{v}_t^{\mathrm{traj}} - \alpha_t \cdot \mathbf{v}_t^{\mathrm{ori}}$进行自适应校正，并通过基于夹角正弦的自适应权重$\beta_t$调节校正强度，能够在轨迹准确性与视觉保真度之间取得平衡。

### 骨干网络迁移性

Figure 6和Table 4验证了WorldForge的模型无关性。方法成功移植到基于U-Net的**SVD**、基于DiT的**Wan 2.1**以及**LongCat-Video**三种架构，均取得有竞争力的结果。这表明IRR-FLF-DSG的引导策略不依赖特定骨干网络的内部表示，而是通过统一的潜变量操作实现轨迹控制。

### 推理效率

Table 3给出了单步计算代价分解。以NVIDIA A100生成832×480分辨率、49帧视频为例，主要开销来自IRR模块的迭代融合与重加噪，DSG模块代价可忽略。默认仅在前20个采样步（约35-45%的去噪过程）施加引导，后续步骤依赖模型先验完成细节生成，在控制精度与推理速度之间取得折中。与训练依赖方法相比，WorldForge完全免除了训练开销，部署成本显著降低。

### 失败模式与深度估计鲁棒性

框架性能受底层深度估计质量制约。在极端动态场景或深度估计严重错误的区域，扭曲帧可能引入结构性失真。然而，Figure 2（supplementary）的深度模型消融表明，视频扩散模型的内在世界知识具有自校正能力——即使输入深度存在明显噪声或缺失区域，模型先验仍能补偿并生成合理结果。此外，FLF的动态门控机制在深度估计不稳定时自动降低通道约束强度，确保输出质量不低于未使用FLF引导的基线。Figure 9展示的失败案例主要集中在深度估计完全失效的复杂遮挡场景，此时光流估计和轨迹指导的可靠性均下降，需要手动验证具体退化模式。

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/011_Figure_2.jpg]]
*Figure 2: Depth-models ablation. Our method leverages the inherent world knowledge of VDMs to correct errors and fill missing regions even under challenging inputs (left). This strong self-correction ability ensures broad compatibility with different depth estimators (right). Despite variations or noise in depth-based warping, it reliably compensates through learned priors and produces realistic, high-quality results*

### 待验证与开放问题

- 论文未报告4D场景的轨迹精度数值（ATE/RPE-T/RPE-R），仅给出FVD和CLIP-V相似度，需要确认补充材料中是否包含完整指标。
- 推理速度虽可接受，但实时生成仍有挑战——IRR的迭代特性使得单步延迟较高，能否通过蒸馏或少步采样缓解需要进一步探索。
- 在DiT架构上的通道选择统计（类似Figure 4）尚未提供，FLF的通道角色分化是否具有跨架构一致性有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparison with existing methods on 3D static scenes. We evaluate generation quality (FID*

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/008_Figure_5.jpg]]
*Figure 5: Ablation of the proposed components. IRR enables trajectory injection; without it, the model defaults to prompt-only free generation, and FLF/DSG cannot be applied. FLF decouples trajectory cues from noisy content; removing it introduces noise from warped frames. DSG guides sampling toward highquality, trajectory-consistent results; without it, detail and plausibility drop. If the standard CFG formulation is applied in DSG, the large angular difference between the two velocity fields causes severe artifacts and errors. The full model achieves the best fidelity and control, demonstrating their complementary effects*

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/007_Figure_6.jpg]]
*Figure 6: Ablation across different VDMs. To verify our method’s transferability, we port it to the U-Net–based SVD model [8] and compare it against other SVD-based methods. Our guidance achieves excellent results on native SVD. Furthermore, we applied our method to the recent LongCat-Video [70] model. Leveraging its rich world priors, our method again achieves SOTA results*

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/010_Figure_1.jpg]]
*Figure 1: Qualitative ablation study of the DSG method. Substituting DSG with a standard CFG formulation fails to handle the large angular disparity between the two velocity fields, resulting in significant visual artifacts and errors. Removing the adaptive weighting factor*

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/013_Table_3.jpg]]
*Table 3: Computational cost breakdown of a single generation step. We report the runtime of each component on an NVIDIA A100, taking the generation of a 49-frame video at 832 × 480 resolution as an example. By default, we apply our guidance during the first 20 sampling steps. The primary overhead comes from the IRR module, while the DSG module incurs negligible cost*

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/015_Table_4.jpg]]
*Table 4: Quantitative comparison across different backbones. Using single-view 3D scene generation as a benchmark, we evaluate our method on SVD [8], Wan 2.1 [75], and LongCat [70]. The results demonstrate the scalability of our approach and its ability to generalize across different VDM architectures. Furthermore, the performance gains on advanced backbones indicate that our method effectively leverages the capabilities of the underlying model, promising improved generation quality as base models continue to evolve*

![[assets/figures/papers/paper_list_l2607_https_arxiv_org_abs_2509_15130/figures/009_Table_1.jpg]]
*Table 1: Default coefficient settings used in our experiments (taking Wan 2.1 implementation as an example). While these values serve as a robust baseline, users can fine-tune them for specific scenes to maximize generation quality*



## 定位与知识库关联

### 与基线方法的关系

WorldForge 的核心贡献在于**完全无需训练**的条件下，将预训练视频扩散模型（VDM）改造为可精确控制6-DoF相机轨迹的3D/4D生成引擎。这一设计使其在方法谱系中占据独特位置，与现有工作形成以下关系：

**训练依赖的3D场景生成方法**（如 **See3D**、**ViewCrafter**、**TrajectoryAttention**、**TrajectoryCrafter**、**ReCamMaster**）通常需要在大规模多视图或视频数据上进行微调或从头训练，以嵌入相机控制能力。WorldForge 避免了这一训练代价，直接利用预训练VDM的时空先验，在零样本条件下即可达到甚至超越这些方法的生成质量（Table 1：FID 96.08 vs See3D 123.26；CLIP_sim 0.948 vs 0.941）。其关键优势在于：IRR模块在每个去噪步内构建微预测-校正循环，将轨迹约束注入潜在空间，而无需修改模型权重。

**训练自由的视角合成方法**（如 **NVS-Solver**、**ViewExtrapolator**）同样避免了训练，但通常依赖基于扭曲-修补（warp-and-inpaint）的范式。这类方法对分布外输入敏感，在深度估计误差或大视角变化下容易产生噪声和几何破碎。WorldForge 通过 FLF 和 DSG 两个模块系统性地解决了这一问题：FLF 利用光流相似性得分选择性更新运动相关通道，避免扭曲噪声污染外观通道；DSG 则通过引导路径与非引导路径的正交分量进行自适应校正，处理两路径间50°–70°的大角度差异（supplementary Figure 1），这是标准CFG无法应对的。

### 技术继承与创新

WorldForge 的技术路线继承自以下几条研究脉络：

1. **DDIM采样与清洁估计**：框架基于DDIM的一步去噪估计公式（Eq. 1）构建，这是扩散模型引导方法的标准起点。IRR 的创新在于将这一清洁估计与轨迹潜变量融合后重新加噪（Eq. 5），在去噪调度中嵌入轨迹约束。

2. **深度扭曲与视角投影**：利用视觉基础模型估计深度图和相机姿态，通过扭曲算子（Eq. 3）将源帧投影到目标轨迹。这一思路与 NVS-Solver 等训练自由方法共享，但 WorldForge 的创新在于不直接使用扭曲结果作为生成目标，而是将其作为扩散过程中的引导信号。

3. **分类器自由引导（CFG）**：DSG 在概念上继承了 CFG 的双路径设计，但针对轨迹引导场景中引导路径与非引导路径之间的大角度差异（50°–70°）进行了根本性改造。标准 CFG 假设两路径的梯度方向接近，而 DSG 利用正交分量和基于夹角正弦的自适应权重 $\beta_t$（Eq. 8），在轨迹准确性与生成质量之间实现平衡。

### 适用边界与局限

WorldForge 的适用边界由以下因素决定：

1. **深度估计质量依赖**：框架的性能受底层深度估计算法制约。在极端动态场景或深度估计严重错误的情况下，扭曲生成的引导帧可能包含结构失真。论文通过消融实验（supplementary Figure 2）表明，VDM 的预训练先验具有一定自校正能力，可补偿部分深度误差，但这一能力的上限尚未量化。需要手动验证的是：在深度完全失效的退化场景（如透明物体、镜面反射）中，框架的鲁棒性边界。

2. **动态场景的复杂性限制**：FLF 的通道选择统计（Figure 4）显示，4D动态场景的得分分布比3D静态场景更分散，反映运动复杂性的增加。对于快速非刚体运动和严重遮挡场景，光流估计和轨迹指导的可靠性会下降。论文未提供此类极端场景的定量分析。

3. **推理效率**：尽管 WorldForge 避免了训练开销，但 IRR 模块在每个去噪步内引入额外的融合和加噪操作，是推理时间的主要开销来源（supplementary Table 3）。在 Wan 2.1 + UniPC 采样器（50步）配置下，IRR 应用于前约20步，实时生成仍有挑战。

### 开放问题

1. **显式相机姿态编码**：当前框架完全依赖深度扭曲生成的引导帧来隐式传递轨迹信息。引入显式的相机姿态编码或语义先验，可能从根本上解决深度失败时的模糊性问题，并提升对复杂轨迹的泛化能力。

2. **蒸馏与实时生成**：能否将该无训练引导框架蒸馏为少步采样模型，在保持轨迹控制精度的同时实现高分辨率视频的实时生成？这是从研究原型走向实际应用的关键一步。

3. **架构迁移性**：论文已在 U-Net 架构（SVD）和 DiT 架构（Wan 2.1、LongCat）上验证了迁移性（Figure 6, supplementary Table 4），但在其他视频扩散架构（如 CogVideoX）上的潜力仍需进一步探索。

4. **多模态条件扩展**：当前框架的输入为单图或视频帧加轨迹。能否扩展至多模态条件（如文本+轨迹联合控制）或更复杂的物理世界模拟（如刚体运动、流体动力学），是值得探索的方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Taming_Video_Models_for_3D_and_4D_Generation_via_Zero_Shot_Camera_Control.pdf]]
