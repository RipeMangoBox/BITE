---
title: "E-3DPSM: A State Machine for Event-based Egocentric 3D Human Pose Estimation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/E_3DPSM_A_State_Machine_for_Event_based_Egocentric_3D_Human_Pose_Estimation.pdf
project_link: null
code_link: null
aliases:
- E3
- E-3DPSM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将姿态估计重新定义为连续的时间动态过程：引入连续状态机（SSM）根据异步事件流不断演化潜在状态，并预测与事件变化对应的三维关节位移（delta pose），同时通过一个可学习的类卡尔曼滤波器自适应融合直接姿态预测和 delta 更新，从而从根本上消除了抖动和漂移。
primary_logic: 事件相机天然记录变化，因此三维空间中应存在对应的变化。通过将自我中心事件数据建模为连续动态过程，并利用 SSM 的长程时序建模能力以及 delta 姿态回归与学习型融合策略，可以在保持实时性的同时显著提升三维姿态的准确性和时间稳定性。
claims:
- E-3DPSM 在 EE3D-R 和 EE3D-W 两个基准上将 MPJPE 和 PA-MPJPE 降低约 19%，并将时间抖动最多降低 2.7 倍。
- 移除 SSM 模块导致精度和光滑度严重下降；改用简单加法融合则导致严重漂移，而提出的学习型融合有效抑制了漂移。
- 连续状态演化（无重置）优于定期重置 SSM 或 Kalman 状态，证明模型学会了自我调节内部状态。
- EE3D-R 上 MPJPE = 81.32 (Non-Causal)
---

# E-3DPSM: A State Machine for Event-based Egocentric 3D Human Pose Estimation

> [!tip] 核心洞察
> 事件相机天然记录变化，因此三维空间中应存在对应的变化。通过将自我中心事件数据建模为连续动态过程，并利用 SSM 的长程时序建模能力以及 delta 姿态回归与学习型融合策略，可以在保持实时性的同时显著提升三维姿态的准确性和时间稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | E-3DPSM：面向事件驱动式自我中心三维人体姿态估计的状态机 |
| 英文题名 | E-3DPSM: A State Machine for Event-based Egocentric 3D Human Pose Estimation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.08543) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | E-3DPSM |
| Dataset | EE3D-R, EE3D-W |

> [!tip] 效果简介
> - EE3D-R 上，MPJPE 81.32 (Non-Causal) vs 103.28 (EventEgo3D++) (-21.96 (约19%))；PA-MPJPE 60.21 (Non-Causal) vs 77.06 (EventEgo3D++) (-16.85 (约22%))；esmooth 6.65 (Non-Causal) vs 22.93 (EventEgo3D++) (-16.28 (约2.7倍提升))。
> - EE3D-W 上，MPJPE 155.82 (Non-Causal) vs 172.43 (EventEgo3D++) (-16.61 (约10%))；PA-MPJPE 90.85 (Non-Causal) vs 98.41 (EventEgo3D++) (-7.56 (约8%))。

## 概要

### 问题背景

事件相机因其高时间分辨率、低延迟和抗光照过曝的特性，在自我中心三维人体姿态估计中展现出独特优势。然而，现有事件驱动方法（如 **EventEgo3D** 和 **EventEgo3D++**）仅通过缓存上一事件帧进行短暂时序建模，未能充分利用事件流固有的异步、连续和变化驱动的特性。这一局限性导致在自遮挡场景下产生严重的三维误差、时序抖动和姿态漂移。此外，依赖二维热图和事件分割掩码的中间表示引入了量化误差，进一步损害了精度。

### 核心方法

**E-3DPSM** 将姿态估计重新定义为连续的时间动态过程，其核心思想源于一个直观观察：事件相机天然记录变化，因此三维空间中应存在对应的变化。方法围绕三个关键设计展开：

1. **连续状态机（SSM）建模**：引入基于 S5 状态空间模型的双向连续状态演化，根据异步事件流不断更新潜在状态，捕获长程时序依赖，从根本上消除短时建模带来的抖动。
2. **Delta 姿态回归**：同时预测直接三维绝对姿态和相邻帧间的三维关节位移（delta pose），使模型能够感知与事件变化对应的精细运动。
3. **可学习类卡尔曼融合**：通过一个可学习的类卡尔曼滤波器自适应融合直接姿态预测和 delta 更新，有效抑制漂移，产生平滑且准确的三维姿态序列。

与先前方法不同，E-3DPSM 移除了显式的二维热图和分割掩码预测，直接学习必要的中间特征，避免了量化误差的累积。

### 主要结果

E-3DPSM 在两个自我中心事件三维姿态估计基准 **EE3D-R** 和 **EE3D-W** 上均达到新的最优水平：

- **精度提升**：相比此前最优方法 EventEgo3D++，MPJPE 和 PA-MPJPE 降低约 19%，在 EE3D-R 上 MPJPE 从 103.28 mm 降至 81.32 mm（非因果模式）。
- **时序稳定性**：时间抖动指标 $e_{\text{smooth}}$ 最高降低 2.7 倍（从 22.93 降至 6.65），显著抑制了姿态漂移。
- **实时性**：在单块 NVIDIA A6000 上可达 80 Hz 的实时更新率，在便携设备 Jetson Orin Nano 上亦可实现约 30 Hz。

消融实验进一步证实：移除 SSM 模块导致精度和光滑度严重下降；用简单加法取代学习型融合会导致严重漂移；连续状态演化（不重置内部状态）优于定期重置策略，证明模型学会了自我调节。



