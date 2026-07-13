---
title: Adaptive 3D Perception for Small Aerial Targets Under Sparse Sampling via Reinforcement Learning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Adaptive_3D_Perception_for_Small_Aerial_Targets_Under_Sparse_Sampling_via_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- A3PSATUSSRL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: RL策略在线调整的5维动作：体素缩放Δx_t、TDS检测阈值θ_T、VC检测阈值θ_V、关联门控τ_gate和动态评分分位数q。
primary_logic: 利用时序色散签名(TDS)编码稀疏LiDAR的时空分布，并将稀疏度、前景接受率和跟踪连续性等无标签统计量作为RL状态，形成一个闭环自适应感知系统，无需测试时标签。
claims:
- 在MMAUD V2/V3上，A3PRL实现总体RMSE 1.17 m，相比无RL版本(1.45 m)相对提升约19%。
- 对无标签观测和动作空间的消融实验表明，逐步引入跟踪连续性、接受率和前景密度可将RMSE从2.80 m降至2.12 m，证实了每个组件的必要性。
- MMAUD V2/V3 上 RMSE (m) = 1.17
- Multi-LiDAR Multi-UAV dataset 上 Mean Position RMSE (m) = 0.068
---

# Adaptive 3D Perception for Small Aerial Targets Under Sparse Sampling via Reinforcement Learning

> [!tip] 核心洞察
> 利用时序色散签名(TDS)编码稀疏LiDAR的时空分布，并将稀疏度、前景接受率和跟踪连续性等无标签统计量作为RL状态，形成一个闭环自适应感知系统，无需测试时标签。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于强化学习的稀疏采样下小型空中目标自适应三维感知 |
| 英文题名 | Adaptive 3D Perception for Small Aerial Targets Under Sparse Sampling via Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yuan_Adaptive_3D_Perception_for_Small_Aerial_Targets_Under_Sparse_Sampling_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | A3PRL |
| Dataset | MMAUD V2/V3, Multi-LiDAR Multi-UAV dataset, In-house LiDAR-RTK rig |

> [!tip] 效果简介
> - MMAUD V2/V3 上，RMSE (m) 1.17 vs A3PRL (w/o RL) 1.45 (-0.28 (~19%))；RMSE (m) 1.17 vs U3DTE 1.76 (-0.59)。
> - Multi-LiDAR Multi-UAV dataset 上，Mean Position RMSE (m) 0.068 vs U3DTE 0.078 (-0.01 (~14%))。
> - In-house LiDAR-RTK rig 上，RTK-referenced RMSE (m) 1.55 (full RL) vs U3DTE 2.30 / A3PRL (non-adaptive) 1.90 (-0.35 (vs non-adaptive) / -0.75 (vs U3DTE))。

## 概要

**问题瓶颈**：长距离稀疏LiDAR扫描下，小型空中目标（如无人机）的点云密度随距离、速度和姿态发生剧烈波动。固定体素分辨率与静态检测阈值无法适应这种稀疏度变化，导致传统LiDAR检测器在敏捷无人机场景中崩溃——点云回波稀疏到与背景噪声难以区分。

**核心思路**：A3PRL 将感知流水线建模为闭环自适应系统，通过强化学习策略在线调整五个关键控制参数——体素缩放 $\Delta x_t$、TDS检测阈值 $\theta_T$、VC检测阈值 $\theta_V$、关联门控 $\tau_{\mathrm{gate}}$ 和动态评分分位数 $q$。策略以无标签统计量（稀疏度、前景接受率、跟踪连续性）为状态，无需测试时标注即可感知场景变化并实时调节检测器行为。

**方法定位**：A3PRL 在检测前端采用时序色散签名（Temporal Dispersion Signature, TDS）编码滑动窗口内LiDAR点云的时空分布，与速度变化（Velocity Change, VC）头并行生成候选体素；后端通过自适应评分融合与序贯概率比检验（SPRT）进行前景确认，并由卡尔曼滤波器维持轨迹。RL策略作为外层控制器，以PPO训练，奖励函数同时惩罚几何误差、时间不连续性和接受率偏离期望。

**主要结果**：在MMAUD V2/V3跨地点评测中，A3PRL 实现总体RMSE 1.17 m，相比无RL版本（1.45 m）相对提升约19%，相比无监督基线U3DTE（1.76 m）提升约34%。在自建LiDAR-RTK平台上，RTK参考RMSE从U3DTE的2.30 m降至1.55 m。消融实验证实，逐步引入跟踪连续性、接受率和前景密度等无标签观测可将RMSE从2.80 m持续降至2.12 m，完整5D动作空间进一步降至1.17 m，验证了每个组件的必要性。



### 问题背景：稀疏采样下小型空中目标感知的挑战

