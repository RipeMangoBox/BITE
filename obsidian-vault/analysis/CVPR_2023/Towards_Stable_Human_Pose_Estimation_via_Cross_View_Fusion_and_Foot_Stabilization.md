---
title: "Towards Stable Human Pose Estimation via Cross-View Fusion and Foot Stabilization"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/Towards_Stable_Human_Pose_Estimation_via_Cross_View_Fusion_and_Foot_Stabilization.pdf
project_link: null
code_link: null
aliases:
- CVFCMRKTDR
- TSHPECVFFS
tags:
- CVPR_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入跨视角融合（CVF）模块显式学习前/侧/顶三视图二维关节点作为三维中间表示以缓解视角不一致；通过多视角优化为现有多视角数据集生成精确的足部姿态和足-地接触伪标注；提出可逆运动学拓扑解码器（RKTD）根据接触状态动态调整下肢关节预测顺序，将接触信息注入姿态回归"
primary_logic: "将三维姿态分解为三个正交视图的二维表示，并利用交叉注意力进行融合，使网络获得视角一致的深层特征；多视角优化能产生更准确的足部伪标注，而基于接触状态的可逆运动学树解码可以显著提升站立时足部姿态的稳定性和精度"
claims:
- "本方法在3DPW测试集上PA-MPJPE达40.1mm，比当时最佳视频方法D&D (42.7mm) 提升2.6mm"
- "CVF模块整体使PA-MPJPE从基线48.7mm降至45.1mm，提升3.6mm"
- "RKTD相比KTD在AIST++上足部PA-MPJPE降低1.3mm (34.9→33.6)"
- "在Human3.6M和AIST++上添加脚部标注后训练，MPJPE分别降低2mm和3mm"
---

# Towards Stable Human Pose Estimation via Cross-View Fusion and Foot Stabilization

> [!tip] 核心洞察
> 将三维姿态分解为三个正交视图的二维表示，并利用交叉注意力进行融合，使网络获得视角一致的深层特征；多视角优化能产生更准确的足部伪标注，而基于接触状态的可逆运动学树解码可以显著提升站立时足部姿态的稳定性和精度

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于跨视角融合与足部稳定的鲁棒人体姿态估计 |
| 英文题名 | Towards Stable Human Pose Estimation via Cross-View Fusion and Foot Stabilization |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2023/html/Zhuo_Towards_Stable_Human_Pose_Estimation_via_Cross-View_Fusion_and_Foot_CVPR_2023_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Cross-View Fusion (CVF) method with Reversible Kinematic Topology Decoder (RKTD) |
| Dataset | 3DPW, AIST++, Human3.6M |

> [!tip] 效果简介
> - 3DPW 上，PA-MPJPE (mm) 为 40.1 (Ours-Large)，对比 42.7 (D&D)，变化 -2.6。
> - 3DPW 上，MPJPE (mm) 为 70.8 (Ours-Large)，对比 73.7 (D&D)，变化 -2.9。
> - AIST++ 上，PA-MPJPE (mm) 为 43.8 (Ours-Large)，对比 67.0 (Trajectory Optimization)，变化 -23.2。

## 概要

单目三维人体姿态估计长期受困于两个核心瓶颈：**深度模糊导致的视角不一致性**，以及**足部姿态估计不稳定**。现有方法通常从整体图像特征直接回归SMPL参数，缺乏显式的三维中间表示，导致同一人体在不同视角下的预测结果差异显著；同时，公开数据集普遍缺失足部关节点和足-地接触标注，使得模型难以捕捉站立、行走等场景下足部与地面的精细交互。

针对上述问题，本文提出了一套包含三个关键设计的解决方案：

