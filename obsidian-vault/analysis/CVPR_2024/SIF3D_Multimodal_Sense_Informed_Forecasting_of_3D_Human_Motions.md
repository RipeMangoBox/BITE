---
title: SIF3D Multimodal Sense Informed Forecasting of 3D Human Motions
type: paper
paper_level: A
venue: CVPR
year: 2024
pdf_ref: paperPDFs/CVPR_2024/SIF3D_Multimodal_Sense_Informed_Forecasting_of_3D_Human_Motions.pdf
project_link: null
code_link: null
aliases:
- SMSIF3HM
tags:
- CVPR_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 通过引入三元意图感知注意力（TIA）和语义一致性注意力（SCA），分别利用全局运动意图和局部姿态语义，显式区分场景中的显著点与底层点，从而加强轨迹规划和姿态预测的场景一致性。
primary_logic: 同时利用3D场景点云、人类注视和运动历史三模态信息，TIA为全局轨迹规划捕捉与移动目标相关的显著点，SCA为每帧姿态预测捕捉语义相关的局部显著点，实现长时、物理合理的人体运动预测。
claims:
- SIF3D 在 GIMO 和 GTA-1M 两个数据集上同时提升了轨迹和姿态的长期预测精度，相比强基线 BiFu 在终点轨迹误差上分别降低 61mm 和 67mm。
- 消融实验表明，移除 TIA 导致终点轨迹误差增加 111mm，移除 SCA 导致终点轨迹误差增加 37mm、终点姿态误差增加 4.7mm，证实两个注意力模块均不可或缺。
- 与 BiFu 相比，SIF3D 能区分场景中的显著点（暖色）与底层点（冷色），生成的运动序列在俯视、全序和终点姿态视图下均与场景几何保持一致，避免了人体网格与环境交叉。
- 同时引入 3D 场景和人类注视信息能够一致地提升所有基线方法的性能，且 SIF3D 受益最大，表明多模态信息互补性对场景感知运动预测至关重要。
---

# SIF3D Multimodal Sense Informed Forecasting of 3D Human Motions

> [!tip] 核心洞察
> 同时利用3D场景点云、人类注视和运动历史三模态信息，TIA为全局轨迹规划捕捉与移动目标相关的显著点，SCA为每帧姿态预测捕捉语义相关的局部显著点，实现长时、物理合理的人体运动预测。

| 字段 | 内容 |
|------|------|
| 中文题名 | SIF3D：多模态感知引导的3D人体运动预测 |
| 英文题名 | SIF3D Multimodal Sense Informed Forecasting of 3D Human Motions |
| 会议/期刊 | CVPR 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SIF3D |
| Dataset | GIMO, GTA-1M |

> [!tip] 效果简介
> - GIMO 上，Traj-dest (mm) 666 vs 727 (BiFu w/ Scene+Gaze) (-61)；MPJPE-dest (mm) 195.7 vs 205.0 (BiFu w/ Scene+Gaze) (-9.3)。
> - GTA-1M 上，Traj-dest (mm) 836 vs 903 (BiFu w/ Scene+Gaze) (-67)；MPJPE-dest (mm) 227.7 vs 234.2 (BiFu w/ Scene+Gaze) (-6.5)。

## 概要

**问题瓶颈**：现有3D人体运动预测方法通常将场景信息编码为统一的全局嵌入，无法区分场景中不同空间点的显著程度。这导致预测的人体轨迹与姿态经常与环境几何发生穿透或失真，违背物理合理性约束。

**核心洞见**：SIF3D 同时利用3D场景点云、人类注视序列和运动历史三模态信息，通过两个互补的注意力机制显式建模场景点的显著性——三元意图感知注意力（TIA）为全局轨迹规划捕捉与移动目标相关的显著点，语义一致性注意力（SCA）为每帧姿态预测捕捉语义相关的局部显著点。

**方法定位**：SIF3D 属于多模态场景感知运动预测方法，在轨迹预测与姿态预测之间引入解耦设计：TIA 输出专用于全局轨迹规划，SCA 输出专用于局部姿态预测。相较于同等对待所有场景点的基线方法（如 **BiFu**, Zheng et al., ECCV 2022），SIF3D 首次将场景显著性显式建模引入3D人体运动预测任务。

**主要结果**：在 GIMO 和 GTA-1M 两个基准数据集上，SIF3D 同时提升了轨迹和姿态的长期预测精度，相比强基线 BiFu 在终点轨迹误差上分别降低 61mm 和 67mm（Table 1）。消融实验证实，TIA 和 SCA 两个注意力模块均不可或缺：移除 TIA 导致终点轨迹误差增加 111mm，移除 SCA 导致终点轨迹误差增加 37mm、终点姿态误差增加 4.7mm（Table 4）。定性可视化表明，SIF3D 能够区分场景中的显著点与底层点，生成的运动序列在多个视角下均与场景几何保持一致（Figure 1, Figure 3）。



