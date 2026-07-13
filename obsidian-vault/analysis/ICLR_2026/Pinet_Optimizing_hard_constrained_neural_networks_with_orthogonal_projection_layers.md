---
title: "Pinet: Optimizing hard-constrained neural networks with orthogonal projection layers"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Pinet_Optimizing_hard_constrained_neural_networks_with_orthogonal_projection_layers.pdf
project_link: null
code_link: https://github.com/antonioterpin/pinet
openreview_forum_id: EJ680UQeZG
aliases:
- Pinet
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "将投影表示为一个固定点迭代，并应用隐函数定理进行高效反向传播，同时使用Douglas-Rachford算子分裂算法实现快速且精确的投影。"
primary_logic: "在神经网络输出后附加一个可微的正交投影层，利用Douglas-Rachford算子分裂快速计算投影，并通过隐函数定理和双共轭梯度法实现高效反向传播，从而在保证约束严格满足的同时，大幅提升训练和推理效率。"
claims:
- "Πnet利用算子分裂进行前向投影，并利用隐函数定理进行反向传播，在训练时间、解质量和超参数鲁棒性上比现有学习方法高出数个量级。"
- "在非凸问题上，Πnet在测试集上达到CV≤1e-3且RS≤5%的最优阈值，而DC3和JAXopt未能达标或无法训练。"
- "在大规模问题（d=1000）上，DC3和JAXopt要么发散要么训练极慢，而Πnet仅用50个epoch便获得高质量解。"
- "消融实验表明，矩阵均衡化和自动调谐将所需前向迭代次数从100/350降至50，同时显著降低约束违反。"
---

# Pinet: Optimizing hard-constrained neural networks with orthogonal projection layers

