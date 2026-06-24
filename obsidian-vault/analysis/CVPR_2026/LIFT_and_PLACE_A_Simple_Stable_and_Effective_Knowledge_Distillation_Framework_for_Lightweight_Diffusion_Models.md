---
title: "LIFT and PLACE: A Simple, Stable, and Effective Knowledge Distillation Framework for Lightweight Diffusion Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/LIFT_and_PLACE_A_Simple_Stable_and_Effective_Knowledge_Distillation_Framework_for_Lightweight_Diffusion_Models.pdf
code_link: null
aliases:
- LP
- LPSSEKDFLDM
tags:
- CVPR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: LIFT and PLACE
primary_logic: LIFT and PLACE
claims:
- LIFT and PLACE
---

# LIFT and PLACE: A Simple, Stable, and Effective Knowledge Distillation Framework for Lightweight Diffusion Models

> [!tip] 核心洞察
> LIFT and PLACE

| 字段 | 内容 |
|------|------|
| 中文题名 | LIFT and PLACE: A Simple, Stable, and Effective Knowledge Distillation Framework for Lightweight Diffusion Models |
| 英文题名 | LIFT and PLACE: A Simple, Stable, and Effective Knowledge Distillation Framework for Lightweight Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.19729) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method |  |
| Dataset | CelebA, LSUN-Bedroom, ImageNet, MS-COCO |
## 概述

大规模扩散模型在图像生成任务中展现出卓越的性能，但其庞大的参数量和计算开销严重制约了在资源受限场景下的部署。通过知识蒸馏（Knowledge Distillation, KD）将教师模型的能力迁移至轻量级学生模型，是解决这一问题的直接路径。然而，当师生容量差距急剧扩大时，传统KD方法面临严峻挑战：学生性能显著退化，且训练过程高度不稳定。

本文针对这一瓶颈，提出了**LIFT**（**L**inear regression-based **I**nitialization for **F**ine-**T**uning）与**PLACE**（**P**artitioned **L**ocal **A**daptive **C**orrection **E**stimation）框架。其核心洞察在于，蒸馏误差可分解为两类性质迥异的成分：由低阶矩不匹配导致的**粗粒度-易优化**（Coarse-Easy）误差，以及由复杂分布差异构成的**细粒度-难优化**（Fine-Hard）误差。LIFT通过线性回归参数化KD目标，将粗粒度对齐转化为对回归系数的正则化约束，同时保留残差用于细粒度学习，从而在根本上缓解了容量差距带来的优化困难。PLACE则进一步将模型输出按误差大小分区，对每个分区独立应用LIFT，实现了空间自适应的局部精细化引导。

在极端压缩场景下（如仅保留教师模型1.6%参数的1.3M学生模型），传统OutKD方法完全失效（FID高达96.64），而本文方法在CelebA 64×64上取得了**15.73**的FID，性能提升逾80点。该框架在不同架构（UNet、DiT、MMDiT）、不同任务（无条件生成、文生图）及不同压缩策略（剪枝、深度缩减）下均展现出一致的稳定性和有效性，为轻量化扩散模型的训练提供了一种简单、稳定且高效的解决方案。

## 背景与动机

扩散模型已在图像生成（Dhariwal & Nichol, NeurIPS 2021）、文本到图像合成（Rombach et al., CVPR 2022）等任务中取得显著成果，但其庞大的参数量和推理成本严重阻碍了实际部署。知识蒸馏（Knowledge Distillation, KD）是压缩扩散模型的主流策略之一，其核心思想是让轻量学生网络模仿强大教师网络的输出或中间特征。

然而，现有KD方法在扩散模型压缩中面临两个根本性瓶颈：

**容量差距导致的不稳定性。** 当教师-学生容量差距增大时，传统输出级KD（OutKD）和特征级KD（FeatKD）的性能急剧下降且方差显著增大。如Figure 1所示，随着教师网络规模扩大，学生网络的平均FID恶化，同时多次运行的性能标准差持续攀升，表明蒸馏过程变得高度不稳定。在极端压缩场景下（例如将模型参数压缩至原来的1.6%），传统KD甚至不如直接微调（w/o KD），出现“负迁移”现象。

**空间非均匀误差被忽略。** 现有KD方法对所有空间位置施加均等的蒸馏约束，但扩散模型在不同空间区域的预测误差存在显著差异。Figure 3的误差图可视化表明，学生网络在物体边界、纹理复杂区域等位置产生更高的预测误差，而平坦背景区域的误差相对较小。均匀施加蒸馏损失会迫使学生在“容易”区域过度模仿教师，同时在“困难”区域缺乏足够的引导，导致蒸馏效率低下。

