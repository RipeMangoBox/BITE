---
title: "Native Segmentation Vision Transformers"
type: paper
paper_level: A
venue: NeurIPS
year: 2025
pdf_ref: paperPDFs/NEURIPS_2025/Native_Segmentation_Vision_Transformers.pdf
code_link: null
project_link: https://research.nvidia.com/labs/dvl/projects/native-segmentation/
aliases:
- SNSVT
- NSVT
tags:
- NEURIPS_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/segmentation
core_operator: "将均匀下采样替换为内容感知的空间分组层（differentiable, iterative clustering）。该层学习将视觉令牌动态分配到语义一致的组中，从而在骨干网络中构建层次化的区域表示。"
primary_logic: "通过堆叠可微分的分组层，骨干网络能够原生地将像素组织成多尺度的语义区域，形成类似马尔可夫链的令牌映射。这种设计使分割掩码从骨干网络中自然涌现，无需专用的分割头，同时保留了可扩展性和端到端可微性。"
claims:
- "空间分组层用基于学习的动态令牌分配替代了均匀网格下采样，以图像内容为导向。"
- "连续分组操作构成从输入像素到最终令牌的映射，自然地创建多尺度的分割掩码层次结构。"
- "在无掩码监督的ImageNet分类训练下，超像素状结构在前几层中涌现，并在最后的密集分组层中被组合成语义连贯的区域。"
- "零样本分割中，SeNaTra 在六个基准上显著优于先前的方法，并且不需要任何后处理（如CRF或PAMR）。"
---

# Native Segmentation Vision Transformers

