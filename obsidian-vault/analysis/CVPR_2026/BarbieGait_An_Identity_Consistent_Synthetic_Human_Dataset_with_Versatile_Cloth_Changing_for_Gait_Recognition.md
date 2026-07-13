---
title: "BarbieGait: An Identity-Consistent Synthetic Human Dataset with Versatile Cloth-Changing for Gait Recognition"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/BarbieGait_An_Identity_Consistent_Synthetic_Human_Dataset_with_Versatile_Cloth_Changing_for_Gait_Recognition.pdf
project_link: null
code_link: "https://github.com/BarbieGait/BarbieGait"
aliases:
- GGOCIF
- BarbieGait
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/representation_self_supervised_transfer
- topic/benchmarks_datasets_evaluation
core_operator: 通过Gait-Oriented Normalization (GON)消除衣物特定统计量，并保留细粒度运动细节（水平分区归一化与时序建模），从而学习衣物不变特征。
primary_logic: 衣物在不同身体部位的影响程度不同，因此对特征图按水平分区并分别归一化，能更有效地消除局部衣物外观差异；同时，帧级时序建模和序列级非线性映射（GON-FC）共同强化了身份相关运动模式的表达。
claims:
- GON与GON-FC组合将BarbieGait上的平均Rank-1从67.7%提升至75.6%，平均mAP从57.6%提升至63.2%（Table 4）。
- GaitCLIF-3D在BarbieGait所有厚度等级上大幅超越先前方法，取得AVG Rank-1 80.4%，mAP 65.7%，而DeepGaitV2-P3D分别为71.7%和60.2%（Table 3）。
- 在真实数据集CCPG、SUSTech1K、Gait3D、GREW上，GaitCLIF均取得一致且显著的性能提升（Table 5和6）。
- 消融实验中，GON在所有衣物厚度等级上的表现全面优于BatchNorm、InstanceNorm和LayerNorm（Table 11）。
---

# BarbieGait: An Identity-Consistent Synthetic Human Dataset with Versatile Cloth-Changing for Gait Recognition

> [!tip] 核心洞察
> 衣物在不同身体部位的影响程度不同，因此对特征图按水平分区并分别归一化，能更有效地消除局部衣物外观差异；同时，帧级时序建模和序列级非线性映射（GON-FC）共同强化了身份相关运动模式的表达。

