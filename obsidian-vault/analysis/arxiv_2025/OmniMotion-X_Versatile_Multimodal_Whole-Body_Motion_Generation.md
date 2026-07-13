---
title: "OmniMotion-X: Versatile Multimodal Whole-Body Motion Generation"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: "paperPDFs/arxiv_2025/OmniMotion-X:_Versatile_Multimodal_Whole-Body_Motion_Generation.pdf"
project_link: null
code_link: https://github.com/GuoweiXu368/OmniMotion-X
aliases:
- OX
- OmniMotion-X
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过将多模态条件统一为序列前缀，并采用渐进式从弱到强的混合条件训练策略，逐步从高层语义过渡到稠密时空约束；同时创新性地引入参考运动条件来强化内容一致性与风格。
primary_logic: 多模态条件应作为统一的前缀上下文进行深度融合，由粗到细的渐进训练能够有效解决不同粒度约束之间的优化冲突，使模型同时获得语义理解、风格保持和精细控制能力。
claims:
- 统一的多模态条件前缀连接克服了独立建模的冲突，实现了条件下的一致性生成。
- 渐进式从弱到强的训练策略大幅提升了文本语义对齐和时空控制的精确度。
- 引入参考运动条件显著改善了生成运动的内容、风格和时间动态一致性。
- OmniMoCap-X Text-to-Motion 上 FID↓ = 5.040
---

# OmniMotion-X: Versatile Multimodal Whole-Body Motion Generation

