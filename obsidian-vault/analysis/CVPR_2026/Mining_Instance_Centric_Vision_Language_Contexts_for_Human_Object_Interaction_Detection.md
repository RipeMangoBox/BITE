---
title: Mining Instance-Centric Vision-Language Contexts for Human-Object Interaction Detection
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Mining_Instance_Centric_Vision_Language_Contexts_for_Human_Object_Interaction_Detection.pdf
project_link: null
code_link: "https://github.com/nowuss/InCoM-Net"
aliases:
- INICCMN
- MICVLCHOID
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过为每个实例生成包含实例内、实例间和全局三种粒度的上下文特征，并采用渐进式交叉注意力将其逐步整合到检测器特征中，显著强化了模型对细微交互关系的建模能力。
primary_logic: 以实例为中心的多上下文建模与渐进聚合策略，使模型能够自适应地关注与目标实例相关的视觉语义线索，从而在HOI检测中实现更精准的上下文推理。
claims:
- ICR 模块在基线基础上提升 1.25 mAP，验证了实例中心上下文精炼的有效性。
- ProCA 模块额外带来 1.00 mAP 提升，表明渐进式上下文聚合对性能至关重要。
- MFT 训练策略在完整模型基础上再提升 1.11 mAP，并有效平衡了检测器与VLM特征的利用。
- 完整的多上下文配置在稀有类别上比常规 RoI 对齐方法提升 2.32 mAP，证明了对稀有交互的强大建模能力。
---

# Mining Instance-Centric Vision-Language Contexts for Human-Object Interaction Detection

