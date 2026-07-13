---
title: "A Biologically Plausible Dense Associative Memory with Exponential Capacity"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Biologically_Plausible_Dense_Associative_Memory_with_Exponential_Capacity.pdf
project_link: null
code_link: null
aliases:
- TBDAMT
- BPDAMEC
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/neuroscience_cognitive_science
core_operator: "将隐藏神经元的激活函数从幂律、softmax 或球面归一化等非线性函数替换为简单的阈值函数（Heaviside step function），从而允许分布式表示。"
primary_logic: "通过使用阈值激活函数，隐藏神经元可以编码多个记忆共享的基本组件，使得所有 $2^{N_h}$ 种隐藏层二元状态都成为稳定不动点，从而在 $N_v \\gg N_h$ 条件下实现指数级存储容量。"
claims:
- "当 $N_v \\gg N_h$ 时，有效权重矩阵 $J_{\\mu\\nu}$ 趋近于单位矩阵，从而解耦隐藏神经元，使得所有 $2^{N_h}$ 种二元模式都是稳定不动点。"
- "无比特翻转的概率下界为 $1 - N_h \\sqrt{(N_h+1)/N_v} \\, e^{-N_v/(8(N_h+1))} / \\sqrt{\\pi/2}$，随着 $N_v$ 增加呈指数趋近于1。"
- "在 MNIST 上，仅用 50 个隐藏神经元即可存储 60,000 张图像，召回准确率达 98%，而 Krotov-Hopfield 模型在相同隐藏神经元数量下最多只能存储 50 个记忆。"
- "在 CIFAR-10 上，用 500 个隐藏神经元存储 50,000 张图像，学习到 49,982 个唯一极小值。"
---

# A Biologically Plausible Dense Associative Memory with Exponential Capacity

> [!tip] 核心洞察
> 通过使用阈值激活函数，隐藏神经元可以编码多个记忆共享的基本组件，使得所有 $2^{N_h}$ 种隐藏层二元状态都成为稳定不动点，从而在 $N_v \gg N_h$ 条件下实现指数级存储容量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 具有指数容量的生物学合理稠密联想记忆 |
| 英文题名 | A Biologically Plausible Dense Associative Memory with Exponential Capacity |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=mRZOayQL1i) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/neuroscience_cognitive_science |
| Method | Threshold-based Dense Associative Memory (TDAM) |
| Dataset | MNIST |

> [!tip] 效果简介
> - MNIST 上，存储记忆数 为 60,000，对比 50 (Krotov-Hopfield 模型)，变化 +59,950。
> - MNIST 上，召回准确率（可见层） 为 98%，对比 90% (Model B)，变化 +8%。
> - MNIST 上，分类准确率（可见层） 为 98%，对比 99% (原始图像)，变化 -1%。

## 概要

本文提出了一种基于阈值激活函数的密集联想记忆模型（Threshold-based Dense Associative Memory, TDAM），在保持生物可解释性的同时，实现了与隐藏神经元数量呈指数关系的存储容量。该模型发表于 ICLR 2026，核心创新在于将隐藏神经元的激活函数从幂律函数、softmax 或球面归一化等非线性函数替换为简单的 Heaviside 阶跃函数，从而允许分布式表示。理论分析表明，当可见神经元数量远大于隐藏神经元数量（$N_v \gg N_h$）时，有效权重矩阵 $J_{\mu\nu}$ 趋近于单位矩阵，使得所有 $2^{N_h}$ 种隐藏层二元状态都成为稳定不动点。在 MNIST 数据集上，仅用 50 个隐藏神经元即可存储 60,000 张图像，召回准确率达 98%；在 CIFAR-10 数据集上，用 500 个隐藏神经元存储 50,000 张图像，学习到 49,982 个唯一极小值。

传统联想记忆模型面临容量瓶颈。Krotov and Hopfield (2021) 提出的密集联想记忆模型虽然引入了两层架构，但其存储容量仅与隐藏神经元数量呈线性关系。该模型采用赢者通吃（winner-take-all）的动力学，导致每个隐藏神经元只能编码一个记忆，无法实现分布式表示。具体而言，Krotov-Hopfield 模型使用了三种非线性激活函数：幂律函数（$f(h_\mu)=h_\mu^n$）、softmax 和球面归一化，这些函数要么导致隐藏神经元活动值无界增长（幂律函数），要么依赖非局部操作（softmax 和球面归一化），既限制了容量，也降低了生物可解释性。