> [!tip] 核心洞察
> 多模态条件应作为统一的前缀上下文进行深度融合，由粗到细的渐进训练能够有效解决不同粒度约束之间的优化冲突，使模型同时获得语义理解、风格保持和精细控制能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | OmniMotion-X：多功能多模态全身运动生成 |
| 英文题名 | OmniMotion-X: Versatile Multimodal Whole-Body Motion Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2510.19789) · [Code](https://github.com/GuoweiXu368/OmniMotion-X) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | OmniMotion-X |
| Dataset | OmniMoCap-X Text-to-Motion, OmniMoCap-X Global Spatiotemporal Control |

> [!tip] 效果简介
> - OmniMoCap-X Text-to-Motion 上，FID↓ 5.040 vs 17.428 (MoMask*) (-71.1%)；R Precision Top-1↑ 0.303 vs 0.267 (MoMask*) (+13.5%)。
> - OmniMoCap-X Global Spatiotemporal Control 上，FID↓ 4.224 vs 10.247 (Ours w/o progressive training) (-58.8%)。

## 概要

### 问题瓶颈

现有全身人体运动生成方法普遍采用**任务特定架构**或**独立控制分支**来处理多模态条件（文本、语音、音乐、轨迹等），导致三个核心瓶颈：**训练冲突**——不同模态的独立建模在联合优化时产生梯度干扰；**控制粒度失配**——高层语义约束与稠密时空约束难以在同一框架内协调；**数据匮乏**——缺乏高质量、统一标注的大规模多模态全身运动数据集。这些问题严重制约了模型的通用性和生成质量。

### 核心思路

OmniMotion-X 提出了一种**统一的多模态全身运动生成框架**，其核心洞察在于：多模态条件应作为**统一的前缀上下文**进行深度融合，而非分散的独立信号。具体而言，该方法将所有模态条件（文本、全局运动、语音、音乐、参考运动）编码后拼接为序列前缀，送入**扩散变压器（DiT）**主干进行联合去噪预测。为化解不同粒度约束的优化冲突，框架采用**渐进式从弱到强的混合条件训练策略**：先建立文本语义与运动的对齐，再逐步引入参考运动、全局轨迹等强时空约束信号。此外，**参考运动条件**的引入是该方法的关键创新——通过将参考运动作为一种特殊条件信号，显著增强了自回归生成过程中的内容一致性、风格保持和时间动态连贯性。

### 方法定位

在方法谱系上，OmniMotion-X 属于**自回归运动扩散模型**，但区别于现有的多模态基线方法：

- 相比于 **MDM**（Tevet et al., 2022）等纯文本驱动扩散模型，OmniMotion-X 原生支持文本、语音、音乐、轨迹和参考运动等多模态条件联合输入。
- 相比于 **MCM**（Ling et al., 2023）、**LMM**（Zhang et al., 2024）和 **MotionCraft**（Bian et al., 2024）等采用独立分支或后融合策略的多模态方法，OmniMotion-X 通过统一前缀连接实现了条件的深度融合，避免了独立建模带来的冲突。
- 相比于 **MoMask**（Guo et al., 2024）、**MotionGPT**（Jiang et al., 2024）等基于离散 token 的自回归方法，OmniMotion-X 在连续运动空间中进行扩散去噪，并引入参考运动条件来强化自回归生成的长程一致性。

### 主要结果

在统一构建的 **OmniMoCap-X** 数据集（包含约 286.2 小时、6430 万帧的高质量全身运动数据）上进行评估，OmniMotion-X 取得了显著领先：

- **文本到运动生成**：FID 达到 **5.040**，相比最优基线 MoMask* 的 17.428 降低 **71.1%**；R Precision Top-1 达到 0.303，提升 **13.5%**。
- **全局时空可控生成**：FID 达到 **4.224**，相比移除渐进训练策略的变体（10.247）降低 **58.8%**，验证了渐进训练策略的关键作用。

消融实验进一步证实：移除渐进训练策略后，文本到运动任务的 FID 从 5.040 升至 9.574，全局时空控制任务的 FID 从 4.224 升至 10.247；仅使用参考运动条件时，FID 仍保持较低水平（7.824），证明了参考运动条件的独立有效性。

### 局限与开放问题

当前框架尚未深度融合**场景、物体及人类交互**等多层次约束，对于复杂的交互式全身运动生成仍存在局限。此外，运动表示与推理速度仍有优化空间，面向实时应用需要更紧凑的表示和更高效的推理架构。后续研究方向包括：如何将场景和交互约束集成到统一条件框架中，以及如何开发更紧凑的运动表示以加速扩散模型的推理过程。



### 问题背景

人体运动生成旨在根据多种模态的输入信号合成自然、逼真的三维人体运动序列，其应用涵盖动画制作、虚拟现实、游戏开发和人机交互等领域。随着扩散模型和自回归架构的快速发展，该领域已从单一的文本到运动生成逐步扩展到支持语音、音乐、轨迹等多种条件模态的多任务生成范式。

然而，现有方法在实际部署中面临三个核心瓶颈：

1. **多模态条件训练冲突**：大多数方法采用任务特定架构或独立控制分支来处理不同模态的条件信号，导致多模态联合训练时出现优化冲突，模型难以同时兼顾语义理解、风格保持和精细时空控制。
2. **控制粒度不匹配**：高层语义条件（如文本描述）与稠密时空约束（如关键点轨迹）在信息密度和约束强度上存在巨大差异，现有单阶段混合训练策略难以有效协调不同粒度的条件信号。
3. **数据规模与质量不足**：缺乏大规模、高质量、统一标注的多模态全身运动数据集，限制了通用运动生成模型的训练和评估。

### 现有方法缺口

表1系统对比了OmniMotion-X与现有代表性方法的差异。从任务覆盖角度看，**MDM**（Tevet et al., 2022）、**MoMask**（Guo et al., 2024）等方法仅支持文本到运动的单一任务；**MCM**（Ling et al., 2023）、**LMM**（Zhang et al., 2024）等方法虽扩展了条件模态，但仍未实现全局时空可控生成与参考运动条件的统一。从数据规模看，现有合并数据集如HumanML3D、KIT-ML等在运动时长和帧数上远小于OmniMoCap-X（286.2小时，64.3M帧），且缺乏对语音、音乐等多模态任务的系统性覆盖。

在架构层面，现有方法多采用独立的条件编码分支或将不同模态交由不同模型处理，这种“分而治之”的策略虽然简化了设计，但牺牲了多模态条件之间的信息交互与互补潜力。具体而言：
- 独立建模导致不同条件信号在特征空间中缺乏统一的对齐机制，难以实现跨模态的一致性生成；
- 单阶段混合训练使模型在同时面对弱条件（文本）和强条件（轨迹）时，容易偏向拟合强约束而忽略语义对齐，产生“控制精确但语义偏离”的生成结果。

### 本文动机

针对上述瓶颈，本文提出OmniMotion-X，一个统一的多模态全身运动生成框架，其设计动机源于以下核心洞察：

**多模态条件应作为统一的前缀上下文进行深度融合**。不同于独立建模，OmniMotion-X采用扩散变压器（DiT）架构，将文本、全局运动、语音、音乐和参考运动等多种条件通过模态特定编码器提取特征后，投影并对齐为统一的条件前缀，与噪声运动序列拼接后送入DiT主干进行去噪预测。这种设计使不同模态的条件信号能够在统一的注意力机制下交互，克服了独立建模带来的优化冲突。

**由粗到细的渐进训练能够有效解决不同粒度约束之间的优化冲突**。OmniMotion-X提出从弱到强的渐进式混合条件训练策略：先以文本条件建立运动-语义对齐基础，再逐步引入参考运动、全局运动、语音、音乐等更强的条件信号。这种课程式训练使模型先掌握高层语义理解能力，再逐步习得精细时空控制能力，避免了单阶段训练中的冲突与退化。

**引入参考运动条件可显著增强生成内容的一致性**。在自回归逐段生成过程中，OmniMotion-X将前序生成的运动片段作为参考运动条件输入到当前片段的生成中，从而在内容、风格和时间动态上保持长程一致性，有效缓解了逐段生成常见的片段间不连贯问题。

此外，为支撑上述方法的训练与评估，本文构建了OmniMoCap-X数据集——目前最大的多模态运动捕捉数据集，整合28个公开高质量数据集，统一转换为SMPL-X格式，并配备了高质量的多模态标注。



## 核心方法与创新机理

OmniMotion-X 的核心创新并非单一技术点的堆砌，而是通过**统一条件前缀连接**、**渐进式从弱到强训练**和**参考运动条件**三个相互耦合的机制，系统性地解决了多模态全身运动生成中长期存在的条件冲突与控制粒度不匹配问题。

### 1. 统一多模态条件前缀连接

现有方法通常为不同模态设计独立的控制分支或任务特定架构（如 **MDM** 仅支持文本、**MCM** 与 **MotionCraft** 采用分离式条件注入），导致多条件联合训练时产生优化冲突，且难以扩展到新的条件组合。OmniMotion-X 将这一范式彻底统一：所有条件模态——文本 $\mathbf{c}_t$、全局运动 $\mathbf{c}_g$、语音 $\mathbf{c}_s$、音乐 $\mathbf{c}_m$ 和参考运动 $\mathbf{c}_r$——首先通过各自的模态特定编码器（如 T5-XXL 用于文本、wav encoder 用于语音、Librosa 用于音乐、body-wise encoding 用于运动）提取特征，再经投影层对齐维度后，直接拼接为扩散变压器（DiT）的条件前缀上下文：

$$c = [ h_t(f_t(c_t)), h_g(f_g(c_g)), h_s(f_s(c_s)), h_m(f_m(c_m)), h_r(f_r(c_r)) ]$$

这一设计的关键在于：条件不再是外挂的控制信号，而是作为序列前缀与噪声运动 token 一同进入 DiT 的注意力计算，使模型能够在前向传播中动态地融合不同粒度的语义与时空约束。配合 $x_0$-prediction 扩散损失 $L_{\mathrm{simple}} = \mathbb{E}_{x_0 \sim q(x_0|c), t \sim [1,T]} [ || x_0 - G(x_t, t, c) ||_2^2 ]$，模型直接预测原始运动而非噪声，进一步强化了条件与运动之间的映射精度。

### 2. 渐进式从弱到强的混合条件训练

仅靠统一前缀连接并不足以解决不同条件粒度间的优化冲突——文本提供高层语义，而全局轨迹或语音节奏则要求稠密的时空对齐。OmniMotion-X 提出的**渐进式从弱到强训练策略**（Figure 3）正是针对这一瓶颈：训练初期仅使用文本条件建立运动-语义对齐，随后逐步引入参考运动、全局运动、语音和音乐等更强的时空约束信号。这种由粗到细的课程式训练，使得模型先在宽松的语义空间中收敛，再逐层适应更严格的时空限制，避免了单阶段混合训练中不同粒度约束相互干扰的问题。

消融实验（Table 7）为这一策略提供了直接证据：移除渐进训练后，文本到运动任务的 FID 从 5.040 恶化至 9.574，全局时空控制任务的 FID 从 4.224 恶化至 10.247，降幅分别达 89.9% 和 142.6%，充分说明渐进训练是模型同时获得语义理解与精细控制能力的决定性因素。

### 3. 参考运动条件

OmniMotion-X 引入了一种全新的条件范式——**参考运动**。与传统的文本或轨迹条件不同，参考运动直接提供了一段示例运动片段作为风格、内容和时间动态的蓝本。在自回归逐段生成过程中，参考运动作为特殊条件注入，显著增强了跨片段的内容一致性与风格保持能力。这一机制尤其适用于需要长序列生成或风格迁移的场景，填补了现有方法仅依赖抽象语义条件而缺乏具体运动参照的空白。

消融实验中，仅使用参考运动而不使用其他多模态条件时，FID 仍保持 7.824 的较低水平（Table 7），验证了参考运动条件本身即具备强大的生成引导能力。当与文本条件联合使用时（Ours+RM），R Precision Top-1 进一步提升至 0.346，FID 降至 3.199，表明参考运动与语义条件之间存在互补增益。

### 创新耦合效应

上述三个 changed slot 并非孤立存在：统一前缀连接为多条件融合提供了架构基础，渐进训练策略确保了不同粒度条件的有序学习，而参考运动则拓展了条件空间的上限。三者共同作用，使得 OmniMotion-X 在单一框架内同时支持文本到运动、语音到手势、音乐到舞蹈、轨迹引导合成、运动插值与预测等多种任务，且在各任务上均取得最优或次优的定量结果（Table 4、Table 5）。



### 设计动机与核心思路

现有全身运动生成方法普遍采用任务特定架构或独立控制分支，导致多模态条件训练冲突、控制粒度不匹配，且缺乏高质量的统一多模态全身运动数据集。OmniMotion-X 的核心洞察在于：**多模态条件应作为统一的前缀上下文进行深度融合，而非独立建模**；同时，由粗到细的渐进训练能够有效解决不同粒度约束之间的优化冲突，使模型同时获得语义理解、风格保持和精细控制能力。

### 统一序列到序列自回归扩散框架

OmniMotion-X 的整体架构如图 Figure 2 所示，采用**统一的多模态自回归 Transformer 扩散模型**，以序列到序列的方式处理全身运动生成。框架将多模态条件——文本 $c_t$（语义引导）、全局运动 $c_g$（时空一致性）、语音 $c_s$（手势与唇形同步）、音乐 $c_m$（节奏对齐）以及参考运动 $c_r$（内容与风格一致性）——统一整合为条件信号。

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/005_Figure_2.jpg]]
*Figure 2: Overview of OmniMotion-X, a unified multimodal autoregressive transformer diffusion model for whole-body human motion generation. OmniMotion-X integrates text, global motion, speech, music, and reference motion as conditions through condition-specific encoders mapped into a unified space. The model fuses multimodal information to produce coherent motion, with spatial-temporal guidance ensuring consistent global motion characteristics*

