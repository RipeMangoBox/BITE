---
title: "Animating the Uncaptured: Humanoid Mesh Animation with Video Diffusion Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Animating_the_Uncaptured_Humanoid_Mesh_Animation_with_Video_Diffusion_Models.pdf
openreview_forum_id: DIPeQTxpe7
aliases:
- AU
- AUHMAVDM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "利用在大规模视频数据上训练的文本-到-视频扩散模型作为运动先验，并通过SMPL身体模型作为变形代理将2D视频中的运动传递到3D网格。"
primary_logic: "视频扩散模型隐式地学习了真实世界动态运动先验，无需额外的4D监督即可生成多样化且逼真的人形网格动画。"
claims:
- "在CAPE数据集上，定量追踪性能（MPJPE, PVE, Accel）全面优于SMPLIFY-X、WHAM、Multi-HMR。"
- "感知用户研究显示参与者明显偏好本方法生成的动作，在提示一致性和自然度上均优于基线（MDM、FineMoGen等）。"
- "消融实验表明时序损失（L_temp）对加速度误差至关重要，移除后Accel从1.5升至3.2；MLP参数化比直接优化更平滑。"
- "CAPE 上 MPJPE = 0.036"
---

# Animating the Uncaptured: Humanoid Mesh Animation with Video Diffusion Models

