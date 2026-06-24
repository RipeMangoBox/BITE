---
title: Scene-aware Human Motion Forecasting via Mutual Distance Prediction
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/MutualDistance_Scene_aware_Human_Motion_Forecasting_via_Mutual_Distance_Prediction.pdf
aliases:
- MDBSAHMF
- SAHMFMDP
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 互距离表示（结合逐顶点符号距离和逐基点距离）能够同时约束局部姿态和全局位置。
primary_logic: 通过先预测未来的互距离作为显式约束，再生成运动，可以更准确地捕捉人景交互，显著提高运动预测的准确性和合理性。
claims:
- 消融实验表明，加入互距离约束相比仅使用场景编码（Scene only）在路径和姿态误差上均有显著下降。
- 在 GTA-IM 和 PROX 数据集上，本文方法均优于所有基线方法，尤其在路径误差上提升显著。
- 使用预测的互距离进行运动预测，比基线方法更接近真实运动，且在消融中去除互距离后运动预测质量明显下降。
- GTA-IM 上 Path Error (mm) = 72.0
---

# Scene-aware Human Motion Forecasting via Mutual Distance Prediction

> [!tip] 核心洞察
> 通过先预测未来的互距离作为显式约束，再生成运动，可以更准确地捕捉人景交互，显著提高运动预测的准确性和合理性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过互距离预测的场景感知人体运动预测 |
| 英文题名 | Scene-aware Human Motion Forecasting via Mutual Distance Prediction |
| 会议/期刊 | ECCV 2024 |
| Links |  [paper](https://doi.org/10.1145/3680528.3687565)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Mutual Distance-based Scene-aware Human Motion Forecasting |
| Dataset | GTA-IM, HUMANISE |

> [!tip] 效果简介
> - GTA-IM 上，Path Error (mm) 72.0 vs ContAware (higher) (significant reduction)。
> - HUMANISE (seen) 上，Path Error (mm) 45.6 vs 52.6 (Scene only) (-7.0)。

## 概述

**问题瓶颈**：现有场景感知人体运动预测方法仅对部分身体运动施加约束，例如只约束接触关节或全局位置，无法对全身运动形成完整约束，导致预测结果出现穿透场景、幽灵运动等不合理现象。

**核心思想**：本文提出一种**互距离（Mutual Distance）** 表示，由两个互补组件构成——人体网格顶点到场景表面的**逐顶点符号距离**（per-vertex signed distance）和场景基点到人体网格表面的**逐基点距离**（per-basis point distance）。该表示能够同时约束局部姿态和全局位置，从而更准确地捕捉人-景交互关系。

**方法定位**：本文方法采用**两阶段训练策略**——先预测未来的互距离作为显式约束，再基于预测的距离自回归地生成未来运动，最后进行联合微调。相比现有方法（如 **ContAware**（Mao et al., NeurIPS 2022）使用接触图、**GIMO**（Zheng et al., ECCV 2022）使用视线信息），互距离约束为全身运动提供了更完整的监督信号。

**主要结果**：在 GTA-IM 和 PROX 数据集上，本文方法在所有指标上均优于现有基线方法，尤其在路径误差上有显著提升。在 HUMANISE 数据集上，无论是已见场景还是未见场景，本文方法均取得最优结果。消融实验进一步验证了互距离表示的有效性：移除互距离约束后运动预测质量明显下降，且逐顶点符号距离和逐基点距离各自独立贡献，两者联合使用效果最佳。

## 背景与动机

### 问题背景

预测人类在未来时刻的运动是计算机视觉与图形学中的核心任务，在自动驾驶、人机交互、AR/VR 等领域有广泛应用。当人类在三维场景中活动时，其运动不仅受自身动力学支配，更受到场景几何的严格约束——例如，人不能穿墙而过，坐下时臀部必须接触椅子表面。因此，**场景感知的人体运动预测**（scene-aware human motion forecasting）要求模型在给定历史人体姿态序列和三维场景信息的条件下，生成物理上合理且符合场景约束的未来运动序列。

### 现有方法缺口：局部约束不足以约束全身运动

现有场景感知方法在约束人景交互时存在一个关键瓶颈：**它们仅对部分身体运动施加约束，而非对全身运动提供完整约束**。具体而言：

- **接触约束方法**（如 **ContAware**，Mao et al., NeurIPS 2022）仅显式建模人体与场景的接触关节或接触区域，对非接触身体部位缺乏有效约束，导致预测中出现穿透场景或“幽灵运动”等不合理结果。
- **视线引导方法**（如 **GIMO**，Zheng et al., ECCV 2022）利用注视信息推断未来意图，但视线本身并不直接约束全身的空间位置，难以保证运动在几何上的一致性。
- **分阶段全局预测方法**（如 **STAG**，Scofano et al., BMVC 2023）先预测全局轨迹再生成局部姿态，但全局轨迹的约束同样仅作用于根节点，无法保证全身各部位与场景的合理交互。

上述方法的共同缺陷在于：**缺乏一种能够同时约束局部姿态和全局位置的统一表示**。当约束仅覆盖身体的部分自由度时，模型在其余自由度上容易产生漂移，导致预测结果在物理和几何上均不可靠。这一瓶颈构成了本文的核心研究动机。

### 本文动机：互距离作为显式约束

本文的核心洞察是：**如果能在预测未来运动之前，先显式地预测人体与场景之间的互距离（mutual distance），再将此距离作为约束条件来生成运动，就可以更准确地捕捉人景交互，显著提升运动预测的准确性和合理性。**

互距离表示由两个互补的分量构成（见 Fig. 1）：

1. **逐顶点符号距离（per-vertex signed distance）**：人体网格上每个顶点到场景表面的带符号最近距离。当顶点位于场景内部时距离为负，外部时为正。该分量从人体视角出发，约束每个身体部位相对于场景的位置。
2. **逐基点距离（per-basis point distance）**：场景表面采样基点到人体网格表面的最小距离。该分量从场景视角出发，约束场景各区域与人体的空间关系。

这两个分量共同构成**双向、全身的人景交互约束**——既约束人体不穿透场景，也约束人体不过度远离场景交互区域。与仅关注接触关节或全局位置的方法不同，互距离对全身所有顶点和场景关键区域均施加显式约束，从根本上解决了“局部约束导致全身运动不合理”的问题。

基于此动机，本文提出**基于互距离预测的场景感知人体运动预测方法**：先预测未来的互距离，再以预测的互距离为条件自回归地生成未来人体姿态，从而实现对全身运动的完整场景约束。

## 核心创新

### 问题瓶颈：从局部约束到全局缺失

现有场景感知人体运动预测方法仅对部分身体运动施加约束，无法为全身运动提供完整、一致的场景交互引导。例如，**ContAware** (Mao et al., NeurIPS 2022) 仅通过接触图约束接触关节，**GIMO** (Zheng et al., ECCV 2022) 依赖注视信息，**STAG** (Scofano et al., BMVC 2023) 分阶段约束全局位置。这些局部约束导致预测运动出现穿透场景、幽灵漂浮等不合理现象——根本原因在于，缺乏一种能够同时约束局部姿态与全局位置的统一表示。

### 核心因果开关：互距离表示

本文的核心创新在于提出**互距离（Mutual Distance）**作为人-景交互的统一约束表示。该表示由两个互补组件构成：

1. **逐顶点符号距离（Per-vertex Signed Distance）**：从人体网格采样顶点到场景表面的带符号最近距离。当顶点位于场景内部（如脚踩地面）时距离为负，位于外部时为正。该组件精细约束人体各部位与场景的相对位置，直接防止穿透。

2. **逐基点距离（Per-basis Point Distance）**：从场景表面采样的基点到人体网格表面的最小距离。该组件从场景视角感知人体占据，约束全局位置，防止人体远离场景的“幽灵运动”。

两个组件形成**双向距离约束**——人体到场景、场景到人体——从而为全身运动提供完整的交互引导。

### 方法范式转变：先预测约束，再生成运动

与基线方法直接端到端预测运动不同，本文引入**两阶段范式**：

- **阶段一**：基于历史运动与场景编码，通过 DCT-GCN 网络**先预测未来的互距离序列**（包括逐顶点符号距离和逐基点距离），作为显式交互约束。
- **阶段二**：以预测的互距离为条件，通过 RNN 自回归地生成未来人体姿态。

这一范式转变的关键洞察在于：**互距离作为人-景交互的紧凑中间表示，比直接映射到高维姿态空间更容易学习**。消融实验证实，端到端训练容易陷入局部最小值，而分阶段训练显著提升性能（Table 3）。

### 场景表示升级：SDF Volume 替代点云

基线方法（如 ContAware）通常使用点云表示场景，信息稀疏且缺乏连续距离场。本文改用**符号距离场体素（SDF Volume）**，通过 3D CNN 编码为全局场景特征。SDF Volume 提供连续、稠密的距离信息，使互距离计算和预测更加精确。消融实验表明，SDF Volume 优于点云表示和占用表示（Table 3）。

### 创新点总结

| 创新维度 | 基线方法 | 本文方法 |
|---------|---------|---------|
| 交互约束 | 局部（接触图、注视） | 全局双向（互距离） |
| 约束范围 | 部分关节/位置 | 全身运动 |
| 预测范式 | 端到端直接预测运动 | 先预测互距离，再生成运动 |
| 场景表示 | 点云 | SDF Volume |
| 训练策略 | 端到端 | 分阶段训练 + 端到端微调 |

## 整体框架

本文提出一种**基于互距离预测的场景感知人体运动预测框架**，核心思路是将“人-景交互”显式建模为可预测的互距离表示，再以此作为约束条件生成未来运动。整个 pipeline 由四个主要模块串联构成，遵循“编码→预测→生成”的信息流。

### 输入与输出定义

给定一段观测到的人体姿态序列 $\mathbf{X} = [\mathbf{x}_1, \mathbf{x}_2, ..., \mathbf{x}_T] \in \mathbb{R}^{M \times T}$（共 $T$ 帧，每帧姿态 $\mathbf{x}_t$ 为 $M$ 维向量）以及对应的三维场景 $\mathbf{S}$，目标是预测未来 $U$ 帧的姿态序列 $\mathbf{Y} = [\mathbf{x}_{T+1}, \mathbf{x}_{T+2}, ..., \mathbf{x}_{T+U}] \in \mathbb{R}^{M \times U}$。

### 模块关系与数据流

如 **Fig. 2** 所示，整个框架包含以下四个核心模块，数据按顺序流经：

![[assets/figures/papers/paper_list_l1764_MutualDistance_Scene_aware_Human_Motion_Forecasting_via_Mutual_Distance/figures/003_Figure_2.jpg]]
*Figure 2: Network architecture. Given the 3D scene S represented as a signed distance volume and the past motion X shown in grey meshes, our approach first predicts the future per-vertex signed distance Dˆ , and the future per-basis point distance Bˆ from historical distance D and B, respectively. The two predicted future distances are then fed into a RNN-based network to predict the future motion Yˆ shown in orange meshes*

1. **Scene Encoder（场景编码器）**  
   将三维场景 $\mathbf{S}$ 表示为**带符号距离场（SDF）体素**，通过 3D CNN 提取全局场景特征 $\mathcal{G}_s(\mathbf{S})$。消融实验表明，SDF 体素表示在路径误差和姿态误差上均优于点云表示和占用表示（Table 3）。

2. **Past Motion Encoder（历史运动编码器）**  
   对观测姿态序列 $\mathbf{X}$ 进行编码，得到历史运动特征 $\mathcal{G}_x(\mathbf{X})$。论文采用 RNN 类结构实现时序建模。

3. **Mutual Distance Predictor（互距离预测器）**  
   这是整个框架的**核心创新模块**。它基于 DCT-GCN 网络，从历史互距离序列预测未来的互距离，包括：
   - 未来逐顶点符号距离 $\hat{\mathbf{D}} = [\hat{d}_{k,T+1}, ..., \hat{d}_{k,T+U}]$（人体网格顶点到场景表面的带符号最近距离）；
   - 未来逐基点距离 $\hat{\mathbf{B}} = [\hat{b}_{p,T+1}, ..., \hat{b}_{p,T+U}]$（场景基点到人体网格表面的最小距离）。  
   该模块使用平均 L1 损失进行训练：
   $$\ell_{\mathrm{dist}} = \frac{1}{(T+U)} \left( \frac{1}{K} \sum_{t=1}^{T+U} \sum_{k=1}^{K} |\hat{d}_{kt} - d_{kt}| + \frac{1}{P} \sum_{t=1}^{T+U} \sum_{p=1}^{P} |\hat{b}_{pt} - b_{pt}| \right)$$

4. **Motion Forecaster（运动预测器）**  
   基于 RNN 的自回归生成模型，在每一未来时刻 $u$，根据上一帧预测姿态 $\hat{\mathbf{x}}_{T+u-1}$、当前帧预测的互距离 $(\hat{\mathbf{d}}_{T+u}, \hat{\mathbf{b}}_{T+u})$、以及历史运动编码 $\mathcal{G}_x(\mathbf{X})$ 和场景编码 $\mathcal{G}_s(\mathbf{S})$，预测当前帧姿态：
   $$\hat{\mathbf{x}}_{T+u} = \mathcal{G}_y(\hat{\mathbf{x}}_{T+u-1}, \hat{\mathbf{d}}_{T+u}, \hat{\mathbf{b}}_{T+u}, \mathcal{G}_x(\mathbf{X}), \mathcal{G}_s(\mathbf{S}))$$

### 训练策略：分阶段训练

与基线方法（如 **ContAware** (Mao et al., NeurIPS 2022)、**GIMO** (Zheng et al., ECCV 2022)）的端到端训练不同，本文采用**三阶段训练策略**：
- **第一阶段**：独立训练互距离预测网络（Mutual Distance Predictor）；
- **第二阶段**：固定互距离预测器，独立训练运动预测网络（Motion Forecaster）；
- **第三阶段**：将两个网络联合，进行端到端微调。

消融实验（Table 3）表明，分阶段训练策略优于直接端到端学习（e2e），后者容易陷入局部最小值。

### 关键设计动机

现有场景感知方法（如 ContAware 的接触图约束、GIMO 的凝视信息）仅约束部分身体运动，无法对全身运动提供完整约束，导致预测中出现穿透场景或“幽灵运动”等不合理结果。本文通过**互距离表示**（同时约束局部姿态和全局位置）解决了这一瓶颈——消融实验中，移除互距离约束后运动预测质量显著下降（Fig. 4），而完整模型在 GTA-IM 和 PROX 数据集上均显著优于所有基线方法（Table 1）。

## 核心模块与公式推导

### 互距离表示

本文的核心创新在于提出**互距离（Mutual Distance）** 表示，用于同时约束人体运动的局部姿态和全局位置。互距离由两个互补的组件构成：

**逐顶点符号距离（Per-vertex Signed Distance）**：从人体网格上采样的 $K$ 个顶点出发，计算其到场景表面 $\partial S$ 的带符号最近距离。符号指示顶点位于场景内部（负）还是外部（正）：

$$d_{kt} = \begin{cases} -\min_{\mathbf{y} \in \partial S} \|\mathbf{v}_{tk} - \mathbf{y}\|_2 & \text{if } \mathbf{v}_{tk} \in S \\ \min_{\mathbf{y} \in \partial S} \|\mathbf{v}_{tk} - \mathbf{y}\|_2 & \text{if } \mathbf{v}_{tk} \notin S \end{cases}$$

其中 $\mathbf{v}_{tk}$ 为时刻 $t$ 人体网格上第 $k$ 个采样顶点的位置，$S$ 为场景内部区域。

**逐基点距离（Per-basis Point Distance）**：从场景中采样的 $P$ 个基点到人体网格表面 $\partial \mathcal{H}_t$ 的最小距离：

$$b_{pt} = \min_{\mathbf{y} \in \partial \mathcal{H}_t} \|\mathbf{p}_p - \mathbf{y}\|_2$$

其中 $\mathbf{p}_p$ 为第 $p$ 个场景基点的位置。

这两个组件从不同方向刻画人-景空间关系：逐顶点符号距离约束人体各部位与场景的接近程度及穿透状态，逐基点距离则从场景视角约束人体整体位置。二者结合形成对全身运动的完整空间约束。

### 互距离预测网络

互距离预测网络采用 **DCT-GCN** 架构，分为时域建模和空域建模两个环节：

**离散余弦变换（DCT）** 用于将时域距离序列转换到频域，捕获时序模式。对于第 $k$ 个顶点的历史符号距离序列，其第 $l$ 个 DCT 系数为：

$$h_{kl} = \sqrt{\frac{2}{T}} \sum_{t=1}^{T} d_{tk} \frac{1}{\sqrt{1+\delta_{l1}}} \cos\left(\frac{\pi}{2T}(2t-1)(l-1)\right)$$

其中 $\delta_{ij}$ 为 Kronecker delta 函数。DCT 将长度为 $T$ 的历史序列压缩为低频系数，再通过逆 DCT 解码出未来 $U$ 帧的距离预测值。

**图卷积网络（GCN）** 用于建模不同顶点/基点之间距离序列的空间依赖关系。GCN 层的传播公式为：

$$\mathbf{F}^{(n+1)} = \sigma(\mathbf{A}^{(n)} \mathbf{F}^{(n)} \mathbf{W}^{(n)}) \mathbf{\Lambda}$$

其中 $\mathbf{A}^{(n)}$ 为可学习的邻接矩阵，$\mathbf{F}^{(n)}$ 为第 $n$ 层的节点特征，$\mathbf{W}^{(n)}$ 和 $\mathbf{\Lambda}$ 为可训练参数。

互距离预测网络的训练使用平均 L1 损失，同时监督逐顶点和逐基点距离的预测：

$$\ell_{\mathrm{dist}} = \frac{1}{(T+U)} \left( \frac{1}{K} \sum_{t=1}^{T+U} \sum_{k=1}^{K} |\hat{d}_{kt} - d_{kt}| + \frac{1}{P} \sum_{t=1}^{T+U} \sum_{p=1}^{P} |\hat{b}_{pt} - b_{pt}| \right)$$

### 运动预测网络

运动预测网络以自回归方式生成未来人体姿态序列。给定场景编码器 $\mathcal{G}_s$ 提取的 SDF 体积特征、历史运动编码器 $\mathcal{G}_x$ 提取的过去姿态特征，以及预测的未来互距离 $\hat{\mathbf{d}}_{T+u}$ 和 $\hat{\mathbf{b}}_{T+u}$，第 $u$ 帧的未来姿态通过 RNN 解码器 $\mathcal{G}_y$ 逐步预测：

$$\hat{\mathbf{x}}_{T+u} = \mathcal{G}_y(\hat{\mathbf{x}}_{T+u-1}, \hat{\mathbf{d}}_{T+u}, \hat{\mathbf{b}}_{T+u}, \mathcal{G}_x(\mathbf{X}), \mathcal{G}_s(\mathbf{S}))$$

该自回归过程将预测的互距离作为显式空间约束注入每一帧的姿态生成，使得运动预测始终保持在合理的人-景交互范围内。

### 训练策略

为规避端到端训练容易陷入局部最小值的问题（消融实验 Table 3 中 e2e 变体性能显著下降），本文采用**分阶段训练**策略：首先独立训练互距离预测网络和运动预测网络，随后将两个网络联合进行端到端微调。

### 补充图表

![[assets/figures/papers/paper_list_l1764_MutualDistance_Scene_aware_Human_Motion_Forecasting_via_Mutual_Distance/figures/002_Figure_1.jpg]]
*Figure 1: Our mutual distances. a) shows the per-vertex signed distance for sampled vertices on human mesh. Their color indicates the distance value. b) shows the perbasis point distance for the basis points which are not sampled on the scene surface. For both figures, the darker the color is, the smaller the distance is*

