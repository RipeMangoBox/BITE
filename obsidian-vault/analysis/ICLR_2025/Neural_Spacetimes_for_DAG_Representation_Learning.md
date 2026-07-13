---
title: "Neural Spacetimes for DAG Representation Learning"
type: paper
paper_level: A
venue: ICLR
year: 2025
pdf_ref: paperPDFs/ICLR_2025/Neural_Spacetimes_for_DAG_Representation_Learning.pdf
code_link: https://github.com/haitzsaezdeocariz/NeuralSpaceTimesICLR2025
project_link: https://github.com/haitzsaezdeocariz/NeuralSpaceTimesICLR2025
aliases:
- NSN
- NSDRL
tags:
- ICLR_2025
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将表示解耦为可学习的空间准度量（捕捉边权重）和可学习的时间偏序（捕捉因果方向），并联合优化两者的神经参数化几何。"
primary_logic: "通过乘积流形将空间结构与因果结构分离，利用神经网络并行学习准度量和多时间维度的偏序，实现任意DAG的低失真、因果一致的连续嵌入。"
claims:
- "通用嵌入定理保证任意k点DAG可以嵌入到神经时空，失真为1+O(log(k))，同时精确保留因果结构。"
- "在合成DAG和真实网络（网页超链接、基因调控网络）上，神经时空嵌入的失真显著低于固定的闵可夫斯基和德西特空间基线。"
- "Cornell (WebKB) dim 2 上 最大失真 (Max Distortion) = 1.31 (NST)"
- "In silico DAG dim 2, metric 1 上 平均失真 (Avg Distortion ± sdev) = 1.13 ± 0.37 (NST)"
---

# Neural Spacetimes for DAG Representation Learning

