---
title: "$\\nabla$-Reasoner: LLM Reasoning via Test-Time Gradient Descent in Latent Space"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/nabla_Reasoner_LLM_Reasoning_via_Test_Time_Gradient_Descent_in_Latent_Space.pdf
aliases:
- NRLRTTGDLS
- "∇-Reasoner"
tags:
- ICLR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: "将推理时扩展从零阶搜索范式转变为**一阶优化**范式：利用奖励模型和语言模型自身的可微性，在解码循环中对token logits进行梯度下降优化，从而获得方向性的搜索引导。"
primary_logic: "推理时对样本空间进行梯度下降以最大化奖励，与通过KL正则化强化学习对齐LLM策略是**对偶的**。因此，无需额外训练，即可在测试时通过可微文本优化（DTO）模拟策略优化过程，实现策略的即时改进。"
claims:
- "∇-Reasoner在数学推理基准上相比强基线实现了超过20%的准确率提升。"
- "∇-Reasoner将模型调用次数减少了约10-40%。"
- "定理4.1：对Eq.2进行Wasserstein梯度流采样等价于最小化KL正则化PPO目标Eq.3的最优分布。"
- "MATH-500 上 Accuracy (%) = 71.0"
---

# $\nabla$-Reasoner: LLM Reasoning via Test-Time Gradient Descent in Latent Space

