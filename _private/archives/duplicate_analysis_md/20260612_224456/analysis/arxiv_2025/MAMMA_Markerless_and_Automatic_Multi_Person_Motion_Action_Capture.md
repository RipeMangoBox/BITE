---
title: MAMMA Markerless and Automatic Multi Person Motion Action Capture
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/CVPR_2026/MAMMA_Markerless_Accurate_Multi_person_Motion_Acquisition.pdf
aliases:
- MMAMPMAC
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 基于Transformer的密集地标检测器 MammaNet，为每个地标学习独立的可学习查询（landmark queries），并结合 SAM2 分割掩码作为条件输入，同时预测可见性、不确定性、人物-人物接触与地面接触，从而在强遮挡下依然能获得准确的个体地标与跨视角匹配。
primary_logic: 通过为每个地标设计独立的嵌入查询，交叉注意力能够自适应地匹配最相关的图像区域，自注意力则学习地标间的空间关系；配合掩码条件化与多任务预测（可见性/不确定性/接触），网络在复杂多人场景中仍能准确、鲁棒地定位全身密集地标。
claims:
- "MammaNet 在单人及双人密集地标预测任务上均显著优于 Look-Ma* 和 CameraHMR，尤其在 SAM2 掩码辅助下，双人场景误差大幅降低（Harmony4D: 31.96→18.33 px）。"
- "基于 MAMMA 的 3D 拟合在多个数据集上取得最优 MPJPE/PVE，大幅超越其他学术方法（如 RICH: MAMMA-C MPJPE 22.20，Look-Ma* 39.52）。"
- 与 Vicon 标记系统对比，MAMMA 在未见过的 37 个额外标记上的平均误差仅比标记方法高 0.862 mm，视觉质量几乎无差别。
- 网络预测的人物-人物接触与地面接触 AUC 均超过 90%，证明接触预测高度可靠。
---

# MAMMA Markerless and Automatic Multi Person Motion Action Capture

> [!tip] 核心洞察
> 通过为每个地标设计独立的嵌入查询，交叉注意力能够自适应地匹配最相关的图像区域，自注意力则学习地标间的空间关系；配合掩码条件化与多任务预测（可见性/不确定性/接触），网络在复杂多人场景中仍能准确、鲁棒地定位全身密集地标。

