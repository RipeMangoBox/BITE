---
title: "Training-Free Determination of Network Width via Neural Tangent Kernel"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Training_Free_Determination_of_Network_Width_via_Neural_Tangent_Kernel.pdf
openreview_forum_id: 0elvad3gEu
aliases:
- NCW
- TFDNWNTK
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/theory
core_operator: "NTK的最小特征值 μ_min（控制泛化误差上界）"
primary_logic: "训练前通过计算初始化NTK的最小特征值，并监测其随宽度增长的饱和趋势，便可无训练地确定泛化性能饱和的“cardinal width”，从而免去反复训练搜索。"
claims:
- "无限宽网络测试误差上界由 μ_min^{-2} 主导（Theorem 3.2）"
- "有限宽网络在惰性训练下测试误差仍由 μ_min 控制，并附加宽度依赖的衰减项（Theorem 3.8）"
- "μ_min 随宽度增加而上升并趋于饱和，饱和点与测试损失平坦区对齐（Figure 2）"
- "方法对优化器、学习率、初始化及数据子采样均具有鲁棒性（Figure 5, Figure 6）"
---

# Training-Free Determination of Network Width via Neural Tangent Kernel

> [!tip] 核心洞察
> 训练前通过计算初始化NTK的最小特征值，并监测其随宽度增长的饱和趋势，便可无训练地确定泛化性能饱和的“cardinal width”，从而免去反复训练搜索。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于神经正切核的训练无关网络宽度确定方法 |
| 英文题名 | Training-Free Determination of Network Width via Neural Tangent Kernel |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0elvad3gEu) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/theory |
| Method | 基于NTK最小特征值的训练无关cardinal width选择 |
| Dataset | DNN on Diabetes / California Housing, CNN / ResNet on CIFAR-10 / MNIST, DNN on MNIST / XOR (classification) |

> [!tip] 效果简介
> - DNN on Diabetes / California Housing 上，Test MSE 为 cardinal width 预测值（如 Diabetes 94.40），对比 手动训练多宽度观察到的饱和宽度，变化 测试损失在预测的 cardinal width 处饱和; Figure 2 显示对齐。
> - CNN / ResNet on CIFAR-10 / MNIST 上，Test loss (cross-entropy) 为 cardinal width 预测值，对比 训练多宽度观察到的饱和宽度，变化 预测宽度与测试损失平坦趋势一致。
> - DNN on MNIST / XOR (classification) 上，Test loss 为 cardinal width 预测值 (e.g., MNIST m*≈131.19)，对比 逐宽度训练观察到的饱和点，变化 在预测的 cardinal width 处测试损失不再下降; 验证分类扩展可行性。

## 概述

深度神经网络的泛化性能通常随宽度增加而提升，但这一趋势终会饱和。实践中，研究者往往通过反复训练不同宽度的网络来寻找饱和点，缺乏理论指导，导致试错成本高昂且饱和宽度难以预判。本文提出一种**无需训练**的网络宽度确定方法，核心思路是：利用初始化时的经验神经正切核（empirical NTK）的最小特征值 $\mu_{\min}$ 作为代理指标，监测其随宽度增长的饱和趋势，从而直接判定泛化性能饱和的“cardinal width”。

**理论支撑**。无限宽网络的测试误差上界由 $\mu_{\min}^{-2}$ 主导（Theorem 3.2）；在惰性训练（lazy training）下，有限宽网络的泛化误差仍由初始化 NTK 的最小特征值控制，并附加一个随宽度衰减的校正项 $\phi(m)$（Theorem 3.8）。这意味着 $\mu_{\min}$ 的饱和行为直接反映了泛化性能的饱和点。

**方法定位**。与传统交叉验证宽度搜索（需对多个候选宽度进行完整训练）不同，本方法仅在初始化时构建一次 NTK、估计其最小特征值，并通过拟合饱和曲线自动判定 cardinal width，完全免去训练过程。具体流程包括：扫描候选宽度 → 构建初始化 NTK → 使用 LOBPCG 估计 $\mu_{\min}$ → 最小二乘拟合饱和曲线 $g(x) = -ax/(b+x) + c$ → 取拟合斜率可忽略的最小宽度作为 cardinal width。

