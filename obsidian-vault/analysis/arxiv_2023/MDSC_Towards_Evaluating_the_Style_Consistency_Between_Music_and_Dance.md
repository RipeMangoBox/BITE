---
title: "MDSC: Towards Evaluating the Style Consistency Between Music and Dance"
type: paper
paper_level: A
venue: arXiv
year: 2023
pdf_ref: paperPDFs/arxiv_2023/MDSC_Towards_Evaluating_the_Style_Consistency_Between_Music_and_Dance.pdf
aliases:
- MMDSC
- MDSC
tags:
- arxiv_2023
- topic/other_unclear
- topic/other_unclear/music_dance_style_consistency
core_operator: 将风格一致性评估建模为聚类问题，通过最小化簇内距离和最大化簇间距离对齐音乐与动作嵌入。
primary_logic: 音乐与舞蹈之间存在多对多映射，直接使用嵌入相似度不适用；通过聚类目标对齐预训练编码器的嵌入空间，利用簇内/簇间距离比（I2I）量化风格一致性。
claims:
- 现有指标无法评估音乐与舞蹈的风格一致性。
- 采用聚类方法对齐跨模态嵌入，而非使用直接嵌入相似度。
- 同时使用簇内损失、簇间损失和正则化项的完整聚类目标获得最佳风格一致性。
- AIST++ & AIOZ-GDANCE 测试集 上 音乐风格分类准确率 = 77.04%
---

# MDSC: Towards Evaluating the Style Consistency Between Music and Dance

> [!tip] 核心洞察
> 音乐与舞蹈之间存在多对多映射，直接使用嵌入相似度不适用；通过聚类目标对齐预训练编码器的嵌入空间，利用簇内/簇间距离比（I2I）量化风格一致性。

