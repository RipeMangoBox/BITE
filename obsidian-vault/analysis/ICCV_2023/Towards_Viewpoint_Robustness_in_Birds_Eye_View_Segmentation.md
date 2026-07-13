---
title: "Towards Viewpoint Robustness in Bird's Eye View Segmentation"
type: paper
paper_level: A
venue: ICCV
year: 2023
pdf_ref: paperPDFs/ICCV_2023/Towards_Viewpoint_Robustness_in_Bird_s_Eye_View_Segmentation.pdf
project_link: https://nvlabs.github.io/viewpoint-robustness/
code_link: null
aliases:
- NBVAF
- TVRBSEVS
tags:
- ICCV_2023
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "训练数据中是否包含目标相机视点的观测；通过新视角合成（NVS）生成目标视点的图像并加入训练，可以控制模型对目标视点的泛化能力。"
primary_logic: "利用改进的Worldsheet新视角合成方法，将源视点采集的已标注数据变换到目标视点，无需额外采集和标注，即可为任意目标车辆类型训练高精度的BEV分割模型，从而弥合视点域差距。"
claims:
- "仅将相机pitch降低10°就导致CVT的BEV分割IoU下降17%。"
- "在CARLA中系统分析表明，LSS和CVT在所有测试的相机视点变化（yaw、pitch、height、pitch+height）下，IoU均出现大幅度下降。"
- "所提出的NVS视点增强方法在部署到新相机平台时，平均能够恢复因视点变化而损失的IoU的14.7%。"
- "将25%–50%的训练数据通过NVS变换到目标视点并与源数据混合，可获得最佳的泛化IoU；完全使用变换数据（100%）会因NVS引入的artifact导致性能下降。"
---

# Towards Viewpoint Robustness in Bird's Eye View Segmentation

