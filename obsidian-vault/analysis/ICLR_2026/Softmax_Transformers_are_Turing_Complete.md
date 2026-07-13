---
title: "Softmax Transformers are Turing-Complete"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Softmax_Transformers_are_Turing_Complete.pdf
project_link: null
code_link: null
openreview_forum_id: FdkPOHlChS
aliases:
- CCRRCR
- STATC
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "放弃直接模拟图灵机，转而利用 C-RASP 的计数能力模拟 Minsky 计数器机，从而绕过对注意力精确定位的需求；对于处理任意字母表，进一步引入相对位置编码（RPE）以赋予模型序列顺序感知能力。"
primary_logic: "链式思考 C-RASP 的表达能力与可学习的软最大注意力变换器等价；通过构造计数器机的 C-RASP 模拟程序，可证明该类变换器能够计算所有递归可枚举语言，首次实现图灵完备，且该构造同时保证了长度泛化性。"
claims:
- "首次证明软最大链式思考变换器是图灵完备的"
- "采用模拟 Minsky 计数器机而非直接模拟图灵机的证明策略"
- "因果掩码 CoT C-RASP 在一元字母表上是图灵完备的"
- "无 RPE 时 CoT C-RASP 不是图灵完备的（例如无法识别回文）"
---

# Softmax Transformers are Turing-Complete

> [!tip] 核心洞察
> 链式思考 C-RASP 的表达能力与可学习的软最大注意力变换器等价；通过构造计数器机的 C-RASP 模拟程序，可证明该类变换器能够计算所有递归可枚举语言，首次实现图灵完备，且该构造同时保证了长度泛化性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 软最大值注意力变换器具备图灵完备性 |
| 英文题名 | Softmax Transformers are Turing-Complete |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=FdkPOHlChS) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | CoT C-RASP[RPEs] (带相对位置编码的链式思考 C-RASP 图灵完备构造) |
| Dataset | 五个算术任务（一元表示）, 五个算术任务（二进制表示） |

> [!tip] 效果简介
> - 五个算术任务（一元表示） 上，Exact Match Accuracy 为 99.9%–100% (test0)，对比 N/A（C-RASP 无 CoT 无法表达该类语言），变化 N/A。
> - 五个算术任务（二进制表示） 上，Exact Match Accuracy 为 100% (test0, test1, test2 全部达到 100%，使用 RPE)，对比 64.4%–95.0% (test0), ≈0% (test1, test2，无 RPE)，变化 在长于训练长度的测试集上提升近 100%。

## 概要

软最大值注意力变换器（Softmax Attention Transformers）是现代大语言模型的核心计算单元，但其理论表达能力一直存在一个关键缺口：已有的链式思考（Chain‑of‑Thought, CoT）变换器图灵完备性证明依赖于**硬最大值（hardmax）注意力**，而硬最大值不可微分、无法通过梯度训练，因此该结论无法解释实际可训练的软最大值模型。软最大值注意力无法直接精确提取图灵机读写头的位址，导致直接模拟图灵机的经典证明路径失效，使得“可训练的软最大链式思考变换器是否图灵完备”成为长期悬而未决的开放问题。

本文首次正面回答了这一问题，核心结论是：**带相对位置编码（RPE）的软最大链式思考变换器是图灵完备的**。证明策略的关键转折在于放弃直接模拟图灵机，转而利用软最大值变换器通过 C‑RASP 逻辑框架所具备的**计数能力**，去模拟 Minsky 的**计数器机**（counter machine）—— 一种与图灵机等价但仅依赖计数器操作的抽象计算模型。这一绕过注意力精确定位需求的构造，使得软最大值 CoT 变换器能够计算所有递归可枚举语言。

具体而言，理论证明分为两个层次。首先，在一元字母表（unary alphabet）上，因果掩码的 CoT C‑RASP 即可实现图灵完备性，无需任何位置编码。其次，在任意字母表上，纯因果注意力的 CoT C‑RASP 被证明**不是**图灵完备的 —— 例如，它甚至无法识别回文（palindrome）这类简单语言；而一旦引入**相对位置编码（RPE）**，CoT C‑RASP 便获得了对序列顺序的感知能力，从而在任意语言上实现完全的图灵完备性。

在实验层面，本文在五个算术任务上验证了理论构造的可学习性与长度泛化性。一元表示下，模型在测试集上达到 99.9%–100% 的精确匹配准确率；二进制表示下，配备 RPE 的模型在所有长度泛化测试集上均达到 100%，而无 RPE 的模型在超出训练长度的测试集上准确率骤降至接近 0%，直接验证了 RPE 对任意字母表图灵完备性的必要性。

