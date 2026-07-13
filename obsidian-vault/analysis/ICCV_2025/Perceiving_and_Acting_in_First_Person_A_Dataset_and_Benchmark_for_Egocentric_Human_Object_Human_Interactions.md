---
title: Perceiving and Acting in First Person A Dataset and Benchmark for Egocentric Human Object Human Interactions
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Perceiving_and_Acting_in_First_Person_A_Dataset_and_Benchmark_for_Egocentric_Human_Object_Human_Interactions.pdf
project_link: null
code_link: null
aliases:
- FDODSDD
- PAFPDBEHOHI
tags:
- ICCV_2025
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 对 FC-Datalog 规则的语法施加系统性限制（线性性、确定性、单字母前瞻 OLLA、严格递减 SD 等），在表达力与复杂度之间建立可控的权衡。
primary_logic: 通过将 FC-Datalog 规则限制在‘单字母前瞻确定性’（DOLLA）片段内，可以在保持 LOGSPACE 表达力的同时，实现多项式时间的确定性检查和线性时间的模型检验，从而为具体应用（如模拟确定性正则表达式 DRX）提供了可定制的查询框架，并在 DOLLA+ 中进一步降低编写成本。
claims:
- 全 FC-Datalog 的联合复杂度为 EXP-完全。
- DOLLA FC-Datalog 捕获 LOGSPACE，且 OLLA 程序的确定性可在多项式时间内检查。
- 严格递减的 DOLLA FC-Datalog（SD-DOLLA）具有线性联合复杂度。
- SD-DOLLA(+) FC-Datalog 可以简洁地模拟确定性正则表达式（DRX），验证了框架的实用价值。
---

# Perceiving and Acting in First Person A Dataset and Benchmark for Egocentric Human Object Human Interactions

> [!tip] 核心洞察
> 通过将 FC-Datalog 规则限制在‘单字母前瞻确定性’（DOLLA）片段内，可以在保持 LOGSPACE 表达力的同时，实现多项式时间的确定性检查和线性时间的模型检验，从而为具体应用（如模拟确定性正则表达式 DRX）提供了可定制的查询框架，并在 DOLLA+ 中进一步降低编写成本。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于FC-Datalog的高效字符串查询框架 |
| 英文题名 | Perceiving and Acting in First Person A Dataset and Benchmark for Egocentric Human Object Human Interactions |
| 会议/期刊 | ICCV 2025 |
| Links |  |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | 受限 FC-Datalog 片段框架（线性、确定性、OLLA/DOLLA、SD-DOLLA 及 DOLLA+） |
| Dataset |  |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

**问题**：全 FC-Datalog 的模型检查联合复杂度为 **EXP-完全**，且其确定性检查等价于字方程可满足性问题（**NP 难**）。这使得直接使用全片段进行高效字符串查询在计算上不可行，亟需在表达力与复杂度之间建立可控的权衡。

**核心思路**：对 FC-Datalog 规则的语法施加系统性限制——线性性、确定性、单字母前瞻（OLLA）、严格递减（SD）等——构造一系列复杂度逐级降低的受限片段。关键洞察在于：将规则约束在 **“单字母前瞻确定性”**（DOLLA）片段内，可以在保持 LOGSPACE 表达力的同时，将确定性检查降至多项式时间，并将模型检验降至线性时间（对 SD-DOLLA 子片段），从而为具体应用提供可定制的查询框架。

**方法定位**：本文属于 **纯理论分析**，未包含实验评估。工作沿两条轴线展开：
- **复杂度分级**：从非受限 FC-Datalog（EXP-完全）→ 线性 FC-Datalog（NLOGSPACE）→ 确定性线性 FC-Datalog（LOGSPACE）→ DOLLA / SD-DOLLA（多项式/线性联合复杂度），逐级收紧语法约束以换取效率。
- **表达力验证**：以 **确定性正则表达式（DRX）** 为基准应用，证明 SD-DOLLA 和 DOLLA+ 可简洁地模拟 DRX，验证了框架的实用价值。

**主要结果**：
- **DOLLA FC-Datalog 捕获 LOGSPACE**，且 OLLA 程序的局部与全局确定性可在多项式时间内判定。
- **SD-DOLLA** 在 O(n|Σ|) 预处理后，模型检查仅需 O(|w|·k) 时间，达到线性联合复杂度。
- **DOLLA+** 通过放宽模式方程形状限制，以更少的规则数量实现 DRX 模拟，降低了编写成本。

