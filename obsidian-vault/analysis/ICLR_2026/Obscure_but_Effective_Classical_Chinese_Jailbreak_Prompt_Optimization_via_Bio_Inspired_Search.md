---
title: "Obscure but Effective: Classical Chinese Jailbreak Prompt Optimization via Bio-Inspired Search"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Obscure_but_Effective_Classical_Chinese_Jailbreak_Prompt_Optimization_via_Bio_Inspired_Search.pdf
openreview_forum_id: O7fxz7D6vf
aliases:
- CB
- OBECCJPOBIS
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "将越狱提示重定向至文言文语境，并将攻击策略分解为八个维度（角色身份、行为引导、机制、隐喻映射、表达风格、知识关系、上下文设置和触发模式），利用果蝇优化算法进行自动化搜索，系统性地探索高成功率策略。"
primary_logic: "文言文与安全对齐之间的“高能力‑低对齐”分布偏移：LLM对文言文保持了较强的理解能力，但缺乏对应的安全护栏，使得文言文成为攻击盲区，可绕过基于现代语言的过滤机制。"
claims:
- "文言文越狱成功率远高于英语和现代中文"
- "CC‑BOS在所有六款LLM上均达到100% ASR，最强基线ICRT仅80%左右"
- "维度消融显示移除Mechanism或Metaphor Mapping使ASR从100%骤降至82%，且查询成本激增"
- "果蝇优化算法（FOA）在ASR和查询效率上均优于遗传算法和随机搜索"
---

# Obscure but Effective: Classical Chinese Jailbreak Prompt Optimization via Bio-Inspired Search

> [!tip] 核心洞察
> 文言文与安全对齐之间的“高能力‑低对齐”分布偏移：LLM对文言文保持了较强的理解能力，但缺乏对应的安全护栏，使得文言文成为攻击盲区，可绕过基于现代语言的过滤机制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 晦涩但有效：基于生物启发式搜索的文言文越狱提示优化 |
| 英文题名 | Obscure but Effective: Classical Chinese Jailbreak Prompt Optimization via Bio-Inspired Search |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=O7fxz7D6vf) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | CC-BOS |
| Dataset | AdvBench |

> [!tip] 效果简介
> - AdvBench 上，ASR on GPT‑4o 为 100%，对比 74% (ICRT)，变化 +26%。
> - AdvBench 上，ASR on Claude‑3.7 为 100%，对比 40% (ICRT)，变化 +60%。
> - AdvBench 上，Avg Queries on Gemini‑2.5‑flash 为 1.46，对比 3.62 (CL‑GSO)，变化 -59.7%。

## 概述

现有大语言模型的安全对齐机制主要针对现代语言（如英语）进行优化，却忽视了文言文在训练语料中的广泛存在。文言文具有简洁凝练、语义多义、隐喻丰富的独特语言特性，这导致了一个关键的安全瓶颈：模型能够充分理解文言文中承载的有害意图，但其安全护栏却无法有效检测和阻止此类攻击。这一“高能力‑低对齐”的分布偏移，使文言文成为越狱攻击的天然盲区。

针对上述问题，本文提出 **CC-BOS**（Classical Chinese Bio‑inspired Optimization Search），一个自动生成文言文对抗提示的黑盒越狱框架。其核心设计包含三个关键创新：

1. **文言文语境重定向**：将越狱提示的生成语言从英语或现代汉语切换至文言文，利用模型在文言文理解与安全防护之间的能力断层。
2. **八维策略空间分解**：将攻击策略系统性地分解为角色身份、行为引导、机制、隐喻映射、表达风格、知识关系、上下文设置和触发模式八个维度，形成结构化的搜索空间 $\mathbb{S} = D_1 \times D_2 \times \cdots \times D_8$。
3. **生物启发式优化**：采用果蝇优化算法（Fruit Fly Optimization Algorithm），通过嗅觉搜索、视觉搜索和柯西变异算子实现策略组合的自动迭代优化，高效探索高成功率策略。

实验结果表明，CC-BOS 在 AdvBench 基准上对所有六款主流 LLM（包括 GPT‑4o、Claude‑3.7、Gemini‑2.5‑flash 等）均达到 **100%** 的攻击成功率，显著超越最强基线 ICRT（最高约 80%）。在查询效率方面，CC-BOS 的平均查询次数仅为 1.12–2.38 次，较 CL‑GSO 等基线降低约 60%。维度消融实验进一步揭示，移除 Mechanism 或 Metaphor Mapping 维度会使攻击成功率从 100% 骤降至 82%，且查询成本激增，印证了策略空间分解的关键作用。

