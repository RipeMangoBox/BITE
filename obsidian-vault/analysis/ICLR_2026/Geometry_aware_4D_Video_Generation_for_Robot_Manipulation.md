---
title: Geometry-aware 4D Video Generation for Robot Manipulation
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Geometry_aware_4D_Video_Generation_for_Robot_Manipulation_dceab2ee24a9.pdf
project_link: "https://robot4dgen.github.io/"
code_link: "https://github.com/ToyotaResearchInstitute/lbm_eval"
aliases:
- GA4VGO
- GA4VGRM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion
core_operator: 在训练时通过跨视角点云图对齐（将第二视角点云投影到参考视角坐标系并最小化与参考点云的差异）引入几何监督，使模型学习共享的三维场景表示；同时利用双分支U‑Net中的多视角交叉注意力实现信息传递。这样在推理时模型能直接生成几何一致的多视角RGB‑D视频，无需相机外参。
primary_logic: 将点云图作为三维几何约束融入预训练的视频扩散模型，联合优化RGB视频扩散损失和点云一致性损失，使模型在保留时序建模先验的同时，获得跨视角的空间对齐能力，从而实现时空一致的4D视频生成。
claims:
- 移除多视角交叉注意力后，跨视角mIoU在Task 1上从0.70骤降至0.41，深度指标（AbsRel-m）从0.11恶化至0.31。
- 所提方法在三个仿真任务上的平均操作成功率达到0.64，而最佳基线仅为0.25。
- 定性对比显示，基线方法在新视角下出现明显的跨视角不一致或人工伪影，而本方法生成的结果几何一致、视觉保真度高。
- StoreCerealBoxUnderShelf (Task 1) 上 FVD-n（视频生成质量） = 411.20
---

# Geometry-aware 4D Video Generation for Robot Manipulation

