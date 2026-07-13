---
title: "From Markov to Laplace: How Mamba In-Context Learns Markov Chains"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/From_Markov_to_Laplace_How_Mamba_In_Context_Learns_Markov_Chains.pdf
project_link: null
code_link: https://github.com/Bond1995/Markov-Mamba
openreview_forum_id: kmK3WSCOCT
aliases:
- FMLHMCLMC
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "卷积机制是Mamba实现计数与拉普拉斯平滑的关键枢纽；卷积窗口大小w决定了可建模的马尔可夫阶数（需满足w ≥ k+1），状态转移因子a_t控制信息累积与重置，是影响ICL学习能力的核心操作变量。"
primary_logic: "单层Mamba通过卷积、输入选择性与递归的精密协作，可以精确实现转移计数及加性平滑，从而匹配最优贝叶斯/极小极大估计器（拉普拉斯平滑）。简化模型MambaZero表明卷积本身即足以完成该任务，理论构造与实验高度一致，并揭示了隐藏维度随马尔可夫阶数指数增长的基本限制。"
claims:
- "单层Mamba在各类马尔可夫链上均能学习最优拉普拉斯平滑估计器，其L1距离趋近于0。"
- "卷积是Mamba成功的关键：移除卷积后模型无法学习，而仅保留卷积的MambaZero即可与完整模型匹敌。"
- "MambaZero在理论上可以精确实现一阶拉普拉斯平滑估计器（定理1），其构造与经验学习的结构一致。"
- "对于高阶马尔可夫链，任何循环架构实现拉普拉斯平滑的隐藏维度必须随阶数指数增长（Ω(2^k)）。"
---

# From Markov to Laplace: How Mamba In-Context Learns Markov Chains

