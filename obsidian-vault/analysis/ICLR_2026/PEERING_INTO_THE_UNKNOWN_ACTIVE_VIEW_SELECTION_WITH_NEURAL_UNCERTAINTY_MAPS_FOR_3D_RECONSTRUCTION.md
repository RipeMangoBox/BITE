---
title: "PEERING INTO THE UNKNOWN: ACTIVE VIEW SELECTION WITH NEURAL UNCERTAINTY MAPS FOR 3D RECONSTRUCTION"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PEERING_INTO_THE_UNKNOWN_ACTIVE_VIEW_SELECTION_WITH_NEURAL_UNCERTAINTY_MAPS_FOR_3D_RECONSTRUCTION.pdf
project_link: null
code_link: "https://github.com/ZhangLab-DeepNeuroCogLab/PUN"
aliases:
- PPIU
- PIUAVSNUM3R
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 是否能够训练一个轻量级神经网络，直接从单视角图像预测出覆盖所有候选视角的不确定性图，从而完全避免在线训练辐射场，并将不确定性估计与视角选择解耦。
primary_logic: 利用经过大量3D对象训练得到的Vision Transformer (UPNet) 直接建立从视角外观到不确定性图的映射，该图在球面坐标上显式地可视化各候选视角的不确定性；通过插值、乘积聚合历史不确定性图并过滤冗余低不确定性视角，以连续的方式选择最具信息量的下一个视角，实现在仅使用一半视角的情况下达到与全部视角上界相当的重建精度，并将视角选择速度提升400倍以上。
claims:
- UPNet takes a single input image of a 3D object and outputs a predicted uncertainty map, representing uncertainty values across all possible candidate viewpoints.
- Our approach aggregates all previously predicted neural uncertainty maps to suppress redundant candidate viewpoints and effectively select the most informative one.
- Despite using half of the viewpoints than the upper bound, our method achieves comparable reconstruction accuracy.
- It significantly reduces computational overhead during AVS, achieving up to a 400 times speedup along with over 50% reductions in CPU, RAM, and GPU usage compared to baseline meth...
---

# PEERING INTO THE UNKNOWN: ACTIVE VIEW SELECTION WITH NEURAL UNCERTAINTY MAPS FOR 3D RECONSTRUCTION

> [!tip] 核心洞察
> 利用经过大量3D对象训练得到的Vision Transformer (UPNet) 直接建立从视角外观到不确定性图的映射，该图在球面坐标上显式地可视化各候选视角的不确定性；通过插值、乘积聚合历史不确定性图并过滤冗余低不确定性视角，以连续的方式选择最具信息量的下一个视角，实现在仅使用一半视角的情况下达到与全部视角上界相当的重建精度，并将视角选择速度提升400倍以上。