小型空中目标（Small Aerial Targets, SATs）——如消费级无人机、物流配送无人机——在现代空域安全、城市空中交通管理等场景中日益重要。然而，对这类目标进行鲁棒的三维检测与跟踪面临一个根本性瓶颈：**长距离稀疏LiDAR点云导致固定参数检测器系统性崩溃**。如图2所示，当无人机处于慢速飞行时，LiDAR回波已丧失几何结构；当无人机高速飞行或处于高空时，点云极度稀疏，回波与背景噪声难以区分。

这一瓶颈的因果链条可以归结为：目标尺寸小（通常低于0.5 m）、运动速度快、观测距离变化大，三者共同导致**点密度在时空维度上剧烈波动**。传统LiDAR检测器依赖固定体素分辨率、固定检测阈值和固定关联门控，无法适应这种密度波动，在稀疏帧中漏检、在密集帧中虚警，最终导致轨迹断裂或定位误差急剧增大。

### 现有方法的缺口

当前面向空中目标感知的方法可分为三类，但均未有效解决上述自适应性问题：

- **有监督视觉检测器**（如DarkNet、YOLOv5s、VisualNet、RTDETR）依赖RGB图像，在夜间或强光干扰下性能退化严重，且无法直接输出三维定位。
- **有监督音频检测器**（如Vora et al., MobiSys 2023）受限于声学传播距离和方向性，仅适用于近距离场景。
- **无监督LiDAR检测器**（如U3DTE, Liang et al., ICASSP 2025）虽不依赖标注，但仍采用**固定体素化和静态阈值**，在稀疏采样下无法自适应调整，导致其RMSE高达1.76 m（MMAUD基准）。

更关键的是，现有方法普遍缺乏一个**闭环自适应机制**：它们将感知流水线的参数（体素尺寸、检测阈值、关联门控）视为静态超参数，由人工离线调参确定。一旦场景的点密度、目标速度或距离分布发生变化，这些固定参数便成为性能瓶颈。

### 本文动机：从开环检测到闭环自适应感知

本文的核心洞察是：**稀疏LiDAR的时空分布本身携带着可用于自适应的信息**。具体而言，时序色散签名（Temporal Dispersion Signature, TDS）能够编码点云在滑动窗口内的时空紧致度与帧稀疏度，这些统计量天然反映了场景的稀疏程度和目标运动状态。若能将稀疏度、前景接受率和跟踪连续性等**无标签统计量**作为反馈信号，驱动感知流水线参数在线调整，便可形成一个**无需测试时标签的自适应闭环系统**。

基于这一洞察，本文提出A3PRL——一个基于强化学习的自适应三维感知框架。RL策略以无标签稠密统计量为状态，输出5维连续动作（体素缩放 $\Delta x_t$、TDS检测阈值 $\theta_T$、VC检测阈值 $\theta_V$、关联门控 $\tau_{\mathrm{gate}}$ 和动态评分分位数 $q$），实时调节感知流水线，使系统在点密度剧烈波动的条件下保持鲁棒。这一设计将感知问题重新定义为**主动感知问题**：检测器不再是固定函数，而是由策略根据场景动态配置的可调模块。



## 核心方法与创新机理

A3PRL 的核心创新在于将**无监督自适应感知**建模为一个强化学习闭环控制问题，使稀疏 LiDAR 检测–跟踪流水线能够根据场景稀疏度、运动模式和目标距离**在线调节**五个关键参数，从而解决固定参数检测器在长距离、高机动小型空中目标场景下的大幅性能退化。

### 问题瓶颈与因果调节变量

**真实瓶颈**：长距离稀疏 LiDAR 导致固定参数检测器崩溃——固定体素化和静态阈值无法适应目标尺寸、速度和距离变化引起的点密度剧烈波动（Figure 2）。传统 LiDAR 检测器在处理静态或大型慢速目标时表现良好，但面对敏捷无人机时，即使慢速飞行也会丢失几何结构，快速或高空无人机产生的稀疏回波则与背景噪声难以区分。

**因果调节变量（5D 动作空间）**：RL 策略在线调整的五维连续动作直接作用于感知流水线的关键决策点：

$$a_t = (\Delta x_t, \theta_T, \theta_V, \tau_{\mathrm{gate}}, q)$$

| 动作维度 | 作用对象 | 调节机制 |
|---------|---------|---------|
| $\Delta x_t$ | 体素缩放因子 | 各向同性缩放体素分辨率，适应点密度变化 |
| $\theta_T$ | TDS 检测头阈值 | 控制时序色散签名头的前景提案灵敏度 |
| $\theta_V$ | VC 检测头阈值 | 控制速度变化头的前景提案灵敏度 |
| $\tau_{\mathrm{gate}}$ | 关联门控阈值 | 动态调节马氏距离门控，反映当前检测稀疏度 |
| $q$ | 动态评分分位数 | 控制自适应评分的前景接受阈值 |

