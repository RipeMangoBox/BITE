---
title: "Risk-Sensitive Reinforcement Learning for Alleviating Exploration Dilemmas in Large Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Risk_Sensitive_Reinforcement_Learning_for_Alleviating_Exploration_Dilemmas_in_Large_Language_Models.pdf
project_link: null
code_link: null
openreview_forum_id: 7kC8ORye4l
aliases:
- RSGRG
- RSRLAEDLLM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "风险敏感超参数 β，通过指数效用函数平滑地控制优化目标在均值奖励与最大奖励之间的偏好，从而调节探索强度。"
primary_logic: "将风险敏感的指数效用目标引入策略梯度，重新加权优势信号，使模型更关注当前表现较差的困难提示，从而驱动更广泛的探索；同时通过保留对高精度提示的非零梯度，维持 pass@1 性能，实现探索与利用的有效平衡。"
claims:
- "在数学推理基准上，RS-GRPO 相比标准 GRPO 在 pass@32 上平均提升约 4%，同时保持或提升 pass@1。"
- "风险敏感策略梯度能从预训练策略的局部最优中逃逸，即使标准策略梯度被困。"
- "风险敏感优势函数在处理高准确率提示时仍保持非零梯度，而其他 pass@k 方法的优势会消失。"
- "Average over 6 mathematical reasoning benchmarks (Qwen2.5-Math-7B trained on de... 上 pass@1 = 28.6%"
---

# Risk-Sensitive Reinforcement Learning for Alleviating Exploration Dilemmas in Large Language Models

> [!tip] 核心洞察
> 将风险敏感的指数效用目标引入策略梯度，重新加权优势信号，使模型更关注当前表现较差的困难提示，从而驱动更广泛的探索；同时通过保留对高精度提示的非零梯度，维持 pass@1 性能，实现探索与利用的有效平衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 用于缓解大语言模型探索困境的风险敏感强化学习 |
| 英文题名 | Risk-Sensitive Reinforcement Learning for Alleviating Exploration Dilemmas in Large Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=7kC8ORye4l) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Risk-Sensitive GRPO (RS-GRPO) |
| Dataset | Average over 6 mathematical reasoning benchmarks (Qwen2.5-Math-7B trained on deepmath103k), AIME24 (Qwen2.5-Math-7B trained on deepmath103k) |

