---
title: An Advanced Multimodal Multitask Framework for Motion Comprehension and Generation
type: paper
paper_level: A
venue: NEURIPS
year: 2024
pdf_ref: paperPDFs/NEURIPS_2024/An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation.pdf
aliases:
- AMMFMCG
tags:
- NEURIPS_2024
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用文本作为桥梁对齐多模态数据，并通过辅助任务（音乐到文本、文本到舞蹈）缓解多任务冲突，同时联合优化语言模型与运动解tokenizer。
primary_logic: 通过将运动、音乐、文本统一离散化到共享词汇表，并在原始运动空间中联合训练语言模型，可以实现多模态运动理解与生成任务的协同互促。
claims:
- 添加辅助文本-舞蹈和音乐-文本任务后，音乐到舞蹈的FID_k下降近10个点。
- 联合优化LLM和运动解tokenizer始终带来性能增益，尤其在舞蹈生成上FID_k显著下降。
- Motion-X Text-to-Motion 上 RPrecision Top1 = 0.661
- AIST++ Music-to-Dance 上 FIDk = 24.34
---

# An Advanced Multimodal Multitask Framework for Motion Comprehension and Generation

> [!tip] 核心洞察
> 通过将运动、音乐、文本统一离散化到共享词汇表，并在原始运动空间中联合训练语言模型，可以实现多模态运动理解与生成任务的协同互促。

