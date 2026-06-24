---
title: "Weakly Supervised Learning of Rigid 3D Scene Flow"
type: paper
paper_level: A
venue: CVPR
year: 2021
pdf_ref: paperPDFs/CVPR_2021/Weakly_Supervised_Learning_of_Rigid_3D_Scene_Flow.pdf
project_link: https://3dsceneflow.github.io/
aliases:
- WSLR3SF
tags:
- CVPR_2021
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入对象级刚性假设，将场景流参数化为少量刚性变换，使得训练仅需前景/背景二值掩码和自运动等弱监督信号。"
primary_logic: "通过将动态场景分解为刚性移动对象，联合利用对象级刚性约束、自运动估计和测试时优化，可在仅提供弱标注的情况下实现准确、可解释的三维场景流估计。"
claims:
- "在 lidarKITTI 上，弱监督的 Ours++ 将 EPE3D 从全监督 PointPWC-Net 的 0.390 m 降至 0.094 m，减少约 0.3 m。"
- "消融实验证明，同时使用自运动损失、Chamfer 距离损失和刚性损失对性能至关重要，完整目标 EPE=0.134 m。"
- "弱监督模型在 stereoKITTI (含地面) 上甚至超越全监督方法，Ours++ EPE3D=0.068 m vs FlowNet3D 0.177 m。"
- "lidarKITTI (w/o ground) 上 EPE3D [m]↓ = 0.094 (Ours++ weakly supervised)"
---

# Weakly Supervised Learning of Rigid 3D Scene Flow