> [!tip] 核心洞察
> 将点云图作为三维几何约束融入预训练的视频扩散模型，联合优化RGB视频扩散损失和点云一致性损失，使模型在保留时序建模先验的同时，获得跨视角的空间对齐能力，从而实现时空一致的4D视频生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向机器人操作的几何感知4D视频生成 |
| 英文题名 | Geometry-aware 4D Video Generation for Robot Manipulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=18gC6pZVVc) · [Project](https://robot4dgen.github.io/) · [Code](https://github.com/ToyotaResearchInstitute/lbm_eval) · [arXiv](https://arxiv.org/abs/2408.00714) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion |
| Method | Geometry-aware 4D Video Generation (Ours) |
| Dataset | StoreCerealBoxUnderShelf |

> [!tip] 效果简介
> - StoreCerealBoxUnderShelf (Task 1) 上，FVD-n（视频生成质量） 411.20 vs SVD: 977.06 (-565.86)；AbsRel-n（深度预测误差） 0.06 vs 4D Gaussian: 0.20 (-0.14)。
> - 三个仿真任务平均 上，操作成功率 0.64 vs DP3: 0.25 (+0.39)。

## 概述

机器人操作任务要求模型同时理解场景的时间动态与三维空间结构。现有视频生成模型虽能产生时序连贯的像素序列，却缺乏对底层3D几何的显式建模，导致跨视角预测时出现严重的空间不一致；而3D感知方法多局限于静态场景或单物体重建，难以处理多物体交互的动态操作环境。

针对这一瓶颈，本文提出**几何感知的4D视频生成方法**，其核心机制是在预训练视频扩散模型（Stable Video Diffusion）中引入跨视角点云图对齐监督：训练时，将第二视角的点云投影到参考视角坐标系，并与参考视角点云联合施加扩散损失，迫使模型学习共享的三维场景表示；同时，在U‑Net解码器中插入多视角交叉注意力层，实现视角间的信息传递。推理时，模型可直接从两路RGB‑D观测中联合生成几何一致的多视角RGB‑D视频，无需已知相机外参。

主要结果如下：
- **视频生成质量与几何一致性**：在仿真任务StoreCerealBoxUnderShelf上，本方法的FVD‑n降至411.20（SVD为977.06），跨视角mIoU达到0.70；移除多视角交叉注意力后，mIoU骤降至0.41，深度指标AbsRel‑m从0.11恶化至0.31，验证了该模块的关键作用。
- **机器人操作成功率**：在三个仿真任务上，本方法的平均操作成功率达0.64，而最佳基线DP3仅为0.25，提升幅度超过一倍。
- **定性表现**：在新视角下，基线方法普遍出现明显的跨视角不一致或人工伪影，而本方法生成的RGB‑D视频在时空维度上均保持高保真度和几何一致性。

本方法在方法谱系上属于**几何监督增强的视频扩散模型**，区别于纯像素级的视频生成基线（如SVD）和基于4D高斯重建的显式场景表示方法。其知识贡献在于将DUSt3R式的跨视图点云对齐策略融入时序扩散框架，实现了从“生成视频”到“生成4D场景流”的能力跃迁，为机器人操作提供了一种可提取6DoF末端执行器轨迹的视觉规划前端。

## 背景与动机

机器人操作任务要求智能体在动态三维环境中精确感知物体几何、推理空间关系并执行时序连贯的动作。视觉感知作为核心环节，其质量直接影响下游策略的成败。近年来，视频生成模型在视觉内容合成上取得了显著进展，为机器人领域提供了通过预测未来视觉观测来辅助决策的新范式。然而，将通用视频生成模型直接应用于机器人操作面临一个根本性瓶颈：**现有模型难以同时保证时间连贯性和跨视角三维几何一致性，尤其对于多物体的动态操作场景。**

具体而言，以 **SVD**（Blattmann et al., 2023）为代表的像素级视频扩散模型虽然具备强大的时序建模先验，但其缺乏对三维场景结构的显式理解，各视角独立预测，无法保证不同相机视角下生成的RGB帧在空间上对齐。另一方面，**4D Gaussian**（Wang et al., 2024a）等3D感知方法虽然能够重建动态场景的几何表示，却局限于静态或简单背景，难以泛化至包含复杂物体交互和机器人运动的操作场景。这种“时序连贯”与“空间一致”之间的割裂，构成了当前4D视频生成在机器人领域应用的核心缺口。

本工作的动机正是弥合这一缺口：**在保留预训练视频扩散模型时序建模能力的同时，引入三维几何约束，使模型能够生成跨视角几何一致的4D视频（RGB‑D序列）。** 这一动机源于一个关键观察——点云图（pointmap）作为一种显式的三维几何表示，可以直接从深度观测中获取，且天然支持跨视角坐标变换。通过将点云图作为几何监督信号融入扩散训练，模型有望在无需推理时相机外参的条件下，输出时空一致的未来观测，从而为下游机器人操作策略提供可靠的感知基础。

## 核心创新

### 从像素生成到几何感知的4D视频建模

现有视频生成模型（如 **SVD**（Blattmann et al., 2023））在单视角时序预测上表现强劲，但面对多视角机器人操作场景时，缺乏对三维空间结构的理解，导致跨视角几何不一致。纯3D重建方法（如 **4D Gaussian**（Wang et al., 2024a））虽能建模场景几何，却难以同时保持长时序的动态连贯性和视觉保真度。本工作的核心创新在于将**点云图作为显式三维几何约束**融入预训练的视频扩散模型，使模型在保留时序建模先验的同时获得跨视角空间对齐能力，从而直接生成时空一致的4D RGB-D视频。

### 关键改变槽位

| 改变槽位 | 基线方法 | 本方法 | 证据锚点 |
|---------|---------|-------|---------|
| **预测模态** | 仅RGB帧 | 同时生成RGB帧和3D点云图 | Section 1, Section 3.2 |
| **多视角处理机制** | 各视角独立预测，无显式几何约束 | 跨视角点云投影对齐 + U-Net解码器多视角交叉注意力 | Section 3.2, Figure 5 |
| **训练目标** | 仅RGB视频扩散损失 | 联合优化RGB扩散损失和点云3D一致性损失（λ=1） | Equation (3), Section 3.3 |

### 几何一致性监督：跨视角点云对齐

本方法的核心机制借鉴了 **DUSt3R**（Wang et al., 2024b）的跨视角点图监督策略，并将其适配到视频生成场景。具体而言，模型接收两个视角的RGB-D历史观测，在训练时不仅预测参考视角 $v_n$ 的未来点云图 $\mathbf{X}_{t'}^n$，还预测第二视角 $v_m$ 的点云图，并利用已知相机外参将其投影到参考坐标系得到 $\mathbf{X}_{t'}^{m \to n}$。通过在投影后的点云上施加扩散损失，强制模型学习跨视角的三维场景共享表示：

$$
\mathcal{L}_{\mathrm{3D-diff}}(t') = \mathbb{E}_{\epsilon_{t'}^{n},\mathbf{z}_{t'}^{n}(0),k}\left[\|\mathbf{z}_{t'}^{n}(0)-f_\theta(\mathbf{z}_{t'}^{n}(k),k,c^{n})\|^2\right] + \mathbb{E}_{\epsilon_{t'}^{m},\mathbf{z}_{t'}^{m\to n}(0),k}\left[\|\mathbf{z}_{t'}^{m\to n}(0)-f_\theta(\mathbf{z}_{t'}^{m\to n}(k),k,c^{m})\|^2\right]
$$

这一设计的核心洞察在于：**点云图天然编码了场景的三维几何信息，将其作为训练信号使得模型必须理解物体的空间位置和形状，而非仅拟合像素纹理**。值得注意的是，相机外参仅在训练时用于点云投影，推理阶段模型可直接生成几何一致的多视角视频，无需任何相机标定信息。

### 多视角交叉注意力：信息传递的桥梁

为实现跨视角信息的高效传递，本方法在U-Net扩散模型的解码器中引入了**多视角交叉注意力机制**（Figure 5）。具体而言，为视角 $v_m$ 的每个解码器块插入交叉注意力层，使其能够查询参考视角 $v_n$ 对应层的特征。这种设计允许模型在生成过程中动态融合两个视角的信息，从而学习跨视角的几何对应关系。

消融实验提供了强有力的因果证据：**移除多视角交叉注意力后，跨视角mIoU在Task 1上从0.70骤降至0.41，深度指标δ1-m从0.92恶化至0.66**（Table 1, Section 4.2）。这表明，仅有点云投影损失而无交叉注意力时，模型难以准确建立跨视角的空间对应——第二视角的点云无法正确转换到参考坐标系。更重要的是，该模块仅轻微增加参数量（2.38B → 2.4B）和推理时间（29.3s → 30.0s），却带来了几何一致性和生成质量的显著提升（Table 3, Section A.3）。

### 联合训练目标：时空一致性的保障

完整的训练目标将RGB视频扩散损失与点云3D一致性损失统一在时域和视角维度上联合优化：

$$
\mathcal{L} = \sum_{t'=t+1}^{t+h}\left[\underbrace{\mathcal{L}_{\mathrm{diff}}^{n}(t')+\mathcal{L}_{\mathrm{diff}}^{m}(t')}_{\mathrm{RGB\ loss}} + \lambda \cdot \underbrace{\mathcal{L}_{\mathrm{3D-diff}}(t')}_{\mathrm{pointmap\ loss}}\right]
$$

其中 $\lambda=1$，RGB损失保证时序连贯性和视觉质量，点云损失强制跨视角几何对齐。这种设计形成了一个**时空一致性闭环**：时序维度上，扩散模型继承了SVD的连贯视频生成先验；空间维度上，点云投影和交叉注意力共同约束了多视角间的三维一致性。定性对比（Figure 3, Figure 11, Figure 12）显示，基线方法在新视角下出现明显的跨视角不一致或人工伪影，而本方法生成的RGB-D视频在几何对齐和视觉保真度上均显著优于基线。

### 创新总结

本方法的核心贡献可归纳为三点：**(1)** 首次将点云图作为三维几何约束引入视频扩散模型，实现了从“像素生成”到“几何感知生成”的范式转变；**(2)** 通过跨视角点云投影对齐和多视角交叉注意力的协同设计，使模型在无需推理时相机外参的情况下生成几何一致的多视角视频；**(3)** 联合优化RGB时序损失和点云空间损失，在保留预训练视频先验的同时获得跨视角空间理解能力。这一创新路径直接解决了现有方法“时间连贯性”与“空间一致性”难以兼得的瓶颈问题。

## 整体框架

### 问题形式化与输入输出

给定两个同步采集的RGB‑D相机视角 $v_n$（参考视角）与 $v_m$（辅助视角），以及长度为 $t$ 的历史观测序列，模型的目标是预测未来 $h$ 帧的4D视频——即同时输出两个视角的RGB视频流和3D点云图序列，且所有点云均统一表达在参考视角 $v_n$ 的相机坐标系下。这一形式化使得生成的RGB‑D内容天然具备跨视角的几何一致性，为下游机器人位姿提取提供了可靠的三维基础。

### 整体Pipeline架构

方法的核心架构可概括为“双流编码—共享扩散去噪—双流解码”的级联式Pipeline，具体包含以下功能模块：

1. **图像VAE编码器**：将历史RGB帧压缩为潜在表示，降低扩散模型在高维像素空间中的计算开销。
2. **点云VAE编码器**：将历史点云图（从深度图反投影得到）编码为潜在表示，为三维几何监督提供隐空间特征。
3. **条件U‑Net扩散模型**：这是Pipeline的中央处理单元。它以历史RGB和点云的潜在表示为条件，通过迭代去噪过程同时生成未来RGB和点云的潜在帧。模型包含独立权重的双视图解码器分支，并在解码器中插入多视角交叉注意力层，实现参考视角与辅助视角之间的信息传递。
4. **图像VAE解码器**：将预测的RGB潜在表示解码回像素空间，生成未来RGB帧。
5. **点云VAE解码器**：将预测的点云潜在表示解码为3D点云图。
6. **6DoF位姿跟踪器**（基于FoundationPose）：从生成的RGB‑D视频中提取机器人末端执行器的6自由度轨迹及夹爪开合状态，将生成的4D内容转化为可执行的操作策略。

### 输入输出数据流

数据流沿时间轴和视角轴两个维度展开：

- **输入端**：两个视角的 $t$ 帧历史RGB图像 $\{I_1^n, \dots, I_t^n\}$、$\{I_1^m, \dots, I_t^m\}$ 以及对应的点云图 $\{X_1^n, \dots, X_t^n\}$、$\{X_1^m, \dots, X_t^m\}$，其中 $X_t^n \in \mathbb{R}^{W \times H \times 3}$ 表示参考视角下每个像素的三维坐标。
- **编码阶段**：RGB和点云分别经各自的VAE编码器映射为潜在变量 $\mathbf{z}_t^n$ 和 $\mathbf{z}_t^m$（RGB通道）以及 $\mathbf{z}_t^{n,\text{pt}}$、$\mathbf{z}_t^{m,\text{pt}}$（点云通道）。
- **扩散去噪阶段**：条件U‑Net以历史潜在序列为条件，从噪声中逐步恢复未来 $h$ 帧的干净潜在表示。对于参考视角 $v_n$，直接预测其RGB和点云潜在变量；对于辅助视角 $v_m$，除预测其自身RGB和点云潜在变量外，还额外预测其点云在参考视角坐标系下的投影版本 $\mathbf{z}_{t'}^{m \to n}(0)$，此投影通过已知的相机外参实现。
- **解码阶段**：所有预测的潜在变量经对应VAE解码器还原为像素空间的RGB帧和点云图，形成完整的4D视频。
- **位姿提取阶段**：FoundationPose跟踪器在生成的RGB‑D序列上运行，输出末端执行器的6DoF位姿轨迹和夹爪状态，直接驱动机器人执行操作任务。

### 关键设计决策

Pipeline的两个核心设计决策直接决定了跨视角几何一致性的实现效果：

1. **跨视角点云投影与联合监督**：训练时，辅助视角 $v_m$ 的点云被显式投影到参考视角 $v_n$ 的坐标系下，并与 $v_n$ 自身的点云一同施加扩散损失。这一机制强制模型学习共享的三维场景表示，使得推理时即使不依赖相机外参，也能生成几何对齐的多视角点云。该设计的思想源自DUSt3R（Wang et al., 2024b）的跨视图点云对齐策略，但被首次适配到视频生成场景中。

2. **多视角交叉注意力**：在U‑Net解码器的每个解码块之后插入交叉注意力层，允许辅助视角 $v_m$ 的解码器特征查询参考视角 $v_n$ 的对应特征。这一轻量级设计（仅增加0.02B参数，推理时间从29.3s微增至30.0s）是学习跨视角三维几何对应的关键——消融实验表明，移除该模块后跨视角mIoU从0.70骤降至0.41，深度指标AbsRel‑m从0.11恶化至0.31。

### 训练与推理流程

**训练阶段**：模型在已知相机外参的多视角RGB‑D视频数据上进行端到端训练，联合优化RGB视频扩散损失 $\mathcal{L}_{\mathrm{diff}}$ 和点云3D一致性损失 $\mathcal{L}_{\mathrm{3D-diff}}$，总损失为二者在时间维度和两个视角上的加权求和（权重 $\lambda=1$）。训练所需的相机外参仅用于点云投影监督，不参与推理。

**推理阶段**：给定两个视角的历史RGB‑D观测，模型直接生成未来 $h$ 帧的RGB视频和点云图，无需相机外参。多视角推断目前采用逐对前向传播的方式，延迟与视角数呈线性关系。生成的4D视频随后输入位姿跟踪器，提取的末端执行器轨迹以开环方式执行操作任务。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/001_Figure_1.jpg]]
*Figure 1: Geometry-aware 4D Video Generation. Our model takes RGB-D observations from two camera views and predicts future 4D pointmaps in the coordinate frame of the reference view*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/002_Figure_2.jpg]]
*Figure 2: 4D Video Generation for Robot Manipulation. Our model takes RGB-D observations from two camera views, and predicts future pointmaps and RGB videos. To ensure cross-view consistency, we apply cross-attention in the U-Net decoders for pointmap prediction. The resulting 4D video can be used to extract the 6DoF pose of the robot end-effector using pose tracking methods, enabling downstream manipulation tasks*