> [!tip] 核心洞察
> 通过乘积流形将空间结构与因果结构分离，利用神经网络并行学习准度量和多时间维度的偏序，实现任意DAG的低失真、因果一致的连续嵌入。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向DAG表示学习的神经时空模型 |
| 英文题名 | Neural Spacetimes for DAG Representation Learning |
| 会议/期刊 | ICLR 2025 |
| Links | [paper](https://arxiv.org/abs/2408.13885) · [GitHub](https://github.com/haitzsaezdeocariz/NeuralSpaceTimesICLR2025) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Neural Spacetime (NST) |
| Dataset | Cornell (WebKB) dim 2, In silico DAG dim 2, metric 1, Wisconsin (WebKB) dim 4 |

> [!tip] 效果简介
> - Cornell (WebKB) dim 2 上，最大失真 (Max Distortion) 为 1.31 (NST)，对比 9.43 (Minkowski)，变化 −8.12 (减少86%)。
> - In silico DAG dim 2, metric 1 上，平均失真 (Avg Distortion ± sdev) 为 1.13 ± 0.37 (NST)，对比 2.86 ± 5.22 (Minkowski)，变化 −1.73。
> - Wisconsin (WebKB) dim 4 上，方向性 (Directionality) 为 0.89 (NST)，对比 0.90 (Minkowski), 0.90 (De Sitter)，变化 与基线相当（均为高方向性）。

## 概要

有向无环图（DAG）广泛存在于网页超链接、引文网络、基因调控等真实场景中，其边不仅携带权重信息，还编码了节点间的因果方向。将这类图嵌入连续几何空间，核心挑战在于**同时保持距离度量与因果顺序**。现有方法多采用固定时空几何（如闵可夫斯基空间或德西特空间），但这些几何的度量与因果结构不可学习，难以灵活适配具有复杂拓扑的DAG，导致嵌入失真大或因果方向性丢失。

针对这一瓶颈，本文提出**神经时空模型（Neural Spacetime, NST）**，其核心思路是将表示解耦为两个可学习的组件：一个**神经准度量（neural quasi-metric）**负责捕捉节点间的加权距离，一个**神经偏序（neural partial order）**负责捕捉因果方向。二者通过乘积流形组合，并由一个共享的MLP编码器将原始节点特征映射到统一的中间表示空间，随后分别处理空间坐标与时间坐标。整个三元组 $(\mathcal{E}, \mathcal{D}, \mathcal{T})$ 以端到端方式联合训练，使几何本身随数据自适应演化。

理论层面，**通用嵌入定理（Theorem 1）** 保证：任意 $k$ 点加权DAG可嵌入神经时空，距离失真不超过 $1 + O(\log(k)^5)$，且因果结构被精确保留。实验层面，在合成DAG与真实网络（WebKB网页超链接、基因调控网络）上，NST的嵌入失真显著低于固定闵可夫斯基和德西特空间基线——例如在Cornell数据集（dim=2）上最大失真从9.43降至1.31（下降86%），同时方向性保持能力与基线相当。消融实验进一步表明，神经准度量在树嵌入任务上比神经雪花（Neural Snowflake）收敛更快、失真更低。

综上，NST通过将几何参数化，实现了对任意DAG的低失真、因果一致的连续嵌入，为图表示学习提供了一种几何可塑的新范式。



### 有向无环图的表示学习困境

有向无环图（DAG）广泛存在于现实世界的复杂系统中，从网页超链接网络、引文网络到基因调控网络，节点间的有向边不仅编码了拓扑连接，更承载了因果方向与度量距离的双重信息。对这些图进行低维连续嵌入，是下游任务（如节点分类、链接预测、因果推断）的关键前置步骤。

然而，DAG表示学习面临一个根本性瓶颈：**空间距离与因果顺序的纠缠**。一条有向边同时规定了“源节点在因果上先于目标节点”和“两节点之间存在某种距离”，而这两者并不总能被同一个几何结构同时完美捕获。传统的图嵌入方法往往将图视为无向的度量空间，忽略方向性；而专门处理有向图的方法又难以在保持因果结构的同时，忠实地重现节点间的加权距离。

### 固定时空几何的局限性

近年来，受物理学启发的时空嵌入方法试图在一个统一的几何框架中同时建模空间距离和因果结构。其核心思想是将节点映射为时空流形中的“事件”，利用时空的因果锥结构来编码有向边，同时用流形上的测地线距离来编码边权重。然而，现有方法几乎都采用**固定的时空几何**：

- **闵可夫斯基时空嵌入**（Minkowski space embedding）：使用固定的闵可夫斯基度量，具有单一时间维度和平坦的空间结构。
- **德西特时空嵌入**（De Sitter space embedding）：使用固定的德西特度量，具有恒定正曲率。

这些固定几何方案存在一个共同缺陷：**几何结构不可学习**。当输入DAG的因果结构和度量结构与预设几何不匹配时，嵌入将产生显著失真。例如，一个树状的层级DAG可能无法被平坦的闵可夫斯基空间低失真地容纳；而一个具有复杂反链（incomparability）结构的DAG，在单一时间维度下必然丢失部分偏序信息。实验证据表明，在合成DAG和真实网络（如WebKB数据集）上，固定几何基线的最大失真可达9.43，而可学习几何的神经时空模型仅为1.31（Table 10）。

### 核心动机：从固定几何到可学习几何

上述困境指向一个清晰的研究动机：**能否让时空几何本身成为可学习的对象？** 即，不再预设一个固定的度量张量或因果结构，而是通过神经网络参数化空间的距离函数和时间偏序关系，使其在训练过程中自适应地塑造为最适合输入DAG的几何形态。

这一动机催生了**神经时空模型**（Neural Spacetime, NST）的核心设计理念：将表示解耦为可学习的空间准度量（捕捉边权重）和可学习的时间偏序（捕捉因果方向），并通过乘积流形将两者联合优化。这种“空间-时间解耦 + 联合学习”的范式，使得模型能够灵活适配任意DAG的复杂因果和度量结构，而不受预设几何假设的束缚。

### 理论支撑与实证前景

从理论角度看，论文给出了一个**通用嵌入定理**（Theorem 1）：任意有限k点DAG可以嵌入到神经时空中，失真为 $1 + O(\log k)$，同时精确保留因果结构。这一定理为可学习几何的表示能力提供了坚实保障——神经时空仅需 $O(k^2)$ 个参数即可全局嵌入一个加权DAG。

从实证角度看，初步证据表明神经时空在合成DAG和真实世界网络（网页超链接、基因调控网络）上均能显著降低嵌入失真，同时保持与固定几何基线相当的方向性捕获能力。这种“低失真 + 高保序”的组合优势，正是DAG表示学习领域长期追求的目标。



## 核心方法与创新机理

### 问题瓶颈：固定几何的刚性约束

传统时空嵌入方法（如闵可夫斯基空间或德西特空间嵌入）将DAG映射到具有固定度量和单一时间维度的几何流形上。这种刚性设计导致两个根本性矛盾：

1. **空间度量的不可适配性**：固定度量（如闵可夫斯基度量）无法灵活适应不同DAG的边权重分布和局部几何结构，导致高失真嵌入。
2. **因果方向性的容量瓶颈**：单一时间维度限制了偏序关系的表达能力，当DAG中存在复杂反链（incomparable pairs）时，无法在保持方向性的同时实现低失真。

实证证据显示，在Cornell（WebKB）数据集上，固定闵可夫斯基空间嵌入的最大失真高达9.43，而神经时空模型降至1.31（Table 10），失真减少86%。这揭示了固定几何的根本性局限。

### 核心创新：可学习几何的三元解耦

神经时空（Neural Spacetime, NST）的核心创新在于将DAG表示学习解耦为三个可协同训练的神经组件，构成可学习三元组 $\mathcal{S} = (\mathcal{E}, \mathcal{D}, \mathcal{T})$（Figure 1）：

| 组件 | 功能 | 关键创新 |
|------|------|----------|
| **特征编码器 $\mathcal{E}$** | MLP将节点特征映射到 $\mathbb{R}^{D+T}$ 中间空间 | 为空间和时间处理提供统一的欧氏潜在表示 |
| **神经准度量 $\mathcal{D}$** | 学习空间距离函数 | 替代固定度量，自适应捕捉边权重和测地线结构 |
| **神经偏序 $\mathcal{T}$** | 学习多时间维度因果顺序 | 替代单一时间维度，增强偏序表达能力 |

这种解耦设计的核心洞察是：**通过乘积流形将空间结构（准度量）与因果结构（偏序）分离，使两者可以独立优化却协同工作**。空间分量专注于最小化距离失真，时间分量专注于保持因果方向性，避免了单一几何中两者的相互干扰。

### Changed Slot 1：从固定度量到可学习神经准度量

**基线方案**：闵可夫斯基空间和德西特空间使用固定的黎曼度量，其距离函数形式在训练前即已确定，无法根据数据调整。

**NST方案**：引入可学习的神经准度量 $\mathcal{D}$，其核心机制包括：

1. **自适应激活函数**（Equation 2 / Definition 3）：
   $$\sigma_{s,l}(x) = \begin{cases} \operatorname{sgn}(x)|x|^s, & |x|<1 \\ \operatorname{sgn}(x)|x|^l, & |x|\ge 1 \end{cases}$$
   可训练参数 $s, l$ 分别控制小尺度（$<1$）和大尺度（$\ge 1$）距离的扩张/收缩行为，使模型能灵活适应图的局部和全局几何特性。

2. **迭代深度变换**（Equation 3）：
   $$\mathcal{D}(\hat{x}_u,\hat{x}_v) = \mathsf{W}_J \sigma_{s_J,l_J} \bullet (u_{J-1}); \quad u_j = \mathsf{W}_j \sigma_{s_j,l_j} \bullet (u_{j-1})$$
   其中 $u_0 = |\sigma_{s_0,l_0} \bullet (\hat{x}_u)_{1:D} - \sigma_{s_0,l_0} \bullet (\hat{x}_v)_{1:D}|$，权重矩阵 $\mathsf{W}_j$ 约束为正以保证准度量性质。这种多层结构受神经雪花（Neural Snowflake）启发，但通过可训练的逐层激活参数实现了更灵活的几何形变。

消融实验（Table 3）表明，在树嵌入任务上，神经准度量（NQM）比神经雪花收敛更快且失真更低，验证了自适应激活函数的优势。

### Changed Slot 2：从单一时间维度到可学习多时间维度偏序

**基线方案**：闵可夫斯基和德西特空间依赖单一时间维度的固定洛伦兹因果结构，偏序关系完全由时空度规的符号决定，缺乏灵活性。

**NST方案**：引入可学习的神经偏序 $\mathcal{T}$，支持 $T$ 个时间维度：

1. **偏序映射网络**（Equation 4）：
   $$\mathcal{T}(\hat{x}_u) = z_{\tilde{J}}; \quad z_j = \mathsf{V}_j \sigma_{\bar{s}_j,\bar{s}_j} \circ \mathrm{LeakyReLU} \bullet (z_{j-1}) + b_j$$
   其中 $z_0 = (\hat{x}_u)_{D+1:D+T}$，权重矩阵 $\mathsf{V}_j$ 约束为正，LeakyReLU激活确保单调性传递。

2. **乘积序定义**（Equation 5）：
   $$\hat{x}_u \lesssim^{\mathcal{T}} \hat{x}_v \Longleftrightarrow \mathcal{T}(\hat{x}_u)_t \le \mathcal{T}(\hat{x}_v)_t, \; \forall t=D+1,\dots,D+T$$
   通过在所有时间维度上同时满足坐标分量不等式来定义偏序关系。多个时间维度显著增强了对复杂反链结构的建模能力。

**关键机制**：使用SteepSigmoid（Figure 6）作为因果损失函数中的松弛约束，其陡峭系数使梯度信号在违反偏序时更强，促使模型更精确地满足因果条件。

### 理论保证：通用嵌入定理

Theorem 1为上述创新提供了理论支撑：**任意 $k$ 点DAG可嵌入到神经时空，失真为 $1+\mathcal{O}(\log k)$，同时精确保留因果结构**。更重要的是，该嵌入仅需 $\mathcal{O}(k^2)$ 参数量，证明了神经时空模型在有限容量下即可实现近似保距和精确保序的双重目标。这一理论结果直接解释了为何可学习几何能显著优于固定几何基线。

### 创新总结

神经时空的核心创新不在于引入新的网络架构，而在于**将几何本身参数化为可学习的神经网络，使空间度量和时间偏序能够根据数据自适应优化**。这种"学习几何"而非"在固定几何中学习嵌入"的范式转换，从根本上解决了固定时空几何的刚性问题，实现了DAG表示学习中距离保真度与因果一致性的统一优化。



神经时空（Neural Spacetime, NST）将DAG嵌入问题形式化为一个可学习的三元组 $\boldsymbol{S} = (\mathcal{E}, \mathcal{D}, \mathcal{T})$，通过**乘积流形**将空间结构与因果结构解耦，并联合端到端优化。其核心设计逻辑是：用可学习的神经准度量 $\mathcal{D}$ 捕捉节点间的加权距离，用可学习的神经偏序 $\mathcal{T}$ 捕捉因果方向性，而特征编码器 $\mathcal{E}$ 则为二者提供共享的中间表示。这一分离使得模型能够灵活适配任意DAG的复杂度量与因果结构，避免了固定时空几何（如Minkowski、De Sitter空间）因度量不可学习而导致的嵌入失真或方向性丢失问题。

### 模块关系与数据流

整个pipeline由三个神经网络模块串联构成，数据流如下（参见 Figure 1）：

1. **特征编码器 $\mathcal{E}: \mathbb{R}^N \to \mathbb{R}^{D+T}$**  
   一个MLP，将原始节点特征映射到 $D+T$ 维的中间欧氏空间。其中前 $D$ 维作为空间坐标，后 $T$ 维作为时间坐标。该编码器为后续的空间距离计算和时间偏序判断提供统一的输入表示。

2. **神经准度量 $\mathcal{D}: \mathbb{R}^{D+T} \times \mathbb{R}^{D+T} \to [0,\infty)$**  
   基于编码向量的前 $D$ 维空间坐标，通过可学习的迭代变换计算节点间的准度量距离。其核心是带可训练参数 $s,l$ 的分段幂律激活函数 $\sigma_{s,l}(x)$（Equation 2），该激活在小尺度（$|x|<1$）和大尺度（$|x|\ge 1$）分别以不同指数进行扩张或收缩，使模型能够自适应地调节局部和全局距离的缩放。多层正权重矩阵 $\mathsf{W}_j$ 与逐元素激活的堆叠（Equation 3）从空间坐标差中学习一个非欧的距离函数。

3. **神经偏序 $\mathcal{T}: \mathbb{R}^{D+T} \to \mathbb{R}^T$**  
   基于编码向量的后 $T$ 维时间坐标，通过带正权重矩阵 $\mathsf{V}_j$、LeakyReLU激活和偏置项的迭代变换（Equation 4），为每个节点输出一个 $T$ 维时间嵌入。因果偏序关系由所有时间维度上的分量比较定义（Equation 5）：
   $$\hat{x}_u \lesssim^{\mathcal{T}} \hat{x}_v \Longleftrightarrow \mathcal{T}(\hat{x}_u)_t \le \mathcal{T}(\hat{x}_v)_t, \quad \forall t=D+1,\dots,D+T$$
   这一乘积偏序支持多个时间维度，能够处理传统单时间维度无法编码的复杂反链结构。

### 联合优化机制

三个模块在端到端训练中协同优化。损失函数由两部分组成：距离损失 $\mathcal{L}_{uv}^{D}$ 仅对有边节点对计算预测准度量距离与真实边权重的MSE；因果损失 $\mathcal{L}_{uv}^{C}$ 使用SteepSigmoid函数鼓励有向边两端在所有时间维度上满足源节点分量小于目标节点分量。这种设计使得空间分量专注于最小化距离失真，时间分量专注于保持因果一致性，二者通过共享编码器实现协调。

### 理论保证

**Theorem 1（通用时空嵌入）** 为上述框架提供了理论支撑：任意 $k$ 点DAG可以嵌入到神经时空中，失真上界为 $1 + \mathcal{O}(\log k)$，同时精确保留因果结构。该定理表明，NST仅需 $\mathcal{O}(k^2)$ 参数即可实现全局嵌入，从原理上解释了可学习几何相较于固定几何的优势来源。



神经时空（**Neural Spacetime, NST**）的核心架构是一个可学习的三元组 $\mathcal{S} = (\mathcal{E}, \mathcal{D}, \mathcal{T})$，如 **Figure 1** 所示。给定一个有向无环图（DAG），编码器 $\mathcal{E}$ 将节点特征映射为时空流形中的事件坐标，而神经准度量 $\mathcal{D}$ 和神经偏序 $\mathcal{T}$ 则并行地学习空间几何与时间因果结构。

### 特征编码器 $\mathcal{E}$

编码器 $\mathcal{E}: \mathbb{R}^N \to \mathbb{R}^{D+T}$ 是一个多层感知机（MLP），将原始节点特征映射到一个 $D+T$ 维的中间欧氏空间。该向量的前 $D$ 维作为空间坐标，后 $T$ 维作为时间坐标，供后续模块分别处理。

### 神经准度量 $\mathcal{D}$

空间分量 $\mathcal{D}: \mathbb{R}^{D+T} \times \mathbb{R}^{D+T} \to [0, \infty)$ 是一个可学习的准度量，用于捕捉节点间的加权距离。其构造基于两个关键组件：

**激活函数**（Definition 3）：定义逐元素激活函数为分段幂函数，通过可训练参数 $s, l$ 分别控制小尺度（$|x| < 1$）和大尺度（$|x| \ge 1$）距离的扩张与收缩行为：

$$
\sigma_{s,l}(x) = \begin{cases} 
\operatorname{sgn}(x)|x|^s, & |x|<1 \\
\operatorname{sgn}(x)|x|^l, & |x|\ge 1 
\end{cases}
$$

**迭代表示**：给定两个节点的空间坐标 $(\hat{x}_u)_{1:D}$ 和 $(\hat{x}_v)_{1:D}$，准度量 $\mathcal{D}$ 通过 $J$ 层迭代变换从坐标差的绝对值中学习距离：

$$
\begin{aligned}
u_0 &= \big|\sigma_{s_0,l_0} \bullet (\hat{x}_u)_{1:D} - \sigma_{s_0,l_0} \bullet (\hat{x}_v)_{1:D}\big| \\
u_j &= \mathsf{W}_j \,\sigma_{s_j,l_j} \bullet (u_{j-1}), \quad j=1,\dots,J-1 \\
\mathcal{D}(\hat{x}_u, \hat{x}_v) &= \mathsf{W}_J \,\sigma_{s_J,l_J} \bullet (u_{J-1})
\end{aligned}
$$

其中 $\mathsf{W}_j$ 是带有正约束的权重矩阵，$\bullet$ 表示逐元素操作。该结构受神经雪花（Neural Snowflake）启发，但通过可训练的尺度参数 $s_j, l_j$ 实现了更灵活的距离度量学习。消融实验表明，在树嵌入任务上，神经准度量的收敛速度与最终失真均优于神经雪花（**Table 3**）。

### 神经偏序 $\mathcal{T}$

时间分量 $\mathcal{T}: \mathbb{R}^{D+T} \to \mathbb{R}^T$ 是一个可学习的偏序映射，用于判断节点间的因果先后关系。其迭代表示利用 LeakyReLU 激活和正权重矩阵，对时间坐标部分进行多层变换：

$$
\begin{aligned}
z_0 &= (\hat{x}_u)_{D+1:D+T} \\
z_j &= \mathsf{V}_j \,\sigma_{\bar{s}_j,\bar{s}_j} \circ \mathrm{LeakyReLU} \bullet (z_{j-1}) + b_j, \quad j=1,\dots,\tilde{J} \\
\mathcal{T}(\hat{x}_u) &= z_{\tilde{J}}
\end{aligned}
$$

其中 $\mathsf{V}_j$ 是带正约束的权重矩阵，$b_j$ 为偏置项。基于此映射，两个节点的偏序关系由所有时间维度上的坐标分量比较定义：

$$
\hat{x}_u \lesssim^{\mathcal{T}} \hat{x}_v \Longleftrightarrow \mathcal{T}(\hat{x}_u)_t \le \mathcal{T}(\hat{x}_v)_t, \;\; \forall t = D+1,\dots,D+T
$$

这种多时间维度的设计使得模型能够处理反链（incomparable elements），克服了单一时间维度的局限性。

### 训练损失函数

模型通过端到端训练联合优化空间距离保持与因果方向保持，损失函数由两部分组成：

**距离损失**：仅对有边节点对计算预测距离与真实边权重的均方误差：

$$
\mathcal{L}_{uv}^{\mathcal{D}} = A_{uv} \; \mathrm{MSE}\big(\mathcal{D}(\hat{x}_u,\hat{x}_v), D_{uv}\big)
$$

**因果损失**：鼓励有向边的源节点在所有时间维度上的嵌入分量均小于目标节点，使用带陡峭系数的 SteepSigmoid 函数（见 **Figure 6**）以更快趋于零：

$$
\mathcal{L}_{uv}^{\mathcal{C}} = A_{uv} \sum_{t=1}^{T} \mathrm{SteepSigmoid}\big(\mathcal{T}(\hat{x}_u)_t - \mathcal{T}(\hat{x}_v)_t\big)
$$

总损失为上述两项的加权和，权重由验证集调参确定。

### 理论保证

**Theorem 1（Universal Spacetime Embeddings）** 为上述架构提供了全局嵌入保证：任意 $k$ 点有限因果度量空间可嵌入到神经时空中，失真界限为 $1 + \mathcal{O}(\log k)$，同时精确保留因果结构。具体地，存在编码 $\mathcal{E}$、准度量 $\mathcal{D}$ 和偏序 $\mathcal{T}$，使得对所有节点对 $(x_u, x_v)$ 满足：

$$
d(x_u, x_v) \le \mathcal{D}(\mathcal{E}(x_u), \mathcal{E}(x_v)) \le \mathcal{O}(\log k)^5 \, d(x_u, x_v)
$$

值得注意的是，该嵌入所需的参数量仅为 $\mathcal{O}(k^2)$，远小于理论上的最坏情况边界。



## 实验与关键发现

### 核心实验设置

神经时空（NST）模型的实验验证围绕三个核心维度展开：**嵌入失真**（距离保持能力）、**方向性**（因果顺序保持能力）以及**下游任务迁移**。所有实验均采用相同的训练超参数与评估协议，固定几何基线（Minkowski、De Sitter）使用与NST相同的MLP特征编码器，仅几何度量部分保持固定，保证比较的公平性（见 Appendix D.5）。训练损失由距离损失 $\mathcal{L}_{uv}^{D}$ 和因果损失 $\mathcal{L}_{uv}^{C}$ 联合构成，仅优化一跳邻域的有边节点对。

### 主实验结果

#### 合成DAG嵌入

在合成加权DAG上，NST在不同距离函数（metric 1–4）和嵌入维度（D=T=2,4,10）下均展现出显著优于固定时空基线的嵌入质量。以 **Table 9** 中 metric 1、维度2的设置为例：NST的平均失真为 **1.13 ± 0.37**，而Minkowski空间嵌入为 **2.86 ± 5.22**，降幅达 1.73，且方差大幅收窄。这一优势在高维设置下进一步扩大——维度10时NST的平均失真接近理论最优值1.0，而Minkowski基线仍存在明显偏差。

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/022_Table_9.jpg]]
*Table 9: DAG embedding results. Embedding dimension D = T = 2 , 4 , 1 0*

