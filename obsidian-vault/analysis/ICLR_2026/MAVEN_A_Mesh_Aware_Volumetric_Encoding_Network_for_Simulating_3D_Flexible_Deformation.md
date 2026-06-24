---
title: "MAVEN: A Mesh-Aware Volumetric Encoding Network for Simulating 3D Flexible Deformation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MAVEN_A_Mesh_Aware_Volumetric_Encoding_Network_for_Simulating_3D_Flexible_Deform_cdb77aedb5f8.pdf
project_link: null
code_link: "https://github.com/zhefeng27/MAVEN"
aliases:
- MAVEN
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/benchmarks_datasets_evaluation
core_operator: 显式引入3D单元和2D面片作为独立的图节点，通过位置感知的几何聚合器将顶点信息映射到高维元素，并在单元-面片二分图上执行两阶段消息传递，使模型能够准确刻画接触边界和体积内场的演化。
primary_logic: 将网格视为包含顶点、面片和单元的三层拓扑结构，并设计对称的聚合-分解机制，使得高维几何特征（体积、面积、周长等）与物理状态深度融合，从而在粗网格下依然保持数值稳定和几何保真度。
claims:
- 消融实验中，完全不建模高维几何元素（Model C）使性能退化至传统节点型方法水平（Cavity Grasping位置RMSE 17.08 vs MAVEN 15.41），证明了面片-单元结构的必要性。
- 移除显式几何特征（Model B）在稀疏Metal Bending数据集上导致位置误差暴增至1652.31（MAVEN 810.42），应力误差6680.39（MAVEN 4776.72），说明显式几何特征对粗网格下的精度至关重要。
- 在Metal Bending数据集上，MAVEN推理每步仅需23.57ms，比传统Abaqus仿真器（712.44ms）快2922.66%，同时预测更准确，验证了数据驱动替代模型的高效性。
- Cavity Grasping 上 Position RMSE (full rollouts) = 15.41
---

# MAVEN: A Mesh-Aware Volumetric Encoding Network for Simulating 3D Flexible Deformation

> [!tip] 核心洞察
> 将网格视为包含顶点、面片和单元的三层拓扑结构，并设计对称的聚合-分解机制，使得高维几何特征（体积、面积、周长等）与物理状态深度融合，从而在粗网格下依然保持数值稳定和几何保真度。