综上，CC-BOS 揭示了文言文作为越狱攻击载体的严重风险，为 LLM 安全对齐的多语言覆盖问题提供了重要的警示与基准。

## 背景与动机

### 大语言模型安全对齐的隐性盲区

当前大语言模型（LLM）的安全对齐机制在设计上存在一个根本性的分布偏移：对齐训练和防护策略主要针对英语及现代高资源语言进行优化，而文言文（Classical Chinese）因其在训练语料中的独特存在，形成了一块“高能力‑低对齐”的攻击盲区。具体而言，LLM对文言文保持了较强的语义理解能力——能够准确解析其中隐含的有害意图——但安全护栏缺乏对文言文语境下越狱模式的识别与过滤能力。这一矛盾构成了本文的核心瓶颈：**安全对齐的语言覆盖缺口使得文言文成为系统性绕过防护的捷径**。

### 现有越狱方法的局限

近年来，自动化越狱攻击方法不断涌现。PAIR 和 TAP 分别采用迭代查询和树搜索策略生成对抗提示，GPTFUZZER 利用变异与选择机制进行黑盒攻击，AutoDAN-Turbo-R 和 CL-GSO 则引入优化框架提升攻击效率，ICRT 进一步通过认知启发式两阶段设计达到约 80% 的攻击成功率。然而，这些方法存在两个共同缺陷：

1. **语言环境单一**：所有攻击均在英语或现代中文语境下展开，未触及文言文这一安全防护薄弱的语言通道。
2. **策略空间碎片化**：攻击策略通常局限于角色扮演或单一语义变换，缺乏对越狱行为多维度特性的系统性建模。

### 本文动机与核心思路

针对上述缺口，本文提出 **CC-BOS（Classical Chinese Jailbreak Prompt Optimization via Bio-Inspired Search）**，其动机源于一个朴素而关键的观察：**将越狱提示重定向至文言文语境，可以系统性绕过基于现代语言的安全过滤机制**。为实现这一目标，CC-BOS 从三个层面重构了越狱攻击框架：

- **语言通道切换**：将提示生成从英语/现代中文迁移至文言文，利用其简洁性、多义性和隐喻丰富性掩盖有害意图。
- **策略空间系统化**：将攻击策略分解为八个维度——角色身份（Role Identity）、行为引导（Behavioral Guidance）、机制（Mechanism）、隐喻映射（Metaphor Mapping）、表达风格（Expression Style）、知识关系（Knowledge Relation）、上下文设置（Contextual Setting）和触发模式（Trigger Pattern）——构成笛卡尔积搜索空间 $\mathbb{S} = D_1 \times D_2 \times \cdots \times D_8$。
- **优化算法生物学启发性**：采用果蝇优化算法（Fruit Fly Optimization Algorithm, FOA），集成嗅觉搜索、视觉搜索和柯西变异算子，实现策略组合的自动迭代精炼。

实验证据表明，这一设计在 AdvBench 基准上使攻击成功率从最强基线 ICRT 的约 80% 跃升至 **100%**（Table 1），且在所有六款主流 LLM 上均达到饱和攻击效果。语言环境对比实验进一步验证了核心假设：文言文语境下的 ASR 达到 100%，而英语和现代中文分别仅为 82% 和 86%（Table 12），直接证实了文言文作为攻击通道的独特优势。

## 核心创新

CC‑BOS 的核心创新在于识别并利用了一个此前未被系统探索的安全盲区——**文言文与安全对齐之间的“高能力‑低对齐”分布偏移**。现有 LLM 的安全对齐主要针对现代语言（英语、现代汉语）优化，但文言文因在训练数据中天然存在，模型对其保持了较强的理解能力，却缺乏对应的安全护栏。这一偏移使得文言文成为攻击者绕开现代语言过滤机制的理想通道。Table 12 的对比实验直接验证了这一点：在 GPT‑4o 上，文言文越狱的 ASR 达到 100%，远高于英语的 82% 和现代汉语的 86%。

围绕这一瓶颈，CC‑BOS 引入了三个相互耦合的 **changed slots**，构成其相对于现有黑盒越狱方法的差异化优势：

**1. 提示语言语境：从现代语言重定向至文言文。**
现有方法（PAIR、TAP、CL‑GSO、ICRT 等）均在英语或现代汉语语境下优化对抗提示。CC‑BOS 将整个攻击流程重定向至文言文，利用其简洁、多义、隐喻丰富的语义特性，使有害意图在模型可理解的前提下绕过基于现代语言特征的安全检测。消融实验（Table 6）表明，仅将基础提示切换为文言文（Base），ASR 即可从接近零提升至 18%，验证了文言文语境本身具有攻击增益。