#### 模态特定编码

对于每种模态，框架采用专用的编码器提取特征：
- **文本**：使用 T5-XXL 编码语义信息
- **语音**：通过 wav encoder 提取音频特征
- **音乐**：基于 Librosa 进行节奏与旋律分析
- **运动**：采用 body-wise encoding 对全局运动和参考运动进行编码

#### 统一前缀条件连接

各模态编码后的特征经投影层对齐维度后，拼接为统一的条件前缀 $c$：

$$c = [ h_t(f_t(c_t)), h_g(f_g(c_g)), h_s(f_s(c_s)), h_m(f_m(c_m)), h_r(f_r(c_r)) ]$$

其中 $f_*$ 为模态特定编码器，$h_*$ 为线性投影层。该前缀作为 Diffusion Transformer（DiT）主干的上下文输入，使模型在去噪过程中能够同时感知语义、时空、节奏和风格等多层次条件。

#### DiT 主干与运动预测

DiT 主干接收带噪运动序列 $x_t$、时间步 $t$ 以及条件前缀 $c$，直接预测原始运动 $x_0$，而非噪声本身。训练目标为简单的均方误差损失：

$$L_{\mathrm{simple}} = \mathbb{E}_{x_0 \sim q(x_0|c), t \sim [1,T]} \left[ \| x_0 - G(x_t, t, c) \|_2^2 \right]$$

