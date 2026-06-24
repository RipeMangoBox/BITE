---
title: "Sapiens: Foundation for Human Vision Models"
type: paper
paper_level: A
venue: ECCV
year: 2024
pdf_ref: paperPDFs/ECCV_2024/Sapiens_Foundation_for_Human_Vision_Models.pdf
aliases:
- Sapiens
tags:
- ECCV_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 预训练数据的规模与领域针对性（大量自然场景人类图像），结合更高的模型容量与输入分辨率（1024像素），是影响下游性能的关键杠杆。
primary_logic: 在相同的计算预算下，使用大规模人类图像进行自监督预训练，相比通用图像预训练，能显著提升二维姿态估计、部位分割、深度估计和表面法线预测等人类中心任务的性能，且模型规模（参数从0.3B到2B）与性能保持正相关，展现出良好的可扩展性。
claims:
- 在 Humans-5K 全身姿态估计上，Sapiens-2B 取得 61.1 AP，超过先前最佳方法 7.6 mAP。
- 在 Humans-2K 部位分割上，Sapiens-2B 取得 81.2 mIoU，比 DeepLabV3+ 提升 17.1 mIoU。
- 在 Hi4D 多人深度估计上，Sapiens-2B 相比 DepthAnything 的相对 RMSE 降低 22.4%。
- 在 THuman2 表面法线估计上，Sapiens-2B 平均角度误差为 11.84°，相比 ECON 相对降低 53.5%。
---

# Sapiens: Foundation for Human Vision Models

> [!tip] 核心洞察
> 在相同的计算预算下，使用大规模人类图像进行自监督预训练，相比通用图像预训练，能显著提升二维姿态估计、部位分割、深度估计和表面法线预测等人类中心任务的性能，且模型规模（参数从0.3B到2B）与性能保持正相关，展现出良好的可扩展性。

| 字段 | 内容 |
|------|------|
| 中文题名 | Sapiens：人类视觉基础模型 |
| 英文题名 | Sapiens: Foundation for Human Vision Models |
| 会议/期刊 | ECCV 2024 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Sapiens |
| Dataset | Humans-5K, Humans-2K, Hi4D, THuman2 |

> [!tip] 效果简介
> - Humans-5K (pose) 上，Whole-body AP 61.1 vs 53.5 (DWPose-l) (+7.6)。
> - Humans-2K (part-seg) 上，mIoU 81.2 vs 64.1 (DeepLabV3+) (+17.1)。
> - Hi4D (depth) 上，RMSE 0.114 vs 0.147 (DepthAny-L) (-22.4% relative)。

## 概述

Sapiens 是一个面向以人为中心的视觉任务的基础模型系列。其核心动机在于，现有视觉模型大多在通用图像数据（如 ImageNet）上预训练，缺乏对大规模、领域特定（人类图像）数据的利用，导致在多样化人类中心任务上的泛化能力、广泛适用性以及高保真度不足。

该工作的核心洞察是：**在相同的计算预算下，使用大规模人类图像进行自监督预训练，相比通用图像预训练，能显著提升下游人类中心任务的性能**。为此，作者构建了包含 3 亿张自然场景人类图片的 Humans-300M 数据集，并采用掩码自编码器（MAE）在高分辨率（1024×1024）下对 ViT 编码器进行预训练，模型参数量从 0.3B 扩展至 2B。预训练后，仅需添加轻量级任务专用解码器进行微调，即可适配四项核心任务：二维姿态估计、身体部位分割、深度估计和表面法线预测。

实验结果表明，Sapiens 在多项基准上显著超越先前方法。以最大的 Sapiens-2B 模型为例，其在 Humans-5K 全身姿态估计上达到 61.1 AP，超越先前最佳方法 7.6 mAP（Table 3）；在 Humans-2K 部位分割上达到 81.2 mIoU，较 DeepLabV3+ 提升 17.1 mIoU（Table 4）；在 Hi4D 多人深度估计上，相对 RMSE 较 DepthAnything 降低 22.4%（Table 5）；在 THuman2 表面法线估计上，平均角度误差为 11.84°，较 ECON 相对降低 53.5%（Table 6）。消融研究进一步证实，领域特定预训练（Humans-300M）在所有四项任务上均一致优于 ImageNet 或通用数据集预训练，且模型规模与性能保持正相关，未观察到饱和迹象（Table 7, Figure 10）。