> [!tip] 核心洞察
> 推理时对样本空间进行梯度下降以最大化奖励，与通过KL正则化强化学习对齐LLM策略是**对偶的**。因此，无需额外训练，即可在测试时通过可微文本优化（DTO）模拟策略优化过程，实现策略的即时改进。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ∇-Reasoner：通过测试时潜在空间梯度下降实现大语言模型推理 |
| 英文题名 | $\nabla$-Reasoner: LLM Reasoning via Test-Time Gradient Descent in Latent Space |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=pEJAja73dk); [GitHub](https://github.com/VITA-Group/Nabla-Reasoner) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | ∇-Reasoner |
| Dataset | MATH-500, AMC |

> [!tip] 效果简介
> - MATH-500 上，Accuracy (%) 为 71.0，对比 N/A (Qwen-2.5-7B base model, best test-time baseline comparison in Table 1)，变化 N/A。
> - MATH-500 上，Accuracy (%) 为 80.4，对比 N/A (Qwen-2.5-7B-Instruct, best test-time baseline comparison in Table 1)，变化 N/A。
> - MATH-500 上，Accuracy (%) 为 55.8，对比 N/A (Llama-3.1-8B-Instruct, best test-time baseline comparison in Table 1)，变化 N/A。

## 概述

本文提出 **∇-Reasoner**，一种将推理时扩展从零阶搜索范式转变为一阶优化范式的新方法。现有方法（如 Best-of-N、Tree-of-Thoughts、Reasoning-as-Planning）在离散 token 空间进行采样和评估，仅依赖标量奖励值，在高维空间中搜索效率低且易饱和。∇-Reasoner 的核心洞察在于：**测试时对样本空间进行梯度下降以最大化奖励，与通过 KL 正则化强化学习对齐 LLM 策略在数学上是对偶的**（定理 4.1）。因此，无需额外训练，即可在解码循环中通过可微文本优化（DTO）模拟策略优化过程，实现策略的即时改进。

方法上，∇-Reasoner 在每一步解码中：1）从基础 LLM 生成初始响应及其逐 token logits；2）通过 DTO 在 logit 空间进行梯度下降，优化联合了奖励函数和序列对数似然的损失函数 $\mathcal{L}(\mathbf{y}) := -\lambda r(\mathbf{y}|\mathbf{x}) - \log \pi_{LLM}(\mathbf{y}|\mathbf{x})$；3）结合拒绝采样接受能产生更高奖励续写的 token。梯度分解为前缀项、后缀项和奖励项，展示了双向梯度传播机制。为提升效率，论文提出了梯度缓存、轨迹复用和置信度/梯度引导的 token 选择等加速策略。

在数学推理基准（MATH-500、AMC、AIME-24、AIME-25）上的实验表明，∇-Reasoner 相比强基线实现了超过 20% 的准确率提升，同时将模型调用次数减少了约 10-40%。在 Qwen-2.5-7B-Instruct 上，MATH-500 准确率达到 80.4%，AMC 达 56.8%，AIME-24 达 26.7%，AIME-25 达 20.0%，超越了所有测试时基线方法，甚至与基于训练的方法（SFT、GRPO）性能相当。消融研究显示，使用较小的 4B 奖励模型不会导致显著性能下降（差距低于 1 个百分点），DTO 显著降低了拒绝采样中的拒绝率（降低高达 30% 以上），加速策略分别绕过了 63.8% 的模型调用、消除了 74.1% 的自回归调用并避免了 89.2% 的 token 优化步骤。

## 背景与动机

大语言模型（LLM）在推理任务上的性能提升，正从单纯扩大模型规模转向“推理时扩展”（inference-time scaling）——即在测试阶段分配更多计算资源以换取更优输出。然而，当前主流的推理时扩展方法，如 Best-of-N (BoN)、Self-Consistency (SC)、Tree-of-Thoughts (ToT) 和 Reasoning-as-Planning (RAP)，本质上都是**零阶搜索算法**。它们的行为模式高度一致：从基础策略采样大量候选响应，仅依赖最终的标量奖励值对其进行评估和筛选。这种范式的根本瓶颈在于，高维离散的token序列空间随着推理链长度呈指数级膨胀，而零阶方法缺乏方向性引导，只能依靠暴力采样来“碰运气”。奖励信号在这一过程中变得稀疏且噪声大，导致搜索效率低下，性能容易过早饱和。

∇-Reasoner 的核心动机是将推理时扩展从零阶搜索范式彻底转变为**一阶优化范式**。其关键洞察在于：利用奖励模型和语言模型自身的可微性，在解码循环中对token logits进行梯度下降优化，从而获得方向性的搜索引导。这相当于在奖励景观（reward landscape）上，从盲目的随机采样升级为沿着梯度方向“爬坡”，从根本上提升了搜索的信息效率。

这一转变不仅是一个工程技巧，更有深厚的理论支撑。论文的核心定理（Theorem 4.1）揭示了：在推理时对样本空间进行梯度下降以最大化奖励，等价于最小化KL正则化PPO目标的最优分布采样过程。换言之，∇-Reasoner 在无需额外训练的情况下，通过可微文本优化（DTO）在测试时即时模拟了策略优化过程，实现了“去摊销”（deamortized）的策略改进。这一理论联系将测试时搜索与训练时强化学习统一在了同一框架下，为推理时扩展提供了全新的理论视角。

实验证据有力地支撑了这一动机的合理性。在具有挑战性的数学推理基准上，∇-Reasoner 相比强基线实现了超过20%的准确率提升，同时将模型调用次数减少了约10-40%。在MATH-500基准上，使用Qwen-2.5-7B-Instruct模型时，∇-Reasoner达到了80.4%的准确率，甚至与基于训练的方法（如SFT和GRPO）性能相当。这些结果共同表明，将推理时扩展从零阶提升到一阶，不仅可行，而且能同时带来性能提升和计算效率改善。

## 核心创新

∇-Reasoner的核心贡献在于将推理时计算扩展从**零阶搜索范式**根本性地转向**一阶优化范式**。现有方法（如Best-of-N、Tree-of-Thoughts、Reasoning-as-Planning）在高维离散token空间中仅依赖标量奖励值进行探索，随着推理链增长，搜索空间指数级扩大，奖励信号稀疏且噪声大，性能容易饱和。∇-Reasoner通过利用奖励模型和语言模型自身的可微性，在解码循环中对token logits进行梯度下降优化，从而获得方向性的搜索引导。

**关键改动点：**

- **搜索范式**：从“零阶搜索”（仅依赖奖励值采样评估）变为“一阶优化”（利用奖励梯度提供方向性引导）。如图1所示，传统方法在奖励景观上随机采样，而∇-Reasoner沿着梯度方向直接优化。
- **优化对象**：从离散token序列变为连续logit向量。DTO（Differentiable Textual Optimization）在logit空间进行梯度下降，优化联合了奖励函数和序列对数似然的损失函数 $\mathcal{L}(\mathbf{y}) := -\lambda r(\mathbf{y}|\mathbf{x}) - \log \pi_{LLM}(\mathbf{y}|\mathbf{x})$，其中负对数似然项作为KL正则化，约束优化后的响应保持流畅性和忠实性。
- **策略更新方式**：从拒绝采样/投票（无梯度信息）变为通过DTO更新logits后从更新后的分布中采样。每次解码时，先对当前token的logits进行多步梯度下降，再将优化后的logits视为改进策略进行采样。
- **计算效率策略**：引入梯度缓存（绕过63.8%模型调用）、轨迹复用（消除74.1%自回归调用）、置信度与梯度引导的token选择（避免89.2%的token优化步骤）等系统协同设计，使∇-Reasoner在模型调用次数上相比强基线减少10-40%。

**理论核心洞察**：定理4.1建立了推理时梯度下降与强化学习的对偶关系——对Eq.2进行Wasserstein梯度流采样等价于最小化KL正则化PPO目标Eq.3的最优分布。这意味着∇-Reasoner在测试时通过可微文本优化模拟了策略优化过程，实现了无需额外训练的即时策略改进。

## 整体框架

![[assets/figures/papers/iclr26_0001_pEJAja73dk_nabla-Reasoner_LLM_Reasoning_via_Test-Time_Gradi/figures/005_Figure_3.jpg]]
*Figure 3: A comparison of computational cost, measured by the number of model calls. Our method reduces costs by up to 40.2% compared to baselines*

∇-Reasoner 将推理时计算扩展从传统的零阶搜索范式转变为一种**一阶优化**范式，其核心思想是在解码循环中对 token logits 进行梯度下降，从而获得方向性的搜索引导。其整体 pipeline 由三个核心模块构成：初始生成、可微文本优化（DTO）和拒绝采样，并辅以一系列系统级加速策略以提高解码吞吐量。

**流程描述：**

1.  **初始生成 (Initial Rollout)**：在每一步解码时，基础 LLM 首先生成一个完整的响应，并同时输出其逐 token 的 logits。这组 logits 构成了后续优化的起点。
2.  **可微文本优化 (DTO)**：这是 ∇-Reasoner 的核心模块。DTO 在连续的 logit 空间中对初始 logits 进行梯度下降，以优化一个联合了奖励函数和序列对数似然的损失函数 $\mathcal{L}(\mathbf{y}) := -\lambda r(\mathbf{y}|\mathbf{x}) - \log \pi_{LLM}(\mathbf{y}|\mathbf{x})$。通过这种方式，DTO 利用来自 LLM 自身似然和奖励模型的梯度信号来精细化文本表示，从而获得一个“改进后”的策略。
3.  **拒绝采样 (Rejection Sampling)**：在从 DTO 优化后的策略采样下一个 token 后，系统会评估该 token 是否能产生一个更高奖励的续写。如果能够，则接受；否则，回退到原始 LLM 策略的初始选择。这确保了优化过程不会产生退化。
4.  **加速策略 (Acceleration Strategies)**：为了降低计算成本，∇-Reasoner 集成了多种系统协同设计策略。这些策略包括：**梯度缓存**，它绕过了超过 63.8% 的模型调用；**轨迹复用**，它消除了超过 74.1% 的自回归模型调用；以及**置信度与梯度引导的 token 选择**，它有效避免了 89.2% 的 token 优化步骤。这些策略共同将模型调用次数相比强基线减少了约 10-40%，最高可达 40.2%。

**模块关系与输入输出流：**

整个 pipeline 是一个迭代解码过程。在每个解码步，输入是当前的 prompt 和已生成的 token 前缀。初始生成模块输出完整的响应及其 logits。DTO 模块接收这些 logits 作为输入，输出优化后的 logits。拒绝采样模块比较从原始策略和优化后策略采样的结果，并决定最终输出的 token。加速策略模块则作为跨模块的优化层，通过选择性跳过或复用计算来减少不必要的模型调用。该框架能够无缝整合过程奖励（process reward），只需将奖励函数 $r(\mathbf{y}|\mathbf{x})$ 替换为广义版本 $R(\mathbf{y}|\mathbf{x}) = \Sigma_{l=1}^{|\mathbf{y}|} r(\mathbf{y}_{\leq l}|\mathbf{x})$。

**理论支撑：**

论文的核心理论洞见在于，推理时对样本空间进行梯度下降以最大化奖励，与通过 KL 正则化强化学习（如 PPO）对齐 LLM 策略是**对偶的**。定理 4.1 严格证明了，对 DTO 目标函数进行 Wasserstein 梯度流采样，等价于最小化 KL 正则化 PPO 目标的最优分布。这意味着，无需额外训练，即可在测试时通过 DTO 模拟策略优化过程，实现策略的即时改进。

## 核心模块与公式推导

### 核心模块：可微文本优化（DTO）

∇-Reasoner 的核心创新在于将推理时扩展从零阶搜索（如 BoN、ToT）转变为**一阶优化**。其核心模块是**可微文本优化（Differentiable Textual Optimization, DTO）**。

DTO 的工作流程如下：在每个解码步骤，语言模型首先生成一个完整的续写及其逐 token logits，作为初始展开。随后，DTO 在 logit 空间（词汇表的连续松弛）中对这些 logits 执行梯度下降，以优化一个联合了奖励函数和序列对数似然的损失函数。优化后的 logits 被用作改进的策略，然后从中采样下一个 token。该方法还集成了拒绝采样：仅当从优化后策略采样的 token 能产生更高奖励的续写时才接受它；否则回退到原始选择。

### 核心公式与变量含义

**1. DTO 目标函数**

$$\mathcal{L}(\mathbf{y}) := -\lambda r(\mathbf{y}|\mathbf{x}) - \log \pi_{LLM}(\mathbf{y}|\mathbf{x})$$

-   $\mathcal{L}(\mathbf{y})$：待最小化的损失函数，作用于整个响应序列 $\mathbf{y}$。
-   $r(\mathbf{y}|\mathbf{x})$：给定提示 $\mathbf{x}$ 下，对响应 $\mathbf{y}$ 的奖励函数（可以是结果奖励或过程奖励）。
-   $\pi_{LLM}(\mathbf{y}|\mathbf{x})$：基础语言模型生成响应 $\mathbf{y}$ 的概率。
-   $\lambda$：平衡奖励项与对数似然项的超参数。该目标结合了负奖励和负对数似然，在优化过程中约束响应保持流畅和忠实于基础模型。

**2. Logit 更新规则**

$$\mathbf{z}^{(t+1)} = \mathbf{z}^{(t)} - \eta \nabla_{\mathbf{z}} \bar{\mathcal{L}}(\bar{\mathbf{z}}^{(t)})$$

-   $\mathbf{z}^{(t)}$：第 $t$ 次迭代时的 logits 向量。
-   $\eta$：学习率，控制梯度下降的步长。
-   $\nabla_{\mathbf{z}} \bar{\mathcal{L}}(\bar{\mathbf{z}}^{(t)})$：损失函数关于 logits 的梯度。

**3. 梯度分解**

$$\frac{\partial \mathcal{L}}{\partial y_i} = - \underbrace{\log \mathrm{Cat}\left(\pi_{LLM}(\cdot|y_{\leq i-1}, \mathbf{x})\right)}_{\delta_{prefix}} - \underbrace{\sum_{j=i+1}^{|y|} \frac{\partial \log \mathrm{Cat}\left(\pi_{LLM}(\cdot|y_{\leq j-1}, \mathbf{x})\right)}{\partial y_i} \mathbf{x}}_{\delta_{postfix}} - \lambda \underbrace{\frac{\partial r(y|\mathbf{x})}{\partial y_i}}_{\delta_{reward}}$$

-   $\frac{\partial \mathcal{L}}{\partial y_i}$：损失函数 $\mathcal{L}$ 关于第 $i$ 个 token $y_i$ 的梯度，被分解为三个部分：
    -   $\delta_{prefix}$：**前缀项**，来自 token $y_i$ 自身的对数似然梯度，鼓励优化后的 token 保持高概率。
    -   $\delta_{postfix}$：**后缀项**，来自所有后续 token 的对数似然对 $y_i$ 的梯度，体现了双向梯度传播——修改当前 token 会影响后续 token 的生成概率。
    -   $\delta_{reward}$：**奖励项**，来自奖励函数对 $y_i$ 的梯度，引导 token 向能提高最终奖励的方向移动。

**4. 理论联系：KL 正则化 PPO 目标**

$$\mathcal{L}_{PPO}(\rho) := - \mathbb{E}_{\mathbf{y} \sim \rho}[\lambda r(\mathbf{y})] + D_{KL}(\rho || \pi_{LLM})$$

-   $\mathcal{L}_{PPO}(\rho)$：KL 正则化的 PPO 目标。
-   $\rho$：待优化的策略分布。
-   $\mathbb{E}_{\mathbf{y} \sim \rho}[\lambda r(\mathbf{y})]$：在分布 $\rho$ 下期望的奖励。
-   $D_{KL}(\rho || \pi_{LLM})$：分布 $\rho$ 与基础策略 $\pi_{LLM}$ 之间的 KL 散度。

**定理 4.1** 建立了 DTO 与 PPO 的理论联系：对 Eq.2（DTO 目标）进行 Wasserstein 梯度流采样，等价于最小化 KL 正则化 PPO 目标 Eq.3 的最优分布。这意味着，无需额外训练，即可在测试时通过 DTO 模拟策略优化过程，实现策略的即时改进。

**5. Softmax 变换与 Logit 梯度**

$$\pmb{x}_i = \frac{\exp(z_i)}{\sum_{j=1}^{|\mathcal{V}|}\exp(z_j)}$$

$$\frac{\partial \mathcal{L}}{\partial z_i} = \pmb{x}_i \left( \left[ \frac{\partial \mathcal{L}}{\partial \pmb{x}} \right]_i - \pmb{x}^\top \frac{\partial \mathcal{L}}{\partial \pmb{x}} \right)$$

-   $\pmb{x}_i$：第 $i$ 个 token 经过 Softmax 变换后的概率。
-   $z_i$：第 $i$ 个 token 的 logit。
-   $\frac{\partial \mathcal{L}}{\partial z_i}$：损失关于 logit $z_i$ 的导数。其大小与 Softmax 后概率 $\pmb{x}_i$ 成正比，这为**置信度引导的 token 选择**提供了理论依据：梯度幅度较小的 token（即高置信度 token）可以被跳过优化，从而加速解码。

## 实验与分析

### 主结果：数学推理准确率显著提升

∇-Reasoner 的核心实验在多个数学推理基准上展开，验证了其作为一阶优化范式的有效性。如表 1 所示，在 MATH-500 基准上，使用 Qwen-2.5-7B 基础模型时，∇-Reasoner 达到了 71.0% 的准确率；使用 Qwen-2.5-7B-Instruct 时，准确率进一步提升至 80.4%；在 Llama-3.1-8B-Instruct 上则为 55.8%。在更具挑战性的 AMC、AIME-24 和 AIME-25 数据集上（均使用 Qwen-2.5-7B-Instruct），∇-Reasoner 分别取得了 56.8%、26.7% 和 20.0% 的准确率。论文明确指出，∇-Reasoner 在数学推理基准上相比强基线实现了**超过 20% 的准确率提升**（decisive_evidence 中置信度为 1.0 的声明），并且其性能与基于训练的方法（如 SFT 和 GRPO）相当，这标志着测试时计算扩展从零阶搜索到一阶优化的范式转变带来了实质性的收益。


![[assets/figures/papers/iclr26_0001_pEJAja73dk_nabla-Reasoner_LLM_Reasoning_via_Test-Time_Gradi/figures/002_Table_1.jpg]]
*Table 1: Accuracy (%) on math reasoning datasets compared with baseline methods, including both test-time and training-time approaches. We skip results on AIME datasets for Llama-3.1-8B as it is incapable of generating reasonable performance. We mark the best performer in bold and the runner-up with underline. Our method outperforms all test-time baselines and even achieves performance on par with the training-based methods (SFT and GRPO), respectively*

### 计算效率：模型调用次数大幅降低

∇-Reasoner 的核心优势不仅在于性能，更在于效率。如图 3 所示，通过系统协同设计（梯度缓存、轨迹复用、置信度与梯度引导的 token 选择），∇-Reasoner 将模型调用次数减少了约 **10-40%**（decisive_evidence 中置信度为 1.0 的声明），最高可达 40.2%。这一效率提升的机制是：梯度缓存绕过了超过 63.8% 的模型调用（ablations 中置信度为 1.0），轨迹复用了消除了超过 74.1% 的自回归模型调用（ablations 中置信度为 1.0），而 token 选择策略则有效避免了 89.2% 的 token 优化步骤（ablations 中置信度为 1.0）。这些加速策略共同作用，使得一阶优化的额外计算开销被有效抵消。

### 测试时扩展定律：梯度引导的搜索优势

图 4 展示了 ∇-Reasoner 与 BoN 和 SC 的测试时扩展曲线。通过改变 BoN 和 SC 的采样数量 N 以及 ∇-Reasoner 的 rollout 数量 N_max，可以观察到：**在任何给定的计算预算下，∇-Reasoner 的准确率曲线始终位于基线之上**。这表明梯度引导的搜索不仅更高效，而且具有更好的扩展性——随着计算预算的增加，一阶优化方法能够更有效地利用额外的计算资源，而零阶方法则更容易陷入性能饱和。这验证了核心因果机制：从零阶搜索到一阶优化的转变，使得搜索过程获得了方向性引导，从而在高维离散空间中实现了更高效的探索。

### 消融研究：奖励模型选择与拒绝采样分析

表 2 的消融研究表明，使用较小的奖励模型（4B vs 8B）不会导致显著的性能下降：在 MATH-500 和 AMC 上，两者的性能差距均低于 1 个百分点（ablations 中置信度为 0.95）。这一发现具有重要的实践意义，意味着 ∇-Reasoner 可以搭配更轻量的奖励模型，从而降低系统复杂性和内存占用。


![[assets/figures/papers/iclr26_0001_pEJAja73dk_nabla-Reasoner_LLM_Reasoning_via_Test-Time_Gradi/figures/007_Table_2.jpg]]
*Table 2: Ablation study on reward model choice*

表 3 分析了拒绝采样中的拒绝率。理论上，若从同一分布独立采样 N=8 次并选择最佳结果（如 BoN），拒绝率为 66.0%。而 ∇-Reasoner 通过 DTO 优化后的策略进行采样，显著降低了拒绝率：在 Qwen-2.5-7B 上为 32.8%，在 Qwen-2.5-7B-Instruct 上为 28.9%，在 Llama-3.1-8B-Instruct 上为 40.1%。**DTO 将拒绝率降低了高达 30% 以上**（ablations 中置信度为 0.95），这直接证明了梯度优化后的策略分布更接近最优奖励区域，从而减少了无效采样。


![[assets/figures/papers/iclr26_0001_pEJAja73dk_nabla-Reasoner_LLM_Reasoning_via_Test-Time_Gradi/figures/008_Table_3.jpg]]
*Table 3: the RewardBench (Malik et al., 2025). According to the Tab. 2, the performance gap between the 4B and 8B variants remains consistently below 1 point across both MATH-500 and AMC. This indicates that using a smaller reward model does not lead to significant performance degradation compared with the larger, stronger version. This justifies our original choice (in Tab. 1) and further suggests smaller reward models may be preferable for improving efficiency. Table 3: Analysis of rejection rate (%) in rejection sampling. We set N = 8 for the BoN baseline and also set N _ { m a x } = 8 for our ∇-Reasoner. The theoretical rejection rate of the baseline is 66.0%*

### 失败模式与局限性

尽管 ∇-Reasoner 在数学推理上表现优异，但存在若干失败模式和局限性。首先，对于 Llama-3.1-8B 模型，论文诚实跳过了其在 AIME 数据集上的结果，因为该模型无法产生合理的性能（fairness_notes），这表明方法的有效性依赖于基础模型的质量。其次，虽然模型调用次数减少，但总 FLOPs 仍显著高于 BoN 基线（2.46×10^17 vs 9.54×10^15，如表 5 所示），在硬件利用率较低的场景下可能带来更高的延迟。第三，方法依赖于奖励模型的可微性，对于非可微或黑盒奖励函数，需要额外的近似或替代方案。最后，当基础模型和奖励模型词汇表不一致时，方法的应用会受到限制。这些失败模式指向了未来工作的关键方向：如何进一步优化一阶优化的计算效率，以及如何扩展到更广泛的奖励函数和模型架构。

### 补充图表

![[assets/figures/papers/iclr26_0001_pEJAja73dk_nabla-Reasoner_LLM_Reasoning_via_Test-Time_Gradi/figures/009_Table_4.jpg]]
*Table 4: Summary of Experimental Settings*

![[assets/figures/papers/iclr26_0001_pEJAja73dk_nabla-Reasoner_LLM_Reasoning_via_Test-Time_Gradi/figures/010_Table_5.jpg]]
*Table 5: Comparison of wall-clock execution time for 83 prompts on the AMC dataset*


## 方法谱系与知识库定位

### 与基线方法的关系：从零阶搜索到一阶优化的范式跃迁

∇-Reasoner 的核心贡献在于将推理时扩展从**零阶搜索**范式转变为**一阶优化**范式。现有方法（BoN、SC、ToT、RAP）本质上都是零阶算法——它们仅依赖标量奖励值在离散 token 空间中进行采样、评估和搜索，缺乏方向性引导。随着推理链增长，搜索空间指数级扩大，奖励信号变得稀疏且噪声增大，性能容易饱和。∇-Reasoner 通过引入**可微文本优化（DTO）**，利用奖励模型和语言模型自身的可微性，在连续 logit 空间中进行梯度下降，从而获得具有方向性的搜索引导。这一转变在概念上如图1所示：零阶方法在奖励景观上随机采样候选点，而一阶方法沿着梯度方向直接向高奖励区域移动。

在优化对象上，基线方法操作离散 token 序列（通过拒绝采样、多数投票或树搜索），而 ∇-Reasoner 操作连续 logit 向量——这是 token 概率分布的连续松弛表示。具体而言，DTO 对来自基础策略的初始 logit 向量进行梯度下降，优化一个联合了奖励函数和序列对数似然的损失函数 $\mathcal{L}(\mathbf{y}) := -\lambda r(\mathbf{y}|\mathbf{x}) - \log \pi_{LLM}(\mathbf{y}|\mathbf{x})$。优化后的 logits 被视为改进的策略，用于采样下一个 token。这与基线方法形成鲜明对比：BoN 从固定策略采样 N 个完整轨迹后选择最佳者，ToT 和 RAP 在离散空间中进行树搜索，均无法利用梯度信息进行精细化调整。

### 理论定位：推理时梯度下降是“去摊销”的 PPO

∇-Reasoner 的理论洞察在于建立了推理时梯度下降与强化学习中策略优化之间的深刻联系。定理4.1证明：对 DTO 目标函数进行 Wasserstein 梯度流采样，等价于最小化 KL 正则化的 PPO 目标的最优分布。这意味着，**无需额外训练**，即可在测试时通过可微文本优化模拟策略优化过程，实现策略的即时改进。这一联系将 ∇-Reasoner 定位为“去摊销”的 PPO——它将训练时摊销到模型参数中的策略优化过程，在推理时显式地、针对每个具体输入实例重新执行。

这一理论定位揭示了方法的适用边界：它适用于任何存在可微奖励信号的场景，但要求基础语言模型和奖励模型能够端到端可微。当奖励函数非可微或为黑盒时，方法需要额外的近似或替代方案。

### 适用边界与条件

1. **奖励模型要求**：方法需要额外的奖励模型，增加了系统复杂性和内存占用。消融实验（Table 2）显示，使用较小的奖励模型（4B vs 8B）在 MATH-500 和 AMC 上的性能差距均低于1个百分点，表明对奖励模型规模不敏感，但奖励模型的质量和词汇表兼容性仍是关键限制。

2. **词汇表一致性**：当基础模型和奖励模型词汇表不一致时，方法的应用会受到限制。这是当前实现的一个实际约束。

3. **任务类型**：当前实验主要聚焦于数学推理（MATH-500, AMC, AIME-24/25），在更广泛的推理任务（常识推理、代码生成）上的泛化能力有待验证。

4. **计算效率的双面性**：虽然加速策略（梯度缓存绕过63.8%模型调用，轨迹复用消除74.1%自回归调用，token选择避免89.2%优化步骤）显著降低了模型调用次数，但总 FLOPs 仍显著高于 BoN 基线（2.46×10¹⁷ vs 9.54×10¹⁵）。壁钟时间对比（Table 5）显示，在 AMC 数据集上 ∇-Reasoner 耗时152.1秒，略高于 BoN 的136.1秒。这意味着在硬件利用率较低或延迟敏感的场景下，方法可能带来更高的实际开销。

### 局限与开放问题

**已识别的局限**：
- 需要额外的奖励模型，增加系统复杂性和内存占用。
- 总 FLOPs 显著高于基线，在硬件利用率低的场景下延迟可能更高。
- 当前主要验证于数学推理任务，泛化性待验证。
- 依赖奖励模型的可微性，对非可微或黑盒奖励函数需要额外近似。
- 词汇表不一致时应用受限。

**开放问题**：
1. **与 RL 训练方法的协同**：∇-Reasoner 与 RL 训练方法（如 OpenAI o1, DeepSeek R1）结合用于优化其长链推理过程时，会产生怎样的协同效应？方法理论上可以作为这些模型的推理时细化层。
2. **系统集成**：需要怎样的系统协同设计才能将 ∇-Reasoner 高效集成到 LLM 服务管线中？当前加速策略虽有效，但实际部署仍需进一步优化。
3. **扩展规律**：在超出当前测试的计算预算下，∇-Reasoner 的性能扩展规律如何？是否会遇到新的饱和点？
4. **与提示优化的协同**：∇-Reasoner 与提示优化方法之间是否存在协同效应？梯度引导的 token 优化是否能与提示工程互补？

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/nabla_Reasoner_LLM_Reasoning_via_Test_Time_Gradient_Descent_in_Latent_Space.pdf

![[paperPDFs/ICLR_2026/nabla_Reasoner_LLM_Reasoning_via_Test_Time_Gradient_Descent_in_Latent_Space.pdf]]