1. **跨视角融合模块（Cross-View Fusion, CVF）**：将三维姿态显式分解为前、侧、顶三个正交视图的二维关节点预测，并通过交叉注意力机制进行多视图特征融合，为网络提供视角一致的三维中间表示。
2. **多视角足部伪标注生成**：基于SMPLify框架，利用多视角图像的投影约束与时序平滑约束，为Human3.6M和AIST++等现有多视角数据集自动生成精确的足部姿态和足-地接触伪标注，弥补训练数据的结构性缺失。
3. **可逆运动学拓扑解码器（Reversible Kinematic Topology Decoder, RKTD）**：根据预测的足-地接触状态，动态选择从左足或右足向根关节反向解码的运动学链方向，将接触信息注入姿态回归过程，显著提升站立姿态下足部估计的精度与稳定性。

在3DPW测试集上，本方法以**40.1mm的PA-MPJPE**取得当时最优结果，较此前最佳的D&D方法（Li et al., ECCV 2022）提升2.6mm；在AIST++上PA-MPJPE达43.8mm，大幅领先既有方法。消融实验证实，CVF模块整体贡献3.6mm的PA-MPJPE提升，RKTD在AIST++上使足部PA-MPJPE额外降低1.3mm，而引入足部伪标注后Human3.6M和AIST++的MPJPE分别下降2mm和3mm。本方法为单帧图像方法，却优于多个同期视频方法，验证了跨视角融合与足部稳定化策略的有效性。



从单目图像或视频中恢复三维人体姿态与形状是计算机视觉的核心任务之一，在动作捕捉、人机交互、虚拟现实等领域有广泛应用。近年来，基于参数化人体模型（如 SMPL）的回归方法取得了显著进展，从早期的单帧方法 **HMR**（Kanazawa et al., CVPR 2018）逐步演进到利用时序信息的视频方法 **VIBE**（Kocabas et al., CVPR 2020）、**MAED**（Wan et al., ICCV 2021）和 **D&D**（Li et al., ECCV 2022），在标准基准上的精度持续提升。

然而，现有方法在追求整体指标提升的过程中，普遍忽视了人体姿态估计中的两个深层瓶颈：

**瓶颈一：单目深度模糊导致的视角不一致性。** 单目图像本身缺乏显式的深度信息，网络从二维像素推断三维结构时存在固有的歧义性。这种歧义性表现为：同一姿态从不同视角观察时，估计结果会出现显著差异。主流方法通常直接从整体图像特征回归 SMPL 参数，缺乏有效的三维中间表示来显式建模多视角几何约束，导致模型对视角变化敏感，难以保证跨视角的姿态一致性。

**瓶颈二：足部姿态与足-地接触的估计不稳定。** 现有方法普遍忽略足部关节的精细估计和足-地接触状态建模。这源于两个层面的缺失：在数据层面，公开数据集（如 Human3.6M、AIST++）缺少足部关节点和足-地接触的精确标注；在方法层面，传统运动学解码器采用固定的从根到叶的关节预测顺序，无法根据接触状态动态调整下肢关节的回归策略。其后果是，即使全身姿态的整体误差较低，足部区域仍常出现悬浮、穿透地面等不自然现象，严重影响姿态的物理合理性。

上述两个瓶颈互为因果：视角不一致性加剧了足部估计的不确定性，而足部接触信息的缺失又使网络失去了一个重要的三维空间约束线索。本文正是针对这两个相互关联的挑战，提出了一套系统的解决方案。



## 核心方法与创新机理

本方法的核心创新围绕两个“因果旋钮”展开：**跨视角融合（CVF）** 缓解单目深度模糊导致的视角不一致，以及**可逆运动学拓扑解码器（RKTD）** 利用足-地接触信息提升下肢姿态稳定性。两者均依赖一个前置条件——通过多视角优化为现有数据集生成高质量的**足部姿态与接触伪标注**。

### 创新一：跨视角融合模块（CVF）

**改变的槽位**：三维中间表示。

主流方法（如 **HMR** Kanazawa et al., CVPR 2018；**SPIN** Kolotouros et al., ICCV 2019）直接从整体图像特征回归 SMPL 参数，缺乏显式的三维中间表示，导致不同视角下估计结果不一致。CVF 将三维姿态分解为**前、侧、顶三个正交视图的二维关节点**，作为三维中间表示，再通过交叉注意力（Cross-View Attention, CVA）融合为三维特征。

