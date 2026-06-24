---
title: "ResiHMR: Residual-Limb Aware Single-Image 3D Human Mesh Recovery for Individuals with Limb Loss"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ResiHMR_Residual_Limb_Aware_Single_Image_3D_Human_Mesh_Recovery_for_Individuals_with_Limb_Loss.pdf
project_link: null
code_link: null
aliases:
- ResiHMR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 引入残肢关键点并适配运动学子图：通过残肢锚点偏移因子优化和基于几何的残肢表面重建两个组件，自适应地修正拓扑并构建水密残端表面。
primary_logic: 通过将残肢终点参数化为锚点与上游关节连线上的比例因子，结合2D残肢关键点监督和人体测量先验，可端到端优化残肢长度与位置；随后通过平面切割和边界密封生成显式水密残端几何，根本解决了固定拓扑模型在截肢场景下的幻觉和失真问题。
claims:
- ResiHMR在HSMR主干上将残肢端点2D MPJPE从73.61像素降低到23.19像素，同时保持完好关节精度。
- 与基线相比，ResiHMR避免了幻肢和代偿性扭曲，生成解剖学一致的网格。
- ResiHMR是唯一显式建模残肢端点的方法，而其他方法使用固定中点代理导致残肢定位误差大。
- LDPose-LimbLoss Evaluation Dataset 上 Body Kpts 2D MPJPE (px) = 24.75
---

# ResiHMR: Residual-Limb Aware Single-Image 3D Human Mesh Recovery for Individuals with Limb Loss

> [!tip] 核心洞察
> 通过将残肢终点参数化为锚点与上游关节连线上的比例因子，结合2D残肢关键点监督和人体测量先验，可端到端优化残肢长度与位置；随后通过平面切割和边界密封生成显式水密残端几何，根本解决了固定拓扑模型在截肢场景下的幻觉和失真问题。

| 字段 | 内容 |
|------|------|
| 中文题名 | 残肢感知的单图像3D人体网格恢复：面向截肢个体的ResiHMR框架 |
| 英文题名 | ResiHMR: Residual-Limb Aware Single-Image 3D Human Mesh Recovery for Individuals with Limb Loss |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.28025) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | ResiHMR |
| Dataset | LDPose-LimbLoss Evaluation Dataset |

> [!tip] 效果简介
> - LDPose-LimbLoss Evaluation Dataset 上，Body Kpts 2D MPJPE (px) 24.75 vs 28.27 (HSMR) (-3.52)；Res-Limb 2D MPJPE (px) 23.19 vs 73.61 (HSMR) (-50.42)；Intact Kpts 2D MPJPE (px) 24.87 vs 24.56 (HSMR) (+0.31)。

## 概述

现有单图像3D人体网格恢复（HMR）方法——无论是优化拟合范式（如 **SMPLify-X**，Pavlakos et al., CVPR 2019）还是回归范式（如 **HSMR**、**TokenHMR**、**CameraHMR**、**PromptHMR**）——均建立在完整肢体先验和固定运动学拓扑之上。当输入为截肢个体时，这些方法无法正确表示残肢几何，普遍产生**幻肢**（在缺失部位生成完整肢体）、**关节塌陷**以及为补偿拓扑失配而出现的**整体姿态扭曲**（Figure 2）。

ResiHMR 针对上述瓶颈，提出了一种**无需训练、即插即用**的优化框架。其核心调控变量是**残肢关键点**的引入与运动学子图的自适应：通过将残肢终点参数化为锚点与上游关节连线上的连续比例因子 $\lambda_r$，并结合2D残肢关键点监督与人体测量先验进行端到端优化，从根本上消除了固定拓扑模型在截肢场景下的幻觉和失真。随后，基于优化后的残肢参数执行几何切割与边界密封，生成显式的水密残端表面。

在覆盖多种截肢类型、级别、姿态和人口统计特征的 **LDPose-LimbLoss** 评估数据集（255张图像，仅用于评估）上，ResiHMR 展现出决定性优势：以 HSMR 为骨干时，残肢端点 2D MPJPE 从 73.61 像素骤降至 **23.19 像素**（降幅 68.5%），同时完好关节精度几乎无损（24.56 → 24.87 像素）；以 SMPLify-X 为骨干时，整体关节 2D MPJPE 从 47.67 降至 **41.77 像素**（Table 1）。定性结果表明，ResiHMR 是唯一显式建模残肢端点的方法，而其他方法使用固定中点代理导致残肢定位误差巨大（Section 4.2）。

ResiHMR 的局限性主要体现在两方面：残肢表面重建依赖光滑凸先验，无法复现个体特异的不规则轮廓（Figure 8）；单目输入导致侧视角度存在深度歧义（Figure 9）。这些局限源于残肢3D真实值数据的缺失，也指明了未来构建专用3D数据集和引入个体化形状先验的开放方向。

## 背景与动机

### 问题背景

