---
title: Learning Hierarchical Hyperbolic Mixture Model for Part-aware 3D Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_Hierarchical_Hyperbolic_Mixture_Model_for_Part_aware_3D_Generation.pdf
project_link: null
code_link: null
aliases:
- HHMMHHD
- LHHMMPA3G
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将径向噪声与角度噪声解耦，并引入缩放因子Λc根据半径自动调整角度噪声，以匹配双曲几何的指数增长特性。
primary_logic: 在双曲空间中，半径控制语义层次（由粗到细），角度控制同一层次内的语义变化；分离这两者并适配几何缩放，可以在扩散过程中保持层次结构的完整性。
claims:
- Isotropic Gaussian noise disrupts the structure of H2MM because the distance between two semantics in the semantic hierarchy is primarily determined by the radius.
- Any Euler update in the tangent space followed by the exponential map is formally equivalent to a Möbius update in the manifold.
- Performing larger initial splits yields better fitting quality, while using fewer splitting layers further improves the overall fit.
- ShapeNet 上 FID↓ = 10.39
---

# Learning Hierarchical Hyperbolic Mixture Model for Part-aware 3D Generation

> [!tip] 核心洞察
> 在双曲空间中，半径控制语义层次（由粗到细），角度控制同一层次内的语义变化；分离这两者并适配几何缩放，可以在扩散过程中保持层次结构的完整性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向部件感知3D生成的分层双曲混合模型学习 |
| 英文题名 | Learning Hierarchical Hyperbolic Mixture Model for Part-aware 3D Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Yang_Learning_Hierarchical_Hyperbolic_Mixture_Model_for_Part-aware_3D_Generation_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Hierarchical Hyperbolic Mixture Model (H2MM) with Hyperbolic Diffusion |
| Dataset | ShapeNet |

> [!tip] 效果简介
> - ShapeNet 上，FID↓ 10.39 vs 12.87 (DiffGS) (-2.48)。

## 概要

**问题瓶颈**：现有3D生成方法大多在欧几里得空间中建模，采用各向同性高斯噪声进行扩散。然而，当将这一范式迁移到双曲空间以捕捉3D物体的语义层次结构时，各向同性欧几里得噪声会破坏语义层次——因为双曲空间中径向和角度方向上的噪声尺度不匹配，导致边缘处的偏差被放大。这一瓶颈直接限制了在双曲流形上进行高质量部件感知3D生成的可能性。

**核心思路**：本文提出**分层双曲混合模型（Hierarchical Hyperbolic Mixture Model, H2MM）**，在Poincaré球模型的双曲空间中构建树形层次结构，将3D物体从全局隐变量分层划分为多个高斯原语。关键创新在于将扩散过程中的径向噪声与角度噪声解耦，并引入缩放因子 $\Lambda_c$ 根据半径自动调整角度噪声，以匹配双曲几何的指数增长特性。这一设计使得半径控制语义层次（由粗到细），角度控制同一层次内的语义变化，从而在扩散过程中保持层次结构的完整性。

**方法定位**：H2MM属于**双曲扩散生成模型**，在表示空间、噪声注入方式、扩散求解器和混合模型四个维度上对现有3D生成基线（如DiffGS、GaussianCube、HGMMSplatting）进行了系统性改进。其扩散求解器基于Möbius运算构建了高阶双曲扩散模型求解器（HDM-Solver），证明了切空间中的欧拉更新经指数映射后等价于流形上的Möbius更新。

**主要结果**：在ShapeNet数据集上，H2MM的FID达到10.39，相较于DiffGS的12.87降低了2.48。消融实验表明，角度噪声缩放因子 $\Lambda_c$ 是生成质量的关键保障（移除后FID从10.12恶化至14.26），而渐进式逐层生成策略进一步将FID降至9.73。



### 3D 生成中的语义结构瓶颈