在方法定位上，Sapiens 属于“大规模领域特定预训练 + 多任务微调”范式，其关键区别于现有工作的三个杠杆点在于：**预训练数据域从通用图像转向人类专属数据**、**输入分辨率从 224/384 像素提升至 1024 像素**、**模型容量扩展至 2B 参数**（Table 1）。该范式在二维人类视觉任务上展现了强大的可扩展性和泛化能力，但其当前未涵盖三维重建或多模态理解，且预训练所需计算资源极高（1024 块 A100 GPU 训练 18 天），在极端野外数据上的鲁棒性及与其他自监督范式（如 DINOv2）的对比仍有待探索。

## 背景与动机

### 人类中心视觉任务的独特挑战

计算机视觉领域在通用图像理解上取得了长足进步，但在以人类为核心的任务中仍面临显著瓶颈。二维姿态估计、身体部位分割、深度估计和表面法线预测等任务，要求模型对人类身体的精细结构、姿态变化、衣物遮挡以及多样化的自然场景具有高度鲁棒的理解能力。然而，现有视觉模型大多在通用图像数据集（如 ImageNet-1K、ImageNet-21K 或 LVD-142M）上进行预训练，缺乏大规模、领域特定的人类图像预训练，导致其在多样化人类中心任务上的泛化能力、广泛适用性以及高保真度不足。

### 现有方法的局限性

当前主流的预训练视觉模型存在三个关键缺口：

1. **预训练数据域不匹配**：现有模型如 ViT、DINOv2 等均在通用场景图像上预训练，这些数据中人类仅作为场景的一部分出现，而非核心关注对象。这导致模型在下游人类任务微调时，需要从零开始学习大量人类特有的视觉模式，效率低下且性能受限。

2. **输入分辨率受限**：大多数先进预训练模型采用 224 或 384 像素的输入分辨率（如 Table 1 所示），难以捕捉人体关键点、部位边界和表面细节等需要高分辨率才能精确建模的细粒度信息。

3. **模型容量与可扩展性未充分探索**：在人类中心任务上，模型规模（参数量）与性能之间的关系尚未被系统研究。现有工作的模型规模通常不超过 1B 参数，更大容量模型能否带来持续的性能提升仍是未知数。

### 本文动机与核心思路

针对上述缺口，Sapiens 提出了一套系统性的解决方案。其核心洞察在于：**在相同的计算预算下，使用大规模人类图像进行自监督预训练，相比通用图像预训练，能显著提升多项人类中心任务的性能**。具体而言，本文从三个关键杠杆入手：

- **领域特定预训练数据**：构建 Humans-300M 数据集，包含 3 亿张自然场景中的人类图像，使模型在预训练阶段即充分接触人类外观、姿态和场景的多样性。
- **高分辨率输入**：将输入分辨率提升至 1024 像素，保留人体细节信息，为下游精细任务提供更高质量的视觉表征。
- **模型规模缩放**：提供从 0.3B 到 2B 参数的系列模型，系统验证了模型容量与人类中心任务性能之间的正相关关系，展现出良好的可扩展性。

该方法遵循“预训练-微调”范式：首先在大规模人类图像上通过掩码自编码器（MAE）进行自监督预训练，随后针对四项具体任务添加轻量级专用解码器进行端到端微调。这种设计既保证了预训练表征的通用性，又实现了下游任务的高效适配。

## 核心创新

Sapiens 的核心创新并非提出全新的网络架构，而是通过**大规模领域特定预训练**这一方法论转变，系统性解决了现有视觉模型在人类中心任务上泛化能力不足的瓶颈。其创新可以凝练为三个相互强化的“changed slots”：

### 1. 领域特定预训练数据：Humans-300M
此前的视觉预训练模型（如 ViT、DINOv2）主要依赖通用图像数据集（ImageNet-1K、ImageNet-21K 或 LVD-142M），这些数据中人类图像占比有限且场景单一。Sapiens 的关键突破在于构建了**Humans-300M**——一个包含 3 亿张自然场景人类图像的专属预训练数据集（Figure 2 显示其中超过 2.48 亿张图像包含多人）。这一数据域的转变（从通用图像到纯人类图像）是性能提升的根本杠杆：消融实验（Table 7）直接证实，在相同模型（Sapiens-0.3B）下，使用 Humans-300M 预训练在所有四项任务上均显著优于 ImageNet 或通用数据集预训练。