> [!tip] 核心洞察
> 单层Mamba通过卷积、输入选择性与递归的精密协作，可以精确实现转移计数及加性平滑，从而匹配最优贝叶斯/极小极大估计器（拉普拉斯平滑）。简化模型MambaZero表明卷积本身即足以完成该任务，理论构造与实验高度一致，并揭示了隐藏维度随马尔可夫阶数指数增长的基本限制。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从马尔可夫到拉普拉斯：Mamba如何通过上下文学习马尔可夫链 |
| 英文题名 | From Markov to Laplace: How Mamba In-Context Learns Markov Chains |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=kmK3WSCOCT) · [GitHub](https://github.com/Bond1995/Markov-Mamba) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | MambaZero |
| Dataset | Random first-order Markov chains, WikiText-103 (14.5M parameters), WikiText-103 (110M parameters), PG-19 (200M parameters) |

> [!tip] 效果简介
> - Random first-order Markov chains 上，Prediction L1 distance from optimal Laplacian estimator 为 ≈0 (sharply matches optimal)，对比 Transformers: significantly higher distance，变化 N/A。
> - WikiText-103 (14.5M parameters) 上，Perplexity 为 27.55 (Mamba-2 full)，对比 30.68 (Mamba-2 w/o convolution)，变化 -3.13。
> - WikiText-103 (110M parameters) 上，Perplexity 为 21.38 (Mamba-2 full)，对比 21.46 (Mamba-2 w/o convolution)，变化 -0.08。

## 概要

本文研究选择性状态空间模型 Mamba 在上下文学习（ICL）中的表征能力，核心问题是：**Mamba 能否通过上下文学习马尔可夫链的最优统计估计器？其背后的机制是什么？**

在此前，Transformer 的 ICL 能力已被广泛研究，但 Mamba 类选择性 SSM 的 ICL 能力主要停留在经验观察层面，缺乏机制性理解。本文以马尔可夫链为可控测试平台，系统揭示了 Mamba 如何通过卷积、输入选择性与递归的精密协作，在上下文中隐式实现转移计数与加性平滑，从而匹配最优贝叶斯/极小极大估计器——**拉普拉斯平滑**。

核心发现可概括为三点：

1. **单层 Mamba 即可学习最优估计器**：在随机马尔可夫链上训练的单层 Mamba，其预测分布与理论最优的拉普拉斯平滑估计器高度一致，L1 距离趋近于零（Fig. 1）。

2. **卷积是关键枢纽**：消融实验表明，移除卷积后模型完全无法学习该任务；而仅保留卷积的简化模型 **MambaZero**（去除门控、ReLU 和 MLP）即可与完整 Mamba 匹敌（Fig. 3a）。这确立了卷积作为实现计数与平滑机制的核心操作变量。

3. **理论构造与经验学习一致**：作者从理论上证明，MambaZero 存在一组参数使其输出精确匹配一阶拉普拉斯平滑估计器（定理 1）；对于高阶马尔可夫链，任何循环架构实现拉普拉斯平滑所需的隐藏维度必须随阶数指数增长（定理 2），且实验验证了 $d = 2^k$ 的充分性（Fig. 6）。

在方法定位上，本文属于 Mamba ICL 能力的表征理论研究，区别于纯经验评估。其简化模型 MambaZero 剥离了门控、非线性激活和 MLP 层，仅保留卷积、状态更新和 L1 归一化预测，作为分析 Mamba 核心机制的最小完备骨架。基线对比涵盖完整 Mamba-2（Dao & Gu, 2024）、标准 Transformer（softmax attention）、线性注意力 Transformer，以及多项消融变体（去卷积、去门控、去非线性）。

在语言建模的附加实验中，卷积的贡献在 WikiText-103 上带来约 3.13 的困惑度降低（14.5M 参数），但在更大规模模型上差距缩小，表明在自然语言任务中门控等其他组件的影响更为显著。

### 上下文学习中的统计估计问题

上下文学习（In-Context Learning, ICL）是当前大语言模型的核心能力之一：模型在推理时仅通过输入序列中的上下文信息，无需参数更新即可完成预测任务。当输入序列由某个随机过程生成时，ICL本质上要求模型隐式地恢复该过程的统计规律并做出最优预测。一个自然且具有理论深度的测试平台是**马尔可夫链**——序列的下一状态仅依赖于最近的有限历史，这使得最优预测器具有闭式解，从而为严格分析模型的ICL能力提供了基准。

具体而言，对于$k$阶马尔可夫链，在狄利克雷先验下的贝叶斯最优预测器为**拉普拉斯平滑估计器**（亦称add-$\beta$估计器）：

$$\mathbb{P}_{\beta}^{(k)}(x_{t+1}=j \mid x_1^t) = \frac{n_j + \beta}{n + 2\beta}$$

其中$n_j$为当前上下文下转移至状态$j$的经验计数，$n$为总转移次数，$\beta$为平滑参数。该估计器同时具备贝叶斯最优性和极小极大最优性，是衡量模型ICL能力的黄金标准。

### 现有方法的缺口

Transformer架构在ICL任务上的理论理解已取得显著进展：已有工作表明，单层softmax注意力可以近似实现一步梯度下降，而线性注意力则能精确执行该操作。然而，对于近年来兴起的**选择性状态空间模型（SSM）**——特别是**Mamba**（Dao & Gu, 2024）——其ICL能力的理论基础几乎空白。此前的认识主要停留在经验层面：Mamba在语言建模等任务上表现优异，但其能否、以及如何通过ICL学习最优统计估计器，缺乏系统性的机理解释。

这一缺口的存在，使得研究者无法回答以下关键问题：Mamba的哪些架构组件驱动了其ICL能力？这些组件之间如何协作？是否存在根本性的表示能力限制？

### 本文的研究动机

本文旨在填补上述理论空白，核心动机包括：

1. **表征能力视角**：从表示论的角度出发，系统刻画Mamba在马尔可夫过程上的ICL能力，而非仅依赖经验观察。
2. **组件归因**：识别Mamba架构中驱动ICL的关键组件——初步证据表明，卷积机制可能扮演比门控和非线性激活更核心的角色。
3. **理论-经验对齐**：通过构造性证明和受控实验，建立Mamba内部表示与最优统计估计器之间的精确对应关系，并揭示其基本限制（如隐藏维度随马尔可夫阶数的指数增长）。

通过将Mamba置于马尔可夫-ICL框架下进行严格分析，本文不仅为选择性SSM的ICL能力提供了首个完整的理论解释，也为理解卷积、选择性与递归在现代序列模型中的协同机制提供了新的视角。

## 核心方法与创新机理

本文的核心创新在于首次从表示能力的角度，系统性地揭示了选择性状态空间模型（Mamba）在上下文学习（ICL）中学习最优统计估计器的理论机制。此前的理解主要停留在经验层面，而本文通过理论构造与实验验证，明确了Mamba实现马尔可夫链上下文学习的关键驱动因素。

### 关键洞察：卷积—选择性—递归的精密协作

论文的核心洞察是：单层Mamba通过**卷积（局部上下文提取）**、**输入选择性（动态门控）**与**递归状态更新（全局信息累积）**三者的精密协作，可以精确实现转移计数及加性平滑，从而匹配最优贝叶斯/极小极大估计器——拉普拉斯平滑。这一机制被凝练为简化模型**MambaZero**，并获得了严格的理论支持（定理1）。

### 相对基线模型的关键架构创新（Changed Slots）

为隔离核心机制，MambaZero相对于完整Mamba-2架构进行了如下关键简化：

| 组件 | 完整Mamba-2（基线） | MambaZero（本文） | 依据 |
|------|---------------------|-------------------|------|
| **MLP层** | 存在 | 移除 | Sec. 4.1 |
| **Input selectivity中的ReLU** | 存在 | 移除 | Sec. 4.1 |
| **门控机制（Gating）** | 存在（$z_t$门控调制） | 移除 | Sec. 4.1 |
| **预测归一化** | Softmax | L1归一化 | Sec. 4.1 |

这些简化表明：在上述马尔可夫上下文学习任务中，**MLP、ReLU非线性、门控机制均非必要组件**。MambaZero仅保留Embedding层、卷积操作（Input selectivity内部）和线性投影层，即可在理论上精确实现一阶拉普拉斯平滑估计器（定理1），且实验表现与完整Mamba-2模型匹敌（Fig. 3a）。

### 因果操纵变量：卷积窗口与状态转移因子

论文识别出两个直接影响Mamba上下文学习能力的核心操作变量：

1. **卷积窗口大小 $w$**：卷积是Mamba实现计数与拉普拉斯平滑的关键枢纽。实验表明，学习 $k$ 阶马尔可夫链需要满足 $w \ge k+1$（Fig. 3b）。移除卷积后，单层Mamba无论宽度多大均无法学会最优估计器（Table 3），而仅保留卷积的MambaZero即可成功。

2. **状态转移因子 $a_t$**：该因子控制历史信息的累积与重置。在标准马尔可夫链上，模型收敛后 $a_t \approx 1$，允许累积全部历史转移计数（Fig. 4）；在切换马尔可夫过程中，模型学习在切换令牌处将 $a_t$ 设为0，实现计数的精确重置（Fig. 13），展现出选择性机制在非平稳场景下的自适应能力。

### 理论贡献：表示能力的上下界

除架构简化外，本文的理论贡献还包括对循环架构表示能力的下界刻画：**任何循环架构实现 $\varepsilon$-近似的 $k$ 阶拉普拉斯平滑，其隐藏维度必须满足 $d \cdot \mathsf{p} \ge 2^k (1-3\varepsilon) \log(1/\varepsilon)$**（定理2），其中 $\mathsf{p}$ 为比特精度。这意味着隐藏维度随马尔可夫阶数呈指数增长是循环架构的基本限制，而非Mamba特有的缺陷。实验验证了 $d = 2^k$ 的充分性（Fig. 6），与理论下界在指数依赖性上一致。

### 卷积作为跨架构的关键组件

值得关注的是，卷积的关键作用并非Mamba独有。实验表明，对标准Transformer的K、Q、V矩阵添加卷积后，单层Transformer也能成功学习马尔可夫任务（Fig. 11），而无卷积的Mamba则需要两层才能解决同一任务（Fig. 12）。这表明**卷积所提供的局部时序上下文提取能力，是实现此类上下文学习任务的通用关键机制**，而非特定于SSM架构。

本文构建了一个从理论构造到经验验证的完整研究管线，旨在揭示Mamba架构在上下文学习（ICL）中学习马尔可夫链最优估计器的内在机制。整体框架围绕三个层次展开：**问题形式化**、**模型解剖与简化**、**表征能力证明与验证**。

### 问题建模与最优目标

研究将Mamba的ICL能力置于**马尔可夫上下文学习（Markov-ICL）**框架下进行考察。核心设定如下：

- **数据生成**：序列 $x_1, x_2, \dots, x_T$ 从一个随机采样的 $k$ 阶马尔可夫链中生成。转移核本身服从狄利克雷先验，因此最优预测器并非简单的经验频率，而是**拉普拉斯平滑（add-β）估计器**：

  $$\mathbb{P}_{\beta}^{(k)}(x_{t+1}=j \mid x_1^t) = \frac{n_j + \beta}{n + 2\beta}$$

  其中 $n_j$ 为从当前上下文转移到状态 $j$ 的经验计数，$n$ 为总计数，$\beta$ 为先验强度参数。

- **训练目标**：模型在随机采样的马尔可夫链序列上以标准的下一词预测交叉熵损失进行训练：

  $$L(\theta) = -\frac{1}{T}\sum_t \mathbb{E}_{P} \mathbb{E}_{x \sim P} \log f_\theta^{(x_{t+1})}(x_1^t)$$

- **评估标准**：以模型预测分布与拉普拉斯平滑估计器之间的L1距离或KL散度作为核心度量，判断模型是否学会了最优的上下文内统计估计。

### Mamba架构的层级管线

完整的Mamba语言模型由以下模块串联构成，形成从离散符号到下一词概率的端到端映射：

```
x_t ∈ {0,1} → Embedding → x_t → Mamba → u_t → MLP → v_t → Linear → logit_t → Prediction → f_θ(x_1^t)
```

各模块的功能与信息流如下：

1. **Embedding**：将离散词元 $x_t$ 映射为 $d$ 维连续向量 $x_t = e_{x_t}$。

2. **Mamba块**：核心序列变换模块，实现序列到序列的映射 $\text{Mamba}: \mathbb{R}^{d \times T} \to \mathbb{R}^{d \times T}$。其内部包含三个关键子机制：
   - **卷积（Input selectivity）**：对输入 $x_t$ 施加局部时间卷积，生成上下文感知的表示 $\widetilde{x}_t$、输入门 $b_t$ 和输出门 $c_t$。卷积窗口大小 $w$ 决定了模型能捕获的局部上下文跨度。
   - **状态更新**：通过线性递归维护隐状态 $H_t$，实现跨时间步的信息累积：
     $$H_t = a_t H_{t-1} + \widetilde{x}_t b_t^{\intercal} \in \mathbb{R}^{ed \times N}$$
     其中 $a_t = \exp(-a \cdot \Delta_t) \in (0, 1)$ 为输入依赖的衰减因子，控制历史信息的遗忘速率。
   - **状态投影**：从当前隐状态读取相关信息：
     $$y_t = H_t c_t \in \mathbb{R}^{ed}$$

3. **MLP**：门控前馈网络，对Mamba输出 $u_t$ 进行非线性变换，增强表示能力。在完整Mamba中，输出还经过门控调制：
   $$z_t = y_t \odot \text{ReLU}(W_z x_t), \quad o_t = W_o z_t$$

4. **Linear**：线性投影层，将 $d$ 维表示映射到词表大小 $S$ 的logits空间。

5. **Prediction**：通过softmax（或L1归一化）将logits转换为下一词的概率分布 $f_\theta(x_1^t)$。

### 简化模型MambaZero：剥离冗余，聚焦本质

为隔离出驱动ICL的核心机制，研究提出了**MambaZero**——一个仅保留最精简组件的简化模型。其与完整Mamba的差异体现在四个关键槽位上：

| 组件 | 完整Mamba | MambaZero | 依据 |
|------|-----------|-----------|------|
| MLP层 | 存在 | 移除 | Sec. 4.1 |
| Input selectivity中的ReLU | 存在 | 移除 | Sec. 4.1 |
| 门控机制 | 存在 | 移除 | Sec. 4.1 |
| 预测归一化 | Softmax | L1归一化 | Sec. 4.1 |

MambaZero的完整前向定义为：

$$x_t = e_{x_t}, \quad u_t = x_t + \text{MambaZero}(x_1^t), \quad \text{logit}_t = W_\ell u_t, \quad f_\theta(x_1^t) = \text{logit}_t / \|\text{logit}_t\|_1$$

这一简化使得模型仅保留**Embedding → 卷积 → 线性投影 → L1归一化**的核心管线，为后续的理论构造（定理1）提供了干净的数学框架。

### 因果枢纽与核心发现

贯穿整个框架的核心洞察是：**卷积机制是Mamba实现计数与拉普拉斯平滑的关键枢纽**。具体而言：

- **卷积窗口 $w$** 决定了可建模的马尔可夫阶数，需满足 $w \geq k+1$（图3b）。
- **状态转移因子 $a_t$** 控制信息累积与重置：当 $a_t \approx 1$ 时，隐状态累积全部历史转移计数；当 $a_t \approx 0$ 时，模型主动遗忘历史（如在切换马尔可夫过程中重置计数，图13）。
- **输入选择性与递归的协作**：卷积提取局部上下文特征，递归在隐状态中累积转移计数，最终通过内积 $b^{(ij)\top} c_t$ 的自动正交化实现仅相关计数的选择性读取（图5）。

这一框架将Mamba的ICL能力归结为一个可证明的构造：单层Mamba通过上述机制的精密协作，可以精确实现转移计数及加性平滑，从而匹配最优贝叶斯/极小极大估计器。同时，定理2揭示了这一能力的基本限制——对于 $k$ 阶马尔可夫链，任何循环架构实现拉普拉斯平滑所需的隐藏维度必须满足 $d \cdot \mathsf{p} \geq 2^k (1-3\varepsilon) \log(1/\varepsilon)$，即随阶数指数增长。

### 关键架构模块

Mamba语言模型由以下核心模块串联构成（图2）：

1. **Embedding**：将离散token映射为连续嵌入向量 $x_t \in \mathbb{R}^d$。
2. **Mamba块**：对嵌入序列执行序列到序列映射 $\text{Mamba}: \mathbb{R}^{d \times T} \to \mathbb{R}^{d \times T}$，是模型的核心计算单元。
3. **MLP**：门控前馈变换（仅完整Mamba中存在）。
4. **Linear**：将隐藏表示投影到词表维度的logits。
5. **Prediction**：将logits转化为下一token概率分布（完整Mamba使用softmax，MambaZero使用L1归一化）。

其中，Mamba块内部包含三个关键子模块：

- **Input selectivity（含卷积）**：从输入 $x_t$ 生成 $\widetilde{x}_t, b_t, c_t$ 及状态转移因子 $a_t$。卷积在此处提取局部时序上下文，是Mamba实现计数与拉普拉斯平滑的核心枢纽。
- **State update**：通过线性递归 $H_t = a_t H_{t-1} + \widetilde{x}_t b_t^\top$ 聚合历史信息，$a_t \triangleq \exp(-a \cdot \Delta_t) \in (0,1)$ 控制信息衰减。
- **State projection**：通过 $y_t = H_t c_t$ 读取当前状态中的相关信息。

### 核心公式与机制

**Mamba状态更新与推理**

状态更新公式为：

$$H_t = a_t H_{t-1} + \widetilde{x}_t b_t^\top \in \mathbb{R}^{ed \times N}$$

其中 $a_t$ 是输入依赖的衰减因子，$\widetilde{x}_t$ 是经卷积处理后的输入表示，$b_t$ 是输入选择性生成的向量。状态投影与输出为：

$$y_t = H_t c_t, \quad z_t = y_t \odot \text{ReLU}(W_z x_t), \quad o_t = W_o z_t$$

**MambaZero简化架构**

为隔离核心机制，MambaZero移除了MLP层、ReLU非线性和门控机制，仅保留Embedding、卷积和Linear层，并将Prediction中的softmax替换为L1归一化：

$$x_t = e_{x_t}, \quad u_t = x_t + \text{MambaZero}(x_1^t), \quad \text{logit}_t = W_\ell u_t, \quad f_\theta(x_1^t) = \text{logit}_t / \|\text{logit}_t\|_1$$

**MambaZero输出分解**

展开状态更新递归，MambaZero块输出可分解为初始项与所有转移计数的加权和：

$$o_t = W_o \widetilde{x}_0 b_0^\top c_t + \sum_{ij} n_{ij} W_o \widetilde{x}^{(ij)} b^{(ij)\top} c_t$$

其中 $n_{ij}$ 为从状态 $i$ 转移到状态 $j$ 的累计次数。实验表明，在收敛时 $b^{(ij)\top} c_t \approx 0$ 对于 $i \neq x_t$，因此只有与当前上下文相关的计数被保留（图5a）。最终logits可表达为：

$$\text{logit}_t = W_\ell x_t + W_\ell W_o \widetilde{x}_0 b_0^\top c_t + \sum_j n_{x_t,j} W_\ell W_o \widetilde{x}^{(x_t,j)} b^{(x_t,j)\top} c_t$$

这一分解揭示了Mamba如何通过线性递归实现精确的转移计数，进而匹配加性平滑估计器。

**最优估计器：拉普拉斯平滑**

在狄利克雷先验下的贝叶斯最优预测器为拉普拉斯平滑（add-$\beta$估计器）：

$$\mathbb{P}_{\beta}^{(k)}(x_{t+1}=j \mid x_1^t) = \frac{n_j + \beta}{n + 2\beta}$$

其中 $n_j$ 是当前上下文中转移到状态 $j$ 的次数，$n$ 是总转移次数，$\beta$ 是平滑参数（当 $\beta=1$ 时即为拉普拉斯平滑）。

**训练目标**

模型通过最小化下一token预测的期望交叉熵损失进行训练：

$$L(\theta) = -\frac{1}{T}\sum_t \mathbb{E}_{P} \mathbb{E}_{x \sim P} \log f_\theta^{(x_{t+1})}(x_1^t)$$

### 关键操作变量

- **卷积窗口大小 $w$**：决定了可建模的马尔可夫阶数。实验与理论一致表明，学习 $k$ 阶马尔可夫链需要 $w \geq k+1$（图3b）。
- **状态转移因子 $a_t$**：控制历史信息的累积与重置。在标准马尔可夫任务中，收敛时 $a_t \approx 1$（图4），允许累积全部历史计数；在切换马尔可夫过程中，模型学习在切换token处设 $a_t = 0$ 以重置计数（图13）。
- **隐藏维度 $d$**：对于 $k$ 阶马尔可夫链，任何循环架构实现 $\varepsilon$ 近似的拉普拉斯平滑所需隐藏维度与精度的乘积下界为 $d \cdot p \ge 2^k (1-3\varepsilon) \log(1/\varepsilon)$（定理2），揭示了维度随阶数指数增长的基本限制。

## 实验与关键发现

### 核心发现：单层Mamba学习最优拉普拉斯估计器

在随机一阶马尔可夫链上训练的**单层**Mamba，能够精确匹配最优的加性平滑（add-β）估计器——即拉普拉斯平滑（Laplacian smoothing），该估计器在狄利克雷先验下既是贝叶斯最优的，也是极小极大最优的。Fig. 1(a)展示了模型在固定测试序列上的预测概率分布，与最优估计器几乎完全重合；Fig. 1(b)则从L1距离角度量化了这一结论：对于不同阶数的马尔可夫链，单层Mamba与最优估计器之间的L1偏差趋近于零，而作为对比的Transformer（softmax attention）和线性注意力Transformer的偏差显著更高（Fig. 7、Fig. 10）。这一结果表明，Mamba在上下文学习（ICL）中对马尔可夫结构的捕捉能力具有坚实的统计基础。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_kmK3WSCOCT/figures/001_Figure_1.jpg]]
*Figure 1: Single-layer Mamba learns the optimal Laplacian estimator when trained on random Markov chains, exhibiting ICL. (a) shows the predicted probability distribution on a fixed test sequence for models trained on binary first-order Markov sources. (b) quantifies the L _ { 1 } deviation from the optimal estimator for random sequences and various Markov orders. The error intervals show the standard deviation across 5 runs. Sec. 4.3 and Fig. 10 further discuss Mamba vs. Transformers*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_kmK3WSCOCT/figures/008_Figure_7.jpg]]
*Figure 7: Comparison of predicted probability and test loss between a 1-layer Mamba and the other baselines, including linear attention. Mamba outperforms all baselines. Linear attention and softmax attention Transformers perform similarly*