> [!tip] 核心洞察
> 通过将动态场景分解为刚性移动对象，联合利用对象级刚性约束、自运动估计和测试时优化，可在仅提供弱标注的情况下实现准确、可解释的三维场景流估计。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 刚性三维场景流的弱监督学习 |
| 英文题名 | Weakly Supervised Learning of Rigid 3D Scene Flow |
| 会议/期刊 | CVPR 2021 |
| Links | [paper](https://arxiv.org/abs/2102.08945); [Project](https://3dsceneflow.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Rigid3DSceneFlow |
| Dataset | lidarKITTI (w/o ground), stereoKITTI (w/o ground), stereoKITTI (with ground), semanticKITTI (w/o ground) |

> [!tip] 效果简介
> - lidarKITTI (w/o ground) 上，EPE3D [m]↓ 为 0.094 (Ours++ weakly supervised)，对比 0.390 (PointPWC-Net, full supervision)，变化 -0.296。
> - stereoKITTI (w/o ground) 上，EPE3D [m]↓ 为 0.042 (Ours fully supervised)，对比 0.056 (FLOT, full supervision)，变化 -0.014。
> - stereoKITTI (with ground) 上，EPE3D [m]↓ 为 0.068 (Ours++ weakly supervised)，对比 0.177 (FlowNet3D, full supervision)，变化 -0.109。

## 概述

### 问题背景与瓶颈

从连续点云帧中估计三维场景流（scene flow）是自动驾驶与机器人感知中的基础任务。当前主流方法依赖全监督学习，需要逐点的密集三维流标注。**获取这类密集标注成本极高且极易引入噪声**，这严重限制了全监督方法的可扩展性与实际部署能力。同时，在合成数据上训练的全监督模型面临显著的域间差异（domain gap），迁移到真实激光雷达数据时性能大幅退化。

### 核心思想

本文提出 **Rigid3DSceneFlow**，一种基于对象级刚性假设的弱监督三维场景流估计框架。其核心洞察是：**将动态场景分解为刚性移动对象，联合利用对象级刚性约束、自运动估计和测试时优化，可在仅提供弱标注信号的情况下实现准确且可解释的场景流估计**。

具体而言，该方法将场景流参数化为少量刚性变换，而非逐点的无约束流向量。训练时仅需**前景/背景二值掩码**和**传感器自运动**两种弱监督信号，完全避开了密集流标注的需求。

### 方法定位

从监督范式看，现有场景流方法主要分为两类：全监督方法（如 **FlowNet3D** 、**PointPWC-Net** 、**FLOT** ）在合成数据上性能良好但域迁移困难；无监督方法则因缺乏引导而精度不足。本文的弱监督策略恰好填补了两者之间的空白——**以远低于全监督的标注成本，获得超越全监督方法的性能**（Figure 2）。

从运动表示看，该方法将传统的无约束逐点流向量替换为**每对象刚性变换参数**，使场景流估计变为对少量 SE(3) 变换的推断，大幅降低了学习复杂度并提升了可解释性。

### 主要结果

- **lidarKITTI（无地面）**：弱监督的 Ours++ 将 EPE3D 从全监督 PointPWC-Net 的 0.390 m 降至 **0.094 m**，误差减少约 0.3 m。
- **stereoKITTI（含地面）**：弱监督模型甚至超越全监督方法，Ours++ EPE3D 为 **0.068 m**，而 FlowNet3D 为 0.177 m。
- **跨数据集泛化**：在 semanticKITTI 上训练后，无需微调即可在 Waymo Open 上取得有竞争力的结果；经微调后前景召回率提升超过 20 个百分点。
- **消融实验**：联合使用自运动损失、Chamfer 距离损失和刚性损失对性能至关重要——仅用分割损失时 EPE 为 0.599 m，而完整目标下 EPE 降至 **0.134 m**。

### 局限与开放问题

该方法仍需弱监督信号，无法完全无监督运行。当前前景聚类依赖 DBSCAN 假设对象空间分离，在密集交互场景可能失效。当背景仅剩地面点时，自运动估计可能失败；稀有对象（如卡车）的掩码预测也不可靠。此外，lidarKITTI 标注噪声影响定量评估的精确性。未来方向包括：结合多帧信息提升时序一致性、改进困难场景和稀有对象的处理、以及加速测试时优化以适应实时自动驾驶应用。

## 背景与动机

### 三维场景流估计的核心瓶颈

三维场景流估计旨在从连续两帧点云中恢复每个点的三维运动向量，是自动驾驶、机器人导航等动态环境感知的基础任务。然而，获取密集的点级场景流真值标注极其困难：人工标注成本高昂且易出错，合成数据（如 FlyingThings3D）虽可提供自动标注，却引入了显著的域间差异，限制了全监督方法在真实 LiDAR 数据上的泛化能力和实际部署。

### 现有方法的困境

当前场景流方法主要分为两个阵营，各自面临根本性困境（见 Figure 2）：

- **全监督方法**（如 **FlowNet3D**、**HPLFlowNet**、**PointPWC-Net**、**FLOT**、**EgoFlow**）：依赖合成数据训练，在真实场景中因域差异导致性能退化。例如，PointPWC-Net 在 lidarKITTI 上的 EPE3D 高达 0.390 m。
- **无监督方法**：完全摆脱标注依赖，但缺乏有效的学习信号，性能显著低于全监督方法。

这种“全监督受限于域差异，无监督受限于性能”的僵局，成为制约场景流估计走向实际应用的关键瓶颈。

### 核心动机：弱监督作为第三条路径

本文的核心动机是打破上述二元对立，探索第三条路径——**弱监督学习**。关键洞察在于：动态场景中的绝大多数对象（车辆、行人、骑行者等）可被近似为**刚性运动体**。基于这一刚性假设，场景流可以被参数化为少量刚性变换参数的组合，而非逐点无约束的运动向量。

这一参数化带来了监督信号的质变：训练不再需要密集的场景流真值，而仅需**前景/背景二值掩码**和**传感器自运动**这两种弱监督信号。前者可通过简单的语义标注或手工标注获得，后者可从 IMU/GPS 或 SLAM 系统获取，获取成本远低于逐点流标注。

### 方法定位

本文提出的 **Rigid3DSceneFlow** 方法通过将场景抽象为刚性对象集合，联合利用对象级刚性约束、自运动估计和测试时优化，在仅提供弱标注的条件下实现准确、可解释的三维场景流估计。其核心思路是：

1. **场景分解**：将场景分割为前景（可移动对象）和背景（静态结构），背景流解释为传感器自运动，前景流解释为刚性运动簇。
2. **弱监督学习**：通过背景分割损失、自运动损失和前景刚性损失的联合优化，使网络在无逐点流监督下学会预测刚性变换参数。
3. **测试时优化**：利用推断出的对象掩码，通过 ICP 迭代精化每个刚性体的变换，进一步提升精度。

这一框架在全监督和弱监督两种设定下均展现出竞争力：在 stereoKITTI 上以全监督训练达到 0.042 m EPE3D，在 lidarKITTI 上以弱监督训练（Ours++）将 EPE3D 降至 0.094 m，相比全监督 PointPWC-Net 降低约 0.3 m，甚至在 stereoKITTI（含地面）上以弱监督超越全监督 FlowNet3D（0.068 m vs 0.177 m）。

## 核心创新

本工作提出 **Rigid3DSceneFlow**，其核心创新在于将三维场景流估计从“逐点稠密回归”重构为“对象级刚性运动分解”，从而将监督信号从昂贵的逐点流标注大幅松弛为前景/背景二值掩码与自运动信息。这一转变由三个关键改变槽位 (changed slots) 驱动，形成一条因果链：**监督信号的弱化 → 运动表征的结构化 → 训练数据的真实化**。

### 改变槽位 1：监督信号 —— 从稠密流到弱标注

全监督方法（如 **FlowNet3D** 、**PointPWC-Net** 、**FLOT** ）依赖合成数据集 FlyingThings3D 提供的逐点场景流真值，获取成本高且域间差异大。本方法仅需：
- **前景/背景二值掩码**：指示每个点属于可移动前景还是静态背景；
- **自运动信息**：传感器自身的刚性变换。

论文明确指出：“we can relax the requirement for dense flow supervision with a much simpler binary mask annotation and ego‑motion”。这一松弛是后续所有设计的基础——因为不再需要逐点流真值，训练可以直接使用真实 LiDAR 数据，从而消除合成-真实的域差异。

### 改变槽位 2：运动表征 —— 从无约束逐点流到对象级刚性变换

全监督方法输出每个点的自由流向量，缺乏结构约束，易导致对象变形（如 **FLOT** 结果中车辆形状扭曲，见 Figure 4）。本方法将场景分解为刚性运动基元：
- **背景**：所有背景点的运动由单一自运动变换 $T_{ego} \in SE(3)$ 解释；
- **前景**：通过 DBSCAN 聚类将前景点划分为若干刚性对象，每个对象 $k$ 由其自身的刚性变换 $T_k \in SE(3)$ 描述。

论文将此表述为：“we propose a scene abstraction approach that uses rigid objects as the basic components”。这种表征不仅使输出可解释，还使得训练仅需对象级一致性约束（刚性损失 $L_{rigid}$ 和 Chamfer 距离损失 $L_{CD}$），而无需逐点真值。

### 改变槽位 3：训练数据 —— 从合成数据到真实 LiDAR

由于监督信号弱化，训练不再受限于合成数据。模型直接在 **semanticKITTI** 的真实 LiDAR 点云上训练，使用其提供的语义标签派生出前景/背景掩码和自运动。论文指出：“We train a joint model ... using the point clouds from semanticKITTI”。这一改变使得模型天然适应真实传感器的稀疏性、噪声和遮挡模式，在 lidarKITTI 等真实基准上展现出对全监督方法的显著优势。

### 因果链条与证据强度

三个槽位形成强因果耦合：**弱监督信号 (槽位1) 使真实数据训练 (槽位3) 成为可能，而对象级刚性表征 (槽位2) 则提供了在弱监督下仍能学习有效运动分解的归纳偏置**。证据强度极高：

- **lidarKITTI 上**：弱监督 Ours++ 的 EPE3D 达到 0.094 m，比全监督 PointPWC-Net 的 0.390 m 降低约 0.3 m（Table 2，置信度 0.98）。
- **stereoKITTI 跨域泛化**：弱监督 Ours++ 在含地面的 stereoKITTI 上 EPE3D=0.068 m，甚至超越全监督 FlowNet3D 的 0.177 m（Table 5，置信度 0.95）。
- **消融实验**：完整目标函数（$L_{ego}+L_{CD}+L_{rigid}$）达 EPE=0.134 m，而仅用 $L_{ego}$ 时 EPE 飙升至 0.599 m（Table 3，置信度 0.95），证明各损失项的协同必要性。

### 辅助创新：测试时优化

除训练阶段的创新外，方法引入测试时优化模块（ICP 迭代精修每个对象的刚性变换），进一步缩小与全监督方法的差距。该模块利用网络预测的对象掩码，在推理时独立优化背景和每个前景对象的变换，无需额外标注。消融显示，简单 DBSCAN 聚类与使用真值实例掩码性能接近（EPE 0.097 vs 0.101，Table 10），表明整个流水线对实例标注的依赖极低。

### 创新边界与局限

需注意，本方法并非完全无监督——它仍需要前景/背景掩码和自运动作为弱监督信号。当前前景聚类依赖 DBSCAN 假设对象空间分离，在密集交互场景可能失效。此外，当背景仅剩地面点时（如移除所有前景后），自运动估计可能失败（Figure 10）。这些局限为后续研究指明了方向。

## 整体框架

### 核心设计理念：从逐点流到对象级刚性抽象

传统场景流方法直接预测每个点的无约束三维运动向量，这带来了两个根本性困难：其一，获取逐点密集流标注成本极高且易出错；其二，无约束的逐点预测容易产生违反物理刚性的变形（如车辆被拉伸）。Rigid3DSceneFlow 的核心洞察是：**将动态场景分解为刚性移动的基本单元**——背景作为一个整体受传感器自运动支配，前景中的每个独立运动对象各服从一个刚性变换。这一抽象将场景流的自由度从数万个逐点向量压缩为少量 SE(3) 变换参数，使得训练仅需前景/背景二值掩码和自运动等弱监督信号。

Figure 2 将这一设计置于方法谱系中：全监督方法受限于合成数据（如 FlyingThings3D）与真实 LiDAR 数据之间的域鸿沟，无监督方法则因缺乏引导而性能显著下降。弱监督路径恰好取两者之长——用廉价标注换取对真实数据的直接学习能力。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/002_Figure_2.jpg]]
*Figure 2: Recent scene flow methods either use full supervision (and suffer from domain gap) or no-supervision (and suffer from reduced performance). Instead, our method uses weak supervision and benefits from the best of both worlds*

