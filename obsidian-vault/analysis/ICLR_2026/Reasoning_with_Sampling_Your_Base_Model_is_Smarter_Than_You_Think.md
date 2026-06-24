---
title: "Reasoning with Sampling: Your Base Model is Smarter Than You Think"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Reasoning_with_Sampling_Your_Base_Model_is_Smarter_Than_You_Think.pdf
openreview_forum_id: Vsgq2ldr4K
aliases:
- PSA1
- RSYBMISTYT
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "从幂分布 p^α 采样，通过 MCMC 算法迭代地重新采样并基于基模型似然接受或拒绝候选序列，以偏向高似然且具有少量高质量未来路径的 token。"
primary_logic: "幂分布采样隐式地纠正了推理中的“关键 token”错误，它通过考虑未来路径的似然，避免选择那些当前似然虽高但未来路径低质的 token，从而无需任何训练，在单次和多次采样中均达到或超越 RL 后训练模型的推理性能。"
claims:
- "低温度采样不等同于幂分布采样，幂分布更有利于规划未来路径。"
- "在多个基准上，幂采样单次性能匹配甚至超越 GRPO 后训练模型。"
- "幂采样避免了 GRPO 的多样性崩溃，pass@k 表现严格优于 GRPO 和基模型。"
- "幂采样在训练域外任务（HumanEval, AlpacaEval）上表现出更优性能。"
---

# Reasoning with Sampling: Your Base Model is Smarter Than You Think

> [!tip] 核心洞察
> 幂分布采样隐式地纠正了推理中的“关键 token”错误，它通过考虑未来路径的似然，避免选择那些当前似然虽高但未来路径低质的 token，从而无需任何训练，在单次和多次采样中均达到或超越 RL 后训练模型的推理性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 通过采样的推理：你的基模型比你想象得更聪明 |
| 英文题名 | Reasoning with Sampling: Your Base Model is Smarter Than You Think |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=Vsgq2ldr4K) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | Power Sampling (Algorithm 1) |
| Dataset | MATH500, HumanEval, GPQA |

> [!tip] 效果简介
> - MATH500 上，Accuracy 为 0.748，对比 0.496 (Base)，变化 +0.252。
> - HumanEval 上，Accuracy 为 0.573，对比 0.329 (Base)，变化 +0.244。
> - GPQA 上，Accuracy 为 0.389，对比 0.278 (Base)，变化 +0.111。

## 概述

当前大语言模型（LLM）的推理能力主要通过强化学习后训练（如 GRPO, Shao et al., 2024）来提升。然而，这一范式存在两个根本性瓶颈：其一，基模型本身蕴含的推理潜力在常规采样（包括低温度采样）下未被充分利用；其二，强化学习后训练虽然提高了单次推理性能，却以牺牲生成多样性和多尝试（pass@k）性能为代价，且需要大量训练资源和外部验证信号。

本文的核心洞察在于：**通过从幂分布 $p^\alpha$ 采样，可以隐式地纠正推理过程中的“关键 token”错误**。具体而言，幂分布采样会考虑未来路径的似然，避免选择那些当前似然虽高但未来路径低质的 token，从而在不进行任何训练的前提下，使基模型的单次和多尝试推理性能达到甚至超越强化学习后训练模型。

该方法名为 **Power Sampling**，其核心机制是：以基模型自身的似然函数定义目标分布 $p^\alpha$（$\alpha=4.0$），通过 Metropolis-Hastings MCMC 算法迭代地随机重采样并基于似然比率接受或拒绝候选序列。这一过程完全训练无关（training-free），仅依赖基模型的前向传播。

主要实验结果（Table 1）表明：
- 在领域内推理任务（MATH500）上，Power Sampling 与 GRPO 后训练模型性能相当（Qwen2.5-Math-7B: 74.8% vs. GRPO 的 74.8%）；
- 在领域外任务上，Power Sampling 显著优于 GRPO，例如 HumanEval 上提升高达 59.8%（Phi-3.5-mini-instruct），AlpacaEval 2.0 上胜率提升 0.50；
- 在 pass@k 指标上，Power Sampling 严格优于 GRPO 和基模型，且在高 k 值时仍保持与基模型相当的多样性，避免了 GRPO 的多样性崩溃（Figure 5）。

这些结果表明：基模型的推理能力远超常规采样所展现的水平，通过恰当的采样策略即可释放，无需昂贵的强化学习后训练。

## 背景与动机