方向性指标方面，NST在所有合成设置下均达到或接近1.0，表明其可学习的神经偏序能够精确保留DAG中的因果方向，与固定洛伦兹因果结构的基线持平或更优。

#### 真实世界网络嵌入

在真实世界数据集上，NST的低失真优势更为突出。以 **Table 10** 中 WebKB 的 Cornell 数据集（维度2）为例：

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/023_Table_10.jpg]]
*Table 10: Embedding results for real-world web page hyperlink graph datasets and gene regulatory networks*

| 方法 | 最大失真 (Max Distortion) |
|------|--------------------------|
| **NST** | **1.31** |
| Minkowski | 9.43 |
| De Sitter | 8.76 |

NST相较Minkowski基线的最大失真减少 **86%**（−8.12），相较De Sitter减少约85%。在 Wisconsin 数据集（维度4）上，NST的方向性为 **0.89**，与Minkowski（0.90）和De Sitter（0.90）基本持平，表明NST在显著降低距离失真的同时，并未牺牲因果顺序的保持能力。

在基因调控网络（Dream5数据集）上，NST同样保持了较低的失真和较高的方向性，验证了该框架在生物网络场景下的适用性。

### 消融与分析

#### 图连接度的影响

**Table 4**（arxiv引用网络）的消融实验揭示了图结构稀疏性对嵌入质量的双向影响：随着图连接度降低（通过边采样控制），平均失真呈下降趋势，但方向性捕获能力同步减弱。这一现象符合直觉——稀疏图中的距离约束更少，模型更容易拟合，但同时可用于学习因果方向的边监督信号也相应减少。该消融表明，**NST的性能边界受图结构密度与因果信号丰富度的共同制约**。

