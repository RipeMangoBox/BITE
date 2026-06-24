---
title: "Curvature-Guided Task Synergy for Skeleton based Temporal Action Segmentation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Curvature_Guided_Task_Synergy_for_Skeleton_based_Temporal_Action_Segmentation.pdf
openreview_forum_id: Vgh30npuN3
aliases:
- CGTSSBTAS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "曲率引导机制：利用分类特征轨迹的几何曲率作为边界先验，并建立双向一致性损失，使分类特征空间和边界预测构成正向循环。"
primary_logic: "在良好学习的特征空间中，动作段内轨迹因类簇约束而呈现高曲率，过渡段轨迹平直而曲率低；利用该几何特性可建立分类与定位的双向协同，形成相互强化的优化过程。"
claims:
- "高曲率的动作段内和低曲率的过渡段可作为边界精确检测的几何先验。"
- "边界定位预测反过来动态优化分类特征空间，使其几何结构更利于清晰边界。"
- "分类特征轨迹的曲率与包含超球半径成反比，实现段内高曲率、段间低曲率的理论保证。"
- "曲率引导的双向一致性损失显式建立了分类与定位任务的协同。"
---

# Curvature-Guided Task Synergy for Skeleton based Temporal Action Segmentation

> [!tip] 核心洞察
> 在良好学习的特征空间中，动作段内轨迹因类簇约束而呈现高曲率，过渡段轨迹平直而曲率低；利用该几何特性可建立分类与定位的双向协同，形成相互强化的优化过程。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 曲率引导的骨架时序动作分割任务协同 |
| 英文题名 | Curvature-Guided Task Synergy for Skeleton based Temporal Action Segmentation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Vgh30npuN3); [GitHub](https://github.com/kong-johnny/CurvSeg) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | CurvSeg |
| Dataset | PKU-MMD (X-sub), LARa |

> [!tip] 效果简介
> - PKU-MMD (X-sub) 上，Acc 为 74.3，对比 73.5 (LaSA)，变化 +0.8。
> - PKU-MMD (X-sub) 上，F1@50 为 65.5，对比 63.6，变化 +1.9。
> - LARa 上，Acc 为 76.6，对比 75.3 (LaSA)，变化 +1.3。

## 概述

骨架时序动作分割（STAS）旨在将连续骨架序列切分为具有语义一致性的动作段。现有主流方法普遍采用解耦架构，将动作分类与边界定位视为两个独立子任务分别优化。然而，这两个子任务对特征的需求存在内在冲突——分类要求特征具有类别不变性，而边界定位则依赖对帧间差异的敏感性——这种需求矛盾导致信息孤岛，缺乏有效的跨任务协同，成为制约分割精度的核心瓶颈。

针对这一问题，本文提出 **CurvSeg**，一种基于曲率引导的任务协同框架。其核心洞见在于：在良好学习的分类特征空间中，动作段内的特征轨迹因类簇约束而呈现高曲率，而过渡段的轨迹则相对平直、曲率较低。这一几何特性为边界检测提供了天然先验，同时边界定位的预测结果又能反向优化分类特征空间的几何结构，使其更利于清晰边界的形成。基于此，CurvSeg 构建了双向一致性损失，使分类与定位两个子任务形成相互强化的正向循环。

方法层面，CurvSeg 在两个关键维度上区别于现有工作：其一，引入**专家驱动解耦（EDD）**模块，通过空间重校准和高斯混合时间专家为分类和定位生成任务特定的特征表示，替代传统共享特征直接输入独立解码头的方式；其二，构建**曲率引导协同（CGS）**模块，利用分类特征轨迹的转向角计算归一化曲率作为边界代理，并施加双向一致性损失，显式建立跨任务协同。

在四个公开基准数据集上的实验表明，CurvSeg 在帧级准确率（Acc）和段级 F1 分数上均取得一致提升。以当前最强基线 LaSA 为参照，CurvSeg 在 PKU-MMD（X-sub）上 Acc 达到 74.3%（+0.8），F1@50 达到 65.5%（+1.9）；在 LARa 上 Acc 达到 76.6%（+1.3），F1@50 达到 59.0%（+1.1）。消融实验进一步证实，EDD 与 CGS 的增益超过各模块独立贡献之和，验证了真正的协同效应。同时，曲率作为边界代理在消融中优于欧氏距离、余弦相似度和梯度显著图等替代方案，证实了其作为几何先验的有效性。

方法仍存在若干局限：内部旋转变化等噪声可能产生虚假曲率峰，渐变过渡动作缺乏明显的曲率谷底，低动态动作的绝对分割性能仍有提升空间。这些方向为后续研究提供了明确的改进线索。

## 背景与动机

### 问题背景

时序动作分割（Temporal Action Segmentation, TAS）旨在对未修剪的长视频进行逐帧动作类别标注，是人机交互、视频理解等领域的核心任务。基于骨架的时序动作分割（Skeleton-based TAS, STAS）因其对光照、背景变化的鲁棒性和数据高效性而受到广泛关注。现有方法通常将STAS分解为两个子任务：**动作分类**（识别每帧所属的动作类别）和**边界定位**（检测动作之间的精确切换点），并采用解耦架构分别处理。

### 现有方法的核心瓶颈：信息孤岛与任务冲突

当前STAS方法的根本问题在于分类与定位两个子任务之间存在**内在需求冲突**，而现有解耦架构缺乏有效的跨任务协同机制，形成了信息孤岛：

- **分类任务**要求特征对动作类别具有高度判别性，同时具备**类内不变性**（intra-class invariance）——同一动作的不同实例、不同执行者在特征空间中应紧密聚集。
- **边界定位任务**则要求特征对动作状态变化高度**敏感**，能够精确捕捉相邻帧之间的细微差异以定位切换点。

这种"不变性 vs. 敏感性"的矛盾使得简单共享编码器特征输入两个独立解码头（如**MS-TCN++**、**ASRF**、**DeST**等方法）难以同时满足两个任务的需求。分类头倾向于抹平类内变化，而边界头则需要放大这些变化，导致两个任务相互掣肘而非相互促进。

### 核心洞察：特征轨迹的几何特性

本文的核心洞察源于对分类特征空间几何结构的观察：在良好学习的分类特征空间中，同一动作类的帧特征会形成**紧凑的聚类**。这导致一个重要的几何现象——特征序列在动作段内部因类簇约束而呈现**高曲率**的弯曲轨迹（特征在紧凑空间内不断转向），而在动作过渡段，特征从一类平滑迁移至另一类，轨迹相对平直，呈现**低曲率**。如Figure 1(c)所示，分类表征形成的紧凑簇迫使段内轨迹具有高曲率。

这一几何特性为边界检测提供了天然的、无需额外学习的先验信号：**曲率谷底对应动作边界**。

### 本文动机：构建曲率引导的双向任务协同

基于上述几何洞察，本文提出**CurvSeg**方法，核心动机是打破分类与定位之间的信息孤岛，建立**双向协同的正向循环**：

1. **分类→定位**：利用分类特征轨迹的曲率作为边界先验，引导边界定位模块精确检测切换点。
2. **定位→分类**：边界预测结果反过来动态优化分类特征空间，使其几何结构更有利于形成清晰的边界。

这种双向协同机制使得两个任务从相互掣肘转变为相互强化，形成"更好的分类特征→更清晰的曲率信号→更精确的边界预测→更优的特征空间组织"的正向循环。

## 核心创新

CurvSeg 的核心创新在于**用几何曲率打通分类与边界定位两个子任务的信息孤岛**，构建了一个相互强化的正向循环。现有骨架时序动作分割方法（如 **DeST**、**LaSA** 等）普遍采用解耦架构：共享编码器提取特征后，分类头和边界头各自独立优化。然而，这两个子任务对特征的需求本质上是冲突的——分类追求类内不变性，边界定位则要求对状态切换高度敏感。解耦虽缓解了冲突，却也切断了任务间的信息流动，使分类特征中蕴含的边界线索和定位反馈对分类空间的塑造作用双双丧失。

CurvSeg 的关键洞察是：**在良好学习的分类特征空间中，动作段内轨迹因类簇约束而呈现高曲率，过渡段轨迹因跨越不同类簇而相对平直、曲率低**。这一几何特性天然携带了边界位置的先验信息。基于此，CurvSeg 引入两个相互咬合的机制：

**1. 曲率引导的跨任务协同（CGS）**

CGS 模块从分类特征序列中计算瞬时曲率 $ \kappa_t $，将其作为边界预测的几何代理。具体而言，通过相邻差分向量的转角 $ \theta_t $ 归一化得到曲率信号：

$$ \theta_{t} = \arccos\frac{(\mathbf{F}_{cls,t} - \mathbf{F}_{cls,t-w})\cdot(\mathbf{F}_{cls,t+w} - \mathbf{F}_{cls,t})}{||\mathbf{F}_{cls,t} - \mathbf{F}_{cls,t-w}||\cdot||\mathbf{F}_{cls,t+w} - \mathbf{F}_{cls,t}||} $$

$$ \kappa_{t} = \frac{\theta_{t}}{||\mathbf{F}_{cls,t} - \mathbf{F}_{cls,t-w}|| \cdot ||\mathbf{F}_{cls,t+w} - \mathbf{F}_{cls,t}|| + \epsilon} $$

随后，CGS 施加双向一致性损失，迫使边界预测概率 $ \hat{y}_t^b $ 与曲率导出的边界度量 $ \varphi(\mathcal{C}_t) $ 相互逼近：

$$ \mathcal{L}_{curv} = -\frac{1}{T}\sum_{t=1}^{T} MSE(\hat{y}_{t}^{b}, \varphi(\mathcal{C}_{t})) + MSE(\mathcal{C}_{t}, \varphi(\hat{y}_{t}^{b})) $$

这一损失函数同时实现了两个方向的协同：曲率为边界预测提供几何先验（正向引导），边界预测的梯度则反向流入分类特征空间，动态优化其几何结构，使动作段内更紧凑、边界处更清晰（反向塑造）。消融实验证实，双向 CGS 的增益显著超过单向路径的简单叠加，证明了真正的协同效应。

**2. 专家驱动的任务自适应解耦（EDD）**

仅靠共享特征计算曲率不足以最大化协同效果。EDD 模块在解耦阶段就为两个任务生成任务特定的特征表示：通过 SE-style 空间重校准对骨架关节点进行任务相关的注意力加权，再引入高斯混合时间专家对视频段进行软性时间掩码分配，使分类专家和定位专家各自聚焦于语义信息和细粒度时序变化。消融表明，EDD 的动态路由机制优于独立编码器和金字塔解耦策略，为 CGS 提供了更高质量的曲率计算基础。

**与 baseline 的关键差异总结：**

| 机制 | 现有方法 | CurvSeg |
|------|---------|---------|
| 跨任务协同 | 无显式协同，分类与定位独立优化 | CGS 利用分类特征曲率作为边界代理，双向一致性损失建立正向循环 |
| 特征解耦 | 共享特征直接输入两个解码头 | EDD 通过空间重校准和高斯混合时间专家生成任务特定特征 |
| 时间建模 | 传统时间卷积或 Transformer 处理全局特征 | 高斯混合专家对视频段进行软性时间掩码分配，自适应加权 |

EDD 与 CGS 并非简单叠加：EDD 单独使用可一致提升所有指标，CGS 单独使用带来最大的段 F1 提升，而完整模型的增益超过各模块独立贡献之和，展现了真正的协同效应。曲率作为边界代理也优于欧氏距离、余弦相似度和梯度显著图等替代方案，验证了几何先验的独特价值。

## 整体框架

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/002_Figure_2.jpg]]
*Figure 2: Overview of CurvSeg. Our model processes video features through EDD to capture decoupled classification and localization representations utilizing task-specific experts. Subsequently, CGS leverages geometric curvature principles to guide task collaboration, enhancing both action boundary detection and classification performance*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/001_Figure_1.jpg]]
*Figure 1: (a) Existing STAS approaches. (b) The proposed method. (c) Classification representations create compact clusters, forcing high trajectory curvature within action segments. (d) Curvature-guided task collaboration*

