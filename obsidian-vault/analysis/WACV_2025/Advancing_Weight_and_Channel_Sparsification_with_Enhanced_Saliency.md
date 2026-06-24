---
title: "Advancing Weight and Channel Sparsification with Enhanced Saliency"
type: paper
paper_level: A
venue: WACV
year: 2025
pdf_ref: paperPDFs/WACV_2025/Advancing_Weight_and_Channel_Sparsification_with_Enhanced_Saliency.pdf
aliases:
- IIEE
- AWCSES
tags:
- WACV_2025
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "统一的显著性准则与‘重新激活-探索’（Reactivate & Explore）机制：将模型划分为活跃结构（exploitation）与探索空间（exploration），并用相同的重要性准则进行剪枝与生长；在探索阶段暂时重激活所有被剪枝参数并训练少量步，冻结当前结构以提供潜在增益预览。"
primary_logic: "通过短暂重激活探索空间中的参数并冻结活动结构，可以获得更准确的参数重要性评估，从而克服动态稀疏训练中的贪婪性和准则不一致性，实现更有效的稀疏结构探索。"
claims:
- "IEE 在 ImageNet 上使用 ResNet50 在 90% ERK 非结构化稀疏度下比 RigL 提高 1.3 个百分点 Top-1 准确率。"
- "IEE 在结构化剪枝上以更低的训练成本（×0.39 vs ×1.39）超越了 HALP，实现了更高的 FPS（2736 vs 2597）和准确率（74.6 vs 74.5）。"
- "IEE 采用统一的显著性准则进行剪枝和生长，避免了动态稀疏训练中准则不一致的问题。"
- "IEE 的生长神经元存活率显著高于 RigL，表明其探索策略更有效。"
---

# Advancing Weight and Channel Sparsification with Enhanced Saliency

