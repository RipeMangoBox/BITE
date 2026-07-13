---
title: "Overparametrization bends the landscape: BBP transitions at initialization in simple Neural Networks"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Overparametrization_bends_the_landscape_BBP_transitions_at_initialization_in_simple_Neural_Networks.pdf
project_link: null
code_link: null
openreview_forum_id: xDLE5n3x9Y
aliases:
- FTBTAHAI
- OBLBTAISNN
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "学生网络宽度p（过参数化程度）和损失函数归一化参数a是主要因果旋钮：a控制Hessian条件数及谱左边缘类型，p通过平滑损失景观降低α_BBP，且两者共同决定相变是连续还是不连续，从而影响有限N下的实际恢复性能。"
primary_logic: "过参数化不仅能降低BBP相变所需的信噪比，甚至在大过参数化极限下可达到信息论弱恢复阈值p*/2；同时它可改变相变的定性性质——从不连续变为连续（或相反），但不连续相变的强有限尺寸效应导致实际观察到的相变阈值远低于理论预测的α_BBP，这一效应可由外推的α_0刻画，且α_0随p单调递减，确保了过参数化在有限维场景中的优势。"
claims:
- "BBP相变条件为离群特征值等于谱左边缘：λ_*(α_BBP) = λ_-(α_BBP)"
- "α_BBP(p)随p增加总体下降，但在某些a下出现非单调行为；当p超过临界值p_c(a)时，相变变为不连续。"
- "在不连续BBP相变中，有限N的数值相变点远低于预测的α_BBP，且外推的α_0随p单调递减。"
- "无限过参数化极限(p→∞)下，α_BBP^{p=∞} = p*(a+1)/2，最小值在a=0时为p*/2，匹配弱恢复阈值。"
---

# Overparametrization bends the landscape: BBP transitions at initialization in simple Neural Networks

> [!tip] 核心洞察
> 过参数化不仅能降低BBP相变所需的信噪比，甚至在大过参数化极限下可达到信息论弱恢复阈值p*/2；同时它可改变相变的定性性质——从不连续变为连续（或相反），但不连续相变的强有限尺寸效应导致实际观察到的相变阈值远低于理论预测的α_BBP，这一效应可由外推的α_0刻画，且α_0随p单调递减，确保了过参数化在有限维场景中的优势。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 过度参数化弯曲损失景观：简单神经网络初始化时的BBP相变 |
| 英文题名 | Overparametrization bends the landscape: BBP transitions at initialization in simple Neural Networks |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=xDLE5n3x9Y) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | Field-theoretic BBP transition analysis of the Hessian at initialization |
| Dataset | Teacher-student setup with p*=1, varying a and p, Teacher-student with p=p*=1, continuous BBP (a=...), discontinuous BBP (a=...), Infinite overparametrization limit (p→∞) for general p* |

> [!tip] 效果简介
> - Teacher-student setup with p*=1, varying a and p 上，α_BBP 为 p=2,3,... overparameterized，对比 p=1 (no overparam.)，变化 α_BBP is generally lower for larger p, but non-monotonic near transition to discontinuous; minimum shifts with a。
> - Teacher-student with p=p*=1, continuous BBP (a=...) 上，φ (fraction of times smallest eigenvector aligned with signal) 为 predicted α_BBP，对比 random chance (φ≈0.5)，变化 φ transitions from 0 to 1 at predicted α_BBP; intersection of finite-N curves matches theory。
> - Teacher-student with p=p*=1, discontinuous BBP (a=...) 上，φ 为 predicted α_BBP (large N limit)，对比 empirical transition from simulations，变化 empirical transition occurs at lower α due to finite-size effects; estimated α_0 lies below predicted。

## 概要

本文研究两层软委员会机（soft-committee machine）在二次激活函数下，过参数化如何改变损失景观的局部曲率结构。核心问题是：在随机初始化点，Hessian矩阵的谱何时能提取出关于教师网络（即真实信号）的信息？这一信息可恢复性由Baik–Ben Arous–Peché（BBP）相变刻画——只有当信噪比（以样本数-参数维度比 $\alpha$ 度量）超过临界阈值 $\alpha_{\mathrm{BBP}}$ 时，Hessian谱中才会出现与信号相关的离群特征值。

**核心瓶颈**在于：低信噪比下，Hessian的连续谱（bulk spectrum）会掩盖信号信息。离群特征值能否脱离连续谱，取决于过参数化程度（学生宽度 $p$）和损失归一化参数 $a$ 的联合作用。这两个参数不仅决定 $\alpha_{\mathrm{BBP}}$ 的数值，还决定BBP相变的定性类型——连续或不连续。不连续相变伴随显著的有限尺寸效应，使得实际可恢复信息的信噪比远低于理论预测的 $\alpha_{\mathrm{BBP}}$。

**方法定位**：本文采用场论方法分析初始化Hessian的谱分布，通过Stieltjes变换和自能图展开获得连续谱密度，进而建立离群特征值的自洽方程，最终由离群特征值与谱左边缘的交点确定BBP相变条件（Eq (15)）。与传统的谱方法（如Mondelli & Montanari, 2018的D矩阵方法）不同，本文直接分析Hessian而非构造加权协方差矩阵；与Bonnaire et al. (2025)对平均化Hessian的BBP研究相比，本文聚焦于过参数化对相变类型和有限尺寸效应的系统性影响。

