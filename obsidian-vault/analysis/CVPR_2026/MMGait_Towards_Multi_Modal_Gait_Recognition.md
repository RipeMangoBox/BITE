---
title: "MMGait: Towards Multi-Modal Gait Recognition"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MMGait_Towards_Multi_Modal_Gait_Recognition.pdf
project_link: null
code_link: "https://github.com/BNU-IVC/MMGait"
aliases:
- MMGait
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过构建覆盖12种模态、5类传感器的大规模多模态步态数据集MMGait，并设计一个可统一处理单模态、跨模态与多模态识别任务的OmniGait共享嵌入框架，实现了异构模态的联合建模与融合。
primary_logic: 模态特定编码、自适应门控交叉模态融合与共享骨干网络相结合，使单一模型能够灵活支持任意模态间的检索与融合；多传感器几何/光度/运动信息的联合利用，大幅提升了对干扰（特别是更换衣物）的鲁棒性。
claims:
- 单模态下结构型模态（LiDAR、深度）在跨服装条件下表现突出，而4D雷达等稀疏模态性能有限。
- 跨模态检索面临严峻的跨服装退化，但融合RGB与LiDAR投影深度可在跨服装场景带来+19.7%的Rank-1提升。
- OmniGait统一了9种图像化模态的单/跨/多模态识别，仅需9.96M参数，并在跨数据集零样本迁移中验证了融合的有效性。
- "MMGait 上 Rank-1 accuracy (NM / BG / CL) = RGB: 99.7 / 99.1 / 60.7; Silhouette: 98.5 / 96.4 / 61.0; Li..."
---

# MMGait: Towards Multi-Modal Gait Recognition