| 字段 | 内容 |
|------|------|
| 中文题名 | BarbieGait：面向换装步态识别的身份一致合成人体数据集 |
| 英文题名 | BarbieGait: An Identity-Consistent Synthetic Human Dataset with Versatile Cloth-Changing for Gait Recognition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.12221) · [Code](https://github.com/BarbieGait/BarbieGait) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/representation_self_supervised_transfer #topic/benchmarks_datasets_evaluation |
| Method | GaitCLIF (Gait-oriented CLoth-Invariant Feature) |
| Dataset | BarbieGait, CCPG, SUSTech1K, Gait3D |

> [!tip] 效果简介
> - BarbieGait (silhouette, THK1-THK9 as probes) 上，AVG Rank-1 accuracy (%) 80.4 (GaitCLIF-3D) vs 71.7 (DeepGaitV2-P3D) (+8.7)。
> - BarbieGait 上，AVG mAP (%) 65.7 (GaitCLIF-3D) vs 60.2 (DeepGaitV2-P3D) (+5.5)。
> - CCPG 上，Mean Rank-1 accuracy (%) under clothing conditions 84.9 (GaitCLIF-P3D*) vs 82.4 (DPGait) (+2.5)。

## 概要

**核心问题**：步态识别在换装条件下性能急剧退化，其根本瓶颈在于衣物多样性引发的类内外观方差大幅增加，使模型难以从外观中解耦出身份相关的运动特征。

**核心方法**：本文提出 **GaitCLIF (Gait-oriented CLoth-Invariant Feature)**，一种面向换装步态识别的鲁棒基线模型。其核心创新是 **Gait-Oriented Normalization (GON)**——将特征图按水平分区独立归一化，消除衣物特定的统计量，同时保留细粒度运动细节。GON被嵌入到时序卷积块（GON-P3D/GON-3D）和序列级全连接头（GON-FC）中，构成完整的衣物不变特征学习框架。

**数据集贡献**：为系统评估换装步态识别，本文构建了 **BarbieGait**——一个身份一致的合成人体数据集，包含521个受试者，每人100种不同衣物组合（涵盖发型、上下装、携带物），并按衣物厚度划分为10个等级（THK0–THK9）。

**主要结果**：
- 在BarbieGait上，GaitCLIF-3D取得平均Rank-1 **80.4%**、mAP **65.7%**，较先前最佳方法DeepGaitV2-P3D分别提升 **+8.7** 和 **+5.5** 个百分点（Table 3）。
- 消融实验证实，GON与GON-FC组合将平均Rank-1从67.7%提升至75.6%（Table 4），且GON在所有衣物厚度等级上全面优于BatchNorm、InstanceNorm和LayerNorm（Table 11）。
- 在真实数据集CCPG、SUSTech1K、Gait3D、GREW上，GaitCLIF均取得一致且显著的性能提升（Tables 5, 6），验证了方法的泛化能力。

**方法定位**：GaitCLIF属于外观基方法，通过归一化层面的创新实现衣物不变特征学习，可与现有步态识别骨干网络（如DeepGaitV2的P3D架构）无缝集成。其设计哲学——按身体部位分别消除衣物外观差异——为换装步态识别提供了简洁而有效的基线。



步态识别通过分析人体行走模式实现远距离、非侵入式的身份鉴别，在安防监控、刑侦追踪等场景中具有独特优势。然而，现实部署面临一个核心瓶颈：**衣物多样性引发的类内外观方差大幅增加，使模型难以学习跨衣物的身份相关特征**。当同一行人在不同时间穿着差异显著的服装（如厚重冬装与轻便夏装）时，外观轮廓的剧烈变化会淹没步态运动模式中的身份信息，导致识别性能急剧下降。

现有步态识别方法可大致分为两类：**基于外观（appearance-based）的方法**（如 **GaitSet**、**GaitPart**、**GaitGL**、**DeepGaitV2** 等）直接利用剪影或RGB图像提取特征，对衣物外观变化高度敏感；**基于姿态（pose-based）的方法**（如 **GaitGraph**、**GaitGraph2**、**GaitTR**、**SkeletonGait**、**DPGait** 等）通过人体关键点表征运动，虽对衣物外观具有一定不变性，但丢失了丰富的细粒度运动线索，且受限于姿态估计精度。两类方法在换装条件下均面临显著的性能退化。

现有换装步态数据集（如 CCPG、OU-ISIR、CCVID、MEVID）在衣物变化数量和身份一致性方面存在明显不足：每个受试者通常仅有2–5套服装，难以覆盖真实世界中衣物的多样性和厚度变化，且缺乏对衣物外观差异的细粒度量化。这限制了模型学习衣物不变特征的能力。

针对上述缺口，本文提出 **BarbieGait**——一个身份一致的合成人体数据集，每位受试者拥有100种不同服装组合，涵盖发型、上下装、鞋履及携带物的系统变化；同时提出 **GaitCLIF**（Gait-oriented CLoth-Invariant Feature）作为换装步态识别的鲁棒基线模型。GaitCLIF 的核心思想是：衣物在不同身体部位的影响程度不同，因此对特征图按水平分区并分别归一化，能更有效地消除局部衣物外观差异，同时通过帧级时序建模和序列级非线性映射强化身份相关运动模式的表达。



## 核心方法与创新机理

GaitCLIF 的核心创新在于提出了一种**面向步态的衣物不变特征学习框架**，通过三个紧密耦合的模块化改进，系统性地消除了衣物外观对步态识别的干扰。其设计哲学是：**衣物在不同身体部位的影响程度不同，因此应按水平分区独立归一化，同时保留细粒度运动细节。**

### 关键改进点（Changed Slots）

| 改进槽位 | 基线方案 | GaitCLIF 方案 | 作用机制 |
|----------|----------|---------------|----------|
| **归一化方式** | Batch Normalization (BN) | Gait-Oriented Normalization (GON)：对特征图按水平分区独立归一化 | 消除各身体区域的衣物特定统计量，保留运动模式 |
| **时序建模** | 标准 (2+1)D 或 3D 卷积 | GON-P3D / GON-3D：将 GON 嵌入时序卷积块 | 在时序建模过程中持续抑制衣物外观，增强运动表示 |
| **头部设计** | 单层分离 FC（每身体部位独立） | GON-FC：双层 FC + 每层后接 GON | 在序列级映射中进一步消除衣物统计量，强化身份相关运动模式 |

### 创新一：Gait-Oriented Normalization (GON)

GON 是 GaitCLIF 的核心归一化单元（Figure 4a），其设计出发点是：衣物在不同身体部位（如躯干、腿部）产生的剪影变化程度不同，全局归一化（如 BN）无法针对性消除局部衣物差异。

具体操作上，GON 将输入特征图 $\mathbf{X}$ 沿高度维度水平分割为 $m$ 个区域 $\{x_0, \dots, x_m\}$，对每个区域独立计算均值 $\mu(x_i)$ 和标准差 $\sigma(x_i)$ 并执行归一化：

$$\mathrm{GON}(x_i) = \gamma \left( \frac{x_i - \mu(x_i)}{\sigma(x_i)} \right) + \beta$$

其中 $\mu(x_i)$ 和 $\sigma(x_i)$ 在区域 $i$ 的所有通道和空间位置上计算（公式 3、4），$\gamma$ 和 $\beta$ 为可学习参数。最终输出为各区域归一化结果的拼接（公式 1）。这一设计使得每个身体区域的衣物外观差异被独立消除，而跨区域的运动结构得以保留。

消融实验（Table 11）证实，GON 在 BarbieGait 所有衣物厚度等级（THK1–THK9）上的 Rank-1 和 mAP 均全面优于 BatchNorm、InstanceNorm 和 LayerNorm，验证了水平分区归一化对换装场景的关键作用。

### 创新二：GON 增强的时序建模块（GON-P3D / GON-3D）

为在时序维度上持续抑制衣物外观，GaitCLIF 将 GON 嵌入到视觉阶段的时序卷积块中，形成两种变体：

- **GON-P3D**（Figure 4b）：将 GON 集成到 (2+1)D 伪三维卷积块中，空间卷积与时序卷积分离，GON 在时序卷积后应用。
- **GON-3D**（Figure 4c）：将 GON 集成到标准 3D 卷积块中，在三维时空卷积后应用 GON。

这两种设计使得模型在逐帧提取时空特征的过程中，每一步都通过 GON 消除衣物特定统计量，从而学习到衣物不变的帧级运动表示。

### 创新三：GON-FC 序列级头部

传统步态识别头部通常使用单层全连接层将各身体部位的特征映射为身份 logits。GaitCLIF 提出 **GON-FC**（Figure 4d）：采用双层 FC 结构，且在每一层 FC 之后均应用 GON。这一设计在序列级特征聚合阶段进一步消除衣物统计量，强化了与身份相关的细粒度运动模式的表达。

### 模块协同效应

消融实验（Table 4）揭示了三个模块的协同效应：
- 单独使用 GON-P3D 将 BarbieGait 平均 Rank-1 从基线 67.7% 提升至 69.8%；
- 单独使用 GON-FC 提升至 69.2%；
- **二者组合达到 75.6%**，mAP 从 57.6% 提升至 63.2%，表明帧级归一化与时序建模、序列级映射的联合优化是性能跃升的关键。

### 方法谱系与知识库定位

GaitCLIF 处于**外观类步态识别方法**的演进线上，其直接基线为 DeepGaitV2 系列（包括 2D/3D/P3D 变体）。与 GaitSet、GaitPart、GaitGL 等早期外观方法相比，GaitCLIF 通过归一化层面的针对性改进实现了换装鲁棒性的大幅提升。与 GaitGraph、GaitGraph2、GaitTR、GPGait、SkeletonGait、DPGait 等姿态类方法相比，GaitCLIF 直接利用剪影输入，避免了姿态估计误差的级联放大，同时通过 GON 机制隐式地聚焦于衣物无关的运动关节区域（Figure 8 热力图可视化证实了这一点）。



GaitCLIF 的整体设计遵循一个清晰的原则：**在保留细粒度运动细节的前提下，消除衣物引入的外观统计量**。其 pipeline 由四个核心阶段串联而成，输入为一段步态序列的剪影或 2D 姿态，输出为身份判别特征。

### 输入与预处理

序列中的每一帧首先经过基础卷积提取空间特征，随后进入由 GON 驱动的视觉阶段。根据 backbone 选择，视觉阶段可采用两种变体：

- **GaitCLIF-P3D**：使用 GON-P3D 块，将 GON 嵌入 (2+1)D 卷积中，先执行空间卷积，再在时序卷积后施加 GON。
- **GaitCLIF-3D**：使用 GON-3D 块，在 3D 卷积后直接施加 GON。

两种变体均通过 GON 对特征图进行水平分区归一化——这一设计的直觉在于，衣物在不同身体部位（头肩、躯干、腿部）造成的外观差异程度不同，分区归一化能更精细地消除局部衣物统计量，而非粗暴地对整张特征图统一操作。

### 视觉阶段与时序建模

框架包含四个堆叠的视觉阶段（visual stages），逐步提取空间-时序特征。每个阶段的核心操作可概括为：

1. **水平分区**：将特征图沿高度方向切分为若干区域。
2. **GON 归一化**：对每个区域独立计算均值 $\mu(x_i)$ 与标准差 $\sigma(x_i)$，执行归一化后拼接，得到衣物不变特征 $\mathbf{X}' = \mathbf{Cat}(\mathrm{GON}(x_0), \dots, \mathrm{GON}(x_m))$。
3. **时序卷积**：在 GON-P3D/GON-3D 块中，时序卷积紧接归一化，强化帧间运动模式的表达。

这种“分区归一化 + 时序建模”的组合，使得网络在抑制衣物外观的同时，仍能捕捉跨帧的动态关节运动——这正是身份相关特征的关键载体。

### 时序池化与水平池化

经过四个视觉阶段后，特征进入时序池化（Temporal Pooling），将帧级特征聚合为序列级表示。随后通过水平池化（Horizontal Pooling），将序列级特征按身体部位进一步划分，为后续的独立映射做准备。这一流程沿袭了 GaitSet 等经典方法的设计，但关键区别在于上游特征已经过 GON 的衣物不变性处理。

### GON-FC 头部

框架的末端是 GON-FC Head——一个两层全连接结构，每层 FC 后均施加 GON。其作用是在序列级别上进一步消除残留的衣物统计量，并将各身体部位的特征非线性映射为身份 logits。消融实验表明，GON-FC 与 GON-P3D 的组合将 BarbieGait 平均 Rank-1 从 67.7% 推升至 75.6%（Table 4），两者存在明显的协同增益。

### 端到端信息流

整体信息流可总结为：

```
输入序列 → 视觉阶段(GON-P3D/GON-3D) ×4 → 时序池化 → 水平池化 → GON-FC Head → 身份特征
```

每一步都在强化“去衣物、留运动”的核心目标：GON 在帧级和序列级两次介入，时序卷积保留动态信息，水平分区提供细粒度归一化粒度，最终 GON-FC 完成从局部运动到全局身份的映射。这一设计使 GaitCLIF 在 BarbieGait 九个衣物厚度等级上均显著超越 DeepGaitV2-P3D（AVG Rank-1 80.4% vs 71.7%，Table 3），并在 CCPG、SUSTech1K、Gait3D、GREW 等真实数据集上取得一致提升。

### 补充图表

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/005_Figure_4.jpg]]
*Figure 4: Overview of GaitCLIF. (a) GON, the core normalization unit. (b) GON-P3D and (c) GON-3D, two GON-based visual blocks used in the visual stages of GaitCLIF. (d) GON-FC, a GONenhanced FC block used in the Head of GaitCLIF. (e) The overall GaitCLIF framework for cross-clothing gait recognition*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/002_Figure_2.jpg]]
*Figure 2: The BarbieGait data generation system includes: (a) Skeleton Length and Body Shape Matching maps real humans to virtual ones based on 3D skeleton and body shape using MakeHuman [3]. (b) Random Dressing refers to randomly selecting outfits for cloth-changing. (c) Kinematic Motion Matching refers to the alignment of gait identity information across different outfits of the same real subject. (d) Scene Construction uses Blender [14] to create multiple environments and capture multi-view images. (e) Rendering refers to accelerate image generation using a GPU cluster*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/018_Figure_7.jpg]]
*Figure 7: The illustration of our synthesized images. Our synthetic images are rendered in different scenes, realistic lighting conditions, diverse clothing conditions, and natural occlusions*



