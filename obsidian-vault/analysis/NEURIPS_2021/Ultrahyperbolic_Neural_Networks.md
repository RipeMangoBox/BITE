---
title: "Ultrahyperbolic Neural Networks"
type: paper
paper_level: A
venue: NeurIPS
year: 2021
pdf_ref: paperPDFs/NEURIPS_2021/Ultrahyperbolic_Neural_Networks.pdf
code_link: null
project_link: "https://openreview.net/forum?id=sf2BxJNXC3K"
aliases:
- UNN
tags:
- NEURIPS_2021
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入商流形(quotient manifold) P_r^{p,q} = S_r^{p,q} / {±1}，将每个点与其对跖点等价视之，保证任意两点间至少有一条测地线，使得黎曼优化成为可能。"
primary_logic: "通过对跖点商空间消除测地线断裂，将伪黎曼几何的灵活表示能力与可导性协调，从而能够构建在超双曲空间中端到端学习的深度神经网络。"
claims:
- "原始伪球面 S_r^{p,q} 上存在不可由测地线连接的点对，阻碍参数学习。"
- "商流形 P_r^{p,q} 的动机是保证任意两点间至少有一条测地线，从而可以优化参数模型。"
- "提出的优化框架通过水平提升算子和平行传输使得梯度下降可行。"
- "超双曲图卷积网络在带环的层次图分类（D&D、Enzymes）上显著优于欧氏和双曲基线。"
---

# Ultrahyperbolic Neural Networks

