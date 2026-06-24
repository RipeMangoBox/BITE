---
title: "A Unified Framework for Implicit Sinkhorn Differentiation"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/A_Unified_Framework_for_Implicit_Sinkhorn_Differentiation.pdf
aliases:
- ISDABKSC
- UFISD
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "反向传播方式：从展开式自动微分切换到基于KKT条件的隐式微分解析求解，使梯度计算与正向迭代次数解耦。"
primary_logic: "利用熵正则化最优传输的KKT条件构造稀疏线性系统，并通过Schur补技巧将求解复杂度降至与输入尺度立方，避免直接求逆和向量化，从而在内存和数值稳定性上显著优于AD，并提供了误差界保证。"
claims:
- "反向传播计算成本与Sinkhorn迭代次数τ无关。"
- "相比AD，我们的方法在大型问题上显存需求降低一个数量级，AD常在τ≥200时因显存不足而失败。"
- "梯度具有理论误差界，保证了近似的可靠性。"
- "在图像重心计算中，即使使用很少的Sinkhorn迭代，隐式梯度也能得到更清晰、更稳定的插值结果。"
---

# A Unified Framework for Implicit Sinkhorn Differentiation

> [!tip] 核心洞察
> 利用熵正则化最优传输的KKT条件构造稀疏线性系统，并通过Schur补技巧将求解复杂度降至与输入尺度立方，避免直接求逆和向量化，从而在内存和数值稳定性上显著优于AD，并提供了误差界保证。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 隐式Sinkhorn微分的统一框架 |
| 英文题名 | A Unified Framework for Implicit Sinkhorn Differentiation |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2205.06688); [GitHub](https://github.com/marvin-eisenberger/implicit-sinkhorn) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Implicit Sinkhorn Differentiation (Analytical Backward via KKT and Schur Complement) |
| Dataset | ModelNet40 point cloud registration with 70% partial removal, Number sorting generalization (test on U(1,2)) |

> [!tip] 效果简介
> - ModelNet40 point cloud registration with 70% partial removal 上，Rotation MAE (degrees) 为 20.9274，对比 52.5945，变化 -31.6671。
> - Number sorting generalization (test on U(1,2)) 上，Mean proportion of false predictions 为 0.2964，对比 0.3163，变化 -0.0199。

## 概述

将Sinkhorn算子嵌入神经网络已成为点云配准、流形插值、图像聚类等视觉任务的基础构建模块。其核心是求解熵正则化最优传输问题：

$$S_{\lambda}(C,\mathbf{a},\mathbf{b}) := \underset{P \in \Pi(\mathbf{a},\mathbf{b})}{\arg\min} \langle P, C \rangle_{\mathcal{F}} - \lambda h(P)$$

该问题通过交替行列归一化（Sinkhorn迭代）高效近似求解。然而，标准自动微分（AD）需展开所有前向迭代的计算图，导致显存占用和运行时间与迭代次数τ线性增长——当τ≥200时，AD常因GPU显存不足而失败，严重制约大批量、高分辨率场景的应用。

**核心瓶颈**：反向传播的计算图长度与正向迭代次数耦合，使梯度计算成为系统性能的硬约束。

**方法定位**：本文提出基于KKT条件的隐式微分解析求解框架，将梯度计算与正向迭代次数解耦。通过Schur补技巧将线性系统求解复杂度控制在O(n³)，避免直接求逆和向量化，在内存效率和数值稳定性上显著优于AD，并提供形式化的梯度误差界保证。

**关键结果**：
- 反向传播计算成本与Sinkhorn迭代次数τ无关，显存需求降低一个数量级。
- 在ModelNet40点云配准（70%部分缺失）中，将RPM-Net的旋转MAE从52.59°降至20.93°；在噪声和部分数据上泛化鲁棒性显著优于AD基线。
- 图像Wasserstein重心计算中，即使使用极少的Sinkhorn迭代，隐式梯度也能产生更清晰、更稳定的插值结果。
- 梯度具有理论误差界（Theorem 5），保证了近似的可靠性。

## 背景与动机

### 最优传输与Sinkhorn算子

最优传输（Optimal Transport, OT）旨在以最小代价将一个概率分布传输到另一个概率分布。对于离散测度 $\mu = \sum_i a_i \delta_{x_i}$ 和 $\nu = \sum_j b_j \delta_{y_j}$，其Kantorovich形式为：

$$d(\mu, \nu) := \min_{P \in \Pi(a,b)} \langle P, C \rangle_{\mathcal{F}}$$

其中 $C_{ij} = c(x_i, y_j)$ 为代价矩阵，$\Pi(a,b) = \{P \in \mathbb{R}_+^{n \times m} \mid P\mathbb{1}_m = a, P^\top\mathbb{1}_n = b\}$ 为传输多胞体。该线性规划问题的精确求解复杂度为 $\tilde{O}(n^3)$，难以嵌入大规模深度学习流程。

**熵正则化Sinkhorn算子**通过引入熵项 $h(P) = -\sum_{ij} P_{ij}(\log P_{ij} - 1)$ 使问题严格凸且可微：

$$S_{\lambda}(C,\mathbf{a},\mathbf{b}) := \underset{P \in \Pi(\mathbf{a},\mathbf{b})}{\arg\min} \langle P, C \rangle_{\mathcal{F}} - \lambda h(P)$$

该算子可通过**Sinkhorn迭代**高效近似求解——交替进行行/列重正则化：

$$S_{\lambda}^{(0)} := \exp\left( -\frac{1}{\lambda} C \right), \quad S_{\lambda}^{(t+1)} := \mathcal{T}_c\left( \mathcal{T}_r\left( S_{\lambda}^{(t)} \right) \right)$$

这使得Sinkhorn算子成为计算机视觉中可微的基本构建块，广泛应用于点云配准、流形插值和图像聚类等任务（Figure 1）。

### 核心瓶颈：自动微分的迭代依赖性

当Sinkhorn层嵌入神经网络时，标准做法是通过**自动微分**（Automatic Differentiation, AD）展开所有 $\tau$ 次Sinkhorn迭代的计算图进行反向传播。这带来两个根本性限制：

1. **显存线性增长**：AD的反向传播需要保存每次迭代的中间激活，GPU显存占用与迭代次数 $\tau$ 呈线性关系。当 $\tau \geq 200$ 时，AD常因显存不足（OOM）而失败（Figure 3 bottom, Figure 4 caption），迫使实际使用中减少迭代次数，牺牲正向解精度。

2. **梯度质量受迭代深度影响**：展开深度不足时，AD梯度不仅偏离真实梯度，且缺乏理论保证；而增加迭代又加剧显存压力，形成精度-资源的死锁。

### 现有隐式微分方法的缺口

已有工作尝试通过隐式微分规避展开计算图，但存在显著局限。**Table 1** 系统对比了先前方法：多数方法仅支持对代价矩阵 $C$ 的微分，或要求边缘分布 $a,b$ 固定；部分方法依赖向量化操作导致 $O(n^4)$ 的过高复杂度，或缺乏对近似正向解的梯度误差理论保证。**尚无方法能在统一框架下同时支持对代价矩阵和边缘分布的联合微分，并提供理论误差界。**

### 本文动机与目标

针对上述缺口，本文从第一性原理出发，提出一个**隐式Sinkhorn微分的统一框架**。其核心动机是：

- **解耦反向传播与正向迭代**：利用熵正则化OT的KKT条件构造稀疏线性系统，通过Schur补技巧将梯度计算复杂度降至与输入尺度立方，使反向传播成本与 $\tau$ 无关。
- **通用性与理论保证**：支持任意损失函数下对代价矩阵 $C$ 和边缘分布 $a,b$ 的联合微分，并提供梯度误差的形式化界（Theorem 5）。
- **即插即用**：作为一个简单模块直接替换AD，在点云配准、排列学习、图像重心计算等任务中提升稳定性和计算效率（Figure 2）。

## 核心创新

本文的核心创新在于将Sinkhorn层的反向传播从**展开式自动微分（AD）**彻底切换为**基于KKT条件的隐式微分解析求解**，实现了梯度计算与正向Sinkhorn迭代次数τ的完全解耦。这一范式转换通过以下三个关键机制实现：

### 1. 反向传播机制的范式转换

标准做法是对Sinkhorn迭代过程展开计算图，通过自动微分逐步回传梯度。该方法存在根本性瓶颈：显存占用和运行时间与迭代次数τ线性增长——当τ较大（如≥200）时，AD常因GPU显存不足而直接失败（Fig. 3）。本文提出的隐式微分方法直接求解由KKT条件导出的稀疏线性系统（Theorem 3, Eq. 11），使反向传播的计算成本与τ无关（Sec. 4.4）。

### 2. Schur补降维求解

直接求解KKT线性系统需要处理规模为$(n+m+nm) \times (n+m+nm)$的矩阵，计算代价过高。本文利用Sinkhorn问题的特殊结构，通过Schur补技巧将系统降维为仅涉及边际变量的小规模稠密矩阵运算（Algorithm 1），避免了对传输计划矩阵的向量化操作，将复杂度控制在$O(n^3)$时间、$O(n^2)$显存。这一设计使得在相同GPU显存预算下，隐式方法的内存占用比AD低一个数量级（Fig. 3 bottom）。

### 3. 梯度质量的误差界保证

与AD梯度受展开深度和数值稳定性影响不同，本文方法在正向解精确时给出精确梯度；当正向解为近似解时，提供了形式化的误差界（Theorem 5, Eqs. 13a-13b），从理论上保证了梯度的可靠性。实验证实，隐式梯度的精度在统计上显著优于AD，尤其在大τ场景下（Fig. 9）。

### Changed Slots 总结

| 组件 | 基线方法（AD） | 本文方法 | 证据锚点 |
|------|---------------|---------|---------|
| 反向传播计算 | 展开Sinkhorn迭代的自动微分 | 基于KKT线性系统的隐式微分 + Schur补求解 | Theorem 3, Algorithm 1 |
| 反向传播显存复杂度 | $O(\tau n^2)$（随τ线性增长） | $O(n^2)$（与τ无关） | Sec. 4.4, Fig. 3 |
| 梯度精度 | 受展开深度与数值稳定性影响，无理论保证 | 精确解对应精确梯度，近似解有误差界 | Theorem 5, Fig. 9 |

这些创新使得隐式Sinkhorn微分在图像重心计算中即使使用极少迭代次数也能产生更清晰、更稳定的插值结果（Fig. 4），在点云配准中面对噪声和部分数据的泛化鲁棒性显著优于基于AD的RPM-Net（Table 2: Rotation MAE从52.59°降至20.93°）。

## 整体框架

本文提出一种通用的隐式Sinkhorn微分框架，将熵正则化最优传输层嵌入神经网络，并为其提供解耦于正向迭代次数的解析反向传播。该框架的核心思想是：**正向传播**通过标准的Sinkhorn迭代缩放近似求解运输计划，而**反向传播**则绕过展开计算图，直接利用KKT条件构造稀疏线性系统，通过Schur补技巧高效计算梯度。整体工作流如图2所示。

### 模块组成与数据流

框架由三个关键模块构成，形成“特征提取→最优传输→损失反馈”的端到端可微管道：

1. **特征提取网络**：输入可以是图像、三维点云、体素网格或曲面网格等任意模态数据。网络输出三个量：
   - 成本矩阵 $C \in \mathbb{R}^{m \times n}$
   - 源边缘分布 $\mathbf{a} \in \Delta_m$
   - 目标边缘分布 $\mathbf{b} \in \Delta_n$

2. **Sinkhorn正向层**：接收 $(C, \mathbf{a}, \mathbf{b})$，通过交替行列归一化近似求解熵正则化最优传输问题：
   $$S_{\lambda}(C,\mathbf{a},\mathbf{b}) := \underset{P \in \Pi(\mathbf{a},\mathbf{b})}{\arg\min} \langle P, C \rangle_{\mathcal{F}} - \lambda h(P)$$
   迭代过程为：
   $$S_{\lambda}^{(0)} := \exp\left( -\frac{1}{\lambda} C \right), \quad S_{\lambda}^{(t+1)} := \mathcal{T}_c\left( \mathcal{T}_r\left( S_{\lambda}^{(t)} \right) \right)$$
   输出运输计划 $P$ 作为下游任务的软匹配或注意力权重。

3. **Sinkhorn反向层（Algorithm 1）**：接收上游损失对 $P$ 的梯度 $\nabla_P \ell$，通过求解KKT线性系统的Schur补形式，一次性输出 $\nabla_a \ell$、$\nabla_b \ell$、$\nabla_C \ell$，无需向量化操作，也无需存储正向迭代的中间激活。

### 与自动微分的本质差异

标准自动微分（AD）将Sinkhorn迭代的每一步都记录在计算图中，反向传播时必须逐步回传，导致：
- **显存占用**与迭代次数 $\tau$ 线性增长（$\mathcal{O}(\tau n^2)$）
- **运行时间**随 $\tau$ 增加而显著上升
- 当 $\tau \geq 200$ 时，在24GB GPU上常因显存不足（OOM）而失败

本框架的隐式微分则将反向传播与正向迭代次数**完全解耦**：无论正向执行多少次Sinkhorn迭代，反向传播只需在最终的运输计划 $P$ 上执行一次Algorithm 1，其计算复杂度为 $\mathcal{O}(n^3)$ 时间、$\mathcal{O}(n^2)$ 显存，与 $\tau$ 无关。这一特性使得框架在大批量、高分辨率场景下具有显著的工程优势。

### 边缘分布约束处理

为确保 $\mathbf{a}, \mathbf{b}$ 始终落在概率单纯形上，框架在前向传播中可选地引入边缘softmax操作。反向传播时，Algorithm 1自动处理该约束，将最后一个梯度分量置零以保持概率和不变性，无需手动推导约束雅可比。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2205_06688/figures/007_Figure_6.jpg]]
*Figure 6: Number sorting. We show that we can improve the Gumbel-Sinkhorn method [28] directly with Algorithm 1. Specifically, we consider the task of permutation learning to sort random number sequences of length n $\in \{$ 2 0 0 , 5 0 0 , 1 0 0 0 $\}$ , see [28, Sec 5.1] for more details. We replace AD in the GS network with implicit differentiation (blue curves) and compare the obtained results to the vanilla GS architecture (orange curves). Our approach yields more accurate permutations while using much less computational resources – GS is out of memory for τ > 200, 100, 50 forward iterations, respectively. For all settings, we show the mean proportion of correct test set predictions (solid lines), a...*

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2205_06688/figures/003_Figure_2.jpg]]
*Figure 2: Overview of a typical workflow with an embedded Sinkhorn layer. We consider a neural network whose inputs are e.g. images, 3D point clouds, voxel grids, surface meshes, etc. The Sinkhorn layer maps the cost matrix C and marginals a, b to the transportation plan P via iterative matrix scaling. During training, we compute respective gradients ( $\nabla _ { C } \ell , \nabla _ { a } \ell , \nabla _ { b } \ell$ ) in closed form via implicit differentiation. Our algorithm applies to the most general formulation of the Sinkhorn operator: Both the cost matrix C and marginals a, b are learnable and the whole network potentially contains learnable weights before and after the Sinkhorn layer