#### 神经准度量 vs. 神经雪花

**Table 3**（树嵌入失真）对比了神经准度量（NQM）与神经雪花（Neural Snowflake）在树结构上的嵌入能力。结果表明，NQM在收敛速度和最终失真两方面均优于神经雪花。这验证了NQM中可训练的逐元素激活函数 $\sigma_{s,l}$（通过可学习参数 $s, l$ 分别控制小尺度和大尺度距离的扩张/收缩）相比固定形式的雪花度量具有更强的几何适配能力。

#### 激活函数设计的影响

**Figure 5** 可视化了神经准度量激活函数及其导数，以及偏序激活（含/不含LeakyReLU）的行为。**Figure 6** 对比了标准Sigmoid与SteepSigmoid函数：SteepSigmoid通过引入陡峭系数，在输入为负时更快趋于零，使得因果损失 $\mathcal{L}_{uv}^{C}$ 能更精确地惩罚违反偏序的节点对，这是NST实现高方向性的关键设计细节。

### 下游任务迁移

**Table 11** 报告了异配图节点分类任务上的测试准确率。将NST学到的空间特征和时间嵌入拼接至原始节点特征后，下游分类器的性能获得一致提升（标记为 ✓ 的设置），验证了神经时空特征包含对图结构预测有用的信息。该实验同时表明，NST的嵌入空间不仅服务于几何重构目标，其学到的表示具有可迁移的判别能力。

