---
title: "PolarMOT: How far can geometric relations take us in 3D multi-object tracking?"
type: paper
paper_level: A
venue: ECCV
year: 2022
pdf_ref: paperPDFs/ECCV_2022/PolarMOT_How_far_can_geometric_relations_take_us_in_3D_multi_object_tracking.pdf
project_link: https://github.com/aleksandrkim61/PolarMOT
aliases:
- PolarMOT
tags:
- ECCV_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "采用局部极坐标（localized polar coordinates）编码成对几何关系，该表示具有全局变换不变性，并内嵌非完整运动先验，是提升跟踪精度和跨场景泛化能力的关键操作性变量。"
primary_logic: "仅基于3D包围盒的几何关系，通过稀疏多路复用图神经网络和局部极坐标编码，即可实现高性能且强泛化的多目标跟踪，证明了几何线索在数据驱动MOT中的巨大潜力。"
claims:
- "在nuScenes测试集上，PolarMOT以66.4 AMOTA超越所有仅用3D输入的方法，达到新的最佳水平。"
- "消融实验表明，将边特征从全局笛卡尔坐标替换为时间归一化的局部极坐标，在mini训练集上AMOTA提升+17.55（57.96 vs 40.41）。"
- "添加帧内空间边可带来+1.05 AMOTA和+2.4%召回率的提升。"
- "跨城市泛化实验：Boston训练→Singapore评估，PolarMOT达到63.12 AMOTA，远超CenterPoint的59.71，验证了几何方法的泛化优势。"
---

# PolarMOT: How far can geometric relations take us in 3D multi-object tracking?