单图像3D人体网格恢复（Human Mesh Recovery, HMR）旨在从单张RGB图像中重建完整的人体三维姿态与形状，在虚拟现实、运动分析、数字人等应用中具有广泛价值。近年来，以**SMPLify-X**（Pavlakos et al., CVPR 2019）、**HSMR**、**TokenHMR**（CVPR 2024）、**CameraHMR**（3DV 2025）、**PromptHMR**（CVPR 2025）为代表的方法取得了显著进展，能够从单目图像中恢复精细的全身网格。

然而，这些方法的共同前提是**人体拥有完整的四肢**。它们依赖从大规模健康人体数据中学习的完整肢体先验，并使用固定的运动学拓扑（如SMPL-X或SKEL骨架的完整关节树）。当面对截肢个体时，这一前提被根本性地打破。

### 现有方法的根本缺陷

现有HMR方法在截肢场景下的失败并非偶然，而是由其设计原理决定的：

**1. 幻肢与关节塌陷。** 由于模型内置了“四肢必须完整”的先验，当输入图像中的肢体缺失时，优化或回归过程仍会强制生成缺失的肢体，导致“幻肢”（hallucinated limbs）现象。另一种表现为关节塌陷——缺失的肢体末端关节被错误地收缩到上游关节附近，产生不自然的几何形态。如Figure 2所示，SMPLify-X和HSMR在截肢者图像上均出现明显的幻肢或下半身扭曲。

**2. 固定拓扑无法表示残肢。** 现有方法的运动学骨架是固定的，没有为残肢端点（residual-limb endpoint）预留表示空间。当需要定位残肢终点时，这些方法只能使用肢体段中点作为朴素代理（naive midpoint proxy），导致残肢定位误差极大——HSMR的残肢端点2D MPJPE高达73.61像素（Table 1）。

**3. 代偿性姿态扭曲。** 为“解释”缺失的肢体，优化过程常常扭曲身体其他部位以最小化整体拟合误差，产生整体姿态失真。这种扭曲不仅影响视觉质量，更使得重建结果在临床和生物力学分析中失去可用性。

### 核心瓶颈与解决思路

**根本瓶颈**在于：现有HMR方法将“完整肢体”作为不可动摇的结构先验，缺乏对运动学拓扑的自适应能力和对残肢几何的显式建模能力。

**ResiHMR的核心洞察**是：通过引入残肢关键点（residual-limb keypoints）并适配运动学子图，可以将问题从“强制拟合完整肢体”转化为“在观测到的解剖有效子图上进行约束优化”。具体而言，将残肢终点参数化为锚点（anchor joint）与上游关节连线上的连续比例因子 $\lambda_r$：$\mathbf{R}_r = \mathbf{J}_a + \lambda_r (\mathbf{J}_t - \mathbf{J}_a)$，使得残肢长度和位置可以端到端优化，同时保持与2D残肢关键点标注和人体测量先验的一致性。在此基础上，通过几何切割和边界密封生成显式的水密残端表面，从根本上解决固定拓扑模型在截肢场景下的幻觉和失真问题。

### 研究动机

ResiHMR的动机源于一个明确的现实需求：**使3D人体重建技术对截肢个体同样可用**。截肢者在全球人口中占有不可忽视的比例，但现有HMR研究几乎完全忽略了这一群体。本文旨在填补这一空白，提出首个显式建模残肢端点并自适应运动学拓扑的优化框架，使得单图像3D人体网格恢复能够生成解剖学一致、残肢感知的重建结果。

## 核心创新

ResiHMR 的根本创新在于**显式打破现有 HMR 方法的“完整肢体”假设**，通过两个互补的模块——残肢锚点-因子优化与残肢表面重建——将固定运动学拓扑自适应地重构为截肢者专属的表示，从而从根本上消除幻肢和代偿性姿态扭曲。

### 问题瓶颈：完整肢体先验的失效

现有单图像 HMR 方法（无论是优化式的 **SMPLify-X**（Pavlakos et al., CVPR 2019），还是回归式的 **HSMR**、**TokenHMR**（CVPR 2024）、**CameraHMR**（3DV 2025）、**PromptHMR**（CVPR 2025））均内嵌了完整肢体的运动学先验和固定关节树。当输入为截肢者图像时，这些方法被迫将不存在的肢体“解释”为可见结构，导致三类典型失败（见 Figure 2）：

- **幻肢**：在截肢位置生成不存在的完整肢体网格；
- **关节塌陷**：缺失肢体的关节被错误地吸附到躯干或其他肢体上；
- **代偿性扭曲**：为“合理化”幻肢，模型扭曲整体姿态，使完好肢体的重建也受到污染。

### Changed Slots：三个维度的拓扑与几何重构

ResiHMR 在以下三个关键维度上对基线方法进行了根本性替换：

#### 1. 运动学拓扑：从固定完整图到自适应残肢子图

**基线**：SMPL-X/HSMR 使用固定的完整肢体关节树，包含所有标准关节，无法表示“肢体终止于某点”的拓扑。

