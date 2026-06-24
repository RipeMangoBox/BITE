---
title: "WildPose: A Unified Framework for Robust Pose Estimation in the Wild"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/WildPose_A_Unified_Framework_for_Robust_Pose_Estimation_in_the_Wild.pdf
code_link: null
aliases:
- WildPose
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将冻结的预训练MASt3R主干网络作为3D感知特征提取器，并设计专用的高容量运动掩码检测器，利用多层特征生成逐边运动掩码，在可微BA中动态降权动态像素的残差。
primary_logic: 融合前馈模型的丰富感知前端（MASt3R）与可微BA的端到端优化后端，通过逐边运动掩码消除时间歧义，实现动态与静态环境统一的鲁棒姿态估计。
claims:
- 在Wild-SLAM MoCap数据集上，WildPose在所有序列上均取得最低ATE RMSE，平均0.39 cm，显著优于MegaSaM（2.40 cm）和WildGS-SLAM（0.46 cm）。
- 在Bonn RGB-D Dynamic和TUM动态数据集上，WildPose同样取得最优或次优结果，平均ATE分别为2.36 cm和1.57 cm。
- 在静态TUM和7-Scenes数据集上，WildPose保持领先，全轨迹ATE分别为0.027 m和0.049 m，优于DROID-SLAM等静态方法。
- 消融实验验证了混合微调、运动掩码检测器和全局BA深度正则化关闭三个组件的有效性，完整模型在所有数据集上达到最佳性能。
---

# WildPose: A Unified Framework for Robust Pose Estimation in the Wild

> [!tip] 核心洞察
> 融合前馈模型的丰富感知前端（MASt3R）与可微BA的端到端优化后端，通过逐边运动掩码消除时间歧义，实现动态与静态环境统一的鲁棒姿态估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | WildPose：面向野外鲁棒姿态估计的统一框架 |
| 英文题名 | WildPose: A Unified Framework for Robust Pose Estimation in the Wild |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.12774) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | WildPose |
| Dataset | Wild-SLAM MoCap, Bonn RGB-D Dynamic, TUM RGB-D, 7-Scenes |

> [!tip] 效果简介
> - Wild-SLAM MoCap 上，ATE RMSE (cm) 0.39 (avg) vs WildGS-SLAM 0.46; MegaSaM 2.40 (↓ 0.07 cm (vs next best dynamic))。
> - Bonn RGB-D Dynamic 上，ATE RMSE (cm) 2.36 (avg) vs WildGS-SLAM 2.31; DROID-SLAM 4.91 (接近最优，优于动态学习方法)。
> - TUM RGB-D (dynamic) 上，ATE RMSE (cm) 1.57 (avg) vs ViPE 1.58; DROID-SLAM 2.25 (↓ 0.01 cm (略优))。

## 概述

**问题背景与瓶颈**：在动态场景中进行鲁棒的相机姿态估计，核心瓶颈在于现有方法难以准确识别动态区域——基于语义分割的方法依赖预定义类别，无法覆盖所有运动物体；基于运动预测的方法容量不足，难以建模复杂运动模式。动态像素的误匹配直接导致光束平差法（Bundle Adjustment, BA）优化失败，而引入动态处理机制的方法又常在静态场景中性能退化。因此，如何统一处理动态与静态环境，成为该领域的核心挑战。

**核心洞察**：WildPose 的关键思路是将现代三维视觉中两种强大范式进行融合——前馈模型（如 MASt3R）提供的丰富三维感知前端，与可微 BA 的端到端优化后端。通过引入逐边运动掩码来消除时间歧义，WildPose 实现了动态与静态环境下统一的鲁棒姿态估计。

**方法定位**：WildPose 以 DROID-SLAM（Teed et al., RSS 2021）的可微 BA 流水线为基础，进行了三个关键改造：(1) 将简单的 CNN 编码器替换为冻结的预训练 MASt3R ViT 编码器，辅以轻量适配器，注入三维感知先验；(2) 设计高容量运动掩码检测器，利用 MASt3R 多层特征生成逐边运动掩码，替代传统逐帧掩码，精细识别动态残差；(3) 采用多阶段课程训练策略（静态预训练 → 动静混合微调 → 运动检测器专项训练），并引入度量深度先验作为局部 BA 正则化项。在方法谱系上，WildPose 区别于纯前馈方法（VGGT、π3）、纯动态 SLAM 方法（WildGS-SLAM, Zheng et al., CVPR 2025；MegaSaM；ViPE）以及前馈+SLAM 方法（MASt3R-SLAM, Dusmanu et al., arXiv 2024），通过“冻结基础模型 + 可学习运动掩码 + 可微 BA”的架构，在动态与静态场景间实现了统一的高性能。

