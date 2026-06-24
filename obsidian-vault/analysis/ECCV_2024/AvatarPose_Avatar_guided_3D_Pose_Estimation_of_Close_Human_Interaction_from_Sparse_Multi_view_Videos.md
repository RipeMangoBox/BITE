---
title: "AvatarPose: Avatar guided 3D Pose Estimation of Close Human Interaction from Sparse Multi view Videos"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/AvatarPose_Avatar_guided_3D_Pose_Estimation_of_Close_Human_Interaction_from_Sparse_Multi_view_Videos.pdf
aliases:
- AvatarPose
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 为每个个体重建个性化的隐式神经化身，并将其作为强先验。通过可微分渲染的直接颜色与剪影损失进行姿态优化，从而绕过2D关节检测瓶颈；同时引入碰撞损失避免人体穿透。
primary_logic: 带纹理的个性化化身不仅提供了丰富的几何与外观线索，还允许直接从像素级观测优化姿态，配合交替优化策略，在严重遮挡和接触场景下显著提升3D人体姿态估计的精度与鲁棒性。
claims:
- 重建每个个体的隐式神经化身，并利用其他作为强先验来优化姿态。
- 通过最小化颜色和剪影渲染损失直接优化姿态参数，而非依赖2D关节重投影误差。
- 引入碰撞损失，通过惩罚多个化身同时占据同一3D点来防止人体穿透。
- 姿态优化与化身重建在整体流程中交替进行。
---

# AvatarPose: Avatar guided 3D Pose Estimation of Close Human Interaction from Sparse Multi view Videos

> [!tip] 核心洞察
> 带纹理的个性化化身不仅提供了丰富的几何与外观线索，还允许直接从像素级观测优化姿态，配合交替优化策略，在严重遮挡和接触场景下显著提升3D人体姿态估计的精度与鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | AvatarPose：基于个体化隐式神经化身的紧密交互多人3D姿态估计 |
| 英文题名 | AvatarPose: Avatar guided 3D Pose Estimation of Close Human Interaction from Sparse Multi view Videos |
| 会议/期刊 | ECCV 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | AvatarPose |
| Dataset | Hi4D, CHI3D |

> [!tip] 效果简介
> - Hi4D (8 views) 上，MPJPE (mm) 32.10 vs 42.63 (MVPose) (-10.53)；PCP high vs lower (outperforms all)。
> - CHI3D (4 views) 上，MPJPE (mm) 32.98 vs N/A (best baseline) (significantly lower)；PCP (mm) high vs lower (outperforms)。

## 概述

### 问题瓶颈

从多视角视频中估计多个紧密交互人体的3D姿态面临核心挑战：**严重的遮挡与身体接触**导致2D关节检测噪声大甚至完全缺失，使得依赖2D检测作为中间表示的现有方法性能急剧下降。无论是基于Transformer的多视角回归方法（**MvP**, Wang et al., NeurIPS 2021）、基于图神经网络的方法（**Graph**, Wu et al., ICCV 2021），还是基于体素特征的方法（**Faster VoxelPose**, Ye et al., ECCV 2022），在人体紧密接触场景下均难以准确恢复3D姿态。

### 核心方法定位

**AvatarPose**提出了一条绕过2D关节检测瓶颈的新路径：**为场景中每个个体重建带纹理的个性化隐式神经化身，并将其作为强先验来直接优化3D姿态**。该方法的关键创新在于：

- **用像素级渲染损失替代2D关节重投影损失**：通过最小化化身渲染图像与真实多视角图像之间的颜色损失和剪影损失来优化SMPL姿态参数，而非依赖不可靠的2D关键点检测。
- **引入碰撞损失防止人体穿透**：通过惩罚多个化身在3D空间中同时占据同一采样点的密度积，有效避免紧密接触时的人体表面穿透。
- **采用交替优化策略**：在化身学习与姿态优化之间交替迭代，避免联合优化在接触区域产生伪影并导致姿态估计错误。

方法在表示层面，为每个个体构建基于Instant-NGP加速的隐式神经辐射场，结合SMPL参数化模型实现形状感知的关节变形，并通过分层体积渲染合成多人体场景。

### 主要结果

