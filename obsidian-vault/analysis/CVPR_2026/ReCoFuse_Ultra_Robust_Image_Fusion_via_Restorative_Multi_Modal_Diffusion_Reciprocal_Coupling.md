---
title: "ReCoFuse: Ultra-Robust Image Fusion via Restorative Multi-Modal Diffusion Reciprocal Coupling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ReCoFuse_Ultra_Robust_Image_Fusion_via_Restorative_Multi_Modal_Diffusion_Reciprocal_Coupling.pdf
project_link: null
code_link: "https://github.com/HaoZhang1018/ReCoFuse"
aliases:
- ReCoFuse
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过在扩散采样每一步插入时间感知的跨模态融合模块（TIM），将多模态信息聚合后反馈给恢复分支，使恢复与融合形成互惠耦合，驱动跨模态互补性用于提升恢复质量。
primary_logic: 将信息恢复与融合定义为相互增强的过程，提出互惠耦合优化范式，打破两者之间的隔阂，利用 TIM 作为桥梁实现深度耦合，从而在复杂降质下实现高保真鲁棒融合。
claims:
- 在多种复杂降质（低光、雾霾、噪声、低对比度、条纹）同时存在的情况下，ReCoFuse 能产生视觉愉悦、高保真的融合结果，而其他范式无法有效去除降质。
- 在 MFNet、FMB、LLVIP 三个基准数据集上，ReCoFuse 在标准差（SD）、互信息（MI）和熵（EN）等多项指标上取得最优或次优成绩。
- 消融实验表明，移除 TIM（互惠耦合机制）会导致可见光和红外恢复分支的 PSNR/SSIM 显著下降，验证了跨模态反馈对信息恢复的关键作用。
- 在语义分割下游任务中，基于 ReCoFuse 融合图像的 mIoU 达到 57.67，优于所有对比方法，表明其在高级视觉任务中的优越性。
---

# ReCoFuse: Ultra-Robust Image Fusion via Restorative Multi-Modal Diffusion Reciprocal Coupling

> [!tip] 核心洞察
> 将信息恢复与融合定义为相互增强的过程，提出互惠耦合优化范式，打破两者之间的隔阂，利用 TIM 作为桥梁实现深度耦合，从而在复杂降质下实现高保真鲁棒融合。