### 失败模式与局限性

1. **局部优化与全局失真**：当前训练仅优化一跳邻域的距离和因果性，不显式保证全局测地线距离的精确重现。在长程依赖显著的图上，可能出现局部失真低但全局路径距离偏差大的情况。
2. **有向环的不支持**：NST框架专为DAG设计，其偏序定义要求严格的反自反性和传递性。对于包含有向环的一般有向图，时间偏序的条件无法直接满足，需要框架层面的扩展。
3. **空间分量的伪度量退化**：当时间维度 $T > 0$ 时，空间分量退化为伪度量（不满足点分离性），意味着两个不同节点可能被映射到空间距离为零的位置。这在部分需要严格空间区分性的应用中可能造成歧义。
4. **大规模验证缺失**：论文未在百万节点级别的图上进行验证，模型在大规模场景下的扩展性和优化稳定性有待进一步研究。

### 未解决问题

- 能否将神经时空框架扩展至任意有向图（包括含环图），而不仅限于DAG？
- 如何在大图场景下实现高效的全局优化，避免仅依赖局部邻域？
- 除了节点分类外，神经时空特征能否用于更多下游任务（如链接预测、因果推断）？
- 能否进一步减少时间维度需求，例如通过更精巧的偏序编码实现 $T=1$ 时仍能处理复杂反链？

