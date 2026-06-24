---
title: "MATCHA: Towards Matching Anything"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/MATCHA_Towards_Matching_Anything.pdf
project_link: https://feixue94.github.io/matcha-project/
aliases:
- MATCHA
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "基于注意力机制的动态特征融合模块，在训练过程中使几何和语义描述子能够从彼此提取互补信息，并通过显式监督增强各自性能。"
primary_logic: "利用预训练基础模型（稳定扩散与DINOv2）的丰富知识，引入注意力驱动的几何-语义动态融合与对应监督，可以学习一个同时胜任几何、语义和时间匹配的统一特征描述子。"
claims:
- "MATCHA在单一特征下跨几何、语义和时间匹配三大任务的平均排名第一，显著超越所有对比方法。"
- "动态融合模块（MATCHA-Light）相较仅添加自注意力层的监督版本（DIFT.S）在语义匹配上提升PCK@0.05达5.4个百分点。"
- "集成DINOv2物体级特征使语义匹配PCK@0.05从69.0进一步提升到70.2（MATCHA），且显著增强了处理重复结构的能力。"
- "SPair-71k (语义匹配) 上 PCK@0.1 = 79.6 (MATCHA)"
---

# MATCHA: Towards Matching Anything

> [!tip] 核心洞察
> 利用预训练基础模型（稳定扩散与DINOv2）的丰富知识，引入注意力驱动的几何-语义动态融合与对应监督，可以学习一个同时胜任几何、语义和时间匹配的统一特征描述子。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MATCHA：迈向万事匹配 |
| 英文题名 | MATCHA: Towards Matching Anything |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2501.14945); [Project](https://feixue94.github.io/matcha-project/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MATCHA |
| Dataset | SPair-71k (语义匹配), MegaDepth (相对位姿估计), TAP-Vid (时间匹配), 综合平均排名 |

> [!tip] 效果简介
> - SPair-71k (语义匹配) 上，PCK@0.1 为 79.6 (MATCHA)，对比 54.3 (DIFT, 本实现)，变化 +25.3。
> - MegaDepth (相对位姿估计) 上，AUC@5° 为 55.8 (MATCHA + SP)，对比 49.7 (DIFT + SP)，变化 +6.1。
> - TAP-Vid (时间匹配) 上，PCK@0.1 为 91.3 (MATCHA)，对比 82.9 (DIFT.Uni + DINOv2)，变化 +8.4。

## 概述

### 问题背景

视觉对应是计算机视觉的基础任务，涵盖**几何匹配**（寻找精确的像素级对应，服务于三维重建和位姿估计）、**语义匹配**（建立跨实例或跨类别的语义对应）以及**时间匹配**（跟踪视频帧间的点轨迹）。然而，这三类对应长期以来依赖不同的特征设计范式：几何匹配偏好具有局部判别力的底层纹理特征，语义匹配需要高层物体级语义理解，时间匹配则要求特征兼具几何精度与语义鲁棒性。

这种割裂导致了两个核心困境。其一，现有预训练特征模型（如基于扩散模型的 **DIFT**，Tang et al., NeurIPS 2023）虽然能同时提取几何描述子 $F_l$ 与语义描述子 $F_h$，但二者彼此独立，使用时需根据任务手工指定，无法形成统一的描述子。其二，简单地将几何与语义特征拼接反而会严重破坏匹配性能——消融实验显示，直接串联（DIFT.Uni）使语义匹配 PCK@0.05 从 63.6 骤降至约 31.8，表明两种特征之间存在冲突，需要更精巧的融合机制。

### 核心方法

MATCHA 的核心思路是：**利用注意力机制驱动几何与语义特征的动态融合，并辅以显式对应监督，从预训练基础模型中蒸馏出一个能同时胜任三类匹配任务的统一描述子。**

具体而言，MATCHA 在稳定扩散模型提取的几何特征 $F_l$ 和语义特征 $F_h$ 之上，引入一个由自注意力和交叉注意力堆叠而成的 Transformer 融合模块。该模块令两类特征在训练过程中相互提取互补信息——几何特征从语义特征中获得物体级结构感知，语义特征从几何特征中获得局部纹理判别力——最终生成增强的几何描述子 $F_g$ 和语义描述子 $F_s$。随后，MATCHA 将 $F_g$、下采样的 $F_s$ 以及来自 **DINOv2**（Oquab et al., arXiv 2023）的物体级语义特征 $F_d$ 沿通道维静态串联，形成统一的描述子 $F_m$。整个融合模块通过双 softmax 几何匹配损失与 CLIP 对比损失联合监督训练。

这一设计的关键洞察在于：**动态融合解决了特征冲突，DINOv2 补全了扩散特征在单物体和重复结构上的盲区，而静态串联则避免了端到端联合微调对语义泛化能力的破坏。**

### 主要结果

MATCHA 在跨任务综合评测中展现出显著优势。如 Table 4 所示，MATCHA 以单一统一特征在几何、语义和时间匹配三大任务的平均排名位列第一，显著超越所有对比方法（包括专用几何特征 **MASt3R.E**、**DISK**、**SuperPoint**，专用语义特征 **SD4Match**、**DHF** 及 DINOv2 等）。

在语义匹配基准 SPair-71k 上，MATCHA 的 PCK@0.1 达到 79.6，较 DIFT 原始实现提升 25.3 个百分点（Table 1）。在几何位姿估计任务中，MATCHA 结合 SuperPoint 关键点在 MegaDepth 上的 AUC@5° 达到 55.8，较 DIFT 提升 6.1 个百分点（Table 2）。在时间匹配基准 TAP-Vid 上，MATCHA 的 PCK@0.1 达到 91.3，较 DIFT 统一特征版本提升 8.4 个百分点。

消融实验进一步揭示了各组件的贡献：动态融合模块（MATCHA-Light）相较仅添加自注意力层的监督版本（DIFT.S），在语义匹配 PCK@0.05 上提升 5.4 个百分点（69.0 vs. 63.6）；集成 DINOv2 特征后，语义 PCK@0.05 进一步提升至 70.2，且在重复结构场景下的匹配鲁棒性显著增强（Table 3, Figure 2）。

### 方法定位

在方法谱系中，MATCHA 处于**预训练基础模型特征增强**与**统一描述子学习**的交叉点。与 DIFT 等直接使用冻结扩散特征的方法不同，MATCHA 引入了可训练的注意力融合层和显式对应监督；与 MASt3R 等专用几何基础模型不同，MATCHA 追求单一特征的多任务泛化；与 SD4Match、DHF 等需要数据集特化模型或额外掩码的语义匹配方法不同，MATCHA 以统一的轻量训练范式覆盖三类任务。其核心贡献在于证明了：通过恰当的动态融合与知识整合策略，从现成基础模型中蒸馏出的统一特征，可以同时超越各领域的专用特征。

## 背景与动机

### 视觉对应的任务割裂现状

建立图像间的精确对应是三维重建、视觉定位、物体姿态估计、视频跟踪等众多下游应用的基础能力。根据匹配目标的不同，视觉对应任务可划分为三个主要分支：

- **几何匹配**：寻找跨视角下同一物理点的像素对应，要求特征对光照、视角变化具有不变性，同时保持高空间精度。
- **语义匹配**：建立属于同一语义部位（如“猫的左眼”）的对应，需要高层语义理解能力，对类别内形变和外观差异具有鲁棒性。
- **时间匹配**：在视频序列中跟踪任意指定像素点，需要同时处理大幅运动、尺度变化和遮挡。

这三类任务对特征描述子的需求存在根本性张力：几何匹配依赖底层纹理和结构信息，语义匹配需要高层物体部件理解，时间匹配则要求运动连续性下的判别力。当前主流方案通常为每个任务设计专用特征或模型，导致系统碎片化且难以泛化。

### 现有方法的局限

**扩散特征（DIFT）的潜力与不足**。Tang et al.（NeurIPS 2023）提出的 DIFT 首次揭示了预训练稳定扩散模型内部特征天然具备几何和语义对应能力——来自去噪 U-Net 浅层的特征（$F_l$）编码了几何结构信息，而深层特征（$F_h$）则捕获了语义部件信息。然而，DIFT 存在两个关键缺陷：（1）用户需要根据任务手工选择使用 $F_l$ 或 $F_h$，无法自动适应；（2）这些特征未经过任何对应监督训练，精度远低于专用监督方法。

**基础模型的互补性未被利用**。DINOv2（Oquab et al., arXiv 2023）作为自监督视觉基础模型，提供了强大的物体级语义特征，在单物体场景中对应精度优异，但在多实例或重复结构场景中表现急剧下降。相反，扩散特征在纹理丰富区域表现更好，却缺乏实例级辨别力。这种互补性在现有工作中未被系统挖掘。

**专用方法的泛化瓶颈**。有监督语义匹配方法（如 SD4Match、DHF、GeoASM）虽然在其训练类别上表现优异，但需要类别级标注甚至分割掩码，跨类别泛化能力有限。几何匹配方法（如 SuperPoint、DISK）仅关注局部结构，完全不具备语义对应能力。近期几何基础模型 MASt3R.E（Leroy et al., ECCV 2024）在几何任务上表现强劲，但在语义和时间匹配上几乎失效。

### 核心瓶颈与本文动机

**核心瓶颈**：不同类型的对应（几何、语义、时间）通常需要专门设计的特征或模型，缺乏统一的视觉对应学习范式，导致系统复杂且难以泛化。

这一瓶颈催生了本文的核心问题：**能否学习一个统一的特征描述子，在无需任务区分的前提下，同时胜任几何、语义和时间匹配？**

### MATCHA 的核心思路

MATCHA 的核心洞察在于：利用预训练基础模型（稳定扩散与 DINOv2）的丰富知识，引入注意力驱动的几何-语义动态融合与对应监督，可以学习一个同时胜任几何、语义和时间匹配的统一特征描述子。

具体而言，MATCHA 通过三个关键设计解决上述瓶颈：

1. **动态融合模块**：基于自注意力和交叉注意力的 Transformer 模块，使几何描述子 $F_l$ 和语义描述子 $F_h$ 在训练中相互增强——几何特征从语义特征中获取结构级理解，语义特征从几何特征中补充细节定位能力。

2. **显式对应监督**：对融合后的几何特征施加双 softmax 损失，对语义特征施加 CLIP 对比损失与密集语义流损失，使原本无监督的扩散特征获得精确匹配能力。

3. **物体级语义补全**：将 DINOv2 的物体级特征通过通道拼接集成到统一描述子中，弥补扩散特征在实例辨别和重复结构处理上的不足。

如 Figure 1 所示，MATCHA 使用单一特征描述子即可建立几何、语义和时间对应，无需任何任务切换或手工特征选择。

## 核心创新

### 问题瓶颈

视觉对应（visual correspondence）涵盖几何匹配、语义匹配和时间匹配三类任务，但现有方法通常为每种对应类型设计专门的特征描述子或模型。例如，**DIFT**（Tang et al., NeurIPS 2023）虽然从预训练稳定扩散模型中同时提取了高层语义特征 $F_h$ 和低层几何特征 $F_l$，却要求使用者根据任务**手工指定**使用哪个描述子——语义匹配用 $F_h$，几何/时间匹配用 $F_l$。这种“一任务一描述子”的范式导致系统复杂、缺乏统一的对应学习框架，且难以在不同任务间泛化。

更关键的是，来自扩散模型的特征虽然蕴含丰富知识，但**从未接受过显式的对应监督**，其匹配精度受限于预训练目标的间接约束。同时，单一模型的特征存在天然盲区：DIFT 的语义特征在重复结构或同类多实例场景中容易混淆，而 DINOv2（Oquab et al., arXiv 2023）的物体级特征虽擅长区分单个实例，却在纹理丰富区域的几何定位上不够精确（见 Figure 2）。如何将多种基础模型的互补知识融合为一个统一描述子，并使其在所有匹配任务上均表现优异，是本文要解决的核心挑战。

### 核心洞察

MATCHA 的核心洞察在于：**利用自注意力和交叉注意力机制，让几何特征与语义特征在训练过程中动态地从对方提取互补信息，并通过显式的几何与语义对应监督信号分别增强二者的表达能力，最终融合为一个统一的描述子。** 同时，引入 DINOv2 的物体级语义特征作为补充，弥补扩散特征在实例级辨别上的不足。这一设计使得单一特征 $F_m$ 能够同时胜任几何、语义和时间三类匹配任务，无需任何任务特定的切换或后处理。

### 关键创新点

#### 创新一：动态特征融合模块

**Baseline 状态：** DIFT 直接使用预提取的单一特征（$F_h$ 或 $F_l$），二者之间无任何信息交互，各自独立用于不同任务。

**MATCHA 改进：** 引入基于 Transformer 的动态融合模块，通过堆叠的自注意力（self-attention）和交叉注意力（cross-attention）块，使几何特征和语义特征在多个层级上相互增强。具体而言，在第 $i$ 个注意力块中：

- 语义特征先经自注意力更新：$F_{hs}^i = F_h^{i-1} + \mathsf{self}_h^i(F_h^{i-1})$
- 几何特征同步经自注意力更新：$F_{ls}^i = F_l^{i-1} + \mathsf{self}_l^i(F_l^{i-1})$
- 随后二者通过交叉注意力双向增强：$F_h^i = F_h^{i-1} + \mathsf{cross}_h^i(F_{hs}^i, F_{ls}^i)$，$F_l^i = F_l^{i-1} + \mathsf{cross}_l^i(F_{ls}^i, F_{hs}^i)$

经过 $k$ 个注意力块后，原始特征与融合后特征经 MLP 投影得到增强描述子：$F_s = \mathsf{MLP}_h([F_h^0 \| F_h^k])$，$F_g = \mathsf{MLP}_l([F_l^0 \| F_l^k])$。这一机制的关键在于“动态”——融合权重由输入图像的内容自适应决定，而非固定的静态组合。

**证据强度：** 消融实验（Table 3）显示，仅对 DIFT 特征添加自注意力层并施加监督（DIFT.S），语义匹配 PCK@0.05 仅为 63.6；而引入完整的动态融合模块（MATCHA-Light）后，该指标跃升至 69.0（+5.4 个百分点）。几何匹配 AUC@5° 也从 50.4 提升至 51.4。这直接验证了交叉注意力驱动的特征互补是性能提升的核心来源。

#### 创新二：双路显式对应监督

**Baseline 状态：** DIFT 完全依赖预训练扩散模型的自监督表示，**无任何显式对应监督信号**，特征空间未针对匹配任务优化。

**MATCHA 改进：** 对动态融合后的两个增强特征分别施加精确的任务特定监督：

- **几何分支（$F_g$）：** 采用双 softmax 损失（dual softmax loss），直接监督几何对应关系的匹配概率分布。
- **语义分支（$F_s$）：** 采用 CLIP 对比损失（CLIP contrastive loss）结合密集语义流损失（dense semantic flow loss），在语义嵌入空间和像素级流场上同时施加约束。

总损失为 $L_{total} = L_{geo} + w_{sem} L_{sem}$，其中 $w_{sem}$ 控制语义损失的权重。这种“分而治之”的监督策略使得融合模块在增强一种特征时不会损害另一种特征的能力。

**证据强度：** 对比 Table 3 中 DIFT（无监督）与 MATCHA-Light（有监督）的结果，语义匹配 PCK@0.05 从 54.3 提升至 69.0（+14.7），几何匹配 AUC@5° 从 49.7 提升至 51.4。监督信号的引入是性能飞跃的关键因素。

#### 创新三：物体级语义特征集成

**Baseline 状态：** DIFT 和 MATCHA-Light 均未利用 DINOv2 等外部物体级语义特征，在重复结构或同类多实例场景中存在辨别力不足的问题。

**MATCHA 改进：** 将 DINOv2 提取的物体级特征 $F_d$ 通过通道拼接的方式静态集成到最终统一描述子中：$F_t = (F_g \| F_s(\ldots, :\!\!\: d_s))$，$F_m = (F_t \| F_d(\ldots, :\!\!\: d_t))$。这种静态串联（而非端到端联合训练）的设计是经过审慎选择的——消融实验（Table 6）表明，对整个统一特征进行联合几何-语义微调会严重破坏语义匹配能力（语义 PCK 均值降至 50.7），因此保持 DINOv2 特征的冻结状态是保护其语义泛化性的必要条件。

**证据强度：** Table 3 显示，在 MATCHA-Light 基础上集成 DINOv2（即完整 MATCHA），语义匹配 PCK@0.05 从 69.0 进一步提升至 70.2，几何匹配 AUC@5° 从 51.4 提升至 51.7。Figure 2 的定性对比更直观地展示了 DINOv2 特征在单物体场景下的精准定位能力和 MATCHA 在重复结构场景下的鲁棒性优势。

#### 创新四：单一统一描述子范式

**Baseline 状态：** 现有方法要求为不同匹配任务选择不同的描述子（语义用 $F_h$，几何用 $F_l$），甚至需要任务特定的模型（如 **SD4Match** (Li et al., CVPR 2024) 针对语义匹配，**MASt3R.E** (Leroy et al., ECCV 2024) 针对几何匹配）。

**MATCHA 改进：** 输出单一特征 $F_m \in \mathbb{R}^{H/8 \times W/8 \times D_m}$，通过最近邻搜索加互检（mutual check）的统一匹配流程，直接适用于所有三类任务。Table 4 的综合排名显示，MATCHA 在几何、语义、时间匹配三大任务上的平均排名为第 1 名（共 9 种方法），显著领先于第二名，且是唯一一个在所有任务上均进入前三的方法。这证明了统一描述子范式不仅可行，而且在跨任务泛化上超越了任务专用方法。

### 方法谱系与知识库定位

MATCHA 处于**预训练基础模型特征适配**与**多任务统一表示学习**的交叉点。其方法谱系可梳理如下：

- **上游基础模型：** 继承自 **DIFT**（Tang et al., NeurIPS 2023）的稳定扩散多层级特征提取范式，以及 **DINOv2**（Oquab et al., arXiv 2023）的自监督物体级语义特征。
- **融合机制：** 借鉴 Transformer 的自注意力/交叉注意力架构（Vaswani et al., NeurIPS 2017），但将其应用于跨层级、跨语义的特征动态交互，而非传统的序列建模。
- **监督策略：** 几何分支的双 softmax 损失可追溯至 **XFeat** 等密集匹配方法；语义分支的 CLIP 对比损失源自 **CLIP**（Radford et al., ICML 2021）的多模态对齐思想，密集语义流损失则与 **DHF**（Luo et al., NeurIPS 2023）等扩散超特征方法共享相似的监督哲学。
- **差异化定位：** 不同于 **SD4Match**（Li et al., CVPR 2024）和 **GeoASM**（Zhang et al., CVPR 2024）等需要语义分割掩码或数据集特定模型的语义匹配方法，MATCHA 以单一模型、单一特征实现零样本跨任务泛化；不同于 **MASt3R.E**（Leroy et al., ECCV 2024）等几何专用基础模型，MATCHA 在保持几何匹配竞争力的同时，大幅拓展了语义和时间匹配的能力边界。

**关键限制与待验证点：** 动态融合模块目前仅在下采样 8× 的特征图上运行，导致在 HPatches 小像素误差阈值（<7 px）下匹配精度不及原始分辨率特征（如 DISK, Tyszkiewicz et al., NeurIPS 2020）。此外，DINOv2 在无明显单一物体的重复结构场景中的弱点仍会传递至 MATCHA。静态串联策略虽保护了语义泛化性，但也意味着几何与语义特征之间的协同潜力尚未被完全挖掘——如何设计端到端的联合训练策略而不损害语义能力，是未来研究的重要方向。

## 整体框架

MATCHA 的设计围绕一个核心目标展开：**用单一特征描述子同时胜任几何匹配、语义匹配和时间匹配**，从而消除传统方法中需要为不同任务分别设计或选择特征的复杂性。其整体流水线由四个紧密衔接的模块构成，如 Figure 3 所示。

### 流水线概览

给定一张 RGB 图像，MATCHA 的处理流程如下：

1. **基础特征提取**：从两个预训练基础模型中并行提取互补的初始特征。
2. **动态融合**：通过基于注意力机制的 Transformer 模块，令几何特征与语义特征相互增强。
3. **特征合并**：将增强后的几何特征、语义特征与 DINOv2 的物体级特征沿通道维静态串联，形成统一描述子。
4. **最近邻匹配**：基于统一描述子进行最近邻搜索与互检，输出最终对应。

### 模块关系与数据流

**第一层：双源基础特征提取**

MATCHA 构建在两个预训练基础模型之上：

- **稳定扩散模型**（Stable Diffusion）：提取多层级特征，得到初始**几何描述子** $F_l \in \mathbb{R}^{H/8 \times W/8 \times 640}$ 和初始**语义描述子** $F_h \in \mathbb{R}^{H/16 \times W/16 \times 1280}$。这两个描述子分别擅长几何对应和语义对应，但彼此孤立、缺乏互补信息的交互。
- **DINOv2**（Oquab et al., 2023）：提取强物体级语义特征 $F_d$，提供实例感知能力，尤其有助于区分同一类别的不同实例和处理重复结构。

**第二层：动态特征融合**

这是 MATCHA 的核心创新模块。采用由自注意力和交叉注意力块堆叠而成的 Transformer 架构，对 $F_l$ 和 $F_h$ 进行动态融合。具体而言：

- 在每个注意力块中，语义特征和几何特征首先各自通过自注意力进行自身增强：
  $$F_{hs}^i = F_h^{i-1} + \mathsf{self}_h^i(F_h^{i-1})$$
  $$F_{ls}^i = F_l^{i-1} + \mathsf{self}_l^i(F_l^{i-1})$$
- 随后通过交叉注意力实现信息交换——增强后的几何特征用于更新语义特征，反之亦然：
  $$F_h^i = F_h^{i-1} + \mathsf{cross}_h^i(F_{hs}^i, F_{ls}^i)$$
  $$F_l^i = F_l^{i-1} + \mathsf{cross}_l^i(F_{ls}^i, F_{hs}^i)$$

经过 $k$ 个注意力块后，将原始特征与融合后的特征串联并通过 MLP 投影，得到最终的增强描述子：
$$F_s = \mathsf{MLP}_h([F_h^0 \| F_h^k]), \quad F_g = \mathsf{MLP}_l([F_l^0 \| F_l^k])$$

该机制的关键在于：**几何特征在融合过程中吸收语义信息以提升对物体结构的感知，语义特征则借助几何信息增强空间定位精度**。消融实验（Table 3）证实，若移除动态融合而仅保留自注意力监督（DIFT.S），语义匹配 PCK@0.05 从 69.0 降至 63.6，几何匹配 AUC@5° 从 51.4 降至 50.4，说明交叉注意力驱动的互补信息交换至关重要。

**第三层：静态特征合并**

动态融合后，MATCHA 采用**静态串联**策略将三类特征整合为统一描述子 $F_m$：
$$F_t = (F_g \| F_s(\ldots, :\!:: d_s)), \quad F_m = (F_t \| F_d(\ldots, :\!:: d_t))$$

其中 $F_s$ 和 $F_d$ 经过降采样以匹配 $F_g$ 的空间分辨率（$H/8 \times W/8$）。最终输出 $F_m \in \mathbb{R}^{H/8 \times W/8 \times D_m}$，作为适用于所有匹配任务的统一特征描述子。

值得注意的是，作者明确选择**不对整个统一特征进行端到端联合训练**。消融实验（Table 6）表明，直接对 $F_m$ 施加联合几何-语义微调会严重破坏语义匹配能力（语义 PCK 均值降至 50.7），因此采用先独立监督融合模块、再静态串联的策略以保护语义泛化性能。

**第四层：最近邻匹配器**

在推理阶段，MATCHA 基于统一描述子 $F_m$ 进行最近邻搜索，并通过互检（mutual check）过滤不可靠匹配，输出最终对应关系。这一匹配流程与 DIFT 等先前工作保持一致，确保公平比较。

### 监督信号与训练策略

动态融合模块的训练由两类精确的对应监督信号驱动：

- **几何监督**：对增强几何特征 $F_g$ 施加双 softmax 损失（dual softmax loss），提供像素级几何对应约束。
- **语义监督**：对增强语义特征 $F_s$ 施加 CLIP 对比损失与密集语义流损失的组合，提供语义级对应约束。

总损失为两者的加权和：
$$L_{total} = L_{geo} + w_{sem} L_{sem}$$

训练仅使用少量标注数据（MegaDepth 和 SPair-71k 的部分样本），避免大规模标注偏差。这种监督策略使得融合后的 $F_g$ 和 $F_s$ 各自获得比原始 DIFT 特征更强的匹配能力，进而通过静态合并将这种增强传递至统一描述子 $F_m$。

### 输入输出规范

- **输入**：单张 RGB 图像（训练时使用图像对，推理时单张提取特征后跨图匹配）。
- **输出**：统一特征图 $F_m$，空间分辨率固定为输入的 1/8（8× 下采样），适用于几何、语义和时间三类匹配任务，无需任务区分或手工特征选择。

## 核心模块与公式推导

MATCHA 的核心由四个模块串联构成：基础特征提取、动态特征融合、特征合并与监督训练。整体流程如 Figure 3 所示。

### DIFT 基础特征提取

从预训练稳定扩散模型（**DIFT**，Tang et al., NeurIPS 2023）中提取两个多层级特征图作为初始描述子：

- 语义描述子 $F_h \in \mathbb{R}^{H/16 \times W/16 \times 1280}$：来自扩散 U-Net 的高层特征，捕获类别级语义信息，用于语义匹配。
- 几何描述子 $F_l \in \mathbb{R}^{H/8 \times W/8 \times 640}$：来自扩散 U-Net 的低层特征，保留细粒度几何结构，用于几何匹配与时间匹配。

这两个特征在 DIFT 原方法中需根据任务手工选择——语义匹配用 $F_h$，几何匹配用 $F_l$。MATCHA 消除这一任务依赖，将其统一送入后续融合模块。

### DINOv2 特征提取

从 **DINOv2**（Oquab et al., arXiv 2023）提取强物体级语义特征 $F_d$，该特征在单物体场景下匹配精度高，但对重复结构或同类多实例场景区分能力不足（Figure 2）。$F_d$ 作为互补信号在最终合并阶段集成。

### 动态融合模块

这是 MATCHA 的核心创新——基于 Transformer 的自注意力与交叉注意力机制，使几何与语义描述子动态地从彼此提取互补信息。模块由 $k$ 个注意力块堆叠而成，每个块对两类特征执行两步更新。

**步骤 1：自注意力增强**

对第 $i$ 个块，先用自注意力分别增强语义特征和几何特征自身：

$$F_{hs}^i = F_h^{i-1} + \mathsf{self}_h^i(F_h^{i-1}) \tag{1}$$

$$F_{ls}^i = F_l^{i-1} + \mathsf{self}_l^i(F_l^{i-1}) \tag{2}$$

**步骤 2：交叉注意力互补**

随后通过交叉注意力，让增强后的几何特征注入语义特征，反之亦然：

$$F_h^i = F_h^{i-1} + \mathsf{cross}_h^i(F_{hs}^i, F_{ls}^i) \tag{3}$$

$$F_l^i = F_l^{i-1} + \mathsf{cross}_l^i(F_{ls}^i, F_{hs}^i) \tag{4}$$

经过 $k$ 个块迭代后，将原始特征与最终融合特征拼接，经 MLP 投影得到增强描述子：

$$F_s = \mathsf{MLP}_h([F_h^0 \| F_h^k]), \quad F_g = \mathsf{MLP}_l([F_l^0 \| F_l^k]) \tag{5}$$

其中 $F_s$ 为增强语义描述子，$F_g$ 为增强几何描述子。

### 特征合并

将增强后的几何、语义特征与 DINOv2 特征沿通道维静态串联，形成统一描述子 $F_m$：

$$F_t = (F_g \| F_s(\ldots, :\!\!\: d_s)), \quad F_m = (F_t \| F_d(\ldots, :\!\!\: d_t)) \tag{6}$$

其中 $F_s(\ldots, :\!\!\: d_s)$ 表示对语义特征进行降采样以匹配几何特征的空间分辨率，$F_d(\ldots, :\!\!\: d_t)$ 同理。最终 $F_m \in \mathbb{R}^{H/8 \times W/8 \times D_m}$ 为单一统一描述子，适用于所有匹配任务。

> **关键设计决策**：统一特征采用静态串联而非端到端联合训练。消融实验（Table 6）表明，直接对整个 $F_m$ 进行联合几何-语义微调会严重破坏语义匹配能力（语义 PCK 均值降至 50.7），因此 MATCHA 选择仅在融合阶段施加监督，合并后冻结特征。

### 监督信号

MATCHA 对融合模块施加显式对应监督，这是区别于 DIFT 无监督特征的关键变化。

- **几何监督**：对增强几何描述子 $F_g$ 施加双 softmax 损失（dual softmax loss），利用几何匹配真值训练关键点级对应精度。
- **语义监督**：对增强语义描述子 $F_s$ 施加 CLIP 对比损失与密集语义流损失的组合，利用语义匹配真值训练区域级语义对齐。

总损失为加权联合：

$$L_{total} = L_{geo} + w_{sem} L_{sem} \tag{12}$$

其中 $w_{sem}$ 为语义损失权重。训练仅使用少量标注数据，避免大规模标注偏差。

### 匹配推理

推理时，使用最近邻搜索加互检（mutual check）在 $F_m$ 的描述子空间建立对应，无需任务区分。几何匹配实验中统一使用 **SuperPoint**（DeTone et al., CVPR 2018）提取关键点，位姿估计采用 Poselib + LO-RANSAC 方案，保证与基线方法的公平对比。

## 实验与分析

### 瓶颈验证与核心实验结论

MATCHA 的设计围绕一个核心瓶颈展开：不同类型的对应（几何、语义、时间）通常需要专门设计的特征或模型，缺乏统一的视觉对应学习范式。实验体系从语义匹配、几何位姿估计和时间匹配三个维度验证了统一描述子的有效性，并通过消融实验量化了动态融合、DINOv2 集成和监督信号各自带来的增益。

**语义匹配（SPair-71k / PF-Pascal / PF-Willow）**。Table 1 给出了语义匹配的主结果。MATCHA 在 SPair-71k 上取得 PCK@0.01/0.05/0.1 分别为 12.2/67.1/79.6，显著超越本实现中的 DIFT（54.3 PCK@0.1，+25.3 个百分点），也优于多数有监督语义匹配方法（如 **SD4Match**，Li et al., CVPR 2024；**DHF**，Luo et al., NeurIPS 2023）。在 PF-Willow 上，MATCHA 达到 PCK@0.05/0.1/0.15 为 70.2/91.3/97.0。值得注意的是，MATCHA 无需数据集专属模型或语义分割掩码（Table 1 中 `†` 标记的方法如 **GeoASM**, Zhang et al., CVPR 2024 需要掩码），在单一统一特征下即达到领先水平。

**几何匹配与相对位姿估计（MegaDepth / ScanNet / Aachen）**。几何匹配实验统一使用 SuperPoint（**SuperPoint**, DeTone et al., CVPR 2018）提取关键点，采用最近邻搜索加互检的匹配流程，位姿估计使用 Poselib + LO-RANSAC 方案，保证公平性。Table 2 显示，MATCHA + SP 在 MegaDepth 上取得 AUC@5°/10°/20° 为 55.8/69.3/80.0，相较于 DIFT + SP 的 49.7/63.2/74.8 提升显著（AUC@5° +6.1）。在 Aachen 日间场景，MATCHA 的 AUC@5° 达到 51.7，MATCHA-Light 达到 51.4，均优于 DIFT（49.7）和 DINOv2（43.6）。ScanNet 室内场景下，MATCHA-Light 的 AUC@5° 为 13.0，较 DIFT（9.3）提升 3.7 个百分点，验证了动态融合对低纹理、重复结构场景的鲁棒性增强。

**时间匹配（TAP-Vid）**。时间匹配复用 TAP-Vid 提供的查询点，评测方式与语义匹配的 PCK 指标对齐。Table 4 显示，MATCHA 在 TAP-Vid-Davis 上取得 PCK@0.1 为 91.3，显著超越 DIFT.Uni + DINOv2（82.9，+8.4 个百分点）。Figure 5 的可视化进一步表明，MATCHA 在极端尺度变化、大视角变化和多相似实例场景下均能建立准确的时间对应，而 DIFT 在这些挑战性场景中失效明显。

**综合排名（Table 4）**。在所有参与对比的特征模型中（包括 **MASt3R.E**, Leroy et al., ECCV 2024；**DISK**, Tyszkiewicz et al., NeurIPS 2020；DINOv2；DIFT 等共 9 种方法），MATCHA 在几何、语义、时间三项任务上的平均排名为第 1 名，而 MASt3R.E 排名第 9（几何强但语义/时间弱），DIFT 平均排名约 4.3。这一结果直接验证了统一描述子跨任务泛化的可行性。

### 消融实验与因果机制分析

Table 3 在 Aachen（几何）和 PF-Willow（语义）上进行了系统的组件消融，揭示了各设计选择的因果作用。

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2501_14945/figures/008_Table_3.jpg]]
*Table 3: MATCHA Ablation Study.We ablate different components of proposed model on Aachen [56] for geometric matching and PF-Willow [17] for semantic matching using the same metrics defined in the previous sections.We denote their descriptor types using SM/GM/Uni that stand for semantic/geometric/unified features.We use green cells for evaluations on a supervised matching task and gray on zero-shot matching tasks*

