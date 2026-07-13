---
title: "Directed Graph Generation with Heat Kernels"
type: paper
paper_level: A
venue: TMLR
year: 2025
pdf_ref: paperPDFs/TMLR_2025/Directed_Graph_Generation_with_Heat_Kernels.pdf
project_link: null
code_link: null
aliases:
- DDGHKM
- DGGHK
tags:
- TMLR_2025
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "设计了一个不依赖神经网络的热扩散编码器，该编码器利用有向图随机游走拉普拉斯矩阵的闭式解，通过非齐次热方程引入均匀噪声，将全局拓扑信息编码到节点表示中，并采用去噪解码器重建图结构。"
primary_logic: "将有向图的热扩散核推广到非对称情形，通过再生核Banach空间（RKBS）建立几何解释，并证明通过设计热源项可以使扩散后的节点表示趋向最大熵分布，同时保留足够的信息用于重建。"
claims:
- "现有一步式方法无法处理有向图，因为Spectre依赖对称拉普拉斯特征向量，DiGress使用的谱特征也要求对称性。"
- "所提出的热扩散编码器不需要学习参数，通过闭式解直接计算噪声节点表示。"
- "在合成数据集上，DGDK生成的图在度分布、聚类系数和谱特征的MMD指标上均接近零，显著优于SwinGNN和GRAN。"
- "学习到的节点表示矩阵N的奇异向量与热核矩阵e^{tΔ}的奇异向量高度相关，说明模型能有效保留图的全局谱信息。"
---

# Directed Graph Generation with Heat Kernels

