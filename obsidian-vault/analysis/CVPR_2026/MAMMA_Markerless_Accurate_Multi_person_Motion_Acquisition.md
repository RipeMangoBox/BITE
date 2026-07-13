---
title: "MAMMA: Markerless Accurate Multi-person Motion Acquisition"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MAMMA_Markerless_Accurate_Multi_person_Motion_Acquisition.pdf
project_link: null
code_link: null
aliases:
- MAMMA
tags:
- CVPR_2026
- topic/pose_trajectory_control
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/motion_animation
core_operator: 密集表面标志点预测的准确性、鲁棒性，以及可见性/接触概率估计的质量。
primary_logic: 通过为每个标志点学习独立的查询向量（landmark queries），并结合分割掩码条件与多任务预测（可见性、接触），Transformer解码器能够更精确地定位密集表面点，从而在无任何姿态先验的情况下，通过优化重投影误差即可恢复准确的SMPL-X参数。
claims:
- MAMMA在MammaEval-Extra上平均每标记器误差为22.481mm，与商业标记系统MoSh++的差距仅为0.862mm。
- MAMMA-C在Hi4D数据集上MPJPE达到12.44mm，大幅领先之前方法。
- 在Harmony4D、CHI3D和MammaEval-D上，MAMMA-C显著减少了平均穿透深度和穿透顶点数（如深度8.46mm vs 9.84mm GT）。
- MammaNet在未曾训练的极端瑜伽姿势（MOYO）上仍能正确预测标志点，展示出强泛化能力。
---

# MAMMA: Markerless Accurate Multi-person Motion Acquisition

> [!tip] 核心洞察
> 通过为每个标志点学习独立的查询向量（landmark queries），并结合分割掩码条件与多任务预测（可见性、接触），Transformer解码器能够更精确地定位密集表面点，从而在无任何姿态先验的情况下，通过优化重投影误差即可恢复准确的SMPL-X参数。

| 字段 | 内容 |
|------|------|
| 中文题名 | MAMMA：无标记精确多人运动采集 |
| 英文题名 | MAMMA: Markerless Accurate Multi-person Motion Acquisition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.13040) |
| Topic | #topic/pose_trajectory_control #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/motion_animation |
| Method | MAMMA |
| Dataset | RICH, MOYO, Harmony4D, MammaEval-D |

> [!tip] 效果简介
> - RICH (单人2D标志点) 上，Mean 2D Euclidean error (pixels) 8.55 vs CameraHMR 8.84, Look-Ma* 13.26 (优于 CameraHMR 0.29px)。
> - MOYO (单人2D标志点) 上，Mean 2D Euclidean error (pixels) 11.40 vs CameraHMR 12.53, Look-Ma* 22.43 (优于 CameraHMR 1.13px)。
> - Harmony4D (双人2D标志点, IoU>0.5) 上，Mean 2D Euclidean error (pixels) 18.33 (+masks) vs CameraHMR 32.84, Look-Ma* 31.45 (优于 CameraHMR 14.51px)。

## 概要

**目标问题**：多视角视频中，当多人发生紧密交互和严重遮挡时，传统无标记运动捕捉方法难以达到与标记式系统相当的精度，且通常需要大量人工清理。

**核心思路**：MAMMA 提出一种两阶段框架——首先在所有相机视图中预测一组密集的表面虚拟标志点（512个），然后通过优化重投影误差直接拟合 SMPL-X 参数化人体模型，全程不使用任何姿态先验或回归初始化。

**关键创新**：
- **独立标志点查询**：为每个标志点学习独立的查询向量（landmark queries），而非使用单一可学习 token，使 Transformer 解码器能够更精确地定位密集表面点。
- **掩码条件与多任务预测**：引入实例分割掩码条件，同时预测标志点坐标、不确定性、可见性概率及接触概率，有效解决多人场景中的身份歧义和穿透问题。
- **无先验拟合**：仅通过最小化相机射线距离初始化 3D 位置，不依赖姿态/形状回归网络。

**主要结果**：
- 在 MammaEval-Extra 上，MAMMA 的平均每标记器误差为 **22.481 mm**，与商业标记系统 MoSh++ 的差距仅 **0.862 mm**（Table 10）。
- 在 Hi4D 数据集上，MAMMA-C 的 MPJPE 达到 **12.44 mm**，大幅领先先前方法（Table 5）。
- 在 Harmony4D、CHI3D 和 MammaEval-D 上，MAMMA-C 显著减少了平均穿透深度和穿透顶点数（Table 3）。
- 使用 SAM2 掩码后，双人交互场景的 2D 标志点误差大幅下降（Harmony4D 从 31.96 降至 18.33 像素），验证了掩码条件在解决多人歧义中的关键作用（Table 2）。

