---
title: "AbstRaL: Augmenting LLMs' Reasoning by Reinforcing Abstract Thinking"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AbstRaL_Augmenting_LLMs_Reasoning_by_Reinforcing_Abstract_Thinking.pdf
aliases:
- AbstRaL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过强化学习训练模型生成问题的符号抽象（抽象思维），使推理过程与具体上下文解耦，从而对表面形式变化不敏感。"
primary_logic: "直接学习问题的抽象模式而非通过数据增强，结合符号推导，能显著提升推理的稳健性和跨任务泛化能力。"
claims:
- "AbstRaL在GSM-Symbolic的Vary Both测试中几乎完全恢复了因分布偏移导致的性能下降。"
- "在GSM-Plus Distract测试中，AbstRaL在Qwen2.5-Math-7B上的准确率比CoT-8S高出6个百分点（82.3% vs 76.3%）。"
- "移除GranulAR精细抽象数据导致Distract准确率从82.3%骤降至66.8%，证实了精细抽象推理格式的关键作用。"
- "GSM-Symbolic 上 Vary Both Accuracy (%) = 44.6"
---

# AbstRaL: Augmenting LLMs' Reasoning by Reinforcing Abstract Thinking

> [!tip] 核心洞察
> 直接学习问题的抽象模式而非通过数据增强，结合符号推导，能显著提升推理的稳健性和跨任务泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AbstRaL：通过强化抽象思维增强大语言模型推理能力 |
| 英文题名 | AbstRaL: Augmenting LLMs' Reasoning by Reinforcing Abstract Thinking |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=49vo7D9LbI) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AbstRaL |
| Dataset | GSM-Symbolic, GSM-Plus, MATH (OOD) |

> [!tip] 效果简介
> - GSM-Symbolic 上，Vary Both Accuracy (%) 为 44.6，对比 36.8 (SyReLM)，变化 +7.8。
> - GSM-Plus 上，Distract Accuracy (%) 为 82.3，对比 76.3 (CoT-8S)，变化 +6.0。
> - MATH (OOD) 上，Zero-shot Accuracy (%) 为 34.7，对比 30.0 (Ori-SFT)，变化 +4.7。

## 概述

大语言模型在小学数学推理任务中面临分布偏移时表现出显著的脆弱性：输入中的数值变化或干扰条件插入即可导致推理准确率大幅下滑，这一问题在小规模模型上尤为突出。AbstRaL 针对该瓶颈提出一种直接学习问题底层抽象的方法：通过强化学习训练模型在推理前先生成输入条件的符号抽象，使后续推理与具体上下文解耦，从而对表面形式的扰动不敏感。

与依赖数据增强的路线不同，AbstRaL 的核心洞察在于"学习抽象模式"本身即可替代海量数据扩充。Figure 1 示意了同一抽象 $A$ 可同时为不同措辞的查询提供一致的求解结构，奠定了方法动机。在方法定位上，AbstRaL 构建了四步抽象推理流程——条件识别 (Condition Recognition)、抽象推理 (Abstract Reasoning)、抽象检索 (Abstraction Retrieval) 和符号推导 (Symbolic Derivation)——并在 GranulAR 精细分解数据上进行监督微调后，进一步引入模型无关的抽象奖励（符号距离奖励 $r_{symbolic}$ 与答案正确性奖励）进行强化学习优化。

主要结果验证了该方案的有效性：在 GSM‑Symbolic 的 Vary Both 测试中，AbstRaL 在 Qwen2.5‑0.5B‑Instruct 上达到 44.6% 的准确率，较大幅领先次优基线 SyReLM（36.8%）；在 GSM‑Plus Distract 测试中，Qwen2.5‑Math‑7B‑Instruct 的准确率从 CoT‑8S 的 76.3% 提升至 82.3%（Table 1）。消融实验进一步锁定关键组件：移除 GranulAR 精细抽象格式导致 Distract 准确率从 82.3% 骤降至 66.8%，证实精细抽象推理格式是方法改进的主要贡献源（Table 2）。

## 背景与动机