**主要结果**：
- 增大 $p$ 总体上降低 $\alpha_{\mathrm{BBP}}$，但相变类型可能从连续转为不连续，此时 $\alpha_{\mathrm{BBP}}$ 出现非单调行为（Figure 2）。
- 无限过参数化极限（$p \to \infty$）下，$\alpha_{\mathrm{BBP}}^{p=\infty} = p^*(a+1)/2$，在 $a=0$ 时达到最小值 $p^*/2$，恰好匹配信息论弱恢复阈值（Eq (18)）。
- 不连续BBP相变中，有限样本下的数值相变点显著低于理论 $\alpha_{\mathrm{BBP}}$；外推量 $\alpha_0$ 刻画了这一有限尺寸效应，且 $\alpha_0$ 随 $p$ 单调递减，确认了过参数化在有限维场景中的优势（Figure 3, Figure 4）。
- 初步实验表明，该现象可扩展到sigmoid和tanh等非线性激活函数（Figure 8），且BBP相变与梯度下降的弱恢复起始点相关（Figure 9, Figure 10）。



### 问题背景：高维非凸优化中的初始化困境

在高维非凸优化问题中，损失景观的结构直接决定了梯度基算法的可行性与效率。一个核心问题是：**在随机初始化点附近，损失函数的局部曲率是否携带关于真实信号的可用信息？** 这一问题在两层神经网络中尤为突出，因为损失景观通常包含大量鞍点和局部极小值，初始化点的信息含量可能直接影响算法能否逃离无信息区域。

本文研究一个扩展的经典相位恢复问题：教师-学生设定下的两层软委员会机，教师网络和学生网络均采用二次激活函数。教师网络输出为

$$y ( \mathbf { x } ^ { \mu } ) = \frac { 1 } { p ^ { * } } \sum _ { l = 1 } ^ { p ^ { * } } \left( \mathbf { w } _ { l } ^ { * } \cdot \mathbf { x } ^ { \mu } \right) ^ { 2 }$$

学生网络输出为

$$\hat { y } \big ( \mathbf { x } ^ { \mu } \big ) = \frac { 1 } { p } \sum _ { k = 1 } ^ { p } \big ( \mathbf { w } _ { k } \cdot \mathbf { x } ^ { \mu } \big ) ^ { 2 }$$

其中 $p^*$ 和 $p$ 分别表示教师和学生的隐藏层宽度。损失函数采用带归一化参数 $a$ 的二次损失：

$$\mathcal { L } _ { \mathbf { w } } = \sum _ { \mu = 1 } ^ { M = \alpha N } \frac { 1 } { 2 } \frac { \left[ y ( \mathbf { x } ^ { \mu } ) - \hat { y } ( \mathbf { x } ^ { \mu } ) \right] ^ { 2 } } { a + y ( \mathbf { x } ^ { \mu } ) }$$

在高维数据极限下，输入维度 $N$ 和样本量 $M$ 同时趋于无穷，而信噪比 $\alpha = M/N$ 保持 $\mathcal{O}(1)$ 量级。这一设定使得谱分析工具能够精确刻画损失景观的统计性质。

### 现有方法缺口：谱方法与Hessian信息的局限

现有的谱方法（如基于 $\mathcal{D}$ 矩阵的方法，Mondelli & Montanari, 2018）通过构造形如

$$\pmb { \mathcal { D } } = \sum _ { i = 1 } ^ { \alpha N } T \bigl ( y ( \mathbf { x } ^ { \mu } ) \bigr ) \mathbf { x } ^ { \mu } ( \mathbf { x } ^ { \mu } ) ^ { T }$$

的矩阵，以其主导特征向量作为信号估计。这类方法的成功依赖于 Baik–Ben Arous–Peché (BBP) 相变：仅当信噪比超过临界阈值 $\alpha_{BBP}$ 时，与信号相关的离群特征值才会从连续谱中脱离，使特征向量携带可用信息。

然而，现有研究存在两个关键缺口：

1. **过参数化的影响未知**：此前对Hessian谱的BBP相变研究（如 Bonnaire et al., 2025 的平均化Hessian分析）主要集中在 $p = p^*$ 的匹配参数化情形，过参数化（$p > p^*$）如何改变损失景观结构缺乏理论刻画。

2. **相变类型的忽视**：标准BBP相变分析假设连续过渡，但Hessian谱的左边缘性质（尖锐 vs. 平滑）可能导致定性不同的相变行为——不连续BBP相变，其有限尺寸效应使得实际可恢复信息的信噪比显著偏离理论预测。

### 核心瓶颈：连续谱掩盖信号特征值

本文的核心洞察在于：**在低信噪比下，高维非凸损失景观中初始化Hessian的连续谱掩盖了与教师信号相关的离群特征值**。具体而言，Hessian矩阵的谱包含两个部分：描述随机波动的连续谱（bulk），以及由教师信号产生的离群特征值。BBP相变定义了离群特征值脱离连续谱的临界信噪比 $\alpha_{BBP}$，其条件为

$$\lambda _ { * } ( \alpha _ { B B P } ) = \lambda _ { - } ( \alpha _ { B B P } )$$