具体而言，CVF 包含三个分支分别预测三视图的 2D 关节点，并以 front-view 特征为查询（Q），对 backbone 输出特征（K, V）进行交叉注意力，得到侧视图和顶视图的增强特征：

$$F_{side} = F_{out}^{\prime} + \mathbf{MLP}(\mathrm{softmax}(\frac{QK^{T}}{\sqrt{d_{K}}})V)$$

这一设计使网络获得视角一致的深层特征。消融实验（Table 3）表明，CVF 整体（三视图 + CVA）相比无中间表示的基线在 3DPW 上 PA-MPJPE 从 48.7mm 降至 45.1mm，提升 3.6mm。

### 创新二：可逆运动学拓扑解码器（RKTD）

**改变的槽位**：运动学解码顺序。

传统方法（如 **HybrIK** Li et al., CVPR 2021）采用固定的运动学树解码（KTD），从根关节向叶关节顺序回归姿态。RKTD 的关键突破在于：根据预测的足-地接触状态**动态选择运动学链方向**——当左脚接触置信度高于右脚时，从左足向根关节反向解码；反之从右足开始；若双脚均未接触，则沿用标准根-叶顺序：

$$F_i = \begin{cases} \mathrm{CONCAT}(F, \{\theta_k | k \in \mathrm{ancestor}_l(i)\}) & \mathrm{if } c_l > c_r > 0,\\ \mathrm{CONCAT}(F, \{\theta_k | k \in \mathrm{ancestor}_r(i)\}) & c_r > c_l > 0,\\ \mathrm{CONCAT}(F, \{\theta_k | k \in \mathrm{ancestor}_p(i)\}) & \mathrm{otherwise}, \end{cases}$$

这一设计将接触信息注入姿态回归过程：站立时接触脚作为稳定锚点，逆向传播更准确的姿态约束。在 AIST++ 上，RKTD 相比 KTD 使足部 PA-MPJPE 降低 1.3mm（34.9→33.6），验证了接触引导的可逆解码对下肢精度的提升效果（Table 4）。

### 支撑创新：足部姿态与接触伪标注

**改变的槽位**：训练数据。

公开数据集（Human3.6M、AIST++）普遍缺少足部关节点和足-地接触标注。本方法引入基于 SMPLify 的多视角优化框架，通过最小化投影损失与平滑损失来修正足部姿态：

$$\operatorname*{argmin}_{\theta_{\mathrm{lowerlegs}},\theta_{\mathrm{feet}}} \mathcal{L}_{\mathrm{proj}}(\theta,\beta,T,j_{2D}) + \mathcal{L}_{\mathrm{smooth}}(\theta)$$

接触标注则通过计算顶点到地平面的距离并与阈值 $\delta$ 比较获得：

$$GC(v) = \begin{cases} \mathrm{True} & \mathrm{if}\ D(v, plane) < \delta,\\ \mathrm{False} & \mathrm{otherwise}, \end{cases}$$

添加这些伪标注后，Human3.6M 上 MPJPE 降低 2mm，AIST++ 上降低 3mm，为 CVF 和 RKTD 的有效训练提供了数据基础。

### 创新间的协同关系

三个创新形成因果链：伪标注提供足部接触监督 → RKTD 利用接触信息动态调整解码顺序 → CVF 提供视角一致的三维特征表示。最终在 3DPW 测试集上 PA-MPJPE 达 40.1mm，较此前最优视频方法 **D&D**（Li et al., ECCV 2022, 42.7mm）提升 2.6mm，且本方法为单帧方法，无需时序信息即可超越视频方法。



![[assets/figures/papers/paper_list_l36_Towards_Stable_Human_Pose_Estimation_via_Cross_View_Fusion_and_Foot_Stab/figures/002_Figure_2.jpg]]
*Figure 2: The top-down framework for 3D human pose and shape estimation, which consists of three parts, including the vision transformer encoder, the cross-view attention representation, and the reversible kinematic topology decoder*