## 实验与分析

### 1. 实验设置

**数据集与基线**。本文在四个具有代表性的场景感知人体运动数据集上进行评估：GTA-IM、PROX、HUMANISE 和 GIMO。其中，HUMANISE 提供了 seen/unseen 场景划分，用于检验模型的泛化能力。基线方法覆盖了该领域近年的代表性工作：基于接触图的 **ContAware**（Mao et al., NeurIPS 2022）、基于凝视信息的 **GIMO**（Zheng et al., ECCV 2022），以及分阶段接触感知全局运动预测方法 **STAG**（Scofano et al., BMVC 2023）。

**评价指标**。采用两个核心指标衡量预测质量：（1）路径误差（Path Error），即预测轨迹与真实轨迹平移分量的 L2 距离，反映全局定位精度；（2）姿态误差（Pose Error），即局部姿态的 MPJPE，反映身体动作的准确性。所有方法在相同的数据划分和评价协议下进行比较，确保公平性。

**训练策略**。本文采用分阶段训练策略：首先分别训练互距离预测网络和运动预测网络，随后将两者合并进行端到端微调。消融实验将验证该策略相对于直接端到端训练的优势。

---

### 2. 主要结果

**Table 1** 展示了在 GTA-IM 和 PROX 数据集上的定量对比。本文方法在所有指标上均优于已有基线方法，尤其在路径误差上提升显著——在 GTA-IM 上路径误差降至 72.0 mm，相比 ContAware 等基线有大幅降低。这一结果表明，互距离约束能够有效改善全局运动轨迹的预测精度。

