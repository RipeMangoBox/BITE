---
title: "AdAEM: An Adaptively and Automated Extensible Measurement of LLMs' Value Difference"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AdAEM_An_Adaptively_and_Automated_Extensible_Measurement_of_LLMs_Value_Difference.pdf
aliases:
- AdAEM
tags:
- ICLR_2026
- topic/safety_alignment_fairness_privacy
- topic/safety_alignment_fairness_privacy/fairness_equity_justice_and_safety
core_operator: "通过自动探测来自不同文化和开发时期的多样化LLMs的价值边界，并以信息论目标指导上下文优化，自适应地生成具有争议性的测试问题，从而最大限度地暴露模型间的价值分歧。"
primary_logic: "将价值评估重新构造为一个信息瓶颈问题：在无人工标注和微调的条件下，交替优化问题与回答，使生成的测试问题既能最大化不同LLM价值分布的广义Jensen-Shannon散度（区分度），又能最小化问题自身价值观对回答的支配（解耦），从而比静态基准更有效地区分模型的价值取向。"
claims:
- "AdAEM生成的问题在人工评估中，价值区分度比人工创建的问题提升52%，且合理性提升8.7%，注释者间一致性Cohen's κ=0.93。"
- "基于AdAEM Bench-MFT评估，四个不同LLMs的价值取向相关系数仅为-0.169（远低于MFQ的~0.6和ValueBench的~0.56），而跨价值维度的标准差高达0.212（其余二者约0.1），表明AdAEM能揭示更深层的价值差异。"
- "可控价值启动实验显示，在GPT-5上使用AdAEM Bench-MFT时，目标价值维度得分显著上升（如Sanctity提升224%），而对立维度下降，证明了评估结果的效度。"
- "AdAEM Bench vs. MFQ & ValueBench (Moral Foundations) 上 平均值向量相关系数 (Avg. Corr.) = -0.169"
---

# AdAEM: An Adaptively and Automated Extensible Measurement of LLMs' Value Difference

> [!tip] 核心洞察
> 将价值评估重新构造为一个信息瓶颈问题：在无人工标注和微调的条件下，交替优化问题与回答，使生成的测试问题既能最大化不同LLM价值分布的广义Jensen-Shannon散度（区分度），又能最小化问题自身价值观对回答的支配（解耦），从而比静态基准更有效地区分模型的价值取向。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AdAEM：一种自适应且自动可扩展的LLMs价值差异测量方法 |
| 英文题名 | AdAEM: An Adaptively and Automated Extensible Measurement of LLMs' Value Difference |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qNlTH4kYJZ); [GitHub](https://github.com/microsoft/ValueCompass/tree/main/AdAEM) |
| Topic | #topic/safety_alignment_fairness_privacy #topic/safety_alignment_fairness_privacy/fairness_equity_justice_and_safety |
| Method | AdAEM |
| Dataset | AdAEM Bench vs. MFQ & ValueBench (Moral Foundations), 控制价值启动实验 (GPT-5 + AdAEM Bench-MFT) |

> [!tip] 效果简介
> - AdAEM Bench vs. MFQ & ValueBench (Moral Foundations) 上，平均值向量相关系数 (Avg. Corr.) 为 -0.169，对比 ~0.6 (MFQ), ~0.56 (ValueBench)，变化 显著降低（负相关 vs 中等正相关）。
> - AdAEM Bench vs. MFQ & ValueBench (Moral Foundations) 上，平均值向量标准差 (Avg. Std.) 为 0.212，对比 ~0.1 (MFQ & ValueBench)，变化 约2倍差距，区分度更高。
> - 控制价值启动实验 (GPT-5 + AdAEM Bench-MFT) 上，目标价值维度得分提升百分比 为 Sanctity +224.05%, Loyalty +81.77%, Authority +71.30%，对比 基准得分（Sanctity 30.19, Loyalty 54.35等），变化 巨大提升，对立维度下降。

## 概述

**AdAEM**（一种自适应且自动可扩展的LLMs价值差异测量方法）直面当前大语言模型价值评估的核心瓶颈：现有基准（如SVS、ValueBench、MFQ等）依赖固定、人工编写或过时的测试问题，所捕获的价值差异高度趋同，仅反映无害性等浅层安全特征，无法真实刻画模型在文化适应、道德基础等方面的深层分歧（图1(a)）。本文提出将价值评估重新构造为**信息瓶颈问题**：在不依赖人工标注和模型微调的条件下，通过自动探测来自不同文化和开发时期的多样化LLMs的内部价值边界，并以信息论目标驱动上下文优化（Eq.1），自适应地生成最具争议性的测试问题，从而最大限度地暴露模型间的价值分歧。

