---
title: Generating Attribute-Aware Human Motions from Textual Prompt
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Generating_Attribute-Aware_Human_Motions_from_Textual_Prompt.pdf
project_link: null
code_link: null
aliases:
- GAAHMFTP
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 利用结构因果模型（SCM）将运动分解为因果的动作语义S和非因果的属性A，并通过因果信息瓶颈（CIB）目标函数（最大化I(X;S,A)+I(Y;S)-I(S;A)-λI(X;S)）来解耦S和A，实现属性独立控制。
primary_logic: 通过因果信息瓶颈从运动数据中提取无属性的语义令牌，再结合属性输入通过条件解码器生成属性感知的运动，从而在文本-运动对齐中显式分离语义和属性。
claims:
- AttrMoGen comprises a Semantic-Attribute Decoupling VQVAE and a Semantics Generative Transformer.
- The CIB objective function is defined as CIB(X,Y,S,A) = I(X;S,A) + I(Y;S) - I(S;A) - λ I(X;S).
- The encoder of Decoup-VQVAE uses a causal information bottleneck to decouple action semantics from human attributes, producing attribute-free semantic tokens.
- The overall loss combines VQVAE loss, entropy loss, and bottleneck loss.
---

# Generating Attribute-Aware Human Motions from Textual Prompt

> [!tip] 核心洞察
> 通过因果信息瓶颈从运动数据中提取无属性的语义令牌，再结合属性输入通过条件解码器生成属性感知的运动，从而在文本-运动对齐中显式分离语义和属性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于文本提示生成属性感知的人体动作 |
| 英文题名 | Generating Attribute-Aware Human Motions from Textual Prompt |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2506.21912) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | AttrMoGen |
| Dataset | HumanAttr test set |

> [!tip] 效果简介
> - HumanAttr test set 上，R-Precision Top-1 ↑ 0.705±0.002 vs 0.685±0.003 (MoMask) (+0.020)；FID ↓ 0.089±0.003 vs 0.245±0.009 (MoMask) (−63.7%)；MM-Dist ↓ 2.266±0.012 vs 2.602±0.009 (MoMask) (−0.336)。

## 概要

现有的文本驱动人体运动生成方法通常仅关注动作语义本身，而忽略了**人的属性（如年龄、性别）对运动模式的系统性影响**。由于文本描述中语义与属性高度耦合，模型无法显式控制生成的运动的属性特征，导致不同属性受试者之间的运动差异被模糊化。

针对这一瓶颈，本文提出 **AttrMoGen**，一个基于**结构因果模型（SCM）** 的属性感知运动生成框架。其核心思路是：将运动分解为**因果的动作语义 $S$** 与**非因果的属性 $A$**，并通过**因果信息瓶颈（Causal Information Bottleneck, CIB）** 目标函数显式解耦二者，从而实现对属性独立控制的运动生成。

AttrMoGen 由两个核心模块构成：**语义-属性解耦 VQVAE（Decoup-VQVAE）** 和 **语义生成 Transformer**。Decoup-VQVAE 的编码器在 CIB 约束下从原始运动中提取**无属性的语义令牌**，解码器则结合语义令牌与属性标签重建运动；语义生成 Transformer 负责从文本预测这些语义令牌，推理时再与用户指定的属性输入结合，生成属性感知的运动。

在 **HumanAttr** 数据集（整合自多个来源，包含 18.2k 条运动序列、640 名受试者，年龄跨度 5–88 岁）上的实验表明，AttrMoGen 在整体指标上显著优于强基线 **MoMask**：FID 从 0.245 降至 0.089（降幅 63.7%），R-Precision Top-1 从 0.685 提升至 0.705，MM-Dist 从 2.602 降至 2.266。消融实验证实，CIB 中的熵损失项（最小化 $I(S;A)$）和瓶颈损失项（限制 $I(X;S)$）对解耦效果至关重要——移除任一损失均会导致 FID 显著恶化。

该方法的主要局限在于：当前仅利用了年龄和性别的离散分组，未能充分利用数据集中约 74% 样本包含的体重和身高信息；属性控制依赖离散分组，可能无法捕捉连续的体格差异。如何将连续属性融入该因果解耦框架，是后续研究的重要方向。

### 文本驱动人体运动生成的现状与盲区

