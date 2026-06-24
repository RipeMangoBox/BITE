---
title: Featurising Pixels from Dynamic 3D Scenes with Linear In-Context Learners
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Featurising_Pixels_from_Dynamic_3D_Scenes_with_Linear_In_Context_Learners.pdf
project_link: https://lila-pixels.github.io
aliases:
- LLCL
- FPFD3SLCL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 线性上下文学习（LILA）训练策略——在时间上要求同一线性投影能从上下文帧映射到查询帧的线索图，以此强制网络学习跨帧不变的视觉表示，同时利用现成的深度和光流网络提供几何线索作为监督信号。
primary_logic: 即使使用来自预训练网络的不完美（噪声）深度和光流估计，通过线性上下文学习框架，编码器-解码器模型也能有效地学习到富含几何、语义和时间一致性的稠密特征表示，这些特征在下游任务上显著优于现有方法。
claims:
- LILA with DINO2-S14 backbone improves VOS linear probing IF by 11.1 points over the DINOv2 baseline (68.6 vs 57.5).
- LILA outperforms LoftUp by 4.3% JF on VOS without using mask supervision, demonstrating superior feature learning from videos alone.
- Removing geometric and motion cues (depth and optical flow) causes a drop of 5.3% JF in VOS-KNN, highlighting the critical role of multi-modal geometric supervision.
- The ERM distillation baseline (training to directly predict cues from a single frame) yields substantially lower VOS-KNN accuracy than LILA (63.2 JF vs 73.9 JF), confirming the ad...
---

# Featurising Pixels from Dynamic 3D Scenes with Linear In-Context Learners

