---
title: "SegFormer: Simple and Efficient Design for Semantic Segmentation with Transformers"
type: paper
paper_level: A
venue: NeurIPS
year: 2021
pdf_ref: paperPDFs/NEURIPS_2021/SegFormer_Simple_and_Efficient_Design_for_Semantic_Segmentation_with_Transformers.pdf
project_link: null
code_link: https://github.com/NVlabs/SegFormer
aliases:
- SegFormer
tags:
- NEURIPS_2021
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "移除位置编码并引入Mix-FFN（3×3卷积）提供位置信息，同时采用层次化Transformer编码器输出多尺度特征，并设计轻量级全MLP解码器融合多级局部与全局注意力。"
primary_logic: "层次化Transformer编码器在低层产生类似卷积的局部注意力，在高层产生全局非局部注意力；通过仅由MLP构成的解码器直接融合这些多尺度特征，即可获得强大的语义表示，无需任何额外的复杂上下文模块。"
claims:
- "Mix-FFN完全替代位置编码，且在不同测试分辨率下性能更加鲁棒（分辨率变化时mIoU仅下降0.7%，而位置编码下降3.3%）。"
- "将相同的MLP解码器用于CNN编码器（ResNet/ResNeXt）时，mIoU显著低于用于Transformer编码器（MiT），证明解码器受益于Transformer更大的有效感受野。"
- "SegFormer-B5在ADE20K上达到51.8% mIoU，比SETR高1.6%，同时参数量减少4倍；在Cityscapes上达到84.0% mIoU，比此前最佳高1.8%，速度快5倍。"
- "ADE20K 上 mIoU (single-scale) = 51.8%"
---

# SegFormer: Simple and Efficient Design for Semantic Segmentation with Transformers

