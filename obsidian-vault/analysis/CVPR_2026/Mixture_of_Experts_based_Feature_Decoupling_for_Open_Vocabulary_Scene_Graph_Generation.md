---
title: Mixture-of-Experts based Feature Decoupling for Open Vocabulary Scene Graph Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Mixture_of_Experts_based_Feature_Decoupling_for_Open_Vocabulary_Scene_Graph_Generation.pdf
project_link: null
code_link: "https://github.com/vacancy/SceneGraphParser"
aliases:
- MF
- MEBFDOVSGG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于混合专家（MoE）的自适应特征解耦机制，通过路由网络动态选择专家以突出关键属性，增强特征判别力。
primary_logic: 利用多个专家隐式解耦物体和关系的细粒度视觉语义属性（如形状、纹理、空间关系），并通过迭代交叉注意力实现物体与关系之间的双向语义交互，从而提升开放词汇场景下的类别辨别和关系三元组建模能力。
claims:
- MoE-FD在OvD-SGG设置下R@50/R@100较OvSGTR分别提升5.36%/5.78%。
- 在OvD+R-SGG全新颖设置下，MoE-FD在Novel Rel. R@20上超越ACC方法4.24%。
- 消融实验证实移除对象或关系特征解耦模块会显著降低性能，验证了MoE解耦的有效性。
- Visual Genome (OvD-SGG) 上 R@50 (Base+Novel Obj.) = 26.64
---

# Mixture-of-Experts based Feature Decoupling for Open Vocabulary Scene Graph Generation

