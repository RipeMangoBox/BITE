---
title: "Adaptive Thinking: Large Language Models Know When to Think in Latent Space"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Adaptive_Thinking_Large_Language_Models_Know_When_to_Think_in_Latent_Space.pdf
project_link: null
code_link: null
openreview_forum_id: 2i6Rp0gCq6
aliases:
- SSCGATA
- ATLLMKWTLS
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "自一致性（self-consistency）作为推理必要性的代理信号，可从查询在最后一层的隐藏表示中预测，进而动态分配思考预算。"
primary_logic: "通过离线训练轻量级适配器，从查询的最后一层隐藏表示预测自一致性分数，在推理时根据预测分数自适应决定是否启用思考，实现计算最优推理，且适配器具有跨任务泛化能力。"
claims:
- "低自一致性表明查询需要扩展思维链推理，高自一致性则表明可直接回答。"
- "自一致性模式在深层隐藏表示中高度可区分，尤其最后一层区分度最强。"
- "Sonata 适配器在维持准确率的同时，将思考 token 消耗降低 20% 至 60%。"
- "Sonata 适配器仅增加 <1‰ 的推理计算开销，并可与现有思维链压缩方法兼容。"
---

# Adaptive Thinking: Large Language Models Know When to Think in Latent Space

> [!tip] 核心洞察
> 通过离线训练轻量级适配器，从查询的最后一层隐藏表示预测自一致性分数，在推理时根据预测分数自适应决定是否启用思考，实现计算最优推理，且适配器具有跨任务泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 自适应思考：大语言模型知道何时在潜在空间中进行思考 |
| 英文题名 | Adaptive Thinking: Large Language Models Know When to Think in Latent Space |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=2i6Rp0gCq6) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Sonata (Self-Consistency-Guided Adapter for Thinking Allocation) |
| Dataset | AIME25, MATH-500, GSM8K, GPQA |

> [!tip] 效果简介
> - AIME25 上，Accuracy (↑) / #Tokens (↓) 为 63.3% / 16449，对比 60.0% / 16995，变化 Acc +3.3%, Tokens -3.2%。
> - MATH-500 上，Accuracy (↑) / #Tokens (↓) 为 97.4% / 3694，对比 97.6% / 4900，变化 Acc ~, Tokens -24.6%。
> - GSM8K 上，Accuracy (↑) / #Tokens (↓) 为 95.6% / 890，对比 95.2% / 1994，变化 Acc +0.4%, Tokens -55.4%。

## 概要

大语言模型（LLM）的推理能力因思维链（chain-of-thought, CoT）而显著提升，但现有方法对所有查询分配**固定的思考预算**，导致简单查询浪费计算资源，而复杂查询计算不足——这是本工作的核心瓶颈。为解决这一问题，本文提出 **Sonata（Self-Consistency-Guided Adapter for Thinking Allocation）**，一种轻量级自适应推理框架。

Sonata 的核心洞察是：**自一致性（self-consistency）可作为推理必要性的可靠代理信号**。具体而言，查询在非思考模式下多次采样的答案一致性越高，说明模型对该查询的掌握越牢固，启用思维链推理的边际收益越小；反之，低自一致性则表明模型需要扩展推理。这一负相关关系在 MATH-500 数据集上得到验证（Figure 2），并且自一致性模式在深层隐藏表示中高度可区分，尤其最后一层区分度最强（Figure 3）。

基于此，Sonata 采用**离线训练、在线决策**的两阶段策略：
- **离线阶段**：从校准数据集的查询中提取 LLM 最后一层最后一个 token 的隐藏表征，训练一个两层 MLP 适配器（仅约 262K 参数）预测自一致性分数。
- **在线阶段**：在预填充完成后，适配器根据查询的隐藏表征预测自一致性分数 $\hat{s}$，并与预设阈值 $\tau_0$ 比较——若 $\hat{s} > \tau_0$，则跳过思考直接生成答案；否则启用默认思考过程。

