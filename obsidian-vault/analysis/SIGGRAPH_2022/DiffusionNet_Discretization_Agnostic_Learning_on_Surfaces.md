---
title: "DiffusionNet: Discretization Agnostic Learning on Surfaces"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/DiffusionNet_Discretization_Agnostic_Learning_on_Surfaces.pdf
project_link: "https://nmwsharp.com/research/diffusion-net/"
code_link: null
aliases:
- DiffusionNet
tags:
- SIGGRAPH_2022
- topic/generative_models_diffusion
core_operator: 将空间通信替换为可学习的扩散过程，用连续扩散时间取代离散邻域和池化，同时引入空间梯度特征捕获方向滤波。
primary_logic: 扩散结合逐点MLP和梯度内积能够表达丰富的径向和方向滤波器，且扩散运算基于几何先验，自然地对离散化鲁棒，从而构建简单、高效、鲁棒的表面学习网络。
claims:
- 去除任意组件导致性能显著下降（无扩散时准确率从 90.6% 降至 31.4%）
- 在网格重剖分和采样变化下，DiffusionNet 的对应误差远低于现有方法（原网格 0.33 vs. 9.57）
- 网络可在网格训练后直接在点云上评估，并保持准确
- FAUST vertex-labelling correspondence (original meshes) 上 mean geodesic error ×100 (↓) = 0.33
---

# DiffusionNet: Discretization Agnostic Learning on Surfaces

> [!tip] 核心洞察
> 扩散结合逐点MLP和梯度内积能够表达丰富的径向和方向滤波器，且扩散运算基于几何先验，自然地对离散化鲁棒，从而构建简单、高效、鲁棒的表面学习网络。

| 字段 | 内容 |
|------|------|
| 中文题名 | 扩散网络：离散化无关的表面学习 |
| 英文题名 | DiffusionNet: Discretization Agnostic Learning on Surfaces |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://nmwsharp.com/research/diffusion-net/) |
| Topic | #topic/generative_models_diffusion |
| Method | DiffusionNet |
| Dataset | FAUST vertex-labelling correspondence |

> [!tip] 效果简介
> - FAUST vertex-labelling correspondence (original meshes) 上，mean geodesic error ×100 (↓) 0.33 vs 9.57 (HSN) (-9.24)。
> - FAUST vertex-labelling correspondence (isotropic remeshing) 上，mean geodesic error ×100 (↓) 0.68 vs 20.01 (HSN) (-19.33)。
> - FAUST vertex-labelling correspondence (dense resampling) 上，mean geodesic error ×100 (↓) 0.62 vs 24.84 (HSN) (-24.22)。

## 概要

现有表面学习方法（如 MeshCNN、SplineCNN、HSN 等）高度依赖网格连接性等特定离散表示，难以泛化到不同采样、分辨率或点云输入，且手工设计的卷积与池化层次限制了可扩展性。本文提出 **DiffusionNet**，一种简单而通用的表面学习架构：将空间信息传播替换为**可学习的扩散过程**，以连续扩散时间取代离散邻域和池化；同时引入**空间梯度特征**，通过可学习内积构造方向敏感滤波器，且不依赖局部切平面基的选择。网络由逐点 MLP、学习扩散层、梯度特征和残差连接堆叠而成，无需显式表面卷积或池化层次。

在 FAUST 顶点标注对应任务上，DiffusionNet 在原始网格上测地线误差仅 **0.33**（HSN 为 9.57）；在网格重剖分和密集重采样下误差分别仅为 **0.68** 和 **0.62**，而 HSN 分别升至 20.01 和 24.84，展现出显著的离散化鲁棒性。网络支持在网格上训练后直接评估点云，并在 SHREC11 分类（30 类仅 10 样本/类）上达到近乎完美准确率。消融实验证实：移除扩散层使准确率从 90.6% 骤降至 31.4%，固定扩散时间或移除梯度特征亦导致明显退化。

该方法以扩散作为核心通信机制，将空间支持的学习内化于连续时间参数，为几何深度学习提供了一种**离散化无关**的新范式。

## 核心方法与创新机理

### 问题瓶颈与设计动机

