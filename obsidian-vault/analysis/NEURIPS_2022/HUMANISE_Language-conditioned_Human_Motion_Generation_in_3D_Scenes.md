---
title: "HUMANISE: Language-conditioned Human Motion Generation in 3D Scenes"
type: paper
paper_level: A
venue: NEURIPS
year: 2022
pdf_ref: "paperPDFs/NEURIPS_2022/HUMANISE:_Language-conditioned_Human_Motion_Generation_in_3D_Scenes.pdf"
project_link: https://silverster98.github.io/HUMANISE/
code_link: https://github.com/Silverster98/HUMANISE
aliases:
- SLCCGMSAFAL
- HUMANISE
tags:
- NEURIPS_2022
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过自动对齐AMASS运动数据与ScanNet场景，并基于模板生成包含动作类型和空间关系的语言描述，构建了大规模语义丰富的合成数据集HUMANISE。
primary_logic: 利用自注意力机制将场景点云特征和文本词特征融合为条件嵌入，并引入目标定位和动作分类两个辅助任务，使得cVAE生成的运动同时符合语言描述和三维场景上下文。
claims:
- HUMANISE含有19.6k个运动序列，跨越643个三维场景，远超现有数据集，且不含姿态抖动。
- 去除目标定位损失L_o后，目标距离从1.008上升到1.383；去除动作分类损失L_a后，动作得分从3.59±1.38下降到2.29±1.43。
- 模型在PROX数据集上微调后，所有评估指标均优于仅在PROX上训练的场景条件方法。
- HUMANISE (all actions) 上 goal dist. ↓ = 1.008
---

# HUMANISE: Language-conditioned Human Motion Generation in 3D Scenes

> [!tip] 核心洞察
> 利用自注意力机制将场景点云特征和文本词特征融合为条件嵌入，并引入目标定位和动作分类两个辅助任务，使得cVAE生成的运动同时符合语言描述和三维场景上下文。

