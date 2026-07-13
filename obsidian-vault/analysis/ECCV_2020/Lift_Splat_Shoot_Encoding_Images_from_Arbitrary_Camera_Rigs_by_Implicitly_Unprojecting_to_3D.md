---
title: "Lift, Splat, Shoot: Encoding Images from Arbitrary Camera Rigs by Implicitly Unprojecting to 3D"
type: paper
paper_level: A
venue: ECCV
year: 2020
pdf_ref: paperPDFs/ECCV_2020/Lift_Splat_Shoot_Encoding_Images_from_Arbitrary_Camera_Rigs_by_Implicitly_Unprojecting_to_3D.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/lift-splat-shoot/
aliases:
- LSS
tags:
- ECCV_2020
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "让每个像素预测一个离散深度上的分类分布（深度注意力），并以此软加权生成视锥特征点云，再由可学习的 BEV CNN 在柱状池化后融合多视角信息。"
primary_logic: "通过将图像隐式“提升”为相机视锥中的三维特征点云，再“投射”到地面平面进行端到端的融合，网络可以在没有深度真值的情况下直接学习如何从任意相机配置中构建连贯的鸟瞰图语义表示，并自然保持平移等变性、置换不变性和自车等距等变性。"
claims:
- "在 nuScenes 车辆 BEV 分割任务上，Lift-Splat 的 IOU 达到 32.06，大幅优于无 3D 归纳偏置的 CNN 基线（IOU 22.78），证明了隐式三维提升对于融合的关键作用。"
- "在训练时随机遗漏相机或加入外参噪声，可以显著提升测试时对相机失效与标定误差的鲁棒性，表明模型学会了数据驱动的跨相机融合。"
- "模型具备跨相机配置的泛化能力：仅在 nuScenes 训练后可直接在 Lyft 数据集上获得远优于基线的 BEV 分割结果（Lyft Car IOU 21.35，Lyft Vehicle IOU 22.59）。"
- "nuScenes BEV 车辆分割 (Car IOU) 上 IOU = 32.06"
---

# Lift, Splat, Shoot: Encoding Images from Arbitrary Camera Rigs by Implicitly Unprojecting to 3D

