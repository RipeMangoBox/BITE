---
title: "On the Wasserstein Geodesic Principal Component Analysis of probability measures"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/On_the_Wasserstein_Geodesic_Principal_Component_Analysis_of_probability_measures.pdf
project_link: null
code_link: null
openreview_forum_id: OJupg4mDjS
aliases:
- WGPCAPM
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "在Wasserstein空间直接优化测地线主成分而非切空间线性PCA。"
primary_logic: "GPCA对高斯测度用Otto纤维丛提升求解，对一般绝对连续测度用MLP参数化测地线并以Sinkhorn散度训练。"
claims:
- "高斯情形下，Bures-Wasserstein GPCA可提升到GL_d中的Frobenius范数优化问题。"
- "一般测度情形下，测地线被参数化为微分同胚和势函数诱导的推前路径。"
- "正交和相交正则化帮助学习与第一主成分正交相交的第二测地线主成分。"
- "GPCA在随机局部高斯数据上与TPCA目标差异小，但在接近SPD锥边界时能避免切线线性化失真。"
---

# On the Wasserstein Geodesic Principal Component Analysis of probability measures

> [!tip] 核心洞察
> On

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | On the Wasserstein Geodesic Principal Component Analysis of probability measures |
| 英文题名 | On the Wasserstein Geodesic Principal Component Analysis of probability measures |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=OJupg4mDjS) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method |  |
| Dataset | |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

本文研究 Wasserstein 空间中概率测度集合的**主成分分析（PCA）**，提出 **Wasserstein 测地线主成分分析（GPCA）**，旨在识别 Wasserstein 空间中最能捕捉数据变异模式的测地线。与传统的切空间 PCA（TPCA）不同，GPCA 直接在弯曲的测地线流形上进行降维，而非在一点处的线性化切空间中近似。

**核心方法定位**：GPCA 分两步处理。对于**高斯分布**，利用 Otto 纤维丛结构将 Bures-Wasserstein 几何中的计算提升到可逆线性映射空间 $GL_d$，将测地线 PCA 转化为 Frobenius 范数下的优化问题，从而获得精确解。对于**绝对连续概率测度**，采用神经网络（MLP）参数化 Otto 几何中的测地线——即参数化微分同胚 $\varphi$ 和函数 $f$，通过最小化 Sinkhorn 散度来学习测地线主成分。

**主要结果**：在高斯设定下，GPCA 在合成数据上恢复了已知的测地线结构，且与 TPCA 相比目标函数改进通常小于 1%，表明 TPCA 在局部已是良好近似。在真实数据实验中，GPCA 成功从 MNIST 数字、3D 点云（椅子、灯具）和彩色图像中恢复出语义上有意义的变异模式（如数字粗细、物体尺寸、颜色变化），而 TPCA 因线性化扭曲可能导致非正交交叉。正则化消融实验表明，正交性约束系数 $\lambda_O = 1.0$ 对恢复有区分力的第二主成分至关重要。



在经典的主成分分析（PCA）中，给定一组欧几里得空间中的点，目标是寻找低维仿射子空间以最小化投影误差。当数据点不再是向量，而是概率分布时，这一范式需要被重新建立：数据空间变为具有适当度量的概率测度空间，而线性子空间则被推广为测地线。

Wasserstein 距离因其在比较概率分布时能保持几何结构的能力，已成为机器学习与计算机视觉中的核心工具。然而，现有的分布降维方法大多采用切线空间线性化策略：先将所有概率测度映射到某个参考点（如 Wasserstein 重心）处的切空间，再在该线性空间中执行标准 PCA。这种“切线 PCA”（Tangent PCA, TPCA）虽然计算上可处理，但存在一个根本性的局限——它用切空间的平坦几何近似了 Wasserstein 空间本身的弯曲几何。当数据分布的离散度较大或曲率效应不可忽略时，切线近似会引入系统性偏差，导致提取的主成分无法忠实地反映数据在原始 Wasserstein 流形上的真实变异模式。