> [!tip] 核心洞察
> 层次化Transformer编码器在低层产生类似卷积的局部注意力，在高层产生全局非局部注意力；通过仅由MLP构成的解码器直接融合这些多尺度特征，即可获得强大的语义表示，无需任何额外的复杂上下文模块。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SegFormer：简单高效的语义分割Transformer设计 |
| 英文题名 | SegFormer: Simple and Efficient Design for Semantic Segmentation with Transformers |
| 会议/期刊 | NeurIPS 2021 |
| Links | [paper](https://arxiv.org/abs/2105.15203) · [GitHub](https://github.com/NVlabs/SegFormer) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | SegFormer |
| Dataset | ADE20K, Cityscapes validation, Cityscapes (real-time), COCO-Stuff full |

> [!tip] 效果简介
> - ADE20K 上，mIoU (single-scale) 为 51.8%，对比 50.2% (SETR)，变化 +1.6%。
> - Cityscapes validation 上，mIoU 为 84.0%，对比 82.2% (SETR)，变化 +1.8%。
> - Cityscapes (real-time) 上，mIoU / FPS 为 76.2% / 15.2 FPS (SegFormer-B0, short side 1024)，对比 75.2% / 8.4 FPS (DeepLabV3+ MobileNetV2)，变化 +1.0% mIoU, +6.8 FPS。

## 概要

语义分割是计算机视觉中的基础任务，要求对图像中的每个像素赋予语义类别标签。近年来，基于Transformer的模型在各类视觉任务中展现出强大的全局建模能力，但其在语义分割上的应用仍面临两个关键瓶颈：**编码器缺乏多尺度特征**，以及**位置编码在测试分辨率变化时需要插值导致性能显著下降**。典型的Transformer分割模型（如**SETR**，Zheng et al., CVPR 2021）采用ViT作为骨干，仅输出单一低分辨率特征图，解码器则依赖复杂的CNN结构进行上采样和特征融合，计算开销大，难以在保持精度的同时实现高效推理。

SegFormer针对上述瓶颈，提出了一套简洁而高效的语义分割框架。其核心设计包含三个关键改动：

1. **层次化Transformer编码器（MiT）**：输出1/4、1/8、1/16、1/32四种分辨率的多尺度特征，低层产生类似卷积的局部注意力，高层产生全局非局部注意力。
2. **Mix-FFN替代位置编码**：在每个Transformer块的FFN中嵌入3×3深度可分离卷积，利用零填充隐式提供位置信息，完全移除显式位置编码，使模型在不同测试分辨率下更加鲁棒。
3. **轻量级全MLP解码器**：仅由MLP层构成，将多级特征统一通道后上采样并拼接，通过线性投影直接预测分割掩膜，无需任何额外的复杂上下文模块。

这一设计带来了显著的性能与效率优势。在ADE20K上，SegFormer-B5达到51.8% mIoU，比SETR高1.6%，同时参数量减少4倍；在Cityscapes验证集上达到84.0% mIoU，比此前最佳方法高1.8%，速度快5倍。即使是最轻量的SegFormer-B0，也能以3.7M参数在Cityscapes上实现71.9% mIoU和48 FPS的实时推理速度。消融实验进一步表明，MLP解码器搭配Transformer编码器（MiT）显著优于搭配CNN编码器（ResNet/ResNeXt），验证了Transformer更大有效感受野对解码器性能的关键支撑作用。



语义分割是计算机视觉的基础任务，要求为图像中的每个像素分配类别标签。该任务在自动驾驶、医学影像分析等场景中具有广泛的应用价值。长期以来，基于全卷积网络（FCN）的编码器-解码器架构主导了该领域，代表性工作包括 **DeepLabV3+**（Chen et al., ECCV 2018）和 **PSPNet**（Zhao et al., CVPR 2017）。这些方法以卷积神经网络（CNN）为骨干，虽然通过空洞卷积、金字塔池化等模块扩大了感受野，但CNN固有的局部操作限制了其捕获全局上下文的能力。

近年来，Vision Transformer（ViT）的兴起为语义分割带来了新的范式。**SETR**（Zheng et al., CVPR 2021）首次将ViT作为分割编码器，利用自注意力机制捕获长程依赖，取得了优于CNN方法的性能。然而，SETR的设计存在两个关键瓶颈：

**瓶颈一：编码器缺乏多尺度特征。** SETR采用标准ViT作为骨干，其自注意力层在整个网络中保持固定的特征图分辨率，仅输出单一尺度的低分辨率特征（通常为输入图像的1/16）。这与CNN骨干（如ResNet）天然输出1/4、1/8、1/16等多尺度特征形成鲜明对比。语义分割要求同时处理大物体（需要全局上下文）和小物体（需要高分辨率细节），单尺度特征表示从根本上限制了分割精度。

**瓶颈二：位置编码的测试分辨率脆弱性。** SETR继承了ViT的可学习位置编码，当测试图像分辨率与训练分辨率不一致时，需要对位置编码进行插值。实验表明，这种插值会导致显著的性能下降——分辨率变化时mIoU可降低3.3%（见Table 1c）。在自动驾驶等实际部署场景中，输入分辨率经常因摄像头规格、天气条件等因素而变化，这一脆弱性严重制约了模型的实用性。

此外，SETR的解码器设计沿用了传统CNN分割头（如多层3×3卷积），计算开销较大。后续工作如 **OCRNet**（Yuan et al., ECCV 2020）通过引入目标上下文表示进一步提升了精度，但整体架构仍依赖复杂的解码器设计，难以在精度和效率之间取得良好平衡。

上述问题揭示了一个核心矛盾：Transformer的自注意力机制天然擅长捕获全局信息，但如何在不引入位置编码脆弱性的前提下，同时获得多尺度特征表示，并以轻量级方式融合这些特征，仍是未解决的关键挑战。SegFormer正是从这三个维度出发，重新设计了语义分割的Transformer架构。



## 核心方法与创新机理

SegFormer 的核心创新并非引入全新的注意力机制或复杂的上下文聚合模块，而是通过**移除传统Transformer分割模型中的两个冗余组件，并重新设计编码器-解码器协作方式**，实现了精度与效率的双重突破。

### 1. 用Mix-FFN替代位置编码

传统Transformer语义分割模型（如 **SETR**，Zheng et al., CVPR 2021）依赖可学习的位置编码（Positional Encoding, PE）来提供空间位置信息。然而，当测试图像分辨率与训练分辨率不一致时，位置编码需要进行插值，导致性能显著下降。SegFormer 的解决方案是**完全移除位置编码**，转而在每个Transformer块的前馈网络（FFN）中嵌入一个 $3 \times 3$ 深度可分离卷积，构成 **Mix-FFN**：

$$x_{out} = MLP(GELU(Conv_{3\times3}(MLP(x_{in})))) + x_{in}$$

Mix-FFN 利用卷积的零填充（zero padding）特性来“泄漏”位置信息，从而隐式地为模型提供空间感知能力。这一设计的决定性优势体现在 **Table 1c** 中：在训练分辨率（$768 \times 768$）下，Mix-FFN 的 mIoU 为 80.5%，而位置编码仅为 77.3%；当测试分辨率切换至 Cityscapes 原生分辨率（$1024 \times 2048$）时，Mix-FFN 仅下降 0.7%（至 79.8%），而位置编码则大幅下降 3.3%（至 74.0%）。这表明 Mix-FFN 在不同测试分辨率下具有更强的鲁棒性，是模型能够灵活部署的关键。

### 2. 从单尺度到多尺度的层次化Transformer编码器

**SETR** 等早期方法采用标准 ViT 作为编码器，仅输出单一的低分辨率特征图（通常为 $H/16 \times W/16$），缺乏处理语义分割所需的多尺度信息。SegFormer 设计了**层次化Transformer编码器（MiT）**，通过重叠补丁合并（Overlapped Patch Merging）逐步降低特征分辨率，输出 $1/4$、$1/8$、$1/16$、$1/32$ 四种尺度的特征图。这一层次化结构在低层产生类似卷积的局部注意力，在高层产生全局非局部注意力，为解码器提供了丰富的多尺度语义信息。

### 3. 轻量级全MLP解码器

传统分割模型（如 **SETR** 的CNN解码器、**DeepLabV3+** 的ASPP模块）使用复杂的卷积结构来融合多尺度特征，计算开销大。SegFormer 提出了一个**仅由MLP层构成的轻量级解码器**，通过四个简单步骤完成特征融合与预测：

$$\hat{F}_i = Linear(C_i, C)(F_i), \quad \hat{F}_i = Upsample_{H/4 \times W/4}(\hat{F}_i)$$
$$F = Linear(4C, C)(Concat(\hat{F}_1, \dots, \hat{F}_4)), \quad M = Linear(C, N_{cls})(F)$$

该解码器将所有多级特征统一通道后上采样至 $1/4$ 分辨率，拼接后通过MLP融合，最后线性投影生成分割掩膜。**Table 1d** 的关键证据表明：当同样的MLP解码器搭配CNN编码器（ResNet/ResNeXt）时，mIoU 显著低于搭配MiT编码器（如 MiT-B2 的 45.4% vs ResNet101 的 38.7%），证明解码器的有效性依赖于Transformer编码器更大的有效感受野，而非解码器本身的复杂度。

### 创新总结

SegFormer 的三项创新——Mix-FFN、层次化MiT编码器、全MLP解码器——共同构成了一个**极简但高效的分割框架**。它移除了位置编码和复杂解码器这两个传统组件，转而利用卷积的隐式位置信息和Transformer的天然全局感受野，在简化设计的同时实现了性能的显著提升。



SegFormer 的整体设计遵循**分层编码器–轻量解码器**范式，由两个核心模块串联构成：层次化 Transformer 编码器（MiT）与全 MLP 解码器（All-MLP Decoder）。输入图像首先被划分为 4×4 的补丁，随后流经四个阶段的层次化编码器，输出分辨率分别为 1/4、1/8、1/16、1/32 的多尺度特征图；这些特征图直接送入仅由线性层构成的解码器，经过通道统一、上采样、拼接与 MLP 融合，最终通过线性投影生成分割掩膜。

### 数据流与模块关系

整个前向传播的数据流可概括为以下步骤：

1. **补丁嵌入**：输入图像 $H \times W \times 3$ 被划分为 $4 \times 4$ 的补丁，经线性投影后得到初始特征图，分辨率降至 $H/4 \times W/4$。
2. **层次化编码**：MiT 编码器包含 4 个阶段（Stage 1–4），每个阶段由若干 Transformer 块堆叠而成。阶段间通过**重叠补丁合并**（Overlapped Patch Merging）降低分辨率并增加通道数，最终输出四种尺度的特征 $\{F_1, F_2, F_3, F_4\}$，分辨率分别为 $1/4$、$1/8$、$1/16$、$1/32$（见 Figure 2）。
3. **轻量化解码**：All-MLP 解码器接收四层特征后执行四步操作（详见公式 4）：
   - **通道统一**：通过 MLP 将各层特征通道 $C_i$ 映射到统一维度 $C$；
   - **上采样**：将所有特征图双线性上采样至 $H/4 \times W/4$；
   - **拼接与融合**：沿通道维拼接后，经 MLP 将 $4C$ 维压缩至 $C$ 维；
   - **掩膜预测**：通过线性层将 $C$ 维特征投影到 $N_{cls}$ 维，得到最终分割掩膜 $M$。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2105_15203/figures/002_Figure_2.jpg]]
