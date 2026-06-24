---
title: Being M0 Scaling Motion Generation Models with Million Level Human Motions
type: paper
paper_level: A
venue: ICML
year: 2025
pdf_ref: paperPDFs/ICML_2025/Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions.pdf
aliases:
- BM
- BMSMGMMLHM
tags:
- ICML_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 同时扩大训练数据规模（从2万逐步增至120万）与模型参数量（从355M至13B），并引入2D无查找量化（2D-LFQ）及保留完整旋转信息的SMPL-D135特征，是突破瓶颈的核心因素。
primary_logic: 将运动序列重构为单通道2D图像，通过逐维标量二值化实现无查找的极大量化码本，既能保留关节级运动细节，又能避免传统VQ的码本坍塌；配合百万级运动和分层文本描述，使大语言模型（LLM）首次在运动模态上展现出清晰的缩放定律与显著的分布外泛化。
claims:
- With LLaMA2-13B, increasing training data from 0.02M (HumanML3D) to 1.2M (MotionLib-full) improves MotionLib-eval R@1 from 0.061 to 0.185.
- 2D-LFQ achieves FID 0.295 on Motion-X, whereas 1D-LFQ gives 2.783; it also surpasses VQ and RVQ on larger datasets.
- Hierarchical part-level descriptions improve R@1 and R@3 by 0.004 over single-level descriptions on Motion-X-eval.
- Instruction tuning with 900K refined examples increases R@1 from 0.471 to 0.488 on Motion-X-eval.
---

# Being M0 Scaling Motion Generation Models with Million Level Human Motions

> [!tip] 核心洞察
> 将运动序列重构为单通道2D图像，通过逐维标量二值化实现无查找的极大量化码本，既能保留关节级运动细节，又能避免传统VQ的码本坍塌；配合百万级运动和分层文本描述，使大语言模型（LLM）首次在运动模态上展现出清晰的缩放定律与显著的分布外泛化。

