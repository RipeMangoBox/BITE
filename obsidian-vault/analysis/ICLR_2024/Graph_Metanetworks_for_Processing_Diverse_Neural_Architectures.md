---
title: "Graph Metanetworks for Processing Diverse Neural Architectures"
type: paper
paper_level: A
venue: ICLR
year: 2024
pdf_ref: paperPDFs/ICLR_2024/Graph_Metanetworks_for_Processing_Diverse_Neural_Architectures.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/GMN/
aliases:
- GMG
- GMPDNA
tags:
- ICLR_2024
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning
core_operator: "将神经网络参数表示为参数图，并利用图神经网络（GNN）进行消息传递。"
primary_logic: "图自同构（Neural DAG Automorphisms）统一刻画了前馈神经网络参数空间中的置换对称性，而图神经网络天然等变于这些图自同构，从而可以构建通用且等变的元网络。"
claims:
- "紧凑的参数图表示可以处理参数共享层（如卷积和注意力），且不会随激活数量而缩放。"
- "任何神经DAG自同构排列参数不会改变网络函数。"
- "图元网络等变于由神经DAG自同构诱导的参数置换。"
- "GMN在多样化架构和不同数据设置下均显著优于DeepSets和DMC基线。"
---

# Graph Metanetworks for Processing Diverse Neural Architectures