| 字段 | 内容 |
|------|------|
| 中文题名 | MAVEN: 网格感知体积编码网络用于3D柔性变形模拟 |
| 英文题名 | MAVEN: A Mesh-Aware Volumetric Encoding Network for Simulating 3D Flexible Deformation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=XmULVr15E0) · [Code](https://github.com/zhefeng27/MAVEN) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/benchmarks_datasets_evaluation |
| Method | MAVEN |
| Dataset | Cavity Grasping, Metal Bending |

> [!tip] 效果简介
> - Cavity Grasping 上，Position RMSE (full rollouts) 15.41 vs 17.08 (Model C, equivalent to node-based GNNs) (-9.8%)。
> - Metal Bending 上，Position RMSE (full rollouts) 810.42 vs 1680.20 (Model C) (-51.8%)；Inference time (ms/step) 23.57 vs 712.44 (Abaqus simulator) (2922.66% faster)。

## 概述

物理模拟的连续介质在数值求解时通常被离散为结构化网格，而现有基于图神经网络（GNN）的模拟器仅将网格抽象为顶点和边构成的点-边图。这种简化忽视了网格中天然存在的高维几何元素——2D面片和3D单元，导致在稀疏网格下接触检测不准确、物理量沿边界和体积的传播误差增大。**MAVEN**（Mesh-Aware Volumetric Encoding Network）针对这一瓶颈，首次将网格的完整三层拓扑结构（顶点、面片、单元）显式引入图网络架构，通过位置感知的几何聚合器与两阶段单元-面片消息传递机制，实现了高维几何特征与物理状态的深度融合。

核心结论可概括为三点：
1. **高维几何元素不可或缺**：消融实验中，完全不建模面片和单元（等效于传统节点型GNN）使性能退化至基线水平——在Cavity Grasping上位置RMSE从15.41升至17.08，在Metal Bending上从810.42升至1680.20（Table 2）。
2. **显式几何特征对粗网格至关重要**：移除几何特征编码后，稀疏Metal Bending数据集上位置误差暴增至1652.31，应力误差升至6680.39（Table 2, Model B），说明模型难以从稀疏顶点信息中隐式推断体积与边界效应。
3. **数据驱动替代方案具备实用价值**：在Metal Bending任务上，MAVEN每步推理仅需23.57ms，比传统Abaqus仿真器（712.44ms/步）快约30倍，同时保持更高预测精度（Table 5）。

在方法谱系中，MAVEN位于**网格感知图网络模拟器**这一新兴方向，相较于仅建模面片接触的**FIGNet**（Allen et al., 2023）和基于层次化图结构的**HOOD**（Grigorev et al., 2023），其核心差异在于同时引入3D单元和2D面片作为独立图节点，并设计了对称的几何聚合-分解机制，使体积内场演化与接触边界处理统一在同一框架下。

## 背景与动机

物理仿真中，连续材料域上的物理状态通常通过结构化网格进行离散化表示。传统的基于图神经网络（GNN）的物理模拟器，如**MGN**（Pfaff et al., 2020）和**GT**（Yun et al., 2019），将网格抽象为仅包含顶点和边的点-边图，并在其上执行消息传递以预测系统演化。这种抽象虽然简洁，却存在一个根本性的瓶颈：**它忽略了网格中固有的高维几何元素——2D面片和3D单元**。在稀疏网格条件下，这一缺陷导致接触检测不准确、物理量传播误差增大，使模型难以精确模拟边界效应和体积内场的演化。

具体而言，节点型方法依赖顶点间的欧氏距离来构建接触边，这在粗网格下容易遗漏或误判接触区域。同时，由于缺乏对体积和表面积等几何属性的显式建模，模型必须隐式地从顶点位置推断这些信息，极大增加了学习负担。已有工作如**FIGNet**（Allen et al., 2023）引入了面片级别的接触网络，但仍缺少有效的体积内传播机制，未能充分利用3D单元所蕴含的结构信息。

MAVEN的核心动机正是弥合这一鸿沟：**将网格视为包含顶点、面片和单元的三层拓扑结构**，显式地引入高维几何元素作为独立的图节点，并设计对称的聚合-分解机制，使体积、面积、周长等几何特征与物理状态深度融合。通过这种网格感知的体积编码方式，模型能够在粗网格下依然保持数值稳定性和几何保真度，同时大幅降低对隐式几何学习的依赖。

## 核心创新

MAVEN的核心创新在于**将传统图网络模拟器对网格的“顶点-边”抽象，升级为“顶点-面片-单元”三层拓扑建模**，从而显式捕获3D体积和2D接触面的几何与物理信息。这一设计通过三个紧密耦合的机制实现：

### 1. 高维几何元素的图节点化

现有基于图网络的方法（如**MGN** (Pfaff et al., 2020)、**HOOD** (Grigorev et al., 2023)）仅将网格顶点作为图节点，通过顶点间距离构建接触边。这种抽象忽略了网格中固有的2D面片和3D单元，导致在稀疏网格下接触检测不准确、物理量传播误差增大——这正是本文识别出的核心瓶颈。

MAVEN将每个3D单元和2D面片分别构造为独立的图节点。单元节点编码**体积**和**表面积**，面片节点编码**面积**和**周长**，且同时注入这些几何属性的初始值作为参考锚点：

$$\mathbf { h } _ { c _ { i } } = \mathcal { A } ^ { C } ( \Omega ( c _ { i } ^ { t } ) , \Sigma ( c _ { i } ^ { t } ) , \Omega ( c _ { i } ^ { 0 } ) , \Sigma ( c _ { i } ^ { 0 } ) ) , \ \mathbf { h } _ { f _ { i } } = \mathcal { A } ^ { F } ( \alpha ( f _ { i } ^ { t } ) , \lambda ( f _ { i } ^ { t } ) , \alpha ( f _ { i } ^ { 0 } ) , \lambda ( f _ { i } ^ { 0 } ) )$$

消融实验（Table 2）提供了决定性证据：完全不建模高维几何元素的Model C在Cavity Grasping上位置RMSE退化至17.08（MAVEN为15.41），在Metal Bending上退化至1680.20（MAVEN为810.42），性能回落至传统节点型方法的水平。移除显式几何特征的Model B在稀疏Metal Bending数据集上位置误差暴增至1652.31，应力误差升至6680.39，验证了显式几何特征对粗网格下精度的关键作用。

### 2. 位置感知的几何聚合器

传统图网络使用邻域平均或注意力机制聚合节点信息，忽略了顶点相对于高维元素的局部几何关系。MAVEN设计了**位置感知几何聚合器**：对每个单元（或面片），以其中心为原点建立局部坐标系，将关联顶点的相对位置向量拼接后输入MLP，生成归一化的聚合权重：

$$a _ { c _ { i } , v _ { 0 } , \ . \ . \ , \ a _ { c _ { i } , v _ { K - 1 } } } = \mathrm { M L P } \left( \operatorname * { c o n c a t } _ { v \in \{ v _ { 0 } , \ldots , v _ { K - 1 } \} } ( \vec { \mathrm { d } } _ { c _ { i } , v } ) \right)$$

这一设计使聚合过程感知顶点在单元/面片内的空间分布，而非简单的度数平均。消融实验中，使用度数平均聚合的Model A在稀疏CG数据集上性能显著下降（Table 2），证实了位置敏感聚合的重要性。

### 3. 单元-面片二分图上的两阶段消息传递

与FIGNet（Allen et al., 2023）仅建模面片接触但缺乏体积内传播机制不同，MAVEN构建了**单元-面片二分图**，并在其上执行两阶段消息传递：

- **第一阶段（面片阶段）**：面片节点综合外部接触力、脚本化运动特征以及相邻单元的上轮信息进行更新。
- **第二阶段（单元阶段）**：单元节点汇总所有关联面片的第一阶段输出，完成体积内的物理量传播。

这一对称的聚合-分解机制（顶点→高维元素→顶点）使得接触边界和体积内场的演化被解耦建模，在粗网格下依然保持数值稳定和几何保真度。接触检测也从传统的顶点间欧氏距离升级为基于Bounding Volume Hierarchy的面片-面片碰撞检测，进一步提升了接触建模的精度。

### 创新总结

| 设计维度 | 基线方法 | MAVEN |
|---------|---------|-------|
| 图结构 | 仅顶点+边 | 顶点+面片+单元三层节点；单元-面片二分图 |
| 节点特征 | 顶点物理量+相对位置 | 单元编码体积/表面积；面片编码面积/周长（含初始值） |
| 信息聚合 | 邻域平均/注意力 | 位置感知几何聚合器（局部坐标系+MLP权重） |
| 内部传播 | 顶点-边单向传递 | 两阶段消息传递（面片→单元→顶点） |
| 接触检测 | 顶点间欧氏距离 | BVH面片-面片碰撞检测 |

这三个机制并非孤立创新，而是形成因果链条：高维节点化提供了几何载体，位置感知聚合器保证了顶点到高维元素的保真映射，两阶段消息传递则在高维空间完成接触与体积效应的解耦传播。三者共同使MAVEN在稀疏网格下仍能实现比传统Abaqus仿真器快近30倍的推理速度（23.57ms vs 712.44ms/步），同时保持更高的预测精度。

## 整体框架

MAVEN 遵循经典的编码器-处理器-解码器（encoder-processor-decoder）流水线架构，其核心创新在于将网格显式建模为包含顶点（vertex）、面片（facet）和单元（cell）的三层拓扑结构，并在这一扩展的图结构上执行几何感知的消息传递。

### 流水线总览

如图2所示，MAVEN 的整体计算流程分为三个阶段：

1.  **编码器（Encoder）**：将顶点上的物理场量、单元与面片的几何属性（体积、表面积、面积、周长及其初始值）分别映射为高维隐空间特征。同时，编码器还负责提取面片-面片接触特征与外力特征。
2.  **处理器（Processor）**：由 $L$ 层堆叠的几何感知处理块构成。每一层依次执行四个关键操作：
    *   **几何聚合器**：基于每个高维元素（单元/面片）的局部坐标系，学习顶点到该元素的加权聚合系数，将顶点信息汇聚到单元和面片节点。
    *   **面片阶段消息传递**：面片节点综合来自外力、面片-面片接触边以及相邻单元的信息，更新自身特征。
    *   **单元阶段消息传递**：单元节点汇总其所有关联面片的更新后特征，完成体积内场的演化。
    *   **几何分解器**：将处理后的单元和面片特征反向映射回顶点，更新顶点特征。
3.  **解码器（Decoder/Updater）**：将处理器输出的最终顶点特征解码为速度与物理量预测，并通过一阶积分更新顶点位置。

### 三层图结构与数据流

MAVEN 将传统 GNN 模拟器中仅包含顶点和边的图结构（图1b）替换为一个包含三种节点类型的异构图（图1c）：
*   **顶点节点**：承载位置、速度等物理状态，是输入输出边界。
*   **面片节点**：编码 2D 面片的面积、周长等几何特征，负责感知接触边界。
*   **单元节点**：编码 3D 单元的体积、表面积等几何特征，负责体积内物理量的传播与演化。

信息在这三层结构中的流动是双向且对称的：**编码阶段**将顶点物理量“聚合”至高维几何元素，使模型获得体积和边界感知能力；**解码阶段**则将处理后的单元/面片特征“分解”回顶点，以驱动下一时间步的变形预测。这种对称的聚合-分解机制使得高维几何特征与物理状态深度融合，是 MAVEN 在稀疏网格下保持数值稳定和几何保真度的结构基础。

### 与节点型方法的根本区别

传统的节点型方法（如 **MGN** (Pfaff et al., 2020)）仅基于顶点间欧氏距离构建接触边，在稀疏网格下会遗漏面片间的真实接触（图1b），且无法显式建模体积效应。MAVEN 通过引入面片节点和基于包围体层次（BVH）的面片-面片碰撞检测，实现了更精确的接触感知；通过引入单元节点和单元-面片二分图上的两阶段消息传递，建立了体积内物理量传播的专用通道。消融实验证实，当完全移除面片和单元结构（Model C）时，模型性能退化至传统节点型方法水平（Cavity Grasping 位置 RMSE 从 15.41 升至 17.08），验证了这一三层结构的必要性。

### 补充图表

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/004_Figure_2.jpg]]
*Figure 2: The overall structure of MAVEN. MAVEN follows an encoder–processor–decoder pipeline: it extracts geometric and physical features for vertices, cells, and facets, updates them through position-aware geometric aggregation and refined cell–facet message passing, and finally disaggregates the processed features back to vertices to produce smooth predictions*

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/002_Figure.jpg]]
*Figure: (a) Mesh division from original physical states. The purple region represents the fixed rigid body, while the blue region represents the deformable body subjected to clamping motion. (c) Mesh aware volumetric encoding based on 3D cells, 2D facets*

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/003_Figure_1.jpg]]
*Figure 1: The physical state on the continuous material domain is discretized using structured meshes. Node-based methods construct point-edge graphs from the mesh and apply GNNs for computation. However, such abstraction may overlook contact interactions. A more effective approach should incorporate higher-dimensional geometric structures in the mesh, such as 3D cells and 2D facets, which retain accurate geometric information after discretization*