**2. 策略分解与搜索空间：从碎片化单策略到八维策略空间。**
现有方法通常依赖角色扮演或单一策略组合，搜索空间碎片化且覆盖不足。CC‑BOS 将越狱提示生成形式化为一个八维策略空间 $\mathbb{S} = D_1 \times D_2 \times \cdots \times D_8$，涵盖角色身份、行为引导、机制、隐喻映射、表达风格、知识关系、上下文设置和触发模式。这一结构化分解使得攻击策略的组合爆炸被显式建模，为后续优化算法提供了系统性的搜索基础。维度消融实验（Table 13）揭示了关键维度的因果作用：移除 Mechanism 或 Metaphor Mapping 维度后，ASR 从 100% 骤降至 82%，且平均查询次数从约 2.4 激增至 9 以上，说明这两个维度是维持高攻击效率的瓶颈组件。

**3. 优化算法：从遗传算法/随机搜索到生物启发式果蝇优化算法（FOA）。**
CL‑GSO 等基线使用遗传算法或随机搜索进行策略优化，存在收敛慢、易陷入局部最优的问题。CC‑BOS 采用受果蝇觅食行为启发的优化算法，集成嗅觉搜索（带衰减步长的局部索引扰动 $\Delta_t \gets \max(1, \lfloor \alpha \cdot |D_i| \cdot \gamma^t \rfloor)$）、视觉搜索（时变全局最优吸引概率 $\beta_t = \beta_0 + (1-\beta_0) \cdot \frac{t}{N}$）和柯西变异算子，在全局探索与局部利用之间实现动态平衡。Table 8 的直接对比显示，FOA 在 GPT‑4o 上达到 100% ASR 且平均查询次数仅 1.28，显著优于遗传算法（94% ASR，4.04 次查询）和随机搜索（90% ASR，6.10 次查询）。

三个 changed slots 之间存在强耦合：文言文语境提供了攻击盲区，八维策略空间将该盲区内的攻击可能性结构化，而 FOA 则以高查询效率在该空间中定位最优策略组合。消融实验（Table 6）的阶梯式结果——Base（18%）→ + Strategy（60%）→ + Bio‑Inspired Opt.（100%）——定量地证实了这一耦合递进关系。

## 整体框架

![[assets/figures/papers/iclr26_0011_O7fxz7D6vf_Obscure_but_Effective_Classical_Chinese_Jailbrea/figures/002_Figure_2.jpg]]
*Figure 2: Overall framework of CC-BOS. (Left) A multi-dimensional strategy space generates candidate jailbreak prompts across context, intent, style, and activation timing. (Right) Candidates are iteratively optimized via a bio-inspired search loop, evaluated by a two-stage keyword and semanticconsistency scorer, and guided by fitness signals toward high-performing strategies*

CC‑BOS 的整体 pipeline 由四个核心模块串联而成，形成“策略组合生成 → 迭代优化 → 响应评估 → 适应度反馈”的闭环，如图 2 所示。

### 输入与输出流

- **输入**：原始有害查询 $q_0$（英文）。
- **输出**：高成功率文言文越狱提示 $q^*$，以及目标模型的对抗响应。

### 模块关系

1. **多维度策略空间生成器（Multi‑Dimensional Strategy Space Generator）**  
   将越狱提示生成形式化为一个八维策略空间 $\mathbb{S} = D_1 \times D_2 \times \cdots \times D_8$，覆盖角色身份、行为引导、机制、隐喻映射、表达风格、知识关系、上下文设置和触发模式八个维度。对任意策略组合 $\mathbf{s} \in \mathbb{S}$，通过确定性映射 $q = G(q_0; \mathbf{s})$ 生成候选文言文对抗查询。

2. **生物启发式优化引擎（Bio‑Inspired Optimization Engine, FOA）**  
   以果蝇优化算法为核心，对策略组合进行迭代搜索。每轮迭代依次执行嗅觉搜索（局部索引扰动）、视觉搜索（向全局最优个体吸引）和柯西变异（停滞时触发），在八维离散空间中平衡探索与利用。种群初始化采用覆盖约束随机采样，并通过去重机制保证个体唯一性。

3. **两阶段翻译模块（Two‑Stage Translation Module）**  
   目标模型返回文言文响应后，先将响应译成现代汉语，再译成英语，得到标准化表示 $\tilde{r} = T(r)$。该设计旨在逐步消解文言文的隐喻丰富性和语义压缩，确保评估一致性。