> [!tip] 核心洞察
> 利用改进的Worldsheet新视角合成方法，将源视点采集的已标注数据变换到目标视点，无需额外采集和标注，即可为任意目标车辆类型训练高精度的BEV分割模型，从而弥合视点域差距。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向鸟瞰图分割的视点鲁棒性研究 |
| 英文题名 | Towards Viewpoint Robustness in Bird's Eye View Segmentation |
| 会议/期刊 | ICCV 2023 |
| Links | [paper](https://arxiv.org/abs/2309.05192) · [Project](https://nvlabs.github.io/viewpoint-robustness/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | 基于新视角合成的视点增强框架 (NVS-based Viewpoint Augmentation Framework) |
| Dataset | NVIDIA DRIVE Sim 目标视点（pitch ±5°, ±10°; depth +1.5m; height +0.2m, +0.8m）, CARLA synthetic views (yaw +12°) |

> [!tip] 效果简介
> - NVIDIA DRIVE Sim 目标视点（pitch ±5°, ±10°; depth +1.5m; height +0.2m, +0.8m） 上，平均恢复的IoU损失比例 为 14.7%，对比 0% (仅源数据训练)，变化 +14.7%。
> - CARLA synthetic views (yaw +12°) 上，IoU 为 N/A，对比 oracle model (上限 IoU ~0.35)，变化 源模型在目标视点 IoU 降至 ~0.15 (CVT) 或更低。

## 概要

现有的鸟瞰图（BEV）分割模型在训练时所依赖的相机视点与测试时存在微小偏差时，其分割精度会急剧下降。例如，仅将相机俯仰角（pitch）降低10°，就导致基于Cross View Transformers（CVT）的BEV分割IoU下降17%（Figure 1）。这一现象揭示了当前BEV感知系统在跨车辆平台部署时面临的核心瓶颈：**视点域差距（viewpoint domain gap）**。

针对上述问题，本文提出了一种**基于新视角合成（Novel View Synthesis, NVS）的视点增强框架**。其核心思路是：利用改进的Worldsheet方法，将源视点下已标注的训练数据变换到目标视点的成像平面上，生成具有目标视点几何特性的合成图像，并将这些图像按一定比例混入训练集。该方法无需在目标车辆平台上进行额外的数据采集与标注，即可显著提升BEV分割模型对未见相机配置的泛化能力。

在NVIDIA DRIVE Sim合成环境下的系统评估表明，所提方法在多种视点变化场景（包括pitch、深度、高度变化）中，平均能够恢复因视点变化而损失的IoU的**14.7%**。消融实验进一步揭示，将训练数据中**25%–50%**的图像通过NVS变换至目标视点并与源数据混合，可获得最佳的泛化IoU；完全使用变换数据（100%）反而会因NVS引入的合成artifact导致性能下降。这些结果确立了NVS视点增强作为一种轻量、高效的数据域适应策略，在提升BEV分割视点鲁棒性方面的有效性。



鸟瞰图（BEV）分割是自动驾驶感知的核心任务，旨在从多视角2D图像中推理出车辆周围道路元素（如车道线、可行驶区域）的俯视语义布局。近年来，以 **LSS**（Lift-Splat-Shoot, Philion & Fidler, ECCV 2020）和 **CVT**（Cross-View Transformers, Zhou & Krähenbühl, ECCV 2022）为代表的方法在BEV分割上取得了显著进展，它们分别代表了基于卷积的显式几何投影和基于Transformer的隐式几何学习两条技术路线。

然而，现有研究普遍忽视了一个关键问题：**BEV分割模型对测试时相机视点的微小变化极其敏感**。如 Figure 1 所示，当目标车辆的相机俯仰角（pitch）仅降低10°时，CVT的BEV分割IoU便急剧下降17%。这种脆弱性源于训练数据与部署平台之间的“视点域差距”——模型在训练期间仅见过源相机平台采集的特定视角数据，一旦部署到相机安装位置（pitch、yaw、高度）略有不同的新车型或改装平台上，泛化性能便大幅衰退。

为系统量化这一问题的严重性，本文首先在CARLA仿真环境中进行了受控分析（Figure 3）。实验覆盖了偏航角、俯仰角、相机高度及其组合共36种视点配置，结果表明：无论是LSS还是CVT，在所有测试的视点变化下，IoU均出现大幅度下降——例如，偏航角增加12°时，LSS的IoU从约0.35降至约0.15。即使为每个目标视点单独训练“oracle”模型作为性能上界，源模型与oracle之间的巨大差距依然表明，**视点鲁棒性是当前BEV分割方法的系统性缺陷**，而非特定架构的偶然问题。

解决这一缺陷的传统思路——为每种目标车辆平台重新采集并标注大量数据——成本高昂且难以规模化。因此，本文的核心动机在于：**能否在不增加任何真实采集和标注成本的前提下，弥合源视点与目标视点之间的域差距？** 本文提出了一种基于新视角合成（Novel View Synthesis, NVS）的视点增强框架，通过将源视点的已标注图像变换到目标视点，生成混合训练集，从而赋予BEV模型对未见相机配置的泛化能力。该方法在NVIDIA DRIVE Sim评估中平均恢复了因视点变化而损失的IoU的14.7%，为BEV分割的实际部署提供了一条低成本、可扩展的鲁棒性提升路径。



## 核心方法与创新机理

本文的核心创新在于提出了一种**基于新视角合成（Novel View Synthesis, NVS）的视点增强框架**，以极低的成本弥合BEV分割模型在源视点与目标视点之间的泛化鸿沟。其关键洞察在于：通过操纵训练数据的视点分布，即可控制模型对未见相机配置的鲁棒性，而无需在目标平台上进行任何真实数据采集或标注。

### 创新一：视点鲁棒性的因果机制建模

现有BEV分割方法（如LSS和CVT）的设计隐含假设了训练与测试时相机视点的一致性。本工作首次系统揭示了这一假设的脆弱性：当测试时相机pitch仅降低10°时，CVT的BEV分割IoU即下降17%（Figure 1）；在CARLA仿真环境中，LSS和CVT在yaw、pitch、height及其组合变化下均出现大幅度IoU衰减（Figure 3）。这一分析确立了“训练数据中是否包含目标视点观测”是控制模型泛化能力的**因果旋钮**。

### 创新二：改进的Worldsheet NVS方法

为实现从源视点到目标视点的数据变换，本工作在Worldsheet（Hu et al., 2022）的基础上进行了四项关键改进，使其能够处理自动驾驶场景中的动态物体和遮挡：

- **SSIM损失**：在像素级L1损失之外引入结构相似性约束，提升渲染图像的结构保真度。
- **最小像素损失（Min Loss）**：对相邻两帧的渲染结果取逐像素最小值，作为图像损失和渲染深度损失的计算策略，有效处理遮挡区域。
- **自动掩码（Automasking）**：自动识别并屏蔽动态物体区域，避免其对静态场景几何学习的干扰。
- **激光雷达深度监督**：引入激光雷达点云作为深度真值，直接监督单帧深度预测，显著提升深度估计精度。

消融实验（Table 1）表明，这四项改进将NVS质量从基础Worldsheet的PSNR大幅提升至22.936 dB，SSIM达到0.608，深度L1误差降至0.00657。

### 创新三：数据混合策略的发现

直接将NVS生成的目标视点数据与源数据混合训练BEV模型，是本框架的核心操作。关键的**changed slot**在于：

| 维度 | 基线方案 | 本工作方案 |
|------|----------|------------|
| **训练数据视点** | 仅包含源相机视点的真实数据 | 源视点数据 + 经NVS生成的目标视点数据（混合比例25%–50%） |
| **训练数据内容** | 原生采集图像 | 部分经NVS变换的图像，可能含有少量合成artifact但足以显著提升视点鲁棒性 |

消融研究（Figure 8）揭示了一个非单调的最优混合规律：随着变换数据比例从0%增加到50%，BEV分割IoU持续提升；但完全使用变换数据（100%）反而因NVS引入的域差距（artifact）导致性能下降。这一发现表明，NVS数据的作用并非替代真实数据，而是作为**视点正则化项**，引导模型学习跨视点不变的特征表示。

在NVIDIA DRIVE Sim的六种目标视点配置上，该框架平均恢复了因视点变化而损失的IoU的14.7%（Table 2），且仅需25%–50%的训练数据经过NVS变换即可实现。



本文提出一种**基于新视角合成的视点增强框架**，核心思路是：在训练阶段，利用新视角合成（Novel View Synthesis, NVS）将源相机平台采集的已标注图像变换到目标相机平台的视点，再将变换后的数据按一定比例混入训练集，使BEV分割模型在未见过的目标视点上获得鲁棒性。

### 管线总览

整个框架由三个核心模块串联构成，如图4所示：

1. **改进的Worldsheet NVS模块**：输入单帧前视图像，估计稠密深度图并构建带顶点偏移的3D网格；通过改变相机外参，将网格渲染到目标视点，生成新视角图像及其对应深度图。
2. **数据混合模块**：将NVS生成的图像按预设比例（实验表明25%–50%最佳）与源视点真实数据混合，构建最终的BEV训练集。
3. **BEV分割模型**：在混合数据集上训练CVT（Cross View Transformers），从多视图2D图像预测鸟瞰视角分割结果。推理时直接部署到目标视点，无需额外NVS步骤。

### 输入输出流

- **输入**：源相机平台采集的单前视图像及其标注（BEV分割标签），以及目标相机平台的内外参。
- **NVS变换过程**：对每张源图像依次执行——(1) 深度估计；(2) 构建场景3D网格 `M = ({V_{(x,y)}}, {F})`；(3) 将相机视点变换至目标平台参数；(4) 渲染生成目标视点下的图像。渲染方程可表示为：
  $$\{\hat{\mathbf{I}}_n^{n+1}, \hat{\mathbf{D}}_n^{n+1}\} = render(\{V_{(x,y)}^{n+1}\}, \{F^{n+1}\}, T^{n+1})$$
- **输出**：经混合数据训练后的BEV分割模型，可直接在目标视点图像上推理，输出鸟瞰视角下的语义分割图。

### 关键设计选择

- **NVS基础架构**：基于Worldsheet进行扩展，针对自动驾驶场景中的动态物体和遮挡问题，引入了四项改进——SSIM损失、最小像素损失（ML）、自动掩码（AM）和激光雷达深度监督（LS）。消融实验（Table 1）表明，这些改进将PSNR提升至22.936 dB，SSIM提升至0.608，深度L1误差降至0.00657。
- **遮挡处理**：利用相邻帧的时间一致性，对两帧渲染结果取逐像素最小值作为损失，公式为：
  $$L_{im} = \frac{1}{\mathcal{P}} \sum_{i=1}^{\mathcal{P}} \min(|I_{n,i} - \hat{\mathbf{I}}_{n,i}^{n+1}|, |I_{n,i} - \hat{\mathbf{I}}_{n,i}^{n-1}|)$$
- **数据混合策略**：并非全部使用NVS数据，而是将25%–50%的训练数据变换到目标视点并与源数据混合。完全使用变换数据（100%）会因NVS引入的artifact导致性能下降（Figure 8）。

### 适用范围说明

当前框架仅基于单前视相机进行验证，未涉及多相机环视配置。评估依赖NVIDIA DRIVE Sim合成数据，虽较CARLA更真实，但与实际道路场景仍存在域差距。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2309_05192/figures/004_Figure_4.jpg]]
*Figure 4: Proposed Pipeline. Current methods for bird’s eye view (BEV) segmentation are trained on data captured from one set of camera rigs (the source rig). At inference time, these models perform well on that camera rig, but, according to our analysis, even small changes in camera viewpoint lead to large drops in BEV segmentation accuracy. Our solution is to use novel view synthesis to augment the training dataset. We find this simple solution drastically improves the robustness of BEV segmentation models to data from a target camera rig, even when no real data from the target rig is available during training*