### 整体 Pipeline 与模块关系

如 Figure 3 所示，系统接收连续两帧点云 $X$（源帧）和 $Y$（目标帧）作为输入，通过一个统一的深度网络 $\phi_\Gamma$ 同时完成三项任务，最终输出对象级的场景抽象和逐点刚性场景流：

1. **背景分割**：对 $X$ 和 $Y$ 分别预测每个点的前景概率，将场景划分为背景（静态结构）和前景（可移动对象）。
2. **自运动估计**：在背景区域上建立 $X$ 与 $Y$ 之间的软对应，通过可微分的加权 Kabsch 算法闭式求解背景的刚性变换 $\mathbf{T}_{\text{ego}}$。
3. **前景运动估计**：对前景点进行无监督聚类（DBSCAN），将每个聚类视为一个刚性体；网络为每个聚类预测刚性变换参数 $\{\mathbf{T}_k\}_{k=1}^{K-1}$，并通过刚性损失和 Chamfer 距离损失联合优化。

三个模块共享一个基于 MinkowskiNet 的稀疏卷积 U-Net 骨干网络（Figure 5），该骨干以体素化点云为输入，提取逐点潜在特征。背景分割头、自运动头和场景流头分别从共享特征中解码各自所需的信息，形成端到端的联合优化框架。

### 端到端能量最小化

整个网络的训练被形式化为一个统一的能量最小化问题：

$$\Gamma^{\star} = \operatorname*{argmin}_{\Gamma}\; \mathcal{L}_{\mathrm{BG}} + \mathcal{L}_{\mathrm{ego}} + \mathcal{L}_{\mathrm{FG}}$$