文本驱动的人体运动生成旨在根据自然语言描述合成符合语义的 3D 人体运动序列。近年来，基于自回归 Transformer、扩散模型和 VQVAE 的方法（如 **T2M-GPT** (Zhang et al., CVPR 2023)、**MDM** (Tevet et al., ICLR 2022)、**MoMask** 等）在运动质量与文本-运动对齐方面取得了显著进展。然而，这些方法存在一个共同的盲区：它们仅关注文本所描述的动作语义（如“走路”“挥手”），而完全忽略了执行动作的**人的属性**——年龄、性别、体型等——对运动模式的系统性影响。

现实世界中，不同属性的人执行同一动作时，运动模式存在显著差异。例如，老年人的步态通常步幅更小、速度更慢，而儿童的跑动则伴随更大的肢体摆动幅度。现有的文本-运动数据集中的描述往往仅聚焦于动作本身，导致**语义与属性在运动数据中高度耦合**：模型无法从“一个人在走路”这样的文本中推断出走路者的年龄或性别，更无法根据用户指定的属性生成差异化的运动。

### 朴素属性注入的失败

一种直观的补救思路是将属性短语直接拼接到文本提示中（如“一个老年男性在走路”），在测试时或训练时注入属性信息。然而实验证据表明，这种策略严重损害生成质量。在消融研究中，对强基线模型 **MoMask** 采用“测试时属性提示”（w/ attr test）策略后，FID 从 0.245 恶化至更差水平；即使在训练和测试中均加入属性提示（w/ attr train），性能仍远不及显式解耦方案（见 Table 6）。这说明，文本层面的简单拼接无法迫使模型将语义与属性分离，反而引入了噪声，干扰了文本-运动的对齐学习。

### 核心动机：因果解耦而非统计关联

上述问题的根源在于，动作语义（S）与人的属性（A）在观测运动数据（X）中是统计关联的，但二者在因果上应当是可分离的：动作“是什么”不应依赖于“谁”在做。本文的核心动机正是基于这一因果直觉——利用**结构因果模型（SCM）**将运动显式分解为因果性的动作语义 S 和非因果性的人体属性 A，并通过**因果信息瓶颈（CIB）**强制编码器从原始运动中剥离属性信息，从而获得“无属性”的语义令牌。这一设计使得下游的文本-语义预测与属性控制可以独立进行，最终实现真正意义上的属性感知运动生成。

## 核心方法与创新机理

AttrMoGen 的核心创新在于将**结构因果模型（SCM）**引入文本驱动的人体运动生成，首次显式解耦了动作语义与人的属性（如年龄、性别），从而实现对属性感知运动的可控生成。其关键突破集中在以下三个 **changed slots** 上：

### 1. 语义编码器设计：从标准 VQVAE 到因果信息瓶颈解耦

传统 VQVAE 编码器（如 **T2M-GPT** (Zhang et al., CVPR 2023)、**MoMask** 等采用的标准方案）直接将原始运动序列 $X$ 映射为隐空间令牌，不区分语义与属性信息。AttrMoGen 的 **Decoup-VQVAE** 编码器 $f$ 则通过**因果信息瓶颈（CIB）** 训练，强制提取**无属性的语义令牌** $S = f(X)$。

其核心机制是引入一个代理属性分类器 $h$，通过最小化条件熵来消除 $S$ 中的属性信息，同时利用**反事实瓶颈损失**限制原始运动 $X$ 到语义令牌 $S$ 的信息流，确保 $S$ 仅保留与动作语义相关的因果成分。这一设计使得语义令牌在向量量化后成为纯粹的“动作描述符”，为后续的属性独立控制奠定了基础。

### 2. 损失函数：从标准 VQVAE 损失到 CIB 目标

标准 VQVAE 仅使用重建损失和承诺损失。AttrMoGen 将其扩展为因果信息瓶颈目标函数：

$$CIB(X,Y,S,A) = I(X;S,A) + I(Y;S) - I(S;A) - \lambda I(X;S)$$

对应到实际训练中，总损失为：

$$\mathcal{L}_{overall} = \mathcal{L}_{vqvae} + \alpha \mathcal{L}_{entropy} + \lambda \mathcal{L}_{bottleneck}$$

