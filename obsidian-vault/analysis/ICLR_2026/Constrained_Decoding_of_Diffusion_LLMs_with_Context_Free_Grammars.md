---
title: "Constrained Decoding of Diffusion LLMs with Context-Free Grammars"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Constrained_Decoding_of_Diffusion_LLMs_with_Context_Free_Grammars.pdf
openreview_forum_id: 7Sph4KyeYO
aliases:
- CDDLCFGCGRS
- CDDLCFG
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: "部分输出的可完成性（completability）：通过将目标上下文无关文法（CFG）与部分输出所有可能补全的正则语言求交，并高效判断该交集是否为空，拒绝不可完成的更新，从而在任意顺序的生成过程中始终将输出约束在目标语言内。"
primary_logic: "将扩散与填充场景下的约束解码统一为约束填充问题，利用形式语言理论中CFL与正则语言的交集构造与空性检查算法，并引入C2F+ε范式与隐式搜索等优化，首次实现了针对任意token插入顺序的实用约束解码。"
claims:
- "在MRI所有设置与模型上，方法将平均语法正确率提升至95.8%，功能正确率平均提升2.8%。"
- "在扩散语言模型上，仅使用拒绝采样（Con.−）即将语法正确率在C++、JSON、SMILES任务上分别绝对提升16.1%、14.7%和26.0%，结合自动补全后JSON可达100%语法正确。"
- "自底向上搜索仅探索生成符号，避免了交叉语言中98%–99.99%的产生式，极大提高了效率。"
- "与DINGO相比，方法在实现相近运行时开销的同时无需任何预处理，每次补全差值≤0.3秒。"
---

# Constrained Decoding of Diffusion LLMs with Context-Free Grammars

