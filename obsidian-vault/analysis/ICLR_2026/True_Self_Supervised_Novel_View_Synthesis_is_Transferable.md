---
title: "True Self-Supervised Novel View Synthesis is Transferable"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/True_Self_Supervised_Novel_View_Synthesis_is_Transferable.pdf
openreview_forum_id: aJJppqAm6r
aliases:
- TSSNVSIT
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "将训练范式从多视图自编码改为双视图外推（立体-单目模型），并引入跨序列的可迁移性目标函数，迫使模型学习可迁移的姿态表示，从而在不依赖任何3D归纳偏置的情况下实现真正的NVS。"
primary_logic: "真正的NVS要求相机姿态表示在不同场景间可迁移；仅使用一对图像（防止插值）并结合保持相机姿态的图像增广进行跨序列训练，使得未受限的潜在变量能够自发学习几何推理，无需SE(3)参数化等先验。"
claims:
- "XFactor在可迁移性指标AUC @ 20°上比RayZer高出超过5倍（RE10K上55.2 vs 7.6）。"
- "XFactor的潜在姿态表示在探针实验中能高度准确地预测真实SE(3)相机姿态（AUC @ 30° 72.9 vs RayZer 60.8）。"
- "消融实验表明：多视图训练逐步破坏可迁移性，而立体-单目+可迁移性目标取得最佳效果。"
- "RE10K 上 Transferability AUC @ 20° = 55.2"
---

# True Self-Supervised Novel View Synthesis is Transferable