### 2. 高分辨率输入与高容量模型
Sapiens 将输入分辨率从常规的 224/384 像素提升至**1024×1024 像素**，同时将模型参数量推至最高 **2B**（Sapiens-2B），远超此前最大约 1B 参数的 DINOv2（Table 1）。高分辨率使得模型能够捕获精细的人体结构细节（如手指关节、面部特征），而大容量模型则为吸收 3 亿张图像中的丰富人类外观变化提供了足够的表示空间。Table 3-6 的缩放实验表明，从 0.3B 到 2B，四项任务的性能单调提升，未观察到饱和迹象——这验证了“更大的领域特定模型”这一技术路线的有效性。

### 3. 统一的预训练-微调范式
Sapiens 采用掩码自编码器（MAE）在 1024×1024 分辨率的人类图像上进行自监督预训练（Figure 3 展示了模型对高度遮挡人类图像的重建能力），随后仅需添加轻量级任务专用解码器即可端到端微调至四项任务。这一设计使得同一预训练编码器可以泛化到姿态估计、部位分割、深度估计和表面法线预测，无需为每项任务重新设计骨干网络，体现了“人类视觉基础模型”的统一性思想。

三个 changed slots 之间存在因果联动：**大规模人类数据**提供了领域知识的基础，**高分辨率与大容量**赋予模型吸收这些知识的能力，而**统一的预训练-微调范式**则确保这些知识可以高效迁移到多样化的下游任务中。

## 整体框架

Sapiens 遵循“预训练-后微调”的统一范式，构建了一个面向人类中心视觉任务的基础模型体系。其整体流水线由三个核心模块串联而成：面向领域的大规模数据构建、高分辨率掩码自编码器预训练，以及针对四项下游任务的轻量级任务头微调。

### 流水线总览

**数据预处理与领域数据集构建** → **自监督预训练** → **任务特定微调**

1. **Human Image Preprocessing**：利用现成的人员检测器从大规模自然场景图像中过滤并裁剪出以人为中心的区域，构建包含 3 亿张多样化人类图像的 **Humans-300M** 数据集。该数据集覆盖单人、多人、面部、上半身及全身等多种场景，其中超过 2.48 亿张图像包含多个主体（Figure 2）。这一步将通用视觉数据转化为领域专属的预训练语料。

2. **Masked Autoencoder Pretraining**：在 1024×1024 高分辨率的人类图像上，采用掩码自编码器（MAE）对 ViT 编码器进行自监督预训练。图像被切分为 16×16 的非重叠 patch，随机掩码后由编码器-解码器结构重建。该阶段仅使用 Humans-300M 的图像数据，不依赖任何人工标注，使编码器学习到强健的人类图像表征。Sapiens 系列提供从 0.3B 到 2B 参数的编码器规格（Table 2），计算量最高达 8709.0 GFLOPs（Table 1）。

3. **Task-specific Finetuning**：在预训练编码器之上，分别附加轻量级的任务专用解码器头，以端到端方式微调，适配以下四项人类中心任务：
   - **二维姿态估计**：输出 308 个全身关键点的热图，使用均方误差损失 $\mathcal{L}_{\mathrm{pose}} = \mathrm{MSE}(\mathbf{y}, \hat{\mathbf{y}})$。
   - **部位分割**：输出 28 类身体部位的逐像素分类，使用加权交叉熵损失 $\mathcal{L}_{\mathrm{seg}} = \mathsf{WeightedCE}(\mathbf{p}, \hat{\mathbf{p}})$。
   - **深度估计**：输出人体区域的单目深度图，使用尺度不变的对数深度损失 $\mathcal{L}_{\mathrm{depth}} = \sqrt{\overline{(\Delta\mathbf{d})^{2}} - \frac{1}{2}(\overline{\Delta\mathbf{d}})^{2}}$，其中 $\Delta\mathbf{d} = \log(\mathbf{d}) - \log(\hat{\mathbf{d}})$。
   - **表面法线预测**：输出人体区域的逐像素法线向量，损失仅在人体像素上计算：$\mathcal{L}_{\mathrm{normal}} = ||\mathbf{n} - \hat{\mathbf{n}}||_{1} + (1 - \mathbf{n} \cdot \hat{\mathbf{n}})$。

