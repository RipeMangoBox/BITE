---
title: "MICDrop: Masking Image and Depth Features via Complementary Dropout for Domain-Adaptive Semantic Segmentation"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/MICDrop_Masking_Image_and_Depth_Features_via_Complementary_Dropout_for_Domain_Adaptive_Semantic_Segmentation.pdf
project_link: null
code_link: https://github.com/ly-muc/MICDrop
aliases:
- MICDrop
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入深度估计作为互补几何信息，并通过互补掩码（Complementary Dropout）策略强制跨模态特征学习，结合全局深度引导交叉注意力和局部自注意力融合模块，增强边界感知和一致性。"
primary_logic: "深度不连续性常与语义分割边界重合，且深度在大物体内部平滑一致。通过以互补方式遮盖RGB和深度特征图，迫使网络利用另一模态重建缺失信息，可有效防止模型过度依赖单一模态，显著提升细粒度分割和抗过分割能力。"
claims:
- "在GTA→Cityscapes基准上，MICDrop将DAFormer的mIoU从68.3提升至70.1（+1.8），将HRDA从73.8提升至74.8（+1.0），并在MIC(HRDA)上取得75.9（+0.7），刷新SOTA。"
- "互补掩码消融实验显示，采用跨所有层级的互补掩码相比未掩码带来+1.0 mIoU增益，而独立按层掩码导致性能下降0.4 mIoU，证明协同掩码的必要性。"
- "MICDrop在边界IoU（Boundary IoU）上比标准IoU提升更显著（+1.6 vs +0.7），直接证明深度信息改善了精细结构分割。"
- "GTA→Cityscapes 上 mIoU = MICDrop (DAFormer) 70.1"
---

# MICDrop: Masking Image and Depth Features via Complementary Dropout for Domain-Adaptive Semantic Segmentation

