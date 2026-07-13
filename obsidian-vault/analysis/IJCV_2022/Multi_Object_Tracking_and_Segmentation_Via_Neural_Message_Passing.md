---
title: "Multi-Object Tracking and Segmentation Via Neural Message Passing"
type: paper
paper_level: A
venue: IJCV
year: 2022
pdf_ref: paperPDFs/IJCV_2022/Multi_Object_Tracking_and_Segmentation_Via_Neural_Message_Passing.pdf
project_link: null
code_link: https://github.com/ocetintas/MPNTrackSeg
aliases:
- MOTSNMP
tags:
- IJCV_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "将 MOT 的网络流图公式与神经消息传递网络（MPN）相结合，直接在图域中对边进行二分类以预测活跃连接，同时通过时间感知和注意力更新机制，将分割特征与关联特征融合为一个统一的端到端可微框架。"
primary_logic: "通过在图上进行时间感知的消息传递，模型能够分别聚合过去和未来的邻居信息，从而隐式地满足流守恒约束；而注意力消息传递则利用边特征来加权引导掩膜特征的更新，使跟踪和分割在训练中相互受益。"
claims:
- "时间感知的节点更新相比普通的 MPN 将 IDF1 提高了约三个点，并将流守恒约束的满足率从 83.2% 大幅提升至 98.8%。"
- "联合训练跟踪与分割带来了 +0.4 IDF1 和 +0.2 MOTA 的提升。"
- "基于注意力的掩膜更新优于简单的加性更新，在融合原始节点特征后 IDF1 进一步增加 1.1 个百分点，且大部分丢失（ML）降低 15%。"
- "在 MOTS20 测试集上建立了新的最佳水平，sMOTSA 达到 73.7，HOTA 达到 58.6，且身份切换（ID Switches）比最接近的方法减少了约 25%。"
---

# Multi-Object Tracking and Segmentation Via Neural Message Passing