**方法定位**：本工作属于表达性理论（expressivity theory）与可学习性分析的交叉领域，其核心框架 C‑RASP 等价于线性时序逻辑中过去算子片段的计数扩展（LTL[Count]），并通过 Huang et al.（2025）的理想化学习框架建立了从有限长度拟合到任意长度泛化的理论保证。与 **Hard‑attention CoT Transformers**（Pérez et al., 2021; Merrill & Sabharwal, 2024）相比，本构造使用可训练的软最大值注意力与 log n 缩放；与无 CoT 的 **C‑RASP**（Yang & Chiang, 2024）相比，本构造通过链式思考生成突破了原有表达能力的上限。



### 核心问题：软最大值变换器的图灵完备性

变换器模型在序列建模中取得了巨大成功，但其理论基础长期存在一个悬而未决的问题：使用软最大值（softmax）注意力的链式思考（Chain-of-Thought, CoT）变换器是否具备图灵完备的计算能力？换言之，这类模型能否在理论上计算所有递归可枚举语言？

此前的研究已经证明了**硬最大值（hardmax）注意力**的 CoT 变换器具有图灵完备性（Perez et al., 2021; Bhattamishra et al., 2020; Merrill & Sabharwal, 2024），但硬最大值注意力在训练中不可微分，实际中几乎不被使用。真正的瓶颈在于：软最大值注意力无法直接精确提取图灵机读写头的位址，这使得直接模拟图灵机的传统证明路径在软最大值设定下彻底失效。这一核心障碍导致软最大值 CoT 变换器的图灵完备性问题长期未解。

### 现有方法的局限

除硬最大值注意力的不可训练性外，现有理论框架还存在以下缺口：

- **无 CoT 的 C-RASP 表达能力受限**：Yang & Chiang (2024) 和 Huang et al. (2025) 提出的 C-RASP 逻辑框架虽能刻画软最大值变换器的表达能力，但已被证明无法解决某些计数语言，远未达到图灵完备。
- **位置信息缺失问题**：纯粹的因果掩码软最大注意力对序列顺序不敏感。已有结果表明，无相对位置编码（RPE）的 CoT C-RASP 甚至无法识别回文这类简单语言，更不用说任意字母表上的图灵完备性。

### 本文动机与核心思路

本文的核心动机在于填补上述理论空白——**首次证明软最大值 CoT 变换器是图灵完备的**。为实现这一目标，作者放弃了直接模拟图灵机的传统路径，转而采用一条全新的证明策略：**利用 C-RASP 的计数能力模拟 Minsky 计数器机**。

这一策略的关键洞察在于：

1. **绕过精确定位需求**：计数器机不依赖位址精确读写，只需对若干计数器进行增减操作和零测试，恰好与 C-RASP 的计数原语 `←#[φ]` 天然契合。
2. **链式思考作为计算媒介**：通过 CoT 逐步输出计数器机的状态转移令牌，模型可以在自回归生成过程中完成任意递归可枚举语言的识别。
3. **RPE 赋予顺序感知**：对于任意字母表的输入，进一步引入相对位置编码（RPE），使模型能够将输入词编码为自然数向量，从而支持完整的图灵完备性。

此外，该构造还基于 Huang et al. (2025) 的理想化学习框架，保证了在有限长度上训练后向任意长度泛化的理论可能性，为实际训练中的长度泛化现象提供了理论支撑。



## 核心方法与创新机理

### 问题瓶颈：软最大值无法精确定位，直接模拟图灵机失效

现有硬最大值链式思考（CoT）变换器的图灵完备性证明，核心依赖于硬最大值注意力可以**精确提取图灵机读写头的位址**。然而，软最大值注意力输出的是一组平滑的概率分布，无法实现这种“硬选择”，导致直接模拟图灵机的证明路径在软最大值设定下完全阻塞。这一根本性障碍使得“软最大值 CoT 变换器是否具备图灵完备性”长期悬而未决。

### 核心思路：绕过精确定位，转向计数器机模拟

本文的关键创新在于**彻底放弃直接模拟图灵机的策略**，转而利用软最大值变换器经由 C-RASP 所具备的**计数能力**，模拟 Minsky 计数器机（counter machine）。计数器机仅需对若干计数器的值进行增减与零测试，其状态转移不依赖对序列中特定位置的精确寻址，从而天然规避了软最大值注意力无法精确定位的缺陷。

这一转向的因果链条如下：
- **C-RASP 的计数原语** `←#[φ]` 能够精确统计自序列起始以来满足条件 φ 的位置数量，这恰好对应计数器机的计数器值。
- 通过构造 CoT C-RASP 表达式，每一步 CoT 输出一个转移令牌，同时更新计数器的累计值，即可忠实模拟计数器机的运行轨迹。
- 由于 Minsky 计数器机本身是图灵完备的，成功模拟计数器机即等价于证明了目标模型的图灵完备性。