> [!tip] 核心洞察
> 通过将图像隐式“提升”为相机视锥中的三维特征点云，再“投射”到地面平面进行端到端的融合，网络可以在没有深度真值的情况下直接学习如何从任意相机配置中构建连贯的鸟瞰图语义表示，并自然保持平移等变性、置换不变性和自车等距等变性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 提升、投射、发射：通过隐式反投影到三维空间对任意相机配置进行图像编码 |
| 英文题名 | Lift, Splat, Shoot: Encoding Images from Arbitrary Camera Rigs by Implicitly Unprojecting to 3D |
| 会议/期刊 | ECCV 2020 |
| Links | [paper](https://arxiv.org/abs/2008.05711) · [Project](https://nv-tlabs.github.io/lift-splat-shoot) · [Project](https://research.nvidia.com/labs/toronto-ai/lift-splat-shoot/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Lift-Splat-Shoot |
| Dataset | nuScenes BEV 车辆分割 (Car IOU), nuScenes 端到端规划 Top5 准确率, Lyft BEV 车辆分割 (跨数据集迁移) |

> [!tip] 效果简介
> - nuScenes BEV 车辆分割 (Car IOU) 上，IOU 为 32.06，对比 22.78 (CNN 基线)，变化 +9.28。
> - nuScenes 端到端规划 Top5 准确率 上，Top5 Accuracy (%) 为 15.52，对比 19.27 (LiDAR 1 scan oracle)，变化 -3.75。
> - Lyft BEV 车辆分割 (跨数据集迁移) 上，IOU 为 21.35 (Car) / 22.59 (Vehicle)，对比 远低于 Lift-Splat（CNN 基线表现极差），变化 显著提升。

## 概要

自动驾驶系统通常依赖激光雷达（LiDAR）来构建精确的鸟瞰图（Bird’s-Eye-View, BEV）环境表示。然而，激光雷达成本高昂，且无法提供语义纹理信息。纯视觉方案面临的核心瓶颈在于：**单目深度模糊性**使得多视角图像特征无法被直接映射到统一的 BEV 网格。先前的方法（如 Orthographic Feature Transform, OFT）将像素特征不加区分地复制到所有深度位置，或仅在二维图像空间进行检测后再做后融合，这严重丢失了空间结构与跨视角互补信息。

针对上述问题，本文提出 **Lift-Splat-Shoot** 架构，其核心洞见在于：让每个像素预测一个离散深度上的分类分布（深度注意力），并以此软加权生成视锥特征点云，再由可学习的 BEV CNN 在柱状池化后融合多视角信息。通过将图像隐式“提升”（Lift）为相机视锥中的三维特征点云，再“投射”（Splat）到地面平面进行端到端融合，网络可以在没有深度真值的情况下，直接从任意相机配置中学习构建连贯的 BEV 语义表示，并自然保持平移等变性、置换不变性和自车等距等变性。

在 nuScenes 数据集上，Lift-Splat 在 BEV 车辆分割任务上取得了 **32.06 IOU**，大幅优于无 3D 归纳偏置的 CNN 基线（22.78 IOU），验证了隐式三维提升对多视角融合的关键作用。模型还展现出对相机失效与标定误差的强鲁棒性：训练时随机丢弃相机或向外参添加噪声，可显著提升测试时的容错能力。此外，仅在 nuScenes 上训练后，模型可直接泛化至 Lyft 数据集，获得 **21.35（Car） / 22.59（Vehicle）IOU**，远优于基线方法，证明其具备跨相机配置的迁移能力。在端到端规划任务上，模型通过将规划建模为 K 条模板轨迹上的分类问题，实现了可解释的运动规划，但其泛化性能仍落后于基于激光雷达的方案。

自动驾驶系统需要从多视角相机图像中理解自车周围的三维场景结构，以支持下游的决策与规划。传统计算机视觉任务（如语义分割）通常在输入图像坐标系中进行预测，但规划任务天然要求在鸟瞰图（Bird’s-Eye-View, BEV）坐标系下进行推理（Fig. 2）。这一坐标系鸿沟构成了多视角视觉感知的核心挑战：如何将分布在不同视角、不同相机参数下的二维图像特征，融合为统一的 BEV 空间表示。

### 现有方法的瓶颈

早期方法试图通过后处理组合单图像检测结果，将二维检测框通过刚性变换投影到自车坐标系。然而，这种管线不可端到端学习，且丢失了跨视角的空间结构信息。另一类方法，如**正交特征变换（OFT）**（Roddick et al., CoRR 2018），通过将预定义的三维体素投影回图像平面来收集特征，但存在一个根本性缺陷：**每个像素的特征被不加区分地复制到其视线上的所有深度位置**。这意味着网络无法区分“近处的小物体”与“远处的大物体”，深度模糊性被完全忽略。

纯 CNN 基线方法（如 MonoLayout 风格模型，Mani et al., ArXiv 2020）则完全放弃三维几何先验，仅对各相机图像独立提取特征后拼接，再通过双线性上采样得到 BEV 预测。虽然结构简单，但缺乏对成像几何的显式建模，导致跨相机融合能力极弱，在 nuScenes BEV 车辆分割任务上 IOU 仅为 22.78（Table 1）。

### 核心洞察与动机

本文的核心洞察在于：**单目深度模糊性是多视角 BEV 感知的瓶颈，而非障碍**。关键在于让网络学习为每个像素预测一个在深度方向上的概率分布，以此软加权地将特征“放置”到三维空间中的正确位置。这一思路将深度估计从显式的回归/分类问题转化为可学习的注意力机制——网络根据像素的语义上下文，自行决定其特征应分布在视锥射线上的哪些深度区间。

基于此，作者提出了 **Lift-Splat-Shoot** 范式：首先将每张图像“提升”（Lift）为相机视锥中的三维特征点云，再将所有视锥“投射”（Splat）到统一的 BEV 网格，最后由 BEV CNN 学习从数据中融合多视角信息。该设计天然保持了三个关键的等变性：**平移等变性**（BEV 卷积的固有属性）、**置换等变性**（对相机顺序不敏感）和**自车等距等变性**（旋转或平移自车等同于旋转或平移 BEV 表示），使得网络无需手工设计融合规则即可从任意相机配置中学习连贯的场景表示（Section 1）。

## 核心方法与创新机理

Lift-Splat-Shoot 的核心创新在于将单目深度模糊性这一根本瓶颈转化为可学习的结构化机制，从而实现了从任意多相机图像到统一鸟瞰图（BEV）表示的端到端映射。与先前方法相比，其关键突破体现在三个紧密耦合的“changed slots”上。

### 从“均匀复制”到“可学习深度注意力”

传统方法（如 **OFT**，Roddick et al., CoRR 2018）在处理图像到 BEV 的转换时，将每个像素的特征不加区分地复制到其对应射线的所有深度体素上。这种做法隐含地假设像素特征在空间上均匀分布，完全忽略了单目深度固有的模糊性——一个像素可能对应近处的行人，也可能对应远处的车辆，但其特征贡献却完全相同。

Lift-Splat-Shoot 的 **Lift** 步骤彻底改变了这一策略。网络为每个像素显式预测一个离散深度上的分类分布 $\alpha \in \triangle^{D-1}$，同时生成一个与深度无关的上下文向量 $\mathbf{c} \in \mathbb{R}^C$。该像素在深度 $d$ 处的最终特征通过外积形式的软加权获得：

$$\mathbf{c}_d = \alpha_d \mathbf{c}$$

这一设计（见 Fig. 3, Eq. 1）的因果作用在于：网络不再被迫做出“非此即彼”的硬性深度决策，而是将深度不确定性编码为特征在视锥射线上的概率分布。上下文向量 $\mathbf{c}$ 捕获了像素的语义属性（如“这是车辆的一部分”），而深度分布 $\alpha$ 则根据单目线索（纹理梯度、遮挡关系、已知的相机高度等）来推断该属性最可能存在的空间位置。这种软分配机制使得梯度可以通过深度分布反向传播，网络能够在没有深度真值的情况下，纯粹从 BEV 层面的分割监督中学会如何进行空间推理。

### 从“后融合”到“端到端可微柱状池化”

先前基于单目 3D 检测或多视图后处理的方法，通常在 2D 图像空间独立完成感知任务后，再通过刚性变换将结果投影到自车坐标系。这种“后融合”范式切断了多相机之间的信息流动，使得跨视角的互补线索（如一个相机看到车辆的前部，另一个看到侧面）无法在特征层面协同利用。

Lift-Splat-Shoot 的 **Splat** 步骤将所有相机的视锥点云统一投影到 BEV 网格，并通过 **柱状池化**（Pillar Pooling）进行融合。具体而言，每个视锥点根据相机内外参被分配到 BEV 平面上的对应柱状单元，同一柱内的所有点特征通过求和池化聚合。作者采用了“累积和”技巧（cumsum trick）来高效实现这一操作，避免了因大量填充导致的显存膨胀。

这一设计的深层价值在于其引入了关键的几何归纳偏置：

1. **平移等变性**：BEV CNN 在池化后的 BEV 特征图上操作，卷积的平移等变性自然保证了预测结果在自车坐标系中的空间一致性。
2. **置换不变性**：求和池化对输入点的顺序不敏感，这意味着无论相机数量如何变化、相机索引如何排列，融合结果保持一致。
3. **自车等距等变性**：当自车发生旋转或平移时，只要相机的外参随之更新，投影到 BEV 的特征就会相应变换，使得网络输出能够保持几何一致性。

### 从“预定义映射”到“数据驱动的 BEV 学习”

与依赖启发式规则或固定上采样的基线（如 **CNN 基线**，Mani et al., ArXiv 2020）不同，Lift-Splat-Shoot 的整个流程——从深度分布预测到多相机投影再到 BEV CNN——完全是可微的。这意味着 BEV CNN 不仅学习如何从融合后的 BEV 特征中提取语义，还通过反向传播间接“教导”Lift 步骤如何生成更有利于最终任务的深度分布。

这种端到端可学习性直接催生了模型在鲁棒性方面的涌现行为。实验表明（Fig. 6），当训练时随机丢弃一个相机（camera dropout）或向外参添加高斯噪声，模型在测试时对相机失效和标定误差的容忍度显著提升。作者将此归因于 BEV CNN 被迫学习不同相机图像之间的相关性，类似于 dropout 的正则化效应。这种鲁棒性并非通过手工设计的故障模式注入，而是从数据中自动习得的跨相机融合策略的自然结果。

综上所述，Lift-Splat-Shoot 的创新本质在于：通过将深度模糊性建模为可学习的概率分布，并将多相机几何投影嵌入到端到端的可微流水线中，网络得以在没有显式深度监督的情况下，从 BEV 层面的任务目标出发，自主发现如何将二维图像证据“提升”到三维空间并进行跨视角融合。这一范式为后续的 BEV 感知工作奠定了核心方法论基础。

Lift-Splat-Shoot 的整体 pipeline 由三条对称性驱动的设计原则贯穿始终：**平移等变性**（BEV 网格上的 CNN 天然保持）、**置换不变性**（对任意顺序的相机输入，柱状池化后的 BEV 表示保持一致）以及**自车等距等变性**（仅依赖相机外参的旋转与平移，不额外依赖自车坐标系原点选择）。在这三条原则的约束下，模型将多视角图像到 BEV 语义/规划的映射分解为四个核心模块，形成端到端可微的计算图。

### 输入输出规范

模型的输入为来自 `n` 个任意配置相机的图像集合 $\{\mathbf{X}_k \in \mathbb{R}^{3 \times H \times W}\}_n$，以及每个相机对应的外参矩阵 $\mathbf{E}_k \in \mathbb{R}^{3 \times 4}$ 和内参矩阵。输出根据任务分为两类：
- **BEV 语义分割**：在自车坐标系下，以 $200 \times 200$ 的栅格（覆盖 $x, y \in [-50\text{m}, 50\text{m}]$，分辨率 $0.5\text{m}$/cell）输出车辆、可行驶区域、车道等语义类别的分割图。
- **端到端运动规划**：在预测的 BEV 代价图上，从 1000 条模板轨迹中选择最优轨迹，输出自车的未来行驶路径。

### 模块分解与数据流

Fig. 4 给出了完整的架构概览，数据流依次经过以下模块：

1. **Image Encoder（图像编码器）**  
   基于 EfficientNet-B0 骨干网络，对每张输入图像独立提取高级特征。输入图像首先被缩放并裁剪至 $128 \times 352$ 分辨率，经骨干网络后输出特征图，作为后续 Lift 步骤的上下文表示。

2. **Lift: Latent Depth Distribution（隐式深度分布提升）**  
   这是整个 pipeline 的核心创新点。对于图像特征图上的每个像素，网络同时预测两个量：
   - 一个在 $D$ 个离散深度值上的分类分布 $\alpha \in \triangle^{D-1}$（深度注意力）；
   - 一个上下文向量 $\mathbf{c} \in \mathbb{R}^C$。
   
   通过外积操作 $\mathbf{c}_d = \alpha_d \mathbf{c}$，每个像素被“提升”为其对应视锥射线上 $D$ 个点的特征点云。这一软赋值机制使得网络能够根据图像上下文动态决定特征应放置在三维空间中的哪个深度位置，从根本上解决了单目深度模糊性问题（Fig. 3 可视化了这一过程）。

3. **Splat: Pillar Pooling（柱状投影池化）**  
   利用各相机的外参与内参，将所有视锥点云投影到统一的 BEV 柱状网格中。对落入同一柱状单元的所有点，执行求和池化（sum pooling）以聚合多视角特征。为了规避大量填充带来的显存开销，作者采用“累加和技巧”（cumsum trick）高效实现该池化操作。最终生成一个 $C \times H \times W$ 的 BEV 特征张量，该张量对相机顺序具有置换不变性。

4. **BEV CNN（鸟瞰图卷积网络）**  
   采用类 ResNet-18 的多尺度处理块对 BEV 表示进行进一步编码与上采样。该网络完全在 BEV 栅格上操作，从数据中学习如何融合来自不同相机的信息，输出最终的分割图或规划所需的代价图。

5. **Shoot: Motion Planning（轨迹发射与规划）**  
   在规划任务中，BEV CNN 输出一张代价图 $\mathbf{c}_o$。将 1000 条由 K-Means 从 nuScenes 训练集专家轨迹中聚类得到的模板轨迹“发射”到代价图上，计算每条轨迹 $\tau_i$ 的负代价和，并通过 softmax 得到轨迹的后验分布：
   $$p(\tau_i|o) = \frac{\exp\left(-\sum_{x_i,y_i\in\tau_i} c_o(x_i,y_i)\right)}{\sum_{\tau\in\mathcal{T}}\exp\left(-\sum_{x_i,y_i\in\tau} c_o(x_i,y_i)\right)}$$
   训练时最小化与专家轨迹的交叉熵损失，测试时选择 argmax 轨迹执行。Fig. 5 展示了这 1000 条模板轨迹的空间分布。

### 与基线方法的关键差异

| 设计维度 | **OFT** (Roddick et al., CoRR 2018) | **CNN 基线** (Mani et al., ArXiv 2020) | **Lift-Splat-Shoot** |
|---------|--------------------------------------|----------------------------------------|---------------------|
| 深度赋值 | 固定复制：同一像素特征无差别复制到所有深度体素 | 无深度推理，仅通过上采样将 2D 特征映射到 BEV | 可学习离散深度分布，软加权生成视锥特征点云 |
| 多相机融合 | 预定义体素投影后收集特征 | 独立提取各相机特征后拼接 | 所有视锥点云统一投影到 BEV 网格，由 CNN 端到端学习融合 |
| 几何归纳偏置 | 使用内外参进行投影，但缺乏深度不确定性建模 | 无任何 3D 几何先验 | 显式建模成像几何，保持平移等变性、置换不变性 |

**PointPillars** (Lang et al., CoRR 2018) 作为使用激光雷达点云的 oracle 基线，用于衡量纯视觉方案与激光雷达方案之间的性能差距，但其输入条件与 Lift-Splat-Shoot 不对等。

### 训练中的鲁棒性增强

pipeline 本身支持两种训练时的数据增强策略，以提升测试时的鲁棒性：
- **外参噪声注入**：训练时向外参添加高斯噪声，使模型在测试时能够容忍更大的标定误差（Fig. 6a）。
- **相机随机丢弃**：训练时随机丢弃一个相机，迫使 BEV CNN 学习跨相机图像的相关性，使模型在测试时面对相机完全失效仍能保持合理预测（Fig. 6b）。

Lift-Splat-Shoot 的核心架构由三个可微模块串联构成，分别对应“提升—投射—发射”的语义流程。以下逐一解析各模块的设计逻辑与关键公式。

### 1. Lift：隐式深度分布与视锥特征生成

该模块解决的核心瓶颈是：单张图像缺乏显式深度信息，无法直接将像素特征映射到三维空间。传统方法（如 **OFT**，Roddick et al., CoRR 2018）将同一像素特征不加区分地复制到所有深度体素，导致空间混淆。Lift-Splat-Shoot 的创新在于让网络**自行预测每个像素的深度不确定性**，并据此对特征进行软分配。

具体而言，对于每张输入图像 $\mathbf{X}_k \in \mathbb{R}^{3 \times H \times W}$，图像编码器（基于 EfficientNet-B0）为每个像素 $p$ 输出两个量：

- **上下文向量** $\mathbf{c} \in \mathbb{R}^C$：编码该像素的语义特征。
- **深度分布** $\boldsymbol{\alpha} \in \triangle^{D-1}$：在预定义的 $D$ 个离散深度值上的分类概率分布。

对于像素 $p$ 在深度 $d$ 处的三维点，其特征 $\mathbf{c}_d$ 由上下文向量与深度概率的外积决定：

$$\mathbf{c}_d = \alpha_d \mathbf{c} \quad (1)$$

**变量含义**：
- $\alpha_d$：像素 $p$ 在深度 $d$ 处的预测概率（标量）。
- $\mathbf{c}$：像素 $p$ 的上下文特征向量（维度 $C$）。
- $\mathbf{c}_d$：该像素在深度 $d$ 处生成的点特征（维度 $C$）。

这一设计的因果杠杆在于：网络必须通过端到端训练学会为每个像素分配合适的深度概率，使得后续 BEV 融合能产生正确的语义预测。如果深度分配错误，特征会被“投射”到错误的空间位置，导致 BEV CNN 收到噪声信号，从而驱动梯度反向传播修正深度分布预测。整个过程无需深度真值监督。

### 2. Splat：柱状池化与 BEV 栅格化

Lift 步骤为每张图像生成了一个相机视锥形状的特征点云。Splat 模块利用相机外参矩阵 $\mathbf{E}_k \in \mathbb{R}^{3 \times 4}$ 和内参矩阵 $\mathbf{I}_k \in \mathbb{R}^{3 \times 3}$，将所有相机的视锥点云投影到统一的鸟瞰图（BEV）平面。

投影后的点被分配到 BEV 网格的柱状单元（pillar）中。为聚合多视角信息，模块对每个柱内的所有点执行**求和池化**（sum pooling），生成一个 $C \times H \times W$ 的 BEV 特征张量。作者特别采用了“累积和”（cumsum）技巧来避免大量零填充带来的内存开销，使求和池化在计算上高效可行。

这一设计保证了两个关键的对称性：
- **置换等变性**：无论输入图像的顺序如何排列，Splat 后的 BEV 特征不变（因为求和池化对顺序不敏感）。
- **平移等变性**：BEV 网格上的平移操作等价于对输入点云的对应平移，CNN 可以自然地利用这一归纳偏置。

### 3. Shoot：基于代价图的轨迹分类

规划模块将运动规划形式化为 $K$ 条模板轨迹的分类问题。模板轨迹通过 K-Means 从 nuScenes 训练集的专家轨迹中聚类得到（$K=1000$），覆盖了常见驾驶行为。

BEV CNN 输出一个单通道的**代价图** $c_o(x, y)$，表示自车占据位置 $(x, y)$ 的代价。对于每条模板轨迹 $\tau_i$，其总代价为该轨迹所经过的所有 BEV 网格单元的代价之和。轨迹的后验分布由 softmax 给出：

$$p(\tau_i|o) = \frac{\exp\left(-\sum_{x_i,y_i\in\tau_i} c_o(x_i,y_i)\right)}{\sum_{\tau\in\mathcal{T}}\exp\left(-\sum_{x_i,y_i\in\tau} c_o(x_i,y_i)\right)} \quad (2)$$

**变量含义**：
- $c_o(x_i, y_i)$：BEV 代价图在位置 $(x_i, y_i)$ 处的值。
- $\tau_i$：第 $i$ 条模板轨迹，由一系列 BEV 坐标点组成。
- $\mathcal{T}$：全部 $K$ 条模板轨迹的集合。
- $p(\tau_i|o)$：给定观测 $o$ 下选择轨迹 $\tau_i$ 的概率。

训练时，网络通过最小化负对数似然来学习代价图，使专家轨迹获得低代价（高概率）。测试时直接选取 argmax 轨迹执行。该公式使整个规划过程完全可微，梯度可以从轨迹选择回传至 BEV CNN 乃至图像编码器，实现端到端学习。

### 模块间的因果链路

Lift 的深度分布学习为 Splat 提供了空间上有意义的特征点云；Splat 的柱状池化将多视角信息压缩为统一的 BEV 表示；BEV CNN 在此基础上提取任务相关特征，输出分割图或代价图；Shoot 则将代价图转化为可执行的轨迹决策。整个管线中，**深度分布是唯一的信息瓶颈**——如果 Lift 无法正确推断深度，后续所有模块的性能都将受到根本性制约。这也解释了为何在夜间等低光照条件下，模型性能会显著下降（见 Fig. 10），因为图像质量退化直接冲击了深度分布预测的可靠性。

## 实验与关键发现

### 核心性能验证：BEV 语义分割

Lift-Splat-Shoot 在 nuScenes 数据集上进行了全面的 BEV 语义分割评估。**Table 1** 展示了目标分割的核心结果：在车辆（Car）类别上，Lift-Splat 的 IOU 达到 **32.06**，相较于无 3D 归纳偏置的 CNN 基线（IOU 22.78）提升了 **+9.28** 个点，证明了隐式三维提升对于多视角融合的关键作用。在车辆元类（Vehicles）上同样取得 32.07 的 IOU，显著优于基线。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2008_05711/figures/006_Table_1.jpg]]
*Table 1: Segment. IOU in BEV frame Table 2: Map IOU in BEV frame*

