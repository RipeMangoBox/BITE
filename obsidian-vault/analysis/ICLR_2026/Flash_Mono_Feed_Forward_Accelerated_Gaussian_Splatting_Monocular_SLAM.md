---
title: "Flash-Mono: Feed-Forward Accelerated Gaussian Splatting Monocular SLAM"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Flash_Mono_Feed_Forward_Accelerated_Gaussian_Splatting_Monocular_SLAM_774a8b41cda9.pdf
project_link: "https://victkk.github.io/flash-mono"
code_link: "https://github.com/borglab/gtsam"
aliases:
- FM
- Flash-Mono
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 将逐帧优化的闭环切换为递归前馈模型，直接预测每帧相机位姿与逐像素2DGS属性，仅需极轻量后端微调；同时利用递归隐藏状态作为紧凑子地图描述子，实现单次前馈重定位与Sim(3)全局优化，根本性突破速度与漂移难题。
primary_logic: 递归前馈架构中的隐藏状态通过交叉注意力逐步聚合多帧几何与纹理信息，不仅支持直接预测高质量高斯属性与位姿，更可作为长期记忆在回环时以条件前馈方式恢复过去坐标框架，从而避免增量式前馈方法常见的尺度与位姿漂移。
claims:
- Flash‑Mono 通过前馈预测取代从零训练，实现10 FPS+实时性能，速度较同期GS‑SLAM方法提升约10倍。
- 在ScanNetV1和BundleFusion数据集上，跟踪精度（ATE RMSE）显著优于所有传统和GS‑SLAM基线，也优于最近的前馈SLAM系统MASt3R‑SLAM。
- 仅用20次后端迭代（MonoGS/S3PO‑GS的十分之一），渲染质量即达到或超越基线，PSNR提升约2‑4 dB，LPIPS降低0.2‑0.3。
- 深度几何精度（Depth L1误差）大幅领先，在ScanNet和BundleFusion上平均误差分别为0.34 m和0.21 m，明显优于MonoGS的1.19 m/1.20 m。
---

# Flash-Mono: Feed-Forward Accelerated Gaussian Splatting Monocular SLAM

> [!tip] 核心洞察
> 递归前馈架构中的隐藏状态通过交叉注意力逐步聚合多帧几何与纹理信息，不仅支持直接预测高质量高斯属性与位姿，更可作为长期记忆在回环时以条件前馈方式恢复过去坐标框架，从而避免增量式前馈方法常见的尺度与位姿漂移。

