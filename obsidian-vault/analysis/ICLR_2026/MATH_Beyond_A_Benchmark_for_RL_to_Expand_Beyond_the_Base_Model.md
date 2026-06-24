---
title: "MATH-Beyond: A Benchmark for RL to Expand Beyond the Base Model"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/MATH_Beyond_A_Benchmark_for_RL_to_Expand_Beyond_the_Base_Model.pdf
openreview_forum_id: RNkErKpCAp
aliases:
- MBBMB
- MATH-Beyond
tags:
- ICLR_2026
- topic/benchmarks_datasets_evaluation
- topic/benchmarks_datasets_evaluation/benchmark_eval
core_operator: "故意构建基模型在高采样预算下无法解决的“零基线”基准，迫使任何性能提升均源于推理边界的真实拓展，而非采样放大已有能力。"
primary_logic: "衡量RL是否真正拓展推理边界，需要使用基模型完全无法解决的困难问题构成“零基线”基准，使得所有成功都代表实质性的新能力获取。"
claims:
- "Nemotron-Research-Reasoning-Qwen-1.5B和DeepScaleR-1.5B-Preview等RL微调模型在MATH-B上pass@1024表现很差。"
- "Qwen2.5-7B在MATH-B上的pass@1024近乎为零，而AIME24上约77%。"
- "RL微调模型扩展率仅为5.22%~21.2%，而SFT/蒸馏模型可达58.93%~66.38%。"
- "随着采样预算k增加，新增解决问题的能力边际递减，扩展率趋于平台。"
---

# MATH-Beyond: A Benchmark for RL to Expand Beyond the Base Model