> [!tip] 核心洞察
> 通过堆叠可微分的分组层，骨干网络能够原生地将像素组织成多尺度的语义区域，形成类似马尔可夫链的令牌映射。这种设计使分割掩码从骨干网络中自然涌现，无需专用的分割头，同时保留了可扩展性和端到端可微性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 原生分割视觉Transformer |
| 英文题名 | Native Segmentation Vision Transformers |
| 会议/期刊 | NeurIPS 2025 |
| Links | [paper](https://arxiv.org/abs/2505.16993) · [Project](https://research.nvidia.com/labs/dvl/projects/native-segmentation) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/segmentation |
| Method | SeNaTra (Native Segmentation Vision Transformer) |
| Dataset | Pascal VOC (zero-shot semantic segmentation), ADE20k (semantic segmentation with mask supervision), ADE20k (semantic segmentation with M2F head), COCO val2017 (panoptic segmentation) |

> [!tip] 效果简介
> - Pascal VOC (zero-shot semantic segmentation) 上，mIoU 为 61.3，对比 55.0 (TCL)，变化 +6.3。
> - ADE20k (semantic segmentation with mask supervision) 上，mIoU 为 49.7 (SeNaTra-T native)，对比 47.1 (NAT-T w/ UperNet)，变化 +2.6。
> - ADE20k (semantic segmentation with M2F head) 上，mIoU 为 51.3 (SeNaTra-T + M2F)，对比 49.1 (NAT-T* w/ M2F)，变化 +2.2。

## 概要

现代视觉骨干网络（如 Swin Transformer、NAT）普遍采用均匀网格下采样（池化或跨步卷积），对所有空间位置一视同仁，不感知图像内容。这导致在下游分割任务中出现特征错位，迫使解码器头承担额外的补偿负担，限制了骨干网络本身的分割能力。

**SeNaTra**（Native Segmentation Vision Transformer）针对这一瓶颈提出了根本性的解决方案：将均匀下采样替换为**内容感知的空间分组层**。该层通过可微的迭代聚类，学习将视觉令牌动态分配到语义一致的组中，使下采样过程遵循图像边界而非固定网格。连续的分组操作在骨干网络各阶段之间构成马尔可夫链式的令牌映射，从而原生地构建出多尺度的区域表示层次。

核心结论是：**分割掩码可以从骨干网络中自然涌现，无需专用的分割头**。即使在无掩码监督的 ImageNet 分类预训练下，早期层中也会自发出现超像素状结构，并在后续密集分组层中组合成语义连贯的区域（Figure 3）。在零样本文本监督语义分割中，SeNaTra-B 在六个基准上平均达到 31.9/33.1 mIoU，显著优于依赖 CRF/PAMR 后处理的先前方法（Table 1）。在有监督分割微调中，SeNaTra-T 以原生掩码方式在 ADE20k 上达到 49.7 mIoU，超过 NAT-T + UperNet 的 47.1 mIoU；结合 Mask2Former 头后达到 51.3 mIoU，较 NAT-T + M2F 提升 +2.2 mIoU（Table 2）。在 COCO 全景分割上，SeNaTra-T 原生掩码达到 49.2 PQ，结合 M2F 后达到 55.0 PQ，分别超出相应基线 +1.5 和 +2.0 PQ。

消融实验进一步证实了分组层的决定性作用：将所有分组层替换为均匀下采样导致 ADE20k 原生掩码 mIoU 从 49.7 骤降至 41.3（-8.4），而添加像素解码器对 SeNaTra 的影响极小（+0.2 mIoU），说明分组层已经提供了丰富的空间信息。在效率方面，尽管分组层相比均匀下采样引入了约 20-40% 的延迟开销，但端到端分割中这一开销被总体性能提升所摊销——SeNaTra-B 原生掩码模型在吞吐量和 mIoU 上均优于 NAT-B + UperNet。

**方法定位**：SeNaTra 属于基于分组的分层视觉骨干方法，在架构层面将分割能力内嵌到骨干网络中，区别于依赖专用分割头（如 UperNet、Mask2Former）的传统范式。它继承了标准分层 Transformer 的四阶段结构，但将下采样操作从“均匀网格”替换为“内容感知分组”，将上采样操作从“双线性插值”替换为“分组分配矩阵的组合”。这一设计使其既能原生输出分割掩码，又能无缝集成到现有分割框架中。

### 视觉骨干网络中的均匀下采样困境

现代视觉骨干网络——无论是卷积架构还是Transformer架构——普遍采用均匀网格下采样（如池化、跨步卷积）来构建层次化特征金字塔。这种操作对所有空间位置一视同仁，完全不感知图像内容。当这些骨干网络被应用于语义分割、全景分割等像素级密集预测任务时，均匀下采样带来的特征错位问题便暴露无遗：边界区域的像素可能被错误地合并到相邻语义区域中，迫使下游的解码器头承担额外的补偿负担。

Figure 1 清晰地展示了这一困境：传统骨干网络（上图）通过均匀下采样压缩特征图，再依赖双线性插值等均匀上采样来恢复分辨率以生成分割掩码。这种“均匀下采样—均匀上采样”的范式在根本上限制了骨干网络本身的分割能力，使得分割任务始终依赖于精心设计的专用解码器头。

### 现有方法的局限性

当前解决这一问题的路径主要有两类：

**专用分割头范式**：以 **UperNet**、**Mask2Former**（M2F）为代表的方法在标准骨干网络之上叠加像素解码器和Transformer解码器，通过复杂的交叉注意力机制来补偿特征错位。然而，这些解码器头引入了大量额外参数和计算开销，且并未从根本上改变骨干网络“内容不感知”的本质。

**基于分组的骨干方法**：**GroupViT** 等工作尝试在骨干网络中引入分组机制，但其分组操作依赖于密集交叉注意力，计算复杂度高，难以扩展到大规模场景。此外，这些方法的分组能力往往需要专门的预训练任务来激活，缺乏通用性。

### 核心动机：让分割从骨干网络中自然涌现

本文的核心洞察在于：如果骨干网络本身能够在特征提取过程中感知图像内容，将像素动态地组织成语义一致的组，那么分割掩码就可以从骨干网络中自然涌现，无需依赖专用的分割头。

具体而言，本文提出将均匀下采样替换为**内容感知的空间分组层**——一种可微分的迭代聚类操作。该层学习将视觉令牌动态分配到语义一致的组中，使下采样过程与图像边界对齐。通过堆叠多个这样的分组层，骨干网络能够在不同阶段构建层次化的区域表示，形成从输入像素到最终令牌的马尔可夫链式映射。这种设计使得：

1. **分割掩码原生生成**：骨干网络的分组分配矩阵可以直接用于上采样，结合轻量MLP即可生成像素级预测，无需专用分割头。
2. **层次化表示自然涌现**：即使在无掩码监督的ImageNet分类训练下，早期层中也会自发形成超像素状结构，并在深层分组层中被组合成语义连贯的区域（Figure 3）。
3. **端到端可微且可扩展**：分组操作完全可微，支持标准反向传播训练，且通过局部稀疏化设计将计算复杂度控制在可接受范围内。

这种“原生分割”范式从根本上重新思考了视觉骨干网络的设计：骨干网络不应仅仅是特征提取器，而应成为分割任务的一等公民。

## 核心方法与创新机理

SeNaTra 的核心创新在于**将视觉骨干网络中的均匀下采样替换为内容感知的空间分组层**，从而将分割能力内化到骨干网络本身，而非依赖外部的专用解码器头。这一转变涉及三个关键组件的重新设计。

### 从均匀下采样到内容感知的空间分组

现代分层视觉骨干（如 **Swin Transformer**、**NAT**）普遍采用池化或跨步卷积进行均匀网格下采样。这类操作对所有空间位置一视同仁，不感知图像内容，导致下游分割任务中特征与物体边界错位，迫使解码器头承担额外的补偿负担。

SeNaTra 提出的**空间分组层**（Spatial Grouping Layer）彻底改变了这一范式：它将下采样建模为一个可微的迭代聚类过程，学习将视觉令牌动态分配到语义一致的组中。具体而言，该层将输出令牌视为聚类中心，通过迭代的软分配与中心更新，将与同一物体或语义区域相似的输入令牌映射到同一个输出令牌。这一过程受 K-means 及其现代可微变体的启发，但被完全嵌入到 Transformer 骨干的前向传播中。

与 **GroupViT** 等先前基于分组的方法使用密集交叉注意力（复杂度 $O(L N^2 d)$）不同，SeNaTra 在高分辨率阶段将注意力限制在 $3\times3$ 的局部窗口内，将复杂度降至 $O(L N d)$，从而实现了对大规模输入的可扩展性。在最终阶段，模型启用密集分组以捕获全局语义一致性。

### 可组合的令牌映射与有原则上采样

空间分组层产生的软分配矩阵不仅是下采样的工具，它们天然构成了一条**马尔可夫链**。连续阶段的分组操作将分配矩阵依次相乘，定义了从任意阶段的令牌到更早或更晚阶段令牌的映射：

$$A_{l\to l-k}^{\mathsf{ups}} := A_{l-k+1}^{\mathsf{ups}} \times \cdots \times A_{l}^{\mathsf{ups}}, \qquad A_{l\to l+k}^{\mathsf{down}} := (A_{l+k-1}^{\mathsf{down}})^{T} \times \cdots \times (A_{l}^{\mathsf{down}})^{T}$$

这一性质使得**上采样不再需要双线性插值等均匀操作**，而是直接利用学习到的分组赋值矩阵，以内容感知的方式将低分辨率令牌映射回像素空间。这为后续的原生分割提供了理论基础。

### 原生分割：无需专用分割头

上述两个创新的直接结果是**分割掩码可以从骨干网络中自然涌现**。SeNaTra 的原生分割范式仅需在骨干的最终组令牌嵌入上附加一个轻量的 2 层 MLP，然后利用组合的赋值矩阵上采样至输入分辨率，即可生成像素级预测。这完全消除了对 **UperNet** 或 **Mask2Former** 等复杂解码器头的依赖。

即使在无掩码监督的 ImageNet 分类预训练下，前几层中也会自发涌现超像素状结构，并在最后的密集分组层中被组合成语义连贯的区域（Figure 3）。当与 Mask2Former 头结合时，SeNaTra 的分组层实质上替代了标准上采样路径，为 Transformer 解码器提供了与物体边界对齐的层次化特征。

### 关键设计选择

消融实验揭示了几个对性能至关重要的设计决策：
- **跳过连接替代 GRU 更新**：在分组层的迭代更新中，用跳过连接替换 GRU 机制带来了 **+4.8 mIoU** 的提升，并解决了预训练中的数值不稳定性。
- **步长卷积初始化**：使用可学习嵌入初始化分组中心会导致性能下降 2.5–3.2 mIoU，表明从输入特征中通过步长卷积导出的初始化对聚类质量至关重要。
- **相对位置编码**：在分组层中引入相对位置编码额外贡献约 1 mIoU。

### 与传统方法的本质区别

| 组件 | 标准骨干（Swin/NAT） | SeNaTra |
|------|---------------------|---------|
| 下采样 | 均匀网格（池化/跨步卷积） | 内容感知空间分组（可微迭代聚类） |
| 上采样 | 双线性插值 | 组合分组分配矩阵（马尔可夫链） |
| 分割掩码生成 | 依赖专用头（UperNet/M2F） | 原生掩码（MLP + 赋值矩阵上采样） |

这一设计使分割能力从“解码器补偿”转变为“骨干内建”，在零样本分割、有监督语义分割和全景分割三个场景下均实现了对标准骨干的显著超越，同时保持了端到端的可微性和可扩展性。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2505_16993/figures/002_Figure_2.jpg]]
*Figure 2: Overall model design. Visualization of our hierarchical architecture and its key components. (a) Our backbone architecture consists of four processing stages interconnected by content-aware grouping layers for downsampling. (b) Core operations of our Spatial Grouping Layer, which computes soft token assignments and updates group features iteratively (detailed in Algorithm 1). (c) The composition of learned assignment matrices across grouping layers in consecutive backbone stages enables principled feature upsampling*