### 消融实验：卷积是核心驱动因素

为定位Mamba成功学习拉普拉斯平滑的关键组件，论文进行了系统的消融实验（Fig. 3a）：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_kmK3WSCOCT/figures/003_Figure_3.jpg]]
*Figure 3: (a) illustrates the fundamental role of convolution, without which the model fails to learn the task. In contrast, a simplified variant with just the convolution (MambaZero) matches the performance of the full model. (b) highlights the relation between the Markov order k and the window size w of Mamba. It is required that w $\geq$ k + 1 for the model to learn the order-k prediction task*

- **去除卷积（Mamba-2 w/o convolution）**：模型完全无法学习任务，测试损失与最优估计器的差距始终很大。
- **仅保留卷积的简化模型MambaZero**：其性能与完整Mamba-2模型几乎一致，成功学习到最优估计器。
- **去除门控（Mamba-2 w/o gating）**：对学习能力的影响相对较小。
- **去除非线性激活（Mamba-2 w/o non-linearities）**：影响同样有限。

这一消融链条清晰地表明：**卷积机制是Mamba实现转移计数和拉普拉斯平滑的关键枢纽**，其重要性远超门控和非线性激活。

进一步地，卷积窗口大小 $w$ 与可建模的马尔可夫阶数 $k$ 之间存在明确的约束关系：**$w \ge k+1$ 是模型学习 $k$ 阶马尔可夫预测任务的必要条件**。Fig. 3b 验证了这一关系——当窗口大小不足时，模型无法收敛到最优估计器。

