---
title: Towards Human-Imperceptible Backdoor Attacks on Text-to-Image Diffusion Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Towards_Human_Imperceptible_Backdoor_Attacks_on_Text_to_Image_Diffusion_Models.pdf
project_link: null
code_link: null
aliases:
- CLBATIDM
- THIBATIDM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 攻击仅在输入提示中同时出现特定同义词（W）和以现在分词短语作状语的句法结构（S）时被激活；该复合触发器是控制模型生成目标图像的关键因果开关。
primary_logic: 通过双模态操纵策略实现高隐蔽 clean-label 后门：在图像域引入潜在空间优化的人类不可感知噪声，在文本域构建基于同义词替换与句法重构的复合语义触发器，并引入覆盖样本防止意外激活，从而在保持视觉-文本语义一致性的同时实现精确的后门植入。
claims:
- 所提方法在三个攻击场景下平均 ASR-H 达到 97.2%，而 FTR-W 和 FTR-S 仅为 4.5% 和 5.7%，表明高攻击成功率和低误触发率。
- 与 dirty-label 基线相比，本文方法的 UCR 为 0%（dirty-label 为 100%），证明投毒样本能够逃避 NSFW 内容过滤器。
- 消融实验表明，移除覆盖样本或仅使用单一文本触发器会导致 FTR 显著升高，验证了复合触发器和覆盖样本的必要性。
- Woman→Nude Woman (Table 2) 上 ASR-H = 99.8%
---

# Towards Human-Imperceptible Backdoor Attacks on Text-to-Image Diffusion Models

> [!tip] 核心洞察
> 通过双模态操纵策略实现高隐蔽 clean-label 后门：在图像域引入潜在空间优化的人类不可感知噪声，在文本域构建基于同义词替换与句法重构的复合语义触发器，并引入覆盖样本防止意外激活，从而在保持视觉-文本语义一致性的同时实现精确的后门植入。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向文本到图像扩散模型的人类不可感知后门攻击 |
| 英文题名 | Towards Human-Imperceptible Backdoor Attacks on Text-to-Image Diffusion Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Wu_Towards_Human-Imperceptible_Backdoor_Attacks_on_Text-to-Image_Diffusion_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Clean-label Backdoor Attack for Text-to-Image Diffusion Models |
| Dataset | Woman→Nude Woman, Average over 3 scenarios |

> [!tip] 效果简介
> - Woman→Nude Woman (Table 2) 上，ASR-H 99.8% vs — (—)。
> - Woman→Nude Woman (Table 3 vs Dirty-label) 上，FTR-W 1.9% vs 19.5% (Dirty-label) (-17.6%)；UCR 0% vs 100% (Dirty-label) (-100%)。
> - Average over 3 scenarios (Table 2) 上，ASR-H 97.2% vs — (—)。

## 概述

### 1. 问题与瓶颈

文本到图像扩散模型（如 Stable Diffusion）的广泛部署使其成为后门攻击的高价值目标。现有攻击主要采用 **dirty-label** 策略：将目标图像与语义不匹配的文本标题配对注入训练集，使模型在推理时遇到特定触发词即生成恶意内容。然而，这种图像-文本语义错配使得投毒样本极易被自动数据清洗工具或人工审核检测，严重限制了攻击的实用性。核心瓶颈在于：**如何在保持图像-文本语义一致性的前提下，实现高成功率、低误触发的后门植入**。

### 2. 核心方法定位

本文提出首个针对文本到图像扩散模型的 **clean-label 后门攻击**，通过双模态操纵策略实现隐蔽且精确的后门注入：

- **文本域**：构建**复合语义触发器**——攻击仅在输入提示中同时满足两个条件时激活：(1) 出现特定同义词替换词 W；(2) 包含以现在分词短语作状语的特定句法结构 S。单条件触发不生效，从而大幅降低误触发率。
- **图像域**：在潜在空间中优化添加人类不可感知的扰动（约束 $\|\delta\|_\infty \leq \epsilon$，默认 $\epsilon=0.10$），使源图像在编码空间接近目标图像，同时保持视觉外观不变。
- **覆盖样本机制**：引入仅含 W 或仅含 S 的干净覆盖样本，防止模型学习到单条件的虚假关联，确保后门仅在双条件同时满足时激活。

与现有方法的关键差异如下：

