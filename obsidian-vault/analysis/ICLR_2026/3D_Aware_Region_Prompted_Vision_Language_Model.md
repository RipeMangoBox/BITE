---
title: "3D Aware Region Prompted Vision Language Model"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/3D_Aware_Region_Prompted_Vision_Language_Model.pdf
aliases:
- S3SR3
- 3ARPVLM
- "SR-3D (Spatial Region 3D)"
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将3D位置嵌入直接集成到基础视觉语言模型的视觉表示中，并通过动态分块（dynamic tiling）的区域提取器，在共享的规范化3D坐标空间中统一单视图和多视图输入。"
primary_logic: "通过将单视图图像的深度估计结果反投影到规范化3D空间，并将该3D位置嵌入与视觉令牌融合，可以在不牺牲2D基础模型通用能力的前提下，显著提升其空间推理能力。这种统一的表示空间使得仅在2D单视图数据上训练的区域表示能够零样本泛化到多视图3D场景。"
claims:
- "SR-3D在BLINK_Depth基准上达到90.3%准确率，远超之前最好的开源模型SpatialRGPT-8B（87.9%）和GPT-4V-Turbo（66.9%）。"
- "SR-3D在COCO-2017区域级分类上达到78.0 mAP和88.6%准确率，显著优于SpatialRGPT-8B（72.9 mAP, 82.9%）。"
- "SR-3D在Scan2Cap、ScanQA和SQA3D三个3D场景理解基准上均达到最先进水平，例如ScanQA Cider达到109.3，SQA3D EM达到62.2。"
- "SR-3D在SR-3D-Bench区域级空间理解上以83.3平均准确率超越所有基线，包括GPT-4o（73.6）和LLaVA-3D（79.5）。"
---

# 3D Aware Region Prompted Vision Language Model

> [!tip] 核心洞察
> 通过将单视图图像的深度估计结果反投影到规范化3D空间，并将该3D位置嵌入与视觉令牌融合，可以在不牺牲2D基础模型通用能力的前提下，显著提升其空间推理能力。这种统一的表示空间使得仅在2D单视图数据上训练的区域表示能够零样本泛化到多视图3D场景。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 三维感知区域提示视觉语言模型 |
| 英文题名 | 3D Aware Region Prompted Vision Language Model |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=GTpf2NuwtR) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | SR-3D (Spatial Region 3D) |
| Dataset | BLINK_Depth, COCO-2017 region-level classification, Scan2Cap |

> [!tip] 效果简介
> - BLINK_Depth 上，Acc. (%) 为 90.3，对比 87.9 (SpatialRGPT-8B)，变化 +2.4。
> - COCO-2017 region-level classification 上，mAP (↑) 为 78.0，对比 72.9 (SpatialRGPT-8B)，变化 +5.1。
> - COCO-2017 region-level classification 上，Acc. (%) 为 88.6，对比 82.9 (SpatialRGPT-8B)，变化 +5.7。

## 概述

SR-3D（Spatial Region 3D）提出了一种将3D空间感知注入基础视觉语言模型（VLM）的统一方法。其核心瓶颈在于：现有2D VLM缺乏3D空间推理能力，而3D VLM又难以利用2D基础模型的先验知识，且受限于有限的3D训练数据。此外，在多视角场景中通过文本指定空间关系（如同类物体）极为繁琐。

SR-3D的核心因果机制是：**将3D位置嵌入直接集成到基础VLM的视觉表示中**。具体而言，对单视图图像使用现成的深度估计器（DepthAnythingV2）估计深度图，并通过反投影得到规范化3D坐标，经正弦函数和可学习MLP编码后加到视觉令牌上。同时，引入**动态分块（tile-then-stitch）区域提取器**，在分块后的高分辨率特征上进行掩码池化，无需后处理上采样。该设计的关键洞察在于：通过共享的规范化3D坐标空间统一单视图和多视图输入，使得仅在2D单视图数据上训练的区域表示能够零样本泛化到多视图3D场景。