实验覆盖 Qwen3-8B、Qwen3-32B 等多个模型，在 AIME25、MATH-500、GSM8K、GPQA 等基准上，Sonata 在**维持甚至略升准确率**（平均 +1.4%）的同时，将思考 token 消耗降低 **20% 至 60%**（Table 1）。适配器仅引入 **< 1‰ 的推理计算开销**，且可与现有思维链压缩方法（如 REFRAIN）兼容叠加（Table 6）。消融实验进一步表明，自一致性作为代理指标显著优于基于熵的指标（如 LM logits entropy 和 attention entropy），且仅需 100 个校准样本即可保持稳定性能。

Sonata 的局限在于：思考决策为生成前的**二值判断**，无法在推理过程中动态调整深度；阈值 $\tau_0$ 通过网格搜索经验设定，缺乏自动优化机制；校准数据依赖正确答案标注。尽管如此，该方法为计算最优推理提供了简洁有效的范式，其跨任务泛化能力和极低开销使其具备较强的实用价值。



### 固定思考预算的困境

具备推理能力的大语言模型在数学、科学和代码等复杂任务上展现了强大的思维链推理能力。然而，当前主流方法对所有查询分配**固定的思考预算**——例如预设统一的思考 token 数，达到预算时插入终止 token 强制结束推理。这种“一刀切”的策略造成了根本性的效率瓶颈：简单查询被强制消耗不必要的计算资源，而真正困难的查询却可能因预算不足而无法充分推理。

以 Qwen3-8B 在 MATH-500 上的表现为例，不同难度级别的查询对思考的需求差异显著。**Figure 1** 展示了自一致性（self-consistency）随题目难度等级变化的趋势——难度越高，模型在无思考模式下多次采样的答案一致性越低，这暗示着模型对困难问题缺乏稳定的推理能力。

### 核心洞察：自一致性作为推理必要性的代理信号

论文的核心发现是：**自一致性可以作为查询是否需要扩展思维链推理的可靠代理信号**。具体而言，在非思考模式下，模型对同一查询进行多次独立采样，其答案的一致性程度与开启思考后的性能增益之间存在**强负相关关系**。

如 **Figure 2** 所示，在 MATH-500 的五个难度级别上，每个查询点在无思考模式下的自一致性分数（x 轴，$N=32$ 次采样）与启用思考后的准确率提升（y 轴）呈现明显的负相关：自一致性低的查询从思考中获益最大，而自一致性高的查询几乎不需要额外推理即可正确回答。这一关系揭示了查询级推理必要性的内在规律——模型在浅层推理中反复出错的查询，恰恰是最需要深度思考的查询。

### 潜在空间中的可区分性

进一步的潜在空间分析表明，自一致性模式在深层隐藏表示中**高度可区分**。**Figure 3** 通过 PCA 可视化了不同 Transformer 层的查询隐藏表征，按自一致性分数着色。在 MATH-500（数学推理）和 GPQA（科学推理）两个基准上，自一致性模式在深层（如第 36、64 层）展现出最显著的分离：高自一致性查询形成紧密的聚类，而低自一致性查询则更加分散。

这一发现具有重要的工程意义：**无需实际执行多次采样**，仅从查询在预填充阶段的最后一层隐藏表示中，就可以预测其自一致性分数，从而在生成前判断是否需要启用思考。

### 现有方法的缺口

与固定预算策略相对，另一种直观的思路是让模型**自判断**是否需要思考——先让 LLM 自行判断查询难度，再决定是否启用思考模式。然而，这种自判断方法存在两个根本缺陷：（1）判断本身消耗额外的推理 token，抵消了部分效率收益；（2）模型的自我评估能力有限，难以准确估计自身的推理需求。

因此，研究缺口在于：**如何在不增加显著计算开销的前提下，准确预测每个查询的推理必要性，从而实现查询级的自适应思考预算分配？**

### 本文动机

基于上述观察，论文提出 Sonata（**S**elf-C**o**nsistency-Guided Adapter for Thi**n**king **A**lloca**t**ion），一个轻量级适配器框架，核心思路是：

