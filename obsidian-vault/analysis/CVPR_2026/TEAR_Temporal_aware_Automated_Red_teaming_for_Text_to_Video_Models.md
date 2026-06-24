---
title: "TEAR: Temporal-aware Automated Red-teaming for Text-to-Video Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TEAR_Temporal_aware_Automated_Red_teaming_for_Text_to_Video_Models.pdf
aliases:
- TEAR
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
- topic/generative_models_diffusion/diffusion_image_video
- topic/generative_models_diffusion
core_operator: 将有害语义分解为文本安全但时序相连的片段，并通过时间感知的奖励函数对生成器进行在线优化，可系统性地挖掘T2V模型在时间维度的安全漏洞。
primary_logic: 将T2V红队测试形式化为对提示空间和时间连续性的联合优化问题，采用基于PPO的在线学习同时约束文本安全性与视频-文本时序一致性，使得生成提示在文本无害的前提下通过事件顺序组合诱导有害视频输出。
claims:
- TEAR在开源模型Hunyuan-Video上达到82.3% ASR，远超最佳基线FLIRT的57.2%
- TEAR在商业T2V服务上取得接近98%的文本过滤通过率，同时保持高ASR（多数类别>85%）
- 迭代细化轮次增加可显著提升ASR和NSFW Filter Pass Rate，证明Refine Model的有效性
- TEAR生成的对抗提示具有高跨模型迁移性，平均迁移ASR达76.4%，峰值82.6%
---

# TEAR: Temporal-aware Automated Red-teaming for Text-to-Video Models

> [!tip] 核心洞察
> 将T2V红队测试形式化为对提示空间和时间连续性的联合优化问题，采用基于PPO的在线学习同时约束文本安全性与视频-文本时序一致性，使得生成提示在文本无害的前提下通过事件顺序组合诱导有害视频输出。

| 字段 | 内容 |
|------|------|
| 中文题名 | TEAR: 面向文本到视频模型的时间感知自动红队测试框架 |
| 英文题名 | TEAR: Temporal-aware Automated Red-teaming for Text-to-Video Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/He_TEAR_Temporal-aware_Automated_Red-teaming_for_Text-to-Video_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation #topic/generative_models_diffusion/diffusion_image_video #topic/generative_models_diffusion |
| Method | TEAR |
| Dataset | Hunyuan-Video, Wan 2.2, Commercial T2V Services |

> [!tip] 效果简介
> - Hunyuan-Video 上，ASR 82.3% vs 57.2% (FLIRT) (+25.1%)。
> - Wan 2.2 上，ASR 80.5% vs 56.4% (FLIRT) (+24.1%)。
> - Commercial T2V Services (Veo-3.1, Hailuo-2.3, Ray 2) 上，ASR ≈85%+ (most categories) vs N/A (N/A)。

## 概述

**问题瓶颈。** 现有文本到视频（T2V）安全评估方法几乎完全聚焦于静态帧内容，忽视了视频中事件**时序组合**产生的安全风险。攻击者可将有害语义拆解为文本层面安全但时序相连的片段，利用时间动态诱导有害视频输出，而传统基于文本安全分类器或单帧审查的防御手段对此无效。

**核心洞察。** TEAR将T2V红队测试形式化为对**提示空间与时间连续性**的联合优化问题——在保证文本无害的约束下，通过事件顺序组合诱导有害视频输出。这一形式化将安全评估从“文本-帧”静态匹配推进到“文本-时序”动态博弈。

**方法定位。** TEAR是一种时间感知的自动红队测试框架，采用两阶段优化：先基于规则式时间重写数据集进行初始生成器训练，再通过**基于PPO的在线偏好学习**联合优化文本安全性与视频-文本时序一致性。与仅扰动文本空间的基线方法（如FLIRT, Mehrabi et al., EMNLP 2024；ART, Li et al., NeurIPS 2024）不同，TEAR额外引入时间模式对齐奖励与视频全局/内部一致性奖励，并通过MLLM驱动的多轮迭代精化持续增强攻击效果。

**主要结果。** 在开源模型Hunyuan-Video上，TEAR达到**82.3%攻击成功率（ASR）**，远超最佳基线FLIRT的57.2%（Table 1）；在Wan 2.2上同样取得80.5% ASR。在商业T2V服务（Veo-3.1, Hailuo-2.3, Ray 2）上，TEAR在保持接近98%文本过滤通过率的同时，多数有害类别ASR超过85%（Figure 3）。此外，TEAR生成的对抗提示具有强跨模型迁移性，平均迁移ASR达76.4%（Table 3）。消融实验证实，迭代精化轮次增加可同步提升ASR与文本过滤通过率（Figure 4），且生成提示在不同有害类别下保持高多样性，未出现模式坍塌（Figure 5）。

