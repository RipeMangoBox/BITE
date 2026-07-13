---
title: "ATLAS: Adaptive Transfer Scaling Laws for Multilingual Pretraining, Finetuning, and Decoding the Curse of Multilinguality"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ATLAS_Adaptive_Transfer_Scaling_Laws_for_Multilingual_Pretraining_Finetuning_and_Decoding_the_Curse_of_Multilinguality.pdf
project_link: null
code_link: null
aliases:
- ATSLA
- ATLAS
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "ATLAS fits multilingual scaling laws with an effective data exposure term that separates target-language, transfer-language, and other-language contributions."
primary_logic: "It models repetition saturation and cross-language transfer weights, then uses the fitted law to predict multilingual loss, curse-of-multilinguality scaling, and pretraining versus fine-tuning tradeoffs."
claims:
- "ATLAS improves generalization to unseen multilingual mixtures by explicitly modeling cross-language transfer."
- "The law uses saturation functions to capture diminishing returns from repeated language data."
- "Experiments across 774 training runs report higher R² than CSL and MSL in multilingual scaling settings."
---

# ATLAS: Adaptive Transfer Scaling Laws for Multilingual Pretraining, Finetuning, and Decoding the Curse of Multilinguality

> [!tip] 核心洞察
> 通过显式建模跨语言迁移（尤其是目标语言与最常共采样的3种语言之间的迁移），ATLAS能够显著提升对未见语言混合的泛化能力（R²(M)从0.70提升至0.82），且模型规模扩展比数据扩展更能有效缓解多语言诅咒。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ATLAS：面向多语言预训练、微调及解码多语言诅咒的自适应迁移缩放定律 |
| 英文题名 | ATLAS: Adaptive Transfer Scaling Laws for Multilingual Pretraining, Finetuning, and Decoding the Curse of Multilinguality |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0BkvUY61MX) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | ADAPTIVE TRANSFER SCALING LAW (ATLAS) |
| Dataset | MADLAD-400 (多语言), MADLAD-400 (单语言) |

> [!tip] 效果简介
> - MADLAD-400 (多语言) 上，R² (整体) 为 0.98，对比 0.64 (CSL), 0.67 (MSL)，变化 +0.34 vs CSL, +0.31 vs MSL。
> - MADLAD-400 (多语言) 上，R²(N) (最大模型规模) 为 0.89，对比 -0.99 (CSL), -0.65 (MSL)，变化 +1.88 vs CSL, +1.54 vs MSL。
> - MADLAD-400 (多语言) 上，R²(M) (未见语言混合) 为 0.82，对比 0.61 (CSL), 0.70 (MSL)，变化 +0.21 vs CSL, +0.12 vs MSL。

## 概要

本文提出了**自适应迁移缩放定律（ADAPTIVE TRANSFER SCALING LAW, ATLAS）**，旨在解决多语言预训练、微调及“多语言诅咒”（curse of multilinguality）中的缩放问题。ATLAS通过显式建模跨语言迁移效应和数据重复带来的收益递减，显著提升了缩放定律对未见模型规模、数据量和语言混合的泛化能力。实验基于774次多语言训练实验，覆盖10M-8B模型参数、400+训练语言和48种评估语言，并构建了38×38语言对的跨语言迁移矩阵。ATLAS在多语言设置下整体R²达到0.98，对未见语言混合的泛化R²(M)达到0.82，远超现有基线。



现有缩放定律（如Chinchilla Scaling Law, CSL；Data-Constrained Scaling Law, DCSL；Multilingual Scaling Law, MSL）存在两个关键缺陷：**无法处理多轮数据重复**和**无法建模目标语言语系之外的跨语言迁移效应**。这导致它们对未见模型规模、数据量和语言混合的泛化能力极差。例如，在多语言设置下，CSL对最大模型规模的泛化R²(N)为-0.99，MSL为-0.65，均无法有效预测更大模型的行为。

此外，多语言训练存在“计算效率税”（compute efficiency tax）：使用多语言词汇表或多语言训练集时，每种语言的最优缩放轨迹会向上偏移，尤其对英语影响显著（Figure 1）。同时，随着训练语言数量的增加，目标语言的损失会相对退化，这种退化对更大模型更不敏感（Figure 4）。



## 核心方法与创新机理

ATLAS的核心创新在于将**有效数据暴露项（effective data exposure）**分解为目标语言、迁移语言和其他语言三个独立来源，并引入饱和函数和可学习的迁移权重。具体创新点包括：