| 字段 | 内容 |
|------|------|
| 中文题名 | Flash-Mono：前馈加速的高斯溅射单目SLAM |
| 英文题名 | Flash-Mono: Feed-Forward Accelerated Gaussian Splatting Monocular SLAM |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=nv3q3crc5D) · [Project](https://victkk.github.io/flash-mono) · [arXiv](https://arxiv.org/abs/2507.02863) · [Code](https://github.com/borglab/gtsam) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Flash‑Mono |
| Dataset | ScanNetV1, ScanNet / BundleFusion, KITTI Odometry |

> [!tip] 效果简介
> - ScanNetV1 (tracking) 上，ATE RMSE (cm) 场景0054: 11.69 cm，所有场景均低于最佳基线 vs MASt3R‑SLAM 场景0054: 13.25 cm (-1.56 cm（在该场景）)。
> - ScanNetV1 (rendering) 上，PSNR (dB) 17.75 – 21.73 dB（各场景） vs MonoGS PSNR 14.52 – 19.24 dB (提升约 2 – 4 dB)；LPIPS 0.39 – 0.45 vs MonoGS LPIPS 0.54 – 0.74 (绝对值降低 0.2 – 0.3)。
> - ScanNet / BundleFusion (geometry) 上，Mean Depth L1 (m) ScanNet 0.34, BundleFusion 0.21 vs MonoGS 1.19 / 1.20 (大幅降低（约 0.85 – 1.0 m）)。

## 概述

单目密集同步定位与建图（SLAM）是机器人、AR/VR 和自动驾驶的核心感知任务。近年来，基于 3D 高斯溅射（3DGS）的 SLAM 方法凭借其高质量的场景重建和新视图合成能力受到广泛关注。然而，现有单目 GS‑SLAM 系统普遍采用**从零训练（Train‑from‑Scratch）**范式：每个关键帧需从随机初始化开始，经数十至数百次高斯优化迭代，单帧耗时约 1 秒，导致系统速度仅约 1 FPS。此外，单帧深度先验存在尺度不一致，阻碍多视图几何一致性，成为实时性与精度的双重瓶颈。

**Flash‑Mono** 提出了一种根本性的范式转换——将逐帧优化的闭环切换为**递归前馈模型**，直接预测每帧相机位姿与逐像素 2D Gaussian Surfels（2DGS）属性，仅需极轻量的后端微调。其核心洞察在于：递归架构中的隐藏状态通过交叉注意力逐步聚合多帧几何与纹理信息，不仅支持直接预测高质量高斯属性与位姿，更可作为长期记忆，在回环时以条件前馈方式恢复过去坐标框架，从而避免增量式前馈方法常见的尺度与位姿漂移。

系统由三大模块构成：**（1）递归前馈前端**，每帧联合预测 SE(3) 位姿与 2DGS 属性，同时更新隐藏状态；**（2）2DGS 建图后端**，对前馈预测进行自适应体素化、增量融合与轻量局部渲染优化（仅 20 次迭代）；**（3）基于隐藏状态的闭环模块**，将隐藏状态作为紧凑子地图描述子，实现单次前馈重定位与 Sim(3) 全局优化。

实验表明，Flash‑Mono 实现了 **10 FPS+ 的实时性能**，速度较同期 GS‑SLAM 方法提升约 10 倍。在 ScanNetV1 和 BundleFusion 数据集上，跟踪精度（ATE RMSE）显著优于所有传统和 GS‑SLAM 基线，也优于最近的前馈 SLAM 系统 **MASt3R‑SLAM**。仅用基线方法十分之一的优化迭代次数，渲染质量即达到或超越 **MonoGS** 与 **S3PO‑GS**，PSNR 提升约 2–4 dB，LPIPS 降低 0.2–0.3。深度几何精度大幅领先，ScanNet 和 BundleFusion 上平均深度 L1 误差分别为 0.34 m 和 0.21 m，远低于 MonoGS 的 1.19 m 和 1.20 m。在 KITTI Odometry 上同样展现了优异的跟踪与渲染性能。

## 背景与动机

### 单目稠密SLAM的实时性困局

同时定位与建图（SLAM）是机器人、AR/VR和自动驾驶的核心感知任务。近年来，基于3D Gaussian Splatting（3DGS）的稠密SLAM方法凭借其高保真场景表示和可微渲染能力，在重建质量上取得了显著突破。然而，现有单目GS-SLAM系统普遍面临一个根本性瓶颈：**从零训练（Train-from-Scratch）范式导致系统速度极慢，难以满足实时应用需求。**

具体而言，以MonoGS为代表的单目GS-SLAM方法在每个关键帧都需要从随机初始化开始，对高斯椭球体的位置、颜色、协方差等属性进行数十至数百次迭代优化，单帧耗时约1秒，导致系统整体运行速度仅约1 FPS。这种逐帧“训练”的闭环虽然保证了局部重建质量，却将计算开销推至不可接受的水平，成为稠密SLAM走向实用的主要障碍。

### 单目深度先验的尺度不一致问题

为缓解从零训练的负担，部分方法（如DepthGS、S3PO-GS）引入单目深度估计网络提供几何先验，试图加速高斯属性优化。但这一策略引入了新的隐患：**单帧深度先验存在尺度不一致性**——不同帧的深度估计可能具有不同的绝对尺度，且缺乏多视图几何一致性约束。这种尺度模糊性在长序列中逐步累积，不仅削弱了先验的有效性，还可能导致后端优化陷入局部极小，反而损害全局轨迹精度和地图一致性。

### 前馈SLAM的兴起与遗留挑战

最近，以MASt3R-SLAM为代表的前馈SLAM系统尝试绕开逐帧优化，直接通过预训练网络预测场景结构和相机位姿。这类方法在速度上取得了数量级的提升，但其增量式前馈设计缺乏显式的长期记忆机制：网络仅基于当前帧和有限的历史窗口进行预测，无法有效利用远距离的时序上下文。因此，它们在长序列中仍面临**尺度漂移和位姿累积误差**的问题，且通常不具备闭环检测与全局优化的能力。

### 本文动机：从“训练”到“预测”的范式转移

上述分析揭示了一个清晰的改进方向：**将逐帧优化的闭环切换为递归前馈模型，在保持稠密建图质量的同时实现实时性能。** 核心思路是训练一个能够逐步聚合多帧视觉信息的前馈网络，使其直接预测每帧的高质量高斯属性和相机位姿，从而将昂贵的“从零训练”降级为轻量级的后端微调。同时，这一递归架构中的隐藏状态天然具备长期记忆能力，可作为紧凑的子地图描述子，支撑高效的闭环检测与全局位姿图优化，从根源上缓解漂移问题。

Flash-Mono正是在这一动机下提出的：通过一个递归前馈前端联合预测位姿与2DGS属性、一个轻量2DGS建图后端进行增量融合与微调，以及一个基于隐藏状态的闭环模块，首次在单目稠密GS-SLAM中实现了10 FPS以上的实时性能，同时将跟踪与建图精度提升至新的最优水平。

## 核心创新

Flash‑Mono 的核心创新在于将单目 GS‑SLAM 从“逐帧从零训练”范式根本性地切换为“递归前馈预测 + 轻量后端微调”范式，同时将隐藏状态复用为长期记忆以支撑高效闭环。以下从三个关键维度展开。

### 1. 从 Train‑from‑Scratch 到 Predict‑and‑Refine 的范式转换

现有单目 GS‑SLAM 方法（如 **MonoGS**、**DepthGS**、**S3PO‑GS**）在每个关键帧都需要从随机初始化开始，经数十至数百次高斯优化迭代（典型值约 250 次），单帧耗时约 1 秒，导致系统整体仅约 1 FPS。这一“从零训练”范式是制约实时性的根本瓶颈。

Flash‑Mono 提出 **Predict‑and‑Refine** 策略，将闭环切换为前馈模型：

- **高斯属性获取方式**：用递归前馈模型直接预测逐像素 2DGS 属性，后端仅需 20 次迭代轻量微调（约为 MonoGS/S3PO‑GS 的十分之一），渲染质量即达到或超越基线——PSNR 提升约 2–4 dB，LPIPS 绝对值降低 0.2–0.3。
- **前端位姿估计**：不再依赖 ORB‑SLAM3 等外部 SLAM 或单目深度/光流网络提供间接先验，而是端到端联合预测相机位姿与 2DGS 属性，通过交叉注意力融合多帧上下文并递归更新隐藏状态。

这一范式转换直接带来约 10 倍速度提升（10+ FPS），是系统实时性的核心驱动力。

### 2. 隐藏状态作为长期记忆：单次前馈重定位与全局优化

Flash‑Mono 的第二个关键创新在于赋予隐藏状态双重角色——不仅是逐帧预测的上下文载体，更作为紧凑的子地图描述子，支撑高效闭环检测与全局优化。

- **场景几何表示**：系统采用 **2D Gaussian Surfel (2DGS)** 替代传统 3D Gaussian Ellipsoid，以增强几何保真度。前馈模型预测的 2DGS 属性与隐藏状态共同构成场景的紧凑表示。
- **闭环与全局优化机制**：视频流被分割为子地图以抑制灾难性遗忘，每个子地图的最终隐藏状态被缓存至 **Bag of Hidden States**。当外观检测发现回环候选时，系统检索历史隐藏状态，对当前帧执行**单次条件前馈重定位**，利用历史与当前隐藏状态对应的点云在相机坐标系下仅差一个尺度因子的特性，鲁棒求解 Sim(3) 约束，并纳入位姿图全局优化。

这一设计使隐藏状态从“短期工作记忆”升级为“长期可检索记忆”，从根本上突破了增量式前馈方法常见的尺度与位姿漂移难题。

### 3. 创新点的因果联动

上述三个 changed slots 并非孤立改进，而是形成因果闭环：

1. **递归前馈架构**通过交叉注意力逐步聚合多帧几何与纹理信息，使得直接预测高质量高斯属性与位姿成为可能；
2. 高质量的前馈预测大幅降低后端优化负担（从 250 次迭代降至 20 次），实现 **10 FPS+ 实时性能**；
3. 隐藏状态作为长期记忆，使系统在回环时能以条件前馈方式恢复过去坐标框架，从而在保持实时性的同时，**跟踪精度（ATE RMSE）显著优于所有传统和 GS‑SLAM 基线**，也优于最近的前馈 SLAM 系统 **MASt3R‑SLAM**。

**证据强度**：上述创新均有消融实验支撑——后端细化迭代从 0 增至 10 次时 PSNR 由 20.14 升至 22.41 dB（收益递减）；子地图片段长度 8 帧时 ATE RMSE 最低（0.106）；自适应体素化模块将高斯原语数量减少超 58%（1.35M→0.56M），PSNR 仅轻微下降（19.70→19.44）。主实验在 ScanNetV1、BundleFusion、KITTI Odometry 三个数据集上均验证了跟踪精度与渲染质量的双重领先。

## 整体框架

Flash‑Mono 提出了一种 **Predict‑and‑Refine** 范式，将传统单目 GS‑SLAM 中逐帧“从零训练”（Train‑from‑Scratch）的闭环切换为**递归前馈预测 + 轻量后端微调**的架构。系统由三个核心模块构成：

1. **递归前馈前端（Recurrent Feed‑Forward Frontend）**：接收视频帧流，通过交叉注意力机制逐步聚合多帧几何与纹理信息到隐藏状态中，并联合预测相机位姿与逐像素 2DGS 属性。
2. **2DGS 建图后端（2DGS Mapping Backend）**：对前馈预测进行自适应体素化、增量地图融合，仅需约 20 次优化迭代即可完成轻量渲染微调。
3. **基于隐藏状态的回环闭合（Loop Closure via Hidden State）**：将隐藏状态作为紧凑的子地图描述子缓存于“隐藏状态袋”（Bag of Hidden States）中，检测回环后执行单次条件前馈重定位，并求解 Sim(3) 约束纳入全局位姿图优化。

### 数据流与模块关系

Figure 2 展示了系统的完整数据流。对于每一帧输入图像 $I_t$，递归前馈模型 $f$ 以当前帧和上一隐藏状态 $M_{t-1}$ 为输入，联合预测三个输出：

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline. For each new frame, our recurrent model jointly infers the camera pose and perpixel 2DGS attributes conditioned on a hidden state. The hidden state is updated simultaneously. To avoid catastrophic forgetting, the stream is partitioned into submaps. The hidden state is reinitialized for each submap. Past hidden states are cached in the Bag of Hidden States. Upon loop detection, i.e., revisiting a location, we perform a single forward pass on the loop frame conditioned on the past hidden state to relocalize the current frame in the past submap. A following pose graph optimization is then performed to correct the full trajectory. In the backend, per-frame 2DGS attributes prediction i...*

$$\hat{T}_t,\; \hat{\mathcal{G}}_t,\; M_t = f(I_t,\; M_{t-1})$$

其中 $\hat{T}_t$ 为相机位姿（SE(3)），$\hat{\mathcal{G}}_t$ 为当前帧坐标系下的逐像素 2DGS 属性图，$M_t$ 为更新后的隐藏状态。

为抑制递归架构在长序列上的灾难性遗忘，系统将视频流分割为固定长度的子地图（submap），每个子地图开始时重新初始化隐藏状态。子地图的最终隐藏状态被缓存至隐藏状态袋，作为长期记忆供后续回环使用。

当外观检测模块发现回环候选时，系统检索历史子地图的隐藏状态，对当前回环帧执行条件前馈重定位——即利用历史隐藏状态在单次前向传播中恢复过去坐标框架下的位姿与高斯属性。随后通过相对尺度最小二乘估计与 Sim(3) 约束构建，将回环边纳入位姿图优化，在 sim(3) 李代数上全局校正轨迹。

在后端，逐帧预测的 2DGS 属性经自适应体素化压缩后增量融合为全局 2DGS 地图，并通过仅 20 次迭代的局部渲染优化完成微调。前端推理与后端优化在并行线程中执行，使得系统整体达到 10+ FPS 的实时性能。

## 核心模块与公式推导

Flash‑Mono 由三大核心模块构成：递归前馈前端（Recurrent Feed‑Forward Frontend）、2DGS 建图后端（2DGS Mapping Backend）以及基于隐藏状态的回环闭合模块（Loop Closure via Hidden State）。系统流水线如 Figure 2 所示。

### 2DGS 场景表示与可微渲染

为增强几何精度，Flash‑Mono 采用 2D Gaussian surfels（2DGS）替代传统 3D 高斯椭球。每个 2DGS 原语由中心位置 $\pmb{\mu}_i$、协方差矩阵 $\Sigma_i$、颜色 $\pmb{c}_i$ 和不透明度 $\sigma_i$ 参数化。像素 $p$ 处的体积渲染通过 alpha 混合完成：

$$w_i(p) = \sigma_i \cdot \exp\left(-\frac{1}{2}(p-\pmb{\mu}_i)^T \Sigma_i^{-1}(p-\pmb{\mu}_i)\right)$$

$$(\hat{I}, \hat{D}, \hat{A}) = \sum_{i=1}^N (\pmb{c}_i, z_i, 1) w_i \prod_{j=1}^{i-1} (1-w_j)$$

其中 $\hat{I}$ 为渲染颜色，$\hat{D}$ 为渲染深度，$\hat{A}$ 为累积不透明度，$z_i$ 为第 $i$ 个 surfel 在相机坐标系下的深度。该公式是整个 2DGS 可微渲染管线的基础（§3）。

### 递归前馈前端

前端核心是一个递归前馈模型 $f$，以当前帧 $I_t$ 和上一时刻隐藏状态 $M_{t-1}$ 为输入，联合预测三个输出：

$$\hat{T}_t, \hat{\mathcal{G}}_t, M_t = f(I_t, M_{t-1})$$

其中 $\hat{T}_t \in SE(3)$ 为相机位姿估计，$\hat{\mathcal{G}}_t$ 为逐像素对齐的 2DGS 属性图，$M_t$ 为更新后的隐藏状态（§4.1）。

**架构细节**：每帧图像首先经 ViT 编码器转化为视觉 token $F_t = \operatorname{Encoder}(I_t)$。模型随后通过两个互连的解码器，在视觉 token $F_t$ 与持久隐藏状态 $M_{t-1}$ 之间进行双向交叉注意力信息交换，逐步聚合多帧几何与纹理信息。隐藏状态在此过程中充当紧凑的子地图描述子，不仅支持直接预测高质量高斯属性与位姿，更在回环时作为长期记忆，以条件前馈方式恢复过去坐标框架。

**训练损失**：前端模型端到端训练，总损失为三项加权和：

$$\mathcal{L}_{\mathrm{total}} = \lambda_{\mathrm{pose}} \mathcal{L}_{\mathrm{pose}} + \lambda_{\mathrm{geo}} \mathcal{L}_{\mathrm{geo}} + \mathcal{L}_{\mathrm{render}}$$

其中 $\mathcal{L}_{\mathrm{pose}}$ 为位姿损失，$\mathcal{L}_{\mathrm{geo}}$ 为几何损失，$\mathcal{L}_{\mathrm{render}}$ 为渲染损失（§4.1）。

### 回环闭合与位姿图优化

为抑制灾难性遗忘，输入视频流被分割为较短的子地图（submap），每个子地图的隐藏状态重新初始化。每个子地图的最终隐藏状态被缓存至“隐藏状态袋”（Bag of Hidden States）作为长期记忆（§4.2）。

**回环重定位**：当外观检测到回环候选后，系统检索历史子地图的隐藏状态，对当前帧执行单次条件前馈重定位。由于历史与当前隐藏状态对应的点云在相机坐标系下仅差一个尺度因子，可鲁棒求解相对尺度：

$$s^{*} = \underset{s}{\operatorname{argmin}} \sum_k \left\| \pmb{\mu}_k^b - s \cdot \pmb{\mu}_k^a \right\|^2$$

结合估计的尺度 $s^{*}$ 与相对位姿 $R_{ji}, t_{ji}$，构造 Sim(3) 回环约束：

$$\mathbf{H}_{ji} = \begin{pmatrix} s^{*} R_{ji} & t_{ji} \\ \mathbf{0}^T & 1 \end{pmatrix}$$

**全局位姿图优化**：将所有顺序约束、子地图间对齐约束和回环约束统一纳入位姿图，在 sim(3) 李代数上进行非线性最小二乘优化：

$$\mathcal{T}^{W^{*}} = \underset{T^W}{\arg\min} \sum_{(i,j)\in\mathcal{E}} \left\| \log\left( \mathbf{H}_{ji}^{-1} \cdot \left( (\mathbf{T}_i^W)^{-1} \cdot \mathbf{T}_j^W \right) \right) \right\|_{\Omega}^2$$

该优化融合所有边约束，输出全局一致的相机轨迹（§4.2）。

### 2DGS 建图后端

后端接收前馈前端预测的逐帧 2DGS 属性，执行以下操作（§4.3）：

1. **自适应体素化**：对 2×2 像素块内的 2DGS 原语进行合并，属性取平均：

   $$\theta_{\mathrm{merged}} = \frac{1}{N} \sum_{n=1}^{N} \theta_n, \quad \mathrm{for} \; \theta \in \{ \mu, \sigma, c, s \}$$

   该模块可将高斯原语数量减少超过 58%，PSNR 仅轻微下降。

2. **增量地图融合**：将多帧预测融合为全局一致的 2DGS 地图。

3. **轻量局部渲染优化**：每关键帧仅执行 20 次迭代（MonoGS/S3PO-GS 的十分之一），对前馈预测进行微调，即“Predict-and-Refine”范式。

4. **回环后地图校正**：回环触发位姿图优化后，对全局 2DGS 地图执行高效刚体校正。

## 实验与分析

### 核心实验设置

Flash‑Mono 在三个标准基准上评估：**ScanNetV1**、**BundleFusion** 和 **KITTI Odometry**。跟踪精度以 **ATE RMSE**（经 Sim(3) 对齐）衡量，渲染质量以 **PSNR / SSIM / LPIPS** 衡量，几何精度以 **Depth L1 Error** 衡量。所有实验在单卡 RTX 4090 + Intel Xeon 6133 平台上运行。对比基线覆盖三类：传统特征法（**ORB‑SLAM3**）、深度光流法（**DROID‑SLAM**）、前馈重建法（**MASt3R‑SLAM**），以及从零训练的 GS‑SLAM 方法（**MonoGS**、**DepthGS**、**S3PO‑GS**）。

公平性需注意：MonoGS 在 ScanNet 0054/0465 和 BundleFusion apt0 序列因内存不足崩溃，其指标仅基于崩溃前子序列，可能偏乐观；S3PO‑GS 在 KITTI 07 序列运行失败，仅报告有效子序列；DepthGS 的 FPS 测量已包含 UniDepthV2 单目深度预测耗时。

### 跟踪精度：ATE RMSE

Table 1 展示了 ScanNetV1 和 BundleFusion 上的 ATE RMSE 对比。Flash‑Mono 在所有场景上均显著优于传统和 GS‑SLAM 基线，在多数场景上也超越了前馈方法 MASt3R‑SLAM。以 ScanNet 场景 0054 为例，Flash‑Mono 的 ATE RMSE 为 11.69 cm，较 MASt3R‑SLAM 的 13.25 cm 降低约 1.56 cm。在 KITTI Odometry 上（Table 3），Flash‑Mono 同样全面领先：序列 06 的 ATE RMSE 为 9.93 m，而 S3PO‑GS 为 16.43 m，绝对降幅达 6.50 m。

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/004_Table_1.jpg]]
*Table 1: ATE RMSE (cm) on ScanNetV1 and BundleFusion datasets. Lower is better. We mark the first and second best results*

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/007_Table_3.jpg]]
*Table 3: ATE RMSE (m) on KITTI Odometry. Lower is better*