> [!tip] 核心洞察
> 将扩散与填充场景下的约束解码统一为约束填充问题，利用形式语言理论中CFL与正则语言的交集构造与空性检查算法，并引入C2F+ε范式与隐式搜索等优化，首次实现了针对任意token插入顺序的实用约束解码。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于上下文无关语法的扩散语言模型约束解码 |
| 英文题名 | Constrained Decoding of Diffusion LLMs with Context-Free Grammars |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7Sph4KyeYO); [GitHub](https://github.com/eth-sri/constrained-diffusion); [Project](https://constrained-diffusion.ai) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Constrained Decoding of Diffusion LLMs with Context-Free Grammars (CFG-guided rejection sampling) |
| Dataset | HumanEval C++ (MRI 1–3 spans), DLM tasks (C++), DLM tasks (JSON) |

> [!tip] 效果简介
> - HumanEval C++ (MRI 1–3 spans) 上，Syntax (percent correct) 为 95.8% (avg.)，对比 Vanilla varies (Con.− gives absolute gains of 5.2%–31.5% over Van.)，变化 +5.2% to +31.5% absolute over Vanilla。
> - HumanEval C++ (MRI 1–3 spans) 上，Functional (pass@1) 为 avg. +2.8% over Vanilla，对比 Vanilla，变化 +2.8% avg.。
> - DLM tasks (C++) 上，Syntax (DREAM 7B) 为 99.4 (Con.)，对比 72.0 (Van.)，变化 +27.4。

## 概述

**核心问题**：现有约束解码方法均建立在自回归模型从左到右的令牌生成范式之上，无法处理扩散语言模型（DLM）的任意顺序生成以及多区域填充（MRI）等高级生成场景。这导致在这些新兴范式中，模型的输出缺乏语法保证，严重制约了其在代码生成、结构化数据合成等任务中的可靠性。

**方法定位**：本文提出一种基于上下文无关文法（CFG）的通用约束解码框架，将扩散生成与填充场景下的约束问题统一为**约束填充问题**（Constrained Infilling Problem）。核心机制是：在每一步解码中，将当前部分输出所有可能补全构成的正则语言与目标CFG求交，通过高效判定该交集是否为空来拒绝不可完成的更新，从而在任意令牌插入顺序下始终将输出约束在目标语言内。方法引入C2F⁺ᵋ文法范式与自底向上隐式搜索等优化，将最坏情况下立方级的交集空性检查成本大幅压缩，实现了首次面向任意顺序生成的实用约束解码。

**主要结果**：
- 在MRI所有设置与模型上，方法将平均语法正确率提升至**95.8%**，功能正确率平均提升**2.8%**（Table 1）。
- 在扩散语言模型上，仅使用拒绝采样（Con.−）即将语法正确率在C++、JSON、SMILES任务上分别绝对提升**16.1%**、**14.7%**和**26.0%**；结合自动补全后，JSON可达**100%**语法正确（Table 2）。
- 与针对左到右生成的专用方法DINGO相比，本方法在实现相近运行时开销的同时**无需任何预处理**，每次补全时间差≤0.3秒（Table 9）。

**方法谱系与知识库定位**：本方法属于**基于形式语言的约束解码**分支，区别于依赖提示工程（如**Grammar Prompting**，Wang et al., 2023）或专用解析器的增量校验（如**DINGO**，Park et al., 2024）。其核心贡献在于将约束解码从“前缀可完成性”推广到“任意部分输出的可完成性”，并借助形式语言理论中CFL与正则语言的交集构造与空性检查算法，实现了生成范式无关的语法保证。

## 背景与动机

### 生成范式的演进与语法约束的缺位

大型语言模型（LLM）的生成范式正从经典的从左到右前缀补全（PRE）向更灵活的填充式生成演进。填充-中段（FIM）允许在给定的前缀与后缀之间插入代码；多区域填充（MRI）进一步支持在文本的多个任意位置同时进行补全；而扩散语言模型（DLM）则彻底打破了序列顺序，通过迭代去噪在任意位置并行插入token。这些范式在代码补全、结构化数据生成等场景中展现出巨大潜力，但其生成过程缺乏语法保证——模型输出的代码可能无法编译，JSON可能包含非法结构，SMILES分子式可能出现括号不匹配。

### 现有约束解码方法的根本局限

当前主流的约束解码方法——无论是基于掩码的token过滤、增量解析器验证，还是拒绝采样——均建立在**从左到右的序列生成假设**之上。它们依赖逐步解析器在每一步验证“下一个token”是否合法，或预先计算整个词汇表的合法掩码。这一设计隐含了两个前提：生成顺序固定为左到右，且当前已验证的前缀在后续步骤中不再改变。然而，在MRI与DLM中，模型可在任意位置插入token，已生成的部分可能被后续更新“环绕”或修改，使得基于前缀的增量验证机制完全失效。例如，在MRI中，模型可能先填充函数体中间的某个表达式，再回头补全其前面的变量声明——此时传统的逐步解析器无法判断一个孤立的表达式在当前部分上下文中是否“可完成”为一个合法程序。

### 核心问题：任意顺序生成的可完成性判定

上述困境的本质在于，现有方法仅能回答“给定前缀，下一个token是否合法”，而无法回答一个更根本的问题：**给定一个包含多个未填充区域的任意部分输出，是否存在至少一种方式将其补全为目标语言中的一个合法字符串？** 这一问题被称为“可完成性”（completability）判定。在从左到右生成中，可完成性退化为前缀合法性，但在MRI和DLM中，它成为一个非平凡的形式语言决策问题——需要判断部分输出的所有可能补全构成的正则语言与目标上下文无关文法（CFG）的交集是否为空。若交集非空，则当前部分输出是可完成的，更新可被接受；若交集为空，则无论后续如何填充，都无法产生合法输出，更新必须被拒绝。

### 本文的动机与统一框架

本文的核心动机是填补约束解码在非自回归、任意顺序生成场景中的空白。作者将MRI与DLM的约束解码统一为**约束填充问题**，并首次提出了一套实用的解决方案：将部分输出转化为描述其所有可能补全的正则语言，与目标CFG求交，并通过高效的空性检查算法实时判定可完成性。这一框架不仅首次使扩散语言模型和多区域填充具备了硬语法约束能力，还通过拒绝采样与自动补全的混合策略，在保证语法正确性的同时维持了功能正确性。

## 核心创新

### 创新动机：从“左到右”到“任意顺序”的约束解码鸿沟

现有约束解码方法（如基于逐步解析器的前缀校验或正则语言约束）均假设模型按从左到右的顺序逐token生成，并在每一步仅验证“下一个token”的合法性。这一假设在扩散语言模型（DLM）和多区域填充（MRI）场景下彻底失效——DLM在任意位置迭代插入token，MRI则需同时填充多个不连续的区域（Figure 2a）。这些生成范式下，部分输出的任意位置都可能被修改，传统的前缀完备性判定不再适用，导致这些高级生成场景长期缺乏语法保证。

本工作的核心瓶颈识别在于：**约束解码的根本困难不是“生成什么”，而是“当前部分输出是否还能被补全为一个合法字符串”**。这一可完成性（completability）判定在不限定填充顺序时，从简单的增量解析问题升级为形式语言交集非空问题。

### 核心机制：约束填充问题的统一归约

方法将MRI和DLM的约束解码统一归约为**约束填充问题**（Constrained Infilling Problem, Definition 1）：给定一个包含若干填充区（以⊔标记）的部分输出x和目标上下文无关文法（CFG）G，判断是否存在对填充区的赋值，使得最终字符串属于G定义的语言L(G)。

这一归约的关键洞察在于：**部分输出的所有可能补全构成一个正则语言Cx**。方法通过构造NFA描述Cx（Figure 2b），将其确定化并最小化为DFA（Figure 3b），然后将目标CFG与该DFA求交，得到交集文法G∩。若G∩的语言非空，则当前部分输出是可完成的，更新被接受；否则更新被拒绝（Algorithm 1, Figure 1）。

这一机制的本质是将“任意顺序生成”下的约束验证，转化为**CFL与正则语言的交集空性检查**——一个在形式语言理论中已有成熟算法的问题。

### Changed Slots：相对于基线的关键差异

| 机制槽位 | 基线方法（自回归约束解码） | 本方法 |
|---------|------------------------|------|
| **解码更新验证机制** | 仅支持左到右前缀解码，依赖逐步解析器验证下一个token | 支持任意位置插入token的扩散与多区域填充，通过将部分输出转换为带有填充区的词法序列，并验证整个填充问题的可完成性（COMPLETABLE） |
| **可完成性判定算法** | 基于前缀/左到右解析的增量校验或正则语言约束（仅限正则语言） | 将部分输出的补全语言构造为正则语言，与目标CFG求交，利用C2F+ε范式和隐式搜索高效判断交集非空 |
| **词法分析处理** | 仅对完整token序列进行词法分析 | 扩展词法分析至含有填充区的部分输出，处理边界歧义并对所有可能词素序列统一建模为NFA（Algorithm 3, Appendix C） |

### 效率优化的关键设计

交集文法G∩的规模在最坏情况下呈立方级增长：非终结符数量|V∩| ∈ O(|V||Q|²)，产生式数量|P∩| ∈ O(|P||Q|³ + |P||Q|²|Σ|)。直接构造G∩并检查空性在实际应用中不可行。

方法引入两个关键优化，将空性检查从“构造完整交集”转变为“隐式搜索”：

1. **C2F+ε范式**：将CFG规范化为一种扩展的Chomsky范式，消除产生式前缀重复（左因子分解），显著减小文法规模（Figure 3a, Appendix B.2）。

2. **自底向上隐式搜索**：所有交集符号具有形式$^p \vec{A}^q$（表示从DFA状态p到状态q推导非终结符A）。搜索从直接产生终结符或ε的符号出发，自底向上反向推导，仅探索可达的产生式。实验表明，这一策略避免了98%–99.99%的产生式探索（Section 3.2）。

### 自动补全：从拒绝到主动修复

当模型连续多次采样无效更新后，方法不仅拒绝这些更新，还从交集语言L∩中采样一个具体的补全字符串（Completion Sampler）。这相当于在模型“卡住”时，由形式语言系统接管并提供一个保证合法的完成方案。该机制使语法正确率从不带补全的Con.−进一步提升至平均95.8%（Table 1），在JSON任务上可达100%（Table 2）。

### 理论保证

方法具备三个形式化保证（Section 3.4）：
- **可靠性（Soundness）**：所有生成的输出均符合目标文法和词法规则。
- **完备性（Completeness）**：任何能导致合法输出的token更新都不会被拒绝。
- **最小侵入性（Minimally Invasive）**：若无约束的模型原本就会生成合法输出w ∈ L，则施加约束后模型仍会生成w。

这些保证将约束解码从启发式过滤提升为具有形式化正确性基础的推理框架。

## 整体框架

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/001_Figure_1.jpg]]
*Figure 1: An overview of our approach. In each step, the input consists of a partial text x with arbitrarily many infilling regions and a context-free grammar (CFG) specifying formal constraints. During decoding, we sample an updated input $x ^ { \prime }$ from M , , obtained, e.g., by inserting a token in one of the regions in x. Our method then intersects the CFG with the regular language of all possible completions of $x ^ { \prime }$ . . If the intersection is empty, the update is rejected and a new $x ^ { \prime }$ is sampled. Otherwise, it is accepted and the decoding continues from $x ^ { \prime }$ . . In the example, the invalid update inserting "foo()" is rejected and "foo" is accepted instead

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/003_Figure_2.jpg]]
*Figure 2: We consider three left-to-right (PRE, FIM, MRI) and one out-of-order (DLM) generation paradigms (a). The NFA in (b) describes the language of all additive completions for the MRI task*

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/004_Figure_3.jpg]]
*Figure 3: Examples of Figures 1 and 4 processed during our method. (a) The grammar is first normalized into $\mathrm { \bar { C } }$ 2 $\mathrm { F } ^ { + \varepsilon }$ , and (b) the NFA is transformed into a minimal DFA. (c) To determine emptiness of $L _ { \cap }$ , the algorithm then searches the initial stat$e ^ { d 0 } \vec { S } ^ { d 7 }$ through the productions in reverse, starting from the terminals

