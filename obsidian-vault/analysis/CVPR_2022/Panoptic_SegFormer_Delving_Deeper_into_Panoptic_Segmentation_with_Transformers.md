---
title: "Panoptic SegFormer: Delving Deeper into Panoptic Segmentation with Transformers"
type: paper
paper_level: A
venue: CVPR
year: 2022
pdf_ref: paperPDFs/CVPR_2022/Panoptic_SegFormer_Delving_Deeper_into_Panoptic_Segmentation_with_Transformers.pdf
project_link: null
code_link: https://github.com/zhiqi-li/Panoptic-SegFormer
aliases:
- PS
- PSDDIPST
tags:
- CVPR_2022
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "通过在掩码解码器中引入逐层深度监督（每层注意力图均由真值掩码指导），实现快速聚焦与收敛；将查询解耦为独立的thing查询集和stuff查询集，并采用固定类别分配策略消除相互干扰；使用同时考虑分类概率和掩码质量的掩码级合并（mask-wise merging）替代像素级argmax。"
primary_logic: "深度监督可以引导注意力模块从一开始就集中到有意义的区域，从而大幅加速训练收敛并提升掩码精度；通过解耦things和stuff的查询集，避免了两种类别间的相互干扰，尤其使stuff的PQ提升了约2.9个百分点；掩码级合并利用置信度分数解决重叠冲突，减少了伪影。"
claims:
- "查询解耦策略将COCO val上的PQ从48.5提升至49.6，stuff的PQ从39.5提升至42.4，证明了things与stuff查询分离可以消除相互干扰。"
- "深度监督的掩码解码器在24轮训练内即可达到49.6% PQ，而原始DETR需300+轮次，且收敛曲线显示出明显加速。"
- "掩码级合并策略单独为DETR带来1.3% PQ的提升，并在Panoptic SegFormer上比像素级argmax高出1.2% PQ（49.6 vs 48.4）。"
- "Panoptic SegFormer在COCO test-dev上以Swin-L骨干网达到56.2% PQ，超过MaskFormer的53.3%和K-Net的55.2%，为无外部数据下的全景分割新纪录。"
---

# Panoptic SegFormer: Delving Deeper into Panoptic Segmentation with Transformers

