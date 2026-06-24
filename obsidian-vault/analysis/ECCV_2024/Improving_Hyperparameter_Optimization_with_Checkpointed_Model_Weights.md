---
title: "Improving Hyperparameter Optimization with Checkpointed Model Weights"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Improving_Hyperparameter_Optimization_with_Checkpointed_Model_Weights.pdf
aliases:
- FMSF
- IHOCMW
tags:
- ECCV_2024
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "在DyHPO的GP代理模型中增加一个由排列不变图元网络（PIGMN）编码的模型权重输入通道，使HPO能够利用训练权重的结构化先验。"
primary_logic: "将神经网络权重视为图结构，并通过PIGMN进行排列不变的特征提取，可以有效捕获与任务、架构和训练过程相关的先验知识，从而显著提升HPO的排序准确性和收敛速度，尤其在跨模型选择与微调的场景中。"
claims:
- "FMS-GMN在所有模型中心（Simple CNN Hub, PTMHub SVHN, PTMHub CIFAR-10）和所有预算下均取得最高的Kendall’s τ值，优于DyHPO等基线。"
- "FMS-GMN的后悔值（regret）在整个计算预算范围内持续低于最强基线DyHPO，证明其找到更好配置的效率更高。"
- "FMS-GMN在多数据集训练后展现正向泛化能力，其后悔值低于仅在当前数据集训练的版本，表明权重特征能跨任务传递知识。"
- "消融实验证明，即使移除学习曲线CNN特征，FMS变体仍维持较好性能，而DyHPO无CNN则性能急剧下降，说明权重特征提供了强健的互补信息。"
---

# Improving Hyperparameter Optimization with Checkpointed Model Weights