> [!tip] 核心洞察
> 仅基于3D包围盒的几何关系，通过稀疏多路复用图神经网络和局部极坐标编码，即可实现高性能且强泛化的多目标跟踪，证明了几何线索在数据驱动MOT中的巨大潜力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PolarMOT: 几何关系在3D多目标跟踪中能走多远？ |
| 英文题名 | PolarMOT: How far can geometric relations take us in 3D multi-object tracking? |
| 会议/期刊 | ECCV 2022 |
| Links | [paper](https://arxiv.org/abs/2208.01957); [GitHub](https://github.com/aleksandrkim61/PolarMOT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | PolarMOT |
| Dataset | nuScenes test, nuScenes val (online), Cross-city Boston→Singapore |

> [!tip] 效果简介
> - nuScenes test 上，AMOTA average 为 66.4，对比 65.6 (OGR3MOT)，变化 +0.8。
> - nuScenes val (online) 上，AMOTA average 为 67.27，对比 65.91 (CenterPoint online)，变化 +1.36。
> - Cross-city Boston→Singapore 上，AMOTA average 为 63.12，对比 59.71 (CenterPoint)，变化 +3.41。

## 概述

3D多目标跟踪（MOT）是自动驾驶感知栈的核心组件，主流方法通常依赖**外观模型**（如重识别嵌入）来关联跨帧检测。然而，外观特征高度依赖训练环境，在光照变化、跨城市部署等场景下泛化能力有限。PolarMOT 提出一个根本性反问：**如果仅使用3D包围盒之间的几何关系，跟踪能走多远？**

其核心洞察是：物体间的**成对几何交互**——相对位置、航向变化、速度——蕴含了丰富的关联线索，但传统方法使用的全局笛卡尔坐标表示对旋转平移敏感，难以捕捉这种结构化信息。PolarMOT 的因果性操作变量是**局部极坐标编码**：将成对检测的相对位姿映射到以观测者为原点的极坐标系 $(v, \varphi_{i,j}, \Delta\phi, \Delta t)$，该表示天然具有全局变换不变性，并内嵌了非完整运动先验（航向角变化 $\Delta\phi$ 约束了车辆的运动可行性）。

方法层面，PolarMOT 将跟踪场景建模为**稀疏多路复用图**：检测作为节点，时序边和帧内空间边分别编码跨帧关联和同帧交互。图神经网络通过消息传递机制（按过去/现在/未来分组聚合）迭代更新边嵌入，最终对时序边进行二分类得到轨迹关联。整个网络完全由 MLP 构成，**不依赖任何外观特征**。

实验证据有力支撑了几何方法的竞争力：
- 在 **nuScenes 测试集**上，PolarMOT 以 **66.4 AMOTA** 超越所有仅使用3D输入的方法，达到新的最佳水平（Table 1）。
- 消融实验表明，将边特征从全局笛卡尔坐标替换为时间归一化的局部极坐标，在 mini 训练集上 AMOTA 提升 **+17.55**（57.96 vs 40.41），这是方法性能提升的最大单一因素（Table 3）。
- **跨城市泛化**实验（Boston→Singapore）中，PolarMOT 达到 63.12 AMOTA，远超 CenterPoint 的 59.71（+3.41），直接验证了几何方法对领域偏移的鲁棒性（Table 7）。

PolarMOT 在方法谱系中定位为**纯几何驱动的图神经网络跟踪器**，其架构基础继承自 2D MOT 的消息传递网络 **MPNTrack**（Brasó & Leal-Taixé, ECCV 2020），但通过局部极坐标编码、多路复用图结构和时间感知消息聚合，将其成功迁移至 3D 场景，并与 **OGR3MOT**（Zaech et al., IEEE R-AL 2022）等 3D 图跟踪方法形成直接对比。

需要指出的是，该方法**仅使用几何线索**，未融合图像外观信息，在严重遮挡或密集人群等几何模糊场景下可能存在固有局限；在线模式因只能访问过去信息，性能相比离线模式下降约 3.87 AMOTA。这些限制为后续融合外观特征或引入域自适应技术留下了明确的改进空间。

## 背景与动机

3D多目标跟踪（3D MOT）是自动驾驶感知栈中的核心任务，其目标是在连续帧间为所有目标维护一致的身份标识。与2D MOT不同，3D MOT直接操作于三维空间中的包围盒（bounding box），这些包围盒通常由激光雷达（LiDAR）点云检测器输出。一个高性能的3D MOT系统需要同时解决目标关联的准确性和跨场景的鲁棒性，而这两者恰恰构成了当前方法的核心瓶颈。

### 现有方法的缺口

当前3D MOT方法普遍存在两个结构性缺陷：

**过度依赖外观模型。** 多数方法将外观特征（如重识别嵌入）作为关联的核心线索。然而，外观模型高度依赖于训练环境的传感器配置、光照条件和目标外观分布。一旦部署到传感器参数不同或城市风貌迥异的新场景，外观特征的判别力便会显著退化。这种脆弱性直接限制了跟踪器的跨域泛化能力。

**几何信息利用不足。** 尽管3D检测天然提供精确的空间位置和朝向信息，现有方法对物体间几何交互的建模仍然粗糙。主流方案要么将几何关系简化为全局笛卡尔坐标下的位置差（如 $\Delta x, \Delta y$），要么仅依赖卡尔曼滤波等运动模型进行单目标状态预测。这些做法忽略了一个关键事实：**全局笛卡尔坐标表示对旋转和平移高度敏感**，同一组目标的相对几何关系在不同坐标系下会产生截然不同的数值表征，迫使模型记忆特定的坐标模式而非学习可泛化的几何规律。

此外，物体之间的空间交互——如同帧内车辆间的相对位姿——蕴含着丰富的场景上下文信息，但这一信号在现有方法中几乎未被利用。例如，在密集交通流中，相邻车辆的空间布局可以为遮挡目标的身份推断提供强约束，而仅依赖时序关联的方法无法捕获此类线索。

### 核心动机与洞察

本文的核心动机源于一个根本性问题：**如果剥离所有外观信息，仅凭3D包围盒之间的几何关系，数据驱动的多目标跟踪能走多远？**

这一追问指向一个被长期低估的假设：几何线索本身——只要以恰当的方式编码——可能足以支撑高性能且强泛化的跟踪。问题的关键不在于几何信息是否充足，而在于**如何表示**这些几何关系。传统的全局笛卡尔坐标差将几何关系与绝对坐标系绑定，破坏了相对运动的本质不变性。本文提出，若能将成对几何关系转化为一种对全局变换不敏感的局部表示，并在此表示中嵌入非完整运动先验（non-holonomic motion prior），几何线索的潜力将得到极大释放。

具体而言，本文的核心洞察是：**采用以观测目标为中心的局部极坐标系（localized polar coordinates）编码成对几何关系，可以使表示天然具备全局旋转平移不变性，同时通过极角分量隐式编码航向变化，为图神经网络提供结构化的运动先验。** 在此基础上，将场景建模为稀疏多路复用图（sparse multiplex graph），通过消息传递网络融合时序和空间上下文，即可构建一个纯粹基于几何的、具有强泛化能力的3D MOT框架——PolarMOT。

## 核心创新

PolarMOT 的核心创新在于**彻底摒弃外观模型，仅依赖几何关系实现高性能、强泛化的3D多目标跟踪**。其关键操作性变量是**局部极坐标编码的成对几何关系**，这一表示具有全局变换不变性，并内嵌非完整运动先验，从根本上解决了传统笛卡尔坐标表示对旋转平移敏感、难以泛化的瓶颈。

### 局部极坐标几何编码：核心因果旋钮

PolarMOT 将3D检测框之间的几何关系编码为局部极坐标特征，而非传统的全局笛卡尔坐标差。具体而言，对于两个检测对象 $o_i$ 和 $o_j$，其边特征初始化为：

$$h_{i,j}^{(0)} = \Delta(o_i, o_j) = \big[ v, \varphi_{i,j}, \Delta\phi, \Delta t \big]$$

其中 $v$ 是相对速度，$\varphi_{i,j}$ 是极角，$\Delta\phi$ 是航向角变化，$\Delta t$ 是时间差。与之对比，传统方法仅使用：

$$h_{i,j}^{(0)} = \Delta(o_i, o_j) = \big[ \Delta x, \Delta y \big]$$

这一改变的因果效应在消融实验中得到了决定性验证：在 mini 训练集上，将边特征从全局笛卡尔坐标替换为时间归一化的局部极坐标，**AMOTA 从 40.41 跃升至 57.96（+17.55）**（Table 3）。局部极坐标的核心优势体现在两个层面：

1. **全局变换不变性**：如图3b所示，对于相同的位姿变化 AB 和 BC，全局笛卡尔特征并不相同，而局部极坐标表示则具有一致性，这使得模型能够学习到与全局坐标系无关的通用几何模式。
2. **非完整运动先验**：极坐标显式编码航向角变化 $\varphi$，这为模型提供了平滑、非完整的运动先验，使其天然倾向于符合物理规律的运动模式。

### 稀疏多路复用图结构

PolarMOT 将场景建模为**稀疏多路复用图**，包含两种不同类型的边：

- **时序边（inter-frame edges）**：连接不同时间步的检测，代表潜在的跨帧关联。通过各类别的最大速度阈值进行剪枝，仅保留物理上可能的关联，确保图的稀疏性。
- **空间边（intra-frame edges）**：连接同一帧内的检测，编码空间交互关系。消融实验表明，加入帧内空间边可带来 **+1.05 AMOTA 和 +2.4% 召回率的提升**（Table 4），证明空间上下文对于跟踪精度有显著贡献。

### 时间感知的消息传递

PolarMOT 在节点消息聚合中引入了**时间方向感知**机制。消息构建根据边的时间方向使用不同的 MLP：

$$m_{(i,j)}^{(l)} = \begin{cases} \mathrm{MLP}_{\mathrm{past}}([h_i^{(l-1)}, h_{(i,j)}^{(l)}, h_j^{(l-1)}]) & t_j < t_i \\ \mathrm{MLP}_{\mathrm{pres}}([h_i^{(l-1)}, h_{(i,j)}^{(l)}, h_j^{(l-1)}]) & t_i = t_j \\ \mathrm{MLP}_{\mathrm{fut}}([h_i^{(l-1)}, h_{(i,j)}^{(l)}, h_j^{(l-1)}]) & t_j > t_i \end{cases}$$

随后，节点分别对过去、现在、未来的消息进行最大池化后拼接融合：

$$h_i^{(l)} = \mathrm{MLP}_{\mathrm{node}} \big( \big[ \max_{t_j < t_i} m_{(i,j)}^{(l)}, \max_{t_i = t_j} m_{(i,j)}^{(l)}, \max_{t_j > t_i} m_{(i,j)}^{(l)} \big] \big)$$

这一设计对于维持时间上下文意识至关重要：消融实验表明，若将所有时间方向的消息混在一起聚合，**AMOTA 将骤降 47.84**（Table 12），充分证明了时间方向感知是不可或缺的设计选择。

### 节点特征隐式学习

与依赖外观嵌入或显式位置编码的传统方法不同，PolarMOT 的**节点特征完全从边特征通过消息传递隐式学习**，不赋予节点任何初始特征。这一设计迫使模型仅从几何关系中提取判别信息，是几何方法纯粹性的关键保证。

### 在线图演化策略

在线模式下，PolarMOT 采用**剪枝+跳跃连接（prune + skip）**策略维持稀疏图并赋予全局时间感受野。具体而言，当新帧到达时，旧节点被剪枝但保留关键跳跃边，使得新节点能够直接访问遥远的过去信息。这一策略相比密集连接提升 **+5.88 AMOTA**，相比仅保留连续边提升 **+1.24 AMOTA**（Table 6），在稀疏性和信息完整性之间取得了最优平衡。

### 与基线方法的关键差异总结

| 设计维度 | 基线方法 | PolarMOT | 因果效应 |
|---------|---------|----------|---------|
| 几何关系编码 | 全局笛卡尔坐标差 | 局部极坐标 $(v, \varphi, \Delta\phi, \Delta t)$ | +17.55 AMOTA (mini) |
| 图边类型 | 仅时序边 | 时序边 + 空间边 | +1.05 AMOTA, +2.4% 召回率 |
| 节点消息聚合 | 所有边一起聚合 | 按过去/现在/未来分组聚合 | 避免 47.84 AMOTA 骤降 |
| 在线图连接 | 密集或仅连续边 | 剪枝+跳跃连接 | +5.88 / +1.24 AMOTA |
| 节点特征 | 外观嵌入或显式编码 | 仅从边特征隐式学习 | 强制几何纯粹性 |
| 运动先验 | 无显式编码 | 极坐标 $\varphi$ 编码航向角变化 | 非完整运动先验 |

## 整体框架

PolarMOT将多目标跟踪形式化为一个基于稀疏多路复用图的消息传递问题。其整体pipeline由四个核心模块串联构成，输入为序列化的3D检测框，输出为跨帧关联的完整轨迹。

**输入与图构建。** 给定一帧或多帧的3D检测集合 $\mathcal{O} = \{ o_i \}_{i=1}^n$，每个检测 $o_i$ 包含3D包围盒的位置、尺寸、航向角以及时间戳。PolarMOT将每个检测实例化为图中的一个节点，并根据两类关系建立边：**时序边**（inter-frame edges）连接不同帧的检测，构成跨帧关联的候选假设；**空间边**（intra-frame edges）连接同一帧内的检测，编码帧内物体间的空间交互。为保证图的稀疏性，时序边在建立时受类别最大速度约束——若两检测间的物理距离超过该类别物体的最大速度可达范围，则认为它们不可能属于同一目标，不建立边（Sec. 4.2, Figure 3a）。

**边特征初始化。** 每条边的初始特征直接从成对检测的几何关系计算得到。与传统方法使用全局笛卡尔坐标差 $[\Delta x, \Delta y]$ 不同，PolarMOT采用**局部极坐标编码** $[v, \varphi_{i,j}, \Delta\phi, \Delta t]$，分别表示相对速度、极角、航向角差和时间差（Eq. 7）。该表示具有全局旋转平移不变性，并内嵌了非完整运动先验（航向角变化 $\varphi$ 编码了平滑转向约束）。初始边特征通过 $\mathrm{MLP}_{\mathrm{edge-init}}$ 映射为高维嵌入 $h_{(i,j)}^{(1)}$ 后进入消息传递网络（Sec. 4.3）。

**消息传递网络。** 图神经网络通过交替执行边更新与节点更新来融合时空上下文。在第 $l$ 步，边嵌入首先由相连节点的前一步嵌入联合更新（Eq. 1）：
$$h_{(i,j)}^{(l)} = \mathrm{MLP}_{\mathrm{edge}}\left(\left[ h_i^{(l-1)}, h_{(i,j)}^{(l-1)}, h_j^{(l-1)} \right]\right)$$
随后，基于更新后的边嵌入和节点嵌入构建有向消息。关键设计在于根据边的时间方向（过去/现在/未来）使用**不同的MLP**分别处理（Eq. 2），以维持时序上下文意识。节点聚合时，对三类消息分别做逐元素最大池化后拼接，再通过 $\mathrm{MLP}_{\mathrm{node}}$ 融合得到新节点特征（Eq. 3）。值得注意的是，节点特征完全通过消息传递从边特征中隐式学习，不依赖任何外观嵌入或显式位置编码（Sec. 4.2, Figure 2 center）。

**边分类与轨迹解码。** 经过 $L$ 步消息传递后，每条时序边被输入一个二分类器，判断其连接的两节点是否属于同一目标。最终通过贪心分配确保每条轨迹在每帧最多拥有一个关联，输出完整的跟踪轨迹（Sec. 4.2, Sec. A.1）。

**在线图演化。** 在线模式下，每帧新检测到来时，PolarMOT采用**剪枝+跳跃连接**（prune + skip）策略维持图的稀疏性：新节点仅与过去 $k$ 帧内的活跃节点建立时序边，同时保留活跃节点与更早帧的跳跃连接，从而在保持计算效率的同时赋予每个新节点全局时间感受野（Sec. 4.4, Figure 3c）。

整个pipeline仅依赖3D包围盒的几何信息，不引入任何图像外观特征，从根本上规避了外观模型对特定环境的过拟合风险。

## 核心模块与公式推导

PolarMOT 将多目标跟踪建模为图上的边分类问题。其核心由四个模块构成：稀疏多路复用图构建、局部极坐标边特征初始化、消息传递网络、以及边分类与后处理。在线模式下，还包括一个持续演化的图构建策略。

### 4.1 稀疏多路复用图构建

给定一帧点云序列的 3D 检测集合 $\mathcal{O} = \{ o_i \}_{i=1}^n$，每个检测 $o_i$ 包含中心位置 $(x_i, y_i)$、朝向角 $\phi_i$、速度 $v_i$ 和时间戳 $t_i$。PolarMOT 将每个检测建模为图节点，并通过两类边构建**稀疏多路复用图（sparse multiplex graph）**（图 3a）：

- **时序边（inter-frame edges）**：连接不同帧的检测，表示潜在的同一目标关联。为保持图稀疏，仅当两检测间的物理距离小于该类别最大速度与时间差的乘积时才建立边。
- **空间边（intra-frame edges）**：连接同一帧内的检测，编码场景中物体间的空间交互关系。

消融实验（Table 4）表明，加入帧内空间边可带来 +1.05 AMOTA 和 +2.4% 召回率的提升，验证了空间上下文对关联决策的辅助作用。

### 4.2 局部极坐标边特征初始化

传统方法通常使用全局笛卡尔坐标差 $[\Delta x, \Delta y]$ 作为边特征（Eq. 6）。PolarMOT 提出**局部极坐标编码**，将成对检测的几何关系表示为：

$$h_{i,j}^{(0)} = \Delta(o_i, o_j) = \big[ v, \varphi_{i,j}, \Delta\phi, \Delta t \big] \quad \text{(Eq. 7)}$$

其中：
- $v$：检测 $o_i$ 的速度幅值
- $\varphi_{i,j}$：从 $o_i$ 到 $o_j$ 的极角，在 $o_i$ 的局部坐标系下计算
- $\Delta\phi$：两检测的朝向角差
- $\Delta t$：时间差

该表示具有两个关键性质：
1. **全局变换不变性**：相同的相对运动在不同全局位置下产生相同的极坐标特征，而笛卡尔坐标差会随全局旋转平移而变化（图 3b）。
2. **非完整运动先验**：极角 $\varphi_{i,j}$ 显式编码了朝向角变化，为网络提供了平滑运动约束的归纳偏置。

消融实验（Table 3）是 PolarMOT 最关键的因果验证：在 mini 训练集上，将边特征从全局笛卡尔坐标替换为时间归一化的局部极坐标，AMOTA 从 40.41 跃升至 57.96（+17.55），证明了几何表示选择对性能的决定性影响。

### 4.3 消息传递网络

PolarMOT 采用 $L$ 步消息传递来融合时空上下文。每步迭代依次执行边更新、消息构建和节点聚合。

**边嵌入更新**（Eq. 1）：第 $l$ 步的边特征通过融合前一步的边嵌入及其两端节点嵌入得到：

$$\boldsymbol{h}_{(i,j)}^{(l)} = \mathrm{MLP}_{\mathrm{edge}}\left(\left[ h_i^{(l-1)}, h_{(i,j)}^{(l-1)}, h_j^{(l-1)} \right]\right)$$

**节点消息构建**（Eq. 2）：根据边的时间方向，使用不同的 MLP 将更新后的边特征转化为有向消息：

$$m_{(i,j)}^{(l)} = \begin{cases} \mathrm{MLP}_{\mathrm{past}}([h_i^{(l-1)}, h_{(i,j)}^{(l)}, h_j^{(l-1)}]) & t_j < t_i \\ \mathrm{MLP}_{\mathrm{pres}}([h_i^{(l-1)}, h_{(i,j)}^{(l)}, h_j^{(l-1)}]) & t_i = t_j \\ \mathrm{MLP}_{\mathrm{fut}}([h_i^{(l-1)}, h_{(i,j)}^{(l)}, h_j^{(l-1)}]) & t_j > t_i \end{cases}$$

**节点聚合**（Eq. 3）：分别对过去（$t_j < t_i$）、现在（$t_i = t_j$）、未来（$t_j > t_i$）的消息进行逐元素最大化池化，拼接后通过 MLP 得到新节点特征：

$$h_i^{(l)} = \mathrm{MLP}_{\mathrm{node}} \big( \big[ \max_{t_j < t_i} m_{(i,j)}^{(l)}, \max_{t_i = t_j} m_{(i,j)}^{(l)}, \max_{t_j > t_i} m_{(i,j)}^{(l)} \big] \big)$$

这种**分组聚合**策略对维持时间上下文意识至关重要。消融实验（Table 12）显示，若将所有消息混在一起处理，AMOTA 会骤降 47.84，充分证明了按时间方向分别编码的必要性。

值得注意的是，PolarMOT 的节点特征**不包含任何显式的外观嵌入或位置编码**，完全通过边特征的消息传递隐式学习节点表示。

### 4.4 边分类与在线图演化

经过 $L$ 步消息传递后，时序边特征通过二分类头输出关联概率。后处理阶段采用贪心分配策略，确保每条轨迹在每帧最多有一个关联。

在在线模式下，PolarMOT 采用**剪枝+跳跃连接（prune + skip）**策略维持稀疏图（图 3c）：新帧到来时，仅保留活跃轨迹节点，并通过跳跃边连接非连续帧的节点，从而在保持图稀疏的同时赋予每个新节点全局时间感受野。消融实验（Table 6）表明，该策略优于密集连接（+5.88 AMOTA）和仅保留连续边（+1.24 AMOTA）的方案。

## 实验与分析

PolarMOT的实验设计围绕一个核心问题展开：**仅凭3D包围盒之间的几何关系，能否实现高性能且强泛化的多目标跟踪？** 为此，作者在nuScenes数据集上进行了全面的基准测试、消融实验和跨域泛化评估，所有实验均使用**CenterPoint**（Yin et al., CVPR 2021）提供的统一检测结果，确保跟踪器本身的性能不受检测器差异影响。

### 主实验结果

在nuScenes测试集上，PolarMOT以**66.4 AMOTA**的平均得分超越了所有仅使用3D输入（激光雷达/3D包围盒）的方法，达到新的最佳水平（Table 1）。相比此前最优的**OGR3MOT**（Zaech et al., IEEE R-AL 2022）的65.6，提升了0.8个点。值得注意的是，这一结果甚至接近了部分融合图像和激光雷达的方法（如AlphaTrack），验证了几何线索在数据驱动MOT中的巨大潜力。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/004_Table_1.jpg]]
*Table 1: Results of state-of-the-art methods for 3D multi-object tracking on the NuScenes test set. Legend: L – lidar, B – 3D bounding boxes*