> [!tip] 核心洞察
> 即使使用来自预训练网络的不完美（噪声）深度和光流估计，通过线性上下文学习框架，编码器-解码器模型也能有效地学习到富含几何、语义和时间一致性的稠密特征表示，这些特征在下游任务上显著优于现有方法。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用线性上下文学习器从动态3D场景中像素特征化 |
| 英文题名 | Featurising Pixels from Dynamic 3D Scenes with Linear In-Context Learners |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.26488) · [Project](https://lila-pixels.github.io) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | LILA (Linear In-Context Learning) |
| Dataset | DAVIS-2017, NYUv2, COCO-Stuff |

> [!tip] 效果简介
> - DAVIS-2017 (VOS) 上，IF (linear probing) 68.6 (DINO2-S14+LILA) vs 57.5 (DINO2-S14) (+11.1)；JF (k-NN) 73.9 (DINO2-S14+LILA) vs 65.5 (DINO2-S14+LoftUp) (+8.4)。
> - NYUv2 (Surface Normal Estimation) 上，RMSE (lower is better) 25.71 (DINO2-B14+LILA) vs 26.56 (DINO2-B14) (-0.85)。
> - COCO-Stuff (Semantic Segmentation) 上，mIoU 62.4 (DINO2-B14+LILA) vs 58.5 (DINO2-B14) (+3.9)。

## 概述

### 问题瓶颈

现有视觉基础模型在像素级表示上存在一个关键短板：它们难以有效嵌入视觉场景的时空属性。以 **DINOv2**（Oquab et al., arXiv 2023）为代表的图像自监督方法能够产生高质量的图像级特征，但无法建模视频中的动态元素；而视频级推理方法又难以扩展到稠密像素预测任务。这导致从视频中学习稠密且时间一致的特征表示成为一个悬而未决的问题——模型要么牺牲了空间分辨率，要么丢失了时序稳定性。

### 核心方法：线性上下文学习（LILA）

本文提出 **LILA（Linear In-Context Learning）**，一种全新的编码器-解码器预训练策略。其核心思想简洁而深刻：**强制一个线性投影同时适用于上下文帧和查询帧**。具体而言，LILA 在训练时要求从上下文帧特征到线索图（由深度、光流和自蒸馏特征拼接而成）的最优线性映射 $W^*$，也必须能够将查询帧的特征近似映射到对应的查询线索图。这一“跨帧不变投影”的约束，迫使网络学习到时间上一致的视觉表示。

LILA 的关键设计选择包括：

- **训练数据流**：从无标注视频中随机采样相邻帧对，时间窗口可变，对上下文帧和查询帧分别施加随机裁剪作为查询增强。
- **监督信号**：利用现成的深度估计和光流网络生成几何线索，辅以 PAMR 细化的编码器特征进行自蒸馏，三者拼接构成线索图。这些网络仅在训练阶段使用，推理时被完全丢弃。
- **模型架构**：冻结的预训练编码器（如 DINOv2）+ 可训练的 DPT 解码器（带跳跃连接），仅训练解码器，计算开销与标准编码器-解码器相当。
- **损失函数**：L1 重建损失与梯度匹配损失的组合，强化边缘一致性。

### 核心结论

LILA 在三个下游基准上取得了一致且显著的提升，验证了其学到的特征富含几何、语义和时间一致性：

- **视频目标分割（DAVIS-2017）**：线性探测 IF 从 DINOv2 基线的 57.5 提升至 68.6（+11.1），k-NN JF 达到 73.9，显著优于使用 SAM 掩码监督的 **LoftUp**（Huang et al., ICCV 2025）的 65.5。
- **表面法线估计（NYUv2）**：RMSE 从 26.56 降至 25.71。
- **语义分割（COCO-Stuff）**：mIoU 从 58.5 提升至 62.4（+3.9）。

消融实验进一步揭示了方法的内在机制：移除几何和运动线索导致 VOS-KNN JF 下降 5.3%，而将 LILA 替换为单帧 ERM 蒸馏则使性能从 73.9 骤降至 63.2，充分证明了跨帧线性上下文学习策略在抑制帧特定噪声方面的关键作用。

### 方法定位与知识库定位

LILA 处于**视频自监督表示学习**与**像素级特征上采样**的交汇点。与纯图像自监督方法（如 DINOv2、**FeatUp**（Fu et al., ICLR 2024））相比，LILA 引入了时序维度，使特征具备跨帧一致性；与视频自监督方法（如 **V-JEPA**（Bardes et al., TMLR 2024）、**VideoMAE**（Tong et al., NeurIPS 2022）、**CRW-ResNet18**（Jabri et al., NeurIPS 2020））相比，LILA 直接输出像素级稠密特征，避免了特征上采样的信息损失；与依赖人工标注的蒸馏方法（如 LoftUp 使用 SAM 掩码）相比，LILA 仅利用现成网络生成的噪声信号，无需任何人工标注。

### 局限与开放问题

LILA 的训练信号依赖预训练的深度和光流模型，在航空影像等域外场景中因阴影等因素导致线索不可靠，表示质量显著下降。当前仅训练解码器，编码器被冻结，联合优化的潜力尚未释放。开放问题包括：能否在训练中自举几何线索而不依赖固定预训练网络？线性上下文学习范式能否扩展到其他几何模态或多模态输入？

## 背景与动机

### 问题背景：像素级稠密特征化的挑战

视觉基础模型的兴起极大地推动了图像级理解任务的发展，然而，将这些模型迁移到需要**像素级稠密预测**的任务（如视频目标分割、表面法线估计、语义分割）时，仍面临根本性困难。核心瓶颈在于：现有视觉基础模型缺乏能有效嵌入视觉场景时空属性的像素级表示，尤其难以从视频中学习稠密且时间一致的特征。

具体而言，当前的自监督学习方法（如 **DINOv2**，Oquab et al., arXiv 2023）主要在静态图像上训练，无法建模动态场景中的运动元素和时序变化；而视频级推理方法（如 **V-JEPA**，Bardes et al., TMLR 2024；**VideoMAE**，Tong et al., NeurIPS 2022）虽然捕获了时序信息，却难以扩展到稠密像素预测，通常只能产出低分辨率的特征图。这一“静态图像方法缺时序，视频方法缺分辨率”的结构性缺口，构成了本文工作的直接驱动力。

### 现有方法的缺口

现有工作尝试从两个方向弥合上述缺口：

1. **特征上采样方法**：如 **FeatUp**（Fu et al., ICLR 2024）和 **LoftUp**（Huang et al., ICCV 2025），通过在预训练编码器之上添加可学习的上采样模块，将低分辨率特征图提升至像素级。然而，这些方法本质上仍是单帧操作，无法利用视频中的运动线索来增强时间一致性。值得注意的是，LoftUp 还依赖 SAM 掩码作为额外监督信号，限制了其在无标注场景下的适用性。

2. **视频自监督方法**：如 **CRW-ResNet18**（Jabri et al., NeurIPS 2020）和 **FlowFeat**（Araslanov et al., NeurIPS 2025），尝试从视频中学习稠密特征。但前者受限于 ResNet 架构的表达能力，后者虽利用光流作为监督，却未能充分整合几何线索（如深度）与语义线索的协同效应。

上述方法的共同缺陷在于：**缺乏一种能将几何约束、运动约束与语义约束统一在同一训练框架中的机制**，使得学习到的特征难以同时具备空间精度、时间一致性和语义判别力。

### 本文动机：从视频中学习跨帧不变的稠密表示

本文的核心动机源于一个关键观察：**即使使用从预训练网络获得的不完美（含噪声）深度和光流估计，通过设计合理的训练策略，编码器-解码器模型也能有效地学习到富含几何、语义和时间一致性的稠密特征表示**。

这一观察催生了本文的核心创新——**线性上下文学习（Linear In-Context Learning, LILA）**。其基本思想是：在时间维度上，要求同一线性投影既能从上下文帧的特征映射到其对应的线索图（深度、光流、细化编码器特征），也能从查询帧的特征映射到查询帧的线索图。这种跨帧一致性约束强制网络学习那些在视频序列中保持不变的视觉属性，从而自然地将几何、运动和语义线索融合为统一的像素级表示。

该方法的关键优势在于：
- **无需人工标注**：训练仅依赖未标注视频和现成的深度/光流网络，不涉及任何人工标注数据；
- **推理高效**：深度和光流网络仅在训练阶段用于生成监督信号，推理时被完全丢弃，模型仅需单张图像输入；
- **通用性强**：学习到的特征可同时服务于视频目标分割、表面法线估计、语义分割等多种下游任务，展现出广泛的迁移能力。

## 核心创新

### 问题瓶颈与设计动机

现有视觉基础模型（如 **DINOv2**，Oquab et al., arXiv 2023）虽在图像级表示上表现优异，但缺乏能有效嵌入视觉场景时空属性的像素级稠密表示。具体而言：图像自监督方法无法建模动态元素，而视频级推理方法（如 **V-JEPA**，Bardes et al., TMLR 2024；**VideoMAE**，Tong et al., NeurIPS 2022）难以扩展到稠密像素预测任务。由此形成一个关键瓶颈——如何从无标注视频中学习既具有几何细节、又保持时间一致性的像素级特征。

### 核心创新：线性上下文学习（LILA）

LILA 的核心思路是将“跨帧表示一致性”作为训练约束，通过一个优雅的线性投影机制实现。具体而言，给定一对相邻帧 $(I_t, I_{t+\Delta})$，训练过程包含以下关键步骤：

**线索图构建（Cue Map Generation）**：首先利用现成的深度估计网络和光流网络为每帧生成几何线索，并将其与编码器特征经 PAMR 细化后拼接，形成“线索图”作为监督信号：

$$G_{\mathrm{context}} := \mathcal{C}_0 \circ (F_t \| D_t \| U_{\uparrow}), \quad G_{\mathrm{query}} := \mathcal{C}_{\Delta} \circ (F_{t+\Delta} \| D_{t+\Delta} \| -U_{\downarrow})$$

其中 $F$ 为细化后的编码器特征，$D$ 为深度图，$U_{\uparrow}$ 和 $-U_{\downarrow}$ 分别为前向光流和反向光流的符号取反，$\mathcal{C}$ 为随机裁剪操作。

**线性上下文投影**：核心约束在于——从上下文帧特征 $x_0$ 到其线索图 $G_{\mathrm{context}}$ 的最优线性映射 $W^*$，必须同样适用于查询帧，即将查询帧特征 $x_{\Delta}$ 映射到查询线索图 $G_{\mathrm{query}}$。$W^*$ 通过岭回归求解：

$$W^* = \arg\min_W \| x_0 W - G_{\mathrm{context}} \| + \lambda \| W \|$$

这一设计的精妙之处在于：问题维度仅为特征维度 $d$（如 128–256），与像素数 $N$ 无关，因此计算开销极低，可在训练中高效求解。

**损失函数**：训练损失由两部分组成——L1 重建损失与梯度匹配损失，后者通过加权 L1 梯度差强化边缘一致性：

$$\mathcal{L}_{\mathrm{L1}} = \| x_{\Delta} W^* - G_{\mathrm{query}} \|_1$$

$$\mathcal{L}_{\nabla \times} = \omega_{\mathrm{x}} \left\| \nabla_{\mathrm{x}} (x_{\Delta} W^*) - \nabla_{\mathrm{x}} G_{\mathrm{query}} \right\|_1$$

$$\mathcal{L}_{\mathrm{LILA}} = \mathcal{L}_{\mathrm{L1}} + \gamma \mathcal{L}_{\nabla}$$

### 与 Baseline 的关键差异

相较于现有方法，LILA 在以下维度实现了根本性改变：

| 维度 | 已有方法 | LILA 方案 |
|------|---------|-----------|
| **训练策略** | 自监督对比学习/自蒸馏，或单帧特征蒸馏 | 线性上下文学习：跨帧线性投影一致性约束，强制网络学习帧间不变表示 |
| **监督信号** | 自监督目标（对比学习、掩码预测）或无蒸馏 | 深度图 + 光流图 + PAMR 细化编码器特征的拼接线索图 |
| **模型架构** | 纯编码器（ViT）或编码器+上采样模块 | 冻结预训练编码器 + 可训练 DPT 解码器（带跳跃连接），仅训练解码器 |
| **损失函数** | 对比损失、L2 回归等 | L1 重建损失 + 自适应梯度匹配损失 |
| **训练数据流** | 单张图像或固定帧间隔视频帧对 | 随机时间窗口的相邻帧对，上下文帧与查询帧分别施加随机裁剪增强 |

### 关键证据支撑

消融实验证实了 LILA 各创新组件的有效性：

- **ERM 蒸馏基线**（直接从单帧预测线索）的 VOS-KNN JF 仅为 63.2，显著低于 LILA 的 73.9（Table 5），证明线性上下文学习策略有效抑制了帧特定噪声，而非简单蒸馏外部线索。
- **移除几何和运动线索**（仅保留自蒸馏）导致 VOS-KNN JF 下降 5.3%（Table 4），表明多模态几何监督具有强协同效应。
- **移除 PAMR 细化**导致 JF 下降 2.0%，**移除随机裁剪查询**下降 1.5%，**移除时间采样**下降 1.5%，**边缘损失**贡献 1.0%（Table 5），各组件均有独立正向贡献。

值得注意的是，LILA 训练仅使用未标注视频，不依赖任何人工标注数据。深度和光流网络仅在训练阶段用于生成线索图，推理时被丢弃，模型仅需单张图像输入，推理计算量与标准编码器-解码器相同。这一设计使其在保持推理效率的同时，显著提升了特征的几何细节和时间一致性。

## 整体框架

LILA 的整体框架围绕一个冻结的视觉编码器与一个可训练的稠密解码器构建，其核心训练策略——线性上下文学习——将跨帧时间一致性约束注入像素级特征学习过程。图 1 给出了方法的高层概览：从未标注视频中训练编码器-解码器模型，输出高分辨率且时间一致的特征图。

### 模块构成与数据流

系统由以下关键模块串联而成：

1. **冻结的预训练编码器**：以 DINOv2 等视觉 Transformer 作为骨干，提取低分辨率特征图。编码器在整个训练过程中保持冻结，仅作为特征提取器。
2. **DPT 解码器**：接收编码器的多层特征（通过跳跃连接），将其上采样至像素级分辨率，输出稠密特征图 $x_0$（上下文帧）和 $x_{\Delta}$（查询帧）。解码器是唯一可训练的组件。
3. **线索图生成模块**：为上下文帧和查询帧分别构建监督信号 $G_{\mathrm{context}}$ 和 $G_{\mathrm{query}}$。每条线索图由三部分拼接而成：
   - 经 PAMR 细化后的编码器特征 $F_t$；
   - 现成单目深度网络估计的深度图 $D_t$；
   - 现成光流网络估计的光流 $U_{\uparrow}$（查询帧使用反向光流的符号取反 $-U_{\downarrow}$）。
4. **线性投影求解模块**：在上下文帧上，通过岭回归求解最优线性映射 $W^*$：
   $$W^* = \arg\min_W \| x_0 W - G_{\mathrm{context}} \| + \lambda \| W \|$$
   该问题的维度仅取决于特征通道数 $d$，与像素数 $N$ 无关，因此计算开销极低。
5. **损失计算模块**：将查询帧特征 $x_{\Delta}$ 经同一 $W^*$ 投影后，与查询线索图 $G_{\mathrm{query}}$ 计算 L1 重建损失与梯度匹配损失：
   $$\mathcal{L}_{\mathrm{L1}} = \| x_{\Delta} W^* - G_{\mathrm{query}} \|_1$$
   $$\mathcal{L}_{\nabla \times} = \omega_{\mathrm{x}} \left\| \nabla_{\mathrm{x}} (x_{\Delta} W^*) - \nabla_{\mathrm{x}} G_{\mathrm{query}} \right\|_1$$
   总损失为二者加权和：$\mathcal{L}_{\mathrm{LILA}} = \mathcal{L}_{\mathrm{L1}} + \gamma \mathcal{L}_{\nabla}$，其中 $\gamma=1$。

### 训练流程

图 2 详细描绘了训练管线。每次迭代从视频中采样一对相邻帧 $(I_t, I_{t+\Delta})$，时间间隔 $\Delta$ 在随机窗口内变化。上下文帧和查询帧分别施加随机裁剪 $\mathcal{C}_0$ 和 $\mathcal{C}_{\Delta}$ 作为查询增强。关键约束在于：从上下文帧求解的线性投影 $W^*$ 必须同样适用于查询帧——这一跨帧不变性要求迫使网络学习时间一致的视觉表示，同时有效抑制现成深度和光流网络引入的噪声。

### 推理流程

推理时，模型仅需单张图像输入，无需深度或光流网络。冻结编码器与 DPT 解码器直接输出像素级稠密特征图，计算量与标准编码器-解码器架构完全相同。这些特征可直接用于下游任务的线性探测或 k-NN 推理，无需额外微调。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/001_Figure_1.jpg]]
*Figure 1: Overview. We train an encoder-decoder model from unlabelled videos to produce high-resolution (HR), temporally consistent feature maps. The core novelty of our training approach is linear in-context learning, or LILA. Trained on noisy cue maps, such as those provided by off-the-shelf optical flow and monocular depth networks, LILA enhances the low-resolution (LR) encoder features with pixel-level geometry and temporally stable semantics*