该方法采用自上而下的三阶段流水线，将单目图像逐级映射为SMPL人体网格参数。整体架构由**视觉Transformer编码器**、**跨视角融合模块**与**可逆运动学拓扑解码器**串联构成（Figure 2）。

**输入与特征提取**。输入为单张RGB图像，经ViT骨干网络提取深层视觉特征。论文采用ViTPose作为默认骨干，并在消融实验中对比了ResNet50、ViT-Base与ViT-Large的缩放效应——ViT-Large在3DPW上相比ResNet50将PA-MPJPE降低4.0 mm（48.5→44.5），验证了更强视觉编码器的收益。

**跨视角融合模块**。该模块是缓解单目深度模糊与视角不一致性的核心。它包含三个并行的二维关节点预测分支，分别输出**前视图**、**侧视图**与**顶视图**的关节点坐标，作为三维姿态的显式中间表示。前视图分支直接从ViT特征解码二维关节点；侧视图与顶视图分支则通过**交叉注意力**机制，以前视图特征为查询（Q），对骨干输出特征（K, V）进行注意力聚合，从而显式地注入多视角几何约束。三视图特征最终融合为三维特征张量，送入后续解码阶段。

**足部姿态与接触伪标注**。训练流水线依赖一个离线的多视角优化工具。该工具基于SMPLify框架，在多视角图像上优化小腿与足部关节旋转参数，目标函数为投影损失与时序平滑损失的加权和（公式1-3）。优化后的网格通过顶点-地平面距离阈值化（$\delta = 0.025$m）获得逐顶点足-地接触伪标注。这些伪标注被注入Human3.6M和AIST++训练集，弥补了公开数据集足部标注缺失的瓶颈。

**可逆运动学拓扑解码器**。解码器接收融合后的三维特征与接触预测分支输出的足-地接触状态，动态选择运动学树的解码方向：若左脚接触置信度高于右脚，则沿左足→左小腿→…→骨盆的逆向链进行关节旋转回归；反之从右足开始；若双脚均未接触，则回退至标准的骨盆→足部前向解码。这一机制将接触先验直接编码进姿态回归的因果顺序中，使网络在站立场景下优先约束支撑足的姿态，从而提升足部估计的稳定性。

**多任务损失监督**。整体损失函数为四项加权和：
$$\mathcal{L} = \lambda_{2D}\mathcal{L}_{2D} + \lambda_{3D}\mathcal{L}_{3D} + \lambda_{SMPL}\mathcal{L}_{SMPL} + \lambda_{Contact}\mathcal{L}_{Contact}$$
其中$\mathcal{L}_{2D}$包含前视图重投影损失与CVF中间表示的MSE及关节点距离损失；$\mathcal{L}_{3D}$与$\mathcal{L}_{SMPL}$分别监督三维关节点与SMPL参数；$\mathcal{L}_{Contact}$为接触预测的二元交叉熵。训练在8张NVIDIA A100上完成，100个epoch，batch size 256，初始学习率$5\times10^{-5}$并在第50、70、90个epoch衰减0.3倍。



### 整体框架

本方法采用自顶向下的三阶段架构（Figure 2）：**Vision Transformer 编码器**提取图像特征，**跨视角融合（CVF）模块**构建三维中间表示以缓解视角不一致，**可逆运动学拓扑解码器（RKTD）**利用足-地接触信息动态调整下肢关节回归顺序。以下重点解析 CVF 与 RKTD 两个核心模块的设计及其关键公式。

---

### 跨视角融合模块（Cross-View Fusion, CVF）

**设计动机**：单目图像存在固有的深度模糊，导致网络在不同视角下对同一姿态的估计不一致。CVF 的核心思想是将三维姿态显式分解为前视图、侧视图和顶视图三个正交视角的二维关节点表示，再通过交叉注意力融合为视角一致的三维特征。

**模块结构**：

1. **三视图分支**：ViT 编码器输出的特征图 $F_{out}$ 分别送入前视图分支和侧/顶视图分支。前视图分支直接预测前视图二维关节点 $\hat{j}_{2D}^{front}$；侧视图和顶视图分支则通过交叉注意力块（Cross-View Attention, CVA）从 $F_{out}$ 中提取对应视角的特征。