> [!tip] 核心洞察
> 通过短暂重激活探索空间中的参数并冻结活动结构，可以获得更准确的参数重要性评估，从而克服动态稀疏训练中的贪婪性和准则不一致性，实现更有效的稀疏结构探索。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 利用增强显著性推进权重与通道稀疏化 |
| 英文题名 | Advancing Weight and Channel Sparsification with Enhanced Saliency |
| 会议/期刊 | WACV 2025 |
| Links | [paper](https://arxiv.org/abs/2502.03658) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | IEE (Iterative Exploitation and Exploration) |
| Dataset | ImageNet1K structured ResNet50, ImageNet1K unstructured ResNet50 90% ERK, ImageNet1K N:M sparsity ResNet50 2:4 |

> [!tip] 效果简介
> - ImageNet1K structured ResNet50 上，Top-1 Accuracy (%) 为 74.6 (IEE-30% from scratch)，对比 74.5 (HALP-30%)，变化 +0.1 (同时 FPS 2736 vs 2597, 训练成本 ×0.39 vs ×1.39)。
> - ImageNet1K unstructured ResNet50 90% ERK 上，Top-1 Accuracy (%) 为 74.3 (IEE)，对比 73.0 (RigL)，变化 +1.3。
> - ImageNet1K N:M sparsity ResNet50 2:4 上，Top-1 Accuracy (%) 为 77.5 (IEE)，对比 77.0 (SR-STE)，变化 +0.5。

## 概述

深度神经网络在资源受限场景下的部署依赖剪枝与稀疏化技术来降低计算与存储开销。然而，现有方法面临两个根本性瓶颈：其一，重要性准则（saliency scores）本身不完美，且传统剪枝一旦执行便不可逆，导致错误剪枝无法被纠正；其二，以 **RigL** 为代表的动态稀疏训练方法存在剪枝与生长准则不一致（如幅值剪枝 vs. 梯度生长）、不适合结构化稀疏、以及生长策略短视等问题。

针对上述瓶颈，本文提出 **IEE（Iterative Exploitation and Exploration）**，其核心思路是将模型参数划分为活跃结构（exploitation）与探索空间（exploration），并用**统一的显著性准则**同时指导剪枝与生长，从而消除准则不一致性。更关键的是，IEE 引入“重新激活-探索”（Reactivate & Explore）机制：在探索阶段暂时重激活所有被剪枝参数并训练少量步，同时冻结当前活跃结构，以获得探索空间中参数潜在增益的准确预览。这一设计克服了动态稀疏训练中的贪婪性，使稀疏结构的探索更加有效。

实验结果表明，IEE 在多种稀疏范式下均取得显著提升：
- **非结构化稀疏**：ImageNet1K 上 ResNet50 在 90% ERK 稀疏度下达到 74.3% Top-1 准确率，比 RigL 提高 **+1.3 个百分点**（Table 2）。
- **结构化剪枝**：以更低的训练成本（×0.39 vs. ×1.39）超越 **HALP**（Shen et al., NeurIPS 2022），实现更高的 FPS（2736 vs. 2597）和准确率（74.6% vs. 74.5%）（Table 1）。
- **N:M 稀疏**：ResNet50 2:4 稀疏度下达到 77.5%，优于 SR-STE 的 77.0%（Table 5）。

消融实验进一步证实，“重新激活-探索”步骤是性能提升的关键——移除该步骤后准确率从 74.3% 降至 73.1%，与 RigL 持平；同时，探索阶段冻结活跃结构也是必要的设计选择（Table 4）。

## 背景与动机

深度神经网络在资源受限环境中的部署持续推动着模型压缩技术的发展。稀疏化——通过移除冗余权重（非结构化稀疏）或整个结构单元（结构化稀疏）来精简网络——已成为平衡模型效率与性能的核心范式。然而，当前方法在两个关键维度上仍面临根本性瓶颈。

### 现有重要性准则的不完美性与不可逆剪枝

传统剪枝方法的核心困境在于：**重要性准则（saliency scores）天然不完美，而剪枝操作本身不可逆**。所有剪枝算法都依赖于某种启发式准则——如权重的幅值、梯度或泰勒展开近似——来判定哪些参数“不重要”。这些准则本质上是模型在特定训练状态下对参数贡献的局部估计，不可避免地存在误判。一旦参数被错误剪枝，传统方法缺乏有效的纠错机制，导致模型容量永久损失。这一“错误剪枝无法纠正”的问题，在结构化剪枝中尤为严重，因为移除整个通道或滤波器会造成不可恢复的信息瓶颈。

### 动态稀疏训练的准则不一致与短视生长

动态稀疏训练（Dynamic Sparse Training）通过交替执行剪枝与生长操作，试图克服静态剪枝的不可逆性。以代表性方法 **RigL** 为例，其核心设计是：基于权重的瞬时幅值进行剪枝，同时基于零化权重的梯度进行生长。这种设计引入了两个结构性缺陷：

1. **准则不一致性**：剪枝与生长使用完全不同的信号（幅值 vs. 梯度），导致两个阶段的目标函数隐含冲突。剪枝阶段移除“当前小”的权重，而生长阶段激活“梯度大”的权重——这两者之间缺乏理论保证的一致性，使得整个探索过程缺乏统一的方向引导。

2. **短视生长策略**：生长操作仅基于未激活参数在当前时刻的瞬时梯度做出决策。由于这些参数始终处于零值状态，其梯度信息极为有限且噪声较大，难以准确反映其被激活后的真实贡献潜力。这种“贪心”策略使得动态稀疏训练容易陷入局部最优的稀疏结构。

此外，RigL 等方法的生长机制天然适用于非结构化稀疏（单个权重独立生长），难以直接迁移到结构化稀疏场景（需要生长整个通道或滤波器），限制了其在硬件感知压缩中的应用范围。

### 本文动机：从“贪心探索”到“预览式探索”

上述分析揭示了一个深层需求：**动态稀疏训练需要一种机制，能够在做出永久性结构决策之前，更准确地评估候选参数的真实潜力**。这引出了本文的核心动机——

- 能否设计一个统一的显著性准则，同时指导剪枝与生长，消除准则不一致问题？
- 能否在生长决策前，为当前被排除的参数提供一个“试运行”机会，通过短暂训练预览其潜在增益，从而克服短视性？

本文提出的 **IEE（Iterative Exploitation and Exploration）** 方法正是沿着这一思路展开：将模型划分为活跃结构（exploitation）与探索空间（exploration），在探索阶段暂时重激活所有被剪枝参数并训练少量步，同时冻结当前活跃结构以隔离干扰，从而获得更准确的参数重要性评估。这一“重新激活-探索”（Reactivate & Explore）机制，使得生长决策从“基于瞬时梯度的猜测”升级为“基于实际训练的预览”，为动态稀疏训练提供了更可靠的探索基础。

## 核心创新

IEE 的核心创新在于将动态稀疏训练中长期存在的**准则不一致**与**生长短视**两个瓶颈统一解决，而非沿袭现有方法“剪枝用一套准则、生长用另一套准则”的分离式设计。

### 1. 统一的剪枝-生长显著性准则

传统动态稀疏训练的典型代表 RigL 在剪枝阶段依赖权重的幅值大小，而在生长阶段则依据被剪枝权重的梯度大小来选择复活参数——两套准则在语义上并不对齐，导致刚被剪掉的参数可能因梯度较大而立即被重新激活，形成无效的“乒乓”更新。IEE 从根本上改变了这一机制：**剪枝和生长使用同一给定的重要性准则**（如幅值或泰勒重要性），从而保证每一轮结构更新的决策逻辑自洽。

$$ \Theta_K \gets \Theta_K - \mathrm{ArgTopK}(-I(\Theta_K), \Omega^t) $$

$$ \Theta_P \gets \Theta_P + \mathrm{ArgTopK}(-I(\Theta_K), \Omega^t) $$

从活动结构 $\Theta_K$ 中移除的，是同一重要性度量下评分最低的参数；从探索空间 $\Theta_P$ 中重新生长的，同样是该度量下评分最高的参数。这种对称设计消除了准则不一致带来的结构震荡。

### 2. “重激活-探索”机制：从短视生长到预览式评估

动态稀疏训练的另一深层缺陷在于生长决策的短视性：被剪枝的参数在未激活状态下只能提供瞬时梯度信号，无法反映其真正参与训练后的潜在贡献。IEE 提出 **Reactivate & Explore** 阶段来弥补这一信息鸿沟：

- **暂时重激活探索空间**：将 $\Theta_P$ 中的所有被剪枝参数重新激活，与当前活动结构 $\Theta_K$ 拼接成完整模型。
- **冻结活动结构**：在探索阶段固定 $\Theta_K$ 的参数不变，仅训练 $\Theta_P$ 共 $Q$ 步。
- **基于预览评估重要性**：在 $Q$ 步训练后，对 $\Theta_P$ 中的参数计算重要性分数，再选取最高分者生长回 $\Theta_K$。

$$ \operatorname*{min}_{\Theta_P} \sum_{i=1}^{Q} \ell(f(\Theta_P \cup \Theta_K; \mathbf{x}^i), \mathbf{y}^i) $$

这一设计的直觉在于：让探索空间中的候选参数在“冻结当前最优结构”的受控条件下获得真实的训练预览，从而为生长决策提供远比瞬时梯度可靠的信号。消融实验直接验证了该机制的必要性——**移除 Reactivate & Explore 后，90% ERK 稀疏度下的 Top-1 准确率从 74.3% 降至 73.1%，与 RigL 持平**（Table 4: w/o ReAct & Explore）；同样，若不冻结 $\Theta_K$，性能也会显著下降（Table 4: w/o Freeze $\Theta_K$）。

### 3. 统一的探索-利用迭代框架

上述两个创新被整合进一个五阶段的迭代更新循环（Figure 2），每个 IEE 更新步包含：

| 阶段 | 操作 | 作用 |
|------|------|------|
| Importance Estimation | 训练 $\Theta_K$ $H$ 步并计算重要性 | 为剪枝提供可靠评分 |
| Prune | 移除 $\Theta_K$ 中低分参数至 $\Theta_P$ | 释放冗余容量 |
| Accuracy Improvement | 训练剪枝后的 $\Theta_K$ $J$ 步 | 稳定当前结构性能 |
| Reactivate & Explore | 冻结 $\Theta_K$，训练 $\Theta_P$ $Q$ 步 | 预览探索空间潜力 |
| Grow | 从 $\Theta_P$ 选取高分参数回归 $\Theta_K$ | 完成结构更新 |

该框架将模型显式划分为**活动结构**（exploitation）与**探索空间**（exploration），使每一轮更新都在“充分利用当前最优结构”和“审慎探索更优结构”之间取得平衡。与 RigL 等方法的本质区别在于：IEE 的生长决策不是基于零化权重的瞬时梯度，而是基于短暂重激活训练后的重要性评估，从而克服了贪婪式生长的短视性。

生长神经元存活率的对比（Figure 5(b)）进一步佐证了这一优势——IEE 生长的神经元在后续训练中被保留的比例显著高于 RigL，说明其探索策略确实找到了更具长期价值的结构连接。

## 整体框架

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2502_03658/figures/008_Figure_5.jpg]]
*Figure 5: (a) Architecture convergence with IoU after pruning and growing; (b) Grown Neurons Survival Rate for ours and RigL [12]*

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2502_03658/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our method. In each IEE update step, we first train the active weights $\Theta _ { K }$ for H steps then prune a number of connections from $\Theta _ { K }$ . We later train the weights $\Theta _ { K }$ just selected for J steps for better exploiting the current architecture. To explore a potentially better sparse architecture, we temporarily activate the exploration space $\Theta _ { P }$ and train them for Q steps while freezing $\Theta _ { K }$ . . We then evaluate the importance scores of the activated $\Theta _ { P }$ to grow the top-ranked weights. This completes one full IEE update step, and it is repeated until the update period ends