## 背景与动机

文本到视频（T2V）生成模型近年来取得了显著进展，能够根据自然语言描述合成高质量、时序连贯的视频内容。然而，随着这些模型向公众开放，其潜在的安全风险也日益凸显。现有的T2V安全评估方法主要沿袭了文本到图像（T2I）领域的静态帧分析范式，即通过检测生成视频中单帧或孤立帧的视觉内容来判断视频是否包含有害信息。这种评估策略存在一个根本性盲区：**它忽略了视频作为时序媒体的本质属性——事件在时间轴上的动态组合与演变**。

具体而言，攻击者可以将一个在文本层面看似无害的语义分解为多个时序相连的片段，这些片段在孤立状态下均不触发安全过滤器，但当它们按特定顺序组合成视频时，却能够诱导出明显的有害内容。例如，一个不包含任何暴力词汇的提示，通过描述“一个人拿起工具→走向目标→做出特定动作”的事件序列，最终生成的视频可能呈现暴力场景。这种**时间聚合攻击（temporal-aggregation attack）** 完全绕过了现有的文本安全过滤器和基于静态帧的视频安全分类器，暴露了当前T2V安全评估体系的系统性缺陷。

现有自动红队测试方法同样未能应对这一挑战。**FLIRT**（Mehrabi et al., EMNLP 2024）和**ART**（Li et al., NeurIPS 2024）等面向T2I的红队方法仅对文本提示空间进行扰动优化，缺乏对视频时间维度的建模。**GPTFuzzer**（Yu et al., arXiv 2023）和**DiverCT**（Zhao et al., AAAI 2025）等面向大语言模型的方法则完全不具备视频生成场景的适用性。这些方法的共同局限在于：**优化空间仅局限于文本语义的安全性评估，奖励函数仅依赖文本安全分类器，无法感知生成视频在时间维度上的有害性**。

上述缺口直接引出了本文的核心研究问题：如何系统性地发现那些在文本层面通过安全检查，却能通过时序事件组合诱导有害视频输出的对抗提示？这要求将T2V红队测试重新形式化为一个**对提示空间和时间连续性的联合优化问题**——在约束文本安全性的前提下，通过优化提示中事件的时间结构与顺序，最大化生成视频的有害性。TEAR框架即为解决这一问题而提出，其核心洞察在于：将有害语义分解为文本安全但时序相连的片段，并通过时间感知的奖励函数对生成器进行在线优化，可系统性地挖掘T2V模型在时间维度的安全漏洞。

## 核心创新

TEAR的核心创新在于将T2V红队测试从静态帧安全评估拓展至**时间维度**，首次系统性地揭示了“文本安全、时序有害”这一新型攻击面。其关键突破可归纳为以下四个维度：

### 1. 优化空间升维：从文本空间到文本-时间联合空间

现有方法（如 **FLIRT**，Mehrabi et al., EMNLP 2024；**ART**，Li et al., NeurIPS 2024）的优化目标仅局限于提示文本空间——通过扰动或反馈循环使文本绕过安全分类器，同时诱导有害图像输出。TEAR将优化空间扩展为**文本空间与时间一致性空间的联合优化**，引入视频-文本全局一致性及视频内部时序一致性作为额外约束（Section 3.3.2, Eq.5）。这一升维使得攻击不再依赖单帧有害内容，而是通过事件序列的组合逻辑触发有害语义，从根本上改变了红队测试的搜索范式。

### 2. 提示生成策略重构：基于规则的时间解构-合成 + 在线偏好学习

传统方法依赖静态语义扰动或单步反馈循环生成对抗提示。TEAR提出了一套三阶段生成策略：
- **基于规则的数据集构建**（Section 3.3.1）：通过时间解构（Temporal Deconstruction）、顺序强制（Sequential Enforcement）、时间-空间合成（Temporal-Space Synthesis）三条重写规则，将有害语义分解为文本安全但时序相连的片段，并经过安全双过滤确保训练数据质量。
- **PPO在线偏好学习**（Section 3.3.2）：将生成器优化形式化为在线强化学习问题，最大化复合奖励函数的同时以KL散度惩罚防止过优化（Eq.6）。
- **MLLM驱动的多轮迭代精化**（Section 3.4）：基于Qwen-3-VL的Refine Model接收判断反馈，迭代修改提示以增强攻击效果与隐蔽性。

### 3. 奖励函数复合化：安全-模式-一致性三重约束