其中三个损失项分别对应上述三个子任务：
- $\mathcal{L}_{\mathrm{BG}}$：前景/背景二值分割的二元交叉熵损失（Eq. 3），对 $X$ 和 $Y$ 分别计算。
- $\mathcal{L}_{\mathrm{ego}}$：自运动变换的 L1 误差与 Sinkhorn 正则项（Eq. 4），其中 $\lambda_{\text{inlier}} = 0.005$。
- $\mathcal{L}_{\mathrm{FG}} = \mathcal{L}_{\mathrm{rigid}} + \lambda_{\text{CD}} \mathcal{L}_{\text{CD}}$：前景刚性损失（Eq. 5）鼓励每个聚类内的流向量可由单一刚性变换解释，Chamfer 距离损失（Eq. 7）对齐变换后的前景点与目标前景点，$\lambda_{\text{CD}} = 0.5$。

### 从对象级变换到逐点场景流

网络直接输出的是对象级的刚性变换参数，而非逐点流向量。为恢复逐点场景流，系统采用两步后处理：

1. **刚性流分配**：将每个前景聚类 $k$ 的刚性变换 $\mathbf{T}_k^\star$ 作用于该聚类内的每个点 $\mathbf{x}$，得到该点的刚性流 $\mathbf{v}^{\text{rigid}} = \mathbf{T}_k^\star \circ \mathbf{x} - \mathbf{x}$。
2. **体素到点的插值**：由于网络在体素化空间中进行计算，刚性流首先在体素中心上定义，然后通过反距离加权插值（Eq. 11）传播回原始点云：

$$\mathbf{v}_i^{\star} = \frac{\sum_{j : \mathbf{x}_j^{v} \in \mathcal{E}(\mathbf{x}_i)} \mathbf{v}_j^{\mathrm{rigid}} \lVert \mathbf{x}_i - \mathbf{x}_j^{v} \rVert_2^{-1}}{\sum_{j : \mathbf{x}_j^{v} \in \mathcal{E}(\mathbf{x}_i)} \lVert \mathbf{x}_i - \mathbf{x}_j^{v} \rVert_2^{-1}}$$

其中 $\mathcal{E}(\mathbf{x}_i)$ 是点 $\mathbf{x}_i$ 的 $k$-近邻体素中心集合。

### 测试时优化（Test-Time Optimization）

网络输出的刚性变换可作为初始化，进一步通过迭代最近点（ICP）在测试时进行精化。优化独立地应用于背景和每个前景对象：以网络预测的掩码为对象区域，最小化变换后源点云与目标点云之间的最近点距离。论文报告了三个递进版本：**Ours**（直接网络输出）、**Ours+**（仅优化自运动）、**Ours++**（优化所有刚性体的变换）。实验表明，完整的测试时优化能持续带来显著的性能增益。

### 输入输出流总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| 骨干网络 | 连续两帧点云 $X, Y$（体素化） | 逐点潜在特征 |
| 背景分割头 | 潜在特征 | 每点前景概率 $\{h_i\}$ |
| 自运动头 | 背景区域特征 | 自运动 $\mathbf{T}_{\text{ego}}$ |
| 场景流头 | 全图特征 | 初始软对应 + 残差流 |
| 前景聚类 | 前景点坐标 | 对象聚类 $\{X_k\}_{k=1}^{K-1}$ |
| 刚性拟合 | 聚类 + 初始流 | 每对象刚性变换 $\{\mathbf{T}_k\}$ |
| 后处理 | 变换 + 掩码 | 逐点刚性场景流 $\mathbf{V}^{\text{rigid}}$ |

### 补充图表

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results of our weakly supervised method on lidarKITTI (top) and waymo open (bottom). For improved visibility, the EPE3D (top row b,c ) is clipped to the range between 0.0 m (white) at 0.3m (red). As a result of predicting an unconstrained pointwise sceneflow, the rigid objects (car) in the results of FLOT might get deformed (d)*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/017_Figure_6.jpg]]
*Figure 6: Successful cases of our method on the lidarKITTI dataset. By correctly splitting the scene into foreground and background (d), our method estimates the accurate scene flow vectors (b), which align the two frames (c)*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/018_Figure_7.jpg]]
*Figure 7: Failure cases of our method on the lidarKITTI dataset. Top: even though the car’s object mask (d) is correctly predicted, its predicted scene flow vectors yield large end-point-errors (b). Bottom: a pillar in the middle of the scene is wrongly predicted as foreground object (d), hence its scene flow does not agree with the background and GT (b)*

## 核心模块与公式推导

### 3.1 整体能量函数

方法的核心是将刚性场景流估计建模为一个能量最小化问题。网络参数 $\Gamma$ 的优化目标为背景分割损失、自运动损失与前景刚性损失之和：

$$\Gamma^{\star} = \operatorname*{argmin}_{\Gamma} \mathcal{L}_{\mathrm{BG}} + \mathcal{L}_{\mathrm{ego}} + \mathcal{L}_{\mathrm{FG}} \tag{Eq.2}$$

该能量函数的设计直接反映了论文的核心洞察：将场景分解为静态背景（由自运动解释）和刚性运动的前景对象，从而仅需弱监督信号即可训练。

### 3.2 背景分割模块

背景分割头由两层稀疏卷积构成，对输入点云 $\mathbf{X}$ 和 $\mathbf{Y}$ 分别预测逐点的前景概率 $h_i$。其损失函数为二元交叉熵：

$$\mathcal{L}_{\mathrm{BG}}^{\mathbf{X}} = \frac{1}{N} \sum_{i=1}^{N} \mathrm{BCE}(h_i^{\mathbf{X}}, \bar{h}_i^{\mathbf{X}}) \tag{Eq.3}$$

