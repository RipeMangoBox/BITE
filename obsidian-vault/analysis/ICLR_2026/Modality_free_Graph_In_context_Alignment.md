---
title: "Modality-free Graph In-context Alignment"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Modality_free_Graph_In_context_Alignment.pdf
openreview_forum_id: cDc95lucVL
aliases:
- MGMFGCA
- MFGCA
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/trustworthy_machine_learning
core_operator: "梯度指纹（gradient fingerprint）：从共享的固定初始化出发，对每个图进行单步梯度更新，得到的参数位移能够编码该图的特征、标签与结构的联合分布特性，作为无外部监督的域描述符，驱动跨域对齐。"
primary_logic: "利用梯度指纹捕获图的域特性，并通过轻量级域条件 FiLM 变换，将任意预编码的特征和本地标签 ID 投影到统一的语义空间，同时保持域内几何结构，实现真正的模态无关的跨域对齐与少样本上下文推理。"
claims:
- "梯度指纹是单步参数更新，编码了特征、标签和结构如何共同影响模型。"
- "MF-GIA 通过梯度指纹参数化的轻量变换，将预编码特征和标签对齐到统一语义空间。"
- "双提示感知注意力（DPAA）配合 episodic 目标，学习匹配查询与对齐的支持示例，实现参数更新自由的推理。"
- "域嵌入保持域间关系，相似域映射到邻近子空间，使得对齐后的特征和标签具有语义连续性。"
---

# Modality-free Graph In-context Alignment