### 推理能力的“隐性”瓶颈

大型语言模型（LLM）在数学、编程等推理任务上展现出了令人瞩目的能力，但这一能力的释放高度依赖后训练阶段，尤其是强化学习（RL）微调。当前主流的推理范式存在一个显著的矛盾：**基模型本身具备强大的潜在推理能力，但标准的自回归采样策略无法有效将其激发。** 具体而言，直接对基模型进行采样（包括低温度采样）所得到的单次（pass@1）性能远低于经过 RL 后训练的模型，这导致了一种普遍认知——必须通过昂贵的 RL 训练来“注入”推理能力。

然而，本文揭示了这一认知的局限性。问题的真正瓶颈不在于基模型缺乏推理知识，而在于**采样策略未能有效利用模型自身的似然信息来规划高质量的未来路径**。基模型在逐 token 生成时，倾向于选择当前似然最高的 token，但这些“贪婪”的选择可能在长程推理中导向低质量的后续路径——即所谓的“关键 token”决策失误。RL 后训练（如 GRPO）通过显式的奖励信号微调模型参数，迫使模型学会选择那些最终能导向正确答案的 token，从而提升了单次性能，但这带来了两个严重的代价：**多样性崩溃**（模型在多次采样中倾向于生成高度相似的解）和**域外泛化能力下降**。

### 现有方法的缺口

当前解决推理能力瓶颈的方法主要分为两大阵营：

- **基模型采样**（Base model sampling）：直接对预训练或指令微调后的模型进行自回归采样。其优点是零训练成本、维持了完整的生成多样性；缺点是单次推理准确率显著偏低。以 Qwen2.5-Math-7B 为例，基模型在 MATH500 上的准确率仅为 49.6%（见 Table 1），远不能满足实际需求。

- **RL 后训练**（以 GRPO 为代表，Shao et al., 2024）：通过强化学习在特定推理任务上微调模型。其优点是单次性能大幅提升（同模型 GRPO 达到 74.8%），但代价是：需要大量训练计算资源和验证信号；在训练域外任务上性能可能退化（如 HumanEval 上 GRPO 仅 53.7%，甚至低于本文方法的 57.3%）；更重要的是，**pass@k 性能曲线揭示了严重的多样性丧失**——当允许从 k 个样本中选择正确答案时，GRPO 的 pass@k 曲线在高 k 值处显著低于基模型（见 Figure 5），这意味着 GRPO 本质上是通过牺牲解的多样性来换取单次精度的提升。

### 本文的核心动机

上述分析指向一个关键的科学问题：**能否在不进行任何训练的前提下，仅通过改进采样策略，使基模型达到甚至超越 RL 后训练模型的推理性能？**

本文的动机源于一个简洁而深刻的观察：基模型的似然分布本身蕴含了关于解质量的有价值信息——高似然的序列更可能是正确的。问题在于，标准的自回归采样未能充分利用这一信号来“规划”生成过程。如果能够设计一种采样算法，使其偏向于**当前似然高且未来路径同样高质量的 token**，就有可能在不改变模型参数的情况下，显著提升推理性能，同时保持基模型原有的生成多样性。

这一动机直接引出了本文的核心技术路径：**幂分布采样**（Power Sampling）——通过将采样目标从原始分布 $p$ 替换为尖锐化的幂分布 $p^\alpha$（$\alpha > 1$），并利用 MCMC 算法迭代地重新采样和接受/拒绝候选序列，实现对高质量推理路径的有效搜索。该方法完全训练无关，仅依赖基模型自身的似然计算，因此在理论上避免了 RL 后训练所带来的多样性丧失和域外退化问题。

## 核心创新

本工作的核心创新在于**完全绕过强化学习后训练，仅通过推理时的采样策略设计，使基模型释放出被常规采样方式掩盖的潜在推理能力**。其关键突破可归纳为两个层面的“changed slots”：目标分布的重定义，以及采样算法的根本性变革。

### 从“逐 token 采样”到“从幂分布采样”

常规自回归采样（包括低温度采样）直接从模型原始分布 $p$ 或其温度缩放版本中逐 token 生成序列。本文指出，这并非一个有利于推理的采样目标。低温度采样（**Low-temperature sampling**, Wang et al., 2020）虽然通过缩放条件分布来降低随机性，但它在数学上并不等价于从幂分布 $p^\alpha$ 采样（Proposition 1）。更关键的是，两者的行为存在本质差异：低温度采样会提升那些拥有多个但低质量未来路径的 token 的概率，而幂分布采样则**偏向那些拥有少量但高质量未来路径的 token**（Observation 1）。这一差异对于推理任务至关重要——推理中的“关键 token”往往不是当前似然最高的选择，而是能够通往正确后续推理路径的选择。幂分布通过指数化序列联合概率，隐式地纠正了这种“短视”偏差。