方法定位上，SR-3D初始化自NVILA-Lite-8B，视觉编码器冻结，微调3D位置编码模块、投影器和Qwen-2-7B大语言模型。单视图和多视图模型共享同一架构，仅在训练数据上区分。

主要结果方面，SR-3D在多个基准上达到领先水平：
- **深度感知**：BLINK_Depth准确率90.3%，超越SpatialRGPT-8B（87.9%）和GPT-4V-Turbo（66.9%）。
- **区域级理解**：COCO-2017区域分类mAP 78.0（+5.1）、准确率88.6%（+5.7）；在自建SR-3D-Bench上平均83.3，超越GPT-4o（73.6）和LLaVA-3D（79.5）。
- **3D场景理解**：Scan2Cap Cider 97.9、ScanQA Cider 109.3、SQA3D EM 62.2，均达最先进水平。
- **多视图空间理解**：VSI-Bench平均62.9，超越所有开源模型并与闭源API模型相当。

消融实验表明，单视图预训练和3D位置编码均至关重要，动态分块模块尤其提升小物体识别性能。SR-3D从真实深度切换到重建输入时性能下降幅度小于基线，显示出对深度估计误差的鲁棒性。局限性包括物体朝向感知困难、动态视频处理挑战，以及在OCR相关任务上观察到轻微性能下降。

## 背景与动机

当前视觉语言模型（VLM）在空间推理能力上存在根本性的瓶颈。2D VLM（如NVILA-Lite-8B）虽然具备强大的通用视觉理解能力，但其视觉表示中不包含显式的3D位置信息，导致在深度估计、相对方向判断等空间推理任务上表现不佳。例如，在BLINK_Depth基准上，GPT-4V-Turbo的准确率仅为66.9%。另一方面，现有的3D VLM（如LLaVA-3D）虽然直接处理3D点云，但面临两个关键问题：一是难以利用2D基础模型中丰富的先验知识，二是3D训练数据（如ScanNet）规模有限，限制了模型的泛化能力。

此外，在多视角场景中，通过文本描述来指定特定实例的空间关系（例如“左边第二个红色椅子”）非常繁琐且不精确，缺乏灵活的实例指定方式。现有方法（如SpatialRGPT）虽然引入了区域级推理能力，但其区域特征提取依赖反卷积层对低分辨率视觉令牌进行后处理上采样，信息损失较大，且同样缺乏统一的单视图与多视图处理范式。

本文的动机是：能否在不牺牲2D基础模型通用能力的前提下，通过一种轻量级的方式将3D空间信息注入到基础VLM的视觉表示中，从而同时提升单视图和多视图场景下的空间推理能力？核心洞察在于：利用现成的单目深度估计器（DepthAnythingV2）将单视图图像反投影到规范化3D坐标空间，并将该3D位置嵌入直接融合到视觉令牌中，使得模型在统一的3D表示空间中进行推理。这种设计允许仅使用2D单视图数据进行预训练的模型，其区域表示能够零样本泛化到多视图3D场景，从而绕过了对大规模3D标注数据的依赖。

## 核心创新

SR-3D 的核心创新在于将3D位置嵌入直接集成到基础视觉语言模型的视觉表示层中，而非将其作为后处理或仅在3D微调阶段引入。这一设计解决了现有2D VLM缺乏3D空间推理能力、而3D VLM又难以利用2D基础模型先验知识的核心瓶颈。

### 因果机理与关键变化

SR-3D 通过三个关键变化实现突破：

1. **视觉表示中的空间信息注入**：基线方法（如SpatialRGPT）仅在3D微调阶段引入位置信息，或根本不使用显式3D坐标。SR-3D 则直接对单视图图像进行深度估计（使用现成深度估计器），通过反投影将深度图转换为规范化3D坐标，再经正弦函数和可学习的逐点MLP编码后加到视觉令牌上。这使得模型在基础VLM阶段就获得了3D空间感知能力，而不牺牲2D基础模型的通用知识。