> [!tip] 效果简介
> - Average over 6 mathematical reasoning benchmarks (Qwen2.5-Math-7B trained on de... 上，pass@1 为 28.6%，对比 26.6% (GRPO)，变化 +2.0%。
> - Average over 6 mathematical reasoning benchmarks (Qwen2.5-Math-7B trained on de... 上，pass@32 为 48.3%，对比 45.3% (GRPO)，变化 +3.0%。
> - AIME24 (Qwen2.5-Math-7B trained on deepmath103k) 上，pass@1 为 30.2%，对比 25.7% (GRPO)，变化 +4.5%。

## 概要

大语言模型（LLM）的强化学习微调面临一个根本性的探索困境：预训练策略的概率分布高度集中，标准强化学习优化倾向于进一步坍缩到已有的高概率区域，仅利用现有能力而无法有效探索新的推理路径，导致多解性能（pass@k）停滞甚至下降。本文提出**风险敏感强化学习框架**（Risk-Sensitive RL），通过引入指数效用目标，在均值奖励与最大奖励之间进行平滑插值，从根本上调节探索强度。

核心思路是将风险敏感的指数效用目标融入策略梯度，推导出**风险敏感优势函数**，重新加权优势信号。这使得模型更关注当前表现较差的困难提示，从而驱动更广泛的探索；同时，该方法对高精度提示保持非零梯度，避免了现有 pass@k 优化方法中优势信号消失的问题，实现了探索与利用的有效平衡。

方法层面，本文将该框架实例化为**RS-GRPO**（Risk-Sensitive GRPO），仅需替换标准 GRPO 中的优势估计函数即可实现，改动极小。在数学推理基准上的实验表明，RS-GRPO 相比标准 GRPO 在 pass@32 上平均提升约 4%，同时 pass@1 保持或略有提升（平均约 +2%）。老虎机实验进一步证明，当标准策略梯度被困于局部最优时，风险敏感策略梯度（β ≥ 4）能够成功逃逸并收敛至全局最优。

### 大语言模型推理训练中的探索困境

近年来，强化学习（RL）已成为微调大语言模型（LLM）以提升其推理能力的主流范式。典型流程中，模型针对给定提示采样多个响应，通过结果验证器分配奖励，再利用策略梯度算法（如 GRPO）更新参数，以最大化期望奖励。然而，这一标准范式隐含着一个根本性的瓶颈：**预训练语言模型的初始策略分布高度集中**——模型倾向于反复生成少数几种高概率的解题模式，而标准 RL 的优化目标（最大化均值奖励）会进一步强化这种集中趋势，使策略坍缩至已有能力的局部最优，无法有效探索新的推理路径。

这一困境在数学推理任务中尤为突出。如图 1 所示，从一个概率质量集中于次优奖励的尖锐策略出发，标准 RL 不仅无法收敛至全局最优，反而进一步压缩策略分布；而风险敏感 RL 则能驱动探索，最终收敛至最优解。其直接后果是：尽管模型在单次采样（pass@1）上表现尚可，但在多次采样（pass@k）上的性能停滞甚至下降——即模型丧失了生成多样化正确解的能力。

### 现有 pass@k 优化方法的局限

针对上述探索困境，近期一系列工作尝试直接优化 pass@k 指标以鼓励多样性。这些方法可分为三类：

- **基于平滑最大目标的方法**（如 **Walder & Karkhanis**, 2025）：通过可微近似替代不可微的 max 算子，但其优势估计在二元奖励下始终保持正值，导致策略熵坍缩，实际表现不佳。
- **基于重新加权的策略梯度方法**（如 **Mahdavi et al.**, 2025）：对高奖励样本赋予更大权重，但当提示准确率超过阈值 $(1 - k/N)$ 时，优势信号消失为零，梯度信息丧失。
- **基于子集估计的训练方法**（如 **Chen et al.**, 2025）：通过子集采样估计 pass@k，但同样面临优势信号稀疏化的问题。

这些方法的共同缺陷在于：**优势估计在提示准确率较高时趋于零**，导致模型对已能部分解决的困难提示停止学习，限制了进一步探索。此外，大多数方法仅适用于二元奖励信号，难以泛化至连续奖励场景。

### 风险敏感视角的引入

本文从风险敏感强化学习的视角重新审视上述问题。核心洞察是：**标准 RL 的风险中性目标（最大化期望奖励）天然倾向于利用而非探索**；若将优化目标调整为风险寻求——即在均值奖励与最大奖励之间进行插值——则能系统性地驱动模型关注当前表现较差的困难提示，从而促进更广泛的探索。

具体而言，本文引入指数效用函数，将优化目标从 $\mathbb{E}[r]$ 连续地变换为 $\frac{1}{\beta} \log \mathbb{E}[e^{\beta r}]$，其中风险敏感参数 $\beta > 0$ 控制风险偏好程度。该目标在 $\beta \to 0$ 时退化为风险中性的均值奖励，在 $\beta \to \infty$ 时逼近最大奖励。由此导出的风险敏感策略梯度保持了标准策略梯度的结构，仅将优势函数替换为风险敏感优势：

$$A_{\beta}^{\pi_{\theta}}(y) = \frac{1}{\beta} \left( \frac{e^{\beta r(y)}}{\mathbb{E}_{y' \sim \pi_{\theta}(\cdot | x)}[e^{\beta r(y')}]} - 1 \right)$$

该优势函数具有两个关键性质：（1）通过指数变换放大高奖励样本的权重、惩罚低奖励样本，驱动策略向高奖励区域探索；（2）即使对于准确率较高的提示，仍保持非零梯度信号，避免了现有方法中优势消失的问题。这使得模型能够在维持 pass@1 性能的同时，持续提升 pass@k 表现，实现探索与利用的有效平衡。

## 核心方法与创新机理

### 1. 探索困境的形式化与因果瓶颈定位

标准强化学习（RL）在微调预训练大语言模型时面临一个根本性的**探索困境**：初始策略分布高度集中于预训练阶段习得的“安全”推理路径，而标准策略梯度优化以最大化期望奖励为目标，倾向于进一步强化这些已有能力，导致策略坍缩至局部最优。其直接后果是 **pass@k**（多次采样下的最佳性能）停滞甚至下降——模型无法探索新的推理路径来发现更优解。

本文的核心洞察在于：**这一困境的因果旋钮并非优化算法本身，而是优势信号的加权方式**。标准 GRPO（Shao et al., 2024）的群组归一化优势基于均值奖励，对高奖励和低奖励样本的区分度不足，尤其在处理高准确率提示时梯度信号趋于消失，无法驱动策略向未探索区域移动。

