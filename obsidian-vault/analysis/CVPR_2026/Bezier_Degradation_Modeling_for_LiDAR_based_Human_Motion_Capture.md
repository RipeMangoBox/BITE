---
title: Bezier Degradation Modeling for LiDAR-based Human Motion Capture
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Bezier_Degradation_Modeling_for_LiDAR_based_Human_Motion_Capture.pdf
project_link: null
code_link: null
aliases:
- BDMLBHMC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 使用贝塞尔曲线对运动轨迹进行参数化，引入轨迹感知的层次化退化策略，生成多尺度运动表示，使模型能够从粗到细地恢复运动。
primary_logic: 人体运动可由贝塞尔曲线紧凑表示，即使大幅减少控制点仍能保留全局运动趋势，这种层次化特性可用于由粗到细的重建，弥合遮挡造成的观测断裂。
claims:
- 即使大幅减少贝塞尔控制点，仍能保留全局运动趋势，表明运动表示对遮挡鲁棒。
- BMLiCap 在四个主流基准上达到最优精度和时序连续性，尤其在 FreeMotion 上大幅超越 LiveHPS++。
- "轨迹感知退化策略和渐进式重建模块（TMT、MMA）的消融实验表明各组件均带来增益，最优配置为 L=3, schedule {32,16,8}。"
- LiDARHuman26M 上 MPJPE↓ / MPVPE↓ / AE↓ (mm) = 66.8 / 85.4 / 28.8 (32-frame)
---

# Bezier Degradation Modeling for LiDAR-based Human Motion Capture

> [!tip] 核心洞察
> 人体运动可由贝塞尔曲线紧凑表示，即使大幅减少控制点仍能保留全局运动趋势，这种层次化特性可用于由粗到细的重建，弥合遮挡造成的观测断裂。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于贝塞尔退化建模的LiDAR人体运动捕捉 |
| 英文题名 | Bezier Degradation Modeling for LiDAR-based Human Motion Capture |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/An_Bezier_Degradation_Modeling_for_LiDAR-based_Human_Motion_Capture_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | BMLiCap |
| Dataset | LiDARHuman26M, FreeMotion |

> [!tip] 效果简介
> - LiDARHuman26M 上，MPJPE↓ / MPVPE↓ / AE↓ (mm) 66.8 / 85.4 / 28.8 (32-frame) vs LiveHPS++, LiDARCap 等 (见 Table 1) (优于所有对比方法，具体数值见表 1)。
> - FreeMotion 上，MPJPE↓ / MPVPE↓ / AE↓ BMLiCap† vs LiveHPS++ (-14.7 / -16.3 / -31.7)。

## 概要

现有 LiDAR 人体运动捕捉方法通常直接从稀疏、不完整的点云特征中逐帧回归 SMPL 参数，缺乏对时序运动先验的有效建模。当面临严重遮挡或传感器噪声时，这类方法容易产生姿态抖动甚至完全失效。核心瓶颈在于：观测层面的断裂无法通过单纯的帧级特征提取来弥合。

BMLiCap 的核心洞察是：**人体运动可由贝塞尔曲线紧凑表示**。即使大幅减少贝塞尔控制点，全局运动趋势仍能得到保留（Figure 2），这一层次化特性为从粗到细的运动重建提供了天然支撑。基于此，BMLiCap 提出两个关键创新：

1. **轨迹感知的层次化贝塞尔退化（TAD）**：将原始关节轨迹拟合为贝塞尔曲线，并通过轨迹感知的降采样生成多尺度运动表示，作为由粗到细重建的监督信号。
2. **渐进式运动重建模块**：包含时标运动变换器（TMT）和多级运动聚合器（MMA），以粗粒度运动趋势为引导，逐步恢复细粒度运动，并通过块状因果掩码调控阶段间的信息流。

在四个主流 LiDAR 动捕基准（LiDARHuman26M、FreeMotion、NoiseMotion、SLOPER4D）上，BMLiCap 均达到最优精度和时序连续性。尤其在极具挑战的 FreeMotion 场景下，BMLiCap 相较 LiveHPS++（Ren et al., ECCV 2024）在 MPJPE/MPVPE/AE 三项指标上分别降低 14.7/16.3/31.7 mm。消融实验证实，TAD 策略、多级运动 token、运动损失、块状因果掩码及多阶段运动聚合器各自带来稳定增益，最优配置为 3 个阶段、调度 {32, 16, 8}。