2. **交叉注意力融合**：以侧视图为例，以前视图特征为查询（Query），对骨干网络输出特征进行交叉注意力计算：

   $$F_{side} = F_{out}^{\prime} + \mathbf{MLP}\left(\mathrm{softmax}\left(\frac{QK^{T}}{\sqrt{d_{K}}}\right)V\right)$$

   其中 $Q$ 来自前视图特征，$K, V$ 来自 $F_{out}$。顶视图特征 $F_{top}$ 采用相同机制获得。三视图特征最终融合为三维中间表示，用于后续的姿态回归。

**关键公式——CVF 损失**：为监督三视图二维关节点的学习，引入联合距离损失 $\mathcal{L}_{jd}$：

$$\mathcal{L}_{CVF} = \frac{1}{m} \sum_{i \in \omega}^{m} (j_{2D_i} - \hat{j}_{2D_i})^2 + \mathcal{L}_{jd}(j_{2D}, \hat{j}_{2D}, m)$$

其中 $\mathcal{L}_{jd}$ 约束预测关节点之间的相对距离与真值一致：

$$\mathcal{L}_{jd}(j_{2D}, \hat{j}_{2D}, m) = \frac{1}{m} \sum \left| \|j_{2D_i} - j_{2D_j}\| - \|\hat{j}_{2D_i} - \hat{j}_{2D_j}\| \right|$$

该损失使网络在缺乏绝对深度信息的情况下，仍能学习到视角一致的二维几何结构。

---

### 可逆运动学拓扑解码器（Reversible Kinematic Topology Decoder, RKTD）

**设计动机**：传统运动学树解码器（如 KTD）按固定根-叶顺序（骨盆→髋→膝→踝→足）回归关节姿态，忽略了足部与地面的接触约束。当人站立时，足部位置受地面约束最确定，从足部反向解码至根关节可以更稳定地估计下肢姿态。

**核心机制**：

1. **接触状态预测**：网络首先预测每个 SMPL 顶点的身体-场景接触状态。足-地接触条件定义为顶点到地平面距离小于阈值 $\delta$（本文取 0.025m）：

   $$GC(v) = \begin{cases} \mathrm{True} & \mathrm{if}\ D(v, plane) < \delta,\\ \mathrm{False} & \mathrm{otherwise}, \end{cases}$$

   据此获得左右足的接触置信度 $c_l$ 和 $c_r$。

2. **动态运动学链选择**：根据接触状态选择逆向运动学树方向，从接触足向根关节反向解码：

   $$F_i = \begin{cases} \mathrm{CONCAT}(F, \{\theta_k | k \in \mathrm{ancestor}_l(i)\}) & \mathrm{if } c_l > c_r > 0,\\ \mathrm{CONCAT}(F, \{\theta_k | k \in \mathrm{ancestor}_r(i)\}) & c_r > c_l > 0,\\ \mathrm{CONCAT}(F, \{\theta_k | k \in \mathrm{ancestor}_p(i)\}) & \mathrm{otherwise}, \end{cases}$$

   - 当左脚接触置信度更高时，沿左足→左踝→左膝→髋→骨盆的逆向链解码；
   - 当右脚接触置信度更高时，沿右足→右踝→右膝→髋→骨盆解码；
   - 当双足均未接触（如跳跃）时，回退至常规骨盆→足的根-叶顺序（$\mathrm{ancestor}_p$）。

**因果机制**：站立时足部与地面的接触提供了强几何约束，从确定性更高的足部位置出发逐级推断髋关节姿态，比从模糊的骨盆位置向下推断足部姿态更稳定。消融实验证实，RKTD 相比固定顺序的 KTD 在 AIST++ 上足部 PA-MPJPE 降低 1.3mm（34.9→33.6）。

---

### 足部姿态与接触伪标注生成

为弥补公开数据集（Human3.6M、AIST++）缺少足部关节点和足-地接触标注的缺陷，本文引入基于多视角优化的标注工具。