> [!tip] 核心洞察
> 将有向图的热扩散核推广到非对称情形，通过再生核Banach空间（RKBS）建立几何解释，并证明通过设计热源项可以使扩散后的节点表示趋向最大熵分布，同时保留足够的信息用于重建。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于热核的有向图生成 |
| 英文题名 | Directed Graph Generation with Heat Kernels |
| 会议/期刊 | TMLR 2025 |
| Links | [paper](https://openreview.net/forum?id=60Gi1w6hte) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | DGDK (Directed Graph Heat Kernel method) |
| Dataset | Erdős-Rényi (p=0.4, n∈[180, 200]), Stochastic Block Model (5 blocks) |

> [!tip] 效果简介
> - Erdős-Rényi (p=0.4, n∈[180,200]) 上，MMD Degree (σ²=100) 为 0.00073 ± 0.00002，对比 SwinGNN: 0.00091 ± 0.00084，变化 -0.00018 (lower is better)。
> - Erdős-Rényi (p=0.4, n∈[180,200]) 上，MMD Clustering (σ²=100) 为 0.0068 ± 0.0005，对比 SwinGNN: 0.0091 ± 0.0012，变化 -0.0023。
> - Erdős-Rényi (p=0.4, n∈[180,200]) 上，MMD Spectrum (σ²=100) 为 0.00085 ± 0.0001，对比 SwinGNN: 0.00110 ± 0.0008，变化 -0.00025。

## 概要

有向图（digraph）广泛存在于现实世界的复杂系统中，但现有的一步式图生成方法——如 **Spectre** 和 **DiGress**——均无法直接处理有向图。其根本瓶颈在于，这些方法依赖对称拉普拉斯矩阵的谱性质，而有向图的拉普拉斯矩阵是非对称的，导致特征分解与谱特征构造失效。

针对这一问题，本文提出 **DGDK（Directed Graph Heat Kernel method，有向图热核方法）**，一种基于去噪自编码器的一步生成框架。其核心创新在于设计了一个**不依赖可学习神经网络的热扩散编码器**：该编码器利用有向图随机游走拉普拉斯矩阵上的非齐次热方程闭式解，通过精心设计的热源项 $Q(t)$ 将均匀噪声注入节点表示，使输出趋向最大熵分布（均匀噪声矩阵 $\mathbf{M} = \frac{1}{n}\mathbf{1}\mathbf{1}^\top$），同时保留足够的全局拓扑信息供解码器重建图结构。解码器采用多任务学习范式，同时重建去噪后的节点表示与邻接矩阵。

从理论角度，DGDK 将有向图的热扩散核推广到非对称情形，并通过再生核 Banach 空间（RKBS）为扩散过程建立了几何解释。

在合成数据集上的实验表明，DGDK 在度分布、聚类系数和谱特征的 MMD 指标上均接近零，显著优于基线方法 **SwinGNN** 和 **GRAN**（Liao et al., NeurIPS 2019）。消融实验进一步揭示了噪声扩散率 $\alpha$ 对生成图结构多样性的调控作用，以及多任务学习中节点重建正则化项对训练收敛的必要性。

**方法定位**：DGDK 属于基于谱扩散的一步式有向图生成方法，其编码器无需训练，解码器采用 Set Transformer 架构实现置换不变性。该方法在方法谱系中填补了扩散类生成模型无法处理有向图的空白。

**主要局限**：当前验证仅限于合成数据集（Erdős-Rényi, Stochastic Block Model），缺乏真实世界有向图（如因果网络、引用网络）的评估；对超参数 $T$ 和 $\alpha$ 较为敏感；大规模图（>200 节点）依赖截断 SVD 低秩近似，扩展性有待进一步验证。



图生成模型旨在从一组观测图中学习其底层分布，并从中采样生成具有相似性质的新图。近年来，基于去噪扩散的生成框架在图生成领域取得了显著进展，代表工作包括 **Spectre** 和 **DiGress** 等。然而，这些方法存在一个根本性局限：它们**无法直接应用于有向图**。Spectre 依赖对称拉普拉斯矩阵的特征向量性质来编码图结构，而这些性质仅在无向图情形下成立；DiGress 同样需要基于对称内积的谱特征，该特征仅对无向图有效。这一瓶颈使得现有的一步式生成方法在有向图场景下完全失效。

有向图广泛存在于现实世界中，如社交网络中的关注关系、引文网络中的引用方向、以及因果推理中的因果图等。然而，专门针对有向图的生成模型相对匮乏。现有方法如 **SwinGNN** 虽可处理有向图，但其基于消息传递的局部邻域编码难以捕获图的全局拓扑特性（如社团结构、谱分布等），导致生成质量在全局指标上表现不佳。另一基线 **GRAN**（Liao et al., NeurIPS 2019）原为无向图设计，虽可适配有向图，但同样缺乏对全局结构的显式建模。

上述缺口揭示了一个核心挑战：**如何在非对称拉普拉斯矩阵的条件下，将图的全局拓扑信息有效编码到节点表示中，并实现高质量的一步式生成？** 本文的动机正是填补这一空白——设计一种能够利用有向图拉普拉斯动力学、无需学习神经网络编码器即可将全局结构信息注入节点表示，并通过去噪解码实现一步生成的新框架。



## 核心方法与创新机理

### 瓶颈突破：从无向到有向的跨越

现有的一步式图生成方法——无论是基于谱分解的 **Spectre**，还是基于扩散的 **DiGress**——均无法直接处理有向图。其根本原因在于这些方法**依赖于对称拉普拉斯矩阵的性质**：Spectre 利用无向图拉普拉斯矩阵的特征向量进行谱分解，而 DiGress 所使用的谱特征（源自 Beaini et al., 2021）也要求拉普拉斯矩阵是对称的。有向图的拉普拉斯矩阵天然是非对称的，导致这些方法在理论层面无法泛化。

DGDK 的核心突破在于**将热扩散核推广到非对称情形**，使得有向图的全局拓扑信息可以通过随机游走拉普拉斯矩阵的矩阵指数 $e^{t\Delta}$ 进行编码，从而在不依赖对称性假设的前提下实现一步式生成。

### 关键创新：三个 Changed Slots

相较于现有方法，DGDK 在三个关键设计点上做出了根本性改变：

**1. 加噪过程：从高斯噪声到非齐次热扩散**

现有方法通常采用标准高斯噪声或简单的边缘扰动来破坏图结构。DGDK 则设计了一个**基于有向图拉普拉斯热方程的非齐次扩散过程**。具体而言，编码器通过精心设计的热源项 $Q(s)$，使得节点表示在扩散时间 $T$ 后的输出 $\mathbf{X}(T)$ 趋于列随机均匀矩阵 $\mathbf{M} = \frac{1}{n}\mathbf{11}^\top$，该矩阵对应最大熵分布。这一设计的数学保证来自 Proposition 1 中给出的闭式解：

$$\mathbf{X}(t) = e^{t\Delta} \mathbf{X}(0) + \int_{0}^{t} e^{(t-s)\Delta} \mathbf{Q}(s) \mathrm{d}s$$

当 $\beta=0$ 时，该解简化为扩散表示与均匀噪声的凸组合：

$$\mathbf{X}(T) = e^{-\alpha T} \mathbf{Z}(T) + (1 - e^{-\alpha T}) \mathbf{M}$$

其中 $\alpha$ 控制噪声注入速率，$T$ 控制扩散深度。

**2. 图结构编码：从局部邻域到全局热核**

现有方法通常仅依赖节点初始特征或局部邻域的消息传递来编码图结构。DGDK 则通过随机游走拉普拉斯矩阵的矩阵指数 $e^{t\Delta}$ 将**全局拓扑信息直接编码到节点表示中**。这一编码器不需要学习任何神经网络参数，完全通过闭式解计算，从而避免了训练编码器带来的额外复杂度和不稳定性。实验证据表明（Figure 3），学习到的节点表示矩阵 $\mathbf{N}$ 的奇异向量与热核矩阵 $e^{t\Delta}$ 的奇异向量高度相关，验证了模型能够有效保留图的全局谱信息。

**3. 噪声目标分布：从无约束到最大熵**

现有方法通常缺乏明确的噪声目标分布，或简单地假设标准正态分布。DGDK 则明确将噪声目标设定为**列随机均匀矩阵 $\mathbf{M}$**，该分布在给定约束下达到最大熵。这一设计使得编码器的输出在 $T \to \infty$ 时趋向于信息量最小的状态，同时保留了足够的拓扑信息供解码器重建——实现了“最大熵加噪”与“信息保留”之间的精确平衡。

### 架构层面的创新

在整体架构上，DGDK 采用**去噪自编码器范式**，但与传统自编码器不同，其编码器是参数无关的闭式解，仅解码器需要学习。解码器分为两个组件：节点解码器 $\varphi$（基于 Set Transformer 的置换不变网络）负责重建去噪后的节点表示 $\mathbf{Z}(t)$；边解码器 $\psi$ 负责预测邻接矩阵中的边存在与否。训练时采用多任务学习，总损失为边重建交叉熵损失与节点重建 Frobenius 损失之和：

$$\sum_{i=1}^m \mathcal{L}_{\text{edge}}(i) + \gamma \mathcal{L}_{\text{node}}(i)$$

其中 $\gamma > 0$ 是损失收敛的必要条件——消融实验表明，节点解码任务对边解码器的学习起到了关键的辅助作用。

### 创新边界与待验证点

需要注意的是，DGDK 的创新目前仅在合成数据集（Erdős-Rényi 和随机块模型）上得到验证，其在真实世界有向图（如因果网络、引用网络）上的有效性仍需进一步检验。此外，该方法对超参数 $T$ 和 $\alpha$ 较为敏感，需通过交叉验证选择，缺乏自适应机制——这在实际部署中可能构成限制。对于超过 200 节点的大规模图，模型依赖截断 SVD 低秩近似，其近似误差对生成质量的影响尚未充分量化。



DGDK 的整体框架可以理解为一个**去噪自编码器**，其核心思想是将有向图的全局拓扑信息编码到节点表示中，再通过解码器重建图结构。整个流程分为编码和解码两个阶段，如图 Figure 1 所示。

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_60Gi1w6hte/figures/001_Figure_1.jpg]]
*Figure 1: Our framework can be viewed as a denoising autoencoder. Our heat diffusion encoder maps a perturbed adjacency matrix $\tilde { \mathbf { A } } \in \{$ 0 , 1 $\} ^ { n \times n }$ to a noisy node representation matrix $\tilde { \mathbf { X } }$ ( T ) $\in$ [ 0 , 1 ]$^ { n \times d }$ that is given as input of a decoder that reconstructs the edges. ( n = 5 , d = 7 in the figure)

