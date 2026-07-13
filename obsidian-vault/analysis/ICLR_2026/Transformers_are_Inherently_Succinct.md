---
title: "Transformers are Inherently Succinct"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Transformers_are_Inherently_Succinct.pdf
project_link: null
code_link: null
openreview_forum_id: Yxz92UuPLQ
aliases:
- TAIS
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "UHAT 通过硬注意力、严格未来掩码和右端断点规则构造双重指数级大计数器，从而在多项式尺寸内仿真 EXPSPACE 完全问题（如 2^n-tiling），这构成了所有下界证明的核心机制。"
primary_logic: "Transformer（UHAT）本质上极为简洁：在表示相同语言时，可以比 LTL 和 RNN 指数级更简洁，比有限自动机双重指数级更简洁，这导致其非空性验证问题是 EXPSPACE 完全的。"
claims:
- "UHAT 和 B-RASP 的非空性问题是 EXPSPACE 完全的。"
- "UHAT 可以比 LTL 指数级更简洁。"
- "UHAT 可以比有限自动机双重指数级更简洁。"
- "UHAT 可以比 RNN（包括 SSM）指数级更简洁。"
---

# Transformers are Inherently Succinct

> [!tip] 核心洞察
> Transformer（UHAT）本质上极为简洁：在表示相同语言时，可以比 LTL 和 RNN 指数级更简洁，比有限自动机双重指数级更简洁，这导致其非空性验证问题是 EXPSPACE 完全的。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Transformer 本质上是简洁的 |
| 英文题名 | Transformers are Inherently Succinct |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=Yxz92UuPLQ) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | UHAT 简洁性测度 |
| Dataset |  |

> [!tip] 效果简介
> 结果与证据沿用下文“实验与关键发现”中的现有记录；本轮不新增或外推论文事实。

## 概要

**核心问题**：Transformer 的表达力研究长期聚焦于其“能识别什么语言类”（如星自由语言），却忽略了另一个关键维度——**简洁性**（succinctness）。对于同一概念，Transformer 是否能用远比其他形式系统更少的参数或状态来描述？这一问题直接关乎验证复杂度：如果 Transformer 表示极其紧凑，那么即使其表达力上界已知，对其行为的自动验证仍可能异常困难。

**核心洞察**：本文提出将**简洁性**作为衡量 Transformer 表达力的新测度，并证明 Transformer（以唯一硬注意力 Transformer UHAT 为分析模型）在本质上极为简洁——在表示相同语言时，可以比线性时序逻辑（LTL）和循环神经网络（RNN）**指数级更简洁**，比有限自动机**双重指数级更简洁**。这一紧凑性的根源在于 UHAT 能够在多项式尺寸内构造**双重指数级大计数器**（从 0 计数到 $2^{2^n}$），进而仿真 EXPSPACE 完全问题。

**方法定位**：本文采用 **UHAT**（唯一硬注意力 Transformer）作为核心分析模型，并与 **B-RASP**（布尔值 RASP）建立等价性。UHAT 的关键机制在于：通过硬注意力、严格未来掩码和右端断点规则，在多项式层数内实现双重指数级计数能力。已有工作（Jerad et al., 2025）表明，UHAT 的表达力上界同样适用于固定精度的 softmax Transformer，因此本文结论具有实际参考价值。

**主要结果**：
- **非空性问题的复杂度**：UHAT 和 B-RASP 的非空性问题是 **EXPSPACE 完全**的（Theorem 5）。下界通过将 EXPSPACE 完全的 $2^n$-tiling 问题归约到 B-RASP 的非空性得到（Lemma 8），上界则通过将 UHAT 翻译为指数大小的 LTL 公式证明。
- **与 LTL 的简洁性比较**：UHAT 可以比 LTL **指数级更简洁**（Theorem 15）。
- **与有限自动机的简洁性比较**：UHAT 可以比有限自动机 **双重指数级更简洁**（Theorem 17）。
- **与 RNN 的简洁性比较**：UHAT 可以比 RNN（包括状态空间模型 SSM）**指数级更简洁**（Corollary 18）。

**局限与边界**：上述简洁性结果为最坏情况结论，并不意味着所有语言上 Transformer 都更紧凑。分析假设固定精度计算，排除了无限精度下可能更强的计算能力。此外，本文聚焦于描述复杂性，未讨论这些紧凑表示的可学习性。



