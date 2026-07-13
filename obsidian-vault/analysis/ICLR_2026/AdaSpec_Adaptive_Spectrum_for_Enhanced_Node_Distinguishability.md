---
title: "AdaSpec: Adaptive Spectrum for Enhanced Node Distinguishability"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AdaSpec_Adaptive_Spectrum_for_Enhanced_Node_Distinguishability.pdf
project_link: null
code_link: https://github.com/Mia-321/AdaSpec
openreview_forum_id: eHhUYoZwWs
aliases:
- AASEND
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "引入一个可学习的对角偏置矩阵 B 和特征自适应的 Hadamard 积项，动态生成图矩阵 Ω(A,X) = Ω_D(A) + α₁ Ω_S(A) + α₂ Ω_F(X)，从而增加不同特征值数量 d_M、将零特征值移离零、并提高非零频率分量的数目 ∥X̃^(M)∥₀。这三个操作直接提升可区分节点的理论上界。"
primary_logic: "节点区分度的理论上界由 min(d_M, ∥X̃^(M)∥₀) 决定，其中 d_M 是图矩阵的不同特征值个数，∥X̃^(M)∥₀ 是节点特征在特征基上的非零频率分量的数量。通过优化图矩阵（而非仅仅改变多项式基底）来提升这两个量，可以显著提高谱 GNN 区分非同类节点的能力。"
claims:
- "Theorem 4.3 证明：存在一个谱 GNN Ψ(M,X) 可以区分至少 min(d_M, ∥X̃^(M)∥₀) 个节点，增加 d_M 或 ∥X̃^(M)∥₀ 可直接提升区分度下界。"
- "Table 2 和 Table 3 显示，在 18 个节点分类基准上，5 种谱 GNN 使用 AdaSpec 后平均准确率或 ROC AUC 均取得可观提升，尤其在异配图（heterophilic graphs）上表现显著。"
- "Table 5 表明 AdaSpec 的 Ω_D(A) 组件将不同特征值数量 d_{Ω_D(A)} 从原 Ã 的 d_{Ã} 大幅提升至接近节点数 |V|（如 Texas：113→181），直接验证了增加不同特征值的理论动机。"
- "Texas 上 Accuracy (%) = 51.16±8.56 (ChebNet(M))"
---

# AdaSpec: Adaptive Spectrum for Enhanced Node Distinguishability