IEE（Iterative Exploitation and Exploration）将模型参数划分为两个互补的集合：**活跃结构** $\Theta_K$（当前被利用的参数）和**探索空间** $\Theta_P$（被剪枝但可重新激活的参数）。方法通过交替执行“利用”与“探索”来持续优化稀疏结构，其核心设计原则是**剪枝与生长使用同一重要性准则**，从而消除传统动态稀疏训练中准则不一致带来的偏差。

每个完整的 IEE 更新步骤包含五个阶段，如 Figure 2 所示：

1. **重要性估计（Importance Estimation）**：对活跃结构 $\Theta_K$ 进行 $H$ 步训练，在最大化性能的同时评估各参数的重要性分数 $I(\Theta_K)$：
   $$\min_{\Theta_K} \sum_{i=1}^{H} \ell(f(\Theta_K; \mathbf{x}^i), \mathbf{y}^i)$$

2. **剪枝（Prune）**：根据重要性分数，将活跃结构中最不重要的参数移除并移入探索空间，移除数量由更新预算 $\Omega^t$ 控制：
   $$\Theta_K \gets \Theta_K - \mathrm{ArgTopK}(-I(\Theta_K), \Omega^t)$$
   $$\Theta_P \gets \Theta_P + \mathrm{ArgTopK}(-I(\Theta_K), \Omega^t)$$

