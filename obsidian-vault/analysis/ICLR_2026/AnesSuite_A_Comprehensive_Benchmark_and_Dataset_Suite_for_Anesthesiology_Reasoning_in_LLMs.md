---
title: "AnesSuite: A Comprehensive Benchmark and Dataset Suite for Anesthesiology Reasoning in LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AnesSuite_A_Comprehensive_Benchmark_and_Dataset_Suite_for_Anesthesiology_Reasoning_in_LLMs.pdf
project_link: null
code_link: https://github.com/MiliLab/AnesSuite
openreview_forum_id: iKRQMeC7yO
aliases:
- AnesSuite
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/health
core_operator: "引入包含详细思维链的麻醉学专用推理数据集 AnesR1，并采用监督微调（SFT）与分组相对策略优化（GRPO）的组合训练范式。"
primary_logic: "通过构建涵盖三层认知需求（System 1/1.x/2）的双语基准 AnesBench，并开发配套的 CoT 训练数据集 AnesR1，结合冷启动 SFT 与强化学习 GRPO，能够显著提升 LLMs 在麻醉学复杂推理上的表现。该推理能力不仅可媲美更大规模模型，还展现出向通用医学和通用领域泛化的潜力。"
claims:
- "大多数开源模型在 AnesBench 的 System 2 问题上准确率低于 0.5。"
- "Morpheus-7B 经过 SFT+GRPO 后，平均准确率达到 0.63，与 Qwen2.5-14B-Instruct 的 0.64 相当。"
- "对 System 2 问题，模型输出长度越长，得分越高，表明 CoT 推理对复杂决策至关重要。"
- "继续预训练（CPT）在 AnesCorpus 上增强了英文基准性能，但损害了中文基准性能。"
---

# AnesSuite: A Comprehensive Benchmark and Dataset Suite for Anesthesiology Reasoning in LLMs