### 输入输出流

整个系统的输入为一张包含人类的自然场景图像，输出则根据任务不同而各异：

- **输入**：任意分辨率的 RGB 图像，经预处理统一缩放至 1024×1024 后送入编码器。
- **共享编码器**：基于 ViT 架构的 MAE 预训练编码器，提取高分辨率人类图像特征。
- **任务头输出**：
  - 姿态估计 → 308 通道的热图（每个关键点一个热图）
  - 部位分割 → 28 通道的逐像素类别概率图
  - 深度估计 → 单通道深度图
  - 表面法线估计 → 三通道法线向量图

### 关键设计决策

该框架的核心洞察在于：**在相同的计算预算下，将预训练数据的领域从通用图像切换为大规模人类专属图像，并配合更高的输入分辨率与模型容量，是驱动下游性能提升的因果杠杆**。消融实验（Table 7）证实，使用 Humans-300M 预训练的 Sapiens-0.3B 在所有四项任务上均显著优于基于 ImageNet 或通用数据集预训练的同等模型。此外，模型规模从 0.3B 到 2B 的扩展带来了性能的单调提升，未观察到饱和迹象（Table 3-6），表明该框架具有良好的可扩展性。

## 核心模块与公式推导

Sapiens 的整个训练流程包含三个核心模块：**人类图像预处理**、**掩码自编码器预训练**和**任务特定微调**。以下逐一展开其关键设计与公式。

### 人类图像预处理

该模块负责构建领域特定的预训练数据集 Humans-300M。其核心操作是：利用现成的人员检测器对大规模自然场景图像进行过滤，仅保留并裁剪出包含人类的图像区域，最终汇聚为约 3 亿张多样化人类图像。该数据集是后续所有模块的数据基础，其领域针对性被证明是性能提升的关键杠杆（见 Table 7 消融实验）。

### 掩码自编码器预训练

预训练阶段采用掩码自编码器（MAE）方法，在 Humans-300M 数据集上对视觉编码器进行自监督学习。关键设计选择包括：

- **输入分辨率**：所有图像统一缩放至 1024×1024 的固定方形尺寸，显著高于通用预训练模型常用的 224 或 384 像素。
- **分块策略**：将图像划分为规则的非重叠图像块（patch），固定块大小为 16×16。
- **掩码机制**：随机掩码掉 75% 的图像块，仅将可见块送入编码器，解码器则负责从编码特征重建被掩码区域的像素值。

该模块的输出是一个具备强大人体图像理解能力的编码器，为下游任务提供高质量的特征表示。Figure 3 展示了模型在未见图像上的重建效果，即使在 95% 的极高掩码率下，重建质量下降也极为有限，印证了模型对人体图像的深层理解。

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/004_Figure_3.jpg]]
*Figure 3: Sapiens reconstruction on unseen images. Top: Each triplet contains the ground truth (left), the masked image (center), and the MAE reconstruction (right), with a masking ratio of 75%, a patch size of 16, and an image size of 1024. Bottom: Varying the mask ratio between [0.75, 0.95] during inference reveals a minimal reduction in quality, underscoring the model’s understanding of human images*

### 任务特定微调

在预训练编码器之上，为四项人类中心任务分别附加轻量级任务专用解码器，并进行端到端微调。各任务的核心公式如下：

#### 二维姿态估计

姿态估计解码器预测每个关键点的热图（heatmap），训练目标是最小化预测热图 $\hat{\mathbf{y}}$ 与真值热图 $\mathbf{y}$ 之间的均方误差：

$$\mathcal{L}_{\mathrm{pose}} = \mathrm{MSE}(\mathbf{y}, \hat{\mathbf{y}})$$

其中，$\mathbf{y}$ 为以关键点坐标为中心生成的高斯热图真值，$\hat{\mathbf{y}}$ 为模型预测的热图。该损失直接约束模型准确定位人体 308 个关键点的空间位置。

#### 部位分割

部位分割解码器输出每个像素在 28 个类别上的概率分布，训练采用加权交叉熵损失：

$$\mathcal{L}_{\mathrm{seg}} = \mathsf{WeightedCE}(\mathbf{p}, \hat{\mathbf{p}})$$