该方法将扩散语言模型（DLM）与多区域填充（MRI）中的约束解码统一为**约束填充问题**（Definition 1），其核心是一个迭代的拒绝采样循环（Algorithm 1）。整体流程由四个关键模块串联而成，形成“更新—验证—拒绝/接受—补全”的闭环。

### 输入与输出

**输入**包含两部分：
1. 一个包含任意数量填充区（以特殊符号 `⊔` 标记）的部分输出文本 `x`；
2. 一个目标上下文无关文法（CFG），指定生成文本须满足的形式约束。

**输出**为完全填充且符合目标文法的完整文本。

### 核心循环（Algorithm 1）

每一步迭代中，系统执行以下操作：

1. **采样更新**：从底层模型 `M` 采样一个对当前部分输出 `x` 的增量修改 `x'`。在 MRI 场景中，这对应于在某个填充区插入一个 token；在 DLM 场景中，则是对任意掩码位置进行 token 替换。

2. **可完成性验证**：调用 `COMPLETABLE(x')` 判定器，检查是否存在对 `x'` 中所有填充区的合法补全，使得最终字符串属于目标语言。该判定是整个方法的核心技术瓶颈。

3. **拒绝/接受**：
   - 若 `COMPLETABLE(x')` 返回假，则拒绝该更新，重新采样新的 `x'`；
   - 若返回真，则接受更新，将 `x` 替换为 `x'`，继续下一轮迭代。