现有表面学习方法面临一个根本性瓶颈：它们高度依赖特定的几何离散表示，尤其是三角网格的连接性结构。基于边的卷积网络（如 **MeshCNN**，Hanocka et al., 2019）、基于样条的卷积（如 **SplineCNN**，Fey et al., 2018）以及各类谱方法（如 **ACSCNN**，Li et al., 2020b）都在训练时隐式地编码了网格拓扑信息，导致当测试形状的采样密度、网格剖分方式或表示形式（如点云）与训练集不同时，性能急剧退化。此外，这些方法普遍依赖手工设计的卷积核半径或池化层次结构（如网格简化），限制了感受野的自适应调节能力和对全分辨率模型的扩展性。

DiffusionNet 的核心洞察在于：**连续域上的扩散过程天然地提供了空间通信机制，且对离散化方式具有内在鲁棒性**。通过将空间信息传播替换为可学习的各向同性扩散，同时引入空间梯度特征以捕获方向滤波，该方法构建了一个简单、高效且离散化无关的表面学习框架。

### 核心机制：扩散作为空间通信原语

DiffusionNet 将空间信息混合建模为热扩散过程。给定表面上的标量场 $u$，其扩散遵循热方程：

$$\frac{d}{dt} u_t = \Delta u_t$$

在离散设定下，使用弱拉普拉斯矩阵 $L$ 和质量矩阵 $M$，扩散速率为 $-M^{-1}Lu$。该方法的核心操作是执行单步隐式欧拉扩散：

$$h_t(u) := (M + tL)^{-1} M u$$

其中 $t$ 是扩散时间，控制空间支持的范围。这一公式的关键意义在于：**扩散时间 $t$ 被设为可学习参数，且每个特征通道独立拥有自己的 $t$ 值**。在训练过程中，网络自动为每一层、每一通道优化最优的扩散时间，从而隐式地实现了从局部到全局的连续感受野调节——无需手工指定邻域大小，也无需构建池化金字塔。

这一设计将传统的显式卷积（测地线卷积、边卷积等）替换为基于物理先验的扩散操作。由于扩散方程的解仅依赖于底层几何（由拉普拉斯算子刻画），而非特定的网格连接结构，该方法天然地对重剖分、重采样和分辨率变化具有鲁棒性。

### 关键公式与计算路径

**谱加速扩散计算**：为高效计算扩散，DiffusionNet 利用拉普拉斯特征值问题的截断谱基。求解弱形式特征问题：

$$L \phi_i = \lambda_i M \phi_i$$

得到特征向量 $\Phi = [\phi_0, \phi_1, \dots, \phi_{k-1}]$ 和特征值 $\lambda_i$。扩散操作可在谱域中表达为：

$$h_t(u) := \Phi \left[ e^{-\lambda_0 t}, e^{-\lambda_1 t}, \dots \right] \odot (\Phi^T M u)$$

其中 $\odot$ 表示逐元素乘法。该方法将特征向量投影到谱基上，乘以指数衰减因子，再反投影回空间域。论文验证了截断到低频基（默认使用 128 个特征向量）对结果影响极小，且谱方法与隐式方法的训练精度相当。需注意，DiffusionNet 并非谱学习方法——谱系数从不用于表示滤波器或潜在数据，因此不存在跨形状特征基不一致的问题。

**空间梯度特征**：仅使用扩散操作只能表达径向对称滤波器（扩散后接 MLP 等价于各向同性卷积）。为捕获方向信息，DiffusionNet 引入空间梯度特征。对于每个标量特征通道 $u$，通过预计算的稀疏梯度矩阵 $G$ 计算逐顶点空间梯度：

$$z_u := G u$$

将所有通道的梯度向量堆叠为 $w_v$，然后通过可学习的线性变换 $A$ 和成对内积构造方向特征：

$$g_v := \mathrm{tanh}(\mathrm{Re}(\overline{w}_v \odot A w_v))$$

其中 $A$ 可以是复矩阵（实现切平面内的旋转变换）或实矩阵（仅实现缩放）。使用复矩阵版本时，网络能感知切平面内的方向（如区分左右），但要求法线一致定向；使用实矩阵版本则避免了对法线一致性的依赖，同时保持对局部切空间基选择的不变性。

### 架构模块与因果链

DiffusionNet 的整体架构由连续的相同结构块（DiffusionNet Block）堆叠而成，每个块包含三个核心模块，按以下顺序执行：

