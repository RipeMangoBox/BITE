---
title: "Beyond Visual Reconstruction Quality: Object Perception-aware 3D Gaussian Splatting for Autonomous Driving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Beyond_Visual_Reconstruction_Quality_Object_Perception_aware_3D_Gaussian_Splatting_for_Autonomous_Driving.pdf
project_link: null
code_link: https://github.com/Shanicky-RenzhiWang/Perception-aware-3DGS
openreview_forum_id: PmQlMTBmpa
aliases:
- PA3TPALOZQL
- BVRQOPA3GSAD
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "在3DGS训练过程中引入感知对齐损失（直接惩罚检测框和分类的不一致）或对象区域质量损失（强化物体区域的视觉保真度），显式优化感知稳定性。"
primary_logic: "将冻结的感知模型的输出一致性作为优化目标，或通过关注物体区域的局部重建质量，能够在不显著降低全局视觉质量的前提下，大幅提升重建场景对下游感知任务的可用性。"
claims:
- "现有方法（S³Gaussian, OmniRe, EMD）在像素级指标（SSIM最高0.969，PSNR最高35.02）上表现优异，但感知稳定性不足（YOLOv8 mAP仅0.452–0.578，miss高达1.5）。"
- "像素级指标与感知稳定性之间存在弱相关（Pearson r最大0.767，p<5E-3），表明仅优化视觉质量不能可靠地提升感知稳定性。"
- "融入感知对齐损失后，YOLOv8 mAP最高提升至0.700（S³Gaussian+L_perc+L_obj-vis），且miss降至0.0，而视觉质量波动小于1%。"
- "对象区域质量损失在保持视觉质量的同时显著提升物体区域的SSIM（Obj SSIM从0.877到0.924），且计算开销远小于感知损失。"
---

# Beyond Visual Reconstruction Quality: Object Perception-aware 3D Gaussian Splatting for Autonomous Driving