### 编码阶段：热扩散编码器

编码器接收两个输入：一个经过扰动的邻接矩阵 $\tilde{\mathbf{A}} \in \{0,1\}^{n \times n}$ 和一个初始节点表示矩阵 $\mathbf{X}(0)$。编码器本身**不需要学习任何神经网络参数**，而是利用有向图随机游走拉普拉斯矩阵 $\Delta$ 的热方程闭式解，直接计算在扩散时间 $T$ 时刻的含噪声节点表示 $\tilde{\mathbf{X}}(T)$。

具体而言，编码器通过精心设计的热源项 $\mathbf{Q}(s)$，使得节点表示沿非齐次热方程演化：
$$\frac{\mathrm{d}}{\mathrm{d}t} \mathbf{X}(t) = \Delta \mathbf{X}(t) + \mathbf{Q}(t)$$

其闭式解为：
$$\mathbf{X}(t) = e^{t\Delta} \mathbf{X}(0) + \int_{0}^{t} e^{(t-s)\Delta} \mathbf{Q}(s) \mathrm{d}s$$

热源项 $\mathbf{Q}(s)$ 的设计目标是使 $\mathbf{X}(T)$ 在 $T \to +\infty$ 时收敛到一个列随机的均匀噪声矩阵 $\mathbf{M} = \frac{1}{n}\mathbf{1}\mathbf{1}^\top$，该矩阵对应最大熵分布。最终，含噪声的节点表示可写为扩散表示与均匀噪声的凸组合：
$$\tilde{\mathbf{X}}(T) = e^{-\alpha T} e^{T\tilde{\Delta}} \mathbf{X}(0) + (1 - e^{-\alpha T}) \mathbf{M}$$