*Figure 2: The proposed SegFormer framework consists of two main modules: A hierarchical Transformer encoder to extract coarse and fine features; and a lightweight All-MLP decoder to directly fuse these multi-level features and predict the semantic segmentation mask. “FFN” indicates feed-forward network*

### 关键设计取舍

- **无位置编码**：编码器中完全移除了传统 Transformer 的位置编码（Positional Encoding），转而依赖 Mix-FFN 中的 3×3 深度可分离卷积提供位置信息。这一设计使模型在测试分辨率变化时无需插值，显著提升了鲁棒性（Table 1c：分辨率变化时 mIoU 仅下降 0.7%，而位置编码方案下降 3.3%）。
- **高效自注意力**：为应对高分辨率特征图带来的 $O(N^2)$ 计算开销，MiT 引入序列缩减机制（缩减比 $R$），将键 $K$ 的序列长度压缩至 $N/R$，使注意力复杂度降至 $O(N^2/R)$（公式 2）。
- **解码器极简化**：解码器仅由 MLP 层构成，不含任何卷积或复杂的上下文聚合模块。消融实验表明，该解码器与 Transformer 编码器配合时效果显著优于与 CNN 编码器（ResNet/ResNeXt）配合（Table 1d），验证了 Transformer 更大的有效感受野是解码器性能的关键支撑。

