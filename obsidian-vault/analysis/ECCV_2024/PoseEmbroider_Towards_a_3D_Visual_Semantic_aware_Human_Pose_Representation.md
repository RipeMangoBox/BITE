---
title: "PoseEmbroider: Towards a 3D, Visual, Semantic-aware Human Pose Representation"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/PoseEmbroider_Towards_a_3D_Visual_Semantic_aware_Human_Pose_Representation.pdf
project_link: null
code_link: null
aliases:
- PoseEmbroider
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 通过Transformer聚合多模态信息到一个可学习的全局token，并在各模态特定空间进行对比学习，而非强制所有模态对齐到同一联合空间。
primary_logic: 将图像、3D姿态和文本视为同一抽象‘人体姿态’概念的三种互补部分观测，训练模型将这些信息‘刺绣’成更丰富、多模态感知的姿态嵌入空间，从而无需模态间精确匹配即可增强下游任务。
claims:
- 在BEDLAM-Script验证集的多模态检索中，PoseEmbroider（S）达到74.6%总mRecall，优于所有Aligner基线（最佳单输入Aligner为72.4%）。
- 在姿态指令生成任务（BEDLAM-Fix）上，使用PoseEmbroider表示时，完全基于3D姿态输入的R@1达到43.1%，比Aligner基线（31.8%）提升36%。
- 在SMPL回归中，PoseEmbroider允许融合可选文本提示，将仅图像输入的pa-MPJPE从49mm降至44mm（提升约11%）。
- BEDLAM-Script 验证集（多模态检索） 上 总 mRecall（单+双查询平均） = 74.6
---

# PoseEmbroider: Towards a 3D, Visual, Semantic-aware Human Pose Representation

> [!tip] 核心洞察
> 将图像、3D姿态和文本视为同一抽象‘人体姿态’概念的三种互补部分观测，训练模型将这些信息‘刺绣’成更丰富、多模态感知的姿态嵌入空间，从而无需模态间精确匹配即可增强下游任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | PoseEmbroider：迈向三维、视觉、语义感知的人体姿态表征 |
| 英文题名 | PoseEmbroider: Towards a 3D, Visual, Semantic-aware Human Pose Representation |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/8959_ECCV_2024_paper.php) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | PoseEmbroider |
| Dataset | BEDLAM-Script 验证集（多模态检索）, BEDLAM-Fix 验证集（姿态指令生成）, BEDLAM-Script 验证集（SMPL 回归） |

> [!tip] 效果简介
> - BEDLAM-Script 验证集（多模态检索） 上，总 mRecall（单+双查询平均） 74.6 vs 72.4 (Aligner 单个输入) (+2.2%)。
> - BEDLAM-Fix 验证集（姿态指令生成） 上，R@1 (P_A, P_B 输入) 43.1 vs 31.8 (Aligner 基线) (+36%)。
> - BEDLAM-Script 验证集（SMPL 回归） 上，pa-MPJPE (mm) 44 (图像+文本提示) vs 49 (仅图像) (-5 mm (-10.2%))。

## 概要

### 问题背景

理解三维人体姿态需要同时把握其几何结构、视觉外观和语义描述——然而，现有的视觉-语义模型在姿态表示上存在根本性瓶颈：它们产生的姿态嵌入分辨率不足，难以区分细粒度或不常见的3D人体姿态，且未能充分利用图像、3D姿态和文本三种模态的互补信息。这类似于仅凭单一角度的投影去推断一个复杂三维物体的全貌，信息天然不完整。

### 核心思想

PoseEmbroider 将图像、3D姿态和文本视为同一抽象“人体姿态”概念的三种互补“影子”——即部分观测。其核心洞见在于：**训练一个模型将这些多模态信息“刺绣”（embroider）成一个更丰富、视觉与语义双重感知的姿态嵌入空间**，而非强制所有模态对齐到同一个联合空间。这种设计使得模型无需模态间精确匹配，即可在下游任务中灵活融合任意可用的模态输入。

### 方法定位

PoseEmbroider 是一个基于 Transformer 的多模态融合框架。与传统的单模态对齐方法（如 **Aligner**，Girdhar et al., CVPR 2023）不同，它通过一个可学习的全局 token 在自注意力机制下聚合可变数量的输入模态，并在各模态**特定空间**内进行对比学习——将全局表示重投影回各自模态空间后再计算 InfoNCE 损失，从而避免模态空间塌缩。训练时同时覆盖所有单输入和双输入组合，使模型天然具备处理部分模态缺失的鲁棒性。