**Table 2** 展示了地图分割结果：可行驶区域（Drivable Area）IOU 达到 72.94，车道边界（Lane Boundary）IOU 为 19.96。车道边界分割的较低绝对值反映了该任务在纯视觉 BEV 框架下的固有难度，但 Lift-Splat 仍大幅超越了 CNN 基线。

### 多相机融合与视角冗余利用

**Table 3** 的消融实验揭示了网络对冗余视角的有效利用。当相机数量从 4 个逐步增加到 5 个、6 个时，车辆 IOU 单调提升：4 相机为 26.53，增加一个前侧相机后升至 27.35，再增加一个后侧相机后达到 27.94。这一趋势表明 Lift-Splat 并非简单地对各相机预测取平均，而是通过 BEV CNN 学会了从数据中融合互补信息。

**Figure 7** 进一步分析了单个相机缺失的影响。当后向相机被移除时性能下降最大——这与 nuScenes 相机配置中后向相机拥有更宽视场角的特性一致，直观反映了该相机在构建完整 BEV 表示中的信息权重。

### 鲁棒性分析：外参噪声与相机失效

**Figure 6** 展示了两种关键鲁棒性实验的结果：

- **外参噪声鲁棒性（Figure 6a）**：训练时向外参添加高斯噪声（蓝色曲线对应大噪声训练），模型在测试时对外参标定误差的容忍度显著提升。噪声水平越大，测试时的性能衰减越平缓，证明 BEV CNN 学会了矫正不准确的投影，而非简单记忆精确的外参映射。