3. **精度改进（Accuracy Improvement）**：对剪枝后的活跃结构进行 $J$ 步训练，以稳定新结构的性能，充分挖掘当前架构的潜力。

4. **重激活与探索（Reactivate & Explore）**：这是 IEE 区别于现有方法的关键机制。暂时激活探索空间 $\Theta_P$ 中的所有参数，同时**冻结活跃结构 $\Theta_K$**，进行 $Q$ 步训练：
   $$\min_{\Theta_P} \sum_{i=1}^{Q} \ell(f(\Theta_P \cup \Theta_K; \mathbf{x}^i), \mathbf{y}^i)$$
   这一设计使得探索空间中的参数能够在不受活跃结构梯度干扰的情况下获得真实的重要性预览，克服了 RigL 等方法仅依赖瞬时梯度进行生长的短视性。

5. **生长（Grow）**：从探索空间中选取重要性分数最高的参数重新加入活跃结构：
   $$\Theta_K \gets \Theta_K + \mathrm{ArgTopK}(I(\Theta_P), \Omega^t)$$
   $$\Theta_P \gets \Theta_P - \mathrm{ArgTopK}(I(\Theta_P), \Omega^t)$$

上述五阶段构成一次完整的 IEE 更新步，整个过程在训练中重复执行 $T$ 步，更新预算 $\Omega^t$ 按指数衰减调度器逐步减小，使稀疏结构从初始分布逐渐收敛至目标稀疏度。

**模块间的因果链路**：重激活与探索阶段（阶段 4）为生长阶段（阶段 5）提供了可靠的重要性评估，而统一的显著性准则确保了剪枝（阶段 2）和生长（阶段 5）的决策一致性。消融实验证实了这一设计的必要性：移除重激活与探索步骤后，性能从 74.3% 下降到 73.1%（与 RigL 持平）；若不冻结 $\Theta_K$，性能同样显著下降（Table 4）。此外，生长参数的初始化策略也影响最终效果——使用 MRU（Most Recently Used）初始化优于零初始化。

**输入输出流**：输入为初始稀疏分布（如 Uniform 或 ERK）下的模型参数划分 $\{\Theta_K, \Theta_P\}$ 和总更新预算衰减调度器；输出为经过 $T$ 步 IEE 更新后收敛的稀疏结构 $\Theta_K$，可直接用于推理。

## 核心模块与公式推导

### 3.1 模型划分与双空间机制

IEE 将模型参数显式划分为两个互斥子集：**活动结构**（active structure）$\Theta_K$ 与**探索空间**（exploration space）$\Theta_P$。$\Theta_K$ 是当前被利用（exploitation）的稀疏网络，直接参与前向推理与训练；$\Theta_P$ 则容纳所有被剪枝的参数，作为潜在结构更新的候选池。这一划分是后续剪枝-生长动态的基础。

### 3.2 IEE 更新步骤的五阶段流水线

每个 IEE 更新步骤由五个阶段组成，形成一次完整的“利用-探索”循环：