### 2. 风险敏感优势函数：核心 changed slot

RS-GRPO 的核心创新是**将风险敏感的指数效用目标引入策略梯度框架**，通过替换标准 GRPO 的群组归一化优势，引入一个新的风险敏感优势函数。这是整个方法唯一的实质性架构变更（changed slot），其余组件（PPO 裁剪、动态采样等）均沿用现有框架。

**标准 GRPO 的优势估计**（基线）：

$$A^{\pi_\theta}(y_i) = \frac{r(y_i) - \mu}{\sigma}$$

其中 $\mu$ 和 $\sigma$ 为群组内奖励的均值和标准差。该优势在样本奖励接近均值时信号微弱，且对高准确率提示的梯度趋于零。

**RS-GRPO 的风险敏感优势估计**（提出）：

$$\hat{A}_{\beta}^{\pi_{\theta}}(y_i) = \frac{1}{\beta} \left( \frac{e^{\beta r(y_i)}}{ \frac{1}{N} \sum_{j=1}^{N} e^{\beta r(y_j)} } - 1 \right)$$

这一公式通过指数变换将奖励映射到指数空间，实现了三个关键机制：

1. **重新加权优势信号**：高奖励样本获得指数级放大的正优势，低奖励样本获得更强的负优势，两者之间的对比度由风险敏感参数 $\beta$ 控制。
2. **保持非零梯度**：即使对于准确率已很高的提示，优势估计仍保持非零值，避免了现有 pass@k 优化方法中“优势消失”的问题（当样本准确率超过 $1 - k/N$ 时，**Mahdavi et al. (2025)** 等方法优势归零，而 RS-GRPO 持续提供稠密信号）。
3. **连续奖励兼容**：与 **Walder & Karkhanis (2025)**、**Chen et al. (2025)** 等方法仅支持二元奖励不同，RS-GRPO 天然处理连续奖励信号（如部分正确的推理步骤得分）。

### 3. 风险敏感参数 $\beta$：探索-利用的控制旋钮

$\beta$ 是连接优化目标与探索强度的因果旋钮。其作用机制可从优化目标的连续插值理解：

$$\mathcal{T}_{RS}(\pi_{\theta}) = \mathbb{E}_{x \sim \mathcal{D}} \left[ \frac{1}{\beta} \log \mathbb{E}_{y \sim \pi_{\theta}(\cdot | x)} \left[ e^{\beta r(y)} \right] \right]$$

- 当 $\beta \to 0$ 时，$\mathcal{T}_{RS}$ 退化为标准期望奖励目标（风险中性，纯利用）；
- 当 $\beta \to \infty$ 时，$\mathcal{T}_{RS}$ 趋近于最大奖励目标（极端风险寻求，纯探索）；
- 有限正 $\beta$ 值在两者之间平滑插值，实现探索与利用的连续调节。

**老虎机验证实验**（Figure 3）提供了决定性证据：在具有明显局部最优的奖励景观中，标准策略梯度（$\beta=0$）被困于奖励约 0.6 的局部最优，而风险敏感策略（$\beta \geq 4$）成功收敛至奖励 1.0 的全局最优。该实验直接证明了风险敏感梯度能够从预训练策略的局部最优中逃逸。

### 4. 与现有 pass@k 优化方法的本质差异

现有 pass@k 优化方法（**Walder & Karkhanis, 2025**；**Mahdavi et al., 2025**；**Chen et al., 2025**）通常通过修改目标函数或重采样策略来直接优化最大奖励，但存在两个结构性缺陷：

- **信号稀疏性**：多数方法的优势估计在提示准确率超过阈值后消失，导致训练后期梯度信息匮乏；
- **二元奖励限制**：仅适用于正确/错误的二元奖励，无法利用连续奖励中的部分推理信息。

RS-GRPO 通过指数效用函数统一解决了这两个问题：稠密的非零优势信号维持了训练全程的优化动力，连续奖励兼容性使得方法可应用于更广泛的推理场景（如代码生成、科学问答，见 Table 3 和 Table 4 的 GPQA-Diamond 和 LiveCodeBench 结果）。

### 5. 方法简洁性与即插即用特性