4. **适应度评估器（Fitness Evaluator）**  
   对翻译后的响应计算适应度得分 $F(\mathbf{s}) = S_{\mathbf{c}}(\mathbf{s}) + S_{\mathbf{k}}(\mathbf{s}) \in [0, 120]$，其中 $S_{\mathbf{c}}$ 为语义一致性得分，$S_{\mathbf{k}}$ 为关键词拒绝检测得分（若命中拒绝关键词则得 0 分，否则得 20 分）。适应度信号反馈至优化引擎，指导下一轮搜索方向。

### 终止条件

搜索在种群最优适应度超过阈值 $\tau$ 或达到最大迭代次数 $N$ 时终止，返回对应的最优策略组合及生成的文言文越狱提示。

> **需注意**：图 2 为框架示意图，其左侧展示策略空间生成候选提示，右侧展示生物启发式搜索循环与评估反馈的交互关系。

## 核心模块与公式推导

### 八维策略空间的形式化

CC‑BOS 将越狱提示生成形式化为一个八维策略空间，每个维度对应一类攻击策略的可选集：

$$ \mathbb{S} = D_1 \times D_2 \times \cdots \times D_8 \tag{5} $$

其中八个维度分别为：**角色身份**（Role Identity）、**行为引导**（Behavioral Guidance）、**机制**（Mechanism）、**隐喻映射**（Metaphor Mapping）、**表达风格**（Expression Style）、**知识关系**（Knowledge Relation）、**上下文设置**（Contextual Setting）和**触发模式**（Trigger Pattern）。每个维度 $D_i$ 是一个离散的策略选项集合，一个具体的策略组合表示为 $\mathbf{s} = (s_1, \dots, s_8) \in \mathbb{S}$，其中 $s_k \in D_k$。

给定原始有害查询 $q_0$ 和策略组合 $\mathbf{s}$，提示生成器 $G$ 将其映射为文言文对抗提示 $q = G(q_0; \mathbf{s})$。优化目标是在策略空间中搜索最大化适应度函数的组合：

$$ \mathbf{s}^\star \in \arg\max_{\mathbf{s} \in \mathcal{S}} F(\mathbf{s}) \tag{4} $$

### 生物启发式优化算法（FOA）

优化采用基于果蝇觅食行为的生物启发式算法，包含三个核心算子：**嗅觉搜索**（smell search）、**视觉搜索**（vision search）和**柯西变异**（Cauchy mutation）。种群更新流程为：

$$ P_t' = \Phi_{\text{smell}}(P_t), \quad P_t'' = \Phi_{\text{vision}}(P_t', \mathbf{s}_{\text{best}}^t), \quad P_{t+1} = \Phi_{\text{cauchy}}(P_t'') $$

**嗅觉搜索**对种群中每个个体的每一维度执行局部随机扰动，步长随迭代衰减：

$$ idx(s_i^{(j)}) \gets idx(s_i^{(j)}) + \delta, \quad \delta \sim U(-\Delta_t, \Delta_t) \tag{10} $$

$$ \Delta_t \gets \max(1, \lfloor \alpha \cdot |D_i| \cdot \gamma^t \rfloor) $$

其中 $\alpha$ 为初始探索比例，$\gamma$ 为衰减因子（设为 0.95），$|D_i|$ 为第 $i$ 维度的选项数量。衰减步长使算法前期侧重全局探索，后期聚焦局部精化。

**视觉搜索**将个体以时变概率吸引至当前全局最优解 $\mathbf{s}_{\text{best}}^t$：

$$ \beta_t = \beta_0 + (1 - \beta_0) \cdot \frac{t}{N} \tag{12} $$

$\beta_t$ 从初始值 $\beta_0$ 线性增长至 1，使种群在迭代后期更倾向于向最优个体靠拢，平衡探索与利用。

**柯西变异**在种群陷入停滞（最优适应度连续未改善达到停滞阈值，设为 2 轮）时触发，对个体施加重尾扰动以增强跳出局部最优的能力，变异尺度设为 0.2。

### 适应度函数与两阶段翻译模块

适应度函数由语义一致性得分和关键词拒检得分相加构成：

$$ F(\mathbf{s}) = S_{\mathbf{c}}(\mathbf{s}) + S_{\mathbf{k}}(\mathbf{s}) \tag{17} $$