具体而言，AdAEM以少量通用社会话题为起点，采用多臂老虎机探索策略与基于期望最大化（EM）的迭代精炼过程，交替优化回答与问题：**响应生成步（E步）** 和 **问题精炼步（M步）** 各自通过得分函数（Eq.2-3）最大化广义Jensen‑Shannon散度（GJS），以鼓励不同LLM价值分布的可分性，同时通过解耦正则项避免问题自身价值观支配模型回答。由此自动产出的问题集（AdAEM Bench）在信息量和区分度上远超静态基准，并可在Schwartz基本价值理论或Moral Foundations Theory等框架下进行聚合评测。

**核心结论与主要结果：**

- 人工评估表明，AdAEM生成的问题在**价值区分度**上比人工创建的问题提升**52%**，且**合理性**提升**8.7%**，注释者间一致性达Cohen's κ=0.93。
- 在Moral Foundations Theory下，四款不同LLMs的价值取向相关系数仅为 **‑0.169**（远低于MFQ的~0.6和ValueBench的~0.56），而跨价值维度标准差达 **0.212**（其余二者约0.1），证实AdAEM能揭示更深层的价值差异（Table 15）。
- 可控价值启动实验显示，采用AdAEM Bench‑MFT后，GPT‑5在**Sanctity**维度得分飙升**224%**，对立维度则显著下降，验证了评估结果的效度（Table 16）。
- 方法具备良好的鲁棒性：使用更小参与LLM集合生成的基准（AdAEM‑2）与原基准结果高度一致（ICC=0.816，Pearson=0.790）；即使在仅200‑1000个问题的有限样本上，评估结果仍与全量问题保持中到高度相关（Figure 21），且多子集分裂测试的Cronbach's α达0.8991。

综上，AdAEM通过自动、自适应的动态问题生成机制，为大规模、细粒度、可扩展的LLM价值评估提供了信息论基础下的解决方案，显著优于传统静态基准。

## 背景与动机

大语言模型（LLM）的安全性研究与对齐实践中，理解并量化模型的内在价值观已成为关键环节。然而，现有的价值评估基准普遍面临信息瓶颈：它们多采用静态、人工设计或简单合成的通用问题集（如Schwartz价值问卷SVS、道德基础问卷MFQ，以及ValueBench等），这些问题不仅容易受到数据污染和时效性影响，更关键的是，它们只能诱发出不同LLM之间共享的、浅层的安全价值（例如无害性），使得评估结果高度趋同、难以区分。正如图1(a)所示，在回答通用问题时，不同LLM表现出的价值观几乎不可分辨。实验数据进一步佐证了这一点：在MFQ和ValueBench等静态基准下，被评估模型的平均价值向量相关系数高达约0.56～0.6，而跨价值维度的标准差仅约0.1（Table 15），这意味着现有的测试问题无法有效捕捉模型在文化适应性、道德倾向、偏见等深层维度的真实价值分歧。

这一困境的核心原因在于，常规基准的固定问题集无法主动触及多样化LLM参差的价值边界。随着LLM在地域文化布局和开发周期上的不断延伸，静态测试正迅速丧失信息量，急需一种能自动、持续地探测模型价值分歧的评估范式。图1(b)揭示了一个重要线索：当测试问题涉及近期、区域相关的话题（如加州山火）时，不同模型的价值观差异可被显著放大。受此启发，本文提出将价值评估重新构造成一个**信息瓶颈优化问题**：在无任何人工标注和模型微调的前提下，通过交替优化问题与回答，使得所生成的测试问题既能最大化不同LLM价值分布的广义Jensen-Shannon散度（提升区分度），又能最小化问题本身携带的价值观对回答的支配（实现解耦）。整体框架如图2所示：左侧的问题精炼步骤持续提升信息量，右侧的回答生成步骤激发模型的价值差异。

正是基于这一动机，我们设计了AdAEM——一种自适应且自动可扩展的LLM价值差异测量方法。它从少量通用社会话题出发，利用多臂老虎机探索策略和EM式迭代优化（见Eq.(1)），不断创建并精炼出能够引发价值冲突的问题。与静态基准的根本区别在于：AdAEM跳出了"固定题目"的局限，在不依赖人工监督的条件下，自动覆盖了106个国家或地区、超过1.2万个测试问题（Table 1），其语义多样性（Self-BLEU 13.42, 语义相似度 0.44）显著优于已有基准。