**动态融合的核心作用**。去除动态融合、仅保留自注意力层并进行监督的版本 DIFT.S 在语义匹配上 PCK@0.05 仅为 63.6，而引入动态融合的 MATCHA-Light 达到 69.0（+5.4 个百分点）；几何匹配上，DIFT.S 的 AUC@5° 为 50.4，MATCHA-Light 为 51.4（+1.0 个百分点）。这表明基于自注意力和交叉注意力的动态融合模块（公式 1-5）使几何描述子 $F_l$ 和语义描述子 $F_h$ 能够从彼此提取互补信息，并通过显式监督增强各自性能，是性能提升的关键因果旋钮。

**简单串联的失败**。直接将原始语义和几何描述子沿通道串联（DIFT.Uni 或 M2）会导致语义匹配性能崩溃——PCK@0.05 降至约 31.8。这说明未经动态融合的几何特征对语义匹配任务存在严重干扰，动态融合对于平衡两种能力至关重要。

**DINOv2 物体级特征的增益**。在动态融合后集成 DINOv2 特征（M1 → MATCHA）使语义匹配 PCK@0.05 从 69.0 进一步提升到 70.2，几何 AUC@5° 从 51.4 提升到 51.7。Figure 2 的定性对比揭示其因果机制：DINOv2 在单物体场景中提供强物体级语义定位能力，但在多实例或重复结构场景中区分能力下降；DIFT 的几何和语义特征则相反。MATCHA 通过融合两者，在重复结构场景中显著增强了辨别能力。

