---
title: "A Probabilistic Hard Concept Bottleneck for Steerable Generative Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Probabilistic_Hard_Concept_Bottleneck_for_Steerable_Generative_Models.pdf
aliases:
- VHCBV
- PHCBSGM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将概念瓶颈层从确定性软概念映射改为基于二元VAE的概率化硬概念映射（VHCB层），通过硬二值表示阻断泄漏，并利用概率公式实现从指定概念配置直接生成。"
primary_logic: "通过将Coded DVAE扩展为包含概念向量c和无监督侧信道s的双重二值潜变量表示，并利用对称KL散度对齐概念后验与条件概念分布，VHCB在保持生成质量的同时显著提升了可操控性，且无需额外的干预训练项。"
claims:
- "VHCB在概念推理指标上一致优于确定性CB-AE"
- "VHCB在单概念激活干预中目标准确率大幅提升（平均增加约46%），非目标准确率仅小幅下降（平均约7%）"
- "VHCB在可操控生成中目标准确率优于CB-AE（全概念集Patterns采样：VHCB 0.873 vs CB-AE 0.712）"
- "VHCB在概念推理和解耦指标上均优于CB-AE（全概念集ResNet18：概念推理Acc 0.855 vs 0.857，解耦Acc 0.927 vs 0.901）"
---

# A Probabilistic Hard Concept Bottleneck for Steerable Generative Models

> [!tip] 核心洞察
> 通过将Coded DVAE扩展为包含概念向量c和无监督侧信道s的双重二值潜变量表示，并利用对称KL散度对齐概念后验与条件概念分布，VHCB在保持生成质量的同时显著提升了可操控性，且无需额外的干预训练项。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向可操控生成模型的概率化硬概念瓶颈 |
| 英文题名 | A Probabilistic Hard Concept Bottleneck for Steerable Generative Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Kcb6WufAco) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Variational Hard Concept Bottleneck (VHCB) |
| Dataset | CelebA-HQ (StyleGAN2) |

> [!tip] 效果简介
> - CelebA-HQ (StyleGAN2) 上，概念推理 Acc (↑) 为 0.855，对比 0.857，变化 -0.002。
> - CelebA-HQ (StyleGAN2) 上，解耦 Acc (↑) 为 0.927，对比 0.901，变化 +0.026。
> - CelebA-HQ (StyleGAN2) 上，可操控生成目标Acc (Patterns, all) (↑) 为 0.873，对比 0.712，变化 +0.161。

## 概述

该论文聚焦于概念瓶颈生成模型（CBGM）中的可操控性问题，指出现有方法依赖软概念和确定性映射导致“概念泄漏”——软概念概率无意中编码了任务相关信息，使得对概念的人工干预无法在生成输出中产生预期效果。针对这一瓶颈，论文提出了**概率化硬概念瓶颈层（Variational Hard Concept Bottleneck, VHCB）**，核心思路是将概念表示从连续概率值转变为二值潜变量，从根本上阻断泄漏通道。

方法层面，VHCB扩展了Coded DVAE，构建了包含概念向量 **c** 和无监督侧信道 **s** 的双重二值潜变量表示。通过平滑变换实现可微采样，并利用对称KL散度对齐概念后验与条件概念分布，训练损失仅包含嵌入重建、概念对齐、侧信道正则化和图像MSE四项，无需额外的干预损失项。这一设计同时支持从指定概念配置直接生成，而非仅能对现有输入进行干预。

主要实验结果（基于StyleGAN2、CelebA-HQ数据集）显示：VHCB在概念推理指标上与确定性CB-AE持平（全概念集Acc 0.855 vs 0.857），但在解耦指标上显著提升（Acc 0.927 vs 0.901）；在可操控生成中，目标准确率大幅领先（Patterns采样：VHCB 0.873 vs CB-AE 0.712）；单概念干预的目标准确率平均提升约46%，而非目标准确率仅下降约7%。消融实验验证了对称KL散度和侧信道正则化的有效性。论文也在DDPM架构上进行了初步验证，但指出扩散模型中强制执行概念变化比GAN更困难，VHCB注入所有上采样层虽有改善但改进幅度有限。