> [!tip] 核心洞察
> 将冻结的感知模型的输出一致性作为优化目标，或通过关注物体区域的局部重建质量，能够在不显著降低全局视觉质量的前提下，大幅提升重建场景对下游感知任务的可用性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 超越视觉重建质量：面向自动驾驶的物体感知增强3D高斯泼溅 |
| 英文题名 | Beyond Visual Reconstruction Quality: Object Perception-aware 3D Gaussian Splatting for Autonomous Driving |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=PmQlMTBmpa) · [GitHub](https://github.com/Shanicky-RenzhiWang/Perception-aware-3DGS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Perception-aware 3DGS Training with Perception-aligned Loss and Object Zone Quality Loss |
| Dataset | Waymo Open Dataset |

> [!tip] 效果简介
> - Waymo Open Dataset 上，mAP (YOLOv8) 为 0.700 (S³Gaussian+L_perc+L_obj-vis)，对比 0.550 (S³Gaussian)，变化 +0.150。
> - Waymo Open Dataset 上，mean IoU (YOLOv8) 为 0.876 (S³Gaussian+L_perc+L_obj-vis)，对比 0.803 (S³Gaussian)，变化 +0.073。
> - Waymo Open Dataset 上，Miss (YOLOv8) 为 0.0 (S³Gaussian+L_perc+L_obj-vis)，对比 1.5 (S³Gaussian)，变化 -1.5。

## 概要

### 问题瓶颈

现有3D高斯泼溅（3DGS）交通场景重建方法（如 **S³Gaussian**（Huang et al., 2024）、**OmniRe**（Chen et al., ICLR 2025）及其运动建模扩展 **EMD**（Wei et al., ICCV 2025））仅以全局视觉相似度（PSNR/SSIM）为优化目标，在像素级指标上表现优异（SSIM最高0.969，PSNR最高35.02），却忽视了自动驾驶系统更依赖的**物体感知稳定性**——即重建场景中感知模块的输出是否与原始场景一致。

初步实验揭示了这一断裂：尽管现有方法视觉质量出色，但YOLOv8检测的mAP仅为0.452–0.578，漏检（Miss）高达1.5。更关键的是，像素级指标与感知稳定性之间仅存在**弱相关**（Pearson r最高0.767，p<5E-3），表明单纯优化视觉质量无法可靠地提升感知可用性。

### 核心方法

本文提出两种互补的感知增强训练策略，在3DGS重建流程中显式注入感知约束：

- **感知对齐损失（Perception-aligned Loss）**：将冻结的感知模型（如YOLOv8）的输出一致性作为优化目标，直接惩罚重建图像与真实图像在检测框（CIoU损失）和分类上的不一致。
- **对象区域质量损失（Object Zone Quality Loss）**：利用真实感知结果生成物体掩码，仅在物体区域内额外计算视觉重建损失，强化关键区域的局部保真度。

两种损失均仅在细阶段训练中应用，与视觉重建损失加权融合，感知模型权重全程冻结，不参与梯度更新。

### 主要结果

在Waymo Open Dataset上的大规模实验表明：

- **感知对齐损失**使YOLOv8的mAP从0.550提升至0.700（S³Gaussian基线上+0.150），漏检从1.5降至0.0，而视觉质量波动小于1%。
- **对象区域质量损失**在保持全局视觉质量的同时，将物体区域SSIM（Obj SSIM）从0.877提升至0.924，且计算开销远小于感知损失。
- 两种损失联合使用在大多数基线上获得**最佳或接近最佳**的感知稳定性与视觉质量平衡，且提升可迁移至黑盒检测器（Faster R-CNN mAP从0.320提升至0.404）。

### 方法定位

本工作属于**3DGS重建训练范式**的改进，不改变网络架构或渲染管线，而是通过损失函数层面的感知注入，将重建目标从“视觉保真”扩展为“视觉保真+感知可用”。其设计思路可泛化至其他重建基线和感知任务，为自动驾驶场景重建的下游任务可用性提供了新的优化维度。



### 自动驾驶场景重建的感知需求错位

自动驾驶系统对三维场景重建的核心需求并非单纯的视觉真实感，而是重建场景能否支撑可靠的下游感知任务。然而，当前主流的3D高斯泼溅（3D Gaussian Splatting, 3DGS）重建方法——包括 **S³Gaussian**（Huang et al., 2024）、**OmniRe**（Chen et al., ICLR 2025）以及基于显式运动建模的 **EMD**（Wei et al., ICCV 2025）——其训练目标均聚焦于最小化渲染图像与真实图像之间的全局视觉差异，典型损失函数为 L1 与 SSIM 的组合。

这一优化目标的隐含假设是：更高的像素级相似度自然意味着更好的感知可用性。**本文的核心发现是这一假设并不成立。**

### 高视觉质量下的感知稳定性缺口

初步实验揭示了现有方法存在显著的“感知-视觉”脱节。如表 1 所示，EMD(OmniRe) 在 Waymo Open Dataset 上达到了 SSIM 0.969、PSNR 35.02 的优异视觉质量，但将其重建图像输入冻结的 YOLOv8 检测器时，mAP 仅为 0.452–0.578，且存在高达 1.5 的漏检率（Miss）。这意味着重建场景中相当数量的物体要么被检测器忽略，要么其检测框与原始场景的检测结果存在显著偏差。

更关键的证据来自像素级指标与感知稳定性之间的统计相关性分析。如表 2 所示，SSIM、PSNR、LPIPS 与 YOLOv8 mAP 之间的 Pearson 相关系数 r 最高仅为 0.767（p < 5E-3），且在不同方法间表现不一致。这一弱相关关系表明：**单纯优化视觉重建质量无法可靠地提升感知稳定性**，两者之间存在结构性张力。

### 问题根源：物体区域的建模断裂与模糊

通过对大量重建失败案例的分析，本文识别出两类典型现象（见 Figure 3）：

- **建模断裂（Modelling Fractures）**：静态物体（如车辆、交通标志）在重建后出现几何不连续或纹理撕裂，导致检测器无法正确识别物体边界。
- **物体区域模糊（Object Zone Blur）**：动态物体（如行人、骑行车辆）在重建中因运动建模不充分而产生区域模糊，使检测框回归和分类置信度下降。

这两类问题均集中在物体区域，而全局视觉损失对背景区域（如路面、天空）的过度拟合掩盖了这些局部退化。因此，核心瓶颈在于：现有方法缺乏针对物体区域的显式优化机制。

### 本文动机：从视觉保真度到感知稳定性

基于上述分析，本文提出将问题重新表述为**约束优化**：在保持视觉重建质量不超过预设阈值的前提下，最小化重建场景与原始场景之间的感知输出差异。形式化表示为：

$$
\min_{\mathcal{R}} \mathbb{E}_{\boldsymbol{x}} [d_{\mathrm{perc}}(\mathcal{P}(\mathcal{R}(\boldsymbol{x})), \mathcal{P}(\boldsymbol{x}))] \quad \mathrm{s.t.} \quad \mathbb{E}_{\boldsymbol{x}} [d_{\mathrm{img}}(\mathcal{R}(\boldsymbol{x}), \boldsymbol{x})] \leq \varepsilon
$$

其中 $\mathcal{R}$ 为重建模型，$\mathcal{P}$ 为冻结的感知模型，$d_{\mathrm{perc}}$ 衡量感知输出的差异，$d_{\mathrm{img}}$ 为视觉重建损失，$\varepsilon$ 为可容忍的视觉质量退化上限。

为实现这一目标，本文提出两类互补的解决方案：

1. **感知对齐损失（Perception-aligned Loss）**：在3DGS训练过程中直接惩罚重建图像与真实图像在感知模型输出（检测框位置、类别标签）上的不一致，将感知稳定性显式纳入优化目标。
2. **对象区域质量损失（Object Zone Quality Loss）**：利用感知模型离线获取的物体掩码，仅在物体区域内计算视觉重建损失，以极低的计算开销强化物体区域的局部保真度。

这两种方法均作为即插即用的损失项集成到现有3DGS训练流程的细阶段，无需修改网络架构或感知模型权重，为自动驾驶场景重建提供了一条从“视觉导向”到“感知导向”的范式转换路径。



## 核心方法与创新机理

本文的核心创新在于将自动驾驶场景重建的优化目标从单一的视觉保真度扩展到**感知稳定性**，并为此提出了两个互补的训练策略：**感知对齐损失**和**对象区域质量损失**。这两种方法均作为即插即用的损失项嵌入现有3DGS训练流程，在不显著牺牲全局视觉质量的前提下，大幅提升重建场景对下游感知任务的可用性。

### 关键瓶颈与因果调节变量

现有3DGS重建方法（如 **S³Gaussian**（Huang et al., 2024）、**OmniRe**（Chen et al., ICLR 2025）、**EMD**（Wei et al., ICCV 2025））在像素级指标上表现优异（SSIM最高0.969，PSNR最高35.02），但其重建图像输入感知模型后的检测输出与原始图像存在显著偏差（YOLOv8 mAP仅0.452–0.578，miss率高达1.5）（Table 1）。统计分析进一步揭示，像素级指标与感知稳定性之间仅存在弱相关（Pearson r最大0.767，p<5E-3）（Table 2），表明单纯优化视觉相似度无法可靠地保障感知一致性。

这一瓶颈的因果调节变量在于**训练目标的重新定义**：将冻结的感知模型的输出一致性作为显式优化项，或将物体区域的局部重建质量作为加权焦点。通过在3DGS的细阶段训练中引入这些信号，模型被引导在保持全局视觉质量的同时，优先修复那些对感知结果影响最大的局部缺陷（如物体断裂和区域模糊）。

### 改变的关键模块：损失函数与区域加权

相对于基线方法仅使用视觉重建损失（L1 + SSIM），本文在两个维度上改变了训练信号：

| 改变维度 | 基线值 | 本文方案 | 证据锚点 |
|---------|--------|---------|---------|
| **损失函数** | 仅视觉重建损失 | 视觉重建损失 + 感知对齐损失（$\mathcal{L}_{\mathrm{perc}}$）和/或 对象区域质量损失（$\mathcal{L}_{\mathrm{obj-vis}}$） | Equation 7 & Section 6.2 |
| **损失应用阶段** | 细阶段训练仅使用视觉损失 | 细阶段训练加入感知损失/对象区域质量损失 | Section 5.1 & Section 7.1 |
| **区域加权策略** | 全局均匀权重 | 对感知模型检测到的物体区域额外计算视觉损失并加权 | Section 6.2 |

**感知对齐损失**直接惩罚重建图像与真实图像在感知输出上的不一致。其由两部分构成：检测框损失采用CIoU，同时惩罚重叠度、中心点距离和长宽比的偏差；分类损失统计类别标签不一致的比例。该损失仅在3DGS参数更新时反向传播，感知模型权重全程冻结。

**对象区域质量损失**则采用更轻量的设计：利用离线获取的真实感知结果生成物体掩码，仅在物体区域内计算视觉相似度损失。由于无需每次迭代进行感知模型推理，其计算开销远小于感知对齐损失（Table 5），同时能显著提升物体区域的SSIM（Obj SSIM从0.877到0.924）（Table 4）。

### 方法谱系与知识库定位

本文的方法属于**感知引导的场景重建**范式，与现有工作形成以下关系：

- **相对于S³Gaussian / OmniRe / EMD**：这些方法专注于提升全局视觉重建质量，本文首次将感知稳定性作为显式优化目标，揭示了视觉质量与感知可用性之间的非单调关系。
- **相对于感知损失的一般形式**：本文将感知损失具体化为检测框CIoU损失与分类一致性损失的组合，并验证了其在2D检测任务上的有效性。
- **相对于对象区域增强方法**：对象区域质量损失提供了一种计算高效、无需在线推理的替代方案，仅依赖离线标注即可实现感知稳定性的提升。

实验表明，在S³Gaussian上同时使用两种损失后，YOLOv8的mAP从0.550提升至0.700，miss率从1.5降至0.0，而SSIM仅从0.924微降至0.920（Table 4）。在黑盒检测器Faster R-CNN上，EMD(OmniRe)组合方案的mAP从0.320提升至0.404（Table 6），验证了感知稳定性的跨模型迁移能力。



![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_PmQlMTBmpa/figures/004_Figure_2.jpg]]
*Figure 2: Overview of this work. Perception stability is measured by comparing the outputs of the same perception model when fed with the original frames versus the reconstructed frames. Based on the perception outputs and the object regions identified by the perception model, we designed a perception-aligned loss and an object zone quality loss to improve perception stability*