**方法定位**：MAMMA 属于基于密集表面标志点预测与多视角优化拟合的无标记运动捕捉方法，区别于依赖稀疏关键点或强姿态先验的传统多视角方法（如 Multi-view SMPLify-X），也不同于使用单 token 回归的 CameraHMR 等方案。其核心优势在于密集标志点的鲁棒预测与无先验优化，在精度上首次逼近商业标记系统。

从多视角视频中精确捕捉多人三维运动是计算机视觉与图形学领域的核心难题，在电影特效、运动分析、虚拟现实和具身智能等应用中具有广泛需求。当前，基于光学标记的商业运动捕捉系统（如 Vicon）仍是精度上的黄金标准，但其昂贵的硬件成本、繁琐的标记粘贴流程以及对受控环境的依赖，严重限制了其可及性与应用场景。

无标记运动捕捉方法旨在摆脱物理标记的束缚，仅从同步的多视角视频中恢复人体的三维姿态与形状。然而，现有方法面临一个核心瓶颈：**当多人紧密交互且存在严重遮挡时，传统无标记方法难以达到与标记系统相当的精度，且重建结果往往需要大量人工清理**。这一瓶颈的根源在于两个层面：其一，单视角下的人体检测与关键点定位在遮挡和重叠区域极易产生歧义；其二，缺乏有效的机制来显式建模人与人、人与地面的接触关系，导致重建的网格出现穿透、悬浮等物理不合理现象。

近年来，基于参数化人体模型（如 SMPL-X）的回归与拟合方法取得了显著进展。以 **CameraHMR** 为代表的方法利用 ViT 提取图像特征，通过单个可学习 token 估计全身密集表面标志点，但其设计存在关键缺陷：单个 token 难以精确编码空间分布广泛的数百个标志点的位置信息，且未预测标志点的可见性状态，导致遮挡区域的预测不可靠。**Look-Ma\*** 采用 HRNet-W48 作为骨干网络直接回归密集标志点坐标，但同样忽略了可见性建模与不确定性估计。另一方面，经典的 **Multi-view SMPLify-X** 方法依赖稀疏 2D 关键点进行多视角拟合，需要强劲的姿态先验来约束优化过程，在极端姿势和复杂交互场景下表现乏力。

更为关键的是，上述方法均未将实例分割掩码作为条件信号引入标志点预测流程。在多人重叠的场景中，缺乏身份引导的预测器难以将标志点正确分配给对应个体，导致跨视角匹配错误和后续拟合的崩溃。同时，接触信息的缺失使得优化器无法利用物理约束来消除穿透和悬浮伪影。

MAMMA 正是在这一背景下提出的。其核心动机在于：**如果能够在每个视角下精确预测一组密集的表面标志点，并同时估计其可见性、不确定性和接触概率，那么仅通过最小化重投影误差——无需任何姿态先验或学习性初始化——就能恢复出与标记系统精度相当的 SMPL-X 参数**。这一思路将问题的关键从“设计复杂的姿态先验”转移到了“提升密集标志点预测的准确性与鲁棒性”上，而后者正是 MAMMA 方法设计的核心着力点。

## 核心方法与创新机理

MAMMA 的核心创新在于将多视角无标记运动捕捉重新表述为一个**两阶段密集表面标志点驱动**的优化问题，并通过三个关键设计突破传统方法在多人紧密交互与严重遮挡场景下的精度瓶颈。

### 从稀疏关键点到密集表面标志点的范式转换

传统多视角人体重建方法（如 Multi-view SMPLify-X）依赖稀疏的 2D 关节关键点，需要强劲的姿态先验来约束优化，这在复杂交互动作中往往失效。MAMMA 转而预测覆盖全身的 **512 个密集表面标志点**（Figure 3），这些标志点从 SMPL-X 模型表面采样，密度足以同时恢复身体和手部的姿态与形状，而无需依赖任何手工姿态先验或回归网络初始化。这一范式转换使得优化过程仅需最小化标志点重投影误差即可恢复准确的 SMPL-X 参数，从根本上降低了对先验的依赖。

### 三个关键 Changed Slots

MAMMA 的密集标志点检测器 MammaNet 相较于基线方法进行了三项关键改进，构成了其性能优势的因果链条：

**1. 独立标志点查询（Landmark Queries）替代单一可学习 Token**

基线方法 **CameraHMR** 使用单个可学习嵌入来估计所有密集标志点，这种信息压缩方式限制了模型对不同身体区域的精细定位能力。MammaNet 引入 **512 个独立的可学习标志点查询**，通过 Transformer 解码器与图像特征进行交叉注意力交互。每个查询负责定位一个特定的表面标志点，使得模型能够为不同身体区域学习专门的定位策略。这一设计在极端姿势上展现出显著的泛化能力：在未曾训练的瑜伽数据集 MOYO 上，MammaNet 仍能正确预测标志点（Figure 5），而 CameraHMR 和 Look-Ma* 的误差分别高出 1.13px 和 11.03px（Table 1）。