> [!tip] 核心洞察
> 以实例为中心的多上下文建模与渐进聚合策略，使模型能够自适应地关注与目标实例相关的视觉语义线索，从而在HOI检测中实现更精准的上下文推理。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向人-物交互检测的实例中心视觉-语言上下文挖掘 |
| 英文题名 | Mining Instance-Centric Vision-Language Contexts for Human-Object Interaction Detection |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.02071) · [Code](https://github.com/nowuss/InCoM-Net) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InCoM-Net (Instance-centric Context Mining Network) |
| Dataset | HICO-DET, V-COCO, HICO-DET Zero-shot |

> [!tip] 效果简介
> - HICO-DET (Full) 上，mAP 45.61 vs 44.58 (NMSR, ICCV 2025) (+1.03)。
> - V-COCO (Scenario 1) 上，AP_role 73.6 vs 69.8 (NMSR, ICCV 2025) (+3.8)。
> - HICO-DET Zero-shot (RF-UC Unseen) 上，mAP 37.69 vs 36.72 (VDRP, NeurIPS 2025?) (+0.97)。

## 概要

### 问题瓶颈

人-物交互（Human-Object Interaction, HOI）检测要求模型同时定位图像中的人与物实例，并识别两者之间的交互关系。近年来，视觉-语言模型（VLM）因其丰富的语义知识被广泛引入HOI检测，但现有方法通常将VLM提供的上下文信息**统一施加于所有实例**，未能提取并利用针对每个实例的细粒度多层级上下文线索。这种粗粒度的上下文建模方式导致模型在面对复杂、细微的交互关系时推理能力不足，尤其在稀有交互类别上表现乏力。

### 核心方法

针对上述瓶颈，本文提出**InCoM-Net（Instance-centric Context Mining Network）**，其核心思想是**以实例为中心的多上下文建模与渐进聚合**。具体而言，InCoM-Net包含两个关键模块：

- **实例中心上下文精炼（Instance-centric Context Refinement, ICR）**：利用检测器生成的实例掩码，在VLM特征图上执行掩码自注意力，为每个实例独立生成**实例内**、**实例间**和**全局**三种粒度的上下文特征，使模型能够自适应地关注与目标实例相关的视觉语义线索。
- **渐进式上下文聚合（Progressive Context Aggregation, ProCA）**：通过多层交叉注意力，将ICR生成的多上下文特征逐步整合到检测器的实例查询特征中，并引入残差连接，避免信息丢失。

此外，InCoM-Net引入**掩码特征训练（Masked Feature Training, MFT）**策略，在训练过程中随机遮盖检测器或VLM特征，迫使模型均衡利用两种异质特征源，进一步缩小检测器与VLM特征之间的利用鸿沟。

### 主要结果

在常规设置下，InCoM-Net在两个主流基准上均取得最优性能：

- **HICO-DET**：Full mAP达到45.61，超越此前最优方法**NMSR**（Yang et al., ICCV 2025）1.03个点。
- **V-COCO**（Scenario 1）：AP_role达到73.6，以**+3.8**的显著优势领先NMSR。

在零样本设置下，InCoM-Net同样展现出强泛化能力，在HICO-DET RF-UC Unseen指标上达到37.69 mAP，超过此前最优方法**VDRP**（NeurIPS 2025）0.97个点。

消融实验进一步验证了各组件的有效性：ICR模块带来1.25 mAP的提升，ProCA额外贡献1.00 mAP，MFT训练策略再增加1.11 mAP。值得注意的是，完整的多上下文配置在稀有类别上比常规RoI对齐方法提升**2.32 mAP**，证明该方法对稀有交互具有强大的建模能力。

### 方法定位

InCoM-Net属于VLM集成型HOI检测方法，与**HOICLIP**（Ning et al., CVPR 2023）等代表性工作共享利用VLM语义知识的基本思路，但在上下文利用方式上有本质区别：它摒弃了全局统一或简单RoI对齐的特征提取范式，转而采用**以实例为中心的分层上下文挖掘与渐进式特征融合**，从而在复杂交互推理上取得显著突破。



### 任务背景

人-物交互（Human-Object Interaction, HOI）检测旨在从图像中同时定位人与物体实例，并识别两者之间的交互关系（如“人-骑-自行车”）。该任务处于目标检测与视觉关系理解的交叉点，是场景理解、行为识别和视觉问答等高层视觉任务的重要基础。

### 现有方法缺口

近年来，视觉-语言模型（VLM）的引入为 HOI 检测注入了丰富的语义先验，使得模型能够利用开放世界的知识辅助交互推理。然而，现有方法存在一个关键瓶颈：**VLM 提供的语义上下文通常被统一施加于所有实例，未能提取并利用针对每个实例的细粒度多层级上下文信息**。具体而言：

- **上下文粒度单一**：多数方法仅使用全局上下文或简单的 RoI 对齐特征，忽略了不同实例在交互推理中对上下文需求的差异性。例如，判断“人-骑-马”需要关注人马之间的空间关系（实例间上下文），而判断“人-穿-衬衫”则更依赖人体自身的视觉线索（实例内上下文）。
- **特征聚合粗糙**：将 VLM 特征与检测器特征进行简单拼接或单层交叉注意力，难以实现两种异质特征源的深度融合与交互式精炼。
- **特征源利用不均衡**：模型在训练过程中容易偏向依赖某一特征源（检测器或 VLM），导致另一方的语义信息未被充分利用，限制了模型的鲁棒性和泛化能力。

### 本文动机

针对上述问题，本文提出 **InCoM-Net（Instance-centric Context Mining Network）**，其核心动机在于：**以实例为中心，从 VLM 特征中挖掘多层级上下文，并通过渐进聚合策略将其有效融入检测器特征，从而实现更精准的交互推理**。如图 1 所示，对于每个实例，上下文信息可被区分为实例内（intra-instance）、实例间（inter-instance）和全局（global）三个层次，每一层次为交互理解提供互补线索。InCoM-Net 正是围绕这一三层上下文范式展开设计，使模型能够自适应地关注与目标实例最相关的视觉语义线索。



## 核心方法与创新机理

InCoM-Net 的核心创新在于将 VLM 提供的语义上下文从“全局均等施加”转变为**以实例为中心的多粒度上下文挖掘与渐进聚合**，并辅以**掩码特征训练**策略来均衡异质特征源的利用。这一设计直接回应了现有方法（如 **HOICLIP** (Ning et al., CVPR 2023) 和 **QPIC** (Tamura et al., CVPR 2021)）的瓶颈：它们通常将 VLM 特征作为统一上下文或以简单 RoI 对齐方式注入，未能针对每个实例提取细粒度的多层级视觉-语义线索，导致对复杂交互的推理能力不足。

### 关键 changed slots

1. **上下文特征生成方式：从单一全局到实例中心的多上下文精炼（ICR）**
   - **Baseline**：使用 RoI 对齐或单一全局特征表示 VLM 上下文，所有实例共享相同的语义信息。
   - **InCoM-Net**：通过实例掩码在 VLM 特征图上执行掩码自注意力，为每个实例独立生成三种粒度的上下文特征：
     - **实例内上下文** $\hat{R}_{i}^{l} = \mathrm{Self-Attention}(V^{l}, M_{i}^{R})$：聚焦实例自身区域内的语义细节；
     - **实例间上下文** $\hat{C}_{i}^{l} = \mathrm{Self-Attention}(V^{l}, M_{i}^{C})$：捕获该实例与其他实例之间的空间-语义关系；
     - **全局上下文** $\hat{G}^{l} = \mathrm{Self-Attention}(V^{l}, \mathbf{1})$：提供场景级别的整体语义背景。
   - **因果机制**：这种设计使模型能够自适应地关注与目标实例相关的视觉语义线索，从而在 HOI 检测中实现更精准的上下文推理。消融实验表明，ICR 模块在基线基础上带来 **+1.25 mAP** 的提升（Table 3），验证了实例中心上下文精炼的有效性。

2. **特征聚合策略：从简单拼接/单层交叉注意力到渐进式上下文聚合（ProCA）**
   - **Baseline**：将多源特征简单拼接或通过单层交叉注意力一次性融合。
   - **InCoM-Net**：采用多层交叉注意力进行**渐进聚合**（ProCA），逐层将 ICR 生成的多上下文特征集成到检测器的实例查询特征中，并引入残差连接。最终通过前馈网络生成上下文聚合特征 $f_{i}^{l} = \mathrm{FFN}([f_{i,G}^{l} \parallel f_{i,R}^{l} \parallel f_{i,C}^{l}])$。
   - **因果机制**：迭代式的注意力交互允许模型逐步精炼对相关上下文的关注，避免一次性融合带来的信息过载或噪声干扰。ProCA 模块额外贡献 **+1.00 mAP**（Table 3），且层数消融（Table 5）进一步证实了渐进式聚合对性能的关键作用。

3. **训练范式：从标准端到端训练到掩码特征训练（MFT）**
   - **Baseline**：标准端到端训练，检测器特征和 VLM 特征同时输入，模型可能过度依赖某一特征源。
   - **InCoM-Net**：引入**掩码特征训练（MFT）**，在训练过程中随机遮盖检测器特征或 VLM 特征（将对应特征置零并停用相关交叉注意力模块），迫使模型在三种配置（完整、仅检测器、仅 VLM）下均能有效推理。训练目标为三种配置下焦点损失之和：$\mathcal{L} = \sum_{x \in \mathcal{X}} \mathcal{L}_{f}(y, \Phi_{\theta}(x))$。
   - **因果机制**：MFT 强制模型均衡利用两种异质特征源，缩小了“仅检测器”与“仅 VLM”设置之间的性能差距（Table 6），并在完整模型基础上再提升 **+1.11 mAP**（Table 3）。

### 创新的协同效应

这三个 changed slots 并非孤立改进，而是形成了一条因果链：**ICR** 产生高质量的实例中心多上下文特征，**ProCA** 以结构化的方式将这些特征渐进注入检测器查询，**MFT** 则确保训练过程中两种特征源被均衡利用。完整的多上下文配置在稀有类别上比常规 RoI 对齐方法提升 **+2.32 mAP**（Sec. 4.3），证明该设计对稀有交互具有强大的建模能力——这正是实例中心精细化上下文推理的直接收益。



InCoM-Net 遵循“检测器提取实例特征 + VLM 提供语义上下文 + 交互解码器推理人-物交互”的总体范式，其核心创新在于以**实例为中心**的多层级上下文挖掘与渐进式聚合机制。图 2 展示了框架的全貌。

**输入与特征提取。** 给定输入图像，框架首先通过两条并行的特征提取通路获取异构表示：
- **检测器通路**：采用基于 DETR 的检测器，以 CNN（ResNet-50）为骨干提取空间特征图 $F$，经 Transformer 编码器-解码器处理后，输出人/物实例的检测器查询特征 $\{q^l\}_{l=1}^{L}$（$L$ 为解码器层数）。
- **VLM 通路**：使用冻结的 CLIP 视觉编码器（ViT-B 或 ViT-L）提取多尺度视觉-语言特征 $\{V^l\}_{l=1}^{L}$，这些特征蕴含丰富的语义先验知识。

**实例中心上下文精炼（ICR）。** ICR 模块接收 VLM 特征 $\{V^l\}$ 以及检测器提供的实例掩码 $M^R$ 和周围掩码 $M^C$，通过掩码自注意力机制为**每一个实例**独立生成三种粒度的上下文特征：
- **全局上下文** $\hat{G}^l$：对全体 VLM 特征进行无掩码自注意力，捕捉场景级语义。
- **实例内上下文** $\hat{R}_i^l$：以实例 $i$ 的掩码 $M_i^R$ 约束注意力范围，提取该实例自身内部的细粒度语义。
- **实例间上下文** $\hat{C}_i^l$：以排除实例 $i$ 的其他实例联合掩码 $M_i^C$ 引导注意力，建模实例间的关系线索。

这三种上下文从不同粒度互补地刻画了与目标实例相关的视觉语义信息，其结构如图 3 所示。

**渐进式上下文聚合（ProCA）。** ProCA 模块将 ICR 生成的多上下文特征逐步整合到检测器查询特征中。具体而言，它以检测器查询 $q_i^l$ 为 Query，分别对全局、实例内、实例间三种上下文特征执行交叉注意力，并将三者的输出拼接后经前馈网络（FFN）融合，形成上下文聚合特征 $f_i^l$。该过程通过堆叠多层交叉注意力实现渐进式精炼，并引入残差连接以稳定训练（图 4）。

**人-物对构建与交互解码。** 获得人与物实例的检测器查询特征 $q_h^L, q_o^L$ 及上下文聚合特征 $f_h^L, f_o^L$ 后，框架通过线性投影与层归一化将其融合，构建人-物对特征 $s$。随后，交互解码器以 $s$ 为查询，分别与 CNN 空间特征图 $F$ 和 VLM 特征 $V^L$ 进行交叉注意力交互，增强对空间布局与语义关系的建模，最终输出交互类别预测。

**掩码特征训练（MFT）。** 为促使模型均衡利用检测器空间特征与 VLM 语义特征这两种异质信息源，InCoM-Net 引入了 MFT 策略。训练时，随机对检测器特征或 VLM 特征进行掩码（置零并停用对应的交叉注意力模块），迫使模型在单一特征源缺失的情况下仍能可靠推理。训练目标为三种输入配置（完整特征、仅检测器特征、仅 VLM 特征）下焦点损失之和，从而缩小仅使用单一特征源时的性能差距，提升整体鲁棒性。

### 补充图表

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of InCoM-Net. Left: overview of Instance-centric Context Mining that integrates multi-context VLM features with instance-level features. Right: masked feature training (MFT), balancing the utilization of heterogeneous feature sources via masking*



InCoM-Net 的核心由两个紧密协作的模块构成：**实例中心上下文精炼（Instance-centric Context Refinement, ICR）** 和 **渐进式上下文聚合（Progressive Context Aggregation, ProCA）**。ICR 负责从 VLM 特征中为每个实例独立提取多粒度上下文线索，ProCA 则通过多层交叉注意力将这些上下文特征逐步融入检测器实例查询中。

### 实例中心上下文精炼（ICR）

ICR 的核心操作是对 CLIP 视觉编码器提取的多层 VLM 特征图 $V^{l} \in \mathbb{R}^{N \times D_{v}}$ 施加**掩码自注意力**，其中 $l$ 为层索引，$N$ 为特征图的空间尺寸，$D_{v}$ 为特征维度。掩码由检测器提供的实例掩码 $M^{R} \in \mathbb{R}^{K \times N}$ 和周围掩码 $M^{C} \in \mathbb{R}^{K \times N}$ 引导（$K$ 为实例数量），从而为每个实例生成三种互补的上下文特征：

**全局上下文特征**（无掩码自注意力）：

$$\hat{G}^{l} = \mathrm{Self-Attention}(V^{l}, \mathbf{1}) \tag{1}$$

该特征捕获整张图像的全局语义信息，不区分任何实例边界。

**实例内上下文特征**（实例掩码自注意力）：

$$\hat{R}_{i}^{l} = \mathrm{Self-Attention}(V^{l}, M_{i}^{R}) \tag{2}$$

使用第 $i$ 个实例的二值掩码 $M_{i}^{R}$ 约束注意力范围，仅聚合该实例内部区域的 VLM 特征，提取与实例自身属性紧密相关的细粒度语义。

**实例间上下文特征**（周围掩码自注意力）：

$$\hat{C}_{i}^{l} = \mathrm{Self-Attention}(V^{l}, M_{i}^{C}) \tag{3}$$

其中 $M_{i}^{C}$ 是除实例 $i$ 外其他所有实例的联合掩码。该特征聚焦于实例之间的空间关系和语义交互线索，为理解“谁在对谁做什么”提供关系上下文。

这三种上下文特征从不同粒度刻画了实例所处的视觉-语言环境，其有效性在消融实验中得到了直接验证：完整的多上下文配置相比仅使用单一上下文类型累计提升 1.23 mAP，且在稀有交互类别上增益更为显著（相较传统 RoI 对齐方法提升 2.32 mAP）。

### 渐进式上下文聚合（ProCA）

ProCA 通过多层交叉注意力将 ICR 生成的多上下文特征逐步注入检测器的实例查询特征 $q^{l}$ 中。在每一层，检测器查询分别与全局、实例内、实例间上下文特征进行交叉注意力交互，随后将三者的输出拼接并通过前馈网络（FFN）融合，形成该层的上下文聚合特征：

$$f_{i}^{l} = \mathrm{FFN}([f_{i,G}^{l} \parallel f_{i,R}^{l} \parallel f_{i,C}^{l}]) \tag{11}$$

其中 $f_{i,G}^{l}$、$f_{i,R}^{l}$、$f_{i,C}^{l}$ 分别表示第 $i$ 个实例的检测器查询对全局、实例内、实例间上下文特征进行交叉注意力后的输出，$\parallel$ 表示通道维度拼接。

ProCA 的关键设计在于**多层渐进聚合**和**残差连接**：每一层的输出 $f_{i}^{l}$ 会作为下一层检测器查询的增强表示，使模型能够逐层精炼上下文信息，而非一次性融合。消融实验表明，ProCA 在 ICR 基础上额外贡献 1.00 mAP 的提升，验证了渐进式聚合策略对性能的实质性影响。层数消融进一步显示，适当的聚合深度对平衡计算开销与建模能力至关重要。

### 人-物对特征构建

在完成上下文聚合后，人、物实例的检测器查询特征 $q_{h}^{L}$、$q_{o}^{L}$ 与对应的上下文聚合特征 $f_{h}^{L}$、$f_{o}^{L}$ 被融合以构建人-物对表示：

$$s = \mathrm{LN}(\mathrm{Linear}(q_{h}^{L} \parallel q_{o}^{L})) + \mathrm{LN}(\mathrm{Linear}(f_{h}^{L} \parallel f_{o}^{L})) \tag{12}$$

该设计将检测器提供的空间定位特征与 VLM 提供的语义上下文特征以残差形式结合，使后续的交互解码器能够同时利用两类异质信息进行交互类别推理。

### 训练目标

为迫使模型均衡利用检测器特征和 VLM 上下文特征，InCoM-Net 采用掩码特征训练（MFT）策略，在训练过程中随机遮盖检测器分支或 VLM 分支的输入。最终训练目标为三种输入配置下焦点损失之和：

$$\mathcal{L} = \sum_{x \in \mathcal{X}} \mathcal{L}_{f}(y, \Phi_{\theta}(x)) \tag{15}$$

其中 $\mathcal{X} = \{x_{f}, x_{d}, x_{v}\}$ 分别对应完整输入、仅检测器特征输入、仅 VLM 特征输入三种配置，$\Phi_{\theta}$ 为模型，$\mathcal{L}_{f}$ 为焦点损失。MFT 在完整模型基础上额外带来 1.11 mAP 的提升，并有效缩小了仅使用单一特征源时的性能差距，验证了该策略对异质特征融合的促进作用。

### 补充图表

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of three levels of contextual information. For each instance, contextual information can be distinguished into intra-instance, inter-instance, and global contexts, each providing complementary cues for interpreting human–object interactions*

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/003_Figure_3.jpg]]
*Figure 3: Structure of ICR. The illustration shows the process of generating the multi-context features for the i-th instance*

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/004_Figure_4.jpg]]
*Figure 4: Structure of ProCA*



