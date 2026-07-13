---
title: "DLWM: Dual Latent World Models enable Holistic Gaussian-centric Pre-training in Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/DLWM_Dual_Latent_World_Models_enable_Holistic_Gaussian_centric_Pre_training_in_Autonomous_Driving.pdf
project_link: null
code_link: null
aliases:
- DDLWM
- DLWM
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 解耦的双潜在世界模型（高斯流引导的潜在预测用于感知/预测，自车规划引导的潜在预测用于规划）在阶段一重建基础上学习时序动态，是性能提升的关键驱动力。
primary_logic: 通过自监督重建深度与语义图学习鲁棒的高斯表示，再利用两个独立的潜在世界模型分别对未来场景的几何/语义演化和自车轨迹运动进行隐式预测，实现覆盖全任务的高斯中心预训练。
claims:
- 仅两阶段预训练，无任何任务标签，即可在三维占据感知上提升1.02 mIoU。
- 解耦的双世界模型相比统一模型显著提升感知（mIoU 18.9→19.3）与规划（L2 0.58→0.46）性能。
- 高斯流引导的潜在世界模型有效提升占据预测（mIoU 18.83→19.30）。
- 自车规划引导的潜在世界模型结合阶段一预训练将平均L2距离从0.55降至0.46。
---

# DLWM: Dual Latent World Models enable Holistic Gaussian-centric Pre-training in Autonomous Driving

> [!tip] 核心洞察
> 通过自监督重建深度与语义图学习鲁棒的高斯表示，再利用两个独立的潜在世界模型分别对未来场景的几何/语义演化和自车轨迹运动进行隐式预测，实现覆盖全任务的高斯中心预训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | DLWM：双潜在世界模型实现自动驾驶中整体高斯中心预训练 |
| 英文题名 | DLWM: Dual Latent World Models enable Holistic Gaussian-centric Pre-training in Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.00969) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | DLWM (Dual Latent World Models) |
| Dataset | SurroundOcc-nuScenes, nuScenes |

> [!tip] 效果简介
> - SurroundOcc-nuScenes 上，mIoU 21.85 vs 20.83 (+1.02)；IoU 34.61 vs 31.77 (+2.84)；mIoU (avg 1-3s) 17.77 vs 15.09 (+2.68)。
> - nuScenes 上，L2 (m) Avg. 0.46 vs 0.55 (-0.09)；Collision Rate (%) Avg. 0.19 vs 0.24 (-0.05)。

## 概要

自动驾驶社区长期面临一个关键瓶颈：以3D高斯为中心的场景表示模型（如GaussianFormer）缺乏统一的预训练范式，难以同时提升感知、预测与规划三大下游任务。现有方案通常依赖特定任务的监督训练，忽略了高斯表示在时空维度上的自监督学习潜力，且高斯查询固有的排列等价性使直接对查询特征施加时序监督变得困难。

本文提出**DLWM（Dual Latent World Models）**，一种两阶段自监督预训练框架，首次实现覆盖感知、预测与规划的**整体高斯中心预训练**。核心思路是：阶段一通过重建多视图深度图与语义图，学习鲁棒的3D高斯场景表示；阶段二引入**解耦的双潜在世界模型**——高斯流引导的潜在世界模型显式预测3D高斯的动态位移，用于提升感知与占据预测；自车规划引导的潜在世界模型以预测轨迹条件化未来场景查询，用于提升运动规划。两个世界模型分别从场景几何/语义演化和自车运动两个维度学习时序动态，避免了统一模型的学习复杂度冲突。

主要结果（基于nuScenes/SurroundOcc-nuScenes验证集）：
- **3D占据感知**：mIoU从20.83提升至21.85（+1.02），IoU从31.77提升至34.61（+2.84）。
- **4D占据预测**：1–3秒平均mIoU从15.09提升至17.77（+2.68），平均IoU从25.65提升至30.60（+4.95）。
- **运动规划**：平均L2距离从0.55降至0.46（-0.09），碰撞率从0.24降至0.19（-0.05）。

消融实验证实：解耦的双世界模型（Dual）在感知（mIoU 19.3 vs 18.9）和规划（L2 0.46 vs 0.58）上均显著优于统一模型（Unified）；预训练数据量从20%增至100%时，3D占据感知mIoU从17.83持续提升至19.98，展现出良好的数据可扩展性。