- **相机失效鲁棒性（Figure 6b）**：训练时随机丢弃一个相机，使得模型在测试时面对相机完全失效的情况下仍能保持较高性能。值得注意的是，**在 6 个相机全部正常工作时表现最佳的模型，恰恰是训练时随机丢弃 1 个相机的模型**——这表明相机 dropout 迫使网络学习跨相机图像之间的相关性，类似于其他 dropout 变体的正则化效应。

**Figure 8** 的定性结果展示了缺失单个相机时网络的“修补”能力：被遮挡区域预测会变得模糊，但仍保持合理的结构。当前置相机被移除时，网络能够从侧向相机中推断出前方车道和可行驶区域的延伸，甚至补全了仅在后侧相机中露出一角的车辆轮廓。

### 跨数据集泛化

**Table 4** 展示了 Lift-Splat 的跨数据集迁移能力。模型仅在 nuScenes 上训练后，直接在 Lyft 数据集上评估，获得车辆 IOU **21.35**、车辆元类 IOU **22.59** 的结果。Lyft 的相机配置与 nuScenes 完全不同，但 Lift-Splat 的泛化表现远超 CNN 基线——后者在跨数据集场景下性能极差。这验证了模型学习到的是与具体相机配置无关的空间推理能力，而非对特定视角的过拟合。

