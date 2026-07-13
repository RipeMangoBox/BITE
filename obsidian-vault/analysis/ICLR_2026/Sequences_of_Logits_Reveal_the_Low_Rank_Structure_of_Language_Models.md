---
title: "Sequences of Logits Reveal the Low Rank Structure of Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Sequences_of_Logits_Reveal_the_Low_Rank_Structure_of_Language_Models.pdf
project_link: null
code_link: null
openreview_forum_id: gdZ6J5hZzF
aliases:
- LLG
- SLRLRSLM
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "扩展对数概率矩阵（extended logit matrix）的近似低秩性质。"
primary_logic: "现代语言模型在将历史（history）和未来（future）扩展为序列矩阵时，其对数概率矩阵展现出近似低秩结构，该低秩性不仅可用于通过线性组合无关提示进行生成（LINGEN），而且与输入切换仿射网络（ISAN）等价，从而为学习与表示提供理论支撑。"
claims:
- "扩展对数概率矩阵对于多种现代LLM均表现出近似低秩，奇异值衰减遵循幂律，指数α>1/2确保常秩近似。"
- "基于低秩结构的线性生成方法（LINGEN）能够仅使用非目标提示的线性组合生成目标提示的合理延续，其KL散度显著低于单token基线等强基线。"
- "扩展对数概率矩阵的低秩性与时间变化ISAN的等价性建立了生成模型的理论基础，并提供了可证明的学习算法（在logit查询模型下）。"
- "OLMo-1b, wiki 数据集构造的提示集 (Option 1) 上 KL divergence between LINGEN and true model = LINGEN"
---

# Sequences of Logits Reveal the Low Rank Structure of Language Models

> [!tip] 核心洞察
> 现代语言模型在将历史（history）和未来（future）扩展为序列矩阵时，其对数概率矩阵展现出近似低秩结构，该低秩性不仅可用于通过线性组合无关提示进行生成（LINGEN），而且与输入切换仿射网络（ISAN）等价，从而为学习与表示提供理论支撑。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 对数概率矩阵序列揭示语言模型的低秩结构 |
| 英文题名 | Sequences of Logits Reveal the Low Rank Structure of Language Models |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=gdZ6J5hZzF) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | LINGEN (Linear Generation) |
| Dataset | OLMo-1b, wiki 数据集构造的提示集 (Option 1), 使用无意义futures的分布外设置 (Option 2) |

> [!tip] 效果简介
> - OLMo-1b, wiki 数据集构造的提示集 (Option 1) 上，KL divergence between LINGEN and true model 为 LINGEN，对比 Single-token baseline，变化 LINGEN 的总KL散度在所有生成步数（15步）上显著低于所有基线（示例：在后期步数从约0.15降至远低于基线的水平）。
> - OLMo-1b, 使用无意义futures的分布外设置 (Option 2) 上，KL divergence 为 LINGEN，对比 Single-token baseline and other methods，变化 LINGEN 的KL散度虽然大于原位设置，但仍小于所有基线。

## 概要

**问题瓶颈**：当前大规模语言模型（LLM）在行为预测与理论保证方面面临一个根本性困难——我们缺乏一个简单、通用且不依赖具体架构的数学抽象来刻画其内在结构。这导致对模型输出行为的理解、控制与可证明分析长期受限。

**核心洞见**：本文发现，现代自回归语言模型的对数概率矩阵（logit matrix）在将历史（history）和未来（future）序列扩展为矩阵形式后，呈现出**近似低秩结构**。具体而言，扩展对数概率矩阵的奇异值遵循幂律衰减，指数 $\alpha > 1/2$ 保证了常秩近似的可行性。这一低秩性不仅意味着不同提示（prompt）在模型内部的表示存在强线性依赖，更揭示了一个生成机制：**可以通过对一组无关提示的 logits 进行线性组合，来生成目标提示的合理延续**，而无需直接查询目标提示的后续 logits（LINGEN 方法）。

**方法与理论定位**：本文的方法论贡献包含三个层次：
1. **结构发现**：定义扩展对数概率矩阵 $\mathcal{L}_M(\mathcal{H}, \mathcal{F})$，并通过奇异值衰减与平均 KL 散度系统验证其低秩性在多种现代 LLM（OLMo、Gemma、LLaMA、Mamba 等）上普遍成立。
2. **生成算法**：基于低秩性提出 LINGEN（Linear Generation）——通过线性回归求解系数向量 $v$，然后逐步加权组合历史提示的 logits 进行采样生成。该方法在分布内和分布外（使用无意义 future）设置下均显著优于单 token 基线等强基线。
3. **理论等价性**：证明扩展对数概率矩阵的低秩性与**时间变化输入切换仿射网络（time-varying ISAN）**等价（Theorem 4.3），从而为语言模型的学习与表示提供了可证明的理论基础，并在 logit 查询模型下给出了可证明的学习算法（Theorem 4.4）。