### 3D 场景感知的人体运动预测

在增强现实、虚拟现实、具身智能等应用中，预测人类在 3D 场景中的未来运动至关重要。给定一段观测到的历史运动序列 $X_{1:T}$、静态 3D 场景点云 $S$，以及可选的注视点序列 $G_{1:T}$，任务目标是生成未来 $\Delta T$ 帧内物理合理且场景一致的人体轨迹与姿态序列 $Y_{1:\Delta T}$。这一问题的核心挑战在于：人体运动不仅受自身动力学约束，还必须与周围 3D 环境几何保持协调——避免穿模、悬空或与障碍物碰撞。

### 现有方法的结构性缺口

近年来，场景感知运动预测取得了显著进展。**LTD**（Mao et al., ICCV 2019）利用图卷积网络建模轨迹依赖，**SPGSN**（Li et al., ECCV 2022）通过骨架分割图散射网络预测姿态，**AuxFormer**（Xu et al., ICCV 2023）引入辅助任务增强 Transformer 预测能力。然而，这些方法最初并未显式利用 3D 场景信息，导致预测结果缺乏环境约束。

为弥补这一缺陷，**BiFu**（Zheng et al., ECCV 2022）提出了双向融合多模态的框架，将 3D 场景编码为全局嵌入并与运动特征融合。这一设计虽在一定程度上改善了场景一致性，却暴露了一个根本性瓶颈：**全局场景嵌入将场景中所有点等同对待，无法区分不同空间位置对运动预测的显著程度**。如图 1 所示，BiFu 生成的运动序列在俯视、全序和终点姿态视图下均出现人体网格与环境几何的交叉或扭曲，表明其未能捕捉场景中哪些区域对轨迹规划和姿态调整真正关键。

### 多模态信息的未充分利用

人类在 3D 环境中移动时，不仅依赖对场景几何的全局感知，还会通过注视行为有选择地关注与当前意图相关的区域。这一“内部注视”信号蕴含了丰富的意图信息，但现有方法要么完全忽略，要么仅将其作为辅助特征简单拼接，未能实现运动、场景、注视三模态之间的深层交互与互补。

值得注意的是，当同时引入 3D 场景和人类注视信息时，所有基线方法的性能均获得一致提升（Table 1），表明多模态信息本身具有互补价值。然而，BiFu 等现有融合策略对这一增益的利用效率有限——它们缺乏一种机制来显式建模“场景中哪些点对当前运动意图是显著的”。

### 本文的核心动机

基于上述分析，本文的核心动机可归纳为三个层面：

1. **从全局嵌入到显著点建模**：设计一种注意力机制，使模型能够根据运动意图和注视行为，自适应地区分场景中的显著点（如目标位置、障碍物边界）与底层点（如远处墙壁、无关物体），从而为轨迹规划和姿态预测提供精细化的场景约束。

2. **三模态深度融合**：将运动序列、3D 场景点云和人类注视三模态信息通过交叉注意力进行有机融合，而非简单拼接，使各模态在统一的显著性框架下互补增强。

3. **轨迹与姿态的解耦预测**：全局轨迹规划需要关注与移动目标相关的远距离显著区域，而逐帧姿态调整需要关注与当前身体姿态语义相关的局部场景点。将两者解耦并用不同的显著性机制分别处理，有望同时提升长期轨迹精度和姿态保真度。

这些动机共同指向一个核心洞察：**同时利用 3D 场景点云、人类注视和运动历史三模态信息，通过全局运动意图和局部姿态语义分别驱动场景显著性建模，是实现长时、物理合理的人体运动预测的关键路径**。



## 核心方法与创新机理

SIF3D 的核心创新在于**将场景从“平等的背景”转变为“具有显著性的意图场”**。现有方法（如 **BiFu**，Zheng et al., ECCV 2022）通常将 3D 场景编码为一个统一的全局嵌入，同等对待场景中的所有点云。这种无差别的表征方式导致模型无法区分哪些场景区域对当前运动目标至关重要（如即将经过的走廊、即将坐下的椅子），哪些仅仅是底层背景。其直接后果是预测的人体轨迹和姿态经常与场景几何发生穿透或失真，无法满足物理合理性约束（Figure 1）。

针对这一瓶颈，SIF3D 通过两个互补的注意力机制——**三元意图感知注意力（TIA）** 与 **语义一致性注意力（SCA）**——对场景点云进行显式的显著性建模，并以此驱动轨迹规划与姿态预测的解耦。