**阶段 1：重要性估计（Importance Estimation）**

对活动结构 $\Theta_K$ 进行 $H$ 步训练，以最大化当前稀疏架构的性能，同时为后续剪枝提供重要性评估依据。训练目标为：

$$\operatorname*{min}_{\Theta_K} \sum_{i=1}^{H} \ell(f(\Theta_K; \mathbf{x}^i), \mathbf{y}^i)$$

其中 $\ell$ 为损失函数，$f$ 为模型，$(\mathbf{x}^i, \mathbf{y}^i)$ 为第 $i$ 步的输入-标签对。训练完成后，对 $\Theta_K$ 中的参数计算重要性分数 $I(\Theta_K)$。

**阶段 2：剪枝（Prune）**

根据重要性分数移除活动结构中最不重要的参数，将其转移至探索空间。操作定义为：

$$\Theta_K \gets \Theta_K - \mathrm{ArgTopK}(-I(\Theta_K), \Omega^t)$$
$$\Theta_P \gets \Theta_P + \mathrm{ArgTopK}(-I(\Theta_K), \Omega^t)$$

$\mathrm{ArgTopK}(-I(\Theta_K), \Omega^t)$ 选取重要性最低的 $\Omega^t$ 个参数，其中 $\Omega^t$ 为第 $t$ 步的更新预算（update budget），控制每次剪枝-生长循环的参数更替量。

**阶段 3：精度改进（Accuracy Improvement）**

对剪枝后的 $\Theta_K$ 进行 $J$ 步训练，以稳定新架构的性能。此阶段不涉及任何结构变更，纯粹服务于当前活动结构的精度恢复。

**阶段 4：重激活与探索（Reactivate & Explore）**

这是 IEE 区别于现有动态稀疏训练的核心机制。在此阶段，暂时激活探索空间 $\Theta_P$ 中的所有参数，同时**冻结** $\Theta_K$，对 $\Theta_P$ 进行 $Q$ 步训练：

$$\operatorname*{min}_{\Theta_P} \sum_{i=1}^{Q} \ell(f(\Theta_P \cup \Theta_K; \mathbf{x}^i), \mathbf{y}^i)$$

冻结 $\Theta_K$ 的意义在于：让探索空间参数在一个稳定的活动结构基础上接受训练，从而获得更准确的潜在增益预览。若不同时冻结 $\Theta_K$，活动结构的参数更新会干扰对探索空间参数真实重要性的评估（消融实验证实了冻结的必要性，详见 Table 4）。

**阶段 5：生长（Grow）**

根据探索阶段收集的重要性分数 $I(\Theta_P)$，选取最高分的参数重新加入活动结构：

$$\Theta_K \gets \Theta_K + \mathrm{ArgTopK}(I(\Theta_P), \Omega^t)$$
$$\Theta_P \gets \Theta_P - \mathrm{ArgTopK}(I(\Theta_P), \Omega^t)$$

### 3.3 关键设计要点

**统一的剪枝-生长准则。** 与 RigL 等方法在剪枝和生长阶段使用不同准则（如幅值剪枝 vs. 梯度生长）不同，IEE 在阶段 2 和阶段 5 中使用**同一重要性准则** $I(\cdot)$。对于非结构化稀疏，可采用幅值重要性（magnitude）；对于结构化稀疏，可采用泰勒重要性（Taylor importance）。这一设计消除了准则不一致带来的次优结构选择。

**重激活机制的理论动因。** 动态稀疏训练中，基于未激活参数的瞬时梯度进行生长（如 RigL 的做法）本质上是短视的——梯度仅反映参数在当前点的局部信息，无法预示其收敛后的真实贡献。IEE 通过 $Q$ 步的短暂重激活训练，让探索空间参数在冻结活动结构的条件下获得更充分的重要性评估，从而克服了贪婪生长策略的局限性。Figure 5(b) 的生长神经元存活率对比直接验证了这一机制的有效性：IEE 生长出的神经元在后续训练中被保留的比例显著高于 RigL。

**更新预算 $\Omega^t$ 的衰减调度。** $\Omega^t$ 随训练进程逐步衰减（采用固定衰减策略，如指数衰减），使得早期允许较大的结构探索幅度，后期趋于精细调整。具体的衰减调度器未针对不同网络自适应调整，这一点在局限性中被指出。

## 实验与分析

### 核心实验设置