**2. 掩码条件（Mask Conditioning）解决多人歧义**

在多人交互场景中，当两人的边界框高度重叠时，传统方法难以区分属于不同个体的像素。MAMMA 引入**分割掩码条件**机制：通过 CNN 编码器处理实例分割掩码，将其特征与图像特征进行逐元素求和融合。这一设计使得网络能够将标志点预测限定在目标个体的可见区域内。消融实验表明，掩码条件对单人场景性能提升有限，但在双人交互场景中至关重要——Harmony4D 数据集上 2D 标志点误差从无掩码的 31.96px 骤降至 18.33px（Table 2 vs Table 1），降幅达 42.6%。

**3. 可见性/不确定性/接触的多任务联合预测**

基线方法或仅预测坐标与不确定性（CameraHMR），或完全忽略不确定性（Look-Ma*），且均不预测可见性与接触。MammaNet 为每个标志点同时输出四个信号：
- **坐标** $\mu_i = [x_i, y_i]$ 及**不确定性** $\sigma_i$；
- **可见性概率** $p_i$，用于在拟合能量中自动降权或忽略被遮挡的标志点；
- **人与人接触概率** $p_c$ 和**地面接触概率** $f_l$，为后续的接触约束优化提供依据。

这种多任务设计形成了从 2D 检测到 3D 拟合的完整信息链：可见性概率使得优化器能够自动忽略严重遮挡区域（由不确定性自适应调整进一步强化），接触概率则为物理合理性约束提供了数据驱动的先验。在接触预测任务上，MammaNet 的人-人接触和地面接触 AUC 均超过 90%（Figure 6）。

### 无需姿态先验的拟合初始化

与依赖回归网络初始化姿态和形状的基线方法不同，MAMMA 的拟合过程**仅通过最小化相机射线距离来初始化 3D 位置**，完全不使用姿态/形状回归网络。这一设计消除了回归网络引入的偏差，使得最终重建质量完全取决于密集标志点的精度——这在 Vicon 标记系统对比实验中得到了验证：MAMMA 在 held-out 37 个标记上的平均每标记误差为 22.481mm，与商业标记系统 MoSh++ 的差距仅为 0.862mm（Table 10），且两种方法均未使用 GT 体型。

### 创新点的协同效应

上述三个 changed slots 并非孤立改进，而是形成了协同效应：独立查询提供了精细定位的能力基础，掩码条件解决了多人场景的身份歧义，而多任务预测则为后续优化提供了不确定性感知和物理约束的完整信息。这一协同效应在 MAMMA-C（加入接触优化阶段）上达到顶峰——在 Hi4D 数据集上 MPJPE 达到 12.44mm，大幅领先先前方法（Table 5）；在 Harmony4D、CHI3D 和 MammaEval-D 上，平均穿透深度从 GT 的 9.84mm 进一步降至 8.46mm（Table 3）。

MAMMA 采用“先感知、后拟合”的两阶段流水线，将多视角同步视频转化为 SMPL-X 参数化人体模型，全程不依赖标记点或强姿态先验。流水线的核心思想是：**密集表面标志点充当虚拟标记**——它们足够丰富以同时约束身体、手部姿态和体型，却又完全从图像中自动预测，从而绕开传统标记系统的人工粘贴与清理成本。

### 阶段一：密集标志点感知

输入为多台同步相机拍摄的 RGB 图像。系统首先利用 **SAM2** 对每一帧进行实例分割与跨帧跟踪，为每个被捕捉者生成唯一身份 ID 及对应的二值掩码。掩码在此承担两个关键角色：一是作为 **MammaNet** 的额外输入通道，通过掩码条件机制将不同个体的特征解耦，避免紧密交互时的身份混淆；二是在后续多视角匹配中辅助跨视图的人物对应。

**MammaNet** 是 MAMMA 的感知核心。其骨干为 ViT-Base 图像编码器与一个轻量 CNN 掩码编码器的组合——两者输出经逐元素求和融合，实现掩码条件注入。融合后的特征送入 Transformer 解码器，解码器使用 **N=512 个独立可学习的标志点查询向量（landmark queries）** 并行解码每个表面点的信息。每个查询向量经线性头部分别预测四项输出：

- **2D 坐标** $\mu_i = [x_i, y_i]$ 及其关联的**不确定性** $\sigma_i$
- **可见性概率** $p_i \in [0,1]$
- **人与人接触概率** $p_c$ 与**地面接触概率** $f_l$