## 核心模块与公式推导

### 整体训练流程

LILA 的训练流程围绕一个冻结的预训练编码器与一个可训练的 DPT 解码器构建。每次训练迭代从视频中采样一对相邻帧 $(I_t, I_{t+\Delta})$，其中 $\Delta$ 为随机变化的时间窗口。两帧分别经过共享的编码器-解码器网络，输出像素级特征图 $x_0$ 和 $x_{\Delta}$。核心训练策略是：从上下文帧 $I_t$ 的特征 $x_0$ 与其线索图 $G_{\mathrm{context}}$ 之间求解一个最优线性投影 $W^*$，然后要求该投影同样能将查询帧 $I_{t+\Delta}$ 的特征 $x_{\Delta}$ 映射到其线索图 $G_{\mathrm{query}}$，并通过最小化重建误差来训练网络。图 Figure 2 展示了这一训练管线的完整结构。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/002_Figure_2.jpg]]
*Figure 2: Training overview. (a) We train an encoder-decoder network (LILA) to produce pixel-level feature maps (here*

### 线索图生成模块

线索图是 LILA 训练中的监督信号，由三个模态的特征拼接而成。对于上下文帧和查询帧，其线索图分别定义为：

$$G_{\mathrm{context}} := \mathcal{C}_0 \circ (F_t \| D_t \| U_{\uparrow}), \quad G_{\mathrm{query}} := \mathcal{C}_{\Delta} \circ (F_{t+\Delta} \| D_{t+\Delta} \| -U_{\downarrow})$$

其中各变量含义如下：
- $F_t$、$F_{t+\Delta}$：经 PAMR（Pixel-Adaptive Mask Refinement）细化后的编码器特征，提供语义自蒸馏信号；
- $D_t$、$D_{t+\Delta}$：由现成的单目深度估计网络生成的深度图，提供几何线索；
- $U_{\uparrow}$：从 $I_t$ 到 $I_{t+\Delta}$ 的前向光流，$U_{\downarrow}$ 为反向光流。注意查询线索图中反向光流取负号（$-U_{\downarrow}$），以保证与上下文帧的空间对应关系在符号上一致；
- $\mathcal{C}_0$、$\mathcal{C}_{\Delta}$：分别对上下文帧和查询帧施加的随机裁剪操作，作为查询增强策略。

深度图和光流图均由预训练的现成网络生成，仅在训练阶段使用，推理时被完全丢弃。

### 线性投影求解模块

给定上下文帧的特征 $x_0 \in \mathbb{R}^{N \times d}$（$N$ 为像素数，$d$ 为特征维度）和线索图 $G_{\mathrm{context}} \in \mathbb{R}^{N \times c}$（$c$ 为线索通道数），LILA 通过岭回归求解最优线性映射 $W^* \in \mathbb{R}^{d \times c}$：

$$W^* = \arg\min_W \| x_0 W - G_{\mathrm{context}} \| + \lambda \| W \|$$

这一问题的关键在于其计算复杂度仅依赖于特征维度 $d$，与像素数 $N$ 无关，因此可以高效求解。该线性投影 $W^*$ 被视为从视觉特征到线索图的“上下文规则”，其核心假设是：在相邻帧之间，这一映射关系应保持跨帧不变。

### 损失函数模块

LILA 的总损失由 L1 重建损失与梯度匹配损失加权组合而成：

$$\mathcal{L}_{\mathrm{LILA}} = \mathcal{L}_{\mathrm{L1}} + \gamma \mathcal{L}_{\nabla}$$

其中 $\gamma$ 在所有实验中设为 1。

**L1 重建损失**衡量查询帧特征经 $W^*$ 投影后与查询线索图之间的逐像素差异：

$$\mathcal{L}_{\mathrm{L1}} = \| x_{\Delta} W^* - G_{\mathrm{query}} \|_1$$

**梯度匹配损失**用于强化边缘一致性，以水平方向为例：

$$\mathcal{L}_{\nabla \times} = \omega_{\mathrm{x}} \left\| \nabla_{\mathrm{x}} (x_{\Delta} W^*) - \nabla_{\mathrm{x}} G_{\mathrm{query}} \right\|_1$$

其中 $\omega_{\mathrm{x}}$ 为自适应权重，根据查询线索图的梯度幅值动态调整，使损失函数更关注边缘区域的重建精度。垂直方向的梯度损失 $\mathcal{L}_{\nabla y}$ 定义方式类似，总梯度损失 $\mathcal{L}_{\nabla} = \mathcal{L}_{\nabla \times} + \mathcal{L}_{\nabla y}$。

### 训练中的查询增强

为提升特征的鲁棒性，LILA 在训练时对上下文帧和查询帧分别施加独立的随机裁剪 $\mathcal{C}_0$ 和 $\mathcal{C}_{\Delta}$。这意味着 $x_0$ 和 $x_{\Delta}$ 对应的空间区域不完全一致，但 $W^*$ 仍须将从局部上下文中学到的映射关系泛化到查询帧的（可能不同的）裁剪区域。这一设计迫使网络学习对空间扰动不敏感的跨帧不变表示。消融实验表明，移除该随机裁剪会导致 VOS-KNN 的 JF 下降 1.5%（Table 5）。

## 实验与分析

### 核心瓶颈与实验设计逻辑

现有视觉基础模型普遍缺乏能有效嵌入时空属性的像素级表示：图像自监督方法无法建模动态元素，而视频级推理方法又难以扩展到稠密像素预测。LILA 通过**线性上下文学习**这一核心训练策略，强制同一线性投影从上下文帧映射到查询帧的线索图，从而学习跨帧不变的视觉表示。实验围绕三个维度验证该设计的有效性：(1) 视频目标分割（VOS）检验时空一致性；(2) 表面法线估计检验几何感知能力；(3) 语义分割检验语义质量。所有实验均使用冻结的预训练编码器，仅训练 DPT 解码器，推理时无需深度或光流网络。

### 视频目标分割（DAVIS-2017）

Table 1 展示了 DAVIS-2017 验证集上的主要结果。LILA 在两种评估协议下均显著超越基线：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/004_Table_1.jpg]]
*Table 1: Video object segmentation (DAVIS-2017, val). We evaluate LILA with linear probing and local k-NN, and report the mean Jaccard index*