### 从“前向生成”到“MCMC 随机重采样”

由于从序列级幂分布 $p^\alpha$ 直接采样是困难的，本文引入了第二个关键变更：用 **Metropolis-Hastings (MH) 算法**替代逐 token 的自回归生成。具体而言，算法从一个初始序列出发，随机选择一个位置，利用基模型作为提议分布重新生成后续 token，然后根据目标分布 $p^\alpha$ 与提议分布的比率计算接受概率：

$$A(\mathbf{x}, \mathbf{x}^i) = \min\left\{1, \frac{p^\alpha(\mathbf{x}) \cdot q(\mathbf{x}^i | \mathbf{x})}{p^\alpha(\mathbf{x}^i) \cdot q(\mathbf{x} | \mathbf{x}^i)}\right\}$$

这一机制的核心在于：**接受/拒绝的决策完全由基模型自身的似然驱动**，无需任何外部奖励信号或训练。通过 $N_{\text{MCMC}}=10$ 步迭代，算法逐步将初始序列“修正”为幂分布下的高概率样本。为缓解初始化质量对 MCMC 混合的影响，方法引入了一系列中间目标分布 $\pi_k(x_{0:kB}) \propto p(x_{0:kB})^{\alpha}$，将序列分块逐步逼近最终目标分布。

### 无训练的“后训练等效”推理

上述两个变更的组合产生了一个令人瞩目的结果：在完全不需要训练数据、奖励模型或策略梯度更新的前提下，幂采样在单次推理性能上**匹配甚至超越 GRPO 后训练模型**（**GRPO**, Shao et al., 2024）。这挑战了“基模型推理能力必须通过 RL 后训练才能充分释放”的既有认知。其本质机制在于，幂分布采样本身就是一种隐式的“test-time search”——它利用基模型对序列整体的似然评估，在推理时进行迭代优化，而 GRPO 则将类似的优化过程固化到了模型参数中。后者的代价是**牺牲了生成多样性**（Figure 5 显示 GRPO 的 pass@k 曲线显著低于基模型），而幂采样在提升单次性能的同时，完整保留了基模型的多样性，使其 pass@k 表现严格优于 GRPO 和基模型。

## 整体框架

Power Sampling 的整体框架围绕一个核心目标展开：从基模型（base model）的原始分布 $p$ 出发，通过无需训练的推理时采样策略，逼近一个经过尖锐化（sharpened）的目标分布 $p^\alpha$（$\alpha > 1$）。该框架的输入是预训练或指令微调后的自回归语言模型，输出是单条推理序列，整个流程由三个关键模块串联而成。