| 字段 | 内容 |
|------|------|
| 中文题名 | HUMANISE：语言引导的三维场景人体运动生成 |
| 英文题名 | HUMANISE: Language-conditioned Human Motion Generation in 3D Scenes |
| 会议/期刊 | NEURIPS 2022 |
| Links | [paper](https://arxiv.org/abs/2210.09729) · [Project](https://silverster98.github.io/HUMANISE/) · [Code](https://github.com/Silverster98/HUMANISE) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Scene-and-language conditioned cVAE generative model with self-attention fusion and auxiliary losses |
| Dataset | HUMANISE |

> [!tip] 效果简介
> - HUMANISE (all actions) 上，goal dist. ↓ 1.008 vs 1.383 (w/o L_o) (-0.375)；action score ↑ 3.59±1.38 vs 2.29±1.43 (w/o L_a) (+1.30)；goal dist. ↓ 1.008 vs 1.406 (GT_action) (-0.398)。

## 概述

三维场景中的人体运动生成是构建智能虚拟角色的关键能力。现有的人-场景交互（HSI）数据集规模有限、运动质量参差不齐，且普遍缺乏语义标注，严重阻碍了语言指令感知的通用化运动学习。HUMANISE 针对这一瓶颈，提出了一个大规模、语义丰富的合成数据集，并配套设计了语言与场景双条件生成模型。

核心思路包含两个层面。**数据层面**，通过将 AMASS 运动数据与 ScanNet 三维场景自动对齐，并基于组合模板生成包含动作类型和空间关系的语言描述，构建了覆盖 643 个场景、19.6k 个运动序列的 HUMANISE 数据集，其规模和质量远超既有 HSI 数据集（见表 1）。**方法层面**，采用条件变分自编码器（cVAE）框架，以自注意力机制融合 Point Transformer 提取的场景点云特征与 BERT 提取的语言词特征，形成联合条件嵌入；同时引入目标定位和动作分类两个辅助任务，强化模型的空间语义理解能力。

实验表明，去除目标定位损失后，目标距离从 1.008 上升至 1.383；去除动作分类损失后，动作得分从 3.59±1.38 降至 2.29±1.43，验证了辅助任务的关键作用。在 PROX 数据集上微调后，模型在所有评估指标上均优于仅在 PROX 上训练的场景条件方法。模型同时支持不同时长的运动生成，展现出良好的泛化能力。

**局限与待验证点**：模型在处理多相似物体或复杂空间关系时仍会出现目标定位错误；语言描述基于固定模板生成，对自由形式指令的泛化能力需进一步验证；当前仅覆盖坐、站起、躺下、行走四类动作，且未显式建模物理碰撞，生成结果可能存在穿透或悬浮现象。

## 背景与动机

### 问题背景：语言引导的三维场景人体运动生成

在具身智能与虚拟人建模的交叉领域，使虚拟角色根据自然语言指令在三维场景中执行合理的交互动作，是构建沉浸式数字体验的关键技术。这一任务要求模型同时理解**场景的几何与语义约束**（如物体的位置、形状、可供性）以及**语言的时空语义**（如动作类型、目标物体、空间关系），并生成物理上可行、语义上一致的人体运动序列。

传统的人体运动生成研究主要分为两类：一类聚焦于**无条件或文本条件运动生成**，不考虑三维场景约束；另一类探索**场景条件运动生成**，但缺乏语言指令的引导。后者虽然能够生成与场景几何兼容的运动（例如在椅子附近生成坐姿），却无法根据用户的自然语言描述精确控制动作类型、交互对象和空间关系。

### 现有方法的瓶颈：数据匮乏与语义缺失

语言引导的场景感知运动生成面临一个根本性瓶颈：**缺乏大规模、高质量、语义丰富的三维人-场景交互（Human-Scene Interaction, HSI）数据集**。

如 Table 1 所示，现有的 HSI 数据集在规模和语义标注方面存在显著不足。以 PROX 为代表的数据集虽然提供了真实扫描场景中的人体运动，但其运动序列数量有限（通常仅数百个片段），且**缺乏与动作类型、交互对象相对应的语言描述标注**。其他数据集如 GTA-IM 和 SAMP 虽然规模稍大，但场景多样性不足或运动质量参差不齐。这些局限导致两个直接后果：

1. **无法学习语言-场景-运动的联合映射**：没有语义标注，模型无法建立从语言描述到具体场景交互行为的对应关系。
2. **泛化能力受限**：小规模数据难以覆盖多样化的场景布局和交互模式，模型容易过拟合到特定场景分布。

此外，现有数据集中的人体运动通常通过优化方法从稀疏传感器数据重建而来，普遍存在**姿态抖动、脚部滑动、物体穿透**等物理不合理现象，进一步降低了训练数据的质量。

### 本文动机与核心思路

针对上述瓶颈，本文提出**HUMANISE**——一个大规模、语义丰富的语言引导三维人-场景交互数据集，以及相应的生成模型。

**核心动机**可以概括为两个层面：

- **数据层面**：通过自动对齐 AMASS 运动捕捉数据与 ScanNet 三维场景，并基于组合模板生成包含动作类型和空间关系的语言描述，构建一个规模远超现有数据集、且天然携带精确语义标注的合成数据集。HUMANISE 包含 **19.6k 个运动序列**，跨越 **643 个室内场景**，覆盖坐、站起、躺下、行走四类核心交互动作。

- **方法层面**：设计一个**场景与语言双重条件**的生成模型，利用条件变分自编码器（cVAE）框架，通过自注意力机制融合场景点云特征与文本词特征，并引入**目标定位**和**动作分类**两个辅助任务，显式增强模型的空间感知与语义理解能力，使生成的运动同时符合语言描述和三维场景上下文。

这种“数据-模型协同设计”的策略，使得模型不仅能够从大规模语义数据中学习丰富的交互模式，还能通过辅助任务获得可解释的空间与动作感知能力，为语言引导的三维人体运动生成建立了新的基准。

## 核心创新

HUMANISE 的核心创新在于将语言条件显式引入三维场景中的人体运动生成，并通过**多模态自注意力融合**与**双辅助任务**解决了“语言-场景-运动”三者对齐的瓶颈。其相对现有工作的关键改变槽位（changed slots）体现在以下三个层面。

### 1. 多模态特征融合：从拼接走向自注意力

现有方法通常将场景特征与条件特征简单拼接后送入解码器。HUMANISE 提出使用**单层自注意力模块**（single-layer self-attention）对场景点云特征和语言词特征进行联合建模：

- **场景编码器**（Point Transformer）输出点级特征 $\{f_{p_i}\}_{i=1}^{N_p}$；
- **语言编码器**（预训练 BERT）输出词级嵌入 $\{f_{w_j}\}_{j=1}^{D}$；
- 两者拼接后送入自注意力层，使每个 token 能够跨模态地关注点云和文本信息，最终以 `[CLS]` token 的输出作为联合条件嵌入 $z_c$。

消融实验表明，移除自注意力融合（`w/o self-att`）会导致运动多样性（APD）和重建精度同时下降（Tab. 2），证实了跨模态交互建模对生成质量的关键作用。

### 2. 训练目标：引入目标定位与动作分类辅助损失

传统 cVAE 仅依赖重建损失与 KL 散度。HUMANISE 在条件嵌入 $z_c$ 之上额外施加两个辅助任务，形成总损失：

$$\mathcal{L} = \mathcal{L}_{rec} + \alpha_{kl} \mathcal{L}_{kl} + \alpha_{o} \mathcal{L}_{o} + \alpha_{a} \mathcal{L}_{a}$$

- **目标定位损失** $\mathcal{L}_{o}$：通过全连接层从 $z_c$ 回归目标交互物体的三维中心坐标，使用 MSE 损失；
- **动作分类损失** $\mathcal{L}_{a}$：通过全连接层从 $z_c$ 预测动作类别，使用交叉熵损失。

这两项辅助损失迫使条件嵌入显式编码“与哪个物体交互”和“执行什么动作”的语义信息。消融证据极为明确：

| 消融条件 | goal dist. ↓ | action score ↑ |
|----------|-------------|----------------|
| 完整模型 | **1.008** | **3.59 ± 1.38** |
| w/o $\mathcal{L}_{o}$ | 1.383 | — |
| w/o $\mathcal{L}_{a}$ | — | 2.29 ± 1.43 |

去除 $\mathcal{L}_{o}$ 后目标距离恶化 37%，去除 $\mathcal{L}_{a}$ 后动作得分下降 1.30 分。完全去除辅助损失（`w/o aux. loss`）时，模型甚至无法生成正确动作或定位到正确交互对象（Fig. 5），生成质量得分显著降低。这构成该工作最决定性的因果证据。

### 3. 场景编码器架构：PointNet++ → Point Transformer

HUMANISE 将场景编码器从 PointNet++ 升级为 **Point Transformer**（Zhao et al., 2021），以获取更强的点云表征能力。消融实验（`PointNet++ Enc.`）表明，替换回 PointNet++ 会导致重建与生成指标下降，验证了更强的点云编码器对场景理解的重要性。

### 创新总结

三个改变槽位形成递进关系：更强的场景编码器提供更丰富的几何特征，自注意力融合实现语言与场景的细粒度对齐，双辅助损失则从目标定位和动作语义两个维度约束条件嵌入，最终使 cVAE 生成的运动同时符合语言描述和三维场景上下文。这一设计无需依赖真实动作类别或目标中心作为中间监督，实现了端到端的语言条件运动生成。

## 整体框架

HUMANISE 采用 **条件变分自编码器（cVAE）** 框架，以三维场景点云和语言描述为条件，生成符合场景上下文的人体运动序列。整体 pipeline 由四个核心阶段构成：**条件编码、运动编码、潜在空间采样与运动解码**，并通过两个辅助任务增强条件嵌入的语义与空间理解能力。

### 输入输出流

- **输入**：三维场景的彩色点云 $S$ 和自然语言描述 $L$（由模板自动生成，格式为 $\langle \text{action} \rangle \langle \text{target-class} \rangle \bigl[ \langle \text{spatial-relation} \rangle \langle \text{anchor-class(es)} \rangle \bigr]$）。
- **输出**：一段时长为 $T$ 的人体运动参数序列 $\widehat{\Theta}_{1:T}$，包含全局平移、全局旋转、关节旋转等参数，可驱动 SMPL-X 人体模型生成最终网格。

### 模块关系与数据流

1. **场景编码器（Point Transformer）** 从场景点云中提取逐点几何与颜色特征，输出点级特征表示。
2. **语言编码器（预训练 BERT）** 将分词后的语言描述编码为词级嵌入。
3. **跨模态自注意力融合模块** 将点级特征与词级特征拼接后，送入单层自注意力层，生成融合的条件嵌入 $z_c$。该嵌入同时捕捉场景几何信息与语言语义信息。
4. **运动编码器（双向 GRU）** 将输入运动序列压缩为潜在表示，与条件嵌入共同参数化潜在空间的后验分布。
5. **潜在空间采样** 从后验分布中采样潜在变量 $z$，与条件嵌入 $z_c$ 拼接后送入解码器。
6. **运动解码器（Transformer Decoder）** 以条件嵌入和潜在变量为输入，自回归地生成指定时长的运动参数序列。

### 辅助任务增强条件嵌入

为强化模型对语言中动作语义和空间关系的理解，pipeline 在条件嵌入 $z_c$ 之上引入两个辅助预测头：

- **目标定位头**：通过全连接层回归交互目标物体的三维中心坐标，采用 MSE 损失 $\mathcal{L}_o$ 监督。
- **动作分类头**：通过全连接层对动作类别进行分类，采用交叉熵损失 $\mathcal{L}_a$ 监督。

这两个辅助任务仅在训练时使用，不增加推理时的计算开销，但其监督信号显著提升了条件嵌入的质量。

### 训练目标

总损失函数为多任务联合优化：

$$\mathcal{L} = \mathcal{L}_{rec} + \alpha_{kl} \mathcal{L}_{kl} + \alpha_{o} \mathcal{L}_{o} + \alpha_{a} \mathcal{L}_{a}$$

其中重建损失 $\mathcal{L}_{rec}$ 由全局平移、全局旋转、关节旋转和顶点位置的 L1 距离加权求和构成：

$$\mathcal{L}_{rec} = \mathcal{L}_{t} + \alpha_{r} \mathcal{L}_{r} + \alpha_{p} \mathcal{L}_{p} + \alpha_{v} \mathcal{L}_{v}$$

$\mathcal{L}_{kl}$ 为 KL 散度，约束潜在空间分布接近标准正态分布。

### 与多阶段流水线的对比

论文还探索了多阶段流水线（GT_action 与 GT_action+target），即先预测动作类别或目标中心，再以此为条件生成运动。附录 **Table A3** 显示，端到端联合学习的方式在目标距离（goal dist.）上优于使用真实动作类别和预测目标中心的多阶段方案（1.008 vs. 1.406），验证了联合优化的优势。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/004_Figure_3.jpg]]
*Figure 3: Illustration of the proposed generative model. It adopts the cVAE framework and incorporates a motion encoder and decoder to generate human motions. The condition is learned from the joint embedding of the 3D scene and language description with auxiliary tasks of 3D location grounding and action recognition*