> [!tip] 核心洞察
> 通过在图上进行时间感知的消息传递，模型能够分别聚合过去和未来的邻居信息，从而隐式地满足流守恒约束；而注意力消息传递则利用边特征来加权引导掩膜特征的更新，使跟踪和分割在训练中相互受益。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于神经消息传递的多目标跟踪与分割 |
| 英文题名 | Multi-Object Tracking and Segmentation Via Neural Message Passing |
| 会议/期刊 | IJCV 2022 |
| Links | [paper](https://arxiv.org/abs/2207.07454) · [GitHub](https://github.com/ocetintas/MPNTrackSeg) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | MPNTrackSeg |
| Dataset | KITTI tracking test set, MOTS20 test set, MOT17 validation (ablation) |

> [!tip] 效果简介
> - KITTI tracking test set 上，HOTA 为 -，对比 之前最佳方法，变化 +4.2。
> - MOTS20 test set 上，sMOTSA 为 73.7，对比 TrackR-CNN (70.2, 估计)，变化 +3.5。
> - MOT17 validation (ablation) 上，IDF1 为 70.0，对比 67.1 (Vanilla MPN)，变化 +2.9。

## 概要

多目标跟踪与分割（MOTS）要求同时估计视频中所有目标的轨迹及其像素级分割掩膜，是自动驾驶、行为分析等场景的核心感知任务。传统跟踪-检测范式中，数据关联与实例分割通常由独立模块分别处理：关联阶段先学习成对检测间的匹配成本，再依赖线性规划求解器（如最小成本流）获得最优划分；分割则由单独训练的模型完成。这种解耦设计导致两个关键瓶颈——**关联优化无法端到端地融入全局时序上下文**，且**跟踪与分割之间缺乏信息交互**，限制了关联精度和分割一致性。

本文提出的 **MPNTrackSeg** 方法，通过将 MOT 的经典网络流图公式与神经消息传递网络（MPN）深度融合，构建了一个**统一、端到端可微的跟踪与分割框架**。其核心洞察在于：在图域中直接对连接边进行二分类以预测活跃轨迹，同时引入**时间感知的消息传递**和**注意力引导的掩膜特征更新**，使模型能够在图上分别聚合过去与未来的邻居信息，隐式地满足流守恒约束，并利用边特征加权引导分割特征的演化，实现跟踪与分割的相互受益。

实验层面，MPNTrackSeg 在八个公开的 MOT 和 MOTS 基准上达到了当时的最佳水平。其中，在 **MOTS20 测试集**上，sMOTSA 达到 73.7，HOTA 达到 58.6，身份切换（ID Switches）较此前最优方法减少约 25%；在 **KITTI 跟踪测试集**上，HOTA 较此前最佳结果提升 4.2 个百分点。消融研究进一步证实：时间感知节点更新使流守恒约束满足率从 83.2% 跃升至 98.8%，IDF1 提高约三个点；联合训练跟踪与分割带来了额外的 IDF1 和 MOTA 提升；注意力消息传递相较于简单加性更新，在融合原始节点特征后 IDF1 进一步提高 1.1 个百分点，且大部分丢失（ML）降低 15%。

该方法仍存在对检测质量高度敏感、极端拥挤场景下图密度增加导致计算负担上升、以及离线处理范式不适用于实时在线场景等局限。后续章节将依次展开问题形式化、方法设计、实验验证与局限性讨论。

多目标跟踪（Multi-Object Tracking, MOT）旨在从视频序列中定位所有感兴趣目标并恢复其完整轨迹，而多目标跟踪与分割（Multi-Object Tracking and Segmentation, MOTS）进一步要求为每个目标输出像素级的实例分割掩膜。这两个任务在自动驾驶、视频监控和行为分析等应用中具有核心地位。

在传统的跟踪-检测（Tracking-by-Detection）范式中，MOT 通常被建模为一个基于图的数据关联问题：节点表示各帧中的检测，边表示跨帧检测之间的可能连接，目标是从图中选出一组边以形成轨迹。这一经典框架自 **Min-Cost Flow**（L. Zhang et al., CVPR 2008）以来被广泛采用，其求解流程通常分为两步：先学习成对的关联成本，再通过线性规划或最小成本流求解器获得全局最优的轨迹划分。

然而，这种两阶段范式存在一个根本性的瓶颈：**数据关联的成本学习与最终的图划分求解是解耦的，无法在全局上下文中进行端到端的联合优化**。具体而言，成本学习阶段只关注局部的成对相似度，而求解器在推理时才引入流守恒等全局约束，导致学习目标与最终优化目标之间存在不一致。此外，在 MOTS 场景中，分割和跟踪通常由独立的模块处理，两类任务之间缺乏有效的信息交互——分割特征无法辅助关联决策，跟踪的时序信息也无法指导分割质量的提升。这使得关联准确率受限，尤其是在密集遮挡和身份切换频繁的复杂场景中。

针对上述问题，本文提出了一种基于神经消息传递（Message Passing Networks, MPN）的统一框架，其核心动机在于：**将 MOT 的网络流图公式与可微的消息传递网络深度融合，使模型能够直接在图上学习预测哪些边属于活跃轨迹，同时通过时间感知和注意力机制实现跟踪与分割特征的协同更新**。这一设计使得整个框架端到端可微，特征学习与最终的任务目标（边分类与掩膜预测）在训练中保持一致，从而突破了传统两阶段方法的优化瓶颈。

## 核心方法与创新机理

本工作将多目标跟踪与分割（MOTS）重新建模为一个**端到端可微的图分类问题**，其核心创新在于三个相互耦合的“changed slots”，分别针对数据关联的求解范式、节点更新的时间结构建模以及跟踪与分割的信息交互方式。

### 从“先学习代价再求解”到“直接学习边分类”

传统基于网络流的跟踪方法（如 **Min-Cost Flow with Learned Costs**，L. Zhang et al., CVPR 2008）遵循两阶段范式：先训练一个网络学习成对的关联代价，再将该代价送入最小成本流线性规划求解器，以获得满足流守恒约束的最优划分。这一范式的根本瓶颈在于**特征学习与最终决策目标之间缺乏端到端的梯度通路**——代价函数并非直接面向轨迹划分的准确性进行优化，且线性规划求解器本身不可微，阻断了误差信号从最终关联结果向特征提取器的反向传播。

本工作提出的 **MPNTrackSeg** 直接摒弃了这一分离式设计。方法将 MOT 的网络流图形式化定义为一个图 $G=(V,E)$，其中节点代表检测，边连接不同帧的检测，并引入二元变量 $y_{(i,j)}$ 表示边 $(i,j)$ 是否属于某条轨迹。与经典方法使用线性规划求解器推断 $y$ 不同，MPNTrackSeg **通过消息传递网络直接对每条边进行二分类，预测其“活跃”概率**。在推理阶段，仅需对分类分数进行阈值化，并可选地求解一个线性规划以保证流守恒约束的严格满足。这一转变使整个关联过程成为可端到端训练的前向传播，特征提取、消息传递和关联决策共享同一优化目标。

### 时间感知的节点更新：将流守恒约束隐式编码进网络结构

普通消息传递网络（Vanilla MPN）在聚合邻居信息时，对所有邻居节点执行无差别的求和或平均操作。这种无序聚合完全忽略了 MOT 问题中**时间箭头**所蕴含的强结构先验：每个检测节点最多只能有一条来自过去帧的进入边和一条去往未来帧的外出边（流守恒约束）。

本工作提出了**时间感知的节点更新**策略，将邻居集合按时间属性显式拆分为过去邻居 $N_i^{\text{past}}$ 和未来邻居 $N_i^{\text{fut}}$，并分别用两个独立的 MLP（$\mathcal{N}_v^{\text{past}}$ 和 $\mathcal{N}_v^{\text{fut}}$）计算消息：

$$m_{(i,j)}^{(l)} = \begin{cases} \mathcal{N}_v^{\text{past}} \left( [h_i^{(l-1)}, h_{(i,j)}^{(l)}, h_{(i)}^{(0)}] \right) & \text{if } j \in N_i^{\text{past}} \\ \mathcal{N}_v^{\text{fut}} \left( [h_i^{(l-1)}, h_{(i,j)}^{(l)}, h_{(i)}^{(0)}] \right) & \text{if } j \in N_i^{\text{fut}} \end{cases}$$

随后，分别聚合过去和未来的消息得到 $h_{i,\text{past}}^{(l)}$ 和 $h_{i,\text{fut}}^{(l)}$，拼接后经一个 MLP 得到最终节点嵌入：

$$h_i^{(l)} = \mathcal{N}_v ( [h_{i,\text{past}}^{(l)}, h_{i,\text{fut}}^{(l)}] )$$

这一设计的深层洞察在于：**通过结构化的消息传递，网络隐式地学习到流守恒约束所要求的行为模式**。消融实验（Table 1）提供了强有力的因果证据：时间感知更新将流守恒约束的满足率从 Vanilla MPN 的 83.2% 大幅提升至 98.8%，同时 IDF1 提高了约 2.9 个百分点（67.1 → 70.0）。这表明，将领域知识以网络结构的形式注入，比依赖后处理求解器来强制约束更加有效。

### 注意力消息传递：以关联特征引导分割特征更新

在传统的跟踪-分割范式中，跟踪和分割通常由独立模块处理，二者之间缺乏信息交互。本工作引入了**注意力消息传递**机制，使关联信息能够直接引导分割特征的更新，实现两个任务的协同优化。

具体而言，边嵌入 $h_{(i,j)}^{(l-1)}$ 中编码了两个节点之间的时序关联强度。方法通过一个可学习函数 $\mathcal{N}_e^w$ 从边嵌入预测未归一化的注意力权重 $w_{(i,j)}^{(l)}$，并在过去（或未来）邻居内分别进行 softmax 归一化，得到注意力系数 $a_{(i,j)}^{(l)}$。这些注意力系数随后被用于加权聚合邻居的掩膜特征，形成上下文向量 $c_{i,\text{past}}^{(l)}$ 和 $c_{i,\text{fut}}^{(l)}$，最终更新节点的掩膜嵌入：

$$\tilde{h}_i^{(l)} = \tilde{\mathcal{N}}_v ( [c_{i,\text{past}}^{(l)}, c_{i,\text{fut}}^{(l)}, \tilde{h}_{(i)}^{(0)}] )$$

这一机制的核心价值在于：**关联置信度高的邻居对掩膜特征更新贡献更大，使得分割模型在训练中能够从更可靠的时序对应中受益**；反之，更精确的分割特征也能为关联提供更强的外观线索。消融实验（Table 3）证实，注意力消息传递优于简单的加性更新，在融合原始节点特征后 IDF1 进一步提升 1.1 个百分点，且大部分丢失（ML）降低 15%。联合训练跟踪与分割（Table 4）相比仅训练跟踪带来了 +0.4 IDF1 和 +0.2 MOTA 的提升，验证了双向信息交互的增益。

### 创新点的协同效应

上述三个 changed slots 并非孤立的技术改进，而是构成了一个紧密耦合的创新体系：**直接边分类**使整个框架可端到端优化；**时间感知更新**为图网络注入了 MOT 必需的时序结构先验，使边分类器能够在不依赖外部求解器的情况下隐式满足流守恒约束；**注意力消息传递**则在统一的图域中打通了跟踪与分割的信息壁垒，使两个任务在训练中相互受益。三者共同作用，使 MPNTrackSeg 在 MOTS20 测试集上建立了新的最佳水平（sMOTSA 73.7，HOTA 58.6），身份切换（ID Switches）比最接近的方法减少了约 25%（Table 9）。

MPNTrackSeg 的整体框架将多目标跟踪与分割统一为一个端到端可微的图神经网络推理过程。如图 1 所示，系统接收一组连续的图像帧及其对应的检测结果作为输入，随后经历图构建、特征编码、神经消息传递、边分类与掩膜预测、以及推理舍入五个阶段。

**图构建**阶段将跟踪问题显式地建模为一张无向图 $G = (V, E)$。图中每个节点 $i \in V$ 代表一个唯一的检测 $o_i = (a_i, p_i, t_i)$，其中 $a_i$ 为原始像素区域，$p_i$ 为二维图像坐标，$t_i$ 为时间戳。边则连接来自不同帧的任意两个检测，从而形成一个稠密的候选关联图。这一建模直接继承了经典最小成本流公式中对 MOT 的网络流图表述（L. Zhang et al., CVPR 2008），但其核心差异在于后续的求解方式：传统方法在此图上学习成对成本，再调用线性规划求解器（如 k-shortest paths）获得最优划分；而 MPNTrackSeg 则通过消息传递网络直接对每条边进行二分类，预测其属于某条轨迹的活跃变量 $y_{(i,j)}$，从而将关联决策内化于可微学习过程中。

**特征编码**模块为图中的节点和边赋予初始嵌入。节点嵌入由两部分组成：一是通过 CNN 从检测区域提取的外观特征，用于数据关联；二是同样由 CNN 提取的掩膜特征，用于后续的分割预测。边嵌入则通过 MLP 编码两个检测之间的相对几何关系，包括相对位置、边界框尺寸比以及时间差等，同时辅以两个节点外观特征之间的欧氏距离。这些编码构成了消息传递的初始状态。

**神经消息传递**是框架的核心计算引擎，分为两个并行的更新流。第一个流是时间感知的边-节点消息传递：在每一轮迭代中，首先由节点嵌入更新边嵌入（节点到边），随后根据邻居节点的时间属性（过去或未来）分别计算消息，并分别聚合后拼接，经 MLP 得到更新后的节点嵌入。这一设计使得模型隐式地学习流守恒约束——每个节点最多有一条来自过去的入边和一条去往未来的出边。第二个流是注意力消息传递：利用边嵌入生成注意力系数，对掩膜特征进行加权更新，使分割特征的演化受关联信息的引导。两个更新流共享边嵌入，实现了跟踪与分割之间的信息交互。

**边分类与掩膜预测**阶段利用消息传递后的最终嵌入产生输出。最终的边嵌入经过一个分类头，输出每条边活跃与否的概率；最终的节点嵌入则结合其原始掩膜特征（通过跳跃连接），经 CNN 预测该检测对应的实例分割掩膜。

**推理舍入**阶段将软分类结果转化为硬性轨迹。模型首先对边分类概率进行阈值二值化，必要时再求解一个小规模的线性规划以确保流守恒约束的严格满足，从而得到最终的目标轨迹及其对应的逐帧分割掩膜。

整个框架以多任务损失 $L = L_t + L_s$ 进行端到端训练，其中 $L_t$ 为边分类的加权交叉熵损失，$L_s$ 为分割掩膜的平均交叉熵损失。这种联合训练使得关联特征和分割特征在消息传递过程中相互增强，是该方法在 MOTS 基准上取得领先性能的关键设计。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2207_07454/figures/001_Figure_1.jpg]]
*Figure 1: (e) Output Fig. 1: Overview of our method. (a) We receive as input a set of frames and detections. (b) We construct a graph in which nodes represent detections, and all nodes at different frames are connected by an edge. (c) We initialize node embeddings in the graph with two CNNs that encode appearance and mask features. Edge embeddings are initialized with an MLP encoding geometry information (not shown in the figure). (c) The information contained in these embeddings is propagated across the graph for a fixed number of iterations through neural message passing. (d) Once this process terminates, the embeddings resulting from neural message passing are used to predict masks and classify ed...*