**目标分布定义**：框架首先将推理任务的目标分布定义为幂分布 $p^\alpha$（$\alpha=4.0$）。这一选择的因果机制在于，幂运算会放大高似然序列与低似然序列之间的相对权重——若 $p(\mathbf{x}) > p(\mathbf{x}')$，则 $\frac{p(\mathbf{x})^\alpha}{p(\mathbf{x}')^\alpha} > \frac{p(\mathbf{x})}{p(\mathbf{x}')}$。更重要的是，幂分布在 token 级别的条件分布会偏向那些“未来路径少但质量高”的 token，而非“未来路径多但质量低”的 token，这与低温采样（low-temperature sampling）的行为有本质区别（见 Proposition 1 和 Observation 1）。这一设计隐式地纠正了推理中的“关键 token”错误，构成了整个方法的理论基石。

**MCMC 采样引擎**：由于 $p^\alpha$ 是未归一化的序列级分布，无法直接自回归采样。框架引入 Metropolis-Hastings（MH）算法作为采样引擎，通过“提议—接受/拒绝”的迭代过程逼近目标分布。具体而言，MH 算法从一个随机重采样（random resampling）的提议分布 $q$ 中生成候选序列，然后依据接受概率 $A(\mathbf{x}, \mathbf{x}^i) = \min\left\{1, \frac{p^\alpha(\mathbf{x}) \cdot q(\mathbf{x}^i | \mathbf{x})}{p^\alpha(\mathbf{x}^i) \cdot q(\mathbf{x} | \mathbf{x}^i)}\right\}$ 决定是否接受新序列。提议分布由基模型配合温度 $1/\alpha$ 的采样构成，保证了不可约性和非周期性，从而确保 MH 链收敛到目标分布。

**分块渐进采样**：为避免从随机初始序列出发导致的混合困难，框架将生成过程划分为多个块（block），定义一系列中间目标分布 $\pi_k(x_{0:kB}) \propto p(x_{0:kB})^{\alpha}$（$k=1,2,\dots$），逐步从短序列的幂分布过渡到完整序列的幂分布。在每个块内，执行 $N_{\text{MCMC}}=10$ 步 MH 重采样，仅对当前块内的 token 进行随机重采样和接受/拒绝判断。块大小 $B=192$（最大长度 $T_{\text{max}}=3072$ 下共 16 个块）控制了中间分布之间的跳跃幅度，直接影响混合效率。

**输入输出流**：整个流程以基模型的一次普通自回归采样为起点，生成初始序列。随后，在分块循环中，对每个块执行 MCMC 迭代——提议分布生成候选 token 子序列，MH 接受概率基于基模型似然进行筛选。最终输出一条经过幂分布校正的完整推理序列。值得注意的是，该流程是“单次”（single-shot）的：尽管涉及多次前向传播（约 8.84 倍 token 开销），但接受/拒绝决策完全依赖基模型自身的似然，无需外部奖励信号或验证器，最终产出的仍是一条序列。

三个模块的依赖关系清晰：目标分布定义“采样什么”，MCMC 引擎决定“如何采样”，分块渐进策略解决“如何高效采样”。这一设计使得 Power Sampling 在保持基模型多样性的同时，将采样质量提升至与 RL 后训练相当甚至更优的水平。

## 核心模块与公式推导

### 幂分布：推理的尖锐化目标

本方法的核心目标分布是原始模型分布 $p$ 的幂分布 $p^\alpha$（$\alpha \in [1, \infty]$）。尖锐化的直觉在于：对于任意两个序列 $\mathbf{x}$ 和 $\mathbf{x}'$，若 $p(\mathbf{x}) > p(\mathbf{x}')$，则

$$p(\mathbf{x})^\alpha / p(\mathbf{x}')^\alpha > p(\mathbf{x}) / p(\mathbf{x}')$$

即指数化进一步放大了高似然序列相对于低似然序列的权重（见 Figure 2 的玩具示例）。

**关键洞察**：低温度采样并不等价于从幂分布采样。低温度采样的条件分布为

$$p_{\mathrm{temp}}(x_t | x_0 \dots x_{t-1}) = \frac{p(x_t | x_{t-1} \dots x_0)^\alpha}{\sum_{x_t' \in \mathcal{X}} p(x_t' | x_{t-1} \dots x_0)^\alpha}$$

而幂分布的条件分布为

$$p_{\mathrm{pow}}(x_t | x_0 \ldots x_{t-1}) = \frac{\sum_{x_{>t}} p(x_0, \ldots, x_t, \ldots, x_T)^\alpha}{\sum_{x_{\geq t}} p(x_0, \ldots, x_t, \ldots, x_T)^\alpha}$$

二者的本质区别在于：幂分布会考虑当前 token 之后所有未来路径的似然，从而**偏好那些具有少量但高质量未来路径的 token**；而低温度采样仅基于当前 token 的条件概率缩放，可能偏好那些虽有多条未来路径但每条路径质量较低的 token（Observation 1, Section 4.1）。

---

### MCMC 重采样：从幂分布近似采样

由于幂分布 $p^\alpha$ 是未归一化的序列级分布，无法直接自回归采样。本文采用 Metropolis-Hastings (MH) 算法进行近似采样。MH 的核心是接受概率：

$$A(\mathbf{x}, \mathbf{x}^i) = \min\left\{1, \frac{p^\alpha(\mathbf{x}) \cdot q(\mathbf{x}^i | \mathbf{x})}{p^\alpha(\mathbf{x}^i) \cdot q(\mathbf{x} | \mathbf{x}^i)}\right\}$$

其中：
- $\mathbf{x}^i$ 是当前序列，$\mathbf{x}$ 是候选序列
- $p^\alpha(\cdot)$ 是目标幂分布（未归一化）
- $q(\cdot|\cdot)$ 是提议分布

**提议分布设计**：采用随机重采样策略——随机选取序列中的一个位置 $t$，从该位置起用基模型重新生成后续 token（见 Figure 3）。该提议分布满足不可约性和非周期性，保证了 MH 算法的收敛性。实际实现中，提议 LLM $p_{\text{prop}}$ 选择基模型配合采样温度 $1/\alpha$（Section 5.1）。

---

### 中间目标分布：分块渐进采样

为避免从随机初始化直接跳到 $p^\alpha$ 导致的病态混合问题，算法引入一系列中间目标分布。将序列划分为大小为 $B$ 的块，第 $k$ 个块的中间目标分布为：

$$\pi_k(x_{0:kB}) \propto p(x_{0:kB})^{\alpha}$$

算法从 $k=1$ 开始，逐步在每个块内执行 $N_{\text{MCMC}}$ 步 MH 重采样，逐步逼近最终的 $p^\alpha$。这一分块策略控制了相邻分布之间的跳跃幅度，直接影响混合时间。实验设置中 $T_{\max}=3072$，$B=192$（即 16 个块）。

---

### 推理计算开销

该算法的期望生成 token 数约为

$$\mathbb{E}_{\mathrm{tokens}} = N_{\mathrm{MCMC}} \sum_{k=1}^{\lceil T/B \rceil} \frac{kB}{2} \approx \frac{N_{\mathrm{MCMC}} T^2}{4B}$$

实际测量中，推理计算量约为基模型的 **8.84 倍** tokens（$N_{\text{MCMC}}=10$ 步），但总体成本与 GRPO 单轮训练（16 个 rollouts）相当。

## 实验与分析

### 主结果：单次推理性能对比

Power Sampling 在多个模型家族和任务上进行了系统评估，核心对比对象为基模型（Base）、低温采样（Low-temp）以及 GRPO 后训练模型。Table 1 汇总了主要结果，其核心发现如下：

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_Vsgq2ldr4K/figures/004_Table_1.jpg]]
*Table 1: Power sampling (ours) matches and even outperforms GRPO across model families and tasks. We benchmark the performance of our sampling algorithm on MATH500, HumanEval, GPQA, and AlpacaEval 2.0. We bold the scores of both our method and GRPO, and underline whenever our method outperforms GRPO. Across models, we see that power sampling is comparable to GRPO on in-domain reasoning (MATH500), and can outperform GRPO on out-of-domain tasks*