## 核心模块与公式推导

### 3.1 图结构构建

MAVEN 的核心创新在于将传统节点型图网络（仅顶点+边）扩展为三层拓扑结构。给定一个由顶点集 $\mathcal{V}$、面片集 $\mathcal{F}$ 和单元集 $\mathcal{C}$ 组成的网格，模型显式地为每个几何元素建立独立的图节点，并构造以下边连接：

- **单元-面片边** $E_G$：每个 3D 单元与其所有组成面片之间的双向连接，形成二分图结构。
- **面片-面片边** $E_{FF}$：基于 Bounding Volume Hierarchy（BVH）检测的面片间接触关系，替代传统方法中基于顶点间欧氏距离的接触边。

这种设计的因果逻辑在于：面片作为 2D 几何元素，天然承载着接触边界信息；单元作为 3D 体积元素，编码了材料内部的物理状态。通过将接触检测提升到面片层级，模型能够更准确地识别边界交互，避免顶点级检测在粗网格下产生的漏检和误检。

### 3.2 编码器模块

编码器负责将原始物理量和几何属性映射到统一的潜在空间。

**顶点编码**：对每个顶点 $v_i$，将其关联的物理场量 $u_{v_i}^t$（如速度、应力等）通过标准 GNN 编码为高维特征：