**Table 2** 报告了 HUMANISE 数据集上的结果。无论是在 seen 场景还是 unseen 场景，本文方法均一致优于所有基线。值得注意的是，在 unseen 场景上的优势并未明显衰减，说明互距离表征具有一定的场景泛化能力，而非仅仅过拟合于训练场景的几何特征。

**Fig. 3** 提供了与基线方法的可视化对比。在 GTA-IM、PROX 和 HUMANISE 三个数据集上，本文方法预测的未来运动均更接近真实运动（Ground Truth）。相比之下，基线方法在长时间预测中容易出现漂移或与场景几何不一致的姿态（如穿透、悬空）。

---

### 3. 消融实验

**Table 3** 系统性地分解了本文方法各组件在 HUMANISE 上的贡献，核心发现如下：

**互距离约束的核心作用**。移除互距离后（Scene only），路径误差从 45.6 mm 上升至 52.6 mm，姿态误差同样显著增加。这直接验证了互距离作为显式约束对运动预测质量的关键贡献——仅使用场景编码不足以提供充分的人景交互信息。

**两种距离分量的互补性**。单独使用逐顶点符号距离（D）或逐基点距离（B）均能带来性能提升，但同时使用两者（D+B）达到最优效果。这表明两类距离从不同角度刻画人景关系：逐顶点距离约束身体局部与场景的接近程度，逐基点距离约束场景关键点与人体的空间关系，二者互为补充。