| 字段 | 内容 |
|------|------|
| 中文题名 | MDSC: 评估音乐与舞蹈风格一致性 |
| 英文题名 | MDSC: Towards Evaluating the Style Consistency Between Music and Dance |
| 会议/期刊 | arXiv 2023 |
| Links | [paper](https://arxiv.org/abs/2309.01340) |
| Topic | #topic/other_unclear #topic/other_unclear/music_dance_style_consistency |
| Method | MDSC (Music-Dance Style Consistency) |
| Dataset | AIST++ & AIOZ-GDANCE 测试集, 生成动作（AIST++ 音乐驱动） |

> [!tip] 效果简介
> - AIST++ & AIOZ-GDANCE 测试集 上，音乐风格分类准确率 77.04% vs 对比模式下约57.60% (Table 1) (+19.44%)；运动风格分类准确率 94.20%。
> - 生成动作（AIST++ 音乐驱动） 上，风格分类准确率 Bailando 37.04% (最高) vs UDE / FACT (较低)。

## 概述

**问题瓶颈**：现有音乐驱动舞蹈生成与评估指标（如动作保真度、多样性、节奏对齐）均无法量化音乐与舞蹈之间的**风格一致性**。直接使用预训练嵌入的相似度（如余弦距离）在音乐与舞蹈的“多对多”映射下失效——一段音乐可对应多种风格的舞蹈，反之亦然。

**核心思路**：MDSC 将风格一致性评估建模为**聚类问题**——将风格一致的音乐嵌入与运动嵌入拉入同一聚类中心，不一致的推至不同中心。通过最小化簇内距离、最大化簇间距离，并引入正则化项，在联合对齐空间中学习可判别的风格表征。最终以簇内/簇间距离之比（I2I）作为风格一致性分数。

**方法定位**：MDSC 并非运动生成方法，而是一种**后验评估指标**。其管线由四个模块构成：预训练音乐编码器（基于 CLIP 范式训练的 Music Tagging Transformer）、预训练运动自编码器（以重建损失训练）、两个轻量 MLP（将跨模态嵌入投影至联合空间），以及可学习的聚类中心嵌入与辅助分类头。评估时仅需舞蹈动作嵌入，无需音乐，因此可独立评估任意生成动作的风格一致性。

**主要结果**：在 AIST++ 与 AIOZ-GDANCE 测试集上，MDSC 的音乐风格分类准确率达 77.04%，运动风格分类准确率达 94.20%。对现有生成方法（**Bailando** (Li et al., CVPR 2022)、**UDE** (Zhou & Wang, CVPR 2023)、FACT）的评估显示，Bailando 的风格一致性最高（37.04%），与用户研究结果一致。消融实验证实，完整的聚类损失（簇内 + 簇间 + 正则化）和联合空间对齐策略是性能的关键支撑。

**局限与待验证问题**：MDSC 依赖预定义的 10 种音乐风格类别，对新风格或开放集场景的泛化能力未经验证；用户研究规模较小（3 人）；如何将风格一致性与节奏一致性结合为统一指标仍是开放问题。

## 背景与动机

音乐驱动的舞蹈生成旨在根据输入的音乐自动合成与之匹配的舞蹈动作序列。这一任务的评估体系长期存在一个结构性缺口：现有指标几乎全部聚焦于**动作保真度**（motion fidelity）、**动作多样性**（diversity）以及**节拍对齐**（rhythmic matching），却系统性地忽略了对音乐与舞蹈之间**风格一致性**的量化度量。换言之，一段舞蹈动作可以在运动学上流畅、在节奏上与音乐同步，但其视觉风格可能与音乐的情感或流派特征完全脱节——而现有指标对此无能为力。

这种评估盲区的根源在于音乐与舞蹈之间存在天然的**多对多映射关系**：同一首音乐可以搭配多种风格的舞蹈，同一种舞蹈风格也可以适配多首不同的音乐。这导致直接使用跨模态嵌入相似度（如余弦相似度）来度量风格一致性在理论上不成立——高相似度既不能保证风格匹配，低相似度也未必意味着风格冲突。因此，需要一种全新的评估范式来填补这一空白。

MDSC 的核心动机正是针对上述瓶颈：**将风格一致性评估建模为一个聚类问题**，而非简单的嵌入对齐问题。其基本直觉是：风格一致的音乐-舞蹈对应形成紧密的簇，风格不一致的对则被推远。通过最小化簇内距离、最大化簇间距离，并计算二者的比值（I2I），MDSC 提供了一种可量化的风格一致性度量，且评估时仅需舞蹈动作嵌入，无需音乐输入，使其能够独立评估生成动作的风格质量。

## 核心创新

MDSC 的核心创新在于将音乐与舞蹈的风格一致性评估从传统的**直接嵌入相似度**范式转变为**聚类驱动的对齐与度量**范式。这一转变解决了音乐与舞蹈之间存在“多对多映射”这一根本性难题——同一首音乐可以搭配多种风格的舞蹈，同一种舞蹈风格也可以适配多首不同的音乐，因此直接计算音乐嵌入与动作嵌入的余弦相似度（如现有方法所做）无法可靠地反映风格一致性。

具体而言，MDSC 在以下两个关键维度上实现了突破：

### 1. 聚类驱动的风格一致性建模

现有音乐-舞蹈一致性指标（如 FACT、Bailando、UDE 等方法所使用的评估手段）仅关注动作保真度、多样性和节奏击打对齐，**缺少对风格一致性的量化度量**。MDSC 首次将风格一致性评估建模为聚类问题：通过最小化簇内距离（$`\mathcal{L}_{intra}`$）和最大化簇间距离（$`\mathcal{L}_{inter}`$），将风格一致的音乐嵌入与舞蹈动作嵌入拉入同一聚类中心，同时将风格不一致的嵌入推远。最终，使用簇内距离与簇间距离的比值 **I2I**（$`I2I = \frac{Intra.}{Inter.}`$）作为风格一致性的量化指标——I2I 值越小，风格一致性越高。

消融实验（Table 3）证实了这一设计的有效性：仅使用簇内损失（$`\mathcal{L}_{intra}`$）时，模型无法学习到有区分力的表征；簇间损失（$`\mathcal{L}_{inter}`$）对模型能力影响显著；完整的聚类损失（$`\mathcal{L}_{intra} + \mathcal{L}_{inter} + \mathcal{L}_{reg}`$）取得最佳运动风格一致性（Motion Acc. 94.20%，I2I 0.16）。

### 2. 联合空间跨模态对齐策略

在跨模态对齐策略上，MDSC 摒弃了“将运动嵌入对齐到音乐嵌入”或“将音乐嵌入对齐到运动嵌入”的单向映射方式，转而采用**双向投影到共享联合空间**的设计。具体地，使用两个轻量级 MLP——$`f_{AJ}`$（音乐→联合空间）和 $`f_{MJ}`$（运动→联合空间）——将预训练的音乐编码器 $`E_A`$ 和运动编码器 $`E_M`$ 的输出同时投影到同一联合空间中进行对齐。

Table 1 的定量结果验证了这一设计的优势：联合空间设计（$`f_{MJ} + f_{AJ}`$）在音乐风格分类准确率上达到 77.04%，显著优于仅对齐运动到音乐空间（57.60%）或仅对齐音乐到运动空间的变体。这一结果表明，**双向对齐能够更好地保留两个模态各自的风格信息**，而非在单向映射中丢失关键的判别特征。

### 关键洞察总结

| 创新维度 | 基线做法 | MDSC 做法 | 证据锚点 |
|---------|---------|----------|---------|
| 风格一致性评估方式 | 直接嵌入距离（余弦相似度）或节奏击打对齐 | 基于聚类的簇内/簇间距离及 I2I 比值 | Abstract: "modeling it as a clustering problem" |
| 跨模态对齐策略 | 单向映射（运动→音乐 或 音乐→运动） | 双向投影到共享联合空间（两个 MLP） | Fig. 3(c), Table 1 |
| 评估独立性 | 需要音乐与动作配对评估 | 仅需舞蹈动作嵌入即可独立评估风格一致性 | Section 4.2 |

值得注意的是，MDSC 的评估阶段**仅需舞蹈动作嵌入**，无需对应的音乐输入，这使得该指标可以独立评估任意生成动作的风格一致性，为音乐驱动舞蹈生成方法提供了即插即用的风格维度基准（Table 2）。

## 整体框架

MDSC 的整体流程遵循“预训练编码器 → 投影对齐 → 聚类评估”三阶段范式，如 Figure 2 所示。其核心设计动机在于：音乐与舞蹈之间存在多对多映射，直接使用嵌入相似度无法可靠地量化风格一致性。因此，MDSC 将风格一致性评估建模为一个聚类问题——通过最小化簇内距离、最大化簇间距离，在联合嵌入空间中实现跨模态风格对齐。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/002_Figure_2.jpg]]
*Figure 2: Pipeline of Music-Dance Style Consistency (a) We train a motion auto-encoder supervised by reconstruction loss, and use the encoder as*