本文的核心动机正是填补这一缺口：直接在 Wasserstein 空间中进行**测地线 PCA**（Geodesic PCA, GPCA），即寻找一条（或多条）测地线，使得所有数据点到该测地线的 Wasserstein 距离平方和最小。这一目标在数学上自然且优雅，但其计算可行性长期受到两方面的制约。其一，对于一般概率测度，Wasserstein 测地线的显式参数化与优化缺乏有效手段；其二，即使对于结构良好的子类（如高斯分布），如何在非欧几里得几何中高效求解该变分问题也并非显然。

本文从两个互补的层面回应上述挑战。在**高斯分布**情形下，利用 Bures-Wasserstein 几何将问题提升到可逆线性映射空间，从而将测地线 PCA 转化为一个可精确求解的优化问题。在**绝对连续分布**情形下，提出一种基于神经网络的测地线参数化方法，通过 Otto 几何的视角将 Wasserstein 测地线表示为微分同胚群中水平线段的投影，并设计相应的正则化策略以保证多个主成分的正交相交。这两个层面的统一框架使得 GPCA 既能享受高斯情形下的精确性与理论可分析性，又能扩展到高维真实数据中的经验分布，从而在理论上弥合了 Wasserstein 几何的非线性结构与实际降维需求之间的鸿沟。



## 核心方法与创新机理

GPCA 的核心创新在于将主成分分析从 Wasserstein 空间的切空间线性近似**提升为真正的测地线流形优化**，从而在弯曲的统计流形上直接寻找数据变异的主方向。这一转变在两个层次上展开，分别对应不同的数据模态与计算策略。

### 从切线 PCA 到测地线 PCA 的范式转换

传统方法（如 TPCA）在 Wasserstein 空间的某个参考点（通常是 Wasserstein 重心）处构建切空间，并在该线性切空间内执行标准 PCA。这种线性化近似在数据分布偏离参考点较远、或流形曲率不可忽略时，会引入系统性偏差。GPCA 直接放弃了切空间近似，将主成分定义为**Wasserstein 空间中的测地线**，最小化数据点到该测地线的平方 Wasserstein 距离之和（式 1）：

$$\operatorname*{inf}_{t \mapsto \mu(t) \text{ geodesic}} \sum_{i=1}^{n} \operatorname*{inf}_{t_i} W_2^2(\mu(t_i), \nu_i)$$

这一目标函数本身就是非线性的：不仅需要优化测地线的参数化，还需要为每个数据点寻找其在测地线上的最优投影时间 $t_i$。因此，GPCA 求解的是一个**嵌套优化问题**，其解空间天然嵌入在流形的弯曲几何中。

### 两个层次的实现路径

GPCA 针对不同数据形式提供了两套互补的实现方案，各自解决了不同维度的核心瓶颈：

**高斯分布层次：纤维丛提升与 Bures-Wasserstein 几何**

对于高斯分布集合，GPCA 将问题从对称正定（SPD）矩阵的 Bures-Wasserstein 流形**提升到 Otto 纤维丛的全空间** $GL_d$。这一提升的关键洞察是：Bures-Wasserstein 距离可以表示为全空间中 Frobenius 范数的最小值（Proposition 1），从而将一个非线性的 SPD 流形优化问题转化为可逆矩阵空间中的更易处理的形式。在 $GL_d$ 中，测地线对应于水平直线，这使得优化目标大幅简化。该方案的核心 changed slot 在于：**用全空间的 Frobenius 范数替代 SPD 流形上的 Bures-Wasserstein 距离**，同时保持几何一致性。

**绝对连续分布层次：神经网络参数化测地线**

对于一般的绝对连续概率测度，测地线不再具有闭式解。GPCA 引入了一种全新的参数化策略：利用 Otto 的测地线表征，将测地线表示为 $\mu(t) = (\mathrm{id} + t \nabla f)_\# (\varphi_\# \rho)$，其中 $\varphi$ 是微分同胚，$f$ 是标量函数，两者均用**多层感知机（MLP）参数化**。这一方案的核心 changed slot 在于：**将无限维的测地线搜索空间压缩为两个神经网络 $\varphi_\theta$ 和 $f_\psi$ 的有限维参数空间**，同时保留 Wasserstein 几何的非线性结构。