其中 $\bar{h}_i^{\mathbf{X}}$ 为前景/背景二值掩码的真值标注。该模块为后续的自运动估计和前景聚类提供必要的场景分解基础。

### 3.3 自运动估计模块

自运动头首先计算背景点云 $\mathbf{X}^b$ 与 $\mathbf{Y}^b$ 的潜在特征之间的亲和矩阵，随后通过 **Sinkhorn 算法**求解最优传输，得到软匹配矩阵。基于该匹配，利用**可微加权 Kabsch 算法**闭式求解背景的刚性变换（即传感器自运动）。

自运动损失由两部分加权组成：

$$\mathcal{L}_{\mathrm{ego}} = \mathcal{L}_{\mathrm{trans}} + \lambda_{\mathrm{inlier}} \mathcal{L}_{\mathrm{inlier}} \tag{Eq.4}$$

- **$\mathcal{L}_{\mathrm{trans}}$**：预测变换与真值变换之间的 L1 误差。
- **$\mathcal{L}_{\mathrm{inlier}}$**：正则项，抑制 Sinkhorn 匹配中向 slack 行/列分配过大权重的倾向，$\lambda_{\mathrm{inlier}} = 0.005$。

消融实验（Table 11）证实，移除 Sinkhorn 正则化会使 EPE 从 0.133 m 急剧升至 0.594 m，表明该模块对自运动估计的稳定性至关重要。

### 3.4 前景刚性损失

前景点经 DBSCAN 聚类后形成 $N^c$ 个刚性代理。对每个聚类 $k$，刚性损失强制其内部的逐点场景流能够被单一刚性变换 $(\mathbf{R}_k, \mathbf{t}_k)$ 解释：

$$\mathcal{L}_{\mathrm{rigid}} = \frac{1}{N^c} \sum_{k=1}^{N^c} \frac{1}{N^k} \sum_{j=1}^{N^k} \| \mathbf{R}_k \mathbf{c}_j^k + \mathbf{t}_k - (\mathbf{c}_j^k + \mathbf{v}_j^k) \|_1 \tag{Eq.5}$$

其中 $\mathbf{c}_j^k$ 为聚类内点的坐标，$\mathbf{v}_j^k$ 为网络预测的初始场景流。该损失是弱监督框架的核心约束，将无约束的逐点流向量参数化为少量刚性变换参数。

### 3.5 Chamfer 距离损失

前景损失的另一组成部分为 Chamfer 距离，对齐变换后的前景点 $\mathbf{X}_v^f$ 与目标帧前景点 $\mathbf{Y}^f$：

$$\mathcal{L}_{\mathrm{CD}} = \sum_{\mathbf{x} \in \mathbf{X}_v^f} \min_{\mathbf{y} \in \mathbf{Y}^f} \|\mathbf{x} - \mathbf{y}\|_2 + \sum_{\mathbf{y} \in \mathbf{Y}^f} \min_{\mathbf{x} \in \mathbf{X}_v^f} \|\mathbf{x} - \mathbf{y}\|_2 \tag{Eq.7}$$

前景总损失为加权和：$\mathcal{L}_{\mathrm{FG}} = \mathcal{L}_{\mathrm{rigid}} + \lambda_{\mathrm{CD}} \mathcal{L}_{\mathrm{CD}}$，其中 $\lambda_{\mathrm{CD}} = 0.5$。消融实验（Table 3）表明，联合使用全部损失项（$\mathcal{L}_{\mathrm{ego}} + \mathcal{L}_{\mathrm{CD}} + \mathcal{L}_{\mathrm{rigid}}$）达到最佳 EPE=0.134 m，而仅用 $\mathcal{L}_{\mathrm{ego}}$ 时 EPE 升至 0.599 m。

### 3.6 场景流插值

网络在体素化空间操作，最终需将体素中心的刚性流 $\mathbf{v}_j^{\mathrm{rigid}}$ 传回原始点云。采用反距离加权插值：

$$\mathbf{v}_i^{\star} = \frac{\sum_{j : \mathbf{x}_j^v \in \mathcal{E}(\mathbf{x}_i)} \mathbf{v}_j^{\mathrm{rigid}} \lVert \mathbf{x}_i - \mathbf{x}_j^v \rVert_2^{-1}}{\sum_{j : \mathbf{x}_j^v \in \mathcal{E}(\mathbf{x}_i)} \lVert \mathbf{x}_i - \mathbf{x}_j^v \rVert_2^{-1}} \tag{Eq.11}$$

其中 $\mathcal{E}(\mathbf{x}_i)$ 为点 $\mathbf{x}_i$ 在体素中心点集中的 k 近邻。该插值保证了从稀疏体素表示到密集点云场景流的平滑过渡。

### 3.7 刚性变换参数化

所有运动均以 SE(3) 群元素表示：

$$SE(3) = \left\{ \mathbf{T} \in \mathbb{R}^{4 \times 4} \colon \mathbf{T} = \begin{bmatrix} \mathbf{R} & \mathbf{t} \\ \mathbf{0} & 1 \end{bmatrix} \right\} \tag{Eq.1}$$