当前大语言模型（LLM）在执行小学数学推理（如GSM风格习题）时，往往依赖题目中特定的数值和表达方式，导致其推理过程对表面形式的变化高度敏感。具体而言，当问题中的相关数值、实体名称发生替换，或插入无关的干扰条件时，模型性能会显著下降，这种由于分布偏移带来的脆弱性在规模较小的模型上尤为突出（§1, Figure 2）。传统的链式思考（CoT）等推理范式虽然在标准测试中取得不错效果，但其思考链条仍紧密绑定于具体上下文，面对GSM-Symbolic和GSM-Plus这类专门考察鲁棒性的基准时，往往出现较大的准确性滑坡。

已有工作尝试通过数据增强——生成大量变体问题来扩充训练集——来缓解这一问题。然而，这种做法本质上仍停留在"实例"层面：模型学习的是更多样的表面实例，而非剥离具体语境、提取问题不变结构的能力（Figure 3(a)）。与之相对，人类在解决类似数学文字题时，常会自然地将"小明有5个苹果，吃掉了2个"抽象为"初始数量为 $a$，减少 $b$"并推导剩余量，从而无视具体人名和数字。受此启发，本工作提出一个直接训练LLM进行**抽象思维**的思路：将数学问题中的具体数值和情境符号化，在抽象空间中完成推理，最后通过符号求解器得到最终答案。这一思路的根本优势在于，推理步骤本身不再与表面形式耦合，因而对分布偏移具有内在的抗干扰能力。

如图（Figure 1）所示，两个措辞不同但本质相同的问题共享一个抽象模式 $A$；若能学会从具体问题 $X$ 中构建抽象 $A$，并在该抽象层面进行推理，便可同时解决所有具有同一抽象结构的实例。图（Figure 3(b)）将这一策略与数据增强进行了对比：前者直接学习底层的抽象结构，有望从根本上提升模型应对分布变化的稳健性。

然而，端到端地激发LLM的抽象思维面临两个关键缺口。其一，现有面向抽象推理的方法（如 Chain of Abstraction、Abstract of Thought）或依赖于严格的手工规则，或仅将符号工具作为后处理步骤，缺少一种自然语言与符号思考深度融合、可被模型自主学习的表示格式。其二，缺乏一种有效的训练机制来确保生成的抽象既忠实于问题原义，又能被后续的符号推导正确利用。为此，本文提出AbstRaL框架，设计了一种细粒度分解的抽象推理数据格式（GranulAR），并引入基于抽象奖励的强化学习策略，使LLM在监督微调之后进一步学会生成高质量、可执行的符号抽象，从而弥补上述缺口，显著提升推理的鲁棒性与跨任务泛化能力。

## 核心创新

AbstRaL 的出发点直指当前大语言模型在小学数学习题（GSM）推理中的一个关键瓶颈：**对分布偏移（数值改变、干扰项插入等）的稳健性极差，尤其在小型模型中更为突出**。现有方法基于隐式数据增强（如修改表面形式产生更多训练样本）并不能从根本上解耦推理与具体上下文的耦合。AbstRaL 的核心洞察是：**直接让模型学习问题的符号抽象——一种不依赖表面形式的"抽象思维"，并通过符号推导得出答案——可以显著提高推理的稳健性与跨任务泛化能力**。这一创新并非简单蒸馏更强的模型知识，而是改变了学习目标本身：从学习"一题一解"的实例，转向学习**可跨实例共享的抽象推理模式**（图 1 中的共享抽象 `A` 呼应了这一思想）。

为实现上述目标，AbstRaL 在三个关键维度上改变了 Baseline 的"标准配方"（Changed Slots）：

### 1. 训练数据格式：从 Socratic CoT 到 GranulAR 精细抽象推理

Baseline 使用普通的 Socratic Chain-of-Thought 数据，而 AbstRaL 采用精心构造的 **GranulAR 抽象推理数据**（§3.1）。GranulAR 要求模型将输入问题中的数值替换为抽象符号 `[in0]`、`[in1]`…，再分解为子问题，并用这些抽象符号写出多步推理，最后以符号形式给出最终答案。这一格式迫使模型在"去上下文化"的级别上做出整体规划，而非在表面文字中顺势推导。