### 框架优势

这一设计将多尺度特征提取与融合完全解耦：编码器在低层产生类似卷积的局部注意力，在高层产生全局非局部注意力；解码器仅通过 MLP 直接融合这些多级特征，即可获得强大的语义表示，无需额外的空间金字塔池化、空洞卷积或交叉注意力模块。整个框架在保持极简结构的同时，实现了参数效率与分割精度的双重优势——SegFormer-B5 在 ADE20K 上以比 SETR 少 4 倍的参数量达到 51.8% mIoU（Table 2）。



SegFormer 由两个核心模块构成：层次化 Transformer 编码器（MiT）与全 MLP 解码器。编码器负责提取多尺度特征，解码器仅通过 MLP 层融合这些特征并直接预测分割掩膜。

### 层次化 Transformer 编码器（MiT）

输入图像首先被划分为 $4 \times 4$ 的补丁，随后送入四阶段层次化结构。每个阶段包含若干 Transformer 块，并通过重叠补丁合并（Overlapped Patch Merging）逐步降低特征分辨率，输出 1/4、1/8、1/16、1/32 四种尺度的特征图。补丁合并参数为：第一阶段 $K=7, S=4, P=3$，后续阶段 $K=3, S=2, P=1$。

**高效自注意力**：标准缩放点积自注意力计算复杂度为 $O(N^2)$，其中 $N$ 为序列长度。为降低计算开销，MiT 引入序列缩减比 $R$ 对键 $K$ 进行降采样：