### 渲染质量：PSNR / SSIM / LPIPS

Table 2 报告了渲染质量对比。Flash‑Mono 仅使用 **20 次后端优化迭代**（MonoGS 和 S3PO‑GS 的 1/10），渲染质量即达到或超越基线。在 ScanNetV1 上，Flash‑Mono 的 PSNR 为 17.75–21.73 dB，较 MonoGS 的 14.52–19.24 dB 提升约 2–4 dB；LPIPS 为 0.39–0.45，较 MonoGS 的 0.54–0.74 绝对值降低 0.2–0.3。定性对比见 Figure 3，Flash‑Mono 在新视图合成中展现出更清晰的纹理和更少的伪影。

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/005_Table_2.jpg]]
*Table 2: Mapping quality on ScanNetV1 and BundleFusion. Higher is better for SSIM/PSNR, lower is better for LPIPS. We mark the first and second best results*

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative Rendering Results*

### 几何精度：Depth L1 Error

Table 5 给出了深度几何精度的定量对比。Flash‑Mono 在 ScanNet 上的平均 Depth L1 误差仅为 **0.34 m**，在 BundleFusion 上为 **0.21 m**，而 MonoGS 分别为 1.19 m 和 1.20 m，降幅约 0.85–1.0 m。Figure 4 的深度图定性对比进一步验证了 Flash‑Mono 在几何重建上的显著优势。

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/010_Table_5.jpg]]
*Table 5: Mean Depth L1 Error (m) on ScanNet and BundleFusion. We mark the best results*

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative Analysis on Rendered Depth*