**Figure 9** 定性展示了全新相机配置下的分割结果，模型能够在未见过的相机布局下生成连贯的道路、车道和车辆语义。

### 深度与天气条件下的性能退化

**Figure 10** 对比了 Lift-Splat 与激光雷达基线 PointPillars 在不同深度和天气条件下的性能：

- **距离维度（Figure 10a）**：随着目标距离增加，Lift-Splat 的 IOU 下降速度快于 PointPillars。这是纯视觉方法的固有局限——远距离目标的像素覆盖稀疏，深度估计的不确定性急剧增大。

- **天气维度（Figure 10b）**：在夜间场景下，Lift-Splat 相对于 PointPillars 的性能下降最为明显。这揭示了图像输入对光照条件的高度敏感性，模型尚未显式处理低光照鲁棒性问题。

### 与 Oracle 深度的对比

**Table 5** 将 Lift-Splat 与使用激光雷达 oracle 深度的模型进行了对比。当用激光雷达点云替换学习到的深度分布时，性能仍有提升空间，表明深度估计质量是当前纯视觉方法的瓶颈之一。但 Lift-Splat 无需任何深度真值即可逼近有深度监督方案的性能，证明了隐式深度学习机制的有效性。

### 端到端规划

**Table 6** 展示了端到端规划任务的 top‑k 准确率。Lift-Splat 的 Top‑5 准确率为 15.52，而使用单帧激光雷达的 PointPillars oracle 基线为 19.27。这一 **-3.75** 的差距反映了纯视觉规划在动态场景理解上的不足。但需要指出，这一对比并不公平——激光雷达基线使用了稠密三维点云作为输入，而 Lift-Splat 仅依赖 6 张单帧 RGB 图像，且未使用自车速度或时序信息。