> [!tip] 核心洞察
> 深度不连续性常与语义分割边界重合，且深度在大物体内部平滑一致。通过以互补方式遮盖RGB和深度特征图，迫使网络利用另一模态重建缺失信息，可有效防止模型过度依赖单一模态，显著提升细粒度分割和抗过分割能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MICDrop：通过互补Dropout掩码图像与深度特征实现域自适应语义分割 |
| 英文题名 | MICDrop: Masking Image and Depth Features via Complementary Dropout for Domain-Adaptive Semantic Segmentation |
| 会议/期刊 | ECCV 2024 |
| Links | [paper](https://arxiv.org/abs/2408.16478) · [GitHub](https://github.com/ly-muc/MICDrop) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MICDrop |
| Dataset | GTA→Cityscapes |

> [!tip] 效果简介
> - GTA→Cityscapes 上，mIoU 为 MICDrop (DAFormer) 70.1，对比 DAFormer 68.3，变化 +1.8。
> - GTA→Cityscapes 上，mIoU 为 MICDrop (HRDA) 74.8，对比 HRDA 73.8，变化 +1.0。
> - GTA→Cityscapes 上，mIoU 为 MICDrop (MIC) 71.8，对比 MIC (DAFormer) 70.6，变化 +1.2。

## 概要

**问题瓶颈**：当前域自适应语义分割方法在细致结构（如电线杆、交通标志）和外观模糊物体的分割中表现不佳，容易发生过分割。RGB特征对域差异敏感，无法充分利用深度几何信息提供的精确边界。

**核心方案**：MICDrop 提出一种即插即用的跨模态学习范式，通过**互补Dropout掩码策略**强制RGB与深度特征进行跨模态信息重建，并设计**全局深度引导交叉注意力**与**局部自注意力融合模块**，将深度估计作为互补几何信息融入分割流程。

**方法定位**：MICDrop 作为轻量级插件，可无缝集成到现有UDA方法（如 **DAFormer** (Hoyer et al., CVPR 2022)、**HRDA** (Hoyer et al., ECCV 2022)、**MIC** (Hoyer et al., ECCV 2022)）中，仅需冻结预训练RGB编码器、训练轻量深度编码器（MiT-B3）与融合模块，即可在单张12 GB GPU上11小时内完成训练。

**主要结果**：
- 在 GTA→Cityscapes 基准上，MICDrop 将 DAFormer 的 mIoU 从 68.3 提升至 70.1（+1.8），将 HRDA 从 73.8 提升至 74.8（+1.0），并在 MIC(HRDA) 上取得 75.9（+0.7），刷新SOTA（Tab. 1）。
- 在 SYNTHIA→Cityscapes 上，MICDrop(DAFormer) 带来 +3.3 mIoU 的显著增益（55.5 vs 52.2）。
- 边界IoU分析表明，MICDrop 对精细结构边界的提升（+1.6）远大于标准IoU（+0.7），直接验证了深度信息对边界感知的增强作用（Tab. 2）。
- 互补掩码消融确认：跨层级一致互补掩码带来 +1.0 mIoU，而独立按层掩码反而下降 0.4 mIoU（Tab. 3a）。



语义分割是场景理解的核心任务，而无监督域自适应（Unsupervised Domain Adaptation, UDA）旨在将源域（如合成数据）上训练的模型迁移到未标注的目标域（如真实街景）。当前UDA方法在细致结构（如杆、交通标志）和外观模糊物体的分割中表现不佳，容易出现过分割问题——即将同一对象错误地切割为多个碎片。这一瓶颈的根源在于，RGB特征对光照、纹理等域差异高度敏感，无法充分利用几何信息提供的精确边界线索。

深度估计为语义分割提供了互补的几何先验：深度不连续性常与语义分割边界重合，而深度在大物体内部平滑一致。然而，现有方法对深度信息的利用存在两个关键缺口。其一，多数UDA方法将深度仅作为辅助任务（如多任务学习），而非直接参与特征表示学习，导致几何信息未能有效注入分割决策。其二，简单的特征相加或拼接无法充分挖掘跨模态互补性，模型容易过度依赖某一模态（通常是RGB），在RGB特征失效时缺乏鲁棒的几何支撑。

针对上述缺口，本文提出**MICDrop**，其核心动机是：通过互补掩码策略强制网络同时利用RGB和深度两种模态，防止对单一模态的过度依赖。具体而言，MICDrop在训练时对RGB和深度特征图施加互补的块级Dropout——当RGB的某块特征被遮盖时，对应位置的深度特征保持可见，反之亦然。这一设计迫使网络在缺失某一模态信息时，必须利用另一模态进行重建，从而学习到真正跨模态的联合表示。结合全局深度引导交叉注意力与局部自注意力融合模块，MICDrop能够同时捕获大物体内部的深度一致性（抑制过分割）和边界处的深度不连续性（提升细粒度分割精度）。



## 核心方法与创新机理

MICDrop的核心创新在于通过**互补Dropout掩码策略**与**深度引导的全局-局部特征融合模块**，将单目深度估计作为互补几何线索引入域自适应语义分割，从而解决现有UDA方法在细致结构（如杆、交通标志）和外观模糊物体上的过分割问题。

### 创新点一：互补Dropout掩码策略

现有UDA方法通常仅依赖RGB特征，对域差异敏感，难以捕获精确边界。MICDrop提出**跨模态互补块级Dropout**：在训练时对RGB与深度编码器输出的多尺度特征图施加互补的二值掩码——若某区域遮盖RGB特征，则对应深度特征保持可见，反之亦然（Eq. 4-5）。这一策略迫使网络在任一模态信息缺失时利用另一模态进行重建，从而防止模型过度依赖单一模态，强制学习跨模态联合表示。

关键设计细节：
- **跨层级一致掩码**：所有特征金字塔层级使用相同的掩码模式，消融实验表明独立按层掩码会导致性能下降0.4 mIoU，而跨层一致的互补掩码带来+1.0 mIoU增益（Tab. 3a）。
- **动态掩码比例调度**：训练初期保留较高比例的深度特征以加速深度编码器收敛，随后逐步调整至更均衡的掩码比例，动态调度优于固定比例（Fig. S2）。
- **仅训练时使用**：掩码仅在训练阶段应用，推理时无需额外计算开销。

### 创新点二：深度引导的全局-局部特征融合模块

为有效利用深度信息，MICDrop设计了**many-to-one**的特征融合模块，将深度特征单向细化RGB特征，而非简单的多模态相加或拼接：

- **全局深度引导交叉注意力**（Global Depth-Guided Cross-Attention）：以深度特征生成查询（Q）与键（K），RGB特征作为值（V），通过缩放点积注意力实现深度相似度引导的全局RGB特征聚合（Eq. 1）。该机制利用深度在大物体内部的平滑一致性，增强分割的区域一致性。

- **局部自注意力**（Local Self-Attention）：通过Sigmoid门控的3×3卷积对深度特征进行逐元素调制（Eq. 2），无需池化操作即可捕获深度不连续性。由于深度不连续常与语义边界重合，该模块直接增强边界区域的判别力。

- **残差融合**（Residual Feature Fusion）：将全局与局部深度聚合特征拼接后经卷积、批归一化、ReLU激活，再与原始RGB特征残差相加（Eq. 3），在引入深度信息的同时保留预训练RGB表示的稳定性。

### 创新点三：冻结RGB编码器的轻量级插件设计

MICDrop冻结预训练的RGB编码器参数，仅训练轻量级深度编码器（MiT-B3）、融合模块和解码头。这一设计不仅将训练时间控制在单张GTX Titan X（12 GB）上约11小时，还轻微提升了性能（69.1 vs 68.7 mIoU），避免了域自适应训练中的表示漂移问题（Tab. S1）。该方法可作为插件无缝集成到**DAFormer**（Hoyer et al., CVPR 2022）、**HRDA**（Hoyer et al., ECCV 2022）、**MIC**（Hoyer et al., ECCV 2022）等多种UDA架构中。

### 创新效果验证

在GTA→Cityscapes基准上，MICDrop将DAFormer的mIoU从68.3提升至70.1（+1.8），将HRDA从73.8提升至74.8（+1.0），并在MIC（HRDA）上取得75.9（+0.7），刷新SOTA（Tab. 1）。边界IoU分析进一步证实，MICDrop在边界IoU上的提升（+1.6）显著高于标准IoU（+0.7），直接验证了深度信息对精细结构分割的改善（Tab. 2）。



MICDrop 是一种即插即用的跨模态域自适应语义分割框架，其核心思想是通过互补掩码策略强制网络同时利用 RGB 与深度几何信息，从而解决现有 UDA 方法对细致结构过分割和对域差异敏感的问题。整体架构由四个关键模块串联构成：**冻结的 RGB 编码器**、**轻量级深度编码器**、**跨模态特征融合模块**以及 **DAFormer 解码头**，如图 Fig. 2 所示。

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2408_16478/figures/002_Figure_2.jpg]]
*Figure 2: Method overview. Our proposed architecture is visualized on the left side. We use a light-weight hierarchical depth encoder and process the features in our proposed cross-modal feature fusion module. On the right side, we illustrate our training pipeline, in which source and target images are fed through the student encoders. Then, our proposed cross-modality complementary dropout is applied to the corresponding features on each feature resolution. Finally, we feed them through our fusion block, followed by the decoder, to make a final prediction*

