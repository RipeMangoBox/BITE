---
title: "SK2Decompile: LLM-based Two-Phase Binary Decompilation from Skeleton to Skin"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SK2Decompile_LLM_based_Two_Phase_Binary_Decompilation_from_Skeleton_to_Skin.pdf
openreview_forum_id: jSQPqdoidy
aliases:
- SK2Decompile
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将反编译任务分解为结构恢复（骨架）和标识符命名（皮肤）两个顺序阶段，引入混淆中间表示作为桥梁，并分别采用编译器和语义相似度奖励进行强化学习训练。"
primary_logic: "通过信息瓶颈原理设计的混淆源代码IR最大化了从二进制到结构的可恢复性，同时最小化了不相关的标识符噪声；两阶段分解使得每个阶段能够通过专门的RL奖励独立优化，分别提升功能正确性和可读性。"
claims:
- "SK2Decompile在HumanEval上的平均重执行率（69.00%）比GPT-5-mini（56.75%）相对提升21.6%，在MBPP上相对提升26.3%。"
- "两阶段分解（pseudo-ir-src）相比单阶段（pseudo-src）在HumanEval上重执行率从54.86%提升至63.75%，相对改善16.2%。"
- "在Structure Recovery上应用RL训练可使重执行率大幅提升：HumanEval AVG +10.0%，MBPP AVG +20.8%。"
- "在真实世界数据集GitHub2025上，SK2Decompile的R2I得分（71.62）比Idioms（61.63）高出29.4%，结构可读性优势明显。"
---

# SK2Decompile: LLM-based Two-Phase Binary Decompilation from Skeleton to Skin

> [!tip] 核心洞察
> 通过信息瓶颈原理设计的混淆源代码IR最大化了从二进制到结构的可恢复性，同时最小化了不相关的标识符噪声；两阶段分解使得每个阶段能够通过专门的RL奖励独立优化，分别提升功能正确性和可读性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SK2Decompile：基于大语言模型的两阶段二进制反编译——从骨架到皮肤 |
| 英文题名 | SK2Decompile: LLM-based Two-Phase Binary Decompilation from Skeleton to Skin |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jSQPqdoidy) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SK2Decompile |
| Dataset | HumanEval, MBPP, GitHub2025, ExeBench |

> [!tip] 效果简介
> - HumanEval 上，Re-executability rate (AVG) 为 69.00%，对比 56.75% (GPT-5-mini)，变化 +21.6%。
> - MBPP 上，Re-executability rate (AVG) 为 59.63%，对比 47.23% (GPT-5-mini)，变化 +26.3%。
> - GitHub2025 上，R2I (AVG) 为 71.62，对比 61.63 (Idioms)，变化 +29.4%。

## 概述

### 问题与瓶颈

二进制反编译旨在从编译后的机器码恢复出可读的高级语言源代码。当前基于大语言模型的单阶段反编译器（如 **LLM4Decompile** (Tan et al., 2024)、**Idioms** (Dramko et al., 2025) 以及商业模型 **GPT-5-mini**）面临一个根本性瓶颈：它们试图在单次生成中同时恢复程序的源级结构（控制流、循环、数据结构）与语义标识符（函数名、变量名、类型名），导致功能正确性与代码可读性之间的难以调和的折衷。图1的动机示例直观地展示了这一点——现有模型在类型恢复和标识符推断上频繁出错，而程序骨架本身的信息却已隐含在伪代码之中。

### 核心方法：从骨架到皮肤的两阶段分解

SK2Decompile 将反编译任务分解为两个顺序阶段，以解耦上述冲突：

- **Structure Recovery（骨架恢复）**：从 IDA 生成的伪代码出发，恢复程序的完整结构骨架，输出一种**混淆中间表示**——将原源代码中的所有标识符替换为通用占位符（如 `var1`、`func1`、`type1`），但保留完整的控制流、数据布局和类型声明。该阶段专注于“程序做什么”，而非“事物叫什么”。
- **Identifier Naming（皮肤命名）**：以上一阶段输出的混淆 IR 为输入，为所有占位符推断出具有实际语义含义的名称，生成最终可读的源代码。该阶段专注于“事物叫什么”，而非结构是否正确。

这一分解的信息论基础是**信息瓶颈原理**：混淆 IR 的设计最大化从二进制到结构的可恢复性，同时最小化不相关的标识符噪声，从而在两个阶段之间形成最优的信息桥梁。

### 训练策略：阶段特化的强化学习

每个阶段在监督微调之后，均采用专门的强化学习奖励进行独立优化：

- **Structure Recovery 的奖励**：基于编译成功验证（使用 Psyche-C 编译器）加上占位符恢复的 Jaccard 相似度。若生成的 IR 可编译则获得基础奖励 1.0，额外奖励取决于占位符的准确恢复程度；若不可编译则奖励为 0。这有效抑制了“奖励黑客”行为——模型仅生成可编译但语义空洞的平凡代码。
- **Identifier Naming 的奖励**：基于生成代码与参考源代码的嵌入余弦相似度（使用 qwen-embedding-0.6B），以捕捉语义等价的命名而非强制精确字符串匹配。人类评估表明，训练对嵌入模型的选择不敏感（平局率达 71.66%）。

### 主要结果概览

SK2Decompile 在两个核心维度上取得了显著提升：

- **功能正确性**：在 HumanEval 上平均重执行率达 **69.00%**，相较 GPT-5-mini 的 56.75% 相对提升 **21.6%**；在 MBPP 上相对提升 **26.3%**。两阶段分解本身（未加 RL）即带来 16.2% 的重执行率改善，而 RL 训练进一步贡献了约 10% 的额外提升。
- **结构可读性**：在真实世界数据集 GitHub2025 上，R2I 得分达 **71.62**，比 Idioms 的 61.63 高出 **29.4%**，验证了混淆 IR 在结构信息保留上的优势。
- **标识符质量**：在 GPT-judge 语义评分上，SK2Decompile 与 GPT-5-mini 持平或略优（HumanEval 上 4.24 vs 4.23），表明两阶段设计并未牺牲命名质量。

