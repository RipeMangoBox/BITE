---
title: "ReVision: High-Quality, Low-Cost Video Generation with Explicit 3D Physics Modeling for Complex Motion and Interaction"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/ReVision_High_Quality_Low_Cost_Video_Generation_with_Explicit_3D_Physics_Modeling_for_Complex_Motion_and_Interaction.pdf
project_link: https://revision-video.github.io/
code_link: null
aliases:
- ReVision
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过从粗生成视频中提取参数化3D运动序列，并利用参数化运动先验模型（PMP）对其进行优化，再作为额外条件反馈至视频扩散模型，从而控制运动一致性和物理真实性。
primary_logic: 三阶段“提取‑优化‑强化”流水线：首先生成粗视频以获取蕴含丰富运动模式的草稿；接着用参数化3D模型表示对象（如SMPL‑X、SMAL、点云），并通过轻量级Transformer去噪优化运动序列；最后将优化后的完整运动序列注入同一扩散模型，实现“自我修正”式的高质量视频再生。
claims:
- 在VBench++上，ReVision-SVD将动态程度（Dynamic Degree）从43.17%大幅提升至83.15%，ReVision-Wan2.1从51.38%提升至73.67%，且其他一致性、流畅性指标保持或提升。
- 用户偏好研究中，仅1.5B参数的ReVision-SVD在运动一致性、运动量和运动真实性上显著超过13B参数的HunyuanVideo。
- 参数化运动先验模型（PMP）的引入使对象一致性从83.0提升至87.6，运动一致性从94.1提升至96.0，同时将形态学失败率从27.1%降至14.3%。
- 舞蹈生成任务上，ReVision（含完整运动序列条件）在所有指标（SSIM、PSNR、LPIPS、FVD）上超越依赖真实姿态序列的人类图像动画方法。
---

# ReVision: High-Quality, Low-Cost Video Generation with Explicit 3D Physics Modeling for Complex Motion and Interaction

