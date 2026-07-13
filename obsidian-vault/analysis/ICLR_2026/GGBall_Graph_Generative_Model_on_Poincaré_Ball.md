---
title: "GGBall: Graph Generative Model on Poincaré Ball"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: "paperPDFs/ICLR_2026/GGBall_Graph_Generative_Model_on_Poincaré_Ball.pdf"
project_link: null
code_link: https://github.com/AI4Science-WestlakeU/GGBall
openreview_forum_id: 4zRRnDscqn
aliases:
- GHVQAPFM
- GGBall
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将整个生成管线从欧氏空间转向庞加莱球双曲几何，采用统一节点潜在表示替代显式边建模。"
primary_logic: "双曲几何因其指数增长的体积天然保持层次结构，将整图编码为节点双曲嵌入后，边连通性可由节点间的几何距离自然涌现，从而实现结构感知的生成。"
claims:
- "GGBall在层次图数据集上平均生成误差最高降低18%。"
- "双曲VQVAE在树结构数据集上重建近乎完美，度MMD仅为7.9×10⁻⁴。"
- "欧氏VQVAE在Comm20上的轨道MMD为0.7555，双曲HVQVAE仅为0.0005，差距超过1500倍。"
- "在QM9上，HVQVAE+Flow实现93.77%的新颖度与85.34的V.U.N.分数，均为最优。"
---

# GGBall: Graph Generative Model on Poincaré Ball