2. **动态分块区域特征提取**：基线方法（如SpatialRGPT）使用反卷积层对低分辨率视觉令牌进行后处理上采样，这引入了额外的信息损失。SR-3D 采用“tile-then-stitch”方法，直接在分块后的高分辨率特征上进行掩码池化，无需后处理。消融实验（Table 13）表明，该模块将COCO区域级分类的mAP从66.2提升至76.3，对小物体的提升尤为显著。

3. **统一的单视图与多视图训练范式**：基线方法（如Oryx）使用分离的路径处理单视图和多视图数据。SR-3D 采用统一的流水线，所有数据流经同一模型架构，在共享的规范化3D坐标空间中进行处理。这使得仅在2D单视图数据上训练的区域表示能够零样本泛化到多视图3D场景（Table 7：2D训练模型在SR-3D-Bench上零样本即达到合理准确率）。

### 证据强度与关键结果

SR-3D 的核心创新在多个基准上得到验证：

- **深度感知**：BLINK_Depth 准确率90.3%，超越SpatialRGPT-8B（87.9%）和GPT-4V-Turbo（66.9%）（Table 2）。
- **区域级分类**：COCO-2017上mAP 78.0、准确率88.6%，显著优于SpatialRGPT-8B（72.9 mAP, 82.9%）（Table 3）。
- **3D场景理解**：在Scan2Cap、ScanQA、SQA3D上均达最先进水平，如ScanQA Cider 109.3、SQA3D EM 62.2（Table 4）。
- **多视图空间理解**：VSI-Bench上平均准确率62.9%，超越所有开源模型并与API模型相当（Table 6）。

### 失败模式与局限性

尽管核心创新有效，但存在以下局限：OCR相关任务（TextVQA、ChartQA、DocVQA）出现一致的小幅性能下降（Table 1），可能需要在训练数据中增加更多OCR任务；物体朝向感知仍不准确，主要由于难以扩展相关训练数据；当前单视图和多视图模型是分开训练的，尚未实现统一检查点。这些局限点需要手动验证其具体影响程度。

## 整体框架

SR-3D（Spatial Region 3D）的核心设计是将3D空间推理能力直接注入基础视觉语言模型（VLM）的视觉表示层，而非在模型外部附加3D处理模块。整个流水线由四个主要模块构成，以统一的规范化3D坐标空间连接单视图和多视图输入。

**视觉编码器**基于SigLIP（来自PaliGemma），负责从输入图像或分块中提取视觉特征。**3D位置编码模块**是该框架的关键因果旋钮：对于单视图输入，首先使用DepthAnythingV2估计相对深度图，通过反投影得到相机坐标系下的逐像素3D位置图，再经正弦函数和可学习的逐点MLP编码为3D位置嵌入，直接加到视觉令牌上。这种设计使得2D基础模型在不牺牲通用能力的前提下获得空间感知能力——Table 1显示SR-3D在BLINKs、SAT、EmbSpat等空间相关基准上显著提升，同时通用VQA和OCR任务性能基本保持，仅OCR相关任务（TextVQA、ChartQA、DocVQA）出现轻微下降。

**动态分块区域提取器**（tile-then-stitch）解决了高分辨率图像中区域特征提取的瓶颈。传统方法使用反卷积层对低分辨率视觉令牌进行后处理上采样（如SpatialRGPT），而SR-3D直接对图像和掩码进行动态分块，拼接后通过掩码池化提取高分辨率区域特征。消融实验（Table 13）表明该模块将COCO分类mAP从66.2提升至76.3，尤其对小物体增益显著。

**大语言模型**采用Qwen-2-7B，接收融合了3D位置信息的视觉令牌和区域令牌进行语言理解与生成。