方法层面，DLWM属于**自监督高斯中心预训练**范式，与无预训练的GaussianFormer、OccWorld、VAD等任务特定基线形成互补。其训练信号完全来自LiDAR稀疏深度、Metric3D伪稠密深度和Grounded SAM自动语义标签，无需任何人工标注。这一设计使其在标注稀缺场景下具有独特优势，但同时也意味着对LiDAR数据和伪真值质量的依赖，在缺乏LiDAR或极端噪声场景下的适用性仍需进一步验证。



### 自动驾驶中的感知-预测-规划一体化挑战

自动驾驶系统需要同时完成三维场景感知、未来状态预测与运动规划三大核心任务。近年来，以三维高斯（3D Gaussian）为中心的场景表示方法因其显式、可微、高效的特点而受到广泛关注，代表性工作如**GaussianFormer**通过可学习高斯查询直接预测高斯属性，在三维占据感知任务中展现出强大潜力。然而，这类高斯中心模型面临一个根本性瓶颈：**缺乏统一的预训练范式**，无法在单一框架下同时提升感知、预测与规划的全链路性能。

现有的预训练方法通常针对单一任务设计——例如仅对感知主干进行对比学习或掩码重建，而忽视了时序动态建模与规划决策之间的耦合关系。这导致两个突出问题：

1. **时序建模缺失**：高斯中心模型天然适合表达场景几何，但如何让高斯查询理解场景随时间的演化（物体运动、遮挡变化、新区域出现）仍是一个开放问题。当前方法（如**OccWorld**）虽能进行四维占据预测，但依赖任务特定的监督信号，未能在预训练阶段建立通用的时序表征。
2. **任务割裂**：感知、预测和规划通常分阶段训练或仅通过下游任务损失进行微调，预训练阶段学到的表示难以直接服务于规划决策。**VAD**、**BEV-Planner**等端到端规划方法虽将感知与规划联合优化，但未利用大规模无标注数据的预训练优势。

### 高斯查询的排列等价性困境

更本质的困难在于，高斯查询具有排列等价性——即高斯体的索引顺序不具有物理意义，这导致**无法直接对查询特征施加时序一致性约束**。传统的时序预测方法（如对BEV特征直接进行时序差分或光流监督）难以迁移到高斯查询空间，因为前后两帧的高斯查询之间缺乏确定的对应关系。这一特性使得为高斯中心模型设计自监督时序预训练任务变得极具挑战性。

### DLWM的动机与核心思路

针对上述缺口，DLWM提出了一种**双潜在世界模型（Dual Latent World Models）**的两阶段预训练范式，其核心动机在于：

- **阶段一**：通过自监督重建多视图深度图和语义图，使高斯查询学会表达丰富的几何与语义场景上下文，为时序学习提供鲁棒的初始表示。
- **阶段二**：引入两个解耦的潜在世界模型，分别对场景的物理演化（高斯流引导）和自车的运动规划（规划引导）进行隐式预测。这种解耦设计的关键洞察在于：场景中其他物体的运动与自车运动遵循不同的动力学规律，统一建模会增加学习复杂度；分离两个世界模型能够更精准地捕获各自的时序规律，从而在潜在空间中实现高效的预训练。

通过这一设计，DLWM首次实现了覆盖感知、预测与规划的**整体高斯中心预训练**，仅需两阶段自监督训练、无需任何下游任务标签，即可在三维占据感知（+1.02 mIoU）、四维占据预测（+2.68 mIoU）和运动规划（L2误差降低0.09 m）三项任务上同步提升。



## 核心方法与创新机理

DLWM 的核心创新在于为**高斯中心模型**（Gaussian-centric models）构建了首个统一的**自监督预训练范式**，通过解耦的双潜在世界模型（Dual Latent World Models）同时提升感知、预测与规划三项下游任务。其关键设计围绕以下三个 changed slots 展开。

### 1. 两阶段自监督预训练策略

现有高斯中心方法（如 **GaussianFormer**）仅依赖任务特定监督从头训练，缺乏通用的表示学习阶段。DLWM 提出**两阶段预训练**，无需任何人工任务标签：

- **阶段一（高斯表示学习）**：通过重建多视图深度图与语义图，学习鲁棒的 3D 高斯场景表示。训练信号完全来自自动生成的伪真值——LiDAR 稀疏深度、Metric3D 伪稠密深度和 Grounded SAM 自动语义标签，损失函数为：

$$\mathcal{L}_{rec} = \omega_{1} \mathcal{L}_{d} + \omega_{2} \mathcal{L}_{pd} + \omega_{3} \mathcal{L}_{sem}$$