**1. 场景显著性建模：从全局嵌入到逐点区分**

这是 SIF3D 最根本的改变。BiFu 等基线方法使用全局场景嵌入，相当于将整个房间压缩为一个向量，丢失了空间细节。SIF3D 则保留逐点场景特征，并通过 TIA 和 SCA 分别为每个场景点计算“显著权重”：
- **TIA** 将压缩后的全局运动表示作为 Query，与所有场景点特征进行交叉注意力计算（Eq. 7），识别出与整体运动意图相关的**全局显著点**（如目的地附近的家具、行进路径上的障碍物）。这些点以暖色高亮，底层点以冷色抑制（Figure 3）。
- **SCA** 为每一帧的独立姿态查询计算场景点的**局部显著权重**（Eq. 13），捕捉与当前身体姿态语义相关的局部几何（如脚即将接触的地面、手即将触碰的桌面）。SCA 还引入了空间位置偏置，使模型对距离身体关节更近的场景点赋予更高关注度。

两种显著性的互补性在消融实验中得到了验证：移除 TIA 导致终点轨迹误差（Traj-dest）增加 111mm，移除 SCA 导致 Traj-dest 增加 37mm、终点姿态误差（MPJPE-dest）增加 4.7mm（Table 4），证明全局路径规划与局部姿态调整均依赖于场景显著性的区分。

**2. 多模态融合输入：运动、场景、注视的三元协同**

SIF3D 将输入模态从传统的“运动序列”或“运动+场景”扩展为**运动序列、3D 场景点云、人类注视序列**三者的联合。注视信息提供了观察者意图的直接线索——人眼注视的方向通常指向下一步交互的目标。TIA 模块通过 GazeEncoder 将注视点索引的场景特征编码为注视特征，并与运动、场景特征融合（Eq. 10），使全局意图分析不仅依赖于运动历史，还显式地参考了视觉注意力指向的区域。

Table 1 的证据表明，同时引入 3D 场景和人类注视信息能够一致地提升所有基线方法（LTD、SPGSN、AuxFormer、BiFu）的性能，且 SIF3D 的受益幅度最大，验证了三模态互补设计的有效性。

**3. 轨迹与姿态的预测解耦**

以往方法通常使用相同的特征同时预测全局轨迹和局部姿态，导致两个不同粒度的任务相互干扰。SIF3D 将二者解耦：TIA 输出的全局显著场景特征专用于 **TrajectoryPlanner** 预测未来平移和朝向（Eq. 18），SCA 输出的逐帧局部显著场景特征专用于 **PosePredictor** 预测身体姿态参数（Eq. 19）。这种“全局规划-局部细化”的分工使得轨迹规划关注大范围场景结构，而姿态预测关注与身体直接交互的近场几何，避免了特征混淆。

综上，SIF3D 的创新本质在于**将场景建模从被动的环境编码升级为主动的意图感知显著性场**，并通过多模态协同和解耦预测架构，实现了长时、物理合理的 3D 人体运动预测。



SIF3D 的整体设计围绕一个核心瓶颈展开：**现有方法将 3D 场景编码为统一的全局嵌入，无法区分场景中不同点的显著程度**，导致预测的人体轨迹和姿态经常与环境发生穿透或失真。为解决这一问题，SIF3D 同时引入**运动序列、3D 场景点云和人类注视**三模态信息，通过两个互补的注意力机制——三元意图感知注意力（TIA）和语义一致性注意力（SCA）——分别服务于全局轨迹规划和局部姿态预测，从而显式区分场景中的显著点与底层点。

### 输入与编码阶段

框架接收三类输入（Fig. 2）：

![[assets/figures/papers/paper_list_l1725_SIF3D_Multimodal_Sense_Informed_Forecasting_of_3D_Human_Motions/figures/002_Figure_2.jpg]]
*Figure 2: The architecture of SIF3D. SIF3D incorporates three modalities of input, the past motion sequence, the 3D scene point cloud, and the human gaze. First, MotionEncoder encodes past motion sequence into a motion embedding*

1. **历史运动序列** $X_{1:T}$：包含过去 $T$ 帧的人体关节位置。MotionEncoder 将历史序列与重复的未来占位帧拼接后编码为运动嵌入 $\mathbf{f}_m$（Eq. 2）。
2. **3D 场景点云** $S$：通过 PointNet++ 提取逐点场景特征 $\hat{S}$ 和全局场景嵌入 $\hat{S}_{global}$（Eq. 3）。
3. **人类注视序列** $G_{1:T}$：GazeEncoder 利用注视点索引场景点云中的对应特征，编码为与运动序列对齐的注视特征 $\mathbf{f}_{gaze}$（Eq. 9）。