| 字段 | 内容 |
|------|------|
| 中文题名 | ReCoFuse：基于恢复性多模态扩散互惠耦合的超鲁棒图像融合 |
| 英文题名 | ReCoFuse: Ultra-Robust Image Fusion via Restorative Multi-Modal Diffusion Reciprocal Coupling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_ReCoFuse_Ultra-Robust_Image_Fusion_via_Restorative_Multi-Modal_Diffusion_Reciprocal_Coupling_CVPR_2026_paper.html) · [Code](https://github.com/HaoZhang1018/ReCoFuse) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | ReCoFuse |
| Dataset | MFNet, FMB, LLVIP, AWMM-100k |

> [!tip] 效果简介
> - MFNet 上，SD 48.473 (best)；MI 3.114 (best)；EN 7.305 (best)。
> - FMB 上，SD 38.213 (best)；MI 2.487 (best)；EN 7.038 (best)。
> - LLVIP 上，SD 40.584 (best)。

## 概要

### 问题背景

鲁棒图像融合旨在从存在复杂降质（如低光、雾霾、噪声、低对比度、条纹等）的多模态源图像中生成高保真融合图像。现有范式主要分为两类：**集成硬回归**（如 **ControlFusion** Tang et al., NeurIPS 2025；**MRFS** Zhang et al., CVPR 2024；**Text-IF** Yi et al., CVPR 2024）和**解耦优化**（如 **BA-Fusion** Sun et al., IJCAI 2024；**DDBF** Zhang et al., CVPR 2024；**OmniFuse** Zhang et al., TPAMI 2025）。这两类范式的核心瓶颈在于：信息恢复与融合过程相互独立，缺乏相互增强机制，导致残留降质和场景表示不完整。

### 核心思路

**ReCoFuse** 提出了一种新的**互惠耦合优化范式**，打破信息恢复与融合之间的隔阂。其核心机制是：在扩散恢复过程的每一个采样步，通过**时间感知跨模态融合模块（TIM）**将多模态信息聚合，再将聚合变量反馈给恢复分支，使恢复与融合形成相互增强的闭环。这一设计的关键洞察在于：跨模态互补性不仅服务于融合，更应驱动恢复质量的提升。

### 方法定位

ReCoFuse 将信息恢复建模为基于均值回复随机微分方程（IR-SDE）的扩散过程，分别构建可见光和红外两个恢复分支（DiM），并通过 TIM 在扩散每一步实现跨模态交互。训练策略上，采用**交替正则化机制**，使信息恢复与信息融合的损失函数交替优化，确保两者协同工作而非相互干扰。

### 主要结果

- **融合质量**：在 MFNet、FMB、LLVIP 三个基准数据集上，ReCoFuse 在标准差（SD）、互信息（MI）和熵（EN）等多项指标上取得最优，并在 AWMM-100k 数据集上验证了泛化能力。
- **消融验证**：移除 TIM（即取消互惠耦合）导致可见光和红外恢复分支的 PSNR/SSIM 显著下降（VIS PSNR 25.205→24.928，IR PSNR 33.294→32.172），证实跨模态反馈对信息恢复的关键作用。
- **下游任务**：在语义分割任务上，基于 ReCoFuse 融合图像的 mIoU 达到 57.67，优于所有对比方法，表明其在高级视觉任务中的优越性。

图像融合旨在将多模态传感器捕获的互补信息整合为单一、信息丰富的表示，在自动驾驶、安防监控、遥感侦察等场景中具有关键应用价值。可见光图像提供丰富的纹理与色彩细节，但在低光、雾霾、烟雾等恶劣条件下信息严重退化；红外图像虽能穿透部分遮挡和弱光照环境，却缺乏精细的纹理结构。因此，鲁棒地融合这两种模态、同时在融合过程中恢复退化信息，成为该领域的核心挑战。

现有鲁棒图像融合方法可归为两类范式。**集成硬回归范式**（如 **ControlFusion** (Tang et al., NeurIPS 2025)、**MRFS** (Zhang et al., CVPR 2024)、**Text-IF** (Yi et al., CVPR 2024)）试图通过语言-视觉降质提示、语义文本引导或多任务互增强等机制，将信息恢复与融合隐式联合建模。然而，这种隐式映射缺乏对恢复过程的显式约束，在复杂降质下难以可靠地还原干净信息。**解耦优化范式**（如 **BA-Fusion** (Sun et al., IJCAI 2024)、**DDBF** (Zhang et al., CVPR 2024)、**OmniFuse** (Zhang et al., TPAMI 2025)）则采用“先恢复后融合”的两阶段策略，先用独立增强模块或扩散模型对退化图像去噪，再执行融合。尽管解耦设计降低了优化难度，但恢复与融合过程相互孤立——恢复阶段无法感知融合所需的跨模态互补信息，导致残留降质和场景表示不完整。

这两类范式的共同瓶颈在于：**信息恢复与融合之间的关系被定义为单向或隐式的，缺乏相互增强的反馈机制**。当多模态源图像同时遭受低光、雾霾、噪声、低对比度乃至条纹等多种降质时，独立恢复分支难以借助另一模态的互补线索来校正自身恢复轨迹，融合阶段也只能在已受损的恢复结果上进行妥协性整合。

针对上述缺口，本文提出一种全新的**互惠耦合优化范式**，其核心洞察是：将信息恢复与融合重新定义为**相互增强的协同过程**。具体而言，在扩散模型的每一步采样中插入**时间感知的跨模态融合模块（TIM）**，动态聚合多模态采样变量，并将聚合后的共享状态反馈给各模态的恢复分支。这一设计打破了恢复与融合之间的隔阂，使跨模态互补性能够实时驱动恢复质量的提升，而更高质量的恢复结果又反过来为融合提供更完整的场景信息，形成闭环增强。基于该范式，我们构建了 **ReCoFuse** 框架，旨在复杂降质下实现超鲁棒、高保真的可见光-红外图像融合。

## 核心方法与创新机理

ReCoFuse 的核心创新在于重新定义了鲁棒图像融合中“信息恢复”与“信息融合”之间的关系，提出**互惠耦合优化范式（Reciprocal Coupling Optimization Paradigm）**。该范式打破了现有工作中恢复与融合相互独立或仅隐式联合的隔阂，使二者在扩散过程的每一步深度交互、相互增强。

### 1. 从解耦/硬回归到互惠耦合

现有鲁棒图像融合范式主要分为两类：

- **集成硬回归范式**（如 **ControlFusion** (Tang et al., NeurIPS 2025)、**MRFS** (Zhang et al., CVPR 2024)、**Text-IF** (Yi et al., CVPR 2024)）将降质恢复隐式地嵌入融合映射中，但恢复过程缺乏显式建模，难以应对复杂降质；
- **解耦优化范式**（如 **BA-Fusion** (Sun et al., IJCAI 2024)、**DDBF** (Zhang et al., CVPR 2024)、**OmniFuse** (Zhang et al., TPAMI 2025)）将恢复与融合分离为两个独立阶段，导致恢复阶段无法利用跨模态互补信息，残留降质被直接传递至融合阶段。

ReCoFuse 的核心洞察在于：信息恢复与融合不应当是先后或隐式的关系，而应当是**相互增强的耦合过程**。具体而言，跨模态互补信息（如红外模态对低光/雾霾的鲁棒性）可以驱动可见光模态的恢复；反之，恢复质量的提升又能为融合提供更完整的场景表示。

### 2. 关键机制：时间感知跨模态集成模块（TIM）

实现互惠耦合的关键组件是**时间感知跨模态集成模块（Time-aware Cross-modal Integration Modules, TIM）**。TIM 被嵌入到扩散模型（DiM）的每一个采样步中，其作用机制如下：

- **动态权重融合**：在扩散步 $t$，TIM 接收可见光和红外模态的采样变量 $z_{vis}^d(t)$ 和 $z_{ir}^d(t)$，生成时变权重 $w_{vis}(t)$ 和 $w_{ir}(t)$，通过加权融合得到聚合变量：
  $$z_f^d(t) = w_{vis}(t) \odot z_{vis}^d(t) + w_{ir}(t) \odot z_{ir}^d(t)$$

- **双向反馈**：聚合变量 $z_f^d(t)$ 被同时反馈给两个恢复分支（DiM_vis 和 DiM_ir），作为下一步扩散噪声估计的共享输入：
  $$\begin{cases} z_{vis}^d(t-1) = \mathrm{DiM}_{vis}(z_f^d(t), t) \\ z_{ir}^d(t-1) = \mathrm{DiM}_{ir}(z_f^d(t), t) \end{cases}$$

- **跨模态校正**：在逆向扩散的漂移项中，TIM 引入跨模态信息对恢复轨迹进行精准校正：
  $$\mathrm{Drift}_{fm}(z_f^d(t), \hat{\epsilon}_{mt}) = \theta_t(\mu_m - z_f^d(t)) + \sigma_t^2 \frac{\hat{\epsilon}_{mt}}{\sqrt{v_t}}$$

这一设计使恢复分支在每一步都能获取另一模态的互补信息，从而在复杂降质下实现更精准的信息恢复。消融实验提供了决定性证据：移除 TIM（Model I - DiM Only）后，可见光恢复分支的 PSNR 从 25.205 降至 24.928，红外恢复分支的 PSNR 从 33.294 降至 32.172，验证了跨模态反馈对信息恢复的关键作用。

### 3. 交替正则化训练策略

为有效协同 DiM 和 TIM 的训练，ReCoFuse 提出了**交替正则化机制（Alternating Regularization Mechanism）**，将优化过程分解为两个交替执行的阶段：

- **信息恢复正则化阶段**：同时更新 DiM 和 TIM，最小化信息恢复损失 $\mathcal{L}_m^{\mathrm{I2R}}$，驱动预测状态逼近理想后验均值；
- **信息融合正则化阶段**：冻结 DiM，仅更新 TIM，最小化融合损失（纹理、对比度、颜色损失 $\mathcal{L}_{\mathrm{texture}}, \mathcal{L}_{\mathrm{contrast}}, \mathcal{L}_{\mathrm{color}}$）。

这一机制简化了多任务联合优化的复杂性，同时通过交替更新确保恢复与融合的稳定协作。消融实验表明，交替正则化（Full Model）相比分离训练方式（Model IV）在融合指标上全面领先（SD 48.473 vs 47.262, MI 3.114 vs 3.054, VIF 0.660 vs 0.647），证明了该策略在协同恢复与融合方面的有效性。

### 4. 创新总结

| 设计维度 | 基线方法 | ReCoFuse |
|---------|---------|----------|
| 信息恢复与融合的关系 | 解耦优化（独立恢复后融合）或集成硬回归（隐式联合映射） | 互惠耦合（TIM 在扩散每一步融合并反馈，使恢复与融合相互增强） |
| 跨模态交互时机 | 仅在融合阶段或图像域增强时进行 | 在扩散恢复过程的每一个采样步均通过 TIM 进行跨模态交互 |
| 训练策略 | 联合训练所有模块或顺序训练 | 交替正则化：交替优化 DiM 和 TIM，支持不同任务损失的独立更新 |

这些创新共同构成了 ReCoFuse 的超鲁棒融合能力：在多种复杂降质（低光、雾霾、噪声、低对比度、条纹）同时存在的情况下，ReCoFuse 能产生视觉愉悦、高保真的融合结果，而其他范式无法有效去除降质（Fig. 1 (d)）。

ReCoFuse 的核心理念是将信息恢复与融合从彼此独立的关系重新定义为**互惠耦合**（reciprocal coupling）过程。如图 2 所示，框架由四个关键模块串联构成：共享编码器、扩散恢复分支、时间感知跨模态集成模块（TIM）和共享解码器，并通过交替正则化机制实现端到端协同训练。

### 数据流与模块关系

给定一对受复杂降质影响的可见光图像 $I_{vis}^d$ 和红外图像 $I_{ir}^d$，**共享编码器** $E$ 首先将源图像映射到潜在空间，提取潜在特征 $\{z_m^d, h_m\} = E(I_m^d)$，其中 $z_m^d$ 承载主场景信息，$h_m$ 保留中间层细节特征。

随后，两个模态特定的**扩散恢复分支**（DiM$_{vis}$ 和 DiM$_{ir}$）基于均值回复随机微分方程（IR-SDE）对 $z_{vis}^d$ 和 $z_{ir}^d$ 进行逐步信息恢复。扩散过程从 $t=T$（高噪声状态）向 $t=0$（干净状态）逆向推进。

在扩散的**每一个采样步** $t$，**时间感知跨模态集成模块**（TIM）接收两个恢复分支的当前采样变量 $z_{vis}^d(t)$ 和 $z_{ir}^d(t)$，通过生成时变权重进行动态融合，得到聚合变量 $z_f^d(t)$：

$$z_f^d(t) = \mathrm{TIM}(z_{vis}^d(t), z_{ir}^d(t), t)$$

这个聚合变量随即被**反馈**给两个恢复分支，作为下一步扩散噪声估计的共享输入：

$$\begin{cases} z_{vis}^d(t-1) = \mathrm{DiM}_{vis}(z_f^d(t), t) \\ z_{ir}^d(t-1) = \mathrm{DiM}_{ir}(z_f^d(t), t) \end{cases}$$

此反馈回路构成了互惠耦合的核心机制：TIM 桥接两个恢复分支，使跨模态互补信息能够实时注入各自的恢复过程，从而在去噪/去雾等恢复任务中利用对方模态的优势信号。

当扩散过程推进至 $t=0$ 时，**共享解码器** $D$ 将最终的聚合潜在特征 $z_f^d(0)$ 与中间特征 $h_f$ 结合，解码生成融合图像：

$$I_f = D(z_f^d(0), h_f)$$

### 交替正则化训练机制

为保证 DiM 与 TIM 的有效协同，ReCoFuse 采用**交替正则化**策略（图 4、图 5）。训练过程在两个约束项之间交替切换：

- **信息恢复正则化** $\mathcal{L}^{\mathrm{I2R}}$ 同时更新 DiM 和 TIM，驱动预测的逆向扩散状态逼近理想后验均值，确保恢复质量；
- **信息融合正则化** $\mathcal{L}^{\mathrm{F}}$（包括纹理、对比度、颜色损失）仅更新 TIM，而 DiM 被冻结，使融合目标在不干扰恢复先验的前提下得到优化。

这种交替更新机制将原本耦合的优化问题解耦为两个独立可解的子问题，同时通过 TIM 作为共享桥梁维持恢复与融合之间的协作交互。消融实验证实，相较于分离训练方式（Model IV），交替正则化在 SD（48.473 vs 47.262）、MI（3.114 vs 3.054）和 VIF（0.660 vs 0.647）等融合指标上均有稳定提升（Table 3）。

![[assets/figures/papers/paper_list_l920_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_ReCoFuse_Ultra_R/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of our proposed robust image fusion framework ReCoFuse*

### 整体框架：互惠耦合优化范式

ReCoFuse 的核心设计在于将信息恢复与融合定义为一个相互增强的过程，而非独立或隐式联合。如图 Figure 2 所示，框架由四个关键模块构成：

1. **共享编码器 (E)**：将降质源图像 $I_{vis}^d$ 和 $I_{ir}^d$ 映射到潜在空间，提取潜在特征 $z_m^d$ 和中间特征 $h_m$，实现主场景信息与降质属性的分离。
2. **扩散恢复模块 (DiM_vis / DiM_ir)**：分别对应可见光和红外模态的恢复分支，基于均值回复随机微分方程（IR-SDE）建模信息恢复过程。
3. **时间感知跨模态集成模块 (TIM)**：作为恢复与融合之间的桥梁，在扩散采样的每一个时间步 $t$ 融合多模态采样变量，生成聚合变量反馈给恢复分支，同时驱动最终融合图像生成。
4. **共享解码器 (D)**：将最终聚合的潜在特征解码为融合图像 $I_f = \mathcal{D}(z_f^d(t), h_f), t=0$。

### 时间感知跨模态集成模块 (TIM)

TIM 是互惠耦合机制的核心枢纽，其详细结构如图 Figure 3 所示。在每个扩散时间步 $t$，TIM 接收两个模态的采样变量 $z_{vis}^d(t)$ 和 $z_{ir}^d(t)$，生成两个时变权重进行动态融合：

$$z_f^d(t) = w_{vis}(t) \odot z_{vis}^d(t) + w_{ir}(t) \odot z_{ir}^d(t) \quad \text{(Eq. 9)}$$

其中 $w_{vis}(t)$ 和 $w_{ir}(t)$ 是通过卷积块注意力模块（CBAM）生成的时变权重，$\odot$ 表示逐元素乘法。该聚合变量 $z_f^d(t)$ 具有双重作用：
- **反馈给恢复分支**：作为共享系统状态，指导 DiM_vis 和 DiM_ir 进行下一步扩散噪声估计：
$$\begin{cases} z_{vis}^d(t-1) = \mathrm{DiM}_{vis}(z_f^d(t), t) \\ z_{ir}^d(t-1) = \mathrm{DiM}_{ir}(z_f^d(t), t) \end{cases} \quad \text{(Eq. 2)}$$

- **驱动融合生成**：在 $t=0$ 时，最终聚合特征经共享解码器输出融合图像。

这种设计使得跨模态互补信息在恢复过程中持续流动，打破了传统范式中恢复与融合的隔阂。

### 基于均值回复 SDE 的信息恢复建模

信息恢复过程被建模为均值回复随机微分方程（IR-SDE）。正向扩散过程为：

$$d z_m^d = \theta_t (\mu_m - z_m^d) dt + \sigma_t d\omega \quad \text{(Eq. 4)}$$

其中 $\theta_t$ 控制向目标均值 $\mu_m$ 的回复速率，$\sigma_t$ 控制噪声尺度，$\mu_m$ 代表干净数据的均值。对应的逆向扩散过程为：

$$d z_m^d = \left[ \theta_t (\mu_m - z_m^d) - \sigma_t^2 \nabla_{z_m^d} \log p_t(z_m^d) \right] dt + \sigma_t d\hat{\omega} \quad \text{(Eq. 5)}$$

得分项 $\nabla_{z_m^d} \log p_t(z_m^d)$ 指向更高数据密度的方向，驱动采样过程向干净数据恢复。

### 跨模态修正的逆向漂移项

在互惠耦合框架下，恢复分支利用聚合变量 $z_f^d(t)$ 进行下一步估计。修正的逆向漂移项利用跨模态信息精准校正恢复轨迹：

$$\mathrm{Drift}_{fm}(z_f^d(t), \hat{\epsilon}_{mt}) = \theta_t(\mu_m - z_f^d(t)) + \sigma_t^2 \frac{\hat{\epsilon}_{mt}}{\sqrt{v_t}} \quad \text{(Eq. 11)}$$

其中 $\hat{\epsilon}_{mt}$ 为 DiM 预测的噪声，$v_t$ 为方差项。通过欧拉积分从聚合状态得到精化的模态特定状态：

$$z_m^d(t-1) = z_f^d(t) - \mathrm{Drift}_{fm}(z_f^d(t), \hat{\epsilon}_{mt}) \cdot \Delta t \quad \text{(Eq. 12)}$$

### 交替正则化机制

为有效协同 DiM 和 TIM 的训练，ReCoFuse 引入交替正则化机制（图 Figure 4、Figure 5），将优化问题分解为两个交替执行的约束项：

**信息恢复正则化**：驱动预测状态逼近理想后验均值 $\tilde{z}_m^d(t-1)$（由 Eq. 13 给出其最大似然估计）：

$$\mathcal{L}_m^{\mathrm{I2R}} = \sum_{t=1}^T \mathbb{E}[ \| z_f^d(t) - \mathrm{Drift}_{fm}(z_f^d(t), \hat{\epsilon}_{mt}) \cdot \Delta t - \tilde{z}_m^d(t-1) \| ] \quad \text{(Eq. 14)}$$

应用此正则项时，TIM 和 DiM 均可更新。

**信息融合正则化**：由纹理损失 $\mathcal{L}_{\mathrm{texture}}$、对比度损失 $\mathcal{L}_{\mathrm{contrast}}$ 和颜色损失 $\mathcal{L}_{\mathrm{color}}$ 共同约束融合图像综合保留多模态优势信息（Eq. 15-17）。应用此正则项时，仅 TIM 保持可训练，DiM 被冻结。

这种交替机制简化了多任务优化，同时通过协作交互增强了对最优解 $g^*$ 的逼近。

![[assets/figures/papers/paper_list_l920_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_ReCoFuse_Ultra_R/figures/001_Figure_1.jpg]]
*Figure 1: Comparisons between our reciprocal coupling optimization paradigm and existing robust image fusion paradigms. Our method effectively removes haze and noise while others cannot*

## 实验与关键发现

### 主实验结果

ReCoFuse 在 MFNet、FMB、LLVIP 三个基准数据集上进行了系统评估，采用标准差（SD）、互信息（MI）、熵（EN）等多项指标衡量融合质量。如表 1 所示，ReCoFuse 在所有三个数据集上均取得最优或次优成绩：在 MFNet 上 SD 达到 48.473，MI 达到 3.114，EN 达到 7.305；在 FMB 上 SD 达到 38.213，MI 达到 2.487，EN 达到 7.038；在 LLVIP 上 SD 达到 40.584，MI 达到 2.289，EN 达到 7.279。这些结果表明互惠耦合范式在信息保留和融合质量上具有一致优势。

定性结果进一步验证了定量结论。图 7 展示了重新训练设置下的鲁棒融合对比，ReCoFuse 在同时存在低光、雾霾、噪声等复杂降质的情况下，能够生成视觉愉悦、高保真的融合图像，而其他范式（如集成硬回归的 **ControlFusion**（Tang et al., NeurIPS 2025）和解耦优化的 **OmniFuse**（Zhang et al., TPAMI 2025））则残留明显的降质痕迹。

### 泛化能力评估

为验证方法的跨域泛化能力，在 AWMM-100k 数据集上进行了评估。该数据集包含真实场景中的复杂降质，对融合方法的鲁棒性构成严峻挑战。如表 2 所示，ReCoFuse 在 SD（44.469）、MI（3.095）、EN（7.296）等指标上均取得最优，表明互惠耦合机制不仅适用于受控实验环境，也能有效泛化到真实世界的复杂场景。图 8 的定性结果显示，ReCoFuse 在 AWMM-100k 上同样保持了高保真融合能力，未出现明显的域偏移退化。

### 下游任务验证

为验证融合结果对高级视觉任务的支撑能力，在 MFNet 数据集上进行了语义分割和目标检测实验。如表 5 所示，基于 ReCoFuse 融合图像的语义分割 mIoU 达到 57.67，优于所有对比方法，表明互惠耦合生成的融合图像在保留语义信息方面具有显著优势。在目标检测任务中（表 4），ReCoFuse 的 mAP@0.5:.95 达到 0.625，同样取得最优成绩。图 11 和图 12 的定性结果进一步展示了 ReCoFuse 在检测边界框精度和分割区域完整性上的优势。

### 消融实验

消融实验围绕互惠耦合机制的核心设计展开，所有实验均控制单一变量，确保结论可靠。

**互惠耦合的必要性。** 移除 TIM 模块（Model I - DiM Only）后，信息恢复与融合之间的桥梁被切断，恢复质量大幅下降：可见光恢复分支的 PSNR 从 25.205 降至 24.928，红外恢复分支的 PSNR 从 33.294 降至 32.172。图 9 的可视化结果表明，无 TIM 时恢复图像残留明显噪声和模糊，验证了跨模态反馈对信息恢复的关键驱动作用。

**融合时机的选择。** 采用后融合方式（Model II - Late Fusion）将恢复与融合解耦，导致融合图像对比度异常和细节丢失，SD、MI 等指标明显低于完整模型（图 10）。这证明在扩散恢复过程中进行逐步融合（而非恢复完成后再融合）是实现高保真融合的关键。

**交替正则化的作用。** 相比分离训练方式（Model IV），交替正则化（Full Model）在融合指标上表现更优：SD 48.473 vs 47.262，MI 3.114 vs 3.054，VIF 0.660 vs 0.647。这表明交替优化信息恢复正则化和信息融合正则化能够有效协同 DiM 和 TIM，避免训练过程中的目标冲突。

**其他设计组件。** 移除时间嵌入（Model III）或替换关键损失函数（Model VII, VIII）均导致融合图像出现过曝、显著性降低或颜色失真等问题（表 3，图 10），进一步验证了时间感知权重和综合损失约束在互惠耦合框架中的重要作用。

### 公平性说明

为确保对比的公平性，所有对比方法均使用与 ReCoFuse 相同的降质训练数据进行重新训练，并在相同的评估策略下测试。对于无法重新训练的外部恢复方法，使用作者提供的建议设置和预训练模型进行评估。

![[assets/figures/papers/paper_list_l920_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_ReCoFuse_Ultra_R/figures/008_Table_1.jpg]]
*Table 1: Quantitative results under different evaluation strategies on three datasets*

![[assets/figures/papers/paper_list_l920_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_ReCoFuse_Ultra_R/figures/007_Figure_7.jpg]]
*Figure 7: Qualitative results of the retrained robust fusion comparison*

![[assets/figures/papers/paper_list_l920_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_ReCoFuse_Ultra_R/figures/012_Table_3.jpg]]
*Table 3: Quantitative results of all ablation studies*

![[assets/figures/papers/paper_list_l920_https_openaccess_thecvf_com_content_CVPR2026_html_Zhang_ReCoFuse_Ultra_R/figures/010_Figure_9.jpg]]
*Figure 9: Visual ablation on reciprocal coupling for restoration*

## 定位与知识库关联

### 1. 问题域与范式定位

ReCoFuse 解决的是**复杂降质下的鲁棒图像融合**问题，其核心矛盾在于：现有范式将信息恢复与融合定义为两个相互独立的过程，导致恢复分支无法利用融合阶段的跨模态互补性，融合分支也无法受益于恢复过程的精细化先验，最终在低光、雾霾、噪声、低对比度、条纹等多种降质共存时产生残留退化与场景表示不完整。

论文将现有鲁棒图像融合方法归纳为两类范式，并据此定位自身贡献：

- **集成硬回归范式 (Integrated Hard Regression)**：通过隐式联合映射将恢复与融合压缩到单一前馈过程中，代表工作包括 **ControlFusion** (Tang et al., NeurIPS 2025)、**MRFS** (Zhang et al., CVPR 2024)、**Text-IF** (Yi et al., CVPR 2024)。这类方法缺乏显式的恢复建模，在复杂降质下难以精确分离退化与场景信息。

- **解耦优化范式 (Decoupled Optimization)**：先独立进行信息恢复，再将恢复结果输入融合模块，代表工作包括 **BA-Fusion** (Sun et al., IJCAI 2024)、**DDBF** (Zhang et al., CVPR 2024)、**OmniFuse** (Zhang et al., TPAMI 2025)。这类方法虽显式建模恢复，但恢复与融合之间无反馈通路，跨模态信息无法回流以提升恢复质量。

ReCoFuse 提出的**互惠耦合优化范式 (Reciprocal Coupling Optimization)** 是第三种路径：通过时间感知跨模态集成模块 (TIM) 在扩散采样的每一步将多模态信息聚合后反馈给各恢复分支，使恢复与融合形成相互增强的闭环。

### 2. 与基线工作的结构性差异

下表从三个关键设计槽位对比 ReCoFuse 与代表性基线的差异：

| 设计维度 | 解耦优化范式 (如 OmniFuse) | 集成硬回归范式 (如 ControlFusion) | ReCoFuse (本文) |
|---------|--------------------------|--------------------------------|-----------------|
| 信息恢复与融合的关系 | 独立恢复→后融合，无反馈 | 隐式联合映射，无显式恢复建模 | TIM 驱动的互惠耦合，恢复与融合相互增强 |
| 跨模态交互时机 | 仅在融合阶段或预融合去噪时 | 仅在特征提取/融合阶段 | 扩散恢复的**每一个采样步**均通过 TIM 交互 |
| 训练策略 | 顺序训练或联合训练所有模块 | 端到端联合训练 | 交替正则化：交替优化 DiM 与 TIM，独立更新恢复损失与融合损失 |

**关键差异的因果机制**：

1. **跨模态反馈回路**：在解耦范式中，可见光恢复分支只能看到自身模态的退化信息；ReCoFuse 中，TIM 生成的聚合变量 $z_f^d(t)$ 同时作为 DiM_vis 和 DiM_ir 的输入 (Eq. 1-2)，使红外模态的热辐射信息可以引导可见光分支去雾/去噪，反之可见光的纹理细节也可辅助红外分支保持边缘。消融实验证实，移除 TIM 后可见光恢复 PSNR 从 25.205 降至 24.928，红外恢复 PSNR 从 33.294 降至 32.172 (Table 3, Model I vs Full Model)。

2. **时变动态融合**：TIM 生成的权重 $w_{vis}(t)$ 和 $w_{ir}(t)$ 随时间步 $t$ 动态变化 (Eq. 9)，在扩散早期（高噪声阶段）可偏向信噪比更高的模态，在后期（细节恢复阶段）可均衡融合纹理信息。移除时间嵌入 (Model III) 会导致融合图像过曝或显著性降低 (Table 3, Fig. 10)。

3. **交替正则化的协同训练**：不同于简单的联合训练，交替正则化机制 (Fig. 4-5) 在应用信息恢复正则化 $\mathcal{L}^{\mathrm{I2R}}$ 时同时更新 DiM 和 TIM，在应用信息融合正则化 $\mathcal{L}_{\mathrm{F}}$ 时冻结 DiM 仅更新 TIM。这避免了恢复目标与融合目标的梯度冲突，消融中交替正则化相比分离训练 (Model IV) 在 SD (48.473 vs 47.262)、MI (3.114 vs 3.054)、VIF (0.660 vs 0.647) 上均有稳定提升 (Table 3)。

### 3. 在扩散模型与图像融合交叉领域的定位

ReCoFuse 的技术路线建立在两个基础之上：

- **均值回复扩散 (IR-SDE)**：采用 IR-SDE (Luo et al., ICML 2023) 作为信息恢复的数学框架，正向 SDE 将退化图像推向可学习的干净均值 $\mu_m$，逆向 SDE 通过得分函数驱动恢复 (Eq. 4-5)。ReCoFuse 的独特之处在于将 IR-SDE 的标准单模态恢复扩展为**跨模态条件恢复**：逆向漂移项被修正为 $\mathrm{Drift}_{fm}$ (Eq. 11)，利用 TIM 聚合的跨模态信息校正恢复轨迹。

- **扩散融合 (Diffusion-based Fusion)**：现有扩散融合方法（如 **Diff-IF**, Yi et al., Inf. Fusion 2024; **DCEvo**, Liu et al., CVPR 2025）主要在融合阶段使用扩散模型，恢复与融合仍是分离的。ReCoFuse 将扩散过程同时用于恢复和融合，并通过 TIM 在采样过程中实现两者的协同。

### 4. 适用边界与局限

**适用场景**：
- 多模态图像融合（可见光-红外）在复杂混合降质下的鲁棒融合
- 需要融合结果同时支持视觉质量（SD, MI, EN 等无参考指标最优）和下游任务（语义分割 mIoU 57.67, 目标检测 mAP 0.625，均优于所有对比方法，Table 4-5）

**已知局限**：
- 论文未明确报告推理速度或计算开销，双分支扩散采样 + 每步 TIM 交互可能带来较高的推理延迟，此点需在实际部署中验证
- 仅在可见光-红外双模态上验证，扩展到更多模态（如近红外、深度图）的泛化性未经验证
- 对极端降质（如大面积遮挡、严重运动模糊）的鲁棒性缺乏专门消融

### 5. 开放问题

1. **互惠耦合的理论收敛性**：交替正则化虽在经验上有效，但其收敛性未给出理论证明。两个目标函数交替优化的不动点是否唯一、是否对应全局最优，仍需进一步分析。

2. **TIM 的信息瓶颈**：TIM 将两个模态的采样变量压缩为一个聚合变量，当模态间信息冲突（如红外热源与可见光纹理在同一位置矛盾）时，聚合过程是否会导致信息丢失或虚假融合，论文未深入讨论。

3. **与其他恢复先验的兼容性**：ReCoFuse 使用 IR-SDE 作为恢复框架，若替换为其他扩散变体（如冷扩散、一致性模型）或非扩散恢复方法，互惠耦合机制是否仍能保持增益，值得探索。

## 原文 PDF

![[paperPDFs/CVPR_2026/ReCoFuse_Ultra_Robust_Image_Fusion_via_Restorative_Multi_Modal_Diffusion_Reciprocal_Coupling.pdf]]