在紧密交互数据集**Hi4D**（8视角）上，AvatarPose的MPJPE达到32.10 mm，相比此前最优方法**MVPose**（Dong et al., CVPR 2019）的42.63 mm降低了10.53 mm（约24.7%）；在**CHI3D**（4视角）上，MPJPE为32.98 mm，显著优于所有对比方法。消融实验证实：移除RGB渲染损失会使MPJPE从29.37 mm飙升至78.40 mm；采用联合优化而非交替优化则导致MPJPE升至66.04 mm，验证了各设计组件的必要性。定性结果显示，AvatarPose在手臂交缠、拥抱等紧密接触场景下能准确恢复姿态，而现有方法常出现肢体错位或穿透。

## 背景与动机

### 问题背景：紧密交互场景中的人体姿态估计

从多视角视频中估计多人的三维姿态与形状是计算机视觉中的一项基础任务，在运动捕捉、AR/VR、人机交互等领域具有广泛应用。然而，当场景中的人体发生**紧密交互**（如拥抱、握手、格斗等）时，该任务面临根本性的困难：严重的**遮挡**与**身体接触**导致二维关节检测器产生大量噪声或完全缺失，进而使得依赖2D检测作为中间表示的现有方法性能急剧下降。这一瓶颈构成了本工作的核心问题锚点。

### 现有方法的局限

当前主流的多视角多人姿态估计方法大致可分为两类。一类方法直接从多视角图像回归三维关节位置，例如基于Transformer的**MvP**（Wang et al., NeurIPS 2021）、基于图神经网络的**Graph**（Wu et al., ICCV 2021）以及基于体素特征的**Faster VoxelPose**（Ye et al., ECCV 2022）。这些方法虽然设计精巧，但其核心依赖仍是跨视角的2D关节检测或特征匹配——当2D观测因遮挡而不可靠时，回归结果会严重退化。另一类方法引入参数化人体模型（如SMPL）作为先验，例如**MVPose**（Dong et al., CVPR 2019）和**4DAssociation**（Zhang et al., CVPR 2020），但它们同样以2D关节重投影误差为主要优化目标，在紧密接触场景中难以规避2D噪声的传导。

概括而言，现有方法存在一个共同的**方法缺口**：它们将2D关节估计作为不可绕过的中间表示，而这一表示恰好在目标场景（紧密交互）中是最脆弱的环节。

### 本文动机：绕过2D瓶颈的个性化先验

本文的核心动机在于**绕过2D关节检测这一瓶颈**。关键思路是：如果能为场景中的每个个体重建一个**带纹理的个性化隐式神经化身**，并将其作为强先验，那么姿态优化就可以直接建立在像素级观测（颜色与剪影）之上，而非依赖有噪声的2D关节坐标。

这一动机建立在以下因果链条之上：

1. **个性化化身**不仅编码了人体的几何形状，还保留了外观纹理信息，提供了比SMPL裸网格丰富得多的约束信号。
2. 借助**可微分渲染**，可以从当前姿态假设直接合成多视角图像，并与真实观测在颜色和剪影层面进行比较，形成端到端的像素级优化目标。
3. 在此基础上，可以引入**碰撞损失**来显式惩罚多人体在三维空间中的穿透，解决紧密接触场景特有的身体交叉问题。
4. 通过**交替优化**策略——先学习化身、再固定化身优化姿态、最后进一步细化化身——可以在严重遮挡下逐步收敛到准确的姿态估计。

简言之，AvatarPose的方法论动机是：**用个性化神经化身的渲染一致性替代2D关节检测的几何一致性，从而在紧密交互这一极端场景中实现鲁棒的三维姿态估计。**

## 核心创新

AvatarPose 的核心创新在于**将个性化隐式神经化身作为强先验引入多人3D姿态估计**，从而绕过紧密交互场景下2D关节检测不可靠的根本瓶颈。与现有方法直接依赖2D关节重投影误差或特征匹配损失不同，AvatarPose 通过三个关键设计实现了方法范式的转变。

### 1. 从2D关节约束到像素级渲染损失的姿态优化

传统多视角多人姿态估计方法（如 **MvP**（Wang et al., NeurIPS 2021）、**Graph**（Wu et al., ICCV 2021）、**Faster VoxelPose**（Ye et al., ECCV 2022））的核心优化目标建立在2D关节检测之上。当人体紧密接触、严重遮挡时，2D关键点检测噪声大甚至完全缺失，导致3D姿态估计性能急剧下降。

