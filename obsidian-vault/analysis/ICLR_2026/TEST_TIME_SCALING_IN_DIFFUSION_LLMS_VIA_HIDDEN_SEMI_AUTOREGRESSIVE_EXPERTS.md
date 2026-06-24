---
title: "TEST-TIME SCALING IN DIFFUSION LLMS VIA HIDDEN SEMI-AUTOREGRESSIVE EXPERTS"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TEST_TIME_SCALING_IN_DIFFUSION_LLMS_VIA_HIDDEN_SEMI_AUTOREGRESSIVE_EXPERTS.pdf
openreview_forum_id: L5y7in91vd
aliases:
- HHSAE
- TTSDLHSAE
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/probabilistic_methods
core_operator: "半自回归解码的块大小（block size）直接激活模型中不同的隐藏专家，多样化块调度构成可聚合的推理路径。"
primary_logic: "扩散大语言模型在任意掩码训练中隐式学习了一个半自回归专家的混合，通过测试时聚合多个不同块调度的输出（多数投票）可以充分激发模型的推理能力，无需针对特定启发式进行微调。"
claims:
- "采用随机去掩码的 GSM8K 准确率（50.87%）远优于 top-K margin 方法（24.72%），后者出现超过 55.5% 的 [AfterEoT] 崩溃。"
- "HEX 在 GSM8K 上将准确率从 24.72% 提升至 88.10%（高达 3.56×），在 MATH、ARC-C、TruthfulQA 上均大幅超过现有推理方法和 GRPO 微调模型。"
- "增加多样化的块调度数量和投票样本可单调提升准确率并降低平局率，表明 HEX 的有效性源于专家组合而非单纯增加采样。"
- "半自回归解码完全消除了 [AfterEoT] 崩溃现象，将 GSM8K 准确率从 22.52% 提升至 76.27%。"
---

# TEST-TIME SCALING IN DIFFUSION LLMS VIA HIDDEN SEMI-AUTOREGRESSIVE EXPERTS