| 字段 | 内容 |
|------|------|
| 中文题名 | MAMMA：无标记精确多人运动采集 |
| 英文题名 | MAMMA Markerless and Automatic Multi Person Motion Action Capture |
| 会议/期刊 | arXiv 2025 |
| Links |  [paper](https://arxiv.org/abs/2506.13040)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MAMMA |
| Dataset | RICH, MammaEval-Extra, Harmony4D |

> [!tip] 效果简介
> - RICH (single-person 3D fitting) 上，MPJPE (mm) 22.20 vs 39.52 (Look-Ma*) (-17.32)。
> - MammaEval-Extra (held-out 37 Vicon markers) 上，mean per-marker distance (mm) 22.48 vs 21.62 (MoSh++ on 73 markers) (0.86)。
> - RICH (2D dense landmark error) 上，mean 2D Euclidean distance (px) 8.55 vs 13.26 (Look-Ma*) (-4.71)。

## 概述

无标记多人运动采集的核心瓶颈在于：当多人紧密交互、发生严重遮挡和复杂身体接触时，传统方法难以准确恢复个体的3D人体网格。根本原因有二：一是缺乏在密集表面地标上的鲁棒检测能力，二是跨视角对应关系在遮挡下极易断裂。MAMMA 针对这一瓶颈，提出了一套**“密集地标检测—跨视角匹配—无先验优化”**的两阶段框架，在不依赖姿态回归网络或强运动先验的前提下，实现了逼近商业标记系统（Vicon）的采集精度。

**核心方法定位。** MAMMA 的关键创新集中在第一阶段的密集地标检测器 **MammaNet** 上。与以往使用单一可学习令牌回归所有地标的方法（如 CameraHMR）不同，MammaNet 为每个地标分配独立的可学习查询（landmark queries），通过交叉注意力自适应匹配图像中最相关的区域，同时利用自注意力学习地标间的空间结构关系。此外，网络以 SAM2 分割掩码作为条件输入，并同时预测每个地标的可见性、不确定性、人物-人物接触概率和地面接触概率。这一设计使得即使在严重遮挡下，网络依然能输出准确的个体地标位置及其置信度，为后续跨视角匹配和3D优化提供了高质量、信息丰富的观测信号。

第二阶段的模型拟合同样打破了常规：MAMMA **不使用任何回归网络来初始化姿态和体型**，而是通过最小化密集地标的重投影误差，直接从多视角2D观测中优化 SMPL-X 参数。优化过程中，预测的不确定性被动态更新以抑制离群地标的影响，接触概率则驱动基于 SDF 的排斥/吸引项，有效减少人物间的穿透并实现合理的物理接触。

**关键实证结果。** 实验证据表明，MAMMA 在多个维度上实现了显著突破：

- **2D 地标精度**：在单人场景（RICH）上，MammaNet 的密集地标误差为 8.55 px，较 Look-Ma* 的 13.26 px 降低 35.5%；在双人交互场景（Harmony4D）上，配合 SAM2 掩码后误差从 31.96 px 降至 18.33 px，降幅达 42.7%（Table 1、Table 2）。
- **3D 拟合精度**：在 RICH 数据集上，MAMMA-C 的 MPJPE 为 22.20 mm，而对比方法 Look-Ma* 为 39.52 mm，性能提升超过 40%（Table 4）。
- **与标记系统的对比**：在未见过的 37 个额外 Vicon 标记上，MAMMA 的平均每标记误差仅比标记方法 MoSh++ 高 0.862 mm，视觉质量几乎无差别（Table 10）。
- **接触预测可靠性**：人物-人物接触与地面接触预测的 AUC 均超过 90%（Figure 6），为优化阶段的物理合理性提供了可靠先验。

**方法谱系与知识库定位。** MAMMA 处于无标记多视角人体运动采集的前沿，其方法设计融合了多个技术脉络：在密集地标检测上，它超越了以 CNN 直接回归为代表的 **Look-Ma*** 和以单一可学习令牌为代表的 **CameraHMR**；在3D拟合上，它区别于依赖姿态先验的 **SMPLify-X（多视角版）** 和基于轮廓对齐的 **Harmony4D**。通过将 Transformer 解码器与 SAM2 分割先验结合，并引入接触感知的多任务学习，MAMMA 在密集地标检测这一关键子问题上建立了新的技术基线，同时证明了“纯优化+密集地标”路线可以替代“回归初始化+稀疏关键点”的传统范式。

## 背景与动机

人体运动捕捉是计算机视觉与图形学的核心问题，其应用覆盖电影特效、运动分析、虚拟现实与人机交互等领域。传统上，基于光学标记（如 Vicon）的商业系统通过在被试身体表面粘贴高反光标记球，利用多相机红外追踪实现亚毫米级精度，长期被视为动捕的“金标准”。然而，这类系统存在固有缺陷：标记粘贴过程繁琐、对服装和皮肤敏感、在多人紧密交互时标记易被遮挡或脱落，且设备成本高昂、部署环境受限。

无标记运动捕捉（markerless motion capture）旨在摆脱物理标记的束缚，直接从多视角视频中恢复人体的三维姿态与形状。近年来，参数化人体模型（如 SMPL、SMPL-X）的成熟与深度学习的发展，使无标记动捕取得了长足进步。主流方法通常遵循两条技术路线：其一是基于回归的方法，直接从图像推断模型参数；其二是基于优化的方法，通过最小化二维关键点或轮廓的重投影误差来拟合模型参数。

然而，**传统无标记动捕方法在多人紧密交互、严重遮挡和复杂接触场景下仍面临根本性瓶颈**。具体表现为三个方面：

**第一，缺乏密集、鲁棒的表面地标检测与跨视角对应。** 现有方法大多依赖稀疏的二维关节关键点（如 OpenPose 的 25 个关节点），或使用单一可学习嵌入来预测所有地标（如 CameraHMR）。这类稀疏或非特异性的表示在遮挡发生时极易丢失关键信息，且难以建立跨视角的精确对应关系，导致多人场景下的三维重建精度急剧下降。

**第二，对姿态先验与回归初始化的过度依赖。** 许多方法需要借助回归网络提供初始姿态和形状估计，再通过优化进一步精修。这种依赖不仅引入了额外的计算开销和误差累积，更在极端姿态（如瑜伽动作）或训练数据未见过的交互模式下表现脆弱。

**第三，接触建模与穿透抑制能力不足。** 在双人拥抱、握手等紧密交互场景中，现有方法难以准确判断人体间的接触状态，导致重建结果出现严重的网格穿透（interpenetration）或虚假间隙（floating），破坏了物理真实感。

针对上述缺口，本文提出 **MAMMA（Markerless Accurate Multi-person Motion Acquisition）**，一种从多视角同步视频中精确恢复多人三维姿态与形状的无标记动捕框架。MAMMA 的核心动机在于：**将无标记动捕问题重新建模为“虚拟标记”的检测与拟合问题**——首先在每台相机的视图中预测一组密集的、具有语义一致性的二维表面地标，然后通过最小化这些地标的重投影误差来优化 SMPL-X 模型参数。这一思路直接对标传统标记系统的精度优势，同时保留了无标记方法的灵活性与可扩展性。

## 核心创新

MAMMA 的核心创新并非简单地将密集地标检测与多视图优化拼接，而是通过**为每个地标赋予独立可学习的身份查询（landmark queries）**，将“在哪里检测”与“检测什么”解耦，从根本上改变了密集地标检测的表示范式。这一设计构成了整个系统的因果杠杆，驱动了后续所有性能增益。

### 从“通用回归”到“身份感知查询”的范式转换

传统密集地标检测方法存在根本性的表示瓶颈。**Look-Ma\***（Hewitt et al. 的重新实现）采用 CNN 直接回归所有地标坐标，每个地标仅由输出特征图上的一个位置隐式表示，缺乏显式的身份建模。**CameraHMR** 虽然引入了 Transformer 架构，但仅使用**单个可学习嵌入**解码所有地标，迫使网络将不同地标的定位信息压缩到同一个查询向量中。这两种方案在面对多人紧密交互和严重遮挡时，地标身份混淆和定位漂移成为系统性的失败模式。

MAMMA 的 **MammaNet** 彻底改变了这一局面。其核心机制是为 N=512 个表面地标分别学习独立的嵌入向量（landmark queries），每个查询在 Transformer 解码器中通过两个关键注意力机制完成精准定位：

- **交叉注意力（Cross-Attention）**：每个 landmark query 自适应地从 ViT-Base 提取的图像 patch 特征中检索最相关的空间区域，实现“每个地标知道自己该看哪里”。
- **自注意力（Self-Attention）**：512 个 landmark queries 之间相互通信，学习地标间的空间拓扑关系（如手肘与手腕的几何约束），形成全局一致的地标布局。

这一设计使得即使在严重遮挡下，可见地标的查询仍能通过自注意力从可见区域的上下文中推断被遮挡地标的合理位置，而非像传统方法那样产生随机漂移。

### 掩码条件化：将分割先验注入特征空间

MammaNet 的第二个关键创新是将 **SAM2 实例分割掩码**作为条件输入，与图像特征在特征空间进行**逐元素求和**融合。这与简单的“先检测人再裁图”策略有本质区别：掩码信息直接参与特征提取过程，使网络能够区分不同个体并抑制背景干扰。

消融实验揭示了这一设计的因果效应（Table 1, Table 2）：
- **单人场景**：掩码条件化带来的增益有限（如 RICH 数据集上仅从 8.55→8.55 px），因为单人场景中个体定位本身已相对容易。
- **双人交互场景**：掩码条件化成为决定性因素。在 Harmony4D 数据集上，误差从 31.96 px 骤降至 18.33 px（降幅 42.6%）；在 CHI3D 上从 6.22 px 降至 4.36 px（降幅 29.9%）。这表明当两人紧密交互、边界模糊时，SAM2 的分割先验为 landmark queries 提供了关键的个体归属信号，有效防止了跨个体的地标混淆。

### 多任务预测：可见性、不确定性与接触的联合学习

MammaNet 在每个 landmark query 之上并行预测四个关键属性，形成对优化阶段的完整信息供给：

1. **可见性概率 $p_i$**：显式建模地标是否被遮挡，使优化阶段能够自动忽略不可见地标，而非将其强行拟合到错误位置。
2. **不确定性 $\sigma_i$**：预测每个地标定位的置信度，在重投影误差能量中作为自适应权重（见公式 $E_{\mathrm{ldmks}}$），使优化过程更信赖高置信度地标。
3. **人物-人物接触概率 $pc_i$** 与 **地面接触概率 $fl_i$**：这两个预测层是 MAMMA 能够处理物理交互的关键。ROC 曲线评估显示两种接触预测的 AUC 均超过 90%（Figure 6），证明网络能够可靠地判断哪些顶点处于接触状态。

这些预测的联合学习形成了一个闭环：**可见性决定是否使用该地标，不确定性决定使用的权重，接触概率引导物理合理性优化**。相比之下，CameraHMR 仅预测坐标和不确定性，缺乏可见性和接触建模，在遮挡和交互场景下必然产生不可靠的地标，进而污染优化过程。

### 免回归初始化的纯优化拟合

MAMMA 的第四项创新在于**完全放弃姿态回归网络进行初始化**。传统方法（如 CameraHMR、SMPLify-X 系列）通常依赖回归网络提供初始姿态和体型参数，这引入了两个问题：回归网络在极端姿态上的泛化误差会传播到优化阶段；回归初始化可能将优化引导至局部最优。

MAMMA 的替代方案极为简洁：将人体初始化为一个位于多相机射线交汇处的 3D 点，仅通过最小化密集地标重投影误差来驱动 SMPL-X 参数优化。这一设计的有效性依赖于前三个创新的协同作用——只有当密集地标本身足够准确、可见性和不确定性预测足够可靠时，纯优化才能收敛到正确解。实验证明，这种“从零开始”的策略不仅可行，而且在多个数据集上取得了最优的 MPJPE 和 PVE（Table 4），同时避免了对特定姿态先验的依赖，提升了泛化能力。

### 创新的协同效应

上述四个 changed slots 并非孤立改进，而是形成了因果链条：**独立 landmark queries** 提供了准确的 2D 定位能力，**掩码条件化**在多人场景中保证了地标的个体归属正确性，**多任务预测**为优化提供了信息充分的误差信号，**免回归初始化**则将前三个模块的精度优势无损地传递到 3D 拟合阶段。这一链条的断裂点（如移除掩码或使用单一查询）会在实验中表现为特定场景（双人交互、极端姿态）的性能骤降，验证了每个创新在系统中的不可替代性。

## 整体框架

MAMMA 采用**两阶段流水线**：首先在所有相机视图中估计密集的 2D 表面地标（虚拟标记），然后求解最优 SMPL-X 人体模型以拟合这些地标。该方法不依赖姿态先验或回归网络进行姿态初始化，而是通过最小化地标重投影误差直接优化 SMPL-X 参数。

### 输入与预处理

系统输入为**同步多视角视频**。对于每一帧，SAM2 负责实例分割与跨帧时序跟踪，为每个被跟踪的人物生成分割掩码。这些掩码随后作为条件信号馈入地标检测网络。

### 阶段一：密集 2D 地标检测（MammaNet）

MammaNet 是该方法的核心检测器，其架构由 **ViT-Base 图像特征提取器**、一个额外的 **CNN 掩码处理分支**以及一个 **Transformer 解码器**组成（Figure 4）。掩码特征与图像特征通过逐元素求和进行融合，实现掩码条件化。

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/004_Figure_4.jpg]]
*Figure 4: MammaNet. The input to the network is the image and mask. It predicts per landmark visibility probability p (green is visible, red not visible), landmark locations µ, uncertainties σ (red means highly uncertain), person–person pc and floor contact f l probabilities (red means no contact and green contact)*