> [!tip] 核心洞察
> 视频扩散模型隐式地学习了真实世界动态运动先验，无需额外的4D监督即可生成多样化且逼真的人形网格动画。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 动画未捕获：基于视频扩散模型的人形网格动画 |
| 英文题名 | Animating the Uncaptured: Humanoid Mesh Animation with Video Diffusion Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=DIPeQTxpe7); [Project](https://marcb.pro/atu) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Animating the Uncaptured |
| Dataset | CAPE, Mixamo |

> [!tip] 效果简介
> - CAPE 上，MPJPE 为 0.036，对比 0.045 (Multi-HMR)，变化 -20%。
> - CAPE 上，PVE 为 0.041，对比 0.054 (WHAM)，变化 -24.1%。
> - CAPE 上，Accel 为 1.49，对比 2.18 (SMPLIFY-X*)，变化 -31.7%。

## 概述

**问题瓶颈**：传统文本-到-动作生成方法依赖于有限的4D动作捕捉数据集（如AMASS、Human3.6M）进行训练，导致对开放域文本提示的泛化能力不足。同时，从单目视频中追踪3D人体运动是一个本质欠约束问题，在遮挡或极端姿态下易产生歧义和不准确的重建结果。

**核心洞察**：在大规模视频数据上训练的文本-到-视频扩散模型隐式地学习了真实世界的动态运动先验，无需额外的4D监督即可生成多样化且逼真的人体动作。通过将这种广义运动先验与SMPL身体模型相结合，可以实现从2D生成视频到3D网格动画的运动传递。

**方法定位**：本文提出“Animating the Uncaptured”框架，其核心调控变量在于**运动先验来源的根本性改变**——从直接从4D动捕数据集学习，转向利用预训练视频扩散模型（如Kling AI）作为广义运动先验。方法将SMPL身体模型作为变形代理，通过重心坐标将输入网格顶点重新参数化到SMPL面片上，并利用浅层MLP预测时序姿态、平移和旋转参数。视频追踪阶段同时使用2D身体关键点、轮廓和DINOv2密集特征作为多模态线索，配合时序正则化确保动作平滑。

**主要结果**：
- 在CAPE数据集上，本方法在MPJPE（0.036）、PVE（0.041）和Accel（1.49）三项指标上全面优于SMPLIFY-X、WHAM和Multi-HMR等基线方法，其中Accel相对最佳基线降低31.7%。
- 30人参与的感知用户研究显示，参与者在提示一致性和动作自然度上显著偏好本方法生成的动画，优于MDM、FineMoGen、MotionDiffuse等文本-到-动作生成方法。
- 消融实验证实时序损失（L_temp）对加速度误差至关重要，移除后Accel从1.5升至3.2；MLP参数化相比直接优化SMPL参数能产生更平滑的运动轨迹。

**局限性**：生成的视频可能包含变形伪影（morphing effects）导致追踪失败；单目追踪在遮挡场景下仍存在歧义；优化过程耗时约1.5小时/序列，难以实时应用；方法依赖外部视频扩散模型的输出质量。

## 背景与动机

### 问题背景

为静态3D人形网格生成逼真的4D动画序列，是计算机视觉与图形学中长期存在的挑战。这一任务在游戏开发、影视制作、虚拟现实等领域有广泛需求，但传统动画制作流程依赖专业动画师手工关键帧设计或昂贵的动作捕捉设备，成本高且周期长。近年来，文本驱动的动作生成方法试图通过自然语言描述直接合成3D人体运动，以降低内容创作门槛。

### 现有方法缺口

当前文本-到-动作生成方法面临一个根本性瓶颈：**训练数据规模与多样性的严重受限**。主流方法——如 **MDM**（Tevet et al., ICLR 2023）、**MotionDiffuse**（Zhang et al., TPAMI 2024）、**ReMoDiffuse**（Zhang et al., ICCV 2023）——依赖AMASS、Human3.6M等4D动作捕捉数据集进行训练。这些数据集虽然标注精确，但规模有限（通常仅涵盖数百小时的动作），且动作类型偏向实验室环境下的规范运动，难以覆盖真实世界中丰富多样的动态行为。这导致模型在面对开放式文本提示时泛化能力不足，生成的动作往往缺乏真实感和多样性。

与此同时，从单目视频中追踪3D人体运动本身就是一个本质欠约束问题——单张2D图像对应无穷多种可能的3D姿态。传统方法如 **SMPLIFY-X**（Pavlakos et al., CVPR 2019）通过逐帧独立优化SMPL参数来拟合2D关键点，但缺乏时序一致性约束，导致生成的动画存在明显抖动；基于学习的方法如 **WHAM**（Shin et al., CVPR 2024）和 **Multi-HMR**（Baradel et al., 2024）虽然利用大规模数据学习先验，但训练数据仍局限于动作捕捉领域，对开放场景的泛化能力有限。

### 核心动机

本工作的核心洞察是：**视频扩散模型在大规模互联网视频数据上训练时，隐式地习得了强大的真实世界动态运动先验**。这些模型——如Kling AI等文本-到-视频生成模型——能够根据文字描述生成包含丰富人体运动的视频序列，其内部表示蕴含了对物理运动规律的深刻理解，且无需额外的4D监督信号。

基于此，本文提出“Animating the Uncaptured”方法，将视频扩散模型作为广义运动先验源，通过SMPL身体模型作为变形代理，将2D视频中的运动传递到3D网格。这一框架跳出了对4D动作捕捉数据集的依赖，使得从任意文本提示生成多样化且逼真的人形网格动画成为可能。

## 核心创新

本方法的核心创新在于**将视频扩散模型隐式学习的大规模真实世界运动先验引入三维网格动画生成**，从而绕过了传统文本-到-动作方法对稀缺4D动作捕捉数据集的依赖。这一范式转换通过三个关键的“changed slots”实现：

### 1. 运动先验来源：从4D捕捉到视频生成模型

传统方法（如MDM、FineMoGen、MotionDiffuse）直接从AMASS、Human3.6M等4D动作捕捉数据集学习运动分布，受限于数据规模和场景多样性。本方法转而利用在互联网规模视频数据上预训练的文本-到-视频扩散模型（如Kling AI）作为广义运动先验——给定文本提示和输入网格的初始渲染图，模型生成描述目标动作的2D视频，其隐式编码的运动动态无需额外4D监督。这一转换使得方法能够生成“跳舞”、“攀岩”等捕捉数据稀缺的动作类别（Figure 3），并在感知用户研究中获得显著更高的提示一致性和自然度评分（Figure 4）。

### 2. 网格变形模型：SMPL作为变形代理

不同于直接对输入网格进行骨架绑定或blend shapes变形，本方法将SMPL身体模型作为**变形代理**：首先将SMPL拟合到输入网格，再通过重心坐标将每个网格顶点重新参数化为其最近SMPL面片的线性组合加沿法线偏移（Equation 4）。运动传递时，仅需优化SMPL的姿态、平移、旋转参数及每顶点偏移量，即可驱动任意人形网格。这一设计解耦了运动表示与网格拓扑，使方法适用于无骨架、无纹理的通用人形网格。

### 3. 视频追踪线索与神经参数化

在从生成视频提取运动信号时，本方法同时使用三类互补线索：
- **2D身体关键点**（MediaPipe估计）提供稀疏关节约束；
- **轮廓**通过二元交叉熵损失匹配渲染轮廓与视频轮廓；
- **DINOv2密集特征**通过可学习的特征映射对齐顶点特征与视频特征，提供稠密语义对应。

相比SMPLIFY-X等逐帧独立优化姿态参数的方法，本方法使用**浅层MLP**参数化时序姿态、平移和旋转，利用位置编码的归纳偏置提升运动平滑性。消融实验（Table 2）证实：直接优化参数（Opt. Parameters）的加速度误差为2.65，而MLP参数化降至1.49；去除时序正则项 $L_{temp}$ 后加速度误差进一步升至3.2，验证了神经时序参数化的关键作用。

### 创新总结

三个changed slots形成闭环：**视频扩散模型**提供开放域运动先验 → **SMPL变形代理**将2D视频运动传递到3D网格 → **多线索追踪+神经参数化**确保时空一致的动画质量。该框架不依赖特定视频扩散模型（附录展示了CogVideoX和Wan2.2的结果），但当前仍受限于单目追踪的固有歧义和优化耗时（约1.5小时/序列）。

## 整体框架

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_DIPeQTxpe7/figures/002_Figure_2.jpg]]
*Figure 2: Method overview. Given an input mesh in an arbitrary pose and a text prompt describing the desired motion, we generate a video conditioned on the text prompt and the rendering of the mesh. We leverage the SMPL body model as a deformation proxy to track the motion from the video and transfer it to the input mesh. Specifically, we fit the SMPL model to the input mesh and associate its vertices with the SMPL faces (3.3.1). Finally, we optimize the SMPL parameters to match the video motion using estimated body landmarks, silhouettes and DINOv2 features extracted from the frames (3.3.2)*