## 核心模块与公式推导

### 3.1 问题形式化：熵正则化最优传输与Sinkhorn算子

给定两个离散概率分布 $\mathbf{a} \in \Delta_n$ 和 $\mathbf{b} \in \Delta_m$，以及代价矩阵 $C \in \mathbb{R}^{n \times m}$，熵正则化最优传输问题定义为：

$$S_{\lambda}(C,\mathbf{a},\mathbf{b}) := \underset{P \in \Pi(\mathbf{a},\mathbf{b})}{\arg\min} \langle P, C \rangle_{\mathcal{F}} - \lambda h(P) \tag{Eq. 4}$$

其中 $\Pi(\mathbf{a},\mathbf{b}) = \{P \in \mathbb{R}_+^{n \times m} \mid P\mathbb{1}_m = \mathbf{a},\; P^\top\mathbb{1}_n = \mathbf{b}\}$ 为传输多胞体，$h(P) = -\sum_{i,j} P_{ij}(\log P_{ij} - 1)$ 为熵正则项，$\lambda > 0$ 控制正则化强度。

该问题可通过 **Sinkhorn迭代** 高效近似求解：

$$S_{\lambda}^{(0)} := \exp\left( -\frac{1}{\lambda} C \right), \quad S_{\lambda}^{(t+1)} := \mathcal{T}_c\left( \mathcal{T}_r\left( S_{\lambda}^{(t)} \right) \right) \tag{Eq. 5}$$