| 字段 | 内容 |
|------|------|
| 中文题名 | M3GPT：一种面向运动理解与生成的高级多模态多任务框架 |
| 英文题名 | An Advanced Multimodal Multitask Framework for Motion Comprehension and Generation |
| 会议/期刊 | NEURIPS 2024 |
| Links | [Project](https://github.com/luomingshuang/M3GPT) · [Code](https://github.com/luomingshuang/M3GPT") |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | M3GPT |
| Dataset | Motion-X Text-to-Motion, AIST++ Music-to-Dance |

> [!tip] 效果简介
> - Motion-X Text-to-Motion 上，RPrecision Top1 0.661 vs 0.645 (单任务训练) (+0.016)。
> - AIST++ Music-to-Dance 上，FIDk 24.34 vs 83.33 (单任务训练) (-59.0)。

## 概述

人体运动理解与生成是构建智能数字人的核心能力，涵盖文本到运动、音乐到舞蹈、运动描述等多个子任务。现有方法通常将各任务独立建模，缺乏统一的表示空间与有效的跨任务协同机制，导致在单一框架内进行多任务联合训练时，各任务性能反而下降。**M3GPT** 针对这一瓶颈，提出了一种基于离散向量量化的多模态多任务框架，其核心思想可归结为三条原则：

1. **统一表示空间**：通过运动 VQ-VAE 与音乐 VQ-VAE（Jukebox）将连续的运动、音乐数据压缩为离散语义标记，并与文本标记共同构成一个共享的扩展词汇表。
2. **原始运动空间建模**：在离散标记的自回归似然损失之外，引入原始运动空间的 L1 重建损失，联合优化语言模型与运动解 tokenizer，使生成结果在连续运动空间中也保持高质量。
3. **文本作为跨模态桥梁**：构建音乐到文本、文本到舞蹈等辅助任务，利用文本作为中介对齐音乐与运动模态，缓解多任务冲突并实现协同互促。

在方法谱系上，M3GPT 属于 **统一多模态语言模型路线**，区别于 **TM2D**（分任务独立建模）、**UDE**（单任务舞蹈生成）、**MotionGPT**（仅文本-运动统一）以及 **MDM**、**MoMask** 等扩散或掩码模型。M3GPT 在能力覆盖广度上具有明显优势——同时支持文本到运动、运动到文本、音乐到舞蹈、舞蹈到音乐、运动预测与运动插值六类任务，而多数基线仅能处理其中一到两类（见 Table 1）。

关键实验结果验证了设计决策的有效性：
- 在 **Motion-X** 文本到运动任务上，多任务联合训练的 RPrecision Top1 达到 **0.661**，优于单任务训练的 0.645。
- 在 **AIST++** 音乐到舞蹈任务上，引入辅助文本-舞蹈和音乐-文本任务后，FID_k 从单任务训练的 83.33 大幅降至 **24.34**（降幅约 59 个点），消融实验进一步表明协同学习贡献了约 10 个点的 FID_k 下降（Table 2）。
- 联合优化 LLM 与运动解 tokenizer 始终带来性能增益，尤其在舞蹈生成上 FID_k 显著下降，同时对文本到运动的 FID 影响极小（增加 <0.003）。

M3GPT 尚存若干局限：当前模型仅关注身体运动，未包含手部与面部建模；训练数据规模有限，零样本泛化在极端未见任务组合上的表现有待验证；训练需 8 块 NVIDIA A40 GPU，计算门槛较高。这些也为后续研究指明了方向——包括扩展统一词汇表至更多模态、引入精细的全身运动建模，以及探索更高效的多任务调度策略以进一步缓解负迁移。

## 背景与动机

### 多模态运动任务的统一挑战

人体运动理解与生成涵盖文本到运动（Text-to-Motion）、运动到文本（Motion-to-Text）、音乐到舞蹈（Music-to-Dance）、舞蹈到音乐（Dance-to-Music）、运动预测（Motion Prediction）及运动插值（Motion In-between）等多项核心任务。这些任务涉及文本、音乐、舞蹈等多种模态，各模态在数据形式、语义粒度和时序结构上存在显著差异。现有方法通常针对单一任务设计专用模型，缺乏统一的表示空间和有效的跨任务协同机制。当尝试将多个任务整合到单一框架内进行联合训练时，各任务性能往往出现明显下降，这一现象揭示了多模态运动任务联合建模的核心瓶颈：模态差异大，任务间存在负迁移。

### 现有方法的局限

近期工作已开始探索统一运动-语言模型的可能性。**MotionGPT** 将运动离散化为token，与文本token混合输入语言模型进行自回归建模，但其仅在离散语义空间优化，忽略了原始连续运动空间的重建质量。**TM2D** 和 **UDE** 分别针对文本-运动和音乐-舞蹈任务，但缺乏跨任务的协同设计。扩散模型如 **MDM** 和掩码变换器如 **MoMask** 在文本到运动生成上表现优异，却无法处理运动理解、音乐-舞蹈等多任务场景。这些方法的核心缺口在于：未能在统一框架内实现多模态数据的对齐表示，且缺乏缓解多任务冲突的有效机制。

### M3GPT的动机与核心思路

针对上述瓶颈，M3GPT提出三条核心设计原则：

1. **统一表示空间**：通过离散向量量化（VQ-VAE）将运动、音乐、文本分别压缩为离散语义token，并扩展为共享的统一词汇表，使不同模态在同一个离散空间中可互操作。
2. **原始运动空间建模**：在离散语义空间优化语言模型的同时，额外引入原始运动空间的L1重建损失，联合优化LLM与运动解tokenizer，确保生成运动的物理真实感。
3. **文本作为桥梁实现多任务协同**：通过构建辅助的音乐到文本（Music-to-Text）和文本到舞蹈（Text-to-Dance）任务，以文本描述为中介对齐音乐与舞蹈模态，缓解直接跨模态映射带来的任务冲突。

这些设计使M3GPT能够在单一框架内处理六项核心运动任务，并通过多任务预训练与指令微调实现任务间的协同互促，而非简单的多任务叠加。

## 核心创新

M3GPT 的核心创新并非提出单一的新模块，而是通过三个相互耦合的 **changed slots**，系统性地解决了多模态运动任务中“模态差异大、缺乏统一表示空间、多任务联合训练导致性能下降”这一瓶颈。

### 1. 统一离散词汇表：打破文本、运动与音乐的模态壁垒

传统方法通常为文本和运动分别建模，音乐模态则常被忽略或独立处理。M3GPT 将文本、运动、音乐三者统一离散化到共享的词汇表中。

- **基线做法**：词汇表仅包含文本标记，运动生成依赖外部解码器或独立的扩散模型，模态间缺乏底层的表示对齐。
- **M3GPT 做法**：通过运动 VQ-VAE tokenizer 将连续 3D 人体运动压缩为离散运动标记序列，并利用预训练的 Jukebox VQ-VAE 将音乐压缩为离散音乐标记序列。这些标记与文本标记共同构成扩展后的统一词汇表（Sec.3.2 “Expanding Vocabulary”）。
- **因果作用**：统一词汇表使得 T5 语言模型主干能够以自回归方式对任意模态的 token 序列进行统一建模，将文本到运动、音乐到舞蹈、运动到文本等异构任务转化为同一个“序列到序列”的格式。这是后续多任务协同与联合优化的基础。

### 2. 多任务协同学习：以文本为桥梁消除任务冲突

多任务联合训练的一个常见失败模式是“负迁移”——多个任务共享同一模型时，各任务性能反而低于单独训练。M3GPT 在 Table 2 中明确观察到了这一现象：直接进行多任务联合训练，各任务指标均劣于单任务训练。

- **基线做法**：各任务独立训练，无跨任务对齐机制；或简单混合多任务数据联合训练，导致任务间梯度冲突。
- **M3GPT 做法**：利用文本作为跨模态对齐的桥梁，构造了两个辅助任务——**文本到舞蹈（Text-to-Dance, T2D）** 和 **音乐到文本（Music-to-Text, A2T）**。这些辅助任务与主任务（文本到运动、音乐到舞蹈）共享同一运动/舞蹈 tokenizer 和语言模型，强制模型在音乐、文本、运动三个语义空间之间建立关联（Sec.3.3 “Synergy learning of multitasks”）。
- **因果作用**：辅助任务在音乐与运动之间插入了文本这一中间表示，缓解了音乐特征与运动特征之间的直接对齐困难。**决定性证据**来自 Table 2 消融：添加 T2D 和 A2T 后，音乐到舞蹈的 FID_k 下降近 10 个点（从 83.33 降至约 73，置信度 0.95），验证了协同学习有效促进了两个主生成任务之间的互促。

### 3. 联合优化 LLM 与运动解 tokenizer：在连续运动空间施加直接监督

现有基于离散 token 的运动生成方法（如 MotionGPT、MoMask）通常固定运动 tokenizer，仅在离散 token 空间优化语言模型的交叉熵损失。这导致模型无法感知生成 token 解码回连续运动空间后的实际重建质量。

- **基线做法**：仅使用离散 token 空间的下一个 token 预测损失（交叉熵）优化 LLM，运动解 tokenizer 保持冻结。
- **M3GPT 做法**：在训练目标中额外引入原始运动空间的 L1 重建损失 $\lambda \left\| \hat{\pmb{m}} - \pmb{m} \right\|_1$，联合优化 LLM 与运动解 tokenizer。完整训练目标为：

  $$\mathcal{L} = \sum_{i=0}^{L_t-1} \log p_{\theta} \left( \pmb{q}_t^i | \pmb{q}_t^{<i}, \pmb{q}_s \right) + \lambda \left\| \hat{\pmb{m}} - \pmb{m} \right\|_1$$

  其中 $\lambda$ 经消融实验确定为 0.2（Table 18，置信度 0.95）。

- **因果作用**：L1 重建损失将连续运动空间的监督信号直接传导至 LLM 的输出端，迫使模型不仅关注 token 级别的分类精度，也关注解码后运动的物理合理性。**决定性证据**来自 Table 2：联合优化始终带来性能增益，尤其在舞蹈生成上 FID_k 下降显著；同时文本到运动的 FID 仅有极轻微的增加（<0.003），表明该方法在多个任务上均有效且无显著副作用。

### 创新点之间的因果链

上述三个 changed slots 并非独立运作，而是形成一条因果链：

1. **统一词汇表**提供了多模态数据在同一序列空间内交互的基础；
2. **多任务协同学习**利用这一统一空间，通过文本桥接消除了音乐与运动之间的对齐困难；
3. **联合优化**在连续运动空间施加直接监督，弥补了纯离散 token 优化在运动质量上的不足。

三者叠加使得 M3GPT 在单一框架内实现了文本到运动、音乐到舞蹈、运动到文本等多项任务的协同互促，而非彼此干扰。

## 整体框架

M3GPT 的整体框架遵循“离散化—对齐—指令化”的三阶段训练范式，核心由**多模态分词器（Multimodal Tokenizers）**与**运动感知语言模型（Motion-Aware Language Model）**两大组件构成。其设计目标是将文本、运动、音乐三种模态统一到一个共享的离散词汇空间中，使单一语言模型主干能够同时处理运动理解与生成任务。

### 多模态分词器：将连续信号压缩为离散语义标记

框架的第一层是模态专用的分词器，负责将原始连续数据转换为离散标记序列，从而消除模态间的表示差异。

- **运动分词器（3D Human Motion Tokenizer）**：基于 VQ-VAE 架构，将连续的 3D 人体运动序列压缩为离散运动标记。编码器将运动序列 $\pmb{m}$ 映射为潜在向量序列 $\pmb{z}$，随后通过最近邻查找在码本 $\mathcal{B}_m$ 中进行量化：

  $$\pmb{e} = \underset{b^k \in \mathcal{B}_m}{\arg \min} \| z - b^k \|_2$$

  运动分词器的训练损失由三项组成——L1 重建损失、嵌入损失与承诺损失：

  $$\mathcal{L}_{vq} = \| \hat{\pmb{m}} - \pmb{m} \|_1 + \| \mathrm{sg}[\pmb{z}] - \pmb{e} \|_2^2 + \beta \| \pmb{z} - \mathrm{sg}[\pmb{e}] \|_2^2$$

  其中 $\beta = 0.02$，码本大小设为 512。

- **音乐分词器（Music Tokenizer）**：直接采用预训练的 Jukebox VQ-VAE，将音乐压缩为离散音乐标记序列，码本大小为 2048。该分词器在 M3GPT 训练过程中保持冻结。

- **文本文分词**：文本部分沿用 T5 语言模型原生的文本分词器，无需额外训练。

### 运动感知语言模型：统一词汇表下的自回归建模

框架的第二层以 **T5** 作为语言模型主干。M3GPT 的关键创新在于**扩展词汇表**：将文本、运动码本、音乐码本合并为一个统一词汇表 $V$。在此基础上，所有运动相关任务被格式化为统一的输入-输出模式——输入与输出标记均来自同一词汇表，使语言模型能够以标准自回归方式对不同模态的标记序列进行联合建模。

这种设计使得 M3GPT 能够天然地处理六类核心任务：文本到运动（T2M）、运动到文本（M2T）、音乐到舞蹈（A2D）、舞蹈到音乐（D2A）、运动预测（Motion Prediction）和运动插值（Motion In-Between），如 Figure 2 所示。

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/003_Figure_2.jpg]]
*Figure 2: An overview of the*