**局限与待解问题**：确定性线性 FC-Datalog 的确定性检查仍为 NP 难；DOLLA 与确定性线性片段之间的表达力-复杂度权衡尚未完整映射；SD-DOLLA 的线性复杂度依赖严格递减的强假设，并非所有有用查询均可自然表达。



### 问题背景：从文档 Spanner 到递归字符串查询

现代信息提取（Information Extraction）的核心任务之一是从非结构化文本中识别并捕获结构化关系。**文档 Spanner**（document spanner）框架为此提供了一种形式化基础：它将提取规则表示为一组变量到文本片段（span）的映射，并通过正则关系（由正则表达式定义）来约束这些片段。然而，基础 Spanner 在表达力上存在天然限制——它无法直接表达递归结构，例如嵌套的依赖关系或层次化的文本模式。

为突破这一限制，**FC-Datalog** 被提出。FC-Datalog 在 **FC**（带字方程的合取查询片段）之上引入递归，其方式类似于传统 Datalog 在存在正一阶逻辑（existential-positive FO）之上引入递归。具体而言，FC-Datalog 程序是一个三元组 $P := (\mathfrak{u}, \mathscr{R}, \Phi)$，其中 $\mathfrak{u}$ 为全域变量（代表整个输入词），$\mathscr{R}$ 为关系符号集，$\Phi$ 为规则集。每条规则由关系原子与**模式方程**（pattern equation，形如 $x \doteq y z$ 的字方程）组成，其语义通过基于输入词 $w$ 的 $w$-代入和最小不动点来定义。

FC-Datalog 的表达力十分强大：其存在正片段 EP-FC[REG] 已能捕获核心 Spanner（core spanner）的表达力，而扩展的 FC[REG] 则可捕获广义核心 Spanner。这使得 FC-Datalog 成为字符串查询领域一个极具吸引力的统一框架。

### 核心瓶颈：全 FC-Datalog 的复杂度障碍

尽管 FC-Datalog 表达力强大，但直接将其用于高效字符串查询面临根本性的复杂度障碍。理论分析表明，**全 FC-Datalog 的模型检查联合复杂度为 EXP-完全**（Theorem 3.1）。这意味着在最坏情况下，判定一个词是否被程序接受所需的时间随程序规模呈指数增长，这对于任何实际应用而言都是不可接受的。

更棘手的是，即便对程序施加**线性限制**（linear restriction，即每条规则最多含一个与头关系符号相互递归的体原子），确定性检查问题依然等价于**字方程可满足性问题**——这是一个经典的 NP 难问题。因此，即使是线性 FC-Datalog 片段，在查询执行前验证程序是否具有良好行为（确定性）的成本也可能高得难以承受。

### 现有方法缺口与本文动机

上述复杂度障碍揭示了一个关键的方法缺口：**在 FC-Datalog 的表达力与可高效评估性之间，缺乏系统性的、可定制的权衡机制**。已有工作虽然识别出线性 FC-Datalog 捕获 NLOGSPACE、确定性线性 FC-Datalog 捕获 LOGSPACE 等理论结果，但并未提供一套实用的语法限制框架，使得：

1. **片段成员资格可高效检查**：能够在多项式时间内判定一个给定程序是否属于某个低复杂度片段；
2. **模型检查可高效执行**：对于属于该片段的程序，能够在输入词规模的多项式甚至线性时间内完成模型检查；
3. **表达力可控且实用**：受限片段仍能自然表达实际查询需求，如模拟确定性正则表达式（DRX）等。

本文的核心动机正是填补这一缺口：通过对 FC-Datalog 规则的语法施加一系列系统性限制（线性性、确定性、单字母前瞻 OLLA、严格递减 SD 等），在表达力与复杂度之间建立可控的权衡，从而将 FC-Datalog 转化为一个**可定制的、高效字符串查询框架**。



## 核心方法与创新机理

本文的核心创新在于对 FC-Datalog 的规则语法施加系统性的受限层阶，在保留足够字符串查询表达力的前提下，将全片段的 EXP-完全联合复杂度逐步降低至可高效处理的级别。这一框架的关键洞察是：**通过将规则限制在“单字母前瞻确定性”（DOLLA）片段内，可以在 LOGSPACE 表达力、多项式时间确定性检查与线性时间模型检验之间建立可控的三元权衡**。

### 从全 FC-Datalog 到受限片段的核心演进