| 维度 | 现有 dirty-label 攻击 | 本文 clean-label 攻击 |
|------|----------------------|----------------------|
| 投毒方式 | 图像与标题语义不对齐 | 图像与标题语义对齐 |
| 图像触发器 | 无或显式修改 | 潜在空间优化的人类不可感知噪声 |
| 文本触发器 | 显式触发词 | 复合语义触发器（同义词 + 句法结构） |
| 覆盖样本 | 无 | 两类覆盖样本防止意外激活 |

在方法谱系上，本文区别于 **BadT2I**（Zhai et al., ACM Multimedia 2023）的 dirty-label 多模态数据中毒、**BAGM**（Vice et al., IEEE TIFS 2024）的组件级后门注入，以及基于文本反转/DreamBooth 的个性化后门方法（Huang et al., AAAI 2024），首次在 clean-label 设定下实现了文本到图像扩散模型的后门攻击。

### 3. 核心结论与证据强度

**主要结果**（Table 2–3）：

- 在三个攻击场景下，平均 **ASR-H（人工评估攻击成功率）达 97.2%**，其中“Woman → Nude Woman”场景高达 99.8%。
- 与 dirty-label 基线相比，误触发率 **FTR-W 从 19.5% 降至 1.9%**，**FTR-S 仅 4.7%**；不安全内容过滤触发率 **UCR 从 100% 降至 0%**，证明投毒样本可完全逃避 NSFW 内容过滤器。

**消融实验**（Table 4–6）：

- 复合触发器显著优于单一触发器：仅使用 W 或仅使用 S 时，在低 log-likelihood 提示下 ASR 下降，FTR 显著升高。
- 覆盖样本对抑制误触发至关重要：默认比例 1:3:3 下 FTR-W 仅 1.9%，移除覆盖样本后 FTR 大幅上升。
- 投毒样本数量达 70 个时 ASR-H 达 99.9%，继续增加收益递减。

**证据强度评估**：主要结论均有置信度 0.9–0.95 的定量实验支撑，但需注意以下局限：(1) 实验仅基于 Stable Diffusion v1.5，在 SDXL、Imagen 等更大模型上的泛化性未验证；(2) NSFW 自动检测器（ASR-N）在噪声防御条件下可能高估攻击成功率，与人工评估存在不一致；(3) 复合触发器要求提示包含合适的主语名词，否则攻击无法激活。

## 背景与动机

### 文本到图像扩散模型的安全威胁

文本到图像扩散模型（如 Stable Diffusion、DALL·E、Imagen）在生成高质量图像方面取得了显著进展，但其训练依赖大规模网络爬取数据，这为后门攻击提供了可乘之机。攻击者可通过投毒少量训练样本，使模型在特定触发条件下生成攻击者指定的目标图像，而在正常输入下保持正常行为。此类攻击一旦被植入并部署到公开模型中，可能被滥用于生成侵权内容、虚假信息或有害图像，构成严重的安全威胁。

### 现有后门攻击的核心瓶颈

当前针对文本到图像模型的后门攻击主要采用 **dirty-label** 策略，典型代表如 **BadT2I**（Zhai et al., ACM Multimedia 2023）和 **BAGM**（Vice et al., IEEE TIFS 2024）。这类方法在投毒时直接修改训练样本的图像-文本对，使图像被替换为目标图像，但文本标题保持不变或仅做简单修改。其根本问题在于：**被投毒的图像-文本对存在显著的语义错配**——图像内容与文本描述不再一致。这种语义不一致性使得投毒样本容易被自动数据清洗工具（如 CLIP-based 过滤器）或人工审查检测出来，从而大幅降低了攻击的实用性和隐蔽性。

Figure 1 直观展示了这一差异：左侧的 dirty-label 投毒样本中，图像已被替换为裸露人体，但标题仍描述“一位穿着裙子的女性”，语义错配一目了然；而本文提出的 clean-label 攻击（右侧）在保持图像与标题语义一致的前提下，仅引入人类难以察觉的扰动。

### 现有防御与攻击的博弈困境

从防御视角看，现有的数据清洗流程通常依赖多模态模型（如 CLIP）计算图像与文本的相似度，过滤掉相似度低于阈值的样本对。dirty-label 攻击因其固有的跨模态语义不一致，极易被此类过滤器拦截。与此同时，基于文本反转（Textual Inversion）或 DreamBooth 的个性化后门注入方法（Huang et al., AAAI 2024）虽然更为隐蔽，但通常需要攻击者掌握目标概念的少量样本，且攻击触发依赖于显式的稀有触发词，在自然语言提示中的泛化性有限。

