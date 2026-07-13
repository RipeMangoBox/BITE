---
title: "Forecasting from LiDAR via Future Object Detection"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/Forecasting_from_LiDAR_via_Future_Object_Detection.pdf
project_link: null
code_link: https://github.com/neeharperi/FutureDet
aliases:
- FFLFOD
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将预测任务重构为未来物体检测：通过检测器在多个未来时刻生成热图，再将这些未来检测回溯到当前帧，利用多对一匹配机制自然捕捉多模态未来。"
primary_logic: "通过从历史LiDAR扫描中训练物体检测器来检测未来时刻的物体位置，并回溯轨迹实现端到端多未来预测，同时设计新的预测mAP指标将检测与预测性能联合评估，解决了传统指标的弊端。"
claims:
- "恒定位置基线在ADE/FDE指标上达到最先进，但在移动物体的AP_f上为0，表明传统指标可被欺骗。"
- "FutureDet在非线形移动物体上的预测APf相比FaF*提升4%（K=5），展现了多未来预测的优势。"
- "FutureDet在行人预测的mAPf达到26.9，超过FaF* 0.5点，并显着优于Trajectron++。"
- "nuScenes (car) 上 mAP_f = FutureDet (outperforms all baselines)"
---

# Forecasting from LiDAR via Future Object Detection