CurvSeg 的整体设计围绕一个核心矛盾展开：骨架时序动作分割（STAS）中的动作分类与边界定位两个子任务对特征的需求是冲突的——分类要求类别内不变性，定位要求对状态转换的敏感性。现有解耦架构（如 **MS-TCN++**、**ASRF**、**DeST**、**LaSA** 等）将两个任务独立处理，形成了信息孤岛。CurvSeg 通过两个关键模块打破这一僵局：**专家驱动解耦（Expert-Driven Decoupling, EDD）** 负责任务自适应特征生成，**曲率引导协同（Curvature-Guided Synergy, CGS）** 负责建立分类与定位之间的双向正向循环。

### 整体数据流

输入为骨架序列 $\mathbf{F}_s \in \mathbb{R}^{D_{in} \times T \times V}$（$T$ 帧，$V$ 个关节点），目标是输出逐帧动作类别标签 $\mathbf{Y} \in \{1, 2, ..., C\}^{\tilde{T}}$ 和边界位置。整体流程如下：

1. **空间特征提取**：采用多尺度图卷积网络（MS-GCN）提取空间结构特征：
   $$F_{gcn} = ReLU[(A_{MS} + B) F_s W_s]$$
   其中 $A_{MS}$ 为归一化多尺度邻接矩阵，$B$ 为可训练自适应矩阵，$W_s$ 为通道调整权重。