## 核心模块与公式推导

### 整体框架：条件变分自编码器

HUMANISE 采用条件变分自编码器（cVAE）框架，建模给定三维场景 $S$ 和语言描述 $\bar{L}_{1:D}$ 下人体运动序列 $\bar{\Theta}_{1:T}$ 的条件概率分布。整个生成管线由七个核心模块串联而成：场景编码器、语言编码器、跨模态自注意力融合模块、运动编码器、运动解码器、辅助目标定位头、辅助动作分类头。

### 场景编码器：Point Transformer

三维场景以带颜色的点云形式输入，采用 **Point Transformer**（Zhao et al., 2021 原架构）提取逐点几何-外观特征。消融实验表明，将其替换为 PointNet++ 会导致重建精度和生成质量下降，验证了 Transformer 结构在捕获长程空间依赖上的优势。

### 语言编码器：预训练 BERT

语言描述 $L$ 经过分词后，送入预训练 **BERT** 模型，提取词级嵌入序列。该嵌入保留了每个 token 的上下文语义信息，为后续与场景点特征的细粒度对齐提供基础。

### 跨模态融合：单层自注意力

场景编码器输出的点级特征与语言编码器输出的词级特征被拼接后，送入一个**单层自注意力模块**进行融合，生成联合条件嵌入。该设计替代了简单的拼接融合（w/o self-att），消融实验显示：移除自注意力会降低运动多样性指标 APD 和重建精度，说明注意力机制能有效建模点-词之间的跨模态对应关系。