> [!tip] 核心洞察
> 利用梯度指纹捕获图的域特性，并通过轻量级域条件 FiLM 变换，将任意预编码的特征和本地标签 ID 投影到统一的语义空间，同时保持域内几何结构，实现真正的模态无关的跨域对齐与少样本上下文推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 模态无关的图上下文对齐方法 |
| 英文题名 | Modality-free Graph In-context Alignment |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=cDc95lucVL); [GitHub](https://github.com/JhuoW/MF-GIA) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/trustworthy_machine_learning |
| Method | MF-GIA (Modality-Free Graph In-context Alignment) |
| Dataset | Cora (Citation, 7-way), ogbn-Products (E-commerce, 47-way), Physics (Co-authorship, 5-way), BlogCatalog (Social Media, 6-way) |

> [!tip] 效果简介
> - Cora (Citation, 7-way) 上，5-shot 准确率 (%) 为 63.98 ±7.13。
> - ogbn-Products (E-commerce, 47-way) 上，5-shot 准确率 (%) 为 22.61 ±1.71。
> - Physics (Co-authorship, 5-way) 上，5-shot 准确率 (%) 为 88.92 ±0.84。

## 概述

### 问题背景

图基础模型（Graph Foundation Models, GFMs）旨在为多样化的图数据提供统一的表示与推理能力。然而，现有 GFMs 难以同时满足真正上下文学习（In-Context Learning, ICL）所需的三个关键条件：**无需后训练与参数更新**（post-training-free）、**跨域对齐**（cross-domain alignment）和**模态独立性**（modality-free）。依赖模态特定编码器或需要原始文本属性图（TAG）的模型无法直接处理已预编码的任意图数据，这构成了当前图基础模型推广的核心瓶颈。

### 核心方法

本文提出 **MF-GIA**（Modality-Free Graph In-context Alignment），一种模态无关的图上下文对齐方法。其核心创新在于引入**梯度指纹**（gradient fingerprint）作为无监督域描述符：从共享的固定初始化出发，对每个图进行单步梯度更新，得到的参数位移能够编码该图特征、标签与结构的联合分布特性。基于此，MF-GIA 通过轻量级域条件 FiLM 变换，将任意预编码的特征和本地标签 ID 投影到统一的语义空间，同时保持域内几何结构，实现真正的模态无关跨域对齐。

在推理阶段，MF-GIA 采用**双提示感知注意力机制**（Dual Prompt-Aware Attention, DPAA），配合 episodic 训练目标，学习匹配查询与对齐后的支持示例，实现参数冻结的少样本上下文推理。

### 方法定位

MF-GIA 在图基础模型谱系中占据独特位置：与传统 GNN（如 **GCN** Kipf & Welling, ICLR 2017；**GAT** Velickovic et al., ICLR 2018）和自监督方法（如 **GraphMAE** Hou et al., NeurIPS 2022）不同，它无需在目标任务上微调；与带后训练的 GFM（如 **GCOPE**、**GFT**、**GPF** 等）相比，MF-GIA 完全免除参数更新；相较于现有具备 ICL 能力的模型（如 **Prodigy** Huang et al., 2023；**OFA** Liu et al., 2024a；**GraphAlign** Hou et al., 2024），MF-GIA 不依赖文本模态或原始 TAG 数据，真正实现了模态无关的上下文推理。

### 主要结果

在跨域少样本节点分类与边分类任务上，MF-GIA 展现出显著优势。以 5-shot 节点分类为例，在引文网络 Cora 上达到 63.98%，在电商图 ogbn-Products 上达到 22.61%，在合著网络 Physics 上达到 88.92%。在知识图谱边分类任务中，MF-GIA 在 FB15K237 上 1-shot 准确率达 98.77%，较 GraphAlign 提升 15.75 个百分点。消融实验证实，域嵌入驱动的特征对齐与标签对齐、DPAA 机制及 episodic 训练范式均为关键贡献因素。此外，MF-GIA 在不同特征编码（BoW、RoBERTa、LLaMa2-7B 等）下性能稳健，验证了其模态无关性。

## 背景与动机

### 图基础模型的上下文学习困境

图基础模型（Graph Foundation Models, GFMs）旨在像大语言模型（LLMs）一样，通过预训练获得跨任务、跨领域的通用图理解能力。然而，现有 GFMs 在实现真正的上下文学习（In-Context Learning, ICL）时面临一个核心瓶颈：**难以同时满足三个基本条件**——无需后训练与参数更新（post-training-free）、跨域对齐（cross-domain alignment）和模态独立性（modality-free）。

具体而言，当前方法可大致分为三类（见表 1）：

- **带后训练的 GFM**（如 **GCOPE** (Zhao et al., 2024)、**GFT** (Wang et al., 2024b)、**AutoGFM** (Chen et al., 2025)、**GPF** (Fang et al., 2023)、**All in One** (Sun et al., 2023)）：这些方法在预训练后仍需在目标域上进行微调或提示学习，无法实现参数冻结的即时推理，违反了“无需后训练”准则。

- **依赖文本属性图（TAG）的 ICL 方法**（如 **OFA** (Liu et al., 2024a)、**GraphAlign** (Hou et al., 2024)）：它们通过将图结构统一到文本模态来实现跨域对齐，但要求图数据附带原始文本描述。当面对仅提供预编码特征和索引标签的任意图时（例如出于隐私或存储限制），这些方法完全不可用，丧失了模态独立性。

- **传统 GNN 与自监督方法**（如 **GCN** (Kipf & Welling, ICLR 2017)、**GAT** (Velickovic et al., ICLR 2018)、**GraphSAGE** (Hamilton et al., NeurIPS 2017)、**GraphMAE** (Hou et al., NeurIPS 2022)、**DGI** (Velickovic et al., ICLR 2019)、**GraphCL** (You et al., NeurIPS 2020)）：它们或依赖特定模态的输入，或需要在目标图上重新训练，无法同时满足三项准则。

唯一在概念上接近真正 ICL 的是 **Prodigy** (Huang et al., 2023)，它通过元学习实现参数冻结推理，但缺乏显式的跨域对齐机制，导致在域偏移场景下性能下降。

### 核心缺口：模态无关的跨域对齐

上述困境的根源在于一个根本性的技术缺口：**如何在不依赖模态特定编码、不访问原始数据、不进行参数更新的前提下，将来自任意域、任意特征空间的图数据对齐到统一的语义空间？**

这一缺口包含两个相互关联的子问题：

1. **域描述符的获取**：现有方法要么依赖外部领域标签（如数据集名称），要么依赖模态元数据（如文本描述）来识别域特性。当面对完全未知的、仅有预编码特征的图时，这些外部信号不可用，模型无法判断不同图之间的域相似性与差异性。

2. **特征与标签的统一**：不同图域的特征维度、语义空间和标签体系各不相同。没有统一的特征空间，跨图的少样本知识迁移无从谈起；没有统一的标签空间，不同图中相同语义的类别（如“论文类别”与“商品类别”中的对应关系）无法建立关联。

### 本文动机与核心思路

针对上述缺口，本文提出 **MF-GIA**（Modality-Free Graph In-Context Alignment），其核心动机是：**利用图自身的内在属性——特征分布、标签分布和图结构——来驱动跨域对齐，而非依赖外部模态信号**。

这一动机的关键洞察在于 **梯度指纹（gradient fingerprint）**：从共享的固定初始化出发，对每个图进行单步梯度更新，得到的参数位移 $\Delta\theta_i = \theta_i - \theta_0$ 编码了该图的特征、标签与结构的联合分布特性。不同域的图因其内在属性的差异，会产生不同的梯度指纹；相似域的图则产生相近的指纹。这一机制使得梯度指纹可以作为**无外部监督的域描述符**，驱动后续的对齐过程。

基于梯度指纹，MF-GIA 通过轻量级的域条件 FiLM 变换，将任意预编码的特征和本地标签 ID 投影到统一的语义空间，同时保持域内几何结构。配合双提示感知注意力（DPAA）和 episodic 预训练目标，模型学会在参数冻结的条件下，仅依靠少量支持示例进行跨域上下文推理。这一设计使得 MF-GIA 成为首个同时满足“无需后训练、跨域对齐、模态无关”三项准则的图上下文学习方法。

## 核心创新

MF-GIA 的核心创新在于以**梯度指纹**（gradient fingerprint）为统一域描述符，构建了首个同时满足真正图上下文学习（ICL）三项准则的框架：**无需后训练与参数更新**（post-training-free）、**跨域对齐**（cross-domain alignment）和**模态无关**（modality-free）。现有方法在这三项准则上存在系统性缺陷（Table 1）：传统 GNN（如 **GCN**, Kipf & Welling, ICLR 2017）和自监督方法（如 **GraphMAE**, Hou et al., NeurIPS 2022）需要后训练微调；带后训练的 GFM（如 **GCOPE**, Zhao et al., 2024；**AutoGFM**, Chen et al., 2025）无法实现参数冻结推理；而具有 ICL 能力的模型（如 **OFA**, Liu et al., 2024a；**GraphAlign**, Hou et al., 2024）则依赖文本属性图（TAG），无法处理仅含预编码特征和索引标签的任意图数据。

MF-GIA 通过以下五个关键设计突破上述瓶颈，构成其与基线方法的本质差异：

### 1. 域描述符：从外部标签到梯度指纹

基线方法依赖外部领域标签或模态元数据（如文本描述）来区分不同图域。MF-GIA 提出**梯度指纹**作为无监督域描述符：从一个共享的固定权重初始化 $\theta_0^\star$ 出发，对每个图进行单步梯度更新，得到的参数位移 $\Delta\theta_i$ 编码了该图特征、标签与结构的联合分布特性（Section 3.1）。这一设计使域嵌入直接从图的内在属性中涌现，无需任何外部监督信号。

域嵌入 $e_i = f_{\phi_{\mathrm{de}}}(\Delta\theta_i)$ 通过 2D 卷积与 MLP 从梯度指纹中提取，并经由距离保持损失训练：

$$\mathcal{L}_{\mathrm{de}} = \sum_{G_i, G_j \in \mathcal{G}} \left( \|\Delta\theta_i - \Delta\theta_j\|_F - \|e_i - e_j\|_2 \right)^2$$

理论分析（Theorem 3.1）证明，域嵌入间的欧氏距离被域分布的 Wasserstein-2 距离线性限定：$\| e_i - e_j \|_2 \leq \widetilde{C} \cdot \mathcal{W}_2(\mathcal{D}_i, \mathcal{D}_j)$，保证相似域在嵌入空间中邻近。

### 2. 特征对齐：从模态依赖到域条件 FiLM

基线方法或缺乏跨域特征对齐，或强制统一到文本模态（如 OFA、GraphAlign）。MF-GIA 采用**域条件 FiLM 变换**，将任意预编码特征映射到统一语义空间：

$$z_{i,w} = \gamma_i^{\mathrm{feat}} \odot h_{i,w} + \beta_i^{\mathrm{feat}}$$

其中缩放参数 $\gamma_i^{\mathrm{feat}}$ 和平移参数 $\beta_i^{\mathrm{feat}}$ 由域嵌入 $e_i$ 通过轻量 MLP 生成。由于 $\|K_i^{\mathrm{feat}} - K_j^{\mathrm{feat}}\| \propto \|e_i - e_j\|$，相似域的特征变换相似，对齐后的特征在统一空间中保持域间几何关系。

### 3. 标签对齐：从本地 ID 到共享语义空间

图数据中本地标签 ID 在不同图间无对应关系，基线方法无法跨图统一标签语义。MF-GIA 引入**共享标签基** $\mathbf{E}^{\mathrm{label}} \in \mathbb{R}^{L_{\max} \times d}$ 配合域条件 FiLM 变换：

$$u_{i,l} = \gamma_i^{\mathrm{label}} \odot \mathbf{E}_l^{\mathrm{label}} + \beta_i^{\mathrm{label}}$$

该设计将每个图的本地标签索引映射到统一的 $d$ 维标签原型空间，使不同图中语义相近的类别自然靠近（Figure 3）。

### 4. 提示注意力：从简单匹配到双提示感知注意力

MF-GIA 提出**双提示感知注意力**（Dual Prompt-Aware Attention, DPAA），包含分离的特征侧与标签侧交叉注意力层。特征侧注意力使查询物品关注支持集特征，生成提示感知的查询表示；标签侧注意力进一步将该表示与域特定标签原型交互，产生最终匹配向量。两层共享投影矩阵 $\mathbf{W}_K, \mathbf{W}_V$，确保特征与标签空间的一致性。

### 5. 训练范式：从微调到完全 Episodic 预训练

MF-GIA 采用完全 **episodic 元学习预训练**（Algorithm 1），在每个 episode 中模拟 $m$-way $k$-shot 场景，最大化查询集真实标签的似然：

$$\min_\Phi \mathbb{E} \left[ -\frac{1}{|\mathcal{Q}|} \sum_{q \in \mathcal{Q}} \log \hat{p}(y_q \mid q, S, G_i) \right]$$

推理时所有参数冻结，仅需为每个新图计算梯度指纹和域嵌入，即可通过支持集进行上下文适应（Algorithm 2），无需任何参数更新。

### 创新点的因果链条

梯度指纹 → 域嵌入 → 域条件 FiLM（特征对齐 + 标签对齐）→ 统一语义空间 → DPAA 匹配 → 参数冻结推理。这一链条使 MF-GIA 成为首个在真正 ICL 三项准则上全部满足的方法，而所有基线方法至少缺失其中一项。

## 整体框架

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/002_Figure_1.jpg]]
*Figure 1: Overview of MF-GIA. (Left) Modality-free Alignment: The pretraining graphs are mapped to a unified space via domain-conditioned transformations. Domain descriptors e ensure similar domains occupy neighboring subspaces. (Middle) Episodic Pretraining: The model learns from m-way k-shot episodes using domain-aligned features and labels. The DPAA mechanism matches queries to classes using only prompts as context. (Right) In-context Prediction: For an unseen graph, the frozen model performs few-shot classification using the support set as a prompt*