### 核心洞察：无标签闭环自适应

A3PRL 的核心洞察在于**利用无需测试时标签的稠密统计量作为 RL 状态**，形成一个闭环自适应感知系统。策略观察的统计量包括：

- **稀疏度**：体素内点的时空分布密度
- **前景接受率**：检测器输出的前景提案被接受的比率
- **跟踪连续性**：时序关联的稳定性指标

这些统计量直接从 LiDAR 点云和检测–跟踪流水线的中间输出中提取，无需任何人工标注。RL 策略通过 PPO 训练，奖励函数同时惩罚几何误差、时间不连续性和接受率偏离期望：

$$r_t = -\big(\lambda_1 \varepsilon_t + \lambda_2 (1 - \xi_t) + \lambda_3 |\rho_t - \tau_{\rho}|\big)$$

### 与 baseline 的关键差异

与无 RL 变体 **A3PRL (w/o RL)** 相比，A3PRL 的 changed slots 体现在流水线的四个关键环节：

1. **体素化阶段**：从固定体素尺寸 $(\delta_x, \delta_y, \delta_z)$ 变为策略驱动的自适应缩放 $\Delta x_t \cdot (\delta_x, \delta_y, \delta_z)$
2. **提案生成阶段**：TDS 和 VC 头的检测阈值 $\theta_T$、$\theta_V$ 从静态变为动态
3. **关联阶段**：门控阈值 $\tau_{\mathrm{gate}}$ 从固定值变为策略调节
4. **评分阶段**：动态阈值分位数 $q$ 替代固定阈值

这种自适应机制使 A3PRL 在 MMAUD V2/V3 跨场景评估中取得总体 RMSE **1.17 m**，相比无 RL 版本（1.45 m）相对提升约 **19%**，相比无监督 LiDAR 基线 **U3DTE**（Liang et al., ICASSP 2025）的 1.76 m 降低 0.59 m（Table 1）。

### 消融验证：组件必要性的因果链

消融实验（Table 2）通过逐步引入观测和动作维度，揭示了各组件的因果贡献链：

- 仅使用体素密度观测 + 体素缩放动作时，RMSE 为 2.80 m
- 加入跟踪连续性指标 $\xi_t$ 后降至 2.55 m
- 加入无标签接受率 $\rho_t$ 后降至 2.33 m
- 加入前景密度 $\bar{s}_F$ 后降至 2.12 m
- 加入置信度阈值控制后降至 1.95 m
- 加入关联门控控制后降至 1.72 m
- 完整 5D 动作空间达到 **1.17 m**

模块消融（Table 4）进一步表明，移除 TDS 头导致最大误差增加至 2.84 m，证实了时序色散签名在稀疏场景下的关键作用。



A3PRL 将稀疏 LiDAR 点云下的空中小目标感知建模为一个闭环自适应优化问题。其核心思路是：感知流水线的关键参数（体素分辨率、检测阈值、关联门控等）不再由人工静态设定，而是由一个轻量级强化学习策略根据当前场景的稀疏度与跟踪状态实时调节，从而在点密度剧烈波动的条件下维持稳定的检测-跟踪性能。

### 系统闭环结构

如图 3 所示，系统按帧迭代运行，每一帧的数据流与决策流形成闭环：

1. **输入**：滑动窗口内的稀疏 LiDAR 点云 $\mathcal{P}_t$。
2. **感知流水线** $f(\cdot; \Delta x_t, \theta_T, \theta_V, \tau_{\mathrm{gate}}, q)$：以当前策略给出的参数为条件，对 $\mathcal{P}_t$ 执行体素化、双头候选生成、自适应评分与接受控制、关联与状态更新，输出当前帧的检测结果 $X_t$。
3. **RL 策略** $\pi_\phi(s_t^{\mathrm{inf}})$：从感知流水线的中间统计量中提取无标签观测状态 $s_t^{\mathrm{inf}}$，输出 5 维连续动作 $a_t = (\Delta x_t, \theta_T, \theta_V, \tau_{\mathrm{gate}}, q)$，用于调节下一帧的感知参数。

这一闭环可形式化为：

$$\mathcal{P}_t \xrightarrow{f(\cdot; \Delta x_t, \theta_T, \theta_V, \tau_{\mathrm{gate}}, q)} X_t, \quad a_t = \pi_\phi(s_t^{\mathrm{inf}})$$

策略的训练目标是最大化期望累积奖励，奖励函数同时惩罚几何定位误差、时间不连续性以及前景接受率偏离期望区间，从而在无需测试时标签的条件下引导策略学会自适应调节。

### 感知流水线模块分解

感知流水线由四个核心模块串联构成，每个模块的行为均受 RL 策略输出的动作参数实时调控：