### 补充图表

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/011_Figure_5.jpg]]
*Figure 5: (c) Activation function used by neural (d) Activation function used by neural partial order without LeakyReLU. partial order (equation 4). Figure 5: NST activation visualizations*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/005_Table_1.jpg]]
*Table 1: DAG embedding results. Embedding dimension D = T = 2, 4, 10*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/006_Table_2.jpg]]
*Table 2: Embedding results for real-world web page hyperlink and gene regulatory networks*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/014_Table.jpg]]

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/015_Table_3.jpg]]
*Table 3: Tree Embedding distortion leveraging Euclidean, Hyperbolic, Neural Snowflake and Neural (Quasi-)metric spaces*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/017_Table_4.jpg]]
*Table 4: Embedding results for arxiv citation network*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/018_Table_5.jpg]]
*Table 5: Statistics of WebKB datasets*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/019_Table_6.jpg]]
*Table 6: Statistics of Dream5 datasets*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/020_Table_7.jpg]]
*Table 7: Statistics of Ogbn-arxiv dataset*

![[assets/figures/papers/paper_list_l52_https_arxiv_org_abs_2408_13885/figures/021_Table_8.jpg]]
*Table 8: Embedding results for arxiv citation network*



## 定位与知识库关联

### 1. 与固定时空几何基线的对比