## 实验与关键发现

### 主实验结果

InCoM-Net 在两个标准 HOI 检测基准上均取得了领先性能。在 HICO-DET 数据集上，使用 ViT-B 视觉 backbone 时，InCoM-Net 达到 39.53 Full mAP，超越此前最优方法 **HORP**（Geng et al., CVPR 2025）0.92 mAP；使用 ViT-L 时达到 43.96 Full mAP，超越 **NMSR**（Yang et al., ICCV 2025）1.03 mAP（Table 1）。在 V-COCO 数据集上，InCoM-Net 在 Scenario 1 下取得 73.6 AP_role，以 3.8 mAP 的显著优势超越 NMSR（Table 1）。

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/005_Table_1.jpg]]
*Table 1: Performance comparison under the regular setting on the HICO-DET and V-COCO datasets. R50 denotes ResNet-50*

零样本泛化能力方面，InCoM-Net 同样表现突出。在 HICO-DET 的 RF-UC（Rare First Unseen Combination）设定下，ViT-L 版本达到 37.69 mAP，超越 **VDRP** 0.97 mAP；在 NF-UC（Non-rare First Unseen Combination）设定下超越 **LAIN** 1.93 mAP（Table 2）。这表明实例中心的多上下文建模不仅在常规设定下有效，在未见组合的泛化场景中也具备强鲁棒性。

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/006_Table_2.jpg]]
*Table 2: Zero-shot performance comparison on HICO-DET*