### 核心结论

在 BEDLAM-Script 验证集上，PoseEmbroider 在多模态检索任务中达到 **74.6%** 的总 mRecall，优于最佳单输入 Aligner 基线（72.4%）。在姿态指令生成任务（BEDLAM-Fix）上，完全基于3D姿态输入的 R@1 达到 **43.1%**，相比 Aligner 基线（31.8%）提升 36%。在 SMPL 回归中，PoseEmbroider 允许融合可选文本提示，将仅图像输入的 pa-MPJPE 从 49mm 降至 **44mm**（提升约 11%）。消融实验证实，Transformer 聚合、模态特定重投影损失、以及单/双输入联合训练三项设计各自贡献了显著的性能增益。

三维人体姿态理解是计算机视觉的核心问题之一，其应用涵盖动作识别、人机交互、虚拟试衣和运动分析等领域。然而，完整地理解一个三维人体姿态本质上是一个多模态挑战：图像提供了视觉外观和场景上下文，三维关节旋转编码了精确的空间几何，而自然语言描述则捕捉了语义属性和细粒度属性（如“左臂弯曲”、“躯干前倾”）。这三种模态各自构成了同一抽象“人体姿态”概念的部分观测——类似于从不同角度照射三维物体所产生的影子，每个影子都揭示了物体的某些特征，但单独一个永远无法完整描述物体本身（Fig. 1）。

当前主流方法通常将这些模态视为独立的信息源，或试图将它们强制对齐到一个共享的联合嵌入空间。例如，**ImageBind**（Girdhar et al., CVPR 2023）风格的对齐器通过成对或三元组对比损失，将不同模态的特征映射到同一空间进行检索。然而，这种直接对齐策略存在两个根本性局限：其一，它要求模态间的精确匹配，但在现实场景中，图像、三维姿态和文本往往只能获得部分配对数据，难以构建完整的三元组；其二，将所有模态压缩到同一空间可能导致模态特定信息的丢失，尤其是当不同模态的语义粒度差异较大时，细粒度或不常见的姿态难以被有效区分。

更关键的是，现有视觉-语义模型产生的姿态嵌入分辨率不足。由于训练数据规模和模态覆盖的限制，这些嵌入在区分高度相似但语义不同的姿态时表现乏力——例如，“右手举过头顶”与“右手举至肩高”在纯视觉或纯三维空间中可能差异微小，但语义上却有本质区别。这一瓶颈直接制约了下游任务（如姿态检索、姿态指令生成和三维人体重建）的性能上限。

PoseEmbroider 的核心动机正是突破上述局限：与其强制不同模态对齐到同一空间，不如将它们视为互补的部分观测，通过一个灵活的聚合机制将这些信息“刺绣”（embroider）成一个更丰富、多模态感知的姿态嵌入。这一嵌入空间不仅融合了视觉、三维和语义信息，还具备处理缺失模态的鲁棒性——当仅有图像或仅有三维姿态时，模型仍能生成有意义的表示。这种设计使得下游任务可以无缝利用多种信息源，而无需模态间的精确匹配。

## 核心方法与创新机理

PoseEmbroider 的核心创新在于**多模态信息聚合机制**与**训练范式**的双重重构，相较于传统的单模态对齐基线（Aligner），其在三个关键维度上实现了根本性突破。

### 从强制对齐到刺绣式融合

传统方法（如基于 ImageBind 思想的 Aligner 基线，Girdhar et al., CVPR 2023）的核心逻辑是**强制所有模态对齐到同一联合嵌入空间**：通过 MLP 投影头将图像、3D 姿态和文本特征映射至共享空间，然后直接在该空间内施加成对或三元组对比损失。这种“硬对齐”策略隐含地假设不同模态的特征应占据相同的几何位置，忽视了模态间固有的语义鸿沟和信息密度差异，尤其对细粒度或不常见姿态的区分能力不足。

PoseEmbroider 则采用了一种更灵活的**刺绣（embroider）式融合**范式。其核心架构是一个基于 Transformer 的聚合器，接收一个可学习的全局 token $x$ 以及来自任意子集（单模态或双模态组合）的输入特征。通过自注意力机制，$x$ 动态地“收集”所有可用模态的姿态信息，最终生成一个增强的多模态感知姿态嵌入 $\bar{x}_G$。这一过程不再要求不同模态的特征在空间上精确重合，而是允许模型自主决定如何从互补的部分观测中提取最有效的表征。