### 运动编码器与解码器

运动编码器采用**双向 GRU**，将输入运动序列压缩为序列级隐变量。运动解码器采用 **Transformer Decoder**，以采样的隐变量和条件嵌入为输入，自回归地生成指定时长 $T$ 的身体参数序列 $\widehat{\Theta}_{1:T}$（包括全局平移、全局旋转、关节旋转等）。

### 训练损失函数

总训练损失由四项加权组成：

$$\mathcal{L} = \mathcal{L}_{rec} + \alpha_{kl} \mathcal{L}_{kl} + \alpha_{o} \mathcal{L}_{o} + \alpha_{a} \mathcal{L}_{a}$$

其中 $\mathcal{L}_{kl}$ 为隐变量分布与先验分布之间的 KL 散度。重建损失 $\mathcal{L}_{rec}$ 进一步分解为四个分量的 L1 距离加权和：

$$\mathcal{L}_{rec} = \mathcal{L}_{t} + \alpha_{r} \mathcal{L}_{r} + \alpha_{p} \mathcal{L}_{p} + \alpha_{v} \mathcal{L}_{v}$$

各分量含义：
- $\mathcal{L}_{t}$：全局平移的 L1 损失
- $\mathcal{L}_{r}$：全局旋转的 L1 损失
- $\mathcal{L}_{p}$：关节旋转的 L1 损失
- $\mathcal{L}_{v}$：顶点位置的 L1 损失