IEE 在结构化稀疏和非结构化稀疏两种范式下均进行了验证。结构化实验采用泰勒重要性准则（Taylor importance），非结构化实验采用幅值重要性准则（magnitude importance）。结构化稀疏的实现依托 **HALP**（Shen et al., NeurIPS 2022）的硬件感知压缩框架，通过延迟查找表（Latency Lookup Table）直接优化推理延迟，查找表基于 NVIDIA Titan V GPU 生成。非结构化稀疏实验遵循标准动态稀疏训练协议，与 **RigL** 等基线使用相同的训练轮数、优化器设置和层稀疏分布（Uniform/ERK），且未采用数据筛选或层冻结等额外技巧（MEST 除外，已注明）。训练 FLOPs 的计算遵循附录中的统一方法，并对某些方法（如 GraNet）的起始 FLOPs 进行了修正以确保公平对比。

### 结构化稀疏主结果

在 ImageNet1K 上使用 ResNet50 的结构化稀疏实验中，IEE 展现出显著的训练成本优势和推理速度提升。如 Table 1 所示，**IEE-30% from scratch** 达到 74.6% Top-1 准确率，FPS 为 2736，训练成本仅为基线 ResNet50 的 0.39 倍。相比之下，HALP-30% 准确率为 74.5%，FPS 为 2597，训练成本却高达 1.39 倍。IEE 在保持甚至略微提升准确率的同时，将训练成本降低了超过 70%，推理速度提升了约 5.4%。在 55% 参数保留的设置下，IEE-55% from scratch 达到 76.6% Top-1 准确率，进一步验证了该方法在不同稀疏度下的稳定性。

在 MobileNet-V1 上的结构化稀疏实验（Figure 3）进一步展示了 IEE 在轻量级架构上的有效性。IEE 在 FPS-准确率权衡曲线上显著优于 **EagleEye**（Li et al., ECCV 2020）、**AutoSlim**（Yu et al., NeurIPS 2019）、**AMC**（He et al., ECCV 2018）、**MetaPruning**（Liu et al., ICCV 2019）和 **HALP**（Shen et al., NeurIPS 2022），同时在训练成本上保持明显优势。

在 PASCAL VOC 目标检测任务上，使用 SSD512-RN50 骨干网络的结构化稀疏实验（Figure 4）表明，IEE 在 FPS-mAP 权衡和训练成本两个维度均优于 HALP，证明了该方法在下游视觉任务中的迁移能力。

### 非结构化稀疏主结果

在 ImageNet1K 上使用 ResNet50 的非结构化稀疏实验中（Table 2），IEE 在 90% ERK 稀疏度下达到 74.3% Top-1 准确率，比 **RigL** 的 73.0% 提高了 1.3 个百分点。在 80% ERK 稀疏度下，IEE 达到 77.0%，比 RigL 的 75.9% 提高了 1.1 个百分点。值得注意的是，当训练轮数扩展到 500 轮（IEE5×）时，IEE 在 80% ERK 稀疏度下达到 77.8% Top-1 准确率，超越了密集 ResNet50 的 76.8%，这表明 IEE 的探索-利用机制能够发现优于原始密集结构的稀疏子网络。


![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2502_03658/figures/006_Table_2.jpg]]
*Table 2: ImageNet1K unstructured sparsity results on ResNet50, averaged over two runs. IEEX× scales the baseline training epochs (100) by X. IEEuniInit and $\mathrm { I E E } _ { e r k I n i t }$ (Non-Uniform) refer to using uniform or ERK for initializing the sparsity distribution. Results are grouped by Train FLOPs. MEST [84] employs dataset sieving and layer freezing for cost reduction. ∗: approximated cost with ERK*

在 CIFAR-10 上使用 WideResNet22-2 的非结构化稀疏实验中（Table 3），IEE 在多种稀疏度设置下均保持领先，进一步验证了该方法在小规模数据集上的鲁棒性。


![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2502_03658/figures/007_Table_3.jpg]]
*Table 3: CIFAR-10 unstructured sparsity results using WideResNet22-2. Averaged results over three runs*

### N:M 稀疏性结果

IEE 同样适用于 Ampere 架构的 N:M 结构化稀疏模式。在 ImageNet1K 上使用 ResNet50 的 2:4 稀疏实验中（Table 5），IEE 达到 77.5% Top-1 准确率，超越了 **SR-STE** 的 77.0%，且在相同训练 FLOPs 下优于其他专用 N:M 剪枝方法。这表明 IEE 的统一探索-利用框架无需针对 N:M 稀疏性进行特殊设计即可取得有竞争力的结果。