### 速度分析

Flash‑Mono 通过前馈预测取代从零训练，实现 **10 FPS+** 的实时性能，速度较同期 GS‑SLAM 方法提升约 10 倍。Table 8 展示了各模块的运行时间分解：系统以前端和后端并行线程运行，后端为主要瓶颈；回环操作为稀疏事件，对实时性影响有限。通过 CUDA Graph 优化（Figure 8），单批次推理延迟进一步降低。

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/016_Table_8.jpg]]
*Table 8: Runtime breakdown of Flash-Mono. The system runs in parallel threads, with the Backend being the primary bottleneck. Loop closure operations are sparse events*

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/015_Figure_8.jpg]]
*Figure 8: CUDA Graph optimization*

### 消融实验

Figure 5 系统性地揭示了关键设计选择的影响：

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/009_Figure_5.jpg]]
*Figure 5: Ablation studies. (a) Refine Iterations vs. PSNR. (b) Submap Length vs. ATE RMSE. (c) Loop Closure Settings. (d) PSNR vs. Model Size*

- **后端细化迭代次数**（Figure 5a）：无细化（0 次迭代）时，前馈模型直接输出 PSNR 为 20.14 dB；应用 10 次迭代后 PSNR 升至 22.41 dB，表明轻量微调即可显著提升渲染质量；继续增加迭代次数收益递减，验证了“Predict‑and‑Refine”范式的有效性——高质量前馈预测大幅降低了对昂贵后端优化的需求。