其中，**熵损失** $\mathcal{L}_{entropy}$ 最小化 $I(S;A)$，迫使语义令牌 $S$ 与属性 $A$ 独立；**瓶颈损失** $\mathcal{L}_{bottleneck}$ 限制 $I(X;S)$，通过迫使原始运动与反事实运动（仅属性不同）的语义嵌入相似，确保 $S$ 仅捕获因果语义而非属性相关的外观变化。消融实验证实，移除熵损失会使 FID 从 0.089 骤升至 0.489，移除瓶颈损失则升至 0.184，验证了这两项对属性解耦的关键作用。

### 3. 属性条件注入机制：从纯文本生成到语义-属性联合解码

现有方法（如 **MDM** (Tevet et al., ICLR 2022)、**MotionDiffuse**、**MLD** 等）仅以文本为输入，生成结果无法按指定属性变化。AttrMoGen 的解码器 $g$ 同时接收无属性语义令牌 $S$ 和属性标签 $A$（经 one-hot 编码与 MLP 融合），重建出属性感知的运动 $\hat{X} = g(S, A)$。推理时，**Semantics Generative Transformer** 从文本预测语义令牌，用户可自由指定属性标签，实现“相同文本、不同属性”的独立控制。

**与朴素文本增强的本质区别**：消融实验（Table 6）表明，直接在文本提示中插入属性短语（如 “a man walks”）进行测试（w/ attr test）会严重损害生成质量；即使在训练中引入属性文本（w/ attr train），其性能仍显著低于 AttrMoGen 的显式解耦方案。这证明简单的文本级属性注入无法解开语义与属性在运动数据中的高度耦合，而 AttrMoGen 的因果解耦机制是实现属性感知生成的根本原因。

AttrMoGen 的整体流程分为两个阶段：**语义-属性解耦 VQVAE（Decoup-VQVAE）** 和 **语义生成 Transformer（Semantics Generative Transformer）**。Decoup-VQVAE 负责从原始运动数据中提取与属性无关的动作语义令牌，并在推理时结合用户指定的属性标签重建运动；语义生成 Transformer 则从文本描述中预测这些语义令牌，使模型能够根据文本生成属性感知的运动。

### 核心思路

该框架的核心洞察在于：现有文本驱动运动生成方法中，动作语义（如“跑步”、“挥手”）与人的属性（如年龄、性别）在运动数据中高度耦合。文本描述通常只关注动作本身，导致模型无法独立控制属性。AttrMoGen 通过**结构因果模型（SCM）** 将运动分解为因果的动作语义 $S$ 和非因果的属性 $A$，并利用**因果信息瓶颈（CIB）** 目标函数实现二者的显式解耦。

### 两阶段流程

**阶段一：Decoup-VQVAE（语义-属性解耦 VQVAE）**

该模块由四个子组件构成：

1. **编码器 $f$（语义-属性解耦编码器）**：输入原始运动 $X$，通过因果信息瓶颈提取语义嵌入 $S = f(X)$。编码器被训练为从 $X$ 中剥离属性信息，产生属性无关的语义表征。
2. **代理属性分类器 $h$**：估计条件分布 $p(A|S)$，用于计算熵损失 $\mathcal{L}_{entropy}$，强制最小化 $I(S;A)$，确保 $S$ 不包含属性信息。
3. **向量量化（Codebook）**：将连续语义嵌入量化为离散语义令牌 $Y$，为后续的生成式建模提供离散表示。
4. **解码器 $g$**：以语义令牌 $S$ 和属性标签 $A$（one-hot 编码后经 MLP 融合）为条件，重建原始运动 $\hat{X} = g(S, A)$。

**阶段二：语义生成 Transformer**

该模块采用 **MoMask**（Guo et al., 2024a）的架构，以 BERT 风格的掩码预测方式从文本中预测语义令牌。具体而言，模型以 CLIP 文本特征为条件，预测随机掩码的语义令牌。推理时，预测出的语义令牌与用户指定的属性输入结合，通过 Decoup-VQVAE 的解码器生成属性感知的人体运动。

### 因果信息瓶颈目标

整个 Decoup-VQVAE 的训练围绕 CIB 目标函数展开：

$$CIB(X,Y,S,A) = I(X;S,A) + I(Y;S) - I(S;A) - \lambda I(X;S)$$