![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2502_03658/figures/010_Table_5.jpg]]
*Table 5: ImageNet1K N:M sparsity results with ResNet50. IEE surpasses strong latest specialized ampere pruning methods in Top-1 with the same training FLOPs needed*

### 消融实验

消融实验（Table 4）在 ImageNet1K 上使用 ResNet50 在 90% ERK 非结构化稀疏度下进行，揭示了 IEE 各组件的关键贡献：


![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2502_03658/figures/009_Table_4.jpg]]
*Table 4: Performance of IEE as a function of the update period, grown initialization, weight freezing, and inclusion of Accuracy Improvement stage. Results with 90% unstructured ERK sparsity on ImageNet1K and ResNet50 trained for 100 epochs*

**重激活与探索阶段至关重要。** 移除该阶段后，性能从 74.3% 下降到 73.1%，与 RigL 的 73.0% 持平。这表明仅靠统一的剪枝-生长准则（无探索阶段）无法带来显著增益，重激活探索空间并冻结活动结构是 IEE 性能提升的核心机制。

**活动结构冻结是必要条件。** 在重激活与探索阶段若不冻结 Θ_K（w/o Freeze Θ_K），性能同样显著下降。这一消融验证了核心洞察：只有冻结当前活动结构，才能获得探索空间中参数潜在增益的准确预览，避免活动结构的梯度干扰探索评估。

**更新周期存在最优值。** 当 H=J=Q=150 时达到最佳性能 74.3%。过短的更新周期（如 H=J=Q=50）导致性能下降至 73.5%，可能因为活动结构未充分收敛即被剪枝；过长的更新周期（如 H=J=Q=300）性能为 73.9%，可能因为探索频率不足限制了稀疏结构的搜索空间。

**MRU 初始化优于零初始化。** 使用 Most Recently Used（MRU）策略初始化生长参数（即使用该参数被剪枝前最后的值）比零初始化带来稳定的性能提升，验证了保留历史参数状态对快速恢复网络容量的价值。

**精度改进阶段有正向贡献。** 移除精度改进阶段（w/o Acc. Imp.）后性能下降，表明剪枝后对活动结构进行额外训练以稳定性能是必要的。

### 架构收敛性与生长神经元存活率

Figure 5 从架构演化的角度分析了 IEE 的有效性。Figure 5(a) 展示了剪枝和生长后稀疏架构的 IoU（Intersection over Union）收敛曲线，IEE 的架构收敛速度更快且最终 IoU 更高，表明其探索策略能更稳定地收敛到优质稀疏结构。Figure 5(b) 展示了生长神经元的存活率对比：IEE 的生长神经元存活率显著高于 RigL，这意味着 IEE 探索阶段筛选出的参数更可能对网络性能产生持久贡献，而非短视的瞬时增益。这一结果直接支持了 IEE 的核心主张——通过重激活探索空间获得的参数重要性评估比基于瞬时梯度的生长策略更准确。

### 失败模式与局限性

尽管 IEE 在多个基准上表现优异，但仍存在以下局限：

1. **硬件依赖性**：结构化稀疏的实现依赖 HALP 框架中的延迟查找表，该表针对特定硬件（NVIDIA Titan V）生成，迁移到其他硬件平台需要重新构建查找表，这限制了方法的即插即用性。

2. **训练 FLOPs 估算偏差**：训练成本的计算基于若干近似，NAS 方法的成本仅以下界估计，实际开销可能更高，这可能导致公平性对比存在一定偏差。

3. **超参数固定**：更新预算 Ω^t 的衰减调度器采用固定策略（如指数衰减），更新周期 H、J、Q 需手动设定，未针对不同网络或任务自适应调整，可能无法在所有场景下达到最优。

4. **架构覆盖有限**：实验主要在 ResNet 系列和 MobileNet 上进行，对于 Transformer 等新型架构的适用性尚未验证，其探索-利用机制是否适用于注意力机制的稀疏化仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_arxiv_org_abs_2502_03658/figures/003_Table.jpg]]


## 方法谱系与知识库定位

### 动态稀疏训练谱系中的定位

IEE 的核心贡献在于解决动态稀疏训练（Dynamic Sparse Training, DST）中长期存在的两个瓶颈：**剪枝-生长准则不一致**和**生长策略的短视性**。在主流 DST 方法中，**RigL** 使用幅值剪枝但基于梯度进行生长，导致两个阶段使用完全不同的信号；**SET** 同样依赖幅值剪枝与随机生长。这种准则不一致使得被剪除的参数即使具有潜在价值也无法获得公平的二次评估机会。IEE 通过统一的重要性准则和"重新激活-探索"机制直接回应了这一缺陷——在探索阶段暂时激活所有被剪枝参数并冻结当前活动结构，以相同的准则（如幅值或泰勒重要性）评估其真实潜力，从而实现了更准确的稀疏结构探索。