1. **离线阶段**：利用校准数据集预先计算每个查询的自一致性标签（正确答案比例），训练一个轻量级 MLP 适配器，从查询的最后一层隐藏表示预测自一致性分数。
2. **推理阶段**：在预填充完成后，适配器以极低开销（<1‰ 推理计算量）预测查询的自一致性分数，根据预设阈值动态决定是否启用思考——高自一致性查询直接生成答案，低自一致性查询进入完整的思维链推理。

这一设计的核心优势在于：将推理必要性的判断从“生成后评估”或“模型内省”转化为“生成前预测”，从根本上避免了不必要的 token 消耗，同时保持了与现有思维链压缩方法的兼容性。



## 核心方法与创新机理

Sonata 的核心创新在于将**思考预算分配**从一个粗粒度的全局策略转变为一个**查询级自适应决策问题**，并通过一个极轻量的机制实现。

### 问题诊断：固定预算的“一刀切”困境

现有的推理模型（如 DeepSeek-R1、Qwen3-Thinking）通常对所有查询分配相同的思考预算，或依赖模型自身的“自判断”一刀切决定。这种策略存在根本性低效：

- **简单查询浪费计算**：对于模型已有高度确定性的问题，强制进行长链思维推理消耗大量 token 却几乎不带来准确率提升。
- **困难查询计算不足**：对于需要深度推理的问题，固定预算可能不足以让模型充分探索解空间。

Sonata 的核心洞察是：**查询本身在模型隐藏空间中的表示已经蕴含了其推理难度的信息**，可以直接用于判断是否需要启动思考。

### 关键机制：自一致性作为推理必要性的代理信号

Sonata 的方法论创新建立在三个递进的发现之上：

**1. 自一致性与思考增益的强负相关**

论文在 MATH-500 上使用 Qwen3-8B 进行实验，对每个查询在非思考模式下采样 32 次，计算自一致性分数：

$$\mathsf{SC}(q) = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}[a_i = a^*]$$

同时测量开启思考后的准确率提升：

$$\Delta_{\mathrm{think}}(q) = \mathrm{Acc}_{\mathrm{think}}(q) - \mathrm{Acc}_{\mathrm{non\text{-}think}}(q)$$

结果显示两者呈**强负相关**：自一致性低的查询从思考中获益最大，而自一致性高的查询几乎不需要思考即可正确回答（Figure 2）。这一发现将“是否需要思考”这一看似需要元认知能力的问题，转化为一个可量化的预测任务。

**2. 自一致性模式在隐藏空间中高度可区分**

通过对不同层的隐藏表示进行 PCA 可视化，论文发现自一致性模式在深层（尤其是最后一层）变得高度可区分：高自一致性查询形成紧密聚类，低自一致性查询则分散分布（Figure 3）。这意味着**无需实际采样**，仅从查询的隐藏表示就可以预测其自一致性。

**3. 基于预测的自适应决策**

基于以上发现，Sonata 将思考分配问题转化为一个**离线训练-在线预测**的轻量流程：

- **离线阶段**：在预填充阶段提取 LLM 最后一层最后一个 token 的隐藏表示 $\mathbf{h} \in \mathbb{R}^d$，训练一个两层 MLP 适配器（64 个隐藏单元）预测自一致性分数 $\hat{s} = f_\theta(\mathbf{h}) = \sigma(\mathrm{MLP}(\mathbf{h}))$。适配器总参数量仅约 262K（对于 Qwen3-8B，$d=4096$），推理开销小于 1‰。
- **在线阶段**：将预测分数 $\hat{s}$ 与预设阈值 $\tau_0$ 比较：若 $\hat{s} > \tau_0$，直接生成答案；否则启用默认思考过程。

### 与基线方法的本质差异

| 设计维度 | 固定预算基线 | 自判断基线 | Sonata |
|---------|------------|-----------|--------|
| 决策依据 | 无（所有查询统一） | LLM 自身判断 | 隐藏状态预测的自一致性 |
| 决策时机 | 预定义 | 生成前 | 预填充后、生成前 |
| 计算开销 | 零 | 额外推理开销 | < 1‰ |
| 粒度 | 全局固定 | 二值 | 二值（可扩展） |