- **子地图长度**（Figure 5b）：子地图片段长度为 8 帧时获得最低 ATE RMSE（0.106）；过短或过长的子地图均导致跟踪误差增大，揭示了递归架构中记忆窗口长度的最优平衡点。

- **自适应体素化**：该模块将高斯原语数量减少超过 58%（1.35M → 0.56M），PSNR 仅轻微下降（19.70 → 19.44），在地图紧凑度与渲染质量之间取得了高效平衡。Table 9 进一步展示了 Flash‑Mono 在 TUM 数据集上的高斯原语总数对比，验证了其地图紧凑性。

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/017_Table_9.jpg]]
*Table 9: Quantitative comparison of the total Gaussian count on the TUM dataset. Our method maintains a balance between map density and compactness*

- **回环设置**（Figure 5c）和**模型尺寸**（Figure 5d）的消融也分别验证了隐藏状态回环机制和模型容量的影响。

### 失败模式与局限性

尽管 Flash‑Mono 在多数场景中表现优异，仍存在以下局限：

1. **模型参数量巨大**：总参数量达 795.7 M（Table 7），需约 3 GB 显存，限制了在低功耗边缘设备上的直接部署。float16 量化和 CUDA Graphs 可部分缓解，但未根本解决。

![[assets/figures/papers/paper_list_l82_https_openreview_net_forum_id_nv3q3crc5D/figures/014_Table_7.jpg]]
*Table 7: Detailed breakdown of Flash-Mono model parameters*