**方法定位**：BMLiCap 属于“运动先验引导的渐进式重建”范式，区别于 LiDARCap（Li et al., CVPR 2022）的单阶段逐帧回归、LiveHPS/LiveHPS++ 的 SMPL 顶点先验跟踪，以及 NIE（Zhang et al., AAAI 2024）的邻域增强策略。其核心差异在于用贝塞尔曲线的层次化压缩特性替代了传统的帧级时序建模，使模型能够从粗粒度运动趋势中“填补”观测断裂。



### 问题背景：LiDAR 人体运动捕捉的观测困境

基于 LiDAR 的三维人体运动捕捉旨在从稀疏、无序的点云序列中恢复精确的人体姿态与运动轨迹。与 RGB 相机不同，LiDAR 传感器通过主动发射激光脉冲获取场景的三维几何信息，具有对光照变化不敏感、能提供绝对尺度等优势，使其在户外、大范围、复杂光照等场景下成为视觉动捕的重要补充。然而，LiDAR 点云本身具有**稀疏性、不完整性和时序不连续性**——人体在运动中频繁发生自遮挡，传感器视角受限导致部分肢体完全不可见，单帧点云往往只覆盖人体表面的一小部分。这种观测层面的断裂使得从逐帧点云直接回归人体姿态极为困难。

### 现有方法的缺口：缺乏对时序运动先验的有效建模

当前主流的 LiDAR 动捕方法，如 **LiDARCap**（Li et al., CVPR 2022）、**LiveHPS**（Ren et al., CVPR 2024）及其改进版 **LiveHPS++**（Ren et al., ECCV 2024），以及 **NIE**（Zhang et al., AAAI 2024），大多遵循“逐帧提取点云特征 → 回归 SMPL 参数”的范式。这些方法的核心瓶颈在于：**它们直接从高度不完整的单帧观测中学习映射，缺乏对时序运动先验的结构化建模**。尽管部分方法引入了 GCN 或 Transformer 进行帧间信息聚合，但这种帧级时序建模本质上仍是对离散观测的平滑后处理，并未从运动本身的结构特性出发构建表征。当面临严重遮挡或快速运动时，观测信号的信噪比急剧下降，模型预测的关节位置出现抖动、漂移甚至完全失败（见 Figure 5）。

### 核心动机：运动的结构化压缩与层次化恢复

人体运动并非随机的时间序列——它具有内在的**平滑性、连续性和可压缩性**。一个自然的假设是：如果能够找到一种紧凑的运动表示，使其在信息大幅压缩后仍能保留全局运动趋势，那么就可以利用这种表示在观测缺失时提供有效的先验约束。

本文的动机正源于这一观察：**贝塞尔曲线能够以极少的控制点紧凑地表示人体运动轨迹，且即使大幅减少控制点数量，仍能保持全局运动趋势**（见 Figure 2）。这一特性意味着，贝塞尔曲线天然具备层次化退化的能力——通过逐步减少控制点，可以生成从精细到粗糙的多尺度运动表示。在粗粒度层级，运动被高度压缩，去除了高频噪声和局部抖动，仅保留大尺度运动趋势；在细粒度层级，运动细节得以恢复。这种从粗到细的层次结构恰好与人类感知运动的方式一致：先把握整体趋势，再填充局部细节。

### 本文的切入点

基于上述洞察，本文提出 **BMLiCap**，核心思路是**用贝塞尔曲线对运动轨迹进行参数化，并引入轨迹感知的层次化退化策略，生成多尺度运动表示，使模型能够从粗到细地恢复运动**。这一设计将问题从“从残缺观测中直接回归完整姿态”转化为“从残缺观测中恢复多尺度运动曲线，再逐步融合细化”，从而弥合遮挡造成的观测断裂，提升严重遮挡下的时序连贯性和预测精度。



## 核心方法与创新机理

BMLiCap 的核心创新在于将人体运动建模从“逐帧回归”范式转变为**层次化贝塞尔运动表示与渐进式重建**范式，通过三个关键机制解决现有 LiDAR 动捕方法在严重遮挡下的时序断裂问题。

### 1. 运动表示的范式转换