| 模块 | 功能 | 受控参数 |
|------|------|----------|
| **时空张量化** (Temporal Dispersion Signature Tensorization) | 将滑动窗口 LiDAR 点云转化为包含时间紧致度 $s_T$ 与帧稀疏度 $s_F$ 的 4D 时空张量 $T_t$ | 体素缩放因子 $\Delta x_t$ |
| **双头候选生成** (Dual-Head Proposal Generation) | TDS 头利用 $s_T$、$s_F$ 检测时空紧致的前景体素；VC 头利用速度变化线索补充检测 | 检测阈值 $\theta_T$、$\theta_V$ |
| **自适应评分与接受控制** (Adaptive Scoring & Acceptance Control) | 融合多源置信度得分 $\psi(v)$，采用分位数动态阈值与序贯概率比检验（SPRT）确认前景 | 动态分位数 $q$ |
| **关联与状态更新** (Association & State Update) | 基于马氏距离的自适应门控关联，结合单目标卡尔曼滤波进行轨迹预测与更新 | 关联门控 $\tau_{\mathrm{gate}}$ |

### 策略观测空间

RL 策略的观测状态 $s_t^{\mathrm{inf}}$ 完全由无标签统计量构成，不依赖测试时的真值标注。消融实验（Table 2）证实了各观测分量的必要性：逐步引入跟踪连续性指标 $\xi_t$、无标签接受率 $\rho_t$ 和前景密度 $\bar{s}_F$，RMSE 从仅使用体素密度的 2.80 m 逐步降至 2.12 m，表明这些稠密统计量有效编码了当前场景的稀疏度与检测质量，为策略决策提供了充分的信息基础。

### 部署时的平滑机制

在训练阶段，策略通过 PPO 在 MMAUD V1 的噪声增强数据上学习，并引入真实 LiDAR 噪声域随机化（模拟户外太阳干扰）以提升跨域泛化能力。部署时，对策略输出的连续动作施加指数移动平均，确保参数的自适应调整平滑稳定，避免单帧抖动对流水线造成冲击。

### 补充图表

![[assets/figures/papers/paper_list_l2713_https_openaccess_thecvf_com_content_CVPR2026_html_Yuan_Adaptive_3D_Perce/figures/003_Figure_3.jpg]]
*Figure 3: Local-window sparse LiDAR streams are voxelized into spatiotemporal tensors. Candidate SATs are proposed by TDS and VC heads, fused through adaptive scoring, and tracked via lightweight association for stable trajectory estimation. The RL policy learns from perception observations to dynamically adjust voxelization and scoring parameters*

![[assets/figures/papers/paper_list_l2713_https_openaccess_thecvf_com_content_CVPR2026_html_Yuan_Adaptive_3D_Perce/figures/002_Figure_2.jpg]]
*Figure 2: Conventional LiDAR detectors handle static or large, slow-moving objects well [13], but fail on agile UAVs [61]. Even slow flights lose geometric structure, while fast or high-altitude UAVs yield sparse echoes indistinguishable from background noise*



### 问题形式化与闭环自适应框架

A3PRL 将稀疏 LiDAR 下的空中小目标感知形式化为一个闭环自适应感知-控制问题。在每一时间步 $t$，系统接收局部滑动窗口内的点云 $\mathcal{P}_t$，通过参数可调的检测-跟踪流水线 $f(\cdot; \Delta x_t, \theta_T, \theta_V, \tau_{\mathrm{gate}}, q)$ 输出目标状态估计 $X_t$。RL 策略 $\pi_\phi$ 根据无标签感知观测 $s_t^{\mathrm{inf}}$ 输出 5 维连续动作 $a_t$，实时调节流水线参数：

$$a_t = (\Delta x_t, \theta_T, \theta_V, \tau_{\mathrm{gate}}, q)$$

其中 $\Delta x_t$ 为各向同性体素缩放因子，$\theta_T$ 和 $\theta_V$ 分别为时间色散头（TDS）和速度变化头（VC）的检测阈值，$\tau_{\mathrm{gate}}$ 为关联门控阈值，$q$ 为动态评分分位数。策略以最大化折扣累积奖励为目标，奖励函数联合惩罚几何误差、时间不连续性和接受率偏离：

$$r_t = -\big(\lambda_1 \varepsilon_t + \lambda_2 (1 - \xi_t) + \lambda_3 |\rho_t - \tau_{\rho}|\big)$$

### 时空张量化与双头提案生成

**时空张量化** 将滑动窗口内的稀疏点云 $\mathcal{P}_t$ 映射为 4D 时空张量 $\mathcal{T}_t$。对每个体素 $v$，记录其内部点的时间跨度 $\Delta T(v) = \tau_{\max}(v) - \tau_{\min}(v)$ 和被占用帧比例 $\kappa(v)$，进而定义两个核心时空签名：