> [!tip] 核心洞察
> 在神经网络输出后附加一个可微的正交投影层，利用Douglas-Rachford算子分裂快速计算投影，并通过隐函数定理和双共轭梯度法实现高效反向传播，从而在保证约束严格满足的同时，大幅提升训练和推理效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Πnet：利用正交投影层优化硬约束神经网络 |
| 英文题名 | Pinet: Optimizing hard-constrained neural networks with orthogonal projection layers |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=EJ680UQeZG) · [GitHub](https://github.com/antonioterpin/pinet) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Πnet |
| Dataset | small non-convex (d=100), small convex (d=100) |

> [!tip] 效果简介
> - small non-convex (d=100) 上，Average Relative Suboptimality (RS) 为 0.00216 (Πnet)，对比 0.02178 (Πnet-inf, 仅在测试时投影)，变化 改善约10×。
> - small non-convex (d=100) 上，Single inference time (s) 为 0.0052 (CPU)，对比 0.0120 (cvxpylayers CPU)，变化 约2.3×加速。
> - small non-convex (d=100) 上，Batch inference time (s) for 1024 instances 为 0.0135 (GPU)，对比 2.5917 (cvxpylayers GPU)，变化 约192×加速。

## 概要

在参数化约束优化问题中，给定上下文 $\mathbf{x}$，需在凸可行集 $\mathcal{C}(\mathbf{x})$ 上最小化目标函数 $\varphi(y, \mathbf{x})$。传统硬约束神经网络通过循环展开前向投影迭代进行训练，导致训练时间和内存开销巨大；软约束方法则无法保证解严格可行。Πnet 提出了一种可微的正交投影输出层，将骨干网络不可行的原始输出 $y_{\mathrm{raw}}$ 投影到可行集上，即 $y = \Pi_{\mathcal{C}(\mathbf{x})}(y_{\mathrm{raw}})$，从而保证输出始终满足约束。

其核心机制包含两个关键设计：前向传播中，利用 Douglas-Rachford 算子分裂算法快速计算投影，充分利用约束集可分解为超平面 $\mathcal{A}$ 与笛卡尔积 $\mathcal{K}$ 的结构（$\mathcal{C} = \Pi_d(\mathcal{A} \cap \mathcal{K})$），两者的投影均可闭式求解；反向传播中，不展开迭代过程，而是将投影视为固定点迭代，通过隐函数定理和双共轭梯度稳定法（bicgstab）高效计算向量-雅可比乘积，大幅降低训练开销。

实验表明，Πnet 在训练时间、解质量和超参数鲁棒性上比现有学习方法高出数个量级。在非凸问题上，Πnet 是唯一能在测试集上达到相对次优性 $\mathrm{RS} \leq 5\%$ 且约束违反 $\mathrm{CV} \leq 10^{-3}$ 最优阈值的方法；在大规模问题（$d=1000$）上，DC3 发散、JAXopt 训练极慢，而 Πnet 仅用 50 个 epoch 即获得高质量解。推理速度方面，Πnet 在批量推理中比 cvxpylayers 快约 192 倍，比 OSQP 快约 149 倍。消融实验进一步验证了矩阵均衡化与自动调谐将所需前向迭代次数从 100–350 次降至 50 次，且训练期间执行投影比仅在推理时投影将相对次优性提高一个数量级。



### 问题设定：参数化约束优化

许多决策问题可形式化为参数化约束优化问题：给定上下文 $\mathbf{x}$，在凸可行集 $\mathcal{C}(\mathbf{x})$ 上最小化目标函数 $\varphi$：

$$
\operatorname*{minimize}_{y} \varphi(y, \mathbf{x}) \quad \mathrm{subject~to} \quad y \in \mathcal{C}(\mathbf{x})
$$

其中 $y \in \mathbb{R}^d$ 为决策变量，$\mathcal{C}(\mathbf{x})$ 是由线性等式和不等式约束定义的凸多面体。这类问题广泛存在于模型预测控制、运动规划、资源分配等场景，其核心挑战在于：当上下文 $\mathbf{x}$ 快速变化时，需要实时或批量地产生高质量可行解。

### 现有方法缺口

**传统求解器**（如 OSQP、IPOPT）对每个问题实例独立求解，精度高但速度慢，尤其在批量场景下无法利用 GPU 并行加速，难以满足实时性要求。

**软约束学习方法**通过在损失函数中引入惩罚项来鼓励约束满足，但无法保证解严格可行，且惩罚系数的调谐极为敏感。**DC3** 等硬约束方法在推理时通过等式完成和不等式校正过程修正不可行输出，但由于训练时缺乏约束反馈，解质量显著受限——在非凸基准上，仅在推理时投影的 Πnet-inf 的相对次优性（RS）为 0.02178，而训练时即强制执行投影的 Πnet 达到 0.00216，改善约一个数量级。

**隐式层方法**（如 cvxpylayers、JAXopt 中的 OSQP 隐式层）将优化求解器嵌入神经网络作为可微层。这类方法的瓶颈在于：

1. **前向投影效率低**：通用求解器未针对投影问题的特殊结构定制，单次推理时间在 CPU 上为 0.0120 s（cvxpylayers），批量 GPU 推理更是高达 2.5917 s。
2. **反向传播开销巨大**：传统方法需循环展开前向投影迭代（如 Dykstra 算法）来计算梯度，导致训练时间和内存开销随迭代次数线性增长；或对求解器进行隐式微分，但未能针对投影问题定制算法，在大规模问题（$d=1000$）上训练极慢甚至发散。
3. **超参数敏感**：软约束惩罚系数和求解器参数需要大量调谐，且在不同问题规模下泛化性差。

### 核心瓶颈与本文动机

传统硬约束神经网络面临一个根本性困境：**保证约束严格满足需要循环展开投影迭代，导致训练成本不可承受；而避免展开则无法利用约束结构进行有效学习**。这一瓶颈的因果链条如下：

- 前向投影本质是一个固定点迭代过程，传统反向传播必须记录完整迭代轨迹，计算图随迭代次数膨胀。
- 软约束方法绕过此问题，但以牺牲可行性和解质量为代价。
- 现有隐式层方法虽支持隐式微分，但依赖通用求解器，既未利用投影问题的分解结构加速前向计算，也未针对固定点方程定制线性系统求解策略。

Πnet 的核心动机正是打破这一困境：**将投影表示为一个固定点迭代，并应用隐函数定理进行高效反向传播，同时使用 Douglas-Rachford 算子分裂算法实现快速且精确的投影**。通过在神经网络输出后附加一个可微的正交投影层，Πnet 在保证约束严格满足的同时，大幅提升训练和推理效率——在非凸基准上，Πnet 以仅 50 个 epoch 的训练即超越 DC3 在 1000 个 epoch 下的解质量，且批量推理速度较 cvxpylayers 加速约 192 倍（GPU）。



## 核心方法与创新机理

Πnet 的核心创新在于将传统硬约束神经网络中“投影—反向传播”这一对偶过程进行了根本性的重构，解决了长期以来训练效率与约束可行性之间的尖锐矛盾。其关键洞察在于：**将投影操作视为一个固定点迭代，并利用隐函数定理进行高效的反向传播，从而避免了对前向迭代的循环展开**。

具体而言，Πnet 在以下三个关键环节实现了突破：

### 1. 前向投影：定制的算子分裂算法

传统方法通常依赖通用优化求解器（如 OSQP）或未经专门优化的投影算法。Πnet 则充分利用约束集合的结构特性，将其分解为超平面与笛卡尔积的交集形式 $\mathcal{C} = \Pi_d(\mathcal{A} \cap \mathcal{K})$，其中 $\Pi_{\mathcal{A}}$ 和 $\Pi_{\mathcal{K}}$ 均具有闭式解。基于此分解，Πnet 采用 **Douglas-Rachford 算子分裂算法**（Algorithm 1）实现快速且精确的投影，其近端算子均可显式计算。这种定制化设计使得 Πnet 在推理速度上较通用求解器 OSQP 快约 149 倍，较 JAXopt 快约 12 倍（Table 3）。

### 2. 反向传播：隐函数定理替代循环展开

这是 Πnet 最关键的创新。传统硬约束方法在反向传播时需要对前向投影迭代进行循环展开，导致训练时间和内存开销巨大。Πnet 另辟蹊径，将投影层的固定点迭代视为一个隐式方程，应用**隐函数定理**直接计算向量-雅可比乘积（VJP），并通过双共轭梯度稳定法（bicgstab）近似求解由此产生的线性系统。这一设计使得反向传播的计算复杂度与投影迭代次数解耦，大幅降低了训练开销，同时保持了严格的可微性。

### 3. 训练范式：投影层嵌入训练循环

与仅在推理时进行投影校正的软约束方法（如 DC3 的等式完成/不等式校正）不同，Πnet 将投影层作为网络的可微组成部分嵌入训练循环中。消融实验表明，在训练期间执行投影（Πnet）相比仅在推理时投影（Πnet-inf），相对次优性（RS）提升了一个数量级（从 0.02178 降至 0.00216），验证了“训练即投影梯度下降”这一范式在解质量上的显著优势。

此外，Πnet 引入了**矩阵均衡化**（Ruiz 均衡化）和**超参数自动调谐**两项辅助技术，改善了线性系统的条件数，将所需前向迭代次数从默认的 100 次或自动调谐的 350 次降至 50 次，同时显著降低约束违反（Figure 16, Table 6）。

综上，Πnet 通过“算子分裂前向投影 + 隐函数定理反向传播”这一核心机制，在严格保证约束满足的前提下，实现了训练效率和解质量的双重飞跃，在非凸问题上成功达到 $\text{CV} \leq 10^{-3}$ 且 $\text{RS} \leq 5\%$ 的最优性阈值，而 DC3 和 JAXopt 未能达标或无法训练（Figure 2）。



![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of the Πnet architecture. The infeasible output of the backbone network is projected onto the feasible set through an operator splitting scheme. To train the backbone network, we use the implicit function theorem to backpropagate the loss through the projection layer*

Πnet 的整体设计遵循“预测-投影”范式，其核心思想是在任意骨干网络之后附加一个可微的正交投影层，从而将硬约束满足问题从网络学习过程中解耦。如 Figure 1 所示，框架由三个关键模块串联构成：

**骨干网络**：一个可任意替换的多层感知机（MLP），以上下文变量 $\mathbf{x}$ 为输入，输出一个未经约束处理的原始决策变量 $y_{\mathrm{raw}}$。该网络不感知约束的存在，仅负责学习从上下文到高质量解候选的映射。

**投影层（前向传播）**：将 $y_{\mathrm{raw}}$ 正交投影到由 $\mathbf{x}$ 参数化的可行集 $\mathcal{C}(\mathbf{x})$ 上，得到严格满足约束的输出 $y$：
$$y = \Pi_{\mathcal{C}(\mathbf{x})}(y_{\mathrm{raw}}) = \operatorname{argmin}_{z \in \mathcal{C}(\mathbf{x})} \|z - y_{\mathrm{raw}}\|^2$$
投影计算采用定制的 **Douglas-Rachford 算子分裂算法**（Algorithm 1），充分利用约束集的分解结构——将 $\mathcal{C}$ 表示为超平面 $\mathcal{A}$ 与盒约束 $\mathcal{K}$ 的交集投影，其中 $\Pi_{\mathcal{A}}$ 和 $\Pi_{\mathcal{K}}$ 均具有闭合形式的解析解。该设计使前向投影迭代快速且可靠，无需调用通用优化求解器。

**隐式反向传播模块**：训练时，损失 $\mathcal{L}$ 需要沿 $y \to y_{\mathrm{raw}} \to \theta$ 的路径回传梯度。Πnet 不通过循环展开前向迭代来求导，而是利用 **隐函数定理** 将投影层的向量-雅可比乘积（VJP）转化为求解一个线性系统：
$$\left( I - \frac{\partial \Phi(s, y_{\mathrm{raw}})}{\partial s} \right)^\top \xi(y_{\mathrm{raw}}, v) = v$$
该线性系统采用 **双共轭梯度稳定法（bicgstab）** 近似求解，从而避免了展开迭代带来的内存和计算开销。

**辅助模块**：为提升数值稳定性和收敛效率，Πnet 引入了 **Ruiz 矩阵均衡化** 以改善约束矩阵的条件数，并通过 **自动调谐** 机制自适应选择 Douglas-Rachford 的超参数 $\sigma$ 和迭代次数。消融实验表明，均衡化与自动调谐可将所需前向迭代次数从默认的 100 次（或未调谐时的 350 次）降至约 50 次，同时显著降低约束违反量（Figure 16, Table 6）。

整个 pipeline 的输入输出流为：上下文 $\mathbf{x}$ → 骨干网络 → $y_{\mathrm{raw}}$ → 投影层（Douglas-Rachford 固定点迭代）→ 可行解 $y$ → 损失函数。训练时，梯度沿反向路径通过隐式微分回传至骨干网络参数 $\theta$（Algorithm 2, 3）。该框架与骨干网络架构解耦，可灵活附加于任意神经网络之后。



Πnet 的核心架构由一个骨干网络与一个可微的正交投影层串联而成。骨干网络（通常为 MLP）将上下文 $\mathbf{x}$ 映射为原始输出 $y_{\mathrm{raw}}$，该输出可能违反约束；投影层则将其严格投影到可行集 $\mathcal{C}(\mathbf{x})$ 上，得到可行输出 $y$。

### 投影层的前向传播：Douglas-Rachford 算子分裂

投影层的数学定义为正交投影：

$$y = \Pi_{\mathcal{C}(\mathbf{x})}(y_{\mathrm{raw}}) = \operatorname{argmin}_{z \in \mathcal{C}(\mathbf{x})} \|z - y_{\mathrm{raw}}\|^2$$

为高效计算该投影，Πnet 将约束集分解为 $\mathcal{C} = \Pi_d(\mathcal{A} \cap \mathcal{K})$，其中 $\mathcal{A}$ 为超平面（编码等式约束），$\mathcal{K}$ 为盒约束的笛卡尔积（编码不等式与变量边界）。两者均具有闭式投影算子，因此可采用 Douglas-Rachford 算子分裂算法进行固定点迭代：

$$z_{k+1} = \mathrm{prox}_{\sigma g}(s_k)$$
$$t_{k+1} = \operatorname{prox}_{\sigma h}(2 z_{k+1} - s_k)$$
$$s_{k+1} = s_k + \omega (t_{k+1} - z_{k+1})$$

其中 $g$ 为 $\mathcal{A}$ 的指示函数，$h$ 为数据项与 $\mathcal{K}$ 的指示函数之和，$\sigma$ 和 $\omega$ 为算法超参数。上述近端算子均可显式计算，使得前向投影迭代高效且可靠。

### 投影层的反向传播：隐函数定理

传统做法需循环展开前向迭代以进行反向传播，导致训练时间和内存开销巨大。Πnet 利用隐函数定理规避此问题：将投影视为固定点迭代 $\Phi(s, y_{\mathrm{raw}})$ 的不动点 $s_{\infty}$，则向量-雅可比乘积（VJP）可解析表达为：

$$v \mapsto \xi(y_{\mathrm{raw}}, v)^\top \frac{\partial \Phi(s_{\infty}(y_{\mathrm{raw}}), y_{\mathrm{raw}})}{\partial y_{\mathrm{raw}}}$$

其中辅助向量 $\xi$ 通过求解以下线性系统得到：

$$\left( I - \frac{\partial \Phi(s, y_{\mathrm{raw}})}{\partial s} \right)^\top \xi(y_{\mathrm{raw}}, v) = v$$

Πnet 采用双共轭梯度稳定法（bicgstab）对该线性系统进行近似求解，从而以常数内存开销和远低于循环展开的计算成本完成反向传播。

### 矩阵均衡化与自动调谐

投影层中约束矩阵的条件数直接影响 Douglas-Rachford 迭代的收敛速度。Πnet 引入 Ruiz 矩阵均衡化预处理以改善条件数，并设计了自动调谐机制为 $\sigma$ 和迭代次数选择合适的值。消融实验表明，均衡化与自动调谐可将所需前向迭代次数从默认的 100 次（或未调谐时的 350 次）降至 50 次，同时显著降低约束违反量。



## 实验与关键发现

### 核心瓶颈与因果机制

传统硬约束神经网络面临一个根本性训练瓶颈：反向传播时需要循环展开前向投影迭代，导致训练时间和内存开销巨大。软约束方法通过惩罚项规避了这一问题，但无法保证解的可行性，且不能利用约束结构。现有隐式层方法（如JAXopt）虽支持隐式微分，但未针对投影问题定制算法，训练效率低且推理慢。

Πnet的核心因果调节变量在于：将投影表示为一个固定点迭代，并应用隐函数定理进行高效反向传播，同时使用Douglas-Rachford算子分裂算法实现快速且精确的投影。这一设计使得网络输出后附加的可微正交投影层，既能保证约束严格满足，又能大幅提升训练和推理效率。

### 主实验结果

#### 非凸问题上的解质量

在非凸基准测试中，Πnet在测试集上达到约束违反（CV）≤ $10^{-3}$ 且相对次优性（RS）≤ 5%的最优阈值，而DC3和JAXopt未能达标或无法训练（Figure 2）。具体而言，在小型非凸问题（$d=100$）上，Πnet的平均RS为0.00216，而仅在测试时投影的变体Πnet-inf为0.02178，改善约10倍（Appendix C.4）。在大规模问题（$d=1000$）上，DC3使用默认参数在训练期间发散，JAXopt训练极慢，而Πnet仅用50个epoch便获得高质量解（Figure 2, Figure 3）。

Πnet显著优于DC3的原因在于：训练损失中不存在软惩罚项，且投影的正交性保证了约束满足的严格性。与JAXopt的训练时间差异则凸显了Πnet利用投影问题结构的定制化算子分裂和实现的重要性。

#### 推理时间优势

在推理效率方面，Πnet展现出数量级的加速优势。在小型非凸问题（$d=100$）上，单实例推理时间（CPU）为0.0052秒，而cvxpylayers为0.0120秒，加速约2.3倍；批量推理（1024个实例，GPU）仅需0.0135秒，cvxpylayers需2.5917秒，加速约192倍（Table 1）。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/006_Table_1.jpg]]
*Table 1: Comparison with cvxpylayers on the small, non-convex benchmark. The RS and CV values reported are the averages over the test set*

