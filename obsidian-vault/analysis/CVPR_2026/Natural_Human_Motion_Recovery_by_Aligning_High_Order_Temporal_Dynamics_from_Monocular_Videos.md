---
title: Natural Human Motion Recovery by Aligning High-Order Temporal Dynamics from Monocular Videos
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Natural_Human_Motion_Recovery_by_Aligning_High_Order_Temporal_Dynamics_from_Monocular_Videos.pdf
project_link: null
code_link: null
aliases:
- HR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 显式估计相机空间每关节的速度和加速度，并将其作为软约束纳入全局优化以强制执行高阶时间一致性。
primary_logic: 通过显式建模并施加速度和加速度一致性约束，可以在保持关节位置精度的前提下恢复自然、物理合理的人体运动动态。
claims:
- HTD-Refine consistently improves motion smoothness and global accuracy over most baselines on EMDB-2.
- Removing acceleration supervision increases jitter, indicating it is essential for motion continuity.
- Removing velocity supervision increases foot sliding, indicating it is essential for high-frequency stability.
- "Velocity and acceleration provide complementary constraints: velocity regulates phase-consistent motion, while acceleration stabilizes higher-order dynamics."
---

# Natural Human Motion Recovery by Aligning High-Order Temporal Dynamics from Monocular Videos

> [!tip] 核心洞察
> 通过显式建模并施加速度和加速度一致性约束，可以在保持关节位置精度的前提下恢复自然、物理合理的人体运动动态。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过对齐高阶时间动态从单目视频恢复自然人体运动 |
| 英文题名 | Natural Human Motion Recovery by Aligning High-Order Temporal Dynamics from Monocular Videos |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wei_Natural_Human_Motion_Recovery_by_Aligning_High-Order_Temporal_Dynamics_from_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | HTD-Refine |
| Dataset | EMDB-2, RICH |

> [!tip] 效果简介
> - EMDB-2 上，Jitter HTD-Refine (various base HMR methods) vs TRAM / GVHMR / WHAM / Human3R (Jitter 降低 58.1%–75.0%)；Foot Sliding (FS) HTD-Refine vs TRAM / Human3R (FS 降低 37.5%–61.3%)；Jitter (refinement comparison) HTD-Refine vs RoHM / trajectory filter (HTD-Refine 降低 93.1% vs RoHM 70.4% vs traj filter 73.9%)。
> - RICH 上，Jitter HTD-Refine vs TRAM (Jitter 降低 72.3%–77.5%)。

## 概要

**核心问题**：现有单目视频人体运动恢复（HMR）方法在关节位置精度上取得了显著进展，但普遍缺乏可靠的高阶时间线索——即速度和加速度信息。这导致重建的运动虽然逐帧看起来准确，却存在过度平滑或高频抖动，动态特性与真实运动不一致。

**核心思路**：HTD-Refine 通过显式估计并强制执行高阶时间一致性来解决这一问题。其核心是一个轻量级时序网络 PVA-Net，能够从单目视频中直接预测每关节的 2D 关键点位置、3D 速度和加速度。这些预测作为软约束，被纳入一个全局优化框架中，对现有 HMR 方法输出的初始运动进行精炼，从而在保持关节位置精度的前提下恢复自然、物理合理的人体运动动态。

**方法定位**：HTD-Refine 是一个**通用后处理框架**，可无缝接入现有的 HMR 管线（如 TRAM、GVHMR、WHAM、Human3R 等），无需修改基线模型的训练或推理过程。其设计理念是直接以动态保真度为目标，而非依赖隐式平滑先验或生成式先验。

**主要结果**：
- 在 **EMDB-2**（动态相机）基准上，HTD-Refine 将运动抖动（Jitter）降低 **58.1%–75.0%**，脚滑动（Foot Sliding）降低 **37.5%–61.3%**，同时改善了全局精度指标（WA-MPJPE、W-MPJPE、RTE）。
- 在 **RICH**（静态相机）基准上，抖动降低 **72.3%–77.5%**。
- 与精炼基线相比，HTD-Refine 的抖动降低幅度（93.1%）显著优于 RoHM（70.4%）和轨迹滤波（73.9%）。
- 消融实验证实，速度监督对高频稳定性至关重要（移除后脚滑动从 7.5 升至 8.8），加速度监督对运动连续性至关重要（移除后抖动从 6.6 升至 9.7），二者提供互补约束。