### 辅助任务设计

为增强模型的空间定位和动作语义理解能力，在条件嵌入之上引入两个辅助任务：

- **目标定位损失 $\mathcal{L}_{o}$**：通过一个全连接层从条件嵌入回归交互目标物体的三维中心坐标，使用 MSE 损失监督。该损失直接驱动模型学习“人在场景中与哪个物体交互”的空间对应关系。

- **动作分类损失 $\mathcal{L}_{a}$**：通过另一个全连接层从条件嵌入预测动作类别，使用交叉熵损失监督。该损失强制条件嵌入保留足够的动作语义信息，确保生成的运动类型与语言描述一致。

消融实验提供了因果证据：去除 $\mathcal{L}_{o}$ 后，目标距离从 1.008 上升至 1.383；去除 $\mathcal{L}_{a}$ 后，动作得分从 3.59±1.38 降至 2.29±1.43。完全去除所有辅助损失（w/o aux. loss）则导致模型无法生成正确动作或定位到正确交互对象，生成质量得分显著降低。

## 实验与分析

### 主实验结果

模型在HUMANISE数据集上进行了全面的定量评估。Table 2展示了分动作模型（action-specific）的重建与生成指标。

在重建精度方面，模型在全局平移（translation）、全局旋转（rotation）、关节姿态（joint rotation）以及MPJPE和MPVPE等指标上均取得了较低的误差。生成质量方面，各动作类别在用户调研中获得了较高的质量评分：行走（walk）为2.91±1.27，坐下（sit）为2.37±0.85，站起（stand up）为2.83±1.23。

目标定位指标（goal distance）是衡量生成运动与目标交互物体之间空间关系准确性的关键指标。完整模型在全部动作上取得了1.008的目标距离，表明生成的人体与目标物体保持了合理的交互距离。