> [!tip] 核心洞察
> 真正的NVS要求相机姿态表示在不同场景间可迁移；仅使用一对图像（防止插值）并结合保持相机姿态的图像增广进行跨序列训练，使得未受限的潜在变量能够自发学习几何推理，无需SE(3)参数化等先验。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 真正的自监督新视角合成具有可迁移性 |
| 英文题名 | True Self-Supervised Novel View Synthesis is Transferable |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=aJJppqAm6r); [Project](https://www.mitchel.computer/xfactor/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | XFactor |
| Dataset | RE10K, DL3DV |

> [!tip] 效果简介
> - RE10K 上，Transferability AUC @ 20° 为 55.2，对比 7.6 (RayZer)，变化 +47.6 (≈7.3×)。
> - DL3DV 上，Transferability AUC @ 20° 为 57.2，对比 5.9 (RayZer)，变化 +51.3。
> - RE10K 上，Pose Probe AUC @ 30° 为 72.9，对比 60.8 (RayZer)，变化 +12.1。

## 概述

### 问题瓶颈

现有自监督新视角合成（NVS）方法——如 **RayZer** (Jiang et al., 2025) 和 **RUST** (Sajjadi et al., 2023)——虽然能在训练序列上合成看似合理的视图，但其学到的相机姿态表示本质上编码的是“如何从上下文帧插值出目标帧”，而非场景无关的视角信息。这导致同一姿态表示在不同场景中渲染出截然不同的视角，违背了NVS的核心定义：相机姿态应当可控且可迁移。

### 核心洞察与方法定位

本文提出 **XFactor**，核心洞察是：**真正的NVS要求相机姿态表示在不同场景间可迁移**。为实现这一点，XFactor 从两个层面重构了训练范式：

1. **立体-单目模型（Stereo-Monocular Model）**：将传统多视图自编码器替换为仅使用一对图像的架构——姿态编码器（POSEENC）从两帧输入预测相对姿态，渲染器（RENDER）仅凭单张上下文图像和该姿态潜变量进行外推渲染。这一设计从根本上消除了插值偏置。

2. **跨序列可迁移性目标**：通过保持相机姿态的图像增广策略（逆遮罩、颜色抖动、模糊），生成两对像素内容几乎不重叠但相机运动相同的图像对；训练时强制模型将从序列A提取的姿态潜变量用于序列B的目标视图渲染，迫使姿态表示与场景内容解耦。

XFactor 不依赖任何3D归纳偏置——无需SE(3)显式参数化、无需多视图几何先验，仅通过未受限的256维潜变量，在训练中自发涌现出几何推理能力。

### 主要结果

在可迁移性核心指标上，XFactor 相比现有方法取得数量级提升：

- **RE10K 数据集**：可迁移性 AUC @ 20° 达到 **55.2**，RayZer 仅为 7.6（提升约 7.3 倍）。
- **DL3DV 数据集**：AUC @ 20° 达到 **57.2**，RayZer 仅为 5.9。
- **姿态探针实验**：从 XFactor 潜变量中可高度准确地解码出真实 SE(3) 相机姿态（AUC @ 30° = 72.9 vs RayZer 60.8），验证了其表示蕴含丰富的几何信息。

消融实验进一步证实：多视图训练会逐步破坏可迁移性，而立体-单目架构与可迁移性目标的组合是性能的关键来源；与 SimCLR、VICReg 等通用自监督目标相比，所提目标在姿态预测准确率上具有绝对优势。

## 背景与动机

新视角合成（Novel View Synthesis, NVS）旨在从一组已知视角的图像生成任意新视角下的场景渲染。近年来，基于学习的NVS方法取得了显著进展，但大多数方法依赖于显式的3D表示或精确的相机姿态标注。自监督NVS试图摆脱这些依赖，仅从原始视频中学习渲染新视角的能力，其核心挑战在于如何从图像中隐式地推断相机姿态。

然而，现有自监督NVS模型学到的“姿态表示”存在根本性缺陷。以**RayZer**（Jiang et al., 2025）和**RUST**（Sajjadi et al., 2023）为代表的现有方法，其训练目标本质上是一个多视图自编码过程：给定同一序列的多个上下文帧，模型学习重建该序列中的目标帧。这种范式导致姿态编码器学到的并非场景无关的相机运动信息，而是“如何从上下文帧插值出目标帧”的捷径——相同的姿态潜在变量在不同场景中会渲染出完全不同的视角，这意味着姿态表示不具备可迁移性，因而并非真正的NVS。

这一瓶颈的因果机制在于：多视图自编码目标允许模型利用场景内容的重叠信息进行帧间插值，姿态编码器无需真正理解相机几何即可完成重建任务。由此产生的姿态表示与场景内容深度耦合，无法在不同序列间迁移使用。

针对上述问题，本文提出**XFactor**，核心思路是将训练范式从多视图自编码转变为双视图外推，并引入跨序列的可迁移性目标函数。具体而言，XFactor采用立体-单目模型，仅使用一对图像作为输入，从设计上杜绝了多帧插值的可能；同时，通过保持相机姿态的图像增广策略生成像素内容不同但相机运动相同的两对图像，强制模型从一个序列提取的姿态潜在变量能够在另一序列中正确渲染目标视图。这一设计使得未受限的潜在变量能够自发学习几何推理，无需SE(3)参数化或任何3D归纳偏置。

**决定性证据**：在可迁移性测试中，XFactor在RE10K数据集上的AUC@20°达到55.2，而RayZer仅为7.6，提升超过5倍（Table 1）。姿态探针实验进一步表明，XFactor的潜在表示能高度准确地预测真实SE(3)相机姿态，AUC@30°达72.9，远超RayZer的60.8（Table 2）。消融实验证实，多视图训练会逐步破坏可迁移性，而立体-单目模型与可迁移性目标的组合取得最优效果（Table 3）。

## 核心创新

XFactor 的核心创新在于通过**训练范式重构**，从根本上解决了现有自监督 NVS 模型缺乏真正视角可控性的瓶颈。其关键洞察是：真正的 NVS 要求相机姿态表示在不同场景间可迁移；仅使用一对图像（防止插值）并结合保持相机姿态的图像增广进行跨序列训练，使得未受限的潜在变量能够自发学习几何推理，无需 SE(3) 参数化等先验。

### 瓶颈诊断：自编码范式下的插值偏置

现有自监督 NVS 模型（如 **RayZer** (Jiang et al., 2025)、**RUST** (Sajjadi et al., 2023)）普遍采用多视图自编码目标：在同一序列内最小化目标帧重建误差。这一范式存在根本性缺陷——模型学习到的姿态表示仅编码了“如何从上下文帧插值目标帧”的信息，缺乏场景无关的视角语义。因此，相同的姿态潜在变量在不同场景中会渲染出不同的视角，模型本质上只是“记忆”了特定序列的帧间关系，而非学习到真正的相机运动表征。

### 核心机制：立体-单目模型 + 跨序列可迁移性目标

XFactor 通过两项关键设计打破上述瓶颈：

**1. 立体-单目模型（Stereo-Monocular Model）**

将模型从多视图架构缩减为仅处理一对图像：姿态编码器 `POSEENC` 接收一对输入图像 `[I₁, I₂]`，输出相对姿态潜在向量 `Z₂`；渲染器 `RENDER` 仅使用单张上下文图像 `I₁` 和该姿态潜在，重建目标视图 `Ĩ₂`。这一设计从根源上消除了插值路径——模型必须仅从两张图像中推断相机运动，无法依赖多帧间的像素冗余。

**2. 可迁移性目标（Transferability Objective）**

训练目标从“同序列重建”改为“跨序列渲染”：给定两对经过不同增广的图像 `[I₁ᴬ, I₂ᴬ]` 和 `[I₁ᴮ, I₂ᴮ]`，要求模型使用从序列 A 提取的姿态潜在 `POSEENC[I₁ᴬ, I₂ᴬ]`，在序列 B 的上下文 `I₁ᴮ` 上渲染出 B 的目标视图 `I₂ᴮ`。损失函数形式为：

$$L \equiv d_I( I_2^B, \mathrm{RENDER}[ I_1^B, \mathrm{POSEENC}[ I_1^A, I_2^A ] ] )$$

这一目标强制姿态表示必须捕获场景无关的相机运动信息，因为相同的姿态潜在必须在完全不同的像素内容上产生一致的视角变换。

**3. 保持相机姿态的增广策略**

为实现上述跨序列训练，XFactor 引入表示学习启发的增广策略：对同一图像对施加逆遮罩（互补的随机等面积掩码）、颜色抖动和模糊，生成两对具有相同相机运动但像素内容几乎不重叠的图像。增广满足严格的姿态保持条件：

$$\mathrm{ORACLE}[ \mathrm{AUG}[\mathbb{Z}] ] = \mathrm{ORACLE}[ \mathrm{AUG}'[\mathbb{Z}] ] = \mathrm{ORACLE}[\mathbb{Z}]$$

这一设计使得在真实视频数据上进行可迁移性训练成为可能，无需真实相机姿态标注。

### 与基线方法的关键差异

| 设计维度 | 基线方法（RayZer/RUST） | XFactor |
|---------|----------------------|---------|
| **训练目标** | 多视图自编码（同序列重建） | 跨序列可迁移性目标 |
| **姿态编码器** | 多视图输入 | 立体-单目（仅一对图像） |
| **渲染器** | 多帧上下文 | 单帧上下文 |
| **姿态潜在** | SE(3) 参数化或瓶颈约束 | 未受限的 256 维向量 |
| **输入增广** | 无专门增广 | 保持姿态的逆遮罩/颜色抖动/模糊 |

### 证据支撑

消融实验（Table 3）直接验证了各设计选择的因果效应：
- **立体-单目 + 可迁移性目标**在所有可迁移性指标和姿态探针准确率上均取得最佳效果；
- 引入额外视图（多视图训练）会**逐步降低并最终完全破坏**可迁移性，证实了插值偏置的破坏性；
- 未受限的 256 维潜在变量优于信息瓶颈（16 维）和显式 SE(3) 参数化变体，表明模型在无几何先验的情况下自发学习了有效的姿态表征。

可迁移性测试（Table 1）进一步证实：XFactor 在 RE10K 上的 AUC @ 20° 达到 55.2，比 RayZer（7.6）高出超过 7 倍，验证了跨场景姿态迁移能力的质的飞跃。

## 整体框架

XFactor 的核心设计是一个“立体-单目”模型与跨序列可迁移性目标的结合，其整体架构与信息流如 Figure 1 所示。模型由两个核心模块构成：**POSEENC**（立体姿态编码器）与 **RENDER**（单目渲染器），二者协同工作，强制模型学习可迁移的相机姿态表示。

### 模块构成与信息流

- **POSEENC（立体姿态编码器）**：一个双视图视觉 Transformer，输入为一对图像 $(I_1, I_2)$，输出一个 256 维的相对姿态潜在向量 $Z_2$。其内部包含局部-全局注意力层和姿态头 MLP，负责从两帧之间的像素对应关系中提取相机运动信息。

- **RENDER（单目渲染器）**：一个单目渲染 Transformer，输入为单张上下文图像 $I_1$ 和姿态潜在向量 $Z_2$，输出为目标视图的预测 $\tilde{I}_2$。该模块仅依赖单帧上下文进行外推渲染，从设计上杜绝了多视图插值的可能性。

二者构成的基础模型遵循以下简洁映射：

$$\mathrm{POSEENC}[I_1, I_2] = Z_2 \quad \text{and} \quad \mathrm{RENDER}[I_1, Z_2] = \tilde{I}_2$$

### 训练范式：可迁移性目标

XFactor 的训练并不使用传统的同序列自编码目标（即在同一序列上最小化目标帧重建误差），而是引入**跨序列可迁移性目标**。具体而言：

1. **增广模块**：对一对输入图像施加保持相机姿态的增广策略（逆遮罩、颜色抖动、模糊），生成两对图像 $(I_1^A, I_2^A)$ 和 $(I_1^B, I_2^B)$。这两对图像共享相同的相对相机运动，但像素内容重叠极小，从而解耦姿态与场景内容。

2. **跨序列迁移渲染**：将序列 A 的图像对送入 POSEENC，提取其相对姿态潜在 $Z_2^A = \mathrm{POSEENC}[I_1^A, I_2^A]$；随后，将该姿态潜在与序列 B 的上下文图像 $I_1^B$ 一起送入 RENDER，要求模型重建序列 B 的目标帧 $I_2^B$。损失函数为：

$$L \equiv d_I\big( I_2^B, \mathrm{RENDER}[ I_1^B, \mathrm{POSEENC}[ I_1^A, I_2^A ] ] \big)$$

这一目标迫使 POSEENC 提取的姿态表示必须具有场景无关性——从序列 A 中学到的“视角变化”必须能在序列 B 中产生相同的视角变化，否则渲染结果将无法匹配 $I_2^B$。

### 多视图微调扩展

在立体-单目模型完成可迁移性训练后，XFactor 通过多视图微调扩展到多帧上下文设置：POSEENC 被成对应用于参考帧与各上下文帧之间，预测相对姿态潜在；RENDER 则整合多个上下文帧及其对应的迁移姿态进行渲染。这一“自举”策略使得多视图 NVS 建立在已具备可迁移性的双视图模型之上，而非从零开始的多视图自编码。

### 关键设计选择

- **无 3D 归纳偏置**：姿态潜在变量为未受限的 256 维向量，不使用显式 SE(3) 参数化或 Plücker 坐标等几何先验。
- **仅双视图外推**：立体-单目模型始终进行外推（仅用单帧上下文渲染目标），从根本上消除了多视图插值偏置。
- **增广驱动的迁移训练**：通过保持相机姿态的图像增广生成训练对，无需真实相机位姿标注即可在真实视频数据上训练。

> **验证提示**：消融实验（Table 3）证实，立体-单目模型与可迁移性目标的结合在所有指标上均优于瓶颈潜在变量、SE(3) 参数化或引入额外视图的变体；而过渡到多视图训练会逐步降低并最终完全破坏可迁移性。

## 核心模块与公式推导

### 3.1 自监督NVS的形式化框架

现有自监督NVS方法可统一分解为三个核心组件：姿态编码器 **POSEENC**、场景编码器 **SCENEENC** 和渲染器 **RENDER**。给定上下文图像 $\mathcal{C}$ 和目标图像 $\mathcal{T}$，模型首先提取潜在姿态表示 $\mathcal{Z}_T = \text{POSEENC}[\mathcal{C}, \mathcal{T}]$，随后编码场景表示 $\mathcal{S} = \text{SCENEENC}[\mathcal{C}, \mathcal{Z}_C]$，最终渲染目标视图 $\tilde{\mathcal{I}}_T = \text{RENDER}[\mathcal{S}, \mathcal{Z}_T]$。

标准自编码训练目标最小化渲染图像与真实目标图像之间的距离：

$$L \equiv d_I( \mathcal{I}_T, \mathrm{RENDER}[ \mathcal{S}, \mathcal{Z}_T ]) \tag{3}$$

该目标仅要求模型在同一序列内重建目标帧，对姿态表示是否编码了场景无关的视角信息没有任何约束，这正是现有方法无法实现真正NVS的根本原因。

### 3.2 真NVS的可迁移性定义

论文指出，真正的NVS要求相机姿态表示具有**可迁移性**——同一姿态潜在变量在不同场景中应渲染出相同的视角。这一性质可形式化为真姿态相似性指标 **TPS**：

$$\mathrm{TPS}( \mathcal{T}^A, \mathcal{T}^B ) \equiv d_{\mathrm{SE}(3)^n}( \mathrm{ORACLE}[ \mathcal{T}^A ], \mathrm{ORACLE}[ \mathcal{T}^B ]) \tag{8}$$

其中 $\mathrm{ORACLE}$ 为提取真实SE(3)相机位姿的外部工具（如VGGT或COLMAP）。TPS通过比较两条序列的全局相机轨迹来量化姿态表示的跨场景一致性，为可迁移性评估提供了数学基础。

### 3.3 立体-单目模型：消除插值偏置

为解决多视图自编码引入的插值偏置，XFactor采用**立体-单目模型**，将架构严格限制为仅使用一对输入图像：

$$\mathrm{POSEENC}[I_1, I_2] = Z_2 \quad \text{and} \quad \mathrm{RENDER}[I_1, Z_2] = \tilde{I}_2 \tag{10}$$

其中 $\mathrm{POSEENC}$ 为双视图视觉Transformer，接收一对图像并输出256维相对姿态潜在向量 $Z_2$；$\mathrm{RENDER}$ 为单目渲染器，仅使用单张上下文图像 $I_1$ 和姿态潜在 $Z_2$ 重建目标视图 $\tilde{I}_2$。由于渲染器仅能访问单帧上下文，模型被迫从双视图中外推而非插值，从根本上切断了场景内容与姿态表示之间的虚假关联。

### 3.4 可迁移性目标函数

XFactor的核心创新在于**跨序列可迁移性目标**。给定两对具有相同相对相机运动但不同像素内容的图像对 $(I_1^A, I_2^A)$ 和 $(I_1^B, I_2^B)$，训练目标要求从序列A提取的姿态潜在变量能够在序列B中正确渲染对应的目标视图：

$$L \equiv d_I( I_2^B, \mathrm{RENDER}[ I_1^B, \mathrm{POSEENC}[ I_1^A, I_2^A ] ]) \tag{11}$$

该目标的因果机制在于：如果 $\mathrm{POSEENC}$ 学习到的姿态表示包含场景特定信息，则从序列A提取的 $Z_2^A$ 无法在序列B中渲染出正确的 $I_2^B$；只有当姿态表示完全解耦于场景内容时，跨序列渲染才能成功。这迫使模型学习可迁移的、场景无关的相机视角表示。

### 3.5 保持相机姿态的增广策略

为在真实世界视频数据上构造满足可迁移性目标所需的图像对，XFactor引入**保持相机姿态的增广**。增广操作需满足严格条件：

$$\mathrm{ORACLE}[ \mathrm{AUG}[\mathbb{Z}] ] = \mathrm{ORACLE}[ \mathrm{AUG}'[\mathbb{Z}] ] = \mathrm{ORACLE}[\mathbb{Z}] \tag{12}$$

即增广不改变ORACLE提取的全局相机位姿。具体实现中，XFactor采用随机等面积逆遮罩（两遮罩并集覆盖整图）、颜色抖动和高斯模糊的组合，在最小化像素内容重叠的同时保留相机运动信息。图1示意了完整的训练流程：对同一帧对施加两种增广生成两对图像，$\mathrm{POSEENC}$ 从第一对提取相对姿态，$\mathrm{RENDER}$ 使用第二对的上下文图像和第一对的姿态潜在渲染目标。

### 3.6 多视图微调扩展

在立体-单目模型完成可迁移性训练后，XFactor通过多视图微调将模型扩展到利用更多上下文帧。$\mathrm{POSEENC}$ 以成对方式预测参考帧与各上下文帧之间的相对姿态潜在，$\mathrm{RENDER}$ 则整合多个上下文帧及其对应的迁移姿态进行渲染。该阶段保留了双视图预训练中习得的可迁移姿态表示，同时通过多帧信息提升渲染质量。消融实验（Table 3）表明，直接在多视图设置下训练会逐步破坏可迁移性，验证了“先双视图外推、再多视图微调”策略的必要性。

## 实验与分析

### 核心瓶颈与因果机制验证

XFactor 的实验设计围绕一个核心主张展开：现有自监督 NVS 模型（如 **RayZer** (Jiang et al., 2025)、**RUST** (Sajjadi et al., 2023)）的姿态表示不具备可迁移性——它们编码的是“如何从上下文帧插值目标帧”，而非场景无关的视角信息。证据来自可迁移性测试（Table 1）：RayZer 在 RE10K 上的 AUC @ 20° 仅 7.6，而 XFactor 达到 55.2，提升超过 7 倍。这一巨大差距直接验证了“多视图自编码目标导致姿态表示与场景内容耦合”的因果诊断。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_aJJppqAm6r/figures/004_Table_1.jpg]]
*Table 1: The Transferability Test. We compare the transferability of XFactor’s, RayZer’s, and RUST’s pose representations across four datasets. We evaluate using TPS with RRA, RTA, and AUC at different error thresholds. For all metrics except FID, higher is better. Visualizations of transfer renderings and camera trajectories extracted with ORACLE are shown for each method above. The target trajectory is visualized in red, XFactor in green, RayZer in blue, and RUST in gold*

XFactor 的因果扭杆（causal knob）是“立体-单目模型 + 跨序列可迁移性目标”：仅用一对输入图像（防止插值），并强制从一个序列提取的姿态潜在变量在另一序列中渲染出正确的目标视角。Table 3 的消融实验系统性地证明了这一设计的必要性——当引入额外视图时，可迁移性逐步退化并最终完全破坏。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_aJJppqAm6r/figures/007_Table_3.jpg]]
*Table 3: Ablations. We ablate potential alternative design decisions using stereo-monocular XFactor as a starting point. Models are compared in terms of transferability and pose probe efficacy*