**优化目标**：在 SMPLify 框架基础上，仅优化小腿和足部的姿态参数 $\theta_{\mathrm{lowerlegs}}, \theta_{\mathrm{feet}}$，保持其他参数固定：

$$\operatorname*{argmin}_{\theta_{\mathrm{lowerlegs}},\theta_{\mathrm{feet}}} \mathcal{L}_{\mathrm{proj}}(\theta,\beta,T,j_{2D}) + \mathcal{L}_{\mathrm{smooth}}(\theta)$$

其中**投影损失**惩罚重投影偏差：

$$\mathcal{L}_{\mathrm{proj}}(\theta,\beta,T,j_{D}) = \frac{1}{n} \sum_{i \in \Omega}^{n} (\pi(j_{3D_i}, T) - j_{2D_i})^2$$

**时序平滑损失**约束相邻帧姿态参数平滑变化：

$$\mathcal{L}_{\mathrm{smooth}}(\theta) = \theta_{[1:t-1]} - \frac{1}{3} (\theta_{[0:t-2]} + \theta_{[1:t-1]} + \theta_{[2:t]})$$

优化完成后，根据顶点-地平面距离阈值 $\delta = 0.025\mathrm{m}$ 为每个顶点赋予接触标签。该伪标注使模型在 Human3.6M 和 AIST++ 上分别额外降低 MPJPE 2mm 和 3mm。



## 实验与关键发现

### 主要结果

本方法在三个主流基准上进行了系统评估，核心指标为 PA-MPJPE 和 MPJPE。在最具挑战性的室外数据集 3DPW 上，基于 ViT-Large 的模型取得了 **40.1 mm** 的 PA-MPJPE，相比此前最优的视频方法 **D&D**（Li et al., ECCV 2022）的 42.7 mm 降低了 2.6 mm，MPJPE 也从 73.7 mm 降至 70.8 mm（Table 1）。值得注意的是，本方法为单帧图像方法，却优于多个同期视频方法（如 **VIBE**、**MAED** 等），说明跨视角融合和足部稳定机制有效地弥补了时序信息的缺失。

![[assets/figures/papers/paper_list_l36_Towards_Stable_Human_Pose_Estimation_via_Cross_View_Fusion_and_Foot_Stab/figures/008_Table_1.jpg]]
*Table 1: Performance comparison between our method and state-of-the-art methods on 3DPW, Human3.6M and AIST++*

在舞蹈数据集 AIST++ 上，本方法的优势更为突出：PA-MPJPE 达 43.8 mm，比 Trajectory Optimization 的 67.0 mm 降低了 23.2 mm。这一巨大提升主要归因于足部姿态伪标注和可逆运动学拓扑解码器（RKTD）对站立姿态下足部稳定性的显著改善——AIST++ 包含大量足部着地的舞蹈动作，恰好是 RKTD 发挥作用的典型场景。

在 Human3.6M 上，本方法 PA-MPJPE 为 36.6 mm，略高于 D&D 的 35.5 mm（+1.1 mm）。这一差距可能源于 Human3.6M 为室内受控环境，视角变化较小，CVF 模块的跨视角一致性优势未能完全体现。然而，在加入足部姿态和接触伪标注后，MPJPE 额外降低了 2 mm，说明足部信息的引入对整体精度仍有显著贡献。

### 消融实验

消融实验从骨干网络、跨视角融合模块和可逆运动学解码器三个维度逐层验证各设计的有效性。

**骨干网络选择**（Table 2）：以 3DPW 为测试平台，ResNet50 基线 PA-MPJPE 为 48.5 mm。替换为 ViT-Base 后降至 44.5 mm（-4.0 mm），ViT-Large 进一步提升至 40.1 mm。ViT 的全局自注意力机制为后续的多视角特征解耦提供了更强的表示基础。

![[assets/figures/papers/paper_list_l36_Towards_Stable_Human_Pose_Estimation_via_Cross_View_Fusion_and_Foot_Stab/figures/009_Table_2.jpg]]
*Table 2: Ablation study of the effectiveness on the backbone*