2. **灾难性遗忘**：递归架构在处理极长序列时仍存在遗忘问题，当前通过人工分块（子地图）缓解，缺乏自适应记忆窗口机制。

3. **跨域泛化未充分验证**：训练依赖 ScanNet++、DL3DV 等多个室内/外数据集，零样本跨域泛化能力未系统评测，未知场景或极端光照下可能退化。

4. **终身建图未系统评测**：Figure 9 展示了隐藏状态在环境变化（夜晚→白天）下的重定位潜力，但未在真正长周期、环境动态变化的场景下进行系统评测，隐藏状态更新与终身建图策略仍需专门训练和工程实现。

## 方法谱系与知识库定位

### 1. 在SLAM谱系中的位置：从优化驱动到前馈驱动

Flash‑Mono 的根本贡献在于将单目稠密SLAM的核心范式从“逐帧从零优化”（Train‑from‑Scratch）切换为“递归前馈预测+轻量后端微调”（Predict‑and‑Refine）。这一转变使其在方法谱系中处于传统SLAM、深度学习SLAM与高斯溅射SLAM三股脉络的交汇点，并同时突破了它们各自的核心瓶颈。

**相对于传统与间接SLAM。** 经典特征法SLAM（如 **ORB‑SLAM3**）依赖稀疏特征匹配与光束平差（BA），在弱纹理或快速运动场景易跟踪丢失，且不产生稠密地图。深度光流法SLAM（如 **DROID‑SLAM**）通过稠密光流与BA联合优化提升了鲁棒性，但计算开销大且仍不直接输出可渲染的场景表示。Flash‑Mono 以端到端前馈方式直接预测位姿与逐像素高斯属性，绕过了显式特征匹配与BA的级联误差，在 ScanNetV1 和 BundleFusion 上的 ATE RMSE 显著优于上述两类基线（Table 1），表明前馈隐式多帧融合在跟踪精度上已超越传统显式几何优化范式。