## 核心模块与公式推导

### 方法概览

本方法以预训练的**SVD**（Blattmann et al., 2023）视频扩散模型为基础，将其扩展为同时预测未来RGB帧和3D点云图（pointmap）的4D视频生成框架。模型输入为两个相机视角的RGB-D历史观测，输出为参考视角坐标系下的未来RGB视频及对应的4D点云序列（Figure 1、Figure 2）。

点云图定义为逐像素的3D坐标：

$$\mathbf{X}_t^n \in \mathbb{R}^{W \times H \times 3}$$

其中 $\mathbf{X}_t^n$ 表示时刻 $t$、视角 $v_n$ 下的点云图，每个像素存储该点在相机坐标系中的 $(x, y, z)$ 坐标。

### 核心模块

#### 1. 双分支VAE编码-解码

模型包含两套独立的VAE编码器和解码器，分别处理RGB帧和点云图：

- **图像VAE编码器**：将历史RGB帧压缩为潜在表示，降低扩散模型的计算开销。
- **点云VAE编码器**：将历史点云图编码为潜在表示，为几何监督提供紧凑的特征空间。
- **图像VAE解码器**：将扩散模型预测的RGB潜在表示解码为未来RGB帧。
- **点云VAE解码器**：将预测的点云潜在表示解码为未来点云图。