这一设计的关键在于：每个标志点拥有独立的查询向量，使网络能够学习各点的语义先验（如“左肩点”应出现在图像左上区域），从而在严重遮挡下仍能合理推断不可见点的位置；同时，可见性预测告诉优化器哪些点可信、哪些点应降权，不确定性则为重投影误差提供自适应加权。

### 阶段二：多视角拟合优化

得到每视角、每帧的密集标志点预测后，系统进入**无回归初始化**的 SMPL-X 拟合阶段。与 CameraHMR 等方法不同，MAMMA 不使用任何网络回归的姿态或体型作为初始值——它仅通过最小化各相机中心射线的交点距离来确定每个人体的 3D 初始位置，随后使用 L-BFGS 优化器分四个阶段逐步求解 SMPL-X 参数：

1. **平移与全局旋转优化**：固定姿态和体型，仅优化根节点平移和全局朝向
2. **姿态与体型联合优化**：引入标志点重投影能量 $E_{\mathrm{ldmks}}$、形状正则项 $E_{\mathrm{shape}}$ 与时序平滑项 $E_{\mathrm{temp}}$，同时优化所有 SMPL-X 参数
3. **不确定性自适应更新**：根据当前重投影误差 $e_i$ 缩放预测的不确定性 $\sigma_i' = \sigma_i \cdot \min(\max(e_i/\tau, 0), 1)$（$\tau=10$ px），使高误差标志点在后续迭代中权重降低
4. **接触约束细化**（MAMMA-C 变体）：引入基于预测接触概率的排斥项 $E_{\mathrm{p}}$ 与吸引力项 $E_{\mathrm{c}}$，惩罚穿透并鼓励接触表面的贴合

多视角对应匹配位于阶段一与阶段二之间：利用 SAM2 的身份跟踪信息和对称极线距离 $D_g$（式 2），通过匈牙利算法建立跨视图的人物身份对应，在评估数据集上匹配成功率达 100%。

### 输入输出流总结

| 阶段 | 输入 | 输出 | 核心模块 |
|------|------|------|----------|
| 分割与跟踪 | 多视角 RGB 图像 | 逐人实例掩码 + 身份 ID | SAM2 |
| 密集标志点估计 | 图像 + 掩码 | 512 个标志点的坐标、不确定性、可见性、接触概率 | MammaNet |
| 多视角对应 | 各视角标志点 + 掩码身份 | 跨视图人物匹配关系 | 极线距离 + 匈牙利算法 |
| SMPL-X 拟合 | 匹配后的标志点集合 | SMPL-X 姿态、体型参数 | 四阶段 L-BFGS 优化 |

整个流水线**不使用时序信息进行标志点预测**（帧间独立），也不做多视角联合推断，这构成了当前框架的一个已知局限——可能导致帧间抖动，但同时也使系统对任意相机配置具备即插即用的灵活性。

MAMMA 的核心流程由两个关键阶段构成：**密集表面标志点预测（MammaNet）** 与 **基于标志点的多视角 SMPL-X 拟合优化**。前者为每帧每视角输出 512 个带有可见性、不确定性和接触概率的表面标志点；后者在无任何姿态先验的条件下，仅通过最小化重投影误差及接触约束，恢复 SMPL-X 参数。以下拆解关键模块与核心公式。

### 密集标志点预测器 MammaNet

MammaNet 以单帧图像和对应的实例分割掩码为输入，输出每个标志点的 2D 坐标、不确定性、可见性概率及接触概率。其架构设计包含三个关键改造：

- **独立标志点查询（Landmark Queries）**：与 CameraHMR 使用单个可学习嵌入解码所有标志点不同，MammaNet 学习 $N=512$ 个独立的可学习嵌入向量 $\mathbf{q}_i$，每个查询专门负责一个特定表面点。这些查询通过 Transformer 解码器与 ViT-Base 提取的图像特征进行交叉注意力，从而获得每个标志点对图像内容的精准定位能力。这一设计使得网络能够为每个标志点学习不同的定位策略，尤其有利于处理遮挡区域的标志点。

- **掩码条件融合（Mask Conditioning）**：掩码通过一个 CNN 编码器处理，将掩码特征与图像特征映射到同一空间后，通过逐元素求和（element-wise summation）进行融合。这一机制使网络明确知晓每个视角中目标人物的可见区域，从而在多人紧密交互场景下有效消除身份歧义。

- **多任务预测头**：Transformer 解码器的输出经四个并行头分别预测：
  - 标志点坐标 $\boldsymbol{\mu}_i = [x_i, y_i]$ 及不确定性 $\sigma_i$
  - 可见性概率 $p_i \in [0,1]$
  - 人与人接触概率 $p_c$
  - 地面接触概率 $f_l$