其中 $\mathcal{L}_{d}$ 为深度 L1 损失，$\mathcal{L}_{pd}$ 为感知伪深度损失，$\mathcal{L}_{sem}$ 为语义交叉熵损失，权重分别为 1.0、0.05、1.0。

- **阶段二（时序动态学习）**：在冻结的阶段一感知网络基础上，训练两个独立的潜在世界模型，分别对未来场景演化和自车轨迹运动进行隐式预测。监督目标为下一帧多视图图像经冻结感知网络生成的 BEV 潜在特征。

这一设计的直接收益是：仅两阶段预训练、无任何任务标签，即可在 3D 占据感知上将 **GaussianFormer** 的 mIoU 从 20.83 提升至 21.85（+1.02），IoU 从 31.77 提升至 34.61（+2.84）（Table 1）。

### 2. 解耦的双潜在世界模型

高斯查询具有**排列等价性**（permutation equivariance），使得直接对查询特征进行时序监督极为困难。DLWM 的因果 knob 在于将时序预测**解耦为两个独立的世界模型**：

- **高斯流引导的潜在世界模型**（Gaussian-flow-guided）：显式预测每个 3D 高斯的局部动态位移流 $\Delta \boldsymbol{\mu}_{k}^{t}$，结合自车运动变换 $\mathbf{T}_{ego}^{t \to t+1}$ 将当前高斯传播至下一帧：

$$\boldsymbol{\mu}_{k}^{t+1} = \mathbf{T}_{ego}^{t \to t+1} ( \boldsymbol{\mu}_{k}^{t} + \Delta \boldsymbol{\mu}_{k}^{t} )$$

传播后的高斯经 BEV 栅格化生成预测的潜在特征 $\hat{B}_{t+1}$，以冻结感知网络生成的真实 BEV 特征 $B_{t+1}$ 为监督目标：

$$\mathcal{L}_{bev} = \| \hat{B}_{t+1} - B_{t+1} \|_2$$

该模型主要服务于**感知与占据预测**任务。

- **自车规划引导的潜在世界模型**（Ego-planning-guided）：以预测的自车轨迹 $\hat{\mathbf{T}}$ 为条件，通过运动感知层归一化（Motion-Aware Layer Normalization, MLN）将当前场景查询 $Q^{t}_{\text{scene}}$ 转化为下一帧场景查询预测。训练目标为模仿学习回归损失与 BEV 重建损失之和：

$$\mathcal{L}_{plan} = \underbrace{\| \hat{\mathbf{T}} - \mathbf{T} \|_1}_{\mathcal{L}_{reg}} + \mathcal{L}_{bev}$$

该模型主要服务于**运动规划**任务。

**解耦的关键性**：消融实验（Table 7）表明，统一模型（Unified）虽可同时处理两项预测，但双模型（Dual）在感知上 mIoU 从 18.9 提升至 19.3，规划上 L2 误差从 0.58 降至 0.46，碰撞率从 0.22 降至 0.19。这验证了感知预测与规划预测需要不同的潜在动力学建模。

### 3. 全自监督训练信号

DLWM 完全摆脱了对人工标注的依赖，训练信号均来自自动生成的伪真值或自监督目标：

| 训练阶段 | 监督信号来源 | 损失函数 |
|---------|------------|---------|
| 阶段一 | LiDAR 稀疏深度 + Metric3D 伪稠密深度 + Grounded SAM 语义 | $\mathcal{L}_{rec}$（深度 L1 + 伪深度 + 语义 CE） |
| 阶段二（高斯流） | 冻结感知网络生成的 BEV 特征 | $\mathcal{L}_{bev}$（L2） |
| 阶段二（规划） | 冻结感知网络生成的 BEV 特征 + 真实轨迹 | $\mathcal{L}_{plan} = \mathcal{L}_{reg} + \mathcal{L}_{bev}$ |

消融实验（Table 4）证实，同时使用稀疏深度、稠密伪深度和语义监督获得最佳 3D 占据性能（mIoU 19.30, IoU 30.56），引入高斯流后进一步提升（mIoU 19.30 → 19.30，IoU 30.56 → 30.56，原文此处数值需人工核实）。规划分支中，加入阶段一预训练和 BEV 预测使平均 L2 从 0.61 降至 0.46，碰撞率从 0.30 降至 0.19（Table 5）。

### 总结

DLWM 的核心创新可归纳为：**以解耦的双潜在世界模型为因果 knob，在阶段一重建学习的高斯表示基础上，分别对场景几何/语义演化和自车轨迹运动进行隐式预测，从而在不依赖任何任务标签的前提下，实现对感知、预测、规划三大任务的统一预训练提升**。这一范式突破了高斯查询排列等价性带来的时序监督难题，为高斯中心模型的规模化预训练提供了可行路径。