### 参数收敛行为的实证验证

训练收敛后，MambaZero的参数呈现出与理论构造高度一致的模式：

- **状态转移因子 $a_t$**：对于所有 $t \ge 1$，$a_t$ 收敛到 $\approx 1$（Fig. 4）。这意味着模型选择**不衰减**历史信息，使隐状态 $H_t$ 能够累积全部历史转移计数，这是实现拉普拉斯平滑的必要条件。
- **计数相关内积的正交性**：参数满足 $b^{(ij)\top} c_t \approx 0$ 当 $i \neq x_t$（Fig. 5a）。即只有与当前上下文相关的转移计数的内积为非零，其他计数被自动屏蔽，确保模型仅使用正确的条件计数进行预测。
- **计数无关向量的收敛**：与计数无关的向量分量收敛到与 $\beta=1$ 对应的最优值（Fig. 5b），实现了精确的加性平滑。


### 自然语言任务中的验证

在WikiText-103语言建模任务上，卷积的作用同样得到验证，但影响程度随模型规模变化（Table 1 / Table 4 / Table 5）：

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_kmK3WSCOCT/figures/004_Table_1.jpg]]
*Table 1: Perplexity results on the WikiText-103 dataset*

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_kmK3WSCOCT/figures/019_Table_4.jpg]]
*Table 4: Perplexity results on the WikiText-103 dataset*

