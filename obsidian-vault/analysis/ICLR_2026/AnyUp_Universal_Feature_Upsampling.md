---
title: "AnyUp: Universal Feature Upsampling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AnyUp_Universal_Feature_Upsampling.pdf
project_link: https://wimmerth.github.io/anyup
code_link: null
aliases:
- AnyUp
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "用特征无关卷积基和局部窗口注意力实现跨编码器特征上采样。"
primary_logic: "AnyUp先把任意维度输入特征映射到规范结构表示，再用图像条件和局部注意力预测高分辨率特征。"
claims:
- "特征无关层对所有输入通道独立卷积并平均聚合，使输出不依赖具体特征维度。"
- "局部窗口注意力降低全局注意力成本并减少伪影。"
- "AnyUp在语义分割、深度估计和法线估计任务上优于或匹配强基线。"
- "在DINOv2上训练的AnyUp能泛化到SigLIP 2、DINOv3等未见特征提取器。"
---

# AnyUp: Universal Feature Upsampling

> [!tip] 核心洞察
> 核心洞察是：上采样任务主要依赖于理解特征图的局部结构变化，而非特征的具体语义内容。因此，可以通过一个与输入特征维度无关的卷积层来捕获这种结构信息，再结合局部窗口注意力机制简化优化目标，从而实现跨编码器的通用上采样。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AnyUp：通用特征上采样 |
| 英文题名 | AnyUp: Universal Feature Upsampling |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Y9UAgPehqo) · [Project](https://wimmerth.github.io/anyup) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | AnyUp |
| Dataset | COCO-Stuff, ADE20k, PASCAL-VOC, NYUv2 |

> [!tip] 效果简介
> - COCO-Stuff 上，mIoU 为 62.16，对比 62.15 (LoftUp)，变化 +0.01。
> - ADE20k 上，mIoU 为 42.43，对比 42.19 (FeatUp)，变化 +0.24。
> - PASCAL-VOC 上，mIoU 为 84.00，对比 84.36 (JAFAR)，变化 -0.36。

## 概要

AnyUp 是一种全新的通用特征上采样方法，旨在解决现有学习型上采样方法（如 FeatUp、LoftUp、JAFAR）的核心局限：它们在推理时无法泛化到未见过的特征提取器，必须针对每个视觉编码器重新训练。AnyUp 通过引入**特征无关层（feature-agnostic layer）**、**局部窗口注意力（local window attention）** 和**基于裁剪的训练策略**，首次实现了在推理时对任意输入特征、任意分辨率和任意任务的通用上采样。实验表明，AnyUp 在语义分割、深度估计和表面法线估计等多个下游任务上取得了最先进的结果，并且能够成功泛化到训练时未见过的特征提取器（如从 DINOv2 泛化到 SigLIP 2、DINOv3 等）。



特征上采样是计算机视觉中的基础操作，旨在将低分辨率特征图提升为高分辨率特征图，以支持需要精细空间信息的任务（如语义分割、深度估计）。现有方法可分为两类：

- **无参数方法**：如双线性插值（Bilinear Upsampling）和引导滤波（Guided Filtering），虽然通用但质量有限。
- **学习型方法**：如 FeatUp、LoftUp、JAFAR，虽然上采样质量更高，但存在严重局限——它们必须针对每个视觉编码器重新训练，无法在推理时泛化到未见过的特征提取器。这限制了它们在新型或大规模视觉模型上的应用。

AnyUp 的核心洞察是：上采样任务主要依赖于理解特征图的局部结构变化，而非特征的具体语义内容。因此，可以通过一个与输入特征维度无关的卷积层来捕获这种结构信息，再结合局部窗口注意力机制简化优化目标，从而实现跨编码器的通用上采样。



## 核心方法与创新机理

AnyUp 的核心创新在于其**特征无关层（feature-agnostic layer）**，这是实现跨编码器泛化的关键因果旋钮。该层通过一组可学习的卷积基对输入特征的所有通道独立处理并平均聚合，使得模型能够处理任意维度和类型的特征，无需针对特定编码器重新训练。

此外，AnyUp 还引入了以下创新：
- **局部窗口注意力**：将注意力计算限制在查询点周围的局部窗口内，替代 JAFAR 的全局注意力，显著降低计算复杂度并消除全局注意力伪影。
- **基于图像局部裁剪的训练策略**：从高分辨率图像中随机采样小裁剪块计算参考特征，替代 JAFAR 的低分辨率训练策略，提升上采样质量。
- **自一致性与输入一致性正则化**：增强模型对噪声和扰动的鲁棒性，并保持输入特征空间。



![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Y9UAgPehqo_AnyUp_Universal/figures/001_Figure_1.jpg]]