AvatarPose 改变了这一范式：**直接通过最小化颜色渲染损失与剪影渲染损失来优化SMPL姿态参数**，而无需依赖任何2D关节中间表示。具体而言，给定已学习好的个性化化身模型（固定网络参数），优化器通过可微分渲染将化身投影到各视角图像，并与真实像素颜色和SAM-Track提取的前景掩码进行比较。姿态优化的总目标函数为：

$$\mathcal { L } ( \pmb { \Theta } ) = \lambda _ { R G B } \mathcal { L } _ { R G B } ( \pmb { \Theta } ) + \lambda _ { \alpha } \mathcal { L } _ { \alpha } ( \pmb { \Theta } ) + \lambda _ { r e g } \mathcal { L } _ { r e g } ( \pmb { \Theta } ) + \lambda _ { p a } \mathcal { L } _ { p a } ( \pmb { \Theta } )$$

这一设计使得姿态优化可以利用像素级的稠密外观与几何线索，而非稀疏且易受遮挡影响的关节坐标。消融实验充分验证了该创新的决定性作用：**移除RGB渲染损失后，MPJPE从29.37 mm飙升至78.40 mm**（Table 3），说明颜色一致性约束是姿态优化的核心驱动力；移除剪影损失后MPJPE也上升至31.00 mm。

### 2. 个性化隐式化身：超越SMPL的强先验

现有方法通常仅使用SMPL网格或骨架作为人体表示（如 **MVPose**（Dong et al., CVPR 2019）），这仅提供了几何先验，缺乏外观信息。AvatarPose 为场景中每个个体重建一个**带纹理的隐式神经辐射场**：在规范空间中，使用基于哈希表的多尺度特征网格（Instant-NGP架构）表示颜色与密度场，并通过SMPL驱动的形状感知关节变形将采样点从姿态空间映射到规范空间进行查询：

$$\mathbf { c } _ { i } , \sigma _ { i } = \bar { \mathbf { F } } _ { \sigma _ { f } } ^ { ( l ) } ( \bar { \mathbf { x } } _ { i } ( \mathbf { x } _ { i } , \mathbf { \Theta } ^ { ( l ) } ) )$$

这种个性化化身不仅编码了个体的体型与外观，还隐式地捕获了衣物等与SMPL裸模型不一致的细节。消融实验对比了仅使用SMPL拟合（无化身先验）的方案：**SMPL拟合的MPJPE为40.41 mm，而完整方法降至29.37 mm**（Table 3）。图5进一步定性展示了差异：仅拟合SMPL时，紧密接触的手臂关节估计错误，甚至导致身体表面相交；而个性化化身先验则能准确估计接触区域的姿态。

### 3. 碰撞损失与交替优化策略

紧密交互场景下，多人身体穿透是现有方法普遍存在的失效模式。AvatarPose 引入**穿透感知碰撞损失**，通过惩罚两个化身在3D空间中同一采样点的密度积来避免穿透：

$$\mathcal { L } _ { p a } ( \boldsymbol { \Theta } ) = \frac { 1 } { \mid S \mid } \sum _ { \mathbf { x } _ { i } \in S } \alpha _ { i } ^ { ( p ) } ( \boldsymbol { \Theta } ) \alpha _ { i } ^ { ( q ) } ( \boldsymbol { \Theta } )$$

该损失直接作用于体渲染的密度场，而非仅约束SMPL网格表面，因此在衣物等偏离裸模型的情况下仍能有效防止穿透。图7的消融显示，移除碰撞损失后，化身和底层SMPL身体均出现表面碰撞。

此外，AvatarPose 采用**交替优化**而非联合优化：先学习化身，再固定化身优化姿态，最后进一步细化化身。消融实验表明，**联合优化（同时优化化身和姿态）导致MPJPE升至66.04 mm**（Table 3），因为接触区域的渲染伪影会反向污染姿态估计；而交替优化通过解耦两个子问题，避免了这一耦合退化（图6）。

### 创新总结