- **14.5M参数规模**：完整Mamba-2的困惑度为27.55，而去除卷积后升至30.68（差距-3.13），卷积的贡献显著。
- **110M参数规模**：完整Mamba-2为21.38，去除卷积后为21.46（差距仅-0.08），卷积的作用明显减弱。
- **PG-19（200M参数）**：完整Mamba-2为14.16，去除卷积后为14.28（差距-0.12）。

这一趋势表明：在小规模模型中，卷积是性能的关键支撑；而在大规模、深层模型中，门控等其他组件的贡献上升，卷积的相对重要性下降。这与合成马尔可夫任务中卷积的绝对核心地位形成对比，揭示了自然语言任务的复杂性需要多组件协同。

### 失败模式与架构限制

**单层无卷积Mamba的失败**：无论隐藏维度如何增大，单层无卷积的Mamba均无法学会最优估计器（Table 3）。这与Transformer的行为类似——无卷积的Transformer同样需要至少两层才能解决马尔可夫预测任务（Fig. 12）。然而，向Transformer的K、Q、V矩阵添加卷积后，单层即可成功学习（Fig. 11），进一步印证了卷积在时序计数中的普适价值。

![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_kmK3WSCOCT/figures/017_Table_3.jpg]]
*Table 3: Experiments on one-layer Mamba without convolution, with varying width. The model does not learn the optimal estimator successfully*