**决定性证据**：在 GSM-Plus *Distract* 测试中，完整 AbstRaL 相较于 CoT‑8S 准确率提升了 6 个百分点（Qwen2.5‑Math‑7B：82.3% vs 76.3%，表 1）。若在消融中**移除 GranulAR 格式**，仅用普通抽象数据，*Distract* 准确率立刻从 82.3% 暴跌至 66.8%（表 2），证明精细抽象推理格式是抵御干扰条件的关键所在。

### 2. 训练方法：从纯 SFT 到 SFT + 强化学习（抽象奖励）

Baseline 依赖监督微调（SFT）让模型模仿推理过程，而 AbstRaL 通过**强化学习（RL）与模型无关的抽象奖励**（§3.2）进一步提升抽象生成的忠实度。RL 奖励由两部分组成：

- **答案正确性奖励**（解算最终数值是否正确）；
- **符号距离奖励**（式 (1)）：
  $$r_{symbolic}(\widetilde{A}, A) = r_{max} \cdot \Big(1 - \frac{\mathrm{EditDistance}(\widetilde{A}, A)}{\max_{a \in \{\widetilde{A}, A\}} \mathrm{Len}(a)}\Big)$$

  通过归一化编辑距离衡量生成抽象序列与目标抽象之间的相似性，从而引导模型输出更紧凑、更准确的符号推理链。

消融实验表明，单独保留 SFT 而不用 RL，整体性能显著低于完整 AbstRaL（表 2），说明 RL 对最终稳健性有独立贡献。

### 3. 推理范式：从单步生成到四步抽象‑求解流程

Baseline（如 CoT）直接生成自然语言推理并给出答案；AbstRaL 引入了一个结构化的四步推理流程（§3）：

1. **条件识别**：识别数值并用抽象符号替换，生成抽象问题 $\chi^A$；
2. **抽象推理**：基于 GranulAR 格式生成包含子问题分解的抽象答案 $y^A$；
3. **抽象检索**：从 $y^A$ 中通过正则匹配提取抽象数学表达式（符号推导链）；
4. **符号推导**：将抽象表达式结合具体条件输入 SymPy 求解器，获得最终答案。

这一范式将"理解问题→规划求解"显式拆分开来。若删除其中的中间抽象上下文（w/o Contexts），小模型在 GSM‑Symbolic *Vary Both* 上的准确率从 44.6% 一路掉到 23.1%（表 2），表明**衔接自然语言与纯符号的中间表示是抽象思维可信赖的关键**。

---

**总结**：AbstRaL 的关键创新并非增加数据量或更换模型，而是通过改变数据格式、训练目标与推理结构，将"学会抽象"本身作为优化目标。这也解释了其在核心 benchmark 上的决定性提升：几乎完全恢复因分布偏移导致的性能退化（GSM‑Symbolic *Vary Both* Δ 仅 −1.27%，表 1），并在跨分布任务上展现出稳定的零样本泛化能力（MATH OOD 提升 4.7%，表 3）。这一从"表象拟合"到"底层模式学习"的转变，构成了 AbstRaL 方法的核心引擎。

## 整体框架

![[assets/figures/papers/iclr26_0005_49vo7D9LbI_AbstRaL_Augmenting_LLMs_Reasoning_by_Reinforcing/figures/005_Figure_4.jpg]]
*Figure 4: Overview of GranulAR training data construction, which consists of an instance rewriting procedure to rewrite existing socratic CoT data $($\mathcal{X}, \mathcal{Y}$)$ into fine-grained abstract reasoning data $($\chi^{\mathcal{A}}, \mathcal{C}, \mathcal{y}^{\mathcal{A}}, \mathcal{A}$)$, followed by a answer verification procedure to check the correctness of rewriting

AbstRaL 的整体 pipeline 围绕一个核心洞察展开：让模型直接学习问题的**抽象模式**，而非依赖数据增强来覆盖表面形式的变化。如图3(b)所示，框架由四个顺序执行的模块构成，形成一条从具体问题到符号推导的完整推理链。

### 1. 条件识别 (Condition Recognition)

该模块负责将输入问题中的具体数值替换为抽象符号，生成抽象问题 $\mathcal{X}^A$ 以及对应的条件映射 $\mathcal{C}$（如 `[in0]=5`, `[in1]=3`）。这一步实现了问题与具体上下文的**解耦**，为后续的抽象推理提供干净的符号化输入。

### 2. 抽象推理 (Abstract Reasoning)