### 消融实验

消融实验系统验证了 InCoM-Net 各核心组件的独立贡献（Table 3）。以仅使用检测器特征的基本 DETR 框架为基线，逐步引入各模块：

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/007_Table_3.jpg]]
*Table 3: Ablation study of main components of InCoM-Net*

- **ICR（实例中心上下文精炼）**：引入 ICR 模块后，性能提升 **1.25 mAP**，验证了从 VLM 特征中提取实例中心多上下文信息的有效性。
- **ProCA（渐进式上下文聚合）**：在 ICR 基础上叠加 ProCA 模块，进一步带来 **1.00 mAP** 的增益，表明多层交叉注意力逐步聚合策略对上下文信息融合至关重要。
- **MFT（掩码特征训练）**：引入 MFT 训练策略后，额外贡献 **1.11 mAP** 提升，证明了迫使模型均衡利用检测器与 VLM 两种异质特征源的有效性。

上下文类型的消融（Table 4）显示，完整的多上下文配置（实例内 + 实例间 + 全局）相比基线模型累计提升 **1.23 mAP**。值得注意的是，在稀有交互类别上，该配置相比常规 RoI 对齐方法提升达 **2.32 mAP**，说明细粒度的实例间与全局上下文对稀有交互的建模尤为关键。

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/008_Table_4.jpg]]
*Table 4: Effect of different context types in ICR*