在在线与离线模式的对比中（Table 2），PolarMOT离线版本达到67.27 AMOTA，在线版本同样以67.27 AMOTA超越了在线CenterPoint的65.91，提升**+1.36 AMOTA**。在线模式由于只能访问过去信息，性能相比离线模式下降约3.87 AMOTA，这是时间因果性约束带来的固有代价。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/005_Table_2.jpg]]
*Table 2: Online vs. offline tracking on the nuScenes validation set [8]*

### 消融实验：关键设计选择

消融实验系统性地拆解了PolarMOT各设计组件的贡献，揭示了几个关键因果机制。

**局部极坐标编码是性能提升的核心杠杆。** Table 3在mini训练集上的消融表明，将边特征从全局笛卡尔坐标（$\Delta x, \Delta y$）替换为时间归一化的局部极坐标（$v, \varphi_{i,j}, \Delta\phi, \Delta t$），AMOTA从**40.41跃升至57.96**，提升幅度高达**+17.55**。这一巨大差异的根源在于：全局笛卡尔坐标对旋转平移敏感，相同的相对运动在不同位置会产生不同的特征表示；而局部极坐标具有全局变换不变性，且通过航向角差$\Delta\phi$内嵌了非完整运动先验，使网络更容易学习到可泛化的运动模式。

