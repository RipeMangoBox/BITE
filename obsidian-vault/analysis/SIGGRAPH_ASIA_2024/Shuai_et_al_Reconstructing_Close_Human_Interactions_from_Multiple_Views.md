---
title: Reconstructing Close Human Interactions from Multiple Views
type: paper
paper_level: A
venue: SIGGRAPH ASIA
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_ASIA_2024/Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views.pdf
aliases:
- RCHIFMV
tags:
- SIGGRAPH_ASIA_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 利用所有个体的估计3D中心构建锚点引导特征体积（anchor-guided feature volumes），作为条件信号输入网络以明确区分个体；采用两阶段网络（HEM过滤噪声＋KLM结合锚点体积定位），并完全使用合成数据训练。
primary_logic: 仅依赖2D关键点热图输入，使网络可完全通过合成数据训练，摆脱真实数据依赖；通过锚点引导的条件体积有效消除近距离遮挡带来的特征歧义，实现高精度且强泛化能力的多人3D姿态估计。
claims:
- 在CHI3D数据集上，本方法3DPCK@50mm达到94.30%，大幅超越现有方法。
- 在Hi4D数据集上，本方法在无训练情况下取得最低MPJPE=20.28mm和最高PCK@50=98.29%。
- 移除3D热图监督后MPJPE升至24.53mm，PCK@50降至91.58，证明该模块关键。
- 移除条件输入后MPJPE升至22.02mm，PCK@50降至95.56，证明锚点引导体积的有效性。
---

# Reconstructing Close Human Interactions from Multiple Views