**OutKD与FeatKD的优化冲突。** 尽管同时使用OutKD和FeatKD直觉上应带来互补收益，但实验表明二者的直接组合往往导致收敛不稳定甚至性能倒退（Table 1中OutKD+FeatKD在多项设置下劣于单独微调）。这表明两种蒸馏信号在优化过程中存在冲突，需要更精细的协调机制。

基于上述观察，本文提出两个核心动机：第一，需要一种能够自适应分解蒸馏目标、缓解容量差距带来的不稳定性的方法；第二，需要一种能够感知空间误差分布、提供局部自适应引导的机制。这直接催生了LIFT（线性回归参数化蒸馏目标）和PLACE（基于误差分组的局部自适应修正）两个技术组件。

## 核心创新

本文的核心创新在于将扩散模型的知识蒸馏（KD）目标重新表述为**粗粒度对齐与细粒度精炼**的两阶段问题，并据此提出了 **LIFT** 与 **PLACE** 两个互补模块。与传统的输出级 KD（OutKD）或特征级 KD（FeatKD）直接最小化 $L_2$ 距离不同，该方法通过线性回归参数化蒸馏误差，显式解耦了低阶矩匹配与残差学习，从而在高压缩比场景下实现了稳定且显著的性能提升。

### 1. 蒸馏误差的分解：Coarse-Easy 与 Fine-Hard

通过对教师-学生输出进行逐样本线性回归分析（Figure 2），作者发现蒸馏误差可被分解为两类性质不同的成分：

- **Coarse-Easy 误差**：由教师与学生分布的低阶矩（均值、方差）不匹配引起，可通过简单的仿射变换 $\epsilon^{\mathcal{T}} \approx \beta_0 + \beta_1 \cdot \epsilon^{\mathcal{S}}$ 近似消除。该部分误差“容易”修正，但仅靠它无法恢复学生生成质量。
- **Fine-Hard 误差**：仿射校正后的残差，对应更复杂的分布差异，难以通过简单的参数化变换消除，需要学生网络进行更深层的表征学习。

这一分解是全文方法论的基础：它揭示了传统 OutKD 将两类误差混为一谈的缺陷，为后续的分离式训练提供了理论依据。

### 2. LIFT：参数化蒸馏与自适应精炼

**LIFT**（Linear regression-guided Fine-Tuning）将 KD 目标参数化为带约束的回归问题：

$$
\operatorname*{argmin}_{\theta^{\mathcal{S}}} \mathcal{D}(\epsilon^{\mathcal{T}}, \beta_0 + \beta_1 \epsilon^{\mathcal{S}}), \quad \mathrm{s.t.} \ \beta_0=0, \ \beta_1=1.
$$

其核心 changed slot 在于**用回归系数约束替代了直接的输出距离最小化**。具体实现包含两个损失项：

- **Coarse 损失**：$\mathcal{L}_{\mathrm{coarse}} = |\beta_0| + |\beta_1 - 1|$，强制学生输出的低阶矩与教师对齐，解决“Coarse-Easy”误差。
- **Fine 损失**：在回归约束下学习仿射校正后的残差 $\epsilon^{\mathcal{T}} - (\beta_0 + \beta_1 \epsilon^{\mathcal{S}})$，解决“Fine-Hard”误差。

为避免 Fine 损失在训练早期干扰特征学习，LIFT 引入**自适应权重** $w = 1 - \min(1, \mathcal{L}_{\mathrm{coarse}})$：当粗粒度对齐尚未完成（$\mathcal{L}_{\mathrm{coarse}}$ 较大）时，自动降低 Fine 损失的权重，优先稳定低阶矩匹配（Figure 6b）。

### 3. PLACE：空间非均匀误差的局部自适应

进一步分析表明，蒸馏误差在空间上具有显著的非均匀性（Figure 3）：边缘、纹理等高频区域的误差远大于平滑区域。全局共享的回归系数无法有效应对这种局部差异。

**PLACE**（Partition-based Locally Adaptive Correction for Errors）将模型输出按误差大小划分为 $K$ 个组 $\{G_i\}_{i=1}^{K}$，对每组独立估计回归系数 $\beta_{0,i}, \beta_{1,i}$ 并计算组内 LIFT 损失：

- 高误差组获得更强的校正信号，实现局部精细调整；
- 低误差组保持轻量约束，避免过拟合。

PLACE 与 LIFT 无缝集成，形成统一的 **LIFT+PLACE** 框架（Figure 4），其训练目标为：

