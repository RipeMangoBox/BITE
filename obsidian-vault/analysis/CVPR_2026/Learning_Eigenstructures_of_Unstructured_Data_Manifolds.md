---
title: Learning Eigenstructures of Unstructured Data Manifolds
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Learning_Eigenstructures_of_Unstructured_Data_Manifolds.pdf
project_link: null
code_link: "https://github.com/royvelich/learning-eigenstructures"
aliases:
- OASBL
- LEUDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 探测函数（probe function）的分布选择——不同的探测函数分布隐式定义了不同的最优重构算子，从而控制所学谱基的性质。具体而言，通过k近邻图上高斯核平滑生成的探测函数诱导出类Laplacian算子；若改变探测函数的生成方式（如不同的平滑策略或分布），则对应不同的隐式算子。该机制使得方法可以泛化到Laplacian以外的算子。
primary_logic: 基于最优逼近理论（定理3.1的Min-Max最优性和定理3.2的算子有界PCA等价性），对于任意对称正定算子L，受约束信号类的最优正交基恰好是L的特征向量，且特征值可由最差重构误差的倒数直接估计。通过训练神经网络在预测的正交基上最小化探测函数的重构误差（公式1），网络隐式地学习某个算子的谱分解全过程，而无需在任何时刻显式构造该算子或其离散矩阵，也无需调用数值特征求解器。
claims:
- 最小化最差k项逼近误差的最优正交基恰好是约束算子L的前k个特征向量（定理3.1），为整个框架提供了严格的理论基础。
- PCA在相同信号类上的期望重构误差与Min-Max公式等价（定理3.2），使得可以将Min-Max中的单样本最差优化替换为全批量平均优化，大幅提升训练稳定性。
- 在3D表面点云过拟合设置下，无监督学到的非归一化特征向量与oracle cotangent Laplacian的特征向量几乎一致，k≤10时余弦相似度普遍超过0.93（如Armadillo 0.968, Bimba 0.964, Botijo 0.972, Kitten 0.993）。
- 模型在仅在表面点云上训练后，可以直接泛化到未见形状和三维体点云（Figure 6），体现了基础模型的泛化能力。
---

# Learning Eigenstructures of Unstructured Data Manifolds

> [!tip] 核心洞察
> 基于最优逼近理论（定理3.1的Min-Max最优性和定理3.2的算子有界PCA等价性），对于任意对称正定算子L，受约束信号类的最优正交基恰好是L的特征向量，且特征值可由最差重构误差的倒数直接估计。通过训练神经网络在预测的正交基上最小化探测函数的重构误差（公式1），网络隐式地学习某个算子的谱分解全过程，而无需在任何时刻显式构造该算子或其离散矩阵，也无需调用数值特征求解器。