GaitCLIF 的核心设计围绕一个关键洞察展开：**衣物对不同身体部位的外观影响程度不同**，因此对特征图按水平分区并分别归一化，能更有效地消除局部衣物外观差异。基于此，方法引入三个紧密协作的模块——Gait-Oriented Normalization（GON）、GON-P3D/GON-3D 时序块和 GON-FC 序列头，形成从帧级到序列级的衣物不变特征学习链路。

### Gait-Oriented Normalization (GON)

GON 是 GaitCLIF 的基础归一化单元，其设计目标是在每一帧内消除衣物特定的统计量，同时保留细粒度的运动细节。与 BatchNorm 在整个批次上计算统计量、InstanceNorm 在单样本空间维度上归一化不同，GON 对特征图的每个水平分区独立执行归一化。

给定输入特征图 $\mathbf{X}$，首先将其沿高度维度水平划分为 $m$ 个区域 $\{x_0, x_1, \dots, x_m\}$。对每个分区 $x_i \in \mathbb{R}^{C \times h_i \times W}$，GON 计算该分区内所有通道和空间位置的均值与标准差：

$$\mu(x_i) = \frac{1}{C h_i W} \sum_{c=1}^{C} \sum_{h=1}^{h_i} \sum_{w=1}^{W} x_{chw}$$