全 FC-Datalog 的联合复杂度为 EXP-完全（Theorem 3.1），且其确定性检查等价于字方程可满足性问题（NP 难），这使得直接使用全片段进行字符串查询在理论和实践上均不可行。本文通过四个逐步收紧的 **changed slots** 构建了复杂度递减的片段谱系：

#### Slot 1：规则线性性（Linearity）

- **基线**（全 FC-Datalog）：规则体可包含多个与头关系符号相互递归的原子，例如 `Ans(z) ← z ≐ x y, Ans(x), Ans(y)` 中同时出现两个 `Ans` 体原子，形成非线性递归。
- **创新**：每条规则最多含一个与头关系符号相互递归的体原子（Definition 3.2），将程序限制为**线性 FC-Datalog**。
- **效果**：线性片段将捕获的复杂度类从 EXP 降至 **NLOGSPACE**（Theorem 3.4），但确定性检查仍是 NP 难的，未能解决可用性问题。

#### Slot 2：局部与全局确定性（Determinism）

- **基线**（线性 FC-Datalog）：模式方程组合可产生一对多的变量赋值关系，且同一关系符号的多条规则可能处理重叠的顶部输入。
- **创新**：引入两层确定性约束（Definition 3.9）——
  - **局部确定性**：每条规则的模式方程关系 `W_ρ` 必须构成偏函数，即给定顶部变量赋值，体变量的解若存在则唯一；
  - **全局确定性**：同一关系符号的不同规则，其合法输入集合互不相交，消除规则选择歧义。
- **效果**：确定性线性 FC-Datalog 将复杂度进一步压缩至 **LOGSPACE**（Theorem 3.11），但确定性检查本身仍是 NP 难的——因为检查字方程是否定义偏函数等价于字方程可满足性问题。

#### Slot 3：单字母前瞻（OLLA）——决定性突破

- **基线**（确定性线性 FC-Datalog）：模式方程可为任意形式的字方程 `α ≐ β`，使确定性检查不可行。
- **创新**：每个模式方程必须具有 `x ≐ y a`、`x ≐ a y` 或 `x ≐ ε` 的形式（Definition 3.14），即**单字母前瞻（OLLA）**限制。这一约束使得每条规则可从其模式方程中提取 **profile 函数** `pro_ρ(x) ∈ {a, ε, ⊥}`，将确定性条件转化为 profile 之间的简单相容性判定。
- **效果**：这是全文最关键的 **causal knob**——
  - **确定性检查**：OLLA 程序的局部与全局确定性可在**多项式时间**内判定（Proposition 3.20），彻底解决了可用性瓶颈；
  - **表达力**：DOLLA（确定性 OLLA）片段精确捕获 **LOGSPACE**（Theorem 3.17），与确定性线性 FC-Datalog 表达力相当，但具有可判定的成员资格检查；
  - **联合复杂度**：DOLLA 的联合复杂度为 PSPACE-完全，虽较全片段有显著改善，但仍未达到线性。

#### Slot 4：严格递减性（SD）——实现线性时间

- **基线**（DOLLA）：变量长度在推导过程中可能保持不变或增加，导致模型检查需要维护任意长度的推导链。
- **创新**：每条规则保证某个变量的长度严格递减（Section 3.4），形成**严格递减 DOLLA（SD-DOLLA）**片段。
- **效果**：SD-DOLLA 实现了 **O(|w|·k) 线性联合复杂度**（Theorem 3.23），仅需 O(n|Σ|) 预处理即可在输入词长度线性时间内完成模型检查。这是通过基于查找表的前向模型检查算法实现的——严格递减性保证了推导深度有界，从而使动态规划成为可能。

### 实用验证：模拟确定性正则表达式

为验证框架的实际价值，本文证明了 SD-DOLLA（及扩展版本 DOLLA+）可以**简洁地模拟确定性正则表达式（DRX）**（Theorem 4.3, Theorem 4.10）。DRX 是正则表达式的一个确定性子类，在文档处理和模式匹配中广泛应用。该模拟不仅展示了受限片段的表达能力，还揭示了 DOLLA+ 如何通过允许更灵活的模式方程（如 `u ≐ x_n' v`）进一步降低规则编写成本，在保持线性复杂度的同时提升可用性。

### 创新总结

综上，本文的核心创新并非单一技术，而是一个**系统性的片段设计方法论**：通过在规则线性性、确定性、前瞻形状和递减性四个维度上施加协同约束，在 FC-Datalog 的表达力与计算复杂度之间建立了精细可控的权衡空间。其中，OLLA 限制的引入是打破“确定性检查不可行”瓶颈的关键转折点，而 SD 限制则进一步将复杂度推至实用的线性边界。