**统一特征联合训练的困境**。Table 6 显示，直接对整个统一特征 $F_m$ 进行联合几何-语义微调会严重破坏语义匹配能力（语义 PCK 均值降至 50.7），因此 MATCHA 采用静态串联而非端到端联合训练。这一发现揭示了一个开放问题：如何在引入几何监督时不破坏语义匹配的泛化性能。

**时间匹配消融**。Table 5 的时间匹配消融表明，DINOv2 单独用于时间匹配表现优异（PCK@0.1 约 82.7），但其几何匹配能力极弱（AUC@5° 仅 43.6）。MATCHA 通过统一特征整合 DINOv2 的时间感知能力和动态融合后的几何-语义特征，在时间匹配上实现了最优性能。

### 局限性分析

1. **特征图分辨率限制**。MATCHA 输出的特征图存在 8× 下采样，在 HPatches 小像素误差阈值（<7 px）下匹配精度不及原始分辨率特征（如 DISK），Figure 4 的 MMA 曲线清晰展示了这一差距。
2. **DINOv2 弱点的传递**。DINOv2 在包含大量重复结构或不明显单一物体的场景中区分能力下降，该弱点仍会传递至 MATCHA 的统一特征中。
3. **静态串联的潜力未充分挖掘**。统一特征采用静态串联而非端到端联合训练，虽然保护了语义能力，但可能未充分挖掘几何与语义的协同潜力。
4. **时间匹配未利用时序先验**。时间匹配评估仅基于 TAP-Vid 的成对帧匹配，未利用视频连续性先验，可能低估了融合时序信息的潜力。

