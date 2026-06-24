---
title: "On the Convergence of Two-Layer Kolmogorov-Arnold Networks with First-Layer Training"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/On_the_Convergence_of_Two_Layer_Kolmogorov_Arnold_Networks_with_First_Layer_Training.pdf
aliases:
- KAFLTTLK
- CTLKANFLT
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "仅训练第一层系数并固定第二层，同时增大隐藏层宽度m，可简化分析并确保收敛。"
primary_logic: "在足够宽且使用RBF基函数的两层KAN中，梯度下降训练第一层参数会线性收敛到零训练误差，收敛速度由标签向量在KAN正切核（KAN‑TK）特征谱上的投影决定，且所需宽度 m=O(n²) 显著优于传统ReLU网络的 O(n⁶)。"
claims:
- "Theorem 4.2 证明在过参数化条件下，仅训练第一层的梯度下降线性收敛至全局最优。"
- "Theorem 4.6 证明收敛速度由标签向量在KAN‑TK特征向量上的投影决定。"
- "实验表明，网络越宽，训练误差下降越快（Figure 2a），权重变化越小（Figure 2b），验证了懒惰训练现象。"
- "结构化标签（与顶部特征向量对齐）比随机标签和反结构化标签收敛更快（Figure 3），验证了标签依赖的收敛速率。"
---

# On the Convergence of Two-Layer Kolmogorov-Arnold Networks with First-Layer Training

> [!tip] 核心洞察
> 在足够宽且使用RBF基函数的两层KAN中，梯度下降训练第一层参数会线性收敛到零训练误差，收敛速度由标签向量在KAN正切核（KAN‑TK）特征谱上的投影决定，且所需宽度 m=O(n²) 显著优于传统ReLU网络的 O(n⁶)。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 关于第一层训练的两层 Kolmogorov-Arnold 网络的收敛性 |
| 英文题名 | On the Convergence of Two-Layer Kolmogorov-Arnold Networks with First-Layer Training |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=buuwRBYfrP) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | 第一层训练的两层 Kolmogorov‑Arnold 网络（First‑Layer Training for Two‑Layer KANs） |
| Dataset | 合成数据 (n=100, d=100), 1D合成数据 (n=50), 理论比较 |

> [!tip] 效果简介
> - 合成数据 (n=100, d=100) 上，训练误差下降速度 为 宽度 m 越大收敛越快，对比 宽度小收敛慢，变化 定性加速。
> - 合成数据 (n=100, d=100) 上，权重偏离初始化的最大距离 为 宽度越大偏离越小，对比 宽度小偏离大，变化 懒惰程度增加。
> - 1D合成数据 (n=50) 上，收敛速度 为 结构化标签最快，对比 随机标签中等，反结构化最慢，变化 定性排序。

## 概述

现代深度学习中 Kolmogorov‑Arnold 网络（KAN）凭借其可学习单变量函数的嵌套结构，展现出强大的表达能力。然而，两层 KAN 的训练动态缺乏理论保证：在过参数化条件下，梯度下降为何能收敛到全局最优？仅训练第一层系数的简化方案是否能保持收敛性？这些问题尚未得到解答。

本文针对 **仅训练第一层参数、固定第二层** 的两层 KAN，在 **过参数化** 与 **径向基函数（RBF）作为基函数** 的设置下，首次建立了梯度下降的 **线性收敛理论**。核心策略是将训练动态的分析转化为对 **KAN‑正切核（KAN‑TK）** 谱特性的研究，从而绕过传统 ReLU 网络所需的极高过参数化要求。

主要结果包括：
- **全局收敛保证**：当隐藏层宽度 $m$ 满足 $m = \mathcal{O}(n^2)$（其中 $n$ 为样本数）且初始化方差足够小时，全批量梯度下降以逆线性速度将训练误差驱动至零，且第一层系数保持在初始值附近，形成 **懒惰训练** 现象（Theorem 4.2）。
- **标签依赖的收敛速率**：收敛速度由标签向量在 KAN‑TK 特征向量上的投影决定——当标签与首部特征向量对齐时收敛最快；反结构化标签最慢（Theorem 4.6，Figure 3）。
- **显著优于经典网络**：与标准 ReLU 网络的 $\mathcal{O}(n^6)$ 隐藏宽度要求相比（Du et al., 2019），以及两层 KAN 联合训练的 $\tilde{\mathcal{O}}(g^9 n^3)$ 要求相比（Gao & Tan, 2025），本文的 $\mathcal{O}(n^2)$ 宽度极大地降低了过参数化成本（Table 1）。