**相对于“从零训练”式GS‑SLAM。** 同期单目GS‑SLAM（**MonoGS**、**DepthGS**、**S3PO‑GS**）均遵循“每关键帧从随机初始化开始，经数百次高斯优化迭代”的范式。这导致两个结构性问题：（1）单帧速度约1 FPS，无法实时；（2）单帧深度先验（如单目深度网络输出）存在尺度不一致，多视图几何一致性差。Flash‑Mono 用递归前馈模型一次性预测高质量2DGS属性，后端仅需20次迭代（MonoGS/S3PO‑GS的十分之一），在10 FPS+实时运行的同时，渲染PSNR提升约2–4 dB，LPIPS降低0.2–0.3（Table 2），深度L1误差从MonoGS的约1.2 m降至0.21–0.34 m（Table 5）。这证明前馈预测不仅加速了系统，更通过多帧上下文聚合从根本上解决了单帧深度先验的尺度不一致问题。

**相对于前馈重建式SLAM。** **MASt3R‑SLAM** 是最近的前馈SLAM系统，利用预训练立体匹配模型进行帧间配准与稠密重建。Flash‑Mono 在大多数ScanNet场景上跟踪精度优于MASt3R‑SLAM（Table 1），且额外提供了可渲染的高斯地图和基于隐藏状态的闭环能力。关键差异在于 Flash‑Mono 的递归架构将历史信息显式编码为隐藏状态，使其具备长期记忆与条件重定位能力，而MASt3R‑SLAM等增量式前馈方法缺乏这一机制，在长序列中更易累积漂移。

### 2. 核心设计决策的适用边界

Flash‑Mono 的每个关键设计决策都同时带来了性能增益和适用边界，理解这些边界对后续工作至关重要。