3D 内容生成近年来取得了显著进展，扩散模型与高斯泼溅（Gaussian Splatting）的结合已成为主流范式。然而，现有方法在生成过程中普遍忽略了一个关键问题：**3D 物体的部件语义具有天然的层次结构**。一个物体由多个部件组成，每个部件又包含子部件，这种从粗到细的语义层次应当被生成模型显式建模。

现有方法如 **DiffGS**、**GaussianCube** 和 **HGMMSplatting** 均采用欧几里得空间中的高斯混合模型来表示 3D 形状，但这种表示存在根本性缺陷：欧几里得空间的平坦几何无法自然编码层次化的语义距离关系。在语义层次中，不同部件之间的相似度应当随层次深度呈指数级变化，而欧几里得空间的线性距离度量无法捕捉这种指数增长的结构。

### 双曲空间的几何优势与噪声困境

双曲空间（具体为 Poincaré 球模型）因其负曲率特性，天然适合建模层次结构——空间中两点间的距离随半径呈指数增长，恰好对应语义层次中由粗到细的指数级分化。这一几何特性使得双曲空间成为表示部件感知 3D 语义的理想选择。

然而，在双曲空间中执行扩散过程面临一个此前未被揭示的困境：**各向同性欧几里得噪声会破坏双曲空间中的语义层次结构**。具体而言，在双曲空间的极坐标表示中，半径方向控制语义层次的深度（由粗到细），角度方向控制同一层次内的语义变化。各向同性高斯噪声在径向和角度方向上施加相同尺度的扰动，但由于双曲几何的指数增长特性，边缘处的角度噪声会被不成比例地放大，导致语义层次边界的模糊和结构的崩塌。

### 本文动机与核心思路

本文的核心洞察在于：**在双曲空间中，半径与角度分别承载着不同性质的语义信息，必须在扩散过程中区别对待**。半径方向的扰动对应于跨层次的语义迁移（如从“椅子”到“扶手”），而角度方向的扰动对应于同层次内的语义变异（如不同风格的扶手）。分离这两类噪声，并根据双曲几何的局部缩放因子自适应调整角度噪声的强度，是在扩散过程中保持层次结构完整性的关键。

基于这一洞察，本文提出 **Hierarchical Hyperbolic Mixture Model (H2MM)** 与配套的 **Hyperbolic Diffusion** 框架，将 3D 生成从欧几里得空间迁移到双曲流形上，通过解耦的径向-角度噪声注入和基于 Möbius 运算的高阶扩散求解器，实现在扩散生成全过程中对部件语义层次结构的保持。



## 核心方法与创新机理

本工作围绕一个根本性的瓶颈展开：**在双曲空间中，各向同性欧几里得噪声会破坏语义层次结构**。具体而言，在 Poincaré 球模型中，半径方向控制语义的层次（由粗到细），而角度方向控制同一层次内的语义变化；由于双曲几何的指数增长特性，径向与角度方向上的噪声尺度天然不匹配，导致边缘处的偏差被持续放大（Figure 1）。这一发现构成了全文的因果调节旋钮。

为解决上述问题，本文提出 **Hierarchical Hyperbolic Mixture Model (H2MM)** 并配套设计了一套双曲扩散框架。与现有 3D 生成基线相比，该方法在以下四个关键 slot 上做出了根本性改变：

| 设计维度 | 基线方案 | H2MM 方案 | 核心作用 |
|---------|---------|----------|---------|
| **表示空间** | 欧几里得空间 | 双曲空间（Poincaré 球模型） | 为层次化语义提供天然几何载体 |
| **噪声注入** | 各向同性高斯噪声 | 解耦的径向/角度噪声 + Λc 缩放 | 保护层次结构在扩散过程中不被破坏 |
| **扩散求解器** | 欧几里得 ODE 求解器 | 基于 Möbius 运算的 HDM-Solver | 在双曲流形上直接执行高阶逆向采样 |
| **混合模型** | 单层高斯混合 | 树形层次结构 H2MM | 从全局隐变量分层划分高斯原语，实现部件级解耦 |