> [!tip] 核心洞察
> 三阶段“提取‑优化‑强化”流水线：首先生成粗视频以获取蕴含丰富运动模式的草稿；接着用参数化3D模型表示对象（如SMPL‑X、SMAL、点云），并通过轻量级Transformer去噪优化运动序列；最后将优化后的完整运动序列注入同一扩散模型，实现“自我修正”式的高质量视频再生。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReVision：通过显式3D物理建模实现高质量低成本复杂运动与交互视频生成 |
| 英文题名 | ReVision: High-Quality, Low-Cost Video Generation with Explicit 3D Physics Modeling for Complex Motion and Interaction |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2504.21855) · [Project](https://revision-video.github.io/) · [paper](https://arxiv.org/abs/2410) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | ReVision |
| Dataset | VBench++, DAVIS, Dance generation |

> [!tip] 效果简介
> - VBench++ 上，Dynamic Degree 83.15% vs 43.17% (+39.98%)；Subject Consistency 96.13% vs 95.42% (+0.71%)；Motion Smoothness 98.88% vs 98.12% (+0.76%)。
> - DAVIS (motion transfer) 上，CoTracker mIoU 0.80 vs 0.74 (+0.06)；Optical Flow Error 0.33 vs 0.36 (-0.03)。
> - Dance generation (TikTok dataset) 上，SSIM / PSNR / LPIPS / FVD 0.864 / 30.08 / 0.210 / 121.26 (w/ full motion) vs VividPose: 0.758 / 29.83 / 0.261 / … (所有指标均最优)。

## 概要

**问题瓶颈**：预训练视频扩散模型（如 Stable Video Diffusion、Wan2.1 等）缺乏显式的三维运动先验，难以生成符合物理规律的复杂肢体动作与物体交互。即使将模型规模扩展至 13B 参数（如 HunyuanVideo），仍无法可靠捕获真实世界的动态复杂性——在 VBench++ 基准上，基础模型的动态程度（Dynamic Degree）仅 43.17%–51.38%，暴露出运动生成能力的根本性不足。

**核心思路**：ReVision 提出一条“提取–优化–强化”（Extract–Optimize–Reinforce）的三阶段流水线，让预训练视频扩散模型通过“自我修正”的方式提升运动质量。其关键因果机制在于：先从粗生成视频中恢复参数化 3D 运动序列，再利用参数化运动先验模型（Parameterized Motion Prior，PMP）对这些序列进行去噪与精炼，最后将优化后的完整运动序列作为强条件反馈至同一扩散模型，实现高质量视频再生。

**主要结论**：
- 在 VBench++ 上，ReVision-SVD 将动态程度从 43.17% 大幅提升至 **83.15%**，ReVision-Wan2.1 从 51.38% 提升至 **73.67%**，同时主体一致性、运动流畅性等指标保持或提升。
- 用户偏好研究中，仅 1.5B 参数的 ReVision-SVD 在运动一致性、运动量和运动真实性上显著超越 13B 参数的 HunyuanVideo。
- 舞蹈生成任务上，ReVision 在所有评估指标（SSIM、PSNR、LPIPS、FVD）上超越依赖真实姿态序列的人类图像动画方法。
- 通过降低粗生成阶段的分辨率、帧数和去噪步数，可将该阶段耗时从 36 秒压缩至 **8 秒**，最终视频质量几乎不降。

**方法定位**：ReVision 属于运动条件视频生成方法，但与 Go-with-the-Flow（Burgert et al., 2025）、MotionClone（Ling et al., 2024）、ImageConductor（Li et al., 2025）等直接注入运动信号的方法不同，其核心创新在于引入参数化 3D 运动先验模型（PMP）作为中间优化环节。PMP 利用 Transformer 架构对 SMPL-X/SMAL/点云等参数化表示的运动序列进行迭代精炼，使运动条件从“粗略草稿”升级为“物理合理的三维运动序列”，从而在运动一致性、对象一致性和形态学正确性上取得显著增益。该方法可适配多种视频扩散模型骨干（SVD、Wan2.1 等），具备良好的模型无关性。

视频生成领域近年来取得了显著进展，以**Stable Video Diffusion (SVD-XT-1.1)**（Blattmann et al., 2023）、**HunyuanVideo**（Kong et al., 2024）和**Wan2.1**（Wan et al., 2025）为代表的大规模预训练扩散模型，已能生成视觉质量可观的视频内容。然而，当任务涉及复杂肢体动作、精确物体交互或大幅度运动时，这些模型的输出往往暴露出一个共同瓶颈：**缺乏显式的三维运动先验**。

这一瓶颈的根源在于，现有视频扩散模型主要通过在海量视频数据上学习像素级或潜在空间中的统计相关性来隐式地捕捉运动模式。这种学习范式虽然能生成流畅的视觉内容，但难以真正理解场景中物体的三维几何结构和物理约束。因此，即使模型参数量扩展至数十亿级别（如HunyuanVideo的13B参数），在生成诸如舞蹈、体育动作或多物体交互等场景时，仍频繁出现运动不连贯、形态学失真（如肢体缺失或扭曲）以及物体间遮挡关系错误等问题。论文明确指出，**大规模模型本身并不足以捕获真实世界的动态复杂性**。

针对上述问题，已有一些工作尝试引入运动条件来引导视频生成，例如**Go-with-the-Flow**（Burgert et al., 2025）、**MotionClone**（Ling et al., 2024）和**ImageConductor**（Li et al., 2025）。这些方法通常依赖2D光流或关键点轨迹作为运动先验，但2D表示在本质上是三维运动的投影，信息损失不可避免，尤其在处理遮挡和深度变化时存在天然局限。

本文的核心动机在于：**能否为预训练视频扩散模型注入显式的、可优化的三维运动知识，从而在不重新训练庞大基础模型的前提下，显著提升其对复杂运动和物理交互的生成能力？** 这一思路的出发点是，预训练模型本身已具备强大的视觉生成能力，所欠缺的并非更多的训练数据或模型容量，而是一个能够对生成过程进行“纠偏”的运动结构化先验。通过将运动建模从隐式学习转向显式三维表示，模型有望在保持原有视觉质量的同时，实现运动一致性和物理真实性的质的飞跃。

## 核心方法与创新机理

ReVision的核心创新在于将**显式3D物理建模**引入预训练视频扩散模型的生成流程，形成一套“提取‑优化‑强化”（Extract–Optimize–Reinforce）的三阶段自修正流水线。其关键设计并非从头训练新模型，而是通过两个**changed slots**对现有扩散模型进行“外科手术式”的增强：

### 1. 扩散模型条件通道的扩展

预训练视频扩散模型（如**Stable Video Diffusion (SVD-XT-1.1)**，Blattmann et al., 2023）原本仅以单帧图像的潜在表示作为条件输入。ReVision在此基础上**拼接两个额外的条件通道**（Figure 3）：
- **部件级分割掩码通道**：由优化后的3D运动序列渲染得到，编码了每个对象部件的精确时空位置信息。
- **置信度图通道**：指示部件掩码在不同区域的可靠性，使模型能够区分运动信息可信与不可信的区域。

这一设计使扩散模型能够直接接受完整的3D运动序列作为强条件，从而在生成过程中显式地控制运动一致性和物理真实性。消融实验表明，置信度图的具体数值设置对性能几乎无影响（Table 9），模型仅需一个软性的区域可靠性指示即可有效利用该信息。

### 2. 参数化运动先验模型（PMP）的引入

传统方法直接从粗生成视频中提取运动信息后便不再处理，而ReVision在第二阶段引入了**参数化运动先验模型（PMP）**作为运动优化模块。PMP的核心机制包括：

- **参数化3D表示**：针对不同对象类型采用不同的参数化模型——人体使用**SMPL‑X**，动物使用**SMAL**，通用物体则构建紧凑的21点3D点云表示$p_o \in \mathbb{R}^{21 \times 3}$（由16个轮廓点、4个边界框角点和1个中心点组成，通过深度估计提升到3D空间）。
- **Transformer去噪优化**：PMP采用一系列Transformer模块，以文本嵌入（通过CLIP编码器提取）和运动强度（由相邻帧间参数化模型参数的差异计算）作为条件，对提取的3D运动序列进行迭代去噪、修复和精炼。

消融实验（Table 7）证实，PMP的引入使对象一致性从83.0提升至87.6，运动一致性从94.1提升至96.0，同时将形态学失败率（错误的人/动物结构比例）从27.1%降至14.3%。Figure 10进一步表明，参数化3D网格比2D关键点更鲁棒——当2D关键点检测器无法识别缺失的右手时，参数化人体网格模型能够准确“恢复”该缺失结构。

### 创新本质：从隐式运动到显式物理的范式转换

这两个changed slots共同构成了ReVision的核心洞察：**预训练视频扩散模型并非缺乏生成复杂运动的能力，而是缺乏显式的3D运动先验来引导这一能力**。通过“先生成粗视频获取运动草稿→用参数化3D模型优化运动→将优化后的运动重新注入同一扩散模型”的闭环设计，ReVision实现了对基础模型生成能力的“自我修正”，而非依赖更大规模的模型或更多的训练数据。这一范式转换使得仅1.5B参数的ReVision-SVD在运动质量上能够超越13B参数的**HunyuanVideo**（Kong et al., 2024），同时保持与基础模型相当的推理速度。

ReVision 的核心思想是将“提取—优化—强化”（Extract–Optimize–Reinforce）的三阶段流水线嵌入预训练视频扩散模型，为模型注入显式的参数化三维运动先验，从而解决复杂肢体动作与物体交互中运动失真、物理不一致的瓶颈。整体流程如 Figure 2 所示。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2504_21855/figures/002_Figure_2.jpg]]
*Figure 2: Method overview. Given the video generation model, ReVision operates in three stages. Stage 1: A coarse video is generated based on the provided conditions (e.g., target pose, marked in blue, indicating the rough position of the yellow part in the last frame). Stage 2: 3D features from the generated coarse video are extracted and optimized using the proposed PMP. Stage 3: The optimized 3D sequences are used to regenerate the video with enhanced motion consistency. Best viewed when zoomed in*

