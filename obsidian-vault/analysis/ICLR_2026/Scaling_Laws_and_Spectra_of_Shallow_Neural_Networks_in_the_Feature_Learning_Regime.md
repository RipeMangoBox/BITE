---
title: "Scaling Laws and Spectra of Shallow Neural Networks in the Feature Learning Regime"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Scaling_Laws_and_Spectra_of_Shallow_Neural_Networks_in_the_Feature_Learning_Regime.pdf
project_link: null
code_link: null
openreview_forum_id: Q3yLIIkt7z
aliases:
- SLSSNNFLR
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "正则化强度 λ 与有效样本量 n_eff 之间的缩放关系决定了过量风险的相变与相位边界。"
primary_logic: "通过将浅层神经网络的经验风险最小化映射到 LASSO 和矩阵压缩感知问题，结合近似消息传递（AMP）的状态演化方程，可以精确预测过量风险的缩放指数、学习权重的谱相图，并给出从欠拟合到有害过拟合的完整相图，从而为经验上观察到的权重谱与泛化的关联提供了第一性原理的解释。"
claims:
- "对角线线性网络的 ERM 等价于 LASSO 问题"
- "二次神经网络的 ERM 映射到低秩矩阵压缩感知（核范数正则化）"
- "过量风险率呈现多个相位（平台、快衰减、有害过拟合峰、最优恢复），且与权重谱紧密连接"
- "Power-law synthetic data (diagonal and quadratic networks) 上 Excess risk = Non-asymptotic state evolution prediction"
---

# Scaling Laws and Spectra of Shallow Neural Networks in the Feature Learning Regime

> [!tip] 核心洞察
> 通过将浅层神经网络的经验风险最小化映射到 LASSO 和矩阵压缩感知问题，结合近似消息传递（AMP）的状态演化方程，可以精确预测过量风险的缩放指数、学习权重的谱相图，并给出从欠拟合到有害过拟合的完整相图，从而为经验上观察到的权重谱与泛化的关联提供了第一性原理的解释。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 浅层神经网络在特征学习区域的缩放定律与谱特性 |
| 英文题名 | Scaling Laws and Spectra of Shallow Neural Networks in the Feature Learning Regime |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=Q3yLIIkt7z) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | AMP状态演化框架（基于 LASSO 和矩阵压缩感知的神经网络训练分析） |
| Dataset | Power-law synthetic data (diagonal and quadratic networks) |

> [!tip] 效果简介
> - Power-law synthetic data (diagonal and quadratic networks) 上，Excess risk 为 Non-asymptotic state evolution prediction，对比 Empirical simulations (PyTorch LBFGS)，变化 Excellent agreement across d=100,200,400,800 and various n_eff, λ。

## 概要

### 问题背景

理解深度神经网络在**特征学习区域**的泛化行为是现代机器学习理论的核心难题。现有理论大多局限于随机特征（核）区域，此时网络权重不发生显著的特征学习，因而无法解释实践中观察到的权重谱演化与泛化性能之间的紧密关联。本文聚焦一个基本问题：**对于浅层神经网络，当训练进入非线性特征学习区域时，过量风险（excess risk）的缩放定律是什么？学习到的权重谱如何随样本量和正则化强度变化？**

### 核心方法定位

本文的核心策略是将非凸的神经网络经验风险最小化（ERM）问题**等价映射**到高维统计中已深入研究的稀疏估计框架：

- **对角线线性网络**：在 L2 权重衰减下，ERM 等价于 **LASSO** 问题，有效参数为 $\theta_i = a_i w_i / \sqrt{d}$。
- **二次神经网络**：ERM 等价于**低秩矩阵压缩感知**问题，使用核范数（nuclear norm）正则化。

通过这一映射，作者得以借助**近似消息传递（AMP）**及其**状态演化（state evolution）方程**这一强大的分析工具，对两类网络进行统一的渐近分析。关键创新在于：将状态演化方程**启发式地推广到准稀疏模型**，超出其已有严格证明的渐近区域，从而覆盖从欠拟合到有害过拟合的完整相图。

### 核心发现

**1. 过量风险的完整相图。** 引入有效样本量 $n_{\mathrm{eff}}$（对角线网络 $n_{\mathrm{eff}}=n$，二次网络 $n_{\mathrm{eff}}=n/d$）统一两类架构的缩放行为。过量风险随 $n_{\mathrm{eff}}$ 和正则化强度 $\lambda$ 呈现**多个相位**：
- **平台区**（$n_{\mathrm{eff}} \ll d$，$\lambda$ 适中）：风险不随样本量衰减。
- **快速衰减区**（$n_{\mathrm{eff}} \gg d$，$\lambda$ 小）：风险以 $\Theta(d/n_{\mathrm{eff}})$ 衰减。
- **有害过拟合峰**（$n_{\mathrm{eff}} \sim d$，$\lambda$ 极小）：风险出现峰值，随后进入最优恢复区。
- **贝叶斯最优恢复**：通过调优 $\lambda$，ERM 可达到贝叶斯最优速率 $\Theta(n_{\mathrm{eff}}^{-1+1/(2\gamma)})$（欠采样）或 $\Theta(d/n_{\mathrm{eff}})$（过采样）。