其中 $G$ 为去噪函数。这种 $x_0$-prediction 策略有助于在自回归生成过程中保持运动片段的连贯性。

#### 空间时间掩码策略

为统一处理全局空间时间可控生成任务（包括稀疏和稠密控制），框架引入空间时间掩码策略。通过对运动序列的特定关节或时间步进行掩码，模型能够在推理时灵活地完成轨迹引导、关键帧插值等多样化任务，而无需为每种控制模式设计单独的分支。

### 渐进式从弱到强的训练策略

OmniMotion-X 的关键创新在于**渐进式从弱到强的混合条件训练策略**（Figure 3）。训练分为多个阶段，逐步从高层语义过渡到稠密时空约束：

1. **第一阶段（弱条件）**：仅使用文本条件训练，建立运动-语义的基本对齐
2. **后续阶段（逐步增强）**：依次引入参考运动、全局运动、语音、音乐等更强约束条件

这种由粗到细的渐进训练有效规避了多粒度条件同时优化时的冲突问题。消融实验（Table 7）证实：移除渐进训练策略后，文本到运动任务的 FID 从 5.040 上升至 9.574，全局时空控制任务的 FID 从 4.224 上升至 10.247，退化幅度分别达 89.9% 和 142.6%。

### 参考运动条件与自回归生成

OmniMotion-X 首次将**参考运动作为特殊条件信号**引入运动扩散框架。在自回归生成过程中，前一生成片段的末尾帧作为当前片段的参考运动，通过条件前缀注入模型，从而显著增强跨片段的内容、风格和时间动态一致性。Table 7 显示，仅使用参考运动而不使用其他多模态条件时，FID 仍保持较低水平（7.824），验证了该条件的独立有效性。