> [!tip] 核心洞察
> 扩散大语言模型在任意掩码训练中隐式学习了一个半自回归专家的混合，通过测试时聚合多个不同块调度的输出（多数投票）可以充分激发模型的推理能力，无需针对特定启发式进行微调。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过隐藏半自回归专家实现扩散大语言模型的测试时扩展 |
| 英文题名 | TEST-TIME SCALING IN DIFFUSION LLMS VIA HIDDEN SEMI-AUTOREGRESSIVE EXPERTS |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=L5y7in91vd); [GitHub](https://github.com/junos-ai-org/Test-Time-Scaling) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/probabilistic_methods |
| Method | HEX (Hidden semi-autoregressive EXperts) |
| Dataset | GSM8K, MATH, ARC-C |

> [!tip] 效果简介
> - GSM8K 上，Accuracy 为 88.10%，对比 24.72% (top-k margin)，变化 +63.38%。
> - GSM8K 上，Accuracy 为 88.10%，对比 79.80% (d1 GRPO)，变化 +8.30%。
> - MATH 上，Accuracy 为 40.00%，对比 16.40% (top-k margin)，变化 +23.60%。

## 概述

扩散大语言模型（dLLM）在推理任务上展现出潜力，但其测试时解码策略长期受困于一个关键瓶颈：**基于置信度的固定掩码调度极易触发灾难性退化**。例如，广泛使用的 top-K margin 方法在 GSM8K 上准确率仅 24.72%，且超过 55.5% 的生成序列完全退化为 `[AfterEoT]` 标记（Figure 2）。这一现象表明，单纯依赖逐 token 置信度进行解码决策，会系统性地将模型引入过信心的错误路径。

本文的核心洞察在于：**dLLM 在任意掩码训练中隐式地学习了一个半自回归专家的混合**。不同的掩码条件实际上激活了模型内部不同的条件预测分布，这些分布可被视为隐藏的“专家”。基于此，作者提出 **HEX（Hidden Semi-autoregressive EXperts）**——一种无需训练的测试时扩展方法。HEX 通过定义一组异质的半自回归块调度，在测试时聚合多个专家的输出，以多数投票的方式产生最终答案。

HEX 的效果是显著的：在 GSM8K 上，准确率从 24.72% 提升至 88.10%（**3.56 倍**），在 MATH、ARC-C、TruthfulQA 上同样大幅超越现有推理方法，甚至超过了需要 GRPO 微调的基线模型（Figure 5）。消融实验进一步证实，性能增益源于**块调度的结构性多样性**而非单纯的采样增加——多块调度集成显著优于单一调度下的多样本采样（Table 7）。

## 背景与动机

### 扩散语言模型的推理瓶颈

扩散语言模型（Diffusion Large Language Models, dLLMs）通过在任意掩码训练中学习从噪声到文本的生成过程，展现出非自回归生成的潜力。其训练目标为最大化被掩码位置上真实 token 的概率：

$$
\theta ^ { * } \in \arg \underset { \theta } { \operatorname* { m i n } } \ : \mathcal { L } _ { \operatorname* { m a x } } ( \theta ) : = \mathbb { E } _ { x \sim \mathcal { D } } \mathbb { E } _ { \ell \sim \operatorname { U n i f } ( [ n ] ) } \mathbb { E } _ { M \subseteq [ n ] , | M | = \ell } \Big [ - \displaystyle \sum _ { i \in M } \log p _ { \theta } ( x _ { i } \mid x [ M ^ { c } ] ) \Big ]
$$

然而，在推理任务中，现有的训练无关解码策略暴露出严重的结构性缺陷。基于置信度的固定掩码策略——尤其是 top-K margin 方法——在 GSM8K 上准确率仅为 24.72%，远低于随机去掩码的 50.87%（Figure 2）。更致命的是，top-K margin 方法在超过 55.5% 的推理过程中产生灾难性的 **[AfterEoT] 崩溃**：模型从序列末端逆向生成，反复输出退化的结束标记，导致输出完全不可用。这一现象揭示出单纯依赖 token 置信度进行解码调度是不可靠的，置信度驱动的启发式方法无法保证推理过程的连贯性。

### 隐藏的半自回归专家结构

上述崩溃的根源在于现有方法未能有效利用 dLLMs 在训练中隐式学到的专家结构。模型在任意掩码训练过程中，实际上学习了一个以不同可见 token 集合 $U$ 为条件的专家混合预测器：

$$
p _ { \mathrm { m i x } } ( x _ { i } = a \mid x _ { \mathrm { p r o m p t } } ) = \sum _ { U } \pi ( U \mid x _ { \mathrm { p r o m p t } } ) p _ { \theta } ( x _ { i } = a \mid [ x _ { \mathrm { p r o m p t } } , x [ U ] ] )
$$

不同的掩码条件激活不同的条件分布，形成隐式的“专家”。然而，直接枚举所有可能的 $U$ 在计算上是不可行的。一个关键的因果调控旋钮是**半自回归解码的块大小**（block size）：通过将序列按块大小 $b$ 划分为连续的块 $M _ { t } = \{ ( t - 1 ) b + 1 , \ldots , \operatorname* { m i n } ( t b , n ) \}$，不同的 $b$ 会迫使模型激活不同的隐藏专家，产生多样化的推理路径。实验表明，仅采用半自回归解码即可完全消除 [AfterEoT] 崩溃（崩溃率从 29%–56% 降至 0%），并将 GSM8K 准确率从 22.52% 提升至 76.27%（Table 1）。

### 测试时扩展的新维度

基于上述发现，本文的核心洞察是：**dLLMs 在训练中隐式学习了一个半自回归专家的混合，通过测试时聚合多个不同块调度的输出，可以充分激发模型的推理能力，无需针对特定启发式进行微调。** 这一思路将测试时扩展（test-time scaling）从传统的增加采样次数提升到结构化多样性聚合的层面——不仅增加样本数量，更重要的是通过异构的块调度引入推理路径的结构性差异。由此，扩散语言模型的推理不再依赖单一的、可能崩溃的解码策略，而是通过多数投票机制在多个隐藏专家的输出中寻找共识，从而稳定且显著地提升推理性能。

## 核心创新

### 瓶颈洞察：置信度驱动的扩散解码为何崩溃

扩散大语言模型（dLLM）在推理任务上采用基于置信度的固定掩码策略时，存在一个被忽视的灾难性失效模式：模型在去掩码过程中会过度自信地优先选择 `[AfterEoT]` 标记，导致超过 55.5% 的生成序列完全退化为无意义的终止标记串（Figure 2）。这一现象的根源在于，模型在任意掩码训练中隐式学习了多个条件专家，而单一置信度驱动的解码策略无法有效激活和利用这些专家结构，反而将模型推向了高置信度但无意义的退化状态。

### 因果调控变量：块大小激活隐藏专家

HEX 的核心发现是：**半自回归解码的块大小（block size）直接激活扩散模型中不同的隐藏专家**。当块大小 $b$ 变化时，模型的条件分布 $p_{\theta}(x_i \mid [x_{\text{prompt}}, x[U_b]])$ 发生显著改变（Figure 3），这意味着每个块调度本质上对应一个不同的“专家”。这一洞察将扩散语言模型重新解释为一个隐式的专家混合（Mixture of Experts），其中专家索引由可见标记集合 $U$ 决定：

$$p_{\text{mix}}(x_i = a \mid x_{\text{prompt}}) = \sum_{U} \pi(U \mid x_{\text{prompt}})\, p_{\theta}(x_i = a \mid [x_{\text{prompt}}, x[U]])$$

### 关键方法创新：从单一调度到专家集成

与现有方法的核心差异体现在两个关键设计槽位上：

**1. 解码调度策略：从单一固定调度到多块大小集成与多数投票**

| 方法 | 调度策略 | 聚合方式 |
|------|---------|---------|
| Random / Top-k / Top-k margin | 单一固定调度（随机或置信度驱动） | 单次解码输出 |
| **HEX** | 多块大小的半自回归调度集成 | 多数投票聚合 |

HEX 通过在一组预定义的块大小 $B = [8, 16, 32, 64, 128]$ 上分别执行半自回归解码，将理想的专家混合近似为：

$$p_{\text{mix}}(x_i = a \mid x_{\text{prompt}}) \approx \mathbb{E}_{b \sim B}\left[p_{\theta}(x_i = a \mid [x_{\text{prompt}}, x[U_b]])\right]$$

每个块大小各采样 5 条轨迹（temperature = 0.9），共产生 25 条推理路径，通过多数投票聚合最终答案。这种“结构性多样性”（不同块调度）显著优于仅靠随机种子增加采样的策略：在 GSM8K 上准确率差距达 8.57%，MATH 上达 4.2%（Table 7），表明性能提升源于专家组合的互补性，而非单纯的采样数量增加。

**2. 平局处理：优先选择最小块大小的生成结果**

当多数投票出现平局时，HEX 采用 `TIED: first` 策略——选择最小块大小生成的答案。这一设计的直觉在于：较小的块大小意味着更细粒度的自回归约束，模型在每个生成步骤中能参考更多已解码的上下文信息，其输出通常更可靠。实验表明，该策略与允许任一正确答案（`TIED: any`）的性能接近，均能有效发挥多数投票的潜力（Table 4）。

### 方法定位：无需训练的测试时扩展范式

HEX 的核心贡献在于开辟了扩散大语言模型的**测试时扩展（test-time scaling）**新维度。与需要 GRPO 微调的 d1 等方法不同，HEX 完全无需训练，仅通过推理时的调度集成即可将 GSM8K 准确率从 24.72% 提升至 88.10%（3.56×），甚至超过 GRPO 微调模型（79.80%）。这一结果确立了测试时计算扩展作为扩散语言模型推理能力提升的有效范式。

## 整体框架

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/002_Figure_1.jpg]]
*Figure 1: Overview of our proposed HEX framework. Left: HEX leverages multiple semiautoregressive hidden experts, guided by different masking schedules, to produce concatenated outputs and a final answer. Right: HEX outperforms Top-K, Top-K margin (Kim et al., 2025) and Random expert selection strategies (Nie et al., 2025b) on reasoning tasks (GSM8K, MATH, ARC-C), surpassing the training-based GRPO baseline (d1) (Zhao et al., 2025)*