**主要结果**。在回归任务（Diabetes、California Housing）和分类任务（MNIST、XOR）上，预测的 cardinal width 与测试损失平坦区高度对齐（Figure 2, Figure 7），覆盖 DNN、CNN、ResNet 等多种架构。消融实验表明，该方法对优化器、学习率、初始化方案（Figure 5）以及 10–50% 的数据子采样（Figure 6）均具有鲁棒性。

**局限与开放问题**。理论严格证明目前仅针对回归任务；分类任务的延伸尚无理论保证。在极端超参数（如极大学习率）下 cardinal width 可能发生偏移。NTK 最小特征值估计仍涉及较大计算开销，但可通过子采样缓解。未来方向包括将理论推广到特征学习状态、建立分类问题的对应理论，以及将 cardinal width 概念扩展到网络深度、注意力头数等其他结构维度。

## 背景与动机

深度神经网络的宽度（即每层神经元数量）是决定模型容量与泛化性能的关键结构超参数。然而，在实践中，宽度的选择长期依赖经验法则或昂贵的试错过程：研究者通常需要针对多个候选宽度逐一完成完整训练，再根据验证集性能人工判断最优宽度。这种方式的根本瓶颈在于**缺乏理论指导的宽度选择准则**——我们无法在训练前预判泛化性能随宽度增长的饱和点，导致计算资源浪费与次优架构的隐性风险。

这一困境在神经正切核（Neural Tangent Kernel, NTK）理论框架下获得了新的审视视角。NTK 理论揭示了无限宽网络与核方法之间的深刻联系：在无限宽极限下，梯度下降训练的神经网络等价于以 NTK 为核的核岭回归（Kernel Ridge Regression, KRR）。这为分析泛化误差提供了严格的数学工具，但现有工作主要聚焦于无限宽极限本身，并未回答一个更具实践价值的问题：**如何在有限宽度下，无需训练即可确定泛化性能趋于饱和的“够用”宽度？**

本文正是从这一缺口出发，提出了一种基于 NTK 最小特征值的训练无关宽度选择方法。其核心洞察简洁而有力：NTK 的最小特征值 $\mu_{\min}$ 控制着泛化误差的上界，而 $\mu_{\min}$ 随宽度增加呈现先上升后饱和的趋势——这一饱和点恰好与测试损失的平坦区对齐。因此，只需在初始化时计算不同宽度下的 $\mu_{\min}$ 并监测其饱和趋势，即可在**不进行任何训练**的前提下定位“cardinal width”——即泛化性能不再显著提升的最小宽度。这一思路将宽度选择从“训练-评估-比较”的试错循环，转变为“构建 NTK-估计特征值-拟合饱和曲线”的单次分析流程，从根本上改变了网络宽度确定的范式。

## 核心创新

本文的核心创新在于将网络宽度的选择问题从一个依赖反复训练的经验搜索过程，转化为一个仅需在初始化时计算神经正切核（NTK）最小特征值的训练无关判定问题。这一转变通过两个关键的 changed slots 实现。

### 从训练后评估到训练前判定的准则转换

传统方法（如交叉验证宽度搜索）的宽度选择准则建立在**训练后**的测试性能之上，需要对多个候选宽度分别完成完整训练，再根据验证集表现人工选择。这构成了一个高成本的试错循环：训练成本随宽度增加而显著增长，且饱和点难以预判。

本文提出的准则将判定依据前移至**训练前**：直接使用初始化 NTK 的最小特征值 $\mu_{\min}(K_m^{(0)})$ 作为宽度是否足够的代理信号。理论分析（Theorem 3.2）表明，无限宽网络的测试误差上界由 $\mu_{\min}^{-2}$ 主导：

$$E_g \leq C_1 \mu_{\min}^{-2} + C_2 \sigma^2 n \mu_{\min}^{-2}$$

