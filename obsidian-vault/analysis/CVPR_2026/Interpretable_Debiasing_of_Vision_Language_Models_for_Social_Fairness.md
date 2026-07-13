---
title: Interpretable Debiasing of Vision-Language Models for Social Fairness
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Interpretable_Debiasing_of_Vision_Language_Models_for_Social_Fairness.pdf
project_link: null
code_link: null
aliases:
- IDVLMSF
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: Interpretable
primary_logic: Interpretable
claims:
- Interpretable
---

# Interpretable Debiasing of Vision-Language Models for Social Fairness

> [!tip] 核心洞察
> Interpretable

| 字段 | 内容 |
|------|------|
| 中文题名 | Interpretable Debiasing of Vision-Language Models for Social Fairness |
| 英文题名 | Interpretable Debiasing of Vision-Language Models for Social Fairness |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.24014) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method |  |
| Dataset | FairFace, CocoGenderTxt, VLAGenderBias, SBBench, ImageNette, MME, MMMU-dev, SEED-Bench-2 |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

视觉语言模型（VLMs）在图像检索与视觉问答等任务中普遍存在社会偏见——模型倾向于检索某一性别、种族或年龄段的图像，或在面对模糊图像-文本对时给出武断的确定性回答。这种偏见源于模型内部表征中编码的社会属性信息，但现有去偏方法大多缺乏可解释性，难以精确定位和调控偏见来源。

本文提出 **DEBIASLENS**，一个可解释的 VLM 去偏框架。其核心思路是：通过在 VLM 的图像/文本编码器之上训练稀疏自编码器（Sparse Autoencoder, SAE），无需社会属性标签即可自动发现对特定人口统计属性高度响应的“社会神经元”；随后在推理阶段将这些社会神经元的激活置零，从而在保持模型通用性能的前提下显著降低社会偏见。

在 FairFace 文本到图像检索基准上，DEBIASLENS 使 CLIP ViT-B/16 的 Max Skew@1000 从 21.9 降至 7.1（降低 67.6%）；在 InternVL2 等大视觉语言模型上，性别不成比例率下降 40–50%。方法在去偏效果与通用性能之间取得了现有工作中最优的权衡，且社会神经元展现出高度的属性特异性——调控性别神经元仅缓解性别偏见，不影响种族或年龄偏见的度量。

DEBIASLENS 属于**基于内部表征干预的后处理去偏方法**，其方法定位介于特征空间线性投影去偏与全模型微调之间：它不修改原始模型权重，而是通过 SAE 在特征空间中解耦并中和特定的社会属性维度。与依赖全局线性方向的方法（如投影去偏）不同，SAE 的稀疏激活机制使不同输入激活不同的神经元集合，从而避免了单一全局方向无法稳定分离社会属性的问题。

视觉-语言模型（VLMs）和大规模视觉-语言模型（LVLMs）在跨模态检索、视觉问答等任务中取得了显著进展，但其内部表征中普遍存在社会偏见——模型倾向于将特定人口统计群体与刻板印象属性过度关联，导致检索结果出现性别、种族、年龄等维度的分布偏斜，或在模糊图像-文本对上给出带有偏见倾向的确定性回答（Figure 1）。

现有去偏方法主要沿两条路径展开：**对抗训练**通过在特征空间中消除敏感属性信息来学习公平表征，但训练开销大且难以泛化到多属性场景；**提示工程**通过修改文本提示引导模型输出公平结果，然而依赖人工设计模板，对不同模型和任务的迁移性有限。更关键的是，这些方法大多将去偏视为一个“黑箱校正”过程——它们可以降低偏见指标，却无法揭示模型内部哪些表征单元承载了社会偏见，也缺乏对去偏操作的可解释性验证。这一缺口导致两个实际问题：一是当去偏效果不理想时，难以定位失败原因；二是无法确保去偏干预不会意外损害模型的通用表征能力。

本文的动机正是填补这一可解释性空白：**能否将VLM的社会偏见归因到具体的神经元级别表征，并通过精准调制这些神经元来实现可控、可解释的去偏？** 为此，作者提出DEBIASLENS框架，利用稀疏自编码器（SAE）在无需社会属性标签的条件下，自动定位多模态编码器中对特定人口统计群体高度响应的“社会神经元”，并通过干预这些神经元的激活值来抑制偏见表征，从而将去偏从黑箱校正转变为一种可解释的干预范式。

## 核心方法与创新机理