HEX（Hidden semi-autoregressive EXperts）是一种无需训练的推理方法，通过聚合多个半自回归解码轨迹的输出来激发扩散大语言模型（dLLM）的推理能力。其核心流程由四个模块串联构成。

### Pipeline 总览

给定一个提示 $x_{\text{prompt}}$，HEX 首先定义一组块调度 $\mathcal{B} = \{b_1, b_2, \ldots, b_K\}$（例如 $[8, 16, 32, 64, 128]$），每个块大小 $b$ 对应一种半自回归解码策略。对每个调度，模型以温度 $0.9$ 采样多个种子，生成完整的输出序列。所有序列经过解析器 $f$ 提取最终答案后，进入多数投票聚合阶段：统计出现频率最高的答案作为最终输出。若多个答案票数相同，HEX 默认选择由最小块大小生成的答案（TIED: first 策略）。

这一流程可形式化为对理想专家混合预测器的蒙特卡洛近似：

$$p_{\mathrm{mix}}(x_i = a \mid x_{\mathrm{prompt}}) \approx \mathbb{E}_{b \sim B}\left[p_{\theta}(x_i = a \mid [x_{\mathrm{prompt}}, x[U_b]]) \right]$$

其中 $U_b$ 表示在块调度 $b$ 下已可见的 token 集合。最终预测通过多数投票简化实现，而非直接计算贝叶斯最优解 $\hat{a} = \arg\max_a p_{\mathrm{mix}}(x_i = a \mid x_{\mathrm{prompt}})$。