### 主实验结果

**可迁移性测试（Table 1）** 是本文最关键的实验。使用 TPS（True Pose Similarity）指标，通过 ORACLE 提取的 SE(3) 位姿评估渲染轨迹与真实轨迹的几何一致性。结果总结如下：

| 数据集 | 方法 | AUC @ 20° | RRA @ 10° | RTA @ 10° |
|--------|------|-----------|-----------|-----------|
| RE10K | XFactor | **55.2** | 98.6 | 78.5 |
| RE10K | RayZer | 7.6 | 82.9 | 40.2 |
| RE10K | RUST | 11.3 | 84.7 | 42.8 |
| DL3DV | XFactor | **57.2** | 99.1 | 80.3 |
| DL3DV | RayZer | 5.9 | 79.4 | 35.7 |

XFactor 在所有数据集和所有阈值上均显著优于基线，且优势随阈值收紧而扩大（AUC @ 10° 差距更大），表明其姿态表示在精细几何精度上同样领先。定性可视化（Table 1 上方轨迹图）显示，XFactor 的渲染轨迹（绿色）与目标轨迹（红色）高度重合，而 RayZer（蓝色）和 RUST（金色）的轨迹严重偏离。

**姿态探针实验（Table 2）** 进一步验证了潜在姿态表示的几何保真度。冻结 POSEENC，训练一个三层 MLP 从姿态潜在向量预测真实 SE(3) 位姿。在 RE10K 上，XFactor 的 AUC @ 30° 达到 72.9，RayZer 为 60.8，RUST 为 63.4。这表明 XFactor 的姿态潜在变量不仅支持跨场景迁移渲染，还隐式编码了与真实相机运动高度一致的信息——尽管训练过程中从未接触过任何 SE(3) 参数化或 3D 几何先验。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_aJJppqAm6r/figures/006_Table_2.jpg]]
*Table 2: Pose Probe Accuracy. We report probe accuracy trained to predict ground-truth SE(3) poses from the latents of each model in terms of RRA, RTA, and AUC. We show several examples of XFactor’s poses (green) relative to ORACLE ground-truth (red). Zoom in to see details*