DEBIASLENS 的核心创新在于将**可解释性机制**系统性地引入 VLM 社会偏见消除，其技术路径围绕三个紧密耦合的“changed slots”展开：

1.  **无监督社会神经元定位（从特征到可解释概念）**
    传统去偏方法通常将模型视为黑箱，通过对抗训练或提示工程间接抑制偏见。DEBIASLENS 的关键突破在于利用**稀疏自编码器（SAE）**在 VLM 多模态编码器的最后一层特征空间上，无监督地解耦出对特定社会属性（性别、种族、年龄）高度敏感的“社会神经元”。SAE 的训练仅需人脸图像或描述文本数据集，**无需社会属性标签**，其重建损失与稀疏性惩罚的联合优化（公式 $\mathcal{L}_1(\mathbf{v}) = \mathcal{L}_R(\mathbf{v}) + \lambda \|\phi(\mathbf{v})\|_1$）迫使模型学习到稀疏且可解释的特征表示。这一设计将“去偏”从黑箱操作转变为对模型内部表征的**透明调控**。

2.  **基于一致性与特异性的神经元筛选（从稀疏激活到因果调控）**
    在获得 SAE 的稀疏激活后，DEBIASLENS 并非简单抑制所有高激活神经元，而是通过计算同一社会属性组内激活的**一致性**与跨组**特异性**，精准筛选出每个属性组中平均激活最高的单个神经元（$j_g^* = \arg\max_{j \in \mathcal{N}_g} (\bar{\mathbf{s}}_j)$）。实验证据表明，**仅关闭这一个 top-1 社会神经元**，即可达到与关闭所有有效神经元相当的偏见消除效果（Table 2 及 Section 4.3），这揭示了社会偏见在 VLM 表征中存在高度集中的“瓶颈”，是方法高效性的因果基础。

3.  **推理阶段零样本特征中性化（从训练到部署的轻量干预）**
    DEBIASLENS 在推理时无需重新训练模型或依赖额外数据，仅需将 SAE 激活向量中对应社会神经元的值置为零（$\mathbf{z}'[j] = \gamma \text{ if } j \in \mathcal{Z}_B$），即可生成去偏后的特征。这种**即插即用**的干预机制使其可无缝适配 CLIP、InternVL2、LLaVA 等多种 VLM 架构，且不改变原始模型权重。在 FairFace T2I 检索任务中，DEBIASLENS (T) 将 Max Skew@1000 从基线的 21.9 降至 7.1（-67.6%），同时在 LVLM 的性别歧义问答中实现 40–50% 的 disproportion 下降（Figure 4），证明了该方法在跨模态、跨任务场景下的鲁棒性。

**与现有工作的本质差异**：传统方法（如对抗去偏、提示调优）直接优化输出分布，而 DEBIASLENS 通过 SAE 构建了一个**可审计的中间表征层**，使社会偏见从“隐式编码”变为“显式神经元”，从而实现了对偏见的精准溯源与最小化干预。这一“先解释、后调控”的范式，是其在可解释性与效率上超越 baseline 的根本原因。

DEBIASLENS 提出了一种可解释的 VLM 社会偏见消除框架，其核心思想是：**通过稀疏自编码器（Sparse Autoencoder, SAE）在多模态编码器的特征空间中定位并调控“社会神经元”，从而在推理阶段实现透明的偏见抑制**。整个 pipeline 由三个顺序阶段构成，如图 Figure 2 所示。