### 问题建模：视觉重建质量之外的感知稳定性

现有3DGS重建方法仅优化全局视觉相似度（PSNR/SSIM），忽略了自动驾驶系统更依赖的物体感知稳定性。初步实验（Table 1）揭示了一个关键瓶颈：当前最优方法（S³Gaussian、OmniRe、EMD）在像素级指标上表现优异（SSIM最高0.969，PSNR最高35.02），但感知稳定性严重不足——YOLOv8 mAP仅0.452–0.578，miss率高达1.5。进一步的统计分析（Table 2）表明，像素级指标与感知稳定性之间仅存在弱相关（Pearson r最大0.767，p<5E-3），说明仅优化视觉质量不能可靠地提升感知稳定性。

基于此，本文将问题形式化为一个约束优化目标：在保证重建视觉质量的前提下，最小化感知模型在重建图像与真实图像上输出的期望差异。形式上，给定重建模型$\mathcal{R}$、视觉差异度量$d_{\mathrm{img}}$、感知差异度量$d_{\mathrm{perc}}$和冻结的感知模型$\mathcal{P}$，目标为：

$$\min_{\mathcal{R}} \mathbb{E}_{\boldsymbol{x}} [d_{\mathrm{perc}}(\mathcal{P}(\mathcal{R}(\boldsymbol{x})), \mathcal{P}(\boldsymbol{x}))] \quad \mathrm{s.t.} \quad \mathbb{E}_{\boldsymbol{x}} [d_{\mathrm{img}}(\mathcal{R}(\boldsymbol{x}), \boldsymbol{x})] \leq \varepsilon$$