其中 $\mathbf{R} \in SO(3)$ 为旋转矩阵，$\mathbf{t} \in \mathbb{R}^3$ 为平移向量。背景由一个全局 $\mathbf{T}_{\mathrm{ego}}$ 描述，每个前景聚类 $k$ 由一个独立的 $\mathbf{T}_k$ 描述，最终逐点刚性场景流由 $\mathbf{V}^{\mathrm{rigid}} = \{\mathbf{T}_k^{\star} \circ \mathbf{X}_k - \mathbf{X}_k\}_{k=1}^K$ 恢复。

### 3.8 网络骨干

骨干网络基于 **MinkowskiNet**（Choy et al., CVPR 2019），采用 U-Net 风格的编码器-解码器架构，包含跳跃连接和稀疏三维卷积层（详见 Figure 5）。场景流头在潜在空间中计算初始软对应关系，随后通过残差稀疏卷积层进行细化。

## 实验与分析

### 核心实验设计

本文在两类监督设定下评估所提方法 **Rigid3DSceneFlow**：全监督设定用于验证骨干网络及刚性流表示的表达能力；弱监督设定则验证仅依赖前景/背景二值掩码与自运动信号的有效性。训练数据方面，弱监督模型在真实 LiDAR 数据集 **semanticKITTI** 上训练，全监督基线沿用合成数据集 **FlyingThings3D** (FT3D) 的范式。评测基准覆盖 **stereoKITTI** (双目点云)、**lidarKITTI** (LiDAR 点云，含/不含地面点) 以及 **Waymo Open** 的跨域泛化测试。主要指标为三维终点误差 **EPE3D [m]**，辅以旋转误差 **RRE [°]**、平移误差 **RTE [m]** 及分前景/背景的细分指标。

测试时优化分为两档：**Ours+** 仅优化自运动，**Ours++** 对所有刚性体（背景+各前景聚类）进行 ICP 精化。这一设计使同一模型可输出网络直接估计与优化后两种结果，便于剥离网络推理能力与几何后处理各自的贡献。

### 全监督设定下的性能验证

在 FT3D 和 stereoKITTI 上的全监督结果 (Table 1) 表明，即使在传统密集流监督范式下，引入刚性运动表示本身已具竞争力：**Ours** 在 stereoKITTI (无地面) 上取得 **EPE3D = 0.042 m**，优于同期全监督方法 **FLOT** (0.056 m) 和 **PointPWC-Net** (0.118 m)。该优势源于刚性归纳偏置有效抑制了非刚性变形对点级流预测的干扰，尤其在车辆等刚体对象上避免了 FLOT 中常见的“对象扭曲”现象 (Figure 4)。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/016_Figure.jpg]]

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/020_Figure.jpg]]

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/004_Table_1.jpg]]
*Table 1: Evaluation results in a fully supervised setting on FT3D and stereoKITTI datasets*

### 弱监督主结果：跨域与跨模态优势

弱监督设定的核心结果见 **Table 2 (lidarKITTI)** 与 **Table 5 (stereoKITTI)**，构成了全文最关键的因果性证据链。

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/005_Table_2.jpg]]
*Table 2: 1 MeteorNet uses three tine frames and was trained on 100 and evaluated on 42 scenes of this dataset. Table 2: Evaluation results on lidarKITTI. Ours (backbone) denotes our model from § 4.3 trained with full supervision on FT3D. Ours are the direct estimates of our pipeline. Ours+ and Ours++ additionally denote test-time optimization of only ego-motion and all rigid bodies, respectively*

**在 lidarKITTI 上**，弱监督 **Ours++** 在无地面设定下达到 **EPE3D = 0.094 m**，相较全监督 **PointPWC-Net** 的 0.390 m 降低约 **0.3 m** (置信度 0.98)。值得注意的是，全监督方法因在合成数据 (FT3D) 上训练，遭受严重的域间差异——lidarKITTI 的稀疏 LiDAR 扫描与 FT3D 的稠密立体点云在采样模式、遮挡特性上截然不同。弱监督模型直接在真实 LiDAR 数据上学习，绕过了这一域间鸿沟，此为性能大幅领先的因果瓶颈所在。

**在 stereoKITTI 上**，跨模态泛化结果更为惊人：弱监督 **Ours++** (在 LiDAR 点云上训练，直接在 stereo 点云上评测) 在有地面设定下达到 **EPE3D = 0.068 m**，而全监督 **FlowNet3D** 仅为 0.177 m (置信度 0.95)。这意味着弱监督模型不仅免除了密集流标注的高昂成本，更在跨传感器模态的场景中实现了对全监督方法的超越。其机制在于：刚性运动假设作为一种强结构性先验，对点云密度和采样模式的敏感度远低于逐点自由流向量回归。

### 消融实验：损失函数的因果贡献

**Table 3** 系统拆解了训练目标各组分的作用。完整目标 ($\mathcal{L}_{\text{BG}} + \mathcal{L}_{\text{ego}} + \mathcal{L}_{\text{rigid}} + \lambda_{\text{CD}}\mathcal{L}_{\text{CD}}$) 在 lidarKITTI (有地面) 上取得 **EPE = 0.134 m**。逐一移除关键项后：

- **仅用 $\mathcal{L}_{\text{ego}}$**：EPE 骤升至 **0.599 m**，表明自运动损失虽能提供背景运动的弱约束，但缺乏对前景对象的显式建模，网络无法将前景点与背景点有效解耦。
- **移除 $\mathcal{L}_{\text{rigid}}$**：性能显著退化，验证了刚性损失对每个聚类内部流向量一致性的约束是不可替代的——它迫使网络学习“对象级”运动而非散乱的点级偏移。
- **移除 $\mathcal{L}_{\text{CD}}$**：Chamfer 距离损失作为几何对齐项，补充了刚性损失在变换后点云形状层面的监督，移除后同样导致性能下降。