其中，$\mathbf{p}$ 为像素的真实类别标签，$\hat{\mathbf{p}}$ 为模型预测的类别概率向量。加权机制用于缓解类别不平衡问题，确保小面积部位（如手指、耳朵）也能得到充分训练。

#### 深度估计

深度估计任务预测每个像素的尺度不变对数深度，损失函数设计为：

$$\mathcal{L}_{\mathrm{depth}} = \sqrt{\overline{(\Delta\mathbf{d})^{2}} - \frac{1}{2}(\overline{\Delta\mathbf{d}})^{2}}$$

其中，$\Delta\mathbf{d} = \log(\mathbf{d}) - \log(\hat{\mathbf{d}})$，$\mathbf{d}$ 为真实深度值，$\hat{\mathbf{d}}$ 为预测深度值，上划线表示空间均值。该损失在尺度不变性约束下优化深度预测的相对误差，使模型聚焦于深度结构而非绝对尺度。

#### 表面法线估计

表面法线估计解码器预测每个像素的单位法向量，损失函数结合 L1 范数与余弦相似度：

$$\mathcal{L}_{\mathrm{normal}} = ||\mathbf{n} - \hat{\mathbf{n}}||_{1} + (1 - \mathbf{n} \cdot \hat{\mathbf{n}})$$

其中，$\mathbf{n}$ 为真实法向量，$\hat{\mathbf{n}}$ 为预测法向量。该损失仅在人体像素区域计算——即只对图像中属于人类的部分施加监督，避免背景区域干扰法线方向的学习。

### 补充图表

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/006_Figure_5.jpg]]
*Figure 5: Ground-truth synthetic annotations for depth and surface normal estimation*

## 实验与分析

### 核心实验设置

Sapiens 系列编码器均从零开始在 1024 × 1024 分辨率、patch size 16 的设置下进行 MAE 预训练（Section 4.1）。预训练完成后，针对四项任务分别添加轻量级任务专用解码器并进行端到端微调。编码器规模从 0.3B 到 2B 参数不等，具体规格见 Table 2。

### 主要结果

#### 二维姿态估计

在 Humans-5K 测试集上，Sapiens 系列模型展现出显著的性能优势（Table 3）。最小的 **Sapiens-0.3B** 即超越 DWPose-l 达 +2.8 AP（全身），而 **Sapiens-2B** 以 **61.1 AP** 的全身姿态估计精度创下新纪录，相较此前最佳方法 DWPose-l（53.5 AP）提升 **+7.6 mAP**。值得注意的是，Sapiens-0.6B 在仅使用 1024 分辨率输入的条件下，已全面超越所有先前方法，包括使用 2560 分辨率输入的 ViTPose+-H。Figure 6 展示了 Sapiens-1B 在自然场景下对 308 个关键点的定性预测结果，模型对全身、半身、面部及多人场景均表现出良好的泛化能力。

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/009_Table_3.jpg]]
*Table 3: Pose estimation results on Humans-5K test set. Flip test is used*

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/008_Figure_6.jpg]]
*Figure 6: Pose estimation with Sapiens-1B for 308 keypoints on in-the-wild images*

#### 身体部位分割

Table 4 报告了 Humans-2K 测试集上的部位分割结果。Sapiens-0.3B 以 76.7 mIoU 的成绩超越 DeepLabV3+（64.1 mIoU）达 **+12.6 mIoU**，并显著优于 Mask2Former（基于 Swin-L 骨干网络）。**Sapiens-2B** 进一步将性能推至 **81.2 mIoU** 和 **89.4 mAcc**，相较 DeepLabV3+ 的 mIoU 提升 **+17.1**。Figure 7 的定性结果显示，Sapiens-1B 在单人和多人图像上均能准确分割 28 类身体部位，且对衣物遮挡、复杂姿态具有较好的鲁棒性。

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/010_Table_4.jpg]]
*Table 4: We report mIoU and mAcc on Humans-2K test set. Methods with * are trained by us*

#### 单目深度估计

深度估计在 THuman2.0（单人）和 Hi4D（多人）两个数据集上进行评估（Table 5）。在 Hi4D 多人场景下，**Sapiens-2B** 的 RMSE 为 **0.114**，相较 DepthAnything-L（0.147）实现 **22.4% 的相对 RMSE 降低**。在 THuman2.0 上，Sapiens-2B 同样以 0.103 的 RMSE 取得最优结果。Figure 8 将 Sapiens-1B 与 DepthAnything-L 的深度预测进行可视化对比，并展示 ∇depth 作为伪法线——Sapiens 预测的深度在人体表面表现出更好的几何一致性，伪法线更平滑、噪声更少。

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/012_Table_5.jpg]]
*Table 5: Comparison of Sapiens for monocular depth estimation on human images*