![[assets/figures/papers/paper_list_l760_https_arxiv_org_abs_2602_24014/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our interpretable VLM debiasing framework. DEBIASLENS consists of three stages: (1) SAE is trained on top of the last layer of the VLM image/text encoder (Section 3.1). (2) The social neurons are identified based on the consistency and specificity of SAE activations across data (Section 3.2). (3) The selected neurons are activated to generate debiased features, weighted summed with original features for further usage across downstream tasks (Section 3.3)*

### 阶段一：SAE 训练（Section 3.1）

在 VLM 图像/文本编码器的最后一层之上附加一个 SAE。SAE 接收编码器输出的原始特征向量 $\mathbf{v} \in \mathbb{R}^d$，将其分解为高维稀疏激活向量 $\phi(\mathbf{v}) \in \mathbb{R}^\omega$（$\omega \geq d$），再通过解码器重建原始特征。训练目标为：

$$
\mathcal{L}_1(\mathbf{v}) = \mathcal{L}_R(\mathbf{v}) + \lambda \|\phi(\mathbf{v})\|_1
$$

其中重建损失 $\mathcal{L}_R(\mathbf{v})$ 采用多尺度设计，在不同 SAE 深度 $m \in \mathcal{M}$ 上累加重建误差：

$$
\mathcal{L}_R(\mathbf{v}) = \sum_{m \in \mathcal{M}} \|\mathbf{v} - \mathbf{W}_{\mathrm{dec}}^{\top} \phi_{1:m}(\mathbf{v})\|_2^2
$$

关键设计在于：SAE 的训练**仅使用面部图像或文本描述数据集，无需任何社会属性标签**。这使得 SAE 能够以无监督方式学习到对特定人口统计特征高度敏感的神经元表征。

### 阶段二：社会神经元识别（Section 3.2）

在 SAE 训练完成后，利用带社会属性分组标签的探测数据集（如 FairFace 用于图像编码器，CocoGenderTxt 用于文本编码器），通过统计 SAE 激活模式来识别社会神经元。具体而言：

1. 对每个属性组 $g$（如性别-男性、性别-女性），收集该组所有样本在 SAE 各神经元上的激活值。
2. 计算神经元 $j$ 在组 $g$ 内的平均激活：

   $$\bar{\mathbf{s}}_j = \frac{1}{S_g} \sum_{i=1}^{S_g} \mathbf{x}_{i,j}^{(g)}$$

3. 选择平均激活最高的神经元作为该组的社会神经元：

   $$j_g^* = \arg\max_{j \in \mathcal{N}_g} (\bar{\mathbf{s}}_j)$$

这一过程的输出是一组与特定社会属性（性别、种族、年龄等）强关联的神经元索引集合。

### 阶段三：去偏特征生成（Section 3.3）

在推理阶段，对 SAE 的激活向量 $\mathbf{z}$ 中对应于已识别社会神经元的元素进行中性化处理——将其值置为零（或一个小的常数 $\gamma$），其他神经元保持不变：

$$\mathbf{z}'[j] = \begin{cases} \gamma & \text{if } j \in \mathcal{Z}_B \\ \mathbf{z}[j] & \text{otherwise} \end{cases}$$

随后用修改后的激活向量通过 SAE 解码器重建特征，替代原始编码器特征参与下游的多模态匹配或生成任务。这种“定位-抑制”的操作模式使得 DEBIASLENS 能够在不重新训练或微调原始 VLM 的前提下，实现即插即用的社会偏见消除。

### 模块关系与数据流总结

整个框架的数据流可概括为：**编码器特征 → SAE 稀疏分解 → 社会神经元定位（离线）→ 激活抑制 → 特征重建 → 下游任务**。三个阶段的依赖关系是严格顺序的：SAE 必须先完成训练，才能进行神经元识别；神经元识别完成后，推理阶段的抑制操作才有明确的干预目标。这种模块化设计使得 DEBIASLENS 天然具备模型无关性——只需在目标编码器上独立训练 SAE 并完成神经元探测，即可部署到任意使用该编码器的 VLM 或 LVLM 中（详见 Table 5 中支持的模型范围）。

![[assets/figures/papers/paper_list_l760_https_arxiv_org_abs_2602_24014/figures/015_Table_5.jpg]]
*Table 5: Overview of multimodal models. The table lists the image and text encoders used in VLMs and LVLMs considered in this work*

DEBIASLENS 框架由三个核心模块级联构成：**SAE 训练**、**社会神经元识别** 与**去偏特征生成**。其关键洞察在于，通过在 VLM 编码器的最后一层之上训练稀疏自编码器（SAE），可以将原始特征分解为一组稀疏激活，进而定位出对特定社会属性（性别、种族、年龄）高度响应的“社会神经元”，并在推理阶段通过置零这些神经元的激活值来实现可解释的去偏。

### SAE 训练

SAE 的核心目标是将原始特征 $\mathbf{v} \in \mathbb{R}^d$ 分解为稀疏激活向量 $\phi(\mathbf{v}) \in \mathbb{R}^\omega$（$\omega \geq d$），并从中重建原始特征。训练采用联合损失函数，由重建误差与稀疏性惩罚两项构成：

$$
\mathcal{L}_{1}(\mathbf{v}) = \mathcal{L}_{R}(\mathbf{v}) + \lambda \|\phi(\mathbf{v})\|_1
$$

其中 $\lambda$ 为稀疏性惩罚系数。为提升重建质量，作者引入了多尺度重建损失，对不同深度的 SAE 特征同时施加约束：

$$
\mathcal{L}_{R}(\mathbf{v}) = \sum_{m \in \mathcal{M}} \left\| \mathbf{v} - \mathbf{W}_{\mathrm{dec}}^{\top} \phi_{1:m}(\mathbf{v}) \right\|_{2}^{2}
$$

式中 $\mathcal{M}$ 为预设的深度集合，$\phi_{1:m}(\mathbf{v})$ 表示取前 $m$ 维的截断激活向量，$\mathbf{W}_{\mathrm{dec}}$ 为解码器权重矩阵。该设计使 SAE 在不同稀疏度水平下均能保持对原始语义的保真度。

### 社会神经元识别

SAE 训练完成后，每个神经元 $j$ 在特定社会属性组 $g$（如“女性”或“年轻”）上的平均激活值由下式给出：

$$
\bar{\mathbf{s}}_{j} = \frac{1}{S_{g}} \sum_{i=1}^{S_{g}} \mathbf{x}_{i,j}^{(g)}
$$

其中 $S_{g}$ 为组 $g$ 的样本数，$\mathbf{x}_{i,j}^{(g)}$ 为第 $i$ 个样本在神经元 $j$ 上的 SAE 激活值。随后，在每个属性组内选择平均激活最高的神经元作为该组的社会神经元：

$$
j_{g}^{*} = \arg\max_{j \in \mathcal{N}_{g}} \left( \bar{\mathbf{s}}_{j} \right)
$$

这一选择策略的关键实验支撑是：**仅去激活 top-1 社会神经元即可获得与去激活所有有效神经元相当的去偏效果**，验证了社会信息的表征高度集中于极少数神经元。

### 去偏特征生成

在推理阶段，对于识别出的社会神经元集合 $\mathcal{Z}_{\mathrm{B}}$，将其 SAE 激活值强制置为常数 $\gamma$（通常取 0），其他神经元保持原值，从而生成去偏后的特征 $\mathbf{z}'$：

$$
\mathbf{z}'[j] = \begin{cases}
\gamma, & \text{if } j \in \mathcal{Z}_{\mathrm{B}} \\
\mathbf{z}[j], & \text{otherwise}
\end{cases}
$$

该操作等价于从特征空间中擦除社会属性相关的方向分量。实验表明，当 SAE 的扩张因子设为 8、神经元一致性阈值 $\tau = 0.9$、去偏强度 $\alpha = 0.6$ 时，方法在去偏效果与通用性能之间取得最优权衡。

## 实验与关键发现

### 4.1 实验设置

**数据集与评估指标**。T2I检索公平性评估采用FairFace数据集（10,954张裁剪人脸图像），配合形容词提示（Adjective prompts）和刻板印象提示（Stereotype prompts）进行性别偏差评测。LVLM公平性评估采用VLAGenderBias（5k张人脸图像）和SBBench（14.6k张图像，涵盖年龄和性别类别）。T2I检索的核心指标为Max Skew@1000（值越低越公平），LVLM评估采用性别回答差异比例（disproportion rate）和准确率。

**实现细节**。SAE的扩展因子（expansion factor）设为8，稀疏性阈值τ设为0.9，去偏强度α设为0.6（基于4.3节的消融结果）。除非特别说明，SAE的训练和社会神经元探测均使用FairFace和Cocogendertxt数据集，分别对应图像编码器和文本编码器。

### 4.2 主实验结果

**T2I检索公平性**。Table 1展示了FairFace数据集上的Max Skew@1000结果。在形容词提示场景下，DEBIASLENS (T)（SAE附加于文本编码器）将Max Skew从CLIP ViT-B/16†的21.9降至7.1，降幅达67.6%；在刻板印象提示场景下，Max Skew从23.4降至8.1。DEBIASLENS取得了与当前最先进方法（SoTA）可比甚至更优的偏差缓解效果。

**LVLM公平性**。Figure 4展示了偏差缓解与通用性能之间的权衡关系。DEBIASLENS-Intern（α=0.6）在InternVL2上实现了40–50%的性别回答差异比例降低，同时在偏差缓解与通用性能之间取得了最佳权衡（图中向左上角方向最优）。

### 4.3 可解释社会神经元分析

**神经元特异性**。Table 2展示了CLIP ViT-B/16图像编码器的神经元特异性结果。关键发现包括：
- 针对性去激活社会神经元比随机去激活神经元产生显著更低的偏差分数。例如，在α=1.0时，年龄神经元去激活使年龄偏差Max Skew降低17.4%。
- 性别神经元表现出高度特异性：调节性别神经元仅缓解性别偏差，对年龄和种族偏差影响甚微。
- 跨属性效应有限但存在：调节年龄神经元对性别偏差也产生一定的缓解效果（Max Skew从10.6降至9.2，α=1.0），表明不同社会属性神经元之间存在部分功能重叠。

Figure 5进一步验证了CLIP文本编码器的神经元特异性——调节性别神经元仅缓解性别偏差，证实了社会神经元的高属性特异性。

**Top-1神经元有效性**。实验表明，仅去激活每个偏差属性组中SAE激活值最高的top-1社会神经元，即可达到与去激活所有有效神经元相当的性能，验证了社会神经元定位的精准性。

### 4.4 消融与权衡分析

**去偏强度α的影响**。Table 4展示了不同加权比例下DEBIASLENS应用于CLIP和LLaVA的通用性能与偏差缓解得分。结果表明，偏差缓解与通用性能之间存在固有权衡——更高的α值带来更强的去偏效果，但会牺牲一定的通用任务性能。这一现象在两种模态和模型类型中均一致存在。

**训练数据与探测数据的影响**。Table 3展示了DEBIASLENS应用于LVLM时，不同SAE训练数据集和社会神经元选择策略对SBBench准确率的影响。当SAE使用FairFace数据集训练并基于FairFace选择性别神经元时，模型在规则评估和模型评估两种方式下均取得最佳性能，表明训练数据与社会神经元探测数据的一致性对去偏效果至关重要。

**非重叠数据集的泛化性**。Table 6展示了在非重叠数据集上的偏差得分结果，验证了DEBIASLENS在训练数据分布之外的泛化能力。

### 4.5 计算成本与交叉公平性

**计算效率**。Table 7展示了计算成本结果。DEBIASLENS以极低的额外计算开销（SAE仅在编码器最后一层之上训练，推理时仅需稀疏激活向量的调节操作）实现了显著的偏差缓解，在偏差得分变化与VLA性能变化的权衡指标上表现优异。

**交叉公平性**。Table 8展示了交叉公平性（Intersectional Fairness）的MaxSkew结果，验证了DEBIASLENS在同时处理多个社会属性（如性别×年龄、性别×种族）交叉场景下的有效性。

### 4.6 合成数据验证

Figure 9展示了新生成的SBBench合成数据集。通过合成图像，研究者系统性地观察了不同SAE训练数据集和社会神经元探测数据集对偏差缓解效果的影响。结果表明，使用通用图像数据集（如ImgNette）训练SAE虽然通用性能保持较好，但偏差缓解效果有限；而使用与偏差属性相关的专用数据集则能实现更强的去偏效果。

---

**需要人工验证的点**：
- Table 1中CLIP ViT-B/16†的具体基线数值和DEBIASLENS (I)（SAE附加于图像编码器）的完整结果需对照原文确认。
- Figure 4中40–50%的具体数值对应InternVL2的哪个评测设置（VLAGenderBias或SBBench）需对照原文核实。
- Table 3、Table 6、Table 7、Table 8的具体数值因分析JSON中未提供完整数据，建议直接查阅原文。

![[assets/figures/papers/paper_list_l760_https_arxiv_org_abs_2602_24014/figures/010_Table_3.jpg]]
*Table 3: SBBench (categories: age and gender) accuracy of DEBIASLENS applied to LVLM. The best performance is achieved when SAE is trained and gender neurons are selected using the FairFace datasets, measured using a rule-based and model-based evaluation*

![[assets/figures/papers/paper_list_l760_https_arxiv_org_abs_2602_24014/figures/018_Table_6.jpg]]
*Table 6: Bias Score Results on Non-Overlapping Datasets*

![[assets/figures/papers/paper_list_l760_https_arxiv_org_abs_2602_24014/figures/020_Table_7.jpg]]
*Table 7: Computational Cost Results. The trade-off score (↑ the better) is proportional to ∆BiasScore − ∆VLAPerf*

![[assets/figures/papers/paper_list_l760_https_arxiv_org_abs_2602_24014/figures/004_Table_1.jpg]]
*Table 1: Max Skew@1000 (scaled by 100) results on Fair-Face dataset using diverse prompts for gender bias evaluation. Note † represents reproduced results (T and I indicate SAE attached to text and image encoder). Our DEBIASLENS attains comparable performance with SoTA VLM debiasing methods without using labels during training (but required during probing), with interpretable inference components*

## 定位与知识库关联

### 与现有去偏方法的谱系关系

DEBIASLENS 处于**基于特征干预的 VLM 去偏**这一分支，其核心操作对象是模型内部表征而非外部数据或提示。与现有工作的关键差异在于**可解释性维度**——它不依赖社会属性标签训练 SAE，而是利用稀疏自编码器从无标注的面部图像/文本数据中自动涌现出对社会属性敏感的神经元，从而实现“透明解耦、定向调控”。

在 CLIP 检索去偏的对比基线中（Table 1），DEBIASLENS (T) 在形容词提示下的 Max Skew@1000 降至 **7.1**，显著优于 CLIP ViT-B/16† 的 **21.9**（-67.6%）。这一结果使其与以下方法形成参照：

- **FairCLIP**（Rosenberg et al., 2023）：通过优化 CLIP 的公平性损失直接微调模型，属于训练时干预。DEBIASLENS 的优势在于无需重新训练骨干网络，且提供神经元级别的归因。
- **MPGD**（He et al., CVPR 2023）：通过多模态提示梯度解耦进行去偏，属于提示层面的干预。DEBIASLENS 与之互补——前者在输入空间操作，后者在表征空间操作。
- **DebiasCLIP**（Berg et al., 2022）：采用对抗训练去除文本编码器中的偏见方向，属于对抗式方法。DEBIASLENS 避免了对抗训练的不稳定性，且可同时作用于图像和文本编码器。

对于 LVLM 的性别偏见评估（Figure 4），DEBIASLENS-Intern（α: 0.6）在 InternVL2 上实现了 **40–50%** 的性别回答差异下降，在偏见缓解与通用性能的权衡曲线上优于现有方法。这表明该方法对不同的 VLM 架构（CLIP 双塔 vs. LVLM 自回归）具有良好的泛化性。

### 关键设计选择与消融证据

DEBIASLENS 的因果杠杆集中于三个设计选择，均有消融实验支撑：

1. **SAE 扩展因子**：设为 8，在神经元粒度和计算开销之间取得平衡。
2. **神经元选择策略**：仅去活 top-1 社会神经元即可达到与去活所有有效神经元相当的性能（Section 4.3），说明偏见信息高度集中于单个主导神经元。
3. **神经元特异性**：Table 2 显示，调节性别神经元仅缓解性别偏见（Max Skew 10.6 → 9.2），对年龄偏见影响微弱；反之亦然。Figure 5 在文本编码器上验证了同样的特异性模式。这意味着 DEBIASLENS 支持**属性级别的细粒度调控**，而非全局式的无差别去偏。

### 适用边界与局限

基于已验证的分析和实验设置，该方法的适用边界如下：

- **模态覆盖**：已验证于 CLIP（ViT-B/16）和 InternVL2，对纯文本或纯图像的编码器结构未提供直接证据。
- **偏见类型**：主要验证于性别、种族、年龄三类社会属性。对于交叉性偏见（如“黑人女性”）的神经元可分离性未做专门分析。
- **数据依赖**：SAE 训练和神经元探测依赖 FairFace 和 Cocogendertxt 数据集。这些数据集的属性覆盖面和标注质量直接影响神经元识别的完备性。
- **性能权衡**：Table 4 明确揭示了去偏强度与通用性能之间的 trade-off——随着干预权重 α 增大，偏见指标下降但检索/生成质量同步衰减。这是特征干预类方法的共性瓶颈，DEBIASLENS 未提出根本性解决方案。

### 开放问题

1. **跨属性交叉神经元的处理**：当某个神经元同时对多个社会属性敏感时，当前“按组选最高激活”的策略可能产生冲突。如何建模和解耦交叉性偏见神经元是未解决的问题。
2. **神经元选择的自动化**：阈值 τ（0.9）和权重 α（0.6）目前通过网格搜索确定，对不同模型和偏见类型可能需要重新调参。自适应选择机制值得探索。
3. **SAE 训练的无监督本质**：虽然避免了社会属性标签，但 SAE 涌现出的神经元是否完整覆盖所有偏见维度缺乏理论保证。可能存在“沉默偏见”——即未被 SAE 捕获但实际影响模型输出的偏见模式。
4. **长尾属性的覆盖**：当前验证集中于高频社会属性（性别、种族、年龄），对于宗教、残疾等长尾属性的神经元可识别性和去偏效果尚不明确，需要手动验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/Interpretable_Debiasing_of_Vision_Language_Models_for_Social_Fairness.pdf]]