自判断基线依赖 LLM 自身的元认知能力来判断是否需要思考，但 LLM 的“自信”往往不可靠——它可能对错误答案高度自信。Sonata 通过直接从隐藏状态预测自一致性，绕过了这一限制，直接捕捉推理的内在难度而非表面不确定性。

### 代理指标选择的优越性

消融实验（Table 3）表明，自一致性作为代理指标**显著优于**基于熵的替代方案：

- **LM logits 熵**：仅反映模型对下一个 token 的不确定性，无法捕捉多步推理的一致性。
- **注意力熵**：反映注意力分布的集中程度，与推理正确性的关联较弱。
- **自一致性**：直接测量模型在多次尝试中一致解决问题的能力，更准确地捕捉推理的内在难度。

这一选择是 Sonata 能够在维持甚至提升准确率的同时，将思考 token 消耗降低 20% 至 60% 的关键原因。



![[assets/figures/papers/paper_list_l6_Adaptive_Thinking_Large_Language_Models_Know_When_to_Think_in_Latent_Spa/figures/004_Figure_4.jpg]]

Sonata 的整体推理流程由三个核心模块串联构成：**预填充阶段隐藏状态提取**、**自一致性适配器预测**和**动态思考决策**。该框架在 LLM 原有的预填充-解码流水线中仅插入一个轻量级适配器，不改变模型权重，也不引入额外的采样开销。

### 模块关系与数据流

1. **预填充阶段隐藏状态提取**
   对于输入查询 $q$，在预填充阶段完成所有 token 的前向传播后，从最后一层 transformer 的最后一个 token 位置提取隐藏表征 $\mathbf{h} \in \mathbb{R}^d$。这一步骤利用 LLM 已有的深层表示能力，无需额外计算。

2. **自一致性适配器预测**
   将提取的隐藏表征 $\mathbf{h}$ 送入一个离线训练好的两层 MLP 适配器 $f_\theta$，经 sigmoid 映射输出预测的自一致性分数：
   $$\hat{s} = f_\theta(\mathbf{h}) = \sigma(\text{MLP}(\mathbf{h}))$$
   其中 MLP 包含 64 个隐藏单元，总参数量约为 $(d \times 64) + 64 + (64 \times 1) + 1$。对于 Qwen3-8B（$d=4096$），适配器仅约 262K 参数，推理计算开销小于 1‰。

3. **动态思考决策**
   将预测分数 $\hat{s}$ 与预设阈值 $\tau_0$（如 0.3）比较：
   - 若 $\hat{s} > \tau_0$，表明查询的自一致性较高，模型**不进行思考**，直接生成答案；
   - 否则，模型**启用默认思考过程**，执行完整的思维链推理。

### 关键设计决策

- **二值决策而非细粒度控制**：消融实验表明，4 级细粒度思考控制引入了难以调优的阈值组合，性能略低于二值方案。因此 Sonata 采用简洁的“思考/不思考”二值决策。
- **仅用最后一层最后一个 token**：聚合多层或多位置的隐藏表示反而降低了准确率或效率，最优方案仅使用最后一层最后一个 token 的表示。
- **自一致性作为代理信号**：相较于基于熵的指标（LM logits entropy、attention entropy），自一致性直接度量模型在多次采样中一致解决问题的能力，与推理必要性的因果关系更强。

### 与固定预算基线的对比

传统固定思考预算方法对所有查询分配相同的思考 token 数，导致简单查询浪费计算资源、复杂查询计算不足。Sonata 的适配器在预填充阶段即可判断查询的推理必要性，在解码开始前完成思考决策，实现了**查询级自适应计算分配**。



### 3.1 自一致性分数：推理必要性的代理信号

Sonata 的核心前提在于：查询在**非思考模式**下的自一致性（Self-Consistency）能够有效预测启用思维链推理后的性能增益。自一致性分数定义为在无思考模式下对同一查询进行 $N$ 次独立采样时，答案等于正确答案的比例：