DLWM 提出一个**两阶段自监督预训练范式**，旨在为高斯中心（Gaussian-centric）的自动驾驶模型提供统一、覆盖感知、预测与规划全任务的表示学习。其核心架构如图 Figure 2 所示，整体流程可概括为：

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/002_Figure_2.jpg]]
*Figure 2: Overall pipeline of DLWM. Stage 1 (Sec. 3.1) focuses on learning robust 3D Gaussian scene representations from multi-view videos using self-supervised reconstruction on depth and semantic maps. Stage 2 introduces dual latent world models. a. Gaussianflow-guided model (Sec. 3.2) explicitly predicts 3D Gaussian flow, propagating the current Gaussian states to the future frame for latent prediction. b. Ego-planning-guided model (Sec. 3.3) conditions the future scene forecasting on the predicted ego trajectory. All predicted latents are supervised by the perceived features from next multi-view image using a frozen Gaussian perception module*

1. **阶段一：高斯表示学习**  
   输入多视图视频序列，通过图像编码器（ResNet101‑DCN + FPN）提取多尺度特征；可学习的高斯查询（Gaussian queries）经高斯变换解码器与图像特征交互，迭代预测一组三维高斯的属性（中心、协方差、语义、不透明度等）。  
   在无需人工标注的条件下，利用 LiDAR 稀疏深度、Metric3D 伪稠密深度和 Grounded SAM 自动语义标签，通过 alpha 混合渲染深度图与语义分割图进行自监督重建，损失函数为：
   $$
   \mathcal{L}_{rec} = \omega_{1} \mathcal{L}_{d} + \omega_{2} \mathcal{L}_{pd} + \omega_{3} \mathcal{L}_{sem}
   $$
   其中 $\mathcal{L}_{d}$ 为深度 L1 损失，$\mathcal{L}_{pd}$ 为伪深度感知损失，$\mathcal{L}_{sem}$ 为语义交叉熵损失。该阶段的目标是学习鲁棒的三维场景几何与语义表示。

2. **阶段二：双潜在世界模型**  
   在冻结的阶段一感知网络基础上，引入两个独立训练的潜在世界模型，分别服务于感知/预测与规划任务：
   - **高斯流引导的潜在世界模型**：对当前帧的每个高斯预测局部动态位移流 $\Delta \boldsymbol{\mu}_{k}^{t}$，结合自车运动变换 $\mathbf{T}_{ego}^{t \to t+1}$ 将高斯中心传播至下一帧：
     $$
     \boldsymbol{\mu}_{k}^{t+1} = \mathbf{T}_{ego}^{t \to t+1} ( \boldsymbol{\mu}_{k}^{t} + \Delta \boldsymbol{\mu}_{k}^{t} )
     $$
     传播后的高斯经 BEV 栅格化生成未来潜在 BEV 特征 $\hat{B}_{t+1}$，以冻结感知网络生成的下一帧 BEV 特征 $B_{t+1}$ 作为自监督目标：
     $$
     \mathcal{L}_{bev} = \| \hat{B}_{t+1} - B_{t+1} \|_2
     $$
     该分支同时输出未来占据体素，用于 4D 占据预测。
   - **自车规划引导的潜在世界模型**：以可学习的路径点查询（waypoint queries）与当前场景查询交互，预测自车轨迹 $\hat{\mathbf{T}}$，并通过运动感知层归一化（Motion‑Aware Layer Normalization）将预测轨迹条件化到场景查询，进而预测未来场景潜在表示。规划分支的总损失为：
     $$
     \mathcal{L}_{plan} = \mathcal{L}_{reg} + \mathcal{L}_{bev}, \quad \mathcal{L}_{reg} = \| \hat{\mathbf{T}} - \mathbf{T} \|_1
     $$

两个世界模型**解耦训练**，分别针对场景动态演化和自车运动进行隐式预测，共同为下游任务提供时序感知与运动先验。预训练完成后，各下游任务（3D 占据感知、4D 占据预测、运动规划）仅需在冻结或微调的骨干网络上添加轻量任务头即可获得显著性能提升。

### 补充图表

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of our DLWM for pre-training and performance improvements for downstream tasks*



DLWM 的核心由两阶段构成：阶段一通过自监督重建学习鲁棒的三维高斯场景表示，阶段二引入双潜在世界模型分别对场景动态演化和自车规划进行时序预测。以下按模块拆解关键设计与公式。