训练损失函数为：
- 坐标：高斯负对数似然损失（Gaussian NLL），以 GT 坐标 $\boldsymbol{\mu}_i'$ 为目标，$\sigma_i$ 为预测方差
- 可见性：二值交叉熵损失，以 GT 可见性 $p_i' \in \{0,1\}$ 为目标
- 接触概率：Focal Loss，以缓解正负样本不平衡

### 多视角 SMPL-X 拟合优化

给定多视角的密集标志点预测结果，MAMMA 通过 L-BFGS 优化器求解 SMPL-X 参数 $\Phi$（姿态、形状、平移）。整个优化过程不使用任何姿态先验或学习性初始化网络，仅依赖标志点重投影约束和物理合理性约束。

**初始化**：所有 SMPL-X 身体被初始放置在最小化各相机射线距离的 3D 点，无需回归网络预测初始姿态或形状。

**核心能量函数**：

$$E(\Phi; \mathbf{Q}, \mathbf{L}) = E_{\mathrm{ldmks}} + E_{\mathrm{shape}} + E_{\mathrm{temp}} + E_{\mathrm{cont}}$$

其中各项含义如下：

**（1）标志点重投影能量 $E_{\mathrm{ldmks}}$**

$$E_{\mathrm{ldmks}} = \frac{1}{C} \sum_{t,c,l} \rho\Bigg(\frac{\| \boldsymbol{\mu}_{t,c,l} - \Pi(\mathbf{V}_{t,l}, \mathbf{Q}_c) \|}{\sigma_{t,c,l}}\Bigg) p_{t,c,l}$$

- $\boldsymbol{\mu}_{t,c,l}$：第 $t$ 帧、第 $c$ 视角、第 $l$ 个标志点的预测 2D 坐标
- $\Pi(\cdot, \mathbf{Q}_c)$：使用相机参数 $\mathbf{Q}_c$ 将 SMPL-X 顶点 $\mathbf{V}_{t,l}$ 投影到图像平面
- $\sigma_{t,c,l}$：预测的不确定性，用于自适应加权——高不确定性标志点在优化中贡献较小
- $p_{t,c,l}$：预测的可见性概率，不可见标志点被完全忽略
- $\rho(\cdot)$：Geman-McClure 鲁棒核函数，抑制离群点影响

**（2）形状正则 $E_{\mathrm{shape}}$**：对 SMPL-X 形状参数施加高斯先验，防止异常体型。

**（3）时序平滑 $E_{\mathrm{temp}}$**：对相邻帧的姿态参数施加平滑约束，减少抖动。

**（4）接触约束 $E_{\mathrm{cont}}$**：包含两部分——
- **人与人排斥项**：

$$E_{\mathrm{p}} = \frac{1}{N} \sum_{i=1}^{N} \left[ - \min\big(0, \mathrm{SDF}_{\mathrm{other}}(\mathbf{v}_i) + \delta\big) \right]^2$$

惩罚顶点 $\mathbf{v}_i$ 穿透进入对方身体的深度，$\delta$ 允许少量软组织变形。

- **接触吸引项**：

$$E_{\mathrm{c}} = \frac{1}{N} \sum_{i=1}^{N} p_i \left[ \max\left(0, \mathrm{SDF}_{\mathrm{other}}(\mathbf{v}_i)\right) \right]^2$$

根据预测的接触概率 $p_i$，将位于对方表面上方但被预测为接触的顶点拉向接触面。

**不确定性自适应更新**：在优化过程中，预测的不确定性 $\sigma_i$ 根据当前重投影误差 $e_i$ 动态调整：

$$\sigma_i' = \sigma_i \cdot \min\left(\max\left(\frac{e_i}{\tau}, 0\right), 1\right)$$

其中阈值 $\tau = 10$ 像素。当重投影误差小于阈值时，不确定性被缩小，使优化器更信任该标志点；反之则放大不确定性，降低其权重。这一机制有效缓解了严重遮挡区域标志点的闪烁问题。

**多视角对应匹配**：在优化前，需建立跨视角的人物身份对应。MAMMA 利用 SAM2 提供的实例掩码进行人物跟踪，并通过对称极线距离和匈牙利算法匹配不同视角间的标志点集：

$$D_g = \frac{1}{2FN} \sum_{i=1}^{FN} \left( d(\mathbf{x}_b^i, \mathbf{F}_{ba} \mathbf{x}_a^i) + d(\mathbf{x}_a^i, \mathbf{F}_{ab} \mathbf{x}_b^i) \right)$$

其中 $d(\cdot, \cdot)$ 为点到极线的距离，$\mathbf{F}_{ba}$ 为从视角 $a$ 到视角 $b$ 的基础矩阵。在所有评估数据集上，该匹配方法的成功率达到 100%。