#### 表面法线估计

Table 6 报告了表面法线估计的结果。在 THuman2.0 上，**Sapiens-2B** 的平均角度误差仅为 **11.84°**，相较 ECON（25.45°）实现 **53.5% 的相对误差降低**；在更严格的角度阈值（≤11.25°）下，Sapiens-2B 的像素占比（62.8%）是 ECON（28.1%）的两倍以上。在 Hi4D 多人场景下，Sapiens-2B 同样以 12.03° 的平均角度误差大幅领先其他方法。Figure 9 的定性对比显示，Sapiens-1B 预测的法线图在面部细节和身体轮廓上明显优于 PIFuHD 和 ECON，后者在复杂姿态或遮挡区域常出现明显的几何失真。

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/014_Table_6.jpg]]
*Table 6: Comparison of Sapiens for surface normal estimation on human images*

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/015_Figure_9.jpg]]
*Figure 9: Qualitative comparison of Sapiens-1B with PIFuHD [89] and ECON [108] for surface normal estimation on in-the-wild images*

### 消融实验

#### 预训练数据领域的影响

Table 7 系统对比了不同预训练数据源对四项下游任务的影响。使用 **Humans-300M** 进行领域特定预训练的 Sapiens-0.3B，在所有四项任务上均显著优于基于 ImageNet-1K、ImageNet-21K 或通用数据集（LVD-142M）预训练的同等模型。例如，在部位分割任务上，Humans-300M 预训练较 ImageNet-1K 预训练提升 **+8.4 mIoU**；在法线估计上，30° 误差内的像素占比从 75.4% 提升至 83.8%。这一结果直接验证了“领域特定预训练数据”是性能提升的关键因果杠杆。

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/017_Table_7.jpg]]
*Table 7: Comparison of Sapiens-0.3B pretrained on various data sources. A domain-specific pretraining yields superior results compared to general data sources*

#### 模型规模的可扩展性

从 Sapiens-0.3B 到 Sapiens-2B，四项任务的性能均呈现单调提升趋势（Table 3-6），未观察到饱和迹象。具体而言：
- 姿态估计（全身 AP）：0.3B 为 55.8，2B 为 61.1（+5.3）
- 部位分割（mIoU）：0.3B 为 76.7，2B 为 81.2（+4.5）
- 深度估计（Hi4D RMSE）：0.3B 为 0.125，2B 为 0.114（-8.8%）
- 法线估计（THuman2 平均角度误差）：0.3B 为 13.17°，2B 为 11.84°（-10.1%）

这表明 Sapiens 的预训练框架具有良好的参数可扩展性，更大的模型容量能够有效利用 Humans-300M 中的丰富信息。

#### 预训练数据量的影响

Figure 10 展示了 Sapiens-0.3B 的法线估计性能随预训练过程中所见唯一人类图像数量增加的变化曲线。以 30° 误差内的像素百分比为指标，性能随数据量单调提升，在约 2.5 亿张图像后增长趋缓但未完全饱和。这进一步支持了大规模领域特定数据对于提升下游性能的价值。

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/016_Figure_10.jpg]]
*Figure 10: Sapiens-0.3B’s normal estimation performance with unique human images seen during pretraining*

### 失败模式与局限性分析

尽管 Sapiens 在各项基准上表现优异，但论文中未系统报告具体的失败案例。基于方法设计和实验设置，可推断以下潜在失效场景：

1. **极端野外条件**：自建的高质量标注数据集（Humans-5K、Humans-2K）依赖于可控采集环境，模型在极端光照、严重遮挡、非典型人体姿态等真实野外条件下的鲁棒性尚待验证。

2. **深度与法线的域间隙**：深度估计和法线预测的训练数据为合成数据（Figure 5），虽然模型在基准测试上泛化良好，但在复杂光照、透明/反射表面、毛发细节等真实场景下可能存在域间隙。

3. **多人密集交互场景**：Hi4D 的多人深度估计结果（Table 5）显示，Sapiens 在多人场景下的相对优势小于单人场景，暗示密集人体交互可能仍是挑战。