这一建模将感知模型的输出一致性显式纳入优化目标，而非仅依赖视觉保真度的间接提升。

### Pipeline架构与模块关系

整体框架围绕“感知稳定性引导的3DGS训练”展开，包含五个核心模块，其输入输出流与依赖关系如Figure 2所示。

**1. 3DGS重建模块**：作为框架主干，该模块执行标准的多视角3D高斯泼溅重建流程，包含粗阶段（coarse-stage）和细阶段（fine-stage）训练。输入为多视角图像，输出为新视角的渲染图像$\mathcal{R}(x)$。粗阶段建立场景几何先验，细阶段进行精细化重建——本文的感知相关损失仅在细阶段引入，以避免干扰几何初始化。

**2. 感知模型（冻结）**：采用预训练的检测模型（默认YOLOv8n）作为引导模型，在训练全程冻结权重，不参与梯度更新。其作用是为感知对齐损失提供目标检测输出（边界框$\mathcal{B}$和类别$\mathcal{C}$），作为重建图像感知稳定性的监督信号。

**3. 感知对齐损失计算模块**：该模块接收重建图像$\mathcal{R}(x)$和真实图像$x$，分别通过冻结的感知模型获取检测输出，计算两者之间的感知差异。损失由两部分组成：

$$\mathcal{L}_{\mathrm{perc}} = \sum_i \left( \lambda_{\mathrm{box}} \cdot \mathcal{L}_{\mathrm{box}} ( \mathcal{B}(x), \mathcal{B}(\mathcal{R}(x)) ) + \lambda_{cls} \cdot \mathcal{L}_{\mathrm{cls}} ( \mathcal{C}(x), \mathcal{C}(\mathcal{R}(x)) ) \right)$$

其中边界框损失$\mathcal{L}_{\mathrm{box}}$采用CIoU度量，同时惩罚重叠度、中心点距离和长宽比的偏差；分类损失$\mathcal{L}_{\mathrm{cls}}$统计类别标签不一致的比例。该损失仅反向传播至3DGS参数，感知模型保持冻结。

**4. 对象区域质量损失计算模块**：作为感知对齐损失的计算高效替代方案，该模块利用离线获取的真实感知结果生成物体掩码$\mathcal{B}(x)$，仅在物体区域内计算视觉重建损失：

$$\mathcal{L}_{\mathrm{obj-vis}} = d_{\mathrm{vis}} \big( \mathcal{R}(\boldsymbol{x}) \odot \mathcal{B}(\boldsymbol{x}), \ \boldsymbol{x} \odot \mathcal{B}(\boldsymbol{x}) \big)$$

由于训练过程仅依赖离线标注，无需每次迭代进行感知模型推理，计算开销显著低于感知对齐损失（Table 5证实其额外时间消耗可忽略不计）。

**5. 总损失融合**：将视觉重建损失与感知相关损失按权重组合，形成最终训练目标：

$$\mathcal{L}_{total} = \lambda_{\mathrm{visual}} \cdot \mathcal{L}_{\mathrm{visual}} + \lambda_{\mathrm{perc}} \cdot \mathcal{L}_{\mathrm{perc}} + \lambda_{\mathrm{obj-vis}} \cdot \mathcal{L}_{\mathrm{obj-vis}}$$

