---
title: BimArt A Unified Approach for the Synthesis of 3D Bimanual Interaction with Articulated Objects
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/BimArt_A_Unified_Approach_for_the_Synthesis_of_3D_Bimanual_Interaction_with_Articulated_Objects.pdf
aliases:
- BUAS3BIAO
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 以距离为基础的双手接触图作为中间生成先验，并结合归一化的分部点基集（BPS）特征，从而实现多样化且物理上可信的双手运动生成，无需任何参考抓握。
primary_logic: 逐帧的距离接触图编码了丰富的双手抓握与操作模式，其细粒度的空间约束能够指导扩散模型生成符合接触逻辑的运动；分部感知的归一化 BPS 确保了对大小迥异的物体部件进行等分辨率编码，这对于铰接物体的双手交互至关重要。
claims:
- 在 ARCTIC 数据集上，BimArt 在穿透（Pen 1cm 2.03%）、接触率（Con 99.63%）和关节接触率（Art 85.57%）上全面超越 CAMS-B、MDM-B 和 OMOMO-B。
- 在 HOI4D 跨类别评测中，BimArt 的接触得分（Pliers 0.966, Scissors 1.0）和关节得分（0.853）大幅领先于 CAMS-X。
- 消融实验证实，归一化分部 BPS、接触调节与引导、以及优化后处理，各自对多样性与物理合理性有显著贡献。
- 用户偏好实验表明，BimArt 在所有物体上的偏好率均高于 MDM-B 和 OMOMO-B。
---

# BimArt A Unified Approach for the Synthesis of 3D Bimanual Interaction with Articulated Objects

> [!tip] 核心洞察
> 逐帧的距离接触图编码了丰富的双手抓握与操作模式，其细粒度的空间约束能够指导扩散模型生成符合接触逻辑的运动；分部感知的归一化 BPS 确保了对大小迥异的物体部件进行等分辨率编码，这对于铰接物体的双手交互至关重要。

| 字段 | 内容 |
|------|------|
| 中文题名 | BimArt: 一种面向关节物体的统一三维双手交互合成方法 |
| 英文题名 | BimArt A Unified Approach for the Synthesis of 3D Bimanual Interaction with Articulated Objects |
| 会议/期刊 | CVPR 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | BimArt |
| Dataset | ARCTIC, HOI4D |

> [!tip] 效果简介
> - ARCTIC 上，Pen 1cm (%) 2.0346 vs 42.519 (CAMS-B) (-40.48)；Con (%) 99.629 vs 98.915 (CAMS-B) (+0.714)；Art (%) 85.572 vs 76.704 (CAMS-B) (+8.868)。
> - HOI4D (Pliers) 上，Con. Score 0.966 vs 0.485 (CAMS-X) (+0.481)。
> - HOI4D (Scissors) 上，Art. Score 0.853 vs 0.167 (CAMS-X) (+0.686)。

## 概述

**问题瓶颈**：现有方法在合成双手与铰接物体的交互时，普遍依赖参考抓握姿态、粗糙的手部轨迹或分阶段处理抓握与关节运动，难以在一个统一模型中同时生成物体的刚体运动与关节运动，且无法泛化到不同物体类别。这导致生成的双手动作在物理合理性（穿透严重）与接触准确性上存在明显缺陷。

**核心方法**：BimArt 提出了一种三阶段统一框架，其核心创新在于以**距离为基础的双手接触图**作为中间生成先验，并结合**归一化的分部点基集（BPS）特征**，从而在无需任何参考抓握的条件下生成多样化且物理上可信的双手运动。逐帧的距离接触图编码了丰富的双手抓握与操作模式，其细粒度的空间约束能够指导扩散模型生成符合接触逻辑的运动；分部感知的归一化 BPS 确保了对大小迥异的物体部件进行等分辨率编码，这对于铰接物体的双手交互至关重要。

**方法定位**：BimArt 是目前唯一同时支持铰接物体、双手交互、无需参考抓握且采用统一模型的方法（Table 4）。其流水线包括：物体编码器（E_o / E_α）将分部 BPS 特征、全局状态和物体尺度编码为潜在特征；接触生成模型（扩散 Transformer）根据物体轨迹生成双手接触图；接触编码器（E_c）将接触图作为运动模型的条件；运动生成模型（扩散 Transformer）基于物体特征和接触图生成手部运动；最后通过基于 MANO 拟合的投影/穿透/加速度联合优化进行后处理。