### 三阶段流水线

**第一阶段（S1）：粗视频生成。** 给定一张首帧图像和可选的目标姿态（如末帧中某部位的大致位置），使用微调后的视频扩散模型（默认骨干为 **Stable Video Diffusion**，Blattmann et al., 2023）生成一个低质量但包含粗略运动模式的视频。这一阶段的计算开销可通过降低分辨率、减少帧数和去噪步数大幅压缩——从 36 秒降至 8 秒，而最终视频质量几乎无损（Table 8）。

**第二阶段（S2）：3D 运动提取与优化。** 从粗视频中恢复场景的参数化三维表示：人体采用 **SMPL-X** 模型，动物采用 **SMAL** 模型，一般物体则通过 2D 包围盒、分割掩码与深度估计构建紧凑的 21 点三维点云表示 $p_o \in \mathbb{R}^{21 \times 3}$。随后，**参数化运动先验模型（PMP）** 以文本提示嵌入（CLIP）和运动强度为条件，通过 Transformer 对提取的三维运动序列进行去噪、修复和精炼，输出物理一致的高质量运动序列。

**第三阶段（S3）：精细化视频再生。** 使用同一扩散模型，但将优化后的完整三维运动序列作为强条件注入，重新生成具有高运动一致性和视觉质量的视频。这一“自我修正”机制使模型无需重新训练或依赖更大规模的骨干网络即可显著提升运动质量。