**主要结果概览**：在动态基准 Wild-SLAM MoCap 上，WildPose 平均 ATE RMSE 为 0.39 cm，显著优于 MegaSaM（2.40 cm）和 WildGS-SLAM（0.46 cm）；在 Bonn RGB-D Dynamic 和 TUM 动态数据集上同样取得最优或次优结果（平均 ATE 分别为 2.36 cm 和 1.57 cm）。更重要的是，在静态 TUM 和 7-Scenes 数据集上，WildPose 保持领先（全轨迹 ATE 分别为 0.027 m 和 0.049 m），优于 DROID-SLAM 等静态方法，验证了其“动态鲁棒、静态不退步”的统一能力。消融实验证实，混合微调、运动掩码检测器和全局 BA 深度正则化关闭三个组件均为有效设计。

## 背景与动机

单目视觉姿态估计是三维视觉与机器人导航的核心任务。近年来，基于学习的SLAM方法在静态场景中取得了显著进展，然而，当场景中出现动态物体时，这些方法的性能会急剧退化。根本原因在于，动态区域产生的光流违反了静态场景假设，导致可微BA（Bundle Adjustment）中的重投影误差被异常值污染，最终使优化陷入局部极小或发散。

现有处理动态场景的方法大致分为两类，但均存在明显缺口。第一类方法依赖**语义分割**来识别并剔除动态区域（如**ViPE**），但这需要预先指定动态语义类别，无法覆盖所有潜在运动物体（例如推车、被移动的箱子），且语义模型本身在域外场景中容易失效。第二类方法尝试**学习运动估计**或**在线训练不确定性模型**（如**MegaSaM**、**WildGS-SLAM** (Zheng et al., CVPR 2025)），但它们或受限于低容量的运动预测器，或在静态场景中性能显著退化——WildGS-SLAM在静态基准上的表现远逊于**DROID-SLAM** (Teed et al., RSS 2021)，暴露了“动态与静态不可兼得”的困境。

更深层的瓶颈在于：现有方法的感知前端与优化后端是割裂的。DROID-SLAM使用简单的CNN编码器，缺乏对三维几何的深层理解；而前馈模型（如**MASt3R-SLAM** (Dusmanu et al., arXiv 2024)、**VGGT**）虽具备强大的3D感知能力，却放弃了可微BA的端到端优化优势，难以在长序列中保持全局一致性。

本文的动机正是弥合这一鸿沟：**将前馈模型的丰富感知前端与可微BA的端到端优化后端融合，构建一个在动态与静态环境中统一鲁棒的单目姿态估计框架**。核心思想是利用冻结的预训练MASt3R编码器提供3D感知特征，并设计专用的高容量运动掩码检测器来识别动态区域，通过逐边运动掩码在BA中动态降权动态像素的残差，从而消除时间歧义，实现动态与静态环境的统一处理。

## 核心创新

WildPose 的核心创新在于将现代三维视觉中两个强大范式——前馈模型的丰富感知前端与可微BA的端到端优化后端——进行深度融合，从而构建一个在动态与静态环境下均能鲁棒工作的统一单目姿态估计框架。这一融合并非简单拼接，而是通过三个关键“changed slots”实现系统性的能力跃升。

### 从简单CNN到3D感知特征编码器

WildPose 将 DROID-SLAM 中原有的简单 CNN 编码器替换为**冻结的预训练 MASt3R ViT 编码器**，并辅以轻量适配器模块。MASt3R 作为经过大规模数据预训练的前馈模型，其内部特征蕴含丰富的三维几何先验，能够为下游的更新算子和运动检测提供更强的感知基础。适配器由两层卷积残差块构成，负责将 ViT 输出的 patch 级特征转换为 ConvGRU 可处理的 1/8 分辨率特征图。这一替换的因果逻辑在于：动态场景中的误匹配往往源于对三维结构的理解不足，而 MASt3R 的 3D 感知特征恰好弥补了这一短板。

