---
title: "TESO: Online Tracking of Essential Matrix by Stochastic Optimization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TESO_Online_Tracking_of_Essential_Matrix_by_Stochastic_Optimization.pdf
project_link: null
code_link: null
aliases:
- TESO
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 核相关损失函数中的 σ 参数（控制吸引盆宽度与跟踪精度的权衡）以及在线随机优化中基于期望梯度/方差的自适应学习率机制。
primary_logic: 通过核化极线误差隐式鲁棒化损失函数，消除了对特定特征匹配质量和显式外点剔除的依赖，使得轻量级的在线随机优化即可在本质矩阵流形上自适应跟踪参数；结合校正精度与深度一致性指标可全面评估并揭示标定参数的不一致性。
claims:
- TESO 在 CARLA‑Drift 数据集上将旋转跟踪精度提升至 X/Z 轴 <0.02°、Y 轴 0.039°，相比无跟踪大幅降低漂移。
- 核化损失函数的差分进化优化在 CARLA‑FlowGuided 上取得与最佳端到端学习方法竞争的结果，无需针对新数据集训练。
- 核化损失函数使关键点检测器和特征提取器的选择不再关键，SuperGlue 与 SIFT 搭配核损失时性能接近。
- 使用重新标定的 KITTI 内参后，TESO 的 Y 轴旋转精度提升 20 倍至 0.025°，深度一致性提升 50 倍。
---

# TESO: Online Tracking of Essential Matrix by Stochastic Optimization

> [!tip] 核心洞察
> 通过核化极线误差隐式鲁棒化损失函数，消除了对特定特征匹配质量和显式外点剔除的依赖，使得轻量级的在线随机优化即可在本质矩阵流形上自适应跟踪参数；结合校正精度与深度一致性指标可全面评估并揭示标定参数的不一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于随机优化的本质矩阵在线跟踪方法 |
| 英文题名 | TESO: Online Tracking of Essential Matrix by Stochastic Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.19420) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | TESO |
| Dataset | CARLA‑Drift, KITTI, MAN TruckScenes |

> [!tip] 效果简介
> - CARLA‑Drift 上，Rx MAE [°] 0.011 vs 0.157 (-0.146)；Ry MAE [°] 0.039 vs 0.166 (-0.127)；Rz MAE [°] 0.015 vs 0.175 (-0.160)。
> - KITTI (00‑01, recalibrated intrinsics ) 上，Ry [°] 0.025 vs ~0.489 (original) (~-0.464)。
> - MAN TruckScenes (Calibrated) 上，Ry [°] 0.115 vs 0 (reference) (0.115)。

## 概述

立体相机的在线标定是自动驾驶与机器人感知系统的关键环节。机械振动、温度变化或冲击等因素会导致相机外参随时间发生缓慢漂移，使得离线标定参数逐渐失效，进而严重退化深度估计与立体匹配的精度。传统应对方案依赖 RANSAC 等显式外点剔除机制、鲁棒估计器或端到端学习的校正模型，但在数据变异性大、信息内容低的在线场景中难以同时满足快速收敛与稳定跟踪的需求。

TESO 针对这一瓶颈提出了一种**无需训练、无需显式外点剔除**的在线本质矩阵跟踪方法。其核心思想是通过**核化极线误差**隐式地鲁棒化损失函数——利用双向 k 近邻描述子匹配与高斯核构建的损失景观，天然抑制外点对梯度估计的干扰，从而消除了对特定特征匹配质量与置信度阈值的依赖。在此基础上，TESO 采用**自适应在线随机二阶优化**直接在本质矩阵的 5 自由度流形上更新参数，通过期望梯度、方差与 Hessian 对角线的指数移动平均估计，动态调整记忆大小与步长，在拟牛顿方向与梯度下降之间平滑切换。

实验表明，TESO 在 CARLA‑Drift 合成漂移数据集上将三轴旋转跟踪精度提升至 X/Z 轴 <0.02°、Y 轴 0.039°，相比无跟踪基线降低了一个数量级的误差（Table 1a）；同时，核化损失函数的差分进化优化在 CARLA‑FlowGuided 数据集上取得了与最佳端到端学习方法竞争的结果，而无需针对新数据集重新训练（Table 4）。在重新标定内参后的 KITTI 序列上，TESO 将 Y 轴旋转精度提升约 20 倍至 0.025°，深度一致性指标改善约 50 倍，揭示了内参精度对外参跟踪评估的显著影响。消融实验进一步证实，核化损失使关键点检测器与特征提取器的选择不再关键——SIFT 与 SuperGlue 搭配核损失时性能接近（Figure 4）——且跟踪器延迟小于一帧，CPU 实现每帧约 86 ms，与最快的 SotA 方法耗时相当。

TESO 的主要局限在于平移自由度在典型远距离驾驶场景中仅能达到厘米级精度，且在低光照、雾天、隧道等条件下因 SIFT 关键点退化导致跟踪性能显著下降。当前实现仅跟踪本质矩阵的 5 个旋转相关自由度，尚未将焦距等内参纳入在线优化框架。

## 背景与动机

立体相机系统被广泛部署于自动驾驶、移动机器人与三维重建等任务中，其感知精度高度依赖精确的立体标定参数。然而，在实际运营条件下，由于温度变化、振动、碰撞或结构老化等因素，标定参数会随时间发生缓慢甚至阶跃式的漂移，导致深度估计出现系统性偏差，进而威胁下游任务的安全性与可靠性。因此，在不中断系统正常运行的前提下，对立体相机外参进行在线、实时、无目标的跟踪与校正，成为一个兼具理论挑战与工程价值的关键问题。