其中 $\mathcal{T}_r$ 和 $\mathcal{T}_c$ 分别为行归一化和列归一化算子，通过交替缩放逐步逼近精确解 $P^*$。

### 3.2 核心洞察：从展开式AD到隐式微分

**瓶颈分析**：标准自动微分（AD）对Sinkhorn层的反向传播需要展开所有 $\tau$ 次前向迭代的计算图，导致显存占用与运行时间随 $\tau$ 线性增长。当 $\tau \geq 200$ 时，AD常因GPU显存不足（24GB预算下）而失败（Fig. 3）。

**因果开关**：将反向传播方式从展开式AD切换为基于KKT条件的隐式微分解析求解，使梯度计算与正向迭代次数 $\tau$ 解耦。

### 3.3 KKT条件与隐式函数雅可比

将熵正则化OT问题的最优解 $P^*$ 及其对偶变量 $\boldsymbol{\alpha}^* \in \mathbb{R}^n$、$\boldsymbol{\beta}^* \in \mathbb{R}^m$ 满足的KKT条件写为残差形式：

$$\mathcal{K}(\cdot) := \begin{bmatrix} \mathbf{c} + \lambda \log(\mathbf{p}^*) + \mathbb{1}_n \otimes \boldsymbol{\alpha}^* + \boldsymbol{\beta}^* \otimes \mathbb{1}_m \\ (\mathbb{1}_n^\top \otimes I_m) \mathbf{p}^* - \mathbf{a} \\ (I_n \otimes \mathbb{1}_m^\top) \mathbf{p}^* - \mathbf{b} \end{bmatrix} = \mathbf{0} \tag{Eq. 8}$$