- **线性探测**：以 DINO2-S14 为骨干时，LILA 的 IF 达到 68.6，较 DINOv2 基线（57.5）提升 **11.1 个百分点**；以 DINO2-B14 为骨干时，IF 为 70.4，较 FlowFeat（65.7）提升 4.7 个百分点。
- **局部 k-NN**：LILA（DINO2-S14）的 JF 达到 73.9，较使用 SAM 掩码监督的 LoftUp（65.5）高出 **8.4 个百分点**——值得注意的是，LILA 完全不依赖任何人工标注数据，仅利用现成的深度和光流网络生成训练信号。

Figure 4 的定性结果进一步印证了定量结论：LILA 在细粒度动态结构（如自行车辐条）上提供了高空间细节和强时间一致性，分割边界清晰且跨帧稳定。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results on VOS. LILA provides a high degree of spatial detail and strong temporal consistency, allowing for a high-quality segmentation of fine and dynamic structures (e.g. a bicycle)*

### 表面法线估计与语义分割

Table 2 报告了 NYUv2 表面法线估计和 COCO-Stuff 语义分割的线性探测结果。LILA 在所有骨干尺寸和训练数据集上均取得一致提升：

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/006_Table_2.jpg]]
*Table 2: Probing surface normals and semantic segmentation. We report the probing accuracy on NYUv2 (val) for surface normals in terms of Root Mean Squared Error (RMSE) and inlier ratios for thresholds*