### 阶段一：高斯表示学习

给定多视图图像，图像编码器（ResNet101-DCN+FPN）提取多尺度特征，随后高斯变换解码器利用可学习的高斯查询与图像特征交叉注意力，迭代预测每个三维高斯的属性。每个高斯由中心 $\mu$、协方差 $\Sigma$、不透明度 $\alpha$、深度 $d$ 和语义 logits $s$ 参数化，其空间分布定义为：

$$G(x) = \exp \left( -\frac{1}{2} (x - \mu)^T \Sigma^{-1} (x - \mu) \right) \tag{1}$$

通过将高斯投影到各相机视图并按深度排序，使用 alpha 混合渲染深度图和语义图：

$$\mathbf{D}(p) = \sum_{i=1}^{K} d_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j) \tag{2}$$

$$\mathbf{S}(p) = \sum_{i=1}^{K} s_i \alpha_i \prod_{j=1}^{i-1} (1 - \alpha_j) \tag{3}$$

其中 $p$ 为像素坐标，$K$ 为该射线上的高斯数量。渲染结果由三类自监督信号约束：LiDAR 点云投影得到的稀疏深度（L1 损失）、Metric3D 生成的稠密伪深度（感知损失）以及 Grounded SAM 自动标注的语义标签（交叉熵损失）。总体重建损失为三者加权和：

$$\mathcal{L}_{rec} = \omega_{1} \mathcal{L}_{d} + \omega_{2} \mathcal{L}_{pd} + \omega_{3} \mathcal{L}_{sem} \tag{4}$$

权重分别设为 1.0、0.05、1.0。此阶段完全无需人工标注，仅依赖自动获取的监督信号。

### 阶段二：双潜在世界模型

阶段二在冻结的阶段一感知网络基础上，训练两个独立的潜在世界模型，分别面向感知/预测和规划任务。

#### 高斯流引导的潜在世界模型

该模型显式预测每个高斯的局部动态位移流 $\Delta \mu_k^t$，并结合自车运动变换 $\mathbf{T}_{ego}^{t \to t+1}$ 将当前高斯中心传播至下一帧：

$$\boldsymbol{\mu}_{k}^{t+1} = \mathbf{T}_{ego}^{t \to t+1} ( \boldsymbol{\mu}_{k}^{t} + \Delta \boldsymbol{\mu}_{k}^{t} ) \tag{5}$$

传播后的高斯经 BEV 栅格化生成预测的未来潜在 BEV 特征 $\hat{B}_{t+1}$，以冻结感知网络从下一帧真实图像提取的 BEV 特征 $B_{t+1}$ 作为自监督目标：

$$\mathcal{L}_{bev} = \| \hat{B}_{t+1} - B_{t+1} \|_2 \tag{6}$$

此设计的关键在于：高斯查询具有排列等价性，直接对查询特征施加时序一致性约束会因匹配歧义而失效；通过在高斯几何空间显式建模流并传播，再在 BEV 潜在空间进行监督，绕开了这一瓶颈。

#### 自车规划引导的潜在世界模型

该模型在规划分支中引入未来场景的条件化预测。首先，可学习的路径点查询 $Q_{wp}$ 与当前场景查询 $Q_{scene}^t$ 交叉注意力后，经 MLP 头输出预测轨迹 $\hat{\mathbf{T}}$。随后，通过运动感知层归一化（Motion-Aware Layer Normalization, MLN）将预测轨迹编码为条件信号，调制当前场景查询以预测下一帧场景查询。轨迹预测采用模仿学习回归损失：

$$\mathcal{L}_{reg} = \| \hat{\mathbf{T}} - \mathbf{T} \|_1 \tag{7}$$

规划分支的总损失为回归损失与 BEV 预测损失之和：

$$\mathcal{L}_{plan} = \mathcal{L}_{reg} + \mathcal{L}_{bev} \tag{8}$$

### 双模型解耦的必要性

两个世界模型在训练时相互独立。消融实验（Table 7）表明，将二者合并为统一模型会导致感知 mIoU 从 19.3 降至 18.9，规划 L2 从 0.46 升至 0.58。原因在于：高斯流引导的模型需要精确建模场景中所有动态元素的细粒度运动，而规划引导的模型仅需关注自车运动对场景观测的条件化影响，二者目标存在本质冲突，解耦是性能提升的关键设计选择。



## 实验与关键发现

### 核心性能验证