### 模态特定空间的对比学习

与聚合机制相配套的关键设计是**在模态特定空间而非增强嵌入空间进行对比学习**。PoseEmbroider 将全局 token $\bar{x}_G$ 通过三个独立的 MLP 重投影头分别映射回图像空间（$\hat{v}_G$）、姿态空间（$\hat{p}_G$）和文本空间（$\hat{t}_G$），然后在每个模态的原始空间内计算 InfoNCE 损失：

$$\mathcal{L}_c(y,z) = -\frac{1}{B} \sum_{i=1}^{B} \log \frac{\exp(\gamma \sigma(y_i, z_i))}{\sum_j \exp(\gamma \sigma(y_i, z_j))}$$

总训练目标为所有输入组合 $G$ 和所有模态 $m$ 的损失之和：

$$\mathcal{L} = \sum_{G \in S} \sum_{\mathcal{M}_G} \mathcal{L}_c(m, \hat{m}_G)$$

这一设计避免了“模态空间塌缩”问题——即强制所有模态映射到同一空间可能迫使模型丢弃模态特有的判别信息。消融实验证实了该策略的有效性：在模态特定空间计算损失相比直接在增强嵌入空间计算，总 mRecall 提升了 1.5%（Table 1, row 7 vs. row 8）。

### 部分模态输入的鲁棒训练

PoseEmbroider 的第三个关键创新在于其**训练策略的完备性**：同时训练所有可能的单输入（{v}, {p}, {t}）和双输入（{v,p}, {v,t}, {p,t}）组合。这使得模型天然具备处理部分模态缺失的能力，无需在推理时进行特殊适配。相比之下，Aligner 基线最初仅支持单输入对齐，其双输入扩展版本通过平均融合双输入特征后执行对比损失，缺乏对多模态交互的显式建模。

消融实验表明，同时使用单输入和双输入训练相比仅用单输入训练，平均 mRecall 提升了 7%（Table 1, row 5 vs. row 1）。这一提升源于模型在训练过程中学习了如何从不同模态组合中提取和融合信息，从而在下游任务中展现出更强的鲁棒性。

### 因果机制总结

上述三个创新构成了一个完整的因果链条：**Transformer 聚合器**提供了灵活的信息融合能力（+1.6% mRecall vs. MLP 融合），**模态特定对比学习**保留了各模态的判别性特征（+1.5% mRecall），而**多组合训练策略**则最大化了对部分模态输入的鲁棒性（+7% mRecall）。三者协同作用，使得 PoseEmbroider 在多模态检索（总 mRecall 74.6% vs. Aligner 72.4%）、姿态指令生成（R@1 提升 36%）和 SMPL 回归（pa-MPJPE 降低 10.2%）等下游任务中均取得显著提升。

PoseEmbroider 的核心设计思想是将图像、3D 姿态和文本三种模态视为同一抽象“人体姿态”概念在不同视角下的部分观测（类比于三维物体在不同光照下的投影），通过 Transformer 将这些互补信息“刺绣”成一个统一的、多模态感知的姿态嵌入空间。该框架由四个主要模块级联构成：**预训练模态编码器**、**模态特定筛选层**、**PoseEmbroider Transformer** 和**模态特定重投影头**，整体架构如 Figure 2 所示。

![[assets/figures/papers/paper_list_l3_https_www_ecva_net_papers_eccv_2024_papers_ECCV_html_8959_ECCV_2024_pape/figures/002_Figure_2.jpg]]
*Figure 2: The PoseEmbroider framework. Each modality is encoded independently by an encoder (left). The PoseEmbroider (right) is a transformer-based model, taking a varying set of modality inputs. It produces a visual-, 3D-, semantic-aware pose representation x¯, by embroidering together available inputs. The model is trained using uni-modal contrastive losses between the modality-speci c reprojections $\hat { m } \in \{ \hat { v } , \hat { p } , \hat { t } \}$ of x¯ and the original modality encodings m $\in \{$ v , p , t $\}$ . The total objective function accounts for various ${ \bar { x } } _ { G }$ . , obtained from the set G of input modalities. x and $e _ { m }$ are learnable tokens,$^ { \circ } + \prim$...

### 输入编码与筛选

每种模态输入首先经过各自独立的**冻结预训练编码器**提取初始特征：
- 图像模态使用 ViT 编码器；
- 3D 姿态模态使用 VPoser 变体编码器；
- 文本模态先经 DistilBERT 词嵌入，再通过一个 Transformer 编码器处理。