即离群特征值恰好等于谱左边缘。在 $\alpha < \alpha_{BBP}$ 时，离群特征值淹没在连续谱中，Hessian的最小特征向量不包含教师信号信息；仅当 $\alpha > \alpha_{BBP}$ 时，离群特征值从连续谱中分离，其对应特征向量才与教师信号对齐。

过参数化和损失归一化参数 $a$ 共同决定了这一临界点的位置及相变类型。连续BBP相变中，谱密度在左边缘呈现平方根奇异性：

$$\rho ( \lambda ) \underset { \lambda \lambda _ { - } ^ { s h } } { \propto } ( \lambda - \lambda _ { - } ^ { s h } ) ^ { 1 / 2 }$$

而不连续BBP相变中，谱密度在左边缘呈指数衰减：

$$\rho ( \lambda ) \underset { \lambda \lambda _ { - } ^ { s m } } { \propto } \exp [ - \frac { A } { ( \lambda - \lambda _ { - } ^ { s m } ) } ]$$

不连续相变伴随的强有限尺寸效应使得有限样本下的实际过渡信噪比远低于理论预测的 $\alpha_{BBP}$，这一效应可由外推的 $\alpha_0$ 刻画，且 $\alpha_0$ 随学生宽度 $p$ 单调递减。

### 本文动机：过参数化如何弯曲损失景观

基于上述缺口，本文聚焦于一个核心问题：**过参数化如何定量和定性地改变初始化Hessian谱中的BBP相变？** 具体而言，本文探索学生网络宽度 $p$（过参数化程度）和损失归一化参数 $a$ 作为两个主要因果旋钮，如何共同调控：

- $\alpha_{BBP}$ 的数值（能否降低恢复教师信号所需的最小信噪比）
- BBP相变的定性类型（连续或不连续）
- 有限尺寸效应在两种相变类型下的表现差异

初步理论分析表明，过参数化不仅能降低BBP相变所需的信噪比，甚至在大过参数化极限下可达到信息论弱恢复阈值 $p^*/2$，同时可能改变相变的定性性质。这一发现暗示：Hessian在初始化点携带的信息可能远超预期，或可用于设计广义谱方法以降低梯度基算法的信噪比需求。



## 核心方法与创新机理

本工作的核心创新在于将**过度参数化**引入损失景观的初始化Hessian谱分析，揭示了过参数化与学生网络宽度$p$、损失归一化参数$a$如何协同决定BBP相变的阈值与定性类型。与先前工作相比，关键变化体现在以下三个维度。

### 从匹配参数化到过度参数化的推广

先前的谱方法（如Mondelli & Montanari, 2018）通常考虑学生网络宽度等于教师宽度（$p = p^*$）的匹配参数化情形，而Bonnaire et al. (2025)对平均化Hessian的BBP研究也主要局限于该设定。本工作明确将分析拓展至$p > p^*$的过度参数化区域，发现**过参数化是调节BBP相变阈值$\alpha_{\text{BBP}}$的核心因果旋钮**：增加$p$可系统性降低从Hessian谱中提取教师信号所需的最小信噪比（见Figure 2）。这一降低并非无代价——当$p$超过某一临界值$p_c(a)$时，BBP相变从连续转变为不连续，并伴随强有限尺寸效应。

### 损失归一化参数$a$作为相变类型控制器

损失函数中引入的归一化参数$a$（见Eq (3)）在先前工作中仅作为避免Hessian谱左边缘发散的数学工具。本工作将其提升为**控制BBP相变连续性与阈值非单调性的独立因果旋钮**。具体而言：

- $a$通过影响Hessian的条件数及谱左边缘的衰减类型，直接决定BBP相变是**连续**（左边缘呈平方根奇异性，Eq (16)）还是**不连续**（左边缘呈指数衰减，Eq (17)）。
- 在固定$p$下，$\alpha_{\text{BBP}}(a)$呈现非单调行为，其最小值恰好位于相变由连续转为不连续的临界点$a_c(p)$处（Figure 2）。
- 这一机制揭示了损失景观的局部曲率结构可通过调整损失函数的归一化方式被定性重塑，而无需改变网络架构。

### 不连续BBP相变与有限尺寸效应的刻画

标准的BBP理论通常假设连续相变，即离群特征值平滑地从连续谱中脱离。本工作识别出在过度参数化下可能出现**不连续BBP相变**，并系统刻画了其独特的有限尺寸效应：

- 在不连续情形下，有限$N$数值模拟中实际观察到的相变阈值**远低于**理论预测的大$N$极限$\alpha_{\text{BBP}}$（Figure 3右），这一偏差源于不连续相变固有的强有限尺寸效应。
- 为量化这一效应，工作引入外推阈值$\alpha_0$，定义为主成分与信号的重叠度开始显著偏离随机水平的最小$\alpha$。实验表明，$\alpha_0$随$p$**单调递减**（Figure 2内插图及Figure 4），确保了过参数化在有限维实际场景中的增益是稳健的。
- 在无限过参数化极限（$p \to \infty$）下，BBP相变总是不连续的，且$\alpha_{\text{BBP}}^{p=\infty} = p^*(a+1)/2$，在$a=0$时达到最小值$p^*/2$（Eq (18)），恰好匹配信息论弱恢复阈值（Maillard et al., 2024），表明过参数化可将初始化Hessian的信息提取能力推向信息论极限。