> [!tip] 核心洞察
> 仅依赖2D关键点热图输入，使网络可完全通过合成数据训练，摆脱真实数据依赖；通过锚点引导的条件体积有效消除近距离遮挡带来的特征歧义，实现高精度且强泛化能力的多人3D姿态估计。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于多视角的近距离人体交互重建 |
| 英文题名 | Reconstructing Close Human Interactions from Multiple Views |
| 会议/期刊 | SIGGRAPH ASIA 2024 |
| Links | [Project](https://github.com/zju3dv/CloseMoCap) · [Code](https://github.com/zju3dv/CloseMoCap") |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | CloseMoCap |
| Dataset | CHI3D, Hi4D, Panoptic |

> [!tip] 效果简介
> - CHI3D 上，3DPCK@50mm 94.30。
> - Hi4D 上，MPJPE 20.28；PCK@50 98.29。
> - Panoptic 上，AP_25 86.16。

## 概述

### 问题背景与核心瓶颈

多视角人体3D姿态估计在近距离交互场景下面临两大核心挑战。其一，**特征体积歧义**：当两人身体极为接近时，基于骨盆中心构建的关键点特征体积高度相似，网络难以区分不同个体的关键点响应，产生严重的个体混淆（见Fig. 2）。其二，**真实标注数据稀缺**：真实多视角图像与3D姿态的配对标注获取成本极高，且不同数据集的相机配置差异巨大（见Fig. 3），导致模型泛化能力受限。

### 核心方法与技术定位

**CloseMoCap** 提出了一种完全基于合成数据训练的3D条件体积网络，以解决上述瓶颈。其核心思路可概括为两点：

1. **锚点引导条件体积**：利用所有个体的估计3D中心构建正/负锚点引导特征体积，作为条件信号显式输入网络，从而消除近距离遮挡带来的特征歧义。
2. **两阶段网络架构**：第一阶段3D热图估计模块（HEM）从关键点特征体积中过滤噪声，输出清理后的全体热图；第二阶段关键点定位模块（KLM）融合清洗热图与锚点引导体积，回归目标个体的关键点概率体积。

由于网络仅依赖2D关键点热图作为输入（而非原始RGB图像），结合已知的相机参数和MoCap数据，可完全通过合成2D热图-3D姿态对进行训练，彻底摆脱对真实标注数据的依赖。

### 主要结论与证据强度

该方法在多个公开数据集上取得了显著领先的性能：

- 在 **CHI3D** 数据集上，3DPCK@50mm达到 **94.30%**，大幅超越现有方法（见Table 1，置信度0.98）。
- 在更具挑战性的 **Hi4D** 数据集上，以零训练（zero-shot）方式取得最低MPJPE **20.28mm** 和最高PCK@50 **98.29%**（见Table 2，置信度0.98），展现出极强的泛化能力。
- 在 **Panoptic** 数据集上，AP_25达到 **86.16%**（见Table 3，置信度0.95）。

消融实验进一步验证了关键设计的有效性：移除3D热图监督后MPJPE从18.78mm升至24.53mm；移除锚点引导条件输入后MPJPE从18.78mm升至22.02mm（见Table 4，置信度0.95）。此外，仅使用一半CMU MoCap数据时性能几乎不变（MPJPE 18.96 vs 18.78），表明合成数据策略的数据效率极高。

### 局限与开放问题

当前方法仍存在若干局限：（1）仅以2D关键点热图为输入，未利用Part Affinity Fields等肢体连接信息；（2）仅输出身体关键点，缺少手部和面部细节；（3）训练过程未融入时序或空间运动先验，仅在推理时进行简单时序过滤；（4）高度依赖前端2D关键点估计质量。未来方向包括融合2D肢体关联特征、引入参数化人体模型与时序运动先验，以及在更大规模动态场景中维持实时性与鲁棒性。

## 背景与动机

多视角3D人体姿态估计是计算机视觉与图形学交叉领域的核心问题，其目标是从一组已标定的多视角图像中恢复场景中所有个体的精确三维骨骼姿态。这一技术在角色动画、自由视点视频合成、运动分析等应用中具有广泛需求。然而，当场景中多个个体发生近距离交互（如拥抱、握手、双人舞蹈）时，现有方法面临两类根本性挑战。

**第一重挑战来自2D观测层面的歧义。** 近距离交互导致严重的个体间遮挡（inter-person occlusion），使得单视角2D关键点检测器难以准确区分属于不同个体的身体部位。如图2所示，当两人紧密接触时，2D关键点的归属变得高度模糊——同一个图像位置可能同时对应两个个体的不同关节。

**第二重挑战来自3D特征层面的混淆。** 对于主流的基于学习的多视角方法（如**VoxelPose**，Tu et al., ECCV 2020），其核心思路是为每个个体构建以骨盆中心为原点的特征体积（feature volume），然后通过3D卷积网络从该体积中回归关键点位置。然而，当两个个体空间距离极近时，他们各自的骨盆中心位置高度接近，导致构建出的特征体积在空间分布上几乎不可区分。网络在接收到两个高度相似的特征体积后，无法可靠地判断某个3D位置的响应究竟来自目标个体还是其交互伙伴，从而在输出端产生严重的歧义性。

**第三重挑战来自数据层面的约束。** 真实场景的多视角3D姿态标注成本极高，现有数据集（如Panoptic、CHI3D、Hi4D）在相机配置、场景规模、交互类型上差异显著（图3），导致在某一数据集上训练的模型难以泛化到其他配置。这意味着，若要部署到新环境（如篮球场），通常需要重新采集并标注该场景的真实数据，这在实际应用中几乎不可行。

上述三重挑战共同构成了本文的核心研究动机：**如何设计一种既能消除近距离交互下的特征歧义，又能摆脱对真实标注数据依赖的多视角多人3D姿态估计方法？** 本文提出的CloseMoCap系统正是围绕这一核心问题展开。

## 核心创新

CloseMoCap 的核心创新在于通过**锚点引导的条件体积**（anchor-guided feature volumes）和**两阶段网络结构**，系统性地解决了近距离人体交互下的特征歧义问题，同时实现了**完全脱离真实数据的合成训练范式**，展现出极强的泛化能力。

### 瓶颈洞察：近距离交互下的特征歧义

在多视角3D姿态估计中，现有学习式方法（如 **VoxelPose**（Tu et al., ECCV 2020）、**Faster-VoxelPose**（Ye et al., ECCV 2022））通常以个体的骨盆中心为参考构建特征体积。然而，当两人近距离交互时（如拥抱、握手），其骨盆中心空间位置极为接近，导致构建出的特征体积高度相似。网络难以区分不同个体的关键点响应，产生严重的输出歧义（Fig. 2）。此外，真实多视角交互场景的3D标注数据稀缺且采集成本高昂，进一步限制了模型的泛化能力。

### 关键因果调控：锚点引导特征体积

针对上述瓶颈，CloseMoCap 引入了**锚点引导特征体积**作为条件信号，显式告知网络目标个体与非目标个体的空间位置信息。具体而言：

- **正锚点体积**：以目标个体的估计3D中心 $\mathbf{c}^i$ 为锚点，构建高斯响应体积 $\mathbf{Z}^{i} = \exp \left( - \frac{1}{2 \sigma^{2}} || \mathbf{x} - \mathbf{c}^{i} ||_{2}^{2} \right)$，为正条件信号（Eq. 2）。
- **负锚点体积**：对其他所有个体的正锚点体积取逐元素最大值 $\mathbf{Z}_{o}^{i} = \max_{k} \mathbf{Z}^{k}$，用于抑制非目标关键点响应（Eq. 3）。

这一设计将个体区分问题转化为网络的条件输入，使网络能够根据锚点信号明确聚焦于目标个体的关键点定位。

### 两阶段网络：从噪声过滤到精确定位

CloseMoCap 将传统的单阶段特征体积到关键点概率体积的直接回归，改造为两阶段级联结构（Fig. 6）：

1. **3D热图估计模块（HEM）**：第一阶段从关键点特征体积 $\mathbf{F}^{i}$ 预测清理后的全体3D热图 $\hat{\mathbf{H}}^{i} = \mathrm{CNN}_{\mathrm{HEM}}(\mathbf{F}^{i})$（Eq. 4），过滤掉由遮挡和歧义引入的噪声响应。
2. **关键点定位模块（KLM）**：第二阶段融合清理后的热图 $\hat{\mathbf{H}}^{i}$、正锚点体积 $\mathbf{Z}^{i}$ 和负锚点体积 $-\mathbf{Z}_{o}^{i}$，回归目标个体的关键点概率体积 $\mathbf{P}^{i} = \mathrm{CNN}_{\mathrm{KLM}}(\hat{\mathbf{H}}^{i}, \mathbf{Z}^{i}, -\mathbf{Z}_{o}^{i})$（Eq. 5）。

消融实验证实了这两个设计的有效性：移除3D热图监督后，CHI3D上MPJPE从18.78mm升至24.53mm，PCK@50从97.12降至91.58；移除条件输入后，MPJPE升至22.02mm，PCK@50降至95.56（Table 4）。

### 纯合成训练范式

CloseMoCap 的输入仅为2D关键点热图，而非原始图像。这一设计使得网络训练完全摆脱对真实多视角图像的依赖：只需利用已知的3D姿态数据和相机参数，即可合成多视角2D热图-3D姿态对进行训练（Section 3.4, Fig. 7）。该方法在CHI3D数据集上以94.30%的3DPCK@50mm大幅超越所有基线方法，在Hi4D数据集上更以零训练样本取得最低MPJPE=20.28mm和最高PCK@50=98.29%（Table 1, Table 2），充分证明了其强大的跨数据集泛化能力。

## 整体框架

CloseMoCap 的整体 pipeline 遵循“2D 感知 → 3D 中心估计 → 条件体积构建 → 两阶段 3D 回归”的递进结构，其核心设计目标是**在近距离人体交互场景下消除特征歧义，并实现完全脱离真实标注数据的训练**。

系统输入为**多视角同步图像及已知的相机参数**（内参 $\mathbf{K}_v$、外参 $\mathbf{R}_v, \mathbf{t}_v$），输出为场景中所有个体的 3D 骨架关键点坐标。整个流程如 Fig. 4 所示，包含以下关键模块：

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of our method. For a multi-view scene, we first estimate (a) the 2D keypoint heatmaps of all people from input images. We then recover (b) the 3D centers of all people from these heatmaps. Following this, we construct keypoint feature volumes and anchor-guided feature volumes, which are subsequently fed through (c) the pose estimation network. The proposed network initially predicts the 3D heatmaps from the keypoint feature volumes and then utilizes these 3D heatmaps along with the anchor-guided feature volumes to generate (d) the 3D keypoints for each person. If the 3D keypoints from the previous time step are available, they can be used to filter the 3D heatmaps. The entire n...*

1.  **2D 关键点热图估计**：使用 HRNet 从各视角图像中提取所有个体的 2D 关键点热图 $\mathbf{h}_v$。这是整个系统唯一的图像域操作，后续所有 3D 推理均仅依赖这些热图，使得网络可以完全通过合成热图训练。
2.  **3D 中心估计与跟踪**：以骨盆点作为人体中心，从多视角 2D 热图中提取候选点并三角化得到 3D 骨盆位置，再通过重投影误差校验筛选有效中心。该模块同时支持时序跟踪，为后续锚点引导提供个体标识和空间锚点 $\mathbf{c}^i$。
3.  **特征体积构建**：对每个个体，将其骨盆中心对齐的局部空间（$2\text{m} \times 2\text{m} \times 2\text{m}$，$32 \times 32 \times 32$ 网格）中的每个 3D 点投影到各视角，采样 2D 热图响应并求平均，构建**关键点特征体积** $\mathbf{F}^i$（Eq. 1）。同时，利用估计的 3D 中心生成**锚点引导特征体积**作为条件信号——正锚点体积 $\mathbf{Z}^i$ 为以自身中心为源的高斯响应（Eq. 2），负锚点体积 $\mathbf{Z}_o^i$ 为其他个体锚点响应的逐元素最大值（Eq. 3）。
4.  **两阶段 3D 姿态回归网络**：
    - **第一阶段——3D 热图估计模块 (HEM)**：以关键点特征体积 $\mathbf{F}^i$ 为输入，通过 3D 卷积网络输出清理后的全体 3D 热图 $\hat{\mathbf{H}}^i$（Eq. 4），其作用是**过滤由 2D 热图噪声和多人混淆引入的伪响应**。
    - **第二阶段——关键点定位模块 (KLM)**：将清理后的热图 $\hat{\mathbf{H}}^i$ 与锚点引导体积 $\mathbf{Z}^i, -\mathbf{Z}_o^i$ 拼接，通过另一个 3D 卷积网络回归目标个体的关键点概率体积 $\mathbf{P}^i$（Eq. 5）。最终对概率体积求期望得到 3D 关键点坐标 $\hat{\mathbf{y}}_j^i$（Eq. 6）。
5.  **可选的时序过滤**：若前一帧关键点已知，可利用距离阈值 $r = 0.05\text{m}$ 对当前帧热图进行掩码过滤（Eq. 7），抑制瞬时错误响应。

这一 pipeline 的关键创新在于：**将个体区分问题转化为条件信号输入问题**。通过锚点引导体积，网络在回归阶段明确知晓“目标个体在空间中的位置”以及“其他个体的干扰区域”，从而在特征高度相似的近距离场景中有效消除歧义。两阶段设计则将“场景理解”（HEM 的全局热图清理）与“个体定位”（KLM 的条件回归）解耦，使网络能更稳健地处理多人遮挡。

训练时，系统完全使用**合成数据**：从 CMU MoCap 中采样多人 3D 骨架，进行随机旋转、平移和“unpose”变换（Fig. 5），再通过已知相机参数渲染为多视角 2D 热图。损失函数联合监督 3D 热图（Focal Loss）和关键点坐标（L1 Loss），如 Eq. 8 所示。这种纯合成训练策略使模型无需任何真实图像-3D 姿态配对数据，即可泛化到不同数据集、相机配置和场景规模（如篮球场，Fig. 12）。

### 补充图表

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/001_Figure_1.jpg]]
*Figure 1: Our system is designed to recover the 3D poses of individuals engaging in close-range interactions, utilizing input from multiple calibrated cameras. We introduce a novel learning-based approach that effectively handles occlusions and interactions between individuals at close quarters. The standout feature of our system, which allows it to be trained without real data, enables the system to handle various scenes, camera configurations, and number of individuals. Our system facilitates a broad range of real applications, such as character animation (top-right) and free-viewpoint video synthesis (bottom-right)*