这是框架的核心模块。模型基于 GranulAR 数据格式（§3.1），在抽象问题 $\mathcal{X}^A$ 上生成包含符号占位符和子问题分解的抽象答案 $\mathcal{y}^A$。GranulAR 格式的关键在于将问题先分解为子问题列表，再用链式思维逐步推导，最终以抽象符号表述结论。这种精细化的推理链使模型能够进行**全局规划**，从而在面对干扰条件时保持推理的稳健性。

### 3. 抽象检索 (Abstraction Retrieval)

从生成的抽象答案 $\mathcal{y}^A$ 中，通过正则匹配提取出数学推导表达式——即抽象化后的推导过程 $\mathcal{A}$。这些表达式是连接自然语言推理与符号求解器的桥梁。

### 4. 符号推导 (Symbolic Derivation)

利用上一步提取的抽象表达式 $\mathcal{A}$ 以及条件识别模块提供的具体条件 $\mathcal{C}$，调用 SymPy 符号求解器进行精确计算，得到最终数值答案。实验表明，框架的主要增益来自抽象推理的学习，而非符号工具本身——去除工具仅导致微小的性能下降。

### 训练与数据构建管线

支撑上述推理流水线的是**两阶段训练**与**数据重写**机制：

- **GranulAR 数据构建**（Figure 4）：将现有的 Socratic CoT 数据 $(\mathcal{X}, \mathcal{Y})$ 重写为抽象推理数据 $(\mathcal{X}^A, \mathcal{C}, \mathcal{y}^A, \mathcal{A})$。流程包括：(1) 条件识别生成抽象问题与条件；(2) Oracle LLM 将金子答案重写为 GranulAR 格式的抽象答案；(3) 抽象检索与符号推导验证重写的正确性。

- **SFT + RL 训练**：先使用 GranulAR 数据进行监督微调（SFT），再通过强化学习（RL）进一步提升抽象生成的忠实度。RL 阶段引入与模型无关的抽象奖励（§3.2），包括**答案正确性奖励**和**符号距离奖励**（公式1），其中符号距离奖励计算生成抽象与目标抽象之间的归一化编辑距离：
  $$r_{symbolic}(\widetilde{A}, A) = r_{max} \cdot \Big(1 - \frac{\mathrm{EditDistance}(\widetilde{A}, A)}{\max_{a \in \{\widetilde{A}, A\}} \mathrm{Len}(a)}\Big)$$

这一整体设计使得 AbstRaL 能够将分布偏移（如数值变化、干扰项插入）对推理性能的影响降至接近零——在 Qwen2.5-0.5B 上实现 Δ 仅 -1.27% 的性能退化恢复，并在 GSM-Plus Distract 测试中较 CoT-8S 提升 6 个百分点。消融实验证实，移除 GranulAR 精细抽象推理格式会导致 Distract 准确率从 82.3% 骤降至 66.8%，直接验证了该格式作为框架关键组件的决定性作用。

## 核心模块与公式推导

AbstRaL 框架遵循"先抽象、后推导"的四步推理流水线，并与 GranulAR 精细抽象数据及强化学习奖励机制紧密耦合。

### 四步推理流程

1. **条件识别 (Condition Recognition)**
   将问题中的具体数值替换为抽象符号（如 `[in0]`，`[in1]`），生成抽象问题 $\chi^A$ 并提取条件 $\mathcal{C}$。该步骤在数据构造阶段由 Llama‑3.3‑70B‑Instruct 通过少量示例提示完成，推断时由模型自身执行。

2. **抽象推理 (Abstract Reasoning)**
   基于 GranulAR 数据的分解范式，模型首先生成一系列子问题，然后对每个子问题以包含抽象符号的思维链方式回答，最终输出抽象答案 $\mathcal{y}^A$ 和抽象表达式 $\mathcal{A}$。

3. **抽象检索 (Abstraction Retrieval)**
   从抽象答案中通过正则匹配提取纯符号推导链（各抽象表达式的推导关系），将其与具体条件隔离，供符号求解器消费。

4. **符号推导 (Symbolic Derivation)**
   将提取的符号表达式与条件 $\mathcal{C}$ 送入 SymPy 符号求解器，得出最终数值答案。实验显示，推理鲁棒性的提升主要来自抽象推理的学习，而非符号工具本身。