**场景表示的影响**。SDF volume 场景表示优于点云（P）和占用表示（O），验证了符号距离场在刻画场景几何细节和提供梯度信息方面的优势。此外，BPS 编码的性能不如本文的逐基点距离，说明基于学习的人景距离表征比手工设计的场景编码更有效。

**训练策略的收益**。分阶段训练（separate + fine-tune）优于直接端到端学习（e2e）。端到端训练容易陷入局部最小值，使得互距离预测和运动生成两个子任务无法充分解耦学习；先分别训练再联合微调能够为两者提供更好的初始化。

**可视化验证**。**Fig. 4** 展示了互距离消融的可视化结果。以“站起”动作为例，完整模型预测的逐顶点符号距离和逐基点距离与真实值高度吻合，运动预测自然合理；而去除互距离后，模型无法准确恢复人景空间关系，导致动作失真（如身体与场景的相对位置偏离）。该图直观地揭示了互距离预测精度与运动生成质量之间的因果链条。

---

### 4. 失败模式与局限性

尽管本文方法在定量和定性结果上均表现出色，但仍存在若干值得关注的局限：

**互距离预测精度瓶颈**。运动预测的质量高度依赖于互距离的预测精度。当场景几何复杂或运动幅度较大时，互距离预测网络可能产生误差，进而传导至运动生成阶段，导致预测姿态偏离真实值。如何进一步提高互距离预测的准确性，是该方法持续改进的关键方向。