解码器采用 **N=512 个可学习的地标查询（landmark queries）**，每个查询对应一个预定义的 SMPL-X 表面地标。通过交叉注意力机制，每个查询自适应地关注图像中最相关的区域；自注意力则建模地标之间的空间关系。对于每个地标，网络同时预测：
- 2D 像素坐标 $\mu_i = [x_i, y_i]$
- 可见性概率 $p_i$
- 不确定性 $\sigma_i$
- 人物-人物接触概率 $pc_i$
- 地面接触概率 $fl_i$

这一多任务设计使得网络在严重遮挡和紧密交互场景下仍能鲁棒地定位全身密集地标。

### 跨视角多人匹配

对于每个被 SAM2 跟踪的人物，MammaNet 独立预测其在各视角下的密集地标。跨视角人物匹配通过计算**对称极线距离** $D_g$（Equation 2）来衡量两组地标之间的几何亲和度，并使用匈牙利算法形成循环一致的人物分组。这确保了同一人物在不同相机视图中的地标被正确关联。

### 阶段二：SMPL-X 模型拟合

给定跨视角匹配后的 2D 地标观测，通过 L-BFGS 优化器分阶段求解 SMPL-X 参数。总能量函数包含四项：

$$E(\Phi; \{\mathbf{Q}\}, \{\mathbf{L}\}) = E_{\mathrm{ldmks}} + E_{\mathrm{shape}} + E_{\mathrm{temp}} + E_{\mathrm{cont}}$$