对于有限宽网络（Theorem 3.8），惰性训练下的泛化误差同样由初始化 NTK 的最小特征值控制，并附加一个随宽度衰减的校正项：

$$E_g^{(m)} \leq \frac{C_4}{\mu_{\min}(K_m^{(0)})^2} + C_5 \frac{\phi(m)}{\mu_{\min}(K_m^{(0)})^2}$$

这一理论链条建立了从“NTK 最小特征值”到“泛化误差上界”的直接因果通路。当 $\mu_{\min}$ 随宽度增加而趋于饱和时，泛化误差的上界不再显著下降，意味着继续增加宽度已无实质收益——这正是 cardinal width 的理论基础。

### 从多次训练到零训练的过程简化

第二个 changed slot 是**所需训练过程的完全消除**。传统方法需对每个候选宽度执行完整训练（包括前向传播、反向传播、多轮迭代），而本文方法仅需在初始化时构建一次 empirical NTK 矩阵 $K_m^{(0)}$，并通过 LOBPCG 算法估计其最小特征值，整个过程无需任何梯度更新。

具体而言，方法流程（Algorithm 1）包含四个模块：
1. **初始化 NTK 构建**：在给定宽度下，利用随机初始化参数计算 empirical NTK 矩阵；
2. **最小特征值估计**：使用 LOBPCG 高效估计 $\mu_{\min}(K_m^{(0)})$；
3. **饱和曲线拟合**：对不同宽度的 $\mu_{\min}$ 估计值进行最小二乘拟合，采用双曲饱和函数 $g(x) = -\frac{ax}{b+x} + c$；
4. **拐点判定**：找到拟合曲线斜率可忽略的最小宽度，作为 cardinal width。

这一流程的计算开销主要来自 NTK 构建和特征值估计，但可通过数据子采样（仅需 10-50% 的训练样本）显著降低，且 cardinal width 估计在子采样下保持稳定（Figure 6）。

### 因果机制的实证验证

Figure 2 展示了核心实证证据：$\mu_{\min}$ 的饱和点（绿色竖线）与测试损失平坦区高度对齐，覆盖 DNN、CNN、ResNet 在多个数据集上的表现。这表明基于 $\mu_{\min}$ 饱和的 cardinal width 判定准则在实际训练中有效。消融实验进一步表明，cardinal width 对优化器（Adam/SGD）、学习率、初始化方案（He/NTK）均具有鲁棒性（Figure 5），验证了准则的稳定性和实用价值。

> **需注意**：理论严格证明仅针对回归任务给出，分类任务的延伸目前缺乏理论保证，但实验（Figure 7）显示了初步可行性。

## 整体框架

![[assets/figures/papers/iclr26_0012_0elvad3gEu_Training-Free_Determination_of_Network_Width_via/figures/004_Figure_2.jpg]]
*Figure 2: The cardinal width identified using fitted $\mu _ { \mathrm { m i n } }$ . Green lines indicate where the growth of $\mu _ { \mathrm { { m i n } } }$ slows down, suggesting a saturation point. At these widths, the test loss also plateaus, validating the proposed criterion for determining the cardinal width

本文提出的训练无关宽度选择方法围绕一个核心因果旋钮展开：**NTK 的最小特征值 $\mu_{\min}$**。理论分析表明，无论是无限宽网络（Theorem 3.2）还是惰性训练下的有限宽网络（Theorem 3.8），其泛化误差上界均由 $\mu_{\min}^{-2}$ 主导。基于这一洞察，方法将宽度选择问题转化为对 $\mu_{\min}$ 饱和趋势的监测，从而免去反复训练的试错成本。

整个 pipeline 由四个模块串联构成，输入为候选宽度集合、训练数据集和初始化方案，输出为推荐的 cardinal width：

### 模块一：初始化 NTK 构建

对每个候选宽度 $m$，仅需在**随机初始化参数**下计算一次 empirical NTK 矩阵 $K_m^{(0)}$。这一步无需任何训练过程，是方法实现训练无关性的基础。具体地，矩阵元素定义为参数梯度内积在训练样本对上的期望近似。

