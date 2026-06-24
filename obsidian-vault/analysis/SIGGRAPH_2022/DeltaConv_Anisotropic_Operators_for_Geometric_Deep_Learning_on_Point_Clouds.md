---
title: "DeltaConv: Anisotropic Operators for Geometric Deep Learning on Point Clouds"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2022
pdf_ref: paperPDFs/SIGGRAPH_2022/DeltaConv_Anisotropic_Operators_for_Geometric_Deep_Learning_on_Point_Clouds.pdf
project_link: "https://rubenwiersma.nl/deltaconv"
code_link: "https://github.com/rubenwiersma/deltaconv"
aliases:
- DeltaConv
tags:
- SIGGRAPH_2022
- topic/benchmarks_datasets_evaluation
core_operator: 引入显式的切向向量流并与标量流分离，通过可学习的梯度、散度、旋度及Hodge-Laplacian等几何微分算子组合，使网络能表达坐标独立的各向异性滤波。
primary_logic: 将卷积视作几何算子的线性组合与非线性复合，而非固定的核函数，可在任意曲面表示上实现方向感知的特征提取，同时自然继承等距不变性。
claims:
- DeltaConv通过组合向量微积分中的几何算子构建各向异性滤波器。
- 网络分为标量流和向量流，由几何算子连接。
- 网络权重不依赖于切空间基的选择，即坐标独立。
- 向量流显著提升性能，在分类任务上错误率降低19-25%，在分割任务上降低3-21%。
---

# DeltaConv: Anisotropic Operators for Geometric Deep Learning on Point Clouds

> [!tip] 核心洞察
> 将卷积视作几何算子的线性组合与非线性复合，而非固定的核函数，可在任意曲面表示上实现方向感知的特征提取，同时自然继承等距不变性。