> [!tip] 核心洞察
> 图自同构（Neural DAG Automorphisms）统一刻画了前馈神经网络参数空间中的置换对称性，而图神经网络天然等变于这些图自同构，从而可以构建通用且等变的元网络。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 图元网络: 处理多样化神经架构 |
| 英文题名 | Graph Metanetworks for Processing Diverse Neural Architectures |
| 会议/期刊 | ICLR 2024 |
| Links | [paper](https://arxiv.org/abs/2312.04501); [Project](https://research.nvidia.com/labs/toronto-ai/GMN/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/transfer_multitask_and_meta_learning |
| Method | Graph Metanetworks (GMNs) |
| Dataset | Varying CNNs (100% data), Diverse Architectures (100% data), Varying CNNs (OOD), Diverse Architectures (10% data) |

> [!tip] 效果简介
> - Varying CNNs (100% data) 上，R^2 为 0.978 ± 0.002，对比 0.948 ± 0.009 (DMC), 0.778 ± 0.002 (DeepSets)，变化 +0.030 (vs DMC)。
> - Diverse Architectures (100% data) 上，R^2 为 0.975 ± 0.002，对比 0.957 ± 0.009 (DMC), 0.562 ± 0.020 (DeepSets)，变化 +0.018 (vs DMC)。
> - Varying CNNs (OOD) 上，R^2 为 0.891 ± 0.037，对比 0.741 ± 0.015 (DeepSets), 0.387 ± 0.229 (DMC)，变化 +0.15 (vs DeepSets)。

## 概述

**核心问题**：元网络（metanetworks）——即以神经网络参数为输入并对其进行推理的神经网络——面临一个根本性瓶颈：现有等变元网络需要针对每种输入架构手工设计等变层，难以泛化到包含归一化层、残差连接、注意力等模块的复杂网络。当输入网络架构多样化时，手工设计的等变结构迅速失效，迫使研究者要么放弃对称性保证，要么将方法局限在简单MLP或CNN上。

**核心洞察**：本文提出，前馈神经网络参数空间中的置换对称性可以被统一刻画为**神经DAG自同构**（Neural DAG Automorphisms）——即保持邻接关系、节点类型和权重共享约束的有向无环图自同构。在此框架下，图神经网络天然等变于这些图自同构，从而无需手工设计即可构建通用且等变的元网络。

**方法定位**：该方法名为**图元网络**（Graph Metanetworks, GMN），其核心创新在于用**参数图**（parameter graph）表示输入神经网络——每个参数对应图中一条边，并通过引入偏置节点、归一化节点等结构捕获各类层的拓扑与对称性。这与将参数视为扁平向量（如DeepSets, DMC）或仅在计算图上建模（导致参数共享层产生大量冗余边）的先前方法形成根本区别。GMN处于元学习、图神经网络和等变深度学习三者的交叉点，在方法谱系上属于**基于图结构编码的通用等变元网络**。

**主要结果**：
- 在CIFAR-10分类器准确率预测任务上，GMN在所有六种数据设置下均显著优于DeepSets和DMC基线：全数据设置下R²达0.975–0.978，低数据（10%）设置下优势扩大（+0.108 vs DMC），分布外（OOD）设置下优势最为显著（+0.15 vs DeepSets）。
- 在2D INR编辑任务上，GMN在Contrast编辑上与NFT持平，在Dilate编辑上略逊于NFT但优于NFN-NP。
- 在神经网络表征自监督学习任务上，GMN的测试MSE为1.13，优于DWSNet的1.37。
- 在小CNN数据集上，GMN同样超越所有先前元网络（Test τ = 0.938）。

**局限性**：网络函数不变性的理论证明目前仅在计算图上严格成立，推广到参数图自同构仍为猜想；方法尚未扩展到循环架构或动态计算图；参数图的构建依赖人工设计的子图模板，每新增一种层类型需要定义新的构造规则。

## 背景与动机

### 元网络的核心任务与瓶颈

元网络（metanetworks）旨在以神经网络自身的参数或架构为输入，预测其性能、生成参数更新或提取表征。这类方法在神经架构搜索、超参数优化、持续学习等场景中具有广泛应用。然而，元网络的设计面临一个根本性瓶颈：**神经网络的参数空间存在复杂的置换对称性**——对隐藏层神经元进行重排不会改变网络所表示的函数，但会彻底改变参数的坐标表示。一个有效的元网络必须对这种对称性保持等变（equivariant）或不变（invariant），否则同一函数的不同参数化将产生不同输出，导致严重的泛化失败。

### 现有方法的缺口

围绕这一瓶颈，现有方法可分为三条路线，但各自存在显著局限：

**手工设计等变层。** 以 **NFN-HNP / NFN-NP**（Zhou et al., 2023a）、**NFT**（Zhou et al., 2023b）和 **DWSNet**（Navon et al., 2023）为代表，这些方法针对多层感知机（MLP）和简单卷积网络，手工推导了参数置换下的等变线性层。其核心机制是对权重矩阵的行、列和全局统计量施加受约束的线性组合（如 NFN 的权重更新公式）。然而，这种手工设计每新增一种层类型（如归一化层、残差连接、注意力机制）就需要重新推导等变形式，**难以泛化到包含多样化模块的现代架构**。

**忽略对称性。** **DMC**（Deep Meta Classifier，Eilertsen et al., 2020）将网络参数向量化后直接输入 1D CNN，**StatNN**（Unterthiner et al., 2020）则仅使用参数的均值、方差等统计量。这些方法可以处理不同规模的网络，但因未显式建模置换对称性，在数据稀缺或分布外（OOD）场景下泛化能力严重受限。

**将参数视为集合。** **DeepSets**（Zaheer et al., NeurIPS 2017）将参数视为无序集合，利用对置换天然不变的集合架构进行处理。虽然保证了对称性，但完全丢弃了参数间的结构关系（如层内连接、层间依赖），表达性受到根本限制。

### 计算图表示的困境

一种直观的思路是将神经网络表示为**计算图**（computation graph），以激活值为节点、参数为边，然后利用图神经网络（GNN）处理。然而，计算图存在致命缺陷：对于参数共享层（如卷积和注意力），同一参数会出现在成百上千条边中。如 Figure 2 所示，一个仅有 2×2 卷积核的单层网络，在处理 4×4 输入时产生 16 条边却仅对应 4 个参数。这种冗余导致图规模随激活数量而非参数数量缩放，在深层网络中变得完全不可行。

### 本文的核心动机

本文的核心观察是：**图自同构（Neural DAG Automorphisms）统一刻画了前馈神经网络参数空间中的置换对称性**，而图神经网络天然等变于其输入图的自同构群。这意味着，如果能将神经网络紧凑地表示为一张“参数图”，使得参数置换恰好对应图上的自同构变换，那么任何在其上运行的 GNN 都将自动获得所需的等变性——无需针对每种架构手工设计等变层。

基于这一洞察，本文提出 **图元网络（Graph Metanetworks, GMNs）**，其关键贡献在于：

1. **紧凑的参数图表示**：为每个参数分配一条边，通过引入偏置节点、归一化节点等辅助结构捕获层类型信息，使图规模仅随参数量而非激活量缩放，天然支持参数共享层。
2. **通用等变性**：通过神经 DAG 自同构的形式化定义（Proposition 1），证明 GNN 对参数置换天然等变（Proposition 2），从而构建一个可处理任意前馈架构的通用元网络框架。
3. **无需手工设计**：将等变性的保证从手工层设计转移至图结构本身，新增层类型只需定义其参数子图模板，GNN 自动继承等变性。

## 核心创新

### 创新动机：现有元网络的对称性瓶颈

元网络（metanetwork）的核心任务是接收一个训练好的神经网络作为输入，输出该网络的属性预测或参数编辑。然而，神经网络参数空间中存在大量的置换对称性——例如，交换一个隐藏层的两个神经元并相应调整前后层权重，网络函数完全不变。一个理想的元网络应当天然**等变**（equivariant）于这些对称性，即输入参数被合法置换时，输出应以可预测的方式变换（对于标量预测则为不变）。

现有方法在处理这一对称性时面临根本性困难：

- **手工设计等变层的局限**：**NFN-HNP / NFN-NP / NFN-PT**（Zhou et al., 2023a）和**NFT**（Zhou et al., 2023b）等方法通过精心构造参数置换等变线性层或注意力层来保证对称性，但这些设计紧密耦合于特定架构（如简单MLP或CNN），每遇到新的层类型（归一化层、残差连接、注意力机制）就需要重新推导等变条件，难以泛化。

- **忽略对称性的妥协**：**DMC**（Eilertsen et al., 2020）将参数向量化后用1D CNN处理，可适应不同大小的网络，但完全未显式保证对称性；**StatNN**（Unterthiner et al., 2020）仅使用参数统计量（均值、方差等），表达力严重受限。

- **集合视角的表达力不足**：**DeepSets**（Zaheer et al., NeurIPS 2017）将参数视为无序集合，天然保证置换不变性，但完全丢弃了参数之间的拓扑关系（哪两个参数属于同一层、谁与谁通过残差连接交互），导致在复杂架构上表现急剧退化。

**核心瓶颈**（来自分析）：*现有等变元网络需要针对每种输入架构手工设计等变层，难以泛化到包含归一化层、残差连接、注意力等模块的复杂网络。*

### 核心洞察：图自同构统一刻画置换对称性

本文的关键洞察是：**前馈神经网络可以表示为有向无环图（DAG），而参数空间中的置换对称性恰好对应于图的某种结构保持自同构（neural DAG automorphisms）。** 一旦将网络参数编码为图的边，图神经网络（GNN）天然等变于图自同构——因为GNN的消息传递仅依赖图的连接结构，当节点被合法置换时，消息传递的结果以可预测的方式变换。

这一洞察将元网络设计问题转化为**图表示学习问题**：不需要为每种层类型手工设计等变层，只需为每种层类型设计合适的参数子图构造规则，随后即可直接应用任意标准GNN（消息传递网络或图Transformer）进行处理。

### 关键创新点（Changed Slots）

#### 创新一：从扁平向量/集合到参数图（网络表示形式）

| 对比维度 | 基线方法 | GMN方法 |
|---------|---------|---------|
| 表示形式 | 扁平参数向量（DMC）或参数集合（DeepSets） | 参数图：每个参数对应一条边，神经元对应节点 |
| 拓扑信息 | 完全丢失 | 通过图结构完整保留层间连接、残差连接等 |
| 参数共享 | 无法表示或需冗余计算图 | 通过多层并行边紧凑表示（见创新三） |
| 对称性来源 | 需手工编码 | 由图的连接模式自然决定 |

**证据锚点**：*"our technique's crux is representing an input neural network as a graph"*

参数图的核心设计原则是：**每个可学习参数恰好对应图中的一条边**。例如，线性层 $W \in \mathbb{R}^{d_{\text{out}} \times d_{\text{in}}}$ 被表示为 $d_{\text{out}}$ 个输出神经元节点与 $d_{\text{in}}$ 个输入神经元节点之间的全二分图，共 $d_{\text{out}} \times d_{\text{in}}$ 条边。偏置参数则编码为从偏置节点到各输出神经元的边，使得同层偏置之间可以通过GNN的消息传递相互通信（消融实验证实这比自环或节点特征编码更具表达力）。

#### 创新二：从手工等变层到GNN天然等变（对称性处理方式）

| 对比维度 | 基线方法 | GMN方法 |
|---------|---------|---------|
| 等变性保证 | 手工推导每层的等变条件（NFN系列） | GNN天然等变于图自同构 |
| 新架构扩展 | 需重新设计等变层 | 仅需定义新的参数子图构造 |
| 理论支撑 | 针对特定层类型的特设证明 | 统一的图自同构理论框架 |

**核心理论结果**（来自分析）：

> **命题1**：对于计算图的任何神经DAG自同构 $\phi$，神经网络函数保持不变：$\forall x \in X, f_\theta(x) = f_{\Phi(\theta)}(x)$

> **命题2**：图元网络等变于由神经DAG自同构诱导的参数置换。

**证据锚点**：*"GNNs acting on these DAGs are equivariant to their permutation symmetries"*

神经DAG自同构定义为保持邻接关系、节点类型和权重共享约束的节点置换。例如，对于线性层，可以独立置换输入神经元和输出神经元（同时相应调整权重矩阵的行和列）；对于卷积层，可以在通道维度上置换（同时置换滤波器的输入/输出通道维度）；对于残差块，置换必须同时作用于主路径和跳跃连接的两端。Figure 4 可视化了这些自同构的具体形式。

#### 创新三：紧凑参数图处理参数共享层（参数共享层处理）

| 对比维度 | 基线方法 | GMN方法 |
|---------|---------|---------|
| 卷积层表示 | 计算图需为每个滑动窗口位置创建独立边（大量冗余） | 每个滤波器参数仅对应一条边，通过位置编码区分 |
| 注意力层 | 难以用传统计算图表示权重共享 | 将Q/K/V投影矩阵分别表示为参数子图 |
| 规模依赖 | 边数随激活图尺寸增长 | 边数仅取决于参数数量，与激活数量无关 |

**证据锚点**：*"compact parameter graph representation... allows us to handle parameter-sharing layers like convolutions and attention layers without scaling with the activation count"*

这是区别于传统计算图表示的关键突破。如图 Figure 2 所示，一个简单的 $2 \times 2$ 卷积在 $4 \times 4$ 输入上，计算图需要16条边来表示仅4个参数。而参数图为每个滤波器参数仅创建一条边，通过边特征中的位置编码（如滤波器内的相对坐标）来区分同一参数在不同滑动窗口位置的作用。这使得图元网络可以高效处理包含大量参数共享的现代架构（如深度可分离卷积、多头注意力），而不会因激活图尺寸膨胀。

### 方法管线总览

GMN的处理管线由三个模块组成：

1. **参数图构建**：自动将PyTorch模型定义转换为参数图，每层类型使用预定义的子图模板（线性层、卷积、注意力、残差、归一化等），为节点和边添加层索引、方向、位置编码等不变特征。

2. **GNN消息传递**：在参数图上运行消息传递GNN（或图Transformer），同时更新节点特征、边特征和全局特征。通用更新形式为：
   - 节点更新：$v_i \leftarrow \mathrm{MLP}_2^v(v_i, \sum_{j, e_{(i,j)}\in E} \mathrm{MLP}_1^v(v_i, v_j, e_{(i,j)}, u), u)$
   - 边更新：$e_{(i,j)} \leftarrow \mathrm{MLP}^e(v_i, v_j, e_{(i,j)}, u)$
   - 全局更新：$u \leftarrow \mathrm{MLP}^u(\sum_i v_i, \sum_{e\in E} e, u)$

3. **下游预测头**：根据任务类型，对边特征进行平均池化得到固定长度表示（网络级预测，如准确率预测），或直接使用最终边特征（参数级预测，如权重编辑），接MLP输出最终结果。

### 创新边界与局限

尽管GMN在统一性和泛化性上取得了显著突破，仍需注意以下边界：

- **理论完备性**：Proposition 1的严格证明目前仅针对计算图给出，扩展到参数图自同构（包括多重图情形）的完整证明仍是一个猜想（见附录B.5），需要进一步验证。

- **架构覆盖范围**：当前方法仅适用于前馈神经网络，尚未扩展到循环架构或动态计算图。参数图的构造依赖人工设计的子图模板，每新增一种层类型需要定义新的构造规则。

- **非置换对称性**：未处理ReLU网络的缩放对称性（对权重和偏置的尺度变换会改变网络输出），这类对称性需要额外机制来保证等变性。

## 整体框架

图元网络（Graph Metanetworks, GMNs）的整体框架遵循一个清晰的三阶段流水线：**参数图构建 → GNN消息传递 → 下游预测**。其核心设计理念是将任意前馈神经网络转化为一种称为“参数图”的紧凑图表示，从而将元学习问题转化为图学习问题。

### 流水线总览

**阶段一：参数图构建。** 给定一个用PyTorch定义的输入神经网络，系统自动将其转换为参数图。参数图的关键设计原则是：每个可学习参数对应图中恰好一条边，而神经元（或功能单元）对应节点。这种设计使得图的规模仅随参数数量线性增长，而非随激活数量增长——这是相较于传统计算图的核心优势。具体而言，线性层的权重矩阵 $W$ 被表示为从前一层神经元节点到后一层神经元节点的有向边；偏置参数则通过引入每层的偏置节点，以从偏置节点到对应神经元的边来编码；批归一化参数同样通过额外的节点和边纳入图中。对于卷积层、注意力层等参数共享层，参数图通过多层并行边来捕获权重共享信息，避免了计算图中因展开卷积操作而产生的大量冗余边。残差连接虽不引入新参数，但会改变参数空间的置换对称性，因此在图中以无参数的虚线边显式表示。

**阶段二：GNN消息传递。** 构建完成的参数图被送入图神经网络进行处理。GMN采用通用的消息传递框架，在每一层中同时更新节点特征、边特征和全局特征：

- **节点更新**：$$v_i \leftarrow \mathrm{MLP}_2^v(v_i, \sum_{j, e_{(i,j)}\in E_{(i,j)}} \mathrm{MLP}_1^v(v_i, v_j, e_{(i,j)}, u), u)$$
- **边更新**：$$\pmb{e}_{(i,j)} \leftarrow \mathrm{MLP}^e(\pmb{v}_i, \pmb{v}_j, \pmb{e}_{(i,j)}, \pmb{u})$$
- **全局更新**：$$\pmb{u} \leftarrow \mathrm{MLP}^u(\sum_i \pmb{v}_i, \sum_{e\in E} e, \pmb{u})$$

在具体实验中，GMN可使用简单的消息传递GNN（不使用全局图特征），也可替换为图Transformer以获得更强的表达能力。节点和边的初始特征包含层索引、方向信息、位置编码等不变特征，这些特征在图自同构下保持不变，从而天然保证了GNN对参数置换的等变性。

**阶段三：下游预测。** 根据任务类型的不同，GMN采用两种预测方式：
- **网络级任务**（如预测分类器准确率）：对所有边特征进行平均池化，得到固定长度的图级表示，再通过MLP输出标量预测值。
- **参数级任务**（如INR权重编辑）：直接使用每条参数边对应的最终边特征 $e_{(i,j)}$ 作为该参数的预测输出。对于INR编辑任务，更新后的权重为 $\tilde{\theta} = \theta + \gamma \cdot \mathrm{Metanet}(\theta)$，其中 $\gamma$ 为可学习标量。

### 对称性保证的理论基础

GMN框架的等变性建立在**神经DAG自同构**这一核心概念之上。对于表示前馈神经网络的有向无环图，神经DAG自同构是保持邻接关系、节点类型和权重共享约束的节点置换。命题1指出，任何神经DAG自同构对参数的置换不会改变网络函数。由于GNN天然等变于图自同构，GMN因此天然等变于参数空间中的置换对称性，无需像NFN、NFT等先前方法那样为每种架构手工设计等变层。这一性质使得GMN能够统一处理包含归一化层、残差连接、注意力等模块的多样化架构，突破了现有等变元网络的泛化瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2312_04501/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Graph Metanetworks (GMNs) Our method converts neural network architectures into a parameter graph where edges correspond to network parameters. The bias (b) and batch-normalization parameters are incorporated via additional nodes with edges to the relevant layer’s neurons. The graph is processed by a graph neural network operating on edge attributes. Fixed-length (invariant) predictions can be extracted by pooling the output graph features*

## 核心模块与公式推导

### 模块一：参数图构建

GMN 的核心操作是将任意前馈神经网络转换为一种紧凑的**参数图**（parameter graph）。与传统的计算图不同，参数图的设计原则是**每个可学习参数恰好对应图中的一条边**，从而避免了因激活数量膨胀而导致的冗余边问题（Figure 2 展示了单卷积层计算图中参数被重复展开的问题）。

具体构建规则如下：

- **线性层**：权重矩阵 $W \in \mathbb{R}^{d_{\text{out}} \times d_{\text{in}}}$ 被表示为从 $d_{\text{in}}$ 个输入神经元节点到 $d_{\text{out}}$ 个输出神经元节点的完全二分图，每条边对应一个权重参数。
- **偏置参数**：为每层引入一个偏置节点（bias node），偏置参数编码为从该偏置节点到对应层神经元的边。这一设计允许同层不同偏置参数在消息传递中相互通信，比自环或节点特征编码更具表达力。
- **卷积层**：将卷积核的每个空间位置建模为一组参数边，通过**多层并行边**（multi-edges）来捕获参数共享——即同一个滤波器权重在不同空间位置被复用，但不为每个激活位置创建独立边，从而保持图规模与参数量而非激活量成正比。
- **残差连接**：残差连接本身不引入额外参数，但会改变参数空间的置换对称性。因此在参数图中以**无参数边**（虚线边）显式表示，确保图自同构能正确反映残差结构带来的对称性约束。
- **归一化层**：批归一化或层归一化的可学习参数（scale 和 shift）同样以边或节点形式嵌入参数图。

Figure 3 汇总了各类层对应的参数子图构造模板。整个转换过程可从 PyTorch 模型定义自动完成。

### 模块二：GNN 消息传递

构建好的参数图由一个通用的图神经网络处理。GMN 采用标准的消息传递框架，同时更新节点特征 $\mathbf{v}_i$、边特征 $\mathbf{e}_{(i,j)}$ 和全局特征 $\mathbf{u}$。每层 GNN 的计算由以下三个方程定义：

**节点更新**（Eq. 1）：

$$v_i \leftarrow \mathrm{MLP}_2^v\left(v_i, \sum_{j, e_{(i,j)}\in E_{(i,j)}} \mathrm{MLP}_1^v(v_i, v_j, e_{(i,j)}, u), u\right)$$

其中 $\mathrm{MLP}_1^v$ 为每条边计算消息（依赖于源节点、目标节点、边特征和全局特征），求和聚合所有入边消息，$\mathrm{MLP}_2^v$ 结合聚合消息与全局特征更新节点表示。

**边更新**（Eq. 2）：

$$\mathbf{e}_{(i,j)} \leftarrow \mathrm{MLP}^e(\mathbf{v}_i, \mathbf{v}_j, \mathbf{e}_{(i,j)}, \mathbf{u})$$

边特征直接根据其两端节点特征、自身当前特征和全局特征更新。由于参数图中的边直接对应网络参数，边特征是承载参数信息的关键载体。

**全局更新**（Eq. 3）：

$$\mathbf{u} \leftarrow \mathrm{MLP}^u\left(\sum_i \mathbf{v}_i, \sum_{e\in E} e, \mathbf{u}\right)$$

全局特征通过聚合所有节点特征和所有边特征来更新，为整个图提供全局上下文。

### 模块三：下游预测头

根据任务类型，GMN 采用不同的读出策略：

- **网络级任务**（如预测输入网络的 CIFAR-10 准确率）：对所有边特征进行**平均池化**，得到一个固定长度的图级表示，再送入 MLP 产生标量预测。论文实验中使用了不含全局特征 $\mathbf{u}$ 的简化 GNN，直接对边表示做均值池化。
- **参数级任务**（如 INR 编辑）：直接使用每条边经 GNN 处理后的最终特征 $\mathbf{e}_{(i,j)}$ 作为对应参数的预测输出。

对于 INR 编辑任务，参数更新方式为：

$$\tilde{\theta} = \theta + \gamma \cdot \mathrm{Metanet}(\theta)$$

其中 $\gamma$ 是一个可学习的标量，控制编辑步长；$\mathrm{Metanet}(\theta)$ 是 GMN 对每个参数产生的输出。

### 核心理论保证

GMN 的等变性建立在**神经 DAG 自同构**（Neural DAG Automorphisms）的概念之上。一个神经 DAG 自同构 $\phi$ 是参数图节点的一个置换，满足：(1) 保持邻接关系；(2) 保持节点类型（如输入神经元不能映射为隐藏神经元）；(3) 保持权重共享约束（如卷积层中共享同一滤波器的边必须同步置换）。

**命题 1**（网络函数不变性）：对于计算图的任意神经 DAG 自同构 $\phi$，神经网络函数保持不变：$\forall x \in \mathcal{X}, f_\theta(x) = f_{\Phi(\theta)}(x)$，其中 $\Phi(\theta)$ 表示按 $\phi$ 对参数进行相应置换。

**命题 2**（GNN 等变性）：图元网络等变于由神经 DAG 自同构诱导的参数置换。

这两个命题共同保证了：当输入网络的隐藏神经元被置换（一种不影响函数表达的对称操作）时，GMN 的输出会以可预测的方式同步变换，从而无需手工为每种架构设计等变层。需要注意的是，命题 1 的严格证明目前仅针对计算图给出，推广到一般参数图（含多重边）仍是一个开放猜想（见附录 B.5）。

## 实验与分析

### 核心实验设置

为系统验证图元网络（Graph Metanetworks, GMN）的有效性，作者构建了三个实验维度：**准确率预测**（网络级元任务）、**INR权重编辑**（参数级元任务）和**自监督表示学习**。实验覆盖了从简单CNN到包含残差连接、注意力机制的多样化架构，并在全量数据、低数据（10%）和分布外（OOD）三种数据设置下评估，以全面检验方法的泛化能力和数据效率。

在准确率预测任务中，训练集包含15 000个在CIFAR-10上训练好的输入网络。GMN采用简单的消息传递GNN（不使用全局图特征），通过对边表示进行均值池化获得不变预测。基线方法包括：**DMC**（Deep Meta Classifier, Eilertsen et al., 2020），将参数向量化后用1D CNN处理；**DeepSets**（Zaheer et al., NeurIPS 2017），将参数视为集合处理；以及在小CNN数据集上额外对比的**StatNN**（Unterthiner et al., 2020）。所有元网络的可训练参数量均控制在约75万，学习率通过验证集网格搜索选择，每个方法使用5个随机种子并报告均值和标准差。

### 准确率预测：全场景最优

Table 1汇总了主要实验结果。在Varying CNNs和Diverse Architectures两个数据集的所有数据设置下，GMN均取得最优R²和Kendall's τ。

**全量数据（100% data）**：在Varying CNNs上，GMN的R²达到0.978 ± 0.002，相比DMC（0.948 ± 0.009）提升3个百分点，相比DeepSets（0.778 ± 0.002）提升20个百分点。在Diverse Architectures上，GMN的R²为0.975 ± 0.002，DMC为0.957 ± 0.009，DeepSets仅为0.562 ± 0.020，表明架构多样性越大，DeepSets的集合假设越不成立，而GMN通过参数图显式建模拓扑结构持续保持优势。

**低数据（10% data）**：当训练数据缩减至10%时，GMN的优势进一步扩大。在Diverse Architectures上，GMN的R²为0.918 ± 0.002，DMC降至0.810 ± 0.046，DeepSets仅为0.126 ± 0.015。GMN相比DMC提升10.8个百分点，说明参数图的结构先验在数据稀缺时提供了更强的归纳偏置。

**分布外泛化（OOD）**：在仅使用低隐层维度网络训练、高隐层维度网络测试的OOD设置下，GMN展现出最强的泛化能力。Varying CNNs上GMN的R²为0.891 ± 0.037，而DeepSets为0.741 ± 0.015，DMC仅为0.387 ± 0.229——DMC在OOD场景下几乎失效，其基于1D CNN的向量化处理无法捕捉网络结构的组合泛化规律。

**小CNN数据集补充验证**：在Unterthiner et al.（2020）的小CNN数据集上，GMN使用图Transformer GRIT（Ma et al., 2023）作为图学习模型，同样超越了所有先前元网络（Table 6），进一步验证了方法的普适性。

### INR编辑任务：参数级精度的验证

2D INR编辑任务要求元网络对隐式神经表示的权重进行精细调整，以改变输出图像（如对比度调整、膨胀操作）。Table 2显示，在Contrast任务上GMN取得0.0197 ± 0.0000的测试MSE，略优于NFT（0.0200 ± 0.0002）和NFN-NP（0.0203 ± 0.0000）。在Dilate任务上，GMN的MSE为0.0603 ± 0.0010，弱于NFT（0.0510 ± 0.0004），但优于NFN-NP（0.0693 ± 0.0009）。

这一结果表明：参数级任务对元网络的表达能力要求更高，GMN虽在多数指标上具备竞争力，但在特定操作（如Dilate）上仍存在改进空间。值得注意，该任务中权重更新公式为 $\tilde{\theta} = \theta + \gamma \cdot \mathrm{Metanet}(\theta)$，其中$\gamma$为可学习标量，说明GMN的输出直接作用于参数空间。

### 自监督表示学习

Table 3展示了自监督学习场景下的结果。GMN学到的网络表示经线性回归器预测后，测试MSE为1.13 ± 0.08，显著优于DWSNet（1.37 ± 0.02），相对降低17.5%。该任务不依赖标注的准确率标签，仅通过重构或对比目标学习网络表示，GMN的优势表明参数图结构天然适合捕获网络的功能性特征。

### 消融：偏置节点设计的作用

作者特别分析了偏置参数的编码方式。相较于将偏置作为自环边或节点特征，使用独立的**偏置节点**（bias node）将偏置编码为从该节点到对应神经元的边，具有更强的表达能力。其因果机制在于：偏置节点允许同层不同偏置参数在消息传递的每一层中相互通信，而自环或节点特征编码则阻断了这种跨偏置的信息交换。这一设计选择直接影响了元网络对偏置参数对称性的建模精度。

### 失败模式与局限

1. **理论缺口**：Proposition 1关于网络函数不变性的证明仅针对计算图给出，扩展到参数图自同构（包括多重图情形）的严格证明仍是一个猜想（附录B.5）。这意味着当前理论保证在形式上是部分的，需要进一步验证。

2. **特定操作的精度瓶颈**：在INR编辑的Dilate任务上，GMN弱于NFT，表明参数图的消息传递机制在处理某些需要长程参数协调的操作时可能不够灵活。

3. **架构覆盖范围**：当前方法仅适用于前馈神经网络，尚未扩展到循环架构或动态计算图。参数图的构建依赖人工设计的子图模板，每新增一种层类型需要定义新的构造规则，缺乏自动化发现机制。

4. **非置换对称性的缺失**：GMN天然等变于神经DAG自同构诱导的参数置换，但未处理ReLU网络的缩放对称性等非置换对称性，这些对称性可能对某些元任务至关重要。

### 可视化诊断

Figure 8提供了OOD设置下Diverse Architectures数据集上预测准确率与真实准确率的散点图。GMN的预测点紧密围绕对角线分布，而DMC在测试集上出现大量偏离，DeepSets则呈现系统性低估。该可视化直观佐证了定量结果：GMN的等变性结构先验在分布外泛化中起到了关键的正则化作用。

### 补充图表

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2312_04501/figures/006_Figure_5.jpg]]
*Figure 5: Histograms of CIFAR-10 accuracies for our Varying CNNs and Diverse Architectures datasets. Left and middle show train and test accuracy for the two datasets. Right shows test accuracy of Diverse Architectures split by model type*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2312_04501/figures/005_Table_1.jpg]]
*Table 1: Results for predicting the test accuracy of input neural networks trained on CIFAR-10. The top results use a training set of 15 000 uniformly selected input networks, the middle results use 10% of this training set, and the bottom results only train on input networks of low hidden dimension (while testing on networks with strictly higher hidden dimension). Our method performs best in all setups, with increasing benefits in the low-data and OOD regimes*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2312_04501/figures/007_Table_2.jpg]]
*Table 2: Test MSE (lower is better) for editing 2D INRs, following the methodology of (Zhou et al., 2023a). Results of baselines are from (Zhou et al., 2023a;b)*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2312_04501/figures/008_Table_3.jpg]]
*Table 3: Results for self-supervised learning of neural net representations, in test MSE of a linear regressor on the learned representations. Numbers besides GMN from Navon et al. (2023)*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2312_04501/figures/009_Table_4.jpg]]
*Table 4: Glossary and notation*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2312_04501/figures/012_Table_5.jpg]]
*Table 5: Hyperparameters for the CIFAR-10 image classifiers that we trained for the predicting accuracy experiments in Section 5.1*