SeNaTra（Native Segmentation Vision Transformer）遵循现代分层视觉骨干网络的标准结构，由四个处理阶段组成，逐步降低特征图的空间分辨率并增加通道数。给定一张尺寸为 $H \times W$ 的输入图像，初始阶段将其划分为 $4 \times 4$ 的补丁以获得初始令牌嵌入；随后的每个阶段 $S_i$（$i=2,3,4$）生成分辨率为 $(H/2^{i+1}) \times (W/2^{i+1})$ 的令牌表示。

该框架的核心创新在于将传统骨干网络中阶段间的均匀下采样操作（池化或跨步卷积）替换为**内容感知的空间分组层**（Content-aware Spatial Grouping Layer）。该层不依赖固定的网格，而是通过可微的迭代聚类过程，根据图像内容将视觉令牌动态分配到语义一致的组中，从而在下采样过程中对齐物体边界。

### 模块关系与数据流

SeNaTra 的 pipeline 由以下关键模块构成，其整体架构如 **Figure 2** 所示：

1. **Patch Embedding**：初始标记化模块，将输入图像切分为 $4 \times 4$ 的补丁，生成初始令牌嵌入序列，作为后续阶段的输入。

2. **Spatial Grouping Layer**（空间分组层）：部署于相邻阶段之间，负责内容感知的下采样。具体而言：
   - 在第二和第三阶段使用**局部分组**（local grouping），将交叉注意力计算限制在每个输出令牌周围的 $3 \times 3$ 局部窗口内，将计算复杂度从 $\mathcal{O}(L N^2 d)$ 降至 $\mathcal{O}(L N d)$。
   - 在最终阶段启用**密集分组**（dense grouping），即非稀疏的全局分组，以捕获更完整的语义上下文。
   - 该层输出软分配矩阵，记录了输入令牌到输出令牌的映射关系。