| 字段 | 内容 |
|------|------|
| 中文题名 | DeltaConv：点云的几何深度学习各向异性算子 |
| 英文题名 | DeltaConv: Anisotropic Operators for Geometric Deep Learning on Point Clouds |
| 会议/期刊 | SIGGRAPH 2022 |
| Links | [paper](https://rubenwiersma.nl/deltaconv) · [Code](https://github.com/rubenwiersma/deltaconv) · [Project](http://www.nealen.com/projects/mls/asapmls.pdf) |
| Topic | #topic/benchmarks_datasets_evaluation |
| Method | DeltaConv |
| Dataset | ModelNet40, ScanObjectNN, ShapeNet, SHREC11 |

> [!tip] 效果简介
> - ModelNet40 上，Overall Accuracy 93.8 vs 92.9 (DGCNN) (+0.9)。
> - ScanObjectNN (NO BG variant) 上，Accuracy 89.5 vs 86.2 (DGCNN) (+3.3)。
> - ShapeNet (part segmentation) 上，instance mIoU 86.9 vs 85.2 (DGCNN) (+1.7)。

## 概要

点云表面缺乏全局坐标系，使得直接构建方向依赖的（各向异性）卷积极为困难。现有方法要么局限于各向同性滤波，要么依赖边缘特征等间接手段来引入方向信息。本文提出 **DeltaConv**，一种将向量微积分中的几何微分算子（梯度、散度、旋度及 Hodge-Laplacian）作为可学习组件的新型卷积层。网络被显式分离为**标量流**与**向量流**，二者通过上述几何算子连接：标量流经梯度算子生成切向向量场，向量流经散度与旋度算子映射回标量场，同时 Hodge-Laplacian 在向量流内部扩散方向特征。这种设计使卷积成为几何算子的线性组合与非线性复合，能够表达坐标独立的各向异性滤波，并自然继承等距不变性。

在 ModelNet40 分类上达到 93.8% 准确率，ScanObjectNN 最难变体上达到 84.7%，ShapeNet 零件分割实例 mIoU 达 86.9%，均超越 DGCNN、KPConv 等基线方法。消融实验证实向量流使分类误差降低 19–25%、分割误差降低 3–21%，且 DeltaConv 在速度上优于 EdgeConv。该方法为点云几何深度学习提供了一种以微分算子为核心、方向感知的特征学习新范式。

## 核心方法与创新机理

### 问题瓶颈：点云表面缺乏全局坐标系

图像具有天然的全局像素网格坐标系，因此定义具有方向依赖性的各向异性卷积（如边缘检测、方向性平滑）是直接的。然而，点云表面不存在这样的全局坐标系：每个点的局部邻域位于不同的切平面上，不同切平面之间缺乏统一的对齐基准。这一根本差异使得直接将图像卷积的各向异性设计迁移到点云变得困难——现有内在卷积方法要么退化为各向同性滤波，要么依赖边缘特征等间接手段来隐式地捕捉方向信息，未能显式地在切平面内构建方向感知的滤波操作。

### 核心洞察：几何微分算子作为卷积原语

DeltaConv 的核心洞察在于重新定义卷积的本质：将卷积视为**几何微分算子的线性组合与非线性复合**，而非学习一个固定的核函数。在向量微积分中，梯度（gradient）、散度（divergence）、旋度（curl）以及 Hodge-Laplacian 等算子天然地刻画了标量场与向量场之间的方向性关系，并且这些算子是坐标独立的——它们的物理意义不依赖于切空间基的具体选取。通过让网络学习这些算子的组合方式，DeltaConv 能够在任意曲面表示上构建各向异性滤波器，同时自然继承等距不变性。

### 架构框架：双流网络与算子连接

DeltaConv 将网络显式分离为**标量流（scalar stream）**和**向量流（vector stream）**，两者通过几何微分算子连接。这是与先前方法的关键架构差异：

**Changed Slot 1：特征类型与聚合方式**
- **基线方法**（如 DGCNN 的 EdgeConv、PointNet++）：使用基于边的特征（点对差值）或多层感知机直接作用于局部点集，方向信息隐含在 3D 坐标中。
- **DeltaConv**：标量流仅使用逐点特征并采用最大值聚合；向量流显式维持切向向量特征，携带方向信息。这一分离使得方向感知操作可以集中在向量流中进行，标量流则专注于位置无关的特征提取。

**Changed Slot 2：各向异性机制**
- **基线方法**：通过 3D 坐标表示的隐式方向性，或通过坐标轴分块 MLP 间接实现各向异性。
- **DeltaConv**：显式学习梯度、散度、旋度等几何算子的组合，在标量流与向量流之间传递方向信息，构建显式的各向异性操作。

### 模块顺序与数据流动

DeltaConv 的单层更新遵循以下模块化流程：

**模块 1：k-NN 图构建**
为每个形状计算 k 近邻图。该图在标量流中用于最大值聚合，同时被复用于法线估计（必要时）和离散梯度算子的构造。邻域大小 k 是方法的关键超参数，直接影响算子的局部支持域。

**模块 2：标量流更新**
标量特征的更新遵循简洁的设计：
$$\mathbf { x } _ { i } ^ { ( l + 1 ) } = h _ { \boldsymbol { \Theta } _ { 0 } } ( \mathbf { x } _ { i } ^ { ( l ) } ) + \operatorname* { m a x } _ { j \in { \cal N } ( i ) } h _ { \boldsymbol { \Theta } _ { 1 } } ( \mathbf { x } _ { j } ^ { ( l ) } )$$
其中 $h_{\Theta_0}$ 和 $h_{\Theta_1}$ 是逐点 MLP，$\mathcal{N}(i)$ 是点 $i$ 的 k 近邻。第一项是逐点变换，第二项是邻域最大值聚合。与 EdgeConv 的最大区别在于不使用边缘特征（点对差值），这带来了显著的效率优势：推理速度提升 1.5-2 倍，反向传播速度提升 2.5-30 倍。

**模块 3：梯度算子（标量 → 向量）**
使用移动最小二乘（Moving Least Squares, MLS）方法在 k 近邻上构造离散梯度算子 $\mathbf{G} \in \mathbb{R}^{2N \times N}$。该算子将标量场映射为切向向量场，是标量流向向量流传递信息的桥梁。为保证数值稳定性，梯度算子需经过两步处理：
- **正则化**：在 MLS 求解中引入 Tikhonov 正则化参数 $\lambda$，防止欠采样区域的病态条件；
- **归一化**：按无穷范数归一化：
$$\hat { \mathbf { G } } = \mathbf { G } / | \mathbf { G } | _ { \infty } , \quad \mathrm { w h e r e ~ } | \mathbf { G } | _ { \infty } = \operatorname* { m a x } _ { i } \sum _ { j } | \mathbf { G } _ { i j } |$$
归一化将算子的缩放行为约束在可控范围内，对性能至关重要（消融实验见后文）。

**模块 4：散度与旋度算子（向量 → 标量）**
离散散度算子 $\mathbf{D}$ 同样通过 MLS 方法构造，将向量场映射回标量场，捕获向量场的“源”强度。旋度算子则由散度与旋转矩阵 $\mathbf{J}$（切平面内 90 度旋转）组合得到：$\mathbf{C} = -\mathbf{D}\mathbf{J}$，捕获向量场的“涡旋”分量。两个算子共同构成向量流向标量流的回传通道。

**模块 5：Hodge-Laplacian（向量 → 向量）**
Hodge-Laplacian 是向量流内部的扩散算子，由梯度、散度、旋度组合实现。连续形式为：
$$\Delta = - ( \mathrm { g r a d d i v } + \mathcal { T } \mathrm { g r a d c u r l } )$$
其中 $\mathcal{T}$ 是切平面内的 90 度旋转。离散形式为矩阵组合：
$$\mathbf { L } = - ( \mathbf { G D } - \mathbf { J G D J } )$$
该算子使向量特征在流形上平滑扩散，同时保持方向信息的几何一致性。

**模块 6：向量 MLP**
向量流内部的变换由向量 MLP 完成：
$$\mathbf { V } ^ { \prime } = \sigma ( \mathbf { V } \mathbf { W } )$$
其中 $\mathbf{W}$ 是作用于通道维度的权重矩阵，$\sigma$ 是非线性激活函数。关键设计在于：$\mathbf{W}$ 对向量通道进行线性组合与缩放，但**不混合单个向量的切平面分量**。这意味着向量 MLP 的输出不依赖于切空间基的具体选择，保证了坐标独立性。此外，向量 MLP 可通过与 $\mathbf{J}$ 的组合实现向量的旋转操作。

**模块 7：DeltaConv 层完整更新**
单层 DeltaConv 的完整更新方程整合了上述所有模块：
$$\begin{array} { r l } & { \mathbf { v } _ { i } ^ { \prime } = \mathbf { h } _ { \boldsymbol { \Theta } _ { 0 } } ( \mathbf { v } _ { i } , \mathbf { \Delta } ( \mathbf { G } \mathbf { X } ) _ { i } , \mathbf { \Delta } ( \mathbf { L } \mathbf { V } ) _ { i } ) } , \\ & { \mathbf { x } _ { i } ^ { \prime } = h _ { \boldsymbol { \Theta } _ { 1 } } ( \mathbf { x } _ { i } , \mathbf { \Delta } ( \mathbf { D } \mathbf { V } ^ { \prime } ) _ { i } , \mathbf { \Delta } ( \mathbf { - D } \mathbf { J } \mathbf { V } ^ { \prime } ) _ { i } , \| \mathbf { v } _ { i } ^ { \prime } \| ) + \underset { j \in { \cal N } _ { i } } { \operatorname* { m a x } } h _ { \boldsymbol { \Theta } _ { 2 } } ( \mathbf { x } _ { j } ) } \end{array}$$

**向量流更新**（第一行）：$\mathbf{v}_i'$ 融合三个信息源——当前向量特征 $\mathbf{v}_i$、标量场经梯度算子作用后的方向信息 $\mathbf{\Delta}(\mathbf{GX})_i$、以及向量场经 Hodge-Laplacian 扩散后的平滑特征 $\mathbf{\Delta}(\mathbf{LV})_i$。$\mathbf{\Delta}(\cdot)$ 表示可学习的逐元素非线性变换。

**标量流更新**（第二行）：$\mathbf{x}_i'$ 融合五个信息源——当前标量特征 $\mathbf{x}_i$、更新后向量场的散度 $\mathbf{\Delta}(\mathbf{DV}')_i$（“源”信息）、旋度 $\mathbf{\Delta}(-\mathbf{DJ}\mathbf{V}')_i$（“涡旋”信息）、向量模长 $\|\mathbf{v}_i'\|$（方向强度），以及邻域标量特征的最大值聚合。

### 训练与推理路径

**训练阶段**：对每个输入形状，首先计算 k-NN 图和法线（若输入不含法线），构造梯度、散度、旋度、Hodge-Laplacian 矩阵。这些几何算子作为固定的预处理步骤，不参与梯度反向传播。网络可训练参数集中在标量 MLP、向量 MLP 以及各非线性变换 $\mathbf{\Delta}(\cdot)$ 中。由于算子本身是坐标独立的，网络权重不依赖于切空间基的选择，实现了真正的几何不变性。

**推理阶段**：与训练相同的前向传播路径。由于使用逐点特征而非边缘特征，推理速度显著优于 EdgeConv 等基于边的方法。具体而言，DeltaConv 的训练批次时间从 EdgeConv 的 196ms 降至 130ms；若仅使用 Laplacian 算子（简化版），可进一步降至 80ms。

### 因果链条：从几何算子到各向异性

DeltaConv 实现各向异性的因果链条可总结为：
1. **梯度算子**将标量特征的空间变化编码为切向向量，携带“沿哪个方向变化最快”的信息；
2. **向量 MLP** 在保持坐标独立性的前提下，对向量通道进行线性重组与缩放，实现方向选择性的增强或抑制；
3. **Hodge-Laplacian** 在向量流内部沿流形扩散方向信息，使各向异性模式在几何上平滑传播；
4. **散度与旋度**将处理后的方向信息回传至标量流，分别捕获“汇聚/发散”和“旋转”模式；
5. **标量 MLP** 综合所有几何信息进行最终的特征融合。

这一设计使得网络能够学习到类似“沿主曲率方向增强边缘”或“沿特定切向方向平滑”等各向异性行为，而无需显式定义核函数或依赖全局坐标系。

![[assets/figures/papers/paper_list_l18_https_rubenwiersma_nl_deltaconv/figures/001_Figure_1.jpg]]
*Figure 1: Images have a global coordinate system (left). Point clouds do not (right), complicating the design of anisotropic convolutions*

## 实验与关键发现

DeltaConv在多个点云分析基准上进行了系统评估，覆盖刚性分类（ModelNet40）、真实扫描分类（ScanObjectNN）、非刚性形状分类（SHREC11）和零件分割（ShapeNet）四类任务。以下从主结果、向量流消融、算子稳定性、效率分析及适用边界五个维度展开。

### 主结果：分类与分割基准

**ModelNet40刚性分类**（Table 1）：DeltaConv取得93.8%的整体准确率（mean class accuracy 91.2%），超越DGCNN的92.9%和KPConv的92.9%，在所有对比方法中排名第一。相比PointNet++（91.9%）和PointCNN（92.2%），DeltaConv的优势源于显式的各向异性滤波能力，而非仅依赖逐点MLP或边缘特征。

**ScanObjectNN真实扫描分类**（Table 2）：该基准包含真实世界扫描中的遮挡和噪声，是检验方法鲁棒性的关键场景。在“无背景”（NO BG）变体上，DeltaConv达到89.5%，比DGCNN（86.2%）高出3.3个百分点；在最具挑战的“最难扰动”（hardest perturbation）变体上达到84.7%。DeltaConv在所有扰动类型上均优于全部对比方法，表明几何算子构建的各向异性滤波对真实扫描中的不规则采样和局部缺失具有更强的容忍度。

**SHREC11非刚性分类**（Table 3）：该基准测试对等距变形的不变性。DeltaConv取得99.6%的准确率，略高于MeshWalker（99.2%）和MeshCNN（98.6%）。由于DeltaConv的几何算子天然继承等距不变性——梯度、散度、旋度均定义在切平面上，不依赖全局坐标——网络无需数据增强即可泛化至大幅度非刚性变形。

**ShapeNet零件分割**（Table 4）：DeltaConv的instance mIoU达到86.9%，超过DGCNN（85.2%）和PointCNN（84.6%）。分割任务要求细粒度的局部几何理解，向量流提供的方向信息使网络能更好地区分几何边界和零件过渡区域。

### 向量流的决定性贡献

DeltaConv的核心设计是将网络分离为标量流和向量流，并通过几何算子连接两者。Table 5的消融实验直接验证了这一设计的必要性：在ModelNet40上，将向量流加入纯标量流（最大值聚合）使误差降低19-25%；在ShapeNet分割上，误差降低3-21%。无论标量流采用何种变体（最大值聚合、EdgeConv、注意力聚合等），向量流的加入均带来一致且显著的性能提升。这证明方向感知的特征提取是独立于标量流具体实现的关键增益来源。

值得注意的是，DeltaConv的标量流仅使用逐点特征和最大值聚合，而EdgeConv使用点对差值作为边缘特征。Table 5显示，即使将EdgeConv作为标量流，加入向量流后性能仍大幅提升，说明几何算子传递的方向信息无法被边缘特征简单替代。

### 梯度算子的正则化与归一化

离散梯度算子在欠采样区域可能产生不稳定的输出。DeltaConv引入两个关键机制：正则化（控制最小二乘拟合的条件数）和无穷范数归一化（约束缩放行为）。Table 7的消融表明，两者对性能至关重要：在ModelNet40上，无归一化时平均类别准确率仅为86.6%，同时使用正则化和归一化后提升至89.4%。正则化参数λ需要根据数据分布调整，这是该方法的一个实用边界条件——不同数据集的最优λ可能不同，需要手动搜索。

### 效率与计算开销

Table 6对比了各方法在ModelNet40上的训练/推理时间和参数量。DeltaConv的训练批次时间为130ms，低于EdgeConv的196ms，推理速度提升1.5-2倍，反向传播速度提升2.5-30倍。这一效率优势源于DeltaConv仅使用逐点特征而非边缘特征——边缘特征需要为每个邻域边计算和存储特征对，而DeltaConv的标量流仅需对逐点MLP输出做最大值聚合。若进一步简化为仅使用Laplacian算子（去除完整的梯度-散度-旋度组合），训练批次时间可降至80ms，但会牺牲部分准确性。

### 适用边界与失效模式

尽管DeltaConv在多个基准上表现优异，其设计存在明确的适用边界：

1. **法线估计依赖**：梯度算子和向量流需要每点的切平面信息，这依赖于法线估计的质量。在极度稀疏（如点数少于100）或噪声严重的区域，法线估计可能失败，导致几何算子退化。ScanObjectNN上的结果虽已展示一定鲁棒性，但极端条件下的行为仍需验证。

2. **邻域大小k的敏感性**：k-NN图同时用于标量流聚合和梯度算子构建，k的选择影响感受野大小和算子精度。论文未系统报告k的消融，但这是实际部署中需要调节的超参数。

3. **生成任务的未探索性**：DeltaConv的设计针对分析任务（分类、分割），其算子基于固定的输入点云构建。在生成任务（如点云上采样、补全）中，点云拓扑动态变化，何时以及如何更新微分算子是一个开放问题。

4. **正则化参数的调参成本**：虽然正则化对性能至关重要，但λ的选择目前依赖经验，不同数据集可能需要独立调参，增加了方法在新领域的部署成本。

![[assets/figures/papers/paper_list_l18_https_rubenwiersma_nl_deltaconv/figures/005_Table_1.jpg]]
*Table 1: Classification results on ModelNet40*

![[assets/figures/papers/paper_list_l18_https_rubenwiersma_nl_deltaconv/figures/006_Table_2.jpg]]
*Table 2: Classification results on ScanObjectNN*

![[assets/figures/papers/paper_list_l18_https_rubenwiersma_nl_deltaconv/figures/007_Table_3.jpg]]
*Table 3: Classification results on SHREC11*

![[assets/figures/papers/paper_list_l18_https_rubenwiersma_nl_deltaconv/figures/009_Table_4.jpg]]
*Table 4: Part segmentation results on ShapeNet*

![[assets/figures/papers/paper_list_l18_https_rubenwiersma_nl_deltaconv/figures/011_Table_5.jpg]]
*Table 5: Ablations of DeltaConv on ShapeNet (Seg) and ModelNet40 (M40) with varying scalar streams*

## 定位与知识库关联

DeltaConv 的核心贡献在于为几何深度学习引入了一种**坐标独立的各向异性卷积机制**。与已有工作的本质差异可归结为一个关键槽位的变化：**特征类型与聚合方式**。

### 相对于已有方法的槽位变化

在 DeltaConv 之前，点云上的卷积操作主要沿两条路径发展。一条路径以 **PointNet++** (Qi et al., NeurIPS 2017) 和 **DGCNN** (Wang et al., ACM Trans. Graph. 2019) 为代表，前者使用逐点多层感知机加对称聚合函数，后者引入基于边缘的特征（EdgeConv，即点对差值）来捕获局部几何。这两类方法虽然有效，但其方向感知能力是隐式的——要么完全缺失各向异性，要么仅通过 3D 坐标差值的组合间接体现，缺乏对切平面方向结构的显式建模。另一条路径以 **KPConv** (Thomas et al., ICCV 2019) 和 **PointCNN** (Li et al., NeurIPS 2018) 为代表，试图通过连续核函数或学习的空间变换引入方向依赖性，但这些方法仍然依赖全局坐标系中的坐标值，无法保证等距不变性。

DeltaConv 改变了这一格局。其核心槽位变化在于：**将网络中传递的特征显式地分离为标量流和向量流**，并通过几何微分算子（梯度、散度、旋度、Hodge-Laplacian）连接两者。标量流仅使用逐点特征并采用最大值聚合，这与 EdgeConv 使用边缘特征形成鲜明对比。向量流则维持切向向量特征，其更新完全在切平面上进行，不依赖全局坐标系。这种设计的直接后果是：网络权重不依赖于切空间基的选择，即实现了坐标独立性（coordinate-independence），同时自然继承了等距不变性。

### 知识库挂载点

DeltaConv 在知识图谱中的挂载点位于**离散微分几何与深度学习的交叉节点**。具体而言：

- **上游依赖**：离散梯度、散度和旋度算子的构造直接继承自几何处理领域的移动最小二乘法（Moving Least Squares, MLS）框架（Nealen 2004）。Hodge-Laplacian 的离散化则来自离散外微积分（Discrete Exterior Calculus, DEC）的传统。这些算子在 DeltaConv 中被重新目的化（repurpose）为神经网络中可微的连接模块，而非单纯的分析工具。

- **平行关系**：与 **MeshCNN** (Hanocka et al., ACM Trans. Graph. 2019) 和 **MeshWalker** (Lahav and Tal, ACM Trans. Graph. 2020) 等面向网格的深度学习方法相比，DeltaConv 直接在点云上操作，无需网格连接信息，但通过 k-NN 图隐式地恢复了局部拓扑。与这些方法共享的目标是等距不变性，但 DeltaConv 通过算子组合而非数据增强或随机行走来实现。

- **下游延伸**：DeltaConv 的向量流设计为后续研究打开了多个方向。例如，向量特征可以作为注意力机制的输入，或者与 Transformer 架构中的位置编码结合。此外，几何算子组合的可学习性暗示了自动算子搜索（neural architecture search for geometric operators）的可能性。

### 适用边界

DeltaConv 的设计假设了以下前提条件，这些条件也构成了其适用边界：

1. **法线估计质量**：梯度算子的构造依赖局部邻域的法线方向。在严重噪声或极度稀疏的点云区域，法线估计的退化会直接影响算子质量，进而降低特征提取的有效性。论文通过正则化参数 λ 部分缓解了这一问题，但不同数据分布可能需要重新调参。

2. **邻域大小 k 的敏感性**：k-NN 图的构建是标量流聚合和几何算子离散化的共同基础。k 值过小会导致算子欠平滑，过大则会模糊局部细节。论文在实验中固定了 k 值，未探索其自适应选择机制。

3. **任务范围**：当前验证局限于分类和分割等分析任务。对于点云生成、补全等生成式任务，如何在生成过程中动态更新微分算子（因为点位置在不断变化）仍是一个开放问题。

4. **表示形式**：虽然理论上 DeltaConv 可适用于任意离散曲面表示，但论文仅在点云上进行了实验。其在网格、四面体网格或其他流形（如双曲空间）上的适用性需要进一步验证。

### 后续研究启发

DeltaConv 为几何深度学习领域提供了以下具体启发：

- **算子组合的可学习性**：论文证明了网络可以学习梯度、散度、旋度等基础算子的线性组合与非线性复合，从而构建复杂的各向异性滤波器。这一思路可推广至其他物理启发的算子（如应力、应变张量算子），为物理模拟与深度学习的融合提供新路径。

- **向量流作为通用组件**：向量流的设计是模块化的，可以与不同的标量流变体（如注意力聚合、Transformer 块）组合。论文的消融实验（Table 5）已初步验证了这一点：在最大值聚合、EdgeConv 等不同标量流上加入向量流均能显著降低错误率（分类任务降低 19–25%，分割任务降低 3–21%）。

- **效率优势的深层原因**：DeltaConv 使用逐点特征而非边缘特征，使得推理速度提升 1.5–2 倍，反向传播速度提升 2.5–30 倍（Section 4.4）。这一发现提示：在几何深度学习中，通过算子设计减少显式的成对特征计算，是实现高效网络的有效策略。

- **与等变网络的关联**：DeltaConv 的坐标独立性使其与群等变网络（如 SE(3)-等变网络）存在天然联系。未来工作可以探索如何将向量流的形式化与群表示论结合，构建更严格的等变几何网络。

综上所述，DeltaConv 在知识库中的定位是：**首个通过可学习几何微分算子组合在点云上实现坐标独立各向异性卷积的方法**。它桥接了离散微分几何的传统工具与深度学习的表示学习需求，为后续研究提供了可复用的向量流模块和算子组合范式。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2022/DeltaConv_Anisotropic_Operators_for_Geometric_Deep_Learning_on_Point_Clouds.pdf]]