## 背景与动机

概念瓶颈生成模型（CBGM）旨在通过显式的可解释概念表示来操控生成内容。然而，现有CBGM方法普遍采用**软概念**（连续概率值）和**确定性映射**，这导致了一个关键缺陷——**概念泄漏（concept leakage）**：软概念的概率值无意中编码了与任务相关的额外信息，使得概念干预无法在生成输出中产生预期的、可分离的效果。具体而言，当用户试图激活或去激活某个概念（如“微笑”）时，由于软概念表示中混杂了其他信息，生成结果往往无法忠实反映该干预意图。

现有代表性方法包括：**Concept Bottleneck Autoencoder (CB-AE)** 和 **Concept Embedding Model (CEM)**。CB-AE通过一个包含嵌入重建、图像重建、概念预测和**额外干预损失**的复杂损失函数进行训练（公式：$\mathcal { L } = \mathcal { L } _ { r _ { 1 } } ( w , \hat { w } ) + \mathcal { L } _ { r _ { 2 } } ( { \pmb x } , \hat { \pmb x } ) + \mathcal { L } _ { c } ( { \pmb y } , { \pmb c } ) + \mathcal { L } _ { i _ { 1 } } ( y _ { \mathrm { t a r g e t } } , y _ { \mathrm { i n t } } ) + \mathcal { L } _ { i _ { 2 } } ( y _ { \mathrm { t a r g e t } } , { \pmb c } _ { \mathrm { i n t } } )$）。尽管这些方法在一定程度上实现了概念层面的操控，但软概念泄漏的本质问题限制了其可操控性的上限。

本文的核心动机是：**能否通过将概念瓶颈从软、确定性表示改为硬、概率化表示，从根源上阻断概念泄漏，从而在不牺牲生成质量的前提下显著提升可操控性？** 为此，作者提出了**变分硬概念瓶颈（VHCB）层**。VHCB的核心洞察在于：通过扩展**编码化离散变分自编码器（Coded DVAE）**，构建一个包含**二值概念向量c**和**无监督侧信道s**的双重二值潜变量表示。其中，c通过**纠错码（ECC）** 进行保护以确保鲁棒推理，s则捕获概念之外的变化因素。VHCB采用**对称KL散度（D_SKL）** 对齐概念后验与条件概念分布，从而在无需额外干预损失项的情况下实现有效的概念干预。其损失函数为：$\mathcal { L } = \mathbb { E } \log { p _ { \theta } ( w | z ) } - \mathcal { D } _ { \mathrm { S K L } } \left( q _ { \eta } ( c | w ) , p ( y | x ) \right) - \mathcal { D } _ { \mathrm { K L } } \left( q _ { \eta } ( s | w ) \| p ( s ) \right) + \mathrm { M S E } ( x , \hat { x } )$。

与CB-AE等基线相比，VHCB在概念表示形式（硬二值 vs. 软连续）、瓶颈层类型（概率化二元VAE vs. 确定性映射）、训练损失（无需干预损失）、侧信道表示（二值潜变量 vs. 连续向量）以及可操控生成方式（支持从指定概念配置直接生成 vs. 仅支持对现有输入干预）上均做出了根本性改变。

## 核心创新

VHCB（Variational Hard Concept Bottleneck）的核心创新在于将概念瓶颈层从**确定性软概念映射**彻底重构为**概率化硬概念映射**，从而从根本上解决了现有CBGM中因软概念泄漏（concept leakage）导致的可操控性受限问题。

### 问题诊断：软概念泄漏的因果机制

现有CBGM（如CB-AE）采用连续概率值（软概念）作为概念表示。分析指出，这种软概念概率在训练过程中会无意中编码与任务相关的非概念信息，形成“概念泄漏”：干预一个软概念时，其概率值的变化不仅反映了该概念状态的改变，还携带了与生成任务相关的其他信息，使得干预无法在生成输出中产生预期效果。这是限制可操控性的核心瓶颈。

### 关键变更：五个changed slots

