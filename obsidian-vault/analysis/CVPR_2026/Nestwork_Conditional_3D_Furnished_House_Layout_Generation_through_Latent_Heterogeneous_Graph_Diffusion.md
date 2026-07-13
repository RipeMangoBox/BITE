---
title: "Nestwork: Conditional 3D Furnished House Layout Generation through Latent Heterogeneous Graph Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Nestwork_Conditional_3D_Furnished_House_Layout_Generation_through_Latent_Heterogeneous_Graph_Diffusion.pdf
project_link: null
code_link: null
aliases:
- Nestwork
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将房屋建模为一个包含房间、家具和多种空间关系的异构图，利用类型感知的图注意力网络（HetGAT）在潜在空间中进行扩散去噪，并采用低秩关系场补偿缺失的几何边信息。
primary_logic: 通过无条件自编码器结合低秩关系场，在潜在空间中对异构图进行编码；利用随机掩蔽语义图训练单一扩散模型，实现从仅拓扑到全语义图的灵活条件生成，无需重新训练。
claims:
- 统一模型相比两阶段基线在FID上从41.90降至7.26，结构满意度从78.60%提升至91.91%。
- HetGAT骨架相比同质GCN在各项指标上均占优，FID降低达50%以上。
- 移除低秩关系场导致碰撞率增加近一倍（21.54% vs 10.91%），且保真度下降。
- 以随机掩蔽交叉注意力替代简单特征注入，性能大幅下滑，验证了拓扑感知条件化的必要性。
---

# Nestwork: Conditional 3D Furnished House Layout Generation through Latent Heterogeneous Graph Diffusion

> [!tip] 核心洞察
> 通过无条件自编码器结合低秩关系场，在潜在空间中对异构图进行编码；利用随机掩蔽语义图训练单一扩散模型，实现从仅拓扑到全语义图的灵活条件生成，无需重新训练。

| 字段 | 内容 |
|------|------|
| 中文题名 | Nestwork: 基于潜在异构图扩散的条件3D带家具房屋布局生成 |
| 英文题名 | Nestwork: Conditional 3D Furnished House Layout Generation through Latent Heterogeneous Graph Diffusion |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Miao_Nestwork_Conditional_3D_Furnished_House_Layout_Generation_through_Latent_Heterogeneous_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Nestwork |
| Dataset | HG-FRONT |

> [!tip] 效果简介
> - HG-FRONT 上，FID↓ 7.26 ± 0.43 vs 41.90 ± 0.40 (-34.64)；KID↓ (x100) 0.26 ± 0.04 vs 2.97 ± 0.02 (-2.71)；Collision %↓ 10.91 ± 0.21 vs 9.84 ± 0.08 (+1.07)。

## 概要

**问题瓶颈**：现有3D带家具房屋布局生成方法普遍将任务拆分为房屋级结构生成（无家具）与房间级家具摆放两个孤立阶段，缺乏对房间结构、家具布置及多类空间关系的联合推理，导致空间不一致与误差累积。

**核心方法**：Nestwork将整栋房屋建模为一个包含房间节点、家具节点及五类空间关系的异构图，通过**异构图注意力网络（HetGAT）**在紧凑的潜在空间中进行扩散去噪，并引入**低秩关系场（LRF）**从节点潜在变量推断缺失的几何边信息，实现端到端的统一生成。

**关键能力**：单一扩散模型通过**随机掩蔽语义图**训练，可在不重新训练的情况下灵活支持从仅拓扑约束到全语义图的多种条件化模式，并兼容自然语言描述作为全局上下文输入。

**主要结果**：在HG-FRONT数据集上，Nestwork相比两阶段基线将FID从41.90降至7.26，结构满意度从78.60%提升至91.91%；HetGAT骨架与LRF模块均被消融实验证实为关键设计，移除后性能显著退化。



### 问题背景

3D室内场景生成是计算机视觉与图形学中长期存在的核心问题，其应用涵盖建筑可视化、室内设计辅助、虚拟现实与具身智能仿真环境构建。一个完整的带家具房屋布局需要同时决定房间的拓扑结构（房间数量、类型、相邻关系）以及每个房间内部家具的类别、位置、尺寸和朝向。这两类决策高度耦合：房间的尺寸和形状约束了可容纳的家具组合，而家具的摆放又反过来影响房间的功能分区和流通路径。因此，生成任务本质上要求对房屋结构进行**联合推理**。

### 现有方法的缺口：拆分式生成与误差累积

当前主流方法普遍采用**拆分式策略**，将问题分解为两个独立阶段：首先生成房屋级布局（房间的边界框和邻接图），然后在每个房间内独立进行家具布局。这种两阶段方案虽然降低了单步建模的复杂度，但引入了根本性的结构缺陷：