整个框架的**统一流水线**是另一关键设计：单视图和多视图数据流经同一模型架构，共享规范化3D坐标空间。多视图设置下，各视图的3D位置映射到同一规范化空间，使得仅在2D单视图数据上训练的区域表示能够零样本泛化到多视图3D场景（Table 7显示2D训练模型在SR-3D-Bench上零样本即达到合理准确率）。训练分为两阶段：先初始化自预训练2D VLM（NVILA-Lite-8B），冻结视觉编码器，微调3D位置编码模块、投影器和LLM；多视图模型在此基础上使用ScanQA、SQA3D、Scan2Cap等数据集微调。这一范式避免了昂贵的3D标注或逐帧密集标注需求。

## 核心模块与公式推导

### 架构总览

SR-3D的核心设计是将3D空间信息直接注入2D视觉语言模型（VLM）的视觉表示层，从而在不牺牲基础模型通用能力的前提下，赋予其3D空间推理能力。其架构包含四个关键模块：视觉编码器、3D位置编码模块、动态分块区域提取器，以及大语言模型。

**视觉编码器**使用PaliGemma中的SigLIP模块作为视觉骨干网络，负责从输入图像或分块中提取视觉特征。

**大语言模型**采用Qwen-2-7B，接收视觉令牌和区域令牌，进行语言理解与生成。

以下重点阐述两个核心创新模块：3D位置编码与动态分块区域提取。

### 3D位置编码模块

该模块是SR-3D实现空间感知的核心因果旋钮。其设计逻辑是：将单视图图像的深度估计结果反投影到规范化3D坐标空间，并将该3D位置嵌入与视觉令牌融合。

**单视图输入的处理流程**：
1. **深度估计**：对输入图像 $I$，使用现成的单目深度估计器DepthAnythingV2估计其相对深度图 $D$。
2. **反投影**：利用相机内参矩阵 $K$，将每个像素 $(u, v)$ 及其深度值 $D(u,v)$ 反投影到相机坐标系下的3D点 $P_{cam} = (x, y, z)$，计算公式为：
   
$$
\begin{bmatrix} x \\ y \\ z \end{bmatrix} = D(u,v) \cdot K^{-1} \begin{bmatrix} u \\ v \\ 1 \end{bmatrix}
$$

   其中 $K$ 是相机内参矩阵。
3. **规范化**：将相机坐标系下的3D点 $P_{cam}$ 通过缩放因子 $s$ 和偏移 $t$ 映射到规范化3D空间 $P_{norm} = s \cdot P_{cam} + t$，使其坐标范围落在 $[-1, 1]$ 区间内。
4. **编码**：对规范化3D坐标 $P_{norm}$ 使用正弦函数进行位置编码，再经过一个可学习的逐点MLP，得到最终的3D位置嵌入向量，并将其与对应的视觉令牌相加。

**多视图输入的处理**：对于多视图场景，每个视图的图像独立经过上述流程得到各自的3D位置嵌入。关键在于，所有视图的3D坐标都被映射到**共享的规范化3D坐标空间**中。这意味着，来自不同视角的同一物理点，在规范化空间中具有相同或相近的坐标。这种统一的表示空间使得仅在2D单视图数据上训练的区域表示能够零样本泛化到多视图3D场景。

**证据强度**：消融研究（Table 8）明确表明，3D位置编码（3D PE）与单视图预训练（PT）均至关重要，两者结合带来最大增益。Table 14进一步证实，3D PE比使用预训练基础模型特征（如DINOv2）更灵活，且性能相当或更优。

### 动态分块区域提取器

该模块旨在解决高分辨率图像中区域特征提取的精度问题。现有方法（如SpatialRGPT）使用反卷积层对低分辨率视觉令牌进行后处理上采样，这会引入信息损失。