| 字段 | 内容 |
|------|------|
| 中文题名 | 窥探未知：基于神经不确定性图的主动视角选择用于3D重建 |
| 英文题名 | PEERING INTO THE UNKNOWN: ACTIVE VIEW SELECTION WITH NEURAL UNCERTAINTY MAPS FOR 3D RECONSTRUCTION |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=e7gbgdw05A) · [Code](https://github.com/ZhangLab-DeepNeuroCogLab/PUN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PUN (Peering into the Unknown) |
| Dataset | NUM-inst, NUM-cat, NUM-3DGS-recon, NUM-light |

> [!tip] 效果简介
> - NUM-inst (novel instances) 上，PSNR 33.19 vs 33.08 (NVF) (+0.11)。
> - NUM-cat (novel categories) 上，PSNR 34.74 vs 33.15 (NVF) (+1.59)。
> - NUM-3DGS-recon 上，PSNR 36.71 vs 30.67 (NVF) (+6.04)。

## 概要

3D重建的质量高度依赖于输入视角的选择。主动视角选择（Active Viewpoint Selection, AVS）旨在从大量候选视角中挑选出最具信息量的子集，以最小化重建误差。然而，现有方法面临一个根本性瓶颈：**每选择一个新视角，都需要重新训练或推断辐射场模型（如NeRF或3DGS）来估计不确定性，导致单次选择耗时数分钟，计算开销极大**。这种在线重训练的范式严重限制了AVS在实际场景中的应用。

针对这一问题，本文提出**PUN（Peering into the Unknown）**方法，其核心思路是**将不确定性估计与视角选择彻底解耦**。具体而言，PUN训练一个轻量级的前馈神经网络UPNet（Uncertainty Prediction Network），直接从单张输入图像预测一张覆盖所有候选视角的神经不确定性图（Neural Uncertainty Map），从而完全避免了测试时的在线模型重训练。在此基础上，PUN通过聚合历史不确定性图、过滤冗余低不确定性视角，以连续的方式选择最具信息量的下一个视角。

实验结果表明，PUN在仅使用一半视角的情况下，即可达到与全视角上界相当的重建精度。在计算效率方面，PUN将视角选择速度**提升高达400倍**，同时CPU、RAM和GPU使用率降低超过50%。该方法在多种数据集设置下均取得最优或次优结果，验证了其有效性和泛化能力。

三维场景的新视角合成是计算机视觉与图形学中的核心任务，其目标是从一组稀疏的输入视角重建出任意新视角下的高质量图像。以**NeRF**（Mildenhall et al., ECCV 2020）和**3D Gaussian Splatting (3DGS)**（Kerbl et al., SIGGRAPH 2023）为代表的神经渲染方法在此任务上取得了突破性进展，但它们的重建质量高度依赖于输入视角的数量与分布。在实际应用中，如机器人探索、无人机航拍和移动端扫描，采集所有可能的视角往往成本高昂甚至不可行。因此，**主动视角选择（Active Viewpoint Selection, AVS）**——即从候选视角中自适应地选择最具信息量的子集以最小化重建误差——成为了一个关键的研究方向。

### 现有方法的瓶颈

当前基于NeRF的主动视角选择方法普遍遵循一个“训练-评估-选择”的迭代范式：每选择一个新视角后，需要重新训练辐射场模型，然后在所有候选视角上计算某种启发式的不确定性度量（如射线权重分布的熵、颜色输出的方差或视野可见性），最后选择不确定性最高的视角作为下一个采集目标。这一范式存在两个根本性瓶颈：

1. **计算开销巨大**：每添加一个视角就需要完整地重新训练或微调辐射场，导致每次视角选择的耗时长达数分钟。例如，基于权重分布熵的方法**WD**（Lee et al., 2022）和基于颜色方差的方法**A-NeRF**（Pan et al., 2022）均需在每步在线评估NeRF模型；即使是最新的**NVF**（Xue et al., 2024）在不确定性估计中显式考虑了视野可见性，仍无法摆脱在线重训练的束缚。当需要选择20个视角时，NVF的累计推理时间高达175分钟（Tab. S4），严重限制了实际部署。

2. **误差累积与解耦缺失**：这些方法的不确定性估计与重建模型的当前状态深度耦合——不确定性值依赖于已训练模型的中间表示，而模型本身又受限于已选择的视角。这种循环依赖导致两个问题：其一，早期选择的视角若存在偏差，后续的不确定性估计会累积误差；其二，无法利用跨场景、跨物体的先验知识来指导不确定性预测，每次面对新物体都需要从零开始。

### 核心动机与因果机制

本文的核心动机在于回答一个根本性问题：**能否将不确定性估计与视角选择从在线重建过程中彻底解耦？** 换言之，是否可能训练一个轻量级神经网络，使其在仅看到当前视角图像的情况下，就能直接预测出覆盖所有候选视角的不确定性分布，从而完全避免在线训练辐射场？

这一动机背后的因果机制是：经过大量3D对象训练的视觉模型应当能够学习到“从外观到不确定性”的映射关系——即，给定一个视角下的物体外观，模型可以推断出哪些区域尚未被充分观测、哪些候选视角能提供最大的信息增益。这种映射一旦被预训练习得，在测试时仅需一次前向传播即可完成不确定性估计，将视角选择的速度提升数个数量级。

### 本文的贡献定位

基于上述动机，本文提出了一种全新的主动视角选择范式**PUN (Peering into the Unknown)**，其核心贡献体现在三个层面：

- **数据集贡献**：构建了大规模**神经不确定性图（Neural Uncertainty Map, NUM）数据集**，涵盖13个物体类别、每类100个实例，每个实例包含48个锚点视角及其对应的真实不确定性图，为学习从外观到不确定性的映射提供了监督信号。

- **方法贡献**：提出**UPNet（Uncertainty Prediction Network）**，一个基于Vision Transformer的轻量级前馈网络，能够从单张输入图像直接预测覆盖球面所有锚点的不确定性图；并设计了基于历史不确定性图乘积聚合与冗余过滤的连续视角选择策略。

- **效率贡献**：在仅使用一半视角的情况下达到与全视角上界相当的重建精度，同时将视角选择速度提升**400倍以上**，CPU、RAM和GPU使用率降低超过50%，使主动视角选择首次具备了实时部署的可行性。

## 核心方法与创新机理

PUN 方法的核心创新在于将主动视角选择（AVS）中“不确定性估计”与“视角选择策略”两个环节进行了根本性的重构，从而突破了传统方法“每选一个视角就需重新训练辐射场”的计算瓶颈。

### 创新一：从在线推断到前馈预测——UPNet 与神经不确定性图

传统 AVS 方法（如 **WD** (Lee et al., 2022)、**A-NeRF** (Pan et al., 2022)、**NVF** (Xue et al., 2024)）的不确定性估计范式是**在线且耦合的**：每选择一个新视角，必须先在当前已选视角上训练或推断一个神经渲染模型（NeRF 或 3DGS），然后基于该模型的内部状态计算启发式不确定性指标（如射线权重分布熵、颜色方差、可见性加权等）。这一过程每次选择耗时数分钟，且误差会随迭代累积。

PUN 将这一范式彻底解耦为**离线训练、前馈预测**的模式。其核心组件 **UPNet**（Uncertainty Prediction Network）是一个轻量级的前馈神经网络，基于在 ImageNet 上预训练的 Vision Transformer (ViT) 进行微调，并在分类 token 输出后附加一个全连接层，直接预测一个 48 维的神经不确定性图（Neural Uncertainty Map）。该图以球面坐标显式编码了以当前视角为中心的整个球面上所有锚点视角的不确定性值。

这一设计的关键因果机制在于：UPNet 学习的是从“视角外观”到“底层体积表征不确定性”的直接映射。训练时，UPNet 的监督信号来自预先生成的 ground-truth 不确定性图——这些图通过在不同锚点视角上独立训练重建模型并计算图像保真度度量（如 PSNR）得到。测试时，UPNet 仅需一次前向传播即可输出完整的不确定性图，**完全避免了在线训练任何重建网络**，从而将视角选择的时间从数分钟级压缩至约半分钟。

### 创新二：从单步贪婪到历史聚合——乘积式不确定性累积与冗余抑制

传统方法在选择下一个视角时，仅根据当前模型估计的单点不确定性值进行贪婪选择，缺乏对历史选择信息的有效利用。这容易导致重复选择信息高度重叠的视角，造成视角预算的浪费。

PUN 引入了**历史不确定性图乘积聚合**策略。在每个时间步 $t$，UPNet 预测的不确定性图 $U_t$ 被保留。对于任意候选视角 $C^i$，其不确定性值通过角度距离加权的 softmax 插值从相邻锚点获得：

$$U^{C_i} = \sum_{\tilde{P_j} \in \tilde{P}} \omega_j U^{\tilde{P_j}}, \quad \omega_j = \frac{e^{-\theta_{ij}}}{\sum_{\tilde{P_j} \in \tilde{P_i}} e^{-\theta_{ij}}}$$

随后，所有历史时间步的插值不确定性值通过乘积进行聚合，下一个最佳视角 $v_{t+1}$ 选择具有最大累积不确定性的候选视角：

$$v_{t+1} = \arg\max_{C_i} \prod_{1,2,\dots,t} U_t^{C^i}$$

此外，PUN 还引入了**冗余过滤机制**：若某候选视角在任意历史时间步的不确定性值低于阈值 0.1，则将其从候选集中剔除。这一设计的直觉是，已被充分观测的视角区域不再需要额外的视角覆盖。

乘积聚合与冗余过滤的协同作用，使得 PUN 能够在仅使用一半视角（20 个）的情况下，达到与全部视角上界（40 个）相当的重建精度，同时将计算速度提升 **400 倍**，CPU、RAM 和 GPU 资源消耗降低超过 50%。

### 创新三：NUM 数据集——为不确定性预测提供规模化监督

上述创新的实现依赖于一个关键的基础设施：**NUM（Neural Uncertainty Map）数据集**。该数据集覆盖 13 个物体类别、每类 100 个实例，为每个实例在 48 个固定锚点视角上预计算了 ground-truth 不确定性图。这一数据集的构建使得 UPNet 能够以监督学习的方式训练，从而获得跨实例和跨类别的泛化能力——实验表明，PUN 在新实例（NUM-inst）和新类别（NUM-cat）上均显著优于所有基线方法。

PUN（Peering into the Unknown）提出了一种全新的主动视角选择范式，其核心思想是将不确定性估计与视角选择完全解耦，从而避免传统方法中每选一个视角就需要重新训练辐射场的巨大计算开销。整个框架由两个紧密协作的模块构成：**神经不确定性图预测**和**下一最佳视角选择**。

### 工作流程

在每一个时间步 $t$，给定当前视角 $v_t$ 采集到的输入图像 $I_t$，PUN 执行以下流程：

1. **不确定性图预测**：将 $I_t$ 送入轻量级前馈网络 **UPNet**（Uncertainty Prediction Network），直接预测出一张覆盖所有锚点视角的神经不确定性图（Neural Uncertainty Map, UMap）$U_t$。该图在球面极坐标系中定义了48个固定锚点位置的不确定性值，无需在线训练任何重建网络。

2. **候选视角采样**：在物体周围的球面上随机采样512个候选视角 $C^i$。

3. **不确定性插值**：对于每个候选视角，利用角度距离加权的 softmax 函数，从其相邻锚点（角度距离在30°以内）的不确定性值插值得到该候选视角的不确定性 $U^{C_i}$：
   $$U^{C_i} = \sum_{\tilde{P_j} \in \tilde{P}} \omega_j U^{\tilde{P_j}}, \quad \omega_j = \frac{e^{-\theta_{ij}}}{\sum_{\tilde{P_j} \in \tilde{P_i}} e^{-\theta_{ij}}}$$

4. **历史聚合与冗余过滤**：将当前不确定性图与过去所有时间步预测的不确定性图通过乘积进行聚合；同时过滤掉在任何历史时间步中不确定性值低于阈值0.1的冗余候选视角。

5. **下一最佳视角选择**：选择累积不确定性乘积最大的候选视角作为下一最佳视角 $v_{t+1}$：
   $$v_{t+1} = \arg\max_{C_i} \prod_{1,2,\dots,t} U_t^{C^i}$$

### 关键设计理念

这一流水线的核心优势在于**计算范式的根本性转变**：UPNet 是一个预训练的轻量级 Vision Transformer，测试时仅需一次前向传播即可完成不确定性预测，完全避免了传统方法（如 **WD**（Lee et al., 2022）、**A-NeRF**（Pan et al., 2022）、**NVF**（Xue et al., 2024））中每添加一个视角就需在线训练或推断辐射场/3DGS模型、然后计算启发式不确定性度量的迭代流程。这使得视角选择速度提升约400倍，同时 CPU、RAM 和 GPU 使用量降低超过50%。

此外，通过乘积聚合所有历史不确定性图并过滤低不确定性冗余视角，PUN 能够有效抑制已充分观测的区域，引导后续视角持续探索信息量最高的未知区域，从而在仅使用一半视角（20个）的情况下达到与全部40个视角上界相当的重建精度。

![[assets/figures/papers/paper_list_l57_https_openreview_net_forum_id_e7gbgdw05A/figures/002_Figure.jpg]]
*Figure: (a) Creation of our NUM dataset (b) Overview of our PUN method*

PUN 方法由两个解耦的核心模块构成：**神经不确定性图预测** 与 **下一最佳视角选择**。前者通过预训练的轻量级网络将单视角外观直接映射为覆盖全候选空间的不确定性图，后者则通过历史不确定性聚合与冗余过滤实现连续、高效的视角规划。

### UPNet：不确定性预测网络

UPNet 是整个方法的前馈推理核心。其设计目标是学习一个从当前视角图像 $I_t$ 到神经不确定性图 $U_t$ 的直接映射，从而完全避免传统方法中每步在线训练辐射场的沉重计算负担。

**网络架构**：UPNet 采用在 ImageNet 上预训练的 Vision Transformer（ViT）作为骨干网络，在分类 token 输出后追加一个全连接层，直接预测一个 48 维向量——每个维度对应球面上一个固定锚点的不确定性值。这种设计使得网络仅需一次前向传播即可完成对所有候选视角方向的不确定性估计，推理过程与历史视角完全解耦。

**监督信号构建**：训练 UPNet 需要成对的（输入图像，真实不确定性图）数据。为此，作者构建了 NUM（Neural Uncertainty Map）数据集：对每个 3D 对象的每个锚点视角，使用单目重建主干网络（Splatting-Image）从该视角重建对象，再渲染其余 47 个锚点视角的图像，计算渲染图像与真实图像之间的保真度度量（如 PSNR）作为该锚点方向的不确定性值。这一过程将“从该视角出发，模型对对象其他部分的未知程度”量化为可学习的监督信号。

### 不确定性插值

UPNet 输出的 48 维向量仅覆盖预定义的锚点方向。为评估任意候选视角 $C^i$ 的不确定性，PUN 采用基于角度距离的加权插值机制。

首先，定义候选视角 $C^i$ 的相邻锚点集合 $\tilde{P}$ 为与 $C^i$ 的角距离在 30° 以内的所有锚点。候选视角的不确定性值由这些相邻锚点的不确定性加权求和得到：

$$U^{C_i} = \sum_{\tilde{P_j} \in \tilde{P}} \omega_j U^{\tilde{P_j}}$$

其中权重 $\omega_j$ 通过以负角距离为输入的 softmax 函数计算：

$$\omega_j = \frac{e^{-\theta_{ij}}}{\sum_{\tilde{P_j} \in \tilde{P_i}} e^{-\theta_{ij}}}$$

这里 $\theta_{ij}$ 为候选视角 $C^i$ 与锚点 $\tilde{P_j}$ 之间的球面角距离。该设计保证了距离越近的锚点对插值结果的贡献越大，同时通过 softmax 归一化确保权重和为 1，使不确定性图在球面上平滑连续。

### 下一最佳视角选择

在获得当前步的插值不确定性图后，PUN 通过历史聚合与冗余过滤两个机制确定下一最佳视角。

**历史不确定性聚合**：不同于传统方法仅依据当前模型状态选择视角，PUN 将过去所有时间步预测的不确定性图通过乘积方式进行累积。对于任意候选视角 $C^i$，其累积不确定性为：

$$v_{t+1} = \arg\max_{C_i} \prod_{1,2,\dots,t} U_t^{C^i}$$

乘积聚合的直觉在于：若某候选视角在任一历史步中表现出低不确定性（即该方向的信息已被充分获取），其累积值将被显著压制，从而避免重复选择已充分观测的区域。

**冗余视角过滤**：在乘积聚合之前，PUN 引入一个硬阈值过滤机制——若某候选视角在任一历史时间步的插值不确定性值低于 0.1，则直接将其从候选集中排除。消融实验表明，该过滤策略（标记为“small”）与全历史聚合（标记为“all”）的组合（small+all）达到了最优性能，而仅使用最后一步的不确定性图或完全禁用冗余过滤均会导致重建质量下降。

这一选择策略的核心优势在于其**连续性**：不确定性图在球面上的平滑插值确保了相邻视角的不确定性值具有合理的相对关系，使得基于 argmax 的贪婪选择不会产生剧烈的视角跳变，有利于后续重建网络的稳定训练。

![[assets/figures/papers/paper_list_l57_https_openreview_net_forum_id_e7gbgdw05A/figures/004_Figure_3.jpg]]
*Figure 3: Visualization of ground-truth and predicted uncertainty maps by our PUN method. We present two examples from: (a) NUM-inst and (b) NUM-cat. In each case, the input view*

## 实验与关键发现

### 主要实验结果

PUN在五个不同难度的基准测试上系统性地评估了视角选择质量，所有实验均遵循严格的公平比较协议：每个主动视角选择（AVS）方法最多选择20个视角，渲染分辨率为512×512，每步随机采样512个候选视角，评估视角集统一为40个固定相机姿态，所有重建主干网络均从零开始训练相同迭代次数。

**Table 1** 汇总了各方法在不同数据集上的重建质量对比。在NUM-inst（新实例）上，PUN以PSNR 33.19的成绩超越所有基线方法，包括最强的NVF（33.08）；在更具挑战性的NUM-cat（新类别）上，PUN的PSNR达到34.74，领先NVF的33.15达+1.59 dB，展现出对未见类别的强泛化能力。当重建主干切换为3DGS时（NUM-3DGS-recon），PUN的优势进一步放大，PSNR达到36.71，远超NVF的30.67（+6.04 dB），表明不确定性图预测对不同的神经渲染主干具有鲁棒性。在变光照条件（NUM-light）下，PUN同样保持领先（32.84 vs. 31.57）。值得强调的是，尽管仅使用一半的视角（20个），PUN的重建质量已与使用全部40个视角的上界（Upper Bound）相当，验证了其视角选择策略的有效性。

在真实场景数据集NeRFAssets上（**Table 2**），PUN的PSNR为26.73，略优于NVF的26.31，证明了方法在复杂背景和遮挡条件下的实用性。

### 计算效率分析

PUN的核心优势在于将视角选择的计算开销降低了两个数量级以上。**Table S4** 显示，选择20个视角时，PUN仅需约0.5分钟，而NVF需要175分钟，加速约350倍（原文声称最高400倍加速）。同时，PUN的CPU、RAM和GPU使用量均降低超过50%。这一效率飞跃源于UPNet的轻量化前馈设计：测试时仅需一次前向传播即可获得覆盖所有候选视角的不确定性图，完全避免了传统方法中每选一个视角就需要重新训练辐射场的迭代开销。

![[assets/figures/papers/paper_list_l57_https_openreview_net_forum_id_e7gbgdw05A/figures/014_Table_S.4.jpg]]
*Table S.4: Processing Time and Resource Comparison. We report the average time, and computing resources (from left to right: CPU usage, RAM, GPU usage, and GPU memory) required to select 20 viewpoints for each AVS method during inference. Average results over 3 runs are reported, with standard deviations shown in the brackets. Best is in bold and the second best is underlined*

### 消融实验

**Table 3** 和 **Table S6** 系统性地剖析了PUN各关键组件的贡献：

- **不确定性度量**（Table 3a/Table S6a）：使用PSNR作为UPNet的监督信号生成真实不确定性图，得到的重建质量最佳，略优于SSIM和LPIPS，明显优于MSE。这表明像素级保真度度量与视角信息量之间存在更强的相关性。

- **视角选择策略**（Table 3b/Table S6b）：执行冗余过滤（阈值0.1）并结合聚合所有历史不确定性图的策略（small+all）达到了最高性能。仅使用最后一个不确定性图（last）或完全禁用冗余过滤（none）都会导致性能下降，证明历史信息累积和冗余抑制对于避免重复选择相似视角至关重要。

- **训练数据构成**（Table 3c/Table S6c）：增加训练集中每个类别的实例多样性对性能的提升，大于增加每个实例的视角密度。这意味着UPNet从多样化的物体形态中学习到了更泛化的“外观→不确定性”映射，而非简单记忆特定视角模式。

- **锚点数量**（Table S6d）：将锚点从12增加到48带来了显著的性能提升，但继续增加到108提升有限，说明48个锚点已能在球面上提供足够的分辨率来表征不确定性分布。

- **冗余过滤阈值**（Table S6e）：阈值设为0.1时取得了最佳的整体性能，平衡了视角多样性与信息量。

### 不确定性图可视化

**Figure 3** 展示了PUN预测的不确定性图与真实不确定性图的可视化对比。在NUM-inst和NUM-cat两个示例中，UPNet从单一输入图像预测出的48维不确定性图能够准确捕捉物体背面、遮挡区域等“未知”视角的高不确定性分布，与通过完整重建计算得到的真实不确定性图高度一致。这直观地验证了UPNet学习到了从单视角外观推断三维结构不确定性的能力。

### 跨主干网络泛化性

PUN在NeRF和3DGS两种截然不同的重建主干上均表现出色。在NeRF-NUM数据集（**Table S3**）上，PUN同样优于所有基线。值得注意的是，NUM数据集的真实不确定性图是基于Splatting-Image主干生成的，但PUN选择的视角在NeRF主干上重建同样有效，说明不确定性图的视角选择策略具有跨主干网络的迁移能力。

![[assets/figures/papers/paper_list_l57_https_openreview_net_forum_id_e7gbgdw05A/figures/012_Table_S.3.jpg]]
*Table S.3: Evaluation of AVS Methods on NeRF-NUM. Best is in bold and second best is underlined. MSE values are scaled by*

### 失败模式与局限性

尽管PUN在多数场景下表现优异，分析揭示了以下边界条件：

1. **球面采样假设**：当前方法假设所有候选视角位于以物体为中心的固定半径球面上（基于HEALPix采样）。在更自由的相机姿态或稀疏视角分布下，锚点定义和插值机制需要重新设计。

2. **不确定性度量的单一性**：不确定性图仅基于图像保真度度量（PSNR等）生成，未显式考虑几何完整性或视觉覆盖率。在某些场景下，可能优先选择纹理丰富但几何信息有限的视角，而忽略了对完整三维重建更关键的几何覆盖。

3. **主干网络依赖性**：虽然实验表明视角选择具有泛化能力，但不确定性图的绝对数值分布仍可能受生成NUM数据集时所使用的特定单目重建主干网络（Splatting-Image）影响，在极端不同的渲染范式下可能需要微调。

4. **真实场景的复杂性**：在NeRFAssets上的提升幅度（+0.42 dB）小于合成数据集，说明背景杂乱和复杂遮挡对不确定性预测精度提出了更高要求。

![[assets/figures/papers/paper_list_l57_https_openreview_net_forum_id_e7gbgdw05A/figures/005_Figure_4.jpg]]
*Figure 4: Visualization of the datasets used for AVS evaluation. From left to right, the object instances exhibit increasing geometric complexity, occlusion, and background clutter*

![[assets/figures/papers/paper_list_l57_https_openreview_net_forum_id_e7gbgdw05A/figures/007_Table_3.jpg]]
*Table 3: Ablation Analysis of Key Components in Our PUN Method. From left to right, we analyze: (a) different uncertainty metrics used to generate ground truth UMaps and train UPNet, (b) the effect of different next-viewpoint selection policies as illustrated in Sec. 5.3, and (c) the trade-off between instance diversity and viewpoint density in training samples. In (c), instance diversity refers to the number of object instances per category, while viewpoint density refers to the number of viewpoint–UMap pairs per instance. Best is in bold and second best is underlined. MSE values are scaled by 104. See Tab. S6 for full results in all metrics*

## 定位与知识库关联

### 1. 主动视角选择（AVS）的范式演进

PUN 的提出根植于主动视角选择领域从“在线重建-评估”范式向“预训练-预测”范式的根本性转变。理解这一转变，需要回溯 AVS 方法在处理不确定性时的三种主流路径，以及它们各自的计算瓶颈。

**基于辐射场在线训练的方法。** 这类方法的核心逻辑是：每选择一个新视角，就从头或增量训练一个神经辐射场（NeRF）或 3D 高斯泼溅（3DGS）模型，然后在该模型上计算某种启发式的不确定性度量，选择不确定性最高的候选视角。代表性工作包括：**WD**（Lee et al., 2022）通过计算射线权重分布的熵来估计体积不确定性；**A-NeRF**（Pan et al., 2022）将 NeRF 的颜色输出建模为高斯分布，基于方差估计不确定性；**NVF**（Xue et al., 2024）在不确定性估计中显式考虑视野可见性。这些方法的共同缺陷是计算开销巨大——每增加一个视角就需要重新训练整个辐射场，导致选择 20 个视角的总耗时可达数十分钟甚至数小时。PUN 论文报告 NVF 选择 20 个视角平均耗时 175 分钟，而 PUN 仅需 0.5 分钟，速度提升约 350 倍。

**基于深度图的方法。** 这类方法利用预训练的单目深度估计网络或多视图立体匹配来评估候选视角的信息量，避免了在线训练辐射场。然而，深度图的精度受限于预训练模型的泛化能力，且深度信息本身无法直接反映辐射场在新视角下的渲染不确定性，导致重建质量通常低于基于辐射场的方法。PUN 的实验表明，这类方法在 NUM-inst 上的 PSNR 通常低于 32 dB，而基于辐射场的方法（如 NVF）可达到 33 dB 以上。

**PUN 的范式突破。** PUN 的关键创新在于将不确定性估计与重建过程完全解耦：它不依赖任何在线训练的辐射场模型，而是训练一个轻量级的前馈网络 UPNet，直接从单张输入图像预测覆盖所有候选视角的不确定性图。这一设计使得 AVS 的计算复杂度从“视角数量 × 辐射场训练时间”骤降为“一次神经网络前向传播”，从根本上解决了计算瓶颈。更重要的是，UPNet 学习的是“视角外观到体积表示不确定性”的直接映射，这意味着它隐式地编码了从 2D 表观推断 3D 重建难度的能力——这是一种跨实例、跨类别可迁移的知识。

### 2. 不确定性建模的知识来源与泛化机制

PUN 的不确定性预测能力并非凭空而来，而是建立在一个精心构建的大规模数据集 NUM（Neural Uncertainty Map）之上。该数据集包含 13 个物体类别、每类 100 个实例、每个实例 48 个锚点视角的真值不确定性图。真值不确定性图的生成方式是：对每个锚点视角，在包含和不包含该视角的两种条件下训练 3D 重建模型，计算两者在新视角渲染质量上的差异（以 PSNR 等图像保真度度量衡量）。

这一数据构建策略具有双重意义。**首先**，它提供了一种可扩展的监督信号生成范式——只要有一个可微的 3D 重建主干网络（如 Splatting-Image），就可以为任意 3D 对象自动生成不确定性标签，无需人工标注。**其次**，真值不确定性图中编码的信息远不止“该视角是否被观测过”，它包含了视角间的几何关联、遮挡关系、纹理复杂度等多维信息。UPNet 通过在大规模数据上学习，将这些隐含知识压缩到网络权重中。

泛化能力的来源可以从两个层面理解。**架构层面**，UPNet 基于在 ImageNet 上预训练的 Vision Transformer（ViT），其自注意力机制天然适合捕捉图像中的长程依赖关系，这对于从单张 2D 图像推断 3D 不确定性至关重要——例如，一张图像中被遮挡的区域暗示了背面视角的高不确定性。**数据层面**，消融实验（Table 3c）揭示了一个关键发现：增加训练集中每个类别的实例多样性对性能的提升，大于增加每个实例的视角密度。这表明 UPNet 学到的是跨实例的“形状-不确定性”映射规律，而非对特定视角的过拟合记忆。这一特性解释了为什么 PUN 在 novel categories（NUM-cat）上的 PSNR 增益（+1.59 dB 相对于 NVF）远大于 novel instances（NUM-inst）上的增益（+0.11 dB）——因为类别间的形状差异更大，而 PUN 的泛化能力恰好在此时凸显。

### 3. 视角选择策略的连续性与冗余抑制

PUN 的视角选择策略区别于以往方法的另一个关键特征是**历史信息的连续聚合**。传统方法在每一步仅根据当前模型估计的不确定性值选择下一个视角，这隐含地假设了不确定性估计是马尔可夫的——但实际上，已选视角会改变剩余候选视角的信息价值。PUN 通过将所有历史不确定性图进行乘积聚合（$v_{t+1} = \arg\max_{C_i} \prod_{1,2,\dots,t} U_t^{C^i}$），显式地建模了视角选择过程中的信息累积效应。

乘积聚合的数学意义在于：如果一个候选视角在任何一个历史时间步被预测为低不确定性（接近 0），其累积不确定性将趋近于 0，从而被有效抑制。这与信息论中的“边际信息增益递减”原理一致——已被充分覆盖的区域不应被重复选择。消融实验（Table 3b）证实，仅使用最后一个不确定性图（“last” 策略）或完全禁用冗余过滤都会导致性能下降，而“small+all”策略（过滤不确定性低于 0.1 的冗余视角并聚合所有历史）达到了最优性能。

这一设计将视角选择从“贪婪的单步优化”提升为“有记忆的序列决策”，尽管它并非严格意义上的全局最优搜索（如旅行商问题式的路径规划），但在计算效率和选择质量之间取得了实用化的平衡。

### 4. 适用边界与局限

PUN 的适用边界由其核心假设和数据构建方式共同决定。

**几何假设：固定半径球面候选视角。** PUN 假设所有候选视角位于以物体为中心的固定半径球面上，锚点采用 HEALPix 采样均匀分布。这一假设在受控的 3D 物体扫描场景中合理，但在更自由的相机姿态分布（如无人机环绕飞行、手持设备随意拍摄）或稀疏视角分布下，需要重新设计锚点映射和插值机制。论文明确指出当前方法尚未处理此类场景。

**不确定性定义的维度局限。** NUM 数据集中的真值不确定性图基于图像保真度度量（如 PSNR）生成，这意味着 UPNet 学到的是“该视角对提升渲染质量的贡献”而非“该视角对完善几何重建的贡献”。在某些场景下，一个纹理丰富但几何信息有限的视角可能被赋予高不确定性，而一个能揭示关键几何结构但纹理平坦的视角可能被低估。论文将“如何融入面向几何的度量（如网格精度、视觉覆盖率）”列为开放问题。

**数据集依赖的主干网络偏差。** NUM 数据集的真值不确定性图依赖于特定的单目重建主干网络（Splatting-Image）。虽然实验表明 PUN 选择的视角在不同重建主干（如 3DGS、Binocular3DGS）上均表现良好（Table 1c, Table S2），但不确定性图的绝对数值分布仍可能受原始主干网络的影响。在极端不同的重建框架下，不确定性值的校准可能需要重新验证。

**动态场景与运动约束的缺失。** 当前 PUN 仅处理静态 3D 物体的视角选择，未考虑动态场景中运动模式对最佳视角的影响，也未考虑真实机器人交互中机械臂或无人机的运动学约束。论文将这两个方向列为开放问题。

### 5. 在知识库中的定位

PUN 在 AVS 领域的方法谱系中占据了一个独特的位置：它是**首个将不确定性估计完全从在线重建中解耦的端到端学习方法**。与基于辐射场的方法相比，它牺牲了不确定性估计与当前重建状态的精确耦合，换取了两个数量级的计算加速和跨类别泛化能力。与基于深度图的方法相比，它直接预测辐射场重建的不确定性，而非依赖深度作为代理信号，从而获得了显著更高的重建质量。

从更广的视角看，PUN 代表了一种“学习式不确定性感知”的范式，其核心思想——训练一个网络直接从观测预测信息价值——可以迁移到其他主动感知任务中，如主动 SLAM、机器人探索、计算摄影中的自动曝光与对焦等。这一范式的关键前提是存在一个可自动生成真值标签的模拟环境，而 PUN 的 NUM 数据集构建流程为此提供了可复用的模板。

## 原文 PDF

![[paperPDFs/ICLR_2026/PEERING_INTO_THE_UNKNOWN_ACTIVE_VIEW_SELECTION_WITH_NEURAL_UNCERTAINTY_MAPS_FOR_3D_RECONSTRUCTION.pdf]]