在凸问题上，Πnet的批量推理时间为0.0130秒，相比传统求解器OSQP（1.9350秒）快149倍，比JAXopt（0.1603秒）快12倍（Table 3）。在非凸问题上，所有学习方法在推理时间上均显著优于传统求解器（Table 2）。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/008_Table_2.jpg]]
*Table 2: Inference time comparison for single-instance and batch (1024 contexts) settings, evaluated on the small and large non-convex problems. The table reports the median, lower quartile (LQ, 25th percentile), upper quartile (UQ, 75th percentile), min and max of the runtime*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/009_Table_3.jpg]]
*Table 3: Inference time comparison for single-instance and batch (1024 contexts) settings, evaluated on the small and large convex problems. The table reports the median, lower quartile (LQ, 25th percentile), upper quartile (UQ, 75th percentile), min and max of the runtime. We report results of the Solver (i.e., OSQP) in two modes, normal and parametric labeled with Solver and Solver†, respectively. Parametric mode means that we inform OSQP that we are repeatedly solving problems with the same structure, which speeds up solution time by reusing calculations across consecutive calls. We note that this is a feature of OSQP that may or may not be available in other solvers*

#### 凸问题上的表现

在凸基准测试中，Πnet同样展现出优异的约束满足和解质量（Figure 5），验证了该方法在不同问题类型上的泛化能力。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/007_Figure_5.jpg]]
*Figure 5: Scatter plots of RS and CV on the small and large convex problems on the test set. The red dashed lines show the thresholds to consider a candidate solution optimal*