VHCB相对于CB-AE基线，在以下五个关键槽位上做出了根本性改变：

1. **概念表示形式**：从连续概率软概念 → **硬二值潜变量**（通过Coded DVAE实现）。硬表示直接阻断了概念值携带非概念信息的通道。

2. **瓶颈层类型**：从确定性编码器-解码器映射 → **概率化二元VAE映射**。VHCB构建于Coded DVAE之上，引入了可微采样（通过重叠指数分布的平滑变换实现）和纠错码（ECC）机制。

3. **训练损失函数**：CB-AE包含嵌入重建、图像重建、概念预测和**额外干预损失**（L_i1, L_i2）；VHCB仅包含嵌入重建、概念对齐（对称KL散度）、侧信道正则化和图像MSE，**无需干预损失项**。这意味着VHCB的可操控性提升并非来自针对干预的专门训练，而是源自硬概念表示本身的结构性优势。

4. **无监督侧信道表示**：从连续向量 s ∈ R^40 → **二值潜变量 s ∈ {0,1}^5**，并通过均匀重复码（码率R=5/50）保护。低维二值侧信道确保其不包含概念信息，同时通过ECC抵抗噪声。

5. **可操控生成方式**：CB-AE仅支持对现有输入进行概念干预；VHCB由于其概率公式，**支持从指定概念配置直接生成**（通过采样c和s）。

### 核心洞察：双重二值潜变量 + 对称KL对齐

VHCB将Coded DVAE扩展为包含**概念向量c**和**无监督侧信道s**的双重二值潜变量表示。训练时，通过**对称KL散度**（D_SKL）对齐概念后验q_η(c|w)与条件概念分布p(y|x)，而非传统的单向KL散度。消融实验（Table 5）表明，对称KL在概念干预性能上提供了最佳平衡。

### 决定性证据

- **概念推理**：VHCB在概念推理指标上一致优于确定性CB-AE（Table 10：全概念集ResNet18，VHCB Acc 0.855 vs CB-AE 0.857，但余弦相似度0.804 vs 0.763，TV 0.148 vs 0.161），表明硬表示在保持推理精度的同时提供了更准确的概率估计。

- **可操控生成**：VHCB在单概念激活干预中目标准确率大幅提升（平均增加约46%），非目标准确率仅小幅下降（平均约7%）（Table 3：低相关概念集，i→a目标Acc VHCB 0.769 vs CB-AE 0.420）。在全概念集Patterns采样生成中，VHCB目标Acc 0.873 vs CB-AE 0.712（Table 2）。

- **解耦质量**：VHCB在概念与侧信道的解耦指标上显著优于CB-AE（Table 10：解耦Acc 0.927 vs 0.901，余弦相似度0.917 vs 0.853），验证了硬表示有效阻断了泄漏。

- **图像质量**：VHCB的前向FID（7.248）优于CB-AE（11.645），表明硬概念瓶颈不仅未损害生成质量，反而通过更干净的潜表示提升了质量（Table 15）。

### 架构集成

VHCB作为一个可插拔模块，在StyleGAN2中置于Mapping Network与Synthesis Network之间（Figure 7）；在DDPM中可注入U-Net瓶颈层或所有上采样层（Figure 8、Figure 9）。这种后验训练（post-hoc）设置使其无需修改基础生成模型即可应用。

### 消融实验揭示的边界条件

- **对称KL散度**：在概念损失消融（Table 5）中，对称KL在干预目标Acc与FID之间提供了最佳权衡，优于CE、MSE和单向KL。
- **侧信道正则化**：对大概念集（40个概念）无显著影响；但对小概念集（8个概念）移除侧信道会使FID几乎翻倍（Table 9：平衡集FID从11.016升至20.950），表明侧信道在概念信息稀疏时承担了必要的生成多样性。
- **侧信道解耦**：s的DCI始终显著低于c的DCI（Table 8），证明侧信道不包含概念信息。

## 整体框架