4. **非人类或混合场景**：Sapiens 专为人类中心任务设计，在包含非人类物体或复杂背景的混合场景中，其行为未被评估，可能产生不可预测的输出。

### 公平性评估

论文未针对性别、年龄、肤色等敏感属性进行公平性评估，也未讨论 Humans-300M 数据集可能存在的分布偏差。这一缺失在人类中心视觉模型中尤为关键，因为训练数据的入口分布可能直接影响模型在不同人群上的表现差异。

### 补充图表

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/002_Table_1.jpg]]
*Table 1: Comparison of state-of-the-art pretrained vision models. Sapiens adopts a higher resolution backbone on a large dataset of in-the-wild human images*

![[assets/figures/papers/paper_list_l1642_Sapiens_Foundation_for_Human_Vision_Models/figures/003_Figure_2.jpg]]
*Figure 2: Overview of number of humans per image in the Humans-300M dataset*

## 方法谱系与知识库定位

### 主干架构与预训练范式的继承与偏离

Sapiens 的编码器架构直接继承自标准 Vision Transformer (ViT)，其核心预训练方法采用掩码自编码器 MAE (He et al., CVPR 2022)。这一技术选型在通用视觉基础模型领域已有充分验证，但 Sapiens 的关键偏离在于三个维度的“领域特化”：

1. **预训练数据域的彻底转向**：现有通用视觉模型（如 DINOv2、AIM、DepthAnything）普遍使用 ImageNet-1K、ImageNet-21K 或 LVD-142M 等通用图像数据集进行预训练。Sapiens 则构建了 Humans-300M——一个包含 3 亿张自然场景人类图像的专属数据集，将预训练分布从“万物”压缩至“人类”。这一决策的因果效应在 Table 7 中得到直接验证：使用 Humans-300M 预训练的 Sapiens-0.3B 在所有四项人类中心任务上均显著优于使用 ImageNet 或通用数据集预训练的同等模型。

2. **输入分辨率的跃升**：主流视觉预训练模型通常采用 224 或 384 像素的输入分辨率（如 DINOv2 最大为 518 像素），而 Sapiens 将分辨率提升至 1024 像素。这一设计服务于人类中心任务对精细结构（如手指关节、面部特征、衣物褶皱）的敏感性需求。

3. **模型容量的扩展**：Sapiens 提供了从 0.3B 到 2B 参数的完整模型系列（Table 2），其中 2B 参数版本在参数量上超越了当时最大的通用视觉预训练模型（如 DINOv2-giant 约 1.1B 参数）。值得注意的是，在 0.3B 到 2B 的范围内，四项任务的性能均呈单调提升趋势，未观察到饱和迹象（Table 3-6），表明该领域特定预训练框架具有良好的可扩展性。

### 下游任务头与对比基线

Sapiens 采用“预训练-微调”范式，在共享的 ViT 编码器之上为每项任务附加轻量级专用解码器，端到端微调。各任务的具体设计及对比基线如下：

**二维姿态估计**：使用基于热图回归的 Transformer 解码器，损失函数为标准均方误差 $\mathcal{L}_{\mathrm{pose}} = \mathrm{MSE}(\mathbf{y}, \hat{\mathbf{y}})$。在 Humans-5K 测试集（308 个全身关键点）上，Sapiens-2B 取得 61.1 AP，超越 **DWPose-l** 的 53.5 AP（+7.6 mAP）。Sapiens-0.6B 即已超过 DWPose-l 达 2.8 AP，表明领域预训练带来的增益在较小模型上已显著显现。

**部位分割**：采用 28 类分割词汇，损失函数为加权交叉熵 $\mathcal{L}_{\mathrm{seg}} = \mathsf{WeightedCE}(\mathbf{p}, \hat{\mathbf{p}})$。在 Humans-2K 测试集上，Sapiens-0.3B 以 76.7 mIoU 大幅超越 **DeepLabV3+** 的 64.1 mIoU（+12.6 mIoU）和 **Mask2Former**；Sapiens-2B 进一步达到 81.2 mIoU 和 89.4 mAcc，相对 DeepLabV3+ 提升 17.1 mIoU。需要指出，标注为 `*` 的对比方法（Table 4）由作者重新训练，其余为原始论文结果，但部分基线工作（如 Mask2Former）的具体发表信息在本文分析材料中未提供，需手动核实。