![[assets/figures/papers/paper_list_l29_https_arxiv_org_abs_2312_04501/figures/013_Table_6.jpg]]
*Table 6: Additional results for predicting accuracy on the dataset of small CNNs from Unterthiner et al. (2020). We see that GMNs outperform all metanetworks. Here, we use the Graph Transformer GRIT (Ma et al., 2023) as our graph learning model for GMN, as we find it performs better than the message passing models that we tried*

## 方法谱系与知识库定位

### 1. 核心问题与基线谱系

图元网络（Graph Metanetworks, GMNs）试图解决的核心瓶颈在于：**现有等变元网络需要针对每种输入架构手工设计等变层，难以泛化到包含归一化层、残差连接、注意力等模块的复杂网络**。这一问题催生了一系列方法，按对称性处理方式可分为三大流派：

#### 1.1 忽略对称性的方法

- **DMC（Deep Meta Classifier）**（Eilertsen et al., 2020）：将网络参数展平为向量后利用1D CNN处理。该方法可以处理不同大小的网络，但未显式保证置换对称性，导致在分布外（OOD）场景下性能急剧下降——在Diverse Architectures的OOD设置中，DMC的R²仅为0.387±0.229，远低于GMN的0.768±0.027。
- **StatNN**（Unterthiner et al., 2020）：使用参数均值、方差等统计量构建元网络，表达力受限于所选的统计特征集合，无法捕获参数间的结构化交互。