### 三阶段训练流程

M3GPT 的训练分为三个递进阶段（Figure 2）：

1. **阶段一：多模态分词器训练**。独立训练运动 VQ-VAE 分词器，音乐分词器则直接使用 Jukebox 预训练权重。此阶段仅涉及模态内部的压缩与重建，不涉及跨模态交互。

2. **阶段二：模态对齐预训练**。在统一词汇表下，语言模型以自回归方式学习多模态标记序列的联合分布。此阶段的核心训练目标包含两项：最大化目标标记的对数似然，以及**在原始运动空间中引入 L1 重建损失**，使语言模型与运动解分词器（motion de-tokenizer）进行联合优化：

   $$\mathcal{L} = \sum_{i=0}^{L_t-1} \log p_{\theta} \left( \pmb{q}_t^i | \pmb{q}_t^{<i}, \pmb{q}_s \right) + \lambda \left\| \hat{\pmb{m}} - \pmb{m} \right\|_1$$

   其中 $\lambda = 0.2$，$\hat{\pmb{m}}$ 为生成的原始运动序列。这一设计使模型不仅在离散语义空间中被优化，同时也在连续运动空间中受到约束，从而提升生成运动的物理合理性。

3. **阶段三：指令微调**。定义 11 项核心任务，每项任务包含 200/50/50 的训练/验证/测试指令模板，以指令跟随（instruction-following）的方式对模型进行微调，使其能够根据自然语言指令灵活切换任务。

