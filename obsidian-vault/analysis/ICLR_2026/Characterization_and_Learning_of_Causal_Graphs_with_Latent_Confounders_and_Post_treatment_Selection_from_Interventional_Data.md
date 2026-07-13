---
title: "Characterization and Learning of Causal Graphs with Latent Confounders and Post-treatment Selection from Interventional Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Characterization_and_Learning_of_Causal_Graphs_with_Latent_Confounders_and_Post_treatment_Selection_from_Interventional_Data.pdf
project_link: null
code_link: null
openreview_forum_id: qclNnbjxNJ
aliases:
- FF
- CLCGLCPTSFI
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/causality
core_operator: "通过显式建模处理后选择变量S，利用干预后边缘分布变化和条件分布不变的模式，结合结构对称性和对间接节点的额外干预进行CI模式检测，可以区分真实因果关系、潜在混淆因子与选择诱导的依赖路径。"
primary_logic: "处理后选择与直接因果关系在干预下具有相同的边际/条件分布变化模式，但这种对称性可通过干预共同原因或诱导路径上的节点打破，从而识别出选择结构；进一步将这种识别能力形式化为FI-Markov等价类和F-PAG图，并设计F-FCI算法实现可证明的正确性和完备性。"
claims:
- "论文提出了显式建模处理后选择的因果形式化方法，并定义了FI-Markov等价类和F-PAG图表示。"
- "开发了可证明正确且完备的F-FCI算法，能够从观测和干预数据中识别因果关系、潜在混淆因子和处理后选择。"
- "定理2提供了FI-Markov等价性的图形准则，为算法提供了理论基础。"
- "Synthetic graphs with latent confounders and post-treatment selection (hard int... 上 Precision = 64.2±0.4"
---

# Characterization and Learning of Causal Graphs with Latent Confounders and Post-treatment Selection from Interventional Data