这些改变之间存在因果耦合关系：**表示空间的选择决定了几何特性 → 噪声注入方式必须适配该几何的度量结构 → 扩散求解器必须在对应流形上保持闭包性 → 混合模型则利用层次化表示实现语义可解释的生成**。

具体而言，H2MM 从根隐变量 $\mathbf{z} \in \mathbb{R}^{768}$ 出发，通过 44 层解码器（含双曲注意力与双曲 MLP 分裂）将高斯原语层次化划分为 128 个部件，形成树形混合结构。在扩散过程中，径向噪声与角度噪声被显式解耦，并通过缩放因子 Λc 根据半径自动调整角度噪声的幅度，从而匹配双曲几何的指数增长规律。逆向采样时，HDM-Solver 利用 Möbius 加法与标量乘法直接在 Poincaré 球上执行三阶 ODE 更新，其正确性由切空间欧拉更新与指数映射的等价性保证（Eq. 8）。

这一设计使得生成过程天然保持“半径控层次、角度控变化”的语义解耦，为后续的部件级编辑与渐进式生成提供了几何基础。



本文提出的**分层双曲混合模型（H2MM）**与**双曲扩散**框架，旨在将3D生成从欧几里得空间迁移到双曲空间，从而在扩散过程中保持语义层次结构的完整性。整个pipeline由四个核心模块串联构成：**树扫描网络**、**H2MM解码器**、**测地线扩散过程**和**双曲扩散模型求解器（HDM-Solver）**。

### 核心瓶颈与设计动机

在双曲空间（Poincaré球模型）中，半径控制语义层次（由粗到细），角度控制同一层次内的语义变化。然而，各向同性欧几里得噪声会破坏这一结构——径向和角度方向上的噪声尺度不匹配，导致边缘处的偏差放大。这一瓶颈是驱动整个框架设计的关键认知：必须将径向噪声与角度噪声解耦，并引入缩放因子 $\Lambda_c$ 根据半径自动调整角度噪声，以匹配双曲几何的指数增长特性。

### 模块关系与数据流

**树扫描网络**作为特征提取前端，接收输入特征集合并构建最小生成树。具体而言，它基于特征间的相异度构建无向m-连通图，通过Contractive Borůvka算法剪枝生成最小生成树 $G_T$。随后，对第 $i$ 个特征的状态聚合通过路径权重 $S(E_{ij})$ 实现，该权重为沿超边路径上所有转移矩阵 $\bar{\mathbf{A}}_k$ 的乘积：

$$h_{i} = \sum_{\forall j \in \Omega} S(E_{ij}) \bar{\mathbf{B}}_{j} x_{j}, \quad S(E_{ij}) = \prod_{k \in N_{ij}} \bar{\mathbf{A}}_{k}$$

聚合后的状态 $H$ 与原始输入 $X$ 通过可学习参数 $\mathbf{C}$、$\mathbf{D}$ 进行残差连接，得到最终输出特征：

$$Y = \mathbf{C} \odot \mathbf{Norm}(H) + \mathbf{D} \odot X$$

**H2MM解码器**接收全局隐变量 $\mathbf{z} \in \mathbb{R}^{768}$（经消融验证，该维度在拟合质量与计算效率间取得最优平衡），通过一个44层的解码器（包含双曲注意力和双曲MLP分裂）将高斯原语层次化划分为128个部件。该树形层次结构从根节点开始，逐层分裂生成混合模型的参数 $\Omega_i^{l=d} = \{\hat{\pi}_i^{l=d}, \mu_i^{l=d}, \Sigma_i^{l=d}\}$，其中协方差矩阵 $\Sigma_i$ 通过正实特征值与特征向量的分解保证正定性。

**测地线扩散过程**在双曲流形上执行前向扩散，注入解耦的径向与角度噪声。这一设计直接回应了核心瓶颈：径向噪声建模跨层语义演化，角度噪声建模层内语义变化，而 $\Lambda_c$ 缩放因子根据半径自适应调整角度噪声幅度。