$$
\mathcal{L} = \lambda_{diff} \mathcal{L}_{diff} + \lambda_{\mathrm{LIFT}} \mathcal{L}_{\mathrm{LIFT}} + \lambda_{\mathrm{FeatKD}} \mathcal{L}_{\mathrm{FeatKD}}.
$$

### 4. 关键 changed slots 总结

| 组件 | 传统 KD | 本文方法 | 作用机制 |
|------|---------|----------|----------|
| 输出级监督 | OutKD（直接 $L_2$） | LIFT（回归参数化 + 约束） | 解耦粗/细粒度误差，避免梯度冲突 |
| 误差处理 | 全局统一 | PLACE（误差分组局部自适应） | 处理空间非均匀误差 |
| 损失权重 | 固定超参 | 自适应权重 $w = 1 - \min(1, \mathcal{L}_{\mathrm{coarse}})$ | 动态平衡粗对齐与细精炼 |

### 5. 证据强度与注意事项

- **强证据**：Table 1 显示，在 CelebA 64×64 90% 剪枝率下，本文方法 FID 达 15.73，而 OutKD 为 96.64，OutKD+FeatKD 甚至劣于无 KD 的微调基线。该结果经过多次运行验证（Figure 1a 显示标准差），置信度 0.98。
- **跨任务验证**：方法在 LSUN-Bedroom 256×256（Table 1）、Stable Diffusion 2.1 / SD3 文生图（Table 2）、ImageNet DiT 类条件生成（Table 3）上均取得最优，表明 LIFT+PLACE 对扩散模型架构和任务具有通用性。
- **需注意的限制**：论文未提供在大规模文本-图像模型（如 SDXL、Flux）上的验证；PLACE 的分组数 $K$ 需作为超参调节，其敏感性未充分讨论。

## 整体框架

LIFT 与 PLACE 共同构成一个面向轻量化扩散模型的知识蒸馏框架，其核心设计思路是将传统输出级蒸馏损失分解为可独立调控的“粗粒度对齐”与“细粒度精修”两个子目标，从而在师生容量差距极大时仍能保持稳定收敛。框架的整体流程如图 4 所示，包含三个关键阶段：误差诊断、LIFT 参数化蒸馏、以及 PLACE 空间自适应增强。

**误差诊断与分解。** 框架首先通过线性回归分析师生输出之间的统计差异。对于给定时间步 $t$ 下的教师噪声预测 $\epsilon^{\mathcal{T}}$ 与学生噪声预测 $\epsilon^{\mathcal{S}}$，拟合线性模型 $\epsilon^{\mathcal{T}} \approx \beta_0 + \beta_1 \cdot \epsilon^{\mathcal{S}}$，其中回归系数由普通最小二乘（OLS）给出：$\beta_1 = \mathbf{Cov}[\epsilon^{\mathcal{T}}, \epsilon^{\mathcal{S}}] / \mathrm{Var}[\epsilon^{\mathcal{S}}]$，$\beta_0 = \mathbb{E}[\epsilon^{\mathcal{T}}] - \beta_1 \mathbb{E}[\epsilon^{\mathcal{S}}]$。该分析将蒸馏误差显式分解为两类：

- **“Coarse-Easy”误差**：低阶矩（均值、方差）层面的统计偏差，可通过仿射变换 $\beta_0 + \beta_1 \epsilon^{\mathcal{S}}$ 近似消除。
- **“Fine-Hard”误差**：残差 $\epsilon^{\mathcal{T}} - (\beta_0 + \beta_1 \epsilon^{\mathcal{S}})$ 中包含的复杂分布差异，无法由简单的线性校正捕获。

**LIFT：参数化蒸馏目标。** 基于上述分解，LIFT 将知识蒸馏目标重新参数化为一个带约束的优化问题：

$$\operatorname*{argmin}_{\theta^{\mathcal{S}}} \mathcal{D}(\epsilon^{\mathcal{T}}, \beta_0 + \beta_1 \epsilon^{\mathcal{S}}), \quad \mathrm{s.t.} \ \beta_0=0, \ \beta_1=1.$$

该约束强制学生输出在低阶矩层面与教师对齐（即“Coarse-Easy”部分），而残差部分则由自适应加权的细粒度损失负责学习。具体实现中，粗对齐损失定义为 $\mathcal{L}_{\mathrm{coarse}} = |\beta_0| + |\beta_1 - 1|$，细粒度损失则采用自适应权重 $w = 1 - \min(1, \mathcal{L}_{\mathrm{coarse}})$ 进行调制——当粗对齐尚未完成时，细粒度损失的权重被自动压低，避免过早的精细约束干扰特征级蒸馏（FeatKD）的收敛。