### 多任务协同学习机制

直接进行多任务联合训练通常会导致各子任务性能劣于单任务训练（Table 2）。M3GPT 通过**以文本为桥梁**构造辅助任务来解决这一冲突：为音乐数据构建配对的文本描述，并设计**文本到舞蹈（T2D）**和**音乐到文本（A2T）**两个辅助任务。这些辅助任务在音乐到舞蹈与文本到运动两条主线之间建立了协同通路，使模型在共享的运动/舞蹈分词器下实现跨任务的知识迁移与相互增强。

### 补充图表

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/001_Figure_1.jpg]]
*Figure 1: M3GPT can handle core motion comprehension and generation tasks, including text-to-motion, motionto-text, music-to-dance, dance-to-music, motion prediction, and motion in-between. The motion sequences within the dashed-line areas are masked in the input*

## 核心模块与公式推导

M3GPT 的核心架构由**多模态分词器（tokenizer）**和**运动感知语言模型**两部分构成，如图 Figure 2 所示。其关键设计在于将所有模态统一到同一离散词汇表，并通过在原始运动空间中的联合优化实现跨任务协同。

### 多模态分词器

**运动 VQ-VAE tokenizer** 负责将连续的 3D 人体运动序列压缩为离散的运动标记。其核心操作为向量量化：对于编码器输出的每个潜在向量 $z$，在码本 $\mathcal{B}_m$ 中搜索最近邻嵌入作为其离散表示：