### 消融实验

消融实验系统性地验证了各模块的贡献（Table 2, Fig. 5）。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/006_Table_2.jpg]]
*Table 2: Quantitative results of reconstruction and generation on HUMANISE dataset*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/007_Figure_5.jpg]]
*Figure 5: Ablation results of action-agnostic models. For the description sit on the coffee table, the model w/o aux. loss struggles in (b) generating the action specified by the description or (c) locating the interacting object. (d) In comparison, our full model generates motions semantically consistent with the language description*

**辅助损失的作用**：去除目标定位损失 $L_o$ 后，目标距离从1.008显著上升至1.383，说明该损失对精确目标定位至关重要。去除动作分类损失 $L_a$ 后，动作得分从3.59±1.38大幅下降至2.29±1.43，表明该损失有助于生成与语言描述一致的动作类型。完全去除辅助损失（w/o aux. loss）导致模型无法生成正确动作或定位到正确交互对象，生成质量得分显著降低（Fig. 5）。

**多模态融合方式**：移除自注意力融合模块（w/o self-att），改用简单拼接方式，导致运动多样性（APD）和重建精度均有所下降，验证了自注意力机制在跨模态特征融合中的有效性。

**场景编码器选择**：将Point Transformer替换为PointNet++编码器（PointNet++ Enc.）后，各项指标均出现退化，表明更强的点云特征提取能力对场景理解至关重要。

**端到端 vs. 多阶段流水线**：与使用真实动作类别和/或预测目标中心的多阶段基线（GT_action、GT_action+target）相比，端到端模型在目标距离上表现更优（1.008 vs. 1.406），验证了联合优化的优势（Table A3）。

### 下游任务迁移

在PROX数据集上的微调实验（Table 3）表明，使用HUMANISE预训练的模型在所有评估指标上均优于仅在PROX上训练的场景条件方法（Wang et al., 2021a），证明了大规模语义标注数据对提升模型泛化能力的价值。

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/009_Table_3.jpg]]
*Table 3: Results of human motion synthesis on PROX dataset*

### 失败模式分析

尽管模型在多数场景下表现良好，但仍存在以下典型失败模式：

1. **目标定位错误**：当场景中存在多个相似物体时（如多张桌子、多把椅子），模型可能选择错误的交互目标。这在包含复杂空间关系描述（如“靠近门的桌子”）时尤为突出。

2. **人-物交互关系错误**：生成的运动可能在语义上正确但在物理接触上不正确，例如坐姿动作中人体接触了错误的物体表面。

3. **物理合理性不足**：由于模型未显式建模物理碰撞约束，生成的运动偶尔会出现穿透物体或悬浮等物理不合理现象。

4. **动作类别局限**：当前数据集仅覆盖坐、站起、躺下、行走四类动作，模型对未见过动作类型的泛化能力尚未验证。

需要人工核实的是，上述失败案例的具体比例和分布情况在论文中未提供系统性的统计分析。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/003_Table_1.jpg]]
*Table 1: Comparison between HUMANISE and existing HSI datasets*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative generation results of action-specific models on the HUMANISE dataset. We visualize one reference motion and three generation motions for each scenario. The attention map visualizes the attention weights the [CLS] token attended to the scene point cloud in the self-attention layer. Red denotes higher weight*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/008_Figure_6.jpg]]
*Figure 6: Motions generated by sampling with different duration T . The language descriptions in these two cases are walk to the end table that is farthest from the door and sit on the coffee table. Our model is capable of generating motions with various duration*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/017_Table.jpg]]
*Table: A3: Comparison between multi-stage pipeline and end-to-end pipeline*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/016_Table.jpg]]
*Table: Figure A7: Failure case with incorrect HOI relation . The language description, in this case, is sit on the table that is close to the door. Table A2: Ablations about lie down action*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/011_Table.jpg]]
*Table: A1: Comparison between HUAMNISE and existing HSI datasets*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/014_Figure.jpg]]
*Figure: A4: Qualitative reconstruction results of the action-specific models*