MF-GIA 的整体 pipeline 围绕一个核心目标展开：让预训练模型在参数完全冻结的前提下，仅通过少量支持示例（support set）即可对任意新图完成推理。这一目标被形式化为 episodic 上下文学习问题——模型在预训练阶段反复经历“从支持集推断查询集标签”的模拟场景，从而学会少样本匹配能力。

框架由三个紧密耦合的阶段构成，其数据流与模块关系如下：

**阶段一：模态无关对齐（Modality-free Alignment）**

这是整个 pipeline 的入口。对于任意输入的预训练图 $G_i$，系统首先通过**域嵌入器（Domain Embedder）** 从该图的内在属性中提取一个紧凑的域描述符 $e_i$。该描述符的生成不依赖任何外部领域标签或模态元数据，而是利用**梯度指纹（gradient fingerprint）**——从共享的固定初始化出发，对每个图执行单步梯度更新，得到的参数位移 $\Delta\theta_i$ 编码了该图特征、标签与结构的联合分布特性。

域嵌入 $e_i$ 随后作为条件信号，驱动两个轻量级对齐变换：
- **特征对齐器（Feature Aligner）**：以域条件 FiLM 变换（缩放 $\gamma_i^{\text{feat}}$ + 平移 $\beta_i^{\text{feat}}$）将共享 GNN 编码器输出的基础物品表示 $h_{i,w}$ 映射到统一的语义特征空间，得到对齐特征 $z_{i,w}$。
- **标签对齐器（Label Aligner）**：架构与特征侧相同，将共享标签基 $\mathbf{E}^{\text{label}}$ 中的域无关原型通过域条件 FiLM 变换为域特定的标签嵌入 $u_{i,l}$，解决跨图标签 ID 不一致的问题。