### 消融实验

Table 3 以立体-单目 XFactor 为起点，系统消融了四个关键设计选择：

1. **瓶颈潜在变量（Bottleneck）**：将 256 维姿态潜在压缩到 16 维。可迁移性指标与 XFactor 相当（AUC @ 20° 约 54），表明维度不是关键因素，但姿态探针准确率有所下降。

2. **SE(3) 与 Plücker 参数化（SE(3) & Plücker）**：用显式位姿参数化替代无约束潜在变量。可迁移性显著劣于 XFactor，证明显式几何先验在自监督设置下反而限制了表示学习。

3. **解码器端额外视图（Additional View: Decoder）**：RENDER 使用额外上下文帧。可迁移性开始下降（AUC @ 20° 降至约 45），说明即使是渲染端的额外信息也会引入场景依赖。

4. **编码器+解码器端额外视图（Additional View: Encoder + Decoder）**：POSEENC 和 RENDER 均使用额外视图，即完全的多视图训练。可迁移性彻底崩溃（AUC @ 20° 降至约 15），直接证明了多视图训练是插值偏置的根源。

**自监督目标对比（Table 6）** 显示，所提可迁移性目标在姿态探针准确率上绝对优于 SimCLR 和 VICReg 等通用自监督目标，验证了“渲染基目标”对几何表示学习的必要性。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_aJJppqAm6r/figures/010_Table_6.jpg]]
*Table 6: Comparison with Self-Supervised Objectives: Pose Probe Accuracy. Probe accuracy for representations produced by training with our transferability objective (results copied from Table 3), a contrastive SimCLR (Chen et al., 2020) objective, and a mutual-information based VI-CReg (Bardes et al., 2022) objective*