第二主成分的构造进一步引入了**正交相交约束**。通过正则化项 $\mathcal{Z}$（强制两条测地线在指定时间相交）和 $\mathcal{O}$（强制水平向量场在 $L^2(\rho)$ 意义下正交），GPCA 确保后续主成分与已有主成分在几何上正交，这与欧氏 PCA 中主成分正交的性质在流形上形成对应。

### 与基线方法的本质差异

TPCA 与 GPCA 在随机二维高斯分布上的目标函数差异平均不足 1%（100 次试验），这表明在数据分布接近欧氏空间时，切空间近似足够精确。然而，当协方差矩阵接近 SPD 锥的边界时，GPCA 与 TPCA 的结果**显著分歧**（Figure 4）。这一分歧的根源在于：SPD 锥的边界附近，Bures-Wasserstein 度量的曲率急剧增大，切空间线性化引入的失真不可忽视。Proposition 4 量化了这一失真率：

$$\frac{BW_2^2(\Sigma, \Sigma')}{BW_{2,\bar{\Sigma}}^2(\Sigma, \Sigma')} = 1 - \left(\frac{a-b}{a+b}\right)^2 \cos^2\theta + O(\cdots)$$

该式揭示：当两个协方差矩阵的特征值差异 $(a-b)/(a+b)$ 增大、或方向夹角 $\theta$ 接近 0 或 $\pi$ 时，线性化失真加剧。GPCA 通过直接在弯曲流形上优化测地线，**从根本上规避了这一失真**，而无需对数据分布做任何局部线性假设。

### 需要人工核实的内容

目前的分析未提供 GPCA 与 TPCA 之外其他潜在基线（如 log-Euclidean PCA 或 Cholesky 系数上的欧氏 PCA）的定量对比。若需完整评估 GPCA 的创新性边界，建议补充与这些替代流形 PCA 方法的实验比较。



![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_OJupg4mDjS/figures/018_Figure_17.jpg]]
*Figure 17: For the lamp (left) and the chair (right) experiment, each point cloud is embedded in the plane according to its projection times onto the first and second principal components computed by the POINTNET + PCA method*

本文提出 Geodesic Principal Component Analysis（GPCA），在 Wasserstein 空间中对概率测度进行主成分分析。整体框架分为两个层次：

**高斯测度的 GPCA。** 对于中心化的高斯分布，Wasserstein 几何退化为 Bures-Wasserstein 几何。第一主成分定义为在对称正定（SPD）矩阵流形 $S_d^{++}$ 上最小化数据点到测地线投影的 Bures-Wasserstein 距离平方和的测地线：

$$\inf_{t \mapsto \Sigma(t) \text{ geodesic}} \sum_{i=1}^{n} \inf_{t_i} BW_2^2(\Sigma(t_i), \Sigma_i)$$

为规避 Bures-Wasserstein 距离的非线性，方法将问题提升到 Otto 纤维丛的全空间 $GL_d$，将目标转化为 Frobenius 范数下的优化。第二主成分定义为与第一成分正交相交的测地线，通过约束优化求解。

**绝对连续测度的 GPCA（GPCAGEN）。** 对于一般绝对连续概率测度，框架利用 Otto-Wasserstein 几何中测地线的参数化形式：

$$\mu(t) = (\mathrm{id} + t \nabla f)_\# (\varphi_\# \rho)$$

其中 $\rho$ 为参考测度，$\varphi \in \mathrm{Diff}(\Omega)$ 为微分同胚，$f$ 为标量函数。第一主成分的目标函数为：