关键设计在于：域嵌入保持了域间距离关系（相似域映射到邻近子空间），使得对齐后的特征和标签具有语义连续性，为后续跨域匹配奠定基础。

**阶段二：Episodic 预训练（Episodic Pretraining）**

对齐后的特征和标签进入**双提示感知注意力（Dual Prompt-Aware Attention, DPAA）** 模块。DPAA 由两层单查询交叉注意力组成：
- **特征侧注意力**：查询特征 $z_{i,q}$ 关注支持集的特征矩阵 $\mathbf{Z}^{\text{pmt}}$，生成提示感知的查询表示 $z_{i,q}^{\text{out}}$。
- **标签侧注意力**：上述输出进一步关注域特定的标签原型 $\mathbf{U}^{\text{pmt}}$，生成最终匹配表示 $u_{i,q}^{\text{out}}$。

最终类别得分通过 $u_{i,q}^{\text{out}}$ 与提示标签矩阵的内积计算，取 argmax 得到预测标签。整个预训练以 episodic 目标优化：在每个 episode 中，从图中采样 m-way k-shot 的支持集和查询集，最大化查询集上真实标签的似然。域嵌入器在此阶段之前已通过距离保持损失 $\mathcal{L}_{\text{de}}$ 单独训练并固定。

**阶段三：上下文推理（In-context Inference）**

推理时，所有可学习参数（共享 GNN 编码器、FiLM 生成网络、DPAA 投影矩阵）保持冻结。对于新图 $G_{\text{new}}$，系统仅执行以下操作：
1. 计算梯度指纹并输入预训练的域嵌入器，得到域嵌入 $e_{\text{new}}$；
2. 利用 $e_{\text{new}}$ 生成对齐参数，将新图的特征和标签映射到统一空间；
3. 通过 DPAA 匹配查询与支持示例，输出预测。

这一流程实现了真正的 **post-training-free**：无需在任何目标任务上微调或学习提示，仅依靠支持集进行 in-context 适应。整个 pipeline 的输入是预编码的任意图数据（特征维度通过 SVD 统一至 $d_o$），输出是查询物品的类别预测，完全独立于底层模态。

## 核心模块与公式推导

MF-GIA 的核心架构由四个紧密耦合的模块构成：域嵌入器（Domain Embedder）、特征对齐器（Feature Aligner）、标签对齐器（Label Aligner）和双提示感知注意力（DPAA）。这些模块协同工作，将任意预编码的图数据和本地标签 ID 投影到统一的语义空间，实现参数更新自由的少样本上下文推理。

### 域嵌入器：梯度指纹驱动的无监督域描述

域嵌入器是整个框架的基石，其核心思想是利用**梯度指纹**（gradient fingerprint）作为域描述符。具体而言，从一个共享的固定权重初始化 $\theta_0^\star \in \mathbb{R}^{d_o \times d}$ 出发，对每个图 $G_i$ 执行单步梯度更新：

$$\Delta\theta_i = \theta_i - \theta_0^\star$$

这一参数位移量 $\Delta\theta_i$ 编码了该图的特征、标签与结构如何共同影响模型的联合分布特性，无需任何外部领域标签或模态元数据。随后，梯度指纹通过一个可训练的域嵌入器 $f_{\phi_{\mathrm{de}}}$ 被压缩为紧凑的域嵌入向量：

$$e_i = f_{\phi_{\mathrm{de}}}(\Delta\theta_i) = \mathrm{MLP}(\mathrm{Flatten}(\mathrm{Conv2D}(\Delta\theta_i))) \in \mathbb{R}^{d_e}$$

其中 $\mathrm{Conv2D}$ 将梯度矩阵视为二维信号提取局部模式，$\mathrm{Flatten}$ 展平后经 $\mathrm{MLP}$ 投影到 $d_e$ 维空间。

**域嵌入的训练**通过保持梯度指纹空间中的成对距离来实现，损失函数为：

$$\mathcal{L}_{\mathrm{de}} = \sum_{G_i, G_j \in \mathcal{G}} \left( \|\Delta\theta_i - \Delta\theta_j\|_F - \|e_i - e_j\|_2 \right)^2$$

该损失确保域嵌入空间忠实地保留图之间的域相似性。理论分析进一步证明，域嵌入之间的距离被域分布的 Wasserstein-2 距离线性限定：

$$\| e_i - e_j \|_2 \leq \widetilde{C} \cdot \mathcal{W}_2(\mathcal{D}_i, \mathcal{D}_j)$$