> [!tip] 核心洞察
> 模态特定编码、自适应门控交叉模态融合与共享骨干网络相结合，使单一模型能够灵活支持任意模态间的检索与融合；多传感器几何/光度/运动信息的联合利用，大幅提升了对干扰（特别是更换衣物）的鲁棒性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MMGait：迈向多模态步态识别 |
| 英文题名 | MMGait: Towards Multi-Modal Gait Recognition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.15979) · [Code](https://github.com/BNU-IVC/MMGait) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | OmniGait |
| Dataset | MMGait |

> [!tip] 效果简介
> - MMGait 上，Rank-1 accuracy (NM / BG / CL) RGB: 99.7 / 99.1 / 60.7; Silhouette: 98.5 / 96.4 / 61.0; LiDAR Point Cloud: 97.... vs 各个模态的最佳单模态基线（Table 4） (见Table 4)。
> - MMGait (跨模态检索) 上，Rank-1 accuracy (NM average / CL average) 跨模态平均NM 55.5% (5种传感器双向), CL平均28.4% vs 独立训练的跨模态模型（Table 5） (RGB→Depth NM: 76.1%, CL仅30.1%)。
> - MMGait (多模态融合) 上，CL Rank-1 improvement over single-modal baseline RGB(Sil.) + LiDAR(Proj. Depth): +19.7% vs 单模态RGB Silhouette CL 61.0% (+19.7%)。

## 概述

步态识别因其远距离、非配合的特性，在安防与身份认证中具有独特优势。然而，现有步态基准几乎完全依赖 RGB 轮廓或少数传感器（如 LiDAR），无法支撑**异构模态的统一建模与跨传感器检索**，导致多模态互补信息——特别是几何、光度与运动线索——未被充分利用。

针对这一瓶颈，本文提出两项核心贡献：

1. **MMGait 数据集**：首个大规模多模态步态基准，覆盖 5 类传感器（RGB 相机、事件相机、红外相机、LiDAR、4D 毫米波雷达），衍生出 12 种模态，包含 10 个视角与 3 种行走条件（正常、背包、换装），为跨模态与多模态步态研究提供了系统性的评估平台。

2. **OmniGait 统一框架**：一个仅需 **9.96M 参数**的共享嵌入模型，能够灵活支持**单模态识别、跨模态检索与多模态融合**三类任务，无需为每对模态单独训练。其核心设计包括模态特定浅层编码器、自适应门控跨模态融合模块以及共享残差骨干网络，使得单一模型即可在任意模态间进行双向检索。

**关键实验发现**：

- 在单模态条件下，结构型模态（LiDAR 点云、深度图）在**换装（CL）场景**中表现突出（LiDAR 点云 CL Rank-1 达 76.6%），而 RGB 轮廓仅 61.0%；4D 雷达等稀疏模态性能有限。
- 跨模态检索在换装条件下退化严重：以 RGB 为中心，跨 5 种传感器双向检索的平均 CL Rank-1 仅 28.4%，远低于正常条件的 55.5%。
- 多模态融合可显著缓解换装退化：将 RGB 轮廓与 LiDAR 投影深度融合，CL Rank-1 提升 **+19.7%**；跨传感器融合（RGB+深度/LiDAR）带来的增益远大于传感器内融合（RGB+事件/姿态），印证了几何与外观信息的强互补性。
- OmniGait 在 9 种图像化模态上以统一模型逼近甚至匹配各模态专用模型的性能，并在跨数据集零样本迁移（MMGait → SUSTech1K）中验证了融合策略的泛化能力。

**方法定位与知识库锚点**：OmniGait 属于**共享嵌入空间的多模态融合架构**，区别于传统的独立双流模型（如为 RGB↔深度单独训练的 GaitBase 双流）或简单拼接/平均融合（如 MultiGait++）。其轻量门控融合与跨模态批次归一化设计，为全模态步态识别提供了可扩展的基线。

**局限与开放问题**：MMGait 未实现严格的帧级跨传感器时间同步；OmniGait 将 3D 点云投影为深度图，损失了部分原始几何结构；换装场景下的性能缺口仍是核心挑战。未来方向包括直接建模原始 3D 点云、联合优化跨模态对齐与协变量鲁棒性，以及在更复杂的现实部署中验证泛化能力。

## 背景与动机

### 步态识别的多模态机遇与瓶颈

步态识别作为一种远距离、非受控的生物特征识别技术，在安防监控、嫌疑人追踪和身份认证等场景中具有独特优势。然而，现有步态识别研究长期受限于单一或少数传感器的数据范式——绝大多数基准数据集仅覆盖RGB相机采集的轮廓（silhouette）序列，少数工作延伸至LiDAR点云或深度图，但始终缺乏一个能够系统性覆盖异构传感器、支持统一建模的大规模多模态平台。

这种数据层面的局限直接导致了方法层面的瓶颈：**现有步态识别模型通常为每种模态单独训练独立网络**（如 **GaitBase**、**GaitSet**、**GaitPart**、**GaitGL** 等基于轮廓的方法，以及 **LidarGait++** 等基于点云的方法），不同模态之间的互补信息无法被联合利用。当面临跨模态检索需求时——例如用RGB图像查询LiDAR点云库中的行人——必须为每一对模态训练单独的双流模型，系统复杂度和部署成本随模态数量呈平方级增长。更重要的是，单模态系统对协变量干扰（尤其是更换衣物）的鲁棒性存在天然天花板：RGB轮廓在跨服装（CL）条件下性能急剧下降，而LiDAR等结构型模态虽对服装变化不敏感，却无法独立提供外观判别信息。

### 核心洞察：异构模态的互补性

不同传感器捕捉的步态信息具有本质上的互补性：
- **RGB相机**提供丰富的外观纹理和轮廓形状，但对光照、服装变化敏感；
- **LiDAR和深度传感器**直接获取三维几何结构，对服装变化鲁棒，但缺乏纹理身份线索；
- **事件相机**捕捉高速运动边缘，具有极高的时间分辨率；
- **红外热成像**对光照不敏感，可在夜间工作；
- **4D毫米波雷达**提供稀疏但包含速度信息的三维点云。

这些模态在几何、光度和运动维度上的信息互补，暗示着一个关键假设：**联合利用多传感器信息可以大幅提升步态识别系统对干扰（特别是更换衣物）的鲁棒性**。然而，由于缺乏一个同时覆盖多种传感器、提供统一评估协议的大规模数据集，这一假设此前无法被系统验证。

### MMGait数据集与OmniGait框架的提出

为填补上述空白，本文提出了**MMGait**——首个大规模多模态步态识别基准数据集。MMGait集成了**5类传感器**（RGB相机、事件相机、红外相机、LiDAR、4D毫米波雷达），覆盖**12种模态表示**（包括RGB图像、轮廓、2D/3D姿态、深度图、LiDAR投影深度、事件帧、红外图像、4D雷达点云等），在**10个视角**和**3种行走条件**（正常NM、背包BG、更换衣物CL）下采集了大规模行人数据。

在此基础上，本文进一步提出了一个新的任务范式——**全模态步态识别（Omni Multi-Modal Gait Recognition）**，目标是构建一个统一模型，能够接受任意模态作为查询，并从任意模态的图库中检索目标。为支撑该任务，本文设计了**OmniGait**基线框架，通过模态特定编码、自适应门控跨模态融合与共享骨干网络相结合，使单一模型能够灵活支持单模态识别、跨模态检索与多模态融合，仅需**9.96M参数**即可处理全部9种图像化模态。

### 本文的核心贡献

1. **大规模多模态基准**：构建了覆盖5类传感器、12种模态的MMGait数据集，为异构步态识别研究提供了统一的评估平台。
2. **全模态识别任务定义**：首次形式化Omni Multi-Modal Gait Recognition任务，支持任意模态间的双向检索与融合。
3. **统一基线OmniGait**：提出轻量、可扩展的统一框架，在单模态、跨模态和多模态场景下均展现出竞争力。

## 核心创新

### 创新动机：从单模态孤岛到全模态统一

现有步态识别基准（如CASIA-B、OUMVLP、SUSTech1K等）通常仅覆盖RGB相机和LiDAR等少数传感器，各模态独立训练独立模型，无法支持异构模态的统一建模与跨传感器检索。这种“模态孤岛”范式导致多模态互补性——特别是几何结构信息（LiDAR/深度）与外观纹理信息（RGB/IR）的联合增益——未得到充分利用。MMGait工作的核心洞察在于：**模态特定编码、自适应门控交叉模态融合与共享骨干网络相结合，使单一模型能够灵活支持任意模态间的检索与融合；多传感器几何/光度/运动信息的联合利用，大幅提升了对干扰（特别是更换衣物）的鲁棒性。**

### 关键创新点（Changed Slots）

相对于现有基线，OmniGait在以下四个维度实现了根本性改变：

| 创新维度 | 基线做法 | OmniGait做法 | 证据锚点 |
|---------|---------|-------------|---------|
| **模态建模方式** | 各模态单独训练独立模型（如GaitBase per modality） | 共享骨干网络 + 模态专属浅层编码器，支持9种图像化模态的统一处理 | Section 4.1 |
| **跨模态检索机制** | 为每一对模态训练单独的双流模型（例如RGB↔深度需独立训练） | 单一OmniGait模型即可在任意模态对之间进行双向检索 | Section 4.1 |
| **多模态融合方法** | 简单拼接或双流特征平均（如MultiGait++） | 轻量自适应门控融合模块 + 残差连接 | Section 4.1 |
| **训练批次组织** | 模态内独立批次 | 单模态与融合特征共享批次，促进BatchNorm层学习跨模态统计量 | Section 4.1 |

### 创新一：模态特定浅层编码 + 共享深层骨干

OmniGait为每种图像化模态（RGB、轮廓、深度图、IR、事件帧、投影深度等）设计独立的浅层编码器 $\varepsilon_m$，将原始输入 $\mathbf{X}_m$ 映射为统一尺寸的特征图：

$$f_m = \varepsilon_m(\mathbf{X}_m), \quad f_m \in \mathbb{R}^{T \times C_1 \times H_1 \times W_1}$$

这些模态特定编码器仅包含少量卷积层，负责保留各模态固有的物理特性（如RGB的纹理、深度的几何结构），而后续的共享残差骨干网络 $E(\cdot)$ 则处理所有单模态和融合后的特征，学习跨模态统一的步态表示：

$$\mathbf{F} = E(\{f_m, f_{i,j}^{\mathrm{fused}}\}), \quad \mathbf{F} \in \mathbb{R}^{T \times C_2 \times H_2 \times W_2}$$

这一设计的核心优势在于：**共享骨干使得BatchNorm层能够从多模态混合批次中学习更鲁棒、更泛化的统计量**，从而隐式实现模态间的特征空间对齐，无需额外的对抗训练或显式对齐损失。

### 创新二：自适应门控跨模态融合模块

与MultiGait++等基线使用的简单拼接或双流特征平均不同，OmniGait设计了一个轻量级的自适应门控融合模块。给定两个模态的特征 $f_i$ 和 $f_j$，首先在通道维拼接并通过 $1\times1$ 卷积进行初步融合：

$$f_{i,j} = \mathbf{Conv}_{1\times1}(\mathbf{Concat}([f_i, f_j], \mathrm{dim}=1))$$

随后，通过全局平均池化和 $1\times1$ 卷积生成2维门控权重并归一化：

$$\mathbf{w} = \mathrm{Softmax}(G(f_{i,j})), \quad \mathbf{w} \in \mathbb{R}^2$$

最终的融合特征通过残差连接将门控加权后的模态特征与卷积融合结果相加：

$$f_{i,j}^{\mathrm{fused}} = f_{i,j} + \sum_{m=1}^2 \mathbf{w}_m f_m$$

这种设计使模型能够**自适应地平衡两个模态的贡献**——例如，在跨服装场景下，当RGB外观信息不可靠时，模型可以自动增大对LiDAR投影深度等几何模态的依赖权重。

### 创新三：统一全模态检索范式

OmniGait提出的“Omni Multi-Modal Gait Recognition”任务定义了一个全新的检索范式：**单一模型接受任意模态作为查询，从任意模态的数据库中检索目标**。这与传统跨模态检索（需为每对模态训练独立模型）有本质区别。

训练时采用对称跨模态三元组损失，锚点来自一种模态，正负样本来自另一种模态：

$$L_{\mathrm{cross-triplet}} = \frac{1}{2} \big( L_{\mathrm{triplet}} \big( A_{\mathrm{modal1}}, P_{\mathrm{modal2}}, N_{\mathrm{modal2}} \big) + L_{\mathrm{triplet}} \big( A_{\mathrm{modal2}}, P_{\mathrm{modal1}}, N_{\mathrm{modal1}} \big) \big)$$

配合标准交叉熵分类损失的均值 $L_{\mathrm{ce}} = \frac{1}{2} ( L_{\mathrm{ce}}^{\mathrm{modal1}} + L_{\mathrm{ce}}^{\mathrm{modal2}} )$，总损失为两者的平均：

$$L_{\mathrm{total}} = \frac{1}{2} ( L_{\mathrm{cross-triplet}} + L_{\mathrm{ce}} )$$

在推理阶段，共享骨干 $E(\cdot)$ 支持任意模态特征输入，使OmniGait无需额外开销即可兼容单模态、跨模态和多模态三种任务范式。

### 创新四：极轻量的统一架构

OmniGait仅使用**9.96M参数**即可支撑全部9种图像化模态的单模态识别、任意模态对之间的跨模态检索以及多模态融合任务（Table 9）。这一参数量远低于为每对模态训练独立双流模型的总开销，证明了统一框架在可扩展性上的显著优势。

## 整体框架

OmniGait 的整体设计遵循“模态特定编码 → 自适应跨模态融合 → 共享表示学习”的三阶段流水线，目标是以单一模型统一处理单模态识别、跨模态检索与多模态融合三类任务。其核心逻辑在于：让每种模态保留自身物理特性的同时，通过共享骨干网络将所有模态的特征映射到同一个嵌入空间，从而消除为每一对模态单独训练模型的开销。

**输入层**：OmniGait 当前支持 9 种图像化模态（包括 RGB 图像、轮廓、红外、事件、投影深度图等），所有模态统一缩放至 64×64 分辨率，以序列形式送入模型。

**第一阶段：模态特定编码器 (εₘ)**。每种模态拥有独立的浅层编码器，将原始输入 Xₘ 映射为特征图：

$$
f_m = \varepsilon_m(\mathbf{X}_m), \quad f_m \in \mathbb{R}^{T \times C_1 \times H_1 \times W_1}
$$

这些编码器仅负责提取模态固有的底层模式，不进行跨模态交互，从而保留各传感器的物理特性（如几何结构、光度信息、运动线索）。

**第二阶段：自适应门控跨模态融合模块**。当需要融合两个模态时，首先将它们的特征在通道维拼接，并通过 1×1 卷积进行初步融合：

$$
f_{i,j} = \mathbf{Conv}_{1\times1}(\mathbf{Concat}([f_i, f_j], \mathrm{dim}=1))
$$

随后，对融合特征施加全局平均池化与 1×1 卷积，经 Softmax 得到二维门控权重：

$$
\mathbf{w} = \mathrm{Softmax}(G(f_{i,j})), \quad \mathbf{w} \in \mathbb{R}^2
$$

最终的融合特征由门控加权的模态特征与卷积融合结果通过残差连接组合而成：

$$
f_{i,j}^{\mathrm{fused}} = f_{i,j} + \sum_{m=1}^2 \mathbf{w}_m f_m, \quad f_{i,j}^{\mathrm{fused}} \in \mathbb{R}^{T \times C_1 \times H_1 \times W_1}
$$

这种轻量设计使模型能自适应地平衡两个模态的贡献，而非简单拼接或平均。

**第三阶段：共享骨干网络 E(·)**。所有单模态特征与融合特征被送入同一个残差骨干网络：

$$
\mathbf{F} = E(\{f_m, f_{i,j}^{\mathrm{fused}}\}), \quad \mathbf{F} \in \mathbb{R}^{T \times C_2 \times H_2 \times W_2}
$$

关键设计在于：单模态与融合特征在同一个批次内共同处理，使得 BatchNorm 层能够学习跨模态的统计量，从而增强表示的泛化性和模态不变性。最终输出的特征 F 经过时序池化后，即可用于任意模态间的检索或分类。

**训练损失**：OmniGait 同时优化单模态交叉熵损失与对称跨模态三元组损失。跨模态三元组损失以锚点来自一种模态、正负样本来自另一种模态的方式促进模态不变表示：

$$
L_{\mathrm{cross-triplet}} = \frac{1}{2} \big( L_{\mathrm{triplet}} ( A_{\mathrm{modal1}}, P_{\mathrm{modal2}}, N_{\mathrm{modal2}} ) + L_{\mathrm{triplet}} ( A_{\mathrm{modal2}}, P_{\mathrm{modal1}}, N_{\mathrm{modal1}} ) \big)
$$

总损失为跨模态三元组损失与组合交叉熵损失的平均：

$$
L_{\mathrm{total}} = \frac{1}{2} \left( L_{\mathrm{cross-triplet}} + L_{\mathrm{ce}} \right)
$$

**与基线方法的关键差异**：传统方案（如 GaitBase、GaitSet、GaitPart、GaitGL、DeepGaitV2-P3D）通常为每种模态单独训练独立模型；跨模态检索则需要为每一对模态训练独立的双流模型（如 MultiGait++ 的扩展）。OmniGait 通过共享骨干与轻量门控融合，仅用 9.96M 参数即可支撑全部 9 种模态的单/跨/多模态任务，且跨模态检索性能在正常和背包条件下优于独立训练的双流模型（见 Figure 6）。

**当前局限**：OmniGait 目前将 3D 点云投影为深度图以纳入统一图像框架，这一操作损失了部分原始几何结构；此外，统一模型在 4D 雷达和 3D 姿态等稀疏或结构化模态上的单模态性能仍明显弱于专用模型。

### 补充图表

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/009_Figure_5.jpg]]
*Figure 5: Overview of the OmniGait framework, including modalspecific encoding, adaptive cross-modal fusion, and shared representation learning to flexibly handle single-modal, cross-modal, and multi-modal gait recognition*