$$\mathbf{h}_{v_i}^0 = \mathcal{A}^{\nu}(u_{v_i}^t)$$

**单元与面片编码**：这是 MAVEN 区别于传统方法的关键设计。单元节点编码其体积 $\Omega(c_i^t)$ 和总表面积 $\Sigma(c_i^t)$，面片节点编码其面积 $\alpha(f_i^t)$ 和周长 $\lambda(f_i^t)$。更重要的是，编码器同时输入这些几何量在初始时刻的值（$\Omega(c_i^0), \Sigma(c_i^0), \alpha(f_i^0), \lambda(f_i^0)$），使模型能够感知网格在变形过程中的几何变化：

$$\mathbf{h}_{c_i} = \mathcal{A}^{C}\big(\Omega(c_i^t), \Sigma(c_i^t), \Omega(c_i^0), \Sigma(c_i^0)\big)$$

$$\mathbf{h}_{f_i} = \mathcal{A}^{F}\big(\alpha(f_i^t), \lambda(f_i^t), \alpha(f_i^0), \lambda(f_i^0)\big)$$

消融实验（Table 2, Model B）证明，移除这些显式几何特征后，在稀疏 Metal Bending 数据集上位置误差从 810.42 暴增至 1652.31，应力误差从 4776.72 升至 6680.39，说明显式几何先验对粗网格下的精度至关重要。

