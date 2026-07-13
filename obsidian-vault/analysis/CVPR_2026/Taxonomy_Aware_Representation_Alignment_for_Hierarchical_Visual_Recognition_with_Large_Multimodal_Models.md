---
title: Taxonomy-Aware Representation Alignment for Hierarchical Visual Recognition with Large Multimodal Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Taxonomy_Aware_Representation_Alignment_for_Hierarchical_Visual_Recognition_with_Large_Multimodal_Models.pdf
project_link: null
code_link: "https://github.com/PKU-ICST-MIPL/TARA_CVPR2026"
aliases:
- TTARA
- TARAHVRLMM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将LMMs的中间视觉表征和回答嵌入与预训练生物基础模型（BFMs）的分类感知表征对齐。
primary_logic: 通过简单地对齐LMMs与BFMs的表征，可有效注入分类学知识，在无需推理时额外模块的情况下，显著提升层次一致性和对已知及新颖类别的泛化能力。
claims:
- TARA consistently enhances LMMs’ hierarchical consistency and leaf node accuracy.
- TARA yields consistent gains over RL-only baseline across metrics on iNat-Plant and iNat-Animal.
- TARA improves Order F1 and Family F1 on TerraIncognita known and novel species.
- TARA achieves faster convergence and surpasses baseline early in training.
---

# Taxonomy-Aware Representation Alignment for Hierarchical Visual Recognition with Large Multimodal Models

