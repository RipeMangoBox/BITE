---
title: "EgoHandICL: Egocentric 3D Hand Reconstruction with In-Context Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/EgoHandICL_Egocentric_3D_Hand_Reconstruction_with_In_Context_Learning_e95df01ae740.pdf
project_link: "https://openreview.net/forum?id=rk6qdGgCZ"
code_link: "https://github.com/Nicous20/EgoHandICL"
aliases:
- EgoHandICL
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用视觉-语言模型引导的多模态模板检索构建上下文示例，通过掩码重建在上下文学习范式下优化手部参数估计。
primary_logic: 将自我中心3D手部重建转化为上下文学习任务，借助检索到的多模态示例提供先验知识，使模型在严重遮挡和歧义场景下具备示例引导的推理能力。
claims:
- EgoHandICL 在 ARCTIC 数据集上将 P-MPVPE 相对于最优基线降低 31.1%，并在双手设置下将 MRRPE 减少 12%。
- 使用推理式提示的模板检索策略（Reas. Prompts）进一步降低 P-MPJPE 至 3.9 mm，相比无提示策略提升显著。
- 70% 的 ICL token 掩码比率达到最佳重建精度，同时 3D 感知损失与几何损失联合训练带来最佳顶点误差。
- ARCTIC 上 P-MPJPE (mm) = 4.0
---

# EgoHandICL: Egocentric 3D Hand Reconstruction with In-Context Learning