### 方法管线总览

本工作提出**基于新视角合成（NVS）的视点增强框架**，其核心思路是：利用时序相邻帧的一致性，训练一个NVS模型，将源视点采集的已标注图像变换到目标相机视点，再将生成数据按一定比例混入训练集，最终训练BEV分割模型（如CVT）。管线包含三个核心模块：改进的Worldsheet NVS模块、数据混合模块、以及下游BEV分割模型训练模块（Figure 4）。

### 改进的Worldsheet NVS模块

NVS模块建立在Worldsheet（Hu et al., 2022）之上，将其从静态场景扩展至包含动态物体和遮挡的复杂自动驾驶场景。其核心流程为：

1. **深度估计与3D网格构建**：对输入的单张图像，通过深度网络预测逐像素深度图，并在此基础上构建场景的3D网格。网格定义为：

   $$M = (\{V_{(x,y)}\}, \{F\})$$

   其中 $\{V_{(x,y)}\}$ 表示由预测深度和可学习的顶点偏移量构成的3D顶点集合，$\{F\}$ 表示网格的面片结构。该网格是对场景几何的显式离散化表达，为后续视点变换提供几何载体。

2. **时序一致性训练**：与原始Worldsheet依赖多视图一致性不同，本方法利用自动驾驶数据中天然存在的时序相邻帧（第 $n-1$、$n$、$n+1$ 帧）来训练NVS模型。核心思想是：将第 $n+1$ 帧（或第 $n-1$ 帧）构建的网格，通过目标相机外参 $T^{n+1}$（或 $T^{n-1}$）渲染到第 $n$ 帧的视点，生成新视角图像和深度图：

   $$\{\hat{\mathbf{I}}_n^{n+1}, \hat{\mathbf{D}}_n^{n+1}\} = render(\{V_{(x,y)}^{n+1}\}, \{F^{n+1}\}, T^{n+1})$$

   其中 $\hat{\mathbf{I}}_n^{n+1}$ 和 $\hat{\mathbf{D}}_n^{n+1}$ 分别表示从第 $n+1$ 帧渲染到第 $n$ 帧视点的新视角图像和深度图，$render(\cdot)$ 为可微渲染函数。