所有损失权重$\lambda$在实验中均设为1，避免超参搜索偏差，确保公平对比。梯度通过$\mathcal{L}_{total}$反向传播更新3DGS场景表示参数，而感知模型权重始终冻结。

### 方法谱系与知识库定位

本文工作在现有3DGS交通场景重建方法的基础上，通过引入感知引导的训练策略，将优化目标从纯视觉保真度扩展到下游感知任务的可用性。基线方法包括：**S³Gaussian**（Huang et al., 2024）、**OmniRe**（Chen et al., ICLR 2025）和**EMD**（Wei et al., ICCV 2025，基于前两者的显式运动建模框架）。这些方法的共同特点是仅优化全局视觉重建损失（L1+SSIM），本文在此基础上改变了三个关键设计槽位：

| 设计槽位 | 基线值 | 本文方案 | 证据锚点 |
|---------|--------|---------|---------|
| 损失函数 | 仅视觉重建损失（L1+SSIM） | 视觉损失 + 感知对齐损失（$\mathcal{L}_{\mathrm{perc}}$）和/或对象区域质量损失（$\mathcal{L}_{\mathrm{obj-vis}}$） | Equation 7, Section 6.2 |
| 损失应用阶段 | 细阶段仅使用视觉损失 | 细阶段加入感知损失/对象区域质量损失 | Section 5.1, Section 7.1 |
| 区域加权策略 | 全局均匀权重 | 对感知模型检测到的物体区域额外计算视觉损失并加权 | Section 6.2 |

核心洞察在于：将冻结感知模型的输出一致性作为优化目标（感知对齐损失），或通过关注物体区域的局部重建质量（对象区域质量损失），能够在不显著降低全局视觉质量的前提下，大幅提升重建场景对下游感知任务的可用性。决定性证据表明，融入感知对齐损失后，YOLOv8 mAP最高提升至0.700（S³Gaussian基线为0.550），miss率降至0.0，而视觉质量波动小于1%（Table 4）。对象区域质量损失在保持视觉质量的同时将物体区域SSIM从0.877提升至0.924，且计算开销远小于感知损失（Table 4, Table 5）。



### 3.1 问题形式化：约束优化视角

给定场景表示函数 $\mathcal{R}$、视觉重建损失 $d_{\mathrm{img}}$、冻结的感知模型 $\mathcal{P}$ 及其输出差异度量 $d_{\mathrm{perc}}$，目标是在保持视觉重建质量的前提下最小化感知输出的不一致性。该问题被形式化为带约束的期望优化：

$$
\min_{\mathcal{R}} \mathbb{E}_{\boldsymbol{x}} [d_{\mathrm{perc}}(\mathcal{P}(\mathcal{R}(\boldsymbol{x})), \mathcal{P}(\boldsymbol{x}))] \quad \mathrm{s.t.} \quad \mathbb{E}_{\boldsymbol{x}} [d_{\mathrm{img}}(\mathcal{R}(\boldsymbol{x}), \boldsymbol{x})] \leq \varepsilon
$$

其中 $\boldsymbol{x}$ 为真实图像，$\varepsilon$ 为可容忍的视觉质量退化阈值（Equation 3）。该形式化为后续两种损失函数的设计提供了统一的数学框架。

### 3.2 感知对齐损失（Perception-aligned Loss）

感知对齐损失的核心机制是：将冻结感知模型在重建图像与真实图像上的输出差异作为可微惩罚项，直接注入3DGS训练的反向传播过程。感知模型本身冻结，不参与参数更新。

损失由检测框损失和分类损失两部分加权构成：

$$
\mathcal{L}_{\mathrm{perc}} = \sum_i \left( \lambda_{\mathrm{box}} \cdot \mathcal{L}_{\mathrm{box}} ( \mathcal{B}(x), \mathcal{B}(\mathcal{R}(x)) ) + \lambda_{cls} \cdot \mathcal{L}_{\mathrm{cls}} ( \mathcal{C}(x), \mathcal{C}(\mathcal{R}(x)) ) \right)
$$

其中 $\mathcal{B}(\cdot)$ 和 $\mathcal{C}(\cdot)$ 分别表示感知模型输出的检测框集合和类别标签集合（Equation 4）。

**检测框损失**采用 Complete IoU（CIoU），同时惩罚重叠度、中心点距离和长宽比偏差：

$$
\mathcal{L}_{\mathrm{box}} = 1 - \frac{1}{n} \sum_{i=1}^{n} \mathrm{CIoU} ( \mathcal{B}_i(\boldsymbol{x}), \mathcal{B}_i(\mathcal{R}(\boldsymbol{x})) )
$$

**分类损失**统计类别标签不一致的物体比例：

$$
\mathcal{L}_{\mathrm{cls}} = 1 - \frac{1}{n} \sum_{i=1}^{n} \mathbf{1} ( \mathcal{C}_i(x) = \mathcal{C}_i(\mathcal{R}(x)) )
$$