其中 $E_{\mathrm{ldmks}}$ 是**加权重投影误差**（Equation 1），利用预测的可见性 $p$ 和不确定性 $\sigma$ 进行加权，使优化更信赖高置信度地标。优化过程中，不确定性根据当前残差动态更新（$\sigma_i' = \sigma_i \cdot \min(\max(e_i/\tau, 0), 1)$，$\tau=10$ px），进一步抑制异常值的影响。

接触能量项 $E_{\mathrm{cont}}$ 包含基于 SDF 的**排斥项** $E_p$（惩罚穿入他人身体的顶点）和**吸引项** $E_c$（将预测接触概率高的顶点拉向对方表面），通过自定义 CUDA 核高效计算，有效减少穿透并实现合理的物理接触。

### 关键设计要点

- **无回归初始化**：人体初始位置通过最小化各相机中心射线距离确定，无需任何姿态或形状回归网络。
- **掩码条件化**：SAM2 分割掩码作为额外输入显著提升了多人遮挡场景的地标精度（Harmony4D 双人误差从 31.96 px 降至 18.33 px）。
- **分阶段优化**：S2（姿态/形状/平移）已提供良好的精度-效率折衷；S3（不确定性更新）和 S4（接触约束）进一步精修细节并抑制穿透。

## 核心模块与公式推导

### 密集地标检测器 MammaNet

MammaNet 是整套方法的前端核心，负责从单张 RGB 图像中预测全身 512 个密集表面地标的 2D 位置、可见性、不确定性以及接触概率。其架构由两个主干组成：**ViT-Base** 提取图像特征，一个额外的 **CNN** 处理 SAM2 分割掩码，两者通过逐元素求和融合，实现掩码条件化（Figure 4）。

解码端采用 **Transformer 解码器**，关键创新在于为每个地标学习一个独立的可学习嵌入（landmark query），共 N=512 个查询向量。交叉注意力使每个查询自适应地关注图像中最相关的区域，自注意力则建模地标之间的空间关系。这种“一地标一查询”的机制从根本上区别于 CameraHMR 的单学习令牌方案和 Look-Ma* 的 CNN 直接回归方案。

每个地标查询经线性层输出五类信息：
- **地标坐标** $\mu_i = [x_i, y_i]$，即预测的像素位置；
- **可见性概率** $p_i$，指示该地标在当前视图中是否可见；
- **不确定性** $\sigma_i$，反映预测的置信度；
- **人物-人物接触概率** $pc_i$；
- **地面接触概率** $fl_i$。

接触预测分支是专门为多人交互场景引入的，网络在 MammaSyn 数据集上重新训练时添加了这两个分支。ROC 评估显示两类接触预测的 AUC 均超过 90%（Figure 6），证明接触概率高度可靠。

