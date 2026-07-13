---
title: "Paparazzo: Active Mapping of Moving 3D Objects"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Paparazzo_Active_Mapping_of_Moving_3D_Objects.pdf
project_link: "https://davidea97.github.io/paparazzo-page/"
code_link: null
aliases:
- Paparazzo
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 基于EKF置信度的双模式切换机制与同步感知的代价函数 B(x,i) = -w_eig·EIG(x) + w_sync·C_sync(x,i)。当EKF状态估计可靠时，系统进入Object Mapping Mode，通过前向传播候选视点并最小化联合代价来选择最优观测位姿；当EKF不确定时，系统切换至Object Tracking Mode优先稳定运动估计。权...
primary_logic: 将候选视点定义在物体局部参考系中并随物体一起运动，利用EKF预测物体未来N_h步的位姿序列，将所有候选视点沿预测轨迹传播，从而在物体运动的未来时刻评估每个视点的信息量和可达性。这使得智能体能够预先规划路径，在物体到达预测位置的同时恰好到达观测位置，实现动态场景下的高效主动重建。
claims:
- Paparazzo在所有运动模式下均一致优于基线方法，在Bouncing Ball运动下平均覆盖率达到81.51%，相比最佳基线TO（75.89%）提升5.62个百分点。
- 在最具挑战性的Stop & Go运动模式下，Paparazzo覆盖率达68.03%，比TO（60.79%）提升7.24个百分点，AUC从0.59提升至0.65。
- Paparazzo在所有场景和运动模式下AUC均优于所有基线，说明其在整个探索过程中重建效率更高。
- 在Stop & Go运动的定性对比中，基线方法（RW, RIS, TO）无法重建物体的完整正面表面，而Paparazzo成功恢复了这些区域。
---

# Paparazzo: Active Mapping of Moving 3D Objects

> [!tip] 核心洞察
> 将候选视点定义在物体局部参考系中并随物体一起运动，利用EKF预测物体未来N_h步的位姿序列，将所有候选视点沿预测轨迹传播，从而在物体运动的未来时刻评估每个视点的信息量和可达性。这使得智能体能够预先规划路径，在物体到达预测位置的同时恰好到达观测位置，实现动态场景下的高效主动重建。