#### 2. 条件U-Net扩散模型

核心生成模块为条件U-Net，基于历史潜在表示去噪生成未来潜在帧。U-Net包含**独立的双视图解码器**，分别处理参考视角 $v_n$ 和第二视角 $v_m$ 的输出。两个解码器架构相同但权重独立。

#### 3. 多视角交叉注意力

为确保跨视角几何一致性，在U-Net中 $v_m$ 视角的每个解码器块之后插入交叉注意力层（Figure 5），使 $v_m$ 分支能够交叉关注 $v_n$ 分支的特征：

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/007_Figure_5.jpg]]
*Figure 5: Multi-View Cross-Attention. We insert a cross attention layer after each decoder block in the U-Net diffusion model for view*

> 具体而言，$v_m$ 解码器中的交叉注意力层以 $v_n$ 对应解码器块的特征作为键（Key）和值（Value），以 $v_m$ 自身的特征作为查询（Query），实现视角间的信息传递。

该模块仅增加约0.02B参数量（从2.38B增至2.4B），推理时间仅增加0.7秒（从29.3s增至30.0s），但带来了跨视角一致性的显著提升（Table 3）。

#### 4. 6DoF位姿跟踪器

从生成的RGB-D视频中提取机器人末端执行器的6DoF轨迹，采用**FoundationPose**作为位姿跟踪器（Section 3.4）。该模块通过匹配生成的点云与实际机器人几何模型，估计末端执行器的平移和旋转，同时从RGB帧中推断夹爪开合状态。