> [!tip] 核心洞察
> 利用多个专家隐式解耦物体和关系的细粒度视觉语义属性（如形状、纹理、空间关系），并通过迭代交叉注意力实现物体与关系之间的双向语义交互，从而提升开放词汇场景下的类别辨别和关系三元组建模能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于混合专家的特征解耦开放词汇场景图生成 |
| 英文题名 | Mixture-of-Experts based Feature Decoupling for Open Vocabulary Scene Graph Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Mixture-of-Experts_based_Feature_Decoupling_for_Open_Vocabulary_Scene_Graph_Generation_CVPR_2026_paper.html) · [Code](https://github.com/vacancy/SceneGraphParser) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MoE-FD |
| Dataset | Visual Genome |

> [!tip] 效果简介
> - Visual Genome (OvD-SGG) 上，R@50 (Base+Novel Obj.) 26.64 vs 21.28 (OvSGTR) (+5.36)。
> - Visual Genome (OvD+R-SGG) 上，R@20 (Novel Rel.) N/A (但优于ACC) vs ACC (值未知) (+4.24%)；R@20 / R@50 / R@100 (Joint Base+Novel) 17.35 / 23.15 / 26.97。

## 概述

### 问题与瓶颈

开放词汇场景图生成（OVSGG）旨在从图像中检测新颖物体及其关系三元组，超越训练集类别限制。现有方法大多直接使用视觉语言模型（VLM）提取单一特征表示，并直接与候选标签进行语义对齐。这种做法存在两个关键缺陷：其一，缺乏对新颖物体与关系**判别性视觉语义属性**（如形状、纹理、空间配置）的提取能力，导致相似类别间混淆；其二，物体与关系特征**缺乏显式语义交互**，三元组关联建模薄弱，图像-文本对齐精度受限。

### 核心方法

针对上述瓶颈，本文提出**基于混合专家（MoE）的特征解耦框架 MoE‑FD**。其核心设计包括三个层面：

- **自适应特征解耦**：构建多组专家网络，通过路由网络动态计算专家权重，隐式解耦物体和关系的细粒度属性，增强特征判别力。
- **语义交互建模**：引入迭代交叉注意力机制，实现物体与关系特征的双向细化，强化三元组语义关联。
- **结构化语义先验**：将 ConceptNet 知识图谱融入路由网络，指导专家选择与新颖类别相关的属性，提升泛化能力。

### 方法谱系与知识库定位

MoE‑FD 属于**特征解耦 + 开放词汇分类**的方法谱系。其关键区别在于：不依赖额外标注数据扩增，而是通过 MoE 在特征空间内自适应增强判别属性。与主要对比基线 **OvSGTR**（Chen et al., ECCV 2024）直接使用单一 VLM 特征不同，MoE‑FD 将特征处理从“统一表示”转变为“多专家解耦—交叉交互—语义对齐”的流程。在 OvD+R‑SGG 设定下，MoE‑FD 亦优于 **ACC** 方法。

### 主要结果

- **OvD‑SGG 设定**：在 Visual Genome 测试集上，MoE‑FD 的 R@50 达到 26.64，较 OvSGTR 提升 **+5.36%**（R@100 提升 +5.78%）。
- **OvD+R‑SGG 设定**：在 Novel Rel. R@20 上超越 ACC **+4.24%**；在 Joint Base+Novel 关系指标上，R@20 / R@50 / R@100 分别达到 17.35 / 23.15 / 26.97。
- **消融实验**：移除对象特征解耦（obj.fd）或关系特征解耦（rel.fd）均导致性能显著下降，其中移除 obj.fd 下降更为明显；移除迭代特征细化模块（IFR）同样损害性能，证实了物体-关系交互的必要性。

### 局限与开放问题

MoE‑FD 依赖外部知识图谱 ConceptNet，其覆盖范围可能限制对极端新颖类别的泛化；当前框架采用固定数量的专家和查询，面对大规模开放世界场景可能不够灵活。未来可探索可学习的专家控制器（如大语言模型引导的动态选择）以及如何有效扩展专家数量以应对更多新颖类别。

## 背景与动机

场景图生成（SGG）旨在将图像解析为结构化图表示 $G = \{ V, E \}$，其中节点 $V$ 表示物体，边 $E$ 表示物体间的关系，从而为视觉理解提供紧凑的语义抽象。传统SGG方法受限于封闭词汇设定——训练和测试共享相同的物体与关系类别集合，无法应对现实场景中持续涌现的新类别。开放词汇场景图生成（OVSGG）应运而生，其目标是在训练集类别之外，检测新颖物体和/或关系，构成更具挑战性的泛化任务。

现有OVSGG方法的核心范式是直接利用视觉-语言模型（VLM）提取图像特征，并在语义空间中将视觉概念与候选类别标签对齐。然而，这一范式存在两个关键瓶颈。**第一，特征判别力不足。** VLM提取的单一特征表示缺乏对新颖物体和关系判别性属性的显式建模能力，难以捕捉形状、纹理、空间配置等细粒度视觉语义线索，导致相似类别之间容易发生混淆（如Figure 1(a)所示）。**第二，物体-关系语义交互缺失。** 现有方法通常将物体和关系独立进行语义对齐，忽视了二者之间的双向约束——物体的属性会影响关系的推断，反之亦然。这种割裂的建模方式削弱了关系三元组的语义一致性，限制了图像-文本对齐的精度。

针对上述问题，本文提出**基于混合专家（Mixture-of-Experts, MoE）的特征解耦框架MoE-FD**。核心动机是：通过多个专家网络隐式解耦物体和关系的细粒度视觉语义属性，并利用路由网络自适应地选择关键专家以突出判别性特征，从而增强模型对新颖类别的辨别能力。同时，引入迭代交叉注意力机制建模物体与关系之间的双向语义交互，强化三元组关联，提升开放词汇场景下的整体生成质量。Figure 1(b)展示了该框架与现有范式的本质差异——从简单的全局对齐转向关注细节属性的解耦式对齐。

## 核心创新

MoE-FD 的核心创新在于将**混合专家 (Mixture‑of‑Experts, MoE) 自适应特征解耦**引入开放词汇场景图生成 (OVSGG)，从根本上改变了现有方法对 VLM 特征的使用方式。与直接依赖单一 VLM 特征进行视觉‑语义对齐的基线方法（如 **OvSGTR** (Chen et al., ECCV 2024)）不同，MoE-FD 通过三个关键 changed slots 实现了判别力的跃升。

### 从单一表示到 MoE 驱动的判别性属性解耦

现有 OVSGG 方法仅简单利用 VLM 提取的全局特征表示，缺乏对新颖物体和关系判别性属性的提取能力，导致相似类别间容易混淆（Figure 1(a)）。MoE-FD 的核心突破在于**通过路由网络动态选择多个专家，隐式解耦物体和关系的细粒度视觉语义属性**（如形状、纹理、空间关系），从而突出关键判别特征（Figure 1(b)）。

具体而言，对象特征解耦通过知识引导的路由网络计算专家权重：

$$z_{o} = \mathrm{MLP}_{\mathrm{Route}}([n_i, C_{k,i}, \boldsymbol{r}]), \quad \alpha_k = \mathrm{Softmax}(z_o)_k \quad \forall k \in \{1,...,E_o\}$$

$$n_i^{*} = \sum_{k=1}^{E_o} \alpha_k \cdot \mathrm{Expert}_k^{\mathrm{obj}}(n_i)$$

关系特征解耦采用类似的 MoE 结构，路由网络根据边特征和语义先验 $\hat{C}_{k,ij}$ 输出权重 $\beta_m$，加权聚合多个关系专家的输出以更新边特征。这种自适应选择机制使模型能够针对不同类别激活最相关的专家——消融实验证实，移除对象特征解耦 (obj.fd) 或关系特征解耦 (rel.fd) 均导致性能显著下降，且移除 obj.fd 的下降更为明显 (Table 5)，验证了 MoE 解耦对判别力提升的关键作用。

### 从独立对齐到迭代交叉注意力的双向语义交互

基线方法中，物体和关系独立进行语义对齐，缺乏显式交互建模，导致关系三元组的语义关联薄弱。MoE-FD 引入了**迭代交叉注意力机制**，实现物体与关系特征的双向细化。首先通过节点对之间的交叉注意力更新边特征：

$$w_{i,j} = \mathrm{Softmax}\left(\frac{\varphi_Q(n_i) \cdot \varphi_K(n_j)^T}{\sqrt{d}}\right)$$

$$\boldsymbol{e}_{i,j}^{\prime} = \boldsymbol{e}_{i,j} + \mathrm{MLP}_{\mathrm{edge}}\left(w_{i,j} \cdot \phi(n_i + n_j)\right)$$

随后通过边到节点的反向注意力细化节点特征：

$$\gamma_{i,j} = \mathrm{Softmax}\left(\frac{\varphi_Q^{\prime}(\boldsymbol{e}_{i,j}^{\prime}) \cdot \varphi_K^{\prime}(n_i)^T}{\sqrt{d}}\right)$$

$$n_i^{\prime} = n_i + \mathrm{MLP}_{\mathrm{node}}\left(\sum_{j=1}^{K} \gamma_{i,j} \cdot \phi^{\prime}(\boldsymbol{e}_{i,j}^{\prime})\right)$$

该过程迭代四次，物体和关系特征各更新两次。消融实验表明，移除迭代特征细化模块 (IFR) 会损害性能 (Table 5)，证实了物体‑关系交互对场景图生成的必要性。

### 从无先验到 ConceptNet 语义先验引导的专家选择

MoE-FD 进一步将 **ConceptNet 结构化语义先验融入路由网络**，这是基线方法未利用的外部知识维度。语义先验 $C_{k,i}$ 和 $\hat{C}_{k,ij}$ 为路由网络提供类别间的语义关联线索，指导模型选择与新颖类别更相关的专家，从而缓解开放词汇场景下对未见类别的泛化瓶颈。这一设计在 OvD+R-SGG 全新颖设置下尤为关键——MoE-FD 在 Novel Rel. R@20 上超越 ACC 方法 4.24% (Table 3)，证明了知识引导的 MoE 路由对新颖关系辨别的增益。

### 创新总结

三个 changed slots 形成协同效应：MoE 解耦增强特征判别力，迭代交叉注意力强化三元组语义关联，ConceptNet 先验提升开放词汇泛化能力。这一组合使 MoE-FD 在 OvD-SGG 设置下 R@50/R@100 较 OvSGTR 分别提升 5.36%/5.78% (Table 1)，系统性解决了现有方法判别性不足和语义交互缺失的瓶颈。

## 整体框架

MoE-FD 的整体流程遵循“多模态特征提取 → 混合专家特征解耦 → 迭代特征细化 → 开放词汇分类与弱监督预训练”的级联结构，如 Figure 2 所示。给定输入图像 $I$ 和候选对象/关系类别集，模型首先提取视觉与文本特征并构建初始场景图，随后通过两个核心模块——基于 MoE 的特征解耦和迭代特征细化——交替增强节点与边的判别性语义表征，最终在语义空间完成开放词汇下的三元组推理。

![[assets/figures/papers/paper_list_l2547_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Mixture_of_Experts/figures/002_Figure_2.jpg]]
*Figure 2: Left: the framework of proposed MoE-FD; Right: the detail of two main components, i.e., Feature Decoupling via MoE and Iterative Feature Refinement*

### 多模态特征提取与场景图构建

视觉端采用 Swin Transformer 提取图像特征，文本端采用 BERT 编码类别标签，二者经 Transformer 上下文提取器融合后得到初始的节点特征 $n_i$ 和边特征 $\boldsymbol{e}_{i,j}$，构成场景图 $G = \{V, E\}$。这一阶段为后续模块提供统一的多模态表示基底。

### MoE 特征解耦

该模块是框架的核心创新，分为对象特征解耦和关系特征解耦两个子模块，分别针对节点和边进行细粒度属性分离。

**对象特征解耦** 通过知识引导的路由网络计算各对象专家权重：

$$z_{o} = \mathrm{MLP}_{\mathrm{Route}}([n_i, C_{k,i}, \boldsymbol{r}]), \quad \alpha_k = \mathrm{Softmax}(z_o)_k \quad \forall k \in \{1,...,E_o\}$$

其中 $C_{k,i}$ 为来自 ConceptNet 的语义先验，$\boldsymbol{r}$ 为关系查询向量。最终节点特征由 $E_o$ 个对象专家的输出加权求和得到：

$$n_i^{*} = \sum_{k=1}^{E_o} \alpha_k \cdot \mathrm{Expert}_k^{\mathrm{obj}}(n_i)$$

**关系特征解耦** 采用类似机制，路由网络根据边特征和语义先验 $\hat{C}_{k,ij}$ 输出权重 $\beta_m$，加权聚合 $E_r$ 个关系专家的输出以更新边特征 $\boldsymbol{e}_{i,j}^{*}$。消融实验表明，对象专家数设为 8、关系专家数设为 6 时性能最优。

### 迭代特征细化

该模块通过交叉注意力实现对象与关系之间的双向语义交互，共迭代四次（对象和关系各更新两次）。第一阶段，利用节点对交叉注意力更新边特征：

$$w_{i,j} = \mathrm{Softmax}\left(\frac{\varphi_Q(n_i) \cdot \varphi_K(n_j)^T}{\sqrt{d}}\right)$$

$$\boldsymbol{e}_{i,j}^{\prime} = \boldsymbol{e}_{i,j} + \mathrm{MLP}_{\mathrm{edge}}\left(w_{i,j} \cdot \phi(n_i + n_j)\right)$$

第二阶段，通过边到节点的反向注意力细化节点特征：

$$\gamma_{i,j} = \mathrm{Softmax}\left(\frac{\varphi_Q^{\prime}(\boldsymbol{e}_{i,j}^{\prime}) \cdot \varphi_K^{\prime}(n_i)^T}{\sqrt{d}}\right)$$

$$n_i^{\prime} = n_i + \mathrm{MLP}_{\mathrm{node}}\left(\sum_{j=1}^{K} \gamma_{i,j} \cdot \phi^{\prime}(\boldsymbol{e}_{i,j}^{\prime})\right)$$

消融实验证实，移除迭代特征细化模块会损害性能，验证了对象-关系交互的必要性。

### 开放词汇分类与弱监督预训练

细化后的节点和边特征在语义空间与候选类别标签计算相似度，采用二分图匹配进行多标签分配。训练时构建正负样本平衡集，优化二元交叉熵损失：

$$\mathcal{L} = -\mathbb{E}[y \log \sigma(s) + (1-y) \log (1-\sigma(s))]$$

为缓解稀有关系的数据稀疏问题，框架引入弱监督预训练策略：利用依赖解析器从图像描述中自动解析关系三元组，再通过二分图匹配与检测到的对象对齐，使模型在预训练阶段获得更丰富的关系语义先验。

### 输入输出流总结

- **输入**：图像 $I$ + 候选对象/关系类别标签文本。
- **中间表示**：Swin Transformer 视觉特征 + BERT 文本特征 → 融合后的初始节点/边特征 → MoE 解耦后的判别性特征 → 迭代细化后的语义对齐特征。
- **输出**：开放词汇场景图 $G = \{V, E\}$，包含对象节点类别和关系边类别预测。

### 补充图表

![[assets/figures/papers/paper_list_l2547_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Mixture_of_Experts/figures/001_Figure.jpg]]
*Figure: (a) Framework of existing OVSGG method. (b) Framework of the proposed method*

## 核心模块与公式推导

MoE-FD 的核心由三个紧密耦合的模块构成：**多模态特征提取**、**基于 MoE 的特征解耦**以及**迭代特征细化**。其中，特征解耦模块是提升开放词汇场景下判别能力的关键瓶颈突破点，而迭代细化模块则负责建模物体与关系之间的双向语义交互。

### 多模态特征提取

给定输入图像 $I$，首先采用 Swin Transformer 提取视觉特征，同时使用 BERT 编码候选物体和关系类别的文本标签。随后，通过一个 Transformer 上下文提取器融合多模态信息，得到初始的节点特征 $n_i$（对应物体 $i$）和边特征 $\boldsymbol{e}_{i,j}$（对应物体对 $(i,j)$ 之间的关系）。这些特征作为后续解耦与细化模块的输入。

### MoE 特征解耦

该模块是方法的核心创新，旨在通过多个专家网络隐式解耦物体和关系的细粒度视觉语义属性（如形状、纹理、空间关系等），并通过路由网络动态选择关键专家以增强特征判别力。

**对象特征解耦** 采用知识引导的路由网络。对于每个物体节点 $i$，将其节点特征 $n_i$、来自 ConceptNet 的语义先验 $C_{k,i}$ 以及一个可学习的关系查询向量 $\boldsymbol{r}$ 拼接后输入路由 MLP，经 Softmax 得到 $E_o$ 个对象专家的权重：

$$z_{o} = \mathrm{MLP}_{\mathrm{Route}}([n_i, C_{k,i}, \boldsymbol{r}]), \quad \alpha_k = \mathrm{Softmax}(z_o)_k \quad \forall k \in \{1,...,E_o\}$$

更新后的节点特征为各专家输出的加权求和：

$$n_i^{*} = \sum_{k=1}^{E_o} \alpha_k \cdot \mathrm{Expert}_k^{\mathrm{obj}}(n_i)$$

**关系特征解耦** 采用类似的路由机制。对于边特征 $\boldsymbol{e}_{i,j}$，路由网络根据边特征本身和语义先验 $\hat{C}_{k,ij}$ 计算 $E_r$ 个关系专家的权重：

$$\boldsymbol{z}_r = \mathrm{MLP}_{\mathrm{Route}}(\boldsymbol{e}_{i,j}, \hat{C}_{k,ij}), \quad \beta_m = \mathrm{Softmax}(\boldsymbol{z}_r)_m \quad \forall m \in \{1,...,E_r\}$$

更新后的边特征为：

$$\boldsymbol{e}_{i,j}^{*} = \sum_{m=1}^{E_r} \beta_m \cdot \mathrm{Expert}_m^{\mathrm{rel}}(\boldsymbol{e}_{i,j})$$

消融实验证实，移除对象特征解耦（obj.fd）或关系特征解耦（rel.fd）均会导致性能显著下降，且移除 obj.fd 的下降幅度更为明显，验证了 MoE 解耦机制的有效性。超参数分析表明，当对象专家数为 8、关系专家数为 6 时模型性能最优。

### 迭代特征细化

该模块通过迭代交叉注意力实现物体与关系特征的双向语义交互，增强三元组关联。整个过程交替进行两个阶段，共迭代四次（物体特征和关系特征各更新两次）。

**阶段一：节点到边的注意力更新。** 首先计算节点对 $(i,j)$ 之间的交叉注意力权重：

$$w_{i,j} = \mathrm{Softmax}\left(\frac{\varphi_Q(n_i) \cdot \varphi_K(n_j)^T}{\sqrt{d}}\right)$$

随后利用该权重聚合节点值特征，更新边特征：

$$\boldsymbol{e}_{i,j}^{\prime} = \boldsymbol{e}_{i,j} + \mathrm{MLP}_{\mathrm{edge}}\left(w_{i,j} \cdot \phi(n_i + n_j)\right)$$

**阶段二：边到节点的注意力细化。** 计算节点 $i$ 对其相邻边 $j$ 的注意力权重：

$$\gamma_{i,j} = \mathrm{Softmax}\left(\frac{\varphi_Q^{\prime}(\boldsymbol{e}_{i,j}^{\prime}) \cdot \varphi_K^{\prime}(n_i)^T}{\sqrt{d}}\right)$$

然后聚合相邻边特征的加权和，更新节点特征：

$$n_i^{\prime} = n_i + \mathrm{MLP}_{\mathrm{node}}\left(\sum_{j=1}^{K} \gamma_{i,j} \cdot \phi^{\prime}(\boldsymbol{e}_{i,j}^{\prime})\right)$$

消融实验表明，移除迭代特征细化模块（IFR）会损害模型性能，证明物体与关系特征之间的交互对于场景图生成是必要的。

### 开放词汇分类与训练

经过解耦和细化后的节点特征 $n_i^{\prime}$ 和边特征 $\boldsymbol{e}_{i,j}^{\prime}$ 在语义空间中与候选类别标签计算相似度，采用二分图匹配策略进行多标签分配。训练时构建正负样本平衡集，优化二元交叉熵损失：

$$\mathcal{L} = -\mathbb{E}[y \log \sigma(s) + (1-y) \log (1-\sigma(s))]$$

其中 $y$ 为样本标签，$s$ 为相似度得分。此外，方法还引入弱监督预训练范式：利用依存句法解析器从图像描述中自动解析关系三元组，通过二分图匹配与检测到的物体对齐，从而缓解稀有关系的数据稀疏问题。

### 补充图表

![[assets/figures/papers/paper_list_l2547_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Mixture_of_Experts/figures/008_Figure_3.jpg]]
*Figure 3: Visualized activation of relation/object experts*

## 实验与分析

### 评估设置与基准

为系统验证 MoE-FD 在开放词汇场景图生成中的有效性，作者在 Visual Genome（VG）数据集上构建了三种典型开放词汇设置：**OvD-SGG**（新颖物体检测，关系类别固定）、**OvR-SGG**（新颖关系预测，物体类别固定）以及 **OvD+R-SGG**（物体与关系同时新颖）。模型采用 Swin Transformer 作为视觉骨干、BERT 作为文本编码器，训练使用 SGD 优化器，初始学习率 0.001，动量 0.9，batch size 为 8，每 epoch 学习率衰减 0.9。迭代交叉注意力执行 4 次，即物体特征和关系特征各更新两轮。

### 主实验结果

**OvD-SGG 设置。** 在物体检测解耦场景下，MoE-FD 在 Base+Novel 物体的 R@50 上达到 26.64%，较现有方法 **OvSGTR**（Chen et al., ECCV 2024）提升 **5.36 个百分点**，R@100 提升 5.78%（Table 1）。在仅评估新颖物体的 R@50 上，MoE-FD 达到 20.94%，表明 MoE 特征解耦对未见类别具有显著的判别力增强作用。

**OvR-SGG 设置。** 在关系解耦场景下，MoE-FD 同样展现出稳定的性能优势（Table 2），验证了关系专家网络对细粒度关系语义属性（如空间关系、动作交互）的有效建模。

**OvD+R-SGG 设置。** 在最具挑战性的全开放场景下，MoE-FD 在 Joint Base+Novel 的 R@20/R@50/R@100 分别达到 17.35/23.15/26.97（Table 3）。在 Novel Rel. 的 R@20 上，MoE-FD 超越 **ACC** 方法 **4.24 个百分点**，证明双向迭代交叉注意力机制有效强化了“物体-关系-物体”三元组的语义关联。

### 消融实验

Table 5 的消融实验揭示了各组件的因果贡献：

![[assets/figures/papers/paper_list_l2547_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Mixture_of_Experts/figures/009_Table_5.jpg]]
*Table 5: Experimental results of ablation feature decoupling experts of object (FD(Obj)), relationship (FD(Rel)), and iterative feature refinement(IFR) module*

- **移除对象特征解耦（obj.fd）** 导致性能大幅下降，且下降幅度超过移除关系特征解耦（rel.fd），说明物体属性的细粒度解耦对开放词汇识别更为关键。
- **移除迭代特征细化模块（IFR）** 同样显著损害性能，证实物体与关系之间的双向语义交互是场景图生成的必要条件——仅靠单向特征提取无法充分建模三元组内部的语义一致性。
- **专家数量配置。** 当对象专家数设为 8、关系专家数设为 6 时，模型性能达到最优（Figure 4）。过少的专家难以覆盖多样化的视觉语义属性，过多则可能引入冗余或路由噪声。
- **知识选择阈值。** 引入 ConceptNet 语义先验时，阈值 ϵ 设为 0.7 取得最佳效果（Figure 4），表明适度的外部知识引导有助于路由网络选择相关专家，但过度依赖先验可能限制对新颖类别的自适应能力。

### 预训练策略对比

Table 4 展示了弱监督预训练策略的效果。MoE-FD 利用图像描述解析关系三元组进行预训练，在 VG150 测试集上直接评估时展现出竞争力，该预训练模型随后被用于 OvD+R-SGG 设置的初始化。这一策略有效缓解了稀有关系的数据稀疏问题，使模型在未见关系类别上具备更强的泛化基础。

![[assets/figures/papers/paper_list_l2547_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Mixture_of_Experts/figures/006_Table_4.jpg]]
*Table 4: Comparison with pre-training methods. All models are pre-trained on image-caption data and tested on VG150 test set directly. Our models trained on COCO captions are used as pre-trained models for OvD+R-SGG settings*

### 可视化分析

**Figure 3** 展示了关系专家和对象专家的激活模式。不同专家对不同语义属性（如形状、纹理、空间关系）呈现差异化的激活分布，直观验证了 MoE 路由网络能够隐式解耦并选择性激活与当前输入最相关的判别性属性。这解释了为何 MoE-FD 在相似类别易混淆的开放词汇场景下具有更强的辨别能力。

### 失败模式与局限性

尽管 MoE-FD 在多个设置下取得显著提升，仍存在以下局限：
1. **外部知识依赖。** 路由网络依赖 ConceptNet 提供语义先验，当新颖类别在知识图谱中覆盖不足时，专家选择可能偏离最优，泛化能力受限。
2. **固定专家架构。** 当前采用固定数量的专家和查询，面对大规模开放世界场景时缺乏灵活扩展能力，可能导致部分长尾类别无法获得足够的专家容量。
3. **计算开销。** 多专家并行计算和迭代交叉注意力增加了推理时的计算负担，在实时场景图生成应用中可能成为瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2547_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Mixture_of_Experts/figures/003_Table_1.jpg]]
*Table 1: Experimental results of OvD setting on VG test set*