RS-GRPO 的工程实现极其简洁：仅需替换 GRPO 中的优势计算模块，无需修改采样策略、奖励模型或优化器架构。经验优势估计公式（式 8）可直接作为现有 GRPO 实现的 drop-in replacement，计算开销与标准 GRPO 相当（仅增加 $N$ 次指数运算）。这一设计使得该方法可无缝集成到主流 RL 微调框架（如 VeRL）中，且所有实验均在统一的超参数设置下进行公平比较。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_7kC8ORye4l/figures/002_Table_1.jpg]]
*Table 1: Comparison of Pass@k optimization methods with Risk-Sensitive RL*

### 设计动机与核心机制

大语言模型微调面临一个根本性的探索困境：预训练策略分布高度集中，标准强化学习（如 GRPO）在优化期望奖励时倾向于进一步收缩策略，仅利用已有能力而无法探索新的推理路径，导致 pass@k（多解性能）停滞甚至下降。RS-GRPO 通过引入**风险敏感目标**直接干预这一瓶颈——利用指数效用函数将优化目标从均值奖励平滑地插值到最大奖励，从而调节探索强度。

核心机制在于**重新加权优势信号**：风险敏感优势函数 $A_{\beta}(y)$ 对高奖励样本赋予指数级增强的权重，同时保持对低奖励样本的惩罚梯度，使模型更关注当前表现较差的困难提示。与现有 pass@k 优化方法的关键区别在于，当提示准确率超过一定阈值时，其他方法的优势估计会消失，而 RS-GRPO 始终维持非零梯度信号（见 Section D），从而在驱动探索的同时保护 pass@1 性能。

### 整体 Pipeline

RS-GRPO 的训练流程由三个模块串联构成，可直接嵌入现有 GRPO 框架：

1. **策略模型采样**：对每个输入提示 $x$，从当前策略 $\pi_{\theta}$ 采样 $N$ 个响应 $\{y_1, \ldots, y_N\}$，并获取对应的奖励 $\{r(y_1), \ldots, r(y_N)\}$。该模块与标准 GRPO 完全一致。

2. **风险敏感优势计算**：替代 GRPO 的原始群组归一化优势，使用经验风险敏感优势估计：
   $$\hat{A}_{\beta}^{\pi_{\theta}}(y_i) = \frac{1}{\beta} \left( \frac{e^{\beta r(y_i)}}{ \frac{1}{N} \sum_{j=1}^{N} e^{\beta r(y_j)} } - 1 \right)$$
   其中 $\beta > 0$ 为风险敏感性参数，$\beta=0$ 退化为标准风险中性目标。该公式通过指数变换放大高奖励样本的相对权重，同时保证优势信号始终非零。

3. **策略梯度更新**：使用 PPO 风格的优化器（包含 clip_high、动态采样等技术）更新策略参数，梯度方向为：
   $$\nabla_{\theta} \mathcal{J}_{RS}(\pi_{\theta}) = \mathbb{E}_{x, y \sim \pi_{\theta}} \left[ A_{\beta}^{\pi_{\theta}}(y) \nabla_{\theta} \log \pi_{\theta}(y \mid x) \right]$$
   训练中采用动态采样技术，排除全对或全错的 rollout 以保持非零梯度。

### 输入输出流

- **输入**：预训练语言模型 $\pi_{\theta}$、训练数据集 $\mathcal{D}$、风险敏感性参数 $\beta$、每提示响应数 $N$。
- **输出**：微调后的策略模型，在保持或提升 pass@1 的同时显著改善 pass@k 性能。
- **关键控制变量**：$\beta$ 是调节探索-利用平衡的核心超参数。消融实验表明，增大 $\beta$ 可提升 pass@32，但 $\beta=2$ 在 pass@1 和 pass@k 间取得最佳平衡（Figure 5）。

### 与现有方法的关系

Table 1 系统比较了 RS-GRPO 与现有 pass@k 优化方法的特性差异。RS-GRPO 是唯一同时支持二元奖励、连续奖励和密集信号的方法。具体而言：
- **Walder & Karkhanis (2025)** 基于平滑最大目标，但其优势估计始终为正，导致熵崩塌。
- **Mahdavi et al. (2025)** 和 **Chen et al. (2025)** 分别通过重新加权和子集估计优化 pass@k，但在高准确率提示上优势信号消失。
- RS-GRPO 通过指数效用函数自然处理连续奖励，并在所有准确率水平上维持非零梯度，实现了更优的探索-利用权衡。

### 风险敏感目标函数