### 事件相机与自我中心三维姿态估计

自我中心三维人体姿态估计旨在从穿戴于人体的单一相机中恢复三维关节位置，是增强现实、具身智能和运动分析等应用的核心感知能力。传统基于帧的 RGB 相机在高速运动下存在运动模糊，且对光照变化敏感，在可穿戴场景中面临严峻挑战。事件相机通过异步记录每个像素的对数强度变化，仅在变化超过阈值 $C$ 时产生事件

$$\Delta I ( x , y , t ) = | I ( x , y , t ) - I ( x , y , t - \Delta t ) | \geq C,$$

从而天然具备高时间分辨率、低延迟和高动态范围等优势。然而，事件数据的稀疏、异步和非结构化特性使得从单目事件相机中恢复三维人体姿态成为一个高度欠约束的问题。

### 现有方法的根本局限：短暂时序建模

首个事件驱动的自我中心三维姿态估计方法 **EventEgo3D** 及其改进版 **EventEgo3D++** 将事件流离散化为事件帧，并通过帧缓冲区保留上一事件帧以进行时序特征传播。这种设计的核心瓶颈在于：**仅利用上一帧的短时上下文，未能充分利用事件流固有的异步、连续和变化驱动的特性**。具体表现为三个层面的失效：

1. **自遮挡下的严重三维误差**：当肢体被躯干遮挡时，事件相机仅能观测到部分关节的运动线索。缺乏长程时序建模意味着模型无法利用遮挡前后的运动历史来推断被遮挡关节的位置，导致三维误差急剧增大。
2. **时间抖动与漂移**：逐帧独立预测或仅依赖单帧历史的模型在连续推理时，预测结果在相邻帧之间产生不自然的抖动；随着时间推移，误差累积形成漂移，使姿态估计逐渐偏离真实轨迹。
3. **二维中间表示的量化误差**：现有方法依赖二维热图和事件分割掩码作为辅助任务，将三维姿态回归锚定在二维像素空间，引入了量化误差和不准确的中间表示。

Figure 1 直观对比了两种范式：先前方法的帧缓冲区机制仅保留单一历史帧，而 E-3DPSM 将运动建模为连续的事件驱动状态演化，从根本上消除了抖动和漂移的机制性根源。

### 核心动机：将姿态估计重新定义为连续动态过程

事件相机天然记录“变化”——每个事件都标志着场景中某处发生了强度变化。一个自然的洞察是：**三维空间中应存在与这些事件变化对应的关节位移**。换言之，事件流不仅是空间外观的稀疏记录，更是底层人体运动的连续时间信号。因此，姿态估计不应被建模为从孤立帧到三维坐标的静态映射，而应被重新定义为**连续的时间动态过程**：一个内部状态根据异步事件流不断演化，并预测与事件变化对应的三维关节位移。

这一重新定义带来了三个关键设计需求：
- 需要一个能够捕获长程时序依赖的状态演化机制，而非短时帧缓存；
- 需要同时建模绝对姿态（全局锚点）和相对位移（事件驱动的变化），并通过自适应融合抑制漂移；
- 需要移除对显式二维热图和分割掩码的依赖，直接学习面向三维姿态的时空特征。

这些需求共同构成了 E-3DPSM 的设计动机：**构建一个连续状态机，将事件驱动的自我中心三维人体姿态估计从“逐帧回归”转变为“状态演化与融合”**，在保持实时性的同时显著提升三维精度和时间稳定性。



## 核心方法与创新机理

E-3DPSM 的核心创新在于将事件驱动的自我中心三维人体姿态估计重新定义为**连续时间动态过程**，从根本上改变了先前方法（如 EventEgo3D、EventEgo3D++）仅通过上一事件帧缓冲区进行短暂时序建模的范式。这一转变体现在三个紧密耦合的 changed slots 上。

### 从帧缓存到连续状态机演化

先前方法将事件流离散化为孤立的帧，仅利用前一帧的特征传播来捕捉运动线索。这种设计在快速运动或严重自遮挡下会迅速积累误差，表现为三维姿态的**抖动**和**漂移**（Figure 1a）。E-3DPSM 引入基于 S5 状态空间模型（SSM）的双向连续状态演化机制：每个时间步的 LNES 帧输入后，内部潜在状态 $\mathbf{Z}_t$ 通过线性递归持续更新，而非在每个序列起点重置（Figure 1b）。这一设计使模型能够捕获跨越数十帧的长程时序依赖，消融实验证实，移除所有 SSM 模块（变为纯空间基线）导致 MPJPE 从 84.45 升至 96.18，时间平滑度误差 $e_{\text{smooth}}$ 从 8.40 恶化至 28.49（Table 3）。更重要的是，连续状态演化（无重置）优于定期重置 SSM 或 Kalman 状态，证明模型学会了自我调节内部状态（Table 8）。

### 从绝对坐标回归到“直接+增量”双路预测与学习型融合

先前方法从二维热图直接回归三维绝对坐标，缺乏对帧间连续变化的显式建模。E-3DPSM 在姿态回归模块（PRM）中同时预测**直接三维姿态** $\mathbf{P}_t^{\text{D}}$（作为全局锚点）和**相对三维位移** $\mathbf{P}_t^{\Delta}$（捕捉事件变化对应的瞬时运动），并通过一个可学习的类 Kalman 滤波器自适应融合两者：

$$\mathbf{P}_t = \mathbf{X}_t + \mathbf{K}_t \cdot (\mathbf{P}_t^{\text{D}} - \mathbf{H} \cdot \mathbf{X}_t)$$