$$\sigma(x_i) = \sqrt{ \frac{1}{C h_i W} \sum_{c=1}^{C} \sum_{h=1}^{h_i} \sum_{w=1}^{W} (x_{chw} - \mu(x_i))^2 }$$

随后对每个分区执行归一化并应用可学习的缩放和平移参数：

$$\mathrm{GON}(x_i) = \gamma \left( \frac{x_i - \mu(x_i)}{\sigma(x_i)} \right) + \beta$$

最终将所有分区的输出沿高度维度拼接，得到衣物不变特征：

$$\mathbf{X}' = \mathbf{GON}(\mathbf{X}) = \mathbf{Cat}(\mathbf{GON}(x_0), \dots, \mathbf{GON}(x_m))$$

这种分区归一化策略的动机在于：上衣、下装、携带物等不同衣物组件在剪影/姿态特征图上对应不同的水平区域，对各区域独立消除统计偏差，可以更精准地抑制局部衣物外观干扰，同时保留跨区域的运动模式差异。

### GON-P3D 与 GON-3D 时序块

为将 GON 的衣物不变特性融入时序建模，GaitCLIF 设计了两种视觉块变体：**GON-P3D** 和 **GON-3D**（Figure 4b, c）。这两种块将 GON 嵌入到时序卷积结构中：