实验在合成数据、MNIST 和 CIFAR‑10 上验证了理论：更宽的网络收敛更快且参数位移更小（Figure 2），仅训练第一层可比拟甚至优于全网络训练（Figure 11, Figure 12），且 KAN 收敛速度快于同宽度的 ReLU 网络（Figure 10）。理论界也与实际损失下降趋势吻合（Figure 9）。

**局限性**：当前理论限于两层 RBF‑KAN、全批量梯度下降及均方误差损失；对深层 KAN、其它基函数（如 B‑spline）、随机优化以及交叉熵损失的行为仍有待探索。

## 背景与动机

两层 Kolmogorov-Arnold 网络（KAN）受 Kolmogorov-Arnold 表示定理启发，将多元连续函数表为嵌套的单变量基函数求和（见图1）：

$$
f ( \pmb { x } ) = \frac { 1 } { \sqrt { m } } \sum _ { p = 1 } ^ { m } \sum _ { l = 1 } ^ { g } \beta _ { p l } \phi _ { l } ( z _ { p } ) , \quad z _ { p } = \sum _ { k = 1 } ^ { d } \sum _ { j = 1 } ^ { g } \alpha _ { p j k } \phi _ { j } ( x _ { k } )
$$

该架构用可学习的单变量函数取代传统神经元的固定激活，在表达能力上具有潜力，但其非凸优化的理论理解远远落后于实践。核心瓶颈在于：**两层 KAN 的训练动态缺乏严格收敛保证，尤其是不清楚仅训练第一层系数 $\alpha$ 并固定第二层权重 $\beta$ 时，梯度下降为何能在过参数化条件下收敛到全局最优**。对比现有理论，标准两层 ReLU 网络（Du et al., 2019）需要隐藏层宽度 $m=\mathcal{O}(n^6)$ 才能保证收敛；对 KAN 联合训练两层（Gao & Tan, 2025）也需要 $m=\tilde{\mathcal{O}}(g^9 n^3)$，宽度需求仍不切实际。

实验现象为简化分析提供了关键线索：当只训练第一层时，**网络越宽，训练误差下降越快（图2a），且权重偏离初始化的幅度越小（图2b），呈现典型的懒惰训练（lazy training）特征**；同时，标签向量与 KAN 正切核（KAN‑TK）特征谱的对齐程度直接决定收敛快慢（图3）。这表明训练动态主要由冻结在初始点附近的 KAN‑TK 控制，而增大隐藏层宽度是进入懒惰训练区并降低核频谱条件的可操控手段。

基于上述动机，本文聚焦于**仅训练第一层系数、固定第二层并采用 RBF 基函数**的两层 KAN，在过参数化条件下建立首个端到端收敛理论。重要改进包括：

- 严格的线性收敛保证：当宽度 $m$ 满足 $m \gtrsim \max\bigl(\frac{d^2 g^6 n^2}{\lambda_0^2}\log(n/\delta),\, n\bigr)$，梯度下降以 $\mathcal{L}(t+1)\le(1-\frac{\eta\lambda_0}{2})\mathcal{L}(t)$ 的速率将训练损失压缩至零（Theorem 4.2），所需宽度从传统网络的 $\mathcal{O}(n^6)$ 和 KAN 全训练的 $\tilde{\mathcal{O}}(g^9 n^3)$ 显著降至 $\mathcal{O}(n^2)$（Table 1）。

- 标签依赖的收敛速率：误差上界 $\|y - \pmb{u}(t)\|_2 \le \sqrt{\sum_i (1-\eta\lambda_i)^{2t}(\pmb{v}_i^{\mathsf T}\pmb{y})^2} \pm \epsilon$ 显式表明，**收敛速度由标签向量在 KAN‑TK 特征向量上的投影决定**，当标签集中投影在顶端特征向量时收敛最快（Theorem 4.6，图3 验证）。

这些结果不仅给出了理论保障，还揭示了 KAN 训练中“宽度—收敛速率—标签结构”的内在因果链条，为后续深层 KAN 的优化理论奠定基础。

## 核心创新

### 关键瓶颈与解决思路

两层 Kolmogorov-Arnold 网络（KAN）的训练动态长期缺乏理论保证。现有工作要么要求联合训练两层参数导致分析复杂，要么所需网络宽度极高。本文的核心洞见在于：**仅训练第一层系数并固定第二层**，同时利用可学习的单变量基函数替代固定激活，可在过参数化条件下获得严格的全局收敛保证，且显著降低宽度需求。

### 架构层面的关键改动

| 改动维度 | 基线方法 | 本文方法 | 证据锚点 |
|---------|---------|---------|---------|
| 可训练层 | 全部层（标准 NN 或 KAN） | 仅第一层系数 α，第二层 β 固定 | Section 2.4 |
| 激活函数 | ReLU（标准 NN） | 可学习的单变量基函数（如 RBF） | Section 2.1, Section 3 |