**物理约束缺失**。当前框架未显式建模真实世界的物理约束（如接触力、动量守恒、穿透惩罚等）。在某些极端姿态下，预测结果可能出现不合理的力分布或微小的物理不一致。这在人机交互等对安全性和稳定性要求较高的实际部署场景中可能构成隐患。

**长时预测的漂移**。尽管本文方法在路径误差上提升显著，但自回归预测框架在长时预测中仍存在误差累积问题。随着预测步长增加，姿态误差逐渐增大，这是该领域的共性挑战，本文方法并未从根本上解决该问题。

---

### 5. 小结

实验结果表明，互距离表征通过同时约束局部姿态和全局位置，有效解决了现有方法仅部分约束身体运动导致的预测不合理问题。在多个数据集上的一致优势、消融实验中各组件的清晰贡献，以及可视化分析中互距离与运动质量的因果关联，共同构成了支持本文核心主张的强证据链。未来的改进方向包括提升互距离预测精度和引入显式物理约束。

### 补充图表

![[assets/figures/papers/paper_list_l1764_MutualDistance_Scene_aware_Human_Motion_Forecasting_via_Mutual_Distance/figures/004_Table_1.jpg]]
*Table 1: Quantitative results on GTA-IM [4] and PROX [10]. Our model outperforms all baselines at all metrics, especially for the path error*