4. **自动补全**（Con. 模式）：当模型连续多次无法产生可完成更新时，系统从有效补全的交集语言中直接采样一个具体补全字符串，将部分输出强制完成。该机制回收了因超时或模型能力不足而无法自行完成的样本。

### 模块关系与数据流

```
部分输出 x (含填充区) + CFG
         │
         ▼
┌─────────────────────┐
│  1. Partial Output  │  将含填充区的Unicode文本转换为
│     Lexer           │  所有可能词素序列的NFA
└────────┬────────────┘
         │ 词素序列NFA
         ▼
┌─────────────────────┐
│  2. Regular Lang.   │  构造描述所有可能补全的
│     Constructor     │  正则语言 NFA/DFA
└────────┬────────────┘
         │ 补全语言 DFA
         ▼
┌─────────────────────┐
│  3. Intersection &  │  将CFG与补全DFA求交，用隐式搜索
│     Emptiness Check │  判定交集是否为空
└────────┬────────────┘
         │ 可完成？(是/否)
         ▼
     ┌───┴───┐
     │ 是/否 │──否──▶ 拒绝更新，重新采样
     └───┬───┘
         │ 是
         ▼
    接受更新，继续迭代
         │
         │ (多次拒绝后触发)
         ▼
┌─────────────────────┐
│  4. Completion      │  从有效交集中采样具体补全字符串
│     Sampler         │
└─────────────────────┘
```

### 关键技术决策

- **可完成性判定的形式化归约**：将“是否存在合法填充”归约为检查交集语言 `L∩ = L(G) ∩ C(x')` 是否为空，其中 `L(G)` 为目标 CFG 描述的语言，`C(x')` 为所有可能补全构成的正则语言。这一归约使得问题可通过形式语言理论的标准工具求解。

- **效率优化**：交集文法的规模在最坏情况下呈立方级增长（`|V∩| ∈ O(|V||Q|²)`，`|P∩| ∈ O(|P||Q|³ + |P||Q|²|Σ|)`）。为避免显式构造整个交集，方法采用**隐式搜索**策略——从终结符出发自底向上推导，仅探索生成符号，在实际任务中避开了 98%–99.99% 的产生式。同时引入 **C2F+ε 范式**（左因子分解等文法化简）进一步控制文法规模。