- **GON-P3D**：采用 (2+1)D 卷积范式，将空间卷积与时序卷积分开，在时序分支中引入 GON，使模型在捕捉帧间运动的同时抑制衣物外观漂移。
- **GON-3D**：直接使用 3D 卷积，并在其中集成 GON，以更紧凑的方式联合学习时空特征。

两种块均作为 GaitCLIF 四个视觉阶段的基本构建单元，负责提取经衣物不变归一化增强的时空表示。

### GON-FC 序列头

在视觉阶段完成帧级特征提取后，GaitCLIF 通过时序池化和水平池化将特征聚合为身体部位表示，随后送入 **GON-FC 头**（Figure 4d）进行序列级映射。GON-FC 是一个两层全连接结构，每层 FC 后均施加 GON 归一化。这一设计进一步增强了模型对细粒度运动模式的表达能力，在序列层面强化身份相关特征的衣物不变性。

### 模块协同机制

三个模块形成从局部到全局的级联去衣物流水线：GON 在帧内消除衣物统计偏差，GON-P3D/GON-3D 在时序维度上保持运动一致性，GON-FC 在序列映射阶段再次抑制残留的衣物干扰。消融实验（Table 4）证实了这一协同的有效性：单独使用 GON-P3D 将 BarbieGait 平均 Rank-1 从 67.7% 提升至 69.8%，单独使用 GON-FC 提升至 69.2%，二者组合则达到 75.6%，表明帧级和序列级去衣物机制互为补充。

### 补充图表

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/019_Figure_8.jpg]]
*Figure 8: Visualization of heatmaps in Silhouette-based (a)-(c) and Pose-based methods (d)-(f). (b) and (e) show activation heatmaps of DeepGaitV2 and SkeletonGait overlaid on the silhouette. (c) and (f) show the effect with GaitCLIF*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/004_Figure_3.jpg]]
*Figure 3: Clothing Complexity and Thickness: (a) Silhouette without clothes. (b) Silhouette with clothes. (c) Non-overlapping area between (a) and (b) indicates garment complexity. (d) Distribution of subjects across thickness levels*



## 实验与关键发现

### 主实验结果

#### BarbieGait基准上的性能

BarbieGait数据集按衣物厚度划分为THK0（无衣着）至THK9共10个等级，其中THK0作为Gallery，THK1–THK9作为Probe。表3报告了以预测剪影和2D姿态为输入时各方法的Rank-1准确率与mAP。

**GaitCLIF在所有衣物厚度等级上均取得最优或次优结果。** 具体而言，GaitCLIF-3D的平均Rank-1达到80.4%，平均mAP达到65.7%，相较此前最强的外观类方法**DeepGaitV2-P3D**（71.7% / 60.2%）分别提升+8.7和+5.5个百分点。姿态类方法中，**SkeletonGait**的平均Rank-1仅为58.8%，**DPGait**为67.6%，表明单纯依赖骨架信息难以应对剧烈的衣物外观变化。

值得注意的是，随着衣物厚度从THK1增加至THK9，所有方法的性能均呈下降趋势。GaitCLIF-3D在THK1上的Rank-1为93.2%，而在THK9上降至约58%，揭示了极端厚重衣物（如大衣、背包组合）对步态特征学习的严重干扰。尽管如此，GaitCLIF在每个厚度等级上均保持对DeepGaitV2的显著优势，尤其在THK5–THK9的中高厚度区间，Rank-1提升幅度达8–12个百分点。

GaitCLIF-P3D*使用热力图作为输入（与SkeletonGait的数据处理流程一致），在姿态类方法中取得最佳平均Rank-1（73.4%），验证了GaitCLIF框架对输入模态的泛化能力。

#### 真实换装数据集上的性能