> [!tip] 核心洞察
> 通过对跖点商空间消除测地线断裂，将伪黎曼几何的灵活表示能力与可导性协调，从而能够构建在超双曲空间中端到端学习的深度神经网络。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 超双曲神经网络 |
| 英文题名 | Ultrahyperbolic Neural Networks |
| 会议/期刊 | NeurIPS 2021 |
| Links | [paper](https://openreview.net/attachment?id=sf2BxJNXC3K&name=supplementary_material) · [Project](https://openreview.net/forum?id=sf2BxJNXC3K) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Ultrahyperbolic Neural Networks |
| Dataset | Citeseer (node classification, d=4), Cora (node classification, Pubmed (node classification, Collab (graph classification, d=64) |

> [!tip] 效果简介
> - Citeseer (node classification, d=4) 上，Test accuracy (%) 为 51.8±2.6 (P_1^{1,3})，对比 44.5±5.9 (Euclidean R^4)，变化 +7.3。
> - Cora (node classification, d=4) 上，Test accuracy (%) 为 64.7±5.3 (P_1^{3,1})，对比 53.5±4.3 (Euclidean R^4)，变化 +11.2。
> - Pubmed (node classification, d=4) 上，Test accuracy (%) 为 73.1±0.6 (P_1^{1,3})，对比 66.9±2.3 (Euclidean R^4)，变化 +6.2。

## 概要

**问题瓶颈**：在原始的伪球面（pseudo-sphere）$S_r^{p,q}$ 上，存在无法由完整测地线连接的点对，导致梯度不能平行传输，从而无法有效地优化参数化模型（如神经网络）。这一几何缺陷直接阻碍了将双曲神经网络的成功经验推广到更一般的超双曲空间。

**核心洞察**：引入商流形 $\mathcal{P}_r^{p,q} = S_r^{p,q} / \{\pm 1\}$，将每个点与其对跖点等价视之，从而保证任意两点间至少有一条测地线。这一对跖点商空间消除了测地线断裂，将伪黎曼几何的灵活表示能力与可导性协调，使超双曲空间中端到端学习的深度神经网络成为可能。

**方法定位**：本文提出的**超双曲神经网络**（Ultrahyperbolic Neural Networks）属于参数化流形学习与图表示学习的交叉。与仅能处理负曲率的双曲 GCN（如 Liu et al., NeurIPS 2019 的洛伦兹模型）和零曲率的欧几里得 GCN（Kipf & Welling, ICLR 2017）不同，该方法在签名 $(p, q)$ 可配置的商流形上统一了正曲率（椭圆）、负曲率（双曲）和混合曲率几何。关键技术模块包括：水平提升算子将商流形切向量与伪球面切向量建立双射对应；伪黎曼梯度通过度量矩阵 $\mathbf{G}$ 转换并正交投影到切空间；沿测地线的平行传输保证了反向传播的正确性；以及基于立体投影的激活函数实现非线性变换。

**主要结果**：在引文网络节点分类任务上，4 维超双曲表示显著优于欧几里得基线——Cora 提升 +11.2%（64.7±5.3 vs 53.5±4.3），Citeseer 提升 +7.3%（51.8±2.6 vs 44.5±5.9），Pubmed 提升 +6.2%（73.1±0.6 vs 66.9±2.3）。在带环的层次图分类任务上优势更为突出：蛋白质数据集 D&D 达到 81.97±3.41（欧氏基线 76.93±7.21），Enzymes 达到 50.50±6.71（欧氏基线 43.83±10.3）。不同签名 $(p,q)$ 的消融实验表明，混合签名（如 $\mathcal{P}_1^{1,3}$、$\mathcal{P}_1^{3,1}$）通常优于纯双曲或纯椭圆退化情形。训练时间较欧几里得方法慢约 25%，在高维（$d=600$）过参数化时各流形性能趋同。



### 1. 图表示学习的几何化趋势

图结构数据的表示学习是机器学习中的核心问题。传统方法在欧几里德空间 $\mathbb{R}^d$ 中优化节点或图的嵌入，但其平坦的几何特性难以高效编码现实世界中普遍存在的层次结构、幂律分布和复杂拓扑模式。近年来，将表示学习从平坦空间推广到非欧几何流形已成为一条富有成效的研究路径。

双曲几何（常负曲率）因其体积随半径指数增长的特性，被证明能自然适配树状或层次化数据的表示。一系列工作——包括双曲浅嵌入、双曲神经网络以及双曲图卷积网络——在无标度网络、引文图和知识图谱等任务上取得了优于欧几里德基线的表现。椭圆几何（正常曲率）则适用于球面或循环结构的数据。然而，真实世界的图数据往往同时包含树状层次、循环和混合拓扑模式，单一曲率的几何空间无法全面刻画这种结构异质性。

### 2. 伪黎曼几何的潜力与根本障碍

伪黎曼几何通过引入非正定的度量张量，允许在同一流形内同时容纳正曲率和负曲率子空间，从而具备表示混合拓扑模式的灵活性。具体而言，具有签名 $(p+1, q)$ 的伪球面 $S_r^{p,q}$ 是嵌入在伪欧几里德环境空间 $\mathbb{R}^{p+1,q}$ 中的常曲率超曲面，其上的测地线可分为类时、类空和类光三种类型，分别对应不同的几何行为。

然而，直接在原始伪球面 $S_r^{p,q}$ 上构建可学习的参数化模型（如神经网络）面临一个根本性障碍：**并非所有点对都能由完整测地线连接**。这意味着，当模型需要计算两点之间的测地线距离或沿测地线进行平行传输时，部分点对之间不存在可行的路径，从而导致梯度无法有效回传，优化过程断裂。正如原文所指出的：“直接将双曲神经网络扩展到超双曲空间是有问题的”。这一测地线断裂问题构成了伪黎曼表示学习从理论走向应用的核心瓶颈。

### 3. 本文动机：通过对跖商消除测地线断裂

本文的核心动机在于解决上述测地线不可达问题，从而解锁伪黎曼几何在深度表示学习中的潜力。关键洞察是：如果我们将伪球面上的每个点 $\mathbf{x}$ 与其对跖点 $-\mathbf{x}$ 视为等价，构造商流形 $P_r^{p,q} = S_r^{p,q} / \{\pm 1\}$，则任意两点之间至少存在一条完整的测地线。

这一对跖商操作的几何直觉如 Figure 1 所示：在 $P_1^{1,1}$ 上，点 $[\mathbf{x}]$ 实际上是点对 $\{\mathbf{x}, -\mathbf{x}\}$。原始伪球面上无法由测地线连接的 $\mathbf{x}$ 与 $-\mathbf{z}$，在商流形中可以通过 $\mathbf{x}$ 与 $\mathbf{z}$ 之间的测地线（红色路径）实现连接。更一般地，商流形上两点 $[\mathbf{x}]$ 与 $[\mathbf{y}]$ 之间的最小测地线长度，等于原始伪球面上 $\mathbf{x}$ 与 $-\mathbf{y}$ 之间最小测地线的长度（蓝色路径）。

这一构造使得在商流形上定义完整的黎曼优化框架成为可能：前向传播将数据映射到商流形上的表示，反向传播通过水平提升算子和平行传输在切空间中计算并回传梯度。由此，本文首次实现了在超双曲空间中端到端学习的深度神经网络，为同时编码层次、循环和混合拓扑模式的图表示学习开辟了新路径。



## 核心方法与创新机理

本文的核心创新在于**通过对跖点商空间构造，首次将伪黎曼几何引入可端到端学习的深度神经网络**。此前的超双曲表示工作（如 Law & Stam, 2020）仅能进行非参数化的嵌入，无法在伪球面 $S_r^{p,q}$ 上优化参数化模型。其根本瓶颈在于：在原始伪球面上，存在无法由完整测地线连接的点对，导致黎曼梯度下降所需的平行传输与梯度流断裂。

本文的关键突破可归纳为以下四个 **changed slots**：

### 1. 表示流形：从伪球面到商伪球面

- **Baseline 值**：直接在伪球面 $S_r^{p,q}$ 上进行表示（如 Law & Stam, 2020 的非参数嵌入）。
- **提出值**：定义商流形 $\mathcal{P}_r^{p,q} = S_r^{p,q} / \{\pm 1\}$，将每个点 $\mathbf{x}$ 与其对跖点 $-\mathbf{x}$ 视作等价类 $[\mathbf{x}]$。
- **证据锚点**：Section 2 明确指出，“动机在于 $\mathcal{P}_r^{p,q}$ 上任意两点间至少存在一条测地线，这使得我们可以优化参数化模型”（confidence 0.95）。

这一构造的几何直觉在 **Figure 1** 中得到直观展示：在商流形 $\mathcal{P}_1^{1,1}$ 上，$[\mathbf{x}]$ 与 $[\mathbf{z}]$ 之间可通过红色测地线连接，而原始伪球面上 $\mathbf{x}$ 与 $-\mathbf{z}$ 之间则无完整测地线。

### 2. 测地线连通性：从部分可达到全局可达

- **Baseline 值**：伪球面 $S_r^{p,q}$ 上并非所有点对都能由测地线连接。
- **提出值**：商流形 $\mathcal{P}_r^{p,q}$ 上任意两点间至少存在一条测地线。
- **因果机制**：通过对跖点等价，原本在 $S_r^{p,q}$ 上断裂的测地线在商空间中被“缝合”——$[\mathbf{x}]$ 到 $[\mathbf{y}]$ 的测地线长度等于 $S_r^{p,q}$ 上 $\mathbf{x}$ 到 $-\mathbf{y}$（或 $\mathbf{x}$ 到 $\mathbf{y}$）的最短测地线长度（见式 (7) 的分段距离定义）。
- **证据锚点**：Section 2 明确陈述了这一动机（confidence 0.95）。

### 3. 梯度下降方向：从非下降方向到保证下降

- **Baseline 值**：在非正定度量下，直接使用负梯度 $-\boldsymbol{\lambda}$ 不能保证是下降方向。
- **提出值**：通过度量矩阵 $\mathbf{G}$ 转换，使用 $-\mathbf{G}\boldsymbol{\lambda}$ 作为搜索方向，保证函数值单调下降。
- **因果机制**：伪黎曼梯度定义为 $D\bar{f}(\mathbf{x}) = \Pi_{\mathbf{x}}(\mathbf{G}\nabla\bar{f}(\mathbf{x}))$，其中 $\Pi_{\mathbf{x}}$ 是到 $S_r^{p,q}$ 切空间的正交投影。由于度量 $\mathbf{G}$ 具有不定号签名，欧氏梯度 $\nabla\bar{f}$ 的方向信息被 $\mathbf{G}$ 扭曲，必须通过 $\mathbf{G}$ 修正才能获得真正的下降方向。
- **证据锚点**：Section 3.4 和 Section 5.1 明确说明“若使用 $-\boldsymbol{\lambda}_{[x_i],p}$ 作为搜索方向则算法不收敛，因为它不是下降方向”（confidence 0.95）。**Figure 2 (left)** 的收敛曲线验证了该优化框架的可行性。

### 4. 模型类型：从非参数嵌入到参数化神经网络

- **Baseline 值**：Law & Stam (2020) 仅能学习非参数化的超双曲嵌入。
- **提出值**：构建参数化的超双曲神经网络，包含完整的前向传播与反向传播。
- **核心流水线模块**：
  - **前向映射**：神经网络 $\phi_\theta$ 将输入映射到参考点 $\mathbf{p}$ 的水平空间 $\mathcal{H}_{\mathbf{p}}$，经指数映射 $\overline{\exp}_{\mathbf{p}}$ 投影到 $S_r^{p,q}$，再自然投影到商流形 $\mathcal{P}_r^{p,q}$（Section 3.4）。
  - **反向传播**：计算伪黎曼梯度 $D\bar{f}$，沿测地线平行传输到参考点 $\mathbf{p}$，通过水平提升算子 $\operatorname{lift}_{\mathbf{p}}$ 拉回水平空间，构建下降方向 $-\mathbf{G}\boldsymbol{\lambda}$ 更新参数（Section 3.4, Eq. (9)）。
  - **图卷积层**：在商流形上实现消息传递——邻居表示通过对数映射拉回切空间，加权求和后经指数映射返回流形，再经立体投影-ReLU-逆投影的激活函数（Section 4）。
- **证据锚点**：Section 3.4 和 Section 4 详细描述了该框架（confidence 0.9）。

### 创新总结

本工作的核心洞察在于：**通过对跖点商空间消除测地线断裂，将伪黎曼几何的灵活表示能力（可同时编码类空、类时和类光关系）与可导性协调**，从而首次实现了在超双曲空间中端到端学习的深度神经网络。这一创新在层次图分类任务上得到了验证——例如在 D&D 数据集上，超双曲 GCN 达到 81.97% 准确率，显著优于欧氏 GCN 的 76.93%（Table 5, confidence 0.95）。



超双曲神经网络（Ultrahyperbolic Neural Networks）的整体框架围绕一个核心几何构造展开：将对跖点等价的**商流形** `$\mathcal{P}_r^{p,q} = \mathcal{S}_r^{p,q} / \{\pm 1\}$` 作为表示空间，以解决原始伪球面 `$\mathcal{S}_r^{p,q}$` 上测地线断裂导致梯度无法平行传输的根本瓶颈。该框架将伪黎曼几何的灵活表示能力与端到端可导性协调，形成四个紧密耦合的模块。

### 1. 输入到水平空间的映射

框架的入口是一个参数化神经网络 `$\phi_\theta$`，它将原始输入数据（如图节点特征）映射到参考点 `$\mathbf{p}$` 的**水平空间** `$\mathcal{H}_{\mathbf{p}}$`。该水平空间是伪球面切空间 `$T_{\mathbf{p}}\mathcal{S}_r^{p,q}$` 中满足特定正交条件的子空间。随后，通过指数映射 `$\exp_{\mathbf{p}}$` 将水平向量映射到伪球面 `$\mathcal{S}_r^{p,q}$` 上，再经自然投影 `$\pi$` 到达商流形 `$\mathcal{P}_r^{p,q}$`，完成从欧氏输入到超双曲表示的转换。

### 2. 反向传播与梯度下降

在商流形上定义损失函数后，反向传播的关键挑战在于非正定度量下如何构造有效的下降方向。框架采用三步机制：

- **伪黎曼梯度计算**：将欧氏梯度 `$\nabla \bar{f}(\mathbf{x})$` 通过度量矩阵 `$\mathbf{G}$` 转换，并正交投影到 `$\mathcal{S}_r^{p,q}$` 的切空间，得到伪黎曼梯度 `$D\bar{f}(\mathbf{x}) = \Pi_{\mathbf{x}}(\mathbf{G}\nabla\bar{f}(\mathbf{x}))$`。
- **平行传输**：将梯度沿测地线平行传输到参考点 `$\mathbf{p}$`，利用伪球面上的平行传输公式保持 `$q$`-内积的线性等距性。
- **水平提升与下降方向**：用水平提升算子 `$\operatorname{lift}_{\mathbf{p}}$` 将传输后的梯度拉回水平空间，构建下降方向 `$-\mathbf{G}\lambda$`。实验验证表明，直接使用 `$-\lambda$` 在非正定度量下并非下降方向，会导致算法不收敛，而 `$-\mathbf{G}\lambda$` 保证了收敛性。

### 3. 超双曲图卷积层

在商流形上实现图卷积的核心操作如下：对于每个节点 `$u$`，将其邻居节点 `$v$` 的表示 `$\mathbf{h}_v^k$` 通过对数映射 `$\log_{[\mathbf{p}]}$` 拉回参考点切空间，经线性变换 `$\mathbf{W}^k$` 加权求和后，通过指数映射 `$\overline{\exp}_{\mathbf{p}}$` 回到商流形。激活函数采用立体投影-ReLU-逆投影的三段式设计：先将流形上的点通过立体投影 `$\omega_\varepsilon$` 映射到切空间，在切空间上施加 ReLU 非线性，再通过逆投影 `$\omega_\varepsilon^{-1}$` 回到流形。

### 4. 输出与损失计算

最终节点或图表示位于商流形 `$\mathcal{P}_r^{p,q}$` 上，损失函数基于商流形的测地线距离 `$\mathbf{d}_\gamma([\mathbf{x}],[\mathbf{y}])$` 计算。该距离根据归一化 `$q$`-内积的绝对值分段定义：当 `$|\langle\mathbf{x},\mathbf{y}\rangle_q / r^2| \ge 1$` 时使用反双曲余弦 `$r\cosh^{-1}$`，否则使用反余弦 `$r\cos^{-1}$`。对于图分类等任务，损失函数（如边缘预测的负对数似然）直接作用在这些超双曲表示上，实现端到端学习。

### 模块间的数据流

整个 pipeline 的数据流是单向且可微的：输入数据 → 神经网络 `$\phi_\theta$` → 水平空间 `$\mathcal{H}_{\mathbf{p}}$` → 指数映射 → 伪球面 `$\mathcal{S}_r^{p,q}$` → 自然投影 → 商流形 `$\mathcal{P}_r^{p,q}$` → 图卷积层（对数映射 → 线性变换 → 指数映射 → 立体投影激活） → 测地线距离损失。反向传播时，梯度沿此路径反向流动，通过水平提升算子和平行传输保证梯度信息的正确传递。

该框架的**核心洞察**在于：通过对跖点商空间消除测地线断裂，使得任意两点间至少存在一条测地线，从而将伪黎曼几何的表示能力与基于梯度的优化统一起来。训练时间比欧几里得方法慢约 25%，主要开销来自伪黎曼梯度中的正交投影和平行传输计算。



### 3.1 商流形的构造与测地线完备性

超双曲神经网络的核心操作空间是**商伪球面**（quotient pseudo-sphere）$\mathcal{P}_r^{p,q}$，其定义为：

$$\mathcal{P}_r^{p,q} := S_r^{p,q} / \{\pm 1\}$$

其中 $S_r^{p,q} := \{\mathbf{x} \in \mathbb{R}^{p+1,q} : \langle\mathbf{x},\mathbf{x}\rangle_q = r^2\}$ 是半径为 $r$ 的伪球面，嵌入在具有签名 $(p+1, q)$ 的伪欧几里得环境空间 $\mathbb{R}^{p+1,q}$ 中。环境空间配备如下内积（式 (1)）：

$$\langle\mathbf{x},\mathbf{y}\rangle_q := \sum_{i=0}^{p} x_i y_i - \sum_{j=p+1}^{d} x_j y_j = \mathbf{x}^\top \mathbf{G} \mathbf{y}$$

其中 $\mathbf{G} = \operatorname{diag}(1, \ldots, 1, -1, \ldots, -1)$ 是对角度量矩阵，前 $p+1$ 个对角元为 $+1$，后 $q$ 个为 $-1$，总维度 $d = p + q$。

**瓶颈与突破**：在原始伪球面 $S_r^{p,q}$ 上，并非任意两点都能由完整测地线连接——这一断裂性使得基于梯度平行传输的参数优化无法进行。通过对跖点等价（$\mathbf{x} \sim -\mathbf{x}$）构造商流形后，**任意两点间至少存在一条测地线**，从而为黎曼优化铺平道路。

### 3.2 切空间与水平提升算子

商流形 $\mathcal{P}_r^{p,q}$ 在点 $[\mathbf{x}]$ 处的切空间 $T_{[\mathbf{x}]}\mathcal{P}_r^{p,q}$ 通过**水平提升算子**（horizontal lift operator）与伪球面 $S_r^{p,q}$ 的切空间建立双射对应。

伪球面在 $\mathbf{x}$ 处的切空间为：

$$T_{\mathbf{x}} S_r^{p,q} := \{\boldsymbol{\xi} \in \mathbb{R}^{p+1,q} : \langle\boldsymbol{\xi}, \mathbf{x}\rangle_q = 0\}$$

由于商映射 $\pi: S_r^{p,q} \to \mathcal{P}_r^{p,q}$ 的纤维 $[\mathbf{x}] = \{\mathbf{x}, -\mathbf{x}\}$ 是离散的（0 维），垂直空间 $V_{\mathbf{x}} := \ker(d\pi_{\mathbf{x}}) = \{0\}$，因此 $d\pi_{\mathbf{x}}$ 在切空间上是单射。水平空间 $\mathcal{H}_{\mathbf{x}}$ 取为整个 $T_{\mathbf{x}} S_r^{p,q}$，水平提升算子 $\operatorname{lift}_{\mathbf{x}}: T_{[\mathbf{x}]}\mathcal{P}_r^{p,q} \to \mathcal{H}_{\mathbf{x}}$ 是双射。这意味着商流形上的切向量可等价地用伪球面上的水平向量表示。

### 3.3 测地线距离

商流形上两点 $[\mathbf{x}], [\mathbf{y}]$ 的测地线距离由归一化 q-内积的绝对值决定，分段定义（式 (7)）：

$$\mathbf{d}_\gamma([\mathbf{x}], [\mathbf{y}]) = \begin{cases}
r\cosh^{-1}\left(\left|\frac{\langle\mathbf{x},\mathbf{y}\rangle_q}{r^2}\right|\right) & \text{if } \left|\frac{\langle\mathbf{x},\mathbf{y}\rangle_q}{r^2}\right| \ge 1 \\
r\cos^{-1}\left(\left|\frac{\langle\mathbf{x},\mathbf{y}\rangle_q}{r^2}\right|\right) & \text{otherwise}
\end{cases}$$

- **类时/类光情形**（$|\langle\mathbf{x},\mathbf{y}\rangle_q|/r^2 \ge 1$）：使用反双曲余弦 $\cosh^{-1}$，对应类时或类光分离的点对。
- **类空情形**（$|\langle\mathbf{x},\mathbf{y}\rangle_q|/r^2 < 1$）：使用反余弦 $\cos^{-1}$，对应类空分离的点对。

该距离的几何意义在于：商流形上的最短测地线长度等于伪球面上 $\mathbf{x}$ 与 $\pm\mathbf{y}$ 之间两条候选测地线中较短的那条。

### 3.4 平行传输

在伪球面 $S_r^{p,q}$ 上，沿测地线 $\overline{\gamma}$ 从 $\mathbf{x}$ 到 $\mathbf{y}$ 的平行传输保持 q-内积不变，其显式公式（式 (6)）为：

$$P_{\mathbf{x}\sim\mathbf{y}}^{\overline{\gamma}}(\overline{\boldsymbol{\xi}}_{\mathbf{x}}) := \overline{\boldsymbol{\xi}}_{\mathbf{x}} - \frac{\langle\mathbf{y}, \overline{\boldsymbol{\xi}}_{\mathbf{x}}\rangle_q}{\langle\mathbf{x},\mathbf{y}\rangle_q + r^2}(\mathbf{y} + \mathbf{x})$$

其中 $\overline{\boldsymbol{\xi}}_{\mathbf{x}} \in T_{\mathbf{x}} S_r^{p,q}$ 是伪球面上的切向量。

商流形上的平行传输则通过水平提升和投影实现：先将商流形切向量 $\boldsymbol{\xi} \in T_{[\mathbf{x}]}\mathcal{P}_r^{p,q}$ 提升到伪球面，执行上述平行传输，再根据 $\langle\mathbf{x},\mathbf{y}\rangle_q$ 的符号选择目标点的提升方向（$\mathbf{y}$ 或 $-\mathbf{y}$），最后通过 $d\pi$ 投影回商流形切空间。

### 3.5 伪黎曼梯度与下降方向

定义在商流形上的函数 $f: \mathcal{P}_r^{p,q} \to \mathbb{R}$ 通过提升到伪球面进行优化。令 $\overline{f} = f \circ \pi$ 为 $S_r^{p,q}$ 上的提升函数，其在 $\mathbf{x}$ 处的**伪黎曼梯度**由欧氏梯度经度量矩阵转换并正交投影得到：

$$D\overline{f}(\mathbf{x}) = \Pi_{\mathbf{x}}(\mathbf{G} \nabla \overline{f}(\mathbf{x})), \quad \Pi_{\mathbf{x}}(\mathbf{z}) = \mathbf{z} - \frac{\langle\mathbf{z},\mathbf{x}\rangle_q}{\langle\mathbf{x},\mathbf{x}\rangle_q}\mathbf{x}$$

其中 $\Pi_{\mathbf{x}}$ 是将环境空间向量正交投影到 $T_{\mathbf{x}} S_r^{p,q}$ 的投影算子。

**关键洞察**：在非正定度量下，朴素的负梯度方向 $-\boldsymbol{\lambda}$ 未必是下降方向。本文证明使用 $-\mathbf{G}\boldsymbol{\lambda}$ 作为搜索方向可保证收敛性，其中 $\boldsymbol{\lambda}$ 是商流形切空间中的梯度表示，$\mathbf{G}$ 是度量矩阵。这一修正是超双曲空间中黎曼优化可行的**必要条件**（见 Section 3.4, Section 5.1 的收敛验证）。

### 3.6 超双曲图卷积层

超双曲图卷积网络（Ultrahyperbolic GCN）的单个图卷积层将邻居节点表示在商流形上进行聚合，核心公式为：

$$\mathbf{h}_u^{k+1} := \sigma\left(\left[\overline{\exp}_{\mathbf{p}}\left(\sum_{v \in \mathcal{T}(u)} \tilde{\mathbf{A}}_{uv} \mathbf{W}^k \operatorname{lift}_{\mathbf{p}}(\log_{[\mathbf{p}]}(\mathbf{h}_v^k))\right)\right]\right)$$

各组件含义：
- $\log_{[\mathbf{p}]}(\mathbf{h}_v^k)$：将第 $k$ 层节点 $v$ 的商流形表示 $\mathbf{h}_v^k$ 通过对数映射拉回到参考点 $[\mathbf{p}]$ 的切空间。
- $\operatorname{lift}_{\mathbf{p}}$：将切向量水平提升到伪球面 $S_r^{p,q}$ 在 $\mathbf{p}$ 处的切空间。
- $\mathbf{W}^k$：可学习的线性变换矩阵。
- $\tilde{\mathbf{A}}_{uv}$：归一化邻接矩阵元素，$\mathcal{T}(u)$ 为节点 $u$ 的邻居集合（含自环）。
- $\overline{\exp}_{\mathbf{p}}$：将切空间向量通过指数映射映射回伪球面，再自然投影到商流形。
- $\sigma$：激活函数，通过立体投影将点映射到切空间、施加 ReLU、再逆投影回商流形实现。

### 3.7 立体投影激活函数

为在商流形上实现非线性激活，引入从伪球面到切空间的立体投影及其逆映射：

**立体投影**（将伪球面上的点映射到 $\mathbb{R}^d$）：
$$\mathbf{a} = \omega_\varepsilon(\mathbf{x}) = \frac{1}{1 - \varepsilon x_0}(x_1, \dots, x_d)^\top$$

**逆立体投影**：
$$\omega_\varepsilon^{-1}(\mathbf{a}) = \frac{1}{1 + \langle\mathbf{a},\mathbf{a}\rangle_q}\begin{pmatrix} \varepsilon(\langle\mathbf{a},\mathbf{a}\rangle_q - 1) \\ 2\mathbf{a} \end{pmatrix}$$

其中 $\varepsilon \in \{-1, 1\}$ 控制投影极点的选择。激活函数 $\sigma$ 的完整流程为：$\mathbf{x} \mapsto \omega_\varepsilon(\mathbf{x}) \mapsto \operatorname{ReLU}(\cdot) \mapsto \omega_\varepsilon^{-1}(\cdot) \mapsto [\cdot]$，即先将商流形点投影到切空间（欧氏空间），施加逐元素 ReLU，再逆投影回商流形。

### 3.8 前向-反向传播框架

整个超双曲神经网络的优化流程可概括为三个核心模块：

1. **前向映射**：输入数据通过神经网络 $\phi_\theta$ 映射到参考点 $\mathbf{p}$ 的水平空间 $\mathcal{H}_{\mathbf{p}}$，经指数映射 $\exp_{\mathbf{p}}$ 到达伪球面 $S_r^{p,q}$，再自然投影到商流形 $\mathcal{P}_r^{p,q}$。

2. **反向传播**：计算伪黎曼梯度 $Df$，沿测地线平行传输到参考点 $\mathbf{p}$，用水平提升算子拉回水平空间，构建下降方向 $-\mathbf{G}\boldsymbol{\lambda}$ 更新参数 $\theta$。

3. **损失计算**：最终表示位于 $\mathcal{P}_r^{p,q}$ 上，使用商流形测地线距离 $\mathbf{d}_\gamma$（式 (7)）计算任务相关损失（如链接预测的负对数似然，式 (12)）。

> **训练开销**：由于需要计算伪黎曼梯度（含正交投影）和平行传输，超双曲模型的训练时间比欧几里得模型慢约 25%（Section 5.1, Table 1）。



## 实验与关键发现

### 核心实验设计

本文在两类任务上验证超双曲神经网络的有效性：**节点分类**（引文网络）与**图分类**（带环层次图）。实验的核心逻辑是：通过改变商流形 $\mathcal{P}_r^{p,q}$ 的签名 $(p,q)$，控制流形的曲率混合特性，观察其对层次结构表示能力的影响。所有实验均以 **欧几里得 GCN**（Kipf & Welling, ICLR 2017）为零曲率基线，以 **洛伦兹双曲 GCN**（Liu et al., NeurIPS 2019）和庞加莱球双曲 GCN 为负曲率基线，以纯椭圆商流形 $\mathcal{P}_1^{4,0}$ 为正曲率基线。

### 节点分类：引文网络上的签名效应

在 Citeseer、Cora、Pubmed 三个引文网络上，将表示维度固定为 $d=4$，对比不同签名 $(p,q)$ 的商流形性能（Table 3）。关键发现：

![[assets/figures/papers/paper_list_l16_https_openreview_net_attachment_id_sf2BxJNXC3K_name_supplementary_materi/figures/005_Table_3.jpg]]
*Table 3: Test node classification accuracy with 4-dimensional manifolds*

1. **混合签名显著优于纯几何**：超双曲签名 $\mathcal{P}_1^{1,3}$ 和 $\mathcal{P}_1^{3,1}$ 在所有数据集上均优于纯双曲 $\mathcal{P}_1^{0,4}$ 和纯椭圆 $\mathcal{P}_1^{4,0}$。例如在 Cora 上，$\mathcal{P}_1^{3,1}$ 达到 **64.7±5.3%**，而欧氏基线仅 53.5±4.3%，提升 **+11.2 个百分点**；纯双曲 $\mathcal{P}_1^{0,4}$ 仅 47.2±5.4%，甚至低于欧氏基线。

2. **签名方向与数据特性相关**：Citeseer 和 Pubmed 上 $\mathcal{P}_1^{1,3}$ 最优（51.8±2.6% 和 73.1±0.6%），Cora 上 $\mathcal{P}_1^{3,1}$ 最优。这表明不同数据集的层次结构可能需要不同的时间/空间维度配比，但论文未提供选择 $(p,q)$ 的系统方法。

3. **纯椭圆几何失效**：$\mathcal{P}_1^{4,0}$（正曲率椭圆几何）在所有数据集上性能最差（如 Pubmed 仅 59.6±3.3%），说明引文网络的层次结构更倾向于包含负曲率成分。

### 图分类：带环层次图的优势

在 D&D、Enzymes、Proteins、Collab、Reddit-multi-12K 五个带环图分类基准上（Table 4 为数据集统计），超双曲 GCN 在较高维度下展现出显著优势（Table 5）：

![[assets/figures/papers/paper_list_l16_https_openreview_net_attachment_id_sf2BxJNXC3K_name_supplementary_materi/figures/006_Table_4.jpg]]
*Table 4: Statistics of the graph datasets used for the classification task*

![[assets/figures/papers/paper_list_l16_https_openreview_net_attachment_id_sf2BxJNXC3K_name_supplementary_materi/figures/007_Table_5.jpg]]
*Table 5: Graph classification accuracy in percents. d is the dimensionality of the manifold*

| 数据集 | 维度 $d$ | 超双曲 GCN | 欧氏 GCN | 提升 |
|--------|----------|-----------|---------|------|
| D&D | 88 | **81.97±3.41** | 76.93±7.21 | +5.04 |
| Enzymes | 256 | **50.50±6.71** | 43.83±10.3 | +6.67 |
| Proteins | 100 | **76.56±2.09** | 75.46±3.88 | +1.10 |
| Collab | 64 | 82.26±1.23 | 81.88±1.76 | +0.38 |
| Reddit-multi-12K | 100 | **47.08±1.26** | 45.65±1.76 | +1.43 |

**瓶颈分析**：D&D 和 Enzymes 这两个数据集以包含环状结构的蛋白质图著称，超双曲 GCN 的提升最大（+5.04 和 +6.67 个百分点）。这表明混合曲率空间能更灵活地编码环结构——纯双曲空间受限于树状层次假设，而超双曲空间的时间维度可容纳环状交互。Collab 和 Reddit-multi-12K 上提升较小，可能因为这些学术合作与社交网络图的环结构不明显，或所需曲率混合与实验签名不完全匹配。

### 消融实验：签名选择与维度效应

**签名消融**（Table 1，Zachary 空手道俱乐部层次提取）：在 4 维流形上，$\mathcal{P}_1^{1,3}$ 和 $\mathcal{P}_1^{3,1}$ 的层次提取评分显著优于纯双曲和纯椭圆，验证了混合签名的必要性。Table 1 同时显示训练时间：超双曲模型比欧氏模型慢约 **25%**，因为需要计算伪黎曼梯度（含正交投影 $\Pi_{\mathbf{x}}$）和平行传输。

**维度消融**（Section 5.2）：当隐层维度升至 $d=600$ 时，欧氏、双曲和超双曲 GCN 均达到相同精度。原因是模型过参数化，在训练集上迅速达到 100% 准确率，流形曲率的表示优势被容量冗余掩盖。这表明超双曲几何的优势主要体现在**有限容量下的归纳偏置**，而非万能近似能力。

### 优化收敛性验证

Figure 2（左）展示了不同 $p$ 值下损失函数（式 12）的收敛曲线。使用 $-G\lambda$ 作为下降方向时，所有签名均稳定收敛；而使用 $-\lambda$（未修正的欧氏梯度方向）在非正定度量下**不是下降方向**，算法不收敛（Section 5.1）。这实证了 Section 3.4 的理论分析：伪黎曼梯度必须通过度量矩阵 $G$ 修正才能保证下降性。

### 表示可视化

Figure 2（右）展示了在 Zachary 空手道俱乐部上学得的 $\mathcal{P}_1^{1,1}$ 表示的立体投影。节点颜色对应两个派系，投影空间中两派节点自然分离，验证了超双曲表示在无监督设置下捕捉层次社群结构的能力。

### 失败模式与局限

1. **高维失效**：$d=600$ 时所有几何趋同，超双曲优势消失。实际应用中需在表示容量与几何偏置间权衡。

2. **签名选择缺乏理论指导**：实验通过网格搜索确定最优 $(p,q)$，但论文未提供基于数据特性（如图的环结构密度）自动选择签名的准则。

3. **训练效率瓶颈**：约 25% 的额外时间开销源于伪黎曼梯度计算和平行传输，限制了在大规模图（百万级节点）上的可扩展性。

4. **任务覆盖有限**：仅在节点分类和图分类上验证，未探索链接预测、推荐系统等需要距离建模的任务，也未与乘积空间方法（如 $\mathbb{H} \times \mathbb{S}$ 的笛卡尔积）进行对比。

### 补充图表

![[assets/figures/papers/paper_list_l16_https_openreview_net_attachment_id_sf2BxJNXC3K_name_supplementary_materi/figures/003_Table_1.jpg]]
*Table 1: Evaluation scores for the different learned representations (mean ± standard deviation)*

![[assets/figures/papers/paper_list_l16_https_openreview_net_attachment_id_sf2BxJNXC3K_name_supplementary_materi/figures/004_Table_2.jpg]]
*Table 2: Statistics of the citation network datasets*



## 定位与知识库关联

### 1. 与基线方法的关系

本文提出的超双曲神经网络（Ultrahyperbolic Neural Networks）位于表示学习流形几何谱系的一个关键空白地带：它首次将可端到端学习的深度参数化模型从定曲率空间（欧氏、双曲、椭圆）推广到具有混合签名的伪黎曼商流形。

**相对于欧几里得基线：**
标准欧氏图卷积网络（**GCN**, Kipf & Welling, ICLR 2017）将所有数据嵌入零曲率的平坦空间，无法显式编码层次结构或环状结构。本文方法将表示流形从 $\mathbb{R}^d$ 替换为 $\mathcal{P}_r^{p,q}$，通过签名 $(p,q)$ 的选择灵活调节正/负曲率成分的比例。实验表明，在具有环状结构的层次图（如 D&D、Enzymes）上，超双曲 GCN 较欧氏 GCN 的准确率提升可达 5-6.7 个百分点（Table 5），而在无环引文网络（Cora、Citeseer、Pubmed）上也有 6-11 个百分点的增益（Table 3）。

**相对于双曲基线：**
双曲图卷积网络（**HGCN**, Liu et al., NeurIPS 2019）和庞加莱球模型均受限于恒定负曲率，仅擅长建模树状层次结构。本文的商流形 $\mathcal{P}_r^{p,q}$ 在 $p>0, q>0$ 时同时包含类空（正曲率）和类时（负曲率）测地线，从而能统一表达层次与环状关系。Table 5 显示，在带环图分类任务上，超双曲 GCN 显著优于洛伦兹模型和庞加莱模型；但在纯层次数据上，纯双曲签名 $\mathcal{P}_1^{0,q}$ 的性能与超双曲签名相当，表明混合签名的增益主要来自对环状结构的额外建模能力。

**相对于椭圆基线：**
当 $q=0$ 时，$\mathcal{P}_r^{p,0}$ 退化为椭圆几何（正曲率），可视为本文框架的一个特例。Table 3 显示，纯椭圆签名 $\mathcal{P}_1^{4,0}$ 在引文网络节点分类上表现最差，验证了仅用正曲率不足以捕获引文图的层次特性。

**相对于非参数嵌入方法：**
Law & Stam (2020) 在超双曲空间上学习了非参数嵌入，但由于原始伪球面 $\mathcal{S}_r^{p,q}$ 上存在无法由完整测地线连接的点对，梯度不能平行传输，无法优化参数化模型。本文的核心突破在于引入商流形 $\mathcal{P}_r^{p,q} = \mathcal{S}_r^{p,q} / \{\pm 1\}$，通过对跖点等价保证任意两点间至少有一条测地线，从而使黎曼梯度下降成为可能。这一几何改造是本文方法区别于所有先前超双曲表示工作的根本分界线。

### 2. 方法适用边界

**数据特征边界：**
- **优势场景：** 同时包含层次结构和环状结构的关系数据，如蛋白质交互网络（Enzymes、Proteins）、含环的化合物图（D&D）、社交网络中的派系重叠。Zachary 空手道俱乐部的可视化（Figure 2 右）直观展示了 $\mathcal{P}_1^{1,1}$ 表示如何同时捕捉两个派系的分离（类空测地线）和各自内部的层次（类时测地线）。
- **退化场景：** 在极高维度（$d=600$）下，模型过参数化导致欧氏、双曲和超双曲 GCN 的精度趋同（Section 5.2），此时流形曲率的表征优势被容量冗余所淹没。
- **未验证场景：** 论文仅在图表示学习任务上验证，未探索其在自然语言处理、计算机视觉或物理模拟等领域的适用性。也未与乘积空间方法（如 $\mathbb{P} \times \mathbb{P} \times \mathbb{R}$）进行系统比较。

**计算资源边界：**
超双曲模型的训练时间比欧几里得方法慢约 25%（Table 1），因为每次前向/反向传播需要计算伪黎曼梯度（含正交投影算子 $\Pi_{\mathbf{x}}$）和平行传输算子 $P_{\mathbf{x}\sim\mathbf{y}}^{\overline{\gamma}}$。这限制了在大规模图（如千万级节点的社交网络）上的直接应用。

**签名选择边界：**
签名 $(p,q)$ 的选择目前依赖验证集上的网格搜索，缺乏理论指导。Table 1 和 Table 3 的消融实验表明，$\mathcal{P}_1^{1,3}$ 和 $\mathcal{P}_1^{3,1}$ 通常表现最佳，但最优签名因数据集而异，且论文未提供类似 Gromov $\delta$-双曲条件的理论判据来从数据拓扑中推断合适的 $(p,q)$。

### 3. 局限与开放问题

**理论局限：**
- **带环图的理论保证缺失：** 双曲几何对无环图有 Gromov 超薄三角条件的理论支撑，但本文未为带环图在超双曲空间中的表示提供类似的理论保证。最优签名 $(p,q)$ 与图的环结构复杂度之间的定量关系仍是开放问题。
- **定曲率假设：** 商流形 $\mathcal{P}_r^{p,q}$ 仍是常曲率空间，无法自适应地调整不同区域的曲率符号和大小。对于曲率在图中非均匀分布的数据（如同时包含稠密团和稀疏链的异质图），定曲率假设可能成为瓶颈。

**方法局限：**
- **训练效率瓶颈：** 约 25% 的额外时间开销源于伪黎曼梯度和平行传输的计算，这两者都涉及度量矩阵 $\mathbf{G}$ 的乘法以及正交投影。当流形维度 $d$ 增大时，这些操作的计算复杂度为 $O(d^2)$，可能成为高维场景的瓶颈。
- **优化稳定性：** 论文证明了使用 $-\mathbf{G}\lambda$ 作为下降方向可保证收敛，而直接使用 $-\lambda$ 在非正定度量下不是下降方向（Section 5.1）。然而，当梯度范数极小或测地线距离接近分段函数的切换点（$|\langle\mathbf{x},\mathbf{y}\rangle_q/r^2| = 1$）时，数值稳定性仍需进一步分析。

**开放问题：**
1. **乘积空间扩展：** 能否将商流形 $\mathcal{P}_r^{p,q}$ 与欧氏空间 $\mathbb{R}^k$ 或双曲空间 $\mathbb{H}^m$ 组合成乘积流形（如 $\mathcal{P}_r^{p,q} \times \mathbb{H}^m \times \mathbb{R}^k$），以更精细地匹配数据中不同子结构的几何特性？
2. **时变曲率推广：** 该框架能否推广到非定曲率的一般伪黎曼流形？如果可以，如何在缺乏闭式测地线公式的情况下进行高效的前向/反向传播？
3. **大规模可扩展性：** 在百万级节点图上，超双曲 GCN 的扩展性如何？是否可以通过近似平行传输或随机梯度下降的变体来降低计算开销？
4. **签名自动推断：** 能否设计一种元学习或神经架构搜索方法，从数据中自动推断最优签名 $(p,q)$，而非依赖昂贵的网格搜索？
5. **社会影响的双面性：** 论文指出该方法改进的图表示能力可能被用于社交网络分析，具有正反两面社会影响。如何在技术部署中建立负责任的审计机制，防止对特定群体的歧视性推断，是一个值得关注的伦理问题。



## 原文 PDF

![[paperPDFs/NEURIPS_2021/Ultrahyperbolic_Neural_Networks.pdf]]