### 从无运动检测到高容量逐边运动掩码

DROID-SLAM 等静态 SLAM 方法缺乏专用运动检测机制，在动态场景中会将运动物体的位移误认为相机运动，导致 BA 优化被动态像素的残差“拉偏”。WildPose 引入了**高容量运动掩码检测器**，利用 MASt3R 编码器的多层特征，为帧图中的每条边预测一个运动掩码。与现有方法（如 WildGS-SLAM、ViPE）的帧级掩码不同，逐边掩码能够捕捉运动相对于第二帧的时序歧义：同一像素在帧 $i \rightarrow j$ 和 $i \rightarrow k$ 两条边上可能具有不同的运动状态。这一设计使得运动检测不再依赖脆弱的语义分割或低容量运动预测器，而是从 3D 感知特征中直接学习运动模式。

### 从静态训练到动静混合课程学习

WildPose 采用三阶段课程训练策略，将训练数据从纯静态扩展到动静混合，并利用 Kubric 合成数据生成多样化的运动模式。第一阶段在静态数据上预训练更新算子；第二阶段混合动静数据微调，使模型适应动态场景；第三阶段冻结更新算子，单独训练运动掩码检测器。这一策略的关键在于：**混合微调**使更新算子学会在动态像素存在时仍能输出可靠的流估计，而**运动掩码检测器**则通过端到端耦合 BA 层进行训练，直接以姿态精度和掩码质量为导向优化。

### 从无尺度到度量深度先验

DROID-SLAM 作为单目方法缺乏度量尺度，而 WildPose 利用 Moge2 度量深度初始化视差，并将其作为局部 BA 的正则化项。在推理阶段，BA 目标函数中的权重矩阵由流置信度与运动掩码的乘积构成 $\text{diag}(\hat{\mathbf{w}} \odot \mathbf{M})$，从而动态降低动态像素残差的权重。在最终全局 BA 中，深度正则化项被显式移除，以避免 Moge2 深度先验中的噪声对全局一致性造成干扰。这一“先用后弃”的策略在消融实验中得到了验证：关闭全局 BA 深度正则化（GBA Dep. Off）可进一步提升精度。

## 整体框架

WildPose 是一个面向单目 RGB 视频的鲁棒姿态估计统一框架，其核心设计哲学在于融合**前馈模型的丰富感知前端**与**可微 BA 的端到端优化后端**。如 Figure 2 所示，系统以一段标定好的单目视频序列为输入，输出全局一致的相机轨迹。整个流水线由四个关键模块串联而成：冻结的 MASt3R 编码器提取 3D 感知特征，更新算子（ConvGRU + 轻量适配器）迭代预测光流与置信度，运动掩码检测器生成逐边运动掩码，可微 BA 层联合优化所有关键帧的姿态与视差。

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/002_Figure_2.jpg]]
*Figure 2: System Overview. WildPose robustly estimates the camera trajectory from a monocular RGB sequence. We leverage 3D-aware features from the frozen MASt3R encoder [25], which are fed into our update operator . Concurrently, a motion mask detector generates motion masks from the backbone’s multi-layer features. These outputs, combined with the metric depth prior [48], enable our Dense Bundle Adjustment layer to mitigate dynamic outliers and perform robust trajectory optimization*

**输入与输出流**：系统以在线视觉里程计模式运行。当新帧到来时，若其相对最近关键帧的运动量超过阈值，则被指定为新关键帧。对于每个新关键帧，其视差由度量深度先验（Moge2）初始化，随后进入局部 BA 窗口与相邻关键帧联合优化。系统周期性地对所有关键帧执行全局 BA 以保证长序列一致性，并在序列结束时进行一次最终全局 BA 作为后处理。最终输出为所有关键帧的相机姿态和场景视差。