### 模块组成与数据流

系统包含四个关键模块，按推理流向依次为：

1. **预训练音乐编码器** $E_A$：接收原始音乐波形，输出固定维度的音乐风格嵌入 $z_A \in \mathbb{R}^{1 \times c_A}$。该编码器基于改进的 Music Tagging Transformer，采用 CLIP 范式在音乐-文本对上预训练，具备捕获高层风格语义的能力。

2. **预训练运动编码器** $E_M$：接收舞蹈动作序列 $x$，输出运动嵌入 $z_M \in \mathbb{R}^{1 \times c_M}$。该编码器来自一个运动自编码器的编码部分，其训练目标为最小化重构损失 $\mathcal{L}_{rc} = \| \tilde{\boldsymbol{x}} - \boldsymbol{x} \|$，其中 $\tilde{x} = \mathcal{D}_M(\mathcal{E}_M(x))$ 为解码器重建的动作序列。这一预训练确保了运动嵌入保留动作的判别性特征。

3. **联合空间投影 MLP** $f_{MJ}$ 与 $f_{AJ}$：两个轻量级多层感知机分别将运动嵌入和音乐嵌入映射到共享的联合对齐空间：
   $$f_{MJ}(z_M): \mathbb{R}^{1 \times c_M} \to \mathbb{R}^{1 \times c_J}$$
   $$f_{AJ}(z_A): \mathbb{R}^{1 \times c_A} \to \mathbb{R}^{1 \times c_J}$$
   这一设计与仅将单模态嵌入对齐到另一模态的变体（Figure 3a、3b）形成对比。实验表明（Table 1），双向投影到联合空间（Figure 3c）在音乐风格分类准确率上达到 77.04%，显著优于其他变体。