$$\mathrm{Attention}(Q,K,V) = \mathrm{Softmax}\left(\frac{QK^{\mathsf{T}}}{\sqrt{d_{head}}}\right)V \tag{1}$$

$$\hat{K} = \mathrm{Reshape}(N/R, C \cdot R)(K), \quad K = \mathrm{Linear}(C \cdot R, C)(\hat{K}) \tag{2}$$

其中 $Q$、$K$、$V$ 分别为查询、键、值矩阵，$d_{head}$ 为每个注意力头的维度，$C$ 为通道维度。通过式 (2) 的序列缩减操作，自注意力复杂度降至 $O(N^2/R)$。

**Mix-FFN**：传统 ViT 依赖位置编码提供空间信息，但固定分辨率的位置编码在测试分辨率变化时需插值，导致性能下降。SegFormer 完全移除位置编码，转而在每个 Transformer 块的前馈网络（FFN）中嵌入 $3 \times 3$ 深度可分离卷积，构成 Mix-FFN：

$$\mathbf{x}_{out} = \mathrm{MLP}(\mathrm{GELU}(\mathrm{Conv}_{3\times3}(\mathbf{MLP}(\mathbf{x}_{in})))) + \mathbf{x}_{in} \tag{3}$$

其中 $\mathbf{x}_{in}$ 为自注意力层输出的特征。Mix-FFN 利用零填充（zero padding）的 $3 \times 3$ 卷积隐式泄露位置信息，实验表明该方法在不同测试分辨率下均优于传统位置编码，且对分辨率变化更加鲁棒（Table 1c）。

### 全 MLP 解码器

解码器仅由 MLP 层构成，无需任何卷积或复杂的上下文模块。其工作流程如式 (4) 所示：

$$\hat{F}_i = \mathrm{Linear}(C_i, C)(F_i), \quad \forall i$$

$$\hat{F}_i = \mathrm{Upsample}_{H/4 \times W/4}(\hat{F}_i), \quad \forall i$$

$$F = \mathrm{Linear}(4C, C)(\mathrm{Concat}(\hat{F}_1, \dots, \hat{F}_4))$$

$$M = \mathrm{Linear}(C, N_{cls})(F) \tag{4}$$

其中 $F_i$ 为编码器第 $i$ 阶段的输出特征（通道数 $C_i$），$C$ 为统一的解码器通道维度（实时模型 B0/B1 设为 256，其余设为 768），$N_{cls}$ 为类别数。四步流程为：① 通过 MLP 将各阶段特征统一到 $C$ 维；② 将所有特征上采样至 1/4 分辨率；③ 拼接四个尺度的特征并通过 MLP 融合为 $C$ 维特征 $F$；④ 线性投影输出最终分割掩膜 $M$。

该设计的核心洞察在于：层次化 Transformer 编码器在低层产生类似卷积的局部注意力，在高层产生全局非局部注意力；全 MLP 解码器通过直接拼接和融合这些多尺度特征，即可获得强大的语义表示，无需额外的复杂上下文模块。Table 1d 的消融实验证实，将相同 MLP 解码器用于 CNN 编码器（ResNet/ResNeXt）时 mIoU 显著低于用于 MiT 编码器，验证了 Transformer 更大有效感受野的关键作用。



## 实验与关键发现

### 核心性能：精度与效率的帕累托前沿