### 图构建与变量定义

MPNTrackSeg 将多目标跟踪与分割建模为无向图 $G = (V, E)$ 上的边分类问题。每个检测 $o_i = (a_i, p_i, t_i)$ 对应一个节点 $i \in V$，其中 $a_i$ 为原始像素区域，$p_i$ 为二维图像坐标，$t_i$ 为时间戳。不同帧的节点之间均建立边连接，构成全连接的时间图结构。

轨迹被定义为时间有序的活跃边路径。对于每条边 $(i, j)$，引入二元变量指示其是否属于某条真实轨迹：

$$y _ { ( i , j ) } : = \left\{ { \begin{array} { l l } { 1 } & { \exists T _ { k } \in { \mathcal { T } } _ { * } { \mathrm { ~ s . t . ~ } } ( i , j ) \in T _ { k } } \\ { 0 } & { { \mathrm { o t h e r w i s e . } } } \end{array} } \right.$$

每个节点需满足流守恒约束——最多有一条来自过去的进入边和一条去往未来的外出边：

$$\sum _ { ( j , i ) \in E { \mathrm { ~ s . t . ~ } } t _ { i } > t _ { j } } y _ { ( j , i ) } \leq 1$$

$$\sum _ { ( i , k ) \in E { \mathrm { ~ s . t . ~ } } t _ { i } < t _ { k } } y _ { ( i , k ) } \leq 1$$

### 特征编码

每条边 $(i, j)$ 的初始特征由三部分组成：时间差、相对几何特征和外观距离。相对几何特征编码了两个检测框之间的空间关系：

$$\left( \frac{2(x_j - x_i)}{h_i + h_j}, \frac{2(y_j - y_i)}{h_i + h_j}, \log \frac{h_i}{h_j}, \log \frac{w_i}{w_j} \right)$$

这些手工特征与 CNN 提取的外观嵌入的欧氏距离拼接后，经 MLP 编码为初始边嵌入。节点嵌入则初始化为 CNN 提取的外观特征和掩膜特征的组合。

### 神经消息传递

消息传递分为两个交替执行的步骤：节点到边更新和边到节点更新。

**节点到边更新**将边嵌入更新为两端节点嵌入与上一步边嵌入的函数：

$$h_{(i,j)}^{(l)} = \mathcal{N}_e \left( [h_i^{(l-1)}, h_j^{(l-1)}, h_{(i,j)}^{(l-1)}] \right)$$

**时间感知的边到节点更新**是方法的核心创新。与普通 MPN 对全部邻居的无序聚合不同，MPNTrackSeg 将邻居按时间方向分为过去邻居集 $N_i^{past}$ 和未来邻居集 $N_i^{fut}$，分别用专用 MLP 计算消息：

$$m_{(i,j)}^{(l)} = \begin{cases} \mathcal{N}_v^{past} \left( [h_i^{(l-1)}, h_{(i,j)}^{(l)}, h_{(i)}^{(0)}] \right) & \text{if } j \in N_i^{past} \\ \mathcal{N}_v^{fut} \left( [h_i^{(l-1)}, h_{(i,j)}^{(l)}, h_{(i)}^{(0)}] \right) & \text{if } j \in N_i^{fut} \end{cases}$$

这里引入了初始节点嵌入 $h_{(i)}^{(0)}$ 作为跳跃连接。随后分别对过去和未来的消息进行聚合，拼接后送入最终 MLP 得到更新后的节点嵌入：

$$h_i^{(l)} = \mathcal{N}_v ( [h_{i,past}^{(l)}, h_{i,fut}^{(l)}] )$$

这种时间感知的设计使模型能够隐式学习流守恒约束——过去和未来的信息流被分别编码，节点自然地“知道”它最多应连接一个过去检测和一个未来检测。

### 注意力消息传递与掩膜更新

为了将分割特征与关联特征融合，MPNTrackSeg 引入注意力消息传递机制。边嵌入被用于生成注意力系数，引导掩膜特征的更新。首先从边嵌入预测未归一化的注意力权重：

$$w_{(i,j)}^{(l)} = \mathcal{N}_e^w \left( h_{(i,j)}^{(l-1)} \right)$$

然后对过去（或未来）邻居的权重分别进行 softmax 归一化：

$$a_{(i,j)}^{(l)} = \frac{\exp(w_{(i,j)}^{(l)})}{\sum_{k \in N_i^{past}} \exp(w_{(i,k)}^{(l)})} \text{ if } j \in N_i^{past}$$

利用这些注意力系数对邻居的掩膜特征加权聚合，得到过去和未来的上下文向量，再与初始掩膜特征拼接后经 CNN 更新：

$$\tilde{h}_i^{(l)} = \tilde{\mathcal{N}}_v ( [c_{i,past}^{(l)}, c_{i,fut}^{(l)}, \tilde{h}_{(i)}^{(0)}] )$$

### 输出与损失函数

经过 $L$ 步消息传递后，最终的边嵌入 $h_{(i,j)}^{(L)}$ 通过分类头预测该边活跃的概率。最终的节点嵌入用于预测每个目标的实例分割掩膜，同样引入跳跃连接：

$$mask_i = \tilde{\mathcal{N}}_v^{mask} ( [\tilde{h}_{(i)}^{(L)}, \tilde{h}_{(i)}^{(0)}] )$$

总损失为跟踪损失与分割损失之和：

$$L = L_t + L_s$$

其中 $L_t$ 为边分类的加权交叉熵损失，$L_s$ 为分割掩膜的平均交叉熵损失。推理时对边分类概率进行阈值二值化，必要时运行线性规划以保证流守恒约束的严格满足。

## 实验与关键发现

### 瓶颈验证与消融实验

本节通过一系列受控消融实验，系统验证了 MPNTrackSeg 各核心组件对性能的贡献及其背后的因果机制。所有消融实验均在 MOT17 验证集上进行，使用统一的检测结果与主干网络，确保对比的公平性。

**时间感知节点更新**是方法的核心创新之一。Table 1 的结果显示，将普通的 MPN（Vanilla MPN）替换为时间感知更新后，IDF1 从 67.1 提升至 70.0（+2.9 个百分点），同时流守恒约束的满足率（Constr）从 83.2% 大幅提升至 98.8%。这一结果直接证明了时间感知聚合机制能够通过分别编码过去与未来的邻居信息，隐式地学习到流守恒约束，从而在不依赖显式后处理求解器的情况下，大幅减少图划分中的非法连接。Figure 2 直观展示了这一差异：普通 MPN 对所有邻居进行无序聚合，而时间感知更新将邻居按时间方向分为过去和未来两组，分别用专用 MLP 计算消息后再拼接融合。

**边特征组合**的实验（Table 2）揭示了不同信息源对数据关联的贡献权重。仅使用时间差特征的模型 IDF1 仅为 42.8，加入相对位置特征后跃升至 67.6，再加入 CNN 外观距离特征后达到最佳 IDF1 70.0 和 MOTA 64.0。这表明相对位置特征是数据关联的最强单一信号，而外观特征提供了互补的判别力。

**注意力消息传递**机制在 Table 3 中得到了充分验证。与简单的加性更新（Add.）相比，基于注意力的掩膜特征更新（Att.）在融合原始节点特征（Raw + Upd.）后，IDF1 进一步提升 1.1 个百分点，同时大部分丢失（ML）降低了 15%。这证实了边嵌入中编码的时间关联信息能够有效引导掩膜特征的更新，使分割与跟踪在训练中相互受益。Figure 3 示意了该机制：边特征通过可学习函数生成注意力系数，经 softmax 归一化后对历史邻居的掩膜特征进行加权聚合。

**联合训练**的收益在 Table 4 中得到量化：相比仅训练跟踪的 MPNTrack，联合训练跟踪与分割的 MPNTrackSeg 带来了 +0.4 IDF1 和 +0.2 MOTA 的提升。这表明分割任务提供的掩膜特征学习有助于增强节点的表示能力，进而改善关联质量。

**消息传递步数**的影响如 Figure 5 所示。随着步数从 1 增加到 4，IDF1 和 MOTA 持续提升，但超过 4 步后性能趋于饱和甚至略有下降。这表明适度的迭代消息传递足以在图上传播足够的上下文信息，过深的传递可能引入噪声。

### 主要基准测试结果

MPNTrackSeg 在多个公开基准上建立了新的最佳水平，具体结果如下：

**MOTChallenge 测试集**（Table 5）：在 MOT17 上，MPNTrack 取得了 58.8 MOTA 和 61.7 IDF1 的成绩，在当年提交的方法中表现突出。值得注意的是，使用 Tracktor 预处理检测框后，性能进一步提升。

**KITTI 跟踪测试集**（Table 6）：MPNTrackSeg 在 HOTA 指标上达到领先水平，相比之前的最佳方法提升了 +4.2 个百分点，体现了该方法在自动驾驶场景下的强泛化能力。

**MOTS20 测试集**（Table 9）：MPNTrackSeg 取得了 sMOTSA 73.7 和 HOTA 58.6 的成绩，建立了新的 state-of-the-art。与当时最接近的方法 TrackR-CNN（sMOTSA 约 70.2）相比，提升了约 3.5 个百分点，且身份切换（ID Switches）减少了约 25%。这直接验证了统一的图消息传递框架在多目标跟踪与分割联合任务上的显著优势。

**HiEve 数据集**（Table 7）：在人体事件理解这一更具挑战性的场景中，MPNTrackSeg 同样取得了领先结果，进一步证明了方法的鲁棒性。

### 失败模式与局限性

尽管 MPNTrackSeg 在多个基准上表现优异，但分析揭示了以下关键局限：

1. **对检测质量的高度敏感性**：该方法为纯图关联方法，不涉及检测框的回归或修正，因此 MOTA 的上限直接受限于输入检测的质量。在检测召回率较低的场景中，漏检将直接导致轨迹断裂。

2. **极端拥挤场景的计算负担**：在 MOT20 等行人密度极高的序列中，图的边密度显著增加，尽管采用了互近邻剪枝策略，消息传递的计算开销仍会上升。Figure 4 的运行时分析表明，处理速度随每帧平均检测数增加而下降。

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2207_07454/figures/003_Figure.jpg]]
*Figure: (b) Graph Construction + Feature Encoding (c) Neural Message Passing*