其中 $\mathbf{p}^* = \text{vec}(P^*)$，$\mathbf{c} = \text{vec}(C)$。由隐函数定理，该KKT系统在解处定义了一个连续可微映射，其雅可比矩阵为：

$$\mathbf{J} := \frac{\partial [\mathbf{p}; \boldsymbol{\alpha}; \tilde{\boldsymbol{\beta}}]}{\partial [\mathbf{c}; -\mathbf{a}; -\tilde{\mathbf{b}}]} = -\begin{bmatrix} \lambda \operatorname{diag}(\mathbf{p})^{-1} & \tilde{\mathbf{E}} \\ \tilde{\mathbf{E}}^\top & \mathbf{0} \end{bmatrix}^{-1} \tag{Eq. 9}$$

其中 $\tilde{\mathbf{E}}$ 为与边缘约束相关的稀疏结构矩阵，$\tilde{\boldsymbol{\beta}}$ 为消除冗余自由度后的对偶变量。

### 3.4 反向传播线性系统（Theorem 3）

给定上游梯度 $\nabla_P \ell$，反向传播需求解向量-雅可比乘积（VJP）。**不显式求逆 $\mathbf{J}$**，而是通过求解以下稀疏线性系统得到 $\nabla_{\mathbf{a}}\ell$ 和 $\nabla_{\tilde{\mathbf{b}}}\ell$：