这意味着相似域在嵌入空间中自然聚集到邻近子空间，为后续的对齐操作提供了语义连续性保证。域嵌入器在 episodic 预训练之前独立优化，之后参数冻结。

### 特征对齐：域条件 FiLM 变换

给定图 $G_i$ 中物品 $w$ 的基础表示 $h_{i,w} = f_\theta(w, G_i) \in \mathbb{R}^d$（由共享 GNN 编码器 $f_\theta$ 提取），特征对齐器通过域条件 FiLM（Feature-wise Linear Modulation）将其映射到统一语义空间：

$$(\gamma_i^{\mathrm{feat}}, \beta_i^{\mathrm{feat}}) = f_{\phi_{\mathrm{feat}}}(e_i), \quad \gamma_i^{\mathrm{feat}}, \beta_i^{\mathrm{feat}} \in \mathbb{R}^d$$

$$z_{i,w} = \gamma_i^{\mathrm{feat}} \odot h_{i,w} + \beta_i^{\mathrm{feat}}$$

其中 $\odot$ 表示逐元素乘法，$\gamma_i^{\mathrm{feat}}$ 为缩放因子，$\beta_i^{\mathrm{feat}}$ 为平移因子，均由域嵌入 $e_i$ 通过小型 MLP $f_{\phi_{\mathrm{feat}}}$ 生成。这种轻量级仿射变换在保持域内几何结构的同时，将不同域的特征对齐到共享空间。由于相似域具有相近的域嵌入 $e_i \approx e_j$，它们产生的 FiLM 参数也相近，使得对齐后的特征自然占据相邻子空间。

在推理阶段，对于新图 $G_{\mathrm{new}}$，通过梯度指纹计算域嵌入 $e_{\mathrm{new}} = f_{\phi_{\mathrm{de}}}(\theta_{\mathrm{new}} - \theta_0)$，再生成对应的 FiLM 参数完成特征对齐，全程无需参数更新。

### 标签对齐：共享标签基的域条件映射

图数据中本地标签 ID 在不同图之间缺乏语义一致性（例如图 A 的类别 0 与图 B 的类别 0 可能毫无关联）。标签对齐器通过维护一个**共享标签基** $\mathbf{E}^{\mathrm{label}} \in \mathbb{R}^{L_{\max} \times d}$（$L_{\max}$ 为预训练中最大类别数），将域无关的标签原型通过域条件 FiLM 变换为域特定的标签嵌入：

$$(\gamma_i^{\mathrm{label}}, \beta_i^{\mathrm{label}}) = f_{\phi_{\mathrm{label}}}(e_i)$$

$$u_{i,l} = \gamma_i^{\mathrm{label}} \odot \mathbf{E}_l^{\mathrm{label}} + \beta_i^{\mathrm{label}}, \quad l \in \{0, \dots, C_i - 1\}$$

标签侧的 FiLM 变换与特征侧架构相同，但参数独立。这种设计使得同一语义概念在不同域中的标签嵌入保持关联，同时允许域特定的偏移。推理时，新图的标签原型通过 $u_{\mathrm{new},l} = \gamma_{\mathrm{new}}^{\mathrm{label}} \odot \mathbf{E}_l^{\mathrm{label}} + \beta_{\mathrm{new}}^{\mathrm{label}}$ 动态生成。

### 双提示感知注意力与 Episodic 训练

在 episodic 预训练阶段，对于每个 episode，从图 $G_i$ 中采样 $m$-way $k$-shot 的支持集 $\mathcal{S}$ 和查询集 $\mathcal{Q}$。DPAA 由两个单查询交叉注意力层组成，特征侧和标签侧共享投影矩阵 $\mathbf{W}_K, \mathbf{W}_V$：

**特征侧注意力**：查询特征 $z_{i,q}$ 关注支持集特征矩阵 $\mathbf{Z}^{\mathrm{pmt}}$：

$$\mathbf{Q}^{\mathrm{feat}} = z_{i,q} \mathbf{W}_Q, \quad \mathbf{K}^{\mathrm{feat}} = \mathbf{Z}^{\mathrm{pmt}} \mathbf{W}_K, \quad \mathbf{V}^{\mathrm{feat}} = \mathbf{Z}^{\mathrm{pmt}} \mathbf{W}_V$$

$$z_{i,q}^{\mathrm{out}} = \mathrm{softmax}\left( \frac{\mathbf{Q}^{\mathrm{feat}} (\mathbf{K}^{\mathrm{feat}})^\top}{\sqrt{d}} \right) \mathbf{V}^{\mathrm{feat}}$$

**标签侧注意力**：提示增强的查询表示进一步关注域特定标签原型 $\mathbf{U}^{\mathrm{pmt}}$：

$$\mathbf{Q}^{\mathrm{label}} = z_{i,q}^{\mathrm{out}} \mathbf{W}_Q, \quad \mathbf{K}^{\mathrm{label}} = \mathbf{U}^{\mathrm{pmt}} \mathbf{W}_K, \quad \mathbf{V}^{\mathrm{label}} = \mathbf{U}^{\mathrm{pmt}} \mathbf{W}_V$$

$$u_{i,q}^{\mathrm{out}} = \mathrm{softmax}\left( \frac{\mathbf{Q}^{\mathrm{label}} (\mathbf{K}^{\mathrm{label}})^\top}{\sqrt{d}} \right) \mathbf{V}^{\mathrm{label}}$$