$$
\pmb{e} = \underset{b^k \in \mathcal{B}_m}{\arg \min} \| z - b^k \|_2
$$

运动 tokenizer 的训练损失 $\mathcal{L}_{vq}$ 由三项构成：重建损失、嵌入损失和承诺损失：

$$
\mathcal{L}_{vq} = \| \hat{\pmb{m}} - \pmb{m} \|_1 + \| \mathrm{sg}[\pmb{z}] - \pmb{e} \|_2^2 + \beta \| \pmb{z} - \mathrm{sg}[\pmb{e}] \|_2^2
$$

其中 $\hat{\pmb{m}}$ 为解码器重建的运动序列，$\pmb{m}$ 为真实运动，$\mathrm{sg}[\cdot]$ 表示停止梯度算子，$\beta$ 为承诺损失的权重（设为 0.02）。运动码本大小为 512。

**音乐 VQ-VAE tokenizer** 直接采用预训练的 Jukebox VQ-VAE，将原始音乐信号压缩为离散音乐标记序列，其码本大小为 2048。

### 统一词汇表与语言模型

M3GPT 将文本、运动、音乐的码本合并为一个**统一词汇表** $V$，并采用 T5 作为语言模型主干。通过这种统一表示，各类运动相关任务可被格式化为通用的指令跟随模板：输入和输出的 token 均来自同一词汇表，语言模型以自回归方式对目标 token 序列进行建模。

### 联合优化与协同学习

M3GPT 的核心创新之一是在离散语义空间之外，额外引入**原始运动空间的重建损失**，实现 LLM 与运动解 tokenizer 的联合优化。训练目标同时最大化目标 token 的对数似然，并最小化生成运动与真实运动之间的 L1 重建误差：

$$
\mathcal{L} = \sum_{i=0}^{L_t-1} \log p_{\theta} \left( \pmb{q}_t^i | \pmb{q}_t^{<i}, \pmb{q}_s \right) + \lambda \left\| \hat{\pmb{m}} - \pmb{m} \right\|_1
$$

其中 $\pmb{q}_t$ 为目标 token 序列，$\pmb{q}_s$ 为源 token 序列，$L_t$ 为目标序列长度，$\hat{\pmb{m}}$ 为解 tokenizer 输出的运动序列，$\lambda$ 为平衡超参数（设为 0.2）。

此外，M3GPT 引入**协同多任务学习**策略：通过构建辅助的文本-舞蹈（Text-to-Dance）和音乐-文本（Music-to-Text）任务，以文本为桥梁对齐音乐与运动模态，缓解多任务联合训练中的性能冲突。消融实验（Table 2）表明，该策略使音乐到舞蹈的 FID_k 下降近 10 个点，验证了跨任务协同互促的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/012_Figure_5.jpg]]
*Figure 5: Tasks for M3GPT pre-training and instruction tuning. Random represents the unconstrained generation of motion/text/music in the corresponding task*

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/010_Figure_4.jpg]]
*Figure 4: Pipeline of Text-Motion Alignment Model. The training of the text-motion alignment model includes two stages: pre-training motion auto-encoder and text-motion contrastive learning*

## 实验与分析

### 核心消融：协同学习与联合优化

M3GPT 在文本-运动（T2M）和音乐-舞蹈（A2D）两个核心生成任务上进行了系统的消融实验，以验证其两大关键设计：多任务协同学习（Synergy Learning）以及 LLM 与运动解 tokenizer 的联合优化（Joint Optimization）。结果汇总于 **Table 2**。

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/004_Table_2.jpg]]
*Table 2: Evaluation of synergy learning and joint optimization of LLM and motion de-tokenizer on Text-to-Motion (Motion-X [29]) and Music-to-Dance (AIST++ [24]). T2M: Text-to-Motion. A2D: Music-to-Dance. T2D: Text-to-Dance. A2T: Music-to-Text. Trained single task refers to a model trained and tested on a single task. Pre-trained and Instruction-tuned indicate the model after pre-training (stage2) and instruction tuning (stage3), followed by direct testing on each task. The arrows (↑) indicate that higher values are better. The arrows (↓) indicate that smaller values are better. Bold indicates the best result*