**隐藏维度的指数下界**：对于 $k$ 阶马尔可夫链，任何循环架构（包括Mamba）实现 $\varepsilon$-近似的拉普拉斯平滑，其隐藏维度 $d$ 与精度 $p$ 的乘积必须满足 $d \cdot p \ge 2^k (1-3\varepsilon) \log(1/\varepsilon)$（Theorem 2）。Fig. 6 的实验验证了 $d = 2^k$ 的充分性，与理论下界一致。这意味着高阶马尔可夫建模对模型容量存在根本性的指数级需求。

### 选择性机制：切换马尔可夫过程

在切换马尔可夫过程（switching Markov process）的实验中，Mamba展现了其选择性机制的实际效用。最优策略要求在切换令牌处重置历史计数，而Mamba通过学习在切换令牌处将 $a_t$ 设为零来实现这一点（Fig. 13），在其他位置则保持 $a_t \approx 1$。这直接体现了状态转移因子 $a_t$ 作为“信息流控制阀门”的功能：通过选择性地遗忘过去信息，Mamba能够适应非平稳的序列分布。

## 定位与知识库关联

### 1. 与基线方法的关系

本研究在“上下文学习（ICL）能否匹配最优统计估计器”这一理论问题下，将Mamba架构置于与Transformer家族的直接比较之中。核心基线包括：