ProCA 层数消融（Table 5）表明，随着交叉注意力层数从 1 层增加到 3 层，性能持续提升，但超过 3 层后趋于饱和，最终选用 3 层作为默认配置。

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/009_Table_5.jpg]]
*Table 5: Ablation study on the number of ProCA layers*

MFT 策略的影响在 Table 6 中进一步分析：引入 MFT 后，仅使用检测器特征（D-only）与仅使用 VLM 特征（V-only）设置之间的性能差距显著缩小，说明 MFT 有效促进了模型对两种异质特征源的均衡利用，而非过度依赖某一方。

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/011_Table_6.jpg]]
*Table 6: Impact of MFT. * denotes reproduced results using their open-source code*

VLM 特征提取策略的对比（Table 7）显示，ICR 采用的掩码自注意力方案在提取实例中心上下文方面优于直接使用全局池化或 RoI 对齐等替代策略，进一步验证了方法设计的合理性。

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/012_Table_7.jpg]]
*Table 7: Comparison with alternative VLM feature extraction strategies*

### 定性分析

Figure 5 可视化了交互解码器的激活图。结果表明，InCoM-Net 能够准确聚焦于与交互相关的关键区域（如人物接触部位、交互物体），而基线方法往往关注范围更分散或错误定位。这直观地印证了实例中心多上下文建模在引导模型关注细粒度视觉语义线索方面的优势。