### 双编码器特征提取

框架采用非对称双编码器设计。RGB 分支沿用预训练的 Segformer 层级编码器，其参数在训练期间**完全冻结**，以保持预训练表示的稳定性并避免表示漂移。深度分支则部署一个基于 MiT-B3 的轻量级层级编码器，从单目深度估计结果中提取多尺度深度特征。两个编码器在相同的特征金字塔层级上输出对应分辨率的特征图，为后续融合提供对齐的多模态表示。

### 跨模态特征融合模块

融合模块（Fig. 3）是连接双编码器与解码头之间的核心桥梁，采用“全局-局部”双支路设计，将深度几何信息单向注入 RGB 特征流：

- **全局深度引导交叉注意力（Global Depth-Guided Cross-Attention）**：以深度特征生成查询 $\mathbf{Q}_{\mathrm{depth}}$ 与键 $\mathbf{K}_{\mathrm{depth}}$，RGB 特征作为值 $\mathbf{V}_{\mathrm{rgb}}$，通过缩放点积注意力实现深度相似度引导的全局 RGB 特征聚合：

$$\mathbf{F}_{\mathrm{global}}^{i} = \mathrm{softmax}\left(\frac{\mathbf{Q}_{\mathrm{depth}}\mathbf{K}_{\mathrm{depth}}^{T}}{\sqrt{d_{k}}}\right)\mathbf{V}_{\mathrm{rgb}}$$