**模块间的协作机制**是理解 WildPose 的关键。MASt3R 编码器（冻结）为后续所有模块提供 3D 感知的多层图像特征——这些特征既通过轻量适配器送入 ConvGRU 更新算子用于预测光流与置信度，又并行地送入运动掩码检测器以生成逐边运动掩码。更新算子迭代输出的光流 $\\hat{\\mathbf{f}}_{ij}$、置信度 $\\hat{\\mathbf{w}}_{ij}$ 和阻尼因子 $\\hat{\\eta}$ 共同构成可微 BA 的输入，而运动掩码检测器输出的逐边掩码 $M_{ij}$ 则与置信度相乘（$\\text{diag}(\\hat{\\mathbf{w}} \\odot M)$）作为 BA 残差的权重矩阵，从而在优化过程中动态降权动态像素的重投影误差。这种“检测-降权”机制使得 BA 优化能够自动忽略动态物体带来的误匹配，而无需依赖脆弱的语义分割或低容量运动预测。

**推理阶段的 BA 目标函数**完整体现了上述协作：

$$E(\\hat{\\omega}, \\hat{d}) = \\sum_{(i,j)\\in G} \\left\\| \\hat{\\mathbf{f}}_{ij} - \\tilde{\\mathbf{f}}_{ij} \\right\\|_{\\bar{\\Sigma}_{ij}}^2 + \\lambda \\sum_{i\\in G} \\left\\| (\\hat{d}_i - 1/D_i) \\right\\|^2$$

其中第一项为运动掩码加权的重投影误差，第二项为度量深度正则化项。值得注意的是，在最终的全局 BA 中，深度正则化项被移除，以减少深度先验噪声对全局一致性的干扰。这一设计使 WildPose 在动态与静态场景间无需切换策略，实现了统一的鲁棒估计。

## 核心模块与公式推导

### 3.1 可微束调整与更新算子

WildPose 将姿态估计形式化为一个端到端可微的束调整（BA）问题。系统的核心迭代单元是 **ConvGRU 更新算子**，它在每次迭代中根据当前光流估计、重投影残差及图像特征，预测下一时刻的光流、置信度、阻尼因子和上采样掩码：

$$(\hat{\mathbf{f}}_{i,j}^{t+1}, \hat{\mathbf{w}}_{i,j}^{t+1}, \hat{\eta}^{t+1}, \hat{\mathbf{u}}^{t+1}) = F(I_i, I_j, \tilde{\mathbf{f}}_{i,j}^{t}, \mathbf{r}_{i,j}^{t})$$

其中 $\hat{\mathbf{f}}_{i,j}$ 为预测光流，$\hat{\mathbf{w}}_{i,j}$ 为流置信度权重，$\hat{\eta}$ 为阻尼因子，$\hat{\mathbf{u}}$ 为上采样掩码，$\mathbf{r}_{i,j}^{t}$ 为重投影残差。

更新算子的输出直接引导可微 BA 层。BA 的目标函数为最小化预测光流与几何诱导光流之间的加权残差，联合优化所有相机姿态 $\hat{\omega}$ 和逆深度（视差）$\hat{d}$：

$$E(\hat{\omega}, \hat{d}) = \sum_{(i,j) \in G} \left\| \hat{\mathbf{f}}_{ij} - \tilde{\mathbf{f}}_{ij} \right\|_{\Sigma_{ij}}^2$$

其中 $G$ 为帧图（frame graph）中所有边的集合，$\tilde{\mathbf{f}}_{ij}$ 为由当前姿态和深度估计导出的几何光流，$\Sigma_{ij}$ 为权重矩阵。该 BA 层通过 Gauss-Newton 优化实现，支持端到端梯度回传。

### 3.2 MASt3R 特征编码器与适配器

WildPose 的核心创新之一是用冻结的预训练 **MASt3R ViT 编码器**替换 DROID-SLAM 中的简单 CNN 编码器，从而引入丰富的 3D 感知先验。MASt3R 编码器输出多层级 patch-based 特征，但 ConvGRU 需要卷积特征图作为输入。为此，论文设计了一个**轻量级适配器模块**，由两层卷积残差层组成，将 ViT 的 patch 特征转换为 1/8 分辨率的卷积特征图，使其与更新算子兼容（Figure 5, Figure 6）。

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/012_Figure_5.jpg]]
*Figure 5: Architecture of Update Operator. The ConvGRU iteratively updates the hiddens state from the image feature correlation, context features, and the current optical flow. The updated hidden state is further decoded to variables that will be used to guide pose and disparity estimation in the differentiable BA process*

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/013_Figure_6.jpg]]
*Figure 6: Architecture of the flow feature and context encoders. Both encoders take the MASt3R features as input and output features at 1/8 of the image resolution. For the context encoder, the dimension of the last convolution layer is 256*