3. **Transformer Encoder Stages**：每个阶段内部包含若干 Transformer 编码器层，使用旋转位置编码（RoPE）和局部自注意力机制进行特征处理。各阶段输出的令牌嵌入在通道维度上逐步加倍，空间维度逐步减半。

4. **分组分配矩阵的组合与上采样**：连续阶段的分组操作自然构成从输入像素到最终令牌的映射，形成类似马尔可夫链的结构。具体而言，从阶段 $l$ 到阶段 $l-k$ 的上采样映射和从 $l$ 到 $l+k$ 的下采样映射通过分配矩阵的乘积定义：

   $$A_{l\to l-k}^{\mathsf{ups}} := A_{l-k+1}^{\mathsf{ups}} \times \cdots \times A_{l}^{\mathsf{ups}}, \qquad A_{l\to l+k}^{\mathsf{down}} := (A_{l+k-1}^{\mathsf{down}})^{T} \times \cdots \times (A_{l}^{\mathsf{down}})^{T}$$

   这一机制使模型能够在没有专用分割头的情况下，通过组合学习到的分配矩阵实现有原则的特征上采样。

5. **预测头**：
   - **原生分割**：将骨干网络最终阶段的分组令牌嵌入送入一个 2 层 MLP（维度 512），然后利用学习到的像素分配矩阵将步长 32 的预测上采样至输入分辨率，直接生成逐像素的类别预测。
   - **全景分割**：额外使用一个 2 层 MLP 进行目标检测，作用于分配值最大的 top-100 个最终分组令牌。
   - **零样本分割**：通过线性投影层处理最终图像输出令牌，经全局池化和 L2 归一化得到图像分组嵌入；分类时，将数据集类别名称通过文本编码器获得文本嵌入，选择与每个分组嵌入余弦相似度最大的类别，再经由上采样操作生成最终掩码。

### 与传统范式的本质区别