标准强化学习微调大语言模型时，优化目标为期望奖励最大化：

$$\mathcal{J}(\pi_{\theta}) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_{\theta}(\cdot | x)} [r(x, y)]$$

该目标在初始策略分布高度集中时，倾向于仅利用已有能力，导致探索不足。为此，本文引入风险敏感目标，通过指数效用函数将优化目标从均值奖励连续地调整到最大奖励：

$$\mathcal{T}_{RS}(\pi_{\theta}) = \mathbb{E}_{x \sim \mathcal{D}} \left[ \frac{1}{\beta} \log \mathbb{E}_{y \sim \pi_{\theta}(\cdot | x)} \left[ e^{\beta r(y)} \right] \right]$$

其中 $\beta \geq 0$ 为风险敏感参数：当 $\beta \to 0$ 时，目标退化为期望奖励（风险中性）；当 $\beta \to \infty$ 时，目标趋近于最大奖励（风险寻求），对应 pass@k 的渐近形式。

### 风险敏感策略梯度

对上述目标求导，得到风险敏感策略梯度定理：

$$\nabla_{\theta} \mathcal{J}_{RS}(\pi_{\theta}) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_{\theta}(\cdot | x)} \left[ A_{\beta}^{\pi_{\theta}}(y) \nabla_{\theta} \log \pi_{\theta}(y \mid x) \right]$$

该梯度在结构上与标准策略梯度完全一致，唯一区别在于优势函数 $A_{\beta}^{\pi_{\theta}}(y)$ 的定义。

### 风险敏感优势函数

风险敏感优势函数的核心形式为：

$$A_{\beta}^{\pi_{\theta}}(y) = \frac{1}{\beta} \left( \frac{e^{\beta r(y)}}{\mathbb{E}_{y' \sim \pi_{\theta}(\cdot | x)}[e^{\beta r(y')}]} - 1 \right)$$

**变量含义**：
- $r(y)$：响应 $y$ 的奖励值
- $\mathbb{E}_{y' \sim \pi_{\theta}(\cdot | x)}[e^{\beta r(y')}]$：当前策略下奖励的指数期望，作为归一化因子
- $\beta$：控制风险偏好强度；$\beta$ 越大，高奖励样本的权重越大，低奖励样本被惩罚越重

该优势函数的关键特性是：即使对于高准确率提示，优势信号仍保持非零梯度，避免了现有 pass@k 方法中优势估计消失的问题（当样本准确率超过 $1 - k/N$ 时）。

### 经验优势估计

在实际实现中，对每个提示采样 $N$ 个响应，使用蒙特卡洛估计替代期望：

$$\hat{A}_{\beta}^{\pi_{\theta}}(y_i) = \frac{1}{\beta} \left( \frac{e^{\beta r(y_i)}}{ \frac{1}{N} \sum_{j=1}^{N} e^{\beta r(y_j)} } - 1 \right)$$

该估计可直接替换 GRPO 中的群组归一化优势计算，无需改动其余训练流程。

### RS-GRPO 算法管线

RS-GRPO 由三个核心模块构成，均基于现有 GRPO 框架（Shao et al., 2024）进行最小修改：

1. **策略模型采样**：基于当前策略 $\pi_{\theta}$ 为每个提示生成 $N$ 个候选响应。
2. **风险敏感优势计算**：使用上述经验优势估计公式，替换 GRPO 原有的群组归一化优势。该模块是唯一被修改的组件。
3. **策略梯度更新**：沿用 PPO 风格的优化器，包含 clip_high、动态采样等技术，将风险敏感优势代入策略梯度进行参数更新。

实验超参数方面，典型配置为 $\beta=2$（在 pass@1 和 pass@k 间取得最佳平衡），响应数 $N=16$，训练使用 VeRL 框架统一管理。训练中采用动态采样技术，排除全对或全错的 rollout 以保持非零梯度。

## 实验与关键发现

### 核心瓶颈与因果机制

标准强化学习（RL）微调预训练语言模型时，初始策略分布高度集中——模型倾向于反复生成其已掌握的高概率推理路径。这种分布特性导致标准策略梯度优化被“困”在局部最优：梯度信号主要来自模型已经表现良好的提示，优化过程仅利用已有能力，无法有效探索新的推理路径。其直接后果是 **pass@k（多解性能）停滞甚至下降**——模型虽然能在单次采样（pass@1）上维持精度，但在多次采样中无法产生足够多样化的正确解答。