消融实验进一步证实：Structure Recovery 阶段单独输出的 GPT-judge 得分极低（HumanEval AVG 仅 2.67），说明其严格专注于结构而不过早泄露命名信息，验证了阶段隔离的有效性。完整的 SK2Decompile（两阶段 + RL）在所有变体中取得最高重执行率，确认了分解与强化学习的组合优势。

## 背景与动机

### 二进制反编译的核心挑战

二进制反编译旨在将编译后的低级机器码恢复为人类可读的高级语言源代码，这在软件安全分析、遗留系统维护和恶意软件检测等领域具有关键价值。然而，该任务面临一个根本性瓶颈：**现有的单阶段LLM反编译器难以同时恢复程序的源级结构（控制流、数据结构）和语义标识符**，导致功能正确性与可读性之间的固有折衷。

具体而言，反编译涉及两个相互耦合但性质迥异的子任务：
- **结构恢复**：重建程序的控制流（如循环形式、条件分支）和数据访问模式（如数组索引、结构体字段），这些信息在编译过程中被部分保留于伪代码中。
- **标识符命名**：为变量、函数和类型赋予有意义的名称，这些语义信息在编译过程中几乎完全丢失，需要从功能上下文中推断。

单阶段模型（如 **LLM4Decompile**，Tan et al., 2024）试图直接从伪代码生成完整源代码，但正如 Figure 1 所示，其在类型恢复（如 `int` 误判为 `int*`）和标识符推断（如变量命名偏离原始语义）上频繁出错。商业大语言模型（如 **GPT-5-mini**，OpenAI, 2025）虽具备更强的生成能力，但在重执行率上仍仅达到 56.75%（HumanEval 平均），表明功能正确性远未满足实际需求。

### 现有方法的局限性

当前基于LLM的反编译器可分为两类，均存在显著缺口：

1. **端到端单阶段模型**（LLM4Decompile、**Idioms**（Dramko et al., 2025）等）：将反编译视为从伪代码到源代码的直接翻译任务。这类方法面临**信息过载**问题——模型需要同时推理结构约束和命名语义，而伪代码中可用的结构信号被标识符噪声所淹没。例如，Figure 1 中 `while` 循环在伪代码中以条件跳转形式存在，单阶段模型难以将其准确还原为 `while` 结构，同时还要猜测变量 `v1` 的原始名称。

2. **反馈循环方法**（**Ref-Decompile** 等）：通过多次自我修正迭代改进输出，但每次迭代仍同时处理结构和命名，缺乏对两个子任务的解耦优化。此外，其反馈信号（如编译错误）难以区分结构错误与命名错误，导致修正方向模糊。

传统反编译器（如 **IDA**）虽能生成伪代码，但其输出仅为中间表示，缺乏可编译性和语义标识符，无法直接用于下游分析。

### 本文动机：从骨架到皮肤的两阶段分解

本文的核心洞察源自**信息瓶颈原理**：伪代码 $u$ 与源代码 $s$ 之间的互信息 $I(u; s)$ 中，结构信息（控制流、数据依赖）在编译过程中保留较多，而标识符信息几乎完全丢失。因此，直接建模 $P(s|u)$ 迫使模型在稀疏的结构信号与嘈杂的标识符猜测之间分配容量，导致两者皆不佳。

SK2Decompile 提出将反编译概率模型分解为：

$$P(s|u) \approx \sum_i P(s|i) \cdot P(i|u)$$

其中 $i$ 为**混淆中间表示（Obfuscated IR）**——一种将所有标识符替换为通用占位符（如 `var1`、`func1`）但仍保留完整C语法的源代码形式。这一分解的动机在于：

- **$P(i|u)$（Structure Recovery）**：从伪代码恢复程序骨架，仅关注结构正确性，不受标识符噪声干扰。IR 设计遵循信息瓶颈目标 $\min I(u; i) - \beta I(i; s)$，最大化从二进制到结构的可恢复性，同时最小化不相关的标识符噪声。
- **$P(s|i)$（Identifier Naming）**：从已恢复的骨架推断语义标识符，此时模型已具备完整的控制流和数据依赖上下文，命名任务从“盲猜”变为“填空”。

两阶段分解使得每个阶段能够通过**专门的强化学习奖励**独立优化：Structure Recovery 使用编译器验证奖励（编译成功即得 1.0）和占位符恢复奖励（Jaccard 相似度），确保生成既可编译又结构准确的 IR；Identifier Naming 使用嵌入余弦相似度奖励，捕捉语义等价的命名而非精确字符串匹配。这种“骨架先行、皮肤后补”的策略，从原理上解耦了功能正确性与可读性的优化路径。

## 核心创新

SK2Decompile 的核心创新在于将二进制反编译任务从传统的单阶段范式重构为**两阶段分解架构**，并通过**信息瓶颈驱动的中间表示设计**和**阶段特化的强化学习奖励**实现功能正确性与可读性的协同优化。

### 1. 任务分解：从单阶段到两阶段

现有 LLM 反编译器（如 **LLM4Decompile** (Tan et al., 2024)、**Idioms** (Dramko et al., 2025)）采用单阶段范式，直接从伪代码生成源代码，面临一个根本性瓶颈：**程序的结构恢复（控制流、数据类型、数据结构）与标识符命名（函数名、变量名、类型名）被耦合在同一生成过程中**，导致模型在功能正确性与可读性之间被迫折衷。

SK2Decompile 将这一耦合任务解耦为两个顺序阶段：

- **Structure Recovery（骨架恢复）**：从伪代码恢复程序的全局代码结构，包括循环、条件分支和数据布局，生成一个仅包含通用占位符（如 `var1`、`func1`）的混淆源代码 IR。
- **Identifier Naming（皮肤命名）**：以混淆 IR 为输入，推断反映程序实际语义的有意义标识符，生成最终的可读源代码。

这一分解的概率模型可形式化为：

$$P ( \mathbf { s } | \mathbf { u } ) \approx \sum _ { \mathrm { i } } P ( \mathbf { s } | \mathbf { i } ) \cdot P ( \mathbf { i } | \mathbf { u } )$$