1. **数据重复建模**：引入共享重复参数λ的饱和函数S_λ(D; U)，单阶段拟合，对低资源语言更鲁棒，避免了DCSL需要两阶段拟合且要求充足数据的限制。
2. **跨语言迁移显式建模**：将有效数据分解为三项：目标语言数据D_t、迁移语言数据（最多3种最常共采样语言）和其他语言数据D_other，每项均经饱和函数处理并赋予可学习权重。
3. **迁移权重初始化**：迁移权重τ_i从双语迁移分数（BTS）初始化，BTS通过双语共训练实验直接测量语言对之间的正迁移或干扰。



![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_0BkvUY61MX_ATLAS_Adaptiv/figures/001_Figure_1.jpg]]
*Figure 1: Optimal Scaling Trajectories for English, French, Russian, Chinese, Hindi, and Swahili. The law for [monolingual vocabulary, monolingual training]=(—), the law for [multilingual vocabulary, monolingual training]=(- - -), and the law for [multilingual vocabulary, unimax training]=(···). We find (1) per-language optimal scaling trajectories are similar, (2) there is a compute efficiency tax for training with multilingual vocabularies or training sets (especially for English), and (3) as Hindi and Swahili observe data repetition their curves slope upward from diminishing returns.*

ATLAS的整体框架包含四个核心模块：

1. **单语言缩放定律拟合**：为每种语言拟合核心缩放定律 L(N, D_eff) = E + A/N^α + B/D_eff^β。
2. **跨语言迁移矩阵构建**：通过双语迁移分数（BTS）和微调适应分数（FAS）测量38×38语言对的迁移/干扰。
3. **多语言诅咒缩放定律**：建模损失与语言数量K、模型规模N、每语言数据量D的关系：L(N,D,K) = L_inf + A K^φ / N^α + B K^ψ / D^β。
4. **预训练 vs 微调决策公式**：估计从零预训练超越微调Unimax检查点所需的计算预算C与模型规模N的关系：C = 10^28 × N^1.65。



### 5.1 ATLAS核心缩放定律

ATLAS的核心缩放定律形式为：

$$\mathcal{L}(N, D_{\mathrm{eff}}) = E + \frac{A}{N^{\alpha}} + \frac{B}{\mathcal{D}_{\mathrm{eff}}^{\beta}}$$

其中N为模型参数量，D_eff为有效数据量，E为不可约损失，A、B为缩放系数，α、β为缩放指数。

### 5.2 有效数据暴露项

有效数据暴露项将数据来源分解为三个独立项：

$$\mathcal{D}_{\mathrm{eff}} = \underbrace{S_{\lambda_t}(D_t; U_t)}_{\mathrm{Monolingual}} + \underbrace{\sum_{i \in \mathcal{K}} \tau_i S_{\lambda_i}(D_i; U_i)}_{\mathrm{Transfer\ Languages}} + \underbrace{\tau_{\mathrm{other}} S_{\lambda_{\mathrm{other}}}(D_{\mathrm{other}}; U_{\mathrm{other}})}_{\mathrm{Other\ Languages}}$$

其中，K_t为迁移语言集合（最多3种最常共采样语言），τ_i为可学习的迁移权重（从BTS初始化），τ_other为其他语言的迁移权重。

### 5.3 饱和函数

饱和函数确保当训练token超过该语言的唯一token数U时，有效数据平滑衰减：

$$\mathcal{S}_{\lambda}(D; U) = \begin{cases} D, & D \le U \ (\le 1\ \mathrm{epoch}) \\ U\left[1 + \frac{1 - \exp(-\lambda(D/U - 1))}{\lambda}\right], & D > U \ (> 1\ \mathrm{epoch}) \end{cases}$$

λ为共享的重复参数，控制衰减速率。

### 5.4 双语迁移分数（BTS）

BTS衡量双语模型（50%源语言s，50%目标语言t）相对于单语模型t达到相同损失所需的额外训练步数：

$$\mathrm{BTS}_{st} = -\frac{\sigma_{\mathrm{bi}}(L_t(d_{\mathrm{mono}})) - 2 d_{\mathrm{mono}}}{d_{\mathrm{mono}}}$$

正值表示正迁移，负值表示干扰。BTS基于2B参数模型和42B token参考水平计算。

### 5.5 多语言诅咒缩放定律

建模损失与语言数量K、模型规模N、每语言数据量D的关系：

$$\mathcal{L}(N,D,K) = \mathcal{L}_\infty + \frac{A K^\phi}{N^\alpha} + \frac{B K^\psi}{D^\beta}$$

φ和ψ分别捕捉容量和数据需求随语言数量增长的指数。拟合结果显示φ=0.11，ψ=-0.04。