SR-3D采用“先分块再拼接”（tile-then-stitch）的动态分块方法，直接在高分辨率特征上进行区域特征提取，无需后处理上采样。其流程为：
1. **图像分块**：将高分辨率输入图像 $I$ 和对应的区域掩码 $M$ 同时切分为多个固定大小的分块（tiles）。
2. **独立编码**：每个分块独立通过视觉编码器和3D位置编码模块，得到带有3D位置信息的视觉令牌。
3. **掩码池化**：在每个分块内，根据对应的区域掩码部分，对视觉令牌进行掩码池化（masked pooling），提取该分块内的区域特征。
4. **特征拼接**：将所有分块中提取到的、属于同一区域的局部特征拼接起来，形成完整的区域特征向量（region token）。

**证据强度**：消融研究（Table 13）显示，分块模块将COCO区域级分类的mAP从66.2提升至76.3，尤其对小物体的识别有显著改善，证实了其提升有效分辨率的有效性。

### 公式与变量含义总结

本节涉及的公式及其变量含义如下：

| 公式 | 变量含义 |
|------|----------|
| $\begin{bmatrix} x \\ y \\ z \end{bmatrix} = D(u,v) \cdot K^{-1} \begin{bmatrix} u \\ v \\ 1 \end{bmatrix}$ | $(u,v)$: 像素坐标；$D(u,v)$: 该像素的估计深度值；$K$: 相机内参矩阵（3x3）；$(x,y,z)$: 相机坐标系下的3D点坐标。 |
| $P_{norm} = s \cdot P_{cam} + t$ | $P_{cam}$: 相机坐标系3D点；$s$: 缩放因子；$t$: 偏移向量；$P_{norm}$: 规范化后的3D坐标（范围 $[-1,1]$）。 |
| 3D位置嵌入 = MLP(Sinusoidal($P_{norm}$)) | Sinusoidal: 正弦位置编码函数；MLP: 可学习的逐点多层感知机。 |

**注**：论文未提供完整的端到端损失函数公式，其训练采用标准的自回归语言建模损失（next-token prediction）。上述公式仅覆盖了3D位置编码模块的核心计算步骤。

## 实验与分析

### 主结果

SR-3D 在多个基准上展示了显著的性能提升，验证了将 3D 位置嵌入集成到基础 VLM 中的有效性。

**2D 空间推理与区域理解。** 在 BLINK_Depth 基准上，SR-3D 达到 90.3% 准确率，显著超越之前最好的开源模型 SpatialRGPT-8B（87.9%）和闭源模型 GPT-4V-Turbo（66.9%）（Table 2）。在 COCO-2017 区域级分类任务上，SR-3D 以 78.0 mAP 和 88.6% 准确率优于 SpatialRGPT-8B（72.9 mAP, 82.9%）（Table 3）。值得注意的是，SR-3D 在提升空间推理能力的同时，在通用 VQA 基准（如 MMBench, MMMU, MathVista）上保持了与基础模型 NVILA-Lite 相当的性能，仅在 OCR 相关任务（TextVQA, ChartQA, DocVQA）上观察到轻微下降（Table 1），表明 3D 感知预训练增强了空间推理而不牺牲通用知识。


![[assets/figures/papers/iclr26_0001_GTpf2NuwtR_3D_Aware_Region_Prompted_Vision_Language_Model/figures/003_Table_1.jpg]]

![[assets/figures/papers/iclr26_0001_GTpf2NuwtR_3D_Aware_Region_Prompted_Vision_Language_Model/figures/005_Table_2.jpg]]

![[assets/figures/papers/iclr26_0001_GTpf2NuwtR_3D_Aware_Region_Prompted_Vision_Language_Model/figures/006_Table_3.jpg]]
*Table 3: Region-level classification results on COCO-2017 val set with ground-truth boxes, following RegionCLIP (Zhong et al., 2022) and RegionGPT (Guo et al., 2024). Table 2: Results on $\mathbf { B L I N K } _ { \mathrm { D e p t h } }$ . We follow Cheng et al. (2024)’s protocol to test whether a VLM effectively leverages auxiliary 3D information