所有嵌入维度统一设为 256。

### 显著性建模与跨模态融合

框架的核心由两个并行的注意力模块构成，分别承担全局与局部场景显著性建模：

- **TIA 模块**：首先通过 Temporal Aggregator 将运动嵌入压缩为单一全局运动表示（默认取最后一帧，消融实验证实该策略在所有时序聚合策略中表现最佳）。该全局运动表示作为查询，与场景点云特征进行交叉注意力计算，得到每个场景点的全局显著权重 $s_g$（Eq. 7）。显著点（暖色）被强化，底层点（冷色）被抑制。随后，TIA 将运动特征、显著场景特征和注视特征通过 MLP 融合，输出 $\mathbf{f}_o^{TIA}$，专用于全局轨迹规划。

- **SCA 模块**：为每一帧姿态独立计算场景点的局部显著性。每个时间步的姿态查询与场景键进行交叉注意力，生成逐帧局部显著权重 $s_l$（Eq. 13），并融入空间位置偏置以增强语义一致性。SCA 输出专用于局部姿态预测。

两个模块的显著性权重通过相乘进一步抑制非显著点，确保轨迹规划关注与移动目标相关的全局场景结构，而姿态预测关注与当前身体姿态语义相关的局部场景区域。

### 预测与解码阶段

框架将轨迹与姿态的预测显式解耦：

- **TrajectoryPlanner**：基于 TIA 输出预测未来全局平移 $\hat{T}$ 和朝向 $\hat{O}$（Eq. 18）。
- **PosePredictor**：基于 SCA 输出预测未来身体姿态参数 $\hat{P}$（Eq. 19）。

随后，预测的轨迹、朝向和姿态参数通过 SMPL-X 模型重建三维关节位置 $\hat{J}$（Eq. 20），再由 MotionDecoder（基于图卷积网络）生成最终的运动序列（Eq. 21）。

### 对抗监督

为提升预测运动的物理合理性，框架引入 **Geometry Discriminator** 作为对抗训练裁判，判断预测运动是否与真实场景-运动分布一致。该判别器与生成器联合训练，约束生成的运动序列在 3D 场景中保持几何一致性，避免人体网格与环境交叉。

### 关键设计决策与证据

- **三模态互补性**：同时加入场景和注视信息在所有基线上均带来增益，且 SIF3D 的提升幅度最大（Table 1），验证了三模态互补设计的有效性。
- **TIA 与 SCA 的不可或缺性**：消融实验表明，移除 TIA 导致终点轨迹误差增加 111mm；移除 SCA 导致终点轨迹误差增加 37mm、终点姿态误差增加 4.7mm（Table 4）。
- **场景点云规模**：点云数量从 512 增至 4096 时性能持续提升，继续增大则饱和，同时 VRAM 和推理速度保持在可接受范围（Table 5）。
- **时序聚合策略**：TIA 中采用“Last”策略（取最后一帧运动嵌入）在所有策略中表现最佳（Table 6）。

### 局限性

当前框架专注于确定性预测，未涉及多模态运动生成中的多样性问题；对复杂的动态场景和人-物交互（如抓取、操作物体）尚未进行验证；GTA-1M 数据集缺少真实人类注视数据，采用近似估计可能影响意图建模的准确性。



SIF3D 的核心架构围绕“解耦全局轨迹规划与局部姿态预测”这一设计原则展开，其关键创新在于两个互补的跨模态注意力模块：三元意图感知注意力（TIA）和语义一致性注意力（SCA）。以下按信息流顺序阐述各模块及其关键公式。

### 问题形式化与多模态编码

给定历史运动序列 $X_{1:T}$、3D 场景点云 $S$ 和人类注视序列 $G_{1:T}$，SIF3D 的目标是最大化未来运动序列 $Y_{1:\Delta T}$ 的条件概率：

$$\arg \max P(Y_{1:\Delta T} | X_{1:T}, S, G_{1:T}; \theta) \tag{1}$$

**运动编码器（MotionEncoder）** 将历史运动序列与重复的最后一帧占位符拼接后编码为运动嵌入 $\mathbf{f}_m$：

$$\mathbf{f}_m = \mathrm{MotionEncoder}(\{X, \mathbf{x}_T, ..., \mathbf{x}_T\}) \tag{2}$$

其中占位帧的数量等于预测帧数 $\Delta T$，这一填充策略使编码器能够感知未来时间跨度。

**场景编码器** 使用 PointNet++ 对 3D 点云 $S$ 提取逐点特征 $\hat{S}$ 和全局场景嵌入 $\hat{S}_{global}$：