其中状态预测步利用 delta 姿态更新内部状态 $\mathbf{X}_t = \mathbf{A} \cdot \mathbf{X}_{t-1} + \mathbf{B} \cdot \mathbf{P}_t^{\Delta}$。这一设计的因果机制在于：delta 路径提供高频运动线索但会累积漂移，直接路径提供低频全局约束但缺乏时序平滑性，学习型 Kalman 增益 $\mathbf{K}_t$ 自适应地权衡两者。消融实验表明，用简单加法取代学习型融合（无锚点）会导致严重漂移，MPJPE 大幅升高；静态 Kalman 滤波有所改善但仍远不如自适应融合（Table 3, Figure 6）。Figure 6 进一步揭示，简单融合的误差随序列长度急剧增长，而学习型融合有效抑制了漂移，保持长时间稳定。

### 移除显式二维中间表示

先前方法依赖预测二维热图和事件分割掩码作为辅助任务，这不仅引入了量化误差，还迫使模型在二维空间中进行不必要的信息压缩。E-3DPSM 完全移除了这些显式二维中间表示，改为通过 SPEM 中的多阶段卷积编码、可变形注意力和关节查询 Transformer 解码器直接学习关节特定的时空特征。这一简化使模型能够端到端地优化三维目标，同时可变形注意力（通过可学习参考点 $\mathbf{R}_s$ 自适应聚焦于关节关键区域）有效补偿了鱼眼镜头的空间畸变——移除该模块导致 MPJPE 升至 89.00，PA-MPJPE 升至 66.30（Table 3）。

三个 changed slots 的协同效应在整体性能上得到验证：E-3DPSM 在 EE3D-R 基准上将 MPJPE 降低约 19%（从 103.28 降至 81.32），PA-MPJPE 降低约 22%，时间抖动降低约 2.7 倍（Table 1）。



E-3DPSM 将单目鱼眼事件相机下的自我中心三维人体姿态估计重新定义为**连续的事件驱动状态演化过程**。其核心洞察在于：事件相机天然记录“变化”，因此三维空间中应存在与之对应的关节位移变化。基于这一思想，整个 pipeline 由三个紧密衔接的阶段构成（Figure 2），从前端事件流到后端时序融合，形成一条端到端的可学习推理链。

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed E-3DPSM approach for monocular egocentric 3D human pose estimation. Incoming raw events e are converted into LNES frames*

### 阶段一：事件流到 LNES 帧的转换

原始事件相机输出的是异步、稀疏的事件流，每个事件 $e_i = (x_i, y_i, t_i, p_i)$ 仅在像素对数强度变化超过阈值 $C$ 时触发：

$$\Delta I ( x , y , t ) = | I ( x , y , t ) - I ( x , y , t - \Delta t ) | \geq C \tag{1}$$

为将这一异步流转换为适合神经网络处理的同步表示，E-3DPSM 采用**局部归一化事件表面（Locally Normalised Event Surface, LNES）**。对每个长度为 $T$ 毫秒的时间窗口，将窗口内事件的时间戳相对于窗口起始时刻 $t_0$ 归一化到 $[0,1]$：

$$\mathbf { L } ( x _ { i } , y _ { i } , p _ { i } ) = \frac { t _ { i } - t _ { 0 } } { T } \tag{2}$$

这一固定时间编码方式被消融实验证实优于可学习的体素表示或可学习 LNES（Table 9），为后续时序建模提供了稳定且信息充分的前端输入。整个事件流由此被划分为 $N$ 个 LNES 帧 $\{\mathbf{L}_t\}_{t=1}^N$。

### 阶段二：时空姿态编码器（SPEM）

SPEM 是 E-3DPSM 的**核心特征提取与长程时序建模模块**（Figure 3），其任务是将 LNES 帧序列转化为富含时间感知和关节特异性的特征表示。SPEM 由四个子模块级联构成：

1. **多阶段卷积编码器**：对每个 LNES 帧独立进行层级式空间特征提取，通过残差块和下采样卷积逐步压缩空间分辨率并扩展通道数：

   $$\mathbf { F } _ { t } ^ { s } = \operatorname { C o n v } \Bigl ( \operatorname { R e s B l o c k } _ { s } ^ { ( 2 ) } \big ( \operatorname { R e s B l o c k } _ { s } ^ { ( 1 ) } ( \mathbf { F } _ { t } ^ { s - 1 } ) \big ) \Bigr ) \tag{4}$$

2. **可变形注意力块**：在特定阶段对展平的特征 token 应用可变形自注意力，利用可学习的参考点 $\mathbf{R}_s$ 自适应地聚焦于关节关键区域，以补偿鱼眼镜头的严重畸变和自遮挡带来的空间偏移：

   $$\mathbf { F } _ { t } ^ { s } = { \mathrm { D e f o r m A t t n } } \left( \mathbf { T } _ { t } ^ { s } , \ \mathbf { T } _ { t } ^ { s } , \ \mathbf { R } _ { s } \right) \tag{5}$$

   消融实验表明，移除可变形注意力会导致 MPJPE 升至 89.00、PA-MPJPE 升至 66.30（Table 3），证实自适应空间推理对自我中心畸变补偿的关键作用。