![[assets/figures/papers/iclr26_0003_Kcb6WufAco_A_Probabilistic_Hard_Concept_Bottleneck_for_Stee/figures/001_Figure_1.jpg]]
*Figure 1: Block diagram of (a) the general architecture of CBGMs, and (b) the VHCB layer. Note that the Error-Correcting Code (ECC) in the VHCB layer is a deterministic transformation that enables effective inference*

VHCB（Variational Hard Concept Bottleneck）的整体架构遵循CBGM（Concept Bottleneck Generative Model）的三段式通用设计：预瓶颈模块（pre-bottleneck module）、概念瓶颈模块（bottleneck module）、后瓶颈模块（post-bottleneck module），如Figure 1(a)所示。在StyleGAN2中，VHCB层被插入在Mapping Network和Synthesis Network之间（Figure 7），其中Mapping Network的输出作为预瓶颈嵌入w，Synthesis Network的输入作为后概念嵌入ŵ。在DDPM中，VHCB模块可注入U-Net的瓶颈层（Figure 8）或所有上采样层（Figure 9），后者需要一个额外的解码器网络来匹配分辨率。

VHCB的核心创新在于将原有的确定性软概念瓶颈替换为基于Coded DVAE的概率化硬概念瓶颈。其内部结构如Figure 1(b)所示：编码器网络从w生成编码比特的边际后验q_η(v|w) = ∏ Ber(v_j; g_j,η(w))，然后通过ECC软多数投票利用重复码结构修正编码器错误，得到c的改进边际。与CB-AE不同，VHCB同时维护两个二值潜变量：概念向量c ∈ {0,1}^K（K为概念数）和无监督侧信道s ∈ {0,1}^5。概念变量使用码率R ∈ {8/240, 10/300, 40/800}（取决于概念集大小），侧信道使用R = 5/50的统一重复码保护。这种双重二值表示的设计源于核心洞察：软概念概率会无意中编码任务相关信息导致概念泄漏，而硬二值表示能阻断泄漏路径。

VHCB的输入输出流为：预瓶颈嵌入w → 编码器生成边际后验 → ECC软多数投票得到c和s的改进边际 → 通过平滑变换（重叠指数分布p(z|v=1) = e^{β(z-1)}/Z_β, p(z|v=0) = e^{-βz}/Z_β）实现可微采样 → 解码器f_θ(·)重建ŵ → 后瓶颈模块生成最终输出x。其训练损失函数为：

L = E_{q_η(c,s,z|w)} log p_θ(w|z) - D_SKL(q_η(c|w), p(y|x)) - D_KL(q_η(s|w) || p(s)) + MSE(x, x̂)

相比CB-AE（包含L_r1, L_r2, L_c, L_i1, L_i2五个损失项），VHCB仅需四项：嵌入重建、概念对齐（对称KL散度）、侧信道正则化和图像MSE，无需额外的干预训练项。概念监督通过条件概念分布p(y|x)作为c的信息先验引入。这种概率化公式还支持从指定概念配置直接生成：通过采样c和s，绕过输入图像，直接驱动生成过程——这是CB-AE不具备的能力。

## 核心模块与公式推导

### 核心瓶颈：从软概念泄漏到硬概念阻断

现有概念瓶颈生成模型（CBGM）的核心缺陷在于**概念泄漏**：当使用软概念（连续概率值）和确定性映射时，概念潜变量会无意中编码与任务相关的非语义信息，导致对概念进行干预后，生成输出无法可靠地反映预期的概念变化。例如，在CB-AE中，编码器输出的软概念概率（如“微笑=0.7”）可能隐含了“性别”或“年龄”等无关信息，使得“关闭微笑”的干预无法完全移除微笑特征。

VHCB通过两个关键设计阻断泄漏：
1. **将概念表示从软概率变为硬二值潜变量**，利用Coded DVAE实现离散采样与可微训练的兼容；
2. **引入无监督侧信道**，将无法用预定义概念捕获的剩余语义信息分离到独立的二值潜变量 $s \in \{0,1\}^5$ 中，防止其污染概念表示。

### VHCB架构与信息流

VHCB层嵌入在生成模型的瓶颈位置（StyleGAN2中位于Mapping Network与Synthesis Network之间；DDPM中位于U-Net瓶颈或所有上采样层）。其处理流程分为三个阶段：