**HDM-Solver**负责逆向采样，在双曲流形上执行高阶ODE求解。其关键理论保证在于：切空间中的任何欧拉更新经指数映射回双曲流形，形式上等价于直接在流形上进行Möbius加法与标量乘法：

$$\mathrm{Exp}_{\mathbf{z}_{t}}(\mathbf{x}_{t-\Delta t}) \equiv \mathbf{z}_{t} \oplus (\lambda \otimes \mathbf{v})$$

这一等价性使得求解器可以在切空间中进行高效的线性运算，同时保持双曲几何的完整性。

### 输入输出流总结

整个pipeline的输入为全局隐变量 $\mathbf{z}$（无条件生成）或条件信号（文本/图像条件生成），经过H2MM解码器生成层次化高斯混合参数，再通过双曲扩散过程进行采样，最终输出3D高斯原语表示。渐进式逐层生成策略（消融实验显示可将FID从15.92降至9.73）进一步提升了输出质量。



### 树扫描网络：基于最小生成树的特征聚合

H2MM 的编码器采用**树扫描网络**，将无序特征集转换为具有层次结构的表示。其核心操作分为两步：

1. **图构建与剪枝**：对特征集 $\{x_i\}$，以特征间相异度为边权重构建无向 $m$-连通图，随后通过 **Contractive Borůvka** 算法剪枝，生成最小生成树 $G_T$。这一步骤确保聚合路径遵循特征空间的固有拓扑。

2. **路径加权状态聚合**：对于第 $i$ 个特征，其聚合状态 $h_i$ 定义为图中所有节点特征的加权和，权重为沿超边路径的转移矩阵乘积：

$$h_i = \sum_{\forall j \in \Omega} S(E_{ij}) \bar{\mathbf{B}}_j x_j, \quad S(E_{ij}) = \prod_{k \in N_{ij}} \bar{\mathbf{A}}_k$$

其中 $S(E_{ij})$ 表示沿路径 $E_{ij}$ 的累积转移权重，$\bar{\mathbf{A}}_k$ 和 $\bar{\mathbf{B}}_j$ 为可学习的转移矩阵。最终输出特征通过残差连接融合原始输入：

$$Y = \mathbf{C} \odot \mathbf{Norm}(H) + \mathbf{D} \odot X$$

$\mathbf{C}$、$\mathbf{D}$ 为可学习缩放参数，$\odot$ 表示逐元素乘法。该残差结构保证了特征变换的稳定性。

### H2MM 解码器：层次化高斯混合参数生成

解码器从全局隐变量 $\mathbf{z} \in \mathbb{R}^{768}$ 出发，通过 44 层双曲注意力与双曲 MLP 分裂，将高斯原语层次化划分为 128 个部件。每个叶节点输出对应混合分量的完整参数：

$$\Omega_i^{l=d} = \{\hat{\pi}_i^{l=d}, \mu_i^{l=d}, \Sigma_i^{l=d}\}$$

其中 $\hat{\pi}_i$ 为混合权重，$\mu_i \in \mathbb{R}^{14}$ 为均值，$\Sigma_i$ 为协方差矩阵。为保证 $\Sigma_i$ 的正定性，模型采用特征分解参数化：$\Sigma_i = U_i \Lambda_i U_i^\top$，其中 $\Lambda_i$ 的对角元素为正实数特征值，$U_i$ 的列向量为对应特征向量。这一分解从数学上保证了协方差矩阵始终是正定矩阵。

### 双曲扩散过程：解耦径向与角度噪声

**核心瓶颈**：在双曲空间（Poincaré 球模型）中，语义层次间的距离主要由**半径**决定——半径越大，语义越精细。各向同性欧几里得噪声会破坏这一结构，因为它在径向和角度方向施加相同的扰动尺度，而双曲几何在边缘处呈指数膨胀，导致边缘语义的偏差被不成比例地放大。