### 消融实验

#### 训练期间投影的必要性

在训练期间执行投影（而非仅在推理时）将相对次优性（RS）提高了一个数量级（Πnet vs Πnet-inf，Appendix C.4），表明让骨干网络在训练过程中感知投影层对解质量至关重要。

#### 矩阵均衡化与自动调谐

矩阵均衡化和自动调谐显著降低了约束违反（CV），并将所需前向迭代次数从默认的100次或自动调谐的350次减少到50次（Figure 16, Table 6）。这一消融表明，通过Ruiz均衡化改善条件数并自动选择超参数，是提升投影层效率的关键技术。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/024_Table_6.jpg]]
*Table 6: Inference time comparison for single-instance and batch-instance (1024 problems) settings across different ablation configurations, evaluated on the large non-convex problem. The table reports median runtime along with statistical descriptors: lower quartile (LQ, 25th percentile), upper quartile (UQ, 75th percentile), min and max of the runtime*

#### 超参数鲁棒性

不同的Douglas-Rachford超参数σ和ω值产生定性相似的性能（Figures 19 and 20），表明Πnet方法具有良好的超参数鲁棒性，降低了实际部署时的调参负担。

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/027_Figure_19.jpg]]
*Figure 19: Scatter plot of RS and CV on the small non-convex test problems for a Πnet network trained with different values of σ and (top) 50, (bottom) 100 forward iterations. The red dashed lines indicate the thresholds used to consider a candidate solution optimal*