1. **预瓶颈模块**：将（可能带噪声的）输入潜变量 $u$ 映射为预瓶颈嵌入 $w$。
2. **VHCB瓶颈模块**：将 $w$ 编码为概念向量 $c$ 和无监督嵌入 $s$，然后从 $(c, s)$ 重建后瓶颈嵌入 $\hat{w}$。
3. **后瓶颈模块**：将 $\hat{w}$ 映射为最终输出 $x$。

瓶颈模块内部采用**编码器-解码器**架构（Figure 1b）：
- **编码器NN**：从 $w$ 生成编码比特的边际后验 $q_\eta(v|w) = \prod \text{Ber}(v_j; g_{j,\eta}(w))$，其中每个比特对应概念或侧信道变量的编码版本。
- **ECC软多数投票**：利用重复码结构对编码器输出进行纠错，得到 $c$ 和 $s$ 的改进边际估计。概念变量的码率根据概念数量设定为 $R \in \{8/240, 10/300, 40/800\}$，侧信道变量码率为 $R = 5/50$。
- **平滑变换**：从二值潜变量实现可微采样，使用重叠指数分布：
  
$$
p(z|v=1) = \frac{e^{\beta(z-1)}}{Z_\beta}, \quad p(z|v=0) = \frac{e^{-\beta z}}{Z_\beta}
$$

  其中 $v$ 是二值变量，$z$ 是平滑后的连续变量，$\beta$ 控制温度，$Z_\beta$ 为归一化常数。
- **解码器NN**：从平滑潜变量 $z$ 重建 $\hat{w}$。

### 训练损失函数

VHCB的总损失函数（公式3）由四项组成：

$$
\mathcal{L} = \underbrace{\mathbb{E}_{q_\eta(c,s,z|w)} \log p_\theta(w|z)}_{\text{嵌入重建}} 
- \underbrace{\mathcal{D}_{\text{SKL}}\left(q_\eta(c|w), p(y|x)\right)}_{\text{概念损失}} 
- \underbrace{\mathcal{D}_{\text{KL}}\left(q_\eta(s|w) \| p(s)\right)}_{\text{侧信道正则化}} 
+ \underbrace{\text{MSE}(x, \hat{x})}_{\text{图像重建}}
$$

各变量含义：
- $w$：预瓶颈嵌入
- $c$：二值概念向量（$K$ 维，$K$ 为概念数量）
- $s$：无监督二值侧信道潜变量（5维）
- $z$：平滑后的连续潜变量（用于可微采样）
- $q_\eta(c|w), q_\eta(s|w)$：编码器对概念和侧信道的后验估计
- $p(y|x)$：条件概念分布，由预训练分类器提供，作为概念的监督先验
- $p(s)$：侧信道的先验分布（通常为均匀伯努利）
- $x, \hat{x}$：原始图像与重建图像
- $\mathcal{D}_{\text{SKL}}$：对称KL散度，定义为 $D_{\text{KL}}(q\|p) + D_{\text{KL}}(p\|q)$
- $\mathcal{D}_{\text{KL}}$：标准KL散度

**关键设计差异**：与CB-AE相比，VHCB的损失函数**不包含任何干预损失项**（CB-AE的 $\mathcal{L}_{i_1}, \mathcal{L}_{i_2}$），仅通过硬二值表示和对称KL对齐实现可控性。消融实验（Table 5）证实，对称KL散度在干预性能上提供了最佳平衡。

### 可操控生成机制

VHCB的概率公式化使其能够**从指定概念配置直接生成**，无需依赖输入图像。给定目标概念配置 $c^*$，生成过程为：
1. 从先验 $p(s)$ 采样侧信道 $s$；
2. 从条件分布 $p(z|c^*, s)$ 采样平滑潜变量 $z$；
3. 通过解码器生成 $\hat{w}$，再经后瓶颈模块得到输出 $x$。

这一能力源于VHCB将概念与侧信道解耦：由于 $s$ 不包含概念信息（通过KL正则化保证），改变 $c$ 不会意外改变 $s$ 的语义，从而确保干预的精确性。