**主要结果**：在 ARCTIC 数据集上，BimArt 的穿透率（Pen 1cm）仅为 2.03%，远低于 CAMS-B 的 42.52%（Table 1）；接触率（Con）达 99.63%，关节接触率（Art）达 85.57%，均全面超越 CAMS-B、MDM-B 和 OMOMO-B。在 HOI4D 跨类别评测中，BimArt 对钳子（Pliers）的接触得分达 0.966，剪刀（Scissors）的关节得分达 0.853，大幅领先于 CAMS-X（Table 2）。消融实验证实，归一化分部 BPS、接触调节与引导、以及优化后处理各自对多样性与物理合理性有显著贡献（Table 3）。用户偏好实验进一步表明，BimArt 在所有物体上的偏好率均高于 MDM-B 和 OMOMO-B（Figure 7）。

**局限与展望**：当前方法仅支持包含两个铰接部件的物体，扩散采样速度较慢，且对未见物体类别的泛化能力有限。未来方向包括利用多模态大语言模型实现零样本泛化、引入更快的扩散采样策略，以及将生成过程与物理模拟器结合以产生完全符合物理定律的交互动作。

## 背景与动机

在增强现实、机器人示教和具身智能等领域，逼真的三维双手交互生成是核心能力之一。与单手操作不同，双手交互要求两只手在空间和时间上高度协调，同时还要与物体的运动（包括刚体位移和关节变化）保持物理一致的接触关系。当操作对象为包含可动部件的铰接物体（如笔记本电脑、剪刀、钳子）时，问题的复杂性进一步上升：生成模型不仅要理解手-物体的接触模式，还必须感知物体部件的运动状态，并据此调整双手的抓握与操作策略。

现有方法在处理这一问题时存在明显的结构性缺口。**CAMS**（Zheng et al., CVPR 2023）等分阶段方法将抓握生成与关节操作解耦为独立步骤，先确定接触目标再拟合手部姿态。这种设计在动态场景下，稀疏的接触目标无法充分约束 MANO 参数拟合，导致穿透率极高（ARCTIC 数据集上 Pen 1cm 达 42.5%），交互的物理可信度严重不足。**MDM**（Tevet et al., ICLR 2023）等基于扩散模型的运动生成方法虽能产生多样化运动，但缺乏显式的接触建模机制，生成的手部常与物体表面存在明显间隙，无法建立精确的接触关系。**OMOMO** 等方法则依赖刚性接触约束，在涉及大幅度手腕运动（如打开盒子）时容易失效。

上述方法的共同瓶颈在于：**无法在不依赖参考抓握、粗糙手部轨迹或分阶段处理的条件下，同时生成物体的刚体运动与关节运动的逼真双手交互，且难以在单一模型中泛化到不同物体类别**。具体而言，现有工作普遍缺乏三个关键能力：一是对铰接物体不同部件进行等分辨率编码的特征表示，使得大小迥异的部件（如剪刀的刀刃与手柄）在特征空间中信息密度失衡；二是细粒度的空间接触先验，能够逐帧指导手部顶点与物体表面的距离关系；三是将接触先验有效注入运动生成过程的机制，确保生成结果在保持多样性的同时满足接触逻辑。

针对上述缺口，BimArt 的核心动机是：**以距离为基础的双手接触图作为中间生成先验，结合归一化的分部点基集（BPS）特征，实现多样化且物理上可信的双手运动生成，无需任何参考抓握**。其关键洞察在于：逐帧的距离接触图编码了丰富的双手抓握与操作模式，其细粒度的空间约束能够指导扩散模型生成符合接触逻辑的运动；而分部感知的归一化 BPS 确保了对大小迥异的物体部件进行等分辨率编码，这对于铰接物体的双手交互至关重要。

## 核心创新

BimArt 的核心创新在于通过**以距离为基础的双手接触图作为中间生成先验**，并结合**归一化的分部点基集（BPS）特征**，首次在单一模型中实现了无需参考抓握的、同时涵盖物体刚体运动与关节运动的逼真双手交互生成。其关键设计围绕四个 changed slots 展开。

### 1. 归一化分部 BPS 物体表示

现有方法多采用未归一化的全局 BPS 或体素表示，难以对大小迥异的铰接物体部件进行等分辨率编码。BimArt 提出**归一化分部 BPS（Normalized Part BPS）**：首先通过物体在最大展角状态下的顶点距离计算归一化尺度 $s_{\mathrm{o}}$（Eq. 1），将物体缩放到单位球内；随后对每个铰接部件（top/bottom）独立计算到 BPS 基点的最小距离向量（Eq. 2），并将两部分特征拼接为完整物体表示（Eq. 3）。这一设计确保了对不同表面积部件分配相等的特征维度，在物体内表面层实现更密集的 BPS 映射（Figure 4），为后续接触生成提供了细粒度的几何先验。消融实验证实，相比未归一化 BPS（U-BPS）和部分无关 BPS（PA-BPS），归一化分部 BPS 在多样性与接触率上均取得最优（Table 3）。