![[assets/figures/papers/paper_list_l1764_MutualDistance_Scene_aware_Human_Motion_Forecasting_via_Mutual_Distance/figures/005_Table_2.jpg]]
*Table 2: Quantitative results on HUMANISE [36]. Our model outperforms all baselines on both seen scenes and unseen scenes*

![[assets/figures/papers/paper_list_l1764_MutualDistance_Scene_aware_Human_Motion_Forecasting_via_Mutual_Distance/figures/006_Table_3.jpg]]
*Table 3: Ablation study on HUMANISE [36]. We show the ablation results of our model. D, B, P , O, BP S and e2e indicate per-vertex signed distance, per-basis point distance, point cloud representation, occupancy representation, BPS encoding and end-to-end training respectively*

![[assets/figures/papers/paper_list_l1764_MutualDistance_Scene_aware_Human_Motion_Forecasting_via_Mutual_Distance/figures/007_Figure_3.jpg]]
*Figure 3: This figure compares our method with baseline models on GTA-IM [4] (top row), PROX [10] (middle row), and HUMANISE [36] (bottom row). Our method predicts future motion closer to the ground truth*

![[assets/figures/papers/paper_list_l1764_MutualDistance_Scene_aware_Human_Motion_Forecasting_via_Mutual_Distance/figures/008_Figure_4.jpg]]
*Figure 4: Ablation of the mutual distance. The three figures in the first three columns (from left to right) depict the ground truth pose for the last frame of future motion, results of our full model, and predictions of our model without mutual distance constraint. The sub-figure in gray is the last observed frame. Other sub-figures depict the predicted middle frame. The blue dot is the scene basis point, and the red dot is the sampled vertex on human mesh. The two graphs in the last two columns show the predicted per-vertex signed distance and the per-basis point distance for the red and blue point, respectively. As shown in the figures, with predicted mutual distance, we can forecast the ’stand-up...*