现有方法（如 **LiDARCap** (Li et al., CVPR 2022)、**LiveHPS** (Ren et al., CVPR 2024)、**LiveHPS++** (Ren et al., ECCV 2024)、**NIE** (Zhang et al., AAAI 2024)）直接从不完整的点云特征逐帧回归 SMPL 参数或中间特征，缺乏对时序运动先验的有效建模。BMLiCap 将运动表示从**直接逐帧回归**转变为**多级贝塞尔曲线表示**：利用贝塞尔曲线的时序压缩特性，通过轨迹感知退化（Trajectory-Aware Degradation, TAD）生成从粗到细的层次化运动表示。即使大幅减少控制点，贝塞尔曲线仍能保留全局运动趋势（Fig. 2），这使得粗粒度表示天然对遮挡鲁棒。

### 2. 从粗到细的渐进式重建策略

传统方法采用**单阶段逐帧推理**，在观测断裂时直接产生抖动或失败预测。BMLiCap 引入**从粗到细的渐进式重建**，由两个核心模块协同实现：

- **时标运动变换器（Time-scale Motion Transformer, TMT）**：以编码器结构联合点云特征与多级运动嵌入，预测各时间尺度上的贝塞尔运动曲线。通过**块状因果掩码（block-wise causal mask）**调控阶段间信息流，使细粒度 token 只能关注粗粒度 token 和自身，实现从粗粒度运动趋势引导细粒度运动恢复。
- **多级运动聚合器（Multi-level Motion Aggregator, MMA）**：通过逐步上采样与融合机制，将多级运动表示从粗到细集成为最终细粒度运动序列。

### 3. 时序信息流的因果调控

现有方法基于 GCN 或 Transformer 进行帧级时序建模，信息流缺乏层次化约束。BMLiCap 通过块状因果掩码实现**阶段间信息流的严格调控**：粗粒度运动趋势作为先验约束，引导细粒度运动恢复，弥合遮挡造成的观测断裂。这一机制在 50% 输入帧缺失时仍保持稳定性能（Fig. 7a）。

### 4. 轨迹感知退化的监督信号设计

不同于简单的降采样，TAD 策略在减少控制点的同时，通过切向量提取与最优长度最小二乘求解（Eq. 2–4），调整曲线段参数以最佳逼近原始运动动态，在去噪与保真度之间取得平衡。这为渐进式重建提供了从易到难的学习课程（curriculum）。

### 关键创新总结

| 变化维度 | Baseline 做法 | BMLiCap 做法 |
|---------|-------------|-------------|
| 运动表示 | 直接逐帧回归 SMPL 参数 | 多级贝塞尔曲线，通过 TAD 生成层次化表示 |
| 重建策略 | 单阶段逐帧推理 | 从粗到细渐进式重建（TMT + MMA） |
| 时序信息流 | 帧级 GCN/Transformer | 块状因果掩码调控阶段间信息流 |
| 逆运动学 | 直接预测 SMPL 参数 | STGCN 将预测关节位置转换为姿态参数 |

这些创新共同构成了一个**以运动先验弥补观测缺陷**的框架：贝塞尔曲线提供运动连续性的结构先验，层次化退化提供从粗到细的学习课程，因果掩码确保粗粒度趋势有效引导细粒度恢复。



BMLiCap 的整体框架围绕一个核心洞察构建：**人体运动在时序上具有高度的可压缩性**——即使大幅减少贝塞尔控制点，全局运动趋势依然得以保留（Fig. 2）。这一特性使得“由粗到细”的渐进式重建成为可能，从而在严重遮挡和噪声条件下弥合观测断裂。基于此，框架由两条协同工作的管线组成：**轨迹感知的贝塞尔退化**（训练阶段生成多级运动监督）和**渐进式运动重建**（推理阶段从点云条件恢复细粒度运动）。

### 输入输出流

给定一段长度为 $T$ 的 LiDAR 点云序列 $\mathcal{P} = \{\mathbf{P}_t \in \mathbb{R}^{N \times 3}\}_{t=0}^{T-1}$，目标是恢复对应的三维人体运动 $\mathcal{M} = \{\pmb{\theta}_t \in \mathbb{R}^{K \times 3}, \mathbf{J}_t \in \mathbb{R}^{K \times 3}\}$，其中 $K$ 为关节数量。整个处理流程如下：

