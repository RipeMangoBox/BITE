---
title: "Neural Fields as Learnable Kernels for 3D Reconstruction"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/Neural_Fields_as_Learnable_Kernels_for_3D_Reconstruction.pdf
code_link: null
project_link: https://research.nvidia.com/labs/toronto-ai/nkf/
aliases:
- NKFN
- NFALK3R
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "学习一个数据依赖的核函数，其核岭回归的解是凸的且天然插值输入点；核参数由输入点云条件化，从而将灵活的归纳偏置注入重建。"
primary_logic: "将三维重建分解为学习核参数的骨干网络和在线核岭回归两部分：骨干网络提供适应数据的核特征，核岭回归通过简单的凸优化保证输出完全尊重输入点，实现高精度且强泛化的重建。"
claims:
- "在 ShapeNet 无噪声重建上，NKF 的 IoU 达到 0.949，显著优于最强基线 Conv-OccNet* 的 0.823，提升约 15.3%。"
- "在类别外泛化实验中（训练 6 类，测试 7 类），NKF 的 IoU 仅下降 1.1%（0.949→0.938），而 OccNet 下降 20.4%，Conv-OccNet* 下降 4.9%，证明 NKF 的强泛化能力。"
- "NKF 在 ScanNet 真实场景重建中，Chamfer 距离为 0.032，比次优方法（SPSR/NS 的 0.060）降低了近一半。"
- "点密度泛化实验中，NKF 在稀疏和密集采样下均保持高性能，且训练-测试密度不一致时无性能衰减，体现其核插值带来的点密度鲁棒性。"
---

# Neural Fields as Learnable Kernels for 3D Reconstruction