> [!tip] 核心洞察
> 将自我中心3D手部重建转化为上下文学习任务，借助检索到的多模态示例提供先验知识，使模型在严重遮挡和歧义场景下具备示例引导的推理能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | EgoHandICL：基于上下文学习的自我中心3D手部重建 |
| 英文题名 | EgoHandICL: Egocentric 3D Hand Reconstruction with In-Context Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=nwjy9BeorI) · [Code](https://github.com/Nicous20/EgoHandICL) · [arXiv](https://arxiv.org/abs/2309.16609) · [Project](https://openreview.net/forum?id=rk6qdGgCZ) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | EgoHandICL |
| Dataset | ARCTIC, EgoExo4D |

> [!tip] 效果简介
> - ARCTIC 上，P-MPJPE (mm) 4.0 vs 5.5 (WiLoR) (-1.5)；P-MPVPE (mm) 3.8 vs 5.5 (WiLoR) (-1.7)；MRRPE (mm, Bimanual) 6.2 vs 7.1 (WildHand) (-0.9)。
> - EgoExo4D 上，MPJPE (mm) 21.1 vs 25.5 (PCIE) (-4.4)；P-MPJPE (mm) 7.7 vs 8.5 (PCIE) (-0.8)。

## 概述

自我中心视角下的 3D 手部重建面临深度歧义、严重自遮挡及复杂手-物交互三重挑战，现有方法依赖辅助线索进行单步回归，在极端遮挡场景中鲁棒性与泛化性不足。**EgoHandICL** 将重建任务重新定义为上下文学习（In-Context Learning）问题：利用视觉-语言模型引导的多模态模板检索构建上下文示例，通过掩码重建 Transformer 在示例先验的引导下精炼粗估计的 MANO 参数，从而在歧义和遮挡条件下实现示例引导的推理。

核心改进体现在四个层面：
- **推理范式转换**：从单图直接回归 MANO 参数转变为基于检索示例的条件化精炼。
- **互补模板检索**：结合预定义视觉模板（手部参与分类）和自适应文本模板（VLM 语义描述）两种策略，获取视觉与语义相似的多模态示例。
- **多模态上下文标记化**：将图像、结构（MANO 参数）和文本信息融合为统一的 ICL tokens，供 Transformer 进行上下文推理。
- **掩码重建训练**：基于 MAE 设计训练目标，训练时部分掩码目标 tokens，推理时完全掩码查询目标 tokens，迫使模型从输入 tokens 中重建精确的手部参数。

在 ARCTIC 数据集上，EgoHandICL 将 P-MPVPE 相对于最优基线 **WiLoR**（Potamias et al., 2025）降低 31.1%（5.5 → 3.8 mm），双手设置下 MRRPE 减少 12%（7.1 → 6.2 mm）。在 EgoExo4D 数据集上，MPJPE 从 25.5 mm 降至 21.1 mm。消融实验证实，推理式提示检索策略将 P-MPJPE 进一步压缩至 3.9 mm，70% 的 ICL token 掩码比率与联合 3D 感知损失训练共同达到最优顶点精度。方法不依赖特定粗估计主干，对 **HaMeR**（Pavlakos et al., 2024）和 WiLoR 均带来 16.1% 至 27.3% 的相对增益。

主要局限在于 VLM 检索引入的计算开销限制了实时部署，且模板数据库的多样性与质量直接影响重建性能。当前自我中心数据集缺乏完整 MANO 参数真值，评估依赖真实边界框，缺乏端到端的公平基准。未来方向包括轻量化检索策略、扩展至连续手部跟踪与手-物联合重建，以及构建全面标注的自我中心 3D 基准。

## 背景与动机

自我中心视角下的 3D 手部重建是具身智能、增强现实和人机交互领域的核心感知任务。与第三人称视角不同，自我中心图像面临**深度歧义严重、手部自遮挡频繁、手-物交互高度复杂**三重挑战。这些挑战导致现有方法在鲁棒性和泛化性上存在显著不足。

当前主流方法——如 **HaMeR**（Pavlakos et al., 2024）、**WiLoR**（Potamias et al., 2025）和 **WildHand**（Prakash et al., 2024）——普遍采用从单张图像直接回归 MANO 参数的范式。尽管这些方法在常规场景下表现良好，但在严重遮挡或双手交叉等困难情形下，其重建质量急剧下降：WiLoR 可能将遮挡的左手误认为右手，HaMeR 则可能在仅有单手可见时错误地重建出双手。根本原因在于，这类方法缺乏对场景上下文的显式建模能力，无法利用相似场景的先验知识来消解歧义。

**核心瓶颈**：自我中心手部重建的本质难点并非特征提取能力不足，而是**单张图像所蕴含的信息量不足以唯一确定 3D 手部姿态**——尤其是在遮挡和深度歧义并存的条件下。因此，突破的关键在于引入额外的结构化先验来约束解空间。

本文的**核心动机**正是将上下文学习范式引入自我中心 3D 手部重建。通过检索与查询图像上下文相似的模板示例，构建“输入-输出”示例对作为上下文条件，模型得以在推理时借鉴模板中的手部姿态先验，从而在严重遮挡和歧义场景下实现示例引导的精确重建。这一思路将手部重建从“单图回归”重新定义为“条件推理”问题，为突破现有方法的泛化瓶颈提供了新的技术路径。

## 核心创新

EgoHandICL 的核心创新在于将自我中心 3D 手部重建**重新定义为上下文学习任务**，通过检索多模态模板示例为严重遮挡和歧义场景提供先验引导。与现有方法从单张图像直接回归 MANO 参数不同，EgoHandICL 引入了三个关键机制：

### 1. 上下文学习推理范式

传统方法（如 **HaMeR**、**WiLoR**）将手部重建建模为从图像 $I$ 到 MANO 参数 $\mathcal{M}$ 的直接映射 $\mathcal{M} = \mathcal{G}(I)$。EgoHandICL 则将其转化为上下文条件下的精炼过程：

$$\mathcal{M}_{\mathrm{qry}} = \mathcal{F}(\tilde{\mathcal{M}}_{\mathrm{qry}} | \mathcal{C}_{\mathcal{M}})$$

其中 $\tilde{\mathcal{M}}_{\mathrm{qry}}$ 为粗估计的 MANO 参数，$\mathcal{C}_{\mathcal{M}} = \{(\tilde{\mathcal{M}}_{\mathrm{tpl}}, \mathcal{M}_{\mathrm{tpl}})\}$ 为检索到的模板示例对。模型通过条件化于这些示例，学习从粗估计到精细参数的映射关系，而非从零开始回归。这一范式转换使得模型在双手交叉、严重遮挡等极端场景下具备示例引导的推理能力。

### 2. 互补式多模态模板检索

EgoHandICL 设计了两种互补的检索策略来构建上下文示例集：

- **预定义视觉模板**：利用 VLM 将查询图像的手部参与类型分类为左手、右手、双手或无手四类，并检索同类型的模板图像。该策略提供了粗粒度的结构先验。
- **自适应文本模板**：通过向 VLM 输入交互特定的推理式提示，生成查询图像的语义描述，再基于文本相似度检索模板。该策略捕捉了更细粒度的语义和交互上下文。

消融实验表明，推理式提示（Reas. Prompts）将 P-MPJPE 从无提示策略的 4.3 mm 进一步降至 3.9 mm，验证了语义引导检索的有效性。

### 3. 掩码重建驱动的多模态上下文标记器

EgoHandICL 设计了一个多模态 ICL Tokenizer，将查询和模板的**图像 tokens、结构 tokens（MANO 参数）和文本 tokens** 融合为统一的四组 ICL tokens（模板输入、模板目标、查询输入、查询目标）。训练时，随机掩码部分目标 tokens，通过基于 MAE 的 Transformer 进行重建，模拟推理时仅有输入 tokens 可用的场景。推理时，查询目标 tokens 被完全掩码，模型仅从输入 tokens 重建查询的 MANO 参数。

掩码比率的消融显示，**70% 的掩码比率**达到最佳性能（P-MPJPE 4.0, P-MPVPE 3.8），过低的掩码比率导致模型过度依赖目标 tokens 而削弱上下文推理能力。

### 4. 手部特定的 3D 感知损失

除标准的 MANO 参数损失 $\mathcal{L}_{mano}$ 和顶点损失 $\mathcal{L}_{V}$ 外，EgoHandICL 引入了一个手部特定的 3D 感知损失 $\mathcal{L}_{3D}$，在预训练 3D 编码器（Uni3D-ti）的特征空间中对预测点云与真值点云进行 L2 对齐：

$$\mathcal{L}_{3D} = \|\phi(\mathcal{P}) - \phi(\mathcal{P}^{\mathrm{gt}})\|_2^2$$

该损失提供了语义层面的手部几何约束，弥补了纯几何损失在严重遮挡下监督信号不足的问题。消融实验证实，联合使用三种损失函数可达到最优顶点误差（P-MPVPE 3.8）。

### 5. 主干无关的通用精炼能力

EgoHandICL 不依赖特定的粗估计主干网络。实验表明，无论是基于 **HaMeR** 还是 **WiLoR** 的粗估计，EgoHandICL 均能带来 16.1% 至 27.3% 的相对性能增益，验证了该方法作为通用精炼模块的即插即用特性。

## 整体框架

EgoHandICL 将自我中心 3D 手部重建转化为**上下文学习（In-Context Learning, ICL）** 任务。其核心思路是：给定一张查询图像 $I_{\mathrm{qry}}$，先通过现成的粗估计网络获得初始 MANO 参数 $\tilde{\mathcal{M}}_{\mathrm{qry}}$，然后利用从数据库中检索到的模板示例对 $\mathcal{C}_{\mathcal{M}} = \{(\tilde{\mathcal{M}}_{\mathrm{tpl}}, \mathcal{M}_{\mathrm{tpl}})\}$ 作为上下文条件，驱动一个掩码重建 Transformer 对粗估计进行精炼，输出最终参数 $\mathcal{M}_{\mathrm{qry}}$：

$$\mathcal{M}_{\mathrm{qry}} = \mathcal{F}(\tilde{\mathcal{M}}_{\mathrm{qry}} | \mathcal{C}_{\mathcal{M}}) \quad \text{(Eq. 3)}$$

整个框架由三个关键模块串联而成，信息流如图 2 所示：

### 模块一：模板检索（Template Retrieval）

该模块负责为查询图像构建上下文示例集。EgoHandICL 设计了两种互补的检索策略：

- **预定义视觉模板（Pre-defined Visual Templates）**：利用视觉-语言模型（VLM）将手部参与类型自动分类为左手、右手、双手或无手四类，从数据库中检索相同参与类型的模板图像及其对应的 MANO 真值参数。
- **自适应文本模板（Adaptive Textual Templates）**：通过向 VLM 提供自我中心场景的推理式提示（如手-物交互语义描述），生成查询图像的语义描述，再基于文本相似度检索语义匹配的模板。

两种策略共同构成上下文示例集 $\mathcal{C}_{\mathcal{M}}$，为后续推理提供视觉与语义先验。

### 模块二：ICL Tokenizer（多模态上下文标记器）

该模块将查询与模板的多模态信息统一编码为 ICL tokens，供 Transformer 进行上下文推理。具体而言，对于每个查询和模板样本，分别提取三类特征：

- **图像 tokens**：由 ViT 图像编码器提取的视觉特征。
- **结构 tokens**：由粗估计网络输出的 MANO 参数（姿态 $\Theta$、形状 $\beta$、全局朝向 $\Phi$）经嵌入后得到的结构化表示。
- **文本 tokens**：由 Qwen-7B 文本编码器对语义描述进行编码。

这些特征被对齐并融合为四组 ICL tokens：模板输入 tokens $T_{\mathrm{tpl}}^{\mathrm{in}}$、模板目标 tokens $T_{\mathrm{tpl}}^{\mathrm{tar}}$、查询输入 tokens $T_{\mathrm{qry}}^{\mathrm{in}}$ 和查询目标 tokens $T_{\mathrm{qry}}^{\mathrm{tar}}$。其中，目标 tokens 对应 MANO 参数的真值（训练时）或待预测的掩码位置（推理时）。

### 模块三：掩码重建 Transformer（Masked Reconstruction for ICL）

该模块是上下文学习的执行核心，基于 MAE（Masked Autoencoder）范式设计。训练时，随机掩码部分目标 tokens（包括模板和查询的目标 tokens），迫使 Transformer 从可见的输入 tokens 中学习重建被掩码的 MANO 参数。推理时，查询目标 tokens 被完全掩码，网络仅依据查询输入 tokens 和完整的模板上下文来预测查询的精细 MANO 参数。

这种设计使得模型在训练中即经历了“不完整监督”的模拟，从而在推理时能够自然地处理自我中心场景下的深度歧义和严重遮挡——即使查询图像本身信息不足，仍可借助检索到的模板示例进行示例引导的鲁棒推理。

### 训练目标

EgoHandICL 的损失函数由三项加权组合而成（ARCTIC 数据集）：

$$\mathcal{L} = \lambda_m \mathcal{L}_{mano} + \lambda_v \mathcal{L}_{V} + \lambda_{3D} \mathcal{L}_{3D} \quad \text{(Eq. 6)}$$

其中 $\mathcal{L}_{mano}$ 为 MANO 参数的 L2 损失（姿态、形状、全局朝向），$\mathcal{L}_{V}$ 为 3D 顶点的 L1 损失，$\mathcal{L}_{3D}$ 为基于预训练 3D 编码器（Uni3D-ti）特征空间的感知损失，提供语义层面的几何约束。对于缺乏 MANO 真值的 EgoExo4D 数据集，则以 3D 关键点 L1 损失 $\mathcal{L}_{J}$ 替代参数级监督。

> **需注意**：当前分析基于论文方法部分与全局实验事实的综合提炼。关于各模块的具体消融效果（如掩码比率 70% 最优、推理式提示增益等）将在后续实验分析章节中详细呈现。

### 补充图表

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our EgoHandICL framework. Part A: Given a query image, we retrieve templates via two complementary strategies. Pre-defined Visual Templates: a VLM classifies the hand-involvement type and retrieves a template image of the same type. Adaptive Textual Templates: we prompt the VLM to generate semantic descriptions, and retrieve a template image given textual similarity. Part B: We encode image tokens*

## 核心模块与公式推导

EgoHandICL 将自我中心 3D 手部重建重新定义为上下文学习任务，其核心思想是：给定查询图像，先获取粗估计的 MANO 参数，再以检索到的模板示例对为条件，通过上下文推理精炼最终参数。整个框架围绕三个关键模块展开：模板检索、ICL Tokenizer 和掩码重建 Transformer。

### 问题形式化

给定输入图像 $I$，传统方法直接学习映射 $\mathcal{M} = \mathcal{G}(I)$，其中 $\mathcal{M}$ 为 MANO 参数集。EgoHandICL 则引入上下文示例集 $\mathcal{C}_{\mathcal{M}} = \{(\tilde{\mathcal{M}}_{\mathrm{tpl}}, \mathcal{M}_{\mathrm{tpl}})\}$，包含模板图像的粗估计参数与真值参数对，将重建转化为条件推理问题：

$$\mathcal{M}_{\mathrm{qry}} = \mathcal{F}(\tilde{\mathcal{M}}_{\mathrm{qry}} | \mathcal{C}_{\mathcal{M}})$$

其中 $\tilde{\mathcal{M}}_{\mathrm{qry}}$ 为查询图像的粗估计 MANO 参数，$\mathcal{M}_{\mathrm{qry}}$ 为精炼后的最终输出。这一形式化将“从单张图像直接回归”的范式转变为“基于示例引导的条件精炼”，使得模型在严重遮挡和深度歧义场景下具备示例驱动的推理能力。

### 模板检索模块

模板检索是构建上下文示例集的核心步骤。EgoHandICL 设计了两种互补的检索策略：

- **预定义视觉模板**：利用视觉-语言模型将查询图像的手部参与类型分类为左手、右手、双手或无手四类，从数据库中检索相同类型的模板图像。该策略利用手部参与模式作为粗粒度的视觉先验。
- **自适应文本模板**：通过向 VLM 输入以自我中心线索设计的推理式提示，生成查询图像的语义描述，再基于文本相似度检索模板。消融实验表明，推理式提示（Reas. Prompts）将 P-MPJPE 从无提示策略的 4.3 mm 降至 3.9 mm，验证了语义引导检索的有效性。

两种策略分别从视觉结构和语义内容两个维度捕获上下文相关性，确保检索到的模板在几何配置和交互语义上与查询图像高度匹配。

### ICL Tokenizer

ICL Tokenizer 负责将多模态信息统一编码为 Transformer 可处理的 token 序列。对于每组查询-模板对，Tokenizer 生成四组 ICL tokens：

- $T_{\mathrm{tpl}}^{\mathrm{src}}$：模板图像的源 tokens，融合图像特征与粗估计 MANO 参数的结构编码
- $T_{\mathrm{tpl}}^{\mathrm{tar}}$：模板图像的目标 tokens，融合图像特征与真值 MANO 参数的结构编码
- $T_{\mathrm{qry}}^{\mathrm{src}}$：查询图像的源 tokens，仅包含图像特征与粗估计参数
- $T_{\mathrm{qry}}^{\mathrm{tar}}$：查询图像的目标 tokens，推理时完全掩码，由模型从上下文重建

每组 token 由图像编码（ViT 骨干，与 WiLoR 一致）、结构编码（MANO 参数嵌入）和文本编码（Qwen-7B 生成的语义嵌入）三部分融合而成。这种统一的多模态表示使得 Transformer 能够在同一特征空间中建立查询与模板之间的对应关系。

### 掩码重建 Transformer

推理网络采用基于 MAE 的掩码重建架构。训练时，随机部分掩码 $T_{\mathrm{tpl}}^{\mathrm{tar}}$ 和 $T_{\mathrm{qry}}^{\mathrm{tar}}$ 的目标 tokens，迫使模型从可见的源 tokens 和未掩码的目标 tokens 中学习重建完整的 MANO 参数。推理时，$T_{\mathrm{qry}}^{\mathrm{tar}}$ 被完全掩码，模型仅依据 $T_{\mathrm{tpl}}^{\mathrm{src}}$、$T_{\mathrm{tpl}}^{\mathrm{tar}}$ 和 $T_{\mathrm{qry}}^{\mathrm{src}}$ 重建查询目标参数。

掩码比率是关键的调控变量：70% 的掩码比率取得最优性能（P-MPJPE 4.0 mm，P-MPVPE 3.8 mm），过低的掩码比率使任务过于简单而缺乏泛化性，过高则导致信息不足。

### 损失函数设计

训练目标由三项损失加权组合：

$$\mathcal{L} = \lambda_m \mathcal{L}_{mano} + \lambda_v \mathcal{L}_{V} + \lambda_{3D} \mathcal{L}_{3D}$$

**MANO 参数损失** $\mathcal{L}_{mano}$ 对姿态 $\Theta$、形状 $\beta$ 和全局朝向 $\Phi$ 施加 L2 约束：

$$\mathcal{L}_{mano} = \|\Theta - \Theta^{\mathrm{gt}}\|_2^2 + \|\beta - \beta^{\mathrm{gt}}\|_2^2 + \|\Phi - \Phi^{\mathrm{gt}}\|_2^2$$

**顶点损失** $\mathcal{L}_{V}$ 在 3D 顶点级别施加 L1 约束：

$$\mathcal{L}_{V} = \|V_{3D} - V_{3D}^{\mathrm{gt}}\|_1$$

**3D 感知损失** $\mathcal{L}_{3D}$ 是本文的关键创新之一。它利用预训练的 3D 编码器 Uni3D-ti 提取手部点云 $\mathcal{P}$ 的深层语义特征，在特征空间进行 L2 对齐：

$$\mathcal{L}_{3D} = \|\phi(\mathcal{P}) - \phi(\mathcal{P}^{\mathrm{gt}})\|_2^2$$

该损失超越了单纯的顶点级几何约束，提供了语义层面的手部结构监督。消融实验证实，联合使用三项损失取得最佳顶点精度（P-MPVPE 3.8 mm），而单独使用 MANO 损失或顶点损失均无法达到同等精度。对于缺乏 MANO 真值的 EgoExo4D 数据集，则使用 3D 关键点 L1 损失 $\mathcal{L}_{J} = \|J_{3D} - J_{3D}^{\mathrm{gt}}\|_1$ 替代 MANO 参数损失。

权重配置为 $\lambda_m=0.05$、$\lambda_v=5.0$、$\lambda_{3D}=0.01$，反映了对不同监督信号相对重要性的平衡。

## 实验与分析

### 主要定量结果

EgoHandICL 在两个主流自我中心手部数据集 ARCTIC 和 EgoExo4D 上均取得了最优性能。在 ARCTIC 数据集的一般设置下，EgoHandICL 的 P-MPJPE 达到 **4.0 mm**，P-MPVPE 达到 **3.8 mm**，相较于此前最优基线 WiLoR（P-MPJPE 5.5 mm，P-MPVPE 5.5 mm）分别降低了 27.3% 和 30.9%（Table 1）。在双手设置下，EgoHandICL 的 MRRPE 为 **6.2 mm**，较最优基线 WildHand 的 7.1 mm 降低 12.7%，PA-MPVPE 降低 24.5%（Table 1）。在 EgoExo4D 数据集上，EgoHandICL 的 MPJPE 为 **21.1 mm**，P-MPJPE 为 **7.7 mm**，均优于所有对比方法（Table 2）。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/003_Table_1.jpg]]
*Table 1: Quantitative results on the ARCTIC dataset. We follow the standard evaluation protocol and report both the joint- and vertex-level metrics*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/004_Table_2.jpg]]
*Table 2: Quantitative results on the EgoExo4D dataset. We follow the standard evaluation protocol and report the joint-level metrics*