Demircigil et al. (2017) 虽然实现了指数容量，但其模型依赖非生物可解释的相互作用。Chandra et al. (2025) 通过使用多个密集联想记忆模块实现了分布式编码和指数容量，但需要多个模块协同工作。本文的核心动机是：能否在单个模块中同时实现指数容量和生物可解释性？

## 核心方法与创新机理

本文的核心创新在于将隐藏神经元的激活函数替换为简单的阈值函数（Heaviside step function），从而允许分布式表示。这一改变带来了三个关键优势：

1. **分布式表示**：通过使用阈值激活函数，隐藏神经元可以编码多个记忆共享的基本组件，使得多个隐藏神经元可同时激活，每个隐藏神经元可参与多个记忆的编码。

2. **指数容量**：所有 $2^{N_h}$ 种隐藏层二元状态都成为稳定不动点，从而在 $N_v \gg N_h$ 条件下实现指数级存储容量。

3. **生物可解释性**：阈值激活函数是局部的，且保持神经元活动在生物可解释的范围内（0 或 1），而 Krotov-Hopfield 模型的幂律激活函数会导致隐藏神经元活动值达到不切实际的高值。

![[assets/figures/papers/iclr26_0002_mRZOayQL1i_A_Biologically_Plausible_Dense_Associative_Memor/figures/001_Figure_1.jpg]]
*Figure 1: a*

模型由两个相互连接的神经元层组成：

- **可见层（Visible Layer）**：接收输入模式，通过动力学方程更新状态，输出重构的记忆。
- **隐藏层（Hidden Layer）**：通过阈值激活函数产生分布式二元表示，作为记忆的隐式编码。
- **突触权重矩阵 $\xi$**：连接可见层与隐藏层，通过学习规则优化，使得目标记忆成为稳定不动点。
- **阈值参数 $\theta$**：控制隐藏神经元激活的阈值，理论最优值为 0.5，确保二元模式的稳定性。

模型的动力学由两个耦合的微分方程定义：

可见神经元动力学（Eq. (1a)）：
$$\tau_v \frac{d v_i}{dt} = -v_i + \frac{1}{\sqrt{N_h}} \sum_{\mu=1}^{N_h} \xi_{i\mu} \Theta(h_\mu - \theta)$$

隐藏神经元动力学（Eq. (1b)）：
$$\tau_h \frac{d h_\mu}{dt} = -h_\mu + \frac{\sqrt{N_h}}{N_v} \sum_{i=1}^{N_v} \xi_{\mu i} v_i$$

其中 $\Theta(z)$ 是 Heaviside 阶跃函数（Eq. (2)）：
$$\Theta(z) = \begin{cases} 0 & \text{if } z \leq 0 \\ 1 & \text{if } z > 0 \end{cases}$$

### 5.1 不动点分析与容量证明

隐藏神经元的二元状态定义为（Eq. (4)）：
$$s_\mu \equiv \Theta(h_\mu - \theta)$$

在不动点处，隐藏状态满足自洽方程（Eq. (5)）：
$$s_\mu = \Theta\left( \sum_{\nu=1}^{N_h} J_{\mu\nu} s_\nu - \theta \right)$$

其中有效权重矩阵 $J_{\mu\nu}$ 定义为（Eq. (6)）：
$$J_{\mu\nu} \equiv \frac{1}{N_v} \sum_{i=1}^{N_v} \xi_{\mu i} \xi_{i\nu}$$

当权重 $\xi$ 为高斯随机矩阵时，根据 Marchenko and Pastur (1967) 的结果，$J_{\mu\nu}$ 可分解为（Eq. (7a)）：
$$J_{\mu\nu} = \delta_{\mu\nu} + \frac{\zeta_{\mu\nu}}{\sqrt{N_v}}$$

其中 $\zeta_{\mu\nu}$ 是均值为 0、方差为 1（$\mu \neq \nu$）或 2（$\mu = \nu$）的随机变量。当 $N_v \gg N_h$ 时，$J_{\mu\nu}$ 趋近于单位矩阵，从而解耦隐藏神经元。

### 5.2 稳定性保证

系统的雅可比矩阵为下三角结构（Appendix A.2）：
$$\mathbf{A} = \begin{bmatrix} -\mathbf{I}_{N_v} & \mathbf{0} \\ \mathbf{A}_{hv} & -\mathbf{I}_{N_h} \end{bmatrix}$$