> [!tip] 核心洞察
> 将三维重建分解为学习核参数的骨干网络和在线核岭回归两部分：骨干网络提供适应数据的核特征，核岭回归通过简单的凸优化保证输出完全尊重输入点，实现高精度且强泛化的重建。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 神经场作为可学习核用于三维重建 |
| 英文题名 | Neural Fields as Learnable Kernels for 3D Reconstruction |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2111.13674) · [Project](https://nv-tlabs.github.io/nkf) · [Project](https://research.nvidia.com/labs/toronto-ai/nkf/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Neural Kernel Fields (NKF) |
| Dataset | ShapeNet (13 类) 单物体重建（无噪声）, ShapeNet 部分点云完成, 类别外泛化（训练 6 类，测试 7 类）, ScanNet 真实场景重建（10k 输入点） |

> [!tip] 效果简介
> - ShapeNet (13 类) 单物体重建（无噪声） 上，IoU 为 0.949，对比 0.823 (C-OccNet*)，变化 +0.126。
> - ShapeNet 部分点云完成 上，IoU 为 0.819，对比 0.770 (C-OccNet*)，变化 +0.049。
> - 类别外泛化（训练 6 类，测试 7 类） 上，IoU 为 0.938，对比 0.785 (C-OccNet*)，变化 +0.153。

## 概要

从稀疏或噪声点云重建三维形状是计算机视觉的核心任务。现有方法在设计空间上呈现出两个极端：数据无关方法（如 **SPSR** [Kazhdan & Hoppe 2013]、**Neural Splines** [Williams et al. 2022]）严格尊重输入点，但其固定的简单先验无法补全缺失区域；数据驱动的前馈方法（如 **OccNet** [Mescheder et al. 2019]、**Conv-OccNet** [Peng et al. 2020]）能从数据中学习强先验，却倾向于“检索”而非“重建”，在分布外输入上会丢失细节甚至不忠实于输入点。局部测试时优化方法（如 **LIG** [Jiang et al. 2020]）则对超参数敏感，易陷入不良局部最优。

**Neural Kernel Fields (NKF)** 通过一个关键洞察弥合了这一分歧：将重建问题分解为两个部分——一个从数据学习核参数的骨干网络，和一个在线求解的核岭回归。核岭回归的解是凸的，天然插值输入点，从而保证对观测的忠实性；而核参数由输入点云条件化，使模型能将灵活的归纳偏置注入重建过程。这种“学习核、求解凸问题”的范式同时获得了数据先验的表达力和测试时优化的保真度。

在 ShapeNet 无噪声重建上，NKF 的 IoU 达到 0.949，显著优于最强基线 Conv-OccNet* 的 0.823（提升约 15.3%）。在类别外泛化实验中（训练 6 类、测试 7 类），NKF 的 IoU 仅下降 1.1%（0.949→0.938），而 OccNet 下降 20.4%，Conv-OccNet* 下降 4.9%，展现出极强的泛化能力。在 ScanNet 真实场景重建中，NKF 的 Chamfer 距离为 0.032，比次优方法降低了近一半。此外，NKF 对输入点密度变化具有鲁棒性，在训练-测试密度不一致时无性能衰减，体现了核插值带来的天然优势。



从稀疏点云重建三维表面是计算机视觉与图形学中的核心任务。给定一组可能带有噪声的输入点及其法线，目标是恢复一个连续、封闭且细节丰富的隐式表面。这一问题的根本挑战在于：如何同时利用数据驱动的形状先验来补全缺失区域，又严格尊重输入观测点的几何信息。

### 现有方法的两个极端

当前主流的隐式重建方法在设计空间上呈现出两个极端（参见 Figure 3 的方法分类学）：

**数据驱动的前馈方法**（如 **OccNet** 和 **Conv-OccNet**）通过学习强大的形状先验取得了显著进展。这些方法利用大规模三维数据集训练神经网络，能够从部分观测中推断出合理的完整形状。然而，它们的本质缺陷在于倾向于"检索"而非"重建"——网络记忆了训练分布中的形状模式，当输入点与记忆模式不完全匹配时，输出可能偏离输入观测，导致细节丢失或几何失真。如 Figure 2 所示，前馈方法在处理略微偏离训练分布的独木舟时，会遗漏关键的板条结构。

**数据无关的方法**（如 **SPSR** 和 **Neural Splines**）则走另一条路。它们不依赖任何训练数据，而是通过求解纯粹的几何优化问题（如泊松重建或核插值）来拟合输入点。这类方法天然保证输出表面严格通过输入点，但其固定的先验假设（如平滑性）过于简单，无法在缺失区域生成合理的几何结构。Figure 2 中，这些方法虽然尊重了输入点，却无法完成部分形状的缺失部分。

### 核心瓶颈

上述两极分化揭示了一个深层瓶颈：**现有方法无法在"利用数据先验"与"忠实于输入观测"之间取得有效平衡**。前馈方法拥有强大的数据先验，但牺牲了对输入点的忠实度；数据无关方法保证了插值精度，却缺乏足够强的归纳偏置来完成缺失区域。局部测试时优化方法（如 **LIG**）试图在局部窗口内融合两者，但引入了新的脆弱性——对块大小高度敏感，且容易陷入不良局部极小值，产生凹凸不平的伪影（Figure 2 底行）。

### 本文动机

本文的核心洞察是：可以将三维重建分解为两个正交的子问题——**学习核参数的骨干网络**和**在线核岭回归**。骨干网络从数据中学习一个条件于输入点云的正定核函数，将灵活的归纳偏置注入重建过程；而核岭回归作为凸优化问题，天然保证输出隐式场在输入点处满足约束。这种分解使得方法同时具备前馈方法的强先验和数据无关方法的插值保真度，从根本上弥合了两者之间的鸿沟。



## 核心方法与创新机理

### 问题瓶颈：先验利用与输入忠实性的两难

三维重建方法长期面临一个根本性张力：**数据驱动方法**（如 OccNet、Conv-OccNet）能够从大规模数据中学习强先验，从而完成缺失几何的合理推断，但其前馈预测本质倾向于“检索”训练记忆，在分布外输入上容易偏离实际观测点；而**数据无关方法**（如 Neural Splines、SPSR）通过固定核或光滑性先验严格插值输入点，忠实性极高，但其过于简单的归纳偏置无法完成缺失区域的合理补全。这一“先验强度—输入忠实性”的权衡构成了领域核心瓶颈。

NKF 的核心洞察在于：**将重建问题分解为两个正交的子问题**——（1）一个从数据学习核参数的骨干网络，负责注入灵活的归纳偏置；（2）一个在线的核岭回归求解器，通过凸优化天然保证输出严格插值输入点。这种分解使得方法同时获得了数据先验的补全能力和对输入点的完全忠实性。

### 关键机制：数据依赖的可学习核

NKF 的方法创新集中体现在一个**changed slot**上——将 Neural Splines 的固定核替换为数据依赖的可学习核：

$$
K_{(\mathcal{X},\theta)}(\pmb{x}, z) = K_{\mathrm{NS}}([\pmb{x} : \phi(\pmb{x}|\mathcal{X},\theta)], [z : \phi(z|\mathcal{X},\theta)])
$$

其中 $\phi(\cdot|\mathcal{X},\theta)$ 是由 3D U-Net 骨干网络为每个点提取的特征向量，$K_{\mathrm{NS}}$ 是 Neural Splines 的固定正定核。这一设计的精妙之处在于：

- **核函数本身保持正定性**，因此后续的核岭回归仍然是凸优化问题，系数求解通过正定线性系统 $\pmb{\alpha} = (\pmb{G} + \lambda \pmb{I})^{-1}\pmb{y}$ 具有唯一全局最优解，天然保证对输入点的插值性质。
- **特征 $\phi$ 由数据驱动学习**，将坐标空间提升到特征空间后，核的相似度度量不再是纯粹的欧氏距离，而是融入了从训练数据中习得的语义相似性——这正是归纳偏置的注入点。
- **核参数与求解过程解耦**：骨干网络只负责预测核参数（特征），无需直接输出占据场；而核岭回归在推理时在线求解，保证了对任意输入点云的适应能力。

### 与基线方法的本质差异

从方法谱系来看，NKF 占据了独特的生态位（见 Figure 3 的分类框架）：

| 方法 | 先验来源 | 优化方式 | 对输入点的忠实性 |
|------|----------|----------|------------------|
| Neural Splines | 固定核（无数据先验） | 测试时核岭回归 | 完全插值 |
| OccNet | 全局隐式网络（学习先验） | 前馈预测 | 可能偏离 |
| Conv-OccNet | 局部卷积特征（学习先验） | 前馈预测 | 可能偏离 |
| LIG | 局部隐式网络（学习先验） | 测试时局部优化 | 局部忠实，但易陷入局部极小 |
| **NKF** | **可学习核（数据先验）** | **测试时全局核岭回归** | **严格插值** |

NKF 的关键优势在于：**凸优化求解器保证了全局最优和输入忠实性**，而**可学习核提供了数据驱动的强先验**。这一组合在实验中得到充分验证——在类别外泛化实验中（Table 3），NKF 的 IoU 仅从 0.949 降至 0.938（下降 1.1%），而 OccNet 下降 20.4%，Conv-OccNet* 下降 4.9%，证明核岭回归的凸性有效避免了前馈方法的过拟合倾向。

### 去噪的拓展：加权核岭回归

NKF 进一步将基础框架拓展到噪声场景，引入逐点权重矩阵 $\pmb{W}$ 的加权核岭回归：

$$
\pmb{\alpha} = (\pmb{W}\pmb{G}\pmb{W} + \lambda \pmb{I})^{-1}\pmb{W}\pmb{y}
$$

其中权重由骨干网络预测，用于抑制噪声点的贡献。这一设计保持了凸优化的良好性质，同时赋予方法对传感器噪声的鲁棒性（见 Figure 5 的消融对比）。

### 训练监督的创新

与 Neural Splines 的无监督核岭回归不同，NKF 通过端到端训练学习核参数，损失函数结合了体积交叉熵和表面 L1 损失：

$$
L(f) = \sum_{i=1}^{|X_{\mathrm{vol}}|} \mathrm{BCE}(f(\pmb{x}_i^{\mathrm{vol}}), y_i^{\mathrm{vol}}) + \lambda_{L1} \sum_{i=1}^{|X_{\mathrm{surf}}|} |f(\pmb{x}_i^{\mathrm{surf}})|
$$

表面 L1 损失的引入（消融实验 Table 5 验证其贡献）使得隐式场在表面附近更精确地归零，从而提升重建精度。这一监督信号通过核岭回归的解析梯度反向传播至骨干网络，形成端到端的可微管线。



Neural Kernel Fields (NKF) 将三维重建问题分解为两个互补的阶段：**预测阶段**与**评估阶段**，分别对应“学习核参数”与“在线核岭回归”两个核心模块。这一分解使得模型能够同时利用数据驱动的归纳偏置和核方法的凸优化性质，在忠实尊重输入点的同时实现强泛化重建。

### 预测阶段：从点云到隐式函数

预测阶段的输入为带法线的有向点云 $\mathcal{X}$，其目标是输出一个完整的隐式函数，该函数由两部分构成：

1. **特征函数 $\phi(\cdot|\mathcal{X},\theta)$**：将三维空间中的任意点映射到 $d$ 维特征空间。该函数由一个骨干网络实现，包含 PointNet 和 3D U-Net 结构（Figure 4）。输入点云首先被离散化为体素网格，经过 3D U-Net 提取多尺度特征后，通过三线性插值获得每个查询点的特征向量。

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2111_13674/figures/007_Figure_4.jpg]]
*Figure 4: Our method works in two stages: (1) prediction (Top row) where we predict an implicit function from an input point cloud, and (2) evaluation (Bottom row) where we evaluate the implicit function. Our predicted implicit consists of a feature function φ which lifts points in the volume to features in $\mathbb { R } ^ { d }$ , and a set of coefficients α, which are used to encode the function as a linear combination of basis functions centered at the input points*