### 本文的核心动机与研究问题

上述困境揭示了一个关键研究缺口：**能否设计一种后门攻击，在保持图像-文本语义一致性的前提下实现精确的后门植入，从而同时规避自动数据清洗和人工审查？**

本文的核心动机正是填补这一空白，提出首个面向文本到图像扩散模型的 **clean-label 后门攻击**。其设计目标可分解为三个层次：

1. **语义一致性**：投毒样本的图像与文本标题必须保持语义对齐，使得多模态相似度过滤器无法将其与干净样本区分。
2. **触发隐蔽性**：后门触发机制不能依赖显式的稀有触发词或明显的图像异常，而应嵌入自然语言和图像的细微变化中。
3. **精确可控性**：攻击仅在特定复合条件满足时激活，避免在正常使用中意外触发，从而降低暴露风险。

为实现上述目标，本文引入**双模态操纵策略**：在图像域，通过潜在空间优化注入人类不可感知的噪声扰动；在文本域，构建基于同义词替换与句法重构的复合语义触发器，并辅以覆盖样本防止意外激活。这一设计从根本上改变了后门攻击的隐蔽性范式，将攻击从“显式错配”推向“隐式操纵”。

## 核心创新

本文提出了首个面向文本到图像扩散模型的 **clean-label 后门攻击**，其核心创新在于通过双模态操纵策略，在保持图像-文本语义一致性的前提下实现高隐蔽、高精度的后门植入。图 1 直观对比了传统 dirty-label 攻击与本文 clean-label 攻击的差异：左侧 dirty-label 投毒样本中，图像内容（如女性肖像）与文本描述（如“裸体女性”）存在显著的语义错配，极易被自动数据清洗工具或人工审查发现；而右侧本文方法生成的投毒样本在视觉与文本层面均保持语义对齐，大幅提升了攻击的隐蔽性。

### 关键 changed slots 分析

与现有后门攻击方法相比，本文在四个关键维度上实现了根本性改进：

**1. 投毒方式：从 dirty-label 到 clean-label**

现有方法如 **BadT2I** (Zhai et al., ACM Multimedia 2023) 和 **BAGM** (Vice et al., IEEE TIFS 2024) 均采用 dirty-label 策略，即投毒图像与标题之间存在语义不对齐。这种错配使得投毒样本在 NSFW 内容过滤器下的不可检测率（UCR）高达 100%（Table 3），完全暴露了攻击行为。本文首次将 clean-label 范式引入文本到图像生成模型的后门攻击，确保投毒图像与其标题保持语义一致，使得 UCR 降至 0%，从根本上规避了基于语义一致性的数据清洗防御。

**2. 图像触发器：从显式修改到潜在空间不可感知扰动**

传统后门攻击通常依赖显式的图像修改（如添加可见水印或特定图案），而本文通过在潜在空间中优化最小扰动实现图像注入。具体而言，攻击者求解以下优化问题：

$$\operatorname* { m i n } _ { \delta } \| z _ { s } + \delta - z _ { t } \| _ { 2 } ^ { 2 } \quad \mathrm { s u b j e c t } \ \mathrm { t o } \quad \| \delta \| _ { \infty } \leq \epsilon$$

其中 $z_s$ 和 $z_t$ 分别为源图像和目标图像在 VAE 潜在空间中的编码，$\delta$ 为施加的扰动，约束 $\epsilon = 0.10$ 确保扰动在人类视觉感知阈值之下。该方法使投毒图像在像素空间保持原始外观，但在潜在空间中向目标图像偏移，从而在微调过程中引导模型建立后门关联。

**3. 文本触发器：从显式关键词到复合语义触发器**

现有方法通常使用单一显式触发词（如特定稀有词汇），容易被基于词频的防御检测。本文设计了**复合语义触发器**，由两个正交维度构成：

- **同义词替换（W）**：利用 CLIP 编码器计算图像主要物体与标题中各名词的显著性分数 $s ( n _ { i } ) = \sin ( f _ { v } ( o _ { \mathrm { m a i n } } ) , f _ { t } ( n _ { i } ) )$，选择显著性最高的名词 $\hat { n } ^ { * }$，并在候选同义词集中选取语义最相似的词 $W$ 进行替换，保证标题语义不变。
- **句法结构重构（S）**：将标题改写为以现在分词短语作状语的特定句法结构，引入结构层面的触发条件。