> [!tip] 核心洞察
> 通过简单地对齐LMMs与BFMs的表征，可有效注入分类学知识，在无需推理时额外模块的情况下，显著提升层次一致性和对已知及新颖类别的泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 分类感知表征对齐：面向大规模多模态模型的层次视觉识别 |
| 英文题名 | Taxonomy-Aware Representation Alignment for Hierarchical Visual Recognition with Large Multimodal Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.00431) · [Code](https://github.com/PKU-ICST-MIPL/TARA_CVPR2026) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TARA (Taxonomy-Aware Representation Alignment) |
| Dataset | iNat21-Plant, iNat21-Animal, TerraIncognita |

> [!tip] 效果简介
> - iNat21-Plant 上，Hierarchical Consistent Accuracy (HCA) 12.78 vs 9.23 (RL only) (+3.55)；Strict Path Overlap Ratio (S-POR) 55.98 vs 50.81 (RL only) (+5.17)。
> - iNat21-Animal 上，HCA 10.26 vs 8.57 (RL only) (+1.69)。
> - TerraIncognita (Known) 上，Order F1 55.61 vs 37.35 (RL only) (+18.26)。

## 概要

层次视觉识别（Hierarchical Visual Recognition, HVR）要求模型不仅识别细粒度类别，还需给出从根节点到叶节点的完整分类路径，并保持路径内各层预测的层次一致性。大规模多模态模型（LMMs）在常规视觉问答中表现优异，但在HVR场景下暴露出严重缺陷：其内部表征未能充分编码分类学层次结构，导致预测路径违反父子约束，尤其对训练中未见过的新颖类别，层次一致性急剧下降。

针对这一瓶颈，本文提出**TARA（Taxonomy-Aware Representation Alignment）**，一种简单高效的训练框架。核心思路是将LMMs的中间视觉表征和回答嵌入，分别与预训练生物基础模型（BFMs，如BioCLIP）的视觉和文本特征进行对齐，从而将BFMs蕴含的分类学知识注入LMMs。TARA与“无思考”强化微调（No-Thinking RFT）交替进行，在训练时通过余弦相似度损失拉近LMMs与BFMs的表征空间；推理时BFMs和投影器被完全丢弃，不引入任何额外参数或计算开销。

实验表明，TARA在已知类别和新颖类别上均带来一致且显著的增益：在iNat21-Plant数据集上，层次一致性准确率（HCA）从9.23%提升至12.78%，严格路径重叠比（S-POR）从50.81%提升至55.98%；在TerraIncognita数据集的已知物种上，目级F1分数从37.35%跃升至55.61%，新颖物种上从29.78%提升至39.93%。消融实验证实，视觉对齐损失和标签对齐损失各自贡献明确，且使用全部视觉token与首回答token的对齐策略为最优。此外，TARA在训练效率上也展现出更快的收敛速度。

方法定位上，TARA属于**表征对齐 + 强化微调**的混合训练范式，区别于需要推理时额外模块或复杂提示工程的方法。其知识来源为预训练BFMs，基座模型为Qwen系列LMMs，目前验证范围限于生物分类学领域。



### 层次视觉识别的核心挑战

层次视觉识别（Hierarchical Visual Recognition, HVR）要求模型不仅识别物体的最细粒度类别（如物种），还需在分类学层次结构的每一层（如门、纲、目、科、属、种）上给出一致的预测。形式化地，给定一个分类树 $\mathcal{T} = (\mathcal{V}, \mathcal{E})$，其中 $\mathcal{V}$ 为类别节点集，$\mathcal{E} \subseteq \mathcal{V} \times \mathcal{V}$ 编码父子关系，HVR 的目标是为输入图像预测一条从根节点到叶节点的完整路径，且路径上的每一跳都必须满足层次约束。

大规模多模态模型（Large Multimodal Models, LMMs）在通用视觉理解任务上展现出强大能力，但在 HVR 场景下暴露出一个关键瓶颈：**层次一致性严重不足**。如 Figure 1 所示，LMMs 在已知类别和全新类别上均频繁违反分类学层次约束——模型可能在叶节点给出正确预测，但在中间层级（如科、目）上出现与叶节点预测逻辑矛盾的输出。这种不一致性源于 LMMs 的内部表征未能充分编码分类学层次结构，模型缺乏对“预测路径必须符合树结构”这一先验的隐式建模能力。

### 现有方法的局限

当前提升 LMMs 层次识别能力的代表性方案是**强化微调（Reinforcement Fine-Tuning, RFT）**，例如 **No-Thinking RFT**（Li et al., arXiv 2025）。该方法通过构造准确性奖励信号，引导模型在已知类别上学习更准确的叶节点预测。然而，RFT 存在两个根本性缺口：

1. **缺乏显式的层次结构注入**：RFT 仅优化最终答案的正确性，未对中间层级的表征施加任何结构化约束，导致模型学到的内部表征仍缺乏分类学归纳偏置。
2. **新颖类别泛化能力弱**：当面对训练中未见过的物种时，RFT 无法提供有效的层次知识迁移机制，模型在新类别上的层次一致性提升有限。

### 核心动机：从生物基础模型注入分类学知识

与 LMMs 相对，**生物基础模型（Biology Foundation Models, BFMs）** 如 **BioCLIP**（Stevens et al., CVPR 2024）和 **BioCLIP2**（Gu et al., arXiv 2025）在大规模生物分类数据上预训练，其视觉和文本编码器天然具备分类感知的表征能力——相近类别的嵌入在特征空间中更为接近，隐式反映了分类学层次结构。

本文的核心洞察在于：**如果能将 BFMs 的分类感知表征对齐到 LMMs 的中间表示中，就能在不增加推理开销的前提下，将分类学知识有效注入 LMMs**。这一思路绕过了直接修改 LMM 架构或引入外部知识图谱的复杂性，转而利用现成 BFMs 作为“知识教师”，通过表征对齐实现知识迁移。

### TARA 的动机定位

基于上述分析，本文提出 **TARA（Taxonomy-Aware Representation Alignment）**，一个简单但有效的训练框架。TARA 在 No-Thinking RFT 的基础上，通过两个余弦相似度对齐损失，分别将 LMMs 的中间视觉表征和回答嵌入与 BFMs 的对应表征对齐，从而在微调过程中显式注入分类学层次知识。推理时，BFMs 和对齐投影器被完全丢弃，LMMs 直接执行 HVR，无额外参数或计算开销。



## 核心方法与创新机理

TARA 的核心创新在于**首次将大规模多模态模型（LMMs）的层次视觉识别能力，通过表征对齐的方式与预训练生物基础模型（BFMs）的分类学知识建立连接**。与现有方法在推理时引入外部模块或依赖复杂提示工程不同，TARA 将层次一致性直接注入模型的内部表征空间，且推理时无任何额外开销。

### 问题瓶颈与因果调控点

LMMs 在层次视觉识别（HVR）中的根本瓶颈在于：其内部表征未能充分编码分类学层次结构，导致模型在新颖类别上尤其缺乏层次一致性。TARA 的因果调控点明确——**将 LMMs 的中间视觉表征和回答嵌入与 BFMs 的分类感知表征对齐**。通过这一简单的对齐操作，分类学知识被有效注入 LMMs，显著提升了对已知和新颖类别的层次一致性及泛化能力。

### 关键改变槽位

相较于仅使用 No-Thinking RFT（Li et al., arXiv 2025）的基线方法，TARA 在以下四个关键槽位进行了创新性改变：

**1. 训练目标：从单一奖励到交替优化**

基线方法仅使用准确率奖励进行强化微调，而 TARA 采用**交替优化策略**——在 No-Thinking RFT 与分类感知表征对齐之间交替进行。对齐损失由视觉对齐损失 $\mathcal{L}_V$ 和标签对齐损失 $\mathcal{L}_C$ 组成，整体对齐损失为二者的均值：

$$\mathcal{L}_{\mathrm{alignment}} = (\mathcal{L}_{\mathrm{V}} + \mathcal{L}_{\mathrm{C}}) / 2$$

这一交替机制使得模型在保持准确率优化的同时，逐步内化分类学的层次结构知识。

**2. 视觉特征对齐：从无约束到分类学引导**

基线方法对 LMM 的视觉特征无任何分类学约束。TARA 引入视觉对齐损失 $\mathcal{L}_V$，通过余弦相似度将投影后的 LMM 视觉特征与 BFM 视觉特征对齐：

$$\mathcal{L}_{\mathrm{V}} = - \frac{1}{N} \sum_{i=1}^{N} \mathrm{sim}\Bigl(P_{\mathrm{V}}(\mathbf{e}_{\ell,i}^{\mathrm{img}}), \mathbf{y}_{i}^{\mathrm{img}}\Bigr)$$

其中 $P_V$ 为轻量级 MLP 视觉投影器，$\mathbf{e}_{\ell,i}^{\mathrm{img}}$ 为 LMM 第 $\ell$ 层视觉隐状态，$\mathbf{y}_{i}^{\mathrm{img}}$ 为 BFM 的目标视觉特征。这一损失强制 LMM 的视觉编码器学习更具分类学区分度的表征。

**3. 回答表征对齐：从无约束到标签语义引导**

基线方法对回答 token 的嵌入无任何语义约束。TARA 引入标签对齐损失 $\mathcal{L}_C$，将 LMM 的首个回答 token 嵌入与 BFM 文本编码器生成的类别标签嵌入对齐：

$$\mathcal{L}_{\mathrm{C}} = - \mathrm{sim}\left(P_{\mathrm{T}}(\mathbf{e}_{m,0}^{\mathrm{answer}}), \mathbf{y}^{\mathrm{label}}\right)$$

其中 $P_T$ 为文本投影器，$\mathbf{e}_{m,0}^{\mathrm{answer}}$ 为 LMM 第 $m$ 层首个回答 token 的隐状态，$\mathbf{y}^{\mathrm{label}}$ 为 BFM 的文本标签嵌入。这一设计将分类学标签的语义信息直接注入 LMM 的生成过程。

**4. 推理开销：从增加模块到零额外参数**

许多现有方法在推理时依赖额外的视觉编码器、知识图谱或检索模块，增加了计算负担。TARA 的关键设计在于：**BFMs 和投影器仅在训练阶段使用，推理时被完全丢弃**，LMM 直接进行层次视觉识别，无需任何额外参数或计算。

### 方法谱系与知识库定位

TARA 位于**知识蒸馏与表征对齐**的方法谱系中，但其独特之处在于将知识源从单一教师模型扩展到预训练生物基础模型（BFMs）。作为教师模型的 **BioCLIP**（Stevens et al., CVPR 2024）和 **BioCLIP2**（Gu et al., arXiv 2025）具备丰富的分类学视觉-文本对齐知识，TARA 通过表征层面的对齐将这些知识迁移至 LMMs。

与传统的知识蒸馏不同，TARA 的对齐发生在**中间表征层**而非输出 logits 层，且同时覆盖视觉和文本两个模态。这种方法与对比学习中的多模态对齐（如 CLIP 系列）有形式上的相似性，但目标不同：TARA 的对齐是为了注入分类学层次结构，而非通用的图文匹配能力。

在层次分类的方法谱系中，TARA 属于**训练时注入层次知识**的范式，区别于推理时使用层次约束（如层次 softmax、层次推理路径）的方法。其优势在于不改变推理流程，且层次知识被内化为模型表征的一部分，具有更好的泛化性。

### 设计决策的证据强度

消融实验（Table 3）为关键设计决策提供了强证据支持：
- 单独添加 $\mathcal{L}_V$ 相较于纯 RL 基线可提升层次一致性；
- 进一步添加 $\mathcal{L}_C$ 在 $\mathcal{L}_V$ 基础上将 HCA 提升约 2.06%（置信度 0.95）；
- 视觉层 14 和文本层 28 的对齐组合产生最佳 HCA（置信度 0.95）；
- 使用所有视觉 token 计算 $\mathcal{L}_V$ 和首个回答 token 计算 $\mathcal{L}_C$ 为最优配置（Table 4，置信度 0.95）。

这些消融结果表明，TARA 的每个组件和设计选择均经过充分验证，并非启发式堆叠。



TARA（Taxonomy-Aware Representation Alignment）的整体训练框架遵循**交替优化**策略，将分类学感知的表征对齐与无思考强化微调（No-Thinking RFT）交织进行，其核心设计如图2所示。

### 框架总览

整个pipeline包含三个关键角色：待微调的**大规模多模态模型（LMM）**、提供分类学知识的**生物基础模型（BFM）**教师，以及两个轻量级**MLP投影器**（$P_V$ 和 $P_T$）。训练时，LMM与两个投影器被联合更新，而BFMs保持冻结；推理时，BFMs和投影器均被丢弃，LMM直接接受提示并执行层次视觉识别（HVR），因此**推理阶段不引入任何额外参数或计算开销**。

### 数据流与模块关系

框架的输入是一张图像及其对应的分类学标签。数据流分为两条并行的对齐路径，与RFT交替执行：

1. **视觉表征对齐路径**：图像同时送入LMM的视觉编码器和BFM的视觉编码器。从LMM的中间视觉层提取图像token特征 $\mathbf{e}_{\ell,i}^{\text{img}}$，经视觉投影器 $P_V$ 映射后，与BFM产生的视觉目标特征 $\mathbf{y}_i^{\text{img}}$ 计算余弦相似度损失 $\mathcal{L}_V$（公式1）。该路径强制LMM的内部视觉表征向BFM的分类学感知表征靠拢。

2. **标签表征对齐路径**：LMM生成回答后，取其首个回答token的隐藏状态 $\mathbf{e}_{m,0}^{\text{answer}}$，经文本投影器 $P_T$ 映射，与BFM文本编码器对类别标签的嵌入 $\mathbf{y}^{\text{label}}$ 计算余弦相似度损失 $\mathcal{L}_C$（公式2）。该路径确保LMM输出的语义表征与分类学标签结构对齐。

3. **RFT路径**：在交替的步骤中，模型执行标准的无思考RFT，使用“{Question} Please directly output the answer.”格式的提示，以准确率奖励优化层次分类能力。

### 交替优化机制

训练采用**交替优化方案**：在每一步中，TARA的对齐损失 $\mathcal{L}_{\text{alignment}} = (\mathcal{L}_V + \mathcal{L}_C) / 2$ 与No-Thinking RFT损失轮流更新LMM和两个投影器。这种设计使模型既能从BFMs吸收分类学结构知识，又能通过强化学习保持任务导向的判别能力，同时避免两种损失直接冲突。

### 关键设计决策

- **对齐目标层级**：视觉对齐在LMM的第14层和BFM的对应视觉层进行，标签对齐在LMM的第28层和BFM的文本层进行——消融实验表明该组合在层次一致性指标（HCA）上最优。
- **特征粒度**：$\mathcal{L}_V$ 使用所有视觉token的平均特征，$\mathcal{L}_C$ 仅使用首个回答token——消融证实该配置在效率和效果间取得最佳平衡。
- **推理零开销**：BFMs和投影器仅在训练阶段作为知识桥梁存在，推理时完全移除，LMM以标准方式运行，这是TARA实用性的核心优势。

### 补充图表

![[assets/figures/papers/paper_list_l2750_https_arxiv_org_abs_2603_00431/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the training framework. Taxonomy-Aware Representation Alignment (TARA) is conducted alternately with No-Thinking RFT to improve the hierarchical recognition performance of LMMs with taxonomic knowledge absorbed from BFMs*



### 3.1 问题形式化：层次视觉识别（HVR）

给定一张图像 $x$ 和一个层次分类学 $\mathcal{T} = (\mathcal{V}, \mathcal{E})$，其中 $\mathcal{V}$ 为类别节点集合，$\mathcal{E} \subseteq \mathcal{V} \times \mathcal{V}$ 为编码父子关系的有向边集。HVR 的目标是从根节点开始，逐层预测一条完整路径，直至叶节点。核心挑战在于，LMM 的内部表征未能充分编码分类学层次结构，导致预测路径违反层次一致性——尤其在面对新颖类别时，这一问题更为突出。

### 3.2 核心洞察与因果机制

TARA 的核心洞察在于：**通过将 LMM 的中间视觉表征和回答嵌入与预训练生物基础模型（BFMs）的分类感知表征对齐，可有效注入分类学知识，在无需推理时额外模块的情况下，显著提升层次一致性和泛化能力。**

其因果机制可拆解为两步：
1. **视觉表征对齐**：迫使 LMM 的视觉编码器学习 BFMs 中蕴含的分类学视觉结构，使模型“看到”的类别特征天然带有层次关系。
2. **回答表征对齐**：迫使 LMM 在生成答案时，其首个 token 的隐藏状态与 BFMs 的类别文本嵌入一致，使模型“说出”的类别标签在语义空间中遵循分类学距离。

### 3.3 关键模块与公式

TARA 框架由三个核心损失函数驱动，训练时交替执行对齐与强化微调。

#### 3.3.1 分类学视觉表征对齐损失 $\mathcal{L}_{\mathrm{V}}$

$$\mathcal{L}_{\mathrm{V}} = -\frac{1}{N}\sum_{i=1}^{N}\mathrm{sim}\Bigl(P_{\mathrm{V}}(\mathbf{e}_{\ell,i}^{\mathrm{img}}), \mathbf{y}_{i}^{\mathrm{img}}\Bigr)$$

**变量含义**：
- $\mathbf{e}_{\ell,i}^{\mathrm{img}}$：LMM 第 $\ell$ 层输出的第 $i$ 个图像 token 的隐藏状态。
- $P_{\mathrm{V}}(\cdot)$：轻量 MLP 视觉投影器，将 LMM 视觉特征映射至 BFM 表征空间。
- $\mathbf{y}_{i}^{\mathrm{img}}$：BFM（如 **BioCLIP**，Stevens et al., CVPR 2024）视觉编码器对同一图像的目标特征。
- $\mathrm{sim}(\cdot, \cdot)$：余弦相似度函数。

该损失通过最大化映射后 LMM 视觉特征与 BFM 视觉目标之间的余弦相似度，将分类学视觉知识蒸馏至 LMM 的中间层。

#### 3.3.2 细粒度标签表征对齐损失 $\mathcal{L}_{\mathrm{C}}$

$$\mathcal{L}_{\mathrm{C}} = -\mathrm{sim}\left(P_{\mathrm{T}}(\mathbf{e}_{m,0}^{\mathrm{answer}}), \mathbf{y}^{\mathrm{label}}\right)$$

**变量含义**：
- $\mathbf{e}_{m,0}^{\mathrm{answer}}$：LMM 第 $m$ 层输出的首个回答 token 的隐藏状态。
- $P_{\mathrm{T}}(\cdot)$：轻量 MLP 文本投影器，将 LMM 回答特征映射至 BFM 文本空间。
- $\mathbf{y}^{\mathrm{label}}$：BFM 文本编码器对目标类别标签的嵌入。

该损失确保模型生成的答案在表征层面与分类学标签结构对齐，强化细粒度语义一致性。

#### 3.3.3 总对齐损失

$$\mathcal{L}_{\mathrm{alignment}} = (\mathcal{L}_{\mathrm{V}} + \mathcal{L}_{\mathrm{C}}) / 2$$

训练时，该损失与 **No-Thinking RFT**（Li et al., arXiv 2025）的准确率奖励交替优化。No-Thinking RFT 通过显式禁止模型进行思维链推理（prompt 格式：`{Question} Please directly output the answer.`），迫使模型直接输出层次路径。

### 3.4 推理时的关键设计

训练完成后，**BFMs 编码器和两个 MLP 投影器 $P_{\mathrm{V}}$、$P_{\mathrm{T}}$ 均被丢弃**，LMM 直接接受 prompt 进行层次预测。这意味着 TARA 在推理时零额外参数、零额外计算开销，所有分类学知识已内化至 LMM 的权重中。

### 3.5 消融验证的关键发现

消融实验（Table 3, Table 4）揭示了以下设计选择的重要性：
- **对齐层选择**：视觉对齐目标层 $\ell=14$、文本对齐目标层 $m=28$ 时 HCA 最优（Table 3）。
- **对齐特征粒度**：$\mathcal{L}_{\mathrm{V}}$ 使用全部视觉 token、$\mathcal{L}_{\mathrm{C}}$ 使用首个回答 token 为最优配置（Table 4, Figure 3）。
- **损失组件贡献**：单独添加 $\mathcal{L}_{\mathrm{V}}$ 已能提升层次一致性；叠加 $\mathcal{L}_{\mathrm{C}}$ 后 HCA 进一步提升约 2.06%（Table 3 中 RL+$\mathcal{L}_{\mathrm{V}}$ 与 RL+$\mathcal{L}_{\mathrm{V}}$+$\mathcal{L}_{\mathrm{C}}$ 对比）。

![[assets/figures/papers/paper_list_l2750_https_arxiv_org_abs_2603_00431/figures/006_Figure_3.jpg]]
*Figure 3: Different designs of target alignment features. (a) and (b) are for*



## 实验与关键发现

### 核心瓶颈与实验动机

大规模多模态模型（LMMs）在层次视觉识别（HVR）中暴露的核心问题是**层次一致性缺失**：模型可能在叶子节点类别上猜对，但其预测路径在中间层（如科、属）出现断裂，违反分类学父子约束。这一问题在训练中未见过的**新颖类别**上尤为严重。TARA 的因果假设是：通过将 LMMs 的中间视觉表征和回答嵌入与预训练生物基础模型（BFMs）的分类感知表征对齐，可以显式注入分类学结构知识，从而在不增加推理开销的前提下提升层次一致性和泛化能力。

### 实验设置

实验基于两个 LMM 主干网络：**Qwen3-VL-2B-Instruct**（Qwen Team, 2025）和 **Qwen2.5-VL-3B-Instruct**（Qwen Team, 2024）。教师 BFM 采用 **BioCLIP**（Stevens et al., CVPR 2024）和 **BioCLIP2**（Gu et al., arXiv 2025）。基线方法为 **No-Thinking RFT**（Li et al., arXiv 2025），即仅使用准确率奖励的强化微调。

训练采用交替优化策略：每步交替执行 No-Thinking RFT 和 TARA 对齐损失。对齐损失由视觉对齐损失 $\mathcal{L}_\mathrm{V}$ 和标签对齐损失 $\mathcal{L}_\mathrm{C}$ 的均值构成：

$$\mathcal{L}_\mathrm{alignment} = (\mathcal{L}_\mathrm{V} + \mathcal{L}_\mathrm{C}) / 2$$

其中 $\mathcal{L}_\mathrm{V}$ 对齐投影后的 LMM 视觉特征与 BFM 视觉目标特征，$\mathcal{L}_\mathrm{C}$ 对齐投影后的 LMM 首 token 回答嵌入与 BFM 文本标签嵌入。推理时 BFM 和投影器均被丢弃，LMM 直接接受提示进行层次识别，无额外推理开销。

评估数据集包括 **iNat21-Plant** 和 **iNat21-Animal**（已知类别），以及 **TerraIncognita**（包含已知和未记录的新颖物种）。评估指标涵盖叶子节点准确率（$\mathrm{Acc}_\mathrm{leaf}$）和四个层次一致性指标：

- **HCA**（Hierarchical Consistent Accuracy）：预测路径从根到叶完全匹配真值的样本比例；
- **POR**（Point-Overlap Ratio）：平均正确预测节点比例；
- **S-POR**（Strict Path Overlap Ratio）：仅奖励连续预测正确的片段，惩罚孤立正确预测；
- **TOR**（Top Overlap Ratio）：评估相邻层对的局部层次一致性。

### 主实验结果

**Table 1** 展示了 TARA 在 iNat21-Plant 和 iNat21-Animal 上的效果。以 Qwen3-VL-2B 为基座，在 iNat21-Plant 上，TARA 将 HCA 从纯 RL 基线的 9.23 提升至 12.78（**+3.55**），S-POR 从 50.81 提升至 55.98（**+5.17**），同时叶子节点准确率也获得一致增益。在 iNat21-Animal 上，HCA 从 8.57 提升至 10.26（**+1.69**），所有层次一致性指标均有正向提升。Qwen2.5-VL-3B 上的趋势一致，验证了方法对基座模型的鲁棒性。

**Table 2** 展示了 TARA 在 TerraIncognita 上的泛化能力。在已知物种上，TARA 将 Order F1 从 37.35 大幅提升至 55.61（**+18.26**），Family F1 同样显著提升。在新颖物种上——这些物种在训练中完全不可见——Order F1 从 29.78 提升至 39.93（**+10.15**），证明了 TARA 注入的分类学知识具有跨物种的泛化能力，而非简单记忆训练类别。

### 消融实验

**Table 3** 报告了对齐目标层的消融。实验表明，选择视觉编码器第 14 层和文本编码器第 28 层作为对齐目标可获得最佳 HCA。层选择过浅或过深均会导致性能下降，说明中层表征在编码分类学结构信息上最为有效。

**Table 4** 和 **Figure 3** 展示了对齐特征设计的消融。对于 $\mathcal{L}_\mathrm{V}$，使用全部视觉 token 优于仅使用 CLS token 或均值池化；对于 $\mathcal{L}_\mathrm{C}$，使用首 token 回答嵌入优于均值池化或末 token。逐步添加 $\mathcal{L}_\mathrm{V}$ 和 $\mathcal{L}_\mathrm{C}$ 的消融表明：在纯 RL 基础上添加 $\mathcal{L}_\mathrm{V}$ 已能提升层次一致性，进一步添加 $\mathcal{L}_\mathrm{C}$ 可将 HCA 再提升约 2.06%，验证了视觉对齐和标签对齐的互补性。

### 训练效率与表征分析

**Figure 5** 显示，TARA 在训练早期即超越纯 RL 基线，并实现更快的收敛速度。这表明分类学表征对齐为 LMM 提供了有效的归纳偏置，加速了层次结构的学习。

**Table 5** 左侧的视觉探测实验表明，经过 TARA 训练后，LMM 的视觉隐藏状态中包含更丰富的分类学信息，验证了对齐训练确实改变了内部表征结构。右侧的 ImageWikiQA 评估则表明，TARA 在注入分类学知识的同时，未损害模型的通用视觉问答能力。

### 失败模式与局限性

尽管 TARA 在已知和新颖类别上均取得一致提升，但存在以下局限：

1. **领域依赖性**：方法仅在生物分类学领域验证，依赖于 BioCLIP/BioCLIP2 等 BFM 的质量和覆盖范围。若 BFM 的分类知识与目标领域不匹配，对齐效果可能下降。
2. **基座模型限制**：实验仅基于 Qwen 系列模型，未在 LLaVA、InternVL 等其他 LMM 架构上测试，跨架构泛化性尚需验证。
3. **训练开销**：训练时需额外计算 BFM 输出和投影器，增加了训练成本（尽管推理时无额外开销）。
4. **评估场景受限**：评估仍局限于固定答案的 VQA 设置，开放生成场景下的层次一致性尚未充分探索。
5. **分类树范围**：若目标分类树的深度和分支数远超生物学分类，TARA 的对齐策略是否依然有效仍有待验证。

### 补充图表

![[assets/figures/papers/paper_list_l2750_https_arxiv_org_abs_2603_00431/figures/003_Table_1.jpg]]
*Table 1: Effects of TARA on iNat-Plant and iNat-Animal datasets*

![[assets/figures/papers/paper_list_l2750_https_arxiv_org_abs_2603_00431/figures/004_Table_2.jpg]]
*Table 2: Effects of TARA on TerraIncognita dataset [8]*

![[assets/figures/papers/paper_list_l2750_https_arxiv_org_abs_2603_00431/figures/005_Table_3.jpg]]
*Table 3: Ablation on target alignment layers of TARA*

![[assets/figures/papers/paper_list_l2750_https_arxiv_org_abs_2603_00431/figures/007_Table_4.jpg]]
*Table 4: Ablation on target alignment features of TARA*

![[assets/figures/papers/paper_list_l2750_https_arxiv_org_abs_2603_00431/figures/008_Table_5.jpg]]
*Table 5: Left: visual probing results on the last and averaged image hidden states. Right: evaluation results on ImageWikiQA [58]*

![[assets/figures/papers/paper_list_l2750_https_arxiv_org_abs_2603_00431/figures/010_Figure_5.jpg]]
*Figure 5: Training efficiency. Models trained with TARA achieve faster convergence*

![[assets/figures/papers/paper_list_l2750_https_arxiv_org_abs_2603_00431/figures/011_Figure_4.jpg]]
*Figure 4: Qualitative comparison of No-Thinking RFT with and without TARA. The two columns show that TARA can achieve better leaf node accuracy and hierarchical consistency*

![[assets/figures/papers/paper_list_l2750_https_arxiv_org_abs_2603_00431/figures/001_Figure_1.jpg]]
*Figure 1: LMMs struggle with hierarchical visual recognition (HVR), failing to obey the hierarchical consistency on both known and novel categories*



## 定位与知识库关联

### 1. 与现有基线的关系

TARA 的核心定位是在**大规模多模态模型（LMMs）**与**生物基础模型（BFMs）**之间架设表征对齐的桥梁。其方法谱系可从两条基线路径来理解。

**相对于纯强化微调基线。** 论文将 **No-Thinking RFT**（Li et al., arXiv 2025）作为直接对比基线。该基线在 Qwen 系列模型上仅使用准确率奖励进行强化微调，未引入任何分类学结构信息。TARA 在此基础上插入了两个余弦相似度对齐损失——视觉对齐损失 $\mathcal{L}_V$ 与标签对齐损失 $\mathcal{L}_C$——并采用交替优化策略（Algorithm 1）。实验表明，这一插入带来了跨数据集的层次一致性增益：在 iNat21-Plant 上，TARA 将 HCA 从 9.23 提升至 12.78，S-POR 从 50.81 提升至 55.98（Table 1，Qwen3-VL-2B）。这表明，**仅靠准确率奖励不足以引导 LMM 习得分类学层次结构**，表征对齐是关键的因果旋钮。

**相对于生物基础模型。** TARA 的教师模型选择了 **BioCLIP**（Stevens et al., CVPR 2024）和 **BioCLIP2**（Gu et al., arXiv 2025）。这两个 BFM 在生物分类学数据上经过大规模对比预训练，其视觉和文本编码器已内化了分类学层次结构。TARA 的创新在于将 BFM 的**静态分类学知识**通过表征对齐蒸馏到 LMM 的**动态推理过程**中，而非在推理时调用 BFM。推理阶段，BFM 和投影器均被丢弃，LMM 直接执行层次视觉识别（HVR），无额外推理开销（Section 4.3）。这与传统的“LMM + 外部知识库”范式形成对比——TARA 选择了一条**训练时注入、推理时零额外成本**的路径。

### 2. 适用边界与前提条件

TARA 的有效性建立在以下前提之上：

1. **BFM 的领域覆盖。** TARA 的对齐目标完全来自预训练 BFM 的表征空间。若目标分类学领域与 BFM 的训练分布存在显著差异（例如从生物分类迁移到商品目录或疾病分类），BFM 提供的视觉和文本目标可能不再具备有效的层次结构信息，对齐效果预计会衰减。论文仅在生物分类学领域（iNaturalist-2021、TerraIncognita）进行了验证，跨领域泛化能力尚需手动核实。

2. **基础 LMM 架构。** 当前实验仅基于 Qwen 系列模型（Qwen3-VL-2B-Instruct、Qwen2.5-VL-3B-Instruct）。TARA 的对齐策略依赖于从 LMM 中间层提取视觉特征 $\mathbf{e}_{\ell,i}^{\mathrm{img}}$ 和回答嵌入 $\mathbf{e}_{m,0}^{\mathrm{answer}}$。不同 LMM 架构（如 LLaVA、InternVL）的中间表征语义可能存在差异，投影器设计和最优对齐层数可能需要重新调优。论文未在其他架构上验证，这一点需要关注。

3. **分类树深度与分支因子。** 当前实验的分类学深度有限（iNaturalist 包含界-门-纲-目-科-属-种七层）。对于深度更大、分支因子更极端的分类树，$\mathcal{L}_C$ 中“特定层级”的标签嵌入选择策略（Section 4.2）可能需要重新设计，单层对齐是否足以支撑深层层次一致性仍是一个开放问题。

### 3. 局限性与已知不足

论文自身披露及实验分析揭示了以下局限：

- **领域单一性。** 仅在生物分类学场景下验证，未涉及商品、场景、文档等其他层次分类任务。TARA 是否是一种通用的层次识别增强策略，还是高度依赖 BFM 的生物学先验，目前无法判断。
- **训练成本增加。** 虽然推理时无额外开销，但训练阶段需要额外计算 BFM 的视觉和文本编码输出，并维护两个 MLP 投影器 $P_V$ 和 $P_T$ 的梯度更新。对于大规模 LMM，这一额外计算成本可能不可忽略。
- **开放生成场景未探索。** 评估均采用固定候选答案的 VQA 设置（模型从给定选项中选择分类路径）。在完全开放生成（无候选选项）的 HVR 场景下，TARA 是否仍能保持层次一致性，论文未提供证据。
- **公平性考量缺失。** iNaturalist-2021 数据集主要覆盖北美物种，TerraIncognita 虽包含中南美洲未记录物种，但评估仍限于昆虫等特定门类。论文未讨论模型在不同地理区域、不同生物类群或不同语言上的表现差异。

### 4. 开放问题与潜在后续方向

从 TARA 的方法设计出发，可识别以下值得探索的方向：

1. **跨领域迁移。** TARA 在非生物层次分类（如电商商品目录、医学疾病分类 ICD 编码树）上的表现如何？若目标领域缺乏强 BFM，是否可以用通用视觉-语言模型（如 CLIP）替代，或通过多 BFM 知识融合来增强常识性层次理解？

2. **反向知识蒸馏。** 论文仅考虑了 BFM → LMM 的单向知识注入。LMM 的视觉理解能力（尤其是对细粒度视觉差异和上下文关系的建模）是否可能反过来改进 BFM 的表征？这一“双向对齐”方向尚未被探索。

3. **动态层次对齐。** 当前 $\mathcal{L}_C$ 在单一固定层级进行标签对齐。对于深度和分支数远超生物学分类的树结构，是否需要在多个层级进行分阶段或加权对齐？层级间的梯度冲突如何解决？

4. **开放生成场景的层次一致性评估。** 在无候选选项的完全生成模式下，如何定义和度量层次一致性？TARA 的对齐信号是否足以约束生成路径的逻辑一致性，还是需要额外的解码策略？



## 原文 PDF

![[paperPDFs/CVPR_2026/Taxonomy_Aware_Representation_Alignment_for_Hierarchical_Visual_Recognition_with_Large_Multimodal_Models.pdf]]