### 方法学贡献：场论框架下的Hessian谱分析

为实现上述分析，工作建立了基于**场论与费曼图**的Hessian谱分析方法（Section 3），通过计算Stieltjes变换的自能$\Sigma(z)$（Eq (14)）获得连续谱密度，再通过自洽方程求解离群特征值$\lambda_*$，最终由$\lambda_*(\alpha_{\text{BBP}}) = \lambda_-(\alpha_{\text{BBP}})$（Eq (15)）确定BBP阈值。这一框架不仅适用于当前的二次激活两层网络，还为推广到更一般的架构提供了可复用的理论工具。

**证据强度说明**：上述核心创新均有理论推导与数值模拟的双重支撑。BBP相变条件（Eq (15)）与无限过参数化极限（Eq (18)）为解析结果，置信度高；连续/不连续相变的区分及有限尺寸效应的刻画主要依赖数值实验（Figure 2-4），置信度良好。$\alpha_0$与梯度流算法实际阈值之间的精确定量关系仍为开放问题，需进一步研究确认。



本工作围绕一个核心问题展开：在两层软委员会机（soft-committee machine）的师生框架下，初始化时损失景观的 Hessian 谱何时、以及如何携带关于教师网络的可提取信息。整个分析 pipeline 由四个关键模块串联而成，形成从模型设定到相变预测再到有限尺寸验证的完整链条。

**输入与设定**：系统接受高维高斯输入 $\mathbf{x}^\mu \sim \mathcal{N}(0, I_N)$，教师网络宽度为 $p^*$，学生网络宽度为 $p$（允许 $p > p^*$ 的过参数化情形）。损失函数采用带归一化参数 $a$ 的二次损失：

$$\mathcal{L}_{\mathbf{w}} = \sum_{\mu=1}^{M=\alpha N} \frac{1}{2} \frac{[y(\mathbf{x}^\mu) - \hat{y}(\mathbf{x}^\mu)]^2}{a + y(\mathbf{x}^\mu)}$$

其中信噪比 $\alpha = M/N$ 是核心控制变量，$a > 0$ 控制 Hessian 的条件数及谱左边缘的类型。

**模块一：Hessian 块计算**。在随机初始化点计算损失函数关于学生权重的 Hessian 矩阵。由于旋转对称性，Hessian 可分解为 $p \times p$ 个 $N \times N$ 的块，每个块的元素为：