其中 $S_{\mathbf{c}}(\mathbf{s}) \in [0, 100]$ 衡量目标模型响应与有害意图的语义一致性，$S_{\mathbf{k}}(\mathbf{s})$ 为关键词得分：若响应 $\tilde{r}$ 包含拒绝关键词集合 $K^-$ 中的任何词，则 $S_{\mathbf{k}}(\mathbf{s}) = 0$；否则 $S_{\mathbf{k}}(\mathbf{s}) = 20$。搜索在最优适应度超过阈值 $\tau$ 或达到最大迭代次数 $N$ 时终止。

由于文言文的隐喻丰富性和语义压缩特性使直接评估困难，CC‑BOS 引入**两阶段翻译模块**：先将目标模型的文言文响应译成现代汉语，再译成英语，得到标准化表示 $\tilde{r} = T(r)$，确保评估的一致性和可比性。消融实验（Table 6）表明，移除翻译模块后 GPT‑4o 上的 ASR 从 100% 降至 90%，证实该模块对准确评估至关重要。

### 种群初始化与去重

种群初始化采用**覆盖约束随机采样**：对每个维度 $D_k$，先随机排列其选项，再从排列中循环采样 $N$ 个个体，保证各维度的选项在初始种群中均匀覆盖。生成个体后通过 **UniqGen 算法**进行去重：若新个体与已有个体相同，则重新采样（最多 $R$ 次尝试），避免冗余个体浪费查询预算。

## 实验与分析

### 核心瓶颈验证：文言文的“高能力–低对齐”分布偏移

CC‑BOS 的攻击有效性根植于一个被现有安全对齐忽略的事实：LLM 对文言文保持了与现代语言相当的理解能力，但安全护栏几乎完全缺失。Table 12 的语言环境对比直接验证了这一点——在相同攻击意图下，文言文 ASR 达到 100%，而英语仅 82%、现代汉语 86%。这一差距揭示了安全对齐的“语言盲区”：训练数据中残留的古典文本赋予了模型理解文言文的能力，但 RLHF 等对齐过程从未覆盖这一模态，导致有害内容可以畅通无阻。

![[assets/figures/papers/iclr26_0011_O7fxz7D6vf_Obscure_but_Effective_Classical_Chinese_Jailbrea/figures/017_Table_12.jpg]]
*Table 12: Attack Success Rate (ASR) comparison across different language contexts*

### 主实验结果：全模型 100% ASR 与查询效率优势

**AdvBench 主基准**（Table 1）：CC‑BOS 在全部六款目标 LLM 上均达到 100% ASR，而最强基线 ICRT 在同一批模型上的 ASR 分布在 40%–74% 之间。具体而言，Claude‑3.7 上 ICRT 仅 40%，CC‑BOS 提升 60 个百分点；GPT‑4o 上 ICRT 为 74%，CC‑BOS 提升 26 个百分点。其他基线方法（PAIR、TAP、GPTFUZZER、AutoDAN‑Turbo‑R、CL‑GSO）的 ASR 普遍在 10%–60% 区间，远低于 CC‑BOS。

![[assets/figures/papers/iclr26_0011_O7fxz7D6vf_Obscure_but_Effective_Classical_Chinese_Jailbrea/figures/003_Table_1.jpg]]
*Table 1: CC-BOS Evaluation on the AdvBench Benchmark and Comparison with Existing Baselines*

**跨数据集泛化**（Table 2）：在 CLAS 和 StrongREJECT 两个独立数据集上，CC‑BOS 的 ASR 维持在 98.30%–100%，而 ICRT 在 Claude‑3.7 上的 StrongREJECT ASR 仅 14%，差距达 86 个百分点。这表明 CC‑BOS 的攻击能力不依赖于特定有害查询分布，具有跨数据集的鲁棒性。

**查询效率**（Table 3）：CC‑BOS 在所有模型上的平均查询次数（Avg.Q）为 1.12–2.38，显著低于其他方法。以 Gemini‑2.5‑flash 为例，CC‑BOS 仅需 1.46 次查询，而 CL‑GSO 需要 3.62 次（降低 59.7%），PAIR 需要 17.80 次。低查询成本意味着攻击者在黑盒场景下可以更隐蔽、更快速地找到有效越狱提示。

### 防御鲁棒性：对抗 Llama‑Guard 与复合防御

Table 4 展示了 CC‑BOS 在 Llama‑Guard‑3‑8B 防御下的表现。无防御时，CC‑BOS 对所有攻击模型保持 100% ASR。当启用 Input & Output 双重过滤后，ASR 有所下降（Claude‑3.7 上降至 40%，Deepseek‑Reasoner 上 28%，Gemini‑2.5‑flash 上 22%），但仍显著高于 GPTFUZZER 和 ICRT 在同等防御下的 ASR（多数为 0%–10%）。这说明文言文越狱对基于现代语言的输出检测器具有天然的规避优势——即使翻译模块被防御方使用，文言文特有的隐喻压缩仍能部分绕过关键词匹配。