| 字段 | 内容 |
|------|------|
| 中文题名 | 学习非结构化数据流形的特征结构 |
| 英文题名 | Learning Eigenstructures of Unstructured Data Manifolds |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Velich_Learning_Eigenstructures_of_Unstructured_Data_Manifolds_CVPR_2026_paper.html) · [Code](https://github.com/royvelich/learning-eigenstructures) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | Optimal-Approximation Spectral Basis Learning |
| Dataset | 3D表面点云（来自[90]，过拟合设置）, 高维图像流形（DINOv2特征，STL10/CIFAR100，1500张图像子集）, 泛化设置：未见表面和三维体点云（来自[41, 48, 69, 76, 86]等） |

> [!tip] 效果简介
> - 3D表面点云（来自[90]，过拟合设置） 上，与oracle cotangent Laplacian特征向量的余弦相似度（k≤10） Armadillo: 0.968; Bimba: 0.964; Botijo: 0.972; Elephant: 0.979; Kitten: 0.993 vs 1.0（oracle自身上界参考） (接近oracle水平（多数形状>0.93）)；相对特征值误差（mean ± std） Armadillo: 0.200±0.126; Bimba: 0.093±0.145; Botijo: 0.153±0.092; Elephant: 0.10... vs oracle cotangent Laplacian特征值（参考） (低误差（多数形状均值<0.20）)。
> - 高维图像流形（DINOv2特征，STL10/CIFAR100，1500张图像子集） 上，聚类性能（NMI/ARI，50次平均，越高越好） Optimal-Approximation Eigenmaps（所提方法）在不同嵌入维度k∈{2,5,10,50}上持续提供竞争性或最优聚类性能 vs PCA、Isomap、Laplacian Eigenmaps、t-SNE、UMAP (竞争性或更优（详见Figure 8）)。
> - 泛化设置：未见表面和三维体点云（来自[41, 48, 69, 76, 86]等） 上，视觉质量——非归一化特征向量v_i的合理性和空间平滑性 模型在仅训练于表面点云后，对未见形状和三维体点云均产生有意义的平滑谱基 vs 无直接量化对比（泛化设定下无oracle参考） (展示出基础模型级别的泛化能力)。

## 概要

### 问题背景

谱方法在几何处理、流形学习和科学计算中占据核心地位，其本质是将数据投影到某个微分算子的特征向量上，从而获得具有频率解释的正交基。然而，传统谱分析流程面临一个根本性瓶颈：**必须显式选择算子（如Laplace-Beltrami算子），对该算子进行离散化构造（质量矩阵和刚度矩阵），再调用数值特征求解器求解广义特征值问题**。这一流程对网格质量和连通性高度敏感，且在高维非结构化数据（如三维以上的点云、图像嵌入流形）上难以优雅扩展——构造可靠的图Laplacian本身就是一个挑战，其结果严重依赖局部密度和连接性选择。

### 核心思路

本文提出**Optimal-Approximation Spectral Basis Learning**，从根本上绕过了上述三步流程。其核心洞察基于最优逼近理论：对于任意对称正定算子 $L$，受约束信号类的最优正交基恰好是 $L$ 的特征向量，且特征值可由最差重构误差的倒数直接估计（定理3.1的Min-Max最优性）。通过训练神经网络在预测的正交基上最小化探测函数的重构误差，网络**隐式地学习某个算子的谱分解全过程，而无需在任何时刻显式构造该算子或其离散矩阵，也无需调用数值特征求解器**。

### 方法定位

与经典谱分析范式相比，本方法在三个关键环节实现了根本性转变：

1. **算子选择与离散化**：不再显式选择目标算子或构造离散矩阵；探测函数的分布选择隐式定义了最优重构算子——例如，通过k近邻图上高斯核平滑生成的探测函数诱导出类Laplacian算子，改变探测函数生成方式则对应不同的隐式算子。
2. **特征分解方式**：神经网络输出经QR分解直接获得正交基 $Q$；特征值由最差重构误差的倒数直接估计（$\lambda_{k+1} = 1/\max_i \|f^{(i)} - f^{(i)}_{\text{proj},k}\|^2$），完全无需数值特征求解器。
3. **度量获取**：质量矩阵由第一个学习到的归一化特征向量直接编码（$M = \text{diag}(\mathbf{q}_1 \odot \mathbf{q}_1)$），与谱基统一学习，无需对底层流形维度和度量做先验假设。

### 主要结果

在**3D表面点云**的过拟合设置下，无监督学到的非归一化特征向量与oracle cotangent Laplacian的特征向量高度一致：$k \leq 10$ 时余弦相似度普遍超过0.93（如Armadillo 0.968、Kitten 0.993），相对特征值误差均值低于0.20。模型仅在表面点云上训练后，可直接泛化到未见形状和**三维体点云**，展现出基础模型级别的泛化能力。在**高维图像流形**（DINOv2特征）上，学到的谱嵌入在聚类任务中持续提供竞争性或优于PCA、Isomap、Laplacian Eigenmaps、t-SNE、UMAP的表现。

### 局限与展望

当前方法存在训练计算成本高的问题，且在高频特征向量（$k > 20$）上与oracle的偏离较大。探测函数分布目前需人工设计，如何自动学习探测函数分布以适配不同算子类型是重要的开放问题。此外，框架向非对称算子的扩展、通用基础模型的训练、以及在大规模数据集上的实用化，均为值得探索的方向。



### 谱方法在几何处理中的核心地位

谱方法（spectral methods）是几何处理、流形学习和科学计算中的基础工具。其核心思想是将数据流形上定义的线性算子（最经典的为Laplace-Beltrami算子，LBO）进行特征分解，得到的特征值和特征向量（谱基）编码了流形的内蕴几何与拓扑信息。这些谱基被广泛应用于形状分析、形变、参数化、聚类、降维和物理模拟等下游任务。

### 传统谱分析流程的瓶颈

尽管谱方法功能强大，但传统谱分析流程存在一个深层瓶颈：**需要显式选择、离散构造并数值分解一个算子**。具体而言，该流程包含三个紧密耦合的步骤：

1. **算子选择**：根据任务需求显式选择一个目标算子，如Laplace-Beltrami算子。
2. **离散化构造**：在给定的离散表示（如三角网格）上，构造质量矩阵 $M$ 和刚度矩阵 $S$ 来近似该算子。例如，经典的cotangent Laplacian需要完整的三角网格连接信息来计算顶点面积和余切权重。
3. **数值特征求解**：调用广义特征求解器求解 $S\mathbf{u} = \lambda M\mathbf{u}$，得到特征值和特征向量。

这一流程存在几个根本性缺陷：

- **对网格质量和连通性高度敏感**：cotangent Laplacian的构造依赖于良剖分的三角网格，网格退化或不规则采样会严重损害谱基质量。
- **难以扩展到高维非结构化数据**：对于三维以上的点云、图像嵌入流形等高维数据，构造可靠的图Laplacian本身就是一个挑战——其结果严重依赖局部密度和连接性的选择（如k近邻图的k值、核宽度等超参数）。
- **特征求解的计算代价随规模增长**：对大规模矩阵调用数值特征求解器在时间和内存上均代价高昂。

### 现有方法的缺口

现有的谱基学习方法（如Laplacian Eigenmaps、扩散映射等）虽然部分缓解了网格依赖问题，但仍需显式构造某种图Laplacian矩阵并求解其特征分解。这些方法本质上是在**离散化后的矩阵**上操作，而非直接面向**底层流形和算子**。对于高维非结构化数据（如DINOv2特征嵌入流形，维度可达数百维），构造有意义的图连接性本身就缺乏可靠的理论指导，使得传统谱方法在此类场景下捉襟见肘。

### 本文的核心动机

本文的核心动机源于一个根本性的理论观察：**基于最优逼近理论，对于任意对称正定算子 $L$，受约束信号类的最优正交基恰好是 $L$ 的特征向量**（定理3.1的Min-Max最优性）。这一洞察暗示了一种全新的范式——**无需在任何时刻显式构造算子或其离散矩阵，也无需调用数值特征求解器，即可直接学习谱基**。

具体而言，本文提出通过训练神经网络，在预测的正交基上最小化探测函数（probe functions）的重构误差。不同的探测函数分布隐式定义了不同的最优重构算子，从而控制所学谱基的性质。该框架将传统流程中的“算子选择→离散化→特征分解”三步压缩为一个端到端的学习过程，仅需非结构化点云坐标作为输入，无需网格连接或图构造。

这一方法论的转变使得谱分析可以优雅地扩展到任意维度的非结构化数据，为构建通用的几何基础模型开辟了新的可能。



## 核心方法与创新机理

本文的核心创新在于将谱分析从“显式算子构造+数值特征分解”的经典范式，根本性地转变为“隐式算子学习+最优逼近优化”的神经网络范式。这一转变通过三个紧密耦合的**changed slots**实现，共同构成了一个端到端、无需网格连接、适用于任意维度非结构化数据的基础谱学习框架。

### 1. 从显式算子构造到隐式算子诱导

传统谱分析方法（如cotangent Laplacian、图Laplacian）的根本瓶颈在于必须**显式选择目标算子**（如Laplace-Beltrami算子），并通过质量矩阵M和刚度矩阵S对其进行离散化近似。这一过程对网格质量、连通性和局部密度高度敏感，且在高维非结构化数据上构造可靠的图Laplacian本身就是一个严峻挑战。

本文的核心突破在于**完全跳过了显式算子选择与构造**。其关键机制是：**探测函数（probe function）的分布族隐式定义了最优重构算子**。具体而言，通过在k近邻图上对随机信号迭代应用高斯核平滑生成的探测函数，隐式地诱导出一个类Laplacian算子——但这一算子从未被显式写出、离散化或存储。神经网络直接从点云坐标预测谱基，而不同的探测函数分布（如不同程度的高斯平滑、无平滑等）则对应不同的隐式算子，使得框架可以泛化到Laplacian以外的算子族（Figure 7）。

### 2. 从数值特征求解器到最优逼近优化

传统流程在构造离散矩阵后，必须调用数值广义特征求解器进行特征分解，这一步骤对近似精度敏感且计算代价高昂。本文用**神经网络训练+QR分解**完全替代了这一过程：

- 神经网络 $\Phi_\theta: \mathbb{R}^{n \times d} \to \mathbb{R}^{n \times K}$ 以点云坐标 $\mathcal{P}$ 为输入，输出每点的K维特征向量；
- 对网络输出进行QR分解 $\Phi_\theta(\mathcal{P}) = \mathbf{Q}\mathbf{R}$，直接将 $\mathbf{Q} = [\mathbf{q}_1, \ldots, \mathbf{q}_K]$ 解释为归一化算子的前K个特征向量；
- 训练损失 $\mathcal{L}_{\mathrm{rec}} = \frac{1}{mK} \sum_{i=1}^{m} \sum_{k=1}^{K} \|\mathbf{f}^{(i)} - \mathbf{f}_{\mathrm{proj},k}^{(i)}\|_2^2$ 在所有探测函数和所有截断级别k上最小化重构误差；
- 特征值由最差重构误差的倒数直接估计：$\lambda_{k+1} = 1 / \max_i \|\mathbf{f}^{(i)} - \mathbf{f}_{\mathrm{proj},k}^{(i)}\|_2^2$。

这一设计的理论基础来自**定理3.1（Min-Max最优性）**和**定理3.2（算子有界PCA等价性）**：对于任意对称正定算子L，受约束信号类的最优正交基恰好是L的特征向量，且Min-Max形式的最差重构误差与PCA形式的期望重构误差等价。这使得可以将单样本最差优化替换为全批量平均优化，大幅提升训练稳定性。

### 3. 从显式度量构造到统一质量矩阵学习

传统方法中，质量矩阵M需要由几何量显式计算（如顶点面积、Voronoi区域），依赖于对底层流形维度和度量的先验知识。本文的创新在于**质量矩阵由第一个学习到的归一化特征向量直接编码**：

$$M = \mathrm{diag}(\mathbf{q}_1 \odot \mathbf{q}_1)$$

这意味着度量信息与谱基在同一个优化过程中被统一学习，无需任何额外的几何先验。基于此，还可以计算非归一化谱基 $\mathbf{v}_i = M^{-1/2} \mathbf{q}_i$，具有更好的采样不变性，更适合下游任务。

### 创新总结

这三个changed slots的协同效应使得方法具有前所未有的数据灵活性：仅需非结构化点云（任意维度d），无网格或图连接要求。实验验证覆盖了1D区间、3D表面点云、3D体点云、以及高达数百维的图像特征流形（DINOv2特征），在过拟合设置下学到的谱基与oracle cotangent Laplacian的特征向量余弦相似度普遍超过0.93（Table 1），且模型在仅训练于表面点云后可直接泛化到未见形状和三维体点云（Figure 6），展现出基础模型级别的泛化能力。



本文提出的**最优逼近谱基学习（Optimal-Approximation Spectral Basis Learning）**框架，从根本上改变了传统谱分析的范式。传统流程需要三步：①显式选择目标算子（如Laplace-Beltrami算子）；②对算子进行离散化，构造质量矩阵和刚度矩阵；③调用数值特征求解器求解广义特征值问题。这一流程对网格质量高度敏感，且难以扩展到高维非结构化数据。本框架的核心突破在于：**无需在任何时刻显式构造算子或其离散矩阵，也无需调用数值特征求解器**，直接从非结构化点云坐标中端到端地学习谱基。

### 整体数据流

框架的输入是任意维度的点云坐标矩阵 $\mathcal{P} \in \mathbb{R}^{n \times d}$（$n$ 为点数，$d$ 为空间维度）。整个 pipeline 由以下核心模块串联构成（Figure 1 给出了完整的框架概览）：

![[assets/figures/papers/paper_list_l2127_https_openaccess_thecvf_com_content_CVPR2026_html_Velich_Learning_Eigens/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our neural framework to compute spectral bases directly from unstructured point clouds of any dimensionality, based on optimal-approximation theory, without first explicitly choosing, discretely approximating, and eigendecomposing an operator*

1. **神经网络特征提取器 $\Phi_{\theta}$**：以点云坐标 $\mathcal{P}$ 为输入，输出每点 $K$ 维特征向量，形成矩阵 $\Phi_{\theta}(\mathcal{P}) \in \mathbb{R}^{n \times K}$。在表面实验中采用 Transformer 架构，在 1D 实验中则使用小型 MLP。

2. **QR 分解正交化**：对网络输出进行 QR 分解 $\Phi_{\theta}(\mathcal{P}) = \mathbf{Q}\mathbf{R}$，其中 $\mathbf{Q} = [\mathbf{q}_1, \ldots, \mathbf{q}_K]$ 的列即为欧几里得正交的**归一化谱基**，直接解释为某个隐式算子的前 $K$ 个特征向量。

3. **度量矩阵（质量矩阵）的隐式学习**：第一个归一化特征向量 $\mathbf{q}_1$ 直接编码了对角度量矩阵 $M = \mathrm{diag}(\mathbf{q}_1 \odot \mathbf{q}_1)$。这意味度量与谱基在同一学习过程中统一获得，无需像传统方法那样通过几何量（如顶点面积、Voronoi 区域）显式计算质量矩阵。

4. **探测函数生成**：在数据的 $k$ 近邻图上，对随机信号迭代应用高斯核平滑，生成一组探测函数 $\{\mathbf{f}^{(i)}\}_{i=1}^m$。这些探测函数近似于具有有界 Dirichlet 能量的平滑信号类，从而**隐式诱导出类 Laplacian 算子**——这是框架中最关键的因果旋钮：不同的探测函数分布族对应不同的隐式算子。

5. **渐进 M-正交投影与重构**（Algorithm 1）：将每个探测函数以 M-正交方式投影到 $\mathbf{Q}_k$（前 $k$ 个基向量张成的子空间）上，计算 $\ell_2$ 重构误差。对 $k=1$ 到 $K$ 遍历执行，为训练损失和特征值估计提供信号。

6. **训练损失**：基于定理 3.2（算子有界 PCA 等价性），用全批量平均优化替代 Min-Max 中的单样本最差优化，损失函数为所有探测函数在所有截断级别上的平均 $\ell_2$ 重构误差：
   $$\mathcal{L}_{\mathrm{rec}} = \frac{1}{mK} \sum_{i=1}^{m} \sum_{k=1}^{K} \|\mathbf{f}^{(i)} - \mathbf{f}_{\mathrm{proj},k}^{(i)}\|_2^2$$

7. **特征值估计**：基于定理 3.1（Min-Max 最优性），第 $(k+1)$ 个特征值由第 $k$ 个谱分辨率下最差重构误差的倒数直接估计：
   $$\lambda_{k+1} = \frac{1}{\max_i \|\mathbf{f}^{(i)} - \mathbf{f}_{\mathrm{proj},k}^{(i)}\|_2^2}$$

8. **非归一化谱基输出**：从归一化谱基 $\mathbf{q}_i$ 和度量矩阵 $M$ 计算非归一化谱基 $\mathbf{v}_i = M^{-\frac{1}{2}} \mathbf{q}_i$，后者具有更好的采样不变性，更适合下游任务。

### 关键因果机制

整个框架的理论根基在于定理 3.1 和定理 3.2 所揭示的等价性：对于任意对称正定算子 $L$，受约束信号类的最优正交基恰好是 $L$ 的特征向量，且该解同时可通过 PCA 形式的期望优化达到。因此，通过训练神经网络在预测的正交基上最小化探测函数的重构误差，网络**隐式地学习某个算子的谱分解全过程**。探测函数的分布选择成为控制所学算子类型的核心旋钮——在默认配置下，$k$ 近邻图上的高斯核平滑探测函数诱导出类 Laplacian 算子；改变探测函数的生成方式（如不同程度的平滑或不同的分布族），则对应不同的隐式算子（见 Figure 7 的消融实验）。



### 3.1 理论基础：最优逼近与算子有界PCA

本方法的理论根基建立在两个核心定理之上，它们共同回答了“给定一个对称正定算子 $L$，什么样的正交基能够最优地表示受该算子约束的信号类”这一问题。

**定理 3.1 (Min-Max 最优性)** 指出，对于任意对称正定算子 $L$，考虑所有满足 $\|f\|_L \leq 1$ 的信号 $f$，其最差 $k$ 项逼近误差的最小值恰好由 $L$ 的前 $k$ 个特征向量达到，且该最优值为 $1/\lambda_{k+1}$。形式化地，Min-Max 逼近误差定义为：

$$\alpha_k = \min_{b=(b_1,\ldots,b_n)} \max_{\|f\|_L \leq 1} \left\| f - \sum_{i=1}^k \langle f, b_i \rangle b_i \right\|^2$$

该定理为整个学习框架提供了严格的理论保证：若我们能够最小化一组探测函数在预测正交基上的最差重构误差，那么所学到的正交基必然收敛于某个隐式算子 $L$ 的特征向量。

**定理 3.2 (算子有界PCA)** 进一步建立了 Min-Max 优化与 PCA 目标之间的等价性。在 $\|f\|_L \leq 1$ 的均匀分布信号上，期望重构误差的最小化解同样收敛于 $L$ 的特征向量：

$$\min_{b=(b_1,\cdots,b_n)} \mathbb{E}_{f \sim \mathcal{U}(\|f\|_L \leq 1)} \left( \left\| f - \sum_{i=1}^k \langle f, b_i \rangle b_i \right\|^2 \right)$$

这一等价性至关重要：它允许我们将 Min-Max 公式中难以优化的单样本最差情形替换为全批量平均优化，从而大幅提升训练的数值稳定性。

### 3.2 神经网络架构与正交基输出

方法的核心是一个神经网络特征提取器 $\Phi_\theta: \mathbb{R}^{n \times d} \to \mathbb{R}^{n \times K}$，其输入为非结构化点云坐标 $\mathcal{P} \in \mathbb{R}^{n \times d}$（$n$ 个点，$d$ 维空间），输出每个点的 $K$ 维特征向量。在表面实验中采用 Transformer 架构，在 1D 验证实验中使用小型 MLP。

对网络输出进行 QR 分解以获得正交基：

$$\Phi_{\theta}(\mathcal{P}) = \mathbf{Q}\mathbf{R}$$

其中 $\mathbf{Q} = [\mathbf{q}_1, \ldots, \mathbf{q}_K]$ 的列向量构成欧几里得正交的归一化谱基，$\mathbf{R}$ 为上三角矩阵。这一设计的精妙之处在于：**度量矩阵（质量矩阵）由第一个学习到的特征向量直接编码**，无需单独学习或显式计算：

$$M = \mathrm{diag}(\mathbf{q}_1 \odot \mathbf{q}_1)$$

其中 $\odot$ 表示逐元素乘积。这一公式的理论依据是：对于归一化算子，其第一个特征向量（对应最小特征值）的平方恰好编码了流形上的采样密度分布，即质量矩阵的对角线。由此，度量与谱基实现了统一学习。

从归一化谱基 $\mathbf{q}_i$ 和质量矩阵 $M$ 可进一步计算非归一化谱基：

$$\mathbf{v}_i = M^{-\frac{1}{2}} \mathbf{q}_i$$

非归一化谱基具有更好的采样不变性，因此更适合下游几何处理任务。论文中展示的实验结果（Figure 3、Figure 6）均以 $\mathbf{v}_i$ 为主要可视化对象。

### 3.3 探测函数生成与训练损失

探测函数（probe functions）的生成是连接隐式算子与神经网络训练的关键环节。具体流程为：在点云的 $k$ 近邻图上，对随机初始化的信号迭代应用高斯核平滑，生成一组具有有界 Dirichlet 能量的平滑信号 $\{\mathbf{f}^{(i)}\}_{i=1}^m$。这些探测函数近似于受某个类 Laplacian 算子约束的信号类，从而隐式地定义了最优重构算子。

训练的核心操作是**渐进 M-正交投影与重构**（Algorithm 1）。对于每个探测函数 $\mathbf{f}^{(i)}$ 和每个截断级别 $k \in \{1, \ldots, K\}$，将其以 $M$-正交方式投影到前 $k$ 个基向量张成的子空间上，得到重构 $\mathbf{f}^{(i)}_{\mathrm{proj},k}$。训练损失函数定义为所有探测函数在所有截断级别上的平均 L2 重构误差：

$$\mathcal{L}_{\mathrm{rec}} = \frac{1}{mK} \sum_{i=1}^{m} \sum_{k=1}^{K} \|\mathbf{f}^{(i)} - \mathbf{f}_{\mathrm{proj},k}^{(i)}\|_2^2$$

该损失函数是定理 3.2 中算子有界 PCA 目标的经验近似，通过同时优化所有截断级别，网络学习到的正交基 $\mathbf{Q}$ 将自然收敛于隐式算子的特征向量，且按特征值升序排列。

### 3.4 特征值估计

基于定理 3.1 的 Min-Max 最优性，第 $(k+1)$ 个特征值可直接从第 $k$ 个谱分辨率下的最差重构误差估计，无需调用任何数值特征求解器：

$$\lambda_{k+1} = \frac{1}{\max_i \|\mathbf{f}^{(i)} - \mathbf{f}_{\mathrm{proj},k}^{(i)}\|_2^2}$$

这一公式的物理直觉是：当基向量仅包含前 $k$ 个特征向量时，最差重构误差恰好由第 $(k+1)$ 个特征值决定——特征值越小（对应更平滑的特征函数），信号在该方向上的投影越难被前 $k$ 个基捕获，重构误差越大。该估计在 3D 表面实验中与 oracle cotangent Laplacian 的特征值保持了良好的一致性（Figure 4），多数形状的相对误差均值低于 0.20。

### 3.5 关键创新总结

整个框架的核心创新在于**将谱分析的全流程——算子选择、离散化、特征分解——压缩为一个端到端的神经网络训练过程**。传统的三个步骤（显式选择算子→构造质量矩阵和刚度矩阵→调用数值特征求解器）被替换为三个隐式操作：（1）探测函数分布隐式定义算子类型；（2）$\mathbf{q}_1$ 的逐元素平方隐式编码度量矩阵；（3）最小化重构误差隐式执行特征分解。这一设计使得方法可以优雅地扩展到高维非结构化数据，而无需面对传统方法中图 Laplacian 构造的敏感性和数值求解的可扩展性瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2127_https_openaccess_thecvf_com_content_CVPR2026_html_Velich_Learning_Eigens/figures/005_Figure_5.jpg]]
*Figure 5: Estimated mass metric M from q1 (overfitting setting)*



## 实验与关键发现

### 核心实验设置与评估逻辑

本文的实验设计围绕一个中心命题展开：**在无需显式选择、离散化或特征分解任何算子的条件下，神经网络能否仅从非结构化点云中恢复出与经典谱方法高度一致的谱基？** 为回答这一问题，作者构建了三层递进的验证体系：

1. **过拟合设置（overfitting setting）**：在单个形状的表面点云上训练模型，以oracle cotangent Laplacian（需要完整三角网格连接信息的经典方法）作为真值参考，直接量化所学谱基的准确性。
2. **泛化设置（generalization setting）**：在大量表面点云上训练后，测试模型对未见形状（包括表面和三维体点云）的零样本泛化能力。
3. **高维流形设置**：在DINOv2图像特征流形上评估所学嵌入在下游聚类任务中的表现，与PCA、Isomap、Laplacian Eigenmaps、t-SNE、UMAP等经典流形学习方法对比。

### 主实验结果

#### 3D表面点云：与Oracle Cotangent Laplacian的定量对比

在过拟合设置下，模型仅使用点云坐标（无网格连接信息）学到的谱基，与oracle cotangent Laplacian的特征向量表现出高度一致性。**Table 1** 报告了不同截断级别k下的平均余弦相似度：

![[assets/figures/papers/paper_list_l2127_https_openaccess_thecvf_com_content_CVPR2026_html_Velich_Learning_Eigens/figures/007_Table_1.jpg]]
*Table 1: Average cosine similarity between predicted and oracle eigenfunctions at different truncation levels k, and mean relative eigenvalue discrepancy (overfitting setting). More in Appendix C*

- 在k≤10的低频范围内，所有测试形状的余弦相似度普遍超过0.93，其中**Armadillo达0.968，Bimba达0.964，Botijo达0.972，Kitten高达0.993**。这表明网络在无监督条件下，几乎完美地恢复了Laplacian算子的低频特征结构。
- 随着k增大（k≤50），部分形状的相似度出现显著下降：**Pegaso降至0.544，Laurent Hand降至0.568**。这揭示了方法在高频特征向量上的退化趋势，构成了一个明确的失败模式——高频谱基对探测函数分布和训练信号的敏感性更高。

**Figure 3** 从视觉层面印证了这一结论：所提方法生成的非归一化谱基（上排）与oracle结果高度相似，且从k个基向量重建的xyz坐标（下排）在细节上甚至略优于oracle重建。

特征值估计方面，**Table 1** 同时报告了相对特征值误差（mean ± std）：
- Armadillo: 0.200±0.126
- Bimba: 0.093±0.145
- Botijo: 0.153±0.092
- Elephant: 0.105±0.123

多数形状的均值低于0.20，考虑到特征值是从最差重构误差的倒数直接估计的（公式 $\lambda_{k+1} = 1/\max_i \|\mathbf{f}^{(i)} - \mathbf{f}_{\text{proj},k}^{(i)}\|_2^2$），且无需任何数值特征求解器，这一精度水平具有实际意义。**Figure 4** 提供了特征值谱的完整可视化对比。

![[assets/figures/papers/paper_list_l2127_https_openaccess_thecvf_com_content_CVPR2026_html_Velich_Learning_Eigens/figures/004_Figure_4.jpg]]
*Figure 4: Eigenvalues of the oracle cotangent Laplacian and our estimated ones (overfitting setting). More in Appendix C*

#### 度量矩阵的统一学习

**Figure 5** 展示了从第一个归一化特征向量 $\mathbf{q}_1$ 导出的对角度量矩阵 $M = \mathrm{diag}(\mathbf{q}_1 \odot \mathbf{q}_1)$。该度量矩阵与传统几何方法显式计算的质量矩阵（如Voronoi面积）在视觉上高度一致，验证了“度量与谱基统一学习”这一核心设计的有效性。这一机制使得方法无需对底层流形的维度和度量做任何先验假设。

#### 泛化能力：跨形状与跨维度

**Figure 6** 展示了模型在泛化设置下的关键能力：模型仅在表面点云上训练后，对未见形状（左栏）和三维体点云（右栏）均能产生有意义的平滑谱基。这体现了基础模型级别的泛化特性——网络学到的是谱分解的通用计算机制，而非对特定训练形状的过拟合记忆。但需注意，论文明确指出泛化设置下的精度低于过拟合设置（"smaller precision than in the overfitting setting"），这是当前方法的一个明确局限。

#### 高维图像流形上的聚类性能

**Figure 8** 报告了在DINOv2图像特征流形（STL10/CIFAR100，1500张图像子集）上，不同流形学习方法在50次随机运行中的平均聚类性能（NMI/ARI）。所提方法（Optimal-Approximation Eigenmaps）在不同嵌入维度 $k \in \{2, 5, 10, 50\}$ 上持续提供竞争性或最优性能。这一结果的意义在于：方法无需对高维流形构造图Laplacian（在高维情况下，构造可靠的图Laplacian本身就是一个敏感且困难的问题），而是通过探测函数隐式定义算子，直接学习谱嵌入。

**Figure 9** 提供了STL10子集的2D嵌入可视化，进一步支持了上述定量结论。

### 消融实验：探测函数分布的关键作用

**Figure 7** 展示了不同探测函数分布族（不同程度的高斯平滑、无平滑等）产生的谱基差异。这是整篇论文最核心的因果旋钮验证：

- 当探测函数通过k近邻图上的高斯核平滑生成时，隐式诱导出类Laplacian算子，学到的谱基与cotangent Laplacian高度一致。
- 改变探测函数的生成方式（如不同的平滑策略或分布），则对应不同的隐式算子，产生具有不同空间特性的谱基。

这一消融实验直接证实了论文的核心主张：**探测函数分布是控制所学算子类型的关键旋钮**，方法可以泛化到Laplacian以外的算子，只需改变探测函数的生成策略。

### 失败模式与局限性

综合已报告的证据，当前方法存在以下明确局限：

1. **高频退化**：在部分形状（Pegaso、Laurent Hand）上，k>20或k>50时余弦相似度降至0.544-0.568，高频特征向量的恢复质量显著下降。这可能是由于高频探测函数的重构误差信号较弱，训练信号不足以约束高频基的精确方向。

2. **泛化精度折损**：泛化设置下的精度明确低于过拟合设置，表明模型在零样本场景下尚无法达到逐形状优化的精度水平。

3. **训练计算成本**：论文明确指出训练需要大量时间和GPU资源，当前代码未经过高效编译和CUDA优化，这限制了方法在大规模数据集上的实用部署。

4. **算子类型的被动定义**：方法目前仅学习由探测函数分布隐式定义的单一算子类；若要针对特定目标算子获得最优结果，需仔细设计探测函数分布，这需要领域知识且缺乏自动化机制。

### 证据强度总结

| 结论 | 证据强度 | 关键支撑 |
|------|---------|---------|
| 低频谱基与oracle高度一致 | **强** | Table 1中k≤10余弦相似度>0.93，多形状验证 |
| 特征值估计准确 | **中强** | 相对误差均值<0.20，但方差较大 |
| 度量矩阵统一学习有效 | **中强** | Figure 5视觉验证，缺乏量化对比 |
| 泛化能力成立 | **中** | Figure 6定性展示，精度低于过拟合设置 |
| 高维聚类竞争性 | **中** | Figure 8竞争性表现，但非全面领先 |
| 探测函数分布是关键旋钮 | **中强** | Figure 7消融验证，但仅展示定性差异 |
| 高频退化是明确失败模式 | **中强** | Table 1中k>20时部分形状相似度骤降 |

### 补充图表

![[assets/figures/papers/paper_list_l2127_https_openaccess_thecvf_com_content_CVPR2026_html_Velich_Learning_Eigens/figures/002_Figure_3.jpg]]
*Figure 3: Unnormalized spectral basis (top) and xyz reconstruction from k basis vectors (bottom), using either the oracle cotangent Laplacian or our method (overfitting setting). Scalars are cosine similarities between basis vectors. We get similar if not more detailed reconstructions. More in Appendix C*

![[assets/figures/papers/paper_list_l2127_https_openaccess_thecvf_com_content_CVPR2026_html_Velich_Learning_Eigens/figures/008_Figure_6.jpg]]
*Figure 6: Unnormalized spectral basis v1 on unseen shapes, either surfaces (left) or volumes (right), when the model was trained on a wide collection of surface point clouds (generalization setting). Our model exhibits foundation-level generalization capabilities*

![[assets/figures/papers/paper_list_l2127_https_openaccess_thecvf_com_content_CVPR2026_html_Velich_Learning_Eigens/figures/009_Figure_8.jpg]]
*Figure 8: Average clustering performance over 50 runs of manifold learning methods on DINOv2 features of random data subsets (1500 images). Higher is better. More in Appendix C*

![[assets/figures/papers/paper_list_l2127_https_openaccess_thecvf_com_content_CVPR2026_html_Velich_Learning_Eigens/figures/003_Figure_2.jpg]]
*Figure 2: Learned eigenfunctions on [0,1] recover frequencyordered harmonics resembling the Laplacian’s spectrum*

![[assets/figures/papers/paper_list_l2127_https_openaccess_thecvf_com_content_CVPR2026_html_Velich_Learning_Eigens/figures/010_Figure_9.jpg]]
*Figure 9: Manifold learning visualization of a random subset of STL10 by 2D embedding DINOv2 features. More in Appendix C*



## 定位与知识库关联

### 1. 问题定位：绕过显式算子构造的谱学习

传统谱几何分析的核心瓶颈在于其“算子选择—离散化—特征分解”的三阶段流水线。以经典的 **Cotangent Laplacian** (Pinkall & Polthier, Experimental Mathematics 1993; Meyer et al., 2003) 为例：首先需显式选定 Laplace-Beltrami 算子作为目标，然后依赖三角网格的质量矩阵和刚度矩阵进行离散近似，最后调用数值广义特征求解器。该流程对网格质量和连通性高度敏感，且在高维非结构化数据（如三维以上点云、图像嵌入流形）上难以优雅扩展——高维情况下构造可靠的图 Laplacian 本身即为一类难题，其结果严重依赖局部密度和连接性选择。

本文提出的 **Optimal-Approximation Spectral Basis Learning** 从根本上改变了这一范式：不显式选择或构造任何算子，而是通过探测函数（probe function）分布隐式定义最优重构算子，由神经网络直接从点云坐标预测谱基。这一设计使得方法对数据维度不敏感，已在三维表面、三维体和高达数百维的图像特征流形上验证。

### 2. 与流形学习基线的关系

在流形学习领域，本文方法与以下基线构成明确的谱系关系：

- **Laplacian Eigenmaps** (Belkin & Niyogi, NIPS 2001)：所提方法中的 Optimal-Approximation Eigenmaps 可视为 Laplacian Eigenmaps 的直接推广。后者需显式构造图 Laplacian 并求解特征分解，而前者通过探测函数分布隐式诱导类 Laplacian 算子，无需显式构造矩阵。当探测函数由 k 近邻图上高斯核平滑生成时，隐式算子恰好对应于某种图 Laplacian 变体。

- **PCA** (Pearson, Philosophical Magazine 1901)：定理 3.2（Operator-Bounded PCA）建立了 Min-Max 最优逼近与 PCA 在 L-有界信号类上的等价性，使得本文的训练损失（公式 1）可以被理解为一种“算子约束的 PCA”。这解释了为何在高维图像流形实验中，所提方法在聚类性能上持续提供竞争性或优于 PCA 的表现（Figure 8）。

- **Isomap** (Tenenbaum et al., Science 2000)、**t-SNE** (van der Maaten & Hinton, JMLR 2008)、**UMAP** (McInnes et al., 2018)：这些方法侧重流形上的距离保持或邻域结构保持，而本文方法直接学习谱基，提供了一种正交的降维策略。在 DINOv2 特征聚类实验中（Figure 8），Optimal-Approximation Eigenmaps 在不同嵌入维度 k∈{2,5,10,50} 上持续提供竞争性或最优的 NMI/ARI 指标。

### 3. 核心创新机制：探测函数分布作为控制旋钮

本文的核心因果旋钮在于**探测函数分布的选择**。不同的探测函数分布族隐式定义了不同的最优重构算子，从而控制所学谱基的性质：

- 在 k 近邻图上通过高斯核平滑生成的探测函数，诱导出类 Laplacian 算子，产生平滑的、频率递增的谱基（Figure 2 在 [0,1] 区间上恢复了类 Fourier 基的谐波结构）；
- 改变平滑策略或分布类型（如不同程度的高斯平滑、无平滑），则对应不同的隐式算子，产生性质迥异的谱基（Figure 7 的消融实验证实了这一点）。

这一机制使得框架可以泛化到 Laplacian 以外的算子，而无需修改网络架构或训练流程。论文已将“学习探测函数分布本身以自动适配不同几何处理任务”列为未来工作方向。

### 4. 适用边界与局限

尽管方法展示了强大的灵活性和泛化能力，其适用边界和局限同样明确：

**数据要求方面**：方法仅需非结构化点云（任意维度 d），无网格或图连接要求，这显著降低了输入门槛。但训练计算成本高，需要大量时间和 GPU 资源，目前代码未经过高效编译和 CUDA 优化（论文已明确指出）。

**精度方面**：
- 在过拟合设置下，k≤10 时与 oracle Cotangent Laplacian 特征向量的余弦相似度普遍超过 0.93（Armadillo 0.968, Bimba 0.964, Botijo 0.972, Kitten 0.993；Table 1），特征值相对误差均值多数低于 0.20（Figure 4）。
- 但在部分形状（如 Pegaso、Laurent Hand）上，高频特征向量（k>20 或 k>50）与 oracle 的偏离较大，余弦相似度降至 0.544–0.568（Table 1）。
- 在泛化设置下，精度低于过拟合设置（论文明确声明“smaller precision than in the overfitting setting”）。

**算子类型方面**：目前仅学习由探测函数分布隐式定义的单一算子类；若要针对特定目标算子（如 LBO 的精确逼近）获得最优结果，需仔细设计探测函数分布。框架目前仅适用于对称正定算子，扩展到非对称或非自伴算子（如 Finsler-Laplacian）尚待探索。

**对比公平性方面**：在与 oracle Cotangent Laplacian 对比时，oracle 使用了完整的网格连接信息，而所提方法仅使用点云坐标，属于信息量不等条件下的对比（论文已明确标注）。泛化实验中模型仅在表面点云上训练，对三维体点云的泛化测试属于跨域评估，结果需结合领域差异理解。

### 5. 开放问题

论文明确或隐含地提出了以下开放问题：

1. **探测函数分布的学习**：如何学习探测函数分布本身，从而自动适配不同的几何处理任务和算子类型？（论文已将其列为未来工作）
2. **通用基础模型**：是否可能训练一个完全通用的基础模型，对任意维度的数据直接适用，而无需按维度重新训练？Figure 6 展示的跨维度泛化能力（从表面到体）已为此方向提供了初步证据。
3. **高维下游任务的应用**：学到的谱基在图神经网络中替代现有谱滤波器、在物理模拟中替代传统有限元基函数等应用潜力有多大？
4. **算子类型的扩展**：能否将框架扩展到非对称或非自伴算子，从而捕获更丰富的几何结构（如方向性扩散过程）？
5. **计算效率的工程化**：能否通过优化代码和 CUDA 实现显著降低训练开销，使该方法在大规模数据集上更具实用性？



## 原文 PDF

![[paperPDFs/CVPR_2026/Learning_Eigenstructures_of_Unstructured_Data_Manifolds.pdf]]