DLWM在nuScenes数据集上对三大下游任务均取得一致且显著的提升。所有实验均基于**GaussianFormer**作为3D高斯感知骨干，且预训练过程完全不使用任何下游任务标签。

**3D占据感知**（Table 1）：在SurroundOcc-nuScenes验证集上，DLWM预训练将mIoU从基线20.83提升至21.85（+1.02），IoU从31.77提升至34.61（+2.84）。这一提升仅来自两阶段自监督预训练，未引入额外标注数据或模型结构修改。

**4D占据预测**（Table 2）：在1s/2s/3s未来帧的平均指标上，DLWM的mIoU从15.09跃升至17.77（+2.68），IoU从25.65提升至30.60（+4.95）。值得注意的是，DLWM在3s时刻的IoU（28.49）已接近基线在1s时刻的水平（29.60），表明时序世界模型有效缓解了长时预测的退化问题。

**运动规划**（Table 3）：在nuScenes验证集上，DLWM将平均L2距离从0.55降至0.46（-0.09），碰撞率从0.24降至0.19（-0.05）。与使用激光雷达的端到端方法相比，DLWM在不使用自车状态信息的条件下取得了具有竞争力的规划性能。

### 消融实验：双潜在世界模型的解耦设计

Table 7直接对比了“统一模型”（Unified）与“双模型”（Dual）两种架构。统一模型将高斯流预测与自车规划集成于同一世界模型，而双模型则分别训练两个独立的世界模型。结果表明：双模型在3D占据感知上mIoU为19.3（vs. 统一模型18.9），在规划上L2为0.46（vs. 0.58），碰撞率为0.19（vs. 0.22）。解耦设计允许两个世界模型分别专注于场景几何/语义演化和自车轨迹的条件化预测，避免了优化冲突，是性能提升的关键架构选择。

### 消融实验：阶段一渲染监督与高斯流

Table 4系统拆解了阶段一重建监督信号与阶段二高斯流预测的贡献。基线（仅稀疏深度监督）的mIoU为18.83。依次加入稠密伪深度监督（+0.22）、语义监督（+0.14）后，mIoU提升至19.19。进一步引入高斯流引导的潜在世界模型后，mIoU达到19.30，IoU达到30.56。这表明：
- 多模态重建信号（稀疏深度、稠密深度、语义）对学习鲁棒的高斯表示均有正向贡献；
- 阶段二的时序预测在强重建表示的基础上带来额外增益，验证了世界模型对场景动态建模的有效性。

### 消融实验：自车规划引导的潜在世界模型

Table 5聚焦于规划分支的消融。基线（直接从高斯渲染的BEV特征规划，无预训练）的平均L2为0.61，碰撞率为0.30。加入阶段一预训练后，L2降至0.55，碰撞率降至0.24。进一步引入BEV未来预测后，L2降至0.46，碰撞率降至0.19。这揭示了两个关键机制：阶段一重建为规划提供了更鲁棒的场景表示；阶段二的BEV预测使模型能够隐式推理未来场景状态，从而生成更安全、更准确的轨迹。

### 消融实验：数据规模与超参数

**预训练数据量**（Table 6）：随着预训练数据比例从25%增至100%，3D占据感知mIoU从19.19单调提升至19.98。这一趋势表明DLWM预训练具有明确的数据扩展性，尚未出现性能饱和。

**高斯数量**（Table 8）：在12,800至51,200的范围内，25,600个高斯在IoU上达到最优（30.56），51,200虽mIoU略高（19.35 vs. 19.30）但IoU下降至29.97。论文选择25,600作为精度与效率的平衡点。

**预测未来帧数**（Table 9）：预测1帧未来时性能最佳（mIoU 19.30, IoU 30.56），预测3帧时mIoU降至18.64，IoU降至28.80。过多的预测帧数可能因场景变化剧烈而引入噪声，反而损害表示学习质量。

### 计算成本分析

Table 10报告了三项任务的计算开销。在NVIDIA A100 GPU上，预训练阶段一约需18小时，阶段二两个世界模型各需约6小时。下游微调时，3D占据感知、4D占据预测和运动规划的单帧推理延迟分别为0.12s、0.15s和0.08s，满足实时性要求。

### 失败模式与局限