**解决方案**：将前向扩散的噪声解耦为两个独立分量：
- **径向噪声**：控制语义层次间的跃迁（由粗到细）
- **角度噪声**：控制同一层次内的语义变化

并引入缩放因子 $\Lambda_c$，根据当前半径自动调整角度噪声的尺度，以匹配双曲几何的指数增长特性。消融实验（Table 5）证实：移除 $\Lambda_c$ 后，FID 从 10.12 恶化至 14.26，验证了该机制的关键作用。

### HDM-Solver：基于 Möbius 运算的高阶双曲 ODE 求解器

逆向采样需要在双曲流形上求解扩散 ODE。关键理论保证在于：**切空间中的欧拉更新后经指数映射回双曲流形，等价于直接在流形上执行 Möbius 加法与标量乘法**：

$$\mathrm{Exp}_{\mathbf{z}_t}(\mathbf{x}_{t-\Delta t}) \equiv \mathbf{z}_t \oplus (\lambda \otimes \mathbf{v})$$

其中 $\oplus$ 为 Möbius 加法，$\otimes$ 为 Möbius 标量乘法。这一等价性使得高阶 ODE 求解器（如论文中的三阶 HDM-Solver-3）可以完全在双曲流形上以闭式 Möbius 运算实现，避免了反复的指数/对数映射带来的数值误差和计算开销。

### 补充图表

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/001_Figure_1.jpg]]
*Figure 1: Visualization of noise injection in a polar-like space*



## 实验与关键发现

### 核心瓶颈与因果机制

本文的核心实验设计围绕一个明确的几何瓶颈展开：在双曲空间中，各向同性欧几里得噪声会破坏语义层次结构。其因果机制在于，双曲空间的半径控制语义层次（由粗到细），角度控制同一层次内的语义变化；而各向同性高斯噪声在径向和角度方向上尺度不匹配，导致边缘处的偏差被指数级放大。为此，作者引入解耦的径向与角度噪声，并使用缩放因子 $\Lambda_c$ 根据半径自动调整角度噪声，以匹配双曲几何的指数增长特性。这一因果调控是后续所有实验的验证基石。

### 主实验结果

在 ShapeNet 数据集上，H2MM 搭配双曲扩散取得了 **FID 10.39**，相较基线 **DiffGS** 的 12.87 降低了 2.48（Table 7）。该结果直接验证了双曲表示与解耦噪声注入对生成质量的提升。Table 7 同时给出了计算复杂度对比，表明 H2MM 在保持竞争力的推理效率下实现了更优的生成保真度。

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/008_Table_7.jpg]]
*Table 7: Complexity analysis of different methods on ShapeNet dataset*

### 消融实验

#### 根隐变量维度

Table 3 的消融表明，将根隐变量 $\mathbf{z}$ 的维度提升至 768 以上收益递减：维度 1024 时 NLL 为 0.95（±0.013），IoU 为 0.96，方差极小。这意味着 768 维已能充分编码全局语义，且对随机初始化鲁棒。

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/004_Table_3.jpg]]
*Table 3: Ablation study on the dimension of root z. The numbers in parentheses indicate the variance*

#### H2MM 分裂策略

Table 4 显示，较大的初始分裂和较少的层次层数能提高拟合质量。分裂方式 [8,4,4] 取得最优 NLL 0.97 和 IoU 0.96，验证了“粗粒度早期分裂 + 浅层结构”有利于保留语义层次。

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/005_Table_4.jpg]]
*Table 4: Ablation study on different H2MM splits*

#### 角度噪声缩放因子 $\Lambda_c$

Table 5 的对照实验是因果机制的直接证据：移除 $\Lambda_c$ 后，FID 从 10.12 恶化至 14.26。这证明角度噪声的几何自适应缩放是保持层次结构完整性的必要条件，而非可选的工程技巧。

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/006_Table_5.jpg]]
*Table 5: Effect of using Λc in our framework*