> [!tip] 核心洞察
> 处理后选择与直接因果关系在干预下具有相同的边际/条件分布变化模式，但这种对称性可通过干预共同原因或诱导路径上的节点打破，从而识别出选择结构；进一步将这种识别能力形式化为FI-Markov等价类和F-PAG图，并设计F-FCI算法实现可证明的正确性和完备性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 干预数据下潜在混杂与处理后选择的因果图表征与学习 |
| 英文题名 | Characterization and Learning of Causal Graphs with Latent Confounders and Post-treatment Selection from Interventional Data |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qclNnbjxNJ) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/causality |
| Method | F-FCI |
| Dataset | Synthetic graphs with latent confounders and post-treatment selection (hard intervention, n=2000), Synthetic graphs with latent confounders and post-treatment selection (soft intervention, Synthetic graphs with latent confounders and post-treatment selection |

> [!tip] 效果简介
> - Synthetic graphs with latent confounders and post-treatment selection (hard int... 上，Precision 为 64.2±0.4，对比 43.7±0.1 (FCI-INTERVEN)，变化 +20.5。
> - Synthetic graphs with latent confounders and post-treatment selection (soft int... 上，Precision 为 70.3±1.5，对比 48.1±0.4 (FCI-INTERVEN)，变化 +22.2。
> - Synthetic graphs with latent confounders and post-treatment selection 上，后处理选择识别准确率 为 >70% (most configs with n>1000)，对比 N/A (独有能力)，变化 N/A。

## 概要

从干预数据中发现因果关系是科学研究的核心任务。然而，现有干预因果发现框架面临一个根本性瓶颈：**处理后选择（post-treatment selection）** 与**真实因果关系**在干预下表现出相同的分布变化模式——两者均导致边缘分布变化而条件分布不变。这种统计信号的不可区分性使得传统方法将它们归入同一等价类，无法分辨因果路径与选择诱导的虚假依赖。

本文通过**显式建模处理后选择变量 $S$** 打破了这一对称性。核心思路是：在增广有向无环图（augmented DAG）中引入干预指标 $\psi$ 和选择节点 $S$，利用三类统计信号——干预分布变化、不变性关系以及结构对称性——来区分因果关系、潜在混淆因子与选择诱导路径。具体而言，直接因果与处理后选择在干预下确实具有相同的边际/条件分布变化模式，但这种对称性可通过**干预共同原因或诱导路径上的节点**来打破，从而识别出选择结构。

基于这一洞察，论文做出了以下贡献：

1. **形式化表征**：定义了精细干预马尔可夫等价类（FI-Markov equivalence），并提出新的图形表示——**F-PAG（精细部分祖先图）**，引入四种标记（尾、箭头、方块 $\square$、圆圈 $\circ$）和八种边类型，能够区分选择诱导路径与真实因果路径。

2. **可证明正确的算法**：开发了 **F-FCI 算法**，在 FI-Markov 等价意义上可证明正确且完备。算法流程包括：从观测数据恢复骨架（因观测分布给出最稀疏的诱导路径图）、利用 CI 模式定向干预变量相关边、检测 Type I 诱导节点以消除歧义、最后应用标准 FCI 定向规则与不变性规则。

3. **实验验证**：在含潜在混淆因子和处理后选择的合成图上，F-FCI 在硬干预下精确度达到 **64.2%**，相比基线 FCI-INTERVEN（43.7%）提升 **20.5 个百分点**；软干预下精确度为 **70.3%**，提升 **22.2 个百分点**。F-FCI 对处理后选择的识别准确率在样本量超过 1000 时多数配置超过 70%，且在不同噪声分布（Laplace、Gumbel）和复杂非线性函数下表现鲁棒。

**局限与开放问题**：当前方法仅能识别含 Type I 诱导节点的路径结构，对完全由 Type II 诱导节点构成的路径尚无法完全识别；此外，如何区分生物约束（如持续过滤非存活细胞）与处理后选择、如何扩展到更一般的选择机制，仍是待解决的问题。



### 干预因果发现中的核心挑战

从观测与干预数据中学习因果结构是因果推断的基石任务。当系统中存在**潜在混淆因子**（latent confounders）时，标准因果发现方法（如PC算法）会产生虚假边，而FCI算法及其变体通过部分祖先图（PAG）表示等价类，能够处理这类未观测混淆。进一步地，Jaber等人将FCI扩展到干预场景，利用干预导致边缘分布变化的模式来精炼因果方向。

然而，上述框架均假设数据是总体的无偏样本。**处理后选择**（post-treatment selection）——即样本包含概率依赖于干预后变量的取值——广泛存在于生物医学、社会科学和A/B测试中。例如，在基因扰动实验中，只有存活的细胞被测量；在临床试验中，只有完成随访的患者被纳入分析。这种选择机制会在变量间引入虚假依赖，使得因果发现面临根本性困难。

### 现有方法的识别瓶颈

现有干预因果发现框架的核心瓶颈在于：**处理后选择导致的虚假依赖与真实因果关系在干预下表现出相同的分布变化模式**。具体而言，如Figure 1所示：

- **直接因果**（$X_1 \rightarrow X_2$）与**选择诱导路径**（$X_1 \rightarrow S \leftarrow X_2$，其中$S$为选择变量）在干预$X_1$时，均表现为$X_2$的边缘分布变化而条件分布$p(X_2|X_1)$不变。传统方法仅依赖“干预导致边缘分布变化”这一信号，无法区分这两种结构，将它们归入同一等价类。
- 类似地，**潜在混淆**（$X_1 \leftarrow L \rightarrow X_2$）与**选择诱导的对称依赖**（$X_1 \rightarrow S \leftarrow X_2$且$X_1$、$X_2$均非$S$的原因）在干预任一变量时，均表现为另一变量的边缘分布不变，同样无法被现有方法区分。

这种不可区分性源于一个更深层的结构对称性：处理后选择与直接因果关系在干预下具有**相同的边际/条件分布变化模式**。打破这种对称性需要额外的结构信息或干预策略，而现有框架缺乏对此的形式化建模。

### 本文动机与核心思路

本文旨在填补这一空白。核心动机是：**通过显式建模处理后选择变量$S$，将选择机制纳入增广DAG的形式化框架，从而在干预数据中区分真实因果关系、潜在混淆因子与选择诱导的依赖路径**。

具体而言，本文提出三个层次的贡献：

1. **形式化建模**：在增广DAG中显式引入选择变量$S$和干预指标$\psi$，利用$S=1$条件下的干预分布分解（Equation 1）刻画选择效应，并定义**FI-Markov等价类**（Fine-grained Interventional Markov equivalence）和新的图形表示**F-PAG**，以区分传统PAG无法表示的因果与选择结构。

2. **识别机制**：利用干预后边缘分布变化与条件分布不变的模式，结合**结构对称性**和**对间接节点（Type I诱导节点）的额外干预**进行条件独立性（CI）模式检测，从而打破因果与选择路径的对称性。

3. **算法实现**：开发**F-FCI算法**，可证明其正确性（Theorem 3）和完备性（Theorem 4），能够从观测和干预数据中识别因果关系、潜在混淆因子和处理后选择，达到FI-Markov等价类的精度上限。

Figure 2展示了这一框架的图形表示：增广DAG包含干预指标$\psi$、观测变量$X$、潜在混淆因子$L$和选择变量$S$，为后续的CI模式刻画和算法设计提供了统一的图基础。



## 核心方法与创新机理

本文的核心创新在于**显式建模处理后选择（post-treatment selection）**，并将其与潜在混淆因子统一纳入干预因果发现框架，从而突破现有方法无法区分选择诱导依赖与真实因果关系的根本瓶颈。

### 瓶颈突破：区分选择与因果的对称性

现有干预因果发现方法（如 FCI-INTERVEN）面临一个深层困境：处理后选择导致的虚假依赖与真实因果关系在干预下表现出**相同的分布变化模式**——干预使边缘分布发生变化，但条件分布保持不变。这意味着仅凭传统的变异/不变性检测，两类结构被归入同一等价类而无法区分（图 1 展示了这一对称性）。本文的核心洞察在于：这种对称性并非不可打破。通过引入**干预指标 $\psi$ 与变量的条件独立模式**，并结合**结构对称性检测**和**对间接节点的额外干预**，可以将选择路径与因果路径分离开来。

### 关键机制：三阶段区分逻辑

F-FCI 的区分能力建立在以下因果调控机制之上：

1. **干预后边缘分布变化 + 条件分布不变**：这是选择与直接因果共有的基础模式，构成识别的起点而非终点。
2. **干预指标 $\psi$ 的条件独立模式**：当存在处理后选择时，干预指标 $\psi$ 与下游变量之间的条件独立关系会呈现出不同于纯因果结构的特征（图 4 中以红色虚线标示的 CI 模式差异），这为区分提供了第一层信号。
3. **Type I 诱导节点的结构打破**：当仅靠端点 CI 模式无法区分时（如图 8 所示的对称情形），算法通过检测诱导路径上的 Type I 诱导节点，并对其施加额外干预来打破结构对称性，从而确定边的真实方向。

### 形式化表征：FI-Markov 等价类与 F-PAG

上述区分能力被形式化为**FI-Markov 等价类**和**F-PAG 图**（定义 5）。相比传统 PAG 仅使用 $\rightarrow$、$\leftrightarrow$、$\circ\!-$、$\circ\!-\!\circ$ 等标准边类型，F-PAG 引入了**四种标记**（尾、箭头、方块 $\square$、圆圈 $\circ$）和**八种边类型**，其中特别新增了 $\rightarrow$ 和 $\blacktriangle$ 边，用于显式表示非直接因果/选择诱导路径。定理 2 给出了 FI-Markov 等价性的图形准则：两个增广 DAG 等价当且仅当对应 MAG 具有相同的骨架、v-结构和干预节点间的边标记。

### 算法实现：F-FCI 的 changed slots

F-FCI 算法在标准约束因果发现流程上进行了三个关键改造：

| 改造槽位 | 基线方法（FCI-INTERVEN） | F-FCI 方法 | 证据锚点 |
|---------|------------------------|-----------|---------|
| **选择建模** | 忽略或仅处理预处理选择 | 增广 DAG 中显式加入选择变量 $S$，利用 $S=1$ 条件下 $\psi$ 与变量的条件独立/依赖关系推测选择存在 | Definition 1, §3.1 |
| **图形表示** | 传统 PAG，无法区分选择诱导路径 | F-PAG，引入 $\square$ 标记和 $\blacktriangle$ 边表示选择诱导路径 | Definition 5 |
| **方向规则** | 仅基于干预导致边缘分布变化或条件不变性 | 额外利用 $\psi$ 与变量的 CI 模式、结构对称性及 Type I 诱导节点干预来区分因果与选择路径 | Step 2.2, §4 |

算法流程分为四个模块：首先从观测数据恢复无向骨架（因其编码所有诱导路径且最稀疏）；然后利用捕获的 CI 模式定向与干预变量相关的边；接着检测 Type I 诱导节点以消除歧义；最后对剩余边应用标准 FCI 定向规则和不变性规则。该算法被证明在 FI-Markov 等价类意义下具有**可证明的正确性和完备性**。



![[assets/figures/papers/iclr26_0011_qclNnbjxNJ_Characterization_and_Learning_of_Causal_Graphs_w/figures/004_Figure_1.jpg]]
*Figure 1: Motivation examples. (a) & (b) exhibit same dependence with tails from X _ { 1 } and arrowheads into X _ { 2 } , regardless of direct causation; (c) & (d) exhibit same dependence with tails on both X _ { 1 } and X _ { 2 } , regardless of direct selection. Existing methods cannot distinguish these cases, whereas ours can*

![[assets/figures/papers/iclr26_0011_qclNnbjxNJ_Characterization_and_Learning_of_Causal_Graphs_w/figures/010_Figure_2.jpg]]
*Figure 2: Examples of graphical representations. (a) Augmented DAG with explicit intervention indicators (ψ). (b) Extension of the augmented DAG to include latent confounders. (c) Modeling post-treatment selection using the augmented DAG, with toy examples of selection on observational data (d) and selection after intervention (e), where the positively invariant $\mathsf { p } ( X _ { 2 } | X _ { 1 }$ ) is marked in red*

![[assets/figures/papers/iclr26_0011_qclNnbjxNJ_Characterization_and_Learning_of_Causal_Graphs_w/figures/013_Figure_5.jpg]]
*Figure 5: Illustrations of F-PAG graphical representation for the FI-Markov equivalence class. targets I if and only if the corresponding MAGs for $\mathcal { M } _ { 1 } = \mathcal { M }$ ( A u $g _ { I } ( \mathcal { G } _ { 1 }$ ) ) and $\mathcal { M } _ { 2 } = \mathcal { M }$ ( A u $g _ { I } ( \mathcal { G } _ { 2 }$ ) ) have the same skeleton and v-structure, and have the same marks and edges among intervened nodes

F-FCI 是一个基于约束的因果发现算法，旨在从观测数据和干预数据中同时识别因果关系、潜在混杂因子和处理后选择，输出结果达到 FI-Markov 等价类。其核心设计逻辑是：**处理后选择与直接因果关系在干预下表现出相同的边际/条件分布变化模式，这种对称性无法被传统方法打破，但可通过显式建模选择变量并检测干预指标与变量间的条件独立模式来区分**。

### 输入与输出

- **输入**：观测分布 $p^{(0)}(X)$ 及若干干预分布 $p^{(k)}(X)$（$k=1,\dots,K$），每个干预对应一个已知的干预目标集合 $I^{(k)} \subset [N]$。
- **输出**：F-PAG 图，即 FI-Markov 等价类的图形表示，包含尾（tail）、箭头（arrowhead）、方块（square）和圆圈（circle）四种标记及八种边类型，能够编码因果关系、潜在混杂因子和处理后选择诱导的依赖路径。

### 算法流程

F-FCI 由四个顺序模块构成，每个模块解决一个逐步递进的识别子问题：

#### 步骤 1：骨架恢复

从观测数据 $p^{(0)}$ 中恢复无向骨架。观测分布给出最稀疏的图，编码了所有诱导路径（inducing paths），因此骨架恢复在此阶段最为高效。该步骤采用标准 FCI 的条件独立性测试框架。

#### 步骤 2.2：干预变量边定向

利用捕获的 CI 模式定向与干预变量相关的边。具体而言，干预指标 $\psi$ 与变量的条件独立/依赖关系——即干预后边缘分布是否变化、条件分布是否不变——被用于推断边的端点标记（tail 或 arrowhead），对应 Figure 4 中总结的定向规则。

#### 步骤 3：Type I 诱导节点消除歧义

检测 Type I 诱导节点（inducing nodes），以区分仅靠端点 CI 模式无法区分的结构。当两个干预变量之间存在诱导路径时，对该路径上的 Type I 节点施加额外干预，可以打破因果路径与选择诱导路径之间的对称性，从而识别出选择结构。

#### 步骤 4：标准 FCI 定向与不变性规则

对步骤 2.2 和步骤 3 未涉及的边（包括干预节点与非干预节点之间、非干预节点之间的边），应用标准 FCI 定向规则及不变性规则完成最终定向。

### 理论保证

定理 2 给出了 FI-Markov 等价性的图形准则：两个增广 DAG 是 FI-Markov 等价的，当且仅当它们对应的 MAG 具有相同的骨架和 v-结构，且在干预节点之间具有相同的边和端点标记。F-FCI 被证明在该等价类下是**可证明正确且完备的**（provably sound and complete）。

### 方法边界

F-FCI 的识别能力受限于诱导路径的结构类型：仅当路径中包含 Type I 诱导节点时，算法才能完全区分因果与选择路径。对于完全由 Type II 诱导节点构成的路径，当前方法尚无法完全识别其因果结构，这是该方法的一个已知局限。此外，算法无法区分处理后选择与生物约束（如持续过滤非存活细胞），因为两者具有不同的不变性/可变性模式，需要更多数据或假设来区分。



### 核心瓶颈与解决思路

现有干预因果发现框架的核心瓶颈在于：处理后选择（post-treatment selection）导致的虚假依赖与真实因果关系在干预下表现出相同的分布变化模式——边缘分布变化而条件分布不变，使得传统方法无法区分两者，将其归入同一等价类。F-FCI 的解决思路是：通过显式建模处理后选择变量 $S$，利用干预后边缘分布变化和条件分布不变的 CI 模式，结合结构对称性以及对间接节点（Type I 诱导节点）的额外干预，来区分真实因果关系、潜在混淆因子与选择诱导的依赖路径。

### 关键公式：干预下含选择的联合分布分解

在增广 DAG 框架下，处理后选择通过引入选择变量 $S$ 建模。给定干预目标 $I^{(k)}$，在 $S=1$ 条件下的观测变量 $X$ 联合分布可分解为：

$$
p_{s}^{(k)}(X) = \prod_{\{i|\{i\}\subset I^{(k)}\}} p^{(k)}(X_i|\hat{X}_{pag(i)}, S=1) \prod_{\{j|\{j\}\subset I^{(k)}\}} p^{(0)}(X_j|\hat{X}_{pag(j)}, S=1)
$$

**变量含义**：
- $p_{s}^{(k)}(X)$：第 $k$ 次干预下、经处理后选择（$S=1$）后的联合分布
- $I^{(k)}$：第 $k$ 次干预的干预目标集合
- $p^{(k)}(\cdot|S=1)$：干预后分布，以选择为条件
- $p^{(0)}(\cdot|S=1)$：观测分布，以选择为条件
- $\hat{X}_{pag(i)}$：变量 $X_i$ 在增广 DAG 中的父母节点集合

该分解将联合分布拆分为两部分：被干预变量条件于干预后分布，未被干预变量条件于观测分布，且两者均以 $S=1$ 为条件。这是 F-FCI 利用分布变化模式进行结构识别的概率基础。

### 关键公式：马尔可夫性质与 CI 实现定理

定理 1 将增广 DAG 中的 d-分离与跨环境的条件独立性和不变性/可变性联系起来，为算法提供统计推断基础。其核心断言为：

> 对于正干预分布，增广 DAG $\text{Aug}_{\mathbb{Z}}(\mathcal{G})$ 中的 d-分离关系蕴含对应的条件独立性，以及跨干预环境的分布不变性或可变性。

该定理使算法能够将三类统计信号映射到图结构：
1. **干预分布变化**：干预 $\psi_i$ 与 $X_j$ 的边缘依赖（$\psi_i \not\perp X_j$）表明 $X_i$ 与 $X_j$ 之间存在诱导路径，且路径在 $X_i$ 端以尾（tail）开始
2. **不变关系**：干预下 $p(X_j|X_i)$ 不变（$\psi_i \perp X_j | X_i$）表明路径在 $X_j$ 端以箭头（arrowhead）开始
3. **结构对称性**：当仅靠端点 CI 模式无法区分因果与选择路径时，通过干预诱导路径上的 Type I 诱导节点来打破对称性

### 算法流程模块

F-FCI 的四个核心模块：

1. **骨架恢复**：从观测数据 $p^{(0)}$ 中恢复无向骨架。观测分布编码了所有诱导路径的最稀疏图结构，是后续定向的基础。

2. **干预变量边定向**：利用捕获的 CI 模式，对与干预变量 $\bar{X}_{\bigcup\mathcal{Z}}$ 相关的边进行定向，使用图 4 中总结的定向规则。

3. **Type I 诱导节点消除歧义**：检测干预变量之间诱导路径上的 Type I 诱导节点，以区分仅靠端点 CI 模式无法区分的结构（如直接因果 $X_1 \to X_2$ 与选择诱导 $X_1 - S - X_2$）。

4. **标准 FCI 定向与不变性规则**：对剩余边（干预与非干预节点之间、非干预节点之间）应用标准 FCI 定向规则及不变性规则，完成 F-PAG 的构建。

### 非线性函数鲁棒性测试集

为评估算法在复杂函数关系下的表现，使用了以下非线性函数集合进行压力测试：

$$
\mathcal{F} = \{\sin(\pi x)+0.2\sin(2\pi x),\; x^2,\; \tanh(x),\; x,\; x e^{-x^2/2},\; \log(1+e^{2x-1})+0.05x^2\}
$$

该集合涵盖周期函数、多项式、双曲正切、线性、非单调函数和复合非线性函数，用于检验条件独立性测试在不同函数形式下的稳定性。实验表明 F-FCI 在函数复杂度增加时精确度仅有轻微下降，整体性能仍具竞争力。



## 实验与关键发现

### 核心性能对比

F-FCI 在同时存在潜在混淆因子和处理后选择的合成数据上，与仅能处理混淆因子的 FCI-INTERVEN 进行了系统对比。表 2 汇总了 20 变量图（含 2–3 个潜在混淆因子、5–6 个随机选择变量）上的主结果：


![[assets/figures/papers/iclr26_0011_qclNnbjxNJ_Characterization_and_Learning_of_Causal_Graphs_w/figures/022_Table_2.jpg]]
*Table 2: Comparison of F-FCI and FCI-INTERVEN on graphs with 20 variables, 2–3 latent confounders, and 5–6 randomly chosen selection variables. All values are averaged over 10 runs*

- **硬干预下（n=2000）**：F-FCI 精确度达 64.2±0.4，较 FCI-INTERVEN 的 43.7±0.1 提升 20.5 个百分点。
- **软干预下（n=2000）**：F-FCI 精确度达 70.3±1.5，较 FCI-INTERVEN 的 48.1±0.4 提升 22.2 个百分点。

这一差距的根源在于核心瓶颈：FCI-INTERVEN 仅利用干预导致的边缘分布变化（变异）和条件分布不变性来推断因果方向，但处理后选择诱导的依赖路径在干预下表现出完全相同的分布变化模式——边缘分布变化而条件分布不变。因此 FCI-INTERVEN 将真实因果关系与选择诱导路径归入同一等价类，无法区分。F-FCI 通过显式建模选择变量 S 并利用干预指标 ψ 与变量的条件独立模式打破这一对称性，从而获得显著的精确度优势。

在 SHD（结构汉明距离）指标上，F-FCI 同样表现更优：硬干预下 SHD 约为 8–13，而 FCI-INTERVEN 约为 14–17（表 2）。图 6 展示了不同样本量下的 DAG Precision 和 DAG SHD 变化趋势，F-FCI 的优势随样本量增加而扩大。


![[assets/figures/papers/iclr26_0011_qclNnbjxNJ_Characterization_and_Learning_of_Causal_Graphs_w/figures/014_Figure_6.jpg]]
*Figure 6: Comparison results in identifying causal relations under DAG Precision and DAG SHD metrics. All values are averaged over 10 graphs. Error bars represent the 95% confidence interval*

### 处理后选择识别能力

F-FCI 独有的能力是显式识别处理后选择的存在。表 1 报告了该能力的准确率：


![[assets/figures/papers/iclr26_0011_qclNnbjxNJ_Characterization_and_Learning_of_Causal_Graphs_w/figures/020_Table_1.jpg]]
*Table 1: Accuracy % of F-FCI in identifying post-treatment selection on synthetic data. We report the mean and variance values of accuracy across 10 independent graphs for each configuration*

- **样本量效应**：当 n>1000 时，大多数配置下准确率超过 70%。
- **干预类型影响**：硬干预下的识别准确率普遍高于软干预。这是因为硬干预完全切断被干预变量的入边，使得选择诱导路径的 CI 模式更加清晰可辨。
- **变量维度影响**：在 |X|=10–25 的范围内，准确率保持稳定，表明方法对图规模具有一定鲁棒性。

FCI-INTERVEN 不具备此能力，因为它未对选择变量进行建模，因此表中无对应基线数据。

### 鲁棒性分析

**噪声水平**（图 12）：在不同噪声标准差下，F-FCI 的精确度保持稳定，而召回率在低噪声条件下相对更高。这一模式符合预期——低噪声时条件独立性测试更可靠，能恢复更多真实边；精确度稳定则表明错误发现的边不会因噪声降低而显著增加。

**非线性函数**（表 3）：在更复杂的非线性函数集 $\mathcal{F} = \{\sin(\pi x)+0.2\sin(2\pi x), x^2, \tanh(x), x, x e^{-x^2/2}, \log(1+e^{2x-1})+0.05x^2\}$ 下，F-FCI 精确度出现适度下降，但整体性能仍具竞争力。下降的原因在于复杂非线性使条件独立性测试的统计功效降低，导致部分真实边被遗漏。

**非高斯噪声分布**：在 Laplace 噪声（表 4）和 Gumbel 噪声（表 5）下，F-FCI 性能保持稳定，部分设置下甚至略有提升。这表明方法不依赖高斯假设，对厚尾分布具有鲁棒性。

### 失败模式与局限

1. **Type II 诱导节点路径**：F-FCI 仅能识别含有 Type I 诱导节点的诱导路径中的结构。对于完全由 Type II 诱导节点构成的路径，当前方法无法完全识别因果结构。这是方法完备性的理论边界，而非实现缺陷。

2. **生物约束与处理后选择的混淆**：在真实基因扰动数据（图 13）中，持续过滤非存活细胞等生物约束与处理后选择具有不同的不变性/可变性模式，但 F-FCI 目前无法区分两者。这需要额外的领域知识或数据假设来消歧。

3. **小样本下的 CI 测试可靠性**：F-FCI 是基于约束的方法，其性能依赖于条件独立性测试的准确性。在 n=500 的设置中，精确度和召回率均明显低于 n=2000（表 2），反映了小样本下 CI 测试统计功效不足的问题。



## 定位与知识库关联

### 1. 与基线方法的关系

F-FCI 的直接基线是 **FCI-INTERVEN**，即标准 FCI 框架下可处理潜在混淆因子和干预数据的因果发现方法。两者的核心差异在于对**处理后选择（post-treatment selection）**的建模能力：

- **FCI-INTERVEN** 仅利用干预导致的边缘分布变化（变异）和条件分布不变性来推断因果方向，但无法区分真实因果关系与选择诱导的虚假依赖。原因在于，直接因果关系（$X_1 \rightarrow X_2$）与处理后选择结构（$X_1$ 和 $X_2$ 均受选择变量 $S$ 影响）在干预下表现出相同的分布变化模式——边缘分布变化而条件分布不变，导致传统方法将两者归入同一等价类（见 Figure 1 的动机示例）。

- **F-FCI** 通过显式建模选择变量 $S$，在增广 DAG 中引入干预指标 $\psi$，利用 $\psi$ 与变量的条件独立/依赖模式以及结构对称性来区分因果与选择路径。具体而言，F-FCI 识别出 **Type I 诱导节点**（inducing nodes），通过对这些节点的额外干预打破因果与选择结构的对称性，从而将选择结构从因果等价类中分离出来。

这一改进带来了显著的性能提升：在含潜在混淆因子和处理后选择的合成图上（20 变量，n=2000），F-FCI 在硬干预下的精确度为 $64.2\pm0.4$，较 FCI-INTERVEN 的 $43.7\pm0.1$ 提升约 20.5 个百分点；在软干预下精确度为 $70.3\pm1.5$，较基线的 $48.1\pm0.4$ 提升约 22.2 个百分点（Table 2）。此外，F-FCI 独有地具备识别处理后选择的能力，在样本量超过 1000 的大多数配置中准确率超过 70%（Table 1）。

### 2. 适用边界

F-FCI 的适用场景由以下条件界定：

1. **数据要求**：需要同时具备观测数据和多个干预目标下的干预数据。干预可以是硬干预（完全切断父节点影响）或软干预（改变条件分布），但要求干预目标已知。

2. **图结构约束**：F-FCI 的可识别性依赖于诱导路径上存在 **Type I 诱导节点**。当诱导路径完全由 Type II 诱导节点构成时，当前方法无法完全识别因果结构。这是该框架的一个根本性局限。

3. **选择机制假设**：选择变量 $S$ 被建模为处理后变量的后代，且选择发生在干预之后。该框架目前无法处理更一般的选择机制，如选择发生在多个时间点、或同时存在预处理选择的情况。

4. **统计假设**：方法依赖于条件独立性测试的准确性，在小样本或高维场景下可能受到影响。虽然通过并行化可缓解可扩展性问题，但算法本身仍是基于约束的方法，其性能受限于 CI 测试的统计功效。

### 3. 已知局限与失效模式

**结构不可识别性**：当两个被干预变量之间的诱导路径完全由 Type II 诱导节点组成时，F-FCI 无法区分因果与选择结构。这是 FI-Markov 等价类的内在边界——此类结构在干预数据下产生相同的 CI 模式，即使显式建模选择变量也无法打破对称性。

**生物约束与选择的混淆**：在真实生物实验中（如基因扰动筛选），治疗后选择（如持续过滤非存活细胞）与生物约束（biological constraints）可能表现出不同的不变性/可变性模式，但 F-FCI 当前无法区分两者。Figure 13 的基因扰动数据案例展示了这一挑战：恢复的因果结构中可能混杂了选择效应与生物约束效应，需要领域知识或额外数据来解耦。

**非线性与噪声鲁棒性**：F-FCI 在不同噪声水平下精确度保持稳定，但低噪声条件下召回率相对较高（Figure 12）。在更复杂的非线性函数下（如 $\sin(\pi x)+0.2\sin(2\pi x)$、$\tanh(x)$、$\log(1+e^{2x-1})$ 等），精确度有轻微下降，但整体性能仍具竞争力（Table 3）。对 Laplace 和 Gumbel 噪声分布表现鲁棒（Tables 4-5）。

**可扩展性**：作为基于约束的方法，F-FCI 在高维场景下的 CI 测试次数随变量数增长较快。论文提到可通过并行化缓解，但未提供大规模（如数百变量）下的实验验证，这一点需要在实际部署中手动评估。

### 4. 开放问题

论文明确指出了三个待解决的核心问题：

1. **Type II 诱导路径的识别**：如何识别沿仅由 Type II 诱导节点组成的诱导路径的因果结构？这是 FI-Markov 等价类理论框架的下一个自然延伸，可能需要引入额外的假设或更丰富的干预设计。

2. **生物约束与选择解耦**：如何从数据中区分生物约束与处理后选择？两者在干预下可能表现出不同的不变性模式，但当前框架缺乏形式化的判别准则。这可能需要结合领域特定的生成机制假设。

3. **更一般的选择机制**：如何将 F-FCI 扩展到多时间点选择、预处理与后处理选择并存、或选择变量本身受干预影响等更复杂的场景？当前增广 DAG 的建模假设相对严格，泛化到这些场景需要重新审视 Markov 性质和等价类理论。



## 原文 PDF

![[paperPDFs/ICLR_2026/Characterization_and_Learning_of_Causal_Graphs_with_Latent_Confounders_and_Post_treatment_Selection_from_Interventional_Data.pdf]]