### 5.6 等损失缩放公式

当语言数量从K扩展到rK时，为保持损失不变：

- 模型规模需乘以：$(N'/N)^\star = r^{\phi/\alpha}$
- 总训练数据量需乘以：$(D_{\mathrm{tot}}'/D_{\mathrm{tot}})^\star = r^{1+\psi/\beta}$
- 计算预算需乘以：$C'/C = r^{1+\phi/\alpha+\psi/\beta}$

具体数值：扩展至4·K语言时，总数据量需扩大2.74倍，模型规模需扩大1.4倍，计算预算需扩大r^0.97倍。

### 5.7 预训练 vs 微调决策公式

从零预训练超越微调Unimax检查点所需的计算预算C与模型规模N的关系：

$$C = 10^{28} \times N^{1.65}$$

交叉点位于144B至283B token之间：若预算<144B token，微调多语言检查点更有效；若预算≥283B token，从零预训练更优。



## 实验与关键发现

### 6.1 主要结果

Table 1展示了不同缩放定律在单语言和多语言设置下对未见模型规模(N)、数据量(D)、计算量(C)和语言混合(M)的泛化R²：

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_0BkvUY61MX_ATLAS_Adaptiv/figures/002_Table_1.jpg]]
*Table 1: The $R ^ { 2 }$ evaluation metrics for the fitted scaling laws, holding out separate dimensions of generalization: the largest model sizes N, most training tokens D, most compute C, and unique multilingual training mixtures M. In both monolingual and multilingual settings, we average $\mathrm { \dot { \bar { \it R } } ^ { 2 } }$ across languages=[EN, FR, RU, ZH, HI, SW], including [ES, DE] for the multilingual setting. We find ADAPTIVE TRANSFER SCALING LAW outperforms prior work in Monolingual and Multilingual settings. We ablate the use of the terms for $D _ { \mathrm { o t h e r } }$ and transfer languages ( $\overline { { \sum } } \kappa _ { t } D _ { i }$ )

| 设置 | 缩放定律 | R² (整体) | R²(N) | R²(D) | R²(C) | R²(M) |
|------|----------|-----------|-------|-------|-------|-------|
| 多语言 | CSL | 0.64 | -0.99 | 0.72 | 0.66 | 0.61 |
| 多语言 | MSL | 0.67 | -0.65 | 0.73 | 0.67 | 0.70 |
| 多语言 | ATLAS (Dt only) | 0.70 | -0.75 | 0.80 | 0.72 | 0.64 |
| 多语言 | ATLAS (Dt + Dother) | 0.98 | 0.89 | 0.97 | 0.97 | 0.66 |
| 多语言 | **ATLAS (完整)** | **0.98** | **0.89** | **0.96** | **0.98** | **0.82** |
| 单语言 | CSL | 0.94 | 0.68 | 0.94 | 0.90 | 1.00 |
| 单语言 | DCSL | 0.93 | 0.78 | 0.93 | 0.88 | 1.00 |
| 单语言 | **ATLAS (Dt only)** | **0.92** | **0.88** | **0.91** | **0.88** | **1.00** |

关键发现：
- ATLAS在多语言设置下整体R²=0.98，R²(N)=0.89，R²(D)=0.96，R²(C)=0.98，R²(M)=0.82。
- 仅添加迁移语言项后，ATLAS的R²(M)从0.66提升至0.82，超越MSL的0.70。
- 在单语言设置下，ATLAS对更大模型规模的泛化R²(N)=0.88，优于Chinchilla的0.68和DCSL的0.78。

### 6.2 消融实验

Table 1的消融结果揭示了各组件的作用：
- **仅使用Dt项**：R²(N)为-0.75，无法泛化到更大模型。
- **添加Dother项**：R²(N)提升至0.89，R²(D)提升至0.97，但R²(M)仅为0.66。
- **进一步添加迁移语言项**：R²(M)从0.66提升至0.82，证明迁移项对混合泛化的关键作用。

### 6.3 跨语言迁移分析

Figure 2展示了30×30跨语言迁移矩阵，Figure 3进一步分析了迁移分数的对称性和语言相似性的影响：
- 迁移分数具有强对称性（点靠近对角线），但最协同的对称对几乎总是共享语言系属和文字。
- 共享语言系属或文字的语言对迁移分数显著更高（p < .001）。
- 共享相同文字的语言对平均迁移分数为-0.23，而不同文字的对为-0.39。

### 6.4 多语言诅咒分析