前向传播公式为：
$$f(\mathbf{x}) = \frac{1}{\sqrt{m}} \sum_{p=1}^{m} \sum_{l=1}^{g} \beta_{pl} \phi_l(z_p) \quad \text{where} \quad z_p = \sum_{k=1}^{d} \sum_{j=1}^{g} \alpha_{pjk} \phi_j(x_k)$$

其中第一层系数 $\alpha_{pjk}$ 通过梯度下降更新，第二层系数 $\beta_{pl}$ 在 $\{-1, +1\}$ 均匀采样后固定不变。这种"半冻结"策略将非凸优化问题转化为可通过正切核（Tangent Kernel）分析的形式。

### 理论保证：线性收敛与宽度缩减

**Theorem 4.2** 建立了全局收敛的充分条件：当隐藏层宽度满足
$$m \gtrsim \max\left( \frac{d^2 g^6 n^2}{\lambda_0^2} \log\left(\frac{n}{\delta}\right), n \right), \quad \sigma = \mathcal{O}\left( \frac{\delta}{\sqrt{m n g^3 d}} \right)$$
时，梯度下降以线性速率收敛：
$$\mathcal{L}(t+1) \leq \left(1 - \frac{\eta \lambda_0}{2}\right) \mathcal{L}(t)$$

其中 $\lambda_0$ 为初始 KAN 正切核（KAN-TK）的最小特征值。这一宽度要求 $m = \mathcal{O}(n^2)$ 相比标准 ReLU 网络的 $\mathcal{O}(n^6)$（Du et al., 2019）和联合训练 KAN 的 $\tilde{\mathcal{O}}(g^9 n^3)$（Gao & Tan, 2025）实现了多项式级改进，且对 $\lambda_0$ 的依赖从 $\lambda_0^{-4}$ 改善为 $\lambda_0^{-2}$（Table 1）。

### 收敛速率的标签依赖性

**Theorem 4.6** 进一步揭示收敛速度并非均匀，而是由标签向量在 KAN-TK 特征谱上的投影结构决定：
$$\|\mathbf{y} - \mathbf{u}(t)\|_2 \leq \sqrt{\sum_{i=1}^{n} (1 - \eta \lambda_i)^{2t} (\mathbf{v}_i^T \mathbf{y})^2} \pm \epsilon$$

实验验证（Figure 3）：结构化标签（与顶部特征向量对齐）收敛最快，随机标签次之，反结构化标签（与底部特征向量对齐）最慢。Figure 8 显示标签能量在特征谱上的分布直接决定训练效率。

### 懒惰训练机制的实验验证

Figure 2 验证了关键的理论预测：网络宽度 $m$ 越大，(a) 训练误差下降越快，(b) 权重系数偏离初始化的 $\ell_\infty$ 距离越小。这与正切核框架下的"懒惰训练"（lazy training）预期一致——宽网络中参数几乎不移动，动态由初始核主导。

消融实验（Figure 11, 12）进一步表明：仅训练第一层不仅优于仅训练第二层，且性能可与全网络联合训练媲美，同时享有更简洁的理论分析。

### 与 ReLU 网络的实证对比

Figure 10 显示，在相同宽度 $m=1000$ 下，FastKAN 比 ReLU 网络收敛更快，验证了可学习基函数在优化效率上的优势。MNIST 和 CIFAR-10 上的收敛分析（Figure 6, 7）表明理论预测在真实数据集上仍具指导性。

### 局限性与待验证点

- 理论仅覆盖两层架构，深层 KAN 的扩展尚属开放问题
- 分析基于 RBF 基函数，B-spline 等其他基函数的收敛性**需手动验证**
- 全批量梯度下降的假设；SGD/Adam 等随机优化的行为**未在理论中涵盖**
- 宽度需求随 $n^2$ 增长，对极大规模数据仍可能过高

## 整体框架

![[assets/figures/papers/iclr26_0015_buuwRBYfrP_On_the_Convergence_of_Two-Layer_Kolmogorov-Arnol/figures/001_Figure_1.jpg]]
*Figure 1: Architecture of a two-layer Kolmogorov-Arnold Network (KAN). The inner functions (blue) map inputs to intermediate latent variables z, which are then processed by outer functions (orange) and aggregated*

![[assets/figures/papers/iclr26_0015_buuwRBYfrP_On_the_Convergence_of_Two-Layer_Kolmogorov-Arnol/figures/006_Table_1.jpg]]
*Table 1: Comparison of required hidden layer width and number of trainable parameters for global convergence guarantees*

本文聚焦于两层 Kolmogorov‑Arnold 网络（Two‑Layer KAN）的训练动态，并提出一种简化的优化策略：仅训练第一层的系数，而将第二层系数固定。该设计通过解耦两层参数，使梯度下降的分析聚焦于可训练的第一层，从而在过参数化（大隐藏层宽度 $m$）条件下建立起全局收敛的严格理论保证。