Table 10 进一步考察了动态防御（In‑Context Defense、Self‑Reminder）与复合防御（结合 Llama‑Guard）下的表现。CC‑BOS 在所有防御配置下均保持最高 ASR，例如在 ICD‑FewShot + Llama‑Guard 组合下仍达 56%，而 ICRT 和 GPTFUZZER 分别仅 12% 和 8%。这表明 CC‑BOS 的攻击策略组合对上下文防御和输出过滤均有一定抗性。

### 跨模型可迁移性

Table 5 的迁移矩阵显示，CC‑BOS 生成的对抗提示具有强跨模型迁移能力。以 GPT‑4o 为源模型生成的攻击样本，迁移到 Qwen3 时 ASR 高达 92%，迁移到 Grok‑3 为 88%。对角线（同模型攻击）均为 100%，非对角线 ASR 最低为 76%（Gemini‑2.5‑flash → DeepSeek‑Reasoner）。这一迁移性意味着攻击者无需针对每个目标模型重新优化，单次搜索即可威胁多款 LLM。

### 组件消融：三大模块的因果贡献

Table 6 的逐步消融清晰展示了 CC‑BOS 各组件的因果效应：

![[assets/figures/papers/iclr26_0011_O7fxz7D6vf_Obscure_but_Effective_Classical_Chinese_Jailbrea/figures/008_Table_6.jpg]]
*Table 6: Ablation study of the proposed method*

- **Base（仅文言文基础）**：ASR 仅 18%。说明单纯的文言文语境不足以稳定越狱，需要策略引导。
- **+ Strategy（加入八维策略空间）**：ASR 跃升至 60%。策略空间的引入使攻击从随机试探变为有结构的搜索，贡献了 42 个百分点的提升。
- **+ Bio‑Inspired Opt.（完整 CC‑BOS）**：ASR 达到 100%。生物启发式优化进一步贡献 40 个百分点，证明 FOA 在策略组合空间中的搜索效率远超随机或手动组合。
- **w/o Translated Module（移除翻译模块）**：ASR 从 100% 降至 90%。翻译模块的移除主要影响评估准确性，但也会间接影响优化过程中的适应度信号质量，导致搜索方向偏差。

### 维度消融：Mechanism 与 Metaphor Mapping 是关键瓶颈

Table 13 的维度归一消融（在 Claude‑3.7 上进行）揭示了八个策略维度的重要性差异：

![[assets/figures/papers/iclr26_0011_O7fxz7D6vf_Obscure_but_Effective_Classical_Chinese_Jailbrea/figures/018_Table_13.jpg]]
*Table 13: Dimension-wise ablation results of CC-BOS on Claude-3.7 under the classical Chinese setting. ASR denotes Attack Success Rate, and Avg.Q denotes the average number of queries*

- **移除 Mechanism 维度**：ASR 从 100% 骤降至 82%，Avg.Q 从 2.38 飙升至 9.08。Mechanism 维度定义了攻击的“实现路径”（如代码解释、角色扮演等），缺少它会迫使搜索在更受限的空间中进行，大幅增加查询成本。
- **移除 Metaphor Mapping 维度**：ASR 同样降至 82%，Avg.Q 升至 9.82。隐喻映射是文言文越狱的核心优势维度——它将有害意图包装为古典典故或比喻，直接利用了安全对齐对文言文隐喻的检测盲区。
- **移除 Behavioral Guidance 维度**：ASR 降至 92%，Avg.Q 升至 5.40。行为引导维度影响相对较小，但仍不可忽略。
- 其他维度（Role Identity、Expression Style 等）的移除对 ASR 影响在 2–8 个百分点范围内，说明这些维度起辅助增强作用。

### 优化算法对比：FOA 的搜索效率优势

Table 8 在 GPT‑4o 上对比了三种优化算法：果蝇优化算法（FOA）达到 100% ASR 且仅需 1.28 次平均查询；遗传算法（GA）ASR 为 94%，平均查询 4.04 次；随机搜索 ASR 为 90%，平均查询 6.10 次。FOA 的优势来源于其嗅觉搜索（局部扰动）+ 视觉搜索（全局最优吸引）+ 柯西变异（跳出局部最优）的三阶段设计，在离散组合空间中实现了高效的探索–利用平衡。

![[assets/figures/papers/iclr26_0011_O7fxz7D6vf_Obscure_but_Effective_Classical_Chinese_Jailbrea/figures/013_Table_8.jpg]]
*Table 8: Performance comparison of different optimization algorithms on AdvBench against GPT-4o. The number in bold indicates the best jailbreak performance*