后门仅在输入提示中**同时**包含特定同义词 $W$ 和特定句法结构 $S$ 时激活，这种复合条件的稀疏性从根本上降低了误触发率。

**4. 覆盖样本：从无防护到主动误触发抑制**

现有后门攻击方法未考虑误触发问题。本文创新性地引入两类覆盖样本——仅含同义词替换 $W$ 的 $\mathcal{D}_{cover}^W$ 和仅含句法结构 $S$ 的 $\mathcal{D}_{cover}^S$——并将其与干净样本、投毒样本按 1:3:3 比例混合构造最终训练集：

$$\mathcal { D } _ { p } = \mathcal { D } _ { c l e a n } \cup \mathcal { D } _ { p } \cup \mathcal { D } _ { c o v e r } ^ { W } \cup \mathcal { D } _ { c o v e r } ^ { S }$$

覆盖样本的作用机制在于：通过向模型暴露仅满足单一触发条件的样本并保持其生成结果不变，迫使模型学习“仅当两个条件同时满足时才激活后门”的精确关联，从而有效抑制对单一条件提示的误触发。消融实验（Table 6）证实，移除覆盖样本或调整其比例会导致 FTR 大幅上升，验证了该设计的必要性。

### 创新总结

上述四个 changed slots 构成了一条完整的隐蔽攻击链路：clean-label 投毒保证样本通过内容审查，潜在空间扰动保证图像视觉不可感知，复合语义触发器保证文本自然且激活条件稀疏，覆盖样本保证低误触发率。这一设计使得本文方法在三个攻击场景下平均 ASR-H 达到 97.2%，而 FTR-W 和 FTR-S 分别仅为 4.5% 和 5.7%（Table 2），在攻击有效性与隐蔽性之间取得了现有方法无法达到的平衡。

## 整体框架

本文提出首个面向文本到图像扩散模型的 **clean‑label 后门攻击**，其核心设计理念是：在保持图像‑标题语义一致性的前提下，通过**双模态操纵**实现高隐蔽、高精度的后门植入。整体流水线如 Figure 2 所示，由三个紧密耦合的模块构成：语义保留文本触发器生成、人类不可感知视觉扰动注入，以及覆盖样本生成与数据集构造。

![[assets/figures/papers/paper_list_l2350_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Towards_Human_Imper/figures/002_Figure_2.jpg]]
*Figure 2: The pipeline of our method*

### 2.1 威胁模型与设计约束

攻击者仅能投毒有限数量的训练样本，且必须满足严格的隐蔽性约束（Section 3）。与传统的 dirty‑label 攻击不同——后者直接篡改标题使其与图像内容失配，极易被自动数据清洗工具或人工审查检出——本文方法要求投毒后的图像‑标题对在语义上保持对齐（clean‑label），从而绕过基于语义一致性的过滤机制。

### 2.2 流水线总览

整个攻击流水线包含三个关键阶段：

1. **语义保留文本触发器生成（Section 4.1）**：对原始干净标题进行双层次改造——**词级替换**（将最显著的名词替换为语义高度相似的同义词 W）与**句级重构**（将标题改写为包含现在分词短语作状语的句法结构 S）。二者共同构成复合语义触发器，仅当 W 和 S 同时出现在输入提示中时，后门才会被激活。

2. **人类不可感知视觉扰动注入（Section 4.2）**：在图像的潜在空间中优化一个幅值受限的扰动 δ（$\|\delta\|_\infty \leq \epsilon$，默认 ε=0.10），使得扰动后的源图像潜在向量在 L2 距离上尽可能接近目标图像的潜在向量。由于扰动施加在潜在空间且幅值极小，重建后的图像在视觉上与原始图像几乎无差异，却能在扩散模型的生成过程中引导模型输出目标图像。

3. **覆盖样本生成与数据集构造（Section 4.3）**：为防止模型学习到“仅含 W”或“仅含 S”的伪相关而导致误触发，引入两类覆盖样本——$\mathcal{D}_{cover}^W$（仅含同义词替换，无句法重构）和 $\mathcal{D}_{cover}^S$（仅含句法重构，无同义词替换）。最终投毒数据集按式 (1) 构造：

$$
\mathcal{D}_p = \mathcal{D}_{clean} \cup \mathcal{D}_p \cup \mathcal{D}_{cover}^W \cup \mathcal{D}_{cover}^S
$$