$$\begin{bmatrix} \lambda \operatorname{diag}(\mathbf{p})^{-1} & \tilde{\mathbf{E}} \\ \tilde{\mathbf{E}}^\top & \mathbf{0} \end{bmatrix} \begin{bmatrix} \cdot \\ -\nabla_{[\mathbf{a}; \tilde{\mathbf{b}}]} \ell \end{bmatrix} = \begin{bmatrix} -\nabla_{\mathbf{p}} \ell \\ \mathbf{0} \end{bmatrix} \tag{Eq. 11}$$

### 3.5 算法1：基于Schur补的高效实现

利用Sinkhorn问题的特殊结构，通过 **Schur补技巧** 将大规模线性系统转化为对小规模稠密矩阵的操作，**无需将矩阵向量化**，从而在GPU上实现高效计算：

**Algorithm 1 (Sinkhorn Backward)**：
$$\begin{aligned} &\mathbf{T} \leftarrow P \odot \nabla_P \ell \\ &[\nabla_{\mathbf{a}} \ell ; \nabla_{\tilde{\mathbf{b}}} \ell] \leftarrow \begin{bmatrix} \operatorname{diag}(\mathbf{a}) & \tilde{P} \\ \tilde{P}^\top & \operatorname{diag}(\tilde{\mathbf{b}}) \end{bmatrix}^{-1} \begin{bmatrix} \mathbf{T}\mathbb{1}_n \\ \tilde{\mathbf{T}}^\top \mathbb{1}_m \end{bmatrix} \\ &\nabla_C \ell \leftarrow -\lambda^{-1} \left( \mathbf{T} - P \odot (\nabla_{\mathbf{a}} \ell \,\mathbb{1}_n^\top + \mathbb{1}_m \nabla_{\mathbf{b}} \ell^\top) \right) \end{aligned}$$

**关键设计决策**：
- 边缘梯度通过求解 $(n+m) \times (n+m)$ 的对称正定系统获得，复杂度 $O((n+m)^3)$，与 $\tau$ 无关
- $\nabla_C \ell$ 通过矩阵逐元素操作直接计算，避免显式向量化
- 内存复杂度 $O(n^2)$，相比AD的 $O(\tau n^2)$ 降低一个数量级

### 3.6 梯度误差界保证（Theorem 5）

当正向Sinkhorn迭代仅给出近似解 $\hat{P}$ 时，隐式梯度引入的误差受以下理论界约束：

$$\|\nabla_{\mathbf{a}}\hat{\ell} - \nabla_{\mathbf{a}}\ell\| \leq \mathcal{O}\left(\|\hat{P} - P^*\|\right)$$

该误差界保证了即使使用较少迭代次数，隐式梯度的可靠性仍受形式化控制（Fig. 9实验验证）。

### 3.7 边缘概率不变性处理

当 $\mathbf{a}, \mathbf{b}$ 需保持在概率单纯形上时，模块通过 **边缘softmax** 确保约束满足，同时允许最后一个梯度分量置零以保持概率和为一的不变性（Sec. 4.4）。

## 实验与分析

### 核心瓶颈验证：计算图展开与显存爆炸

本文的核心动机是消除标准自动微分（AD）对Sinkhorn迭代次数的依赖。实验系统性地验证了这一瓶颈：**AD的反向传播需要展开全部τ次迭代的计算图，导致GPU显存占用和运行时间与τ线性增长**。Figure 3给出了定量证据——当τ≥200时，AD在24GB显存预算下直接因显存不足（OOM）而失败，而本文方法的内存占用与τ无关，始终保持在O(n²)水平。在运行时间上，本文方法在τ≳40–90（取决于矩阵尺寸）之后开始优于AD，且优势随τ增大而持续扩大。这一结果直接支撑了核心论断：**将反向传播从展开式AD切换到基于KKT条件的隐式微分，使梯度计算与正向迭代次数解耦**。

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2205_06688/figures/001_Figure.jpg]]