编码器输出的特征随后进入**模态特定的可学习筛选层**（线性层 + ReLU 激活），其作用是过滤与姿态无关的冗余信息。对于产生多 token 表示的编码器（如 ViT 或文本 Transformer），该层后还通过平均池化将多 token 表示压缩为单个特征向量。这一设计确保了无论原始编码器的输出维度如何，进入核心 Transformer 的每个模态表示均为统一的一维特征。

### 核心聚合：PoseEmbroider Transformer

筛选后的模态特征与一个**可学习的全局 token** $x$ 一同输入 PoseEmbroider Transformer。该 Transformer 通过自注意力机制，从可变数量的输入模态中聚合姿态知识，最终输出增强的多模态感知姿态嵌入 $\bar{x}_G$，其中 $G$ 表示当前输入的模态组合（如 $\{v\}$、$\{p,t\}$ 等）。

框架的关键灵活性在于：Transformer 可接受**任意数量和组合的输入模态**，包括所有可能的单输入（$\{v\}$、$\{p\}$、$\{t\}$）和双输入（$\{v,p\}$、$\{v,t\}$、$\{p,t\}$）组合。训练时同时使用这些组合，使模型学会在部分模态缺失时仍能产出有意义的嵌入，这是其与简单对齐基线（如 Aligner）的本质区别——后者仅能处理单输入或通过平均融合双输入特征，缺乏 Transformer 的自适应聚合能力。

### 模态特定重投影与对比训练

与现有方法将多模态特征对齐到同一联合空间不同，PoseEmbroider 采用**模态特定重投影**策略：全局 token $\bar{x}_G$ 被分别送入三个独立的 MLP 重投影头，生成对应图像、姿态和文本空间的表示 $\hat{v}_G$、$\hat{p}_G$、$\hat{t}_G$。训练目标是在各模态的**原生空间**中计算 InfoNCE 对比损失：

$$\mathcal{L}_c(y,z) = -\frac{1}{B} \sum_{i=1}^{B} \log \frac{\exp(\gamma \sigma(y_i, z_i))}{\sum_j \exp(\gamma \sigma(y_i, z_j))}$$

其中 $y$ 为原始模态编码，$z$ 为重投影表示，$\gamma$ 为温度参数，$\sigma$ 为余弦相似度。总损失为所有输入组合 $G$ 和所有模态类型 $m$ 上的 InfoNCE 损失之和：

$$\mathcal{L} = \sum_{G \in S} \sum_{\mathcal{M}_G} \mathcal{L}_c(m, \hat{m}_G)$$

这一设计避免了强制所有模态坍缩到同一空间可能带来的信息损失，同时通过“拉近重投影与原始编码”的方式，隐式地约束全局 token 学习到跨模态一致的姿态表示。消融实验证实，在模态特定空间计算对比损失相比直接在增强嵌入空间计算，总 mRecall 提升 1.5%（Table 1, row 7 vs. row 8）。

### 信息流总结

整体信息流可概括为：**多模态原始数据 → 冻结编码器提取 → 可学习筛选层压缩 → Transformer 全局 token 聚合 → 重投影至各模态空间 → 单模态对比损失反向传播**。训练完成后，冻结的 PoseEmbroider 可为任意模态组合生成统一的姿态嵌入，直接用于下游检索、生成或回归任务。

### 整体框架

PoseEmbroider 的核心思想是将图像、3D 姿态和文本视为同一抽象“人体姿态”概念的三种互补部分观测，通过 Transformer 将这些信息“刺绣”成一个更丰富、多模态感知的姿态嵌入空间。框架由四个关键模块构成：**冻结的预训练编码器**、**模态特定筛选层**、**PoseEmbroider Transformer** 和**模态特定重投影 MLP**。

### 预训练模态编码器（冻结）

三种模态分别通过各自的冻结编码器提取初始特征。图像使用 ViT 编码器，3D 姿态使用 VPoser 变体编码器，文本使用 DistilBERT 词嵌入后接 Transformer 编码器。这些编码器在训练过程中保持冻结，不参与梯度更新，确保各模态的预训练知识不被破坏。

### 模态特定筛选层

每个编码器的输出首先经过一个可学习的线性层和 ReLU 激活函数，用于过滤与姿态无关的模态特定信息。对于产生多 token 表示的编码器（如 ViT），随后通过平均池化将多个 token 压缩为单个特征向量。这一步骤确保输入到 Transformer 的每个模态都是紧凑的单一向量表示。