RS-GRPO 的因果调节旋钮是**风险敏感超参数 β**。通过指数效用函数：

$$\mathcal{T}_{RS}(\pi_{\theta}) = \mathbb{E}_{x \sim \mathcal{D}} \left[ \frac{1}{\beta} \log \mathbb{E}_{y \sim \pi_{\theta}(\cdot | x)} \left[ e^{\beta r(y)} \right] \right]$$

该目标在 β → 0 时退化为标准均值奖励最大化（风险中性），在 β → ∞ 时趋近于最大化单次采样的最高奖励（极端风险寻求）。由此，β 平滑地控制优化目标在“均值奖励”与“最大奖励”之间的偏好，从而调节探索强度。

核心洞察在于：将风险敏感的指数效用目标引入策略梯度后，优势函数被重新加权为：

$$\hat{A}_{\beta}^{\pi_{\theta}}(y_i) = \frac{1}{\beta} \left( \frac{e^{\beta r(y_i)}}{ \frac{1}{N} \sum_{j=1}^{N} e^{\beta r(y_j)} } - 1 \right)$$

这一变换产生两个关键效应：其一，模型更关注当前表现较差的困难提示——低奖励样本获得更强的负向梯度惩罚，驱动策略远离次优路径；其二，对高奖励提示仍保持非零梯度信号，从而维持 pass@1 性能。这与现有 pass@k 优化方法形成本质区别：后者在提示准确率超过阈值（1 - k/N）后优势信号消失，而 RS-GRPO 的优势函数始终保持密集信号（见 Figure 9 对比）。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_7kC8ORye4l/figures/030_Figure_9.jpg]]
*Figure 9: Comparison of advantage estimations across different inference-time objective methods under the binary reward setting with N = 1 6 . . Left - Positive: Advantage estimation for positive responses. Middle - Negative: Advantage estimation for negative responses. Right - Cumulative: Cumulative absolute advantage value per prompt*

### 老虎机验证实验

Figure 3 展示了一个决定性证据：在 100 臂老虎机问题中，策略被初始化为一个远离全局最优（奖励 1.0）的局部最优（奖励约 0.6）。风险中性策略（β = 0）始终被困在局部最优，而风险敏感策略（β ≥ 4）成功收敛到全局最优。值得注意的是，更大的 β 值虽然最终也能收敛，但收敛速度明显变慢——这揭示了风险敏感性与优化效率之间的权衡。


### 主要实验结果

Table 2 汇总了 RS-GRPO 在 6 个数学推理基准上的核心结果。以 Qwen2.5-Math-7B 在 deepmath103k 数据集上训练为例：

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_7kC8ORye4l/figures/014_Table_2.jpg]]
*Table 2: Main results on mathematical reasoning benchmarks, reporting pass@1 and pass@32 (%) for five models and three training datasets. Subscripts denote improvement over GRPO. RS-GRPO consistently outperforms the GRPO baseline on pass@32, while maintaining or improving pass@1 accuracy. RS-GRPO also achieves a better trade-off than prior pass@k optimization methods. We observe that the approach of Walder & Karkhanis (2025) performs unsatisfactorily, mainly because its advantage estimates remain strictly positive (see Appendix D). The absence of negative advantages causes rapid entropy collapse and poor training performance, consistent with prior findings on the importance of negative signals (Zhu...*

- **pass@1**：RS-GRPO 达到 28.6%，相较 GRPO 的 26.6% 提升 **+2.0%**。
- **pass@32**：RS-GRPO 达到 48.3%，相较 GRPO 的 45.3% 提升 **+3.0%**。
- 在 AIME24 上，pass@1 从 25.7% 提升至 30.2%，增幅达 **+4.5%**。

RS-GRPO 在 pass@32 上平均提升约 4%，同时保持或提升 pass@1——这一模式在 5 个不同模型（Qwen2.5-Math-1.5B/7B、Qwen2.5-7B、Qwen3-4B-Base、Llama3.1-8B-Instruct）和 3 个训练数据集上一致复现。

Figure 4 的 pass@k 曲线（k 从 1 到 1024）进一步揭示了趋势：RS-GRPO 的优势随 k 增大而扩大，表明其探索能力的增益在高采样预算下尤为显著。

### 与其他 pass@k 优化方法的对比

Figure 6 展示了 RS-GRPO 与三类现有 pass@k 优化方法的训练动态对比：

- **Walder & Karkhanis (2025)** 的方法表现不佳，主要因为其优势估计始终保持正值，导致策略熵崩溃。
- **Mahdavi et al. (2025)** 和 **Chen et al. (2025)** 的方法在 pass@32 上与 RS-GRPO 大致持平，但在 pass@1 上被 RS-GRPO 稳定超越。
- RS-GRPO 的优势在于其优势信号更密集——即使在提示准确率较高时仍保持非零梯度，从而在探索与利用之间实现更优平衡。

### 消融研究

**β 敏感性分析**（Figure 5）：增大 β 可提升 pass@32，但 β = 2 在 pass@1 和 pass@k 之间取得最佳平衡。β 过大（如 β = 8）会导致 pass@1 下降，因为过度风险寻求会牺牲对已掌握能力的利用。尝试的动态 β 策略（如线性增加）未能优于固定 β = 2。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_7kC8ORye4l/figures/009_Figure_5.jpg]]
*Figure 5: Ablation Study of β in RS-GRPO on Qwen2.5-Math-1.5B (top) and -7B (bottom)*