基线方法的奖励函数通常仅依赖文本安全分类器（如仇恨言论检测）。TEAR设计了**复合奖励函数**，包含三个层次：
- **文本安全奖励**（Eq.3）：$1 - \mathbf{g}_t(p_t)$，确保提示通过文本安全过滤；
- **时间模式对齐奖励**（Eq.4）：$\mathbf{g}_r(p_t)$，通过提示嵌入与参考时间风格原型之间的余弦相似度，约束生成提示保持时序诱导能力；
- **时间一致性奖励**（Eq.5）：$\mathbf{R}_{con}(p_s, p_t)$，基于视频-文本全局一致性和视频内部时序一致性的综合评分，确保生成视频在时间维度上实现有害语义的连贯表达。

这一三重约束使得TEAR能够在**文本无害的前提下**，通过事件顺序组合系统性地诱导有害视频输出——这正是TEAR的核心洞察。

### 4. 数据构建方式革新：三层时间感知规则式改写

区别于人工收集或简单LLM改写，TEAR的数据构建采用了**三层时间感知规则式改写**，并经过安全双过滤。这一构造方式确保了训练数据天然具备“文本安全-时序有害”的特性，为后续在线优化提供了高质量的初始策略空间，是TEAR能够收敛到高效攻击策略的关键基础。

### 效果验证

上述创新带来了显著的性能提升：在Hunyuan-Video上，TEAR达到**82.3% ASR**，远超最佳基线FLIRT的57.2%（+25.1个百分点，Table 1）；在商业T2V服务上，TEAR在保持接近98%文本过滤通过率的同时，多数有害类别的ASR超过85%（Figure 3）。消融实验进一步证实，迭代细化轮数的增加可同时提升ASR和NSFW Filter Pass Rate（Figure 4），验证了Refine Model在攻击效果与隐蔽性平衡中的关键作用。

## 整体框架

TEAR 框架将文本到视频（T2V）模型的红队测试形式化为对提示空间与时间连续性的联合优化问题，其核心目标是发现一类特殊对抗提示：文本本身被安全分类器判定无害，但通过事件时序组合诱导 T2V 模型生成有害视频内容。如图 Figure 2 所示，TEAR 由三个核心组件构成：**时间感知测试生成器（Temporal-aware Test Generator）**、**精化模型（Refine Model）** 以及**目标 T2V 模型**，整体运行分为两个阶段。

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_He_TEAR_Temporal_aware/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the TEAR framework. Our approach has two phases. (a) Test-case Generator Optimization: A generator is trained in three stages (Dataset Construction, Initial Training, Temporal-aware Optimization) using rule-based construction and temporalaware rewards*

### 阶段一：测试用例生成器优化

该阶段旨在训练一个能够生成“文本安全—视频有害”对抗提示的专用生成器，分为三个子步骤：

1. **数据集构建**：基于三层时间感知规则（时间解构、顺序强制、时间-空间合成）对种子提示进行改写，生成包含安全提示-目标提示-时间指令三元组的数据集 $\mathbf{D}_p$，并经过文本安全与视频有害双过滤，确保训练数据的质量与攻击导向。
2. **初始训练**：以 Llama-3 为基础模型，采用 LoRA 微调，在构建的数据集上最小化自回归负对数似然损失 $\mathcal{L}_{\mathrm{Ini}} = -\mathbb{E}_{(p_s, p_t, T) \sim \mathbf{D}_p} \log p(p_t | p_s, I)$，使生成器初步掌握从安全种子生成时序攻击提示的能力。
3. **时间感知在线偏好学习**：以初始训练后的生成器 $G_{initial}$ 为起点，引入复合奖励函数进行 PPO 在线优化。奖励由两部分构成：**提示空间奖励** $\mathbf{R}_{pmt}$ 结合文本安全性（仇恨言论置信度的反向指标）与时间模式对齐度（提示嵌入与参考原型的余弦相似度）；**时间一致性奖励** $\mathbf{R}_{con}$ 基于视频-文本全局一致性与视频内部时序一致性综合评分。最终优化目标为 $\zeta = \mathbb{E}[\mathbf{R}_{pmt} + \mathbf{R}_{con} - \lambda \log \frac{G_\delta}{G_{initial}}]$，其中 KL 散度惩罚项防止生成器过度偏离初始分布。

### 阶段二：红队测试用例生成

优化后的生成器 $G_{final}$ 进入推理-精化循环：