1. **点云特征提取**：原始点云序列首先通过预训练的 **PointNet++** 编码器提取逐帧特征 $\mathbf{F}_{\mathcal{P}}$，作为后续所有模块的观测条件。
2. **训练阶段的退化监督生成**：真实关节轨迹被拟合为最精细的贝塞尔曲线，随后通过**轨迹感知退化（TAD）** 策略逐级降采样，生成 $L$ 个时间尺度的运动表示 $\{\mathbf{M}_l\}_{l=1}^L$，作为渐进式重建的多级监督信号。
3. **推理阶段的渐进式重建**：
   - **时标运动变换器（TMT）** 以点云特征 $\mathbf{F}_{\mathcal{P}}$ 和可学习的多级运动嵌入 $\{\mathbf{E}_l\}_{l=1}^L$ 为输入，通过编码器结构预测各时间尺度的贝塞尔运动曲线 $\{\widehat{\mathbf{M}}_l\}_{l=1}^L$；
   - **多级运动聚合器（MMA）** 从最粗尺度开始，逐步上采样并融合多级运动表示，生成最终的细粒度运动序列；
   - **STGCN 逆运动学求解器** 将预测的关节位置转换为 SMPL 姿态参数。

### 模块关系与信息流控制

框架的关键设计在于**阶段间的信息流调控**。TMT 内部采用**块状因果掩码**（block-wise causal mask），约束每个运动 token 仅能关注来自更粗尺度的所有 token 和同尺度内的 token，形成从粗到细的层级依赖关系。这种设计确保粗粒度的全局运动趋势能够有效引导细粒度的局部运动恢复，而非让各尺度独立预测。

MMA 则通过**缩减机制**（reduction mechanism）逐步聚合多尺度运动表示：
$$
\widehat{\mathbf{M}}_{l+1}^{\prime} = \operatorname{MLP}\left(\operatorname{Resample}(\widehat{\mathbf{M}}_l^{\prime}), \widehat{\mathbf{M}}_{l+1}\right), \quad l = 2, \ldots, L-1
$$
其中 $\widehat{\mathbf{M}}_l^{\prime}$ 表示第 $l$ 级的聚合后表示，$\operatorname{Resample}$ 为上采样操作。最终输出 $\widehat{\mathbf{M}}_L^{\prime}$ 即为重建的细粒度运动序列。

整个框架在训练时采用**多级运动损失**进行端到端监督：
$$
\mathcal{L}_M = \sum_{l=1}^{L} \frac{1}{M_{s_l}} \left\| \widehat{\mathbf{M}}_l - \mathbf{M}_l \right\|_F^2
$$
确保每个时间尺度的预测都与对应的退化目标对齐。

### 与现有方法的根本差异