$$\hat{S}, \hat{S}_{global} = \mathrm{PointNet}++(S) \tag{3}$$

逐点特征 $\hat{S}$ 保留了场景的空间局部信息，为后续显著性计算提供了逐点粒度的表征基础。

### 三元意图感知注意力（TIA）

TIA 模块的核心功能是为全局轨迹规划识别场景中的显著点。其处理流程分为三步：

**第一步：全局运动聚合。** 时序聚合器（Temporal Aggregator）将运动嵌入 $\mathbf{f}_m$ 沿时间维度压缩为单一全局运动表示 $\Delta\mathbf{f}_{gm}^{TIA}$。默认采用“Last”策略，即取最后一帧的运动嵌入，消融实验证实该策略在所有候选方案中表现最优。

**第二步：全局显著性计算。** 以全局运动表示作为查询（Query），以场景逐点特征作为键（Key）和值（Value），通过交叉注意力计算每个场景点的全局显著权重：

$$s_g = \mathrm{softmax}\bigg(\frac{Q^{TIA} * (K^{TIA})^T}{\sqrt{c}}\bigg) \tag{7}$$

其中 $c$ 为注意力维度。权重 $s_g$ 反映了场景中哪些点与整体运动意图相关——例如，走向沙发时，沙发附近的点会获得更高的全局显著权重。

**第三步：三模态融合。** 注视编码器（GazeEncoder）将注视点对应的场景特征序列编码为注视特征 $\mathbf{f}_{gaze}$：

$$\mathbf{f}_{gaze} = \mathrm{GazeEncoder}(\{\hat{S}[G], \hat{S}[g_T], ..., \hat{S}[g_T]\}) \tag{9}$$

随后，运动特征、加权场景特征和注视特征通过 MLP 融合为 TIA 输出 $\mathbf{f}_o^{TIA}$：

$$\mathbf{f}_o^{TIA} = \mathbf{MLP}(\mathrm{concat}(\mathbf{f}_m, \mathbf{f}_{sm}^{TIA}, \mathbf{f}_{gaze})) \tag{11}$$

该输出直接供给轨迹规划器（TrajectoryPlanner）进行全局平移和朝向预测。

### 语义一致性注意力（SCA）

SCA 模块与 TIA 互补，为每一帧的姿态预测独立计算场景点的局部显著性。其关键区别在于：TIA 使用聚合后的全局运动表示作为查询，而 SCA 使用每个时间步的姿态特征作为查询，从而捕捉与当前身体姿态语义相关的场景点。

$$s_l = \mathrm{softmax}\bigg(\frac{Q^{SCA} * (K^{SCA})^T}{\sqrt{c}}\bigg) \tag{13}$$

例如，当人体处于坐姿时，SCA 会为座椅表面的点分配较高的局部显著权重，而站立行走时则关注地面附近的点。SCA 的输出 $\mathbf{f}_o^{SCA}$ 供给姿态预测器（PosePredictor）。

### 预测与重建

**轨迹规划器** 基于 TIA 输出预测未来全局平移 $\hat{T}$ 和朝向 $\hat{O}$：

$$\hat{T}, \hat{O} = \mathrm{TrajectoryPlanner}(\mathbf{f}_o^{TIA}) \tag{18}$$

**姿态预测器** 基于 SCA 输出预测未来身体姿态参数 $\hat{P}$：

$$\hat{P} = \mathrm{PosePredictor}(\mathbf{f}_o^{SCA}) \tag{19}$$

最后，通过 SMPL-X 模型从预测参数重建三维关节位置：

$$\hat{J} = \mathrm{SMPL-X}(\hat{T}, \hat{O}, \hat{P}, \mathrm{VPoser}(\hat{P})) \tag{20}$$

其中 VPoser 作为姿态先验约束姿态参数的合理性。运动解码器（GCN）进一步从重建的关节位置生成最终运动序列，并由几何判别器进行对抗训练以提升物理合理性。

### 模块协同机制

TIA 和 SCA 的协同作用体现在两个层面：**时间尺度上**，TIA 关注整个预测序列的全局意图，SCA 关注每帧的局部语义；**空间尺度上**，TIA 的全局显著权重与 SCA 的局部显著权重相乘，实现对非显著点的双重抑制，确保预测的运动既符合长期目标导向，又在每一帧与场景几何保持一致。消融实验表明，移除 TIA 导致终点轨迹误差增加 111mm，移除 SCA 导致终点轨迹误差增加 37mm、终点姿态误差增加 4.7mm，证实两个模块均不可或缺。

### 补充图表