### 运动条件注入机制

为实现运动条件控制，ReVision 对预训练视频扩散模型的输入通道进行了最小化改造：在原始单帧图像条件的基础上，拼接两个额外通道——**部件级分割掩码**（由三维运动序列投影得到）和**置信度图**（指示各区域运动信息的可靠性）。消融实验表明，模型对置信度图的具体数值高度鲁棒，仅需软指示即可有效工作（Table 9）。

### 模块间的因果链路

三阶段之间存在清晰的因果依赖：S1 提供蕴含丰富运动模式的“草稿”，其质量决定了 S2 中 3D 提取的上限；S2 的 PMP 是运动质量跃升的关键控制变量——消融实验显示，引入 PMP 使对象一致性从 83.0 提升至 87.6，运动一致性从 94.1 提升至 96.0，形态学失败率从 27.1% 降至 14.3%（Table 7）；S3 则将优化后的运动先验反馈至生成过程，完成闭环修正。这种“生成—提取—优化—再生”的循环使 ReVision 能以仅 1.5B 参数的骨干（SVD）在运动质量上超越 13B 参数的 **HunyuanVideo**（Figure 5）。

ReVision 的核心架构建立在预训练视频扩散模型之上，通过扩展其条件输入通道并引入参数化运动先验模型（Parameterized Motion Prior, PMP），形成“提取‑优化‑强化”三阶段流水线。以下详述其关键模块与公式。

### 扩散模型基础

ReVision 以预训练的视频扩散模型为骨干（如 Stable Video Diffusion, SVD），其前向扩散过程逐步向潜在表示 $z_0$ 添加高斯噪声：

$$q(z_t | z_{t-1}) = \mathcal{N}\left(z_t; \sqrt{1 - \gamma_t} z_{t-1}, \gamma_t \mathbf{I}\right)$$

其中 $\gamma_t$ 为噪声调度参数。该过程可从干净潜在表示 $z_0$ 直接一步推导至任意时间步 $t$：

$$z_t = \sqrt{\bar{\alpha}_t} z_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon$$

此处 $\bar{\alpha}_t = \prod_{i=1}^{t} (1 - \gamma_i)$，$\epsilon \sim \mathcal{N}(0, \mathbf{I})$。模型训练目标为最小化网络预测噪声与真实噪声之间的均方误差：