三者联合构成互补监督结构：$\mathcal{L}_{\text{ego}}$ 提供全局运动锚点，$\mathcal{L}_{\text{rigid}}$ 强制局部运动一致性，$\mathcal{L}_{\text{CD}}$ 提供稠密几何对齐信号。

### 关键模块消融

**Sinkhorn 正则化的必要性** (Table 11)：移除 Sinkhorn 算法中的正则化项后，EPE 从 0.133 m 升至 **0.594 m**。Sinkhorn 迭代在背景点匹配中起到“软分配”作用，缺乏正则化时匹配矩阵退化为硬分配，导致自运动估计对离群点极度敏感。该结果揭示：可微匹配层的熵正则化不仅是数值技巧，更是保证自运动估计鲁棒性的结构要素。

**预训练与随机初始化** (Table 7)：在 FT3D 上预训练骨干网络相较随机初始化，在无地面设定下 EPE3D 降低约 **1.4 cm**，有地面设定下降低约 **2.3 cm**。预训练提供了良好的特征提取起点，但即使随机初始化，弱监督目标仍能收敛至可用水平，说明损失函数本身具备足够的约束力。

**前景聚类策略** (Table 10)：简单 DBSCAN 聚类与使用真实实例掩码性能接近 (EPE 0.097 vs 0.101)，甚至略优。这一反直觉结果的原因在于：DBSCAN 基于空间邻近性聚类，恰好与“空间分离的刚性对象”假设吻合；而真实实例掩码可能包含标注噪声或语义上分离但空间上相邻的歧义情况。

**跨域微调** (Table 9)：在 Waymo Open 上微调后，前景召回率提升 **>20 百分点**，平移误差 RTE 降低 **2 cm**。未微调的直接泛化在前景掩码上存在明显退化，说明弱监督信号虽具跨域迁移能力，但目标域的传感器特性（如线束分布、扫描模式）仍需少量适配样本进行校准。

### 失败模式与局限性

本文坦诚展示了三类典型失败情况 (Figure 7, Figure 10)：

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/021_Figure_10.jpg]]
*Figure 10: Failure cases on waymo open dataset. Top: our model is unable to estimate accurate ego-motion and scene flow (b) if the background points consists only of the ground points after foreground removal (c). Bottom: rare objects such as trucks (top right corner in c and d) appear ambiguous to our model and cause prediction of the wrong masks (c)*

1. **背景仅剩地面点**：当前景移除后背景仅含地面点时，自运动估计因缺乏三维结构约束而失效。地面点近乎共面，退化了几何匹配的自由度，导致自运动沿某些方向不可观。这是“刚性假设”在极端稀疏场景下的结构性盲区。

2. **罕见对象掩码错误**：稀有类别（如卡车、柱状物）因训练数据中样本不足，前景/背景分割头易产生误判。Figure 7 底部案例中，路中柱体被误标为前景，导致其流向量与真实背景运动不一致。

3. **密集交互场景**：DBSCAN 依赖对象间存在空间间隙，当车辆紧密并排或部分遮挡时，聚类可能合并多个实例或错误切分，使刚性损失施加于非单一对象的点集上，产生平均化后的错误变换。

4. **标注噪声干扰**：lidarKITTI 的 GT 标注在对象边界处存在噪声，影响定量评估的精确性。论文通过报告中位 EPE 和基于预测掩码的分区域指标来缓解此问题。

### 开放问题

- 多帧时序信息的融合能否进一步提升运动估计的时序一致性与长程精度？
- 如何处理背景仅含地面点的退化场景——引入惯性测量或路面平面约束是否可行？
- 对罕见对象的掩码估计，能否通过少样本学习或合成数据增强来改善？
- 测试时 ICP 优化的计算开销较大，能否通过网络预测的初始化变换近似或学习式优化器加速，以满足自动驾驶的实时性需求？
- 若引入更强大的实例分割模块替代简单 DBSCAN，在密集交互场景下能否获得显著增益？当前实验 (Table 10) 中 GT 实例掩码并未带来明显提升，暗示瓶颈可能不在聚类本身，而在于网络对对象边界的特征判别力。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/014_Table_9.jpg]]
*Table 9: Comparison of the model fine-tuned on waymo open with the model trained only on semantiKITTI (generalization), on the waymo open dataset. Fine-tuned model outperforms the directly generalized one in terms of FG precision and ego-motion error*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/007_Table_4.jpg]]
*Table 4: Comparison of our full pipeline with specialized networks for BG segmentation and ego-motion estimation, respectively. Note, we provide GT background masks to the ego-motion specialized network also in the test phase*

![[assets/figures/papers/paper_list_l31_https_arxiv_org_abs_2102_08945/figures/008_Table_3.jpg]]
*Table 3: Ablation study of the proposed training objective. All models are trained on semanticKITTI and evaluated without test-time optimization on lidarKITTI (with ground) dataset*

## 方法谱系与知识库定位

### 核心定位：弱监督刚性场景流

本文提出的 **Rigid3DSceneFlow** 在三维场景流估计领域占据了一个独特的“弱监督”生态位，其核心定位可通过三个关键“插槽变更”来刻画：