- **表面法线估计**：DINO2-B14+LILA 的 RMSE 降至 25.71，较 DINOv2 基线（26.56）降低 0.85；在更严格的 δ₁=11.25° 阈值下，内点率亦有明显改善。
- **语义分割**：DINO2-B14+LILA 的 mIoU 达到 62.4，较 DINOv2 基线（58.5）提升 3.9 个百分点；像素准确率（pAcc）同步提升。

Table 3 的 ADE20K 和零样本 COCO-Stuff 结果进一步验证了 LILA 特征的泛化能力：在零样本设置下，LILA 对未见类别的分割 mIoU 同样优于基线，表明学习到的表示具有超越训练分布的可迁移性。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/008_Table_3.jpg]]
*Table 3: Probing segmentation: ADE20K and zero-shot COCO-Stuff. (a) Using linear probing, we evaluate LILA on ADE20K. (b) In the zero-shot setting, we train a linear probe initialised from the text embeddings, extracted from CLIP [20], of seen classes in COCO-Stuff and test on 15 unseen categories, reporting mIoU*

Figure 5 的定性对比揭示了一个值得关注的现象：尽管 LILA 在动态场景视频上训练，其在以静态为主的室内场景中仍能揭示更精细的表面结构（如家具曲面），并产生更准确的语义边界和背景细节。这暗示线性上下文学习框架所施加的跨帧一致性约束，本质上促进了网络对通用几何和语义线索的提取能力。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results: surface normal estimation and semantic segmentation. (a) Despite pre-training on dynamic scenes, LILA reveals a finer surface structure than the baseline (DINOv2 [1] / ViT-B14) in predominantly static scenes. (b) LILA enables more accurate semantic segmentation, providing more accurate semantic boundaries and background detail*