从单目视频中恢复自然的人体运动是计算机视觉的核心挑战之一，在虚拟现实、数字人驱动、运动分析等领域有广泛应用。近年来，基于学习的全局人体网格恢复方法取得了显著进展，代表性工作包括 **TRAM**（Wang et al., ECCV 2024）、**GVHMR**（Shen et al., SIGGRAPH Asia 2024）和 **WHAM**（Shin et al., CVPR 2024）等。这些方法通常以逐帧方式估计相机空间的人体姿态和相机外参，再将其变换到世界空间，在关节位置精度上表现良好。

然而，现有方法存在一个关键瓶颈：**它们缺乏对高阶时间动态（速度和加速度）的可靠建模**。由于逐帧估计忽略了帧间连续性约束，重建的运动往往表现出过度平滑或抖动伪影，即使关节位置的数值误差很小，运动的动态特性仍然不一致。Figure 1 直观地展示了这一问题——TRAM 在位置误差上表现良好，但其速度和加速度曲线与真实值存在明显偏差。

这一瓶颈的根源在于，单目视频本身缺乏显式的速度和加速度线索。现有方法要么完全忽略这些高阶信息，要么仅通过隐式的时间平滑（如轨迹滤波）来缓解抖动，但无法从根本上恢复物理合理的运动动态。扩散模型（如 **RoHM**, Zhang et al., CVPR 2024）和神经运动场（如 **NeMF**, He et al., NeurIPS 2022）等精炼方法虽然尝试改善运动质量，但它们主要关注姿态本身的合理性，并未显式约束速度和加速度的一致性。

本文的动机正是针对这一缺口：**如果能从视频中显式估计每关节的速度和加速度，并将其作为约束纳入全局优化，就有可能在保持关节位置精度的前提下，恢复自然、物理合理的人体运动动态。** 这一思路的核心洞察是：速度和加速度提供了互补的约束——速度调控相位一致的运动，加速度则稳定更高阶的动态，二者共同作用才能实现自然且物理可信的运动恢复。

## 核心方法与创新机理

### 问题瓶颈：高阶时间动态的缺失

现有单目视频人体运动恢复（HMR）方法（如 **TRAM** (Wang et al., ECCV 2024)、**GVHMR** (Shen et al., SIGGRAPH Asia 2024)、**WHAM** (Shin et al., CVPR 2024)）主要关注逐帧关节位置精度，却忽略了运动的高阶时间线索——即速度和加速度。这导致恢复的运动虽然关节位置数值准确，但在动态上表现出过度平滑或高频抖动，缺乏物理合理性和自然感（Figure 1）。

### 核心创新：显式高阶动力学约束

HTD-Refine 的核心创新在于**显式估计并强制执行相机空间的高阶时间动态一致性**。与传统方法依赖隐式平滑先验或生成式扩散先验不同，本方法直接建模每关节的 3D 速度和加速度，并将其作为软约束纳入全局优化。这一设计通过以下三个 changed slot 实现：

1.  **高阶动力学约束**：基线方法无显式速度和加速度约束。HTD-Refine 通过 **PVA-Net** 预测相机空间每关节的速度 $V_c^t$ 和加速度 $A_c^t$，并在全局优化能量函数中引入速度一致性项 $E_V$ 和加速度一致性项 $E_A$（Eq. 11–12），强制优化后的运动与预测的高阶动态一致。

2.  **2D 关键点时间一致性**：基线方法（如 ViTPose）逐帧独立检测 2D 关键点，缺乏时间约束。HTD-Refine 在 PVA-Net 中引入**时间梯度匹配损失 $L_{tgm}$**（Eq. 9），鼓励相邻帧热图的时间梯度一致，从而输出时间稳定的 2D 关键点序列，为后续优化提供更可靠的投影约束。

3.  **基于速度的脚部锁定**：基线方法无基于运动状态的脚部接触建模。HTD-Refine 利用 PVA-Net 预测的速度计算静止概率 $p_s = \max(0, 1 - \frac{\|\mathbf{V}^t\|}{\xi_v})$，并据此混合当前帧与下一帧关节位置作为逆运动学（IK）目标，有效减少脚滑动伪影。