**主要实证结果**：
- **低秩近似**：OLMo-7b 的扩展对数概率矩阵在秩 5–500 范围内，平均 KL 散度随秩增加呈幂律下降（Figure 1a）；该性质在预训练早期迅速涌现，KL 散度在训练初期急剧下降后缓慢回升至最终值（Figure 3）。
- **生成性能**：LINGEN 在 OLMo-1b 上 15 步生成的总 KL 散度显著低于所有基线，包括单 token 基线和中间训练检查点模型（Figure 6）。即便使用无意义 future 构造回归矩阵（Option 2），LINGEN 的 KL 散度仍低于所有基线（Figure 1b）。
- **跨模型迁移**：不同模型的对数概率矩阵列空间之间的主角度显示大量重叠，表明历史之间的线性关系在不同模型间可迁移（Figure 12）。

**局限与开放问题**：理论泛化界（如 Lemma D.18）依赖强假设且不紧凑，难以直接应用；LINGEN 需要大量模型查询以构建回归矩阵，可能被滥用于绕过安全过滤器；低秩观察基于有限子集，尚未对全序列空间提供严格近似保证；此外，低秩性质随序列长度增长的变化、与标准解码策略的直接比较等问题仍有待探索。

大规模语言模型（LLM）已展现出令人瞩目的生成与推理能力，然而我们对这些模型内部工作机制的理解仍然相当有限。当前研究面临一个核心瓶颈：**缺乏简单、通用的数学抽象来刻画语言模型内在的低维结构**，这使得我们难以对模型行为做出可测试的预测，更无法提供可证明的理论保证。

现有的大多数分析方法往往依赖于特定的架构细节（如 Transformer 的注意力机制或状态空间模型的状态转移），这限制了其普适性。本文试图绕开架构细节，将语言模型视为一个**从序列到序列的顺序概率映射**，从而在统一的视角下研究其结构特性。

本文的核心动机源于一个关键观察：**现代语言模型的扩展对数概率矩阵（extended logit matrix）展现出近似低秩性质**。具体而言，当我们将一组历史序列 $\mathcal{H}$ 和未来序列 $\mathcal{F}$ 构造为矩阵时，该矩阵的奇异值呈现幂律衰减（幂律指数 $\alpha > 1/2$），意味着可以用常秩矩阵对其进行良好近似（Figure 1a, Figure 2）。这一低秩结构并非训练初始即存在，而是在预训练早期迅速涌现（Figure 3），且在不同模型（OLMo、Gemma、LLaMA、Mamba）和不同数据集（wiki、arxiv、c4 等）间表现出一致性（Figure 7, Figure 9）。

这一发现暗示了一个深刻的理论可能性：如果对数概率矩阵是低秩的，那么**语言模型的输出可以用一组基函数的线性组合来表示**。换句话说，存在特征映射 $\phi(h)$ 和 $\psi(f)$，使得给定历史 $h$ 下未来 $f$ 的对数概率近似为内积形式：

$$\log \Pr_M[f \mid h] \approx \langle \phi(h), \psi(f) \rangle$$

基于这一洞察，本文提出了 **LINGEN（Linear Generation）** 方法：仅通过查询模型在一组与目标提示无关（甚至无意义）的提示上的输出，利用线性回归求解组合系数，即可生成目标提示的合理延续（Figure 1b, Figure 5）。这一方法不仅在分布内设置下显著优于单 token 基线，在分布外（使用无意义 future）设置下同样保持优势（Figure 6, Figure 1b）。

此外，本文进一步建立了低秩结构与**输入切换仿射网络（ISAN）**之间的理论等价性（Theorem 4.3），表明语言模型等价于一个隐藏维度为 $d$ 的时间变化 ISAN 当且仅当所有时间步的扩展对数概率矩阵的秩不超过 $d$。这为语言模型的学习与表示提供了可证明的理论支撑，并在 logit 查询模型下给出了可证明的学习算法（Theorem 4.4）。

综上，本文的动机在于：**通过对数概率矩阵的低秩结构，为语言模型建立一个架构无关的数学框架，从而实现对模型行为的可预测操控和理论理解**。

## 核心方法与创新机理

本文的核心创新在于将语言模型的对数概率输出重新组织为**扩展对数概率矩阵**（extended logit matrix），并发现该矩阵在现代大语言模型中展现出**近似低秩结构**。这一发现并非对模型架构的修改，而是对模型行为的数学抽象，其关键突破体现在以下两个层面。

### 1. 从模型输出到低秩矩阵的抽象

传统上，语言模型被视为从历史序列到下一个token分布的映射。本文的**关键概念创新**在于将这一映射扩展为矩阵形式：行索引为历史序列 $h$，列索引为“未来序列 $f$ 与目标token $z$”的笛卡尔积，矩阵条目为均值中心化后的对数概率：