> [!tip] 核心洞察
> 深度监督可以引导注意力模块从一开始就集中到有意义的区域，从而大幅加速训练收敛并提升掩码精度；通过解耦things和stuff的查询集，避免了两种类别间的相互干扰，尤其使stuff的PQ提升了约2.9个百分点；掩码级合并利用置信度分数解决重叠冲突，减少了伪影。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Panoptic SegFormer：深入探究全景分割的Transformer方法 |
| 英文题名 | Panoptic SegFormer: Delving Deeper into Panoptic Segmentation with Transformers |
| 会议/期刊 | CVPR 2022 |
| Links | [paper](https://arxiv.org/abs/2109.03814) · [GitHub](https://github.com/zhiqi-li/Panoptic-SegFormer) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | Panoptic SegFormer |
| Dataset | COCO val2017, COCO test-dev, ADE20K val |

> [!tip] 效果简介
> - COCO val2017 上，PQ 为 49.6 (R50)，对比 43.4 (DETR R50)，变化 +6.2。
> - COCO val2017 上，PQ 为 49.6 (R50)，对比 46.5 (MaskFormer R50)，变化 +3.1。
> - COCO test-dev 上，PQ 为 56.2 (Swin-L)，对比 53.3 (MaskFormer Swin-L)，变化 +2.9。

## 概要

全景分割要求对图像中的每个像素同时赋予语义类别和实例ID，既识别可数的“物体”（things，如人、车），也识别不可数的“背景”（stuff，如天空、草地）。基于Transformer的端到端方法（以**DETR**（Carion et al., ECCV 2020）为代表）虽然简化了流水线，却面临三个核心瓶颈：（1）训练收敛极慢，需300+轮次；（2）自注意力的计算复杂度限制了特征分辨率，导致掩码边界模糊；（3）用同一组查询同时处理things和stuff，并为stuff预测边界框，造成两类目标相互干扰，尤其损害stuff的分割质量，且后处理的像素级argmax策略容易产生假阳性。

Panoptic SegFormer针对上述瓶颈提出了三个关键改进，构成了一条高效的全景分割Transformer流水线。其核心洞察在于：**深度监督可以引导注意力模块从一开始就集中到有意义的区域，从而大幅加速训练收敛并提升掩码精度；通过解耦things和stuff的查询集，避免了两种类别间的相互干扰，尤其使stuff的PQ提升约2.9个百分点；掩码级合并利用置信度分数解决重叠冲突，减少了伪影。**

具体而言，方法将查询解耦为独立的thing查询集（通过匈牙利匹配）和stuff查询集（固定类别分配），并引入位置解码器为thing查询提供位置感知特征；在掩码解码器中，每一层的注意力图均由真值掩码进行深度监督，通过超轻量FC头（约200参数）直接从注意力图生成掩码；后处理阶段采用掩码级合并策略，按融合分类概率与分割质量的置信度分数排序掩码，依次填充非重叠区域，替代传统的像素级argmax。

在COCO test-dev上，Panoptic SegFormer以Swin-L骨干网达到**56.2% PQ**，超过MaskFormer的53.3%和K-Net的55.2%，为当时无外部数据下的全景分割新纪录。相比基线DETR，该方法在COCO val上以ResNet-50骨干网将PQ从43.4提升至**49.6**（+6.2），且仅需24轮训练即可收敛，而原始DETR需300+轮次。消融实验进一步证实：查询解耦策略将stuff的PQ从39.5提升至42.4；深度监督是快速收敛的关键；掩码级合并单独为DETR带来1.3% PQ的提升。

该方法仍存在若干局限：在高度拥挤、同类别小目标密集的场景下召回率较低；当大面积stuff区域具有高置信度分数时，可能覆盖空间上重叠的things实例；掩码级合并依赖固定的二值化阈值和置信度阈值，当置信度估计不准确时可能产生低质量全景掩码。

全景分割（panoptic segmentation）要求对图像中的每个像素同时完成语义和实例标签的统一预测，是视觉感知的核心任务之一。近年来，以 **DETR**（Carion et al., ECCV 2020）为代表的端到端Transformer方法将目标检测的查询（query）机制引入分割领域，试图用统一的架构同时处理可数物体（things）和不可数区域（stuff）。然而，这类方法在落地全景分割时暴露出三个系统性的瓶颈。

**瓶颈一：训练收敛极慢。** 基于DETR的全景分割通常需要300轮以上的训练才能达到可用精度，主要原因在于掩码解码器缺乏中间监督信号，注意力模块在训练初期难以快速聚焦到有意义的空间区域。

**瓶颈二：特征分辨率受限，掩码边界模糊。** Transformer自注意力的计算复杂度与特征图尺寸呈二次方关系，迫使模型只能使用低分辨率的C5级特征。这导致预测掩码的边缘粗糙，小目标细节丢失严重。

**瓶颈三：things与stuff相互干扰。** 现有方法（如DETR、**MaskFormer**（Cheng et al., NeurIPS 2021）、**K-Net**（Zhang et al., NeurIPS 2021））将things和stuff的查询混在同一集合中进行二部匹配，并为stuff也预测边界框。这一设计造成两类查询在匹配过程中相互竞争，尤其损害stuff的分割质量。此外，通用的像素级argmax后处理仅依据像素级最大响应决定归属，忽略了掩码整体的分类置信度与分割质量，容易产生假阳性伪影。

上述瓶颈共同制约了Transformer全景分割方法的精度上限和训练效率。**Panoptic SegFormer** 的提出正是为了系统性地解决这三个问题：通过掩码解码器的深度监督实现快速收敛，通过查询解耦消除things与stuff的相互干扰，并通过掩码级合并（mask-wise merging）替代像素级argmax，利用融合分类概率与分割质量的置信度分数解决重叠冲突，从而在更少的训练轮次内达到更高的全景分割质量。

## 核心方法与创新机理

Panoptic SegFormer 围绕 DETR 全景分割的三个瓶颈——训练收敛慢、特征分辨率受限导致掩码边界模糊、thing/stuff 共用查询集产生相互干扰——提出了四个相互耦合的关键创新。

### 1. 查询解耦：消除 thing 与 stuff 的相互干扰

原始 DETR 使用单一查询集同时匹配 things 和 stuff，并为 stuff 类别预测无意义的边界框，导致两类目标在查询内部产生干扰，尤其损害 stuff 的分割质量。Panoptic SegFormer 将查询解耦为独立的 thing 查询集和 stuff 查询集（Figure 3）：

- **thing 查询**：通过匈牙利算法进行二部匹配，并配备位置解码器提供位置感知特征。
- **stuff 查询**：采用固定类别分配策略，每个 stuff 类别对应一个专属查询，无需边界框预测。

这一解耦的因果效应在 Table 8 中得到直接验证：联合匹配时 stuff 的 PQ 仅为 39.5%，解耦后提升至 42.4%（+2.9 pp），总体 PQ 从 48.5 提升至 49.6。此外，stuff 查询精度从 0.60 提高到 0.66，证实了消除干扰的有效性。

### 2. 深度监督的掩码解码器：加速收敛与提升掩码精度

Panoptic SegFormer 的掩码解码器在每个 Transformer 层均引入深度监督——每一层的注意力图由真值掩码直接指导。其核心机制在于：

- 使用超轻量全连接头（仅约 200 参数）从注意力图生成掩码，使注意力模块从一开始就被强制聚焦于有意义的区域。
- 多尺度注意力图经上采样和拼接后融合为统一分辨率的掩码预测。

深度监督的因果效应在 Figure 5 中得到充分体现：配备深度监督的 Panoptic SegFormer 在 24 轮训练内即可达到 49.6% PQ，而移除深度监督后收敛速度显著变慢，最终性能大幅下降。这一机制从根本上解决了 DETR 需要 300+ 轮次训练的收敛瓶颈。

### 3. 掩码级合并：解决重叠冲突与假阳性

传统像素级 argmax 后处理仅按像素选择最大概率类别，忽略了分类概率与掩码质量之间的关联，容易产生假阳性（Figure 4）。Panoptic SegFormer 提出掩码级合并策略（Algorithm 1）：

- 按融合置信度分数排序所有预测掩码，分数定义为分类概率与掩码质量（像素 logit > 0.5 的平均值）的乘积：
  $$s _ { i } = p _ { i } ^ { \alpha } \times \mathrm { a v e r a g e } \big ( \mathbb { 1 } _ { \{ m _ { i } [ h , w ] > 0 . 5 \} } m _ { i } [ h , w ] \big ) ^ { \beta }$$
  其中默认 $\alpha=1, \beta=2$。
- 按序将掩码填充至非重叠区域，滤除低置信度、低覆盖比的掩码。

该策略单独为 DETR 带来 1.3% PQ 的提升，在 Panoptic SegFormer 上比像素级 argmax 高出 1.2% PQ（49.6 vs 48.4，Table 7）。

### 4. 多尺度可变形编码器：突破特征分辨率瓶颈

DETR 仅使用 C5 级低分辨率特征，限制了小目标和边界细节的捕捉。Panoptic SegFormer 引入多尺度可变形注意力编码器，精炼 C3、C4、C5 高分辨率特征。消融实验（Table B.1）显示，多尺度可变形注意力将 DETR 的 PQ 从 43.4 提升至 51.9，显著优于单尺度可变形注意力的 46.3。

### 创新耦合效应

上述四个创新并非孤立存在。从 DETR 到 Panoptic SegFormer 的逐步消融（Table 5）揭示了其累积效应：多尺度编码器奠定特征基础，查询解耦消除类别间干扰，位置解码器为 thing 查询注入空间信息，深度监督加速收敛并提升掩码质量，掩码级合并优化最终输出。最终以 ResNet-50 骨干网在 COCO val 上达到 49.6% PQ，较 DETR 基线提升 6.2 个百分点，同时训练轮次从 300+ 降至 24。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2109_03814/figures/027_Figure.jpg]]
*Figure: B.8. Comparing visualization results of Panoptic SegFormer with other methods on the COCO val set. For a fair comparison, all results are generated with ResNet-101 [23] backbone. The second and fourth row results show that our method still performs well in highly crowded or occluded scenes. Benefits from our mask-wise inference strategy, our results have few artifacts, which often appear in the results of DETR [1] (e.g., dining table of the third row). Figure B.9. Failure case of Panoptic SegFormer*