### 公平性说明

所有学习方法均使用相同的MLP骨干架构（2个隐藏层，每层200个神经元，ReLU激活）和自监督损失（直接最小化目标函数）。对于DC3，当默认参数在大数据集上发散时，调整了学习率以使其能够学习，并报告了最佳结果。Πnet仅训练50个epoch，而DC3训练1000个epoch，但Πnet仍表现出更优的解质量和更快的收敛。在推理时间比较中，传统求解器OSQP使用了参数模式以加速重复求解，且所有方法均在相同硬件上评估。

### 多车辆运动规划应用

Πnet成功应用于多车辆运动规划任务（Figure 4），验证了该方法在具有任意可微目标函数的约束优化问题上的灵活性。该应用展示了Πnet处理复杂约束结构的能力，同时保持了推理效率。

### 补充图表

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/019_Figure.jpg]]

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/031_Figure_22.jpg]]
*Figure 22: VJP estimation error (measured via the ℓ2-norm of the difference and the cosine similarity) for 100 different vectors $v _ { i }$ instances (light blue) for two different instances of the small non-convex benchmark as the number of iterations in the backward pass n iter bwd increases, as well as the maximum $\ell _ { 2 }$ -error and the minimum cosine similarity among all instances (dark blue)*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/014_Table_4.jpg]]
*Table 4: Inference time comparison for single-instance and batch-instance (1024 problems) settings across different methods, evaluated on small and large non-convex problems. The table reports median runtime along with statistical descriptors: lower quartile (LQ, 25th percentile), upper quartile (UQ, 75th percentile), min and max of the runtime. DC3 uses more than the default correction steps*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/020_Figure_14.jpg]]
*Figure 14: Scatter plots of RS and CV on the second-order cone programs on the test set. The red dashed lines show the thresholds to consider a candidate solution optimal. Table 5: Inference time comparison for single-instance and batch-instance (1024 problems) settings across different methods, evaluated on the second-order cone programs. The table reports median runtime along with statistical descriptors: lower quartile (LQ, 25th percentile), upper quartile (UQ, 75th percentile), min and max of the runtime*