> [!tip] 核心洞察
> 通过从历史LiDAR扫描中训练物体检测器来检测未来时刻的物体位置，并回溯轨迹实现端到端多未来预测，同时设计新的预测mAP指标将检测与预测性能联合评估，解决了传统指标的弊端。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于激光雷达的未来物体检测进行预测 |
| 英文题名 | Forecasting from LiDAR via Future Object Detection |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2203.16297) · [GitHub](https://github.com/neeharperi/FutureDet) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | FutureDet |
| Dataset | nuScenes (car), nuScenes (pedestrian), nuScenes (car, non-linear subset) |

> [!tip] 效果简介
> - nuScenes (car) 上，mAP_f 为 FutureDet (outperforms all baselines)，对比 FaF* 31.5 mAP_f，变化 outperforms, e.g., +4% AP_f non-linear at K=5。
> - nuScenes (pedestrian) 上，mAP_f 为 26.9，对比 FaF* 26.4，变化 +0.5。
> - nuScenes (car, non-linear subset) 上，AP_f non-lin 为 FutureDet，对比 FaF* 7.5，变化 +4% improvement。

## 概要

本文针对从原始LiDAR数据直接进行端到端运动预测这一任务，揭示并解决了一个关键瓶颈：**现有端到端预测方法无法推理多模态未来轨迹，且传统评估指标（如ADE/FDE）容易被简单基线欺骗**。具体而言，一个仅预测所有物体保持静止的“恒定位置”基线，在ADE/FDE指标上可达最先进水平，但在移动物体上的预测平均精度（AP_f）为0（Table 1），暴露了传统指标在联合评估检测与预测性能时的根本缺陷。

针对上述问题，本文提出**FutureDet**，其核心洞察在于**将预测任务重构为未来物体检测**：通过检测器在多个未来时刻生成热图，再将未来检测回溯到当前帧，利用多对一匹配机制自然捕捉多模态未来轨迹。该方法无需物体轨迹或高精地图输入，直接从累积的历史LiDAR扫描中端到端地联合完成当前检测与多未来预测。

在方法定位上，FutureDet区别于两类主流范式：一是以**FaF***（Luo et al., CVPR 2018）为代表的前向预测方法（从当前检测出发预测未来位置），二是以**Trajectron++**（Salzmann et al., ECCV 2020）为代表的分阶段轨迹预测模型（依赖完美轨迹输入）。FutureDet通过“先检测未来，再回溯匹配”的范式转换，在nuScenes数据集上的车辆和行人联合检测与预测任务中均取得最优性能——在车辆非线性运动子集上，FutureDet的AP_f相比FaF*提升4%（K=5），行人预测的mAP_f达到26.9，超过FaF* 0.5个点，并显著优于Trajectron++（Table 2, Table 3）。

同时，本文贡献了新的**预测mAP指标**，将检测与预测性能联合评估，按静态、线性运动、非线性运动三个子类取平均，有效防止了指标被忽略移动物体的简单模型所欺骗。这一指标设计为端到端预测任务的公平比较奠定了基础。



自动驾驶系统的安全运行依赖于对周围场景未来演变的准确预测。传统方法将这一任务拆解为检测、跟踪与预测三个独立阶段，形成级联流水线。然而，这种分阶段范式存在一个根本性缺陷：每个子模块都错误地假设其输入是完美的，导致误差在流水线中逐级累积放大（Figure 1a）。例如，检测器的漏检或定位偏差会直接污染跟踪结果，进而使基于跟踪轨迹的预测模型产生严重偏离。

为克服这一问题，近年来的研究开始探索端到端的预测范式——直接从原始LiDAR传感器数据出发，绕过显式的跟踪步骤，将检测与预测统一在一个可学习框架中（Figure 1b）。代表性工作包括**FaF**（Luo et al., CVPR 2018），它在当前帧检测物体的同时，通过预测速度场来前向推演未来位置。然而，这类端到端方法仍然面临一个核心瓶颈：**它们通常只能输出单一确定性的未来轨迹，无法推理真实场景中固有的多模态未来分布**。一辆车在路口可能直行、转弯或停车，而现有端到端模型缺乏有效机制来表征这种不确定性。

与此同时，传统预测任务的评估指标——平均位移误差（ADE）和终点位移误差（FDE）——本身存在严重缺陷。本文揭示了一个令人警醒的现象：一个极其简单的**恒定位置基线**（仅预测所有物体保持静止）在ADE/FDE指标上竟然能达到甚至超越现有最先进方法的性能（Table 1）。原因在于，ADE/FDE仅在匹配成功的子集上计算误差，不惩罚误报，且真实场景中超过60%的车辆处于静止状态。这意味着，一个忽略所有移动物体的“懒惰”模型可以通过对静止物体的高置信度预测来“作弊”，在传统指标上获得虚高分数。这一发现直接暴露了现有评估体系的脆弱性。

上述双重困境——**端到端方法缺乏多未来推理能力**与**传统指标无法公平评估联合检测与预测性能**——构成了本文的核心动机。为此，本文提出了两个关键创新方向：（1）重构预测范式，使模型能够自然地输出多模态未来；（2）设计新的评估指标，将检测质量与预测质量联合考核，从根本上杜绝简单基线的“作弊”空间。



## 核心方法与创新机理

FutureDet 的核心创新在于将预测任务**重构为未来物体检测**，并配套设计了**防作弊的联合评估指标**，从而系统性地解决了端到端预测中的两个瓶颈问题。

### 瓶颈诊断：传统指标的欺骗性

现有端到端预测方法普遍采用 ADE/FDE 作为评估指标，但该指标存在根本性缺陷——它仅评估匹配子集的平均位移误差，不惩罚误报。这一漏洞使得一个简单的**恒定位置模型**（仅预测物体静止不动）能够在 ADE/FDE 上达到最先进水平，而实际上该模型对移动物体的预测完全失败（AP_f 为 0，Table 1）。这表明 ADE/FDE 无法公平评估联合检测与预测的性能，容易被简单基线欺骗。

### 创新一：预测范式从“前向外推”到“未来检测+回溯”

传统端到端方法（如 **FaF**，Luo et al., CVPR 2018）的范式是：在当前帧检测物体，然后前向预测其未来位置。这种方式本质上是确定性的单条轨迹外推，难以建模多模态未来。

FutureDet 将范式彻底翻转：
- **在未来帧检测物体**：网络在多个未来时刻（t+1 到 t+T）分别生成检测热图，直接预测物体在未来时刻的位置。
- **回溯到当前帧建立轨迹**：将未来检测“回溯”（backcast）到当前帧，与当前帧检测进行匹配，从而自然形成轨迹。
- **多对一匹配实现多模态**：多个未来检测可以匹配到同一个当前检测，这种多对一匹配机制**天然地表示了多模态未来分布**，无需额外的生成模型或显式多样性约束。

这一范式转换的核心洞察在于：检测器本身已经学会了预测热图来表示可能的目标位置，将这些热图用于未来时刻，就相当于对每个物体生成了多个可能的未来位置假设。

### 创新二：防作弊的预测 mAP 指标

为解决 ADE/FDE 的漏洞，FutureDet 提出了**预测平均精度（forecasting mAP，mAP_f）**：

$$mAP_f = \frac{1}{3} ( AP_f^{\mathrm{stat.}} + AP_f^{\mathrm{lin.}} + AP_f^{\mathrm{non.lin.}} )$$

该指标的设计包含三个关键机制：
1. **联合评估检测与预测**：一个预测被视为真正例，必须同时在当前帧和未来帧都与真值成功匹配（当前帧匹配阈值为 {0.5, 1, 2, 4}m 中心距离均值，未来帧为 {1, 2, 4, 8}m）。这强制模型必须同时做好检测和预测，无法通过牺牲检测质量来提升预测分数。
2. **子类平均防止数据偏差**：nuScenes 中超过 60% 的车辆处于静止状态，若直接计算整体 AP，模型可仅靠预测静止物体获得高分。通过将静态、线性运动、非线性运动三个子类的 AP_f 取平均，确保模型必须在移动物体上也表现良好才能获得高分。
3. **不可欺骗性**：恒定位置基线在移动物体子类上的 AP_f 为 0（Table 1），无法通过该指标作弊，而真正具有预测能力的模型（如 FaF* 在非线性运动上获得 7.5 AP_f）则能获得合理的分数。

### 创新三：轻量级未来特征变换

FutureDet 的架构基于 CenterPoint 检测器，但 CenterPoint 为所有类别共享一组特征，不适合长期预测任务。FutureDet 引入了一个**浅层特征变换网络**，将当前帧特征转换为未来帧特征（Figure 6），使模型能够学习时间偏移的表示，而无需大幅增加计算开销。这一设计在保持检测性能的同时，赋予模型预测未来物体位置的能力。

### 创新边界：未解决的问题

需要指出，FutureDet 未显式强制生成多样化轨迹，部分多未来预测会聚集在一起（Figure 5），且原始输出包含大量误报需要后处理（Figure 4）。如何鼓励真正的多模态多样性、以及如何在下游任务中有效利用这些带噪声的预测，仍是待解决的开放问题。



FutureDet 将端到端预测重新定义为**未来物体检测**任务。其核心思想是：给定一段累积的历史 LiDAR 扫描序列，训练一个检测器同时在当前时刻 $t$ 和未来时刻 $t+T$ 检测物体，然后将未来检测结果**回溯**到当前帧，通过多对一匹配自然地捕获多模态未来轨迹。

### 输入-输出流

- **输入**：一段累积的原始 LiDAR 点云序列，覆盖过去若干时间步。
- **输出**：当前帧的物体检测结果，以及每个当前检测对应的 $K$ 条未来轨迹预测（通过 $K$ 个未来检测回溯得到）。

### Pipeline 模块

1. **时空特征编码器**  
   使用 VoxelNet 或 PointPillars 等标准骨干网络对累积点云序列进行编码，提取鸟瞰图特征。该模块将时序点云压缩为统一的 BEV 特征表示。

2. **未来特征变换网络**  
   一个浅层网络，将当前时刻的特征变换为未来时刻的特征。其设计动机在于：CenterPoint 原本为所有类别共享一组特征，但预测任务需要面向未来的表征，因此引入轻量变换来适应长期预测需求。

3. **多时刻检测头**  
   在共享特征或变换后的未来特征上，分别设置当前时刻和未来时刻的检测头。每个检测头输出物体热图和边界框参数，从而在多个未来时间步上独立检测物体位置。

4. **回溯匹配模块**  
   将未来时刻的检测结果沿时间反向投射到当前帧，与当前帧的物体检测进行匹配。由于一个当前检测可以匹配多个未来检测，该机制自然地实现了**多未来解释**——每个匹配的未来检测代表一条可能的轨迹，无需显式生成模型。

### 与基线范式的关键差异

- **传统流水线**：检测→跟踪→预测分阶段进行，各模块假设上游输入完美，导致误差累积。
- **端到端前向预测**：从当前检测出发，向前预测未来位置，通常只输出单条确定性轨迹。
- **FutureDet**：在**未来帧**检测物体，再回溯到当前帧建立轨迹。这一“反向”范式使得多对一匹配成为可能，从而以简洁的方式表示多模态未来分布。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2203_16297/figures/001_Figure_1.jpg]]
*Figure 1: (a) Current stage-wise methods independently address the problems of detection, tracking, and forecasting, allowing for compounding errors in the full pipeline. Each sub-module incorrectly assumes that its input will be perfect, leading to further integration errors. In contrast to current forecasting methods that use object tracks as input, end-to-end forecasting directly from LiDAR sensory data (b) streamlines forecasting pipelines. To this end, we propose FutureDet (c), an end-to-end model capable of forecasting multiple-future trajectories directly from LiDAR via future object detection. We show that our end-to-end pipeline improves upon state-of-the-art three-stage and end-to-end metho...*