## 核心模块与公式推导

OmniGait 框架围绕一个核心洞察展开：**模态特定浅层编码保留物理特性，共享深层骨干学习跨模态不变表示，轻量门控融合实现自适应互补**。整个框架由三个关键模块串联构成，其整体结构如 **Figure 5** 所示。

### 模态特定编码器

对于每一种图像化模态输入 $\mathbf{X}_m$（如 RGB 图像、轮廓图、深度投影图等），框架首先使用独立的浅层编码器 $\varepsilon_m$ 提取模态特定特征：

$$f_m = \varepsilon_m(\mathbf{X}_m), \quad f_m \in \mathbb{R}^{T \times C_1 \times H_1 \times W_1}$$

其中 $T$ 为序列帧数，$C_1$、$H_1$、$W_1$ 分别为特征图的通道数、高度和宽度。该设计的因果逻辑在于：不同模态的底层统计特性差异显著（如 RGB 的光度信息 vs. 深度图的几何结构），强制共享早期层会抹杀模态固有的判别线索。因此，$\varepsilon_m$ 仅由少量卷积层构成，其作用是保留模态原始物理特性，为后续融合提供高质量的模态专属表征。

### 自适应门控跨模态融合模块

给定两个模态的特征 $f_i$ 和 $f_j$，融合模块首先在通道维度上进行拼接，并通过 $1\times1$ 卷积进行初步信息交换：