**PLACE：空间自适应分组。** 实验观察表明，蒸馏误差在空间上呈现显著的非均匀分布（Figure 3, Figure 9）：某些区域（如背景、纹理丰富区）的误差远高于其他区域。PLACE 针对这一现象，将模型输出按误差大小划分为 $K$ 个组 $\{G_1, \dots, G_K\}$，对每个组独立估计回归系数 $\beta_{0,i}, \beta_{1,i}$ 并计算组内 LIFT 损失。这使得框架能够为不同空间区域提供局部自适应的蒸馏指导，进一步缓解大容量差距下的性能退化。

**训练目标。** 完整的训练损失为三项的加权和：

$$\mathcal{L} = \lambda_{diff} \mathcal{L}_{diff} + \lambda_{\mathrm{LIFT}} \mathcal{L}_{\mathrm{LIFT}} + \lambda_{\mathrm{FeatKD}} \mathcal{L}_{\mathrm{FeatKD}},$$

其中 $\mathcal{L}_{diff} = ||\epsilon^{\mathcal{T}} - \epsilon^{\mathcal{S}}||_2^2$ 为标准扩散损失，$\mathcal{L}_{\mathrm{LIFT}}$ 为上述参数化蒸馏损失，$\mathcal{L}_{\mathrm{FeatKD}}$ 为经过维度对齐后的中间特征 L2 损失。该框架可无缝替换现有蒸馏方法中的 OutKD 损失（如 **TinyFusion** 的蒸馏管线），仅需将输出级损失替换为 LIFT 与 PLACE，其余模块（如掩码表示损失）保持不变。

**适用场景。** 该框架已在像素空间扩散模型（CelebA 64×64、LSUN Bedroom 256×256）、文本到图像扩散模型（Stable Diffusion v2.1、Stable Diffusion 3-Medium）以及 ImageNet 类条件 DiT 上得到验证，覆盖 U-Net 与 MMDiT 两种主流架构，在 30% 至 90% 的剪枝率范围内均表现出稳定的收敛性和一致的性能提升。

### 补充图表

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/004_Figure_4.jpg]]
*Figure 4: Overview of LIFT and PLACE. LIFT parameterizes KD via linear regression, regularizing*

## 核心模块与公式推导

### 3.1 蒸馏误差分解：Coarse-Easy 与 Fine-Hard

LIFT 的核心洞察来源于对教师-学生输出差异的回归分析。对于每个去噪时间步 $t$，将教师噪声预测 $\epsilon^{\mathcal{T}}$ 对学生噪声预测 $\epsilon^{\mathcal{S}}$ 做线性回归：

$$\epsilon^{\mathcal{T}} \approx \beta_0 + \beta_1 \cdot \epsilon^{\mathcal{S}}$$

其中回归系数由普通最小二乘（OLS）给出：

$$\beta_1 = \mathbf{Cov}[\epsilon^{\mathcal{T}}, \epsilon^{\mathcal{S}}] / \mathrm{Var}[\epsilon^{\mathcal{S}}], \quad \beta_0 = \mathbb{E}[\epsilon^{\mathcal{T}}] - \beta_1 \mathbb{E}[\epsilon^{\mathcal{S}}]$$

该分解将蒸馏误差划分为两类（见 Figure 2 的回归校正分析）：

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/003_Figure_2.jpg]]
*Figure 2: Regression-based correction analysis. At each time step t, we estimate regression coefficients from teacher-student pairs and affine-correct the student output, following Alg. 1. Qualitative samples are shown below. Left: student; middle: corrected as in Alg. 1; right: teacher. The corrected sampler yields more faithful images. However, a performance gap between the corrected output and the teacher remains, especially for fine and hard details*

1. **Coarse-Easy 误差**：由低阶矩（均值、方差）的不匹配造成，可通过仿射变换 $\beta_0 + \beta_1 \epsilon^{\mathcal{S}}$ 近似消除。
2. **Fine-Hard 误差**：回归校正后的残差，反映学生无法通过简单线性变换匹配的复杂分布差异。

这一分解构成了 LIFT 框架的理论基础——先对齐低阶统计量（Coarse），再学习残差（Fine）。

### 3.2 LIFT：参数化知识蒸馏目标

LIFT 将上述分解转化为可优化的训练目标。核心思想是将回归系数 $(\beta_0, \beta_1)$ 推向恒等映射 $(0, 1)$，从而使学生的输出分布直接逼近教师。

**约束优化形式：**

$$\operatorname*{argmin}_{\theta^{\mathcal{S}}} \mathcal{D}(\epsilon^{\mathcal{T}}, \beta_0 + \beta_1 \epsilon^{\mathcal{S}}), \quad \mathrm{s.t.} \ \beta_0 = 0, \ \beta_1 = 1.$$