$$\mathcal{L}_M(\mathcal{H}, \mathcal{F})_{(h, (f, z))} := L_M[z \mid h \circ f]$$

这一构造的威力在于，它将模型对任意历史-未来组合的完整行为编码为一个线性代数对象。实验证据表明，对于OLMo、Gemma、LLaMA、Mamba等多种模型，该矩阵的奇异值衰减遵循**幂律**，且指数 $\alpha > 1/2$（如OLMo-7b的 $\alpha \approx 0.536$），这意味着存在常秩近似——这是低秩可近似性的理论相变条件（Figure 2, Figure 7）。

### 2. 低秩结构的生成应用：LINGEN

基于上述发现，本文提出了**LINGEN**（Linear Generation）——一种利用低秩结构进行文本生成的机制。其核心changed slot如下表所示：

| 机制环节 | 基线做法 | LINGEN做法 |
|---------|---------|-----------|
| 生成机制 | 直接计算目标提示的logits并自回归采样 | 通过对一组**无关历史提示**的logits进行线性回归得到系数 $v$，然后逐步使用 $v$ 加权组合这些历史提示的logits来生成，无需查询目标提示的后续logits |

LINGEN的采样过程可形式化为：

$$z_t \sim \mathsf{softmax}\left( \sum_{h \in \mathcal{H}} v_h \cdot L_{h,t} \right)$$

其中系数 $v$ 通过将目标提示的logit行向量对其他历史提示的行向量进行回归得到。这意味着**模型从未见过目标提示的后续token分布**，却能够生成合理的延续文本。

实验表明，LINGEN在15步生成过程中的总KL散度显著低于所有基线，包括单token基线（仅使用空future的logits）和中间训练检查点模型（Figure 6, Figure 1b）。即使在**分布外**设置下（使用无意义futures构造回归矩阵），LINGEN的KL散度仍低于所有基线（Figure 1b）。

### 3. 理论等价性：低秩与ISAN

本文的另一核心创新是建立了**低秩结构与输入切换仿射网络（ISAN）之间的等价性**。定理4.3表明，一个语言模型等价于隐藏维度为 $d$ 的时间变化ISAN，当且仅当所有时间步的扩展对数概率矩阵的秩不超过 $d$：

$$\mathrm{Rank}(\mathcal{L}_M(\Sigma^t, \Sigma^{\leq T-t})) \leq d \quad \forall t \leq T$$

这一等价性为语言模型的学习提供了可证明的算法（在logit查询模型下），将经验观察到的低秩性质与序列模型的表达能力建立了理论桥梁。

### 4. 创新边界与局限

需注意，LINGEN的生成质量尚未与标准解码策略（如温度采样、束搜索）进行直接比较，其实用性有待验证。理论泛化界（如Lemma D.18）依赖强假设且不紧凑，难以直接指导实践。此外，低秩结构的观察基于有限的历史/未来子集，尚未对全序列空间提供严格的近似保证。

本文提出了一套与架构无关的分析框架，将任意语言模型视为从序列到序列的序贯概率映射，并通过**扩展对数概率矩阵**（extended logit matrix）揭示其内在的低维结构。整个工作流程由三个核心模块构成，形成“观测—利用—理论解释”的完整闭环。

### 模块一：扩展对数概率矩阵构造

该模块是整个框架的数据基础。给定一个语言模型 $M$，从数据集中采样一组历史序列 $\mathcal{H}$ 和未来序列 $\mathcal{F}$，对每个 $(h, f)$ 对，查询模型在拼接序列 $h \circ f$ 下的对数概率分布，并构造均值中心化的对数概率矩阵 $\mathcal{L}_M(\mathcal{H}, \mathcal{F})$。矩阵的行索引为历史 $h$，列索引为未来-词元对 $(f, z)$，条目为：

$$\mathcal{L}_M(\mathcal{H}, \mathcal{F})_{(h, (f, z))} := L_M[z \mid h \circ f]$$

其中 $L_M[z \mid \cdot]$ 为均值中心化对数概率（Definition 2.1），即每个词元的对数概率减去词汇表上的平均对数概率。这一中心化操作消除了词频先验的干扰，使矩阵的代数结构更纯粹地反映模型对序列关系的编码。

在实际计算中，为控制矩阵规模，对每个未来 $f$ 仅保留其 $k$ 个最可能后续词元对应的列，得到子矩阵 $\mathcal{L}_{M,k}(\mathcal{H}, \mathcal{F})$（Section 3.1）。该子矩阵是后续所有低秩分析及线性生成（LINGEN）的输入。

### 模块二：系数回归与线性生成（LINGEN）

基于模块一构造的矩阵，框架进一步利用其近似低秩性质实现**无需查询目标提示的生成**。具体流程如 Figure 5 所示：