### PoseEmbroider Transformer

这是框架的核心聚合模块。Transformer 接收可变数量的输入模态（单输入或双输入的任意组合）以及一个可学习的全局 token $x$。通过自注意力机制，全局 token $x$ 与所有输入模态特征进行交互，聚合跨模态的姿态知识，最终输出增强的多模态感知姿态嵌入 $\bar{x}_G$（其中 $G$ 表示输入的模态集合）。这种设计使得模型能够处理任意模态组合的输入，具备部分模态缺失时的鲁棒性。

### 模态特定重投影 MLP

与现有方法直接在联合嵌入空间进行对比学习不同，PoseEmbroider 将全局 token $\bar{x}_G$ 分别投影回各模态的原始空间。具体而言，通过三个独立的 MLP 将 $\bar{x}_G$ 重投影为图像空间 $\hat{v}_G$、姿态空间 $\hat{p}_G$ 和文本空间 $\hat{t}_G$。这一设计的核心洞察是避免强制所有模态对齐到同一联合空间导致的模态空间塌缩，而是在各自模态特定空间内保持对比学习的有效性。

### 核心公式：InfoNCE 对比损失

训练采用单模态 InfoNCE 对比损失，在模态特定空间内拉近正样本对、推开负样本对。对于给定的原始编码 $y$ 和重投影 $z$，损失函数定义为：

$$\mathcal{L}_c(y,z) = -\frac{1}{B} \sum_{i=1}^{B} \log \frac{\exp(\gamma \sigma(y_i, z_i))}{\sum_j \exp(\gamma \sigma(y_i, z_j))}$$

其中 $B$ 为批次大小，$\gamma$ 为温度参数，$\sigma$ 为余弦相似度。该损失确保重投影表示 $\hat{m}_G$ 与对应原始模态编码 $m$ 在语义上保持一致，同时与其他样本的编码保持区分度。

### 核心公式：总训练目标

总损失函数对所有考虑的输入模态组合 $G$ 以及所有模态类型进行求和：

$$\mathcal{L} = \sum_{G \in S} \sum_{\mathcal{M}_G} \mathcal{L}_c(m, \hat{m}_G)$$

其中 $S$ 为所有训练输入组合的集合（包括单输入 $\{v\}, \{p\}, \{t\}$ 和双输入 $\{v,p\}, \{v,t\}, \{p,t\}$），$\mathcal{M}_G$ 为组合 $G$ 中涉及的模态集合。通过同时训练所有可能的输入组合，模型学会从任意部分观测中构建完整的多模态感知姿态表示。消融实验表明，相比仅使用单输入训练，这种多组合训练策略使平均 mRecall 提升了 7%（Table 1, row 5 vs. row 1）。

### 与 Aligner 基线的关键差异

Aligner 基线（Girdhar et al., CVPR 2023 的 ImageBind 风格方法）采用 MLP 投影头将各模态映射到联合嵌入空间，直接在该空间计算成对或三元组对比损失。双输入扩展版本通过平均融合多模态特征后执行对比损失。PoseEmbroider 与之有两个核心差异：（1）使用 Transformer 替代简单的平均融合进行信息聚合，消融实验表明这带来 1.6% 的 mRecall 提升（Table 1, row 6 vs. row 7）；（2）在模态特定重投影空间而非联合空间计算对比损失，进一步提升 1.5% mRecall（Table 1, row 7 vs. row 8）。

![[assets/figures/papers/paper_list_l3_https_www_ecva_net_papers_eccv_2024_papers_ECCV_html_8959_ECCV_2024_pape/figures/006_Figure_5.jpg]]
*Figure 5: The pose instruction generation model. We train the model on pairs of poses (pA, pB) and use our frozen PoseEmbroider to encode them. These two embeddings are fused with TIRG [63], whose output is used to condition an auto-regressive transformer text decoder via cross-attentions. At test time, the trained model can be directly applied on poses, images or a mix of both*

![[assets/figures/papers/paper_list_l3_https_www_ecva_net_papers_eccv_2024_papers_ECCV_html_8959_ECCV_2024_pape/figures/008_Figure_6.jpg]]
*Figure 6: Instruction generations on real-world images using the PoseEmbroider pose representation. The text model was trained using the frozen PoseEmbroider embeddings of 3D poses only. The generated text is shown below each image pairs*

## 实验与关键发现

### 多模态检索实验