### 输入输出流总结

- **输入**：文本描述、语音/音乐音频、全局轨迹/关键帧约束、参考运动片段（可选组合）
- **处理**：模态编码 → 特征投影与拼接 → DiT 去噪预测 $x_0$
- **输出**：统一 SMPL-X 格式的全身运动序列，包含根位移、关节旋转、面部表情等完整参数
- **生成模式**：支持单次生成和自回归长序列生成，参考运动条件确保片段间平滑过渡

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/001_Figure_1.jpg]]
*Figure 1: We present OmniMotion-X, a unified sequence-to-sequence autoregressive motion diffusion transformer designed for flexible and interactive whole-body human motion generation. It supports a variety of tasks, including text-to-motion, music-todance, speech-to-gesture, and globally spatial-temporal controllable motion generation, which encompasses motion prediction, in-betweening, completion, and joint/trajectory-guided synthesis. These conditions can be combined in various ways to enable versatile motion generation*



### 统一多模态条件建模

OmniMotion-X 的核心设计是将异构多模态条件统一为序列前缀，注入扩散变压器（DiT）主干。模型支持五类条件：文本 $\mathbf{c}_t$（语义引导）、全局运动 $\mathbf{c}_g$（时空一致性）、语音 $\mathbf{c}_s$（手势同步）、音乐 $\mathbf{c}_m$（舞蹈节奏）以及参考运动 $\mathbf{c}_r$（内容与风格锚定）。

每种模态首先通过专用编码器提取特征：文本采用 T5-XXL，语音采用 wav encoder，音乐采用 Librosa，运动条件采用 body-wise encoding。随后，各模态特征经投影函数 $h_*$ 对齐至统一维度，拼接为条件前缀：

$$c = [\, h_t(f_t(\mathbf{c}_t)),\; h_g(f_g(\mathbf{c}_g)),\; h_s(f_s(\mathbf{c}_s)),\; h_m(f_m(\mathbf{c}_m)),\; h_r(f_r(\mathbf{c}_r)) \,]$$

该前缀直接作为 DiT 的上下文输入，使去噪过程在所有条件下联合进行，避免了独立分支带来的优化冲突。这一设计是模型从高层语义到精细时空约束实现一致生成的结构基础。

### 扩散损失函数

OmniMotion-X 采用直接预测原始运动 $\mathbf{x}_0$ 的扩散范式，而非预测噪声。给定条件前缀 $c$ 和时间步 $t$，去噪网络 $G$ 从带噪运动 $\mathbf{x}_t$ 重建原始运动，损失函数为：

$$\mathcal{L}_{\text{simple}} = \mathbb{E}_{\mathbf{x}_0 \sim q(\mathbf{x}_0|c),\, t \sim [1,T]}\left[ \|\mathbf{x}_0 - G(\mathbf{x}_t, t, c)\|_2^2 \right]$$

该公式的含义是：在条件 $c$ 下采样真实运动 $\mathbf{x}_0$，对其加噪至时刻 $t$，然后最小化网络预测与原始运动之间的均方误差。直接预测 $\mathbf{x}_0$ 的策略简化了训练目标，并有助于在渐进式多条件训练中保持运动语义的稳定性。

### 文本-运动对比对齐（补充损失）

为进一步强化文本与运动之间的细粒度语义对齐，OmniMotion-X 在训练中引入对比损失。记文本特征为 $\mathbf{s}_t$，对应运动特征为 $\mathbf{s}_m$，两者之间的 L2 距离定义为：

$$D_{\mathbf{s}_t, \mathbf{s}_m} = \|\mathbf{s}_t - \mathbf{s}_m\|_2$$

对比损失函数为：

$$\mathcal{L}_{\text{Cta}} = (1 - y)\,(D_{\mathbf{s}_t, \mathbf{s}_m})^2 + y\,\{\max(0,\, d - D_{\mathbf{s}_t, \mathbf{s}_m})\}^2$$

其中 $y$ 为匹配指示符：当文本与运动构成匹配对时 $y=0$，损失最小化特征距离；当两者不匹配时 $y=1$，损失将距离推开至边界 $d$ 之外。该损失作为扩散损失的补充，在渐进训练的语义对齐阶段发挥关键作用。

### 空间-时间掩码策略

OmniMotion-X 将多种全局时空控制任务（如运动预测、中间帧插值、轨迹引导生成等）统一为空间-时间掩码框架。具体而言，对于给定的控制约束，模型对运动序列中未受约束的关节或时间步施加掩码，仅以可见部分作为条件输入 DiT 进行去噪生成。这一策略使同一模型无需额外分支即可处理稀疏关节控制、稠密关节控制、稀疏轨迹引导和稠密轨迹引导等多种任务变体，实现了全局时空可控生成的统一。