| 字段 | 内容 |
|------|------|
| 中文题名 | Being-M0：利用百万级人体运动扩展运动生成模型 |
| 英文题名 | Being M0 Scaling Motion Generation Models with Million Level Human Motions |
| 会议/期刊 | ICML 2025 |
| Links |  [paper](https://arxiv.org/abs/2410.03311)|
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Being-M0 |
| Dataset | HumanML3D, Motion-X-eval, MotionLib-eval, UNSEEN-90K |

> [!tip] 效果简介
> - HumanML3D 上，R@1 0.528 (Being-M0-LFQ) vs 0.525 (LMM) (+0.003)。
> - Motion-X-eval 上，R@1 0.486 (LLaMA3-8B, 1.2M data) vs 0.472 (GPT-2 355M, 1.2M data) (+0.014)。
> - MotionLib-eval 上，R@1 0.185 (LLaMA2-13B, 1.2M data) vs 0.166 (GPT-2 355M, 1.2M data) (+0.019)。

## 概述

**问题瓶颈**：现有文本-动作生成模型长期受困于两个相互强化的短板——**训练数据规模极小**（最大仅约8万条）与**运动表征能力不足**。传统VQ（Vector Quantization）分词器信息损失严重且易发生码本崩溃，导致模型在多样化及分布外（OOD）动作上泛化性能骤降。当面对包含百万级运动概念的MotionLib时，现有方法几乎完全失效（Figure 1 TOP）。

**核心思路**：Being-M0提出了一套系统性的“缩放”方案——**同时扩大数据规模与模型容量**，并重新设计运动表征。其核心洞察是将运动序列重构为单通道2D图像（$\bar{\mathcal{M}} \in \mathbb{R}^{T \times D \times 1}$），通过**2D无查找量化（2D-LFQ）**实现逐维标量二值化，使码本规模至少扩大两个数量级，从根本上规避了传统VQ的码本坍塌问题。配合保留完整旋转信息的**SMPL-D135**特征与分层文本描述，首次让大语言模型（LLM）在运动模态上展现出清晰的缩放定律。

**决定性证据**：
- 将LLaMA2-13B的训练数据从0.02M（HumanML3D）增至1.2M（MotionLib-full），MotionLib-eval上的R@1从0.061跃升至0.185（Table 2），验证了数据缩放的因果效应。
- 2D-LFQ在Motion-X上取得FID 0.295，而1D-LFQ为2.783（Table 14）；在大规模数据上显著超越VQ与RVQ（Table 8），证明表征创新是突破瓶颈的关键。
- 在分布外测试集UNSEEN-90K上，使用MotionLib训练的模型R@1达0.098，远超仅用HumanML3D的0.034（Table 4），展现了前所未有的OOD泛化能力。

**方法定位**：Being-M0属于**自回归离散词元生成**范式，采用解码器仅有的LLM骨干（如LLaMA2/3）将运动视为“外语”进行序列建模。其管线包含运动分词器（2D-LFQ）、LLM骨干、指令微调模块与运动解码器四个核心组件，通过两阶段训练（全量MotionLib预训练实现运动-文本对齐 + 90万条指令微调提升指令跟随能力）完成。

**主要结果**：在HumanML3D上以HM3D-Format特征公平对比，Being-M0-LFQ取得R@1 0.528，与现有最优方法LMM（0.525）持平（Table 3）。在更大规模的Motion-X-eval上，LLaMA3-8B配合1.2M数据达到R@1 0.486（Table 2）。指令微调进一步将R@1从0.471提升至0.488（Table 5），分层描述相比单层描述带来0.004的R@1/R@3增益（Table 6）。

**局限与开放问题**：当前评估器仅在约2万条数据上训练，泛化性不足，可能无法可靠评估大规模模型；运动分词器表示容量仍有限（1024词元），导致大模型收敛较慢；静态/合成数据的辅助效果有限。未来方向包括设计更鲁棒的评估指标、扩展分词器至3D量化，以及探索缩放定律的极限。

## 背景与动机

### 运动生成的数据与表征瓶颈

文本驱动的人体运动生成（Text-to-Motion）旨在根据自然语言描述合成逼真的三维人体动作序列，在游戏、影视、虚拟人等领域具有广泛应用。近年来，扩散模型与自回归模型在该任务上取得了显著进展，代表性工作包括 **MLD**、**MotionDiffuse**、**ReMoDiffuse**、**Fg-T2M++** 以及 **LMM** 等。然而，这些方法普遍面临两个核心瓶颈：

**数据规模受限。** 现有模型几乎全部在 HumanML3D（约2万条）或 Motion-X（约8万条）等小规模数据集上训练与评估。相比之下，视觉与语言领域早已进入百万级乃至十亿级数据驱动的缩放时代。当模型面对分布外（Out-of-Distribution, OOD）的多样化动作概念时——例如 MotionLib 中涵盖的户外极限运动、复杂多人交互等场景——现有方法的泛化性能急剧下降（Figure 1 TOP）。这一现象揭示出：运动生成领域长期缺乏一个与 ImageNet 规模相当的基础数据集，严重制约了模型对长尾动作的理解与生成能力。

**运动表征能力不足。** 主流方法通常采用 VQ-VAE 将连续运动序列压缩为离散词元（token），再交由生成模型进行自回归或扩散建模。然而，传统矢量量化（Vector Quantization, VQ）存在两个固有问题：其一，小规模码本（如 512 或 1024 个码字）不可避免地造成关节级运动细节的信息损失；其二，训练过程中容易出现“码本崩溃”（codebook collapse），即大量码字未被充分利用，进一步削弱表征容量。此外，广泛使用的 H3D-Format 特征仅保留关节位置和 Y 轴旋转，丢弃了原始的完整旋转信息，导致生成动作的物理合理性与细节保真度不足。

### 核心动机与研究问题

上述双重瓶颈引出了本文的核心研究问题：**能否通过同时扩展数据规模与模型容量，并设计更强大的运动表征与量化方法，使运动生成模型展现出类似大语言模型的缩放定律（Scaling Law）？**

具体而言，本文试图回答以下子问题：
1. 构建一个百万级运动数据集能否显著提升模型在分布外动作上的泛化能力？
2. 如何设计一种无查找（lookup-free）的量化机制，在避免码本崩溃的同时将运动码本扩大至少两个数量级？
3. 将运动视为“外语”并集成到解码器仅（decoder-only）大语言模型（LLM）中，能否借助 LLM 的规模化能力实现更优的文本-运动对齐？

### 方法概览

为回应上述问题，本文提出 **Being-M0** 框架，其核心设计包含三个层面：

- **MotionLib 数据集**：首个百万级运动数据集，包含超过 120 万条运动序列及 240 万条分层文本描述，规模至少为现有最大数据集的 15 倍（Table 1）。数据经过采集、分层描述生成、运动与描述精炼等多阶段处理，覆盖从室内到户外、从单人至多人的丰富场景（Figure 2）。

- **2D 无查找量化（2D-LFQ）**：将运动序列重构为单通道二维图像 $\bar{\mathcal{M}} \in \mathbb{R}^{T \times D \times 1}$，通过对特征向量的每一维进行标量二值化（$Q(z_i) = -\mathbf{1}\{z_i \leq 0\} + \mathbf{1}\{z_i > 0\}$）实现无码本查找的量化，码本规模可扩展至 $2^d$，较传统 VQ 提升至少两个数量级。同时采用 SMPL-D135 特征完整保留根旋转、关节旋转等 135 维运动信息。

- **LLM 骨干与两阶段训练**：将运动词元视为大语言模型的扩展词汇，第一阶段在 MotionLib 全量数据上进行运动-文本对齐预训练，第二阶段利用 250+ 指令模板和 Gemini-Pro 精炼的 90 万条指令进行指令微调，使模型具备指令跟随能力。

这一设计使得 Being-M0 首次在运动模态上展现出清晰的缩放定律：随着数据量从 0.02M 增至 1.2M、模型从 355M 扩展至 13B，生成质量（R@1、FID）持续提升（Table 2），并在分布外评测集 UNSEEN-90K 上取得显著增益（R@1 从 0.034 提升至 0.098，Table 4）。

## 核心创新

Being-M0 的核心创新并非单一算法改进，而是一套系统性的“数据—表征—量化—训练”协同扩展方案，旨在突破现有文本-动作生成模型在数据规模和运动表征能力上的双重瓶颈。

### 1. 百万级运动数据集 MotionLib

现有模型的最大训练集仅约 8 万条（Motion-X），严重制约了模型对多样化及未见动作的泛化能力。Being-M0 构建了 **MotionLib**——首个百万级运动数据集，包含超过 240 万条运动-文本对，规模达以往最大数据集的 **15 倍以上**（Table 1）。

MotionLib 的构建包含三项关键设计：
- **分层文本描述**：为每条运动生成“身体级总结 + 部分级（上肢/下肢）详细描述”，替代传统的单一全身描述。消融实验表明，分层描述在 Motion-X-eval 上将 R@1 和 R@3 提升了 0.004（Table 6）。
- **运动与描述精炼**：利用基于强化学习的精炼策略 $\pi_{\mathrm{refine}}$ 修正原始运动中的物理不合理之处，并通过 Gemini-Pro 优化文本指令。
- **指令微调数据集**：基于 250+ 模板和 90 万条精炼指令，构建了大规模指令微调数据，使模型具备更强的指令跟随能力。

### 2. 无信息损失的运动表征 SMPL-D135

传统方法普遍采用 H3D-Format 特征（仅保留关节位置和 Y 轴旋转），丢失了原始旋转信息。Being-M0 改用 **SMPL-D135** 特征，每帧编码为 135 维向量：
- **根节点（9D）**：6D 旋转 $r_{rot} \in \mathbb{R}^6$、2D XZ 平面速度 $r_{xz}^v \in \mathbb{R}^2$、1D 高度 $r^y \in \mathbb{R}$
- **身体关节（126D）**：21 个关节 × 6D 旋转

该表征完整保留了 SMPL 模型的旋转信息，在重建任务上显著优于 H3D-Format 等表征（Table 7）。

### 3. 2D 无查找量化（2D-LFQ）

传统 VQ 面临码本规模小（通常 512/1024）和码本崩溃问题。Being-M0 将运动序列重构为单通道 2D 图像 $\bar{\mathcal{M}} \in \mathbb{R}^{T \times D \times 1}$，并引入 **2D Lookup-Free Quantization**：

$$Q(z_i) = \arg\min_{c_{ik}} ||z_i - c_{ik}|| = -\mathbf{1}\{z_i \leq 0\} + \mathbf{1}\{z_i > 0\}$$

$$\mathrm{Index}(z) = \sum_{i=1}^{d} 2^{i-1} \mathbf{1}\{z_i > 0\}$$

其核心机制是将特征向量的每一维独立二值化至 {-1, +1}，通过笛卡尔积隐式构建码本 $\mathbb{C} = \times_{i=1}^{d} \{-1, 1\}$。这一设计带来三重优势：
- **码本容量指数级扩展**：码本规模至少扩大两个数量级，且利用率随码本增大持续提升，彻底避免了 VQ/RQ 的码本坍塌（Figure 11 RIGHT）。
- **重建质量跃升**：在 Motion-X 上，2D-LFQ 的 FID 为 0.295，而 1D-LFQ 高达 2.783（Table 14）；在跨数据集泛化上，2D-LFQ 同样显著优于 VQ 和 RVQ（Table 8）。
- **保留部件级细节**：2D 结构使量化过程能捕获关节间的空间关系。

### 4. 将运动作为外语的 LLM 集成范式

Being-M0 将运动视为一种“外语”，通过以下方式集成到自回归 LLM 中：
- 将运动分词器的离散码本作为额外词汇表注入 LLM
- 引入特殊词元标记运动序列边界
- 采用两阶段训练：第一阶段在完整 MotionLib 上建立运动-文本对齐，第二阶段利用 90 万条指令进行指令微调

实验证实，**Decoder-only 架构**（GPT-2 Medium）在 MotionLib-eval 上的 R@1 为 0.166，优于 Encoder-Decoder 架构的 T2M-GPT（0.161，Table 13）；**全参数微调**的 R@1 为 0.166，显著优于 LoRA 的 0.157（Table 10）；指令微调将 Motion-X-eval 的 R@1 从 0.471 提升至 0.488（Table 5）。

### 5. 缩放定律的首次验证

Being-M0 首次在运动生成领域展示了清晰的缩放定律：以 LLaMA2-13B 为骨干，当训练数据从 0.02M（HumanML3D）增至 1.2M（MotionLib-full）时，MotionLib-eval 的 R@1 从 0.061 跃升至 0.185（Table 2）。同时，模型参数从 355M 扩展至 13B 也带来一致的性能增益。在分布外泛化测试中，使用 MotionLib 训练的模型在 UNSEEN-90K 上的 R@1 达到 0.098，远超使用 HumanML3D 训练的 0.034（Table 4）。

> **注意**：2D-LFQ 在小规模数据集（如 HumanML3D）上可能略逊于 RQ-VAE，其优势主要体现在大规模数据场景（Section C.2.1）。这一局限性提示该方法的设计哲学是“为规模而生”。

## 整体框架

Being-M0 将运动生成建模为一种“外语”翻译任务，其整体框架由**运动分词器（Motion Tokenizer）**、**大语言模型（LLM）骨干**与**运动解码器（Motion Decoder）**三大模块串联构成，并通过**两阶段训练**实现百万级运动-文本对齐与指令跟随生成（Figure 3）。

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/004_Figure_3.jpg]]
*Figure 3: Overview of our large motion model named Being-M0, which can be divided into two stages. In the first stage (left), we pre-train a motion VQ-VAE to quantify motion sequences into tokens. In the second stage (right), we fine-tune an autoregressive language model to predict motion tokens*