![[assets/figures/papers/paper_list_l10_https_openreview_net_forum_id_EJ680UQeZG/figures/026_Figure.jpg]]
*Figure: However, if we would train an unconstrained network to predict { \hat { y } } ( \mathbf { x } ) , its values would result in yˆ(x) + for \mathrm { ~ x > 0 ~ } and \hat { y } ( \mathbf x ) \to - \infty for \mathrm { x } < 0*



## 定位与知识库关联

### 硬约束神经网络中的投影与微分困境

Πnet 所解决的核心瓶颈是硬约束神经网络中长期存在的“投影-微分”效率矛盾。传统上，将神经网络输出投影到可行集（如等式、不等式、框约束构成的凸集）有两种策略：

1. **软约束方法**：将约束作为惩罚项加入损失函数。该方法实现简单，但无法保证解严格可行，且惩罚系数调谐困难，容易在目标最优性与约束满足之间产生冲突。DC3 等方法试图通过推理时的等式完成与不等式校正来补救，但在大规模问题上约束违反（CV）仍然不可接受（Figure 2）。

2. **硬约束方法**：在输出端附加投影层，确保输出始终位于可行集内。然而，反向传播通过投影层时，若采用循环展开（loop unrolling）前向迭代（如 Dykstra 算法），计算图将随迭代次数线性膨胀，导致训练时间和内存开销巨大。cvxpylayers 等基于凸优化层的方法虽然提供了隐式微分，但在批量推理时 GPU 利用率极低——Table 1 显示，在 1024 实例的小型非凸问题上，cvxpylayers 的 GPU 批量推理时间为 2.5917 秒，而 Πnet 仅需 0.0135 秒，加速约 192 倍。