### 模块间的因果机制

上述模块之间存在明确的因果依赖：统一前缀连接解决了多模态条件的表示融合问题，使 DiT 能够同时感知所有条件信号；直接预测 $\mathbf{x}_0$ 的扩散损失为多条件联合优化提供了稳定的训练目标；对比损失在语义层面强化了文本-运动对齐，弥补了纯重建损失的语义模糊性；空间-时间掩码策略则将不同粒度的控制任务统一为同一推理范式。三者共同支撑了渐进式从弱到强训练策略的有效执行——在训练初期，模型仅依赖文本条件建立语义对齐；随后逐步引入参考运动、全局运动、语音和音乐等更强约束，使模型从粗粒度语义平滑过渡到细粒度时空控制。

**证据强度说明**：上述公式均直接引自论文 Equation (1)–(4) 及 Supplementary Material，具有高置信度（≥0.95）。公式变量含义基于原文描述，未进行外推或猜测。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/006_Figure_3.jpg]]
*Figure 3: We propose the weak-to-strong progressive training strategy, establishing motion-semantic alignment with text, followed by progressive integration of stronger multimodal signals (reference motion, global motion, speech, music) for enhanced generation quality and controllability*



## 实验与关键发现

### 文本到运动生成主结果

表 4 报告了 OmniMoCap-X 测试集上的文本到运动定量结果。OmniMotion-X 在 FID 指标上达到 **5.040**，相比此前最优的 MoMask*（17.428）降低 71.1%；R Precision Top-1 达到 **0.303**，较 MoMask*（0.267）提升 13.5%。引入参考运动条件后（Ours+RM），FID 进一步降至 **3.199**，R Precision Top-1 升至 **0.346**，验证了参考运动对内容一致性和语义对齐的增益。值得注意的是，OmniMotion-X 的 Diversity 为 8.650，与真实数据（9.003）最为接近，表明其在保证质量的同时未牺牲生成多样性。

与现有方法对比时需注意：MoMask、MotionGPT 等基线未在 OmniMoCap-X 上训练，表中以 * 标注重新训练版本以保证公平；所有结果均基于 20 次重复实验的均值和 95% 置信区间。

### 全局时空可控生成

表 5 展示了全局时空可控生成任务的定量结果。OmniMotion-X 在稀疏关节控制（GSTC(S)）和稠密关节控制（GSTC(D)）两个子任务上均显著优于基线。以 FID 为例，完整模型在全局时空控制任务上达到 **4.224**，而移除渐进训练策略的变体（w/o progressive training）FID 劣化至 10.247，降幅达 58.8%。这直接证明了渐进式从弱到强训练策略对稠密时空约束任务的关键作用——仅靠单阶段混合训练无法有效协调高层语义与精细空间约束之间的优化冲突。

### 消融实验：训练策略与参考运动

表 7 的消融实验揭示了两个核心组件的贡献：

1. **渐进训练策略**：移除渐进训练（w/o TrSt）后，文本到运动 FID 从 5.040 上升至 9.574，全局时空控制 FID 从 4.224 上升至 10.247。这表明由粗到细的阶段式训练是解决多粒度条件冲突的瓶颈机制——模型需要先建立文本-运动语义对齐，再逐步引入更强的时空约束信号。

2. **参考运动条件**：仅使用参考运动而不使用其他多模态条件时，FID 仍保持 7.824 的较低水平，验证了参考运动作为独立条件信号的有效性。当参考运动与文本条件联合使用时，FID 从 5.040 进一步降至 3.199，说明参考运动提供的风格和动态先验与文本语义形成互补。

### 定性结果与任务覆盖

图 4 展示了 OmniMotion-X 在六类任务上的生成能力：(a) 文本到运动、(b) 语音到手势、(c) 音乐到舞蹈、(d) 轨迹引导运动、(e) 运动中间帧插值、(f) 运动预测。定性结果表明，统一的多模态前缀条件连接使模型能在不同条件组合下保持运动质量和时间一致性，无需为每类任务设计独立架构。

### 失败模式与局限性

尽管 OmniMotion-X 在多任务上取得领先结果，仍存在以下局限：

- **复杂交互场景**：当前框架尚未深度融合场景几何、物体约束及多人交互条件。对于“人坐在椅子上并操作物体”这类涉及环境上下文的多层次约束运动，生成质量可能下降。这是统一条件框架的已知扩展方向，需要手动验证具体失败案例。
- **推理效率**：扩散变压器在自回归推理时仍需多步去噪，面向实时应用（如交互式角色动画）的推理速度有优化空间。论文未报告具体推理延迟数据，该点需结合代码仓库实际测试确认。