该机制利用深度在大物体内部平滑一致的特性，捕获大范围上下文一致性。

- **局部自注意力（Local Self-Attention）**：通过 Sigmoid 门控的 3×3 卷积对深度特征进行逐元素调制，无需池化操作，从而保留深度不连续性提供的强边界线索：

$$\mathbf{F}_{\mathrm{local}}^{i} = \sigma\left(\mathrm{Conv}_{3\times3}\left(\mathbf{F}_{\mathrm{depth}}^{i}\right)\right) \odot \mathrm{Conv}_{3\times3}\left(\mathbf{F}_{\mathrm{depth}}^{i}\right)$$

- **残差特征融合（Residual Feature Fusion）**：将全局与局部深度聚合特征拼接后，经卷积、批归一化与 ReLU 激活，再与原始 RGB 特征相加，形成残差连接：

$$\mathbf{F}_{\mathrm{refined}}^{i} = \mathbf{F}_{\mathrm{rgb}}^{i} + \mathrm{ReLU}(\mathrm{BN}(\mathbf{Conv}(\mathbf{F}_{\mathrm{global}}^{i} || \mathbf{F}_{\mathrm{local}}^{i})))$$

融合后的细化特征 $\mathbf{F}_{\mathrm{refined}}^{i}$ 送入 DAFormer 的 Transformer 解码头，输出最终分割预测。

### 互补 Dropout 掩码策略

训练阶段，框架在双编码器输出的多尺度特征图上施加**互补块级 Dropout**（Complementary Dropout），这是 MICDrop 实现跨模态强制的关键正则化手段。具体而言，对每个特征金字塔层级，生成块状二值掩码：

$$\mathbf{M}_{\mathrm{rgb}}(u,v) = [\gamma > m_{r}^{t}], \quad \gamma \sim \mathrm{Uniform}(0,1)$$

$$\mathbf{M}_{\mathrm{depth}}(u,v) = 1 - \mathbf{M}_{\mathrm{rgb}}(u,v)$$

其中 $m_{r}^{t}$ 为动态掩码比例，训练初期保留较高比例的深度特征以加速深度编码器收敛，随后逐步调整掩码比例以平衡双模态利用。RGB 与深度特征的掩码严格互补，迫使网络在某一模态被遮盖时依赖另一模态重建缺失信息。该掩码**仅在训练时应用**，推理阶段移除，所有特征完整通过融合模块。

### 训练流程

源域和目标域图像分别通过学生编码器，在各特征分辨率上施加互补掩码后，经融合模块与解码头生成预测。整体训练沿用 DAFormer 的自训练范式与损失函数，深度编码器、融合模块和解码头参与参数更新，RGB 编码器保持冻结。MICDrop 在单张 GTX Titan X（12 GB）上约 11 小时即可完成训练，体现了其作为插件模块的轻量高效特性。



MICDrop 的核心由两个可插拔模块构成：**跨模态特征融合模块**（Cross-Modal Feature Fusion）和**互补Dropout掩码模块**（Complementary Dropout Masking）。前者将深度几何信息注入RGB特征表示，后者在训练时强制网络同时依赖两种模态，防止退化为单模态捷径。

### 跨模态特征融合模块

该模块在每个特征金字塔层级独立运行，包含三个子组件：全局深度引导交叉注意力、局部自注意力和残差特征融合。其设计动机源于深度信息的双重特性——大物体内部深度平滑一致，而物体边界处深度存在不连续性，这两种信号分别由全局和局部注意力捕获。

**全局深度引导交叉注意力** 以深度特征生成查询（Query）和键（Key），以RGB特征作为值（Value），通过缩放点积注意力实现深度引导的全局RGB特征聚合：

$$\mathbf{F}_{\mathrm{global}}^{i} = \mathrm{softmax}\left(\frac{\mathbf{Q}_{\mathrm{depth}}\mathbf{K}_{\mathrm{depth}}^{T}}{\sqrt{d_{k}}}\right)\mathbf{V}_{\mathrm{rgb}}$$