## 核心模块与公式推导

CloseMoCap 的核心是一个**3D条件体积网络**，它接收多视角2D关键点热图，输出场景中每个个体的3D姿态。整个管线由三个紧密耦合的模块组成：特征体积构建、两阶段姿态估计网络，以及合成数据训练策略。以下按模块拆解其数学形式与设计逻辑。

### 3.1 3D中心估计与跟踪

系统首先从多视角2D关键点热图中估计每个人的3D骨盆中心。具体做法是：在各视图中选取骨盆关键点的2D候选点，利用已知的相机内参 $\mathbf{K}_v$ 和外参 $\mathbf{R}_v, \mathbf{t}_v$ 进行三角化，得到候选3D点；再通过重投影误差检验其有效性。对于时序数据，该方法支持跨帧跟踪，为后续的锚点引导体积提供稳定的个体中心 $\mathbf{c}^i$。

### 3.2 特征体积构建

这是整个方法的核心创新所在。给定第 $v$ 个视图的2D关键点热图 $\mathbf{h}_v$，对于3D空间中的任意点 $\mathbf{x}$，首先将其投影到该视图：

$$\Pi_v(\mathbf{x}; \mathbf{K}_v, \mathbf{R}_v, \mathbf{t}_v)$$

然后采样热图响应，对所有 $V$ 个视图求平均，得到**关键点特征体积**：