4. **可学习聚类中心** $\hat{c}_i$（$i=1,\dots,K$）：在联合空间中定义 $K$ 个可学习的聚类中心嵌入（$K$ 等于预定义的风格类别数）。评估时，通过计算嵌入与聚类中心的距离，得到簇内距离（Intra）、簇间距离（Inter）及其比值 I2I，以此量化风格一致性。

### 训练与评估解耦

值得注意的设计选择是：训练阶段需要成对的音乐-舞蹈数据以优化 MLP 和聚类中心，但**评估阶段仅需舞蹈动作嵌入**。这意味着 MDSC 可以独立评估任意生成模型产出的舞蹈序列的风格一致性，无需对应的音乐输入。这一特性使其可作为通用评估工具，直接应用于音乐驱动动作生成方法的基准测试（如 Table 2 中对 Bailando、UDE、FACT 的评估）。

### 设计变体与关键决策

Figure 3 展示了跨模态对齐的三种设计空间：
- **(a) 固定音乐嵌入，对齐运动嵌入**：$f_{MA}(z_M): \mathbb{R}^{1 \times c_M} \to \mathbb{R}^{1 \times c_A}$
- **(b) 固定运动嵌入，对齐音乐嵌入**：$f_{AM}(z_A): \mathbb{R}^{1 \times c_A} \to \mathbb{R}^{1 \times c_M}$
- **(c) 双向投影到联合空间**：同时使用 $f_{MJ}$ 和 $f_{AJ}$

Table 1 的量化结果表明，联合空间设计在音乐风格分类准确率（77.04% vs. 约 57.60%）和运动风格分类准确率（94.20%）上均取得最优，证实了双向对齐对于跨模态风格一致性建模的必要性。

## 核心模块与公式推导

MDSC 将音乐-舞蹈风格一致性评估建模为聚类问题，其核心由四个模块构成：预训练音乐编码器、预训练运动编码器、联合空间投影 MLP 以及可学习聚类中心。以下逐一展开关键设计。

### 预训练音乐编码器 $E_A$

音乐编码器采用文献 [31] 中预训练的改进版 Music Tagging Transformer，该模型以 CLIP 风格范式在音乐-文本对上训练，能够输出富含风格信息的音乐嵌入 $z_A \in \mathbb{R}^{1 \times c_A}$。在 MDSC 训练阶段，$E_A$ 被冻结，仅作为特征提取器使用。

### 预训练运动编码器 $E_M$

运动编码器通过自编码器预训练获得。给定运动序列 $x$，编码器 $E_M$ 将其压缩为低维嵌入 $z_M$，解码器 $\mathcal{D}_M$ 则从嵌入重建运动：

$$
\tilde{x} = \mathcal{D}_M(\mathcal{E}_M(x)) \tag{1}
$$

训练目标为最小化重建损失：

$$
\mathcal{L}_{rc} = \| \tilde{\boldsymbol{x}} - \boldsymbol{x} \| \tag{2}
$$

这一预训练使 $E_M$ 能够提取运动序列的紧凑风格表征。与音乐编码器一致，$E_M$ 在后续风格对齐阶段也被冻结。

### 联合空间投影 MLP

为对齐音乐与运动两种异质嵌入，MDSC 引入两个轻量级 MLP——$f_{AJ}$ 和 $f_{MJ}$，分别将音乐嵌入和运动嵌入映射到共享的联合空间：

$$
f_{AJ}(z_A): \mathbb{R}^{1 \times c_A} \to \mathbb{R}^{1 \times c_J} \tag{5}
$$

$$
f_{MJ}(z_M): \mathbb{R}^{1 \times c_M} \to \mathbb{R}^{1 \times c_J} \tag{6}
$$

这一设计（对应 Figure 3(c)）相较于将运动对齐到音乐空间（$f_{MA}$，Eq. 3）或将音乐对齐到运动空间（$f_{AM}$，Eq. 4）两种变体，在音乐风格分类准确率上提升显著（77.04% vs. 约57.60%，Table 1），验证了双向投影到联合空间的必要性。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/003_Figure_3.jpg]]
*Figure 3: Variants of Design in Aligning Cross-Modality EmbeddingAlignment of motion embedding and music embedding in three different approaches. (a) Fix music embedding and align motion embedding. (b) Fix motion embedding and align music embedding. (c) Align both music and motion embedding to joint space. Fixed, Trainable*