**脚本化面片特征**：为增强面片对运动的感知，编码器将面片所有关联顶点的运动特征拼接后编码为脚本化特征：

$$\mathbf{h}_{f_i}^S = \mathcal{A}^S\big(\text{concat}_{v_j \in f_i}(\mathbf{h}_{v_i}^S)\big)$$

### 3.3 处理器模块

处理器由 $L$ 层堆叠，每层包含四个关键子模块。

**位置感知几何聚合器**：这是 MAVEN 的第二个核心创新。传统方法使用度数平均或注意力聚合顶点信息，忽略了网格的几何结构。MAVEN 为每个单元/面片构建局部坐标系，计算其与各组成顶点的相对位置向量 $\vec{\mathrm{d}}_{c_i, v}$，并通过 MLP 学习位置相关的聚合权重：

$$a_{c_i, v_0}, \ldots, a_{c_i, v_{K-1}} = \text{MLP}\Big(\text{concat}_{v \in \{v_0,\ldots,v_{K-1}\}}(\vec{\mathrm{d}}_{c_i, v})\Big)$$

这些权重在顶点间归一化后，用于将顶点特征加权聚合到高维元素。消融实验（Table 2, Model A）显示，用度数平均聚合替代位置感知聚合在稀疏 Cavity Grasping 数据集上性能显著下降，验证了位置敏感聚合的重要性。

**两阶段消息传递**：信息在单元-面片二分图上分两个阶段流动。

第一阶段，面片节点综合脚本化特征、面片间接触信息及相邻单元特征进行更新：

$$\mathbf{h}_{f_i}^{\mathcal{F}, l} = \mathcal{A}_l^{\mathcal{F}}\Big(\mathbf{h}_{f_i}^S, \mathbf{h}_{f_i}^{\mathcal{FF}, l}, \mathbf{h}_{f_i}^l, \sum_{(c_j, f_i) \in E_G} a_{f_i, c_j} \mathbf{h}_{c_j}^l\Big)$$