**Coarse 损失（低阶矩对齐正则项）：**

$$\mathcal{L}_{\mathrm{coarse}} = |\beta_0| + |\beta_1 - 1|$$

该损失直接惩罚回归系数对恒等映射的偏离，驱动学生匹配教师的均值和方差结构。

**Fine 损失（残差学习）：** 在 Coarse 对齐的基础上，对回归残差施加额外的距离度量，使学生进一步学习 Fine-Hard 误差。

**自适应权重：** 为避免 Fine 损失在训练早期干扰 Coarse 对齐或与特征蒸馏（FeatKD）冲突，LIFT 引入自适应权重：

$$w = 1 - \min(1, \mathcal{L}_{\mathrm{coarse}})$$

当 $\mathcal{L}_{\mathrm{coarse}}$ 较大（低阶矩尚未对齐）时，$w$ 自动降低 Fine 损失的权重，优先完成粗粒度对齐；随着训练推进，权重逐渐恢复，使模型专注于精细修正（见 Figure 6(b) 的权重动态分析）。

### 3.3 PLACE：空间非均匀误差的分组自适应蒸馏

Figure 3 揭示了蒸馏误差在空间上高度非均匀——某些区域（如物体边缘、纹理复杂区）的误差远大于平滑区域。单一的全局回归系数 $(\beta_0, \beta_1)$ 无法捕捉这种局部差异。

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/002_Figure_3.jpg]]
*Figure 3: Visualization of (a) input image, latent error map*

PLACE 将模型输出按误差大小划分为 $K$ 个组 $\{G_i\}_{i=1}^K$，对每个组独立估计回归系数：

$$\beta_{0,i}, \beta_{1,i} = \text{OLS}(\epsilon^{\mathcal{T}}, \epsilon^{\mathcal{S}} \mid G_i)$$

并在每个组内计算独立的 LIFT 损失（含 Coarse 和 Fine 项）。这等价于在不同空间区域施加不同强度的蒸馏约束，实现**局部自适应引导**。实验表明 $K=16$ 时在 CelebA 64×64 上取得最优效果。

### 3.4 完整训练目标

最终的蒸馏损失为三项的加权和：

$$\mathcal{L} = \lambda_{diff} \mathcal{L}_{diff} + \lambda_{\mathrm{LIFT}} \mathcal{L}_{\mathrm{LIFT}} + \lambda_{\mathrm{FeatKD}} \mathcal{L}_{\mathrm{FeatKD}}$$

其中：

- **扩散损失** $\mathcal{L}_{diff} = ||\epsilon^{\mathcal{T}} - \epsilon^{\mathcal{S}}||_2^2$：教师-学生输出的直接 L2 距离。
- **LIFT 损失** $\mathcal{L}_{\mathrm{LIFT}}$：包含 Coarse 正则项与自适应加权的 Fine 残差项（PLACE 中为分组聚合形式）。
- **特征蒸馏损失** $\mathcal{L}_{\mathrm{FeatKD}}$：教师与学生中间特征的 L2 距离（经维度对齐）。

## 实验与分析

### 主实验结果

#### 图像空间扩散模型：CelebA 与 LSUN-Bedroom

Table 1 汇总了在 CelebA 64×64 和 LSUN-Bedroom 256×256 上不同学生容量与剪枝率下的 FID、Precision、Recall。核心发现如下：

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/005_Table_1.jpg]]
*Table 1: Quantitative results of CelebA and LSUN-Bedroom image space diffusion. Each row grouped by student size. OutKD+FeatKD often underperform fine-tuning (w/o KD), while our method achieves the best performance and convergence at a pruning ratio 90%. On the challenging high-resolution LSUN-Bedroom, ours at a pruning ratio 70% even outperforms OutKD+FeatKD at a pruning ratio 50%*

- **极端压缩场景（90% 剪枝，学生仅 1.3M 参数，约为教师的 1.6%）**：传统 OutKD 完全失效（FID 96.64），OutKD+FeatKD 亦不稳定；本文方法（K=16 的 PLACE 配置）取得 **FID 15.73**，Precision 0.690，Recall 0.366，较 OutKD 降低 **80.91**。
- **中等剪枝（50%/70%）**：本文方法在 CelebA 上分别达到 FID 4.93 和 5.97，显著优于所有基线。
- **LSUN-Bedroom 256×256（70% 剪枝）**：本文方法取得 FID 37.96，Precision 0.326，Recall 0.470，同样优于 OutKD 及 OutKD+FeatKD。
- **关键趋势**：随着教师-学生容量差距增大，OutKD 及 OutKD+FeatKD 的性能均值恶化、方差增大；本文方法在各容量差距下均保持最低 FID 均值与最小方差，收敛最稳定。