### 补充图表

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2501_14945/figures/003_Figure_3.jpg]]
*Figure 3: Architectureof MATCHA.GivenanRGB image,MATCHA produces asingle feature for geometric,semanticand temporal matching withnearestneighborsearching.MATCHA isbuiltontopofstabledifusion (SD)models[53]andDINOv2[44].Specificaly original geometricandsemanticfeatures extractedfromSDarfrstfuseddynamicallwithatransforer64]consistsofselfandcross atentionblocks.Intisdynamicfusionprocess,othgeometricandsematicfeaturesareaugmentedwitheachoterwhicharesupeised withcorrespondinggound-truthsnalsinteringprocs.eaugmentedgometricandmanticsfeaturealongwithOv feature are unified statically via concatenations into a single feature for matching anything*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2501_14945/figures/007_Figure_5.jpg]]
*Figure 5: Visualization of temporal matches on TapVID-Davis [12].Here we visualize several challenging cases for exstablishing temporal correspondences，where MATCHA generally achieves the best performance in handling extreme scale and viewpoint changes,as well as scenes with multiple similar instances.(DIFT* is the adapted DIFT where we use its concatenated semantic and geometric feature for temporal matching for better performance.)*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2501_14945/figures/004_Table_1.jpg]]
*Table 1: Evaluation on Semantic Matching. We report PCK under different thresholds.* denotes methods with dataset-specific models and † denotes semantic masks being required. Red indicates methods using image pairs as inputs. Both results of DIFT from its original paper [6O] (*DIFT) and our implementation (DIFT) are included*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2501_14945/figures/006_Table_2.jpg]]
*Table 2: Evaluation on Relative Pose Estimation. We report the AUC values at error thresholds of 5°/10°/2O°on all datasets*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2501_14945/figures/009_Table_4.jpg]]
*Table 4: Twards Matching Anything with A Unified Feature.Wecompare ourselves to various feature models across geometric, semanticandtemporalmatchingandcompute therankingofeach methodforeachtaskandaveragedovertasks.WeshowthatMATCHA is able to achieve the topk averaged ranking among al types of methods using a single feature for matching anything*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2501_14945/figures/010_Table_5.jpg]]
*Table 5: Ablation Study on Temporal Matching.We report the Percentage of Correct Keypoints (PCK) under different thresholds. The best and second-best results are highlighted*