上述结果验证了核心洞察：通过将 3D 手部重建转化为上下文学习任务，EgoHandICL 能够利用检索到的多模态模板示例为严重遮挡和歧义场景提供有效的先验引导。公平性方面，所有基线方法均在相同训练划分上微调且未使用外部数据；双手评估仅考虑双方均被正确检测的样本，排除了检测能力差异带来的偏差。

### 消融实验分析

#### 模板检索策略的有效性

自适应文本模板检索中，推理式提示（Reas. Prompts）相较于无提示检索将 P-MPJPE 从 4.3 mm 降至 **3.9 mm**（Table 4），表明 VLM 生成的语义描述能够更精准地匹配视觉上相似的手部交互模式。预定义视觉模板与自适应文本模板形成互补：前者通过手部参与类型（左手、右手、双手、无手）提供粗粒度结构先验，后者通过语义相似性提供细粒度外观和交互先验。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/008_Table_4.jpg]]
*Table 4: Comparison of different prompts for adaptive textual templates retrieval. Results are tested on the ARCTIC dataset*

#### 上下文学习机制的关键设计

- **掩码比率**：ICL tokens 的掩码比率在 70% 时取得最佳性能（P-MPJPE 4.0 mm，P-MPVPE 3.8 mm），过低（50%）导致重建任务过于简单而缺乏泛化性，过高（90%）则信息不足难以有效重建（Table 6）。
- **损失函数**：联合使用 MANO 参数损失、顶点损失和 3D 感知损失得到最优顶点精度（P-MPVPE 3.8 mm）。单独使用 MANO 损失时 P-MPVPE 为 4.2 mm，加入顶点损失后降至 4.0 mm，再加入 3D 感知损失后进一步降至 3.8 mm（Table 7），验证了 3D 感知损失在语义层面对手部几何约束的有效性。
- **主干网络无关性**：EgoHandICL 对 HaMeR 和 WiLoR 两种粗估计主干均带来显著增益，相对提升幅度为 +16.1% 至 +27.3%（Table 5），表明上下文学习精炼范式具有通用性，不依赖特定粗估计架构。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/009_Table_6.jpg]]
*Table 6: Comparison of different mask ratios for ICL tokens. Results are tested on the ARC-TIC dataset*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/011_Table_7.jpg]]
*Table 7: Comparison of different loss items for the EgoHandICL training. Results are tested on the ARCTIC dataset*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/010_Table_5.jpg]]
*Table 5: Comparison of coarse MANO prediction backbones. Improvement denotes relative gains over the corresponding baseline performance on the ARCTIC dataset in Tab. 1*