#### 渐进式生成策略

Table 6 表明，采用 3 层渐进式生成策略可将 FID 进一步降至 9.73，而去除该策略后 FID 飙升至 15.92。这说明逐层解码与扩散过程的协同是高质量生成的关键，单阶段生成难以捕捉由粗到细的部件层次。

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/007_Table_6.jpg]]
*Table 6: Ablation study on progressive generation*

### 数据集与实验配置

实验覆盖 ShapeNet（Car 7,462 对象、Chair 6,775 对象，各 150 视图）、OmniObject3D（5,795 对象，100 视图）和 Objaverse（82,575 对象，150 视图），详见表 1。H2MM 采用 4 层树结构，44 层解码器（双曲注意力 + 双曲 MLP 分裂），根隐变量 $\mathbf{z} \in \mathbb{R}^{768}$ 层次化划分出 128 个高斯原语，并使用 0 阶球谐函数获得高斯原语。生成配置（噪声调度、扩散步数、推理采样器）详见表 2。

### 可视化分析

Figure 1 直观对比了各向同性高斯噪声与解耦径向/角度噪声在类极坐标空间中的行为差异，为几何直觉提供了视觉锚点。Figure 2 展示了去噪过程中语义层次的逐步恢复。Figure 3 将无条件生成结果与 H2MM 树结构并列，清晰揭示部件层次划分与生成质量的关系。Figure 4、Figure 5、Figure 6 分别展示了类别条件生成、复杂文本到 3D 生成和图像到 3D 生成的效果，表明该方法在多模态条件下的泛化能力。

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/009_Figure_2.jpg]]
*Figure 2: Visualization of denoising process*

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/010_Figure_3.jpg]]
*Figure 3: Visualization of unconditional generation and H2MM*

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/011_Figure_4.jpg]]
*Figure 4: Visualization of class-conditioned generation*

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/013_Figure_5.jpg]]
*Figure 5: Visualization of complex text-to-3D generation*

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/014_Figure_6.jpg]]
*Figure 6: Visualization of image-to-3D generation*

### 失败模式与局限

当前分析未提供明确的失败案例或局限讨论。从实验设计推断，H2MM 的层次深度和分裂策略需针对不同数据集手工调整，这可能限制其在新类别上的即插即用能力。此外，双曲扩散求解器（HDM-Solver-3）的高阶 ODE 采样虽在 Table 7 中效率可接受，但在实时应用场景下的推理延迟仍需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2536_https_openaccess_thecvf_com_content_CVPR2026_html_Yang_Learning_Hierarch/figures/002_Table_1.jpg]]
*Table 1: Details of each dataset*



## 定位与知识库关联

### 核心创新与差异化定位

本工作提出的 **Hierarchical Hyperbolic Mixture Model (H2MM)** 与双曲扩散框架的核心创新，在于将3D高斯原语的生成从欧几里得空间迁移到双曲空间，并针对双曲几何特性设计了专用的噪声注入与求解机制。这一迁移并非简单的空间替换，而是基于一个关键的几何洞察：**在双曲空间中，半径控制语义层次（由粗到细），角度控制同一层次内的语义变化**。各向同性欧几里得噪声会破坏这种层次结构，因为径向和角度方向上的噪声尺度不匹配，导致边缘处的偏差放大。

基于此，本工作在三个关键维度上与现有方法形成差异化：

1.  **表示空间**：从欧几里得空间切换至双曲空间（Poincaré球模型），天然适配物体部件的树形层次结构。
2.  **噪声注入方式**：将各向同性高斯噪声解耦为径向与角度噪声，并引入缩放因子 $\Lambda_c$ 根据半径自动调整角度噪声，以匹配双曲几何的指数增长特性。
3.  **扩散求解器**：从欧几里得ODE求解器升级为基于Möbius运算的双曲HDM-Solver，在流形上直接执行高阶逆向采样。