传统在线标定方法通常依赖显式的外点剔除机制（如 RANSAC）、鲁棒估计器或预训练的端到端学习模型，以应对特征匹配中不可避免的误匹配与噪声。这类方案存在三重瓶颈：其一，RANSAC 等迭代外点剔除方案在低信息量或高外点率的在线场景中收敛速度慢且稳定性不足；其二，鲁棒估计器（如 M‑估计器）的损失函数形态对超参数敏感，难以在吸引盆宽度与跟踪精度之间取得自适应平衡；其三，基于学习的方法虽然在特定数据集上表现优异，但其泛化能力受限于训练域，难以应对开放世界中数据分布的大幅变异。上述瓶颈共同导致现有方法难以在数据变异性大、信息内容低的在线场景中维持快速且稳定的收敛。

本文的核心动机在于提出一种**隐式鲁棒化**的在线标定跟踪范式：通过核化极线误差直接在损失函数层面抑制外点影响，从而消除对显式外点剔除、复杂鲁棒估计器或训练模型的依赖。在此基础上，我们设计了一个轻量级的在线随机优化框架（TESO），使其能够在本质矩阵流形上自适应地跟踪外参变化，并联合校正精度与深度一致性指标全面评估标定参数的不一致性。该方法无需针对新场景进行训练，仅依赖通用关键点检测与特征描述子，即可在多种驾驶场景下实现高精度、低延迟的旋转标定跟踪。

## 核心创新

TESO 的核心贡献在于**通过损失函数的内在鲁棒化，消除了对显式外点剔除、鲁棒估计器或学习模型的依赖**，使轻量级的在线随机优化即可在本质矩阵流形上实现高精度、低延迟的立体外参跟踪。

### 从“匹配质量敏感”到“损失函数鲁棒”

传统立体标定与在线校正方法将性能瓶颈锚定在对应点质量上：要么依赖高置信度匹配器（如 SuperGlue）提供干净的一对一对应，要么借助 RANSAC 等外点剔除方案反复清洗匹配集。这种设计在数据变异性大、信息内容低的在线场景中面临双重困境——匹配器本身可能失效，而 RANSAC 的随机性又引入额外的收敛波动。

TESO 的因果旋钮是**核化极线误差**（kernelized epipolar error）。对于第 $s$ 帧提取的关键点集 $\mathbf{X}$ 和 $\mathbf{Y}$，TESO 在描述子空间中为每个关键点寻找 $k=5$ 个最近邻，构建临时对应集合，并定义双向核相关损失：

$$
\mathcal{L}(\boldsymbol{\theta} | \mathbf{X}, \mathbf{Y}) = -\sum_{\mathbf{x}\in\mathbf{X}}\sum_{\mathbf{y}\in\mathrm{NN}^1(\mathbf{x})} \exp\left[-\frac{(\mathbf{y}^{\top}\mathbf{E}(\boldsymbol{\theta})\mathbf{x})^2}{2\sigma^2}\right] - \sum_{\mathbf{y}\in\mathbf{Y}}\sum_{\mathbf{x}\in\mathrm{NN}^0(\mathbf{y})} \exp\left[-\frac{(\mathbf{y}^{\top}\mathbf{E}(\boldsymbol{\theta})\mathbf{x})^2}{2\sigma^2}\right]
$$

这一设计的深层机制是：高斯核将极线距离映射为 $[0, 1]$ 区间的相关性得分，内点（极线距离小）贡献近 1 的高权重，外点（极线距离大）的贡献被指数衰减压制至接近零。**外点抑制发生在损失函数内部，而非上游的匹配筛选环节**。核宽 $\sigma$ 成为控制吸引盆宽度与跟踪精度权衡的关键参数——$\sigma$ 越大，吸引盆越宽，收敛越鲁棒但稳态精度越低；$\sigma$ 越小，精度越高但容易陷入局部极小。实验表明 $\sigma = 0.001$ 在 CARLA‑Drift 上提供了良好折衷。

这一创新的直接后果是**关键点检测器和特征提取器的选择不再关键**。Figure 4 的消融实验清晰展示：当使用非鲁棒二次损失时，SuperGlue 的匹配置信度超参数显著影响精度；而切换到核化损失后，置信度参数变得无关紧要。更关键的是，SIFT 搭配 5‑NN 匹配与 SuperGlue 搭配核化损失的跟踪精度差异极小，证明鲁棒损失函数有效解耦了匹配质量与跟踪性能。

### 从“批处理优化”到“流形上的自适应随机优化”

传统方法通常将标定参数估计建模为批处理优化问题（如全局 Bundle Adjustment）或采用卡尔曼滤波进行逐帧更新。前者计算量大且难以适应非平稳漂移，后者依赖线性化假设和噪声模型先验。

TESO 将外参跟踪形式化为**本质矩阵流形上的在线随机优化问题**。本质矩阵 $\mathbf{E}$ 通过本征参数化表示为 5 维参数 $\boldsymbol{\theta}$ 的函数：

$$
\mathbf{E}(\theta) = \mathbf{U} \exp[\Omega_1(\theta)] \, \boldsymbol{\Sigma}_0 \exp[-\Omega_2(\theta)] \mathbf{V}^{\top}
$$

在线优化采用 Schaul et al. 的自适应随机梯度方法，核心创新在于**根据梯度-方差比自适应调整记忆大小和学习率**。对于每个参数维度 $i$，梯度的一阶矩 $g_i$、二阶矩 $h_i$（Hessian 对角线）和方差 $v_i$ 通过指数移动平均估计：