1. **空间不一致**：房间级家具生成器无法感知跨房间的空间约束，例如相邻房间的家具可能穿透墙壁，或门口区域被两侧家具同时阻塞。
2. **误差累积**：房屋级布局的几何误差（如房间尺寸偏差）会直接传播到下游家具布局，第二阶段无法修正上游的错误。
3. **缺乏联合推理**：房间形状与家具配置之间存在双向约束——例如，一个狭长房间可能更适合靠墙放置沙发而非居中摆放——但拆分式方法割裂了这一反馈回路。

### 核心瓶颈与本文动机

上述问题的根源在于现有方法缺乏对**房间结构与家具摆放的联合表示与推理机制**。房屋本质上是一个包含多类实体（虚拟房屋、房间、家具）和多种空间关系（相邻、包含、远离）的异构图，但现有工作要么忽略图结构，要么使用同质图模型抹平了类型差异。

**Nestwork** 的动机正是填补这一空白：将带家具的3D房屋显式建模为一个**异构图（heterogeneous graph）**，其中节点类型包括房屋、房间和家具，边类型涵盖家具-家具全连接、家具-房间归属、相邻房间、远离房间以及房间-房屋包含共五类关系。在此基础上，通过**类型感知的图注意力网络（HetGAT）**在潜在空间中进行扩散去噪，实现房屋结构与家具布局的联合生成。这一设计使得模型能够同时推理房间拓扑和家具配置，从根本上消除了拆分式方法的结构性缺陷。



## 核心方法与创新机理

Nestwork 的核心创新在于将“房屋结构—家具布局”联合推理建模为一个**异构图的潜在扩散生成问题**，从而突破了现有方法将房屋级布局与房间级家具摆放拆分为两阶段处理的根本瓶颈。围绕这一思路，方法在四个关键维度上引入了与 baseline 本质不同的设计。

### 1. 异构图表征：从“先结构后家具”到“统一异构图”

传统两阶段方案（如先独立生成房间内家具，再拼接为完整房屋）将房间结构与家具摆放视为两个孤立的生成任务，缺乏跨房间的空间一致性约束，容易导致家具碰撞、流线断裂和误差累积。Nestwork 将整个房屋建模为一个统一的异构图：

$$G = \langle V, E, T_V, T_E, X_V, X_E \rangle$$

其中节点 $V$ 同时包含虚拟房屋节点、房间节点和家具节点三种类型（$T_V$），边 $E$ 涵盖五类空间关系：家具-家具全连接（$E_{FF}$）、家具-房间（$E_{FR}$）、相邻房间（$E_{RR}^{adj}$）、远离房间（$E_{RR}^{far}$）和房间-房屋（$E_{RH}$）。这一设计使得模型能够在一次前向传播中同时推理房间拓扑与家具布局，从根本上消除了两阶段分离带来的信息割裂。

### 2. HetGAT 骨架：类型感知的图注意力网络

**Changed Slot：图神经网络骨架**  
Baseline 采用同质 GNN（如 GCN）或 Transformer，对所有节点和边使用统一的消息传递规则，无法区分房间节点与家具节点在空间语义上的本质差异。Nestwork 采用**异构图注意力网络（HetGAT）**，融合了 GAT 的注意力机制、EGAT 的边特征感知以及 HEAT 的类型特定变换：

$$s_{uv,h}^{(l)} = \text{LeakyReLU}\big( \mathbf{q}_h^\top [ \mathbf{h}_u^{(l)} \| \mathbf{h}_v^{(l)} \| \mathbf{e}_{uv}^{(l)} ] \big)$$

$$\mathbf{h}_u^{(l+1)} = \|_{h=1}^H \sigma\big( \sum_{v\in\mathcal{N}(u)} \alpha_{uv,h}^{(l)} \mathbf{W}_h [ \mathbf{h}_v^{(l)} \| \mathbf{e}_{uv}^{(l)} ] \big)$$

类型感知的变换矩阵 $\mathbf{W}_h$ 随节点类型而异，使房间节点和家具节点在消息聚合时使用不同的投影空间。消融实验（Table 2）证实，HetGAT 在所有指标上均优于 GCN、GAT 等同质变体，FID 降低幅度超过 50%，尤其在结构满意度上优势显著——这验证了异构类型感知对于联合推理房间拓扑与家具布局的关键作用。

### 3. 低秩关系场：从“依赖真值几何”到“潜在空间推断”

**Changed Slot：解码阶段边特征获取**  
在自编码器框架中，解码器需要边特征来重建节点间的空间关系。Baseline 方案依赖地面真值几何边特征（如相对位置、距离），这在生成场景中不可用。Nestwork 引入**低秩关系场（LRF）**模块，直接从节点潜在变量预测边嵌入：

$$\tilde{\mathbf{e}}_{uv} := \text{MLP}\big( [\mathbf{a}_u \| \mathbf{b}_v \| \boldsymbol{\alpha}_u^\top \boldsymbol{\alpha}_v \mathbf{\alpha}] \big)$$