**域内推理任务（MATH500）**：Power Sampling 在 Qwen2.5-Math-7B 上达到 74.8% 的准确率，与 GRPO（74.8%）完全持平，同时显著超越基模型（49.6%）和低温采样（66.4%）。在 Phi-3.5-mini-instruct 上，Power Sampling（50.8%）甚至超越了 GRPO（40.6%），提升达 +10.2 个百分点。这表明幂分布采样在模型已擅长的数学推理域内，能够匹配 RL 后训练的性能增益。

**域外泛化任务**：Power Sampling 在训练域外任务上展现出明显优势：
- **HumanEval**：Qwen2.5-Math-7B 上达到 57.3%，超越 GRPO（53.7%）+3.6 个百分点，相对基模型（32.9%）提升 +24.4 个百分点。Phi-3.5-mini-instruct 上的差距更为显著——Power Sampling 达到 51.9%，而 GRPO 仅为 32.3%，提升幅度高达 +59.8%。
- **GPQA**：Qwen2.5-Math-7B 上 Power Sampling（38.9%）与 GRPO（40.6%）基本持平，均显著优于基模型（27.8%）。
- **AlpacaEval 2.0**：在不可验证的通用任务上，Power Sampling 的胜率达到 2.88，超越 GRPO（2.38）+0.50，进一步验证了该方法在非推理任务上的泛化能力。

**关键洞察**：GRPO 在 MATH 训练集上进行了专门的后训练，而 Power Sampling 完全无需任何训练数据。即便如此，Power Sampling 在域内匹配 GRPO，在域外则持续超越。这揭示了基模型本身蕴含的推理能力远超常规采样所能释放的水平，而 RL 后训练在提升单次性能的同时，可能牺牲了模型在分布外任务上的泛化性。

### 多样性保持：Pass@k 分析