**ResiHMR**：引入残肢锚点（anchor joint）和残肢比例因子（residual-limb factor），仅保留观测到的运动学子图。具体而言，对于每个截肢部位，定义锚点关节 $\mathbf{J}_a$ 和上游关节 $\mathbf{J}_t$，残肢端点不再是一个独立关节，而是两者连线上的连续点：

$$\mathbf{R}_r = \mathbf{J}_a + \lambda_r (\mathbf{J}_t - \mathbf{J}_a)$$

其中 $\lambda_r \in [0, 1]$ 控制残肢的相对长度。这一参数化将残肢定位从离散的“关节存在/不存在”二值问题转化为连续的标量优化问题，使得端点位置可以精确匹配 2D 观测。

#### 2. 残肢表示：从中点代理到显式可优化端点

**基线**：其他 HMR 方法不显式预测残肢端点。为进行公平比较，作者为这些方法定义了“朴素中点代理”（naive midpoint proxy）——即取对应肢体段的中点作为残肢端点近似。这种代理与真实残肢位置存在系统性偏差，导致残肢定位误差极大（HSMR 的 Res-Limb 2D MPJPE 高达 73.61 px）。

**ResiHMR**：通过残肢锚点-因子优化（Residual Anchor-Factor Optimization）模块，联合优化锚点位置和比例因子 $\lambda_r$，损失函数为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{reproj}} + \alpha \mathcal{L}_{\mathrm{reg}} + \mu \mathcal{L}_{\mathrm{len}}$$

其中 $\mathcal{L}_{\mathrm{reproj}}$ 约束残肢端点的 2D 重投影与标注关键点一致，$\mathcal{L}_{\mathrm{len}}$ 保持残肢节段长度在 SMPLify-X 初始值附近（编码人体测量先验）：

$$\mathcal{L}_{\mathrm{len}} = ((\mathbf{J}_t - \mathbf{J}_a) - (\mathbf{J}_t - \mathbf{J}_a^{\mathrm{init}}))^2$$

这一设计使得 ResiHMR 成为**唯一显式建模残肢端点的方法**（Section 4.2），直接将残肢端点误差从 73.61 px 降至 23.19 px（Table 1）。

#### 3. 网格重建：从完整肢体网格到几何切割与密闭残端

**基线**：所有现有方法输出完整肢体网格，即使截肢部位也被“填满”为标准肢体几何。

**ResiHMR**：在获得优化后的残肢参数后，通过几何切割（geometry-based cutting）移除远端肢体几何。切割平面由残肢端点 $\mathbf{p}_r$ 和法向量 $\hat{\mathbf{n}}$ 定义：

$$\mathbf{p}_r = \mathbf{J}_a^{\star} + \lambda_r^{\star} (\mathbf{J}_t^{\mathrm{init}} - \mathbf{J}_a^{\star})$$

$$\hat{\mathbf{n}} = \frac{\mathbf{J}_a^{\star} - \mathbf{J}_t^{\mathrm{init}}}{\|\mathbf{J}_a^{\star} - \mathbf{J}_t^{\mathrm{init}}\|}$$

切割后提取边界环并进行密封处理，生成光滑凸起的水密残端表面。这一几何管线不依赖任何训练数据，完全基于优化后的运动学参数驱动，确保残端与身体网格的拓扑一致性。

### 关键洞察：端到端可微的拓扑自适应

ResiHMR 的核心洞察在于：**将残肢终点参数化为锚点与上游关节连线上的比例因子，结合 2D 残肢关键点监督和人体测量先验，可端到端优化残肢长度与位置；随后通过平面切割和边界密封生成显式水密残端几何**。这一设计使得：

- 残肢定位与完好关节重建**解耦但协同优化**：Table 1 显示，ResiHMR 在 HSMR 主干上使残肢端点误差下降 50.42 px 的同时，完好关键点精度几乎不变（24.56 → 24.87 px），证明组件主要改善残肢定位且无副作用；
- 框架具有**主干通用性**：在优化式主干（SMPLify-X）和回归式主干（HSMR）上均带来显著增益，表明拓扑自适应和重建模块独立于具体的参数回归策略；
- 完全**无需训练数据**：ResiHMR 是纯优化框架，不依赖任何截肢者 3D 训练集，仅利用 2D 关键点监督和 SMPL-X 的人体先验即可工作。

### 证据强度与需人工验证点

- **强证据**：Table 1 的定量消融直接证明了 changed slots 的有效性——残肢端点误差的巨幅下降（73.61 → 23.19）与完好关节精度的保持（24.56 → 24.87）构成清晰的因果证据链。
- **需人工验证**：Figure 6 中与 AJAHR 的对比声称 AJAHR 的“关节塌陷”表示不符合真实解剖，但该结论依赖专家验证的外部证据，论文未提供独立的量化解剖学评估指标，建议读者结合临床专业知识判断。

## 整体框架

ResiHMR 是一个完全基于优化的即插即用框架，无需任何训练数据集，可嵌入任意能输出 SMPL‑X 参数（相机、姿态、形状）的 HMR 管线，包括优化式方法（如 **SMPLify‑X** (Pavlakos et al., CVPR 2019)）和回归式方法（如 **HSMR**、**TokenHMR** (CVPR 2024)、**CameraHMR** (3DV 2025)、**PromptHMR** (CVPR 2025) 等）。框架的整体流程如 Figure 3 和 Figure 10 所示，由三个阶段串联构成：