所有对角元均为 -1，且由于 Heaviside 阶跃函数的导数几乎处处为零，非对角块 $\mathbf{A}_{vh} = 0$，因此所有不动点都是稳定的。

### 5.3 噪声容忍性

噪声项的上界为（Eq. (9)）：
$$|q_\mu| \leq \sqrt{\frac{N_h+1}{N_v}}$$

无比特翻转的概率下界为（Eq. (10)）：
$$P_{\mathrm{no\ bit\ flips}} \geq 1 - N_h \sqrt{\frac{N_h+1}{N_v}} \frac{e^{-\frac{N_v}{8(N_h+1)}}}{\sqrt{\pi/2}}$$

该下界随着 $N_v$ 增加呈指数趋近于 1。可见层噪声方差需满足条件（Eq. (15)）：
$$\sigma_v^2 \ll \frac{N_v}{N_h}$$

### 5.4 学习规则

稳态可见活动可表示为基本记忆向量的线性组合（Eq. (16)）：
$$\mathbf{v} = \frac{1}{\sqrt{N_h}} \sum_{\mu=1}^{N_h} \xi_\mu s_\mu$$

学习目标是最小化重构误差（Eq. (17)）：
$$(\xi, \theta) = \arg\min_{\xi,\theta} \sum_{m=1}^M \left\| \mathbf{v}_m - \frac{1}{\sqrt{N_h}} \sum_{\mu=1}^{N_h} \pmb{\xi}_\mu \Theta\left( \frac{\sqrt{N_h}}{N_v} \pmb{\xi}_\mu^\top \mathbf{v}_m - \theta \right) \right\|^2$$

该学习规则与 Radhakrishnan et al. (2020) 提出的规则相同。

## 实验与关键发现

### 6.1 主要实验结果

**Table 4** 比较了本文模型与 Krotov-Hopfield 模型的召回性能：

![[assets/figures/papers/iclr26_0002_mRZOayQL1i_A_Biologically_Plausible_Dense_Associative_Memor/figures/010_Table_4.jpg]]
*Table 4: And from a biological perspective, the nonlinearity used in Model A is not plausible, because the power-law activation causes hidden neuron activity to reach unrealistically high values during recall. Models B and C also rely on non-local activation functions, which would require additional circuit mechanisms to implement. In contrast, our model maintains bounded activity, and the nonlinearity is fully local. Table 4: Nonlinearities used in the Dense Associative Memory models from Krotov and Hopfield (2021) and in our model, and a comparison of their recall performance. Recall performance is the percentage of recalled digits that are classified correctly.*

| 模型 | 隐藏神经元数量 | 存储记忆数 | 召回性能 |
|------|----------------|------------|----------|
| Krotov-Hopfield Model A(i) | 50 | 50 | 12% |
| Krotov-Hopfield Model A(ii) | 50 | 50 | 84% |
| Krotov-Hopfield Model B | 50 | 50 | 90% |
| Krotov-Hopfield Model C | 50 | 50 | 2% |
| **本文模型** | **50** | **60,000** | **98%** |

**Table 1** 展示了非线性分类器在召回表示和原始图像上的分类准确率：

![[assets/figures/papers/iclr26_0002_mRZOayQL1i_A_Biologically_Plausible_Dense_Associative_Memor/figures/007_Table_1.jpg]]

| 数据集 | 召回可见层 | 召回隐藏层 | 原始图像 |
|--------|------------|------------|----------|
| MNIST | 98% | 95% | 99% |
| CIFAR-10 | 56% | 40% | 88% |

**Figure 2** 展示了在 MNIST 数据集上，50 个隐藏神经元存储 60,000 张图像的召回示例。高度相关的图像（如数字 6）收敛到唯一但重叠的隐藏表示。

**Figure 4** 展示了在 CIFAR-10 数据集上，500 个隐藏神经元存储 50,000 张图像的召回示例，学习到 49,982 个唯一极小值。

**Figure 3** 和 **Figure 5** 分别展示了 MNIST 和 CIFAR-10 上学习到的基本记忆（权重矩阵列）及其相关性矩阵，以及网络的组合泛化能力。

### 6.2 消融实验

1. **隐藏神经元数量不足**（Figure 7 和 Figure 8）：当 $N_h=16$ 时，MNIST 和 CIFAR-10 的重构图像不可识别。

2. **平滑 sigmoid 替代 Heaviside**（Figure 10b）：使用平滑 sigmoid 函数时，召回性能保持不变，容量仍为指数级。