3. **S5 状态空间模型（SSM）块**：这是 E-3DPSM 区别于先前方法（**EventEgo3D** 及其改进版 **EventEgo3D++** 仅使用上一事件帧的帧缓冲区进行短时特征传播）的核心创新。S5 层对每个空间位置的特征序列沿时间维度进行双向递归建模：

   $$\widetilde { \mathbf { F } } _ { 1 : N } ^ { \hat { s } } , \ \mathrm { a n d } \ \mathbf { Z } _ { t } ^ { \hat { s } } = \mathrm { S S M } _ { \hat { s } } ( \mathbf { F } _ { 1 : N } ^ { \hat { s } } ) \tag{6}$$

   其内部状态 $\mathbf{Z}_t$ 随事件流连续演化，无需重置——消融实验（Table 8）证明连续状态演化优于定期重置 SSM 或 Kalman 状态，表明模型学会了自我调节内部状态。移除所有 SSM 模块（退化为纯空间基线）会使 MPJPE 从 84.45 升至 96.18，时间平滑度 $e_\text{smooth}$ 从 8.40 升至 28.49（Table 3），证实长程时序建模的决定性作用。

4. **关节查询 Transformer 解码器**：以可学习的关节查询嵌入 $\mathbf{U}$ 与多阶段特征生成的记忆 token $\mathbf{M}_t$ 进行交叉注意力，为每个时间步提取 16 个关节的特定特征 $\mathbf{F}_t \in \mathbb{R}^{16 \times 192}$。

### 阶段三：姿态回归模块（PRM）与可学习 Kalman 融合

PRM 是 E-3DPSM 的**输出与融合层**，由三个子组件构成，共同实现时间一致的三维姿态估计：

1. **直接姿态回归器**：从关节 token 直接预测三维关节绝对位置 $\mathbf{P}_t^\mathrm{D}$，为融合提供全局锚点：

   $$\mathbf { P } _ { t } ^ { \mathrm { D } } = \mathrm { M L P } _ { \mathrm { D i r e c t } } ( \mathbf { F } _ { t } ) \tag{8}$$

2. **Delta 姿态回归器**：利用当前帧特征和上一帧姿态嵌入 $\mathbf{E}_{t-1}$ 预测相邻帧间的三维关节相对位移 $\mathbf{P}_t^\Delta$，捕捉事件流所反映的瞬时运动变化：

   $$\mathbf { P } _ { t } ^ { \Delta } = \mathbf { M } \mathbf { L } \mathbf { P } _ { \Delta } ( [ \mathbf { F } _ { t } ; \mathbf { E } _ { t - 1 } ] ) \tag{10}$$

3. **可学习 Kalman 风格融合模块**：这是 E-3DPSM 消除抖动和漂移的**核心机制**。模块维护一个内部状态 $\mathbf{X}_t$ 及其协方差 $\boldsymbol{\Sigma}_t$，通过预测-校正循环自适应融合直接姿态和 delta 姿态：

   - **预测步**：用 delta 姿态更新状态预测 $\mathbf{X}_t = \mathbf{A} \cdot \mathbf{X}_{t-1} + \mathbf{B} \cdot \mathbf{P}_t^\Delta$（Eq. 12）
   - **校正步**：利用可学习的 Kalman 增益 $\mathbf{K}_t$ 融合直接姿态观测，产生最终三维姿态 $\mathbf{P}_t$（Eq. 15），并采用 Joseph 形式更新协方差以保证数值稳定性（Eq. 16）

   消融实验（Table 3, Figure 6）揭示了这一设计的必要性：用简单加法取代学习型融合（无锚点）会导致严重漂移，MPJPE 大幅升高；静态 Kalman 滤波有所改善但仍不及自适应融合。学习型融合有效抑制了随时间累积的漂移，保持精度稳定。

### 训练与监督

整个框架以端到端方式训练，总损失函数为多维度的加权组合：

$$\mathcal { L } _ { \mathrm { t o t a l } } = \lambda _ { \mathrm { 3 D } } \mathcal { L } _ { \mathrm { 3 D } } + \lambda _ { \Delta } \mathcal { L } _ { \Delta } + \lambda _ { \mathrm { 2 D } } \mathcal { L } _ { \mathrm { 2 D } } + \lambda _ { \mathrm { B L } } \mathcal { L } _ { \mathrm { B L } } + \lambda _ { \mathrm { B A } } \mathcal { L } _ { \mathrm { B A } } \tag{17}$$

其中三维损失 $\mathcal{L}_\mathrm{3D}$ 监督最终融合姿态，Delta 损失 $\mathcal{L}_\Delta$ 监督帧间位移，二维重投影损失 $\mathcal{L}_\mathrm{2D}$ 提供弱监督，骨骼长度损失 $\mathcal{L}_\mathrm{BL}$ 和骨骼角度损失 $\mathcal{L}_\mathrm{BA}$ 约束运动学合理性。值得注意的是，E-3DPSM 移除了先前方法（EventEgo3D/EventEgo3D++）所需的显式二维热图和事件分割掩码预测，直接学习必要的中间特征，从而避免了量化误差的引入。

### 推理模式

E-3DPSM 支持两种推理模式：**非因果模式**（Non-Causal）利用双向 SSM 捕获完整时序上下文，获得最优精度；**因果模式**（Causal）仅使用过去信息，适用于实时应用。非因果训练在因果推理下仍优于纯因果训练（MPJPE 降低 5.43 mm, Table 7），表明利用未来上下文进行训练能增强特征学习质量。在单块 NVIDIA A6000 上，E-3DPSM 可实现约 80 Hz 的实时三维姿态更新率（Table 5），并在便携设备 Jetson Orin Nano 上达到约 30 Hz（Figure 7）。