SegFormer在多个语义分割基准上实现了精度与效率的双重突破。在ADE20K上，SegFormer-B5以单尺度测试达到**51.8% mIoU**，相比此前最优的SETR（50.2%）提升1.6个百分点，同时参数量减少4倍（Table 2）。在Cityscapes验证集上，SegFormer-B5达到**84.0% mIoU**，比SETR（82.2%）高出1.8个百分点，推理速度提升5倍。值得注意的是，即使是最轻量的SegFormer-B0，在Cityscapes上以1024短边输入也能达到76.2% mIoU，同时保持15.2 FPS的实时推理速度，在精度和速度上均优于**DeepLabV3+**（Chen et al., ECCV 2018）搭配MobileNetV2（75.2% mIoU / 8.4 FPS）（Table 2）。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2105_15203/figures/005_Table_2.jpg]]
*Table 2: Comparison to state of the art methods on ADE20K and Cityscapes. SegFormer has significant advantages on #Params, #Flops, #Speed and #Accuracy. Note that for SegFormer-B0 we scale the short side of image to {1024, 768, 640, 512} to get speed-accuracy tradeoffs. Mix-FFN vs. Positional Encoder (PE). In this experiment, we analyze the effect of removing the positional encoding in the Transformer encoder in favor of using the proposed Mix-FFN. To this end, we train Transformer encoders with a positional encoding (PE) and the proposed Mix-FFN and perform inference on Cityscapes with two different image resolutions: 768×768 using a sliding window, and 1024×2048 using the whole image*

在COCO-Stuff全量数据集（164K图像，172类）上，SegFormer同样取得46.7% mIoU，超过SETR的45.8%（Table 4）。Cityscapes测试集结果显示，在使用相同或更少额外数据的情况下，SegFormer持续优于此前方法（Table 3）。Figure 1以散点图形式直观展示了SegFormer在ADE20K上的性能-效率权衡：在同等参数量下，SegFormer的mIoU显著高于此前所有方法，形成了新的帕累托前沿。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2105_15203/figures/006_Table_3.jpg]]
*Table 3: Comparison to state of the art methods on Cityscapes test set. IM-1K, IM-22K, Coarse and MV refer to the ImageNet-1K, ImageNet-22K, Cityscapes coarse set and Mapillary Vistas. SegFormer outperforms the compared methods with equal or less extra data*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2105_15203/figures/007_Table_4.jpg]]
*Table 4: Results on COCO-Stuff full dataset containing all 164K images from COCO 2017 and covers 172 classes*

### 消融实验：设计选择的因果验证

消融实验系统验证了SegFormer三个核心设计选择的因果效应（Table 1）。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2105_15203/figures/004_Table_1.jpg]]
*Table 1: Ablation studies related to model size, encoder and decoder design. (a) Accuracy, parameters and flops as a function of the model size on the three datasets. “SS” and “MS” means single/multi-scale test*

**编码器规模与解码器轻量化。** Table 1a显示，将编码器从MiT-B0逐步扩大到MiT-B5，在ADE20K、Cityscapes和COCO-Stuff上均带来一致的mIoU提升（如ADE20K单尺度从37.4%升至51.0%）。与此同时，解码器参数量仅占总参数的极小比例（3.3M至0.4M），证明性能增益主要来自编码器容量，而非解码器复杂度。Table 1b进一步表明，解码器通道维度C=256时已获得最佳效率-精度权衡；当C超过768后，性能趋于饱和（C=768时45.4%，C=2048时45.6%），验证了轻量级MLP解码器的充分性。

**Mix-FFN替代位置编码。** Table 1c直接对比了Mix-FFN与可学习位置编码（PE）的效果。在训练分辨率（768×768）下，Mix-FFN达到80.5% mIoU，优于PE的77.3%；当测试分辨率变化为1024×2048时，Mix-FFN仅下降0.7%（至79.8%），而PE则大幅下降3.3%（至74.0%）。这一定量证据有力证明了Mix-FFN通过3×3卷积的零填充机制提供了对分辨率变化鲁棒的位置信息，完全消除了传统位置编码在测试分辨率变化时需插值导致的性能退化。