本文提出了一种将静态3D人形网格转化为4D动画序列的方法，其核心思路是利用视频扩散模型隐式习得的广义运动先验，绕过对4D动作捕捉数据集的依赖。整体pipeline由两个阶段构成：**视频生成**与**运动传递**。

### 输入与输出

方法接受两个输入：(1) 一个无纹理、无骨骼绑定的人形网格 $S$，处于任意初始姿态；(2) 一段描述目标动作的自然语言文本提示 $P$。输出为一系列时变变形参数 $\Theta_t$，驱动输入网格生成与文本描述一致的运动序列。

### 阶段一：视频生成

首先将输入网格渲染为单帧RGB图像 $I_{t=0}^{\text{RGB}}$，将其与文本提示 $P$ 一同送入预训练的文本-到-视频扩散模型（如Kling AI），生成一段展示目标动作的2D视频。视频扩散模型在大规模视频数据上训练，隐式编码了真实世界的动态运动先验，因此能够生成多样化且物理合理的运动序列，而无需额外的4D监督。

### 阶段二：运动传递

运动传递阶段将生成视频中的2D运动提取并迁移到3D网格上，包含三个子模块：

1. **特征提取**：从生成视频的每一帧中提取三类线索——MediaPipe 2D身体关键点、前景轮廓、以及DINOv2密集语义特征。这些线索共同构成视频运动的监督信号。

2. **SMPL注册与重参数化**：将SMPL身体模型拟合到输入网格，优化形状参数 $\beta$、初始姿态 $\theta_0$、平移 $T_0$ 和旋转 $R_0$。随后，将输入网格的每个顶点 $v$ 重新参数化为其最近SMPL面片的重心坐标与沿法线偏移量 $d$ 的组合：
   $$v = \gamma_1 v_1^{\text{SMPL}} + \gamma_2 v_2^{\text{SMPL}} + \gamma_3 v_3^{\text{SMPL}} + d \mathbf{n}$$
   这使得SMPL模型成为网格的变形代理——驱动SMPL参数即可间接驱动输入网格。

3. **视频追踪优化**：通过浅层MLP参数化时变姿态 $\theta_t$、平移 $T_t$ 和旋转 $R_t$（利用MLP的位置编码归纳偏置提升时序平滑性），优化变形模型：
   $$\mathcal{D}(S, \Theta_t) = \Gamma\left( s \cdot R_t \cdot \text{SMPL}(\beta, \theta_t) + T_t \right) + \Delta_t$$
   其中 $\Delta_t$ 为每顶点偏移量。优化目标是最小化重投影的SMPL关节与视频2D关键点之间的German-McClure损失、渲染轮廓与视频轮廓之间的二元交叉熵损失、以及渲染密集特征与视频DINOv2特征之间的余弦相似度损失，同时施加时序平滑正则项 $\mathcal{L}_{\text{temp}}$ 和解剖学先验（VPoser正则化、极端弯曲惩罚）。