![[assets/figures/papers/paper_list_l1035_https_arxiv_org_abs_2604_28025/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our ResiHMR framework.Given an input image, SMPL-X is initialized using intact 2D keypoints. Our Residual Anchor–Factor Optimization adapts the kinematic graph by refining anchor joints and residual-limb proportions under supervision of residual-limb 2D keypoints. The Residual-Limb Reconstruction module then removes distal limb geometry and generates a smooth, watertight stump surface, producing anatomically realistic residual-limb aware meshes*

![[assets/figures/papers/paper_list_l1035_https_arxiv_org_abs_2604_28025/figures/013_Figure_10.jpg]]
*Figure 10: Overview of our ResiHMR Framework with other existing HMR methods to initialize the SMPL-X/SMPL, in this case, we have HSMR as the exmaple for the regression-based HMR method*

1. **SMPL‑X 初始化**  
   给定单张 RGB 图像及 LDPose 格式的全身 2D 关键点，首先利用完好肢体的关键点拟合 SMPL‑X 模型，获得初始的姿态、形状和相机参数。该步骤采用标准 SMPLify‑X 优化目标：
   $$
   \operatorname*{min}_{\theta,\beta,\mathbf{t}} E_{\mathrm{data}} + E_{\mathrm{prior}}
   $$
   其中数据项为投影 3D 关节与检测到的 2D 关键点之间的加权重投影误差：
   $$
   E_{\mathrm{data}} = \sum_i w_i \| \boldsymbol{\pi}(\mathbf{J}_i) - \mathbf{k}_i^{2D} \|^2
   $$

2. **残肢锚点‑因子优化 (Residual Anchor–Factor Optimization)**  
   在初始化参数基础上，该模块自适应地修正运动学拓扑：将残肢终点参数化为锚点关节 $\mathbf{J}_a$ 与其上游关节 $\mathbf{J}_t$ 连线上的连续点，由可优化的残肢比例因子 $\lambda_r$ 控制：
   $$
   \mathbf{R}_r = \mathbf{J}_a + \lambda_r (\mathbf{J}_t - \mathbf{J}_a)
   $$
   优化时联合最小化残肢端点的 2D 重投影误差、锚点正则化项以及节段长度保持项，使残肢定位与 2D 关键点监督一致，同时保留人体测量先验。优化器采用带强 Wolfe 线搜索的 L‑BFGS，当残肢端点重投影误差低于 15 像素时接受解。

3. **残肢重建 (Residual‑Limb Reconstruction)**  
   根据优化后的锚点 $\mathbf{J}_a^{\star}$ 和比例因子 $\lambda_r^{\star}$，在 3D 空间中确定切割平面位置：
   $$
   \mathbf{p}_r = \mathbf{J}_a^{\star} + \lambda_r^{\star} (\mathbf{J}_t^{\mathrm{init}} - \mathbf{J}_a^{\star})
   $$
   切割平面法向沿残肢轴线方向：
   $$
   \hat{\mathbf{n}} = \frac{\mathbf{J}_a^{\star} - \mathbf{J}_t^{\mathrm{init}}}{\|\mathbf{J}_a^{\star} - \mathbf{J}_t^{\mathrm{init}}\|}
   $$
   随后执行网格切割、远端几何移除、边界提取与密封，生成光滑凸起的水密残端表面，最终输出解剖学一致的残肢感知 3D 人体网格。

整个框架的核心设计在于：通过引入残肢关键点并适配运动学子图，从根本上消除了固定完整肢体拓扑带来的幻肢、关节塌陷和姿态扭曲问题；同时以几何切割与密封替代简单的关节折叠或顶点坍缩，显式重建出可解释的残端几何。

### 补充图表

![[assets/figures/papers/paper_list_l1035_https_arxiv_org_abs_2604_28025/figures/001_Figure_1.jpg]]
*Figure 1: Demonstration of ResiHMR. Our framework recovers anatomically coherent 3D body meshes from a single RGB image by adapting the kinematic topology and explicitly reconstructing residual-limb geometry*

## 核心模块与公式推导

ResiHMR 是一个纯优化框架，无需训练数据，可作为即插即用模块嵌入任何输出 SMPL-X 参数的 HMR 管线（包括优化式和回归式方法）。其核心由两个模块构成：**残肢锚点-因子优化**（Residual Anchor-Factor Optimization）和**残肢重建**（Residual-Limb Reconstruction）。前者自适应地修正运动学拓扑，后者基于几何操作生成水密残端表面。

### SMPL-X 初始化

给定输入图像和 LDPose 格式的全身 2D 关键点（包含 8 个残肢端点），ResiHMR 首先仅使用完好关键点拟合 SMPL-X 模型，获得初始姿态 $\theta$、形状 $\beta$ 和全局平移 $\mathbf{t}$。优化目标为：

$$\operatorname*{min}_{\theta,\beta,\mathbf{t}} E_{\mathrm{data}} + E_{\mathrm{prior}} \tag{1}$$

其中数据项将投影的 3D 关节与检测到的 2D 关键点对齐：

$$E_{\mathrm{data}} = \sum_i w_i \| \boldsymbol{\pi}(\mathbf{J}_i) - \mathbf{k}_i^{2D} \|^2 \tag{2}$$

$\boldsymbol{\pi}(\cdot)$ 为相机投影，$w_i$ 为关键点权重，$\mathbf{J}_i$ 为 SMPL-X 回归的 3D 关节位置。先验项 $E_{\mathrm{prior}}$ 约束姿态和形状在合理范围内。此阶段仅使用完好关键点，残肢端点不参与拟合，避免完整肢体先验引入幻肢。

### 残肢锚点-因子优化

初始化完成后，该模块联合优化残肢锚点位置和残肢比例因子，以适配截肢后的运动学子图。残肢端点 $\mathbf{R}_r$ 参数化为锚点 $\mathbf{J}_a$ 与上游关节 $\mathbf{J}_t$ 连线上的连续点：

$$\mathbf{R}_r = \mathbf{J}_a + \lambda_r (\mathbf{J}_t - \mathbf{J}_a) \tag{3}$$

其中 $\lambda_r \in (0, 1)$ 为可优化的残肢比例因子，控制残肢长度。锚点 $\mathbf{J}_a$ 为截肢侧最近的完好关节（如膝上截肢时锚点为髋关节），上游关节 $\mathbf{J}_t$ 为原完整肢体的远端关节（如踝关节）。此参数化将残肢终点约束在解剖学合理的射线上，避免了固定中点代理带来的定位偏差。

优化损失函数由三项组成：

$$\mathcal{L} = \mathcal{L}_{\mathrm{reproj}} + \alpha \mathcal{L}_{\mathrm{reg}} + \mu \mathcal{L}_{\mathrm{len}} \tag{4}$$

- **$\mathcal{L}_{\mathrm{reproj}}$**：残肢端点 2D 重投影误差，将 $\mathbf{R}_r$ 投影后与标注的残肢端点关键点对齐。
- **$\mathcal{L}_{\mathrm{reg}}$**：锚点正则化项，约束 $\mathbf{J}_a$ 不偏离其初始位置过远。
- **$\mathcal{L}_{\mathrm{len}}$**：节段长度保持项，编码人体测量先验，约束残肢节段长度保持在 SMPLify-X 初始值附近：

$$\mathcal{L}_{\mathrm{len}} = ((\mathbf{J}_t - \mathbf{J}_a) - (\mathbf{J}_t - \mathbf{J}_a^{\mathrm{init}}))^2 \tag{5}$$

优化采用 L-BFGS 配合强 Wolfe 线搜索，当残肢端点重投影误差低于 15 像素时接受解。此设计的因果机制在于：通过 $\lambda_r$ 显式建模残肢比例，结合 2D 残肢关键点监督和长度正则，可端到端地确定残肢终点位置，同时保持完好关节精度不变（Table 1 显示完好关键点 MPJPE 仅从 24.56 变为 24.87）。

### 残肢重建

获得优化后的锚点 $\mathbf{J}_a^{\star}$ 和比例因子 $\lambda_r^{\star}$ 后，该模块执行三步几何操作生成水密残端表面：

**第一步：切割平面定位。** 3D 切割点 $\mathbf{p}_r$ 沿残肢轴线确定：

$$\mathbf{p}_r = \mathbf{J}_a^{\star} + \lambda_r^{\star} (\mathbf{J}_t^{\mathrm{init}} - \mathbf{J}_a^{\star}) \tag{6}$$

切割平面法向量 $\hat{\mathbf{n}}$ 沿残肢轴线方向：

$$\hat{\mathbf{n}} = \frac{\mathbf{J}_a^{\star} - \mathbf{J}_t^{\mathrm{init}}}{\|\mathbf{J}_a^{\star} - \mathbf{J}_t^{\mathrm{init}}\|} \tag{7}$$

**第二步：网格切割与边界清理。** 在 $\mathbf{p}_r$ 处以 $\hat{\mathbf{n}}$ 为法向切割 SMPL-X 网格，移除远端肢体几何（包括顶点和面片），仅保留近端部分。随后清理切割产生的非流形边界，确保边界为单连通环。

**第三步：残端密封。** 对切割边界进行三角剖分，生成光滑凸起的残端表面，并与近端网格缝合，形成水密网格。残端表面采用凸先验近似，不依赖个体化形状数据。

该模块的根本价值在于：与 AJAHR 等将 SMPL 顶点塌缩至父关节的方法不同（Figure 6），ResiHMR 通过几何切割和边界密封生成显式的解剖学残端表面，避免了关节级截断导致的解剖失真。但需注意，光滑凸先验无法完全复现个体特异的不规则残肢轮廓（Figure 8），这是缺乏残肢 3D 训练数据带来的固有限制。

## 实验与分析

### 核心发现：残肢端点定位的突破性改善

现有HMR方法在截肢个体上的根本失败在于：它们依赖完整肢体先验和固定运动学拓扑，无法表示残肢的真实几何，因而普遍产生幻肢、关节塌陷和代偿性姿态扭曲。ResiHMR通过引入残肢关键点并适配运动学子图，从根本上解决了这一问题。**Table 1** 的核心结果清晰地揭示了这一突破：

![[assets/figures/papers/paper_list_l1035_https_arxiv_org_abs_2604_28025/figures/006_Table_1.jpg]]
*Table 1: Comparison of recent HMR methods and ResiHMR under either SMPLify-X or HSMR as backbone. Best results are shown in bold. For all other HMR methods, as they do not explicitly predict residual-limb endpoints, we define a naive midpoint proxy on the corresponding limb segment to enable consistent scoring under a unified protocol*

- **残肢端点定位精度飞跃**：以HSMR为骨干时，残肢端点2D MPJPE从73.61像素骤降至23.19像素（降幅达68.5%）。这一巨大差距源于所有基线方法均无法显式建模残肢端点——它们仅使用固定中点代理进行评分，而ResiHMR通过残肢锚点-因子优化端到端地学习残肢的真实终止位置。
- **完好关节精度无损**：在同一配置下，完好关键点2D MPJPE仅从24.56像素微增至24.87像素（+0.31像素），证明ResiHMR的拓扑自适应和残肢重建模块对完好身体区域的精度无副作用。
- **整体身体精度提升**：Body Kpts 2D MPJPE从28.27降至24.75像素，mIoU从0.705提升至0.741，表明残肢端点的准确定位有助于全局网格对齐。

### 跨骨干的通用性验证

ResiHMR作为即插即用模块，在优化式主干（SMPLify-X）和回归式主干（HSMR）上均表现出显著增益：
- 在SMPLify-X骨干上，Body Kpts 2D MPJPE从47.67降至41.77像素（-5.90），完好关键点从41.32降至37.40像素（-3.92），mIoU从0.662提升至0.703（+0.041）。
- 在HSMR骨干上，残肢端点改善尤为突出（73.61→23.19），这是因为回归式方法在缺乏残肢先验时更容易产生严重的幻肢和关节错位，而ResiHMR的显式残肢建模从根本上修正了这一偏差。

两组结果共同证明：ResiHMR的拓扑自适应机制和几何重建模块具有骨干无关的通用性，可广泛部署于现有HMR流程。

### 定性对比：幻肢消除与姿态一致性

**Figure 2** 的定性对比直观展示了ResiHMR相较于SMPLify-X和HSMR的关键优势：
- SMPLify-X和HSMR在截肢个体上出现明显的幻肢（重建出不应存在的完整肢体）或为补偿缺失肢体而产生下肢扭曲。
- ResiHMR正确定位残肢终止点，避免了代偿性姿态失真，生成解剖学一致的网格。

**Figure 5** 的多视角重建结果进一步验证了残肢重建的几何合理性：从正面、背面、侧面及T-Pose视角观察，残端表面呈现光滑凸起的闭合几何，与输入图像中的残肢轮廓基本吻合。

### 消融分析：组件贡献的证据链

Table 1中ResiHMR变体与基线的对比提供了清晰的消融证据：
- **残肢端点显式建模的贡献**：ResiHMR是唯一显式建模残肢端点的方法（Section 4.2明确声明），而所有其他方法使用固定中点代理。残肢端点MPJPE从73.61到23.19的降幅直接量化了这一设计的贡献。
- **拓扑自适应的贡献**：ResiHMR将运动学估计约束到观测到的运动学子图（仅保留存在的关节和残肢锚点），避免了在缺失肢体上产生虚假关节回归。完好关键点精度的保持（24.56→24.87）证明这一约束未损害有效区域的估计。
- **残肢重建的贡献**：mIoU的提升（0.705→0.741）表明几何切割和密闭残端生成模块改善了整体网格与人体轮廓的对齐。

### 失败模式与局限性

尽管ResiHMR在残肢端点定位上取得了突破性进展，但实验也揭示了两个核心局限：

**1. 残肢表面形状近似（Figure 8）**：重建的残端表面采用光滑凸先验，无法完全复现个体特异的不规则残肢轮廓。图中黄色标注区域显示真实残端轮廓与重建凸表面之间存在明显偏差，而完好肢体（绿色标注）则重建忠实。这一局限源于缺乏残肢3D训练数据，残端形状仅依赖几何先验而非实例级形状线索。

**2. 单目深度歧义（Figure 9）**：正面视角下网格与输入图像对齐良好，但侧面视角暴露出深度歧义——手臂被误置于躯干前方而非搭在髋部，上身前倾的姿态无法从正面视角推断。这些歧义源于对2D标注和健康人体先验的依赖，缺少3D残肢真实值进行深度约束。

### 评估数据集的公平性保障

LDPose-LimbLoss评估数据集（255张图像，**Figure 4**展示样本多样性）的设计确保了评估的公平性：
- 涵盖多种截肢类型、级别、残肢长度、活动、性别和种族分布（**Figure 7**统计分布）。
- 仅用于评估，未参与训练或超参数调优，消除数据泄露和过拟合偏差。
- 所有残肢端点标注经过多轮审核和共识，保证标签精确一致。

![[assets/figures/papers/paper_list_l1035_https_arxiv_org_abs_2604_28025/figures/004_Figure_4.jpg]]
*Figure 4: Dataset Demonstration of the proposed LDPose-LimbLoss Evaluation Dataset. Representative samples illustrating the diversity of subjects, amputation levels, poses, activities, and environments included in the dataset. Green overlays indicate the manually annotated body masks used to isolate the human body region*

![[assets/figures/papers/paper_list_l1035_https_arxiv_org_abs_2604_28025/figures/008_Figure_7.jpg]]
*Figure 7: Key Statistics of our LDPose-LimbLoss Evaluation Dataset. (a) Distribution of residual-limb types, covering upper- and lower-limb amputations across both sides of the body. (b) Gender distribution. (c) Ethnic composition of the participants. Together, these statistics demonstrate the dataset’s demographic and impairment diversity, providing a representative foundation for benchmarking residual-limb–aware 2D/3D human pose and mesh reconstruction*

### 与AJAHR的对比：显式残端重建 vs 关节塌陷

**Figure 6** 将ResiHMR与AJAHR进行了对比。AJAHR通过将SMPL顶点塌陷至父关节来实现截肢表示，导致关节级截断。然而，专家验证证据和同一对象的额外真实图像显示，该个体存在明显的膝下残肢，关节塌陷无法匹配真实解剖结构。ResiHMR则显式估计解剖残端表面，生成更真实且具有临床可解释性的肢体终止形态。

### 补充图表

![[assets/figures/papers/paper_list_l1035_https_arxiv_org_abs_2604_28025/figures/002_Figure_2.jpg]]
*Figure 2: Failure cases of existing HMR methods on individuals with limb loss. SMPLify-X and HSMR hallucinate intact limbs or distort the lower body due to their intact-limb priors and fixed kinematic topologies. In contrast, ResiHMR correctly localizes the residual-limb, avoids compensatory distortions, and reconstructs an anatomically coherent body mesh*

![[assets/figures/papers/paper_list_l1035_https_arxiv_org_abs_2604_28025/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative Evaluation of ResiHMR. For each input example, we show: (a) the input image, (b) the overlay of SMPL-X in the input view, (c) front view, (d) back view, (e) side view, (f) T-Pose view with model output*

![[assets/figures/papers/paper_list_l1035_https_arxiv_org_abs_2604_28025/figures/007_Figure_6.jpg]]
*Figure 6: A visual comparison of AJAHR and ResiHMR (ours). (a,c) are copied from the AJAHR paper [8], where limb loss is represented by collapsing SMPL vertices toward the parent joint, resulting in joint-level truncation. (b) shows expert-verified evidence and an additional real image of the same individual revealing a clear below-knee residual limb, indicating that joint-level collapse fails to match the true anatomy. (d) shows ResiHMR reconstructions, including a normalized T-pose, with the residual limb highlighted in red (d1,d2). ResiHMR explicitly estimates the anatomical stump surface rather than collapsing geometry, producing a more realistic and clinically interpretable limb termination*

![[assets/figures/papers/paper_list_l1035_https_arxiv_org_abs_2604_28025/figures/009_Figure_8.jpg]]
*Figure 8: Limitation: Residual-limb surface shape approximation. Although ResiHMR accurately localizes the residual-limb endpoint, the reconstructed stump surface adopts a smooth, convex prior that does not fully reflect the subject’s true residuallimb contour (yellow). The intact limb is reconstructed faithfully (green), indicating that the discrepancy arises from limited instance-specific stump shape cues rather than errors in body alignment. This limitation reflects the absence of residual-limb 3D training data and highlights a natural growth direction toward modeling individualized residual-limb geometry*

![[assets/figures/papers/paper_list_l1035_https_arxiv_org_abs_2604_28025/figures/014_Figure_11.jpg]]
*Figure 11: Qualitative Comparison of ResiHMR with SOTA HMR methods. Please see this in GIF format in project page  ResiHMR*

## 方法谱系与知识库定位

### 问题定位：完整肢体先验的失效边界

现有单图像人体网格恢复（HMR）方法——无论是优化驱动还是回归驱动——均建立在**完整肢体拓扑**的默认假设之上。SMPLify-X（Pavlakos et al., CVPR 2019）通过拟合参数化人体模型到2D关键点来恢复3D姿态与形状，但其运动学骨架固定包含全部四肢关节，无法表示截肢后的残肢终点。HSMR基于SKEL生物力学骨架进行回归预测，同样内嵌了完整关节树先验。TokenHMR（CVPR 2024）、CameraHMR（3DV 2025）、PromptHMR（CVPR 2025）等最新回归方法虽然在通用场景下精度持续提升，但其架构设计从未考虑过肢体缺失的拓扑变异。

这一系统性盲区导致两类典型失败模式：**幻肢生成**——网络在缺失肢体位置强行输出完整肢体网格；**代偿性扭曲**——为匹配2D观测，模型将躯干或对侧肢体拉长、弯折以填补残肢区域的重投影误差。Figure 2中的定性对比清晰地展示了SMPLify-X和HSMR在这两类失败上的表现。

### ResiHMR的谱系定位：即插即用的拓扑适配层

ResiHMR并非一个独立的HMR方法，而是**作用于已有HMR输出之上的即插即用模块**。其设计哲学是：不替换现有HMR主干，而是在主干输出（SMPL-X参数：姿态$\theta$、形状$\beta$、全局变换$\mathbf{t}$）的基础上，通过后处理式的优化与几何操作，修正残肢区域的拓扑和几何表示。

这一设计选择具有明确的工程意义——ResiHMR与任何能输出SMPL-X参数的HMR管线兼容，包括优化类方法（如SMPLify-X）和回归类方法（如HSMR）。Table 1的结果验证了这一通用性：在SMPLify-X主干上，ResiHMR将Body Kpts 2D MPJPE从47.67 px降至41.77 px；在HSMR主干上，则从28.27 px降至24.75 px，两个主干均获得一致增益。

### 与同类截肢感知方法的对比

在截肢者人体重建这一细分方向上，ResiHMR的直接对比对象是**AJAHR**。AJAHR采用顶点坍缩策略——将残肢区域的SMPL顶点向其父关节收缩，从而在关节层级实现截断。Figure 6的对比揭示了这一策略的根本缺陷：关节级截断无法匹配真实的解剖截肢平面（如膝下截肢的残端位于小腿中段，而非膝关节处），且坍缩后的几何缺乏水密残端表面。

ResiHMR的关键区分点在于**显式建模残肢终点**。通过参数化残肢端点为锚点与上游关节连线上的连续点$\mathbf{R}_r = \mathbf{J}_a + \lambda_r (\mathbf{J}_t - \mathbf{J}_a)$，残肢长度$\lambda_r$成为可优化的连续变量，而非二值的"有关节/无关节"判定。Table 1中残肢端点2D MPJPE从73.61 px（HSMR的中点代理）骤降至23.19 px（ResiHMR），定量印证了这一设计优势。如原文Section 4.2所确认："ResiHMR is the only method that explicitly models residual-limb endpoints"，这解释了其在残肢定位上的大幅领先。

### 适用边界与局限

**适用前提**：ResiHMR依赖LDPose关键点格式中的8个残肢端点标注，以及SMPL-X的初始拟合质量。若初始拟合严重偏离（如极端遮挡或罕见姿态），后续的残肢锚点-因子优化可能收敛到次优解。此外，ResiHMR是完全基于优化的框架，不依赖训练数据，这一特性既是优势（零样本泛化），也是约束——无法从数据中学习残肢形状的统计先验。

**已知局限**：
1. **残肢表面形状近似**：残肢重建模块通过平面切割和边界密封生成光滑凸起的残端表面，但这一几何先验无法复现个体特异的不规则轮廓。Figure 8展示了这一差距：残端表面（黄色标注）的光滑凸形状与真实残肢轮廓存在可辨识偏差，而完好肢体（绿色标注）的重建则忠实于原图。该误差根源于缺乏残肢3D训练数据，而非身体对齐失败。
2. **单目深度歧义**：单张RGB图像固有的深度模糊性在侧视角度尤为突出。Figure 9显示，尽管前视角度下网格与图像对齐良好，侧视图却暴露出手臂前伸误置于躯干前方、上身前屈未被正面视角捕捉等问题。这类歧义源于2D标注和健康人体先验无法提供充分的3D约束。
3. **缺乏3D真值监督**：当前优化仅依赖2D重投影误差和人体测量先验（节段长度保持），没有残肢3D几何的真值数据。这限制了精细解剖重建的上限。

### 开放问题

从ResiHMR的局限出发，可识别以下开放方向：

- **3D残肢数据集的构建**：多视角或标记点捕获系统可提供残肢3D几何真值，为监督式方法奠定基础，同时支持标准化评估。
- **学习驱动的残肢形状先验**：生成模型或扩散模型有望从大规模截肢者图像中学习个体化的残肢软组织形变和截肢界面形态，减少对光滑凸先验的依赖。
- **复杂肢体畸形的扩展**：当前框架假设残肢沿肢体轴线截断，对于先天性肢体畸形或高度不规则的截肢界面，需要更灵活的拓扑表示和几何建模。
- **临床下游应用**：重建的残端表面在假肢接受腔适配、步态分析和截肢者康复评估中具有潜在价值，但需要验证重建精度是否满足临床生物力学要求。

## 原文 PDF

![[paperPDFs/CVPR_2026/ResiHMR_Residual_Limb_Aware_Single_Image_3D_Human_Mesh_Recovery_for_Individuals_with_Limb_Loss.pdf]]