$$
g_i^{(s)} = (1-\gamma_i^{(s)}) g_i^{(s-1)} + \gamma_i^{(s)} \frac{\partial\mathcal{L}}{\partial\theta_i}, \quad \gamma_i^{(s)} = \frac{1}{m_i^{(s-1)}}
$$

记忆大小 $m_i$ 根据信噪比 $(g_i)^2 / v_i$ 动态调整：

$$
m_i^{(s)} = \left(1 - \frac{(g_i^{(s)})^2}{v_i^{(s)}+\varepsilon}\right) \cdot m_i^{(s-1)} + 1
$$

当梯度信号清晰（信噪比高）时，记忆缩小以快速响应变化；当噪声主导时，记忆增大以平滑估计。参数更新步长融合二阶信息：

$$
\Delta\theta_i^{(s)} = -\nu_i \frac{1}{h_i^{(s)}} \frac{\partial\mathcal{L}}{\partial\theta_i}, \quad \nu_i = \frac{(g_i^{(s)})^2}{v_i^{(s)}+\varepsilon}
$$

权重 $\nu_i$ 在拟牛顿步（$\nu_i \to 1$，梯度可靠时）和保守梯度下降（$\nu_i \to 0$，噪声主导时）之间平滑切换。更新后的参数通过指数映射回本质矩阵流形，保证拓扑结构不变：

$$
\mathbf{U}^{(s)} = \mathbf{U}^{(s-1)} \exp[\Omega_1(\Delta\theta^{(s)})], \quad \mathbf{V}^{(s)} = \mathbf{V}^{(s-1)} \exp[\Omega_2(\Delta\theta^{(s)})], \quad \mathbf{E}^{(s)} = \mathbf{U}^{(s)} \boldsymbol{\Sigma}_0 \mathbf{V}^{(s)\top}
$$

### 与 SotA 的差异化定位

TESO 与现有方法的根本区别在于**零训练成本与跨域泛化**。Table 4 显示，仅使用核化损失 + 差分进化优化（无任何学习），TESO 在 CARLA‑FlowGuided 数据集上取得了与最佳端到端学习方法竞争的结果——而后者需要针对特定数据集训练。这一优势源于核化损失的隐式鲁棒性：它不需要学习“什么是好的匹配”，而是让损失函数本身对坏匹配不敏感。

在计算效率上，TESO 仅需存储 38 个参数，CPU 实现每帧约 86 ms，与最快的 SotA 学习方法耗时相当（79 ms vs. 86 ms），同时互相关分析表明跟踪延迟小于一帧。

## 整体框架

TESO 的整体流程围绕一个核心设计展开：**通过核化极线误差隐式鲁棒化损失函数，从而将在线立体标定跟踪简化为本质矩阵流形上的自适应随机优化问题**。该设计消除了对显式外点剔除（如 RANSAC）、鲁棒估计器或训练模型的依赖，使整个 pipeline 保持轻量且对匹配质量不敏感。

### 输入与预处理

系统输入为连续到达的无畸变立体图像对。每帧处理前，先利用离线标定的相机内参矩阵对原始图像进行**去畸变**，得到归一化坐标下的校正图像对。

### 关键点检测与特征提取

对每帧左右图像分别进行 **SIFT 关键点检测与 128 维描述子提取**。消融实验表明，SIFT 与 BRISK 在该框架下表现最佳且无统计显著差异，而 ORB 精度略低；但核化损失函数使得关键点检测器和特征提取器的选择不再关键——即便使用 SuperGlue 与 SIFT 搭配核损失时，性能差异也很小。

### k 近邻搜索与临时对应构建

传统方法依赖高质量的一对一匹配（如 SuperGlue）或多次 RANSAC 估计来构建点对应关系。TESO 则采用更轻量的策略：在描述子空间中，为每个关键点寻找 **k 个最近邻（k=5）**，构建临时对应集合。这些临时对应无需经过外点筛选，直接输入损失函数。在挑战性场景下，k=5 比更小的 k 值表现出更强的鲁棒性。

### 核相关损失函数

损失函数基于**核化极线距离**计算，其核心形式为双向 k 近邻上的高斯核求和：

$$
\mathcal{L}(\boldsymbol{\theta} | \mathbf{X}, \mathbf{Y}) = -\sum_{\mathbf{x}\in\mathbf{X}}\sum_{\mathbf{y}\in\mathrm{NN}^1(\mathbf{x})} \exp\left[-\frac{(\mathbf{y}^{\top}\mathbf{E}(\boldsymbol{\theta})\mathbf{x})^2}{2\sigma^2}\right] - \sum_{\mathbf{y}\in\mathbf{Y}}\sum_{\mathbf{x}\in\mathrm{NN}^0(\mathbf{y})} \exp\left[-\frac{(\mathbf{y}^{\top}\mathbf{E}(\boldsymbol{\theta})\mathbf{x})^2}{2\sigma^2}\right]
$$

其中 $\mathbf{E}(\boldsymbol{\theta})$ 为本质矩阵的 5 自由度本征参数化，$\sigma$ 为核宽参数。该损失函数的关键特性在于：**高斯核对大残差的对应点贡献趋近于零，从而隐式抑制外点，无需显式的外点剔除步骤**。$\sigma$ 参数控制吸引盆宽度与跟踪精度的权衡——$\sigma = 0.001$ 在 CARLA‑Drift 上提供了两者之间的良好折衷。

### 自适应随机优化

优化器采用来自 Schaul 等人的自适应随机梯度下降方法，在本质矩阵流形的 5 维参数空间 $\boldsymbol{\theta}$ 上在线更新。每帧执行以下步骤：