Panoptic SegFormer 的整体 pipeline 由三个核心模块串联构成：**Transformer 编码器**、**位置解码器**与**掩码解码器**，最后通过**掩码级合并**（mask-wise merging）将输出转换为无重叠的全景分割结果（Figure 2）。

### 数据流与模块关系

1. **主干网**提取多尺度特征图 $C_3, C_4, C_5$，空间尺寸分别为 $\frac{H}{8} \times \frac{W}{8}$、$\frac{H}{16} \times \frac{W}{16}$、$\frac{H}{32} \times \frac{W}{32}$。支持 ResNet、Swin Transformer、PVTv2 等主干网。
2. **Transformer 编码器**以多尺度特征图与对应位置编码为输入，利用**可变形注意力**（deformable attention）进行多尺度特征精炼。可变形注意力的低计算复杂度使得编码器能够处理高分辨率特征，克服了 DETR 中自注意力对特征分辨率的限制。
3. **查询解耦**：系统维护两组独立的查询集——$N_{th}$ 个 thing 查询和 $N_{st}$ 个 stuff 查询。thing 查询先进入**位置解码器**，通过辅助检测损失学习位置感知特征，输出带位置信息的 thing 查询；stuff 查询则直接送入掩码解码器，不参与位置解码。
4. **掩码解码器**接收精炼后的多尺度特征、位置解码器输出的 thing 查询以及原始 stuff 查询，逐层预测类别与掩码。每一层的注意力图均由真值掩码进行**深度监督**，并通过一个仅约 200 参数的极轻量 FC 头将注意力图直接转换为掩码预测。
5. **掩码级合并**（Algorithm 1）将掩码解码器输出的所有掩码按置信度分数 $s_i = p_i^{\alpha} \times \text{average}(\mathbb{1}_{\{m_i[h,w] > 0.5\}} m_i[h,w])^{\beta}$ 排序，依次填充非重叠区域，滤除低置信度、低覆盖比的掩码，最终生成无重叠的全景分割画布。