其核心机制是将边关系分解为一组可学习的关系槽（relation slots），每个节点通过注意力分配 $\boldsymbol{\alpha}_u$ 表达其与各槽的亲和度，两个节点的槽亲和度内积经低秩分解后重建边嵌入。这一设计使解码器在推理时完全摆脱对真值几何边的依赖。消融实验（Table 5）表明，移除 LRF 导致碰撞率从 10.91% 飙升至 21.54%，Walkability 和 FID 均显著恶化，证实 LRF 提供的几何先验对于空间一致性不可或缺。

### 4. 随机掩蔽条件化：单模型适应多条件强度

**Changed Slot：条件化机制**  
现有条件生成方法通常针对固定条件强度设计（如全语义图或仅拓扑），不同条件模式需分别训练模型。Nestwork 提出**随机掩蔽跨注意力 + 图级嵌入**的多级条件化策略：训练时以 50% 概率随机掩蔽节点语义标签，迫使单一扩散模型同时学会从稀疏拓扑到全语义图的各类条件映射。

条件化通过两个层次注入：
- **节点级**：掩蔽后的语义图 $\tilde{G}_{\text{sem}}$ 经交叉注意力以残差形式更新节点潜在变量 $\mathbf{z}_u^{(t)} \gets \mathbf{z}_u^{(t)} + \alpha_{\text{ca}}(\mathbf{c}_u + \mathbf{g})$；
- **图级**：房屋包围盒和可选的文本描述经嵌入后作为全局上下文 $\mathbf{g}$ 注入所有节点。

条件扩散损失为：

$$\mathcal{L}_{\text{LD}}^{\text{cond}}(\theta) = \mathbb{E}_{G,t,\epsilon} \big[ \| \epsilon_\theta(G_t, t, \tilde{G}_{\text{sem}}, \mathbf{g}) - \epsilon \|_2^2 \big]$$

Table 3 显示，同一模型在仅拓扑、部分语义、全语义和文本提示四种条件下均能生成合理布局，无需重新训练。若将交叉注意力替换为简单特征注入（Table 5），FID 从 7.26 骤升至 76.35，KID 升至 5.87，验证了拓扑感知条件化的必要性。

### 创新总结

上述四个 changed slots 形成了一条完整的因果链：**异构图**提供了联合推理的表达基础，**HetGAT** 赋予模型区分节点类型的推理能力，**LRF** 在潜在空间中补全了几何边的缺失信息，而**随机掩蔽条件化**使单一模型获得了从稀疏到密集条件的灵活泛化能力。这一组合使 Nestwork 在 HG-FRONT 数据集上实现了 FID 从 41.90 到 7.26 的跨越式提升（Table 1），结构满意度从 78.60% 提升至 91.91%，同时保持了与两阶段方案可比的碰撞率水平。



Nestwork 将带家具的 3D 房屋布局生成建模为**异构图潜在扩散**问题，整个管线由三个核心阶段构成：**图自编码 → 潜在扩散去噪 → 解码与后处理**。其关键设计在于将房屋统一表示为一张异构图，并在紧凑的潜在空间中完成条件化生成，从而避免传统两阶段方法中房间结构与家具摆放分离推理导致的误差累积。

### 管线总览

如 Figure 2 所示，系统首先通过一个无条件的图自编码器将房屋异构图压缩为节点级潜在变量，随后在潜在空间中以掩蔽语义图为条件进行扩散去噪，最后将去噪后的潜在变量解码为完整的 3D 布局，并经后处理（Figure 3）得到最终可视化结果。