**2. 权重谱的第一性原理预测。** 学习到的权重矩阵的谱分布由目标谱、噪声方差 $\Delta$ 和正则化诱导的截止阈值 $\lambda\epsilon$ 共同决定，理论预测与仿真直方图高度吻合（Figure 2）。

**3. 普适错误分解。** 在欠正则化区域，过量风险可精确分解为**过拟合项**（与噪声和谱截止相关）和**近似误差项**（与目标谱的截断相关），揭示了谱特性与泛化之间的因果机制。

### 实验验证

在幂律合成数据上，使用 PyTorch LBFGS 训练的仿真结果与**非渐近状态演化预测**在 $d=100$ 到 $800$ 的范围内高度一致（Figure 3, 5），验证了缩放律的准确性。此外，通过修剪（pruning）后处理，可在无需精细调参的情况下达到最优错误率。

### 局限与展望

当前分析限于两层浅层网络、线性/二次激活函数和各向同性高斯数据。状态演化在非比例渐近区域的严格数学证明尚未完成。未来方向包括：推广到更深架构、更一般的数据协方差结构，以及分析 SGD 等梯度下降算法下的计算缩放律与隐式偏差。



### 问题背景：特征学习区域的缩放定律之谜

现代深度学习的成功很大程度上依赖于神经网络的缩放定律——模型性能如何随数据量、参数量和计算量变化。然而，现有的理论理解存在一个根本性的缺口：**对于非线性特征学习区域的缩放定律缺乏理论解释**。绝大多数已有理论工作局限于随机特征（核）区域，即网络权重在初始化附近线性化的情形，此时网络本质上退化为核方法，无法捕捉特征学习的本质——权重在训练过程中自适应地调整以提取任务相关表征。

经验上，研究者已观察到神经网络学习权重的谱（singular value spectrum）与泛化性能之间存在紧密关联，例如重尾谱（heavy-tailed spectrum）往往对应更好的泛化。但这些观察缺乏第一性原理的理论支撑，使得缩放定律的预测和设计原则仍然依赖经验摸索。

### 核心瓶颈

本文识别出两个交织的核心瓶颈：

1. **特征学习区域的理论工具匮乏**：浅层网络的经验风险最小化（ERM）是非凸优化问题，直接分析其全局解的性质极为困难。现有理论要么依赖凸松弛，要么局限于无限宽极限下的核行为，无法描述有限宽度下的特征学习动力学。
2. **正则化与数据量的耦合机制不明**：权重衰减（L2 正则化）是训练神经网络的标准做法，但正则化强度 λ 如何与有效样本量 n_eff 相互作用，从而决定过量风险（excess risk）的缩放行为，此前没有系统性的理论刻画。

### 本文动机：从凸等价到第一性原理的相图

本文的出发点是一个关键观察：**在特定的浅层架构下，带权重衰减的 ERM 问题可以精确等价于经典的稀疏估计问题**。具体而言：

- **对角线线性网络**（diagonal linear network）的 ERM 等价于 **LASSO**（L1 正则化线性回归），参数为 θ_i = a_i w_i / √d，目标函数为：

$$\hat { \boldsymbol \theta } = \underset { \boldsymbol \theta \in \mathbb { R } ^ { d } } { \arg \min } \frac { 1 } { 2 } \sum _ { \mu = 1 } ^ { n } \left( y _ { \mu } - \boldsymbol \theta ^ { \top } \boldsymbol x _ { \mu } \right) ^ { 2 } + \lambda \| \boldsymbol \theta \| _ { 1 }$$

- **二次神经网络**（quadratic network）的 ERM 则映射到**矩阵压缩感知**（matrix compressed sensing），即低秩矩阵估计的核范数（nuclear norm）正则化问题。

这两个等价性揭示了本文的核心主题：**通过将神经网络训练映射到稀疏向量和矩阵估计问题，可以借助 LASSO 和矩阵压缩感知领域丰富的理论工具箱，从第一性原理出发精确刻画特征学习区域的缩放定律。**

### 理论工具：近似消息传递（AMP）的启发式应用

本文的分析依赖**近似消息传递**（Approximate Message Passing, AMP）及其**状态演化**（State Evolution, SE）方程。AMP 是一类在高维统计中用于分析凸优化估计器渐近性能的迭代算法框架，其状态演化方程能精确描述估计量在极限 d → ∞ 下的分布演化。

本文的创新之处在于：**将 AMP 状态演化方程以启发式的方式推广到准稀疏模型（quasi-sparse models），超越其严格证明的渐近区域**（即不再要求 n_eff/d = Θ(1) 的比例极限）。这种推广使得作者能够分析从欠拟合到有害过拟合的完整相图，并给出任意缩放极限下的过量风险率预测。虽然这一推广的严格数学证明尚未完成，但数值实验（Figure 3、Figure 5）表明非渐近状态演化预测与有限维度的仿真结果高度吻合，验证了其有效性。

### 目标设定：教师-学生框架与幂律谱

为进行可控的理论分析，本文采用教师-学生（teacher-student）设定：目标任务由一个具有相同架构的教师网络生成：

$$y _ { \mu } = f ( { \pmb x } _ { \mu } ; { \pmb W } ^ { \star } , { \pmb a } ^ { \star } ) + \sqrt { \Delta } { \xi } _ { \mu }$$

其中 Δ 控制标签噪声强度。教师网络的权重服从幂律衰减谱，例如对角线网络的有效权重满足：