AnyUp 的整体框架如 Figure 3 所示，包含以下主要模块：

1. **特征无关层**：将任意维度的输入特征图转换为规范维度的特征图。
2. **卷积块（含残差连接）**：处理输入图像和低分辨率特征图。
3. **位置编码**：为图像特征添加位置信息。
4. **局部窗口注意力**：基于查询点局部窗口内的键值对计算上采样特征。
5. **图像裁剪采样**：训练时从高分辨率图像中随机采样局部裁剪块以获取参考特征。

训练流程如 Section 4.3 所述：从高分辨率图像中随机采样局部裁剪块，计算低分辨率特征和高分辨率参考特征，然后通过上采样网络生成预测特征，并与参考特征计算损失。



### 5.1 特征无关层

特征无关层是 AnyUp 实现跨编码器泛化的核心。其输出计算如 Eq. (1) 所示：

$$f_j = \frac{1}{N} \sum_{i \in \{1, \dots, N\}} \frac{\exp(p_i * \psi_j)}{\sum_{j' \in \{1, \dots, M\}} \exp(p_i * \psi_{j'})}$$

其中，$N$ 为输入通道数，$M$ 为卷积基数量，$p_i$ 为第 $i$ 个输入通道，$\psi_j$ 为第 $j$ 个可学习卷积核。每个输入通道独立卷积后经 softmax 归一化，再对所有通道取平均，使得输出与输入维度无关。

### 5.2 局部窗口注意力

AnyUp 使用局部窗口注意力替代 JAFAR 的全局注意力，将注意力计算限制在查询点周围的局部窗口内（窗口大小 $\sigma=0.2$，相对于输入尺寸）。这显著降低了计算复杂度：从 $H \times W \times H \times W$ 降至 $H \times W \times \sigma h \times \sigma w$，同时消除了全局注意力导致的伪影（如 Figure 8 所示）。

### 5.3 损失函数

AnyUp 的损失函数包含三个部分：

**cos-mse 损失**（Eq. (2)）：
$$L_{cos-mse}(q', \hat{q}) = 1 - \cos(q', \hat{q}) + L^2(q', \hat{q})$$

结合余弦距离和 L2 距离，用于监督上采样特征与参考特征的一致性。

**自一致性正则化**（Eq. (3)）：
$$L_{self-consistency} = d_{cos-mse}(f(p, I_{hr}), f(p, I_{hr}'))$$

通过比较原始高分辨率图像和增强后图像的上采样特征，增强模型对噪声和扰动的鲁棒性。

**输入一致性正则化**：计算输入特征 $p$ 与下采样后的预测输出特征 $q$ 之间的 cos-mse 损失，保持特征空间。

### 5.4 特征融合方式

与 JAFAR 使用空间语义特征调制不同，AnyUp 采用简单的特征拼接后接标准 ResNet 块，实验表明这不会带来性能下降。



## 实验与关键发现

### 6.1 主要结果

**语义分割**（Table 2）：AnyUp 在 COCO-Stuff 上达到 62.16 mIoU（最佳），在 ADE20k 上达到 42.43 mIoU（最佳），在 PASCAL-VOC 上达到 84.00 mIoU（与最佳基线 JAFAR 的 84.36 相当）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Y9UAgPehqo_AnyUp_Universal/figures/007_Table_2.jpg]]
*Table 2: Semantic Segmentation. Highlights for best, second and third best scores.*

**表面法线与深度估计**（Table 3）：在 NYUv2 上，AnyUp 在表面法线 RMSE（31.17）、深度绝对 RMSE（0.4755）和深度 δ1（0.8216）等指标上均优于所有基线方法。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Y9UAgPehqo_AnyUp_Universal/figures/008_Table_3.jpg]]
*Table 3: Surface Normal and Monocular Depth Estimation. AnyUp outperforms previous upsamplers for geometric tasks. Evaluation on the NYUv2 dataset (Silberman et al., 2012).*

**任意分辨率上采样**（Table 4）：AnyUp 在不同输入输出分辨率组合下均优于竞争对手，例如 32→224 分辨率下语义分割 mIoU 达 62.25，深度 RMSE 为 0.4441。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Y9UAgPehqo_AnyUp_Universal/figures/009_Table_4.jpg]]
*Table 4: Upsampling from any to any resolution. Linear probing results for Semantic Segmentation (COCO) and depth estimation when varying the feature map and output resolutions.*