整个框架的前向计算流由以下四个模块级联构成（参见 Figure 1 / Figure 4）：

1. **输入层**：接收 $d$ 维向量 $\pmb{x} \in \mathbb{R}^d$，代表单个训练样本。
2. **第一层基函数变换**：对每个隐藏节点 $p=1,\dots,m$ 和每个输入维度 $k=1,\dots,d$，使用可学习的系数 $\alpha_{pjk}$ 对一组基函数 $\phi_j(\cdot)$ 进行线性组合，并跨维度求和，生成中间潜变量
   $$\displaystyle z_p = \sum_{k=1}^{d}\sum_{j=1}^{g} \alpha_{pjk}\,\phi_j(x_k),$$
   其中 $\phi_j$ 为预设的单变量基函数（本文主要使用高斯型 RBF）。$\alpha_{pjk}$ 是 **唯一** 通过梯度下降更新的参数。
3. **第二层基函数变换**：对潜变量 $z_p$ 再次应用基函数，并用固定系数 $\beta_{pl}$ 加权。系数 $\beta_{pl}$ 在初始化后保持不变，通常从 $\{\pm 1\}$ 等对称分布采样并除以 $\sqrt{m}$ 以稳定前向。
4. **缩放与聚合**：将所有 $p$ 和 $l$ 的贡献相加，再乘以缩放因子 $1/\sqrt{m}$，最终得到标量输出
   $$\displaystyle f(\pmb{x}) = \frac{1}{\sqrt{m}} \sum_{p=1}^{m}\sum_{l=1}^{g} \beta_{pl}\,\phi_l(z_p).$$

训练过程以均方误差（MSE）为目标函数：
$$\displaystyle \mathcal{L} = \frac{1}{2}\sum_{i=1}^{n}\bigl(y_i - f(\pmb{x}_i)\bigr)^2,$$
利用全批量梯度下降仅更新 $\alpha$ 参数。第二层系数 $\beta$ 完全不参与训练，这一设计切断了层间耦合，使得梯度计算仅依赖第一层的局部线性化。

**理论收敛机制**。在隐藏层宽度充分大（$m \gtrsim \max\!\bigl(\frac{d^2 g^6 n^2}{\lambda_0^2}\log\frac{n}{\delta},\,n\bigr)$）且初始化方差足够小（$\sigma = O(\frac{\delta}{\sqrt{m n g^3 d}})$）的条件下，该框架表现出 **懒惰训练** 行为：训练过程中参数变化极小，整个网络的输出可由其一阶泰勒展开近似，正切核 $\pmb{H}(t)$ 始终接近其无限宽时的极限 $\pmb{H}^\infty$，且最小特征值 $\lambda_0>0$ 恒定。由此可证明梯度下降以线性速度将训练误差驱动至零：
$$\displaystyle \mathcal{L}(t+1) \le \Bigl(1 - \frac{\eta\lambda_0}{2}\Bigr)\,\mathcal{L}(t).$$
进一步，收敛速率由标签向量在 KAN‑TK（KAN Tangent Kernel）特征向量上的投影分布决定：标签能量越集中在最大特征值对应的方向，收敛越快（Theorem 4.6）。

**与现有方案的对比**。传统的两层 ReLU 神经网络需要 $m = O(n^6)$ 的宽度才能保证全局收敛，而本框架通过固定第二层并利用 RBF 基函数的分析特性，将宽度需求降低到 $m = O(n^2)$（Table 1）。实验证据表明，更宽的网络不仅误差下降更快（Figure 2a），而且权重与初始化的距离更小（Figure 2b），验证了懒惰训练假设。此外，与训练全部两层或仅训练第二层相比，仅训练第一层在收敛速度上具有竞争力，甚至接近全网络训练的性能（Figure 11–12）。

总体而言，该整体框架以极简的训练设计（仅更新第一层系数）和大幅降低的宽度需求，为两层 KAN 的优化提供了首个具有多项式改善的收敛理论，并为后续深层架构和随机优化的分析搭建了基础模板。

## 核心模块与公式推导

### 网络前向结构与分层模块

论文分析的两层 Kolmogorov‑Arnold 网络（KAN）接收 $d$ 维输入 $\pmb{x}$，经宽度为 $m$ 的隐藏层后输出标量。其关键设计在于：**仅第一层系数可训练，第二层系数固定**，且基函数采用**可学习的单变量表示**（如 RBF）。

#### 模块 1：第一层基函数变换（可训练）