$$\theta _ { i } ^ { \star } \stackrel { i . i . d . } { \sim } \mathcal { N } ( 0 , d i ^ { - 2 \gamma } )$$

其中 γ > 1/2 控制目标函数的可压缩性。这种幂律结构广泛存在于真实数据和任务中，使得分析结果具有实际相关性。

过量风险定义为教师网络与学生网络在期望输入上的均方误差：

$$R ( W , a ) = \mathbb { E } _ { x \sim \mathcal { N } ( 0 , I _ { d } ) } \left[ \left( f ( x ; W ^ { \star } , a ^ { \star } ) - f ( x ; W , a ) \right) ^ { 2 } \right]$$

### 主要贡献预览

在上述设定下，本文给出了三个核心结果（Figure 1 概括）：

1. **过量风险率的完整相图**（Result 1）：揭示了正则化强度 λ 与有效样本量 n_eff 如何共同决定过量风险的缩放指数，涵盖平台区、快衰减区、有害过拟合峰和最优恢复区。
2. **学习权重的谱预测**（Result 2）：精确刻画了训练后网络权重的谱分布，由目标谱、有效噪声 δ 和正则化截止 λε 共同决定，解释了经验上观察到的谱与泛化的关联。
3. **普适误差分解**（Result 3）：将过量风险分解为过拟合项和近似误差项，该分解不依赖于目标谱的具体形式、数据集大小或正则化强度，揭示了特征学习的内在结构。

这些结果共同构成了对浅层神经网络在特征学习区域缩放行为的第一性原理解释，为理解更深架构中的缩放定律奠定了基础。



## 核心方法与创新机理

本文的核心创新在于建立了一套从第一性原理出发的理论框架，将浅层神经网络在特征学习区域的训练动力学**精确映射**到稀疏估计问题，从而首次系统性地揭示了权重谱、正则化强度与泛化误差之间的因果机制。相对于直接求解神经网络非凸目标的传统范式，本文的方法论突破体现在以下几个关键维度。

### 问题映射与原-对偶等价

本文最根本的洞察在于将两层网络的 ERM 问题等价地转化为凸优化问题，从而将非凸神经网络训练的分析纳入经典高维统计的理论工具箱。

对于**对角线线性网络**，在 L2 权重衰减下的 ERM 目标等价于 LASSO 问题：

$$
\hat{\boldsymbol{\theta}} = \underset{\boldsymbol{\theta} \in \mathbb{R}^{d}}{\arg\min} \frac{1}{2} \sum_{\mu=1}^{n} \left(y_{\mu} - \boldsymbol{\theta}^{\top} \boldsymbol{x}_{\mu}\right)^{2} + \lambda \|\boldsymbol{\theta}\|_{1}
$$

其中有效参数 $\theta_i = a_i w_i / \sqrt{d}$。这一等价性将权重衰减正则化自然地解释为对有效权重的 L1 稀疏约束。

对于**二次神经网络**，ERM 问题映射到低秩矩阵压缩感知（核范数正则化）：

$$
\hat{\boldsymbol{S}} = \underset{\boldsymbol{S} \succeq 0}{\arg\min} \sum_{\mu=1}^{n} \left(y_{\mu} - \mathrm{Tr}[\boldsymbol{S} \boldsymbol{Z}_{\mu}]\right)^{2} + \lambda \|\boldsymbol{S}\|_{*}
$$

这两种等价性构成了整个分析框架的基石：通过将神经网络训练问题转化为稀疏向量和矩阵估计任务，作者得以利用为 LASSO 和矩阵压缩感知开发的丰富理论工具，尤其是近似消息传递（AMP）及其状态演化方程。

### AMP 状态演化框架的非渐近推广

本文的方法论核心在于**AMP 状态演化方程**的运用。与传统严格依赖比例渐近极限（$n/d = \Theta(1)$）的分析不同，作者将状态演化方程**启发式地推广到非比例渐近区域**，用于分析准稀疏模型在更广泛缩放区域的行为。这一推广使得理论能够覆盖从欠拟合到有害过拟合的完整相图，包括 $n_{\mathrm{eff}} \ll d$ 和 $n_{\mathrm{eff}} \gg d$ 等传统 AMP 理论未严格覆盖的区域。

状态演化方程通过固定点分析，将高维随机优化问题的渐近风险和学习权重谱表征为低维参数的确定性函数。具体而言，对于二次网络，ERM 的固定点方程由以下耦合系统给出：

$$
\begin{cases}
4\frac{n}{d^{2}} \delta - \frac{\delta}{\epsilon} = \partial_{1} J(\delta, \lambda\epsilon), \\
Q^{\star} + \frac{\Delta}{2} + 2\frac{n}{d^{2}} \delta^{2} - \frac{\delta^{2}}{\epsilon} = (1 - 2\frac{n}{d^{2}}\epsilon) \partial_{2} J(\delta, \lambda\epsilon)
\end{cases}
$$

其中参数 $\delta$ 量化来自标签噪声和有限样本估计的噪声水平，而 $\lambda\epsilon$ 设定正则化截断的阈值。这两个参数完全决定了学习权重的谱分布和过量风险，使得整个分析具有高度的可解释性。

### 统一的有效样本量缩放

本文引入**有效样本量** $n_{\mathrm{eff}}$ 的概念，将对角线网络和二次网络的分析统一到同一框架下：