**帧内空间边的引入带来一致但相对温和的增益。** Table 4显示，在时序边基础上添加空间边，AMOTA提升**+1.05**，召回率提升**+2.4%**。空间边使同一帧内的检测节点能够交换上下文信息，有助于处理遮挡和密集场景中的歧义关联，但其贡献远小于极坐标编码，说明时序关系仍是关联任务的主导线索。

**节点消息的时序分组聚合是维持上下文意识的关键。** Table 12的消融揭示了最极端的性能退化：若将过去、现在、未来的边消息混在一起进行聚合（而非分别池化），AMOTA将从正常水平骤降**47.84**。这一现象表明，不同时间方向的边携带了本质上不同的语义信息——过去边提供轨迹历史约束，未来边（仅离线模式）提供后续观测证据，现在边编码空间交互——将它们混淆会导致节点无法区分时间上下文，丧失关联判断能力。

**在线图构建的剪枝+跳跃策略在稀疏性和感受野之间取得最优平衡。** Table 6对比了三种在线图连接策略：密集连接、仅保留连续边、以及PolarMOT的剪枝+跳跃连接。剪枝+跳跃相比密集连接提升**+5.88 AMOTA**，相比仅连续连接提升**+1.24 AMOTA**。密集连接引入过多噪声边导致优化困难，仅连续连接则限制了时间感受野；剪枝+跳跃通过保留关键跳跃边，在维持图稀疏性的同时赋予每个新节点全局时间感受野。