#### 文本到图像扩散模型：Stable Diffusion 2.1 与 SD 3

Table 2 展示了在 SD 2.1（UNet 架构）和 SD 3（MMDiT 架构，flow matching 训练）上的剪枝蒸馏结果：

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/006_Table_2.jpg]]
*Table 2: Quantitative results on text-to-image diffusion models, evaluating both Stable Diffusion v2.1 (SD 2.1) and Stable Diffusion 3- Medium (SD 3). SD 3 employs an MMDiT architecture trained via flow matching, where D denotes the model depth, and its student is initialized via ShortGPT [23]. MACs and Params are measured excluding the VAE and text encoders. Ours replaces only OutKD with LIFT and PLACE. † indicates that FID, IS, and CLIP are reported from [13]*

- 本文方法在 SD 2.1 和 SD 3 上均取得最优 FID 与 CLIP Score，且定性结果（Figure 5）显示对提示语义的遵循更好。
- 在 SD 3 的 MMDiT 架构上，本文仅替换 OutKD 损失为 LIFT 和 PLACE，保留 mask-representation 损失，即插即用地提升了蒸馏质量。

#### ImageNet 类别条件 DiT

Table 3 报告了在 DiT 架构上的结果。以 TinyFusion 为基线（使用 OutKD + mask-representation KD），本文将其中的 OutKD 替换为 LIFT 和 PLACE：

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/008_Table_3.jpg]]
*Table 3: Quantitative results on ImageNet class-conditioned DiT. Where D in architecture is depth. TinyFusion [6] applied block-pruning and finetuned with OutKD and masked-representation KD loss. Our model replaces OutKD loss with LIFT and PLACE, keeping the masked-representation loss. † indicates that FID, IS, Precision and Recall are reported in [6]*

- 在 DiT-D7 学生上，本文方法 FID 显著优于 TinyFusion。
- Table 7 进一步表明：更大的教师容量对 TinyFusion 造成 FID 恶化，而本文方法在更强教师下持续受益，与像素空间扩散观察一致。

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/014_Table_7.jpg]]
*Table 7: Effects of teacher capacity in DiT. We compare the TinyFusion baseline with our method when distilling a DiT-D7 student from two teachers of different capacities. As in pixel-space diffusion, larger teachers degrade FID for TinyFusion, whereas our LIFT and PLACE provide consistent improvements, with a slightly larger gain when distilling from the stronger teacher. Bold indicates the best performance for each teacher used in distillation, and † denotes metrics reported in [6]*

### 消融实验

#### LIFT 与 PLACE 的组件贡献

Table 8 对完整目标函数（Eq. (8)）的各组件进行消融，所有学生均从最强的 78.7M 教师蒸馏：

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/016_Table_8.jpg]]
*Table 8: Ablation study on the components of Eq. (8). All of student models distilled from the strongest 78.7M-teacher*

- 移除 Coarse 损失（仅保留 Fine-Hard 项）导致 FID 明显上升，验证了低阶矩对齐的必要性。
- 移除 PLACE 的分组机制（即仅使用全局 LIFT）在空间非均匀误差大的场景下性能下降，证实了局部自适应精炼的价值。
- 同时使用 Coarse + Fine-Hard + PLACE 分组取得最优 FID。

#### 教师容量的影响

Table 5 与 Table 6 固定学生容量（1.3M，90% 剪枝），变化教师容量：

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/011_Table_5.jpg]]
*Table 5: Effect of teacher capacity. (90% pruned student for CelebA). Conventional KD fails to converge or yields suboptimal results. In contrast, our method achieves the best performance and most stable convergence with the strongest teacher*

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/013_Table_6.jpg]]
*Table 6: All of the above models use a fixed size of the student model (1.3M). For OutKD and OutKD+FeatKD, larger teachers result in higher FID means and larger FID variances. When distilled from the strongest teacher, LIFT and PLACE achieve the lowest FID mean and standard deviation. Values in bold correspond to those reported in Tab. 1*

- OutKD 和 OutKD+FeatKD 在更大教师下 FID 均值升高、方差增大，表现出“容量差距诅咒”。
- 本文方法从更强教师中稳定获益：最强教师下 FID 均值最低、方差最小，表明 LIFT 和 PLACE 有效解耦了容量差距带来的优化困难。

Table 7 在 DiT 上重复该实验，结论一致：更大教师对 TinyFusion 有害，对本文方法有益。

#### 自适应权重调度器