**可迁移性目标的鲁棒性（Table 7）**：通过时间偏移扰动构造训练对（而非使用增广策略），逐步破坏可迁移性目标。随着偏移概率增加，性能平缓下降，表明目标函数对噪声具有合理鲁棒性，不会出现突变失效。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_aJJppqAm6r/figures/011_Table_7.jpg]]
*Table 7: Robustness of Transferability Objective. We progressively corrupt our stereo-monocular transferability objective by forming pairs of sequences by sometimes applying a temporal offset to pairs of frames, instead of via our proposed augmentation strategy. XFactor results are copied from Table 3*

### 自编码重建质量与推理时增广

**Table 4** 报告了自编码重建质量。XFactor 在标准感知指标（PSNR、SSIM、LPIPS）上与基线可比，说明可迁移性目标并未牺牲重建保真度。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_aJJppqAm6r/figures/008_Table_4.jpg]]

**Table 5** 展示了推理时应用保持姿态增广的迁移渲染质量。多视图 XFactor 在增广条件下仍能保持合理的渲染质量，FID 指标表明分布级一致性良好。

### 失败模式与局限

尽管可迁移性指标大幅领先，XFactor 的渲染质量仍有明显局限：

- **大基线与分布外视角**：当目标视角与上下文帧基线较大或超出训练分布时，渲染结果出现模糊和扭曲伪影。这一现象在监督方法 **LVSM**（Jin et al., 2024）上同样存在（Figure 3），表明这是当前 NVS 方法的共性难题，而非 XFactor 特有。