1. **梯度与二阶矩估计**：计算损失函数对每个参数的梯度，并通过指数移动平均估计其一阶矩 $g_i$、二阶矩（Hessian 对角线）$h_i$ 和方差 $v_i$。
2. **自适应记忆大小**：根据梯度平方与方差之比动态调整移动平均的记忆长度 $m_i$，以应对随机过程的非平稳变化。
3. **自适应步长**：结合二阶信息计算参数更新步长 $\Delta\theta_i$，在拟牛顿方向与梯度下降之间平滑切换。
4. **流形收缩**：通过指数映射将参数增量应用回本质矩阵流形，保证更新后的矩阵始终满足本质矩阵的拓扑约束。

### 输出与分解

每帧输出跟踪后的本质矩阵 $\mathbf{E}$。通过 OpenCV 的标准分解从中提取相对旋转 $\mathbf{R}$ 和平移方向 $\mathbf{t}$（平移缩放不可观，需重缩放到参考基线长度以与真值比较）。整个 pipeline 仅需存储 **38 个参数**，CPU 实现每帧约 **86 ms**，与最快的 SotA 学习方法耗时相当。

### 流程总览

整体流程可概括为：**去畸变图像对 → SIFT 关键点与描述子 → k 近邻临时对应 → 核相关损失计算 → 自适应随机梯度估计 → 本质矩阵流形更新 → 旋转/平移分解输出**。该闭环在每个新帧到达时执行一次，实现完全在线的标定参数跟踪。

### 补充图表

![[assets/figures/papers/paper_list_l2143_https_arxiv_org_abs_2604_19420/figures/002_Figure_2.jpg]]
*Figure 2: The full overview of TESO*

## 核心模块与公式推导

### 3.1 本质矩阵流形参数化

立体相机的相对位姿由旋转矩阵 $\mathbf{R} \in SO(3)$ 和平移向量 $\mathbf{t} \in \mathbb{R}^3$（仅方向）决定，它们构成本质矩阵：

$$\mathbf{E} = [\mathbf{t}]_\times \mathbf{R} \quad \text{(Eq. 2)}$$

对于一对归一化图像坐标 $(\mathbf{x}, \mathbf{y})$，极线约束要求：

$$\mathbf{y}^{\top} \mathbf{E} \mathbf{x} = 0 \quad \text{(Eq. 1)}$$

本质矩阵具有 5 个自由度，其流形结构与 $SE(3)/\sim$ 同胚。TESO 采用本征参数化，在参考本质矩阵 $\mathbf{E}_0 = \mathbf{U} \boldsymbol{\Sigma}_0 \mathbf{V}^{\top}$（其中 $\boldsymbol{\Sigma}_0 = \operatorname{diag}(1, 1, 0)$）附近，用 5 维参数 $\boldsymbol{\theta} \in \mathbb{R}^5$ 局部表达：

$$\mathbf{E}(\boldsymbol{\theta}) = \mathbf{U} \exp[\Omega_1(\boldsymbol{\theta})] \, \boldsymbol{\Sigma}_0 \exp[-\Omega_2(\boldsymbol{\theta})] \mathbf{V}^{\top} \quad \text{(Eq. 3)}$$

其中 $\Omega_1, \Omega_2$ 将 5 维参数映射为反对称矩阵，$\exp$ 为矩阵指数映射。该参数化保证了 $\mathbf{E}(\boldsymbol{\theta})$ 始终位于本质矩阵流形上，且 $\mathbf{E}(\mathbf{0}) = \mathbf{E}_0$。

### 3.2 核相关损失函数

传统极线误差对误匹配高度敏感，通常需要 RANSAC 等外点剔除方案。TESO 的核心创新在于通过**核化极线误差**隐式鲁棒化损失函数，消除了对显式外点剔除或学习模型的依赖。

对于左右图像的关键点集合 $\mathbf{X}$ 和 $\mathbf{Y}$，TESO 不使用严格的一对一匹配，而是为每个关键点寻找描述子空间中的 $k$ 个最近邻（$k=5$），构建临时对应。损失函数定义为双向核相关极线误差：

$$\mathcal{L}(\boldsymbol{\theta} | \mathbf{X}, \mathbf{Y}) = -\sum_{\mathbf{x}\in\mathbf{X}}\sum_{\mathbf{y}\in\mathrm{NN}^1(\mathbf{x})} \exp\left[-\frac{(\mathbf{y}^{\top}\mathbf{E}(\boldsymbol{\theta})\mathbf{x})^2}{2\sigma^2}\right] - \sum_{\mathbf{y}\in\mathbf{Y}}\sum_{\mathbf{x}\in\mathrm{NN}^0(\mathbf{y})} \exp\left[-\frac{(\mathbf{y}^{\top}\mathbf{E}(\boldsymbol{\theta})\mathbf{x})^2}{2\sigma^2}\right] \quad \text{(Eq. 4)}$$

**关键机制**：
- **高斯核** $\exp(-d^2 / 2\sigma^2)$ 将极线距离 $d = \mathbf{y}^{\top}\mathbf{E}\mathbf{x}$ 映射到 $[0, 1]$：正确匹配的 $d$ 接近 0，贡献接近 1；外点的 $d$ 较大，贡献被指数衰减压制，实现隐式鲁棒化。
- **核宽 $\sigma$** 是核心因果旋钮：较小的 $\sigma$ 提供更窄的吸引盆和更高的跟踪精度，但可能降低收敛范围。消融实验表明 $\sigma = 0.001$ 在 CARLA-Drift 上提供了吸引盆宽度与跟踪方差之间的良好折衷。
- **双向 $k$ 近邻** 使损失函数对关键点检测器和特征提取器的选择不敏感。实验证实，使用核损失时 SIFT 与 SuperGlue 的性能差异极小，且 SuperGlue 的匹配置信度超参数变得无关紧要（Figure 4）。