> [!tip] 核心洞察
> 双曲几何因其指数增长的体积天然保持层次结构，将整图编码为节点双曲嵌入后，边连通性可由节点间的几何距离自然涌现，从而实现结构感知的生成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | GGBall: 基于庞加莱球的图生成模型 |
| 英文题名 | GGBall: Graph Generative Model on Poincaré Ball |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=4zRRnDscqn) · [GitHub](https://github.com/AI4Science-WestlakeU/GGBall) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | GGBall (Hyperbolic Vector-Quantized Autoencoder + Poincaré Flow Matching) |
| Dataset | Community-small, Ego-small, QM9 |

> [!tip] 效果简介
> - Community-small 上，平均MMD（度、聚类系数、轨道） 为 0.0215，对比 0.0240 (HGDM)，变化 -0.0025。
> - Ego-small 上，平均MMD 为 0.0112，对比 0.0137 (HGDM)，变化 -0.0025。
> - QM9 上，V.U.N.分数 为 85.34%，对比 81.31% (GDSS)，变化 +4.03%。

## 概要

图生成模型旨在学习图数据的分布并从中采样，但现有方法大多在欧氏空间中操作，难以捕捉真实世界图中普遍存在的指数级层次复杂性和幂律度分布。欧氏潜在空间的体积仅随半径多项式增长，无法自然容纳树状或层次化拓扑的长程依赖，导致生成图的结构保真度严重失真。

针对这一瓶颈，**GGBall** 提出将整个生成管线从欧氏空间转向庞加莱球双曲几何。其核心创新在于采用**统一的节点潜在表示**——整张图被映射为一组双曲嵌入，边连通性不再显式建模，而是作为节点间几何距离的自然涌现。双曲空间因其指数增长的体积天然保持层次结构，使得这一表示方式具有结构感知能力。

方法层面，GGBall 结合了**双曲向量量化自编码器（HVQVAE）**与**黎曼流匹配先验**，形成“编码-量化-生成”三阶段管线：图先经 Poincaré GNN 和测地线注意力 Transformer 编码为节点双曲嵌入，再通过 Poincaré 码本离散化以增强稳定性和结构性，最后利用双曲空间中的流匹配学习从基础分布到目标潜在分布的确定性映射，支持一步生成。

实验表明，GGBall 在层次图数据集上将平均生成误差最高降低 **18%**，在 QM9 分子生成上实现 **93.77%** 的新颖度与 **85.34%** 的 V.U.N. 综合分数，均为最优水平。消融实验进一步证实，性能增益源于双曲几何的归纳偏置而非架构本身——欧氏 VQVAE 在 Community-20 上的轨道 MMD 高达 0.7555，而双曲 HVQVAE 仅为 0.0005，差距超过三个数量级。



图生成模型在分子设计、社交网络建模等任务中扮演着关键角色。然而，现有方法面临一个根本性瓶颈：**欧氏潜在空间无法捕捉图数据中普遍存在的指数级层次复杂性**。真实世界的图——从社交网络到分子结构——通常呈现幂律度分布、长程依赖和深层树状层次，这些模式在欧氏空间中需要极高维度才能嵌入，否则会导致严重的结构失真。

具体而言，当前欧氏图生成模型存在两大结构性缺陷：

1. **显式边建模的冗余与偏差**：主流方法（扩散模型、自回归模型）将节点和边分别建模，或者采用混合潜在空间。这种分离式设计不仅增加了计算开销，更关键的是，边连通性被当作独立对象处理，丧失了从全局几何结构自然涌现的能力。当图规模增大或层次加深时，显式边预测的误差会逐层累积，导致生成的图在度分布、聚类系数等结构统计量上偏离真实分布。

2. **欧氏几何的容量瓶颈**：欧氏空间体积随半径多项式增长，而层次结构的节点数通常随深度指数增长。这一容量失配迫使欧氏模型在高维空间中“挤压”层次信息，造成长程依赖的衰减和幂律尾部的截断。实验证据表明，欧氏VQVAE在Community-20数据集上的轨道MMD高达0.7555，而双曲版本仅为0.0005——差距超过1500倍，直接印证了欧氏空间对层次结构的表达无能。

GGBall的动机源于一个核心洞察：**双曲几何因其指数增长的体积，天然保持层次结构**。庞加莱球模型中，距离边界越近，空间体积呈指数膨胀，恰好匹配树状层次中节点数随深度指数增长的规律。将整图编码为统一的节点双曲嵌入后，边连通性可由节点间的测地线距离自然涌现——距离近的节点更可能相连，距离远的节点则自然断开。这种“结构感知”的生成范式，使得模型无需显式枚举边即可保持全局拓扑一致性。

基于上述动机，GGBall提出三项关键转变：
- **空间几何**：从欧氏空间转向庞加莱球双曲空间；
- **图表示**：从节点/边分离建模转向统一节点潜在表示，边由几何距离隐式编码；
- **生成范式**：从迭代去噪的扩散过程转向向量量化编码配合黎曼流匹配先验，支持一步生成。

这一设计使得模型在层次图数据集上平均生成误差最高降低18%，在树结构数据集上实现近乎完美的重建（度MMD仅7.9×10⁻⁴），并在QM9分子生成任务上同时实现最高新颖度（93.77%）和最优V.U.N.分数（85.34%），突破了现有方法在有效性与新颖性之间的权衡困境。



## 核心方法与创新机理

### 瓶颈：欧氏空间的层次坍塌

图生成模型长期受困于一个根本性矛盾：现实世界的图数据——从社交网络到分子结构——普遍呈现指数级增长的层次复杂性和幂律度分布，而主流生成范式却将整张图强行嵌入平坦的欧氏潜在空间。欧氏空间的体积仅随半径多项式增长，无法为深层树状或社区嵌套结构提供足够的“几何容量”，导致长程依赖被压缩、度分布严重失真。这正是 **GGBall** 试图打破的核心瓶颈。

### 关键转向：从欧氏到双曲的全管线重构

GGBall 的核心创新并非在现有欧氏框架上修补，而是将整个生成管线从欧氏空间**整体迁移**到庞加莱球双曲几何。这一转向由三个环环相扣的 changed slots 驱动：

**1. 潜在空间几何：欧氏 → 庞加莱球双曲空间**

双曲几何的独特优势在于其体积随半径**指数增长**——这与层次图拓扑的扩张模式天然同构。庞加莱球模型将无穷大的双曲空间共形映射到单位开球内，使得深层树结构可以在有限坐标范围内被精确编码。实验证据极其有力：在 Community-small 数据集上，欧氏 VQ-VAE 的轨道 MMD 高达 0.7555，而双曲 HVQVAE 仅为 0.0005，差距超过 **1500 倍**。这直接证明性能增益源于双曲几何的归纳偏置，而非网络架构或量化策略本身。

**2. 图表示形式：节点/边分离建模 → 统一节点潜在表示**

传统方法将节点和边分别建模，或采用混合潜在空间，割裂了图拓扑的内在统一性。GGBall 采用 **节点唯一潜在表示**：整张图被编码为一组节点的双曲嵌入，边连通性不再显式建模，而是作为节点间双曲距离的**涌现属性**。解码器仅通过双曲几何特征——对数映射、测地线距离、角度余弦——即可重建边概率。这种设计使得层次结构被隐式编码在节点嵌入的相对几何位置中，避免了显式边建模的信息瓶颈。

**3. 生成范式：迭代扩散 → 向量量化 + 黎曼流匹配**

扩散模型虽在图像生成中占据主导，但将其应用于图结构时需反复去噪，计算开销大且对离散拓扑的建模不够直接。GGBall 采用两阶段方案：先用 **双曲向量量化自编码器（HVQVAE）** 将图离散化为 Poincaré 码本中的 token，再通过 **黎曼流匹配先验** 在双曲空间学习从基础分布到目标潜在分布的确定性向量场。流匹配基于闭式测地线定义条件向量场，支持 **一步生成**，避免了扩散的迭代开销。在 QM9 分子生成上，HVQVAE+Flow 同时实现 93.77% 的新颖度和 85.34 的 V.U.N. 分数，均为所有方法中最优。

### 架构支撑：Poincaré GNN 与 Poincaré DiT

上述 changed slots 的实现依赖于两个原生双曲神经网络：

- **Poincaré GNN**：通过切线空间聚合和双曲距离调制的消息函数，在保持几何一致性的前提下进行节点特征更新。公式为 $\pmb{h}_i^{l+1} = \exp_0^c(\log_0^c(\pmb{h}_i^l) + \mathcal{W}_x[\log_0^c(\pmb{h}_i^l), \log_0^c(\mathbf{M}(m_i^{l+1}))])$，将自表示与聚合消息在原点切空间融合后映射回双曲流形。
- **Poincaré Diffusion Transformer (DiT)**：用测地线距离替代点积计算注意力权重 $\alpha_{ij} \propto \exp(-\tau d_c(\mathbf{q}_i, \mathbf{k}_j))$，并以 Möbius 回旋中点聚合 value 向量，确保加权平均操作在双曲空间中的几何封闭性。

### 证据强度总结

| 创新维度 | 关键证据 | 置信度 |
|---------|---------|--------|
| 双曲几何优势 | 欧氏 vs 双曲 VQVAE 轨道 MMD 差距 >1500× | 极高 |
| 统一节点表示 | 树结构重建度 MMD 仅 7.9×10⁻⁴ | 极高 |
| 一步流匹配 | QM9 新颖度 93.77%，V.U.N. 85.34 | 高 |
| 架构稳定性 | 多随机种子下方差小，HVQVAE 避免 HVAE 的 KL 散度振荡 | 高 |

需要注意的是，当前验证集中在中小规模图（Community-Small 12-20 节点、Ego-small 4-18 节点、QM9 最多 9 个重原子），扩展到万级节点社交网络或引文图的可行性尚未验证。此外，码本坍缩风险在高维庞加莱空间中的鲁棒性仍需进一步研究。



![[assets/figures/papers/iclr26_0010_4zRRnDscqn_GGBall_Graph_Generative_Model_on_Poincaré_Ball/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our hyperbolic graph generation framework. We encode graphs into a hyperbolic latent space using a Poincaré GNN and geodesic-attention Transformer. The latent representations are quantized via a Poincaré codebook and modeled with a Poincaré flow prior. A hyperbolic Transformer then decodes the latent code to reconstruct or generate graphs, enabling structure-aware generation in non-Euclidean geometry*

GGBall 采用**两阶段生成范式**，将图生成问题完全迁移至庞加莱球双曲空间。其核心创新在于**统一的节点潜在表示**：整张图被编码为一组节点嵌入，边连通性由节点间的几何距离自然涌现，而非显式建模。

### 管线总览

整个框架由四个模块串联构成，均在庞加莱球模型 $\mathbb{B}_c^n$ 内运作：

1. **双曲图编码器**：以 Poincaré GNN 与测地线注意力 Transformer 为骨干，将输入图映射为节点级双曲嵌入。
2. **双曲向量量化**：通过 Poincaré 码本将连续潜在表示离散化为离散 token，增强训练稳定性与结构表达能力。
3. **黎曼流匹配先验**：在双曲潜在空间学习确定性向量场，将简单基础分布连续变换为目标潜在分布，支持一步生成。
4. **双曲解码器**：基于节点嵌入的几何特征（对数映射、双曲距离、夹角等）重建节点属性与边概率。

这一设计使得**图拓扑完全由潜在空间的几何结构决定**，避免了欧氏空间对层次结构的指数级压缩失真。

### 编码器：结构感知的双曲嵌入

编码器首先通过**Poincaré GNN** 聚合局部邻域信息。每一层将邻域节点与边特征投影到原点切空间进行线性变换，再通过指数映射拉回双曲空间：

$$\pmb{h}_i^{l+1} = \exp_0^c\left(\log_0^c(\pmb{h}_i^l) + \mathcal{W}_x\left[\log_0^c(\pmb{h}_i^l), \log_0^c(\mathbf{M}(m_i^{l+1}))\right]\right)$$

其中消息函数 $\mathbf{M}(\cdot)$ 融合了**双曲距离调制**的边权重，使几何邻近的节点获得更强的信息交互。

随后，**Poincaré 扩散 Transformer** 捕获全局依赖。注意力权重由测地线距离而非内积计算：

$$\alpha_{ij} \propto \exp\left(-\tau \, d_c(\mathbf{q}_i, \mathbf{k}_j)\right)$$

值向量的聚合使用 **Möbius 回旋中点** 加权平均，确保结果始终保持在庞加莱球内，保持几何一致性。

### 向量量化：离散潜在空间

编码器输出的连续嵌入 $z$ 通过 Poincaré 码本 $\mathcal{C}$ 离散化：

$$z_q = \arg\min_{c \in \mathcal{C}} d_c(z, c)$$

码本通过**测地线聚类**初始化，并使用黎曼优化器更新。训练目标结合重建损失、承诺损失与一致性损失：

$$\mathcal{L}_{\mathrm{HVQVAE}} = \lambda_1 \mathcal{L}_{\mathrm{AE}} + \lambda_2 \mathbb{E}_z [d_c^2(\mathbf{sg}(z_q), z)] + \lambda_3 \mathbb{E}_z [d_c^2(z_q, \mathbf{sg}(z))]$$

离散化不仅稳定了训练过程，还避免了连续变分自编码器中 KL 散度的数值不稳定问题。

### 黎曼流匹配先验

在潜在空间，GGBall 采用**黎曼条件流匹配**学习生成先验。给定基础分布 $p(z_0)$ 与目标分布 $p(z_1)$，模型学习向量场 $v_\theta$ 以匹配条件概率路径：

$$\mathcal{L}_{\mathrm{RCFM}} = \mathbb{E}_{t, z_0, z_1, z_t} \left\| v_{\theta}(z_t, t) - u_t(z_t \mid z_1, z_0) \right\|_{\mathfrak{g}}^2$$

其中 $u_t$ 是沿测地线连接 $z_0$ 与 $z_1$ 的条件向量场。该先验支持从噪声直接一步采样生成，无需迭代去噪。

### 解码器：几何驱动的图重建

解码器从量化后的节点嵌入 $z_q$ 重建图结构。对每对节点 $(i, j)$，构造五维几何特征向量：

$$f_{ij} = \left[ \log_0^c(h_i),\; \log_0^c(h_j),\; \log_{h_i}^c(h_j),\; d_c(h_i, h_j),\; \cos\theta_{ij} \right]$$

这些特征捕获了节点在双曲空间中的绝对位置、相对位移、测地线距离与方向角，经 MLP 解码为边概率与节点属性。由于边信息完全由节点几何隐式编码，解码器无需显式建模边嵌入。

### 输入输出流

- **输入**：图 $G = (X, E)$，包含节点特征 $X$ 与边特征 $E$。
- **编码**：$G \to$ Poincaré GNN $\to$ Poincaré Transformer $\to$ 节点嵌入 $z \in \mathbb{B}_c^n$。
- **量化**：$z \to z_q \in \mathcal{C}$（训练时通过直通估计器传递梯度）。
- **生成**：从基础分布采样 $z_0$，经流匹配 ODE 推演至 $z_1$，量化后送入解码器。
- **输出**：重建/生成的节点属性 $\hat{X}$ 与邻接矩阵 $\hat{E}$。



### 整体架构与设计理念

GGBall 采用“编码-量化-先验-解码”四阶段管线，全程在庞加莱球 $\mathbb{B}_c^n = \{ \mathbf{x} \in \mathbb{R}^n \mid c \|\mathbf{x}\|^2 < 1 \}$ 上运行。核心创新在于：将整图映射为统一的节点级潜在表示，边的连通性由节点在双曲空间中的几何距离自然涌现，而非显式建模邻接矩阵。

框架包含三个可互换的自编码器变体——连续型 HGAE、概率型 HVAE 和离散型 HVQVAE，其中 HVQVAE 因离散化带来的训练稳定性和表达力成为主模型。生成阶段采用黎曼流匹配作为双曲先验，支持一步生成，避免了扩散模型的迭代去噪开销。

### 双曲图编码器

编码器由 Poincaré GNN 和 Poincaré 扩散 Transformer 堆叠而成，逐层提取局部和全局结构特征。

**Poincaré GNN 层** 的核心操作是在切线空间进行消息聚合，再通过指数映射回到双曲流形。邻居消息的聚合公式为：

$$m_i^{l+1} = \sum_{j \in \mathcal{N}(i)} \mathcal{W}_e[\log_0^c(h_i^l), \log_0^c(h_j^l), \log_0^c(h_{ij}^l)]$$

其中 $\log_0^c(\cdot)$ 将节点和边嵌入映射到原点处的切线空间，$\mathcal{W}_e$ 为可学习的消息函数。聚合后的消息通过距离调制增强结构感知，节点更新公式为：

$$\pmb{h}_i^{l+1} = \exp_0^c(\log_0^c(\pmb{h}_i^l) + \mathcal{W}_x[\log_0^c(\pmb{h}_i^l), \log_0^c(\mathbf{M}(m_i^{l+1}))])$$

$\exp_0^c$ 将更新后的切线空间表示映射回庞加莱球，$\mathbf{M}$ 为距离调制函数。

**Poincaré 扩散 Transformer 层** 用测地线注意力替代标准点积注意力，权重计算基于双曲距离：

$$\alpha_{ij} \propto \exp(-\tau d_c(\mathbf{q}_i, \mathbf{k}_j))$$

其中 $d_c(\mathbf{x}, \mathbf{y}) = \frac{2}{\sqrt{c}} \tanh^{-1}(\sqrt{c} \|\ominus_c \mathbf{x} \oplus_c \mathbf{y}\|)$ 为庞加莱球上的测地线距离。值向量的聚合使用 Möbius 回旋中点，保持几何一致性：

$$\pmb{Z}_i = \sum_{j=1}^T [\pmb{v}_j, \alpha_{ij}]_c := \frac{1}{2} \otimes_c \left( \frac{\sum_j \alpha_{ij} \lambda_c^{v_j} \pmb{v}_j}{\sum_j |\alpha_{ij}| (\lambda_c^{v_j} - 1)} \right)$$

其中 $\lambda_c^x = 2(1 - c\|\mathbf{x}\|^2)^{-1}$ 为共形因子，$\oplus_c$ 为 Möbius 加法。

### 双曲向量量化

编码器输出的连续嵌入 $z$ 通过 Poincaré 码本离散化：$z_q = \arg\min_{c \in \mathcal{C}} d_c(z, c)$。码本通过双曲 k-Means（测地线聚类）初始化，使用黎曼优化器更新。训练目标结合重建损失、承诺损失和一致性损失：

$$\mathcal{L}_{\mathrm{HVQVAE}} = \lambda_1 \mathcal{L}_{\mathrm{AE}} + \lambda_2 \mathbb{E}_z [d_c^2(\mathbf{sg}(z_q), z)] + \lambda_3 \mathbb{E}_z [d_c^2(z_q, \mathbf{sg}(z))]$$

其中 $\mathbf{sg}$ 为梯度截断算子。第二项鼓励编码器输出靠近码本向量，第三项约束码本向量不过度偏离编码器输出。

### 黎曼流匹配先验

生成阶段在双曲潜在空间上学习确定性向量场 $v_\theta(z_t, t)$，将基础分布 $p(z_0)$ 连续变换为目标潜在分布 $p_\phi(X, E)$。训练最小化黎曼条件流匹配目标：

$$\mathcal{L}_{\mathrm{RCFM}} = \mathbb{E}_{t \sim U(0,1), z_0 \sim p(z_0), z_1 \sim p_{\phi}, z_t \sim p_t(z_0, z_1)} \| v_{\theta}(z_t, t) - u_t(z_t | z_1, z_0) \|_{\mathfrak{g}}^2$$

其中 $u_t$ 为以 $z_0, z_1$ 为条件的闭式测地线向量场，$\|\cdot\|_{\mathfrak{g}}$ 为黎曼度量下的范数。向量场 $v_\theta$ 由 Poincaré DiT 主干参数化，推理时沿学习到的向量场积分即可一步生成潜在码。

### 双曲解码器

解码器基于节点双曲嵌入的几何特征重建节点属性和边概率。对每对节点 $(i,j)$，计算五维几何特征向量：

$$f_{ij} = [\log_0^c(h_i), \log_0^c(h_j), \log_{h_i}^c(h_j), d_c(h_i, h_j), \cos\theta_{ij}]$$

包含原点切线投影、相对对数映射、测地线距离和夹角。这些特征经 MLP 映射为边类型 logits 和节点属性预测。整体训练目标为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{recon}} + \lambda_{\mathrm{degree}} \mathcal{L}_{\mathrm{degree}} + \lambda_{\mathrm{reg}} \mathcal{L}_{\mathrm{reg}}$$

其中 $\mathcal{L}_{\mathrm{degree}}$ 约束预测边数与节点度一致性，$\mathcal{L}_{\mathrm{reg}}$ 为正则化项。



## 实验与关键发现

### 核心瓶颈验证

欧氏潜在空间无法捕捉图数据中指数级的层次复杂性，导致长程依赖和幂律度分布严重失真。GGBall 将整个生成管线从欧氏空间转向庞加莱球双曲几何，核心因果机制在于：双曲空间因其指数增长的体积天然保持层次结构，将整图编码为节点双曲嵌入后，边连通性由节点间的几何距离自然涌现，从而实现结构感知的生成。

这一机制在实验中得到系统性验证。表 10 的消融实验给出了决定性证据：在 Comm20 数据集上，欧氏 VQVAE 的轨道 MMD 为 0.7555，而双曲 HVQVAE 仅为 0.0005，差距超过 **1500 倍**。这表明性能增益并非源于网络架构或码本量化本身，而是双曲几何的归纳偏置。Figure 1 进一步展示了双曲模型在度相似性和边重建精度上的一致性优势——双曲潜在模型在幂律度分布上的 MMD 比欧氏模型低约 **4 倍**。

![[assets/figures/papers/iclr26_0010_4zRRnDscqn_GGBall_Graph_Generative_Model_on_Poincaré_Ball/figures/017_Table_10.jpg]]
*Table 10: Reconstruction Performance: Hyperbolic vs. Euclidean Parametrization*

![[assets/figures/papers/iclr26_0010_4zRRnDscqn_GGBall_Graph_Generative_Model_on_Poincaré_Ball/figures/001_Figure_1.jpg]]
*Figure 1: Degree similarity and edge reconstruction accuracy on reconstructed dataset. Hyperbolic models consistently outperform Euclidean baselines*

### 主实验结果

**抽象图生成（Community-small & Ego-small）。** 表 2 报告了抽象图生成的结构统计差异。HVQVAE+Flow 在两个数据集上均取得最低平均 MMD：Community-small 上为 0.0215（HGDM 为 0.0240），Ego-small 上为 0.0112（HGDM 为 0.0137），平均生成误差最高降低 **18%**。这一优势在度分布、聚类系数和轨道计数三个结构敏感指标上均保持一致。

![[assets/figures/papers/iclr26_0010_4zRRnDscqn_GGBall_Graph_Generative_Model_on_Poincaré_Ball/figures/005_Table_2.jpg]]
*Table 2: Abstract graph generation on Community-small and Ego-small dataset. We evaluate the difference in graph statistics (and their mean) between generated and ground truth graphs. Best results are in bold, second best are underlined*

**分子图生成（QM9）。** 表 3 展示了分子生成结果。HVQVAE+Flow 实现了 **93.77%** 的新颖度，显著超越此前最优的 EDP-GNN（86.58%），提升幅度达 **7.19 个百分点**。在综合指标 V.U.N.（有效性 × 独特性 × 新颖性）上，HVQVAE+Flow 达到 **85.34%**，超越 GDSS 的 81.31% 和 HGDM 的 83.64%，实现了有效性与新颖性的最优平衡——此前方法通常在这两个维度间存在严重折中。

![[assets/figures/papers/iclr26_0010_4zRRnDscqn_GGBall_Graph_Generative_Model_on_Poincaré_Ball/figures/006_Table_3.jpg]]
*Table 3: Molecular graph generation on QM9. We report standard metrics and derived metrics V.N. (Valid × Novel), N/U (Novelty rate). All values are reported as percentages*

**ZINC250k 扩展验证。** 表 9 显示 GGBall 在更大规模的 ZINC250k 数据集上保持 100% 独特性，V.U.N 指标与 GraphDF 接近（88.32 vs 89.03），验证了方法在中等规模分子图上的可扩展性。

### 重建质量与架构消融

表 1 和表 8 系统对比了三种自编码器变体的重建性能。HVQVAE 在所有指标上一致优于连续 HAE：在 QM9 上，有效性从 HAE 的 95.18% 提升至 99.14%。HVAE 表现最差，原因在于双曲空间中 KL 散度的数值不稳定——训练过程中 KL 项剧烈波动，导致优化困难。HVQVAE 通过离散化潜在空间规避了这一问题，同时保持了高表达力。

![[assets/figures/papers/iclr26_0010_4zRRnDscqn_GGBall_Graph_Generative_Model_on_Poincaré_Ball/figures/012_Table_8.jpg]]
*Table 8: Reconstruction performance of our baseline models HAE, HVAE, and HVQVAE on abstract graphs (Community-small, Ego-small)*

树结构数据集上的重建近乎完美：双曲 VQVAE 的度 MMD 仅为 **7.9×10⁻⁴**，验证了双曲几何对层次结构的天然适配能力。多随机种子稳定性测试（表 11）表明，双曲 VQVAE 的重建误差和生成指标方差极小，具有良好的可复现性。

### 推理效率

表 12 报告了 Community-small 上的推理效率对比。HVQVAE+Flow 支持一步生成，避免了扩散模型的迭代去噪过程，在推理时间和显存占用上具备竞争力。具体而言，其推理速度显著快于需要多步去噪的扩散基线（如 DiGress、GDSS），同时保持更低的显存占用。

### 失败模式与局限

1. **规模扩展未验证。** 当前实验仅覆盖小到中等规模图（节点数 9-38），扩展到万级节点的社交网络或引文网络时，双曲 GNN 的切线空间聚合和测地线注意力的计算开销可能成为瓶颈。
2. **混合曲率缺失。** 对于包含异构结构模式（如局部团状结构嵌套在全局树状结构中）的图，单一负曲率空间可能不是最优选择，混合曲率潜在空间的潜力未被探索。
3. **双曲 VAE 不稳定。** HVAE 的 KL 散度数值不稳定问题仍待解决，当前 VQ 方案是规避而非根除此问题。
4. **码本坍缩风险。** 在高维庞加莱空间中，EMA 更新和死码元复活策略能否完全避免码本坍缩，尚未经过充分验证。
5. **应用验证不足。** 未在条件分子设计、知识图谱增强等应用导向任务上验证实用性。

> **注意：** 部分消融实验（如带宽损失与双曲正则器的交互影响、高维码本坍缩鲁棒性）在提供的证据中未充分覆盖，相关结论需查阅原文附录或进行手动验证。



## 定位与知识库关联

### 生成范式定位

GGBall 在现有图生成方法谱系中占据了一个独特的交叉点：它将向量量化自编码器（VQ-VAE）的离散潜在表示与黎曼流匹配（Riemannian flow matching）的连续先验相结合，且整个管线运行在庞加莱球双曲空间上。这种设计使其区别于以下主要范式：

- **欧氏一步生成模型**（GraphVAE、VQGAE）：共享 VAE/VQ 架构骨架，但受限于欧氏潜在空间对层次结构的表达能力瓶颈。GGBall 通过将整个管线转向双曲几何，从根本上改变了潜在空间的归纳偏置。
- **扩散模型**（EDP-GNN、GDSS、DiGress）：依赖迭代去噪过程，推理效率受限。GGBall 的流匹配先验支持一步生成，在推理速度上具有天然优势。混合双曲-欧氏扩散模型 HGDM 虽引入了双曲组件，但仅在部分模块使用，且仍保留扩散范式。
- **自回归模型**（GraphRNN、GraphAF）：逐节点/逐边生成，需要显式排序，难以捕获全局拓扑。GGBall 的统一节点潜在表示使边连通性从几何距离中自然涌现，避免了对生成顺序的依赖。
- **流模型**（GNF、CatFlow）：GGBall 的流匹配组件与这些方法共享连续归一化流的思想，但将流定义在黎曼流形而非欧氏空间上，利用闭式测地线构造条件向量场。

### 适用边界

当前验证的适用范围明确：

1. **图规模**：实验覆盖 Community-Small（12-20节点）、Ego-Small（4-18节点）、QM9（最多9个重原子）、ZINC250k（最多38个重原子）。扩展到万级节点的大规模网络（社交网络、引文网络）的可行性尚未验证。
2. **图类型**：在层次结构显著的数据集（树状社区图、分子图）上优势突出。对于缺乏明显层次结构的随机图或网格图，双曲几何的归纳偏置可能不带来增益。
3. **任务类型**：当前聚焦于无条件生成和重建质量评估。未在应用导向任务（条件分子设计、知识图谱增强、属性可控生成）上验证实用性。

### 局限性与已知失效模式

1. **双曲 VAE 的数值不稳定性**：HVAE 变体在训练中 KL 散度剧烈振荡，边重建精度提升缓慢且次优。这一失效模式直接促使作者放弃连续变分先验，转向离散 VQ 方案。但 VQ 方案本身在高维庞加莱空间中仍面临码本坍缩风险，其鲁棒性未充分验证。

2. **曲率选择的单一性**：当前模型在整个潜在空间中使用固定负曲率。对于包含异构结构模式的图（如局部树状、局部团状），混合曲率潜在空间可能更具优势，但这一方向未被探索。

3. **规模扩展的未解问题**：双曲 GNN 和 Transformer 的计算复杂度随节点数增长，且庞加莱球中的数值精度在边界附近衰减。这些因素可能限制向大规模图的扩展。

4. **评估指标的局限**：生成质量主要依赖 MMD（度、聚类系数、轨道计数）和分子有效性指标。对于更细粒度的结构保真度（如子图同构频率、模体分布）缺乏系统评估。

### 开放问题

1. **大规模扩展**：如何将双曲生成模型扩展到万级节点的图，同时保持层次结构建模优势？可能需要层次化潜在编码或混合精度计算策略。

2. **混合曲率潜在空间**：在单一半径的庞加莱球中，不同区域的体积增长率是均匀的。引入混合曲率（如乘积流形或可学习曲率）能否进一步提升对异构图拓扑的建模能力？

3. **稳定的双曲变分先验**：当前 VQ 方案虽稳定，但牺牲了潜在空间的连续性和平滑插值能力。如何设计数值稳定的双曲 VAE 先验（如改进的 KL 散度估计或正则化策略）仍是一个开放挑战。

4. **码本坍缩的几何根源**：在高维庞加莱球中，EMA 更新和死码元复活策略是否能完全避免码本坍缩？坍缩风险是否与曲率、码本大小和潜在维度存在系统性关系？

5. **带宽损失与双曲正则器的交互**：HVQVAE 中使用的带宽损失（bandwidth loss）与其他双曲特定正则器（如保持距离的映射约束）在高深度架构中的交互影响尚不清楚。



## 原文 PDF

![[paperPDFs/ICLR_2026/GGBall_Graph_Generative_Model_on_Poincaré_Ball.pdf]]