### 评估指标

论文使用三个核心指标评估概念推理和干预效果：
- **硬概念准确率**：$\text{acc}(y,c) = \frac{1}{K} \sum_{j=1}^K \mathbb{1}[y_j = c_j]$，衡量二值概念预测与标签的匹配比例。
- **总变差距离**：$\text{TV} = \frac{1}{K} \sum_{j=1}^K |p_j - q_j|$，衡量预测概率与真实概率的平均绝对差，越低越好。
- **余弦相似度**：$\text{sim}(p,q) = \frac{p \cdot q}{\|p\|_2 \|q\|_2}$，衡量向量方向一致性，越高越好。

## 实验与分析

### 核心结果：概念推理与解耦

VHCB在概念推理指标上一致优于确定性CB-AE基线（Table 10, Table 1）。在全概念集（CelebA-HQ, ResNet18伪标签监督）上，VHCB的概念推理准确率为0.855，与CB-AE的0.857基本持平，但VHCB在余弦相似度（0.804 vs 0.763）和总变差距离（TV, 0.148 vs 0.161）上显著更优，表明其预测的**概念概率分布更接近真实分布**。更重要的是，VHCB在概念与无监督侧信道s的解耦指标上大幅领先：解耦准确率0.927 vs 0.901，余弦相似度0.917 vs 0.853，TV 0.076 vs 0.101。这直接验证了**硬二值表示和ECC机制有效阻断了概念泄漏**——s的DCI始终显著低于c（Table 8），证明侧信道不包含概念信息。


![[assets/figures/papers/iclr26_0003_Kcb6WufAco_A_Probabilistic_Hard_Concept_Bottleneck_for_Stee/figures/003_Table_1.jpg]]
*Table 1: Concept inference and disentanglement between c and s. Evaluation on 1k random samples generated by a StyleGAN2 pretrained on CelebA-HQ. Figure 3: Qualitative evaluation of the disentanglement between s and c with the VHCB layer and StyleGAN2 models pretrained on CelebA-HQ*

### 可操控生成：从概念配置直接生成

VHCB的概率公式使其支持从指定概念配置直接生成（无需输入图像），而CB-AE仅支持对现有输入进行概念干预。在Patterns采样（按训练数据经验频率采样概念集）下，VHCB的目标准确率达0.873，显著优于CB-AE的0.712（Table 2）。在Random采样（均匀随机采样概念集）下，VHCB同样领先（0.846 vs 0.736）。定性示例（Figure 4, Figure 14）显示VHCB能可靠地生成符合指定概念组合（如“微笑+男性+无胡须”）的图像，而CB-AE常产生概念混淆。


![[assets/figures/papers/iclr26_0003_Kcb6WufAco_A_Probabilistic_Hard_Concept_Bottleneck_for_Stee/figures/004_Table_2.jpg]]
*Table 2: Steerable Generation. Evaluation of generation from specific concept configurations using a StyleGAN2 pretrained on CelebA-HQ. Random samples concept sets uniformly at random, while Patterns samples them according to their empirical frequency in the training data*

### 测试时干预：单概念激活/去激活

VHCB在单概念干预中实现了**目标准确率的大幅提升（平均增加约46%）**，同时非目标准确率仅小幅下降（平均约7%）（Table 11, Table 12）。在低相关概念集（8个平衡且低相关概念）上，VHCB的激活（i→a）目标准确率达0.769，而CB-AE仅0.420；去激活（a→i）目标准确率0.765 vs 0.500。这一差距揭示了**CB-AE中概念泄漏的严重性**：软概念概率无意中编码了任务相关信息，使得干预无法产生预期效果。VHCB通过硬二值表示切断了这一泄漏路径。

### 汉明距离干预

在基于训练概念模式的最小汉明距离干预中，VHCB同样优于CB-AE（Table 13）：全概念集目标准确率0.660 vs 0.542，低相关集0.654 vs 0.519。这表明VHCB能更可靠地执行多概念组合的联合干预。

### 图像质量