$$\inf_{f, \varphi, t_1, \ldots, t_n} \mathcal{L}(f, \varphi, t_1, \ldots, t_n) := \sum_{i=1}^{n} W_2^2((\mathrm{id} + t_i \nabla f)_\# (\varphi_\# \rho), \nu_i)$$

**参数化与训练。** 函数 $f$ 和 $\varphi$ 分别由两个 MLP 参数化，每个 MLP 含四个隐藏层（大小 128），输出层大小分别为 1 和 $d$。第二主成分的优化在数据损失基础上加入两项正则化：相交正则化 $\mathcal{Z}$ 强制两条测地线在指定时间相交，正交正则化 $\mathcal{O}$ 确保水平向量场在 $L^2(\rho)$ 中正交。总目标为：

$$\mathscr{L}(f_{\psi_2}, \varphi_{\theta_2}, t_1^2, \ldots, t_n^2) + \lambda_I \mathscr{L}(\xi_{\theta,\psi}, \xi_{\theta_2,\psi_2}, t_{\mathrm{inter}}^1, t_{\mathrm{inter}}^2) + \lambda_O \mathcal{O}(g, h)$$

其中 $\lambda_I$ 和 $\lambda_O$ 均设为 1.0。训练流程遵循 Algorithm 1（GPCAGEN）的结构，在第七步将正则化项基于 minibatch 估计后加入损失。

**输入输出流。** 输入为一组概率测度（高斯分布或经验分布），输出为 Wasserstein 空间中的主测地线及其参数化。对于高斯情形，输出为 $S_d^{++}$ 上的测地线路径；对于一般测度，输出为经 MLP 参数化的微分同胚和标量函数，可沿测地线采样生成分布序列。



### GPCA 目标函数

GPCA 的核心思想是将第一主成分定义为 Wasserstein 空间中的一条测地线，使其到所有数据点的平方 Wasserstein 距离之和最小。对于高斯分布情形，该目标在 Bures-Wasserstein 度量下表述为：

$$
\operatorname*{inf}_{t \mapsto \Sigma(t) \text{ geodesic}} \sum_{i=1}^{n} \operatorname*{inf}_{t_i} BW_2^2(\Sigma(t_i), \Sigma_i)
$$

其中 $\Sigma(t)$ 是 $S_d^{++}$（对称正定矩阵空间）中的测地线，$\Sigma_i$ 为数据协方差矩阵，$BW_2^2$ 为 Bures-Wasserstein 平方距离。

### 高斯情形的纤维丛提升

直接优化上述目标面临 $BW_2^2$ 距离计算的非线性瓶颈。论文的关键技巧是将问题从底空间 $S_d^{++}$ 提升到 Otto 纤维丛的全空间 $GL_d$（可逆矩阵空间）。利用投影映射：

$$
\pi: A \in GL_d \mapsto AA^{\top} \in S_d^{++}
$$

在 $GL_d$ 中，$BW_2^2$ 距离等价于 Frobenius 范数下的距离，从而将非线性优化转化为更易处理的形式。第一和第二主成分测地线在全空间中表现为水平直线，其底空间投影即为所求的测地线主成分。

### 绝对连续测度情形的参数化

对于一般的绝对连续概率测度，GPCA 利用 Otto-Wasserstein 几何将测地线参数化为：

$$
\mu(t) = (\mathrm{id} + t \nabla f)_{\#} (\varphi_{\#} \rho)
$$

其中 $\rho$ 为参考测度，$\varphi \in \mathrm{Diff}(\Omega)$ 为微分同胚，$f$ 为标量函数。实际优化中，$\varphi$ 和 $f$ 分别用多层感知机（MLP）参数化，记为 $\varphi_\theta$ 和 $f_\psi$，均为四隐藏层、每层宽度 128 的网络。

第一主成分的优化目标为：

$$
\operatorname*{inf}_{f, \varphi, t_1, \ldots, t_n} \mathcal{L}(f, \varphi, t_1, \ldots, t_n) := \sum_{i=1}^{n} W_2^2((\mathrm{id} + t_i \nabla f)_{\#} (\varphi_{\#} \rho), \nu_i)
$$

### 第二主成分的正交约束

第二主成分的测地线需与第一主成分正交相交。为此引入两项正则化：

**相交正则化**，强制两条测地线在指定时刻重合：

$$
\mathcal{Z}(\xi_1, \xi_2, t_{\mathrm{inter}}^1, t_{\mathrm{inter}}^2) = \|\xi_1(t_{\mathrm{inter}}^1) - \xi_2(t_{\mathrm{inter}}^2)\|^2
$$

**正交正则化**，确保两测地线在交点的水平向量场在 $L^2(\rho)$ 意义下正交：

$$
\mathcal{O}(g, h) = \frac{\langle g, h \rangle_{L^2(\rho)}^2}{\|g\|_{L^2(\rho)}^2 \|h\|_{L^2(\rho)}^2}
$$

第二主成分的总损失为数据拟合项与上述正则项之和，正则系数 $\lambda_I$ 和 $\lambda_O$ 均设为 1.0。

### 线性化失真分析

论文还给出了在固定点 $\bar{\Sigma}$ 处线性化 Bures-Wasserstein 距离的失真比率（Proposition 4）。对于具有相同特征值的协方差矩阵，失真比率满足：

$$
\frac{BW_2^2(\Sigma, \Sigma')}{BW_{2, \bar{\Sigma}}^2(\Sigma, \Sigma')} = 1 - \left(\frac{a - b}{a + b}\right)^2 \cos^2\theta + O(\cdots)
$$

该公式揭示了当协方差矩阵接近锥边界（即 $a$ 与 $b$ 差异悬殊）或方向角 $\theta$ 偏离时，切线 PCA 的线性化近似与真实测地线距离之间的偏差会显著增大。这为 GPCA 相对于 TPCA 的优势提供了理论依据。



## 实验与关键发现

### 5.1 高斯分布上的 GPCA 与 TPCA 对比

在随机生成的 2D 高斯分布数据集上，GPCA 相对于 TPCA 的客观函数（式 11）改善幅度极小：100 次试验平均低于 1%。这一结果意味着，对于随机生成的高斯数据，精确的测地线 PCA 与切线空间线性化近似在客观函数值上几乎无差异。

然而，当协方差矩阵接近 SPD 锥边界时，两者差异显著。具体而言：

- **对角协方差矩阵（相同方向）**：GPCA 与 TPCA 的结果完全一致（Figure 3）。这是因为当所有矩阵可同时对角化时，Bures-Wasserstein 几何退化为欧氏几何，测地线与直线重合。
- **相同特征值、不同方向**：当协方差矩阵具有相同的特征值但取向不同时，GPCA 与 TPCA 的结果可能截然不同（Figure 4）。这些矩阵在 SPD 锥的水平截面上等距分布，TPCA 的线性近似在锥边界附近引入显著畸变，而 GPCA 保持了正确的测地线结构。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_OJupg4mDjS/figures/003_Figure_3.jpg]]
*Figure 3: GPCA on a set of diagonal covariance matrices $\Sigma _ { i j }$ with varying eigenvalues 1 \ $\leq$ \ $a _ { i } ^ { 2 }$ \ $\leq$ \ 3 , \ 1 $\leq$ \ $b _ { i } ^ { 2 }$ \ $\leq$ \ 2 The matrices form a planar grid inside the cone C of SPD matrices in equation 16 (left), and correspond to ellipses of varying width and height (right). The first component (red) captures the variation in a, while the second component (blue) captures the variation in b

这一现象的理论根源在于命题 4 所揭示的线性化畸变：当协方差矩阵具有相同特征值 $a^2, b^2$ 时，真实 Bures-Wasserstein 距离与线性化距离之比为 $1 - \left(\frac{a-b}{a+b}\right)^2 \cos^2\theta + O(\cdots)$。当 $a$ 与 $b$ 差异增大（即矩阵接近锥边界）时，畸变项权重增大，TPCA 的近似误差随之放大。

### 5.2 GPCAGEN 在合成数据上的验证

在已知测地线结构的合成数据集上，GPCAGEN 能够准确恢复前两个主成分。实验中，$f_\psi$ 和 $\varphi_\theta$ 均采用四层隐藏层（尺寸 128）的 MLP，输出层尺寸分别为 1 和 $d$。正则化系数 $\lambda_I$ 和 $\lambda_O$ 均设为 1.0，在所有实验中均能保证算法正常工作（Table 1 汇总了全部超参数）。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_OJupg4mDjS/figures/021_Table_1.jpg]]
*Table 1: Hyperparameters used across all experiments*