**CVF 模块消融**（Table 3）：基线（无中间表示）PA-MPJPE 为 48.7 mm。单独添加前视图分支降至 47.1 mm（-1.6 mm），引入三视图表示（前/侧/顶）后降至 46.5 mm（-2.2 mm），再加入交叉注意力（CVA）融合后进一步降至 45.1 mm，整体提升 3.6 mm。这表明三视图分解和交叉注意力融合是两个互补的关键设计：三视图提供了结构化的三维中间表示，CVA 则以前视图特征为查询，从骨干特征中提取侧视图和顶视图的互补信息。

![[assets/figures/papers/paper_list_l36_Towards_Stable_Human_Pose_Estimation_via_Cross_View_Fusion_and_Foot_Stab/figures/010_Table_3.jpg]]
*Table 3: The effectiveness of each part of Our Cross-View Fusion module. ‘Three views’ indicates our proposed front, side, and top view representation without the cross-view fusion. ‘CVA’ indicates our Cross-View Attention blocks as shown in Figure 2. Table 4. Ablation study of the effectiveness on RKTD*

**RKTD 消融**（Table 4）：在 AIST++ 上，独立回归（Independent）的足部 PA-MPJPE 为 39.5 mm，固定运动学树解码（KTD）降至 34.9 mm，RKTD 进一步降至 33.6 mm（相比 KTD 降低 1.3 mm）。RKTD 的核心机制是根据预测的足-地接触状态动态选择运动学链方向：当左脚接触概率更高时，从左足向根关节逆向解码；反之从右足开始。这一设计将接触信息直接注入关节旋转的回归过程，使得站立时支撑足的姿态估计更加稳定。

**伪标注有效性**：在 Human3.6M 和 AIST++ 上，使用多视角优化生成的足部姿态和接触伪标注进行训练后，MPJPE 分别降低 2 mm 和 3 mm（Introduction, Section 4.4）。这验证了伪标注的质量足以提供有效的监督信号。

### 定性分析

Figure 5 展示了 AIST++ 上的三视图定性结果：前、侧、顶三个视图的二维关节点预测与真值高度吻合，对应的三维网格在三个正交视角下均能准确还原人体姿态。Figure 6 对比了本方法与 MAED 在 3DPW 上的三视图结果，本方法在侧视图和顶视图下的姿态一致性明显优于 MAED，尤其在四肢末端的位置精度上表现更优，直接体现了 CVF 模块缓解视角不一致性的效果。

### 局限与讨论

尽管整体性能优异，仍存在若干值得关注的边界情况。首先，CVF 模块的训练依赖三视图二维关节点监督，这限制了其在纯单目无标注数据上的扩展性——如何在没有多视角标注的真实场景中训练 CVF 是一个开放问题。其次，RKTD 当前仅应用于下肢关节链，其可逆运动学树策略是否可推广到上肢或全身关节链尚未验证。此外，足部伪标注的优化过程依赖多视角图像，对于真实室外单目视频，接触信息的获取仍缺乏有效方案。最后，本方法在极端姿态（如躺下、倒立）下的泛化能力未在实验中覆盖，这些场景下足-地接触的定义和运动学树方向的选择可能需要重新设计。

### 补充图表

![[assets/figures/papers/paper_list_l36_Towards_Stable_Human_Pose_Estimation_via_Cross_View_Fusion_and_Foot_Stab/figures/001_Figure_1.jpg]]
*Figure 1: Two main challenges towards stable human pose estimation*



## 定位与知识库关联

### 1. 方法在领域中的位置

本工作处于单目三维人体姿态与形状估计的主流演进路径上，其核心设计思想可追溯到两个关键脉络：**基于SMPL参数回归的端到端方法**，以及**利用运动学结构先验的解码策略**。

**SMPL回归基线**：方法继承了从单张图像直接回归SMPL参数的基本范式。早期工作如 **HMR**（Kanazawa et al., CVPR 2018）建立了“图像→SMPL参数”的端到端框架，**SPIN**（Kolotouros et al., ICCV 2019）进一步引入回归-优化循环以提升精度。本方法在损失函数层面延续了这一传统，采用2D重投影、3D关节点和SMPL参数损失的加权组合。与这些纯图像方法相比，本方法的核心差异在于引入了三视图二维中间表示作为三维特征构建的桥梁，而非直接从整体图像特征回归SMPL参数。