### 补充图表

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/001_Figure_1.jpg]]
*Figure 1: Rethinking event-based egocentric 3D human pose estimation. (a) Previous methods [25, 26] capture temporal information only through a single previous event frame stored in the frame buffer leading to jitter and drift. (b) Our E-3DPSM approach models motion as a continuous event-driven state evolution, fusing delta and direct 3D human pose updates, thereby achieving real-time and temporally stable 3D reconstruction and significantly outperforming prior approaches in the 3D accuracy*



### 问题形式化与事件表示

事件相机异步输出事件流 $e_i = (x_i, y_i, t_i, p_i)$，当像素对数强度变化超过阈值 $C$ 时触发：

$$\Delta I(x,y,t) = |I(x,y,t) - I(x,y,t - \Delta t)| \geq C \tag{1}$$

E-3DPSM 首先将原始事件流转换为局部归一化事件表面（LNES）帧。对时间窗口 $T$ 内的事件，LNES 将每个事件的时间戳相对窗口起始时刻 $t_0$ 归一化：

$$\mathbf{L}(x_i, y_i, p_i) = \frac{t_i - t_0}{T} \tag{2}$$

该表示将异步事件流转换为 $N$ 帧规则采样的时空表示 $\{\mathbf{L}_t\}_{t=1}^N$，作为后续网络的输入。

### 时空姿态编码器（SPEM）

SPEM 是 E-3DPSM 的核心特征提取模块，由多阶段卷积编码、可变形注意力、S5 状态空间模型和关节查询 Transformer 解码器四部分级联构成（图 3），旨在从 LNES 帧中提取时间感知的关节特定表示。

**多阶段卷积编码。** 第 $s$ 阶段的特征图 $\mathbf{F}_t^s$ 由前一阶段特征经两个残差块和卷积下采样得到：

$$\mathbf{F}_t^s = \operatorname{Conv}\Bigl(\operatorname{ResBlock}_s^{(2)}\big(\operatorname{ResBlock}_s^{(1)}(\mathbf{F}_t^{s-1})\big)\Bigr) \tag{4}$$

**可变形注意力。** 在最后两个阶段 $\hat{s}$，将特征图展平为 token 序列 $\mathbf{T}_t^{\hat{s}}$，利用可学习参考点 $\mathbf{R}_{\hat{s}}$ 进行自注意力以聚焦关节关键区域：

$$\mathbf{F}_t^{\hat{s}} = \mathrm{DeformAttn}\left(\mathbf{T}_t^{\hat{s}},\ \mathbf{T}_t^{\hat{s}},\ \mathbf{R}_{\hat{s}}\right) \tag{5}$$

**S5 状态空间时序建模。** 对每个空间位置的 $N$ 帧特征序列，S5 层执行双向线性递归，同时输出细化特征 $\widetilde{\mathbf{F}}_{1:N}^{\hat{s}}$ 和内部状态 $\mathbf{Z}_t^{\hat{s}}$：

$$\widetilde{\mathbf{F}}_{1:N}^{\hat{s}},\ \mathbf{Z}_t^{\hat{s}} = \mathrm{SSM}_{\hat{s}}(\mathbf{F}_{1:N}^{\hat{s}}) \tag{6}$$

其底层递归形式为 $\mathbf{Z}_{t+1} = \mathbf{A}\mathbf{Z}_t + \mathbf{B}x_t,\ \mathbf{Y}_t = \mathbf{C}\mathbf{Z}_t$（式 3），捕获跨越长时间窗口的运动依赖。

**关节查询解码器。** 利用 $J$ 个可学习关节查询嵌入 $\mathbf{U}$ 与多尺度记忆 token $\mathbf{M}_t$ 进行交叉注意力，输出关节特定特征：

$$\mathbf{F}_t = \operatorname{TransformerDecoder}(\mathbf{U}, \mathbf{M}_t) \in \mathbb{R}^{16 \times 192} \tag{7}$$

### 姿态回归模块（PRM）

PRM 包含三个子组件：直接姿态回归器、Delta 姿态回归器和可学习 Kalman 融合模块。

**直接姿态回归器。** 从关节 token 直接预测三维绝对位置，作为全局锚点：

$$\mathbf{P}_t^{\mathrm{D}} = \mathrm{MLP}_{\mathrm{Direct}}(\mathbf{F}_t) \in \mathbb{R}^{16 \times 3} \tag{8}$$

**Delta 姿态回归器。** 利用当前帧特征和上一帧姿态嵌入 $\mathbf{E}_{t-1}$ 预测帧间三维位移：

$$\mathbf{P}_t^{\Delta} = \mathrm{MLP}_{\Delta}([\mathbf{F}_t; \mathbf{E}_{t-1}]) \tag{10}$$

**可学习 Kalman 融合。** 这是抑制漂移的关键设计。预测步利用 delta 姿态更新内部状态：

$$\mathbf{X}_t = \mathbf{A} \cdot \mathbf{X}_{t-1} + \mathbf{B} \cdot \mathbf{P}_t^{\Delta} \tag{12}$$

校正步利用可学习 Kalman 增益 $\mathbf{K}_t$ 融合直接姿态观测，产生最终三维姿态：

$$\mathbf{P}_t = \mathbf{X}_t + \mathbf{K}_t \cdot \left(\mathbf{P}_t^{\mathrm{D}} - \mathbf{H} \cdot \mathbf{X}_t\right) \tag{15}$$

协方差更新采用 Joseph 形式以保证数值稳定性：