### 可学习聚类中心与聚类损失

MDSC 在联合空间中设置 $K$ 个可学习聚类中心嵌入 $\hat{c}_i$（$K$ 等于预定义的音乐风格数）。风格一致性通过以下三个损失项联合优化：

**簇内损失** 最小化嵌入与其所属聚类中心的余弦距离：

$$
\mathcal{L}_{intra}^a = \frac{1}{K} \sum_{i=1}^K (1 - \langle \tilde{z}_a^{c_i}, \hat{c}_i \rangle) \tag{8}
$$

**簇间损失** 最大化嵌入与非所属聚类中心的距离，防止不同风格嵌入混杂：

$$
\mathcal{L}_{inter}^a = \frac{1}{K(K-1)} \sum_{i=1}^K \sum_{j=1, j \neq i}^K \langle \tilde{z}_a^{c_i}, \hat{c}_j \rangle \tag{9}
$$

**正则化损失** 约束聚类中心之间的相似度，避免中心过度坍塌：

$$
\mathcal{L}_{reg} = \frac{1}{K(K-1)} \sum_{i=1}^K \sum_{j=1, j \neq i}^K \langle \hat{c}_i, \hat{c}_j \rangle \tag{10}
$$

消融实验（Table 3）表明：仅使用 $\mathcal{L}_{intra}$ 无法学习到有区分力的表征；$\mathcal{L}_{inter}$ 对模型能力影响最大；三者联合使用（$\mathcal{L}_{cluster} = \mathcal{L}_{intra} + \mathcal{L}_{inter} + \mathcal{L}_{reg}$）获得最佳运动风格一致性（Motion Acc. 94.20%, I2I 0.16）。

此外，模型还引入 InfoNCE 对比损失作为辅助目标，拉近配对音乐-运动嵌入、推远非配对样本：

$$
\mathcal{L}_{MA} = -\log \frac{\exp(z_i^M \cdot z_i^A / \tau)}{\sum_{j=1}^N \exp(z_i^M \cdot z_j^A / \tau)} \tag{7}
$$

### 风格一致性度量：I2I 比率

评估阶段，MDSC 仅需舞蹈动作嵌入，计算其与各聚类中心的簇内距离均值（Intra.）和簇间距离均值（Inter.），并以二者比值作为风格一致性指标：

$$
I2I = \frac{Intra.}{Inter.}
$$

I2I 值越小，表明动作嵌入越紧密聚集在对应风格中心附近、同时远离其他风格中心，即风格一致性越高。该指标无需音乐输入，可独立评估生成舞蹈的风格质量。

## 实验与分析

MDSC 在 AIST++ 和 AIOZ-GDANCE 两个数据集上进行了系统的定量与定性评估。实验围绕三个核心维度展开：风格分类准确率、聚类质量指标（I2I 比率）以及生成舞蹈动作的基准测试。关键发现是，联合对齐空间配合完整聚类损失的设计在所有指标上均取得最优，且 I2I 比率与人类主观判断高度一致。

### 跨模态对齐设计对比

Table 1 报告了三种跨模态对齐策略在音乐风格分类和运动风格分类上的表现。三种策略分别为：(a) 将运动嵌入对齐到固定的音乐嵌入空间（$f_{MA}$）；(b) 将音乐嵌入对齐到固定的运动嵌入空间（$f_{AM}$）；(c) 将两者同时投影到联合空间（$f_{MJ} + f_{AJ}$）。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/005_Table_1.jpg]]
*Table 1: Evaluation Results on Music Streams and GT Motion Sequences. We report the quantitative results of the variants of our method in music-dance style consistency evaluation on the test set of AIST++[25] and AIOZ-GDANCE[21]. We measure the style estimation accuracy, style retrieval accuracy, as well as style consistency score on both music streams and dance motion sequences. Indicate best results*

联合空间设计在音乐风格分类准确率上达到 **77.04%**，显著优于其他两种方案（约 57.60%），提升幅度达 **+19.44 个百分点**。在运动风格分类准确率上，三种方案均表现较高（约 94%），说明运动编码器本身的判别能力较强。值得注意的是，仅使用 $f_{MA}$ 或 $f_{AM}$ 的单向对齐策略在音乐风格分类上表现相近，表明单向投影无法充分捕获音乐-舞蹈之间的多对多映射关系。