1. **学习扩散层**：对输入的 $D$ 维逐顶点特征，在每个通道上以独立的学习扩散时间 $t$ 执行热扩散。该层负责空间信息混合，其输出是原始特征经不同程度空间平滑后的结果。学习到的扩散时间分布如图 4 所示：浅层块主要使用小时间（局部扩散），深层块中部分通道学习到大时间（近全局支持），自动形成了多尺度特征层次。

2. **空间梯度特征**：在扩散后的特征上计算空间梯度，通过可学习的内积生成方向敏感特征。该模块将扩散层输出的标量场转化为包含局部方向信息的特征向量，使网络能够捕获各向异性模式（如边缘、弯曲方向），同时保持对切空间基选择的不变性。

3. **逐点 MLP**：在每个顶点独立应用相同的多层感知机，将扩散特征与梯度特征联合映射到新的特征空间。该 MLP 是逐点共享的，负责非线性特征变换和通道混合。

此外，每个块内包含残差连接以稳定训练。整个网络不含任何池化层或显式的多尺度结构——空间支持的层次化完全由不同通道的学习扩散时间自动实现。

**训练与推理路径**：训练时，网络输入为逐顶点坐标（或 HKS 等预计算特征），通过多个 DiffusionNet Block 逐层处理，最终输出逐顶点预测（分割、对应等）。推理时，由于扩散操作仅依赖拉普拉斯算子，网络可直接应用于与训练集不同离散化的网格、不同分辨率的模型，甚至点云（通过从点云构建拉普拉斯矩阵）。图 3 展示了这一能力：在网格上训练的网络可直接在点云上评估并保持准确分割。

### Changed Slots：相对于基线方法的三个关键改变

**Slot 1：空间信息传播方式**。基线方法使用显式卷积（如 MeshCNN 的边卷积、SplineCNN 的样条卷积）或基于图邻域的聚合，这些操作将网格连接性硬编码到计算图中。DiffusionNet 将其替换为可学习扩散时间的各通道独立热扩散层。因果效应：扩散方程的解仅依赖于底层连续几何，使网络自动获得离散化鲁棒性；可学习时间消除了手工设定感受野大小的需求。

**Slot 2：多尺度/池化策略**。基线方法依赖池化层次结构（如网格简化）或手工选择不同大小的卷积核来获取多尺度信息。DiffusionNet 完全移除了池化操作，通过不同通道学习不同扩散时间实现从局部到全局的连续空间支持。因果效应：避免了池化带来的信息损失和实现复杂性；网络可在全分辨率模型上直接训练（图 2），无需简化预处理。

**Slot 3：方向滤波器实现**。基线方法通过等变卷积、旋转对齐或仅使用径向滤波器来处理方向信息。DiffusionNet 利用空间梯度特征的内积（经学习旋转/缩放）构造方向敏感特征，同时保持对局部切空间基选择的不变性。因果效应：无需显式定义切平面方向或进行旋转对齐；通过复矩阵或实矩阵的选择，可在方向感知与法线一致性要求之间灵活权衡。

### 表达能力的理论支撑

扩散后接逐点 MLP 的组合被证明可以表达丰富的径向滤波器族——任何可表示为拉普拉斯算子函数的滤波器都可由该架构近似。引入梯度特征后，表达空间进一步扩展至方向滤波器（图 6 可视化了学习到的径向与方向滤波器）。这一设计使得 DiffusionNet 在保持架构简洁性的同时，具备了与复杂卷积网络相当的表达能力。

![[assets/figures/papers/paper_list_l24_https_nmwsharp_com_research_diffusion_net/figures/008_Figure_7.jpg]]
*Figure 7: We present DiffusionNet, a simple and effective architecture for learning on surfaces. It is composed of successive identical DiffusionNet blocks. Each block diffuses every feature for a learned time scale, forms spatial gradient features, and applies a spatially shared pointwise MLP at each vertex in a mesh/point cloud/etc. These networks achieve state-of-the-art performance on surface learning tasks without any explicit surface convolutions or pooling hierarchies, in part because they automatically optimize for variable spatial support (see e.g., Figure 4)*

## 实验与关键发现

### 主要任务性能