**视频时序方法的参照**：尽管本方法本质上是单帧方法（不使用时序信息），但其性能对比对象包含了同期最强的视频方法。**VIBE**（Kocabas et al., CVPR 2020）利用AMASS运动先验约束时序姿态，**MAED**（Wan et al., ICCV 2021）通过时空注意力建模帧间依赖，**D&D**（Li et al., ECCV 2022）则处理动态相机场景。本方法在3DPW上以40.1mm PA-MPJPE超越D&D的42.7mm，表明精心设计的三维中间表示可以在不依赖时序信息的条件下，获得比视频方法更强的视角一致性。

**运动学解码的改进**：在姿态解码策略上，本方法与 **HybrIK**（Li et al., CVPR 2021）形成对比。HybrIK采用混合解析-神经网络方法进行逆运动学求解，而本方法提出可逆运动学拓扑解码器（RKTD），其关键创新在于根据足-地接触状态动态选择运动学链方向——当检测到左脚触地时从左足向根关节反向解码，右脚触地时从右足反向解码，双足离地时则回退到传统的根→叶方向。这本质上是在运动学树中引入了条件分支，使接触约束能够直接作用于下肢关节的回归顺序。

### 2. 适用边界与局限

**适用场景**：方法在站立、行走、舞蹈等足部与地面有明显交互的场景下优势显著。AIST++上PA-MPJPE达43.8mm，远超Trajectory Optimization的67.0mm，印证了足部稳定化策略在舞蹈动作估计中的有效性。

**已知局限**：
- **Human3.6M上的PA-MPJPE未达最优**：在Human3.6M上PA-MPJPE为36.6mm，略高于D&D的35.5mm（+1.1mm）。这表明在常规室内受控场景下，跨视角融合带来的收益不足以抵消视频方法利用时序平滑获得的优势。但添加脚部伪标注后MPJPE降低2mm，说明足部信息的补充可以部分弥补这一差距。
- **对多视角监督的依赖**：跨视角融合模块需要前、侧、顶三视图的二维关节点作为监督信号。在仅有单目标注的训练数据下，该模块的有效训练方式尚不明确。这是方法向更广泛单目数据扩展的关键瓶颈。
- **足部标注的获取成本**：伪标注生成依赖多视角优化框架（SMPLify-based），需要多视角图像和二维关键点。对于真实室外单目视频（如3DPW的部分场景），该方法无法直接获取接触信息，限制了RKTD在这些场景下的完整效用。

### 3. 开放问题

1. **跨视角融合的单目训练**：当前CVF模块依赖多视角2D关节点监督。在纯单目训练设置下，如何通过自监督或弱监督方式学习三视图表示，是降低数据依赖的关键方向。

2. **可逆运动学树的扩展性**：RKTD目前仅应用于下肢链。理论上，接触信息同样可以指导上肢链的解码顺序（如手-物接触），但需要相应的接触标注和运动学树重构。该策略向全身关节链的推广值得探索。

3. **极端姿态的泛化**：方法在站立和舞蹈姿态下验证充分，但在躺下、倒立、翻滚等足部接触模式剧烈变化的姿态下，接触预测的可靠性和RKTD的逆向解码策略是否仍然有效，尚缺乏实验证据。

4. **接触预测的精度瓶颈**：RKTD的性能依赖于接触预测分支的准确性。当前接触标注通过顶点-平面距离阈值（δ=0.025m）生成，这一简化假设在非平坦地面或复杂地形下可能失效。如何提升接触预测的鲁棒性，是进一步改善足部姿态估计的前提。



## 原文 PDF

![[paperPDFs/CVPR_2023/Towards_Stable_Human_Pose_Estimation_via_Cross_View_Fusion_and_Foot_Stabilization.pdf]]