$$\mathbf{\Sigma}_t = (\mathbf{I} - \mathbf{K}_t \cdot \mathbf{H}) \cdot \mathbf{\Sigma}_{t|t-1} \cdot (\mathbf{I} - \mathbf{K}_t \cdot \mathbf{H})^{\top} + \mathbf{K}_t \cdot \mathbf{R} \cdot \mathbf{K}_t^{\top} \tag{16}$$

其中状态转移矩阵 $\mathbf{A}$、控制矩阵 $\mathbf{B}$、观测矩阵 $\mathbf{H}$ 以及过程噪声协方差 $\mathbf{Q}$、观测噪声协方差 $\mathbf{R}$ 均为可学习参数。消融实验（Table 11）表明，全局学习的 $\mathbf{Q}$ 和 $\mathbf{R}$ 比输入/状态依赖的协方差更稳定，后者导致过拟合（MPJPE 升高 6.7 mm）。

### 损失函数

总损失为五项加权和：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{3D}}\mathcal{L}_{\mathrm{3D}} + \lambda_{\Delta}\mathcal{L}_{\Delta} + \lambda_{\mathrm{2D}}\mathcal{L}_{\mathrm{2D}} + \lambda_{\mathrm{BL}}\mathcal{L}_{\mathrm{BL}} + \lambda_{\mathrm{BA}}\mathcal{L}_{\mathrm{BA}} \tag{17}$$

其中 $\mathcal{L}_{\mathrm{3D}}$ 为三维关节位置 L1 损失，$\mathcal{L}_{\Delta}$ 为 delta 位移 L1 损失，$\mathcal{L}_{\mathrm{2D}}$ 为二维投影损失，$\mathcal{L}_{\mathrm{BL}}$ 为骨骼长度损失，$\mathcal{L}_{\mathrm{BA}}$ 为骨骼角度损失——后者通过比较预测与真值骨骼向量的夹角来正则化肢体角度配置。

### 关键设计决策的因果链

1. **连续状态演化**：SSM 内部状态在推理时不重置（Table 8），模型自动学习自我调节，这优于定期重置 SSM 或 Kalman 状态。
2. **学习型融合 vs. 简单加法**：若用 $\mathbf{P}_t = \mathbf{P}_{t-1} + \mathbf{P}_t^{\Delta}$ 替代 Kalman 融合（式 11），会导致误差随序列长度快速累积漂移；学习型融合通过自适应增益 $\mathbf{K}_t$ 有效抑制了该漂移（图 6）。
3. **非因果训练**：双向 SSM 在训练时利用未来上下文增强特征学习，即使推理时切换为因果模式仍优于纯因果训练（MPJPE 降低 5.43 mm，Table 7）。

### 补充图表

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/003_Figure_3.jpg]]
*Figure 3: Architecture of SPEM, combining multi-stage convolutional encoding, SSM blocks, deformable attention, and a jointquery decoder for temporally-aware pose features*

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/009_Figure_6.jpg]]
*Figure 6: Pose drift over time. Comparison of learned fusion (Eq. (15)), direct pose only (Eq. (8)), and naive fusion (Eq. (11)) across temporal sequence length. Naive fusion leads to rapidly increasing drift, whereas our learned fusion effectively mitigates this drift, maintaining stable accuracy over time*



## 实验与关键发现

### 主要定量结果

E-3DPSM 在两个事件驱动的自我中心三维人体姿态估计基准——EE3D-R（真实数据集）和 EE3D-W（野外数据集）上，全面超越了先前方法。Table 1 汇总了核心指标对比。

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/005_Table_1.jpg]]
*Table 1: Quantitative comparisons on EE3D-R and EE3D-W*

在 EE3D-R 上，非因果模式（Non-Causal）的 E-3DPSM 将 MPJPE 从 EventEgo3D++ 的 103.28 mm 降至 **81.32 mm**（降幅约 19%），PA-MPJPE 从 77.06 mm 降至 **60.21 mm**（降幅约 22%）。因果模式（Causal）同样取得显著提升，MPJPE 为 84.45 mm。在 EE3D-W 上，非因果模式的 MPJPE 从 172.43 mm 降至 **155.82 mm**（降幅约 10%），PA-MPJPE 从 98.41 mm 降至 **90.85 mm**（降幅约 8%）。值得注意的是，E-3DPSM 的因果模式已优于所有先前方法，这保证了实时推理场景下的性能。

**时间稳定性**是最显著的提升维度。在 EE3D-R 上，E-3DPSM 的 $e_{\mathrm{smooth}}$ 从 EventEgo3D++ 的 22.93 降至 **6.65**，提升约 2.7 倍；在 EE3D-W 上从 29.74 降至 **20.24**。这一指标通过比较预测和真值的帧间关节位移幅度来衡量（见 Eq. (24)），直接量化了先前方法中普遍存在的抖动和漂移问题的改善程度。

Figure 5 可视化了每帧所有关节的平均位移，直观展示了 E-3DPSM 预测轨迹与真值的高度吻合，而 EventEgo3D 系列方法则表现出明显的高频抖动。

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/006_Figure_5.jpg]]
*Figure 5: We plot the per-frame all-joint average displacement (Eq. (24)) for EE3D-R (top) and EE3D-W (bottom)*

**遮挡条件下的表现**进一步验证了方法的鲁棒性。Table 2 仅评估被遮挡关节的误差：在 EE3D-R 上，E-3DPSM 非因果模式的 MPJPE 为 64.69 mm，远低于 EventEgo3D++ 的 96.30 mm。Figure 8 揭示了关键机制——随着时间历史窗口 $k$ 的增加，遮挡关节（尤其是下半身关节）的 MPJPE 持续改善，证明 SSM 的长程时序建模有效补偿了瞬时遮挡导致的信息缺失。