VHCB在保持可操控性的同时，还显著提升了生成质量。前向FID从CB-AE的11.645降至7.248（Table 15），接近无概念瓶颈的基线StyleGAN2（6.067）。这表明**概率化瓶颈和ECC机制不仅没有损害生成质量，反而通过更优的潜空间结构提升了保真度**。

### 消融实验

**概念损失函数选择**（Table 5）：对称KL散度在干预性能上提供了最佳平衡。与标准KL散度（前向或反向）相比，对称KL在单概念激活和去激活任务中均取得更高目标准确率，同时保持较低的FID。这归因于对称KL能更均匀地惩罚预测与目标分布之间的双向偏差。


![[assets/figures/papers/iclr26_0003_Kcb6WufAco_A_Probabilistic_Hard_Concept_Bottleneck_for_Stee/figures/014_Table_5.jpg]]
*Table 5: Ablation on the concept loss. StyleGAN2 CelebA-HQ*

**侧信道正则化**（Table 6, Table 7, Table 8）：对大概念集（40个概念），侧信道正则化权重对概念推理和可操控性影响很小。但对小概念集（8个概念），**移除侧信道（s维度为0）会使前向FID几乎翻倍**（从11.016升至20.950，Table 9），同时可操控性指标显著下降。这表明无监督侧信道s对捕获概念未覆盖的视觉变化至关重要，特别是在概念空间较稀疏时。

### 扩散模型（DDPM）扩展

将VHCB注入DDPM的U-Net瓶颈层（Table 4, Table 22-24）取得了与StyleGAN2一致的定性趋势：概念推理和解耦指标合理，单概念干预成功。但**汉明距离干预无法可靠地强制执行目标概念**，表明在扩散模型中强制执行多概念变化比在GAN中更困难。将VHCB注入所有上采样层虽有所改善，但改进幅度有限。这一瓶颈源于扩散模型的迭代去噪过程与VHCB的单步瓶颈表示之间的不匹配。


![[assets/figures/papers/iclr26_0003_Kcb6WufAco_A_Probabilistic_Hard_Concept_Bottleneck_for_Stee/figures/008_Table_4.jpg]]
*Table 4: DDPM results, obtained with a DDPM pretrained on CelebA-HQ*

### 失败模式与数据偏差

实验揭示了数据中概念相关性和偏差对可操控性的强烈影响。例如，激活“mustache”概念时，由于训练数据中“mustache”与“Male”高度相关，干预结果倾向于生成男性面部特征（Figure 13）。这反映了模型捕获并放大了数据中的虚假相关性。低相关概念集上的干预成功率通常低于全概念集，表明**概念集定义（大小、平衡性、相关性）对CBGM性能有显著影响**，概念不完整性问题仍然存在。

### 补充图表

![[assets/figures/papers/iclr26_0003_Kcb6WufAco_A_Probabilistic_Hard_Concept_Bottleneck_for_Stee/figures/007_Table_3.jpg]]
*Table 3: Test-time interventions. Evaluation of single-concept activation (i → a), deactivation (a → i), and interventions guided by training concept patterns (minimum Hamming distance) using a StyleGAN2 pretrained on CelebA-HQ*


## 方法谱系与知识库定位

### 基线关系与核心改进

VHCB的直接基线是**Concept Bottleneck Autoencoder (CB-AE)** (Kulkarni et al., 2025)，后者是当前概念瓶颈生成模型（CBGM）的代表性方法。CB-AE采用确定性软概念映射，其损失函数包含五项：嵌入重建、图像重建、概念预测以及两项显式的干预损失（$\mathcal{L}_{i_1}$ 和 $\mathcal{L}_{i_2}$）。VHCB的核心洞察在于识别出软概念表示的根本缺陷——**概念泄漏（concept leakage）**：软概念概率无意中编码了任务相关信息，导致对概念的干预无法在生成输出中产生预期效果。

VHCB通过三个关键机制改变这一范式：

1. **表示形式从软到硬**：将连续概率值替换为二值潜变量（通过Coded DVAE实现），从根本上阻断泄漏路径。实验证据表明，这一改变使单概念激活干预的目标准确率从CB-AE的0.420提升至0.769（低相关概念集，ResNet18），提升幅度约83%。