$$f_{i,j} = \mathbf{Conv}_{1\times1}(\mathbf{Concat}([f_i, f_j], \mathrm{dim}=1))$$

随后，通过一个轻量门控网络 $G$ 自适应地学习两个模态的贡献权重。该网络对 $f_{i,j}$ 执行全局平均池化后接 $1\times1$ 卷积，输出一个 2 维向量并经 Softmax 归一化：

$$\mathbf{w} = \mathrm{Softmax}(G(f_{i,j})), \quad \mathbf{w} \in \mathbb{R}^2$$

最终的融合特征通过残差连接将门控加权后的原始模态特征与卷积融合结果相加得到：

$$f_{i,j}^{\mathrm{fused}} = f_{i,j} + \sum_{m=1}^2 \mathbf{w}_m f_m, \quad f_{i,j}^{\mathrm{fused}} \in \mathbb{R}^{T \times C_1 \times H_1 \times W_1}$$

这一设计的因果机制体现在两个层面：**门控权重 $\mathbf{w}$ 使模型能够根据输入模态对的互补性强弱动态调节融合比例**（例如，当 RGB 与 LiDAR 投影深度融合时，几何模态在跨服装场景下自动获得更高权重）；**残差连接保证了即使门控失效，卷积融合路径仍能传递基础信息**，避免梯度消失。该模块仅引入极少量参数，却实现了传感器内与传感器间融合的自适应平衡。