$$(\mathcal{H}_{qq'})_{ij} = \sum_{\mu=1}^{\alpha N} F_{qq'}^\mu x_i^\mu x_j^\mu$$

其中因子 $F_{qq'}^\mu$ 依赖于预激活和归一化参数 $a$（Eq 5）。这一结构将 Hessian 表达为数据协方差结构的加权和，为后续谱分析奠定基础。

**模块二：Stieltjes 变换与连续谱求解**。通过场论方法将 Stieltjes 变换 $g(z)$ 表达为高斯积分，利用 Wick 定理和 Feynman 图展开求平均，最终得到 1PI 自能 $\Sigma(z)$ 满足的自洽方程：

$$g(z) = \frac{1}{z - \Sigma(z)}$$

由此解得 Hessian 的连续谱密度 $\rho(\lambda)$ 及其左边缘 $\lambda_-(\alpha)$。这是判断离群特征值是否脱离连续谱的基准。

**模块三：离群特征值与 BBP 相变条件**。通过求解离群特征值 $\lambda_*$ 的自洽方程（附录 B Eq 40），建立 BBP 相变的临界条件：

$$\lambda_*(\alpha_{\text{BBP}}) = \lambda_-(\alpha_{\text{BBP}})$$

即离群特征值恰好触及连续谱左边缘时对应的信噪比 $\alpha_{\text{BBP}}$。根据谱密度在左边缘的衰减方式，相变分为两类：平方根奇异性对应**连续 BBP**，指数衰减对应**不连续 BBP**。这一分类直接影响有限 $N$ 下的实际可恢复性。

**模块四：有限尺寸数值验证与外推**。通过有限 $N$ 的数值模拟，计算最小特征向量与教师信号的对齐分数 $\phi$ 随 $\alpha$ 的变化。对于连续 BBP，不同 $N$ 的 $\phi$ 曲线交点与理论 $\alpha_{\text{BBP}}$ 一致；对于不连续 BBP，有限尺寸效应导致实际过渡点远低于理论预测，需通过外推得到有效阈值 $\alpha_0$，后者随 $p$ 单调递减，确保过参数化在有限维场景中的优势。

**输出与因果链路**：整个框架以 $p$ 和 $a$ 为可控旋钮，输出 $\alpha_{\text{BBP}}$ 及相变类型。过参数化通过平滑损失景观降低 $\alpha_{\text{BBP}}$，但超过临界宽度 $p_c(a)$ 后相变变为不连续，此时 $\alpha_{\text{BBP}}$ 可能出现非单调行为，而 $\alpha_0$ 仍保持单调递减。在无限过参数化极限 $p \to \infty$ 下，$\alpha_{\text{BBP}}^{p=\infty} = p^*(a+1)/2$，最小值 $p^*/2$ 恰好匹配信息论弱恢复阈值，揭示过参数化可将谱方法的信息提取能力推至理论极限。



### 问题设定与损失景观

论文考虑一个教师-学生框架，其中教师网络和学生网络均为两层软委员会机（soft-committee machine），激活函数为二次函数。教师网络输出为：

$$y ( \mathbf { x } ^ { \mu } ) = \frac { 1 } { p ^ { * } } \sum _ { l = 1 } ^ { p ^ { * } } \left( \mathbf { w } _ { l } ^ { * } \cdot \mathbf { x } ^ { \mu } \right) ^ { 2 }$$

其中 $p^{*}$ 为教师网络宽度，$\mathbf{w}_l^{*} \in \mathbb{R}^N$ 为教师权重。学生网络输出为：

$$\hat { y } \big ( \mathbf { x } ^ { \mu } \big ) = \frac { 1 } { p } \sum _ { k = 1 } ^ { p } \big ( \mathbf { w } _ { k } \cdot \mathbf { x } ^ { \mu } \big ) ^ { 2 }$$

其中 $p$ 为学生网络宽度。过参数化情形对应 $p > p^{*}$。

损失函数采用带归一化的二次损失：

$$\mathcal { L } _ { \mathbf { w } } = \sum _ { \mu = 1 } ^ { M = \alpha N } \frac { 1 } { 2 } \frac { \left[ y ( \mathbf { x } ^ { \mu } ) - \hat { y } ( \mathbf { x } ^ { \mu } ) \right] ^ { 2 } } { a + y ( \mathbf { x } ^ { \mu } ) }$$

其中 $\alpha = M/N$ 为信噪比，参数 $a > 0$ 控制归一化强度，用于防止分母为零并调节Hessian矩阵的条件数。

### Hessian矩阵结构

论文的核心分析对象是随机初始化处损失函数的Hessian矩阵。Hessian的第 $(q, q')$ 块（对应学生网络第 $q$ 和第 $q'$ 个神经元的权重）的第 $(i, j)$ 个元素为：

$$( \mathcal { H } _ { q q ^ { \prime } } ) _ { i j } = \sum _ { \mu = 1 } ^ { \alpha N } F _ { q q ^ { \prime } } ^ { \mu } x _ { i } ^ { \mu } x _ { j } ^ { \mu }$$

其中因子 $F_{qq'}^{\mu}$ 依赖于学生预激活 $\lambda_k^{\mu} = \mathbf{w}_k \cdot \mathbf{x}^{\mu}$ 和教师预激活 $u_l^{\mu} = \mathbf{w}_l^{*} \cdot \mathbf{x}^{\mu}$：

$$F _ { q q ^ { \prime } } ^ { \mu } = \frac { 2 } { p } \cdot \frac { \frac { 2 } { p } \lambda _ { q } ^ { \mu } \lambda _ { q ^ { \prime } } ^ { \mu } + \delta _ { q q ^ { \prime } } \left[ \frac { 1 } { p } \sum _ { k = 1 } ^ { p } \left( \lambda _ { k } ^ { \mu } \right) ^ { 2 } - \frac { 1 } { p ^ { * } } \sum _ { l = 1 } ^ { p ^ { * } } \left( u _ { l } ^ { \mu } \right) ^ { 2 } \right] } { a + \frac { 1 } { p ^ { * } } \sum _ { l = 1 } ^ { p ^ { * } } \left( u _ { l } ^ { \mu } \right) ^ { 2 } }$$

该因子编码了损失景观的局部曲率如何受到学生-教师预激活差异和归一化参数 $a$ 的联合影响。

### 场论方法与谱分析流程

为获得Hessian的谱分布，论文采用场论方法计算Stieltjes变换。整个分析流程包含以下关键模块：

1. **Stieltjes变换的场论表示**：将Stieltjes变换表达为高斯积分形式，利用Wick定理将随机平均转化为Feynman图展开。

2. **自能方程**：通过求和所有1PI（单粒子不可约）图，得到Stieltjes变换的简洁形式：

   $$g ( z ) = \frac { 1 } { z - \Sigma ( z ) }$$

   其中 $\Sigma(z)$ 为自能，其具体形式由 $p$、$p^{*}$ 和 $a$ 决定。

3. **离群特征值方程**：在连续谱之外，离群特征值 $\lambda_{*}$ 满足自洽方程（见附录B Eq (40)），其解的存在性取决于信噪比 $\alpha$。

### BBP相变条件

Hessian谱中与教师信号相关的信息由离群特征值携带。BBP相变的临界条件为离群特征值恰好等于连续谱的左边缘：

$$\lambda _ { * } ( \alpha _ { B B P } ) = \lambda _ { - } ( \alpha _ { B B P } )$$

当 $\alpha < \alpha_{BBP}$ 时，离群特征值被连续谱淹没，无法从中提取教师信息；当 $\alpha > \alpha_{BBP}$ 时，离群特征值脱离连续谱，其对应的特征向量与教师信号具有非零重叠。

### 相变类型与谱边缘行为

BBP相变的定性性质取决于连续谱密度 $\rho(\lambda)$ 在左边缘处的衰减行为：

- **连续BBP相变**：谱密度在尖锐左边缘 $\lambda_{-}^{sh}$ 处呈现平方根奇异性：

  $$\rho ( \lambda ) \underset { \lambda \to \lambda _ { - } ^ { s h } } { \propto } ( \lambda - \lambda _ { - } ^ { s h } ) ^ { 1 / 2 }$$

- **不连续BBP相变**：谱密度在平滑左边缘 $\lambda_{-}^{sm}$ 处呈指数衰减：

  $$\rho ( \lambda ) \underset { \lambda \to \lambda _ { - } ^ { s m } } { \propto } \exp \left[ - \frac { A } { ( \lambda - \lambda _ { - } ^ { s m } ) } \right]$$

归一化参数 $a$ 是决定边缘类型的关键旋钮，从而控制相变是连续还是不连续。

### 无限过参数化极限

在 $p \to \infty$ 的极限下，BBP阈值具有简洁的解析形式：

$$\alpha _ { \mathrm { B B P } } ^ { p = \infty } = \frac { p ^ { * } ( a + 1 ) } { 2 }$$

该阈值在 $a = 0$ 时达到最小值 $p^{*}/2$，恰好匹配信息论弱恢复阈值（Maillard et al., 2024）。在此极限下，BBP相变总是不连续的。

### 有限尺寸效应与外推阈值

不连续BBP相变伴随强有限尺寸效应：有限 $N$ 下的数值模拟显示，实际观察到的相变点远低于理论预测的 $\alpha_{BBP}$。为刻画这一效应，论文引入外推阈值 $\alpha_0$，其定义为有限 $N$ 下离群特征值中信息实际消失的信噪比下界。$\alpha_0$ 随 $p$ 单调递减，确保了过参数化即使在有限维场景中仍具有优势。



## 实验与关键发现

### 核心发现：BBP相变的连续与不连续两种类型

该工作通过分析初始化Hessian谱中离群特征值的行为，揭示了BBP相变存在两种定性不同的类型——连续相变和不连续相变，其判别标准取决于谱密度$\rho(\lambda)$在左边缘$\lambda_-$附近的衰减方式。

- **连续BBP相变**：当谱左边缘是“尖锐”的（sharp edge），即$\rho(\lambda) \propto (\lambda - \lambda_-^{sh})^{1/2}$时，离群特征值$\lambda_*$随信噪比$\alpha$连续地从谱边缘脱离。此时，离群特征向量与教师信号的重叠在$\alpha_{BBP}$附近从零连续增长（Figure 1左），有限$N$数值模拟中不同$N$的$\varphi$曲线在理论预测的$\alpha_{BBP}$处相交（Figure 3左），验证了理论的准确性。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_xDLE5n3x9Y/figures/005_Figure_3.jpg]]
*Figure 3: Comparison of BBP transitions for p = $p ^ { * }$ = 1 . On the y axis we plot $\phi$ , defined as the fraction of times the eigenvector with the maximum overlap with the signal corresponds to the smallest eigenvalue. On the left a value of a for which the transition is continuous, on the right a value for which it is discontinuous. The vertical blue lines show our prediction for the BBP threshold, while for the discontinuous case the red line shows our estimate of $\alpha _ { 0 }$

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_xDLE5n3x9Y/figures/003_Figure_1.jpg]]
*Figure 1: Overlap between the signal estimate and the true signal as a function of α for continuous BBP ( L e f t ) and discontinuous BBP ( R i g h t ) , with p = 2 and p ^ { * } = 1*