### 关键设计决策

- **运动先验来源的迁移**：传统方法直接从4D动作捕捉数据集学习运动分布，而本方法将先验来源迁移至视频扩散模型，使其能够生成训练数据中未见的动作类型。
- **多线索融合追踪**：同时使用关键点、轮廓和密集特征三种互补线索，缓解单目追踪的欠约束问题。其中DINOv2密集特征通过可学习的特征映射与顶点特征对齐，增强了纹理缺失情况下的追踪鲁棒性。
- **神经参数化的平滑归纳偏置**：使用MLP而非逐帧独立优化姿态参数，天然抑制高频抖动。消融实验证实，直接优化参数会导致加速度误差从1.49升至2.65。

## 核心模块与公式推导

本方法的核心是将视频扩散模型的广义运动先验通过SMPL变形代理传递到任意人形网格。整个流程由四个关键模块串联：视频扩散模型生成、SMPL注册与重参数化、视频追踪优化、以及时序MLP参数化。

### 视频扩散模型生成

给定文本提示 $P$ 和无纹理人形网格 $S$ 的初始渲染图 $I_{t=0}^{\mathrm{RGB}} \in \mathbb{R}^{H \times W \times 3}$，利用预训练的视频扩散模型（如Kling AI）生成一段描述指定动作的视频序列。该模型隐式地编码了从大规模视频数据中学习的真实世界动态运动先验，无需额外的4D动作捕捉监督。

### SMPL注册与重参数化

SMPL身体模型作为变形代理，其参数包括形状系数 $\beta \in \mathbb{R}^{10}$ 和姿态参数 $\theta \in \mathbb{R}^{23 \times 3}$（23个关节的轴角表示）。注册阶段通过最小化以下目标将SMPL拟合到输入网格：

**关节损失**（加权L2距离，最小化SMPL关节与输入网格估计3D关节位置之差）：

$$\mathcal{L}_{J} = \frac{1}{N} \sum_{i=1}^{N} \omega_i \left\| \hat{J}_i - J_i \right\|_2^2 \tag{1}$$

**点到点损失**（L2距离，最小化输入网格顶点与SMPL网格最近邻顶点之差）：

$$\mathcal{L}_{\mathrm{p2p}}(\mathcal{V}) = \frac{1}{|\mathcal{V}|} \sum_{v \in \mathcal{V}} \left\| v - \mathbf{NN}(v, \mathcal{V}^{\mathrm{SMPL}}) \right\|_2^2 \tag{2}$$

**形状与姿态先验**（L2正则化）：

$$\mathcal{L}_{\beta}(\beta) = \|\beta\|_2^2, \quad \mathcal{L}_{\theta}(\theta_t) = \|\theta_t\|_2^2 \tag{3}$$

注册完成后，输入网格的每个顶点 $v$ 被重新参数化为其最近SMPL面片的重心坐标与沿法线偏移量：

$$v = \gamma_1 v_1^{\mathrm{SMPL}} + \gamma_2 v_2^{\mathrm{SMPL}} + \gamma_3 v_3^{\mathrm{SMPL}} + d \mathbf{n} \tag{4}$$

这一重参数化使得后续仅需优化SMPL参数即可驱动整个输入网格变形。

### 变形模型与视频追踪优化

对于视频第 $t$ 帧，变形模型将SMPL参数映射到输入网格：

$$\mathcal{D}(S, \Theta_t) = \Gamma\left( s \cdot R_t \cdot \mathrm{SMPL}(\beta, \theta_t) + T_t \right) + \Delta_t \tag{5}$$

其中 $\Theta_t = (s, \beta, \theta_t, T_t, R_t, \Delta_t)$ 包含尺度 $s$、形状 $\beta$、姿态 $\theta_t$、平移 $T_t$、旋转 $R_t$ 和每顶点偏移 $\Delta_t$。追踪阶段固定 $s$ 和 $\beta$，优化其余参数以匹配生成视频中的运动。

**总损失函数**（所有帧的数据项平均加正则项）：

$$\mathcal{L}_{\mathrm{total}} = \frac{1}{F} \sum_{t=1}^{F-1} \left( \mathcal{L}_j + \mathcal{L}_{\mathrm{sil}} + \mathcal{L}_{\phi} \right) + \mathcal{L}_{\mathrm{regs}} \tag{6}$$