其中 $\alpha$ 为噪声扩散率，控制噪声注入的速度；$\tilde{\Delta}$ 是由扰动邻接矩阵 $\tilde{\mathbf{A}}$ 计算的拉普拉斯矩阵。噪声比率 $1 - e^{-\alpha T}$ 随 $T$ 和 $\alpha$ 的变化关系见 Figure 2。

### 解码阶段：去噪解码器

解码器由两个并行的神经网络组成，均以 $\tilde{\mathbf{X}}(T)$ 作为输入：

- **节点解码器 $\varphi$**：采用基于注意力机制的置换不变网络 **Set Transformer** 架构，其任务是预测去噪后的节点表示 $\mathbf{Z}(t) = e^{t\Delta} \mathbf{X}(0)$。该模块的损失函数为预测值与真实值之间的 Frobenius 范数：
  $$\mathcal{L}_{\text{node}}(i) = \| \varphi(\tilde{\mathbf{X}}^i(T)) - \mathbf{T}^i \|_F^2$$

- **边解码器 $\psi$**：同样以 $\tilde{\mathbf{X}}(T)$ 为输入，直接预测原始邻接矩阵中每条边的存在与否，其损失为边重建的交叉熵损失 $\mathcal{L}_{\text{edge}}(i)$。

### 联合训练与数据增强

整个模型通过多任务学习联合优化，总损失函数为：
$$\sum_{i=1}^m \mathcal{L}_{\text{edge}}(i) + \gamma \mathcal{L}_{\text{node}}(i)$$
其中 $\gamma > 0$ 为正则化参数。消融实验表明，$\gamma > 0$ 是损失收敛的必要条件，节点解码任务对边解码器的学习具有辅助作用。

为提高模型鲁棒性，训练过程中引入了两种数据增强策略：
- **边缘扰动**：以概率 $\rho \approx 1/n_i$ 随机翻转邻接矩阵中的边，生成扰动矩阵 $\tilde{\mathbf{A}}^i = \mathbf{A}^i \oplus \mathbf{C}$。
- **同构图排列增强**：对训练邻接矩阵施加随机排列变换，促进模型的置换不变性。实验表明，该增强对训练损失的影响很小，模型对此类变换具有天然鲁棒性。

### 推理生成

在推理阶段（Algorithm 1），模型从均匀噪声分布 $\mathbf{M}$ 出发，结合随机生成的拉普拉斯矩阵，通过训练好的解码器直接生成新的有向图，实现一步式生成。对于类条件生成任务，可将类别标签的 one-hot 矩阵 $\mathbf{Y}^i$ 与 $\tilde{\mathbf{X}}^i(T)$ 拼接后输入解码器。



### 3.1 热扩散编码器 (Heat Diffusion Encoder)

热扩散编码器是整个框架的核心创新，它是一个**非参数化**的加噪模块，不需要学习任何神经网络参数。其设计目标是将输入的有向图结构信息编码到节点表示矩阵中，同时注入可控的均匀噪声，使得编码器输出在极限情况下趋近于最大熵分布。

**输入与输出**：
- **输入**：扰动后的邻接矩阵 $\tilde{\mathbf{A}}^i \in \{0,1\}^{n_i \times n_i}$ 和初始节点表示矩阵 $\mathbf{N} = \mathbf{X}(0)$
- **输出**：含噪声的节点表示矩阵 $\tilde{\mathbf{X}}^i(T) \in [0,1]^{n_i \times d}$

**核心机制**：编码器基于有向图的**随机游走拉普拉斯矩阵** $\Delta$ 构建非齐次热方程：

$$\forall t \geq 0, \quad \frac{\mathrm{d}}{\mathrm{d}t} \mathbf{X}(t) = \Delta \mathbf{X}(t) + \mathbf{Q}(t)$$

其中 $\mathbf{Q}(t)$ 是精心设计的**热源项**，其作用是驱动节点表示向均匀噪声矩阵 $\mathbf{M} = \frac{1}{n}\mathbf{1}\mathbf{1}^\top$ 演化。该方程的闭式解为：