Transformer 架构已在序列建模领域取得广泛成功，但其表达能力的形式化理解仍存在显著缺口。现有理论工作主要沿两个方向展开：一是将 Transformer 刻画为特定语言类的识别器，例如证明其恰好能识别星自由语言（star-free languages）；二是分析其图灵完备性，即在无限精度或无限深度的极限条件下所能达到的计算能力。然而，这两类分析都忽略了一个关键维度——**简洁性（succinctness）**：即描述同一个概念时，Transformer 所需的最小描述长度可以比传统形式系统短多少。

这一忽略带来了实质性的后果。如果 Transformer 在表示相同语言时远比有限自动机或时序逻辑紧凑，那么对其行为进行形式验证（如非空性检查）的复杂度将被严重低估。换言之，即使 Transformer 的表达力上界已知，若其简洁性远高于比较基准，验证任务的实际难度将远超预期。本文正是从这一观察出发，将**简洁性**确立为衡量 Transformer 表达能力的新测度。

在模型选择上，本文采用**唯一硬注意力 Transformer（Unique-Hard Attention Transformer, UHAT）**作为分析对象。UHAT 是自注意力机制的一种简化和流行抽象，其核心特征包括：每层只允许唯一的最大注意力位置被激活（硬注意力），使用严格未来掩码（causal masking），并通过断点函数（tie-breaking function）处理注意力评分相同的情况。已有工作表明，UHAT 的表达力上界同样适用于固定精度的 softmax Transformer，这使得 UHAT 成为分析实际 Transformer 行为的合理代理模型。

本文的核心动机可以概括为：**通过建立 UHAT 的简洁性上下界，揭示 Transformer 在描述复杂度上的本质优势，并由此推导其验证问题的计算复杂度下界。** 具体而言，本文试图回答以下问题：Transformer 可以比线性时序逻辑（LTL）、有限自动机、循环神经网络（RNN）等经典形式系统紧凑多少？这种紧凑性如何影响自动化验证的可行性？



## 核心方法与创新机理

本文的核心创新在于将分析视角从 Transformer **能识别什么语言类**转移到**描述同一概念需要多大规模**，即提出**简洁性**作为表达力的新测度。这一视角转换揭示了一个此前被忽视的根本性质：Transformer 在表示相同语言时可以远比其他形式系统紧凑，而这种极端的简洁性直接导致其验证问题具有极高的计算复杂度。

### 视角转换：从语言类到简洁性

以往对 Transformer 表达力的研究主要关注其识别的语言类上界（如星自由语言），但忽略了描述复杂性维度。本文明确指出，即使两个形式系统识别完全相同的语言类，它们在描述同一语言时所需的模型尺寸可能存在指数级甚至双重指数级差异。这一洞察构成了所有后续结论的逻辑起点——Transformer 的验证之所以困难，不仅因为它能识别复杂的语言，更因为它能以极紧凑的方式编码这些语言。

### 核心机制：双重指数级大计数器

实现极端简洁性的关键机制是 UHAT 在多项式尺寸内仿真**双重指数级大计数器**。具体而言，UHAT 通过以下设计实现从 0 计数到 $2^{2^n}$：

- **硬注意力**：每个位置精确选择唯一的注意力目标，避免 softmax 的概率分散。
- **严格未来掩码**：位置 $i$ 只能关注 $j < i$，保证因果顺序，使计数能沿序列逐位传递。
- **右端断点规则**：当多个位置满足掩码条件时选择最右侧者，这对在序列中定位“最近的 # 标记”至关重要。

论文通过将 EXPSPACE 完全的 $2^n$-tiling 问题归约到 B-RASP 的非空性，构造性地展示了这一能力：B-RASP 程序用多项式尺寸的注意力操作同时检查水平邻接约束和垂直跨行约束，而跨行约束的检查正依赖于大计数器来追踪行号。这一归约构成了所有下界证明的**因果旋钮**——一旦 Transformer 能编码大计数器，非空性问题的 EXPSPACE 完全性便自然导出。

### 简洁性差距的层次结构

在上述机制基础上，论文建立了 UHAT 与其他形式系统之间的简洁性层次：

| 比较对象 | 简洁性差距 | 依据 |
|----------|-----------|------|
| LTL | UHAT 指数级更简洁 | Theorem 15：存在语言族，UHAT 用多项式尺寸可表示，LTL 需指数级公式 |
| RNN（含 SSM） | UHAT 指数级更简洁 | Corollary 18：由 RNN 可被有限自动机以指数级膨胀模拟，结合双重指数差距得出 |
| 有限自动机 | UHAT 双重指数级更简洁 | Theorem 17：UHAT 多项式尺寸可表示的语言，DFA 需双重指数级状态数 |