### GranulAR 数据格式

训练样本由四元组 $\big(\chi^{\mathcal{A}}, \mathcal{C}, \mathcal{y}^{\mathcal{A}}, \mathcal{A}\big)$ 构成：

- $\chi^{\mathcal{A}}$：将具体问题数词替换为抽象符号后的抽象问题；
- $\mathcal{C}$：条件，即各符号对应的具体数值；
- $\mathcal{y}^{\mathcal{A}}$：抽象答案，包含分解后的子问题、带符号的思维链推导及最终抽象输出符号；
- $\mathcal{A}$：抽象表达式链，即 $\mathcal{y}^{\mathcal{A}}$ 中通过正则匹配提取到的纯符号推导步骤。

数据构造流程为：先用 oracle LLM 将标准苏格拉底 CoT 答案重写为 GranulAR 格式，再通过抽象检索和符号求解验证一致性，确保数据正确性。

### 强化学习中的抽象奖励

AbstRaL 在 SFT 之上引入两组模型无关奖励，促使模型生成更忠实的抽象：

- **答案正确性奖励** $r_{\text{answer}}$：将生成的抽象 $\widetilde{A}$ 与条件 $\mathcal{C}$ 送入符号求解器，若结果与真实答案一致则给予正向奖励。

- **符号距离奖励** $r_{\text{symbolic}}$：度量生成抽象 $\widetilde{A}$ 与真实抽象 $A$ 在 token 级别上的归一化编辑距离相似度，公式为：

  $$r_{\text{symbolic}}(\widetilde{A}, A) = r_{\max} \cdot \Big(1 - \frac{\mathrm{EditDistance}(\widetilde{A}, A)}{\max_{a \in \{\widetilde{A}, A\}} \mathrm{Len}(a)}\Big)$$

  其中 $\mathrm{EditDistance}(\cdot,\cdot)$ 计算两 token 序列的编辑距离，$\max_{a \in \{\widetilde{A}, A\}} \mathrm{Len}(a)$ 为两序列中较长的长度，$r_{\max}$ 为最大奖励上限。该奖励鼓励模型生成的抽象表达式与目标抽象在结构上高度相近。

### 策略优化目标

训练采用 Group Relative Policy Optimization (GRPO) 目标，内嵌抽象奖励。对每个抽象问题 $\mathcal{X}^A$，从当前策略 $\pi_{\theta}$ 采样 $G$ 个抽象输出 $\widetilde{\mathcal{V}_i^A}$，组内相对优势 $R_i$ 由答案正确性与符号距离奖励组合后经组归一化得到：

$$R_i = \frac{r_i - \mathrm{mean}\big(\{r_1, r_2, \ldots, r_G\}\big)}{\mathrm{std}\big(\{r_1, r_2, \ldots, r_G\}\big)},$$

$$r_i = r_{\text{answer}}(\widetilde{A}_i, \mathcal{C}, \mathrm{Ans}) + r_{\text{symbolic}}(\widetilde{A}_i, \mathcal{A}).$$

最终 GRPO 目标函数为：

$$\frac{1}{G} \sum_{i=1}^G \left( \min\left( \frac{\pi_{\theta}(\overline{\mathcal{V}_i^A} \mid \mathcal{X}^A)}{\pi_{\theta_{\text{old}}}(\overline{\mathcal{V}_i^A} \mid \mathcal{X}^A)} R_i,\; \operatorname{clip}\!\left( \frac{\pi_{\theta}(\overline{\mathcal{V}_i^A} \mid \mathcal{X}^A)}{\pi_{\theta_{\text{old}}}(\overline{\mathcal{V}_i^A} \mid \mathcal{X}^A)}, 1-\varepsilon, 1+\varepsilon \right) R_i \right) - \beta\,\mathbb{D}_{\text{KL}}(\pi_{\theta} \| \pi_{\text{ref}}) \right),$$

式中 $\pi_{\theta_{\text{old}}}$ 为更新前策略，$\pi_{\text{ref}}$ 为仅经 SFT 训练的策略，$\beta$ 控制 KL 惩罚强度，$\varepsilon$ 为裁剪超参数。该目标在稳定策略更新的同时，直接优化抽象表达的准确度与结构一致性。