默认混合比例为 1:3:3（投毒样本:W覆盖样本:S覆盖样本），迫使模型必须同时感知到 W 和 S 两个条件才能触发后门行为。

### 2.3 因果开关机制

该流水线的核心因果逻辑可概括为：**同义词 W 提供语义锚点，句法结构 S 提供上下文约束，覆盖样本抑制单条件误触发**。三者协同作用，使得攻击仅在输入提示中精确匹配“W + S”的复合模式时才被激活，而在仅含单一条件或正常提示下保持正常生成行为。消融实验（Table 4, Table 6）证实，移除覆盖样本或退化为单一文本触发器均会导致误触发率（FTR）显著升高，验证了这一复合触发机制的必要性。

> **手动验证提示**：Figure 2 的完整流水线示意图需结合原文查看，以确认各模块间数据流的精确连接方式。

## 核心模块与公式推导

### 双模态操纵总体框架

本方法的核心思路是通过**图像域**和**文本域**的双模态协同操纵，在保持图像-标题语义一致性的前提下植入后门。整体流水线（Figure 2）包含三个关键模块：语义保留文本触发器生成、人类不可感知视觉扰动注入、以及覆盖样本生成与数据集构造。

### 语义保留文本触发器生成

文本触发器的设计目标是在不破坏标题原意的前提下，构建一个复合的、难以被偶然触发的语义开关。该模块由两个子步骤构成：

**1. 最显著名词选择**

给定原始标题 $c$，首先利用词性标注工具提取所有名词，构成名词集合 $\mathcal{N}(c)$。然后，利用 CLIP 模型计算每个名词 $n_i$ 与图像中主要物体 $o_{\mathrm{main}}$ 之间的语义关联度，定义显著性分数为：

$$s(n_i) = \sin\bigl(f_v(o_{\mathrm{main}}), f_t(n_i)\bigr)$$

其中 $f_v(\cdot)$ 和 $f_t(\cdot)$ 分别为 CLIP 的图像编码器和文本编码器，$\sin(\cdot,\cdot)$ 表示余弦相似度。选择显著性分数最高的名词作为待替换词：

$$\hat{n}^* = \operatorname*{argmax}_{n_i \in \mathcal{N}(c)} s(n_i)$$

**2. 同义词替换词选择**

在候选同义词集 $\mathcal{W}$ 中，选择与原名词语义最相似的词作为替换词 $W$：

$$W = \underset{w \in \mathcal{W}}{\mathrm{argmax}} \ \sin\bigl(f_t(\hat{n}^*), f_t(w)\bigr)$$

完成同义词替换后，进一步对标题进行句法重构，将原始标题改写为包含**现在分词短语作状语**的结构 $S$。最终，只有同时满足“包含同义词 $W$”和“采用特定句法结构 $S$”两个条件的提示才会激活后门，从而构成复合语义触发器。

### 人类不可感知视觉扰动注入

图像域的操纵目标是在源图像中注入极小的扰动，使其在潜在空间中接近目标图像，同时保持视觉外观不变。具体而言，给定源图像潜在向量 $z_s$ 和目标图像潜在向量 $z_t$，求解如下优化问题：

$$\operatorname*{min}_{\delta} \|z_s + \delta - z_t\|_2^2 \quad \mathrm{subject\ to} \quad \|\delta\|_\infty \leq \epsilon$$

其中 $\delta$ 为待优化的扰动，$\epsilon$ 控制扰动强度的上界（默认 $\epsilon=0.10$）。该优化在潜在空间中完成，确保扰动在像素空间中几乎不可察觉。

### 覆盖样本生成与数据集构造

为防止模型仅学习到单一条件（仅 $W$ 或仅 $S$）与目标图像之间的虚假关联，方法引入了两类覆盖样本：$\mathcal{D}_{\mathrm{cover}}^W$（仅含同义词替换但无句法结构）和 $\mathcal{D}_{\mathrm{cover}}^S$（仅含句法结构但无同义词替换）。这些覆盖样本保持干净标签，使模型必须同时感知两个条件才会触发后门。

最终投毒数据集 $\mathcal{D}_p$ 由四部分混合构成：

$$\mathcal{D}_p = \mathcal{D}_{\mathrm{clean}} \cup \mathcal{D}_p \cup \mathcal{D}_{\mathrm{cover}}^W \cup \mathcal{D}_{\mathrm{cover}}^S$$