## 方法谱系与知识库定位

### 核心瓶颈与因果旋钮

现有场景感知人体运动预测方法普遍存在一个关键瓶颈：它们仅对部分身体运动施加约束，例如仅约束接触关节或全局位置，而无法对全身运动提供完整约束。这导致预测结果中出现穿透场景、幽灵运动等不合理现象。本文识别出的因果旋钮是**互距离表示**——通过同时建模逐顶点符号距离（per-vertex signed distance）和逐基点距离（per-basis point distance），能够对局部姿态和全局位置施加联合约束。核心洞察在于：先显式预测未来的互距离作为中间约束，再以其为条件生成运动，可以更准确地捕捉人-景交互，从而显著提升运动预测的准确性和合理性。

### 与基线方法的关系

本文方法在场景感知人体运动预测这一任务线上，与三类代表性基线形成直接对比：

- **ContAware**（Mao et al., NeurIPS 2022）：当前最先进的接触感知运动预测方法，使用接触图（contact map）作为人-景交互表示。本文将其作为主要对比基线，在 GTA-IM 和 PROX 数据集上均取得显著更优的路径误差和姿态误差（Table 1）。
- **GIMO**（Zheng et al., ECCV 2022）：基于注视信息（gaze）的人体运动预测方法。本文在可视化对比（Fig. 3）中展示了该方法在复杂交互场景下的预测偏差。
- **STAG**（Scofano et al., BMVC 2023）：分阶段接触感知全局人体运动预测方法。作为同期工作，本文在 HUMANISE 数据集上与其进行了定量和定性对比（Table 2, Fig. 3）。