其中 $\mathbf{u}$ 为伪代码，$\mathbf{i}$ 为中间表示，$\mathbf{s}$ 为源代码。该分解基于 Markov 假设，使得两个阶段可以独立优化，分别聚焦于结构正确性和语义可读性。

**消融实验直接验证了这一创新的有效性**：两阶段分解（pseudo-ir-src）相比单阶段（pseudo-src）在 HumanEval 上的重执行率从 54.86% 提升至 63.75%，相对改善 16.2%；在 MBPP 上从 47.51% 提升至 52.83%，相对改善 11.2%（Table 4）。

### 2. 中间表示设计：信息瓶颈驱动的混淆 IR

SK2Decompile 的第二个关键创新是引入**混淆源代码 IR** 作为两阶段之间的桥梁。与现有方法直接使用伪代码或无显式 IR 不同，该 IR 的设计遵循**信息瓶颈（Information Bottleneck）**原理：

$$\operatorname* { m i n } _ { P ( i \mid u ) } \mathcal { L } _ { \mathrm { I B } } = I ( \mathbf { u } ; \mathbf { i } ) - \beta I ( \mathbf { i } ; \mathbf { s } )$$

该目标函数最小化伪代码 $\mathbf{u}$ 与 IR $\mathbf{i}$ 之间的互信息（压缩无关细节），同时最大化 IR $\mathbf{i}$ 与源代码 $\mathbf{s}$ 之间的互信息（保留结构信息）。具体实现为：将源代码中的所有标识符（函数名、变量名、类型名、结构体字段）替换为类型感知的通用占位符（如 `var1`、`func1`、`struct1`），但完整保留控制流、数据类型声明和数据结构布局。

这一设计的核心优势在于：**最大化了从二进制到程序结构的可恢复性，同时最小化了不相关的标识符噪声**。Table 6 的证据表明，Structure Recovery 模型的单独输出在 GPT-judge 上得分极低（pseudo-ir 在 HumanEval AVG 仅 2.67/5），证明该阶段确实专注于结构而非命名，验证了阶段隔离的有效性。

### 3. 训练方法创新：阶段特化的强化学习奖励

SK2Decompile 的第三个关键创新是**为两个阶段分别设计了专门的强化学习奖励函数**，替代传统反编译器的纯监督微调（交叉熵损失）：

- **Structure Recovery 奖励**：结合编译验证与占位符恢复精度。若生成的 IR 可通过 Psyche-C 编译，则给予 $1.0 + r_{\mathrm{placeholder}}$ 的奖励，其中 $r_{\mathrm{placeholder}}$ 为生成占位符与参考 IR 占位符的 Jaccard 相似度；若不可编译，奖励为 0。这一设计有效抑制了奖励黑客行为——模型若仅生成可编译的平凡代码（如空函数），将因占位符恢复精度低而获得较低奖励。