### 核心设计思路

框架的核心洞察在于：现有 VQ 压缩方案将运动序列映射为 1D 词元序列（大小为 $\lfloor T / \alpha \rfloor \times d$），造成关节级细节丢失与码本坍塌；同时，传统运动数据集规模（最大约 8 万条）远不足以支撑大模型的缩放定律。Being-M0 从两个维度突破这一瓶颈：

1. **表征层面**：将运动序列重构为单通道 2D 图像 $\bar{\mathcal{M}} \in \mathbb{R}^{T \times D \times 1}$，并引入 2D 无查找量化（2D-LFQ），通过逐维标量二值化实现极大量化码本（至少扩大两个数量级），在保留部件级运动细节的同时避免传统 VQ 的码本崩溃。
2. **数据与模型层面**：构建百万级运动数据集 MotionLib（最多 120 万条，15 倍于以往最大数据集），并采用参数量从 355M 到 13B 的 decoder-only LLM 作为自回归生成器，首次在运动模态上展现出清晰的缩放定律。

### 模块构成与数据流

**1. 运动分词器（Motion Tokenizer / 2D-LFQ）**

输入为原始运动序列，首先编码为 SMPL-D135 特征（135 维：根节点 9D + 21 个身体关节各 6D 旋转），完整保留旋转信息。随后将特征序列重塑为 2D 形式，通过 2D-LFQ 进行量化：