### Πnet 的方法学定位：算子分裂 + 隐式微分

Πnet 的方法学贡献在于将投影层的正向传播与反向传播解耦优化：

- **正向传播**：将投影问题形式化为 Douglas-Rachford 算子分裂的固定点迭代（Algorithm 1）。该算法的关键优势在于利用了约束集的分解结构 $\mathcal{C} = \Pi_d(\mathcal{A} \cap \mathcal{K})$，其中 $\mathcal{A}$（超平面）和 $\mathcal{K}$（笛卡尔积框）的投影均可闭式求解，使得每次迭代仅需廉价的近端算子计算，而非通用 QP 求解。

- **反向传播**：利用隐函数定理（implicit function theorem）将梯度计算转化为求解一个线性系统，并通过双共轭梯度稳定法（bicgstab）近似求解（Equation 8-9）。这避免了循环展开，使得反向传播的计算成本与正向迭代次数解耦，同时保持了数值稳定性。

这种“定制化算子分裂 + 隐式微分”的组合，使 Πnet 在方法谱系中处于一个独特位置：它既不同于 DC3 的“软约束 + 推理校正”范式，也不同于 JAXopt 的“通用求解器隐式层”范式。JAXopt 使用 OSQP 求解器进行隐式微分，虽然理论优雅，但未能针对投影问题的特殊结构进行算法定制，导致训练时间比 Πnet 高出数个量级（Figure 3，大规模非凸问题上 JAXopt 的训练曲线因时间过长仅报告于附录）。