### 跨域泛化实验

为验证纯几何方法的泛化优势，作者进行了跨城市迁移实验（Table 7）。在Boston训练→Singapore评估的设置下，PolarMOT达到**63.12 AMOTA**，远超CenterPoint的**59.71**，提升**+3.41 AMOTA**。这一结果直接证明了：外观模型容易过拟合到训练环境的外观特征分布，而几何关系具有更强的环境不变性，使PolarMOT在域迁移场景下展现出显著优势。反向迁移（Singapore→Boston）同样观察到一致趋势。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/010_Table_7.jpg]]
*Table 7: CenterPoint (CP) [62] and our method when trained on training data from one city, and evaluated on the validation data from another*

进一步的跨数据集泛化实验中（Table 8, Table 9），仅用nuScenes训练的PolarMOT直接应用于KITTI数据集，在3D MOT和2D MOT任务上均取得有竞争力的结果，无需任何微调，进一步验证了几何表示的通用性。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/011_Table_8.jpg]]
*Table 8: Unofficial KITTI 3D MOT validation set benchmark [56]. Our model was trained only on nuScenes dataset*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/012_Table_9.jpg]]
*Table 9: KITTI 2D MOT test set benchmark. Our model was trained only on nuScenes dataset*

### 失败模式与局限

尽管PolarMOT在纯几何跟踪上取得了突破性进展，其设计选择也带来了固有的局限：