$$
n_{\mathrm{eff}} \equiv \begin{cases}
n & \text{对角线网络} \\
n/d & \text{二次网络}
\end{cases}
$$

这一缩放因子的差异源于两种架构参数化方式的不同：对角线网络的参数数量为 $d$，而二次网络的等效参数矩阵 $\boldsymbol{S}$ 具有 $d^2$ 个自由度，但其低秩结构使得有效自由度与 $d$ 成比例。通过这一统一，两种看似不同的网络架构展现出深刻的普适性——它们的过量风险缩放律、谱相图和相位边界在 $n_{\mathrm{eff}}$ 的坐标下完全对应。

### 从谱特性到泛化的因果链条

本文首次建立了**学习权重谱**与**过量风险**之间的完整因果链条。核心发现是：学习到的权重是目标谱的噪声软阈值版本——参数 $\delta$ 控制噪声幅度，$\lambda\epsilon$ 设定软阈值截断。这一表征直接导出了过量风险的**普适错误分解**（Result 3），将风险拆解为过拟合项和近似误差项，且该分解不依赖于目标谱的具体形式、数据集大小或正则化强度。

在欠正则化情形下，分解形式为：

$$
\mathbf{R}_{n,d} = \underbrace{\delta^{2} \int_{\lambda\epsilon/\hat{\rho}_{\delta}}^{2} \mu_{\mathrm{sc}}(\mathrm{d}x) \left(x - \frac{\lambda\epsilon}{\delta}\right)^{2} + \frac{1}{d} \delta K'(\delta)(2\delta - \lambda\epsilon)^{2}}_{\text{过拟合项}} + \underbrace{\frac{1}{d} \sum_{i=K(\delta')+1}^{d} s_i^{2} + \frac{1}{d} \sum_{i=1}^{K(\delta)} \left[\left(\frac{\delta^{2}}{s_i} - \lambda\epsilon\right)^{2} + \frac{\delta^{2}}{s_i}\left(s_i + \frac{\delta^{2}}{s_i} - \lambda\epsilon\right)\right]}_{\text{近似误差项}}
$$

这一分解揭示了正则化强度 $\lambda$ 与有效样本量 $n_{\mathrm{eff}}$ 之间的缩放关系如何决定风险的相变：当 $\lambda$ 过小时，过拟合项主导风险，导致 $n_{\mathrm{eff}} \sim d$ 处的插值峰（有害过拟合）；当 $\lambda$ 过大时，近似误差项因过多特征被截断而上升。最优正则化恰好平衡这两项，使 ERM 达到贝叶斯最优速率。

### 后处理修剪策略

基于对谱结构的精确理解，本文提出了一种**无需手动调节正则化强度的修剪后处理策略**（Corollary 2）：在训练后，将学习矩阵 $\hat{\boldsymbol{S}}$ 的特征值替换为 $\mathrm{ReLU}(\lambda - (2\delta - \lambda\epsilon))$。这一操作等价于截断由有限样本效应引入的噪声体（bulk），从而在不重新训练的情况下达到最优错误率。这一发现将谱分析与实际算法改进直接连接，展示了理论洞察向实践转化的潜力。



本文提出了一套基于**近似消息传递（AMP）状态演化**的理论框架，用于精确刻画浅层神经网络在特征学习区域的缩放定律与权重谱特性。该框架的核心思路是：将非凸的神经网络经验风险最小化（ERM）问题，通过结构等价性映射到凸的稀疏估计问题，进而利用高维统计力学中成熟的 AMP 状态演化方程进行渐近分析。

整个分析 pipeline 由四个核心模块串联构成：

### 1. 问题映射 (Problem Mapping)

框架的起点是将两类浅层网络的 ERM 问题等价地转化为凸优化问题：
- **对角线线性网络**：ERM 等价于 **LASSO**（L1 正则化线性回归）问题，参数为 $\theta_i = a_i w_i / \sqrt{d}$，目标函数如公式 (5) 所示。
- **二次网络**：ERM 映射为**低秩矩阵压缩感知**问题，采用核范数正则化，目标矩阵 $\hat{\boldsymbol S}$ 由权重外积构造。

这一映射是框架成立的基石——它将神经网络训练中复杂的非凸动力学，转化为已有丰富理论工具的稀疏/低秩估计问题。

### 2. AMP 状态演化 (AMP State Evolution)

在问题映射的基础上，框架引入 AMP 算法及其**状态演化方程**。状态演化是刻画高维极限下估计量统计性质的一组确定性迭代方程，其关键参数 $\delta$（有效噪声）和 $\epsilon$（正则化截断）完全决定了渐近过量风险和权重谱。

值得注意的是，本文**启发式地将状态演化方程推广到非比例渐近区域**（即 $n_{\mathrm{eff}} / d$ 不固定为常数时），并假设其依然有效。这一假设虽未得到严格数学证明，但在仿真中表现出极佳的吻合度（见 Figure 3）。

### 3. 相图与缩放律推导 (Phase Diagram and Scaling Laws)

通过求解状态演化的固定点方程，框架导出了过量风险 $\mathsf{R}_{n_{\mathrm{eff}}, d}(\lambda)$ 的**分段缩放律**（Result 1），涵盖了从欠拟合到有害过拟合的完整相图。相图的控制变量为：
- **有效样本量** $n_{\mathrm{eff}}$：对角线网络为 $n$，二次网络为 $n/d$；
- **正则化强度** $\lambda$ 与 $n_{\mathrm{eff}}$ 之间的缩放关系。