### 训练与推理流程

- **训练阶段**：thing 分支通过匈牙利算法进行二部匹配，stuff 分支采用固定类别分配策略（class-fixed assign），总体损失为两者加权和：
  $$\mathcal{L} = \lambda_{\text{things}} \mathcal{L}_{\text{things}} + \lambda_{\text{stuff}} \mathcal{L}_{\text{stuff}}$$
  其中 $\mathcal{L}_{\text{things}}$ 包含检测损失及掩码解码器各层的分类与分割损失之和，$\mathcal{L}_{\text{stuff}}$ 为各层分类与分割损失之和。掩码解码器的深度监督使模型在 24 轮训练内即可收敛至 49.6% PQ，而原始 DETR 需 300+ 轮次（Figure 5）。

- **推理阶段**：掩码解码器输出所有查询对应的类别概率与掩码 logits，经掩码级合并后生成最终的全景分割结果。该后处理策略相比传统的像素级 argmax 在 Panoptic SegFormer (R50) 上将 PQ 从 48.4 提升至 49.6（Table 7），并为 DETR 单独带来 1.3% PQ 的提升。

### 关键设计动因

整体框架围绕 DETR 在全景分割中的三个瓶颈展开针对性改进：
- **收敛慢** → 掩码解码器深度监督，引导注意力快速聚焦到有意义区域；
- **特征分辨率受限** → 可变形注意力编码器处理多尺度高分辨率特征；
- **thing/stuff 相互干扰** → 查询解耦，消除两类查询在同一集合中的竞争与干扰，使 stuff 的 PQ 从 39.5 提升至 42.4（Table 8）。

Panoptic SegFormer 的核心架构由 Transformer 编码器、位置解码器和掩码解码器三个模块构成，并通过查询解耦策略和掩码级合并实现高效的全景分割。

### 查询解耦策略

传统方法（如 DETR、MaskFormer、K-Net）使用单一查询集同时匹配 things 和 stuff，导致两类目标在同一个查询内相互干扰。Panoptic SegFormer 将查询解耦为两个独立集合（Figure 3）：

- **Thing 查询集**（$N_{th}$ 个）：通过匈牙利算法的二部匹配与真实实例对应，未匹配的查询分配空标签 $\varnothing$。
- **Stuff 查询集**（$N_{st}$ 个）：采用固定类别分配策略——每个 stuff 类别固定分配一个查询，直接预测该类别的掩码，无需匹配过程。

这种解耦消除了 things 与 stuff 之间的相互干扰。消融实验（Table 8）表明，解耦后 stuff 的 PQ 从 39.5 提升至 42.4，总体 PQ 从 48.5 提升至 49.6。

### Transformer 编码器

编码器采用可变形注意力（Deformable Attention, Zhu et al., ICLR 2020）精炼多尺度特征。主干网输出 C3、C4、C5 三个尺度的特征图，空间尺寸为：

$$L_i = \frac{H}{2^{i+2}} \times \frac{W}{2^{i+2}}, \quad i \in \{3,4,5\}$$

可变形注意力的低计算复杂度使得编码器能够处理高分辨率特征并引入位置编码，为后续解码器提供丰富的空间信息。多尺度可变形注意力将 DETR 的 PQ 从 43.4 提升至 51.9（Table B.1）。

### 位置解码器

位置解码器专为 thing 查询设计，通过交叉注意力从多尺度特征中学习位置感知特征。训练时在位置解码器顶部附加辅助 MLP 头预测边界框和类别，使用检测损失进行监督。这使得 thing 查询能够捕获实例的空间位置信息，辅助后续掩码解码器区分不同实例。6 层位置解码器将 thing 的 PQ 从 50.0 提升至 54.4（Table 6）。

### 掩码解码器与深度监督

掩码解码器接收来自位置解码器的 thing 查询和独立的 stuff 查询，通过交叉注意力与编码器精炼的多尺度特征交互，预测每个查询的类别和掩码。其核心创新在于**逐层深度监督**：

1. 每一层解码器的注意力图 $A$ 按尺度拆分并融合：

   $$(A_3, A_4, A_5) = \text{Split}(A), \quad A_i \in \mathbb{R}^{\frac{H}{2^{i+2}} \times \frac{W}{2^{i+2}} \times h}$$

   $$A_{fused} = \text{Concat}(A_1, \text{Up}_{\times 2}(A_2), \text{Up}_{\times 4}(A_3))$$