1. **系数回归**：将目标历史 $h_{\text{targ}}$ 对应的行向量 $\mathcal{L}_M(\{h_{\text{targ}}\}, \mathcal{F})$ 作为响应变量，将其他历史集合 $\mathcal{H}$ 对应的行向量作为回归量，求解线性系数 $v \in \mathbb{R}^{|\mathcal{H}|}$，使得 $\sum_{h \in \mathcal{H}} v_h \cdot \mathcal{L}_M(\{h\}, \mathcal{F})$ 逼近目标行向量（Section 3.3）。

2. **逐步加权采样**：在生成的第 $t$ 步，对每个历史 $h \in \mathcal{H}$ 查询当前部分序列下的对数概率向量 $L_{h,t}$，以系数 $v$ 加权组合后通过 softmax 采样下一个词元：

$$z_t \sim \mathsf{softmax}\left( \sum_{h \in \mathcal{H}} v_h \cdot L_{h,t} \right)$$

这一过程完全避免了对目标提示 $h_{\text{targ}}$ 的后续对数概率查询——所有查询仅针对 $\mathcal{H}$ 中的历史进行。当 $\mathcal{H}$ 由与目标无关甚至无意义的提示构成时，LINGEN 仍能生成合理延续（Figure 1b, Table 2-3）。

### 模块三：理论等价性建立

框架的理论支柱是扩展对数概率矩阵的低秩性与**时间变化输入切换仿射网络**（time-varying ISAN）之间的等价性（Theorem 4.3）。ISAN 的状态更新与输出分别为：

$$x_t = A_{z_t, t} \, x_{t-1}, \quad z_t \sim \mathsf{softmax}(B_t \, x_{t-1})$$

其中隐藏维度 $d$ 控制模型容量。该等价性表明：语言模型等价于隐藏维度为 $d$ 的 ISAN，当且仅当所有时间步的扩展对数概率矩阵的秩不超过 $d$。这一定理将经验观测到的低秩现象提升为生成模型的理论基础，并暗示了在 logit 查询模型下存在可证明的学习算法（Theorem 4.4）。

### 输入输出流总结

```
输入: 语言模型 M, 历史集 H, 未来集 F, 目标历史 h_targ
     ↓
模块一: 构造 L_{M,k}(H, F)  [查询 M 的 logits]
     ↓
模块二: 回归得到系数 v → 逐步加权采样生成  [仅查询 H 的 logits]
     ↓
输出: 目标历史的生成延续
     ↓
模块三: 低秩性 ↔ ISAN 等价性  [理论保证]
```

三个模块之间的因果关系清晰：模块一观测到的近似低秩性（奇异值幂律衰减，$\alpha > 1/2$）是模块二可行的必要条件；模块三则为这种可行性提供了严格的数学解释。整个框架不依赖任何特定的模型架构，仅通过 logit 查询接口即可运作，具有广泛的适用性。

### 均值中心化对数概率

语言模型在给定上下文 $y_{1:t}$ 时，对每个token $z$ 输出原始logit。为消除词汇表整体偏移的影响，定义均值中心化对数概率（Mean-Centered Logits），将每个token的对数概率减去词汇表上的平均对数概率：

$$L_M[z \mid y_{1:t}] = \log \Pr_M[z \mid y_{1:t}] - \frac{1}{|\Sigma|} \sum_{z' \in \Sigma} \log \Pr_M[z' \mid y_{1:t}]$$

其中 $\Sigma$ 为词汇表，$\Pr_M[z \mid y_{1:t}]$ 为模型 $M$ 在给定上下文下的token概率。该中心化操作是后续矩阵构造的基础（Definition 2.1）。

### 扩展对数概率矩阵

将历史序列集合 $\mathcal{H}$ 与未来序列集合 $\mathcal{F}$ 进行笛卡尔积扩展，构造扩展对数概率矩阵（Extended Logit Matrix）。矩阵的行由历史 $h \in \mathcal{H}$ 索引，列由未来 $f \in \mathcal{F}$ 与token $z \in \Sigma$ 的配对 $(f, z)$ 索引：

$$\mathcal{L}_M(\mathcal{H}, \mathcal{F})_{(h, (f, z))} := L_M[z \mid h \circ f]$$

其中 $h \circ f$ 表示历史与未来的拼接。该矩阵的每一行对应一个特定历史下、所有未来序列中每个token的均值中心化对数概率（Definition 2.2）。

### 对数条件概率的链式分解

未来序列 $f = z_1, z_2, \ldots, z_t$ 在给定历史 $h$ 下的对数条件概率，可通过逐token对数条件概率之和计算：

$$\log \Pr[f \mid h] = \log \Pr[z_t \mid h \circ z_{1:t-1}] + \cdots + \log \Pr[z_1 \mid h]$$

这一分解使得扩展对数概率矩阵的行向量能够线性表示完整未来序列的对数概率，为低秩结构下的线性生成提供基础（Section 2）。

### 平均KL散度与Frobenius界