其中：
- $I(X;S,A)$ 鼓励语义和属性共同保留运动的重建信息；
- $I(Y;S)$ 增强语义令牌与量化索引的互信息，确保语义令牌的因果性；
- $-I(S;A)$ 强制语义令牌与属性解耦；
- $-\lambda I(X;S)$ 作为信息瓶颈项，限制从原始运动 $X$ 到语义 $S$ 的信息流，仅保留对动作语义必要的信息。

### 总损失函数

Decoup-VQVAE 的总损失为三项的加权组合：

$$\mathcal{L}_{overall} = \mathcal{L}_{vqvae} + \alpha \mathcal{L}_{entropy} + \lambda \mathcal{L}_{bottleneck}$$

- $\mathcal{L}_{vqvae}$：标准 VQVAE 的重建损失和承诺损失；
- $\mathcal{L}_{entropy}$：通过最小化条件熵 $H(A|S)$ 来减少 $I(S;A)$，实现属性解耦；
- $\mathcal{L}_{bottleneck}$：迫使原始运动和反事实运动（相同语义 $S$ 但随机化属性 $A^{-}$）的语义嵌入相近，限制 $X$ 到 $S$ 的信息流。

超参数经验设置为 $\alpha = 0.01$，$\lambda = 0.5$。

### 推理流程

推理时，用户提供文本描述和期望的属性标签。语义生成 Transformer 从文本中预测语义令牌，随后这些令牌与属性输入一同送入 Decoup-VQVAE 的解码器，生成符合文本语义且体现指定属性特征的运动序列。由于语义令牌已剥离属性信息，属性控制完全由解码器端的属性输入实现，二者互不干扰。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2506_21912/figures/005_Figure_4.jpg]]
*Figure 4: Overall architecture of our proposed AttrMoGen. The encoder of Decoup-VQVAE uses a causal information bottleneck to decouple action semantics from human attributes, producing attribute-free semantic tokens. The decoder then reconstructs motion from these semantic tokens and attribute labels. The Semantics Generative Transformer predicts semantic tokens from textual input, which are subsequently combined with attribute inputs to generate attribute-aware human motions during inference*

AttrMoGen 的核心由两个模块构成：**语义-属性解耦 VQVAE（Decoup-VQVAE）** 和 **语义生成 Transformer**。Decoup-VQVAE 负责从原始运动数据中提取无属性的语义令牌，语义生成 Transformer 则从文本输入预测这些语义令牌，推理时将预测的语义令牌与用户指定的属性标签结合，通过解码器生成属性感知的运动。

### 因果信息瓶颈目标函数

Decoup-VQVAE 的设计基于结构因果模型（SCM），其核心思想是将运动数据 $X$ 分解为因果的动作语义 $S$ 和非因果的属性 $A$。为实现这一解耦，论文提出了因果信息瓶颈（Causal Information Bottleneck, CIB）目标函数：

$$CIB(X,Y,S,A) = I(X;S,A) + I(Y;S) - I(S;A) - \lambda I(X;S)$$

其中各项含义如下：
- $I(X;S,A)$：最大化语义 $S$ 和属性 $A$ 对原始运动 $X$ 的互信息，保证重建质量；
- $I(Y;S)$：最大化语义令牌 $Y$（量化后的 $S$）与语义 $S$ 的互信息，确保语义保留；
- $-I(S;A)$：最小化语义 $S$ 与属性 $A$ 的互信息，强制解耦；
- $-\lambda I(X;S)$：瓶颈项，限制原始运动 $X$ 到语义 $S$ 的信息流，仅保留因果相关的语义信息。

### 属性解耦：熵损失

直接优化 $I(S;A)$ 难以实现，论文利用互信息的上界将其转化为可优化的条件熵最小化问题：

$$I(S;A) \leq \log |A| - \mathbb{E}_{s \sim p(S)} H(A|S=s)$$

由此引入一个代理属性分类器 $h$，估计 $p(A|S)$，并定义熵损失：

$$\mathcal{L}_{entropy} = -\sum_{i=1}^{B} H(A|S=s_i)$$

通过最小化该损失，迫使语义嵌入 $S$ 不携带属性信息，从而实现语义与属性的解耦。

### 信息瓶颈：瓶颈损失