### 共享表示学习骨干

融合模块输出的 $f_{i,j}^{\mathrm{fused}}$ 与各模态的单模态特征 $f_m$ 被一同送入共享骨干网络 $E(\cdot)$：

$$\mathbf{F} = E(\{f_m, f_{i,j}^{\mathrm{fused}}\}), \quad \mathbf{F} \in \mathbb{R}^{T \times C_2 \times H_2 \times W_2}$$

共享骨干采用残差网络结构，其关键设计在于**单模态特征与融合特征在同一批次内共同处理**。这意味着 BatchNorm 层在训练过程中学习的是跨模态的联合统计量，而非某一模态的局部分布。这一机制使得 $E(\cdot)$ 输出的嵌入空间能够自然地支持任意模态间的距离度量，无需为每对模态单独训练模型。

### 损失函数设计

训练过程由两个对称的损失项联合驱动。**跨模态三元组损失**确保不同模态的同类身份特征在共享空间中彼此靠近：

$$L_{\mathrm{cross-triplet}} = \frac{1}{2} \big( L_{\mathrm{triplet}} ( A_{\mathrm{modal1}}, P_{\mathrm{modal2}}, N_{\mathrm{modal2}} ) + L_{\mathrm{triplet}} ( A_{\mathrm{modal2}}, P_{\mathrm{modal1}}, N_{\mathrm{modal1}} ) \big)$$

其中锚点 $A$ 来自一种模态，正样本 $P$ 和负样本 $N$ 来自另一种模态。对称设计使两个方向的跨模态对齐同时得到优化。**交叉熵分类损失**则维护单模态内部的判别性：

$$L_{\mathrm{ce}}^{\mathrm{modal}} = - \sum_{i=1}^{c} y_i \log(\hat{y}_i), \quad L_{\mathrm{ce}} = \frac{1}{2} \left( L_{\mathrm{ce}}^{\mathrm{modal1}} + L_{\mathrm{ce}}^{\mathrm{modal2}} \right)$$

最终总损失为两者的均衡组合：

$$L_{\mathrm{total}} = \frac{1}{2} \left( L_{\mathrm{cross-triplet}} + L_{\mathrm{ce}} \right)$$

该损失函数的因果逻辑在于：三元组损失拉近跨模态同类特征、推远异类特征，构建模态不变空间；交叉熵损失确保每个模态内部的类间可分性。两者的均衡权重使模型在单模态判别力与跨模态对齐之间取得平衡，避免任一方过度主导导致另一方退化。

### 模块协同的因果链条

上述三个模块形成一条清晰的因果链：**模态特定编码器 $\to$ 自适应门控融合 $\to$ 共享骨干 $\to$ 统一嵌入空间**。这一链条解释了 OmniGait 为何能以仅 9.96M 参数（Table 9）同时支撑单模态识别、跨模态检索和多模态融合三类任务：浅层编码器保留了各模态的物理特异性，门控融合按需组合互补信息，共享骨干则将异构表征映射到同一度量空间，使任意模态对之间的检索无需额外适配。

## 实验与分析