Table 4 比较了不同权重调度策略对 FID 的影响。本文采用基于 Coarse 损失的自适应权重 $w = 1 - \min(1, \mathcal{L}_{\mathrm{coarse}})$（见 part_006），该策略在训练过程中动态抑制 Fine-Hard 精炼对 FeatKD 的干扰：

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/010_Table_4.jpg]]
*Table 4: FID comparison under different w schedulers. where i and I denote the current and total training iterations. All of student models distilled from the strongest 78.7M-teacher*

- 固定权重或简单线性调度均不如自适应调度。
- Figure 6(b) 展示了自适应权重随训练进程的变化曲线，验证了其“粗对齐优先、细精炼逐步介入”的行为。

![[assets/figures/papers/paper_list_l894_https_arxiv_org_abs_2605_19729/figures/009_Figure_6.jpg]]
*Figure 6: (a) Numerical labels indicate FID at each iteration. Decreasing of gradient norm demonstrates stable convergence of our method. (b) We compare our adaptive weight*

### 收敛性分析

Figure 6(a) 展示了扩散损失梯度范数的收敛曲线。本文方法的梯度范数下降更平滑、终值更低，与 OutKD 的剧烈震荡形成对比。自适应权重机制（Figure 6(b)）在训练早期保持较低的精炼强度，避免了大梯度冲突，是收敛稳定的关键因素。

### 失败模式与局限性

- **极限容量差距下的残留误差**：尽管本文方法在 90% 剪枝的 1.3M 学生上取得 FID 15.73，但与教师（FID 约 2-3）仍有显著差距。Figure 3 的空间误差图显示，即使训练后期，某些空间区域仍存在集中的残留误差，PLACE 的分组策略可缓解但无法完全消除。
- **分组数 K 的敏感度**：Table 1 中 K=16 为默认配置，但论文未系统报告 K 的鲁棒性范围。极端 K 值（过小导致分组粗糙，过大导致每组样本不足）可能影响性能，需手动验证。
- **Flow Matching 架构的适配深度**：SD 3 的 MMDiT 架构上仅替换了输出级损失，未探索特征级 LIFT/PLACE 的扩展，可能留下额外增益空间。
- **计算开销**：PLACE 需对每组分别估计回归系数并计算组级损失，K 增大时训练开销线性增长，论文未提供详细的训练时间对比。

### 重要图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Table 1 | 极端压缩下本文方法大幅优于 OutKD（FID 15.73 vs 96.64）；中等剪枝亦全面领先 |
| Table 2 | 文本到图像扩散模型上即插即用，跨架构有效 |
| Table 5/6/7 | 本文方法是唯一从更强教师中稳定获益的 KD 方法 |
| Table 8 | Coarse 损失与 PLACE 分组缺一不可 |
| Figure 6 | 自适应权重实现平滑收敛，避免梯度冲突 |
| Figure 3 | 空间非均匀误差客观存在，PLACE 可缓解但未根除 |

## 方法谱系与知识库定位

### 蒸馏范式定位：从输出对齐到结构化误差分解

本工作 LIFT and PLACE 处于扩散模型知识蒸馏（Knowledge Distillation for Diffusion Models）这一研究脉络中，其核心贡献在于将传统的输出级蒸馏（Output KD）重新参数化为“粗对齐 + 细精炼”的结构化误差分解框架。

**传统基线方法**包括两类主流范式：
- **输出级蒸馏（OutKD）**：直接最小化教师与学生去噪输出之间的 L2 距离，即 $\mathcal{L}_{\mathrm{OutKD}} = \mathbb{E}_{\boldsymbol{x},t} [|| \epsilon^{\mathcal{T}} - \epsilon^{\mathcal{S}} ||_2^2]$。该范式在师生容量差距较小时有效，但在极端压缩场景下（如 90% 剪枝率）会严重退化——论文在 **Table 1** 中报告 OutKD 在 CelebA 64×64 上仅取得 FID 96.64，甚至不如无 KD 的微调基线。
- **特征级蒸馏（FeatKD）**：在中间特征层进行对齐，通过维度适配后最小化 L2 距离。论文将其作为辅助损失保留在最终目标中。

**LIFT 的关键突破**在于对 OutKD 目标的重新参数化：通过逐样本线性回归 $\epsilon^{\mathcal{T}} \approx \beta_0 + \beta_1 \cdot \epsilon^{\mathcal{S}}$，将蒸馏误差显式分解为：
- **Coarse-Easy 误差**：由低阶矩不匹配（$\beta_0 \neq 0$ 或 $\beta_1 \neq 1$）引起的统计偏差；
- **Fine-Hard 误差**：线性回归残差中剩余的复杂分布差异。