**基线设定与问题**：实验首先对比了单任务训练（Trained single task）与直接多任务联合训练（Pre-trained / Instruction-tuned w/o synergy）的效果。结果表明，简单的多任务联合训练会导致各子任务性能显著下降，尤其在音乐-舞蹈生成上，FID_k 从单任务的 83.33 急剧恶化，验证了多模态运动任务间存在严重的训练冲突与负迁移现象。

**协同学习的决定性作用**：引入辅助的文本-舞蹈（T2D）和音乐-文本（A2T）任务后，模型性能发生质变。关键证据是，音乐-舞蹈生成的 FID_k 指标大幅下降近 10 个点（Table 2, synergy learning rows）。这一结果强有力地证明，通过文本作为桥梁构建跨模态对齐任务，能够有效缓解多任务冲突，实现文本-运动和音乐-舞蹈两大主任务之间的协同互促。

**联合优化的增益**：将 LLM 与运动解 tokenizer 进行联合优化（即在离散 token 空间与原始连续运动空间同时施加监督），在所有设置下均带来了稳定的性能提升。该增益在舞蹈生成上尤为突出，FID_k 显著下降；而在文本-运动任务上，FID 的增加极其微小（<0.003），表明该方法在提升舞蹈质量的同时，几乎未损害文本-运动的生成能力。

### 主任务性能对比

#### 文本-运动生成与理解

在 Motion-X 数据集上，M3GPT 与多个专用及统一基线模型进行了全面对比（**Table 3**）。

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/005_Table_3.jpg]]
*Table 3: Comparison results on Motion-X [29] dataset. The evaluation metrics are computed using the encoder introduced in Appendix A. Empty columns of previous methods indicate that they can not handle the task. Instruction-tuned only T2M indicates the model that is initially pre-trained on multiple tasks, followed by instruction tuning solely on text-to-motion task*

- **文本-运动生成（T2M）**：M3GPT 在 RPrecision Top1 上达到 0.661，优于单任务训练基线（0.645）及多数对比方法。在 FID 指标上，M3GPT 同样展现出竞争力。值得注意的是，经过指令微调（Instruction-tuned）的模型在文本-运动任务上性能进一步提升，验证了多任务预训练与特定任务微调结合的有效性。
- **运动-文本生成（M2T）**：M3GPT 能够生成准确的自然语言描述，其性能显著优于缺乏该能力的专用生成模型。
- **运动预测与插值（M2M）**：作为统一框架，M3GPT 自然支持运动预测和运动插值任务，而多数对比方法（如 MDM、MoMask）无法处理这些任务，体现了统一词汇表建模的灵活性优势。

#### 音乐-舞蹈与舞蹈-音乐生成

在 AIST++ 和 FineDance 数据集上的对比结果（**Table 5**）进一步验证了 M3GPT 在跨模态舞蹈生成上的优势。

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/007_Table_5.jpg]]
*Table 5: Comparison results on AIST++ [24] and FineDance [25] datasets*

- **音乐-舞蹈生成（A2D）**：在 AIST++ 上，M3GPT 取得了 24.34 的 FID_k，远优于单任务训练基线（83.33）及对比方法 TM2D、UDE。在 FineDance 数据集上，M3GPT 同样展现出优异的舞蹈质量与音乐对齐能力。
- **舞蹈-音乐生成（D2A）**：M3GPT 能够从舞蹈动作反向生成匹配的音乐，这是多数基线方法不具备的能力。

#### 定性分析

**Figure 7** 展示了 M3GPT 与 MDM、MoMask 在文本-运动任务上的定性对比。M3GPT 生成的运功作文本一致性更好，而基线方法在复杂语义理解上存在明显偏差（图中红色标注区域）。在音乐-舞蹈任务上，与 Bailando 的对比显示，M3GPT 生成的舞蹈与 5 秒 Break 风格音乐片段在节奏和风格上更加契合。

**Figure 3** 和 **Figure 6** 进一步展示了 M3GPT 在长时舞蹈生成和音乐-文本联合条件舞蹈生成上的能力，验证了统一框架在多条件组合生成任务上的扩展性。

### 失败模式与已知局限

尽管 M3GPT 在多任务统一建模上取得了显著进展，论文仍明确指出以下局限：

1. **运动建模不完整**：当前模型仅关注身体运动，未包含手部和面部精细运动建模，限制了其在需要全身表达的场景中的适用性。
2. **数据规模与泛化**：训练数据规模有限，在极端未见任务组合上的零样本泛化性能尚待验证。论文虽展示了部分零样本能力，但未提供系统性的量化评估。
3. **计算资源需求**：模型训练需要 8 块 NVIDIA A40 GPU，较高的资源门槛可能限制其在小规模研究或应用场景下的推广。
4. **多任务负迁移**：尽管协同学习显著缓解了任务冲突，但消融实验中仍可观察到多任务训练对某些指标的轻微负面影响，未来可能需要更动态的任务调度策略来进一步缓解负迁移现象。