1. **生成**：$G_{final}$ 以安全种子提示 $p_s$ 为输入，生成候选对抗提示 $p_t$。
2. **判定**：提示判定系统 $\Phi_P$ 对 $p_t$ 进行文本安全评估；目标 T2V 模型 $\mathcal{M}$ 根据 $p_t$ 生成视频，视频判定系统 $\Phi_V$ 评估视频有害性。
3. **精化**：若未满足红队目标（即 $\Phi_P(p_t)=0$ 且 $\Phi_V(\mathcal{M}(p_t))=1$），精化模型 $\mathcal{R}_m$（基于 Qwen-3-VL，采用少样本上下文学习）接收问题提示、生成视频及双判定反馈，迭代修改提示以增强攻击效果与隐蔽性，直至达成目标或达到最大迭代轮次。

### 输入输出流

- **输入**：安全种子提示 $p_s$（来自预定义有害类别或自由生成）、时间指令 $T$。
- **中间产物**：对抗提示 $p_t$、生成视频 $\mathcal{M}(p_t)$、文本/视频判定结果。
- **输出**：满足 $\Phi_P(p)=0 \land \Phi_V(\mathcal{M}(p))=1$ 的对抗提示集 $\mathcal{P}_v^*$，即文本安全但视频有害的红队测试用例。

该两阶段设计的关键在于将时序风险挖掘从静态文本扰动提升为对提示空间与视频时间一致性的联合在线学习，使得生成器能够在保持文本无害性的前提下，通过事件顺序组合系统性地暴露 T2V 模型在时间维度的安全漏洞。

## 核心模块与公式推导

### 3.1 问题形式化

TEAR将T2V红队测试形式化为一个约束优化问题。给定目标T2V模型 $\mathcal{M}$、文本安全判断器 $\Phi_P$ 和视频有害性判断器 $\Phi_V$，自动红队系统 $\mathcal{R}$ 的目标是发现一组对抗提示 $\mathcal{P}_v^*$，使得每个提示 $p$ 在文本层面被判定为安全，但其生成的视频被判定为有害：

$$\mathcal{P}_v^* = \mathcal{R}(\mathcal{P}_v^u, T, \mathcal{M}, \Phi_P, \Phi_V) \quad \mathrm{s.t.} \ p \in \mathcal{P}_v^* \mid \Phi_P(p) = 0 \land \Phi_V(\mathcal{M}(p)) = 1$$

其中 $\mathcal{P}_v^u$ 为初始有害种子提示集，$T$ 为目标有害类别。这一形式化的核心挑战在于：提示必须在文本空间保持“无害”（$\Phi_P(p)=0$），同时通过视频帧之间的时序组合诱导有害内容（$\Phi_V(\mathcal{M}(p))=1$）。

### 3.2 框架总览

TEAR框架由三个核心组件构成（Figure 2）：

1. **时间感知测试生成器（Temporal-aware Test Generator）**：基于Llama-3构建，经LoRA微调，负责生成文本安全但可诱导有害时序视频的对抗提示。该生成器通过两阶段优化：初始训练和时序感知在线偏好学习。

2. **精化模型（Refine Model）**：基于Qwen-3-VL的多模态大语言模型，接收判断反馈（文本安全性、视频有害性）并迭代修改提示，以增强攻击效果与隐蔽性。

3. **判断系统**：包含提示判断器 $\Phi_P$（评估文本安全性）和视频判断器 $\Phi_V$（评估视频有害性），为生成器和精化模型提供反馈信号。

### 3.3 时间感知测试生成器优化

#### 3.3.1 规则驱动的初始训练

初始生成器 $G_{initial}$ 在精心构建的数据集 $\mathbf{D}_p$ 上进行微调。该数据集通过三层时间感知规则式改写构建：

- **时间解构（Temporal Deconstruction）**：将单一有害动作分解为多个文本安全但时序相连的子动作。
- **顺序强制（Sequential Enforcement）**：强制子动作按特定时序排列，使得单独帧无害而连续播放产生有害语义。
- **时间-空间合成（Temporal-Space Synthesis）**：将时间模式与空间场景组合，增强隐蔽性。

生成器以自回归方式学习从安全种子提示 $p_s$ 生成时序对抗提示 $p_t$，优化目标为标准负对数似然损失：

$$\mathcal{L}_{\mathrm{Ini}} = -\mathbb{E}_{(p_s, p_t, T) \sim \mathbf{D}_p} \log p(p_t | p_s, I)$$

其中 $I$ 为类别指令。

#### 3.3.2 时序感知在线偏好学习

初始训练后，生成器 $G_{final}$ 通过PPO在线偏好学习进一步优化。核心创新在于复合奖励函数的设计，同时约束提示空间的安全性与视频-文本时序一致性。

**提示级奖励** $\mathbf{R}_{pmt}$ 包含两个分量：

$$\mathbf{R}_{pmt}(p_t) = \mathbb{E}_{p_t \sim G_\delta(p_s)} \left[ \boldsymbol{\alpha}_1 \cdot (1 - \mathbf{g}_t(p_t)) + \boldsymbol{\alpha}_2 \cdot \frac{(\mathbf{g}_r(p_t) + 1)}{2} \right]$$