$$r_{\mathrm{stncure}} = \left\{ \begin{array}{ll} 0.0, & \mathrm{if~} IR \mathrm{~cannot~be~compiled} \\ 1.0 + r_{\mathrm{placeholder}}, & \mathrm{if~} IR \mathrm{~can~be~compiled} \end{array} \right.$$

- **Identifier Naming 奖励**：采用生成代码与参考源代码的嵌入余弦相似度，而非精确字符串匹配。这使模型能够学习语义等价的命名（如 `allocate` 与 `alloc`），而非机械复制训练数据中的标识符。

$$r_{\mathrm{identifier}} = \cos(\mathbf{e}_{\mathrm{gen}}, \mathbf{e}_{\mathrm{src}}) = \frac{\mathbf{e}_{\mathrm{gen}} \cdot \mathbf{e}_{\mathrm{src}}}{\|\mathbf{e}_{\mathrm{gen}}\| \|\mathbf{e}_{\mathrm{src}}\|}$$

**RL 训练的增益十分显著**：对 Structure Recovery 阶段施加 RL（pseudo-ir-rl）使 HumanEval AVG 重执行率从 62.56% 升至 68.84%（+10.0%），MBPP 从 47.25% 升至 57.06%（+20.8%）（Table 4）。完整的 SK2Decompile（pseudo-ir-src-rl）在所有变体中取得最高重执行率，验证了两阶段分解与阶段特化 RL 的组合优势。人类评估进一步表明，Identifier Naming 的训练对嵌入模型选择不敏感（71.66% 平局率），说明语义相似度奖励具有良好的鲁棒性。

### 创新总结

SK2Decompile 的三个 changed slots——任务分解、中间表示设计和训练方法——构成了一个协同的创新体系：两阶段分解使得结构正确性和语义可读性可以分别优化，信息瓶颈驱动的混淆 IR 为阶段隔离提供了表示基础，而阶段特化的 RL 奖励则为每个阶段提供了精确的优化信号。这一体系在 HumanEval 上实现了 69.00% 的平均重执行率，相对 **GPT-5-mini** (OpenAI, 2025) 提升 21.6%，在 GitHub2025 上 R2I 得分 71.62，相对 **Idioms** 提升 29.4%。

## 整体框架

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_jSQPqdoidy/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the SK2Decompile framework. (a) Data preparation: We obfuscate identifiers to produce an Intermediate Representation (IR). Headers are inferred using psychec to serve as ground truth for checking compilability during the RL stage of Structure Recovery (b). We also compile the code and use IDA to generate initial pseudo code. SK2Decompile employs a two-phase decompilation process comprising (b) Structure Recovery and (c) Identifier Naming, where obfuscated source code serves as the IR connecting the two phases. Each model undergoes Supervised Fine-Tuning (SFT) followed by Reinforcement Learning (RL) with phase-specific rewards*

SK2Decompile 将二进制反编译任务分解为两个顺序阶段：**Structure Recovery**（结构恢复）与 **Identifier Naming**（标识符命名），分别对应程序的“骨架”与“皮肤”。其核心洞察是：通过引入一个精心设计的**混淆中间表示**（Obfuscated IR）作为桥梁，将原本耦合的功能正确性恢复与语义可读性恢复解耦，使每个阶段能够独立优化。

### 概率建模视角

从概率角度，反编译可建模为给定伪代码 $\mathbf{u}$ 下生成源代码 $\mathbf{s}$ 的条件概率 $P(\mathbf{s}|\mathbf{u})$。SK2Decompile 基于 Markov 假设，通过引入中间表示 $\mathbf{i}$ 将其分解为：

$$P ( \mathbf { s } | \mathbf { u } ) \approx \sum _ { \mathrm { i } } P ( \mathbf { s } | \mathbf { i } ) \cdot P ( \mathbf { i } | \mathbf { u } )$$

其中 $P(\mathbf{i}|\mathbf{u})$ 对应 Structure Recovery 阶段，负责从伪代码恢复程序的结构骨架；$P(\mathbf{s}|\mathbf{i})$ 对应 Identifier Naming 阶段，负责为骨架上的占位符赋予语义有意义的标识符。这一分解使得两个阶段可以使用各自的奖励函数进行强化学习训练，分别提升功能正确性与可读性（Section 3.2）。

### 管道模块与数据流

整个框架由四个核心模块串联构成（Figure 2）：

1. **数据准备模块**：将 C 源码编译为二进制，使用 IDA 生成初始伪代码；同时对源码进行标识符混淆生成混淆 IR（Algorithm 1），并利用 Psyche-C 推断头文件作为编译性验证的地面真相。训练数据集来自 ExeBench 和 Decompile-Bench 的 C 程序，覆盖 GCC/Clang 编译器在 O0–O3 优化级别下的约 500 万样本（Section 3.4, Section 4）。

2. **Structure Recovery 模型**：基于 LLM4Decompile-6.7B，以伪代码为输入，输出混淆 IR。该模型先经监督微调（SFT），再通过强化学习（RL）优化，奖励函数为编译成功（1.0）加上生成占位符与参考 IR 占位符的 Jaccard 相似度 $r_{\mathrm{placeholder}}$；若不可编译则奖励为 0（Formula 3）。编译器验证使用 Psyche-C 提供的头文件进行。

3. **Identifier Naming 模型**：同样基于 LLM4Decompile-6.7B，以混淆 IR 为输入，输出带有语义标识符的源代码。RL 奖励采用生成代码与参考源代码的嵌入余弦相似度，而非精确字符串匹配，以捕捉语义等价的命名差异（Formula 4）。嵌入模型使用 qwen-embedding-0.6B。

4. **强化学习训练管道**：两个阶段均采用 GRPO 算法（veRL 库实现），在 50,000 个随机样本上进行 RL 训练。推理阶段使用 vLLM 库配合贪婪解码加速生成。

### 混淆 IR 的设计原理

混淆 IR 是连接两个阶段的关键桥梁。其设计遵循**信息瓶颈**（Information Bottleneck）原则：

$$\operatorname* { m i n } _ { P ( i \mid u ) } \mathcal { L } _ { \mathrm { I B } } = I ( \mathbf { u } ; \mathbf { i } ) - \beta I ( \mathbf { i } ; \mathbf { s } )$$

即最小化伪代码 $\mathbf{u}$ 与 IR $\mathbf{i}$ 之间的互信息（压缩不相关细节），同时最大化 IR $\mathbf{i}$ 与源代码 $\mathbf{s}$ 之间的互信息（保留结构信息）。具体实现为：保留源代码的完整语法结构（循环、条件、数据结构），但将所有标识符（变量名、函数名、类型名）替换为通用占位符（如 `var1`, `func1`），从而在保留结构可恢复性的同时消除标识符噪声（Section 3.3, Algorithm 1）。

### 输入输出流

- **输入**：编译后的二进制文件经 IDA 生成的伪代码。
- **Stage 1 输出**：混淆 IR，包含完整的控制流与数据结构，但标识符为占位符。
- **Stage 2 输出**：最终反编译的 C 源代码，具备语义有意义的标识符。
- **训练信号**：Stage 1 使用编译器反馈（可编译性）+ 占位符恢复精度；Stage 2 使用语义相似度（嵌入余弦距离）。

## 核心模块与公式推导

### 两阶段分解的概率模型

SK2Decompile将反编译任务形式化为一个条件概率模型，并通过引入中间表示（IR）将任务分解为两个可独立优化的阶段。给定伪代码 $\mathbf{u}$ 和源代码 $\mathbf{s}$，反编译的目标是最大化 $P(\mathbf{s} \mid \mathbf{u})$。基于Markov假设，该概率可近似分解为结构恢复与标识符命名两部分的乘积之和：

$$P ( \mathbf { s } | \mathbf { u } ) \approx \sum _ { \mathrm { i } } P ( \mathbf { s } | \mathbf { i } ) \cdot P ( \mathbf { i } | \mathbf { u } )$$

其中，$\mathbf{i}$ 为中间表示（IR），$P(\mathbf{i} \mid \mathbf{u})$ 对应**Structure Recovery**阶段——从伪代码恢复程序骨架结构；$P(\mathbf{s} \mid \mathbf{i})$ 对应**Identifier Naming**阶段——从结构骨架恢复语义标识符。这一分解使得两个阶段可以分别通过专门的强化学习奖励进行优化，分别提升功能正确性与可读性。

### 信息瓶颈驱动的IR设计

IR的设计是两阶段分解的核心。SK2Decompile将IR设计问题建模为信息瓶颈（Information Bottleneck）优化任务，目标是在压缩伪代码信息的同时最大化与源代码的相关性：

$$\operatorname* { m i n } _ { P ( i \mid u ) } \mathcal { L } _ { \mathrm { I B } } = I ( \mathbf { u } ; \mathbf { i } ) - \beta I ( \mathbf { i } ; \mathbf { s } )$$

其中，$I(\mathbf{u}; \mathbf{i})$ 表示伪代码与IR之间的互信息（需最小化以实现压缩），$I(\mathbf{i}; \mathbf{s})$ 表示IR与源代码之间的互信息（需最大化以保持结构相关性），$\beta$ 为权衡参数。基于此优化目标，论文提出使用**混淆源代码**作为IR：将原始源代码中的所有标识符替换为通用占位符（如 `var1`、`func1`），从而在保留完整程序结构（控制流、数据类型、函数调用关系）的同时，彻底剥离标识符语义噪声。

### 关键管道模块

SK2Decompile框架包含以下核心模块：

- **数据准备模块**：编译C源码、使用IDA生成伪代码、通过混淆算法生成IR、提取头文件（用于后续编译验证）。混淆过程按标识符起始位置降序替换，避免偏移量漂移。
- **Structure Recovery模型**：基于LLM4Decompile-6.7B，输入伪代码，输出混淆IR。该模型通过监督微调（SFT）初始化，随后使用强化学习（RL）优化。
- **Identifier Naming模型**：同样基于LLM4Decompile-6.7B，输入混淆IR，输出带语义标识符的源代码。训练流程与Structure Recovery对称。
- **强化学习训练管道**：采用GRPO算法，在50,000个随机样本上进行RL训练。Structure Recovery的编译验证使用Psyche-C编译器，语义相似度使用qwen-embedding-0.6B。

### 阶段特定的RL奖励函数

两个阶段采用不同的奖励函数，分别对齐各自目标。

**Structure Recovery奖励**：鼓励生成既可编译又准确恢复占位符的IR。若生成的IR不可编译，奖励为0；若可编译，则给予基础奖励1.0加上占位符恢复的Jaccard相似度：

$$r_{\mathrm{placeholder}} = \frac{\left| I_{\mathrm{gen}} \cap I_{\mathrm{IR}} \right|}{\left| I_{\mathrm{gen}} \cup I_{\mathrm{IR}} \right|}, \qquad r_{\mathrm{stncure}} = \left\{ \begin{array}{ll} 0.0, & \mathrm{if~} IR \mathrm{~cannot~be~compiled} \\ 1.0 + r_{\mathrm{placeholder}}, & \mathrm{if~} IR \mathrm{~can~be~compiled} \end{array} \right.$$

其中，$I_{\mathrm{gen}}$ 为生成IR中的占位符集合，$I_{\mathrm{IR}}$ 为参考IR中的占位符集合。该奖励机制有效抑制了奖励黑客行为——模型若仅生成可编译的平凡代码（如空函数），将因占位符恢复得分低而受到惩罚。

**Identifier Naming奖励**：采用生成代码与参考源代码嵌入向量的余弦相似度，以捕捉语义等价的命名而非精确字符串匹配：

$$r_{\mathrm{identifier}} = \cos(\mathbf{e}_{\mathrm{gen}}, \mathbf{e}_{\mathrm{src}}) = \frac{\mathbf{e}_{\mathrm{gen}} \cdot \mathbf{e}_{\mathrm{src}}}{\|\mathbf{e}_{\mathrm{gen}}\| \|\mathbf{e}_{\mathrm{src}}\|}$$

其中，$\mathbf{e}_{\mathrm{gen}}$ 和 $\mathbf{e}_{\mathrm{src}}$ 分别为生成代码与参考源代码的嵌入向量。使用语义相似度而非精确匹配，使得模型能够学习到功能等价但命名风格不同的合理标识符，而非机械地复制训练数据中的命名。

## 实验与分析

### 核心瓶颈与实验动机

SK2Decompile的实验设计围绕一个核心因果假设展开：**将反编译任务分解为结构恢复（骨架）与标识符命名（皮肤）两个顺序阶段**，并分别施加阶段专属的强化学习奖励，能够同时提升功能正确性与代码可读性。现有单阶段LLM反编译器（如GPT-5-mini、LLM4Decompile）在这两个目标之间存在根本性折衷——要么生成结构正确但标识符无意义的代码，要么产生语义命名良好但无法编译的代码。实验系统性地验证了这一分解策略的有效性，以及混淆中间表示（IR）作为阶段桥梁的必要性。

### 主实验结果

#### 重执行率：功能正确性的决定性证据

重执行率（Re-executability rate）是衡量反编译代码功能正确性的核心指标。SK2Decompile在所有优化级别和基准上均取得最优结果（Table 1）：


![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_jSQPqdoidy/figures/003_Table_1.jpg]]
*Table 1: Re-executability results between the studied decompilers*

- **HumanEval基准**：SK2Decompile平均重执行率达69.00%，相比GPT-5-mini的56.75%相对提升21.6%，相比LLM4Decompile的49.50%提升39.4%。在-O3高优化级别下，SK2Decompile（66.93%）比GPT-5-mini（55.12%）高出11.81个百分点。
- **MBPP基准**：SK2Decompile平均重执行率59.63%，相比GPT-5-mini（47.23%）相对提升26.3%，相比Idioms（36.05%）提升65.4%。值得注意的是，GPT-5-mini在MBPP上相比LLM4Decompile（50.55%）反而下降，说明通用LLM的直接反编译能力在复杂程序上不稳定。
- **优化级别趋势**：所有方法的性能随优化级别升高而下降，但SK2Decompile的下降幅度更小。例如在HumanEval上，SK2Decompile从-O0的71.65%降至-O3的66.93%（降幅4.72个百分点），而GPT-5-mini从58.27%降至55.12%（降幅3.15个百分点），LLM4Decompile从53.54%降至43.31%（降幅10.23个百分点）。这表明SK2Decompile的结构恢复阶段对编译器优化具有更强的鲁棒性。

**证据强度**：Table 1提供了跨6个反编译器、2个基准、4个优化级别的系统比较，置信度0.95。所有模型使用相同的数据预处理和编译链，确保了公平性。

#### 结构可读性（R2I）：代码结构恢复质量

R2I指标衡量反编译代码与原始源码在结构层面的相似度，重点关注控制流和数据结构的恢复质量。SK2Decompile在真实世界数据集上优势尤为显著（Table 2）：


![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_jSQPqdoidy/figures/004_Table_2.jpg]]
*Table 2: R2I results between the studied decompilers with the compilation optimization levels O0, O3 and the averaged results on -O{0,1,2,3}*