- **TPS 评估的 ORACLE 依赖性**：可迁移性评估依赖外部 ORACLE 的鲁棒性。Table 8 显示，COLMAP 在视觉扰动下拒绝率极高，而 VGGT 虽更鲁棒但仍非完美。Table 9 进一步表明，COLMAP 在 RayZer 的迁移视频上几乎完全失效（拒绝率显著偏高），使得 TPS 无法有效测量基线方法的可迁移性——这实际上意味着 RayZer 的真实可迁移性可能比 Table 1 报告的更低。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_aJJppqAm6r/figures/013_Table_8.jpg]]
*Table 8: Quantitative Robustness Analysis of TPS Oracles. We evaluate the robustness of the VGGT (Wang et al., 2025b) and COLMAP (Schonberger et al., ¨ 2016; Schonberger & Frahm, 2016b) oracles against visual corruptions by mea- ¨ suring the TPS between reference and corrupted videos. A weak distortion, visualized in Fig. 2 (a), is applied to the video. We find that the VGGT oracle is significantly more robust across all datasets and metrics. In contrast, the COLMAP oracle suffers from an excessive rejection ratio, diminishing the utility of the evaluation samples*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_aJJppqAm6r/figures/016_Table_9.jpg]]
*Table 9: Fragility of COLMAP on Transferred Videos We find that COLMAP is highly fragile when applied to transferred videos. In particular, samples from the baseline method, RayZer (Jiang et al., 2025), exhibit a significantly higher rejection ratio, preventing meaningful measurement of transferability with TPS*