$$Q(z_i) = \arg\min_{c_{ik}} ||z_i - c_{ik}|| = -\mathbf{1}\{z_i \leq 0\} + \mathbf{1}\{z_i > 0\}$$

该量化器对特征向量的每一维进行二值化（映射至 -1 或 +1），无需传统码本查找。词元索引通过下式计算：

$$\mathrm{Index}(z) = \sum_{i=1}^{d} 2^{i-1} \mathbf{1}\{z_i > 0\}$$

量化后的离散词元序列作为后续 LLM 的生成目标。解码时，运动解码器将离散词元映射回连续运动序列。

**2. LLM 骨干（自回归生成器）**

框架将运动视为一种“外语”，通过引入 K 个离散运动码本词元作为 LLM 的额外词汇表，并添加两个特殊词元标记运动序列的起止。生成过程以文本描述为条件，自回归预测运动词元序列：

$$\mathcal{L}(\Theta) = - \sum_{j=1}^{L} \log P_{\Theta}(y_j \mid desc, \hat{y}_{1:j-1})$$

实验验证了 decoder-only 架构在运动-文本对齐上的优势：在 MotionLib-eval 上，GPT-2 Medium（decoder-only）的 R@1 达到 0.166，优于 encoder-decoder 架构的 T2M-GPT（0.161）（Table 13）。

**3. 运动解码器（Motion Decoder）**

将 LLM 生成的离散词元序列解码回连续运动表示，最终输出可驱动的人体运动序列。

### 两阶段训练策略

**第一阶段：运动-文本对齐预训练**。在完整 MotionLib 数据集上进行全参数微调，使 LLM 学习运动词元与分层文本描述之间的基本关联。消融实验表明，全参数微调的 R@1（0.166）显著优于 LoRA（0.157），且从零开始训练远不及基于预训练 LLM 的微调（R@1 0.213 vs 0.042，Table 10、Table 11）。

**第二阶段：指令微调**。构建包含 250+ 模板并经 Gemini-Pro 精炼的 90 万条指令数据，进一步提升模型的指令跟随能力。在 Motion-X-eval 上，指令微调使 R@1 从 0.471 提升至 0.488（Table 5）。

### 输入输出流总结

- **输入**：分层文本描述（身体级总结 + 部分级详细描述）
- **处理**：LLM 以文本为条件自回归生成运动词元序列
- **输出**：经运动解码器还原的连续人体运动序列

该框架的模块化解耦设计使得运动分词器与 LLM 骨干可独立扩展——2D-LFQ 的码本利用率随码本增大持续提升（Figure 11 RIGHT），而 LLM 的生成质量随模型参数量与数据规模同步增长（Table 2）。

## 核心模块与公式推导

### 整体框架：运动作为外语