- **安全性分量**：$\mathbf{g}_t(p_t)$ 为仇恨言论分类器输出的置信度，$1 - \mathbf{g}_t(p_t)$ 鼓励生成文本安全的提示。
- **模式对齐分量**：$\mathbf{g}_r(p_t)$ 度量提示嵌入与参考时间风格原型之间的余弦相似度：

$$\mathbf{g}_r(p_t) = \frac{\mathcal{T}_p(p_t) \cdot \frac{1}{|\mathcal{P}_{ref}|} \sum_{p' \in \mathcal{P}_{ref}} \mathcal{T}_p(p')}{\|\mathcal{T}_p(p_t)\| \cdot \left\| \frac{1}{|\mathcal{P}_{ref}|} \sum_{p' \in \mathcal{P}_{ref}} \mathcal{T}_p(p') \right\|}$$

其中 $\mathcal{T}_p$ 为提示编码器，$\mathcal{P}_{ref}$ 为参考时间风格样本集。该分量确保生成的提示在时序表达模式上与目标风格保持一致。

**时序一致性奖励** $\mathbf{R}_{con}$ 引入视频空间的约束：

$$\mathbf{R}_{con}(p_s, p_t) = \mathbb{E}_{v_p' \sim \mathcal{M}(p_t)} \min\left(\beta, \frac{\mathbf{g}_{gc}(p_s, \mathcal{E}_v(\mathcal{F}_{v_p'})) - \gamma_1}{\theta_1} \right)$$

该奖励基于视频-文本全局一致性评分 $\mathbf{g}_{gc}$，衡量生成视频与原始安全提示 $p_s$ 在语义上的偏离程度。通过截断参数 $\beta$ 防止奖励爆炸，$\gamma_1$ 和 $\theta_1$ 控制评分尺度。

**PPO训练目标** 最大化复合奖励，同时用KL散度惩罚防止策略过优化：

$$\zeta = \mathbb{E}_{p_s \sim \mathbf{D}_m, p_t \sim G_\delta(x)} \left[ \mathbf{R}_{pmt}(p_t) + \mathbf{R}_{con}(p_s, p_t) - \lambda \log \frac{G_\delta(p_t | p_s)}{G_{initial}(p_t | p_s)} \right]$$

其中 $\lambda$ 控制KL惩罚强度，$G_{initial}$ 为初始生成器策略，$G_\delta$ 为当前优化策略。这一设计使得生成器在最大化攻击效果的同时，不会偏离初始安全生成能力过远。

### 3.4 多模态迭代精化

精化模型 $\mathcal{R}_m$ 接收当前对抗提示 $p_t$、生成的视频 $\mathcal{M}(p_t)$ 以及来自 $\Phi_P$ 和 $\Phi_V$ 的反馈，通过少样本上下文学习产生更新后的提示 $p_{t+1}$。该迭代过程持续进行，直到满足红队测试目标（文本安全且视频有害），从而在保持文本隐蔽性的前提下逐步增强攻击效果。消融实验（Figure 4）证实，迭代精化轮次的增加可同时提升ASR和NSFW Filter Pass Rate，验证了该模块的必要性。

## 实验与分析

### 主实验结果

TEAR在开源和商业文本到视频（T2V）模型上均展现出显著的攻击有效性，系统性验证了时间感知红队测试的核心价值。

**开源模型表现。** 在Hunyuan-Video和Wan 2.2两个主流开源T2V模型上，TEAR的攻击成功率（ASR）分别达到**82.3%**和**80.5%**，远超所有基线方法。如表1所示，表现最强的基线**FLIRT**（Mehrabi et al., EMNLP 2024）在Hunyuan-Video上仅取得57.2%的ASR，TEAR将这一指标提升了**25.1个百分点**。针对文本到图像红队设计的**ART**（Li et al., NeurIPS 2024）表现更弱，在两个模型上的ASR分别为52.6%和49.7%。这一差距的根本原因在于，FLIRT和ART均仅操作文本空间，无法感知视频内容的时间维度——它们生成的对抗提示虽然可能绕过文本安全过滤器，但缺乏对事件时序组合的利用能力。TEAR通过将有害语义分解为文本安全但时序相连的片段，并利用时间感知奖励函数进行在线优化，成功挖掘了T2V模型在时间维度的安全漏洞。