相图揭示了多个典型相位：平台区、快衰减区、插值峰（有害过拟合峰）以及最优恢复区。各相位之间的边界由 $\lambda$ 与 $\sqrt{n_{\mathrm{eff}}/d}$ 的相对大小决定。

### 4. 谱分析与错误分解 (Spectral Analysis and Error Decomposition)

框架进一步将学习权重的谱特性与泛化误差直接关联：
- **谱相图**（Result 2）：学习到的权重是目标谱的噪声软阈值版本，由 $\delta$ 和截止值 $\lambda\epsilon$ 共同决定。二次网络的谱分布为 $\nu(x) = F_{\mu_\delta}(\lambda\epsilon) \delta_0(x) + \mu_\delta(x + \lambda\epsilon) \mathbf{1}_{x > 0}$。
- **普适错误分解**（Result 3）：在欠正则化条件下，过量风险被分解为过拟合项和近似误差项，该分解不依赖于目标谱、数据集大小或正则化强度，具有普适性。

### 输入输出流

整个框架的输入为：
- 目标任务的幂律谱参数 $\gamma$；
- 标签噪声方差 $\Delta$；
- 有效样本量 $n_{\mathrm{eff}}$ 与输入维度 $d$；
- 正则化强度 $\lambda$。

输出为：
- 过量风险的精确缩放指数；
- 学习权重的谱分布（包括体谱和尖峰）；
- 贝叶斯最优正则化策略 $\lambda_{\mathrm{opt}}$ 及对应的最优速率（Corollary 1）。

框架的**关键因果调节变量**是 $\lambda$ 与 $n_{\mathrm{eff}}$ 之间的缩放关系——正是这一关系决定了过量风险在不同相位间的相变与相位边界。



### 问题映射：从非凸 ERM 到凸稀疏估计

本文的核心方法论起点是将两层神经网络的非凸经验风险最小化（ERM）等价地转化为凸优化问题，从而能够借助稀疏估计与压缩感知的成熟理论工具箱。

**对角线线性网络 → LASSO**

对于两层线性网络 $f(x; W, a) = \sum_i a_i w_i x_i / \sqrt{d}$，在 L2 权重衰减下，ERM 目标可等价转化为标准 LASSO 问题（eq. 5）：

$$
\hat{\boldsymbol \theta} = \underset{\boldsymbol \theta \in \mathbb{R}^d}{\arg\min} \frac{1}{2} \sum_{\mu=1}^{n} \left(y_\mu - \boldsymbol \theta^\top \boldsymbol x_\mu\right)^2 + \lambda \|\boldsymbol \theta\|_1
$$

其中有效参数 $\theta_i = a_i w_i / \sqrt{d}$。这一等价性将神经网络训练直接映射为高维稀疏线性回归。

**二次神经网络 → 矩阵压缩感知**

对于二次网络 $f(x; W, a) = \frac{1}{\sqrt{p d}} \sum_j a_j (w_j^\top x)^2$，ERM 被映射到低秩矩阵压缩感知问题，即核范数正则化的低秩矩阵估计：

$$
\hat{\boldsymbol S} = \underset{\boldsymbol S \succeq 0}{\arg\min} \sum_{\mu=1}^{n} \left(y_\mu - \mathrm{Tr}[\boldsymbol S \boldsymbol Z_\mu]\right)^2 + \lambda \|\boldsymbol S\|_*
$$

其中 $\boldsymbol S = \frac{1}{\sqrt{p d}} \sum_j a_j w_j w_j^\top$ 为学习到的对称正半定矩阵，$\boldsymbol Z_\mu = x_\mu x_\mu^\top$ 为数据的外积矩阵。

### 有效样本量统一

为统一两种架构的分析，定义有效样本量（eq. 10）：

$$
n_{\mathrm{eff}} \equiv \begin{cases}
n & \text{对角线网络} \\
n/d & \text{二次网络}
\end{cases}
$$

这一缩放使得两种架构的相图和缩放律在 $n_{\mathrm{eff}}$ 坐标下呈现高度一致的普适结构。

### AMP 状态演化框架

分析的核心工具是近似消息传递（AMP）及其状态演化（State Evolution, SE）方程。本文的关键方法论创新在于：**将 SE 方程启发式地推广到非比例渐近区域**（即 $n_{\mathrm{eff}} / d$ 不固定为常数的情况），以分析准稀疏模型在所有缩放极限下的行为。

**二次网络 ERM 的固定点方程**

对于二次网络，状态演化收敛到以下固定点方程：

$$
\begin{cases}
4 \frac{n}{d^2} \delta - \frac{\delta}{\epsilon} = \partial_1 J(\delta, \lambda \epsilon), \\[6pt]
Q^\star + \frac{\Delta}{2} + 2 \frac{n}{d^2} \delta^2 - \frac{\delta^2}{\epsilon} = (1 - 2 \frac{n}{d^2} \epsilon) \partial_2 J(\delta, \lambda \epsilon)
\end{cases}
$$