- **GitHub2025数据集**：SK2Decompile平均R2I得分71.62，相比最强基线Idioms（61.63）相对提升29.4%，相比GPT-5-mini（53.53）提升33.8%。这表明SK2Decompile在处理真实世界复杂代码结构时具有明显优势。
- **ExeBench数据集**：SK2Decompile（72.99）相比Idioms（63.82）提升18.4%，相比LLM4Decompile（55.16）提升32.3%。
- **HumanEval和MBPP**：SK2Decompile在HumanEval上R2I得分71.65，MBPP上70.13，均高于所有基线。Idioms在MBPP上表现最接近（67.40），但仍低于SK2Decompile。

**关键观察**：Idioms虽然结合了调用图上下文和类型恢复，在结构可读性上已显著优于LLM4Decompile和GPT-5-mini，但SK2Decompile通过两阶段分解和编译器引导的RL训练，进一步大幅提升了结构恢复的准确性。这验证了混淆IR作为结构载体比伪代码直接生成源代码更有效。

#### 标识符命名质量（GPT-judge）：语义可读性

GPT-judge评分（1-5分）由GPT-4o评估标识符命名的语义适当性。SK2Decompile在标识符命名上与GPT-5-mini持平或略有优势（Table 3）：


![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_jSQPqdoidy/figures/005_Table_3.jpg]]
*Table 3: GPT-judge results between the studied decompilers*