最终类别得分通过输出向量与提示标签矩阵的内积计算：

$$s_{i,q} = u_{i,q}^{\mathrm{out}} (\mathbf{U}^{\mathrm{pmt}})^\top \in \mathbb{R}^{C_i}, \quad \hat{p}(y_q = j \mid q, \mathcal{S}, G_i) = \frac{\exp(s_{i,q}[j])}{\sum_{c=1}^{C_i} \exp(s_{i,q}[c])}$$

整个框架通过最小化 episodic 负对数似然进行端到端预训练：

$$\min_\Phi \mathbb{E}_{G_i \sim \mathcal{G}} \mathbb{E}_{\mathrm{episode} \sim G_i} \left[ -\frac{1}{|\mathcal{Q}|} \sum_{q \in \mathcal{Q}} \log \hat{p}(y_q \mid q, \mathcal{S}, G_i) \right]$$

预训练完成后，所有参数 $\Phi$ 冻结。推理时仅需计算新图的梯度指纹、生成域嵌入、执行特征与标签对齐，再通过 DPAA 完成少样本匹配预测，全程无需任何参数更新。

## 实验与分析

### 核心实验设置

MF-GIA 在四个不同领域的图数据集上进行预训练：引文网络（Cora）、电子商务（ogbn-Products）、合著网络（Physics）和社交媒体（BlogCatalog），覆盖了节点分类与边分类两种任务。所有基线方法遵循相同的 episodic 协议（相同的 m-way, k-shot 支持/查询划分），在适用时使用可比的骨干网络，并在作者推荐范围内调优超参数。对于依赖文本属性图（TAG）的模态依赖模型（如 **OFA**（Liu et al., 2024a）、**GraphAlign**（Hou et al., 2024）），在它们原始的数据集和实现上进行评估以确保公平。传统和自监督方法在支持集上微调后在查询集评估，具有 ICL 能力的模型则按其设计的推理方式评估。

### 少样本节点分类主结果

Table 2 报告了 5-shot 节点分类的准确率。MF-GIA 在跨域场景下展现出显著的性能优势：

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/005_Table_2.jpg]]
*Table 2: Few-shot node classification accuracy (%) with standard deviation over 10 runs. Best and second-best results are shown in bold and underlined. “–” denotes datasets where only encoded features and indexed labels are available, making modality-dependent models inapplicable*

- **Cora**（引文网络，7-way）：MF-GIA 达到 63.98% ±7.13，相比传统 GNN（如 **GCN**（Kipf & Welling, ICLR 2017）仅 36.24%）和自监督方法（如 **GraphMAE**（Hou et al., NeurIPS 2022）的 42.88%）有大幅提升。对于需要后训练的 GFM（如 **GCOPE**（Zhao et al., 2024）的 32.51%、**GPF**（Fang et al., 2023）的 40.14%），MF-GIA 的优势更为明显。
- **ogbn-Products**（电子商务，47-way）：MF-GIA 取得 22.61% ±1.71，在 47 类分类的高难度场景下，显著优于所有对比方法。
- **Physics**（合著网络，5-way）：MF-GIA 达到 88.92% ±0.84，接近该数据集上的性能上限。
- **BlogCatalog**（社交媒体，6-way）：MF-GIA 取得 67.31% ±2.60，同样领先于所有基线。

值得注意的是，模态依赖的 ICL 方法（OFA、GraphAlign）在仅提供预编码特征和索引标签的数据集上无法运行（表中以“–”标记），而 MF-GIA 的模态无关设计使其在这些场景下仍能正常工作，这是其核心优势之一。

### 少样本边分类结果

Table 3 展示了边分类任务的少样本准确率。在知识图谱 FB15K237 上，MF-GIA 在 1-shot 场景下达到 98.77% ±1.03，相比 GraphAlign 的 83.02% 提升了 15.75 个百分点；5-shot 下进一步提升至 99.64% ±0.20。在词汇知识图谱 WN18RR 的 10-way 5-shot 场景下，MF-GIA 达到 68.05% ±4.39。这些结果表明梯度指纹驱动的跨域对齐在关系推理任务上同样有效，且 1-shot 场景下的巨大优势说明 MF-GIA 的域嵌入在极端少样本条件下仍能提供可靠的域描述。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/006_Table_3.jpg]]
*Table 3: Few-shot edge classification accuracy (%) with standard deviation over 20 episodes*

### 消融实验：核心组件的因果贡献

Table 4 通过逐步加入核心组件，揭示了各模块的因果效应：

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/008_Table_4.jpg]]
*Table 4: Effect of core components*

1. **基础模型**（仅共享 GNN 编码器 + 无对齐）：性能最低，验证了跨域特征和标签空间不一致是核心瓶颈。
2. **+ 域嵌入 & 特征对齐（+Feat. Align.）**：引入梯度指纹驱动的 FiLM 特征对齐后，性能显著跃升。这证实了域条件变换能够有效将异构特征空间映射到统一语义空间，是跨域泛化的关键使能因素。
3. **++ 标签对齐（++Label Align.）**：将对齐扩展到标签空间，进一步统一了跨图的类索引语义，带来额外增益。这一步解决了图本地标签 ID 不一致的问题，使得不同图中相同语义的类别在嵌入空间中彼此靠近。
4. **完整 MF-GIA（+DPAA + episodic 目标）**：引入双提示感知注意力和 episodic 训练目标后达到最优性能。DPAA 使得查询能够同时关注支持集的特征和标签信息，而 episodic 训练则让模型学会从少量示例中推理，而非简单记忆类别。