![[assets/figures/papers/paper_list_l2547_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Mixture_of_Experts/figures/004_Table_2.jpg]]
*Table 2: Experimental results of OvR-SGG setting on VG test set*

![[assets/figures/papers/paper_list_l2547_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Mixture_of_Experts/figures/005_Table_3.jpg]]
*Table 3: Experimental results of OvD+R-SGG setting on VG test set*

![[assets/figures/papers/paper_list_l2547_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Mixture_of_Experts/figures/007_Table.jpg]]

## 方法谱系与知识库定位

### 1. 与现有方法的继承与差异

MoE-FD 直接继承自开放词汇场景图生成（OVSGG）这一任务线，其最核心的对比基线是 **OvSGTR**（Chen et al., ECCV 2024）。OvSGTR 代表了现有 OVSGG 方法的典型范式：利用视觉-语言模型（VLM）提取视觉特征，然后在语义空间中与类别标签进行对齐。然而，OvSGTR 仅使用单一的 VLM 特征表示，缺乏对新颖物体和关系判别性属性的提取能力，且物体与关系之间无显式的语义交互建模。

MoE-FD 在三个关键维度上对基线进行了根本性改造：

- **特征处理方式**：从直接使用 VLM 单一特征，转变为通过 MoE 路由网络自适应选择专家，对物体和关系特征进行解耦，突出关键视觉语义属性（如形状、纹理、空间关系）。
- **物体-关系交互机制**：从物体和关系独立进行语义对齐，转变为引入迭代交叉注意力机制，实现物体和关系特征的双向细化，增强三元组语义关联。
- **先验知识利用**：从未使用结构化外部知识，转变为将 ConceptNet 语义先验融入路由网络，指导专家选择与新颖类别相关的属性。