### 模块二：最小特征值估计

为高效获取 $\mu_{\min}(K_m^{(0)})$，采用 **LOBPCG（Locally Optimal Block Preconditioned Conjugate Gradient）** 算法。该方法通过在小规模子空间上最小化 Rayleigh 商来逼近极端特征对，避免了全矩阵分解的高昂计算开销。作者指出，对于较大数据集，可进一步通过 10–50% 的子采样来降低计算成本，同时保持 cardinal width 估计的稳定性（Figure 6）。

### 模块三：饱和曲线拟合

将不同宽度下估计的 $\mu_{\min}$ 值作为观测点，采用双曲饱和函数进行最小二乘拟合：

$$g(x) = -\frac{ax}{b+x} + c$$

该函数形式能够捕捉 $\mu_{\min}$ 随宽度增加先快速上升、后趋于饱和的典型行为模式。

### 模块四：拐点判定

在拟合曲线上找到**斜率可忽略的最小宽度**，即判定为 cardinal width。判定准则的直观含义是：当进一步增加宽度不再带来 $\mu_{\min}$ 的显著提升时，泛化性能也已达到饱和。实验表明，该判定点与测试损失的实际平坦区高度对齐（Figure 2），覆盖 DNN、CNN、ResNet 及多个回归/分类数据集。

### 输入输出流总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| NTK 构建 | 候选宽度 $m$、训练数据 $X$、初始化方案 | $K_m^{(0)}$ 矩阵 |
| 特征值估计 | $K_m^{(0)}$ | $\mu_{\min}(K_m^{(0)})$ 估计值 |
| 曲线拟合 | $\{(m, \mu_{\min})\}$ 观测点集 | 拟合参数 $(a, b, c)$ |
| 拐点判定 | 拟合曲线 $g(m)$ | cardinal width $m^*$ |

整个流程的突出优势在于：**只需在初始化时构建一次 NTK 并估计最小特征值，无需任何训练步骤**，即可给出与多轮完整训练搜索相一致的宽度推荐。消融实验进一步表明，该推荐对优化器选择、学习率、初始化方案均具有鲁棒性（Figure 5），验证了方法的实用可靠性。

## 核心模块与公式推导

### 核心因果机制：μ_min 的饱和探测

整个方法围绕一个关键量展开——初始化 NTK 的最小特征值 μ_min(K_m^{(0)})。理论分析表明，无论是无限宽网络还是惰性训练下的有限宽网络，泛化误差的上界均由该特征值的平方反比主导。具体地，无限宽网络的测试误差界为：

$$E_g \leq C_1 \mu_{\min}^{-2} + C_2 \sigma^2 n \mu_{\min}^{-2}$$

而在有限宽惰性训练下，泛化误差进一步包含一个随宽度衰减的校正项：

$$E_g^{(m)} \leq \frac{C_4}{\mu_{\min}(K_m^{(0)})^2} + C_5 \frac{\phi(m)}{\mu_{\min}(K_m^{(0)})^2}$$

其中 φ(m) 随宽度增加而趋于零，表征有限宽与无限宽 NTK 之间的漂移。这一结构揭示了核心因果链：**宽度增加 → μ_min 上升 → 泛化误差界收紧 → 测试性能改善；当 μ_min 趋于饱和时，进一步增加宽度的边际收益消失**。因此，无需实际训练，仅通过监测 μ_min 随宽度的饱和趋势即可定位 cardinal width。

### 误差分解：从无限宽到有限宽

将有限宽网络输出 f_m(T) 与无限宽 NTK 预测器 f_∞ 之间的差距分解为三项：

$$|f_m(T) - f_\infty| \le \underbrace{|f_m(T) - \widehat{f}_m^{(T)}|}_{\text{(G1) 线性化间隙}} + \underbrace{|\widehat{f}_m^{(T)} - \widehat{f}_m^{(0)}|}_{\text{(G2) 时间变分间隙}} + \underbrace{|\widehat{f}_m^{(0)} - f_\infty|}_{\text{(G3) 初始化间隙}}$$