![[assets/figures/papers/paper_list_l2143_https_arxiv_org_abs_2604_19420/figures/009_Figure_4.jpg]]
*Figure 4: TESO performance visualized as an average rotational error on two sequences from the MAN TruckScenes dataset using different matching algorithms and loss functions. It is evident that with a higher confidence level in SuperGlue matches and a non-robust loss function (represented by the red points), the precision increases. However, using our proposed kernelized loss function with SuperGlue matches (blue points) renders the confidence hyper-parameter unimportant. The difference between SIFT (with 5-NN matching) and SuperGlue, using a kernelized loss function, is also very small, suggesting that the robust loss function renders the selection of keypoint detector and feature extractor uncritic...*

### 3.3 在线自适应随机优化

TESO 在本质矩阵流形上执行在线随机优化，每帧基于当前关键点计算梯度并更新参数 $\boldsymbol{\theta}$。优化器采用 Schaul et al. 的自适应学习率框架，核心在于估计每个参数的一阶矩（梯度期望）、二阶矩（Hessian 对角线）和方差。

**梯度指数移动平均**（Eq. 5）：

$$g_i^{(s)} = (1-\gamma_i^{(s)}) g_i^{(s-1)} + \gamma_i^{(s)} \frac{\partial\mathcal{L}}{\partial\theta_i}, \quad \gamma_i^{(s)} = \frac{1}{m_i^{(s-1)}}$$

**自适应记忆大小**（Eq. 6）：

$$m_i^{(s)} = \left(1 - \frac{(g_i^{(s)})^2}{v_i^{(s)}+\varepsilon}\right) \cdot m_i^{(s-1)} + 1$$

其中 $v_i$ 为梯度平方的移动平均。当梯度平方与方差之比较大时（信号强），记忆大小减小以快速响应；反之（噪声主导）则增大记忆以平滑估计。这一机制使优化器能自适应非平稳变化的随机过程。

**参数更新步长**（Eq. 7）：

$$\Delta\theta_i^{(s)} = -\nu_i \frac{1}{h_i^{(s)}} \frac{\partial\mathcal{L}}{\partial\theta_i}, \quad \nu_i = \frac{(g_i^{(s)})^2}{v_i^{(s)}+\varepsilon}$$

其中 $h_i$ 为 Hessian 对角线的移动平均。自适应因子 $\nu_i \in [0, 1]$ 在拟牛顿方向（$\nu_i \to 1$）与梯度下降（$\nu_i \to 0$）之间平滑切换：当梯度估计可靠时更接近牛顿步，噪声大时退化为保守的梯度步。

**流形收缩映射**（Eq. 8）：参数增量 $\Delta\boldsymbol{\theta}$ 通过指数映射作用在 $\mathbf{U}, \mathbf{V}$ 上，保证更新后的本质矩阵始终位于流形上：

$$\mathbf{U}^{(s)} = \mathbf{U}^{(s-1)} \exp[\Omega_1(\Delta\boldsymbol{\theta}^{(s)})], \quad \mathbf{V}^{(s)} = \mathbf{V}^{(s-1)} \exp[\Omega_2(\Delta\boldsymbol{\theta}^{(s)})], \quad \mathbf{E}^{(s)} = \mathbf{U}^{(s)} \boldsymbol{\Sigma}_0 \mathbf{V}^{(s)\top}$$

### 3.4 完整流水线

TESO 的每帧处理流程为：
1. **图像去畸变**：利用离线标定的内参矩阵 $\mathbf{K}$ 校正镜头畸变。
2. **SIFT 关键点检测与特征提取**：从左右图像提取归一化关键点坐标 $\mathbf{X}, \mathbf{Y}$ 及 128 维描述子。
3. **$k$ 近邻搜索**：在描述子空间中为每个关键点寻找 $k=5$ 个最近邻。
4. **核相关损失计算**：按 Eq. (4) 计算当前参数 $\boldsymbol{\theta}$ 下的损失及梯度。
5. **自适应随机优化**：按 Eqs. (5)–(7) 更新一阶/二阶矩估计并计算参数增量。
6. **流形更新**：按 Eq. (8) 将增量映射回本质矩阵流形，得到 $\mathbf{E}^{(s)}$。
7. **位姿分解**：通过 OpenCV 的 SVD 分解从 $\mathbf{E}^{(s)}$ 恢复旋转 $\mathbf{R}$ 和平移方向 $\mathbf{t}$，平移缩放归一化到参考基线长度。

整个流水线仅需存储 38 个参数（5 维 $\boldsymbol{\theta}$ 及其梯度/方差/Hessian 估计），CPU 实现每帧约 86 ms，与最快的学习方法耗时相当。

### 补充图表

![[assets/figures/papers/paper_list_l2143_https_arxiv_org_abs_2604_19420/figures/015_Figure_6.jpg]]
*Figure 6: Kernel corelation loss evaluations. Narrower is better*

## 实验与分析

### 核心实验结果

#### CARLA‑Drift 漂移跟踪