| 创新维度 | 传统方法 | AvatarPose |
|---------|---------|------------|
| 姿态优化目标 | 2D关节重投影误差 / 特征匹配损失 | 像素级颜色渲染损失 + 剪影损失 + 碰撞损失 |
| 人体先验 | SMPL裸模型（仅几何） | 个性化隐式神经化身（几何 + 外观纹理） |
| 优化模式 | 单阶段或联合优化 | 化身学习与姿态优化的交替迭代 |
| 穿透处理 | 通常无显式约束 | 密度场级别的碰撞损失 |

## 整体框架

AvatarPose 的整体流程围绕一个核心思想展开：**为场景中的每个个体重建带纹理的隐式神经化身，并将其作为强个性化先验来优化 3D 姿态**。这一设计直接回应了紧密交互场景下的根本瓶颈——严重的遮挡与身体接触导致 2D 关节检测噪声大或缺失，使得依赖 2D 检测的 3D 姿态估计方法性能急剧下降。通过从像素级观测直接优化姿态，AvatarPose 绕过了对 2D 关节检测的依赖，转而利用化身提供的丰富几何与外观线索。

整个 pipeline 由两个主要模块构成，并以交替优化的方式协同工作（Figure 2）：

![[assets/figures/papers/paper_list_l1757_AvatarPose_Avatar_guided_3D_Pose_Estimation_of_Close_Human_Interaction_f/figures/002_Figure_2.jpg]]
*Figure 2: Method Overview: Our method consists of two modules: (a) Multi-Avatar Prior Learning: Given the input multi-view images and estimated poses*

1. **多化身先验学习 (Multi-Avatar Prior Learning)**：给定多视角图像和初始姿态估计，为每个个体重建隐式神经化身。
2. **化身引导的姿态优化 (Avatar-guided Pose Optimization)**：固定学习到的化身模型，通过最小化颜色和剪影渲染损失直接优化姿态参数，同时引入碰撞损失防止人体穿透。

这两个模块并非一次性执行完毕，而是在整体流程中**交替进行多轮迭代**：先学习化身，再固定化身优化姿态，随后进一步细化化身。这种交替优化策略是 AvatarPose 区别于联合优化方法的关键设计——消融实验表明，联合优化（同时优化化身和姿态）会导致接触区域出现伪影，进而引发错误的姿态估计（MPJPE 从 29.37 升至 66.04），而交替优化能正确重建化身和姿态。

### 输入输出流

- **输入**：稀疏多视角视频（例如 Hi4D 的 8 个视角或 CHI3D 的 4 个视角），以及由现成 3D 人体姿态估计器提供的初始姿态提议。初始 3D 姿态被配准到 SMPL 参数化模型上，为后续化身学习和姿态优化提供起点。
- **输出**：场景中每个个体的精确 3D 姿态与形状参数（SMPL 参数），以及重建的个性化隐式神经化身。

### 关键模块关系

**多化身先验学习**模块为每个人体实例构建一个基于 Instant-NGP 加速的神经辐射场，该辐射场在规范空间（canonical space）中表示外观，并通过 SMPL 模型建模形状感知的关节变形。为了支持多人场景，AvatarPose 引入了**分层体积渲染 (Layered Volume Rendering)**：沿每条射线对所有人体的采样点进行排序和 alpha 合成，将多个化身的渲染结果合成为一幅图像，从而直接从多视角图像中学习所有化身模型。

**化身引导的姿态优化**模块则反过来利用已学习的化身作为先验。其优化目标由四项损失加权组成：

$$\mathcal { L } ( \pmb { \Theta } ) = \lambda _ { R G B } \mathcal { L } _ { R G B } ( \pmb { \Theta } ) + \lambda _ { \alpha } \mathcal { L } _ { \alpha } ( \pmb { \Theta } ) + \lambda _ { r e g } \mathcal { L } _ { r e g } ( \pmb { \Theta } ) + \lambda _ { p a } \mathcal { L } _ { p a } ( \pmb { \Theta } )$$

其中 RGB 颜色一致性损失和透明度（剪影）损失直接比较渲染结果与真实图像，正则项约束姿态合理性，而**穿透感知碰撞损失 (Penetration-aware Collision Loss)** 则通过惩罚两个化身在同一 3D 采样点上的密度积来防止人体穿透：