本文提出的框架并非一个端到端的工程流水线，而是一套**通过语法限制对 FC-Datalog 进行表达能力与计算复杂度分层控制的理论体系**。其核心思想是：从表达能力最强但计算代价极高的全 FC-Datalog（联合复杂度 EXP-完全）出发，通过逐级施加规则形态约束，构造出多个具有可判定确定性和可接受复杂度的子片段，从而为高效字符串查询提供可定制的逻辑基础。

### 框架的输入与输出

框架的输入是一个 FC-Datalog 程序 $P := (\mathfrak{u}, \mathscr{R}, \Phi)$（Definition 2.1），其中 $\mathfrak{u}$ 为全域变量，$\mathscr{R}$ 为关系符号集，$\Phi$ 为规则集。给定一个输入词 $w \in \Sigma^*$，框架的输出是判定 $w$ 是否属于程序 $P$ 定义的语言 $L(P)$，即模型检查问题的布尔结果。

### 语法限制的分层体系

框架的核心操作是在规则集 $\Phi$ 上施加以下逐级增强的语法限制，每一级都在表达力与复杂度之间建立新的权衡点：

| 限制层级 | 关键约束 | 表达力 | 联合复杂度 |
|---------|---------|--------|-----------|
| 全 FC-Datalog | 无限制 | 递归可枚举 | EXP-完全（Theorem 3.1） |
| 线性 FC-Datalog | 每条规则体最多含一个与头关系符号相互递归的原子（Definition 3.2） | NLOGSPACE（Theorem 3.4） | PSPACE-完全 |
| 确定性线性 FC-Datalog | 局部确定性（$W_\rho$ 为偏函数）+ 全局确定性（不同规则输入互不相交）（Definition 3.9） | LOGSPACE（Theorem 3.11） | 确定性检查等价于字方程可满足性（NP 难） |
| OLLA FC-Datalog | 每个模式方程形如 $x \doteq y\mathsf{a}$、$x \doteq \mathsf{a}y$ 或 $x \doteq \varepsilon$（Definition 3.14） | LOGSPACE | 确定性检查为多项式时间（Proposition 3.20） |
| DOLLA FC-Datalog | OLLA + 确定性 | LOGSPACE（Theorem 3.17） | 多项式时间确定性检查 + PSPACE-完全联合复杂度 |
| SD-DOLLA FC-Datalog | DOLLA + 严格递减（每条规则保证某变量长度严格减少） | LOGSPACE 子集 | 线性时间 $O(|w|k)$（Theorem 3.23） |
| DOLLA+ FC-Datalog | OLLA 扩展，允许 $x \doteq yz$ 形式的模式方程 | 包含 DRX | 多项式时间确定性检查（Proposition 4.9） |

### 核心处理模块

框架包含两个逻辑上先后执行的模块：

**1. 程序片段识别与确定性检查。** 在模型检查之前，首先验证输入程序是否属于目标片段（如 DOLLA 或 DOLLA+），并判定其是否满足局部和全局确定性条件。对于 OLLA 程序，确定性检查可在多项式时间内完成（Proposition 3.20）；对于 DOLLA+ 程序，同样保持多项式可判定性（Proposition 4.9）。这一步骤是整个框架的“准入控制”机制，确保后续模型检查的复杂度可控。

**2. 基于查找表的前向模型检查。** 对于通过确定性检查的 SD-DOLLA(+) 程序，框架采用自底向上的前向推导策略，利用查找表记录已推导出的关系事实。在 $O(n|\Sigma|)$ 的预处理后（$n$ 为关系符号的最大元数），模型检查可在 $O(|w|k)$ 时间内完成，其中 $k$ 为程序中的规则条数（Theorem 3.23, Theorem 4.8）。严格递减性保证了推导过程必然终止，而确定性保证了每个输入仅触发唯一的推导路径，从而避免了回溯。

### 框架的实用价值验证

为证明受限片段并非过于贫乏，框架通过将**确定性正则表达式（DRX）** 编码为 SD-DOLLA 和 DOLLA+ 程序，验证了其实际表达能力。具体而言，任意 DRX 定义的语言可由 SD-DOLLA FC-Datalog 程序以线性规模模拟（Theorem 4.3）；在 DOLLA+ 中，通过允许 $x \doteq yz$ 形式的模式方程直接处理内存变量，可进一步减少所需规则数量，降低编写成本（Theorem 4.10）。

