---
title: "$\\boldsymbol{\\partial^\\infty}$-Grid: A Neural Differential Equation Solver with Differentiable Feature Grids"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/boldsymbolpartialinfty_Grid_A_Neural_Differential_Equation_Solver_with_Differentiable_Feature_Grids.pdf
project_link: https://4dqv.mpi-inf.mpg.de/DInf-Grid/
code_link: null
aliases:
- BPIGNDESDFG
- "∂∞-Grid"
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将特征网格与径向基函数（RBF）插值相结合，并采用多分辨率共位网格分解。"
primary_logic: "使用无限可微的RBF插值替代线性插值，使得基于网格的特征表示能够通过自动微分计算高阶导数，从而在保持网格训练速度优势的同时，能够求解微分方程。"
claims:
- "线性插值在网格节点处仅C⁰连续，在网格内部仅C¹连续，导致二阶及以上导数为零，无法用于求解微分方程。"
- "K-Planes在拉普拉斯监督下完全失败（PSNR为0），因为其线性插值不可微。"
- "∂∞-Grid在泊松方程图像重建任务中，梯度监督下PSNR达32.24，拉普拉斯监督下达12.19，而Siren分别为31.08和10.96，且训练时间从Siren的数小时缩短至25秒和15分钟。"
- "在亥姆霍兹方程求解中，K-Planes和Instant-NGP因线性分量导致二阶导数为零而完全失败，而∂∞-Grid能准确匹配参考解，且训练速度比Siren快4倍。"
---

# $\boldsymbol{\partial^\infty}$-Grid: A Neural Differential Equation Solver with Differentiable Feature Grids