数据项包含三个线索：

**关节损失**（German-McClure鲁棒损失 $\rho$，最小化重投影SMPL关节与MediaPipe预测的2D关键点之差）：

$$\mathcal{L}_j = \frac{1}{N} \sum_{i=1}^{N} w_i \rho(\hat{j}_i - j_i) \tag{7}$$

**轮廓损失**（二元交叉熵，对齐渲染轮廓与视频提取轮廓）：

$$\mathcal{L}_{\mathrm{sil}} = -\frac{1}{N} \sum_{i=1}^{N} \left( I_{t,i}^{\mathrm{sil}} \log(\hat{I}_{t,i}^{\mathrm{sil}}) + (1 - I_{t,i}^{\mathrm{sil}}) \log(1 - \hat{I}_{t,i}^{\mathrm{sil}}) \right) \tag{8}$$

**特征损失**（余弦相似度，对齐渲染的DINOv2密集特征与视频提取特征，并通过可学习映射提升对齐质量）：

$$\mathcal{L}_{\phi} = \frac{1}{N} \sum_{i=1}^{N} \left( 1 - \frac{\hat{I}_{t,i}^{\phi} \cdot I_{t,i}^{\phi}}{\| \hat{I}_{t,i}^{\phi} \|_2 \| I_{t,i}^{\phi} \|_2} \right) \tag{9}$$

正则项包括：

**时序正则化**（惩罚连续帧间平移、旋转、姿态、3D关节的突变，确保动作平滑）：

$$\mathcal{L}_{\mathrm{temp}}(x) = \sum_{t=1}^{T} \| x_t - x_{t-1} \|_2 \tag{10}$$

**极端弯曲惩罚**（防止肘部和膝部出现不合理解剖学姿势）：

$$\mathcal{L}_{\mathrm{ex.ben.}}(\theta) = \sum_{i \in (\mathrm{elbows, knees})} \exp\{ \theta_i \} \tag{11}$$

### 时序MLP参数化

与传统逐帧独立优化姿态参数不同，本方法使用浅层MLP对 $\theta_t$、$T_t$、$R_t$ 进行时序参数化。MLP的位置编码提供了平滑归纳偏置——消融实验（Table 2）证实，直接优化参数（Opt. Parameters）会使加速度误差（Accel）从1.49升至2.65，验证了神经参数化对时序一致性的关键作用。

## 实验与分析

### 核心实验设置

论文在两类基准上验证方法：**CAPE数据集**（用于定量追踪性能评估）和**Mixamo数据集**（用于可绑定网格的泛化性测试）。追踪对比的基线包括基于优化的**SMPLIFY-X**（Pavlakos et al., CVPR 2019）、其平滑版本SMPLIFY-X*、基于学习的**WHAM**（Shin et al., CVPR 2024）和**Multi-HMR**（Baradel et al., 2024）。动作生成质量的感知评估则与**MDM**（Tevet et al., ICLR 2023）、**FineMoGen**（Zhang et al., NeurIPS 2023）、**MotionDiffuse**（Zhang et al., TPAMI 2024）、**ReMoDiffuse**（Zhang et al., ICCV 2023）和**MotionCLIP**（Tevet et al., ECCV 2022）等文本-到-动作方法进行对比。追踪对比中对WHAM和SMPLIFY-X进行了公平的Procrustes对齐，以匹配输入网格的初始姿态。

### 定量追踪性能

在CAPE数据集的无纹理序列上，本方法在所有三个指标上均全面超越基线（Table 1）：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_DIPeQTxpe7/figures/004_Table_1.jpg]]
*Table 1: Pose fitting performance comparison with SMPLIFY-X (Pavlakos et al., 2019), it’s smoothed version SMPLIFY-X*, WHAM (Shin et al., 2024), Multi-HMR (Baradel* et al., 2024),and our proposed method on untextured sequences from the CAPE dataset. Metrics include Mean-Per-Joint-Position-Error (MPJPE), Per-Vertex-Error (PVE), and acceleration error (Accel). Lower values indicate better performance across all metrics*

- **MPJPE**（Mean Per Joint Position Error）：本方法达到**0.036**，相比Multi-HMR的0.045降低约20%，相比WHAM的0.051降低约29.4%。
- **PVE**（Per Vertex Error）：本方法达到**0.041**，相比WHAM的0.054降低约24.1%，相比SMPLIFY-X的0.057降低约28.1%。
- **Accel**（加速度误差）：本方法达到**1.49**，相比SMPLIFY-X*的2.18降低约31.7%，相比原始SMPLIFY-X的20.57更是降低了一个数量级。