在 OvD+R-SGG 设置下，MoE-FD 还与 **ACC** 方法进行了对比，并在 Novel Rel. R@20 上超越 ACC 4.24%。此外，MoE-FD 复用了 **SceneGraphParser**（, 2022）作为弱监督预训练阶段的依赖解析工具，用于从图像描述中自动解析关系三元组。

### 2. 适用边界与条件依赖

MoE-FD 的有效性依赖于以下边界条件：

- **知识图谱覆盖**：模型依赖 ConceptNet 提供语义先验来指导路由网络。ConceptNet 的覆盖范围直接影响模型对新颖类别的泛化能力——对于 ConceptNet 中缺失或稀疏的概念，路由网络可能无法有效选择相关专家。
- **专家数量固定**：当前框架采用固定数量的对象专家（最优为 8）和关系专家（最优为 6）。在面对大规模开放世界场景时，固定的专家容量可能不足以覆盖所有细粒度属性的解耦需求。
- **查询数量固定**：路由网络中的关系查询 r 为固定设计，限制了模型对动态变化的新颖类别集合的自适应能力。
- **弱监督预训练依赖**：模型在 OvD+R-SGG 设置下的性能部分受益于 COCO Captions 上的弱监督预训练。若缺乏大规模图像-描述数据，稀有关系的数据稀疏问题可能加剧。