Being-M0 将运动生成视为序列建模问题，核心思路是将**运动视为一门“外语”**，通过运动分词器（Motion Tokenizer）将连续运动序列转换为离散词元，再交由因果语言模型（LLM）自回归生成。整个框架分为两个阶段（Figure 3）：

1. **第一阶段**：预训练运动 VQ-VAE，将运动序列量化为离散词元。
2. **第二阶段**：微调自回归 LLM，以文本描述为条件预测运动词元序列。

### 关键模块一：SMPL-D135 运动特征

传统方法（如 HumanML3D 的 H3D-Format）仅保留关节位置和 Y 轴旋转，丢失了原始旋转信息。Being-M0 采用 **SMPL-D135** 特征，每帧编码为 $\mathbf{m} \in \mathbb{R}^{135}$，完整保留旋转信息（Section 4.2, Table 7）：

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/011_Table_7.jpg]]
*Table 7: Ablation results of different motion features. Here, “FPS” denotes the speed to recover original motion information (e.g., rotation)*

- **根节点（9D）**：6D 旋转 $\mathbf{r}_{rot} \in \mathbb{R}^6$、2D XZ 平面速度 $\mathbf{r}_{xz}^v \in \mathbb{R}^2$、1D 高度 $r^y \in \mathbb{R}$。
- **身体关节（126D）**：21 个关节 × 6D 旋转表示。

消融实验（Table 7）表明，SMPL-D135 在重建 FID 和 MPJPE 上均优于 H3D-Format 等表征，同时保留了完整旋转信息。

### 关键模块二：2D 无查找量化（2D-LFQ）

传统向量量化（VQ）存在码本规模小（如 512/1024）、码本坍塌等问题。Being-M0 引入 **2D Lookup-Free Quantization（2D-LFQ）**，核心创新在于：

1. **运动序列重塑为 2D 图像**：将运动序列表示为单通道 2D 图像 $\bar{\mathcal{M}} \in \mathbb{R}^{T \times D \times 1}$（时间 × 特征维度），而非传统的 1D 序列（Section 1）。

2. **逐维标量二值化**：对特征向量 $\mathbf{z}$ 的每一维独立量化，无需码本查找：

   $$Q(z_i) = \arg\min_{c_{ik}} \|z_i - c_{ik}\| = -\mathbf{1}\{z_i \leq 0\} + \mathbf{1}\{z_i > 0\}$$

   其中 $c_{ik} \in \{-1, 1\}$，量化码本 $\mathbb{C}$ 为各维二值集合的笛卡尔积：$\mathbb{C} = \times_{i=1}^{d} C_i$，$C_i = \{-1, 1\}$（Section 4.2, Equation 2）。

3. **词元索引计算**：根据二值量化结果计算整数词元索引：

   $$\mathrm{Index}(\mathbf{z}) = \sum_{i=1}^{d} 2^{i-1} \mathbf{1}\{z_i > 0\}$$

   该索引直接作为 LLM 词汇表中的离散词元 ID。

**核心优势**：码本规模从传统 VQ 的 $K$（如 512）扩展至 $2^d$（$d$ 为特征维度），扩大至少两个数量级，且从根本上避免了码本坍塌（Figure 11 RIGHT, Section 5.3）。在 Motion-X 上，2D-LFQ 的 FID 为 0.295，而 1D-LFQ 为 2.783（Table 14），优势显著。

### 关键模块三：自回归训练损失

在第二阶段，LLM 以文本描述和已生成的运动词元为条件，自回归预测下一个运动词元。训练目标为负对数似然损失（Section 4.1, Equation 1）：

$$\mathcal{L}(\Theta) = - \sum_{j=1}^{L} \log P_{\Theta}(y_j \mid desc, \hat{y}_{1:j-1})$$

其中：
- $\Theta$：LLM 模型参数
- $desc$：分层文本描述（身体级总结 + 部分级细节）
- $\hat{y}_{1:j-1}$：前 $j-1$ 个预测的运动词元
- $y_j$：第 $j$ 个真实运动词元
- $L$：运动词元序列长度

### 关键模块四：指令微调

为进一步提升指令跟随能力，Being-M0 构建了包含 **250+ 指令模板**和 **90 万条精炼指令**（经 Gemini-Pro 优化）的微调数据集（Section 4.1）。消融实验（Table 5）表明，指令微调使 Motion-X-eval 上的 R@1 从 0.471 提升至 0.488。

### 方法谱系与知识库定位

| 维度 | 传统方法 | Being-M0 创新 |
|------|---------|--------------|
| 运动特征 | H3D-Format（丢失旋转） | SMPL-D135（完整 6D 旋转） |
| 量化方式 | VQ/RVQ（小码本，易坍塌） | 2D-LFQ（无查找，码本扩大百倍） |
| 数据规模 | 最多 8 万条 | 120 万条（15×） |
| 文本粒度 | 单一全身描述 | 分层描述（身体级 + 部分级） |
| 训练策略 | 常规预训练 | 两阶段：对齐预训练 + 指令微调 |