对于每个隐藏神经元 $p=1,\dots,m$，输入的各分量 $x_k$ 先通过 $g$ 个基函数 $\phi_j(\cdot)$ 展开，再由可训练系数 $\alpha_{pjk}$ 加权求和，形成中间潜变量 $z_p$：

$$
z_p = \sum_{k=1}^{d} \sum_{j=1}^{g} \alpha_{pjk}\,\phi_j(x_k)
$$

其中 $\alpha_{pjk}$ 初始化为 $\mathcal{N}(0,\sigma^2)$，并沿梯度下降更新；基函数常采用 RBF 形式：

$$
\phi_j(x) = \exp\!\left(-\frac{(x-\mu_j)^2}{2\sigma^2}\right)
$$

#### 模块 2：第二层基函数变换（固定）与输出聚合

每个潜变量 $z_p$ 被送入第二层基函数 $\phi_l(\cdot)$，经固定系数 $\beta_{pl}\in\{-1,+1\}$ 加权，最后以 $1/\sqrt{m}$ 缩放求和得到网络输出：

$$
f(\pmb{x}) = \frac{1}{\sqrt{m}}\sum_{p=1}^{m}\sum_{l=1}^{g} \beta_{pl}\,\phi_l(z_p)
$$

缩放因子 $1/\sqrt{m}$ 保证在无限宽极限下切线核（KAN‑TK）存在确定性闭式（见 Proposition 3.1 及附录 A.2），从而支撑后续收敛分析。

### 训练目标与参数更新

网络在 $n$ 个样本上的训练采用均方误差（MSE）损失：

$$
\mathcal{L} = \frac{1}{2}\sum_{i=1}^{n}\bigl(y_i - f(\pmb{x}_i)\bigr)^2 = \frac{1}{2}\|y-\pmb{u}\|_2^2
$$

其中 $\pmb{u}\in\mathbb{R}^n$ 为当前网络对所有样本的输出向量。**仅更新第一层系数** $\alpha$，梯度下降步长为 $\eta$。

### 理论保证中的关键公式

以下公式来自论文的核心定理，定义了全局收敛所需的条件与收敛速率。

**过参数化条件（Theorem 4.2）**  
为保证线性收敛，隐藏层宽度 $m$ 和初始化方差 $\sigma$ 需满足：

$$
m \gtrsim \operatorname{max}\!\left( \frac{d^{2} g^{6} n^{2}}{\lambda_{0}^{2}} \log\!\left(\frac{n}{\delta}\right),\; n\right), \qquad
\sigma = \mathcal{O}\!\left( \frac{\delta}{\sqrt{m\,n\,g^{3}\,d}} \right)
$$

其中 $\lambda_0>0$ 是初始切线核 $\pmb{H}(0)$ 的最小特征值（或极限核 $\pmb{H}^{\infty}$ 的特征值下界），$\delta$ 控制近似误差。

**线性收敛保证（Theorem 4.2）**  
在过参数化区域内，每一步梯度下降使损失按固定因子收缩：

$$
\mathcal{L}(t+1) \leq \left(1 - \frac{\eta\lambda_0}{2}\right) \mathcal{L}(t)
$$

这意味着训练误差以线性速率趋近于零，且权重始终停留在初始化附近（懒惰训练）。

**标签依赖的误差界（Theorem 4.6）**  
进一步，收敛速度由标签向量 $\pmb{y}$ 在 KAN‑TK 特征谱上的投影决定：

$$
\|y - \pmb{u}(t)\|_2 \leq \sqrt{ \sum_{i=1}^{n} \bigl(1 - \eta\lambda_i\bigr)^{2t} \bigl(\pmb{v}_i^{T}\pmb{y}\bigr)^2 } \pm \epsilon
$$

其中 $\lambda_i$、$\pmb{v}_i$ 为极限核 $\pmb{H}^{\infty}$ 的特征值与特征向量，$\epsilon$ 为有限宽度造成的扰动项。由此，**标签与顶部特征向量对齐越好，收敛越快**（实验 Figure 3 验证了这一预测）。

上述宽度需求 $m=\mathcal{O}(n^{2})$ 比传统两层 ReLU 网络所需的 $\mathcal{O}(n^{6})$ 显著降低（Table 1），体现了 KAN 在仅训练第一层时的理论优势。

## 实验与分析

**实验目的** 直接在受控合成数据上验证两层KAN第一层训练的收敛性质：宽度对懒惰训练与误差衰减的影响（Figure 2）、标签向量在KAN‑TK特征谱上的投影对收敛速率的决定作用（Figure 3），以及与标准网络相比所需的资源量级（Table 1）。此外通过消融确认第一层训练相对于其他训练配置的优越性（Figure 11, 12），并揭示KAN在相同宽度下比ReLU网络收敛更快（Figure 10），但亦明确当前框架的失效边界与未覆盖场景。