为量化低秩近似的质量，定义平均KL散度（Average KL Divergence），在全体历史-未来对上衡量真实对数概率矩阵 $L$ 与近似矩阵 $A$ 在下一token分布上的差异：

$$D_{\mathsf{KL}}^{\mathsf{avg}}(L, A) = \frac{1}{|\mathcal{H}| |\mathcal{F}|} \sum_{h \in \mathcal{H}, f \in \mathcal{F}} D_{\mathsf{KL}}(\mathsf{softmax}(L_{h,f}) \parallel \mathsf{softmax}(A_{h,f}))$$

该散度可由矩阵差的Frobenius范数平方控制（Fact B.2）：

$$D_{\mathsf{KL}}^{\mathsf{avg}}(\mathcal{L}_M(\mathcal{H}, \mathcal{F}), A) \leq \frac{1}{|\mathcal{H}| \cdot |\mathcal{F}|} \cdot \| \mathcal{L}_M(\mathcal{H}, \mathcal{F}) - A \|_F^2$$

这一不等式为通过低秩近似减小KL散度提供了理论依据：若能用低秩矩阵充分逼近扩展对数概率矩阵，则下一token分布的近似误差也随之受控（Definition 3.1）。

### LINGEN采样机制

LINGEN（Linear Generation）的核心操作为：在第 $t$ 步生成时，使用预先回归得到的系数向量 $v$，对历史集合 $\mathcal{H}$ 中所有历史在当前部分序列下的对数概率向量 $L_{h,t}$ 进行线性组合，再通过softmax采样下一个token：

$$z_t \sim \mathsf{softmax}\left( \sum_{h \in \mathcal{H}} v_h \cdot L_{h,t} \right)$$

系数 $v$ 通过将目标历史的扩展对数概率行向量作为响应、其他历史的行向量作为回归量进行线性回归得到。整个过程无需查询模型在目标历史上的后续logits（Section 3.3, Algorithm 1）。

### 时间变化ISAN的等价性

扩展对数概率矩阵的低秩性与时间变化输入切换仿射网络（Time-varying Input-Switched Affine Network, ISAN）存在理论等价关系。ISAN的隐藏状态更新由当前token $z_t$ 决定状态转移矩阵 $A_{z_t, t}$：

$$x_t = A_{z_t, t} x_{t-1}$$

下一token的分布由上一隐藏状态通过线性投影 $B_t$ 并经softmax得到：

$$z_t \sim \mathsf{softmax}(B_t x_{t-1})$$

核心等价定理（Theorem 4.3）指出：语言模型等价于一个隐藏维度为 $d$ 的时间变化ISAN，当且仅当对所有时间步 $t \leq T$，扩展对数概率矩阵的秩不超过 $d$：

$$\mathrm{Rank}(\mathcal{L}_M(\Sigma^t, \Sigma^{\leq T-t})) \leq d \quad \forall t \leq T$$

该等价性将语言模型的低秩结构从经验观察提升为表示学习的理论基础（Section 4.1）。

## 实验与关键发现

### 核心发现：对数概率矩阵的近似低秩结构

本文的核心实验围绕一个关键观察展开：现代语言模型的扩展对数概率矩阵（extended logit matrix）展现出近似低秩结构。这一性质在多个维度上得到了系统验证。

**奇异值衰减与幂律行为。** 对OLMo-7b模型构造的对数概率矩阵 $\mathcal{L}_M(\mathcal{H}, \mathcal{F})$ 进行奇异值分解，结果显示奇异值遵循近似幂律衰减（Figure 2），幂律指数 $\alpha \approx 0.536$。这一数值具有理论意义：当 $\alpha > 1/2$ 时，矩阵可以用常秩近似来捕捉其主要结构，这是后续LINGEN方法可行的数学基础。该幂律行为在多个模型（OLMo-1b、Gemma、LLaMA、Mamba等）上一致出现（Figure 7），且在不同数据集（wiki、arxiv、c4、math、starcoder）上也保持稳定（Figure 9），表明低秩性并非特定模型或数据分布的偶然产物。

**KL散度度量的低秩近似质量。** 除奇异值外，论文采用平均KL散度 $D_{\mathsf{KL}}^{\mathsf{avg}}$ 直接衡量低秩近似矩阵与真实对数概率矩阵在下一次token分布上的差异（Definition 3.1）。该度量有Frobenius范数上界保证：
$$D_{\mathsf{KL}}^{\mathsf{avg}}(\mathcal{L}_M(\mathcal{H}, \mathcal{F}), A) \leq \frac{1}{|\mathcal{H}| \cdot |\mathcal{F}|} \cdot \| \mathcal{L}_M(\mathcal{H}, \mathcal{F}) - A \|_F^2$$
实验表明，随着近似秩增加，平均KL散度同样呈现幂律下降（Figure 1a, Figure 8），与奇异值衰减行为一致。这一结果为后续通过低秩结构进行生成提供了直接的误差控制依据。