初步的人机协同验证强有力地支撑了本文的动机：在人工评估中，AdAEM生成的问题相较于人工编写问题，在价值区分度上提升52%，合理性提升8.7%（注释者间一致性Cohen's κ=0.93，Table 9）；当使用AdAEM Bench-MFT评估四款不同LLM时，模型间的平均价值相关系数降至**-0.169**（远低于MFQ的~0.6和ValueBench的~0.56），而跨维度的标准差升至**0.212**（为其余二者约2倍）（Table 15），清晰表明该方法能够揭示更深层的价值差异。此外，在GPT-5上的可控价值启动实验显示，AdAEM下的目标道德维度得分可产生巨大的正向偏移（如Sanctity提升224.05%），而对立维度则相应下降（Table 16），证明了评估结果的效度。这些证据一致表明，构建一种以信息论目标驱动的自适应价值评估体系，是突破现有基准瓶颈、深度测量LLM价值差异的必要路径。

## 核心创新

现有价值评估基准（SVS、ValueBench、MFQ 乃至 ValueDCG）的共同瓶颈在于使用固定、通用或过时的问题，这些题目倾向于反映不同 LLM 共享的浅层安全价值（如无害性），导致评估结果高度正相关、区分度极低，无法捕捉文化适应性与深层价值分歧。AdAEM 将这一瓶颈重新构造为一个信息瓶颈问题：如何在无人工标注、无微调的条件下，**自动且自适应地生成最大化模型间价值分布差异的问题**，从而暴露真实的价值边界。

### 关键 changed slots

1. **测试问题由静态固定变为自适应生成**  
   传统基准依赖人工编写或半自动合成的静态问题集，既容易过时又易受数据污染。AdAEM 从少量通用社会话题出发，使用基于 UCB 的多臂老虎机探索策略不断发现争议性话题，再通过 EM 式迭代精炼（响应生成步与问题精炼步交替）持续创建并优化引发价值分裂的问题。整个过程**完全自动化，无需任何人工标注或微调**。这使得最终生成的 AdAEM Bench 包含 12 310 个覆盖 106 个国家/地区的问题，其语义多样性（Self-BLEU 13.42）和覆盖广度（Figure 3，t-SNE 可视化）显著优于 SVS（57 题）、ValueBench（40 题）甚至 ValueDCG（4561 题）。

2. **信息量保证从经验设计转向信息论优化**  
   静态基准无法系统保证题目区分度。AdAEM 明确将问题优化目标定义为一个**信息论目标函数**：
   $$\mathbf{x}^* = \arg\max_{\mathbf{x}} \mathrm{GJS}_\alpha\big[p_{\theta_1}(\mathbf{v}|\mathbf{x}), \dots, p_{\theta_K}(\mathbf{v}|\mathbf{x})\big] + \frac{\beta}{K} \sum_{i=1}^K \mathrm{JS}[\hat{p}(\mathbf{v}|\mathbf{x}) \| p_{\theta_i}(\mathbf{v}|\mathbf{x})]$$
   第一项最大化不同 LLM 价值分布的广义 Jensen-Shannon 散度，迫使问题能强烈区分模型立场；第二项作为解耦正则项，避免问题本身包含的价值观主导回答。在 EM 式迭代中，分别用响应得分 $S(\mathbf{y})$（Eq.2）和问题精炼得分 $S(\mathbf{x})$（Eq.3）近似此目标，驱动问题向高区分度方向演化，同时不牺牲合理性。人评结果表明，AdAEM 生成的问题将价值区分度相对人工问题**提升 52%**，且合理性提升 8.7%（Cohen's κ = 0.93）。

### 效果验证的因果证据

- **深层价值差异被释放**：在 AdAEM Bench-MFT 评估下，四款不同 LLM 的价值取向相关系数降至 **-0.169**，而传统 MFQ 和 ValueBench 均达约 0.56～0.6 的正相关；同时跨价值维度标准差从约 0.1 跃升至 0.212，表明 AdAEM 能可靠揭示基准无法区分的价值分歧（Table 15）。
- **因果效度成立**：可控价值启动实验显示，针对 GPT-5 注入特定道德基础时，目标维度得分出现**极端提升**（如 Sanctity 提升 224.05%），而对立维度显著下降（Table 16），证实评估反映的是模型真实的价值倾向。
- **稳健性检验**：不同模型集合（AdAEM-2）、不同问题子集（200/500/1000 题）以及互斥分半检验均证明生成问题的有效性和评估结果的鲁棒性（ICC = 0.816，Cronbach's α = 0.8991）。