**商业T2V服务表现。** TEAR在Veo-3.1、Hailuo-2.3和Luma Ray-2三个商业T2V服务上的攻击效果同样显著。如图3所示，TEAR生成的对抗提示在这些服务上取得了**接近98%的API级和NSFW过滤器通过率**，意味着提示本身几乎不被文本安全机制拦截。然而，这些“文本无害”的提示在多数有害类别上仍保持了**85%以上**的ASR，证明商业T2V服务同样缺乏对时序组合攻击的防御能力。值得注意的是，色情（Pornography）类别在商业服务上的ASR相对较低（低于80%），这可能与商业模型针对该类内容部署了更严格的帧级安全检测有关，具体原因需要进一步验证。

**无种子提示生成。** 在无种子提示的设置下（即不依赖预定义的有害种子提示），TEAR仍能生成大量有效的对抗测试用例。如表2所示，TEAR在Hunyuan-Video上的ASR达到**76.8%**，在Wan 2.2上达到**74.3%**，同时保持较高的提示通过率。这一结果验证了TEAR的时间感知优化策略并非简单地改写已知有害提示，而是具备从零开始构造时间维度攻击的能力。

### 消融实验与分析

**迭代精化轮次的影响。** 如图4所示，迭代精化轮次对攻击效果具有显著的正向影响。随着精化轮次从0增加到5，ASR和NSFW过滤器通过率同步提升。这一现象揭示了Refine Model的核心作用：基于Qwen-3-VL的多模态精化模型能够接收判断系统的反馈（包括文本安全性和视频有害性评估），针对性地修改提示以增强攻击效果，同时维持文本层面的隐蔽性。精化轮次超过5后增益趋于饱和，表明提示优化存在边际效用递减。

**生成参数敏感性。** 图6展示了T2V模型生成参数对攻击有效性的影响。推理步数（Step）、引导尺度（Scale）和帧数（Number of Frames）三个参数均对ASR和提示安全率存在明显影响：过低的推理步数可能导致视频质量下降从而降低有害内容识别率，过高的引导尺度可能抑制模型对时序指令的遵循能力。这表明在实际红队测试中，需要针对目标模型合理选择生成配置以获得最优攻击效果。

**提示多样性分析。** 为验证TEAR是否发生模式坍塌，实验从自BLEU距离和余弦不相似度两个维度评估了生成提示的多样性。如图5所示，TEAR在不同有害类别下生成的提示均保持高多样性，未出现重复或高度相似的对抗模式。这得益于时间感知重写规则（时间解构、顺序强制、时间-空间合成）的多样性以及PPO在线学习对探索行为的鼓励。

### 跨模型迁移性

TEAR生成的对抗提示具有强大的跨模型迁移能力，这是其实际威胁性的关键体现。如表3所示，在Hunyuan-Video上优化得到的对抗提示，迁移到Wan 2.2、CogVideoX和Open-Sora等其他开源模型时，平均迁移ASR达到**76.4%**，峰值达**82.6%**。图7的案例研究进一步展示了同一提示在不同模型上均能诱导生成相似的有害时序视频内容。这种高迁移性说明，TEAR挖掘的是T2V模型在时间理解上的共性缺陷，而非某个特定模型的独立漏洞——时序组合攻击构成了T2V模型族的结构性安全风险。

### 失败模式与局限性

尽管TEAR展现出强大的攻击能力，实验中仍存在若干值得关注的失败模式和局限：

1. **色情类别攻击效果受限。** 在商业T2V服务上，色情类别的ASR显著低于暴力、恐怖等其他类别。这可能源于商业模型针对色情内容部署了更细粒度的帧级检测机制。然而，由于缺乏对商业模型内部安全架构的可见性，这一解释需要手动验证。

2. **视频长度限制。** 实验默认视频长度主要为5-8秒，未系统评估更长视频或无限长生成场景下的攻击有效性。在更长的时间跨度下，时序组合攻击可能面临事件连贯性衰减或安全检测窗口增大的挑战。

3. **安全判断器偏见。** 文本安全分类器和视频有害性判断器（VLM）自身并非完美，可能引入评估偏见或漏报/误报。这意味着报告的ASR和提示通过率存在系统性误差，结果需谨慎解读。

4. **商业API调用约束。** 商业模型API的调用频率和配额限制可能影响在线RL训练的规模和频率，进而限制最终ASR的理论上限。在无约束环境下，TEAR的攻击效果可能进一步提升。