**优化阶段**：整个拟合过程分为四个阶段——（1）仅优化全局平移和旋转；（2）加入姿态和形状参数；（3）执行不确定性自适应更新；（4）引入接触约束项（MAMMA-C 变体）。

## 实验与关键发现

### 2D密集标志点预测评估

MammaNet在单人和多人场景下均展现出显著的2D标志点预测优势。在单人数据集上（Table 1），MAMMA在RICH上达到8.55像素的平均2D欧氏误差，优于**CameraHMR**的8.84像素和**Look-Ma***的13.26像素；在包含大量极端瑜伽姿势的MOYO数据集上，MAMMA误差为11.40像素，比CameraHMR低1.13像素，比Look-Ma*低11.03像素。值得注意的是，MAMMA在未曾训练的MOYO极端姿势上仍能正确预测标志点（Figure 5），展示了强泛化能力。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_13040/figures/005_Table_1.jpg]]
*Table 1: Dense landmark evaluation on single person datasets. Mean 2D Euclidean distance error (in pixels) between GT and predicted landmarks. Bold is the most accurate and underline is the most accurate without mask*

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_13040/figures/007_Figure_5.jpg]]
*Figure 5: Comparison on extreme poses. Ground-truth landmarks are shown in green. For each prediction, landmarks are color-coded: red indicates higher pixel error, green indicates lower pixel error. We compare networks trained on BEDLAM*

掩码条件（mask conditioning）的消融实验揭示了其在不同场景下的差异化作用：在单人场景中，掩码带来的提升有限（Table 1中加下划线者为无掩码最优）；但在双人紧密交互场景中，掩码成为关键因素。以Harmony4D为例（Table 2），当两人IoU>0.5时，加入SAM2掩码后MAMMA的误差从无掩码的31.96像素骤降至18.33像素，降幅达42.6%，而CameraHMR和Look-Ma*在相同条件下误差均超过31像素。这表明掩码条件通过为网络提供明确的身份信息，有效解决了多人遮挡和歧义问题。

### 3D身体拟合精度

MAMMA在3D拟合任务上全面超越现有方法（Table 4）。在RICH数据集上，MAMMA的MPJPE为22.20mm，比CameraHMR低3.41mm，比经典的**Multi-view SMPLify-X**低73.98mm；PVE为19.76mm，同样显著优于各基线。在双人舞蹈数据集MammaEval-D上，MAMMA的MPJPE为17.71mm，比CameraHMR低2.70mm。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_13040/figures/010_Table_4.jpg]]
*Table 4: Benchmark 3D fitting errors (mm)*

在Hi4D数据集上（Table 5），MAMMA-C（加入接触优化的版本）在19个SMPL关节上达到12.44mm的MPJPE，大幅领先先前方法。更全面的基准测试（Table 8）进一步揭示：MAMMA在全身、身体和手部三个维度上均保持领先，但手部精度仍是相对薄弱的环节。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_13040/figures/018_Table_8.jpg]]
*Table 8: Full Benchmark 3D fitting errors (mm). We evaluate the error for the full body, only for the body, and only for the hands*

### 接触优化与穿透消融

接触预测和优化是MAMMA-C的核心贡献。接触预测的ROC评估（Figure 6）显示，地面接触和人人接触预测的AUC均超过90%，但论文同时指出接触概率预测较为保守（最高约60%），源于单视角歧义——两人靠近但未接触时容易被误判。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_13040/figures/008_Figure_6.jpg]]
*Figure 6: ROC curve evaluation of our contact predictions*

Table 3的穿透消融实验量化了接触优化的效果：在Harmony4D、CHI3D和MammaEval-D三个数据集上，MAMMA-C的平均穿透深度和穿透顶点数均显著低于MAMMA（无接触优化）和GT。例如在Harmony4D上，MAMMA-C的平均穿透深度为8.46mm，而MAMMA为10.50mm，GT为9.84mm。这表明接触项不仅减少了穿透，甚至在某些情况下优于GT的物理合理性。

### 训练数据消融

Table 7的训练数据消融实验表明，使用MammaSyn+BEDLAM联合训练比仅用BEDLAM显著降低标志点误差。在MOYO数据集上，联合训练误差为6.95像素，而仅用BEDLAM为11.92像素；在交互序列上同样观察到一致提升。这验证了MammaSyn数据集中丰富的人体交互和接触标注对模型鲁棒性的关键贡献。

### 与商业标记系统的对标

MammaEval-Extra实验（Table 10）是验证MAMMA实用价值的关键证据。在held-out的37个Vicon标记上，MAMMA的平均每标记器距离为22.481mm，与基于标记的商业系统**MoSh++**的21.619mm仅相差0.862mm。这一差距在统计上极为接近，且MAMMA完全无需物理标记和人工清理，证明了无标记方法在精度上已可对标标记系统。