$$s_T(v) = 1 - \frac{\Delta T(v)}{W}, \quad s_F(v) = 1 - \kappa(v)$$

其中 $s_T(v)$ 衡量时间紧致度（体素内点的时间跨度相对窗口长度 $W$ 的紧凑程度），$s_F(v)$ 衡量帧稀疏度（体素被占用的帧比例）。这两个签名共同构成 **时序色散签名（TDS）**，编码了稀疏 LiDAR 点云的时空分布特征。

**TDS 头** 基于上述签名生成原始检测分数：

$$\phi_T(v) = w_T s_T(v) + w_F s_F(v)$$

**VC 头** 则利用速度一致性线索，计算体素内点的短时速度变化，提供互补的运动敏感度。双头并行生成候选体素，经自适应阈值 $\theta_T$、$\theta_V$ 筛选后进入融合阶段。

### 自适应评分与序贯接受控制

每个候选体素 $v$ 获得融合置信度分数：

$$\psi(v) = \alpha s_T(v) + \beta s_F(v) + \gamma s_V(v) + \delta s_S(v)$$

该分数加权组合了时间紧致度 $s_T$、帧稀疏度 $s_F$、速度一致性 $s_V$ 和空间稳定性 $s_S$ 四类线索。速度一致性分数定义为：

$$s_V(v) = 1 - \frac{1}{L} \sum_{\ell=1}^{L} \frac{\| \mathbf{u}_t(v) - \mathbf{u}_{t-\ell}(v) \|_2}{\| \mathbf{u}_t(v) \|_2 + \varepsilon}$$

其中 $\mathbf{u}_t(v)$ 为体素 $v$ 在当前帧的估计速度向量，通过 $L$ 帧回溯计算速度方向的一致性。

前景确认采用 **序贯概率比检验（SPRT）**，累积对数似然比统计量：

$$S_k = \sum_{m=1}^{k} \log \frac{P(y_{t_m}(v) \mid H_1)}{P(y_{t_m}(v) \mid H_0)}$$

其中 $H_1$ 为前景假设，$H_0$ 为背景假设。当 $S_k$ 超过上下界阈值时做出接受/拒绝决策，替代固定阈值判决，在稀疏观测下提供统计上更可靠的前景确认机制。

### 关联门控与状态更新

确认的前景体素通过自适应门控的马氏距离进行数据关联。门控阈值 $\tau_{\mathrm{gate}}$ 由 RL 策略动态调节，以适应检测稀疏度的变化。马氏距离定义为：

$$d_p(i) = \| \mathbf{S}_t^{-1/2} \mathbf{r}_t^{(i)} \|_2$$

其中 $\mathbf{S}_t = \mathbf{H} \Sigma_{t \mid t-1} \mathbf{H}^{\top} + \mathbf{R}$ 为新息协方差，$\mathbf{r}_t^{(i)}$ 为第 $i$ 个候选检测的新息向量。关联成功后，采用标准卡尔曼滤波进行状态更新，运动模型为常速度模型：

$$\hat{\mathbf{x}}_{t \mid t-1} = \mathbf{F} \hat{\mathbf{x}}_{t-1}, \quad \Sigma_{t \mid t-1} = \mathbf{F} \Sigma_{t-1} \mathbf{F}^{\top} + \mathbf{Q}$$

### RL 策略的无标签观测设计

策略 $\pi_\phi$ 的观测空间由三类无标签稠密统计量构成：**跟踪连续性** $\xi_t$（衡量当前轨迹的时间连贯性）、**前景接受率** $\rho_t$（SPRT 接受的前景体素比例）和 **前景密度** $\bar{s}_F$（前景区域的平均帧稀疏度）。这些统计量无需测试时真值标签，形成闭环自监督信号。消融实验证实，逐步引入这三类观测可将 RMSE 从 2.80 m 降至 2.12 m，验证了每个组件的必要性。



## 实验与关键发现

### 跨域泛化主结果

表1报告了在MMAUD V2/V3上的跨地点评估结果：策略仅在V1上训练，在未见过的V2/V3场景上测试，直接检验自适应策略的泛化能力。A3PRL（完整RL自适应）取得总体RMSE **1.17 m**，相比无RL启发式调参版本A3PRL (w/o RL)的1.45 m，相对提升约19%。这一差距的核心驱动力在于RL策略能够根据场景稀疏度在线调整体素分辨率、检测阈值和关联门控，而非依赖固定的手工参数。

与LiDAR-only基线对比，无监督方法**U3DTE** (Liang et al., ICASSP 2025) 的RMSE为1.76 m，A3PRL将其降低了约0.59 m。有监督视觉检测器如**RTDETR** (Zhao et al., CVPR 2024)、**VisualNet** (Yang et al., JAI 2024) 等受限于视场遮挡和光照条件，在夜间或遮挡场景下性能退化明显，而A3PRL的LiDAR-only设计天然具备全天候鲁棒性。