3. **遮挡处理与损失函数**：为处理时序帧之间的遮挡和去遮挡区域，本方法引入**最小像素损失（Min Loss, ML）**策略——对相邻两帧（$n-1$ 和 $n+1$）分别渲染到第 $n$ 帧视点，然后逐像素取与真实图像 $I_n$ 之间损失的最小值：

   $$\mathcal{L}_{im} = \frac{1}{\mathcal{P}} \sum_{i=1}^{\mathcal{P}} \min(|I_{n,i} - \hat{\mathbf{I}}_{n,i}^{n+1}|, |I_{n,i} - \hat{\mathbf{I}}_{n,i}^{n-1}|)$$

   其中 $\mathcal{P}$ 为像素总数。该设计的基本逻辑是：对于第 $n$ 帧中被遮挡的区域，至少有一侧相邻帧能够提供有效的可见信息，取最小值可避免对遮挡区域施加不合理的监督信号。

   深度监督同样采用直接损失与渲染损失相结合的方式。直接深度损失约束单帧深度预测与激光雷达真值的一致性：

   $$\mathcal{L}_{D}^{direct} = \frac{1}{\mathcal{P}} \sum_{i=1}^{\mathcal{P}} |D_{n-1,i} - F_{depth}(I_{n-1,i})| + |D_{n+1,i} - F_{depth}(I_{n+1,i})|$$

   渲染深度损失则约束渲染深度图与真实深度图的一致性，同样采用最小策略处理遮挡：

   $$\mathcal{L}_{D}^{rendered} = \frac{1}{\mathcal{P}} \sum_{i=1}^{\mathcal{P}} \min(|D_{n,i} - \hat{\mathbf{D}}_{n,i}^{n+1}|, |D_{n,i} - \hat{\mathbf{D}}_{n,i}^{n-1}|)$$

   此外，本方法在Worldsheet基础上额外引入了SSIM损失、自动掩码（Automasking）机制，共同提升NVS质量。消融实验（Table 1）表明，逐步加入这些改进后，NVS的PSNR达到22.936 dB，SSIM达到0.608，深度L1误差降至0.00657，显著优于原始Worldsheet。