上述两式的设计依据见 Equation 5 和 Equation 6。

### 3.3 对象区域质量损失（Object Zone Quality Loss）

对象区域质量损失的设计动机源于实证观察：3DGS重建的感知失效主要集中在物体区域，表现为建模断裂（modelling fractures）和物体区域模糊（object zone blur）（Figure 3）。该损失通过在物体掩码区域内额外计算视觉相似度，强制模型关注这些关键区域的重建质量：

$$
\mathcal{L}_{\mathrm{obj-vis}} = d_{\mathrm{vis}} \big( \mathcal{R}(\boldsymbol{x}) \odot \mathcal{B}(\boldsymbol{x}), \ \boldsymbol{x} \odot \mathcal{B}(\boldsymbol{x}) \big)
$$

其中 $\odot$ 表示逐元素乘法，$\mathcal{B}(\boldsymbol{x})$ 为由离线感知模型预生成的物体区域二值掩码（Section 6.2）。与感知对齐损失不同，该损失无需在线推理感知模型，仅依赖预计算的掩码，计算开销显著更低。

### 3.4 总损失融合

两种损失分别与基础视觉重建损失 $\mathcal{L}_{\mathrm{visual}}$ 按权重组合，形成最终训练目标。

**方案一**（感知对齐损失 + 视觉损失）：

$$
\mathcal{L}_{total} = \lambda_{\mathrm{visual}} \cdot \mathcal{L}_{\mathrm{visual}} + \lambda_{\mathrm{perc}} \cdot \mathcal{L}_{\mathrm{perc}}
$$

**方案二**（对象区域质量损失 + 视觉损失）：

$$
\mathcal{L}_{total} = \lambda_{\mathrm{visual}} \cdot \mathcal{L}_{\mathrm{visual}} + \lambda_{\mathrm{obj-vis}} \cdot \mathcal{L}_{\mathrm{obj-vis}}
$$

**方案三**（两者联合）：将 $\mathcal{L}_{\mathrm{perc}}$ 和 $\mathcal{L}_{\mathrm{obj-vis}}$ 同时加入总损失，在大多数基线上取得最优或接近最优的感知稳定性与视觉质量平衡（Table 4, Table 6）。

### 3.5 训练阶段与模块协作

两种感知增强损失均仅在**细阶段训练**（fine-stage）中应用，粗阶段训练保持仅使用视觉损失的标准流程（Section 5.1, Section 7.1）。这一设计的原因在于：粗阶段主要建立场景几何结构，过早引入感知约束可能干扰几何收敛；细阶段则侧重纹理细节优化，此时注入感知信号可有效引导物体区域的精细化重建。

所有实验统一采用 5000 步粗阶段 + 30000 步细阶段的训练配置，且损失权重 $\lambda$ 均设为 1，避免超参搜索引入的偏差。



## 实验与关键发现

### 视觉质量与感知稳定性之间的弱相关性

现有自动驾驶场景重建方法（S³Gaussian、OmniRe、EMD）在像素级视觉质量指标上表现优异，但下游感知稳定性严重不足。**Table 1** 显示，EMD(OmniRe) 的 PSNR 高达 35.02，SSIM 达 0.969，然而其 YOLOv8 检测 mAP 仅为 0.452，且 miss 率高达 1.5。S³Gaussian 的 SSIM 为 0.924，mAP 为 0.550，miss 为 1.5。这表明高视觉重建质量并不能自动保证感知模块输出的一致性。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_PmQlMTBmpa/figures/002_Table_1.jpg]]
*Table 1: Visual Quality and Perception Metrics of Existing Methods (On Average)*

**Table 2** 进一步通过统计分析揭示了这一瓶颈的本质：像素级指标（SSIM、PSNR、LPIPS）与 YOLOv8 检测稳定性（mAP）之间的 Pearson 相关系数 r 最高仅为 0.767（S³Gaussian 的 SSIM，p=2.43E-3），其余方法的相关性更弱（OmniRe 的 SSIM r=0.417，p=3.11E-3）。尽管这些相关性在统计上显著（p<5E-3），但其强度远不足以支撑“优化视觉质量即可可靠提升感知稳定性”的假设。这一发现构成了本文方法设计的核心动机：**需要显式地将感知稳定性作为优化目标**。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_PmQlMTBmpa/figures/003_Table_2.jpg]]
*Table 2: The statistical correlation between pixel-level metrics(mAP) and detection stability with Yolo v8. Limited to page size, more data(correlations with meanIOU) will be shown in the Appendix. r denotes the Pearson correlation coefficient, and p denotes the p-value*

### 感知对齐损失的集成效果