基于此分解，LIFT 构建了约束优化目标 $\operatorname{argmin} \mathcal{D}(\epsilon^{\mathcal{T}}, \beta_0 + \beta_1 \epsilon^{\mathcal{S}})$，s.t. $\beta_0=0, \beta_1=1$，并引入粗对齐正则项 $\mathcal{L}_{\mathrm{coarse}} = |\beta_0| + |\beta_1 - 1|$ 来显式驱动低阶矩对齐。这一设计将原本黑箱的 L2 匹配转化为可解释的“先对齐统计矩，再精炼残差”的两阶段过程。

**PLACE** 进一步将 LIFT 推广到空间非均匀误差场景：通过将模型输出按误差大小划分为 $K$ 个分组，对每组独立估计回归系数 $\beta_{0,i}, \beta_{1,i}$ 并施加组级 LIFT 损失，实现局部自适应的蒸馏引导。

### 与相关工作的关系

**与 TinyFusion 的集成**：在 ImageNet 类条件 DiT 实验中（**Table 3**），本方法直接替换 TinyFusion 中的 OutKD 损失，保留其掩码表示蒸馏损失，验证了 LIFT/PLACE 可作为即插即用的 OutKD 替代方案，与现有剪枝-蒸馏流程兼容。

**与特征蒸馏的协同**：论文在 **Table 1** 中显示，单独的 OutKD+FeatKD 组合在极端剪枝下甚至劣于无 KD 微调，而 LIFT/PLACE 通过自适应权重 $w = 1 - \min(1, \mathcal{L}_{\mathrm{coarse}})$ 动态降低细精炼强度，避免与 FeatKD 产生干扰，从而在 CelebA 50% 和 70% 剪枝率下分别取得 FID 4.93 和 5.97。

**与 Stable Diffusion 系列的适配**：方法在 Stable Diffusion v2.1 和 Stable Diffusion 3-Medium（MMDiT 架构，Flow Matching 训练）上均得到验证（**Table 2**），表明 LIFT/PLACE 对 UNet 和 DiT 架构、噪声预测与流匹配训练范式均具有通用性。

### 适用边界与局限

**已验证的适用场景**：
- 图像空间扩散模型：CelebA 64×64、LSUN Bedroom 256×256
- 文本到图像扩散模型：Stable Diffusion v2.1、SD 3-Medium
- 类条件 DiT：ImageNet
- 剪枝率范围：30%–90%
- 学生参数量低至 1.3M（教师容量的 1.6%）

**已知局限与开放问题**：
1. **分组数 $K$ 的敏感性**：PLACE 的分组数 $K$ 是超参数，论文在 Table 1 中报告了 $K=16$ 的结果，但未系统分析 $K$ 的选择对性能的影响规律。该参数的最优值可能依赖于师生容量差距和任务复杂度，需手动验证。
2. **线性回归假设的边界**：LIFT 的核心假设是低阶矩对齐可通过线性回归近似。当师生分布差异高度非线性时（例如架构族差异极大），该假设的保真度需要进一步检验。
3. **潜在空间扩散模型的验证缺失**：论文主要在图像空间扩散模型上实验，对潜在扩散模型（如 SD 的 VAE 潜在空间）的蒸馏效果仅通过 SD 系列间接体现，未与专门针对潜在空间设计的蒸馏方法进行对比。
4. **推理效率的讨论不足**：论文聚焦于蒸馏后的生成质量（FID、Precision、Recall），未报告蒸馏学生的推理延迟或吞吐量增益，这对于实际部署场景的评估至关重要。
5. **更大规模模型的极限压缩**：虽然已在 SD 3-Medium 上验证，但对于更大规模的模型（如 SDXL、Flux 等）在更高压缩比下的表现仍是开放问题。

### 知识库定位

本工作可定位于**扩散模型压缩与加速**方向下的**知识蒸馏子领域**，具体贡献属于**蒸馏目标函数设计**这一技术路线。与传统 OutKD 和 FeatKD 形成互补而非替代关系——论文的最终目标函数仍保留扩散损失和 FeatKD 损失，LIFT/PLACE 替代的是 OutKD 的角色。这一设计哲学与近年将传统 KD 损失重新参数化以提高蒸馏效率的趋势一致，其通过统计矩显式对齐实现稳定收敛的思路，为极端压缩场景下的扩散模型蒸馏提供了新的基线。

## 原文 PDF

![[paperPDFs/CVPR_2026/LIFT_and_PLACE_A_Simple_Stable_and_Effective_Knowledge_Distillation_Framework_for_Lightweight_Diffusion_Models.pdf]]