#### 1.2 手工设计等变层的方法

- **NFN系列**（Zhou et al., 2023a）：基于参数置换等变线性层（NFN-HNP、NFN-NP、NFN-PT）设计元网络。其核心是手工推导的等变线性映射，如无偏置MLP的权重更新规则（见公式NP-NFN weight update）。这类方法的**根本局限**在于：每引入一种新层类型（如归一化层、注意力层），需要重新推导等变条件，难以系统化扩展。
- **NFT**（Zhou et al., 2023b）：采用Transformer风格的参数置换等变元网络，使用特殊的注意力层。在2D INR编辑任务中表现强劲（Dilate任务上Test MSE为0.0510±0.0004，优于GMN的0.0603±0.0010），但其注意力机制的设计同样依赖对特定架构的适配。
- **DWSNet**（Navon et al., 2023）：针对MLP设计的参数置换等变元网络，在自监督学习任务上取得了Test MSE 1.37±0.02，但GMN进一步将其降至1.13±0.08。

#### 1.3 基于集合的方法

- **DeepSets**（Zaheer et al., NeurIPS 2017）：将参数视为集合，利用置换不变的聚合操作进行预测。虽然天然保证对称性，但**表达性严重受限**——在Diverse Architectures的100%数据设置下，R²仅为0.562±0.020，而GMN达到0.975±0.002。其根本缺陷在于忽略了参数间的拓扑关系。