> [!tip] 核心洞察
> 将神经网络权重视为图结构，并通过PIGMN进行排列不变的特征提取，可以有效捕获与任务、架构和训练过程相关的先验知识，从而显著提升HPO的排序准确性和收敛速度，尤其在跨模型选择与微调的场景中。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 利用检查点模型权重改进超参数优化 |
| 英文题名 | Improving Hyperparameter Optimization with Checkpointed Model Weights |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2406.18630); [GitHub](https://github.com/NVlabs/forecasting-model-search); [Project](https://research.nvidia.com/labs/toronto-ai/FMS/) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Forecasting Model Search (FMS) |
| Dataset | Simple CNN Hub (100 epochs), PTMHub SVHN (100 epochs), PTMHub CIFAR-10 (100 epochs), 所有模型中心（计算预算扫描） |

> [!tip] 效果简介
> - Simple CNN Hub (100 epochs) 上，Kendall’s τ 为 0.92，对比 0.77 (DyHPO)，变化 +0.15。
> - PTMHub SVHN (100 epochs) 上，Kendall’s τ 为 0.90，对比 0.76 (DyHPO)，变化 +0.14。
> - PTMHub CIFAR-10 (100 epochs) 上，Kendall’s τ 为 0.91，对比 0.78 (DyHPO)，变化 +0.13。

## 概述

超参数优化（HPO）是深度学习落地的关键瓶颈。现有方法，尤其是以**DyHPO**为代表的多保真度贝叶斯优化，在构建代理模型时仅利用超参数配置、学习曲线和计算预算，却系统性地忽略了训练过程中自然产生的**模型检查点权重**——这些权重隐式编码了架构、数据集、损失景观与优化动态等丰富先验。这一信息缺口限制了代理模型对配置性能的预测精度，尤其在跨模型选择与微调场景中，排序准确性和收敛效率存在明显天花板。

针对上述瓶颈，本文提出 **Forecasting Model Search (FMS)**，核心思路是将检查点权重视为图结构，通过**排列不变图元网络（PIGMN）**提取结构化特征，并将其作为新增输入通道嵌入 DyHPO 的高斯过程深度核代理模型中。这一设计的关键因果机制在于：权重图特征提供了与学习曲线互补的强健信息源，使代理模型能够同时利用“训练结果”（学习曲线）和“训练过程痕迹”（权重演化）进行推断，从而显著提升对配置性能的排序能力和搜索效率。

实验证据构成完整的验证链条：
- **排序准确性**：在 Simple CNN Hub、PTMHub SVHN 和 PTMHub CIFAR-10 三个模型中心上，FMS-GMN 在所有计算预算下均取得最高的 Kendall’s τ 值（Table 1），较最强基线 DyHPO 提升 0.13–0.15。
- **收敛效率**：在整个计算预算范围内，FMS-GMN 的后悔值（regret）持续低于 DyHPO（Figure 2），证明其能以更少的计算资源找到更优配置。
- **跨任务泛化**：多数据集训练的 FMS-GMN 后悔值低于仅在当前数据集训练的版本（Figure 3），表明权重特征能跨任务传递知识，具备正向泛化能力。
- **信息互补性**：消融实验显示，移除学习曲线 CNN 模块后，FMS 变体仍保持较好性能，而 DyHPO 无 CNN 则完全失效（Figure 4），强有力地证明了权重特征提供了有效的替代信息。

方法定位上，FMS 属于**多保真度贝叶斯优化**框架下的代理模型增强方法，通过引入权重特征通道扩展了深度核 GP 的输入空间，可与现有采集函数和预算分配策略无缝集成。其局限性包括对检查点存储的依赖、GP 可扩展性对大规模评估的约束，以及当前仅在中小规模图像分类任务上验证。

## 背景与动机

### 超参数优化与多保真度贝叶斯优化

深度学习模型的性能高度依赖超参数配置的选择，包括学习率、批量大小、正则化系数以及网络架构本身。超参数优化（HPO）的目标是在有限的计算预算内，从庞大的搜索空间中找到使目标函数（如验证集准确率）最大化的配置。贝叶斯优化（BO）是解决这一问题的核心范式，其通过构建目标函数的概率代理模型（通常为高斯过程，GP）来指导搜索，在每一轮选择期望提升（Expected Improvement, EI）最大的候选配置进行评估。

然而，完整训练一个深度学习模型以评估单个超参数配置的计算成本极高。多保真度贝叶斯优化（Multi-fidelity BO）通过允许在不同预算水平（如训练轮数）下评估配置来缓解这一问题。其核心思想是：低预算下的性能可以部分预测高预算下的性能，从而在有限资源内探索更多候选配置。DyHPO（Wistuba et al.）是该方向的代表性方法，它使用深度核高斯过程作为代理模型，将超参数配置 $\mathbf{x}$、当前预算 $j$ 以及截至上一预算的学习曲线 $\mathbf{Y}_{i,j-1}$ 共同映射到一个特征空间，再通过可学习的核函数建模配置间的相似性：

$$\mathbf{K}(\pmb{\theta}, \mathbf{w}, \mathcal{D}) := k(\varphi(\mathbf{x}_i, \mathbf{Y}_{i,j-1}, j; \mathbf{w}), \varphi(\mathbf{x}_{i'}, \mathbf{Y}_{i',j'-1}, j'; \mathbf{w}); \pmb{\theta})$$

该深度核的参数 $\pmb{\theta}$ 和神经网络权重 $\mathbf{w}$ 通过最大化数据似然（即最小化负对数边缘似然 $\mathcal{L}(\mathcal{D})$）联合学习。DyHPO 在此基础上使用多保真度采集函数 $\mathrm{EI}_{\mathrm{MF}}$ 同时选择下一评估的配置和预算，并通过增量预算分配策略逐步增加训练轮数。

### 被忽视的信息源：模型检查点权重

尽管 DyHPO 通过引入学习曲线显著提升了 HPO 的预测精度，但其代理模型在构建时忽略了一个在深度学习训练过程中天然存在且信息丰富的信号——**模型检查点权重**（checkpointed model weights）。在标准的多保真度 HPO 流程中，每个配置在特定预算下训练后都会产生一组神经网络权重。这些权重并非随机噪声，而是隐式编码了以下结构化先验：

- **架构信息**：权重的张量形状和连接模式直接反映了网络结构；
- **数据集特征**：权重值本身是模型对特定数据分布的适应结果；
- **优化动态**：不同检查点之间的权重变化轨迹包含了损失景观和收敛速度的信息；
- **配置交互效应**：超参数如何影响模型参数的学习过程，被直接记录在权重的数值模式中。

现有方法将这部分信息完全丢弃，仅保留标量形式的学习曲线（如损失值或准确率序列）。这构成了当前 HPO 代理模型的一个关键瓶颈：**学习曲线是对高维权重空间的极度压缩，丢失了大量关于模型状态和任务结构的细粒度信息**。

### 核心动机与研究问题

本文的核心动机在于回答一个直接的问题：**能否将模型检查点权重作为代理模型的额外输入，从而提升 HPO 的预测精度和搜索效率？**

这一动机面临两个关键技术挑战：

1. **排列不变性（Permutation Invariance）**：神经网络中的神经元没有内在顺序，对同一层的神经元进行重排会产生功能完全等价但权重张量形式不同的网络。任何处理权重的模型必须对这种排列变换保持输出不变，否则会将对同一网络状态的不同表示误判为不同配置。
2. **异构架构处理**：HPO 搜索空间通常包含不同架构的候选模型（如不同层数、不同通道数的 CNN），其特征提取器需要能够处理结构各异的权重图，而非仅限于同构网络。

解决上述挑战，有望使 HPO 代理模型获得超越传统学习曲线的信息增益，尤其在跨模型选择与微调的场景中，权重特征可能提供关于模型-数据-优化三者交互的结构化先验，从而加速搜索收敛并提升排序准确性。

## 核心创新

### 问题瓶颈：现有HPO代理模型的信息盲区

当前主流的多保真度贝叶斯优化方法（以 **DyHPO** (Wistuba et al.) 为代表）在构建代理模型时，其输入特征空间仅包含三个信息通道：超参数配置 $\mathbf{x}$、部分学习曲线 $\mathbf{Y}_{i,j-1}$ 和当前预算 $j$。这一设计存在一个关键的信息盲区——它完全忽略了训练过程中自然产生的**模型检查点权重**（checkpointed model weights）。这些权重张量中隐式编码了架构特性、数据集难度、损失景观和优化轨迹等丰富先验，但在现有HPO流程中未被利用。

### 核心因果机制：权重特征通道的引入

FMS 的核心创新在于对代理模型的输入特征空间进行了一次**因果性扩展**——在 DyHPO 的深度核高斯过程（Deep Kernel GP）中增加了一个模型权重输入通道。这一改变的因果逻辑链如下：

1. **权重图构建**：将任意神经网络检查点的权重重新组织为图结构 $\mathcal{G}^{(0)}(W)$，其中节点对应网络层，边对应层间权重矩阵。这一转换使得异构架构的权重能够被统一表示。

2. **排列不变图元网络（PIGMN）编码**：通过多层图卷积与节点平均聚合，从权重图中提取排列不变特征向量 $\xi$：
   $$\xi(\mathcal{G}^{(0)}) = \sum_{v \in V(\mathcal{G}^{L})} \frac{\mathbf{h}_v^{L}}{|V(\mathcal{G}^{L})|}, \quad \mathcal{G}^{(l+1)} = \sigma\left(\sum_{k=1}^{K} \Theta_k^{(l)} \ast \mathcal{G}^{(l)}\right)$$
   排列不变性确保了权重空间的对称性（如神经元重排）不会影响特征表示，这是将权重作为结构化先验输入的关键设计。

3. **增强核函数**：将权重特征 $\xi$ 与原有特征（超参数、学习曲线CNN特征、预算）拼接，通过混合特征编码器 $\psi$ 生成深度核GP的输入，形成增强核：
   $$\mathbf{K}(\pmb{\theta}, \mathbf{w}) := k(\psi(\mathbf{x}_i, \mathbf{W}_i, \mathbf{Y}_{i,j-1}, j; \mathbf{w}), \psi(\mathbf{x}_{i'}, \mathbf{W}_{i'}, \mathbf{Y}_{i',j'-1}, j'; \mathbf{w}); \pmb{\theta})$$

### 与基线的核心差异

| 特征槽位 | DyHPO 基线 | FMS 改进 |
|---------|-----------|---------|
| 代理模型输入 | 超参数 + 学习曲线 + 预算 | 超参数 + 学习曲线 + 预算 + **模型权重特征** |
| 权重编码方式 | 无 | PIGMN 图元网络（排列不变） |
| 核函数 | $k(\varphi(\mathbf{x}_i, \mathbf{Y}_{i,j-1}, j; \mathbf{w}), \ldots)$ | $k(\psi(\mathbf{x}_i, \mathbf{W}_i, \mathbf{Y}_{i,j-1}, j; \mathbf{w}), \ldots)$ |

这一改变的本质在于：FMS 让代理模型能够**直接“看到”训练状态本身**，而非仅通过标量性能曲线间接推断。权重特征提供了与学习曲线互补的结构化信息——消融实验证明，即使移除学习曲线CNN模块，FMS变体仍能维持可观的HPO性能，而 DyHPO 在同样条件下完全失效（Figure 4, Section A.7）。

### 创新带来的能力跃迁

权重特征的引入产生了三个超出基线能力的效应：

1. **跨模型结构的知识迁移**：PIGMN 的图结构编码使得 FMS 能够处理异构架构的权重，在多数据集上训练后展现出正向泛化能力——其后悔值（regret）持续低于仅在单数据集训练的版本（Figure 3），证明权重特征可以跨任务传递知识。

2. **排序准确性的显著提升**：在 Simple CNN Hub、PTMHub SVHN 和 PTMHub CIFAR-10 三个模型中心上，FMS-GMN 在所有预算下均取得最高的 Kendall’s $\tau$ 值（分别达到 0.92、0.90、0.91），相比 DyHPO 基线提升 0.13–0.15（Table 1）。

3. **计算效率的全程改善**：FMS-GMN 的后悔值在整个计算预算范围内持续低于最强基线 DyHPO（Figure 2），表明其能够更快地定位高质量配置。

## 整体框架

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2406_18630/figures/006_Figure_4.jpg]]
*Figure 4: We show the regret against the compute budget for the hyperparameter optimization (HPO) method across different hubs in each plot and various methods in each color. The regret values reflect the difference between the actual performance and the best possible performance over time. Lower regret indicates better performance. Our method, FMS-GMN, consistently shows lower regret over time across all hubs, demonstrating its effectiveness in HPO. The compute budget is measured in epochs (a full pass through the dataset), standardizing the compute effort across different tasks. FMS-NFN doesn’t support diverse architectures, so it only runs on Simple CNN Hub*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2406_18630/figures/001_Figure_1.jpg]]
*Figure 1: We show an overview of our method, Forecasting Model Search (FMS), which builds on DyHPO’s multifidelity method from Algorithm 1. Novel components of FMS are highlighted in blue and further detailed in Algorithm 2. We include DyHPO’s features from the hyperparameter configuration, budget, and learning curve [15]. Notably, we also featurize the model’s checkpointed weights W with a permutation-invariant graph metanetwork (PIGMN) as in Section 3.1 for input to a deep kernel GP (see Equation 2/7). This provides the HPO with an – often pre-existing – rich source of information, which implicitly includes the architecture, dataset, loss, and optimization process. FMS shows improved predictions ab...*