### 攻击模型选择的影响

Table 7 显示，使用不同 LLM 作为攻击模型（即生成对抗提示的模型）对 CC‑BOS 的最终 ASR 影响有限。Deepseek‑Chat、GPT‑3.5‑Turbo 和 Gemini‑2.0‑Flash 作为攻击模型时，CC‑BOS 在多数目标模型上仍保持 98%–100% ASR。这说明 CC‑BOS 的框架对攻击模型的选择具有鲁棒性，不依赖特定模型的生成能力。

### 失败模式与局限性

尽管 CC‑BOS 在主实验中表现近乎完美，但以下情况需要手动验证或存在不确定性：

1. **强输入输出双重过滤下的残留 ASR**：Table 4 中 Claude‑3.7 在 Input & Output 防御下仍保持 40% ASR，但论文未详细分析这些成功案例的具体特征，无法确定是防御的漏洞还是文言文特有的绕过机制。
2. **翻译增强防御的评估**：Table 9 提出了 Translation Enhanced Output Defense，但该防御的实验设置和结果细节在提供的材料中不完整，需要查阅原文确认其实际有效性。
3. **多轮对话与代理场景**：所有实验均在单轮对话设定下进行，CC‑BOS 在多轮交互或工具调用场景中的有效性尚未验证。
4. **安全对齐更新的适应性**：当目标模型针对文言文进行专门的安全微调后，CC‑BOS 的八维策略空间和 FOA 搜索是否仍能保持高 ASR，属于开放问题。

## 方法谱系与知识库定位

### 与现有越狱方法的谱系关系

CC-BOS 在攻击策略、搜索机制和语言语境三个维度上与现有方法形成系统性差异。图 1 通过方法对比图直观展示了这一谱系分化：传统方法（PAIR、TAP、GPTFUZZER、AutoDAN-Turbo-R、CL-GSO、ICRT）均在英语或现代中文语境下进行攻击优化，而 CC-BOS 将攻击重定向至文言文语境，并构建了一个八维策略搜索空间。

在攻击策略层面，CC-BOS 将越狱提示生成形式化为一个八维策略空间 $\mathbb{S} = D_1 \times D_2 \times \cdots \times D_8$，涵盖角色身份（Role Identity）、行为引导（Behavioral Guidance）、机制（Mechanism）、隐喻映射（Metaphor Mapping）、表达风格（Expression Style）、知识关系（Knowledge Relation）、上下文设置（Contextual Setting）和触发模式（Trigger Pattern）。这与基线方法的策略粒度形成鲜明对比：PAIR 和 TAP 依赖迭代查询进行策略探索，但缺乏显式的策略维度分解；GPTFUZZER 采用变异和选择策略，但搜索空间未结构化；CL-GSO 虽引入了策略分解，但仅覆盖部分维度组合；ICRT 采用认知启发式的两阶段方法，但策略空间仍受限于现代语言框架。CC-BOS 将攻击策略从单一或碎片化组合提升为系统性的八维笛卡尔积空间，使策略探索的覆盖度和组合灵活性大幅提升。

在搜索机制层面，CC-BOS 采用基于果蝇觅食行为的生物启发式优化算法（FOA），集成了嗅觉搜索（smell search）、视觉搜索（vision search）和柯西变异（Cauchy mutation）三个算子。嗅觉搜索通过带衰减步长的局部索引扰动 $\delta \sim U(-\Delta_t, \Delta_t)$ 实现局部探索，视觉搜索通过时变吸引概率 $\beta_t = \beta_0 + (1-\beta_0) \cdot t/N$ 向全局最优解靠拢，柯西变异则在种群停滞时注入长尾扰动以跳出局部最优。这一设计在探索-利用平衡上优于基线方法：遗传算法（GA）和随机搜索在相同条件下仅分别达到 94% 和 90% 的 ASR，且平均查询次数分别为 4.04 和 6.10，而 FOA 以 1.28 次查询即达到 100% ASR（Table 8）。FOA 的种群初始化采用覆盖约束随机采样（coverage-constrained random sampling）确保维度均匀覆盖，并通过 UniqGen 去重算法避免冗余个体，这些机制设计进一步提升了搜索效率。

### 适用边界与关键依赖

CC-BOS 的高效性建立在三个关键依赖之上，这些依赖同时界定了其适用边界。