$$\mathcal { L } _ { p a } ( \boldsymbol { \Theta } ) = \frac { 1 } { \mid S \mid } \sum _ { \mathbf { x } _ { i } \in S } \alpha _ { i } ^ { ( p ) } ( \boldsymbol { \Theta } ) \alpha _ { i } ^ { ( q ) } ( \boldsymbol { \Theta } )$$

这种"先学习化身，再用化身优化姿态"的双向依赖关系，使得 AvatarPose 在严重遮挡和接触场景下能够显著提升 3D 人体姿态估计的精度与鲁棒性。

> **注意**：当前方法假设场景中人数已知且相对固定，且初始姿态估计的误差非常大时（例如方向完全相反），优化可能陷入局部最小值，提升效果有限。此外，化身模型目前未包含手部精细建模，这会影响握手、牵手等紧密交互场景的精度。

## 核心模块与公式推导

### 1. 多化身先验学习 (Multi-Avatar Prior Learning)

该方法首先为场景中的每个个体重建一个个性化的隐式神经化身。每个人体在规范空间中使用加速神经辐射场（基于 Instant-NGP 的哈希特征网格）表示，并通过 SMPL 参数化模型驱动形状感知的关节变形。

对于属于人体 $l$ 的采样点 $\mathbf{x}_i$，其颜色和密度由规范外观网络在对应规范点处查询得到：

$$
\mathbf{c}_i, \sigma_i = \bar{\mathbf{F}}_{\sigma_f}^{(l)}(\bar{\mathbf{x}}_i(\mathbf{x}_i, \mathbf{\Theta}^{(l)})) \tag{1}
$$

其中 $\bar{\mathbf{x}}_i$ 是通过逆 SMPL 变形将姿态空间点映射到规范空间的位置，$\mathbf{\Theta}^{(l)}$ 为第 $l$ 个人的 SMPL 参数。

沿射线 $\mathbf{r}$ 的像素颜色通过 alpha 合成计算：

$$
\hat{\mathbf{C}}(\mathbf{r}) = \sum_{i=1}^{N} \alpha_i \prod_{j < i} (1 - \alpha_j) \mathbf{c}_i, \quad \alpha_i = 1 - \exp(-\sigma_i \delta_i) \tag{2}
$$

其中 $\delta_i$ 为相邻采样点间距，$\alpha_i$ 为点 $i$ 的透明度。

为支持多人体场景的联合学习，引入分层体积渲染。每个人体实例对射线的遮挡贡献通过实例遮挡率衡量：

$$
\alpha^{(l)}(\mathbf{r}) = \sum_{i=1}^{N} \alpha_i \prod_{j < i} (1 - \alpha_j) m_i^{(l)} \tag{4}
$$

其中 $m_i^{(l)}$ 为独热身份掩码，指示采样点是否属于人体 $l$。

化身学习阶段的 RGB 颜色一致性损失采用 Huber 损失：

$$
\mathcal{L}_{RGB} = \frac{1}{|\mathcal{R}|} \sum_{r \in \mathcal{R}} \rho(\|\hat{\mathbf{C}}(\mathbf{r}) - \mathbf{C}_{gt}(\mathbf{r})\|) \tag{5}
$$

同时使用 alpha 损失将渲染透明度与 SAM-Track 前景掩码对齐，提供剪影监督。

### 2. 化身引导的姿态优化 (Avatar-guided Pose Optimization)

在获得个性化化身后，固定化身模型参数，仅通过最小化渲染损失来优化姿态参数 $\mathbf{\Theta}$。姿态优化总目标为：

$$
\mathcal{L}(\mathbf{\Theta}) = \lambda_{RGB}\mathcal{L}_{RGB}(\mathbf{\Theta}) + \lambda_{\alpha}\mathcal{L}_{\alpha}(\mathbf{\Theta}) + \lambda_{reg}\mathcal{L}_{reg}(\mathbf{\Theta}) + \lambda_{pa}\mathcal{L}_{pa}(\mathbf{\Theta}) \tag{8}
$$