- **(G1)** 线性化间隙：衡量实际网络与其线性化近似之间的偏离，由训练过程中 NTK 的路径漂移控制，使用 Duhamel 原理与 Gronwall 不等式得到界：

$$|f_m(T) - \widehat{f}_m^{(T)}| \leq \frac{C_{\mathrm{lin}}}{\mu_{\min}(K_m^{(0)})} \sup_{u \in [0,T]} \| K_m^{(u)} - K_m^{(T)} \|$$

- **(G2)** 时间变分间隙：衡量 KRR 预测器从初始化到训练结束的变化，通过 resolvent 恒等式得到界：

$$|\widehat{f}_m^{(T)} - \widehat{f}_m^{(0)}| \leq \frac{C_{\mathrm{tv}}}{\mu_{\min}^2(K_m^{(0)})} \| K_m^{(T)} - K_m^{(0)} \|$$

- **(G3)** 初始化间隙：衡量初始化时有限宽 NTK 与无限宽 NTK 的差异，直接由 ‖K_m^{(0)} - K_∞‖ 控制。

三项合并后得到最终的有限宽误差控制律：

$$|f_m(T) - f_\infty| \le \frac{C_*}{\mu_{\min}^2(K_m^{(0)})} \Big( \sup_{u\in[0,T]} \|K_m^{(u)} - K_m^{(T)}\| + \|K_m^{(T)} - K_m^{(0)}\| + \|K_m^{(0)} - K_\infty\| \Big)$$

该界的所有核漂移项在惰性训练假设下均随宽度衰减，因此 μ_min 成为决定泛化性能饱和的唯一主导因子。

### KRR 预测器与谱分解

在理论分析中，无限宽 NTK 对应一个核岭回归（KRR）预测器，其闭式解为：

$$\hat{f}(\mathbf{x}) = \mathbf{k}(\mathbf{x}, X) (K + n\alpha I_n)^{-1} \mathbf{y}$$

通过有限数据集上的经验 Mercer 展开，将 NTK 矩阵 K 在经验测度下分解为：

$$K(\pmb{x},\pmb{x}') = \sum_{k=1}^{n} \lambda_k \phi_k(\pmb{x}) \phi_k(\pmb{x}') \quad \mathrm{on~supp}(p_n)$$

据此，KRR 的泛化误差可表达为各模态的偏差-方差分解：

$$E_g = \frac{1}{1-\gamma} \sum_{k=1}^{n} \frac{\mu_k}{n(\kappa+\mu_k)^2} \Big( \kappa^2 w_k^2 + \sigma^2 \mu_k \Big)$$

在零脊惩罚（ridgeless）极限下，最小特征值 μ_min 成为误差的主导项，偏差项的上界直接由 μ_min^{-2} 控制：

$$\frac{B}{1-\gamma} \leq C_1 \mu_{\min}^{-2}$$

### 算法流水线：从 μ_min 到 cardinal width

基于上述理论，方法通过四个模块实现无需训练的宽度选择：

1. **初始化 NTK 构建**：对每个候选宽度 m，使用随机初始化参数计算 empirical NTK 矩阵 K_m^{(0)}。
2. **最小特征值估计（LOBPCG）**：采用 Locally Optimal Block Preconditioned Conjugate Gradient 方法，通过在小子空间上最小化 Rayleigh 商来估计 μ_min(K_m^{(0)})。
3. **饱和曲线拟合**：对不同宽度的 μ_min 估计值，用最小二乘法拟合双曲饱和函数：

$$g(x) = -\frac{ax}{b+x} + c$$

4. **拐点判定**：找到拟合曲线斜率可忽略的最小宽度，即 cardinal width。

整个流程仅需一次初始化前向传播和 NTK 计算，无需任何训练步骤，从根本上消除了传统交叉验证搜索的试错成本。

## 实验与分析

### 一、核心发现：最小特征值饱和与测试损失平坦区的对齐

本文的核心实验主张是：**初始化 NTK 的最小特征值 μ_min 随网络宽度增加的饱和点，与测试损失的平坦区高度一致**，且这一关系对多种架构和数据集具有普适性。