- **HumanEval**：SK2Decompile得分4.24，GPT-5-mini得分4.23，差异仅为0.01（+0.2%），基本持平。
- **MBPP**：SK2Decompile得分4.12，GPT-5-mini得分4.08，相对提升1.0%。
- **真实世界数据集**：在ExeBench上SK2Decompile（2.42）相比GPT-5-mini（2.37）提升2.1%；在GitHub2025上SK2Decompile（3.06）相比GPT-5-mini（2.87）提升6.7%。真实世界数据集的绝对分数较低，反映了复杂程序中标识符恢复的固有难度。

**关键观察**：SK2Decompile在标识符命名上并未大幅超越GPT-5-mini，但这恰恰验证了阶段隔离的有效性——Identifier Naming阶段使用仅7B参数的模型，通过语义相似度奖励训练，达到了与商业大模型相当的命名质量。结合重执行率和R2I的大幅领先，SK2Decompile实现了功能正确性与可读性的双重提升，而非单方面的折衷。

### 消融实验：分解与RL的因果贡献

消融实验通过比较SK2Decompile的5个变体（Table 4-6），系统性地量化了两阶段分解和RL训练各自的贡献：


![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_jSQPqdoidy/figures/006_Table_4.jpg]]
*Table 4: Re-executability results between the S K ^ { 2 } Decompile variants*

#### 两阶段分解的效果

比较单阶段变体（pseudo-src，直接从伪代码生成源代码）与两阶段变体（pseudo-ir-src，通过混淆IR中转）：

- **HumanEval重执行率**：从54.86%提升至63.75%，相对改善16.2%。
- **MBPP重执行率**：从47.51%提升至52.83%，相对改善11.2%。
- **R2I**：在GitHub2025上从62.75提升至68.12（+8.6%），在ExeBench上从60.80提升至67.99（+11.8%）。

这证实了**信息瓶颈原理的实际效果**：混淆IR通过去除标识符噪声，使模型能够专注于结构恢复，从而在功能正确性和结构可读性上均获得显著提升。

#### RL训练的独立贡献

对Structure Recovery阶段施加RL（pseudo-ir-rl vs. pseudo-ir）：

- **HumanEval重执行率**：从62.56%跃升至68.84%，绝对提升6.28个百分点（+10.0%）。
- **MBPP重执行率**：从47.25%跃升至57.06%，绝对提升9.81个百分点（+20.8%）。

RL训练的效果在MBPP上更为显著，可能因为MBPP程序更复杂，编译器反馈对纠正结构错误的作用更大。值得注意的是，pseudo-ir-rl在GPT-judge上得分极低（Table 6：HumanEval AVG仅2.67），因为其输出为混淆IR，标识符均为占位符，这验证了Structure Recovery阶段确实专注于结构而非命名。

#### 完整组合的优势

完整SK2Decompile（pseudo-ir-src-rl）在所有变体中取得最高重执行率：
- HumanEval AVG 69.00%，MBPP AVG 59.63%。
- 相比未使用RL的两阶段变体（pseudo-ir-src），HumanEval提升8.2%，MBPP提升12.9%。
- 相比仅对Structure Recovery使用RL（pseudo-ir-rl），HumanEval基本持平（68.84% vs 69.00%），但GPT-judge从2.67大幅提升至4.24，说明Identifier Naming阶段成功恢复了语义标识符。

#### 占位符恢复奖励的必要性

在Structure Recovery的RL训练中，仅使用编译成功奖励（1.0/0.0）会导致**奖励黑客行为**：模型倾向于生成可编译但语义空洞的平凡代码（如仅包含`return 0;`）。引入占位符Jaccard相似度作为额外奖励项（公式3）有效抑制了这一问题，使模型在追求可编译性的同时必须准确恢复占位符标识符。这一消融在附录A.15中进行了验证。

### 案例研究：阶段隔离的可视化验证

Figure 3展示了一个内存分配函数（`dtoa_alloc`）的反编译案例，直观展示了各阶段的输出差异：


![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_jSQPqdoidy/figures/007_Figure_3.jpg]]
*Figure 3: A case study on a memory allocation function with (a) pseudocode, (b) source code, (c) decompilation result from pseudo-src in Table 4, (d) Structure Recovery result from pseudo-ir in Table 4, (e) Identifier Naming result from pseudo-ir-src in Table 4, and (f) decompilation from GPT-5-mini*