## 实验与分析

### 主实验结果

我们在 GSM 推理鲁棒性基准 GSM-Symbolic（条件变化）和 GSM-Plus（干扰项插入）上评估了 AbstRaL。结果表明，模型无关的显式抽象学习（数据增强仅做同分布泛化）能系统性地缓解分布偏移下的性能退化，且这一收益在不同模型规模上均成立。图 2 展示了所测 LLM 的整体趋势，Table 1 给出了 Qwen 系列的代表性数值。


![[assets/figures/papers/iclr26_0005_49vo7D9LbI_AbstRaL_Augmenting_LLMs_Reasoning_by_Reinforcing/figures/003_Figure_2.jpg]]
*Figure 2: Our AbstRaction Learning (AbstRaL) method effectively improves GSM reasoning robustness of LLMs, especially facing the variations of relevant input conditions and the interference of distracting conditions. We present average accuracy of all our tested LLMs on GSM-Plus (Li et al., 2024), including the original GSM8K testing set (Original Reasoning Problem), the testing sets with numerical variations (Vary Relevant Conditions), averaged across three portions (digit expansion, integer-decimal-fraction conversion and numerical substitution), the testing set with problem rephrasing (Vary Problem Contexts) and with distractor insertion (Add Distracting Conditions)*

![[assets/figures/papers/iclr26_0005_49vo7D9LbI_AbstRaL_Augmenting_LLMs_Reasoning_by_Reinforcing/figures/007_Table_1.jpg]]
*Table 1: Evaluation results of GSM reasoning robustness, measured by the accuracy (%) of final answer. ∆ denotes the relative percentage of drop comparing performance on Vary Both to performance on Origin 100. Num. Pert. denotes the average performance on the three GSM-Plus testing sets that perturb input numbers (i.e., Digit Ex., Int-Dec-Fra and Num. Sub.). Best results on each model are bold, where lower is better for ∆. Standard deviation (std) of multi-round evaluation results on Vary Both are in brackets, where lowest std on each model are underlined*

在 Qwen2.5‑0.5B‑Instruct 上，AbstRaL 在 Vary Both 条件下取得 44.6% 的准确率，比最佳基线 SyReLM（36.8%）高出 7.8 个百分点，而 CoT‑8S 仅为 34.6%。更具信息量的是相对退化指标 Δ：AbstRaL 的 Δ 为 -1.27%，意味着其 Vary Both 性能甚至略高于 Origin 100 的参考线，而其他方法的 Δ 均为正且绝对值更大（Table 1）。在 Qwen2.5‑Math‑7B‑Instruct 上，这一趋势同样成立：AbstRaL 的 Distract 准确率达到 82.3%，比 CoT‑8S（76.3%）高 6 个百分点，对应的 Vary Both 退化 Δ 仅为 0.86%，远低于竞争方法。跨模型扩展结果（Table 5 和 Table 6）进一步证实，AbstRaL 在 9 个模型（含 Llama‑3.2 1B/3B、Llama‑3.1 8B、Qwen2.5 0.5B/1.5B/3B/7B/Math‑7B、Mathstral‑7B）上几乎始终取得最优的 Δ 和最低的标准差，说明其鲁棒性提升具有跨模型族和跨规模的稳定性。


![[assets/figures/papers/iclr26_0005_49vo7D9LbI_AbstRaL_Augmenting_LLMs_Reasoning_by_Reinforcing/figures/011_Table_5.jpg]]
*Table 5: More evaluation results on GSM-Symbolic. ∆ denotes the relative percentage of drop comparing performance on Vary Both to performance on Origin 100. Best results on each model are bold, where lower is better for ∆. Standard deviation (std) of multi-round evaluation results are in brackets, where lowest std values on each model are underlined. The best (bold) results with ∗ are significantly better than their corresponding second-best results, with significant test p-value \< 0.05*

需要注意的是，完整方法中包含符号求解工具；但移除工具后性能退化有限（以下将量化），表明性能增益主要来自抽象推理的学习，而非符号计算的机械优势。

### 消融实验