为限制 $X$ 到 $S$ 的信息流（即 $-\lambda I(X;S)$ 项），论文通过反事实机制构造瓶颈损失。具体而言，将原始属性 $A$ 随机化为反事实属性 $A^{-}$，生成反事实运动 $X^{-} = g(S, A^{-})$，然后迫使原始语义嵌入 $S$ 与反事实语义嵌入 $S^{-}$ 在通道维度上对齐：

$$\mathcal{L}_{bottleneck} = \| \tilde{D}(X, X^{-}) - I \|_F^2$$

其中 $\tilde{D}(X, X^{-})_{ij} = \text{Cosine}(S[:,i], S^{-}[:,j])$ 为余弦相似度矩阵，$I$ 为单位矩阵。该损失强制同一通道的语义特征在属性变化时保持一致，从而滤除属性相关信息。

### 总损失函数

Decoup-VQVAE 的总损失由 VQVAE 标准重建损失、熵损失和瓶颈损失加权组合：

$$\mathcal{L}_{overall} = \mathcal{L}_{vqvae} + \alpha \mathcal{L}_{entropy} + \lambda \mathcal{L}_{bottleneck}$$

其中 $\alpha$ 和 $\lambda$ 为超参数，默认设置为 $\alpha=0.01$、$\lambda=0.5$。消融实验表明，移除熵损失（w/o entropy）会导致 FID 从 0.089 急剧恶化至 0.489，验证了 $-I(S;A)$ 项对消除语义令牌中属性信息的关键作用；移除瓶颈损失（w/o bottleneck）同样使 FID 升至 0.184，证明限制 $X$ 到 $S$ 信息流的必要性。

### 语义生成 Transformer

在获得解耦的语义令牌后，AttrMoGen 采用一个基于 **MoMask** 架构的语义生成 Transformer，以文本的 CLIP 特征为条件，通过掩码预测方式从文本生成语义令牌序列。推理时，该模块预测的语义令牌与用户指定的属性标签（经 one-hot 编码和 MLP 融合）共同输入 Decoup-VQVAE 的解码器 $g$，生成符合文本语义且体现指定属性特征的人体运动。

## 实验与关键发现

### 主实验结果

AttrMoGen 在 HumanAttr 测试集上全面超越现有文本驱动运动生成方法，验证了属性感知解耦的有效性。如表 3 所示，与强基线 **MoMask** 相比，AttrMoGen 的 FID 从 0.245 降至 0.089（降幅 63.7%），MM-Dist 从 2.602 降至 2.266，R-Precision Top-1 从 0.685 提升至 0.705。这表明解耦后的语义令牌保留了更纯粹的动作语义，同时属性条件的引入显著提升了生成运动与真实分布的对齐程度。

在属性分组评估中（表 4），AttrMoGen 在不同性别和年龄组上均保持一致的性能优势，说明因果解耦机制对不同属性组合具有鲁棒性。值得注意的是，基线方法在属性分布稀疏的子集上性能波动较大，而 AttrMoGen 的 FID 在各组间更为稳定，间接证明属性信息已被有效从语义令牌中剥离。

### 消融实验

消融实验从三个维度验证了 AttrMoGen 各组件的关键作用（表 2、表 6）：

**属性解耦策略对比。** 将属性短语直接拼接到文本提示中的两种基线策略均不及 AttrMoGen。仅测试时拼接（`w/ attr test`）导致性能严重退化，说明模型无法从简单的文本增强中习得属性-语义分离；训练时加入属性提示（`w/ attr train`）虽有所改善，但 FID 仍显著高于 AttrMoGen。这一对比揭示了显式因果解耦的必要性：属性信息在原始运动数据中与语义高度耦合，仅靠数据层面的提示工程无法实现有效分离。

**熵损失的关键作用。** 移除熵损失项（`w/o entropy`）后，FID 从 0.089 飙升至 0.489，增幅超过 4 倍。熵损失 $ \mathcal{L}_{entropy} $ 通过最小化 $ H(A|S) $ 来降低 $ I(S;A) $，其实质是迫使语义嵌入 $ S $ 无法被属性分类器 $ h $ 准确识别。移除该项意味着编码器失去了消除属性信息的能力，语义令牌中残留的属性信号干扰了后续的文本-语义对齐。