第二阶段，单元节点汇总所有关联面片的更新后特征：

$$\mathbf{h}_{c_i}^{\mathcal{C}, l} = \mathcal{A}_l^{\mathcal{C}}\Big(h_{c_i}^l, \sum_{(c_i, f_j) \in E_G} a_{c_i, f_j} h_{f_j}^{\mathcal{F}, l}\Big)$$

这种设计形成了“顶点→单元/面片→面片交互→单元汇总”的信息流，使接触边界信息通过面片层有效传递到体积内部。

**几何分解器**：与聚合器对称，将更新后的单元特征通过位置感知权重反投影回顶点：

$$\mathbf{h}_{v_i}^{\mathcal{V}, l} = \mathscr{A}_l^{\mathcal{V}}\Big(h_{v_i}^l, \sum_{v_i \in c_j} a_{v_i, c_j} h_{c_j}^{\mathcal{C}, l}\Big)$$

$$\mathbf{h}_{v_i}^{l+1} = \mathbf{h}_{v_i}^l + \mathbf{h}_{v_i}^{\mathcal{V}, l} + \text{FFN}(\mathbf{h}_{v_i}^l + \mathbf{h}_{v_i}^{\mathcal{V}, l})$$

### 3.4 解码器与损失函数

解码器将处理后的顶点特征 $\mathbf{h}_V^L$ 通过 MLP 解码为速度预测 $\hat{\dot{x}}^{t+1}$ 和物理量预测 $\hat{c}^{t+1}$，下一时刻位置通过一阶积分得到：

$$\hat{x}^{t+1} = \hat{\dot{x}}^{t+1} + x^t$$

训练采用一步均方误差损失，同时监督位置和物理量：

$$\mathcal{L} = \frac{1}{|\mathcal{V}|} \| x^{t+1} - \hat{x}^{t+1} \|^2 + \frac{1}{|\mathcal{V}|} \| c^{t+1} - \hat{c}^{t+1} \|^2$$

### 3.5 关键设计总结

MAVEN 的模块设计遵循一条清晰的因果链：**显式几何编码**提供粗网格下的几何先验 → **位置感知聚合**保留网格拓扑信息 → **面片级接触检测**提升边界交互精度 → **两阶段消息传递**实现接触-体积信息融合。消融实验（Table 2, Model C）表明，完全移除高维几何元素建模后，模型性能退化至传统节点型方法水平（Cavity Grasping 位置 RMSE 17.08 vs MAVEN 15.41），证明了面片-单元结构的必要性。

## 实验与分析

### 核心实验设置

实验覆盖三类数据集（Figure 3）：**Deforming Plate**（DP，来自 Pfaff et al., 2020，密集四面体网格）、**Cavity Grasping**（CG，来自 Linkerhägner et al., 2023，较粗网格）、以及新构建的 **Metal Bending**（MBD，弹塑性粗六面体网格，含大变形和长时接触）。所有模型在相近参数量（约 3.1M–3.85M，Table 3）和统一训练步数（1M 步）下训练，接触检测半径经调整使节点型方法与 MAVEN 检测到相近数量的接触边，确保比较公平。

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/015_Table_3.jpg]]
*Table 3: Key hyperparameters and parameter numbers of models*

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/006_Figure_3.jpg]]
*Figure 3: Visual description of the dataset*

### 主实验结果

Table 1（Rollout results）展示了各模型在全测试集上的滚动预测误差。MAVEN 在所有数据集上一致达到最优或接近最优性能。关键定量对比：

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/008_Table_1.jpg]]
*Table 1: Rollout results*