同时，反向翻译保持多项式或指数级开销：LTL 到 UHAT 是多项式时间（Proposition 16），UHAT 到 LTL 是指数时间（Proposition 13）。这种非对称性精确刻画了 UHAT 在描述能力上的压缩优势。

### 理论后果：验证问题的复杂度跃升

简洁性的直接后果是验证问题复杂度的跃升。由于 UHAT 可以在多项式尺寸内编码 EXPSPACE 完全问题，其**非空性**和**等价性**均为 EXPSPACE 完全（Theorem 5, Theorem 19）。这意味着即使检查一个 UHAT 是否接受任何输入，在最坏情况下也需要指数空间。这一结论为 Transformer 的形式验证设定了理论上界，也解释了为何在实际中验证 Transformer 极为困难。

### 边界条件

需注意，这些结论基于以下假设：分析对象为 UHAT（唯一硬注意力），但已有工作表明其表达力上界同样适用于固定精度的 softmax Transformer；简洁性结果为最坏情况，不意味着所有语言上 Transformer 都更紧凑；论文未讨论如何学习这些紧凑表示，关注点在描述复杂性而非可学习性。



本文不提出新的模型架构或训练方法，而是从**描述复杂性**的视角重新审视 Transformer 的表达力。研究的核心对象是**唯一硬注意力 Transformer**（UHAT）及其等价的布尔编程语言 **B-RASP**。整个分析框架围绕一个中心问题展开：给定一个概念（形式语言），Transformer 需要多少参数量或层数才能精确描述它？

### 分析对象与计算模型

论文采用 UHAT 作为 Transformer 的抽象模型，其选择基于两个关键事实：
- UHAT 是自注意力的简单且广泛使用的抽象，其表达力上界已被证明同样适用于固定精度的 softmax Transformer（Jerad et al., 2025）。
- UHAT 与 B-RASP 之间存在多项式时间的互译关系，使得下界证明可以在更便于操作的 B-RASP 中构造，再传递回 UHAT。

UHAT 的计算流程由三个模块级联而成：

1. **Token Embedding**：将有限字母表 $\Sigma$ 中的每个符号映射为有理数向量 $\text{emb}: \Sigma \to \mathbb{Q}^d$，作为序列的初始表示。
2. **UHA 层**：带掩码的唯一硬注意力层，由三个仿射变换 $A, B: \mathbb{Q}^r \to \mathbb{Q}^r$ 和 $C: \mathbb{Q}^{2r} \to \mathbb{Q}^s$、掩码谓词 $M$ 以及断点函数 $\tau$ 定义。注意力评分函数为内积形式 $S(\mathbf{v}_i, \mathbf{v}_j) := \langle A(\mathbf{v}_i), B(\mathbf{v}_j) \rangle$，每个位置仅关注评分最高（且满足掩码条件）的唯一位置。
3. **ReLU 层**：对指定坐标应用 ReLU 激活函数，引入非线性。

整个 UHAT 是长度保持函数 $T: \Sigma^+ \to (\mathbb{Q}^s)^+$，由 token embedding 后接固定序列的 UHA 层和 ReLU 层组成，最终通过接受向量与输出向量的内积符号判定接受与否。

### 简洁性测度的定义

传统表达力分析关注 Transformer 能识别哪些语言类（如正则语言、星自由语言等），而本文提出**简洁性**作为新的测度：比较不同形式系统在描述**同一语言**时所需表示的最小尺寸。形式化地，若存在一个语言族，UHAT 可以用多项式尺寸描述，而某个参考形式系统（如 LTL、有限自动机、RNN）需要指数级甚至双重指数级尺寸，则称 UHAT 比该系统更简洁。

### 证明管线

整个理论结果通过一条清晰的证明管线串联：