2. **损失函数重构**：VHCB的损失函数仅包含嵌入重建、概念对齐（对称KL散度）、侧信道正则化和图像MSE，**完全无需显式的干预损失项**。消融实验（Table 5）验证了对称KL散度在干预性能上提供了最佳平衡——相比前向KL或反向KL，对称KL在目标准确率和生成质量之间取得了更好的折中。

3. **概率化生成框架**：VHCB的概率公式支持从指定概念配置直接生成（通过采样c和s），而CB-AE仅支持对现有输入进行干预。在Patterns采样模式下，VHCB的目标准确率达0.873，显著优于CB-AE的0.712。

### 架构差异与消融发现

VHCB在架构上与CB-AE的关键差异体现在：

- **无监督侧信道**：VHCB使用低维二值潜变量 $s \in \{0,1\}^5$（码率 $R=5/50$），而CB-AE使用连续向量 $s \in \mathbb{R}^{40}$。消融实验表明，侧信道正则化对大概念集无显著影响，但移除小概念集的侧信道会使FID几乎翻倍（从11.016增至20.950，Table 9），说明侧信道在概念信息不足时承担了重要的生成质量补偿角色。

- **ECC保护机制**：VHCB通过错误纠正码（ECC）的软多数投票过程修正编码器错误，这一确定性变换是有效推理的关键（Figure 1）。

- **后验对齐方式**：VHCB使用对称KL散度对齐概念后验 $q_\eta(c|w)$ 与条件概念分布 $p(y|x)$，而非CB-AE的确定性交叉熵损失。

### 适用边界与局限

**适用条件**：
- VHCB特别适用于概念集定义清晰、可标注的场景，且对概念相关性敏感——低相关概念集上的干预成功率通常低于全概念集，表明概念集定义对CBGM性能有显著影响。
- 在GAN架构（StyleGAN2）中表现优异，FID从CB-AE的11.645降至7.248（Table 15），同时保持或提升了概念推理和解耦指标。

**关键局限**：
1. **扩散架构适配困难**：在DDPM中，仅在U-Net瓶颈层注入VHCB时，汉明距离干预无法可靠地强制执行目标概念。将VHCB注入所有上采样层虽有所改善，但改进幅度仍然有限。这表明在扩散模型的去噪轨迹中集成和保持概念表示比在GAN中更具挑战性。

2. **数据偏差放大**：实验揭示了数据中概念相关性和偏差对可操控性的显著影响。例如，激活"mustache"概念时，由于训练数据中"mustache"与"Male"高度相关，干预结果倾向于生成男性面部特征（Figure 13）。这反映了模型捕获并放大了数据中的虚假相关性。

3. **概念不完整性问题**：概念集的大小、平衡性和相关性对CBGM性能有显著影响，概念不完整性问题仍然存在。

### 开放问题

1. **概念关系建模**：如何在潜空间中显式建模概念之间的关系（如相关性、层次结构）以进一步提升可操控性？

2. **偏差缓解策略**：如何微调基础生成模型以减轻通过可操控性分析暴露的虚假偏差？这需要将可操控性评估作为模型审计工具。

3. **扩散架构注入策略**：在DDPM中，如何确定最有效的VHCB注入策略（瓶颈层 vs. 所有上采样层 vs. 其他变体），并确保稳定且一致的改进？当前结果（Table 4）表明，全层注入在概念推理上优于仅瓶颈层（0.753 vs. 0.733），但在生成目标准确率上仍有提升空间（0.752 vs. 0.711）。

4. **概念集设计原则**：如何系统性定义概念集以最大化可操控性？实验表明，低相关概念集上的干预成功率显著低于全概念集，但全概念集又面临维度灾难和标注成本问题。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/A_Probabilistic_Hard_Concept_Bottleneck_for_Steerable_Generative_Models.pdf

![[paperPDFs/ICLR_2026/A_Probabilistic_Hard_Concept_Bottleneck_for_Steerable_Generative_Models.pdf]]