![[assets/figures/papers/paper_list_l25_https_arxiv_org_abs_2506_13040/figures/025_Table_10.jpg]]
*Table 10: Vicon Markers comparison experiment: Mean per-marker distance (mm) of MoSh and MAMMA on the Vicon held-out 37 markers of our MammaEval-Extra dataset*

### 多视角对应与相机数目影响

多视角对应匹配在评估数据集上达到100%的成功率，验证了基于对称极线距离和匈牙利算法的匹配策略的可靠性。相机数目消融实验（Figure 12）表明，4台相机即可获得强性能，12台相机接近最优，这为实际部署提供了灵活的配置参考。

### 失败模式与局限性

尽管整体性能优异，MAMMA仍存在若干已知失败模式：

1. **遮挡下的不确定性处理**：预测的不确定性和可见性可能导致优化器忽略严重遮挡的标志点，在时间平滑项权重较大时引发闪烁或过度平滑。
2. **接触预测的保守性**：接触概率预测偏向保守，增加接触损失权重可能导致假阳性，在真假接触的边界区域尤为明显。
3. **地面接触与鞋高**：地面接触预测受鞋子高度影响，若过度惩罚接触误差，优化器可能将人体向下拉以符合约束，而在身体已接触地面时额外接触项效果甚微。
4. **手部精度**：手部运动恢复精度仍有改进空间，这与大多数标记系统因成本原因忽略手部的现状一致。
5. **时序独立性**：当前流程不利用时序信息，标志点预测帧间独立，可能导致抖动；多视角联合预测也未实现。

## 定位与知识库关联

### 核心设计动机与瓶颈突破

MAMMA 瞄准的核心瓶颈在于：多视角视频中多人紧密交互和严重遮挡时，传统无标记运动捕捉方法难以达到与标记系统相当的精度，且需要大量人工清理。其因果调节旋钮（causal knob）落在**密集表面标志点预测的准确性与鲁棒性**，以及**可见性/接触概率估计的质量**上。核心洞察是：通过为每个标志点学习独立的查询向量（landmark queries），并结合分割掩码条件与多任务预测（可见性、接触），Transformer 解码器能够更精确地定位密集表面点，从而在**无任何姿态先验**的情况下，仅通过优化重投影误差即可恢复准确的 SMPL-X 参数。

### 与基线方法的关键差异

MAMMA 在方法设计上对多个基线工作进行了系统性改造，主要体现在以下五个“被改变的槽位”（changed slots）：

| 方法槽位 | 基线做法 | MAMMA 做法 | 证据锚点 |
|---------|---------|-----------|---------|
| **解码器 token 设计** | 单个可学习嵌入（如 **CameraHMR** ） | 512 个独立的可学习标志点查询（landmark queries） | Section 4.1, Figure 4 |
| **掩码条件** | 无掩码条件 | CNN 掩码编码器 + 逐元素求和与图像特征融合 | Section 4.1, Figure 4 |
| **不确定性与可见性预测** | 仅预测坐标和不确定性（CameraHMR）或无不确定性（**Look-Ma\***, Hewitt et al. ） | 同时预测坐标、不确定性 $\sigma$、可见性概率 $p$ | Section 4.1 |
| **接触预测** | 均无接触预测 | 预测人与人接触概率 $p_c$ 和地面接触概率 $f_l$ | Section 4.1, Section 5.2 |
| **拟合初始化** | 通常使用回归网络初始化姿态和形状（如 CameraHMR、Look-Ma\*） | 仅通过最小化相机射线距离初始化 3D 位置，无需姿态/形状回归初始化 | Section 4.2 |

具体而言：

- **相对于 CameraHMR**：CameraHMR 采用基于 ViT 的单一可学习 token 估计所有密集标志点，且不预测可见性与接触。MAMMA 将 token 扩展为 512 个独立查询，使每个标志点拥有专属表示空间，同时引入可见性概率 $p$ 和不确定性 $\sigma$ 的多任务预测分支。在 RICH 数据集上，MAMMA 的 2D 标志点误差为 8.55 px，优于 CameraHMR 的 8.84 px（Table 1）；在双人交互场景 Harmony4D 上，MAMMA 加掩码后误差为 18.33 px，大幅领先 CameraHMR 的 32.84 px（Table 2）。

- **相对于 Look-Ma\***：Look-Ma\* 基于 HRNet-W48 的密集标志点回归器仅预测坐标，缺乏不确定性和可见性建模。MAMMA 在 MOYO 极端瑜伽姿势上误差为 11.40 px，远低于 Look-Ma\* 的 22.43 px（Table 1），证明多任务预测对分布外姿势的鲁棒性优势。