$$\mathsf{SC}(q) = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}[a_i = a^*]$$

其中 $a_i$ 为第 $i$ 次采样的答案，$a^*$ 为正确答案。该分数的取值范围为 $[0, 1]$，高自一致性意味着模型在多次采样中能稳定给出正确答案，暗示查询对模型而言相对简单，无需额外思考；低自一致性则表明模型答案分歧大，查询需要扩展思维链推理。

启用思考后的准确率提升定义为：

$$\Delta_{\mathrm{think}}(q) = \mathrm{Acc}_{\mathrm{think}}(q) - \mathrm{Acc}_{\mathrm{non\text{-}think}}(q)$$

实验表明，$\mathsf{SC}(q)$ 与 $\Delta_{\mathrm{think}}(q)$ 之间呈现**强负相关**（Figure 2）：自一致性越低的查询，启用思考后的准确率提升越大。这一关系构成了 Sonata 以自一致性作为思考必要性代理信号的经验基础。

### 3.2 潜在空间的可区分性

自一致性模式在深层 Transformer 的隐藏表示中高度可区分。PCA 可视化（Figure 3）显示，在 MATH-500 和 GPQA 两个基准上，不同自一致性分数的查询在浅层（如第 1 层）的隐藏表示几乎不可分，但随着层数加深，高自一致性与低自一致性查询的表示逐渐形成分离的聚类，**最后一层**的区分度最为显著。这一发现直接支撑了 Sonata 的设计选择：仅从最后一层提取隐藏表征即可有效预测自一致性。

### 4.1 适配器训练：从隐藏表征到自一致性预测

Sonata 训练一个轻量级适配器 $f_\theta$，将查询的隐藏表征直接映射为自一致性预测值，从而在推理时避免昂贵的多次采样。具体流程如下：

1. **隐藏状态提取**：在预填充阶段，从 LLM 最后一层 Transformer 的最后一个 token 提取隐藏表征 $\mathbf{h} \in \mathbb{R}^d$。
2. **适配器预测**：适配器采用两层 MLP（64 个隐藏单元），将 $\mathbf{h}$ 映射为标量预测值，经 sigmoid 函数输出：

$$\hat{s} = f_\theta(\mathbf{h}) = \sigma(\mathrm{MLP}(\mathbf{h}))$$

其中 $\hat{s} \in [0, 1]$ 为预测的自一致性分数。适配器总参数量为 $(d \times 64) + 64 + (64 \times 1) + 1$，对于 Qwen3-8B（$d=4096$）约为 262K 参数，仅占模型总参数的极小比例。

3. **训练目标**：以校准数据集上预先计算的真实自一致性分数 $\mathsf{SC}(q_k)$ 作为标签，最小化预测误差。

### 4.2 动态思考决策

推理时，Sonata 将预测分数 $\hat{s}$ 与预设阈值 $\tau_0$ 比较：

- 若 $\hat{s} > \tau_0$，模型**不进行思考**，直接生成答案；
- 否则，模型启用默认的思维链推理过程。

阈值 $\tau_0$ 通过网格搜索在 $\{0.1, 0.3, 0.5\}$ 中经验设定。该二值决策机制在生成前完成，计算开销极小（$<1‰$ 的推理计算增量），且可与现有思维链压缩方法（如 REFRAIN 早期停止）兼容叠加。消融实验（Table 10）表明，二值控制优于 4 级细粒度控制，后者引入难以调优的多阈值组合。



## 实验与关键发现

### 核心发现

Sonata 在多个推理基准上实现了“准确率不降、思考 token 大幅减少”的计算最优推理。以 Qwen3-8B 为例，平均准确率从 vanilla 模型的 78.2% 提升至 79.6%，同时思考 token 消耗降低 21%（Table 1）。在 GSM8K 和 GPQA 上，token 节省尤为显著，分别达到 55.4% 和 51.9%，且准确率保持或超越基线。这一效果在不同规模的模型上均得到验证：Qwen3-32B、GPT-OSS-120B 和 Qwen3-235B-A22B 均展现出类似的准确率-效率增益模式。