在CCPG和SUSTech1K两个真实换装步态基准上，GaitCLIF同样表现出一致且显著的性能提升（表5）。在CCPG上，GaitCLIF-P3D的平均Rank-1达到84.9%，超越此前最佳的**DPGait**（82.4%）+2.5个百分点。在SUSTech1K上，GaitCLIF-P3D的Overall Rank-1为59.7%，Rank-5为80.4%，相较**SkeletonGait**（50.1% / 72.6%）分别提升+9.6和+7.8个百分点。

在大型野外步态数据集Gait3D和GREW上（表6），GaitCLIF-P3D同样取得最优性能。Gait3D上Rank-1达到76.5%、mAP达到67.9%，相较DeepGaitV2（70.0% / 59.7%）提升+6.5 / +8.2。GREW上Rank-1为80.2%、Rank-5为89.2%，相较DeepGaitV2（74.5% / 85.0%）提升+5.7 / +4.2。这些结果表明，GaitCLIF的衣物不变特征学习能力不仅适用于合成数据，也能有效迁移至真实场景。

#### 额外换装基准上的验证

在HybridGait、OU-ISIR、CCVID、MEVID等补充换装基准上（表9），GaitCLIF相较DeepGaitV2的Rank-1提升幅度在3.5至4.8个百分点之间，进一步验证了方法的鲁棒性和泛化能力。

### 消融实验

#### 核心模块的贡献

表4报告了GaitCLIF-P3D在BarbieGait上的模块消融结果。基线模型（使用标准BatchNorm和单层FC Head）的平均Rank-1为67.7%，mAP为57.6%。单独引入**GON-P3D**（将Gait-Oriented Normalization嵌入(2+1)D卷积块）将Rank-1提升至69.8%（+2.1），单独引入**GON-FC**（双层FC结构配合GON）提升至69.2%（+1.5）。**二者组合**将Rank-1推至75.6%（+7.9），mAP达到63.2%（+5.6），证明了GON在帧级特征归一化和序列级特征映射两个层面的协同作用。

表10进一步按衣物厚度等级分解了各模块的贡献。在THK1–THK3的轻度换装条件下，GON-FC的增益更为显著；而在THK7–THK9的重度换装条件下，GON-P3D的贡献占比更大。这表明GON-P3D主要负责消除由厚重衣物引入的局部外观差异，而GON-FC则在序列层面强化身份相关运动模式的表达。

#### 归一化方式的对比

表11系统比较了GON与BatchNorm（BN）、InstanceNorm（IN）、LayerNorm（LN）在不同衣物厚度等级下的性能。**GON在所有厚度等级上均取得最高的Rank-1和mAP。** 具体而言，在THK9极端条件下，GON的Rank-1为58.2%，而BN仅为48.1%，IN为50.3%，LN为51.7%。GON的优势源于其按水平分区独立计算统计量的设计——不同身体部位受衣物影响的程度不同，分区归一化能更精准地消除局部衣物特定统计量，同时保留细粒度运动细节。

### 跨域迁移分析

表7展示了BarbieGait预训练对真实数据集CCPG的迁移效果。仅使用CCPG训练（Scratch）时，GaitCLIF的Rank-1为94.8%、mAP为77.0%；经过BarbieGait预训练后微调（Pretrain），Rank-1提升至95.8%（+1.0）、mAP提升至79.5%（+2.5）。这一增益验证了BarbieGait合成数据在衣物多样性方面的价值——大规模、多等级的换装合成数据为模型提供了丰富的衣物不变特征先验，有助于在真实数据上更快收敛并获得更好的泛化性能。

### 上游姿态估计的改善

表8报告了使用BarbieGait重新训练的姿态估计器对下游步态识别的影响。在CCPG上，BarbieGait重训练的姿态估计器使GaitCLIF的Rank-1从82.4%提升至84.9%（+2.5）；在SUSTech1K上，Rank-1从56.2%提升至59.7%（+3.5）。这表明BarbieGait提供的多样化合成人体数据不仅能直接用于步态识别训练，还能改善上游姿态估计的质量，从而间接提升下游任务的性能。

### 失败模式与局限性分析

尽管GaitCLIF在多数条件下表现优异，实验仍揭示了若干明显的失败模式：

1. **极端衣物厚度下的性能退化**：在THK9（最厚重衣物等级）条件下，GaitCLIF-3D的Rank-1仅约58%，较THK1下降超过35个百分点。厚重衣物（如长款大衣、大型背包）造成的大面积剪影遮挡严重破坏了步态运动模式的可辨识性，现有归一化策略难以完全恢复被遮挡区域的运动信息。

2. **合成-真实域差距**：尽管BarbieGait预训练能提升真实数据集上的性能，但增益幅度（CCPG上+1.0 Rank-1）相对有限，表明合成数据与真实数据之间仍存在不可忽视的域差异。渲染光照、背景纹理、人体纹理等方面的分布偏移可能限制了预训练特征的直接迁移效果。