### 模块关系与数据流

1. **多块调度生成**：输入为预定义的块大小集合和采样种子数。该模块负责为每个块大小分配独立的随机种子，确保不同调度产生结构多样化的推理轨迹。

2. **半自回归解码**：对每个块调度 $b$，将输出序列按 $M_t = \{(t-1)b+1, \ldots, \min(tb, n)\}$ 划分为连续块。解码从左到右逐块进行：块内采用扩散式并行去掩码（每步去掩码 2 个 token），块间强制顺序依赖。这种设计既保留了扩散生成在块内的并行效率，又通过位置约束迫使推理从左到右推进，从根本上消除了非半自回归解码中常见的 [AfterEoT] 灾难性崩溃——该崩溃在 top-K margin 方法中发生率超过 55.5%（Figure 2）。

3. **答案解析**：将每条生成序列转换为可比较的答案形式（数值或字符串），为多数投票做准备。

4. **多数投票聚合与平局决断**：统计所有调度输出中每个答案的出现频次，选取最高频答案。平局时优先采纳最小块大小的输出，因为较小块大小通常对应更细粒度的推理步骤。

### 关键设计依据

HEX 的设计根植于一个核心洞察：dLLM 在任意掩码训练中隐式地学习了一个半自回归专家的混合。不同的块调度激活模型中不同的隐藏专家（Figure 3），而单一调度（无论是随机去掩码还是置信度驱动的 top-K margin）仅能利用部分专家能力。实验表明，随机去掩码在 GSM8K 上达到 50.87% 准确率，远优于 top-K margin 的 24.72%（Figure 2），说明基于置信度的固定策略存在系统性缺陷。HEX 通过集成多种块调度，以多数投票方式聚合互补的推理路径，从而充分释放模型的潜在推理能力——在 GSM8K 上将准确率提升至 88.10%，达到 3.56 倍的提升（Figure 5）。

### 计算开销

相比单一解码策略，HEX 的计算开销约增加 5 倍（使用 5 种块大小各采样 1 个种子）。该开销源于多轨迹生成的并行需求，但换取了无需训练的显著性能提升，且在实际部署中可通过并行化部分缓解。

## 核心模块与公式推导

### 关键模块

HEX 方法由四个核心模块串联构成，形成从调度定义到答案聚合的完整推理管线：

1. **多块调度生成**：预先定义一组半自回归块大小 $B$（如 $[8, 16, 32, 64, 128]$）及对应的采样种子。每个块大小 $b \in B$ 对应一个独立的解码轨迹，构成可聚合的专家路径。

2. **半自回归解码**：对每个块大小 $b$，将输出序列按连续块划分 $M_t = \{(t-1)b+1, \ldots, \min(tb, n)\}$，从左到右逐块生成。块内采用扩散式并行去掩码，块间保持自回归的顺序约束。这一约束从根本上消除了非半自回归解码中常见的 [AfterEoT] 灾难性崩溃（Table 1 显示崩溃率从 29%–56% 降至 0%）。

3. **答案解析**：通过解析器 $f$ 将每个解码轨迹的生成文本转换为可比较的答案形式（数值或字符串），为后续投票提供标准化输入。

4. **多数投票与平局决断**：统计所有调度输出中出现频率最高的答案。当多个答案票数相同时，优先选择由最小块大小生成的答案（TIED: first 策略）。消融实验表明，这一策略与基于负对数似然的平局决断相比无显著劣势，且实现更简洁（Table 4）。

### 核心公式

**训练目标**

扩散语言模型的训练目标为最大化被掩码位置上真实 token 的对数似然：

$$\theta^{*} \in \arg\min_{\theta} \mathcal{L}_{\max}(\theta) := \mathbb{E}_{x \sim \mathcal{D}} \mathbb{E}_{\ell \sim \operatorname{Unif}([n])} \mathbb{E}_{M \subseteq [n], |M| = \ell} \left[ -\sum_{i \in M} \log p_{\theta}(x_i \mid x[M^c]) \right]$$