为厘清增益来源，我们对 AbstRaL 的五个关键组件进行了消融：移除符号工具（w/o Tools）、移除抽象中间上下文（w/o Contexts）、移除强化学习（w/o RL）、移除符号距离奖励（w/o r_symbolic）、以及移除 GranulAR 精细分解推理格式（w/o GranulAR）。结果如 Table 2 所示，揭示了以下因果机制：


![[assets/figures/papers/iclr26_0005_49vo7D9LbI_AbstRaL_Augmenting_LLMs_Reasoning_by_Reinforcing/figures/008_Table_2.jpg]]
*Table 2: Ablation study results of GSM reasoning robustness*

1. **GranulAR 格式是鲁棒性的核心。** 完整 AbstRaL 在 Qwen2.5‑Math‑7B 上的 Distract 准确率为 82.3%；当直接用未改写的 Socratic CoT 数据做 RL（即 w/o GranulAR），准确率骤降至 66.8%，退回到与基线 CoT‑8S（76.3%）相比更差的水平。这表明仅凭强化学习的训练形式不足以赋予模型抗干扰能力，关键在于训练数据中融入了子问题分解与抽象符号对应的精细推理结构。

2. **抽象中间上下文是符号抽象落地到自然语言推理的桥梁。** 移除中间上下文（w/o Contexts）导致 0.5B 模型 Vary Both 性能从 44.6% 猛跌至 23.1%，7B 模型也出现显著下降。这一结果支撑了"缩小符号抽象与自然语言之间的语义鸿沟是实现忠实抽象思维的关键"这一核心论点。

3. **RL 与符号奖励的贡献具有层级性。** 仅用 SFT（w/o RL）的整体性能明显低于完整 AbstRaL，表明在已获得 GranulAR 格式先验的基础上，RL 进一步强化了抽象生成的忠实度。单独移除符号距离奖励（w/o r_symbolic）造成中等程度的退化，说明将抽象表达的精确匹配纳入优化目标有其独立价值。

综合消融结果表明，AbstRaL 的鲁棒性来源是一个联合机制：GranulAR 格式提供抽象推理的"模板"，中间上下文维持自然语言与符号间的映射，RL 与模型无关奖励则确保生成抽象忠实于目标结构。

### 跨任务泛化与 OOD 评估

我们通过在 GSM 相关数据集之外进行零样本评估来考察抽象思维是否能跨任务迁移。Table 3 报告了 MATH OOD 数据集上的零样本准确率：在 Qwen2.5‑0.5B‑Instruct 上，AbstRaL 达到 34.7%，比 Ori‑SFT 基线 30.0% 高出 4.7 个百分点，并优于 CoT‑RL 和 CoA；在 7B 模型上趋势一致但增益幅度较小。更广泛的 OOD 评估（Table 4）覆盖 MMLU 各子类、BBH、ARC‑Challenge 和 OpenBookQA，AbstRaL 在两个模型上取得多数指标的最优结果，其中 7B 模型在 BBH 上达到 54.8%，显著优于 Ori‑SFT（48.3%）。这些结果说明，通过学习在推理初期进行"整体性问题分析与分解"，模型获得了可应用于未见任务的元推理能力，而不仅仅是 GSM 域内的泛化。


![[assets/figures/papers/iclr26_0005_49vo7D9LbI_AbstRaL_Augmenting_LLMs_Reasoning_by_Reinforcing/figures/009_Table_3.jpg]]
*Table 3: Zero-shot evaluation results on OOD math datasets. Best results on each model are bold*

### 失败模式分析

随着模型在推理初期投入更多认知资源进行全局规划，AbstRaL 在个别简单问题上出现了"过度思考"导致的误判（Table 9 展示了一个基本算术错误案例）。具体而言，当问题在逻辑上足够简单、无需刻意抽象就能一步求解时，模型仍强制进行条件识别与子问题分解，引入了不必要的推理层面，反而放大了出错概率。这一现象提示，未来可探索动态选择抽象层级的推理策略，在低复杂度样本上适时退化为轻量推理，以平衡鲁棒性与效率。本结论基于附录示例的定性分析，未提供量化的复杂度分档统计，建议在使用中对其影响程度做进一步手动验证。

## 方法谱系与知识库定位