Table 2 进一步将 MDSC 应用于三种音乐驱动动作生成方法（**Bailando** (Li et al., CVPR 2022)、**UDE** (Zhou & Wang, CVPR 2023)、**FACT**）的输出进行评估。在 AIST++ 音乐条件下，Bailando 生成的舞蹈动作获得最高的风格分类准确率（37.04%），而 UDE 和 FACT 的表现较低。这表明现有生成方法在风格一致性方面仍有较大改进空间，MDSC 能够有效区分不同方法的风格保持能力。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/006_Table_2.jpg]]
*Table 2: Evaluation Results on Generated Motion Sequences. We conduct evaluation on the generated motion sequences of different methods [25][38][55]. Indicate best results*

### 聚类损失消融

Table 3 对聚类损失项进行了消融实验，验证了三个损失组件的独立贡献：

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/008_Table_3.jpg]]
*Table 3: Ablation on loss terms We train our method using design option*

- **仅使用簇内损失（$\mathcal{L}_{intra}$）**：模型无法学习到有区分力的表征，风格分类准确率大幅下降。这印证了仅靠拉近同类嵌入不足以形成有意义的聚类结构。
- **簇间损失（$\mathcal{L}_{inter}$）的影响显著**：移除 $\mathcal{L}_{inter}$ 后，模型性能明显退化，说明推远不同风格聚类中心是学习判别性特征的关键驱动力。
- **正则化损失（$\mathcal{L}_{reg}$）**：作为辅助项，通过约束聚类中心之间的余弦相似度，防止中心过度集中，进一步提升了聚类质量。
- **完整聚类损失**（$\mathcal{L}_{intra} + \mathcal{L}_{inter} + \mathcal{L}_{reg}$）在运动风格分类准确率（94.20%）和 I2I 比率（0.16）上均取得最优，验证了三个损失项协同作用的必要性。

### 学习策略消融

Table 4 对比了两种聚类学习策略：固定聚类数量（已知风格数为 10）与未知聚类数量的自适应策略。结果表明，在已知聚类数量的设定下，模型能够更稳定地学习到与预定义风格类别对齐的聚类结构。未知聚类数量的策略表现较差，说明当前方法依赖于先验的风格类别信息，对开放集场景的泛化能力有限。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/009_Table_4.jpg]]
*Table 4: Ablation on Learning Strategy We train our method using design option*

### I2I 比率与生成方法评估

Figure 5 展示了不同生成方法在 10 种音乐风格下的聚类距离统计（簇内距离 Intra、簇间距离 Inter 及 I2I 比率）。I2I 比率定义为 $\text{I2I} = \frac{\text{Intra}}{\text{Inter}}$，值越小表示风格一致性越高。Bailando 在多数风格上获得最低的 I2I 比率，与 Table 2 中的风格分类准确率排序一致，验证了 I2I 作为风格一致性量化指标的有效性。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/007_Figure_5.jpg]]
*Figure 5: Results of Cluster Distance of SOTAs. We calculate the intracluster(Intra.) distance, intercluster distance(Inter.), and intra-to-inter(I2I.) between generated motion embedding and learned cluster centers embedding and report their mean and variance*

Figure 4 和 Figure 10-19 提供了各风格下生成舞蹈与真值（GT）的视觉对比，进一步从定性角度支持了量化结论。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/004_Figure_4.jpg]]
*Figure 4: Visual Comparison of Music-Dance Style Consistency. We compare the generated motion sequences conditioned on different music styles with GTs. (a) JB means Ballet Jazz style, (b) JS means Street Jazz style, (c) LH means LA Hiphop style, (d) BR means Break style, (e) LO means Lock style, (f) MH means Middle Hiphop style, (g) KR means Krump style, (h) WA means Waacking style, (i) HO means House style, (j) PO means Pop style. For each dance, we adopt 10sec motion segment and evenly sample 10 frames. The dashed box indicates poses that are style inconsistent with GTs*

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/015_Figure_10.jpg]]
*Figure 10: Visual Comparison of Dance Moves Generated by BR Style Music. The average MDSC: Bailando > UDE ≈ FACT*

### 用户研究验证