其中 $x$ 为完整序列，$M$ 为随机采样的掩码位置集合，$\ell$ 为掩码数量，$M^c$ 为可见 token 的补集。该目标使模型在训练中隐式学习了以任意可见 token 集合为条件的预测能力。

**理想推理目标**

给定解码轨迹 $\tau$（即一系列掩码调度 $\{M_t\}_{t=1}^{T}$），其推理质量的对数似然泛函为：

$$\mathcal{I}(\tau; \theta \mid x_{\text{prompt}}) = \sum_{t=1}^{T} \sum_{i \in M_t} \log p_{\theta^{*}}(x_i \mid x_{\text{prompt}}, x\left[\bigcup_{s=1}^{t-1} M_s^c\right])$$

该式衡量在逐步揭示 token 的过程中，每个被掩码位置的条件预测质量之和。

**专家混合预测器**

论文的核心洞察在于：训练后的 dLLM 可视为一个隐式专家混合，每个专家对应一种可见 token 集合 $U$ 下的条件分布。理想的聚合方式为：

$$p_{\text{mix}}(x_i = a \mid x_{\text{prompt}}) = \sum_{U} \pi(U \mid x_{\text{prompt}}) p_{\theta}(x_i = a \mid [x_{\text{prompt}}, x[U]])$$

其中 $\pi(U \mid x_{\text{prompt}})$ 为专家权重。由于枚举所有可能的 $U$ 不可行，HEX 通过在一组块调度 $B$ 上取平均来近似该理想聚合：

$$p_{\text{mix}}(x_i = a \mid x_{\text{prompt}}) \approx \mathbb{E}_{b \sim B}\left[ p_{\theta}(x_i = a \mid [x_{\text{prompt}}, x[U_b]]) \right]$$

其中 $U_b$ 表示按块大小 $b$ 进行半自回归解码时已揭示的 token 集合。最终答案通过多数投票从该近似分布中得出。

## 实验与分析

### 核心发现：半自回归解码消除灾难性崩溃

扩散大语言模型在推理任务上采用基于置信度的解码策略时，存在一个致命瓶颈：模型在去掩码过程中过早且过度自信地生成 `[AfterEoT]` 退化标记，导致整条输出序列崩溃。Figure 2 揭示了这一现象的严重性——在 GSM8K 上，top-K margin 方法的准确率仅为 24.72%，而超过 55.5% 的运行出现了全部标记坍缩为 `[AfterEoT]` 的灾难性失败。相比之下，简单的随机去掩码反而达到 50.87% 的准确率，这直接动摇了“置信度越高越好”的直觉。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/003_Figure_2.jpg]]
*Figure 2: Random vs. Top-K margin inference on GSM8K. Left: Random decoding achieves 50.87% accuracy, while Right: Top-K margin only 24.72%. For each method, the text box shows the result at the last unmasking step. Top-K margin generates output tokens in reverse, from the end toward the beginning, and exhibits a catastrophic collapse in which all tokens are [AfterEoT] (shown in red). Over 55.5% of top-K margin runs suffered this collapse, yielding very low accuracy. These failures cast doubt on methods that rely solely on token confidence*

Table 1 给出了根治这一问题的关键证据：将解码策略从非半自回归切换为半自回归（semi-AR）后，`[AfterEoT]` 崩溃率从 29%–56% 降至 **0.00%**。在 GSM8K 上，准确率从 22.52% 跃升至 76.27%；在 MATH 上，从 16.60% 提升至 32.80%。因果机制在于：半自回归解码通过块划分（$M_t = \{(t-1)b+1, \ldots, \min(tb, n)\}$）强制推理从左到右推进，同时允许块内进行扩散式并行生成，从而避免了模型从末尾高置信度标记（恰是 `[AfterEoT]`）开始反向填充的惯性崩溃（Figure 8）。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/006_Table_1.jpg]]
*Table 1: Semi-AR based decoding eliminates [AfterEoT] collapse and improves accuracy*

### 主要结果：HEX 在推理基准上的表现