$$\mathbf{F}_{\mathbf{x}} = \frac{1}{V} \sum_{v} \mathbf{h}_{v} \left( \Pi_{v} ( \mathbf{x}; \mathbf{K}_{v}, \mathbf{R}_{v}, \mathbf{t}_{v} ) \right) \tag{1}$$

这个体积编码了3D空间中每个位置存在关键点的多视图一致性。然而，当两人近距离交互时，以各自骨盆为中心构建的 $\mathbf{F}^i$ 高度相似，网络难以区分不同个体的关键点响应——这是方法的**核心瓶颈**。

为解决这一歧义，CloseMoCap 引入了**锚点引导特征体积**作为条件信号。对于第 $i$ 个人，以估计的3D中心 $\mathbf{c}^i$ 为锚点，生成正、负两类引导体积：

- **正锚点引导体积**：以自身锚点为中心的高斯响应场，指示目标个体可能存在的位置：

$$\mathbf{Z}^{i} = \exp \left( - \frac{1}{2 \sigma^{2}} || \mathbf{x} - \mathbf{c}^{i} ||_{2}^{2} \right) \tag{2}$$

- **负锚点引导体积**：对其他所有个体 $k \neq i$ 的正锚点体积取逐元素最大值，形成抑制场：

$$\mathbf{Z}_{o}^{i} = \max_{k} \mathbf{Z}^{k} \tag{3}$$

正体积 $\mathbf{Z}^i$ 告诉网络“目标个体大概在这里”，负体积 $\mathbf{Z}_o^i$ 告诉网络“这里很可能是别人”。两者共同构成条件输入，使网络能够明确区分不同个体。

此外，为消除人体全局旋转对特征体积的影响，系统对2D热图施加了**“unpose”变换**：将估计的躯干部分旋转到标准空间后再构建特征体积（见 Fig. 5），使网络专注于局部姿态差异。

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/005_Figure_5.jpg]]
*Figure 5: Coordinate transformation in 3D pose estimation. We apply "unpose" operation to the estimated torso part (marked by the pink line in (a)), which is transformed into a standard space thus reducing the influence of global rotation*

### 3.3 两阶段姿态估计网络

传统方法（如 VoxelPose）直接从特征体积回归关键点概率体积。CloseMoCap 将其重构为两阶段设计（见 Fig. 6）：

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/006_Figure_6.jpg]]
*Figure 6: Two-stage design. This image highlights the main difference between our approach and the previous methods in the field. Given the feature volume obtained through multiple viewpoints (a), the previous methods directly estimate the keypoint probability volume (b) of a target person. In contrast, we propose a two-stage method. The first Heatmap Estimation Module focuses on identifying and filtering out the noise present in the input feature volume and outputs a cleaned response volume of all individuals (c), while the second Keypoint Localization Module leverages the cleaned response volume and the conditional inputs to acquire the desired keypoint probability volume for each individual. This...*