### 2. GMN的定位与突破

GMN的核心创新在于**将对称性处理从“手工设计”提升为“结构导出”**：

- **参数图表示**：将神经网络参数编码为图结构，每个参数对应一条边，通过节点类型和邻接关系自然编码网络拓扑。这一表示的关键优势在于：
  - **紧凑性**：对比计算图（如图2所示，单卷积层4×4输入产生16条边对应4个参数），参数图不会随激活数量缩放。
  - **参数共享处理**：通过多层并行边捕获卷积、注意力等层中的权重共享信息。
  - **残差连接编码**：使用无参数边表示跳跃连接，确保对称性结构被正确捕获。

- **图自同构理论**：引入**神经DAG自同构**（Neural DAG Automorphisms）概念，统一刻画前馈神经网络参数空间中的置换对称性。核心定理（Proposition 1）表明：任何神经DAG自同构排列参数不会改变网络函数。在此框架下，GNN天然等变于这些图自同构（Proposition 2），从而**无需为每种架构手工设计等变层**。

- **通用GNN骨干**：使用消息传递GNN（或图Transformer）在参数图上操作，其更新规则（公式1-3）天然保证等变性。下游任务通过边特征池化（图级预测）或直接使用边特征（参数级预测）完成。

### 3. 适用边界与局限