![[assets/figures/papers/paper_list_l46_https_arxiv_org_abs_2501_14945/figures/011_Table_6.jpg]]
*Table 6: Ablationstudyonobtainingaunifiedfeature.Wecomparediferent waysofobtainingaunifiedfeature.Weshowthatsimple concatenationleads tobeterwaytokeeptheleaed geometricandsemanticrepresentationwhileaddingaditionaljoint trainingonthe concatenated feature pushes the feature tofocus more on geometric matching,leading to significantly degraded semantic matching*

## 方法谱系与知识库定位

### 1. 问题定位：从专用描述子到统一特征

视觉对应学习长期面临一个核心瓶颈：**不同类型的对应——几何匹配、语义匹配、时间匹配——通常需要专门设计的特征或模型**。几何匹配依赖局部纹理和结构信息，语义匹配需要高层物体理解，时间匹配则要求对运动和外观变化的鲁棒性。这一分裂导致系统复杂、难以泛化，且各方法的知识无法共享。

MATCHA 试图打破这一壁垒，其核心主张是：**利用预训练基础模型的丰富知识，通过注意力驱动的动态融合与对应监督，可以学习一个同时胜任几何、语义和时间匹配的统一特征描述子**。这一思路将问题从“为每个任务设计特征”转化为“融合并增强已有基础特征”，在方法谱系上属于**多基础模型知识整合与特征增强**范式。