### 数据混合与BEV训练模块

给定已标注的BEV分割源数据集 $\mathcal{D}_{source}$（规模为 $N$），NVS模块将其中 $n$ 张图像变换到目标相机视点，生成目标视点数据集 $\mathcal{D}_{target\_pred}$（规模为 $n$）。变换过程包括四个步骤：(1) 估计每张图像的深度图；(2) 构建3D网格；(3) 修改相机参数至目标视点；(4) 将网格渲染到目标视点。

将 $\mathcal{D}_{target\_pred}$ 与 $\mathcal{D}_{source}$ 按一定比例混合，构建最终训练集。下游BEV分割模型（如CVT）在该混合数据集上训练，学习从2D多视图图像预测鸟瞰视角分割结果。消融实验（Figure 8）表明，变换25%–50%的训练数据可获得最佳泛化IoU；完全使用变换数据（100%）反而因NVS引入的合成artifact导致性能下降，揭示了合成数据质量与数量之间的权衡关系。



## 实验与关键发现

### 视点变化对BEV分割的破坏性影响

论文首先在CARLA仿真环境中系统量化了相机视点变化对现有BEV分割模型的冲击。实验以nuScenes外参作为源相机配置，分别训练LSS和CVT模型，然后在36种不同视点配置下进行测试，每次仅改变单一参数（yaw、pitch、height）或组合参数（pitch+height）。Figure 3的结果揭示了一个核心发现：**即使是微小的视点偏移，也会导致IoU大幅崩溃**。

具体而言，当相机yaw角增加12°时，CVT的IoU从约0.35骤降至约0.15，LSS也呈现类似幅度的下降。pitch变化同样具有破坏性——仅降低10°就导致CVT的IoU损失17%（Figure 1）。值得注意的是，相机高度变化对LSS的影响相对温和（IoU从约0.35降至约0.30），但CVT对高度变化仍然敏感。在组合变化（pitch+height）场景下，两种模型的性能退化更为严重。

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2309_05192/figures/001_Figure_1.jpg]]
*Figure 1: Impact of Changed Camera Viewpoint: We find that the performance of state-of-the-art methods for bird’s eye view (BEV) segmentation quickly drop with small changes to viewpoint at inference. Above we see predictions from Cross View Transformers [29] trained on data from a source rig (top). The target rig pitch is reduced by 10◦ (bottom), leading a 17% drop in IoU*

实验同时训练了各目标视点的“oracle模型”（直接在目标视点数据上训练），作为该视点的性能上界。对比发现，源模型在目标视点的IoU与oracle之间存在巨大差距，且这一差距无法通过简单的数据增强弥合——这直接指向了**训练数据中目标视点观测缺失**这一根本瓶颈。

### NVS质量消融：从Worldsheet到完整方法

Table 1系统消融了NVS模块中各改进组件对合成质量的贡献。以原始Worldsheet为基线，逐步添加SSIM损失、最小损失（ML）、自动掩码（AM）和激光雷达深度监督（LS），在1000张测试图像上评估PSNR、SSIM和深度L1误差。