### 3. 局限性与待解决问题

**已验证的局限**：

1. **外部知识依赖**：ConceptNet 的覆盖范围有限，可能成为模型泛化的瓶颈。当面对 ConceptNet 未覆盖的新颖类别时，知识引导的路由机制可能退化。
2. **固定容量架构**：对象专家数（Eo=8）和关系专家数（Er=6）为固定超参数，缺乏对输入复杂度的动态适配能力。

**开放问题**：

1. **可学习的专家控制器**：如何采用强化学习或大语言模型引导的动态专家选择机制，替代当前的固定路由网络，以提升对更广泛新类别的自适应能力？
2. **专家数量扩展**：当物体查询和专家数量固定时，如何有效扩展到更多新颖类别？是否可以通过层次化专家架构或条件计算来突破容量瓶颈？
3. **知识图谱替代方案**：能否通过自监督方式从大规模图文数据中学习语义先验，减少对 ConceptNet 的硬依赖？

> **注意**：以上开放问题源自论文自身的讨论，部分推断（如层次化专家架构）需结合后续工作手动验证，论文未提供相关实验证据。

## 原文 PDF

![[paperPDFs/CVPR_2026/Mixture_of_Experts_based_Feature_Decoupling_for_Open_Vocabulary_Scene_Graph_Generation.pdf]]