**3D 场景理解。** 在三个 3D 场景理解基准上，SR-3D 均达到最先进水平（Table 4）：Scan2Cap 上 Cider 达 97.9（LLaVA-3D 为 84.1），ScanQA 上 Cider 达 109.3（LLaVA-3D 为 103.1），SQA3D 上 EM 达 62.2（LLaVA-3D 为 60.1）。这些结果证实了统一 3D 表示空间的有效性。


![[assets/figures/papers/iclr26_0001_GTpf2NuwtR_3D_Aware_Region_Prompted_Vision_Language_Model/figures/007_Table_4.jpg]]
*Table 4: Evaluation of spatial scene understanding on the Scan2Cap, ScanQA, and SQA3D benchmarks. † indicates methods evaluated in a zero-shot setting. SR-3D achieves state-of-the-art results across all metrics. DynRefer’s RoIAlign (448 variant) (Zhao et al., 2025) as a baseline at the same resolution. Their proposed strategies are also complementary to our approach*

**区域级与全局空间理解。** 在 SR-3D-Bench 区域级空间理解上，SR-3D 以 83.3 平均准确率超越所有基线，包括 GPT-4o（73.6）和 LLaVA-3D（79.5）（Table 5）。在多视图全局空间理解基准 VSI-Bench 上，SR-3D 达到 62.9 平均准确率，超越所有开源模型并与 API 模型相当，尤其在相对方向任务上表现突出（Table 6）。


![[assets/figures/papers/iclr26_0001_GTpf2NuwtR_3D_Aware_Region_Prompted_Vision_Language_Model/figures/009_Table_5.jpg]]
*Table 5: Evaluation of region-level spatial scene understanding on the SR-3D-Bench. SR-3D outperforms all baselines, highlighting the importance of strong region understanding and spatial awareness. Notably, SoM struggles with multi-frame inputs, reflecting the inherent difficulty of multi-frame visual grounding*

![[assets/figures/papers/iclr26_0001_GTpf2NuwtR_3D_Aware_Region_Prompted_Vision_Language_Model/figures/011_Table_6.jpg]]

### 消融研究

**3D 位置编码与单视图预训练。** Table 8 的消融表明，单视图预训练（PT）和 3D 位置编码（3D PE）均至关重要，两者结合带来最大增益。单视图预训练提供主要增益，使模型能够迁移空间知识；3D PE 在当前规模下提供有限但一致的改进。

**动态分块模块。** Table 13 显示，动态分块（tile-and-stitch）模块将 COCO 分类 mAP 从 66.2 提升至 76.3，尤其在小物体上改进显著，表明该模块有效增加了有效分辨率。

**替代 3D 表示。** Table 14 比较了 3D PE 与使用预训练基础模型特征（如 DINOv2）的替代方案。3D PE 在 ScanQA（29.1 EM）、SQA3D（59.5 EM）和 Scan2Cap（97.3 Cider）上性能相当或更优，且更灵活——不依赖于特定预训练骨干。

**零样本泛化。** Table 7 显示，仅 2D 单视图训练的模型在 SR-3D-Bench 上零样本推理即达到合理准确率（如 3D Tall/Short 71.4%，3D Big/Small 79.7%），表明统一表示空间有效，3D 空间推理能力可以从 2D 数据中涌现。

**对重建输入的鲁棒性。** Table 9 显示，从真实深度切换到 Cut3R 重建输入时，SR-3D 的性能下降幅度小于 Video-3D LLM 基线，表明其对深度估计误差具有更强的鲁棒性。

### 失败模式与开放问题

论文识别了几个关键限制：（1）物体朝向感知——当前 VLM 难以准确回答与物体朝向相关的空间问题，主要由于难以扩展相关训练数据；（2）动态视频——方法针对多视图静态数据设计，扩展到动态输入具有挑战性；（3）OCR 任务性能下降——在 Table 1 中观察到 OCR 相关任务上的一致小幅下降，可能需要在训练数据中增加更多 OCR 任务；（4）单视图和多视图模型目前分开训练，未来需要研究如何有效合并为统一模型。