#### 跨手部参与类型的上下文推理

Table 3 展示了不同手部参与类型子数据集上的上下文推理分析。在左手、右手、双手和无手四种划分下，EgoHandICL 均能通过检索同类型模板获得一致的性能提升，验证了上下文示例的领域匹配性对重建精度的重要性。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/005_Table_3.jpg]]
*Table 3: In-context reasoning analysis across different hand-involvement types. L, R, T, and N denote training on the left-hand, right-hand, two-hand, and non-hand involvement type sub-dataset, respectively. Results are tested on the ARCTIC under these four sub-dataset divisions*

### 定性结果分析

Figure 3 展示了 ARCTIC 数据集上的定性对比。在双手交叉且左手严重遮挡的极端场景下，WiLoR 仅重建出右手却错误地将其标记为左手，而 EgoHandICL 通过检索到的双手交互模板成功重建了双手的正确姿态和位置。Figure 4 进一步展示了 EgoExo4D 及自采数据上的结果：在单手严重遮挡案例中，HaMeR 错误地重建出两只手，WiLoR 则完全无法重建，而 EgoHandICL 利用上下文示例的先验知识准确恢复了被遮挡手部的姿态。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/006_Figure_3.jpg]]
*Figure 3: Qualitative results on the ARCTIC dataset. Note: In the bottom case, where the two hands cross and the left hand is severely occluded, WiLoR (Potamias et al., 2025) reconstructs only the right hand but mistakenly identifies it as the left*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative results on the EgoExo4D dataset (left) and self-captured cases (right). Note: In the bottom-left case with a single heavily occluded hand, HaMeR (Pavlakos et al., 2024) mistakenly reconstructs two hands, whereas WiLoR (Potamias et al., 2025) fails to reconstruct any*