- **伪代码（a）**：IDA生成的伪代码包含大量无意义变量名（如`v3`, `v4`），控制流结构基本保留但可读性差。
- **单阶段输出（c, pseudo-src）**：直接生成源代码，函数签名恢复为`sub_xxx`，内部变量名仍为通用占位符，结构基本正确但语义信息丢失。
- **Structure Recovery输出（d, pseudo-ir）**：生成混淆IR，结构完整且可编译，但所有标识符均为占位符（如`var1`, `func1`）。
- **Identifier Naming输出（e, pseudo-ir-src）**：在混淆IR基础上恢复语义标识符，函数名恢复为`dtoa_alloc`，变量名如`result`, `v1`等部分恢复语义。
- **GPT-5-mini输出（f）**：函数签名完全错误（`sub_xxx`），内部逻辑与原始代码差异较大。

这个案例具体说明了：**两阶段分解使得模型能够先确保结构正确，再专注命名，避免了单阶段模型中两个目标相互干扰的问题**。

### 公平性说明与评估局限性

实验设计中的公平性考量需要关注以下几点：

1. **统一预处理**：所有方法使用相同的数据集（ExeBench和Decompile-Bench的C程序）、相同的编译链（GCC/Clang, O0-O3），并经过统一的预处理（去除注释、clang-format、MinHash-LSH去重）。
2. **R2I指标修正**：如果pycparser解析失败则赋值0而非丢弃样本，这可能导致整体分数偏低，但影响对所有方法均等。
3. **语言限制**：评估仅局限于C语言，因为现有LLM反编译器（包括SK2Decompile）均专注于C。
4. **基线排除**：某些基线（Nova, Ref-Decompile, D-LIFT）因未公开模型或预处理细节而被排除，这可能略微高估相对性能，但已包含最强的公开模型GPT-5-mini和LLM4Decompile/Idioms。
5. **重执行率测试**：对于stripped二进制需要恢复原始函数名以确保可编译和可测试，这在所有方法中保持一致处理。
6. **RL训练计算约束**：RL阶段仅在50,000个随机样本上训练，可能未充分发挥RL的潜力。

### 失败模式与局限

尽管SK2Decompile在整体指标上表现优异，但仍存在以下失败模式：

1. **真实世界数据集的标识符命名质量有限**：在ExeBench和GitHub2025上GPT-judge得分仅为2.42和3.06（5分制），远低于HumanEval（4.24）和MBPP（4.12）。这说明在复杂真实代码中，仅依赖嵌入相似度奖励可能不足以恢复高度语义化的标识符。
2. **优化级别间的性能差异**：虽然SK2Decompile对优化级别的鲁棒性优于基线，但-O3下的重执行率仍明显低于-O0（HumanEval: 66.93% vs 71.65%）。高优化级别下的编译器激进优化（如内联、循环展开）对结构恢复构成持续挑战。
3. **跨平台泛化**：实验主要在x86-64平台进行，附录中的跨平台实验（Table 12）显示在不同架构上的性能可能下降，但具体数据需要查阅原文确认。
4. **代码混淆的脆弱性**：附录中的混淆鲁棒性实验（Table 13）表明，针对性的代码混淆技术可能降低反编译质量，具体影响程度需要查阅原文。

### 实验结论

实验系统性地验证了SK2Decompile的核心假设：**两阶段分解+阶段专属RL训练**是实现高质量反编译的有效范式。混淆IR作为信息瓶颈，有效分离了结构恢复与标识符命名两个子任务；编译器引导的RL训练显著提升了结构正确性；语义相似度奖励使小模型也能达到商业大模型的命名质量。SK2Decompile在功能正确性（重执行率）、结构可读性（R2I）和语义可读性（GPT-judge）三个维度上实现了综合最优，且每个维度的提升均可通过消融实验归因到具体的设计选择。
## 方法谱系与知识库定位

### 1. 方法谱系：从单阶段到两阶段分解

SK2Decompile 的核心贡献在于将反编译任务从“端到端翻译”重新定义为“结构恢复→语义命名”的两阶段概率分解。这一设计直接回应了现有 LLM 反编译器在功能正确性与可读性之间的根本折衷。

**与单阶段 LLM 反编译器的关系。** 此前的主流范式是将伪代码直接细化为源代码。**LLM4Decompile**（Tan et al., 2024）是该范式的代表性工作，它使用 SFT 训练模型从伪代码生成源代码，但如 Figure 1 所示，其输出在类型推导和标识符恢复上存在明显缺陷。**Idioms**（Dramko et al., 2025）通过引入调用图上下文和类型恢复增强了这一流程，但仍受限于单阶段架构的信息混合问题。SK2Decompile 的消融实验（Table 4）量化了这一改进：仅将单阶段 `pseudo-src` 分解为两阶段 `pseudo-ir-src`（无 RL），HumanEval 重执行率即从 54.86% 提升至 63.75%（+16.2%），MBPP 从 47.51% 提升至 52.83%（+11.2%）。这验证了阶段隔离本身的结构性优势。

**与商业 LLM 的关系。** **GPT-5-mini**（OpenAI, 2025）作为当前最强的通用 LLM 之一，在直接反编译任务上表现出色（HumanEval AVG 56.75%），但 SK2Decompile 仍以 69.00% 的重执行率实现 21.6% 的相对提升。这表明即使是最先进的基础模型，在没有任务特定架构和训练的情况下，仍难以同时优化结构正确性和语义可读性。值得注意的是，在 GPT-judge 标识符命名评分上，GPT-5-mini 在 HumanEval 上与 SK2Decompile 几乎持平（4.23 vs 4.24），但在真实世界数据集 ExeBench 和 GitHub2025 上落后（2.1% 和 6.7% 的相对差距），暗示通用模型的命名能力在分布外数据上退化更明显。

**与规则基反编译器的关系。** **IDA** 作为传统反编译器，输出为伪代码而非可编译源代码。在 R2I 结构可读性评估中，IDA 在 ExeBench 上仅得 47.55，而 SK2Decompile 达到 72.99，差距反映了伪代码与真实源代码在结构表达上的本质鸿沟。SK2Decompile 的混淆 IR 设计（Algorithm 1）正是为了在保留完整语法结构的同时消除标识符噪声，从而桥接这一鸿沟。