### 数据集与基准构建

MMGait 数据集覆盖 **5 类传感器**（RGB 相机、事件相机、红外相机、LiDAR、4D 毫米波雷达），衍生出 **12 种模态**，包含多视角、多协变量（正常 NM、背包 BG、换衣 CL）的步态序列。传感器规格与对应模态详见 Table 1，采集布置见 Figure 2。与现有步态数据集的对比（Table 2）表明，MMGait 是首个同时覆盖如此多异构传感器的大规模多模态步态基准。

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/003_Table_1.jpg]]
*Table 1: Specifications of sensing devices and corresponding modalities in MMGait*

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/004_Table_2.jpg]]
*Table 2: Comparison of existing gait recognition datasets with various capture sensors*

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/002_Figure_2.jpg]]
*Figure 2: The collection*

评估协议统一：所有图像化模态输入分辨率固定为 64×64，训练/测试集划分为 200/525 个身份；NM-01 视角为 gallery，NM-02/BG-01/CL-01 视角为 query，排除同视角对。点云模态使用 512 点/帧的采样配置。

### 单模态识别性能

#### 经典模态：轮廓与姿态

Table 3 报告了基于轮廓和姿态的主流方法在 MMGait 上的性能。基于轮廓的 **GaitBase** 在换衣（CL）条件下取得最高 Rank-1（61.0%），而基于姿态的 **DeepGaitV2-P3D** 在正常（NM）条件下达到 98.7%。这一对比揭示了不同模态表征在不同协变量下的互补优势：轮廓对衣着变化更鲁棒，姿态在正常行走时判别力更强。

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/005_Table_3.jpg]]
*Table 3: Baseline performance of silhouette- and pose-based gait recognition methods on MMGait. Results are reported in %. Bold numbers indicate the best performance within each modality*

#### 新兴模态：多传感器分析

Table 4 展示了各新兴模态的单模态识别结果。核心发现：

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/007_Table_4.jpg]]
*Table 4: Recognition performance across diverse and emerging gait sensing modalities. Results are reported in %. Bold numbers indicate the best performance within each sensor type*

- **结构型模态在跨服装条件下优势显著**：LiDAR 点云在 CL 条件下 Rank-1 达 76.6%，红外图像达 78.8%，远超 RGB 图像（60.7%）和轮廓（61.0%）。这表明深度几何信息和热辐射信息对衣着变化具有天然鲁棒性。
- **RGB 衍生模态在正常条件下表现最优**：RGB 图像和轮廓在 NM 条件下分别达到 99.7% 和 98.5%，但在 CL 条件下急剧退化，暴露了外观特征对衣着的敏感性。
- **稀疏模态性能有限**：4D 雷达投影深度在所有条件下性能均较低（NM 仅 13.2%），说明当前稀疏点云表征的判别力不足，需进一步探索更有效的建模方式。

### 跨模态检索

Table 5 和 Figure 4 报告了以 RGB 为中心的跨模态检索结果。采用双流框架（模态特定浅层编码器 + 共享深层骨干），联合优化交叉熵损失与跨模态三元组损失。

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/006_Table_5.jpg]]
*Table 5: RGB-Centered Cross-Modal Retrieval. Results are reported in %*

核心瓶颈：**跨模态检索面临严峻的跨服装退化**。五类传感器双向检索的平均 Rank-1 从 NM 的 55.5% 骤降至 CL 的 28.4%。具体而言：
- RGB(轮廓) → 红外(轮廓) 在 NM 下可达 95.7%，但 CL 下仅 45.3%。
- RGB(轮廓) → 深度 和 RGB(轮廓) → LiDAR(投影深度) 在 CL 下分别仅 30.1% 和 35.6%。
- 4D 雷达作为检索源几乎不可用（RGB→4D 雷达 CL 仅 2.2%）。

这一退化模式表明：**跨模态检索的核心难点并非模态间的语义鸿沟本身，而是协变量（特别是衣着）变化导致的外观-几何对应关系崩溃**。正常和背包条件下模态间共享的步态模式尚可对齐，但换衣后各模态捕捉的身份线索发生差异化偏移，使得跨模态匹配极度困难。

### 多模态融合

Table 6 对比了传感器内（Intra-Sensor）和传感器间（Inter-Sensor）的多模态融合性能。基线为单模态 RGB 轮廓（CL Rank-1 61.0%）。

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/008_Table_6.jpg]]
*Table 6: Performance comparison under Intra- and Inter-Sensor settings. Green numbers denote improvement over the baseline*

关键发现：
- **传感器内融合收益有限**：RGB 轮廓 + 事件（+1.1%）、RGB 轮廓 + 姿态（+3.0%），提升幅度较小。这是因为这些模态均源自同一 RGB 传感器，信息冗余度较高。
- **传感器间融合收益显著**：RGB 轮廓 + LiDAR 投影深度在 CL 条件下提升 **+19.7%**（达到 80.7%），RGB 轮廓 + 深度提升 +14.0%。几何信息（深度/LiDAR）与外观信息（RGB/轮廓）形成强互补，几何线索对衣着变化不敏感，有效弥补了外观特征的失效。
- **融合收益与模态互补性正相关**：外观模态 + 几何模态 > 外观模态 + 外观模态，验证了多传感器融合的核心价值在于**跨物理特性的信息互补**。