- **词法分析扩展**：传统词法分析仅处理完整 token 序列，而该方法将其扩展至含填充区的部分输出，通过构造 NFA 统一建模所有可能的词素边界歧义，再将 NFA 确定化、最小化为 DFA 供交集模块使用。

### 理论保证

该方法满足三项理论性质：
- **健全性**：所有生成输出均符合目标文法和词法规则；
- **完备性**：允许采样任何能产生合法输出的 token，不预先排除有效路径；
- **最小侵入性**：若无约束模型 `M` 本身能生成合法输出 `w ∈ L`，则施加约束后仍会生成该输出，不会因约束引入新的偏差。

## 核心模块与公式推导

### 约束填充问题形式化

方法将扩散语言模型（DLM）与多区域填充（MRI）的约束解码统一为**约束填充问题**（Definition 1）：给定部分输出 $\mathbf{x} = x_1 \sqcup x_2 \ldots \sqcup x_n$（其中 $\sqcup$ 表示填充区域）和目标上下文无关文法 $G$，判断是否存在对填充区域的赋值，使得完整字符串属于 $L(G)$。这一决策问题称为 COMPLETABLE，是全部后续算法的核心判定原语（Algorithm 1）。

### 关键公式与变量含义

**DFA 定义**

$$(Q, \Sigma, \delta, q_0, F)$$

- $Q$：有限状态集
- $\Sigma$：输入字母表
- $\delta: Q \times \Sigma \to Q$：状态转移函数
- $q_0 \in Q$：初始状态
- $F \subseteq Q$：接受状态集

**CFG 定义**

$$(V, \Sigma, P, S)$$

- $V$：非终结符集
- $\Sigma$：终结符集
- $P$：产生式规则集
- $S \in V$：起始符号

**交集文法符号形式**

$$^p \vec{A}^q$$

表示从 DFA 状态 $p$ 推导至状态 $q$ 的过程中生成非终结符 $A$。所有交集文法中的符号均采用此三元组形式，将 CFG 推导与 DFA 状态转移耦合。

**交集文法规模上界**

$$|V_{\cap}| \in O(|V||Q|^2) \quad \text{且} \quad |P_{\cap}| \in O(|P||Q|^3 + |P||Q|^2|\Sigma|)$$

该立方级复杂度反映了将 CFG 与 DFA 求交后文法规模的理论最坏情况增长。非终结符数量与 $|V|$ 和 $|Q|^2$ 成正比，产生式数量则进一步受 $|Q|^3$ 和 $|\Sigma|$ 影响。这一上界是后续优化设计的直接动因。

**左因子分解规则**

$$A \to \alpha A', \quad A' \to \beta, \quad A' \to \beta'$$

用于消除产生式前缀重复（如 $A \to \alpha\beta$ 与 $A \to \alpha\beta'$ 共享前缀 $\alpha$），通过引入辅助非终结符 $A'$ 压缩文法规模，是 C2F$^{+\varepsilon}$ 范式中的核心化简步骤。

### 流水线模块

**模块一：部分输出词法分析器（Partial Output Lexer）**

将含填充区域的 Unicode 文本转换为可能的词素（terminal）序列的 NFA。与常规词法分析不同，该模块需处理填充区边界的歧义——填充区两侧的字符可能被不同词法规则切分。模块通过构造并行的词法路径（union automaton）和跳跃连接（skip connection），将所有合法词素序列统一编码为单一 NFA（Algorithm 3, Figure 5–6）。

**模块二：正则语言构造器（Regular Language Constructor）**

根据当前部分输出构建描述所有可能补全的正则语言 $C_{\mathbf{x}}$。首先构造接受 $C_{\mathbf{x}}$ 的 NFA，随后转换为等价的极小化 DFA（Figure 3b）。该 DFA 的每个状态对应部分输出在词法层面的“完成进度”，接受状态对应可合法结束的补全位置。

**模块三：交集与空性检查器（Intersection & Emptiness Checker）**

将目标 CFG 与 $C_{\mathbf{x}}$ 对应的 DFA 求交，判断 $L_{\cap}$ 是否为空。核心优化包括：

- **C2F$^{+\varepsilon}$ 范式**：将 CFG 规范化为无 $\varepsilon$ 产生式（除起始符号外）且无单元产生式的二元形式，配合左因子分解压缩文法规模（Figure 3a）。
- **隐式搜索**：不显式构造完整的 $G_{\cap}$，而是从终结符出发自底向上搜索可生成的 $^p \vec{A}^q$ 符号。搜索仅沿实际可达的产生式展开，避免了 98%–99.99% 的产生式探索。