- **Cavity Grasping**：MAVEN 位置 RMSE 为 **15.41**，相比仅建模顶点-边图的 Model C（等效于传统节点型 GNN）的 17.08，降低约 9.8%（Table 2）。
- **Metal Bending**：MAVEN 位置 RMSE 为 **810.42**，Model C 为 1680.20，误差降低 **51.8%**（Table 2），表明高维几何元素在粗网格、弹塑性大变形场景下的增益尤为显著。
- **推理效率**：在 Metal Bending 数据集上，MAVEN 每步推理仅需 **23.57 ms**，相比传统 Abaqus 仿真器（712.44 ms/步）加速约 **2922.66%**，同时预测更准确（Table 5）。

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/018_Table_5.jpg]]
*Table 5: The inference time per step(ms) for each model on three dataset*

Figure 4 的误差图可视化进一步显示，MAVEN 在接触区域和大变形区域的误差分布明显低于对比方法，尤其在 Metal Bending 的弯曲接触区（Figure 10，灰色区域表示误差超上限）保持了更好的几何保真度。

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/010_Figure_4.jpg]]
*Figure 4: Visualization of error maps. The first and second rows respectively show sample visualizations from cavity grasping and metal bending datasets*

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/019_Figure_10.jpg]]
*Figure 10: Visualization of distance error map on Metal Bending dataset. Gray indicates that the error at this location exceeds the given error upper bound*

### 消融实验分析

Table 2 的消融实验揭示了 MAVEN 各组件的因果贡献：

1. **几何感知聚合器（Model A）**：将位置感知聚合替换为度数平均聚合后，在稀疏 CG 数据集上性能显著下降，验证了基于局部坐标系的聚合系数（Eq.6–Eq.7）对位置敏感信息编码的关键作用。

2. **显式几何特征（Model B）**：移除单元和面片的显式几何特征编码（体积、表面积、面积、周长及其初始值）后，MBD 数据集上位置误差暴增至 **1652.31**（MAVEN 810.42），应力误差升至 **6680.39**（MAVEN 4776.72）。这说明在粗网格条件下，显式几何先验对模型精度至关重要——模型难以从稀疏顶点分布中隐式推断体积和面积信息。

3. **高维几何元素建模（Model C）**：完全不建模面片和单元节点，退化为传统节点型 GNN 结构。CG 位置 RMSE 升至 17.08，MBD 升至 1680.20，性能退化至基线水平，直接证明了面片-单元二分图结构的必要性。

### 网格质量敏感性

分析指出 MAVEN 对初始网格质量敏感：在低质量网格（如从点云重建获得的网格）上性能显著下降。当前局部算子无法捕获长程相互作用，扩展层次化几何感知结构以支持长程依赖仍具挑战。此外，模型尚未适配薄壳、曲面几何或欧拉描述体系，这些方向留待后续工作探索。

### 推理效率对比

Table 5 展示了各模型在三数据集上的每步推理时间。MAVEN 在 DP、CG、MBD 上分别为 16.67 ms、9.14 ms、23.57 ms，处于合理水平，且显著快于传统仿真器（Abaqus 712.44 ms）。尽管 MAVEN 的图结构比节点型方法更复杂，但其推理时间仍保持在可接受范围内，验证了数据驱动替代模型在实际部署中的高效性。

### 补充图表

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/016_Table_4.jpg]]
*Table 4: Model input, output and contact detection parameters for dataset. S denotes stress, and P denotes PEEQ*

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/017_Figure_9.jpg]]
*Figure 9: Visualization of distance error map on Cavity Grasping*

![[assets/figures/papers/paper_list_l74_https_openreview_net_forum_id_XmULVr15E0/figures/013_Figure_7.jpg]]
*Figure 7: Description of Metal Bending*

## 方法谱系与知识库定位

### 从节点图到网格感知编码：方法演进脉络

传统基于图神经网络的物理模拟器将连续介质离散化为顶点-边图结构，代表性工作如 **MGN**（Pfaff et al., 2020）通过编码器-处理器-解码器管线在顶点图上执行消息传递，**GT**（Yun et al., 2019）引入图Transformer机制增强长程交互建模。这类方法的根本局限在于：网格中固有的2D面片和3D单元被完全丢弃，导致接触边界仅能通过顶点间欧氏距离近似检测，体积内场的应力-应变传播缺乏高维几何约束。