### 主实验结果

#### 点云配准：泛化鲁棒性的显著提升

在ModelNet40点云配准任务上，本文方法将RPM-Net的Sinkhorn层反向传播替换为隐式微分，保持网络结构、训练协议和超参数完全一致。Table 2的结果显示，在70%部分点云移除的严苛条件下，隐式微分将旋转MAE从52.5945降至**20.9274**（降低31.6671），提升幅度超过一倍。Figure 7的定性对比进一步揭示：AD版本在噪声和部分数据上配准结果明显漂移，而隐式版本保持了更紧致的对齐。这一差异的因果机制在于：**AD的梯度质量受展开深度和数值稳定性影响，在训练早期（前向解尚未精确时）梯度信号噪声较大；隐式微分通过解析求解KKT线性系统，即使前向迭代次数有限，也能提供具有理论误差界保证的梯度**（Theorem 5）。

#### 数字排序：泛化能力的边际改善

在数字排序任务中，将Gumbel-Sinkhorn方法的反向传播替换为隐式微分后，在分布外测试集U(1,2)上的错误比例从0.3163降至0.2964（Table 3, Appendix B.3）。提升幅度较小，但方向一致，说明隐式梯度在组合优化类任务中也具有正向迁移能力。

### 梯度精度与误差界验证

Theorem 5为隐式微分提供了梯度误差的理论上界，Figure 9通过直方图进行了实证验证。在图像重心实验中，对∇_a ℓ和∇_C ℓ的梯度精度进行统计检验，结果显示隐式微分的梯度分布在真值附近更集中，而AD的梯度分布更分散且存在系统性偏差。这一差异在τ较大时尤为显著——AD的数值误差累积效应随展开深度加剧，而隐式微分通过Schur补技巧直接求解线性系统，避免了误差传播链。

Figure 10给出了图像重心梯度的定性对比：隐式梯度（第3行）与真值梯度（末行）在空间结构和强度分布上高度一致，而AD梯度（第4行）在边缘区域出现明显噪声和衰减。这解释了Figure 4中隐式方法在τ很小时仍能产生清晰插值结果的现象——**梯度信号的质量而非前向解的精度，是决定训练稳定性的关键因素**。

### 消融与效率分析

#### 批处理尺寸的解放

在MNIST k-means聚类任务中（Figure 11），隐式微分允许使用**1024**的批处理尺寸，而AD受限于显存只能使用512甚至32的批次。这一差异直接源于内存复杂度的结构性差异：AD为O(τ n²)，隐式微分为O(n²)。对于需要大批量以稳定梯度估计的聚类任务，这一优势转化为实际训练可行性的质变。

#### 边际概率不变性

本文方法通过可选的marginal softmax模块确保输入边缘分布落在概率单纯形上，同时允许最后一个梯度分量置零以满足自由度约束。这一设计在图像重心实验中保证了优化过程的数值稳定性，避免了AD中常见的梯度爆炸或消失问题。

### 失败模式与局限性

1. **极小迭代次数的训练速度劣势**：当τ≈10时，AD的前向-反向总时间可能更短，因为隐式微分需要求解O(n³)的线性系统，前处理开销相对较高。这一现象在Figure 3的运行时间曲线中可见（τ<40时AD更快）。

2. **超高分辨率的计算瓶颈**：算法1的理论复杂度为O(n³)，对于n>10⁴的矩阵，Schur补矩阵的构造和求逆仍可能成为瓶颈。文中未给出n>1000的实验结果，该边界行为需要进一步验证。

3. **前向解精度依赖性**：隐式梯度依赖于正向Sinkhorn解的精度；当正向迭代严重不足时，梯度误差虽受Theorem 5约束，但仍可能影响训练收敛速度。Figure 9中τ=10时的梯度分布方差明显大于τ=100时，印证了这一局限性。

### 实验公平性保障