3. **对输入质量的依赖**：GaitCLIF的性能依赖于上游剪影提取和姿态估计的质量。在低分辨率、运动模糊或严重遮挡的真实场景中，输入噪声可能被GON的分区归一化过程放大，导致特征判别力下降。

### 可视化分析

图8展示了基于剪影和基于姿态的方法在BarbieGait上的热力图可视化对比。DeepGaitV2和SkeletonGait的激活区域分散在衣物轮廓和背景区域，而GaitCLIF的激活热力图明显聚焦于动态关节区域（如髋、膝、踝），且在不同衣物条件下保持高度一致的空间分布。这一可视化证据直接支持了GaitCLIF的核心设计理念——通过GON消除衣物特定统计量后，模型能够学习到衣物无关的身份相关运动模式。

### 补充图表

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/007_Table_3.jpg]]
*Table 3: Performance comparison on BarbieGait when using predicted silhouette and 2D pose as input. Best result is in bold, and the second-best result is underlined. GaitCLIF-P3D∗ uses heatmaps as input, following the same data processing pipeline as SkeletonGait. In our experiments, THK0 serves as the gallery and THK1-THK9 as probes*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/008_Table_4.jpg]]
*Table 4: Ablation studies for GaitCLIF-P3D on BarbieGait*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/016_Table_11.jpg]]
*Table 11: Comparison of common normalization methods (BN, IN, LN) and our proposed GON across different clothing thickness levels*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/012_Table_7.jpg]]
*Table 7: Cross-domain performance on CCPG using different training strategies. “Scratch” indicates training only on CCPG, while “Pretrain” denotes BarbieGait pretraining followed by CCPG fine-tuning. GaitCLIF refer to P3D-based models*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/009_Table_5.jpg]]
*Table 5: Performance comparison on CCPG and SUSTech1K. For clarity, DeepGaitV2 and GaitCLIF refer to P3D-based models*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/010_Table_6.jpg]]
*Table 6: Performance comparison on Gait3D and GREW. For clarity, DeepGaitV2 and GaitCLIF refer to P3D-based models*

![[assets/figures/papers/paper_list_l1042_https_arxiv_org_abs_2604_12221/figures/015_Table_10.jpg]]
*Table 10: Ablation study of each module under different clothing conditions (THK1-THK9). We report Rank-1 (R1) accuracy and mean Average Precision (mAP) for each variant*



## 定位与知识库关联

### 方法继承与基线关系

GaitCLIF 建立在基于外观的步态识别框架之上，其骨干网络直接继承自 **DeepGaitV2** 的 (2+1)D 卷积架构。在方法谱系上，GaitCLIF 可视为对以下两类基线的统一超越：

**外观类方法**：包括 **GaitSet**、**GaitPart**、**GaitGL** 和 **DeepGaitV2**（含 2D/3D/P3D 变体）。这些方法以剪影序列为输入，通过水平分区和时序聚合学习步态表示。然而，它们在换装场景下的核心瓶颈在于：标准 Batch Normalization 保留了大量衣物特定的统计信息，导致类内外观方差急剧膨胀，模型难以分离身份相关特征与衣物相关特征。GaitCLIF 通过将 BN 替换为 Gait-Oriented Normalization，从根本上改变了特征归一化的统计量计算方式——从全局通道均值/方差转向水平分区内的局部统计量，从而在保留运动细节的同时消除衣物外观干扰。

**姿态类方法**：包括 **GaitGraph**、**GaitGraph2**、**GaitTR**、**GPGait**、**SkeletonGait** 和 **DPGait**。这些方法以人体关键点或骨架图为输入，天然对衣物外观不敏感，但受限于姿态估计精度和运动信息编码能力。在 BarbieGait 上，GaitCLIF-3D 以剪影输入取得 AVG Rank-1 80.4%，大幅超越姿态类最优方法 **SkeletonGait** 的 72.3%（Table 3），证明精心设计的衣物不变特征学习可以在保留外观方法信息丰富度的同时，达到甚至超越姿态方法的换装鲁棒性。

### 核心创新在知识库中的定位

GaitCLIF 的核心贡献在于将“衣物不变性”从数据层面（如域适应、数据增强）提升到**架构设计层面**，具体体现为三个技术槽位的改变：