### 预训练域多样性的关键作用

Table 7 的预训练数据集组成消融揭示了域多样性的决定性影响：使用全部四个域进行预训练时，总体准确率达到 60.73%；而仅使用单一域预训练时，最高仅为 45.57%（以 Physics 预训练为例）。这一证据链表明，MF-GIA 的跨域泛化能力并非来自对特定域分布的过拟合，而是源于多域预训练中学习到的通用对齐机制。域嵌入空间在多样化预训练下能够形成更有意义的域间拓扑结构，使得相似域映射到邻近子空间，从而在遇到新域时能够通过插值实现有效泛化。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/012_Table_7.jpg]]
*Table 7: Effect of pretraining dataset composition on few-shot node classification accuracy (%). We systematically vary domain coverage from single to full four-domain pretraining. Results are 5-shot accuracy averaged over 20 episodes. Best results are bold*

### 模态无关性验证

Table 8 展示了 MF-GIA 在 Cora 数据集上使用不同特征编码时的性能：BoW（63.98%）、Skip-Thought（62.15%）、RoBERTa（64.32%）、LLaMa2-7B（61.87%）。无论底层特征来自浅层词袋模型还是深层大语言模型，性能波动很小（标准差约 1.1%），有力验证了 MF-GIA 的模态无关性。梯度指纹捕获的是特征-标签-结构的联合分布特性，而非特定编码方式的统计特征，因此对齐机制对输入模态不敏感。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/013_Table_8.jpg]]
*Table 8: Performance of MF-GIA on Cora with different feature encodings*

### 梯度指纹的稳定性与参数灵敏度

**指纹稳定性**（Table 11）：在 5-shot 支持集下，同一域内不同 episode 的梯度指纹嵌入余弦相似度均超过 0.91，表明梯度指纹作为域描述符具有高度的一致性和可复现性。这为域嵌入的可靠性提供了实证支撑——即使在少样本场景下，单步梯度更新也能稳定捕获域的固有特性。

**温度参数 τ**（Table 12）：在 [0.2, 1] 范围内，MF-GIA 的性能波动很小，模型对该超参数不高度敏感，降低了实际部署中的调参负担。

**DPAA 配置**（Table 13）：1 层 1 头的 DPAA 配置在效率和效果间取得了最佳平衡。增加层数或头数可能引入轻微过拟合，表明当前任务规模下，轻量级注意力已足以捕获提示示例间的匹配关系。

### 附加预训练任务的增益

Table 10 显示，添加链接预测作为辅助预训练任务可进一步提升少样本准确率（例如 ogbn-Products 从 22.61% 提升至 24.59%）。这表明梯度指纹框架具有良好的可扩展性，能够兼容多任务预训练范式，结构信息的额外监督信号有助于域嵌入捕获更丰富的图拓扑特征。

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/015_Table_10.jpg]]
*Table 10: Performance of MF-GIA with additional pretraining tasks (5-shot)*

### 失败模式与局限性

尽管 MF-GIA 在跨域少样本场景下表现优异，仍存在以下已知局限：

1. **极端少样本退化风险**：梯度指纹的稳定性依赖于支持集大小，1-shot 场景下指纹质量可能下降（尽管在 FB15K237 上表现良好，但在更复杂的节点分类任务上尚需验证）。
2. **推理计算开销**：每个新图需额外进行一次反向传播以计算梯度指纹，虽然参数不更新，但相比纯前向方法仍有计算成本。
3. **域分布偏移敏感性**：域嵌入的模板初始化和共享编码器可能对与预训练域完全不同的图分布敏感，在跨域泛化的边界处性能可能衰减。
4. **任务覆盖范围**：当前仅在节点和边分类任务上验证，尚未探索图级别预测或生成任务，方法的通用性边界尚不明确。

### 补充图表

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/011_Figure_5.jpg]]
*Figure 5: Pretraining curves of MF-GIA*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/001_Table_1.jpg]]
*Table 1: Comparison of methods with respect to the three main criteria of true ICL*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/009_Table_5.jpg]]
*Table 5: Effect of ICL scheme*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/010_Table_6.jpg]]
*Table 6: Dataset statistics*

![[assets/figures/papers/paper_list_l5_https_openreview_net_forum_id_cDc95lucVL/figures/014_Table_9.jpg]]
*Table 9: Performance on MF-GIA with expressive dimension unification component*

## 方法谱系与知识库定位

### 1. 问题定位：图基础模型的“真正上下文学习”瓶颈

现有图基础模型（GFMs）在追求少样本跨域泛化时，面临一个核心瓶颈：难以同时满足真正上下文学习（in-context learning, ICL）所需的三个条件——**无需后训练与参数更新**（post-training-free）、**跨域对齐**（cross-domain alignment）和**模态独立性**（modality-free）。表1对已有方法进行了系统比较：

- **传统GNN**（如 **GCN** (Kipf & Welling, ICLR 2017)、**GAT** (Velickovic et al., ICLR 2018)、**GraphSAGE** (Hamilton et al., NeurIPS 2017)）和**自监督方法**（如 **GraphMAE** (Hou et al., NeurIPS 2022)、**DGI** (Velickovic et al., ICLR 2019)、**GraphCL** (You et al., NeurIPS 2020)）虽然模态无关，但缺乏跨域对齐能力，且需要在新任务上进行微调，无法实现参数更新自由的推理。

