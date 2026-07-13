---
title: "Cultivating Pluralism In Algorithmic Monoculture: The Community Alignment Dataset"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Cultivating_Pluralism_In_Algorithmic_Monoculture_The_Community_Alignment_Dataset.pdf
project_link: https://huggingface.co/datasets/facebook/community-alignment-dataset
code_link: null
openreview_forum_id: 4NtoAVqfhA
aliases:
- NCS
- CPAMCAD
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/alignment_preference
core_operator: "采用负相关采样 (Negatively‑Correlated Sampling) 控制候选回复集合的生成，使同一集合内尽量减少相似价值观的回复。"
primary_logic: "当候选回复集合通过负相关采样获得时，即使在训练中只用一个模型生成，也能比用21个模型独立温度采样更有效地覆盖多种价值观，并使所有主流的对齐方法都能成功学习到不同价值观的偏好。"
claims:
- "21个SOTA LLM的英文回复仅与41%的人类偏好对齐，且几乎全部落在世俗‑理性/自我表达象限。"
- "负相关采样使传统/生存价值的平均覆盖率从温度采样的15%/30%提升至约60%/53%。"
- "在所有四种对齐方法（prompt‑steering、SFT、DPO、GRPO）下，使用NC采样数据集的胜率从约随机水平跃升至70–90%以上。"
- "PRISM prompts (Section 3.1) + Inglehart-Welzel 价值维度 上 传统价值 (Traditional) 回复覆盖率 = 60%"
---

# Cultivating Pluralism In Algorithmic Monoculture: The Community Alignment Dataset