### 5.3 MNIST 实验

在人工构造的 MNIST 数据集上（Figure 5），GPCAGEN 成功恢复了两个正交相交的测地线：第一个成分捕捉颜色空间的变化，第二个成分则恢复从数字 1 到数字 2 的插值路径。这验证了算法在已知真实测地线结构时的恢复能力。

### 5.4 3D 点云实验：椅子与灯具

在椅子点云数据集上（Figure 6 顶行，Figure 10），第一个主成分区分椅子与扶手椅，第二个主成分捕捉座椅高度的变化。在灯具点云数据集上（Figure 6 中行，Figure 7 左），第一个主成分区分吊灯与立灯，第二个成分反映灯具结构的粗细变化。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_OJupg4mDjS/figures/009_Figure_7.jpg]]
*Figure 7: Each lamp point cloud (left) and each image (right) is embedded in the plane according to its projection times onto the first and second principal components computed by GPCAGEN*

Figure 7 进一步展示了每个灯具点云和图像在由前两个主成分投影时间构成的平面上的嵌入，直观呈现了 GPCAGEN 学到的变化模式。

### 5.5 与 TPCA 及 PointNet+PCA 的对比

在相同的椅子和灯具点云数据集上，TPCA 的结果如 Figure 15 和 Figure 16 所示。与 GPCAGEN 相比，TPCA 学到的变化模式存在差异，尤其在数据分布偏离线性结构时更为明显。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_OJupg4mDjS/figures/016_Figure_15.jpg]]
*Figure 15: For the chair and the lamp experiment, each point cloud is embedded in the plane according to its projection times onto the first and second principal components computed by TPCA*