**深度估计**：使用尺度不变的对数深度损失 $\mathcal{L}_{\mathrm{depth}} = \sqrt{\overline{(\Delta\mathbf{d})^{2}} - \frac{1}{2}(\overline{\Delta\mathbf{d}})^{2}}$，其中 $\Delta\mathbf{d} = \log(d) - \log(\hat{d})$。在 Hi4D 多人深度估计基准上，Sapiens-2B 相比 **DepthAnything-L** 的相对 RMSE 降低 22.4%（0.114 vs 0.147）。DepthAnything 本身以大规模通用数据预训练著称，Sapiens 的优势直接归因于领域特定预训练对人物几何结构的更好捕捉。

**表面法线估计**：损失函数为 L1 损失与余弦相似度损失之和 $\mathcal{L}_{\mathrm{normal}} = ||\mathbf{n} - \hat{\mathbf{n}}||_{1} + (1 - \mathbf{n} \cdot \hat{\mathbf{n}})$，仅计算人体像素区域。在 THuman2 基准上，Sapiens-2B 的平均角度误差为 11.84°，相比 **ECON** 的 25.45° 相对降低 53.5%；相比 **PIFuHD** 的优势更为显著。定性对比（Figure 9）显示，Sapiens 在自然场景图像的表面法线预测上具有更强的细节保持能力和泛化性。

### 适用边界与结构局限

1. **任务域限制**：Sapiens 专注于二维人类视觉任务（姿态、分割、深度、法线），不适用于通用物体或场景理解。其预训练数据仅包含人类图像，对非人类目标的表征能力未经验证。若需处理混合场景（如人-物交互），直接使用 Sapiens 可能不足，需考虑通用与领域数据的混合预训练策略。

2. **计算资源门槛极高**：预训练使用 1024 块 A100 GPU 训练 18 天，这一资源需求远超大多数学术实验室的承受能力，严重限制了复现性和后续研究的可及性。

3. **标注数据的可控性偏差**：自建的高质量标注数据集（Humans-5K、Humans-2K）依赖可控采集环境，真实野外场景的标注更难获得且质量更难保证。模型在极端野外条件（如严重遮挡、非典型姿态、极端光照）下的鲁棒性尚待独立验证。

4. **自监督方法的单一性**：Sapiens 仅探索了 MAE 一种自监督预训练范式，未与 DINOv2、AIM 等其他大规模预训练方法在同等条件下进行对比。其核心结论——“领域特定预训练优于通用预训练”——是否适用于其他自监督学习框架，目前尚不明确。

5. **合成数据的域间隙**：深度估计与表面法线预测的训练数据为合成数据（Figure 5）。虽然模型在测试集上泛化良好，但在复杂光照、半透明材质、动态遮挡等真实场景下可能存在域间隙，这一风险在论文中未做定量评估。

### 公平性与伦理考量

论文未针对性别、年龄、肤色、体型等敏感属性进行公平性评估，也未讨论 Humans-300M 数据集可能存在的分布偏差（如地域、种族、文化背景的不平衡）。考虑到人类中心模型的下游应用（如虚拟试穿、运动分析、医疗诊断）对社会公平有直接影响，这一缺失值得关注。

### 开放问题与未来方向

1. **三维拓展**：如何将 Sapiens 的领域特定预训练框架扩展至三维人体数字化任务（三维姿态估计、人体重建、新视角合成）？二维预训练的表征能否有效迁移至三维空间理解？

2. **多模态融合**：是否可以通过引入语言监督或图文多模态预训练，增强模型对人体语义属性（如动作描述、衣着属性）的理解能力，从而提升任务通用性？

3. **缩放策略优化**：当前观察到性能随模型规模和数据量单调增长，但未探索饱和点。是否存在更高效的缩放策略（如 Chinchilla 最优分配）来平衡计算预算与性能收益？

4. **混合场景泛化**：在非人类场景或人-物交互场景中，领域特定预训练是否仍然有效？通用数据与领域数据的最优混合比例是多少？这些问题对于将 Sapiens 的方法论推广至更广泛的应用场景至关重要。

## 原文 PDF

![[paperPDFs/ECCV_2024/Sapiens_Foundation_for_Human_Vision_Models.pdf]]