**MLP解码器与Transformer编码器的协同效应。** Table 1d揭示了关键因果机制：将相同的MLP解码器分别搭配Transformer编码器（MiT-B2）和CNN编码器（ResNet-101/ResNeXt-101），前者达到45.4% mIoU，而后者仅分别为38.7%和39.0%。这一显著差距（约6.5个百分点）证明MLP解码器的有效性并非源于其自身设计，而是受益于Transformer编码器更大的有效感受野（ERF）。进一步消融显示，仅使用Stage-4特征时mIoU为40.7%，而融合Stage-1至Stage-4特征后提升至45.4%，验证了结合低层局部注意力与高层全局注意力的必要性。

### 有效感受野分析

Figure 3可视化了DeepLabV3+与SegFormer在Cityscapes上的有效感受野（ERF）（100张图像平均）。结果显示，SegFormer各阶段的ERF显著大于DeepLabV3+对应阶段，且SegFormer解码器的ERF覆盖更广的上下文区域。这从机制层面解释了Table 1d中的现象：Transformer编码器天然具备更大的非局部感受野，使得仅由MLP构成的解码器无需额外的上下文聚合模块即可获得强大的语义表示。

### 鲁棒性评估

在Cityscapes-C损坏数据集上（Table 5），SegFormer在所有损坏类型下均优于DeepLabV3+（搭配MobileNetV2、ResNet或Xception）。Figure 7进一步展示了不同损坏严重度下的性能下降曲线：SegFormer（蓝线）在各严重度级别上均保持高于DeepLabV3+（橙线）的mIoU，且下降趋势更平缓，表明其对图像损坏具有更强的零样本鲁棒性。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2105_15203/figures/009_Table_5.jpg]]
*Table 5: Main results on Cityscapes-C. “DLv3+”, “MBv2”, “R” and “X” refer to DeepLabv3+, MobileNetv2, ResNet and Xception. The mIoUs of compared methods are reported from [77]*

### 定性结果

Figure 4和Figure 5展示了Cityscapes、ADE20K和COCO-Stuff上的分割可视化。相比SETR，SegFormer在物体边界附近预测出明显更精细的细节；相比DeepLabV3+，SegFormer显著减少了长程错误（如Figure 4中红色高亮区域），直观验证了Transformer全局注意力机制在语义分割中的优势。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2105_15203/figures/012_Figure_5.jpg]]
*Figure 5: Qualitative results on Cityscapes, ADE20K and COCO-Stuff. First row: Cityscapes. Second row: ADE20K. Third row: COCO-Stuff. Zoom in for best view*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2105_15203/figures/014_Figure_7.jpg]]
*Figure 7: Comparison of zero shot robustness on Cityscapes-C between SegFormer and DeepLabV3+. Blue line is SegFormer and orange line is DeepLabV3+. X-Axis means corrupt severity and Y-Axis is mIoU. Following[77], we test 3 severities for “Noise” and 5 severities for the rest*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2105_15203/figures/010_Table.jpg]]

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2105_15203/figures/011_Table_7.jpg]]
*Table 7: Mix Transformer Encoder*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2105_15203/figures/001_Figure_1.jpg]]
*Figure 1: Performance vs. model efficiency on ADE20K. All results are reported with single model and single-scale inference. SegFormer achieves a new state-of-the-art 51.0% mIoU while being significantly more efficient than previous methods*



## 定位与知识库关联

**SegFormer** 处于语义分割从纯卷积架构向Transformer架构过渡的关键节点。其设计直接回应了早期ViT式分割模型（如 **SETR**, Zheng et al., CVPR 2021）的两个核心瓶颈：编码器缺乏多尺度特征层级，以及位置编码在测试分辨率变化时需插值导致性能退化。SegFormer通过三个因果调节变量——层次化Transformer编码器（MiT）、Mix-FFN替代位置编码、全MLP解码器——在保持Transformer全局感受野优势的同时，实现了比CNN方法更优的效率-精度权衡。

