---
title: "Ultra Diffusion Poser: Diffusion-Based Human Motion Tracking from Sparse Inertial Sensors and Ranging-based Between-sensor Distances"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Ultra_Diffusion_Poser_Diffusion_Based_Human_Motion_Tracking_from_Sparse_Inertial_Sensors_and_Ranging_based_Between_sensor_Distances.pdf
project_link: null
code_link: "https://github.com/eth-siplab/UltraDiffusionPoser"
aliases:
- UDPU
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 显式建模传感器间距离的几何约束——通过从 UWB 距离中重建 3D 传感器布局，并在扩散采样中强制预测姿态与观测距离一致——可以显著提升姿态估计的准确性和物理合理性。
primary_logic: 利用多维尺度分析从 UWB 距离中解析重建 3D 传感器位置，作为扩散模型的强几何先验条件；同时在扩散采样过程中引入前向运动学计算预测距离，通过梯度引导将姿态修正至满足观测距离约束，从而在不依赖外部物理优化器的情况下产生平滑、高保真的运动估计。
claims:
- UDP 通过 Spatial Layout Module 和 UWB-Diffusion Guidance 显式建模几何约束，在所有评估设置中均取得 SOTA 性能，关节位置误差最多降低 22%。
- Spatial Layout Module 利用 MDS 从 UWB 距离中封闭形式恢复 3D 传感器布局，并经可学习的 Rotation Estimator 定向，提供强姿态先验。
- UWB-Diffusion Guidance 在扩散采样中内联前向运动学，将预测传感器间距离与测量值的偏差作为引导信号，有效纠正违反距离约束的预测。
- 消融实验表明，同时移除 Spatial Layout Module 和 UWB-Diffusion Guidance 使 JPE 增加 17%；单独应用 UWB-Diffusion Guidance 可降低 SIP 5% 和 JPE 7%。
---

# Ultra Diffusion Poser: Diffusion-Based Human Motion Tracking from Sparse Inertial Sensors and Ranging-based Between-sensor Distances