HEX 通过聚合多个不同块大小的半自回归解码输出并进行多数投票，在四个推理基准上实现了大幅提升。Figure 5 和 Table 3 汇总了核心对比：

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/007_Figure_5.jpg]]
*Figure 5: HEX improves reasoning accuracy. On LLaDA-8B-Instruct, HEX outperforms trainingfree baselines (Random, Top-k, Top-k-margin) on GSM8K, MATH, ARC-C, and TruthfulQA. In GSM8K, MATH, ARC-C, it even outperforms the model trained with GRPO without any training*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/013_Table_3.jpg]]
*Table 3: Ablations across datasets. NLL selects the candidate with the lowest NLL. HEX’s tie issue diminishes as the number of samples increases. Block sizes: [8, 16, 32, 64, 128]*

| 基准 | Top-K Margin | HEX (×5 seeds) | 提升倍数 | d1 (GRPO) |
|------|-------------|----------------|---------|-----------|
| GSM8K | 24.72% | **88.10%** | 3.56× | 79.80% |
| MATH | 16.40% | **40.00%** | 2.44× | 37.20% |
| ARC-C | 54.18% | **87.80%** | 1.62× | 82.68% |
| TruthfulQA | 28.36% | **57.46%** | 2.03× | — |

HEX 在 GSM8K、MATH、ARC-C 上甚至超过了需要 GRPO 微调的 d1 模型，而自身完全无需训练。这确立了测试时扩展作为扩散大语言模型推理能力提升的新范式。

### 消融分析：是什么驱动了 HEX 的性能？

#### 1. 多数投票优于似然选择

Table 3 对比了两种聚合策略：基于频率的多数投票（HEX）与基于负对数似然的最优选择（NLL）。在 ARC-C 上，HEX 的多数投票（87.80%）比 NLL 选择（74.07%）高出约 13.73 个百分点。这表明**轨迹间的共识信号比模型自身的置信度评分更可靠**，与前述 top-K margin 失败的原因一脉相承——模型在推理任务上的置信度估计存在系统性偏差。

#### 2. 结构性多样性优于随机多样性

Table 7 给出了一个关键对照：HEX 使用 5 种块大小各 5 个种子（共 25 样本）与单一固定块大小 25 样本进行对比。在 GSM8K 上，HEX 的多样块调度（88.10%）比单一块调度（79.53%）高出 8.57%；在 MATH 上高出 4.20%。这直接证明：**性能增益源于不同块大小激活的隐藏专家之间的互补性，而非单纯增加采样数量**。块大小的变化改变了可见 token 集合 $U$，从而调用了模型中不同的隐式专家 $p_\theta(x_i \mid [x_{\text{prompt}}, x[U]])$。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/024_Table_7.jpg]]
*Table 7: HEX outperforms the baseline with a single block schedule and 25 samples*

#### 3. 动态块数量与投票样本的扩展行为

Table 2 显示，将动态块调度数量从 5 增加到 30，GSM8K 准确率从 81.96% 单调提升至 84.15%，同时平局率从 3.87% 降至 1.06%。Figure 6 进一步表明，增加投票样本数（种子数从 1 到 6）可单调提升准确率并降低平局率。这种可预测的扩展行为是 HEX 实用性的重要保证。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/012_Table_2.jpg]]

#### 4. 平局处理策略

Table 4 比较了三种平局决断方式：TIED: NLL（选似然最低者）、TIED: first（选最小块大小输出）、TIED: any（只要平局候选中有正确答案即算正确）。TIED: any 在各基准上均取得最高准确率（GSM8K 83.09%、MATH 41.00%），说明多数投票本身已有效将正确答案推入平局候选集，平局决断策略主要影响边界收益。HEX 默认采用 TIED: first，在简洁性和有效性之间取得平衡。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/021_Table_4.jpg]]
*Table 4: Evaluation on tie breaking methods. If the most frequent output is in a tie situation, TIED: NLL selects the result with the lowest negative log-likelihood in tie situations, TIED: first selects the result generated from the smallest block size when tied, and TIED: any treats the case as correct if a correct option exists among the tied candidates. The results of TIED: any clearly highlight that majority voting of HEX works well across datasets*

### 失败模式与边界条件

尽管 HEX 大幅消除了 `[AfterEoT]` 崩溃，仍有约 2.96% 的案例中半自回归解码失败（Figure 9）。这些失败案例的去掩码顺序表现为**从两端向中心收敛**——模型先确定了答案，再反向推导过程。这意味着模型在完成完整推理前就锁定了答案，而 Wang et al. (2025) 已表明扩散大语言模型在推理过程中答案可能反复翻转，过早锁定答案难以保证正确性。

