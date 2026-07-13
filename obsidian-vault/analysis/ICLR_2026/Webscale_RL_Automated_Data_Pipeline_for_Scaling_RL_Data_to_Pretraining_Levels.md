---
title: "Webscale-RL: Automated Data Pipeline for Scaling RL Data to Pretraining Levels"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Webscale_RL_Automated_Data_Pipeline_for_Scaling_RL_Data_to_Pretraining_Levels.pdf
project_link: https://huggingface.co/datasets/Salesforce/Webscale-RL
code_link: https://github.com/SalesforceAIResearch/PretrainRL-pipeline
aliases:
- WR
- Webscale-RL
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "通过自动化、分阶段的数据转换管道，将海量预训练文档转化为符合RL格式的问答对，同时保留原始数据的多样性与规模，从而直接解除RL的数据供给瓶颈。"
primary_logic: "将预训练文本转换为可验证的QA对，使RL能够以极低的token消耗（约1/100）匹配甚至超越持续预训练的性能，证明了RL的样本效率优势在通用领域同样适用，并为RL规模化至预训练级别提供了可行路径。"
claims:
- "Webscale-RL pipeline can convert large-scale pretraining documents into 1.2M verifiable QA pairs across 9+ domains, matching the scale of existing RL/SFT datasets but with superio..."
- "RL training on Webscale-RL data achieves average score 52.1 across benchmarks, outperforming all data refinement baselines and narrowing the gap to Qwen2.5-7B from 10.6 to 6.1."
- "Webscale-RL shows ~100× data efficiency: RL with 10M tokens attains similar MMLU-pro performance to continual pretraining with 1B tokens."
- "The pipeline's QA pairs are extracted from documents rather than distilled from a strong LLM, reducing bias and enabling use of cost-effective generators."
---

# Webscale-RL: Automated Data Pipeline for Scaling RL Data to Pretraining Levels