![[assets/figures/papers/paper_list_l980_https_arxiv_org_abs_2604_02071/figures/010_Figure_5.jpg]]
*Figure 5: Visualization of activation maps from the interaction decoder*

### 公平性说明

所有对比方法均采用相同的评估协议（IoU ≥ 0.5，HICO-DET 和 V-COCO 标准划分）。本方法使用的 DETR 检测器和 CLIP 编码器均采用与其他工作一致的预训练权重并保持冻结，确保了比较的公平性。



## 定位与知识库关联

### 任务定位与基线关系

InCoM-Net 面向**人-物交互（HOI）检测**任务，核心问题是如何将视觉-语言模型（VLM）提供的语义上下文有效注入到检测器中。现有方法通常将 VLM 特征以统一方式施加于所有实例，未能实现实例粒度的细粒度上下文利用——这是本文识别出的真实瓶颈。

在方法谱系上，InCoM-Net 与以下工作形成直接对比：

- **NMSR**（Yang et al., ICCV 2025）：先前最优方法，InCoM-Net 在 HICO-DET Full 上以 +1.03 mAP 超越，在 V-COCO Scenario 1 上以 +3.8 AP_role 超越。这一差距表明实例中心的多上下文挖掘比 NMSR 的上下文利用策略更有效。
- **HORP**（Geng et al., CVPR 2025）：ViT-B 设置下的先前最优，InCoM-Net 以 +0.92 mAP 超越。
- **HOICLIP**（Ning et al., CVPR 2023）：代表性 VLM 集成方法，InCoM-Net 同样采用 CLIP 作为 VLM 特征源，但通过 ICR 和 ProCA 实现了更精细的上下文聚合，而非简单的特征拼接。
- **QPIC**（Tamura et al., CVPR 2021）：Transformer 基线，InCoM-Net 沿用了 DETR 架构作为检测器基础，但在上下文利用方式上有本质区别。