### 框架的边界与局限

需要明确指出的是，该框架的有效性建立在一系列强假设之上：SD-DOLLA(+) 的线性复杂度要求程序同时满足严格递减和确定性，并非所有有用查询都能自然表达；DOLLA 与确定性线性 FC-Datalog 之间的中间片段尚未完整映射；若在 DOLLA+ 中引入 DRX 约束，由于 DRX 交集非空问题不可判定，全局确定性检查可能丧失多项式可判定性。本文为纯理论分析，未包含实验评估，在具体信息提取基准上的工程表现有待验证。



### 程序片段识别与确定性检查

FC-Datalog 程序的语法限制构成了框架的核心控制机制。给定程序 $P := (\mathfrak{u}, \mathscr{R}, \Phi)$，在实际查询评估之前，系统需先判定 $P$ 所属的片段并验证其确定性。这一过程包含两个正交维度：

**线性性检查**：根据 Definition 3.2，一条规则 $\rho \in \Phi$ 是线性的，当且仅当其规则体中最多包含一个与头关系符号相互递归的关系原子。违反该限制的典型形式如：

$$\operatorname{Ans}(z) \gets z \doteq x y, \operatorname{Ans}(x), \operatorname{Ans}(y)$$

该规则体包含两个与头符号 $\operatorname{Ans}$ 相互递归的原子，属于非线性规则。全 FC-Datalog 允许此类规则，导致其联合复杂度达到 EXP-完全（Theorem 3.1）；而线性 FC-Datalog 则将表达力降至 NLOGSPACE（Theorem 3.4）。

**确定性检查**：在线性基础上，确定性进一步分为局部确定性和全局确定性两个层次（Definition 3.9）。局部确定性要求每条规则的模式方程所定义的关系 $W_\rho$ 构成偏函数——即对于给定的顶部变量赋值，底部变量的解若存在则唯一。全局确定性则要求同一关系符号的不同规则之间，其合法输入集合互不相交，避免非确定性分支。

确定性检查的复杂度高度依赖于模式方程的形状。对于允许任意字方程的确定性线性 FC-Datalog，其确定性检查等价于字方程可满足性问题，属于 NP 难。这构成了直接使用该片段的核心障碍。

### OLLA 限制与 profile 函数

为解决上述可判定性瓶颈，框架引入单字母前瞻（One Letter Lookahead, OLLA）限制（Definition 3.14）。OLLA 规则要求每条模式方程严格遵循以下三种形式之一：

- $x \doteq y \mathsf{a}$（变量 $x$ 由变量 $y$ 后接终端符号 $\mathsf{a}$ 构成）
- $x \doteq \mathsf{a} y$（变量 $x$ 由终端符号 $\mathsf{a}$ 前接变量 $y$ 构成）
- $x \doteq \varepsilon$（变量 $x$ 为空串）

基于此限制，可为每条规则提取 profile 函数：

$$\operatorname{pro}_{\rho}(x) = \begin{cases} \mathsf{a} & \text{if } x \doteq y\mathsf{a} \text{ or } x \doteq \mathsf{a}y \\ \varepsilon & \text{if } x \doteq \varepsilon \\ \perp & \text{otherwise} \end{cases}$$

该函数将每个顶部变量映射到其对应的终端符号约束（或空串、无约束）。profile 函数的关键价值在于：它将原本需要求解任意字方程的确定性检查问题，转化为对终端符号一致性的多项式时间验证。具体而言，OLLA FC-Datalog 的局部和全局确定性均可在多项式时间内判定（Proposition 3.20），这是框架从理论走向可用的关键转折点。

DOLLA（Deterministic OLLA）片段即满足 OLLA 限制且通过全局确定性检查的程序集合，已被证明精确捕获 LOGSPACE（Theorem 3.17）。

### 严格递减性与前向模型检查

为进一步降低查询评估的联合复杂度，框架引入严格递减（Strictly Decreasing, SD）限制。SD-DOLLA 要求每条规则在执行过程中保证某个变量的长度严格递减，从而杜绝无限长的非递减推导链。

对于 SD-DOLLA 程序，模型检查采用基于查找表的前向评估算法。其核心复杂度边界由 Theorem 3.23 给出：给定输入词 $w$ 和 SD-DOLLA 程序 $P$，在 $O(n|\Sigma|)$ 的预处理后（其中 $n$ 为程序规模，$|\Sigma|$ 为字母表大小），可在 $O(|w|k)$ 时间内判定 $w \in L(P)$，其中 $k$ 为程序中的关系符号数量。这一线性联合复杂度使 SD-DOLLA 具备了实际可部署性。