> [!tip] 核心洞察
> 将预训练文本转换为可验证的QA对，使RL能够以极低的token消耗（约1/100）匹配甚至超越持续预训练的性能，证明了RL的样本效率优势在通用领域同样适用，并为RL规模化至预训练级别提供了可行路径。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Webscale-RL：将RL数据扩展至预训练规模的自动化数据管道 |
| 英文题名 | Webscale-RL: Automated Data Pipeline for Scaling RL Data to Pretraining Levels |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=hOJS9RB1NU) · [GitHub](https://github.com/SalesforceAIResearch/PretrainRL-pipeline) · [Project](https://huggingface.co/datasets/Salesforce/Webscale-RL) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Webscale-RL |
| Dataset | Average across 7 benchmarks (MMLU-pro, Big-Bench, GPQA-D, MATH500, GSM8K, MBPP, EvalPlus), Gap to Qwen2.5-7B (average across benchmarks), MMLU-pro (Scaling efficiency), Big-Bench (Scaling efficiency) |

> [!tip] 效果简介
> - Average across 7 benchmarks (MMLU-pro, Big-Bench, GPQA-D, MATH500, GSM8K, MBPP,... 上，Score 为 52.1，对比 48.7 (GDR), next best is 48.3 (Continual Pretraining+SFT)，变化 +3.4 over strongest baseline。
> - Gap to Qwen2.5-7B (average across benchmarks) 上，Score difference 为 6.1，对比 10.6 (Qwen2.5-3B base vs. 7B)，变化 -4.5 (gap reduced by 42%)。
> - MMLU-pro (Scaling efficiency) 上，Tokens required to reach ~43 score 为 ~10M RL tokens (derived from >1000 original documents)，对比 ~1B tokens (continual pretraining)，变化 ~100× fewer tokens。

## 概要

大规模语言模型的强化学习（RL）训练长期受制于高质量、可验证问答数据的稀缺：现有RL数据集规模（<10B tokens）远小于预训练语料（>1T tokens），且领域集中在数学、代码等少数方向，限制了RL在通用推理能力上的规模化。Webscale-RL 提出一条自动化数据管道，将海量预训练文档转化为可验证的问答对，从而在保持多样性的同时为RL提供足量训练信号。管道分为四个阶段——数据过滤、领域分类与角色分配、基于文档的可验证QA生成、以及质量与泄漏检查——最终构造出约 1.2M 对、覆盖 9+ 领域的 RL 数据集（Table 1，Table 3）。

该方法的核心是将数据表示从非结构化文本序列转换为自包含的问答对，并将训练目标从 teacher forcing 的下一个token预测转化为基于二元奖励的强化学习（公式(1)(2)）。实验表明，在 Qwen2.5-3B 基座上，Webscale-RL 的 RL 训练仅需约 10M（源自原始文档的）token，即可在 MMLU-pro、Big-Bench 等基准上达到持续预训练约 1B token 的性能水平（约 100× 数据效率，Figure 4）。在七项综合评测上，Webscale-RL 平均得分 52.1，高出最强数据精炼基线（GDR）3.4 分，并将与 Qwen2.5-7B 的性能差距从 10.6 缩窄至 6.1（缩小 42%，Table 2）。这一结果证明了将预训练文本转换为可验证问答并施加 RL，在通用领域同样具有极高的样本效率，并为 RL 数据扩展至预训练级别提供了可行路径。

大语言模型的能力通常通过两个阶段构建：在大规模非结构化文本上的预训练（next‑token prediction）让模型习得广泛的世界知识与语言模式；随后借助微调或对齐手段提升其指令遵循能力与推理质量。在微调环节，基于强化学习（RL）的训练（如通过答案匹配的二元奖励优化）已被证明能够显著改善模型的输出。然而，RL 训练能否在通用任务上持续精进，高度依赖**高质量、多样化且可验证**的问答对数据。现有 RL 数据集大多集中于数学、编程等少数领域，整体规模不足 100 亿 token，而预训练语料却可触及万亿 token 并覆盖数百个领域（图 1、表 1）。这一严重的数据供给瓶颈将 RL 限制在窄域之内，使其在线探索和样本效率的天然优势难以在通用推理上释放，成为当前范式升级的核心障碍。

为缓解预训练模型的推理短板，业界常采用**持续预训练**（在专业文档上继续 next‑token prediction 并配合监督微调）或**数据精炼**（如用强语言模型重写文档后再次预训练）。但这些方案仍固守 teacher forcing 范式，迭代需数十亿 token 量级，且缺乏 RL 特有的正向强化与负向惩罚信号，数据利用效率低下。另一方面，高质量 RL 数据传统上依赖强模型（如 GPT‑4）蒸馏，不仅成本高昂，还引入了生成者偏差——蒸馏答案并非直接从训练文档中可验证地产生，削弱了奖励信号的可靠性。可见，业界亟需一套能够**自动、系统化**地将海量预训练文本转化为自包含、可验证问答对的技术路径，从而解除 RL 的数据桎梏，让 RL 在规模与多样性上向预训练看齐。

正是围绕这一缺口，本文提出 **Webscale‑RL** 自动化数据管道。其核心动机在于：若能以极低的成本将预训练文档转换为可验证的 RL 问答对，RL 训练便可挣脱对昂贵标注或蒸馏的依赖，获得与预训练同等丰富的领域分布，进而用远少于 teacher forcing 的 token 消耗实现相当甚至更优的推理表现。Webscale‑RL 通过**过滤‑域分类与角色分配‑QA 生成‑质量防泄漏**四个阶段，将原始文档转换为短答案的问答对；答案直接从文档中提取而非蒸馏自强模型，从根源上降低了偏差并增强了奖励的保真度（第 3‑4 节）。管道产出 120 万对问答，覆盖 9 个以上领域，其语义多样性与现有 RL 数据集相比显著占优（图 3）。基于此数据的 RL 训练在 7 项基准上平均得分超出最强数据精炼基线 3.4 分，与更大规模模型 Qwen2.5‑7B 的性能差距从 10.6 缩窄至 6.1（表 2）；尤值注意的是，RL 仅消耗约 1000 万 token 即达到持续预训练 10 亿 token 才能企及的 MMLU‑pro 和 Big‑Bench 水平，展现出**约 100 倍的数据效率**（图 4）。这一实证有力地表明，解除数据瓶颈后的 RL 训练足以在通用领域逆袭 teacher forcing 范式，为 RL 规模扩展至预训练级别提供了坚实路径。Webscale‑RL 因而不仅是一次数据工程的创新，更意在验证 RL 的样本效率优势在广域任务中依然成立，为后训练范式变革开辟可行性。

## 核心方法与创新机理

### 关键瓶颈与解决思路

当前 RL 训练的根本瓶颈在于**高质量可验证数据的规模与多样性严重不足**：现有 RL 数据集通常不足 100 亿 token，且集中于数学、代码等少数领域，而预训练语料规模超过万亿 token。这一数量级差距导致 RL 无法发挥在线探索优势，通用推理能力受限。

Webscale-RL 的核心因果机制是**将预训练文档的"阅读"任务转换为"问答"任务**，通过自动化管道把海量非结构化文本转化为可验证的 QA 对，直接解除数据供给约束。关键洞察在于：RL 在通用领域同样具备极高的样本效率——仅需约 1/100 的 token 消耗即可匹配持续预训练性能（Figure 4）。

### 三个关键 changed slots

| 维度 | Baseline | Webscale-RL | 证据锚点 |
|:---|:---|:---|:---|
| **数据表示** | 非结构化文本序列（原始文档片段） | 自包含可验证 QA 对，答案直接从文档提取而非蒸馏 | Section 3.2, Figure 2 |
| **训练目标** | Next-token prediction（教师强制，最小化 NLL） | 基于二元奖励的 GRPO：$R(\mathbf{q},\mathbf{a}) \in \{0,1\}$，答案完全匹配即得奖励 | Section 3.1, Formula (1)(2), Table 4 |
| **数据扩展效率** | 需数十亿 token 持续预训练方见显著提升 | 约 1000 万 token（源于原始文档的 RL 数据）达到同等或更优性能，效率提升约 100× | Figure 4, Section 5.2 |

### 四阶段管道机制

管道设计遵循"过滤→结构化→生成→验证"的递进逻辑，核心创新在于**领域驱动的多样性控制**与**答案可验证性保障**：

1. **数据过滤**：启发式规则（<50 tokens 剔除）结合 LLM 判断，去除导航页等非信息性内容
2. **领域分类与角色分配**：LLM 将文档归入具体领域，并为每篇文档分配最多 3 个角色（如医生/患者），以引导多视角提问
3. **可验证 QA 生成**：基于领域专属少样本示例库，LLM 生成问题及简短答案——**答案直接从文档摘取，非从强模型蒸馏**，降低偏差并允许使用成本更低的生成器
4. **质量校验与泄漏控制**：LLM 双重验证答案准确性（对照源文档）及问题自包含性（无答案泄漏）

### 效率优势的实证支撑

- **规模**：产出 120 万 QA 对，覆盖 9+ 领域，来源包括 DCLM（~55 万）、Wikipedia（~35 万）等（Table 1, Table 3）
- **性能**：7 项 benchmark 平均得分 52.1，超越最强基线 GDR（48.7）3.4 分；将 Qwen2.5-3B 与 7B 的差距从 10.6 缩至 6.1（Table 2）
- **效率**：MMLU-pro 上约 1000 万 RL token 匹配约 10 亿持续预训练 token 的性能（Figure 4）

### 局限与待验证点

- 当前二元奖励信号粒度较粗，且依赖生成式奖励模型，推理成本较高（Section 6）
- 数据管道依赖 GPT-4.1/mini，完全开源复现的成本与可访问性受限
- 代码领域性能相对薄弱，可能需要针对性的域平衡策略
- 数据效率对比中的"token 计数"基于原始文档 token 而非模型实际处理 token，存在近似性（fairness notes）

![[assets/figures/papers/iclr26_0014_hOJS9RB1NU_Webscale-RL_Automated_Data_Pipeline_for_Scaling/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the Webscale-RL data pipeline that systematically converts large-scale pretraining data into RL data while preserving the scale and diversity of web data. The pipeline maintains a domain-specific demonstration library for few-shot examples for high quality generation and assigns multiple personas to each document to encourage reflecting different viewpoints. The generated QA pairs are verified for correctness and leakage prevention to ensure the reliability of the RL dataset. The prompt templates of four stage are listed in Appendix B.1.1*

![[assets/figures/papers/iclr26_0014_hOJS9RB1NU_Webscale-RL_Automated_Data_Pipeline_for_Scaling/figures/003_Table_1.jpg]]
*Table 1: The comparison of various datasets with our Webscale-RL dataset. The number of data indicates the number of documents (for pretraining datasets) or the number of QA pairs (for SFT and RL datasets). The scalability indicates the potential of scaling up the dataset size: DeepScaler has low scalability because it is collected from competitions and relies on human annotation. Other post-training datasets generate answers by distillation but they collect queries from limited sources, which limits the further scaling. In contrast, both the questions and answers in the Webscale-RL dataset are converted from and grounded by the pretraining datasets, which can be easily scaled up to pretraining level*

![[assets/figures/papers/iclr26_0014_hOJS9RB1NU_Webscale-RL_Automated_Data_Pipeline_for_Scaling/figures/001_Figure_1.jpg]]
*Figure 1: The scaling on LLM RL is fundamentally bottlenecked by the scarcity of high-quality RL data. While pretraining leverages >1T diverse web tokens, RL datasets remain limited to \<10B tokens with limited diversity. We propose Webscale-RL data pipeline to fundamentally improve the scalability of RL data: we convert the pretraining corpora to verifiable query and ground-truth answer pairs, scaling RL data to pretraining levels while preserving the diversity. The experiments show that RL with Webscale-RL data is significantly more effective and efficient than continual pretraining and data refinement baselines*

大规模语言模型（LLM）的强化学习（RL）训练长期受困于高质量、多样化、可验证问答数据的极度稀缺——现有 RL 数据集的总 token 量不足 10B，且高度集中于数学与代码领域，远逊于预训练语料（>1T）的多样性。Webscale-RL 通过一个**自动化、分阶段的四步管道**，将海量预训练文档系统性转换为数百万个面向不同领域的、包含简短可验证答案的问答对，从而直接解除了 RL 的数据供给瓶颈，将其可扩展性提升至预训练级别（**Figure 1**，**Figure 2**）。

管道的输入为原始互联网文档（如 DCLM、Wikipedia 等，**Table 3**），经过四个顺序模块处理后，最终输出约 1.2M 个覆盖 9+ 领域的 RL 可用问答对（**Table 1**）。四个阶段紧密耦合，共同保障数据的多样性、可验证性和无偏性（**Section 3.2**）：

*   **数据过滤**：引入双重机制——**启发式规则**直接丢弃极短文档（<50 tokens），随后调用 **LLM 过滤器**清除无信息页面（如导航页）与非自包含片段，确保仅信息丰富、独立的文档进入后续流程。
*   **域分类与角色分配**：LLM 将每篇文档归类至具体领域（如医疗、商业），并为每篇文档分配**最多 3 个特定角色**（如医生、患者），以此引导生成视角多样的提问。
*   **可验证 QA 生成**：基于**领域专属少样本示例库**、已分配的角色以及源文档内容，LLM 生成一个自包含的问题（不依赖文档外上下文）与一个**简短、可验证的答案**。答案直接从源文档中摘取，而非由强模型蒸馏产出，从而降低了后端 LLM 的偏置影响（**Section 4.1**）。
*   **质量检查与泄露控制**：最后阶段由 LLM 完成双重校验：①核验答案与源文档一致；②审查问题中是否隐式包含答案（泄露检查），确保奖励信号的可靠性。

该管道在设计上兼顾**规模化潜力与多样性保全**：成本较低的模型（如 GPT‑4.1‑mini）承担域分类与质量校验，生成能力更强的模型（GPT‑4.1）专注 QA 生成，使大规模构建成为可能；同时，通过多域覆盖与多角色视角，保留了原始预训练语料的丰富性（**Figure 3**）。与现有 RL/SFT 数据集相比，Webscale-RL 数据集不仅规模相当（120 万对），更具备本质上的**高可扩展性**——可通过增量添加文档持续扩大，且不依赖昂贵的人工标注或强模型蒸馏（**Table 1**，**Section 4.2**）。

Webscale‑RL 的核心机制是将海量预训练文档自动转换为**可验证的问答对**，从而解除 RL 训练面临的数据规模与多样性瓶颈。该管道通过四个阶段性模块，将非结构化文本重新表示为自包含的问题‑答案对，并利用二元奖励的强化学习目标替代传统的教师强制训练。以下详细描述这四个模块的职责与设计，以及两个关键训练公式的变量含义。

### 数据过滤 (Data Filtering)

- **目的**：去除低质量和非自包含的文档片段，保证后续生成的 QA 对具有可靠的上下文基础。
- **实现**：采用双重过滤策略。首先，启发式规则筛掉 token 数量低于 50 的极短文档；其次，基于 LLM 的二次过滤（使用 GPT‑4.1）识别并丢弃纯导航页面、无信息片段等非有用内容。这一阶段确保进入管道的文档具备生成有意义问答对的最小信息量。
- **证据锚点**：`Section 3.2`，`Stage 1 prompt in Appendix B.1.1`

### 领域分类与角色分配 (Domain Classification & Persona Assignment)

- **目的**：为文档赋予细粒度领域标签和多重视角，引导后续生成多样化的提问。
- **实现**：对通过过滤的每一篇文档，使用 LLM（GPT‑4.1‑mini）将其归类到具体领域（例如商业、医疗、技术），同时为每篇文档分配最多 3 个角色（如医生、患者、记者）。这些角色在后续 QA 生成中充当提问者身份，促使模型围绕同一文档内容从不同专业视角构造问题，极大提升了问题的覆盖面和多样性。
- **证据锚点**：`Section 3.2`，`Stage 2 prompt in Appendix B.1.1`

### 可验证的 QA 生成 (Verifiable QA Generation)

- **目的**：基于处理过的文档和角色，生成自包含且答案可直接从文档中提取的问答对。
- **实现**：利用领域专属的少样本示例库（即预设的示范问答）和分配的角色，LLM（GPT‑4.1）从源文档中抽取关键信息，生成问题及其简短、可验证的答案。答案严格来源于源文档文本，而非由 LLM 自行推理或概括（即非蒸馏式生成），以此降低生成器偏差和对强模型的过度依赖。生成的问题被设计为自我包含（无需额外上下文即可理解），这为后续 RL 训练中的奖励验证提供了便利。
- **证据锚点**：`Section 3.2`，`Stage 3 prompt in Appendix B.1.1`，`Appendix B.2.1 example`

### 质量检查与泄漏控制 (Quality Check & Leakage Control)

- **目的**：确保生成的 QA 对答案正确且问题本身不含答案信息，防止 RL 训练中的“答案泄漏”。
- **实现**：再次调用 LLM（GPT‑4.1‑mini）执行两重校验：第一，基于源文档核对每个答案的准确性；第二，检查问题的措辞是否隐式地包含了答案（泄漏检查），一旦发现泄露即丢弃该 QA 对。该阶段是保证奖励信号可靠性的关键——因为 RL 训练使用精确匹配奖励，任何泄漏都会导致奖励失真。
- **证据锚点**：`Section 3.2`，`Stage 4 prompt in Appendix B.1.1`

---

### 关键公式与变量含义

Webscale‑RL 的总体设计可以抽象为两个核心训练目标：标准预训练阶段的负对数似然最小化，以及 RL 微调阶段的期望奖励最大化。

#### 预训练负对数似然目标
$$
\min_{\theta} \ - \mathbb{E}_{\mathbf{x} \sim \mathcal{D}_{\text{pretraining}}} \left[ \sum_{t=1}^{T} \log P_{\theta}(x_t \mid \mathbf{x}_{(<t)}) \right]
$$
- $\theta$：模型参数。
- $\mathbf{x}$：从预训练数据分布 $\mathcal{D}_{\text{pretraining}}$ 中采样的一条文本序列。
- $T$：序列长度。
- $x_t$：序列在位置 $t$ 的 token。
- $\mathbf{x}_{(<t)}$：位置 $t$ 之前的所有 token（语境）。
- $P_{\theta}(x_t \mid \mathbf{x}_{(<t)})$：模型在给定上文时生成下一个 token 的条件概率。

该目标的含义是：模型以**教师强制**方式最小化预测下一 token 的负对数似然，本质上是在模仿预训练语料中的 token 分布。

#### RL 目标与二元奖励
$$
\max_{\theta} \ \mathbb{E}_{\mathbf{q} \sim Q, \, \mathbf{a} \sim P_{\theta}(\cdot \mid \mathbf{q})} \left[ R(\mathbf{q}, \mathbf{a}) \right]
$$
- $\theta$：模型参数（策略网络）。
- $Q$：由 Webscale‑RL 管道生成的问题集（分布）。
- $\mathbf{q}$：从 $Q$ 中采样的一个问题。
- $P_{\theta}(\mathbf{a} \mid \mathbf{q})$：模型在给定问题 $\mathbf{q}$ 下生成答案 $\mathbf{a}$ 的策略（概率分布）。
- $R(\mathbf{q}, \mathbf{a})$：二元奖励函数，当模型生成的答案与管道提供的标准答案**完全匹配**时取 $1$，否则取 $0$。

该目标的含义是：RL 训练最大化期望奖励，模型自主探索如何生成与标准答案完全一致的回复。由于奖励信号仅依赖最终答案的正确性，这一设计既保持了训练的简洁性，又因其严格的可验证性而有效驱动模型学习问题到答案的直接映射。

上述公式与管道模块紧密联动：管道产出的高质量 $\mathbf{q}$‑$\mathbf{a}$ 对直接充当 RL 的查询集和奖励基准，而公式（2）定义的约束迫使模型在稀疏奖励下压缩推理路径，最终实现了远超传统预训练的数据效率。

## 实验与关键发现

### 主实验结果
Webscale-RL 在 7 项基准（MMLU‑pro, Big‑Bench, GPQA‑D, MATH500, GSM8K, MBPP, EvalPlus）上的平均得分为 52.1，较最强基线 GDR（48.7）提升 3.4，较持续预训练+SFT 的次优结果 (48.3) 高出 3.8（Table 2）。该方案将 Qwen2.5‑3B 与 Qwen2.5‑7B 之间的平均性能差距从 10.6 压缩至 6.1，缩小幅度达 42%。在数学推理任务上优势突出：MATH500 达到 58.0，较 3B 基础模型提高 13.6，仅比 7B 模型 (60.8) 低 2.8；GSM8K 达到 78.5，较基础模型提升 4.3。知识密集型任务（MMLU‑pro、Big‑Bench）亦获得一致改善。上述结果表明，将预训练文档转化为可验证 QA 对后，RL 训练能够突破原有领域局限，仅需极少数据即可实现广泛的能力提升。

### 数据效率与缩放分析
Figure 4 的缩放曲线揭示了 RL 的数据效率优势：在 MMLU‑pro 上，RL 训练仅需约 1 千万 token（由>1000 篇文档生成）即可达到与持续预训练约 10 亿 token 相当的分数（~43 分）；在 Big‑Bench 上亦呈现相同趋势，同等分数水平下令牌消耗降低约两个数量级。这一增益源于 RL 直接优化答案正确性的二元奖励，而预训练仅对下一个 token 进行无区分模仿——RL 能够用更少的数据提取出文档中的关键推理信息。随着数据量增加，RL 收益持续提升且未饱和，表明 Webscale‑RL 具备向预训练级别规模扩展的潜力。

### 失败模式与局限性
实验同时暴露出以下瓶颈：

- **二元奖励的粗糙性**：RL 仅依据生成答案与标准答案的精确匹配给出 0/1 反馈，导致奖励稀疏，部分正确的推理过程无法获得正向信号，增加了训练难度并可能减缓收敛。这或许是 MATH500 仍需较多训练步数才能完全匹配 7B 模型的原因之一。
- **领域表现不均衡**：代码类基准（MBPP、EvalPlus）的改善幅度相对较小（Table 2）。Webscale‑RL 数据中代码文档占比较低（Figure 3 左），且 QA 格式未充分覆盖代码生成与调试的多样化模式，提示后续需针对性调整领域平衡。
- **对商业 LLM 的依赖**：管道调用 GPT‑4.1/mini 进行过滤、生成与校验，导致较高的外部成本和可复现门槛。尽管论文提及开源模型有望替代，但当前未提供基于开源生成器的等效对比。
- **答案简洁性限制**：QA 对强调答案直接选自文档且简短，模型在需要长链推理的任务上缺少中间步骤示范，RL 探索起点更困难，可能拖累复杂推理任务的收敛效率。
- **消融实验缺失**：本文未对各管道模块（过滤、角色分配、质量检查等）进行单独消融，因此难以归因性能增益的主要来源及各组件的贡献度。

![[assets/figures/papers/iclr26_0014_hOJS9RB1NU_Webscale-RL_Automated_Data_Pipeline_for_Scaling/figures/005_Table_2.jpg]]
*Table 2: Comparison results of our Webscale-RL with baselines on various benchmarks. To mitigate evaluation bias, continual pretraining and data refinement baselines are followed by SFT training to enhance instruction following. While all finetuning are based on the Qwen2.5-3B model, we also compare with the 7B base model. Blue bold indicates the best result among 3B baselines; green bold shows where we match or exceed the 7B model*

### 核心图表结论
- **Table 2**：Webscale‑RL 在所有 3B 基线中取得最优，且在 MATH500 和 GSM8K 上超越 7B 模型，验证了 RL 训练结合自动化 QA 管道在通用推理上的有效性与数据效率。
- **Figure 4**：直观展示 RL 相较于持续预训练的 token 效率优势，支持“将预训练资源转换为 RL 格式可成倍降低数据需求”的核心结论。
- **Table 1**：Webscale‑RL 数据集以 1.2M QA 对覆盖 9+ 领域，其扩展性远超现有 RL/SFT 数据集，从数据端保障了 RL 向预训练规模的迈进。

![[assets/figures/papers/iclr26_0014_hOJS9RB1NU_Webscale-RL_Automated_Data_Pipeline_for_Scaling/figures/008_Figure_4.jpg]]
*Figure 4: Scaling comparison between Webscale-RL training and continual pretraining with the original pretraining corpora. We report the performances on MMLU-pro (left), Big-Bench (middle) and average on all benchmarks (right). The token number for RL training is calculated based on the original pretraining corpus used to generate the Webscale-RL dataset. The each data point in continual pretraining baselines are followed by a SFT training using the same 10K high-quality examples. The RL training on Webscale-RL consistently outperforms continual pretraining at different training scales and exhibits better scaling efficiency*

![[assets/figures/papers/iclr26_0014_hOJS9RB1NU_Webscale-RL_Automated_Data_Pipeline_for_Scaling/figures/011_Table_3.jpg]]
*Table 3: Source distribution of the Webscale-RL dataset (∼1.2M total QA pairs)*

## 定位与知识库关联

Webscale-RL 在方法谱系中位于**以数据为中心的强化学习后训练路线**，其核心贡献在于将 RL 训练的数据供给从手动标注或强模型蒸馏的有限规模，系统性地扩展到与预训练体量相匹配的水平。在此之前的代表性基线可分为两类：一类是持续预训练（Continual Pretraining）及其衍生数据精炼方法（如 GDR、QuRating、ProX），它们沿用下一 token 预测目标，本质上仍属于教师强制范式，无法利用 RL 的在线探索与试错优势；另一类是以 Nemotron 等为代表的现有 RL/SFT 数据集，规模普遍小于 10B tokens 且领域集中在数学、代码等少数方向，难以支撑通用推理能力的广泛提升（Figure 1, Table 1）。Webscale-RL 通过两个关键变量的改变打破了这一僵局：**数据表示**从非结构化文档序列转变为自包含、可验证的问答对，**训练目标**从负对数似然最小化转变为基于二元奖励的策略优化。这一“表示-目标”组合的切换，使得原本在预训练数据上效果有限的 RL，能以极低的 token 消耗（约 100 倍效率差距，Figure 4）达到甚至超过持续预训练的性能，同时在平均得分上以 52.1 超过最强数据精炼基线 GDR 的 48.7，并将与 Qwen2.5-7B 的性能差距从 10.6 压缩至 6.1（Table 2）。值得注意的是，与依赖强 LLM 蒸馏生成答案的合成数据管道不同，Webscale-RL 的答案直接从源文档提取而非蒸馏，降低了上游模型偏差，并使成本较低的生成器成为可能（Section 4.1）。这些改进确立了它在 RL 数据扩展路线中的独特定位：**不是替代预训练，而是提供一种在后训练阶段以极高样本效率注入多样化世界知识的全新范式**，尤其适用于那些原始文档中蕴含的可验证事实或明确结论的知识迁移场景。

然而，该方法存在明确的**适用边界**。管道成功的前提是源文档包含自包含、可短答验证的信息——百科类、教科书式、实用指南类的文本最为匹配；对于高度主观、抽象或依赖长程上下文暗示的内容，LLM 难以生成高质量的可验证问答对，数据产出率与质量会急剧下降。任务层面，当前管道在对知识依赖较强的基准（MMLU-pro、Big-Bench）和数学推理（MATH500、GSM8K）上提升显著，但在代码类任务上仍相对薄弱（Table 2），这主要归因于代码问题的正确性往往需要执行验证而非表面短答，且源数据中代码文档的覆盖度可能不足。在规模与复现性上，当前实验基于 3B 模型，虽展现出良好的缩放趋势，但当模型规模或领域极度扩充时，二元奖励信号的稀疏性和流水线对商用 LLM（GPT-4.1/mini）的依赖都会成为瓶颈，使其在开源社区或资源受限场景下的直接迁移存在障碍。

从机制角度看，**主要局限**集中在以下方面。其一，采用生成式二元奖励（只判断生成答案与标准答案的完全匹配）会忽略部分正确或中间推理步骤的质量，造成奖励信号过于稀疏且容易因表述差异而误判，同时奖励模型自身的推理也增加了训练成本（Section 6）。其二，管道四个阶段目前强依赖 GPT-4.1 和 GPT-4.1-mini，尽管使用了少样本示例库和答案提取策略来控制质量，但整体产线的开放可复现性和经济成本仍受制于商业 API。其三，领域分布不均衡——尽管覆盖了 9 个以上的领域，但代码、深层科学推理等需要多步推导的子领域性能依然欠佳（Table 2），表明管道需要更精细的域平衡和评价机制。其四，生成的问答对答案天然追求简洁，对于需要复杂思维链的任务，模型在 RL 训练中需从零探索推理路径，训练难度与不稳定性增加，这也部分解释了为何在需要长推理的任务上提升幅度有限。

基于上述分析，**若干重要的开放问题**有待后续工作解决。第一，如何设计更高效的奖励机制，例如过程奖励、部分匹配奖励或置信度校准的软奖励，以在保持验证可靠性的前提下降低奖励模型推理成本并加速训练收敛？第二，管道的不同阶段是否可以合并或重组（如将域分类与角色分配合一、减少泄漏检查比例）以提升吞吐量，且域分布与角色策略是否存在可预测的最优配置？第三，Webscale-RL 生成的 QA 数据能否与原始预训练文本混合进行联合训练，从而同时收获预训练的泛化表征和 RL 的定向优化收益？第四，能否将管道完全适配到强大且开源的大语言模型（如 DeepSeek 系列、LLaMA 3），使其彻底摆脱商业 API 依赖，实现全开源复现？第五，当 QA 规模扩展至数亿级别时，RL 训练的效率增益能否继续保持线性甚至超线性，是否需要开发分布式 RL 和奖励近似策略？最后，在管道未见过的领域（如多模态理解、工具使用）上，通过 Webscale-RL 数据训练的模型是否能涌现出出人意料的能力，亦或是暴露更深层的表示缺陷，仍是值得深入探索的命题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Webscale_RL_Automated_Data_Pipeline_for_Scaling_RL_Data_to_Pretraining_Levels.pdf]]