2. 融合后的注意力图通过一个超轻量 FC 头（仅约 200 参数）生成掩码预测。

3. **每一层**的掩码预测均由真实掩码监督，引导注意力模块从一开始就聚焦于有意义的区域。

深度监督是掩码解码器快速收敛的关键：移除深度监督后，24 轮训练下的 PQ 显著下降，收敛速度明显变慢（Figure 5）。Figure 6 的可视化表明，有深度监督时注意力图能准确定位目标区域，而无监督时注意力分散。

### 损失函数

整体损失为 things 损失与 stuff 损失的加权和：

$$\mathcal{L} = \lambda_{things} \mathcal{L}_{things} + \lambda_{stuff} \mathcal{L}_{stuff}$$

**Things 损失**包含检测损失和掩码解码器各层的分类与分割损失：

$$\mathcal{L}_{things} = \lambda_{det} \mathcal{L}_{det} + \sum_{i}^{D_m} (\lambda_{cls} \mathcal{L}_{cls}^i + \lambda_{seg} \mathcal{L}_{seg}^i)$$

其中 $D_m$ 为掩码解码器层数，$\mathcal{L}_{det}$ 为位置解码器的辅助检测损失（分类 + 边界框回归），$\mathcal{L}_{cls}^i$ 和 $\mathcal{L}_{seg}^i$ 分别为第 $i$ 层的分类损失（Focal Loss）和分割损失（Dice Loss + BCE Loss），通过匈牙利算法匹配预测与真值。

**Stuff 损失**采用固定一对一匹配，仅含分类与分割损失：

$$\mathcal{L}_{stuff} = \sum_{i}^{D_m} (\lambda_{cls} \mathcal{L}_{cls}^i + \lambda_{seg} \mathcal{L}_{seg}^i)$$

### 掩码级合并

推理阶段，掩码解码器输出 $N_{th} + N_{st}$ 个掩码及其类别预测。Panoptic SegFormer 采用掩码级合并（Algorithm 1）替代传统的像素级 argmax：

1. 计算每个掩码的置信度分数，融合分类概率与分割质量：

   $$s_i = p_i^{\alpha} \times \text{average}\big(\mathbb{1}_{\{m_i[h,w] > 0.5\}} m_i[h,w]\big)^{\beta}$$

   其中 $p_i$ 为分类概率，$\alpha=1$，$\beta=2$ 为默认设置。括号内为掩码 logit 大于 0.5 像素的平均值，衡量分割质量。

2. 按置信度分数降序排列掩码，依次将掩码的非重叠部分填充到全景画布中。

3. 滤除置信度低于阈值 $t_{cnf}$ 或有效像素占比低于 $t_{keep}$ 的掩码。

该策略相比像素级 argmax 在 Panoptic SegFormer (R50) 上将 PQ 从 48.4 提升至 49.6（Table B.2），且在所有对比模型上均表现更优（Table 7）。Figure 4 展示了掩码级合并能利用分类概率线索解决重叠冲突（如笔记本电脑与键盘），避免像素级 argmax 的假阳性问题。

## 实验与关键发现

### 核心性能对比

Panoptic SegFormer 在 COCO 和 ADE20K 数据集上均显著超越同期方法。在 COCO val2017 上，以 ResNet-50 为骨干网，Panoptic SegFormer 达到 **49.6% PQ**，相比 DETR（Carion et al., ECCV 2020）的 43.4% PQ 提升 **+6.2 个百分点**，相比 MaskFormer（Cheng et al., NeurIPS 2021）的 46.5% PQ 提升 **+3.1 个百分点**（Table 1）。在 COCO test-dev 上，以 Swin-L 为骨干网，Panoptic SegFormer 达到 **56.2% PQ**，超越 MaskFormer 的 53.3% PQ 和 K-Net（Zhang et al., NeurIPS 2021）的 55.2% PQ，创下当时无外部数据辅助下的全景分割新纪录（Table 2）。在 ADE20K val 上，以 ResNet-50 为骨干网，Panoptic SegFormer 达到 **36.4% PQ**，比 MaskFormer 高出 1.7 个百分点（Table 3）。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2109_03814/figures/005_Table_1.jpg]]
*Table 1: Experiments on COCO val set. #P and #F indicate number of parameters (M) and number of FLOPs (G). Panoptic Seg-Former (R50) achieves 49.6% PQ on COCO val, surpassing previous methods such as DETR [1] and MaskFormer [3] over 6.2% PQ and 3.1% PQ respectively. † notes that backbones are pretrained on ImageNet-22K*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2109_03814/figures/006_Table_2.jpg]]
*Table 2: Experiments on COCO test-dev set. † notes that backbones are pre-trained on ImageNet-22K. Table 3. Panoptic segmentation results on ADE20K val set*