3. **离线处理范式**：该方法需要构建跨多帧的图结构，属于离线跟踪方法，不适用于需要逐帧实时输出的在线跟踪场景。

4. **分割与跟踪的耦合限制**：分割模块仅在 MPNTrackSeg 联合训练时使用，MPNTrack 本身并未利用掩膜信息。这意味着当仅需跟踪而不需分割时，模型无法从掩膜特征中获益，性能可能受限于外观和几何特征。

### 开放问题

1. 如何将基于图的消息传递与基于回归的跟踪器（如 CenterTrack）相结合，以同时提升关联精度和检测召回？
2. 注意力消息传递在复杂的密集遮挡场景中能否稳定地聚焦于正确的历史邻居？
3. 时间感知图方法能否直接扩展到 3D 多目标跟踪，并保持对时间结构的高效编码？
4. 对于跨长时间跨度的轨迹恢复，是否存在最优的消息传递步数上限，以及如何适应不同序列特性？

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2207_07454/figures/005_Figure_2.jpg]]
*Figure 2: Visualization of node updates during message passing. Arrow directions in edges show time direction. Note the time division in t − 1, t, and t + 1. In this case, we have N _ { 3 } ^ { p a s t } = \{ 1 , 2 \} and N _ { 3 } ^ { f u t } = \{ 4 , 5 \} . 2a shows the starting point after an edge update has been performed (equation 3), and the intermediate node update embeddings (equation 4) have been computed. 2b shows the standard node update in vanilla MPNs, in which all neighbors’ embeddings are aggregated jointly. 2c shows our proposed update, in which embeddings from past and future frames are aggregated separately, then concatenated and fed into an MLP to obtain the new node embedding*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2207_07454/figures/008_Table_1.jpg]]
*Table 1: We investigate how our proposed update improves tracking performance with respect to a vanilla MPN. Vanilla stands for a basic MPN, T. aware denotes our proposed time-aware update. The metric Constr refers to the percentage of flow conservation constraints satisfied on average over entire validation sequences*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2207_07454/figures/014_Table_5.jpg]]
*Table 5: Comparison of our method with state-of-the art on the MOTChallenge test sets. Methods written in grey were published after our CVPR2020 work. Methods with † after their name also used Tracktor-based preprocessing on their input boxes*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2207_07454/figures/015_Table_6.jpg]]
*Table 6: Comparison of our method with state-of-the-art on KITTI-tracking test set. Methods written in grey were published after our CVPR2020 work. Table 7: Comparison of our method with state-of-the-art on the Human in Events test dataset. Methods written in grey were published after our CVPR2020 work*