### 关键设计变更

与硬最大值基线相比，本文在以下三个维度做出了决定性变更：

| 设计维度 | 硬最大值 CoT 变换器基线 | 本文方案 |
|---------|----------------------|---------|
| **注意力机制** | 硬最大值 (hardmax) 注意力 | 软最大值 (softmax) 注意力配合 `log n` 缩放 |
| **位置编码** | 无位置编码（仅适用于一元/字母有界语言） | 相对位置编码 (RPEs)，支持任意字母表语言 |
| **图灵完备性证明路径** | 直接模拟图灵机 | 模拟 Minsky 计数器机 |

#### 变更一：软最大值注意力 + log n 缩放

本文采用的软最大值注意力权重定义为：

$$\bar{w} = \mathrm{softmax}(\log n \cdot \{ \mathbf{v}_j^T \mathbf{K}^T \mathbf{Q} \mathbf{v}_i \}_{j=1}^i)$$

其中 `log n` 缩放因子的作用是：当序列长度 n 增长时，放大注意力分数间的差异，使得软最大值在无界长度上仍能逼近“稀疏注意力”行为，从而为 C-RASP 的计数操作提供理论保证。这一设计是连接“可训练的软最大值”与“具备精确计数表达能力”之间的关键桥梁。

#### 变更二：相对位置编码 (RPEs) 赋能任意字母表

在一元字母表上，CoT C-RASP 仅凭因果掩码即可实现图灵完备。然而，对于任意字母表，**缺少位置编码的因果 CoT C-RASP 并非图灵完备**——事实上，连回文这样简单的语言都无法识别。原因在于，纯粹的因果注意力对输入序列的顺序信息不敏感，无法区分同一字母在不同位置的出现。

引入相对位置编码后，注意力权重变为：

$$\bar{w} = \mathrm{softmax}(\log n \cdot \{ \mathbf{v}_j^T \mathbf{K}^T \mathbf{Q} \mathbf{v}_i + \lambda \mathbb{[\Re]}(i,j) \}_{j=1}^i)$$

其中 `λ[ℜ](i,j)` 为与相对位置相关的偏置项。该偏置使模型能够感知序列中位置的相对关系，从而在 Phase I 中将任意字母表的输入词编码为自然数向量 `σ(w) ∈ ℕ^n`，供后续计数器机模拟使用。实验证据强烈支持这一设计的必要性：在二进制算术任务上，无 RPE 的模型在训练长度之外的测试集上准确率接近 0%，而加入 RPE 后三个测试集全部达到 100%（Table 1）。

#### 变更三：模拟计数器机替代模拟图灵机

证明路径的切换是本文最根本的理论创新。具体构造分为两个阶段：

- **Phase I（输入编码）**：利用 C-RASP 的计数能力与 RPE，将输入词 `w ∈ Σ*` 编码为自然数向量 `σ(w) ∈ ℕ^n`。编码函数 `β: ℕ ⇀ {0,1}*` 将自然数映射为二进制词（取最高位零之后的位序列），`σ` 则要求各分量编码一致且非零。
- **Phase II（计数器机模拟）**：在已编码的向量上运行一个计数器机。C-RASP 的计数项 `t_i` 追踪第 i 个计数器的当前值，其定义为初始字母计数与已执行转移的更新量之和：