**瓶颈损失的辅助作用。** 移除瓶颈损失（`w/o bottleneck`）使 FID 升至 0.184。瓶颈损失 $ \mathcal{L}_{bottleneck} $ 通过约束原始运动与反事实运动（属性随机化）的语义嵌入相似，限制了 $ X $ 到 $ S $ 的信息流，确保仅保留与动作语义相关的信息。其缺失虽不如熵损失影响剧烈，但仍导致语义令牌中混入冗余信息，降低了生成质量。

### 属性控制能力验证

AttrMoGen 的属性控制精度通过分类准确率量化（表 5）。当使用真实属性标签控制生成时，属性分类器对生成运动的识别准确率显著高于随机属性标签，证明解码器 $ g(S, A) $ 能够根据输入的 $ A $ 可靠地调节运动模式。t-SNE 可视化（图 6）进一步提供了定性证据：AttrMoGen 的 VQVAE 嵌入未呈现性别聚类，而生成运动的特征在属性控制下形成了清晰的性别分组，表明编码器成功去除了属性信息，解码器则有效利用了属性输入。

### 失败模式与局限

尽管 AttrMoGen 在离散属性上表现优异，其属性控制机制存在粒度限制。当前框架将年龄分为 0-18、19-35 等离散区间，可能无法捕捉连续年龄变化带来的渐进式运动差异。此外，数据集中约 74% 样本包含体重和身高信息（图 7），但主要实验仅使用年龄和性别，连续体格属性未被充分利用。部分子数据集（如 KIT）中 90% 受试者年龄集中在 18-45 岁，可能导致模型在极端年龄（如幼儿或高龄）下的泛化能力未经充分验证，该结论需人工确认。

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2506_21912/figures/006_Table_2.jpg]]
*Table 2: Results of ablation studies. “↑” denotes that higher is better. “↓” denotes that lower is better. The default settings for AttrMogen are λ = 0.5 and*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2506_21912/figures/008_Table_4.jpg]]
*Table 4: Performance comparison on different attribute groups. “↑” denotes that higher is better. “↓” denotes that lower is better*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2506_21912/figures/009_Figure_5.jpg]]
*Figure 5: Visualization of generated motions of MoMask and AttrMoGen. As shown, subjects of different attributes exhibit variations in the extent and patterns of movements*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2506_21912/figures/010_Figure_6.jpg]]
*Figure 6: t-SNE visualization with colors representing male and female. The VQVAE embeddings of AttrMoGen exhibit no gender-based clustering, indicating effective removal of gender cues from the motion. Meanwhile, with attributes control input, features of the generated motion by AttrMo-Gen displays distinct gender-based clusters, demonstrating better alignment with attributes input. Best viewed in color*

![[assets/figures/papers/paper_list_l10_https_arxiv_org_abs_2506_21912/figures/012_Table_6.jpg]]
*Table 6: Results of ablation studies. “↑” denotes that higher is better. “↓” denotes that lower is better*

## 定位与知识库关联

### 任务定位与核心差异

AttrMoGen 面向**属性感知的文本驱动人体运动生成**，其核心创新在于将运动分解为因果的动作语义 $S$ 和非因果的人体属性 $A$，并通过结构因果模型（SCM）显式解耦二者。这与现有文本驱动运动生成方法形成根本差异：主流方法（如 **T2M-GPT** (Zhang et al., CVPR 2023)、**MDM** (Tevet et al., ICLR 2022)、**MoMask**、**MLD**、**MotionDiffuse** 等）仅关注文本语义到运动的映射，未显式建模人体属性对运动模式的影响。

论文通过消融实验（Table 6）验证了这一差异的关键性：若仅在测试时将属性短语直接拼接到文本提示中（w/ attr test），性能严重退化；即使在训练和测试时均加入属性文本（w/ attr train），效果仍明显劣于 AttrMoGen 的显式解耦方案。这表明**简单的文本增强无法实现语义与属性的解耦**，显式的因果信息瓶颈机制是必要的。

### 方法组件溯源

AttrMoGen 的两阶段架构可以追溯到以下方法谱系：

**第一阶段：Semantic-Attribute Decoupling VQVAE (Decoup-VQVAE)。** 其基础架构继承自 VQVAE 的离散潜在表示学习范式，但编码器设计引入了**因果信息瓶颈（CIB）** 机制。CIB 目标函数为：
$$CIB(X,Y,S,A) = I(X;S,A) + I(Y;S) - I(S;A) - \lambda I(X;S)$$
其中 $I(Y;S)$ 项保留与文本 $Y$ 因果相关的语义信息，$-I(S;A)$ 项通过最小化互信息消除语义令牌中的属性信息，$-\lambda I(X;S)$ 项限制原始运动 $X$ 到语义令牌 $S$ 的信息流，仅保留必要语义。该公式在信息瓶颈理论框架中引入了因果方向性约束，与标准信息瓶颈形成差异。