块大小的选择也存在敏感区间。Figure 10 显示，在 TruthfulQA 上，当块大小从 16 递增至 256 时，准确率在 128–256 区间出现急剧下降。过大的块大小退化为非半自回归解码，重新引入崩溃风险。

### 效率考量

Table 5 报告了推理效率：HEX（×1 seed，5 个块大小各 1 样本）的单数据点推理时间约为随机解码的 5.2 倍（GSM8K 上 11.98s vs. 2.30s）。这是测试时扩展的固有代价，但与 GRPO 微调的数小时训练成本相比，仍具有显著的资源效率优势。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/022_Table_5.jpg]]
*Table 5: Inference efficiency (in seconds) of HEX (×1 seed) on GSM8K, MATH, ARC-C, TruthfulQA. The numbers in parentheses indicate the number of data points. Random, top-k, and top-k margin use a single sample with a block size of 32. HEX (×1 seed) uses five samples, where each sample is generated with block sizes of 8, 16, 32, 64, and 128. Across all samples, the output length is set to 256, with 2 tokens being unmasked at each step*

### 输出长度的鲁棒性

Table 8 的消融表明，HEX 在输出长度 128 和 256 的设置下均保持一致的性能优势，方法对输出长度具有鲁棒性。Table 6 进一步证实，HEX 的多数投票结果始终优于参与投票的各样本的平均准确率——这从数学上验证了集成学习的核心原理：多样性专家的组合可以超越任何单一专家。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/023_Table_6.jpg]]
*Table 6: HEX (the bottom three rows) consistently surpasses the mean accuracy (the top three rows) of samples used in majority voting across various output length settings. The number preceding [ ] represents the output length, and the numbers inside [ ] correspond to the block sizes used*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/025_Table_8.jpg]]
*Table 8: Ablation study of HEX across output lengths of 128, 256. The results demonstrate that HEX consistently exhibits robust performance irrespective of output length. Block sizes used are the same as Table 6. Refer to Table 4 for detailed explanation about (b), (c), (d)*

### 补充图表

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_L5y7in91vd/figures/026_Table_9.jpg]]

## 方法谱系与知识库定位

### 1. 与现有推理方法的定位关系

HEX 在扩散大语言模型（dLLM）的推理方法谱系中占据一个独特位置：它完全无需训练，却能达到甚至超越基于强化学习微调的方法。

**训练自由基线（Training-free Baselines）**

现有 dLLM 推理方法主要依赖基于置信度的启发式去掩码策略，HEX 揭示了这类策略的根本性缺陷：

- **Top-K / Top-K Margin**：这类方法在每一步选择置信度最高的 K 个 token 进行去掩码。实验表明，Top-K margin 在 GSM8K 上准确率仅为 24.72%，且超过 55.5% 的生成出现灾难性的 [AfterEoT] 崩溃——模型从序列末尾开始逆向生成，最终所有 token 坍缩为 [AfterEoT]（Figure 2）。这暴露了单纯依赖 token 置信度的解码策略在推理任务上的结构性脆弱。
- **Random Unmasking**：随机去掩码反而取得 50.87% 的 GSM8K 准确率，远超 Top-K margin 的 2 倍以上。这一反直觉现象构成了 HEX 的核心动机：随机性带来的多样化可见 token 集合无意中激活了模型内部的不同“专家”，而置信度驱动的方法则系统性地选择了导致崩溃的专家。

**训练依赖基线（Training-based Baselines）**

- **d1 (GRPO)**：Zhao et al., 2025 提出的基于 GRPO 强化学习微调的 dLLM。HEX 在无任何训练的情况下，在 GSM8K（88.10% vs. 79.80%）、MATH（40.00% vs. 37.20%）和 ARC-C（87.80% vs. 82.68%）上均超越了该微调模型（Figure 5）。这表明，测试时扩展（test-time scaling）通过激活隐式专家结构，可以成为一种与训练时优化正交且互补的范式。

### 2. 方法的核心因果机制

HEX 的有效性建立在三个相互关联的因果机制上：

**机制一：隐式专家混合的激活**

扩散语言模型在任意掩码训练（Equation 1）中隐式学习了一个专家混合：每个可能的可见 token 子集 $U$ 定义了一个条件分布 $p_\theta(x_i \mid [x_{\text{prompt}}, x[U]])$，构成一个“隐藏专家”（Equation 3, Section 3）。不同块大小的半自回归调度激活了不同的专家子集——Figure 3 的玩具示例显示，仅改变前三个 token 的掩码状态，第 4 个 token 的预测分布就发生显著变化，某些掩码组合甚至产生语法错误或信息缺失的坍缩分布。