![[assets/figures/papers/paper_list_l12_https_arxiv_org_abs_2210_09729/figures/012_Figure.jpg]]
*Figure: A2: Motions aligned with scenes in Replica [Straub et al., 2019]*

## 方法谱系与知识库定位

### 1. 问题定义与基线对比

HUMANISE 解决的核心问题是**语言引导的三维场景人体运动生成**（Language-conditioned Human Motion Generation in 3D Scenes）。该任务要求模型同时理解三维场景的几何语义和自然语言指令，生成符合场景约束和动作描述的 SMPL-X 参数序列。

在 HUMANISE 提出之前，该领域的基线方法存在明确的能力边界：

- **场景条件运动生成**：以 **Wang et al. (2021a)** 为代表的方法仅将三维场景作为条件输入，缺乏语言指令的语义引导，无法根据文本描述指定交互目标和动作类型。这类方法的适用边界限于“给定场景，生成合理运动”，但无法响应“坐在咖啡桌旁”这类细粒度指令。

- **纯语言条件运动生成**：基于文本生成人体运动的方法（如 Action2Motion、TEMOS 等）不考虑三维场景约束，生成的运动在物理空间上可能与场景产生穿透或悬浮。其适用边界限于无场景上下文的自由空间运动。

- **现有 HSI 数据集**：PROX、GTA-IM 等数据集虽然提供了人-场景交互的运动数据，但存在规模有限、场景多样性不足、缺乏语义标注等问题（见 Table 1）。这导致基于这些数据集训练的方法难以泛化到新场景和新指令。

HUMANISE 的方法定位是**将场景条件和语言条件统一到同一生成框架中**，并通过大规模语义丰富的合成数据集弥补数据瓶颈。其方法谱系可归纳为：*cVAE 生成框架 + 多模态自注意力融合 + 辅助空间/语义对齐任务*。

### 2. 核心方法模块与消融基线的关系

论文通过系统的消融实验建立了各方法模块的因果贡献。以下将各消融基线与其对应的设计选择进行对照分析：

| 消融基线 | 对应移除的模块 | 核心影响 | 证据强度 |
|---------|--------------|---------|---------|
| **w/o Lₒ** | 目标定位辅助损失 | goal dist. 从 1.008 上升至 1.383，目标定位能力显著退化 | 强（Tab. 2） |
| **w/o Lₐ** | 动作分类辅助损失 | action score 从 3.59±1.38 降至 2.29±1.43，动作语义一致性下降 | 强（Tab. 2） |
| **w/o aux. loss** | 同时移除 Lₒ 和 Lₐ | 模型无法生成正确动作或定位到正确交互对象，生成质量得分显著降低 | 强（Fig. 5, Tab. 2） |
| **w/o self-att** | 自注意力融合模块（退化为简单拼接） | 运动多样性（APD）和重建精度均下降 | 中（Tab. 2） |
| **PointNet++ Enc.** | 场景编码器从 Point Transformer 替换为 PointNet++ | 场景特征提取能力下降，影响条件嵌入质量 | 中（Tab. 2） |

从方法谱系角度看，这些消融实验揭示了三个关键机制：

1. **辅助任务作为隐式正则化**：Lₒ 和 Lₐ 并非仅在推理时使用，而是通过训练过程中的梯度信号，迫使条件嵌入 z_c 学习到空间定位和动作语义的可分离表征。移除这些损失后，条件嵌入退化为缺乏结构化语义的通用向量，导致生成质量全面下降。

2. **自注意力融合的必要性**：简单的拼接融合无法建模场景点云特征与文本词特征之间的跨模态对齐关系。单层自注意力机制通过学习点-词之间的注意力权重，隐式地实现了“哪些场景区域与哪些描述词相关”的软对齐，这是模型能够根据空间关系描述（如“离门最远的边桌”）定位目标物体的关键。