2. **全局时序建模**：使用 Linear Transformer 捕获全局时序依赖，复杂度为 $O(n)$：
   $$F_{ST}^{l+1} = ReLU[\phi(Q_t)(\phi(K_t^\top) V_t) W_t + F_{ST}^l]$$
   其中 $\phi$ 为 sigmoid 激活函数。

3. **专家驱动解耦（EDD）**：将统一的时空特征 $F_{ST}$ 分解为分类专用特征 $F_{cls}$ 和定位专用特征 $F_{loc}$。EDD 包含两个核心机制：
   - **空间重校准**：通过 SE-style 关节点注意力，为每个关节点学习任务相关的空间权重：
     $$\mathbf{F}_{ST} := \mathbf{F}_{ST} + \mathrm{Sigmoid}\big(\mathrm{MLP}(\mathbf{z}_{st})\big) \mathbf{F}_{ST}$$
   - **高斯混合时间专家**：将视频划分为 $M$ 个片段，每个片段由 $G$ 个高斯专家进行软性时间掩码分配，专家路由权重为：
     $$\boldsymbol{\tau}^{(m)} = \mathrm{Sigmoid}(\mathbf{MLP}(\mathbf{Avg}(\mathbf{F}^{(m)}) \cdot \mathbf{W}^{g}))$$
     最终通过加权求和整合专家输出：
     $$\tilde{\mathbf{F}}^{(m)} = \sum_{i=1}^{G} \tau_i^{(m)} \mathcal{G}_i^{(m)} \mathbf{F}^{(m)}$$
     分类专家和定位专家各自独立路由，从同一编码器特征中提取任务特定表示。