3. **时间常数比**（Figure 11）：可见层与隐藏层时间常数比 $\tau_v/\tau_h$ 仅需达到 4 即可确保完美召回。

4. **非对称权重和异质阈值**（Figure 9）：网络在非对称权重和异质阈值下仍能实现稳定召回。

### 6.3 公平性说明

- 实验仅使用 MNIST 和 CIFAR-10 两个标准图像数据集，未在更多样化的数据集上验证。
- 分类准确率比较中，原始图像的分类器是在完整图像上训练的，而召回表示的分类器是在网络重构后的图像上训练的，两者训练数据分布不同。
- CIFAR-10 上可见层召回准确率（56%）显著低于原始图像（88%），表明模型对复杂彩色图像的表示能力有限。

![[assets/figures/papers/iclr26_0002_mRZOayQL1i_A_Biologically_Plausible_Dense_Associative_Memor/figures/008_Table_2.jpg]]
*Table 2: Architecture and Parameters of the CNN Classifier*

![[assets/figures/papers/iclr26_0002_mRZOayQL1i_A_Biologically_Plausible_Dense_Associative_Memor/figures/009_Table_3.jpg]]
*Table 3: Architecture and Parameters of the MLP Classifier*

![[assets/figures/papers/iclr26_0002_mRZOayQL1i_A_Biologically_Plausible_Dense_Associative_Memor/figures/002_Figure_1.jpg]]
*Figure 1: b Figure 1: Capacity versus the number of hidden units, $N _ { h }$ , with $N _ { v }$ = 1 0 0 $N _ { h }$ and $\tau _ { v }$ = 2 0 $\tau _ { h }$ . (a) Capacity for different thresholds, θ. The highest storage capacity is achieved when the threshold is set to its optimal theoretical value , $\theta$ = 0 . 5 . (b) The effect of noise in the visible layer ( $\epsilon _ { i } ^ { v }$ in Eq. (12a)), shown for different noise variances, demonstrates the large basin of attraction of the fixed points.

## 定位与知识库关联

### 7.1 与现有方法的关系

本文方法在密集联想记忆的谱系中占据独特位置：

- **Krotov and Hopfield (2021)**：提出了两层密集联想记忆架构，但容量线性于隐藏神经元数量，且使用赢者通吃动力学。本文通过替换激活函数，将容量提升至指数级。

- **Demircigil et al. (2017)**：实现了指数容量，但依赖非生物可解释的相互作用。本文在保持生物可解释性的同时实现了指数容量。

- **Chandra et al. (2025)**：通过多个密集联想记忆模块实现分布式编码和指数容量。本文证明单个模块即可实现相同效果。

- **Amit et al. (1985)**：经典 Hopfield 网络容量上限为 $N_v < 0.138 N_h$。本文模型在 $N_v \gg N_h$ 条件下实现 $2^{N_h}$ 个稳定不动点。

### 7.2 局限性与开放问题

**局限性**：
- 理论分析假设权重为高斯随机矩阵，学习到的权重可能偏离此假设，影响理论保证。
- CIFAR-10 上可见层召回准确率（56%）远低于原始图像（88%），表明模型对复杂彩色图像的表示能力有限。
- 模型需要 $N_v \gg N_h$ 的条件才能实现指数容量，限制了隐藏神经元的相对数量。
- 实验仅在 MNIST 和 CIFAR-10 两个标准数据集上进行。
- 学习规则在优化过程中使用平滑 sigmoid 近似 Heaviside 函数，可能导致训练与推理之间的不匹配。
- 模型未考虑生物神经网络的稀疏连接性和 Dale 法则等约束。

**开放问题**：
- 如何将模型扩展到具有稀疏连接或 Dale 法则约束的更真实生物神经网络？
- 模型能否在更大规模、更高分辨率的数据集（如 ImageNet）上保持指数容量和高召回率？
- 如何进一步提高 CIFAR-10 等复杂数据集的召回准确率？
- 模型中的分布式表示是否与生物神经编码（如群体编码）有更深的联系？
- 如何将模型与分层预测编码（如 Li et al. (2025), Salvatori et al. (2021)）结合，实现层次化特征学习？
- 模型能否扩展到序列记忆或时间依赖的记忆任务？

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Biologically_Plausible_Dense_Associative_Memory_with_Exponential_Capacity.pdf

![[paperPDFs/ICLR_2026/A_Biologically_Plausible_Dense_Associative_Memory_with_Exponential_Capacity.pdf]]