Figure 2 展示了这一对齐现象的四组典型案例：
- **DNN on Diabetes**：μ_min 的增长在宽度约 94 处显著放缓（绿色竖线），对应测试 MSE 恰好进入平坦区。
- **DNN on California Housing**：类似的对齐出现，饱和宽度因数据集特性而不同。
- **CNN on CIFAR-10 / ResNet on MNIST**：即使在卷积和残差架构上，μ_min 的饱和趋势仍能准确预测测试损失不再下降的宽度。

这一对齐关系的理论依据来自 Theorem 3.8：惰性训练下有限宽网络的测试误差上界为

$$E_g^{(m)} \leq \frac{C_4}{\mu_{\min}(K_m^{(0)})^2} + C_5 \frac{\phi(m)}{\mu_{\min}(K_m^{(0)})^2}$$

其中 $\phi(m)$ 是随宽度衰减的校正项。当宽度足够大时，$\phi(m) \to 0$，误差界完全由 $\mu_{\min}^{-2}$ 主导。Figure 1（底部）的实证验证表明，测试损失确实被 $O(\mu_{\min}^{-2})$ 上界控制，但实际趋势更接近 $O(1/\sqrt{\mu_{\min}})$，说明理论界虽然保守，但方向正确。


![[assets/figures/papers/iclr26_0012_0elvad3gEu_Training-Free_Determination_of_Network_Width_via/figures/003_Figure_1.jpg]]
*Figure 1: $\mu _ { \mathrm { m i n } } ^ { - 2 }$ and test loss on two-layer networks. From the top plots, we see that the decrease in the test loss and the increase in $\mu _ { \mathrm { { m i n } } }$ saturate in wide networks. The bottom plot illustrates that the test loss is upper bounded by $\mathcal { O } ( \mu _ { \operatorname* { m i n } } ^ { - 2 }$ ) (consistent with Theorem 3.8) but is closer to $\mathcal { O }$ ( 1 / $\sqrt { \mu _ { \mathrm { m i n } } }$ ) The scope of this plot is the point with sufficiently large width (closer to yellow)

### 二、分类任务的拓展验证

尽管理论证明仅覆盖回归任务，作者在分类场景下进行了探索性验证。Figure 7 展示了 **DNN on MNIST** 的结果：算法在 $\mu_{\min}(K_m^{(0)})$ 的拟合曲线上标记出 cardinal width $m^* \approx 131.19$（垂直虚线），而下方测试损失曲线在该宽度附近明显饱和。这意味着方法在分类任务上具有潜在可行性，但需注意 **分类任务尚无理论保证**，这一结论的置信度低于回归场景（置信度 0.9 vs 0.95）。


![[assets/figures/papers/iclr26_0012_0elvad3gEu_Training-Free_Determination_of_Network_Width_via/figures/012_Figure_7.jpg]]
*Figure 7: The predicted cardinal width in classification tasks. At the cardinal width identified using our algorithm, the test loss correspondingly saturates, indicating the potential extension of our method to classification tasks*

### 三、关键消融：对训练超参数的鲁棒性

方法的实用性取决于 cardinal width 是否对训练配置敏感。Figure 5 在 Diabetes 数据集上测试了以下维度的鲁棒性：


![[assets/figures/papers/iclr26_0012_0elvad3gEu_Training-Free_Determination_of_Network_Width_via/figures/010_Figure_5.jpg]]
*Figure 5: Cardinal width is stable across training recipes (DNN on Diabetes). Test loss versus width for Adam (top) and SGD (bottom) with two learning rates/schedules and two initializations (He, NTK). All curves exhibit a sharp drop followed by a plateau beginning at widths ∼ 100, with only minor shifts in the cardinal width across recipes. Figure 6: Subsampling preserves the cardinal width. Computed $\mu _ { \mathrm { m i n } } \big ( K _ { m } ^ { ( 0 ) } \big$ ) versus width for DNNs. The curves are fits of g ( m ; $\vartheta$ ) and vertical dashed lines mark the estimated cardinal widths. The predicted cardinal widths are broadly stable under 10–50% subsampling, supporting a lowercost, training-free...