![[assets/figures/papers/paper_list_l2552_https_openaccess_thecvf_com_content_CVPR2026_html_Miao_Nestwork_Conditio/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our proposed pipeline, which encodes a heterogeneous house graph into a latent space via autoencoding, performs masked-graph-conditioned denoising through latent diffusion, and decodes the output into a complete 3D layout*

**阶段一：异构图自编码。** 编码器 $E$ 将房屋异构图 $G = \langle V, E, T_V, T_E, X_V, X_E \rangle$ 映射为节点级潜在表示 $Z$；解码器 $D$ 从 $Z$ 重建完整的图结构。由于解码阶段缺少地面真值的几何边特征，系统引入**低秩关系场**模块，直接从节点潜在变量推断边嵌入，为解码器提供几何关系先验。自编码器的训练目标为：

$$\mathcal{L} = \mathcal{L}_{\text{rec}} + \lambda_{\text{KL}} \mathcal{L}_{\text{KL}} + \lambda_{\text{LRF}} \mathcal{L}_{\text{LRF}}$$

其中重构损失 $\mathcal{L}_{\text{rec}}$ 分解为包围盒、角度、语义和形状四项损失，$\lambda_{\text{KL}}=10^{-4}$，$\lambda_{\text{LRF}}=0.1$。

**阶段二：条件潜在扩散。** 在冻结的自编码器潜在空间之上，训练一个时间条件化的 HetGAT 去噪器 $\epsilon_\theta$。前向扩散过程采用线性噪声计划向 $Z$ 逐步注入高斯噪声：

$$Z_t = \sqrt{\bar{\alpha}_t} Z + \sqrt{1-\bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

去噪器以掩蔽语义图 $\tilde{G}_{\text{sem}}$ 和全局上下文 $\mathbf{g}$ 为条件，训练目标为：

$$\mathcal{L}_{\text{LD}}^{\text{cond}}(\theta) = \mathbb{E}_{G,t,\epsilon} \big[ \| \epsilon_\theta(G_t, t, \tilde{G}_{\text{sem}}, \mathbf{g}) - \epsilon \|_2^2 \big]$$

条件化通过两级机制注入：**节点级条件化**利用掩蔽交叉注意力将语义信息融入节点潜在变量；**图级条件化**通过房屋包围盒和可选的文本描述嵌入提供全局几何与语义上下文。训练时采用 50% 随机掩蔽策略，使单一模型能够适应从仅拓扑到全语义图的多种条件强度，无需重新训练。

**阶段三：解码与后处理。** 去噪后的潜在变量经解码器还原为完整的异构图，再通过后处理管线（Figure 3）将离散的图表示转化为具有空间一致性的 3D 家具布局。

### 输入输出流

- **输入：** 房屋异构图，包含虚拟房屋节点、房间节点和家具节点三类节点，以及家具-家具全连接、家具-房间、相邻房间、远离房间、房间-房屋五类关系边。每个节点 $u$ 的特征向量为 $\mathbf{x}_u = [c; \mathbf{b}; o; \mathbf{s}]$，由类别 $c$、包围盒 $\mathbf{b} \in \mathbb{R}^6$、离散化朝向 $o$ 和形状编码 $\mathbf{s}$ 拼接而成。条件生成时可额外提供部分语义标签或自然语言描述。
- **输出：** 完整的 3D 房屋布局，包含所有房间的几何结构及内部家具的位置、朝向、尺寸和类别信息。

### 核心模块关系

整个管线的骨干网络为**异构图注意力网络**，在编码器、解码器和扩散去噪器中共享架构设计。HetGAT 对三类节点和五类边关系执行类型感知的消息传递，其注意力计算融合了节点状态和边特征：

$$s_{uv,h}^{(l)} = \text{LeakyReLU}( \mathbf{q}_h^\top [ \mathbf{h}_u^{(l)} \| \mathbf{h}_v^{(l)} \| \mathbf{e}_{uv}^{(l)} ] )$$

$$\mathbf{h}_u^{(l+1)} = \|_{h=1}^H \sigma\big( \sum_{v\in\mathcal{N}(u)} \alpha_{uv,h}^{(l)} \mathbf{W}_h [ \mathbf{h}_v^{(l)} \| \mathbf{e}_{uv}^{(l)} ] \big)$$

**低秩关系场**是连接编码器与解码器的关键桥梁：在解码阶段，它利用节点对关系槽的注意力分配和低秩分解，从潜在变量直接生成边嵌入 $\tilde{\mathbf{e}}_{uv}$，弥补了潜在空间无法保留完整几何边信息的缺陷。消融实验表明，移除 LRF 后碰撞率从 10.91% 升至 21.54%，验证了该模块提供的几何先验对空间一致性至关重要。



### 房屋异构图表示

Nestwork 将带家具的 3D 房屋统一建模为一个异构图，这是实现房间结构与家具摆放联合推理的基础数据结构。其形式化定义为：

$$G = \langle V, E, T_V, T_E, X_V, X_E \rangle$$

其中各符号含义如下：
- $V$：节点集合，包含三类节点——虚拟房屋节点（1个）、房间节点、家具节点；
- $E$：有类型标记的边集合，由五类关系构成：$E = E_{FF} \cup E_{FR} \cup E_{RR}^{adj} \cup E_{RR}^{far} \cup E_{RH}$，分别对应家具-家具全连接、家具-房间归属、相邻房间、远离房间、房间-房屋隶属关系；
- $T_V$ 与 $T_E$：节点类型与边类型的标记集合；
- $X_V$ 与 $X_E$：节点与边的特征矩阵。

每个节点 $u$ 的特征向量由类别、几何和形状信息拼接而成：

$$\mathbf{x}_u = [c; \mathbf{b}; o; \mathbf{s}]$$

其中 $c$ 为语义类别编码，$\mathbf{b} \in \mathbb{R}^6$ 为包围盒参数，$o$ 为离散化的朝向角，$\mathbf{s}$ 为预训练的形状潜在编码。这一表示在 §3.1 中定义，是整个管线统一处理房间级和家具级信息的核心载体。

### 异构图注意力网络（HetGAT）

图神经网络骨架是 Nestwork 的核心计算模块，用于编码器、解码器和扩散去噪器中的消息传递。该骨架以标准 GAT 为基础，融合了 EGAT 的边特征注意力机制和 HEAT 的异构图类型特定变换，形成**异构图注意力网络（HetGAT）**。

在第 $l$ 层中，对于节点 $u$ 和其邻居 $v$，注意力头 $h$ 的原始分数计算为：

$$s_{uv,h}^{(l)} = \text{LeakyReLU}\left( \mathbf{q}_h^\top \left[ \mathbf{h}_u^{(l)} \| \mathbf{h}_v^{(l)} \| \mathbf{e}_{uv}^{(l)} \right] \right)$$

其中 $\mathbf{h}_u^{(l)}$、$\mathbf{h}_v^{(l)}$ 分别为节点 $u$、$v$ 在第 $l$ 层的隐藏状态，$\mathbf{e}_{uv}^{(l)}$ 为边 $(u,v)$ 的特征嵌入，$\|$ 表示向量拼接，$\mathbf{q}_h$ 为可学习的注意力查询向量。注意力权重通过 softmax 归一化得到：$\alpha_{uv,h}^{(l)} = \frac{\exp(s_{uv,h}^{(l)})}{\sum_{k \in \mathcal{N}(u)} \exp(s_{uk,h}^{(l)})}$。

节点 $u$ 的多头聚合更新公式为：

$$\mathbf{h}_u^{(l+1)} = \big\|_{h=1}^H \sigma\left( \sum_{v \in \mathcal{N}(u)} \alpha_{uv,h}^{(l)} \mathbf{W}_h \left[ \mathbf{h}_v^{(l)} \| \mathbf{e}_{uv}^{(l)} \right] \right)$$

其中 $H$ 为注意力头数，$\mathbf{W}_h$ 为头 $h$ 的线性变换矩阵，$\sigma$ 为非线性激活函数。这一设计使模型能够同时感知节点类型差异和边所携带的空间关系信息，在 §3.2 中详细阐述，并在 Table 2 的消融实验中证明了其相较于同质 GCN/GAT 变体的显著优势。

### 低秩关系场（LRF）

在解码阶段，由于扩散生成的是节点潜在变量而非原始边特征，模型需要一个机制来重建边嵌入以支持 HetGAT 的消息传递。**低秩关系场（Low-Rank Relational Field, LRF）** 正是为此设计的关键模块——它直接从节点潜在变量推断几何关系，无需依赖地面真值边特征。

LRF 的核心思想是将边关系建模为一组可学习的“关系槽”（relational slots），并通过节点对注意力分配的低秩分解来生成边嵌入：

$$\tilde{\mathbf{e}}_{uv} := \text{MLP}\left( \left[ \mathbf{a}_u \| \mathbf{b}_v \| \boldsymbol{\alpha}_u^\top \boldsymbol{\alpha}_v \boldsymbol{\alpha} \right] \right)$$

其中 $\mathbf{a}_u$、$\mathbf{b}_v$ 为节点 $u$、$v$ 的潜在变量经线性投影后的表示，$\boldsymbol{\alpha}_u$、$\boldsymbol{\alpha}_v$ 分别为两节点对关系槽的注意力分配向量，$\boldsymbol{\alpha}$ 为全局槽权重，其内积 $\boldsymbol{\alpha}_u^\top \boldsymbol{\alpha}_v \boldsymbol{\alpha}$ 实现了低秩分解。该模块由 LRF 监督损失 $\mathcal{L}_{\text{LRF}}$ 驱动，权重 $\lambda_{\text{LRF}}=0.1$。

Table 5 的消融实验显示，移除 LRF 后碰撞率从 10.91% 飙升至 21.54%，Walkability 和 FID 均显著恶化，验证了 LRF 提供的几何先验对生成质量不可或缺。

### 自编码器训练目标

整个无条件自编码器的训练采用 VAE 框架，总损失函数为：

$$\mathcal{L} = \mathcal{L}_{\text{rec}} + \lambda_{\text{KL}} \mathcal{L}_{\text{KL}} + \lambda_{\text{LRF}} \mathcal{L}_{\text{LRF}}$$

其中 $\lambda_{\text{KL}} = 10^{-4}$，$\lambda_{\text{LRF}} = 0.1$。重构损失进一步分解为四项：

$$\mathcal{L}_{\text{rec}} = \mathcal{L}_{\text{box}} + \mathcal{L}_{\text{ang}} + \mathcal{L}_{\text{sem}} + \mathcal{L}_{\text{shp}}$$

分别对应包围盒回归、朝向分类、语义类别预测和形状编码重建。这一多任务训练目标确保编码器将异构图压缩为紧凑的 128 维潜在变量，同时保留几何与语义信息。

### 潜在扩散过程

在潜在空间中，扩散模型以前向加噪和反向去噪的方式学习先验分布。前向过程采用线性噪声计划：

$$Z_t = \sqrt{\bar{\alpha}_t} Z + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

其中 $Z$ 为编码器输出的节点潜在变量，$\bar{\alpha}_t$ 为累积噪声系数，$t$ 为扩散时间步。

条件扩散的训练目标为：

$$\mathcal{L}_{\text{LD}}^{\text{cond}}(\theta) = \mathbb{E}_{G, t, \epsilon} \left[ \left\| \epsilon_\theta(G_t, t, \tilde{G}_{\text{sem}}, \mathbf{g}) - \epsilon \right\|_2^2 \right]$$

其中 $\epsilon_\theta$ 为时间条件化的 HetGAT 去噪器，$G_t$ 为加噪后的图状态，$\tilde{G}_{\text{sem}}$ 为经随机掩蔽的语义条件图，$\mathbf{g}$ 为图级全局嵌入（包含房屋包围盒和可选的文本描述嵌入）。训练时采用 50% 随机掩蔽策略，使单一模型能适应从仅拓扑到全语义图的多种条件强度（见 Table 3）。

条件注入通过节点级交叉注意力实现残差更新：

$$\mathbf{z}_u^{(t)} \gets \mathbf{z}_u^{(t)} + \alpha_{\text{ca}} (\mathbf{c}_u + \mathbf{g})$$

其中 $\mathbf{c}_u$ 为节点 $u$ 的语义条件嵌入，$\mathbf{g}$ 为全局上下文嵌入，$\alpha_{\text{ca}}$ 为可学习的缩放因子。Table 5 显示，将交叉注意力替换为简单特征注入会导致 FID 从 7.26 骤升至 76.35，验证了拓扑感知条件化机制的必要性。



## 实验与关键发现

### 核心瓶颈验证：统一建模 vs. 两阶段拆分

论文首先通过对比统一单次生成与经典的两阶段方案，验证了联合推理房间结构与家具布局的必要性。两阶段基线先独立生成各房间的家具布局，再将其组合为完整房屋，缺乏对房间间空间关系的全局感知。如 **Table 1** 所示，Nestwork 在保真度指标上取得压倒性优势：FID 从 41.90 降至 7.26（降幅达 82.7%），KID（×100）从 2.97 降至 0.26。结构满意度（Graph satisfaction）从 78.60% 提升至 91.91%，说明统一模型能更好地遵循输入图的拓扑约束。值得注意的是，碰撞率（Collision）从 9.84% 微升至 10.91%，仍接近地面真值的 9.80%，表明联合推理并未以牺牲物理可行性为代价。**Figure 4** 的俯视布局着色对比直观展示了 Nestwork 在房间连通性和家具摆放合理性上的优势。

![[assets/figures/papers/paper_list_l2552_https_openaccess_thecvf_com_content_CVPR2026_html_Miao_Nestwork_Conditio/figures/004_Table_1.jpg]]
*Table 1: Unified one-pass vs. two-stage generation. Numbers report mean ± std over three random seeds. Graph/Coll./Walk. are percentages; lower is better for FID, KID, Coll. and KL divergence. (HG-FRONT GT collision baseline 9.80%)*

![[assets/figures/papers/paper_list_l2552_https_openaccess_thecvf_com_content_CVPR2026_html_Miao_Nestwork_Conditio/figures/005_Figure_4.jpg]]
*Figure 4: Color-coded top-down layouts from our method (top) and the two-stage baseline*

### 图自编码器骨架消融

为验证异构图注意力网络（HetGAT）的设计选择，论文在相同全语义图条件下对比了多种图神经网络骨架（**Table 2**）。实验表明，HetGAT 在所有指标上均优于同质 GCN、标准 GAT 及 Transformer 变体，尤其在 FID 和结构满意度上优势显著——相比 GCN，FID 降幅超过 50%。这验证了类型感知的消息传递对异构图建模的关键作用：不同节点类型（房屋、房间、家具）和边类型（家具-家具、家具-房间、房间-房间等）需要独立的变换矩阵来捕捉其特有的空间语义。

![[assets/figures/papers/paper_list_l2552_https_openaccess_thecvf_com_content_CVPR2026_html_Miao_Nestwork_Conditio/figures/006_Table_2.jpg]]
*Table 2: Autoencoder backbone comparison. All variants are evaluated under full semantic graph conditioning. Diversity metrics (Size/Loc./Angle) are computed over 10 samples per input*

### 潜在先验模块消融

**Table 4** 对比了三种潜在先验建模策略：独立同分布（IID）先验、自回归（AR）先验和扩散先验。在 IID 先验下，模型简单地假设各节点潜在变量相互独立，FID 高达 85.91；AR 先验引入顺序依赖，FID 降至 51.60，但仍远逊于扩散先验的 7.13。这一差距表明，房屋布局中节点间的空间关系是高度耦合的，需要扩散模型的迭代去噪过程来逐步协调全局一致性。

### 关键模块消融：低秩关系场与拓扑感知条件化

**Table 5** 揭示了两个核心模块的贡献：

- **移除低秩关系场（LRF）**：碰撞率从 10.91% 飙升至 21.54%，Walkability 和 FID 同步恶化。LRF 在解码阶段从节点潜在变量直接预测边嵌入，为解码器提供几何关系先验。缺少这一模块时，模型无法有效推断家具间、家具与房间间的空间约束，导致大量穿透和错位。

- **将交叉注意力替换为简单特征注入**：FID 从 7.26 升至 76.35，KID 从 0.26 升至 5.87，性能几乎退化至无条件生成水平。这验证了拓扑感知条件化的必要性：随机掩蔽交叉注意力机制能够根据已知节点的语义信息，有选择地引导未知节点的生成，而简单注入则无法区分条件信息的来源和范围。

### 多模式条件生成能力

**Table 3** 展示了同一扩散模型在四种条件化模式下的表现：仅拓扑（topology-only）、拓扑+房间语义、拓扑+房间+家具语义、以及全语义图。随着条件信息增加，FID 从 23.34 单调下降至 7.26，结构满意度从 78.76% 提升至 91.91%。这验证了随机掩蔽训练策略的有效性——单一模型无需重新训练即可适应不同粒度的条件输入。**Figure 5** 的布局对比进一步表明，即使仅给定房间拓扑，模型也能生成合理的家具布局；随着条件细化，生成结果逐渐收敛至特定配置。

### 局限性与失败模式

尽管 Nestwork 在整体指标上表现优异，仍存在以下不足：

1. **碰撞率仍略高于真值**：最优模型的碰撞率（10.91%）未能低于地面真值的 9.80%，说明模型在精细几何约束上仍有改进空间。当前方法未显式强制执行物理可行性约束，碰撞仅通过数据驱动的方式隐式学习。

2. **低秩关系场的泛化边界**：LRF 依赖低秩分解来近似边嵌入，对训练分布内的房屋结构表现良好，但面对极端或不常见的房间拓扑时，关系场的外推能力可能不足。这一局限性在论文中未被定量评估，需要手动验证。

3. **自然语言接口的语义歧义**：虽然论文展示了基于提示词摘要嵌入的自然语言交互（**Figure 1**），但该接口受限于预定义的语义映射，复杂描述（如“L型沙发靠窗放置”）可能无法准确转化为图条件，实际可用性需要进一步用户研究确认。

![[assets/figures/papers/paper_list_l2552_https_openaccess_thecvf_com_content_CVPR2026_html_Miao_Nestwork_Conditio/figures/001_Figure_1.jpg]]
*Figure 1: Flexible graph conditioning and natural-language interface*

### 开放问题

论文在结尾提出了若干值得探索的方向：如何显式地强制执行功能合理性和无阻碍的流通路径（walkability）？能否将方法拓展到动态场景或交互式编辑，支持用户逐步细化布局？未来工作可考虑引入物理仿真反馈作为额外的监督信号，以优化布局的稳定性和可用性。

### 补充图表

![[assets/figures/papers/paper_list_l2552_https_openaccess_thecvf_com_content_CVPR2026_html_Miao_Nestwork_Conditio/figures/007_Table_3.jpg]]
*Table 3: Conditional generation. The same diffusion model is evaluated under four conditioning modes*

![[assets/figures/papers/paper_list_l2552_https_openaccess_thecvf_com_content_CVPR2026_html_Miao_Nestwork_Conditio/figures/008_Table_4.jpg]]
*Table 4: Latent–prior ablation*

![[assets/figures/papers/paper_list_l2552_https_openaccess_thecvf_com_content_CVPR2026_html_Miao_Nestwork_Conditio/figures/009_Figure_5.jpg]]
*Figure 5: Comparison of generated layouts across four conditioning modes applied to the same house graph*

![[assets/figures/papers/paper_list_l2552_https_openaccess_thecvf_com_content_CVPR2026_html_Miao_Nestwork_Conditio/figures/003_Figure_3.jpg]]
*Figure 3: Post-processing pipeline*



## 定位与知识库关联

### 问题定位：从拆分式生成到统一联合推理

现有3D房屋布局生成方法大多沿袭一条拆分式流水线：先独立生成房间级家具布局，再将其拼装为完整房屋。这类两阶段方案（如本文构造的 room-level VAE + house-level layout 基线）的**核心瓶颈**在于缺乏对房间结构与家具摆放的联合推理——房间边界与家具位置在生成过程中彼此解耦，导致空间不一致和误差累积。在 HG-FRONT 数据集上，该两阶段基线的 FID 高达 41.90，结构满意度仅 78.60%，直观反映了拆分式范式的上限。

Nestwork 的方法论转向在于**将整个房屋建模为单一异构图**，在统一潜在空间中同时处理房间邻接关系与家具布局，从而将“先拆后合”的级联误差转化为“端到端联合去噪”的协同优化。这一转向在定量上表现为 FID 从 41.90 骤降至 7.26（Table 1），结构满意度提升至 91.91%。

### 方法谱系：图生成、异构图网络与潜在扩散的交汇

Nestwork 处于三条技术脉络的交汇点：

**1. 图生成与场景图到布局**

场景图到布局生成（scene-graph-to-layout）的工作通常将物体关系建模为同质图或序列，再通过 GAN、Transformer 或自回归模型生成2D/3D布局。Nestwork 继承了“图到布局”的范式，但将图结构从同质物体关系图拓展为包含房间、家具和五类空间关系的**异质房屋图**，并首次在3D房屋尺度上进行潜在扩散生成。

**2. 异构图神经网络**

在编码器-解码器骨干选择上，Nestwork 采用 **HetGAT**——融合了 GAT 的注意力机制、EGAT 的边特征感知以及 HEAT 的类型特定变换。消融实验（Table 2）表明，相比同质 GCN、GAT 和 EGAT 变体，HetGAT 在所有保真度与结构指标上均占优，FID 降幅超过 50%。这一优势源于类型感知的消息传递能够区分房间-房间、家具-家具、家具-房间等不同语义通道，避免同质聚合造成的信息混淆。

**3. 潜在扩散模型**

Nestwork 将扩散过程从原始数据空间迁移到图自编码器的潜在空间，采用时间条件化的 HetGAT 作为去噪器。这继承了 LDM（Latent Diffusion Models）的核心思想，但将其适配到图结构数据。关键创新在于**随机掩蔽语义图条件化**：训练时以 50% 概率随机掩蔽节点语义标签，使单一扩散模型能够适应从仅拓扑条件到全语义条件的四种模式，无需重新训练（Table 3）。

### 关键技术决策及其证据强度

| 设计选择 | 替代方案 | 证据强度 | 关键发现 |
|---------|---------|---------|---------|
| 异构图统一建模 | 两阶段拆分式 | ★★★ Table 1 | FID 降低 82.7%，结构满意度提升 13.3pp |
| HetGAT 骨干 | 同质 GCN/GAT | ★★★ Table 2 | 所有指标一致占优，FID 降幅 >50% |
| 低秩关系场 (LRF) | 无 LRF / 依赖真值边 | ★★★ Table 5 | 移除 LRF 后碰撞率升至 21.54%（接近翻倍） |
| 掩蔽交叉注意力条件化 | 简单特征注入 | ★★★ Table 5 | 替换后 FID 升至 76.35，KID 升至 5.87 |
| 扩散先验 | IID / 自回归先验 | ★★★ Table 4 | FID 从 85.91/51.60 降至 7.13 |

**低秩关系场（LRF）** 是连接编码器与解码器的关键桥梁。在推理阶段，解码器无法获取地面真值几何边特征，LRF 通过节点潜在变量的低秩分解直接预测边嵌入，为解码器提供几何关系先验。移除 LRF 后碰撞率从 10.91% 升至 21.54%，Walkability 和 FID 同步恶化，证明这一模块在补偿缺失几何信息上的不可替代性。

**掩蔽交叉注意力** 的设计同样值得关注。简单地将条件信息注入潜在变量（而非通过拓扑感知的交叉注意力）会导致性能崩溃（FID 76.35 vs 7.26），说明条件信号必须与图拓扑结构对齐才能有效引导去噪过程。

### 适用边界与局限

尽管 Nestwork 在统一生成范式上取得了显著进展，其适用边界受以下因素制约：

1. **碰撞约束的软性处理**：当前碰撞率（10.91%）仍略高于数据集地面真值（9.80%），且模型未显式强制执行物理可行性约束。生成布局的碰撞问题通过后处理管线缓解，而非在生成过程中硬约束。

2. **低秩关系场的泛化能力**：LRF 依赖函数近似从节点潜在变量推断边嵌入，对于训练分布之外的极端房屋结构（如非矩形房间、多层建筑），其推断精度可能下降。这一局限在论文中未被系统验证。

3. **自然语言接口的语义覆盖**：文本条件化依赖于预定义的语义映射，复杂或模糊的自然语言描述可能导致歧义。该接口的鲁棒性未经过大规模用户研究验证。

4. **静态场景假设**：当前方法生成的是静态房屋布局快照，未考虑动态场景（如可移动家具）或交互式编辑需求。

### 开放问题与未来方向

论文明确指出的开放问题包括：

- **功能合理性的显式约束**：如何在生成过程中强制执行无阻碍的流通路径和功能区域划分？这可能需要引入可达性分析或物理仿真反馈。
- **动态与交互式拓展**：方法能否扩展到支持用户交互式编辑、增量式布局更新或时序场景生成？
- **物理仿真闭环**：未来工作可探索将物理仿真（如碰撞检测、稳定性分析）嵌入生成循环，以优化布局的物理可行性。

从更宏观的视角看，Nestwork 的异构图扩散范式为“结构感知的条件生成”提供了可复用的技术模板——类型感知的消息传递、低秩关系场补偿、随机掩蔽条件化这三项设计决策，有望迁移到其他需要联合推理异构实体及其空间关系的生成任务中。



## 原文 PDF

![[paperPDFs/CVPR_2026/Nestwork_Conditional_3D_Furnished_House_Layout_Generation_through_Latent_Heterogeneous_Graph_Diffusion.pdf]]