$$\mathcal{L} = \|\epsilon - \epsilon_{\Theta}(z_t, t, c)\|_2^2$$

其中 $c$ 为条件信息（如首帧图像），$\epsilon_{\Theta}$ 为去噪网络。

### 运动条件通道扩展

为使扩散模型能够接受运动序列作为条件，ReVision 在原有条件输入上拼接两个额外通道：

1. **部件级分割掩码通道**：由参数化3D运动序列渲染得到，编码每个身体部件或物体关键点的空间位置。
2. **置信度图通道**：指示每个部件区域掩码的可靠性，为模型提供软性引导信号。

这一扩展使模型能够在不改变原始架构权重的前提下，通过微调适应运动条件输入，从而在第三阶段生成时接受优化后的完整运动序列作为强条件。

### 参数化运动先验模型

PMP 是 ReVision 的核心创新模块，负责对第二阶段提取的3D运动序列进行去噪、修复和精炼。其输入包括：

- **文本嵌入**：通过预训练 CLIP 编码器从文本描述中提取，提供语义层面的运动引导。
- **运动强度**：由相邻帧间参数化3D模型参数（如 SMPL‑X 关节旋转）的差异计算得到，控制运动幅度。

PMP 采用一系列 Transformer 块对运动序列进行迭代优化，输出与输入同维度的精炼运动序列。该模型的训练目标为最小化优化后序列与真实运动序列之间的误差，使其能够作为一个通用的运动去噪器，适用于人体、动物和一般物体的运动优化。

### 一般物体的参数化表示

对于非人体/动物的通用物体，ReVision 构建紧凑的3D点云表示。首先从2D边界框、分割掩码和估计深度中提取关键点：从掩码轮廓中近似16个顶点，结合4个边界框角点和1个中心点，共21个关键点，通过深度估计提升至3D空间：

$$p_o \in \mathbb{R}^{21 \times 3}$$

该表示在保持计算效率的同时，为一般物体提供了足够的空间结构信息，使 PMP 能够统一处理多种对象类别的运动优化。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2504_21855/figures/017_Figure_10.jpg]]
*Figure 10: The parametric 3D mesh serves as an effective object-level prior, ensuring complete human body structures in the coarse video generated during the first stage. In the left two images, the human keypoint model fails to detect the missing right hand, which is accurately “recovered" by the parametric human mesh model. In the right two images, the human mesh model provides a more accurate prior for both blurred hands*

## 实验与关键发现

### 核心定量结果：VBench++基准

**Table 1**（见附件）汇总了ReVision在VBench++上的主要指标。最显著的提升体现在动态程度（Dynamic Degree）上：ReVision-SVD将基础模型SVD-XT-1.1的43.17%大幅提升至83.15%（+39.98个百分点），ReVision-Wan2.1则将Wan2.1-I2V-14B-720P的51.38%提升至73.67%（+22.29个百分点）。这一跃升表明，显式3D运动先验的注入直接解决了预训练扩散模型“运动贫乏”的核心瓶颈。

与此同时，其他维度指标并未因运动增强而退化：主体一致性（Subject Consistency）从95.42%微升至96.13%，运动流畅性（Motion Smoothness）从98.12%微升至98.88%。这验证了“提取-优化-强化”三阶段流水线在增强运动表现力的同时，能够保持甚至略微提升视频的时空一致性和视觉质量。

### 运动条件生成对比：DAVIS数据集

在DAVIS数据集上的运动迁移任务中（**Table 2**），ReVision与三类运动条件视频生成基线进行了对比：**MotionClone**（Ling et al., 2024）、**Go-with-the-Flow**（Burgert et al., 2025）和**ImageConductor**（Li et al., 2025）。ReVision在CoTracker mIoU上达到0.80（基线最优为0.74），光流误差降至0.33（基线最优为0.36），表明优化后的3D运动序列作为条件能够实现更精确的运动迁移，同时更好地保持物体外观和场景细节。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2504_21855/figures/007_Table_2.jpg]]
*Table 2: Comparisons with motion-conditioned video generation methods on DAVIS. ReVision achieves more accurate motion transfer while preserving object appearance and scene details, resulting in enhanced temporal coherence and reduced visual artifacts*