在自建LiDAR-RTK真值平台上进一步验证：RTK参考系下，U3DTE的RMSE为2.30 m，非自适应A3PRL降至1.90 m，完整RL版本进一步降至**1.55 m**，相比U3DTE降低约0.75 m。这一跨平台验证排除了仿真域偏差，证实了自适应策略在真实部署中的有效性。

在多LiDAR多无人机数据集上，A3PRL的平均位置RMSE为**0.068 m**，优于U3DTE的0.078 m（约14%相对提升），表明策略在多传感器配置下同样具备迁移能力。

### 无标签观测与动作空间消融

表2的系统消融揭示了RL策略中每个无标签观测信号和动作维度的边际贡献，实验从最弱配置（仅观测体素密度、仅调控体素缩放）逐步累加至完整5D动作空间：

- **基线（A）**：仅体素密度观测 + 仅体素缩放动作，RMSE高达2.80 m。此时策略对目标运动状态和检测质量完全盲视，仅能粗粒度调整空间分辨率。
- **+跟踪连续性ξ_t（B）**：RMSE降至2.55 m。策略开始感知时序断裂，能够在轨迹中断时主动调整参数以恢复跟踪。
- **+接受率ρ_t（C）**：RMSE降至2.33 m。策略获得检测流水线输出质量的反馈信号，可据此调节阈值以平衡虚警与漏检。
- **+前景密度s̄_F（D）**：RMSE降至2.12 m。策略能区分前景体素与背景噪声的稀疏度差异，在点云极度稀疏时做出更精准的判断。
- **+置信度阈值控制（E）**：RMSE降至1.95 m。引入对检测阈值θ_T、θ_V的调控能力，策略可根据场景动态放宽或收紧提案接受标准。
- **+关联门控控制（F）**：RMSE降至1.72 m。自适应门控τ_gate使数据关联能适应目标机动引起的预测不确定性变化。
- **完整5D动作（G）**：RMSE达到1.17 m。体素缩放Δx_t、双检测阈值θ_T/θ_V、关联门控τ_gate和动态评分分位数q的联合调控形成闭环，各维度协同应对稀疏度、运动速度和距离的复合变化。

消融趋势表明：**观测信号的边际收益递减但持续为正**，每个无标签统计量都为策略提供了不可替代的环境感知能力；**动作空间的扩展收益更为显著**，尤其是检测阈值和关联门控的引入带来了阶跃式提升。

### 模块消融与TDS头关键性

表4左侧的模块消融直接验证了各感知组件的必要性：**移除TDS（时间色散签名）头导致最大误差增加至2.84 m**，远超其他模块移除的影响。这一结果表明，在稀疏LiDAR条件下，时序分布特征（时间紧致度s_T和帧稀疏度s_F）是区分真实小目标和随机噪声的核心判别信号——单帧点云缺乏足够的几何结构，而多帧时序签名弥补了这一信息缺口。

相比之下，移除VC（速度变化）头或简化融合策略的退化幅度较小，说明在极稀疏场景中，运动线索的可靠性受限于点云本身的信噪比，TDS提供的时空统计量更为稳健。

### 策略网络深度与简单自适应基线

表3显示策略MLP深度从2层增至4层时性能持续改善，但5层出现轻微过拟合（需手动验证具体数值）。轻量MLP设计（最终采用4层，参数量极小）是策略能以约51.2 ms总延迟在线运行的关键。

表4右侧对比了简单自适应基线：基于启发式规则（如点云密度阈值触发参数切换）的方案远不及学习型策略，验证了稀疏度-运动-检测质量之间的耦合关系难以手工建模，RL的价值在于从数据中自动发现这些非线性映射。

### 实时性分析

表5的逐帧延迟剖析显示，在线自适应循环的总延迟约**51.2 ms**，其中体素化和张量化占主导，策略推理仅需亚毫秒级。这一延迟水平支持约20 Hz的感知更新率，足以应对小型无人机的机动。但需注意：在更高输入帧率或更多目标场景下，延迟瓶颈可能转移至数据关联和后端优化，当前设计未对此进行压力测试。

### 失败模式与局限性

基于消融和跨域实验结果，可归纳以下失败模式：