### 下游应用验证

EgoHandICL 的重建结果可作为视觉提示增强视觉-语言模型的手-物交互推理能力。Table 8 显示，将 EgoHandICL 的重建结果融入 EgoVLM 后，手部相关动作识别的准确性得到提升。Figure 5 的定性对比表明，结合 EgoHandICL 的重建信息后，EgoVLM 能够更可靠地识别自我中心视频中的细粒度手部动作。

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/013_Figure_5.jpg]]
*Figure 5: EgoVLM’s hand–object interaction reasoning with and without EgoHandICL. By incorporating our hand reconstructions as visual prompts, hand-related actions in egocentric videos can be recognized reliably with finer details*

![[assets/figures/papers/paper_list_l24_https_openreview_net_forum_id_nwjy9BeorI/figures/012_Table_8.jpg]]
*Table 8: Comparison of EgoVLMs on handobject interaction reasoning*

### 失败模式与局限性

尽管 EgoHandICL 在多个基准上表现优异，仍存在以下局限：

1. **计算开销**：依赖 VLM 进行模板检索引入了显著的计算负担，难以部署在资源受限的实时设备上。
2. **模板数据库依赖**：检索和重建性能受限于模板数据库的质量和多样性，在分布外场景下模板匹配度下降时，性能可能退化。
3. **标注约束**：EgoExo4D 等数据集仅提供关键点级标注，缺乏完整 MANO 参数真值，限制了模型在复杂场景下的泛化能力——这一问题在 Table 2 中 EgoExo4D 的绝对 MPJPE（21.1 mm）远高于 ARCTIC 的 P-MPJPE（4.0 mm）上有所体现。
4. **检测依赖**：现有评估均基于真实边界框，而自我中心视角下的手部检测本身极具挑战性，缺乏端到端的公平评估基准。