其中 $\mathbf{Q}_{\mathrm{depth}}$ 和 $\mathbf{K}_{\mathrm{depth}}$ 由深度特征经线性投影得到，$\mathbf{V}_{\mathrm{rgb}}$ 由RGB特征投影得到，$d_k$ 为键的维度。该操作使具有相似深度值的空间位置在RGB特征空间中相互聚合，从而增强大物体内部的一致性。

**局部自注意力** 采用Sigmoid门控的3×3卷积直接作用于深度特征图，捕获深度不连续性以增强边界：

$$\mathbf{F}_{\mathrm{local}}^{i} = \sigma\left(\mathrm{Conv}_{3\times3}\left(\mathbf{F}_{\mathrm{depth}}^{i}\right)\right) \odot \mathrm{Conv}_{3\times3}\left(\mathbf{F}_{\mathrm{depth}}^{i}\right)$$

其中 $\sigma(\cdot)$ 为Sigmoid函数，$\odot$ 表示逐元素乘法。该模块不使用任何池化操作，以保留边界区域的精细深度不连续信号——这些不连续性常与语义分割边界高度重合（Sec. 3.1, Fig. 3）。

**残差特征融合** 将全局和局部深度聚合特征拼接后经卷积、批归一化、ReLU激活，再与原始RGB特征相加：

$$\mathbf{F}_{\mathrm{refined}}^{i} = \mathbf{F}_{\mathrm{rgb}}^{i} + \mathrm{ReLU}(\mathrm{BN}(\mathrm{Conv}(\mathbf{F}_{\mathrm{global}}^{i} || \mathbf{F}_{\mathrm{local}}^{i})))$$

其中 $||$ 表示通道维拼接。残差设计确保深度信息作为RGB特征的补充而非替代，避免破坏预训练RGB编码器的语义表示。消融实验（Tab. 3b）证实，全局+局部融合组合达到70.1 mIoU，优于简单相加、CMX交叉注意力或单独使用任一模块，且单独使用全局模块会导致训练不稳定。

### 互补Dropout掩码模块

该模块仅在训练时生效，对每个特征金字塔层级的多尺度特征图应用块状二值掩码。RGB特征掩码 $\mathbf{M}_{\mathrm{rgb}}$ 基于动态掩码比例 $m_r^t$ 生成：

$$\mathbf{M}_{\mathrm{rgb}}(u,v) = [\gamma > m_{r}^{t}], \quad \gamma \sim \mathrm{Uniform}(0,1)$$

深度特征掩码 $\mathbf{M}_{\mathrm{depth}}$ 为RGB掩码的互补：

$$\mathbf{M}_{\mathrm{depth}}(u,v) = 1 - \mathbf{M}_{\mathrm{rgb}}(u,v)$$

掩码比例 $m_r^t$ 采用动态线性调度：训练初期保留较高比例的深度特征以加速深度编码器训练并提升特征质量，随着训练推进逐渐调整至均衡比例（Sec. 4, Fig. S2）。掩码块大小设为64（相对于输入图像）时取得最优70.1 mIoU，较大的块迫使网络必须利用另一模态重建被遮盖区域的信息，从而验证了跨模态学习的核心假设（Tab. S3）。

消融实验（Tab. 3a）揭示了该策略的关键设计约束：跨所有层级的互补掩码相比无掩码基线带来+1.0 mIoU增益，而独立按层级掩码（即不同层级掩码模式不一致）导致性能下降0.4 mIoU。这证明跨层级一致的互补掩码对于有效跨模态特征学习至关重要。推理阶段不应用任何掩码，融合模块直接处理完整的RGB和深度特征。



## 实验与关键发现

### 核心实验设置

MICDrop 采用冻结的预训练 RGB 编码器（MiT-B5）与轻量级深度编码器（MiT-B3）双流架构，仅在训练阶段施加互补掩码，推理时移除所有掩码操作。训练在单张 GTX Titan X GPU（12 GB）上约 11 小时完成。掩码比例采用动态线性调度：训练初期保留较高比例的深度特征以加速深度编码器收敛，随训练推进逐步均衡两模态的掩码比例。

### 主实验结果