Figure 5 展示了 MATH500 上的 pass@k 性能曲线（k 从 1 到 64）。Power Sampling 的曲线严格位于基模型和 GRPO 之上，且在高 k 值时 pass rate 与基模型持平，表明其保持了与基模型相当的生成多样性。相比之下，GRPO 的 pass@k 曲线在 k 增大时趋于平缓，呈现出典型的多样性崩溃特征——RL 后训练使模型过度集中于少数高奖励模式，丧失了探索不同解题路径的能力。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_Vsgq2ldr4K/figures/007_Figure_5.jpg]]
*Figure 5: Pass@k performance on MATH500. We plot the pass@k accuracy (correct if at least one of k samples is accurate) of power sampling (ours) and RL (GRPO) relative to the base model (Qwen2.5-Math-7B). Our performance curve is strictly better than both GRPO and the base model, and our pass rate at high k matches the base model, demonstrating sustained generation diversity*

这一现象在 HumanEval（Figure 8）和 GPQA（Figure 9）上同样得到验证。Power Sampling 在保持单次高性能的同时，通过多次采样仍能持续获得收益，这在实际部署中具有重要意义：当允许多次尝试时，Power Sampling 的优势会进一步放大。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_Vsgq2ldr4K/figures/010_Figure_8.jpg]]
*Figure 8: Pass@k performance on HumanEval (Qwen2.5-Math-7B)*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_Vsgq2ldr4K/figures/011_Figure_9.jpg]]
*Figure 9: Pass@k performance on GPQA (Qwen2.5-Math-7B)*

### 似然与置信度分布分析

Figure 4 对比了基模型、Power Sampling 和 GRPO 在 MATH500 上生成序列的对数似然和模型置信度分布。GRPO 的生成序列集中在最高似然和最高置信度区域，而 Power Sampling 的分布紧随其后，同样偏向高似然区域，但保留了一定的分布宽度。这与准确率的提升呈正相关：幂分布采样通过 MCMC 接受/拒绝机制，隐式地筛选出那些在当前 token 选择上具有更高质量未来路径的序列，而非简单追求局部似然最大化。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_Vsgq2ldr4K/figures/006_Figure_4.jpg]]
*Figure 4: Base model (Qwen2.5-Math-7B) likelihoods and confidences for MATH500 responses. Left: We plot the log-likelihoods (relative to the base model) of original, power sampling, and GRPO responses over MATH500. Right: We do the same but for confidences relative to the base model. We observe that GRPO samples from the highest likelihood and confidence regions with power sampling close behind, which correlates with higher empirical accuracy*

模型置信度定义为序列上各 token 分布负熵的均值：

$$\mathrm{Conf}(x_{0:T}) = \frac{1}{T+1} \sum_{t=0}^{T} \sum_{x \in \mathcal{X}} p(x | x_{<t}) \log p(x | x_{<t})$$

置信度越高，表明模型在生成每一步时对所选 token 越“确定”。Power Sampling 在提升置信度的同时避免了 GRPO 的过度集中，这与其核心机制一致：幂分布 $p^\alpha$ 偏向那些具有少量但高质量未来路径的 token，而非多个低质量路径的 token。

### 超参数消融

**幂指数 $\alpha$**：Figure 6（左）展示了 $\alpha$ 在 $\{1, 2, 4, 8, 16\}$ 范围内对 MATH500 准确率的影响。$\alpha=4.0$ 在两个模型家族上均达到或接近最优，且 $\alpha \geq 2.0$ 后性能相对稳定。$\alpha=1$ 退化为基模型采样，性能最低；过大的 $\alpha$（如 16）可能导致分布过于尖锐，反而损害性能。

**MCMC 步数 $N_{\text{MCMC}}$**：Figure 6（右）展示了 MCMC 步数从 0 增加到 20 的影响。从 0 步（等价于直接低温采样）到 2 步带来了约 3-4% 的显著跳跃，验证了 MCMC 随机重采样机制的核心作用。步数继续增加到 10 时准确率稳步提升，之后趋于饱和。这一饱和行为表明，MCMC 链在约 10 步后已充分混合，额外的计算投入不再带来显著收益。

### 失败模式与公平性说明

**计算开销**：Power Sampling 的推理成本约为基模型的 8.84 倍 tokens（$N_{\text{MCMC}}=10$，$B=192$，$T_{\text{max}}=3072$）。这一开销与 GRPO 训练中单轮 16 个 rollouts 的推理量相当，但 Power Sampling 无需任何训练阶段。对于延迟敏感场景，这一开销可能构成限制。