1. **TDS头失效场景**：当目标悬停或极低速运动时，时间跨度ΔT(v)接近窗口长度W，s_T趋近于0，TDS头退化为纯帧稀疏度检测器，与背景噪声的区分度下降。这解释了为何VC头在低速段提供互补信号。
2. **单目标假设边界**：当前框架的关联模块和RL状态设计均假设场景中仅存在一个待跟踪目标。多目标场景下，接受率ρ_t和跟踪连续性ξ_t的语义将模糊化（无法区分是哪个目标中断），策略可能产生错误的自适应行为。
3. **域随机化的覆盖盲区**：训练阶段使用MCD真实LiDAR噪声增强以模拟太阳干扰，但未涵盖雨雾衰减、多径反射等极端条件。在未见过的强背景干扰下，前景密度s̄_F的估计偏差可能导致策略误判稀疏度。
4. **奖励函数对GT轨迹的依赖**：训练时需GT轨迹计算几何误差ε_t，这限制了策略在完全无标签新场景的持续学习能力。未来可探索自监督替代信号（如点云重投影一致性）以解除此约束。

### 补充图表

![[assets/figures/papers/paper_list_l2713_https_openaccess_thecvf_com_content_CVPR2026_html_Yuan_Adaptive_3D_Perce/figures/005_Table_1.jpg]]
*Table 1: Cross-venue evaluation on MMAUD [61]: train on V1 and test on unseen V2/V3 subsets collected at different locations and platforms. This setting stresses generalization of the adaptive LiDAR policy beyond the training venue*

![[assets/figures/papers/paper_list_l2713_https_openaccess_thecvf_com_content_CVPR2026_html_Yuan_Adaptive_3D_Perce/figures/006_Table_2.jpg]]
*Table 2: Ablation on label-free observations and action space on MMAUD V2/V3*

![[assets/figures/papers/paper_list_l2713_https_openaccess_thecvf_com_content_CVPR2026_html_Yuan_Adaptive_3D_Perce/figures/009_Table_4.jpg]]
*Table 4: Ablation (left) and simple adaptive baselines (right)*

![[assets/figures/papers/paper_list_l2713_https_openaccess_thecvf_com_content_CVPR2026_html_Yuan_Adaptive_3D_Perce/figures/004_Figure_4.jpg]]
*Figure 4: Experimental results of the proposed A3PRL pipeline*

![[assets/figures/papers/paper_list_l2713_https_openaccess_thecvf_com_content_CVPR2026_html_Yuan_Adaptive_3D_Perce/figures/008_Table_5.jpg]]
*Table 5: Per-frame runtime of the online adaptive loop on our deployment setup. The average latency is 51.2 ms and the*

![[assets/figures/papers/paper_list_l2713_https_openaccess_thecvf_com_content_CVPR2026_html_Yuan_Adaptive_3D_Perce/figures/007_Table_3.jpg]]
*Table 3: Effect of policy MLP depth on MMAUD V2/V3*

![[assets/figures/papers/paper_list_l2713_https_openaccess_thecvf_com_content_CVPR2026_html_Yuan_Adaptive_3D_Perce/figures/001_Figure_1.jpg]]
*Figure 1: Conceptual illustrations of representative small aerial target scenarios. From guided delivery drones landing [49] to ensure airliner safety [1], robust SATs detection and tracking are essential*



## 定位与知识库关联

### 1. 与现有工作的关系

A3PRL 处于**无监督三维小目标感知**与**自适应感知系统**的交叉点。与现有基线相比，其核心差异在于引入强化学习策略对感知流水线进行闭环在线调控，而非依赖固定参数或启发式规则。

**相对于有监督视觉检测器**：DarkNet (Liu et al., Sensors 2021)、YOLOv5s (Zhang et al., Sustainability 2022)、VisualNet (Yang et al., JAI 2024) 和 RTDETR (Zhao et al., CVPR 2024) 等视觉方法依赖大规模标注数据训练，在夜间或低光照条件下性能受限。A3PRL 以 LiDAR 为主传感器，不依赖视觉标注，在昼夜条件下均能稳定工作。类似地，基于音频的检测方法 (Vora et al., MobiSys 2023) 受环境噪声影响较大，而 LiDAR 点云在稀疏采样下虽面临密度波动，但不受光照和声学干扰的直接影响。

**相对于无监督 LiDAR 检测器**：U3DTE (Liang et al., ICASSP 2025) 是本文最直接的无监督 LiDAR 基线。U3DTE 采用固定的体素化和静态检测阈值，在稀疏点云条件下难以适应目标距离和速度变化引起的点密度剧烈波动。在 MMAUD V2/V3 跨域评估中，U3DTE 的 RMSE 为 1.76 m，而 A3PRL 达到 1.17 m，相对降低约 33%。这一差距的根源在于：U3DTE 的固定参数在长距离稀疏场景下要么漏检（阈值过高），要么产生大量虚警（阈值过低），而 A3PRL 的 RL 策略可根据当前帧的稀疏度统计量实时调整体素缩放 $\Delta x_t$ 和检测阈值 $(\theta_T, \theta_V)$，在检测召回与精度之间动态平衡。