![[assets/figures/papers/paper_list_l1725_SIF3D_Multimodal_Sense_Informed_Forecasting_of_3D_Human_Motions/figures/001_Figure_1.jpg]]
*Figure 1: The proposed SIF3D: multimodal Sense-Informed Forecasting of 3D human motions. Our SIF3D takes the observed motion sequence, as well as the 3D scene point cloud as input modalities, and is able to identify salient points (redder) and underlying ones (bluer), to generate the accurate trajectory and high-fidelity future poses within given 3D scenarios. In contrast, the state-of-the-art baseline of BiFu [73] equally considers the global scene embedding, and thus cannot distinguish the saliency of the 3D scene, leading to the physically implausible motions, e.g., human mesh intersecting or distorting with the 3D environment, violating any physical constraints*



## 实验与关键发现

### 核心瓶颈与设计动机

现有场景感知人体运动预测方法（如**BiFu**，Zheng et al., ECCV 2022）普遍将3D场景编码为统一的全局嵌入，对所有场景点等权处理。这导致模型无法区分场景中不同位置对运动规划的显著程度——例如，人即将走向的沙发区域与远处的墙壁具有完全不同的行为约束意义。其后果是预测的人体轨迹和姿态频繁与环境发生穿透或网格失真（Figure 1）。

SIF3D的核心洞察在于：**同时利用3D场景点云、人体注视和运动历史三模态信息，显式建模场景点的显著程度**。具体而言，三元意图感知注意力（TIA）为全局轨迹规划捕捉与移动目标相关的显著点，语义一致性注意力（SCA）为每帧姿态预测捕捉语义相关的局部显著点。这种“全局-局部”解耦的显著性建模，使模型能够生成物理合理的长时运动序列。

### 主要实验结果

#### 整体性能对比（Table 1）

![[assets/figures/papers/paper_list_l1725_SIF3D_Multimodal_Sense_Informed_Forecasting_of_3D_Human_Motions/figures/003_Table_1.jpg]]
*Table 1: Comparison of trajectory deviation and MPJPE (in mm) over the sequences of the GIMO [73] and GTA-1M [5] datasets. The best result is highlighted in bold. From the results, we observe that the 3D scene and gaze information can boost all the methods, and the proposed SIF3D obtains both lower trajectory deviation and smaller MPJPE in almost all scenarios compared to the previous methods*

在GIMO和GTA-1M两个基准数据集上，SIF3D在轨迹和姿态的长期预测精度上均达到最优。与最强基线BiFu（同时使用场景和注视模态）相比：

- **GIMO数据集**：终点轨迹误差（Traj-dest）从727mm降至**666mm**（-61mm），终点姿态误差（MPJPE-dest）从205.0mm降至**195.7mm**（-9.3mm）。
- **GTA-1M数据集**：终点轨迹误差从903mm降至**836mm**（-67mm），终点姿态误差从234.2mm降至**227.7mm**（-6.5mm）。

值得注意的是，SIF3D在长期预测（终点指标）上的优势尤为突出，这与TIA模块专注于全局轨迹规划的设计初衷一致。

#### 多模态互补性验证（Table 1）

实验系统性地验证了场景和注视两种模态的增益效应。在LTD（Mao et al., ICCV 2019）、SPGSN（Li et al., ECCV 2022）、AuxFormer（Xu et al., ICCV 2023）和BiFu四个基线方法上，同时加入3D场景和人类注视信息均能一致提升性能。其中，SIF3D受益最大，表明其TIA和SCA模块能更有效地利用多模态互补信息。这一发现确认了**多模态信息互补性对场景感知运动预测至关重要**，而非简单堆叠输入即可获得增益。

#### 各场景详细性能（Table 2, Table 3）

![[assets/figures/papers/paper_list_l1725_SIF3D_Multimodal_Sense_Informed_Forecasting_of_3D_Human_Motions/figures/004_Table_2.jpg]]
*Table 2: Performance details on the GIMO test set [73] using trajectory deviation and MPJPE (in mm). Our SIF3D demonstrates strong performance across all scenarios, particularly excelling in long-term predictions, and achieves the best result on average*

![[assets/figures/papers/paper_list_l1725_SIF3D_Multimodal_Sense_Informed_Forecasting_of_3D_Human_Motions/figures/005_Table_3.jpg]]
*Table 3: Performance details on the GTA-1M test set [5] using trajectory deviation and MPJPE (in mm). We observe that our SIF3D consistently outperforms the baseline methods in motion prediction within game engine-rendered 3D scenarios*

在GIMO测试集的五个场景（客厅、卧室、厨房等）和GTA-1M的多个游戏引擎渲染场景中，SIF3D均展现出稳定的领先优势。特别是在需要复杂空间推理的场景（如家具密集的卧室），SIF3D相比BiFu的优势更加明显，验证了逐点显著性建模在复杂环境中的价值。