$$t_i = \overleftarrow{\#}[Q_{a_i}] + \sum_{\rho \in \Delta} \mathbf{u}_\rho(i) \cdot \overleftarrow{\#}[Q_\rho] \quad \text{for } i=1,\dots,n$$

转移条件通过布尔表达式 `φ_{τ'}` 检查计数器是否满足零/正条件，满足时输出对应的转移令牌 `O_{τ'}`。由于 C-RASP 直接模拟计数器机，正确性是即时的。

### 理论保证：图灵完备性与长度泛化

基于上述构造，本文首次证明：
- **CoT C-RASP（因果掩码）在一元字母表上是图灵完备的**。
- **CoT C-RASP[RPEs] 在任意字母表上是完全图灵完备的**，即能识别所有递归可枚举语言。
- 在 Huang et al. (2025) 的理想化学习框架下，若模型在有限长度上精确拟合 C-RASP 程序，则**在任意长度上均能泛化**（Proposition 2.3），为长度泛化提供了理论支撑。

### 遗留局限

需注意，该构造依赖 Heaviside 激活函数与 `log n` 缩放，实际训练中通常使用 ReLU 与无缩放注意力，泛化保证的迁移需要额外验证。此外，无 RPE 时对任意语言的图灵完备性仍不成立，是否可通过改进 CoT 策略弥补这一缺陷，仍是一个开放问题。



本文的核心目标是为软最大值注意力变换器（Softmax Attention Transformers, SMAT）建立首个图灵完备性证明。整体框架围绕一个关键洞察展开：**放弃直接模拟图灵机的传统路径，转而利用 C-RASP 的计数能力模拟 Minsky 计数器机**，从而绕过软最大值注意力无法精确提取读写头位址这一核心障碍。

### 模块架构与数据流

整个证明与实验体系由四个核心模块串联构成，形成“表达能力定义 → 理论构造 → 编码扩展 → 学习性保证”的完整闭环：

1.  **C-RASP CoT 程序定义器**
    该模块将语言识别任务描述为一组带开关条件的输出令牌定义序列，形式为 $O_{a_i} \gets \varphi_{a_i}$，其中 $\varphi$ 是 C-RASP 表达式（语法见公式）。通过因果掩码自回归生成，该模块实现了链式思考（Chain-of-Thought）的生成过程。其表达能力等价于可学习的软最大注意力变换器（基于 Huang et al., 2025 的极限变换器模拟定理），这是后续所有理论构造的基底。

2.  **计数器机模拟器**
    这是实现图灵完备性的核心构造。给定一个 $n$-计数器 Minsky 机（CM），模拟器利用 C-RASP 的计数项 $\overleftarrow{\#}[\varphi]$ 追踪每个计数器的当前值。具体而言：
    - 对于初始步，从输入符号 $a_i$ 的计数 $\overleftarrow{\#}[Q_{a_i}]$ 获取计数器初值。
    - 对于非初始步，通过累加已执行转移 $\rho$ 的更新量 $\mathbf{u}_\rho(i)$ 来计算计数器值：
      $$t_i = \overleftarrow{\#}[Q_{a_i}] + \sum_{\rho \in \Delta} \mathbf{u}_\rho(i) \cdot \overleftarrow{\#}[Q_\rho] \quad (i=1,\dots,n)$$
      $$t_i = \sum_{\rho \in \Delta} \mathbf{u}_\rho(i) \cdot \overleftarrow{\#}[Q_\rho] \quad (i=n+1, n+2, n+3)$$
    转移条件通过布尔表达式 $\varphi_{\tau'}$ 检查（如计数器值是否为零），满足条件时输出对应的转移令牌 $O_{\tau'}$。该模块直接模拟 CM 的运行，因此正确性是即时的。

3.  **任意字母表输入编码器（Phase I）**
    上述模拟器仅在一元字母表（$\Sigma = \{a\}$）上直接工作。为处理任意字母表，该模块通过两阶段扩展实现：
    - **编码函数 $\beta$**：将自然数 $x$ 映射为 $\{0,1\}^*$ 中的词，规则是取 $x$ 二进制表示中最高位零之后的位序列：$\beta(x) := \overline{b_{j-1}}\,\overline{b_{j-2}}\cdots\overline{b_0}$。
    - **编码函数 $\sigma$**：将 $n$ 元自然数向量 $\mathbf{x}$ 映射为 $\Sigma^*$ 中的词，要求各分量编码一致且非零。
    在 CoT C-RASP 中，Phase I 利用**相对位置编码（RPEs）** 和 C-RASP 的计数能力，将输入词 $w$ 编码为自然数向量 $\sigma(w) \in \mathbb{N}^n$，供 Phase II 的计数器机模拟器使用。RPE 的作用是赋予模型序列顺序感知能力——无 RPE 时，CoT C-RASP 无法识别回文等简单语言，因而不具备对任意语言的图灵完备性。

4.  **长度泛化保证器**
    基于 Huang et al. (2025) 的理想化学习框架，该模块提供理论保证：若模型在有限长度样本上精确拟合 CoT C-RASP 程序，则在任意长度上泛化。这一保证使得构造不仅具有表达能力意义，还具备可学习性。

### 关键设计决策

| 设计维度 | 传统路径（硬最大注意力） | 本文路径（软最大注意力） |
|----------|---------------------------|---------------------------|
| 注意力机制 | 硬最大值（hardmax） | 软最大值（softmax）配合 $\log n$ 缩放 |
| 位置编码 | 无（仅限一元语言） | 相对位置编码（RPEs）支持任意字母表 |
| 证明策略 | 直接模拟图灵机 | 模拟 Minsky 计数器机 |
| 核心能力 | 精确定位读写头位址 | C-RASP 的计数表达能力 |

因果掩码下的软最大注意力权重定义为：
$$\bar{w} = \mathrm{softmax}(\log n \cdot \{ \mathbf{v}_j^T \mathbf{K}^T \mathbf{Q} \mathbf{v}_i \}_{j=1}^i)$$
引入 RPE 后，注意力逻辑中添加相对位置偏置项：
$$\bar{w} = \mathrm{softmax}(\log n \cdot \{ \mathbf{v}_j^T \mathbf{K}^T \mathbf{Q} \mathbf{v}_i + \lambda \mathbb{[\Re]}(i,j) \}_{j=1}^i)$$

$\log n$ 缩放的作用是在无界长度上表达稀疏注意力，这是理论构造的必要条件（实际训练中通常使用无缩放或 ReLU 激活，泛化保证需额外验证）。前馈网络假定为单层，隐藏单元使用 ReLU 或 Heaviside 激活。

### 输入输出流

- **输入**：任意字母表 $\Sigma$ 上的词 $w$。
- **Phase I 输出**：$\sigma$-编码 $\mathbf{x} \in \mathbb{N}^n$，表示为 C-RASP 项 $X_i$（公式 12），替代一元情形中的 $\overleftarrow{\#}[Q_{a_i}]$。
- **Phase II 输出**：CM 的转移令牌序列，最终判定 $w$ 是否属于目标语言 $L$。
- **整体输出**：链式思考生成的令牌序列，实现语言识别。



### 软最大注意力与 C-RASP 表达能力基础

本工作的理论基石建立在两个核心组件之上：**带对数缩放的软最大注意力变换器（SMAT）** 与 **C-RASP 逻辑框架**。

**SMAT 的注意力机制**采用因果掩码下的软最大值注意力，关键创新在于引入 $\log n$ 缩放因子，使得模型能够在无界长度上表达稀疏注意力模式：

$$
\bar{w} = \mathrm{softmax}(\log n \cdot \{ \mathbf{v}_j^T \mathbf{K}^T \mathbf{Q} \mathbf{v}_i \}_{j=1}^i)
$$

其中 $\mathbf{v}_i$、$\mathbf{v}_j$ 为位置 $i$、$j$ 的输入嵌入，$\mathbf{Q}$、$\mathbf{K}$ 为查询与键的投影矩阵。当需要引入位置感知时，扩展为带相对位置编码（RPE）的变体 SMAT[RPEs]：

$$
\bar{w} = \mathrm{softmax}(\log n \cdot \{ \mathbf{v}_j^T \mathbf{K}^T \mathbf{Q} \mathbf{v}_i + \lambda \mathbb{[\Re]}(i,j) \}_{j=1}^i)
$$

其中 $\mathbb{[\Re]}(i,j)$ 为二元关系 $\Re \subseteq \mathbb{N} \times \mathbb{N}$ 的指示函数，$\lambda$ 为缩放常数。前馈网络采用单层结构，每个隐藏单元使用 ReLU 或 Heaviside 激活函数。

**C-RASP 语法**定义了用于语言识别的布尔与计数表达式语言，其表达能力等价于线性时序逻辑的过去算子片段 LTL[Count]：

$$
\begin{aligned}
\varphi &::= Q_a \mid \varphi \land \varphi \mid \lnot \varphi \lor \varphi \mid t \sim t \quad (\sim \in \{<,=,>\}) \\
t &::= c \mid \overleftarrow{\#}[\varphi] \mid t + t
\end{aligned}
$$

其中 $Q_a$ 为字母 $a \in \Sigma$ 的命题变量，$\overleftarrow{\#}[\varphi]$ 为计数项，表示到当前位置为止满足 $\varphi$ 的位置数量，$c \in \mathbb{N}$ 为常数。Huang et al.（2025）的定理 9 建立了 C-RASP 与极限变换器之间的模拟关系，进而与 SMAT[RPEs] 紧密关联，这构成了本工作证明链条的起点。

### 链式思考 C-RASP 程序定义器

**CoT C-RASP 表达式**将语言识别问题描述为一组带开关条件的输出令牌定义序列 $S = d_1, \ldots, d_l$，每条定义形如：

$$
O_{a_i} \gets \varphi_{a_i}
$$

其中 $O_{a_i}$ 为输出令牌 $a_i \in \Gamma$（$\Gamma$ 为 CoT 字母表），$\varphi_{a_i}$ 为 C-RASP 条件表达式。该序列实现链式思考生成：在每一步，所有满足条件的输出令牌被同时生成（并发语义），形成自回归的推理轨迹。

**可学习性保证**基于 Huang et al.（2025）的理想化学习框架：若模型在有限长度样本上精确拟合 CoT C-RASP 程序，则可在任意长度上泛化（命题 2.3），这为后续实验中的长度泛化现象提供了理论支撑。

### 计数器机模拟器

图灵完备性证明的核心策略是**放弃直接模拟图灵机，转而模拟 Minsky 计数器机**，从而绕过软最大值注意力无法精确提取读写头位址的根本障碍。模拟器通过以下两类 C-RASP 计数项追踪计数器状态：

**输入型计数器值项**（$i = 1, \ldots, n$）：

$$
t_i = \overleftarrow{\#}[Q_{a_i}] + \sum_{\rho \in \Delta} \mathbf{u}_\rho(i) \cdot \overleftarrow{\#}[Q_\rho]
$$

第一项 $\overleftarrow{\#}[Q_{a_i}]$ 给出初始字母 $a_i$ 的计数（即计数器初始值），第二项累加所有已执行转移 $\rho$ 对第 $i$ 个计数器的更新量 $\mathbf{u}_\rho(i)$，其中 $\overleftarrow{\#}[Q_\rho]$ 统计转移 $\rho$ 的历史执行次数。

**辅助型计数器值项**（$i = n+1, n+2, n+3$）：

$$
t_i = \sum_{\rho \in \Delta} \mathbf{u}_\rho(i) \cdot \overleftarrow{\#}[Q_\rho]
$$

辅助计数器无初始输入值，其状态完全由转移的累计效应决定，用于支持计数器机的通用计算。

**转移条件检查与令牌输出**通过以下规则实现：对任意满足 $\text{tgt}(\tau) = \text{src}(\tau')$ 的转移对 $\tau, \tau' \in \Delta$，添加定义：

$$
O_{\tau'} \gets \varphi_{\tau'}(t_1, \ldots, t_{n+3}) \land Q_\tau
$$

其中 $\varphi_{\tau'}$ 编码转移 $\tau'$ 的触发条件（如计数器零测试），$Q_\tau$ 确保前一步状态匹配。该构造使 C-RASP 直接模拟计数器机的状态转移，正确性由构造本身直接保证。

### 任意字母表输入编码器（Phase I）

对于任意字母表 $\Sigma$（$|\Sigma| = n$），CoT C-RASP[RPEs] 需先将输入词 $w \in \Sigma^*$ 编码为自然数向量 $\mathbf{x} \in \mathbb{N}^n$，再交由计数器机处理。

**两字母字编码函数** $\beta: \mathbb{N} \rightharpoonup \{0,1\}^*$ 将非零自然数映射为二进制词：取 $x$ 的二进制表示中最高位零之后的所有位序列：

$$
\beta(x) := \overline{b_{j-1}} \overline{b_{j-2}} \cdots \overline{b_0}, \quad j = \max\{i \mid b_i = 0\}
$$

**任意字母表编码函数** $\sigma: \mathbb{N}^n \rightharpoonup \Sigma^*$ 要求各分量编码一致且非零：

$$
\sigma(\mathbf{x}) := \mu(\beta(x_1), \ldots, \beta(x_n))
$$

其中 $\mu$ 为将 $n$ 元二进制词组映射为 $\Sigma^*$ 中词的一致性合并函数。

**RPE 关系定义**是实现 Phase I 的关键。相对位置编码关系 $\Re$ 基于 $\beta$ 定义：$(i, j) \in \Re$ 当且仅当 $i \leq j$，$i \in [1, |\beta(j)|]$，且 $\beta(j)$ 在第 $i$ 位为 1。这使得 C-RASP 能够通过 $\overleftarrow{\#}_{\Re}[\varphi]$（在 $\Re$ 关系下的受限计数）感知输入词的结构信息，逐分量构造 $\sigma$-编码。

Phase I 的核心检查逻辑包括：
- 检查当前长度是否已编码目标分量 $w_i$：$O_{\boxplus_i} \gets Q_{\boxed{i}_i} \land \overleftarrow{\#}_{\Re}[Q_{a_i}] = \overleftarrow{\#}[Q_{a_i}] \land \overleftarrow{\#}_{\Re}[\top] = \overleftarrow{\#}[Q_{a_i}]$
- 检查当前长度是否尚未完成编码：$O_{\square_i} \gets Q_{\square_i} \land (\overline{\#}_{\Re}[Q_{a_i}] \neq \overline{\#}[Q_{a_i}] \lor \overline{\#}_{\Re}[\top] \neq \overline{\#}[Q_{a_i}])$

完成 Phase I 后，Phase II 将编码向量 $\mathbf{x}$ 的各分量 $X_i$（由式 (12) 定义）替换计数器机模拟器中的初始计数项 $\overleftarrow{\#}[Q_{a_i}]$，实现对任意字母表语言的图灵完备识别。



## 实验与关键发现

### 实验设置

为验证理论构造的可学习性与长度泛化性，论文在五个算术任务上训练了小型 LLaMA 风格的解码器仅 Transformer 模型。任务涵盖加法、乘法、奇偶性判断、素数判断及整除性判断，每个任务均以一元和二进制两种表示方式编码（Table 2）。一元表示下模型不使用位置编码（NoPE），二进制表示下则分别测试带相对位置编码（Binary^R）和不带 RPE（Binary^N）两种配置。所有模型采用 ReLU 激活函数，超参数配置详见 Table 3，模型规模控制在单层至六层之间，注意力头数为一至四个。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_FdkPOHlChS/figures/003_Table_2.jpg]]

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_FdkPOHlChS/figures/005_Table_3.jpg]]
*Table 3: Hyperparameters used for training LLaMA-style decoder-only Transformers on each task, across the Unary (NoPE) and Binary ( $\mathrm { B i n a r y } ^ { \mathfrak { R } }$ with RPEs, BinaryN without RPEs) representations. All models use ReLU activations and are trained from scratch with AdamW. Weight decay is 0.01 for Prime, Exponential, and GCD; 0.05 for Division; and 0.03 for Multiplication

### 主实验结果

Table 1 汇总了五个任务在三个长度测试集上的泛化准确率。一元表示下，模型在训练长度分布内的 test0 上达到 99.9%–100% 的精确匹配准确率，在超出训练长度分布的 test1 和 test2 上同样保持接近完美的泛化性能。这一结果与理论预测一致：一元字母表上的 CoT C-RASP 具备图灵完备性，且理想化学习框架保证长度泛化。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_FdkPOHlChS/figures/002_Table_1.jpg]]
*Table 1: Generalization accuracy on three test sets (test0, test1, test2) in unary/binary*

二进制表示下的结果揭示了位置编码的关键作用。当配备 RPE 时，模型在所有任务的全部三个测试集上均达到 100% 准确率，实现了从训练长度到任意长度的完全泛化。然而，移除 RPE 后，模型在 test0 上的准确率骤降至 64.4%–95.0%，在 test1 和 test2 上更是接近 0%。这一消融结果直接验证了理论断言：无 RPE 的因果掩码 CoT C-RASP 无法处理任意字母表语言，连回文这样的简单语言都无法识别。

### 消融分析

**相对位置编码的消融**是实验中最关键的发现。无 RPE 时，二进制输入模型在超出训练长度的测试集上完全崩溃，准确率接近随机水平。这一失败模式直接对应于理论中的核心限制：纯软最大值因果注意力对序列顺序信息不敏感，无法区分同一字母在不同位置的语义。RPE 通过在注意力逻辑中引入与位置相关的偏置项，赋予模型感知序列顺序的能力，从而将图灵完备性从一元字母表扩展到任意字母表。

### 失败模式与局限

尽管实验结果与理论构造高度一致，仍需注意以下局限。首先，实验任务仅限于特定的算术语言，其链式思考轨迹由计数器机直接生成，不代表真实世界自然语言推理的分布。其次，模型规模极小（最多 6 层、4 头），在更大规模模型上的一致性需进一步验证。第三，理论构造中使用的 Heaviside 激活函数和 log n 注意力缩放是证明所需的技术条件，而实验中采用 ReLU 激活和无缩放的标准配置，泛化保证的迁移需要额外验证。最后，学习性结论依赖理想化的无限数据与精确拟合假设，实际训练中可能面临优化难度，但实验中观察到的高准确率表明这些构造在实践中是可学习的。

### 关键图表结论

- **Table 1**：一元表示下模型无需 RPE 即可实现长度泛化，二进制表示下 RPE 是实现泛化的必要条件，无 RPE 的模型在超出训练长度的测试集上完全失效。
- **Table 2**：定义了各算术任务在一元和二进制下的具体表示方式，为实验的可复现性提供了基础。
- **Table 3**：列出了每个任务下模型的超参数配置，模型规模与任务复杂度相匹配。

![[assets/figures/papers/paper_list_l9_https_openreview_net_forum_id_FdkPOHlChS/figures/004_Table_2.jpg]]
*Table 2: For each task shown in Table 2, we generate paired datasets of input strings and k-CM output traces under two encoding regimes: Unary and Binary encoding. Table 2: Unary and Binary representation of arithmetic languages. Here P is the set of prime numbers, j | i denotes divisibility, $\operatorname { g c d }$ ( i , j ) is the greatest common divisor, and i $\times$ j is multiplication



## 定位与知识库关联

### 核心瓶颈与突破路径

本工作的根本挑战在于：**软最大值（softmax）注意力无法像硬最大值（hardmax）那样精确提取图灵机读写头的位址**，使得直接模拟图灵机的经典证明策略彻底失效。这一障碍长期阻碍了软最大链式思考变换器图灵完备性的证明。

论文的关键突破在于**放弃直接模拟图灵机，转而利用 C-RASP 的计数能力模拟 Minsky 计数器机**。计数器机只需对计数器值进行增减和零值检测，不依赖对序列位置的精确索引，恰好规避了软最大注意力的根本弱点。对于任意字母表语言，进一步引入**相对位置编码（RPEs）**以赋予模型序列顺序感知能力，从而完成从一元字母表到任意语言的推广。

### 方法谱系

#### 直接前驱：硬最大注意力变换器的图灵完备性

**Hard-attention CoT Transformers**（Pérez et al., 2021; Bhattamishra et al., 2020; Merrill & Sabharwal, 2024）已通过直接模拟图灵机读写头移动被证明具备图灵完备性。然而硬最大值注意力不可微，无法通过梯度下降训练，使其理论结果与实际可训练模型之间存在鸿沟。本工作填补了这一鸿沟，证明了可训练的软最大注意力同样具备图灵完备的表达能力。

#### 表达力框架基础：C-RASP

**C-RASP**（Yang & Chiang, 2024; Huang et al., 2025）是一种用于刻画变换器表达能力的逻辑语言，等价于 LTL[Count] 的过去算子片段。无链式思考的 C-RASP 已被证明无法解决某些计数语言，而本工作将其扩展为**CoT C-RASP**——通过链式思考生成，C-RASP 的表达能力被提升至图灵完备。这一等价性（CoT C-RASP 与可学习的软最大注意力变换器在表达力上等价）是整个证明体系的理论基石。

#### 学习性保证的理论基础

本工作的学习性结论直接建立在 Huang et al.（2025）的**理想化学习框架**之上：若变换器在有限长度样本上精确拟合 CoT C-RASP 程序，则可在任意长度上实现泛化。这一保证依赖于无限数据与精确拟合的假设，实际训练中的泛化行为仍需独立验证。

### 方法的关键组件与设计取舍

| 组件 | 基线方法 | 本工作方法 | 设计理由 |
|------|---------|-----------|---------|
| 注意力机制 | 硬最大值（hardmax） | 软最大值 + $\log n$ 缩放 | 保持可微性；$\log n$ 缩放用于在无界长度上表达稀疏注意力 |
| 位置编码 | 无（仅限一元/有界字母表） | 相对位置编码（RPEs） | 赋予因果注意力顺序感知能力，是处理任意字母表的必要条件 |
| 图灵完备性证明 | 直接模拟图灵机 | 模拟 Minsky 计数器机 | 规避软最大值无法精确定位读写头的根本障碍 |
| 激活函数 | — | Heaviside / ReLU | Heaviside 为理论构造所需，实验中替换为 ReLU |

### 适用边界与局限

**1. 无 RPE 时的表达能力上限**

CoT C-RASP（以及对应的软最大 CoT 变换器）在无位置编码时**不是图灵完备的**。具体而言，连回文这样简单的语言也无法识别。这是因为纯因果软最大注意力对输入符号的**顺序信息不敏感**——它只能感知各符号的出现次数（Parikh 映射），而无法区分排列。RPEs 的引入是突破这一限制的充分条件，但**是否必要仍为开放问题**。

**2. 学习性假设的理想化性质**

长度泛化保证依赖于：（a）训练数据覆盖所有有限长度；（b）模型精确拟合目标 CoT C-RASP 程序。实际训练中，优化难度可能导致无法精确收敛，且 Heaviside 激活在实际中被替换为 ReLU，$\log n$ 缩放也未必被采用，这些差异可能影响泛化行为。

**3. 实验验证的规模限制**

实验仅在小型算术任务（一元/二进制表示的加法、乘法、奇偶性等）和小规模模型（最多 6 层、单头或少头）上进行。这些任务具有高度结构化特征，与真实世界自然语言推理的分布差异显著。在大规模自然语言场景下的实用性未经检验。

**4. 链式思考步数的复杂度刻画缺失**

构造所需的 CoT 步数与问题复杂度之间的精确关系尚未建立。当前证明仅给出存在性结论，未提供复杂度类（如时间/空间复杂度与 CoT 步数的对应关系）的精细刻画。

### 开放问题

1. **能否不借助 RPEs 实现任意字母表的图灵完备？** 是否可以通过改进链式思考策略（如让模型自行推断位置信息）或其他结构设计，使纯软最大 CoT 变换器在任意字母表上达到图灵完备？

2. **CoT 步数与计算复杂度的精确对应关系是什么？** 能否将本构造的 CoT 步数与标准复杂度类（如 PTIME、PSPACE）建立对应，从而给出变换器链式思考推理的复杂度理论？

3. **实际大模型训练中的长度泛化性能如何？** 在真实规模的变换器训练中，本理想框架所预测的长度泛化行为是否可被观察到？是否需要额外的架构改进（如特定的位置编码设计或训练策略）才能实现？

4. **激活函数与缩放因子的实际影响？** Heaviside 激活和 $\log n$ 缩放是理论构造的关键要素，在实际中分别被替换为 ReLU 和省略。这些替换对表达力和泛化性的实际影响需要系统的消融研究。



## 原文 PDF

![[paperPDFs/ICLR_2026/Softmax_Transformers_are_Turing_Complete.pdf]]