### 数据集对比与实验公平性

表 2 对比了 OmniMoCap-X 与现有合并数据集的规模和质量。OmniMoCap-X 包含约 286.2 小时、64.3M 帧的运动数据，且 100% 来自动捕源（Mocap Source），远高于 Motion-X（13.6%）和 HumanML3D（50.1%）。在文本标注方面，OmniMoCap-X 采用视觉信息（V）和文本信息（T）联合补全缺失描述，避免了纯模板生成导致的语义单一问题（表 8 的 TTR 统计佐证了标注的词汇多样性）。这一数据优势为 OmniMotion-X 的多任务泛化提供了基础，但也意味着在更小规模或更低质量数据集上的迁移表现需要额外验证。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/007_Table_4.jpg]]
*Table 4: Quantitative results of text-to-motion on the OmniMoCap-X test set. ↑ (↓) indicates that a larger (smaller) value is better. → indicates that a value closer to the GT is better. Red and Blue colors indicate the best and second-best results respectively. All evaluations are repeated 20 times, reporting the mean and 95% confidence interval*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/012_Table_7.jpg]]
*Table 7: Ablation Study on the Training Strategy*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/008_Table_5.jpg]]
*Table 5: Quantitative results of global spatiotemporal controllable generation on the OmniMoCap-X test set*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/002_Table_1.jpg]]
*Table 1: Comparison between OmniMotion-X and existing human motion generation methods. ”GSTC(S)” and ”GSTC(D)” denote global spatial-temporal controllable motion generation, where ”S” and ”D” indicate sparse and dense controlled joints, respectively. “Reference Motion” originates from user-designed or previously generated motion. ”Mixed-condition” refers to the simultaneous occurrence of multiple conditions during training. “Datasets” indicates the total number of datasets used for training, while ”Hours” represents the longest training dataset duration. For methods like MoMask, trained separately on HumanML3D or KIT, the duration of the HumanML3D dataset is considered*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/003_Table_2.jpg]]
*Table 2: Comparisons between OmniMoCap-X and existing merged datasets. ”Mocap Source” indicates the proportion of mocap datasets. ”Caption Source” specifies the method for completing missing descriptions: ”-” (no completion), ”V” (visual information), and ”T” (textual information). ”Hierarchical Caption” shows if captions include hierarchical text*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/011_Figure_4.jpg]]
*Figure 4: Diverse motion synthesis capabilities of OmniMotion-X. OmniMotion-X supports multiple tasks: (a) text-to-motion, (b) speech-to-gesture, (c) music-to-dance, (d) trajectory-guided motion, (e) motion in-betweening, and (f) motion prediction*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/004_Table_3.jpg]]
*Table 3: Composition of OmniMoCap-X dataset, unifying motion formats into SMPL-X with captions. We select 28 publicly available high-quality datasets across various tasks. Frames and Hours are computed based on raw dataset FPS. MoCap represents data capture methods, ranked by quality: Marker with manual correction (Marker-M), Vicon Marker (Marker-V), IMU, Multi-View RGB (MV-RGB), and Single-View RGB (SV-RGB). Format specifies the original motion format*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/013_Table_8.jpg]]
*Table 8: Text quality statistics across motion datasets. The third column shows the number of text samples per dataset. The fourth column displays the average sentence length (in word count). The fifth column presents the Type-Token Ratio (TTR) range, indicating lexical diversity (higher values represent richer vocabulary). The sixth column lists the ten most frequent verbs in each dataset, reflecting the predominant actions described in the motion text. The datasets are grouped by their primary task: Text-to-Motion (T2M), Music-to-Dance (M2D), Speech-to-Gesture (S2G), Human-Human Interaction (HHI), Human-Object Interaction (HOI), and Human-Scene Interaction (HSI)*

![[assets/figures/papers/paper_list_l4_https_arxiv_org_abs_2510_19789/figures/010_Figure.jpg]]
*Figure: (a) Text-to-motion (d) Trajectory-guided synthesis*



## 定位与知识库关联

### 与现有方法的谱系关系

OmniMotion-X 处于**多模态全身运动生成**这一交叉地带，其方法谱系可追溯至三条主线：文本到运动扩散模型、多模态条件运动生成、以及自回归运动序列建模。