| 字段 | 内容 |
|------|------|
| 中文题名 | Paparazzo：移动3D物体的主动建图 |
| 英文题名 | Paparazzo: Active Mapping of Moving 3D Objects |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.19556) · [Project](https://davidea97.github.io/paparazzo-page/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | Paparazzo |
| Dataset | Active Mapping of Moving Objects Benchmark |

> [!tip] 效果简介
> - Active Mapping of Moving Objects Benchmark (6 scenes × 4 objects × 4 motion pat... 上，Coverage (%) 81.51 (BB) / 70.73 (CBB) / 67.73 (FB) / 68.03 (SG) vs 75.89 (TO-BB) / 68.15 (TO-CBB) / 62.05 (TO-FB) / 60.79 (TO-SG) (+5.62 / +2.58 / +5.68 / +7.24)。
> - Active Mapping of Moving Objects Benchmark 上，Completeness (cm) 0.77 (BB) / 1.11 (CBB) / 1.23 (FB) / 1.20 (SG) vs 0.90 (TO-BB) / 1.11 (TO-CBB) / 1.45 (TO-FB) / 1.41 (TO-SG) (-0.13 / 0.00 / -0.22 / -0.21)；AUC 0.75 (BB) / 0.67 (CBB) / 0.62 (FB) / 0.65 (SG) vs 0.70 (TO-BB) / 0.64 (TO-CBB) / 0.58 (TO-FB) / 0.59 (TO-SG) (+0.05 / +0.03 / +0.04 / +0.06)。

## 概要

**问题背景** 现有主动建图方法均假设场景为静态，无法处理独立运动的非合作目标。当物体自主运动时，智能体必须在估计物体运动状态的同时预测其未来轨迹，并规划自身路径以在正确的时间到达信息量最大的观测位置——视点质量同时取决于几何信息量和时间可达性，二者之间存在根本性的权衡。

**核心思路** Paparazzo是一个无学习（learning-free）的主动三维重建框架，专为动态场景中移动物体的重建而设计。其关键洞察在于：将候选视点定义在物体局部参考系中并随物体一起运动，利用扩展卡尔曼滤波（EKF）预测物体未来 $N_h$ 步的位姿序列，将所有候选视点沿预测轨迹传播，从而在物体运动的未来时刻评估每个视点的信息量和可达性。这使得智能体能够预先规划路径，在物体到达预测位置的同时恰好到达观测位置，实现动态场景下的高效主动重建。

**方法定位** Paparazzo采用基于EKF置信度的双模式切换机制：当状态估计可靠时，系统进入Object Mapping Mode，通过前向传播候选视点并最小化联合代价 $B(\mathbf{x}, i) = -w_{\mathrm{eig}}\mathrm{EIG}(\mathbf{x}) + w_{\mathrm{sync}} C_{\mathrm{sync}}(\mathbf{x}, i)$ 来选择最优观测位姿；当EKF不确定时，系统切换至Object Tracking Mode优先稳定运动估计。权重 $w_{\mathrm{eig}}=0.8$ 和 $w_{\mathrm{sync}}=1.2$ 控制信息量与时间同步的权衡。

**主要结果** 在Habitat 3.0模拟器中构建的6个场景 × 4个物体 × 4种运动模式的基准测试上，Paparazzo在所有运动模式下均一致优于基线方法：在Bouncing Ball运动下平均覆盖率达到81.51%，相比最佳基线TO（75.89%）提升5.62个百分点；在最具挑战性的Stop & Go运动模式下，覆盖率达68.03%，比TO（60.79%）提升7.24个百分点，AUC从0.59提升至0.65。Paparazzo在所有场景和运动模式下AUC均优于所有基线，说明其在整个探索过程中重建效率更高。

### 问题背景：移动物体的主动建图

三维重建是计算机视觉与机器人领域的核心任务之一。近年来，随着神经辐射场（NeRF）和3D Gaussian Splatting等可微分表示的兴起，主动建图（active mapping）取得了显著进展——智能体可以自主规划观测轨迹，以最大化信息增益的方式逐步构建场景的完整三维模型。

然而，现有主动建图方法存在一个根本性的假设局限：**它们均假定场景是静态的**。在这一假设下，视点的信息量仅取决于几何覆盖的完备性，智能体只需按部就班地访问未观测区域即可。当场景中包含**独立运动的非合作目标**（如移动的车辆、行人或被操控的物体）时，这一范式完全失效。

### 核心瓶颈：信息量与时间可达性的根本权衡

移动物体的主动建图面临一个双重挑战，构成了问题的本质瓶颈：

1. **运动状态估计的不确定性**：智能体必须在建图的同时估计物体的运动状态（位姿与速度）。当观测不足时，运动估计不可靠，导致预测的未来轨迹存在较大误差，进而使视点规划失去依据。

2. **信息量与时间同步的根本权衡**：视点的质量同时取决于两个相互制约的因素——该视点能提供多少新的几何信息（信息量），以及智能体能否在物体到达对应位置的同时恰好抵达该视点（时间可达性）。一个信息量极高的视点，如果智能体无法及时到达，则毫无价值；反之，一个容易到达的视点，如果无法覆盖物体的未观测表面，同样贡献有限。

这一权衡可形式化表达为：智能体需要在物体运动的未来时刻评估每个候选视点的信息量和可达性，并在二者之间做出最优折中。这正是现有方法无法处理的核心难题。

### 现有方法缺口

当前主动建图方法可分为两类，均无法有效应对动态目标：

- **静态场景主动建图方法**（如基于FisherRF信息增益的视点选择）：完全不考虑物体运动，在动态场景中会因目标移动而持续“追丢”，导致重建覆盖率极低。例如，随机游走策略（Random Walk）在弹跳球运动下的平均覆盖率仅为51.50%（Table 1），说明完全忽略物体位置的探索无法有效重建移动目标。

- **纯被动跟踪策略**：仅使用滤波器（如扩展卡尔曼滤波）跟踪物体运动，但不进行主动视点选择。这种策略在物体运动方向单一时尚可维持跟踪，但无法从多角度观察物体，导致重建不完整。例如，在Forward & Backward运动模式下，纯跟踪策略的覆盖率仅为62.05%（Table 1）。

### 本文动机与核心思路

针对上述缺口，本文提出**Paparazzo**——一个面向动态场景的无学习主动建图框架。其核心洞察是：**将候选视点定义在物体的局部参考系中并随物体一起运动，利用运动预测将视点沿未来轨迹传播，从而在物体运动的未来时刻评估每个视点的信息量与可达性**。

具体而言，Paparazzo通过以下机制解决信息量与时间同步的权衡：

- **双模式自适应切换**：基于扩展卡尔曼滤波（EKF）的置信度，系统在Object Tracking Mode（优先稳定运动估计）和Object Mapping Mode（主动选择最优观测位姿）之间切换，确保在运动估计可靠时才进行高风险的主动探索。

- **前向预测与视点传播**：利用EKF预测物体未来$N_h = 60$步的位姿序列，将所有候选视点沿预测轨迹传播，生成$|\mathcal{V}| \times N_h$个未来对齐视点，从而在规划阶段就显式地考虑时间同步约束。

- **联合代价函数**：视点选择准则$B(\mathbf{x}, i) = -w_{\mathrm{eig}} \mathrm{EIG}(\mathbf{x}) + w_{\mathrm{sync}} C_{\mathrm{sync}}(\mathbf{x}, i)$同时优化期望信息增益（EIG）和同步代价$C_{\mathrm{sync}}$，权重$w_{\mathrm{eig}}=0.8$和$w_{\mathrm{sync}}=1.2$控制二者的权衡。

通过这一设计，Paparazzo使智能体能够预先规划路径，在物体到达预测位置的同时恰好到达观测位置，实现动态场景下的高效主动重建。

## 核心方法与创新机理

Paparazzo的核心创新在于突破了主动建图领域长期以来“场景静态”的根本性假设，首次系统性地解决了**非合作运动目标的主动3D重建**问题。传统主动建图方法（如Random Walk、基于信息增益的贪心探索）均假设目标物体在世界坐标系中保持静止，视点选择仅需考虑当前时刻的信息量。当目标物体自主运动时，这类方法面临双重困境：智能体既无法预测物体未来的空间位置，也无法在正确的时间到达信息量最大的观测位姿。

Paparazzo通过以下五个关键机制实现了对动态场景的适应，每个机制均直接针对现有方法的根本性缺陷：

### 1. 场景假设：从静态世界到动态SE(3)状态估计

传统方法假设物体静止于世界坐标系中，而Paparazzo引入**基于SE(3)的扩展卡尔曼滤波（EKF）**来实时估计物体的位姿和速度。EKF维护物体在SE(3)流形上的状态，包括旋转、平移及其对应速度，通过恒速运动模型预测物体未来位姿：

$$T_{k|k-1} = T_{k-1} \exp(\omega_{k-1} \Delta t)$$

这一状态估计机制使得系统能够持续追踪物体的运动轨迹，并根据观测更新预测。EKF的置信度通过协方差矩阵的迹 $U_k$ 和归一化新息平方 $\mathrm{NIS}_k = y_k^{\top} S_k^{-1} y_k$ 量化，为后续的自适应模式切换提供了决策依据。

### 2. 视点参考系：从世界固定到物体中心随动

传统方法在世界坐标系中定义固定的候选视点，在动态场景中这些视点会因物体运动而迅速失效。Paparazzo将候选视点定义在**物体局部参考系**中，采用foveated分布——三个同心环（半径1.2-1.8 m），方位角间隔12°——使得候选视点随物体一起运动。这一设计确保了无论物体如何移动，候选视点始终围绕物体分布，保持有效的观测几何关系。

### 3. 时间规划：从当前时刻贪心到未来轨迹传播

传统方法仅考虑当前时刻的视点信息量，采用贪心策略选择下一个观测位置。Paparazzo利用EKF预测物体未来 $N_h = 60$ 步的位姿序列，将所有 $|\mathcal{V}|$ 个候选视点沿预测轨迹传播，评估 $|\mathcal{V}| \times N_h$ 个未来对齐视点的信息量和可达性。这使得智能体能够预先规划路径，在物体到达预测位置的同时恰好到达观测位置，实现了**时间维度上的主动规划**。

### 4. 视点选择准则：从单一信息量到信息-同步联合优化

传统方法仅基于FisherRF期望信息增益（EIG）选择视点。Paparazzo引入**联合代价函数**，同时考虑信息量和时间同步：

$$B(\mathbf{x}, i) = -w_{\mathrm{eig}} \mathrm{EIG}(\mathbf{x}) + w_{\mathrm{sync}} C_{\mathrm{sync}}(\mathbf{x}, i)$$

其中同步代价 $C_{\mathrm{sync}}(\mathbf{x}, i) = |\hat{s}_{\mathrm{agent}}(\mathbf{x}, i) - (i - k)|$ 衡量智能体到达视点所需步数与物体到达预测位姿所需步数之差。权重 $w_{\mathrm{eig}} = 0.8$ 和 $w_{\mathrm{sync}} = 1.2$ 控制信息量与时间同步的权衡。最优视点通过最小化联合代价选择：

$$(\mathbf{x}^*, i^*) = \underset{\mathbf{x} \in \mathcal{V}, (i-k) \le N_h}{\arg\min} B(\mathbf{x}, i)$$

这一设计解决了动态场景中“知道去哪里看”和“能否及时到达”之间的根本性权衡。

### 5. 运行模式：从单一建图到跟踪-建图自适应切换

传统方法采用单一建图模式，在运动估计不可靠时仍盲目进行视点规划。Paparazzo引入**双模式自适应切换机制**：当 $U_k < \tau_u$ 且 $\mathrm{NIS}_k < \tau_n$ 连续 $N_s = 4$ 帧时，系统进入**Object Mapping Mode**，执行上述联合优化视点选择；当EKF不确定时，系统切换至**Object Tracking Mode**，主动旋转使物体保持在图像中心，调整距离使物体表观尺寸约为图像一半，优先稳定运动估计。这一机制确保了系统在运动预测不可靠时不会浪费步数进行无效的建图探索。

### 创新总结

上述五个机制形成了完整的动态场景主动建图闭环：EKF提供运动预测能力，物体中心视点系确保候选视点的有效性，未来轨迹传播实现时间维度规划，联合代价函数平衡信息量与可达性，双模式切换保证系统鲁棒性。消融实验验证了每个创新组件的必要性：忽略同步代价和运动预测的RIS变体在Bouncing Ball运动下覆盖率仅67.07%（Paparazzo为81.51%），纯跟踪策略TO在Forward & Backward运动下覆盖率仅62.05%，证明了仅信息量选择或被动跟踪均不足以应对动态场景。

Paparazzo 是一个无学习（learning-free）的主动三维重建框架，专门针对**独立运动的非合作目标**。其核心设计围绕一个根本性的瓶颈展开：现有主动建图方法均假设场景为静态，当目标物体自主运动时，智能体必须在估计物体运动状态的同时预测其未来轨迹，并规划自身路径以在正确的时间到达信息量最大的观测位置——视点质量同时取决于几何信息量和时间可达性，二者之间存在根本性的权衡。

为应对这一挑战，Paparazzo 采用**基于 EKF 置信度的双模式切换机制**作为因果调控旋钮。系统在两种运行模式之间交替：

- **Object Tracking Mode（物体跟踪模式）**：当 EKF 状态估计不可靠时（不确定性度量 $U_k$ 和归一化新息平方 $\mathrm{NIS}_k$ 超过阈值），系统优先稳定运动估计。智能体主动旋转使物体分割掩码移向图像中心，并调整距离使物体表观尺寸约为图像的一半，从而获取稳定的跟踪观测。
- **Object Mapping Mode（物体建图模式）**：当 EKF 连续 $N_s=4$ 帧满足 $U_k < \tau_u$ 且 $\mathrm{NIS}_k < \tau_n$ 时，系统认为运动估计可靠，切换至主动建图模式。在此模式下，系统利用 EKF 预测物体未来 $N_h=60$ 步的位姿序列，将定义在物体局部参考系中的候选视点沿预测轨迹传播，并通过最小化联合代价函数选择最优观测位姿。

### 系统流水线

Paparazzo 的完整流水线由五个核心模块串联而成，形成“感知—预测—决策—执行—优化”的闭环：

1. **初始化模块（Initialization）**：在首次检测到目标物体时，通过质心和 PCA 估计物体在相机坐标系中的初始位姿 $T_{O_{t_d}}^{C_{t_d}}$，结合相机位姿 $T_{C_{t_d}}^{W}$ 计算物体在世界坐标系中的位姿 $T_{O_{t_d}}^{W}$。同时，从物体的 RGB-D 分割观测中初始化 3D Gaussian Splatting 模型的高斯原语。

2. **EKF 运动预测（EKF-Based Motion Prediction）**：在 SE(3) 上使用扩展卡尔曼滤波，以恒速运动模型 $T_{k|k-1} = T_{k-1} \exp(\omega_{k-1} \Delta t)$ 传播物体位姿。通过协方差迹 $U_k$ 和归一化新息平方 $\mathrm{NIS}_k = y_k^{\top} S_k^{-1} y_k$ 量化估计置信度，作为模式切换的决策依据。

3. **Object Tracking Mode**：当 EKF 不确定时触发。智能体执行视觉伺服式控制，使用 KISS-Matcher 结合 Colored ICP 估计当前物体位姿并更新 EKF，为后续建图模式积累可靠的运动先验。

4. **Object Mapping Mode**：当 EKF 置信时触发。在物体周围生成 foveated 分布的候选视点集 $\mathcal{V}$（三同心环，半径 1.2–1.8 m，方位角间隔 12°），视点定义在物体局部参考系中并随物体一起运动。利用 EKF 预测未来 $N_h$ 步的物体位姿，将所有候选视点沿预测轨迹传播，评估 $|\mathcal{V}| \times N_h$ 个未来对齐视点。通过最小化联合代价函数选择最优视点：
   $$B(\mathbf{x}, i) = -w_{\mathrm{eig}} \mathrm{EIG}(\mathbf{x}) + w_{\mathrm{sync}} C_{\mathrm{sync}}(\mathbf{x}, i)$$
   其中 $\mathrm{EIG}(\mathbf{x})$ 为基于 FisherRF 的期望信息增益，$C_{\mathrm{sync}}(\mathbf{x}, i) = |\hat{s}_{\mathrm{agent}}(\mathbf{x}, i) - (i - k)|$ 为同步代价（智能体到达步数与物体到达预测位姿步数之差），权重 $w_{\mathrm{eig}}=0.8$、$w_{\mathrm{sync}}=1.2$ 控制信息量与时间同步的权衡。选定视点后使用 A* 规划路径执行。

5. **3D Gaussian Splatting 优化**：基于 SplaTAM 骨干网络，在物体参考系中增量式稠密化和优化高斯原语。使用深度一致性滤波器 $|z_{g_k}(u) - z_k(u)| \leq \tau_d$（$\tau_d = 0.02$ m）确保几何正确性，选择可见关键帧联合优化 RGB 和 SSIM 损失，实现高质量的动态物体三维重建。

### 输入输出流

- **输入**：每步的 RGB-D 观测（512×512，90° 视场角）、目标物体的分割掩码。
- **内部状态**：EKF 估计的物体 SE(3) 位姿和速度、3D Gaussian Splatting 模型、历史关键帧。
- **输出**：智能体的导航动作（旋转、平移），以及增量更新的物体三维重建结果。
- **运行效率**：系统在线运行速度为 8 FPS。

整个框架的核心洞察在于：将候选视点定义在物体局部参考系中并随物体一起运动，利用 EKF 预测物体未来位姿序列，将所有候选视点沿预测轨迹传播，从而在物体运动的未来时刻评估每个视点的信息量和可达性。这使得智能体能够预先规划路径，在物体到达预测位置的同时恰好到达观测位置，实现动态场景下的高效主动重建。

### 补充图表

![[assets/figures/papers/paper_list_l2644_https_arxiv_org_abs_2604_19556/figures/002_Figure_2.jpg]]
*Figure 2: Paparazzo alternates between Object Tracking Mode and Object Mapping Mode based on the confidence of the EKF motion estimate. When the filter is uncertain, the agent prioritizes acquiring stabilizing observations; once confident, it predicts future object motion, generates and propagates candidate viewpoints, and selects the optimal one*

Paparazzo 的核心架构围绕一个 **EKF 置信度驱动的双模式切换机制** 展开，使智能体能够在跟踪运动物体和主动建图之间自适应切换。系统包含五个关键模块，其运行逻辑如图 Figure 2 所示。

### 初始化模块

在首次检测到目标物体时，系统通过质心和 PCA 估计物体在相机坐标系中的初始位姿。设检测时刻为 $t_d$，物体点云的质心作为平移向量，PCA 确定旋转矩阵，构建物体在相机系中的位姿 $T_{O_{t_d}}^{C_{t_d}}$。结合已知的相机位姿 $T_{C_{t_d}}^{W}$，物体在世界坐标系中的初始位姿为：

$$T_{O_{t_d}}^{W} = T_{C_{t_d}}^{W} T_{O_{t_d}}^{C_{t_d}}, \quad T_{O_{t_d}}^{C_{t_d}} = [R_{O_{t_d}}^{C_{t_d}} \quad t_{O_{t_d}}^{C_{t_d}}]$$

同时，从物体的分割 RGB-D 观测中初始化 3D Gaussian Splatting 模型的原语，为后续增量式重建提供几何先验。

### EKF 运动预测与置信度评估

系统在 SE(3) 上使用扩展卡尔曼滤波估计物体的位姿和速度。状态向量包含物体位姿和广义速度，预测步采用恒速运动模型，通过指数映射在 SE(3) 上传播位姿：

$$T_{k|k-1} = T_{k-1} \exp(\omega_{k-1} \Delta t)$$

滤波器置信度通过两个指标量化：**状态协方差矩阵的迹** $U_k$（衡量估计不确定性）和**归一化新息平方**（Normalized Innovation Squared, NIS），后者定义为：

$$\mathrm{NIS}_k = y_k^{\top} S_k^{-1} y_k$$

其中 $y_k$ 为观测位姿与预测位姿之间的新息向量，$S_k$ 为新息协方差矩阵。NIS 量化当前观测与运动预测之间的一致性，是模式切换的核心判据。

### Object Tracking Mode

当 $U_k < \tau_u$ 且 $\mathrm{NIS}_k < \tau_n$ 未能在连续 $N_s = 4$ 帧内同时满足时，EKF 被视为不可靠，系统进入 **Object Tracking Mode**。此模式下，智能体优先稳定运动估计：

- **旋转控制**：主动旋转使物体分割掩码移向图像中心
- **平移控制**：调整与物体的距离，使物体表观尺寸约为图像的一半
- **位姿估计**：使用 KISS-Matcher 结合 Colored ICP 估计当前帧的物体位姿，并更新 EKF

该模式牺牲建图效率以换取运动估计的快速稳定，为后续 Object Mapping Mode 提供可靠的运动预测基础。

### Object Mapping Mode

当 EKF 连续 $N_s$ 帧满足置信条件后，系统切换至 **Object Mapping Mode**，执行主动视点规划与建图。核心创新在于将候选视点定义在物体局部参考系中，使其随物体一起运动，并利用 EKF 预测未来轨迹进行时空联合优化。

#### 候选视点生成

候选视点集 $\mathcal{V}$ 以 foveated 配置分布在物体周围：三个同心环（半径 1.2–1.8 m），方位角间隔 12°，确保从多角度覆盖物体表面（Figure 5）。

![[assets/figures/papers/paper_list_l2644_https_arxiv_org_abs_2604_19556/figures/013_Figure_5.jpg]]
*Figure 5: Generation of candidate viewpoints for Object Mapping Mode. When the EKF becomes confident, Paparazzo switches from tracking to mapping and evaluates a set of candidate viewpoints V distributed around the object. The expected information gain (EIG) of each pose, computed using the FisherRF criterion, is visualized here with a color gradient: darker tones correspond to low informativeness, while brighter tones highlight more informative poses for reconstructing the object*

#### 未来轨迹传播与视点选择

EKF 预测物体未来 $N_h = 60$ 步的位姿序列（Figure 6），将所有候选视点沿预测轨迹传播，生成 $|\mathcal{V}| \times N_h$ 个未来对齐视点。对每个候选视点 $\mathbf{x}$ 在时间步 $i$ 的配置，计算联合代价函数：

![[assets/figures/papers/paper_list_l2644_https_arxiv_org_abs_2604_19556/figures/015_Figure_6.jpg]]
*Figure 6: EKF-based prediction of future object poses. The EKF predicts the object pose, denoted in orange, over the next*

$$B(\mathbf{x}, i) = -w_{\mathrm{eig}} \mathrm{EIG}(\mathbf{x}) + w_{\mathrm{sync}} C_{\mathrm{sync}}(\mathbf{x}, i)$$

其中：
- $\mathrm{EIG}(\mathbf{x})$ 为 FisherRF 期望信息增益，衡量视点的几何信息量
- $C_{\mathrm{sync}}(\mathbf{x}, i)$ 为同步代价，定义为智能体到达视点所需步数 $\hat{s}_{\mathrm{agent}}(\mathbf{x}, i)$ 与物体到达预测位姿所需步数 $(i - k)$ 之差的绝对值：

$$C_{\mathrm{sync}}(\mathbf{x}, i) = |\hat{s}_{\mathrm{agent}}(\mathbf{x}, i) - (i - k)|$$

- $w_{\mathrm{eig}} = 0.8$ 和 $w_{\mathrm{sync}} = 1.2$ 控制信息量与时间同步的权衡

最优视点选择为：

$$(\mathbf{x}^*, i^*) = \underset{\mathbf{x} \in \mathcal{V}, (i-k) \le N_h}{\arg\min} B(\mathbf{x}, i)$$

选定后使用 A* 算法规划智能体到 $\mathbf{x}^*$ 的路径。

### 3D Gaussian Splatting 优化

建图骨干基于 **SplaTAM**，在物体参考系中增量式优化高斯原语。关键设计包括：

- **深度一致性滤波**：仅当高斯原语的渲染深度 $z_{g_k}(u)$ 与观测深度 $z_k(u)$ 满足 $|z_{g_k}(u) - z_k(u)| \leq \tau_d$（$\tau_d = 0.02$ m）时，该原语才被视为物理可见，参与稠密化和关键帧选择。这避免了背面高斯被误认为可见表面。
- **多关键帧联合优化**：选择与当前帧共视的过去关键帧，联合优化 RGB 和 SSIM 损失，确保重建的全局一致性。

### 模式切换闭环

Object Mapping Mode 执行过程中，系统持续监控 EKF 的 $U_k$ 和 $\mathrm{NIS}_k$。一旦置信度降至阈值以下，立即回退至 Object Tracking Mode 重新稳定运动估计，形成闭环自适应控制。该机制在物体突然改变运动方向时尤为关键——此时 EKF 预测失效，系统通过切换模式避免基于错误预测的无效探索。

## 实验与关键发现

### 评估基准与实验设置

Paparazzo在**Active Mapping of Moving Objects Benchmark**上进行评估，该基准涵盖6个照片级真实室内场景（3个来自Matterport3D，3个来自Gibson）、4个具有不同形状和颜色的目标物体（Figure 3）、以及4种运动模式：**Bouncing Ball (BB)**、**Curved Bouncing Ball (CBB)**、**Forward & Backward (FB)** 和 **Stop & Go (SG)**。所有实验在Habitat 3.0模拟器中进行，智能体配备512×512 RGB-D相机（90°视场角），每轮运行500步，每组配置重复5次。所有方法从相同的物体初始化状态开始，物体随机放置在智能体前方1.0–2.5 m范围内。

![[assets/figures/papers/paper_list_l2644_https_arxiv_org_abs_2604_19556/figures/003_Figure_3.jpg]]
*Figure 3: The four target objects used in our experiments, featuring different shapes and colors. Each object is evaluated independently across all environments*

基线方法包括：
- **Random Walk (RW)**：经典静态场景主动建图基线，智能体在环境中随机移动，不考虑物体运动。
- **Random Informative Selection (RIS)**：Paparazzo的消融变体，从信息量候选视点中随机选择，忽略同步代价和运动预测。
- **Tracking-Only (TO)**：纯被动跟踪策略的下界基线，仅使用EKF跟踪物体运动，不进行主动视点选择。

RW、RIS、TO基线共享相同的物体检测和位姿估计流程，仅视点选择策略不同，确保对比的公平性。Paparazzo的关键参数（$w_{\text{eig}}=0.8$, $w_{\text{sync}}=1.2$, $\tau_u=0.1$, $\tau_n=0.5$, $N_s=4$, $N_h=60$）在验证集上经验确定，所有实验使用相同参数（Table 3）。

![[assets/figures/papers/paper_list_l2644_https_arxiv_org_abs_2604_19556/figures/012_Table_3.jpg]]
*Table 3: EKF parameters used in all experiments*

### 主要定量结果

**Table 1** 和 **Table 2** 展示了四种运动类型在六个场景下的Coverage（%）、Completeness（cm）和AUC对比，报告值为所有测试物体和运行次数的平均值。

**整体性能**：Paparazzo在所有运动模式和场景下一致优于所有基线方法。在Bouncing Ball运动下，Paparazzo平均覆盖率达到**81.51%**，相比最佳基线TO（75.89%）提升**5.62个百分点**；AUC从0.70提升至**0.75**。在最具挑战性的Stop & Go运动模式下，Paparazzo覆盖率达**68.03%**，比TO（60.79%）提升**7.24个百分点**，AUC从0.59提升至**0.65**。Completeness指标上，Paparazzo在所有运动模式下均取得更低（更优）的值，例如BB运动下为0.77 cm vs TO的0.90 cm。

**效率优势**：如**Figure 7**所示，Paparazzo在整个500步探索预算内持续保持更高的覆盖率，且曲线上升更陡，表明其在整个探索过程中重建效率更高。

**Stop & Go运动的显著优势**：在物体间歇性静止的Stop & Go运动中，Paparazzo的优势最为突出。**Table 4**显示，在Object 1上Paparazzo覆盖率达**81.23%** vs TO的68.25%，在Object 2上达**74.45%** vs TO的58.24%。定性对比（**Figure 8**）表明，基线方法（RW, RIS, TO）无法重建物体的完整正面表面，而Paparazzo成功恢复了这些区域，重建结果更完整、几何一致性更好。

### 消融实验

**RIS消融**验证了同步代价和运动预测的关键作用：在BB运动下，RIS覆盖率仅为**67.07%** vs Paparazzo的81.51%，表明仅基于信息量选择视点（忽略时间同步）不足以应对动态场景。RIS的性能甚至在某些情况下低于TO，说明不考虑运动预测的随机信息选择可能将智能体引导至无法及时到达的视点。

**TO消融**验证了主动建图策略的必要性：纯被动跟踪策略在Forward & Backward运动下覆盖率仅**62.05%**，因为被动策略无法从多角度观察物体。在Stop & Go运动中，TO基线在物体静止时完全被动等待，而Paparazzo持续主动探索（**Figure 11**），这解释了Table 4中二者性能的巨大差距。

**RW基线的低性能**（BB平均覆盖率仅**51.50%**）表明完全忽略物体位置的随机探索无法有效重建移动目标，进一步证明了运动感知规划的必要性。

### 失败模式与局限性分析

尽管Paparazzo在所有配置下均优于基线，其性能仍受以下因素制约：

1. **运动预测失效**：EKF在物体突然改变运动方向时变得不可靠，此时系统需切换至Tracking Mode重新稳定估计，导致建图效率损失。这在Curved Bouncing Ball和Forward & Backward运动中尤为明显，Coverage分别降至70.73%和67.73%。

2. **狭窄环境约束**：在Ribera等狭窄场景中性能下降，因为智能体的机动空间受限，难以在物体弹跳前及时重新定位到信息量最大的视点。

3. **单物体假设**：当前方法仅支持单个移动物体的重建，无法处理多物体场景。

4. **无学习限制**：作为无学习方法，Paparazzo无法从历史经验中持续改进策略，对新物体和场景的适应依赖手工设计的参数（$\tau_u$, $\tau_n$, $N_s$, $N_h$, $w_{\text{eig}}$, $w_{\text{sync}}$）。

5. **运行速度**：在线运行速度为8 FPS，在需要快速响应的场景中可能不足。

6. **仿真到现实的差距**：仅在Habitat 3.0模拟器中验证，实际部署依赖背景减法或运动分割方法的准确性，且真实传感器噪声和动态环境复杂度可能带来额外挑战。

### 补充图表

![[assets/figures/papers/paper_list_l2644_https_arxiv_org_abs_2604_19556/figures/006_Table_1.jpg]]
*Table 1: Quantitative results across scenes for the four dynamic motion types (Bouncing Ball (BB), Curved Bouncing Ball (CBB), Forward & Backward (FB), and Stop & Go (SG)). Reported values are averaged over all test objects and runs. Each entry shows Coverage (%), Completeness (cm), and AUC*

![[assets/figures/papers/paper_list_l2644_https_arxiv_org_abs_2604_19556/figures/007_Table_2.jpg]]
*Table 2: Quantitative comparison of different motion types averaged across all scenes. We evaluate four dynamic behaviors (Bouncing Ball (BB), Curved Bouncing Ball (CBB), Forward & Backward (FB), and Stop & Go (SG)) and report results for all test objects. Each cell shows Coverage (%), Completeness (cm), and AUC*

![[assets/figures/papers/paper_list_l2644_https_arxiv_org_abs_2604_19556/figures/014_Figure_7.jpg]]
*Figure 7: Coverage over exploration steps. Results are averaged across all scenes, motion patterns, and objects. Paparazzo consistently achieves higher coverage throughout the entire step budget. Shaded areas indicate the standard deviation across runs*

![[assets/figures/papers/paper_list_l2644_https_arxiv_org_abs_2604_19556/figures/020_Table_4.jpg]]
*Table 4: Reconstruction coverage (%) for Object 1 and Object 2 under the Stop & Go motion pattern. Paparazzo significantly outperforms all baselines*

![[assets/figures/papers/paper_list_l2644_https_arxiv_org_abs_2604_19556/figures/021_Figure_9.jpg]]
*Figure 9: Benchmark examples of active mapping of moving objects. In each scenario, the agent plans camera viewpoints around a moving target while compensating for its motion to acquire informative observations for reconstruction*

![[assets/figures/papers/paper_list_l2644_https_arxiv_org_abs_2604_19556/figures/022_Figure_10.jpg]]
*Figure 10: Examples of object trajectories. The moving target is performing the Bouncing Ball motion in the Denmark, Greigsville, and Ribera scenes (left to right). The agent executes the Paparazzo framework while continuously adapting its motion to track and map the moving object*

## 定位与知识库关联

### 问题定位：从静态主动建图到动态目标主动建图

传统主动建图（Active Mapping）方法的核心假设是**场景静态性**——智能体在固定环境中规划视点以最大化信息增益，目标物体的位姿在世界坐标系中保持不变。这一假设在机器人操作、自动驾驶、动态场景监控等实际应用中频繁失效：当目标物体自主运动时，智能体必须同时估计物体运动状态、预测其未来轨迹，并规划自身路径以在正确的时间到达信息量最大的观测位置。视点质量同时取决于**几何信息量**和**时间可达性**，二者之间存在根本性的权衡——一个信息量极高的视点若无法在物体通过前到达，则毫无价值。

Paparazzo正是在这一瓶颈上做出突破：它将主动建图的任务定义从静态场景扩展到**独立运动的非合作目标**，通过在物体局部参考系中定义候选视点并利用扩展卡尔曼滤波（EKF）预测物体未来位姿序列，将空间信息量与时间同步性纳入统一的代价函数进行联合优化。

### 基线对比与方法谱系

论文设置了三个基线方法，分别对应不同的策略层级，构成清晰的消融链条：

**Random Walk (RW)**：经典静态场景主动建图的最简基线。智能体在环境中随机移动，完全忽略物体位置和运动状态。其低性能（Bouncing Ball运动下平均覆盖率仅51.50%）为任务难度提供了下界参考，验证了“完全忽略物体位置的随机探索无法有效重建移动目标”这一直观判断。

**Tracking-Only (TO)**：纯被动跟踪策略。该基线仅使用EKF跟踪物体运动状态，通过Object Tracking Mode维持物体在视野中，但不进行任何主动视点选择。TO代表了“跟踪而不建图”的策略下界：在Forward & Backward运动下覆盖率仅62.05%，因为被动策略无法从多角度观察物体；在Stop & Go运动中，TO在物体静止时完全被动等待，错失了宝贵的多视角采集窗口。

**Random Informative Selection (RIS)**：Paparazzo的消融变体。RIS保留了基于FisherRF信息增益（EIG）的候选视点生成机制，但从信息量最高的候选视点中**随机选择**，忽略同步代价 $C_{\mathrm{sync}}$ 和EKF运动预测。RIS在Bouncing Ball运动下覆盖率为67.07%，相比Paparazzo的81.51%下降14.44个百分点，直接验证了“仅信息量选择不足以应对动态场景”的核心论断——时间同步性是不可或缺的决策维度。

从方法谱系角度看，Paparazzo位于**无学习（learning-free）主动感知**与**动态场景状态估计**的交汇点。其3D重建骨干基于**SplaTAM**（3D Gaussian Splatting的SLAM框架），运动估计采用经典的SE(3)上的扩展卡尔曼滤波，信息增益计算沿用**FisherRF**准则，视点选择策略则借鉴了foveated采样的思想。与基于强化学习或模仿学习的主动建图方法不同，Paparazzo完全依赖手工设计的代价函数和阈值规则，这使其具备良好的可解释性和零样本迁移能力，但也限制了其从历史经验中持续改进策略的可能性。

### 适用边界与局限

**单目标假设**：Paparazzo当前仅支持单个移动物体的重建。在多物体场景中，不同目标的运动模式可能相互独立或耦合，候选视点的定义和同步代价的计算需要从单目标参考系扩展到多目标联合空间，这一扩展并非平凡。

**分割依赖**：系统假设可获取目标物体的分割掩码（通过背景减法或运动分割），实际部署中分割质量直接影响物体位姿初始化和EKF观测更新的准确性。在不完全分割、动态遮挡或传感器噪声条件下，系统的鲁棒性尚未验证。

**EKF预测的脆弱性**：当物体突然改变运动方向时，恒速运动模型的EKF预测变得不可靠，系统需切换至Object Tracking Mode重新稳定估计。这一模式切换机制虽然保证了估计的可靠性，但在物体频繁变速的场景中可能导致系统长时间停留在跟踪模式，损失建图效率。论文在Ribera等狭窄场景中观察到的性能下降正源于此——智能体机动空间受限，难以在物体弹跳前及时重新定位。

**环境约束**：所有实验在Habitat 3.0模拟器中进行，使用512×512 RGB-D相机（90°视场角）。真实世界的传感器噪声、动态光照、非刚性变形等因素可能引入额外挑战。系统在线运行速度为8 FPS，在需要快速响应的场景中可能不足。

**参数敏感性**：系统的关键参数——EKF置信度阈值 $\tau_u=0.1$、$\tau_n=0.5$，连续稳定步数 $N_s=4$，预测步长 $N_h=60$，代价权重 $w_{\mathrm{eig}}=0.8$、$w_{\mathrm{sync}}=1.2$——均在验证集上经验确定。这些参数对不同物体尺寸、运动速度和场景尺度的泛化能力尚需进一步验证，目前缺乏针对不同场景自动调整参数的机制。

### 开放问题

1. **多目标扩展**：如何将候选视点定义和同步代价计算从单目标参考系扩展到多目标联合空间，同时处理目标间的相互遮挡和运动耦合？

2. **真实世界部署**：在不完全分割、传感器噪声和动态遮挡条件下，系统的位姿估计和建图质量如何保证？是否需要引入鲁棒估计或不确定性感知的分割方法？

3. **学习增强的运动预测**：能否将基于学习的轨迹预测（如神经网络运动预测器）与当前EKF框架结合，在保持在线运行效率的同时提高对复杂运动模式（如突然转向、变速）的泛化能力？

4. **参数自适应**：系统的关键阈值和权重能否根据场景特征（物体尺寸、运动速度、环境开阔度）自动调整，避免手工调参的局限性？

5. **与SLAM的集成**：该方法能否与未知环境中的同时定位与建图（SLAM）系统集成，在智能体自身位姿不确定的条件下同时进行环境建图和移动物体主动重建？

6. **非刚体扩展**：如何处理可变形物体的主动建图？这需要从根本上重新考虑状态表示（从SE(3)位姿到变形场）和信息增益的定义。

## 原文 PDF

![[paperPDFs/CVPR_2026/Paparazzo_Active_Mapping_of_Moving_3D_Objects.pdf]]