**模块四：补全采样器（Completion Sampler）**

当模型连续多次拒绝无效更新后，从 $L_{\cap}$ 中采样一个具体补全字符串。采样时需将交集文法生成的词素序列与当前部分输出的 Unicode 正则语言再次求交，确保补全文本在字符层面与已有输出无缝拼接。

## 实验与分析

### 主结果：多区域填充（MRI）与扩散语言模型（DLM）的语法与功能正确性

方法在两类非自回归生成范式上均实现了语法正确性的显著跃升，并保持或提升了功能正确性。核心机制在于：通过拒绝不可完成的更新，将任意顺序的token插入始终约束在目标上下文无关语言内；当模型连续拒绝后，自动补全（Con.）从有效交集中采样具体字符串，回收部分失败样本。

**MRI场景（Table 1）**：在HumanEval C++的单区域至三区域填充任务上，约束解码（Con.−）将语法正确率相对于无约束基准（Van.）绝对提升5.2%–31.5%。自动补全（Con.）进一步回收超时或无法完成的样本，将平均语法正确率推至**95.8%**。功能正确率（pass@1）平均提升**2.8%**，表明语法约束不仅未损害功能质量，反而通过排除无效结构使模型更易生成可执行代码。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/005_Table_1.jpg]]
*Table 1: Our method consistently improves the percentage of syntactically and functionally correct infillings for varying numbers of regions in MRI under standard decoding (Van.), constrained decoding (Con.−), and completing partially completed outputs (Con.)*

**DLM场景（Table 2）**：在C++、JSON、SMILES三类结构化生成任务上，仅使用拒绝采样（Con.−）即带来显著增益。以DREAM 7B为例：C++语法正确率从72.0%升至**99.4%**（+27.4），JSON从59.2%升至**100.0%**（+40.8），SMILES从26.7%升至**99.4%**（+72.7）。值得注意的是，非约束性基线**Grammar Prompting**（G.P.，Wang et al., 2023）并未一致提升语法或语义性能，说明软提示无法替代硬约束。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/006_Table_2.jpg]]
*Table 2: Constrained decoding (Con.−) consistently increases the percentage of syntactically correct completions for DLMs over standard decoding (Van.). Non-constraining baselines like Grammar prompting (G.P.) do not consistently improve syntactic or semantic performance*

### 消融实验：组件贡献与扩散步数影响

**自动补全的边际贡献**：在MRI中，Con.−已提供大部分语法增益，Con.在此基础上回收失败样本，使语法正确率逼近天花板。在DLM中，Con.−将JSON语法正确率从59.2%推至100%，自动补全在此场景下边际贡献为零（已完美）；但在C++和SMILES上，Con.可进一步回收少量失败案例。

**扩散步数消融（Table 5, Table 6）**：在DREAM 7B上，约束解码在16–256步的所有设置下持续提升语法正确性，即使模型自身精度随步数增加而提高。步数越多，运行时开销越低：从16步时的14%–108%降至256步时的9%，甚至出现1%的加速。这一反直觉现象源于：更多扩散步数使模型单次生成质量更高，减少了被拒绝的无效更新次数，从而降低了验证开销的累积。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/013_Table_5.jpg]]
*Table 5: Percent syntactically and functionally correct generations for DREAM 7B based on varying number of diffusion steps. Our method consistently increases syntactic correctness in all settings, even when model accuracy increases with step sizes*

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/014_Table_6.jpg]]
*Table 6: Time difference per completion for different step sizes on DREAM 7B diffusion, in seconds, and the percentual overhead over the original completion. For larger numbers of diffusion steps, overhead reduces from 14% − 108% down to 9% or even a speedup of 1%*

**行级删除MRI（MRI-L, Table 7）**：在移除完整代码行的填充场景中，约束解码同样一致提升语法和功能正确性，证明方法对不同粒度的填充区域具有鲁棒性。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/015_Table_7.jpg]]
*Table 7: When infilling between 1 and 3 missing lines, our method consistently improves syntactic and functional correctness. Shown below the results of MRI-L under standard decoding (Van.), constrained decoding (Con.−), and completing partially completed outputs (Con.)*

### 运行时效率与可扩展性