### 补充图表

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_He_TEAR_Temporal_aware/figures/003_Table_1.jpg]]
*Table 1: Success cases and prompt pass rate on 390 meta harmful seed prompts*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_He_TEAR_Temporal_aware/figures/004_Figure_3.jpg]]
*Figure 3: The effectiveness of TEAR on commercial T2V services*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_He_TEAR_Temporal_aware/figures/005_Table_2.jpg]]
*Table 2: Success cases and prompt pass rate on Seed-free generation*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_He_TEAR_Temporal_aware/figures/007_Figure_4.jpg]]
*Figure 4: The impact of refining rounds on ASR and NSFW Filter Pass Rate*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_He_TEAR_Temporal_aware/figures/009_Figure_6.jpg]]
*Figure 6: Impact of generation settings (Step, Scale, and Number of Frames on attack effectiveness and safe prompt generation*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_He_TEAR_Temporal_aware/figures/006_Figure_5.jpg]]
*Figure 5: Diversity of prompts generated by TEAR for different categories*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_He_TEAR_Temporal_aware/figures/010_Figure_7.jpg]]
*Figure 7: Case studies on the transferability of optimized problematic prompt*

![[assets/figures/papers/paper_list_l14_https_openaccess_thecvf_com_content_CVPR2026_html_He_TEAR_Temporal_aware/figures/001_Figure_1.jpg]]
*Figure 1: Textually safe prompts can generate temporally harmful videos, which is shown below the video frames*

## 方法谱系与知识库定位

### 1. 与现有红队测试方法的谱系关系

TEAR 的核心创新在于将红队测试的搜索空间从纯文本维度拓展至**时间语义组合维度**，这使其在方法谱系中处于文本对抗生成与视频安全评估的交叉地带。

#### 1.1 与文本红队方法的继承与突破

TEAR 继承了 LLM 红队测试中“以生成器驱动对抗样本发现”的基本范式。与 **GPTFuzzer** (Yu et al., arXiv 2023) 和 **DiverCT** (Zhao et al., AAAI 2025) 等面向 LLM 的越狱提示生成方法相比，TEAR 共享了“利用语言模型生成对抗输入”的技术基因，但存在本质差异：前者仅需突破文本安全分类器的单一防线，而 TEAR 必须同时满足**文本安全通过**与**视频有害生成**两个互相拮抗的约束条件。这一双重约束使得简单的文本扰动策略失效——TEAR 通过规则式时间解构-合成重写与 PPO 在线偏好学习的联合优化，将对抗信号的传递路径从“文本→文本”重构为“文本→视频→反馈”，实现了跨模态的攻击闭环。

#### 1.2 与文本到图像红队方法的对比

**FLIRT** (Mehrabi et al., EMNLP 2024) 和 **ART** (Li et al., NeurIPS 2024) 是当前文本到图像（T2I）自动红队测试的代表性工作。TEAR 与这两类方法的核心差异体现在以下四个维度：

| 对比维度 | FLIRT / ART | TEAR |
|---------|------------|------|
| **优化空间** | 仅文本空间（提示安全性与有害性评估） | 联合文本空间与时间一致性空间 |
| **提示生成策略** | 静态语义扰动或单步反馈循环 | 规则式时间解构-合成重写 + PPO 在线偏好学习 + MLLM 多轮迭代精化 |
| **奖励函数** | 仅依赖文本安全分类器（如仇恨言论检测） | 复合奖励：文本安全分类 + 时间模式对齐（余弦相似度） + 视频全局/内部一致性评分 |
| **数据构建** | 人工收集或简单 LLM 改写 | 三层时间感知规则式改写（时间解构、顺序强制、时间-空间合成），并经过安全双过滤 |

这一结构性的方法升级带来了显著的性能跃迁：在 Hunyuan-Video 上，TEAR 的 ASR 达到 82.3%，远超 FLIRT 的 57.2% 和 ART 的 52.6%（Table 1）；在 Wan 2.2 上，TEAR 的 ASR 为 80.5%，对比 FLIRT 的 56.4% 和 ART 的 49.7%（Table 1）。超过 25 个百分点的绝对提升表明，**忽略时间维度是现有 T2I 红队方法迁移至 T2V 场景时的根本性瓶颈**。

#### 1.3 在视频安全研究谱系中的定位

在视频安全评估领域，现有工作主要关注静态帧的内容审核（如暴力、色情帧检测）。TEAR 首次揭示了**事件时序组合**作为独立攻击面的存在——文本层面无害的片段通过特定的时间顺序编排，可在视频整体层面诱导出有害叙事。这一发现将视频安全研究的边界从“帧级内容合规”拓展至“时序语义安全”，为后续的防御机制设计提供了新的威胁模型。

### 2. 适用边界与限制条件

TEAR 的有效性依赖于若干关键前提，这些前提同时界定了其适用边界：