$$\mathbf{X}(t) = e^{t\Delta} \mathbf{X}(0) + \int_{0}^{t} e^{(t-s)\Delta} \mathbf{Q}(s) \mathrm{d}s$$

第一项 $e^{t\Delta} \mathbf{X}(0)$ 是齐次解，保留了图的全局拓扑信息；第二项是强制项，引入噪声。

**热源项设计** (Proposition 1)：为使 $\mathbf{X}(T)$ 在 $T \to +\infty$ 时收敛到 $\mathbf{M}$，作者设计了如下热源项：

$$\mathbf{Q}(s) := \alpha e^{-\alpha s} e^{s\Delta} \left( \mathbf{R} - e^{\beta\Delta} \mathbf{X}(0) \right)$$

对应的强制项闭式解为：

$$\mathbf{F}(t) = (1 - e^{-\alpha t}) e^{t\Delta} \left( \mathbf{R} - e^{\beta\Delta} \mathbf{X}(0) \right)$$

其中 $\alpha > 0$ 控制噪声注入速率，$\beta \geq 0$ 控制初始信息保留程度，$\mathbf{R}$ 是参考矩阵。当 $\beta = 0$ 时，编码器输出简化为一个**凸组合**形式：

$$\tilde{\mathbf{X}}(T) = e^{-\alpha T} e^{T\Delta} \mathbf{X}(0) + (1 - e^{-\alpha T}) \mathbf{M}$$

**关键性质**：
- 噪声比率 $1 - e^{-\alpha T}$ 由超参数 $\alpha$ 和 $T$ 联合控制（见 Figure 2）
- 当 $T \to \infty$ 时，$\tilde{\mathbf{X}}(T) \to \mathbf{M}$，实现最大熵目标
- 矩阵指数 $e^{T\Delta}$ 通过截断SVD低秩近似计算，适用于较大规模图

### 3.2 去噪解码器 (Denoising Decoder)

解码器采用**多任务学习**框架，同时训练两个神经网络：

**节点解码器 $\varphi$**：以含噪表示 $\tilde{\mathbf{X}}^i(T)$ 为输入，重建去噪后的节点表示 $\mathbf{Z}^i(t) = e^{t\Delta^i} \mathbf{N}$。采用 **Set Transformer** 架构保证置换不变性。损失函数为 Frobenius 范数：

$$\mathcal{L}_{\mathrm{node}}(i) := \| \varphi(\tilde{\mathbf{X}}^i(T)) - \mathbf{T}^i \|_F^2$$

其中 $\mathbf{T}^i$ 是从 $\mathbf{Z}^i(t)$ 采样的目标表示。

**边解码器 $\psi$**：以相同的含噪表示 $\tilde{\mathbf{X}}^i(T)$ 为输入，预测原始邻接矩阵 $\mathbf{A}^i$。采用二元交叉熵损失：

$$\mathcal{L}_{\mathrm{edge}}(i) := \mathrm{BCE}(\psi(\tilde{\mathbf{X}}^i(T)), \mathbf{A}^i)$$

**联合训练损失**：

$$\sum_{i=1}^m \mathcal{L}_{\mathrm{edge}}(i) + \gamma \mathcal{L}_{\mathrm{node}}(i)$$

其中 $\gamma > 0$ 是正则化参数。消融实验表明，$\gamma > 0$ 是损失收敛的**必要条件**，节点解码任务为边解码器提供了有效的辅助监督信号。

### 3.3 数据增强策略

为提高模型鲁棒性，训练时采用两种数据增强：

1. **边扰动**：对邻接矩阵 $\mathbf{A}^i$ 以概率 $\rho \approx 1/n_i$ 随机翻转边，生成扰动矩阵 $\tilde{\mathbf{A}}^i = \mathbf{A}^i \oplus \mathbf{C}$
2. **同构排列增强**：对训练图施加随机节点排列，使模型学习置换不变性。消融实验（Figure 5）表明，该增强对训练损失影响很小，模型天然对此类变换具有鲁棒性

### 3.4 推理过程

推理时（Algorithm 1），从均匀噪声矩阵 $\mathbf{M}$ 出发，利用训练好的解码器 $\varphi$ 和 $\psi$ 迭代生成图结构，无需访问真实拉普拉斯矩阵。



## 实验与关键发现

### 主要结果