### 消融实验

#### 关键组件消融（Table 4）

![[assets/figures/papers/paper_list_l1725_SIF3D_Multimodal_Sense_Informed_Forecasting_of_3D_Human_Motions/figures/007_Table_4.jpg]]
*Table 4: SIF3D performance with ablations of components, evaluated using trajectory deviation and MPJPE (in mm)*

消融实验直接验证了TIA和SCA两个注意力模块的必要性：

- **移除TIA模块**（仅使用运动特征进行轨迹预测）：终点轨迹误差从666mm增至777mm（+111mm），退化幅度显著，证明全局场景显著性对轨迹规划不可或缺。
- **移除SCA模块**：终点轨迹误差增加37mm，终点姿态误差增加4.7mm，表明局部场景显著性对精细姿态预测有独立贡献。

两个模块的贡献具有互补性：TIA主导轨迹质量，SCA主导姿态精度，同时移除将导致性能全面崩溃。

#### 场景点云规模消融（Table 5）

![[assets/figures/papers/paper_list_l1725_SIF3D_Multimodal_Sense_Informed_Forecasting_of_3D_Human_Motions/figures/009_Table_5.jpg]]
*Table 5: SIF3D performance with various scene point cloud sizes*

场景点云数量从512增至4096时，性能持续提升；继续增大至8192时性能趋于饱和，同时显存占用和推理速度保持在可接受范围。这表明SIF3D能有效利用稠密场景信息，但过高的点密度带来的边际收益递减。论文最终选择4096作为默认配置。

#### 时序聚合策略消融（Table 6）

![[assets/figures/papers/paper_list_l1725_SIF3D_Multimodal_Sense_Informed_Forecasting_of_3D_Human_Motions/figures/008_Table_6.jpg]]
*Table 6: Performance of SIF3D with various temporal aggregators*

TIA模块中的时序聚合器负责将运动嵌入压缩为全局运动表示。实验比较了Last（取最后一帧）、Mean（平均池化）、Max（最大池化）和Attention（可学习注意力池化）四种策略。**Last策略在所有指标上表现最佳**，这与轨迹预测任务的性质相符——最后一帧的运动状态包含了最直接的未来行进意图信息。

### 定性分析（Figure 3）

![[assets/figures/papers/paper_list_l1725_SIF3D_Multimodal_Sense_Informed_Forecasting_of_3D_Human_Motions/figures/006_Figure_3.jpg]]
*Figure 3: Visualizations of our SIF3D compared with the SoTA BiFu, under the scenarios of (a) living room and (b) bedroom. The top is the results of BiFu [73], which equally treats all scene points; in contrast, the middle row is our SIF3D, where the salient points are highlighted in red, and the underlying points are in blue. For the sake of clarity, the predicted sequence is presented from the vertical view, whole-seq view, and end-pose view. We note that the red human meshes are the ground truth, while the blue ones indicate the predictions. At the bottom, we present the local scene salience heatmap across time for SIF3D, with a time interval of 2 seconds*

与BiFu的定性对比揭示了SIF3D的核心行为差异。在客厅和卧室场景中：

- **BiFu**：对所有场景点等权处理（热力图呈现均匀分布），生成的运动序列在俯视图、全序视图和终点姿态视图下均出现人体网格与环境交叉。
- **SIF3D**：能清晰区分显著点（暖色，如即将到达的沙发/床区域）与底层点（冷色，如远处墙壁），生成的运动序列在所有视角下均与场景几何保持一致。

此外，SIF3D的局部场景显著性热力图随时间动态变化（时间间隔2秒），直观展示了SCA模块如何为每帧姿态自适应地关注不同的场景区域。

### 公平性说明

对于原本不使用场景或注视模态的基线方法（如LTD、SPGSN），实验在比较时均额外拼接了全局场景嵌入和注视嵌入，确保对比的公平性。SIF3D在同等输入条件下的优势，归因于其结构化的显著性建模而非简单的信息增量。

### 局限性与失败模式

尽管SIF3D在确定性预测上表现优异，论文明确指出了以下局限：

1. **缺乏多样性建模**：当前框架专注于单模态确定性预测，未涉及多模态运动生成中的多样性问题，无法为同一输入生成多种合理运动。
2. **动态场景与人-物交互未验证**：实验场景均为静态3D环境，对包含移动物体或需要抓取、操作物体的复杂交互任务尚未进行验证。
3. **注视数据的近似性**：GTA-1M数据集缺少真实人类注视数据，采用近似估计，可能影响意图建模的准确性，该结论在GTA-1M上的泛化性需谨慎解读。