## 方法谱系与知识库定位

SR-3D 的核心贡献在于将 3D 位置嵌入直接集成到基础 2D VLM 的视觉表示中，而非像此前工作那样仅在 3D 微调阶段引入。这一设计选择直接回应了领域内的一个关键瓶颈：现有 2D VLM（如 GPT-4V-Turbo）缺乏 3D 空间推理能力，而 3D VLM（如 LLaVA-3D）则难以利用 2D 基础模型的先验知识，且受限于稀缺的 3D 训练数据。SR-3D 通过深度估计和反投影将单视图图像映射到规范化 3D 坐标空间，使得仅在 2D 单视图数据上训练的区域表示能够零样本泛化到多视图 3D 场景（Table 7 显示，2D 训练的模型在 SR-3D-Bench 上零样本即达到合理准确率）。

**与基线方法的对比关系**：SR-3D 在多个基准上建立了新的最优水平。在 BLINK_Depth 上达到 90.3%（Table 2），超越 SpatialRGPT-8B（87.9%）和 GPT-4V-Turbo（66.9%）；在 COCO-2017 区域级分类上达到 78.0 mAP（Table 3），显著优于 SpatialRGPT-8B（72.9 mAP）；在 Scan2Cap、ScanQA、SQA3D 三个 3D 场景理解基准上均达到最先进水平（Table 4），例如 ScanQA Cider 达到 109.3，超过 LLaVA-3D 的 103.1。在 SR-3D-Bench 区域级空间理解上（Table 5），SR-3D 以 83.3 平均准确率超越所有基线，包括 GPT-4o（73.6）和 LLaVA-3D（79.5）。在 VSI-Bench 多视图全局空间理解上（Table 6），SR-3D 达到 62.9 平均准确率，超越所有开源模型并与 API 模型相当。

**方法差异的关键槽位**：SR-3D 在三个关键设计上与基线方法不同。其一，视觉表示中的空间信息注入方式——SpatialRGPT 仅在 3D 微调阶段引入空间信息，而 SR-3D 在基础 VLM 中直接集成 3D 位置嵌入。其二，区域特征提取方式——SpatialRGPT 使用反卷积层对低分辨率视觉令牌进行后处理上采样，SR-3D 则采用动态分块（tile-then-stitch）方法，直接在分块后的高分辨率特征上进行掩码池化，无需后处理。其三，训练范式——Oryx 等方法使用分离路径处理单视图和多视图数据，SR-3D 采用统一流水线，所有数据流经同一模型架构，共享规范化 3D 坐标空间。

**适用边界与局限**：SR-3D 的适用边界由四个已知局限明确界定。第一，物体朝向感知——当前 VLM 难以准确理解和回答与物体朝向相关的空间问题，主要由于难以扩展相关训练数据。第二，动态视频——方法设计针对多视图静态数据，现实场景中常涉及动态环境，将位置嵌入扩展到动态输入具有挑战性。第三，OCR 任务性能下降——在 Table 1 中观察到 OCR 相关任务（如 TextVQA、ChartQA、DocVQA）上有一致的小幅性能下降，可能需要在训练数据中增加更多 OCR 任务。第四，统一检查点——当前单视图和多视图模型是分开训练的，未来需要研究如何有效合并为一个统一模型。

**开放问题**：论文识别了七个需要进一步研究的方向，其中三个最为紧迫：如何更大规模地利用位置表示来充分挖掘空间推理的潜力；如何有效结合单视图和多视图模型为一个统一的检查点；以及如何缓解 OCR 相关任务上的轻微性能下降。此外，在机器人等安全关键领域确保模型的鲁棒性和可靠性，以及在 VR/AR 智能眼镜等潜在应用中解决隐私和安全问题，也是重要的未来方向。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/3D_Aware_Region_Prompted_Vision_Language_Model.pdf

![[paperPDFs/ICLR_2026/3D_Aware_Region_Prompted_Vision_Language_Model.pdf]]