PointNet+PCA 方法的结果如 Figure 17 所示。该方法首先使用 PointNet 提取点云特征，再在特征空间执行标准 PCA。与直接在 Wasserstein 空间中进行测地线 PCA 相比，这种两阶段方法无法利用 Wasserstein 几何的结构信息，其投影嵌入的语义分离度明显弱于 GPCAGEN。

### 5.6 正则化系数消融

Table 2 展示了不同 $\lambda_O$ 值对正交性正则化值和第二成分损失的影响。Table 3 展示了不同 $\lambda_I$ 值对两测地线交点距离和第二成分损失的影响。实验表明，将 $\lambda_I$ 和 $\lambda_O$ 均设为 1.0 在所有实验中均能取得稳定的平衡——既保证了相交和正交约束的满足，又不损害数据拟合质量。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_OJupg4mDjS/figures/022_Table_2.jpg]]
*Table 2: Orthogonality regularization value and second-component loss for different values of $\lambda _ { O }$*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_OJupg4mDjS/figures/025_Table_3.jpg]]
*Table 3: Squared Euclidean distance between $\xi _ { 1 } ( t _ { \mathrm { i n t e r } } ^ { 1 }$ ) and $\xi _ { 2 } ( t _ { \mathrm { i n t e r } } ^ { 2 }$ ) and second-component loss for different values of $\lambda _ { I }$

### 局限性说明

需要指出的是，GPCAGEN 的实验目前限于合成数据和相对简单的 3D 点云数据集。对于高维绝对连续分布的 GPCA 是否与限制在高斯子流形上的 GPCA 给出相同结果，在高维情形下仍是一个开放问题。此外，GPCAGEN 的计算开销显著高于 TPCA，每次迭代需要估计 Wasserstein 距离，限制了其在大规模数据集上的直接应用。

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_OJupg4mDjS/figures/019_Figure_18.jpg]]
*Figure 18: GPCA scores obtained on 60 new point clouds of chairs (never seen during training) and 60 point clouds of cars (left) / planes (right). The separation of the histograms indicates that GPCA can be used for outlier detection*



## 定位与知识库关联

### 与切空间 PCA（TPCA）的关系

GPCA 的直接前身是切空间 PCA（Tangent PCA, TPCA），后者在 Wasserstein 空间的某个参考点（通常为 Wasserstein 重心）处的切空间上执行线性 PCA，然后将结果投影回流形。GPCA 将 TPCA 的线性近似替换为精确的测地线优化，两者在以下条件下表现出不同行为：