![[assets/figures/papers/paper_list_l6_Adaptive_Thinking_Large_Language_Models_Know_When_to_Think_in_Latent_Spa/figures/006_Table_1.jpg]]
*Table 1: Comparison results on the AIME25, MATH-500, GSM8K, LiveCodeBench (LCB) and GPQA across four models with thinking capability. We use temperature = 0.6, top p = 0.95 for decoding. We report the average performance of three repeated trials for each run. Accuracy (Acc.) comparable to or higher than the vanilla baseline model are underlined, and the lowest thinking token counts (#Tokens) among those with underlined accuracy are marked in bold*

端到端推理效率方面，Sonata 带来的延迟降低幅度为 27% 至 36%，而显存开销增加不足 1%（Table 2）。适配器本身仅引入约 262K 参数（对于隐藏维度 d=4096 的 Qwen3-8B），推理计算开销低于千分之一（<1‰），使其成为几乎零成本的动态调度方案。

### 帕累托前沿：准确率-效率权衡

通过调整自一致性阈值 $\tau_0$，Sonata 在准确率-效率帕累托前沿上显著优于固定思考预算基线（Figure 5）。在 Qwen3-8B 和 Qwen3-32B 上，Sonata 在同等准确率水平下可节省高达 50% 的 token 预算。这一优势源于 Sonata 按查询难度动态分配计算资源——简单查询跳过思考直接回答，困难查询保留完整思维链推理——而非对所有查询一视同仁地分配固定预算。


![[assets/figures/papers/paper_list_l6_Adaptive_Thinking_Large_Language_Models_Know_When_to_Think_in_Latent_Spa/figures/009_Figure_5.jpg]]
*Figure 5: Accuracy-efficiency Pareto frontiers comparing Sonata against constant budget baseline on Qwen3-8B and Qwen3-32B. By adjusting the selfconsistency threshold $\tau _ { 0 }$ , , Sonata consistently outperforms the fixed budget approach, achieving up to 50% token savings at comparable accuracy levels*

### 代理指标消融：自一致性为何有效

Table 3 对比了三种用于预测思考必要性的代理指标：自一致性（Sonata）、LM logits 熵和注意力熵。结果表明，自一致性在准确率-效率权衡上显著优于两种基于熵的指标。其根本原因在于：自一致性直接测量模型在多次独立采样中稳定得出正确答案的能力，捕捉的是推理本身的内在难度，而非模型输出的表面不确定性。基于熵的指标反映的是 token 级预测的不确定性，无法有效区分“模型不确定但凭直觉也能答对”和“模型看似确定但实际推理错误”的情况。


![[assets/figures/papers/paper_list_l6_Adaptive_Thinking_Large_Language_Models_Know_When_to_Think_in_Latent_Spa/figures/010_Table_3.jpg]]
*Table 3: Comparison of different proxy metrics for adaptive thinking allocation on four benchmarks. We report accuracy (Acc.) and average thinking tokens (#Tokens) across Qwen3-8B and Qwen3- 32B models. Results show that self-consistency (Sonata) substantially outperforms two entropybased metrics, i.e. LM logits entropy and Attention entropy, in the accuracy-efficiency tradeoff*

### 适配器架构与数据效率

适配器架构消融（Table 4）显示，两层 MLP（64 个隐藏单元）在准确率和效率之间取得了最佳平衡。线性投影表达能力不足，三层 MLP 则可能过拟合且增加不必要的复杂度。校准数据集规模消融（Table 5）进一步表明，仅需 100 个样本，Sonata 仍能保持 79.0% 的平均准确率（vanilla 基线为 78.2%），展现出极强的样本效率。

### 与现有方法的兼容性

Sonata 可与思维链压缩方法协同工作。Table 6 显示，将 Sonata 与 REFRAIN 早期停止方法结合，可将 token 使用进一步压缩至 vanilla 模型的 64%，同时保持 78.7% 的平均准确率。这表明 Sonata 的“是否思考”决策与 REFRAIN 的“何时停止思考”机制是互补的，两者叠加可产生更大的效率增益。

### 表示聚合策略

Table 7 的消融实验验证了仅使用最后一层最后一个 token 的隐藏表示即为最优设计。聚合最后四层或最后四个 token 的表示反而导致准确率下降或效率损失。这一发现与 Figure 3 的 PCA 可视化一致：深层（尤其是最后一层）隐藏表示中自一致性模式的可分性最强，额外的聚合引入噪声而非信息增益。


![[assets/figures/papers/paper_list_l6_Adaptive_Thinking_Large_Language_Models_Know_When_to_Think_in_Latent_Spa/figures/003_Figure_3.jpg]]
*Figure 3: PCA visualization of query hidden representations across different transformer layers, colored by self-consistency scores, evaluated on both MATH-500 (math reasoning) and GPQA (scientific reasoning) benchmarks. Self-consistency patterns become increasingly distinguishable in deeper layers, with the last layers (i.e. 36, 64) showing the most pronounced separation. High self-consistency queries (dark) form tight clusters while low self-consistency queries (light) are more dispersed, demonstrating that self-consistency signals are learnable from latent representations across diverse reasoning domains*

### 细粒度控制与扩展尝试

将二值思考控制（是否思考）扩展为 4 级细粒度控制（Table 10）并未带来性能提升，反而因阈值组合难以调优而略逊于二值方案。同时预测自一致性和思考增益的扩展版本（Table 8）与原始 Sonata 性能几乎无差别，说明自一致性本身已足够作为有效的思考必要性代理信号。

### 失败模式与局限性

尽管 Sonata 在数学、科学和代码推理任务上表现优异，但其思考决策是生成前的二值判断，无法在推理进行中动态调整思考深度。对于“本质困难”的问题——即自一致性低且开启思考后准确率提升也有限的问题——Sonata 仍会分配思考预算但收效甚微。此外，阈值 $\tau_0$ 通过网格搜索在 {0.1, 0.3, 0.5} 中经验设定，未针对不同模型或任务自动优化。校准数据集需要正确答案来预先计算自一致性标签，限制了在完全无监督场景下的直接应用。

### 待验证的泛化性

当前评估集中在数学推理（MATH-500、GSM8K、AIME25）、科学推理（GPQA）和代码生成（LiveCodeBench），长文本生成或开放域对话中的适用性尚待验证。适配器在模型微调或持续学习后的准确性保持情况也需进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l6_Adaptive_Thinking_Large_Language_Models_Know_When_to_Think_in_Latent_Spa/figures/002_Figure_2.jpg]]
*Figure 2: Correlation between self-consistency and thinking improvement across five difficulty levels on MATH-500 using Qwen3-8B. Each point denotes an individual query, with self-consistency computed from N = 32 samples in non-thinking mode (x-axis) and accuracy improvement from enabling thinking averaged over 3 runs (y-axis)*