| 消融维度 | 测试配置 | 结论 |
|---------|---------|------|
| 优化器 | Adam vs SGD | 两种优化器下测试损失均在宽度 ∼100 处饱和，cardinal width 仅轻微偏移 |
| 学习率 | 默认学习率 vs 调整后的学习率 | 学习率变化未改变饱和宽度的基本位置 |
| 初始化 | He 初始化 vs NTK 参数化初始化 | 不同初始化方案下饱和趋势一致 |

所有曲线均呈现“先急剧下降、后在宽度 ∼100 处进入平台”的特征，cardinal width 在不同训练配方间保持稳定（置信度 0.95）。**但需注意**：在极端超参数（如极大学习率）下，cardinal width 可能发生偏移，这是方法的一个已知局限。

### 四、数据子采样的影响

全数据集的 NTK 最小特征值估计计算开销较大。Figure 6 验证了**子采样策略的可行性**：仅使用 10%–50% 的训练样本计算 $\mu_{\min}(K_m^{(0)})$ 并拟合饱和曲线，预测的 cardinal width 仍保持合理稳定性。这一发现为低成本部署提供了依据——用户可在小批量数据上运行算法，快速获得宽度建议，再在全数据上训练目标模型。


![[assets/figures/papers/iclr26_0012_0elvad3gEu_Training-Free_Determination_of_Network_Width_via/figures/006_Figure_6.jpg]]

### 五、理论假设的实证支撑

除了主结果，作者还在附件中验证了两个关键假设：

- **Assumption 3.5（相对谱稳定性）**：Figure 3 显示 $\mu_{\min}(K_m^{(0)})$、$\mu_{\min}(K_m^{(T)})$ 和 $\mu_{\min}(K_\infty)$ 均随宽度增加而上升并趋于饱和，且三者的谱比值保持有界（远离 0 和 ∞），支持了“初始化 NTK 的最小特征值与无限宽极限在谱意义上可比”的假设。

- **Assumption 3.6（NTK 变化随宽度衰减）**：Figure 4 展示了路径漂移 $\sup_u \|K_m^{(u)} - K_m^{(0)}\|$ 和初始化漂移 $\|K_m^{(0)} - K_\infty\|$ 均随宽度增大而减小，与 $\phi(m) \to 0$ 的假设一致。

这些实证支撑增强了 Theorem 3.8 的理论可信度，但也提示：**当网络未处于惰性训练状态（即特征学习显著）时，NTK 在训练中变化较大，$\phi(m)$ 的衰减可能不充分，此时 μ_min 的饱和点与测试损失平坦区的对齐需要额外验证**。

### 六、方法的已知局限

1. **分类任务缺乏理论保证**：虽然在 MNIST 上观察到对齐，但严格的理论分析仅覆盖回归场景。
2. **极端超参数下的偏移**：极大学习率等非标准配置可能导致 cardinal width 预测值偏离实际最优宽度。
3. **计算开销**：NTK 最小特征值的 LOBPCG 估计在全数据集上仍较昂贵，子采样虽可缓解，但可能引入估计方差。

以上局限在原文中均有明确讨论，用户在应用时需根据具体场景评估风险。

## 方法谱系与知识库定位

### 与现有宽度选择方法的对比

传统网络宽度选择依赖**试错式交叉验证**：对多个候选宽度分别完成完整训练，再根据测试性能人工判定最优宽度。这一范式存在两个根本性瓶颈：一是计算成本随候选宽度数量线性增长，二是缺乏理论指导，无法预判性能饱和点，导致盲目搜索。

本文提出的**基于 NTK 最小特征值的训练无关 cardinal width 选择**，在以下关键维度上实现了范式转变：