尽管DLWM展现了全面的性能提升，分析中仍识别出以下局限：
1. **LiDAR依赖**：阶段一的稀疏深度监督依赖LiDAR点云，限制了该方法在纯视觉场景下的直接应用。
2. **伪真值噪声**：Metric3D伪稠密深度和Grounded SAM自动语义标签可能引入噪声，在边缘场景（如细长物体、透明表面）中表现不佳。
3. **数据集单一性**：所有实验仅在nuScenes上进行，其在Waymo Open Dataset或nuPlan等更大规模、更多样场景下的泛化性有待验证。
4. **规划性能差距**：尽管L2误差显著降低，但与使用多辅助任务（如检测、跟踪、地图预测）的端到端方法相比，DLWM的规划指标仍有一定差距，表明纯自监督预训练在规划任务上尚未完全替代任务特定监督。
5. **里程计依赖**：高斯流传播依赖真实自车运动变换，在线推理时需准确的里程计估计，里程计误差会传播至未来预测。

### 补充图表

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/004_Table_1.jpg]]
*Table 1: 3D occupancy perception results on the SurroundOcc-nuScenes validation set [39]. *: We re-evaluate the checkpoints released by GaussianWorld because they repeatedly calculated the metrics for intermediate time-interval frames within each video*

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/005_Table_2.jpg]]
*Table 2: 4D occupancy forecasting results on the SurroundOcc-nuScenes validation set [39]. Aux. Sup. represents auxiliary supervision. Avg. computes the average result of 1s, 2s, and 3s*

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/006_Table_3.jpg]]
*Table 3: Motion Planning Results on the nuScenes validation set. The metrics are computed by the way in VAD [15]. ⋄: Lidar-based methods. We do not utilize ego status in the planning module*

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/007_Table_4.jpg]]
*Table 4: Ablation study on render supervision and latent world model guided by Gaussian flow. “Sup-DL”: sparse depth supervision derived from LiDAR points. “Sup-D”: dense pseudo-depth map supervision. “Sup-S”: semantics supervision. “Gaussian Flow”: denotes the inclusion of the Stage 2 latent world model guided by Gaussian flow*

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/008_Table_5.jpg]]
*Table 5: Ablation study on latent world model guided by ego planning. Latent BEV: planning with latent BEV rendered from 3D Gaussians. BEV Forecasting: future latent BEV forecasting integrated into planning. Stage-1 Pretrain: image reconstruction*

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/009_Table_6.jpg]]
*Table 6: Ablation study on data scale. 3D occupancy perception performance under different pre-training data scales*

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/010_Table_7.jpg]]
*Table 7: Ablation study on “Dual” and “Unified”*

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/011_Table_8.jpg]]
*Table 8: Ablation study on the number of 3D Gaussians*

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/012_Table_9.jpg]]
*Table 9: Ablation study on the number of future frames*

![[assets/figures/papers/paper_list_l2465_https_arxiv_org_abs_2604_00969/figures/013_Table_10.jpg]]
*Table 10: The computation cost analysis of all three tasks*



## 定位与知识库关联

### 一、与现有工作的关系

**DLWM** 的定位是首个面向高斯中心（Gaussian-centric）自动驾驶模型的整体自监督预训练范式。其方法谱系可从三个维度追溯：

**1. 高斯中心感知模型。** DLWM 直接建立在 **GaussianFormer** 的 3D 高斯场景表示之上——该工作首次将 3D Gaussian Splatting 引入占据感知，用可学习的高斯查询替代稠密体素或 BEV 网格。然而 GaussianFormer 仅做单帧感知，没有预训练机制，其高斯表示完全依赖任务特定标注训练。DLWM 在保留高斯查询的排列等价性（permutation equivariance）的前提下，为其设计了阶段一的重建预训练和阶段二的时序世界模型，使同一套高斯表示可同时服务于感知、预测和规划三个下游任务。

**2. 世界模型与占据预测。** 在 4D 占据预测方面，**OccWorld** 是代表性基线，它直接在 3D 体素空间学习世界模型以预测未来占据。DLWM 与之的核心差异在于：(a) 世界模型作用在潜在空间（高斯特征和 BEV 特征）而非显式占据体素上；(b) 世界模型被解耦为两个独立分支——高斯流引导的几何/语义演化模型和自车规划引导的场景条件化模型，而非使用单一统一模型。消融实验（Table 7）证实，解耦设计使感知 mIoU 从 18.9 提升至 19.3，规划 L2 从 0.58 降至 0.46。