### DRX 模拟中的规则构造

框架的表达力通过模拟确定性正则表达式（DRX）得到验证。在 SD-DOLLA 中，DRX 的终端转移被编码为如下形式的规则：

$$Q_{\mathrm{src}}(u, x_1', \dots, x_k') \gets Q_{\mathrm{dst}}(v, x_1, \dots, x_k), u \doteq \mathsf{a} v, x_1 \doteq x_1' \mathsf{a}, \dots$$

该规则消耗输入词 $u$ 的首字符 $\mathsf{a}$，同时将对应的内存变量 $x_1$ 更新为 $x_1' \mathsf{a}$（Theorem 4.3 证明过程）。在表达能力更强的 DOLLA+ 片段中，后向引用（backreference）可通过模式方程直接处理，无需引入额外辅助规则：

$$Q_{\mathrm{src}}(u, x_1', \dots, x_k') \gets Q_{\mathrm{dst}}(v, x_1, \dots, x_k), u \doteq x_n' v, x_1 \doteq x_1' x_n', \dots, x_{\ell} \doteq x_{\ell}' x_n'$$

该规则中 $x_n'$ 同时出现在 $u$ 和多个内存变量的模式方程中，实现了对同一因子的多重引用，大幅降低了编写成本（Theorem 4.10 证明过程）。

### 复杂度分层总结

框架的核心公式推导建立了清晰的复杂度分层：

- **全 FC-Datalog**：联合复杂度 EXP-完全，确定性检查 NP 难
- **线性 FC-Datalog**：捕获 NLOGSPACE，确定性检查仍 NP 难
- **DOLLA FC-Datalog**：捕获 LOGSPACE，确定性检查多项式时间，联合复杂度 PSPACE-完全
- **SD-DOLLA FC-Datalog**：捕获 LOGSPACE，确定性检查多项式时间，联合复杂度 $O(|w|k)$（线性）

这一分层揭示了语法限制、表达力与计算复杂度之间的精确权衡关系，构成了框架的理论支柱。



## 实验与关键发现

**本文为纯理论性工作，未包含实验评估。** 所有结论均基于严格的定理证明和计算复杂度分析，不涉及数据集、基准测试或工程实现。以下从理论验证的角度，梳理作者如何通过复杂度层级和表达力模拟来支撑框架的实用主张。

### 理论验证的核心路径

作者通过一条清晰的复杂度递减链来验证“受限片段框架”的有效性：

1. **全 FC-Datalog 作为上界基线**：Theorem 3.1 确立全 FC-Datalog 的联合复杂度为 **EXP-完全**，这构成了不可接受的效率瓶颈，直接驱动了对语法限制的需求。

2. **线性化作为第一步**：将规则限制为线性后，联合复杂度降至 **PSPACE**，且线性 FC-Datalog 被证明恰好捕获 **NLOGSPACE**（Theorem 3.4）。这验证了语法限制对复杂度的改善是实质性的。

3. **确定性作为关键分水岭**：在线性基础上叠加局部和全局确定性，得到确定性线性 FC-Datalog，其捕获 **LOGSPACE**（Theorem 3.11）。然而，确定性检查本身等价于字方程可满足性问题，属于 **NP 难**，这暴露了该片段在实际可用性上的根本缺陷——程序能否通过检查本身就是难以判定的。

4. **OLLA/DOLLA 作为实用转折点**：通过将模式方程限制为“单字母前瞻”（OLLA）形式，确定性检查变得可在**多项式时间**内完成（Proposition 3.20），同时 DOLLA FC-Datalog 仍然捕获 **LOGSPACE**（Theorem 3.17）。这是整个框架中最关键的权衡——以表达力上的适度让步，换取了可高效验证的确定性保证。

5. **SD-DOLLA 达到线性联合复杂度**：在 DOLLA 基础上进一步要求“严格递减”（SD），模型检查的时间复杂度降至 **O(|w|·k)**，预处理开销为 O(n|Σ|)（Theorem 3.23）。这为大规模字符串查询提供了理论上的可行性保证。

### 表达力验证：DRX 模拟

为证明受限片段并未牺牲过多的实用表达力，作者给出了将**确定性正则表达式（DRX）**编码为 SD-DOLLA(+) 程序的构造性证明：