**GTA→Cityscapes 基准。** MICDrop 作为即插即用模块，在四种代表性 UDA 方法上均取得一致提升（Table 1）：
- **DAFormer**（Hoyer et al., CVPR 2022）：mIoU 从 68.3 提升至 70.1（**+1.8**）
- **HRDA**（Hoyer et al., ECCV 2022）：mIoU 从 73.8 提升至 74.8（**+1.0**）
- **MIC**（Hoyer et al., ECCV 2022）：mIoU 从 70.6 提升至 71.8（**+1.2**）
- **MIC（HRDA）**：mIoU 从 74.8 提升至 **75.9**（**+0.7**），刷新该基准最优结果

值得注意的是，当使用 ResNet-101 作为 DAFormer 的 backbone 时，MICDrop 带来 **+4.1 mIoU** 的增益，表明深度几何信息对较小编码器架构的补充作用更为显著。

**SYNTHIA→Cityscapes 基准。** MICDrop（DAFormer）将 mIoU 从 52.2 提升至 55.5（**+3.3**），在更大的域差异下展现出更强的鲁棒性。

### 边界分割专项分析

MICDrop 对精细结构的分割改善在边界 IoU（Boundary IoU）指标上尤为突出。在 GTA→Cityscapes 上，边界 IoU 提升 **+1.6**，远超标准 mIoU 的提升幅度（+0.7）（Table 2）。这一结果直接验证了核心假设：深度不连续性与语义边界高度重合，局部自注意力模块通过捕获深度图中的不连续区域，为杆、交通标志等细长结构提供了精确的边界定位线索。

### 消融实验

**互补掩码策略（Table 3a）。** 跨所有特征层级的互补掩码相比无掩码基线带来 **+1.0 mIoU** 的显著增益。若改为各层级独立随机掩码（非互补），性能反而下降 **0.4 mIoU**，证明强制跨模态互补学习——而非单纯的 dropout 正则化——是性能提升的关键机制。

**特征融合模块（Table 3b）。** 全局深度引导交叉注意力与局部自注意力的组合（Local+Global）达到 70.1 mIoU，优于以下替代方案：
- 简单相加融合
- CMX 交叉注意力融合
- 单独使用全局或局部模块

其中，单独使用全局模块会导致训练不稳定，而局部模块单独使用即可提供大部分增益，表明深度不连续性提供的边界线索是融合模块中最关键的信息源。

**冻结 RGB 编码器（Table S1）。** 冻结预训练 RGB 编码器不仅将训练吞吐量提升约 40%、显存占用降低约 30%，还带来轻微的性能提升（69.1 vs 68.7 mIoU）。类别级分析（Fig. S1）进一步显示，冻结 backbone 减少了各类别间性能的剧烈波动，表明其有效防止了源域预训练表示的灾难性遗忘。

**掩码超参数。** 动态线性掩码比例调度优于任意固定比例（Fig. S2）。掩码块大小设置为 64（相对于输入图像分辨率）时取得最佳 70.1 mIoU（Table S3），较大的掩码块强制网络利用另一模态重建更大区域的信息，验证了交叉模态学习的核心假设。

### 失败模式与局限性

尽管整体增益显著，MICDrop 存在以下已知失灵场景：

1. **错误标签传播。** 深度线索偶尔会继承并放大预训练 RGB 网络的系统性错误分类。典型失败案例包括将建筑物误分为栅栏（fence），此时深度图中大面积平滑区域的一致性反而加剧了错误标签的扩散。该问题源于深度编码器接收的监督信号完全来自 RGB 分支的伪标签，缺乏独立的深度真值约束。

2. **超参数敏感性。** 掩码块大小、掩码比例调度、训练批次中源域/目标域图像的构成比例（Table S2）需针对特定数据集进行适度调优。论文显示方法对这些参数在合理范围内具有鲁棒性，但极端取值会导致性能退化。

3. **深度估计质量依赖。** 方法假设输入的深度估计具备合理质量。在深度估计本身存在严重伪影的场景（如透明表面、镜面反射区域），深度不连续性可能与语义边界产生错误对应，从而引入噪声。