### 模型拟合优化

给定多视图地标预测后，MAMMA 通过最小化能量函数恢复 SMPL-X 参数 $\Phi$（姿态、形状、平移）。总能量为：

$$E(\Phi; \{\mathbf{Q}\}, \{\mathbf{L}\}) = E_{\mathrm{ldmks}} + E_{\mathrm{shape}} + E_{\mathrm{temp}} + E_{\mathrm{cont}}$$

其中 $\{\mathbf{Q}\}$ 为相机参数集合，$\{\mathbf{L}\}$ 为所有视图的地标预测。

#### 重投影误差能量 $E_{\mathrm{ldmks}}$

$$E_{\mathrm{ldmks}} = \frac{1}{C} \sum_{t,c,l} \rho\Bigg( \frac{\| \pmb{\mu}_{t,c,l} - \Pi(\mathbf{V}_{t,l}, \mathbf{Q}_c) \|}{\sigma_{t,c,l}} \Bigg) p_{t,c,l}$$

其中 $t$ 为时间帧索引，$c$ 为相机视图索引，$l$ 为地标索引；$\pmb{\mu}_{t,c,l}$ 为预测的 2D 地标位置；$\Pi(\mathbf{V}_{t,l}, \mathbf{Q}_c)$ 将 SMPL-X 网格上对应顶点 $\mathbf{V}_{t,l}$ 投影到相机 $c$ 的图像平面；$\sigma_{t,c,l}$ 为预测不确定性，用于自适应加权；$p_{t,c,l}$ 为可见性概率，使不可见地标不参与误差计算；$\rho$ 为鲁棒损失函数（Geman-McClure）。该设计使优化自动信赖低残差、高可见性的地标，抑制遮挡或不确定区域的干扰。

#### 不确定性动态更新

在优化后期阶段，MAMMA 利用当前重投影残差 $e_i$ 动态调整不确定性权重：

$$\sigma_i' = \sigma_i \cdot \min\left( \max\left( \frac{e_i}{\tau}, 0 \right), 1 \right)$$

阈值 $\tau = 10$ 像素。当残差 $e_i < \tau$ 时，$\sigma_i'$ 被缩小，使该地标在后续优化中获得更高权重；反之则保持原有权重。此机制进一步提升了拟合精度。

#### 接触能量 $E_{\mathrm{cont}}$

接触优化阶段引入两个基于 SDF 的能量项，由自定义 CUDA 核高效计算。

**排斥项** $E_{\mathrm{p}}$ 惩罚穿入他人身体内部的顶点：

$$E_{\mathrm{p}} = \frac{1}{N} \sum_{i=1}^{N} \left[ \min\big( 0, \mathrm{SDF}_{\mathrm{other}}(\mathbf{v}_i) + \delta \big) \right]^2$$

其中 $\mathrm{SDF}_{\mathrm{other}}(\mathbf{v}_i)$ 为顶点 $\mathbf{v}_i$ 在他人身体 SDF 中的有符号距离（内部为负），$\delta$ 允许有限的软组织变形。

**吸引项** $E_{\mathrm{c}}$ 将预测接触概率高的顶点拉向对方表面：

$$E_{\mathrm{c}} = \frac{1}{N} \sum_{i=1}^{N} p_i \left[ \max\left( 0, \mathrm{SDF}_{\mathrm{other}}(\mathbf{v}_i) \right) \right]^2$$

其中 $p_i$ 为网络预测的人物-人物接触概率。当 $p_i$ 高且顶点在对方体外（SDF > 0）时，该项施加吸引力，使接触区域贴合。消融实验表明，接触优化阶段（MAMMA-C）将平均穿透深度从 10.50 mm 降至 8.46 mm，穿透顶点数从 456.05 降至 378.02，同时 3D 拟合精度几乎不受影响（Table 3, Table 4）。

### 多视图跨视角对应

对于多人场景，MAMMA 利用 SAM2 进行实例分割与时序跟踪，为每个跟踪到的人在各帧各视图独立预测密集地标。跨视角人员匹配基于**对称极线距离** $D_g$：

$$D_g = \frac{1}{2FN} \sum_{i=1}^{FN} \left( d(\mathbf{x}_b^i, \mathbf{F}_{ba} \mathbf{x}_a^i) + d(\mathbf{x}_a^i, \mathbf{F}_{ab} \mathbf{x}_b^i) \right)$$

其中 $\mathbf{x}_a^i, \mathbf{x}_b^i$ 为视图 $a$ 和 $b$ 中两组地标的对应点，$\mathbf{F}_{ab}$ 为基础矩阵，$d(\cdot, \cdot)$ 为点到极线的距离。利用该距离构建亲和矩阵，通过匈牙利算法求解最优匹配，并形成跨视图的循环一致性人员分组。

### 优化初始化策略

与传统方法不同，MAMMA 不依赖任何姿态回归网络进行初始化。身体初始位置通过最小化各相机中心射线的距离来确定 3D 点，姿态和形状从零均值初始化。这种简洁策略得益于密集地标提供的强约束，使优化过程无需姿态先验即可收敛到准确解。

## 实验与分析

### 评估设置概览