**公平性验证**：Table 4 显示，对 EventEgo3D 和 EventEgo3D++ 施加推理时 Kalman 后处理滤波后，其 MPJPE 仅小幅下降，仍远高于 E-3DPSM。这排除了“增益仅来自后平滑”的质疑，证明性能提升源于方法本身的结构性改进。

### 消融实验

Table 3 在 EE3D-R 上系统拆解了各组件的贡献。

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/008_Table_3.jpg]]
*Table 3: Ablation study on the EE3D-R dataset evaluating the impact of each component of our E-3DPSM approach*

**SSM 时序建模是核心驱动力**。移除所有 SSM 模块（退化为纯空间基线）后，MPJPE 从 84.45 mm 飙升至 96.18 mm，$e_{\mathrm{smooth}}$ 从 8.40 升至 28.49。这表明仅靠空间特征无法建模事件流中的时序依赖，SSM 提供的连续状态演化对精度和时间稳定性均不可或缺。

**可变形注意力的作用**：移除可变形注意力（w/o Deform.Attn）使 MPJPE 升至 89.00 mm，PA-MPJPE 升至 66.30 mm。自我中心视角固有的鱼眼畸变和非均匀空间分布要求模型自适应地聚焦于关节关键区域，可变形注意力恰好提供了这一能力。

**融合策略是关键设计**。用简单加法（Eq. (11)）取代可学习 Kalman 融合模块会导致严重漂移——Figure 6 显示，简单加法的误差随序列长度急剧增长，而可学习融合有效抑制了这一趋势，保持稳定的时序精度。Table 3 中“w/o Kalman”变体的 MPJPE 大幅升高，证实了自适应融合的不可替代性。静态 Kalman 滤波（固定协方差）虽优于简单加法，但仍不及全局可学习协方差策略（Table 11）。

**训练策略**：Table 7 显示，非因果训练（双向 SSM）在因果推理下仍优于纯因果训练，MPJPE 降低 5.43 mm（84.45 vs. 89.88），表明利用未来上下文进行训练能增强特征学习质量。训练序列长度从 20 帧增加到 40 帧带来稳定增益，MPJPE 从 86.25 降至 84.45。

**状态重置策略**：Table 8 表明，连续状态演化（不重置内部状态）优于定期重置 SSM 状态或 Kalman 状态，证明模型学会了自我调节内部状态，无需人工干预。

**事件表示**：Table 9 对比了可学习体素表示、可学习 LNES 和标准预定义 LNES，后者在所有指标上均占优，表明固定时间编码更适合本任务。

### 计算效率

Table 5 和 Table 6 展示了效率对比。E-3DPSM 的参数为 4.1M，FLOPs 为 1.8G（单帧），高于 EventEgo3D++ 的 0.9M / 0.5G，但保持在同量级。在单块 NVIDIA A6000 上，E-3DPSM 可达到 **80 Hz** 的三维姿态更新率，满足实时需求。在便携设备 Jetson Orin Nano 上，更新率约为 30 Hz（Figure 7 展示了头戴式设备实物照片），证明方法具备边缘部署潜力。

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/012_Table_5.jpg]]
*Table 5: Model efficiency comparison in terms of parameters, FLOPs, GPU memory, and 3D pose update rate in Hz (measured on a single NVIDIA A6000 GPU)*

### 失败模式与局限性

Figure 9 展示了三类典型失败场景：
1. **强自遮挡**（如爬行动作）：当大量关节被身体遮挡时，三维姿态精度下降，预测结果可能出现解剖学不合理。
2. **物体交互**：手持或接触物体时，手部关节的定位误差增大。
3. **多人场景**：视野中出现其他人时，模型可能混淆目标人物。

此外，突发的光照变化（如闪烁效应）在快速复杂运动中可能导致暂时的时序不稳定。当前方法依赖有监督的三维标注数据，尚未探索无监督或自监督范式。

### 补充图表

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/007_Table_2.jpg]]
*Table 2: Occlusion-only quantitative comparison on EE3D-R and EE3D-W. Evaluation is performed only on occluded joints*

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/010_Table_7.jpg]]
*Table 7: Training strategy ablation on the EE3D-R dataset. We compare causal (forward) vs. non-causal (bidirectional) training and different sequence lengths used during training*

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/011_Table_4.jpg]]
*Table 4: Comparison with Kalman-smoothed baselines on the EE3D-R dataset. We apply inference-time Kalman filtering (KF) to prior methods to rule out post-hoc smoothing as the main reason for improvements. Our method achieves substantially lower MPJPE and*

![[assets/figures/papers/paper_list_l1014_https_arxiv_org_abs_2604_08543/figures/015_Table_8.jpg]]
*Table 8: Inference-time ablation on the EE3D-R dataset comparing different strategies for resetting internal states. We evaluate resetting the SSM block states, resetting the Kalman fusion states, and using continuous state evolution without resets (ours)*



## 定位与知识库关联

### 问题定位：从帧缓冲到连续状态机

事件驱动的自我中心三维人体姿态估计是一个新兴交叉方向，其核心挑战在于如何有效利用事件相机异步、连续、变化驱动的特性。在此之前的代表性工作 **EventEgo3D** 及其改进版 **EventEgo3D++** 是该方向的开创性方法，它们首次将事件数据引入自我中心三维姿态估计任务。然而，这些方法在时序建模上存在根本性瓶颈：它们仅通过存储上一事件帧的帧缓冲区（frame buffer）进行短暂时序特征传播，未能充分利用事件流固有的长程时序依赖。这直接导致在自遮挡场景下产生严重的三维误差、抖动和漂移——这些正是事件相机本应擅长处理的动态场景。