本质上，AdAEM 将价值评估从一个"静态问卷调查"创新为一个**自适应信息发现过程**，使 benchmark 本身能够随 LLM 的价值边界自我扩展——这一定义性差异正是它与所有 baselines 的根本分界。

## 整体框架

![[assets/figures/papers/iclr26_0006_qNlTH4kYJZ_AdAEM_An_Adaptively_and_Automated_Extensible_Mea/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of AdAEM framework. The left part demonstrates the questiono refinement step to increase informativeness and the right depict the response generation step to elicit value difference*

AdAEM 将 LLM 的价值评估重新建模为一个**信息瓶颈问题**：在不依赖人工标注和模型微调的前提下，自适应地生成一组能够最大化暴露不同模型价值分歧的测试问题，并据此对模型进行量化分析。这一思路直接回应了现有静态基准"问题过于通用、区分度不足"的核心瓶颈——传统问卷（如 SVS、MFQ）倾向于捕捉不同模型共享的安全价值，难以揭示模型中因文化背景、开发时期不同而形成的深层价值差异。

框架由两个相互耦合的阶段构成：**基准问题集的迭代探索‑优化构建阶段**与**基于该问题集的价值提取与聚合阶段**。两者通过一个统一的信息论目标衔接：构建阶段追求生成问题 $\boldsymbol{x}$ 的**信息量最大化**，而评估阶段则利用这些高区分度问题获得更可靠的价值分布。

- **输入**：一组待评估的 LLM（可包含参与问题生成的"探测器"模型集 $\mathbb{P}_1$、$\mathbb{P}_2$ 以及最终被测模型），以及目标价值理论（如 Schwartz 十维基本价值或道德基础五维）。
- **输出**：每个 LLM 的价值取向向量（如 $\boldsymbol{v} \in [0,1]^{10}$）及其在群体中的相对排序，同时产出大规模、可扩展的测试问题集（AdAEM Bench）。

### 1. 基准问题集的构建

构建过程从少量封闭的通用社会话题出发，通过**探索‑优化双循环**逐步扩展为高区分度的争议性问题集合。整个周期的核心模块如下：

#### (1) 初始话题选择与拓展
从已有的价值相关数据集（Touche23‑ValueEval、ValueBench）中筛选通用话题描述，作为多臂老虎机（MAB）的臂（arm），并利用链式思考（Chain‑of‑Thought）将这些描述自动转换为初始问题。这一步仅提供启动种子，所有后续问题均由框架自主生成与精炼，无需人工再介入。

#### (2) 探索算法驱动的迭代优化
每一轮迭代中，MAB 基于当前各话题的估计奖励 $Q_i$ 和探索奖励 $\sqrt{2\ln B / C_i}$ 选择话题臂 $i^*$，在利用高分话题（exploit）与探索新话题（explore）之间动态平衡。选定话题后，进入一个 **EM 式交替优化**循环：

- **E 步（响应生成）**：固定当前问题 $\boldsymbol{x}^{t-1}$，为参与生成的每个 LLM $\theta_i$ 多次采样回答 $\boldsymbol{y}$，并根据得分 $S(\boldsymbol{y})$ 筛选最具区分度的回答。该得分综合了回答与模型自身价值的符合度、语义连贯性，以及与其他模型在价值趋向和语义上的差异性（公式 2）。
- **M 步（问题精炼）**：固定上一步选出的高区分度回答集合，通过反思‑再生成机制调整问题 $\boldsymbol{x}$，使得新问题与这些观点鲜明的回答保持上下文连贯，同时其他模型不宜给出相同回答或价值倾向。精炼目标由得分 $S(\boldsymbol{x})$ 引导（公式 3）。

整个 EM 循环的最终目标由公式 (1) 给出：

$$
\boldsymbol{x}^* = \arg\max_{\boldsymbol{x}} \; \mathrm{GJS}_\alpha\!\big[p_{\theta_1}(\boldsymbol{v}|\boldsymbol{x}),\dots,p_{\theta_K}(\boldsymbol{v}|\boldsymbol{x})\big] + \frac{\beta}{K}\sum_{i=1}^K \mathrm{JS}[\hat{p}(\boldsymbol{v}|\boldsymbol{x}) \| p_{\theta_i}(\boldsymbol{v}|\boldsymbol{x})].
$$

其中第一项（广义 Jensen‑Shannon 散度）鼓励不同 LLM 在给定问题下的价值分布尽可能可分（**区分度**），第二项通过 JS 散度正则化迫使问题自身价值观不主导模型回答（**解耦**）。通过交替执行 E、M 步，$S(\boldsymbol{x})$ 单调上升并收敛，问题的信息量持续增强。

#### (3) 话题拓展与问题集累积
当某个话题被 MAB 选中足够次数且 EM 收敛后，系统利用 LLM 生成新的子话题并扩充臂库，同时保留已生成的高分问题。全部迭代预算 $B$ 耗尽时，得到包含数万问题的 AdAEM Bench（默认设置下约 12,310 个问题）。该问题集语义覆盖远广于静态基准（Self‑BLEU 仅 13.42，语义相似度 0.44），且天然具有自适应扩展能力。

### 2. 基于问题集的价值提取与聚合

获得高质量问题集后，对任意一组待测 LLM 执行评估流程：

- **回答采样与价值分类**：用 AdAEM Bench 中每一个问题 $x$ 分别询问每个 LLM，获取回答 $y$，然后通过一个外部价值分类器 $p_\omega(\boldsymbol{v}|y)$ 将回答映射为二分价值向量（如体现某一价值即为 1，否则为 0）。
- **个体价值聚合**：对于每个 LLM，将从同一问题产生的多个采样回答的二分向量做**逻辑或（union）** 合并，得到该问题下的合成意见；再通过 TrueSkill 相对排名系统将所有问题上的意见聚合成一个可区分的全局价值向量，突出不同模型间的相对强弱而非绝对分数。
- **最终输出**：每个 LLM 在所有价值维度上的优先取向，以及在群体中的相对排序（例如 Schwartz 的十维轮廓或道德基础的 Care、Fairness 等五维）。此结果可直接用于模型间的横向对比或价值启动效应验证。

整个框架通过 **信息量最大化驱动的自适应生成 + 相对排名聚合**，在完全无监督（无手工标注、无微调）的条件下，比人工设计的静态基准更深刻地揭示了 LLM 之间不易觉察的价值分歧（如跨文化、跨时期带来的差异）。后续实验表明，即使在有限的样本量（200～1000 问）或较小的生成模型集合（AdAEM‑2）下，该框架仍能保持高度一致性与区分度。

## 核心模块与公式推导

AdAEM 将价值评估重新构造为信息瓶颈问题：通过交替优化问题与回答，自动生成能最大化不同 LLM 价值分布差异的测试问题。整体流程由四个核心模块构成，协同完成从话题探索到价值分析的全过程。

### 1. 初始话题选择与拓展
从已有的价值相关数据集（如 ValueEval、ValueBench）中筛选通用社会话题作为多臂老虎机（MAB）的"臂"。利用 LLM 的链式思考（Chain-of-Thought）将话题描述转换为初始问题，为后续优化提供起点。

### 2. 问题优化（EM 式迭代）
该模块是生成高区分度问题的核心。它将优化过程建模为期望最大化（EM）迭代：
- **E 步（响应生成）**：固定当前问题 $x^{t-1}$，为每个 LLM 采样一组回答，并根据得分 $S(\mathbf{y})$ 选择最优回答。
- **M 步（问题精炼）**：固定已采样的回答，通过最大化得分 $S(\mathbf{x})$ 来调整问题，使其更具区分度。
迭代持续至信息量得分收敛（收敛曲线见 Figure 18）。

### 3. 探索算法
采用基于置信上界（UCB）的多臂老虎机变体，在多个话题间自适应分配优化预算。该算法平衡了"利用"（优化已获高分的话题）与"探索"（通过 CoT 生成新话题），确保问题集既深入又广泛。

### 4. 价值分析与聚合
使用外部价值分类器（$p_\omega$）对每个回答输出二分价值向量，代表该回答是否体现某价值维度。随后通过两种机制聚合：
- **逻辑或合并（union）**：将同一 LLM 的多条回答的价值向量取并集，得到初始价值向量。
- **TrueSkill 排名系统**：将所有 LLM 的回答进行相对排名，生成最终可区分的价值分布。

### 关键公式
下面给出信息量优化目标及迭代得分的精确定义。

**整体优化目标** (Eq. 1)

$$
\mathbf{x}^* = \arg\max_{\mathbf{x}} \; \mathrm{GJS}_\alpha\big[p_{\theta_1}(\mathbf{v}|\mathbf{x}), \dots, p_{\theta_K}(\mathbf{v}|\mathbf{x})\big] + \frac{\beta}{K}\sum_{i=1}^K \mathrm{JS}\big[\hat{p}(\mathbf{v}|\mathbf{x}) \,\|\, p_{\theta_i}(\mathbf{v}|\mathbf{x})\big]
$$

- $\mathbf{x}^*$：最优问题。
- $\mathrm{GJS}_\alpha$：广义 Jensen‑Shannon 散度，衡量不同 LLM 在给定问题下价值分布的可分性（区分度）。
- $\mathrm{JS}$：Jensen‑Shannon 散度，用于解耦正则项，防止问题自身的价值倾向主导回答。
- $\hat{p}(\mathbf{v}|\mathbf{x})$：由所有模型平均得到的参考价值分布。
- $p_{\theta_i}(\mathbf{v}|\mathbf{x})$：第 $i$ 个 LLM 的条件价值分布。
- $\beta$：正则化系数（论文中设为 1）。

**响应生成得分** (Eq. 2)

$$
S(\mathbf{y}) = \sum_{i=1}^K p_{x^{t-1}}^i(\mathbf{y}|\mathbf{v}^i) \Big[ \log p_{x^{t-1}}^i(\mathbf{v}^i|\mathbf{y}) + \log p_{x^{t-1}}^i(\mathbf{y}) - \log p_{x^{t-1}}^M(\mathbf{v}^i|\mathbf{y}) - \log p_{x^{t-1}}^M(\mathbf{y}) \Big]
$$

- $\mathbf{y}$：候选回答。
- $p_{x^{t-1}}^i$：第 $i$ 个 LLM 在当前问题 $x^{t-1}$ 下的生成分布。
- $p_{x^{t-1}}^M$：参考模型（如更强的基座 LLM）的分布。
- 得分鼓励回答与自身价值相符（第一项）、语义连贯（第二项），同时与其他模型的价值及语义存在差异（第三、四项）。

**问题精炼得分** (Eq. 3)

$$
S(\mathbf{x}) = \sum_{i=1}^K \sum_{j=1}^N p_{x^{t-1}}^i(y_j^{i,t}|\mathbf{v}^i) \Big[ \log p_{\mathbf{x}}^i(y_j^{i,t}|\mathbf{v}^i) - \log p_{\mathbf{x}}^M(\mathbf{v}^i|y_j^{i,t}) - \log p_{\mathbf{x}}^M(y_j^{i,t}) \Big]
$$

- $\mathbf{x}$：调整中的问题。
- $y_j^{i,t}$：第 $i$ 个模型在迭代中采样的第 $j$ 条回答。
- $N$：每个模型采样的回答数（论文中 $N=1$）。
- 第一项确保新问题与已采纳回答在上下文上连贯；后两项保证其他模型不易给出相同回答或价值倾向，从而提升区分度。

**真实价值分布近似**
由于 LLM 内部价值不可直接观测，AdAEM 通过外部价值分析器近似：

$$
p_{\boldsymbol{\theta}_i}(\mathbf{v}) \approx \mathbb{E}_{\hat{p}(\mathbf{x})} \mathbb{E}_{p_{\boldsymbol{\theta}_i}(\mathbf{y}|\mathbf{x})}\big[p_{\boldsymbol{\omega}}(\mathbf{v}|\mathbf{y})\big]
$$

即在经验问题分布 $\hat{p}(\mathbf{x})$ 下，对模型采样回答利用分类器 $p_{\boldsymbol{\omega}}$ 得到价值向量的期望，作为该模型价值分布的估计。这一近似是整个优化链路的基础。

> 注意：上述公式中的所有概率（如 $p_x(\mathbf{y})$、$p_x(\mathbf{v}|\mathbf{y})$）在面向黑盒 LLM 时通过外部分类器或语义相似度进行近似，可能引入系统误差，但实验显示该近似仍能支撑有效的区分结果。

## 实验与分析

### 主结果

AdAEM 测试基准在揭示 LLM 价值差异上大幅优于静态问卷基准。在道德基础维度上，AdAEM **Bench-MFT** 下四个不同 LLM 的平均价值向量相关系数仅为 **-0.169**，远低于 MFQ 和 ValueBench 的 ~0.6 和 ~0.56（Table 15）。这意味着前者能暴露模型间根本性的负相关价值取向，而后者只能捕捉浅层的一致的安全偏好。同时，跨价值维度的平均标准差从约 0.1 跃升至 **0.212**，区分度提升接近一倍，证明 AdAEM 生成的问题能迫使模型进入差异化表达。


![[assets/figures/papers/iclr26_0006_qNlTH4kYJZ_AdAEM_An_Adaptively_and_Automated_Extensible_Mea/figures/035_Table_15.jpg]]
*Table 15: Evaluation results under MFQ, Value Bench, and AdAEM Bench-MFT*

控制实验进一步验证了评估效度。在 **GPT-5** 上通过价值启动，目标道德基础维度得分出现巨幅增长：**Sanctity** 提升 224.05%（30.19→97.83）、**Loyalty** 提升 81.77%、**Authority** 提升 71.30%；而对立维度得分则相应下降（Table 16）。类似趋势在 Schwartz 价值维度实验中同样重现（Table 12），表明 AdAEM 的测量结果确实反映了可操控的内在价值倾向，而非随机波动。


![[assets/figures/papers/iclr26_0006_qNlTH4kYJZ_AdAEM_An_Adaptively_and_Automated_Extensible_Mea/figures/036_Table_16.jpg]]
*Table 16: Controlled Experiment Results Across Moral Foundations on GPT-5*

### 消融与鲁棒性

**生成规模的影响**：仅使用 200、500 或 1000 个 AdAEM 生成问题与完整 12k 问题评估结果的相关系数依次上升，当问题量达到 1000 时各维度相关性均超过 0.8（Figure 21）。这说明即使在小样本下，AdAEM 仍能获得高度可靠的估计，且在相同数量问题上其信息量仍优于静态基准（详见 fairness 分析）。


![[assets/figures/papers/iclr26_0006_qNlTH4kYJZ_AdAEM_An_Adaptively_and_Automated_Extensible_Mea/figures/039_Figure_21.jpg]]
*Figure 21: Consistency between evaluation results of different question subsets and the full AdAEM Bench*

**参与者多样性的影响**：将生成阶段的 LLM 集合缩减为两模型（AdAEM-2），其生成问题的信息量仍高于初始问题，并且由此得到的评估结果与主设置（多模型参与）高度一致，组内相关系数 ICC 为 **0.816**，Pearson 相关系数为 **0.790**（Table 17, Section K.1）。这证明框架对参与者组合的依赖较弱，收益主要来自信息论优化目标，而非仅仅依赖模型多样化。

**子集稳定性**：将数据集随机划分为 5 个互斥子集分别评估，得到的 Cronbach's α 为 **0.8991**，变异系数 CV 为 0.2845（Section K.3）。这意味着不同问题子集得到的结果高度一致，评估不依赖于特定问题集合。

### 重要图表结论

- **Table 1（基准统计）**：AdAEM 问题数量达 12,310，显著超过 SVS（57）、ValueBench（40）和 ValueDCG（4,561）；其 Self-BLEU（13.42）和语义相似度（0.44）表明不会简单重复，且覆盖了更广泛的语义空间（Figure 3 的 t-SNE 可视化）。
- **Table 9（人工评估）**：与通用问题相比，AdAEM 生成的问题在价值区分度上提升 **52%**，在合理性上提升 8.7%，注释者间一致性 Cohen's κ = 0.93，显示其问题既合理又富有争议性。
- **Figure 18**：优化过程中信息量得分 $S(x)$ 随迭代轮次单调上升并收敛，直接验证了 EM 式优化目标（Eq. 1–3）的有效性。


![[assets/figures/papers/iclr26_0006_qNlTH4kYJZ_AdAEM_An_Adaptively_and_Automated_Extensible_Mea/figures/022_Table_9.jpg]]
*Table 9: Human Evaluation Results*

### 失败模式与限制

1. **理论框架受限**：当前仅验证 Schwartz 价值理论和道德基础理论，对其他更细粒度或文化特定框架（如 Hofstede 维度）的泛化能力仍未探索。
2. **近似误差**：在黑盒 LLM 场景下，多项概率（$p_x(y)$, $p_x(v|y)$）不得不依赖外部分类器或语义相似度代替，可能引入系统性偏差。当前分析采用二元价值判断，未处理连续或多极价值表达，这限制了测量精度。
3. **静态评估假设**：尽管方法强调自适应和可扩展，但本实验的预算 ($B=1500$) 和模型集合是固定的，尚未验证在模型动态更新环境下的稳定性，也未量化所有近似步骤对最终测量准确性的具体影响。

### 补充图表

![[assets/figures/papers/iclr26_0006_qNlTH4kYJZ_AdAEM_An_Adaptively_and_Automated_Extensible_Mea/figures/020_Table_7.jpg]]
*Table 7: AdAEM benchmark statistics. SVS: SVS Questionnaire; VB: Value Bench; DCG: ValueDCG; #q: # of questions; Avg.L.: average question length; SB: Self-BLEU; Sim: average semantic similarity*


## 方法谱系与知识库定位

AdAEM 处于**动态、自适应价值评估**的新交叉点——它同时区别于传统的静态心理问卷基准和近期的大规模动态生成基准。在现有支撑点上，SVS、MFQ、ValueBench 等本质上是固定问题集，用少量人工编写或问卷导出的题目捕捉 LLM 的价值倾向。这类基准的瓶颈在于**问题过于通用且易过时**，使得不同模型的安全/无害化等"浅层共享价值"难以被区分，评估结果的信息量低，无法揭示文化适应、偏见等方面的深层分歧（Figure 1 对此做了直观对比）。ValueDCG 虽然大规模合成判断性问题，但仍然依赖人工设计的议题模板，缺乏对模型内部价值边界的针对性探测和系统化的信息量保证。

AdAEM 的核心路径是将价值评估重新表述为一个**信息瓶颈下的自适应生成问题**。它不再使用静态测试项，而是通过探测来自不同文化、不同开发时期的多样化 LLM 的价值边界，以**上下文优化（in‑context optimization）**的方式自动生成并不断拓展争议性问题。这一转变解决了两大基底缺陷：

1. **测试问题生成方式的更新**：从"固定、合成问题"变为"多臂老虎机驱动的探索‑优化循环"。AdAEM 用初始的少量通用社会话题作为臂，在每个话题下交替进行响应生成和问题精炼，并利用 UCB 策略在利用高分话题与探索新话题之间分配计算预算。这一过程无需任何人工标注或模型微调，直接建立在参与者 LLM 本身的上下文学习能力之上。
2. **信息量保证机制的引入**：静态基准无法系统保证问题对价值差异的区分力。AdAEM 则显式最大化不同 LLM 价值分布之间的广义 Jensen‑Shannon 散度（GJS），同时加入解耦正则项以抑制问题自身价值观对回答的支配（Eq. (1)）。实验证据表明，这种信息论驱动的优化使生成问题的价值区分度较人工编写问题提升 52%（人类评估，Cohen's κ = 0.93），且在相同问题数量条件下，AdAEM 仍能产生更显著的价值差异：在 AdAEM Bench‑MFT 上，四个 LLM 的价值取向相关系数仅为 –0.169，远低于 MFQ（~0.6）和 ValueBench（~0.56）；跨价值维度的标准差达 0.212，约为其他基准的两倍（Table 15）。更进一步，受控价值启动实验显示，在 GPT‑5 上目标价值维度可提升逾 200%（如 Sanctity 从 30.19 升至 97.83），对立维度则相应下降，证实了该评估效度（Table 16）。

**适用边界与局限。**当前 AdAEM 的实现仅在 Schwartz 基本价值理论和 Moral Foundations Theory 两种框架下得到验证，对于更细粒度或文化特定的价值维度（如 Hofstede 维度）的可迁移性尚不明确。方法的多处近似——包括外部分类器估计 $p(\mathbf{v}|\mathbf{y})$、用语义相似度替代部分概率项——可能引入系统误差，尤其在对黑盒 LLM 的评估中难以量化。价值分析阶段默认采用二元判断（体现/未体现某价值），未能处理连续或多极的价值表达。此外，研究是在固定计算预算（$B=1500$）和固定参与者集合条件下进行的，在模型快速更替或需要实时更新的环境中，问题的持续有效性和评估一致性仍有待验证。大规模消融实验表明，即使减少参与者规模（AdAEM‑2）或仅使用 200 个问题，评估结果仍与全量基准高度一致（ICC = 0.816，Cronbach's α = 0.8991），但完全动态环境下的稳定性仍需另行确认。

**开放问题。**首先，AdAEM 能否无缝应用于 Schwartz 以外的理论框架，以及不同理论下的评估结果能否相互印证，是推动该方法走向一般化价值评估的关键。其次，在连续价值谱系（而非离散二分）中如何定义并优化信息量目标，将直接决定方法对真实价值表达的覆盖能力。第三，所有近似步骤（价值分类器、语义相似度替换等）对最终评估准确性的量化影响尚未测量，这为后续的误差分析和校准研究留下了空间。最后，当 LLM 参与者集合动态变化（新模型加入、旧模型退役）时，AdAEM 能否持续生成有效问题并维持评估的一致性，是面向实时治理和持续审计场景必须回答的问题。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/AdAEM_An_Adaptively_and_Automated_Extensible_Measurement_of_LLMs_Value_Difference.pdf

![[paperPDFs/ICLR_2026/AdAEM_An_Adaptively_and_Automated_Extensible_Measurement_of_LLMs_Value_Difference.pdf]]