| 配置 | PSNR (dB) ↑ | SSIM ↑ | Depth L1 ↓ |
|------|-------------|--------|------------|
| Worldsheet (WS) | 基线 | 基线 | 基线 |
| WS + SSIM | 提升 | 提升 | — |
| WS + SSIM + ML | 进一步提升 | 进一步提升 | — |
| WS + SSIM + ML + AM | 继续提升 | 继续提升 | — |
| WS + SSIM + ML + AM + LS (完整方法) | **22.936** | **0.608** | **0.00657** |

消融揭示了一条清晰的因果链：**SSIM损失**改善了纹理保真度；**最小损失**通过逐像素选取两帧渲染结果中的最优值，有效处理了动态物体和遮挡区域的伪影；**自动掩码**过滤了训练信号不可靠的像素；**激光雷达深度监督**则显著提升了深度估计精度，进而改善了3D网格的几何质量。Figure 5的定性对比直观展示了这一递进式改进——完整方法生成的未校正图像和深度图在动态物体边缘和遮挡边界处明显优于原始Worldsheet。

### 主实验结果：视点增强的有效性

Table 2汇总了在NVIDIA DRIVE Sim上使用CVT架构的主要实验结果。测试覆盖六种目标视点配置：pitch ±5°、pitch ±10°、depth +1.5m、height +0.2m、height +0.8m。对比方法包括：

- **Source-only**：仅使用源视点数据训练（下界）
- **Identity Augmentations (Id. Aug.)**：颜色抖动、裁剪、翻转等传统增强
- **Extrinsic Augmentations (Extr. Aug.)**：对外参矩阵和3D标签施加随机旋转，模拟视点变化但不进行实际图像变换
- **Ours (NVS Augmentation)**：将部分训练数据通过NVS变换到目标视点后混合训练

结果显示，Source-only模型在所有目标视点上均表现最差，IoU普遍在0.14-0.18区间。Id. Aug.和Extr. Aug.仅能提供微弱改善，表明传统增强策略无法弥合视点域差距。相比之下，**NVS增强方法在所有目标视点上均取得显著提升，平均恢复因视点变化而损失的IoU的14.7%**。例如，在pitch -10°配置下，IoU从source-only的约0.14提升至0.165；在height +0.8m配置下达到0.214，接近源视点上的oracle性能（Table 2第一行）。

### 关键消融：变换数据比例的影响

Figure 8揭示了训练数据中NVS变换图像比例与BEV分割性能之间的非单调关系。实验逐步将变换数据比例从0%增加到100%，发现：

- **0%-25%**：IoU快速提升，少量目标视点数据即可显著改善泛化
- **25%-50%**：达到性能平台，获得最佳测试IoU
- **50%-100%**：IoU开始下降，100%变换数据训练的性能明显劣于25%-50%混合训练

这一现象的根本原因在于**NVS引入的合成artifact与真实数据之间存在域差距**。当变换数据比例过高时，模型过度拟合NVS特有的伪影模式（如纹理模糊、边缘失真），反而损害了对真实目标视点图像的泛化能力。25%-50%的混合比例在“引入目标视点信息”和“保持源数据真实性”之间取得了最优平衡。

### 插值与外推泛化

论文进一步探索了NVS增强模型的插值和外推能力。使用两个视点数据训练的模型，在未见过的中间视点（插值）上达到14.9% IoU，在外推视点上达到14.8% IoU。这一结果表明，NVS增强不仅能在已知目标视点上恢复性能，还能赋予模型一定程度的连续视点泛化能力——这对于实际部署中相机安装误差和车辆姿态变化具有重要价值。

### 失败模式与局限

尽管NVS增强方法整体有效，实验仍暴露了若干值得关注的失败模式：

1. **大视点变换下的artifact加剧**：在height +0.8m的极端变换中，NVS生成的图像出现明显的几何失真和纹理伪影，导致该配置下IoU恢复幅度相对有限（Table 2中0.214 vs source-only的0.18左右，提升幅度小于其他配置）。

2. **LSS在负pitch下的oracle偏差**：CARLA分析中，LSS在负pitch下的oracle模型性能异常偏低，可能源于CARLA渲染管线中未完全控制的因素（如遮挡模式变化），这提示仿真分析的结论需在真实场景中谨慎外推。

3. **单相机配置的局限性**：所有实验均基于单前视相机，未验证多相机环视配置下的视点鲁棒性。实际自动驾驶系统通常配备6-8路相机，多相机间的视点协同变化可能引入更复杂的退化模式。