### 3.3 运动掩码检测器

为处理动态场景，WildPose 引入一个专用的**高容量运动掩码检测器**。该检测器利用 MASt3R 编码器的多层特征，预测**逐边（per-edge）运动掩码**，而非传统方法中的逐帧掩码。

逐边掩码的关键优势在于解决时间歧义：对于帧图上的每条边 $(i, j)$，掩码 $M_{ij}$ 表示像素在帧 $i$ 到帧 $j$ 之间是否发生了独立运动。动态像素的真实光流由两部分组成——相机运动诱导的光流加上物体自身的 3D 位移投影：

$$\tilde{\mathbf{f}}_{i,j}^{\star} = \Pi_c \left( \hat{\omega}_j^{-1} \hat{\omega}_i \Pi_c^{-1} (p_i, \hat{d}_i) + X_{i,j}(p_i) \right)$$

其中 $\Pi_c$ 为相机投影函数，$X_{i,j}(p_i)$ 为像素 $p_i$ 在帧间经历的 3D 位移。运动掩码检测器通过学习识别哪些像素的 $X_{i,j}(p_i) \neq 0$，从而在 BA 中对动态区域进行降权处理。

### 3.4 多阶段训练策略

WildPose 采用三阶段课程训练：

**第一阶段（静态预训练）**：仅在静态数据集上训练更新算子，损失函数为：

$$\mathcal{L}_1 = w_{cam}\mathcal{L}_{cam} + w_{flow}\mathcal{L}_{flow} + w_{res}\mathcal{L}_{res}$$

其中 $\mathcal{L}_{cam}$ 为相机姿态误差，$\mathcal{L}_{flow}$ 为几何流误差，$\mathcal{L}_{res}$ 为残差流误差。

**第二阶段（混合微调）**：在静态与动态数据混合集上微调更新算子，使模型适应动态场景的残差模式。

**第三阶段（运动掩码训练）**：冻结更新算子，耦合可微 BA 层训练运动掩码检测器，损失函数为：

$$\mathcal{L}_2 = w_{cam}\mathcal{L}_{cam} + w_{mask}\mathcal{L}_{BCE}$$

其中 $\mathcal{L}_{BCE}$ 为运动掩码的二值交叉熵损失。此阶段不使用真实运动掩码，而是用预测掩码参与 BA 优化，使检测器学习生成有利于姿态估计的掩码。

### 3.5 推理阶段的 BA 与深度先验

推理时，BA 目标函数引入两个关键修改。首先，权重矩阵 $\bar{\Sigma}_{ij}$ 由流置信度 $\hat{\mathbf{w}}$ 与运动掩码 $M$ 的逐元素乘积构成，即 $\text{diag}(\hat{\mathbf{w}} \odot M)$，从而在优化中自动抑制动态像素的贡献。其次，加入度量深度先验作为正则化项：

$$E(\hat{\omega}, \hat{d}) = \sum_{(i,j)\in G} \left\| \hat{\mathbf{f}}_{ij} - \tilde{\mathbf{f}}_{ij} \right\|_{\bar{\Sigma}_{ij}}^2 + \lambda \sum_{i\in G} \left\| (\hat{d}_i - 1/D_i) \right\|^2$$

其中 $D_i$ 来自预训练度量深度估计器 Moge2 的初始深度，$\lambda$ 为正则化系数。该深度先验在局部 BA 中提供尺度约束，但在最终全局 BA 中被移除，以避免深度噪声对全局一致性的负面影响。

### 补充图表

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of Motion Masks. Top: Our per-edge masks (Frame i → j and i → k) resolve temporal ambiguity by capturing motion relative to a second frame, enabling fine-grained detection of inconsistencies along each frame-graph edge. Bottom: Per-frame masks from prior methods (WildGS-SLAM [60] and Vipe [17]) are shown for comparison; these approaches produce frame-level predictions that are unable to identify transient motion*