- **多视图扩展的插值偏置**：当前多视图 XFactor 需从双视图模型微调，且多视图姿态估计可能重新引入插值偏置。如何在自监督设置下直接训练多视图 POSEENC 而不引入插值偏置，仍是开放问题。

### 公平性说明

所有模型统一使用 L1 + LPIPS 损失、5 个上下文视图，并在相同的四数据集混合训练集上从头训练。RayZer 和 RUST 的官方代码未公开，作者根据论文描述自行实现，其中 RayZer 实现已获原作者确认。由于使用了更大的混合数据集和更少上下文视图，RayZer 的重建指标与原论文略有不同，但可迁移性评估更为严格。

### 补充图表

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_aJJppqAm6r/figures/009_Table_4.jpg]]
*Table 4: Autoencoding Reconstruction Quality. Table 5: Augmentations at Inference. We evaluate transferred rendering quality in terms of standard perceptual metrics by applying our pose-preserving augmentations at inference with multi-view XFactor*

## 方法谱系与知识库定位

### 核心瓶颈：自监督NVS中的插值偏置

现有自监督新视角合成方法（如 **RayZer** (Jiang et al., 2025) 和 **RUST** (Sajjadi et al., 2023)）在训练中隐式地学习了“如何从上下文帧插值出目标帧”的捷径。这些模型学到的姿态表示编码的是场景相关的插值信息，而非场景无关的相机视角——同一姿态表示在不同场景中会渲染出不同视角的图像，因此并非真正的NVS。XFactor的核心洞察是：**真正的NVS要求相机姿态表示在不同场景间可迁移**，即可控性等价于可迁移性。