2. **基函数系数 $\boldsymbol{\alpha}$**：用于将隐式场表示为以增强点为中心的核基函数的线性组合。系数通过求解一个正定线性系统获得：
   $$\boldsymbol{\alpha} = (\boldsymbol{G}(\boldsymbol{\chi},\theta) + \lambda \boldsymbol{I})^{-1} \boldsymbol{y}$$
   其中 $\boldsymbol{G}$ 为数据依赖核矩阵，$\boldsymbol{y}$ 为增强点上的目标值（输入点处为 0，正负增强点处分别为 $\pm\epsilon$），$\lambda$ 为正则化参数。

### 评估阶段：从隐式函数到占据场

评估阶段对任意查询点 $\boldsymbol{x}$ 计算隐式场值，通过核加权和实现：
$$f(\boldsymbol{x}) = \sum_{\boldsymbol{x}_j' \in X'} \alpha_j K_{(\boldsymbol{\chi},\theta)}(\boldsymbol{x}, \boldsymbol{x}_j')$$
其中 $K_{(\boldsymbol{\chi},\theta)}$ 为数据依赖核，其核心设计是将坐标与学习特征拼接后应用 Neural Spline 核：
$$K_{(\mathcal{X},\theta)}(\boldsymbol{x}, z) = K_{\mathrm{NS}}([\boldsymbol{x} : \phi(\boldsymbol{x}|\mathcal{X},\theta)], [z : \phi(z|\mathcal{X},\theta)])$$

这一核构造方式使得核的度量不仅依赖于空间距离，还依赖于由骨干网络学到的语义特征相似性，从而将灵活的归纳偏置注入重建过程。

### 可选去噪模块

当输入点云含有噪声时，NKF 引入逐点权重预测模块，通过加权核岭回归抑制噪声点的影响：
$$\boldsymbol{\alpha} = (\boldsymbol{W} \boldsymbol{G} \boldsymbol{W} + \lambda \boldsymbol{I})^{-1} \boldsymbol{W} \boldsymbol{y}$$
其中 $\boldsymbol{W}$ 为对角权重矩阵，由网络预测每个输入点的重要性。如 Figure 5 所示，加权回归能有效平滑噪声点产生的表面凸起，产生更精确的重建结果。

### 训练与推理流程

整个框架端到端训练，监督信号结合体积交叉熵损失和表面 L1 损失：
$$L(f) = \sum_{i=1}^{|X_{\mathrm{vol}}|} \mathrm{BCE}(f(\boldsymbol{x}_i^{\mathrm{vol}}), y_i^{\mathrm{vol}}) + \lambda_{L1} \sum_{i=1}^{|X_{\mathrm{surf}}|} |f(\boldsymbol{x}_i^{\mathrm{surf}})|$$

推理时，给定输入点云，骨干网络前向传播一次得到特征函数和系数，随后可对任意查询点评估隐式场。值得注意的是，核岭回归的求解是凸优化问题，保证了解的唯一性和对输入点的天然插值性质，这是 NKF 在点密度泛化和类别外泛化实验中表现优异的关键原因（Figure 9, Table 3）。

### 与基线方法的架构差异

相较于 Neural Splines（固定核、无学习先验），NKF 将核函数从仅依赖坐标扩展为数据依赖的“坐标+特征”拼接核（**changed_slot: 核函数**）。相较于 OccNet 和 Conv-OccNet 等前馈方法，NKF 不直接回归占据场，而是通过核岭回归显式求解系数，从而保证输出对输入点的忠实性。这一架构选择使得 NKF 在方法谱系中占据独特位置：既非纯粹的数据无关方法，也非纯粹的前馈方法，而是二者的融合（Figure 3）。



NKF 的核心思想是将三维重建分解为两个阶段：**预测阶段**由骨干网络学习数据依赖的核参数，**评估阶段**通过核岭回归在线拟合输入点。以下按流水线顺序阐述关键模块与核心公式。

### 1. 增强点对构造（继承自 Neural Splines）

NKF 继承了 Neural Splines 的增强点对机制，将法线约束转化为有限差分形式。给定输入点 $x_i$ 及其法线 $n_i$，构造正负增强点：

$$x_i^+ = x_i + \epsilon n_i, \quad x_i^- = x_i - \epsilon n_i$$

其中 $\epsilon$ 是一个小步长。这些增强点将法线匹配转化为对隐式场值的直接约束：要求 $f(x_i^+) \approx \epsilon$，$f(x_i^-) \approx -\epsilon$，$f(x_i) \approx 0$。由此得到 Neural Splines 的有限差分损失：

$$L(f) = \sum_{i=1}^{S} |f(\pmb{x}_i)|^2 + |f(\pmb{x}_i^+) - \epsilon|^2 + |f(\pmb{x}_i^-) + \epsilon|^2$$

该损失的解析解可表示为以增强点为中心的核基函数的线性组合（见 Eq. (3)），为后续数据依赖核的引入奠定基础。

### 2. 特征提取网络 φ

骨干网络 $\phi(\cdot|\mathcal{X}, \theta)$ 负责从输入点云 $\mathcal{X}$ 中提取逐点特征，为核函数注入数据依赖的归纳偏置。其结构为 **PointNet + 3D U-Net**：

- 首先将增强点云离散化为体素网格；
- 使用 PointNet 对每个体素内的点进行局部编码；
- 通过 3D U-Net 进行上下文聚合，输出每个点的 $d$ 维特征 $\phi(x|\mathcal{X}, \theta)$。

该设计借鉴了 Conv-OccNet 的局部特征提取范式，但目的不同：Conv-OccNet 直接预测占据场，而 NKF 将这些特征作为核函数的条件输入。

### 3. 数据依赖核的构建

NKF 的核心创新在于将固定核 $K_{\text{NS}}$ 升级为**数据依赖核** $K_{(\mathcal{X},\theta)}$。具体做法是将点坐标与学习到的特征拼接后，再应用 Neural Spline 核：

$$K_{(\mathcal{X},\theta)}(\pmb{x}, z) = K_{\text{NS}}\big([\pmb{x} : \phi(\pmb{x}|\mathcal{X},\theta)], [z : \phi(z|\mathcal{X},\theta)]\big)$$

其中 $[\cdot : \cdot]$ 表示向量拼接。这意味着核的相似度度量不再仅依赖空间坐标，而是同时考虑由骨干网络提取的语义特征，从而将数据驱动的先验知识注入核岭回归框架。

### 4. 系数求解（核岭回归）

给定增强点集 $X'$ 和目标值向量 $\pmb{y}$（增强点对应 $\pm\epsilon$，原始点对应 $0$），隐式场表示为核基函数的线性组合。系数 $\pmb{\alpha}$ 通过求解以下正定线性系统获得：

$$\pmb{\alpha} = (\pmb{G}(\pmb{\chi}, \theta) + \lambda \pmb{I})^{-1} \pmb{y}$$

其中 $\pmb{G}$ 是核矩阵，$G_{ij} = K_{(\mathcal{X},\theta)}(x_i', x_j')$，$\lambda$ 为正则化系数。该系统的求解是**凸优化问题**，保证全局最优解，且天然满足输入点处的约束——这是 NKF 忠实于输入点的数学基础。

### 5. 隐函数评估

对于任意查询点 $\pmb{x}$，其占据场值通过核加权和计算：

$$f(\pmb{x}) = \sum_{\pmb{x}_j' \in X'} \alpha_j K_{(\pmb{\chi},\theta)}(\pmb{x}, \pmb{x}_j')$$

该式的计算复杂度与增强点数量 $|X'|$ 线性相关，与核矩阵求逆的 $O(N^3)$ 复杂度解耦。

### 6. 加权核岭回归（去噪模块）

为处理噪声输入，NKF 引入逐点权重矩阵 $\pmb{W} = \text{diag}(w_1, ..., w_{|X'|})$，将标准核岭回归扩展为加权形式：

$$\pmb{\alpha} = (\pmb{W}\pmb{G}\pmb{W} + \lambda \pmb{I})^{-1} \pmb{W}\pmb{y}$$

权重 $w_i$ 由一个小型子网络预测，学习识别并抑制噪声点对重建的贡献。如 Figure 5 所示，加权回归能有效平滑噪声点引起的表面凸起，产生更精确的重建表面。

### 7. 训练损失

整个框架通过端到端训练学习核参数 $\theta$。训练损失结合了体积交叉熵和表面 L1 损失：

$$L(f) = \sum_{i=1}^{|X_{\text{vol}}|} \text{BCE}\big(f(\pmb{x}_i^{\text{vol}}), y_i^{\text{vol}}\big) + \lambda_{L1} \sum_{i=1}^{|X_{\text{surf}}|} |f(\pmb{x}_i^{\text{surf}})|$$

第一项监督体积采样点的二分类占据预测，第二项鼓励表面附近点的隐式场值趋近于零。消融实验（Table 5）表明 L1 表面损失对性能有显著贡献。



## 实验与关键发现

### 核心实验设计

作者围绕三个关键维度展开实验评估：(1) **单物体重建**——在 ShapeNet 的 13 个类别上测试无噪声和带噪声的完整点云重建；(2) **部分点云补全**——从局部观测中恢复完整形状；(3) **泛化能力**——包括类别外泛化（训练 6 类、测试 7 类）和跨域泛化（ShapeNet→ScanNet 真实扫描场景）。所有基线方法在统一的输入点数量（1000 点）和噪声条件下评估，主要对比对象为使用增强点对的 **Conv-OccNet***（C-OccNet*），该变体与 NKF 的输入表示更具可比性。

### 主要定量结果

#### ShapeNet 单物体重建（Table 1）

在无噪声设定下，NKF 以 **0.949 的均值 IoU** 取得压倒性优势，比最强基线 C-OccNet* 的 0.823 提升了约 15.3%（+0.126）。在 Chamfer 距离（0.024 vs 0.037）和法线一致性（0.948 vs 0.934）上也全面领先。当加入高斯噪声（σ=0.005）时，NKF 的 IoU 仍保持 0.915，而 C-OccNet* 降至 0.789，差距进一步拉大至 0.126。这一结果表明，**核岭回归的凸优化机制使 NKF 在噪声扰动下仍能忠实于输入点**，而前馈方法则因缺乏显式拟合约束而性能衰减更剧烈。

#### 部分点云补全（Table 2）

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2111_13674/figures/011_Table_2.jpg]]
*Table 2: Object completion from partial point clouds*

在仅给定局部点云的补全任务中，NKF 的 IoU 达到 0.819，优于 C-OccNet* 的 0.770（+0.049）。值得注意的是，NKF 在 Chamfer 距离和法线一致性上与 C-OccNet* 持平或略优，但 IoU 的大幅领先说明其**重建的占据场更精确地贴合真实表面**，而非仅在外观轮廓上接近。

#### 类别外泛化（Table 3）

这是最能体现 NKF 方法论优势的实验。在训练 6 类、测试 7 类的设定下，NKF 的 IoU 仅从 0.949 降至 0.938（下降 1.1%），而 OccNet 从 0.731 骤降至 0.582（下降 20.4%），C-OccNet* 从 0.823 降至 0.785（下降 4.9%）。NKF 在未见类别上的 IoU（0.938）甚至超过 C-OccNet* 在**训练类别内**的表现（0.823）。这验证了核心设计假设：**将归纳偏置编码在可学习的核函数中，而非直接映射到输出空间，使得模型习得的是“如何重建”的通用策略，而非特定类别的形状先验**。

#### 极端泛化：单类训练（Table 6 和 Figure 11）










仅用椅子类别训练的 NKF 模型，在其余 12 个类别上测试时，IoU 仅比全类别训练模型下降约 0.01，且定性结果（Figure 11）显示其能合理重建汽车、步枪等结构迥异的物体。这进一步证实了核方法的强泛化本质。

#### ScanNet 真实场景重建（Table 4）

在从 ShapeNet 合成数据直接迁移到 ScanNet 真实扫描场景的跨域泛化测试中，NKF 在 10k 输入点设定下取得 **0.032 的 Chamfer 距离**，比数据无关方法 SPSR 和 Neural Splines 的 0.060 降低了近一半。这证明学习到的核特征在真实传感器噪声和稀疏采样下仍能提供有效的几何先验，同时核回归机制保证了对观测点的忠实拟合。

### 点密度鲁棒性（Figure 9）

NKF 在稀疏（100 点）到密集（10k 点）的宽输入密度范围内均保持高 IoU，且当训练与测试的点密度不一致时（如 1k 训练、100 测试），性能几乎无衰减。相比之下，前馈方法在训练-测试密度不匹配时性能显著下降。这一性质源于**核插值公式天然具有点密度无关性**——系数 α 的求解仅依赖输入点自身，查询点的场值通过核加权和得到，不依赖固定分辨率的网格或采样模式。

### 消融研究

#### L1 表面损失与特征维度（Table 5）

消融实验表明，L1 表面损失对性能有显著贡献：移除该损失项后 IoU 下降明显。此外，即使将特征维度降至 d=4，NKF 仍保持较高性能，说明核机制本身提供了强正则化，降低了对高维特征的依赖。

#### 噪声过滤与加权回归（Figure 10）

通过引入逐点权重矩阵 W 的加权核岭回归（Eq. 13），NKF 能有效抑制噪声点的贡献。Figure 10 的定性对比显示，未加权模型在噪声点附近产生凹凸伪影，而加权模型能平滑滤除这些扰动，产生更精确的表面。该去噪模块通过骨干网络预测每点的置信度权重，与核回归联合优化。

### 推理效率（Table 7）

在 ShapeNet 设定（1k 输入点、210 万评估点）下，NKF 的推理时间为 0.29 秒，其中核矩阵求解占主导。在 ScanNet 设定（10k 输入点、1690 万评估点）下，推理时间为 3.4 秒。核矩阵求解的 $O(N^3)$ 复杂度是当前实现的主要计算瓶颈，限制了最大输入点数约 1.2 万点。

### 失败模式与局限性

1. **有向点云依赖**：NKF 依赖带法线的输入点云来构建增强点对（$x_i^+$ 和 $x_i^-$），无法直接处理无向点云。对于缺乏法线的数据，需额外的法线估计模块，这引入了外部依赖和潜在的误差传播。

2. **核矩阵求解的规模限制**：$O(N^3)$ 的计算复杂度使当前实现无法处理超过约 1.2 万输入点的场景。虽然 Nyström 近似等稀疏化方法可缓解此问题，但尚未集成到框架中。

3. **大场景的泛化差距**：尽管在 ScanNet 上表现优于数据无关方法，但与在 ShapeNet 上的压倒性优势相比，跨域到真实大场景时性能提升幅度收窄，说明核特征在复杂场景几何中的表达能力仍有提升空间。

### 补充图表

![[assets/figures/papers/paper_list_l2_https_arxiv_org_abs_2111_13674/figures/004_Figure_2.jpg]]
*Figure 2: Comparison of our approach with methods along three Axes in Sec. 1. Top Row: Data free methods [35, 64] respect the input points but their simple fixed priors cannot complete the partial shape. Middle Row: Feed-forward methods [48, 48] learn from data, but miss the slats on the slightly out of distribution canoe. Bottom Row: LIG [33], a local method which performs test-time optimization, is very sensitive to the choice of patch size (0.3 left vs 0.1 middle), and gets stuck in bad local minima (bumpy artefacts)*



## 定位与知识库关联

### 1. 方法分类学定位

NKF 在三维隐式重建的设计空间中占据了一个独特位置。根据论文提出的分类学框架（Figure 3），现有方法沿三个轴分化：

- **轴1：先验来源**——数据无关（如 SPSR、Neural Splines）vs. 数据驱动（如 OccNet、Conv-OccNet、LIG）。
- **轴2：优化时机**——前馈推理 vs. 测试时优化。
- **轴3：重建粒度**——局部 vs. 全局。

NKF 的定位是**数据驱动的全局测试时优化方法**。这一组合在现有谱系中几乎是空白的：数据无关方法在测试时优化（如 Neural Splines）但缺乏学习先验，无法补全缺失部分；数据驱动的前馈方法（如 Conv-OccNet）学习强先验但倾向于检索而非忠实重建输入点；局部测试时优化方法（如 LIG）则对分块大小敏感且易陷入局部极小。NKF 通过将核岭回归作为凸的测试时优化步骤，同时将核参数的学习委托给数据驱动的骨干网络，实现了两者优势的融合。

### 2. 与基线方法的核心差异

**与 Neural Splines 的关系（继承与超越）**

NKF 直接继承了 Neural Splines 的核机器形式体系——将隐式场表示为以增强点为中心的核基函数线性组合，并通过求解线性系统获得系数。两者的本质差异在于核函数本身：

- **Neural Splines** 使用固定的核 $K_{\mathrm{NS}}$，仅依赖点坐标。这使其天然插值输入点，但固定的归纳偏置太弱，无法完成缺失部分的重建（Figure 2 顶行）。
- **NKF** 将核替换为数据依赖的 $K_{(\mathcal{X},\theta)}$，通过将坐标与学习特征拼接后应用 Neural Spline 核（Eq. 8），使核的等距度量由数据驱动定义。这保留了插值性质的同时注入了灵活的归纳偏置。

可以理解为：NKF 将 Neural Splines 从“固定度量空间中的核回归”升级为“可学习度量空间中的核回归”。

**与 Conv-OccNet 的关系（竞争与互补）**

Conv-OccNet 是数据驱动前馈方法的代表，与 NKF 共享部分架构组件（3D U-Net 特征提取），但根本机制不同：

- Conv-OccNet 将点特征直接解码为占据概率，是一个**检索式**过程——输出受训练分布约束，对分布外输入可能丢失细节（Figure 2 中行，独木舟的板条缺失）。
- NKF 将特征用于**构建核**，再由核岭回归在测试时求解隐式场。这个凸优化步骤保证输出通过输入点，实现**重建式**行为。

实验证据充分支撑这一机制差异：在类别外泛化实验中（Table 3），NKF 的 IoU 仅下降 1.1%（0.949→0.938），而 Conv-OccNet* 下降 4.9%，OccNet 下降 20.4%。这表明 NKF 的核插值机制提供了更强的分布外鲁棒性。

**与 LIG 的关系（局部优化 vs. 全局凸优化）**

LIG 采用局部测试时优化，将重建分解为重叠分块的独立优化。NKF 的全局核岭回归提供了两个关键优势：

1. **凸性保证**：核岭回归的解是唯一的全局最优，而 LIG 的局部优化可能陷入不良局部极小（Figure 2 底行显示凹凸伪影）。
2. **分块不敏感**：LIG 对分块大小极为敏感（Figure 2 底行，分块大小 0.3 vs. 0.1 产生截然不同的结果），NKF 无需此类超参数调优。

### 3. 适用边界与局限

**输入要求**

NKF 依赖带法线的有向点云。法线用于构造增强点对（正负 ε 偏移点），这是 Neural Splines 损失函数的要求（Eq. 2）。无法直接处理无向点云（如原始 LiDAR 扫描），需要外部法线估计或附加预测模块。这一约束继承自 Neural Splines 框架，但 NKF 并未提出解决方案。

**计算规模瓶颈**

核矩阵 $\mathbf{G}$ 的构建和求逆复杂度为 $O(N^3)$，其中 $N$ 为增强点数量（输入点数的 3 倍）。论文明确指出当前实现的最大输入点数约为 12,000。对于大规模场景重建（如完整 ScanNet 场景），这一限制是实质性的。论文提及 Nyström 采样可作为缓解方案，但尚未集成。

**训练数据依赖**

尽管 NKF 展现出强泛化能力，其核参数的训练仍需覆盖一定类别多样性的数据。在极端泛化实验中（仅用椅子训练，Figure 11），模型可泛化至其他 12 个类别，但性能略低于全类别训练模型。这表明核特征的学习仍受益于训练类别的覆盖度。

### 4. 开放问题

1. **大规模扩展**：如何利用 Nyström 采样或空间衰减将核求解器扩展到超过 12k 点？这是将 NKF 应用于大规模真实场景的关键工程挑战。

2. **无向点云处理**：如何将法线预测集成到方法中以处理无向点云？可能的路径包括联合训练法线预测模块，或设计不依赖增强点对的新损失形式。

3. **核设计的进一步探索**：当前核仅将坐标与特征拼接后应用 Neural Spline 核。是否存在更优的特征-坐标融合方式？特征空间的度量学习是否可进一步结构化？

4. **与 NeRF 类方法的融合**：NKF 的核机制天然支持连续场表示，与 NeRF 类方法的体渲染管线是否存在结合点？这可能在视图合成任务中开辟新方向。

5. **理论分析**：NKF 的泛化能力是否可从核方法理论（如表示定理、泛化界）获得更深入的解释？这有助于理解其分布外鲁棒性的理论根源。



## 原文 PDF

![[paperPDFs/CVPR_2022/Neural_Fields_as_Learnable_Kernels_for_3D_Reconstruction.pdf]]