> [!tip] 核心洞察
> 当候选回复集合通过负相关采样获得时，即使在训练中只用一个模型生成，也能比用21个模型独立温度采样更有效地覆盖多种价值观，并使所有主流的对齐方法都能成功学习到不同价值观的偏好。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 在算法单一文化中培育多元性：社区对齐数据集 |
| 英文题名 | Cultivating Pluralism In Algorithmic Monoculture: The Community Alignment Dataset |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=4NtoAVqfhA) · [Project](https://huggingface.co/datasets/facebook/community-alignment-dataset) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/alignment_preference |
| Method | 负相关候选采样 (Negatively‑Correlated Sampling) |
| Dataset | PRISM prompts (Section 3.1) + Inglehart-Welzel 价值维度, 同上, PRISM prompts, SFT+DPO on Llama-3.3-70B Instruct, SFT+GRPO on Llama-3.1-8B Instruct |

> [!tip] 效果简介
> - PRISM prompts (Section 3.1) + Inglehart-Welzel 价值维度 上，传统价值 (Traditional) 回复覆盖率 为 60%，对比 15%（温度采样平均），变化 +45%。
> - 同上 上，生存价值 (Survival) 回复覆盖率 为 53%，对比 30%（温度采样平均），变化 +23%。
> - PRISM prompts, SFT+DPO on Llama-3.3-70B Instruct 上，自我表达 (Self‑expression) 方向的胜率 (vs 原始模型) 为 0.958 ± 0.006 (NC sampling)，对比 ~0.5 (温度采样 τ=1, 1 LLM)，变化 > +0.45。

## 概要

现有对齐方法在构建偏好数据集时，候选回复几乎全部通过温度采样生成。这种独立采样策略导致候选集合高度同质化——所有回复集中在“世俗‑理性”与“自我表达”的价值端，而“传统”与“生存”价值观几乎完全缺失。大规模人类研究（五国、N=15,000）证实，人类偏好呈现显著的异质性，但21个主流LLM的回复仅与41%的人类偏好对齐，且几乎全部落在同一价值象限（Figure 1）。这一“算法单一文化”现象的根本瓶颈在于：候选集合缺乏价值观多样性，使得任何对齐方法都无法学习到多样的人类偏好。

本文的核心洞察是：**控制候选集合的生成方式，而非简单地增加模型数量或采样温度，才是打破算法单一文化的关键杠杆**。基于此提出的负相关采样（Negatively‑Correlated Sampling, NC sampling），通过提示单一模型同时生成四个代表不同价值观的回复，并要求回复之间具有多样性，从而在候选集合层面主动引入价值观差异。

NC采样的效果具有决定性：仅使用一个模型，就将传统价值的平均覆盖率从温度采样的15%提升至60%，生存价值从30%提升至53%（Figure 2），且显著超越了21个模型独立温度采样的效果。更重要的是，在四种主流对齐方法（prompt‑steering、SFT、DPO、GRPO）下，使用NC采样数据集的胜率从约随机水平跃升至70–90%以上（Figure 3, Table E.1），证明候选集合多样性是对齐学习成功的必要条件。基于这一技术，本文构建并开源了Community Alignment数据集——目前最大的多语言偏好数据集，覆盖五种语言、233K偏好比较。

### 算法单一文化：大语言模型的价值偏好同质化

当前主流大语言模型（LLM）在生成回复时表现出显著的价值偏好同质化现象。一项覆盖美国、法国、意大利、印度和巴西五国、共15,000名参与者的多语言人类研究显示，个体在LLM回复中所偏好的价值观存在高度异质性——即使在同一国家内部，人们对世俗-理性与传统、自我表达与生存等价值维度的偏好也呈现广泛分布（Figure 1左侧）。然而，21个最先进LLM的英文回复几乎全部集中在世俗-理性与自我表达的价值象限，仅与约41%的人类偏好对齐（Figure 1右侧）。这种“算法单一文化”意味着大量持有传统或生存价值观的用户群体在现有模型中被系统性忽视。

### 候选回复生成的瓶颈：独立温度采样导致价值覆盖不足

造成这一问题的根本原因并非对齐算法本身，而在于偏好数据集的构建方式。现有偏好数据集的候选回复通常由温度采样（Temperature Sampling, τ=1）独立生成，这种策略使得同一提示下的多个候选回复在语义和价值观上高度相似。实验表明，温度采样对传统价值的平均覆盖率仅为15%，对生存价值的平均覆盖率仅为30%（Figure 2蓝色部分）。即使尝试通过从21个不同LLM独立采样来增加多样性，候选集合仍然无法有效覆盖这些被忽视的价值维度。当偏好数据集中缺乏某一价值端的样本时，任何对齐方法——无论是提示引导、监督微调（SFT）、直接偏好优化（DPO）还是群体相对策略优化（GRPO）——都无法学习到相应的偏好，导致对齐后的模型在这些维度上的胜率接近随机水平。

### 核心洞察：负相关采样打破候选同质性

本文的核心洞察在于：候选回复集合的多样性——而非模型数量或对齐算法的选择——是学习多元人类偏好的关键因果杠杆。当候选回复通过**负相关采样（Negatively-Correlated Sampling）**生成时，即要求单一模型同时生成四个代表不同价值观的回复并明确要求回复间具有多样性，候选集合的价值覆盖发生根本性改变：传统价值覆盖率跃升至60%，生存价值覆盖率提升至53%（Figure 2橙色部分）。这一简单提示策略带来的帕累托改进，使得仅使用一个模型生成的候选集合，其价值多样性远超21个模型独立温度采样的效果。更重要的是，在此数据集上，所有四种主流对齐方法均能成功学习到不同价值观的偏好，胜率从随机水平跃升至70%–90%以上（Figure 3, Table E.1）。

## 核心方法与创新机理

### 问题瓶颈：候选回复集合的同质化

现有偏好数据集构建流程中存在一个被长期忽视的结构性缺陷：候选回复的生成方式导致集合内部缺乏真正的价值观多样性。具体而言，当使用温度采样（Temperature Sampling, τ=1）从单个或甚至多个模型生成候选回复时，这些回复几乎全部集中在 Inglehart-Welzel 价值框架中的**世俗-理性（Secular-Rational）与自我表达（Self-Expression）**象限。Figure 1 的证据表明，21 个 SOTA LLM 的英文回复仅与 41% 的人类偏好对齐，且系统性地排斥传统价值（Traditional）与生存价值（Survival）的表达。这意味着，无论标注者如何选择，模型能从中学习的偏好信号本身就被限制在一个狭窄的价值区间内——**算法单一文化（Algorithmic Monoculture）的根源不在标注环节，而在候选生成环节**。

### 核心因果机制：负相关采样

针对上述瓶颈，本文提出的关键创新是**负相关采样（Negatively-Correlated Sampling, NC Sampling）**。其核心思想是改变候选回复集合的生成策略，从“独立同分布采样”转向“显式诱导集合内多样性”。

具体的 changed slot 如下：

| 模块 | 基线策略 | 负相关采样策略 |
|------|----------|----------------|
| **候选回复生成** | 独立温度采样（τ=1），各候选回复相互独立，或从 21 个不同 LLM 独立采样以试图增加多样性 | 提示单一模型**同时**生成四个代表不同价值观的回复，并要求回复之间具有多样性（`Generate four responses that represent diverse values...`） |

这一设计的因果逻辑在于：当候选集合内各回复之间存在负相关关系——即一个回复的出现降低了相似回复被选中的概率——标注者才真正有机会在不同价值取向上做出选择。NC 采样通过简单的提示工程实现这一目标，且**未在指令中显式提及 Inglehart-Welzel 的具体价值维度**，模型仍能自发地产生覆盖多元价值观的回复。

### 决定性证据

NC 采样的效果在多个层面得到验证：

1. **候选集合覆盖率的帕累托改进**：Figure 2 显示，NC 采样将传统价值的平均覆盖率从温度采样的 15% 提升至约 60%，生存价值覆盖率从 30% 提升至约 53%，在所有四个 IW 维度上均实现了帕累托改进。

2. **超越多模型策略的单模型效率**：消融实验证实，NC 采样仅使用一个模型即可**显著超越**从 21 个模型独立温度采样的效果。这揭示了模型多样性（增加模型数量）并非解决候选同质化的有效途径，关键在于采样策略本身的相关性结构。

3. **对齐学习的普适性提升**：Table E.1 和 Figure 3 表明，在四种主流对齐方法（prompt-steering、SFT、DPO、GRPO）下，使用 NC 采样数据集的模型胜率从接近随机水平（~0.5）跃升至 70–90% 以上。这一结果在两个模型规模（Llama-3.1-8B 和 Llama-3.3-70B）上均成立，证明 NC 采样的收益不依赖于特定对齐算法或模型规模。

### 局限与待验证点

NC 采样目前完全依赖提示工程实现，其有效性受限于模型遵循指令的能力。在资源较少的语言（如印地语）上，模型可能无法充分理解“多样性”指令，导致负相关采样失效——这需要进一步的手动验证。此外，虽然 NC 采样更容易覆盖极端价值观，但在实际部署中需要谨慎控制对齐方向，防止产生不希望的价值表达。

![[assets/figures/papers/iclr26_0011_4NtoAVqfhA_Cultivating_Pluralism_In_Algorithmic_Monoculture/figures/005_Table_1.jpg]]
*Table 1: Comparison of Community Alignment to other open-source preference datasets*

该工作构建了一个从“诊断算法单一文化”到“通过负相关采样培育多元性”的完整流水线。核心瓶颈在于：现有偏好数据集的候选回复几乎全部集中在世俗‑理性与自我表达价值端，传统与生存价值的表现严重不足，导致标准对齐方法无法学习多样的人类偏好（Figure 1）。流水线由三个关键模块串联而成：

**1. 候选回复生成 (Candidate Response Generation)**
这是整个流水线的核心创新。传统方法采用独立温度采样（$\tau=1$），候选回复之间相互独立，导致生成的候选集合高度同质化。本研究提出**负相关采样 (Negatively‑Correlated Sampling)**：通过提示单一模型同时生成四个代表不同价值观的回复，并要求回复之间具有多样性（“Generate four responses that represent diverse values...”），使得同一候选集合内相似价值观的回复出现概率降低。该策略仅依赖提示工程，未显式指定价值观维度，却能在候选集合层面实现帕累托改进——传统价值的平均覆盖率从温度采样的15%提升至60%，生存价值从30%提升至53%（Figure 2）。值得注意的是，仅使用一个模型进行NC采样，其效果已显著超越从21个不同LLM独立温度采样的方案。

**2. 偏好标注 (Preference Annotation)**
在获得覆盖多元价值观的候选回复集合后，由人类标注者选择偏好的回复。主研究采用大规模多语言人类调查，从五个国家（美国、法国、意大利、印度、巴西）招募代表性样本（$N=15,000$），标注者经过年龄、性别、族裔的平衡抽样。消融实验与对齐学习实验中，则使用GPT‑4o裁判模拟人类选择——该裁判在手工标注测试集上对世俗‑理性/传统维度的判断准确率为85.8%，对自我表达/生存维度的准确率为78.3%。

**3. 对齐学习 (Alignment Tuning)**
使用上述偏好数据集对基础模型进行对齐训练，涵盖四种主流方法：prompt‑steering、SFT、DPO和GRPO。实验在Llama‑3.3‑70B Instruct和Llama‑3.1‑8B Instruct两个规模上验证。当使用NC采样构建的数据集时，所有对齐方法在四种Inglehart‑Welzel价值观方向上的胜率均从约随机水平（~0.5）跃升至70–90%以上（Table E.1，Figure 3）；而使用温度采样数据时，即使从21个LLM采样，各方法仍难以有效引导模型朝向目标价值观。

**输入输出流**：流水线以日常提示（60个精心策划的提示）为输入，经NC采样生成每组四个候选回复，由人类或GPT‑4o裁判标注偏好，最终输出对齐后的模型。基于此流水线，作者构建并开源了Community Alignment数据集——目前最大的开源多语言偏好数据集，包含233K条对比、覆盖五种语言、来自3,603名标注者，且每位标注者贡献的中位会话数（26次）远超PRISM数据集（6次）（Table 1，Figure F.1）。

### 候选回复生成：负相关采样

本工作的核心模块是**负相关采样（Negatively‑Correlated Sampling, NC Sampling）**，其设计动机源于一个关键发现：传统温度采样（τ=1）生成的候选回复集合在价值观维度上高度同质化，几乎全部集中在世俗‑理性与自我表达象限，导致传统与生存价值方向的回复覆盖率极低（分别仅为15%和30%）。NC采样通过改变候选回复的生成策略来打破这一瓶颈。

**实现方式**：NC采样并不依赖多模型集成或复杂的解码算法，而是通过提示工程实现。具体而言，向单一模型发出如下指令：要求同时生成四个代表不同价值观的回复，并明确要求回复之间具有多样性。论文指出，即使提示中未显式指定具体的价值观维度，该策略也能有效诱导模型产生价值观层面的负相关性——即一个候选集合中已包含某类价值观回复时，其他回复倾向于覆盖不同的价值取向。

**效果**：在相同的日常提示集合上，NC采样使传统价值的平均覆盖率从温度采样的15%提升至约60%，生存价值的覆盖率从30%提升至约53%（Figure 2）。更关键的是，仅使用一个模型进行NC采样，其候选集合的价值观多样性就显著超越了从21个不同LLM独立温度采样的效果。

### 偏好标注与对齐学习流水线

完整的流水线包含三个模块：

1. **候选回复生成**：使用NC采样为每个提示生成一组四个候选回复，覆盖多样价值观。
2. **偏好标注**：主研究中由人类标注者从候选集合中选择偏好回复；消融与对齐学习实验中，使用GPT‑4o裁判模拟人类选择。裁判在手工标注测试集上的准确率为：世俗‑理性 vs 传统维度85.8%，自我表达 vs 生存维度78.3%。
3. **对齐学习**：使用获得的偏好数据集对基础模型进行对齐训练，覆盖四种主流方法——prompt‑steering、SFT、DPO和GRPO。

### 关键公式

本文未提出新的数学公式或推导。负相关采样的核心机制是**候选集合构建策略的定性改变**，而非数学优化。其效果通过经验覆盖率指标（给定采样方法在四候选集合中至少包含一个符合特定价值观回复的比例）和胜率指标（对齐后模型相对于原始模型在特定价值观方向上的偏好胜率）来量化评估。

若需深入理解NC采样的形式化定义，可参考论文中关于“负相关”概念的描述：候选集合中某一特定回复的纳入会降低另一个相似回复被纳入的概率。但论文未给出该概念的严格概率公式，仅通过提示工程近似实现这一原则。

## 实验与关键发现

### 核心瓶颈：候选回复集的价值观单一性

本研究的实验围绕一个关键瓶颈展开：传统偏好数据集的候选回复生成方式（独立温度采样）导致候选集合几乎完全集中在世俗‑理性与自我表达价值端，严重缺乏传统与生存价值的表达。Figure 1 直观地呈现了这一现象——左侧散点图显示人类参与者的偏好分布具有显著异质性，而右侧 21 个 SOTA LLM 的回复则系统性地聚集在世俗‑理性/自我表达象限，仅与 41% 的人类偏好对齐（置信度 0.95）。这一“算法单一文化”构成了所有后续实验的基线问题。

![[assets/figures/papers/iclr26_0011_4NtoAVqfhA_Cultivating_Pluralism_In_Algorithmic_Monoculture/figures/002_Figure_1.jpg]]
*Figure 1: Human pluralism vs algorithmic monoculture.. Individuals show substantial heterogeneity in the values they prefer in LLM responses, even within the U.S. (left). However, all 21 state-of-the-art language models systematically output responses towards secular-rational and selfexpression values (right). See Figure C.2 for results in France, Italy, India, and Brazil*

### 负相关采样的覆盖效果

负相关采样（Negatively‑Correlated Sampling, NC sampling）通过提示单一模型同时生成四个代表不同价值观的回复，并要求回复之间具有多样性，从根本上改变了候选集合的生成策略。Figure 2 展示了该策略在 Inglehart‑Welzel 四个价值维度上的覆盖效果：

![[assets/figures/papers/iclr26_0011_4NtoAVqfhA_Cultivating_Pluralism_In_Algorithmic_Monoculture/figures/003_Figure_2.jpg]]
*Figure 2: Temperature sampling has limited coverage of Inglehart-Welzel values (blue), but NC sampling yields Pareto improvements (orange). For the set of everday prompts curated in Section 2.1, each plot captures the proportion of times that a given sampling method yields at least one example aligning with a certain value within a set of four candidate responses. With temperature sampling, the mean coverage of traditional and survival values, averaged across models, is 15% and 30%. With NC sampling, the mean coverage of traditional and survival values increases to 60% and 53%. See Section H.1 for qualitative examples of the candidate sets generated by temperature sampling and NC sampling*

| 价值维度 | 温度采样平均覆盖率 | NC 采样平均覆盖率 | 提升幅度 |
|---------|-------------------|------------------|---------|
| 传统价值 (Traditional) | 15% | 60% | +45% |
| 生存价值 (Survival) | 30% | 53% | +23% |

NC 采样在所有四个维度上实现了帕累托改进（置信度 0.95）。值得注意的是，这一改进仅通过单一模型实现——消融实验表明，NC 采样使用一个模型即可显著超越从 21 个不同 LLM 独立温度采样的效果（置信度 0.95），且提示指令中并未显式指定价值观维度（置信度 0.9）。

### 对齐学习的胜率提升

Figure 3 和 Table E.1 报告了四种对齐方法（prompt‑steering、SFT、SFT+DPO、SFT+GRPO）在温度采样与 NC 采样数据集上的胜率对比。在温度采样条件下，所有方法对四种价值观的胜率均接近随机水平（约 0.5）；切换至 NC 采样数据集后，胜率跃升至 70–90% 以上（置信度 0.95）。以 Llama-3.3-70B Instruct 为例：

![[assets/figures/papers/iclr26_0011_4NtoAVqfhA_Cultivating_Pluralism_In_Algorithmic_Monoculture/figures/004_Figure_3.jpg]]
*Figure 3: Win rates of models tuned with 4 alignment methods, against the original models, with respect to the four IW values. While all methods struggle to steer towards these values when using temperature-sampled responses (blue, orange), even when sampled from 21 LLMs (the original PRISM responses), they all substantially improve in performance when using a dataset constructed via NC sampling (green). Error bars are standard error of mean*

![[assets/figures/papers/iclr26_0011_4NtoAVqfhA_Cultivating_Pluralism_In_Algorithmic_Monoculture/figures/019_Figure_3.jpg]]
*Figure 3: Table E.1: Win rates of models tuned with 4 alignment methods, against the original models, with respect to the four IW values. While all methods struggle to steer towards these values when using temperature-sampled responses, even when sampled from 21 LLMs (the original PRISM responses), they all substantially improve in performance when using a dataset constructed via NC sampling. Same results as those presented in Figure 3 of Section 3*

- **自我表达方向**：SFT+DPO 在 NC 采样下的胜率为 $0.958 \pm 0.006$，而温度采样（τ=1, 1 LLM）仅约 0.5。
- **传统价值方向**：SFT+GRPO 在 NC 采样下的胜率为 $0.827 \pm 0.010$。

该提升在 8B 和 70B 两个模型规模上一致成立，且跨所有四种对齐方法和四种价值观维度均呈现帕累托改进。

### 裁判模型可靠性

偏好学习实验使用 GPT‑4o 裁判替代人类标注进行大规模评估。在人工标注测试集上，裁判模型准确率为：世俗‑理性 vs 传统维度 85.8%，自我表达 vs 生存维度 78.3%（Table C.1，置信度 0.9）。虽然存在系统性偏差的可能，但其相对对比仍能有效揭示候选集合多样性对对齐学习的影响。

### 数据集规模与标注质量

Community Alignment 数据集在规模和多语言覆盖上显著优于现有开源偏好数据集（Table 1）：包含 233K 偏好比较（vs PRISM 的 169K 和 HH 的 27K），66% 为非英语数据，覆盖 5 个国家、3,603 名标注者。每位标注者贡献的中位会话数为 26，远高于 PRISM 的 6（Figure F.1，置信度 0.95），为个体层面的偏好分析提供了更细粒度的支持。

### 局限性与失败模式

1. **价值维度覆盖有限**：仅聚焦于 Inglehart‑Welzel 两个维度（世俗‑理性/传统、自我表达/生存），未涵盖政治光谱等更一般的偏好差异。
2. **裁判偏差**：偏好学习实验使用 GPT‑4o 裁判，其评分可能引入系统性偏差，但用于比较候选集合影响的相对结论仍然有效。
3. **多语言鲁棒性**：NC 采样依赖模型遵循提示指令的能力，在印地语等资源较少的语言上，模型生成回复的价值观表达丰富度可能不足（Table C.2 展示了英/印地语回复的质性差异）。
4. **部署控制**：NC 采样虽能覆盖极端价值观，但在实际部署中需谨慎控制对齐方向，防止产生不希望的输出。
5. **标注者代表性**：标注者虽在年龄、性别、族裔上有所平衡，但教育水平和政治倾向分布可能仍不具代表性（Tables F.5–F.6），需手动验证。

![[assets/figures/papers/iclr26_0011_4NtoAVqfhA_Cultivating_Pluralism_In_Algorithmic_Monoculture/figures/007_Table_2.jpg]]
*Table 2: Table C.1: Accuracy of the judge model from our joint human study and model evaluation, broken down by value dimension and language*

## 定位与知识库关联

### 与现有候选生成策略的关系

当前主流偏好数据集的候选回复生成几乎全部依赖**独立温度采样**（Temperature Sampling, τ=1），无论使用单一模型还是21个不同LLM，候选回复之间相互独立。这一策略的根本缺陷在于：它无法突破模型自身的价值分布倾向——所有SOTA LLM的输出几乎全部集中在Inglehart-Welzel文化维度的世俗-理性与自我表达象限（Figure 1）。即使从21个不同模型采样以试图引入“模型多样性”，传统价值的平均覆盖率也仅为15%，生存价值约为30%（Figure 2）。

**负相关采样（Negatively-Correlated Sampling, NC sampling）** 改变了这一范式：它通过提示单一模型同时生成四个代表不同价值观的回复，并要求回复之间具有多样性，从而在候选集合内部主动引入负相关结构。核心机制在于：当某一回复被纳入候选集时，相似价值观的回复被排斥，这迫使模型探索其输出分布中原本被抑制的区域。实证表明，仅用一个模型的NC采样即可将传统与生存价值的覆盖率分别提升至约60%和53%，显著超越21个模型独立温度采样的效果（Figure 2, Section 3）。

从方法谱系看，NC采样属于**基于提示的多样性诱导策略**，与更复杂的多样性采样方法（如基于嵌入的聚类重采样、对比解码）相比，其优势在于实现极简且无需额外模型或训练。论文明确指出，“即使这些价值观并未在指令中显式提及”，简单的提示工程即可有效实现负相关（Section 3）。这使其成为当前最轻量级的候选集多样化方案。

### 适用边界

NC采样的有效性建立在两个前提之上：

1. **模型遵循提示指令的能力**：NC采样依赖于模型理解并执行“生成多样价值观回复”的指令。在英文等资源丰富语言上，主流模型（如Llama 3.3 70B）表现出足够的指令遵循能力。但在印地语等资源较少的语言上，模型可能难以产生同样丰富的价值观表达，需要更精细的方法设计（Limitations）。

2. **价值维度的可提示性**：当前仅验证了Inglehart-Welzel的两个维度（世俗-理性/传统、自我表达/生存）。这些维度具有明确的文化理论支撑，但并非所有人类偏好差异都能被如此清晰地映射。论文将此列为开放问题：如何将NC采样扩展到更一般的价值维度（如政治光谱）尚待探索（Open Questions）。

在部署层面，NC采样虽然更容易覆盖极端价值观，但需要谨慎控制对齐方向。论文明确指出，在模型优化后，需要评估其是否会产生不希望的输出（Limitations）。这意味着NC采样更适合作为**偏好数据构建工具**，而非直接部署的生成策略。

### 局限与开放问题

**已验证的局限**：

- **价值覆盖的有限性**：仅聚焦于Inglehart-Welzel两个维度，未涵盖所有可能的人类偏好差异。不同文化背景下同一价值观维度的语义差异如何影响候选生成和对齐学习，仍需进一步研究（Limitations, Open Questions）。
- **评估代理的偏差**：偏好学习实验使用GPT-4o裁判替代真实人类标注。尽管裁判在手持标注测试集上的准确率为85.8%（世俗-理性/传统）和78.3%（自我表达/生存），其评分仍可能引入系统性偏差。论文承认这一局限，但同时指出用于比较候选集合影响的相对结论仍然有效（Fairness Notes, Limitations）。
- **标注者代表性的不足**：虽然标注者来自五个国家，经过年龄、性别、族裔的平衡抽样，但老年人和教育水平未完全平衡，教育水平和政治倾向分布可能仍不具代表性（Fairness Notes, Limitations）。

**待解决的开放问题**：

- **控制粒度的提升**：如何在NC采样中更精确地控制生成回复的价值观表达强度？当前方法仅能“覆盖”某价值观，但无法精细调节其表达程度（Open Questions）。
- **多语言扩展**：能否利用回译等技术诱导模型在非英语语言中产生更丰富的价值观表达？这是将NC采样推广到全球多语言场景的关键挑战（Open Questions）。
- **在线偏好收集的结合**：能否将NC采样与在线偏好收集方法结合，进一步提升采样效率和个性化程度？这指向了从静态数据集向动态、交互式偏好学习的演进方向（Open Questions）。

## 原文 PDF

![[paperPDFs/ICLR_2026/Cultivating_Pluralism_In_Algorithmic_Monoculture_The_Community_Alignment_Dataset.pdf]]