## 定位与知识库关联

### 1. 与基线方法的关系

#### 1.1 对经典图关联范式的继承与颠覆

MPNTrackSeg 的问题建模直接继承自经典的基于网络流的最小成本流（Min-Cost Flow）MOT 范式（**L. Zhang et al., CVPR 2008**）。该范式将多目标跟踪抽象为图上的最小成本流问题：节点表示检测，边表示帧间关联候选，通过求解线性规划得到全局最优的轨迹划分。MPNTrackSeg 保留了这一图结构建模的核心思想——包括流守恒约束（每个节点最多一条入边和一条出边）——但对其求解方式进行了根本性颠覆。

传统流程分为两个解耦阶段：先学习成对关联成本，再调用线性规划求解器（如 k-shortest paths）求最优划分。这种两阶段设计存在一个本质性瓶颈：特征学习与全局优化相互独立，关联成本的学习无法直接感知最终的轨迹级目标，导致端到端优化信号断裂。MPNTrackSeg 的核心改造在于将求解器本身替换为可微的消息传递网络：**直接在图域中对边进行二分类以预测活跃连接**（Section 3.3），从而将整个数据关联过程内化为神经网络的前向传播。推理阶段仅需对分类概率进行阈值二值化，必要时辅以线性规划保证约束满足（Section 4.6），但不再依赖求解器进行核心决策。