### 关键公式推导

#### 公式1：RGB视频扩散损失

标准扩散模型训练目标，从加噪潜在变量预测原始干净潜在变量：

$$\mathcal{L}_{\mathrm{diff}}(t') = \mathbb{E}_{\epsilon_{t'},\mathbf{z}_{t'}(0),k}\left[\|\mathbf{z}_{t'}(0)-f_\theta(\mathbf{z}_{t'}(k),k)\|^2\right]$$

其中：
- $t' \in \{t+1, \dots, t+h\}$ 为预测的未来时间步
- $\mathbf{z}_{t'}(0)$ 为时刻 $t'$ 的干净潜在变量
- $\mathbf{z}_{t'}(k)$ 为加噪 $k$ 步后的潜在变量
- $f_\theta$ 为去噪网络
- 该损失对RGB帧的每个视角独立计算

#### 公式2：3D一致性扩散损失

核心创新——跨视角点云对齐监督，强制模型学习共享的三维场景表示：

$$\mathcal{L}_{\mathrm{3D-diff}}(t') = \mathbb{E}_{\epsilon_{t'}^{n},\mathbf{z}_{t'}^{n}(0),k}\left[\|\mathbf{z}_{t'}^{n}(0)-f_\theta(\mathbf{z}_{t'}^{n}(k),k,c^{n})\|^2\right] + \mathbb{E}_{\epsilon_{t'}^{m},\mathbf{z}_{t'}^{m\to n}(0),k}\left[\|\mathbf{z}_{t'}^{m\to n}(0)-f_\theta(\mathbf{z}_{t'}^{m\to n}(k),k,c^{m})\|^2\right]$$

其中：
- $\mathbf{z}_{t'}^{n}(0)$ 为参考视角 $v_n$ 的点云潜在变量
- $\mathbf{z}_{t'}^{m\to n}(0)$ 为第二视角 $v_m$ 的点云经相机外参投影到 $v_n$ 坐标系后的潜在变量
- $c^n$、$c^m$ 分别为两个视角的条件信息（历史观测）
- 第一项对参考视角原生点云施加扩散损失
- 第二项对投影后的点云施加扩散损失，迫使模型在 $v_n$ 坐标系下生成一致的3D结构

**关键机制**：训练时将 $v_m$ 视角的点云通过已知相机外参投影到 $v_n$ 坐标系，最小化投影点云与 $v_n$ 原生点云的差异。这使得模型学习到跨视角共享的几何表示，推理时即使不提供外参也能生成几何一致的多视角输出。

#### 公式3：联合训练目标

总损失为RGB扩散损失与点云一致性损失的加权和，在时域和双视角上求和：

$$\mathcal{L} = \sum_{t'=t+1}^{t+h}\left[\underbrace{\mathcal{L}_{\mathrm{diff}}^{n}(t')+\mathcal{L}_{\mathrm{diff}}^{m}(t')}_{\mathrm{RGB\ loss}} + \lambda \cdot \underbrace{\mathcal{L}_{\mathrm{3D-diff}}(t')}_{\mathrm{pointmap\ loss}}\right]$$

其中：
- $\mathcal{L}_{\mathrm{diff}}^{n}(t')$ 和 $\mathcal{L}_{\mathrm{diff}}^{m}(t')$ 分别为两个视角的RGB扩散损失
- $\lambda = 1$，即RGB损失与点云损失等权重
- 求和覆盖所有预测时间步 $h$ 和两个相机视角

### 设计动机与因果机制

**核心瓶颈**：现有视频生成模型（如SVD）虽能生成时序连贯的单视角视频，但缺乏对三维场景结构的理解，导致多视角生成时出现几何不一致——同一物体在不同视角下的位置、形状产生矛盾。

**因果调节变量**：通过在训练时引入跨视角点云对齐监督，将第二视角的点云投影到参考坐标系并最小化与参考点云的差异，迫使模型学习共享的3D场景表示。同时，U-Net中的多视角交叉注意力层提供显式的信息传递通道，使两个视角分支能够协调生成。

**消融证据**：移除多视角交叉注意力后，跨视角mIoU从0.70骤降至0.41（Task 1），深度指标 $\delta_1\text{-}m$ 从0.92降至0.66（Table 1），证实该模块对学习跨视角几何对应至关重要。

## 实验与分析

### 核心瓶颈与验证目标

现有视频生成模型在机器人操作场景中面临一个根本矛盾：像素级生成模型（如SVD）缺乏对三维场景结构的理解，难以保证跨视角的几何一致性；而基于显式3D表示的方法（如4D Gaussian）则局限于静态或简单动态背景，无法有效处理多物体交互的复杂操作时序。本文的实验设计围绕两个核心验证目标展开：（1）所提出的几何感知4D视频生成方法能否在保持高视觉质量的同时，实现跨视角的三维几何一致性；（2）从生成视频中提取的机器人轨迹能否支撑有效的操作策略执行。

### 数据集与评估协议

实验覆盖三个仿真机器人操作任务（StoreCerealBoxUnderShelf、PlaceAppleFromBowlIntoBin、PutSpatulaOnTable）和四个真实世界操作任务。仿真数据使用Robosuite和MimicGen生成，每个任务采集16个相机视角的RGB-D视频，其中12个视角用于训练、4个用于测试。真实世界数据通过双摄像头同步采集。所有模型在相同的多视角RGB-D视频数据集上训练，训练超参数和基模型SVD的初始化保持一致，仅方法本身的架构差异被评估。测试在100个未见过的相机视角下进行，确保评估的公平性和泛化性。

### 多视角4D视频生成质量（Table 1）

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/003_Table_1.jpg]]
*Table 1: Multi-view 4D Video Generation Results. We compare our method with baselines in terms of cross-view consistency, RGB video generation quality, and depth generation quality. Our method consistently enables high-quality video and depth generation while maintaining strong cross-view consistency on both simulated and real-world datasets*

Table 1系统对比了所提方法与三个基线（4D Gaussian、SVD、SVD w/ MV attn）在跨视角一致性、RGB视频质量和深度预测精度三个维度的表现。

**跨视角几何一致性**：在StoreCerealBoxUnderShelf任务上，所提方法达到跨视角mIoU 0.70，而SVD w/ MV attn仅为0.46，4D Gaussian为0.50。这一差距在PlaceAppleFromBowlIntoBin任务上同样显著（0.69 vs. 0.47 vs. 0.44）。mIoU指标直接度量两个视角预测点云在参考坐标系下的空间对齐程度，数值越高表明模型越能学习到共享的三维场景表示。

**视频生成质量**：以FVD-n（参考视角FVD）衡量，所提方法在Task 1上达到411.20，显著优于SVD的977.06和4D Gaussian的1049.17。值得注意的是，SVD w/ MV attn在FVD指标上与所提方法接近（Task 1 FVD-n为474.37），但其跨视角一致性远低于所提方法，说明仅靠多视角交叉注意力不足以同时保证视觉质量和几何一致性——点云一致性损失的联合优化是关键差异化因素。

**深度预测精度**：所提方法在AbsRel-n上达到0.06，而4D Gaussian为0.20，SVD为0.17。δ1-n指标（阈值准确率，比值<1.25视为正确）上，所提方法达到0.93，4D Gaussian仅为0.71。这表明将点云图作为显式几何监督信号，比单纯依赖RGB像素重建能更准确地恢复场景的三维结构。

在真实世界数据集上，所提方法同样保持优势：跨视角mIoU达到0.72，FVD-n为345.51，AbsRel-n为0.07，验证了从仿真到真实的迁移能力。

### 消融实验：多视角交叉注意力的关键作用（Table 1, Table 3）

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/011_Table_3.jpg]]
*Table 3: Quantitative comparisons with baselines in terms of inference time, GPU memory / compute resource consumption and parameter count*

移除多视角交叉注意力（OURS w/o MV attn）导致性能全面退化，这一消融揭示了该方法中信息传递机制的核心地位：

- **几何一致性崩溃**：Task 1跨视角mIoU从0.70骤降至0.41，Task 2从0.69降至0.44。这表明没有跨视角信息传递，模型无法准确建立两个视角间的空间对应关系。
- **深度预测恶化**：Task 1的AbsRel-m从0.11恶化至0.31，δ1-m从0.92降至0.66。模型无法将第二视角的点云正确转换到参考坐标系，导致投影后的深度预测严重偏离真值。
- **视觉质量受损**：FVD-m从561.43升至1185.51，说明几何约束的缺失反过来影响了RGB帧的生成质量，二者存在耦合关系。

Table 3的效率对比进一步表明，多视角交叉注意力仅轻微增加参数量（2.38B → 2.4B）和推理时间（29.3s → 30.0s），却带来了几何一致性和生成质量的显著提升，验证了该设计的高效性。

### 机器人操作成功率（Table 2）

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/006_Table_2.jpg]]
*Table 2: Task Success Rate for Manipulation Tasks*

Table 2展示了从生成4D视频中提取6DoF轨迹后的实际操作表现。所提方法在三个仿真任务上的平均成功率达到0.64，而最佳基线DP3仅为0.25，DP为0.19，Dreamitate为0.09。逐任务分析显示：

- StoreCerealBoxUnderShelf：0.60 vs. DP3 0.20
- PlaceAppleFromBowlIntoBin：0.60 vs. DP3 0.30
- PutSpatulaOnTable：0.73 vs. DP3 0.25

这一结果说明，几何一致的4D视频生成能够为下游操作策略提供更可靠的视觉输入。相比之下，基于视频预测的Dreamitate和基于扩散策略的DP/DP3缺乏对三维场景结构的显式建模，在需要精确空间推理的操作任务中表现受限。

### 定性分析与失败模式

定性对比（Figure 3, Figure 11, Figure 12）显示，基线方法在新视角下出现明显的跨视角不一致或人工伪影：4D Gaussian在动态区域产生模糊或几何畸变，SVD和SVD w/ MV attn在RGB和深度预测中出现跨视角的不对齐。所提方法生成的RGB-D视频在不同视角间保持几何一致，视觉保真度高，尤其在机器人末端执行器的精细运动捕捉上表现突出。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/004_Figure_3.jpg]]
*Figure 3: Qualitative Results and Comparisons under Novel Camera Views. Our method generates geometrically consistent 4D videos across camera views. In contrast, baseline results often exhibit significant cross-view inconsistencies or contain noticeable artifacts in the RGB or depth predictions. Video results can be found on the project website*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/014_Figure_11.jpg]]
*Figure 11: Qualitative Results of PlaceAppleFromBowlIntoBin task. Our method achieves the best RGB video and depth generation quality, with high multi-view consistency. Baseline results often exhibit significant cross-view inconsistencies (marked in red) or contain noticeable artifacts in the RGB or depth predictions*

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/015_Figure_12.jpg]]
*Figure 12: Qualitative Results of PutSpatulaOnTable task. Our method achieves the best RGB video and depth generation quality, with high multi-view consistency. Baseline results often exhibit significant cross-view inconsistencies (marked in red) or contain noticeable artifacts in the RGB or depth predictions*