属性解耦的具体实现依赖两个关键损失：
- **熵损失** $\mathcal{L}_{entropy}$：通过代理属性分类器 $h$ 估计条件熵 $H(A|S=s)$，最小化该熵以降低 $I(S;A)$，其理论依据为互信息上界 $I(S;A) \leq \log |A| - \mathbb{E}_{s \sim p(S)} H(A|S=s)$。
- **瓶颈损失** $\mathcal{L}_{bottleneck}$：通过反事实运动 $X^{-} = g(S, A^{-})$（随机化原始属性 $A$ 得到 $A^{-}$）约束原始语义嵌入与反事实语义嵌入的余弦相似度矩阵趋近单位矩阵，迫使 $S$ 对属性变化不敏感。

**第二阶段：Semantics Generative Transformer。** 该模块直接采用 **MoMask** 的掩码预测架构，以 CLIP 文本特征为条件预测语义令牌。这一选择基于 MoMask 在文本-运动对齐上的强性能和高效推理能力，AttrMoGen 将其作为语义预测的骨干网络，而非重新设计文本编码器。

### 与现有工作的关系

| 维度 | 现有方法 | AttrMoGen |
|------|---------|-----------|
| 属性建模 | 无显式属性条件；TM2T、T2M、MDM、MLD、MotionDiffuse 等仅基于文本生成 | 属性标签作为独立条件输入解码器 |
| 语义-属性关系 | 语义与属性在运动数据中隐式耦合 | 通过 CIB 显式解耦，语义令牌不包含属性信息 |
| 生成控制 | 文本唯一控制信号 | 文本控制语义 + 属性标签控制运动风格 |
| 风格/属性迁移 | **GenMoStyle** 关注运动风格，但非基于因果解耦 | 通过反事实解码实现属性迁移（Figure 8） |

### 适用边界与局限

**已验证的有效范围：**
- 属性类型：离散的年龄组（0-18, 19-35, 36-55, 56+）和性别（男/女）
- 数据来源：HumanAttr 数据集（整合自 HumanML3D、KIT 等多个子集，共 18.2k 序列，640 名受试者）
- 运动表示：3D 标记点坐标序列 $L \times V \times 3$

**已知局限（需人工验证）：**
1. **连续属性未充分利用**：数据集中约 74% 样本包含体重和身高信息（Figure 7），但主要实验仅使用年龄和性别作为离散标签。将连续属性（如精确年龄、BMI）融入该框架的能力尚未验证。
2. **离散分组的粒度限制**：年龄分组（如 0-18, 19-35）可能无法捕捉连续的年龄相关运动差异，模型对组内细粒度变化的敏感性未知。
3. **数据多样性偏差**：部分子数据集存在年龄分布不均问题（如 KIT 中 90% 受试者年龄在 18-45 岁），可能影响模型在极端年龄段的泛化评估。
4. **属性类型的可扩展性**：当前框架仅验证了年龄和性别，推广至更多样属性（如运动风格、身体质量指数、情绪状态）的有效性待探索。

### 开放问题

1. **连续属性建模**：如何将精确的连续属性值（年龄、体重、身高）融入 CIB 框架，实现更细粒度的运动控制？可能需要将离散属性分类器替换为回归器，或采用条件连续归一化流。
2. **跨域泛化**：该因果解耦机制能否推广至真实视频数据中的运动生成？视频中的属性信息（如衣着、体型）可能与运动语义存在更复杂的混杂。
3. **未见属性组合**：模型在训练时未见过的属性组合（如极端年龄 + 特定动作类型）下的生成质量和语义保持能力如何？
4. **反事实生成的可靠性**：Figure 8 展示了反事实运动可视化，但缺乏系统的量化评估（如用户研究或属性分类一致性指标），该能力的鲁棒性需要进一步验证。

## 原文 PDF

![[paperPDFs/arxiv_2025/Generating_Attribute-Aware_Human_Motions_from_Textual_Prompt.pdf]]