## 方法谱系与知识库定位

### 1. 与已有工作的关系

EgoHandICL 处于 **自我中心 3D 手部重建** 与 **上下文学习（In-Context Learning, ICL）** 的交叉地带。其核心推进在于将手部重建从单图回归范式迁移到示例引导的推理范式。

**（1）相对于回归式重建方法的改进**

现有主流方法均采用“单张图像 → MANO 参数”的直接映射：
- **HaMeR**（Pavlakos et al., 2024）基于 Vision Transformer 实现通用手部重建，但在严重遮挡下易产生双手误检或漏检（见 Figure 4 底部案例：单只被遮挡的手被错误重建为两只手）。
- **WiLoR**（Potamias et al., 2025）在 HaMeR 基础上增加手腕姿态预测，但在双手交叉且一侧严重遮挡时，仅重建可见手且错误分配左右标签（见 Figure 3 底部案例）。
- **WildHand**（Prakash et al., 2024）专为自我中心视角设计，利用辅助线索提升鲁棒性，但在双手场景下相对手腕误差（MRRPE）仍达 7.1 mm。

EgoHandICL 的关键差异在于 **推理范式变更**：不直接从图像回归，而是先获取粗估计 MANO 参数，再以检索到的模板示例对为上下文条件，通过掩码重建 Transformer 进行精炼（Eq. 3: $\mathcal{M}_{\mathrm{qry}} = \mathcal{F}(\tilde{\mathcal{M}}_{\mathrm{qry}} | \mathcal{C}_{\mathcal{M}})$）。这使模型在歧义场景下具备“参考类似案例”的推理能力，而非仅依赖单图特征。