默认混合比例为 $1:3:3$（投毒样本 : 覆盖样本$^W$ : 覆盖样本$^S$），这一比例在消融实验（Table 6）中被验证为平衡攻击成功率与误触发率的最优配置。

### 补充图表

![[assets/figures/papers/paper_list_l2350_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Towards_Human_Imper/figures/001_Figure_1.jpg]]
*Figure 1: An examples of poisoned image-caption pair by dirty-label backdoor attack (left) and poisoned image-caption pair by our proposed clean-label attacks (right)*

## 实验与分析

### 主实验结果

本文在三种攻击场景（Woman→Nude Woman、Cat→Dog、Flower→Tree）上对 clean-label 后门攻击的有效性与隐蔽性进行了全面评估。如 Table 2 所示，所提方法在人类评估下（ASR-H）的平均攻击成功率达到 **97.2%**，其中 Woman→Nude Woman 场景高达 **99.8%**，表明攻击能够在复合触发器激活时稳定生成目标图像。

![[assets/figures/papers/paper_list_l2350_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Towards_Human_Imper/figures/005_Table_2.jpg]]
*Table 2: Effectiveness and stealthiness of our method across different target tasks*

![[assets/figures/papers/paper_list_l2350_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Towards_Human_Imper/figures/009_Table_5.jpg]]
*Table 5: Performance with varying poison sample ratios on the woman→nude woman scenario, the best-performing case in Table 2. * is denoted as the default setting*

隐蔽性方面，两类误触发率均保持在低位：仅含同义词 W 而不含句法结构 S 的提示（FTR-W）平均误触发率为 **4.5%**，仅含 S 而不含 W 的提示（FTR-S）平均误触发率为 **5.7%**。这意味着在绝大多数非目标提示下，模型行为不受影响，后门不会被意外激活。

与 dirty-label 基线的对比（Table 3）进一步凸显了 clean-label 策略的优势。在 Woman→Nude Woman 场景下：

![[assets/figures/papers/paper_list_l2350_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Towards_Human_Imper/figures/006_Table_3.jpg]]
*Table 3: Comparison between clean-label backdoor attack and dirty-label attack*

- **FTR-W**：本文方法仅 **1.9%**，而 dirty-label 方法高达 **19.5%**，降幅达 17.6 个百分点。
- **不安全内容检出率（UCR）**：本文方法为 **0%**，即所有投毒样本均能通过 NSFW 内容过滤器；dirty-label 方法则为 **100%**，所有投毒样本均被检出。

这一对比揭示了核心瓶颈：dirty-label 攻击中图像与标题的语义错配使其极易被自动数据清洗工具识别，而本文通过双模态操纵保持了视觉-文本语义一致性，从而实现了对内容过滤器的完全规避。

### 消融实验

#### 复合触发器 vs. 单一触发器

Table 4 展示了在不同对数似然（log-likelihood）区间下，复合触发器与单一触发器的 ASR 对比。在低对数似然提示（即罕见或非典型提示）下，仅使用同义词替换（W-only）或仅使用句法重构（S-only）的方法 ASR 显著下降，而本文的复合触发器（W+S）保持了较高的攻击成功率。这验证了**双模态触发器设计的必要性**：单一触发条件容易被模型泛化能力稀释，而复合条件通过联合约束形成了更精确的因果开关。

![[assets/figures/papers/paper_list_l2350_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Towards_Human_Imper/figures/007_Table_4.jpg]]
*Table 4: ASR of our method and single trigger methods under different log-likelihood values*

#### 投毒样本数量

Table 5 展示了投毒样本数量对 ASR 的影响。当投毒样本从 10 个增加至 70 个时，ASR-H 从约 85% 提升至 **99.9%**，但进一步增加至 90 个时收益递减。这表明在默认实验设置下，**70 个投毒样本**已足以实现近乎完美的后门注入，过度投毒并无必要。

#### 覆盖样本比例

Table 6 展示了覆盖样本 $\mathcal{D}_{\text{cover}}^W$ 和 $\mathcal{D}_{\text{cover}}^S$ 比例对误触发率的影响。在默认比例 **1:3:3**（投毒样本:W覆盖样本:S覆盖样本）下，FTR-W 仅为 1.9%，FTR-S 为 4.7%。当完全移除覆盖样本时，FTR 大幅上升；当比例失衡（如 1:1:1 或 1:5:5）时，误触发率同样恶化。这验证了覆盖样本在**防止模型学习虚假相关性**方面的关键作用——通过让模型在训练中接触仅满足单一条件的样本，模型学会了区分“同时满足 W 和 S”与“仅满足其一”的提示，从而显著降低了误触发。