### 问题形式化

FutureDet 将联合物体检测与预测定义为：给定当前 LiDAR 扫描 $S_{t_{obs}}$，估计一组物体位置（参数化为 3D 立方体）及其在未来扫描 $S_{t_{obs}+1}, \dots, S_{t_T}$ 中的轨迹延续。对于智能体 $i$，其历史轨迹观测为：

$$X_i = \{ (x_i^t, y_i^t) \in \mathbb{R}^2, t = 1, \dots, t_{obs} \}$$

未来轨迹真值为：

$$Y_i = \{ (x_i^t, y_i^t) \in \mathbb{R}^2, t = t_{obs}+1, \dots, t_T \}$$

### 预测平均精度指标（mAP_f）

为克服传统 ADE/FDE 指标易被简单基线欺骗的缺陷，FutureDet 提出联合评估检测与预测性能的 mAP_f。一个预测被视为真正例需同时满足两个条件：在当前帧 $t_{obs}$ 和未来最终帧 $t_{obs} + T$ 均存在正匹配，否则计为误报。当前帧匹配基于中心距离，在阈值 $\{0.5, 1, 2, 4\}$ m 上取平均；未来帧匹配在阈值 $\{1, 2, 4, 8\}$ m 上取平均。

由于 nuScenes 数据中超过 60% 的车辆处于静止状态，数据严重不平衡，指标进一步按运动类型分解为三个子类，取平均值作为最终指标：