![[assets/figures/papers/iclr26_0015_buuwRBYfrP_On_the_Convergence_of_Two-Layer_Kolmogorov-Arnol/figures/003_Figure_2.jpg]]
*Figure 2: Convergence behavior across hidden widths m. (a) Training error decreases faster for wider networks. (b) Wider networks exhibit smaller deviations from initialization, consistent with the lazy training regime*

![[assets/figures/papers/iclr26_0015_buuwRBYfrP_On_the_Convergence_of_Two-Layer_Kolmogorov-Arnol/figures/005_Figure_3.jpg]]
*Figure 3: Effect of label structure on convergence. (a) Structured labels align with top eigenvectors, whereas random labels distribute across the spectrum. (b) Training converges fastest for structured labels, slower for random labels, and slowest for anti-structured labels*

![[assets/figures/papers/iclr26_0015_buuwRBYfrP_On_the_Convergence_of_Two-Layer_Kolmogorov-Arnol/figures/023_Figure_10.jpg]]
*Figure 10: Convergence of FastKAN and a ReLU network with width m = 1000 across different sample sizes*

### 主实验结果

**宽度增大触发懒惰训练与加速收敛**  
在 $n=100,d=100$ 的合成数据上，将隐藏宽度 $m$ 从 200 升至 6400，训练误差下降速率显著提升（Figure 2a），同时第一层系数相对初始值的最大偏移量单调递减（Figure 2b）。该现象直接支持过参数化条件下的“懒惰训练”假说：当 $m$ 超过约 $O(n^2)$ 的门槛后，参数几乎静止，网络行为由初始化附近的切核线性化主导，从而使梯度下降以 $(1-\eta\lambda_0/2)$ 的恒定速率线性收缩损失（Theorem 4.2 的保证）。实验趋势与理论一致：越宽越懒、越懒收敛越快。

**标签‑特征对齐决定收敛速率**  
构造结构化（标签对齐于 KAN‑TK 顶部特征向量）、随机、反结构化（对齐于底部特征向量）三类标签（1D 合成，$n=50$）。Figure 3a 显示结构化标签的能量集中在最大的几个特征值上，而随机标签均匀散布，反结构化标签集中于小特征值。这一差异直接映射到收敛速度：结构化标签最快，随机居中，反结构化最慢（Figure 3b）。此结果验证了标签依赖误差界——训练 $t$ 步后的残差可被 $\\sum_i (1-\eta\lambda_i)^{2t} (\\bm{v}_i^T\\bm{y})^2$ 控制（Theorem 4.6），当 $\bm{y}$ 与较大特征向量对齐时平方和衰减更快。类似行为在附录中的 MNIST（Figure 6）和 CIFAR‑10（Figure 7）上亦被观察到，表明标签结构解释力并非合成数据独有。

**资源需求量级显著降低**  
Table 1 汇总了保证全局收敛所需的理论隐藏层宽度：标准两层ReLU网络为 $m=\mathcal O(n^6)$（Du et al., 2019），同时训练两层KAN为 $\tilde{\mathcal O}(g^9 n^3)$（Gao & Tan, 2025），而仅训练第一层的KAN仅需 $m=\mathcal O(n^2)$。实验虽未直接测量 $n^6$ 规模，但 Figure 2a 证实 $m$ 只需数千即可在 $n=100$ 上实现快速收敛，与 $O(n^2)$ 量级一致；相比之下，同等尺寸的标准网络在相似任务上需要 $m$ 远大于 $10^4$ 才能进入懒惰区域。在所需学习率方面（Table 2），第一层训练要求 $\eta=\mathcal O(\lambda_0/(n^3 d^2 g^6))$，虽更严苛，但懒惰性质使训练不易发散。

### 消融实验

**第一层训练优于仅训练第二层，且逼近全网络训练**  
在合成数据上，仅训练第二层系数而固定第一层，训练误差几乎不下降；仅训练第一层则目视同等于全网络训练的性能（Figure 11, Figure 12）。这一消融支撑了核心设计决策：第一层系数的梯度承载了输入变量间的交互信息，而固定第二层不会严重损害表达力，反而大幅简化动力学并导出更紧的宽度要求。由此“第一层训练+固定第二层”作为分析范式的实用价值得到确认。

![[assets/figures/papers/iclr26_0015_buuwRBYfrP_On_the_Convergence_of_Two-Layer_Kolmogorov-Arnol/figures/027_Figure_12.jpg]]
*Figure 12: Comparison of first-layer and full-network training: (a) training error over all epochs, and (b) final training error*