MAMMA 的评估覆盖三个层级：密集地标检测精度、3D 网格拟合精度，以及与商业标记系统的对比。实验在多个数据集上进行，包括单人场景（RICH、MOYO、MammaEval-S）、双人交互场景（Harmony4D、CHI3D、MammaEval-D）、极限姿态场景（MOYO yoga），以及专门采集的与 Vicon 同步的 MammaEval-Extra 数据集。所有对比实验均使用真实边界框初始化，并在需要时统一采用 SAM2 掩码进行条件化，确保公平比较。对于 Hi4D 的跨数据集评估，MAMMA 网络在训练时移除了 Hi4D 序列，避免数据泄露。

### 密集地标检测精度

**单人场景。** 在 RICH、MOYO 和 MammaEval-S 三个数据集上，MammaNet 的 2D 地标误差均显著低于基线方法（Table 1）。在 RICH 上，MammaNet 达到 8.55 px，而 Look-Ma* 为 13.26 px，CameraHMR 为 12.51 px。SAM2 掩码的加入对单人场景提升有限（RICH: 8.55→8.47 px），因为单人场景下分割相对简单，网络本身已能有效定位地标。

**双人交互场景。** 双人紧密交互是核心难点。在 Harmony4D 上，MammaNet 不加掩码时误差为 31.96 px，加入 SAM2 掩码后骤降至 18.33 px（Table 2），降幅达 42.6%。同样，在 CHI3D 上从 6.22 px 降至 4.36 px。这表明掩码条件化在严重遮挡和人物重叠时起到了关键的注意力引导作用：掩码帮助交叉注意力机制聚焦于正确的人物区域，避免地标查询错误地关注到另一人的图像特征。

**极限姿态泛化。** 在 MOYO yoga 数据集上，即使 MammaNet 从未在类似瑜伽姿态上训练，其地标预测仍保持了合理的精度（11.40 px，Table 1），且定性结果（Figure 5）显示预测地标在极端关节角度下仍能正确附着在身体表面。这归因于地标查询的自注意力机制学习了地标间的空间关系先验，使得遮挡或极端变形下的地标可以通过可见地标推断。

**训练数据的影响。** 消融实验（Table 7）表明，在 BEDLAM 合成数据基础上加入 MammaSyn 训练后，MOYO 上的误差从 11.92 px 降至 6.95 px，MammaEval-D 上从 10.00 px 降至 7.70 px。MammaSyn 提供了更丰富的交互和接触场景，直接提升了网络对复杂多人情形的鲁棒性。

### 3D 网格拟合精度

**主基准结果。** Table 4 汇总了各方法在多个数据集上的 MPJPE 和 PVE。MAMMA 在所有数据集上均取得最优结果。在 RICH 上，MAMMA-C（含接触优化阶段）的 MPJPE 为 22.20 mm，而 Look-Ma* 为 39.52 mm，CameraHMR 为 35.55 mm，多视图 SMPLify-X 为 42.51 mm。MAMMA 的优势在交互数据集上更为显著：Harmony4D 上 MAMMA-C 的 MPJPE 为 27.42 mm，远低于 Harmony4D 原方法的 51.67 mm。

**跨数据集泛化。** 在 Hi4D 数据集上（Table 5），MAMMA 的 MPJPE 为 42.90 mm，优于所有对比方法。该数据集包含复杂的双人交互，且 MAMMA 网络在训练时未接触 Hi4D 数据，验证了方法的泛化能力。

**接触优化阶段的效果。** 消融实验（Table 3, Table 4）表明，接触优化阶段（MAMMA-C）的加入使穿透深度和穿透顶点数显著下降：平均穿透深度从 10.50 mm 降至 8.46 mm，穿透顶点数从 456.05 降至 378.02。同时，MPJPE 几乎不受影响（RICH: 22.06→22.20 mm），说明接触约束在消除物理不合理穿透的同时，并未牺牲拟合精度。接触预测的 AUC 超过 90%（Figure 6），为接触能量项提供了可靠的权重依据。

**优化阶段分析。** 四阶段优化中（Figure 13），S2（姿态/形状/平移优化）已提供良好的精度-效率折衷，S3（不确定性更新）和 S4（接触约束）进一步精修细节并抑制穿透。不确定性更新机制利用当前残差动态调低高误差地标的权重（阈值 τ=10 px），使优化更信赖一致性好的地标，有效抑制了误匹配地标对拟合的干扰。

**相机数量影响。** 即使使用少至 4 台相机，方法仍保持较强性能；相机数量增至约 12 台时精度趋于饱和（Figure 12）。这表明密集地标的多视图约束具有冗余性，少量相机即可提供足够的几何信息。

### 与 Vicon 标记系统的对比

在 MammaEval-Extra 数据集上，MAMMA 与 Vicon 标记系统进行了直接对比（Table 10）。实验使用 73 个 Vicon 标记进行 MoSh++ 拟合作为标记方法基线，在剩余 37 个未见过的额外标记上评估误差。MAMMA 的平均每标记误差为 22.48 mm，MoSh++ 为 21.62 mm，差距仅 0.862 mm。视觉质量几乎无差别，证明无标记方法在精度上已接近商业标记系统。需要指出，该评估排除了一例因校准错误导致的无效被试数据。

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/025_Table_10.jpg]]
*Table 10: Vicon Markers comparison experiment: Mean per-marker distance (mm) of MoSh and MAMMA on the Vicon held-out 37 markers of our MammaEval-Extra dataset*