$$\text{mAP}_f = \frac{1}{3} ( AP_f^{\mathrm{stat.}} + AP_f^{\mathrm{lin.}} + AP_f^{\mathrm{non.lin.}} )$$

其中 $AP_f^{\mathrm{stat.}}$、$AP_f^{\mathrm{lin.}}$、$AP_f^{\mathrm{non.lin.}}$ 分别对应静止、线性运动和非线性运动物体的预测平均精度。这种子类平均设计确保模型不能仅通过高置信度预测静止物体来提升指标——恒定位置基线在移动物体上的 $AP_f$ 为 0（Table 1），验证了指标的有效性。

### 核心模块

FutureDet 由四个关键模块构成：

**时空特征编码器**：累积历史 LiDAR 扫描序列，使用 VoxelNet 或 PointPillars 骨干网络提取 BEV 特征。该模块将原始点云序列编码为统一的空间特征表示，为后续检测头提供共享特征基础。

**未来特征变换网络**：由于 CenterPoint 对所有类别共享一组特征，难以有效建模长期预测，FutureDet 学习一个浅层网络将当前帧特征变换为未来帧特征（Figure 6）。该模块是连接当前感知与未来预测的关键桥梁，使模型能基于当前证据推断未来特征表示。

**多时刻检测头**：在共享特征基础上，分别预测当前时刻 $t$ 和未来时刻 $t+T$ 的物体热图和边界框。检测头复用 CenterPoint 架构，但扩展为多时刻输出，使网络在训练时同时学习当前检测和未来检测任务。