**Figure 11** 的定性结果显示，尽管存在性能差距，Lift-Splat 展现了一些引人注目的规划行为：模型预测出双峰分布（如在路口对左转和右转同时赋予较高概率），并在人行横道和刹车灯附近自动预测低速轨迹——尽管模型并未显式获得自车速度输入。

### 公平性说明

在解读上述结果时需注意以下公平性问题：

1. **激光雷达基线的不对等输入**：PointPillars 使用稠密激光雷达点云，与仅依赖摄像头图像的方法处于不同输入条件，规划准确率的直接数值对比并不公平。
2. **CNN 基线缺少几何归纳偏置**：CNN 基线未使用任何相机内外参或三维几何先验，其较低性能部分源于缺少结构化归纳偏置，而非模型绝对能力的上限。
3. **Lyft 数据集的划分差异**：Lyft 数据集缺少官方训练/验证划分，作者自行分割，可能导致与其他工作在相同数据集上的结果不可直接对比。
4. **模板轨迹的分布偏差**：规划任务中使用的模板轨迹提取自 nuScenes 训练集专家轨迹，可能对 nuScenes 场景分布存在一定过拟合。

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2008_05711/figures/010_Table.jpg]]

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2008_05711/figures/012_Table_4.jpg]]
*Table 4: We train the model on nuScenes then evaluate it on Lyft. The Lyft cameras are entirely different from the nuScenes cameras but the model succeeds in generalizing far better than the baselines. Note that our model has widened the gap from the standard benchmark in Tables 1 and 2*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2008_05711/figures/014_Figure_9.jpg]]
*Figure 9: We qualitatively show how our model performs given an entirely new camera rig at test time. Road segmentation is shown in orange, lane segmentation is shown in green, and vehicle segmentation is shown in blue. Table 5: When compared to models that use oracle depth from lidar, there is still room for improvement. Video inference from camera rigs is likely necessary to acquire the depth estimates necessary to surpass lidar*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2008_05711/figures/009_Figure_7.jpg]]
*Figure 7: We measure intersection-over-union of car segmentation when each of the cameras is missing. The backwards camera on the nuScenes camera rig has a wider field of view so it is intuitive that losing this camera causes the biggest decrease in performance relative to performance given the full camera rig (labeled “full” on the right)*