### 消融实验：线索模态与训练组件

**线索模态的协同效应**（Table 4）：移除所有几何和运动线索（仅保留自蒸馏）导致 VOS-KNN JF 从 73.9 骤降至 68.6，降幅达 **5.3 个百分点**，表明深度和光流线索具有强协同效应。单独分析各模态贡献：自蒸馏、深度、光流各自独立贡献约 1.3%、1.3% 和 1.4% JF 的提升。

**训练策略的关键性**（Table 5）：将 LILA 替换为 ERM 蒸馏基线（直接从单帧预测线索图）后，VOS-KNN JF 从 73.9 降至 63.2，降幅达 **10.7 个百分点**。这一巨大差距直接证明了线性上下文学习策略在抑制帧特定噪声方面的核心作用——ERM 基线倾向于过拟合单帧线索图中的噪声，而 LILA 的跨帧投影约束迫使网络学习时间不变的特征。

其他组件的贡献（Table 5）：
- 移除 PAMR 细化：JF 下降 2.0%
- 移除随机裁剪查询增强：JF 下降 1.5%
- 移除时间窗口采样（固定帧间隔）：JF 下降 1.5%
- 移除梯度匹配损失（仅保留 L1）：JF 下降 1.0%

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/011_Table_5.jpg]]
*Table 5: Ablation study: training components. We switch off LILA’s training components to assess their downstream impact on VOS (DAVIS 2017), surface normal estimation (NYUv2) and semantic segmentation (COCO-Stuff)*