Forecasting Model Search (FMS) 以 DyHPO 的多保真度贝叶斯优化管线为基础，通过引入模型检查点权重作为额外信息源来增强代理模型的预测能力。其整体框架由六个核心模块串联构成，数据流从超参数配置与模型训练出发，最终输出下一轮评估的候选配置与预算。

### 管线模块与数据流

**权重图构建** 是 FMS 的入口模块。当某个超参数配置以预算 $j$ 完成训练后，系统保存的检查点权重 $\mathbf{W}$ 被转化为图结构 $\mathcal{G}^{(0)}(\mathbf{W})$，其中节点对应神经网络的各层，边对应层间权重矩阵。这一转化使权重的拓扑信息得以保留，为后续的结构化特征提取奠定基础。

**PIGMN 特征提取器** 接收权重图 $\mathcal{G}^{(0)}$，通过多层图卷积与节点平均操作生成排列不变特征向量 $\xi$（见公式 6）。排列不变性保证了无论网络内部神经元如何重排，提取的特征保持一致，这是处理神经网络权重的关键设计。

**混合特征编码器** 将来自四个通道的信息拼接融合：
- 超参数配置 $\mathbf{x}_i$
- 由 CNN 编码的学习曲线特征 $\mathbf{Y}_{i,j-1}$
- 当前预算 $j$
- PIGMN 提取的权重特征 $\xi(\mathcal{G}^{(0)})$