![[assets/figures/papers/paper_list_l2350_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Towards_Human_Imper/figures/010_Table_6.jpg]]
*Table 6: Performance on Cover Samples with varying proportions. Here, we also select the attack scenario of woman→nude woman. * is denoted as the default setting*

### 防御鲁棒性评估

Table 7 展示了在推理阶段对输入图像施加不同程度高斯噪声扰动（$\delta$）时的攻击性能。随着噪声强度增加，ASR-H 和 ASR-N 均呈下降趋势，表明**简单的预处理防御可在一定程度上抑制后门**。然而，这一防御的代价是生成图像质量的严重退化——强高斯噪声虽然降低了攻击成功率，但也破坏了正常图像的生成质量，使其难以在实际应用中部署。这一发现揭示了当前防御的困境：有效抑制后门与保持生成质量之间存在难以调和的权衡。

![[assets/figures/papers/paper_list_l2350_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Towards_Human_Imper/figures/008_Table_7.jpg]]
*Table 7: Performances under different perturbations δ. The attack scenario is woman→nude woman*

### 失败模式与局限性

1. **模型泛化性未验证**：所有实验仅在 Stable Diffusion v1.5 上进行，攻击在更大规模模型（如 SDXL、Imagen、DALL·E 3）上的有效性未知，需要进一步验证。
2. **触发器依赖主语名词**：复合触发器要求提示中包含可被替换的主语名词。若输入提示不含合适的名词（如纯抽象描述），攻击可能无法激活。
3. **NSFW 检测器与人工评估的不一致**：在某些噪声防御条件下，基于 NSFW 检测器的 ASR-N 可能过高估计攻击成功率，与人工评估 ASR-H 存在偏差，需注意指标选择的合理性。

### 补充图表

![[assets/figures/papers/paper_list_l2350_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Towards_Human_Imper/figures/003_Figure_3.jpg]]
*Figure 3: Visual results of the attacking*

![[assets/figures/papers/paper_list_l2350_https_openaccess_thecvf_com_content_CVPR2026_html_Wu_Towards_Human_Imper/figures/004_Table_1.jpg]]
*Table 1: Visualization of three attack scenarios*

## 方法谱系与知识库定位

### 问题定位：从 Dirty-Label 到 Clean-Label 后门攻击

文本到图像扩散模型的后门攻击研究可划分为两条主线：**dirty-label 攻击**与**clean-label 攻击**。本文属于后者，且是首个针对文本到图像生成模型提出 clean-label 后门攻击的工作。

**Dirty-label 攻击**的典型代表包括 **BadT2I**（Zhai et al., ACM Multimedia 2023）和 **BAGM**（Vice et al., IEEE TIFS 2024）。这类方法的核心策略是在训练数据中注入语义错配的图像-文本对——例如，将目标图像的标题错误地标注给源图像，使模型在特定触发条件下将源图像映射到目标概念。其致命弱点在于：被投毒的图像-文本对存在显著的语义不一致，容易被自动数据清洗工具（如 NSFW 内容过滤器）或人工检测发现。本文实验表明，dirty-label 攻击的 UCR（不安全内容检测率）高达 100%，即所有投毒样本均可被 NSFW 检测器识别，严重削弱了攻击的实用性。

**个性化后门注入**是另一条技术路线，如基于文本反转或 DreamBooth 的后门攻击（Huang et al., AAAI 2024）。这类方法通过少量样本进行个性化微调以注入后门，但其攻击场景受限，通常需要访问特定的个性化训练流程，且触发机制较为显式。

本文提出的 **clean-label 后门攻击** 从根本上改变了投毒范式：图像与标题在语义上保持对齐，使投毒样本在视觉和文本层面均呈现“干净”的外观，从而绕过自动数据清洗。这一转变的关键在于**双模态操纵策略**——图像域引入潜在空间优化的人类不可感知噪声，文本域构建基于同义词替换与句法重构的复合语义触发器，并引入覆盖样本防止意外激活。

### 核心技术差异：方法槽位对比