## 实验与分析

### 动态场景跟踪性能

WildPose在多个动态基准上展现出显著优势，尤其在挑战性最高的Wild-SLAM MoCap数据集上，平均ATE RMSE达到**0.39 cm**，较次优的动态SLAM方法WildGS-SLAM（0.46 cm）降低0.07 cm，较MegaSaM（2.40 cm）降低一个数量级（Table 1）。该数据集包含复杂的人-物交互运动，WildPose的逐边运动掩码能够精确识别动态像素，避免了传统语义分割方法对非预定义动态类别的漏检问题。

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/004_Table_1.jpg]]
*Table 1: Tracking Performance on Wild-SLAM MoCap Dataset [60] (ATE RMSE ↓ [cm]). Best results are highlighted as first , second , and third . All baseline methods were run using their publicly available code*

在Bonn RGB-D Dynamic数据集上，WildPose取得平均ATE RMSE **2.36 cm**，与WildGS-SLAM（2.31 cm）接近，但显著优于DROID-SLAM（4.91 cm）和MegaSaM（Table 2）。值得注意的是，Bonn数据集的Person序列存在严重的不一致曝光问题，这对依赖光度一致性的方法构成挑战——WildPose在该序列上的退化也揭示了合成数据预训练与真实域之间的差距（Figure 7）。

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/005_Table_2.jpg]]
*Table 2: Tracking Performance on Bonn RGB-D Dynamic Dataset [34] (ATE RMSE ↓ [cm])*

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/018_Figure_7.jpg]]
*Figure 7: Limitations. We visualize sampled images from Bonn RGB-D Dynamic Dataset [34] (Person sequence). The dataset has inconsistent exposure, which is challenging to our approach*

在TUM RGB-D动态序列上，WildPose以平均ATE RMSE **1.57 cm**略优于ViPE（1.58 cm），且无需后者所需的预定义动态语义类别先验（Table 3）。这验证了运动掩码检测器对通用动态模式的捕获能力，而非依赖特定语义类别。

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/006_Table_3.jpg]]
*Table 3: Tracking Performance on TUM RGB-D (dynamic) Dataset [42] (ATE RMSE ↓ [cm])*

### 静态与低运动量场景的鲁棒性

动态SLAM方法常见的副作用是在静态场景中性能退化，而WildPose通过混合微调策略有效避免了这一问题。在TUM RGB-D静态序列上，WildPose取得全轨迹ATE **0.027 m**，优于DROID-SLAM（0.038 m）（Table 4）。在7-Scenes数据集上，平均ATE为**0.049 m**，与DROID-SLAM（0.050 m）持平（Table 4）。在Sintel低运动量基准上，尺度归一化ATE为**0.022**，优于DROID-SLAM的0.029（Table 4）。这些结果表明，MASt3R提供的3D感知特征不仅有助于动态检测，也提升了静态场景下的几何推理精度。

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/007_Table_4.jpg]]
*Table 4: Tracking Performance on Low-motion and Static benchmarks. Reported as ATE RMSE ↓ in meters, except for Sintel where trajectories are scale-normalized following MegaSaM [27]. † indicates evaluation on all the frames*

### 深度估计性能

在Bonn RGB-D Dynamic数据集的长序列深度估计任务中，WildPose取得Abs.Rel **0.12**和δ1.25 **96.3**，优于MegaSaM（0.14 / 95.9）（Table 5）。这得益于Moge2度量深度先验在局部BA中提供的尺度约束，以及运动掩码对动态区域残差的降权，使得深度优化不受运动物体干扰。

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/010_Table_5.jpg]]
*Table 5: Comparison on Long-video Depth Estimation on Bonn RGB-D Dynamic [34] Dataset*

### 消融实验

Table 6的系统消融验证了三个核心组件的必要性：