4. **曲率引导协同（CGS）**：这是 CurvSeg 的核心创新。在分类特征空间 $F_{cls}$ 中计算轨迹的几何曲率：
   - 首先计算相邻差分向量的转向角 $\theta_t$：
     $$\theta_{t} = \arccos\frac{(\mathbf{F}_{cls,t} - \mathbf{F}_{cls,t-w})\cdot(\mathbf{F}_{cls,t+w} - \mathbf{F}_{cls,t})}{||\mathbf{F}_{cls,t} - \mathbf{F}_{cls,t-w}||\cdot||\mathbf{F}_{cls,t+w} - \mathbf{F}_{cls,t}||}$$
   - 再归一化为瞬时曲率 $\kappa_t$：
     $$\kappa_{t} = \frac{\theta_{t}}{||\mathbf{F}_{cls,t} - \mathbf{F}_{cls,t-w}|| \cdot ||\mathbf{F}_{cls,t+w} - \mathbf{F}_{cls,t}|| + \epsilon}$$
   - 曲率向量 $\mathcal{C}_t$ 作为边界位置的几何代理：动作段内因类簇约束轨迹弯曲，曲率高；过渡段轨迹平直，曲率低。
   - 通过双向一致性损失建立跨任务协同：
     $$\mathcal{L}_{curv} = -\frac{1}{T}\sum_{t=1}^{T} MSE(\hat{y}_{t}^{b}, \varphi(\mathcal{C}_{t})) + MSE(\mathcal{C}_{t}, \varphi(\hat{y}_{t}^{b}))$$
     其中 $\hat{y}_t^b$ 为边界预测概率，$\varphi$ 为梯度截断映射。该损失同时约束边界预测逼近曲率信号，并迫使分类特征空间向利于清晰边界的方向演化，形成相互强化的正向循环。

5. **任务头输出**：
   - 分类头基于 $F_{cls}$ 输出逐帧类别概率 $\hat{y}_{t,c}^{cl}$。
   - 边界头基于 $F_{loc}$ 输出边界概率 $\hat{y}_t^b$。

### 优化目标

总损失为三个分量的加权和：
$$\mathcal{L} = \mathcal{L}_{c} + \mathcal{L}_{b} + \lambda \mathcal{L}_{curv}$$

其中 $\mathcal{L}_c$ 为带时序平滑正则的交叉熵分类损失，$\mathcal{L}_b$ 为二值逻辑回归边界损失，$\lambda$ 为平衡系数（PKU-MMD 取 4，LARa 取 2.5，MCFS 取 2）。

### 关键设计逻辑

该框架的核心洞察在于：在良好学习的分类特征空间中，动作段内特征因向类中心聚拢而呈现高曲率轨迹，过渡段特征因类别切换而呈现低曲率直线轨迹。CGS 利用这一几何特性，将分类特征空间的结构信息转化为边界定位的先验，同时边界预测的反馈又反向优化分类特征空间，使其几何结构更利于清晰边界。EDD 则通过专家路由机制为两个任务生成适配的特征表示，避免了共享特征导致的冲突。消融实验证实，EDD 和 CGS 的联合使用产生了超越各自独立贡献之和的协同增益（Table 3），验证了“任务解耦 + 几何协同”这一设计范式的有效性。

## 核心模块与公式推导

CurvSeg 的核心架构由两个关键模块构成：**曲率引导的协同模块（CGS）** 和 **专家驱动解耦模块（EDD）**。前者利用分类特征轨迹的几何曲率建立跨任务双向协同，后者通过混合专家机制为分类和边界定位生成任务自适应特征。