**相对于非自适应变体**：A3PRL (w/o RL) 是本文自身的启发式调参版本，使用手工设定的固定参数。该变体在 MMAUD 上取得 1.45 m RMSE，而完整 A3PRL 的 1.17 m 对应约 19% 的相对提升。这一对比直接量化了 RL 自适应策略的增益，证明在线参数调控优于任何静态参数组合。

**方法谱系定位**：A3PRL 可视为将**主动感知**（active perception）范式引入稀疏 LiDAR 小目标跟踪领域的首次尝试。其 RL 策略以无标签统计量（稀疏度、前景接受率、跟踪连续性）为状态，输出连续动作调控下游检测-跟踪流水线，形成“感知-决策-调整”闭环。这一架构与机器人领域的主动视觉和自适应传感有思想渊源，但在小目标 LiDAR 感知场景中尚无先例。

### 2. 适用边界

A3PRL 的设计假设和评估范围定义了其当前适用边界：

- **传感器模态**：专为机械旋转式 LiDAR 设计，利用多帧扫描的时间累积构建时空张量。对固态 LiDAR 或单帧 flash LiDAR 的适应性未经验证。
- **目标类型**：面向小型空中目标（SATs），如消费级无人机。目标尺寸在亚米级，点云回波极为稀疏（单帧可能仅 1-3 个点）。对更大或更密集的目标，TDS 头的时序色散签名可能失去区分度。
- **跟踪模式**：当前框架仅支持**单目标跟踪**。流水线中的关联模块和卡尔曼滤波均假设单一轨迹，未提供多目标场景下的数据关联和轨迹管理机制。
- **运动假设**：卡尔曼滤波采用匀速运动模型。对剧烈机动（急转弯、快速加减速）的目标，模型失配可能导致跟踪发散。
- **环境条件**：训练阶段通过 MCD（Monte-Carlo Dropout 风格的 LiDAR 噪声注入）模拟了日照干扰噪声，但未在真实暴雨、浓雾、沙尘等极端天气下评估。强背景杂波（如飞鸟群、飘落物）下的鲁棒性也未经测试。
- **部署平台**：实时自适应循环的总延迟约 51.2 ms（见 Table 5），对应约 20 Hz 的处理帧率。在更高输入帧率或资源更受限的边缘设备上，策略推理和体素化可能成为瓶颈。

### 3. 局限与开放问题

**方法局限**：

1. **训练依赖标注轨迹**：尽管推理阶段完全无标签，RL 策略的训练仍需 GT 轨迹计算奖励函数 $r_t$ 中的几何误差项 $\varepsilon_t$。这限制了策略在完全无标签新场景中的持续学习能力。
2. **单目标假设**：关联门控 $\tau_{\mathrm{gate}}$ 和卡尔曼滤波均针对单一轨迹设计，无法处理多目标交叉、新目标出现或目标消失等场景。
3. **传感器与平台泛化**：仅在有限种类的 LiDAR（如 16/32 线）和旋翼无人机上评估。对不同线数 LiDAR 或固定翼飞行器（运动模式差异大）可能需要重新训练策略。
4. **手工特征依赖**：TDS 和 VC 头的检测分数基于手工设计的时空统计量（$s_T, s_F, s_V, s_S$），而非学习到的特征表示。在复杂背景下，这些特征可能缺乏足够的判别力。
5. **实时性边界**：总延迟 51.2 ms 中，策略推理仅占约 0.3 ms（Table 5），主要开销在体素化和特征提取。若需支持更高帧率，需优化前端流水线。

**开放问题**：

- **多目标扩展**：如何将自适应门控和 SPRT 接受控制扩展到多目标场景？可能的路径包括引入联合概率数据关联（JPDA）或随机有限集（RFS）框架，并让 RL 策略调控多目标关联的超参数。
- **自监督微调**：能否利用推理阶段的无标签统计量（如 $\xi_t, \rho_t, \bar{s}_F$）设计自监督损失，在部署过程中持续微调策略网络，实现终身自适应？
- **学习化检测头**：将手工设计的 TDS/VC 头替换为轻量学习化检测器（如 PointNet 变体或稀疏卷积），并由 RL 策略调控其置信度阈值，可能进一步提升判别力。但需权衡训练数据需求和泛化性。
- **边缘部署优化**：在微控制器或 NPU 上部署 RL 策略（当前为浅层 MLP，Table 3 显示 2-3 层即可），并量化/剪枝前端体素化模块，以支持 50+ Hz 的实时处理。
- **极端条件鲁棒性**：在真实暴雨、浓雾、强光干扰等条件下系统评估，并探索域随机化策略（如更激进的点丢弃和噪声注入）是否足以覆盖这些退化模式。



## 原文 PDF

![[paperPDFs/CVPR_2026/Adaptive_3D_Perception_for_Small_Aerial_Targets_Under_Sparse_Sampling_via_Reinforcement_Learning.pdf]]