Figure 4和Figure 5展示了多语言诅咒的量化结果：
- 目标语言损失受训练语言数量的影响最大，但这种损失惩罚随模型规模增大而减小。
- 扩展至4·K语言时，总数据量需扩大2.74倍，模型规模需扩大1.4倍。
- 模型规模扩展比数据扩展更能有效缓解多语言诅咒。

### 6.5 预训练 vs 微调决策

Figure 6和Figure 7展示了八种语言从零预训练与微调Unimax检查点的损失曲线对比：
- 从零预训练超越微调Unimax检查点的计算预算交叉点位于144B至283B token之间。
- 关系式为C = 10^28 × N^1.65。

### 6.6 公平性说明

- 实验覆盖48种评估语言，涵盖不同语系、文字和资源水平，但低资源语言（如斯瓦希里语）的独特token数量极少（仅770M，占英语的0.03%），可能导致拟合不稳定。
- Unimax采样率高度不均：英语占5%，多数语言仅1.42%，最低的ta_Latn仅2.29e-06%，这可能使低资源语言的迁移分数估计偏差较大。
- 双语迁移分数（BTS）基于2B参数模型和42B token参考水平，对于更小或更大的模型，迁移动态可能不同（如Figure C.1所示）。

### 补充图表

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_0BkvUY61MX_ATLAS_Adaptiv/figures/011_Table_2.jpg]]
*Table 2: Table B.1: An overview of experiment configurations in this work. We enumerate the experiment types: <Lang> for monolingual scaling, Unimax as a massively multilingual baseline, Language Pairs to measure language-to-language transfer, Capacity to measure the curse of multilinguality, or model capacity constraints on learning new languages, and Finetunes to understand how finetuning from a massively multilingual model compares to pretraining from scratch. We use a mix of Monolingual and Multilingual vocabularies, and training data. In the LANGUAGES and SCALES columns we use parentheses to show the number of language mixtures and number of scales run. Symbols such as ${ \mathcal { L } } _ { \m...$

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_0BkvUY61MX_ATLAS_Adaptiv/figures/012_Table_3.jpg]]
*Table 3: Table B.2: The pretraining hyperparameters used across experiments. We detail the batch size scheduling, the vocabulary choice, as well as fine-grained hyperparameter choices. Each choice is justified and grounded in prior work, discussed in the Explanation column.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_0BkvUY61MX_ATLAS_Adaptiv/figures/013_Table_4.jpg]]
*Table 4: Table B.3: The SCALE value mapped to the dimensions of the model, and the parameter count. The model dimensions, borrowed from Muennighoff et al. (2024), report the number of attention heads, number of layers, embed size, feedforward size, and key-value size. Our model may be slightly different sizes than prior work based on our vocabulary size (64000 + 512 special tokens).*

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_0BkvUY61MX_ATLAS_Adaptiv/figures/014_Table_5.jpg]]
*Table 5: Table B.4: The Unimax language sampling rates adapted from Chung et al. (2023). Languages are listed in order of their percentage sampling rate, which sum to 100.*



## 定位与知识库关联

ATLAS建立在以下工作基础上：

- **Chinchilla Scaling Law (Hoffmann et al., 2022)**：标准单语言缩放定律基线，使用两个幂律项建模模型规模N和数据量D。ATLAS在此基础上引入了数据重复和跨语言迁移建模。
- **Data-Constrained Scaling Law (Muennighoff et al., 2024)**：考虑数据重复后收益递减的基线，但需要两阶段拟合。ATLAS提出了更简单的单阶段饱和函数变体。
- **Multilingual Scaling Law (He et al., 2024)**：多语言缩放定律基线，使用N、D和目标语言语系采样比例建模损失。ATLAS通过显式建模个体语言迁移超越了语系级别的聚合。
- **Unimax (Chung et al., 2023)**：多语言采样策略，ATLAS使用其检查点进行预训练 vs 微调对比实验。
- **MADLAD-400 (Kudugunta et al., 2024)**：多语言数据集，ATLAS的实验基于此数据集。

ATLAS的独特贡献在于：
1. 首次将有效数据暴露项分解为目标语言、迁移语言和其他语言三个独立来源。
2. 构建了最大的经验性跨语言迁移矩阵（38×38语言对）。
3. 推导了多语言诅咒的量化缩放定律，为实践者提供了扩展语言覆盖范围时的最优缩放策略。
4. 提供了预训练 vs 微调的通用决策公式。



## 原文 PDF

![[paperPDFs/ICLR_2026/ATLAS_Adaptive_Transfer_Scaling_Laws_for_Multilingual_Pretraining_Finetuning_and_Decoding_the_Curse_of_Multilinguality.pdf]]