### OmniGait 统一框架评估

#### 单模态统一建模

Table 7 展示了 OmniGait 在 9 种图像化模态上的单模态性能。OmniGait 通过共享骨干网络和模态特定浅层编码器，以单一模型（仅 9.96M 参数，Table 9）同时处理所有模态。

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/011_Table_7.jpg]]
*Table 7: Single-Modal Recognition performance of OmniGait across different modalities. Results are reported in %. Bold numbers indicate the best performance within each sensor type*

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/015_Table_9.jpg]]
*Table 9: Parameters and FLOPs for different models evaluated in our experiments*

结果分析：
- 在多数模态上，OmniGait 的统一模型性能接近甚至匹配专用模型（对比 Table 4）。例如，RGB 轮廓 NM 98.1%（专用 GaitBase 98.5%），LiDAR 投影深度 CL 73.2%（专用 76.6%）。
- 但在部分稀疏/弱模态上差距明显：4D 雷达投影深度 CL 仅 6.4%，3D 姿态 CL 仅 19.0%。这表明**共享骨干对弱模态的适应性不足**，统一架构在模态间性能均衡方面仍有较大提升空间。

#### 多模态融合

Table 8 报告了 OmniGait 在统一框架下的多模态融合性能。与专用双流融合（Table 6）相比：
- RGB(轮廓) + LiDAR 在 CL 条件下提升 +6.0%（基线 OmniGait 单模态 RGB 轮廓 CL 44.9%）。
- RGB(RGB 图像) + 轮廓提升 +19.8%，体现了统一框架内模态间协同的潜力。
- 融合增益的模式与专用模型一致：传感器间融合 > 传感器内融合。

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/010_Table_8.jpg]]
*Table 8: OmniGait performance under intra- and inter-sensor settings. Green numbers denote improvement over the baseline*

#### 跨模态检索对比

Figure 6 对比了 OmniGait 统一模型与独立训练的双流模型在跨模态检索上的性能。OmniGait 通过共享批次归一化（所有单模态和融合特征在同一批次中处理），使 BatchNorm 层学习跨模态统计量，在 NM 和 BG 条件下优于独立双流模型。但在 CL 条件下优势缩小，说明**统一批次归一化对协变量鲁棒性的帮助有限**，CL 场景仍是核心挑战。

### 跨数据集零样本迁移

Table 10 报告了 OmniGait 在 SUSTech1K 数据集上的零样本迁移结果（仅在 MMGait 训练，不做微调）。融合模型在跨数据集场景下仍保持正向增益，验证了 OmniGait 学习到的多模态互补策略具有一定的泛化性，而非对 MMGait 特定分布过拟合。

![[assets/figures/papers/paper_list_l1069_https_arxiv_org_abs_2604_15979/figures/016_Table_10.jpg]]
*Table 10: Cross-dataset evaluation on SUSTech1K. OmniGait is trained on MMGait and directly evaluated without fine-tuning*

### 消融与效率分析

- **跨传感器 vs. 传感器内融合**（Table 6, Table 8）：跨传感器融合的 CL 增益（+14.0% 至 +19.7%）远超传感器内融合（+1.1% 至 +3.0%），确证**几何-外观互补是核心驱动因素**。
- **统一批次归一化**（Figure 6）：共享批次统计量在 NM/BG 条件下提升跨模态检索性能，但在 CL 条件下增益微弱，提示需要针对协变量鲁棒性的专门设计。
- **模型效率**（Table 9）：OmniGait 仅需 9.96M 参数即可支撑全部单模态、跨模态和多模态任务，相比为每对模态训练独立双流模型，参数效率提升一个数量级以上。

### 失败模式与局限

1. **跨服装（CL）退化是全局性瓶颈**：无论单模态、跨模态还是多模态融合，CL 条件下性能均大幅下降。即使最优的传感器间融合（+19.7%），CL 绝对性能（80.7%）仍远低于 NM（>97%），表明衣着变化对步态识别的根本性挑战尚未解决。
2. **稀疏模态建模不足**：4D 雷达和 3D 姿态在统一框架中的性能显著弱于专用模型，将点云投影为深度图损失了原始几何结构，且共享骨干难以同时适配稠密和稀疏表征。
3. **统一模型内的模态间性能不均衡**：强模态（RGB、轮廓）接近专用模型，弱模态（4D 雷达、3D 姿态）差距明显，全模态联合训练可能引入负迁移。
4. **时间同步精度受限**：MMGait 未在异构传感器间实施严格的帧级时间同步（仅序列级对齐），可能影响需要精确时序对齐的跨模态融合方法。此点需在后续版本中手动验证实际影响程度。

## 方法谱系与知识库定位

### 1. 单模态步态识别基线谱系

MMGait论文在轮廓（silhouette）和姿态（pose）两种传统模态上评估了多个代表性基线，构成了单模态方法谱系的上游参照。

**轮廓基方法**：以 **GaitBase** 为简洁高效的默认基线，同时纳入经典方法 **GaitSet**、局部建模方法 **GaitPart**、全局-局部融合方法 **GaitGL**，以及基于CCPG配置的强基线 **DeepGaitV2-P3D**。在MMGait的跨服装（CL）场景下，GaitBase取得61.0%的Rank-1准确率，为轮廓模态中最优（Table 3）。