### 补充图表

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2408_16478/figures/001_Figure_1.jpg]]
*Figure 1: b) Qualitative Examples Fig. 1: Previous UDA methods such as MIC [23] struggle with the segmentation of fine structures (top row) and oversegmentation of difficult objects (bottom row). Therefore, we propose MICDrop to improve semantic segmentation UDA with depth estimates, which can capture fine structures and are consistent within object boundaries. We apply MICDrop to four different methods on the GTA→Cityscapes benchmark and show consistent improvements*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2408_16478/figures/004_Table_1.jpg]]
*Table 1: Comparison of MICDrop with state-of-the-art UDA methods. The performance is reported as IoU in %. We group methods based on ResNet [15] and Segformer [57] backbones. † denotes results obtained with a Segformer backbone from [22]. On both GTA and SYNTHIA, MICDrop achieves consistent improvements, demonstrating the effectiveness of our masking strategy and fusion module*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2408_16478/figures/007_Table.jpg]]
*Table: (a) Dropout strategy ablation*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2408_16478/figures/008_Table.jpg]]
*Table: (b) Feature Fusion ablation*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2408_16478/figures/009_Table.jpg]]
*Table: S1: Effect of freezing the RGB encoder. The tables highlight the benefits gained from freezing the RGB encoder. This process notably decreases resource usage while also yielding slight performance improvements*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2408_16478/figures/011_Table.jpg]]
*Table: S2: Detailed analysis of the choice of image batches used for loss computation. The chosen composition of image batches used in the paper is highlighted in green*

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2408_16478/figures/013_Table.jpg]]

![[assets/figures/papers/paper_list_l19_https_arxiv_org_abs_2408_16478/figures/010_Figure.jpg]]
*Figure: Fig. S1: Classwise performance. This figure highlights not only improved average performance but also a reduction of strong deviations in classwise performances when using a frozen backbone. The dotted checkpoint line indicates the model’s performance at its initialization with pretrained weights*



## 定位与知识库关联

### 1. 在域自适应语义分割中的定位

MICDrop 属于**基于深度几何线索的多模态域自适应语义分割**方法，其核心贡献在于提出了一种即插即用的跨模态互补学习机制。与现有工作相比，MICDrop 的方法论定位可从以下几个维度加以界定：

**与单模态UDA方法的关系。** 当前域自适应语义分割的主流范式以纯RGB输入为基础，通过输出空间对齐、熵最小化或跨域混合增强来缩小域差异。代表性工作包括 **AdaptSeg**（Tsai et al., CVPR 2018）的输出空间对抗对齐、**ADVENT**（Vu et al., CVPR 2019）的熵最小化、**DACS**（Tranheden et al., WACV 2021）的跨域类混合采样，以及 **ProDA**（Zhang et al., CVPR 2021）的原型伪标签去噪。这些方法在RGB特征空间内操作，对域差异敏感，且在细致结构（如杆、交通标志）上容易出现边界模糊和过分割。MICDrop 通过引入深度估计作为互补模态，从根本上扩展了可用信息源。

**与多模态UDA方法的关系。** **CorDA**（Wang et al., ICCV 2021）是较早将自监督深度估计引入域自适应的尝试，但其将深度作为辅助任务进行多任务学习，而非直接用于特征级融合。MICDrop 的差异在于：(1) 采用轻量级深度编码器（MiT-B3）进行单向深度到RGB的特征细化（many-to-one），而非对称的双向融合；(2) 通过全局深度引导交叉注意力和局部自注意力实现结构感知的特征聚合，直接利用深度不连续性与语义边界的天然对应关系。

**与掩码建模UDA方法的关系。** **MIC**（Hoyer et al., ECCV 2022）利用掩码图像建模增强上下文推理能力，但其掩码仅作用于RGB模态。MICDrop 的互补掩码策略（Complementary Dropout）将掩码从单模态扩展为跨模态的协同机制——RGB与深度特征以互补方式被块级遮盖，迫使网络在缺失一种模态时依赖另一种模态重建信息。这一设计在方法论上区别于 MIC 的单模态掩码范式，且实验证明两者具有互补性：将 MICDrop 叠加于 MIC 可进一步带来 +1.2 mIoU 的提升（Tab. 1）。

**与基线架构的关系。** MICDrop 以 **DAFormer**（Hoyer et al., CVPR 2022）和 **HRDA**（Hoyer et al., ECCV 2022）为主要插件载体。DAFormer 提供了基于 Segformer 的Transformer UDA架构，HRDA 则通过多分辨率特征融合提升细节分割能力。MICDrop 在冻结预训练RGB编码器的前提下，仅训练深度编码器、融合模块和解码头，实现了即插即用的集成方式。这一设计使其与现有UDA方法形成松耦合关系，而非替代关系。