Figure 7 报告了由 3 名独立用户对不同算法生成舞蹈的风格一致性评分。用户研究结果与 MDSC 指标排序一致，表明所提指标与人类主观感知之间存在良好的相关性。但需注意，用户研究规模较小（仅 3 人），统计稳健性有待更大规模验证。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/011_Figure_7.jpg]]
*Figure 7: Average score of different algorithms annotated by 3 independent users. The results of user study are consistent with our metrics as shown in Sec. 4.3*

### 嵌入空间可视化

Figure 8 和 Figure 9 分别展示了预训练编码器的原始嵌入与经过 MLP 投影到联合空间后的嵌入分布。原始嵌入中，音乐与运动模态各自形成独立的分布，跨模态对应关系不明确。经过联合空间投影后，相同风格的音乐与运动嵌入被拉近并形成清晰的聚类簇，直观验证了联合对齐策略的有效性。

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/012_Figure_8.jpg]]
*Figure 8: Visualization of Embeddings Encoded by Pre-Trained Encoders. We show why embeddings obtained directly from pretrained encoders are not aligned. a) Shows the results of motion embeddings obtained by*

![[assets/figures/papers/paper_list_l1051_https_arxiv_org_abs_2309_01340/figures/013_Figure_9.jpg]]
*Figure 9: Visualization of Embeddings after Projection in Joint Space. We show the results after projected by adopting ML*

### 失败模式与局限性

1. **风格类别依赖**：MDSC 的训练和评估均依赖预定义的 10 种音乐风格标签，对未见风格或开放集场景的泛化能力未经验证。Table 4 中未知聚类数策略的性能下降进一步佐证了这一局限。
2. **全局风格评估**：I2I 比率仅衡量全局风格一致性，不涉及节奏对齐或局部动作细节。对于节奏高度匹配但风格偏离的舞蹈，I2I 可能无法提供完整评价。
3. **标注成本**：训练需要风格标注数据（AIST++/AIOZ-GDANCE），扩展到新领域时标注成本较高。
4. **用户研究规模**：仅 3 名评估者，主观评价的统计显著性需进一步验证。

## 方法谱系与知识库定位

### 问题定位：音乐-舞蹈评估中的风格盲区

现有音乐驱动舞蹈生成领域的评估指标集中在三个维度：动作保真度（motion fidelity）、动作多样性（diversity）以及节奏对齐（rhythmic matching）。然而，这些指标无法回答一个关键问题：生成的舞蹈是否在**风格**上与音乐一致？MDSC 的核心贡献正是填补了这一评估盲区——将风格一致性从保真度和节奏对齐中解耦，作为独立的评估维度引入。

这一问题的本质在于音乐与舞蹈之间存在**多对多映射**（multiple music-dance mappings）：同一段音乐可以对应多种风格的舞蹈，同一种舞蹈风格也可以适配不同音乐。因此，直接使用跨模态嵌入的余弦相似度（如 CLIP 式的对齐方式）无法有效度量风格一致性——高相似度可能来自风格匹配，也可能来自其他混淆因素。

### 方法谱系中的位置

MDSC 处于**跨模态风格对齐评估**这一细分领域，其方法谱系可从以下三个维度定位：

**1. 与音乐驱动动作生成方法的关系**

MDSC 本身不生成舞蹈，而是作为评估工具作用于生成结果。论文中直接评估的生成方法包括：
- **Bailando**（Li et al., CVPR 2022）：基于编解码器结构的音乐驱动舞蹈生成方法，在风格一致性评估中表现最优（风格分类准确率 37.04%）。
- **FACT**：音乐驱动动作生成方法（论文未提供完整引用，需人工核实）。
- **UDE**（Zhou & Wang, CVPR 2023）：音乐驱动动作生成方法，风格一致性表现较弱。

这些方法在设计时并未显式优化风格一致性，MDSC 的评估结果揭示了它们在风格对齐方面的差异，为后续方法改进提供了量化依据。

**2. 与跨模态对齐方法的对比**

MDSC 探索了三种跨模态对齐策略（Figure 3）：
- **(a) 固定音乐嵌入，对齐运动嵌入**：将运动嵌入投影到音乐空间（$f_{MA}$），音乐编码器冻结。
- **(b) 固定运动嵌入，对齐音乐嵌入**：将音乐嵌入投影到运动空间（$f_{AM}$），运动编码器冻结。
- **(c) 联合空间对齐**：同时将音乐和运动嵌入投影到共享的联合空间（$f_{AJ} + f_{MJ}$），两个 MLP 均可训练。