1. **监督信号降级**：全监督基线（如 **FlowNet3D** 、**PointPWC-Net** 、**FLOT** ）依赖密集的逐点场景流真值，标注成本极高且易出错。本方法将监督信号降级为前景/背景二值掩码和自运动信息，大幅降低了标注门槛。
2.  **运动表征结构化**：基线方法通常预测无约束的逐点流向量，导致物体可能发生非物理形变。本方法将运动表征结构化为每个对象聚类的刚性变换参数，强制输出物理上可解释的刚性运动。
3.  **训练数据域迁移**：全监督方法通常在合成数据集（如 FlyingThings3D）上训练，面临严重的域间隙问题。本方法直接在真实 LiDAR 数据（semanticKITTI）上训练，从根本上避免了合成到真实的泛化难题。

这种定位使该方法兼具全监督的性能优势与无监督的标注经济性，正如 **Figure 2** 所示，实现了“两全其美”。

### 与全监督基线的定量关系

在 **lidarKITTI** 基准上，弱监督的 Ours++ 取得了 **EPE3D = 0.094 m**（无地面），相较于全监督的 **PointPWC-Net** 的 0.390 m，误差降低约 **0.3 m**（Table 2）。在 **stereoKITTI**（含地面）上，Ours++ 的 **EPE3D = 0.068 m** 甚至超越了全监督的 **FlowNet3D**（0.177 m）和 **HPLFlowNet**（0.116 m），证明了弱监督范式在真实数据上的竞争力（Table 5）。

在全监督设定下，本方法同样具有优势：在 **stereoKITTI**（无地面）上，全监督 Ours 的 **EPE3D = 0.042 m**，优于 **FLOT**（0.056 m）和 **PointPWC-Net**（0.058 m）（Table 1）。

### 方法谱系中的位置与适用边界

#### 刚性假设的合理性与局限

本方法的核心归纳偏置是**对象级刚性假设**——将动态场景分解为刚性移动的物体。这一假设在自动驾驶场景（车辆、行人等）中高度合理，也是方法成功的关键。然而，它划定了明确的适用边界：

-   **非刚性运动失效**：对于行人肢体摆动、旗帜飘动等非刚性运动，单一刚性变换无法准确描述。
-   **密集交互场景挑战**：前景聚类依赖 DBSCAN 算法，假设对象在空间上相互分离。当车辆密集交互、点云相互渗透时，聚类可能将多个对象合并或错误分割。

#### 弱监督信号的依赖

方法并非完全无监督，仍需以下弱标注：

-   **前景/背景二值掩码**：用于训练背景分割头。
-   **自运动信息**：用于监督自运动估计头。

当背景仅剩地面点时（如移除所有前景后），自运动估计可能失败（见 **Figure 10** 顶部失败案例）。这一退化场景是方法的一个已知脆弱点。

#### 罕见对象的泛化能力

模型对训练数据中罕见的对象（如卡车）的掩码预测不可靠（见 **Figure 10** 底部失败案例）。在 **Waymo Open** 数据集上微调后，前景召回率提升超过 20 个百分点，RTE 降低 2 cm（Table 9），表明域内微调是缓解此问题的有效策略。

### 消融证据：关键设计的作用

消融实验揭示了各组件的重要性：

| 消融配置 | EPE3D [m] | 关键发现 |
| :--- | :--- | :--- |
| 完整目标 (Lego + LCD + Lrigid) | **0.134** | 最佳性能 |
| 仅 Lego | 0.599 | 性能崩溃，自运动与 Chamfer 损失至关重要 |
| 无 Sinkhorn 正则化 | 0.594 | 自运动估计严重退化 |
| DBSCAN 聚类 vs GT 实例掩码 | 0.097 vs 0.101 | 简单聚类接近 GT 实例掩码性能，无需实例标注 |

这些结果表明，**自运动损失、Chamfer 距离损失和刚性损失的联合优化**是方法有效性的基石，而 Sinkhorn 正则化对稳定自运动估计不可或缺。

### 局限与开放问题

#### 已知局限

1.  **标注依赖性**：需要前景/背景掩码和自运动弱标注，无法完全无监督。
2.  **聚类假设**：DBSCAN 假设对象空间分离，密集交互场景可能失效。
3.  **退化场景**：背景仅含地面点时自运动估计不可靠。
4.  **罕见对象**：对训练分布外的对象（如卡车）掩码预测不可靠。
5.  **标注噪声**：lidarKITTI 的 GT 标注存在边界噪声，影响定量评估的精确性。

#### 开放问题

1.  **多帧信息融合**：当前方法仅使用两帧，如何结合多帧信息提升时序一致性和精度？
2.  **退化场景鲁棒性**：如何有效处理背景仅含地面点的困难场景？
3.  **罕见对象检测**：如何改善对罕见对象的检测与掩码估计？
4.  **实时性优化**：测试时优化（ICP）能否通过近似或加速实现实时自动驾驶应用？
5.  **实例分割进阶**：更强大的实例分割模块（如基于学习的聚类）能否进一步提升性能？

### 知识库定位总结

本方法属于**弱监督三维场景流估计**，其核心贡献在于将**对象级刚性先验**显式编码进网络架构与损失函数，从而在仅需弱标注的条件下实现可解释、高性能的场景流估计。它在方法谱系中桥接了全监督方法（性能高但标注昂贵）与无监督方法（标注经济但性能受限）之间的鸿沟，为自动驾驶等实际部署场景提供了一种高性价比的解决方案。

## 原文 PDF

![[paperPDFs/CVPR_2021/Weakly_Supervised_Learning_of_Rigid_3D_Scene_Flow.pdf]]