这些异构特征通过全连接网络 $\psi$ 映射到统一的特征空间，形成深度核高斯过程（Deep Kernel GP）的输入表示。

**深度核高斯过程** 作为代理模型的核心，利用学习到的混合特征构建增强核函数（见公式 7）：
$$\mathbf{K}(\pmb{\theta}, \mathbf{w}) := k(\psi(\mathbf{x}_i, \mathbf{W}_i, \mathbf{Y}_{i,j-1}, j; \mathbf{w}), \psi(\mathbf{x}_{i'}, \mathbf{W}_{i'}, \mathbf{Y}_{i',j'-1}, j'; \mathbf{w}); \pmb{\theta})$$

该核函数同时编码了超参数、训练动态（学习曲线）和模型结构先验（权重），提供预测均值与方差。核参数 $\pmb{\theta}$ 与网络权重 $\mathbf{w}$ 通过最大化负对数边缘似然联合优化。

**多保真度采集函数** 基于 GP 后验预测，通过最大化多保真度期望提升 $\mathrm{EI}_{\mathrm{MF}}$（公式 5）选择下一轮评估的配置与预算对 $(\mathbf{x}, j)$。

**预算分配与检查点** 模块负责动态增量预算的执行：恢复上一检查点继续训练至目标预算，记录新的权重检查点和验证性能，将观测数据 $\mathcal{D}$ 反馈至代理模型以更新 GP。

### 与 DyHPO 的核心差异

FMS 与 DyHPO 的唯一结构性差异在于代理模型的输入特征空间。DyHPO 的深度核仅包含超参数、学习曲线和预算三个输入通道（公式 2），而 FMS 在此基础上增加了由 PIGMN 编码的模型权重通道（公式 7）。这一扩展使代理模型能够利用训练过程中自然产生的检查点权重所蕴含的架构、数据集与优化动态等结构化先验。实验证据表明，这一信息通道提供了与学习曲线互补的强健信号——消融实验中，即使移除学习曲线 CNN 模块，FMS 变体仍能维持可观的 HPO 性能，而 DyHPO 在无 CNN 时性能急剧下降（见 Figure 4 及附录 A.7）。

### 算法流程

FMS 的整体优化循环如 Algorithm 2 所示，蓝色标注部分标识了相对于 DyHPO 的新增步骤：权重图构建、PIGMN 特征提取，以及增强核中权重特征的注入。GP 代理模型的训练沿用 DyHPO 的梯度优化框架，通过 Adam 优化器最小化负对数边缘似然来学习核参数与网络权重。

## 核心模块与公式推导

### 基础代理模型：深度核高斯过程

FMS 建立在 **DyHPO**（Wistuba et al.）的多保真度贝叶斯优化框架之上。DyHPO 使用深度核高斯过程作为代理模型，其核函数通过神经网络 $\varphi$ 将超参数配置 $\mathbf{x}_i$、学习曲线 $\mathbf{Y}_{i,j-1}$ 和预算 $j$ 映射到特征空间：

$$\mathbf{K}(\pmb{\theta}, \mathbf{w}, \mathcal{D}) := k(\varphi(\mathbf{x}_i, \mathbf{Y}_{i,j-1}, j; \mathbf{w}), \varphi(\mathbf{x}_{i'}, \mathbf{Y}_{i',j'-1}, j'; \mathbf{w}); \pmb{\theta})$$

核参数 $\pmb{\theta}$ 和神经网络权重 $\mathbf{w}$ 通过最大化数据似然联合学习，损失函数为负对数边缘似然：

$$\mathcal{L}(\mathcal{D}) = \frac{1}{2} \mathbf{y}^\top \mathbf{K}(\boldsymbol{\theta}, \mathbf{w}, \mathcal{D})^{-1} \mathbf{y} + \frac{1}{2} \log |\mathbf{K}(\boldsymbol{\theta}, \mathbf{w}, \mathcal{D})| + \frac{n}{2} \log 2\pi$$

其梯度为：

$$\nabla_{\pmb{\theta}, \mathbf{w}} \mathcal{L}(\mathcal{D}) = -\left( \mathbf{y}^\top \mathbf{K}(\pmb{\theta}, \mathbf{w}, \mathcal{D})^{-1} \mathbf{y} - \operatorname{Tr}\left( \mathbf{K}(\pmb{\theta}, \mathbf{w}, \mathcal{D})^{-1} \right) \right)$$

给定训练数据 $\mathcal{D}$，GP 在新点 $\mathbf{x}_*$ 处的后验预测均值与方差为：

$$\mu(\mathbf{x}_*) = \mathbf{k}_*^\top (\mathbf{K} + \sigma_n^2 \mathbf{I})^{-1} \mathbf{y}, \quad \sigma^2(\mathbf{x}_*) = k(\mathbf{x}_*, \mathbf{x}_*) - \mathbf{k}_*^\top (\mathbf{K} + \sigma_n^2 \mathbf{I})^{-1} \mathbf{k}_*$$

### FMS 核心创新：权重图构建与 PIGMN 特征提取

FMS 的核心创新在于向代理模型引入**模型检查点权重**作为额外输入。权重被组织为图结构 $\mathcal{G}^{(0)}(W)$：节点对应网络的各层，边对应层间权重矩阵。该图随后由**排列不变图元网络（PIGMN）** 处理，通过多层图卷积提取全局特征：

$$\xi (\mathcal{G}^{(0)}) = \sum_{v \in V(\mathcal{G}^{L})} \frac{\mathbf{h}_v^{L}}{|V(\mathcal{G}^{L})|}, \quad \mathcal{G}^{(l+1)} = \sigma\left(\sum_{k=1}^{K} \Theta_k^{(l)} \ast \mathcal{G}^{(l)}\right)$$

其中 $\mathbf{h}_v^{L}$ 是第 $L$ 层图卷积后节点 $v$ 的隐藏表示，通过平均所有节点表示获得排列不变的特征向量 $\xi$。$\Theta_k^{(l)}$ 为第 $l$ 层第 $k$ 个卷积核，$\ast$ 表示图卷积操作，$\sigma$ 为非线性激活函数。

### 增强核函数与混合特征编码器

FMS 将 PIGMN 提取的权重特征 $\xi$ 与原有输入拼接，构建增强核函数：

$$\mathbf{K}(\pmb{\theta}, \mathbf{w}) := k(\psi(\mathbf{x}_i, \mathbf{W}_i, \mathbf{Y}_{i,j-1}, j; \mathbf{w}), \psi(\mathbf{x}_{i'}, \mathbf{W}_{i'}, \mathbf{Y}_{i',j'-1}, j'; \mathbf{w}); \pmb{\theta})$$

其中 $\psi$ 为混合特征编码器，其输入包括：
- 超参数配置 $\mathbf{x}_i$
- 模型检查点权重 $\mathbf{W}_i$（经 PIGMN 编码为 $\xi$）
- 学习曲线 $\mathbf{Y}_{i,j-1}$（经 CNN 编码）
- 预算 $j$

这些特征拼接后通过全连接网络生成深度核 GP 的输入。该设计使 GP 能够同时利用训练动态的结构化先验（权重特征）和性能轨迹信息（学习曲线），从而显著提升排序准确性和收敛速度。

### 多保真度采集函数

FMS 沿用 DyHPO 的多保真度期望改进（Expected Improvement）作为采集函数，同时选择下一评估的配置与预算：

$$\mathrm{EI}_{\mathrm{MF}}(\mathbf{x}, j | \mathcal{D}) = \mathbb{E}\left[ \max\{ f(\mathbf{x}, j) - y_j^{\max}, 0 \} \right]$$

其中 $y_j^{\max}$ 为预算 $j$ 下的当前最优观测值，$f(\mathbf{x}, j)$ 为 GP 代理模型在配置 $\mathbf{x}$ 和预算 $j$ 下的预测。

## 实验与分析

### 核心性能对比：排序准确性与收敛效率

FMS-GMN在所有评估的模型中心（model hub）和计算预算下，均展现出最优的超参数配置排序能力。表1汇总了不同预算下的Kendall’s τ值。在Simple CNN Hub上，FMS-GMN在100 epoch预算时达到0.92的τ值，比最强基线**DyHPO**（Wistuba et al.）的0.77提升了0.15。在更具挑战性的PTMHub SVHN和PTMHub CIFAR-10上，FMS-GMN同样分别取得0.90和0.91的τ值，分别优于DyHPO 0.14和0.13。值得注意的是，基于神经功能网络（NFN）的变体**FMS-NFN**因无法处理异构架构的权重，仅能在Simple CNN Hub上运行，其性能与FMS-GMN接近，但通用性受限。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2406_18630/figures/002_Table_1.jpg]]
*Table 1: Kendall’s τ values at various budgets for different model hubs. NFN variants can not process the weights of diverse architectures [28], so they are not run on either PTM hub. Figure 2 investigates the effectiveness of FMS by recording regret over time in various settings. Lower regret values indicate better performance with Kendall’s τ coefficient recorded at the 50th and 100th epochs in Table 1. Our results show that FMS-GMN achieves the best performance, with consistently lower regret per compute and higher Kendall’s τ values than other methods*

排序能力的优势直接转化为更高效的优化过程。图2展示了不同模型中心下后悔值（regret）随计算预算的变化曲线。FMS-GMN（蓝色）的后悔值在整个预算范围内持续低于最强基线DyHPO（红色），表明FMS能以更少的计算资源找到更接近全局最优的配置。这种优势在Simple CNN Hub、PTMHub SVHN和PTMHub CIFAR-10三个场景中均保持一致，验证了权重特征在不同任务上的普适有效性。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2406_18630/figures/004_Figure_2.jpg]]
*Figure 2: In each plot, we show the regret against the compute budget across different hubs and various hyperparameter optimization (HPO) methods in each color. The regret values reflect the difference between the actual performance and the best possible performance over time. Lower regret indicates better performance. Our method, FMS-GMN in blue, consistently shows lower regret than the strongest baseline DyHPO in red. This persists over most compute budgets across all hubs, demonstrating that our method is effective for HPO. FMS-NFN in cyan doesn’t support diverse architectures, so it only runs on the Simple CNN Hub. Figure 3 further investigates the generalization of our FMS-GMN method, while Appe...*

### 泛化能力验证

FMS的一个关键优势在于其跨任务的知识迁移潜力。图3对比了两种训练模式下的后悔值：FMS-GMN with generalization（蓝色）在多数据集上联合训练，FMS-GMN without generalization（红色）仅在当前目标数据集上训练。结果显示，泛化设置下的后悔值持续低于非泛化设置，表明FMS能够有效利用来自其他任务和架构的训练权重信息，加速在新任务上的收敛。这一发现意味着权重特征编码了超越单任务边界的先验知识——包括优化动态、架构归纳偏置和数据集特性——使HPO代理模型能够从更广泛的训练经验中受益。

### 消融实验：权重特征的关键作用

消融实验揭示了模型权重特征相对于学习曲线特征的互补性和稳健性。图4展示了移除学习曲线CNN编码器后的性能变化。关键发现是：FMS变体在无CNN模块时仍能维持可观的HPO性能，而DyHPO在移除CNN后性能急剧崩溃。这一对比强有力地证明，模型权重特征提供了与学习曲线互补的丰富信息源。权重中蕴含的架构结构、训练轨迹和数据集特征，即使在没有显式学习曲线输入的情况下，也能为代理模型提供足够的预测信号。这解释了FMS在低预算场景下的优异表现——当学习曲线尚不完整时，权重特征已能提供可靠的性能预测依据。

### 失败模式与边界条件

尽管FMS展现出显著优势，实验和分析揭示了若干明确的边界条件。首先，FMS-NFN变体无法处理异构架构集合，这限制了其在PTMHub等包含多种预训练模型架构的场景中的应用。其次，所有方法的性能增益随预算增加而趋于饱和，表明权重特征在早期预算阶段的信息增益最为显著。此外，实验覆盖范围局限于小至中等规模的图像分类任务，对于NLP、语音或大规模基础模型的泛化能力尚未验证。GP代理模型固有的可扩展性瓶颈也限制了训练数据的规模，尽管采用了共轭梯度近似，大规模HPO评估仍面临计算挑战。最后，当前方法假设检查点始终可用且完整；当部分配置的检查点缺失时，系统的鲁棒性将受到影响。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2406_18630/figures/005_Table_2.jpg]]
*Table 2: Glossary and Notation*