### 2. 距离接触图作为中间生成目标

基线方法或缺乏显式接触建模，或仅使用基于点的稀疏接触目标。BimArt 将**逐帧最小距离接触图**定义为生成管线中的显式中间表示：对每只手，计算每个物体顶点到该手任意顶点的最小距离向量（Eq. 4）。这一设计将丰富的双手抓握与操作模式编码为细粒度空间约束——接触图不仅指示“哪里接触”，还通过距离值编码“多近算接触”，从而指导扩散模型生成符合接触逻辑的运动。接触图生成模型（扩散 Transformer）以物体轨迹为输入，先于运动模型独立生成双手接触图，形成“先规划接触、再合成运动”的解耦范式。

### 3. 去噪过程中的接触引导

不同于仅将接触作为条件输入的做法，BimArt 在运动扩散模型的去噪过程中引入**接触引导（Contact Guidance）**机制：在每个去噪步骤，从当前预测的干净手部关键点推导出即时接触图（Eq. 5），计算其与目标接触图的差异，并通过梯度下降将运动拉向接触一致的方向（Eq. 6）。同时，结合分类器自由引导（Eq. 7），在多样性与接触一致性之间取得平衡。消融实验表明，引入接触调节（w C）提升了多样性、接触率和关节接触率，而接触引导（w C+CG）进一步降低了接触图差异（Table 3）。

### 4. 物理后处理优化

生成的手部运动可能存在穿透、悬浮和时间抖动等问题。BimArt 设计了基于 MANO 拟合的**联合优化后处理模块**：首先通过最小化预测关键点与 MANO 前向输出之间的距离估计 MANO 参数（Eq. 8）；随后以投影损失（Eq. 10）、穿透损失（Eq. 11）和加速度平滑损失（Eq. 12）组成的联合目标（Eq. 9）进行优化。这一模块大幅降低了穿透百分比和加速度，同时保持高接触率（Table 3），弥补了纯生成模型在物理合理性上的不足。

综上，BimArt 通过上述四个 changed slots 的系统性创新，在 ARCTIC 和 HOI4D 数据集上全面超越 CAMS-B、MDM-B、OMOMO-B 等基线方法，尤其在穿透率（Pen 1cm 仅 2.03% vs CAMS-B 的 42.5%）和关节接触率（Art 85.57% vs CAMS-B 76.70%）上取得显著提升（Table 1），并首次展示了跨类别的统一双手交互生成能力（Table 2）。

## 整体框架

BimArt 采用三阶段流水线，将关节物体的 7-DoF 轨迹（6D 全局位姿 + 1D 关节角）作为唯一输入，输出逐帧的双手 MANO 参数，全程无需参考抓握或粗糙手部轨迹。

**输入与输出定义。** 给定 N 帧物体轨迹 $\xi = \{\xi_i\}_{i=1}^N$，其中 $\xi_i = [\mathbf{g}_i | \mathbf{a}_i]$，$\mathbf{g}_i \in \mathbb{R}^6$ 为根节点的朝向与平移，$\mathbf{a}_i \in \mathbb{R}$ 为旋转关节角度。BimArt 生成对应的 N 帧双手运动 $\Theta = \{\Theta_i\}_{i=1}^N$，$\Theta_i \in \mathbb{R}^{61 \times 2}$ 对应左右手 MANO 参数。

**三阶段流水线。** 图 2 展示了完整流程：

1. **接触图生成。** 物体编码器 $\mathcal{E}_o$ 将关节感知的分部 BPS 特征、6D 全局状态和归一化尺度 $s_o$ 编码为潜在特征，送入扩散 Transformer 生成双手距离接触图 $\mathbf{C}$。该接触图编码了每只手到物体每个顶点的最小距离向量，作为中间生成先验。

2. **手部运动生成。** 接触编码器 $\mathcal{E}_c$ 将生成的接触图 $\mathbf{C}$ 编码为条件信号，与物体编码器 $\mathcal{E}_\alpha$ 输出的物体特征共同输入运动扩散 Transformer。在去噪过程中，接触引导机制通过梯度下降最小化当前预测手部推导的接触图与目标接触图之间的差异，使生成的运动逐步对齐接触先验。分类器自由引导则平衡多样性与接触一致性。

3. **优化后处理。** 对扩散模型输出的手部表面关键点进行 MANO 参数拟合，并联合优化投影损失、穿透损失和加速度平滑损失，得到最终的双手网格序列。