PoseEmbroider的核心能力首先在多模态检索任务上得到验证。实验在BEDLAM-Script验证集上进行，模型需根据单模态或双模态查询，从候选库中检索匹配的其他模态样本。表1汇总了主要结果。

**表1** [Table 1] 展示了Aligner基线（单输入与双输入扩展）与PoseEmbroider各变体的对比。Aligner（单输入）可视为ImageBind（Girdhar et al., CVPR 2023）在人体姿态领域的应用，其最佳单输入变体总mRecall为72.4%。PoseEmbroider（S）——即同时使用单输入和双输入组合训练的完整模型——达到74.6%总mRecall，提升2.2个百分点。其中，双查询mRecall从Aligner的78.5%提升至82.2%（+4.7%），说明Transformer聚合机制对融合多模态信息尤为有效。

消融实验揭示了三个关键设计选择的作用：
- **输入组合训练策略**：仅用单输入训练时，PoseEmbroider平均mRecall为67.9%；加入双输入组合训练后提升至74.6%（+7%），验证了多输入训练对模型鲁棒性的重要性。
- **核心聚合器架构**：将Transformer替换为MLP简单相加融合时，总mRecall下降1.6%（73.0% vs. 74.6%），表明自注意力聚合优于浅层融合。
- **对比学习空间**：在模态特定重投影空间计算InfoNCE损失，相比直接在增强嵌入空间计算对比损失，总mRecall提升1.5%（74.6% vs. 73.1%），证实了避免模态空间塌缩的有效性。

定性结果（图3、图4）进一步展示了模型的任意模态互检能力和编辑式检索能力——用户可通过文本描述修改图像中的姿态要求，系统能检索到符合新约束的姿态，即使图像存在人工遮挡。

### 姿态指令生成实验

姿态指令生成任务评估PoseEmbroider表示在下游生成任务中的迁移能力。模型架构如图5所示：冻结的PoseEmbroider编码姿态对（P_A, P_B），通过TIRG模块融合后条件化自回归文本解码器。训练仅使用3D姿态对，测试时可直接应用于图像输入。

**表2** [Table 2] 的结果显示，PoseEmbroider在所有查询类型上均优于Aligner基线。当两个输入均为3D姿态时，PoseEmbroider的R@1达到43.1%，相比Aligner的31.8%提升36%；在PoseFix-OOS测试集上，提升幅度达41%。值得注意的是，3D姿态输入的性能远优于图像输入（R@1: 43.1 vs. 15.6），这反映了训练数据仅包含3D姿态对的限制。然而，图6的定性示例表明，仅在3D姿态上训练的模型，其表示仍能迁移到真实世界图像，生成合理的姿态修正指令。

### SMPL回归实验

SMPL回归任务验证PoseEmbroider表示在3D人体重建中的实用性。回归头仅在BEDLAM-Script上训练，使用冻结的图像特征作为输入。

**表3** [Table 3] 报告了pa-MPJPE指标。仅使用图像输入时，PoseEmbroider的误差为49mm，与Aligner持平。关键优势在于PoseEmbroider允许融合可选文本提示：当提供文本描述（如“左臂抬起”）时，误差降至44mm，相对提升约11%。这体现了PoseEmbroider的核心价值——在推理时可灵活利用额外模态信息提升任务性能，而无需重新训练。然而，在3DPW真实数据集上，误差仍然较大，暴露了合成数据训练的泛化瓶颈。

### 失败模式与局限分析

综合三项实验，PoseEmbroider的主要失败模式可归纳如下：

1. **训练数据规模与多样性不足**：所有训练仅使用50k合成渲染样本（BEDLAM），远少于CLIP等大规模对比学习模型。这导致姿态指令生成中图像输入性能显著弱于3D姿态输入（R@1差距达27.5%），以及SMPL回归在真实数据集上的高误差。

2. **模态信息不对称**：3D姿态编码器（VPoser变体）提供的是精确的关节旋转信息，而图像编码器仅能提取外观特征。在需要精确几何理解的任务中（如指令生成），这种信息不对称被放大，导致图像输入性能受限。

3. **对比学习目标的局限性**：InfoNCE仅优化排序目标，未引入预测或生成式损失。这可能使模型倾向于学习模态间的“可区分”特征，而非“可重构”的完备表示，限制了在下游回归任务中的进一步提升。

4. **真实世界泛化差距**：尽管姿态指令生成在真实图像上展现出一定的零样本迁移能力，但SMPL回归在3DPW上的误差仍较高，表明合成到真实的域差距尚未被多模态表示充分弥合。