![[assets/figures/papers/paper_list_l44_https_arxiv_org_abs_2008_05711/figures/017_Figure_10.jpg]]
*Figure 10: We compare how our model’s performance varies over depth and weather. As expected, our model drops in performance relative to pointpillars at nighttime*

## 定位与知识库关联

### 核心瓶颈与因果机制

Lift-Splat-Shoot 所解决的核心瓶颈在于**单目深度模糊性**与**多视角融合的结构化缺失**。在自动驾驶的多相机设定下，直接将图像特征映射到统一的鸟瞰图（BEV）网格面临根本困难：单张图像丢失了深度信息，而简单地将像素特征不加区分地复制到所有深度候选位置（如 **Orthographic Feature Transform (OFT)**，Roddick et al., CoRR 2018 的做法）会导致空间信息被严重稀释，丢失跨视角的互补结构。纯 CNN 基线方法（如 **MonoLayout** 类方法，Mani et al., ArXiv 2020）则完全放弃 3D 几何归纳偏置，仅在各相机独立提取特征后通过双线性上采样拼接到 BEV，无法有效利用多视角间的空间一致性。

该工作的因果调控旋钮是**可学习的离散深度注意力机制**：让每个像素预测一个在离散深度桶上的分类分布 $\alpha$，并与该像素的上下文特征向量 $\mathbf{c}$ 做外积，产生视锥射线上的软加权特征 $\mathbf{c}_d = \alpha_d \mathbf{c}$。这一操作将“特征应该放在空间的哪个位置”变成了一个可微的学习问题，网络可以根据上下文动态决定每个像素特征在 3D 空间中的归属，而无需深度真值监督。随后，所有相机的视锥点云通过内外参投影到 BEV 柱状网格，由 BEV CNN 端到端地学习融合策略。