1. **严重遮挡场景下的脆弱性**：由于完全未使用外观特征，当两个同类目标在空间上高度接近且运动模式相似时（如行人交错穿行），纯几何线索可能不足以区分它们的身份。Figure 1的定性对比显示，PolarMOT在处理高遮挡场景时优于CenterPoint，但仍存在改进空间。

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/003_Figure.jpg]]
*Figure: (a) Full (sparse) graph. (b) Relational features. (c) Online construction*

2. **在线-离线性能差距**：在线模式因无法访问未来信息，AMOTA比离线模式低约3.87，这一差距在需要即时决策的自动驾驶场景中具有实际影响。

3. **对检测质量的依赖**：方法性能依赖于3D检测的精度，尽管通过训练时的噪声丢弃数据增强提升了鲁棒性，但在检测质量显著下降时关联性能仍会受到影响。

### 开放问题

基于上述实验分析，几个值得进一步探索的方向包括：如何有效地将外观特征与几何特征融合以提升拥挤场景下的判别力；能否通过自监督或域自适应技术缩小在线-离线性能差距；局部极坐标编码能否推广到其他涉及位姿估计和时序建模的任务中。

### 补充图表

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/006_Table_3.jpg]]
*Table 3: Ablation on parametrization of geometric relations among objects on nuScenes validation set. Trained on the official mini training set*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/007_Table_4.jpg]]
*Table 4: Ablation for intra-frame edges on the nuScenes validation set*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/008_Table_5.jpg]]
*Table 5: Sparse graph construction: the impact of reducing/increasing the maximal velocity threshold on online tracking (nuScenes validation set)*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/009_Table_6.jpg]]
*Table 6: Online graph construction analysis (nuScenes validation set)*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/013_Table_10.jpg]]
*Table 10: Neural network architecture of PolarMOT . Each cell describes the output dimensionality of each layer in the fully-connected MLPs of our model*