**回溯匹配模块**：将未来时刻的检测结果回溯（backcast）到当前帧，与当前帧检测进行匹配。由于一个当前检测可对应多个未来检测，这种多对一匹配自然实现了多模态未来轨迹的表示——每个未来检测代表一种可能的未来状态，无需显式生成模型。



## 实验与关键发现

### 核心实验设计

FutureDet 在 nuScenes 数据集上进行联合检测与预测评估，预测时域设定为 3 秒（对应 nuScenes 的 6 个未来时间步）。实验采用提出的预测平均精度（mAP$_f$）作为主指标，该指标定义为静态、线性运动和非线性运动三个子类 AP$_f$ 的平均值：

$$\frac{1}{3} ( AP_f^{\mathrm{stat.}} + AP_f^{\mathrm{lin.}} + AP_f^{\mathrm{non.lin.}} )$$

这一设计直接回应了 nuScenes 数据中超过 60% 车辆处于静止状态的严重类别不平衡问题——子类平均策略确保模型不能仅通过准确预测静止物体来"刷高"指标。此外，实验采用 Top-K 评估（K=1 和 K=5），允许模型输出多个未来预测，并通过多对一匹配机制自然捕捉多模态未来。

基线设置涵盖三个层次：**恒定位置模型**（Constant Position）仅预测物体保持静止，作为揭露传统指标缺陷的简单基线；**检测+匀速外推**（Detection + Constant Velocity）使用 CenterPoint 检测器的速度估计进行匀速外推，作为强基线；**FaF\***（Luo et al., CVPR 2018 的重新实现）代表端到端预测方法，从当前检测出发前向预测速度。此外，还与 **Trajectron++**（Salzmann et al., ECCV 2020）、**PnPNet**（Liang et al., CVPR 2020）和 **SPF2**（Weng et al., CoRL 2020）等代表性方法进行了比较。

### 指标欺骗性分析

Table 1 的指标分解分析是本文最具洞察力的实验发现之一。恒定位置基线在传统 ADE/FDE 指标上达到了最先进水平，但在移动物体的 AP$_f$ 上为 0——这一矛盾揭示了传统指标的致命缺陷：ADE/FDE 仅评估匹配上的轨迹子集，不惩罚误报，使得一个仅输出"物体原地不动"的模型可以通过高置信度的静止物体预测获得优异分数。相比之下，FaF\* 在移动物体上取得了 7.5 的 AP$_{\text{non-lin}}$，但在 ADE/FDE 上反而不如恒定位置基线。这一发现构成了本文提出预测 mAP 的核心动机，并解释了为什么恒定速度基线在文献中长期被忽视——传统指标无法区分真正的预测能力和简单的启发式策略。

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2203_16297/figures/004_Table_1.jpg]]
*Table 1: Metric Breakdown Analysis: We compare our simple constant position model to state-of-the-art prediction models, highlighting differences among various proposed metrics. ADE/FDE based metrics measured at different recall rates favor our trivial constant position baseline over state-of-the-art methods [33, 37, 43]. Only our proposed forecasting mAP ( m A P _ { f } ) favors state-of-the-art models over the constant position baseline. We report numbers for PnPNet [33] and SPF2 [49] from their respective papers. Note: Lower ADE/FDE is better and higher A P _ { f } is better. Table 2. Joint car detection and forecasting evaluation on nuScenes. We adopt top-K evaluation for forecasting and evaluat...*