### 问题形式化

给定骨架序列 $\mathbf{F}_s \in \mathbb{R}^{D_{in} \times T \times V}$（$T$ 帧，$V$ 个关节点，$D_{in}$ 输入通道），STAS 任务被分解为两个子任务：动作分类与边界定位。对应真值标签为 $\mathbf{Y} \in \{1, 2, ..., C\}^{\tilde{T}}$（$C$ 个动作类别）。

### 基础框架

空间建模采用多尺度图卷积网络（MS-GCN），通过归一化多尺度邻接矩阵 $A_{MS}$、可训练自适应矩阵 $B$ 和通道调整权重 $W_s$ 提取空间特征：

$$F_{gcn} = ReLU[(A_{MS} + B) F_s W_s]$$

时序建模采用线性 Transformer，以 $O(n)$ 复杂度捕获全局时序依赖。使用 sigmoid 激活 $\phi$ 的线性注意力机制更新时空特征：

$$F_{ST}^{l+1} = ReLU[\phi(Q_t)(\phi(K_t^\top) V_t) W_t + F_{ST}^l]$$

### 曲率引导协同模块（CGS）

CGS 的核心洞察是：在良好学习的分类特征空间中，动作段内轨迹因类簇约束呈高曲率，过渡段轨迹平直而曲率低。该几何特性可作为边界检测的先验。

**曲率计算。** 给定分类特征 $F_{cls}$，首先计算相邻差分向量的转向角：

$$\theta_{t} = \arccos\frac{(F_{cls,t} - F_{cls,t-w})\cdot(F_{cls,t+w} - F_{cls,t})}{||F_{cls,t} - F_{cls,t-w}||\cdot||F_{cls,t+w} - F_{cls,t}||}$$

其中 $w$ 为时间窗口大小。归一化瞬时曲率定义为：

$$\kappa_{t} = \frac{\theta_{t}}{||F_{cls,t} - F_{cls,t-w}|| \cdot ||F_{cls,t+w} - F_{cls,t}|| + \epsilon}$$

曲率与包含超球半径成反比，从理论上保证了段内高曲率（$\kappa_{F_T}(R_{intra})$）与段间低曲率（$\kappa_{F_T}(R_{inter})$）的几何特性。

**双向一致性损失。** 在边界预测概率 $\hat{y}_t^b$ 与曲率导出的边界度量 $\mathcal{C}_t$ 之间施加双向 MSE 约束，其中 $\varphi$ 为梯度截断操作：

$$\mathcal{L}_{curv} = -\frac{1}{T}\sum_{t=1}^{T} MSE(\hat{y}_{t}^{b}, \varphi(\mathcal{C}_{t})) + MSE(\mathcal{C}_{t}, \varphi(\hat{y}_{t}^{b}))$$

该损失显式建立分类特征空间与边界预测之间的正向循环：曲率为边界定位提供几何先验，边界预测反过来动态优化分类特征空间，使其几何结构更利于清晰边界。

### 专家驱动解耦模块（EDD）

EDD 通过空间重校准和时序混合专家机制，为分类和定位生成任务特定特征，替代传统解耦架构中共享编码器特征直接输入独立解码头的方式。

**空间重校准。** 采用 SE-style 关节点注意力，对骨架特征进行任务相关的空间重标定：

$$F_{ST} := F_{ST} + Sigmoid\big(MLP(z_{st})\big) F_{ST}$$

**时序混合专家。** 视频被划分为 $M$ 个片段，每个片段配备 $G$ 个高斯专家。专家路由权重通过 sigmoid 门控计算：

$$\tau^{(m)} = Sigmoid(MLP(Avg(F^{(m)}) \cdot W^{g})$$

各专家输出经加权求和集成：

$$\tilde{F}^{(m)} = \sum_{i=1}^{G} \tau_i^{(m)} \mathcal{G}_i^{(m)} F^{(m)}$$

该动态路由机制使分类专家聚焦语义表征，定位专家关注细粒度边界信息，实现任务自适应特征解耦。

### 总体优化目标

分类损失 $\mathcal{L}_c$ 结合逐帧交叉熵与片段平滑正则项，边界损失 $\mathcal{L}_b$ 采用二值 logistic 回归损失。最终优化目标为三者的加权和：

$$\mathcal{L} = \mathcal{L}_{c} + \mathcal{L}_{b} + \lambda \mathcal{L}_{curv}$$

其中 $\lambda$ 为平衡超参数，在 PKU-MMD 上设为 4，LARa 上设为 2.5，MCFS 数据集上设为 2。

## 实验与分析

### 核心发现与主实验

CurvSeg 在四个基准数据集上进行了系统验证，涵盖不同规模与场景：MCFS-22（22 类）、MCFS-130（130 类）、PKU-MMD（X-sub 和 X-view 两个划分）以及 LARa。主要对比基线包括 **DeST** 和 **LaSA** 等近年强方法，以及 MS-TCN++、ASRF、MS-GCN 等经典解耦架构。

在 MCFS-22 和 MCFS-130 上，CurvSeg 在所有指标上均取得最优（Table 2）。MCFS-22 上 Acc 达到 81.2，F1@50 为 76.7，分别超出 LaSA 0.4 个百分点；MCFS-130 上 Acc 为 73.1，F1@50 为 66.7，提升幅度相近。值得注意的是，MCFS-130 类别数远多于 MCFS-22，但 CurvSeg 的边界 F1 优势依然保持，说明曲率引导的协同机制对类别数量具有一定鲁棒性。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/004_Table_2.jpg]]
*Table 2: Comparison of methods on MCFS-22 and MCFS-130 datasets*