### 2. 与基线方法的关系与演进

MATCHA 建立在多个已有工作的基础之上，其贡献可通过与以下基线的对比清晰定位：

#### 2.1 扩散特征基线：DIFT（Tang et al., NeurIPS 2023）

DIFT 首次揭示了预训练稳定扩散模型的特征图天然包含几何和语义对应信息，但其使用方式存在关键局限：**需要为不同任务分别手工选择语义描述子 $F_h$ 或几何描述子 $F_l$**，且无显式对应监督。MATCHA 直接继承 DIFT 的多层级特征提取框架，但在三个维度上实现突破：

- **描述子统一性**：输出单一特征 $F_m$ 适用于所有任务，消除任务区分需求（Table 4 综合排名第1 vs DIFT 排名4.3）。
- **特征融合机制**：引入基于自注意力和交叉注意力的动态融合模块，使几何与语义特征相互增强，而非简单使用原始提取特征。
- **监督信号**：对融合后的几何特征施加双 softmax 损失，对语义特征施加 CLIP 对比损失+密集语义流损失，提供精确匹配监督。消融实验（Table 3）表明，仅添加自注意力监督的 DIFT.S 在语义匹配 PCK@0.05 上仅达 63.6，而引入动态融合的 MATCHA-Light 提升至 69.0（+5.4 pp），验证了融合机制本身的关键作用。