> [!tip] 核心洞察
> 节点区分度的理论上界由 min(d_M, ∥X̃^(M)∥₀) 决定，其中 d_M 是图矩阵的不同特征值个数，∥X̃^(M)∥₀ 是节点特征在特征基上的非零频率分量的数量。通过优化图矩阵（而非仅仅改变多项式基底）来提升这两个量，可以显著提高谱 GNN 区分非同类节点的能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AdaSpec：增强节点区分性的自适应频谱 |
| 英文题名 | AdaSpec: Adaptive Spectrum for Enhanced Node Distinguishability |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=eHhUYoZwWs) · [GitHub](https://github.com/Mia-321/AdaSpec) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | AdaSpec |
| Dataset | Texas, Minesweeper, Roman_Empire, Cora |

> [!tip] 效果简介
> - Texas 上，Accuracy (%) 为 51.16±8.56 (ChebNet(M))，对比 38.67±9.31 (ChebNet(O))，变化 +12.49。
> - Minesweeper 上，ROC AUC (%) 为 89.13±0.1 (JacobiConv(M))，对比 87.34±0.12 (JacobiConv(O))，变化 +1.79。
> - Roman_Empire 上，Accuracy (%) 为 54.55±0.3 (ChebNet(M))，对比 47.15±0.42 (ChebNet(O))，变化 +7.4。

## 概要

谱图神经网络（Spectral GNNs）遵循统一范式 $\Psi(M,X) = g_{\Theta}(M) f_W(X)$，其中图矩阵 $M$ 通常固定为归一化邻接矩阵 $\tilde{A}$。这种固定设计存在一个根本性瓶颈：**特征值重数高**（eigenvalue multiplicity）和**节点特征在特征基上非零频率分量缺失**（missing frequency components），导致模型无法为非同构节点产生不同的嵌入，直接限制了谱 GNN 的表达能力和分类性能。

本文提出 **AdaSpec**，一种即插即用的自适应频谱增强模块。其核心思路是：不改变多项式基底，而是**动态优化图矩阵本身**，生成一个同时适应图结构与节点特征的自适应矩阵 $\Omega(A,X)$。该矩阵由三个可学习组件构成——$\Omega_D(A)$ 增加不同特征值数量 $d_M$、$\Omega_S(A)$ 将零特征值移离零、$\Omega_F(X)$ 提高非零频率分量数量 $\|\tilde{X}^{(M)}\|_0$——从而直接提升节点区分度的理论上界 $\min(d_M, \|\tilde{X}^{(M)}\|_0)$（Theorem 4.3）。

实验覆盖 5 种主流谱 GNN 基底（ChebNet、ChebNetII、JacobiConv、GPRGNN、BernNet）和 18 个节点分类基准。主要结果：
- **异配图**上提升显著，例如 Texas 数据集上 ChebNet 准确率从 38.67% 提升至 51.16%（+12.49），Roman_Empire 上提升至 54.55%（+7.4）；
- **同配图**上保持或小幅提升，如 Cora 上 ChebNet 准确率从 80.45% 提升至 81.01%（+0.56）；
- 消融实验确认三个组件的协同作用，其中 $\Omega_D(A)$ 在异配图上贡献最大；
- Table 5 定量验证了 $\Omega_D(A)$ 将不同特征值数量从原 $\tilde{A}$ 的水平大幅提升至接近节点总数（如 Texas：113→181），直接支撑理论动机；
- 时间复杂度与原始谱 GNN 保持同阶（Table 1），实际训练开销极小（Table 6）。

AdaSpec 保持了置换等变性，可与图重连（如 GDC）正交叠加，进一步获得增益（Table 10）。当前验证限于节点分类任务，$\Omega_F(X)$ 的预计算在极高维特征或超大规模图上可能引入一次性开销，且超参数 $\alpha_1$、$\alpha_2$ 需手动调节。



### 谱图神经网络的核心范式

谱图神经网络（Spectral GNNs）通过在图矩阵的特征空间上施加多项式滤波器来聚合邻居信息，其一般形式为：

$$\Psi(M, X) = g_{\Theta}(M) f_W(X)$$

其中 $M$ 为图矩阵（通常取归一化邻接矩阵 $\tilde{A} = D^{-1/2} A D^{-1/2}$ 或其归一化拉普拉斯矩阵），$g_{\Theta}(M)$ 是以 $M$ 为基的多项式滤波器，$f_W(X)$ 是对节点特征 $X$ 的可学习变换。ChebNet、ChebNetII、JacobiConv、GPRGNN 和 BernNet 等代表性方法均沿袭这一范式，区别仅在于多项式基的选择（Chebyshev、Jacobi、单项式、Bernstein 等）与系数参数化方式。

### 固定图矩阵的两重瓶颈

现有谱 GNN 的一个关键盲区在于：**图矩阵 $M$ 一旦选定便固定不变**，而该固定矩阵在真实图上普遍存在两个结构性缺陷，直接削弱模型区分非同构节点的能力。

**瓶颈一：特征值重数过高。** 真实图的归一化邻接矩阵通常只有远少于节点数的不同特征值。以 Texas 数据集为例，$\tilde{A}$ 的不同特征值数 $d_{\tilde{A}} = 113$，而节点数 $|V| = 183$。高重数意味着大量节点在特征空间中被投影到相同的特征值上，当滤波器阶数 $K$ 不足以利用特征向量差异时，这些节点将获得相同的嵌入，无法被区分。Figure 1(b) 给出了一个示意性案例：当 $d_{\tilde{A}} = 3$ 时，即使节点特征在特征基上有 5 个非零频率分量，一阶谱 GNN 仍无法区分节点 1 和节点 6。

**瓶颈二：节点特征的非零频率分量缺失。** 将节点特征 $X$ 投影到图矩阵的特征基上，得到频率分量矩阵 $\tilde{X}^{(M)}$。若 $\tilde{X}^{(M)}$ 中非零行的数量 $\|\tilde{X}^{(M)}\|_0$ 不足，即便特征值完全互异，滤波器也无法为不同节点产生不同的响应。Figure 1(a) 展示了这一情形：$d_{\tilde{A}} = 6$ 但 $\|\tilde{X}^{(\tilde{A})}\|_0 = 5$，节点 1 和 6 依然不可区分。Figure 2 在 Texas 和 Cora 数据集上的实证观测进一步验证了上述两种现象在真实图中的普遍性。

### 区分度的理论上界

上述两个量并非孤立存在，而是共同决定了谱 GNN 输出嵌入矩阵的秩的下界。Theorem 4.3 建立了核心理论关系：

$$\operatorname{rank}(\Psi(M, X)) \geq \min\left(d_M, \|\tilde{X}^{(M)}\|_0\right)$$

该下界直接给出了模型可区分的节点数目的理论上限：**增加不同特征值数量 $d_M$ 或增加非零频率分量数量 $\|\tilde{X}^{(M)}\|_0$，即可提升可区分节点的下界**。这一洞察揭示了问题的本质：谱 GNN 的表达瓶颈不在于多项式基的选择，而在于图矩阵本身的信息容量。

### 现有方法的缺口

现有改进谱 GNN 的工作几乎全部聚焦于优化多项式滤波器 $g_{\Theta}$ 的设计——例如引入更灵活的参数化策略或更稳定的基函数——而将图矩阵 $M$ 视为不可变的外部给定项。这种“固定图矩阵 + 优化滤波器”的策略无法从根本上突破由 $d_M$ 和 $\|\tilde{X}^{(M)}\|_0$ 所决定的区分度上界。当图矩阵本身的信息容量不足时，无论滤波器如何精妙，模型区分非同构节点的能力始终受限于 $\min(d_M, \|\tilde{X}^{(M)}\|_0)$。

### 本文动机

AdaSpec 的核心动机正是打破上述僵局：**不再将图矩阵视为固定输入，而是将其设计为一个可学习的、同时适应图结构与节点特征的模块**，通过直接优化 $d_M$ 和 $\|\tilde{X}^{(M)}\|_0$ 来提升节点区分度的理论上界。该模块以即插即用的方式嵌入任意谱 GNN，保持置换等变性，且不改变原模型的时间复杂度阶数。



## 核心方法与创新机理

AdaSpec 的核心创新在于将谱图神经网络（Spectral GNN）中**固定的图矩阵替换为一个自适应生成的图矩阵**，从而突破现有方法在节点区分能力上的理论上限。这一创新的因果机制可归结为以下三个关键层面的改变。

### 从固定图矩阵到自适应图矩阵

传统谱 GNN 遵循统一范式 $\Psi(M, X) = g_{\Theta}(M) f_W(X)$，其中图矩阵 $M$ 通常固定为归一化邻接矩阵 $\tilde{A} = D^{-1/2} A D^{-1/2}$ 或其变体。AdaSpec 将这一固定组件替换为**自适应图矩阵生成模块**：

$$\Psi^{+}(A, X) = g_{\Theta}(\Omega(A, X)) f_W(X)$$

其中 $\Omega(A, X)$ 同时依赖于图结构 $A$ 和节点特征 $X$，打破了传统方法仅依赖固定图拓扑的限制。这一改变是 AdaSpec 区别于所有 baseline 的根本性差异。

### 三个核心 changed slots 及其因果作用

AdaSpec 的自适应图矩阵由三个组件加权组合而成：

$$\Omega(A, X) = \Omega_D(A) + \alpha_1 \Omega_S(A) + \alpha_2 \Omega_F(X)$$

每个组件对应一个 baseline 所不具备的能力，直击节点区分度不足的两个根源——**特征值重数过高**和**非零频率分量缺失**。

**1. Ω_D(A)：增加不同特征值数量（changed slot: 图矩阵的谱多样性）**

Baseline 使用的 $\tilde{A}$ 在不同图上的不同特征值个数 $d_{\tilde{A}}$ 通常远小于节点数 $|V|$，导致谱 GNN 无法区分大量非同构节点。AdaSpec 引入可学习的对角偏置矩阵 $B$，构造：

$$\Omega_D(A) = (D + B)^{-1/2}(A + B)(D + B)^{-1/2}$$

这一设计的因果逻辑是：通过对每个节点施加独立的偏置 $B_{ii}$，打破原有图矩阵的对称性约束，从而**显著增加不同特征值的数量**。根据 Theorem 4.3，节点区分度的下界为 $\min(d_M, \|\tilde{X}^{(M)}\|_0)$，因此 $d_M$ 的提升直接推高了区分能力的天花板。实验验证（Table 5）表明，$\Omega_D(A)$ 将不同特征值数量从 $\tilde{A}$ 的水平大幅提升至接近 $|V|$（如 Texas 数据集：113 → 181），为这一因果机制提供了直接证据。

值得注意的是，标准归一化邻接矩阵 $\tilde{A}$ 及其自环版本 $\hat{A}$ 恰好是 $\Omega_D(A)$ 在 $B=0$ 和 $B=I$ 时的特例，说明 AdaSpec 是 baseline 图矩阵的严格推广，而非完全替代。

**2. Ω_S(A)：消除零特征值（changed slot: 特征值的零点偏移）**

Baseline 的图矩阵常存在零特征值，这些零特征值对应的特征基上节点特征无法产生区分性信号。AdaSpec 通过简单的平移操作：

$$\Omega_S(A) = I$$

将所有特征值统一加 1，从而**将零特征值移离零点**，减少零特征值的重数。该操作不改变特征向量结构，仅调整特征值分布，以极低的成本消除了零特征值对节点区分度的抑制效应。

**3. Ω_F(X)：增加非零频率分量（changed slot: 特征自适应的谱调制）**

Baseline 方法完全忽略节点特征在图矩阵构造中的作用。AdaSpec 引入特征自适应的 Hadamard 积项：

$$\Omega_F(X) = \sum_{i=1}^{h} \frac{X_{:i} X_{:i}^{\top}}{\|X_{:i}\|_F^2} \circ A$$

该组件利用节点特征各维度的归一化外积与邻接矩阵进行逐元素乘积，使得图矩阵能够**感知节点特征在特征基上的频率分布**，从而增加非零频率分量的数量 $\|\tilde{X}^{(M)}\|_0$。根据 Theorem 4.3，这一提升同样直接推高节点区分度的下界。

### 创新点的协同效应

消融实验（Table 4）揭示了三个组件的协同关系：单独使用 $\Omega_D(A)$ 在异配图（heterophilic graphs）上贡献最大，$\Omega_S(A)$ 在大规模数据集上有额外增益，而**三者联合使用时在所有场景下均取得最优性能**。这表明 AdaSpec 的三个 changed slots 并非独立工作，而是分别从谱多样性、零点消除和特征自适应三个维度协同提升图矩阵的表达能力。

### 与 baseline 的本质区别

所有 baseline 方法（ChebNet、ChebNetII、JacobiConv、GPRGNN、BernNet）的改进均集中在**多项式基函数 $g_{\Theta}$ 的设计**上——例如使用 Chebyshev 多项式、Jacobi 多项式或 Bernstein 多项式——而图矩阵 $M$ 始终保持固定。AdaSpec 的创新在于**将优化对象从多项式基底转移到图矩阵本身**，这一视角转变使得谱 GNN 的表达能力不再受限于固定的图拓扑表示，而是可以通过学习自适应地调整图矩阵以最大化节点区分度。两种改进方向是正交的：AdaSpec 作为即插即用模块，可以与任何多项式基函数组合，实现叠加增益。

### 理论保证的完备性

AdaSpec 的设计并非启发式拼接，而是有严格理论支撑：Theorem 4.3 给出了节点区分度的下界公式，三个组件分别针对下界公式中的两个因子（$d_M$ 和 $\|\tilde{X}^{(M)}\|_0$）进行优化。此外，Theorem 5.4 和 Proposition 5.5 保证了自适应图矩阵 $\Omega(A, X)$ 与图的自同构群可交换，且增强后的谱 GNN 保持置换等变性——这意味着 AdaSpec 在不破坏谱方法基本对称性的前提下实现了表达能力的提升。



AdaSpec 是一种即插即用的谱增强模块，其设计目标不是替代现有的谱图神经网络，而是通过优化图矩阵来提升节点区分度的理论上界。该模块可无缝嵌入任意遵循通用形式 $`\Psi(M,X) = g_{\Theta}(M) f_W(X)`$ 的谱 GNN 中，其中 $`M`$ 为图矩阵（通常为归一化邻接矩阵 $`\tilde{A}`$ 或归一化拉普拉斯矩阵），$`g_{\Theta}`$ 为多项式谱滤波器，$`f_W`$ 为节点特征变换。

**整体 Pipeline**

AdaSpec 增强的谱 GNN 前向传播流程由三个核心模块串联构成：

1. **特征变换模块（MLP）**：通过可学习权重 $`W`$ 对原始节点特征 $`X`$ 进行线性或非线性变换，输出变换后的特征 $`f_W(X)`$。该模块与标准谱 GNN 完全一致，不引入额外改动。

2. **图矩阵生成模块（AdaSpec $`\Omega`$）**：这是 AdaSpec 的核心创新。该模块以原始邻接矩阵 $`A`$ 和节点特征 $`X`$ 为输入，动态生成自适应图矩阵 $`\Omega(A,X)`$，替代固定的 $`\tilde{A}`$。生成过程由三项可学习/可调节的组件加权求和完成：
   $$`\Omega(A,X) = \Omega_D(A) + \alpha_1 \Omega_S(A) + \alpha_2 \Omega_F(X)`$$
   其中：
   - $`\Omega_D(A) = (D+B)^{-1/2}(A+B)(D+B)^{-1/2}`$：引入可学习的对角偏置矩阵 $`B`$，增加图矩阵的不同特征值数量 $`d_M`$；
   - $`\Omega_S(A) = I`$：通过单位矩阵将所有特征值平移远离零点，减少零特征值重数；
   - $`\Omega_F(X) = \sum_{i=1}^{h} \frac{X_{:i} X_{:i}^{\top}}{\|X_{:i}\|_F^2} \circ A`$：利用节点特征的归一化外积与邻接矩阵的 Hadamard 积，增加节点特征在特征基上的非零频率分量数量 $`\|\tilde{X}^{(M)}\|_0`$。
   
   超参数 $`\alpha_1`$ 和 $`\alpha_2`$ 控制各组件的贡献权重，需通过网格搜索手动调节。$`\Omega_D(A)`$ 中的 $`B`$ 通过梯度下降端到端学习，而 $`\Omega_F(X)`$ 需在训练前预计算（复杂度 $`O(h \cdot |E|)`$，$`h`$ 为特征维度）。

3. **图卷积模块（多项式滤波器 $`g_{\Theta}`$）**：将自适应图矩阵 $`\Omega(A,X)`$ 代入多项式滤波器 $`g_{\Theta}(\cdot)`$ 进行谱域卷积，输出与变换后特征 $`f_W(X)`$ 相乘，得到最终节点嵌入：
   $$`\Psi^+(A,X) = g_{\Theta}(\Omega(A,X)) \, f_W(X)`$$

**模块关系与数据流**

三个模块以严格的串行依赖关系组织：原始图结构 $`A`$ 和节点特征 $`X`$ 分别流入特征变换模块和图矩阵生成模块，二者的输出在卷积模块汇合。图矩阵生成模块不直接与特征变换模块交互，而是通过改变 $`g_{\Theta}`$ 的谱作用域来间接影响最终的嵌入表达。这种解耦设计使得 AdaSpec 可以作为插件嵌入 ChebNet、ChebNetII、JacobiConv、GPRGNN、BernNet 等不同多项式基的谱 GNN，无需修改其后端架构。

**理论保证与计算开销**

从理论层面，上述三组件直接作用于区分度下界 $`\min(d_M, \|\tilde{X}^{(M)}\|_0)`$：$`\Omega_D`$ 提升 $`d_M`$，$`\Omega_S`$ 防止零特征值重数侵蚀下界，$`\Omega_F`$ 提升 $`\|\tilde{X}^{(M)}\|_0`$。Theorem 4.3 证明，存在谱 GNN 可区分至少 $`\min(d_M, \|\tilde{X}^{(M)}\|_0)`$ 个节点，因此优化 $`\Omega`$ 直接提升可区分节点数的理论上界。

在计算开销方面，AdaSpec 增强的谱 GNN 与原始谱 GNN 的前向和反向传播时间复杂度同阶（Table 1）。主要额外开销来自 $`\Omega_F(X)`$ 的预计算，对于特征维度极高或边数极大的图可能引入不可忽略的一次性成本（如 Coauthor-Physics 数据集预计算时间达 12.44 秒），但训练过程中的额外开销极小，甚至在某些大数据集上因更快的收敛而缩短总训练时间（Table 6）。

**置换等变性保持**

AdaSpec 增强的谱 GNN 保持置换等变性：Theorem 5.4 证明 $`\Omega(A,X)`$ 与图自同构群 $`\text{Aut}(G)`$ 可交换，Proposition 5.5 进一步保证当 $`f_W`$ 满足置换等变性时，$`\Psi^+(A,X)`$ 整体置换等变。这意味着节点重排仅导致嵌入的对应重排，不会破坏图的结构一致性。

**局限性**

当前框架仅在节点分类任务上验证有效，尚未拓展至图分类或链接预测。$`\alpha_1`$、$`\alpha_2`$ 缺乏自动选择机制，需手动调参。当训练与测试的特征分布不一致时，特征自适应的 $`\Omega_F(X)`$ 可能引入过拟合风险。



### 谱图神经网络的一般形式

AdaSpec 的增强对象是谱图神经网络（Spectral GNN），其一般形式为：

$$\Psi(M, X) = g_{\Theta}(M) f_W(X) \tag{1}$$

其中 $M$ 为图矩阵（通常为归一化邻接矩阵 $\tilde{A} = D^{-1/2} A D^{-1/2}$ 或归一化拉普拉斯矩阵），$g_{\Theta}(M)$ 是作用在图矩阵上的多项式谱滤波器，$f_W(X)$ 是对节点特征 $X$ 的可学习特征变换（通常为 MLP）。该形式将图卷积分解为谱域滤波与特征变换两个独立模块。

### AdaSpec 增强的谱 GNN

AdaSpec 的核心思想是用一个自适应生成的图矩阵 $\Omega(A, X)$ 替换固定的 $M$，从而提升节点区分度的理论上界。增强后的谱 GNN 定义为：

$$\Psi^+(A, X) = g_{\Theta}(\Omega(A, X)) f_W(X) \tag{2}$$

其中 $\Omega(A, X)$ 同时依赖于图结构 $A$ 和节点特征 $X$，作为一个即插即用的模块嵌入任意谱 GNN 中，无需修改原有的多项式基底或特征变换结构。

### 自适应图矩阵生成

$\Omega(A, X)$ 由三个功能互补的组件加权组合而成：

$$\Omega(A, X) = \Omega_D(A) + \alpha_1 \Omega_S(A) + \alpha_2 \Omega_F(X) \tag{3}$$

其中 $\alpha_1, \alpha_2$ 为可调节的超参数，控制各组件的贡献权重。三个组件分别针对节点区分度下界的不同瓶颈：

- **$\Omega_D(A)$**：增加不同特征值的数量 $d_M$；
- **$\Omega_S(A)$**：将零特征值移离零，减少零特征值重数；
- **$\Omega_F(X)$**：利用节点特征信息增加非零频率分量的数量 $\|\tilde{X}^{(M)}\|_0$。

这三者共同提升区分度下界 $\min(d_M, \|\tilde{X}^{(M)}\|_0)$（Theorem 4.3）。

### 组件一：增加不同特征值的 $\Omega_D(A)$

$$\Omega_D(A) = (D + B)^{-1/2}(A + B)(D + B)^{-1/2}$$

其中 $B = \text{diag}(b_1, b_2, \ldots, b_{|V|})$ 是一个可学习的对角矩阵，为每个节点引入独立的偏置项。$D$ 为度矩阵，$A$ 为邻接矩阵。该设计通过节点级别的偏置扰动打破了原始图矩阵的对称性约束，从而显著增加不同特征值的数量。当 $B = 0$ 时退化为标准归一化邻接矩阵 $\tilde{A}$，当 $B = I$ 时退化为带自环的版本 $\hat{A}$。

### 组件二：移除零特征值的 $\Omega_S(A)$

$$\Omega_S(A) = I$$

该组件直接取单位矩阵 $I$，将其加到图矩阵上等价于对所有特征值进行平移操作。由于单位矩阵与原图矩阵共享相同的特征向量空间，该操作在不改变特征基的前提下将零特征值移离零，减少零特征值的重数，从而缓解因零特征值导致的信息湮灭问题。

### 组件三：特征自适应的 $\Omega_F(X)$

$$\Omega_F(X) = \sum_{i=1}^{h} \frac{X_{:i} X_{:i}^{\top}}{\|X_{:i}\|_F^2} \circ A$$

其中 $X_{:i}$ 表示节点特征矩阵 $X$ 的第 $i$ 列（第 $i$ 个特征维度），$h$ 为特征维度数，$\circ$ 表示 Hadamard 积（逐元素乘积）。该组件计算每个特征维度的归一化外积矩阵，与邻接矩阵 $A$ 逐元素相乘后求和。其作用是引入特征空间的结构信息，增加节点特征在谱域中非零频率分量的数量，从而提升区分度下界中 $\|\tilde{X}^{(M)}\|_0$ 这一项。

### 理论保证

**节点区分度下界**（Theorem 4.3）：对于任意谱 GNN $\Psi(M, X)$，其输出矩阵的秩满足：

$$\text{rank}(\Psi(M, X)) \geq \min(d_M, \|\tilde{X}^{(M)}\|_0)$$

其中 $d_M$ 为图矩阵 $M$ 的不同特征值个数，$\|\tilde{X}^{(M)}\|_0$ 为节点特征在 $M$ 的特征基上投影后非零频率分量的数量。该下界直接决定了模型能区分的节点数上限——当两个量中任一较小时，模型便无法为非同构节点产生不同嵌入。AdaSpec 的三个组件分别从这两个维度提升该下界，从而在理论上保证区分能力的增强。

**置换等变性**（Proposition 5.5）：当 $f_W$ 满足置换等变性时，使用 AdaSpec 增强的谱 GNN $\Psi^+(A, X)$ 保持置换等变性，即图节点的重排会导致节点嵌入的相应重排，保证了模型对图同构的不变性。



## 实验与关键发现

### 整体性能提升

AdaSpec 在 18 个节点分类基准上对 5 种谱 GNN 骨干（ChebNet、ChebNetII、JacobiConv、GPRGNN、BernNet）进行了系统性验证。核心结论如下：

**异配图上的显著增益。** Table 2 和 Table 9 汇总了 AdaSpec 在异配数据集上的表现。在小规模异配图上，AdaSpec 使平均准确率提升 **1.89%**；在大规模异配图上，平均 ROC AUC 提升 **1.27%**。典型案例包括：
- Texas 数据集上 ChebNet(M) 达到 51.16±8.56%，较 ChebNet(O) 的 38.67±9.31% 提升 **+12.49%**（Table 2）。
- Roman_Empire 数据集上 ChebNet(M) 达到 54.55±0.3%，较 ChebNet(O) 的 47.15±0.42% 提升 **+7.4%**（Table 9）。
- Minesweeper 数据集上 JacobiConv(M) 的 ROC AUC 达到 89.13±0.1%，较 JacobiConv(O) 的 87.34±0.12% 提升 **+1.79%**（Table 2）。

![[assets/figures/papers/paper_list_l3_AdaSpec_Adaptive_Spectrum_for_Enhanced_Node_Distinguishability/figures/008_Table_2.jpg]]
*Table 2: Performance of spectral GNNs with/without AdaSpec on heterophilic datasets. ROC AUC is reported on Minesweeper, Questions. Testing accuracy is reported on other datasets. High accuracy and ROC AUC indicate good performance*

![[assets/figures/papers/paper_list_l3_AdaSpec_Adaptive_Spectrum_for_Enhanced_Node_Distinguishability/figures/035_Table_9.jpg]]
*Table 9: Performance with/without AdaSpec on large heterophilic datasets (Roman_Empire, Amazon_Ratings, Tolokers, Minesweeper, Questions ). Test accuracy is used as the metric for Roman-Empire and Amazon-Ratings datasets and ROC AUC is reported on Minesweeper, Tolokers, Questions. High accuracy and ROC AUC indicate good performance*

**同配图上的稳定保持。** Table 3 显示，AdaSpec 在同配数据集上平均准确率提升 **0.43%**，未出现性能退化。例如 Cora 上 ChebNet(M) 为 81.01±1.11%，较 ChebNet(O) 的 80.45±1.09% 微增 +0.56%。这表明 AdaSpec 在不损害同配图性能的前提下，大幅改善了异配场景的区分能力。

![[assets/figures/papers/paper_list_l3_AdaSpec_Adaptive_Spectrum_for_Enhanced_Node_Distinguishability/figures/009_Table_3.jpg]]
*Table 3: Test accuracy of spectral GNNs with/without AdaSpec on homophilic datasets. High accuracy indicates good performance*

### 消融实验：各组件的贡献

Table 4 以 ChebNet 为骨干，逐一剥离 AdaSpec 的三个组件进行消融。核心发现：

![[assets/figures/papers/paper_list_l3_AdaSpec_Adaptive_Spectrum_for_Enhanced_Node_Distinguishability/figures/010_Table_4.jpg]]
*Table 4: Test accuracy of ChebNet with different components of AdaSpec across datasets that $\Omega$ ( A , X ) contains all three components*

- **Ω_D(A)（增加不同特征值）** 在异配图上贡献最大。例如 Texas 上单独使用 Ω_D(A) 即可将准确率从 38.67% 提升至 47.08%，接近全组件版本的 51.16%。
- **Ω_S(A)（零特征值平移）** 在大规模数据集（如 Roman_Empire、Amazon_Ratings）上有额外增益，单独使用时分别带来约 +2.5% 和 +1.3% 的提升。
- **Ω_F(X)（特征自适应频率分量）** 单独使用时效果有限，但与 Ω_D(A) 和 Ω_S(A) 联合使用时能产生协同效应，使全组件版本在所有数据集上达到最优。
- **全组件组合** 一致取得最佳性能，验证了三个机制在提升节点区分度上的互补性。

### 理论动机的实证验证

**不同特征值数量的直接证据。** Table 5 量化了 Ω_D(A) 对图矩阵不同特征值数量 $d_M$ 的影响。在所有测试数据集上，$d_{\Omega_D(A)}$ 均显著高于原始归一化邻接矩阵的 $d_{\tilde{A}}$：
- Texas：$d_{\tilde{A}}=113 \rightarrow d_{\Omega_D(A)}=181$（节点总数 $|V|=183$，几乎达到理论上限）
- Cornell：$d_{\tilde{A}}=122 \rightarrow d_{\Omega_D(A)}=144$
- Citeseer：$d_{\tilde{A}}=1071 \rightarrow d_{\Omega_D(A)}=1670$

![[assets/figures/papers/paper_list_l3_AdaSpec_Adaptive_Spectrum_for_Enhanced_Node_Distinguishability/figures/011_Table_5.jpg]]
*Table 5: Number of distinct eigenvalues of the graph matrix. |V| denotes the number of nodes in graphs. $d _ { \tilde { A } }$ and $d _ { \Omega _ { D } ( A ) }$ are numbers of distinct eigenvalues of A˜ and $\Omega _ { D }$ ( A ) in AdaSpec respectively

这直接验证了 Theorem 4.3 的核心机制：增加不同特征值数量 $d_M$ 可提升节点区分度下界 $\min(d_M, \|\tilde{X}^{(M)}\|_0)$。

### 计算开销分析

**时间复杂度同阶。** Table 1 的理论分析表明，AdaSpec 增强的谱 GNN 在正向和反向传播中的时间复杂度与原始版本保持同阶（均为 $O(KT|E| + |V||W|)$），未引入额外的高阶项。

**实际训练时间。** Table 6 的实测数据表明 AdaSpec 的实际开销极小：
- 在大规模异配图上，ChebNet(M) 的训练时间甚至略快于 ChebNet(O)（Roman_Empire 上 1.88s vs 1.93s，Amazon_Ratings 上 1.35s vs 1.91s），这归因于 AdaSpec 优化后的图矩阵加速了收敛。
- Ω_F(X) 的预计算开销与图规模相关：Amazon_Ratings 仅需 0.03s，而 Coauthor-Physics 需 12.44s。对于特征维度极高或边数极大的图，这一一次性开销需纳入考虑。

### 与图扩散方法的正交性

Table 10 展示了 AdaSpec 与图扩散卷积（GDC）的组合效果。在 9 个基准上，GDC+ChebNet(M) 在 7 个数据集上取得最优结果。典型增益包括 Chameleon 上 +10.32%、Cornell 上 +6.41%。这证明 AdaSpec 的频谱增强机制与基于空间扩散的图重连方法相互正交、可叠加使用。

![[assets/figures/papers/paper_list_l3_AdaSpec_Adaptive_Spectrum_for_Enhanced_Node_Distinguishability/figures/036_Table_10.jpg]]
*Table 10: Impact of AdaSpec applied on top of GDC. Our method (GDC + ChebNet(M)) consistently improves performance across most benchmarks. Three configurations: (1) Standard ChebNet ( ChebNet(O) ), (2) ChebNet with GDC ( GDC+ChebNet(O) ), and (3) ChebNet with GDC + AdaSpec ( GDC+ChebNet(M) )*

### 失败模式与局限性

1. **特征分布偏移风险。** Ω_F(X) 直接依赖节点特征构造 Hadamard 积项。当训练集特征分布与测试集不一致时，自适应图矩阵可能过拟合训练分布，导致泛化下降。目前缺乏对此风险的系统性消融。

2. **高维特征的预计算瓶颈。** 在 Coauthor-Physics 等特征维度高、边数大的图上，Ω_F(X) 的预计算时间达 12.44s（Table 6），可能成为大规模应用的单次负担。

3. **超参数敏感性。** α₁ 和 α₂ 需通过网格搜索手动调节，当前未提供自动选择机制，增加了不同数据集上的调参成本。

4. **任务范围有限。** 目前仅在节点分类任务上验证，尚未在图分类、链接预测等任务上评估 AdaSpec 的迁移能力。



## 定位与知识库关联

### 谱图神经网络中的图矩阵优化路径

AdaSpec 在谱 GNN 方法谱系中占据一个独特的位置：它不改变多项式基函数的选择，而是直接优化图矩阵本身。传统谱 GNN 的演进主要围绕多项式基的设计展开——ChebNet 使用切比雪夫多项式，GPRGNN 使用单项式基，BernNet 使用伯恩斯坦基，JacobiConv 使用雅可比基——但所有这些方法都共享同一个固定的归一化邻接矩阵 $\tilde{A} = D^{-1/2} A D^{-1/2}$ 作为谱域变换的基础。AdaSpec 识别出这一被忽视的优化维度：图矩阵的特征值分布和频率分量映射直接决定了节点区分度的理论上界 $\min(d_M, \|\tilde{X}^{(M)}\|_0)$，而固定矩阵 $\tilde{A}$ 在这两个维度上远未达到最优。

从因果机制看，AdaSpec 的三项设计 $\Omega_D(A)$、$\Omega_S(A)$、$\Omega_F(X)$ 分别对应三个可操作的瓶颈：不同特征值数量 $d_M$ 不足（通过可学习对角偏置 $B$ 增加）、零特征值重数过高（通过单位矩阵平移）、以及节点特征在特征基上非零频率分量缺失（通过特征自适应 Hadamard 积补充）。Table 5 的实证证据直接验证了这一机制：$\Omega_D(A)$ 将 Texas 数据集的不同特征值数从 113 提升至 181，接近节点总数 $|V|=183$，为区分度提升提供了结构基础。

### 与图重连方法的互补关系

AdaSpec 明确将自己定位为谱增强模块而非图重连（graph rewiring）的竞争者。图重连方法通过修改图的拓扑结构来改善消息传递，而 AdaSpec 在谱域操作图矩阵，两者作用于不同层面。Table 10 的正交性实验证实了这种互补性：在图扩散卷积（GDC）预处理的基础上叠加 AdaSpec，能在多数基准上获得进一步增益，表明谱增强和图拓扑优化可以协同工作。这一特性使 AdaSpec 成为现有 GNN 管线中的即插即用组件，而非需要替代现有预处理步骤的方法。

### 适用边界与性能特征

AdaSpec 的增益在不同图类型上呈现显著分化。在异配图（heterophilic graphs）上，AdaSpec 带来的提升最为突出：ChebNet 在 Texas 上提升 12.49 个百分点（38.67% → 51.16%），在 Roman_Empire 上提升 7.4 个百分点（47.15% → 54.55%）。在同配图（homophilic graphs）上，增益较为温和，平均提升约 0.43 个百分点，部分数据集上仅维持原有性能。这一分化与理论预期一致：异配图中节点特征与局部结构的相关性较弱，固定图矩阵的频率分量缺失问题更为严重，因此自适应调整的边际效用更大。当图矩阵的特征值分布本身已经较为“饱满”时（如部分高连通性同配图），AdaSpec 的优化空间受限。

### 已知局限

**任务覆盖范围有限。** 目前 AdaSpec 仅在节点分类任务上进行了验证，尚未在图分类、链接预测等需要图级或边级表示的任务上评估其有效性。节点区分度的理论框架直接服务于节点级表示学习，向图级任务的推广需要额外的聚合理论支撑。

**$\Omega_F(X)$ 的预计算开销。** 特征自适应项 $\Omega_F(X) = \sum_i \frac{X_{:i} X_{:i}^\top}{\|X_{:i}\|_F^2} \circ A$ 的预计算复杂度为 $O(h \cdot |E|)$，其中 $h$ 为特征维度。在 Coauthor-Physics 数据集上，这一预计算耗时 12.44 秒，对于特征维度极高或边数极大的图可能引入不可忽略的一次性开销。不过 Table 6 显示，训练阶段的总体时间并未显著增加，且在部分大数据集上 AdaSpec 版本反而收敛更快（Roman_Empire 上 ChebNet(M) 1.88s vs ChebNet(O) 1.93s）。

**特征分布偏移风险。** 自适应矩阵 $\Omega(A,X)$ 依赖于节点特征 $X$，当训练数据覆盖的特征分布与测试时特征分布不一致时，存在过拟合风险。论文未提供跨分布泛化实验，这一风险点需要在实际部署中通过验证集监控。

**超参数选择未自动化。** 权重系数 $\alpha_1$ 和 $\alpha_2$ 控制 $\Omega_S(A)$ 和 $\Omega_F(X)$ 的贡献比例，目前依赖手动调节或网格搜索，增加了调参负担。论文未提出基于图特性（如同配性度量）的自动选择机制。

### 开放问题

1. **向非谱 GNN 的推广。** AdaSpec 的核心思想——通过优化图矩阵的特征值分布和频率映射来增强节点区分度——是否可推广到基于注意力机制或消息传递的非谱模型？这需要建立谱域分析与非谱模型表达能力之间的桥梁。

2. **动态图场景下的增量更新。** 对于结构随时间变化的动态图或流式图，如何高效更新 $\Omega(A,X)$ 而不重新计算整个矩阵的特征分解？$\Omega_D(A)$ 的可学习偏置 $B$ 可能需要设计增量学习策略。

3. **区分度下界的紧致性。** Theorem 4.3 给出的下界 $\min(d_M, \|\tilde{X}^{(M)}\|_0)$ 是否可以通过联合优化多项式基底和图矩阵进一步紧致？当前 AdaSpec 仅优化图矩阵端，多项式基的选择仍独立进行。

4. **边际效用的自适应判断。** 当图矩阵的特征值分布已经接近满秩时，AdaSpec 是否还能带来显著增益？能否设计一个轻量级的预检机制，在训练前判断 AdaSpec 的预期边际效用，从而避免不必要的计算开销？

5. **与图同配性度量的理论关联。** AdaSpec 在异配图上的显著增益暗示其机制与图的同配性/异配性存在深层关联。建立 $\Omega(A,X)$ 的优化效果与同配性度量（如边同配率）之间的定量关系，可为超参数 $\alpha_1, \alpha_2$ 的自动选择提供理论依据。



## 原文 PDF

![[paperPDFs/ICLR_2026/AdaSpec_Adaptive_Spectrum_for_Enhanced_Node_Distinguishability.pdf]]