在 PKU-MMD 和 LARa 上，将 CurvSeg 的核心模块（EDD + CGS）附加到 DeST 和 LaSA 基线上，均带来一致且显著的提升（Table 1）。以 PKU-MMD X-sub 为例，DeST + Ours 的 Acc 从原始 DeST 的 67.8 提升至 70.3，F1@50 从 55.1 提升至 58.7；LaSA + Ours 的 Acc 从 73.5 提升至 74.3，F1@50 从 63.6 提升至 65.5。LARa 上趋势一致，LaSA + Ours 达到 Acc 76.6、F1@50 59.0。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/003_Table_1.jpg]]
*Table 1: Comparison of methods on PKU-MMD and LARa datasets*

这些结果表明，CurvSeg 的增益并非依赖特定基线，而是通过曲率引导的任务协同机制，在分类和边界定位两个子任务之间建立了互补增强的正向循环。F1@50 的提升幅度通常大于 Acc，说明边界精度的改善是整体性能提升的关键驱动力。

### 消融实验：模块贡献与协同效应

Table 3 的消融实验揭示了各模块的独立贡献及协同效果。以 PKU-MMD X-sub 为例：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/005_Table_3.jpg]]
*Table 3: Ablation Study Results on PKU and LARa dataset*

- **Base 模型**（仅含分类和边界两个独立解码头）：Acc 72.8，F1@50 63.6。
- **Base + CGS**：F1@50 从 63.6 提升至 64.7（+1.1），Edit 从 72.9 提升至 73.6，边界指标的提升最为突出，验证了曲率引导机制对边界精度的直接增强作用。
- **Base + EDD**：Acc 从 72.8 提升至 73.8（+1.0），F1@50 提升至 64.8（+1.2），说明任务特定特征解耦对分类和定位均有裨益。
- **完整模型（Ours = Base + CGS + EDD）**：Acc 达到 74.3，F1@50 达到 65.5。完整模型的增益（Acc +1.5，F1@50 +1.9）明显超过 CGS 和 EDD 独立增益之和，展现了真正的协同效应——EDD 提供的任务特定特征使 CGS 的曲率计算更加可靠，而 CGS 的双向约束又反过来优化了 EDD 的特征空间结构。

LARa 数据集上的消融趋势完全一致，完整模型的 F1@50 达到 59.0，超出 Base 模型 1.8 个百分点。

### CGS 模块深度分析

**曲率作为边界代理的有效性**（Table 4）：将 CGS 中的曲率度量替换为欧氏距离、余弦相似度和梯度显著图，在 LARa 上进行比较。曲率在所有指标上均最优（Acc 76.2，F1@50 58.7），欧氏距离次之（Acc 76.0，F1@50 57.8），梯度显著图最差。这验证了核心洞察：曲率显式捕获了特征流形的方向演化，而不仅仅是幅度或相似度的变化，因此能更精确地反映动作段内的高弯曲轨迹和过渡段的平直轨迹。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/010_Table_4.jpg]]
*Table 4: CGS ablation studies on LARa dataset*

**双向一致性的必要性**（Table 6）：仅使用分类到边界的单向约束（C→L）或边界到分类的单向约束（L→C），F1@10 分别为 71.7 和 71.6；完整的双向 CGS 达到 72.5。双向约束使分类特征空间和边界预测形成相互强化的闭环，而非单向的信息灌输。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/012_Table_6.jpg]]
*Table 6: Task synergy ablation study on LARa*

**曲率预测边界 vs. 学习边界**（Table 5）：直接用曲率信号作为边界预测（Curv）与可学习的边界预测头（Pred）性能高度接近（F1@10 分别为 72.3 和 72.5），说明曲率本身已具备作为高质量边界代理的能力，无需额外参数即可提供有效的定位信号。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/011_Table_5.jpg]]
*Table 5: Refine with different boundary prediction*