![[assets/figures/papers/paper_list_l3_https_www_ecva_net_papers_eccv_2024_papers_ECCV_html_8959_ECCV_2024_pape/figures/003_Table_1.jpg]]
*Table 1: Multi-modal retrieval results. Models are trained on BEDLAM-Script and evaluated on its validation set. The total mRecall is the average of single and dual, corresponding to the average over all single- and dual-query retrieval tasks respectively. V, P, and T refer to the visual (image), pose and text modalities respectively. The aligner trained on single-input only ( rst row) corresponds to the idea of [14, 24]*

![[assets/figures/papers/paper_list_l3_https_www_ecva_net_papers_eccv_2024_papers_ECCV_html_8959_ECCV_2024_pape/figures/007_Table_2.jpg]]
*Table 2: Text generation results for different query types. Models are trained on BEDLAM-Fix using pairs of poses only, and evaluated on the associated validation split for queries of different natures. We further netune the text decoder on a mix of BEDLAM-Fix and PoseFix-OOS data, and report results on the test set of PoseFix-OOS. The Aligner baseline represents [15]*

![[assets/figures/papers/paper_list_l3_https_www_ecva_net_papers_eccv_2024_papers_ECCV_html_8959_ECCV_2024_pape/figures/009_Table_3.jpg]]
*Table 3: SMPL regression results for different representations and inputs. The regression head is trained solely on BEDLAM-Script, with frozen image-based features of the Aligner/PoseEmbroider models. We report the pa-MPJPE in mm with the ground truth pose, on BEDLAM-Script (validation set) and 3DPW [47] (test set)*

## 定位与知识库关联

### 核心思想溯源与基线关系

PoseEmbroider 的出发点是对现有视觉-语义对齐方法在人体姿态领域的能力边界进行诊断。其最直接的参照系是 **ImageBind**（Girdhar et al., CVPR 2023）所代表的多模态联合嵌入范式——通过对比学习将多种模态对齐到同一联合空间。论文将这一范式在人体姿态领域的直接应用称为 **Aligner**（单输入版本），作为核心基线。Aligner 使用与 PoseEmbroider 完全相同的冻结预训练编码器（图像 ViT、3D 姿态 VPoser 变体、文本 DistilBERT），仅在编码器后接可学习的 MLP 投影头，并通过成对/三元组对比损失进行训练。这一设计确保了方法比较的公平性：所有性能差异均可归因于架构创新本身，而非编码器质量或数据差异。

PoseEmbroider 对 Aligner 范式的改造体现在三个相互耦合的维度：

1. **从“对齐空间”到“聚合-重投影”的范式转换**：Aligner 强制所有模态对齐到同一联合空间，这在模态信息互补但异构时可能导致“模态空间塌缩”——各模态特有的判别信息被对齐压力所压制。PoseEmbroider 改为在模态特定空间进行对比学习：先用 Transformer 将多模态信息聚合到全局 token，再将全局 token 重投影回各模态空间，分别计算 InfoNCE 损失。这一设计保留了各模态空间的固有结构，同时通过共享的全局 token 实现信息融合。

2. **从“固定输入组合”到“可变模态集合”的架构设计**：Aligner 的双输入扩展版本通过平均融合两模态特征后执行对比损失，但无法优雅处理单输入场景。PoseEmbroider 的 Transformer 架构天然支持可变数量的输入模态——全局 token $x$ 通过自注意力从任意子集的模态特征中聚合信息，使得同一模型可同时处理 $\{v\}$、$\{p\}$、$\{t\}$、$\{v,p\}$、$\{v,t\}$、$\{p,t\}$ 六种输入组合。消融实验表明，这种多输入组合联合训练相比仅用单输入训练，平均 mRecall 提升 7%（Table 1, row 5 vs. row 1）。

3. **从“MLP 融合”到“Transformer 聚合”的表征能力升级**：将 Aligner 的平均融合替换为 Transformer 聚合器，即使保留联合空间对比损失，总 mRecall 仍提升 1.6%（Table 1, row 6 vs. row 7）。进一步将对比损失移至模态特定重投影空间，再提升 1.5%（Table 1, row 7 vs. row 8），验证了两项创新的独立贡献。