1. **下界构造**：将 EXPSPACE 完全的 $2^n$-tiling 问题归约到 B-RASP 的非空性。核心技巧是利用严格未来掩码与右端断点规则，在 B-RASP 中构造双重指数级大计数器（从 0 数到 $2^{2^n}$），从而在多项式尺寸内仿真 tiling 问题的所有约束。
2. **复杂度传递**：通过 B-RASP 到 UHAT 的多项式时间翻译（Lemma 9），将非空性问题的 EXPSPACE 完全下界从 B-RASP 传递到 UHAT（Theorem 5）。
3. **上界验证**：证明 UHAT 的计算值只需多项式比特表示（Proposition 12），且 UHAT 可在指数时间内翻译为等价的 LTL 公式（Proposition 13），从而确立 EXPSPACE 上界。
4. **简洁性分离**：利用非空性问题的复杂度鸿沟，通过反证法得出：若 UHAT 不比 LTL/有限自动机/RNN 更简洁，则非空性问题的复杂度会坍缩到更低复杂度类，与已证明的 EXPSPACE 完全性矛盾。

### 输入输出流

- **输入**：有限字母表 $\Sigma$ 上的有限长度词 $w \in \Sigma^+$。
- **输出**：接受或拒绝的二值判定。
- **中间表示**：每层输出有理数向量序列，维度由层宽度参数决定。B-RASP 则操作布尔向量，每个位置对应一个布尔谓词的取值。



### 1. UHAT 架构的组成模块

本文的分析基于**唯一硬注意力 Transformer（UHAT）**，其计算过程由以下三个核心模块顺序组合而成：

**Token 嵌入层**：将输入字母表 $\Sigma$ 中的每个符号映射为一个有理数向量，即 $\text{emb}: \Sigma \to \mathbb{Q}^d$。这是所有后续计算的起点。

**UHA 层**：一个宽度为 $r > 0$ 的掩码唯一硬注意力层由以下组件定义：
- 三个仿射变换 $A, B: \mathbb{Q}^r \to \mathbb{Q}^r$ 和 $C: \mathbb{Q}^{2r} \to \mathbb{Q}^s$；
- 一个掩码谓词 $M$，用于限制注意力范围；
- 一个断点函数 $\tau$，在多个位置取得相同最大评分时决定唯一选中位置。

该层的核心操作是计算位置 $i$ 与 $j$ 之间的注意力评分：

$$S(\mathbf{v}_i, \mathbf{v}_j) := \langle A(\mathbf{v}_i), B(\mathbf{v}_j) \rangle$$

即对两个仿射变换的输出求内积。随后，在满足 $M(i,j)$ 的位置中选取评分最高者（由 $\tau$ 断点），将其与 $\mathbf{v}_i$ 拼接后经 $C$ 变换得到该位置的输出。

**ReLU 层**：对向量中指定坐标施加 ReLU 激活函数，提供非线性能力。

一个 UHAT 即由上述 Token 嵌入层后接固定序列的 UHA 层和 ReLU 层构成，是一个保持长度的函数 $T: \Sigma^+ \to (\mathbb{Q}^s)^+$。

### 2. B-RASP 注意力操作

B-RASP 是 UHAT 的高层抽象，其注意力操作有两种断点模式，分别定义为：

**左端断点**（取满足条件的最小索引 $j$）：

$$P_{t+1}(i) := \blacktriangleleft_{j} \left[ M(i,j), S(i,j) \right] V(i,j) : D(i)$$

**右端断点**（取满足条件的最大索引 $j$）：

$$P_{t+1}(i) := \blacktriangleright_{j} \left[ M(i,j), S(i,j) \right] V(i,j) : D(i)$$

其中 $M(i,j)$ 为掩码谓词，$S(i,j)$ 为评分谓词，$V(i,j)$ 为值谓词，$D(i)$ 为默认值。B-RASP 的操作语义是：在满足 $M(i,j)$ 且 $S(i,j)=1$ 的位置中按断点规则选取唯一的 $j_i$，然后将 $P_{t+1}(i)$ 设为 $V(i,j_i)$（若存在），否则设为 $D(i)$。

### 3. 大计数器构造中的关键公式

证明 UHAT 简洁性的核心机制是构造**双重指数级大计数器**，即用多项式尺寸的 UHAT 表示 $0$ 到 $2^{2^n}$ 的计数。这一构造依赖以下关键注意力操作：

**二进制递增检查**：验证当前位置的二进制计数器是否为前一个 `#` 位置计数器的加 $1$ 结果。其 B-RASP 表达式为：