这一转变的因果机制在于：消息传递的多步迭代天然具备在图上传播上下文信息的能力，使得每条边的分类决策能够感知全局图结构，而非仅依赖局部的成对相似度。

#### 1.2 与普通消息传递网络（Vanilla MPN）的差异

Vanilla MPN 作为直接基线，使用标准的节点-边交替更新（公式 3-5），但对所有邻居节点进行无序聚合（求和或平均）。MPNTrackSeg 在此基础上引入了两个关键改进：

- **时间感知节点更新**：将邻居按时间方向分为过去（$N_i^{past}$）和未来（$N_i^{fut}$）两组，分别用专用 MLP（$\mathcal{N}_v^{past}$ 和 $\mathcal{N}_v^{fut}$）计算消息并聚合，再拼接后经最终 MLP 得到新节点嵌入（公式 6-9）。这一设计隐式编码了流守恒的方向性约束，使模型能够区分“来自过去的连接”和“去往未来的连接”，从而天然抑制违反时间因果性的边激活。

- **注意力消息传递**：在分割分支中，利用边嵌入生成注意力系数（公式 10-11），对掩膜特征的更新进行加权引导（公式 12-14）。这使得分割特征能够选择性聚合来自相关历史/未来节点的信息，而非对所有邻居一视同仁。