实验表明（Table 1），联合空间设计在音乐风格分类准确率上达到 57.60%（对比模式下），显著优于单向对齐策略。这一发现表明，**对称的跨模态投影**比非对称对齐更适合风格一致性建模。

**3. 与聚类方法的关联**

MDSC 将风格一致性评估建模为聚类问题，这与传统的对比学习（如 CLIP 的 InfoNCE 损失）形成互补。具体而言：
- **对比学习**（Eq. 7 的 $\mathcal{L}_{MA}$）负责拉近配对样本、推远非配对样本，建立初步的跨模态关联。
- **聚类目标**（$\mathcal{L}_{intra} + \mathcal{L}_{inter} + \mathcal{L}_{reg}$）进一步将嵌入空间组织为具有明确风格语义的簇结构。

消融实验（Table 3）揭示了各损失项的关键作用：
- 仅使用簇内损失 $\mathcal{L}_{intra}$ 时，模型无法学习到有区分力的表征。
- 簇间损失 $\mathcal{L}_{inter}$ 对模型能力影响显著，是风格区分的关键驱动力。
- 完整聚类目标（三项损失联合）获得最佳运动风格一致性（Motion Acc. 94.20%, I2I 0.16）。

### 适用边界与局限

**已知适用场景：**
- 评估对象为 10 种预定义音乐风格（来自 AIST++ 和 AIOZ-GDANCE 数据集），包括芭蕾爵士（JB）、街头爵士（JS）、LA Hiphop（LH）、霹雳舞（BR）等。
- 评估粒度为全局风格一致性，不涉及节奏对齐或局部动作细节。
- 评估时仅需舞蹈动作嵌入，无需音乐输入，可独立评估生成动作的风格属性。

**关键局限：**

1. **风格类别封闭性**：MDSC 依赖预定义的 10 种风格类别进行训练和评估，对开放集场景或未见风格的泛化能力未经验证。当面对新的舞蹈风格时，聚类中心的数量和语义均需重新定义。

2. **标注依赖性**：训练过程需要风格标注数据（AIST++/AIOZ-GDANCE），标注成本较高。这限制了 MDSC 向更大规模、更多样化数据集的扩展。

3. **评估维度的单一性**：MDSC 仅评估风格一致性，未与节奏对齐、动作质量等维度整合。一个完整的音乐-舞蹈评估体系需要将风格一致性与现有指标（如 Beat Align Score、FID 等）协同使用。

4. **用户研究规模有限**：论文中仅 3 名独立用户参与主观评价，统计稳定性有待加强。虽然用户研究结果与 MDSC 指标一致，但更大规模的人类评估仍是必要的验证手段。

### 开放问题

1. **风格数量的自适应确定**：当前聚类中心数量 $K$ 固定为已知风格数。是否可以通过自适应机制（如 DP-means 或 Bayesian nonparametrics）在训练中动态确定 $K$，使 MDSC 能够处理未知风格？

2. **统一一致性指标的设计**：如何将风格一致性（I2I 比率）与节奏一致性（如 Beat Align Score）融合为单一的统一评价指标？这需要考虑两个维度的量纲差异和权衡关系。

3. **弱监督/自监督训练**：在减少标注依赖的条件下训练 MDSC 是否可行？例如，利用舞蹈视频的风格标签自动挖掘，或通过跨模态聚类伪标签进行自训练。

4. **细粒度风格评估**：当前 MDSC 评估全局风格一致性，但一段舞蹈的风格可能在时间上变化（如风格融合或过渡）。如何将风格一致性评估扩展到时间维度，实现片段级别的细粒度评估？

5. **与人类感知的对齐**：I2I 比率作为客观指标，其数值变化与人类对风格一致性的感知敏感度之间的关系尚未量化研究。建立心理物理曲线（psychometric curve）将有助于确定 I2I 的实际意义阈值。

## 原文 PDF

![[paperPDFs/arxiv_2023/MDSC_Towards_Evaluating_the_Style_Consistency_Between_Music_and_Dance.pdf]]