其中：
- $\delta$：量化标签噪声和有限样本估计引入的有效噪声强度
- $\epsilon$：与正则化强度 $\lambda$ 和样本量 $n$ 相关的参数，控制谱的软阈值截止
- $J(\delta, \lambda\epsilon)$：由自由概率论确定的泛函，描述谱的体（bulk）和尖峰（spike）结构
- $Q^\star = \frac{1}{d} \sum_i s_i^2$：目标矩阵的 Frobenius 范数平方
- $\Delta$：标签噪声方差

### 过量风险分段缩放律

通过求解固定点方程，得到过量风险 $\mathsf{R}_{n_{\mathrm{eff}}, d}(\lambda)$ 的完整分段缩放律（Result 1, eq. 11），涵盖五个主要相位：

$$
\mathsf{R}_{n_{\mathrm{eff}}, d}(\lambda) = \begin{cases}
\Theta\left(n_{\mathrm{eff}}^{-1 + 1/(2\gamma)} + \rho(n_{\mathrm{eff}}/d)\right) & \text{if } 1 \ll n_{\mathrm{eff}} \ll d \text{ and } \lambda \ll \sqrt{\frac{n_{\mathrm{eff}}}{d}} \\[6pt]
\Theta(\lambda^{-2/3}) & \text{if } n_{\mathrm{eff}} \sim d \text{ and } \lambda \ll 1 \\[6pt]
\Theta(d / n_{\mathrm{eff}}) & \text{if } n_{\mathrm{eff}} \gg d \text{ and } \lambda \ll \sqrt{\frac{n_{\mathrm{eff}}}{d}} \\[6pt]
\Theta\left((\lambda d^{1/2} / n_{\mathrm{eff}})^{2 - 1/\gamma}\right) & \text{if } \max\left(\sqrt{\frac{n_{\mathrm{eff}}}{d}}, \frac{n_{\mathrm{eff}}}{d^{-1/2}}\right) \ll \lambda \ll \frac{n_{\mathrm{eff}}}{d^{1/2}} \\[6pt]
\Theta(\lambda^2 d^2 / n_{\mathrm{eff}}^2) & \text{if } \sqrt{\frac{n_{\mathrm{eff}}}{d}} \ll \lambda \ll \frac{n_{\mathrm{eff}}}{d^{\gamma + 1/2}}
\end{cases}
$$

其中 $\gamma$ 为教师网络权重幂律衰减指数（$\theta_i^\star \sim \mathcal{N}(0, d i^{-2\gamma})$），$\rho(n_{\mathrm{eff}}/d)$ 为描述插值峰的普适函数。

### 学习权重的谱特性

Result 2 给出了学习权重的谱分布。对于二次网络，学习矩阵 $\hat{\boldsymbol S}$ 的谱密度为（eq. 16）：

$$
\nu(x) = F_{\mu_\delta}(\lambda \epsilon) \delta_0(x) + \mu_\delta(x + \lambda \epsilon) \mathbf{1}_{x > 0}
$$

其中：
- $\mu_\delta$：在半圆律体上叠加尖峰的谱分布，尖峰位置由目标谱和 $\delta$ 共同决定
- $\lambda\epsilon$：正则化引起的谱左移量，低于此截止的奇异值被压为零
- $F_{\mu_\delta}(\lambda\epsilon)$：零奇异值的累积质量

**谱相位的调控机制**：正则化强度 $\lambda$ 通过控制截止 $\lambda\epsilon$ 来调节谱结构——弱正则化时保留大量尖峰但引入估计噪声，强正则化时截断噪声但也丢失部分信号尖峰。最优正则化恰好截断噪声体（bulk）而保留所有信息性尖峰。

### 普适错误分解

Result 3 给出了欠正则化情形下的普适过量风险分解（eq. 17）：

$$
\mathbf{R}_{n,d} = \underbrace{\delta^2 \int_{\lambda\epsilon / \hat{\rho}_\delta}^{2} \mu_{\mathrm{sc}}(\mathrm{d}x) \left(x - \frac{\lambda\epsilon}{\delta}\right)^2 + \frac{1}{d} \delta K'(\delta)(2\delta - \lambda\epsilon)^2}_{\text{过拟合项}} + \underbrace{\frac{1}{d} \sum_{i=K(\delta')+1}^{d} s_i^2 + \frac{1}{d} \sum_{i=1}^{K(\delta)} \left[\left(\frac{\delta^2}{s_i} - \lambda\epsilon\right)^2 + \frac{\delta^2}{s_i}\left(s_i + \frac{\delta^2}{s_i} - \lambda\epsilon\right)\right]}_{\text{近似误差项}}
$$

其中 $\mu_{\mathrm{sc}}(x) = (2\pi)^{-1}\sqrt{4 - x^2}\,\mathbf{1}_{x \in [-2,2]}$ 为标准半圆律密度。该分解的**普适性**体现在：不依赖于具体的目标谱、数据集大小或正则化强度，对任意 $\Delta \geq 0$ 均成立，且在不同谱相位间保持一致结构。过拟合项源于噪声体（bulk）的残留，近似误差项则来自未学习到的尖峰和已学习尖峰的估计偏差。

### 贝叶斯最优速率

通过调优正则化强度至 $\lambda_{\mathrm{opt}}$，ERM 的过量风险可达到贝叶斯最优速率（Corollary 1, eq. 14）：