**第一阶段：3D热图估计模块 (HEM)**
从关键点特征体积 $\mathbf{F}^i$ 预测一个“清理后”的全体3D热图 $\hat{\mathbf{H}}^i$，过滤掉噪声和歧义响应：

$$\hat{\mathbf{H}}^{i} = \mathrm{CNN}_{\mathrm{HEM}}(\mathbf{F}^{i}) \tag{4}$$

**第二阶段：关键点定位模块 (KLM)**
将清理后的热图 $\hat{\mathbf{H}}^i$ 与锚点引导体积 $\mathbf{Z}^i$（正）和 $-\mathbf{Z}_o^i$（负）拼接，回归目标个体的关键点概率体积 $\mathbf{P}^i$：

$$\mathbf{P}^{i} = \mathrm{CNN}_{\mathrm{KLM}}(\hat{\mathbf{H}}^{i}, \mathbf{Z}^{i}, -\mathbf{Z}_{o}^{i}) \tag{5}$$

最终，对概率体积求期望得到每个关键点 $j$ 的3D坐标：

$$\hat{\mathbf{y}}_{j}^{i} = \sum_{l=1}^{W} \sum_{m=1}^{H} \sum_{n=1}^{D} \mathbf{P}_{j}^{i}(\mathbf{x}) \cdot \mathbf{x} \tag{6}$$

**可选的时序过滤**：若前一帧的关键点 $\hat{\mathbf{y}}_{j,t-1}^{i}$ 可用，则对当前热图施加距离阈值过滤（$r=0.05\text{m}$）：

$$\hat{\mathbf{H}}_{j}^{i}(\mathbf{x}) = \begin{cases} \hat{\mathbf{H}}_{j}^{i}(\mathbf{x}) & \text{if } \|\hat{\mathbf{y}}_{j,t-1}^{i} - \mathbf{x}\|_{2} < r \\ 0 & \text{otherwise} \end{cases} \tag{7}$$

### 3.4 合成数据训练与损失函数

CloseMoCap 的另一个关键设计是**完全使用合成数据训练**，无需任何真实图像-3D姿态配对数据。给定已知的3D姿态和相机参数，可直接渲染多视角2D关键点热图，与3D姿态构成训练对。这一策略使网络摆脱了对真实多视角标注数据的依赖。

训练损失由两部分组成——对HEM输出的3D热图施加Focal Loss，对KLM回归的坐标施加L1 Loss：

$$L^{i} = \lambda \mathrm{FocalLoss}(\hat{\mathbf{H}}^{i}, \mathbf{H}^{i}) + \frac{1}{J} \sum_{j} |\hat{\mathbf{y}}_{j}^{i} - \mathbf{y}_{j}^{i}| \tag{8}$$

其中 $\mathbf{H}^i$ 是由真值3D姿态生成的监督热图，$\mathbf{y}_j^i$ 是真值关键点坐标。消融实验证实（Table 4），移除3D热图监督后MPJPE从18.78mm升至24.53mm，PCK@50从97.12降至91.58，表明中间热图监督对网络收敛至关重要。

### 补充图表

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/002_Figure_2.jpg]]
*Figure 2: Challenges in pose estimation with close proximity. This image highlights that when two individuals are in close proximity, it becomes difficult to obtain accurate 2D pose estimates due to heavy inter-person occlusion and keypoint association ambiguity. Moreover, in learning-based methods that directly regress 3D poses from feature volumes, the similarity in constructed volumes due to their spatial closeness complicates keypoint distinction for regression networks*

## 实验与分析

### 主实验结果

CloseMoCap在多个多视角人体姿态估计基准上取得了最优结果，尤其在近距离交互场景下展现出显著优势。

**CHI3D数据集**（Table 1）：本方法在3DPCK@50mm指标上达到94.30%，大幅超越所有对比方法。值得注意的是，该方法完全使用合成数据训练，而部分对比方法（如VoxelPose、Faster-VoxelPose）直接在CHI3D真实数据上训练，仍被本方法超越，充分证明了合成训练策略与锚点引导设计的有效性。

**Hi4D数据集**（Table 2）：在零样本跨数据集泛化设定下，本方法取得MPJPE=20.28mm和PCK@50=98.29%的最优结果。Hi4D的相机布局与训练数据差异显著（Fig. 3），但本方法凭借对2D热图输入的依赖和合成训练策略，展现出极强的泛化能力。在更严格的阈值下（Fig. 9），本方法在0-100mm范围内的3DPCK曲线始终高于其他方法，且优势随阈值收紧而扩大。

**Panoptic数据集**（Table 3）：在AP_25指标上达到86.16%，验证了方法在标准多视角场景下的竞争力。使用真实图像热图训练的版本（Ours*）进一步提升性能，表明前端2D估计质量的改善可有效传递至3D输出。

