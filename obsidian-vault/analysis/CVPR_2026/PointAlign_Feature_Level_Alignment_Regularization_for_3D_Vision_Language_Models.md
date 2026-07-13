---
title: "PointAlign: Feature-Level Alignment Regularization for 3D Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/PointAlign_Feature_Level_Alignment_Regularization_for_3D_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/yharoldsu0627/PointAlign"
aliases:
- PointAlign
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
core_operator: 在LLM的中间层引入一个对齐正则化项，强制点云token与冻结的Q-Former输出保持一致性，从而显式保留几何结构与语义信息。
primary_logic: Q-Former在预训练阶段已经学习了点云与文本之间的映射，其输出同时包含几何与语义信息，且比深层LLM表示更完整，因此可作为高质量的内部监督目标；通过一个轻量级投影器将LLM中间层点云token映射回该空间并用余弦相似度约束，即可有效防止几何信息衰减。
claims:
- 仅用语言建模损失训练时，深层点云token的特征质量显著下降（KNN准确率降低）。
- 对齐后，LLM中间层的点云token保留更高几何语义辨别力，KNN准确率明显提升（K=1时峰值85.43% vs 基线83.40%）。
- 引入对齐正则化后，在分类任务上平均准确率提升2.08个百分点，尤其是在开放词汇Objaverse分类任务上提升7.50个百分点。
- 在3D物体描述任务上，Qwen2-72B-Instruct评估得分提升4.88个百分点。
---

# PointAlign: Feature-Level Alignment Regularization for 3D Vision-Language Models

> [!tip] 核心洞察
> Q-Former在预训练阶段已经学习了点云与文本之间的映射，其输出同时包含几何与语义信息，且比深层LLM表示更完整，因此可作为高质量的内部监督目标；通过一个轻量级投影器将LLM中间层点云token映射回该空间并用余弦相似度约束，即可有效防止几何信息衰减。