**文言文的“高能力-低对齐”分布偏移**是攻击成功的根本前提。Table 12 显示，在 GPT-4o 上，文言文语境下的 ASR 达 100%，而英语和现代中文分别为 82% 和 86%。这一差异源于 LLM 安全对齐的训练数据偏向现代语言，而文言文在预训练语料中的存在使模型保持了较强的语义理解能力，却缺乏对应的安全护栏。当这一偏移被修复（例如通过针对文言文的安全微调），CC-BOS 的攻击效能可能显著下降。Table 11 进一步表明，这一攻击向量对拉丁语和梵语等古典语言同样有效，暗示该漏洞具有跨古典语言的通用性。

**八维策略空间的完整性**是攻击效能的另一关键依赖。维度消融实验（Table 13）揭示了各维度的贡献差异：移除 Mechanism 维度使 ASR 从 100% 骤降至 82%，平均查询次数从 2.38 飙升至 9.08；移除 Metaphor Mapping 维度产生几乎相同的影响（ASR 82%，Avg.Q 9.82）；移除 Behavioral Guidance 维度使 ASR 降至 92%，Avg.Q 升至 5.40。这表明 Mechanism 和 Metaphor Mapping 是攻击成功的瓶颈维度，它们分别负责构建有害行为的执行逻辑和利用文言文的隐喻特性绕过语义过滤。在攻击策略设计中，这两个维度的缺失将导致攻击效能的断崖式下降。

**两阶段翻译模块**对评估一致性至关重要，但对攻击生成本身并非必需。消融实验（Table 6）显示，移除翻译模块后 ASR 从 100% 降至 90%，这主要是因为翻译模块将文言文的隐喻丰富性和语义压缩逐步缓解，使评估器能准确判断响应是否真正包含有害内容。翻译模块的公式化表示为 $\tilde{r} = T(r)$，其两阶段设计（先译为现代汉语再译为英语）是应对文言文多义性和隐喻密度的工程化折中。在不需要精确评估的场景下，该模块可被简化或省略。

### 开放问题与未来方向

CC-BOS 的发现引发了一系列待探索的问题。

**跨语言攻击的泛化边界**尚未被充分刻画。虽然 Table 11 验证了拉丁语和梵语的有效性，但攻击成功率是否依赖于目标语言与模型训练数据的共现关系、语言的形态学特性（如屈折度、语序灵活性）以及文化隐喻的丰富程度，仍需系统研究。低资源古典语言（如古埃及语、苏美尔语）因训练数据极度稀疏，可能不满足“高能力”前提。

**防御机制的针对性设计**是一个紧迫的开放问题。Table 4 显示，Llama-Guard-3-8B 的输入输出联合防御可将 CC-BOS 的 ASR 压低至 22%-40%，但仍未完全消除威胁。Table 9 和 Table 10 分别探索了翻译增强防御和动态复合防御策略，但这些防御的泛化性和对正常文言文理解能力的损伤尚未评估。能否设计出专门针对文言文越狱的鲁棒防御机制，同时不影响模型对文言文的正常理解和生成能力，是安全对齐研究的一个新方向。

**安全对齐更新后的攻击鲁棒性**需要持续跟踪。当目标模型针对文言文攻击进行安全微调后，CC-BOS 的关键组件（尤其是 Mechanism 和 Metaphor Mapping 维度）是否仍能保持高攻击成功率，还是会被针对性防御瓦解，目前缺乏实验证据。这一问题的答案将决定 CC-BOS 是一个可被快速修补的漏洞，还是一个需要架构级防御的深层脆弱性。

**多轮对话与代理场景的扩展**是方法实用性的试金石。CC-BOS 当前在单轮越狱场景中表现出色，但在多轮对话或代理场景中，搜索效率和攻击有效性可能因上下文累积、目标模型的状态跟踪能力增强而下降。Table 5 的跨模型迁移性结果（GPT-4o 生成的攻击示例在 Qwen3 上达 92% ASR）暗示攻击策略具有模型无关的语义特性，但多轮场景下的策略退化速率和重搜索成本尚未被测量。

**攻击模型选择的影响**值得注意。Table 7 显示不同攻击模型（Deepseek-Chat、GPT-3.5-Turbo、Gemini-2.0-Flash）对 CC-BOS 的性能有影响，这意味着攻击效能部分依赖于攻击模型自身的文言文生成质量和对策略空间的理解能力。这一依赖关系在攻击模型能力进一步提升或下降时的变化趋势，是理解攻击可扩展性的关键。

## 原文 PDF

![[paperPDFs/ICLR_2026/Obscure_but_Effective_Classical_Chinese_Jailbreak_Prompt_Optimization_via_Bio_Inspired_Search.pdf]]