将感知对齐损失 L_perc 集成到 3DGS 细阶段训练后，感知稳定性获得显著提升。**Table 3** 显示，S³Gaussian 的 YOLOv8 mAP 从 0.550 提升至 0.593（+0.043），mean IoU 从 0.803 提升至 0.840，miss 从 1.5 降至 0.83。OmniRe 的 mAP 从 0.489 提升至 0.507，mean IoU 从 0.832 提升至 0.845。值得关注的是，视觉质量指标仅出现微小波动（SSIM 变化 <1%），表明感知对齐损失在几乎不牺牲全局视觉保真度的前提下实现了感知稳定性的增益。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_PmQlMTBmpa/figures/005_Table_3.jpg]]
*Table 3: Perception-aligned Loss Integration, use YOLOv8 as guidance model, test Faster RCNN and RT-DETR as black-box model*

更重要的是，这种感知稳定性的提升能够**迁移到黑盒检测器**。在 Faster R-CNN 上，S³Gaussian+L_perc 的 mAP 从 0.171 提升至 0.229；在 RT-DETR 上，mAP 从 0.494 提升至 0.509。这验证了感知对齐损失并非仅仅过拟合于引导模型（YOLOv8），而是真正改善了重建场景对通用检测器的可用性。

### 对象区域质量损失的双重优势

对象区域质量损失 L_obj-vis 通过在物体掩码区域内额外计算视觉重建损失，直接强化了感知关键区域的保真度。**Table 4** 显示，S³Gaussian+L_obj-vis 将物体区域 SSIM（Obj SSIM）从 0.877 提升至 0.924，同时 YOLOv8 mAP 从 0.550 提升至 0.611，miss 降至 0.83。该方法在视觉质量和感知稳定性之间取得了更均衡的改善。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_PmQlMTBmpa/figures/013_Table_4.jpg]]
*Table 4: Object Zone Quality Loss Integration, use YOLOv8 as guidance model, test Faster RCNN and RT-DETR as black-box model*

**Table 5** 揭示了 L_obj-vis 的关键效率优势。以 S³Gaussian 为例，原始训练每 100 轮耗时 25.79 秒，加入 L_perc 后增至 26.67 秒，而加入 L_obj-vis 后仅为 25.85 秒——几乎无额外开销。对于计算量更大的 EMD(OmniRe)，L_perc 使总训练时间从 381.3 分钟增至 413.2 分钟，而 L_obj-vis 仅需 382.3 分钟。这是因为 L_obj-vis 依赖离线获取的真实感知结果生成物体掩码，训练过程中无需进行感知模型的前向推理。

### 联合损失的最优配置

同时使用 L_perc 和 L_obj-vis 在绝大多数基线上取得了最佳或接近最佳的感知稳定性。**Table 4** 中，S³Gaussian+L_perc+L_obj-vis 的 YOLOv8 mAP 达到 0.700（+0.150），mean IoU 达 0.876（+0.073），miss 降至 0.0——即重建图像中不再出现漏检。EMD(OmniRe)+L_perc+L_obj-vis 在保持最高视觉质量（SSIM 0.969）的同时，mAP 达 0.652，miss 为 0.0。

**Table 6** 的黑盒消融进一步证实了联合损失的有效性：在 Faster R-CNN 上，EMD(OmniRe)+L_perc+L_obj-vis 的 mAP 达 0.404，相较于 OmniRe 基线的 0.320 提升了 0.084。RT-DETR 上，S³Gaussian+L_perc+L_obj-vis 的 mAP 达 0.666，相较于基线的 0.494 提升了 0.172。

![[assets/figures/papers/paper_list_l34_https_openreview_net_forum_id_PmQlMTBmpa/figures/014_Table_6.jpg]]

### 失效模式与定性分析

**Figure 3** 揭示了现有方法的两类典型失效模式：
- **建模断裂（I）**：静态物体（如远处车辆）在重建中出现几何不连续或碎片化，导致检测框偏移或置信度下降。
- **物体区域模糊（II）**：动态物体（如行人）的重建区域出现纹理模糊或边缘退化，使检测器无法准确定位或分类。

加入感知对齐损失后，这些失效得到显著缓解：重建图像中的物体边界更清晰，检测框与真值的一致性明显改善。但需注意，感知对齐损失的效果受限于引导感知模型（YOLOv8n）本身的检测能力——若引导模型在原始图像上即存在漏检或误检，损失信号将无法提供有效监督。

### 公平性说明

所有实验遵循严格的公平对比原则：损失权重 λ 均设为 1，避免超参搜索偏差；所有方法统一使用 5000 步粗阶段 + 30000 步细阶段的训练配置；感知模型权重在整个训练过程中冻结，不涉及任何微调。因此，性能提升完全归因于损失函数设计本身，而非训练策略或模型容量的差异。



## 定位与知识库关联

### 核心瓶颈与因果机制