**架构选择依据**：Decoder-only LLM（如 GPT-2 355M）在 MotionLib-eval 上的 R@1 为 0.166，优于 Encoder-Decoder 架构的 T2M-GPT（0.161）（Table 13），验证了因果语言模型在运动生成任务上的优势。

### 已知局限与待验证点

1. **分词器容量瓶颈**：当前 2D-LFQ 的码本规模仍有限（如 1024 个词元），大模型收敛较慢，且无法充分捕捉细粒度运动（Section C.1.5）。**需进一步验证**更大码本（如 3D 量化）的可行性。

2. **小数据集表现**：2D-LFQ 在 HumanML3D 等小规模数据集上可能略逊于 RQ-VAE，其优势主要体现在大规模数据上（Section C.2.1）。**此结论需手动核实**具体数值对比。

3. **评估器泛化性**：当前 R-Precision 和 FID 依赖在约 2 万条数据上训练的轻量级运动编码器，其在大规模模型上的可靠性存疑（Section C.4）。**该局限可能影响所有对比结果的公平性**。

### 补充图表

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/012_Table_8.jpg]]
*Table 8: Ablation results of different motion tokenizer trained on HumanML3D on the motion reconstruction task*

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/026_Table_14.jpg]]
*Table 14: Ablation of 2D motion quantization vs. its 1D version*

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/023_Table_13.jpg]]
*Table 13: Ablation results of Encoder-Decoder vs. Decoder-only architecture*

## 实验与分析

### 核心发现：运动生成的缩放定律

Being-M0的核心实验贡献在于首次在运动生成领域验证了清晰的缩放定律（Scaling Law）：**同时增大模型参数量和训练数据规模，能够持续提升文本-动作对齐质量与分布外泛化能力**。Table 2汇总了不同骨干LLM与数据规模下的关键指标：

- **数据规模效应**：以LLaMA2-13B为例，当训练数据从0.02M（HumanML3D规模）增至1.2M（MotionLib-full）时，MotionLib-eval上的R@1从0.061提升至0.185，FID从10.443降至6.221。这一趋势在所有模型规模上一致成立。
- **模型规模效应**：在1.2M数据下，从GPT-2（355M）到LLaMA2-13B，Motion-X-eval上R@1从0.472提升至0.491，MotionLib-eval上FID从6.936降至6.221。LLaMA3-8B在MotionLib-eval上取得最佳FID（6.029），但R@1略低于LLaMA2-13B（0.486 vs 0.491），提示参数量与架构代际之间存在复杂交互。
- **数据效率**：在0.02M数据下，从零训练（R@1 0.042）远逊于微调预训练模型（R@1 0.213，Table 11），说明LLM先验知识对极小运动数据场景至关重要。

**关键证据强度**：Table 2为全文核心结果表，置信度高（0.95）。需注意，当前评估器（R-Precision和FID所用的运动编码器）仅在约2万条数据上训练，其泛化性存疑，可能低估大模型在MotionLib上的真实性能（见局限性声明）。

### 分布外泛化：UNSEEN-90K的检验

Table 4揭示了数据规模对分布外（OOD）泛化的决定性作用。在UNSEEN-90K（包含训练集未见的动作类别）上，仅用HumanML3D（约2万条）训练的模型R@1仅为0.034；当使用MotionLib的11个子集（#11，约110万条）时，R@1跃升至0.098（+0.064，相对提升近2倍）。这一消融直接证实了Figure 1中的动机：**小规模数据训练的模型在面对多样化/未见动作时泛化崩溃，而百万级数据能显著缓解此问题**。

### 指令微调与分层描述的增益

两阶段训练策略中的指令微调（Instruction Tuning）带来一致但温和的提升（Table 5）：在Motion-X-eval上，R@1从0.471增至0.488（+0.017），FID从0.365降至0.344。这表明90万条精炼指令（由Gemini-Pro优化）有效增强了模型的指令跟随能力。

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/008_Table_5.jpg]]
*Table 5: Ablation results of motion instruction tuning*

分层文本描述（Hierarchical Description）的贡献更为微妙（Table 6）：相较于单一全身描述，身体级总结+部分级（上肢/下肢）详细描述在Motion-X-eval上仅将R@1和R@3各提升0.004。增益虽小，但方向一致，暗示细粒度空间对齐信息对LLM的运动理解有边际贡献，可能受限于当前分词器的表示容量。

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/010_Table_6.jpg]]
*Table 6: Ablation results of hierarchical description vs. single-level description*

### 运动分词器：2D-LFQ的决定性优势

2D-LFQ是Being-M0突破VQ瓶颈的关键设计。Table 8与Table 14提供了系统性消融证据：