**特征空间保持**（Table 5）：AnyUp 在使用预训练低分辨率探针评估时，语义分割 mIoU 达 40.83，深度 RMSE 为 0.498，均优于所有基线。相比之下，LoftUp 由于使用亲和矩阵损失导致特征分布严重偏移（语义分割 mIoU 仅 4.27）。

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Y9UAgPehqo_AnyUp_Universal/figures/010_Table_5.jpg]]
*Table 5: Feature Space Preservation. Semantic Segmentation (ADE20k) and Depth Estimation (NYUv2) with linear probes pre-trained on low-resolution DINOv2 features. AnyUp retains the input feature distribution while improving upsampling quality. LoftUp does not retain the input feature distribution, hence its results are heavily degraded. Guided Filtering requires tuning of hyperparameters per sample.*

### 6.2 跨模型泛化

**模型大小泛化**（Figure 6）：AnyUp 在不同 ViT 架构（ViT-S、ViT-B、ViT-L）上均能良好泛化，且训练较小模型时不会显著降低上采样质量。

**跨特征提取器泛化**（Table 6）：在 DINOv2 上训练的 AnyUp 模型能够成功泛化到 SigLIP 2、DINOv3 等未见过的特征提取器，性能匹配或超越在这些特征提取器上专门训练的方法。例如，DINOv2 训练的 AnyUp 在 SigLIP 2 LoftUp 特征上达到 51.68 mIoU，而 LoftUp 专门训练后仅 40.73 mIoU。

**多骨干训练**（Table 7）：在多个特征提取器上联合训练可进一步提升对未见特征的泛化能力，同时保持对已见特征的性能。

### 6.3 消融实验

Table 8 的消融实验验证了各组件的必要性：
- 移除特征无关层（替换为固定维度卷积）导致性能下降
- 移除局部窗口注意力（使用全局注意力）导致性能下降
- 移除裁剪训练策略导致性能下降
- 移除输入一致性正则化导致性能下降

Table 9 显示增大特征无关层的卷积基大小 $M$ 可提升性能，最终选择 $M=128$。

### 6.4 性能分析

Table 10 显示 AnyUp 具有 0.8M 参数，在 224² 分辨率下推理时间 12.8ms，FLOPs 20.6 GFLOPs，前向内存 0.8 GB，后向内存 3.3 GB。得益于窗口注意力的稀疏性，AnyUp 在计算效率和内存使用上均优于 JAFAR 和 LoftUp。

### 6.5 公平性说明

所有实验均使用官方发布的预训练权重进行对比。语义分割线性探针结果与 JAFAR 原始报告存在偏差，原因是修复了其实现中的一个 bug。FeatSharp 的权重未公开，因此未纳入对比。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__vision_models_multimodal__b001_Y9UAgPehqo_AnyUp_Universal/figures/002_Table_1.jpg]]
*Table 1: Categorization of feature upsampling methods. AnyUp is the first learnable method that generalizes to any input feature at inference time, while being able to upsample from any to any resolution and being task-agnostic.*



## 定位与知识库关联

AnyUp 属于**学习型特征上采样**方法谱系，其直接前身包括：

- **FeatUp**（Fu et al., 2024）：使用多视图重建训练，但需针对每个编码器重新训练。
- **LoftUp**（Huang et al., 2025）：使用堆叠注意力与自蒸馏，但同样无法跨编码器泛化。
- **JAFAR**（Couairon et al., 2025）：使用单层全局注意力，是 AnyUp 的架构基础，但无法跨编码器泛化。

AnyUp 的核心贡献在于首次实现了**编码器无关的通用上采样**，其关键创新——特征无关层——使得模型能够处理任意维度和类型的特征，无需针对特定编码器重新训练。这填补了学习型上采样方法在通用性方面的空白，为大规模视觉模型的应用提供了即插即用的上采样解决方案。

**开放问题**：
- AnyUp 的特征无关层是否能够泛化到非视觉特征（如文本或音频特征）？
- 局部窗口注意力中的窗口大小 $\sigma=0.2$ 是否在所有场景下都是最优的？是否存在自适应窗口大小的策略？
- 多骨干训练策略在更多样化的特征提取器集合上表现如何？是否存在性能上限？
- AnyUp 能否与特征去噪方法（如 FeatSharp 中的去偏置）结合以进一步提升性能？
- AnyUp 在 3D 场景理解或多视图重建等更复杂的下游任务中表现如何？



## 原文 PDF

![[paperPDFs/ICLR_2026/AnyUp_Universal_Feature_Upsampling.pdf]]