### EDD 模块深度分析

**专家路由机制的有效性**（Table 7）：将 EDD 的动态高斯混合专家路由替换为独立编码器（Indep. Enc.）和金字塔解耦（Pyr. Decoupling），在 LARa 上进行比较。EDD 的 F1@10 为 72.0，优于独立编码器的 71.6 和金字塔解耦的 71.2。动态路由的关键优势在于：它根据视频段的时序位置和内容，软性地为分类专家和定位专家分配不同的时间注意力权重，而非简单地将特征一分为二。分类专家聚焦于语义稳定的段内区域，定位专家关注过渡段附近的细粒度变化，这种互补性使得特征解耦更加高效。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/013_Table_7.jpg]]
*Table 7: EDD ablation study on LARa dataset*

### 超参数敏感性

Figure 3 和 Tables 9-12 展示了四个关键超参数的影响：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/019_Table_9.jpg]]
*Table 9: Effect of hyperparameter λ on model performance Table 10: Effect of segment count M on model performance*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/020_Table_10.jpg]]

- **曲率窗口大小 w**：w=10 时性能最优。过小的窗口对噪声敏感，产生虚假曲率峰；过大的窗口会平滑掉真实的边界信号。
- **CGS 损失权重 λ**：PKU-MMD 上 λ=4、LARa 上 λ=2.5、MCFS 上 λ=2 时最优。λ 过大会使曲率约束主导训练，干扰分类和边界的基础损失。
- **EDD 分段数 M**：M=64 时性能最优。分段过粗则时间专家粒度不足，过细则每个分段内的特征统计不稳定。
- **高斯专家数量 G**：G=2 时最优。更多专家（G≥3）带来冗余，且路由权重趋于均匀化，丧失了任务特化能力。

### 失败模式与局限性

Figure 4 可视化了两种典型的失败场景：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_Vgh30npuN3/figures/015_Figure_4.jpg]]
*Figure 4: Visualization of Limitation Cases. (a) Internal spin variations cause noise. (b) Gradual step transitions lack deep curvature valleys. Table 8: Performance on High vs. Low Dynamic Actions. Low-dynamic actions show lower absolute scores but higher relative gains from our method*

1. **内部旋转变化噪声**（Figure 4a）：当动作段内存在大幅度的身体旋转或关节抖动时，分类特征轨迹会产生虚假的高曲率峰，被误判为动作边界。这是曲率作为几何代理的固有脆弱性——它对特征空间中的所有方向突变都敏感，无法区分语义边界和噪声扰动。

2. **渐变过渡动作**（Figure 4b）：对于缓慢、连续变化的动作过渡（如从"站立"逐渐转为"行走"），特征轨迹缺乏明显的曲率谷底，边界定位模糊。这是因为曲率依赖于特征方向的突变，而渐变过渡的方向变化是平滑的。

Table 8 进一步量化了动作动态性对性能的影响。低动态动作（如"阅读""使用手机"）的绝对 F1@10 和 Edit 分数显著低于高动态动作（如"挥手""跳跃"），但 CurvSeg 在低动态动作上的相对提升更大（F1@10 提升 +3.24 vs. 高动态的 +1.68）。这说明曲率引导机制对边界模糊的困难场景具有更强的补偿能力，但绝对性能仍有较大提升空间。

### 训练过程中的曲率演化

Figure 6 展示了训练过程中曲率信号的变化，为几何假设提供了实证支撑。在早期训练阶段（Epoch 2, 8），曲率信号呈现噪声状或无规律的平坦分布，此时分类特征空间尚未形成良好的聚类结构。随着训练收敛（Epoch 64, 128），曲率信号呈现出清晰的模式：动作边界处出现明显的低曲率谷底，动作段内则呈现高曲率波动。这一演化过程验证了论文的核心理论——随着分类损失的优化，特征空间中的类簇越来越紧凑，迫使段内轨迹弯曲度增大，而段间过渡轨迹保持平直，曲率自然成为可靠的边界指示器。

## 方法谱系与知识库定位

### 1. 问题定位：解耦架构中的信息孤岛

骨架时序动作分割（STAS）的现有方法普遍采用解耦架构：共享编码器提取特征后，分别送入分类头和边界定位头独立优化。**MS-TCN++**、**ASRF**、**DeST-TCN** 等代表性工作均遵循这一范式，分类任务追求类内特征的紧凑不变性，而边界定位任务则要求对帧间差异高度敏感。这两种相互冲突的特征需求形成了信息孤岛——分类特征无法为边界检测提供有效先验，边界预测也无法反过来优化分类特征空间。**DeST** 和 **LaSA** 作为当前最强基线，虽然通过改进时间建模或注意力机制提升了各自任务的性能，但本质上仍未打破这一解耦瓶颈。