## 定位与知识库关联

### 1. 与基线方法的关系

SIF3D 的核心突破在于将 3D 场景感知从“全局嵌入”范式推进到“显著性区分”范式。在 SIF3D 之前，场景感知的人体运动预测方法普遍采用统一的场景编码策略：

- **BiFu**（Zheng et al., ECCV 2022）是该方向最具代表性的强基线，它通过双向融合网络将运动序列与全局场景嵌入进行交互，但在场景建模上存在根本缺陷——同等对待所有场景点，无法区分哪些点对当前运动意图具有更高显著性。如 Figure 1 和 Figure 3 所示，这种无差别处理导致预测的人体网格频繁与环境几何发生穿透或失真。

- **LTD**（Mao et al., ICCV 2019）和 **SPGSN**（Li et al., ECCV 2022）分别代表了轨迹依赖建模和骨架姿态预测的经典范式，但它们原始版本均未引入场景和注视模态。**AuxFormer**（Xu et al., ICCV 2023）则通过辅助任务增强 Transformer 的运动预测能力，同样缺乏对 3D 场景的显式利用。

SIF3D 相对于这些基线做出了三个关键的方法论改进：

1. **从全局到显著**：TIA 模块通过全局运动表示与场景点云的交叉注意力（Eq. 7），显式计算每个场景点的全局显著权重；SCA 模块进一步为每帧姿态独立计算局部显著权重（Eq. 13），两者相乘实现非显著点的有效抑制。

2. **三模态互补融合**：同时引入 3D 场景点云和人类注视序列，并通过 TIA 和 SCA 实现跨模态交互。Table 1 的消融实验表明，同时加入场景和注视信息在所有基线上均带来一致增益，而 SIF3D 受益最大——这验证了三模态设计的互补性并非简单叠加，而是通过显著性机制实现了信息的有效整合。

3. **轨迹与姿态的解耦预测**：TIA 输出专用于全局轨迹规划（TrajectoryPlanner），SCA 输出专用于局部姿态预测（PosePredictor），避免了以往方法中两者共享相同特征导致的目标冲突。

### 2. 适用边界与技术局限

尽管 SIF3D 在 GIMO 和 GTA-1M 两个基准上取得了显著提升（终点轨迹误差分别降低 61mm 和 67mm），其适用边界仍存在明确约束：

**场景静态性假设**：SIF3D 的显著性建模依赖于静态 3D 点云，TIA 和 SCA 的注意力计算均假设场景几何在预测期间保持不变。对于包含移动物体、动态障碍或可变家具布局的真实场景，当前框架无法适应场景点的动态变化。

**人-物交互的缺失**：当前工作专注于人体与场景几何的空间一致性（避免穿透），但未涉及抓取、操作物体等复杂交互行为。这些行为不仅需要场景几何信息，还要求对物体功能可供性（affordance）和物理属性的理解。

**确定性预测的局限**：SIF3D 是一个确定性预测器，给定相同输入总是输出相同结果。在真实应用中，同一场景下人类可能采取多种合理运动路径（如绕过桌子左侧或右侧），确定性框架无法捕捉这种多模态性。

**注视数据的依赖性**：GTA-1M 数据集缺少真实人类注视数据，实验中采用的近似估计可能影响意图建模的准确性。在真实部署场景中，获取高质量注视数据本身就是一个工程挑战。

### 3. 开放问题与后续方向

基于 SIF3D 的方法论框架和当前局限，以下几个方向值得关注：

**动态场景下的显著性更新**：如何将 TIA/SCA 的显著性机制扩展到时变场景？一个可能的路径是引入时序场景编码器，在每一时间步更新点云特征，同时保持显著性计算的效率。

**多样化运动生成**：在 SIF3D 的框架上引入条件生成机制（如扩散模型或 CVAE），在保持场景一致性的同时生成多样化的合理运动轨迹，是自然且迫切的方向。

**人-物交互的显著性扩展**：将场景点云扩展为包含物体实例的语义图，使 TIA 能够关注与任务目标相关的物体点，SCA 能够为手部姿态预测提供物体几何约束，有望将框架推广到操作任务。

**真实场景部署**：从 GIMO 的室内扫描场景和 GTA-1M 的游戏渲染场景迁移到真实世界的动态环境，需要解决传感器噪声、部分遮挡和实时性要求等工程问题。Table 5 显示场景点云从 512 增至 4096 时性能持续提升，但进一步增大则饱和，这为实际部署中的分辨率选择提供了参考。



## 原文 PDF

![[paperPDFs/CVPR_2024/SIF3D_Multimodal_Sense_Informed_Forecasting_of_3D_Human_Motions.pdf]]