## 方法谱系与知识库定位

### 多保真度贝叶斯优化的继承与突破

FMS 直接构建于 **DyHPO**（Wistuba et al.）之上，继承了其完整的“深度核高斯过程 + 多保真度期望改进”框架：代理模型使用神经网络 $\varphi$ 将超参数配置 $\mathbf{x}$、学习曲线 $\mathbf{Y}_{i,j-1}$ 和预算 $j$ 映射到特征空间，再通过 GP 核函数建模配置间相关性，最后以 $\mathrm{EI}_{\mathrm{MF}}$ 采集函数同时选择下一配置与预算。FMS 的核心突破在于**扩展了代理模型的输入通道**——在原有三要素之外，增加了一个由排列不变图元网络（PIGMN）编码的模型权重特征通道，使核函数从：

$$\mathbf{K}(\pmb{\theta}, \mathbf{w}, \mathcal{D}) := k(\varphi(\mathbf{x}_i, \mathbf{Y}_{i,j-1}, j; \mathbf{w}), \varphi(\mathbf{x}_{i'}, \mathbf{Y}_{i',j'-1}, j'; \mathbf{w}); \pmb{\theta})$$

增强为：

$$\mathbf{K}(\pmb{\theta}, \mathbf{w}) := k(\psi(\mathbf{x}_i, \mathbf{W}_i, \mathbf{Y}_{i,j-1}, j; \mathbf{w}), \psi(\mathbf{x}_{i'}, \mathbf{W}_{i'}, \mathbf{Y}_{i',j'-1}, j'; \mathbf{w}); \pmb{\theta})$$

这一改动看似“加一个输入”，实则**改变了 HPO 代理模型可利用的信息结构**：权重张量 $\mathbf{W}$ 隐式编码了架构拓扑、数据集特性、损失景观和优化轨迹，而 PIGMN 的排列不变图卷积设计保证了这些信息在不同层重排下保持稳定。消融实验提供了因果证据——当移除学习曲线 CNN 模块后，FMS 变体仍维持较好性能，而 DyHPO 在同等条件下性能急剧崩溃（Figure 4），表明权重特征提供了与学习曲线互补且更鲁棒的先验信息。

### 与相关工作的边界关系

**权重编码方法对比**。FMS 实验了三种权重编码策略：PIGMN（FMS-GMN）、Neural Functional Network（FMS-NFN）和直接扁平化（FMS-FLAT）。FMS-NFN 受限于 NFN 对同构架构的要求，无法处理 PTMHub 中异构的预训练模型集合（Table 1 中留空）；FMS-FLAT 丧失了置换不变性，性能劣于 FMS-GMN。这表明**图结构先验 + 置换不变性**是有效利用权重的关键设计选择，而非简单的“多一个输入”。

**与标准 BO 和随机搜索的差距**。在 Simple CNN Hub 100 epoch 预算下，FMS-GMN 的 Kendall’s $\tau$ 达到 0.92，显著优于 DyHPO 的 0.77（Table 1）；在 PTMHub SVHN 和 CIFAR-10 上同样保持 0.13–0.15 的领先。后悔值曲线（Figure 2）显示 FMS-GMN 在整个计算预算范围内持续低于 DyHPO，证明其不仅排序更准，且能以更少总计算量找到更优配置。

**跨任务泛化的独特能力**。FMS 展现出标准 HPO 方法不具备的特性：在多数据集上训练后，其在新任务上的后悔值**低于**仅在当前数据集训练的版本（Figure 3）。这意味着权重特征捕获了可跨任务迁移的元知识——架构模式、优化动力学等——使 FMS 进入“摊销优化”的范畴，而 DyHPO 等传统方法完全依赖当前任务的观测数据。

### 适用边界与结构局限

**计算与存储开销**。FMS 依赖训练过程中保存的模型检查点，这对存储和网络传输提出额外需求；PIGMN 的前向推理和反向传播训练也增加了代理模型更新的计算成本。在 GP 代理模型本身已受限于可扩展性（尽管使用了共轭梯度近似）的背景下，这进一步约束了可处理的评估规模。

**任务与规模范围**。当前实验仅覆盖小到中等规模的图像分类任务（Simple CNN Hub、PTMHub 上的 SVHN 和 CIFAR-10），尚未在 NLP、语音或其他模态上验证。权重特征能否在更大规模模型（如数十亿参数）或根本不同的架构范式（如 Transformer）上保持有效性，仍是开放问题。

**超参数空间假设**。方法假设搜索空间固定且预算（训练轮数）已知可控，不支持动态变化的搜索空间或更现实的计算成本模型（如不同硬件、不同模型大小导致的异构时间成本）。与所有基于 BO 的方法类似，当超参数维度超过数十个时，FMS 同样面临维度灾难。

**权重特征鲁棒性**。当前设计中权重特征为必选输入，当部分检查点缺失或不可用时，方法缺乏优雅的退化机制——无法像移除 CNN 模块那样平滑回退到 DyHPO 级别的性能。

### 开放问题与未来方向

1. **跨领域迁移**：FMS 能否在 NLP、语音、强化学习等任务上复现其排序优势和泛化能力？尤其在架构高度异构（如 CNN + Transformer 混合搜索空间）时，PIGMN 的图表征是否仍有效？

2. **文本上下文融合**：能否将 LLM 嵌入的代码文档、README 文件等文本信息作为额外上下文通道注入代理模型，进一步提升 HPO 的冷启动效率？

3. **鲁棒退化机制**：是否可将权重特征设计为可选输入，使方法在无检查点或检查点不完整时自动退化为标准 DyHPO，从而在实用部署中兼顾性能与容错？

4. **与动态调度结合**：FMS 当前假设固定预算的增量训练，如何将其与基于种群的训练（PBT）或自适应超参数调度（hyperparameter schedules）结合，以支持训练过程中动态调整超参数？

5. **异构成本模型**：当计算成本无法预先精确界定（例如不同 GPU 型号、不同模型大小导致每步时间差异显著）时，如何调整多保真度采集函数中的预算分配策略？

6. **搜索空间扩展**：如何支持动态变化的超参数搜索范围（如神经架构搜索中可变层数带来的条件参数），以及如何将有效维度扩展到数十个以上？

## 原文 PDF

![[paperPDFs/ECCV_2024/Improving_Hyperparameter_Optimization_with_Checkpointed_Model_Weights.pdf]]