**预训练过程中低秩结构的涌现。** Figure 3揭示了低秩性质的时间演化规律：在OLMo-1b的Stage-1预训练初期，低秩近似的KL散度急剧下降，表明模型迅速习得低维表示结构；随后KL散度缓慢回升至最终值。这一“先降后升”的模式暗示低秩结构是早期预训练的关键产物，可能对应模型对语言统计规律的压缩编码。值得注意的是，未训练模型（Step 0）的奇异值衰减指数 $\alpha \approx 0.374$（Figure 7d），不满足 $\alpha > 1/2$ 的条件，说明低秩结构确实来自训练过程而非架构的固有偏置。

**跨模型与跨futures的结构共享。** 实验进一步检验了低秩结构的泛化性。通过比较真实futures与随机置换tokens构造的“无意义futures”（nonsense futures）下低秩近似的列空间主角度，发现两者存在大量重叠（Figure 4，大量主角度余弦值接近1）。这意味着历史之间的线性关系并不依赖于futures的语义合理性，而是嵌入在模型的深层表示中。更令人惊讶的是，不同模型（如OLMo、Gemma、LLaMA）的对数概率矩阵列空间之间也存在显著的主角度重叠（Figure 12），暗示跨模型的表示迁移潜力。

### LINGEN：基于低秩结构的线性生成

基于上述低秩性质，论文提出了LINGEN（Linear Generation）方法，其核心流程包含三个模块：

1. **扩展对数概率矩阵构造**：从数据集采样历史集合 $\mathcal{H}$ 和未来集合 $\mathcal{F}$，构建对数概率子矩阵 $\mathcal{L}_M(\mathcal{H}, \mathcal{F})$ 作为回归数据。
2. **系数回归**：将目标提示的行向量 $\mathcal{L}_M(\{h_{\text{targ}}\}, \mathcal{F})$ 作为响应，其他历史提示的行向量作为回归量，求解线性系数 $v$。
3. **逐步加权采样**：在每一步生成时，使用 $v$ 对历史提示在当前部分序列下的logits进行线性组合，通过softmax采样下一个token：
   $$z_t \sim \mathsf{softmax}\left( \sum_{h \in \mathcal{H}} v_h \cdot L_{h,t} \right)$$

该方法的核心优势在于：生成过程中**无需查询目标提示的后续logits**，仅依赖无关历史提示的logits线性组合。

**主实验结果。** 在OLMo-1b上，使用wiki数据集构造的提示集（Option 1），LINGEN在15步生成过程中的总KL散度显著低于所有基线（Figure 6）。特别值得注意的是与单token基线（single-token baseline）的对比：该基线仅使用空future（即单步logits）进行线性组合，在第一步表现尚可，但随后KL散度迅速上升，而LINGEN通过利用完整的多步futures信息，在整个生成过程中保持了较低的KL散度。Table 2的生成示例进一步佐证了这一点：LINGEN的生成文本能够合理利用提示中的上下文信息，而单token基线的生成在初始token之后往往偏离主题。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_gdZ6J5hZzF/figures/046_Table_2.jpg]]
*Table 2: Sample generations from LINGEN (Option 1) and single-token baseline. Prompts are shown in gray and italicized, and continuations are shown in black. Samples were not cherry-picked, i.e., the first generation from each prompt was selected. The generations from LINGEN (left) all read well and make clear use of context in the prompt; in contrast, while generations from LINGEN with the single-token logit matrix (right) typically are reasonable for the first token or few, they become derailed soon thereafter*

**分布外设置的鲁棒性。** 在使用无意义futures的Option 2设置下（Figure 1b），LINGEN的KL散度虽高于原位设置，但仍优于所有基线方法。Table 3的生成示例显示，尽管并非所有生成都是目标提示的自然延续，但大多数生成仍能明显利用提示中的信息。这表明低秩结构对futures的语义扰动具有一定鲁棒性。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_gdZ6J5hZzF/figures/047_Table_3.jpg]]
*Table 3: Sample generations from LINGEN and single-token baseline with Hnonsense (i.e., Option 2), for the same 5 target prompts as in Table 2. Prompts are shown in gray and italicized, while LINGEN’s generations are in black. While not all of the generations are natural continuations of the target prompt, most of the generations show clear use of information from the prompt*

### 消融实验与稳健性分析

**子矩阵构造方式的消融。** 为验证低秩性质不依赖于特定的子矩阵构造方式，论文测试了两种替代方案：使用 $k=200$ 个最可能token构造的 $\mathcal{L}_{M,200}(\mathcal{H}, \mathcal{H})$，以及随机抽取50个token构造的 $\tilde{\mathcal{L}}_{M,50}(\mathcal{H}, \mathcal{F})$（Figure 11）。两种方案均展现出类似的低秩近似能力，且幂律指数接近（$\alpha \approx 0.543, 0.527$），表明低秩性质对子矩阵的构造方式不敏感。

