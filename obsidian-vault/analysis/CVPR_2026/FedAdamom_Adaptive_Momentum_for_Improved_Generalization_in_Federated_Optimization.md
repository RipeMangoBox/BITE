---
title: "FedAdamom: Adaptive Momentum for Improved Generalization in Federated Optimization"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FedAdamom_Adaptive_Momentum_for_Improved_Generalization_in_Federated_Optimization.pdf
project_link: null
code_link: "https://github.com/Tenshawn/FedAdamom"
aliases:
- FedAdamom
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: "服务器端优化器的自适应对象：将自适应从学习率转移到动量超参数 $\\beta_1$，使动量参数 $\\beta_{1,t}$ 根据梯度二阶矩动态调整，既能利用动量快速逃离鞍点，又能保持与 SGD 一致的平坦极小值选择能力。"
primary_logic: "通过构造参数级自适应动量系数 $\\beta_{1,t} = (1 - v_t/\\bar{v}_t) \\cdot \\text{Clip}(0,1-\\epsilon)$，在联邦优化中同时实现：1）鞍点逃离速度与自适应方法相当（因动量漂移项 Hessian 无关）；2）平坦极小值选择与 FedAvg 一致（逃逸时间 $\\log(\\tau) = \\mathcal{O}(H_{ae}^{-1})$，而非 FedAdam 的 $\\mathcal{O}(H_{ae}^{-1/2})$），从而在收敛速度和泛化性能之间取得显著提升。"
claims:
- "FedAdamom 的设计核心是将自适应作用于动量而非学习率：设置 $\\beta_{1,t} = (1 - v_t/\\bar{v}_t) \\cdot \\text{Clip}(0,1-\\epsilon)$，并采用无分母的模型更新 $x_{t+1} = x_t + \\eta m_t$。"
- "扩散理论分析表明：FedAdam 的逃逸时间 $\\log(\\tau_{FedAdam}) = \\mathcal{O}(H_{ae}^{-1/2})$，而 FedAvg、FedAvgM 和 FedAdamom 均为 $\\log(\\tau) = \\mathcal{O}(H_{ae}^{-1})$，说明自适应学习率破坏了平坦极小值的选择，而 FedAdamom..."
- 在 CIFAR-10/100 和 Tiny-ImageNet 上（100 客户端、5% 参与、Dir(0.3)），FedAdamom 达到的最佳准确率（88.93%, 57.58%, 47.38%）显著优于 FedAdam 及其他基线。
- 损失景观可视化显示 FedAdamom 收敛到比 FedAdam 和 FedAvgM 更平坦的极小值，验证了平坦极小值选择理论。
---

# FedAdamom: Adaptive Momentum for Improved Generalization in Federated Optimization