**GRPO 的格式错误问题**：在 Phi-3.5-mini-instruct 的 HumanEval 评估中，GRPO 的失败案例中有 76.05% 归因于缩进格式错误（Table 2 示例），而 Power Sampling 未出现此类问题。这暗示 RL 后训练可能引入了对特定格式的过拟合，在域外任务上表现为脆性。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_Vsgq2ldr4K/figures/005_Table_2.jpg]]
*Table 2: Sample responses on HumanEval: Phi-3.5-mini-instruct. We present an example where our method solves a simple coding question, but GRPO does not. 5.3 ANALYSIS*

**方法适用范围**：当前实验仅覆盖 7B 参数规模的模型（Qwen2.5-Math-7B、Phi-3.5-mini-instruct），对更大模型的效果尚未验证。此外，幂采样依赖基模型的序列似然作为唯一信号，对于需要高度创造性或多样性的生成任务，纯粹的似然最大化策略可能不适用。

### 定性案例

Table 2 展示了 HumanEval 上的典型案例：Phi-3.5-mini-instruct 的 GRPO 版本因缩进错误未能通过测试，而 Power Sampling 成功生成了正确代码。Table 5 展示了 MATH500 上 GRPO 给出错误答案而 Power Sampling 成功的案例——后者采用了一种完全不同的解题方法，体现了幂分布采样在探索不同推理路径上的优势。Table 3 则展示了两者均正确的案例，表明在模型已有较强能力的任务上，两种方法可以达成一致的正确答案。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_Vsgq2ldr4K/figures/014_Table_5.jpg]]
*Table 5: MATH500 comparison between our sampling algorithm and GRPO for Qwen2.5-Math-7B. Here is an example where GRPO gets an incorrect answer, while our sampling algorithm succeeds. Our sample answer uses a distinct method altogether*

### 补充图表

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_Vsgq2ldr4K/figures/001_Figure_1.jpg]]
*Figure 1: Our sampling algorithm can match and outperform RL-posttraining. Left: we compare our sampling algorithm (ours) against the base model (base) and RL-posttraining (GRPO) on three verifiable reasoning tasks (MATH500, HumanEval, GPQA). Right: we compare them on an unverifiable general task (AlpacaEval2.0). Our algorithm achieves comparable performance to GRPO within the posttraining domain (MATH500) but can outperform on out-of-domain tasks such as HumanEval and AlpacaEval*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_Vsgq2ldr4K/figures/012_Table.jpg]]

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_Vsgq2ldr4K/figures/013_Table_4.jpg]]
*Table 4: HumanEval comparison on Phi-3.5-mini-instruct*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_Vsgq2ldr4K/figures/009_Figure_7.jpg]]
*Figure 7: Pass@k performance on MATH500 (Qwen2.5-Math-7B)*

## 方法谱系与知识库定位

### 1. 方法在推理增强谱系中的位置

本工作处于**推理时计算扩展**与**免训练推理增强**的交叉点。与主流的强化学习后训练（RL-posttraining）范式形成直接对比。

**基线方法关系：**

- **基模型采样（Base model sampling）**：直接自回归采样是本方法的起点。论文揭示基模型本身蕴含的推理能力远未被常规采样充分利用——低温度采样并非幂分布采样的有效近似（Proposition 1），因为低温度采样会提升“当前似然高但未来路径低质”的 token，而幂分布采样偏向“未来路径少但质量高”的 token（Observation 1）。

- **GRPO**（Shao et al., 2024）：作为标准 RL 后训练方法，GRPO 通过训练改变模型参数来提升单次推理性能。本方法以零训练成本达到与 GRPO 相当甚至更优的性能：在 MATH500 上匹配 GRPO，在 HumanEval 上以 +59.8% 的幅度超越 GRPO（Table 1, Phi-3.5-mini-instruct）。更关键的是，GRPO 存在**多样性崩溃**问题——其 pass@k 曲线在高 k 时显著低于基模型，而幂采样在高 k 时保持与基模型一致的多样性（Figure 5）。

- **低温度采样**（Wang et al., 2020）：论文通过 Proposition 1 严格证明了低温度采样不等同于从幂分布 $p^\alpha$ 采样。低温度采样在每个 token 位置独立进行温度缩放，而幂分布考虑完整序列的联合似然，隐式地执行了“未来路径规划”。

**方法谱系定位：**

本方法可归入基于 MCMC 的推理时采样优化家族。其核心创新在于：