### 2. 核心突破：曲率引导的双向协同

CurvSeg 的核心创新在于将几何曲率引入跨任务协同。其关键洞察是：在良好学习的分类特征空间中，同一动作段内的特征轨迹因类簇约束而呈现高曲率（频繁转向以维持在紧凑超球内），而过渡段轨迹则相对平直、曲率低。这一几何特性被形式化为理论保证——随机游走的平均曲率与包含超球半径成反比，即 $\kappa_{F_T}(R_{intra}) > \kappa_{F_T}(R_{inter})$。

基于此，CurvSeg 构建了曲率引导协同模块（CGS），包含两个关键机制：
- **曲率作为边界代理**：利用分类特征轨迹的瞬时曲率 $\kappa_t$（由转角 $\theta_t$ 归一化得到）直接生成边界信号，无需额外学习参数。
- **双向一致性损失**：$\mathcal{L}_{curv} = -\frac{1}{T}\sum_{t=1}^{T} MSE(\hat{y}_{t}^{b}, \varphi(\mathcal{C}_{t})) + MSE(\mathcal{C}_{t}, \varphi(\hat{y}_{t}^{b}))$，强制边界预测与曲率度量相互逼近，形成正向循环——分类特征为边界提供几何先验，边界预测反过来优化分类特征空间的几何结构。

### 3. 与现有方法的差异化对比

| 维度 | 现有方法 | CurvSeg |
|------|----------|---------|
| 特征解耦 | 共享编码器直接分叉 | 专家驱动解耦（EDD），通过空间重校准和高斯混合时间专家生成任务特定特征 |
| 跨任务协同 | 无显式协同机制 | 曲率引导的双向一致性损失，建立分类与定位的正向循环 |
| 边界检测 | 纯学习式边界预测 | 曲率作为参数无关的几何代理，与学习式预测互补 |
| 时间建模 | 固定感受野的时间卷积或全局Transformer | 基于高斯混合专家的软性时间掩码分配，自适应加权不同时间尺度 |

消融实验（Table 3）验证了这一协同设计的有效性：EDD 模块单独使用可一致提升所有指标，CGS 模块单独使用带来最大的段 F1 提升，而完整模型（EDD+CGS）的增益超过各模块独立贡献之和，展现了真正的协同效应。具体而言，在 PKU-MMD (X-sub) 上，完整模型达到 74.3 Acc 和 65.5 F1@50，相比 LaSA 基线分别提升 +0.8 和 +1.9。

### 4. 适用边界与局限性

**适用场景**：
- 基于骨架数据的时序动作分割，要求骨架估计质量较高。
- 动作类别具有明确边界且动作段内运动模式相对稳定的场景。
- 需要同时优化分类精度和边界定位精度的任务。

**已知局限**（Figure 4 和 Table 8 揭示）：
1. **内部旋转噪声**：动作段内的自旋变化会产生虚假曲率峰，干扰边界检测。
2. **渐变过渡**：步态序列等缓慢过渡动作缺乏明显的曲率谷底，难以准确定位边界。
3. **低动态动作**：虽然 CurvSeg 对低动态动作的相对提升更显著（F1@10: +3.24 vs 高动态 +1.68），但其绝对分割性能仍然较低，泛化能力有限。
4. **数据质量依赖**：方法依赖骨架数据的质量和估计精度，在极度嘈杂或多人场景下可靠性下降。
5. **时间窗口约束**：曲率计算需要一定窗口大小（$w=10$），对极短动作段的响应可能不够迅速。

### 5. 开放问题

1. **在线/实时扩展**：当前方法依赖全局时间上下文，如何将其扩展至在线或实时动作分割场景？
2. **多模态融合**：能否融合 RGB 或光流等多模态信息，进一步增强特征质量与鲁棒性，尤其是在骨架数据缺失或噪声强烈的情况下？
3. **几何协同的泛化**：曲率引导的双向协同思想能否推广到更一般的视频理解任务，如时序动作检测或动作预测？
4. **自适应超参数**：窗口尺寸 $w$、分段数 $M$、损失权重 $\lambda$ 等超参数目前需按数据集手动调整，是否可通过元学习或自适应机制减少人工调参依赖？
5. **极端噪声下的可靠性**：在骨架数据极度缺失或多人交互导致关节点混淆的场景下，如何保证曲率计算的可靠性？

## 原文 PDF

![[paperPDFs/ICLR_2026/Curvature_Guided_Task_Synergy_for_Skeleton_based_Temporal_Action_Segmentation.pdf]]