- **对角协方差矩阵（相同取向）**：当所有协方差矩阵共享相同的特征向量取向时，GPCA 与 TPCA 产生完全相同的结果（Figure 3）。此时切空间近似不引入失真。
- **协方差矩阵接近锥边界**：当协方差矩阵靠近 SPD 锥的边界时，GPCA 与 TPCA 可能产生显著差异（Figure 4）。这是因为切空间线性化在锥边界附近的曲率效应更明显。
- **目标函数改进幅度**：在随机 2D 高斯分布的 100 次试验中，GPCA 相对于 TPCA 在式 (11) 目标函数上的平均改进不足 1%（Section 5.1）。这表明在一般随机设置下，TPCA 的近似质量已经较高，GPCA 的收益主要体现在几何结构特殊的边缘情形。

GPCA 的核心贡献在于将 PCA 概念从切空间的线性近似推广到流形上的精确测地线优化，而非在典型场景下显著超越 TPCA 的数值表现。

### 方法适用边界

**高斯分布情形（Gaussian GPCA）**：
- 适用于协方差矩阵可计算且维度适中的场景。
- 计算被提升到可逆线性映射空间 $GL_d$ 上，利用 Otto 纤维丛的结构将 Bures-Wasserstein 距离替换为 Frobenius 范数进行优化。
- 在一维高斯分布下，在绝对连续分布空间中执行 GPCA 与限制在高斯子流形上执行 GPCA 得到相同结果；高维情形下该等价性仍是开放问题。

**绝对连续分布情形（GPCAGEN）**：
- 通过神经网络（MLP）参数化 Otto-Wasserstein 几何中的测地线，适用于无法用有限维参数族表示的分布集合。
- 需要训练两个 MLP（$\varphi_\theta$ 和 $f_\psi$），均为四隐藏层、宽度 128 的结构；正则化系数 $\lambda_I$ 和 $\lambda_O$ 设为 1.0。
- 第二主成分的训练在 Algorithm 1 基础上增加了相交正则化项 $\mathcal{Z}$ 和正交正则化项 $\mathcal{O}$，通过 minibatch 估计后加入损失函数。

### 局限性与开放问题

1. **高维高斯等价性未解决**：在一维情形下已证明 GPCA 在绝对连续分布空间与高斯子流形上等价，但高维情形仍是开放问题（Section 4）。
2. **测地线相交与正交性的数值实现**：第二及更高阶主成分依赖于相交和正交性正则化项的软约束，而非硬约束，可能影响几何解释的严格性。
3. **神经网络参数化的收敛性**：GPCAGEN 依赖 MLP 对测地线的参数化能力和训练收敛性，缺乏理论上的收敛保证。
4. **可扩展性**：Gaussian GPCA 的计算涉及 $GL_d$ 上的优化，随维度 $d$ 增长的计算代价未在论文中系统评估；GPCAGEN 的每次迭代需要估计 Wasserstein 距离，在大规模数据集上的可扩展性有待验证。
5. **与现有流形 PCA 方法的系统比较缺失**：论文仅与 TPCA 进行了定量比较，未与其他流形 PCA 变体（如基于对数-欧几里得度量或 Cholesky 系数的欧几里得 PCA）进行系统性的定量对比。Figure 13 展示了不同度量下测地线的定性差异，但未给出对应的 PCA 性能指标。

### 知识库定位

GPCA 位于 Wasserstein 几何与非线性降维的交叉点，其方法谱系可概括为：

- **上游**：Otto 的 Wasserstein 几何形式化、McCann 测地线参数化、Bures-Wasserstein 度量理论、切空间 PCA 在黎曼流形上的通用框架。
- **平行工作**：基于对数-欧几里得度量的 SPD 流形 PCA、基于 Cholesky 分解的欧几里得 PCA（Figure 13 中定性比较了这些度量下的测地线行为）。
- **下游潜在方向**：Wasserstein 空间中的非线性降维、概率测度集合的生成建模、基于测地线主成分的分布插值与外推。

> **注意**：论文未引用具体基线工作的作者/会议/年份信息（如 MPGD 等），上述平行方法的描述仅基于论文内部的定性讨论。如需补充具体文献元数据，需手动检索验证。



## 原文 PDF

![[paperPDFs/ICLR_2026/On_the_Wasserstein_Geodesic_Principal_Component_Analysis_of_probability_measures.pdf]]