### 因果机制

速度和加速度约束在优化中扮演互补角色（Table 3 消融实验）：

-   **速度监督**：约束运动的一阶相位一致性。移除速度监督后，脚滑动（FS）从 7.5 增至 8.8，表明速度对高频稳定性至关重要。
-   **加速度监督**：约束运动的二阶连续性。移除加速度监督后，抖动（Jitter）从 6.6 增至 9.7，表明加速度对运动连续性至关重要。

两者联合作用，使得优化后的运动在保持 2D 关键点投影精度的前提下，恢复自然、物理合理的高阶动态（Figure 1）。

HTD-Refine 是一种即插即用的后处理框架，通过对齐显式估计的高阶时间动态来精细化现有 HMR 管线恢复的全局人体运动。其核心思路是：现有方法在关节位置精度上表现良好，但缺乏对速度和加速度的可靠约束，导致运动过度平滑或高频抖动。HTD-Refine 直接针对这一瓶颈，引入显式的速度和加速度监督，在保持位置精度的前提下恢复自然、物理合理的运动动态。

### 三阶段流水线

如图 2 所示，HTD-Refine 由三个顺序阶段构成：

1. **初始化**：给定单目视频，首先利用现成的 HMR 模型（如 TRAM、GVHMR、WHAM 等）和相机位姿估计器，逐帧获取相机空间的人体姿态参数（SMPL 姿态 $\boldsymbol{\theta}_c$、平移 $\boldsymbol{\tau}_c$、朝向 $\Gamma_c$）及相机外参 $[\mathbf{R}_c^t|\mathbf{t}_c^t]$。随后通过坐标变换将相机空间运动转换到世界空间，得到初始的全局人体运动序列。

2. **速度与加速度估计（PVA-Net）**：将视频帧序列输入 PVA-Net，该网络联合预测每关节的 2D 关键点热图、相机空间 3D 速度 $\hat{V}_c^t$ 和加速度 $\hat{A}_c^t$。这些高阶运动线索为后续优化提供了显式的动态监督信号。

3. **运动优化**：从当前全局运动中提取相机空间的速度和加速度，与 PVA-Net 的预测值构建一致性损失；同时引入 2D 关键点重投影约束和 jerk 平滑项，通过全局优化迭代更新世界空间的姿态 $\boldsymbol{\theta}_w$、平移 $\boldsymbol{\tau}_w$ 和朝向 $\Gamma_w$，最终输出精细化后的自然人体运动。

### PVA-Net 的设计定位

PVA-Net 是整个框架的核心预测模块，其架构如图 3 所示：冻结的 ViTPose 编码器提取逐帧特征，经重塑后送入轻量级时序 Transformer 建模帧间依赖，三个解码头分别输出 2D 关键点、速度和加速度。训练时采用加权多任务损失：

$$L_{\mathrm{total}} = \alpha_H L_{\mathrm{H}} + \alpha_V L_{\mathrm{V}} + \alpha_A L_{\mathrm{A}} + \alpha_{tgm} L_{\mathrm{tgm}}$$

其中 $L_{\mathrm{H}}$ 为热图 MSE，$L_{\mathrm{V}}$ 和 $L_{\mathrm{A}}$ 分别为速度和加速度的 MSE，$L_{\mathrm{tgm}}$ 为时间梯度匹配损失，鼓励 2D 关键点在时间维度上梯度一致。

### 优化中的约束关系

全局优化能量函数将高阶动态约束与几何约束统一在一个框架内：

$$E(\theta_w, \boldsymbol{\tau}_w, \Gamma_w) = \lambda_V E_V + \lambda_A E_A + \lambda_K E_K + \lambda_{\mathrm{jerk}} E_{\mathrm{jerk}} + \lambda_{\mathrm{reg}} E_{\mathrm{reg}}$$

速度和加速度一致性项（$E_V$、$E_A$）直接匹配 PVA-Net 的预测值，分别约束一阶和二阶动态；2D 关键点项（$E_K$）保证投影一致性；jerk 平滑项（$E_{\mathrm{jerk}}$）对轨迹三阶差分施加惩罚以抑制残余高频抖动；正则化项（$E_{\mathrm{reg}}$）防止优化后的参数偏离初始估计过远。消融实验（Table 3）证实：移除加速度监督导致 Jitter 从 6.6 升至 9.7，移除速度监督导致 Foot Sliding 从 7.5 升至 8.8，表明速度和加速度提供了互补的约束——速度调节相位一致性，加速度稳定高阶动态连续性。