**递归前馈架构与子地图分块。** 隐藏状态通过交叉注意力聚合多帧信息，是系统精度与闭环能力的核心。但递归架构在极长序列上仍存在灾难性遗忘——隐藏状态的固定容量无法无限容纳历史信息。当前方案通过人工将视频流分割为固定长度子地图（消融实验表明8帧最优，ATE RMSE = 0.106）来重置隐藏状态，这本质上是一种固定窗口的记忆管理策略。在需要跨子地图长期关联的场景（如大尺度室外自动驾驶），固定分块可能割裂关键的时空依赖，需要自适应记忆窗口或层次化隐藏状态机制。

**“预测‑微调”范式与模型容量。** 前馈模型的高质量预测是轻量后端（20次迭代）有效的前提。这要求模型在训练阶段见过足够多样化的场景，以学习通用的几何与外观先验。当前模型参数量达795.7 M，需约3 GB显存（Table 7），在低功耗边缘设备上部署困难。消融实验显示，减小模型尺寸会导致PSNR下降（Figure 5d），表明前馈预测质量与模型容量之间存在强耦合——这是“预测‑微调”范式固有的“精度‑效率”权衡，而非单纯的工程问题。

**基于隐藏状态的闭环。** 闭环模块利用缓存的历史隐藏状态对当前帧执行单次前馈重定位，并求解Sim(3)约束。其有效性依赖于两个假设：（1）重访场景的外观与缓存时相近；（2）隐藏状态编码了足够的几何信息以支持跨子地图的尺度对齐（通过最小二乘求解相对尺度）。在环境光照、季节或物体布局发生显著变化的终身建图场景中，外观匹配可能失效，隐藏状态的直接条件化也可能产生错误的位姿估计。附录中的案例研究（Figure 9）展示了从夜晚到白天的重定位能力，但这仅是初步验证，系统性的时序变化鲁棒性尚未建立。

### 3. 已知局限与开放问题

**显存与计算效率。** 795.7 M参数和约3 GB显存是当前最直接的部署障碍。虽然float16量化和CUDA Graphs优化可将单帧推理延迟降至可接受范围，但模型压缩（如高效注意力机制、知识蒸馏）对前馈预测精度的影响尚未系统研究。如何在保持“预测‑微调”范式优势的前提下将系统压缩至移动平台，是一个开放问题。

**终身建图与时序鲁棒性。** 论文未在真正长周期、环境动态变化的场景下系统评测。隐藏状态的更新策略（当前为每子地图重置）缺乏对时序变化的适应性——理想情况下，系统应在环境变化时选择性更新记忆，而非简单遗忘。TTT（Test‑Time Training）类方法的自适应学习率门控可能是一个方向，但需要专门的数据集和训练范式支持。

**零样本跨域泛化。** 训练数据覆盖ScanNet++、DL3DV等多个室内/外数据集，但模型在完全陌生场景（如极端光照、水下、医疗内窥）下的前馈预测质量未经验证。递归架构可能在这些域外场景产生累积误差，因为隐藏状态的更新缺乏对预测不确定性的校准机制。

**前馈位姿估计的长期鲁棒性。** 在大规模室外环境中，前馈模型能否完全取代传统BA尚不明确。当前系统依赖位姿图优化（PGO）融合闭环约束来全局校正轨迹，但前端位姿预测的局部精度仍是PGO收敛的基础。在GPS拒止、长距离无回环的室外场景，前馈位姿估计的累积漂移特性需要更深入的理论与实证分析。

### 4. 知识库定位：对后续工作的启示

Flash‑Mono 为单目稠密SLAM建立了一个新的基线范式，其知识贡献可归纳为三个可迁移的“因果旋钮”：

1. **递归隐藏状态作为紧凑子地图描述子**：这一设计将“记忆”从显式的地图存储抽象为隐式状态向量，使闭环重定位退化为单次前馈操作。后续工作可探索更高效的隐藏状态编码（如稀疏记忆token）和自适应更新规则。

2. **前馈预测+轻量微调的效率‑精度解耦**：通过将计算密集的高斯属性初始化从前端剥离并交由预训练模型完成，后端仅需极少量迭代即可收敛。这一范式可推广至其他神经场SLAM（如NeRF‑based SLAM），前提是预训练模型能提供足够好的初始化。

3. **自适应体素化的地图紧凑性控制**：在保证渲染质量的前提下将高斯原语数量减少58%以上（1.35M → 0.56M），为资源受限场景的地图存储与传输提供了实用方案。

需要指出的是，论文中部分基线的对比公平性存在注意事项：MonoGS在ScanNet 0054/0465和BundleFusion apt0因内存不足崩溃，指标仅基于崩溃前子序列；S3PO‑GS在KITTI 07运行失败。这些因素可能导致基线性能被高估，Flash‑Mono的实际优势可能比报告数值更大。

## 原文 PDF

![[paperPDFs/ICLR_2026/Flash_Mono_Feed_Forward_Accelerated_Gaussian_Splatting_Monocular_SLAM_774a8b41cda9.pdf]]