位姿跟踪误差分析（Figure 13）揭示了方法的主要失败模式：在抓取小物体或存在遮挡的情况下，FoundationPose的跟踪误差增大，导致提取的轨迹偏离真值。这一误差源于生成视频质量与位姿估计器精度的双重依赖，而非方法本身的几何一致性缺陷。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/017_Figure_13.jpg]]
*Figure 13: Analysis of 6-DoF pose-tracking errors. Left: per-action MSE curves for left and right grippers across one representative trajectory from each of the three tasks. Right: visual examples of the five highest-error frames for each task*

### 三视图扩展实验（Table 4）

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/016_Table_4.jpg]]
*Table 4: Performance generating three views simultaneously on StoreCerealBoxUnderShelf*

Table 4展示了将方法从双视图扩展到三视图的结果。在StoreCerealBoxUnderShelf任务上，三视图生成的跨视角一致性（mIoU 0.68）与双视图（0.70）接近，但推理时间随视角数线性增长。这一实验验证了方法的可扩展性，同时暴露了当前逐对前向传播策略的计算瓶颈。

### 方法谱系与知识库定位

该方法处于视频扩散生成与多视角几何重建的交叉地带。其基座模型**SVD**（Blattmann et al., 2023）提供了时序连贯的视频生成先验；几何一致性监督机制借鉴了**DUSt3R**（Wang et al., 2024b）的跨视角点云对齐策略，但将其从静态场景重建扩展到动态视频生成场景。与**4D Gaussian**（Wang et al., 2024a）的显式场景重建路线不同，该方法在潜在空间施加几何约束，保留了视频扩散模型的生成灵活性。在机器人操作策略层面，该方法与**DP3**（Ze et al., 2024）形成互补：DP3在3D点云上直接学习策略，而本方法通过生成几何一致的4D视频为策略提供视觉输入，二者可组合使用。