#### 2.2 物体级语义基线：DINOv2（Oquab et al., arXiv 2023）

DINOv2 提供强物体级语义特征，在单物体对应上表现优异，但在多实例或重复结构场景中区分能力下降（Figure 2 第3-4行）。MATCHA 将 DINOv2 特征 $F_d$ 通过通道拼接集成到最终统一特征 $F_m$ 中，作为对扩散特征的互补。消融实验（Table 3, M1 vs MATCHA）显示，集成 DINOv2 使语义匹配 PCK@0.05 从 69.0 进一步提升至 70.2，且显著增强了处理重复结构的能力（Figure 2 第4行）。

#### 2.3 几何匹配基线：SuperPoint（DeTone et al., CVPR 2018）与 DISK（Tyszkiewicz et al., NeurIPS 2020）

SuperPoint 和 DISK 代表传统有监督几何局部特征。MATCHA 在相对位姿估计上全面超越这些方法（Table 2）：在 MegaDepth 上 AUC@5° 达 55.8（MATCHA+SP），对比 DIFT+SP 的 49.7 提升 6.1 点。但需注意 MATCHA 的特征图存在 8× 下采样，在 HPatches 小像素误差阈值（<7 px）下匹配精度不及原始分辨率特征如 DISK（Figure 4），这是其几何匹配的已知局限。