本文相对于上述基线的关键改动槽位包括：

| 改动槽位 | 基线取值 | 本文取值 | 证据锚点 |
|---------|---------|---------|---------|
| 人-景交互表示 | 接触图（ContAware）、注视信息（GIMO） | 互距离（逐顶点符号距离 + 逐基点距离） | Section 3.1, Fig. 1 |
| 场景表示 | 点云（ContAware） | SDF volume | Section 3, Table 3 |
| 训练策略 | 端到端训练 | 两阶段训练（先互距离预测，再运动预测，最后联合微调） | Section 3.2-3.3, Implementation details |

消融实验（Table 3）验证了每个改动槽位的有效性：SDF volume 场景表示优于点云和占用表示；分阶段训练优于直接端到端学习，后者容易陷入局部最小值。

### 方法适用边界

1. **对互距离预测精度的依赖**：运动预测质量直接受互距离预测精度影响。本文明确指出，提高互距离预测可以进一步改善运动预测，这意味着在互距离预测困难的场景（如高度动态或遮挡严重的交互）中，整体性能可能受限。
2. **物理约束缺失**：模型未显式建模真实世界物理约束（如接触力、动量守恒），预测结果中可能出现不合理的力分布。在实际部署场景（如人机交互、机器人规划）中，这可能产生不稳定或不安全的运动。这是该方法从感知驱动预测走向物理合理生成的关键差距。
3. **数据集覆盖范围**：实验在 GTA-IM、PROX、HUMANISE 和 GIMO 四个数据集上进行，涵盖合成和真实场景。HUMANISE 上的 unseen 场景测试（Table 2）表明方法具有一定泛化能力，但所有数据集均以室内场景为主，对室外或开放场景的适用性需要进一步验证。

### 局限与开放问题

**已知局限**：
- 运动预测质量依赖于互距离的预测精度，当前框架未对互距离预测本身的误差传播进行显式建模或鲁棒处理。
- 缺乏物理约束导致预测运动可能在力学上不合理，限制了其在安全关键应用中的部署。

**开放问题**：
1. 如何进一步提高互距离（尤其逐顶点符号距离和逐基点距离）的预测精度？是否可以通过多尺度表示、时序注意力机制或物理引导的损失函数来改善？
2. 能否将显式物理约束（如接触力、动量守恒、地面反作用力）融入当前两阶段框架，以生成更符合物理规律的运动？这可能需要引入可微分物理模拟器或物理感知的损失项。
3. 互距离表示是否可以推广到多人与动态场景的交互预测中？当前方法假设静态场景和单人运动，扩展到多智能体动态交互是一个自然但非平凡的延伸方向。

## 原文 PDF

![[paperPDFs/ECCV_2024/MutualDistance_Scene_aware_Human_Motion_Forecasting_via_Mutual_Distance_Prediction.pdf]]