### 方法局限与待验证假设

尽管实验结果整体正面，以下局限需要在解读时审慎对待：

1. **推理效率**：30.0秒的推理时间和47GB显存需求限制了实时应用场景。文中未提供批量推理或模型压缩的实验，实际部署可行性需进一步验证。
2. **开环执行**：机器人策略采用开环执行模式，缺乏闭环反馈调整。Table 2的成功率可能高估了在真实扰动环境中的表现。
3. **相机外参依赖**：训练需要已知相机姿态进行点云投影，尽管推理时不再需要，但训练数据的采集成本高于无标定方法。
4. **视角数线性扩展**：多视角推断需逐对进行前向传播，延迟与视角数线性增长，限制了大规模多视角应用。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_18gC6pZVVc/figures/008_Figure_6.jpg]]
*Figure 6: Simulation Tasks for Evaluation*

## 方法谱系与知识库定位

### 1. 技术路线与基线关系

本文提出的**几何感知4D视频生成模型**（Geometry‑aware 4D Video Generation）处于视频扩散模型与多视角几何学习的交叉地带。其技术骨架直接继承自**Stable Video Diffusion (SVD)**（Blattmann et al., 2023），利用其预训练权重初始化U‑Net，并将单视角视频生成能力扩展到联合RGB‑D多视角生成。在此基础上，方法引入了一条关键的几何约束分支，其核心思想源自**DUSt3R**（Wang et al., 2024b）的跨视角点云图对齐策略——将第二视角的点云投影到参考视角坐标系，并最小化投影点云与参考点云之间的差异。

这种设计使本文方法在谱系上区别于两类已有工作：

- **纯像素级视频生成模型**（如SVD本身）：这些模型缺乏对三维场景结构的显式理解，在多视角条件下容易产生跨视角不一致的RGB帧和深度预测。本文通过引入点云图作为显式3D监督信号，弥补了这一结构缺失。
- **4D场景重建方法**（如**4D Gaussian**，Wang et al., 2024a）：这类方法通常要求完整的场景观测或多视角覆盖，难以直接处理动态的、部分可观测的机器人操作场景。本文方法则从两个RGB‑D视角的历史观测出发，直接生成未来的4D视频，更贴合机器人操作的感知条件。