这一显著优势的核心机制在于：传统方法仅依赖2D关键点或轮廓作为追踪线索，而本方法同时引入了**DINOv2密集特征损失**（Equation 9），提供了更丰富的空间对应信号；此外，**MLP参数化**的时序归纳偏置（而非逐帧独立优化）有效抑制了高频抖动，这在加速度指标上体现尤为明显。

在Mixamo数据集上的泛化性测试（Table 3）进一步验证了方法的鲁棒性：本方法PVE为**0.058**，优于WHAM的0.066（降低12.1%）和SMPLIFY-X的0.099（降低41.4%）。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_DIPeQTxpe7/figures/012_Table_3.jpg]]
*Table 3: Per-Vertex-Error (PVE) on riggable untextured sequences from Mixamo (Mixamo, 2025) dataset for WHAM (Shin et al., 2024), SMPLIFY-X (Pavlakos et al., 2019) and our method*

### 感知用户研究

30名参与者参与了双选强制选择偏好测试和Likert量表评分（Figure 4）：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_DIPeQTxpe7/figures/007_Figure_4.jpg]]
*Figure 4: User study results. (Left) User study indicating the percentage of users that prefer our method over baselines. (Right) Perceived quality of the generated motions, where 5/0 indicate strong agreement/disagreement with the statement: “The video...” Figure 5: Qualitative evaluation. We compare the motions generated by MDM (Tevet et al., 2023) and our method for some of the prompts used in the perceptual study. We show two views (front and side) of the generated motions for multiple frames*

- **提示一致性**（Q1：“视频中的人是否在执行文本描述的动作？”）：参与者对本方法的偏好百分比**显著高于所有基线**。
- **自然度**（Q2：“动作看起来是否自然？”）：本方法同样获得多数偏好。
- **Likert量表**（1-5分，评估整体真实感）：本方法得分高于所有对比方法。

定性对比（Figure 5）显示，MDM生成的“练习双截棍”动作存在明显的脚部滑动和身体僵硬问题，而本方法通过视频扩散模型的广义运动先验，生成了更符合物理直觉的流畅动作。

### 消融实验

Table 2的消融实验揭示了各组件的因果贡献：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_DIPeQTxpe7/figures/009_Table_2.jpg]]
*Table 2: Ablation study on the effect of various components on performance. Metrics include MPJPE (Mean Per Joint Position Error), PVE (Per Vertex Error), and Accel (Acceleration Error). Lower is better for all metrics*

| 消融变体 | MPJPE | PVE | Accel |
|---------|-------|-----|-------|
| 完整方法（Ours） | **0.0362** | **0.0410** | **1.49** |
| 移除姿态先验 L_θ | 0.0486 | 0.0556 | 1.79 |
| 移除极端弯曲惩罚 L_ex.ben. | 0.0366 | 0.0416 | 1.52 |
| 移除特征损失 L_φ | 0.0378 | 0.0427 | 1.51 |
| 移除时序正则 L_temp | 0.0362 | 0.0411 | **3.20** |
| 直接优化参数（Opt. Parameters） | 0.0385 | 0.0427 | 2.65 |

关键发现：

1. **时序正则项 L_temp 是加速度平滑的决定性因素**：移除后Accel从1.49飙升至3.20（增幅115%），而空间精度（MPJPE/PVE）几乎不受影响。这表明L_temp独立承担了时序一致性约束的角色。
2. **MLP参数化优于直接优化**：将MLP替换为逐帧独立优化（Opt. Parameters）后，Accel升至2.65，验证了神经参数化提供的平滑归纳偏置。MLP通过位置编码隐式编码了相邻帧之间的连续性先验。
3. **姿态先验 L_θ 对空间精度贡献最大**：移除后MPJPE从0.0362升至0.0486（增幅34%），PVE从0.0410升至0.0556（增幅36%）。该损失通过VPoser将姿态约束在合理的人体姿态流形上，防止追踪陷入解剖学不合理的局部最优。
4. **特征损失 L_φ 和极端弯曲惩罚 L_ex.ben. 提供边际但稳定的改进**：移除后各指标轻微上升，但未出现灾难性退化，说明它们是辅助性正则项。

### 失败模式分析