- **不连续BBP相变**：当谱左边缘是“平滑”的（smooth edge），即$\rho(\lambda) \propto \exp[-A/(\lambda - \lambda_-^{sm})]$时，离群特征值在$\alpha_{BBP}$处突然从谱内部跳出，其与信号的重叠在相变点发生跳变（Figure 1右）。然而，**不连续相变伴随强烈的有限尺寸效应**：有限$N$的数值模拟显示，实际的相变点远低于理论预测的$\alpha_{BBP}$（Figure 3右），且不同$N$的曲线并不在$\alpha_{BBP}$处相交。

这一有限尺寸效应是该工作的关键发现之一。为量化实际可用的信噪比下界，作者引入外推量$\alpha_0$，定义为有限$N$下离群特征向量开始携带信号信息的最小$\alpha$。Figure 4显示，$\alpha_0$始终低于$\alpha_{BBP}$，且**$\alpha_0$随$p$单调递减**，这确保了即使在有限维场景中，过参数化仍然带来优势。

### 过参数化对$\alpha_{BBP}$的影响

Figure 2展示了固定教师宽度$p^*=1$时，BBP阈值$\alpha_{BBP}$随损失归一化参数$a$和学生宽度$p$的变化：

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_xDLE5n3x9Y/figures/004_Figure_2.jpg]]
*Figure 2: αBBP as a function of a for $p ^ { * }$ = 1 and several values of $\cdot$ \ : $\boldsymbol { p }$ . The point at which the curves start increasing almost linearly is the point in which the transition becomes discontinuous. The dashed line shows $\alpha _ { B B P }$ ( a ) in the large overparametrization limit where the transition is always discontinuous. The insets show $\alpha _ { B B P }$ as a function of p for three fixed values of a. Here, red points indicate the transition is continuous, while blue points that it is discontinuous. The red crosses are estimates of $\alpha _ { 0 }$ , a ”finite- . $N ^ { \mathbf { \ell } , \mathbf { \ell } }$ estimate of the transition described in section 4.2