### 消融实验

Table 4系统验证了各核心设计的贡献：

- **3D热图监督**：移除中间热图监督后，MPJPE从18.78mm骤升至24.53mm，PCK@50从97.12降至91.58。该监督信号迫使HEM模块学习清理特征体积中的噪声响应，为后续KLM提供高质量输入。
- **条件输入（锚点引导体积）**：移除条件输入后，MPJPE升至22.02mm，PCK@50降至95.56。这验证了正/负锚点体积对消除近距离个体间特征歧义的关键作用——网络通过条件信号明确区分目标个体与他人。
- **2D热图增强**：去除热图增强后MPJPE飙升至51.99mm（Table 6），表明合成训练中模拟真实检测噪声对弥合sim-to-real差距至关重要。
- **训练数据量**：仅使用一半CMU MoCap数据时，MPJPE为18.96mm（全量18.78mm），性能下降极小，说明方法对数据量需求不高。
- **多视角数量**：视角数从8降至4时，Hi4D上MPJPE从19.22mm增至28.85mm（Table 5），多视角覆盖对遮挡场景下的精度影响明显。

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/016_Table_5.jpg]]
*Table 5: Comparison of pose estimation performance with different numbers of views on Hi4D [Yin et al. 2023]. This table compares the performance of our proposed 3D pose estimation method with different numbers of views (4, 6, and 8). The performance metrics are MPJPE and MPJPE with ground-truth root (MPJPE w/ GT root). The lower values indicate better performance*

### 定性分析

Fig. 11对比了本方法与关联式方法的定性结果：传统自顶向下方法MV-Pose在远距离表现良好，但在近距离交互时因2D关键点关联错误而失败；自底向上方法4DA在近距离有一定鲁棒性，但仍存在关键点重建缺失；本方法在复杂近距离场景下准确重建了所有个体的姿态。

### 失败模式与局限性

尽管整体性能优异，方法存在以下局限：

1. **前端依赖**：系统高度依赖2D关键点热图质量。当2D估计误差较大（如严重遮挡、罕见姿态）时，3D重建精度会明显下降。Table 4中使用真值2D热图时MPJPE仅8.74mm，而使用估计热图为18.78mm，差距显著。
2. **肢体关联信息缺失**：当前仅以关键点热图为输入，未利用Part Affinity Fields等肢体连接特征，在极端遮挡下可能产生解剖学不合理的姿态。
3. **输出粒度有限**：仅重建身体关键点，缺少手部和面部关键点，无法捕获完整的人体运动与表情细节。
4. **运动先验缺失**：训练过程未引入时序或空间运动先验，推理时仅使用简单的基于距离的时序过滤（Eq. 7），可能丢失运动平滑性信息。

### 关键图表结论

- **Table 1**：CHI3D上3DPCK@50mm达94.30%，超越所有对比方法，包括在真实数据上训练的方法。
- **Table 2**：Hi4D零样本泛化MPJPE=20.28mm，验证合成训练策略的强泛化能力。
- **Table 4**：消融实验证实3D热图监督和条件输入各自贡献显著，移除后性能大幅下降。
- **Fig. 11**：定性对比展示本方法在近距离交互场景下相比关联式方法的鲁棒性优势。

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/008_Table_1.jpg]]
*Table 1: Evaluation on CHI3D [Fieraru et al. 2020]. We report 3D Percentage of Correct Keypoints (3DPCK) with a threshold of 50mm here, so higher is better. Our approach achieves state-of-the-art results compared to the previous methods, surpassing even learning-based methods trained on the dataset by a large margin. ‘†’ indicates the methods that are trained on Panoptic [Joo et al. 2015] with 4 camera views close to CHI3D. ‘*’ indicates the methods that are trained with synthetic data generated by their official code. ‘**’ indicates the methods that are trained on the ‘s02’ and ‘s04’ sequences of CHI3D*

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/011_Table_2.jpg]]
*Table 2: Evaluation on Hi4D [Yin et al. 2023]. We report 3DPCKs with different thresholds (50mm, 100mm, and 200mm) and MPJPE. ‘§’ indicates the methods that are trained on CHI3D [Fieraru et al. 2020] and tested on Hi4D using the 4 views close to the training ones. ‘*’ indicates the methods that are trained with synthetic data generated from CHI3D using their official code*

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/013_Table_4.jpg]]
*Table 4: Ablation study on CHI3D [Fieraru et al. 2020]. We report the MPJPE, PCK@50 for all scenarios, and PCK@50 for the ‘Hug’ scenario. This table highlights the significance of 3D heatmap supervision and conditional inputs and also shows the superior performance achieved with ground-truth 2D heatmaps*

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/015_Figure_11.jpg]]
*Figure 11: Qualitative comparison with association-based methods. This figure compares the efficacy of our method and two pose estimation methods at varying interaction distances. We render skeletons using the viewpoint of the image in the first row. The traditional top-down method MV-Pose performs well at long distances but fails at close range. The bottom-up method 4DA excels at close range, though it still fails to reconstruct some keypoints as shown in the red circle. In contrast, our method accurately reconstructs poses in this complex scenario, outperforming the other two methods*