**姿态基方法**：以 **GPGait++** 为2D/3D姿态的顶级基线，同时评估了基于骨架时序建模的 **SkeletonGait**。DeepGaitV2-P3D在正常行走（NM）条件下达到98.7%的Rank-1（Table 3），体现了姿态模态在受控场景下的竞争力。

**新兴模态基线**：对于RGB、事件（Event）、红外（IR）和投影深度等视觉化模态，统一采用GaitBase作为基线；对于2D/3D姿态，采用GPGait++。LiDAR点云则使用 **LidarGait++** 作为专用基线（Section 3.1.2）。

### 2. 跨模态与多模态融合基线

在跨模态检索任务中，基线方案为每一对模态独立训练一个双流模型——该框架包含模态特定的浅层编码器与共享深层网络，并联合优化交叉熵损失和跨模态三元组损失（Section 3.2）。这一范式要求为RGB↔深度、RGB↔红外等每一对模态分别训练独立模型，缺乏统一性。

在多模态融合任务中，基线采用 **MultiGait++** 的双流融合策略：两个模态的特征在保留各自浅层编码器的前提下进行联合优化（Section 3.3）。融合方式为简单特征拼接或平均，未引入自适应权重机制。

### 3. OmniGait的方法定位与关键改进

OmniGait在上述谱系中的核心贡献在于**从“每模态/每模态对独立建模”走向“单一统一模型覆盖全模态全任务”**。具体改进槽位如下：

| 改进槽位 | 基线做法 | OmniGait做法 | 证据锚点 |
|---------|---------|-------------|---------|
| 模态建模方式 | 各模态单独训练独立模型（如GaitBase per modality） | 共享骨干网络 + 模态专属浅层编码器，统一处理9种图像化模态 | Section 4.1 |
| 跨模态检索机制 | 为每一对模态训练独立双流模型 | 单一模型支持任意模态对间的双向检索 | Section 4.1 |
| 多模态融合方法 | 简单拼接或双流特征平均（MultiGait++） | 轻量自适应门控融合模块 + 残差连接 | Section 4.1 |
| 训练批次组织 | 模态内独立批次 | 单模态与融合特征共享批次，促进BatchNorm学习跨模态统计量 | Section 4.1 |

OmniGait仅需**9.96M参数**即可支撑9种模态的单模态、跨模态和多模态全部任务（Table 9），而基线方案需要为每个模态或模态对训练独立模型，参数总量随模态数线性增长。

### 4. 适用边界与局限

**适用边界**：
- OmniGait目前覆盖**9种图像化模态**（RGB图像、轮廓、红外图像、事件帧、投影深度图、2D姿态热图、3D姿态投影等），要求输入统一为64×64分辨率的图像表示。
- 框架在**正常行走（NM）和背包（BG）**条件下表现稳健，单模态Rank-1普遍在90%以上。
- 跨传感器融合（RGB+LiDAR投影深度）在跨服装场景可带来**+19.7%的Rank-1提升**（Table 6），表明几何与外观信息的互补性在统一框架下得到有效利用。

**关键局限**（需人工验证具体数值边界）：
1. **3D点云的信息损失**：OmniGait将LiDAR点云投影为深度图以纳入统一图像框架，损失了原始3D几何结构。这可能是LiDAR投影深度单模态性能（CL Rank-1 76.6%，Table 4）未进一步突破的原因之一。
2. **稀疏模态性能差距**：统一模型在4D雷达（单模态CL Rank-1仅约2.2%，Table 5）和3D姿态等稀疏模态上的性能明显弱于特定模态专用模型，表明共享骨干对稀疏输入的适应性有限。
3. **跨服装退化未根本解决**：尽管多模态融合带来显著提升，跨服装场景下所有检索范式的性能仍大幅下降（跨模态CL平均Rank-1仅28.4%，Table 5），表明服装变化仍是核心挑战。
4. **时间同步精度有限**：MMGait数据集未在异构传感器间实施严格的帧级时间同步（RGB与深度天然对齐，其他模态仅序列级对齐），可能制约精确的多模态时序建模。

### 5. 开放问题

1. **跨模态对齐与跨协变量鲁棒性的联合优化**：跨模态三元组损失促进模态不变表示，但服装变化引入的类内变异可能与模态差异产生冲突。如何同时优化这两个目标仍待探索。

2. **原生3D点云建模**：能否在统一全模态架构中直接对原始3D点云进行建模（而非投影为深度图），以保留更丰富的几何线索？

3. **现实部署泛化性**：OmniGait在MMGait受控采集环境下的有效性已初步验证（包括零样本迁移至SUSTech1K，Table 10），但在动态背景、人群遮挡等更复杂现实场景中的泛化能力尚需进一步验证。

4. **模态间性能差异的缩小**：是否可通过预训练-微调范式或语言引导（如文本描述步态属性）进一步降低统一模型中模态间的性能差距，使稀疏模态也能受益于丰富模态的知识迁移？

## 原文 PDF

![[paperPDFs/CVPR_2026/MMGait_Towards_Multi_Modal_Gait_Recognition.pdf]]