### 超参数敏感性

论文在附录中报告了关键超参数 λ（Eq. 4 中重建损失的权重）的敏感性分析（**Table 18**）。实验表明，λ=0.2 在文本-运动任务上达到了 RPrecision 与 FID 的最佳平衡，验证了在离散 token 空间与连续运动空间之间进行适度权衡的重要性。

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/023_Table_18.jpg]]
*Table 18: Hyper-parameter analysis of λ. Comparison of Text-to-Motion on Motion-X [29] with different values of λ. For this ablation study, M3GPT is trained solely on the text-to-motion task to examine the impact of λ. This study is conducted during the pre-training stage*

### 方法谱系与知识库定位

M3GPT 处于多模态运动生成与理解的交叉点，其方法谱系可追溯至以下关键基线：

- **运动离散化**：继承了将连续运动压缩为离散 token 的思路，与 **TM2D**、**MotionGPT** 等方法共享技术基础，但 M3GPT 进一步将音乐也纳入统一词汇表。
- **语言模型驱动生成**：采用 T5 作为主干，与 **MotionGPT** 等运动-语言模型类似，但 M3GPT 引入了原始运动空间的联合优化，这是其区别于纯离散 token 空间建模的关键创新。
- **扩散模型对比**：与扩散模型基线 **MDM** 和掩码 Transformer **MoMask** 相比，M3GPT 以自回归语言模型范式实现了可比的文本-运动生成质量，同时天然支持更多样的运动理解任务。
- **舞蹈生成**：与专用舞蹈生成方法 **TM2D**、**UDE** 相比，M3GPT 通过多任务协同学习实现了更优的音乐-舞蹈生成质量，且具备舞蹈-音乐反向生成能力。

总体而言，M3GPT 在统一多模态运动理解与生成框架中引入了“文本桥梁”协同学习与“双空间联合优化”两个关键机制，有效缓解了多任务训练冲突，为构建更通用的运动智能体提供了可行路径。

### 补充图表

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/002_Table_1.jpg]]
*Table 1: Comparison of recent multimodal, multitask methods across various motion comprehension and generation tasks. T2M: text-to-motion; M2T: motion-to-text; A2D: music-to-dance; D2A: dance-to-music; M2M: motion-to-motion that includes motion prediction and motion in-between. Random M, Random T, and Random A represent the unconstrained generation of motion, text, and music3, respectively*

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/025_Figure_7.jpg]]
*Figure 7: Qualitative comparisons for text-to-motion task and music-to-dance task. (a) refers to the qualitative comparison between Real, MDM, MoMask and M3GPT on text-to-motion task. The red words and boxes highlight the misaligned motions. The results demonstrate that our M3GPT shows good text understanding for motion generation. (b) refers to the qualitative comparison between Bailando and M3GPT on music-to-dance task. The input is an 5-second-long piece of music in the Break style*

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/009_Figure_3.jpg]]
*Figure 3: Qualitative results for long-term dance and music-text conditioned dance generation of M3GPT*

![[assets/figures/papers/paper_list_l1913_An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and/figures/024_Figure_6.jpg]]
*Figure 6: The qualitative results for different motion comprehension and generation tasks*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

M3GPT 处于“多模态运动理解与生成”这一交叉领域，其设计同时回应了单任务模型能力受限、以及现有多任务框架协同不足的双重瓶颈。与相关工作的关系可从三个维度梳理。

**单任务运动生成基线。** 在文本到运动（Text-to-Motion）任务上，M3GPT 的直接对比对象包括扩散模型 **MDM**（Tevet et al., 2023）和掩码运动 Transformer **MoMask**（Guo et al., 2024）。这些方法在各自专精的任务上表现强劲，但其架构天然局限于“文本→运动”的单一映射，无法处理运动到文本、运动预测、运动插值等反向或序列任务。M3GPT 通过将运动离散化为 token 并纳入语言模型的自回归框架，使得同一模型可以统一执行文本到运动、运动到文本、运动预测、运动插值等六类核心任务（Table 1），从根本上突破了单任务模型的能力边界。