**KAN 比同宽 ReLU 网络收敛更快**  
无论样本量 $n$ 如何变化，宽度 $m=1000$ 的 KAN 在训练损失下降速度上均快于同宽的ReLU网络（Figure 10）。这暗示可学习的径向基函数组合赋予了 KAN 更优的初始切核条件数（即 $\lambda_0$ 更大），使得梯度下降的方向更直接朝向全局最优，而 ReLU 的切核可能更不适定。与表1中理论宽度需求降阶的趋势一致。

**切核回归与实际训练的一致性**  
Figure 5 展示用推导出的无穷宽 KAN‑TK 进行核回归，即可在简单合成函数上获得光滑拟合；Figure 9 进一步比较理论收敛界（红色虚线）与真实损失曲线（蓝色实线），在合适学习率下理论界紧紧跟踪经验动态，表明切核线性化模型在过参数化区域内是高度保真的近似。

### 失效模式与局限性

1. **深度限制** 所有理论保证及实验验证均仅针对两层KAN。一旦堆叠更多层，切核结构会剧烈变化，懒惰训练是否延续未知；初步尝试深层KAN的数值不稳定与梯度弥散已在部分附录实验中暴露。
2. **基函数依赖** 收敛性推导强烈依赖RBF基函数的解析可积性以得出闭式KAN‑TK。若替换为 B‑spline、SiLU 等常用基函数，核的形式无法写出，理论保证失效，且实验中常观察到不同的收敛速度与稳定性表现。
3. **仅第一层训练的应用局限** 尽管消融显示其能与全训练媲美，但在需要第二层高度数据自适应的场景（如风格迁移、复杂强化学习任务）中，固定第二层可能导致容量不足。当前结果无法简单推广至全训练。
4. **优化器与批量假设** 全批量梯度下降的动力学与随机优化（SGD/Adam）存在本质差异，尤其当噪声主导参数更新时，“懒惰”不再能由切核稳定保证。Figure 6‑7 在真实数据上虽显示类似趋势，但均使用全批量或大batch，小批量下的泛化与收敛尚需进一步实验。
5. **宽度‑样本量依赖** 虽然宽度需求从 $O(n^6)$ 降至 $O(n^2)$，对于百万级数据仍意味着庞大的隐藏层（$m\sim10^{12}$），不具备实用可部署性。中等宽度下的早停与隐式正则化效果并未在理论中刻画。
6. **损失函数类型** 全部分析基于MSE损失；交叉熵等分类损失下，切核不再定义，网络参数是否保持接近初始化的结论不可直接迁移，现有的MNIST/CIFAR‑10实验（Figure 6, 7）仅作为观察性补充，而非定理证明。

### 重要图表结论归纳

- **Figure 2**：宽度增大导致训练损失下降更快、参数位移更小，强证据支持懒惰训练机制与 $m=\mathcal O(n^2)$ 的充分性。
- **Figure 3 & Figure 8**：标签在 KAN‑TK 特征谱上的投影分布是收敛速率的直接原因；结构化标签在前少数特征值上能量集中，反结构标签在尾部，收敛速度差异达数量级，验证 Theorem 4.6。
- **Table 1**：仅训练第一层的KAN将全局收敛所需隐藏宽度从 $O(n^6)$ 或 $\tilde O(g^9 n^3)$ 大幅缩减至 $O(n^2)$，且可训练参数仅来自第一层，资源效率突出。
- **Figure 11‑12**：第一层训练与全网络训练性能持平，优于仅训练第二层，说明第一层系数是训练的关键自由度；验证“第一层训练+固定第二层”作为分析性替身的有效性。
- **Figure 10**：在相同网络宽度下，KAN较ReLU网络收敛更快，提示可学习基函数的组合带来更好的初始核条件。

## 方法谱系与知识库定位

本文提出的“仅训练第一层系数、固定第二层”的两层 Kolmogorov‑Arnold 网络（First‑Layer Training KAN）处于 KAN 优化理论发展的一个关键节点：它用简化但富有洞见的训练方案，首次给出了两层 KAN 的全局收敛速度与特征谱依赖的显式理论。在方法谱系上，其位置通过两个明确的基线来界定。

**相对于标准两层神经网络**（Du et al., 2019，ReLU 激活、全参数训练），本工作的根本差异在于将激活函数从固定的 ReLU 替换为可学习的单变量基函数（RBF），并把训练参数缩减为仅第一层系数。这一改变导致了两项关键改进：（1）保证全局收敛所需的隐藏层宽度从 $m = \mathcal O(n^6 / \lambda_0^4 \delta^3)$ 骤降至 $m = \mathcal O(n^2)$（表 1），同时所需学习率从 $\mathcal O(\lambda_0 / n^2)$ 变为与 n 无关的常数量级（表 2）；（2）对正切核最小特征值 $\lambda_0$ 的依赖性由 $\lambda_0^{-4}$ 改善为 $\lambda_0^{-2}$，显著降低了对数据条件数的敏感度。这些改进的因果杠杆在于：仅训练第一层使得正切核（KAN‑TK）的秩结构与随机初始化的第二层解耦，从而在过参数化时收敛行为仅由第一层参数的线性化动力学支配（Lemma 4.3、Lemma 4.4）。