DGDK 在两个合成数据集上与两个有向图生成基线——基于注意力机制的 **SwinGNN** 和将无向图生成模型 **GRAN**（Liao et al., NeurIPS 2019）适配到有向图的版本——进行了比较。所有实验均在 Erdős-Rényi (ER) 和随机块模型 (SBM) 上展开，采用平方 MMD 距离作为评价指标，度量生成图与测试图在度分布、聚类系数和谱特征三个维度上的分布差异。

在 ER 分布（$p=0.4$，节点数 $n \in [180, 200]$）上，DGDK 在所有指标上均优于 SwinGNN 和 GRAN（Table 2）。具体而言，DGDK 的度分布 MMD 为 $0.00073 \pm 0.00002$，而 SwinGNN 为 $0.00091 \pm 0.00084$；聚类系数 MMD 为 $0.0068 \pm 0.0005$，相比 SwinGNN 的 $0.0091 \pm 0.0012$ 降低了约 25%；谱特征 MMD 为 $0.00085 \pm 0.0001$，低于 SwinGNN 的 $0.00110 \pm 0.0008$。GRAN 在所有指标上均显著劣于 DGDK，其谱特征 MMD 高达 $0.0135 \pm 0.0046$，表明其无法有效捕捉有向图的全局拓扑结构。

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_60Gi1w6hte/figures/006_Table_2.jpg]]
*Table 2: Squared MMD distances over 5 random initializations (average ± standard deviation) for the Erdős-Rényi distribution ( p = 0 . 4 )*

在 SBM（5 个块）上，DGDK 的优势更为突出（Table 3）。其聚类系数 MMD 仅为 $0.0039 \pm 0.0023$，而 SwinGNN 为 $0.0245 \pm 0.0094$，差距达 6 倍以上；谱特征 MMD 为 $0.00038 \pm 0.0003$，SwinGNN 为 $0.00831 \pm 0.0103$，差距超过 20 倍。这表明热扩散编码器通过随机游走拉普拉斯矩阵的矩阵指数 $e^{t\Delta}$ 成功将图的全局谱信息编码到了节点表示中，使得去噪解码器能够准确重建社区结构。

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_60Gi1w6hte/figures/007_Table_3.jpg]]
*Table 3: Squared MMD distances over 5 random initializations (average ± standard deviation) for the stochastic block model (5 blocks)*

**证据强度**：Table 2 和 Table 3 的结果来自 5 次随机初始化的均值和标准差，置信度 0.95。需注意，所有实验均在合成数据集上进行，缺乏真实世界有向图（如引文网络、因果网络）的验证。

### 消融实验

#### 噪声扩散率 α 的影响

噪声扩散率 $\alpha$ 是控制生成图结构多样性的关键超参数。通过调节 $\alpha$，可以控制节点表示 $\mathbf{X}(T) = e^{-\alpha T} \mathbf{Z}(T) + (1 - e^{-\alpha T}) \mathbf{M}$ 中均匀噪声 $\mathbf{M}$ 的比例（Figure 2）。在多峰分布数据集上的消融实验（Table 4）揭示了以下模式：

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_60Gi1w6hte/figures/010_Table_4.jpg]]
*Table 4: Squared MMD distances for the experiments on the multimodal dataset in Section G.4 for different values of α*

- **$\alpha = 0$**：噪声项完全消失，$\mathbf{X}(T) = \mathbf{Z}(T)$，模型退化为确定性自编码器。生成的图趋向于单一聚类结构（Figure 6），无法捕捉训练数据的多峰分布。
- **$\alpha = 1.0$**：噪声比率适中，模型生成的图在聚类结构上与训练分布高度一致（Figure 7），MMD 指标最优。
- **$\alpha = 2.3$**：噪声比率过高，模型开始生成包含孤立节点的退化图（Figure 8），生成质量显著下降。

这一消融验证了热源项设计 $\mathbf{Q}(s) := \alpha e^{-\alpha s} e^{s\Delta} (\mathbf{R} - e^{\beta\Delta} \mathbf{X}(0))$ 的有效性——通过调节 $\alpha$，可以在信息保留和噪声注入之间取得平衡，使扩散后的表示趋向最大熵分布，同时保留足够的拓扑信息用于重建。

**证据强度**：Figure 6-8 和 Table 4 提供了可视化样本和定量 MMD 指标，置信度 0.95。但 $\alpha$ 和扩散时间 $T$ 需通过交叉验证手动选择，缺乏自适应机制。

#### 节点解码器正则化的必要性