### 方法谱系：从多视图自编码到双视图外推

XFactor在方法谱系上完成了一次范式转换，具体体现在四个关键设计槽位的改变：

| 设计槽位 | 基线方法（RayZer/RUST） | XFactor |
|---------|----------------------|---------|
| **训练目标** | 多视图自编码目标（同序列内最小化目标帧重建误差） | 跨序列可迁移性目标（强制从序列A提取的姿态在序列B中渲染对应目标视图） |
| **姿态编码器架构** | 多视图姿态编码器（处理多个上下文视图） | 立体-单目模型（仅处理一对输入图像，渲染器使用单帧上下文） |
| **输入增广** | 无专门增广或仅使用部分视图掩码（RUST） | 保持相机姿态的增广策略（逆遮罩、颜色抖动、模糊），最小化像素内容重叠 |
| **姿态潜在变量** | 显式SE(3)参数化（RayZer）或通过部分目标视图信息瓶颈（RUST） | 未受限的256维潜在向量，无需任何3D归纳偏置 |

**立体-单目模型**是消除插值偏置的关键。通过仅使用一对图像（POSEENC处理两帧，RENDER仅使用单帧上下文），模型被强制进行外推而非插值。可迁移性目标则进一步要求从一对增广图像中提取的姿态潜在变量，能在另一对增广图像中正确渲染目标视图。这种设计使得未受限的潜在变量能够自发学习几何推理，无需SE(3)参数化或任何多视图几何先验。

### 与监督方法的边界

XFactor与监督式NVS方法（如 **LVSM** (Jin et al., 2024)）的根本区别在于训练信号来源：XFactor完全自监督，不依赖任何相机姿态标注或3D信息。然而，即使是监督方法在困难视角（大基线、超出视野）下也会产生模糊或扭曲的伪影（Figure 3），这表明渲染质量的上限部分受限于NVS任务本身的难度，而非仅由监督信号决定。

### 与自监督表示学习的交叉

XFactor的可迁移性目标与经典自监督表示学习方法（如SimCLR、VICReg）存在概念上的联系，但实验表明其效果显著优于这些通用目标。在姿态探针准确率上，可迁移性目标相比SimCLR和VICReg具有绝对优势（Table 6），说明针对NVS任务定制的渲染基目标比通用对比学习或信息最大化目标更有效。

### 适用边界与局限

1. **视角外推限制**：对于大基线、超出视野或分布外视角，XFactor的渲染可能产生模糊或扭曲的伪影，影响视觉质量。这是NVS任务的固有挑战，即使是监督方法也无法完全避免。

2. **评估依赖外部Oracle**：基于TPS（True Pose Similarity）的可迁移性评估依赖于外部姿态估计Oracle的鲁棒性。COLMAP等传统SfM方法在增广或合成视频上可能失效（Table 8, Table 9），VGGT虽然更鲁棒但仍非完美。这为可迁移性的精确量化引入了不确定性。

3. **多视图扩展的插值偏置回归**：当前多视图扩展仍需从双视图模型微调，且消融实验表明引入额外视图会逐步降低可迁移性，最终完全破坏（Table 3）。如何在自监督多视图设置中直接训练多视图POSEENC而不引入插值偏置，仍是一个开放问题。

4. **场景覆盖范围有限**：实验集中在RE10K、DL3DV等室内外场景和物体级数据集，尚未在大规模开放场景或动态视频上验证。模型对动态场景、非朗伯表面、遮挡和语义信息的处理能力尚不明确。

### 开放问题

1. **多视图自监督训练的去偏置**：如何设计多视图自监督训练范式，使其在利用多帧信息的同时不重新引入插值偏置？这是将XFactor的核心思想推广到更丰富输入设置的关键挑战。

2. **可迁移性评估的完善**：如何设计更全面的可迁移性评估基准，减少对外部Oracle的依赖？TPS指标本身的可信度边界需要进一步刻画。

3. **与表示学习前沿的融合**：如何将对比学习、信息最大化等自监督表示学习的前沿思想更有效地融入渲染基目标，以进一步提升姿态表示的质量和可迁移性？

4. **泛化能力拓展**：模型能否推广到动态场景、非朗伯表面或包含复杂遮挡的环境？如何处理语义信息与几何推理的交互？这些问题决定了XFactor范式在真实世界应用中的适用范围。

## 原文 PDF

![[paperPDFs/ICLR_2026/True_Self_Supervised_Novel_View_Synthesis_is_Transferable.pdf]]