在姿态指令生成任务上，基线 **PoseFix**（Delmas et al., ICCV 2023）采用基于 3D 姿态对的文本生成模型。PoseEmbroider 在该任务中的角色是替代 PoseFix 原有的姿态编码器，文本解码器架构保持不变。当完全基于 3D 姿态输入时，PoseEmbroider 编码器的 R@1 达到 43.1%，较 Aligner 基线的 31.8% 提升 36%（Table 2），表明更丰富的多模态感知嵌入对下游生成任务具有显著的迁移价值。

### 适用边界与限制条件

PoseEmbroider 的当前设计存在若干明确的适用边界，这些边界既源于技术选择，也受限于资源约束：

**数据规模与多样性的根本限制**。模型训练仅使用 BEDLAM-Script 数据集（约 50k 样本），远少于 CLIP 等大规模对比学习模型（通常使用数亿样本）。这一规模限制直接影响了嵌入空间的细粒度判别能力和泛化范围。论文明确指出，当前方法尚无法利用现实中大量存在的仅包含部分模态的数据集（如图像-文本对、图像-姿态对），训练范式要求三模态同时存在的完整数据。

**合成数据的域迁移瓶颈**。所有训练数据均为 BEDLAM 合成渲染图像，虽然姿态指令生成任务在真实图像上表现出一定迁移能力（Figure 6），但 SMPL 回归在真实数据集 3DPW 上的误差仍然较大（Table 3），真实世界泛化存在可观测的性能差距。这一限制源于合成图像与真实图像在纹理、光照、背景复杂度等方面的分布差异，而非方法本身的架构缺陷。

**监督信号的保守性**。当前训练仅采用 InfoNCE 排序损失，未引入预测目标特征或生成式损失。这意味着模型学习的是“区分正负样本”而非“重建模态信息”，可能未能充分利用多模态间的互补信息。论文将此列为开放问题，暗示引入更激进的监督信号（如跨模态预测）可能进一步提升表示质量。

**模态覆盖的有限性**。当前框架仅处理图像、3D 姿态和文本三种模态。对于深度图、2D 关键点、惯性传感器（IMU）等在实际应用中常见的模态，框架尚未提供接入机制。论文将此列为未来工作方向，但当前版本不具备此类扩展能力。

### 在知识库中的定位

PoseEmbroider 在多模态人体理解领域占据了一个独特的方法论位置。与传统的多模态对齐方法（如 ImageBind、CLIP）不同，它不追求将所有模态映射到统一的度量空间，而是构建一个以“人体姿态”为中心的、可融合部分观测的表示空间。这一设计哲学与“多模态融合”和“跨模态检索”的传统二分法形成差异：它既不是简单的晚期融合（late fusion），也不是纯粹的跨模态映射，而是通过一个共享的全局 token 实现“信息刺绣”（embroidering）——将来自不同模态的部分信息编织成更完整的姿态表征。

从技术谱系看，PoseEmbroider 继承了 Transformer 在多模态聚合中的通用能力，但其核心创新——模态特定重投影对比学习——提供了一种避免模态空间塌缩的新机制。这一机制对多模态学习社区具有潜在的参考价值，尤其是在模态异构性强、对齐标注稀缺的场景下。

### 开放问题与未来方向

论文明确提出了三个值得进一步探索的方向：

1. **多数据集联合训练**：能否从多个仅包含部分模态的数据集（如仅图像-文本、仅图像-姿态）进行联合训练，使模型在无需完整三模态标注的情况下扩展训练规模和应用范围？这需要设计新的训练策略来处理模态缺失的样本。

2. **更强监督信号的引入**：采用预测目标模态特征或生成对应数据的方式，是否能获得更高质量的多模态姿态表示？这涉及从“对比判别”向“生成重建”的范式扩展。

3. **额外模态的纳入**：将深度图、2D 关键点、IMU 信号等模态纳入框架，是否能进一步提升对遮挡、模糊或罕见姿态的理解能力？这需要评估新模态的信息增益与架构扩展成本之间的权衡。

此外，一个论文未明确讨论但值得关注的问题是：当前方法在 BEDLAM-Script 上的性能提升（+2.2% 总 mRecall）虽然一致且消融充分，但绝对提升幅度相对有限。这是否意味着在现有数据规模下，架构创新的收益已接近饱和？扩大训练数据后，PoseEmbroider 与 Aligner 的差距是会放大（表明架构优势在更大数据下更显著）还是缩小（表明 Aligner 的简单范式在充足数据下同样有效），仍是一个需要实证检验的开放问题。

## 原文 PDF

![[paperPDFs/ECCV_2024/PoseEmbroider_Towards_a_3D_Visual_Semantic_aware_Human_Pose_Representation.pdf]]