### 骨干网络泛化与时序窗口分析

Table 6 展示了 LILA 在不同预训练骨干上的泛化能力：包括 Masked Autoencoder、带 registers 的 DINOv2 以及 DINOv3，LILA 训练后均带来一致的性能增益，表明该方法不依赖于特定编码器的归纳偏置。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/013_Table_6.jpg]]
*Table 6: Generalisation across other backbones. We report the probing accuracy by pre-training LILA with diverse backbones: Masked Autoencoder, DINOv2 with registers and DINOv3*

Figure 7 分析了时序采样窗口 Δ 大小对 VOS 性能的影响：过小的 Δ 导致帧间变化不足，无法有效学习时间一致性；过大的 Δ 则因场景变化剧烈而增加学习难度。存在一个最优窗口范围，在该范围内 LILA 能有效平衡时间一致性与学习难度。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/012_Figure_7.jpg]]
*Figure 7: The temporal gap trade-off. We report J F on VOS (DAVIS 2017) with k-NN inference for different LILA models trained with varying sizes of the sampling window ∆*

### 失败模式与局限性

Figure 6 的域外测试揭示了 LILA 的关键局限：在航空影像中，由于阴影等因素导致深度和光流线索不可靠，LILA 的表示质量显著下降，特征图被阴影混淆。这直接源于 LILA 对预训练深度和光流模型质量的依赖——当这些现成模型在目标域表现不佳时，训练信号本身即存在系统性偏差。在胸部 X 光片上，LILA 仍能产生合理的表示，表明其对线索噪声具有一定容忍度，但这种容忍度是有限的。

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/009_Figure_6.jpg]]
*Figure 6: Further qualitative analysis. (a) A qualitative comparison between LILA and ERM distillation — a distillation baseline based on the external cues without linear in-context learning. LILA yields noticeably sharper feature maps, suggesting that linear in-context learning is effective at handling inherent noise in the external cues. (b) We test LILA on out-of-domain images — here, chest X-rays and aerial imagery. Although LILA produces plausible representations for chest X-rays, its representations for aerial images are confounded by shadows, revealing a limitation*

此外，当前训练仅更新解码器而冻结编码器，可能未充分释放联合优化的潜力；训练阶段仍需额外计算深度和光流网络的前向传播，增加了训练成本（尽管推理时无需这些网络）。

### 公平性说明

实验比较遵循严格的公平性原则：(1) 所有基线模型使用相同的预训练骨干网络；(2) 评估采用标准线性探测或 k-NN 协议，不引入额外微调偏差；(3) LILA 训练仅使用未标注视频，不依赖任何人工标注数据——与之对比，LoftUp 使用了 SAM 掩码监督，FlowFeat 依赖光流标注，而 LILA 仅利用现成网络生成的自动信号。

### 补充图表

![[assets/figures/papers/paper_list_l6_https_arxiv_org_abs_2604_26488/figures/010_Table_4.jpg]]
*Table 4: Ablation study: cue modalities. We train LILA with varying modalities in the cue maps and report the accuracy on VOS (DAVIS 2017), surface normal estimation (NYUv2) and semantic segmentation (COCO-Stuff)*

## 方法谱系与知识库定位

### 1. 问题定位：从静态特征到时空一致表征

LILA 所要解决的核心瓶颈在于：现有视觉基础模型（如 DINOv2，Oquab et al., arXiv 2023）虽然具备强大的语义理解能力，但其输出特征图分辨率低且缺乏对动态场景中几何结构与时间一致性的显式建模。图像自监督方法（如 FeatUp，Fu et al., ICLR 2024）通过特征上采样提升了空间分辨率，但无法捕获视频中的运动信息；而视频自监督方法（如 V-JEPA，Bardes et al., TMLR 2024；VideoMAE，Tong et al., NeurIPS 2022；CRW-ResNet18，Jabri et al., NeurIPS 2020）虽能建模时序依赖，却难以扩展到稠密的像素级预测任务。LILA 的独特定位在于：**仅利用未标注视频和现成的几何估计网络，训练一个编码器-解码器模型，使其输出的稠密特征图同时具备几何精度、语义判别力和时间一致性**。