> [!tip] 核心洞察
> 衡量RL是否真正拓展推理边界，需要使用基模型完全无法解决的困难问题构成“零基线”基准，使得所有成功都代表实质性的新能力获取。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | MATH-Beyond：超越基模型的强化学习基准 |
| 英文题名 | MATH-Beyond: A Benchmark for RL to Expand Beyond the Base Model |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=RNkErKpCAp); [Project](https://huggingface.co/datasets/brendel-group/MATH-Beyond) |
| Topic | #topic/benchmarks_datasets_evaluation #topic/benchmarks_datasets_evaluation/benchmark_eval |
| Method | MATH-Beyond Benchmark (MATH-B) |
| Dataset | MATH-B-U, MATH-B vs AIME24 |

> [!tip] 效果简介
> - MATH-B-U 上，Expansion Rate (%, pass@1024) 为 Qwen3-8B (SFT/Distillation) 66.38，对比 Base model (pass@1024 ≈ 0)，变化 +66.38。
> - MATH-B-U 上，Expansion Rate (%, pass@1024) 为 Skywork-OR1-7B (RL) 21.2，对比 Base model (pass@1024 ≈ 0)，变化 +21.2。
> - MATH-B-U 上，Expansion Rate (%, pass@1024) 为 DeepScaleR-1.5B (RL) 5.22，对比 Base model (pass@1024 ≈ 0)，变化 +5.22。

## 概述

当前主流数学推理基准（如MATH-500、AIME 2024）存在一个根本性缺陷：基模型凭借高采样预算（pass@1024）即可解决其中绝大多数问题。这一现象使得强化学习（RL）微调仅能锐化模型已有的求解模式，而无法激发真正的探索与技能获取，背离了RL探索性学习的初衷。

针对这一瓶颈，本文提出 **MATH-Beyond (MATH-B)** 基准，其核心设计原则是构建一个“零基线”：即基模型在高采样预算下完全无法解决的问题集合。在此设定下，任何性能提升都必然源于推理边界的真实拓展，而非采样放大已有能力。衡量这一拓展的核心指标是 **扩展率（Expansion Rate）**，定义为基模型未能解决而微调策略成功解决的题目占比。

MATH-B的构建采用多阶段过滤流水线：从DAPO-Math-17K和DeepScaleR中获取53,682道高难度候选题目，经质量过滤、预筛选、前沿模型真值验证、去重，最终通过11款基模型和9款补充模型的pass@1024筛选，保留基模型无法解决的181道题目构成MATH-B-U（并集），以及41道所有基模型均无法解决的MATH-B-I（交集）。

主要实验结果揭示了RL微调的显著局限：

- **RL微调模型拓展有限**：基于GRPO/PRIME的RL后训练模型扩展率仅为5.22%~21.2%，而SFT/蒸馏模型可达58.93%~66.38%。
- **零基线有效性验证**：Qwen2.5-7B在MATH-B上pass@1024近乎为零，而在AIME24上约77%，证实了基准的“零基线”特性。
- **边际收益递减**：随着采样预算k增加，新增解决问题的能力呈现边际递减，扩展率在k=1024时趋于平台。

这些结果表明，当前RL方法在无教师模型指导下，难以自主探索有效推理路径，真正的探索性学习仍是开放挑战。

## 背景与动机

### 现有基准的“天花板”困境

当前主流数学推理基准（如 MATH-500、AIME 2024）在评估强化学习（RL）后训练模型时面临一个根本性问题：**基模型凭借大量采样即可解决几乎所有问题**。以 Qwen2.5-7B 为例，其在 AIME24 上的 pass@1024 约为 77%，而 RL 微调模型在这些基准上的提升本质上只是对已有求解模式的“锐化”，并非真正拓展推理边界。这使得 RL 的探索性学习目标——发现新技能、突破原有能力边界——在现有评估框架下无法被有效测量。

### 核心瓶颈：采样放大 vs. 真实拓展

问题的症结在于：当基模型在高采样预算下已能覆盖绝大部分题目时，任何后训练方法的性能增益都可能只是**采样放大了基模型已有的隐式能力**，而非获得了实质性新技能。这一混淆使得研究者无法区分 RL 微调究竟是在“探索未知”还是在“挖掘已知”。因此，衡量 RL 是否真正拓展推理边界，需要一个基模型完全无法解决的“零基线”基准——所有成功都代表实质性的新能力获取。

### 现有评估框架的验证漏洞

除基准难度不足外，现有基于规则的数学答案验证框架普遍存在解析失败问题。Table 1 系统记录了七类常见失败模式（F1–F7），包括仅读取第一个或最后一个 `\boxed{}` 答案、依赖特定文本锚点（如 “Answer:”）、对答案顺序敏感等。Table 3 的对比分析表明，TRL、VERL、LightEval、LM-Eval 等八个主流评估框架均存在不同程度的漏洞，尚无框架能完全覆盖所有失败模式。这些验证缺陷可能导致对模型能力的系统性误判。

### MATH-Beyond 的定位

针对上述缺口，MATH-Beyond（MATH-B）被设计为一个**零基线基准**：通过多阶段筛选流水线，从 DAPO-Math-17K 和 DeepScaleR 的 53,682 个高难度候选题中，构建出基模型在 pass@1024 下近乎无法解决的题目集合。其核心度量指标**扩展率（Expansion Rate）**定义为基模型 $q$ 未能解决而策略 $\pi$ 成功解决的题目占比：

$$\mathbf{Expansion Rate} = \frac{|\mathcal{E}_k|}{|D|}$$

在零基线设定下（$\mathcal{R}_k(q, D) = \varnothing$），扩展率等价于策略 $\pi$ 的 pass@k，从而使得任何非零性能提升都直接反映推理边界的真实拓展，排除了采样放大已有能力的干扰。

## 核心创新

### 问题瓶颈：现有基准无法衡量RL的真实拓展

当前常用数学推理基准（如MATH-500、AIME 2024）存在一个根本性缺陷：基模型（base model）仅凭大量采样（pass@1024）即可解决几乎所有问题。例如，Qwen2.5-7B在AIME24上的pass@1024可达约77%，但在MATH-B上几乎为零（Figure 1右）。这意味着，在这些基准上观察到的RL微调性能提升，很可能只是对已有求解模式的“锐化”，而非真正的探索与新技能获取——这背离了RL探索性学习的核心目标。

### 因果开关：零基线基准设计

MATH-Beyond的核心创新在于**故意构建一个基模型在高采样预算下完全无法解决的“零基线”基准**。具体而言，该基准通过多阶段筛选，确保基模型在pass@1024下对基准中所有问题的解决率趋近于零。这一设计切断了“采样放大已有能力”的捷径，迫使任何性能提升都必须源于推理边界的真实拓展。

### 关键指标：扩展率

为量化这一拓展，论文提出**扩展率**作为核心评估指标：

$$\mathbf{Expansion Rate} = \frac{|\mathcal{E}_k|}{|D|}$$

其中 $\mathcal{E}_k$ 是基模型 $q$ 未能解决、而策略 $\pi$ 在 $k$ 次采样中成功解决的问题集合。由于基准本身是零基线（$\mathcal{R}_k(q, D) = \emptyset$），扩展率直接等于策略的pass@k，但语义上更精确地捕捉了“新能力获取”的含义。与之配套的**收缩率**和**保留率**则分别衡量遗忘和已有能力的保持。

### 构建流程的关键变更

相比标准基准构建，MATH-Beyond在以下环节进行了系统性创新：

| 变更维度 | 基线做法 | MATH-Beyond做法 |
|---------|---------|----------------|
| **题目筛选** | 标准基准（MATH-500、AIME24等），基模型高采样预算可解 | 从DAPO-Math-17K和DeepScaleR中筛选，经质量过滤和pass@1024测试，确保基模型无法解决 |
| **验证机制** | 基于规则的验证，易受7类解析失败影响（Table 1） | 规避7类失败模式的鲁棒验证，额外使用前沿模型（o4-mini-high、GPT-5-Mini）验证真值答案 |
| **评估指标** | 普通基准上的pass@1或pass@k | 零基线基准上的扩展率，仅计基模型原本无法解决的问题 |
| **过滤流水线** | 无系统过滤 | 多阶段流水线：题型过滤→预筛选（pass@16）→前沿模型验证→去重→11款基模型+9款补充模型的pass@1024最终筛选 |

### 验证框架的强化

现有基于规则的数学答案验证存在7类常见失败模式（Table 1），包括仅读取第一个/最后一个boxed答案、依赖特定文本锚点（如"Answer:"）、顺序敏感等。MATH-Beyond的验证框架明确规避这些模式，并通过前沿模型交叉验证确保真值答案的正确性。Table 3显示，当前主流评估框架（TRL、VERL、LM-Eval等）对这7类失败模式的覆盖均不完整，尚无框架能完全免疫所有漏洞。

### 实验揭示的核心发现

在MATH-B-U（并集，181题）上，RL微调模型的扩展率仅为5.22%~21.2%，而SFT/蒸馏模型可达58.93%~66.38%（Table 2）。这一巨大差距揭示了当前RL方法的根本瓶颈：**在没有教师模型指导的情况下，RL的探索过程难以自主发现有效的推理路径**。扩展率随采样预算增加呈对数线性增长，但边际收益递减，在k=1024时趋于平台（Figure 5, Figure 7），表明单纯增加采样无法弥补探索能力的不足。

## 整体框架

![[assets/figures/papers/iclr26_0010_RNkErKpCAp_MATH-Beyond_A_Benchmark_for_RL_to_Expand_Beyond/figures/002_Figure_1.jpg]]
*Figure 1: MATH-Beyond: Benchmark Construction and Difficulty. Left: Schematic of the MATH-B creation process. A large set of problems from DAPO-Math-17K and DeepScaleR is first refined through quality filters to ensure answer correctness and verifiability. This is followed by evaluation against a gauntlet of open-source base models (≤ 8B, e.g., Qwen3, Qwen2.5 (-Math), DeepSeek-R1-Distill) at a pass@1024 budget to isolate problems that lie beyond their limits. The filtering yields the MATH-B suite of benchmarks: a 41-problem intersection set (unsolved by all base models) for evaluating universal difficulty, and a larger 181-problem union set (unsolved by at least one model) with model-specific splits...*

![[assets/figures/papers/iclr26_0010_RNkErKpCAp_MATH-Beyond_A_Benchmark_for_RL_to_Expand_Beyond/figures/003_Table_1.jpg]]
*Table 1: Common failure modes in rule-based math answer verification. These failures often stem from rigid heuristics, such as reading only the first or last boxed answer, requiring specific text anchors (e.g., "Answer:"), or other parsing failures. Each row shows the ground truth (GT), a model snippet, and the resulting verifier error*

![[assets/figures/papers/iclr26_0010_RNkErKpCAp_MATH-Beyond_A_Benchmark_for_RL_to_Expand_Beyond/figures/009_Table_3.jpg]]

MATH-Beyond 的核心思路是构建一个“零基线”基准，迫使模型在高采样预算下也无法依赖基模型已有能力，从而衡量 RL 是否真正拓展了推理边界。整个框架围绕三个关键环节展开：问题筛选流水线、鲁棒验证机制和扩展率评价体系。

### 问题筛选流水线

基准构建采用多阶段过滤流水线（Figure 1 左），从 DAPO-Math-17K 和 DeepScaleR 两个高难度数据源获取 53,682 道候选题目，逐步剔除易解、歧义和重复问题，最终形成基模型在 pass@1024 下无法解决的题目集。

流水线的模块串联关系如下：

1. **题型过滤**：移除多选题、含中文题、引用图片题、非整数答案题等，保留整数值真值的题目以减少验证歧义。
2. **预筛选**：使用 DeepSeek-R1-Distill-Qwen2.5-7B 以 pass@16 排除可解题目，随机采样缩减规模。
3. **真值验证**：调用前沿模型 o4-mini-high 和 GPT-5-Mini 以 pass@2 验证真值答案的正确性，仅保留至少一个前沿模型能复现真值的题目。
4. **去重**：与 MATH-500、MinervaMath、OlympiadBench、AMC23、AIME-2024、AIME-2025 等标准基准进行精确字符串匹配去重。
5. **pass@1024 终筛**：对候选题目在 11 款基模型（如 Qwen2.5-1.5B/7B、OLMo-7B、Llama-3.1-8B 等）和 9 款补充模型上各生成 1024 个样本，筛选出至少一个模型未能解决的问题。
6. **组装**：形成 181 题的 MATH-B-U（并集）和 41 题的 MATH-B-I（基模型交集），以及各模型专属子集。

### 鲁棒验证机制

标准基于规则的数学答案验证存在 7 类常见失败模式（Table 1），包括仅读取第一个/最后一个 boxed 答案、依赖特定文本锚点（如 “Answer:”）、忽略多答案场景等。现有评估框架（TRL、VERL、LM-Eval、LightEval 等）对这些失败模式的覆盖程度不一，尚无框架能完全规避所有漏洞（Table 3）。MATH-Beyond 通过保留整数值真值、使用前沿模型交叉验证答案正确性，从设计上规避了大部分解析失败。

### 扩展率评价体系

评价的核心指标是**扩展率**（Expansion Rate），定义为基模型 q 未能解决而策略 π 解决的题目占比：

$$\mathbf{Expansion Rate} = \frac{|\mathcal{E}_k|}{|D|}$$

其中 $\mathcal{E}_k$ 是 π 在 k 次采样中成功而 q 失败的题目集合。在零基线设定下，基模型 q 的 pass@1024 ≈ 0，因此扩展率直接反映推理边界的真实拓展。

配套指标还包括：
- **收缩率**（Shrinkage Rate）：q 能解而 π 失败的题目占比，反映遗忘。
- **保留率**（Preservation Rate）：q 已解题目中 π 仍保留的比例。
- **巩固度**（Consolidation）：保留题目中可被 π 在 pass@1 稳定解决的比例。

### 输入输出流

**输入**：DAPO-Math-17K 和 DeepScaleR 的 53,682 道高难度数学题，经流水线处理后输出 181 道（MATH-B-U）或 41 道（MATH-B-I）零基线题目。每道题附带真值答案、领域标签和难度评级。

**输出**：对待评估模型在 MATH-B 上以 pass@k（通常 k=1024）采样，计算扩展率、收缩率、保留率和巩固度，形成模型推理边界拓展的量化画像。k=1024 被选为原则性折衷——足够大以推动模型超出舒适区，同时在计算上可行且稳定（Figure 5、Figure 6 显示扩展率和 pass@k 在 k 接近 1024 时趋于平台）。

Figure 1 右侧直观展示了 MATH-B 与 AIME24 的难度鸿沟：Qwen2.5-7B 在 AIME24 上 pass@1024 约 77%，而在 MATH-B 上近乎为零，验证了零基线设计的有效性。

## 核心模块与公式推导

### 评估框架的核心公式

MATH-Beyond 的评估体系建立在三个递进的数学定义之上。首先，对于策略 $p$ 在单题 $x$ 上的 $k$ 次采样，成功指示器定义为：

$$\mathsf{pass@k}(p; x) = \begin{cases} 1 & \text{if } \exists i \in \{1,\ldots,k\} \text{ such that } y_i \in \mathcal{C}(x), \\ 0 & \text{otherwise.} \end{cases}$$

其中 $y_i$ 为第 $i$ 次采样的输出，$\mathcal{C}(x)$ 为题目 $x$ 的正确答案集合。在数据集 $D$ 上的平均成功率为：

$$\mathtt{pass@k}(p) = \frac{1}{|D|} \sum_{x \in D} \mathtt{pass@k}(p; x)$$

### 拓展率：衡量推理边界扩张的核心指标

设基模型为 $q$，后训练策略为 $\pi$。令 $\mathcal{E}_k$ 为基模型 $q$ 在 $k$ 次采样下未能解决、但策略 $\pi$ 成功解决的题目集合。拓展率（Expansion Rate）定义为：

$$\mathbf{Expansion Rate} = \frac{|\mathcal{E}_k|}{|D|}$$

该指标直接量化了后训练带来的推理边界扩张——在零基线设定下，基模型的 $\mathtt{pass@k}(q) \approx 0$，因此拓展率近似等于 $\pi$ 的绝对表现，所有成功都代表新能力的获取。

### 辅助指标：遗忘与巩固

为全面刻画后训练效果，框架还引入三个辅助指标。收缩率（Shrinkage Rate）衡量基模型已解决而 $\pi$ 失败的题目比例：

$$\mathrm{Shrinkage Rate} = \frac{|S_k|}{|D|}$$

保留率（Preservation Rate）衡量基模型已解题目中被 $\pi$ 保留的比例：

$$\mathrm{Preservation Rate} = \frac{|\mathcal{P}_k|}{|\mathcal{R}_k(q, D)|}$$

其中 $\mathcal{R}_k(q, D)$ 为基模型在 $k$ 次采样下解决的题目集合，$\mathcal{P}_k$ 为其中 $\pi$ 仍能解决的子集。巩固率（Consolidation）进一步衡量保留题目中可被 $\pi$ 在单次采样（pass@1）稳定解决的比例：

$$C_k(\pi, q) = \frac{|\mathcal{P}_k \cap \mathcal{R}_1(\pi, D)|}{|\mathcal{P}_k|}$$

### 基准构建的流水线模块

MATH-B 的构建依赖多阶段过滤流水线，核心模块按执行顺序包括：

1. **候选来源获取**：从 DAPO-Math-17K 和 DeepScaleR 中提取 53,682 道高难度候选题目（Section 3.2.1）。

2. **质量过滤**：移除多选题、含中文题目、引用图片题目、非整数答案题目等，保留整数值真值以减少验证歧义（Section 3.2.2）。

3. **预筛选与随机采样**：使用 DeepSeek-R1-Distill-Qwen2.5-7B 以 pass@16 排除易解题，随机采样缩减规模（Section 3.2.2）。

4. **真值答案验证**：采用前沿模型 o4-mini-high 和 GPT-5-Mini 以 pass@2 验证真值答案的正确性，仅保留至少一个前沿模型能正确求解的题目（Section 3.2.2）。

5. **去重**：与 MATH-500、MinervaMath、OlympiadBench、AMC23、AIME-2024、AIME-2025 等标准基准进行精确字符串匹配去重（Section 3.2.2）。

6. **pass@1024 最终筛选**：对候选题目在 11 款基模型（如 Qwen2.5、OLMo、Llama-3.1 等系列，参数量 ≤8B）和 9 款补充模型上各生成 1024 个样本，筛选出至少一个模型未能解决的题目（Section 3.2.3）。

7. **最终基准组装**：形成 181 题的 MATH-B-U（并集）和 41 题的 MATH-B-I（交集），以及各模型专属子集（Section 3.2.3）。

### 验证框架的鲁棒性设计

现有基于规则的数学答案验证器存在七类常见失败模式（Table 1），包括仅读取首个或末个盒装答案、依赖特定文本锚点（如 "Answer:"）、答案顺序敏感性等。MATH-B 的验证框架通过规避这些失败模式实现鲁棒验证，但 Table 3 显示，目前尚无评估框架能完全覆盖所有七类失败——TRL、VERL、LM-Eval、LightEval、SCORE、evalchemy、HMMT、Math-V 等八个常见框架在不同失败模式上存在不同程度的漏洞。

## 实验与分析

### 核心发现：RL微调与SFT/蒸馏在推理边界拓展上的显著差距

MATH-Beyond的核心实验围绕扩展率（Expansion Rate）展开，该指标衡量后训练模型在基模型完全无法解决的问题上所获得的新能力。由于MATH-B被设计为零基线基准（基模型pass@1024≈0），任何非零的扩展率都直接反映推理边界的真实拓展。

**Table 2** 展示了主要结果。RL微调模型的扩展率普遍偏低：基于r1-1.5b的Nemotron v1、v2和DeepScaleR-1.5B在pass@1024下分别仅达到7.83%、9.57%和5.22%；基于r1-7b的Skywork-OR1-7B表现稍好，达到21.2%。相比之下，SFT/蒸馏模型Qwen3-4B和Qwen3-8B分别达到58.93%和66.38%的扩展率，差距达3–12倍。这一对比揭示了当前RL后训练的核心瓶颈：**在缺乏教师模型指导的情况下，RL的探索过程难以自主发现有效的推理路径**，导致大部分潜在可学习的问题仍然无法解决。


![[assets/figures/papers/iclr26_0010_RNkErKpCAp_MATH-Beyond_A_Benchmark_for_RL_to_Expand_Beyond/figures/008_Table_2.jpg]]
*Table 2: Expansion Rates of post-trained models using either RL or SFT/Distillation. The Expansion Rate measures the percentage of previously unsolvable problems (from the base model’s perspective) that the post-trained model can now solve We additionally add AIME24 (pass@1) numbers of the post-trained models to illustrate the difficulty of our dataset (He et al., 2025a; Yang et al., 2025; Liu et al., 2025a)*

值得注意的是，这些模型在AIME24上的pass@1表现并不能预测其在MATH-B上的扩展能力。例如，Qwen3-8B在AIME24上pass@1为86.7%，扩展率为66.38%；而Skywork-OR1-7B的AIME24 pass@1为70.0%，扩展率仅21.2%。这说明**传统基准上的性能提升可能主要来自对已有求解模式的锐化，而非真正的新能力获取**。

### 扩展率随采样预算的演化：边际收益递减

**Figure 5** 展示了RL微调模型扩展率随采样预算k的演化。所有RL模型的扩展率在k较小时快速增长，但随着k接近1024，增长趋于平台。这表明即使大幅增加采样预算，RL模型也难以持续解决新的难题——探索能力的上限制约了扩展潜力。


![[assets/figures/papers/iclr26_0010_RNkErKpCAp_MATH-Beyond_A_Benchmark_for_RL_to_Expand_Beyond/figures/011_Figure_5.jpg]]
*Figure 5: Evolution of Expansion Rate for RL Models. Models are evaluated on the MATH-B problems failed by their respective base models (115 for R1-Qwen2.5-1.5B; 99 for R1-Qwen2.5-7B)*

**Figure 6** 进一步展示了所有模型在MATH-B-U上pass@k的对数线性增长模式。虽然整体趋势一致，但不同模型的斜率差异显著：SFT/蒸馏模型的增长曲线明显更陡峭，而RL模型在k较大时几乎停滞。

**Figure 7** 量化了边际收益的递减：平均而言，每增加64次采样，新解决问题的比例随总预算k增大而持续下降。这一发现验证了k=1024作为评估点的合理性——在此预算下，扩展率已基本稳定，进一步增加采样只会带来微弱的边际收益。


![[assets/figures/papers/iclr26_0010_RNkErKpCAp_MATH-Beyond_A_Benchmark_for_RL_to_Expand_Beyond/figures/017_Figure_7.jpg]]
*Figure 7: Average gains in pass@k relative to the size of MATH-B-U. Averaged over 21 models, the rate of solving new problems per 64-sample increment decreases as the total budget k grows, demonstrating diminishing returns*

### 基模型未解决问题的交集分析

**Table 4** 统计了各模型在pass@1024下未解决问题的数量及交集。11款基模型的未解决问题数在99–158之间，交集为41道（MATH-B-I base）；加入9款补充模型后，21款模型的交集缩减为13道（MATH-B-I all）。这一分析表明：

1. **基模型之间的失败模式存在显著差异**：不同模型感到困难的问题并不完全重叠，说明MATH-B的难度来源是多样化的。
2. **41道交集题目代表了对当前开源模型（≤8B）最具挑战性的核心问题集**，可作为评估推理能力突破的“试金石”。
3. **补充模型（如Qwen3-8B）的加入大幅缩减了交集**，这提示SFT/蒸馏方法确实能够覆盖部分基模型无法解决的问题，但仍有13道题目对所有21款模型构成挑战。

### 验证框架的脆弱性分析

**Table 3** 系统比较了8个常见评估框架（TRL、VERL、LM-Eval、LightEval、SCORE、evalchemy、HMMT、Math-V）在7类验证失败模式（F1–F7）上的脆弱性。结果显示：**没有任何框架能完全覆盖所有失败模式**。例如，部分框架仅读取第一个或最后一个boxed答案（F1/F2），或依赖特定文本锚点如“Answer:”（F3），导致在模型输出格式变化时产生错误的评分信号。这些验证漏洞可能在RL训练中引入噪声梯度，误导策略优化方向。MATH-B的鲁棒验证设计（规避F1–F7）确保了评估结果的可靠性，这是准确衡量扩展率的前提。

### 人类难度感知与模型失败的脱节

**Figure 3** 对比了MATH-B-U和MATH-B-I的难度分布（基于人类标注的1–10分制）。一个反直觉的发现是：**模型感到最困难的题目（出现在交集中）并不一定是人类认为最难的题目**。MATH-B-I中的题目难度分布与MATH-B-U整体并无显著偏移，说明人类对数学题难度的直觉与模型的实际失败模式之间存在系统性脱节。这一现象提示，单纯依赖人类难度标注来筛选“挑战性”基准可能不够有效，基于模型实际表现的零基线筛选是更可靠的方法。

## 方法谱系与知识库定位

### 与基线方法的关系

MATH-Beyond 的核心设计意图并非提出一种新的后训练算法，而是构建一个**零基线评估框架**，以暴露当前 RL 微调方法在探索性学习上的根本局限。在这一框架下，三类方法形成了清晰的能力谱系：

- **基模型（零基线）**：如 Qwen2.5-7B、DeepSeek-R1-Distill-Qwen2.5-7B 等，在 MATH-B-U 上 pass@1024 近乎为零（Figure 1 右），构成评估的绝对零点。这意味着任何正扩展率都代表实质性的推理边界拓展，而非对已有能力的采样放大。

- **RL 微调模型（探索瓶颈）**：Nemotron-Research-Reasoning-Qwen-1.5B、DeepScaleR-1.5B-Preview、Skywork-OR1-7B 等基于 GRPO/PRIME 的 RL 后训练模型，在 MATH-B-U 上的扩展率仅为 5.22%~21.2%（Table 2）。这一结果揭示了当前 RL 方法的核心瓶颈：**基模型具备学习能力，但 RL 的探索过程无法自主发现有效的推理路径**（Section 5）。

- **SFT/蒸馏模型（能力上界）**：Qwen3-4B 和 Qwen3-8B 通过长链式思维蒸馏，扩展率分别达到 58.93% 和 66.38%（Table 2），远超 RL 微调模型。这提供了对比上界，同时也暴露了一个关键矛盾：蒸馏方法虽然拓展率高，但依赖强教师模型，本质上并非自主探索性学习。

### 适用边界

MATH-Beyond 的适用边界由以下设计选择严格界定：

1. **模型规模边界**：基准筛选过程以 ≤8B 参数的开源模型为核心（Section 3.2.3），评估结论推广至大参数量模型时需谨慎。扩展率在更大模型上的表现可能不同，但零基线的构建逻辑本身是规模无关的。

2. **数据分布边界**：题目来源于 DAPO-Math-17K 和 DeepScaleR 两个数据集（Section 3.2.1），可能存在分布偏差。特别是 Qwen3 系列模型若在预训练阶段接触过类似数据，可能获得不公平优势（见 fairness_notes）。尽管筛选流程使用了 11 款不同家族的基模型，仍无法完全消除数据污染风险。

3. **验证可靠性边界**：尽管 MATH-Beyond 的验证框架已规避了 7 类常见解析失败模式（Table 1），但 Table 3 显示，现有八个主流评估框架均存在不同程度的验证漏洞，尚无框架能完全覆盖所有失败模式。极端情况下的解析仍可能不完全。

4. **采样预算边界**：扩展率测量基于 pass@1024 的固定采样预算。Figure 5 和 Figure 7 表明，扩展率在 k 接近 1024 时趋于平台，边际收益递减。这一预算在计算可行性和稳定性之间取得了平衡，但更高预算下的行为未经验证。

### 局限与开放问题

#### 已明确的结构性局限

- **RL 探索失效**：当前 RL 方法在无教师模型的情况下，难以自主发现有效推理路径，导致扩展率远低于 SFT/蒸馏方法。这是 MATH-Beyond 揭示的核心瓶颈，而非基准本身的设计缺陷。

- **人类与模型难度感知脱节**：Figure 3 显示，MATH-B-U 和 MATH-B-I 的难度分布广泛，但模型感到困难的题目并不一定是人类认为最难的题目。这一脱节现象目前缺乏量化解释。

- **题目来源集中**：候选题目仅来自两个数据集，可能限制基准的领域覆盖和分布多样性。

#### 开放问题

1. **如何设计 RL 算法使其在无教师模型的情况下自主发现有效推理路径？** 这是 MATH-Beyond 暴露的最紧迫问题。当前 RL 方法扩展率有限，但 SFT/蒸馏方法的高扩展率证明基模型具备学习能力——瓶颈在于探索过程本身。

2. **人类难度感知与模型失败模式之间的脱节是否有可量化的解释？** 理解这一脱节的根源，可能为设计更有效的训练信号或课程学习策略提供方向。

3. **扩展率评价框架能否推广至其他领域？** 在代码、科学推理等领域构建类似的零基线基准，可能揭示 RL 探索性学习在不同推理模态中的共性瓶颈。

## 原文 PDF

![[paperPDFs/ICLR_2026/MATH_Beyond_A_Benchmark_for_RL_to_Expand_Beyond_the_Base_Model.pdf]]