- **SD-DOLLA 可简洁模拟 DRX**（Theorem 4.3）：每个 DRX 可被翻译为等价的 SD-DOLLA 程序，验证了该片段足以覆盖一类具有实际应用价值的查询语言。

- **DOLLA+ 进一步降低编写成本**（Theorem 4.10）：DOLLA+ 允许模式方程直接引用内存变量（如 $u \doteq x_n' v$），使得 DRX 中后向引用（backreference）的模拟仅需常数条规则，而在纯 DOLLA 中可能需要规则数量随变量数增长。这表明 DOLLA+ 在保持同样高效模型检查的同时，显著提升了程序的可编写性。

### 失败模式与已知局限

尽管理论结果完整，框架存在以下明确限制，可视为实际应用中可能遇到的“失败模式”：

1. **确定性检查的脆弱性**：DOLLA/DOLLA+ 的全局确定性检查依赖于 DRX 本身的性质。若在 DRX 上叠加额外约束，由于 DRX 交集非空问题**不可判定**，全局确定性检查可能丧失多项式可判定性。这意味着框架对输入程序的“来源”有隐含假设。

2. **SD 假设过强**：SD-DOLLA(+) 的线性复杂度建立在严格递减的强假设上，并非所有有意义的字符串查询都能自然地满足该条件。对于不满足 SD 的程序，联合复杂度仍为 **PSPACE-完全**，可能限制大规模部署。

3. **中间片段尚未映射**：DOLLA 与确定性线性 FC-Datalog 之间的表达力与复杂度权衡谱系尚未完整刻画，存在理论空白。

4. **缺乏工程验证**：所有结论停留在理论层面，未在任何信息提取基准或真实规则集上进行效率或表达力验证，框架的实际工程价值仍需后续工作佐证。

### 小结

本文的实验验证本质上是**理论证明驱动的复杂度分析**，而非经验性的基准测试。其核心贡献在于构建了一条从 EXP-完全到线性时间的复杂度递减链，并在 DOLLA/SD-DOLLA 片段上同时实现了“多项式可检查的确定性”与“线性模型检查”，最后通过 DRX 模拟证明了该片段保留了足够的实用表达力。这一论证结构严谨自洽，但缺乏实验数据支撑是其明确局限。



## 定位与知识库关联

### 1. 问题根源与基线对比

FC-Datalog 的提出旨在扩展 **FC[REG]**（Freydenberger et al.）的表达能力，使其能够通过递归定义核心 spanner 的关系。全 FC-Datalog 在理论上具有强大的表达力，但其**联合复杂度为 EXP-完全**（Theorem 3.1），且确定性检查等价于字方程可满足性问题（NP 难），这使其无法直接用于高效字符串查询。本文的核心工作并非提出一个全新的查询语言，而是在全 FC-Datalog 这一最优基线上，通过系统性地施加语法限制，构建一个在表达力与计算复杂度之间可定制的片段谱系。

基线方法包括：
- **Unrestricted FC-Datalog**：全片段，作为复杂度上界（EXP-完全）和表达力上界的参照点。
- **Linear FC-Datalog**：仅施加线性限制的片段，作为引入确定性概念之前的前驱基线。该片段捕获 **NLOGSPACE**（Theorem 3.4），证明了线性性本身即可将复杂度从 EXP 降至 NLOGSPACE，但尚未解决确定性检查的不可判定性问题。

### 2. 限制性片段的递进构建与因果机制

本文的方法论核心在于识别并施加一组相互关联的语法限制，逐步收紧程序的行为，从而在复杂度谱系上向下移动。这一过程的因果链条如下：

| 限制槽位 | 基线（全 FC-Datalog） | 本文方案 | 因果效果 |
|:---|:---|:---|:---|
| **规则线性性** | 规则体可含多个与头关系符号相互递归的原子 | 每条规则最多含一个相互递归的体原子（Definition 3.2） | 将联合复杂度从 EXP-完全降至 NLOGSPACE（Theorem 3.4） |
| **局部确定性** | 模式方程组合可产生一对多的变量赋值 | 每条规则的 $W_\rho$ 构成偏函数（Definition 3.9） | 消除非确定性分支，为 LOGSPACE 捕获奠定基础 |
| **全局确定性** | 同一关系符号的多条规则可能处理相同的顶部输入 | 不同规则的合法输入集合互不相交（Definition 3.9） | 确保整个程序的行为是确定的，与局部确定性协同将表达力降至 LOGSPACE（Theorem 3.11） |
| **模式方程形状（OLLA）** | 任意的字方程（形如 $\alpha \doteq \beta$） | 每个方程必须为 $x \doteq y a$、$x \doteq a y$ 或 $x \doteq \varepsilon$（Definition 3.14） | 使确定性检查从 NP 难降至多项式时间（Proposition 3.20），同时保持 LOGSPACE 表达力（Theorem 3.17） |
| **严格递减性（SD）** | 变量长度在推导中可能保持不变或增加 | 每条规则保证某个变量长度严格递减（Section 3.4） | 将联合复杂度进一步降至线性时间 $O(|w|k)$（Theorem 3.23），实现高效模型检查 |