#### 3.1 理论局限

- **证明缺口**：当前关于网络函数不变性的理论证明（Proposition 1）仅针对**计算图**给出，扩展到参数图自同构（包括多重图情形）的严格证明仍是一个**猜想**（见附录B.5）。这意味着在包含偏置节点、归一化参数等复杂参数图结构上，等变性的理论保证尚未完备。

- **对称性覆盖范围**：当前方法仅处理**置换对称性**，未覆盖其他类型的对称性。例如，ReLU网络的缩放对称性（对权重和偏置的尺度变换会改变网络输出）需要额外的机制来保证等变性。这一问题在NFN系列中同样存在，是领域共性挑战。

#### 3.2 工程局限

- **子图模板依赖**：参数图的构建依赖人工设计的子图模板（如图3所示的各种层类型）。每新增一种层类型（如新型注意力机制、门控单元等），需要定义新的子图构造规则。这限制了方法对新奇架构的即时适应能力。

- **规模瓶颈**：元网络的参数量与输入网络的规模相关。当处理十亿参数级大模型时，参数图的节点和边数量将急剧膨胀，带来计算和内存效率瓶颈。论文未提供大规模网络的实验验证。

- **架构覆盖范围**：当前方法仅适用于**前馈神经网络**，尚未扩展到循环架构（RNN、LSTM）或动态计算图。这是方法谱系中的显著空白。