Figure 6展示了典型的失败案例：“抱石攀岩”动作中，生成的视频突然将身体正面变形（morph）为背面。本方法通过**平滑旋转网格**来适应这一突变，在中间帧保持了网格完整性，但最终帧仍无法准确表示网格形态。这一失败模式揭示了方法的根本局限：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_DIPeQTxpe7/figures/008_Figure_6.jpg]]
*Figure 6: Failure case. Example of a failure case for the action “bouldering” where the generated video suddenly morphs the front of the body into the back. Our method solves this by smoothly rotating the mesh to accommodate the sudden change. At the end, the generated video fails to represent the mesh accurately which can be seen in the last column. However, this still does not collapse the final mesh*

- **单目追踪的本质欠约束性**：当视频扩散模型产生不符合三维几何一致性的变形伪影时，基于2D线索的追踪优化无法区分“真实的姿态变化”与“生成模型的渲染错误”。
- **视频扩散模型的质量瓶颈**：方法效果直接受限于上游视频生成模型。当前使用的Kling AI为闭源模型，其输出可控性和一致性存在上限。论文在附录中展示了使用CogVideoX和开源Wan2.2的结果，表明方法不依赖于特定模型，但生成质量差异会影响最终动画效果。

### 计算开销与实用限制

优化过程耗时约**1.5小时/序列**，难以满足实时应用需求。这一开销主要来自：逐帧的SMPL参数优化、密集特征提取与匹配、以及ARAP正则化的迭代求解。论文未提供详细的推理时间分解或加速策略，这一限制在当前阶段是实际部署的主要障碍。

## 方法谱系与知识库定位

### 核心瓶颈与动机

传统文本-到-动作生成方法（如 **MDM** (Tevet et al., ICLR 2023)、**FineMoGen** (Zhang et al., NeurIPS 2023)、**MotionDiffuse** (Zhang et al., TPAMI 2024)）的训练依赖于4D动作捕捉数据集（如AMASS、Human3.6M），这些数据集体量有限、动作多样性不足，导致模型在开放文本提示下的泛化能力薄弱。与此同时，单目视频追踪方法（如 **SMPLIFY-X** (Pavlakos et al., CVPR 2019)、**WHAM** (Shin et al., CVPR 2024)）面临本质上的欠约束问题——从2D观测恢复3D运动存在固有歧义，在遮挡或极端姿势下尤为严重。

本方法的核心洞察在于：大规模视频扩散模型在训练过程中隐式习得了丰富的真实世界动态运动先验，无需额外4D监督即可生成多样化且物理合理的运动。通过将这一先验与SMPL身体模型作为变形代理相结合，方法在“文本→视频→3D网格动画”的路径上绕开了4D数据瓶颈。

### 方法定位与关键设计

**Animating the Uncaptured** 处于文本-到-动作生成与单目视频3D追踪的交叉点，但其设计逻辑与两类基线存在根本差异：

| 设计维度 | 基线方法 | 本方法 |
|---------|---------|--------|
| 运动先验来源 | 直接从4D动作捕捉数据集学习（MDM、FineMoGen等） | 利用在大规模视频数据上预训练的文本-到-视频扩散模型（如Kling AI）作为广义运动先验 |
| 网格变形模型 | 基于骨架绑定或blend shapes的直接变形 | 使用SMPL身体模型作为变形代理，将输入网格顶点重新参数化为SMPL面片的重心坐标 |
| 视频追踪线索 | 仅使用2D关键点或轮廓（SMPLIFY-X、WHAM等） | 同时使用2D身体关键点、轮廓、以及DINOv2密集特征，并引入可学习的特征映射 |
| 时序参数化 | 逐帧独立优化姿态参数（如SMPLIFY-X） | 使用浅层MLP预测时序姿态、平移、旋转参数，利用位置编码的归纳偏置提升平滑性 |

**SMPL注册与重参数化**（Section 3.3.1）是连接视频先验与任意输入网格的关键桥梁。方法首先将SMPL模型拟合到输入网格，通过加权关节损失 $\mathcal{L}_J$ 和点到点损失 $\mathcal{L}_{\mathrm{p2p}}$ 优化形状参数 $\beta \in \mathbb{R}^{10}$、姿态参数 $\theta \in \mathbb{R}^{23 \times 3}$、尺度 $s$、平移 $T_0$ 和旋转 $R_0$。随后，每个输入网格顶点被表示为最近SMPL面片的重心坐标与沿法线偏移的组合：