上述限制并非独立施加，而是形成了一条**表达力-复杂度权衡链**：
- **全 FC-Datalog**（EXP-完全）$\supset$ **线性 FC-Datalog**（NLOGSPACE）$\supset$ **确定性线性 FC-Datalog**（LOGSPACE）$\supset$ **DOLLA FC-Datalog**（LOGSPACE + 多项式可判定确定性）$\supset$ **SD-DOLLA**（线性时间联合复杂度）。

### 3. 框架的实用验证：DRX 模拟

为验证受限片段在实际查询场景中的价值，本文以**确定性正则表达式（DRX）** 作为目标应用，证明了：
- **SD-DOLLA FC-Datalog** 可以表达任意 DRX 的语言（Theorem 4.3），其规则通过消耗输入中的终端符号并更新对应变量来模拟 DRX 的状态转移。
- **DOLLA+** 片段进一步引入更灵活的模式方程形式（如 $u \doteq x_n' v$），允许在保持 SD-DOLLA 线性时间复杂度的同时，**显著降低编写 DRX 模拟程序所需的规则数量**（Theorem 4.10），从而在编写成本与运行时效率之间取得更好的平衡。

### 4. 适用边界与局限

本文框架的适用性受以下边界条件约束：

1. **确定性依赖强假设**：全局确定性检查依赖于 DRX 本身的性质。若引入 DRX 约束，由于 DRX 交集非空问题不可判定，全局确定性检查可能丧失多项式可判定性。这意味着在需要约束求解的场景中，框架的可判定性优势可能被削弱。
2. **SD-DOLLA(+) 的表达力上限**：线性复杂度建立在严格递减和确定性的强假设之上，并非所有有用的字符串查询都能被自然地表达为 SD-DOLLA 程序。对于需要非确定性或非严格递减递归的查询，必须退回到更高复杂度的片段。
3. **片段间映射不完整**：DOLLA 与确定性线性 FC-Datalog 之间的表达力与复杂度权衡尚未被完整映射，存在尚未探索的中间片段。
4. **缺乏实验佐证**：本文为纯理论分析，所有结论基于定理证明和复杂度分析，未在具体信息提取基准或规则集上验证工程性能。
5. **非 SD 片段的 PSPACE 瓶颈**：对于非严格递减的 DOLLA 程序，联合复杂度仍为 PSPACE-完全，可能限制大规模应用。

### 5. 开放问题与知识库定位

本文在 FC-Datalog 与文档 spanner 理论的交叉地带留下了若干开放方向，为后续工作提供了切入点：

- **片段粒度细化**：在 DOLLA 与确定性线性 FC-Datalog 之间添加或放松语法限制时，如何影响片段成员资格检查的复杂度？是否存在具有多项式可判定性和更高表达力的中间片段？
- **结构标准引入**：能否将 **FC-CQ** 的无环性等结构标准引入 FC-Datalog 片段，以进一步改善复杂度？
- **不可表达性刻画**：这些受限片段的不可表达性具体结果有哪些？这有助于精确界定各片段的适用场景。
- **解析技术适配**：**区间串接文法（RCG）** 的解析技术（如 Boullier 算法）能否适配到 FC-Datalog，带来更高效的评价器？
- **文档 spanner 原语设计**：如何在文档 spanner 设定中定义与 DOLLA/SD-DOLLA 相对应的自然片段，从而获得同样高效的信息提取原语？
- **DRX 约束的引入边界**：在保持确定性可判定的前提下，DRX 约束能在多大程度上引入 FC-Datalog 片段，而不会使全局确定性检查不可判定？
- **非线性片段的复杂度分级**：是否可以为非线性的受限 FC-Datalog 设计类似的复杂度分级体系？



## 原文 PDF

![[paperPDFs/ICCV_2025/Perceiving_and_Acting_in_First_Person_A_Dataset_and_Benchmark_for_Egocentric_Human_Object_Human_Interactions.pdf]]