**手部与物体表示。** 手部运动在物体规范坐标系中编码——该坐标系将关节轴对齐至负 z 轴，确保运动表示与物体姿态解耦。每只手由表面关键点位置和指向最近物体表面的方向向量参数化。物体则通过归一化分部 BPS 特征表示：先按最大展角状态下的顶点距离计算归一化尺度 $s_o$，再对每个部件独立计算基点到最近顶点的距离向量，最后将所有帧、所有部件的 BPS 特征拼接为完整物体表示。这种分部感知的归一化策略确保了对大小迥异的物体部件进行等分辨率编码。

**流水线中的关键因果机制。** 距离接触图作为中间生成目标，将复杂的双手-物体空间关系压缩为逐顶点的距离场，既降低了直接生成手部运动的难度，又为后续运动生成提供了细粒度的空间约束。接触引导则进一步在去噪过程中强制执行这种约束，使生成的运动在保持多样性的同时具备物理合理性。

### 补充图表

![[assets/figures/papers/paper_list_l1730_BimArt_A_Unified_Approach_for_the_Synthesis_of_3D_Bimanual_Interaction_w/figures/002_Figure_2.jpg]]
*Figure 2: Overview. BimArt takes N frames of object trajectories as input and generates N frames of 3D bimanual interactions. The object features (articulation-aware BPS features O, 6D global states G, and the object scale*

## 核心模块与公式推导

BimArt 的生成流水线由五个核心模块构成，各模块之间通过归一化分部 BPS 特征和距离接触图紧密耦合。以下按数据流顺序逐一说明其设计逻辑与关键公式。

---

### 3.1 物体编码器

物体编码器负责将铰接物体的几何与运动信息压缩为统一的潜在特征，供下游的接触生成模型和运动生成模型共享。其输入包含三部分：

- **归一化分部 BPS 特征** $\mathbf{O}$：解决不同物体部件尺度差异导致的特征分辨率不均问题。
- **6D 全局状态** $\mathbf{G}$：描述物体根节点的朝向与平移。
- **物体尺度** $s_{\mathrm{o}}$：用于将物体归一化到单位球内。

**尺度归一化公式**：

$$s_{\mathrm{o}} = \frac{1 - d_{\mathrm{margin}}}{\max_{\mathbf{v} \in \mathbf{V}_{\mathrm{ao}}} \|\mathbf{v}\|} \tag{1}$$

其中 $\mathbf{V}_{\mathrm{ao}}$ 是物体处于最大展开角度时的顶点集合，$d_{\mathrm{margin}}$ 是防止物体触及单位球边界的边距。该操作确保不同尺寸的物体在归一化空间中具有可比的特征分布。

**分部 BPS 特征计算**：

$$\mathbf{O}_i^p = \left[ \operatorname{argmin}_{\mathbf{v} \in \mathbf{V}_i^p} d\left(\frac{\mathbf{v}}{s_0}, \mathbf{b}\right) - \mathbf{b}, \ \mathrm{for} \ \mathbf{b} \in \mathbf{B} \right] \tag{2}$$

对每个物体部件 $p \in \{\text{top}, \text{bottom}\}$ 和每一帧 $i$，计算归一化后的部件顶点到每个基点点 $\mathbf{b}$ 的最小距离向量。基点点集 $\mathbf{B}$ 在单位球内均匀采样，为每个部件分配 $K$ 个基点，从而保证无论部件表面积大小，均获得等分辨率的编码。

**全物体特征拼接**：

$$\mathbf{O} = [\mathbf{O}_i^p, \ \mathrm{for} \ i \in \{1, 2, \dots, N\}, \ p \in \{\text{top, bottom}\}] \tag{3}$$

所有帧和两个部件的 BPS 特征沿通道维度拼接，形成完整的物体时空表示。物体编码器 $\mathcal{E}_o$（用于接触模型）和 $\mathcal{E}_\alpha$（用于运动模型）均为 MLP，将拼接后的特征映射为扩散模型的条件嵌入 $\mathbf{Z}_o$。

---

### 3.2 接触生成模型

接触生成模型是一个扩散 Transformer，以物体轨迹条件 $\mathbf{Z}_o$ 为输入，生成逐帧的双手距离接触图。接触图作为中间生成先验，编码了手部与物体表面之间的细粒度空间关系。

**接触图定义**：

$$\mathbf{C}_i^{\rho} = \left[ \operatorname{argmin}_{\mathbf{h} \in \Xi_i^{\rho}} d(\mathbf{h}, \mathbf{v}) - \mathbf{v}, \ \text{for} \ \mathbf{v} \in \tilde{\mathbf{V}}_i \right], \quad \rho \in \{\text{left, right}\} \tag{4}$$

其中 $\Xi_i^{\rho}$ 是第 $i$ 帧左手或右手的手部顶点集合，$\tilde{\mathbf{V}}_i$ 是物体表面采样顶点。对每个物体顶点 $\mathbf{v}$，计算其到手部最近顶点的距离向量。该向量场同时编码了接触位置（向量起点）和接触距离（向量模长），为后续运动生成提供了丰富的空间约束。

接触生成模型通过标准扩散去噪过程从高斯噪声逐步恢复接触图，训练目标为最小化预测噪声与真实噪声之间的均方误差。

---

### 3.3 运动生成模型与接触引导

运动生成模型同为扩散 Transformer，以物体特征 $\mathbf{Z}_o$ 和接触编码器 $\mathcal{E}_c$ 编码的接触图条件 $\mathbf{Z}_c$ 为输入，生成双手的表面关键点位置 $\mathbf{H}$ 和方向向量 $\mathbf{D}$。为增强生成运动与接触图的一致性，BimArt 在去噪过程中引入了接触引导机制。

**从预测手部推导接触图**：

$$\tilde{\mathbf{C}}_{(t)}^{\rho} = \left[ \operatorname{argmin}_{\mathbf{h} \in \hat{\mathbf{H}}_{(t)}^{\rho}} d(\mathbf{h}, \mathbf{v}) - \mathbf{v}, \ \text{for} \ \mathbf{v} \in \tilde{\mathbf{V}} \right], \quad \rho \in \{\text{left, right}\} \tag{5}$$

在去噪步骤 $t$，从当前预测的干净手部关键点 $\hat{\mathbf{H}}_{(t)}^{\rho}$ 重新计算接触图，与目标接触图 $\hat{\mathbf{C}}^{\rho}$ 比较。

**接触引导方程**：

$$\tilde{\mathbf{X}}_{(t)}^{\rho} = \hat{\mathbf{X}}_{(t)}^{\rho} - \lambda_c \nabla_{\hat{\mathbf{X}}_t^{\rho}} \left\| \hat{\mathbf{C}}^{\rho} - \tilde{\mathbf{C}}_{(t)}^{\rho} \right\| \tag{6}$$

通过梯度下降最小化预测接触图与目标接触图的差异，引导预测的运动 $\hat{\mathbf{X}}_{(t)}^{\rho}$ 向符合接触先验的方向修正。引导尺度 $\lambda_c$ 设为梯度范数的倒数，以自适应调节步长。

**分类器自由引导组合**：

$$\tilde{\mathbf{X}}_{(t-1)} = (1 + \lambda_f) \tilde{\mathbf{X}}_{(t)} - \mathcal{M}(\hat{\mathbf{X}}^{(t)}, t, \mathbf{Z}_o \varnothing) \tag{7}$$

将带接触条件 $\mathbf{Z}_c$ 和空条件 $\varnothing$ 的两路去噪输出按引导强度 $\lambda_f$ 线性组合，在多样性与接触一致性之间取得平衡。训练时以 0.5 的概率随机丢弃接触条件，使模型学会条件与无条件两种生成模式。

---

### 3.4 优化后处理模块

扩散生成的手部关键点序列可能存在穿透、悬浮和时间抖动等物理不一致性。优化后处理模块通过 MANO 参数拟合与多目标正则化对生成结果进行精修。

**MANO 拟合损失**：

$$l_{\mathrm{MANO}} = \left\| \hat{\mathbf{H}} - f_{\mathrm{MANO}}(\boldsymbol{\theta}, \beta) \right\| \tag{8}$$

最小化预测关键点 $\hat{\mathbf{H}}$ 与 MANO 模型前向输出之间的欧氏距离，估计手部姿态参数 $\boldsymbol{\theta}$ 和形状参数 $\beta$。

**物理正则化损失**：

$$l_{\mathrm{reg}} = w_{\mathrm{proj}} l_{\mathrm{proj}} + w_{\mathrm{pen}} l_{\mathrm{pen}} + w_{\mathrm{acc}} l_{\mathrm{acc}} \tag{9}$$

由三项子损失加权组合，在 ARCTIC 数据集上权重设置为 $w_{\mathrm{proj}}=100$、$w_{\mathrm{pen}}=10$、$w_{\mathrm{acc}}=1000$。

**投影损失**：

$$l_{\mathrm{proj}} = \sum_{\mathbf{p} \in \mathbf{P}} \min_{\mathbf{v} \in \mathbf{V}} \| \mathbf{p} - \mathbf{v} \| \tag{10}$$

鼓励方向向量的投影点 $\mathbf{p}$ 落在物体表面 $\mathbf{V}$ 上，消除手部悬浮现象。

**穿透损失**：

$$l_{\mathrm{pen}} = \sum_{\mathbf{h} \in \mathrm{Int}(\hat{\Xi})} \min_{\mathbf{v} \in \mathbf{V}} \left\| \mathbf{h} - \mathbf{v} \right\| \tag{11}$$

惩罚陷入物体内部的手部顶点 $\mathrm{Int}(\hat{\Xi})$，将其推向最近的表面点。

**加速度平滑损失**：

$$l_{\mathrm{acc}} = \sum_{\mathbf{h}_i \in \hat{\Xi}} \| \mathbf{h}_i - 2 \cdot \mathbf{h}_{i-1} + \mathbf{h}_{i-2} \| \tag{12}$$

最小化手部顶点轨迹的二阶差分，抑制时间轴上的高频抖动，使运动更加平滑自然。

### 补充图表

![[assets/figures/papers/paper_list_l1730_BimArt_A_Unified_Approach_for_the_Synthesis_of_3D_Bimanual_Interaction_w/figures/004_Figure_4.jpg]]
*Figure 4: Different BPS Sampling Strategies. Top left*

## 实验与分析

### 主实验结果

BimArt 在两个核心基准上展现了显著的双手交互物理合理性优势。在 **ARCTIC** 数据集（Table 1）上，BimArt 将穿透率（Pen 1cm）从 CAMS-B 的 42.52% 大幅降至 **2.03%**，降幅达 40.48 个百分点；接触率（Con）达到 99.63%，关节接触率（Art）达 85.57%，分别领先 CAMS-B 0.71 和 8.87 个百分点。值得注意的是，CAMS-B 虽在多样性（Multimodality）和加速度平滑性上优于 BimArt，但其极高的穿透率导致交互整体不可信——这一矛盾揭示了仅优化运动统计量而忽视接触约束的固有缺陷。MDM-B 和 OMOMO-B 在穿透与接触指标上也均明显弱于 BimArt，验证了以距离接触图作为中间生成先验的有效性。

![[assets/figures/papers/paper_list_l1730_BimArt_A_Unified_Approach_for_the_Synthesis_of_3D_Bimanual_Interaction_w/figures/005_Table_1.jpg]]
*Table 1: Quantitative Comparison on ARCTIC. Our method outperforms the state-of-the-art in penetration, contact, and articulation. Even though CAMS-B scores better in the multimodality and acceleration, it exhibits low interaction plausibility, as seen in high penetration percentage and qualitative results in Fig. 5*

在 **HOI4D** 跨类别评测（Table 2）中，BimArt 以统一模型（Unified）训练，在钳子（Pliers）和剪刀（Scissors）上的接触得分分别达到 **0.966** 和 **1.000**，关节得分达 0.853，大幅超越跨类别基线 CAMS-X（对应得分分别为 0.485、0.858 和 0.167）。在部分物体上，BimArt 的统一模型表现甚至接近或达到类别特定训练方法（Cat.Spec）的水平，验证了归一化分部 BPS 表示对跨类别泛化的关键支撑作用。

![[assets/figures/papers/paper_list_l1730_BimArt_A_Unified_Approach_for_the_Synthesis_of_3D_Bimanual_Interaction_w/figures/006_Table_2.jpg]]
*Table 2: Evaluation on the HOI4D Dataset. We show comparisons in the category-specific setting (denoted as “Cat.Spec”) and the cross-category setting where a unified model is trained (denoted as “Unified”). The numbers for “Cat.Spec” are taken from CAMS [82]. Our method outperforms CAMS-X, and performs comparatively with methods trained in a category-specific way*

用户偏好实验（Figure 7）进一步佐证了定量结果：在所有测试物体上，参与者对 BimArt 的偏好率均高于 MDM-B 和 OMOMO-B，表明生成的运动在视觉真实感和交互合理性上获得了人类评估者的一致认可。

![[assets/figures/papers/paper_list_l1730_BimArt_A_Unified_Approach_for_the_Synthesis_of_3D_Bimanual_Interaction_w/figures/010_Figure_7.jpg]]
*Figure 7: User Study Results. We show the preference rate of BimArt against MDM-B and OMOMO-B. Our method outperforms existing state-of-the-art for all objects covered in the user study*

### 消融实验分析

消融实验（Table 3）系统拆解了物体表示、接触建模和后处理三个核心设计的作用：

**归一化分部 BPS（NP-BPS）** 相比未归一化 BPS（U-BPS）和分部无关 BPS（PA-BPS），在多样性和接触率上均表现最优。其优势源于两个机制：（1）尺度归一化使不同大小的物体部件获得等分辨率编码，避免了大部件主导特征空间；（2）分部独立计算 BPS 特征确保了铰接物体的运动部件（如剪刀手柄）获得与固定部件同等的特征维度，从而在接触图映射中实现更密集的内表面覆盖（Figure 4 底部，Table 6 的接触图误差分析佐证了这一点）。

**接触调节（w C）** 的引入提升了多样性、接触率和关节接触率，表明接触图作为条件信号能有效约束生成空间，使运动向物理合理的方向收敛。在此基础上加入**接触引导（CG）** 进一步降低了接触图差异，使生成的手部关键点更贴合预期的接触分布——这验证了在去噪过程中显式对齐接触图的必要性，而非仅将其作为被动条件输入。

**优化后处理（Opt）** 在保持高接触率的前提下，大幅降低了穿透百分比和加速度。具体而言，投影损失（Eq. 10）消除悬浮现象，穿透损失（Eq. 11）惩罚手部顶点陷入物体内部，加速度平滑损失（Eq. 12）抑制时间上的抖动。三项损失的联合优化（Eq. 9）使最终输出在物理合理性上达到实用水平。

### 定性结果与失败模式

定性比较（Figure 5）揭示了各基线的典型失败模式：MDM-B 难以建立精确接触，在剪刀和盒子示例中出现明显的手-物间隙；OMOMO-B 的刚性接触约束在需要大幅度腕部运动时（如打开盒子）容易失效；CAMS-B 的分阶段接触目标在动态场景和复杂接触模式下欠约束 MANO 拟合，导致生成动作不合理。

![[assets/figures/papers/paper_list_l1730_BimArt_A_Unified_Approach_for_the_Synthesis_of_3D_Bimanual_Interaction_w/figures/008_Figure_5.jpg]]
*Figure 5: Qualitative Comparison. MDM-B struggles with establishing accurate contact, as seen in the hand-object gap in the scissors and the box example. OMOMO-B’s rigid contact constraints make it prone to failure, especially with large wrist movements, like opening a box. CAMS-B failed to generate plausible motions, since its stage-wise contact targets under-constrain MANO fitting in dynamic settings with complex contact patterns and diverse object trajectories*

多样性生成结果（Figure 6）展示了 BimArt 对同一未见轨迹生成多种合理交互的能力，预测的接触图准确指导了手指放置位置。接触图可视化（Figure 9）进一步揭示了模型对“抓握”和“关节操作”两种模式的区分能力：关节操作示例中，接触区域始终保持在运动部件上；抓握示例中，一只手固定物体，另一只手调整接触点。

![[assets/figures/papers/paper_list_l1730_BimArt_A_Unified_Approach_for_the_Synthesis_of_3D_Bimanual_Interaction_w/figures/009_Figure_6.jpg]]
*Figure 6: Diverse Results. We show diverse bimanual sequences together with the predicted contact maps on the laptop, ketchup and mixer given the same unseen trajectory per object. Our method generates accurate finger placements guided by the predicted contact maps*

### 已知局限

1. **物体拓扑限制**：当前方法仅支持包含两个铰接部件的物体，无法处理更复杂的多部件结构或变形物体。
2. **推理效率**：扩散模型的迭代采样过程较慢，无法满足实时生成需求。
3. **泛化边界**：训练数据集中于 ARCTIC 和 HOI4D，对未见物体类别的泛化能力受限于数据覆盖范围。
4. **物理保真度**：后处理优化仅缓解穿透和抖动，无法保证复杂的物理约束（如摩擦、受力平衡），生成的运动在严格物理意义上仍可能不成立。

### 补充图表

![[assets/figures/papers/paper_list_l1730_BimArt_A_Unified_Approach_for_the_Synthesis_of_3D_Bimanual_Interaction_w/figures/012_Table_5.jpg]]
*Table 5: Penetration percentage at 5mm threshold*

![[assets/figures/papers/paper_list_l1730_BimArt_A_Unified_Approach_for_the_Synthesis_of_3D_Bimanual_Interaction_w/figures/013_Table_6.jpg]]
*Table 6: Contact Map Error (in cm) due to BPS mapping. We present the average and per-category contact map errors resulting from the sparse mapping of BPS features. Both part-agnostic BPS (PA-BPS) and the proposed part BPS (P-BPS) achieve a denser mapping compared to BPS features without scale normalization (U-BPS), resulting in smaller contact map errors. The proposed part-based BPS method further enhances mapping density for the top part of the object (which corresponds to the movable part in canonical space), by allocating equal feature dimensions to individual parts irrespective of their surface area*

## 方法谱系与知识库定位

### 1 与现有工作的关系

BimArt 的核心贡献在于首次将**双手交互生成**、**物体关节运动**与**无参考抓握的接触推理**统一于单一扩散框架中。其与现有工作的关系可从四个维度理解。

**相对于双手交互生成方法。** 早期的双手交互工作，如 **CAMS**（Zheng et al., CVPR 2023），采用分阶段策略：先生成粗糙的手部轨迹，再通过接触目标进行 MANO 拟合。CAMS 依赖类别特定的训练，且其接触目标在动态场景中约束不足，导致高穿透率（ARCTIC 上 Pen 1cm 达 42.5%）。BimArt 摒弃了分阶段范式，通过**距离接触图作为中间生成先验**，在扩散模型内部完成接触推理与运动生成的联合建模，从而在穿透率上实现数量级下降（降至 2.03%）。

**相对于人体-物体交互的扩散模型。** **MDM**（Tevet et al., ICLR 2023）将运动扩散模型引入人体动作生成，但其双手适配版本 MDM-B 仅将物体轨迹作为条件输入，缺乏显式的接触建模。这导致 MDM-B 在剪刀、盒子等物体上出现明显的手-物间隙（Figure 5）。BimArt 在扩散过程中引入**接触引导**（Contact Guidance），通过梯度下降最小化预测接触图与目标接触图的差异（Eq. 6），使生成的运动主动对齐接触先验。

**相对于物体表示方法。** 传统方法使用全局 BPS（Basis Point Set）或体素表示编码物体几何。BimArt 提出的**归一化分部 BPS**（Normalized Part BPS）有两个关键改进：（1）通过物体尺度归一化（Eq. 1）消除不同大小物体间的尺度差异；（2）对每个铰接部件独立分配等量基点数，确保小部件（如剪刀的活动刃）获得与大部件相同的特征分辨率。Table 6 的接触图误差分析证实，分部 BPS 比未归一化 BPS 的映射误差更小，尤其对物体活动部件（top part）的映射密度显著提升。

**相对于后处理优化。** 现有方法或缺乏后处理，或仅做简单的穿透修正。BimArt 的优化后处理模块联合最小化投影损失、穿透损失和加速度平滑损失（Eq. 9-12），在 MANO 参数空间中进行拟合，同时解决悬浮、穿透和时间抖动三个问题。消融实验（Table 3）表明，该模块将穿透百分比从 8.67% 降至 2.03%，加速度指标也大幅改善。

### 2 适用边界与局限

BimArt 的设计存在以下明确边界：

**物体拓扑限制。** 方法仅支持**包含两个铰接部件的物体**（如笔记本电脑、剪刀、钳子），无法处理多部件铰接结构（如多关节机械臂）或可变形物体（如布料、绳索）。这一限制源于分部 BPS 表示和接触图定义均假设物体由固定的两个部件组成。

**生成速度瓶颈。** 扩散模型的迭代去噪过程导致采样速度较慢，无法满足实时交互应用的需求。论文未报告具体的推理延迟数据，但明确指出这是扩散模型固有的局限。

**泛化边界。** 训练数据集中于 ARCTIC（10 类物体）和 HOI4D（6 类物体），对未见过的物体类别泛化能力有限。尽管 HOI4D 跨类别实验（Table 2）展示了统一模型的潜力，但物体几何和运动模式的分布外泛化仍未被充分验证。

**物理保真度不足。** 后处理优化仅缓解穿透和抖动，无法保证复杂的物理约束，如摩擦力、接触力平衡和动力学一致性。生成的运动可能在视觉上合理，但未必满足牛顿力学。

### 3 开放问题与后续方向

基于上述局限，以下方向值得探索：

1. **零样本泛化。** 如何利用多模态大语言模型（MLLM）的常识推理能力，使模型在未见物体上推断合理的抓握区域和操作模式，而无需重新训练？
2. **高效采样策略。** 引入 DDIM、潜在扩散模型（Latent Diffusion）或一致性模型（Consistency Models）等加速采样技术，将生成延迟降低至实时或近实时水平。
3. **物理模拟耦合。** 将扩散生成过程与物理模拟器（如 Isaac Gym）结合，在生成阶段或后处理阶段引入物理约束，确保输出动作满足接触力、摩擦锥和动量守恒等物理定律。
4. **多部件与可变形物体扩展。** 将分部 BPS 表示泛化到任意数量的铰接部件，或引入基于图的物体表示以支持可变形物体的交互生成。

## 原文 PDF

![[paperPDFs/CVPR_2025/BimArt_A_Unified_Approach_for_the_Synthesis_of_3D_Bimanual_Interaction_with_Articulated_Objects.pdf]]