### 2. 与基线方法的方法论差异

LILA 的方法论创新体现在训练策略和监督信号两个维度，与现有工作形成清晰对比：

**训练策略的跃迁：从单帧蒸馏到跨帧线性上下文学习。** 传统特征上采样方法（如 FeatUp 和 LoftUp，Huang et al., ICCV 2025）采用单帧特征蒸馏范式——直接训练解码器从单张图像预测高分辨率特征或外部线索。LILA 的关键改变在于引入**线性上下文学习**：在上下文帧上求解最优线性投影 $W^*$（通过岭回归，见 Eq. (2)），然后要求该投影也能将查询帧的特征映射到对应的查询线索图。这一跨帧一致性约束迫使网络学习跨时间不变的视觉元素，从而天然抑制单帧噪声。消融实验（Table 5）直接验证了该策略的优越性：ERM 蒸馏基线（单帧预测线索）在 VOS-KNN 上仅得 63.2 JF，而 LILA 达到 73.9 JF，差距达 10.7 个百分点。

**监督信号的扩展：从单模态到多模态几何线索。** FlowFeat（Araslanov et al., NeurIPS 2025）仅利用光流作为运动监督，而 LILA 将监督信号扩展为三种线索的拼接：经 PAMR 细化的编码器特征（自蒸馏）、单目深度图和光流图（见 Eq. (1) 及线索图生成模块）。Table 4 的消融表明，移除深度和光流线索（仅保留自蒸馏）导致 VOS-KNN JF 下降 5.3%，各模态独立贡献约 1.3–1.4% JF，证明了多模态几何线索的强协同效应。

**推理效率的对比。** 与 FlowFeat 等需要在推理时计算光流的方法不同，LILA 的深度和光流网络仅在训练阶段用于生成线索图，推理时被完全丢弃。模型仅需单张图像输入，计算量与标准编码器-解码器相同，实现了训练阶段利用多帧几何信息、推理阶段保持单帧效率的实用平衡。

### 3. 知识库贡献与适用边界

LILA 对知识库的主要贡献在于：**证明了即使使用预训练网络产生的不完美（噪声）深度和光流估计，线性上下文学习框架也能有效驱动编码器-解码器模型学习到富含几何、语义和时间一致性的稠密特征**。这一发现将“上下文学习”的概念从语言模型的提示工程迁移到了视觉表征学习的训练范式设计中，为无需人工标注的视频预训练提供了新的技术路径。

**适用边界与局限：**

1. **域外泛化受限。** LILA 的训练信号依赖预训练的深度和光流模型，其表征质量受限于这些现成模型表现良好的场景。Figure 6(b) 显示，在航空影像等域外数据中，由于阴影等因素造成线索不可靠，LILA 的表示质量显著下降。在胸片 X 光图像上 LILA 尚能产生合理表征，但在航空图像中受到阴影干扰，暴露了该方法对线索质量的依赖性。

2. **编码器冻结的取舍。** 当前训练仅更新 DPT 解码器，编码器被冻结。这一设计降低了训练成本并保持了编码器的通用性，但也可能未充分释放联合优化的潜力。Table 6 展示了 LILA 在 MAE、DINOv2 with registers 和 DINOv3 等多种骨干网络上的泛化能力，但端到端微调编码器是否能进一步提升性能仍是开放问题。

3. **训练成本。** 虽然推理时无需深度/光流网络，但训练阶段仍需计算这些额外的神经网络输出，增加了训练开销。这一成本能否通过自举式线索学习（即在训练过程中联合学习几何线索）来降低，是值得探索的方向。

### 4. 开放问题

LILA 开辟了若干值得进一步研究的方向：

- **自举式线索学习。** 能否在训练过程中联合学习或自举几何线索，而不依赖固定的预训练深度和光流网络？这将使 LILA 摆脱对现成几何估计器的依赖，扩展其适用范围。
- **模态扩展。** 线性上下文学习框架是否可扩展到其他几何模态（如表面法线、3D 点云）或多模态输入（如语言-视频联合建模）？当前工作仅验证了深度和光流两种线索，框架本身对线索类型并无硬性约束。
- **编码器联合优化。** 端到端微调编码器（而非冻结）配合 LILA 训练能否进一步提升性能？Table 6 已展示跨骨干的泛化能力，但联合优化的增益尚未被量化。
- **静态数据适应。** 在仅有静态图像数据的情况下，LILA 的训练范式能否利用合成视频或几何增广进行适应？这将决定该方法能否推广到视频数据稀缺的领域。

## 原文 PDF

![[paperPDFs/CVPR_2026/Featurising_Pixels_from_Dynamic_3D_Scenes_with_Linear_In_Context_Learners.pdf]]