值得注意的是，Panoptic SegFormer 在参数量与计算量方面具有显著优势。Figure 1 显示，Panoptic SegFormer（PVTv2-B5）以更少的参数量达到 55.4% PQ，在 PQ-参数量曲线上明显优于 MaskFormer 和 K-Net 等同期工作。

### 从 DETR 到 Panoptic SegFormer 的逐步消融

Table 5 展示了从 DETR 基线（43.4% PQ）逐步引入 Panoptic SegFormer 各模块的累积收益：

1. **多尺度可变形注意力编码器**：将 DETR 的 C5 单尺度特征替换为 C3-C5 多尺度特征，并采用可变形注意力（Deformable DETR, Zhu et al., ICLR 2020）进行精炼，PQ 从 43.4% 提升至 **51.9%**（+8.5 个百分点）。该模块是单点提升最大的改动，附录 Table B.1 进一步证实多尺度可变形注意力（51.9% PQ）显著优于单尺度变形注意力（46.3% PQ）。

2. **查询解耦策略**：将单一查询集拆分为独立的 thing 查询集和 stuff 查询集，PQ 进一步提升至 **52.9%**（+1.0 个百分点）。Table 8 的详细消融表明，解耦策略将 stuff 的 PQ 从 39.5（联合匹配）提升至 42.4，总体 PQ 从 48.5 提升至 49.6，且 stuff 查询精度从 0.60 提高到 0.66，验证了 thing 与 stuff 查询分离可以消除相互干扰。

3. **掩码级合并**：替代像素级 argmax 后处理，PQ 提升至 **53.5%**（+0.6 个百分点）。Table 7 和附录 Table B.2 显示，掩码级合并策略在 Panoptic SegFormer (R50) 上将 PQ 从 48.4 提升至 49.6，且在所有对比模型上均优于像素级 argmax。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2109_03814/figures/012_Table_7.jpg]]
*Table 7: Effect of mask-wise merging strategy. The table shows the results of models with different post-processing methods, and the backbone is ResNet-50. “(p)” refers to using pixel-wise argmax as the post-processing method. “(p*)” considers both class probability and mask prediction probability in its pixel-wise argmax strategy [3]. Models with “(m)” that employ mask-wise merging always perform better in both Mask PQ and Boundary PQ [41] than pixel-wise argmax method. Table 8. Effect of query decoupling strategy. PQ and AP scores of various panoptic segmentation models on COCO val2017*

4. **位置解码器**：为 thing 查询引入位置感知特征，PQ 提升至 **54.4%**（+0.9 个百分点）。Table 6 的消融表明，6 层位置解码器将 thing 的 PQ 从 50.0 提升至 54.4，移除位置解码器会使 thing PQ 下降 4.4 点，证明其对实例分割至关重要。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2109_03814/figures/007_Table_6.jpg]]
*Table 6: Ablate location decoder*

5. **深度监督掩码解码器**：在掩码解码器各层引入逐层深度监督，最终达到 **55.2% PQ**（+0.8 个百分点）。Figure 5 的收敛曲线显示，深度监督使模型在 24 轮训练内即可达到 49.6% PQ，而移除深度监督后收敛速度显著变慢，证明深度监督对加速训练收敛和提升掩码精度均有关键作用。

### 深度监督的收敛加速效应

Figure 5 对比了 Panoptic SegFormer 与 D-DETR-MS 在不同训练轮次下的收敛曲线。结果表明，Panoptic SegFormer 在 24 轮训练后即可达到 49.6% PQ，而原始 DETR 需要 300+ 轮次。移除深度监督（“w/o ds”）后，模型在 24 轮下的 PQ 显著下降，收敛速度明显减缓。Figure 6 进一步可视化了掩码解码器各层的注意力图：有深度监督时，注意力图从第一层开始就能聚焦于有意义的语义区域；无深度监督时，浅层注意力图分散且缺乏语义聚焦，深层才逐渐收敛。

### 掩码级合并 vs. 像素级 argmax

掩码级合并策略的核心机制是按置信度分数 $s_i = p_i^{\alpha} \times \text{average}(\mathbb{1}_{\{m_i[h,w] > 0.5\}} m_i[h,w])^{\beta}$ 对掩码排序，依次填充非重叠区域，并滤除低置信度、低覆盖比的掩码（Algorithm 1）。Table 7 显示，该策略单独为 DETR 带来 1.3% PQ 的提升，在 Panoptic SegFormer 上比像素级 argmax 高出 1.2% PQ。附录 Figure B.1 的可视化对比表明，像素级 argmax 容易在 thing 边界附近产生假阳性碎片，而掩码级合并通过掩码级冲突解决机制有效抑制了此类伪影。

### 掩码解码器深度分析