### 可选后处理：基于速度的脚部锁定

在优化完成后，可根据预测速度计算静止概率 $p_s = \max(0, 1 - \|\mathbf{V}^t\|/\xi_v)$，对脚部（及手部）应用逆运动学锁定，目标关节位置由当前帧与下一帧按 $p_s$ 混合得到。该步骤可进一步减少脚滑动，但可能将偏差传播到其他关节，因此设为可选。

![[assets/figures/papers/paper_list_l957_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Natural_Human_Moti/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the HTD-Refine pipeline. Given an input video, our method proceeds in three stages. (a) Initialization. We first apply an off-the-shelf human mesh recovery model [29, 39] and a camera pose estimator [36, 39] to obtain per-frame camera-space human pose and camera extrinsics, which are then transformed into world coordinates. (b) Velocity and acceleration estimation. In addition to predicting per-joint 2D keypoint positions, our PVA-Net also outputs camera-space 3D joint velocities and accelerations that serve as high-order motion cues. (c) Motion optimization. We extract velocities and accelerations from the current global motion, impose losses against the PVA-Net predictions, an...*

HTD-Refine 的核心由三个级联模块构成：**初始化**、**PVA-Net** 和**运动优化**。其设计哲学是“直接瞄准动态保真度，而非依赖隐式平滑或生成先验”。以下逐一剖析各模块的关键公式与变量含义。

### 3.1 初始化：世界空间运动构建

给定单目视频，首先利用现成的 HMR 模型（如 TRAM、GVHMR）和相机位姿估计器获取逐帧的**相机空间**人体姿态参数和相机外参，再将其变换到**世界空间**，为后续优化提供初始轨迹。

**世界空间根节点朝向**由相机外参旋转与相机空间根朝向组合得到：

$$\Gamma_w^t = \mathbf{R}_c^t \Gamma_c^t$$

其中 $\mathbf{R}_c^t$ 为第 $t$ 帧的相机旋转矩阵，$\Gamma_c^t$ 为相机空间 SMPL 根节点朝向。

**世界空间根节点平移**需考虑 SMPL 模型的根节点偏置 $\mathbf{t}_{\mathrm{root}}$：

$$\boldsymbol{\tau}_w^t = \mathbf{t}_c^t + \left( \mathbf{R}_c^t ( \boldsymbol{\tau}_c^t + \mathbf{t}_{\mathrm{root}} ) - \mathbf{t}_{\mathrm{root}} \right)$$

其中 $\mathbf{t}_c^t$ 为相机平移，$\boldsymbol{\tau}_c^t$ 为相机空间根节点平移。该变换确保了相机空间与世界空间运动在几何上的一致性。

### 3.2 PVA-Net：高阶动力学预测

PVA-Net 是方法的核心预测器，其架构如图 3 所示：冻结的 ViTPose 编码器提取逐帧特征，经轻量时序 Transformer 处理后，由三个解码头分别预测**每关节 2D 关键点热图**、**相机空间 3D 速度**和**相机空间 3D 加速度**。

**监督信号定义**。相机空间速度通过一阶有限差分计算：

$$V_c^t = \frac{\mathbf{J}_c^t - \mathbf{J}_c^{t-1}}{\Delta t}$$

相机空间加速度通过二阶有限差分近似：

$$A_c^t = \frac{\mathbf{J}_c^{t+1} - 2\mathbf{J}_c^t + \mathbf{J}_c^{t-1}}{(\Delta t)^2}$$

其中 $\mathbf{J}_c^t$ 为第 $t$ 帧相机空间的 3D 关节位置，$\Delta t$ 为帧间隔。二阶差分形式天然抑制低频漂移，为加速度预测提供稳定监督。

**训练损失**。PVA-Net 的总损失为四项加权和：

$$L_{\mathrm{total}} = \alpha_H L_{\mathrm{H}} + \alpha_V L_{\mathrm{V}} + \alpha_A L_{\mathrm{A}} + \alpha_{tgm} L_{\mathrm{tgm}}$$

各分量定义如下：

- **热图损失**（MSE）：

$$L_{\mathrm{H}} = \frac{1}{T} \sum_{t=1}^{T} \| \hat{H}^t - H^t \|^2$$

- **速度损失**（MSE）：

$$L_{\mathrm{V}} = \frac{1}{T-1} \sum_{t=2}^{T} \| \hat{V}_c^t - V_c^t \|^2$$

- **加速度损失**（MSE）：

$$L_{\mathrm{A}} = \frac{1}{T-2} \sum_{t=2}^{T-1} \| \hat{A}_c^t - A_c^t \|^2$$

- **时间梯度匹配损失**（Temporal Gradient Matching, $L_{\mathrm{tgm}}$）：鼓励 2D 关键点热图在时间维度上梯度一致，增强时序稳定性：

$$L_{\mathrm{tgm}} = \frac{1}{T-1} \sum_{t=2}^{T} \| (\hat{H}^t - \hat{H}^{t-1}) - (H^t - H^{t-1}) \|^2$$

其中 $\hat{H}^t$ 和 $H^t$ 分别为预测和真实热图。该损失不直接约束高阶动力学，但为 2D 关键点提供时间一致性先验。

### 3.3 运动优化：高阶约束下的全局精炼

获得 PVA-Net 预测的速度 $\hat{V}_c^t$ 和加速度 $\hat{A}_c^t$ 后，将其作为**软约束**纳入全局优化，通过最小化加权能量函数精炼世界空间运动参数 $(\theta_w, \boldsymbol{\tau}_w, \Gamma_w)$：

$$E(\theta_w, \boldsymbol{\tau}_w, \Gamma_w) = \lambda_V E_V + \lambda_A E_A + \lambda_K E_K + \lambda_{\mathrm{jerk}} E_{\mathrm{jerk}} + \lambda_{\mathrm{reg}} E_{\mathrm{reg}}$$

各能量项定义：

- **速度一致性项**：匹配当前运动的速度与 PVA-Net 预测：

$$E_V = \frac{1}{T-1} \sum_{t=2}^{T} \| \mathbf{V}_c^t - \hat{V}_c^t \|_2^2$$

- **加速度一致性项**：匹配当前运动的加速度与 PVA-Net 预测：

$$E_A = \frac{1}{T-2} \sum_{t=2}^{T-1} \| \mathbf{A}_c^t - \hat{A}_c^t \|_2^2$$

- **2D 关键点约束**：约束优化后的 3D 关节投影与 PVA-Net 预测的 2D 关键点一致：

$$E_K = \frac{1}{T} \sum_{t=1}^{T} \| \mathbf{K}^t - \hat{K}^t \|_2^2$$

- **Jerk 平滑项**：对关节轨迹的三阶差分施加正则化，抑制高频抖动：

$$E_{\mathrm{jerk}} = \frac{1}{T-3} \sum_{t=1}^{T-3} \| \mathbf{J}^{t+3} - 3\mathbf{J}^{t+2} + 3\mathbf{J}^{t+1} - \mathbf{J}^t \|_2^2$$

- **参数正则化项**：防止优化后的姿态、朝向和平移偏离初始估计过远：

$$E_{\mathrm{reg}} = \frac{1}{T} \sum_{t=1}^{T} \left( \| \boldsymbol{\theta}^t - \check{\boldsymbol{\theta}}^t \|_2^2 + \| \Gamma^t - \check{\Gamma}^t \|_2^2 + \| \boldsymbol{\tau}^t - \check{\boldsymbol{\tau}}^t \|_2^2 \right)$$

其中 $\check{\boldsymbol{\theta}}^t, \check{\Gamma}^t, \check{\boldsymbol{\tau}}^t$ 为初始化阶段获得的参数。

**速度与加速度的互补机制**是该方法的关键洞察：速度约束调节相位一致性运动（高频稳定），加速度约束抑制二阶漂移（运动连续性）。消融实验（Table 3）证实：移除加速度监督后 Jitter 从 6.6 升至 9.7，移除速度监督后 Foot Sliding 从 7.5 升至 8.8，二者缺一不可。

### 3.4 后处理：基于速度的脚部锁定（可选）

为进一步减少脚滑动，HTD-Refine 引入基于预测速度的逆运动学脚部锁定。给定速度阈值 $\xi_v = 0.1$，计算静止概率：

$$p_s = \max\left(0, 1 - \frac{\|\mathbf{V}^t\|}{\xi_v}\right)$$

随后混合当前帧与下一帧关节位置作为 IK 目标：

$$\hat{\mathbf{J}}^t = p_s \mathbf{J}^t + (1 - p_s) \mathbf{J}^{t+1}$$

该步骤作为可选后处理，可提升视觉质量，但可能将偏差传播到其他关节，故不作为默认配置。

## 实验与关键发现

### 实验设置与评估协议

实验在两个公开基准上评估：**EMDB-2**（动态相机）和 **RICH**（静态相机）。评估指标覆盖三个维度：

- **运动稳定性**：Jitter（三阶差分平滑度）和 Foot Sliding（FS，脚滑动）；
- **关节动力学**：相机空间平均每关节速度误差（MPJVE）和平均每关节加速度误差（MPJAE）；
- **全局精度**：世界空间平均每关节位置误差（WA-MPJPE、W-MPJPE）和根平移误差（RTE）。

所有基线均使用官方发布的模型和权重，HTD-Refine 作为后处理框架不重新训练任何基线模型。

### 主实验结果

#### EMDB-2 动态相机基准

Table 1 汇总了 HTD-Refine 与多个主流 HMR 方法的对比。核心结论：

![[assets/figures/papers/paper_list_l957_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Natural_Human_Moti/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison on the EMDB-2 [17] benchmark with moving cameras. We report global motion stability (Jitter, FS), joint dynamics (MPJVE, MPJAE), and global accuracy (WA-MPJPE, W-MPJPE, RTE) for different baselines and their variants with HTD-Refine. HTD-Refine consistently improves motion smoothness and global accuracy over most baselines*

**运动稳定性大幅提升。** 以 TRAM 为基线的 HTD-Refine 将 Jitter 降低 58.1%–75.0%，Foot Sliding 降低 37.5%–61.3%。对于 Human3R，FS 降幅达 61.3%。这表明显式高阶动力学约束能有效抑制单目重建中普遍存在的抖动和脚滑动伪影。

**关节动力学显著改善。** 相机空间 MPJVE 降低 33.3%–55.2%，MPJAE 降低 24.0%–72.5%。加速度误差的降幅尤为突出，验证了 PVA-Net 预测的加速度信号对恢复运动真实动态的关键作用。

**全局精度同步提升。** WA-MPJPE 降低 7.6%–41.7%，说明在增强时间一致性的同时，空间精度并未牺牲，反而因更合理的运动约束而受益。

#### RICH 静态相机基准

Table 2 展示了静态相机场景下的结果。HTD-Refine 在 TRAM 基线上将 Jitter 降低 72.3%–77.5%，Foot Sliding 降低 49.6%。MPJVE 和 MPJAE 分别降低 25.0%–33.3% 和 29.4%–41.4%，WA-MPJPE 降低 2.8%–12.9%。静态相机下 Jitter 降幅更大，说明高阶动力学约束对消除由相机位姿估计噪声引入的抖动同样有效。

![[assets/figures/papers/paper_list_l957_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Natural_Human_Moti/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison on the RICH [15] test set with static cameras. HTD-Refine consistently enhances the temporal quality of reconstructed motion, markedly reducing jitter artifacts*

#### 与精炼基线对比

Table 4 对比了 HTD-Refine 与专门的运动精炼方法。在 EMDB 上，HTD-Refine 将 Jitter 降低 93.1%，而 **RoHM**（Zhang et al., CVPR 2024）降低 70.4%，轨迹滤波降低 73.9%。Table 5 在 RICH 上与 **NeMF**（He et al., NeurIPS 2022）和 **PACE**（Kocabas et al., 3DV 2024）的对比进一步验证了显式高阶约束优于隐式平滑或生成先验。

![[assets/figures/papers/paper_list_l957_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Natural_Human_Moti/figures/008_Table_4.jpg]]
*Table 4: Comparison with refinement baselines on EMDB*

### 消融实验

Table 3 系统拆解了各模块的贡献：

![[assets/figures/papers/paper_list_l957_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Natural_Human_Moti/figures/007_Table_3.jpg]]
*Table 3: Ablation studies. We compare our method with five variants on the EMDB dataset [17]*

**加速度监督是运动连续性的关键。** 移除加速度监督（w/o Acc）后，Jitter 从 6.6 升至 9.7，证实二阶动力学信息对抑制高频抖动不可或缺。

**速度监督控制脚滑动。** 移除速度监督（w/o Vel）后，Foot Sliding 从 7.5 升至 8.8，说明速度一致性约束是维持脚-地接触稳定性的主要驱动力。

**速度与加速度提供互补约束。** 速度约束调节相位一致的运动节奏，加速度约束稳定更高阶的动力学变化。二者联合使用产生协同效应（Sec. 4.4）。

**时间梯度匹配损失的定位。** 移除 $L_{\mathrm{tgm}}$（w/o TGM）主要影响 2D 关键点的时间一致性，但对 Jitter 和 FS 的直接影响较小，说明其作用更多体现在投影层面的稳定性，而非动力学质量本身。

**脚部锁定的作用与局限。** 基于速度的静止概率脚部锁定（Sec. 3.3）可进一步提升视觉质量，但可能将 IK 偏差传播到其他关节，因此论文将其设为可选后处理步。消融中该模块的独立贡献需手动核实具体数值。

![[assets/figures/papers/paper_list_l957_https_openaccess_thecvf_com_content_CVPR2026_html_Wei_Natural_Human_Moti/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results on EMDB. Compared to TRAM [39], our method substantially reduces foot sliding and over-smoothing in world space, and preserves accurate camera-space poses that stay well aligned with the input video*

## 定位与知识库关联

### 单目全局人体运动恢复的基线谱系

HTD-Refine 定位为一个**通用后处理框架**，其设计目标是与现成的 HMR 流水线协同工作，而非替代它们。因此，理解其方法谱系需要同时考察它所增强的“上游”全局 HMR 方法，以及它所对标的“下游”运动精炼方法。

**上游全局 HMR 基线**（HTD-Refine 的初始化来源）可分为两类：

- **相机优先（camera-first）方法**：以 **TRAM**（Wang et al., ECCV 2024）为代表，先估计相机外参，再将相机空间人体运动变换到世界空间。这类方法在关节位置精度上表现优异，但其世界空间轨迹继承了相机估计的逐帧噪声，导致严重的高频抖动和脚滑动——这正是 Figure 1 和 Figure 4 所揭示的核心矛盾：TRAM 的位置误差低，但速度和加速度一致性差。
- **直接全局方法**：包括 **GVHMR**（Shen et al., SIGGRAPH Asia 2024）、**WHAM**（Shin et al., CVPR 2024）和 **Human3R**（Chen et al., arXiv 2025）。这些方法在统一坐标框架下直接回归世界空间运动，减少了对相机外参的依赖，但同样缺乏对高阶时间动态的显式约束，普遍存在过度平滑问题。

**下游运动精炼基线**（与 HTD-Refine 直接竞争的后处理方法）：

- **RoHM**（Zhang et al., CVPR 2024）：基于扩散模型的运动精炼方法，依赖生成式先验来修复运动伪影。在 EMDB 上，RoHM 将 Jitter 降低 70.4%，而 HTD-Refine 降低 93.1%（Table 4），表明显式动力学约束比隐式生成先验更有效。
- **NeMF**（He et al., NeurIPS 2022）：神经运动场精炼方法，在 RICH 上的对比同样显示 HTD-Refine 的优势（Table 5）。
- **PACE**（Kocabas et al., 3DV 2024）：联合人体与相机估计方法，但未引入高阶动力学监督。
- **轨迹滤波**：简单的后处理平滑方法，在 EMDB 上仅降低 Jitter 73.9%，且可能引入额外的位置误差。

### 核心差异：从隐式平滑到显式动力学约束

HTD-Refine 与上述所有基线的根本分歧在于**对“运动质量”的定义和控制方式**：

| 维度 | 基线方法 | HTD-Refine |
|------|---------|------------|
| **动力学建模** | 隐式平滑先验（如 jerk 正则）或生成式先验 | 显式估计并约束每关节速度和加速度 |
| **时间一致性** | 逐帧独立检测 2D 关键点（如 ViTPose） | PVA-Net 预测时间一致的 2D 关键点 + 时间梯度匹配损失 $L_{\mathrm{tgm}}$ |
| **脚滑动处理** | 无基于速度的锁定机制 | 基于预测速度的静止概率 $p_s = \max(0, 1 - \frac{\|\mathbf{V}^t\|}{\xi_v})$ 驱动 IK 脚部锁定 |
| **优化目标** | 主要关注位置精度 | 位置精度 + 速度一致性 $E_V$ + 加速度一致性 $E_A$ + jerk 平滑 $E_{\mathrm{jerk}}$ |

这种差异的因果机制在于：单目视频的运动模糊和遮挡使得逐帧位置估计本身是病态的，但**相邻帧之间的速度和加速度变化具有更强的物理约束性**。PVA-Net 直接学习从 RGB 序列到相机空间 3D 速度和加速度的映射，绕过了“先估计位置再差分”的误差放大路径（Eq. 3–4 的有限差分仅在真值计算中使用，推理时由网络直接预测）。

### 适用边界与局限

**已验证的有效范围**：

- **相机条件**：动态相机（EMDB-2）和静态相机（RICH）均有效，Jitter 分别降低 58.1%–75.0% 和 72.3%–77.5%（Table 1, Table 2）。
- **上游方法兼容性**：对 TRAM、GVHMR、WHAM、Human3R 四种不同架构的全局 HMR 方法均能一致提升运动平滑度和全局精度（Table 1），验证了其作为通用后处理框架的定位。
- **运动类型**：在 EMDB 和 RICH 的多样化日常动作上有效，但论文未在极端运动（如快速旋转、杂技）上验证。

**已知局限与开放问题**：

1. **脚部锁定的偏差传播**：消融实验（Table 3）表明，基于速度的脚部锁定后处理可提升视觉质量，但可能将偏差传播到其他关节，因此论文将其设为可选步骤。这暗示了硬约束（IK 锁定）与软约束（能量项）之间存在未解决的张力——如何在局部约束与全局一致性之间取得最优平衡，论文未给出系统答案。

2. **PVA-Net 的泛化边界**：PVA-Net 在包含真值速度和加速度的合成数据上训练，其对真实世界视频的域迁移鲁棒性未经验证。当输入视频的运动模式与训练分布显著偏离时，预测的速度和加速度质量是否会退化，论文未讨论。

3. **与物理约束的关系**：HTD-Refine 的速度和加速度约束是数据驱动的（匹配 PVA-Net 预测），而非物理驱动的（如牛顿力学或接触力约束）。在需要严格物理合理性的场景（如生物力学分析），该方法可能不足。

4. **计算开销**：全局优化需要多轮迭代，论文未报告推理时间，对于实时应用（如 VR/AR）的适用性需手动验证。

5. **多人场景**：论文仅讨论单人运动恢复，PVA-Net 的架构和优化框架如何扩展到多人交互场景是开放问题。

### 知识库定位

HTD-Refine 在人体运动恢复领域占据了**显式高阶动力学监督**这一此前未被充分探索的生态位。其核心贡献不是提出新的 HMR 架构，而是证明了一个可泛化的原则：**在优化层面显式强制执行速度和加速度一致性，可以在不牺牲位置精度的前提下恢复自然运动动态**。这一原则独立于具体的上游 HMR 方法选择，因此 HTD-Refine 更像是运动恢复流水线中的一个“动力学校准层”，而非传统意义上的独立方法。

在方法演进脉络中，HTD-Refine 桥接了**纯几何优化**（依赖 2D 关键点和正则项）与**纯生成式精炼**（依赖扩散或 VAE 先验）之间的空白，提供了一种更直接、更可解释的动力学增强路径。其消融实验（Table 3）进一步揭示了速度监督和加速度监督的互补角色：速度约束主要抑制脚滑动（FS 7.5→8.8），加速度约束主要抑制抖动（Jitter 6.6→9.7），二者共同构成了从低频到高频的完整动力学覆盖。

## 原文 PDF

![[paperPDFs/CVPR_2026/Natural_Human_Motion_Recovery_by_Aligning_High_Order_Temporal_Dynamics_from_Monocular_Videos.pdf]]