> [!tip] 核心洞察
> 通过构建涵盖三层认知需求（System 1/1.x/2）的双语基准 AnesBench，并开发配套的 CoT 训练数据集 AnesR1，结合冷启动 SFT 与强化学习 GRPO，能够显著提升 LLMs 在麻醉学复杂推理上的表现。该推理能力不仅可媲美更大规模模型，还展现出向通用医学和通用领域泛化的潜力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AnesSuite：面向LLMs麻醉学推理的综合基准与数据集套件 |
| 英文题名 | AnesSuite: A Comprehensive Benchmark and Dataset Suite for Anesthesiology Reasoning in LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=iKRQMeC7yO) · [GitHub](https://github.com/MiliLab/AnesSuite) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/health |
| Method | Morpheus |
| Dataset | AnesBench-English (Overall), AnesBench-English System2, MedQA (US) |

> [!tip] 效果简介
> - AnesBench-English (Overall) 上，Accuracy 为 Morpheus-7B: 0.56; Morpheus-14B: 0.63; Morpheus-32B: 0.68，对比 Qwen2.5-7B-Inst: 0.51; Qwen2.5-14B-Inst: 0.57; Qwen2.5-32B-Inst: 0.61，变化 +0.05, +0.06, +0.07。
> - AnesBench-English System2 上，Accuracy 为 Morpheus-14B: 0.47，对比 Qwen2.5-14B-Inst: 0.41，变化 +0.06。
> - MedQA (US) 上，Accuracy 为 Morpheus-7B: 0.656，对比 Qwen2.5-7B-Inst: 0.505，变化 +0.151。

## 概要

当前大语言模型（LLMs）在麻醉学领域面临一个核心瓶颈：**高阶推理能力（System 2）严重不足**。多数开源模型在需要多步逻辑推演的麻醉学问题上准确率低于 0.5，且普遍出现非逻辑推理（Non‑Sequitur）与过度推断（Over‑extrapolation）等逻辑幻觉（Table 3）。这意味着通用模型即使具备一定医学知识，也难以胜任麻醉临床中复杂的决策推理。

针对这一瓶颈，本文提出 **AnesSuite**——首个面向麻醉学推理的综合数据集套件，并基于此开发了 **Morpheus** 系列模型。其核心思路是：通过构建涵盖三层认知需求（System 1 / 1.x / 2）的双语基准 **AnesBench**，以及配套的思维链（CoT）训练数据集 **AnesR1**，再结合冷启动监督微调（SFT）与分组相对策略优化（GRPO）的组合训练范式，显著提升模型在麻醉学复杂推理上的表现。方法定位上，Morpheus 以 Qwen2.5 系列为基座，先在 AnesR1 上进行 SFT 获得 CoT 推理格式与领域知识，再通过 GRPO 利用结果二元奖励进一步强化推理能力（Figure 1）。

主要结果表明，该方案有效且具备良好的规模扩展性：
- Morpheus‑7B 经 SFT + GRPO 后，平均准确率达到 0.63，与参数规模大得多的 Qwen2.5‑14B‑Instruct（0.64）相当（Table 4）。
- 在 AnesBench 英文整体基准上，Morpheus‑7B/14B/32B 相比对应规模的 Qwen2.5‑Instruct 基线分别提升 +0.05、+0.06、+0.07（Table 4）。
- 对 System 2 问题，模型输出长度越长则得分越高，验证了 CoT 推理对复杂决策的关键作用（Figure 7）。

此外，推理能力还展现出向通用医学领域泛化的潜力：Morpheus‑7B 在 MedQA（US）上准确率达 0.656，较基线的 0.505 提升 +0.151（Table 20）。消融实验同时揭示，继续预训练（CPT）虽能增强英文基准性能，却会损害中文基准表现（Table 5），提示多语言知识对齐仍是待解决问题。



麻醉学是围术期医学的核心，涉及从术前评估、术中管理到术后监护的全链条复杂决策。临床决策不仅依赖大量事实性知识的即时回忆（System 1 认知），更需要在不确定、信息不完全的条件下进行多步骤逻辑推理（System 2 认知）。然而，当前大语言模型（LLMs）在麻醉学领域的表现存在一个关键瓶颈：**多数开源模型的高阶推理能力严重不足，在需要复杂推理的 System 2 问题上准确率普遍低于 0.5**（Table 3）。具体而言，模型频繁出现非逻辑推理（Non-Sequitur）和过度推断（Over-extrapolation）等逻辑幻觉，无法可靠地支撑临床决策。

这一瓶颈的根源在于领域资源的系统性缺失。通用医学基准（如 MedQA、MedMCQA）虽然覆盖广泛的医学知识，但几乎不涉及麻醉学特有的围术期推理场景；而现有的麻醉学考试题库（如美国麻醉学委员会试题）多为零散的非公开资源，缺乏结构化的认知层级标注和双语覆盖。更为关键的是，**缺乏包含详细思维链（Chain-of-Thought, CoT）的麻醉学专用推理数据集**，导致模型无法通过监督信号学习该类复杂推理的模式。

针对上述缺口，本文的核心动机是构建一个从基准评估到训练数据的完整麻醉学推理套件 AnesSuite，并基于此开发专门的推理模型。AnesSuite 包含四个组件：双语结构化基准 AnesBench、大规模领域语料库 AnesCorpus、文献问答数据集 AnesQA，以及带有可验证 CoT 标注的推理数据集 AnesR1（Figure 1）。AnesBench 采用三层认知需求框架——System 1（事实回忆）、System 1.x（混合基础推理）和 System 2（复杂推理），以精细诊断模型在不同认知层级上的能力差异（Figure 2）。

在模型层面，本文提出 Morpheus 系列模型，以 Qwen2.5 系列为基础，在 AnesR1 上采用监督微调（SFT）冷启动与分组相对策略优化（GRPO）的组合训练范式。SFT 阶段使模型获得麻醉学 CoT 推理的格式与领域知识，GRPO 阶段则通过基于结果的二元奖励机制进一步强化推理能力。通过这一套件与训练范式的协同，Morpheus 不仅在麻醉学推理上显著超越同规模基线，还展现出向通用医学和通用领域泛化的潜力。



## 核心方法与创新机理

### 问题瓶颈：LLMs 在麻醉学高阶推理上的系统性失败

AnesSuite 的基准评估揭示了一个清晰的瓶颈：当前大语言模型在麻醉学领域的 **System 2 高阶推理**上严重不足。如 Table 3 所示，大多数开源模型在 AnesBench 的 System 2 问题上准确率低于 0.5，即便是 GPT-4o 和 Claude-3.7-Sonnet 等闭源前沿模型也仅能达到 0.5 至 0.6 的水平。进一步的幻觉分析（Table 24）表明，这些错误并非随机的知识缺失，而是系统性地表现为**非逻辑推理（Non-Sequitur）**和**过度推断（Over-extrapolation）**——模型在缺乏充分依据时强行建立因果联系或超出给定信息范围进行推测。这一发现将问题从“模型缺乏麻醉学知识”重新定义为“模型缺乏结构化的临床推理能力”，为后续方法设计提供了明确的因果靶点。

### 核心创新：领域专用 CoT 推理数据集与两阶段训练范式

针对上述瓶颈，AnesSuite 的核心创新在于构建了 **AnesR1**——首个包含详细思维链（Chain-of-Thought）标注的麻醉学推理数据集——并配套设计了“监督微调（SFT）+ 分组相对策略优化（GRPO）”的组合训练范式。这一方案实现了两个关键的 **changed slots**：

| 创新维度 | 基线方法 | 本工作方法 | 证据锚点 |
|---------|---------|-----------|---------|
| **领域微调数据集** | 通用医学 QA 或无领域微调 | AnesR1（包含麻醉学多选题与 CoT 推理链） | “Initialized from the Qwen2.5-7B, Qwen2.5-14B and Qwen2.5-32B, it was trained on AnesR1 using SFT and GRPO” |
| **强化学习阶段** | 无强化学习（仅指令微调） | GRPO（基于结果二元奖励的强化学习） | “Both models underwent SFT followed by GRPO” |

AnesR1 的设计直接回应了 System 2 推理失败的根本原因：它不仅在问题层面覆盖了三层认知需求（System 1/1.x/2，分布见 Figure 2），更关键的是为每个问题提供了**可验证的推理链标注**。这使得模型在 SFT 阶段能够学习到麻醉学特有的临床推理模式（如鉴别诊断的逻辑展开、检查结果的逐步解读），而非仅仅记忆事实性知识。

训练流程分为三个模块：
1. **基础模型初始化**：以 Qwen2.5 系列（7B/14B/32B）作为初始参数，利用其已有的通用语言能力。
2. **监督微调（SFT）**：在 AnesR1 上进行冷启动训练，使模型获得麻醉学 CoT 推理的格式和知识——“the SFT stage serves as a cold-start initializing for the subsequent GRPO training”。
3. **分组相对策略优化（GRPO）**：采用基于结果的二元奖励机制进一步强化推理能力。与仅做 SFT 相比，GRPO 阶段利用可验证奖励信号对复杂推理任务进行针对性优化。

### 创新效果：推理能力的质变与规模效率

Table 4 的结果直接验证了上述创新的有效性。以 Morpheus-7B 为例，经过 SFT+GRPO 训练后，其在 AnesBench 上的平均准确率达到 0.63，**与未经领域训练的 Qwen2.5-14B-Instruct（0.64）相当**——这意味着通过领域推理训练，7B 模型实现了与两倍规模通用模型相媲美的性能。在 System 2 子集上，Morpheus-14B 达到 0.47，较 Qwen2.5-14B-Inst 的 0.41 提升了 6 个百分点（+0.06），增幅显著。

更值得关注的是推理能力的泛化效果。在 MedQA（US）基准上，Morpheus-7B 达到 0.656，较基线的 0.505 提升了 15.1 个百分点（Table 20），表明在麻醉学这一稀疏暴露领域获得的推理技能具有向通用医学推理迁移的潜力。

Figure 7 从机制层面解释了性能提升的来源：对于 System 2 问题，模型输出长度与得分呈正相关，说明 **CoT 推理链的长度直接贡献于复杂决策质量**。这一发现与 AnesR1 提供详细推理链的设计初衷高度一致，构成了“数据设计→训练范式→推理行为→性能提升”的完整因果链条。



![[assets/figures/papers/iclr26_0011_iKRQMeC7yO_AnesSuite_A_Comprehensive_Benchmark_and_Dataset/figures/001_Figure_1.jpg]]
*Figure 1: Overview of AnesSuite. AnesSuite is composed of four components: AnesBench, a crosslingual structured benchmark; AnesCorpus, a collection of anesthesiology documents; AnesQA, a question-answering dataset derived from domain literature; and AnesR1, a dataset featuring verifiable anesthesiology questions with chain-of-thought annotations. Leveraging this suite, we developed Morpheus, the first collection of reasoning LLMs for anesthesiology. Subsequent ablation and experiments identified key factors influencing reasoning performance in this specialized domain*

AnesSuite 是一个面向麻醉学推理与决策的综合数据套件，其核心由四个组件构成：**AnesBench**（双语结构化基准）、**AnesCorpus**（大规模领域文档集）、**AnesQA**（领域文献衍生的问答数据集）和 **AnesR1**（带思维链标注的麻醉学推理数据集）。基于该套件，作者开发了 **Morpheus**——首个专为麻醉学设计的推理型大语言模型系列。

### 数据套件架构与模块关系

AnesSuite 的四组件设计遵循“评估-预训练-监督微调-强化学习”的递进逻辑，其整体架构如 Figure 1 所示。各模块的规模与角色概览见 Table 1。

**AnesBench** 是整个套件的评估核心，包含 7,972 道双语（中/英）多选题，按三层认知需求框架组织：System 1（事实回忆）、System 1.x（事实回忆与初级推理的混合）和 System 2（复杂推理与决策）。这一分层设计直接锚定了后续模型训练与评估的目标维度。

**AnesCorpus** 作为预训练语料，汇集了超过 240 万份麻醉学文档。其构建采用基于频率的关键词过滤方法，并经过两阶段去污染处理：第一阶段使用 n-gram 重叠快速筛选，第二阶段以最长公共子序列（LCS，阈值 64 字符）严格剔除与 AnesBench 题目重叠的文档。

**AnesQA** 是从领域文献中通过多阶段 LLM 流水线生成的监督微调数据集，包含超过 20,713 个问答对。生成流程中，LLaMA3.3-70B-Instruct 负责从文档片段生成自包含问题，Qwen2.5-72B-Instruct 进行质量过滤，最终经正则表达式筛查剔除 119 个有问题的 QA 对。

**AnesR1** 是推理能力训练的关键数据集，包含可验证的麻醉学多选题及其详细思维链（CoT）标注。其认知需求分布与 AnesBench 对齐（Figure 2），为后续的监督微调和强化学习提供了格式与推理路径的冷启动基础。

### Morpheus 模型开发流水线

Morpheus 系列的开发遵循三阶段流水线：

1. **基础模型初始化**：以 Qwen2.5 系列（7B/14B/32B）作为初始参数，利用其通用语言能力作为领域特化的起点。

2. **监督微调（SFT）**：在 AnesR1 上进行冷启动训练，使模型获得麻醉学 CoT 推理的格式规范和领域知识。此阶段为后续强化学习提供稳定的初始策略。

3. **分组相对策略优化（GRPO）**：采用基于结果的二元奖励机制进行强化学习。模型对每个问题生成一组候选回答，根据答案正确性获得奖励信号，通过组内相对比较优化推理策略。训练奖励曲线（Figure 9、Figure 10）显示了模型在 GRPO 阶段的持续改进。

### 输入输出流

整个系统的输入输出流可概括为：
- **评估流**：AnesBench 题目 → 零样本 CoT 提示 → 模型推理（温度 0，最大 2048 tokens，sglang 框架）→ 答案提取 → 准确率计算。
- **训练流**：AnesR1 数据 → SFT 冷启动 → GRPO 强化优化 → Morpheus 模型。
- **预训练增强流**（可选）：AnesCorpus → 继续预训练（CPT）→ 增强领域知识基础。

该架构的核心设计思想在于：通过构建与评估基准认知层次对齐的训练数据，结合监督微调与强化学习的组合范式，系统性地提升 LLM 在麻醉学复杂推理上的表现。Figure 1 以信息图形式完整呈现了从数据构建到模型开发的闭环流程。



### 关键模块

AnesSuite 的核心技术链路围绕三个关键模块展开，构成从数据构建到推理能力强化的完整闭环。

**模块一：AnesR1 — 麻醉学思维链训练数据集**
AnesR1 是驱动 Morpheus 模型推理能力的核心数据引擎。该数据集包含带有详细思维链（Chain-of-Thought, CoT）标注的麻醉学多选题，其认知需求分布与基准 AnesBench 对齐，覆盖 System 1（事实回忆）、System 1.x（混合推理）和 System 2（复杂推理）三个层级（Figure 2）。AnesR1 的 CoT 标注为模型提供了结构化的推理模板，是后续监督微调（SFT）冷启动和强化学习（GRPO）的基础燃料。

**模块二：SFT 冷启动**
监督微调阶段在 AnesR1 上进行，使模型获得麻醉学领域 CoT 推理的格式规范与基础知识。该阶段的核心作用是为后续强化学习提供稳定的初始策略，避免 GRPO 在稀疏奖励环境中从随机策略出发导致的训练不稳定。论文明确指出：“the SFT stage serves as a cold-start initializing for the subsequent GRPO training”。

**模块三：GRPO 强化学习**
分组相对策略优化（Group Relative Policy Optimization, GRPO）利用基于结果的二元奖励机制进一步强化模型的推理能力。GRPO 不依赖过程奖励模型（Process Reward Model），而是仅根据最终答案的正确性给予奖励，在保持训练简洁性的同时，显著提升了模型在 System 2 复杂推理任务上的准确率。训练奖励曲线（Figure 9、Figure 10）显示 Morpheus-7B 和 Morpheus-14B 在 GRPO 阶段均获得了稳定的奖励提升。

### 关键公式

论文在数据泄露检测和统计分析中给出了明确的公式定义，以下为可直接引用的公式。

**数据泄露检测的置信度分数**

该公式用于检测多选题是否存在数据泄露风险。对于给定的多选题实例，计算模型在原始选项顺序下的 token 概率几何平均值，并与所有选项排列组合下的置信度进行比较。

$$\mathrm{Conf}_{\mathrm{LLM}}(x) = \left( \prod_{i=1}^{m-1} p_{\mathrm{LLM}}(t_i | x) \right)^{\frac{1}{m-1}}$$

其中：
- $x$ 为输入上下文（包含问题与选项序列）
- $t_i$ 为序列中第 $i$ 个 token
- $m-1$ 为序列长度（token 数量）
- $p_{\mathrm{LLM}}(t_i | x)$ 为语言模型在给定上下文 $x$ 下预测 token $t_i$ 的概率
- $\mathrm{Conf}_{\mathrm{LLM}}(x)$ 为几何平均置信度分数

若原始选项顺序在所有排列中具有最高置信度分数，则认为该多选题实例存在潜在数据泄露。论文基于随机基线假设，验证该方法在无先验知识情况下的潜在泄露比例为 0.04。

**规模-性能交互效应的线性模型**

该公式用于比较 System 1.x 和 System 2 两类问题随模型规模变化的性能斜率是否存在显著差异。

$$y = \beta_0 + \beta_1 x + \beta_2 \cdot \mathrm{group} + \beta_3 (x \times \mathrm{group}) + \varepsilon$$

其中：
- $y$ 为模型在特定问题类型上的准确率
- $x$ 为模型规模指标（model index）
- $\mathrm{group}$ 为问题类型指示变量（System 1.x 或 System 2）
- $\beta_1$ 为 System 1.x 的规模-性能斜率
- $\beta_3$ 为两类问题斜率差异的交互项系数
- $\varepsilon$ 为误差项

通过检验 $\beta_3$ 的显著性，论文验证了 System 2 任务的规模收益递减趋势与 System 1.x 存在统计差异。

> **注意**：以上公式均来自论文附录 A.1 和 F.1 节，变量含义严格依据原文定义。论文未给出 GRPO 奖励函数或 SFT 损失函数的具体数学形式，因此本节不予推导。



## 实验与关键发现

### 主要评估结果

AnesBench 上的大规模评测揭示了当前 LLMs 在麻醉学推理上的能力瓶颈。**核心瓶颈在于 System 2（高阶推理）**：多数开源模型在该类问题上的准确率低于 0.5（Table 3），而 GPT-4o 和 Claude-3.7-Sonnet 等闭源模型也仅在 0.5 至 0.6 之间徘徊。这一定量证据直接暴露了现有模型在复杂临床决策中的逻辑短板。

![[assets/figures/papers/iclr26_0011_iKRQMeC7yO_AnesSuite_A_Comprehensive_Benchmark_and_Dataset/figures/008_Table_3.jpg]]
*Table 3: Main Evaluation Results on AnesBench. The highest and second-highest accuracies in each column are highlighted in bold and underlined, respectively. Complete results are in Appendix B.3*

Morpheus 系列模型在 SFT + GRPO 训练后取得了显著提升。**Morpheus-7B 的平均准确率达到 0.63，与 Qwen2.5-14B-Instruct 的 0.64 相当**（Table 4），表明领域推理训练可以有效弥补参数规模的差距。具体而言，Morpheus-7B 在 AnesBench-English 总体准确率上从基线的 0.51 提升至 0.56，Morpheus-14B 从 0.57 提升至 0.63，Morpheus-32B 从 0.61 提升至 0.68（Table 4）。在最具挑战性的 System 2 子集上，Morpheus-14B 达到 0.47，较 Qwen2.5-14B-Instruct 的 0.41 提升了 6 个百分点。

![[assets/figures/papers/iclr26_0011_iKRQMeC7yO_AnesSuite_A_Comprehensive_Benchmark_and_Dataset/figures/009_Table_4.jpg]]
*Table 4: Evaluation Results of Morpheus on AnesBench*

### 关键消融发现

**1. 模型规模与性能呈强正相关，但存在边际收益递减。** 统计检验（Table 13, Table 14）证实了这一趋势。Figure 5 的散点图清晰展示了性能随模型规模增长而提升的总体模式，但 System 2 问题的斜率更为平缓，暗示单纯扩大规模对高阶推理的增益有限。

**2. 思维链长度对 System 2 任务至关重要。** Figure 7 的分析表明，对于 System 2 问题，模型输出长度与得分呈正相关——输出越长的模型往往得分越高。然而，这一效应在 System 1 和 System 1.x 问题上不显著。这验证了 CoT 推理对复杂决策的核心作用：浅层知识检索不需要长链推理，但临床综合判断依赖于逐步的逻辑展开。

![[assets/figures/papers/iclr26_0011_iKRQMeC7yO_AnesSuite_A_Comprehensive_Benchmark_and_Dataset/figures/014_Figure_7.jpg]]
*Figure 7: Impact of Output Length Shapes and colors denote model families and scales*

**3. 继续预训练（CPT）存在语言性能的二分效应。** 在 AnesCorpus 上进行 CPT 提升了英文基准性能，但损害了中文基准性能（Table 5, Table 16）。这一发现提示，单语 CPT 可能导致灾难性遗忘或语言特定知识系统的偏移，双语训练策略的必要性由此凸显。

![[assets/figures/papers/iclr26_0011_iKRQMeC7yO_AnesSuite_A_Comprehensive_Benchmark_and_Dataset/figures/015_Table_5.jpg]]
*Table 5: Effectiveness of Training Strategies and Data The Qwen2.5-7B-Base-CPT model is trained on our AnesCorpus, with Qwen2.5-7B-Base serving as the foundation model*

**4. SFT 数据集的互补性。** AnesQA 与 Medical-o1 两个 SFT 数据集联合使用时，可获得优于单独使用的麻醉学推理性能（Table 5, Table 17），表明领域知识注入与通用医学推理训练存在协同效应。

### 跨领域泛化

Morpheus 展现出了超出麻醉学领域的泛化潜力。在 MedQA（US）上，Morpheus-7B 达到 0.656，较 Qwen2.5-7B-Instruct 的 0.505 提升了 15.1 个百分点（Table 20）。在 MMLU 和 AGIEval 等通用基准上也观察到了一致性提升（Table 21, Table 22），说明麻醉学推理训练获得的技能具有向通用领域迁移的能力。

![[assets/figures/papers/iclr26_0011_iKRQMeC7yO_AnesSuite_A_Comprehensive_Benchmark_and_Dataset/figures/035_Table_20.jpg]]
*Table 20: Evaluation Result on MedQA*

### 失败模式与推理幻觉

对 System 2 问题的输出分析（Table 24）揭示了两种主要的**逻辑幻觉**模式：

- **非逻辑推理（Non-Sequitur）**：模型生成的推理步骤之间缺乏逻辑连贯性，结论与前提脱节。
- **过度推断（Over-extrapolation）**：模型在证据不足的情况下进行超出合理范围的推断，导致错误决策。

这些幻觉模式在较小规模模型中更为突出，且与 CoT 长度不足密切相关，进一步强化了“长链推理对复杂决策至关重要”的因果论断。

### 跨语言性能差异

Figure 6 和 Table 15 揭示了显著的跨语言性能差异。Llama-3.1-8B 系列模型在中文上的表现大幅下降（p=9e-5），而 Qwen2.5 系列由于在中文语料上的预训练优势，跨语言差距相对较小。这表明基础模型的语言预训练分布对领域微调后的跨语言性能有决定性影响。

### 数据泄露检测

采用基于置信度分数的数据泄露检测方法（Figure 8），多数模型显示出约 0.10 的潜在泄露比例，高于随机基线假设的 0.04。这一结果提示在基准构建中需持续关注数据污染问题，但当前泄露水平尚不足以显著影响主要结论的有效性。



## 定位与知识库关联

### 1. 方法谱系与基线关系

Morpheus 系列的训练范式可视为“领域冷启动 + 推理强化”两条主线的交汇点。其直接基线是 Qwen2.5-Instruct 系列（7B/14B/32B），这些模型仅经过通用指令微调，在 AnesBench 的 System 2 层级上准确率普遍低于 0.5（Table 3），暴露出通用大模型在麻醉学高阶推理上的结构性短板。另一类对照是医学专用推理模型 HuatuoGPT-o1（7B/8B/70B/72B），其领域特异性训练虽带来一定提升，但在 System 2 上仍未能突破多数开源模型面临的瓶颈。

从方法演变看，Morpheus 在两个关键槽位上做出了改变：

- **领域微调数据集**：从通用医学 QA 或无领域微调，替换为 AnesR1——一个包含麻醉学多选题与详细思维链（CoT）推理过程的数据集。这一改变使模型在 SFT 阶段即获得了麻醉学特有的推理格式与知识框架。
- **强化学习阶段**：从无强化学习（仅指令微调）升级为 GRPO（分组相对策略优化），采用基于结果正确性的二元奖励机制。GRPO 在 SFT 冷启动之后进一步强化推理能力，使模型学会在复杂场景下生成更长的有效推理链。

这一范式与 BioMistral 7B Chat 等早期生物医学微调模型形成代际差异：后者仅依赖领域文本的继续预训练或简单指令微调，缺乏针对推理过程的显式建模。

### 2. 适用边界与前提条件

Morpheus 的有效性依赖于以下前提：

1. **基础模型能力下限**：实验表明模型规模与性能呈强正相关（Figure 5），且 AnesR1 在 7B 模型上效果显著，但 0.5B 模型上几乎无提升（Table 11），说明极小模型缺乏承载 CoT 推理的容量。
2. **双语知识对齐**：继续预训练（CPT）在 AnesCorpus 上存在明显的语言偏向性——提升英文基准性能的同时损害中文基准性能（Table 5, Table 16）。这意味着单语 CPT 策略在多语言场景下存在适用边界，需额外设计双语对齐机制。
3. **CoT 推理的边际价值**：思维链长度对 System 2 任务有显著促进作用，但对 System 1/1.x 任务不显著（Figure 7）。因此，GRPO 强化推理的收益主要集中在需要多步逻辑推理的场景，对事实回忆型问题帮助有限。
4. **数据集互补性**：AnesQA 与 Medical-o1 两个 SFT 数据集相互补充，联合使用可获得更优的麻醉学推理性能（Table 5, Table 17），单独使用任一个可能无法达到最优效果。

### 3. 局限与已知盲区

论文明确指出的局限包括：

- **生态效度不足**：AnesBench 的 System 2 问题基于抽象场景构建，而非真实临床病例。这意味着基准高分未必能直接映射到实际临床决策能力，需手动验证。
- **模态单一**：当前基准仅包含文本多选题和少量开放式问题，未涵盖影像、监护波形、药物剂量曲线等多模态临床数据，限制了评估的全面性。
- **专科泛化待验证**：Morpheus 仅在麻醉学数据上微调，其对其他医学亚专科的推理泛化能力仍需更大规模验证。虽然在 MedQA 上观察到 +0.151 的显著提升（Morpheus-7B: 0.656 vs. Qwen2.5-7B-Inst: 0.505），但这仅是单一外部基准的结果。
- **评估偏差风险**：自动化指标（BLEU、F1）无法可靠评估医学推理的细微之处，而采用 LLM-as-Judge 的评估方式可能引入新的系统性偏差。

此外，分析揭示了两类系统性推理幻觉：**非逻辑推理（Non-Sequitur）**——结论与前提之间缺乏逻辑关联；以及**过度推断（Over-extrapolation）**——基于不完整信息做出超出证据支持的判断（Table 24）。这些幻觉在 System 2 任务中尤为突出，且当前 GRPO 的二元奖励机制无法直接惩罚推理过程的质量问题。

### 4. 开放问题

论文提出了若干未解决的关键问题：

1. **推理技能的跨领域迁移性**：通过强化学习在麻醉学这一稀疏暴露领域获得的推理能力，能否稳定迁移到更通用的推理任务？初步证据显示 Morpheus 在 MedQA 和 AGIEval 上有正向泛化（Table 18, Table 20, Table 21），但其机制尚不清晰。

2. **过程奖励与幻觉抑制**：如何结合过程奖励模型（Process Reward Model）和检索增强生成（RAG）来减少临床推理中的非逻辑推理和过度推断？当前 GRPO 仅使用结果奖励，无法对推理链的中间步骤进行质量约束。

3. **多模态推理扩展**：如何将检索系统扩展至多模态临床数据（影像、波形、时序监测数据），以增强推理的连贯性和准确性？这一方向将直接影响模型在真实临床场景中的实用性。

4. **跨语言知识对齐机制**：多语言模型中语言专属知识系统的建立过程如何影响跨语言推理性能？CPT 实验揭示的语言偏向性提示，需要更精细的双语知识对齐策略，而非简单的语料混合训练。



## 原文 PDF

![[paperPDFs/ICLR_2026/AnesSuite_A_Comprehensive_Benchmark_and_Dataset_Suite_for_Anesthesiology_Reasoning_in_LLMs.pdf]]