- **$a$的调控作用**：$\alpha_{BBP}(a)$呈现非单调行为。在连续相变区域，$\alpha_{BBP}$随$a$减小而降低；但当$a$降至某个临界值$a_c(p)$时，相变类型由连续转为不连续，此后$\alpha_{BBP}$几乎线性上升。**$\alpha_{BBP}$的最小值恰好出现在$a_c(p)$处**，即相变类型切换的临界点。

- **$p$的总体效应**：增加$p$（过参数化）通常降低$\alpha_{BBP}$，使信号信息在更低的信噪比下即可被Hessian谱捕获。但Figure 2的内插图揭示了重要细节：当$p$超过临界值$p_c(a)$后，相变变为不连续，此时$\alpha_{BBP}$可能出现微小的非单调上升。然而，外推的$\alpha_0$始终随$p$单调递减，说明**过参数化在有限维场景中的实际收益是稳健的**。

### 无限过参数化极限

在$p \to \infty$的极限下，BBP相变总是不连续的，且阈值有简洁的解析表达式：

$$\alpha_{\mathrm{BBP}}^{p=\infty} = \frac{p^*(a+1)}{2}$$

该公式揭示了一个深刻结论：当$a=0$时，$\alpha_{BBP}^{p=\infty} = p^*/2$，**恰好匹配Maillard et al. (2024)给出的信息论弱恢复阈值**。这意味着在无限过参数化极限下，初始化Hessian谱所包含的教师信号信息可以达到信息论允许的最优水平。

### 对教师宽度的鲁棒性

Figure 6将分析扩展到$p^*=2$的情形，验证了上述结论对教师宽度的鲁棒性：$\alpha_{BBP}$随$a$和$p$的定性行为与$p^*=1$一致，过参数化同样降低BBP阈值，且连续/不连续相变的切换机制保持不变。Figure 7进一步展示了欠参数化（$p=1$，$p^*$增大）的效果：$\alpha_{BBP}$随$p^*$增大而上升，说明教师宽度增加使问题难度增大。

### 与梯度下降动态的关联

Figure 9和Figure 10分别展示了连续和不连续BBP情形下，梯度下降动态中最大平方磁化强度$m^2$随$\alpha$的变化。结果表明，**BBP相变的发生与弱恢复的起始高度一致**——当$\alpha$超过BBP阈值时，梯度流开始能够从初始化点恢复出教师信号的部分信息。这一关联在两种相变类型中均成立，但需注意不连续情形下有限尺寸效应导致的阈值偏移同样会影响算法行为。

### 激活函数扩展实验

Figure 8展示了将分析框架扩展到其他非线性激活函数的初步结果。在sigmoid激活（$a=1$）和tanh激活（$a=50$，为避免分母发散而取大值）下，Hessian最小特征向量与教师信号的重叠仍随$\alpha$呈现类似BBP相变的行为。这表明**所发现的BBP相变现象不限于二次激活**，但完整的理论推广尚未完成。

### 方法局限与待验证问题

1. **平均化Hessian的局限**：Bonnaire et al. (2025)提出的平均化Hessian方法在大$p$极限下不能定量匹配BBP相变，信号恢复性能可能不完全遵循预测的$\alpha_{BBP}$。

2. **有限尺寸效应的精确刻画**：外推量$\alpha_0$与有限$N$下实际算法阈值之间的精确关系尚未建立；在不连续BBP情形下，经验相变点如何随$N$增大而移动仍是开放问题。

3. **阈值状态的BBP相变**：对梯度动力学最终停滞配置的BBP相变进行完整刻画，对于确认当前理论图景是必要的，目前仅有初步模拟显示关联。

4. **损失函数形式的限制**：归一化分母$(a+y)$的形式对于非正激活（如tanh）需要调整，实验中使用了很大的$a$来近似MSE损失，更一般的损失函数形式有待探索。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_xDLE5n3x9Y/figures/009_Figure.jpg]]

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_xDLE5n3x9Y/figures/014_Figure.jpg]]



## 定位与知识库关联

### 方法定位与基线关系

本工作属于高维统计物理与随机矩阵理论交叉领域，核心方法是通过场论与费曼图技术分析初始化时Hessian矩阵的谱分布及其BBP相变。该方法在谱系上可追溯到两个主要分支：

**谱方法传统**：在相位恢复问题中，经典的谱方法通过构造形如 $\pmb{\mathcal{D}} = \sum_{i=1}^{\alpha N} T(y(\mathbf{x}^\mu)) \mathbf{x}^\mu (\mathbf{x}^\mu)^T$ 的矩阵，取其主特征向量作为信号估计（Mondelli & Montanari, 2018）。本工作将这一思路推广到Hessian矩阵——损失景观的局部曲率算子，其最小特征值对应的特征向量在BBP相变点以上携带教师信号信息。相比传统谱方法直接利用标签构造矩阵，Hessian方法无需选择预处理函数 $T(\cdot)$，且能自然地纳入过参数化效应。

