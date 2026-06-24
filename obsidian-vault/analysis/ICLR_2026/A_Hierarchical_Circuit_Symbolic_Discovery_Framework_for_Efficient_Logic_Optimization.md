---
title: "A Hierarchical Circuit Symbolic Discovery Framework for Efficient Logic Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Hierarchical_Circuit_Symbolic_Discovery_Framework_for_Efficient_Logic_Optimization.pdf
aliases:
- HCSDFH
- HCSDFELO
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/neuroscience_cognitive_science
core_operator: "评分函数（scoring function）的准确性和效率，它决定了LO启发式算法中哪些节点级变换被保留或剪枝。"
primary_logic: "受图神经网络（GNN）消息传递机制的启发，提出层次化符号树表示，通过可解释且计算高效的符号聚合操作捕获电路图的多层结构信息，从而替代昂贵的GNN推理。"
claims:
- "HIS-Mfs2在六个挑战性电路上平均运行时间提升27.22%，电路尺寸减少6.95%"
- "HIS在EPFL和IWLS基准上平均推理速度比COG快296倍和254倍"
- "HIS在六个电路上的top-50%预测召回率一致优于所有基于图和基于节点的基线方法"
- "EPFL (Hyp, Square, Multiplier, DesPerf, Ethernet, Conmax) 上 And Reduction (AR) ↑ = 566, 6, 22, 936, 37, 647"
---

# A Hierarchical Circuit Symbolic Discovery Framework for Efficient Logic Optimization