所有对比实验均在相同GPU显存预算（24GB）下进行，超出预算视为OOM。点云配准和数字排序任务中，除Sinkhorn层的反向传播实现外，网络结构、训练协议和超参数均保持一致。两种方法在同一PyTorch环境中实现，内存分配遵循PyTorch的离散单元机制，排除了框架层面的系统性偏差。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2205_06688/figures/002_Table_1.jpg]]
*Table 1: Overview of prior work. We provide an overview of related approaches that, like ours, derive implicit gradients of a Sinkhorn layer. For each method, we denote admissible inputs, i.e. which inputs are differentiated. In the most general case, we want to optimize both the marginals a and b and the cost matrix C defined in Sec. 3. As a special case, [11, 17] provide gradients $\nabla _ { \pmb { x } } \ell$ for low rank cost matrices of the form $\begin{array} { r } { \pmb { C } _ { i , j } : = \| \pmb { x } _ { i } - \pmb { y } _ { j } \| _ { 2 } ^ { p } . } \end{array}$ We furthermore denote which types of loss functions are permitted and whether gradients are derived via the primal or dual obje...

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2205_06688/figures/009_Table.jpg]]

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2205_06688/figures/010_Table_2.jpg]]
*Table 2: Point cloud registration. We compare the quantitative performance of RPM-Net [47] and implicit differentiation on ModelNet40 [44]. The two architectures are identical except for the altered Sinkhorn module. For all results, we follow the training protocol described in [47, Sec. 6]. Moreover, we assess the ability of the obtained networks to generalize to partial and noisy inputs at test time. For the former, we follow [47, Sec. 6.6] and remove up to 70% of the input point clouds from a random half-space. For the noisy test set, we add Gaussian white noise $\mathcal { N }$ ( 0 , $\sigma$ ) with different variances $\sigma \in \{$ 0 . 0 0 1 , 0 . 0 1 , 0 . 1 $\}$ . For all settings, we report the rot...

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2205_06688/figures/011_Figure_9.jpg]]
*Figure 9: Gradient accuracy. We empirically assess the accuracy of the error bound discussed in Theorem 5. Specifically, we show the accuracy of the gradients $\nabla _ { a } \ell$ for the image barycenter experiment in Sec. 5.2 (top row) and $\nabla _ { C } \ell$ for the number sorting experiment in Sec. 5.3 (bottom row). While both distributions have a large overlap, the gradients from our approach (blue) are noticeably more accurate than AD (orange) on average. Note that all comparisons show histograms on a log scale

![[assets/figures/papers/paper_list_l35_https_arxiv_org_abs_2205_06688/figures/012_Figure_10.jpg]]
*Figure 10: Image barycenter gradients. A qualitative comparison of our gradients (3rd row), the AD gradients (4th row), and the ground truth gradients (last row) for the image barycenter experiment from Sec. 5.2. Specifically, we consider the task of interpolating between two input images (1st row) with uniform interpolation weights $w _ { 1 } = w _ { 2 }$ = 0 . 5 . We show intermediate snapshots of the obtained barycenter image (2nd row) for different numbers of gradient descent iterations t $\in \{$ 0 , $\ldots$ , 7 0 $\}$ that result from minimizing the energy in Equation 14

## 方法谱系与知识库定位

### 1. 方法定位与核心贡献

本文提出的**隐式Sinkhorn微分**（Implicit Sinkhorn Differentiation）针对的是一个明确且普遍存在的瓶颈：标准自动微分（AD）在Sinkhorn层的反向传播中，需要展开所有前向迭代的计算图，导致显存占用和运行时间与迭代次数τ线性增长，使得大批量或高分辨率任务在有限GPU显存下不可行。该工作的核心创新在于将反向传播方式从**展开式自动微分**切换为**基于KKT条件的隐式微分解析求解**，使梯度计算与正向迭代次数解耦。

具体而言，该方法利用熵正则化最优传输的KKT条件构造稀疏线性系统，并通过Schur补技巧将求解复杂度降至与输入尺度立方（O(n³)），避免了直接求逆和向量化操作。这一定位使其在方法谱系中处于“可微最优传输层的高效反向传播”这一节点，填补了通用Sinkhorn层隐式微分的空白。

### 2. 与现有工作的关系

#### 2.1 与先前隐式微分方法的对比

在本文之前，已有若干工作尝试对Sinkhorn层进行隐式微分，但均存在输入限制。如**Table 1**所总结的，先前方法通常只能对部分输入（如仅对成本矩阵C或仅对边缘分布a, b）进行微分，而本文提出的框架支持**最通用的Sinkhorn算子形式**：允许任意损失函数，且能同时对目标容量（a, b）和成本矩阵（C）进行联合微分。这一通用性使得该方法可以直接替换现有架构中的Sinkhorn模块，无需修改网络设计。

#### 2.2 与标准自动微分（AD）的关系

AD是Sinkhorn层反向传播的**标准基线**。两者的本质区别在于：

| 维度 | 自动微分（AD） | 隐式微分（本文） |
|------|---------------|-----------------|
| 反向传播方式 | 展开所有Sinkhorn迭代的计算图 | 基于KKT条件解析求解线性系统 |
| 显存复杂度 | O(τ n²)，与迭代次数τ线性增长 | O(n²)，与τ无关 |
| 梯度精度 | 受展开深度和数值稳定性影响 | 精确解对应精确梯度；近似解有形式化误差界（Theorem 5） |
| 适用场景 | 小τ、小规模问题 | 大τ、大规模问题、显存受限场景 |