**（2）相对于上下文学习范式的迁移**

上下文学习最初在自然语言处理中作为大语言模型的涌现能力被系统研究（Brown et al., 2020），后续被引入视觉域（如 **POTTER**（Zheng et al., 2023）用于人体 mesh 重建）。EgoHandICL 将 ICL 引入自我中心手部重建，并做了三处关键适配：
- **多模态上下文构建**：不同于纯视觉 token 拼接，EgoHandICL 的 ICL Tokenizer 融合图像、结构（MANO 参数）和文本三种模态，生成四组 ICL tokens（模板输入、模板目标、查询输入、查询目标）。
- **掩码重建训练**：基于 MAE 设计，训练时随机掩码部分目标 tokens 模拟推理时的完全未知状态，迫使模型从输入 tokens 和未掩码目标 tokens 中学习上下文依赖。
- **互补检索策略**：预定义视觉模板（基于手部参与类型分类）与自适应文本模板（基于 VLM 语义描述）双路检索，提供多角度示例先验。

**（3）与手部重建中辅助信息利用方法的对比**

部分方法利用额外模态信息（如深度、分割）提升重建精度，但 EgoHandICL 不依赖测试时的额外传感器输入，仅通过检索数据库中的模板提供“虚拟辅助信息”。这使其在纯 RGB 输入约束下获得可比甚至更优的性能。