- **跨数据集泛化**（Table 8）：在HumanML3D上训练的2D-LFQ，于分布外数据集Motion-X上取得FID 0.295，而1D-LFQ为2.783（差距近一个数量级）；在MotionLib上，2D-LFQ的FID为1.051，同样大幅优于1D-LFQ的3.790。VQ和RVQ在OOD数据集上的FID均超过5.0，暴露出严重过拟合。
- **码本利用率**：Figure 11（RIGHT）显示，2D-LFQ的码本利用率随码本增大持续上升，而VQ/RQ在大码本下出现利用率骤降（码本坍塌）。这解释了为何2D-LFQ能支撑至少两个数量级的码本扩展。
- **小数据集上的局限性**：在HumanML3D本身上，2D-LFQ的FID（0.049）略逊于RQ-VAE（0.018，Table 8），说明其优势主要体现在大规模数据场景。

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/024_Figure_11.jpg]]
*Figure 11: LEFT: Training curves with Y-axis denoting R@1 retrieval accuracy. All these models are trained for 300 epochs at most and are evaluated every 1000 steps; RIGHT: Ablation of codebook usage of different quantization methods*

### 运动特征表示：SMPL-D135的保真度

Table 7消融了不同运动特征表示对重建质量的影响。SMPL-D135（135维：6D根旋转+2D速度+1D高度+21关节×6D旋转）在保留完整旋转信息的同时，取得了与H3D-Format（仅Y轴旋转）可比的MPJPE（38.8 vs 38.4），且FPS（恢复原始旋转信息的速度）显著更优。这验证了“无损特征”设计的有效性：**不牺牲旋转完整性即可实现紧凑表示**。

### 架构选择：Decoder-only优于Encoder-Decoder

Table 13对比了Decoder-only（GPT-2 Medium）与Encoder-Decoder（T2M-GPT）架构。在MotionLib-eval上，Decoder-only的R@1为0.166，高于Encoder-Decoder的0.161；FID为6.936 vs 7.125。这支持了将运动视为“外语”直接输入Decoder-only LLM的设计选择，避免了编码器-解码器间的信息瓶颈。

### 微调策略：全参数优于LoRA

Table 10显示，在MotionLib-eval上全参数微调的R@1为0.166，优于LoRA的0.157。这一差距虽不大（+0.009），但在大规模数据下全参数微调的优势更明显，说明运动-文本对齐需要充分调整LLM的全部参数。

### 失败模式与评估局限性

1. **评估器泛化不足**：当前R-Precision和FID依赖的运动评估器仅在约2万条数据上训练，在MotionLib的多样化场景下可能不可靠（论文Section C.4明确指出的局限）。Table 2中部分模型R@1提升与FID下降不完全同步（如LLaMA3-8B的FID最优但R@1非最优），可能部分源于评估器偏差。
2. **分词器容量瓶颈**：2D-LFQ虽大幅扩展了码本，但当前仍仅使用1024个词元（10维二值量化）。论文指出这导致大模型收敛较慢，且无法充分捕捉细粒度运动（Section C.1.5）。
3. **静态数据增益有限**：附录中探索的静态图像辅助训练对动态运动生成提升有限，未被纳入主要贡献（Section C.3）。
4. **小数据集劣势**：2D-LFQ在HumanML3D上略逊于RQ-VAE，说明其设计高度依赖数据规模，在小规模场景下优势不显。

### 与SoTA的公平对比

Table 3在HumanML3D上使用HM3D-Format特征进行公平对比。Being-M0-LFQ取得R@1 0.528，略优于LMM的0.525（+0.003），FID为0.071 vs 0.082。虽优势微弱，但在统一特征下验证了方法的有效性。需注意，HumanML3D仅约2万条数据，远未触及Being-M0的缩放优势区间——其真正价值体现在大规模数据场景。

### 补充图表

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/005_Table_2.jpg]]
*Table 2: Comparisons under different model parameters and data sizes, showing their scaling law for motion generation*

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/006_Table_3.jpg]]
*Table 3: Comparison with existing SoTA methods on HumanML3D. Results marked with ∗ represent values reproduced using the official code, while unmarked results are taken from the original papers. 1 and 2 denote different works with the same model name. For fair comparison, experiments here are conducted using HM3D-Format feature*

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/009_Table_4.jpg]]
*Table 4: Ablation of out-of-domain evaluation on UNSEEN-90K dataset, where #N denotes we use N subsets of MotionLib for training*

![[assets/figures/papers/paper_list_l1911_Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motio/figures/019_Table_10.jpg]]
*Table 10: Ablation results of LoRA tuning vs. full-parameter fine-tuning*

## 方法谱系与知识库定位

### 1. 方法沿革与基线对比

Being-M0 的提出建立在文本驱动人体运动生成领域的两个关键瓶颈之上：**数据规模受限**（此前最大数据集仅约8万条）与**运动表征能力不足**（传统VQ量化存在信息损失与码本崩溃）。其核心突破在于将“缩放定律”从语言/视觉领域迁移至运动模态，通过同时扩大数据与模型规模，并引入2D无查找量化（2D-LFQ）及SMPL-D135特征，实现了显著的分布外泛化能力。

#### 1.1 运动分词器的演进

传统运动生成模型普遍采用基于VQ（Vector Quantization）或RQ（Residual Quantization）的运动分词器，其码本大小通常限制在512或1024，导致对细粒度关节运动的表征能力有限。Being-M0提出的**2D-LFQ**将运动序列重构为单通道2D图像（$T \times D \times 1$），通过逐维标量二值化实现无查找量化：