### 核心差异与因果机制

InCoM-Net 与上述方法的关键差异体现在三个设计槽位：

1. **上下文特征生成方式**：从“RoI 对齐或单一全局特征”变为“掩码自注意力生成三层上下文”。ICR 模块利用实例掩码和周围掩码对 VLM 特征图进行自注意力，独立生成实例内、实例间和全局三种上下文特征。消融实验表明，完整的多上下文配置比常规 RoI 对齐方法在稀有类别上提升 2.32 mAP，证明了细粒度上下文对复杂交互建模的因果作用。

2. **特征聚合策略**：从“简单拼接或单层交叉注意力”变为“多层交叉注意力渐进聚合（ProCA）”。ProCA 通过逐层交叉注意力将多上下文特征逐步集成到实例查询特征中，并引入残差连接。消融显示 ProCA 在 ICR 基础上额外贡献 1.00 mAP，验证了渐进式聚合对性能的因果重要性。

3. **训练范式**：从“标准端到端训练”变为“掩码特征训练（MFT）”。MFT 随机遮盖检测器特征或 VLM 特征，迫使模型均衡利用两种异质特征源。该策略在完整模型基础上再提升 1.11 mAP，并有效缩小了仅使用检测器特征（D-only）与仅使用 VLM 特征（V-only）时的性能差距。