### 用户偏好研究：小模型超越大模型

**Figure 5**展示了用户偏好对比结果。仅1.5B参数的ReVision-SVD在运动一致性、运动量和运动真实性三个维度上，不仅显著超越其基础模型SVD，还超越了13B参数的最新通用视频生成模型**HunyuanVideo**（Kong et al., 2024）。这一反直觉的结果揭示了关键洞察：参数规模并非运动生成质量的唯一决定因素，显式3D运动建模能够以极小的模型体量实现对大模型的“运动质量超越”。

### 舞蹈生成：超越依赖真值姿态的方法

在TikTok数据集上的舞蹈生成任务中（**Table 5**），ReVision（使用完整运动序列条件）在所有四项指标上超越了依赖真实姿态序列的人类图像动画方法：SSIM达0.864、PSNR达30.08、LPIPS为0.210、FVD为121.26。值得注意的是，即使ReVision仅使用目标姿态（w/ target pose）而非完整运动序列，其表现仍具有竞争力，说明PMP优化后的运动序列质量足以媲美甚至超越真实动作捕捉数据。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2504_21855/figures/013_Table_5.jpg]]
*Table 5: Quantitative comparisons for dance generation. ‘ReVision (w/ full motion)’ follows baselines and takes full motion sequences as condition, while ‘ReVision (w/ target pose)’ uses the target pose from the final frame*

### 消融实验：参数化运动先验模型（PMP）的关键作用

**Table 7**的用户研究消融直接量化了PMP的贡献：
- 对象一致性从83.0提升至87.6（+4.6）
- 运动一致性从94.1提升至96.0（+1.9）
- 形态学失败率（生成的人/动物结构出现错误的比例）从27.1%降至14.3%（-12.8个百分点）

这一消融证实了PMP的核心机制：通过Transformer迭代去噪和精炼3D运动序列，不仅能提升运动质量，还能利用参数化3D网格（如SMPL-X、SMAL）的结构先验“修复”粗生成阶段可能出现的肢体缺失或变形问题。**Figure 10**提供了直观证据：当2D关键点检测器无法识别粗视频中缺失的右手时，参数化人体网格模型能够准确“恢复”该手部结构，体现了3D先验相较于2D先验的鲁棒性优势。

### 推理效率与成本优化

**Table 8**展示了推理效率的定量评估。粗生成阶段（Stage 1）通过降低分辨率、减少帧数和去噪步数，计算时间可从36秒压缩至8秒，而最终视频质量几乎不下降。结合**Table 3**的推理速度对比，ReVision-SVD生成32帧视频的平均时间与SVD相当，但比HunyuanVideo快8.4倍，在运动质量更优的前提下实现了显著的速度优势。

### 置信度图的鲁棒性

**Table 9**的消融显示，置信度图的具体数值设置对性能影响极小。在{完整运动序列, 多边形目标姿态, 空条件}三种条件下，测试了(1, 0.5, 0)、(0.8, 0.5, 0.2)和(3, 2, 1)三组参数配置，结果高度一致。这表明模型仅需软性的区域可靠性指示，而不依赖精确的置信度数值，降低了调参复杂度。

### 失败模式与局限性

尽管整体表现优异，论文指出以下不足：
1. **细粒度细节质量不足**：手指和手部等精细结构的生成质量仍然欠佳，这是当前3D参数化模型（如SMPL-X）自身表达能力的上限所限。
2. **长视频生成的显存瓶颈**：基于SVD的实现受限于80GB显存，无法直接生成长于32帧的视频；扩展至更长视频需要**Figure 7**所示的运动序列插值/外推策略，但长程一致性仍有提升空间。
3. **系统复杂度**：依赖多种现成3D模型（SMPL-X、SMAL、深度估计等），虽总推理时间仅增加约5秒，但增加了工程部署的复杂度。

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2504_21855/figures/011_Figure_7.jpg]]
*Figure 7: Long video generation. Our PMP extends a 32-frame 3D motion to 128 frames through interpolation (32 → 64), extrapolation (64 → 128), and refinement, enabling complex, large-scale motion generation over long video sequences. See supplementary videos for details*