- **相对于 Multi-view SMPLify-X** [8, 47]：经典多视角 SMPLify-X 依赖稀疏 2D 关键点拟合 SMPL-X，需要强劲姿态先验。MAMMA 完全摒弃姿态先验，仅依赖密集表面标志点的重投影误差进行优化。在 RICH 上，MAMMA 的 MPJPE 为 22.20 mm，而 SMPLify-X 高达 96.18 mm（Table 4），差距显著。

### 流程模块与知识库定位

MAMMA 的完整流程由四个核心模块串联：

1. **SAM2 分割与跟踪**：为每个人生成并跟踪实例分割掩码，提供身份和每帧可见区域（Section 4.3）。该模块将 MAMMA 定位在“分割引导的运动捕捉”这一支线上，与依赖边界框或全图输入的方法形成对比。

2. **MammaNet 密集标志点估计**：以图像和掩码为输入，预测每视角的 512 个密集标志点坐标、不确定性、可见性和接触概率（Section 4.1, Figure 4）。这是整个方法的核心创新模块，将密集标志点回归从“单 token 全局估计”推进到“逐点查询解码 + 多任务预测”的范式。

3. **多视角对应匹配**：利用对称极线距离和匈牙利算法建立跨视图的人物身份对应（Section 4.3）。该模块解决了多人场景下的身份歧义问题，消融实验表明匹配成功率达到 100%（Section 5.3）。

4. **SMPL-X 模型拟合优化**：通过四阶段优化（平移/旋转、姿态/形状、不确定性更新、接触约束）恢复 SMPL-X 参数（Section 4.2）。该模块将 MAMMA 定位为“优化驱动”而非“回归驱动”的方法，与端到端回归方法（如 CameraHMR 的回归初始化）形成方法论分支。

### 适用边界与局限

尽管 MAMMA 在多个基准上表现优异，其适用边界和局限值得关注：

- **不确定性与可见性机制的双刃剑效应**：预测的不确定性和可见性可能导致优化器忽略严重遮挡且高度不确定的标志点，从而引起闪烁或过度平滑，尤其在时间平滑项权重较大时。这意味着在极端遮挡场景下，重建质量可能退化。

- **接触预测的保守性**：接触概率预测较为保守（最高约 60%），源于单视角歧义——两人靠近但未接触时容易被误判。增加接触损失权重可能导致假阳性穿透约束，这限制了在精细交互场景（如格斗、拥抱）中的接触建模精度。

- **地面接触的鞋子敏感性**：地面接触预测受鞋子高度影响，若过度惩罚接触误差，优化器可能将人体向下拉以符合接触约束；而在身体已接触地面时额外接触项效果甚微。这表明该方法对鞋类变化缺乏自适应能力。

- **手部运动恢复精度有限**：当前大多数标记系统因成本原因也忽略手部，MAMMA 在手部运动恢复上仍有改进空间，尤其是在手指交互场景。

- **时序信息缺失**：当前流程不利用时序信息，标志点预测帧间独立，可能导致抖动；多视角联合预测也未实现。这限制了在快速运动或低帧率场景下的平滑性。

- **分割掩码依赖性**：当 SAM2 等分割模型丢失身体部分（如两人过于靠近时），掩码条件可能失效。消融实验显示掩码对单人性能提升有限，但对双人交互场景至关重要（Harmony4D 误差从 31.96 降至 18.33，Table 1 vs Table 2），说明掩码质量是多人场景的性能瓶颈。

### 开放问题

基于上述局限，以下开放问题值得后续工作关注：

1. **多视角联合预测**：如何通过多视角联合预测改进标志点的时空一致性，减少帧间抖动？
2. **运动先验引入**：能否引入扩散模型等人体运动先验进一步细化重建，尤其在手部和遮挡场景？
3. **手部精度提升**：如何提升手部运动的捕捉精度，尤其是在手指交互场景？
4. **少相机鲁棒性**：在极少数相机（<4）且严重遮挡下如何保持鲁棒性？消融实验表明 4 台相机即可获得强性能（Figure 12），但更少相机下的退化模式尚不明确。
5. **不完整掩码适应**：当 SAM2 等分割模型丢失身体部分时，如何自动纠正或适应不完整掩码？
6. **优化加速**：是否可以将当前 L-BFGS 优化器替换为可微分优化或端到端网络，以进一步提高速度？当前优化各阶段运行时间见 Figure 13，但实时性仍是实际部署的瓶颈。

## 原文 PDF

![[paperPDFs/CVPR_2026/MAMMA_Markerless_Accurate_Multi_person_Motion_Acquisition.pdf]]