> [!tip] 核心洞察
> 使用无限可微的RBF插值替代线性插值，使得基于网格的特征表示能够通过自动微分计算高阶导数，从而在保持网格训练速度优势的同时，能够求解微分方程。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ∂∞-Grid：一种具有可微特征网格的神经微分方程求解器 |
| 英文题名 | $\boldsymbol{\partial^\infty}$-Grid: A Neural Differential Equation Solver with Differentiable Feature Grids |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7G0L4cj452) · [Project](https://4dqv.mpi-inf.mpg.de/DInf-Grid/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | ∂∞-Grid |
| Dataset | 泊松方程图像重建（梯度监督）, 泊松方程图像重建（拉普拉斯监督） |

> [!tip] 效果简介
> - 泊松方程图像重建（梯度监督） 上，PSNR 为 32.24，对比 31.08 (Siren)，变化 +1.16。
> - 泊松方程图像重建（梯度监督） 上，训练时间 为 25秒，对比 数小时 (Siren)，变化 显著减少。
> - 泊松方程图像重建（拉普拉斯监督） 上，PSNR 为 12.19，对比 10.96 (Siren)，变化 +1.23。

## 概要

本文提出 **∂∞-Grid**，一种用于高效求解微分方程的可微特征网格表示方法。其核心瓶颈在于：现有的坐标基MLP神经求解器（如Siren）训练缓慢（需数小时），而基于线性插值的网格表示（如Instant-NGP、K-Planes）虽然训练快，但线性插值在网格节点处仅C⁰连续、内部仅C¹连续，导致二阶及以上导数为零，无法计算求解微分方程所需的梯度、雅可比矩阵和拉普拉斯算子。K-Planes在拉普拉斯监督下完全失败（PSNR为0）便是这一缺陷的直接证据。

**核心洞察**：用无限可微的径向基函数（RBF）插值替代线性插值，使基于网格的特征表示能够通过自动微分计算高阶导数，从而在保持网格训练速度优势的同时求解微分方程。方法的关键设计包括：（1）多分辨率共位网格分解，所有分辨率共享相同网格节点位置；（2）重叠的多环邻域（N₃，每维3个邻居），保证C∞连续性；（3）硬边界约束，通过距离加权函数强制边界条件。

**主要结果**：在泊松方程图像重建任务中，∂∞-Grid在梯度监督下PSNR达32.24（Siren为31.08），训练时间从Siren的数小时缩短至25秒；在拉普拉斯监督下PSNR达12.19（Siren为10.96），训练时间缩短至15分钟。在亥姆霍兹方程求解中，K-Planes和Instant-NGP因线性分量导致二阶导数为零而完全失败，而∂∞-Grid能准确匹配参考解，且训练速度比Siren快4倍。在1D平流方程中，∂∞-Grid的MAE为0.0023（INSR为0.0030），训练时间从INSR的5.33小时缩短至1.5分钟（200倍加速）。方法在热方程、Eikonal方程和Kirchhoff-Love布料模拟中也取得了成功验证。



求解微分方程（DE）是科学计算和物理模拟的核心任务。近年来，神经微分方程求解器（如基于坐标的MLP）通过学习一个连续函数 $\mathbf{u}(\mathbf{x})$ 来逼近方程的解，并通过自动微分计算所需的导数项。然而，现有方法面临一个根本性的瓶颈：**精度与速度难以兼得**。

**现有方法的缺口**：
1.  **基于坐标的MLP求解器（如Siren）**：采用正弦激活函数的MLP能够表达高频信号并计算高阶导数，但其训练极其缓慢，处理高分辨率图像需要数小时。其瓶颈在于每次前向传播都需要对整个MLP进行全连接计算，且优化过程收敛慢。
2.  **基于网格的混合表示（如Instant-NGP、K-Planes）**：这类方法将信号存储在可学习的特征网格中，通过高效的线性插值和一个小型解码器来加速训练。然而，线性插值在网格节点处仅 $C^0$ 连续（不可微），在网格内部仅 $C^1$ 连续，导致其二阶及以上导数为零。这从根本上阻止了它们计算求解微分方程所需的雅可比矩阵和拉普拉斯算子。实验证明，K-Planes在拉普拉斯监督下完全失败（PSNR为0）。
3.  **其他RBF网格方法（如NeuRBF）**：虽然使用了径向基函数（RBF），但其中心是自适应的且位于网格外，且每个查询点仅属于单一邻域，导致跨网格边界时出现不连续性，无法可靠地计算梯度。在梯度监督的图像重建任务中，NeuRBF完全失败（PSNR/SSIM仅为10.85/0.17）。

**本文的动机与核心洞察**：
本文的核心动机是**弥合上述两种范式之间的鸿沟**：在保留网格表示训练速度优势的同时，获得计算高阶导数（如梯度、拉普拉斯算子）的能力。作者提出**∂∞-Grid**，其核心洞察在于：用**无限可微的径向基函数（RBF）插值**替代线性插值。RBF插值在整个空间上都是 $C^\infty$ 连续的，使得基于网格的特征表示能够通过自动微分稳定地计算任意阶导数。此外，该方法引入了**多分辨率共位网格**（所有分辨率共享相同的网格节点位置）和**重叠的多环邻域**（$N_3$，即每维3个邻居），进一步保证了插值的连续性和高阶导数的稳定性。通过这一设计，∂∞-Grid在泊松方程图像重建任务中，梯度监督下PSNR达到32.24（Siren为31.08），且训练时间从Siren的数小时缩短至25秒；拉普拉斯监督下PSNR达到12.19（Siren为10.96），训练时间缩短至15分钟。在亥姆霍兹方程求解中，K-Planes和Instant-NGP因二阶导数为零而完全失败，而∂∞-Grid能准确匹配参考解，且训练速度比Siren快4倍。



## 核心方法与创新机理

∂∞-Grid 的核心创新在于**将特征网格的可扩展训练效率与径向基函数（RBF）的无限可微性相结合**，从而首次使得基于网格的神经表示能够通过自动微分计算求解微分方程所需的高阶导数（如拉普拉斯算子）。

**瓶颈：** 现有神经求解器存在不可兼得的矛盾：基于坐标的MLP（如Siren）虽然支持高阶导数，但训练速度极慢（数小时）；而基于网格的混合表示（如Instant-NGP、K-Planes）虽然训练快（秒级），但其线性插值在网格节点处仅C⁰连续、内部仅C¹连续，二阶及以上导数恒为零，无法用于求解微分方程。K-Planes在拉普拉斯监督下PSNR为0，完全失败。

**因果机制：** 作者将问题分解为两个关键的可变组件——插值方法和网格结构，并同时替换了它们。

1.  **插值方法：从d-线性插值到RBF插值。** 线性插值在网格节点处不可微，而作者采用归一化的高斯RBF核进行插值。由于高斯核是C^∞连续的，且RBF中心固定在网格节点上、采用重叠的多环邻域（N_3，每维3个邻居），插值权重对查询坐标的任意阶导数均可通过自动微分计算。这直接解决了“网格表示无法求高阶导”的根本瓶颈。

2.  **网格结构：从单分辨率或非共位多分辨率到共位多分辨率网格。** 作者引入多分辨率共位网格（co-located grids），所有分辨率共享相同的网格节点位置。这种设计使得不同尺度的插值特征可以稳定地拼接，加速全局梯度传播，并有效捕获高频信号。消融实验（Figure II）证实，多分辨率相比单分辨率在更少迭代次数内达到更高PSNR。

3.  **边界条件：从软约束到硬约束。** 通过距离加权函数B(x) = 1 - exp(-||x - x_∂Ω||²/σ) 强制边界条件，已知可改善收敛性。

**证据强度：** 核心证据链完整且置信度高。论文明确给出了线性插值不可微的数学分析（Figure III），并通过实验验证了关键因果链：K-Planes和Instant-NGP在需要二阶导数的亥姆霍兹方程上完全失败（ℓ1误差远高于参考解），而∂∞-Grid能准确匹配参考解，且训练速度比Siren快4倍（约6分钟 vs 约24分钟）。在泊松方程图像重建中，∂∞-Grid在梯度监督下PSNR达32.24（Siren为31.08），拉普拉斯监督下达12.19（Siren为10.96），训练时间从Siren的数小时分别缩短至25秒和15分钟。

**失败模式：** 需要手动验证的潜在弱点包括：RBF形状参数ε和邻域大小ρ对重建质量敏感（Table 2）；RBF在域边界附近可能出现Runge现象；网格方法受维度灾难影响，在3D中比2D慢得多；效率提升主要依赖结构化笛卡尔网格，在流形上求解PDE时优势丧失；与传统数值求解器（如多重网格法）相比可能效率不高。



![[assets/figures/papers/iclr26_0001_7G0L4cj452_boldsymbolpartialinfty-Grid_A_Neural_Differentia/figures/036_Figure_34.jpg]]
*Figure 34: Figure V: Solutions to the Eikonal equation from oriented point clouds. For each method, we visualise 2D slices (left) and the mesh extracted from the SDF (right). Instant-NGP and NeuRBF can overfit when groundtruth SDF supervision ( ${ \mathcal { L } } _ { \mathrm { s d f } }$ ) is available, but they cannot reliably solve the Eikonal equation given partial pointcloud observations ( $\mathcal { L } _ { \mathrm { e i k o n a l } }$ ) because their gradients are not differentiable across grid boundaries (Fig. III). In contrast, our smooth formulation handles these gradients and solves the Eikonal problem comparably to baselines such as a sinusoidal MLP

∂∞-Grid 的整体 pipeline 围绕“可微特征网格 + RBF 插值 + 解码器 + 自动微分”这一核心链路展开，旨在同时获得网格表示的训练速度和 MLP 表示的高阶可微性。

**输入与采样阶段：** 从定义域 Ω（例如 2D 图像域、3D 空间域或时空域）中采样查询坐标 **x**。这些坐标是后续所有微分和插值操作的基点。

**多分辨率共位特征网格：** 这是核心存储模块。系统维护一组多分辨率（S 个层级）的共位特征网格 {Fₛ}，每个网格节点存储一个可学习的特征向量。所有分辨率共享相同的网格节点位置（共位设计），这保证了不同尺度特征在空间上对齐，使得后续特征拼接在物理上具有一致性。每个网格的初始值从均匀分布 U(−10⁻⁴, 10⁻⁴) 中采样。

**无限可微的 RBF 插值器：** 这是解决瓶颈的关键模块。对于每个查询坐标 **x**，系统不是使用传统的 d-线性插值，而是采用径向基函数（RBF）插值。具体来说，对于每个尺度 s，系统在预计算的重叠邻域 N₃(**x**)（每维 3 个邻居，共 (2ρ)^d 个节点）内，使用归一化的高斯核计算插值权重：

$$w(\mathbf{x}, \mathbf{x}_i) = \frac{\varphi(\|\mathbf{x} - \mathbf{x}_i\|)}{\sum_{j \in \mathcal{N}(\mathbf{x})} \varphi(\|\mathbf{x} - \mathbf{x}_j\|)}$$

由此提取出平滑的、查询相关的插值特征 **fₛ**(**x̄**)。所有尺度的插值特征被拼接为 **f**(**x**)。RBF 插值的关键优势在于其 C^∞ 连续性，这直接解决了线性插值在网格节点处仅 C⁰ 连续、在网格内部仅 C¹ 连续的问题，使得后续可以通过自动微分计算二阶及以上的高阶导数。

**特征解码器：** 拼接后的多尺度特征 **f**(**x**) 被送入解码器 d(·; Θ)，输出最终的目标信号 **u**(**x**) = d(**f**(**x**; **F**); Θ)。解码器可以是简单的线性层，也可以是带平滑激活函数（如 tanh）的小型 MLP。

**硬边界约束调制：** 为了确保解的唯一性和稳定性，系统采用硬约束而非软约束。通过一个距离加权函数 B(x) = 1 − exp(−‖x − x_∂Ω‖² / σ) 来调制输出：

$$\mathbf{u}(\mathbf{x}) = \mathbf{d}(\mathbf{f}(\mathbf{x}; \mathbf{F}); \Theta) \mathcal{B}(\mathbf{x}) + \mathbf{h}(\mathbf{x}) \big(1 - \mathcal{B}(\mathbf{x})\big)$$

该机制在域边界处强制满足 Dirichlet 边界条件，在域内部则让网络自由学习。

**自动微分引擎与 PDE 损失：** 解码后的信号 **u**(**x**) 通过自动微分（autograd）计算其对输入坐标 **x** 的梯度、雅可比矩阵和拉普拉斯算子。这些微分量被代入 PDE 残差损失函数：

$$\mathcal{L}(\mathbf{F}, \boldsymbol{\Theta}) = \int_{\Omega} \mathcal{F}(\cdot) d\mathbf{x} = \sum_{i \in \mathcal{D}} \mathcal{F}\left(\mathbf{x}_i, \mathbf{u}(\mathbf{x}_i), \nabla_{\mathbf{x}_i} \mathbf{u}(\mathbf{x}_i), \nabla_{\mathbf{x}_i}^2 \mathbf{u}(\mathbf{x}_i), \dots; g(\mathbf{x}_i)\right)$$

该损失函数直接编码了待求解的微分方程（如泊松方程、亥姆霍兹方程、Eikonal 方程等），优化目标是最小化 PDE 残差。整个流程通过反向传播同时优化网格特征 **F** 和解码器权重 Θ。

**模块关系总结：** 特征网格提供局部、可学习的表示能力；RBF 插值桥接了离散网格与连续坐标，并提供了高阶可微性；解码器将多尺度特征融合为最终信号；自动微分将信号转化为 PDE 所需的微分量；PDE 损失驱动整个系统的优化。相比 Siren 等纯 MLP 方法，网格结构使得梯度传播更快、训练收敛更迅速；相比 K-Planes 和 Instant-NGP 等线性插值网格方法，RBF 插值使得计算高阶导数成为可能。



∂∞-Grid的核心设计围绕一个瓶颈展开：基于坐标的MLP神经求解器（如Siren）训练极慢，而基于网格的表示（如Instant-NGP、K-Planes）虽然训练快，但其线性插值在网格节点处仅C⁰连续，在网格内部仅C¹连续，导致二阶及以上导数为零，无法计算求解微分方程所需的雅可比矩阵和拉普拉斯算子。K-Planes在拉普拉斯监督下完全失败（PSNR为0）直接证实了这一缺陷。

**因果旋钮**在于将特征网格与径向基函数（RBF）插值相结合，并采用多分辨率共位网格分解。核心洞察是：使用无限可微的RBF插值替代线性插值，使得基于网格的特征表示能够通过自动微分计算高阶导数，从而在保持网格训练速度优势的同时求解微分方程。

### 模块化流水线

1. **多分辨率共位特征网格**：存储可学习的局部特征向量，每个网格节点一个特征向量，所有分辨率共享相同的网格节点位置。
2. **RBF插值器**：对查询坐标进行无限可微的插值，提取平滑的查询相关特征。
3. **特征解码器**：将拼接后的多尺度插值特征映射到目标信号，可以是线性层或小型MLP（tanh激活）。
4. **自动微分引擎**：计算解码后信号相对于输入坐标的梯度、雅可比矩阵和拉普拉斯算子。
5. **PDE损失函数**：根据微分方程残差定义损失，可选地包含边界约束或数据项。

### 关键公式

**信号组合**：场 $\mathbf{u}$ 表示为特征编码器 $\mathbf{f}$ 和解码器 $\mathbf{d}$ 的组合

$$
\mathbf{u}(\mathbf{x}) = \mathbf{d}(\mathbf{f}(\mathbf{x}; \mathbf{F}); \Theta)
$$

其中 $\mathbf{F}$ 是网格节点特征，$\Theta$ 是解码器权重。

**插值特征**：查询点 $\mathbf{x}$ 处的特征向量是相邻网格节点特征向量的加权和

$$
\mathbf{f}(\mathbf{x}) = \sum_{i \in \mathcal{N}(\mathbf{x})} w(\mathbf{x}, \mathbf{x}_i) \mathbf{F}(\mathbf{x}_i)
$$

**RBF插值权重**：使用归一化的高斯核，保证C∞连续性

$$
w(\mathbf{x}, \mathbf{x}_i) = \frac{\varphi(\|\mathbf{x} - \mathbf{x}_i\|)}{\sum_{j \in \mathcal{N}(\mathbf{x})} \varphi(\|\mathbf{x} - \mathbf{x}_j\|)}
$$

**硬边界条件**：通过距离加权函数 $\mathcal{B}(\mathbf{x}) = 1 - \exp(-\|\mathbf{x} - \mathbf{x}_{\partial\Omega}\|^2 / \sigma)$ 强制实现

$$
\mathbf{u}(\mathbf{x}) = \mathbf{d}(\mathbf{f}(\mathbf{x}; \mathbf{F}); \Theta) \mathcal{B}(\mathbf{x}) + \mathbf{h}(\mathbf{x})(1 - \mathcal{B}(\mathbf{x}))
$$

**PDE残差损失**：时空域上的积分

$$
\mathcal{L}(\mathbf{F}, \Theta) = \int_{\Omega} \mathcal{F}(\cdot) d\mathbf{x} = \sum_{i \in \mathcal{D}} \mathcal{F}\left(\mathbf{x}_i, \mathbf{u}(\mathbf{x}_i), \nabla_{\mathbf{x}_i} \mathbf{u}(\mathbf{x}_i), \nabla_{\mathbf{x}_i}^2 \mathbf{u}(\mathbf{x}_i), \dots; g(\mathbf{x}_i)\right)
$$

### 关键设计选择

- **邻域定义**：采用重叠的多环邻域 $\mathcal{N}_3$（每维3个邻居），保证C∞连续性和稳定的高阶导数。邻域索引对所有训练和测试样本预计算。
- **多分辨率共位网格**：所有分辨率共享相同的网格节点位置，使得多尺度特征可以简单拼接。消融实验表明，多分辨率相比单分辨率能在更少迭代次数内获得更高PSNR。
- **RBF形状参数**：固定形状的高斯RBF，形状参数 $\varepsilon$ 和邻域大小 $\rho$ 对重建质量有影响，存在最优配置（见Table 2消融研究）。
- **特征初始化**：每个特征网格从均匀分布 $\mathbf{F}_s \sim \mathcal{U}(-10^{-4}, 10^{-4})$ 初始化。



## 实验与关键发现

### 泊松方程图像重建：梯度与拉普拉斯监督

∂∞-Grid 的核心优势在于其能够利用高阶导数监督进行信号重建，这是对线性插值网格方法的直接突破。在泊松方程图像重建任务中（Table 1, Figure 4），模型分别从目标图像的梯度场和拉普拉斯场进行重建。在梯度监督下，∂∞-Grid 的 PSNR 达到 32.24，高于 Siren 的 31.08；而在更具挑战性的拉普拉斯监督下，∂∞-Grid 的 PSNR 为 12.19，Siren 为 10.96。更重要的是训练时间：Siren 需要数小时，而 ∂∞-Grid 在梯度监督下仅需 25 秒，在拉普拉斯监督下也只需 15 分钟。K-Planes 在梯度监督下表现挣扎（PSNR 显著低于其他方法），在拉普拉斯监督下完全失败（PSNR 为 0）。这一失败模式的因果机制在于线性插值的 C⁰ 连续性导致二阶导数为零，无法计算拉普拉斯算子。该证据强度很高（Table 1 明确报告了数值），直接验证了核心瓶颈。

![[assets/figures/papers/iclr26_0001_7G0L4cj452_boldsymbolpartialinfty-Grid_A_Neural_Differentia/figures/015_Table_1.jpg]]
*Table 1: Comparison against Siren (Sitzmann et al., 2020) and K-planes (Fridovich-Keil et al., 2023) for image reconstruction (Fig. 4). $\partial ^ { \infty }$ -Grid achieves higher PSNR with substantially reduced training time than Siren. K-planes struggle (for gradient supervision) or fail (for Laplacian) due to non-differentiable interpolation

### 亥姆霍兹方程：二阶 PDE 求解的架构验证

亥姆霍兹方程（二阶 PDE）的求解进一步展示了架构差异导致的成败分界（Figure 5, Figure VI）。K-Planes 和 Instant-NGP 完全失效，因为其线性分量在计算二阶导数时为零，无法表示波动场。∂∞-Grid 的解与参考解高度吻合，且训练时间约为 6 分钟，比 Siren 的约 24 分钟快 4 倍。对于更高波数（ω=30, 40），∂∞-Grid 仍能保持整体准确性，但在 ω=40 时波源附近出现可察觉的误差（Figure VII, Table I）。该误差可能源于 RBF 插值在源点附近的平滑效应，或网格分辨率不足以捕获极高频率的振荡。这暴露了方法的一个失败模式：对于极高频信号，即使 RBF 无限可微，有限网格分辨率仍会限制精度。

### 平流方程与热方程：时变 PDE 的泛化能力

在 1D 平流方程上（Table II），∂∞-Grid 的 MAE 为 0.0023，略优于 INSR 的 0.0030，但训练时间从 INSR 的 5.33 小时骤降至 1.5 分钟（约 200 倍加速）。这一巨大加速的因果机制在于：网格表示允许并行查询和快速前向传播，而 INSR 作为 MLP 需要逐点计算且收敛缓慢。在 2D 平流方程（高斯波）和热方程上，∂∞-Grid 均能成功求解（Section H.2, Section G），热方程的 MAE 为 0.004。这些结果共同表明，∂∞-Grid 的加速优势在时变 PDE 上同样成立，且不局限于椭圆型方程。

### 消融研究：多分辨率与 RBF 参数

多分辨率共位网格的有效性通过消融实验得到验证（Figure II）。单分辨率网格在 PDE 损失收敛速率上与多分辨率网格相似，但在 PSNR 指标上，多分辨率架构在更少的迭代次数内达到更高的重建质量。这表明多分辨率分解的主要收益不在于加速损失下降，而在于更有效地捕获多频段信号，从而提升重建精度。RBF 形状参数 ε 和邻域大小 ρ 存在最优配置（Table 2），过小或过大均会降低重建质量。ε 控制 RBF 核的有效宽度，影响插值的平滑程度和邻域覆盖范围。

### 与 NeuRBF 的对比：邻域设计的决定性作用

NeuRBF 也使用 RBF 插值，但其失败模式揭示了邻域设计的关键性（Figure I, Figure V）。在梯度监督的图像重建中，NeuRBF 的 PSNR/SSIM 仅为 10.85/0.17，而 ∂∞-Grid 达到 29.44/0.87。NeuRBF 能拟合信号本身，但无法计算准确的梯度。其根本原因在于 NeuRBF 将 RBF 中心置于网格外并自适应调整，且每个查询点仅限制在一个单环邻域内，导致邻域边界处出现不连续性（Figure III）。∂∞-Grid 采用固定网格节点上的重叠多环邻域（N₃），保证了 C^∞ 连续性。在 Eikonal 方程求解中，Instant-NGP 和 NeuRBF 同样因梯度在网格边界处不可微而失败，而 ∂∞-Grid 能可靠地求解（Figure V）。这一对比强烈表明：RBF 本身并非充分条件，重叠邻域和固定中心的设计才是保证高阶可微性的决定性因果机制。

### 与 PINN 的对比

与使用 GELU 激活函数的标准 PINN 相比（Figure IV），∂∞-Grid 在图像重建和亥姆霍兹方程求解上均显著更优。PINN (GELU) 的 PSNR/SSIM 约为 19/0.65，而 ∂∞-Grid 为 29.44/0.87。PINN 难以处理高频内容，而 ∂∞-Grid 的多分辨率网格天然具备多频段表示能力。

### 补充图表

![[assets/figures/papers/iclr26_0001_7G0L4cj452_boldsymbolpartialinfty-Grid_A_Neural_Differentia/figures/018_Figure_6.jpg]]
*Figure 6: Kirchhoff-Love Simulation (Kairanda et al., 2024). $\partial ^ { \infty }$ -Grid captures fine-grained cloth wrinkles by solving a highly nonlinear problem. Table 2: Ablation study for varying RBF shapes ε and neighbourhood sizes $\rho$ for the high-resolution gradientbased image reconstruction in Fig. I

![[assets/figures/papers/iclr26_0001_7G0L4cj452_boldsymbolpartialinfty-Grid_A_Neural_Differentia/figures/040_Table_3.jpg]]
*Table 3: Table I: Helmholtz equation with higher wavenumbers: We report ℓ1 error with the reference solution for the real and imaginary parts of the wavefield. Parameter count: 45.19k for ω = 20, 30; 176.71k for $\omega$ = 4 0 Figure VII: Results for Helmholtz equation with $\omega$ = 3 0 , 40 compared with closed-form solutions. Our $\partial ^ { \aa \hat { \infty } }$ -Grid method remains accurate overall, with minor errors near the source at $\omega$ = 4 0

![[assets/figures/papers/iclr26_0001_7G0L4cj452_boldsymbolpartialinfty-Grid_A_Neural_Differentia/figures/042_Table_4.jpg]]
*Table 4: Table II: 1D Advection comparison with INSR (Chen et al., 2023a) and Grid solver (Fedkiw et al., 2001)*



## 定位与知识库关联

### 与基线方法的关系

∂∞-Grid 的定位直接源于现有神经微分方程求解器的两个对立范式之间的瓶颈。第一类是基于坐标的 MLP 神经求解器（以 Siren 为代表），其正弦激活函数支持无限可微性，能够通过自动微分计算求解 PDE 所需的高阶导数（梯度、雅可比、拉普拉斯算子），但训练极其缓慢——在泊松方程图像重建任务中需要数小时。第二类是基于网格的混合表示（Instant-NGP、K-Planes），它们通过局部线性插值从可学习特征网格中提取查询特征，训练速度极快（秒级），但其线性插值在网格节点处仅 C⁰ 连续、网格内部仅 C¹ 连续，导致二阶及以上导数为零，从根本上无法求解微分方程。论文的核心证据显示，K-Planes 在拉普拉斯监督下完全失败（PSNR 为 0），因为其线性分量对二阶导数的贡献为零；Instant-NGP 在亥姆霍兹方程求解中也因同样原因崩溃。

∂∞-Grid 的关键因果旋钮是将网格的插值方式从 d-线性插值替换为径向基函数（RBF）插值，并采用多分辨率共位网格分解。具体来说，它使用归一化的高斯核进行插值，每个查询点的特征向量是其邻域内网格节点特征向量的加权和，权重由 RBF 核的归一化结果给出。由于高斯核是无限可微的（C^∞），整个特征提取过程可以通过自动微分计算任意阶导数，从而在保持网格训练速度优势的同时，具备了求解 PDE 的能力。

### 与 NeuRBF 的区分

在 RBF 网格表示的子领域中，NeuRBF 也使用了 RBF 插值，但存在两个关键差异。第一，NeuRBF 将 RBF 中心置于网格外部并使其自适应，而 ∂∞-Grid 将 RBF 中心固定在网格节点上。第二，NeuRBF 将每个查询点限制在单一邻域内，导致邻域边界处的导数不连续；∂∞-Grid 使用重叠的多环邻域（N₃，即每维 3 个邻居），保证了跨邻域的 C^∞ 连续性。实验证据表明，这一差异是决定性的：在梯度监督的图像重建中，NeuRBF 完全失败（PSNR/SSIM 为 10.85/0.17），而 ∂∞-Grid 成功恢复图像（29.44/0.87）；在从有向点云求解 Eikonal 方程时，NeuRBF 无法恢复光滑表面，而 ∂∞-Grid 的表现与正弦 MLP 基线相当。

### 适用边界

∂∞-Grid 的适用性受限于以下几个因素。首先，RBF 插值对形状参数 ε 和邻域大小 ρ 敏感，存在最优配置，偏离最优值会导致重建质量下降（消融实验 Table 2 证实了这一点）。其次，RBF 方法在域边界附近可能出现 Runge 现象，影响边界附近的重建精度。第三，网格方法受维度灾难影响——在 3D 中拟合 SDF 比 2D 慢得多，插值计算成本随输入维度指数增长。第四，效率提升主要得益于结构化笛卡尔网格，当在流形上求解 PDE 时，这一优势会丧失。最后，与传统的数值求解器（如多重网格法）相比，∂∞-Grid 可能效率不高，论文作者也承认需要更全面的比较来指导未来工作。

### 局限与开放问题

论文明确承认的局限性包括：插值特征对 RBF 形状参数敏感，可能导致一定程度的平滑；边界附近的 Runge 现象影响精度；网格方法的维度灾难；以及在非结构化域上效率优势的丧失。开放的待解决问题包括：需要建立截断邻域下 C^∞ 连续性的严格理论保证；对于更高维输入，探索投影到低维空间的策略以提高可扩展性；自定义 CUDA 内核实现能否进一步加速优化。



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/boldsymbolpartialinfty_Grid_A_Neural_Differential_Equation_Solver_with_Differentiable_Feature_Grids.pdf

![[paperPDFs/ICLR_2026/boldsymbolpartialinfty_Grid_A_Neural_Differential_Equation_Solver_with_Differentiable_Feature_Grids.pdf]]