消融实验（Table 1）提供了强因果证据：时间感知更新将 IDF1 从 67.1 提升至 70.0（+2.9），同时将流守恒约束的满足率从 83.2% 大幅提升至 98.8%。这表明时间感知机制不仅改善了数值指标，更在结构层面使模型内化了物理约束。注意力消息传递相较于简单的加性更新，在融合原始节点特征后进一步将 IDF1 提升 1.1 个百分点，且大部分丢失（ML）降低 15%（Table 3）。

#### 1.3 与 TrackR-CNN 等联合方法的对比定位

在 MOTS（多目标跟踪与分割）任务中，TrackR-CNN 等前期工作通常将跟踪和分割作为两个松耦合模块处理：分割由 Mask R-CNN 独立完成，跟踪则基于分割结果进行关联。MPNTrackSeg 的关键突破在于**将分割特征与关联特征融合为统一的端到端可微框架**：通过注意力消息传递，边嵌入（编码关联信息）直接引导掩膜特征的更新（Figure 3），使得两个任务在训练中相互受益。联合训练的因果效应在 Table 4 中得到验证：相较于仅训练跟踪的 MPNTrack，联合训练的 MPNTrackSeg 带来了 +0.4 IDF1 和 +0.2 MOTA 的提升。

### 2. 适用边界