TESO 在 CARLA‑Drift 合成漂移数据集上展现出高精度旋转跟踪能力。该数据集对每帧施加 ±0.01° 每自由度的旋转标定漂移，模拟真实场景中缓慢累积的标定偏差。Table 1a 显示，TESO 将三个旋转自由度的平均绝对误差（MAE）从无跟踪时的 0.15°–0.18° 降至亚 0.04° 水平：Rx 轴精度达 0.011°，Rz 轴为 0.015°，而最困难的 Y 轴（绕垂直轴旋转，对深度估计影响最大）也达到 0.039°。这一结果验证了核化极线损失在 X 和 Z 轴旋转上具有更强的可观性，与 Figure 1 中跟踪曲线（实线）紧密跟随漂移真值（虚线）的视觉证据一致。

![[assets/figures/papers/paper_list_l2143_https_arxiv_org_abs_2604_19420/figures/001_Figure_1.jpg]]
*Figure 1: At the top (a) is an example of TESO tracking (solid) on a sequence from the CARLA–Drift dataset with rotational calibration drift (dashed) of ±0.01◦ per frame per DoF (see the coordinate system on the left). The easiest degrees to track are the rotations around X (red) and then Z (blue), which are easily observable in our kernelized epipolar error. The rotation around Y (green) is the most difficult to track, but also has the largest impact on depth estimation. At the bottom, there are stereo depth error maps for the image (b) on drifted calibration without tracking (c) and with TESO tracking (d). TESO can visibly reduce the effect of rotational drift because the disparity map is denser an...*

从立体视觉指标看（Table 1b），TESO 跟踪使关键点偏移改善量（KO‑I）从 1.94 px 降至 0.03 px，视觉里程计流改善量（VOF‑I）从 1.65 px 降至 0.07 px，深度一致性改善量（DC‑I）从 2.06 m 降至 0.52 m。三项指标均实现一个数量级以上的提升，表明旋转参数的在线校正显著改善了立体匹配和深度估计的质量。

#### KITTI 标定不一致性发现

在 KITTI 数据集上，TESO 揭示了原始标定参数的系统性不一致。使用原始内参时，序列 00‑01 之间的 Y 轴旋转差异高达 0.489°（Table 2a），这一量级远超传感器热漂移的预期范围。当替换为重新标定的内参（来自文献 ）后，TESO 的 Y 轴旋转精度提升约 20 倍至 0.025°，深度一致性改善量提升约 50 倍（Table 2b）。该结果说明：**(1) 内参误差会显著污染外参跟踪结果；(2) TESO 可以作为诊断工具，揭示多传感器系统中隐藏的标定不一致性**。Figure 3 进一步显示，在序列 01 的首尾段落，关键点偏移改善指标出现明显负值（即优于参考标定），与文献 [2, 5, 23] 的既往发现相互印证。