神经时空（NST）最直接的对比对象是使用固定几何度量的时空嵌入方法，主要包括**Minkowski空间嵌入**和**De Sitter空间嵌入**。这些基线共享相同的特征编码器（MLP），仅几何度量部分保持固定，保证了比较的公平性（见 Appendix D.5）。

两者的核心差异体现在两个可学习槽位上：

| 组件 | 固定几何基线 | 神经时空（NST） |
|------|-------------|----------------|
| **空间距离度量** | 固定的Minkowski或De Sitter度量（不可学习） | 可学习的神经准度量（neural quasi‑metric），由式(3)定义的多层带权迭代变换参数化 |
| **因果顺序建模** | 基于单一时间维度的固定洛伦兹因果结构 | 可学习的神经偏序（neural partial order），支持多个时间维度，由式(4)(5)定义 |

**性能差异的因果机制**：固定几何的瓶颈在于其度量函数形式预设，无法根据具体DAG的局部和全局结构自适应调整。例如，Minkowski空间的距离函数是全局线性的，而真实DAG的图测地线距离往往呈现高度非欧几里得特性。NST通过可训练的激活参数 $s, l$（式(2)）分别控制小尺度和大尺度距离的扩张/收缩，使模型能灵活适配从树状到网格状的多样图结构。