1. **目标分布选择**：将 $p^\alpha$ 作为采样目标，利用指数化放大高似然区域的权重；
2. **采样算法设计**：采用 Metropolis-Hastings 框架，通过随机重采样提议分布实现对长序列的有效探索；
3. **中间分布调度**：引入分块策略（block size $B=192$），逐步从局部幂分布过渡到全局幂分布，避免初始化病态问题。

### 2. 适用边界

**已验证的适用场景：**

- **数学推理**：MATH500 上 Qwen2.5-Math-7B 从 0.496 提升至 0.748（+25.2%），Phi-3.5-mini-instruct 从 0.444 提升至 0.508（+6.4%）。
- **代码生成**：HumanEval 上 Qwen2.5-Math-7B 从 0.329 提升至 0.573（+24.4%），Phi-3.5-mini-instruct 从 0.079 提升至 0.598（+51.9%）。
- **科学问答**：GPQA 上 Qwen2.5-Math-7B 从 0.278 提升至 0.389（+11.1%）。
- **开放域生成**：AlpacaEval 2.0 上 Win Rate 从基模型的 2.38 提升至 2.88，超越 GRPO 的 2.38。

**适用条件：**

- 模型规模：当前仅在 7B 级别模型（Qwen2.5-Math-7B、Phi-3.5-mini-instruct）上验证；
- 任务类型：适用于存在“关键 token”决策的推理任务，即某些 token 的选择会显著影响后续路径质量；
- 计算预算：需要约 8.84 倍 tokens 的推理开销（$N_{\text{MCMC}}=10$ 步重采样），适合对延迟不敏感但追求高质量的场景。

**不适用的边界：**

- 低延迟场景：8.84 倍的推理计算量使其不适用于实时交互；
- 创造性生成：幂分布天然偏向高似然区域，可能抑制低概率但富有创意的输出；
- 超大规模模型：在 70B 及以上模型上的效果和计算可行性尚未验证。

### 3. 局限与开放问题

**已知局限：**

1. **推理计算开销**：$N_{\text{MCMC}}=10$ 步重采样产生约 8.84 倍 tokens 的计算量（Section A.3）。虽然论文指出总成本与 GRPO 单轮训练（16 个 rollouts）相当，但这是训练成本与推理成本的比较，对于纯推理场景，开销仍然显著。

2. **超参数敏感性**：幂指数 $\alpha$ 和 MCMC 步数 $N_{\text{MCMC}}$ 需要针对任务调整。消融实验（Figure 6）显示 $\alpha=4.0$ 在 MATH500 上最优，且 $\alpha \geq 2.0$ 后性能相对稳定；MCMC 步数从 0 增加到 10 持续提升准确率后趋于饱和。但尚未证明这些设置在更广泛任务上的普适性。

3. **模型规模限制**：仅在 7B 参数规模上验证。更大模型（如 70B、405B）的似然分布特性可能不同，幂采样的效果和计算可行性需要进一步探索。

4. **依赖基模型似然质量**：方法完全依赖基模型的序列似然作为质量信号。若基模型在某些领域存在系统性偏差，幂分布采样会放大这些偏差。

**开放问题：**

1. **规模扩展性**：幂采样能否在 70B/405B 级别模型上保持性能优势？更大模型的似然分布是否更有利于幂采样，还是会引入新的挑战？

2. **与 RL 后训练的协同**：能否将幂采样作为 RL 后训练的初始化策略或数据增强手段？论文暗示两者在目标上互补——幂采样保持多样性，RL 后训练提升单次精度——但未探索结合路径。

3. **高效 MCMC 策略**：当前随机重采样提议分布较为朴素。是否可以通过更智能的提议分布（如基于模型置信度的自适应重采样）或更高效的 MCMC 变体（如 Hamiltonian MCMC 的离散版本）进一步降低推理成本？

4. **非推理任务适用性**：在创意写作、对话生成等多样性要求高的任务上，幂分布的“尖锐化”倾向是否会产生负面影响？是否可以通过调整 $\alpha$ 或提议分布温度来平衡质量与多样性？

5. **理论分析深化**：Proposition 1 揭示了低温度采样与幂分布采样的本质区别，但幂分布采样为何在推理任务中优于低温度采样的理论机制（特别是“未来路径规划”效应）仍需更严格的形式化分析。

## 原文 PDF

![[paperPDFs/ICLR_2026/Reasoning_with_Sampling_Your_Base_Model_is_Smarter_Than_You_Think.pdf]]