DiffusionNet 在多个表面学习基准上取得最优或接近最优的结果，同时保持架构的简洁性。

**SHREC11 分类（Table 1）**：在 30 类形状分类任务上，DiffusionNet 仅使用每类 10 个训练样本即达到近乎完美的准确率（99.5%），显著优于 MeshCNN（98.6%）、SplineCNN（97.5%）等方法。值得注意的是，DiffusionNet 直接在全分辨率网格上训练和测试，而部分基线方法（以 † 标记）需依赖简化模型。

**RNA 分割（Table 2）**：在 RNA 分子分割任务上，DiffusionNet 以原始网格坐标（xyz）作为输入时达到 90.6% 的准确率，优于所有网格和点云基线方法。关键优势在于该方法可直接应用于原始网格，无需简化处理，从而保留了分子表面的细节信息。定性结果（Fig. 8）显示，DiffusionNet 在网格和采样点云上均能产生准确的分割结果。

**非刚性对应（Fig. 9, Table 5）**：在 FAUST 顶点标注对应任务上，DiffusionNet 在原始测试网格上达到 0.33 的平均测地误差（×100，经测地直径归一化），而次优方法 HSN 的误差为 9.57。在跨数据集泛化场景（SCAPE 训练，FAUST 测试）中，DiffusionNet 是唯一保持合理对应质量的方法，其他方法因过拟合训练网格连接性而完全失效。

### 离散化鲁棒性：核心实验

Table 5 的离散化鲁棒性实验是支撑论文核心主张的关键证据。实验设置：所有方法在 FAUST 模板网格上训练，然后在三种不同离散化版本的测试集上评估：

![[assets/figures/papers/paper_list_l24_https_nmwsharp_com_research_diffusion_net/figures/017_Table_5.jpg]]
*Table 5: DiffusionNet automatically retains highly accurate results under changes in meshing and sampling, while many other approaches overfit to mesh connectivity. Here we give correspondence errors on our remeshed FAUST dataset after training on template meshes, measured in mean geodesic distance ×100 after normalizing by the geodesic diameter*

![[assets/figures/papers/paper_list_l24_https_nmwsharp_com_research_diffusion_net/figures/015_Figure_11.jpg]]
*Figure 11: Accuracy curves for vertex-labelling correspondence on the FAUST dataset, as in Table 5. The first plot gives accuracy on the original test meshes, and the subsequent plots denote testing on our remeshed variants of the test set. For each plot, the x-axis is the geodesic error ×100 after normalizing by geodesic diameter, and the y-axis is the percent of predicted correspondences within that error*

| 测试网格类型 | DiffusionNet | HSN | ACSCNN | SplineCNN | MeshCNN |
|-------------|-------------|-----|--------|-----------|---------|
| 原始网格 | **0.33** | 9.57 | 1.00 | 2.11 | 1.56 |
| 各向同性重剖分 | **0.68** | 20.01 | 9.74 | 10.41 | 2.95 |
| 密集重采样 | **0.62** | 24.84 | 9.11 | 10.89 | 4.96 |

在重剖分和重采样条件下，DiffusionNet 的误差仅从 0.33 略微上升至 0.68 和 0.62，而所有基线方法的误差均剧烈增加。HSN 从 9.57 退化至 24.84，ACSCNN 从 1.00 退化至 9.74。这一对比直接验证了扩散层对离散化无关性的因果作用：基于显式卷积或邻域聚合的方法深度耦合网格连接性，而扩散过程仅依赖拉普拉斯算子这一几何先验，对具体离散化方案天然鲁棒。

Fig. 11 的准确率曲线进一步揭示：在原始网格上，DiffusionNet 和 ACSCNN 的曲线接近；但在重剖分网格上，ACSCNN 的曲线显著右移（误差增大），而 DiffusionNet 的曲线几乎不变。

### 表示迁移：网格训练 → 点云评估

Fig. 3 最后一列展示了一个独特的能力：DiffusionNet 可在网格上训练后直接在点云上评估，并保持准确的分割结果。相比之下，SplineCNN 和 ACSCNN 在训练网格上表现良好，但无法泛化到不同表示。这一能力源于扩散运算仅需拉普拉斯算子，而拉普拉斯算子可从点云近似构建。需注意，从网格到点云的迁移仍存在一定性能差距，这是方法的一个实际边界。