此外，先前方法依赖显式的二维热图和事件分割掩码作为中间表示和辅助监督信号，这不仅引入了量化误差，还使整个流程对二维预测的不准确度高度敏感。

### 核心方法差异：因果机制的重新设计

E-3DPSM 与 EventEgo3D/EventEgo3D++ 的本质差异不在于网络规模或训练技巧，而在于对“事件数据中蕴含何种运动信息”这一根本问题的不同回答。下表总结了四个关键设计槽位的变化：

| 设计维度 | EventEgo3D / EventEgo3D++ | E-3DPSM |
|---------|--------------------------|---------|
| **时序建模架构** | 单帧缓冲区的短时特征传播 | 基于 S5 状态空间模型的双向连续状态演化，捕获长程时序依赖 |
| **姿态预测方式** | 从二维热图直接回归三维绝对坐标 | 同时回归直接三维姿态和相对三维位移（delta pose），通过可学习 Kalman 融合模块自适应集成 |
| **监督信号与中间表示** | 需要预测二维热图和事件分割掩码作为辅助任务 | 移除显式的二维热图和分割掩码预测，直接学习必要的中间特征 |
| **状态重置机制** | 不存在状态机概念 | 连续演化而不重置内部状态，由模型自动调节 |

这些变化的因果逻辑链如下：

1. **从帧缓冲到 SSM 连续状态演化**：事件相机天然记录“变化”，因此三维空间中应存在对应的“变化”。E-3DPSM 将姿态估计重新定义为连续的时间动态过程——SSM 根据异步事件流不断演化潜在状态，而非仅在离散帧之间传播信息。消融实验证实，移除所有 SSM 模块（变为纯空间基线）使 MPJPE 从 84.45 mm 升至 96.18 mm，时间平滑度误差 $e_{\text{smooth}}$ 从 8.40 升至 28.49，证实时序建模是性能提升的关键因果因素。

2. **从绝对回归到 delta 姿态 + 学习型融合**：直接回归绝对坐标缺乏对运动连续性的显式约束。E-3DPSM 引入 delta 姿态回归器预测相邻帧之间的三维关节位移，并通过一个可学习的类 Kalman 滤波器自适应融合直接姿态（作为全局锚点）和 delta 更新（作为局部运动线索）。这一设计的决定性证据来自漂移分析（Figure 6）：用简单加法取代学习型融合导致误差随时间快速累积（严重漂移），而学习型融合有效抑制了漂移，保持长时间稳定精度。

3. **移除二维中间表示**：二维热图和分割掩码的预测误差会传播到三维姿态估计。E-3DPSM 直接学习必要的中间特征，避免了这一误差源。

### 与跨模态方法的边界

**EgoPoseFormer** 是基于 RGB 的自我中心三维姿态估计方法，代表传统相机模态下的技术路线。E-3DPSM 与它的差异不仅是模态不同（事件 vs. RGB），更在于对时序信息的利用方式：RGB 方法通常依赖固定帧率的密集帧序列，而事件数据天然稀疏、异步，要求不同的时序建模策略。定性对比（Figure 4）显示，E-3DPSM 在事件模态下显著优于 EgoPoseFormer，但两者适用于不同的硬件和场景约束。

### 适用边界与局限性

基于论文提供的证据，E-3DPSM 的适用边界如下：

1. **严重自遮挡场景**：在爬行等强自遮挡动作中，三维姿态精度会下降（Figure 9A）。这源于事件相机本身的观测局限性——被遮挡的关节无法产生事件信号，SSM 的时序推理能力虽能缓解但无法完全补偿信息缺失。

2. **物体交互与多人场景**：当视野中存在交互物体或其他人物时，模型性能下降（Figure 9B, 9C）。当前模型假设场景中仅存在单个人体，缺乏对多人或物体干扰的显式建模。

3. **突发光照变化**：在快速复杂运动中，突发的光照变化（如闪烁效应）可能导致暂时的时序不稳定。这反映了事件相机对光照变化高度敏感的双刃剑特性。

4. **监督数据依赖**：当前模型依赖有监督的三维标注数据，尚未探索无监督或自监督方式以减少对昂贵标注的依赖。

### 开放问题与未来方向

1. **显式遮挡建模**：是否可以通过显式的遮挡推理和生成式姿态优化进一步提高在高度遮挡下的合理性？例如，结合人体运动先验对被遮挡关节进行条件生成。

2. **事件表示的选择**：预定义事件表示（如 LNES）与可学习表示的选择是否取决于具体任务？消融实验（Table 9）表明标准 LNES 优于可学习体素或可学习 LNES，但这一结论是否在更广泛的事件视觉任务中成立仍未有定论。

3. **连续状态机范式的扩展**：能否将连续状态机范式扩展到以事件为中心的全身运动重建（包括手指、面部）或多模态（事件+IMU）设置？这将是验证该方法通用性的重要方向。

4. **实时部署的进一步优化**：当前模型在 Jetson Orin Nano 上达到约 30 Hz，虽已满足实时需求，但进一步降低计算开销将有助于在更低功耗设备上的部署。



## 原文 PDF

![[paperPDFs/CVPR_2026/E_3DPSM_A_State_Machine_for_Event_based_Egocentric_3D_Human_Pose_Estimation.pdf]]