现有 LiDAR 动捕方法（如 **LiDARCap** (Li et al., CVPR 2022)、**LiveHPS**/**LiveHPS++** (Ren et al., CVPR/ECCV 2024)）直接从不完整的点云特征逐帧回归 SMPL 参数或中间特征，缺乏对时序运动先验的有效建模，在严重遮挡下姿态预测产生抖动甚至失败。BMLiCap 的核心改变在于：

| 设计维度 | 基线做法 | BMLiCap 做法 |
|---------|---------|-------------|
| **运动表示** | 直接逐帧回归 SMPL 参数 | 多级贝塞尔曲线表示，通过 TAD 生成层次化运动 |
| **重建策略** | 单阶段逐帧推理 | 从粗到细的渐进式重建（TMT + MMA） |
| **时序信息流** | 基于 GCN/Transformer 的帧级建模 | 块状因果掩码实现阶段间信息流调控 |
| **逆运动学** | 直接预测 SMPL 参数 | STGCN 求解器将关节位置转换为姿态参数 |

这种“先压缩、再渐进恢复”的范式使得模型即使在 50% 输入帧缺失的情况下仍能保持稳定性能（Fig. 7a），从根本上提升了对遮挡和噪声的鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/003_Figure_3.jpg]]
*Figure 3: The pipeline of our proposed BMLiCap framework. During training, we first apply the Bezier motion degradation module to ´ generate multi-level motion representations. Then, the progressive motion reconstruction module reconstructs the motion in a coarse-tofine manner, where a Time-scale Motion Transformer (TMT) predicts motion curves at different temporal scales conditioned on LiDAR features, and a Multi-level Motion Aggregator (MMA) fuses these multi-scale cues to produce the final fine-grained motion*



BMLiCap 的核心由两个级联模块构成：**轨迹感知贝塞尔退化 (TAD)** 与 **渐进式运动重建**。前者在训练时将原始关节轨迹转化为层次化贝塞尔运动表示，后者在推理时以由粗到细的方式从 LiDAR 点云中恢复人体运动。

### 问题形式化

给定长度为 $T$ 的 LiDAR 点云序列：

$$\mathcal { P } = \{ \mathbf { P } _ { t } \in \mathbb { R } ^ { N \times 3 } \} _ { t = 0 } ^ { T - 1 }$$

其中每帧包含 $N$ 个三维点。目标是恢复 $K$ 个关节的三维人体运动：

$$\mathcal { M } = \{ \pmb { \theta } _ { t } \in \mathbb { R } ^ { K \times 3 } , \mathbf { J } _ { t } \in \mathbb { R } ^ { K \times 3 } \} _ { t = 0 } ^ { \bullet }$$

其中 $\pmb{\theta}_t$ 为姿态参数，$\mathbf{J}_t$ 为关节位置。

### 轨迹感知贝塞尔退化 (TAD)

**核心思想**：人体运动可由贝塞尔曲线紧凑表示，即使大幅减少控制点仍能保留全局运动趋势（Figure 2）。TAD 利用这一特性生成多级运动表示作为监督信号。

**步骤 1：最精细贝塞尔拟合。** 对每个关节 $k$，用 $C^1$ 连续的三次贝塞尔曲线连接相邻帧的关节位置 $\mathbf{J}_t^{(k)}$ 和 $\mathbf{J}_{t+1}^{(k)}$：

$$\mathcal{B}_t^{(k)}(u) = (1-u)^3 \mathbf{J}_t^{(k)} + 3(1-u)^2 u \mathbf{C}_{t,2}^{(k)} + 3(1-u)u^2 \mathbf{C}_{t+1,1}^{(k)} + u^3 \mathbf{J}_{t+1}^{(k)}$$

其中 $\mathbf{C}_{t,2}^{(k)}$ 和 $\mathbf{C}_{t+1,1}^{(k)}$ 为控制点，保证曲线段间 $C^1$ 连续性。

**步骤 2：层次化退化。** 从最精细曲线中按时间间隔降采样锚点 $\widetilde{\mathbf{J}}_i^{(k)}$，并从原曲线提取该点的单位切向量：

$$\widehat{\mathbf{d}}_i^{(k)} = \widetilde{\mathbf{J}}_i^{(k)} \mathbf{C}_{t_i,1}^{(k)} / \| \widetilde{\mathbf{J}}_i^{(k)} \mathbf{C}_{t_i,1}^{(k)} \|_2$$

利用切方向构造退化后的新控制点：

$$\widetilde{\mathbf{C}}_{i,1}^{(k)} = \widetilde{\mathbf{J}}_i^{(k)} - \ell_{i,1} \widehat{\mathbf{d}}_i^{(k)}, \quad \widetilde{\mathbf{C}}_{i,2}^{(k)} = \widetilde{\mathbf{J}}_i^{(k)} + \ell_{i,2} \widehat{\mathbf{d}}_i^{(k)}$$

其中控制点长度 $\ell$ 通过最小二乘优化求解，以最佳逼近原始运动动态：

$$\min_{\{\ell_{i,2}, \ell_{i+1,1}\}} \sum_m \| \tilde{\mathcal{B}}_i^{(k)}(u_{i,m}) - \mathbf{Y}_{i,m}^{(k)} \|_2^2$$

通过重复降采样和参数调整，TAD 生成 $L$ 个时间尺度的运动表示 $\{\mathbf{M}_l\}_{l=1}^L$。Figure 4 展示了该退化过程：不仅重采样控制点，还调整其长度以更好地拟合最精细曲线。

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/004_Figure_4.jpg]]
*Figure 4: A demonstration of trajectory-aware Bezier degrada- ´ tion, we not only resample the control points but also adjust their lengths to better fit the finest curve*

### 渐进式运动重建

该模块以由粗到细的方式从 LiDAR 特征中恢复运动，包含两个子模块：

**时标运动变换器 (TMT)。** 首先用 PointNet++ 从点云序列提取逐帧特征 $\mathbf{F}_{\mathcal{P}}$，并与可学习的多级运动嵌入 $\{\mathbf{E}_l\}_{l=1}^L$ 一同送入标准 Transformer 编码器。TMT 输出各时间尺度的重建运动曲线：

$$\{ \widehat { \mathbf { M } } _ { l } \} _ { l = 1 } ^ { L } = \operatorname { M L P } \left( \operatorname { T M T } ( \mathbf { F } _ { \mathcal { P } } , \{ \mathbf { E } _ { l } \} _ { l = 1 } ^ { L } ) \right)$$

为调控阶段间信息流，TMT 的自注意力层施加**块状因果掩码 (block-wise causal mask)**：每个运动 token 只能关注所有更粗粒度层级的 token 以及同层级的前序 token。这迫使粗粒度运动趋势引导细粒度运动的恢复。

**多级运动聚合器 (MMA)。** MMA 采用渐进式上采样与融合机制，从最粗尺度开始，逐步融合更细粒度的运动表示：

$$\widehat { \mathbf { M } } _ { l + 1 } ^ { \prime } = \operatorname { M L P } \left( \operatorname { R e s a m p l e } ( \widehat { \mathbf { M } } _ { l } ^ { \prime } ) , \widehat { \mathbf { M } } _ { l + 1 } \right), \quad l = 2 , \ldots , L - 1$$

最终输出细粒度运动序列，再通过基于 STGCN 的逆运动学求解器转换为 SMPL 姿态参数。

**多级运动损失。** 训练时对各级贝塞尔运动表示施加监督：

$$\mathcal { L } _ { M } = \sum _ { l = 1 } ^ { L } \frac { 1 } { M _ { s _ { l } } } \left\| \widehat { \mathbf { M } } _ { l } - \mathbf { M } _ { l } \right\| _ { F } ^ { 2 }$$

其中 $M_{s_l}$ 为第 $l$ 级的时间尺度。该损失与关节位置损失、速度损失等联合优化。

**关键设计决策**：消融实验（Table 3, Table 4）表明，最优配置为 $L=3$ 级、调度 $\{32, 16, 8\}$，且 TAD 策略、多级运动 token、运动损失、块状因果掩码和多阶段运动聚合器各自带来显著增益。

### 补充图表

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/002_Figure_2.jpg]]
*Figure 2: Analysis of motion approximation error using Bezier ´ curves with different ratios of control points, indicating its robustness against occlusion*



## 实验与关键发现

### 核心定量结果

BMLiCap 在四个主流 LiDAR 人体运动捕捉基准上均取得了最优精度和时序连续性。Table 1 汇总了与现有方法的全面对比。在 **LiDARHuman26M** 基准上，BMLiCap 达到 MPJPE 70.1 mm、MPVPE 89.5 mm、AE 31.2 mm；当输入窗口扩展至 32 帧时，性能进一步提升至 **MPJPE 66.8 mm、MPVPE 85.4 mm、AE 28.8 mm**，显著优于 LiveHPS++、LiDARCap、NIE 等基线方法。在极具挑战性的 **FreeMotion** 数据集上，BMLiCap 相较 LiveHPS++ 实现了 **MPJPE 降低 14.7 mm、MPVPE 降低 16.3 mm、加速度误差降低 31.7 mm** 的大幅领先，验证了方法在自由运动场景下的鲁棒性。

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/005_Table_1.jpg]]
*Table 1: Comparison with state-of-the-art methods on four mainstream benchmarks*

### 消融实验

#### 轨迹感知退化策略的有效性

Table 3 系统评估了阶段数 L 与轨迹感知退化（TAD）策略的影响。实验表明，**在所有阶段数 L 的配置下，引入 TAD 均能持续提升 MPJPE**，验证了通过调整控制点长度以更好逼近最精细曲线这一设计的必要性。最优配置为 **L=3，调度方案 {32, 16, 8}**，此时 MPJPE 达到最低的 66.8 mm。

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/013_Table_3.jpg]]
*Table 3: Ablation study of stages and the effectiveness of our Trajectory-Aware Degradation (TAD) policy*

#### 渐进式重建模块的组件贡献

Table 4 对渐进式运动重建阶段的各组件进行了消融分析。逐步引入多级运动 token（m.s.）、多级运动损失（m.l.）、块状因果掩码（b.m.）以及多阶段运动聚合器（mma.）后，性能均获得稳定增益。这证实了**从粗到细的层次化信息流调控**和**多尺度运动表示的渐进融合**是性能提升的关键机制。

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/014_Table_4.jpg]]
*Table 4: Ablation study of the introduced components in our progressive motion reconstruction stage*

#### 运动表示对比

Table 2 将贝塞尔曲线表示与其他运动表示（如直接回归 SMPL 参数、基于 GCN 的时序建模等）进行了对比。结合 TAD 的贝塞尔表示（Bézier+TAD）取得了最优的 MPJPE 66.8 mm、MPVPE 85.4 mm、AE 28.8 mm，表明**层次化贝塞尔运动表示**在 LiDAR 人体运动捕捉任务上具有显著优势。

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/007_Table_2.jpg]]
*Table 2: Comparison with other motion representations on the Li-DARHuman26M benchmark*

### 鲁棒性分析

Figure 7 展示了模型在不同点云帧掩码策略和缺失比例下的稳定性测试。结果表明，**即使高达 50% 的输入帧缺失，BMLiCap 仍能保持稳定的性能输出**。这一鲁棒性源于贝塞尔曲线对全局运动趋势的紧凑保持能力——如 Figure 2 所示，即使大幅削减控制点，全局运动趋势依然得以保留，使模型能够弥合严重遮挡造成的观测断裂。

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/009_Figure_7.jpg]]
*Figure 7: Stability test under different point cloud frame masking policy and ratio*

### 定性可视化

Figure 5 的序列可视化对比显示，在严重遮挡场景下，其他方法产生明显的抖动甚至失败，而 BMLiCap 提供了连贯且准确的估计。Figure 6 的单帧可视化进一步表明，对于特殊运动或严重遮挡的样本，方法能够有效补偿缺陷，生成稳定且连贯的结果。Figure 8 可视化了各阶段预测的中间贝塞尔曲线，直观展示了从粗粒度运动趋势到细粒度运动细节的渐进恢复过程。Figure 9 的注意力图揭示了不同遮挡程度下跨层级交互的触发机制，为方法的可解释性提供了支撑。

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/006_Figure_5.jpg]]
*Figure 5: Sequential visualization. Even under severe occlusion, BMLiCap provides coherent, accurate estimations, while other methods produce jittery/failed results*

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/008_Figure_6.jpg]]
*Figure 6: Single frame visual comparisons. On samples with special motion or severe occlusion, our method can compensate for defects, producing stable and coherent results*

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/011_Figure_8.jpg]]
*Figure 8: Visualization of the predicted intermediate Bezier curves from each level of BMLiCap´*

![[assets/figures/papers/paper_list_l1055_https_openaccess_thecvf_com_content_CVPR2026_html_An_Bezier_Degradation/figures/012_Figure_9.jpg]]
*Figure 9: Attention map of different occlusion levels. The attention masking triggers cross-level interaction to fix missing frames*

### 失败模式与待验证问题

当前分析中未提取到明确的失败模式记录。以下问题需要手动验证：该方法在**极端非平滑运动**（如跌倒、突然转向）上的泛化能力；贝塞尔拟合的 **C¹ 连续性假设**是否适用于所有自然人体运动；以及如何将层次化运动表示方法扩展到**多人场景**。



## 定位与知识库关联

### 问题定位与核心瓶颈

LiDAR 人体运动捕捉 (LiDAR-based Human Motion Capture) 旨在从稀疏、带噪的点云序列中恢复精确的三维人体运动。现有方法面临一个根本性瓶颈：**直接从不完整的点云特征学习，缺乏对时序运动先验的有效建模**。当场景中出现严重遮挡或传感器噪声时，逐帧推理范式会导致姿态预测产生剧烈抖动甚至完全失败。这一瓶颈的本质在于，点云观测在单帧层面往往是高度退化的，而人体运动本身具有强时序结构——这一结构信息在现有方法中未被充分利用。

BMLiCap 的核心洞察在于：**人体运动可由贝塞尔曲线紧凑表示，即使大幅减少控制点仍能保留全局运动趋势**。如 Figure 2 所示，激进地剪枝贝塞尔控制点后，运动近似误差虽有所上升，但全局运动趋势得以保持。这一层次化特性为“由粗到细”的重建提供了理论依据——粗粒度运动表示对遮挡鲁棒，可作为细粒度恢复的强先验。

### 与基线方法的关系图谱

BMLiCap 继承并改造了 LiDAR 动捕领域的关键技术路线，其与主要基线的关系如下：

- **LiDARCap** (Li et al., CVPR 2022)：首个 LiDAR 动捕基准和基线方法，建立了从点云到 SMPL 参数的端到端回归范式。BMLiCap 沿用了点云编码器 (PointNet++) 与逆运动学求解的基本架构，但将“单阶段逐帧回归”替换为“多级贝塞尔运动表示 + 渐进式重建”，从根本上改变了信息流结构。

- **LiveHPS / LiveHPS++** (Ren et al., CVPR 2024 / ECCV 2024)：利用 SMPL 顶点特征和点云先验进行鲁棒跟踪，LiveHPS++ 进一步引入速度预测。BMLiCap 与之共享“利用时序信息提升鲁棒性”的目标，但技术路径截然不同：LiveHPS++ 在帧级引入速度约束，而 BMLiCap 通过贝塞尔曲线在运动轨迹层面进行层次化建模，在 FreeMotion 基准上将 MPJPE 降低 14.7 mm、加速度误差降低 31.7 mm/s²。

- **NIE** (Zhang et al., AAAI 2024)：通过邻域增强提升 3D 姿态估计精度。BMLiCap 的块状因果掩码机制与 NIE 的邻域聚合存在概念上的相似性——两者都试图扩大感受野以补偿局部观测缺失。但 BMLiCap 的掩码设计服务于跨时间尺度的信息流调控，而非空间邻域增强。

### 方法谱系中的关键改造

BMLiCap 对现有动捕范式进行了四个维度的系统性改造：

| 改造维度 | 基线做法 | BMLiCap 做法 | 因果机制 |
|---------|---------|-------------|---------|
| **运动表示** | 直接逐帧回归 SMPL 参数或中间特征 | 多级贝塞尔曲线表示，通过轨迹感知退化生成层次化运动表示 | 粗粒度表示对遮挡鲁棒，为细粒度恢复提供全局运动先验 |
| **重建策略** | 单阶段逐帧推理 | 从粗到细的渐进式重建 (TMT + MMA) | 先恢复全局趋势，再逐步填充细节，降低单阶段学习难度 |
| **时序信息流** | 基于 GCN 或 Transformer 的帧级时序建模 | 块状因果掩码实现阶段间信息流调控 | 粗粒度运动趋势引导细粒度运动恢复，避免错误传播 |
| **逆运动学求解** | 直接预测 SMPL 参数或使用其他 IK 方法 | 基于 STGCN 的逆运动学求解器 | 将预测关节位置转换为 SMPL 姿态参数，保持运动学一致性 |

这些改造形成了清晰的因果链条：**贝塞尔退化 → 层次化运动表示 → 渐进式重建 → 鲁棒运动恢复**。每一环节的消融实验均验证了其独立贡献 (Table 3, Table 4)。

### 适用边界与局限

尽管 BMLiCap 在四个主流基准上取得了最优性能，其适用边界值得审慎界定：

1. **运动平滑性假设**：贝塞尔曲线的 C¹ 连续性假设适用于大多数日常人体运动，但对于极端非平滑运动（如跌倒、突然转向、碰撞反弹），C¹ 连续性可能成为过度约束，导致运动细节被过度平滑。论文未在包含此类极端运动的数据集上进行验证，该边界需要进一步实验确认。

2. **单人场景限制**：当前方法针对单人动捕设计，贝塞尔退化策略和渐进式重建模块均未考虑多人交互场景中的遮挡交叉和身份混淆问题。扩展到多人场景需要重新设计运动表示和注意力掩码机制。

3. **训练数据依赖**：PointNet++ 编码器在合成人体实例上预训练，这可能引入合成-真实域间隙。论文未报告在纯真实数据上训练的性能对比，域迁移鲁棒性尚待验证。

### 开放问题

1. **贝塞尔拟合的普适性**：C¹ 连续贝塞尔参数化是否适用于所有自然人体运动？对于包含急停、跳跃落地等高加速度片段的运动，贝塞尔曲线的逼近误差上界如何？这关系到方法在体育、舞蹈等高速运动场景中的适用性。

2. **层次化表示的通用性**：轨迹感知退化策略能否推广到其他时序建模任务（如手势识别、步态分析）？其核心思想——通过可控退化生成易于学习的层次化表示——具有跨任务的迁移潜力，但需要针对性验证。

3. **计算效率与实时性**：BMLiCap 使用 12 层 Transformer 编码器和多级运动聚合器，在 4× RTX 4090 上训练 50 轮。论文未报告推理延迟，实时应用（如在线动捕、人机交互）的可行性需要补充延迟分析。

4. **与多模态融合的关系**：LiDAR 点云本质上提供几何信息，而 RGB 或 IMU 可补充纹理和惯性信息。贝塞尔运动表示能否作为统一的多模态运动先验，融合来自不同传感器的观测？这可能是提升极端遮挡下性能的潜在方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Bezier_Degradation_Modeling_for_LiDAR_based_Human_Motion_Capture.pdf]]