![[assets/figures/papers/paper_list_l24_https_nmwsharp_com_research_diffusion_net/figures/003_Figure_3.jpg]]
*Figure 3: Although past methods have achieved high-accuracy benchmark results for learning on meshes [Fey et al. 2018; Li et al. 2020b], they are prone to over-fitting to the mesh connectivity, rather than learning the underlying shape structure (Section 5.4). In contrast, DiffusionNet learns an accurate representation-agnostic solution, which even supports training on meshes and evaluating on a point cloud (last column)*

### 消融研究（Table 7）

![[assets/figures/papers/paper_list_l24_https_nmwsharp_com_research_diffusion_net/figures/021_Table_7.jpg]]
*Table 7: An ablation study, evaluated on the human segmentation task. Omitting any of the components of our method leads to a significant drop in performance. Manually fixing a non-optimal diffusion time also impairs performance—our learned procedure automatically optimizes a diffusion time for each channel*

在人分割任务上的组件消融揭示了各模块的因果贡献：

| 配置 | 准确率 |
|------|--------|
| 完整 DiffusionNet | **90.6%** |
| 移除扩散层 | 31.4% |
| 固定扩散时间 t=0.1 | 89.1% |
| 移除梯度特征 | 84.1% |

**移除扩散层**导致准确率从 90.6% 骤降至 31.4%，降幅达 59.2 个百分点。这直接证明空间信息传播是该架构的核心能力，逐点 MLP 单独无法捕获形状结构。

**固定扩散时间**（t=0.1）使准确率降至 89.1%，说明可学习的通道级扩散时间是架构的重要设计选择。Fig. 4 可视化展示了学习到的扩散时间分布：浅层块主要使用局部扩散（小 t），深层块中某些通道学习到近全局的支持（大 t），自动形成了从局部到全局的多尺度感受野，无需手工设计池化层次。

**移除梯度特征**使准确率降至 84.1%，降幅 6.5 个百分点。这验证了方向滤波器对分割任务的贡献。Fig. 6 的可视化显示，仅使用扩散+MLP 时网络学习径向对称滤波器，引入梯度特征后扩展为方向敏感滤波器，同时保持对局部切平面基选择的不变性。

### 谱基尺寸敏感性（Fig. 13）

谱加速方案使用截断的特征基近似扩散运算。实验表明：当特征向量数量少于 64 时，性能显著下降；128 个特征向量是安全默认值，在所有实验中使用。这一发现为实际部署提供了参数选择指导。

### 运行效率（Table 6）

在运行时间方面，DiffusionNet 展现出良好的可扩展性。对于中等规模网格（约 5K 顶点），单次推理约需 15ms；对于大规模网格（约 200K 顶点），推理时间约 200ms。相比之下，ACSCNN 和 HSN 在大网格上内存或时间开销过高（表中标记为“—”）。预处理阶段（拉普拉斯特征分解）为一次性开销，在训练和推理中均摊。

### 失败模式与适用边界

**非连通组件（Fig. 12）**：扩散无法在几何上不连通的组件之间传播信息，导致分割错误。这是扩散机制的本质限制——热扩散仅沿连通域传播。对于包含多个不连通组件的形状，该方法需要额外的组件间通信机制。

**法线一致定向要求**：利用梯度特征的旋转能力（用于区分左右等方向）要求网格法线一致定向。若法线方向不一致，需退化为仅使用缩放的实矩阵版本，此时网络丧失方向敏感性但仍可工作（Fig. 5 对比左右两列）。

**表示迁移的性能差距**：虽然支持网格到点云的迁移，但性能并非完全等同。在需要极高精度的场景下，建议在目标表示上进行微调。

**极大规模形状**：对于顶点数超过百万级别的形状，拉普拉斯特征分解的预处理开销可能成为瓶颈，尽管推理阶段仍保持高效。

### 实验公平性说明

所有实验统一使用 Adam 优化器（学习率 0.001，batch size 1，标准衰减策略）。在分割任务中报告了软真实值变体以确保与先前工作的公平比较。重网格化实验使用相同数据集的模板网格训练，确保离散化鲁棒性评估的公平性。