1. **混合微调（Mix. Ft.）**：仅使用静态数据训练更新算子会导致动态场景性能大幅下降，验证了动态数据微调对泛化到运动场景的关键作用。
2. **运动掩码检测器（Mot. Mask）**：移除运动掩码后，动态数据集上的ATE显著升高，证实了逐边运动掩码对动态像素残差降权的有效性。
3. **全局BA深度正则化关闭（GBA Dep. Off）**：在最终全局BA中保留深度正则化项会引入噪声，关闭后性能提升，说明度量深度先验在局部优化阶段更有价值，全局优化应依赖多视图几何一致性。

完整模型在所有数据集上均取得最低误差，三个组件缺一不可。

### 失败模式与局限性

1. **域差距与曝光敏感性**：可学习模块仅在合成数据上训练，在真实场景中曝光剧烈变化时性能下降，典型案例如Bonn RGB-D Person序列（Figure 7）。这指向域自适应或在线微调的必要性。
2. **内参依赖**：方法假设相机内参已知且固定，不适用于未标定视频或变焦场景。
3. **计算开销**：推理时峰值GPU显存达18.62 GiB（Table 11），主要源于MASt3R和Moge2基础模型，限制了在资源受限设备上的部署。模型蒸馏或轻量化替代方案是可行的缓解方向。

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/017_Table_11.jpg]]
*Table 11: Run time and memory usage on Wild-SLAM [60]. We compute FPS by dividing the total number of frames by the total running time. The experiments are conducted on an RTX 4090 GPU*

### 公平性说明

实验设置中需注意以下公平性考量：
- VGGT和π3仅在关键帧上评估（由WildPose挑选的关键帧），而其他方法在全轨迹上评估，关键帧评估的挑战性更低。
- WildPose使用Moge2度量深度作为初始化和局部BA正则项，而DROID-SLAM等基线无此先验；但在最终全局BA中已去除深度正则项以减少噪声影响。
- ViPE需要预定义动态语义类别，WildPose无需此类先验，但实验中已按要求为ViPE提供语义输入。
- 所有基线均使用公开代码运行，确保对比公平。

### 补充图表

![[assets/figures/papers/paper_list_l2275_https_arxiv_org_abs_2605_12774/figures/009_Table_6.jpg]]
*Table 6: WildPose Ablation Study (ATE RMSE ↓ [cm]). We report the average tracking error for each dataset. Mix. Ft. denotes finetuning the update operator with the mix of static and dynamic datasets, Mot. Mask denotes the motion mask detector, and GBA Dep. Off denotes removing the depth regularization term during the final global BA*

## 方法谱系与知识库定位

### 1. 在动态SLAM谱系中的位置

WildPose 处于**前馈感知模型与可微束调整（BA）交叉融合**的关键节点。其方法谱系可沿两条主线追溯：

**主线一：可微BA SLAM。** DROID-SLAM（Teed et al., RSS 2021）建立了基于ConvGRU迭代更新与可微BA的端到端可学习SLAM范式，但设计上仅面向静态场景。WildPose 直接继承了 DROID-SLAM 的更新算子架构与可微BA优化框架，但在三个核心维度上实现了根本性改造：（1）将浅层CNN编码器替换为冻结的预训练MASt3R ViT编码器（Dusmanu et al., arXiv 2024），引入3D感知先验；（2）新增专用运动掩码检测器，利用MASt3R多层特征生成逐边运动掩码；（3）将BA权重矩阵从单一的流置信度 $\mathbf{w}$ 扩展为流置信度与运动掩码的乘积 $\text{diag}(\hat{\mathbf{w}} \odot M)$，实现对动态像素残差的软降权。这三项改造使得原本仅适用于静态环境的可微BA管线能够鲁棒地处理动态场景。

**主线二：动态SLAM的运动处理策略。** 现有动态SLAM方法可依运动检测机制分为两类。第一类依赖语义分割识别潜在动态物体，如 **ViPE** 需预先指定动态语义类别作为输入，但语义先验无法覆盖所有运动物体（如被移动的椅子），且静态物体被误标为动态时会造成信息损失。第二类依赖在线学习的不确定性建模，如 **WildGS-SLAM**（Zheng et al., CVPR 2025）通过训练不确定性MLP生成帧级掩码，但帧级掩码无法解析时间歧义——一个像素在帧 $i \to j$ 中可能是动态的，但在帧 $i \to k$ 中可能是静态的。**MegaSaM** 则尝试学习运动估计，但受限于运动预测器的容量和训练数据多样性。