## 定位与知识库关联

### 与现有方法的关系

Sonata 处于自适应推理预算分配的方法谱系中，其核心创新在于**将“是否需要思考”的判断从模型内部生成转移到外部轻量预测**，从而避免了自判断方法的高昂推理开销。

**固定思考预算基线**（Constant Thinking Budget）对所有查询分配相同的思考 token 数，达到预算时插入终止 token 强制结束思考。该方法的问题在于：简单查询浪费计算资源，复杂查询思考不足。Sonata 通过查询级自适应分配直接解决了这一瓶颈。

**自判断基线**（Self-Judge）先让 LLM 自行判断是否需要思考，再根据判断决定是否启用思考模式。该方法虽然引入了查询级自适应，但判断过程本身消耗大量 token，且判断准确率受限于模型自身的元认知能力。Sonata 用离线训练的轻量适配器替代了这一昂贵的在线判断过程，适配器仅增加 <1‰ 的推理计算开销。

**与思维链压缩方法的兼容性**：Sonata 的策略是“是否思考”的二值决策，与“思考多长”的早期停止方法（如 REFRAIN）正交。实验表明，Sonata 与 REFRAIN 结合可将 token 使用进一步压缩至基线的 64%，平均准确率保持在 78.7%（Table 6），验证了两类方法的互补性。