1. **归一化类型**：从 Batch Normalization 变为 Gait-Oriented Normalization（GON）。GON 受 Layer Normalization 启发，但针对步态数据的水平分区特性设计——对特征图按身体部位进行水平切分后，每个分区独立计算均值 $\mu(x_i)$ 和标准差 $\sigma(x_i)$，再执行通道-空间联合归一化：
   $$\mathrm{GON}(x_i) = \gamma \left( \frac{x_i - \mu(x_i)}{\sigma(x_i)} \right) + \beta$$
   这一设计的关键洞察是：衣物在不同身体部位的影响程度不同（如上衣主要影响躯干区域，裤装影响腿部区域），因此按水平分区分别归一化能更精准地消除局部衣物外观差异。消融实验证实，GON 在所有衣物厚度等级（THK1–THK9）上全面优于 BatchNorm、InstanceNorm 和 LayerNorm（Table 11）。

2. **时序建模块**：从标准 (2+1)D 或 3D 卷积变为 GON-P3D 和 GON-3D 块。这些模块将 GON 嵌入到时序卷积中，使帧级特征学习同时受益于时序运动增强和衣物不变归一化。这种设计在知识库中桥接了“时序建模”与“归一化技术”两个通常独立研究的领域。

3. **头部设计**：从单层分离 FC 变为 GON-FC——两层 FC 结构，每层后施加 GON。这一设计将衣物不变性从帧级特征扩展到序列级特征，强化了身份相关运动模式的表达。

### 适用边界与局限

**已知适用边界**：

- **输入模态**：当前验证覆盖剪影序列和 2D 姿态热力图两种输入。GaitCLIF-P3D* 使用热力图输入时在 BarbieGait 上取得 AVG Rank-1 80.4%（Table 3），表明方法对输入表示具有一定泛化性。但尚未验证对 RGB 图像、深度图或光流等其他模态的直接适用性。
- **数据集规模**：在 BarbieGait（521 个身份，约 120 万序列）、CCPG（200 个身份）、SUSTech1K（1,050 个身份）、Gait3D（3,000 个身份）和 GREW（26,345 个身份）上均验证有效，覆盖从小规模受控场景到大规模野外场景。
- **衣物变化程度**：在 THK1–THK8 衣物厚度等级上表现稳健，但在极端厚重衣物（THK9）条件下性能显著下降——GaitCLIF-3D 的 Rank-1 降至约 58%（Table 3），表明当前方法对剧烈外观遮挡的鲁棒性仍有提升空间。

**明确局限**：

1. **合成-真实域差异**：BarbieGait 预训练后微调 CCPG 虽有增益（Rank-1 从 94.8% 提升至 95.8%，Table 7），但域差异仍然存在。论文未提出专门的域适应机制，仅依赖数据层面的预训练-微调策略。需要额外技术（如域随机化、对抗域适应）来进一步弥合差距。

2. **极端遮挡场景**：GON 依赖水平分区内统计量的稳定性。当衣物极度厚重导致剪影严重变形时，分区内的统计量可能不再可靠，这解释了 THK9 条件下的性能骤降。当前方法缺乏对遮挡区域的显式建模或补偿机制。

3. **隐私限制导致的数据不完整性**：出于隐私保护，BarbieGait 仅公开合成剪影和姿态数据，不提供 RGB 人脸或环境图像。这限制了基于 RGB 外观的步态识别方法在该数据集上的直接训练和公平比较。

### 开放问题

1. **合成-真实域差距的弥合**：GaitCLIF 在合成数据上学习到的衣物不变特征能否通过更好的域随机化策略（如随机化光照、纹理、背景）或基于真实无标注数据的自监督域适应方法，进一步迁移到真实场景？

2. **多模态扩展**：GON 的水平分区归一化策略能否自然地扩展到 RGB 图像输入？对于深度图或光流等提供额外几何/运动线索的模态，GON 的分区策略是否需要调整？

3. **复杂野外场景的鲁棒性**：在严重遮挡、多目标交互、极端视角等更复杂的野外场景下，GaitCLIF 的衣物不变特征是否依然有效？水平分区策略在人体不完整或被遮挡时如何自适应调整？

4. **衣物属性的语义化建模**：当前衣物厚度等级仅基于剪影非重叠区域面积定义，是一种粗粒度的几何度量。是否可以引入更语义化的衣物属性（如风格、材质、宽松度）来指导特征学习，使模型理解不同衣物类型的干扰模式差异？

5. **归一化策略的理论理解**：GON 为何优于 IN 和 LN 的理论分析尚不充分。IN 在风格迁移中有效消除实例特定统计量，LN 在 Transformer 中稳定训练——GON 在步态换装场景下的优势是否源于其“局部身体部位”的归纳偏置与步态运动结构的对齐？这需要更深入的理论或实证分析。



## 原文 PDF

![[paperPDFs/CVPR_2026/BarbieGait_An_Identity_Consistent_Synthetic_Human_Dataset_with_Versatile_Cloth_Changing_for_Gait_Recognition.pdf]]