WildPose 的运动掩码检测器在机制上区别于上述两类：它不依赖语义类别，而是从MASt3R的3D感知特征中直接学习**逐边**运动模式，从而天然具备时间歧义解析能力。Figure 3 的定性对比清晰展示了这一优势：WildPose 的逐边掩码能够区分同一帧在不同边上的运动状态，而 WildGS-SLAM 和 ViPE 的帧级掩码则无法做到。

### 2. 与前馈方法的边界

近年来，全前馈姿态估计方法（如 **VGGT**、**$\pi$3**）通过大规模预训练展现出强泛化能力，但其本质是逐帧或短窗口回归，缺乏长序列的全局一致性约束。MASt3R-SLAM 尝试将 MASt3R 直接接入SLAM管线，但未引入可学习的运动处理机制。WildPose 的定位恰好落在前馈方法与优化方法的**互补边界**上：利用MASt3R的丰富感知前端提取3D特征，再通过可微BA的端到端优化后端实现长序列的全局一致性。这一融合策略使得 WildPose 在动态场景中超越纯前馈方法，在静态场景中超越纯优化方法——Table 4 显示其在静态TUM和7-Scenes上的全轨迹ATE分别达到0.027 m和0.049 m，优于DROID-SLAM的0.038 m和0.050 m。

### 3. 适用边界与关键假设

WildPose 的有效性建立在以下假设之上，这些假设也构成了其适用边界：

- **已知固定内参。** 方法假设相机内参已知且在整个序列中保持恒定。对于未标定视频或变焦场景，方法无法直接适用。这是一个硬性边界，源于可微BA层需要内参来建立像素与3D点的投影关系。
- **度量深度先验可用。** 推理阶段依赖 Moge2 提供的度量深度来初始化视差并作为局部BA的正则化项。在深度先验质量差的场景（如无纹理区域、透明表面），初始化和正则化可能引入偏差。值得注意的设计是，最终全局BA中显式去除了深度正则化项，以降低噪声深度对全局一致性的影响——Table 6 消融实验证实了这一操作的有效性。
- **合成数据训练的域差距。** 可学习模块（更新算子、运动掩码检测器）仅在合成数据上训练（TartanAir V2、Kubric生成数据等），与真实场景存在域差距。这一限制在曝光剧烈变化的序列上尤为突出——Figure 7 展示了Bonn RGB-D Person序列中不一致曝光对方法的挑战。

### 4. 局限性与开放问题

**已知局限：**

1. **域差距导致的性能退化。** 在Bonn RGB-D Dynamic数据集上，WildPose 的平均ATE为2.36 cm，略逊于 WildGS-SLAM 的2.31 cm（Table 2），部分原因在于Bonn数据集的曝光不一致性超出了合成训练数据的覆盖范围。
2. **计算资源消耗较高。** 峰值GPU显存达18.62 GiB（Table 11），主要源于MASt3R和Moge2两个基础模型。这限制了其在资源受限平台上的部署。
3. **未标定视频不适用。** 内参已知假设排除了大量消费级视频和野外数据。

**开放问题：**

1. **域自适应与在线内参标定。** 能否通过测试时自适应（test-time adaptation）或在线内参估计，缩小合成数据到真实场景的域差距，同时将方法拓展到未标定视频？这需要在不破坏冻结MASt3R特征稳定性的前提下，设计轻量的自适应机制。
2. **基础模型轻量化。** MASt3R和Moge2是计算瓶颈的主要来源。能否通过知识蒸馏或架构搜索，在保持3D感知质量的同时显著降低推理开销？这直接关系到方法的实际可部署性。
3. **运动掩码检测器的泛化边界。** 当前运动检测器在Kubric生成的刚体运动模式上训练，其对非刚体运动（如人体关节运动、流体）的泛化能力尚未被系统评估。这需要在更丰富的运动模式数据上进行验证和可能的架构调整。

## 原文 PDF

![[paperPDFs/CVPR_2026/WildPose_A_Unified_Framework_for_Robust_Pose_Estimation_in_the_Wild.pdf]]