**MRI每token开销（Table 3）**：约束解码的中位每token开销为4.2 ms。较大模型（如33B）因推理时间本身更长，相对开销更低（13%–28%），而较小模型（1.3B）相对开销可达158%–557%。填充区域数量增加会提高开销，因为正则语言与交集文法的规模随之增长。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/011_Table_3.jpg]]
*Table 3: Median overhead per token for different infilling settings in milliseconds and percent increase over unconstrained generation. Larger models with higher inference time experience a lower slowdown due to constraining. More infilling regions also increase constraining overhead*

**DLM每次完成开销（Table 4）**：中位完成时间差仅0.1秒。当模型无法采样出有效完成而提前中止时，可能出现加速。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/012_Table_4.jpg]]
*Table 4: Median time difference per completion for different diffusion models in seconds, and the overhead over the original completion in percent. When the completion aborts pre-emptively, as no valid completion is sampled from the model, speed-ups are possible*

**与DINGO对比（Table 8, Table 9）**：在JSON-NOUS上，本方法（Con.）达到与**DINGO**（Park et al., 2024）相同的100%语法正确率；在GSM8K-SYMBOLIC上，DINGO略优。关键差异在于预处理：DINGO需要11.9–37.0秒的schema预处理，而本方法无需任何预处理（0秒），每次完成的时间差≤0.3秒，与DINGO的0.1秒处于同一量级。这使本方法在需要即时切换文法的场景中更具实用性。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/017_Table_9.jpg]]
*Table 9: Pre-procesing time (PreX) and time difference per completion of DINGO and our method (Con.). We observe that our method has a similar runtime overhead as DINGO while requiring no preprocessing. Notably, preprocessing is done once per schema, which implies once per task on the JSON-NOUS dataset*

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_7Sph4KyeYO/figures/016_Table_8.jpg]]
*Table 8: On JSON-NOUS, our method (Con.) achieves the same performance as DINGO. On GSM8K-SYMBOLIC, DINGO slightly outperformsn Con*

### 失败模式与剩余语法错误

尽管方法将语法正确率推向极高水平，仍存在两类残余错误（Figure 8）：

1. **令牌预算不足**：当模型已达到最大生成令牌数，但填充区仍需更多令牌才能完成语法结构时，约束解码无法拯救。这在MRI和DLM中均会出现——前者因超出令牌上限，后者因可用的掩码令牌（⊥）耗尽。
2. **自动补全的非概率性**：Con.从交集中采样补全字符串时不依赖模型概率分布，可能降低输出与上下文的相关性。这解释了为何功能正确率的提升幅度小于语法正确率。

### 案例分析（Table 10）

三个典型案例揭示了约束解码的实际作用机制：
- **JSON类型强制**：DREAM 7B在生成金融评论摘要时，无约束版本错误地输出字符串类型值，约束解码强制生成正确数值类型。
- **SMILES括号平衡**：DREAMCODER 7B生成分子式时，无约束版本多闭合了括号，约束解码阻止了这一无效操作。
- **C++语法补全**：DeepSeek Coder 6.7B在编写字符串处理函数时遗漏if语句条件的括号，约束解码自动补全了缺失的括号。

这些案例表明，方法的核心价值在于实时拦截违反形式语法的更新，而非事后修复——这正是其“最小侵入性”性质的体现：若模型自身能生成有效输出，约束解码不会改变该输出。

## 方法谱系与知识库定位

### 1. 与现有约束解码方法的关系

本工作处于**约束解码**与**扩散语言模型**的交叉地带，其核心贡献在于将约束解码的适用范围从自回归模型的左到右生成，首次系统性地拓展至任意顺序的token生成范式。

**与自回归约束解码基线的关系。** 传统约束解码方法（如基于前缀解析器的增量校验、正则语言掩码等）均假设生成过程严格遵循从左到右的顺序，因而无法直接应用于多区域填充（MRI）和扩散语言模型（DLM）这类允许在任意位置插入token的场景。本文通过将问题统一形式化为**约束填充问题**（Definition 1），使得这一鸿沟得以弥合。在左到右生成的特殊情况下（PRE/FIM），本方法退化为现有约束解码的特例；但在MRI和DLM场景下，本方法是目前唯一提供形式化语法保证的方案。