### 补充图表

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/010_Table_3.jpg]]
*Table 3: Evaluation on Panoptic [Joo et al. 2015]. We report Average Precision (AP) with thresholds of 25, 50, and 100mm, where the higher values indicate better performance. Ours is trained using synthetic data, while Ours* is trained using heatmaps generated from images*

![[assets/figures/papers/paper_list_l1809_Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views/figures/012_Figure_9.jpg]]
*Figure 9: Evaluation on Hi4D [Yin et al. 2023] with tight thresholds. We report 3DPCKs with a tight threshold from 0 to 100mm. The results show that our method outperforms others by a large margin even in tight thresholds. The notations of methods follow those in Tab. 2*

## 方法谱系与知识库定位

### 1. 方法族谱与核心差异

CloseMoCap 属于**学习式多视角3D人体姿态估计**这一技术脉络。该脉络的核心范式是将多视角2D关键点热图通过反投影构建为3D特征体积，再使用3D CNN回归关键点概率体积。CloseMoCap 在此范式上做出了三个关键改变，使其在近距离交互场景中与基线方法形成显著差异。

#### 1.1 与体积回归方法的继承与改变

**VoxelPose** (Tu et al., ECCV 2020) 是该脉络的奠基性工作，其核心思路是：以每个个体的骨盆中心为原点构建关键点特征体积，然后使用3D CNN直接从该体积回归关键点概率体积。这一单阶段设计在个体间距较大的场景中表现良好，但在近距离交互时面临根本性困难：当两个个体身体接近时，以各自骨盆为中心构建的特征体积高度相似，网络无法区分不同个体的关键点响应，产生严重的歧义（见Fig. 2）。

**Faster-VoxelPose** (Ye et al., ECCV 2022) 是VoxelPose的实时扩展，在推理速度上做了优化，但继承了相同的单阶段回归架构和特征体积构建方式，因此在近距离交互场景中面临同样的歧义问题。

CloseMoCap 针对这一瓶颈做出了以下改变：

| 改变维度 | 基线做法 | CloseMoCap 做法 | 改变原因 |
|---------|---------|----------------|---------|
| 特征体积构建 | 仅使用骨盆中心的关键点特征体积 | 额外构建锚点引导特征体积（正：自身锚点高斯响应；负：他人锚点最大响应）作为条件输入 | 提供明确的个体区分信号，消除特征歧义 |
| 网络结构 | 单阶段从特征体积直接回归关键点概率体积 | 两阶段：3D热图估计模块（HEM）过滤噪声 + 关键点定位模块（KLM）融合锚点引导体积 | 先清理场景级噪声，再基于条件信号定位目标个体 |
| 训练数据 | 需要真实多视角图像-3D姿态配对数据 | 完全使用已知相机参数和MoCap数据合成的2D热图-3D姿态对训练 | 摆脱真实标注数据依赖，实现跨数据集泛化 |

#### 1.2 与其他学习式方法的差异

**基于图卷积的方法** (Wu et al., ICCV 2021) 将多视角2D关键点构建为图结构，利用图卷积网络进行跨视角信息融合和3D姿态回归。该方法在视角数较多时表现良好，但图结构的构建依赖于准确的2D关键点关联，在近距离遮挡导致关键点关联错误时性能会显著下降。CloseMoCap 通过体积表示绕开了显式的跨视角关键点关联步骤，避免了关联错误对3D估计的级联影响。

**Multi-view Transformer** (Wang et al., NeurIPS 2021) 使用Transformer架构直接从多视角2D关键点回归3D姿态，利用注意力机制隐式地学习跨视角对应关系。该方法在标准多视角场景中取得了有竞争力的结果，但在近距离交互场景中，Transformer的注意力图可能因相似的2D输入模式而产生混淆。CloseMoCap 的锚点引导机制提供了显式的空间先验，比隐式的注意力学习更直接地解决了个体区分问题。

### 2. 适用边界与假设条件

CloseMoCap 的有效性建立在以下关键假设之上，这些假设定义了方法的适用边界：

**（1）已知且固定的多相机标定参数。** 方法需要所有相机的内参 $\\mathbf{K}_v$、外参 $\\mathbf{R}_v, \\mathbf{t}_v$ 作为输入，用于2D热图反投影和3D中心三角化。在相机参数未知或动态变化的场景中，方法无法直接应用。

**（2）可靠的2D关键点热图估计。** 整个3D重建流程以2D关键点热图为唯一输入，因此前端2D姿态估计器的质量直接决定了3D估计的上限。消融实验（Table 6）表明，去除2D热图增强后MPJPE从18.78mm骤升至51.99mm，证明方法对2D热图质量高度敏感。在严重遮挡、极端光照或运动模糊导致2D热图质量显著下降的场景中，3D估计精度会受到严重影响。