AbstRaL 的核心定位不是一种新的数据增强策略，而是通过**强化学习直接塑造抽象思维模式**，使小型大语言模型在小学数学（GSM）推理中对表面形式变化（数值替换、实体改名、干扰条件插入）表现出更高的稳健性。这一思路与现有方法形成了鲜明的对照：CoT‑8S / PoT‑8S 依赖少样本提示，并未改变模型内部的推理结构；CoT‑RL 虽然使用强化学习，却仅基于未经改写的 Socratic CoT 数据，缺少显式抽象学习目标；CoA（Chain of Abstraction）和 AoT（Abstract of Thought）更侧重将抽象作为一种推理格式，但训练仍局限于监督模仿，未能引入奖励信号对抽象忠实性进行优化；SyReLM 等符号推理系统虽然具有形式化优势，却难以与自然语言推理无缝衔接。AbstRaL 通过三个关键变更槽位将"抽象学习"作为中心训练目标：（1）**训练数据格式**从标准 Socratic CoT 转为 GranulAR 精细分解的抽象推理链（§3.1，表 2 消融证实该格式对分布鲁棒性提升贡献最大）；（2）**训练范式**从纯监督微调升级为 SFT + 强化学习，并引入模型无关的抽象奖励（符号距离奖励与答案正确性奖励，式 (1)）；（3）**推理流程**固定为四步管道：条件识别 → 抽象推理 → 抽象检索 → 符号推导（§3，图 3(b)）。这种"先抽象、再推导"的范式使得推理过程与具体上下文解耦，从而在 GSM‑Symbolic 的 Vary Both 测试中将小模型（Qwen2.5‑0.5B）的性能衰退几乎完全恢复（Δ = –1.27%，表 1），并在 GSM‑Plus Distract 上带来了+6.0pp 的增益（82.3% vs CoT‑8S 76.3%，表 1）。消融实验进一步表明，移除 GranulAR 格式会导致 Distract 准确率从 82.3% 骤降至 66.8%，移除抽象中间语境则使 Vary Both 性能从 44.6% 跌至 23.1%（表 2），说明精细抽象链和自然语言‑符号接口的协同作用是性能增益的主要来源，而非单纯的外挂符号工具。

**适用边界**方面，当前工作聚焦于 GSM 类单步/多步算术文字题，在跨数据集零样本泛化（MATH、MMLU STEM、BBH 等，表 3、表 4）上虽有一定溢出效益，但未见对开放域推理、代码生成或需要领域知识的科学推理任务的评估。GranulAR 数据的构造需要**借助强预言模型**（如 Llama‑3.3‑70B‑Instruct）进行条件识别和逐步重写（附录 B），虽然作者在讨论中证明性能增益并非源于对预言模型推理能力的蒸馏（§5.3），但数据构造过程仍可能遗留预言模型的特定偏差，且该流程本身成本较高，限制了方法的快速迁移。此外，实验中仅在 0.5B‑7B 参数规模上验证，更大模型的抽象学习潜力与计算代价尚不明确。

AbstRaL 在定性分析中也暴露了**过度抽象**的风险：强制要求推理开始前进行分步拆解，可能导致模型在少数简单问题上"过度思考"，反而错误理解题目（附录表 9 的错误示例）。这表明抽象程度的控制（何时抽象、抽象到何种粒度）仍是一个待解决的问题。更根本的局限在于，抽象学习目前依赖于奖励函数中符号距离的正确匹配，若符号表示设计不当，会直接将错误模式强化到策略中。

论文本身明确指出了若干**开放问题**：为何在自然语言、代码等多源语料上预训练的 LLM 仍然难以直接预测上下文无关的抽象？能否建立一个形式化框架，将抽象对样本/时间学习复杂度的影响加以量化？如何定义"真正的抽象"——当抽象（A）不应等同于推理结果（Y）时，如何保证 A 仅仅剥离语境而非包含推理本身？这些问题的探索有望将抽象学习从启发式工程推向理论支撑的领域，也为将 AbstRaL 范式扩展到更复杂的推理任务（如多步规划、科学推理）提供了方向。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/AbstRaL_Augmenting_LLMs_Reasoning_by_Reinforcing_Abstract_Thinking.pdf

![[paperPDFs/ICLR_2026/AbstRaL_Augmenting_LLMs_Reasoning_by_Reinforcing_Abstract_Thinking.pdf]]