#### 3.3 实验覆盖的盲区

- 在2D INR编辑的Dilate任务上，GMN（Test MSE 0.0603±0.0010）**弱于NFT**（0.0510±0.0004），表明在某些参数级编辑任务上，Transformer风格的等变设计可能更具优势。
- 所有实验均在相对小规模的网络上进行（CIFAR-10分类器、小型INR），缺乏对大规模模型（如ResNet-101、ViT）的验证。

### 4. 开放问题与未来方向

1. **理论完备化**：能否将Proposition 1的证明从计算图严格推广到参数图自同构（包括多重图情形）？这是方法理论根基的未竟之业。

2. **自动化图构建**：如何设计自动化的参数图构造方法，使其能发现并利用任意新奇层类型的子图表示？当前的模板化方法限制了通用性。

3. **规模扩展**：图元网络能否有效地处理具有数亿乃至数十亿参数的大型模型？需要哪些加速或近似技术（如层次化图构建、图采样）？

4. **架构泛化**：能否将元网络设计扩展到非前馈架构，例如图神经网络本身或具有循环连接的网络？这需要重新审视对称性群的定义。

5. **对称性扩展**：如何在图元网络框架内整合非置换对称性（如缩放、旋转等）的处理能力？这可能需要引入连续群等变GNN。

6. **表示空间优化**：参数图中节点和边特征的最优设计空间是什么？是否可以通过可学习的方式自动获取，而非依赖手工设计的层索引、位置编码等特征？

7. **多任务统一**：多任务元网络（同时进行准确率预测、权重编辑、自监督表示学习）是否在图元网络框架下更容易实现？参数图表示天然支持多任务输出头的设计。

## 原文 PDF

![[paperPDFs/ICLR_2024/Graph_Metanetworks_for_Processing_Diverse_Neural_Architectures.pdf]]