在机器人操作策略层面，本文与**扩散策略（DP）**（Chi et al., 2023）和**3D扩散策略（DP3）**（Ze et al., 2024）形成对比。DP和DP3直接预测末端执行器位姿，而本文方法先生成4D视频，再通过**FoundationPose**位姿跟踪器从生成的RGB‑D序列中提取6DoF轨迹和夹爪状态。这种“生成‑提取”的两阶段范式将运动规划问题转化为视觉预测问题，其优势在于可以利用大规模视频预训练先验，但也引入了位姿估计环节的误差累积风险。

### 2. 核心机制与因果瓶颈

方法的因果杠杆在于**跨视角点云图对齐**与**多视角交叉注意力**的协同作用。训练时，模型同时优化三个损失分量：参考视角的RGB扩散损失、第二视角的RGB扩散损失，以及点云3D一致性损失（权重λ=1）。点云一致性损失通过以下方式强制几何对齐：

$$
\mathcal{L}_{\mathrm{3D-diff}}(t') = \mathbb{E}_{\epsilon_{t'}^{n},\mathbf{z}_{t'}^{n}(0),k}\left[\|\mathbf{z}_{t'}^{n}(0)-f_\theta(\mathbf{z}_{t'}^{n}(k),k,c^{n})\|^2\right] + \mathbb{E}_{\epsilon_{t'}^{m},\mathbf{z}_{t'}^{m\to n}(0),k}\left[\|\mathbf{z}_{t'}^{m\to n}(0)-f_\theta(\mathbf{z}_{t'}^{m\to n}(k),k,c^{m})\|^2\right]
$$

其中$\mathbf{z}_{t'}^{m\to n}(0)$是第二视角点云投影到参考坐标系后的干净潜在表示。这一设计使模型学习到共享的三维场景表示，而非独立建模每个视角。

多视角交叉注意力则作为信息传递的通道：在U‑Net解码器中，第二视角分支的每个解码块后插入交叉注意力层，查询来自参考视角分支的特征。消融实验提供了强有力证据：**移除多视角交叉注意力后，Task 1的跨视角mIoU从0.70骤降至0.41，深度指标δ₁‑m从0.92恶化至0.66**（Table 1, Section 4.2）。值得注意的是，该模块仅将参数量从2.38B微增至2.4B，推理时间从29.3s增至30.0s（Table 3），却带来了几何一致性和生成质量的显著跃升。

### 3. 适用边界与局限

**训练数据依赖**：方法在训练阶段需要已知的相机外参来完成跨视角点云投影（推理时无需外参），这限制了其在无标定多视角数据上的直接应用。仿真数据通过随机采样相机位姿生成（Figure 7），真实世界数据则需要双摄像头同步采集。

**推理效率**：当前模型的推理时间为30.0秒，需47GB显存和2.4B参数（Table 3），远未达到实时要求。多视角推断时需逐对进行前向传播，延迟与视角数线性增长，这限制了其在需要快速响应的操作场景中的部署。

**策略执行模式**：机器人操作采用开环执行——从生成的视频中一次性提取完整轨迹并执行，缺乏闭环反馈调整能力。这意味着模型无法应对执行过程中的意外扰动或动态环境变化。

**位姿估计瓶颈**：末端执行器轨迹的精度依赖于FoundationPose在生成RGB‑D视频上的跟踪性能。对于小物体、严重遮挡或快速运动的场景，位姿估计误差可能显著增大（Figure 13），进而影响操作成功率。

**任务泛化边界**：当前验证集中在三个仿真任务（StoreCerealBoxUnderShelf, PlaceAppleFromBowlIntoBin, PutSpatulaOnTable）和四个真实世界任务（Figure 6, Figure 8），均为桌面级、刚体为主的拾放操作。方法在移动操作、人机交互、非结构化环境中的泛化能力尚未检验。

### 4. 开放问题

1. **高效生成架构**：能否将几何一致性监督应用于更高效的生成模型（如单步扩散、一致性模型或自回归变换器），以将推理延迟从30秒降至亚秒级，同时保持跨视角几何精度？

2. **任意多视角扩展**：当前方法从两视角训练出发，能否设计一种架构（如视角条件编码或可学习的视角嵌入），使其在训练后自然泛化到任意多视角，而不增加线性计算开销？Table 4的三视图扩展实验表明这一方向有初步可行性，但机制尚不清晰。

3. **闭环规划集成**：生成的4D视频能否直接作为世界模型嵌入闭环规划或模型预测控制框架中？这需要解决生成速度与规划频率之间的匹配问题，以及生成不确定性下的鲁棒决策。

4. **几何表示升级**：点云一致性损失能否与其他几何表示（如隐式神经场、3D高斯泼溅）结合？这可能在保持生成质量的同时提升几何精度，尤其对于细粒度物体和复杂拓扑结构。

5. **跨具身泛化**：该方法在双臂操作、移动操作或不同末端执行器形态下的泛化能力如何？当前仅验证了单臂夹爪场景，扩展到更多样的机器人形态需要重新审视几何监督的普适性。

6. **真实世界训练数据效率**：当前真实世界微调需要约15k步（Section 4.3），能否通过域随机化、数据增强或元学习策略降低对真实数据的依赖，加速从仿真到真实的迁移？

## 原文 PDF

![[paperPDFs/ICLR_2026/Geometry_aware_4D_Video_Generation_for_Robot_Manipulation_dceab2ee24a9.pdf]]