#### 2.4 几何基础模型基线：MASt3R.E（Leroy et al., ECCV 2024）

MASt3R.E 作为几何基础模型编码器，在几何匹配上表现强劲，但在语义和时间匹配上能力有限。Table 4 的综合排名显示，MASt3R.E 平均排名为 9/9（末位），而 MATCHA 以平均排名 1/9 显著领先，体现了统一特征在多任务上的压倒性优势。

#### 2.5 有监督语义匹配基线：SD4Match（Li et al., CVPR 2024）、DHF（Luo et al., NeurIPS 2023）、GeoASM（Zhang et al., CVPR 2024）

这些方法在语义匹配上各有优势，但通常需要数据集特定模型或额外输入（如 GeoASM 需分割掩码）。MATCHA 在 SPair-71k 上以单一模型达到 PCK@0.1 为 79.6，超越除 GeoASM 外的所有方法（Table 1），且无需掩码或图像对输入，在泛用性上具有明显优势。

### 3. 适用边界与局限

尽管 MATCHA 在多任务统一上取得突破，其适用边界和局限同样明确：

1. **分辨率受限**：特征图 8× 下采样导致在小像素误差下的几何精度不足，不适用于需要亚像素精度的精细匹配场景（如 HPatches <7 px 阈值）。

2. **重复结构退化**：DINOv2 在重复结构或不明显单一物体的场景中区分能力下降，此弱点通过特征集成传递至 MATCHA（Figure 2 第3行），在高度重复纹理场景中仍可能失效。

3. **静态串联的代价**：统一特征采用静态通道串联而非端到端联合训练。消融实验（Table 6）表明，直接对整个统一特征进行联合几何-语义微调会严重破坏语义匹配能力（语义 PCK 均值降至 50.7）。这一设计保护了语义泛化性，但可能未充分挖掘几何与语义的协同潜力。

4. **时间匹配的简化**：时间匹配评估仅基于 TAP-Vid 的成对帧匹配，未利用视频连续性先验，可能低估了融合时序信息的潜力。

5. **推理效率**：动态融合模块叠加 DINOv2 与扩散特征提取，计算开销显著高于轻量级几何特征（如 SuperPoint），限制了在实时或资源受限场景下的部署。

### 4. 开放问题

基于上述局限，以下几个方向值得进一步探索：

- **端到端统一训练**：如何设计一种联合训练策略，能在引入几何监督时不破坏语义匹配的泛化性能，从而实现真正端到端的统一描述子学习？这是当前静态串联设计的根本性局限。

- **多尺度分辨率增强**：能否通过多尺度特征融合或超分辨率技术提高特征图分辨率，以提升在小像素误差下的几何匹配精度？

- **时序信息融合**：是否可以将视频时序约束融入特征学习，使统一描述子进一步利用帧间运动连续性提升时间匹配？

- **推理效率优化**：如何优化动态融合模块与大规模基础特征的推理效率，使其适用于实时或资源受限的应用？

- **更多基础模型的整合**：除 DINOv2 外，其他预训练基础模型（如 CLIP、SAM）的语义或结构特征是否也能通过类似融合策略进一步增强统一匹配能力？这为方法谱系的进一步扩展提供了想象空间。

## 原文 PDF

![[paperPDFs/CVPR_2025/MATCHA_Towards_Matching_Anything.pdf]]