其中各项含义：
- $\mathcal{L}_{RGB}(\mathbf{\Theta})$：预测渲染颜色与真值图像的颜色一致性损失。
- $\mathcal{L}_{\alpha}(\mathbf{\Theta})$：渲染透明度与分割掩码的匹配损失。
- $\mathcal{L}_{reg}(\mathbf{\Theta})$：SMPL 姿态正则项，防止姿态偏离合理范围。
- $\mathcal{L}_{pa}(\mathbf{\Theta})$：穿透感知碰撞损失。

### 3. 穿透感知碰撞损失 (Penetration-aware Collision Loss)

为防止不同人体化身在 3D 空间中穿透，引入碰撞损失，惩罚两个化身在同一采样点同时具有高密度的情况：

$$
\mathcal{L}_{pa}(\mathbf{\Theta}) = \frac{1}{|S|} \sum_{\mathbf{x}_i \in S} \alpha_i^{(p)}(\mathbf{\Theta}) \alpha_i^{(q)}(\mathbf{\Theta}) \tag{12}
$$

其中 $S$ 为 3D 空间中的采样点集合，$\alpha_i^{(p)}$ 和 $\alpha_i^{(q)}$ 分别为人体 $p$ 和 $q$ 在点 $\mathbf{x}_i$ 处的透明度。当两点密度积较大时，表明两个化身在同一位置重叠，损失值增大，从而推动姿态调整以避免穿透。

### 4. 交替优化策略 (Alternating Optimization)

整个流程采用交替优化而非联合优化：先学习化身模型，再固定化身优化姿态，最后进一步细化化身。此策略循环 $N$ 步，关键优势在于避免了联合优化中接触区域产生伪影并导致姿态估计错误的问题——消融实验证实，联合优化的 MPJPE 升至 66.04 mm，而交替优化仅为 29.37 mm。

## 实验与分析

### 核心性能对比

AvatarPose 在 Hi4D 和 CHI3D 两个紧密交互多人数据集上均显著超越现有方法。在 Hi4D（8 视角）上，AvatarPose 的 MPJPE 达到 **32.10 mm**，相比此前最佳方法 **MVPose**（Dong et al., CVPR 2019）的 42.63 mm 降低了 10.53 mm（Table 1）。在 CHI3D（4 视角）上，AvatarPose 的 MPJPE 为 **32.98 mm**，同样大幅优于所有基线（Table 2）。除 MPJPE 外，该方法在 PCP、AP_K 和 Recall 指标上也全面领先。