**决定性证据**：Figure 3（bottom）和Figure 4的caption明确指出，“AD在τ≥200时因显存不足而失败”，而本文方法在相同显存预算下可正常运行。Figure 3（top）进一步显示，当τ超过约40-90（取决于矩阵尺寸）后，本文方法的运行时间开始优于AD。

#### 2.3 在具体应用中对基线方法的改进

- **Gumbel-Sinkhorn**（排列学习基线）：在数字排序任务中，本文方法直接替换Gumbel-Sinkhorn中的Sinkhorn层反向传播，在n∈{200, 500, 1000}的序列长度上均取得更低的错误预测比例（Table 3, Appendix B.3）。
- **RPM-Net**（点云配准基线，Yew & Lee, 2019）：在ModelNet40点云配准任务中，仅将Sinkhorn模块的反向传播替换为本文的Algorithm 1，其余网络结构和训练协议完全保持一致。结果显示，在70%部分点云移除的噪声条件下，旋转MAE从RPM-Net的52.5945°降至20.9274°（Table 2），且“在噪声和部分数据上的泛化鲁棒性显著优于RPM-Net”（Figure 7 caption）。

### 3. 适用边界

#### 3.1 适用条件

- **输入规模**：方法适用于中小规模矩阵（n≤10⁴），此时O(n³)的理论复杂度在GPU上可接受。对于分辨率极高的矩阵（n>10⁴），Schur补求逆仍可能成为计算瓶颈。
- **正向求解精度**：隐式梯度依赖于正向Sinkhorn解的精度。当正向迭代充分收敛时，梯度具有理论误差界保证（Theorem 5）；当正向迭代不足时，近似解会引入误差，尽管该误差受形式化约束。
- **正则化类型**：当前框架专为**熵正则化**最优传输设计，利用其特殊的KKT结构和Sinkhorn迭代的分解性质。

#### 3.2 不适用或需谨慎的场景

- **极小迭代次数（τ≈10）**：此时AD的前处理开销更低，隐式微分的Schur补构造和线性系统求解可能反而更慢。
- **非熵正则化**：如L²正则化或组稀疏正则化，其KKT系统结构不同，本文的Schur补技巧无法直接迁移。
- **极端显存受限环境**：尽管显存占用已降至O(n²)，对于n>10⁴的矩阵，存储运输计划P（n²个元素）本身即可能超出显存预算。

### 4. 局限性与开放问题

#### 4.1 已识别的局限性

1. **理论复杂度下界**：算法1的核心操作涉及对(n+m)×(n+m)稠密矩阵的求逆（通过Schur补），其O(n³)复杂度是固有的，无法通过工程优化完全消除。
2. **正向-反向耦合**：梯度质量受正向解精度影响。当Sinkhorn迭代未充分收敛时，梯度误差虽受Theorem 5约束，但在极端情况下仍可能影响训练稳定性。
3. **小τ场景的效率劣势**：当τ极小时，隐式微分的前处理开销（构造线性系统、求解Schur补）可能超过AD的图展开开销。

#### 4.2 开放问题

1. **正则化扩展**：该方法是否可以扩展到熵正则化以外的其他正则化形式（如L²、组稀疏、unbalanced OT）？这需要重新推导对应的KKT系统和Schur补结构。
2. **大规模分布式训练**：在分布式训练场景中，如何进一步降低通信开销和内存占用？Sinkhorn层本身涉及全局归一化操作，其分布式实现与隐式微分的结合尚待探索。
3. **双层优化整合**：隐式微分能否整合进更复杂的双层优化框架（如超参数优化、元学习）？隐式微分的天然优势在于避免了展开式微分的计算图依赖，理论上适合此类场景，但实证验证仍缺乏。
4. **跨领域推广**：除视觉任务（点云配准、图像插值、聚类）外，该统一框架是否能显著推动其他领域中的最优传输应用，如单细胞组学分析、图匹配、3D形状对应等？这些领域通常涉及大规模或非标准成本矩阵，对梯度计算的效率和稳定性有更高要求。

### 5. 知识库定位总结

本文在可微最优传输的知识库中占据**通用隐式反向传播**这一关键节点。与先前工作相比，其核心区分性在于：
- **通用性**：支持对所有输入（C, a, b）的联合微分，覆盖最一般的Sinkhorn层形式；
- **理论保证**：提供了梯度误差的形式化上界（Theorem 5），这是先前隐式微分工作所缺乏的；
- **即插即用**：Algorithm 1可直接替换现有架构中的AD反向传播，无需修改网络结构或训练协议。

该方法在方法谱系中的位置可概括为：**从“展开式自动微分”到“基于KKT的解析隐式微分”的范式转换**，其技术核心（Schur补降维、避免向量化）为后续工作提供了可复用的设计模式。

## 原文 PDF

![[paperPDFs/CVPR_2022/A_Unified_Framework_for_Implicit_Sinkhorn_Differentiation.pdf]]