### 适用边界与局限

**适用边界**：
- 方法依赖 DETR 架构和 CLIP 视觉编码器，检测器和 VLM 均保持冻结，仅训练新增的 ICR、ProCA 和交互解码器模块。这使得方法具有较好的即插即用特性，但前提是目标场景能受益于 CLIP 的视觉-语言对齐能力。
- 三层上下文（实例内、实例间、全局）的划分假设交互信息可从实例掩码的空间关系中捕获，适用于以人-物空间关系为核心的 HOI 检测，但未显式建模时序或因果逻辑关系。

**局限与待验证问题**：
- 论文未报告任何明确的局限性分析或失败案例。以下推断需人工确认：
  - 方法在极度密集场景（实例掩码高度重叠）下，实例间上下文特征的区分度可能下降。
  - MFT 的随机遮盖策略虽有效，但其最优遮盖比率和训练稳定性未在消融中充分探讨。
  - 方法在非 CLIP VLM（如纯视觉模型）上的迁移能力未经验证。
- 开放问题：三层上下文的划分是否最优？是否存在更细粒度的上下文层级（如部件级、场景图级）可进一步提升性能？MFT 策略是否可推广至其他多模态特征融合任务？

### 知识库定位

InCoM-Net 可定位于 **VLM 增强的检测器上下文建模** 子领域，与以下工作共享技术 DNA：
- 继承 DETR 的查询式检测范式（Carion et al., ECCV 2020）
- 继承 CLIP 的视觉-语言对齐特征（Radford et al., ICML 2021）
- 与 HOICLIP、NMSR 等同属 VLM 集成 HOI 检测路线，但在上下文粒度和聚合策略上形成差异化贡献

其核心 insight——以实例为中心的多上下文建模与渐进聚合——为后续工作提供了可复用的设计模式：将 VLM 语义知识按空间粒度解耦，并通过渐进式注意力机制与检测器特征深度融合。



## 原文 PDF

![[paperPDFs/CVPR_2026/Mining_Instance_Centric_Vision_Language_Contexts_for_Human_Object_Interaction_Detection.pdf]]