### 2. 知识库定位：信息瓶颈与强化学习的交叉

SK2Decompile 的方法论基础建立在两个理论支柱上，使其在反编译文献中具有独特的定位。

**信息瓶颈（Information Bottleneck）指导的 IR 设计。** 传统反编译器通常直接使用伪代码或抽象语法树作为中间表示，缺乏对信息压缩与保留的理论指导。SK2Decompile 将 IR 设计形式化为 IB 优化问题（Formula 2），目标是最小化伪代码 u 与 IR i 的互信息 I(u;i)（压缩无关标识符），同时最大化 IR i 与源代码 s 的互信息 I(i;s)（保留结构信息）。这一理论框架解释了为何混淆源代码 IR 优于其他候选表示：它通过占位符替换消除了标识符噪声，同时保留了完整的 C 语法结构（循环、条件、数据访问模式），从而在 IB 意义上实现了最优压缩-保留平衡。

**编译器反馈与语义相似度驱动的强化学习。** 与仅依赖交叉熵损失的 SFT 训练不同，SK2Decompile 为两个阶段分别设计了专门的 RL 奖励函数。Structure Recovery 阶段使用编译成功（1.0）+ 占位符 Jaccard 相似度作为奖励（Formula 3），直接利用 **Psyche-C** 编译器验证生成 IR 的可编译性。消融实验（Table 4）表明，对 Structure Recovery 施加 RL（`pseudo-ir-rl`）使 HumanEval 重执行率从 62.56% 跃升至 68.84%（+10.0%），MBPP 从 47.25% 跃升至 57.06%（+20.8%），是单一技术改进中增益最大的操作。Identifier Naming 阶段则使用嵌入余弦相似度（Formula 4）而非精确字符串匹配，通过 **qwen-embedding-0.6B** 编码语义等价性。这一设计的关键洞察在于：语义正确的命名可能有多种形式（如 `len` vs `length`），精确匹配奖励会错误地惩罚有效变体，而嵌入相似度能捕捉这种等价性。人类评估（Appendix A.16）显示训练对嵌入模型选择不敏感（71.66% 平局率），进一步支持了该设计的鲁棒性。

**奖励黑客的抑制机制。** 纯编译奖励可能导致模型生成可编译但语义空洞的“奖励黑客”代码。SK2Decompile 通过引入占位符恢复奖励（`r_placeholder`）有效抑制了这一问题（Appendix A.15）：模型必须同时满足编译约束和占位符恢复约束，从而生成既合法又有意义的 IR。这一机制与 GRPO 算法（Guo et al., 2025）的结合，构成了一个约束满足框架，确保 RL 优化不偏离反编译的本质目标。

### 3. 适用边界与局限

**语言边界。** SK2Decompile 的训练和评估完全局限于 C 语言。所有数据集（ExeBench、Decompile-Bench）和编译链（GCC/Clang, O0-O3）均针对 C 程序。该方法的核心设计——混淆源代码 IR——依赖于 C 的静态类型系统和显式语法结构，直接迁移到动态类型语言（如 Python）或不同编译范式的语言（如 C++ 的模板元编程）可能需要重新设计 IR 和奖励函数。

**二进制类型边界。** 评估中对于 stripped 二进制需要恢复原始函数名以确保可编译和可测试，这一处理在所有方法中保持一致，但暗示 SK2Decompile 在完全 stripped 场景下的独立性能可能低于报告值。Figure 4 展示了 stripped 与未 stripped 伪代码的可读性差异，但未量化其对最终反编译质量的影响程度。

**数据集覆盖边界。** 训练数据来自 ExeBench 和 Decompile-Bench，均为合成或精选的 C 程序集合。虽然在 GitHub2025 真实世界数据集上取得了最强的 R2I 性能（71.62 vs Idioms 61.63，+29.4%），但该数据集的规模和多样性未在论文中详细说明，其代表性需要进一步验证。

**计算成本边界。** RL 训练阶段因计算约束仅使用 50,000 个随机样本，而非全量数据集。这可能导致 RL 的收益在更大规模训练时呈现出不同的 scaling 特性，目前无法确定全量 RL 训练是否会带来额外的边际收益或出现过拟合。

**评估指标的局限。** R2I 指标在 pycparser 失败时赋值 0 而非丢弃样本，这可能导致分数整体偏低，但影响所有方法均等。GPT-judge 评估依赖于 GPT 模型的主观判断，其一致性和与人类偏好的校准程度未进行系统验证。此外，某些基线（Nova、Ref-Decompile、D-LIFT）因未公开模型或预处理细节而被排除，这可能略微高估 SK2Decompile 的相对性能，但已包含最强的公开模型作为参照。

### 4. 开放问题

1. **跨语言泛化。** 混淆源代码 IR 的设计能否推广到 C++、Rust 等具有更复杂类型系统和编译范式的语言？IB 框架是否仍然适用，还是需要重新定义 IR 的信息压缩目标？

2. **RL 的 scaling 特性。** 当前 RL 训练仅使用 50K 样本，全量 RL 训练能否带来进一步的性能提升？编译奖励和语义奖励之间的平衡参数（隐式体现在 `r_placeholder` 的权重中）是否存在最优配置？

3. **两阶段误差传播。** Structure Recovery 阶段的错误如何影响 Identifier Naming 阶段的性能？当前论文未对级联误差进行定量分析，这一分析对于理解两阶段架构的鲁棒性至关重要。

4. **真实世界部署。** 在完全 stripped 二进制、大规模代码库、跨编译链场景下的性能退化程度如何？BringUpBench 上的初步结果（Table 7，42.3% 平均重编译率）表明仍有较大提升空间。

5. **与程序分析技术的融合。** 当前方法完全依赖 LLM 进行结构恢复，是否可以将传统的程序分析技术（如值集分析、类型推断）作为先验或约束融入 RL 奖励中，以进一步提升结构恢复的准确性？

## 原文 PDF

![[paperPDFs/ICLR_2026/SK2Decompile_LLM_based_Two_Phase_Binary_Decompilation_from_Skeleton_to_Skin.pdf]]