### 车辆预测主结果

在车辆联合检测与预测任务上（Table 2），FutureDet 在所有基线中表现最优。在非线性运动子类上，FutureDet 在 K=5 时相比 FaF\* 提升 4% AP$_f$，这直接归因于多未来预测机制——模型可以在多个可能位置"下注"，而非被迫输出单条确定性轨迹。从 K=1 到 K=5 的性能提升（尽管幅度不大）验证了多对一匹配捕捉多模态分布的有效性，但提升幅度有限也暗示了模型生成多样化轨迹的能力尚待增强。

与 Trajectron++ 的对比尤其值得注意：Trajectron++ 在非线性运动子类上仅取得 2.8 AP$_{\text{non-lin}}$，而 FutureDet 显著优于这一结果。考虑到 Trajectron++ 是一个基于完美轨迹输入的自回归预测模型，这一对比突显了端到端方法在避免级联误差方面的优势——当上游检测模块的输出并非完美时，分阶段流水线中的误差累积会严重损害最终预测质量。

### 行人预测结果

行人预测任务（Table 3）揭示了 FutureDet 的优势与局限。FutureDet 在行人预测上达到 26.9 mAP$_f$，超过 FaF\* 0.5 点，并显著优于 Trajectron++（后者被 FaF\* 和匀速基线分别超越 14.4% 和 16.6% mAP$_f$）。这一结果进一步强化了端到端方法的优势，同时也表明行人预测的绝对性能远低于车辆预测——行人运动更动态、更不可预测，且常以群体形式出现，使得个体运动建模更加困难。

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2203_16297/figures/008_Table_3.jpg]]
*Table 3: Joint pedestrian detection and forecasting evaluation on nuScenes. We adopt top-K evaluation for forecasting and evaluate under two settings of K = 1 and K = 5 (for forecasting only). We further breakdown the performance of each model by examining the detection $\mathbf { A P } \left$( A $P _ { d e t . } \right$) and forecasting $\mathbf { A P } \left$( A $P _ { f } \right$) on static, linear, and non-linearly moving sub-categories. Note that since pedestrians have smaller displacement over a 3 second forecasting horizon, we tighten the match thresholds as described above. FutureDet performs the best, improving over FaF* by 0.5 mAPf . As with car forecasting, $\mathrm { F a F ^ { * } }$ and the const...

定性可视化（Figure 5）印证了这一挑战：FutureDet 对行人的多未来预测通常都呈线性且彼此相似，缺乏真正的多模态多样性。在人群场景中，模型难以准确检测和预测个体行人运动，这是端到端方法从原始传感器数据中分离群体行为的固有限制。

### 消融实验

**骨干网络选择**：使用 PointPillars 替代 CenterPoint 作为骨干网络导致各指标大幅下降（Table 3），表明强大的检测骨干对预测性能至关重要。这一发现暗示，端到端预测模型的性能上限在很大程度上受制于底层检测器的质量——更好的当前帧检测能力直接转化为更好的未来预测能力。

**地图信息融合**：添加道路掩码作为输入通道对行人预测性能几乎无影响（Table 3, FutureDet+Map vs FutureDet），表明模型可能已经从 LiDAR 数据中隐式学习了空间上下文信息，或者当前的地图融合方式不足以提供额外有效信息。如何最佳地将高清地图信息融入端到端 LiDAR 预测模型仍是一个开放问题。

**数据增强**：使用轨迹级复制粘贴数据增强（Trajectory Sampler）缓解了轨迹长尾分布问题，提升了非线性运动物体的预测性能。这一策略通过在训练时复制稀有运动模式的轨迹来平衡数据分布，是对 nuScenes 数据中静止物体占主导这一偏置的直接应对。

### 失败模式与局限性