$$v = \gamma_1 v_1^{\mathrm{SMPL}} + \gamma_2 v_2^{\mathrm{SMPL}} + \gamma_3 v_3^{\mathrm{SMPL}} + d \mathbf{n}$$

这一参数化使得任意拓扑的网格都能通过SMPL的变形驱动，同时保留原始网格的几何细节。

**视频追踪优化**（Section 3.3.2）通过多线索损失函数将视频中的运动传递到3D网格。总损失函数为：

$$\mathcal{L}_{\mathrm{total}} = \frac{1}{F} \sum_{t=1}^{F-1} \left( \mathcal{L}_j + \mathcal{L}_{\mathrm{sil}} + \mathcal{L}_{\phi} \right) + \mathcal{L}_{\mathrm{regs}}$$

其中 $\mathcal{L}_j$ 使用German-McClure鲁棒损失最小化重投影关节与MediaPipe预测2D关键点的差异；$\mathcal{L}_{\mathrm{sil}}$ 为渲染轮廓与视频轮廓的二元交叉熵损失；$\mathcal{L}_{\phi}$ 为渲染密集特征与DINOv2视频特征的余弦相似度损失。正则项包括时序平滑 $\mathcal{L}_{\mathrm{temp}}$、姿态先验 $\mathcal{L}_\theta$、极端弯曲惩罚 $\mathcal{L}_{\mathrm{ex.ben.}}$ 等。

### 证据强度与消融发现

**定量追踪性能**（Table 1）在CAPE数据集上提供了强证据（置信度0.95）：本方法在MPJPE（0.036 vs. Multi-HMR 0.045，-20%）、PVE（0.041 vs. WHAM 0.054，-24.1%）、Accel（1.49 vs. SMPLIFY-X* 2.18，-31.7%）上全面优于所有基线。

**消融实验**（Table 2）揭示了各组件的因果贡献：
- 移除时序正则项 $\mathcal{L}_{\mathrm{temp}}$ 导致加速度误差从1.5骤升至3.2，验证了时序平滑约束对运动连贯性的关键作用。
- 直接优化SMPL参数（Opt. Parameters）替代MLP参数化，Accel升至2.65，证实了神经参数化的平滑归纳偏置。
- 移除姿态先验 $\mathcal{L}_\theta$ 导致空间精度下降（MPJPE 0.0486，PVE 0.0556），表明VPoser人体先验对约束解空间的重要性。

**感知用户研究**（Figure 4，30名参与者）显示本方法在提示一致性和自然度上显著优于MDM、FineMoGen等基线，提供了用户体验层面的支持证据（置信度0.9）。

### 适用边界与局限

1. **视频扩散模型依赖性**：方法效果直接受制于所使用视频生成模型的质量。当前主要使用闭源的Kling AI，尽管附录展示了CogVideoX和开源Wan2.2的兼容性结果，但模型输出的变形伪影（morphing effects）仍可能导致追踪失败（Figure 6展示了“攀岩”动作中身体前后翻转的失败案例）。

2. **单目歧义**：尽管多线索追踪（关键点+轮廓+DINOv2特征）缓解了部分歧义，但在严重遮挡或极端姿势下，3D姿态估计仍存在固有不确定性。

3. **计算开销**：优化过程耗时约1.5小时/序列，难以满足实时应用需求。

4. **输入假设**：方法仅适用于人形网格，且假设输入为无纹理网格。对于带纹理的网格或非人形角色，当前框架无法直接适配。

### 开放问题

论文明确指出的开放方向包括：
- 集成深度预测器（如Khirodkar et al., 2024）或多视图扩散模型（如4Diffusion、SV4D）以减轻单目歧义。
- 利用本方法生成4D人类运动数据集，用于训练和评估下游任务。
- 扩展到非人形角色或复杂交互场景。
- 处理视频中的相机运动或变焦，而非假设固定相机视角。

需要手动验证的问题：论文未提供与检索增强方法 **ReMoDiffuse** (Zhang et al., ICCV 2023) 和CLIP空间对齐方法 **MotionCLIP** (Tevet et al., ECCV 2022) 的直接定量对比，仅通过用户研究间接比较。这些基线的相对优势需进一步实验确认。

## 原文 PDF

![[paperPDFs/ICLR_2026/Animating_the_Uncaptured_Humanoid_Mesh_Animation_with_Video_Diffusion_Models.pdf]]