**文本到运动扩散基线。** 以 **MDM**（Tevet et al., 2022）为代表的早期扩散方法将运动生成建模为去噪过程，但其条件模态单一，无法扩展至多模态控制。OmniMotion-X 继承了扩散范式的基本框架，但将条件空间从纯文本扩展为多模态前缀，并在去噪目标上采用直接预测 $x_0$ 而非噪声残差（见公式 $L_{\mathrm{simple}}$），这与 MDM 的 $\epsilon$-prediction 形成差异。

**多模态条件运动生成基线。** 现有方法如 **MCM**（Ling et al., 2023）、**LMM**（Zhang et al., 2024）、**MotionCraft**（Bian et al., 2024）、**MGPT**（Luo et al., 2024）、**MotionLLAMA**（Ling et al., 2024）和 **AMD**（Han et al., 2024）均尝试融合多种条件模态，但它们普遍采用**任务特定架构或独立控制分支**——不同条件通过分离的编码器-解码器路径注入，导致训练冲突和控制粒度不匹配。OmniMotion-X 的关键突破在于将所有条件统一为序列前缀连接（公式 $c = [h_t(f_t(c_t)), h_g(f_g(c_g)), ...]$），使 DiT 主干能够在统一的注意力空间中进行跨模态融合。这一设计消除了独立分支间的优化冲突，是 FID 从基线最优 17.428 降至 5.040（降低 71.1%）的核心架构因素。

**自回归运动序列建模基线。** **MoMask**（Guo et al., 2024）、**MotionGPT**（Jiang et al., 2024）和 **DART**（Zhao et al., 2024）采用自回归范式生成运动序列。OmniMotion-X 同样采用自回归方式逐段生成长序列，但创新性地引入**参考运动条件**来强化跨片段的内容和风格一致性——这是上述自回归方法所不具备的。消融实验表明，仅使用参考运动（无其他多模态条件）时 FID 仍保持 7.824（Table 7），验证了该条件的独立有效性。

**数据集谱系。** 在数据层面，OmniMoCap-X 整合了 28 个公开动捕数据集（Table 3），总计 64.3M 帧、286.2 小时，远超现有合并数据集（Table 2）。其统一 SMPL-X 表示和高质量文本标注体系，为多模态统一训练提供了此前缺失的数据基础。

### 适用边界

OmniMotion-X 的适用边界由其设计选择决定：

**强适用场景。** 该方法在以下条件下表现最优：（1）需要文本语义、全局轨迹、语音节奏、音乐节拍等多种条件**同时驱动**的全身运动生成；（2）需要长序列生成且要求跨片段内容与风格一致（得益于参考运动条件）；（3）需要全局时空可控生成（稀疏或稠密关键点约束），这通过空间-时间掩码策略统一处理。

**弱适用场景。** 以下情况可能超出当前框架的有效边界：（1）**复杂场景与物体交互**——框架尚未深度融合场景几何、物体属性以及人-物接触等多层次约束；（2）**多人交互运动**——当前建模聚焦单人全身运动，多人协同或对抗场景未纳入条件体系；（3）**实时推理需求**——扩散模型的多步去噪和自回归生成范式在推理速度上存在天然瓶颈，面向实时应用需要更紧凑的运动表示和更高效的推理架构（这是论文明确指出的开放问题之一）。

### 局限与开放问题

**已确认的局限。** 论文明确指出的局限包括：（1）场景、物体与人类交互等多层次约束尚未深度融合，对于“人在环境中”的复杂交互式全身运动生成仍存在局限性；（2）运动表示与推理速度仍有优化空间，当前框架难以满足实时交互应用的低延迟需求。

**开放问题。** 从方法谱系的角度，以下问题值得关注：

1. **条件空间的进一步扩展。** 如何将场景几何、物体属性、物理接触力等结构化约束以统一前缀的方式集成到现有条件框架中？这可能需要新的模态特定编码器和跨模态对齐策略。

2. **运动表示的效率优化。** 当前 SMPL-X 表示维度较高，如何开发更紧凑的运动表示（如离散化 token、隐空间压缩）以加速扩散模型的推理，是该方向走向实用的关键瓶颈。

3. **渐进训练策略的泛化性。** 从弱到强的渐进训练在 OmniMotion-X 上验证有效（移除该策略导致 FID 从 5.040 上升至 9.574，全局时空控制 FID 从 4.224 上升至 10.247），但该策略是否适用于其他多模态生成任务（如视频生成、音频合成）仍有待验证。

4. **参考运动条件的理论理解。** 参考运动为何能有效提升跨片段一致性？其在特征空间中是否隐式编码了运动风格和动态模式的原型表示？这一机制的理论分析尚不充分。



## 原文 PDF

![[paperPDFs/arxiv_2025/OmniMotion-X:_Versatile_Multimodal_Whole-Body_Motion_Generation.pdf]]