**相对于两层 KAN 的联合训练**（Gao & Tan, 2025，两层系数同时学习），本工作通过“冻结第二层”进一步简化了分析对象，同时也带来了由耦合训练无法获得的新理论结果。联合训练方法要求的宽度为 $\tilde{\mathcal O}(g^9 n^3 / \lambda_0^4)$，且理论依赖于两层的交互；而第一层训练方案将宽度降至 $m = \mathcal O(n^2)$，并首次给出了依赖标签结构的细粒度收敛速度：训练误差的上界由标签向量在 KAN‑TK 特征向量上的投影决定，与顶部特征向量对齐的“结构化标签”收敛最快，随机标签次之，反结构化标签最慢（Theorem 4.6，图 3）。消融实验中，仅训练第一层的最终训练误差可与全网络训练相媲美，且显著优于仅训练第二层的方案（图 11、图 12），证明这一简化设置具有一定实用潜力。

**适用边界**建立在若干明确假设之上。首先，网络限定为两层标量输出结构，且第二层系数固定并随机初始化（$\beta_{pl}\in\{-1,+1\}$）；基函数须为径向基函数（RBF）以便推导 KAN‑TK 的闭合形式。训练使用全批量梯度下降与均方误差（MSE）损失，并要求隐藏层宽度满足 $m \gtrsim \max\left( \frac{d^2 g^6 n^2}{\lambda_0^2} \log(n/\delta), n \right)$ 且初始化方差 $\sigma = \mathcal O(\delta / \sqrt{m n g^3 d})$（Theorem 4.2）――这些条件共同界定了“过参数化的懒惰训练区域”。在此区域内，网络参数始终保持在初始化的小邻域内，训练误差每一步以线性速度收缩（$\mathcal L(t+1) \le (1 - \eta\lambda_0/2)\,\mathcal L(t)$）。脱离这些假设（如减小宽度、增大初始化、切换为 SGD 或交叉熵损失）时，收敛保证将不再适用，网络可能进入特征学习区间或趋于发散。此外，宽度要求虽已从 $n^6$ 改进为 $n^2$，但对超大规模数据集（$n > 10^5$）仍属偏高，限制了直接应用。

**局限性**主要体现在理论与实践的间隙。其一，理论仅覆盖两层网络与 RBF 基函数，对更深架构或更常用的 B‑spline 基函数是否成立，尚缺乏证明。其二，全批量梯度下降与 MSE 损失的设定与实际训练中广泛使用的 SGD/Adam 和交叉熵损失存在差异，后者的隐式正则化效应未被纳入理论框架。其三，固定第二层虽带来分析便利，但在某些任务中可能限制表示能力；当前实验仅在合成数据及 MNIST、CIFAR‑10 等相对简单的任务上验证，未见大规模或更复杂的真实世界任务上的表现。其四，过参数化下 $m = \mathcal O(n^2)$ 的宽度意味着训练参数量的快速增长，计算成本仍显著。最后，理论依赖的正切核分析框架虽然给出了收敛性，但未能刻画网络在中等宽度下的特征学习能力，以及 KAN 所特有的可解释性优势如何在过参数化区域中被保留或丧失。

**待解决的开放问题**自然从这些局限中生长出来：**（1）深层扩展**――将正切核框架推广到三层及更深 KAN，并揭示深度对收敛速率与“宽度‑深度”权衡的作用；**（2）实用优化器**――在 SGD/Adam 等随机优化及交叉熵损失下，理论保证是否延续，懒惰训练何时过渡到主动的特征学习；**（3）紧致收敛界**――探索超越正切核的替代理论路径（如平均场方法），以消除对 $\lambda_0$ 和对数因子的依赖，得到更实用的宽度建议；**（4）KAN‑TK 的一般化**――对多维输入、不同基函数（如 B‑spline）以及向量输出版本，推导 KAN‑TK 的解析表达式；**（5）可解释性与理论的融合**――在过参数化懒惰区域内，KAN 的符号回归与函数分解能力是否得到保持或强化，能否将收敛保证转化为可解释性保证。这些问题的推进将决定 Kolmogorov‑Arnold 网络理论能否从简化的两层第一层训练走向复杂但更现实的实际应用场景。

## 原文 PDF

![[paperPDFs/ICLR_2026/On_the_Convergence_of_Two_Layer_Kolmogorov_Arnold_Networks_with_First_Layer_Training.pdf]]