FutureDet 的原始输出包含大量误报检测与预测（Figure 4），需要后处理才能用于下游任务。这一现象源于端到端检测器天然的高召回率倾向——在没有显式负样本抑制机制的情况下，模型倾向于在不确定区域输出低置信度预测。此外，模型未显式强制生成多样化轨迹，导致部分多未来预测聚集在一起，缺乏真正的多模态覆盖。在行人预测中，多个未来预测通常都呈线性且相似，表明模型倾向于"安全"的匀速假设，而非探索可能的转向或变速行为。

### 关键图表指引

- **Table 1**：指标分解分析，揭示 ADE/FDE 可被恒定位置基线欺骗，而 mAP$_f$ 能有效区分方法优劣。
- **Table 2**：车辆联合检测与预测主结果，FutureDet 在非线性运动子类上相比 FaF\* 提升 4% AP$_f$（K=5）。
- **Table 3**：行人预测评估，FutureDet 达到 26.9 mAP$_f$，骨干网络选择和地图融合的消融结果。
- **Figure 4**：展示原始输出的误检问题，强调后处理的必要性。
- **Figure 5**：行人预测定性结果，揭示多未来预测缺乏多样性和人群场景下的困难。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2203_16297/figures/003_Table.jpg]]



## 定位与知识库关联

### 问题瓶颈与范式转换

端到端从激光雷达进行运动预测的核心瓶颈在于**多模态未来轨迹的推理困难**与**评估指标的失效**。传统分阶段流水线（检测→跟踪→预测）存在级联误差，每个子模块错误地假设其输入是完美的（Figure 1a）。而现有端到端方法（如**FaF** (Luo et al., CVPR 2018)）从当前帧检测出发前向预测未来位置，只能输出单条确定性轨迹，无法捕捉真实场景中固有的多模态未来分布。

更严重的是，广泛使用的ADE/FDE指标仅评估匹配子集的平均位移误差，不惩罚误报。这使得一个简单的**恒定位置基线**（仅预测静止物体且赋予高置信度）在ADE/FDE上能达到最先进水平，却在移动物体上的预测AP_f为0（Table 1）。这一发现揭示了传统指标可被简单基线轻易欺骗的根本缺陷。

FutureDet的核心洞察在于**将预测任务重构为未来物体检测**：通过检测器在多个未来时刻生成热图，再将未来检测回溯到当前帧，利用多对一匹配机制自然捕捉多模态未来（Figure 2）。这种"检测未来→回溯轨迹"的范式转换，使得模型无需显式轨迹生成模块即可端到端地输出多未来预测。

### 方法谱系定位

#### 与端到端感知预测方法的关系

FutureDet位于**端到端LiDAR感知预测**这一研究脉络中，与以下工作构成直接对比：

- **FaF** (Luo et al., CVPR 2018)：首个端到端从LiDAR进行检测和预测的工作，从当前检测前向预测速度。FutureDet将其作为主要基线（标记为FaF*，即论文的重新实现版本），在车辆非线性运动子集上AP_f提升4%（K=5时），行人预测mAP_f达到26.9，超过FaF* 0.5点（Table 2, Table 3）。

- **PnPNet** (Liang et al., CVPR 2020)：端到端感知与预测方法，在Table 1的指标分解中，其ADE/FDE表现被恒定位置基线超越，但在预测mAP上优于该基线。

- **SPF2** (Weng et al., CoRL 2020)：先预测未来点云再进行检测的流水线方法，同样在Table 1中展示了传统指标的局限性。

FutureDet与上述方法的本质区别在于**预测方向**：从"当前→未来"的前向预测转为"未来→当前"的回溯匹配，这使得多未来建模成为检测头输出的自然产物，而非需要额外设计的生成模块。

#### 与轨迹预测方法的关系