传统分割流程（如 **Swin Transformer** 或 **NAT** 搭配 **UperNet**/**Mask2Former**）依赖均匀下采样提取特征，再通过专用的分割头（像素解码器 + Transformer 解码器）进行上采样和掩码预测。SeNaTra 将分割能力内化到骨干网络中：分组层在下采样时已学习对齐语义边界，上采样则直接复用分组分配矩阵的转置乘积，无需额外的双线性插值或可学习的上采样模块。这种设计使分割掩码从骨干网络中自然涌现，而非依赖外部分割头的补偿。

### 整体架构：四阶段层次化骨干网络

SeNaTra 遵循现代层次化视觉骨干网络的标准结构，由四个处理阶段组成，逐步降低空间分辨率并加倍通道数。给定输入图像 $H \times W$，初始阶段将其分割为 $4 \times 4$ 的补丁以获得初始令牌嵌入；后续每个阶段 $S_i$（$i = 2, 3, 4$）产生的令牌分辨率为 $(H/2^{i+1}) \times (W/2^{i+1})$。核心创新在于阶段间的下采样操作：用**内容感知的空间分组层**替换传统的均匀网格下采样（池化/跨步卷积）。

### 空间分组层：可微迭代聚类

空间分组层将具有相似特征嵌入的令牌映射到同一输出令牌，从而在下采样表示中保留语义上有意义的边界。其核心思想源自 K-means 聚类及其现代可微变体：输出令牌充当聚类中心，输入令牌通过迭代过程进行软分配。

**算法流程（Algorithm 1）** 包含以下关键步骤：

1. **初始化**：使用步长卷积从输入令牌生成初始输出令牌嵌入，而非可学习嵌入（消融实验表明，使用可学习嵌入初始化会导致性能下降 2.5/3.2 mIoU）。
2. **软分配计算**：计算输入令牌与输出令牌之间的相似度，生成软分配矩阵。对于高分辨率特征图（第二阶段和第三阶段），交叉注意力计算被限制在每个输出令牌周围的 $3 \times 3$ 局部窗口内，将计算复杂度从 $\mathcal{O}(L N^2 d)$ 降至 $\mathcal{O}(L N d)$。在最终阶段启用密集分组（非稀疏）。
3. **中心更新**：根据软分配加权聚合输入令牌特征来更新输出令牌嵌入。消融实验表明，使用**跳跃连接**替代 GRU 更新机制带来了 **+4.8 mIoU** 的提升，并解决了 ImageNet 预训练期间的数值不稳定性问题。
4. **迭代细化**：重复分配和更新步骤，使分组逐步收敛到语义一致的令牌组。

### 分配矩阵的马尔可夫链组合

空间分组层输出的软分配矩阵具有关键性质：它们定义了相邻阶段间令牌的映射关系。通过矩阵乘法，这些分配矩阵可以组合成跨多个阶段的上下采样映射，构成马尔可夫链：

$$
A_{l\to l-k}^{\mathsf{ups}} := A_{l-k+1}^{\mathsf{ups}} \times \cdots \times A_{l}^{\mathsf{ups}}, \qquad A_{l\to l+k}^{\mathsf{down}} := (A_{l+k-1}^{\mathsf{down}})^{T} \times \cdots \times (A_{l}^{\mathsf{down}})^{T}
$$

其中：
- $A_{l}^{\mathsf{ups}}$ 是从阶段 $l$ 到阶段 $l-1$ 的上采样分配矩阵（行随机矩阵）
- $A_{l}^{\mathsf{down}}$ 是从阶段 $l$ 到阶段 $l+1$ 的下采样分配矩阵（列随机矩阵）
- $A_{l\to l-k}^{\mathsf{ups}}$ 定义了从阶段 $l$ 到更早阶段 $l-k$ 的令牌上采样映射
- $A_{l\to l+k}^{\mathsf{down}}$ 定义了从阶段 $l$ 到更深阶段 $l+k$ 的令牌下采样映射

这一组合性质使得骨干网络能够**有原则地进行特征上采样**，无需依赖双线性插值等均匀上采样方法。在原生分割模式下，最终阶段的分组令牌嵌入通过轻量级 2 层 MLP 生成类别预测，然后利用学习到的像素分配矩阵 $A_{4\to 1}^{\mathsf{ups}}$ 上采样至输入分辨率，直接产生像素级分割掩码。

### Transformer 编码器阶段

每个阶段内部使用标准 Transformer 编码器块进行特征处理。SeNaTra 将自注意力层中的相对位置偏置替换为 **RoPE**（旋转位置编码），并使用局部自注意力机制。不同模型变体（Tiny/Base/Large）的阶段层数、输出维度和 MLP 比率详见 Table 5，输出嵌入维度分别为 512、1024 和 1536。

## 实验与关键发现

### 核心实验设置

SeNaTra 的实验覆盖三种监督范式：无掩码监督（图像分类与图像-文本对比学习）、掩码监督（语义与全景分割微调）以及零样本文本监督分割。模型提供 Tiny (T)、Base (B)、Large (L) 三个规模变体，输出嵌入维度分别为 512、1024、1536，详细配置见 Table 5。关键公平性保证包括：

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2505_16993/figures/011_Table_5.jpg]]
*Table 5: Model variants. We summarize the model configuration of each of our backbone variants: number of transformer encoder layers used at each stage (# layers), output token dimension (dim), and MLP hidden dimension ratio in transformer encoder layers (MLP ratio)*

- 零样本分割中**完全不使用 CRF 或 PAMR 等后处理技术**，而多数对比方法依赖这些后处理获得 3–4 mIoU 的提升。
- 用于零样本分割的训练数据仅为 CC3M+CC12M（约 2000 万图像-文本对），远小于 CLIP 的 4 亿对，但取得了有竞争力的结果。
- 与 Mask2Former 结合时遵循相同的训练设置和迭代次数，确保公平对比。

### 主实验结果

#### 零样本文本监督语义分割

Table 1 展示了 SeNaTra 在六个基准上的零样本分割性能。SeNaTra-B（CC3M+CC12M）在 Pascal VOC 上达到 **61.3 mIoU**，较 TCL 的 55.0 提升 **+6.3**，六个数据集平均 mIoU 为 **31.9**。额外使用 RedCaps12M 数据后，平均 mIoU 进一步提升至 **33.1**。值得注意的是，SeNaTra 在多数基准上超越了一众专用方法，包括那些利用 CLIP 在 4 亿图像-文本对上预训练的模型，且完全无需后处理——而 TCL、CoDe、SimSeg 等方法均依赖 CRF/PAMR 获得性能增益。

Table 7 的消融进一步验证了骨干网络本身的能力：SeNaTra-B 无后处理平均 mIoU 达 **41.4**，显著优于 ViT-B+CRF 的 37.8，说明分组层带来的空间归纳偏置是零样本分割性能的关键来源。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2505_16993/figures/013_Table_7.jpg]]
*Table 7: Backbone comparison for text-supervised zero-shot segmentation. Our approach significantly outperforms SimSeg [41] trained with a ViT backbone, without relying on CRF post-processing*

#### 有监督语义分割（ADE20k）

Table 2a 显示，SeNaTra-T 的原生掩码在 ADE20k 上达到 **49.7 mIoU**，较 NAT-T+UperNet 的 47.1 提升 **+2.6**。当集成 Mask2Former (M2F) 头时，SeNaTra-T+M2F 达到 **51.3 mIoU**，较 NAT-T*+M2F 的 49.1 提升 **+2.2**。这表明分组骨干不仅能够独立产生高质量分割掩码，也能作为更强的特征提取器提升现有分割头的性能。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2505_16993/figures/007_Table_2.jpg]]
*Table 2: Downstream semantic and panoptic segmentation after fine-tuning. (a) mIoU on ADE20k. (b) PQ on COCO val2017. (c) Conceptual visualization of segmentation paradigms. Models marked with † are pre-trained on ImageNet-22K. NAT-T∗ is our implementation. (a) Impact of grouping at each backbone stage*

#### 有监督全景分割（COCO）

Table 2b 显示，SeNaTra-T 原生掩码在 COCO val2017 上达到 **49.2 PQ**，显著超越 MaskFormer+Swin-T 的 47.7 PQ（**+1.5**）。集成 M2F 头后，SeNaTra-T+M2F 达到 **55.0 PQ**，较 Swin-T+M2F 的 53.0 提升 **+2.0**；更大规模的 SeNaTra-L+M2F 进一步提升至 **58.1 PQ**。

### 架构消融分析

#### 分组层的阶段级贡献

Table 3a 系统评估了各阶段分组层的重要性。**将全部分组层替换为均匀下采样**导致 ADE20k 原生掩码 mIoU 从 49.7 骤降至 41.3（**-8.4**），证实了内容感知下采样是性能的核心来源。逐阶段分析表明，在早期阶段引入分组层带来的增益最大，而在最后阶段使用局部（而非密集）分组会显著降低性能。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2505_16993/figures/008_Table_3.jpg]]
*Table 3: Architecture-level ablations. We report native masks mIoU on ADE20k and Zero-Shot(ZS) mIoU on Pascal VOC. In (a), we evaluate the effect of replacing grouping layers with uniform downsampling at each stage. In (b), we study low-level design decisions inside our grouping layer*

#### 分组层内部设计选择

Table 3b 揭示了分组层内部的关键设计决策：

- **用跳过连接替代 GRU 更新机制**带来 **+4.8 mIoU** 的提升，并解决了 ImageNet 预训练中的数值不稳定问题。
- 使用可学习嵌入初始化（而非步长卷积）导致性能下降 **2.5/3.2 mIoU**，而从头学习的高斯分布初始化同样损害稳定性。
- 使用相对位置编码带来约 **+1 mIoU** 的额外增益。

#### 分割范式对比

Table 4 的分析表明，在标准骨干（NAT）上添加像素解码器可带来 **+6.4 mIoU** 的提升，但对 SeNaTra 的影响极小——这直接证明了**分组层已经提供了丰富的空间信息**，使得额外的像素解码器变得冗余。这一发现从实验角度验证了论文的核心主张：分割能力可以被编码进骨干网络内部表示，而非依赖专用解码器模块。

![[assets/figures/papers/paper_list_l9_https_arxiv_org_abs_2505_16993/figures/009_Table_4.jpg]]
*Table 4: Segmentation paradigms. We ablate adding a Pixel Decoder and Transformer Decoder on ADE20k (mIoU) and COCO-Panoptic (PQ)*

### 效率分析

Table 8 比较了 SeNaTra 原生掩码与 NAT+UperNet 的端到端效率。尽管分组层相比均匀下采样引入了约 20–40% 的延迟开销，但在端到端分割场景中，这一开销被整体性能提升所摊销。Table 9 进一步展示了不同输入分辨率和分组实现方式下的骨干级吞吐量与内存消耗，高分辨率下内存需求仍是需要关注的问题。

### 定性分析：从 ImageNet 预训练中涌现的分割能力

Figure 3 提供了最具说服力的定性证据：即使在**完全没有掩码监督**的 ImageNet 分类预训练下，SeNaTra 的早期层中自发涌现出超像素状结构，并在最后的密集分组层中被组合成语义连贯的区域。Figure 4 进一步展示了从图像-文本对比预训练中获得的零样本分割结果，模型在 Pascal VOC 验证图像上产生了与真实掩码高度一致的层次化分割，且未经过任何启发式后处理。

### 失败模式与局限性

1. **延迟开销**：分组层相比均匀下采样引入约 20–40% 的延迟，作为纯特征提取器使用时仍是一个额外负担。
2. **全景分割中的过度分割**：原生全景分割中出现的过度分割错误需要额外的细化步骤（如重新计算最终分组层的分配矩阵）来处理，增加了设计复杂性。
3. **高分辨率下的资源需求**：尽管通过稀疏 CUDA 内核进行了优化，在极高分辨率下的内存和计算需求仍未达到与均匀下采样完全相同的效率水平（Table 9 中部分配置出现 OOM）。

## 定位与知识库关联

### 核心问题与因果杠杆

现代视觉骨干网络（如 **Swin Transformer**、**NAT**）普遍采用均匀网格下采样（池化或跨步卷积），对所有空间位置一视同仁，不感知图像内容。这在下游分割任务中导致特征与物体边界错位，迫使解码器头（如 **UperNet**、**Mask2Former**）承担额外的补偿负担。SeNaTra 提出的因果杠杆是将均匀下采样替换为**内容感知的空间分组层**——一种可微的迭代聚类过程，学习将视觉令牌动态分配到语义一致的组中。连续分组操作构成从输入像素到最终令牌的马尔可夫链式映射，使分割掩码从骨干网络中自然涌现，无需专用分割头。

### 方法谱系定位

SeNaTra 处于**基于分组的视觉骨干**与**原生分割范式**的交汇点，其设计可沿以下谱系追溯：

**1. 标准分层骨干的继承与改造**

SeNaTra 继承了现代分层骨干（**Swin Transformer**、**NAT**）的四阶段架构范式——逐步降低空间分辨率并加倍通道数，初始阶段将输入分割为 4×4 补丁获取令牌嵌入。关键改造在于将阶段间的均匀下采样操作替换为空间分组层。消融实验（Table 3a）表明：将分组层全部替换为均匀下采样，导致 ADE20k 原生掩码 mIoU 从 49.7 骤降至 41.3（-8.4），证实分组层是性能的核心来源。

**2. 分组骨干方法的区别与改进**

与 **GroupViT** 采用密集交叉注意力进行分组不同，SeNaTra 的空间分组层在高分辨率阶段将交叉注意力限制在 3×3 局部窗口内，将复杂度从 $\mathcal{O}(L N^2 d)$ 降至 $\mathcal{O}(L N d)$，仅在最终阶段启用密集分组。这种设计兼顾了计算效率与全局语义聚合能力。

在分组层内部，SeNaTra 用**跳跃连接**替代了 K-means 可微变体（如 **Slot Attention**）中常用的 GRU 更新机制，带来 +4.8 mIoU 的提升并解决了训练稳定性问题（Table 3b）。此外，采用步长卷积初始化分组中心（而非可学习嵌入或高斯分布采样）被证明对性能至关重要——后者导致 2.5/3.2 mIoU 的性能下降。

**3. 分割范式的重新定义**

SeNaTra 提出了三种分割范式（Table 2c 概念图）：
- **原生分割**：通过骨干网络的分组分配矩阵和 2 层 MLP 直接生成像素级预测，无需专用分割头。
- **骨干+专用头**：将 SeNaTra 作为特征提取器，与 **Mask2Former** 等分割头结合，用分组分配矩阵替代标准双线性上采样。
- **传统范式**：标准骨干+UperNet/Mask2Former，依赖均匀上采样。

关键发现（Table 4）：在标准骨干（NAT）上添加像素解码器带来 +6.4 mIoU 的提升，但对 SeNaTra 的影响极小，说明分组层已经提供了丰富的空间信息，无需额外的解码器补偿。

### 适用边界与局限性

**1. 计算效率的权衡**

分组层相比均匀下采样引入了约 20-40% 的延迟开销（Table 8, 9）。尽管在端到端分割任务中被总体性能提升所摊销，但作为纯特征提取器使用时，这是一个不可忽视的额外负担。在高分辨率输入下，内存和计算需求仍需关注，尚未达到与均匀下采样完全相同的效率水平。

**2. 全景分割的过度分割问题**

原生全景分割中出现过度分割错误，需要额外的细化步骤（重新计算最终分组层的分配矩阵）来处理，增加了设计复杂性。SeNaTra-T 原生全景分割达到 49.2 PQ，虽已超过 **MaskFormer w/ Swin-T** 的 47.7 PQ，但与结合 M2F 头的 55.0 PQ 仍有差距。

**3. 预训练数据规模的限制**

零样本分割实验中，SeNaTra 仅使用 CC3M+CC12M（约 20M 图像-文本对）进行预训练，远小于 CLIP 的 400M 对。虽然已取得有竞争力的结果（SeNaTra-B 平均 31.9 mIoU，无后处理），但在更大规模数据上的潜力尚未被充分探索。

**4. 分组窗口的固定性**

当前分组层在局部阶段使用固定的 3×3 窗口，未根据特征图分辨率动态调整。这是否在所有阶段都是最优选择，仍需验证。

### 开放问题

1. **面向对象的预训练**：能否通过设计面向对象的预训练方案来进一步提高全景分割中实例级分组的质量？
2. **计算效率的极限优化**：未来的低层次 CUDA 优化能否将分组层的开销降低到与均匀下采样相当的水平？
3. **大规模预训练的潜力**：SeNaTra 的分组能力是否可以通过在更大规模（>400M）的图像-文本数据上进行预训练而进一步释放，从而在细粒度数据集上超越 CLIP 预训练的方法？
4. **动态窗口策略**：是否需要根据特征图分辨率动态调整分组窗口大小，以在不同阶段获得最优的分组粒度？
5. **分组层的理论理解**：分组分配矩阵构成的马尔可夫链是否具有更深层的理论性质（如收敛性、信息瓶颈），可以指导架构设计？

### 实验证据强度总结

| 证据类型 | 关键发现 | 置信度 |
|---------|---------|--------|
| 核心机制验证 | 分组层替换均匀下采样导致 -8.4 mIoU（Table 3a） | 高 |
| 设计选择验证 | 跳跃连接替代 GRU 带来 +4.8 mIoU（Table 3b） | 高 |
| 零样本分割 | SeNaTra-B 无后处理平均 31.9 mIoU，超越依赖 CRF/PAMR 的方法（Table 1） | 高 |
| 涌现性质 | ImageNet 分类预训练下自发涌现超像素状和语义区域（Figure 3） | 高 |
| 分割头独立性 | 像素解码器对 SeNaTra 影响极小，证明分组层已提供丰富空间信息（Table 4） | 高 |
| 效率权衡 | 分组层引入 20-40% 延迟开销，但在端到端分割中被性能提升摊销（Table 8, 9） | 中（需更多硬件环境验证） |
| 全景分割 | 原生全景分割存在过度分割，需额外细化步骤 | 中（需更系统的错误分析） |

## 原文 PDF

![[paperPDFs/NEURIPS_2025/Native_Segmentation_Vision_Transformers.pdf]]