训练损失函数 $\sum_{i=1}^m \mathcal{L}_{\mathrm{edge}}(i) + \gamma \mathcal{L}_{\mathrm{node}}(i)$ 中，正则化参数 $\gamma > 0$ 是损失收敛的必要条件。消融实验表明，当 $\gamma = 0$（即仅使用边重建损失）时，训练损失无法有效下降。这说明节点解码任务——预测去噪后的节点表示 $\mathbf{Z}(t) = e^{t\Delta} \mathbf{X}(0)$——为边解码器提供了关键的辅助监督信号，帮助模型学习图的全局拓扑结构。

**证据强度**：该结论来自原文对训练动态的分析，置信度 0.9。原文未提供 $\gamma$ 取不同值时的定量 MMD 对比表，具体敏感度需进一步验证。

#### 数据增强的影响

- **边缘扰动**：以概率 $\rho \approx 1/n_i$ 随机翻转邻接矩阵中的边，轻微提升了生成性能，但并非关键因素（置信度 0.85）。
- **同构图排列增强**：在训练时随机排列节点顺序，损失曲线与不使用该增强时几乎一致（Figure 5），表明 Set Transformer 架构天然具有排列不变性，模型对此类变换高度鲁棒（置信度 0.9）。

#### 谱信息保留验证

通过分析学习到的节点表示矩阵 $\mathbf{N}$ 与热核矩阵 $e^{t\Delta}$ 的奇异向量相关性，可以验证模型是否有效保留了图的全局谱信息。Figure 3 的热图显示，$e^{t\Delta^i} \mathbf{N}$ 的主导左奇异向量与 $e^{t\Delta^i}$ 的对应奇异向量高度相关。这解释了 DGDK 在谱特征 MMD 指标上大幅领先基线的原因——热扩散编码器通过闭式解将拉普拉斯谱信息直接注入节点表示，而不依赖神经网络学习近似。

**证据强度**：Figure 3 提供了可视化证据，置信度 0.9。

### 失败模式与局限性

1. **大规模图的可扩展性瓶颈**：对于节点数超过 200 的图，矩阵指数 $e^{t\Delta}$ 的精确计算代价过高。原文采用截断 SVD 低秩近似，但近似误差对生成质量的影响缺乏量化分析（Table 2-3 的实验均在 $n \leq 200$ 范围内）。
2. **超参数敏感性**：扩散时间 $T$ 和噪声率 $\alpha$ 需通过交叉验证针对每个任务单独选择，缺乏自适应选择机制。Figure 2 展示了噪声比率随 $T$ 和 $\alpha$ 的变化曲线，但未给出自动调参方案。
3. **真实场景验证缺失**：所有实验均限于 ER 和 SBM 合成数据集，未在真实有向图（如因果发现网络、社交网络、引文网络）上评估。模型对复杂度分布、异配性等真实图特性的泛化能力未知。
4. **基线比较不充分**：仅与 SwinGNN 和 GRAN 两个基线比较，未与近期一步式图生成方法（如 Spectre、DiGress）进行直接消融，无法量化热扩散编码器相对于其他全局编码方案的增益。

### 补充图表

![[assets/figures/papers/paper_list_l53_https_openreview_net_forum_id_60Gi1w6hte/figures/004_Table_1.jpg]]
*Table 1: Squared MMD distances*



## 定位与知识库关联

### 瓶颈与动机：一步式生成方法在有向图上的失效

现有的一步式图生成方法（one-shot generation）在无向图上取得了显著进展，但其核心设计依赖对称拉普拉斯矩阵的谱性质，无法直接迁移到有向图。具体而言：

- **Spectre** 依赖对称拉普拉斯矩阵的特征向量分解来编码图结构，而有向图的拉普拉斯矩阵是非对称的，因此 Spectre 无法泛化到有向图场景（见原文 Section 5 的解释）。
- **DiGress** 虽然基于扩散过程，但其使用的谱特征来自 Beaini et al. (2021)，这些特征依赖于对称内积，仅在无向图上有效。

这一瓶颈构成了本文的核心动机：设计一种不依赖对称性假设的全局拓扑编码机制，使一步式生成范式能够覆盖有向图。

### 方法定位：热扩散自编码器

本文提出的 **DGDK**（Directed Graph Heat Kernel method）在方法谱系上属于**去噪自编码器式生成模型**，其关键创新在于将热扩散方程引入编码器设计，形成“物理驱动编码 + 神经网络解码”的混合架构。

与典型基线方法的差异体现在三个关键设计槽位上：