### 与现有3D生成方法的对比

与现有基于3D高斯泼溅（3DGS）的生成方法相比，H2MM的层次化混合模型设计提供了显式的部件感知能力：

*   **DiffGS**、**GaussianCube** 等方法在欧几里得空间中操作，缺乏对物体语义层次结构的显式建模。H2MM通过树形层次结构，从全局隐变量 $z \in \mathbb{R}^{768}$ 出发，经4层解码器分层划分高斯原语至128个部件，实现了从粗粒度到细粒度的结构化生成。
*   **HGMMSplatting** 采用单层高斯混合模型，而H2MM的混合模型是树形层次结构，能够捕捉不同粒度级别的语义分组。

在计算复杂度与生成质量方面，**Table 7** 显示H2MM在ShapeNet数据集上取得了 **FID 10.39**，相比DiffGS的12.87降低了2.48，在保持竞争力的同时提供了部件级别的可解释性。

### 关键技术组件的谱系

1.  **树扫描网络（Tree Scanning Network）**：该模块基于特征间的相异度构建无向m-连通图，通过Contractive Boruvka算法剪枝生成最小生成树，并利用路径权重 $S(E_{ij}) = \prod_{k \in N_{ij}} \bar{\mathbf{A}}_k$ 对所有特征进行加权聚合。其状态聚合公式为：
    $$h_{i} = \sum_{\forall j \in \Omega} S(E_{ij}) \bar{\mathbf{B}}_{j} x_{j}$$
    这一设计与图神经网络中的消息传递机制一脉相承，但通过树结构显式编码了层次关系。

2.  **双曲扩散模型求解器（HDM-Solver）**：该求解器的理论基础是证明了切空间中的欧拉更新后经指数映射回双曲流形，等价于直接在流形上进行Möbius加法与标量乘法：
    $$\mathrm{Exp}_{\mathbf{z}_{t}}(\mathbf{x}_{t-\Delta t}) \equiv \mathbf{z}_{t} \oplus (\lambda \otimes \mathbf{v})$$
    这一等价性使得扩散过程可以在双曲流形上以闭式运算高效执行，避免了反复的指数/对数映射。

3.  **协方差矩阵的参数化**：为保证每个混合成分的协方差矩阵 $\Sigma_i$ 保持正定性，本工作采用基于正实特征值与对应特征向量的分解方式，确保了数值稳定性。

### 适用边界与局限

根据消融实验提供的证据，该方法存在以下适用边界：

*   **隐变量维度**：根隐变量 $z$ 的维度增加至768以上时收益递减（Table 3），且方差极小，表明模型对初始化鲁棒，但也说明表示能力在此维度附近趋于饱和。
*   **层次结构设计**：较大的初始分裂和较少的层次层数能提高拟合质量。**Table 4** 显示 split [8,4,4] 取得了最优的 NLL 0.97 和 IoU 0.96，表明并非层次越深越好。
*   **噪声缩放的必要性**：移除角度噪声缩放因子 $\Lambda_c$ 导致 FID 从 10.12 恶化至 14.26（Table 5），验证了双曲几何适配的不可或缺性。
*   **渐进式生成策略**：采用逐层渐进生成可显著提升输出质量，3层渐进式策略将 FID 从无渐进式的 15.92 降至 9.73（Table 6），表明一步到位的生成策略在层次化框架中效果有限。

### 开放问题

当前分析材料中未提供明确的开放问题或未来工作方向。基于方法本身的设计，以下几个方向值得关注但需手动验证：

*   该框架在更复杂的多物体场景或动态场景中的扩展性尚未讨论。
*   双曲空间的维度选择与物体语义层次深度之间的关系缺乏理论分析。
*   当前实验集中在ShapeNet等合成数据集，在真实扫描数据上的泛化能力需要进一步验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_Hierarchical_Hyperbolic_Mixture_Model_for_Part_aware_3D_Generation.pdf]]