### 失败模式与局限性

尽管整体性能优异，以下失败模式值得关注：

1. **严重遮挡与掩码不完整。** 当人数超过 2 人且出现严重遮挡时，部分序列出现不真实姿态。失败主要源于 SAM2 掩码在近距离交互时分割不完整，导致地标检测器的注意力分散到错误区域。

2. **接触预测偏保守。** 接触概率预测在单视图下最高约 60%，可能导致接触约束不足，或在非接触区域误判接触。这种保守性在网络训练的数据分布和损失设计中具有内在原因。

3. **手部精度不足。** 手部运动恢复精度仍有提升空间（Table 8 中手部单独评估的误差相对较高），现有训练数据对手指精细运动覆盖不足。

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/018_Table_8.jpg]]
*Table 8: Full Benchmark 3D fitting errors (mm). We evaluate the error for the full body, only for the body, and only for the hands*

4. **脚接触优化的副作用。** 脚接触地面优化时可能错误地将人体向下拉拽，建议仅用于单视图或后处理矫正。消融实验也表明地板接触优化对整体精度提升有限。

5. **时间抖动。** 高度遮挡且不确定的地标可能在优化中被忽略，在强时间正则化下引起局部抖动或过度平滑。

### 补充图表

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/005_Table_1.jpg]]
*Table 1: Dense landmark evaluation on single person datasets. Mean 2D Euclidean distance error (in pixels) between GT and predicted landmarks. Bold is the most accurate and underline is the most accurate without mask*

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/006_Table_2.jpg]]
*Table 2: Two-person datasets dense landmark evaluation. We use the images where IOU > 0.5 between two people*

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/007_Figure_5.jpg]]
*Figure 5: Comparison on extreme poses. Ground-truth landmarks are shown in green. For each prediction, landmarks are color-coded: red indicates higher pixel error, green indicates lower pixel error. We compare networks trained on BEDLAM*

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/008_Figure_6.jpg]]
*Figure 6: ROC curve evaluation of our contact predictions*

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/009_Table_3.jpg]]
*Table 3: Mean Penetration (M.P.) depth (mm) and vertices on Harmony4D, CHI3D, and MammaEval-D*

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/010_Table_4.jpg]]
*Table 4: Benchmark 3D fitting errors (mm)*

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/016_Table_7.jpg]]
*Table 7: Evaluation of datasets. Mean 2D Euclidean distance error (in pixels) between ground truth and predicted landmarks; includes visible and invisible landmarks*

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/020_Figure_12.jpg]]
*Figure 12: Camera variation accuracy*

![[assets/figures/papers/paper_list_l1691_MAMMA_Markerless_and_Automatic_Multi_Person_Motion_Action_Capture/figures/011_Table_5.jpg]]
*Table 5: MPJPE on the Hi4D dataset for 19 SMPL joints*

## 方法谱系与知识库定位

### 1. 核心设计路径与基线对比

MAMMA 的核心架构选择——从密集表面地标出发，通过重投影优化求解 SMPL-X 参数——在思路上与传统的两步式无标记动捕方法一脉相承，但在多个关键模块上做出了实质性重构。

**密集地标检测器的进化。** 早期方法如 **Look-Ma\***（Hewitt 等人，无具体出版信息）采用 CNN 直接回归地标坐标，缺乏对地标间空间关系的显式建模。**CameraHMR**（基于 Transformer 的方法）引入了可学习查询机制，但使用单一嵌入表示所有地标，限制了模型对不同地标语义的区分能力。MAMMA 的 **MammaNet** 将这一机制推向极致：为 512 个地标各分配一个独立的可学习查询（landmark query），使交叉注意力能够自适应地匹配每个地标最相关的图像区域，而自注意力则学习地标间的空间关系。这一设计本质上将地标检测从“回归坐标”转变为“查询驱动的特征聚合”，在强遮挡下具有更强的鲁棒性。

**输入条件化的创新。** MammaNet 的另一关键改进是将 SAM2 分割掩码作为条件输入，通过逐元素求和与图像特征融合。这与单纯依赖 RGB 图像的基线形成鲜明对比。实验表明，掩码条件化在双人紧密交互场景中效果尤为显著（Harmony4D 误差从 31.96 px 降至 18.33 px），但在单人场景中提升有限——这说明掩码的核心价值在于帮助模型区分重叠人体区域，而非提升一般性定位精度。

**多任务预测的扩展。** 与仅预测地标坐标和不确定性的 CameraHMR 不同，MammaNet 同时输出可见性概率、人物-人物接触概率和地面接触概率。接触预测的 AUC 均超过 90%（Figure 6），为后续的物理约束优化提供了可靠先验，这是此前方法完全缺失的能力。