> [!tip] 核心洞察
> 通过构造参数级自适应动量系数 $\beta_{1,t} = (1 - v_t/\bar{v}_t) \cdot \text{Clip}(0,1-\epsilon)$，在联邦优化中同时实现：1）鞍点逃离速度与自适应方法相当（因动量漂移项 Hessian 无关）；2）平坦极小值选择与 FedAvg 一致（逃逸时间 $\log(\tau) = \mathcal{O}(H_{ae}^{-1})$，而非 FedAdam 的 $\mathcal{O}(H_{ae}^{-1/2})$），从而在收敛速度和泛化性能之间取得显著提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | FedAdamom：自适应动量提升联邦优化泛化能力 |
| 英文题名 | FedAdamom: Adaptive Momentum for Improved Generalization in Federated Optimization |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Hou_FedAdamom_Adaptive_Momentum_for_Improved_Generalization_in_Federated_Optimization_CVPR_2026_paper.html) · [Code](https://github.com/Tenshawn/FedAdamom) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FedAdamom |
| Dataset | CIFAR-10 (100 clients, 5% participation, Dir(0.3), 1000 rounds), CIFAR-100 (100 clients, 5% participation, Dir(0.3), 1000 rounds), Tiny-ImageNet (100 clients, 5% participation, Dir(0.3), 1000 rounds), FEMNIST |

> [!tip] 效果简介
> - CIFAR-10 (100 clients, 5% participation, Dir(0.3), 1000 rounds) 上，Accuracy (%) 88.93 vs FedAdam (best baseline) (显著优于 FedAdam)。
> - CIFAR-100 (100 clients, 5% participation, Dir(0.3), 1000 rounds) 上，Accuracy (%) 57.58 vs FedAdam (best baseline) (显著优于 FedAdam)。
> - Tiny-ImageNet (100 clients, 5% participation, Dir(0.3), 1000 rounds) 上，Accuracy (%) 47.38 vs FedAdam (best baseline) (显著优于 FedAdam)。

## 概述

在联邦学习中，数据异构性是制约模型泛化性能的核心瓶颈。当客户端数据分布高度非独立同分布（non-i.i.d.）时，以 **FedAdam**（Reddi et al., ICLR 2021）为代表的自适应优化器虽然凭借自适应学习率加速了收敛，但其机制——通过梯度二阶矩的平方根倒数缩放更新步长——会系统性地削弱算法对平坦极小值的偏好，使模型倾向于收敛到更尖锐的极小值，从而损害泛化能力。数据异构程度越高，这一效应越显著。

本文提出 **FedAdamom**，一种新的自适应联邦优化算法，其核心设计思想是将自适应的对象从学习率转移到动量超参数上。具体而言，FedAdamom 构造了参数级自适应动量系数 $\beta_{1,t} = (1 - v_t/\bar{v}_t) \cdot \text{Clip}(0,1-\epsilon)$，并采用无分母的标准动量 SGD 形式进行全局模型更新。这一设计在保持自适应方法快速逃离鞍点能力的同时，恢复了对平坦极小值的偏好，从根本上解决了 FedAdam 泛化性不足的问题。

从扩散理论角度，论文严格证明了：FedAdam 的平均逃逸时间与 Hessian 特征值的关系为 $\log(\tau_{\text{FedAdam}}) = \mathcal{O}(H_{ae}^{-1/2})$，而 FedAvg、FedAvgM 和 FedAdamom 均为 $\log(\tau) = \mathcal{O}(H_{ae}^{-1})$。这意味着 FedAdamom 成功消除了自适应学习率对极小值选择的负面影响，在收敛速度与泛化性能之间取得了显著提升。

实验验证了理论分析的有效性。在 CIFAR-10/100 和 Tiny-ImageNet 上（100 客户端、5% 参与率、Dir(0.3) 数据划分），FedAdamom 分别达到 **88.93%**、**57.58%** 和 **47.38%** 的准确率，显著优于 FedAdam 及其他基线方法。在 FEMNIST、CelebA 和 Shakespeare 等真实联邦数据集上，FedAdamom 同样保持了领先优势。损失景观可视化和逃逸速率实验进一步证实，FedAdamom 收敛到的极小值比 FedAdam 和 FedAvgM 更平坦，且其对数逃逸时间与尖锐度的关系符合 $\mathcal{O}(k^{-1})$ 的理论预测。

## 背景与动机

联邦学习在数据异构场景下，服务器端优化器的选择对模型泛化性能具有决定性影响。以 **FedAvg**（McMahan et al., AISTATS 2017）为代表的经典方法在服务器端执行 SGD 更新，能够稳定收敛到平坦极小值，从而获得良好的泛化能力。为加速收敛，**FedAdam**（Reddi et al., ICLR 2021）等自适应优化方法被引入联邦学习框架，通过在服务器端引入自适应学习率机制（利用梯度二阶矩 $v_t$ 调整步长，即 $\eta \cdot m_t / (\sqrt{v_t}+\epsilon)$）显著提升了收敛速度。

然而，自适应学习率机制在加速收敛的同时引入了一个被忽视的代价：它削弱了算法对平坦极小值的偏好。如 Figure 1 所示，在数据异构程度较高（Dirichlet 分布参数 $\alpha$ 较小）的条件下，FedAdam 倾向于收敛到比 FedAvg 更尖锐的极小值，导致泛化性能下降。这一现象的扩散理论分析揭示，FedAdam 从尖锐极小值逃逸到平坦极小值的平均逃逸时间满足 $\log(\tau_{FedAdam}) = \mathcal{O}(H_{ae}^{-1/2})$，而 FedAvg 的逃逸时间为 $\log(\tau_{FedAvg}) = \mathcal{O}(H_{ae}^{-1})$。自适应学习率分母中的 $1/\sqrt{v_t}$ 项改变了鞍点附近的扩散动力学，使得逃逸时间对 Hessian 特征值 $H_{ae}$ 的依赖从线性减弱为平方根关系，从而破坏了平坦极小值选择能力。

这一瓶颈的因果机制在于：自适应优化器的自适应对象是学习率，而学习率的自适应缩放直接干预了参数在损失景观中的扩散行为。一个自然的替代思路是将自适应从学习率转移到动量超参数上——动量本身不影响极小值选择（FedAvgM 的逃逸时间同样为 $\mathcal{O}(H_{ae}^{-1})$），但能有效加速鞍点逃离。基于这一洞察，本文提出 **FedAdamom**，通过构造参数级自适应动量系数 $\beta_{1,t} = (1 - v_t/\bar{v}_t) \cdot \text{Clip}(0,1-\epsilon)$，在保持与 FedAvg 一致的平坦极小值选择能力的同时，获得与自适应方法相当的收敛速度。

## 核心创新

### 问题瓶颈：自适应学习率损害联邦泛化

在数据异构的联邦学习中，FedAdam 等自适应优化器通过梯度二阶矩 $v_t$ 动态调整学习率（即 $\eta \cdot m_t / (\sqrt{v_t}+\epsilon)$），在收敛速度上具有显著优势。然而，这种自适应学习率机制引入了一个被忽视的副作用：它削弱了算法对**平坦极小值**的偏好，导致模型收敛到更尖锐的极小值，从而损害泛化性能。该效应在数据异构程度高（如 Dir(0.3) 甚至更低 $\alpha$ 值）时尤为明显（Figure 1 提供了不同异构程度下的损失景观对比）。

扩散理论分析揭示了这一现象的本质原因：在鞍点附近，FedAdam 的平均逃逸时间满足 $\log(\tau_{FedAdam}) = \mathcal{O}(H_{ae}^{-1/2})$，而 FedAvg 则为 $\log(\tau_{FedAvg}) = \mathcal{O}(H_{ae}^{-1})$。这意味着 FedAdam 对 Hessian 特征值 $H_{ae}$ 的敏感度降低，从而无法有效区分尖锐极小值与平坦极小值，丧失了泛化优势。

### 核心洞察：将自适应从学习率迁移到动量

FedAdamom 的核心设计理念是**改变自适应的作用对象**：将自适应机制从学习率转移到动量超参数 $\beta_1$ 上。这一设计基于一个关键观察——动量漂移项与 Hessian 无关，因此对动量系数进行自适应调整不会破坏平坦极小值的选择能力，同时仍能利用动量机制实现快速的鞍点逃离。

具体而言，FedAdamom 将动量系数从固定标量（通常为 0.9）升级为**参数级自适应向量**：

$$\beta_{1,t} = \left(1 - \frac{v_t}{\bar{v}_t}\right) \cdot \text{Clip}(0, 1-\epsilon)$$

其中 $v_t$ 为梯度二阶矩的指数移动平均，$\bar{v}_t$ 为 $v_t$ 的移动平均。该设计使得每个参数的动量系数根据其梯度二阶矩的相对大小动态调整：当某参数梯度方差较大时，$\beta_{1,t}$ 减小，算法更依赖当前梯度信号；反之则增大，保留更多历史动量信息。

### 关键改变槽位

与现有自适应联邦优化方法相比，FedAdamom 在以下三个核心槽位上做出了根本性改变：

| 槽位 | 基线方法（FedAdam 等） | FedAdamom |
|------|----------------------|-----------|
| **自适应机制** | 自适应学习率（利用 $v_t$ 缩放步长） | 自适应动量系数 $\beta_{1,t}$ |
| **$\beta_1$ 参数** | 固定标量（通常 0.9） | 参数级自适应向量 $\beta_{1,t}$ |
| **模型更新公式** | $x_{t+1} = x_t + \eta \frac{m_t}{\sqrt{v_t}+\epsilon}$ | $x_{t+1} = x_t + \eta \cdot m_t$（无分母） |

最关键的改变在于**模型更新公式**：FedAdamom 采用标准动量 SGD 形式 $x_{t+1} = x_t + \eta m_t$，完全移除了分母中的 $\sqrt{v_t}$ 项。这使得算法的扩散行为回归到与 FedAvg 一致的动力学特征，从而恢复了平坦极小值选择能力。理论分析证实，FedAdamom 的平均逃逸时间为 $\log(\tau_{FedAdamom}) = \mathcal{O}(H_{ae}^{-1})$，与 FedAvg 和 FedAvgM 一致，而与 FedAdam 的 $\mathcal{O}(H_{ae}^{-1/2})$ 形成本质区别。

### 理论保障

FedAdamom 的设计在理论上获得了双重保障：

1. **平坦极小值选择**（Theorem 4）：通过将自适应作用于动量而非学习率，FedAdamom 的逃逸时间缩放律恢复为 $\mathcal{O}(H_{ae}^{-1})$，从理论上保证了算法对平坦极小值的偏好。

2. **收敛性保证**（Convergence Theorem）：在非凸联邦学习设定下，FedAdamom 的收敛上界为 $\mathcal{O}\left(\frac{L\Theta_0}{\sqrt{sKT}} + \frac{\beta_{1,max}}{1-\beta_{1,max}}\left(\frac{\sigma_l^2}{KT} + \frac{\sigma_g^2}{T} + \Psi\right)\right)$，与已知自适应联邦方法的收敛率相匹配，未因改变自适应对象而牺牲收敛速度。

这种"收敛速度与泛化性能兼得"的特性，使得 FedAdamom 在保持自适应方法快速收敛优势的同时，显著提升了模型的泛化能力。

## 整体框架

FedAdamom 遵循标准联邦优化（FEDOPT）框架，其核心创新在于将服务器端的自适应机制从**学习率**迁移至**动量系数**，从而在保持快速收敛的同时恢复平坦极小值偏好。整体流程分为三个顺序模块：

### 模块一：客户端本地训练

每轮通信中，服务器随机采样 $s$ 个客户端构成子集 $\mathcal{S}_t$，并将当前全局模型 $x_t$ 分发至各选中客户端。每个客户端 $i \in \mathcal{S}_t$ 在本地私有数据上执行 $K$ 步 SGD 更新，得到本地模型 $x_{t,K}^i$：

$$x_{t,k+1}^i = x_{t,k}^i - \eta_l \nabla F_i(x_{t,k}^i; \xi_{t,k}^i), \quad k = 0, 1, \dots, K-1$$

其中 $\eta_l$ 为客户端学习率，$\xi_{t,k}^i$ 为本地采样的小批量数据。该模块与 FedAvg、FedAdam 等基线方法完全一致，保证客户端计算开销无差异。

### 模块二：服务器伪梯度聚合

服务器收集所有选中客户端返回的本地模型，计算**伪梯度**（pseudo-gradient）$\Delta_t$，作为全局优化器的输入信号：

$$\Delta_t = \frac{1}{s} \sum_{i \in \mathcal{S}_t} \left( x_t - x_{t,K}^i \right)$$

该伪梯度本质上是客户端本地更新累积方向的聚合表示，其统计特性（噪声协方差结构）直接决定了后续扩散动力学行为。在数据异构场景下，$\Delta_t$ 的方差增大，导致不同优化器对极小值尖锐度的选择出现显著分化。

### 模块三：FedAdamom 服务器全局更新

这是 FedAdamom 区别于所有现有自适应联邦方法的关键模块。服务器维护两组全局状态变量：

- **一阶动量** $m_t$：累积伪梯度的指数移动平均
- **二阶矩** $v_t$：伪梯度平方的指数移动平均，及其长期均值 $\bar{v}_t$

具体更新流程（Algorithm 1）如下：

1. **二阶矩更新**（与 FedAdam 一致）：
   $$v_t = \beta_2 v_{t-1} + (1-\beta_2) \Delta_t^2$$
   $$\bar{v}_t = \beta_2 \bar{v}_{t-1} + (1-\beta_2) v_t$$

2. **自适应动量系数计算**（核心创新）：
   $$\beta_{1,t} = \left( 1 - \frac{v_t}{\bar{v}_t} \right) \cdot \text{Clip}(0, 1-\epsilon)$$
   该参数级向量根据当前梯度二阶矩与历史均值的比值动态调整：当某参数维度梯度波动剧烈（$v_t$ 相对 $\bar{v}_t$ 较大）时，$\beta_{1,t}$ 减小，降低历史动量权重以增强对新梯度的响应；反之则增大动量权重以加速收敛。

3. **动量更新**：
   $$m_t = \beta_{1,t} \odot m_{t-1} + (1-\beta_{1,t}) \odot \Delta_t$$
   其中 $\odot$ 表示逐元素乘积。

4. **全局模型更新**（无分母的标准动量 SGD 形式）：
   $$x_{t+1} = x_t + \eta \cdot m_t$$

### 设计逻辑与因果链

上述框架的设计围绕一个核心因果瓶颈展开：**FedAdam 的自适应学习率（$1/\sqrt{v_t}$ 分母项）破坏了平坦极小值选择能力**。理论分析表明，在鞍点附近，FedAdam 的均方位移包含与 Hessian 特征值平方根相关的扩散项，导致逃逸时间 $\log(\tau_{\text{FedAdam}}) = \mathcal{O}(H_{ae}^{-1/2})$，削弱了对尖锐极小值的逃离倾向。相比之下，FedAvg 和 FedAvgM 的逃逸时间为 $\mathcal{O}(H_{ae}^{-1})$，天然偏好平坦极小值。

FedAdamom 通过将自适应从分母（学习率缩放）移至分子（动量系数），实现了**自适应性与平坦极小值偏好的解耦**：
- 自适应动量 $\beta_{1,t}$ 提供与 FedAdam 相当的鞍点逃离速度（动量漂移项与 Hessian 无关）
- 模型更新 $x_{t+1} = x_t + \eta m_t$ 保持标准动量 SGD 形式，逃逸时间恢复为 $\mathcal{O}(H_{ae}^{-1})$（Theorem 4），与 FedAvg 一致

这一设计使得 FedAdamom 在收敛速度上匹配自适应方法，在泛化性能上匹配 FedAvg，实现了两者长期以来被认为不可兼得的权衡突破。

## 核心模块与公式推导

### 问题建模：联邦优化框架

联邦学习的全局优化目标为最小化所有 $n$ 个客户端的平均损失：

$$\operatorname* { m i n } _ { x } \left\{ { \frac { 1 } { n } } \sum _ { i = 1 } ^ { n } F _ { i } ( x ) \right\}$$

在通用联邦优化框架 FEDOPT 下，服务器端通过聚合客户端本地更新构造伪梯度，并应用全局优化器进行模型更新：

$$\left\{ \begin{array} { l l } \Delta _ { t } = \frac { 1 } { s } \sum _ { i \in \mathcal { S } _ { t } } \left( x _ { t } - x _ { t , K } ^ { i } \right) , \\ x _ { t + 1 } = x _ { t } - \mathrm { G L O B A L O P T } ( x _ { t } , \Delta _ { t } , \eta ) , \end{array} \right.$$

其中 $\Delta_t$ 为第 $t$ 轮通信的伪梯度，$s$ 为选中客户端数量，$x_{t,K}^i$ 为客户端 $i$ 执行 $K$ 步本地 SGD 后的模型，$\eta$ 为服务器端学习率。

### 关键模块一：扩散动力学分析框架

为分析不同优化器在联邦学习中极小值选择的本质差异，论文采用基于朗之万方程的扩散理论框架。SGD 在临界点附近的连续时间近似由以下朗之万方程描述：

$$d x = - \nabla f ( x ) d t + [ \eta C ( x ) ] ^ { \frac { 1 } { 2 } } d W _ { t }$$

其中 $C(x)$ 为梯度噪声协方差矩阵，$dW_t$ 为标准维纳过程。参数概率密度 $P(x,t)$ 的演化遵循福克-普朗克方程：

$$\frac { \partial P ( x , t ) } { \partial t } = \nabla \cdot [ P ( x , t ) \nabla f ( x ) ] + \nabla \cdot \nabla D ( x ) P ( x , t )$$

其中 $D(x) = \eta C(x)/2$ 为扩散矩阵。该框架将优化过程建模为噪声驱动的扩散过程，使极小值间的逃逸时间可解析计算。

### 关键模块二：自适应动量机制（核心创新）

FedAdamom 的核心设计理念是将自适应从学习率转移到动量超参数。具体而言，算法维护梯度二阶矩的指数移动平均 $v_t$ 及其长期平均 $\bar{v}_t$，据此构造参数级自适应动量系数：

$$\beta _ { 1 , t } = \left( 1 - \frac { v _ { t } } { \bar { v } _ { t } } \right) \cdot \mathrm { C l i p } ( 0 , 1 - \epsilon )$$

其中 $v_t = \beta_2 v_{t-1} + (1-\beta_2)\Delta_t^2$，$\bar{v}_t$ 为 $v_t$ 的移动平均，$\epsilon$ 为防止 $\beta_1$ 达到 1 的小常数。该设计的直觉是：当梯度分量波动较大（$v_t$ 大）时，降低动量系数以减弱历史梯度的影响；当梯度分量稳定时，增大动量系数以加速收敛。

基于此自适应动量系数，FedAdamom 的服务器端更新采用无分母的标准动量 SGD 形式：

$$m_t = \beta_{1,t} m_{t-1} + (1-\beta_{1,t})\Delta_t, \quad x_{t+1} = x_t + \eta m_t$$

与 FedAdam 的更新公式对比，关键差异在于取消了分母 $\sqrt{v_t}$ 的自适应学习率缩放：

$$\text{FedAdam: } x_{t+1} = x_t + \eta \frac{m_t}{\sqrt{v_t} + \epsilon}$$

### 关键公式：逃逸时间对比

扩散理论分析揭示了不同优化器在尖锐极小值 $a$ 与平坦极小值 $d$ 之间通过鞍点 $b$ 逃逸的平均时间差异，这是理解泛化性能差异的核心。

**FedAvg 的平均逃逸时间**（Theorem 1）：

$$\log ( \tau _ { F e d A v g } ) = \mathcal { O } \left( \frac { 2 B \Delta f } { \eta \eta _ { l } H _ { a e } } \right)$$

其中 $B$ 为本地批量大小，$\Delta f$ 为极小值间势垒高度，$\eta_l$ 为客户端学习率，$H_{ae}$ 为尖锐极小值 $a$ 方向上的 Hessian 特征值。逃逸时间与 $H_{ae}^{-1}$ 成正比，意味着尖锐极小值更难逃离，因此算法偏好平坦极小值。

**FedAvgM 的平均逃逸时间**（Theorem 2）：

$$\log \left( \tau _ { F e d A v g M } \right) = \mathcal { O } \left( \frac { 2 ( 1 - \beta ) B \Delta f } { \eta \eta _ { l } H _ { a e } } \right)$$

固定动量仅引入常数因子 $(1-\beta)$ 缩放逃逸时间，不改变对 $H_{ae}^{-1}$ 的依赖关系，因此不破坏平坦极小值选择。

**FedAdam 的平均逃逸时间**（Theorem 3）：

$$\log ( \tau _ { F e d A d a m } ) = \mathcal { O } \left( \frac { 2 \sqrt { B } \Delta f } { \eta \eta _ { l } \sqrt { H _ { a e } } } \right)$$

自适应学习率的分母 $\sqrt{v_t}$ 改变了扩散过程的噪声结构，使逃逸时间仅依赖 $H_{ae}^{-1/2}$。这意味着对尖锐极小值的逃离惩罚减弱，算法不再强烈偏好平坦极小值——这是 FedAdam 泛化性能下降的根本原因。

**FedAdamom 的平均逃逸时间**（Theorem 4）：

$$\log( \tau _ { F e d A d a m o m }) = \mathcal { O } \left( \frac { 2 B \Delta f } { \eta \eta _ { l } H _ { a e } } \right)$$

由于 FedAdamom 取消了分母自适应，更新公式退化为标准动量 SGD 形式，其扩散行为与 FedAvg 一致，逃逸时间恢复为 $\mathcal{O}(H_{ae}^{-1})$。这意味着 FedAdamom 同时保留了动量加速鞍点逃离的能力和平坦极小值选择特性。

### 收敛性保证

FedAdamom 在非凸联邦学习中的收敛上界为：

$$\frac{1}{T}\sum_{t=0}^{T-1}\mathbb{E}\|\nabla f(x_t)\|^2 \leq \mathcal{O}\left(\frac{L\Theta_0}{\sqrt{sKT}} + \frac{\beta_{1,max}}{1-\beta_{1,max}}\left(\frac{\sigma_l^2}{KT} + \frac{\sigma_g^2}{T} + \Psi\right)\right)$$

其中 $\Theta_0 = f(x_0) - f^*$ 为初始最优间隙，$L$ 为光滑性常数，$\sigma_l^2$ 和 $\sigma_g^2$ 分别为本地和全局梯度方差，$\beta_{1,max}$ 为自适应动量系数的上界，$\Psi$ 为与数据异构相关的项。该收敛率与已知自适应联邦方法匹配，证明自适应动量机制不损害理论收敛速度。

## 实验与分析

### 核心瓶颈验证：自适应学习率如何损害泛化

FedAdamom 的理论起点是一个被忽视的现象：在数据异构的联邦学习中，FedAdam 等自适应优化器虽然通过自适应学习率加速收敛，但其 $1/\sqrt{v_t}$ 项削弱了算法对平坦极小值的偏好，导致模型向更尖锐的极小值收敛。Figure 1 直观展示了这一效应——随着数据异构程度增加（Dirichlet 参数 $\alpha$ 减小），FedAdam 倾向于收敛到比 FedAvg 更尖锐的极小值，验证了自适应学习率机制与平坦极小值选择之间的内在冲突。

![[assets/figures/papers/paper_list_l2123_https_openaccess_thecvf_com_content_CVPR2026_html_Hou_FedAdamom_Adaptive/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of FedAvg(net) and FedAdam(solid) loss landscapes with varying degrees of data heterogeneity (α) on the CIFAR-10 datasets. The effectiveness of FedAdam and FedAvg in converging to global flat minima is highly influenced by data heterogeneity, with higher heterogeneity (α ↓) leading to convergence toward sharper minima. This highlights the importance of optimizing global sharpness. Model: CNN*

### 主要实验结果

**中等规模联邦学习**（100 客户端，5% 参与率，Dir(0.3)，1000 轮通信）的结果汇总于 Table 1。FedAdamom 在三个标准基准上均取得最优准确率：
- **CIFAR-10**：88.93%，显著优于 FedAdam 及其他基线方法；
- **CIFAR-100**：57.58%，同样领先于所有对比方法；
- **Tiny-ImageNet**：47.38%，在更具挑战性的细粒度分类任务上保持优势。

这些提升源于自适应动量参数的设计：通过将自适应从学习率转移到动量系数 $\beta_{1,t}$，FedAdamom 在保持鞍点逃离速度的同时，恢复了对平坦极小值的偏好。

**真实联邦数据集**（Table 3）进一步验证了方法的鲁棒性：
- **FEMNIST**（特征偏斜）：82.85%，显著优于 FedAdam；
- **CelebA**（数据不平衡）：89.95%；
- **Shakespeare**（下一词预测）：48.02%。

三个场景分别涵盖特征偏斜、标签不平衡和语言建模，表明 FedAdamom 的自适应动量机制在不同数据异质性模式下均有效。

### 平坦极小值选择的实验验证

Figure 2 提供了损失景观可视化的直接证据：在 CIFAR-10 上，FedAdamom 收敛到比 FedAdam 和 FedAvgM 更平坦的极小值，且损失值更低。这与理论预测一致——FedAdamom 的逃逸时间满足 $\log(\tau) = \mathcal{O}(H_{ae}^{-1})$，与 FedAvg 和 FedAvgM 相同，而 FedAdam 的逃逸时间为 $\mathcal{O}(H_{ae}^{-1/2})$。

![[assets/figures/papers/paper_list_l2123_https_openaccess_thecvf_com_content_CVPR2026_html_Hou_FedAdamom_Adaptive/figures/007_Figure_2.jpg]]
*Figure 2: Loss landscapes of models trained with FedAdamom (net) vs. FedAdam and FedAvgM (solid) on CIFAR10. FedAdamom achieves flatter minima and lower loss values w.r.t. FedAdam and FedAvgM*

Figure 3 通过受控实验量化验证了这一关系：实验构造不同尖锐度缩放因子 $k$ 的极小值，测量算法从尖锐极小值逃逸到平坦极小值的平均时间。结果显示，FedAdamom 和 FedAvgM 的对数逃逸时间 $-\log(\Gamma)$ 与 $k^{-1}$ 呈线性关系，而 FedAdam 更符合 $k^{-1/2}$ 的标度律。这直接证实了自适应学习率（分母项）是破坏平坦极小值选择的因果机制，而 FedAdamom 通过将自适应作用于动量成功规避了这一问题。

![[assets/figures/papers/paper_list_l2123_https_openaccess_thecvf_com_content_CVPR2026_html_Hou_FedAdamom_Adaptive/figures/008_Figure_3.jpg]]
*Figure 3: Flat Minima Selection: The log-scale mean escape time − log(Γ) with the 95% confidence interval is displayed. We empirically verify that FedAdamom and FedAvgM satisfy*

### 超参数敏感性分析

Table 2 展示了 FedAdamom 对 $\beta_2$（二阶矩衰减系数）的敏感性。在 $\beta_2 \in [0.01, 0.3]$ 范围内，算法性能保持稳定：
- Dir(0.3) 设置下，最佳准确率 88.93% 出现在 $\beta_2=0.05$；
- i.i.d. 设置下，最佳准确率 91.83% 同样出现在 $\beta_2=0.05$。

较宽的稳定区间表明，自适应动量系数 $\beta_{1,t} = (1 - v_t/\bar{v}_t) \cdot \text{Clip}(0,1-\epsilon)$ 的设计对二阶矩估计的精确值不敏感，降低了实际部署中的调参负担。

### 公平性保障

所有对比实验遵循一致的公平性准则：
- 客户端本地优化器统一使用 SGD，保证局部计算量与通信代价一致；
- 超参数按各方法原始论文或官方代码设置，并在相同范围内调优；
- 数据划分、随机种子和参与率设置完全一致。

### 已知局限与待验证场景

尽管实验结果全面，以下方面仍需注意：
- 理论分析基于准平衡假设和低温近似，在梯度噪声极高或数据极度异构（如 Dir(0.05)）时，理论预测可能存在偏差，需进一步实验验证；
- 当前实验覆盖图像分类和文本下一词预测，尚未在语音识别、推荐系统等联邦学习典型应用上验证；
- FedAdamom 在结合客户端差分隐私、梯度压缩或异步更新等实用约束下的表现仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l2123_https_openaccess_thecvf_com_content_CVPR2026_html_Hou_FedAdamom_Adaptive/figures/002_Table_1.jpg]]
*Table 1: Moderate-scale: 100 clients, 5% participation*

![[assets/figures/papers/paper_list_l2123_https_openaccess_thecvf_com_content_CVPR2026_html_Hou_FedAdamom_Adaptive/figures/009_Table_3.jpg]]
*Table 3: Results on the realistic datasets involving feature skewness and data imbalance between clients*

## 方法谱系与知识库定位

### 方法谱系：从 FedAvg 到 FedAdamom 的演化逻辑

FedAdamom 的核心贡献在于重新定义了联邦优化中“自适应”的施加对象。理解这一贡献需要梳理从基础联邦平均到自适应联邦优化的技术演进。

**FedAvg** (McMahan et al., AISTATS 2017) 奠定了联邦学习的标准范式：客户端本地执行多步 SGD，服务器端对收集的模型更新进行加权平均。Reddi et al. (ICLR 2021) 在 **FedOpt** 框架下证明，FedAvg 等价于在服务器端执行 SGD，其伪梯度为 $\Delta_t = \frac{1}{s}\sum_{i\in\mathcal{S}_t}(x_t - x_{t,K}^i)$。这一等价性使得服务器端优化器的选择成为影响联邦学习性能的关键设计维度。

**FedAvgM** (Hsu et al., arXiv 2019) 在服务器端引入固定动量：

$$
m_t = \beta m_{t-1} + \Delta_t, \quad x_{t+1} = x_t + \eta m_t
$$

其中 $\beta$ 为固定标量（通常取 0.9）。动量加速了鞍点逃离，但不改变极小值选择偏好——FedAvgM 与 FedAvg 的逃逸时间均满足 $\log(\tau) = \mathcal{O}(H_{ae}^{-1})$，即两者都偏好平坦极小值。

**FedAdam** (Reddi et al., ICLR 2021) 将 Adam 的自适应机制引入服务器端，同时维护动量 $m_t$ 和二阶矩 $v_t$：

$$
m_t = \beta_1 m_{t-1} + (1-\beta_1)\Delta_t, \quad v_t = \beta_2 v_{t-1} + (1-\beta_2)\Delta_t^2
$$

$$
x_{t+1} = x_t + \eta \frac{m_t}{\sqrt{v_t}+\epsilon}
$$

自适应学习率 $1/\sqrt{v_t}$ 在梯度方向不一致时缩小步长、一致时放大步长，显著加速收敛。然而，本文的扩散理论分析揭示了其代价：FedAdam 的逃逸时间变为 $\log(\tau_{FedAdam}) = \mathcal{O}(H_{ae}^{-1/2})$，对 Hessian 特征值的依赖从线性降为平方根，削弱了对平坦极小值的偏好。Figure 1 直观展示了这一效应——在数据异构程度高（$\alpha$ 小）时，FedAdam 倾向于收敛到更尖锐的极小值。

**FedAdamom** 的突破在于将自适应从“学习率”转移到“动量系数”上。其关键设计是将 $v_t$ 的信息用于动态调整 $\beta_{1,t}$ 而非缩放步长：

$$
\beta_{1,t} = \left(1 - \frac{v_t}{\bar{v}_t}\right) \cdot \text{Clip}(0, 1-\epsilon)
$$

模型更新退化为标准动量 SGD 形式 $x_{t+1} = x_t + \eta m_t$，不含分母项。这一设计同时保留了两方面优势：
- **鞍点逃离速度**：动量漂移项与 Hessian 无关，逃离速度与自适应方法相当；
- **平坦极小值选择**：逃逸时间恢复为 $\log(\tau_{FedAdamom}) = \mathcal{O}(H_{ae}^{-1})$，与 FedAvg/FedAvgM 一致。

### 与其他自适应联邦方法的横向对比

在自适应联邦学习的更广谱系中，FedAdamom 占据了一个独特位置。**FAFED** (Wu et al., AAAI 2023) 通过动量方差缩减提升自适应效率，**FADAS** (Wang et al., ICML 2024) 面向异步场景设计自适应优化，**FedCAda** (Zhou et al., ICASSP 2025) 将自适应置于客户端侧，**Mime** (Karimireddy et al., NeurIPS 2021) 则通过控制变量与服务器优化器状态的结合来缓解客户端漂移。这些方法均未触及 FedAdamom 的核心洞察——自适应学习率本身是泛化性能的瓶颈，而自适应动量可以在不牺牲收敛速度的前提下恢复平坦极小值偏好。

### 适用边界与局限

FedAdamom 的理论分析基于准平衡假设和低温近似，其适用边界受以下因素制约：

1. **梯度噪声假设**：扩散理论分析假设梯度噪声服从高斯分布，在梯度噪声极高或分布严重偏离高斯的场景（如极小批量、强非 i.i.d.）下，理论预测可能存在偏差。论文未在 Dir(0.05) 等极度异构条件下验证平坦极小值选择优势是否始终成立。

2. **服务器端内存开销**：自适应动量计算需维护全局二阶矩 $v_t$ 及其移动平均 $\bar{v}_t$，服务器内存开销与原 FedAdam 相比增量可忽略，但与 FedAvg/FedAvgM 相比有所增加。在模型规模极大（如大语言模型联邦微调）的场景下，这一开销需纳入考量。

3. **任务覆盖范围**：实验验证主要覆盖图像分类（CIFAR-10/100、Tiny-ImageNet、FEMNIST、CelebA）和文本下一词预测（Shakespeare），未在语音识别、推荐系统、医疗影像等联邦学习典型应用上验证泛化能力。

4. **实用约束下的性能未知**：论文未探讨 FedAdamom 在结合客户端差分隐私、梯度压缩、安全聚合或异步更新等实用约束下的性能表现。这些约束可能改变梯度噪声结构，进而影响自适应动量的行为。

### 开放问题

1. **自适应动量机制的推广性**：FedAdamom 的自适应动量设计能否推广到其他自适应优化器（如 AMSGrad、Adan、LAMB）的联邦版本？AMSGrad 通过修正二阶矩估计的非单调性来稳定训练，将其与自适应动量结合可能进一步提升性能。

2. **极端非 i.i.d. 下的失效模式**：在 Dir(0.05) 等极度异构场景下，客户端伪梯度的方差急剧增大，$v_t/\bar{v}_t$ 的估计可能变得不稳定。FedAdamom 的平坦极小值选择优势是否始终成立，是否存在新的失效模式，需进一步研究。

3. **端到端联合自适应**：当前 FedAdamom 仅在服务器端施加自适应动量，客户端仍使用标准 SGD。如何将其与客户端自适应优化（如 FedCAda）结合，实现服务器动量自适应与客户端学习率自适应的协同，是值得探索的方向。

4. **异步与掉线鲁棒性**：在客户端频繁掉线或异步通信的联邦环境中，服务器端 $v_t$ 的估计可能因陈旧更新而产生偏差。如何设计稳健的 $v_t$ 更新机制，或引入衰减因子来降低陈旧更新的影响，是实际部署中需要解决的问题。

5. **通信效率的进一步优化**：自适应动量带来的额外稳定性是否允许更大的本地更新步数 $K$，从而进一步降低通信轮次？这需要在收敛性理论与通信-计算权衡中进行更深入的分析。

## 原文 PDF

![[paperPDFs/CVPR_2026/FedAdamom_Adaptive_Momentum_for_Improved_Generalization_in_Federated_Optimization.pdf]]