**模型访问假设**：TEAR 的在线偏好学习阶段需要与目标 T2V 模型进行交互以获取生成视频反馈。对于开源模型（如 Hunyuan-Video、Wan 2.2），这一假设自然成立；对于商业 T2V 服务（Veo-3.1、Hailuo-2.3、Ray 2），TEAR 通过 API 调用实现交互，但 API 的调用频率限制和内容审核机制可能约束在线 RL 训练的规模和频率，进而影响最终 ASR 的上限。实验表明，即使在商业服务的严格过滤下，TEAR 仍能实现接近 98% 的文本过滤通过率，同时多数有害类别的 ASR 维持在 85% 以上（Figure 3），说明当前商业防护体系对时间感知攻击存在系统性盲区。

**视频时长限制**：实验默认视频长度主要为 5-8 秒，未系统评估更长视频或无限长生成场景下的攻击有效性。在更长的时间跨度下，时序有害模式的构建可能需要更复杂的事件图结构，攻击成功率是否保持稳定尚需验证。

**安全判断器的可靠性**：TEAR 的奖励函数和评估体系依赖文本安全分类器与 VLM 判断器。这些判断器自身并非完美——文本分类器可能漏报隐晦的有害语义，VLM 对视频内容的评估可能存在偏见或误报。这意味着 TEAR 报告的 ASR 和文本通过率存在由判断器误差引入的系统性偏差，实际攻击效果可能被高估或低估。

**跨模型迁移的前提**：TEAR 生成的对抗提示具有高跨模型迁移性（平均迁移 ASR 达 76.4%，峰值 82.6%，Table 3），但这一迁移性建立在不同 T2V 模型共享相似的时序语义理解能力之上。对于架构或训练数据分布差异极大的模型，迁移效果可能显著下降。

### 3. 局限性与开放问题

#### 3.1 已识别的局限性

1. **时序长度的覆盖不足**：当前实验聚焦于 5-8 秒的短视频生成，未探索更长时序场景下的攻击有效性。随着 T2V 模型向长视频生成演进，攻击面的形态可能发生变化。
2. **判断器偏差**：文本安全分类器和 VLM 判断器自身的不完美可能引入评估偏差。TEAR 的 ASR 和文本通过率应被理解为“在给定判断器条件下的相对度量”，而非绝对的安全/有害边界。
3. **在线训练的规模受限**：商业模型 API 的调用限制可能约束在线 RL 训练的规模和频率，限制最终 ASR 的上限。在更宽松的 API 访问条件下，TEAR 的性能可能进一步提升。
4. **有害类别的不均衡**：在商业服务上，色情类别的 ASR 低于其他类别（Figure 3），表明不同有害类别的时间敏感性存在差异，TEAR 的通用攻击策略在某些类别上可能未达到最优。

#### 3.2 开放问题

1. **防御机制的缺失**：如何自动防御此类时间感知攻击？是否可在 T2V 模型中内置时序安全检查模块，在生成过程中实时检测有害事件序列的形成？这一方向目前完全空白。
2. **复杂时序场景的泛化**：在更复杂的事件图（如多分支时序场景、非线性叙事）中，攻击成功率是否会显著变化？TEAR 当前的三层规则式改写是否能覆盖更丰富的时序攻击模式？
3. **跨模态适配性**：TEAR 的框架——将有害语义分解为时序片段并通过在线优化诱导有害输出——能否直接适配到其他时序生成任务（如文本到语音、文本到 3D 动画）的安全测试？这涉及时间感知攻击是否为时序生成模型的通用脆弱性。
4. **奖励权重的自适应调节**：在线偏好学习过程中，奖励函数的权重系数（$\boldsymbol{\alpha}_1, \boldsymbol{\alpha}_2, \beta, \gamma_1, \theta_1$）如何自适应调整以平衡攻击效果与提示隐蔽性？当前固定权重的设计可能在不同目标模型或有害类别上未达到帕累托最优。
5. **评估标准的统一化**：当前视频有害性的判断依赖 VLM 的单一评分，缺乏统一的时序安全评估基准。社区是否需要建立包含时序有害标注的标准数据集，以消除判断器偏差对评估结果的影响？

### 4. 知识库定位总结

TEAR 在方法谱系中占据**首个面向 T2V 模型的时间感知自动红队测试框架**这一独特位置。它通过揭示“时序组合”作为独立安全维度的存在，将红队测试的方法论从纯文本空间拓展至跨模态时序空间，为视频生成安全研究开辟了新的子方向。其技术贡献——规则式时间解构-合成重写、PPO 驱动的在线偏好学习、MLLM 驱动的迭代精化——构成了一套可复用的时间感知对抗生成范式，对后续的视频安全评估与防御研究具有奠基性意义。

## 原文 PDF

![[paperPDFs/CVPR_2026/TEAR_Temporal_aware_Automated_Red_teaming_for_Text_to_Video_Models.pdf]]