在传统轨迹预测领域，**Trajectron++** (Salzmann et al., ECCV 2020)是代表性的自回归轨迹预测模型，但其依赖完美轨迹输入（而非原始传感器数据）。FutureDet在联合检测与预测的设定下，车辆和行人的预测mAP均显著优于Trajectron++（Table 2, Table 3）。值得注意的是，Trajectron++在非线性运动上的AP_f仅为2.8，而FutureDet达到更高水平，这表明端到端从传感器直接预测相比基于完美轨迹的预测具有更强的鲁棒性。

#### 技术组件溯源

FutureDet的架构组件可追溯到以下工作：

- **特征编码器**：采用VoxelNet/PointPillars风格的骨干网络累积历史LiDAR扫描并提取BEV特征，这是3D检测领域的标准做法。

- **检测头设计**：基于**CenterPoint** (Yin et al., CVPR 2021)的检测架构进行改造，通过浅层特征变换网络（Shallow Feature Transform）将当前特征映射到未来特征空间（Figure 6），而非为每个时间步独立训练检测头。

- **多对一匹配机制**：将多个未来检测回溯匹配到当前帧检测，这一设计借鉴了多假设跟踪的思想，但将其融入端到端检测框架中。

### 适用边界与局限

#### 数据分布依赖

FutureDet的性能高度依赖训练数据的分布特性。nuScenes数据集中超过60%的车辆处于静止状态，导致模型倾向于预测匀速运动或静止（Figure 3）。虽然通过子类平均AP_f（静态/线性/非线性）缓解了评估偏差，但模型本身并未从机制上克服这一数据不平衡。消融实验显示，使用轨迹级复制粘贴数据增强（Trajectory Sampler）可以部分缓解轨迹长尾分布，提升非线性运动预测性能。

#### 多模态多样性的局限

尽管FutureDet通过多对一匹配自然支持多未来输出，但**并未显式强制生成多样化轨迹**。定性结果显示，部分多未来预测聚集在一起，缺乏足够的模态覆盖（Figure 3, Figure 5）。特别是在行人预测中，多个未来预测通常都呈线性且相似，无法有效捕捉行人的突然转向或交互行为（Figure 5）。

#### 误报控制不足

FutureDet的原始输出包含大量误报检测与预测（Figure 4），需要后处理才能用于下游规划任务。这一局限源于检测范式本身：模型被训练为在每个未来时刻独立生成热图，缺乏对时序一致性的显式约束。

#### 地图信息融合失效

添加道路掩码作为输入通道对行人预测性能几乎无影响（Table 3），表明模型可能已从LiDAR数据中隐式学习空间上下文，但如何最佳融合LiDAR与HD地图信息以提升预测精度仍是一个开放问题。

### 开放问题与未来方向

1. **多样化轨迹生成机制**：如何设计损失函数或架构组件，显式鼓励多个未来预测覆盖不同的运动模态（如左转/右转/直行），而非仅输出相似轨迹？

2. **时序一致性约束**：如何在检测头之间引入时序依赖，减少跨时刻的误报不一致问题，使回溯匹配更加可靠？

3. **地图信息有效融合**：鉴于道路掩码输入未能显著提升性能，需要探索更有效的地图编码方式（如车道图拓扑、交通规则约束）与LiDAR特征的融合策略。

4. **恒定速度基线的启示**：为什么简单的匀速外推基线在文献中被长期忽视却具有强大性能？这一发现提示需要重新审视预测任务的难度来源——在nuScenes这类以结构化道路为主的数据集上，运动模式的多样性可能被高估。

5. **非线性运动建模**：当前模型在非线性运动（如转弯、避障）上的预测精度仍有较大提升空间，需要探索专门的机制来捕捉加速度和方向变化。

6. **下游任务适配**：如何设计轻量级后处理模块，在保留多未来多样性的同时有效抑制误报，使FutureDet的输出可直接用于运动规划和决策？



## 原文 PDF

![[paperPDFs/CVPR_2022/Forecasting_from_LiDAR_via_Future_Object_Detection.pdf]]