### 与基线方法的关键差异

| 维度 | OFT (Roddick et al., 2018) | CNN 基线 (Mani et al., 2020) | Lift-Splat-Shoot (本方法) |
|------|---------------------------|------------------------------|---------------------------|
| **深度赋值** | 固定/均匀复制到所有体素 | 无深度推理 | 可学习的离散深度分布，软加权 |
| **融合机制** | 预定义体素投影，后融合 | 2D 特征拼接后上采样 | 视锥点云投影 + BEV CNN 端到端融合 |
| **几何归纳偏置** | 体素-像素映射（弱） | 无 3D 偏置 | 显式建模成像几何，保持平移等变性、置换等变性、自车等距等变性 |
| **可微性** | 部分可微 | 可微但无几何约束 | 完全可微，深度分布与融合联合学习 |

相较于 **PointPillars**（Lang et al., CoRR 2018）这类使用激光雷达点云作为输入的 oracle 基线，Lift-Splat-Shoot 在输入模态上有本质差距——纯视觉方案缺乏精确的深度测量。在 nuScenes 端到端规划任务上，Lift-Splat-Shoot 的 Top-5 准确率为 15.52%，而 PointPillars 达到 19.27%（Table 6），这一差距主要源于视觉深度估计在远距离和夜间场景下的退化（Fig. 10）。

### 适用边界与局限

**适用场景**：
- 多相机环视配置下的 BEV 语义分割（车辆、可行驶区域、车道线）
- 端到端运动规划（基于模板轨迹分类框架）
- 跨相机配置泛化：在 nuScenes 训练后可直接迁移至 Lyft 数据集，车辆 IOU 达 21.35（Car）/ 22.59（Vehicle），远优于基线（Table 4）

**已知局限**：

1. **时序信息缺失**：模型仅使用单帧多相机图像，缺乏时序融合能力。这导致在远距离和低光照（夜间）条件下深度估计质量不足，性能显著落后于激光雷达方案。Table 5 显示，若使用来自激光雷达的 oracle 深度替换学习到的深度分布，模型仍有明显提升空间，表明深度估计是当前瓶颈。

2. **夜间性能退化**：Fig. 10(b) 显示，在夜间天气条件下，模型相对于 PointPillars 的 IOU 下降明显，说明纯视觉方案尚未显式处理光照鲁棒性问题。

3. **规划模板的封闭性**：规划模块依赖从 nuScenes 训练集专家轨迹通过 K-Means 聚类得到的 1000 条固定模板（Section 3.3），在开放道路中可能缺乏对某些激进或复杂驾驶行为的覆盖。模板集对 nuScenes 场景分布存在一定过拟合风险。

4. **缺少车辆动力学信息**：网络未显式利用自车速度或其他车辆运动状态，尽管模型展现了一定的隐式推理能力（如在人行横道附近预测低速轨迹，Fig. 11），这可能制约规划在高度动态场景中的精度。

### 开放问题

1. **时序多帧融合**：如何高效地融合多时间步的多相机图像，以提升深度估计精度和整体性能，使其达到与激光雷达方案相当的水平？这是从“单帧感知”走向“视频感知”的关键一步。

2. **通用 3D 推理扩展**：能否将“Lift-Splat”机制从 BEV 语义分割扩展到更一般的 3D 推理任务（如 3D 目标检测、运动预测、占据栅格预测），并在计算效率上保持可行性？

3. **极端条件下的鲁棒性**：在极端天气、复杂光照以及传感器剧烈退化（如大面积遮挡、强眩光）条件下，深度分布学习是否会过拟合于训练场景的几何先验？如何确保在未见过的环境中保持泛化能力？

4. **规划框架的灵活性**：端到端规划当前被框定为模板轨迹的分类问题。能否引入更丰富的车辆动力学约束和交互建模（如对其他交通参与者的轨迹预测），使规划框架超越固定模板的局限，处理更复杂的驾驶决策？

5. **深度分布的可解释性**：学习到的深度分布是否真正对应了场景的几何结构，还是仅仅作为“特征路由”的黑箱工具？对深度分布的显式正则化或弱监督是否有助于提升跨域泛化能力？

## 原文 PDF

![[paperPDFs/ECCV_2020/Lift_Splat_Shoot_Encoding_Images_from_Arbitrary_Camera_Rigs_by_Implicitly_Unprojecting_to_3D.pdf]]