### 补充图表

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2504_21855/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons on VBench++. We achieve a significantly higher Dynamic Degree while maintaining similar performance across all metrics of consistency, smoothness, and quality*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2504_21855/figures/006_Figure_5.jpg]]
*Figure 5: User preference comparisons. Our model enhances the motion generation capability of the pre-trained SVD. It even surpasses HunyuanVideo, a SOTA model with 13B parameters. These results highlight the effectiveness of our model in generating complex motions and interactions*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2504_21855/figures/014_Table_7.jpg]]
*Table 7: User studies for PMP. PMP improves object and motion consistency, while reducing morphological failure rates*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2504_21855/figures/016_Table_8.jpg]]
*Table 8: Quantitative evaluation regarding inference efficiency. We reduce Stage 1 compute time from 36 seconds to 8 seconds, while maintaining comparable final video quality*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2504_21855/figures/018_Table_9.jpg]]
*Table 9: Ablation on confidence score. We evaluate three parameter configurations corresponding to the {full motion sequence, polygon target pose, empty} conditions: (1, 0.5, 0), (0.8, 0.5, 0.2), and (3, 2, 1). The results demonstrate that performance is highly robust to the specific choice of confidence values*

![[assets/figures/papers/paper_list_l37_https_arxiv_org_abs_2504_21855/figures/008_Figure_6.jpg]]
*Figure 6: Handling occlusion. As illustrated by the two apples falling into the basket, ReVision handles occlusions by lifting and optimizing motion in 3D space, which allows explicit reasoning about object spatial relationships, effectively resolving occlusions that are ambiguous in 2D*

## 定位与知识库关联

### 与基线方法的关系

ReVision 并非从零训练一个视频生成模型，而是在**预训练视频扩散模型**之上构建一个“提取‑优化‑强化”的外挂式运动增强流水线。其核心骨干可替换为不同的基础模型，论文中已验证了两个代表性骨干：**Stable Video Diffusion (SVD‑XT‑1.1)**（Blattmann et al., 2023）和 **Wan2.1‑I2V‑14B‑720P**（Wan et al., 2025）。这种“模型无关”的设计使 ReVision 能够将基础模型的动态程度（Dynamic Degree）提升近一倍（SVD：43.17% → 83.15%；Wan2.1：51.38% → 73.67%，见 Table 1），同时保持或改善其他一致性指标。

在**运动条件视频生成**这一子领域，ReVision 与以下方法形成直接对比：
- **Go‑with‑the‑Flow**（Burgert et al., 2025）、**MotionClone**（Ling et al., 2024）、**ImageConductor**（Li et al., 2025）：这些方法均以某种形式的运动信号（如光流、轨迹、关键点）作为条件来驱动视频生成。ReVision 在 DAVIS 数据集上的运动迁移任务中，以 CoTracker mIoU 0.80 和光流误差 0.33 优于上述方法（Table 2），其关键差异在于 ReVision 使用**参数化 3D 运动序列**而非 2D 运动场作为条件，从而在遮挡场景中具有更强的空间推理能力（Figure 6）。
- **人类图像动画方法**（如 VividPose）：在舞蹈生成任务上，ReVision 即使仅使用完整运动序列作为条件（不使用真实姿态序列），也在 SSIM、PSNR、LPIPS、FVD 四项指标上全面超越依赖真实姿态序列的 SOTA 方法（Table 5）。这表明参数化 3D 运动先验所提供的结构化信息，在运动精度上已接近甚至超过真实 2D 姿态监督。