### 与相关工作的关系

- **cvxpylayers**：同样提供可微的凸优化层，但其底层依赖锥规划求解器，在批量推理时无法充分利用 GPU 并行性。Πnet 的算子分裂实现天然适合 GPU 批量化，Table 1 中的 192 倍加速印证了这一结构性优势。

- **OSQP 与 IPOPT**：作为传统求解器，它们在单实例求解上具有竞争力（OSQP 参数模式），但无法从批量并行中获益。Table 3 显示，Πnet 在 1024 实例批量推理时比 OSQP 快 149 倍（0.0130 秒 vs 1.9350 秒）。

- **DC3**：作为硬约束学习的代表性基线，DC3 在默认参数下于大规模数据集上发散，即使调整学习率后仍无法达到 Πnet 的解质量——Figure 2 中 DC3 的 RS 和 CV 远高于最优阈值（RS ≤ 5%，CV ≤ 1e-3），而 Πnet 以显著裕度达标。

### 适用边界与约束假设

Πnet 当前版本基于一个关键的结构性假设：**可行集 $\mathcal{C}(\mathbf{x})$ 必须是凸集**，且可分解为 $\mathcal{C} = \Pi_d(\mathcal{A} \cap \mathcal{K})$ 的形式。这一假设覆盖了广泛的实际约束类型（等式、不等式、框约束），但明确排除了非凸约束（如碰撞避免、非凸几何约束）。论文在结论中明确指出，将 Πnet 扩展到非凸约束需要通过序列凸化（sequential convexification）技术，这是一个开放的工程挑战。

此外，Πnet 要求约束矩阵在训练前已知且固定，不适用于约束结构动态变化的在线学习场景。

### 消融实验揭示的关键依赖

消融实验揭示了 Πnet 性能的两个关键依赖：

1. **矩阵均衡化与自动调谐**（Appendix C.3，Figure 16，Table 6）：Ruiz 均衡化改善了约束矩阵的条件数，使得 Douglas-Rachford 迭代的收敛速度大幅提升——所需正向迭代次数从默认的 100 次或自动调谐的 350 次降至 50 次，同时约束违反显著降低。这表明 Πnet 的性能对约束矩阵的数值特性敏感，均衡化是实际部署中不可或缺的预处理步骤。

2. **训练期间投影的必要性**（Appendix C.4）：若仅在推理时投影（Πnet-inf），相对次优性（RS）比训练期间投影（Πnet）差约一个数量级（0.02178 vs 0.00216）。这验证了“端到端可微投影”对学习质量的因果作用——骨干网络需要感知投影层的几何效应才能学会生成易于投影的原始输出。

### 开放问题

1. **非凸约束的扩展**：如何将算子分裂框架推广到非凸可行集？序列凸化与 Πnet 的结合是否仍能保持训练效率优势？
2. **约束结构动态变化**：当约束矩阵随上下文 $\mathbf{x}$ 变化时，矩阵均衡化和自动调谐需要在线执行，其计算开销是否可接受？
3. **新应用领域的验证**：论文提及神经 PDE 求解器、调度、机器人等潜在应用，但除多车辆运动规划外，尚未在更复杂的约束类型上验证 Πnet 的泛化能力。



## 原文 PDF

![[paperPDFs/ICLR_2026/Pinet_Optimizing_hard_constrained_neural_networks_with_orthogonal_projection_layers.pdf]]