$$
\mathsf{R}_{n_{\mathrm{eff}}, d}(\lambda_{\mathrm{opt}}) = \Theta(\mathsf{R}_{n_{\mathrm{eff}}}^{\mathrm{BO}}) = \begin{cases}
\Theta(n_{\mathrm{eff}}^{-1 + 1/(2\gamma)}) & \text{if } \Delta > 0 \text{ and } 1 \ll n_{\mathrm{eff}} \ll d^{2\gamma} \\[6pt]
\Theta(d / n_{\mathrm{eff}}) & \text{if } \Delta > 0 \text{ and } n_{\mathrm{eff}} \gg d^{2\gamma}
\end{cases}
$$

最优正则化参数在欠参数化区域（$n_{\mathrm{eff}} \ll d$）取 $\lambda_{\mathrm{opt}} = O(\sqrt{n_{\mathrm{eff}}/d})$，在过参数化区域（$n_{\mathrm{eff}} \gg d$）取 $\lambda_{\mathrm{opt}} = O(n_{\mathrm{eff}}/d^{\gamma+1/2})$。



## 实验与关键发现

### 实验设置

本文的实验验证在两个架构上进行：**对角线线性网络**和**二次神经网络**。两种网络均为两层结构，输入来自各向同性的高斯分布 $\mathcal{N}(0, I_d)$，目标由同架构的教师网络生成，教师权重遵循幂律衰减 $i^{-2\gamma}$（对角线网络）或旋转不变的幂律谱（二次网络），并可选地叠加标签噪声 $\Delta$。训练采用 PyTorch 的 LBFGS 优化器，等价于求解 ERM 问题。

核心控制变量为**有效样本量** $n_{\mathrm{eff}}$（对角线网络 $n_{\mathrm{eff}}=n$，二次网络 $n_{\mathrm{eff}}=n/d$）和**正则化强度** $\lambda$。理论预测来自近似消息传递（AMP）的状态演化方程，在非渐近区域（$n_{\mathrm{eff}}/d$ 变化）作为启发式使用。

### 主实验结果

**Figure 3** 展示了过量风险在仿真与非渐近状态演化预测之间的对比（$d=100,200,400,800$，$\lambda \in \{1/d, 1, \sqrt{d}\}$，$\Delta=0.5$）。仿真点与理论实线在所有 $n_{\mathrm{eff}}$ 范围内均表现出极好的一致性，尽管状态演化仅在 $n_{\mathrm{eff}}/d=\Theta(1)$ 且 $d\gg1$ 的渐近极限下严格成立。图中黑色线条标注了 Result 1 预测的衰减速率，同样与仿真吻合。

关键观察：
- **欠参数化区域**（$n_{\mathrm{eff}} \ll d$）：风险处于平台期，受限于目标谱中未学习的高频分量。
- **插值峰**（$n_{\mathrm{eff}} \sim d$）：正则化不足时出现有害过拟合峰，风险由 bulk 的第二矩主导，衰减率为 $\Theta(\lambda^{-2/3})$。
- **过参数化区域**（$n_{\mathrm{eff}} \gg d$）：风险快速衰减，最优速率可达 $\Theta(d/n_{\mathrm{eff}})$。

**Figure 5** 在无噪声设置（$\Delta=0$）下重复了相同对比，进一步验证了 Result 4 的缩放律预测。

### 谱特性验证

**Figure 2** 对比了不同训练相下仿真与理论预测的权重谱。蓝色直方图为训练后的特征值分布，紫色和橙色分别为理论预测的 bulk 和 spike。理论不仅准确捕捉了 bulk 的平移（正则化使 bulk 左移约 $\lambda d^2/(4n)$），还预测了零处的尖峰（为视觉清晰未绘制）。各相位（II-VI）的谱结构差异显著：从重尾 spike 主导（Phase II-III）到 bulk 截断（Phase V-VI），均与理论一致。

### 消融分析

**正则化强度 $\lambda$ 的调控**（Figure 1 和 Figure 8）：
- 在 $n_{\mathrm{eff}} \ll d$ 时，减小 $\lambda$ 可使风险从平台转入快衰减相，但需穿越插值峰。
- 最优正则化策略是截断 bulk（将过拟合项归零），仅保留近似误差项，无需手动调参即可通过**修剪后处理**实现（Corollary 2）：将学习矩阵的特征值替换为 $\text{ReLU}(\lambda - (2\delta - \lambda\epsilon))$。

**修剪（pruning）后处理**：
- 在无需调整 $\lambda$ 的情况下，修剪可达到最优错误率（置信度 0.9）。
- 该方法等价于自动选择截断阈值，消除 bulk 噪声分量。

### 失败模式与局限性

1. **非渐近区域的理论缺口**：状态演化方程在 $n_{\mathrm{eff}}/d$ 变化时的严格数学证明尚未完成，当前依赖启发式假设。尽管仿真验证了其准确性，但理论完备性需进一步工作。
2. **架构限制**：分析仅限于两层浅层网络，激活函数为线性或二次。扩展到更深架构和更复杂激活函数（如 ReLU）仍需新的理论工具。
3. **数据分布假设**：当前结果依赖于各向同性高斯输入和幂律目标谱。在一般协方差结构下的缩放律行为是开放问题。
4. **优化器偏差**：本文聚焦 ERM 解的统计性质，未涉及 SGD 等梯度下降算法的隐式偏差和计算缩放律。