**与DINGO的直接比较。** **DINGO**（Park et al., 2024）是针对左到右生成的语法约束方法，在JSON-NOUS和GSM8K-SYMBOLIC任务上被用作直接基线。实验表明（Table 8），在JSON-NOUS上，本方法（Con.）与DINGO达到相同的100%语法正确率；在GSM8K-SYMBOLIC上，DINGO在功能正确性上略优于本方法，这反映了DINGO针对算术任务的专门优化。然而，本方法的关键优势在于**零预处理**：DINGO需要针对每个schema进行一次性预处理，而本方法无需任何预处理即可达到相近的运行时开销（每次补全差值≤0.3秒，Table 9）。

**与Grammar Prompting的关系。** **Grammar Prompting**（Wang et al., 2023）将文法规则以文本形式注入系统提示，但不施加硬约束。实验一致表明（Table 2），该方法不能持续提升语法或语义性能，在某些情况下甚至导致功能正确性下降。这印证了软约束方法在需要严格语法保证的场景中的根本局限。

### 2. 方法适用边界

**支持的生成范式。** 本方法统一支持四种生成范式：前缀生成（PRE）、填空生成（FIM）、多区域填充（MRI）和扩散语言模型（DLM）。其中MRI和DLM是此前约束解码方法无法处理的核心场景。

**支持的语言类。** 方法目前仅支持**上下文无关语言**（CFL），通过用户提供的上下文无关文法（CFG）和词法分析器（lexer）进行约束。这意味着：
- 可以保证语法正确性（如括号匹配、JSON结构、C++语法、SMILES分子式规范）；
- 无法直接处理上下文敏感语义特征（如类型约束、变量作用域检查），这些需要结合类型检查器等语义工具。

**模型兼容性。** 实验覆盖了多种规模的模型（1.3B至33B参数），包括StarCoder2、CodeGemma、DeepSeek Coder系列以及多个扩散语言模型（DREAM 7B、DREAMCODER 7B、LLADA 8B、DIFFUSIONCODER 7B）。方法对不同模型均表现出一致的语法正确性提升，且模型越大，约束解码的相对运行时开销越低（Table 3）。

### 3. 局限性与已知失败模式

**令牌不足导致的语法残差。** 剩余语法错误主要源于对填充区可容纳token数量的过度近似。当模型生成的token数达到上限（实验中统一限制为256），但语法约束要求更多token才能完成有效补全时，输出将不可避免地包含语法错误（Figure 8）。这一局限在MRI和DLM场景中均有出现。

**重复计算的运行时开销。** 当前实现未集成增量解析，每次token更新后需重新计算交集空性，带来重复开销。虽然自底向上的隐式搜索避免了98%–99.99%的产生式探索，但运行时开销仍随文法规模和填充区数量增加（Table 3, Figure 7），对于极复杂文法可能影响交互式使用体验。

**自动补全的概率盲区。** 自动补全机制（Con.）虽然能回收部分因超时或无法完成而失败的样本，将平均语法正确率推至95.8%，但其从交集语言中采样时不依赖模型的概率分布，可能降低生成文本的连贯性和相关性。

**上下文敏感语义的缺失。** 方法无法保证类型正确性、变量定义与使用的一致性等上下文敏感属性。在GSM8K-SYMBOLIC任务上功能正确性略低于为算术量身优化的DINGO，体现了通用CFG方法在语义约束上的固有局限。

### 4. 开放问题与研究前景

1. **精确令牌预算建模。** 如何精确建模填充区可使用的剩余token数量，在表达力与正则语言/交集文法规模之间取得更优平衡，是减少令牌不足导致的语法残差的关键。

2. **增量解析与缓存机制。** 能否通过增量解析和缓存先前的交集结果，大幅降低步骤间验证的平摊开销，使方法在更大规模文法下依然保持实用效率？

3. **向上下文敏感语言拓展。** 如何将方法扩展到上下文敏感语言（如类型约束），通过与类型检查器等语义工具的协同，实现语法与语义的双重保证？

4. **概率感知的自动补全。** 如何在自动补全阶段引入模型的概率偏好，使补全结果既满足语法约束，又保持与上下文的高度连贯性？

5. **与扩散解码策略的协同。** 能否将本方法与其他扩散解码策略（如迭代精化、分类器引导）结合，在保证语法正确性的同时进一步提升功能正确性？

6. **模型训练层面的改进。** 如何训练模型在需要更多填充token时主动发出信号，或学习在约束解码的拒绝采样过程中更高效地生成有效更新，从根本上缓解令牌不足和运行时开销问题？

## 原文 PDF

![[paperPDFs/ICLR_2026/Constrained_Decoding_of_Diffusion_LLMs_with_Context_Free_Grammars.pdf]]