### 2. 适用边界与局限

**适用场景**：
- 自我中心视角下的单手与双手 3D 重建，尤其是存在严重自遮挡和手-物交互的场景。
- 需要高精度顶点级重建的下游任务（如手-物交互推理，见 Figure 5 中 EgoVLM 结合 EgoHandICL 后的推理增强）。
- 可适配不同粗估计主干（Table 5 显示对 HaMeR 和 WiLoR 分别带来 +16.1% 至 +27.3% 的相对增益），具有架构灵活性。

**已知局限**（基于论文明确讨论）：
- **计算开销**：依赖 VLM 进行模板检索引入显著推理成本，难以部署在资源受限的实时设备上。
- **模板数据库依赖**：检索质量受限于模板数据库的覆盖度和多样性；在分布外场景下，检索到的模板与查询语义不匹配时，精炼效果可能下降。
- **MANO 真值缺失**：当前自我中心数据集（如 EgoExo4D）仅提供关键点级标注，缺乏完整 MANO 参数真值，限制模型在复杂场景下的泛化训练。
- **检测依赖**：现有评估均基于真实边界框，而自我中心视角下的手部检测本身极具挑战性，缺乏端到端的联合检测与重建公平评估基准。

### 3. 开放问题

论文明确指出的未来方向包括：

1. **轻量化检索**：如何设计轻量级 VLM 或检索无关的策略以降低模板检索的计算开销？
2. **任务扩展**：如何将 EgoHandICL 扩展到连续 3D 手部跟踪、手-物联合重建等更丰富的自我中心任务？
3. **数据与基准建设**：如何构建包含手部、物体和身体姿态一致标注的全面自我中心 3D 基准？
4. **分布外鲁棒性**：在检索到的模板质量下降时，如何进一步提升模型的鲁棒性？
5. **端到端框架**：能否开发不依赖真实边界框的端到端联合检测与重建框架？

### 4. 方法谱系定位总结

EgoHandICL 在方法谱系中位于 **“检索增强的上下文学习式手部重建”** 节点。其上游承接 ViT-based 手部重建方法（HaMeR, WiLoR）的粗估计能力，横向借鉴视觉上下文学习（POTTER）和掩码重建（MAE）的训练范式，下游可对接手-物交互理解（EgoVLM）等高层视觉推理任务。该节点填补了“严重遮挡下利用示例先验进行手部重建”的方法空白，但检索效率与数据标注完备性仍是制约其大规模应用的关键瓶颈。

## 原文 PDF

![[paperPDFs/ICLR_2026/EgoHandICL_Egocentric_3D_Hand_Reconstruction_with_In_Context_Learning_e95df01ae740.pdf]]