> [!tip] 核心洞察
> 利用多维尺度分析从 UWB 距离中解析重建 3D 传感器位置，作为扩散模型的强几何先验条件；同时在扩散采样过程中引入前向运动学计算预测距离，通过梯度引导将姿态修正至满足观测距离约束，从而在不依赖外部物理优化器的情况下产生平滑、高保真的运动估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | Ultra Diffusion Poser: 基于扩散模型的稀疏惯性传感器与UWB测距人体运动跟踪 |
| 英文题名 | Ultra Diffusion Poser: Diffusion-Based Human Motion Tracking from Sparse Inertial Sensors and Ranging-based Between-sensor Distances |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Hollidt_Ultra_Diffusion_Poser_Diffusion-Based_Human_Motion_Tracking_from_Sparse_Inertial_CVPR_2026_paper.html) · [Code](https://github.com/eth-siplab/UltraDiffusionPoser) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Ultra Diffusion Poser (UDP) |
| Dataset | DIP-IMU, DanceDB, TotalCapture, UIP-DB |

> [!tip] 效果简介
> - DIP-IMU 上，SIP (°) / GAE (°) / JPE (cm) / Jitter (m/s³) 10.39 / 8.19 / 3.42 / 0.125 vs UIP (best prior IMU+UWB) (JPE 相对 UIP 降低 ~22%)。
> - DanceDB 上，JPE (cm) / GAE (°) 4.67 / 9.91 vs UIP (JPE 显著优于 UIP)。
> - TotalCapture 上，SIP (°) / GAE (°) / JPE (cm) 8.95 / 10.19 / 3.76 vs UIP (各项指标均优于 UIP)。

## 概要

传统基于惯性传感器（IMU）的人体运动捕捉方法在长时间运行中面临严重的漂移问题，而引入超宽带（UWB）测距虽能提供传感器间的绝对距离信息，但现有工作仅将 UWB 距离作为辅助输入特征，忽略了这些距离对传感器位置的物理几何约束，导致预测的 3D 姿态可能违反测量的传感器间距离，限制了姿态精度和平滑性。

针对这一瓶颈，本文提出 **Ultra Diffusion Poser (UDP)**，其核心思路是显式建模传感器间距离的几何约束：一方面通过多维尺度分析（MDS）从 UWB 距离中封闭式重建 3D 传感器布局，作为扩散模型的强几何先验条件；另一方面在扩散采样过程中引入前向运动学计算预测距离，通过梯度引导将姿态修正至满足观测距离约束，从而在不依赖外部物理优化器的情况下产生平滑、高保真的运动估计。

在方法定位上，UDP 属于自回归扩散修复模型，区别于主流基于 RNN/Transformer 的回归网络或混合物理优化框架。其关键创新在于将 UWB 距离的利用方式从“辅助特征”升级为“显式几何约束建模”，并通过 Spatial Layout Module 和 UWB-Diffusion Guidance 两个模块实现。

实验结果表明，UDP 在 DIP-IMU、DanceDB、TotalCapture 等多个数据集上均取得 SOTA 性能，关节位置误差（JPE）相对最优 IMU+UWB 基线最多降低 22%。消融研究进一步验证了显式几何建模的必要性：同时移除 Spatial Layout Module 和 UWB-Diffusion Guidance 会使 JPE 增加 17%，而单独应用 UWB-Diffusion Guidance 可降低 SIP 误差 5%、JPE 7%。



### 可穿戴人体运动捕捉的传感器融合瓶颈

基于惯性测量单元（IMU）的可穿戴运动捕捉系统因其不受光照、遮挡限制的户外可用性，已成为视觉动捕的重要替代方案。然而，纯 IMU 方案面临两大根本性挑战：**全局漂移**导致长时间定位误差累积，以及**下肢运动模糊**使得腿部姿态难以可靠推断。为缓解这些问题，近年工作引入超宽带（UWB）测距作为补充模态——通过在身体关键点部署 UWB 模块，可实时获取传感器对之间的物理距离测量。

但现有 IMU+UWB 方法（如 **UIP**、**UMotion**（Liu et al., CVPR 2025）、**GIP**（Xue et al., ICCV 2025））存在一个共同的结构性缺陷：**它们仅将 UWB 距离作为网络的辅助输入特征**（通过 GCN 或直接拼接），而完全忽略了这些距离对传感器位置的物理几何约束。这意味着，即使网络预测的 3D 姿态在运动学上合理，其对应的传感器间距离可能与实际测量值严重不符——网络从未被要求“遵守”它所接收的距离信息。

### 缺失的几何先验

这一缺陷的深层原因在于，从稀疏 IMU 信号到全身姿态的映射是高度欠定的——同一个 IMU 读数可以对应多种不同的肢体构型。UWB 距离本应提供强有力的几何约束来缩小解空间：给定 6 个传感器之间的 15 对距离测量，3D 传感器布局在刚体变换意义下是唯一确定的。然而，现有方法并未显式地利用这一结构——它们既不从距离中重建传感器位置，也不在预测中强制距离一致性，导致模型学习的映射缺乏物理基础。

### 扩散模型的机遇与挑战

扩散模型在人体运动生成中展现了生成平滑、多样运动的能力，**DiffusionPoser**（Van Wouwe et al., CVPR 2024）已将其应用于纯 IMU 姿态估计。扩散框架的一个关键优势在于其迭代采样过程天然支持**引导**——可在采样时注入额外的约束信号来修正预测。这为在推理阶段强制距离约束提供了独特的机制。然而，现有扩散方法仍未将 UWB 几何约束结构性地融入模型架构。

### 本文动机

上述分析指向一个明确的研究缺口：**如何将 UWB 距离从被动的输入特征升级为主动的几何约束，使其在模型结构和推理过程中都发挥物理引导作用？** 本文提出的 **Ultra Diffusion Poser (UDP)** 正是针对这一缺口设计：通过多维尺度分析（MDS）从距离中封闭形式地重建 3D 传感器布局，将其作为扩散模型的显式空间条件；同时在扩散采样中引入基于前向运动学的距离一致性引导，使预测姿态始终满足观测约束。这一设计使得 UDP 无需依赖外部物理优化器即可产生平滑、高保真的运动估计，在多个基准上将关节位置误差最多降低 22%。



## 核心方法与创新机理

Ultra Diffusion Poser (UDP) 的核心创新在于**将 UWB 传感器间距离从“辅助输入特征”提升为“显式几何约束”**，从根本上改变了 IMU+UWB 融合的范式。传统方法（如 UIP、UMotion）仅将 UWB 距离作为附加特征通过 GCN 或拼接输入网络，完全忽略了这些距离对传感器位置的物理几何约束——预测的 3D 姿态可能违反测量的传感器间距离，导致姿态精度和平滑性受限。UDP 通过两个紧密协同的模块化设计填补了这一空白：

### 创新一：从距离到 3D 布局的几何先验重建（Spatial Layout Module）

UDP 的 Spatial Layout Module 首次将**多维尺度分析（MDS）**引入 IMU+UWB 姿态估计管线，从成对 UWB 距离矩阵中以封闭形式恢复 3D 传感器布局。具体而言，该模块对距离矩阵执行双中心化构造 Gram 矩阵 $\mathbf{B}$，通过 SVD 分解取前三个特征向量获得无向的 3D 传感器坐标 $\mathbf{X}_{\mathrm{MDS}}$。随后，一个可学习的 Rotation Estimator（3 层 LSTM）以 IMU 信号和归一化后的 MDS 布局为输入，预测旋转矩阵 $R_{\mathrm{MDS}}$ 和位置残差 $P_{\mathrm{res}}$，生成有向且精化的传感器位置 $P_{\mathrm{SPL}}$，作为扩散模型的条件输入。

这一设计的因果机制在于：**MDS 将距离约束转化为空间坐标，为扩散模型提供了强几何先验**——网络不再需要从原始距离中隐式推断传感器相对位置，而是直接获得物理上一致的 3D 布局作为条件。消融实验证实，移除 Rotation Estimator 仅使用未定向的 MDS 布局会降低性能，验证了定向模块对恢复真实传感器方位的关键作用。

### 创新二：扩散采样中的内联几何引导（UWB-Diffusion Guidance）

UDP 在扩散采样过程中引入 **UWB-Diffusion Guidance**，通过前向运动学（FK）计算当前预测姿态对应的传感器间距离 $\hat{d}_{ij}$，并与测量距离 $d_{ij}$ 比较，将偏差作为引导梯度：

$$\epsilon_{uwb} = \sum_{i < j} \| \hat{d}_{ij}(\hat{\mathcal{M}}_0) - d_{ij} \|^2$$

该引导信号在每一步去噪采样中修正预测姿态，使其满足观测距离约束。与依赖外部物理优化器的方法（如 PIP、PNP、GlobalPose）不同，UDP 将几何约束**内联到扩散模型的生成过程中**，无需额外的后处理优化步骤即可产生物理一致的平滑运动。

### 创新三：自回归扩散修复架构

UDP 采用**自回归扩散修复模型（autoregressive diffusion inpainting）**作为运动估计主干，以历史运动帧 $\mathcal{M}_{\mathrm{hist}}$ 和当前条件信号 $\pmb{\mathcal{C}}$ 为输入，通过迭代去噪预测当前干净运动。相较于主流的回归网络（RNN/Transformer）或混合物理优化框架，扩散模型天然具备捕捉多模态运动分布的能力，而自回归机制确保了帧间运动的平滑连续性。在训练目标上，UDP 采用简化的扩散损失配合平移、SMPL 角度和速度辅助损失，无需传统方法中常见的前向运动学损失，加快了训练收敛。

### 协同效应与量化验证

上述三个创新形成闭环：Spatial Layout Module 提供几何先验条件，自回归扩散修复模型生成平滑运动，UWB-Diffusion Guidance 在采样中强制执行距离约束。消融实验清晰揭示了各模块的贡献——同时移除 Spatial Layout Module 和 UWB-Diffusion Guidance 导致 JPE 增加 17%；单独应用 UWB-Diffusion Guidance 可使 SIP 降低 5%、JPE 降低 7%，表明扩散引导能有效纠正违反距离约束的预测。这一“重建—条件—引导”的几何约束闭环，使 UDP 在所有评估基准上均取得 SOTA 性能，关节位置误差相对最佳 IMU+UWB 基线 UIP 最多降低 22%。



Ultra Diffusion Poser (UDP) 是一个端到端可学习的自回归扩散修复模型，其核心设计在于将 UWB 传感器间距离从传统的辅助特征升级为显式几何约束的载体。整体映射关系为：

$$( \Theta , {\bf T} ) = \mathrm { UDP } ( {\bf R} , {\bf A} , {\bf D} , \beta )$$

其中 ${\bf R}$ 为传感器方向，${\bf A}$ 为加速度，${\bf D}$ 为 UWB 测距矩阵，$\beta$ 为 SMPL 体形参数。模型输出 $N$ 帧的 6D 关节旋转 $\Theta^{6D}$ 和全局平移 ${\bf T}$，拼接为运动表示 $\mathcal{M} \in \mathbb{R}^{N \times 147}$。

**Pipeline 由三大核心模块串联构成：**

1. **Spatial Layout Module (SPL)**：接收 UWB 距离矩阵 ${\bf D}$，通过 metric MDS 在闭式解中重建无向的 3D 传感器布局，再经 Rotation Estimator（3 层 LSTM）学习旋转矩阵和位置残差，输出有向的传感器位置 $P_{SPL}$ 及其镜像 $\bar{P}_{SPL}$。这一布局作为强几何先验条件注入扩散模型。

2. **Autoregressive Diffusion Inpainting Model**：以条件张量 $\pmb{\mathcal{C}} \in \mathbb{R}^{N \times 154}$（包含 $P_{SPL}$、$\bar{P}_{SPL}$、${\bf R}$、${\bf A}$、${\bf D}$、$\beta$）和历史运动帧为输入，采用 DDPM 框架迭代去噪预测当前干净运动。自回归机制利用已预测的历史帧确保运动平滑性。

3. **UWB-Diffusion Guidance**：在扩散采样过程中，通过前向运动学从当前预测姿态计算传感器间距离 $\hat{d}_{ij}$，与测量距离 $d_{ij}$ 比较形成引导损失 $\epsilon_{uwb} = \sum_{i<j} \| \hat{d}_{ij} - d_{ij} \|^2$，以梯度信号修正采样方向，强制预测姿态满足观测距离约束。

**数据流**：UWB 距离 → SPL 模块（MDS 重建 + Rotation Estimator 定向）→ 3D 传感器布局 → 条件张量 → 扩散去噪器（结合历史运动）→ 初步姿态预测 → UWB-Diffusion Guidance（FK 距离校验与梯度引导）→ 最终姿态输出。整个过程无需外部物理优化器即可产生平滑、高保真的运动估计。

Figure 1 展示了方法概览，Figure 2 详细描绘了模块间的交互关系。

![[assets/figures/papers/paper_list_l1004_https_openaccess_thecvf_com_content_CVPR2026_html_Hollidt_Ultra_Diffusio/figures/001_Figure_1.jpg]]
*Figure 1: Our method UDP improves wearable IMU+UWB pose estimation by extending UWB as an auxiliary feature to actively model its geometric constraints. The Spatial Layout Module reconstructs 3D sensor positions from UWB measurements, providing a physically-informed input that conditions a diffusion model to predict SMPL poses. UWB-Diffusion Guidance encourages alignment between predicted poses and measured distances during diffusion sampling, improving accuracy and producing consistent motions*



### 3.1 问题建模与运动表示

UDP 的整体映射定义为：

$$( \Theta , {\bf T} ) = \mathrm { UDP } ( {\bf R} , {\bf A} , {\bf D} , \beta )$$

其中 ${\bf R}$ 为传感器方向序列，${\bf A}$ 为加速度序列，${\bf D}$ 为传感器间 UWB 测距矩阵，$\beta$ 为 SMPL 体形参数。输出 $\Theta$ 为关节旋转，${\bf T}$ 为全局平移。

运动序列以 $N$ 帧窗口表示，每帧包含 6D 关节方向和平移：

$$\mathcal { M } \in \mathbb { R } ^ { N \times 147 } = [ \Theta ^ { 6D } , {\bf T} ]$$

扩散模型的条件张量整合了空间布局模块恢复的 3D 传感器位置、IMU 信号、UWB 距离和体形：

$$\pmb { \mathcal { C } } \in \mathbb { R } ^ { N \times 154 } = [ P _ { SPL } , \bar { P } _ { SPL } , \mathbf { R } , \mathbf { A } , \mathbf { D } , \beta ]$$

---

### 3.2 Spatial Layout Module (SPL)

SPL 模块是 UDP 的核心创新之一，它从 UWB 距离矩阵中显式重建 3D 传感器布局，为扩散模型提供强几何先验。该模块包含两个子步骤：**经典多维尺度分析 (MDS)** 和 **可学习旋转估计器**。

#### 3.2.1 MDS 重建无向布局

给定 $k$ 个传感器间的成对距离矩阵 ${\bf D}$，MDS 的目标是寻找一组 3D 点坐标，使其欧氏距离尽可能匹配测量值：

$$\underset { \mathbf { X } _ { \mathrm { MDS } } \in \mathbb { R } ^ { k \times 3 } } { \mathrm { argmin } } \sum _ { i < j } \left( | x _ { i } - x _ { j } | ^ { 2 } - d _ { i j } \right) ^ { 2 }$$

该优化问题可通过以下封闭形式求解。首先构造双中心化矩阵 $\mathbf{H}$，将平方距离矩阵 $\mathbf{D}^{(2)}$ 转化为 Gram 矩阵 $\mathbf{B}$：

$$\mathbf { H } = \mathbf { I } - \frac {1}{k} \mathbf { 1 1 } ^ { \top } , \quad \mathbf { B } = - \frac {1}{2} \mathbf { H } \mathbf { D } ^ { (2) } \mathbf { H }$$

对 $\mathbf{B}$ 进行奇异值分解：

$$\mathbf { B } = \mathbf { U } \pmb { \Sigma } \mathbf { V } ^ { \top }$$

取前 3 个最大特征值及其对应特征向量，恢复 3D 传感器坐标：

$$\mathbf { X } _ { \mathrm { MDS } } = \mathbf { U } _ { 3 } \mathbf { \Sigma } _ { 3 } ^ { 1/2 }$$

由于 MDS 恢复的布局是无向的（存在镜像歧义），需要后续模块确定其空间朝向。

#### 3.2.2 Rotation Estimator 定向与精化

Rotation Estimator 是一个 3 层 LSTM，输入归一化后的 MDS 布局 $\mathbf{X}$、其镜像版本 $\bar{\mathbf{X}}$ 以及 IMU/UWB 信号，输出旋转矩阵和位置残差：

$$R _ { MDS } , P _ { res } = \mathrm { RotEstimator } ( X , \bar { X } , {\bf R} , {\bf A} , {\bf D} )$$

最终的有向 3D 传感器布局及其镜像版本为：

$$P _ { SPL } = R _ { MDS } X + P _ { res } , \quad \bar { P } _ { SPL } = R _ { MDS } \bar { X } + P _ { res }$$

残差项 $P_{res}$ 用于补偿传感器噪声导致的 MDS 重建不准确性。该布局直接作为扩散模型的条件输入，提供了物理上可解释的传感器空间关系。

---

### 3.3 Autoregressive Diffusion Inpainting Model

UDP 采用自回归扩散修复框架：以历史运动帧 $\mathcal{M}_{hist}$ 和当前条件张量 $\pmb{\mathcal{C}}$ 为输入，通过迭代去噪预测当前干净运动。去噪网络 $D_\theta$ 基于 LSTM，在任意噪声步 $t$ 预测干净运动：

$$\hat { \mathcal { M } } _ { 0 } = D _ { \theta } ( \mathcal { M } _ { t } , \mathcal { M } _ { hist } , \pmb { c } , t )$$

训练采用简化扩散损失，配合三个辅助损失项。简化扩散损失为 DDPM 标准形式：

$${ \mathcal { L } } _ { \mathrm { simple } } = \mathbb { E } _ { q ( x _ { t } \mid x _ { 0 } ) } \left[ \| x _ { 0 } - D _ { \theta } ( x _ { t } , t , \pmb { \mathcal { C } } ) \| _ { 2 } ^ { 2 } \right]$$

辅助损失包括：全局平移 L2 损失 $\mathcal{L}_{tran}$、SMPL 关节角度 L1 损失 $\mathcal{L}_{smpl}$，以及速度一致性损失 $\mathcal{L}_{vel}$：

$$\mathcal { L } _ { tran } = \| \mathbf { T } ^ { pred } - \mathbf { T } ^ { gt } \| _ { 2 }$$

$$\mathcal { L } _ { smpl } = | \Theta _ {6d} ^ { pred } - \Theta _ {6d} ^ { gt } |$$

$$\mathcal { L } _ { vel } = \left( \Vert \mathbf { T } _ { n } ^ { pred } - \mathbf { T } _ { n-1 } ^ { pred } \Vert _ { 2 } - \Vert \mathbf { T } _ { n } ^ { gt } - \mathbf { T } _ { n-1 } ^ { gt } \Vert _ { 2 } \right) ^ { 2 }$$

值得注意的是，UDP 训练中**不包含**前向运动学（FK）损失，这加快了训练速度，而几何一致性由 UWB-Diffusion Guidance 在采样阶段保证。

---

### 3.4 UWB-Diffusion Guidance

在扩散采样过程中，UDP 引入基于前向运动学的引导机制，强制预测姿态与测量距离一致。具体地，在每一步去噪后，通过前向运动学从预测姿态 $\hat{\mathcal{M}}_0$ 计算传感器间距离 $\hat{d}_{ij}$，并与测量距离 $d_{ij}$ 比较，构造引导损失：

$$\epsilon _ { uwb } = \sum _ { i < j } \| \hat { d } _ { i j } ( \hat { \mathcal { M } } _ { 0 } ) - d _ { i j } \| ^ { 2 }$$

该损失的梯度用于修正扩散采样方向，使生成的姿态满足观测距离约束。这一机制无需外部物理优化器，内嵌于扩散迭代中，是 UDP 实现平滑、物理一致运动的关键。消融实验表明，单独应用 UWB-Diffusion Guidance 可使 SIP 误差降低 5%，JPE 降低 7%。

### 补充图表

![[assets/figures/papers/paper_list_l1004_https_openaccess_thecvf_com_content_CVPR2026_html_Hollidt_Ultra_Diffusio/figures/002_Figure_2.jpg]]
*Figure 2: The Spatial Layout Module applies metric MDS to the pairwise distance matrix D to recover initial sensor positions, which are then oriented by a learnable Rotation Estimator. The resulting 3D sensor layout provides a strong conditioning signal for the diffusion model. The autoregressive diffusion inpainting model extends the previously predicted motion based on the current conditioning signal to ensure smooth motion prediction. UWB-Diffusion Guidance steers the pose predictions to align with the measured inter-sensor distances*



## 实验与关键发现

### 核心性能验证

UDP 在多个基准数据集上均取得 SOTA 性能，验证了显式几何约束建模的有效性。在 DIP-IMU 数据集上（Table 1），UDP 的关节位置误差（JPE）为 3.42 cm，相比此前最佳的 IMU+UWB 方法 UIP 降低约 22%，全局角度误差（GAE）为 8.19°，姿态平滑度指标 Jitter 仅为 0.125 m/s³，远低于 UIP 的 0.351 m/s³。值得注意的是，UDP 在不依赖外部物理优化器（如 PIP、PNP 使用的物理仿真）的情况下，实现了更低的 Jitter 值，表明扩散模型的自回归修复机制本身即能产生时序平滑的运动估计。

![[assets/figures/papers/paper_list_l1004_https_openaccess_thecvf_com_content_CVPR2026_html_Hollidt_Ultra_Diffusio/figures/003_Table_1.jpg]]
*Table 1: Results on DIP-IMU. ”*” denotes the results we reproduced, because they were not provided in the original paper. ”†” denotes results that we reproduced, because the paper used a different evaluation framework. GT Jitter is 1.830*

在 DanceDB 和 TotalCapture 数据集上（Table 2），UDP 同样保持领先。DanceDB 上 JPE 为 4.67 cm，GAE 为 9.91°；TotalCapture 上 SIP 为 8.95°，GAE 为 10.19°，JPE 为 3.76 cm，各项指标均优于 UIP。在 UIP-DB 上，UDP 微调后 JPE 为 6.68 cm，相比 UIP 微调版本改善约 22%；在 GIP-DB 上，UDP 的 SIP 为 15.33°，低于多人物方法 GIP（Xue et al., ICCV 2025），JPE 为 6.68 cm，显著优于 UIP。相比纯 IMU 方法（如 DIP、TIP、TransPose），UDP 的 JPE 改善幅度最高可达 35%，充分体现了 UWB 距离信息对提升空间定位精度的价值。

![[assets/figures/papers/paper_list_l1004_https_openaccess_thecvf_com_content_CVPR2026_html_Hollidt_Ultra_Diffusio/figures/004_Table_2.jpg]]
*Table 2: Combined colored results on DanceDB (blue), TotalCapture (green), and UIP-DB (orange). “*” denotes values we reproduced because they were not reported in the original papers. ”†” denotes results that we reproduced because the paper used a different evaluation framework. Ground Truth Jitter: DanceDB: 2.09, TotalCapture: 0.465, UIP-DB: 0.850, GIP-DB: 0.113. Bold indicates best*

### 几何约束建模的消融分析

Table 4 的消融实验揭示了各模块的独立贡献。同时移除 Spatial Layout Module 和 UWB-Diffusion Guidance 后，JPE 增加 17%，证实显式几何建模是 UDP 性能增益的核心来源。单独应用 UWB-Diffusion Guidance 可使 SIP 误差降低 5%、JPE 降低 7%，说明扩散采样中的距离引导能有效修正违反物理约束的预测姿态。移除 Rotation Estimator 而仅使用未定向的 MDS 布局会降低性能，证明可学习的定向模块对提供有效空间先验至关重要。

![[assets/figures/papers/paper_list_l1004_https_openaccess_thecvf_com_content_CVPR2026_html_Hollidt_Ultra_Diffusio/figures/005_Table_4.jpg]]
*Table 4: Ablation Studies on TotalCapture*

这些结果共同表明：Spatial Layout Module 为扩散模型提供了强几何先验条件，而 UWB-Diffusion Guidance 在采样过程中进一步强制预测姿态与观测距离一致，二者协同工作，缺一不可。

### 噪声鲁棒性

Table 3 展示了 UDP 在不同 UWB 噪声水平下相对 UIP 的性能提升。在 0% 噪声（即真实 UWB 距离）条件下，UDP 的 GAE 和 JPE 分别比 UIP 改善 4.59° 和 1.40 cm。随着噪声比例增加（通过线性插值在真实测量与真值距离之间模拟），改善幅度逐渐缩小，但 UDP 在所有噪声水平下均保持优势。这表明 MDS 重建和扩散引导对传感器噪声具有一定容忍度，但在极高噪声或多路径干扰场景下，几何约束的精度可能下降，需要手动验证实际部署中的性能边界。

![[assets/figures/papers/paper_list_l1004_https_openaccess_thecvf_com_content_CVPR2026_html_Hollidt_Ultra_Diffusio/figures/006_Table_3.jpg]]
*Table 3: Improvement of UDP over UIP across different UWB noise levels, non-finetuned. The UWB distances are linearly interpolated between real and ground-truth measurements*

### 定性分析

Figure 3 的定性对比以红色热力图展示位置误差分布。UDP 在 DanceDB 和 TotalCapture 上均产生一致的准确姿态，误差区域显著小于对比方法，尤其在快速运动或自遮挡场景下仍能保持较低的关节位置偏差。这得益于自回归扩散修复模型利用历史运动帧进行平滑预测，以及 UWB-Diffusion Guidance 对距离约束的持续校正。

![[assets/figures/papers/paper_list_l1004_https_openaccess_thecvf_com_content_CVPR2026_html_Hollidt_Ultra_Diffusio/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative Results of UDP from DanceDB and Total-Capture. A brighter red indicates a higher position error. UDP consistently produces accurate poses*

### 局限性与失败模式

尽管 UDP 在标准基准上表现优异，仍需注意以下边界情况：
- **高噪声场景**：当 UWB 距离受到严重多路径干扰时，MDS 重建的 3D 传感器布局精度下降，可能导致 UWB-Diffusion Guidance 引导方向偏差，需要手动验证在真实传感器噪声分布下的鲁棒性。
- **传感器配置泛化**：当前系统限定为六个固定位置的传感器布局（头、骨盆、手腕、膝盖），尚未验证在更少或任意位置传感器配置下的泛化能力。
- **计算延迟**：扩散模型的迭代采样过程可能引入较高延迟，论文未提供在低功耗设备上的实时性分析，实际部署时需评估推理速度是否满足实时需求。
- **训练数据偏差**：模型在现有 MoCap 数据集生成的合成 IMU/UWB 数据上训练，真实场景中的传感器噪声分布差异可能影响精度，需要在实际硬件平台上进一步验证。



## 定位与知识库关联

### 1. 方法谱系：从 IMU 位姿估计到几何约束驱动的扩散模型

UDP 的核心贡献在于首次将 UWB 测距从“辅助输入特征”升级为“显式几何约束”，从而在可穿戴人体运动跟踪的方法谱系中开辟了新的技术路径。为理解这一跃迁的意义，需将其置于以下三条技术脉络的交汇处：

**（1）纯 IMU 位姿估计的演进。** 早期工作如 **DIP**（Huang et al., TOG 2018）采用 RNN 直接从 6 个 IMU 的旋转和加速度回归 SMPL 姿态，奠定了稀疏传感器全身姿态估计的基础。后续方法通过引入 Transformer 架构（**TIP**, Jiang et al., SIGGRAPH Asia 2022）或更精细的运动学约束（**DynaIP**, Zhang et al., CVPR 2024）逐步提升精度，但纯 IMU 方法始终面临一个根本性瓶颈：缺乏传感器间相对位置信息，导致全局平移漂移和肢体间相对位置的不确定性。

**（2）物理优化混合方法的引入。** 为缓解上述瓶颈，**PIP**（Yi et al., CVPR 2022）、**PNP**（Yi et al., SIGGRAPH 2024）和 **GlobalPose**（Yi et al., TOG 2025）等工作在神经网络预测后附加物理优化器，利用关节力矩最小化或接触力约束来修正姿态。这些方法有效提升了物理合理性，但依赖外部优化器增加了计算复杂度，且物理约束本身无法直接解决传感器间相对位置的模糊性。

**（3）IMU+UWB 融合方法的兴起。** 近年来，UWB 测距被引入以弥补传感器间位置信息的缺失。**UIP** 和 **UMotion**（Liu et al., CVPR 2025）将 UWB 距离作为 GCN 或拼接输入特征，**GIP**（Xue et al., ICCV 2025）进一步扩展到多人场景。然而，这些方法仍将 UWB 距离视为“黑箱”特征，忽略了其蕴含的物理几何约束——即任意两点间的距离必须满足三维欧氏空间的三角不等式和刚性约束。UDP 正是针对这一被忽视的瓶颈，将 UWB 距离从辅助特征提升为显式几何先验。

**（4）扩散模型在运动生成中的应用。** **DiffusionPoser**（Van Wouwe et al., CVPR 2024）首次将扩散模型用于 IMU 位姿估计，证明了去噪扩散概率模型在运动修复和生成中的潜力。UDP 继承了这一架构范式，但通过引入自回归修复机制和 UWB 引导采样，将扩散模型从纯粹的生成工具转化为可嵌入物理约束的估计框架。

### 2. 核心机制对比：UDP 如何改变“UWB 距离利用”这一关键槽位

| 方法类别 | 代表工作 | UWB 距离的利用方式 | 几何约束建模 | 运动估计架构 |
|---------|---------|-------------------|-------------|-------------|
| 纯 IMU | DIP, TIP, DynaIP | 不使用 UWB | 无 | RNN/Transformer 回归 |
| IMU+物理优化 | PIP, PNP, GlobalPose | 不使用 UWB | 间接（物理优化器） | 回归 + 物理后处理 |
| IMU+UWB（特征级融合） | UIP, UMotion, GIP | 作为辅助输入特征（拼接/GCN） | 无显式建模 | GCN/Transformer 回归 |
| 扩散模型 | DiffusionPoser | 不使用 UWB | 无 | 扩散去噪 |
| **UDP（本文）** | — | **通过 MDS 重建 3D 传感器布局作为显式空间条件；在采样中引入 FK 引导强制距离一致性** | **显式：MDS 几何先验 + 前向运动学引导** | **自回归扩散修复模型** |

这一对比揭示了 UDP 的方法论跃迁：从“让网络隐式学习距离与姿态的关联”到“将距离的几何约束显式编码进模型结构和采样过程”。具体而言，UDP 通过两个互补模块实现这一跃迁：

- **Spatial Layout Module（SPL）**：利用经典多维尺度分析（metric MDS）从 UWB 距离矩阵的封闭解中恢复无向 3D 传感器布局，再通过可学习的 Rotation Estimator（3 层 LSTM）将其定向并细化，生成有向的 3D 传感器位置作为扩散模型的条件输入。这一过程将 UWB 距离转化为物理上可解释的空间先验，而非抽象的特征向量。

- **UWB-Diffusion Guidance**：在扩散采样步骤中，通过前向运动学计算当前预测姿态对应的传感器间距离，与测量距离比较得到引导损失 $\epsilon_{uwb} = \sum_{i<j} \| \hat{d}_{ij}(\hat{\mathcal{M}}_0) - d_{ij} \|^2$，并以此梯度引导采样过程，强制预测姿态满足观测距离约束。这一机制将几何约束内联到生成过程中，无需外部物理优化器。

### 3. 适用边界与局限

尽管 UDP 在多个基准上取得 SOTA 性能，其方法设计隐含以下适用边界：

- **传感器布局固定性**：当前系统假定六个传感器位于标准位置（头、骨盆、双腕、双膝），SPL 模块和引导机制均依赖这一固定拓扑。在任意数量或非标准位置的传感器配置下，MDS 重建的语义对齐和引导的有效性尚未验证。

- **UWB 噪声的容忍上限**：消融实验表明，UDP 对 UWB 噪声具有鲁棒性，但在极高噪声或多路径干扰场景下，MDS 重建精度和引导效果可能显著下降。论文未给出噪声容忍的定量上限。

- **单人假设**：当前框架仅处理单人姿态估计，未扩展到多人交互或人与物体交互场景。GIP 等工作的多人扩展路径对 UDP 的适用性有待探索。

- **实时性限制**：扩散模型的迭代采样过程可能引入较高计算延迟，论文未提供在低功耗可穿戴设备上的实时性分析。这是从学术基准走向实际部署的关键瓶颈。

### 4. 开放问题与未来方向

UDP 开启的“几何约束驱动扩散估计”范式为以下问题提供了研究入口：

1. **不确定性感知的几何建模**：如何将 UWB 距离的不确定性（如置信度或残差分布）融入 SPL 模块和 UWB 引导损失，使模型在传感器噪声增大时自适应降低几何约束的权重？

2. **多约束联合引导**：是否可以将物理约束（如关节限制、接触力、动力学方程）作为额外的扩散引导项，与 UWB 几何引导协同作用，实现物理上更合理的运动估计？这将是 UDP 与 PIP/PNP 等物理优化方法在扩散框架下的统一。

3. **传感器布局泛化**：UDP 的框架能否扩展到任意数量和位置的传感器？例如，从松散的 3-4 个传感器可靠恢复全身姿态，将极大降低穿戴复杂度。

4. **实时扩散采样**：扩散模型的采样步骤是否可以大幅减少（如通过蒸馏、一致性模型或隐式扩散）以满足严格实时应用的需求？这是可穿戴设备部署的关键。

5. **统一状态估计框架**：在真实世界部署中，如何联合校准 IMU 传感器偏移和 UWB 天线延迟，建立统一的状态估计框架？当前训练依赖合成数据，真实传感器噪声分布差异可能影响精度。

6. **跨模态几何约束推广**：UDP 的几何约束建模能否推广到其他测距模态（如 ToF、蓝牙 RSSI 测距、声学测距）以提升通用性和鲁棒性？

### 5. 知识库定位

UDP 在可穿戴人体运动估计知识库中占据“几何约束驱动的扩散生成”这一新坐标。其核心知识贡献可归纳为：

- **方法论贡献**：首次证明，将 UWB 距离的几何约束显式建模为 MDS 空间先验和扩散引导信号，可以在不依赖外部物理优化器的情况下，同时提升姿态精度和平滑性。消融实验表明，同时移除 SPL 和 UWB 引导使 JPE 增加 17%，单独应用 UWB 引导可使 SIP 降低 5%、JPE 降低 7%。

- **架构贡献**：提出了自回归扩散修复模型与几何引导采样的联合框架，为扩散模型在物理约束估计任务中的应用提供了可复用的设计模式。

- **经验贡献**：在 DIP-IMU、DanceDB、TotalCapture、UIP-DB 和 GIP-DB 五个数据集上的全面评估（包括 UWB 噪声鲁棒性分析）为后续研究提供了可靠的基准参照。



## 原文 PDF

![[paperPDFs/CVPR_2026/Ultra_Diffusion_Poser_Diffusion_Based_Human_Motion_Tracking_from_Sparse_Inertial_Sensors_and_Ranging_based_Between_sensor_Distances.pdf]]