| 字段 | 内容 |
|------|------|
| 中文题名 | PointAlign：面向三维视觉语言模型的特征级对齐正则化 |
| 英文题名 | PointAlign: Feature-Level Alignment Regularization for 3D Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.00412) · [Code](https://github.com/yharoldsu0627/PointAlign) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer |
| Method | PointAlign |
| Dataset | ModelNet40 + Objaverse, Objaverse 分类, Scan2Cap |

> [!tip] 效果简介
> - ModelNet40 + Objaverse (平均) 上，生成式分类准确率 (%) 66.08 vs 64.00 (MiniGPT-3D) (+2.08 pp)。
> - Objaverse 分类 (指令提示) 上，准确率 (%) 72.50 vs 65.00 (MiniGPT-3D) (+7.50 pp)。
> - Objaverse 描述 (Qwen2-72B-Instruct) 上，评估得分 53.05 vs 48.17 (MiniGPT-3D) (+4.88 pp)。

## 概要

**问题瓶颈**：当前3D视觉语言模型（如MiniGPT-3D、PointLLM）在训练时仅依赖下一token预测的交叉熵损失，缺乏对中间点云特征的直接监督。这导致LLM深层中点云token的细粒度几何语义信息逐渐退化——实验表明，基线模型深层token的KNN分类准确率显著下降，模型对3D结构的辨别力随层深增加而衰减。

**核心洞察**：Q-Former在预训练阶段已学习到点云与文本之间的映射，其输出同时包含几何结构与语义信息，且比深层LLM表示更完整，因此可作为高质量的内部监督目标。通过一个轻量级投影器将LLM中间层点云token映射回该空间并用余弦相似度约束，即可有效防止几何信息衰减。

**方法定位**：PointAlign是一种训练阶段的特征级对齐正则化方法，而非架构修改。它在第二阶段微调时冻结点云编码器、MLP投影、Q-Former和模态投影器，仅训练LLM的LoRA层和一个三层对齐投影器（约8.39M参数），推理时该投影器完全移除，不引入任何额外推理开销。

**方法谱系与知识库定位**：PointAlign建立在**MiniGPT-3D**（Tang et al., MM 2024）的高效对齐框架之上，继承了其两阶段训练范式（预训练+指令微调）。与**PointLLM-7B**（Xu et al., ECCV 2024）的全量微调策略不同，PointAlign保持参数高效。与**Point-Bind LLM**（Guo et al., arXiv 2023）和**GPT4Point**（Qi et al., CVPR 2024）等早期3D-LLM方法相比，PointAlign首次在LLM中间层引入显式的点云特征对齐正则化。该方法的思想可追溯到2D视觉语言模型中的特征一致性约束，但针对3D点云模态进行了专门设计。

**主要结果**：在生成式3D物体分类任务上，PointAlign平均准确率达66.08%，较MiniGPT-3D基线提升2.08个百分点，其中开放词汇Objaverse分类提升高达7.50个百分点。在3D物体描述任务上，Qwen2-72B-Instruct评估得分提升4.88个百分点。该方法对不同LLM骨架（Phi-2、Phi-3）和架构（含无Q-Former的3D-LLaVA）均表现出通用性，在场景级3D密集描述任务上也取得一致提升。

### 3D视觉语言模型的兴起与架构范式

三维视觉语言模型（3D-VLM）旨在将点云等三维数据的感知能力与大语言模型（LLM）的语义理解与生成能力相结合，实现对三维世界的多模态理解与交互。当前主流的3D-VLM普遍采用“点云编码器 → 连接器 → LLM”的级联架构。其中，点云编码器（如PointBERT）负责从原始点云中提取几何特征；连接器（如Q-Former或MLP投影）将点云特征映射至LLM的文本嵌入空间；LLM则接收对齐后的视觉token与文本token，通过自回归语言建模完成分类、描述生成、视觉问答等下游任务。

在这一范式下，训练过程通常分为两个阶段：第一阶段对点云编码器和连接器进行预训练，使其学会将点云信息映射为LLM可理解的表示；第二阶段则对LLM进行指令微调，训练目标几乎完全依赖于下一token预测的交叉熵损失。**PointAlign**延续了这一两阶段训练框架，其第一阶段完全遵循**MiniGPT-3D**（Tang et al., MM 2024）的三种预训练策略，第二阶段则冻结点云编码器、MLP投影、Q-Former和模态投影器，仅训练LLM的LoRA层。

### 核心瓶颈：深层点云特征的几何语义退化

尽管上述范式在多项3D理解任务上取得了显著进展，但PointAlign揭示了一个被忽视的关键问题：**仅依赖下一token预测损失进行训练，缺乏对中间点云特征的直接监督，导致LLM深层表示中的细粒度几何语义信息逐渐退化。**

具体而言，Q-Former在预训练阶段已经学习了点云与文本之间的高质量映射，其输出同时包含几何结构与语义信息，且比深层LLM表示更为完整。然而，当这些点云token进入LLM后，在逐层变换过程中，由于语言建模损失仅约束最终的文本输出，中间层点云token的表示质量并未受到任何显式约束。实验证据表明（Figure 3），在基线模型中，随着层数加深，点云token的KNN分类准确率显著下降——K=1时从浅层的较高水平降至深层的83.40%，这直接印证了几何辨别力的丧失。

这一退化现象在数据稀缺场景下尤为严重。3D-文本配对数据的规模远小于2D图文数据，有限的监督信号难以自发地维持中间表示中的细粒度几何信息。因此，如何在不增加推理开销的前提下，显式地保护LLM中间层点云token的几何语义质量，成为提升3D-VLM性能的关键突破口。

### 现有方法的局限与本文动机

现有3D-VLM方法在应对上述问题时存在明显不足：

- **全量微调方法**（如**PointLLM-7B**，Xu et al., ECCV 2024）虽然释放了LLM的全部参数，但训练成本高昂，且仍未对中间层特征施加显式约束，几何退化问题依然存在。
- **高效对齐方法**（如**MiniGPT-3D**）通过LoRA等参数高效微调策略降低了训练开销，但其训练目标与全量微调方法一样，完全依赖输出端的语言建模损失，中间层特征质量同样缺乏保障。
- **2D方法**（如**InstructBLIP-7B**，Dai et al., NeurIPS 2023；**LLaVA-7B**，Liu et al., CVPR 2024）虽在多模态理解上表现优异，但其架构设计未针对3D点云的几何特性进行优化，无法直接解决点云token的退化问题。

上述分析揭示了一个明确的研究缺口：**如何在LLM的中间层引入轻量级监督机制，以保留点云token中的几何语义信息，同时不增加推理阶段的额外计算开销？** PointAlign正是针对这一缺口，提出了一种特征级对齐正则化方法——在LLM的特定中间层提取点云token，通过一个轻量级对齐投影器将其映射回Q-Former的特征空间，并利用余弦相似度损失强制保持与Q-Former输出的一致性。该对齐投影器仅在训练阶段使用，推理时完全移除，因此不引入任何额外的推理延迟或参数量。

### 方法定位与预期贡献

PointAlign的核心动机可概括为：**利用Q-Former输出作为高质量的内部监督目标，通过显式的中间层对齐正则化，防止点云几何语义信息在LLM逐层变换中衰减。** 这一设计根植于一个关键洞察——Q-Former在预训练阶段已经习得了点云与文本之间的鲁棒映射，其输出天然具备几何与语义的双重完整性，因此是比深层LLM表示更可靠的监督信号来源。

基于上述动机，PointAlign预期在以下方面取得突破：在生成式3D物体分类任务上实现显著提升，尤其是在开放词汇场景下弥补现有方法的不足；在3D物体描述生成任务上产出更精准、几何感知更强的文本输出；同时保持方法的架构通用性，使其可适配不同的LLM骨架和连接器设计。

## 核心方法与创新机理

PointAlign 的核心创新在于**在 LLM 的中间层引入特征级对齐正则化**，以解决 3D 视觉语言模型训练中细粒度几何语义信息逐渐退化的瓶颈问题。其关键洞察是：Q-Former 在预训练阶段已经学习了点云与文本之间的映射，其输出同时包含几何与语义信息，且比深层 LLM 表示更完整，因此可作为高质量的内部监督目标。

### 问题诊断：中间特征的几何退化

现有 3D 视觉语言模型（如 MiniGPT-3D）在第二阶段训练中仅依赖下一 token 预测的交叉熵损失 $\mathcal{L}_{ntp}$，缺乏对中间点云特征的直接监督。实验证据表明（Figure 3），随着 LLM 层数加深，点云 token 的 KNN 分类准确率显著下降——基线模型在深层时几何辨别能力明显衰减。这意味着仅靠语言建模损失无法有效保留点云编码器提取的细粒度 3D 结构信息。

### 方法骨架：对齐正则化机制

PointAlign 在 MiniGPT-3D 的训练框架上做出以下关键改动（changed slots）：

| 改动槽位 | 基线方法 (MiniGPT-3D) | PointAlign |
|---------|----------------------|------------|
| 训练目标 | 仅 $\mathcal{L}_{ntp}$ | $\mathcal{L}_{ntp} + \lambda \mathcal{L}_{align}$ |
| 中间层监督 | 无 | 在 LLM 第 $\ell$ 层提取点云 token，通过对齐投影器映射至 Q-Former 特征空间并计算余弦相似度损失 |
| 对齐投影器 | 无 | 三层线性层+SiLU 激活，仅训练阶段使用，推理时丢弃 |
| 第二阶段可训练组件 | 全量或部分微调 | 冻结点云编码器、MLP 投影、Q-Former 和模态投影器；仅训练 LLM 的 LoRA 层和对齐投影器 |

具体而言，PointAlign 引入一个轻量级的**对齐投影器**（Alignment Projector），将 LLM 第 $\ell$ 层的点云 token $\mathbf{T}_{pc}^{(\ell)}$ 映射回 Q-Former 的特征空间：

$$\mathbf{h}^{(1)} = \mathbf{W}_1 \cdot \mathbf{T}_{pc}^{(\ell)} + \mathbf{b}_1, \quad \mathbf{h}^{(2)} = \mathbf{W}_2 \cdot \mathrm{SiLU}(\mathbf{h}^{(1)}) + \mathbf{b}_2, \quad \tilde{\mathbf{Q}} = \mathbf{W}_3 \cdot \mathrm{SiLU}(\mathbf{h}^{(2)}) + \mathbf{b}_3$$

随后，通过余弦相似度损失约束映射后的表示 $\tilde{\mathbf{Q}}$ 与冻结的 Q-Former 输出 $\overline{\mathbf{Q}}$ 保持一致：

$$\mathcal{L}_{align} = -\frac{1}{o}\sum_{i=1}^o \frac{\tilde{\mathbf{Q}}_i^\top \overline{\mathbf{Q}}_i}{\|\tilde{\mathbf{Q}}_i\|_2 \|\overline{\mathbf{Q}}_i\|_2}$$

总训练损失为：

$$\mathcal{L}_{total} = \mathcal{L}_{ntp} + \lambda \mathcal{L}_{align}$$

### 设计选择的因果逻辑

**为什么选择 Q-Former 输出作为对齐目标？** 消融实验（Table 8）表明，选择 Q-Former 输出（含几何与语义信息）优于点云编码器输出或最终投影层。Q-Former 通过可学习查询向量与点云特征的交叉注意力，已经聚合了丰富的多模态信息，且其表示在预训练后被冻结，提供了稳定的监督信号。

**为什么使用余弦相似度而非 L1/L2？** 消融实验（Table 4）显示，余弦相似度损失（平均准确率 66.08%）优于 L1 损失（65.72%）和 L2 损失（65.57%）。余弦相似度鼓励方向一致性而非幅度一致性，更适合高维特征空间中的表示对齐。

**为什么在第 16 层对齐？** 层选择消融（Table 5）表明，在第 16 层进行对齐效果最佳（平均 66.08%），过浅（如第 4 层 65.35%）或过深（如第 28 层 65.38%）均导致性能下降。中间层恰好处于语义抽象与几何信息保留的平衡点。

**为什么 $\lambda=0.1$？** 权重消融（Table 6）显示，$\lambda=0.1$ 时取得最优平均准确率 66.08%，增大 $\lambda$ 会过度约束表示学习，干扰语言建模目标。

### 关键特性：零推理开销

对齐投影器仅包含 8.39M 参数，且**仅在训练阶段使用，推理时完全移除**。这意味着 PointAlign 在不增加任何推理延迟或内存开销的前提下，显著提升了模型性能。这一设计使其成为即插即用的正则化手段，可灵活应用于不同的 3D 视觉语言架构（如无 Q-Former 的 3D-LLaVA，Table 9）和不同的 LLM 骨架（如 Phi-2、Phi-3，Table 10）。

PointAlign 在现有 3D 视觉语言模型的基础上引入了一个轻量级的特征级对齐正则化机制，其核心思想是：大语言模型（LLM）在逐层处理点云 token 时，仅受下一 token 预测损失驱动，缺乏对中间表示的显式几何语义监督，导致细粒度 3D 信息在深层逐渐衰减。为解决这一问题，PointAlign 在 LLM 的某一中间层提取点云 token，通过对齐投影器将其映射回冻结的 Q-Former 特征空间，并以余弦相似度损失强制该中间表示与 Q-Former 输出保持一致，从而保留几何结构与语义信息。

### 两阶段训练流程

PointAlign 的训练分为两个阶段，整体架构如 Figure 1 所示：

![[assets/figures/papers/paper_list_l2407_https_arxiv_org_abs_2603_00412/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our method. Stage 1 adopts the three training recipes of MiniGPT-3D for pre-training. Stage 2 freezes the point cloud encoder, MLP, Q-Former, and modality projector, and only trains the LoRA layers of the LLM and the alignment projector. The alignment projector aligns the latent representations of point cloud tokens in the LLM with the Q-Former output through cosine similarity loss. Flame icons indicate trainable modules, and snowflakes indicate frozen modules*

**第一阶段：预训练。** 完全沿用 MiniGPT-3D（Tang et al., MM 2024）的三阶段预训练策略，包括点云-文本对齐、指令微调等步骤，得到一个具备基础 3D 理解能力的模型。此阶段不引入任何额外模块。

**第二阶段：对齐正则化微调。** 在第一阶段预训练模型的基础上，冻结点云编码器（PointBERT）、MLP 投影层、Q-Former 和模态投影器，仅训练 LLM 的 LoRA 层和新引入的对齐投影器。对齐投影器在训练阶段使用，推理时完全移除，不引入任何额外推理开销。

### 模块组成与数据流

PointAlign 的完整 pipeline 包含以下核心模块：

1. **点云编码器（PointBERT）**：接收输入点云 $\mathbf{P}$，提取初始 3D 特征 $f_{pc}(\mathbf{P}) \in \mathbb{R}^{m \times D}$。第二阶段冻结。

2. **MLP 投影层**：将点云特征投影至 Q-Former 的语义空间，为后续的跨模态交互做准备。第二阶段冻结。

3. **Q-Former**：通过一组可学习的查询向量 $\mathbf{Q}$ 对投影后的点云特征进行交叉注意力编码，生成点云 token $\overline{\mathbf{Q}} = f_{QF}(f_{MLP}(f_{pc}(\mathbf{P})), \mathbf{Q}) \in \mathbb{R}^{o \times D_1}$。Q-Former 在预训练阶段已学习到点云与文本之间的映射，其输出同时包含几何与语义信息，因此被选作对齐目标。第二阶段冻结。

4. **模态投影器**：将 Q-Former 输出的点云 token 映射至 LLM 的输入嵌入空间。第二阶段冻结。

5. **LLM（带 LoRA）**：大语言模型（默认使用 Phi-2），接收点云 token 和文本 token 的拼接序列，通过自回归方式生成文本。仅 LoRA 参数可训练。

6. **对齐投影器（3 层 MLP）**：从 LLM 第 $\ell$ 层提取点云 token $\mathbf{T}_{pc}^{(\ell)}$，通过三层线性变换和 SiLU 激活函数映射至 Q-Former 特征空间：

   $$\mathbf{h}^{(1)} = \mathbf{W}_1 \cdot \mathbf{T}_{pc}^{(\ell)} + \mathbf{b}_1, \quad \mathbf{h}^{(2)} = \mathbf{W}_2 \cdot \mathrm{SiLU}(\mathbf{h}^{(1)}) + \mathbf{b}_2, \quad \tilde{\mathbf{Q}} = \mathbf{W}_3 \cdot \mathrm{SiLU}(\mathbf{h}^{(2)}) + \mathbf{b}_3$$

   该投影器仅 8.39M 参数，仅在训练阶段使用，推理时移除。

### 训练目标

PointAlign 的总损失函数由两部分组成：

$$\mathcal{L}_{total} = \mathcal{L}_{ntp} + \lambda \mathcal{L}_{align}$$

其中 $\mathcal{L}_{ntp}$ 为标准的下一 token 预测交叉熵损失，$\mathcal{L}_{align}$ 为对齐正则化项，定义为映射后的点云 token $\tilde{\mathbf{Q}}$ 与冻结的 Q-Former 输出 $\overline{\mathbf{Q}}$ 之间的余弦相似度损失：

$$\mathcal{L}_{align} = -\frac{1}{o}\sum_{i=1}^o \frac{\tilde{\mathbf{Q}}_i^\top \overline{\mathbf{Q}}_i}{\|\tilde{\mathbf{Q}}_i\|_2 \|\overline{\mathbf{Q}}_i\|_2}$$

该损失鼓励两个向量方向一致而非幅度一致，使 LLM 中间层的点云表示保持与 Q-Former 输出相同的几何语义辨别力。超参数 $\lambda$ 控制对齐损失的权重，默认取 0.1。

### 关键设计选择

- **对齐目标选择 Q-Former 输出**：相比于点云编码器输出或深层 LLM 表示，Q-Former 输出在预训练阶段已融合了视觉与语言信息，且比深层 LLM 表示保留了更完整的几何细节。消融实验（Table 8）证实了这一选择的优越性。

- **对齐层选择中间层（第 16 层）**：实验表明，在 Phi-2 的第 16 层施加对齐效果最佳（平均分类准确率 66.08%），过浅或过深的层均导致性能下降（Table 5）。这一现象与 Figure 3 的特征质量分析一致：未对齐时，深层点云 token 的 KNN 分类准确率显著退化；对齐后，中间层的几何语义辨别力得到有效保持。

- **余弦相似度损失优于 L1/L2**：消融实验（Table 4）表明，余弦相似度损失的平均准确率（66.08%）高于 L1 损失（65.72%）和 L2 损失（65.57%），说明方向一致性约束比逐元素距离约束更适合特征空间对齐。

- **推理时零开销**：对齐投影器仅在训练阶段参与梯度计算，推理时被完全移除，模型结构与原始 MiniGPT-3D 完全一致，不增加任何推理延迟或显存占用。

### 整体架构与训练范式

PointAlign采用两阶段训练框架（Figure 1）。第一阶段完全遵循MiniGPT-3D的预训练方案，完成点云编码器、Q-Former、模态投影器及LLM的初始对齐。第二阶段冻结点云编码器、MLP投影层、Q-Former和模态投影器，仅训练LLM的LoRA层和新引入的对齐投影器（Alignment Projector）。推理时对齐投影器被完全移除，不引入额外计算开销。

### 对齐投影器

对齐投影器是PointAlign的核心新增模块，由一个三层MLP构成，负责将LLM中间层（第ℓ层）的点云token映射回Q-Former的特征空间。其前向计算过程为：

$$
\mathbf{h}^{(1)} = \mathbf{W}_1 \cdot \mathbf{T}_{pc}^{(\ell)} + \mathbf{b}_1
$$
$$
\mathbf{h}^{(2)} = \mathbf{W}_2 \cdot \mathrm{SiLU}(\mathbf{h}^{(1)}) + \mathbf{b}_2
$$
$$
\tilde{\mathbf{Q}} = \mathbf{W}_3 \cdot \mathrm{SiLU}(\mathbf{h}^{(2)}) + \mathbf{b}_3
$$

其中 $\mathbf{T}_{pc}^{(\ell)} \in \mathbb{R}^{o \times D_2}$ 为LLM第ℓ层输出的点云token序列（共o个token，维度为 $D_2$），$\tilde{\mathbf{Q}} \in \mathbb{R}^{o \times D_1}$ 为映射到Q-Former特征空间的表示。三层线性变换配合两层SiLU激活函数，实现特征维度的逐步压缩与非线性变换。该投影器仅引入8.39M可训练参数，且在推理阶段被丢弃。

### 对齐损失函数

对齐损失采用余弦相似度，强制映射后的点云token $\tilde{\mathbf{Q}}$ 与冻结的Q-Former输出 $\overline{\mathbf{Q}}$ 保持方向一致：

$$
\mathcal{L}_{align} = -\frac{1}{o}\sum_{i=1}^o \frac{\tilde{\mathbf{Q}}_i^\top \overline{\mathbf{Q}}_i}{\|\tilde{\mathbf{Q}}_i\|_2 \|\overline{\mathbf{Q}}_i\|_2}
$$

选择余弦相似度而非L1或L2距离的原因在于：对齐的核心目标是保持特征方向的一致性，而非精确的幅度匹配。消融实验（Table 4）证实，余弦相似度损失的平均分类准确率达66.08%，优于L1损失（65.72%）和L2损失（65.57%）。

### 对齐目标选择

对齐目标选定为Q-Former的输出 $\overline{\mathbf{Q}}$——即Q-Former之后经过Normalization和LoRA层处理的特征。这一选择的依据是：Q-Former在预训练阶段已学习到点云与文本之间的跨模态映射，其输出同时蕴含几何结构与语义信息，且比深层LLM的中间表示更为完整。消融实验（Table 8）表明，以Q-Former输出为对齐目标优于以点云编码器输出或最终投影层为目标，验证了该选择的有效性。

### 总训练损失

第二阶段的总训练目标为语言建模损失与对齐正则化项的加权组合：

$$
\mathcal{L}_{total} = \mathcal{L}_{ntp} + \lambda \mathcal{L}_{align}
$$

其中 $\mathcal{L}_{ntp}$ 为标准的下一token预测交叉熵损失，$\lambda$ 为平衡系数。消融实验（Table 6）确定 $\lambda=0.1$ 时取得最优平均准确率66.08%，过大的 $\lambda$ 会过度约束LLM的表示学习能力，导致性能下降。

### 对齐层位置

对齐操作施加于LLM的单一中间层。以Phi-2为骨干网络时，选定第16层（共32层）进行对齐。层位置消融实验（Table 5）揭示了中间层对齐的优越性：过浅的层（如第8层）尚未充分整合多模态信息，过深的层（如第24层）已发生显著的几何信息衰减，中间层恰好处于信息保留与语义融合的平衡点。

### 补充图表

## 实验与关键发现

### 核心瓶颈验证：中间特征退化

PointAlign 的设计动机源于一个关键观察：仅用下一 token 预测损失（$\mathcal{L}_{ntp}$）训练 3D 视觉语言模型时，点云 token 在 LLM 深层会逐渐丧失细粒度几何语义信息。Figure 3 通过 KNN 分类准确率量化了这一退化——基线模型深层点云 token 的特征辨别力显著下降。引入对齐正则化后，LLM 中间层的点云 token 保留更高的几何语义辨别力，K=1 时峰值准确率达 85.43%，相比基线 83.40% 有明显提升。这一证据直接支撑了论文的核心因果机制：通过强制中间层点云 token 与冻结的 Q-Former 输出保持一致，可有效阻止几何信息在深层变换中的衰减。

### 生成式 3D 物体分类

Table 1 展示了在 ModelNet40 和 Objaverse 两个数据集上的生成式分类结果。PointAlign 以平均准确率 66.08% 显著优于所有对比方法，相较主要基线 **MiniGPT-3D**（Tang et al., MM 2024）的 64.00% 提升 2.08 个百分点。在更具挑战性的开放词汇 Objaverse 分类任务上，指令提示格式下 PointAlign 达到 72.50%，比 MiniGPT-3D 的 65.00% 提升 7.50 个百分点，验证了对齐正则化在保留细粒度类别语义方面的有效性。值得注意的是，PointAlign 在仅引入 8.39M 训练参数（推理时完全移除）的前提下取得这些增益，无额外推理开销。

![[assets/figures/papers/paper_list_l2407_https_arxiv_org_abs_2603_00412/figures/002_Table_1.jpg]]
*Table 1: Performance evaluation of generative 3D object classification on ModelNet40 test set and Objaverse dataset. Classification accuracy (%) is evaluated using two prompt formats: Instruction-based (I) “What is this?” and Completion-based (C) “This is an object*

### 3D 物体描述

Table 2 报告了 Objaverse 数据集上的描述生成性能。PointAlign 在 Qwen2-72B-Instruct 语义评估得分上达到 53.05，相比 MiniGPT-3D 的 48.17 提升 4.88 个百分点，在传统指标（BLEU-4、METEOR、ROUGE-L、CIDEr）上也全面领先。Table 3 的定性对比进一步显示，PointAlign 生成的描述在几何细节和语义准确性上均优于基线，例如对复杂形状物体的空间关系描述更为精确。

![[assets/figures/papers/paper_list_l2407_https_arxiv_org_abs_2603_00412/figures/003_Table_2.jpg]]
*Table 2: Performance evaluation of 3D object captioning on the Objaverse dataset. Evaluation metrics include Qwen2 evaluation and traditional metrics. Bold and underlined values represent the best and second-best performances, respectively*

![[assets/figures/papers/paper_list_l2407_https_arxiv_org_abs_2603_00412/figures/005_Table_3.jpg]]
*Table 3: Qualitative comparison of model outputs for classification and captioning on the Objaverse datasets*

### 消融实验

**损失函数选择**（Table 4）：余弦相似度损失（平均 66.08%）优于 L1 损失（65.72%）和 L2 损失（65.57%）。余弦相似度关注方向一致性而非幅度匹配，更适合高维特征空间中的语义对齐。

**对齐目标层**（Table 5）：在 Phi-2 的第 16 层施加对齐取得最优平均准确率 66.08%。过浅的层（如第 8 层）特征尚未充分融合跨模态信息，过深的层（如第 24 层）几何信息已严重退化，对齐效果均下降。这一结果与 Figure 3 的特征退化曲线相互印证。

**损失权重 λ**（Table 6）：λ=0.1 时取得最优平均准确率 66.08%。增大 λ 会导致性能下降，表明过强的对齐约束会干扰语言建模目标，需要在几何保持和文本生成能力之间取得平衡。

**对齐投影器深度**（Table 7）：三层线性层（带 SiLU 激活）优于单层或两层，验证了适度的非线性映射能力对于跨空间特征对齐的必要性。

**对齐目标选择**（Table 8）：选择 Q-Former 输出作为对齐目标（平均 66.08%）优于点云编码器输出（64.92%）或最终投影层（65.31%）。这验证了核心洞察：Q-Former 输出同时包含几何与语义信息，且比深层 LLM 表示更完整，是高质量的内部监督信号。

### 通用性与数据效率

Table 9 将对齐正则化应用于无 Q-Former 架构的 **3D-LLaVA**，在 Scan2Cap 场景级稠密描述任务上 CIDEr@0.5 从 76.1 提升至 78.8（+2.7），证明方法不依赖特定架构。Table 10 在 Phi-3 骨干上验证了中层对齐的通用性。Figure 4 的数据效率实验显示，即使在仅 10% 训练数据下，对齐模型仍保持对基线的稳定优势，表明正则化有效利用了有限 3D 数据的内部监督信号。

![[assets/figures/papers/paper_list_l2407_https_arxiv_org_abs_2603_00412/figures/013_Table_9.jpg]]
*Table 9: Scene-level 3D dense captioning on Scan2Cap [2]. Our alignment regularization is applied to 3D-LLaVA [5], which does not use Q-Former. (* denotes reproduced results.)*

![[assets/figures/papers/paper_list_l2407_https_arxiv_org_abs_2603_00412/figures/010_Figure_4.jpg]]
*Figure 4: Impact of training data fraction on 3D object captioning performance. We evaluate baseline and aligned models using 10%, 30%, 50%, 70%, and 100% of training data on Objaverse dataset*

### 失败模式与局限

尽管 PointAlign 在多个基准上表现优异，仍存在以下局限：对齐质量受限于 Q-Former 预训练阶段对精细几何的捕获能力，若 Q-Former 本身未能充分编码细粒度几何信息，对齐效果的上限将受制约。此外，仅在单一固定层施加对齐损失可能无法最优地监督整个特征变换过程，多层联合对齐策略尚待探索。采用的静态余弦相似度损失未能适应性地关注不同 token 或维度的重要性，可能遗漏更优的分布对齐形式（如对比学习或可学习距离度量）。

### 补充图表

![[assets/figures/papers/paper_list_l2407_https_arxiv_org_abs_2603_00412/figures/007_Table_4.jpg]]
*Table 4: Ablation study on loss functions. We evaluate the impact of different loss functions at 16-th layer on classification accuracy*

![[assets/figures/papers/paper_list_l2407_https_arxiv_org_abs_2603_00412/figures/008_Table_5.jpg]]
*Table 5: Ablation study on target layers. We evaluate the impact of different layer indices on classification accuracy (%)*

![[assets/figures/papers/paper_list_l2407_https_arxiv_org_abs_2603_00412/figures/006_Table_6.jpg]]
*Table 6: Ablation study on the weight of the alignment loss λ. We evaluate the impact of different λ at 16-th layer*

![[assets/figures/papers/paper_list_l2407_https_arxiv_org_abs_2603_00412/figures/011_Table_7.jpg]]
*Table 7: Ablation study on the number of linear layers in the alignment projector. We evaluate the impact at layer 16 on classification accuracy using cosine similarity loss with λ = 0.1*

![[assets/figures/papers/paper_list_l2407_https_arxiv_org_abs_2603_00412/figures/012_Table_8.jpg]]
*Table 8: Ablation study on the alignment target. We evaluate the impact of different alignment targets at layer 16 on classification accuracy (%) using cosine similarity loss with λ = 0.1*

## 定位与知识库关联

### 与现有3D视觉语言模型的继承与改进关系

PointAlign 直接构建在 **MiniGPT-3D**（Tang et al., MM 2024）的预训练框架之上，继承了其三阶段训练范式：点云编码器（PointBERT）通过 MLP 投影层接入 Q-Former，再经模态投影器馈入 LLM。在此基础之上，PointAlign 的核心创新在于引入了一个**特征级对齐正则化机制**——在第二阶段微调时，冻结点云编码器、MLP 投影、Q-Former 和模态投影器，仅训练 LLM 的 LoRA 层和一个轻量级对齐投影器，通过余弦相似度损失强制 LLM 中间层的点云 token 与冻结的 Q-Former 输出保持一致。

这一设计填补了现有 3D 视觉语言模型训练中的一个关键空白：**仅依赖下一 token 预测损失（$\mathcal{L}_{ntp}$）无法保证中间表示中细粒度几何语义信息的保留**。与 **PointLLM-7B**（Xu et al., ECCV 2024）的全量微调策略相比，PointAlign 采用参数高效的方式（仅引入 8.39M 可训练参数，推理时完全移除）实现了更优的性能，表明问题不在于模型容量，而在于训练信号的充分性。与 **InstructBLIP-7B**（Dai et al., NeurIPS 2023）和 **LLaVA-7B**（Liu et al., CVPR 2024）等 2D 方法相比，PointAlign 针对 3D 模态的稀疏性和几何语义退化问题提出了专门的解决方案。与早期 3D 方法如 **Point-Bind LLM**（Guo et al., arXiv 2023）和 **GPT4Point**（Qi et al., CVPR 2024）相比，PointAlign 不需要额外的点云-文本对齐预训练阶段，而是直接利用已有 Q-Former 的内部表示作为监督信号，降低了训练复杂度。

### 方法适用边界与约束条件

PointAlign 的有效性受限于以下边界条件：

1. **Q-Former 预训练质量的依赖**：对齐目标选择的是 Q-Former 的输出，这意味着对齐质量的上限由 Q-Former 本身的视觉特征聚合能力决定。若预训练阶段 Q-Former 并未充分捕获精细几何结构（例如训练数据不足或点云编码器表达能力有限），对齐正则化的效果将受到根本性制约。

2. **单一固定层的对齐策略**：当前方法仅在 LLM 的第 16 层（Phi-2 模型）施加对齐损失，这种单点监督可能无法最优地引导整个深层变换过程中的几何信息保留。多层联合对齐策略是否能够进一步提升效果，尚待探索。

3. **静态余弦相似度损失的局限性**：采用的余弦相似度损失对所有 token 和维度赋予相同权重，缺乏对关键几何特征的自适应关注能力。更灵活的对齐形式（如对比学习或可学习距离度量）可能带来进一步的性能增益。

4. **LLM 规模的验证范围**：当前实验主要在 Phi-2（2.7B）和 Phi-3 等较小规模 LLM 上进行验证，在更大规模模型（如 7B、13B）上的可扩展性尚未被系统性地评估。随着 LLM 层数增加，几何信息衰减的模式可能发生变化，最优对齐层的位置和策略可能需要重新校准。

### 已知局限与开放问题

**已识别的局限性**：

- 对齐投影器虽在推理时被移除，不引入额外推理开销，但其训练仍需额外的显存和计算资源（约 8.39M 参数）。
- 在极低数据条件下（如 10% 训练数据），对齐正则化的增益虽然存在（见 Figure 4），但绝对性能仍较低，表明该方法不能完全替代数据规模的不足。
- 余弦相似度损失仅约束方向一致性，放弃了幅度信息，可能在某些需要区分细微几何差异的任务上不够充分。

**开放的后续研究问题**：

1. **多层对齐策略**：在不同中间层同时施加一致性约束，或设计层间递进式的对齐目标（如从浅层几何到深层语义的逐步对齐），能否进一步提升特征保留效果？
2. **自适应对齐形式**：用对比学习或可学习的距离度量替代静态余弦相似度，能否使对齐过程更灵活地关注关键 token 和维度？
3. **大规模模型扩展**：所提方法在更大规模 LLM（如 7B、13B）和更复杂 3D 场景（如室内场景理解、多物体交互）上的可扩展性如何？是否需要调整对齐层的位置或强度？
4. **数据效率的极限**：对齐正则化在数据极缺条件下的泛化边界在哪里？是否需要更复杂的内部监督目标（如自蒸馏或多层一致性）来补偿更少的训练数据？
5. **与 2D 模态的联合对齐**：Q-Former 通常同时处理点云和图像输入，对齐目标是否可以从纯点云扩展到多模态融合表示，以进一步提升跨模态理解能力？

## 原文 PDF

![[paperPDFs/CVPR_2026/PointAlign_Feature_Level_Alignment_Regularization_for_3D_Vision_Language_Models.pdf]]