> [!tip] 核心洞察
> 受图神经网络（GNN）消息传递机制的启发，提出层次化符号树表示，通过可解释且计算高效的符号聚合操作捕获电路图的多层结构信息，从而替代昂贵的GNN推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向高效逻辑优化的层次化电路符号发现框架 |
| 英文题名 | A Hierarchical Circuit Symbolic Discovery Framework for Efficient Logic Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=YaXSEbRrHP); [GitHub](https://github.com/MIRALab-USTC/HIS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/neuroscience_cognitive_science |
| Method | Hierarchical Circuit Symbolic Discovery Framework (HIS) |
| Dataset | EPFL (Hyp, Square, Multiplier, DesPerf, Ethernet, Conmax), EPFL + IWLS (六个电路) |

> [!tip] 效果简介
> - EPFL (Hyp, Square, Multiplier, DesPerf, Ethernet, Conmax) 上，And Reduction (AR) ↑ 为 566, 6, 22, 936, 37, 647，对比 COG: 435, 6, 21, 732, 36, 259; CMO: 142, 6, 22, 900, 2, 730; Random: 563, 3, 18, 906, 19, 579; Effisyn: 498, 3, 22, 886, 24, 593，变化 HIS在Hyp上AR最高（566），在DesPerf上AR最高（936），在Ethernet上AR最高（37）。
> - EPFL (Hyp, Square, Multiplier, DesPerf, Ethernet, Conmax) 上，Times (s) ↓ 为 85.46, 10.69, 13.52, 22.84, 13.19, 13.63，对比 COG: 198.09, 14.70, 17.07, 29.01, 18.30, 16.66; CMO: 129.56, 13.60, 15.08, 22.82, 20.88, 14.43; Random: 238.22, 15.62, 14.99, 23.30, 19.04, 14.25; Effisyn: 218.20, 14.66, 15.51, 24.68, 20.93, 16.76，变化 HIS在所有电路上运行时间最短。
> - EPFL + IWLS (六个电路) 上，平均运行时间提升 为 27.22%，对比 Default Mfs2，变化 27.22%。

## 概述

逻辑优化（Logic Optimization, LO）是现代芯片设计流程中的关键瓶颈。其核心问题在于：LO启发式算法在执行过程中会产生大量节点级变换，其中绝大多数对优化目标无效，却消耗了绝大部分运行时间。现有方法试图通过评分函数（scoring function）来预测并剪枝这些无效变换，但面临两难选择——基于图神经网络（GNN）的方法（如COG、CMO）预测准确但推理成本过高，难以部署在纯CPU的工业环境中；手工设计的轻量级符号函数（如Effisyn）效率虽高但表达能力有限，无法充分捕获电路图的多层结构信息。

本文提出层次化电路符号发现框架（Hierarchical Circuit Symbolic Discovery Framework, HIS），核心思路是：受GNN消息传递机制的启发，用可解释且计算高效的**层次化符号树**替代昂贵的GNN推理。该符号树将GNN的多层邻居聚合操作显式地建模为一系列符号函数（由min、max、mean、sum等聚合算子和数学算子组合而成），每层执行一次符号级别的消息聚合，从而在保持结构感知能力的同时实现极快的推理速度。符号树的生成通过强化学习（PPO）优化结构感知Transformer实现，逐层生成符号序列。

主要结果如下：
- **推理效率**：HIS在EPFL基准上平均推理速度比COG快**296倍**，在IWLS基准上快**254倍**，且推理时间与Effisyn等轻量级方法相当（见表5）。
- **优化性能**：集成到Mfs2启发式后，HIS-Mfs2在六个挑战性电路上平均运行时间提升**27.22%**，电路尺寸减少**6.95%**（见表2）。
- **预测质量**：HIS在top-50%预测召回率上一致优于所有基于图和基于节点的基线方法（见表1）。
- **在线效率**：HIS-Mfs2在EPFL基准上的平均运行时间（85.46s, 10.69s, 13.52s, 22.84s, 13.19s, 13.63s）均短于COG-Mfs2、CMO-Mfs2、Random-Mfs2和Effisyn-Mfs2（见表7）。

方法定位：HIS属于**可学习的符号评分函数**范式，填补了GNN高精度-高成本与手工函数低成本-低表达力之间的空白。其层次化符号树表示本质上是一种**显式、可解释的GNN蒸馏**——将GNN隐式学习的消息传递模式蒸馏为符号表达式，从而在CPU上实现近乎零开销的结构感知推理。

## 背景与动机

逻辑优化（Logic Optimization, LO）是芯片设计流程中的关键环节，其核心是通过一系列节点级变换（如布尔重写、节点消去）来减小电路面积与深度。然而，现有LO启发式算法面临一个根本性瓶颈：在大型工业电路上，大量节点级变换是无效的，导致运行时间过长，严重拖慢设计迭代周期。这一问题在纯CPU部署的工业环境中尤为突出，因为昂贵的GPU推理难以集成到现有的EDA工具链中。

现有方法试图通过评分函数来预测并剪枝无效变换，但存在明显的性能与效率权衡。一方面，基于图神经网络（GNN）的评分函数（如COG、CMO）能够编码电路的结构信息，但其推理成本极高——GNN的逐层消息传递需要大量矩阵运算，在CPU上难以实时运行。另一方面，轻量级的符号评分函数（如Effisyn）虽然推理速度快，但受限于手工设计的简单数学表达式，无法充分捕捉电路的多层结构信息，导致预测精度不足。这一矛盾构成了LO领域的关键缺口：**如何设计一种既具备GNN级别的结构感知能力，又保持符号函数级别的推理效率的评分函数？**

本文受GNN消息传递机制的启发，提出了层次化电路符号发现框架（Hierarchical Circuit Symbolic Discovery, HIS），其核心洞察在于：GNN的逐层聚合过程本质上可以表示为一种可解释的符号计算树。HIS将这一过程显式建模为**层次化符号树**——每一层通过预定义的聚合算子（min, max, mean, sum）和数学算子（+, -, ×, ÷, log, exp）对节点特征进行可解释且计算高效的符号消息聚合，从而替代昂贵的GNN推理。这一设计在保持结构感知能力的同时，将推理复杂度降低到常数级：实验表明，HIS在EPFL和IWLS基准上的平均推理速度分别比COG快296倍和254倍，且推理时间与轻量级基线方法相当。

进一步地，HIS引入了一个基于强化学习的符号生成框架：使用结构感知Transformer逐层生成符号序列，并通过PPO算法优化策略网络。该框架避免了手工设计符号函数的局限性，能够自动为不同电路发现最优的层次化聚合表达式。在六个挑战性电路上的评估显示，HIS-Mfs2（将HIS嵌入Mfs2启发式）相比默认Mfs2实现了平均27.22%的运行时间提升和6.95%的电路尺寸减少，且其top-50%预测召回率一致优于所有基于图和基于节点的基线方法。

## 核心创新

HIS 框架的核心创新在于将逻辑优化中昂贵的 GNN 评分函数替换为一种**层次化符号树表示**，从而在保持甚至提升预测精度的同时，将推理速度提升两个数量级。这一创新精准地解决了现有方法的核心瓶颈：GNN 推理在纯 CPU 工业环境下的高成本与低效率。

**核心洞察与机制创新**

受 GNN 消息传递机制的启发，HIS 提出用可解释且计算高效的符号聚合操作来模拟 GNN 的多层结构信息捕获过程，其核心是 `changed_slots` 中的 **评分函数表示**：从手工设计的轻量级数学表达式或复杂的 GNN 模型，转变为层次化符号树。具体而言，该符号树的每一层都执行一种可解释且高效的消息聚合形式（如 min, max, mean, sum 等聚合算子与数学算子的组合），以捕获电路图的多层结构信息。这相当于将 GNN 的隐式嵌入更新过程，显式地编码为可解析的符号表达式，从而避免了昂贵的矩阵运算。

**学习方式与训练框架**

与现有方法不同，HIS 没有采用手工设计或端到端训练 GNN，而是引入了一个基于强化学习的符号生成框架。该框架使用一个**结构感知的 Transformer** 模型来逐层生成符号序列。具体来说，框架设计了 L 个编码器-only Transformer 模型（实验中 L=2），每个模型 `π_θ_i` 负责生成第 i 层的符号函数。Transformer 在生成过程中不仅考虑了父节点信息，还引入了兄弟节点嵌入，从而更好地捕获了计算树的结构上下文。模型参数通过 **PPO 强化学习算法**进行优化，其奖励函数基于 focal loss 设计，旨在提升对关键节点变换的预测召回率。训练完成后，采用 **Best-of-N (BON)** 集成策略，选择训练奖励最高的 N 个表达式（N=4）构建集成模型，以进一步提升鲁棒性。

**效率与性能的实证优势**

这一系列创新带来了显著的性能提升，主要体现为 `changed_slots` 中的 **推理效率** 变革：

*   **极致的推理速度**：在 EPFL 和 IWLS 基准上，HIS 的平均推理速度相比基于 GNN 的 SOTA 方法 COG 分别快 **296 倍** 和 **254 倍**，同时推理时间与其它轻量级方法相当。
*   **端到端的优化增益**：当 HIS 学习到的评分函数被集成到 Mfs2 逻辑优化启发式算法中（形成 HIS-Mfs2）后，在六个挑战性电路上取得了平均 **27.22%** 的运行时间提升和 **6.95%** 的电路尺寸缩减。
*   **一致的最优预测性能**：在 top-50% 预测召回率这一关键指标上，HIS 在 EPFL 和 IWLS 的所有测试电路上均一致优于所有基于图（COG, CMO）和基于节点（Random, Effisyn）的基线方法。

## 整体框架

![[assets/figures/papers/iclr26_0002_YaXSEbRrHP_A_Hierarchical_Circuit_Symbolic_Discovery_Framew/figures/001_Figure_1.jpg]]
*Figure 1: Our HIS framework learns a hierarchical symbolic tree which performs an interpretable and efficient message aggregation motivated by the graph neural networks (GNNs)*

HIS（Hierarchical Circuit Symbolic Discovery Framework）的核心设计围绕一条清晰的流水线展开：**计算树构建 → 层次化符号树表示 → 结构感知Transformer生成 → PPO强化学习训练 → Best-of-N集成**。整个框架的目标是用一个可解释、计算高效的符号评分函数替代昂贵的GNN推理，从而在逻辑优化（LO）启发式中快速预测哪些节点级变换是有效的。

**流水线各模块的输入输出与因果链路如下：**

1. **计算树构建**：给定一个以节点 $v_0$ 为根的电路子图，将其转换为 $L$ 层计算树 $T_{v_0}^L$，并提取每个节点的5维特征（节点类型、扇入/扇出数等），形成特征矩阵 $\mathbf{H}_{\mathbf{v}_i} \in \mathbb{R}^{n_i \times 5}$。这一步的输出是所有层的节点特征集合 $\mathcal{F} = \bigcup_{i=0}^L \{ \mathbf{H}_{\mathbf{v}_i}^0, \cdots, \mathbf{H}_{\mathbf{v}_i}^5 \}$，作为后续符号树的“原料”。

2. **层次化符号树表示**：定义 $L$ 层符号函数（实验中 $L=2$，与2层GNN配置一致）。每一层 $i$ 执行一个可解释的符号聚合操作——从预定义的聚合算子集合（min, max, mean, sum）和数学算子集合（+, -, ×, ÷, log, exp）中选择并组合，更新节点特征。具体地，对于 $i=0$ 层，函数直接输出评分 $score = \mathbf{F}_0(\hat{\mathbf{H}}_{\mathbf{v}_0})$；对于 $i>0$ 层，函数更新上一层特征 $\hat{\mathbf{H}}_{\mathbf{v}_{i-1}} = \mathbf{F}_i(\hat{\mathbf{H}}_{\mathbf{v}_i}, \mathbf{H}_{\mathbf{v}_{i-1}})$。这种层次化设计模仿GNN的消息传递机制，但用纯符号计算替代了神经网络权重矩阵乘法，使得推理在CPU上极快。

3. **结构感知Transformer生成器**：每层使用一个编码器-only Transformer模型 $\pi_{\theta_i}$，负责生成该层的符号函数序列。与标准Transformer的关键区别在于，该生成器在计算注意力时显式编码了**父节点嵌入**和**兄弟节点嵌入**——即当前节点在计算树中的结构位置信息。生成过程是自回归的：符号序列 $\tau$ 的概率为 $p_{\theta}(\tau) = \prod_{i=1}^{|\tau|} p_{\theta}(\tau_i | \tau_1, \cdots, \tau_{i-1})$。这一设计直接对应了“因果旋钮”：评分函数的准确性和效率取决于能否捕捉电路图的多层结构信息，而结构感知注意力正是为此服务的。

4. **PPO强化学习训练**：将符号序列生成建模为强化学习问题。奖励函数 $r(\tau)$ 定义为基于focal loss的负值：$r(\tau) = -\frac{1}{n} \sum_{i=1}^n [\alpha y_i (1-\hat{y}_i)^\gamma \log(\hat{y}_i) + (1-\alpha)(1-y_i) \hat{y}_i^\gamma \log(1-\hat{y}_i)]$，其中 $\hat{y}_i$ 是符号树对节点变换有效性的预测。优势函数通过组归一化计算：$A_{\theta}(\tau) = (r(\tau) - \bar{r}) / \sigma_r$。PPO的裁剪代理目标函数 $J(\theta)$ 用于稳定更新策略网络。这一训练过程替代了手工设计或端到端GNN训练，使得符号函数可以针对特定电路基准自动优化。

5. **Best-of-N (BON) 集成**：训练完成后，从所有生成的符号树中选择训练奖励最高的 $N=4$ 个表达式构建集成模型。集成投票机制进一步提升预测鲁棒性，是实验中HIS一致优于所有基线的关键因素之一（消融实验显示移除BON导致性能显著下降）。

**关键瓶颈与因果链**：整个流水线直接回应了“逻辑优化启发式中大量节点级变换无效”这一核心瓶颈。传统方法要么使用手工设计的轻量级数学表达式（如Effisyn）但表达能力有限，要么使用复杂的GNN模型（如COG）但推理成本高。HIS的层次化符号树在这两者之间找到了平衡点：符号表达式的推理速度比COG快296倍（EPFL基准）和254倍（IWLS基准），同时通过可学习的符号组合保持了与GNN相当的预测能力。证据显示，HIS在六个挑战性电路上平均运行时间提升27.22%，电路尺寸减少6.95%，且top-50%预测召回率一致优于所有基于图和基于节点的基线方法。

**需要手动验证的点**：虽然论文声称HIS的推理速度与Effisyn等轻量级方法相当，但具体比较数据在Table 5中，建议核实Effisyn的推理时间数值以确保公平性。此外，层次化符号树的层数 $L=2$ 是固定设置，更深层次的探索（如 $L=3$ 或 $L=4$）是否带来性能提升，论文中未提供实验证据，这是一个开放问题。

## 核心模块与公式推导

本节聚焦 HIS 框架中替代昂贵 GNN 推理的核心——层次化符号树表示及其生成与优化机制。所有公式均直接来自论文，不引入未经验证的推导。

### 3.1 层次化符号树表示

HIS 的核心洞察是：受 GNN 消息传递机制启发，可以用一个可解释且计算高效的**层次化符号树**来捕获电路图的多层结构信息，从而替代 GNN 的嵌入计算。

给定以节点 $v_0$ 为根的电路子图，首先按照 (Wang et al.) 的方法将其构建为一个 L 层计算树 $T_{v_0}^L$。每一层 $i$ 包含 $n_i$ 个节点，其节点特征被组织为一个矩阵：

$$
\mathbf{H}_{\mathbf{v}_i} = \left[ \mathbf{h}_{v_i^1} \quad \cdots \quad \mathbf{h}_{v_i^{n_i}} \right]^\top \in \mathbb{R}^{n_i \times 5}
$$

其中 $\mathbf{h}_{v_i^j} \in \mathbb{R}^5$ 是第 $i$ 层第 $j$ 个节点的 5 维特征向量。所有层的特征列集合定义为：

$$
\mathcal{F} = \bigcup_{i=0}^L \{ \mathbf{H}_{\mathbf{v}_i}^0, \cdots, \mathbf{H}_{\mathbf{v}_i}^5 \}
$$

这里的 $\mathbf{H}_{\mathbf{v}_i}^k$ 表示第 $i$ 层节点特征矩阵的第 $k$ 列（即所有节点在该特征维度上的值）。

层次化符号树的关键在于**逐层聚合函数**。对于第 $i$ 层，聚合函数 $\mathbf{F}_i$ 接收当前层的节点特征 $\hat{\mathbf{H}}_{\mathbf{v}_i}$ 和（当 $i > 0$ 时）上一层的原始特征 $\mathbf{H}_{\mathbf{v}_{i-1}}$，并产生输出。其形式为分段函数：

$$
\left\{
\begin{array}{ll}
\operatorname{score} = \mathbf{F}_i \big( \hat{\mathbf{H}}_{\mathbf{v}_i} \big), & \mathrm{if} i = 0, \\
\hat{\mathbf{H}}_{\mathbf{v}_{i-1}} = \mathbf{F}_i \big( \hat{\mathbf{H}}_{\mathbf{v}_i}, \mathbf{H}_{\mathbf{v}_{i-1}} \big), & \mathrm{if} i > 0,
\end{array}
\right.
$$

*   **当 $i = 0$**（最顶层）：聚合函数直接输出一个标量评分 $\operatorname{score}$，用于预测该节点级变换是否有效。
*   **当 $i > 0$**：聚合函数通过对当前层特征 $\hat{\mathbf{H}}_{\mathbf{v}_i}$ 进行符号聚合（如 min, max, mean, sum）并结合上一层的原始特征 $\mathbf{H}_{\mathbf{v}_{i-1}}$，计算出更新后的特征 $\hat{\mathbf{H}}_{\mathbf{v}_{i-1}}$，作为下一层（$i-1$）的输入。

这种设计使得信息从树的叶子节点（最底层）逐层向上传播，最终汇聚到根节点。在实验中，层数 $L$ 被设置为 2，与 2 层 GNN 配置保持一致；更新特征向量的维度 $d$ 被设置为 10。

### 3.2 结构感知 Transformer 生成器

层次化符号树的每层函数 $\mathbf{F}_i$ 并非手工设计，而是由一个**结构感知 Transformer** 模型自动生成。论文设计了 $L$ 个编码器-only 的 Transformer 模型 $\pi_{\theta_i}$，每个模型负责生成第 $i$ 层的符号序列。

生成过程是自回归的。给定一个符号序列 $\tau = (\tau_1, \tau_2, \ldots, \tau_{|\tau|})$，其生成概率为各步条件概率的乘积：

$$
p_{\boldsymbol{\theta}}(\tau) = \prod_{i=1}^{|\tau|} p_{\boldsymbol{\theta}}(\tau_i | \tau_1, \cdots, \tau_{i-1})
$$

这里 $\tau_i$ 是从一个预定义的符号库（包含 +, -, ×, ÷, log, exp 等数学算子以及 min, max, mean, sum 等聚合算子）中选取的 token。Transformer 模型通过自注意力机制，在生成当前 token 时能够关注到已生成的 token 序列，从而保证符号序列的语法和语义一致性。

### 3.3 PPO 强化学习训练

由于符号函数的优化目标（最大化逻辑优化性能）不可微，论文将符号序列生成问题建模为强化学习问题，并使用 PPO 算法进行优化。

**奖励函数** 基于 focal loss 设计，用于评估生成的符号树 $\tau$ 在预测节点级变换有效性上的表现：

$$
r(\tau) = -\frac{1}{n} \sum_{i=1}^n \left[ \alpha y_i (1-\hat{y}_i)^\gamma \log(\hat{y}_i) + (1-\alpha)(1-y_i) \hat{y}_i^\gamma \log(1-\hat{y}_i) \right]
$$

其中 $y_i$ 是真实标签（变换是否有效），$\hat{y}_i$ 是符号树 $\tau$ 对第 $i$ 个节点的预测概率，$\alpha$ 是类别平衡因子，$\gamma$ 是聚焦参数（focal parameter）。该奖励函数通过降低易分类样本的权重，促使模型关注难以预测的节点。

**优势函数** 通过组归一化计算，以降低训练方差：

$$
A_{\boldsymbol{\theta}}(\boldsymbol{\tau}) = \frac{r(\boldsymbol{\tau}) - \bar{r}}{\sigma_r}
$$

其中 $\bar{r}$ 和 $\sigma_r$ 分别是同一批次（group）内所有符号树奖励的均值和标准差。

**PPO 目标函数** 使用带裁剪的代理目标来稳定策略更新：

$$
J(\theta) = \mathbb{E}_{\tau \sim p(\tau \mid \theta)} \left[ \min \left( \frac{p_\theta(\tau)}{p_{\theta_{\mathrm{old}}}(\tau)} A_{\theta_{\mathrm{old}}}(\tau), \ \mathrm{clip} \left( \frac{p_\theta(\tau)}{p_{\theta_{\mathrm{old}}}(\tau)}, 1-\epsilon, 1+\epsilon \right) A_{\theta_{\mathrm{old}}}(\tau) \right) \right]
$$

其中 $p_\theta(\tau)$ 是当前策略生成序列 $\tau$ 的概率，$p_{\theta_{\mathrm{old}}}(\tau)$ 是旧策略的概率，$\epsilon$ 是裁剪阈值。该目标函数通过限制策略更新的步长，防止因单次更新过大而导致训练崩溃。

### 3.4 Best-of-N (BON) 集成

为了进一步提升推理稳定性，论文采用 Best-of-N 策略：在训练完成后，从生成的符号树中选出训练奖励最高的 $N$ 个表达式（实验中 $N = 4$），构建集成模型。在推理时，这 $N$ 个符号树分别对每个节点进行预测，最终评分取它们的平均值。

## 实验与分析

### 主结果：在线启发式效率与优化性能

HIS框架的核心验证是将学习的层次化符号评分函数集成到Mfs2启发式算法中（记为HIS-Mfs2），在六个挑战性电路（EPFL: Hyp, Square, Multiplier, DesPerf, Ethernet, Conmax；IWLS: 具体电路名见原文Table 2）上与默认无剪枝的Mfs2（Default Mfs2）对比。关键结论如下：

*   **运行时间与电路尺寸**：在超参数k（应用变换的节点百分比）设为30%、40%、50%时，HIS-Mfs2在六个电路上平均实现**27.22%的运行时间减少**和**6.95%的电路尺寸（节点数）减少**（Table 2）。例如，当k=40%时，平均尺寸和深度改善达7.43%，同时运行时间降低40.27%，而优化性能仅边际下降0.38%。
*   **与基于GNN和轻量级基线的对比**：在EPFL基准的六个电路上，HIS-Mfs2在**And Reduction (AR)**指标（即减少的节点数）上全面优于或持平于所有基线：COG-Mfs2、CMO-Mfs2、Random-Mfs2和Effisyn-Mfs2（Table 7）。例如，在Hyp电路上HIS的AR为566（COG为435，Random为563），在DesPerf上为936（COG为732，CMO为900）。同时，HIS-Mfs2在所有电路上**运行时间最短**，平均比COG-Mfs2快22.91%，比CMO-Mfs2快11.96%，比Random-Mfs2快19.24%，比Effisyn-Mfs2快21.82%。
*   **推理速度**：在纯CPU环境下，HIS的符号函数推理极快。在EPFL电路上平均推理速度比COG快**296倍**，在IWLS电路上快**254倍**（Table 5）。这直接解决了GNN模型在工业CPU部署中的效率瓶颈。


![[assets/figures/papers/iclr26_0002_YaXSEbRrHP_A_Hierarchical_Circuit_Symbolic_Discovery_Framew/figures/005_Table_2.jpg]]
*Table 2: We compare the Default Mfs2 heuristic with our HIS-Mfs2 heuristic with the hyperparameter k set as 30%, 40% and 50% on six challenging circuits. Optimized Nd denotes the node number (size) of circuits, and Lev denotes the level (depth) of circuits. We define an Improvement metric by M(Default)−M(Ours)M(Default) , where M (·) denotes the Optimized Nd, Lev, or Time. M(Default)*

![[assets/figures/papers/iclr26_0002_YaXSEbRrHP_A_Hierarchical_Circuit_Symbolic_Discovery_Framew/figures/010_Table_5.jpg]]
*Table 5: The model inference results show that our HIS is extremely efficient for inference compared to the SOTA graph-based approach (COG) when executed on CPU-based LO tools*

### 预测召回率与剪枝有效性

HIS评分函数的离线预测质量通过top-50%召回率衡量（Table 1）。在六个电路上，HIS的召回率（0.82, 0.94, 0.94, 0.83, 0.99, 0.75）**一致优于**所有基于图的基线（COG, CMO）和基于节点的基线（Effisyn, Random）。这表明层次化符号树能更准确地识别出有效的节点级变换，从而在剪枝时保留高价值操作。


![[assets/figures/papers/iclr26_0002_YaXSEbRrHP_A_Hierarchical_Circuit_Symbolic_Discovery_Framew/figures/003_Table_1.jpg]]
*Table 1: The results show that HIS consistently outperforms all graph-based and node-based baselines in terms of generalization top 50% prediction recall*

### 消融实验

Table 3的消融实验验证了HIS各核心组件的必要性：


![[assets/figures/papers/iclr26_0002_YaXSEbRrHP_A_Hierarchical_Circuit_Symbolic_Discovery_Framew/figures/006_Table_3.jpg]]
*Table 3: The ablation results demonstrate that each component contributes significantly to the overall performance of HIS. Removing any individual module leads to noticeable performance degradation, indicating that the effectiveness relies on the complementary design*

*   **移除层次化结构**（退化为单层符号函数）：性能显著下降，证明多层消息聚合对捕获电路多级结构信息至关重要。
*   **移除结构感知Transformer**（替换为标准Transformer）：性能下降，说明融入父节点和兄弟节点信息的序列生成策略优于无结构感知的生成。
*   **移除PPO强化学习**（改用监督学习）：性能下降，表明基于组奖励（focal loss）的RL优化比直接模仿学习更能探索出高性能的符号函数。

### 失败模式与局限性

*   **启发式泛化性**：当前方法仅针对Mfs2启发式验证，尚未在Resub、Rewrite等其他LO启发式上测试。符号函数是否对不同的节点变换类型具有鲁棒性仍需验证。
*   **层次深度固定**：层数L固定为2（与2层GNN配置一致），更深的层次可能带来更好的性能但会增加符号复杂度，最优L值未探索。
*   **符号库手工设计**：算子集合（+,-,×,÷,log,exp）和聚合算子（min,max,mean,sum）是手工选择的，可能存在更优组合。自动搜索符号库是开放问题。
*   **训练敏感性**：PPO训练对超参数（组大小、裁剪阈值ε）敏感，调参成本较高。不同电路可能需要不同的RL配置才能达到最佳性能。

### 重要图表结论

*   **Figure 3**：在线运行时间对比图显示，HIS-Mfs2在所有六个电路上的运行时间均显著低于COG-Mfs2、CMO-Mfs2、Random-Mfs2和Effisyn-Mfs2，且优势在较大电路（如Hyp）上更为明显。
*   **Figure 5**：可视化展示了EPFL和IWLS基准上发现的层次化符号函数。所有发现的表达式都同时聚合了根节点和候选节点的信息，表明HIS自动学到了结合局部和全局特征的评分策略。
*   **Table 8**：随机模型实验表明，召回率与k值呈近线性正相关，但优化性能（And Reduction）并非单调，存在最优k值区间（通常为40%-50%）。

### 补充图表

![[assets/figures/papers/iclr26_0002_YaXSEbRrHP_A_Hierarchical_Circuit_Symbolic_Discovery_Framew/figures/009_Table_4.jpg]]
*Table 4: We provide comprehensive implementation details, including the arguments for training, the Transformer model, and RL algorithms, along with a subset of the tokens library*


## 方法谱系与知识库定位

### 与基线方法的关系

HIS 的核心定位是替代逻辑优化（LO）启发式中的评分函数，其直接对标的是基于 GNN 的评分函数（COG、CMO）和轻量级符号评分函数（Effisyn）。与这些基线相比，HIS 在表示范式上发生了根本性变化：基线方法要么依赖复杂的 GNN 推理（COG、CMO），要么使用手工设计的浅层数学表达式（Effisyn），而 HIS 提出了层次化符号树表示，每层执行可解释且高效的符号消息聚合。这一变化带来了三个关键优势：

1. **推理效率的质变**：HIS 在 EPFL 和 IWLS 基准上的平均推理速度比 COG 快 296 倍和 254 倍（Table 5），同时保持了与 Effisyn 等轻量级方法相当的推理时间。这一效率提升使得 HIS 能够部署在纯 CPU 的工业 EDA 工具中，而 GNN 基线则因推理成本过高难以落地。

2. **优化性能的持续领先**：在六个挑战性电路上，HIS 的 top-50% 预测召回率一致优于所有基于图和基于节点的基线方法（Table 1）。当集成到 Mfs2 启发式中时，HIS-Mfs2 相比默认 Mfs2 实现了平均 27.22% 的运行时间提升和 6.95% 的电路尺寸减少（Table 2）。与 COG-Mfs2 和 CMO-Mfs2 相比，HIS 分别实现了 22.91% 和 11.96% 的平均运行时间改进（Table 7）。

3. **可解释性的天然优势**：所有发现的层次化符号函数都从根节点和候选节点聚合信息（Table 6），使得优化决策过程可被人类理解，这是黑盒 GNN 方法难以提供的特性。

### 适用边界

HIS 的适用性受限于以下边界条件：

- **启发式类型**：当前方法仅针对 Mfs2 启发式进行了验证，尚未在 Resub、Rewrite 等其他 LO 启发式上测试。HIS 框架的核心假设——电路子图的结构信息可通过层次化符号聚合有效捕获——是否适用于不同语义的启发式，仍需验证。
- **电路规模与结构**：实验在 EPFL 和 IWLS 基准上进行，这些电路规模适中（节点数从数千到数十万）。对于超大规模电路（如百万节点级），计算树的构建和符号函数的推理效率可能成为新的瓶颈。
- **层次深度固定**：层数 L 固定为 2，与 2 层 GNN 配置一致。更深的层次可能捕获更远距离的结构信息，但也会增加符号树的复杂度和搜索空间。最优 L 值的存在性及其与电路特性的关系尚不清楚。
- **符号库的手工定义**：算子集合（+,-,×,÷,log,exp）和聚合算子（min,max,mean,sum）是手工选择的，可能存在更优的算子组合。符号库的完备性直接影响表达能力和搜索效率。

### 局限与开放问题

1. **跨启发式的泛化能力**：HIS 框架能否推广到其他 LO 启发式（如 Resub、Rewrite）以及更广泛的 EDA 任务（如技术映射、布局布线）？这需要验证层次化符号树表示是否具有任务无关的结构捕获能力。

2. **符号库的自动搜索**：如何自动发现最优的符号库算子集合，而非依赖手工定义？这涉及到算子空间的组合优化问题，可能通过元学习或进化搜索来解决。

3. **层次深度的自适应选择**：L=2 是经验性选择，是否存在与电路拓扑特性相关的自适应 L 选择策略？更深的层次可能带来性能提升，但也会增加训练难度和过拟合风险。

4. **跨电路的可迁移性**：HIS 学习的符号函数是否具有跨电路、跨工艺的可迁移性？当前实验在同一基准的不同电路上评估，但未测试跨基准或跨工艺节点的泛化能力。如果符号函数过度拟合特定电路结构，其实际工业价值将受限。

5. **训练稳定性与调参成本**：PPO 强化学习对超参数（组大小、裁剪阈值 ε）敏感，调参成本较高。消融实验（Table 3）显示移除任何模块都会导致性能显著下降，表明各组件的互补设计是性能的关键，但也意味着系统复杂度较高。是否存在更鲁棒的训练策略或更简洁的架构设计？

6. **与 GNN 的潜在融合**：HIS 受 GNN 消息传递机制启发但完全替代了 GNN。能否将 HIS 的符号表示与更复杂的 GNN 架构（如注意力机制）结合，以在可解释性和表达力之间取得更好的平衡？这是一个值得探索的混合方向。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Hierarchical_Circuit_Symbolic_Discovery_Framework_for_Efficient_Logic_Optimization.pdf

![[paperPDFs/ICLR_2026/A_Hierarchical_Circuit_Symbolic_Discovery_Framework_for_Efficient_Logic_Optimization.pdf]]