![[assets/figures/papers/paper_list_l30_https_arxiv_org_abs_2208_01957/figures/014_Table_11.jpg]]
*Table 11: Ablation on parametrization of geometric relations among objects on the nuScenes validation set. Trained on the full training set*

## 方法谱系与知识库定位

### 方法继承与演化

PolarMOT 直接继承自 **MPNTrack**（Brasó & Leal-Taixé, ECCV 2020）的消息传递网络框架，该工作将2D多目标跟踪建模为图上的边分类问题。PolarMOT 沿用了“检测为节点、关联假设为边、通过学习边分类获得最终轨迹”的核心范式，但进行了三个关键维度的迁移与改造：

1. **从2D到3D的域迁移**：将图构建和特征编码从图像平面扩展至三维空间，处理激光雷达点云生成的3D包围盒。
2. **从外观到几何的线索切换**：MPNTrack 依赖外观嵌入作为节点特征，而 PolarMOT 完全摒弃外观信息，仅基于成对几何关系进行关联推理，节点特征完全通过边消息传递隐式习得。
3. **图结构的时空扩展**：在原有帧间时序边的基础上，引入帧内空间边，构建**稀疏多路复用图**（sparse multiplex graph），使模型能够同时建模物体间的时序关联和空间交互。

与同属3D MOT图神经网络路线的 **OGR3MOT**（Zaech et al., IEEE R-AL 2022）相比，PolarMOT 的核心差异在于：（i）OGR3MOT 将检测和轨迹建模为两类异质节点，而 PolarMOT 采用同质节点设计；（ii）OGR3MOT 使用全局笛卡尔坐标差作为边特征，PolarMOT 则引入**局部极坐标编码**，具备全局变换不变性和非完整运动先验。