**机制二：半自回归的位置约束消除崩溃**

半自回归解码（块大小 $b < n$）强制从左到右逐块生成，切断了 [AfterEoT] 从序列末尾逆向传播的路径。Table 1 显示，半自回归解码将 [AfterEoT] 崩溃率从 29-56% 降至 0%，GSM8K 准确率从 22.52% 跃升至 76.27%。Figure 8 的可视化进一步揭示：非半自回归（块大小=256）时，模型从最高置信度的末尾 token——恰好是 [AfterEoT]——开始去掩码，并因反复生成相同 token 的惯性最终完全坍缩。

**机制三：多样性聚合的集成效应**

HEX 通过多数投票聚合多个块调度生成的答案，其效果源于结构性多样性而非单纯增加采样。Table 7 的关键消融显示：使用单一块调度（块大小=32）的 25 个样本多数投票，在 GSM8K 上准确率为 75.53%，而 HEX 使用 5 种块调度各 5 个样本（共 25 样本）达到 84.10%，差距达 8.57 个百分点。这表明不同块调度激活了互补的推理路径，其集成效果超越了独立同分布采样的简单平均。

### 3. 适用边界与局限

**已验证的适用范围**

- 模型：仅在 LLaDA-8B-Instruct 上验证
- 任务类型：数学推理（GSM8K、MATH）、常识推理（ARC-C）、真实性判断（TruthfulQA）——均为具有确定性答案的推理任务
- 解码设置：输出长度 256 token，每步去掩码 2 token，温度 0.9

**已知局限**

1. **计算开销**：HEX 需要 25 次独立解码（5 种块大小 × 5 个种子），相比单一解码策略约 5 倍推理成本（Table 5）。虽然可通过减少种子数或动态块数量进行权衡（Table 2 显示 5 个动态调度即可达到 81.96%），但开销仍显著高于单次推理。

2. **块大小的先验选择**：块大小集合 [8, 16, 32, 64, 128] 是预先定义的超参数。Figure 10 显示，块大小在 128-256 范围时性能急剧下降，Figure 11 则表明不同数据点对不同块大小的响应没有一致模式——不存在单一最优块大小。这意味着在实际部署中可能需要针对任务进行调参。

3. **非确定性推理任务的未探索**：论文明确指出 HEX 尚未在开放域生成、故事创作、多轮对话等创造性任务上评估。这些任务缺乏唯一的正确答案，多数投票的适用性存疑。

4. **失败模式**：约 2.96% 的情况下半自回归也会失败（Figure 9），此时去掩码顺序从两端向中间收敛——模型在完整推理前就锁定了答案，先给出结论再补充推导。这种“答案先行”的模式违背了推理的自然逻辑。

### 4. 开放问题

1. **置信度驱动方法退化根源**：为什么基于置信度的 Top-K margin 方法会系统性地选择导致 [AfterEoT] 崩溃的去掩码路径？模型对 [AfterEoT] 的过度自信是训练目标的副产品，还是数据分布的偏差？理解这一现象的根源可能指导更鲁棒的置信度校准方法。

2. **理论分析框架**：HEX 目前缺乏严格的理论解释——为什么隐式专家的多数投票能稳定提升性能？能否建立类似于集成学习中偏差-方差分解的分析框架，或从模式连接性（mode connectivity）角度理解不同块调度激活的专家之间的关系？

3. **自适应块调度**：当前块大小集合是固定的。能否学习一个 prompt 条件的块大小选择策略，或设计在解码过程中动态调整块大小的机制？这将减少调参需求并可能进一步提升性能。

4. **超越确定性答案的任务扩展**：对于故事生成、对话等开放式任务，多数投票不适用。是否可以通过聚合不同专家的生成分布（而非离散答案）来实现测试时扩展，例如使用 Equation 4 中的概率混合而非硬投票？

5. **与其他测试时扩展方法的协同**：HEX 与自回归模型中的 chain-of-thought、self-consistency 等方法在哲学上相似（均通过聚合多条推理路径提升性能），但实现机制迥异。探索这两类方法的交叉融合可能产生更强的推理系统。

## 原文 PDF

![[paperPDFs/ICLR_2026/TEST_TIME_SCALING_IN_DIFFUSION_LLMS_VIA_HIDDEN_SEMI_AUTOREGRESSIVE_EXPERTS.pdf]]