在**通用视频生成**层面，ReVision‑SVD（仅 1.5B 参数）在用户偏好研究中，于运动一致性、运动量和运动真实性三个维度上显著超过 13B 参数的 **HunyuanVideo**（Kong et al., 2024）（Figure 5）。这一结果说明，显式注入 3D 运动先验所带来的收益，可以弥补模型参数规模上的巨大差距。

### 适用边界

ReVision 的适用性由以下因素界定：

1. **对象类型的参数化能力**：ReVision 的性能依赖于对场景中对象的参数化 3D 表示。对于人体，使用 SMPL‑X 模型；对于动物，使用 SMAL 模型；对于一般物体，则构建由 21 个关键点组成的紧凑点云表示 $p_o \in \mathbb{R}^{21 \times 3}$（16 个轮廓顶点 + 4 个边界框角点 + 1 个中心点，通过深度估计提升至 3D）。这意味着**对象必须能被现有的 3D 模型或点云抽象所覆盖**——对于形态极端不规则、缺乏清晰轮廓或无法被深度估计器可靠处理的物体，参数化质量会下降，进而影响运动优化的效果。

2. **对现成 3D 模型的依赖**：流水线中集成了多个现成模型（SMPL‑X、SMAL、深度估计器、分割模型等），虽然总推理时间仅增加约 5 秒（Table 3），但系统复杂度显著上升。这限制了 ReVision 在资源受限场景下的部署灵活性，也意味着任何上游 3D 模型的失效都会级联影响最终生成质量。

3. **视频长度的硬件约束**：当前基于 SVD 的实现受限于 80GB 显存，无法直接生成长于 32 帧的视频。论文提出了通过 PMP 对 3D 运动序列进行插值和外推以支持 128 帧长视频生成的策略（Figure 7），但这属于后处理扩展，而非模型原生的长视频生成能力。

4. **细节保真度不足**：论文明确承认，生成的细节（如手指和手部）质量仍然不足。这是参数化模型本身分辨率的固有限制——SMPL‑X 等模型对手部的建模精度有限，且粗生成阶段产生的模糊或缺失结构虽然可被参数化网格“修复”（Figure 10），但修复后的细节仍缺乏真实感。

### 局限与开放问题

**已知局限**（来自论文自述与实验分析）：
- **多模型依赖与系统复杂度**：依赖 SMPL‑X、SMAL、深度估计等多个现成模型，增加了部署和维护成本。
- **细节生成质量不足**：手指、手部等精细结构的生成质量仍然欠缺。
- **显存受限的视频长度**：80GB 显存限制下原生仅支持 32 帧生成，长视频需额外策略。
- **粗生成阶段的质量依赖**：虽然消融实验表明粗生成阶段可在低分辨率、少帧数、少去噪步数下运行（时间从 36 秒降至 8 秒，最终质量几乎不降，见 Table 8），但极端降质情况下粗视频中的运动模式可能过于退化，超出 PMP 的修复能力。

**开放问题**（需进一步研究）：
- **统一 3D 先验编码**：能否用一个统一的扩散模型直接编码通用物体的 3D 先验，从而减少对多个现成模型的依赖？目前人体、动物、一般物体使用不同的参数化方案，统一表示将大幅降低系统复杂度。
- **长视频连贯性**：如何将更先进的时间压缩技术与 3D 感知框架结合，以原生支持更长视频的连贯生成，而非依赖运动序列的后处理扩展？
- **推理效率优化**：在保持运动质量的前提下，能否进一步降低推理计算开销，使模型更适用于实时应用？当前 8 秒的粗生成时间虽已大幅优化，但整体三阶段流水线仍不适合实时场景。
- **公平性与数据偏差**：论文未分析训练数据偏差或模型在不同人群、对象类别上的公平性表现，这是一个需要后续工作填补的空白。

## 原文 PDF

![[paperPDFs/arxiv_2025/ReVision_High_Quality_Low_Cost_Video_Generation_with_Explicit_3D_Physics_Modeling_for_Complex_Motion_and_Interaction.pdf]]