**训练中间检查点基线。** 为排除LINGEN的优势来自“使用了更成熟模型”的可能，实验将预训练中间检查点的模型作为生成基线（Figure 1b）。结果显示LINGEN的性能优于这些中间检查点模型，说明低秩结构的利用确实提供了超越模型成熟度的增益。

### 失败模式与局限性

尽管实验结果整体积极，但仍存在若干值得注意的局限：

1. **理论界的实用性不足**：理论泛化界（如Lemma D.18）严重依赖假设且不紧凑，难以直接指导实际应用中的参数选择。
2. **查询成本与安全风险**：LINGEN需要大量查询模型以构建回归矩阵，这一过程可能被滥用于绕过安全过滤器（如通过拆分目标提示来规避内容审核）。
3. **有限子集的近似保证**：低秩结构的观察基于有限的历史/未来子集，尚未对全序列空间提供严格的近似保证。随着序列长度增长，低秩性质的变化规律未被系统研究。
4. **解码策略的缺失比较**：生成质量尚未与标准解码策略（如温度采样、束搜索）进行直接比较，LINGEN在实际应用中的相对优势有待验证。
5. **长文本生成一致性**：论文未讨论超长文本生成场景下低秩结构的保持性，以及LINGEN在长序列上的生成一致性。

### 重要图表结论速览

| 图表 | 核心结论 |
|------|----------|
| Figure 1a | 扩展对数概率矩阵的低秩近似误差（平均KL散度）随秩增加呈幂律衰减 |
| Figure 1b | LINGEN在分布外设置下的KL散度仍优于所有基线 |
| Figure 2 | OLMo-7b奇异值衰减遵循幂律，$\alpha \approx 0.536 > 1/2$，保证常秩近似 |
| Figure 3 | 低秩结构在预训练早期迅速涌现，KL散度先急剧下降后缓慢回升 |
| Figure 4 | 真实futures与无意义futures的列空间主角度大量重叠，低秩结构不依赖语义合理性 |
| Figure 6 | LINGEN在15步生成中KL散度显著低于单token基线等强基线 |
| Figure 7 | 多个不同模型均展现一致的奇异值幂律衰减 |
| Figure 9-10 | 低秩性质在不同数据集上保持稳定 |
| Figure 11 | 不同子矩阵构造方式（top-k token、随机token）均保持低秩近似能力 |
| Figure 12 | 不同模型间的列空间存在显著主角度重叠，暗示跨模型表示迁移 |
| Table 2 | LINGEN生成文本合理利用上下文，单token基线生成后期偏离主题 |

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_gdZ6J5hZzF/figures/045_Table_1.jpg]]
*Table 1: For 10 values of h $\in \mathcal$ H (left column) we display the history $h ^ { \prime } \in \mathcal { H } , h ^ { \prime } \ne$ h minimizing the distance between the respective rows of the logits matrix, i.e., \| $\dot { \mathcal { L } _ { M } } ( \{$ h $\} , \mathcal { F }$ ) - $\dot { \mathcal { L } } _ { M } ( \{ h ^ { \prime } \} , \mathcal { F }$ ) \|$_ { 2 } ^ { \infty }$ . Examples were not cherry-picked (they correspond to the first 10 examples in the set H described in Section 3.1, as obtained from wiki)

## 定位与知识库关联

### 核心机制与理论等价性

本文的核心贡献在于揭示了现代语言模型的一个通用数学结构：**扩展对数概率矩阵（extended logit matrix）的近似低秩性质**。这一性质并非特定架构的产物，而是将语言模型视为从序列到序列的序贯概率映射后涌现的统计规律。具体而言，对于历史集合 $\mathcal{H}$ 和未来集合 $\mathcal{F}$，矩阵 $\mathcal{L}_M(\mathcal{H}, \mathcal{F})$ 的奇异值遵循幂律衰减，指数 $\alpha > 1/2$ 确保了常秩近似的可行性（Figure 2, Figure 7）。该低秩性在预训练早期迅速出现（Figure 3），且在不同模型（OLMo、Gemma、LLaMA、Mamba）和不同数据集（wiki、arxiv、c4、math、starcoder）间一致存在（Figure 7-10），表明它是一种与架构和领域无关的深层表征特性。

理论层面，本文建立了低秩结构与**时间变化输入切换仿射网络（time-varying Input-Switched Affine Network, ISAN）**的等价性（Theorem 4.3）：语言模型等价于隐藏维度为 $d$ 的时间变化 ISAN，当且仅当所有时间步的扩展对数概率矩阵的秩不超过 $d$。这一等价性为语言模型的表示学习提供了可证明的理论基础，并在 logit 查询模型下给出了可证明的学习算法（Theorem 4.4）。