#### 2.1 检测依赖性

MPNTrackSeg 是纯图关联方法，其性能高度依赖前端检测器的质量。方法本身不修改或补充检测结果，较差的检测召回或定位精度会直接限制 MOTA 的上限。在 MOTChallenge 和 HiEve 基准上，论文使用官方提供的相同检测结果以保证公平比较；在 MOTS20 和 KITTI 上则使用 Mask R-CNN（ResNeXt-152 主干）并辅以 Tracktor（**Bergmann et al., ICCV 2019**）对检测框进行预处理。

#### 2.2 离线处理范式

该方法构建的图跨越多帧（通常为整个序列或滑动窗口），消息传递需要在完整图结构上进行多步迭代，因此属于离线处理范式。这使其不适用于需要逐帧实时响应的在线跟踪场景。Figure 4 报告了不同行人密度下的处理速度，但未给出在线场景的适配方案。

#### 2.3 密集场景的计算负担

在极端拥挤场景（如 MOT20）下，检测数量增加导致图密度上升，尽管已通过互近邻剪枝策略缓解，计算负担仍然显著。消息传递步数与图规模呈超线性关系，需要在精度和效率之间权衡（Figure 5 显示步数增加带来的边际收益递减）。

### 3. 局限与开放问题

#### 3.1 已知局限

1. **检测质量敏感**：如 2.1 所述，方法不具备检测修正能力，漏检和误检会直接传播到关联结果。
2. **分割模块仅在联合训练时激活**：MPNTrack（纯跟踪版本）未利用掩膜信息，其性能可能受限于外观和几何特征的表征能力。
3. **离线批处理限制**：无法直接迁移至在线场景，需要引入滑动窗口或增量图更新机制。
4. **长跨度轨迹恢复**：消息传递步数决定了信息在图中的传播半径，对于跨长时间跨度的轨迹断裂恢复，存在理论上的感受野上限。

#### 3.2 开放问题

1. **与基于回归的跟踪器融合**：如何将图消息传递的关联能力与 CenterTrack 等基于回归的跟踪器相结合，以同时提升关联精度和检测召回？这需要解决图结构推理与密集预测之间的架构兼容性问题。

2. **注意力机制的鲁棒性**：在密集遮挡场景中，注意力消息传递能否稳定地聚焦于正确的历史邻居？当多个候选邻居外观高度相似时，边嵌入的判别力可能下降，导致注意力权重分散。

3. **向 3D 多目标跟踪的扩展**：时间感知图方法能否直接扩展到 3D MOT，并保持对时间结构的高效编码？3D 场景中空间关系的表示和边特征的构建需要重新设计。

4. **自适应消息传递步数**：对于不同序列特性（如帧率、目标运动速度），是否存在最优的消息传递步数上限，以及如何自适应地确定这一参数？Figure 5 显示步数超过一定阈值后性能趋于饱和，但该阈值的跨场景泛化性尚未被系统研究。

5. **流守恒约束的软硬结合**：当前方法在训练中通过时间感知更新隐式学习约束，推理时通过后处理线性规划强制满足。是否存在更优雅的方式将硬约束完全融入网络结构，实现严格满足约束的端到端推理？

## 原文 PDF

![[paperPDFs/IJCV_2022/Multi_Object_Tracking_and_Segmentation_Via_Neural_Message_Passing.pdf]]