**优化范式的转变。** 传统方法（如多视图 SMPLify-X）通常依赖回归网络初始化姿态和形状，再通过优化精修。MAMMA 彻底摒弃了这一依赖：它通过最小化各相机中心射线距离来初始化人体 3D 位置，完全依靠地标重投影驱动 SMPL-X 参数优化。这一选择使得方法不绑定于任何特定的姿态先验或回归模型，在跨域泛化时具有天然优势。

### 2. 在知识库中的定位

MAMMA 处于**无标记多人运动采集**与**基于优化的 3D 人体重建**的交叉地带。其技术脉络可追溯至以下几条线索：

- **密集地标检测**：从单视图 CNN 回归（Look-Ma\*）到 Transformer 查询机制（CameraHMR），再到 MammaNet 的独立查询 + 掩码条件化。MAMMA 将这一方向推向了当前最优水平，尤其在多人遮挡场景中建立了显著的性能壁垒。
- **多视图优化拟合**：继承自 SMPLify-X 的重投影优化框架，但 MAMMA 用密集地标替代了稀疏关键点，并通过预测的不确定性动态加权、接触约束等机制大幅提升了拟合精度和物理合理性。与 **Harmony4D**（多视图交互基线，采用网格拟合 + 轮廓对齐）相比，MAMMA 在 3D 精度和穿透控制上均有明显优势。
- **接触建模**：MAMMA 的接触预测和 SDF 约束优化（排斥项 $E_p$、吸引项 $E_c$）是此前无标记系统中缺失的关键组件。这一模块将物理接触从“事后矫正”提升为“优化过程中的主动约束”，使多人交互重建的穿透深度和顶点数显著下降（平均穿透深度 10.50→8.46 mm）。

### 3. 适用边界与局限

尽管 MAMMA 在多个基准上取得了领先结果，其适用边界和已知局限同样值得关注：

**接触预测的保守性。** 单视图下人物-人物接触概率最高约 60%，这意味着网络倾向于低估接触区域。这种保守性可能导致接触约束不足，或在非接触区域产生误判。在极端紧密交互（如拥抱、摔跤）中，接触优化的效果可能受限。

**地面接触优化的副作用。** 脚部接触地面的优化可能错误地将人体向下拉拽，尤其在脚部被遮挡或地标预测噪声较大时。论文建议仅将地面接触用于单视图或后处理矫正，说明该模块在多视图场景中的稳定性尚未完全验证。

**手部运动的精度瓶颈。** 现有训练数据对手指精细运动的覆盖不足，导致手部姿态恢复仍有提升空间。这是当前无标记动捕系统的普遍短板，MAMMA 未能完全突破。

**遮挡下的局部退化。** 当某个地标被严重遮挡且预测不确定性较高时，优化器可能选择忽略该地标，导致局部区域出现抖动或过度平滑。强时间正则化虽然抑制了抖动，但也可能抹去快速运动的细节。

**多人扩展的脆弱性。** 当人数超过 2 人时，部分序列出现不真实姿态。失败主要源于严重遮挡或 SAM2 掩码不完整——当人体在图像中大面积重叠时，SAM2 的分割边界可能模糊或断裂，直接损害地标检测和跨视角匹配的质量。

**相机数量的边际收益递减。** 消融实验（Figure 12）显示，4 台相机即可提供较强性能，增至约 12 台时精度趋于饱和。这意味着 MAMMA 在中等规模的多视图设置下已接近性能上限，增加硬件投入的回报有限。

### 4. 开放问题与未来方向

基于上述局限，以下几个方向值得进一步探索：

1. **手部与手指交互数据的增强。** 如何系统性地构建覆盖精细手部动作的训练数据，是提升手部运动捕捉精度的关键瓶颈。可能的路径包括合成数据增强、手部专用地标设计，或引入手部先验模型。

2. **多视图联合地标预测。** 当前 MammaNet 在每个视图中独立推理地标，跨视角一致性仅在后处理阶段通过极线距离匹配实现。如果能在网络层面引入视图间的信息交换（如跨视图注意力），可能进一步提升遮挡区域的地标质量和匹配精度。

3. **时序建模的引入。** 当前方法通过优化阶段的时间平滑项处理时序一致性，但地标检测本身是逐帧独立的。引入时序 Transformer 或状态空间模型进行跨帧地标预测，有望减少抖动并提升快速运动下的稳定性。

4. **扩散先验与优化的融合。** 将基于扩散模型的人体运动先验融入优化过程，可能更好地处理严重遮挡和接触模糊——扩散模型能够生成合理的姿态假设，弥补地标信息不足时的歧义性。

5. **SAM2 掩码的鲁棒性提升。** 在近距离交互场景中，SAM2 掩码的不完整性是系统失败的主要原因之一。探索掩码修复策略、多视图掩码一致性约束，或训练专用的交互场景分割模型，都是可行的改进方向。

6. **接触预测的校准。** 如何在保持单视图泛化能力的前提下，提高接触预测的置信度（降低保守性）？可能的方案包括多视图接触一致性约束、接触区域的针对性数据增强，或引入物理模拟作为弱监督信号。

## 原文 PDF

![[paperPDFs/CVPR_2026/MAMMA_Markerless_Accurate_Multi_person_Motion_Acquisition.pdf]]