| 设计槽位 | 基线方法 | DGDK 方案 |
|----------|----------|-----------|
| **加噪过程** | 标准高斯噪声或边缘随机扰动（如 GRAN, Liao et al., NeurIPS 2019） | 基于有向图随机游走拉普拉斯矩阵的非齐次热扩散过程，输出趋向均匀噪声矩阵 $\mathbf{M} = \frac{1}{n}\mathbf{1}\mathbf{1}^\top$ |
| **图结构编码** | 仅使用节点特征或局部邻域消息传递（如 SwinGNN） | 通过矩阵指数 $e^{t\Delta}$ 将全局拓扑信息编码到节点表示中，利用热方程的闭式解避免学习编码器参数 |
| **噪声目标分布** | 无明确目标或标准正态分布 | 列随机均匀矩阵，对应最大熵分布，确保加噪后的表示信息量可控 |

### 核心机制：非对称热核与再生核 Banach 空间

DGDK 的理论基础是将热扩散核推广到非对称情形。对于有向图的随机游走拉普拉斯矩阵 $\Delta$，热方程

$$\forall t \geq 0, \frac{\mathrm{d}}{\mathrm{d}t} \mathbf{X}(t) = \Delta \mathbf{X}(t) + \mathbf{Q}(t)$$

的闭式解为

$$\mathbf{X}(t) = e^{t\Delta} \mathbf{X}(0) + \int_{0}^{t} e^{(t-s)\Delta} \mathbf{Q}(s) \mathrm{d}s.$$

通过设计特定的热源项 $\mathbf{Q}(s)$（见 Proposition 1），编码器输出在 $T \to +\infty$ 时趋向均匀噪声矩阵 $\mathbf{M}$，而在有限时间 $T$ 处，节点表示为扩散表示与噪声的凸组合：

$$\mathbf{X}(T) = e^{-\alpha T} \mathbf{Z}(T) + (1 - e^{-\alpha T}) \mathbf{M}.$$

该设计在**再生核 Banach 空间**（RKBS）框架下具有几何解释，保证了扩散后的表示既保留足够信息用于重建，又逼近最大熵分布。

### 实验证据强度与适用边界

**证据强度**：
- 在合成数据集（Erdős-Rényi 和随机块模型）上，DGDK 在度分布、聚类系数和谱特征的 MMD 指标上均接近零，显著优于 SwinGNN 和 GRAN（Table 1-3，置信度 0.95）。
- 学习到的节点表示矩阵 $\mathbf{N}$ 的奇异向量与热核矩阵 $e^{t\Delta}$ 的奇异向量高度相关（Figure 3），验证了模型能有效保留图的全局谱信息（置信度 0.9）。
- 消融实验表明，正则化参数 $\gamma > 0$ 是损失收敛的必要条件，节点解码任务对边解码器学习起关键辅助作用（置信度 0.9）。

**适用边界与局限**：
1. **数据集局限**：所有实验均在合成数据集上进行，缺乏真实世界有向图（如因果网络、引用网络）的验证，泛化性存疑。
2. **基线覆盖不足**：仅与 SwinGNN 和 GRAN 两个基线比较，未直接与 Spectre 或 DiGress 进行消融对比，无法量化热扩散编码器相对于谱方法的增益。
3. **扩展性瓶颈**：对于节点数超过 200 的大图，模型依赖截断 SVD 低秩近似，近似误差对生成质量的影响缺乏量化分析，且扩展性未充分证明。
4. **超参数敏感性**：扩散时间 $T$ 和噪声率 $\alpha$ 需通过交叉验证选择，缺乏自适应机制。$\alpha=0$ 时生成单块图，$\alpha=2.3$ 时出现孤立节点（Figure 6-8），表明超参数选择对生成结果影响显著。

### 开放问题

1. **属性图推广**：当前方法仅处理拓扑结构，能否将热扩散编码器推广到节点和边带有额外特征的属性图？
2. **自适应超参数选择**：如何自动选择最优的扩散时间 $T$ 和噪声率 $\alpha$，避免依赖任务特定的交叉验证？
3. **真实场景验证**：在真实有向图生成任务（如因果发现、社交网络分析）上的性能如何？与专门针对有向图设计的生成模型相比有何优势？
4. **近似方案优化**：截断 SVD 带来的近似误差对生成质量的影响有多大？是否存在更高效的矩阵指数近似方案以支持大规模图？
5. **与扩散生成模型的融合**：DGDK 的物理驱动编码器能否与 DiGress 等扩散生成模型的迭代去噪范式结合，形成“热扩散编码 + 扩散去噪”的混合生成框架？



## 原文 PDF

![[paperPDFs/TMLR_2025/Directed_Graph_Generation_with_Heat_Kernels.pdf]]