3. **Point Transformer 的场景编码优势**：相比 PointNet++，Point Transformer 通过自注意力机制捕捉点云中的长程依赖关系，这对于理解室内场景中物体之间的空间布局（如“桌子旁边的椅子”）至关重要。

### 3. 多阶段流水线与端到端方法的对比

论文在附录 Table A3 中对比了端到端方法与多阶段流水线：

- **GT_action**：使用真实动作类别和预测的目标中心作为条件，分阶段生成运动。其 goal dist. 为 1.406，显著劣于端到端方法的 1.008。
- **GT_action+target**：同时使用真实动作类别和真实目标中心，性能接近端到端方法但需要额外的标注信息。

这一对比表明，端到端的联合训练不仅简化了流水线，还通过共享条件嵌入实现了更好的空间-语义对齐。多阶段方法存在误差累积问题：目标预测阶段的误差会传播到运动生成阶段。

### 4. 适用边界与局限

HUMANISE 的方法存在明确的适用边界，这些边界定义了其方法谱系中的位置：

**动作类型边界**：数据集仅覆盖四种室内动作（sit, stand-up, lie-down, walk）。对于更复杂的交互动作（如“拿起杯子”、“打开抽屉”），模型无法生成。这限制了其在细粒度手-物交互场景中的适用性。

**时序边界**：运动序列时长为 30-120 帧（约 1-4 秒），无法处理长时间、多步骤的交互序列（如“走到沙发旁，坐下，然后站起来走向门口”）。

**语言理解边界**：语言描述基于固定模板生成，形式为 `⟨action⟩ ⟨target-class⟩ [⟨spatial-relation⟩ ⟨anchor-class(es)⟩]`。对于自由形式的自然语言指令（如“找个地方坐坐”），模型的泛化能力未经验证。

**物理合理性边界**：模型未显式建模物理碰撞约束，生成的运动可能存在人体与场景的穿透或悬浮现象。这是 cVAE 生成框架的固有局限——重建损失和 KL 散度无法完全保证物理合理性。

**目标定位失败模式**：当场景中存在多个同类物体（如多把椅子）或空间关系描述复杂时，模型偶尔会定位到错误的交互对象。这是自注意力融合模块的软对齐机制在歧义场景下的固有失效模式。

### 5. 下游迁移与泛化能力

在 PROX 数据集上的微调实验（Table 3）表明，HUMANISE 预训练模型在下游真实扫描场景中优于仅在 PROX 上训练的场景条件方法。这说明：

- HUMANISE 的大规模合成数据提供了有效的预训练信号，使模型学习到了可迁移的场景-运动先验。
- 但该迁移能力依赖于目标场景的语义标注（物体分割），这限制了其在完全无标注的真实扫描场景中的直接应用。

### 6. 开放问题与后续方向

基于上述分析，HUMANISE 在方法谱系中留下的开放问题包括：

1. **长时序交互生成**：如何扩展框架以支持多步骤、长时序的人-场景交互序列？这可能需要引入层次化生成结构或时序分割策略。

2. **复杂空间关系理解**：当前的自注意力融合机制在处理“离门最远的边桌”这类复杂空间关系时仍存在失败案例。如何增强三维场景中的语言基础能力，以精确理解多样化的空间关系描述？

3. **物理仿真集成**：能否将生成模型与物理仿真器（如 SAPIEN、Isaac Gym）相结合，在生成过程中引入物理约束以确保运动在物理上完全合理？这需要在生成框架中引入可微分的物理损失或后处理优化步骤。

4. **无标注场景泛化**：如何将模型直接应用于真实扫描场景，而无需依赖人工标注的场景分割？这可能需要结合三维视觉基础模型（如 3D-LLM）实现自动场景理解。

5. **自然语言泛化**：如何突破模板化描述的局限，使模型能够理解自由形式的自然语言指令？这需要构建包含多样化语言描述的数据集，或利用大语言模型进行描述增强。

## 原文 PDF

![[paperPDFs/NEURIPS_2022/HUMANISE:_Language-conditioned_Human_Motion_Generation_in_3D_Scenes.pdf]]