**响应数 N 的影响**（Figure 11）：RS-GRPO 在 N ∈ {4, 8, 16, 32} 下均一致优于 GRPO，表明该方法对不同采样预算具有鲁棒性。


**探索多样性验证**（Figure 7 左）：RS-GRPO 生成的唯一答案数量显著多于 GRPO，直接证实了其增强探索能力的效果。Figure 7 右的准确率转移图进一步显示，RS-GRPO 在 GRPO 失败的提示上获得了更多正确解答。

### 跨领域泛化

- **GPQA-Diamond**（Table 3）：RS-GRPO 在 pass@32 上达到 88.9%，超过 GRPO 的 84.8%。
- **LiveCodeBenchv5** 代码生成（Table 4）：RS-GRPO 在 pass@1 上达到 29.7%（GRPO 为 28.5%），pass@8 上达到 36.2%（GRPO 为 32.7%）。

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_7kC8ORye4l/figures/016_Table_3.jpg]]
*Table 3: Pass@k comparison on GPQA-Diamond*

![[assets/figures/papers/paper_list_l7_https_openreview_net_forum_id_7kC8ORye4l/figures/017_Table_4.jpg]]
*Table 4: Pass@k comparison on LiveCodeBenchv5*

### 已知失败模式

1. **部分模型高 k 值退化**：在 Qwen2.5-7B 和 Llama3.1-8B-Instruct 上，RS-GRPO 在高 k 值下未能超越基础模型。可能原因是这些基础模型的最优策略离初始分布太远，仅靠风险敏感梯度不足以充分跨越分布鸿沟。
2. **自适应 β 机制缺失**：尝试的动态 β 策略未能超越固定 β = 2，表明当前缺乏有效的自适应风险调节机制。
3. **框架局限性**：风险敏感框架目前为 bandit 设置设计，尚未扩展到具有状态转移的完整强化学习场景。

## 定位与知识库关联

### 核心瓶颈与设计动机

标准强化学习（RL）在微调预训练语言模型时面临一个根本性的探索困境：初始策略分布高度集中在预训练阶段已习得的行为模式上，基于期望奖励最大化的策略梯度优化倾向于进一步坍缩这一分布，仅利用已有能力而无法有效探索新的推理路径。这导致模型的多解性能指标 pass@k（k 次采样中至少有一次正确的概率）停滞甚至下降。本文的核心洞察是，通过引入风险敏感的指数效用目标，重新加权优势信号，使模型更关注当前表现较差的困难提示，从而驱动更广泛的探索；同时通过保留对高精度提示的非零梯度，维持 pass@1 性能，实现探索与利用的有效平衡。

### 与现有 pass@k 优化方法的关系

本文提出的风险敏感 RL 框架与现有的 pass@k 优化方法处于同一问题域，但在方法设计和适用性上有本质区别。Table 1 系统比较了各方法在三个关键维度上的支持情况：二元奖励、连续奖励和稠密信号。

| 方法 | 二元奖励 | 连续奖励 | 稠密信号 |
|------|---------|---------|---------|
| Tang et al. | ✓ | ✗ | ✗ |
| **Walder & Karkhanis (2025)** | ✓ | ✗ | ✗ |
| **Mahdavi et al. (2025)** | ✓ | ✗ | ✗ |
| **Chen et al. (2025)** | ✓ | ✓ | ✗ |
| **RS-GRPO (本文)** | ✓ | ✓ | ✓ |