### 关键创新与知识贡献

PolarMOT 的核心知识贡献在于证明：**仅凭3D包围盒间的几何关系，通过合适的表示编码和图网络架构，即可实现高性能且强泛化的多目标跟踪**。具体知识增量体现在：

- **局部极坐标编码**（localized polar coordinates）：将成对检测的相对位姿表示为 $(v, \varphi_{i,j}, \Delta\phi, \Delta t)$，其中 $\varphi$ 显式编码航向角变化，内嵌非完整运动先验。该表示对全局旋转平移不变，解决了传统笛卡尔坐标差对坐标系敏感的泛化瓶颈。消融实验表明，将边特征从全局笛卡尔坐标替换为时间归一化的局部极坐标，在mini训练集上AMOTA从40.41提升至57.96（+17.55，Table 3），是全文中效应量最大的单一设计选择。

- **时间感知的节点消息聚合**：按过去、现在、未来三个时间方向分别进行消息构建和池化（Eq. 2-3），再拼接融合。若将所有时间方向的消息混在一起聚合，AMOTA骤降47.84（Table 12），证明分时间方向维护上下文意识是维持跟踪性能的必要条件。

- **在线图演化策略**：提出“剪枝+跳跃连接”（prune + skip）策略，在保持图稀疏性的同时赋予新节点全局时间感受野，相比密集连接提升+5.88 AMOTA，相比仅保留连续边提升+1.24 AMOTA（Table 6）。

### 适用边界与局限

**适用条件**：
- 依赖3D检测器提供的高质量包围盒，所有实验均基于 **CenterPoint**（Yin et al., CVPR 2021）的检测结果。
- 需要已知检测类别以设定最大速度阈值用于图稀疏化剪枝。
- 训练和推理仅需3D包围盒的位置、尺寸、航向角和时间戳，不依赖外观特征或原始传感器数据。

**已知局限**：
1. **纯几何线索的天花板**：在严重遮挡或相似轨迹交错场景下，缺乏外观信息可能导致关联歧义。论文明确指出未融合图像外观信息是潜在改进方向。
2. **在线模式的性能折损**：由于只能访问过去信息，在线模式相比离线模式AMOTA下降约3.87（67.27 vs 71.14，Table 2），反映了因果约束下的信息损失。
3. **检测质量敏感性**：方法性能对3D检测精度有一定依赖，尽管通过噪声丢弃等数据增强手段提升了鲁棒性，但在检测召回率低或定位噪声大的场景下关联质量可能退化。

### 开放问题

1. **几何与外观的融合机制**：如何在保持几何编码泛化优势的同时，有效融入外观特征以提升拥挤场景下的区分能力？简单的特征拼接可能破坏极坐标编码的变换不变性，需要设计更精细的融合策略。

2. **在线-离线差距的缩小**：能否通过自监督预训练、域自适应技术或引入预测模块，在不牺牲在线约束的前提下缩小与离线模式的性能差距？

3. **表示方法的可迁移性**：局部极坐标编码是否可推广至其他涉及相对位姿估计和时序建模的任务，如轨迹预测、行为识别或多智能体协同感知？

4. **长序列在线图演化**：剪枝+跳跃策略在极长序列下的图规模增长和计算效率尚需进一步验证，是否存在更优的图维护策略以平衡感受野与计算开销？

## 原文 PDF

![[paperPDFs/ECCV_2022/PolarMOT_How_far_can_geometric_relations_take_us_in_3D_multi_object_tracking.pdf]]