- **带后训练的GFM**（如 **GCOPE** (Zhao et al., 2024)、**GFT** (Wang et al., 2024b)、**AutoGFM** (Chen et al., 2025)、**GPF** (Fang et al., 2023)、**All in One** (Sun et al., 2023)）实现了跨域对齐，但依赖参数更新或提示学习，无法做到真正的后训练自由。

- **具有上下文学习能力的GFM**（如 **Prodigy** (Huang et al., 2023)、**OFA** (Liu et al., 2024a)、**GraphAlign** (Hou et al., 2024)）虽然部分满足ICL条件，但均依赖文本属性图（TAG）提供的模态信息，无法处理仅包含预编码特征与本地标签ID的任意图数据，因此不具备真正的模态无关性。

MF-GIA 是首个同时满足三项准则的方法，其核心突破在于用**梯度指纹**（gradient fingerprint）替代外部模态元数据作为域描述符，驱动跨域对齐。

### 2. 因果机制：梯度指纹如何驱动跨域对齐

MF-GIA 的因果调控旋钮是**梯度指纹**——从共享的固定初始化出发，对每个图进行单步梯度更新，得到的参数位移 $\Delta\theta_i$ 编码了该图的特征、标签与结构的联合分布特性。这一设计的深层逻辑在于：

- **无外部监督的域描述**：梯度指纹直接捕获图的内在属性如何影响模型学习，无需领域标签或文本描述。域嵌入器 $f_{\phi_{\mathrm{de}}}$ 将高维梯度指纹压缩为紧凑的域嵌入 $e_i$，并通过保持成对距离的损失 $\mathcal{L}_{\mathrm{de}}$ 确保嵌入空间保留域间相似性。

- **理论保证**：域嵌入满足 Lipschitz 型上界 $\| e_i - e_j \|_2 \leq \widetilde{C} \cdot \mathcal{W}_2(\mathcal{D}_i, \mathcal{D}_j)$，即相似域（Wasserstein-2距离小）映射到邻近子空间，保证对齐后的特征和标签具有语义连续性。

- **轻量对齐变换**：域嵌入参数化 FiLM 变换（缩放 + 平移），分别作用于特征空间和标签空间，将任意预编码的特征和本地标签ID投影到统一的语义空间，同时保持域内几何结构。这一设计避免了将异构特征统一到文本模态的中间步骤，实现了真正的模态无关对齐。

### 3. 训练范式：Episodic 元学习与双提示注意力

MF-GIA 采用完全 episodic 的元学习预训练范式，与推理时的少样本场景严格对齐。其核心组件**双提示感知注意力**（Dual Prompt-Aware Attention, DPAA）包含分离的特征侧与标签侧交叉注意力层：

- **特征侧注意力**：查询特征 $z_{i,q}$ 仅关注支持集特征矩阵 $\mathbf{Z}^{\mathrm{pmt}}$，获得提示感知的查询表示。
- **标签侧注意力**：提示增强的查询表示进一步关注域特定标签原型，生成最终匹配表示 $u_{i,q}^{\mathrm{out}}$。
- **最终预测**：通过 $s_{i,q} = u_{i,q}^{\mathrm{out}} (\mathbf{U}^{\mathrm{pmt}})^\top$ 计算各类别得分。

推理时所有参数冻结，仅依靠支持集进行 in-context 适应，真正实现参数更新自由的推理。

### 4. 适用边界与局限

尽管 MF-GIA 在跨域少样本节点分类和边分类上展示了强大的泛化能力，其适用边界仍需注意：

- **预训练语料多样性依赖**：消融实验表明，全四域预训练的总体准确率达60.73%，而单域预训练最高仅45.57%（Table 7），说明域多样性对泛化至关重要。当前仅使用四个基准数据集，更广泛多样的预训练语料可能进一步提升性能。

- **梯度指纹的稳定性约束**：指纹稳定性依赖于支持集大小，5-shot下同域指纹嵌入余弦相似度 >0.91（Table 11），但极端少样本（如1-shot）下指纹质量可能下降，影响域嵌入的可靠性。

- **推理开销**：推理时需为每个新图计算梯度指纹，带来额外的反向传播开销（尽管无参数更新），在实时性要求高的场景下可能成为瓶颈。

- **任务覆盖**：当前仅在节点和边分类任务上验证，尚未探索图级别预测、生成任务或异常检测。

- **分布偏移敏感性**：域嵌入的模板初始化和共享编码器可能对与预训练域完全不同的图分布敏感，在开放世界动态图场景下的持续适应能力尚未验证。

### 5. 开放问题

- **梯度指纹与LLM耦合**：如何将梯度指纹与大语言模型耦合，生成语义域描述并实现可解释的域总结，是提升模型可解释性的重要方向。

- **数据驱动的域发现**：能否利用梯度指纹自动发现大规模未标注图集合中的潜在域结构，实现无监督的域分解与增量学习。

- **高效域嵌入方案**：如何设计更高效的域嵌入方案（如基于采样的指纹近似、哈希投影等），以减少或避免推理时的梯度计算开销。

- **任务扩展**：MF-GIA 的模态无关对齐机制能否扩展到图分类、链接预测以外的任务（如图生成、异常检测），并保持对异构模态的鲁棒性。

- **谱理论连接**：梯度指纹与非欧结构的谱理论之间是否存在更深层的联系，能否指导更强大的对齐机制设计，值得进一步探索。

## 原文 PDF

![[paperPDFs/ICLR_2026/Modality_free_Graph_In_context_Alignment.pdf]]