**（3）人体中心可被可靠估计。** 锚点引导体积的构建依赖于3D骨盆中心的准确估计。如果骨盆中心因严重遮挡而无法被三角化或定位误差较大，锚点引导信号的质量会下降，进而影响关键点定位模块的性能。方法通过时序跟踪和重投影误差检查来提升中心估计的鲁棒性，但在极端遮挡下仍可能失效。

**（4）交互个体的运动模式在训练数据分布内。** 方法完全使用CMU MoCap等合成数据训练，虽然通过多人随机采样和交互动作合成增强了数据多样性，但训练数据的运动模式仍局限于现有MoCap数据集的覆盖范围。对于训练数据中未出现的极端交互姿态或运动模式，模型的泛化能力需要进一步验证。

**（5）场景规模在体积表示范围内。** 每个个体的特征体积固定为 $2\\text{m} \\times 2\\text{m} \\times 2\\text{m}$，分辨率为 $32 \\times 32 \\times 32$。这适用于室内近距离交互场景，但在篮球场等大尺度场景中（见Fig. 12），虽然方法仍能工作，但固定体积范围可能限制对远距离个体的精细重建。

### 3. 已知局限

**（1）仅以2D关键点热图为输入，未利用肢体连接信息。** 当前方法仅使用关键点位置的热图响应，未利用Part Affinity Fields（PAFs）等肢体连接信息。在复杂多人场景中，肢体连接信息可以帮助网络理解关键点之间的从属关系，减少跨个体的关键点混淆。这一局限在论文的开放问题中被明确提及。

**（2）输出仅为身体关键点，缺少手部和面部细节。** 方法仅估计躯干和四肢的关键点（遵循COCO/MPII关键点定义），不包含手部和面部关键点。对于需要完整人体运动捕捉的应用（如虚拟现实、精细动画），这一输出粒度不足。扩展到包含手部和面部关键点需要处理更高分辨率的体积表示和更复杂的自遮挡问题。

**（3）训练过程未使用运动先验。** 方法在训练时仅使用单帧的合成数据，未引入时序运动先验（如人体运动的速度、加速度约束）或空间交互先验（如接触约束）。推理时的时序过滤（Eq. (7)）仅是基于前一帧关键点距离的简单硬阈值过滤（$r=0.05\\text{m}$），可能丢失有效的运动模式信息，且在快速运动场景中可能错误抑制正确的关键点响应。

**（4）未与参数化人体模型集成。** 当前输出为独立的3D关键点坐标，未拟合到参数化人体模型（如SMPL/SMPL-X）。这限制了方法在以下方面的应用：物理合理性约束（如肢体长度一致性、关节角度限制）、表面接触建模（对于交互场景尤为重要）、以及下游的动画和渲染任务。

**（5）对2D估计误差的级联敏感性。** 整个流程是级联式的：2D热图估计 → 3D中心估计 → 特征体积构建 → 3D姿态回归。前端模块的误差会向后传播和放大。虽然方法通过合成数据增强（热图噪声模拟）提升了鲁棒性，但级联架构本身缺乏端到端的误差纠正机制。

### 4. 开放问题与未来方向

基于论文明确提出的开放问题和方法的已知局限，以下方向值得进一步探索：

**（1）融合Part Affinity Fields等2D肢体连接特征。** 将PAFs或类似的2D肢体连接信息作为额外输入通道，与关键点热图一起构建特征体积，可能增强网络对肢体关联的理解，减少跨个体的关键点混淆。这需要设计合适的3D肢体连接表示，并将其有效融入现有的体积回归框架。

**（2）集成参数化人体模型与物理约束。** 将3D关键点稳健地拟合到SMPL/SMPL-X等参数化模型，并引入表面接触损失（鼓励交互个体的接触表面在空间上一致）和物理合理性约束（如穿透惩罚），可以提升重建结果的物理合理性和动画可用性。这需要解决从稀疏关键点到密集模型参数的鲁棒拟合问题，特别是在关键点存在估计误差时。

**（3）引入时序和空间运动先验。** 将时序运动先验（如HUMOR等学习式人体运动模型）和空间交互先验融入训练过程，而非仅在推理时进行简单过滤，有望提升运动建模能力和时序一致性。这需要设计合适的训练策略，使网络能够在合成数据训练阶段学习到运动模式的隐式表示。

**（4）扩展至更大规模动态场景的实时处理。** 在篮球场等大尺度、多人的动态场景中（如Fig. 12所示），如何维持系统的实时性和鲁棒性是一个开放挑战。这涉及：自适应体积范围调整（根据个体在场景中的分布动态调整体积大小和位置）、计算效率优化（稀疏体积表示、级联分辨率）、以及多人场景的并行化处理策略。

**（5）减少对多视角的依赖。** 消融实验（Table 5）表明，视角数从8减至4时MPJPE从19.22mm增至28.85mm，性能下降明显。探索如何在更少视角（如2-3个）下维持可接受的精度，将扩展方法的实际部署范围。这可能涉及更强的时序先验、场景几何约束、或与单目人体姿态估计方法的融合。

## 原文 PDF

![[paperPDFs/SIGGRAPH_ASIA_2024/Shuai_et_al_Reconstructing_Close_Human_Interactions_from_Multiple_Views.pdf]]