![[assets/figures/papers/paper_list_l2143_https_arxiv_org_abs_2604_19420/figures/004_Figure_3.jpg]]
*Figure 3: Keypoint offset improvement metric (negative values are improvements over the reference) evaluation on seq. 01 (drive #42, 2011/10/03) with offline recalibration suggested in [4]. TESO clearly improves this metric at the beginning and end of the sequence. This corroborates the findings from [2, 5, 23]*

#### MAN TruckScenes 真实场景验证

在 MAN TruckScenes 数据集上，TESO 面对宽基线、相机汇聚以及雨雾、隧道、高速公路等挑战场景。对于标定正确的序列，TESO 跟踪结果与参考值偏差极小（Ry 为 0.115°，Table 3a），表明跟踪器在无漂移条件下是无偏的。对于施加合成旋转漂移的序列，TESO 同样实现了精确跟踪。Table 5 的细粒度分析显示，按时间（白天/夜晚）、地点（城市/高速）和天气（晴/雨）分组后，跟踪精度在大多数条件下保持稳定，仅在低光照和雾天等 SIFT 关键点检测性能下降的场景中出现统计显著的退化（红色标记）。

![[assets/figures/papers/paper_list_l2143_https_arxiv_org_abs_2604_19420/figures/014_Table_5.jpg]]
*Table 5: Full results of TESO on the MAN Dataset based on the time of the day, location, and weather of each sequence. It shows results for sequences with correct calibration (a) and for sequences with synthetic calibration drift in all rotational DoFs (b). Red shows a statistically significantly worse precision than the tracking results over all sequences*

#### CARLA‑FlowGuided 离线校正对比

Table 4 展示了核化损失函数在离线校正场景下的竞争力。使用差分进化（DE）优化 Eq. (4) 的核化极线误差，TESO 在 CARLA‑FlowGuided 数据集上取得了与最佳端到端学习方法 Gong et al. 竞争的结果，且无需针对新数据集训练。这一对比凸显了核化损失隐式鲁棒外点的优势——即使在没有在线自适应学习率的情况下，仅凭损失函数本身的设计即可跨域泛化。

![[assets/figures/papers/paper_list_l2143_https_arxiv_org_abs_2604_19420/figures/007_Table_4.jpg]]
*Table 4: Results of our kernelized error Eq. (4) optimization using differential evolution (DE) on CARLA–FlowGuided dataset and current SotA methods on this dataset (taken from [15, 21]). Our recalibration shows competitive results with the best end-to-end learning method [15]. This suggests very good robustness of our kernel-based error to outlier matches, without any need for training on new datasets*

### 消融实验

#### 核化损失函数的关键作用

Figure 4 展示了损失函数和匹配策略的消融结果。当使用非鲁棒二次损失时，SuperGlue 匹配置信度阈值成为关键超参数——高置信度匹配才能保证精度（红色点）。然而，当采用核化损失函数后，置信度超参数变得无关紧要（蓝色点），SIFT 搭配 5‑NN 匹配与 SuperGlue 的性能差异也极小。这一发现确立了核化损失的核心价值：**通过损失函数层面的隐式鲁棒化，消除了对特定关键点检测器和特征提取器的依赖**，使系统在匹配质量波动时保持稳定。

#### 关键点检测器与超参数选择

Supplement A.4 的对比表明，SIFT 与 BRISK 作为关键点检测器表现最佳且无统计显著差异，ORB 精度略低。核宽参数 σ = 0.001 在 CARLA‑Drift 上提供了吸引盆宽度与跟踪方差之间的良好折衷（Supplement A.5）；k=5 的近邻数量在挑战性场景下比 k=1 更鲁棒，因为多近邻策略增加了损失函数的平滑性和外点容错能力。

#### 跟踪延迟与计算效率

Figure 5 的互相关分析显示，TESO 跟踪序列与累积漂移序列的互相关峰值位于零滞后，表明跟踪延迟小于一帧。在计算开销方面，TESO 仅需存储 38 个参数（5 个流形参数及其梯度、方差、Hessian 对角线等统计量），CPU 实现每帧约 86 ms，与最快的学习型方法（79 ms）耗时相当（Supplement A.3），满足实时应用需求。

![[assets/figures/papers/paper_list_l2143_https_arxiv_org_abs_2604_19420/figures/010_Figure_5.jpg]]
*Figure 5: Latency evaluation on MAN TruckScenes dataset. It is estimated as a discrete cross-correlation between the TESO tracking sequence and the cumulative drift sequence for shifts in the range (−1600, 1600). The maxima in all three degrees of freedom are at zero, which suggests the latency is less than one frame*

### 失败模式与局限性

尽管 TESO 在多数场景下表现鲁棒，分析揭示了以下失败模式：

1. **平移跟踪精度受限**：由于本质矩阵无法恢复基线尺度，平移跟踪需重缩放至参考基线长度。在典型驾驶场景中，平移精度仅达厘米级，远低于旋转精度。这是因为远距离场景下平移信息在极线约束中的可观性天然较弱。

2. **低纹理与恶劣环境退化**：在低光照、雾天、隧道等条件下，通用 SIFT 关键点检测数量和质量的下降直接导致跟踪精度显著变差（Table 5 红色标记）。当前方法缺乏针对这些场景的特征表示或损失函数适配机制。

3. **内参误差传递**：KITTI 实验清晰表明，离线标定的内参矩阵误差会系统性污染外参跟踪结果。当前框架仅在线更新本质矩阵的 5 个自由度，未包含焦距等内参，因为内参不是流形参数，直接集成需要改变优化框架。

4. **非连续跳变的响应未知**：所有实验均基于缓慢漂移假设，TESO 对快速、大幅度的非连续标定跳变（如撞击）的反应时间及稳定性尚未评估。

### 实验公平性说明

所有评估均采用统一的立体指标（KO、VOF、DC），并在可能时使用 LiDAR 投影进行深度一致性验证，确保指标的可比性。TESO 无需数据驱动训练，因此在跨数据集泛化方面具有天然优势；与其他学习方法对比时，需注意后者可能过拟合特定域。KITTI 实验揭示的内参不一致性问题提示：在评估在线标定方法时，内参的准确性应作为先决条件加以验证。

### 补充图表

![[assets/figures/papers/paper_list_l2143_https_arxiv_org_abs_2604_19420/figures/003_Table_1.jpg]]
*Table 1: TESO performance on CARLA–Drift dataset, visualised as geometric precision 1a and stereo metrics 1b (first rows) vs. metrics without tracking. One can see that TESO tracking consistently improves both the rotation precision and stereo metrics. The hardest DoF is*

![[assets/figures/papers/paper_list_l2143_https_arxiv_org_abs_2604_19420/figures/005_Table_3.jpg]]
*Table 3: TESO performance on the MAN TruckScenes dataset, visualised as geometric precision 3a and stereo metrics 3b*

![[assets/figures/papers/paper_list_l2143_https_arxiv_org_abs_2604_19420/figures/006_Table.jpg]]
*Table: (a) Geometric Precision (lower is better) (b) Stereo Metrics (lower is better, negative means improvement over the reference parameters)*

## 方法谱系与知识库定位

### 方法在立体视觉在线标定谱系中的位置

立体相机在线标定长期面临一个核心瓶颈：**传统方法依赖复杂的外点剔除方案（如RANSAC）、鲁棒估计器或训练好的模型，难以在数据变异性大、信息内容低的在线场景中维持快速且稳定的收敛**。TESO 通过一条不同的路径绕开了这一瓶颈——**核化极线误差隐式鲁棒化损失函数，消除了对特定特征匹配质量和显式外点剔除的依赖，使得轻量级的在线随机优化即可在本质矩阵流形上自适应跟踪参数**。

从方法谱系看，TESO 位于以下几条技术路线的交汇处：

- **基于几何约束的在线标定**：传统方法依赖极线约束的二次误差，配合 RANSAC 或 M-估计器剔除误匹配。TESO 将这一范式颠倒——不是先筛选内点再优化，而是通过核相关损失函数（Eq. (4)）使优化过程本身对误匹配不敏感。这一设计借鉴了核相关在点云配准中的思想（如 Tsin & Kanade 2004），但将其首次系统性地引入本质矩阵的在线跟踪场景。

- **端到端学习方法的替代路径**：近年来，**Gong et al.** 的端到端立体校正网络和 **Kumar et al.** 的实时学习框架代表了数据驱动的标定路线。TESO 在 CARLA–FlowGuided 数据集上使用差分进化优化核化损失函数，取得了与最佳端到端学习方法竞争的结果（Table 4），且无需针对新数据集训练。这表明核化损失函数本身具有强大的泛化能力，在无需学习的前提下接近了学习方法的性能上限。

- **在线随机优化的流形约束**：TESO 的优化框架继承了 Schaul et al. 的自适应随机梯度方法，但将其扩展到本质矩阵的 5 维流形上。通过指数映射进行流形收缩（Eq. (8)），保证每次更新后的矩阵始终满足本质矩阵的拓扑约束，避免了传统方法中事后投影带来的信息损失。

### 关键设计选择的适用边界

TESO 的核相关损失函数中，**带宽参数 σ 是控制吸引盆宽度与跟踪精度的核心因果旋钮**。消融实验表明，σ = 0.001 在 CARLA–Drift 上提供了吸引盆宽度与跟踪方差之间的良好折衷（Supplement A.5）。这一参数直接决定了方法的适用边界：

- **吸引盆宽度**：较大的 σ 使损失函数更平滑，吸引盆更宽，有助于从较大初始误差中恢复，但会降低跟踪精度。
- **跟踪精度**：较小的 σ 使损失函数更尖锐，精度更高，但吸引盆收窄，可能在快速漂移时丢失跟踪。

近邻数量 k = 5 在挑战性场景下表现出更强的鲁棒性（Supplement A.5），这一设计使 TESO 对关键点检测器和特征提取器的选择不再敏感。Figure 4 清晰展示了这一性质：使用核化损失函数后，SuperGlue 与 SIFT 的性能差异大幅缩小，匹配置信度超参数的重要性也随之消失。

### 与基线方法的对比分析

| 对比维度 | 传统 RANSAC + 几何优化 | 端到端学习方法（Gong et al. / Kumar et al.） | TESO |
|---------|----------------------|------------------------------------------|------|
| 外点处理 | 显式 RANSAC 或 M-估计器 | 隐式学习鲁棒特征 | 核相关损失隐式鲁棒化 |
| 训练需求 | 无 | 需要标注数据 | 无 |
| 泛化能力 | 依赖场景纹理 | 可能过拟合训练域 | 跨数据集泛化能力强 |
| 优化方式 | 批处理或卡尔曼滤波 | 端到端推理 | 在线随机二阶优化 |
| 对应点构建 | 高质量一对一匹配 | 端到端学习匹配 | k 近邻搜索（k=5）搭配核损失 |
| 流形约束 | 事后投影 | 网络隐式学习 | 指数映射显式保持 |

在 CARLA–Drift 数据集上，TESO 将旋转跟踪精度提升至 X/Z 轴 <0.02°、Y 轴 0.039°，相比无跟踪的原始标定（Rx 0.157°, Ry 0.166°, Rz 0.175°）大幅降低漂移（Table 1a）。立体指标同样显著改善：KO-I 从 1.94 px 降至 0.03 px，深度一致性 DC-I 从 2.06 m 降至 0.52 m（Table 1b）。

### 局限性与开放问题

**平移跟踪的精度上限**：在典型驾驶场景下，平移跟踪精度受限于远距离场景的结构信息不足，仅能达到厘米级。这一局限源于本质矩阵本身的性质——基线尺度无法从极线约束中恢复，TESO 通过参考基线长度进行缩放，但无法在线更新尺度信息。

**恶劣条件下的特征退化**：在低光照、雾天、隧道等条件下，通用 SIFT 关键点检测性能下降，导致跟踪精度显著变差（Table 5 按天气/时间分组的结果证实了这一点）。这是所有基于特征的几何方法的共性局限。

**内参耦合效应**：TESO 依赖离线标定的相机内参矩阵，内参的误差会传递到跟踪结果中。KITTI 数据集上的实验揭示了这一问题的严重性：使用原始 KITTI 内参时，TESO 检测到序列对之间存在显著不一致（00-01 的 Ry 达 0.489°）；使用重新标定的内参后，Y 轴旋转精度提升 20 倍至 0.025°，深度一致性提升 50 倍（Table 2a–2b）。这表明内参精度是外参在线跟踪的隐藏前提。

**当前实现的自由度限制**：TESO 仅在线跟踪本质矩阵的 5 个自由度（旋转 3 + 平移方向 2），未包含焦距等内参。作者明确指出，内参不是流形参数，直接集成需要改变优化框架。

**开放问题**：
1. 如何将焦距和主点等内参有效地整合到在线随机优化框架中，而不仅是依赖离线内参？
2. 在低纹理、重复纹理或纯夜间场景中，如何设计更鲁棒的特征表示或损失函数以维持跟踪精度？
3. 基线长度（平移缩放）无法从本质矩阵中恢复，如何利用其他传感器（如 LiDAR 或车速）在线更新基线尺度？
4. TESO 对快速、大幅度的非连续标定跳变（如撞击）的反应时间及稳定性如何？

### 知识库定位

TESO 的核心贡献在于**将核相关损失与在线流形优化结合，构建了一个无需训练、对匹配质量不敏感的立体外参在线跟踪框架**。它在方法谱系中填补了传统几何方法与端到端学习方法之间的空白：既有几何方法的可解释性和无需训练的优势，又通过损失函数设计获得了接近学习方法的鲁棒性。其揭示的内参与外参耦合效应，也为后续研究提供了重要的实验依据——立体标定评估必须同时考虑内参一致性和深度一致性指标，单一指标可能掩盖系统性的标定误差。

## 原文 PDF

![[paperPDFs/CVPR_2026/TESO_Online_Tracking_of_Essential_Matrix_by_Stochastic_Optimization.pdf]]