Table 10 显示，掩码解码器第 2 层的输出已接近最终层精度（49.5% PQ vs. 49.6% PQ），表明深度监督使浅层注意力图已具备较强的掩码预测能力。这一特性使得推理时可以使用更浅的解码器以加速计算，而精度损失极小。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2109_03814/figures/011_Table_10.jpg]]
*Table 10: Results of each layer in the mask decoder*

### 鲁棒性评估

Table 11 报告了 COCO-C 数据集上的鲁棒性结果。Panoptic SegFormer (Swin-L) 在 16 种损坏类型上的平均 PQ 为 47.2%，比 MaskFormer (Swin-L) 的 41.7% 高出 **5.5 个百分点**，差距大于干净数据上的 2.9 个百分点，表明 Panoptic SegFormer 对图像损坏具有更强的鲁棒性。使用 Transformer 骨干网（Swin-L 和 PVTv2-B5）进一步提升了鲁棒性。

### 失败模式与局限

尽管 Panoptic SegFormer 整体表现优异，但仍存在以下已知局限：

1. **小目标召回率低**：在高度拥挤、同类别小目标密集的场景下，模型容易遗漏小目标。这与可变形注意力在有限采样点下对小尺度特征的覆盖不足有关。

2. **stuff 覆盖 things**：当大面积 stuff 区域（如天空、草地）具有高置信度分数时，掩码级合并可能将其优先填充，覆盖空间上重叠的 things 实例，导致部分目标无法出现在最终全景画布上。

3. **阈值敏感性**：掩码级合并采用固定的二值化阈值（>0.5）和置信度阈值（$t_{cnf}$、$t_{keep}$）。当置信度估计不准确时，可能产生低质量的全景掩码，或在多候选掩码均低于阈值时导致部分像素被赋予 void 标签。附录 Table B.4 的阈值敏感性分析显示，PQ 在不同阈值组合下存在约 0.3-0.5 个百分点的波动。

4. **置信度估计依赖**：掩码级合并策略对分类概率和掩码质量分数的准确性有较强依赖，模型需要同时产出可靠的分类和分割置信度。

## 定位与知识库关联

### 与现有方法的继承与差异

Panoptic SegFormer 的方法谱系根植于基于 Transformer 的端到端全景分割框架，其直接前身是 **DETR**（Carion et al., ECCV 2020）和 **Deformable DETR**（Zhu et al., ICLR 2020）。DETR 首次将 Transformer 引入目标检测与全景分割，但其核心瓶颈在于训练收敛极慢（需 300+ 轮次）、自注意力计算复杂度限制了特征分辨率，以及使用单一查询集同时处理 things 和 stuff 导致两类目标相互干扰。Panoptic SegFormer 针对这三个瓶颈进行了系统性改造：首先，用可变形注意力替代全局自注意力，使编码器能够高效处理多尺度高分辨率特征（C3、C4、C5），从而缓解了特征分辨率受限的问题；其次，引入逐层深度监督的掩码解码器，使注意力模块从一开始就被真值掩码引导到有意义的区域，大幅加速收敛——仅需 24 轮训练即可达到 49.6% PQ，而 DETR 需 300+ 轮次（Figure 5, Table 5）。

与同期工作相比，Panoptic SegFormer 与 **MaskFormer**（Cheng et al., NeurIPS 2021）和 **K-Net**（Zhang et al., NeurIPS 2021）同属“掩码 Transformer”范式，但核心设计路径不同。MaskFormer 将全景分割统一为掩码分类问题，使用单一查询集处理所有类别，并通过像素级 argmax 进行后处理。Panoptic SegFormer 则提出查询解耦策略——将 things 查询和 stuff 查询分离，things 查询通过匈牙利二部匹配分配，stuff 查询采用固定类别分配——从而消除了两类目标在同一查询内部的干扰。这一策略使 stuff 的 PQ 从 39.5 提升至 42.4，总体 PQ 从 48.5 提升至 49.6（Table 8）。K-Net 通过动态卷积核统一处理语义与实例分割，但其后处理仍依赖像素级 argmax；Panoptic SegFormer 的掩码级合并策略则利用融合分类概率与掩码质量的置信度分数排序掩码，依次填充非重叠区域，比像素级 argmax 高出 1.2% PQ（Table B.2）。

与 **Panoptic FCN**（Li et al., CVPR 2021）和 **Max-Deeplab**（Wang et al., CVPR 2021）相比，Panoptic SegFormer 的方法论差异更为根本。Panoptic FCN 采用“自顶向下 + 自底向上”的混合框架，需要独立的语义分割分支和实例分割分支，并通过后处理融合；Panoptic SegFormer 则以统一的查询驱动掩码解码器完成所有预测，架构更为简洁。Max-Deeplab 是首个将掩码 Transformer 用于全景分割的工作，但其掩码预测机制与 Panoptic SegFormer 的深度监督注意力图生成掩码的方式不同，且后者在训练效率和精度上均有显著优势。