4. **仿真-真实域差距**：评估依赖NVIDIA DRIVE Sim合成数据，虽比CARLA更真实，但与实际道路数据仍存在光照、天气、纹理等方面的差异，方法在完全真实场景中的稳定性尚待实车验证。

### 公平性说明

实验设计中的若干因素值得读者注意：（1）CARLA分析中CVT未使用外参嵌入（因仿真中外参无噪声），而真实数据实验中外参嵌入被启用，这可能影响两种设置下结果的可比性；（2）CARLA oracle模型在高相机高度下IoU反而更高，可能与视场角变化导致的地面采样密度差异有关，而非模型本身更优；（3）所有对比均使用相同的CVT架构和训练配置，确保了方法层面的公平比较。

### 补充图表

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2309_05192/figures/003_Figure_3.jpg]]
*Figure 3: Analysis of impact of viewpoint changes in CARLA: We train a source BEV model using Lift Splat Shoot (LSS) [21] and Cross View Transformers (CVT) [29], denoted at point 0 on the x axis of each graph. We then test the model across different target rigs where the camera pitch, yaw, height, or pitch and height are changed, as denoted by the different points along the x axes. We also trained each model on the target rig directly and refer to this model as the ”oracle”, as it reflects the expected upper bound IoU for each viewpoint*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2309_05192/figures/007_Table_1.jpg]]
*Table 1: NVS Ablation: We ablate our changes, which improve NVS and depth over Worldsheet (WS). We test with 1K images*

![[assets/figures/papers/paper_list_l39_https_arxiv_org_abs_2309_05192/figures/009_Table_2.jpg]]
*Table 2: Results: We report the IoU of the CVT model trained on a source rig and tested across target rigs where pitch, depth, and height are changed (source). We then compare against two baselines, described in text. Last, we compare with our method, which is trained with some data transformed to the target rig view. The first row shows IoU of the source evaluated on sim data from the same viewpoint, and is our best estimate of oracle performance*



## 定位与知识库关联

### 问题定位与核心瓶颈

本文揭示并解决了一个此前被忽视的系统性脆弱性：当前最先进的BEV分割模型（如**LSS**（Philion & Fidler, ECCV 2020）和**CVT**（Zhou & Krähenbühl, CVPR 2022））对测试时相机视点的微小变化极其敏感。实验表明，仅将相机pitch降低10°就导致CVT的BEV分割IoU下降17%（Figure 1）；在CARLA中系统改变yaw、pitch、height及其组合时，两种架构的IoU均出现大幅度下降（Figure 3）。这一瓶颈的本质在于：训练数据仅覆盖单一源视点的观测分布，模型学到的2D→3D映射高度依赖于特定的相机外参，缺乏对未见视点的泛化能力。

### 方法谱系：从域适应到新视角合成

现有应对训练-测试分布偏移的范式主要包括三类，本文的方法定位与它们形成互补或替代关系：

**域适应与域泛化。** 传统域适应方法假设目标域的无标签数据可用，通过对抗训练或自训练对齐特征分布。本文场景的特殊性在于：目标视点的真实图像根本不存在（例如新车型的相机安装位置尚未部署），因此域适应方法无法直接适用。域泛化方法虽不依赖目标域数据，但通常通过数据增强或元学习提升鲁棒性，而本文的分析表明，简单的颜色抖动、裁剪、翻转（Identity Augmentations）或对外参矩阵施加随机旋转（Extrinsic Augmentations）均无法有效弥合视点变化带来的性能损失（Table 2），说明视点偏移构成了一种独特的、需要几何感知的分布偏移类型。

**基于新视角合成的数据增强。** 本文的核心方法属于这一谱系。作者在**Worldsheet**（Hu et al., CVPR 2021）的基础上构建了改进的NVS模块。Worldsheet是一种单图像静态场景NVS方法，通过估计深度图构建3D网格并渲染到新视点。本文的关键改进在于使其适配包含动态物体和遮挡的复杂自动驾驶场景：引入时序相邻帧间的**最小像素损失**（min loss）以处理遮挡、加入**SSIM损失**以提升感知质量、采用**自动掩码**（automasking）机制忽略静态像素、以及利用**激光雷达深度监督**增强几何精度。消融实验（Table 1）表明，这些改进将PSNR从基线的较低水平提升至22.936 dB，深度L1误差降至0.00657。在NVS方法谱系中，本文方案介于纯几何变换（如基于深度图的单应性扭曲）和完全生成式方法（如基于NeRF或扩散模型的新视角生成）之间：它利用几何先验保证结构一致性，同时通过学习残差处理动态场景，在保真度和泛化性之间取得平衡。