| 方法槽位 | Dirty-Label 基线（BadT2I / BAGM） | 本文 Clean-Label 方法 |
|----------|-----------------------------------|----------------------|
| **投毒方式** | dirty-label：图像与标题语义不对齐 | clean-label：图像与标题语义保持对齐 |
| **图像触发器** | 无或显式修改 | 潜在空间优化的人类不可感知噪声（ϵ=0.10） |
| **文本触发器** | 显式关键词（如触发词） | 复合语义触发器：同义词替换 + 特定句法结构（现在分词短语作状语） |
| **覆盖样本** | 无 | 两类覆盖样本（仅含 W 或仅含 S）以防止意外激活 |

**图像域扰动**通过求解一个约束优化问题实现：在潜在空间中最小化受扰动源图像与目标图像之间的 L2 距离，同时将扰动限制在 ϵ 范数球内（式见 Algorithm 1）。这种设计确保投毒图像在像素空间保持视觉不变，但在扩散模型的编码空间中携带指向目标图像的信号。

**文本域触发器**采用复合设计：首先利用 CLIP 编码器计算图像主要物体与标题中名词之间的显著性分数 $s(n_i) = \sin(f_v(o_{\mathrm{main}}), f_t(n_i))$，选择最显著的名词 $\hat{n}^*$ 进行同义词替换；同时将标题改写为现在分词短语作状语的句法结构。该设计的因果逻辑在于：模型只有在输入提示中**同时**出现特定同义词（W）和特定句法结构（S）时才会触发后门，单一条件无法激活。

**覆盖样本**是本文方法区别于所有基线工作的独特设计。通过在训练数据中混入仅含 W 或仅含 S 的干净样本，迫使模型学习“单一条件不触发”的约束，从而将误触发率（FTR）控制在极低水平。消融实验（Table 6）表明，移除覆盖样本或比例不当会导致 FTR 大幅上升，验证了该设计的必要性。

### 适用边界与泛化性局限

本文方法的适用边界受以下因素制约：

1. **模型架构限制**：所有实验仅在 **Stable Diffusion v1.5** 上进行验证。该方法对更大规模或架构差异显著的模型（如 SDXL、Imagen、DALL·E 3、Midjourney）的有效性尚未被评估。扩散模型在潜在空间结构、文本编码器选择和训练数据分布上的差异可能影响后门植入的成功率和隐蔽性。

2. **触发条件依赖**：复合触发器要求输入提示中同时包含特定同义词和特定句法结构。若提示不含合适的主语名词（如抽象描述、无人物场景），攻击可能无法激活。此外，同义词替换依赖于预定义的候选词集，其覆盖范围受限于语言资源。

3. **防御脆弱性**：简单的预处理防御（如强高斯噪声扰动）可显著抑制后门激活，但代价是严重损害生成图像质量（Table 7）。这一权衡表明，当前缺乏能在不牺牲生成质量的前提下有效检测并中和此类 clean-label 后门的防御方法。

4. **伦理边界**：攻击涉及不安全图像生成（如裸体图像），虽然所有实验离线进行且强调防御目的，但该方法的技术原理可被滥用于生成有害内容，这对其研究伦理提出了更高要求。

### 开放问题

1. **防御机制设计**：能否开发在不损害生成质量的前提下有效检测并中和 clean-label 后门的鲁棒防御方法？当前高斯噪声防御的“质量-安全”权衡表明，需要更精细的防御策略，如基于激活分析的检测或对抗性训练。

2. **跨模态扩展**：复合触发器机制能否扩展到更多模态？例如，在视频生成模型中，时间维度的扰动和字幕结构可能提供更丰富的触发空间；在语音合成中，音素级替换和韵律结构可类比于同义词和句法触发。

3. **大规模商业模型验证**：如何评估该攻击在 DALL·E 3、Midjourney 等黑盒商业模型上的可行性与隐蔽性？这些模型通常采用多阶段流水线和专有数据过滤机制，可能天然具备一定的抗攻击能力。

4. **覆盖样本的自动化生成**：攻击者能否利用更先进的生成模型自动构造更自然、更多样的覆盖样本，以进一步增强隐蔽性并降低人工构造成本？

5. **NSFW 检测器的不一致性**：实验观察到 NSFW 自动检测器（ASR-N）与人工评估（ASR-H）在某些防御条件下存在显著不一致。这一现象的根源是检测器本身的局限性还是攻击的对抗特性，值得进一步探究。

## 原文 PDF

![[paperPDFs/CVPR_2026/Towards_Human_Imperceptible_Backdoor_Attacks_on_Text_to_Image_Diffusion_Models.pdf]]