- **标准Softmax注意力Transformer**：作为ICL研究的经典参照系，单层Transformer在随机马尔可夫链上无法学习最优拉普拉斯平滑估计器，其预测概率与最优估计器之间存在显著L1距离（Fig. 1）。即使增加层数，Transformer的测试损失缺口仍系统性地大于Mamba（Fig. 10）。

- **线性注意力Transformer**：作为另一类高效序列模型，线性注意力Transformer在马尔可夫ICL任务上的表现与标准Softmax注意力Transformer相似，均无法匹敌Mamba（Fig. 7）。

- **Mamba-2（完整版）**（Dao & Gu, 2024）：本研究以Mamba-2为完整模型基线，在合成马尔可夫链和WikiText-103语言建模任务上均进行了对比。在WikiText-103上，14.5M参数的Mamba-2困惑度为27.55，显著优于去除卷积的变体（30.68）（Table 1 / Table 4）。

- **Mamba-2消融变体**：通过系统移除Mamba-2的组件，本研究明确了各组件的相对重要性。去除卷积的Mamba-2完全无法学习马尔可夫任务（Fig. 3a）；去除门控（状态转移因子$a_t$）或非线性激活（ReLU）的变体虽性能有所下降，但影响远小于卷积的移除（Table 4）。

值得注意的是，本研究进一步发现：**向Transformer的K、Q、V矩阵添加卷积**，可以使其在单层下成功学习马尔可夫任务（Fig. 11）。这一跨架构的迁移证据强烈暗示，卷积所赋予的局部时序上下文提取能力，而非Mamba特有的选择性状态空间机制，才是实现计数型统计估计的关键要素。