**3. 端到端运动规划。** 在规划方面，DLWM 与 **VAD**、**BEV-Planner** 和 **LAW** 等基线形成对比。VAD 和 BEV-Planner 依赖多辅助任务（检测、跟踪、建图）的监督信号，LAW 则在 BEV 潜在空间学习世界模型用于规划。DLWM 的独特之处在于：(a) 规划分支仅使用模仿学习回归损失和 BEV 预测损失，不引入任何辅助任务监督；(b) 规划模块通过运动感知层归一化（Motion-Aware Layer Normalization）将预测的自车轨迹条件化到场景查询中，实现“规划引导的场景预测”，而非简单的“场景预测后规划”。

### 二、适用边界与关键假设

DLWM 的有效性依赖以下前提条件，这些条件也划定了其适用边界：

- **LiDAR 数据可用性。** 阶段一的稀疏深度监督来自 LiDAR 点云投影，阶段二的高斯流传播依赖真实自车运动（GT ego motion）进行帧间对齐。在缺乏 LiDAR 或高精度里程计的场景（如纯视觉低成本平台），这两项监督信号无法直接获取，预训练效果可能退化。论文明确将此列为局限性之一。

- **伪真值质量。** 阶段一同时使用 Metric3D 生成的伪稠密深度图和 Grounded SAM 生成的自动语义标签作为辅助监督。这些伪真值在 nuScenes 等标准数据集上质量较高，但在域外场景（如极端天气、非结构化道路）可能引入噪声，影响预训练表示质量。

- **高斯数量的经验选择。** 消融实验（Table 8）表明，高斯数量从 12,800 增至 25,600 时 IoU 提升至最优（30.56），但继续增至 51,200 时 IoU 反而下降。这意味着高斯表示存在一个与场景复杂度和计算预算相关的“甜区”，在不同数据集或感知范围下需要重新标定。

- **单帧预测假设。** 阶段二的潜在世界模型仅预测未来 1 帧效果最佳（Table 9，mIoU 19.30），预测更多帧时性能下降，论文归因于“场景变化太大”。这表明当前世界模型对长时域动态建模能力有限，适合短时域（~0.5s）场景预测，不适用于长期轨迹预测。

- **数据集验证范围。** 所有实验仅基于 nuScenes 数据集（SurroundOcc 标注），未在 Waymo Open Dataset、nuPlan 或更复杂的城市/高速场景验证。跨数据集的泛化性尚不明确。

### 三、局限性与开放问题

**已确认的局限性：**

1. **LiDAR 依赖瓶颈。** 预训练流程强依赖 LiDAR 提供稀疏深度监督和真实自车运动，限制了其在纯视觉系统上的直接应用。
2. **伪真值噪声。** Metric3D 和 Grounded SAM 的预测误差会通过渲染损失反向传播至高斯表示，可能成为性能上界约束。
3. **规划性能仍有差距。** 尽管预训练使规划 L2 从 0.55 降至 0.46，但与使用多辅助任务监督的端到端方法相比，L2 误差仍略高，说明自监督预训练尚不能完全弥补任务特定监督的增益。
4. **计算开销。** 两阶段预训练 + 三个下游任务的微调增加了整体训练成本（Table 10 有计算分析，但具体数值需核实原文）。

**开放问题：**

1. **跨架构泛化性。** 当前预训练范式针对 GaussianFormer 架构设计，能否直接迁移至其他高斯中心模型（如 GaussianAD、GaussianWorld）或其他 3D 表示（如 Triplane、NeRF-based）尚未验证。
2. **纯自监督世界模型。** 能否设计完全无需 LiDAR 或伪真值的时序世界模型？例如利用多视图光度一致性或时间对比学习替代深度/语义监督。
3. **大规模数据扩展性。** 消融实验（Table 6）显示数据量从 25% 增至 100% 时 mIoU 从 15.05 持续提升至 19.98，未出现饱和，暗示更大规模数据可能带来进一步增益，但在百万级数据上的扩展行为未知。
4. **双世界模型的统一。** 当前解耦设计虽优于统一模型，但增加了训练复杂度。是否可能设计一个统一的世界模型同时预测高斯流和自车规划，且保持性能不退化？
5. **鲁棒性评估缺失。** 论文未评估在遮挡、恶劣天气、动态 agent 密集交互等 corner case 下的预训练增益，这些场景下的表示鲁棒性尚不明确。
6. **在线推理的里程计需求。** 高斯流传播依赖真实自车运动进行帧间对齐，在线推理时需要准确的视觉里程计或 IMU 积分，这一依赖在实际部署中的影响未讨论。



## 原文 PDF

![[paperPDFs/CVPR_2026/DLWM_Dual_Latent_World_Models_enable_Holistic_Gaussian_centric_Pre_training_in_Autonomous_Driving.pdf]]