### 2. 适用边界与关键设计约束

**适用条件。** MICDrop 假设目标域场景中存在可利用的深度估计信号。对于缺乏几何结构的场景（如纯纹理表面、远距离平面），深度线索的信息增益可能有限。此外，方法的有效性依赖于预训练深度估计器在目标域上的泛化能力——论文中使用的深度估计器在 GTA→Cityscapes 和 SYNTHIA→Cityscapes 等标准自动驾驶场景适配基准上表现良好，但在更极端的域差异下（如从合成室内到真实室外）需要额外验证。

**冻结RGB编码器的必要性。** 消融实验（Tab. S1）表明，冻结预训练RGB编码器不仅提升训练效率（吞吐量提高，显存减少），还轻微提升性能（69.1 vs 68.7 mIoU）。这一设计约束源于：在域自适应训练中，RGB编码器的表示漂移可能破坏预训练特征质量，而深度模态的引入恰好弥补了RGB特征在目标域上的不足，无需对RGB编码器进行微调。

**掩码策略的协同依赖性。** 消融实验（Tab. 3a）揭示了互补掩码的关键约束：跨所有层级的互补掩码相比未掩码带来 +1.0 mIoU 增益，而独立按层掩码（各层独立决定掩码区域）导致性能下降 0.4 mIoU。这表明跨层级一致的互补掩码是迫使网络学习跨模态表示的必要条件，而非简单的正则化手段。

### 3. 已知局限与失效模式

**标签错误传播。** 深度线索偶尔会继承并放大预训练RGB网络的错误分类。论文明确指出，在极少数情况下，深度信息可能将建筑物误分为栅栏，导致大范围标签错误传播。这一失效模式源于深度特征与RGB特征的联合学习机制——当RGB编码器对某一区域产生高置信度错误预测时，深度引导的全局注意力可能将这一错误扩散到具有相似深度特征的区域。

**超参数敏感性。** 方法的掩码块大小、掩码比例调度、批次构成等超参数可能需要针对新数据集进行调优。消融实验（Tab. S3）显示，掩码块大小为64（相对于输入图像）时取得最佳效果（70.1 mIoU），较大块强制网络使用另一模态重建，验证了交叉模态学习假设。但论文也承认，在合理范围内性能保持提升，表明方法对适度超参数偏差具有鲁棒性。

**训练与推理的不对称性。** 互补掩码仅在训练时使用，推理时所有特征均参与计算。这一设计虽然简化了推理流程，但也意味着训练和推理时的特征分布存在差异，可能影响模型在极端域偏移下的泛化稳定性。

### 4. 开放问题

1. **自适应掩码调度。** 当前采用动态线性掩码比例调度（Fig. S2），在不同比例下均取得最佳性能。然而，如何针对不同的域差异程度自动确定最优掩码调度策略仍是一个开放问题。域差异的度量（如特征分布距离、类别分布偏移）与掩码策略之间的定量关系尚未建立。

2. **块大小的跨层级机制。** 掩码块大小在跨模态学习中的具体影响机制尚不完全清晰。不同特征金字塔层级的感受野不同，块大小与层级之间的最优匹配关系值得进一步探索。当前方法在所有层级使用统一的块大小，这可能不是最优方案。

3. **跨模态泛化能力。** 互补掩码策略能否泛化到其他模态（如热成像、激光雷达点云）并取得类似的交叉模态学习增益，是方法普适性的关键验证方向。深度与RGB之间的几何-外观互补关系在其他模态组合中可能呈现不同的特性。

4. **与自训练方法的深度结合。** MICDrop 当前以特征级融合和掩码正则化为核心，与基于伪标签的自训练方法（如 ProDA、HRDA 的伪标签机制）形成松耦合。如何将互补掩码策略与伪标签质量评估、置信度加权等机制深度结合，可能进一步释放跨模态学习的潜力。



## 原文 PDF

![[paperPDFs/ECCV_2024/MICDrop_Masking_Image_and_Depth_Features_via_Complementary_Dropout_for_Domain_Adaptive_Semantic_Segmentation.pdf]]