**平均化Hessian研究**：Bonnaire et al. (2025) 曾研究过平均化Hessian的BBP相变，但该方法在大过参数化极限下无法定量匹配实际BBP阈值，且无法刻画相变类型（连续/不连续）的转变。本工作通过完整的场论推导，直接处理非平均化的Hessian矩阵，揭示了损失归一化参数 $a$ 和过参数化程度 $p$ 如何共同决定相变的定性性质。

### 因果旋钮与关键机制

本工作识别的核心因果旋钮有两个：

1. **学生网络宽度 $p$（过参数化程度）**：当 $p > p^*$ 时，过参数化通过平滑损失景观降低BBP相变所需的信噪比 $\alpha_{\text{BBP}}$。其作用机制是：增加 $p$ 改变了Hessian矩阵的块结构，使与信号相关的离群特征值更容易从连续谱中脱离。在无限过参数化极限下，$\alpha_{\text{BBP}}^{p=\infty} = p^*(a+1)/2$，最小值 $p^*/2$ 恰好匹配信息论弱恢复阈值（Maillard et al., 2024），表明过参数化可将谱方法的信息提取能力推向理论极限。

2. **损失归一化参数 $a$**：$a$ 控制Hessian矩阵的条件数及谱左边缘的奇异性类型。当 $a$ 较小时，谱左边缘呈尖锐的平方根奇异性 $\rho(\lambda) \propto (\lambda - \lambda_-^{sh})^{1/2}$（Eq 16），对应连续BBP相变；当 $a$ 超过临界值 $a_c(p)$ 时，左边缘变为平滑的指数衰减 $\rho(\lambda) \propto \exp[-A/(\lambda - \lambda_-^{sm})]$（Eq 17），对应不连续BBP相变。

两者的交互决定了相变类型：固定 $a$ 增加 $p$ 会降低 $\alpha_{\text{BBP}}$，但当 $p$ 超过临界值 $p_c(a)$ 后，相变从连续转为不连续。在不连续区域，$\alpha_{\text{BBP}}$ 可能出现微弱的非单调上升（Figure 2 内插图），但外推的有限尺寸阈值 $\alpha_0$ 始终随 $p$ 单调递减，确保了过参数化在实际有限维场景中的优势。

### 适用边界与局限

本工作的理论分析建立在以下严格假设之上，超出这些边界时结论需要谨慎推广：

1. **架构限制**：分析局限于两层软委员会机（soft-committee machine）且激活函数为二次函数。虽然初步实验表明BBP相变现象可扩展到sigmoid和tanh激活（Figure 8），但完整的场论推导尚未完成。对于更深的网络或更复杂的架构，Hessian的块结构和谱性质可能发生本质变化。

2. **高维极限假设**：所有理论结果在 $N \to \infty$、$M/N = \alpha = O(1)$ 的热力学极限下严格成立。在有限维场景中，尤其是不连续BBP相变情况下，有限尺寸效应显著——实际观察到的相变阈值远低于理论预测的 $\alpha_{\text{BBP}}$。虽然可通过外推的 $\alpha_0$ 进行估计，但 $\alpha_0$ 与有限 $N$ 下实际算法阈值之间的精确关系仍是开放问题。

3. **损失函数形式**：归一化分母采用 $a + y(\mathbf{x}^\mu)$ 的形式，对于输出可能为负的激活函数（如tanh），需要设置很大的 $a$ 以避免分母为零，此时损失函数近似退化为标准MSE。这种参数选择虽然可行，但偏离了理论分析的核心区域。

4. **初始化信息与算法动态的鸿沟**：本工作仅分析了初始化时Hessian的谱信息，虽然初步模拟表明BBP相变与梯度下降的弱恢复开始存在相关性（Figure 9, 10），但初始化时的谱信息如何定量转化为梯度流算法的实际过渡阈值，仍是一个重要的开放问题。特别地，在不连续BBP区域，有限尺寸效应导致的信息损失如何影响实际优化动态，尚未被完整刻画。

### 开放问题

1. **过参数化对梯度流算法过渡的定量影响**：当前工作仅建立了初始化Hessian谱与算法恢复之间的相关性，但缺乏从BBP相变到梯度动力学过渡的因果桥梁。这是连接谱分析与实际优化的关键缺失环节。

2. **有限尺寸效应的精确刻画**：在不连续BBP情况下，经验过渡点如何随 $N$ 增大而移动？$\alpha_0$ 的精确理论表达式是什么？这些问题对于理解实际规模网络的行为至关重要。

3. **阈值状态的BBP相变**：梯度动力学最终停滞的配置（阈值状态）处的Hessian谱性质尚未被分析。对该状态进行完整刻画，对于确认初始化BBP相变与最终恢复性能之间的关联是必要的。

4. **方法推广**：将场论分析方法推广到更一般的网络架构（深度网络、卷积结构）和非线性激活函数（ReLU、GeLU等），是验证该方法普适性的重要方向。当前对sigmoid和tanh的初步实验仅提供了现象层面的支持。



## 原文 PDF

![[paperPDFs/ICLR_2026/Overparametrization_bends_the_landscape_BBP_transitions_at_initialization_in_simple_Neural_Networks.pdf]]