**与CNN分割范式的对比。** 在SegFormer之前，语义分割的主流方案长期由卷积架构主导：**PSPNet** (Zhao et al., CVPR 2017) 利用金字塔池化聚合多尺度上下文；**DeepLabV3+** (Chen et al., ECCV 2018) 将空洞空间金字塔池化与编解码器结构结合；**OCRNet** (Yuan et al., ECCV 2020) 引入目标上下文表示进一步提升精度。这些方法依赖堆叠卷积层逐步扩大感受野，但受限于卷积的局部操作特性，长程依赖的建模效率较低。SegFormer的层次化Transformer编码器在低层产生类似卷积的局部注意力、在高层产生全局非局部注意力，有效感受野（ERF）可视化（Figure 3）显示其解码器输出显著优于DeepLabV3+的全局覆盖能力。

**在Transformer分割谱系中的位置。** SETR首次将ViT引入语义分割，但仅输出单尺度低分辨率特征，且依赖复杂的CNN解码器恢复空间细节。SegFormer的改进体现在三个维度：（1）通过重叠补丁合并构建层次化结构，输出1/4至1/32四种分辨率的特征图，自然适配密集预测任务的多尺度需求；（2）以Mix-FFN中的3×3深度可分离卷积完全替代位置编码，不仅消除了测试分辨率变化时的插值退化（Table 1c：Mix-FFN在分辨率变化时mIoU仅下降0.7%，而位置编码下降3.3%），还使模型对输入尺寸具有零样本鲁棒性；（3）将解码器简化为仅由线性层构成的全MLP结构，参数量仅0.4M–3.3M，远低于SETR的CNN解码器。

**解码器设计的因果证据。** Table 1d的消融实验揭示了SegFormer解码器设计的因果机制：将相同的MLP解码器分别用于Transformer编码器（MiT-B2）和CNN编码器（ResNet-101/ResNeXt-101）时，mIoU从45.4%骤降至38.7%/39.1%，证明MLP解码器的有效性依赖于Transformer编码器提供的更大有效感受野。此外，仅使用Stage-4特征（全局注意力）的mIoU为43.8%，而融合Stage-1至Stage-4特征（同时结合局部和全局注意力）提升至45.4%，验证了多尺度特征融合对MLP解码器的必要性。

**适用边界与局限。** SegFormer在标准基准上展现了强大的性能（ADE20K: 51.8% mIoU；Cityscapes: 84.0% mIoU），且SegFormer-B0以3.7M参数在Cityscapes上达到76.2% mIoU/15.2 FPS的实时性能，显著优于DeepLabV3+ MobileNetV2（75.2%/8.4 FPS）。然而，其高效自注意力机制通过序列缩减比R将K/V的序列长度压缩，在极高分辨率输入下仍可能面临计算瓶颈。此外，最小的SegFormer-B0是否能在内存仅100K的极端边缘设备上正常工作，仍是一个开放问题。论文未报告在医学影像、遥感等特殊领域的迁移表现，这些场景中Transformer的归纳偏置是否同样有效需要进一步验证。

**鲁棒性评估。** 在Cityscapes-C损坏数据集上，SegFormer在所有损坏类型上均优于DeepLabV3+（Table 5），且在不同损坏严重度下的性能下降曲线更平缓（Figure 7），表明Mix-FFN提供的卷积式位置先验可能增强了模型对图像损坏的结构鲁棒性。这一特性与ViT类模型通常需要大规模数据训练才能获得鲁棒性的认知形成对比，但论文未深入分析其内在机制。



## 原文 PDF

![[paperPDFs/NEURIPS_2021/SegFormer_Simple_and_Efficient_Design_for_Semantic_Segmentation_with_Transformers.pdf]]