![[assets/figures/papers/paper_list_l24_https_nmwsharp_com_research_diffusion_net/figures/004_Figure_4.jpg]]
*Figure 4: We propose to learn a diffusion time for each feature channel, automatically tuning spatial support during training. The histograms show the learned times at each block in a DiffusionNet trained for segmentation; the times marked by the dashed lines are visualized by diffusing a point source from the starred point. The first block uses mainly local diffusion, while a channel in the last block finds nearly global support*

## 定位与知识库关联

DiffusionNet 的核心定位在于将表面学习的**空间信息传播 slot** 从显式离散卷积替换为连续扩散过程，从而解耦学习与几何离散化。现有方法如 **MeshCNN**（Hanocka et al., TOG 2019）依赖边折叠池化和固定拓扑的边卷积，**SplineCNN**（Fey et al., CVPR 2018）依赖样条基的显式坐标卷积，**HSN**（Wiersma et al., NeurIPS 2020）依赖切平面旋转等变设计——这些方法共同的问题是：学习到的特征提取器与训练时的具体网格连接性、采样密度强绑定，重剖分或改变采样后性能急剧退化（对应误差从 0.33 升至 9.57 甚至更高，Table 5）。DiffusionNet 通过将空间通信建模为 $h_t(u) := (M + tL)^{-1} M u$ 或谱域 $e^{-\lambda_i t}$ 缩放，将“邻域大小”这一离散概念替换为连续、可学习的扩散时间 $t$，从而在**多尺度/池化 slot** 上取消了手工设计的池化金字塔，使感受野自适应地从局部到全局连续变化（Fig. 4）。

在**方向滤波器 slot** 上，DiffusionNet 与 **HSN** 等旋转等变方法形成对比。HSN 通过显式构造旋转等变基实现方向敏感，但需要一致的局部坐标系或法线定向。DiffusionNet 则利用空间梯度特征的内积 $g_v := \mathrm{tanh}(\mathrm{Re}(\overline{w}_v \odot A w_v))$（Eq. 6），通过学习矩阵 $A$ 的旋转或缩放，在保持切平面基不变性的同时获得方向滤波能力（Fig. 5, Fig. 6）。这一设计的边界条件是：若使用旋转版本则要求法线一致定向，否则需退化为仅缩放的实矩阵版本。

**知识库挂载点**：DiffusionNet 应挂载在“几何深度学习—表面学习—离散化无关方法”分支下。其上游连接包括：(1) 谱几何处理的理论基础（Laplace-Beltrami 算子、热核、functional maps 框架），(2) 点云网络如 **PointNet/++**（Qi et al., CVPR 2017）和 **DGCNN**（Wang et al., TOG 2019）的逐点 MLP + 空间通信范式，(3) 热扩散作为平滑算子的经典几何处理。DiffusionNet 的关键创新在于将扩散时间参数化、可学习化，并与梯度特征结合构成完整的表面学习模块——这一点在谱方法中并不常见（谱方法通常将谱系数作为特征直接学习，而 DiffusionNet 明确不学习谱系数，仅用谱基加速扩散计算）。

**适用边界**：(1) 扩散在几何不连通的组件之间无法通信，导致分割错误（Fig. 12），这是热扩散本身的物理限制；(2) 依赖拉普拉斯矩阵 $L$ 和质量矩阵 $M$ 的预计算，对极大规模网格（百万级以上顶点）的谱分解可能成为瓶颈；(3) 从网格训练到点云评估虽可行（Fig. 3），但存在性能差距，说明离散化无关并非完全无损；(4) 谱基截断到 128 维是经验安全默认值，少于 64 维时性能显著下降（Fig. 13）。

**后续启发**：(1) 将可学习扩散时间解释为注意力机制：每个通道的 $t$ 本质上控制了空间注意力的范围，这为连接扩散网络与 Transformer 类架构提供了理论桥梁；(2) 扩散层可替代图神经网络中的消息传递步骤，用于分子图、社交网络等非几何图数据；(3) 将扩散网络与生成模型结合（如扩散模型本身），用于形状生成或补全；(4) 引入跨组件的虚拟边或图内边机制解决不连通组件问题，扩展适用场景。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/DiffusionNet_Discretization_Agnostic_Learning_on_Surfaces.pdf]]