**多模态舞蹈/运动生成基线。** 在音乐到舞蹈（Music-to-Dance）任务上，**TM2D** 和 **UDE** 是典型的多模态基线。TM2D 尝试同时处理文本到运动和音乐到舞蹈，但缺乏统一的表示空间，导致两个任务在联合训练时相互干扰。UDE 专注于统一舞蹈生成，但其任务覆盖范围较窄。M3GPT 的关键改进在于：利用文本作为跨模态桥梁，构建辅助的音乐到文本（A2T）和文本到舞蹈（T2D）任务，使得音乐和舞蹈模态通过文本语义空间建立间接对齐。消融实验（Table 2）表明，加入这两个辅助任务后，音乐到舞蹈的 FID_k 下降近 10 个点，验证了文本桥接策略对缓解多任务冲突的有效性。

**统一运动-语言模型基线。** 与 M3GPT 最接近的同期工作是 **MotionGPT**（Jiang et al., 2023）。两者都采用“运动 tokenizer + 语言模型”的范式，但存在关键差异。MotionGPT 仅在离散 token 空间优化语言模型，运动解 tokenizer 保持冻结。M3GPT 则额外引入原始运动空间的 L1 重建损失（Eq. 4），联合优化 LLM 与运动解 tokenizer。Table 2 的消融显示，这一联合优化在舞蹈生成上带来显著的 FID_k 下降，同时在文本到运动任务上仅引入极轻微的 FID 增加（<0.003），证明在连续运动空间施加监督信号能够有效提升生成质量，而不会损害语义理解能力。

### 2. 适用边界

M3GPT 的适用边界由其设计选择和数据条件共同决定。

**任务覆盖范围。** 框架当前支持六类核心任务：文本到运动、运动到文本、音乐到舞蹈、舞蹈到音乐、运动预测、运动插值（Figure 1, Table 1）。此外，通过指令微调模板的灵活性，模型展示了零样本泛化能力，例如音乐+文本联合条件舞蹈生成（Figure 3）。然而，这些泛化能力目前仅在有限的任务组合上得到验证，极端未见任务组合（如音乐+文本+语音联合控制）的性能尚不明确。

**运动表示范围。** 模型当前仅关注身体运动，未包含手部和面部建模。这意味着 M3GPT 不适用于需要精细手部交互（如手语、乐器演奏）或面部表情同步（如对话场景中的微表情）的应用场景。这一限制源于训练数据本身缺少手部和面部标注，而非架构层面的根本约束。

**数据与计算门槛。** 模型训练需要 8 块 NVIDIA A40 GPU，数据规模受限于公开数据集（Motion-X、AIST++、FineDance）。在小规模场景或数据稀缺的特定领域（如专业舞蹈流派、非标准人体运动）中，直接迁移可能面临性能退化。

### 3. 局限与开放问题

**已确认的局限。**

- **身体建模不完整：** 未包含手部和面部，限制了全身动作生成的完整性。
- **数据规模有限：** 当前训练集规模可能不足以覆盖运动风格的多样性，未来需要更大规模的多模态数据集以增强泛化能力。
- **零样本泛化未充分验证：** 虽然展示了初步的零样本能力，但在极端未见任务组合上的鲁棒性尚待系统评估。
- **计算资源需求高：** 8 块 A40 GPU 的训练成本可能限制小团队或小规模场景的复现与应用。

**值得关注的开放问题。**

- **模态扩展的极限：** 统一词汇表当前仅覆盖文本、运动、音乐三种模态。如何将这一框架扩展到图像、视频、语音等其他模态，是通向真正通用多模态运动智能的关键问题。
- **负迁移的深层机制：** 多任务训练中观察到的负迁移现象（Table 2 中单任务训练优于直接多任务联合训练），是否可以通过更动态的任务调度策略（如基于梯度的任务权重自适应调整）进一步缓解，是一个值得探索的方向。
- **精细运动建模：** 手部和面部运动涉及更高维度的自由度与更复杂的时空依赖，现有 VQ-VAE 压缩框架能否直接扩展，还是需要专门的分层 tokenizer 设计，目前尚无定论。
- **评估体系的完备性：** 当前评价指标（FID、R-Precision 等）主要关注运动质量和文本对齐度，缺乏对运动多样性、风格一致性、音乐节拍同步性的精细度量，评估体系本身仍有改进空间。

## 原文 PDF

![[paperPDFs/NEURIPS_2024/An_Advanced_Multimodal_Multitask_Framework_for_Motion_Comprehension_and_Generation.pdf]]