### 开放问题

- 能否将状态演化猜想严格推广到任意缩放极限？
- 如何在更一般的数据协方差和特征结构下分析缩放律？
- SGD 的隐式偏差如何与权重谱的 heavy-tail 特性关联？
- 类似的第一性原理分析能否扩展到更深层网络？

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Q3yLIIkt7z/figures/006_Table_1.jpg]]

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Q3yLIIkt7z/figures/007_Table_2.jpg]]

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_Q3yLIIkt7z/figures/004_Figure_4.jpg]]
*Figure 4: Effective number of samples $n _ { \mathrm { e f f } }$ (n for diagonal, n / d for quadratic) Figure 4: Excess risk rates of result 4 for the noiseless task ( $\Delta$ = 0 ) , the corresponding spectral properties of neural networks



## 定位与知识库关联

### 问题映射：从非凸训练到凸稀疏估计

本工作的核心方法论贡献在于将浅层神经网络的经验风险最小化（ERM）等价地映射到经典的稀疏估计问题，从而绕开了对非凸训练动力学的直接分析。具体而言：

- **对角线线性网络**的 ERM 等价于 LASSO 问题，参数为 $\theta_i = a_i w_i / \sqrt{d}$，目标函数为 (5) 式。这一等价性使得权重衰减正则化自然地转化为 L1 正则化。
- **二次神经网络**的 ERM 映射到低秩矩阵压缩感知问题，采用核范数正则化。目标矩阵定义为 $S^\star := \frac{1}{\sqrt{pd}} \sum_{j=1}^p a_j^\star \boldsymbol{w}_j^\star (\boldsymbol{w}_j^\star)^T$，具有旋转不变性和幂律特征值。

这两类映射构成了统一分析框架的基石，使得可以利用 LASSO 和矩阵压缩感知的丰富理论工具箱来精确刻画神经网络的泛化行为。

### 分析工具：近似消息传递与状态演化

论文的分析依赖于**近似消息传递（AMP）及其状态演化（SE）方程**。状态演化在高维极限 $n, d \to \infty$ 且 $n/d = \Theta(1)$ 下是严格成立的，但本文的关键技术突破在于**启发式地将状态演化方程推广到非比例渐近区域**（即 $n_{\text{eff}}/d$ 可任意变化时），并以此推导出所有缩放区域的过量风险率和权重谱。

这一推广目前尚缺乏严格的数学证明。文中明确指出：“对极限的更精细控制仍然是完全严格证明 AMP 在此设置下成立的必要条件。”因此，本文的理论结果应理解为基于状态演化猜想的精确预测，其有效性由大量数值实验（Figure 3、Figure 5）提供强有力的经验支撑。

### 与现有理论的定位关系

| 理论框架 | 核心假设 | 本文定位 |
|---------|---------|---------|
| 随机特征/核区域（NTK） | 权重冻结，网络退化为线性模型 | 本文突破此限制，分析特征学习区域 |
| 比例渐近AMP理论 | $n/d = \Theta(1)$ | 本文推广至任意 $n_{\text{eff}}/d$ 缩放 |
| 岭回归（L2 正则化） | 线性模型基线 | 本文通过 L1/核范数正则化揭示稀疏性与谱结构 |

与**岭回归**（Ridge Regression）等经典线性基线的对比体现在：本文揭示了 L1 正则化（对角线网络）和核范数正则化（二次网络）如何通过软阈值机制产生稀疏的权重谱，从而在幂律目标下实现贝叶斯最优的过量风险率。这一机制是 L2 正则化所不具备的。

### 适用边界与局限

1. **架构限制**：分析仅限于两层浅层网络，且激活函数为线性（对角线网络）或二次（二次网络）。扩展到更深架构和更复杂的激活函数（如 ReLU）是开放问题。
2. **数据假设**：输入数据假设为各向同性的高斯分布 $\boldsymbol{x} \sim \mathcal{N}(0, I_d)$，目标权重/矩阵假设具有幂律谱。在更一般的数据协方差和特征结构下的分析尚待完成。
3. **算法限制**：理论分析针对 ERM 的全局最优解，未涉及随机梯度下降（SGD）等梯度下降算法的隐式偏差和计算缩放律。
4. **理论严格性**：状态演化在非比例渐近区域的使用缺乏严格数学证明，文中将其定位为“猜想”，需要未来工作提供乘法界或更精细的极限控制。

### 开放问题

- **状态演化的严格推广**：能否将状态演化猜想严格推广到任意缩放极限 $n_{\text{eff}}/d \to 0$ 或 $\to \infty$？
- **更一般的数据结构**：如何在非各向同性协方差和更一般的特征结构下分析缩放律与谱特性？
- **计算缩放律**：SGD 等梯度下降算法下的计算缩放律和隐式偏差如何与权重谱的相图关联？
- **深层网络扩展**：是否可以将类似的第一性原理分析（问题映射 + AMP 状态演化）扩展到更深层的网络？文中指出这是“有趣的未来方向”。
- **普适错误分解的推广**：文中的普适错误分解（Result 3）是否适用于更广泛的架构族？



## 原文 PDF

![[paperPDFs/ICLR_2026/Scaling_Laws_and_Spectra_of_Shallow_Neural_Networks_in_the_Feature_Learning_Regime.pdf]]