$$Q(z_i) = \arg\min_{c_{ik}} ||z_i - c_{ik}|| = -\mathbf{1}\{z_i \leq 0\} + \mathbf{1}\{z_i > 0\}$$

这一设计的核心优势在于：码本大小从 $K$ 扩展至 $2^d$，至少提升两个数量级，且无需维护显式码本嵌入，从根本上规避了VQ中常见的码本坍塌问题。实验证据显示，在Motion-X上，2D-LFQ的FID为0.295，而1D-LFQ为2.783（Table 14）；在跨数据集泛化实验中，2D-LFQ在Motion-X和MotionLib上的重建FID与MPJPE均显著优于VQ和RVQ（Table 8）。**需注意**：在小规模数据集（如HumanML3D）上，2D-LFQ可能略逊于RQ-VAE，其优势主要体现在大规模数据场景下（Section C.2.1）。

#### 1.2 运动特征表示的升级

基线方法普遍采用**H3D-Format**特征（仅保留关节位置和Y轴旋转），丢失了原始旋转信息。Being-M0引入**SMPL-D135**特征（135维：6D根旋转 + 2D速度 + 1D高度 + 21关节×6D旋转），完整保留旋转信息，在重建FID和MPJPE上均优于其他表征（Table 7）。这一改进为大规模运动数据的精细建模提供了特征基础。

#### 1.3 生成架构的范式选择

在LLM骨干网络的选择上，Being-M0系统验证了**Decoder-only架构**（如GPT-2 355M, Radford et al., 2019；LLaMA2-7B/13B, Touvron et al., 2023）相较于Encoder-Decoder架构（如**T2M-GPT**, Zhang et al., 2023a）的优势：在MotionLib-eval上，GPT-2 Medium的R@1为0.166，而T2M-GPT为0.161（Table 13）。这一发现与LLM领域“Decoder-only在自回归生成任务中更具扩展性”的共识一致。

#### 1.4 与现有SoTA的公平比较

在HumanML3D基准上，Being-M0-LFQ的R@1达到0.528，略优于**LMM**的0.525（Table 3）。需注意，该比较采用HM3D-Format特征以保证公平性。在更大规模的Motion-X-eval上，LLaMA3-8B配合1.2M数据达到R@1 0.486，显著优于GPT-2 355M的0.472（Table 2）。与**MLD**、**MotionDiffuse**、**ReMoDiffuse**、**Fg-T2M++**等扩散/VAE基线的对比，论文主要在HumanML3D上展开（Table 3），在MotionLib上的泛化对比则通过Figure 1定性展示。

### 2. 适用边界与局限

#### 2.1 评估体系的滞后性

当前文本-动作生成的评测指标（R-Precision、FID）依赖在有限数据（约2万条）上训练的轻量级运动编码器作为评估器。论文明确指出，这些评估器的泛化性不足，可能无法可靠评估大规模模型（Section C.4）。**这是一个系统性问题**：当生成模型的训练数据规模远超评估器的训练数据时，现有指标可能产生误导性结论。

#### 2.2 运动分词器的容量上限

尽管2D-LFQ大幅扩展了码本，但当前实现仍受限于1024个词元的设计，导致大模型收敛较慢，且无法充分捕捉极细粒度的运动差异（Section C.1.5）。如何进一步扩展分词器容量（如引入3D量化）仍是一个开放问题。

#### 2.3 数据质量与模态局限

- **文本噪声**：MotionLib的文本描述虽经GPT-4o精炼，但自发标注仍可能存在不精确之处（Section 3）。
- **静态数据利用**：论文在附录中探索了静态图像数据，但发现其对动态运动的辅助提升有限，不属于主要贡献（Section C.3）。
- **多模态缺失**：当前模型仅处理文本到运动的映射，未涉及音频、场景等多模态条件。

### 3. 开放问题与未来方向

1. **评估指标的重新设计**：如何构建与人类感知一致、且能随数据规模同步扩展的运动生成评估指标？
2. **分词器容量的进一步扩展**：能否引入3D量化或更大规模的无查找码本（如 $2^{16}$ 以上），以捕捉更精细的运动细节？
3. **缩放定律的极限探索**：在更大规模数据（千万级）和模型（百亿参数以上）下，运动生成的缩放曲线是否会遇到新的瓶颈？饱和点在哪里？
4. **部件级可控生成**：当前分层描述仅提供上下肢的粗略区分，如何实现更精细的部件级控制（如仅控制左臂动作）？
5. **多模态条件的融合**：如何有效利用静态图像、音频、场景上下文等辅助模态，突破纯文本条件的性能上限？
6. **合成数据的价值挖掘**：论文初步探索了合成数据（Section C.3），但效果有限。更高质量的合成运动数据能否成为规模化训练的可行路径？

## 原文 PDF

![[paperPDFs/ICML_2025/Being_M0_Scaling_Motion_Generation_Models_with_Million_Level_Human_Motions.pdf]]