$$C_{+1}(i) := \mathscr{P}_j \left[ j < i, Q_{\#}(j) \right] \bigvee_{k=1}^{4} \big( \bigwedge_{r=1}^{k-1} { -C_r(i) \wedge C_r(j) } \big) \wedge C_k(i) \wedge \neg C_k(j) \wedge \big( \bigwedge_{r=k+1}^{4} C_r(i) C_r(j) \big) : 1$$

该公式使用右端断点 $\mathscr{P}_j$（即 $\blacktriangleright$ 的变体），在 $j < i$ 且 $Q_{\#}(j)$ 为真的位置中寻找最右侧的 `#`，然后检查 $i$ 处的计数器 $C_k(i)$ 是否恰好是 $j$ 处计数器 $C_k(j)$ 的二进制加 $1$。

**水平约束检查**：验证相邻瓦片是否满足给定的水平约束关系 $H$：

$$M(i) := \nu_j [ j < i, Q_a(j) \vee Q_b(j) \vee Q_c(j) ] \bigvee_{(h,h') \in H} Q_h(j) \wedge Q_{h'}(i) : 1$$

该公式同样使用右端断点，在 $i$ 左侧最近的瓦片符号位置 $j$ 处，检查 $(Q_h(j), Q_{h'}(i))$ 是否属于允许的水平相邻关系集合 $H$。

### 4. B-RASP 到 UHAT 的翻译评分函数

从 B-RASP 到 UHAT 的多项式时间翻译（Lemma 9）依赖于一种受限注意力形式，其对应的 UHAT 评分函数设计为：

$$\Big( \sum_{k \in K} \big( P_k(i) P_k(j) + (1 - P_k(i)) (1 - P_k(j)) \big) \Big) - \big( 1 - S(j) \big)$$

该评分在位置 $j$ 上所有谓词 $P_k$ 与位置 $i$ 完全匹配且 $S(j)=1$ 时取得最大值，从而精确仿真 B-RASP 的注意力选择行为。

### 5. UHAT 到 LTL 的翻译公式

为证明 UHAT 到 LTL 的指数上界翻译（Proposition 13），需将每个 UHA 层的输出递归地编码为 LTL 公式。对于使用严格未来掩码和右端断点的注意力层，其翻译为：

$$\varphi_{v}^{\ell+1} := \bigvee_{\substack{u, a \in F^r: \\ C(u, a) = v}} \varphi_{u}^{\ell} \wedge \big( \big( \bigvee_{\substack{b \in F^r: \\ S(u, a) < S(u, a)}} \varphi_{b}^{\ell} \big) \mathbf{S} \big( \varphi_{a}^{\ell} \wedge \neg \mathbf{P} \bigvee_{\substack{b \in F^r: \\ S(u, b) > S(u, a)}} \varphi_{b}^{\ell} \big) \big)$$

其中 $\varphi_{v}^{\ell}$ 表示第 $\ell$ 层输出为向量 $v$ 的 LTL 公式，$F^r$ 为所有可能的有理数向量值的有限集合（由固定精度保证），$\mathbf{S}$ 为“自从”时序算子。整个 UHAT 的最终接受公式为：

$$\varphi := \bigvee_{\mathbf{v} \in F^s: \langle \mathbf{t}, \mathbf{v} \rangle > 0} \varphi_{\mathbf{v}}^{m}$$

其中 $\mathbf{t}$ 为接受向量，当最终层输出与其内积为正时接受。



## 实验与关键发现

### 核心理论结果

本文是一项理论工作，不涉及传统意义上的数据集实验，而是通过一系列严格的形式化定理建立 UHAT 的表达力边界。核心结果围绕 **EXPSPACE 完全性** 和 **简洁性差距** 两条主线展开。

#### 非空性与等价性问题的下界

**Theorem 5** 确立了 UHAT 和 B-RASP 的非空性问题是 EXPSPACE 完全的。证明的下界方向（EXPSPACE-hardness）通过将 EXPSPACE 完全的 $2^n$-tiling 问题归约到 B-RASP 的非空性来实现（Lemma 8）：给定一个 $2^n$-tiling 实例，可以在 $n$ 的多项式时间内构造一个 B-RASP 程序，该程序接受的语言非空当且仅当 tiling 实例有解。上界方向（EXPSPACE membership）则依赖于 Proposition 12 和 Proposition 13：UHAT 计算中的值只需要多项式比特表示，且 UHAT 可在指数时间内翻译为 LTL 公式，而 LTL 的非空性在 PSPACE 中，结合指数爆炸即得 EXPSPACE 上界。

作为推论，**Theorem 19** 进一步证明 UHAT 的等价性问题也是 EXPSPACE 完全的。这意味着即使是判定两个 Transformer 是否识别同一语言，在最坏情况下也需要指数空间。

#### 简洁性差距：与经典形式系统的对比

本文的核心洞察是：Transformer 在描述相同概念时可以远比其他形式系统更紧凑。具体结果如下：

| 对比对象 | 简洁性差距 | 锚点 |
|---------|-----------|------|
| LTL | 指数级更简洁 | Theorem 15 |
| 有限自动机 | 双重指数级更简洁 | Theorem 17 |
| RNN（含 SSM） | 指数级更简洁 | Corollary 18 |

这些下界结果的证明依赖于 UHAT 能够编码 **双重指数级大计数器**：通过硬注意力、严格未来掩码和右端断点规则的组合，UHAT 可以在多项式尺寸内表示从 $0$ 到 $2^{2^n}$ 的计数。这是所有简洁性下界的核心构造机制。

值得注意的是，Proposition 16 同时给出了一个正向翻译：给定任意 LTL 公式 $\varphi$，可以在多项式时间内构造一个识别相同语言的 UHAT。这意味着 UHAT 的表达力至少不低于 LTL，而 Theorem 15 表明它在紧凑性上可以指数级优于 LTL。

#### 结果的意义与局限

这些理论结果解释了为什么 Transformer 的形式化验证极为困难：即使模型规模不大，其编码的语言也可能具有极高的描述复杂度，导致验证问题的复杂度达到 EXPSPACE 完全。换言之，**Transformer 的本质简洁性恰恰是其验证困难的根本原因**。

需要明确的是，这些简洁性结果是最坏情况下的下界，并不意味着在所有语言上 Transformer 都更紧凑。此外，分析对象限于 UHAT 模型，但已有工作（Jerad et al., 2025）表明 UHAT 的表达力上界同样适用于固定精度的 softmax Transformer，因此这些结论对实际模型具有参考意义。

### 关键构造机制

证明中反复出现的核心构造是 **二进制递增检查注意力**（Example 4 中的 $C_{+1}$ 操作）和 **水平约束检查注意力**（$M$ 操作）。前者利用严格未来掩码和右端断点，在多项式尺寸内实现双重指数级计数器的递增验证；后者则在 tiling 归约中用于检查相邻符号是否满足给定的水平约束关系 $H$。这两个构造共同支撑了从 $2^n$-tiling 到 B-RASP 非空性的多项式时间归约（Lemma 8），进而得到 EXPSPACE 下界。

从 B-RASP 到 UHAT 的翻译（Lemma 9）要求注意力操作满足特定的受限形式，其中评分函数仅依赖目标位置 $j$ 的布尔谓词 $S(j)$ 以及源位置 $i$ 和目标位置 $j$ 的谓词匹配 $\bigwedge_{k \in K} P_k(i) P_k(j)$。该受限形式保证了翻译可在多项式时间内完成，从而将 B-RASP 的复杂度结果传递到 UHAT。



## 定位与知识库关联

### 1. 形式语言接受器的表达力谱系

本文的核心贡献在于将 **简洁性（succinctness）** 确立为 Transformer 表达力的一个新的测度维度。传统上，对 Transformer 表达力的分析聚焦于其识别的语言类——例如，UHAT 所能识别的语言恰好是星自由语言（star-free languages），这与 LTL 和有限自动机等价。然而，本文揭示了一个此前被忽视的关键事实：**在描述相同语言时，不同形式系统的紧凑程度可以存在指数级甚至双重指数级的差距**。

具体而言，本文在统一的形式语言接受器框架下，建立了以下简洁性层次关系（箭头方向表示“可以指数级或双重指数级更简洁”）：

- **UHAT → LTL**：指数级更简洁（Theorem 15）。给定一个 LTL 公式，可在多项式时间内构造等价的 UHAT（Proposition 16），但反向翻译在最坏情况下需要指数级膨胀。
- **UHAT → 有限自动机**：双重指数级更简洁（Theorem 17）。这是本文最强的简洁性分离结果，其根源在于 UHAT 能够在多项式尺寸内编码 $2^{2^n}$ 量级的大计数器，而有限自动机必须以状态数显式存储这些计数。
- **UHAT → RNN（含 SSM）**：指数级更简洁（Corollary 18）。这一推论建立在 RNN 与有限自动机的关系之上：固定精度 $k$、隐藏维度 $d$ 的 RNN 等价于一个具有 $2^{kd}$ 个状态的有限自动机（Proposition 3，参见 Siegelmann & Sontag, 1995），因此 UHAT 相对于 RNN 的简洁性优势自然成立。

### 2. 与基线方法的关系

本文的基线比较对象均为形式语言理论中的经典语言接受器，而非具体的 Transformer 变体：

- **LTL**（Pnueli, 1977）：线性时序逻辑是星自由语言的规范描述语言。本文证明了 UHAT 在描述星自由语言时可以比 LTL 指数级更紧凑，同时给出了从 LTL 到 UHAT 的多项式时间构造性翻译（Proposition 16），表明 UHAT 在表达力上至少不弱于 LTL。
- **有限自动机**（McNaughton & Papert, 1971）：作为星自由语言的识别器，有限自动机的状态数直接反映了描述复杂度。双重指数级的简洁性差距揭示了 Transformer 架构在编码长程依赖和大规模计数方面的根本优势。
- **RNN**（Siegelmann & Sontag, 1995）：固定精度 RNN 的计算能力受限于有限状态空间。本文的指数级简洁性结果表明，即使 RNN 在理论上是图灵完备的（无限精度下），在实际的固定精度约束下，其描述效率远逊于 UHAT。

### 3. 核心机制：大计数器的构造

所有简洁性下界证明的核心技术枢纽是 **UHAT 编码双重指数级大计数器** 的能力。通过以下三个关键设计选择，UHAT 可以在多项式尺寸内仿真 EXPSPACE 完全的 $2^n$-tiling 问题：

1. **硬注意力**：通过唯一硬注意力（unique hard attention）选择单个位置，避免了 softmax 平均注意力的信息稀释。
2. **严格未来掩码**：确保注意力只能关注严格过去的位置，赋予模型自回归的因果归纳偏置。
3. **右端断点规则**：在多个等分位置中选择最右端的一个，使得模型能够精确定位“最近一次出现的特定符号”，从而在序列中维护和更新计数器。

这一构造构成了从 $2^n$-tiling 到 B-RASP 非空性问题的归约（Lemma 8），进而通过 B-RASP 到 UHAT 的多项式时间翻译（Lemma 9），得到 UHAT 非空性的 EXPSPACE 下界（Theorem 5）。

### 4. 适用边界与局限

本文的分析框架存在以下明确的适用边界：

- **模型限定于 UHAT**：所有理论结果针对唯一硬注意力 Transformer。尽管已有工作（Jerad et al., 2025）表明 UHAT 的表达力上界同样适用于固定精度的 softmax Transformer，但简洁性结果是否可直接迁移至 softmax 情形仍需进一步验证。
- **固定精度假设**：本文假设所有计算在固定精度有理数下进行。这一假设符合实际硬件的离散计算特性，但也排除了无限精度下可能更强的计算能力（例如，无限精度 RNN 是图灵完备的）。
- **最坏情况分析**：简洁性分离结果是最坏情况下的理论下界，并不意味着在所有语言上 Transformer 都更紧凑。存在某些语言可能用 LTL 或有限自动机描述更为自然。
- **描述复杂性而非可学习性**：本文关注的是 Transformer 作为语言描述工具的紧凑程度，而非这些紧凑表示是否可以通过梯度下降等方法有效学习。可学习性问题被明确列为开放问题。

### 5. 开放问题

论文明确提出了以下未来研究方向：

1. **扩展简洁性分析至 softmax 和平均硬注意力 Transformer**：固定精度 softmax Transformer 和平均硬注意力（average hard attention）Transformer 的简洁性特征尚待刻画。
2. **开发自动化 Transformer 验证工具**：尽管非空性问题是 EXPSPACE 完全的，理论上极难处理，但实际中可借鉴自动验证领域的技术（如 SAT/SMT 求解、抽象解释等）来开发实用工具。
3. **识别低验证复杂度的 Transformer 子类**：研究无法编码大计数器的 Transformer 架构子类（例如限制注意力范围、限制层数或头数），以降低验证的计算复杂度。
4. **探索简洁 Transformer 的可学习性**：理论上的紧凑表示是否对应实践中可学习的参数配置，是一个连接理论表达力与经验成功的关键问题。



## 原文 PDF

![[paperPDFs/ICLR_2026/Transformers_are_Inherently_Succinct.pdf]]