**实验证据**（Table 10, Table 9）：
- 在Cornell (WebKB) dim=2上，NST的最大失真为1.31，Minkowski基线为9.43，**降低86%**。
- 在合成DAG (dim=2, metric 1)上，NST的平均失真为 $1.13 \pm 0.37$，Minkowski为 $2.86 \pm 5.22$。
- 方向性指标上，NST（0.89）与Minkowski（0.90）、De Sitter（0.90）相当，表明可学习几何在保持因果一致性方面不牺牲性能。

### 2. 与神经雪花（Neural Snowflake）的关系

NST的空间准度量组件直接继承并扩展了神经雪花（Neural Snowflake）的迭代表示框架。神经雪花通过可学习的逐元素激活和正权矩阵构造度量嵌入，NST在此基础上：
- 引入了**非对称的准度量结构**（放弃对称性要求），更贴合有向图的边权重方向性；
- 将空间嵌入与时间偏序嵌入**联合优化**，形成乘积流形结构。

消融实验（Table 3, Tree Embedding）显示，神经准度量（NQM）在树嵌入任务上比神经雪花**收敛更快且失真更低**，验证了准度量松弛对图结构适配的增益。

### 3. 理论基础的谱系定位

NST的理论根基可追溯至以下方向：
- **粗几何与双曲嵌入**：NST的空间组件借鉴了大规模和渐近嵌入方法，特别是Gromov双曲空间的嵌入理论。
- **序嵌入与因果推理**：时间偏序组件继承了因果集理论（causal set theory）中多时间维度的偏序编码思想，但将其实现为可微的神经网络。
- **通用嵌入定理**（Theorem 1）：为NST提供了理论完备性保证——任意 $k$ 点DAG可嵌入神经时空，失真上界为 $O(\log(k)^5)$，且精确保留因果结构。该定理将NST定位为**首个具备通用嵌入保证的可学习时空几何框架**。

### 4. 适用边界与局限

**适用场景**：
- 有向无环图（DAG）的连续表示学习，包括网页超链接网络、基因调控网络、引文网络等。
- 需要同时保持图距离和因果方向的下游任务（如节点分类，Table 11显示NST特征可提升异配图分类精度）。

**明确局限**：
1. **仅支持DAG**：当前框架对包含有向环的一般有向图缺乏直接支持，无法处理循环因果结构。
2. **局部优化瓶颈**：训练仅优化一跳邻域的距离和因果性（式 $\mathcal{L}_{uv}^{D}$ 和 $\mathcal{L}_{uv}^{C}$），不显式保证全局测地线距离的精确重现。这在长程依赖图上可能导致累积失真。
3. **空间退化为伪度量**：当时间维度 $T>0$ 时，空间分量不满足点分离性（即 $\mathcal{D}(x,y)=0$ 不能推出 $x=y$），可能影响部分应用中距离的严格解释。
4. **规模未验证**：论文未在大规模图（百万节点级）上进行实验，参数效率（$O(k^2)$）和优化稳定性有待进一步检验。

### 5. 开放问题

1. **向含环图的扩展**：能否将神经时空框架推广至任意有向图（包括含环图），例如通过引入循环一致的时间维度编码？
2. **全局优化策略**：如何在大图场景下实现高效的全局嵌入优化，避免仅依赖局部邻域导致的失真累积？
3. **下游任务泛化**：除节点分类外，神经时空特征能否用于链接预测、因果推断、反事实推理等更多下游任务？
4. **时间维度压缩**：能否通过更精巧的偏序编码（如基于序维度的自适应分配）实现 $T=1$ 时仍能处理复杂反链结构，从而降低嵌入总维度？



## 原文 PDF

![[paperPDFs/ICLR_2025/Neural_Spacetimes_for_DAG_Representation_Learning.pdf]]