**BEV感知架构的内生鲁棒性。** 另一条可能的路径是设计天然对相机外参变化鲁棒的BEV架构（例如显式编码外参不确定性或使用视角无关的表示）。本文未沿此方向探索，而是选择在数据层面解决问题，这使得其方法可与任意BEV架构（LSS、CVT、BEVFormer等）正交组合。这一设计选择的优势在于即插即用，但也意味着方法未从根本上改变模型对相机参数的依赖方式。

### 适用边界与关键假设

本文方法的有效性建立在以下假设之上，超出这些边界时性能可能退化：

1. **单前视相机假设。** 所有实验仅基于单前视相机配置，未验证多相机环视条件下的视点鲁棒性。实际自动驾驶系统通常配备6-8路环视相机，不同相机间的视点变化存在耦合，NVS变换在多相机几何一致性方面的表现尚待研究。

2. **视点变化幅度有限。** 实验覆盖的视点变化范围（pitch ±10°、height +0.8m、depth +1.5m）虽已涵盖典型车型差异，但未测试极端变化（如相机安装位置大幅偏离或旋转角度超过20°）。在此类极端条件下，NVS生成图像中的空洞和artifact可能急剧增加，导致数据增强失效。

3. **合成评估数据的域差距。** 主要评估依赖NVIDIA DRIVE Sim合成数据（Figure 7），虽比CARLA更真实，但与实际道路数据仍存在光照、纹理、天气等方面的域差距。方法在完全真实场景中的稳定性尚待实车验证证实。

4. **NVS质量依赖时序一致性。** NVS训练依赖相邻帧间的时序一致性假设，在高度动态场景（如拥堵路口、快速变道）或大帧间距条件下，该假设可能被违反，导致生成质量下降。

### 局限性与开放问题

**已知局限。** NVS生成的图像仍会引入artifact，尤其在+0.8m高度变换等较大视点偏移时更为明显。这解释了Figure 8中的关键发现：将100%训练数据变换到目标视点反而导致性能下降，而25%-50%的混合比例最优——完全依赖合成数据会引入NVS特有的域差距，源真实数据的存在起到了正则化作用。此外，方法目前为每个目标视点单独训练模型，尚无法生成单个统一模型泛化到多个目标视点。

**开放问题。** 以下方向值得后续工作关注：

- **最优混合比例的自动化确定。** 当前25%-50%的比例是经验性结论，该比例是否因目标视点变化量、场景复杂度、NVS质量等因素而变化，以及如何自动确定最优混合比例，仍需理论指导。

- **多目标视点的统一模型。** 如何利用NVS生成覆盖多个目标视点的混合数据集，训练单个可泛化到任意视点的BEV模型，是实际部署中的关键需求。初步实验（Section 6）表明，利用两个视点数据训练的模型在中间插值视点（14.9% IoU）和外推视点（14.8% IoU）具有一定泛化能力，但距离实用仍有差距。

- **NVS鲁棒性提升。** 在严重遮挡和快速动态物体场景下，当前NVS方法的质量瓶颈如何突破？可能的路径包括融合多帧信息、引入运动补偿、或利用语义先验指导空洞填充。

- **跨任务泛化。** 视点鲁棒性问题是否同样影响其他3D感知任务（3D目标检测、在线高精地图构建、占据预测）？本文提出的NVS增强框架在方法论上具有任务无关性，但具体效果和最优配置可能因任务特性而异，需逐一验证。

- **与架构内生鲁棒性的协同。** 将数据层面的NVS增强与架构层面的外参鲁棒设计（如外参扰动训练、视角无关特征学习）相结合，能否产生超加性收益，是一个值得探索的方向。



## 原文 PDF

![[paperPDFs/ICCV_2023/Towards_Viewpoint_Robustness_in_Bird_s_Eye_View_Segmentation.pdf]]