### 适用边界

Sonata 的有效性建立在以下假设之上，这些假设界定了其适用边界：

1. **自一致性作为代理信号的有效性**：Sonata 依赖自一致性（多次采样答案的一致性）作为思考必要性的代理指标。这一假设在数学推理（MATH-500、GSM8K）、科学推理（GPQA）和竞赛级数学（AIME25）上得到了充分验证，但在开放式生成、创意写作或主观评价任务中，自一致性的定义和有效性尚待检验。

2. **隐藏表征的可区分性**：适配器需要从查询的最后一层隐藏表征中提取自一致性信号。论文通过 PCA 可视化（Figure 3）证明了深层表征中自一致性模式的可区分性，但这一发现目前仅在 Qwen3 系列模型上得到验证。不同架构（如非 Transformer 架构、不同训练目标的模型）的隐藏表征是否具有类似的可区分性，需要进一步验证。

3. **校准数据的可获得性**：适配器训练需要正确答案来计算自一致性标签。虽然实验表明仅需 100 个校准样本即可保持性能（Table 5），但在完全无监督场景下，如何获取或构造校准数据仍是一个开放问题。

4. **任务类型覆盖**：实验覆盖了数学、科学和代码推理任务，长文本生成、多轮对话、开放域问答等任务类型的泛化性未知。

### 局限与开放问题

**架构层面的局限**：

- **生成前二值决策**：Sonata 在生成开始前做出“是否思考”的一次性决策，无法在推理进行中动态调整思考深度。对于需要“适度思考”的中间难度查询，二值决策可能不够精细。实验也表明，4 级细粒度控制（Table 10）并未带来性能提升，反而引入了难以调优的阈值组合，说明当前的隐藏表征对细粒度思考需求的区分能力有限。

- **适配器与模型绑定**：适配器针对特定 LLM 的隐藏表征训练，更换模型架构需要重新训练。虽然论文在 Qwen3-8B、Qwen3-32B、GPT-OSS-120B 和 Qwen3-235B 上展示了效果，但适配器的跨模型迁移能力未被系统研究。

**训练与优化层面的局限**：

- **阈值设定依赖经验网格搜索**：决策阈值 $\tau_0$ 通过网格搜索在 {0.1, 0.3, 0.5} 中经验设定，未针对每个模型或任务自动优化。不同任务的最优阈值可能存在差异，手动调参限制了方法的即插即用性。

- **自一致性标签的监督需求**：校准数据集需要正确答案来预先计算自一致性标签，这限制了在无监督场景下的直接应用。如何在无标签数据上训练适配器，或利用模型自身的置信度信号替代正确答案，是一个重要的开放问题。

**开放研究方向**：

1. **推理中动态控制**：能否在推理进行中（mid-reasoning）动态调整推理长度？这需要设计能够感知中间推理状态的控制器，而非仅依赖查询的初始隐藏表征。

2. **更丰富的控制器设计**：当前适配器仅使用最后一层最后一个 token 的隐藏状态。消融实验（Table 7）表明聚合多层或多位置反而降低性能，但这是否意味着更复杂的聚合策略（如注意力加权、跨层交互）也无效，仍有待探索。

3. **在线强化学习优化**：可否通过在线强化学习直接优化 token 预算-性能权衡下的早期停止策略，替代当前的离线监督训练范式？

4. **本质困难问题的处理**：对于自一致性和思考增益均低的“本质困难”问题，当前方法无法有效分配计算资源。如何识别这类问题并设计针对性的资源分配策略，是一个重要的实践挑战。

5. **适配器的持续适应性**：适配器在模型微调或持续学习后能否保持准确性，或者需要自适应更新机制，这一问题对实际部署至关重要但尚未被研究。



## 原文 PDF

![[paperPDFs/ICLR_2026/Adaptive_Thinking_Large_Language_Models_Know_When_to_Think_in_Latent_Space.pdf]]