**Walder & Karkhanis (2025)** 采用基于平滑最大目标的 pass@k 优化方法，但其优势估计始终为正，导致策略熵坍缩，实际表现不佳（Table 2 讨论部分明确指出该方法“performs unsatisfactorily”）。**Mahdavi et al. (2025)** 和 **Chen et al. (2025)** 分别基于重新加权和子集估计进行 pass@k 训练，但这些方法的一个共同缺陷是：当提示的样本准确率超过阈值 `(1 - k/N)` 时，优势信号会消失（Section D），导致对高准确率提示的优化停止，限制了 pass@1 性能。相比之下，RS-GRPO 的风险敏感优势函数通过指数变换，在所有奖励水平上保持非零梯度，提供更稠密的优化信号（Figure 9 对比了各方法在二元奖励下的优势估计差异）。

### 方法谱系中的定位

从方法谱系来看，RS-GRPO 直接继承自 **GRPO**（Group Relative Policy Optimization, Shao et al., 2024），后者是当前 LLM 推理能力训练的主流算法框架。RS-GRPO 的核心改动仅在于优势估计函数，将 GRPO 的群组归一化优势替换为风险敏感优势：

$$\hat{A}_{\beta}^{\pi_{\theta}}(y_i) = \frac{1}{\beta} \left( \frac{e^{\beta r(y_i)}}{ \frac{1}{N} \sum_{j=1}^{N} e^{\beta r(y_j)} } - 1 \right)$$

这一替换保持了与 GRPO 训练框架的完全兼容性，可作为即插即用的模块嵌入现有的 PPO 风格优化器（包括 clip_high、动态采样等技术）。训练框架 VeRL 的超参数设置在所有比较方法中保持一致，确保了公平性。

从更广泛的 RL 理论谱系看，本文的风险敏感目标属于指数效用函数框架，通过风险敏感性参数 β 平滑地控制优化目标在均值奖励（β→0）与最大奖励（β→∞）之间的偏好。这一形式与 bandit 理论中的风险敏感决策有深刻联系，但本文首次将其系统地引入 LLM 的策略梯度微调场景。

### 适用边界与局限

尽管 RS-GRPO 在数学推理基准上展现了稳健的改进，但其适用边界需要审慎界定：

1. **基础模型依赖**：在某些基础模型（如 Qwen2.5-7B、Llama3.1-8B-Instruct）的高 k 值上，RS-GRPO 未能超越基础模型本身。分析指出这可能是因为最优策略距离初始分布太远，风险敏感探索的强度不足以弥合这一差距。

2. **β 调节机制不足**：尝试的动态 β 策略（如线性增加）未能优于固定 β=2，表明当前缺乏自适应的风险偏好调节机制。β 的选择目前依赖经验调参，最优值（典型为 2 或 8）可能因模型规模、任务类型和训练数据而异。

3. **理论框架限制**：风险敏感框架目前是为 bandit 设置设计的，尚未扩展到具有状态转移的完整强化学习场景。在需要多步交互的任务中，其理论保证和实际效果有待验证。

4. **任务泛化边界**：虽然 RS-GRPO 在 GPQA-Diamond（科学推理）和 LiveCodeBenchv5（代码生成）上展现了初步的跨任务泛化能力（Table 3, Table 4），但其在更广泛的非推理任务（如对话生成、创意写作）上的有效性尚未得到系统验证。

### 开放问题

本文揭示了若干值得进一步探索的方向：

- **自适应 β 机制**：如何根据训练动态、提示难度或模型不确定性自动调整风险敏感参数 β，以在探索与利用之间实现动态平衡？
- **与内在奖励的结合**：风险敏感 RL 能否与基于模型不确定性的探索奖励或好奇心驱动机制结合，进一步提升对未知区域的探索效率？
- **完整 RL 场景扩展**：如何将风险敏感框架从 bandit 设置扩展到具有状态转移的序列决策问题，以支持更复杂的推理链优化？
- **理论收敛性分析**：在 LLM 的非凸策略空间中，风险敏感策略梯度的收敛性理论尚不完整，特别是 β 与收敛速度之间的定量关系需要进一步刻画。

## 原文 PDF

![[paperPDFs/ICLR_2026/Risk_Sensitive_Reinforcement_Learning_for_Alleviating_Exploration_Dilemmas_in_Large_Language_Models.pdf]]