### 适用边界

Panoptic SegFormer 的设计使其在以下场景中具有明显优势：

1. **训练资源受限但追求高精度**：深度监督的掩码解码器使模型在 24 轮训练内即可收敛，大幅降低了训练时间成本，适合无法承受 300+ 轮次训练的团队。
2. **stuff 类别占比较高的场景**：查询解耦策略专门解决了 stuff 分割质量差的问题，在 ADE20K 等 stuff 类别丰富的数据集上，Panoptic SegFormer (R50) 达到 36.4% PQ，超过 MaskFormer 的 34.7%（Table 3）。
3. **多骨干网兼容性**：方法支持 ResNet、Swin Transformer、PVTv2 等多种骨干网，用户可根据计算预算灵活选择——从轻量级 ResNet-50（约 47M 参数）到高性能 Swin-L（约 212M 参数），PQ 从 49.6 提升至 56.2（Table 1, Table 2）。

然而，该方法在以下边界条件下可能表现不佳：

1. **高度拥挤的小目标场景**：作者明确指出，在同类别小目标密集的场景下，召回率较低，易遗漏小目标。这源于可变形注意力虽然降低了计算复杂度，但特征分辨率仍受限于 C3 级别（下采样 8 倍），对极小目标的定位能力有限。
2. **stuff 区域覆盖 things 实例**：当大面积的 stuff 区域（如天空、草地）具有高置信度分数时，掩码级合并策略可能使其覆盖空间上重叠的 things 实例，导致部分目标无法出现在最终画布上。这是掩码级合并的固有缺陷——按置信度排序填充时，高置信度的 stuff 掩码会优先占据画布。
3. **置信度估计不准确时**：掩码级合并依赖固定的二值化阈值（>0.5）和置信度阈值，当模型输出的分类概率或掩码质量分数不准确时，可能产生低质量的全景掩码，或在多候选掩码均低于阈值时导致部分像素被赋予 void 标签。

### 局限与开放问题

**已知局限**：

1. **小目标召回率低**：在密集小目标场景中，模型倾向于遗漏小目标。这一局限与可变形注意力的采样点数量和多尺度特征融合策略有关，但论文未提供针对性的消融实验来量化小目标性能损失的具体程度。
2. **stuff 对 things 的覆盖问题**：掩码级合并按置信度排序填充，高置信度的 stuff 掩码可能覆盖空间上重叠的 things 实例。这一问题的根源在于合并策略缺乏显式的空间冲突解决机制，仅依赖置信度分数作为软性优先级。
3. **阈值敏感性**：掩码级合并使用固定的二值化阈值和置信度阈值，当置信度估计不准确时，可能产生低质量掩码或 void 标签。论文未探索自适应阈值或动态阈值调整策略。
4. **对置信度准确性的强依赖**：掩码级合并策略要求模型同时产出可靠的分类概率和掩码质量分数，这对训练损失的设计提出了更高要求。如果分类头或分割头的校准不佳，合并效果会显著下降。

**开放问题**：

1. **更大空间尺寸的特征处理**：如何在保持计算效率的前提下处理更大空间尺寸的特征，以进一步改善小目标的性能？当前可变形注意力的计算复杂度虽低于全局自注意力，但仍随特征分辨率线性增长，限制了更高分辨率特征（如 C2 级别）的使用。
2. **可变形注意力的实时化**：能否进一步加速可变形注意力的计算，使其在实时场景下更具竞争力？论文中 Panoptic SegFormer (R50) 的 FPS 约为 11.8（Table 5），距离实时应用（>30 FPS）仍有较大差距。
3. **统一查询管道的泛化性**：统一查询管道是否适用于所有分割任务仍然是个开放问题。如何自适应地为不同任务（如全景分割、实例分割、语义分割、视频全景分割）设计查询和匹配策略，避免为每个任务重新设计查询集？
4. **掩码级合并的自适应阈值**：掩码级合并的阈值选择能否通过自学习或动态调整进一步提升鲁棒性？例如，根据图像的复杂度或掩码的重叠程度动态调整置信度阈值，可能减少 void 标签的产生。
5. **深度监督的泛化机制**：深度监督在掩码解码器中展示了显著的收敛加速效果，但其泛化机制尚不完全清楚——深度监督是否对所有 Transformer 解码器结构都有效？在其他视觉任务（如视频分割、3D 分割）中，类似的注意力图监督策略是否同样有效？

## 原文 PDF

![[paperPDFs/CVPR_2022/Panoptic_SegFormer_Delving_Deeper_into_Panoptic_Segmentation_with_Transformers.pdf]]