在结构化稀疏方向上，IEE 与 **HALP**（Shen et al., NeurIPS 2022）构成直接的改进关系。IEE 复用了 HALP 的硬件感知压缩框架，包括延迟查找表（Latency Lookup Table）和泰勒重要性准则，但将 HALP 的静态剪枝流程改造为迭代的 exploit-explore 循环。实验结果表明，IEE 以 HALP 约 39% 的训练成本（×0.39 vs ×1.39）实现了更高的推理速度（2736 vs 2597 FPS）和相当的准确率（74.6 vs 74.5），证明动态结构探索比一次性剪枝-微调范式具有更优的精度-效率权衡。

### 与剪枝方法谱系的关系

IEE 位于**训练时动态剪枝**（pruning during training）与**迭代剪枝**（iterative pruning）的交汇点。与传统的一次性剪枝方法（如 **EagleEye**, Li et al., ECCV 2020；**AutoSlim**, Yu et al., NeurIPS 2019）不同，IEE 不依赖预训练模型的权重继承，而是支持从头训练（from scratch）的稀疏化，这使其在训练成本上具有可比性。与基于强化学习的剪枝方法（如 **AMC**, He et al., ECCV 2018）相比，IEE 避免了昂贵的搜索过程，其训练 FLOPs 仅需对基线训练的适度扩展（如 IEE-30% 结构化剪枝仅需 0.39 倍基线训练成本）。

在 N:M 稀疏性（Ampere 架构）这一细分领域，IEE 展现了跨稀疏模式的泛化能力——尽管未针对 N:M 约束进行特殊设计，其统一的剪枝-生长框架在 2:4 稀疏度下仍以 77.5% Top-1 准确率超越了专用方法 **SR-STE**（77.0%），表明 exploit-explore 机制对结构化稀疏模式具有天然的适应性。

### 适用边界与局限

IEE 的适用边界受以下因素制约：

1. **硬件依赖性**：结构化稀疏的实现依赖 HALP 框架中的延迟查找表，该表针对特定 GPU（NVIDIA Titan V）生成。迁移到其他硬件平台（如移动端 NPU 或新型 GPU 架构）时，需重新构建延迟模型，否则无法保证实际的推理加速。

2. **更新预算调度器的固定性**：更新预算 $\Omega^t$ 的衰减策略采用预定义的指数衰减，未针对不同网络深度或任务复杂度进行自适应调整。对于层间稀疏度分布差异较大的网络，固定调度可能导致某些层过早或过晚停止结构探索。

3. **探索空间的完整重激活开销**：Reactivate & Explore 阶段需要暂时激活所有被剪枝参数并训练 Q 步，其计算成本与探索空间大小成正比。在高稀疏度（>95%）场景下，探索空间远大于活动结构，此时的训练开销可能抵消动态探索的收益。

4. **架构验证范围有限**：实验验证集中在 ResNet 系列（ResNet-50, WideResNet-22-2）和 MobileNet-V1 上，对于 Transformer、Vision Transformer 或大型语言模型等注意力机制主导的架构，IEE 的 exploit-explore 机制是否依然有效尚待验证。

### 开放问题

1. **自适应周期调度**：当前 IEE 需要手动设定更新步数 H、J、Q 及总更新步数 T。能否基于训练过程中的梯度方差、重要性分数稳定性或架构收敛速度（如 Figure 5(a) 中的 IoU 指标）自适应地调整这些超参数？

2. **硬件感知的去耦合**：能否通过可微的延迟代理模型替代预构建的延迟查找表，使 IEE 在无需硬件先验知识的情况下实现硬件感知剪枝？这将显著提升方法的即插即用性。

3. **探索空间的采样策略**：是否可以对探索空间进行子采样（如仅重激活最近被剪枝的参数或高梯度参数），在保持探索效果的同时降低 Reactivate & Explore 阶段的训练开销？

4. **大规模模型的扩展性**：在大型语言模型（如 LLaMA 系列）的稀疏化场景中，IEE 的 exploit-explore 循环是否能够有效发现 Transformer 注意力头和 FFN 层的结构化稀疏模式？冻结活动结构进行探索的策略在分布式训练环境下如何实现高效的梯度通信？

## 原文 PDF

![[paperPDFs/WACV_2025/Advancing_Weight_and_Channel_Sparsification_with_Enhanced_Saliency.pdf]]