### 2. 方法适用边界

本研究的理论构造与经验发现基于以下明确边界：

**适用场景**：
- **有限状态马尔可夫过程**：理论分析（定理1）精确适用于状态空间大小为$S$的任意一阶马尔可夫链，且经验上推广至高阶马尔可夫链（Fig. 3b, Fig. 6）。
- **单层或浅层架构**：MambaZero的构造性证明针对单层模型；经验上，增加层数对Mamba在马尔可夫任务上的性能提升有限（Fig. 9b, Fig. 10），表明单层已具备足够的表示能力。
- **加性平滑估计器**：Mamba学习到的估计器精确匹配拉普拉斯平滑（$\beta=1$的add-$\beta$估计器），这是狄利克雷先验下的贝叶斯最优解。

**不适用或受限场景**：
- **深层架构的理论推广**：当前理论分析严格限于单层MambaZero；深层Mamba中卷积、门控、非线性与跨层信息流动的协同机制仍缺乏形式化理解。
- **自然语言任务的机制归因**：在WikiText-103上，卷积的作用随模型规模增大而减弱——110M参数时去除卷积仅导致困惑度从21.38升至21.46，200M参数时在PG-19上从14.16升至14.28（Table 5）。这表明在复杂语言建模中，门控等其他组件的作用可能更为显著，合成任务上的发现不能简单外推。
- **非马尔可夫过程**：论文未涉及隐马尔可夫模型、长程记忆过程或非平稳序列的ICL能力分析。

### 3. 局限与开放问题

**已识别的局限**：

1. **理论深度受限**：定理1的构造依赖于特定的维度选择（$d=2S$，$N=S$，$e=1$）和精确的参数化，与实际训练中模型自主学习到的内部表示可能不完全一致。定理2虽给出了隐藏维度下界$d \cdot \mathsf{p} \ge 2^k (1-3\varepsilon) \log(1/\varepsilon)$，但该下界针对的是一般循环架构，且证明依赖于表示精度的比特数假设。

2. **任务覆盖狭窄**：绝大多数实验在合成的随机马尔可夫链上进行；自然语言实验仅作为辅助验证，且卷积的作用在语言任务中相对较弱。

3. **学习动力学缺失**：论文仅证明了MambaZero在表示能力上可以精确实现拉普拉斯平滑，但梯度下降训练如何收敛到该解的动力学过程（收敛速率、相变行为、损失景观结构）未被分析。

**开放问题**：

- **深层推广**：如何将单层MambaZero的表示理论扩展到多层Mamba？层间交互是否允许建模更复杂的统计估计器？
- **更一般的序列模型**：Mamba能否学习隐马尔可夫模型、非马尔可夫过程或具有层次结构序列的最优上下文估计器？
- **学习动力学**：Mamba收敛到拉普拉斯平滑估计器的具体动力学是什么？是否存在从计数到平滑的阶段性转变？
- **门控与选择性的协同**：在语言任务中，门控（$a_t$）和选择性机制如何与卷积协同工作？切换马尔可夫实验（Fig. 13）已初步展示了$a_t$在重置计数中的作用，但其在自然文本中的功能仍待探索。
- **架构设计的可迁移性**：向Transformer添加卷积即可使其获得类似Mamba的马尔可夫ICL能力（Fig. 11），这是否意味着卷积可以作为通用的“计数归纳偏置”模块嵌入各类序列架构？

## 原文 PDF

![[paperPDFs/ICLR_2026/From_Markov_to_Laplace_How_Mamba_In_Context_Learns_Markov_Chains.pdf]]