### 提出方法：LINGEN

基于低秩结构，本文提出了 **LINGEN（Linear Generation）** 生成方法。其核心流程分为三步：

1. **扩展对数概率矩阵构造**：从数据集采样历史集合 $\mathcal{H}$ 和未来集合 $\mathcal{F}$，构建对数概率子矩阵，为回归提供数据。
2. **系数回归**：将目标提示的行向量作为响应，其他历史提示的行向量作为回归量，求解线性系数向量 $v$。
3. **逐步加权采样**：在每一步生成时，使用 $v$ 对历史提示在当前部分序列下的 logits 进行线性组合，并通过 softmax 采样下一个 token：
   $$z_t \sim \mathsf{softmax}\left( \sum_{h \in \mathcal{H}} v_h \cdot L_{h,t} \right)$$

LINGEN 的关键特性在于：**生成过程完全不需要查询目标提示的后续 logits**，仅依赖无关历史提示的线性组合即可产生目标提示的合理延续。

### 与基线方法的关系

本文的基线设计服务于不同层次的比较目的：

- **Single-token baseline**：仅使用空 future（即单步 logits）进行线性组合生成。该方法可视为“软最大瓶颈”（soft max-bottleneck）方法，仅能捕获单步信息，无法建模多步依赖。实验表明，该方法在首个 token 表现尚可，但随后 KL 散度急剧上升（Figure 6），从反面验证了扩展对数概率矩阵中多步 future 信息对低秩结构的必要性。

- **Intermediate training checkpoint**：使用预训练中间检查点的模型作为生成基线。该基线旨在衡量 LINGEN 相对于不成熟模型的优势——即使模型尚未充分训练，LINGEN 仍能通过线性组合提取有效的生成能力，其 KL 散度显著低于中间检查点模型的直接生成。

- **Random (untrained) model**：作为低秩结构的反例。未训练模型（OLMo-1b step 0）的奇异值衰减指数 $\alpha \approx 0.374$（Figure 7d），远低于 $1/2$ 的相变阈值，不具备一致的幂律衰减，从而证明低秩结构是预训练过程中涌现的产物，而非架构的固有偏置。

### 适用边界与局限

尽管低秩结构展现出跨模型、跨数据集的稳健性，本文的方法和结论存在以下明确边界：

1. **理论泛化界的实用性有限**：主要理论结果（如 Lemma D.18）给出的 KL 散度界严重依赖假设且不紧凑，难以直接指导实际部署中的超参数选择或性能预测。

2. **LINGEN 的查询成本与安全风险**：LINGEN 需要大量查询模型以构建回归矩阵，这在计算上是昂贵的。更值得关注的是，该方法可能被滥用于绕过安全过滤器——攻击者可通过拆分目标提示，利用无关提示的线性组合生成不安全回复，而无需直接查询敏感内容。本文明确将此列为开放安全问题。

3. **低秩近似的有限样本保证缺失**：当前的低秩结构观察基于有限的历史/未来子集（如 $|\mathcal{H}|=|\mathcal{F}|=50$），尚未对全序列空间提供严格的近似保证。尽管消融实验（Figure 11）表明使用 $k=200$ 最可能 token 或随机抽取 50 个 token 构造的子矩阵同样展示低秩近似能力，但扩展到更大规模时的行为仍需进一步验证。

4. **生成质量评估的局限性**：LINGEN 的生成质量主要通过 KL 散度与真实模型分布进行比较，尚未与标准解码策略（如温度采样、束搜索）进行直接对比。Table 2 和 Table 3 的生成示例虽展示了合理的延续能力，但其在开放域生成任务中的实际应用性有待系统评估。

5. **序列长度依赖性未探索**：论文未讨论序列长度增长时低秩性质的变化趋势，以及超长文本生成中 LINGEN 的一致性问题。

### 开放问题

本文在讨论中明确提出了若干待探索的方向：

- **训练动力学诊断**：能否更好地理解训练过程中奇异值衰减的演化，并将其用作训练进度的诊断工具？
- **模型无关的可解释性**：能否在历史表示空间 $\phi(h)$ 中提取概念与特征，从而实现跨模型的可解释性？
- **安全攻击与防御**：LINGEN 或其变体是否能够通过拆分目标提示来绕过安全防护？该框架是否暗示了针对此类攻击的防御技术？
- **近似低秩的理论扩展**：能否将理论结果扩展到近似低秩情形，并确定哪些近似度量（如全变差 vs 矩阵范数）在理论上可行且贴近实践？
- **架构偏置的起源**：为什么未训练的模型（如 OLMo-1b step 0）也显示出比随机子空间稍多的列空间重叠（Figure 12）？这是否源于架构的归纳偏置？

## 原文 PDF

![[paperPDFs/ICLR_2026/Sequences_of_Logits_Reveal_the_Low_Rank_Structure_of_Language_Models.pdf]]