![[assets/figures/papers/paper_list_l1757_AvatarPose_Avatar_guided_3D_Pose_Estimation_of_Close_Human_Interaction_f/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparison with SotA on the Hi4D [67] Dataset (8 views). We compare our method with MvP [61], Graph [63], Faster VoxelPose [66], MVPose* [19], MVPose [18] and 4DAssociation [72]. We report MPJPE, PCP*

![[assets/figures/papers/paper_list_l1757_AvatarPose_Avatar_guided_3D_Pose_Estimation_of_Close_Human_Interaction_f/figures/005_Table_2.jpg]]
*Table 2: Quantitative Comparison with SotA on the CHI3D [25] Dataset (4 views). We compare our method with Faster VoxelPose [66], MVPose* [19], MV-Pose [18] and 4DAssociation [72]. We report MPJPE, PCP*

定性结果（Figure 3）进一步印证了 AvatarPose 在紧密接触场景下的优势：当两人身体发生拥抱、推搡等交互时，基线方法（如 **MvP**、**Graph**、**Faster VoxelPose**）常出现肢体交叉或关节错位，而 AvatarPose 能保持正确的相对位置和姿态。

![[assets/figures/papers/paper_list_l1757_AvatarPose_Avatar_guided_3D_Pose_Estimation_of_Close_Human_Interaction_f/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative Comparison with SotA methods [19,61,64,66,72] on Hi4D and CHI3D. We show two examples from the Hi4D and CHI3D datasets compared with Graph, MvP, Faster VoxelPose, MVPose, and 4DAssociation. For each example, we show 2D projections on two sampled views*

### 消融实验：各组件贡献

Table 3 和 Figure 5–7 系统验证了 AvatarPose 各关键设计的必要性：

![[assets/figures/papers/paper_list_l1757_AvatarPose_Avatar_guided_3D_Pose_Estimation_of_Close_Human_Interaction_f/figures/008_Table_3.jpg]]
*Table 3: Quantitative Ablation Results. Ablations to evaluate our method with only the SMPL fitted method, our method without RGB loss and without Silhouette loss, and our method without alternating optimization*

![[assets/figures/papers/paper_list_l1757_AvatarPose_Avatar_guided_3D_Pose_Estimation_of_Close_Human_Interaction_f/figures/007_Figure_5.jpg]]
*Figure 5: Comparison with SMPL Body Prior. Only fitting SMPL to 2D observations, some joints in close contact such as arms are incorrectly estimated and even cause intersections between body surfaces. In contrast, our personalized prior enables accurate estimation of poses*

**个性化化身先验 vs. 纯 SMPL 先验。** 仅使用 SMPL 拟合（无化身先验）时 MPJPE 为 40.41 mm，而完整方法降至 29.37 mm（Table 3）。Figure 5 显示，纯 SMPL 先验在手臂等接触部位会产生错误估计甚至表面交叉，而个性化化身先验能准确恢复紧密接触下的姿态。

**RGB 渲染损失的核心作用。** 移除 RGB 损失后 MPJPE 急剧上升至 78.40 mm（Table 3），表明颜色渲染损失是姿态优化的主导驱动力。相比之下，移除剪影损失仅使 MPJPE 略微上升至 31.00 mm，说明颜色信息比轮廓信息提供了更强的优化信号。

**交替优化 vs. 联合优化。** 采用联合优化（同时优化化身和姿态）时 MPJPE 升至 66.04 mm（Table 3）。Figure 6 揭示了原因：联合优化在接触区域产生渲染伪影，进而导致姿态估计错误；交替优化则先固定化身再优化姿态，避免了伪影-姿态的恶性循环。

**碰撞损失的必要性。** 移除碰撞损失后，化身表面和底层 SMPL 身体均出现穿透现象（Figure 7），验证了碰撞损失在防止多人交互中的空间重叠方面的关键作用。

### 失败模式与局限性

AvatarPose 在以下场景中存在性能退化：

- **初始姿态严重错误。** 当初始姿态估计方向完全相反或大部分关键点严重失准时，优化可能陷入局部最小值，提升效果有限。这是基于渲染损失的优化方法的固有局限——当初始解远离真实值时，梯度信号可能无法引导参数收敛到全局最优。
- **手部未建模。** 当前化身模型不包含手部精细结构，在握手、牵手等手部紧密交互场景中精度受限。论文指出整合手部参数化模型是未来方向。
- **计算开销。** 训练化身和交替优化总计约需 11 分钟，难以满足实时运动捕捉需求。如何利用更轻量的神经表示（如三平面/张量分解）加速是待探索的问题。
- **人数假设。** 当前方法假设场景中人数已知且相对固定，尚未扩展到人数动态变化的场景。

### 补充图表

![[assets/figures/papers/paper_list_l1757_AvatarPose_Avatar_guided_3D_Pose_Estimation_of_Close_Human_Interaction_f/figures/010_Figure_6.jpg]]
*Figure 6: Ablation of Alternating Optimization. We show the results of rendered avatars and projections of the estimated 3D poses. Joint optimization suffers from artifacts around the contact part and in turn causes wrong pose estimations. In contrast, ours reconstructs both avatars and poses correctly*

![[assets/figures/papers/paper_list_l1757_AvatarPose_Avatar_guided_3D_Pose_Estimation_of_Close_Human_Interaction_f/figures/009_Figure.jpg]]
*Figure: GT Joint Opt Alternating Opt*

## 方法谱系与知识库定位

### 方法对比与谱系定位

AvatarPose 处于多视角3D人体姿态估计与神经隐式表示重建的交叉点，其核心创新在于通过**个性化隐式神经化身**构建强先验，将姿态估计从依赖2D关节检测的范式转向基于像素级渲染损失的优化范式。

**与多视角多人姿态估计方法的对比。** 现有主流方法可大致分为两类：基于体素/图神经网络的特征匹配方法，以及结合SMPL参数化模型的优化方法。前者如 **MvP** (Wang et al., NeurIPS 2021) 采用Transformer直接回归多视角多人体姿态，**Graph** (Wu et al., ICCV 2021) 利用图神经网络进行跨视角特征聚合，**Faster VoxelPose** (Ye et al., ECCV 2022) 在体素空间中检测人体关键点。这些方法的共同瓶颈在于严重依赖2D关节检测器的精度——在紧密交互场景中，遮挡和身体接触导致2D关键点大量缺失或噪声极大，进而使3D估计性能急剧下降。后者如 **MVPose** (Dong et al., CVPR 2019) 和 **4DAssociation** (Zhang et al., CVPR 2020) 引入了SMPL参数化模型进行姿态细化，但其优化目标仍以2D关节重投影误差为核心，本质上未摆脱对2D检测的依赖。

AvatarPose 的方法论突破在于**改变了姿态优化的目标函数**：不再依赖2D关节重投影误差，而是利用学习到的个性化化身，通过最小化**颜色渲染损失**与**剪影损失**直接优化SMPL姿态参数。这一转变的根本优势在于：带纹理的隐式化身编码了丰富的几何与外观信息，即使2D关键点检测失败，像素级的颜色一致性约束仍能提供有效的优化信号。同时，引入**碰撞损失**惩罚多个化身密度场在同一3D点的重叠，有效防止紧密接触时的人体穿透。

**与神经化身重建方法的对比。** 在化身表示层面，AvatarPose 借鉴了 Instant-NGP 的哈希编码加速策略和 InstantAvatar 的SMPL变形场设计，但将其扩展为**多化身分层体积渲染**框架，支持同时学习场景中多个个体的隐式辐射场。与常见的联合优化化身与姿态的方法不同，AvatarPose 采用**交替优化**策略：先固定姿态学习化身，再固定化身优化姿态，最后进一步细化化身。消融实验表明，联合优化（同时优化化身和姿态）会导致接触区域产生严重伪影，MPJPE升至66.04 mm，而交替优化可将误差降至29.37 mm——这一机制性差异说明在紧密交互场景中，解耦化身先验学习与姿态优化对于避免优化过程相互干扰至关重要。

### 适用边界与局限

**初始姿态敏感性问题。** AvatarPose 的性能依赖于初始姿态估计的质量。当初始姿态误差极大（例如方向完全相反或大部分关节严重错位）时，基于渲染损失的优化可能陷入局部最小值，提升效果有限。这表明化身先验的引导能力受限于优化初始点的合理范围。

**手部建模缺失。** 当前化身模型未包含手部的精细几何与外观建模。在握手、牵手等紧密手部交互场景中，这一缺失会直接影响姿态估计精度。从方法架构看，整合手部参数化模型需要在规范空间中扩展辐射场的表示能力，同时不破坏现有的交替优化流程。

**运行时效率。** 化身训练和交替优化需要分钟级时间（论文报告约11分钟），远不能满足实时运动捕捉需求。这一瓶颈主要源于神经辐射场的逐点采样与体积渲染开销，以及多轮交替优化的迭代成本。

**场景假设。** 当前方法假设场景中人数已知且相对固定，未处理人数动态变化或未知的场景。分层体积渲染框架在理论上可扩展至可变人数，但需要相应的实例检测与跟踪机制。

### 开放问题

1. **鲁棒初始化策略。** 在初始姿态严重错误的情况下，能否通过更强的姿态先验（如基于物理的约束或运动学合理性惩罚）或更好的初始化策略（如多假设跟踪）来扩大优化收敛域？

2. **手部模型整合。** 如何在不变动整体交替优化流程的前提下无缝整合手部参数化模型（如MANO），使化身能够表示手部的精细几何与外观，从而提升握手、牵手等场景的姿态估计精度？

3. **动态人数扩展。** 分层体积渲染框架能否与在线实例检测/跟踪机制结合，处理人数动态变化或未知的开放场景？这需要解决化身模型的动态创建与销毁问题。

4. **轻量化加速。** 能否利用更轻量的神经表示（如三平面分解、张量分解或高斯泼溅）替代当前的哈希编码辐射场，在保持渲染质量的同时大幅加速化身学习和姿态优化，以满足实时运动捕捉需求？

## 原文 PDF

![[paperPDFs/ECCV_2024/AvatarPose_Avatar_guided_3D_Pose_Estimation_of_Close_Human_Interaction_from_Sparse_Multi_view_Videos.pdf]]