现有3D高斯泼溅（3DGS）场景重建方法——包括 **S³Gaussian** (Huang et al., 2024)、**OmniRe** (Chen et al., ICLR 2025) 以及在其上构建的显式运动建模框架 **EMD** (Wei et al., ICCV 2025)——均以像素级视觉相似度（PSNR/SSIM）为唯一优化目标。初步实验（Table 1）揭示了这一范式下的根本性瓶颈：尽管上述方法在视觉质量上表现优异（SSIM最高0.969，PSNR最高35.02），但重建场景在下游感知模型（YOLOv8）上的输出与原始场景严重不一致——mAP仅0.452–0.578，漏检（Miss）高达1.5。进一步的统计分析（Table 2）表明，像素级指标与感知稳定性之间仅存在弱相关（Pearson r最大0.767，p<5E-3），证实仅优化全局视觉质量无法可靠地保障感知一致性。

本文的核心因果洞察在于：自动驾驶系统真正依赖的是感知模块在重建场景上的输出稳定性，而非人眼感知的视觉保真度。因此，将冻结的感知模型的输出一致性作为优化目标，或通过关注物体区域的局部重建质量，能够在不显著降低全局视觉质量的前提下，大幅提升重建场景对下游感知任务的可用性。

### 方法定位与差异化

本文提出的两种互补方案——感知对齐损失（Perception-aligned Loss）和对象区域质量损失（Object Zone Quality Loss）——在方法谱系中定位为对现有3DGS训练范式的损失函数层面改进，具有以下差异化特征：

1. **与纯视觉重建范式的对比**：现有方法（S³Gaussian, OmniRe, EMD）在细阶段训练中仅使用视觉重建损失（L1 + SSIM），对场景中所有区域施加全局均匀权重。本文通过引入感知模型引导的损失项，将优化目标从“看起来像”转向“感知起来对”，属于损失函数层面的因果干预。

2. **感知对齐损失的独特设计**：该方法将冻结的检测模型（YOLOv8）的输出作为监督信号，直接惩罚重建图像与真实图像在检测框（CIoU损失）和类别（分类一致性损失）上的不一致。与传统的感知损失（如LPIPS依赖预训练分类网络的特征空间）不同，本文的感知对齐损失直接作用于任务相关的语义输出空间，具有更强的任务针对性。该损失仅在3DGS训练中反向传播，感知模型权重完全冻结。

3. **对象区域质量损失的效率优势**：该方法利用离线获取的真实感知结果生成物体掩码，仅在物体区域内计算额外的视觉重建损失。与感知对齐损失相比，该方法无需在每次训练迭代中进行感知模型推理，计算开销极小（Table 5），同时能够显著提升物体区域的SSIM（Obj SSIM从0.877到0.924），是一种轻量级的感知增强策略。

### 适用边界与局限

1. **损失权重敏感性**：感知稳定性与视觉质量之间的平衡依赖于损失权重λ的选择。本文仅探索了均等权重（所有λ设为1），缺乏针对不同场景的自适应或学习策略。在实际部署中，不同自动驾驶场景（如高速 vs. 城区）可能对视觉保真度和感知稳定性的需求存在差异。

2. **计算开销瓶颈**：感知对齐损失需在每次训练迭代中额外交付感知模型推理，导致训练时间显著增加（Table 5：EMD(OmniRe)总训练时间从约400分钟增至413.2分钟）。这一开销在更大规模场景或更复杂的感知模型下可能进一步放大。

3. **对感知模型的依赖**：对象区域质量损失需依赖预训练的感知模型生成物体掩码，其性能受限于感知模型本身的质量。若感知模型在特定场景（如极端光照、严重遮挡）下失效，掩码质量下降将直接影响损失的有效性。

4. **任务泛化未验证**：实验仅在自动驾驶交通场景重建和2D目标检测任务（YOLOv8、Faster R-CNN、RT-DETR）上验证。该方法对其他感知任务（如3D目标检测、语义分割、跟踪）以及机器人、AR/VR等领域的泛化能力尚未得到实证支持。

### 开放问题

1. **自适应权重策略**：能否开发自适应或学习式的λ权重调整机制，以在不同场景和任务需求下自动平衡视觉真实感与感知稳定性？

2. **训练效率优化**：能否通过知识蒸馏或替代训练方式（如离线预计算感知特征）避免在线感知模型推理，从而降低训练开销？

3. **多任务感知扩展**：感知对齐损失的设计是否可扩展至其他感知任务（如语义分割、实例分割、3D目标检测）？对于输出空间更复杂的任务，如何定义有效的感知差异度量？

4. **下游任务闭环验证**：感知稳定性的提升是否能够直接转化为下游规划或控制模块的性能增益？这需要端到端的闭环评估来验证。

5. **复杂场景鲁棒性**：在更复杂的动态场景（如高密度交通流、多智能体交互）和恶劣天气条件下，所提方法能否维持稳定的感知提升？这需要更多样化的场景覆盖测试。



## 原文 PDF

![[paperPDFs/ICLR_2026/Beyond_Visual_Reconstruction_Quality_Object_Perception_aware_3D_Gaussian_Splatting_for_Autonomous_Driving.pdf]]