为弥补接触检测的不足，**FIGNet**（Allen et al., 2023）首次将面片显式引入图结构，通过面片-面片碰撞检测改善接触建模，但其消息传递仍局限于面片层面，缺少体积单元内的物理量传播机制。**HOOD**（Grigorev et al., 2023）和 **HCMT**（Yu et al., 2024）则从层次化图构建的角度出发，通过多尺度消息传递提升模拟精度，但它们同样未将3D单元作为独立的信息载体，高维几何特征（体积、表面积等）仅隐式地存在于顶点坐标中。

MAVEN的方法论定位在于**首次将顶点-面片-单元三层拓扑完整纳入统一的编码-传播-解码框架**。其核心创新不是简单地增加节点类型，而是设计了一套对称的几何聚合-分解机制：位置感知聚合器将顶点信息映射到单元和面片，两阶段消息传递在单元-面片二分图上实现接触力与体积内场的协同演化，几何分解器再将更新后的高维特征回传至顶点。这一设计使得MAVEN同时继承了FIGNet的面片接触优势、HOOD/HCMT的层次化思想，并填补了体积内传播机制的关键空白。

### 适用边界与约束条件

MAVEN的适用场景存在明确的边界约束：

**网格类型依赖**：模型假设输入为结构化网格（四面体或六面体），且需要明确的单元-面片-顶点拓扑关系。对于粒子系统、无网格方法或点云重建的低质量网格，当前架构无法直接适配。消融实验（Table 2）中Model C将单元和面片节点移除后退化为节点型方法，性能降至传统GNN水平（Cavity Grasping位置RMSE 17.08 vs MAVEN 15.41），从反面证明了网格质量对模型效能的决定性影响。

**局部算子限制**：几何聚合器和消息传递均基于局部邻域（单元与其组成面片、面片与其关联顶点），缺乏显式的长程相互作用机制。对于需要全局力平衡或远距离接触传播的场景，当前设计可能产生累积误差。

**物理模型适配范围**：论文验证集中于弹性（Deforming Plate）和弹塑性（Metal Bending）固体力学问题，尚未涉及薄壳结构、曲面几何、流体动力学或欧拉描述体系。损失函数（一步MSE）和滚动预测策略均基于拉格朗日网格更新，对拓扑变化（如断裂、融合）不具备内建支持。

### 局限性与开放问题

论文明确指出的局限包括三个方面，这些问题构成了该方向的后续研究空间：

1. **网格质量敏感性**：MAVEN对初始网格质量敏感，在低质量网格上性能显著下降。如何通过几何增强编码或自适应网格重划分策略降低这一敏感性，是提升模型鲁棒性的关键。

2. **长程依赖建模**：当前局部算子无法捕获长程相互作用。在单元-面片二分图上实现几何感知的层次化池化（类似HOOD的多尺度策略但保留高维几何特征），有望在不牺牲几何保真度的前提下扩展感受野。

3. **几何与物理范式扩展**：尚未适配薄壳、曲面几何或欧拉描述体系。将面片-单元编码思想推广至表面系统（如布料模拟）或固定网格下的欧拉仿真，需要重新定义几何元素类型及其聚合逻辑，这构成方法泛化的核心挑战。

此外，从实验证据的覆盖范围来看，Metal Bending数据集作为本文新提出的弹塑性弯曲任务，虽展示了MAVEN相对于Abaqus仿真器2922.66%的加速比（Table 5, 23.57ms vs 712.44ms），但该数据集的泛化基准尚不充分——缺少与FIGNet等面片方法在该任务上的直接比较，且材料参数（铝合金应力-应变曲线，Figure 8a）的单一性限制了结论的普适性。这一缺口值得在后续工作中通过多材料、多几何参数的基准测试加以填补。

## 原文 PDF

![[paperPDFs/ICLR_2026/MAVEN_A_Mesh_Aware_Volumetric_Encoding_Network_for_Simulating_3D_Flexible_Deform_cdb77aedb5f8.pdf]]