| 维度 | 传统交叉验证宽度搜索 | 本文方法 |
|------|---------------------|----------|
| **宽度选择准则** | 训练后根据测试性能人工判断，需多次训练 | 根据初始化 NTK 最小特征值 μ_min 的饱和点自动判定，无需训练 |
| **所需训练过程** | 需对多个候选宽度进行完整训练 | 仅在初始化时构建一次 NTK 并估计 μ_min，无需任何训练 |
| **理论依据** | 无，纯经验驱动 | 有：μ_min 控制泛化误差上界（Theorem 3.2/3.8） |

方法的核心因果链条可概括为：**μ_min（调节变量）→ 泛化误差上界（被控变量）→ 宽度饱和点（决策变量）**。具体而言，理论分析表明无限宽网络的测试误差上界由 μ_min^{-2} 主导（$E_g \leq C_1 \mu_{\min}^{-2} + C_2 \sigma^2 n \mu_{\min}^{-2}$），而有限宽网络在惰性训练下测试误差仍由初始化 NTK 的 μ_min 控制，并附加随宽度衰减的校正项（$E_g^{(m)} \leq \frac{C_4}{\mu_{\min}(K_m^{(0)})^2} + C_5 \frac{\phi(m)}{\mu_{\min}(K_m^{(0)})^2}$）。μ_min 随宽度增加而上升并趋于饱和，饱和点与测试损失平坦区对齐（Figure 2），因此可在训练前通过监测 μ_min 的饱和趋势确定 cardinal width。

### 方法适用边界

**已验证的适用范围：**
- **回归任务**：在 Diabetes、California Housing 等 UCI 数据集上，预测的 cardinal width 与测试损失饱和点高度一致（Figure 2）。
- **分类任务的初步拓展**：在 MNIST 和 XOR 上，预测的 cardinal width 处测试损失同样饱和（Figure 7），表明方法具备向分类任务延伸的潜力，但目前**尚无严格理论保证**。
- **多种架构**：方法在 DNN、CNN、ResNet 上均表现出一致性（Figure 2 底部两行）。
- **对训练超参数鲁棒**：cardinal width 对优化器（Adam/SGD）、学习率、初始化方案（He/NTK）不敏感（Figure 5），所有曲线在宽度约 100 处均呈现急剧下降后趋于平坦。
- **支持数据子采样**：仅使用 10-50% 的训练样本即可估计 cardinal width，且预测结果基本稳定（Figure 6），有效降低了 NTK 构建的计算开销。

**已知局限与失效模式：**

1. **理论覆盖范围受限**：严格证明仅针对回归任务给出，分类任务的延伸缺乏理论保证（原文明确承认"While the NTK can also be computed for classification problems...it lacks a theoretical guarantee at present"）。
2. **极端超参数下的偏移**：在极大学习率等极端设置下，cardinal width 可能发生偏移（原文指出"minor shifts in the cardinal width"）。
3. **计算开销**：NTK 最小特征值估计仍涉及较大的计算开销，尤其在完整数据集上构建 NTK 矩阵时。子采样是缓解手段，但需注意样本量过少时估计精度的退化。
4. **特征学习机制的适用性**：理论框架建立在惰性训练（lazy training）假设之上，尽管实验观察到在特征学习机制下 μ_min 饱和点仍与测试损失饱和对齐（原文 Section 4.2），但该现象尚无理论解释。

### 开放问题与后续方向

1. **特征学习机制的理论推广**：如何将 μ_min 控制泛化误差的理论框架从惰性训练推广到特征学习状态，建立深度非线性网络在非惰性条件下的严格泛化界？
2. **分类问题的理论奠基**：能否在分类问题中建立与回归问题类似的 μ_min 控制理论？这需要处理交叉熵损失下 NTK 谱与泛化误差之间的关系。
3. **结构维度的拓展**：cardinal width 概念是否可推广到网络深度、注意力头数、token 维度等其他结构维度？这需要建立对应结构参数与 NTK 谱之间的联系。
4. **高效特征值估计**：如何进一步降低大规模数据集上 NTK 最小特征值的估计成本，使其在实际应用中更具可操作性？

## 原文 PDF

![[paperPDFs/ICLR_2026/Training_Free_Determination_of_Network_Width_via_Neural_Tangent_Kernel.pdf]]
