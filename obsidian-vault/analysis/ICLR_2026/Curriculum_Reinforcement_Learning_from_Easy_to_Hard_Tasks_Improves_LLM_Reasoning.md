---
title: "Curriculum Reinforcement Learning from Easy to Hard Tasks Improves LLM Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Curriculum_Reinforcement_Learning_from_Easy_to_Hard_Tasks_Improves_LLM_Reasoning.pdf
project_link: null
code_link: https://github.com/divelab/E2H-Reasoning
openreview_forum_id: KJvHnl3kUv
aliases:
- ERE
- CRLFEHTILR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过任务难度分解和概率调度策略（高斯/余弦调度器）控制训练过程中不同难度任务的采样比例，使模型从易到难逐步建立推理能力。"
primary_logic: "从易到难的课程学习能够帮助语言模型逐步学习核心推理原则，而精心设计的调度器可在避免简单任务过拟合的同时保留泛化能力，并在理论上保证更优的样本复杂度。"
claims:
- "E2H-G在多个基准的困难子集和OOD任务上显著优于GRPO和直接训练基线，且所需困难样本更少。"
- "理论证明了课程学习在分布插值和样本效率上的优势，并给出了收敛保证和样本复杂度上界。"
- "Blocksworld 上 Hard Accuracy = 32.9 (E2H-G)"
- "Countdown 上 Hard Accuracy = 28.1 (E2H-G)"
---

# Curriculum Reinforcement Learning from Easy to Hard Tasks Improves LLM Reasoning

> [!tip] 核心洞察
> 从易到难的课程学习能够帮助语言模型逐步学习核心推理原则，而精心设计的调度器可在避免简单任务过拟合的同时保留泛化能力，并在理论上保证更优的样本复杂度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于从易到难任务课程强化学习的大语言模型推理提升 |
| 英文题名 | Curriculum Reinforcement Learning from Easy to Hard Tasks Improves LLM Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KJvHnl3kUv) · [GitHub](https://github.com/divelab/E2H-Reasoning) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | E2H Reasoner (E2H) |
| Dataset | Blocksworld, Countdown, GSM8K, AIME24 |

> [!tip] 效果简介
> - Blocksworld 上，Hard Accuracy 为 32.9 (E2H-G)，对比 21.1 (GRPO All)，变化 +11.8。
> - Countdown 上，Hard Accuracy 为 28.1 (E2H-G)，对比 18.1 (GRPO All)，变化 +10.0。
> - GSM8K 上，Average Accuracy 为 78.7 (E2H-G)，对比 67.7 (GRPO)，变化 +11.0。

## 概要

大语言模型在数学推理、规划等复杂任务上直接应用强化学习（RL）时，面临一个根本瓶颈：**稀疏奖励与分布偏移**。由于奖励仅在最终答案正确时给出，模型从零开始探索困难任务时几乎无法获得有效学习信号，导致收敛缓慢、过拟合训练分布，且难以泛化到分布外（OOD）场景。

针对这一瓶颈，本文提出 **E2H Reasoner（E2H）**，一种基于课程学习的强化学习后训练方法。其核心思想是：**将训练数据按难度分解为从易到难的多个级别，并通过概率调度器在训练过程中逐步将采样重心从简单任务转移到困难任务**。这一设计使模型能够先掌握核心推理原则，再将其迁移到更复杂的问题上，从而缓解稀疏奖励和分布偏移问题。理论分析进一步证明，课程学习在分布插值和样本效率上具有优势，并给出了收敛保证和样本复杂度上界。

在方法谱系中，E2H 的定位如下：
- **相对于 GRPO**（Guo et al., 2025）：GRPO 采用平衡采样，所有难度任务均匀混合训练；E2H 引入任务分解和从易到难的概率调度，显著提升困难任务性能。
- **相对于 DAPO**（Yu et al., 2025）：DAPO 是 GRPO 的改进变体，E2H 与其互补——结合后不仅性能进一步提升，且训练过程中零优势批次的占比显著下降。
- **相对于传统课程学习**：传统课程学习按固定顺序切换任务阶段，而 E2H 的概率调度器（高斯调度 E2H-G 和余弦调度 E2H-C）允许不同难度任务在训练全程中按平滑变化的概率被采样，避免简单任务过拟合和灾难性遗忘。

实验结果表明，E2H 在五个推理基准上一致优于基线方法。在 Blocksworld 的困难子集上，E2H-G 相较 GRPO 提升 **+11.8** 个百分点（32.9 vs 21.1）；在 Countdown 困难子集上提升 **+10.0** 个百分点（28.1 vs 18.1）；在 GSM8K 上平均准确率提升 **+11.0** 个百分点（78.7 vs 67.7）。更重要的是，E2H 所需的困难训练样本远少于非课程基线，验证了其样本效率优势。在 MATH 训练的模型上，E2H 在 AIME24 和 OlympiadBench 等 OOD 竞赛级任务上也展现出更强的泛化能力。

E2H 的主要局限在于其调度器是非自适应的——高斯和余弦调度在训练前预设参数，不会根据训练过程中的模型能力动态调整。此外，难度分档数和调度器超参数仍需人工设定。将 E2H 与自适应课程策略结合，是未来进一步提升的方向。



### 推理任务中的强化学习困境

大语言模型在数学推理、规划等复杂任务上的能力近年来受到广泛关注。强化学习后训练（RL-based post-training）被认为是提升模型推理性能的有效途径，尤其在低采样预算（low $k$）的 Pass@$k$ 评估中表现突出。然而，直接对困难推理任务应用强化学习面临两个根本性瓶颈：

**稀疏奖励问题**：复杂推理任务通常仅在最终答案完全正确时给予正向奖励，中间步骤缺乏密集的反馈信号。这使得模型从零开始探索时几乎无法获得有效的学习信号，训练效率极低。

**分布偏移与过拟合**：当训练集包含大量高难度样本时，模型容易陷入局部最优，学到的策略缺乏泛化能力。即便在训练分布内表现尚可，面对分布外（OOD）任务时性能往往急剧下降。

现有方法如 **GRPO**（Guo et al., 2025）和 **DAPO**（Yu et al., 2025）采用平衡采样策略，即均匀混合所有难度级别的数据进行训练。这种策略忽视了任务难度之间的结构关系，未能利用简单任务中蕴含的核心推理原则来辅助困难任务的学习。

### 课程学习的启示

课程学习（Curriculum Learning）的核心思想是模仿人类学习过程——从简单概念入手，逐步过渡到复杂问题。在教育学和认知科学中，这一策略被证明能够加速学习并提升泛化能力。然而，将课程学习应用于大语言模型的强化学习后训练时，两个关键问题尚未得到充分解决：

1. **如何定义和划分任务难度？** 推理任务的难度不仅取决于表面特征（如问题长度、数字大小），更与所需推理步骤的深度和组合方式相关。
2. **如何设计从易到难的过渡策略？** 固定顺序的传统课程学习缺乏灵活性，而自适应方法（如 **Self-Evolve**，Chen et al., 2025，通过维持 50% 解决率调整采样难度）虽能动态调节，但可能因过度聚焦当前能力边界而忽略对基础技能的巩固。

### 本文动机

本文旨在回答一个核心问题：**能否通过精心设计的从易到难课程学习策略，使大语言模型在稀疏奖励的推理任务上获得更高效、更泛化的强化学习训练？**

具体而言，本文提出 **E2H Reasoner（E2H）**，一种基于课程学习的强化学习方法，通过以下两个关键设计解决上述问题：

- **任务难度分解**：将训练集按难度划分为 trivial、easy、medium、hard 四个级别，使模型能够从最基础的推理模式开始学习。
- **概率调度器**：采用高斯调度（E2H-G）或余弦调度（E2H-C）控制训练过程中不同难度任务的采样比例，从易到难平滑过渡，避免简单任务过拟合的同时保留泛化能力。

本文从理论和实验两个层面验证了课程学习的优势：理论上证明了课程学习在分布插值和样本效率上优于直接学习，并给出了收敛保证；实验上在 Blocksworld、Countdown、MATH、GSM8K 等多个推理基准上取得了显著的性能提升，尤其在困难子集和 OOD 任务上表现突出，且所需困难样本量远少于非课程基线。



## 核心方法与创新机理

### 创新动机：稀疏奖励与分布偏移的双重困境

大语言模型在困难推理任务上直接使用强化学习（RL）后训练时，面临两个根本性瓶颈。其一，**稀疏奖励**问题：奖励信号仅在模型输出最终正确答案时给出，中间步骤无任何反馈，导致从零开始的策略探索极其低效。其二，**分布偏移**问题：预训练模型的初始策略分布与目标困难任务的分布之间存在巨大差距，直接使用平衡采样（Balanced Scheduling）训练时，模型难以获得有效的学习信号，容易过拟合或无法泛化。E2H Reasoner 的核心洞察是：**从易到难的课程学习能够帮助语言模型逐步建立核心推理原则，而精心设计的概率调度器可在避免简单任务过拟合的同时保留泛化能力，并在理论上保证更优的样本复杂度。**

### 关键创新点一：任务难度分解（Task Decomposition）

**Baseline 做法**：GRPO（Guo et al., 2025）等现有 RL 后训练方法直接将完整训练集混合，采用均匀采样进行训练，不对任务难度进行区分。

**E2H 的改变**：E2H 首先将训练数据集按难度显式分解为四个等级——trivial（琐碎）、easy（简单）、medium（中等）、hard（困难）。分解依据分两种情形：
- 对于具有人工难度标注的数据集（如 Blocksworld 按规划步数、Countdown 按操作数数量、MATH 按题目级别），直接使用预定义的分档标准（Table 9）。
- 对于无人工标注的数据集（如 GSM8K、AQuA），通过模型在 CoT 提示下的错误率自动估计难度，并按四分位数分组（Figure 5, Figure 6）。

这一分解的因果作用在于：**简单任务使模型能够先学习核心推理原理，再将这些原理迁移到困难任务上**。消融实验（Table 1）直接验证了这一机制：仅使用 hard 数据训练时，模型在 Blocksworld Hard 上的准确率仅为 0.0%，而加入 trivial 和 easy 数据后提升至 21.1%，证明简单任务对建立基础推理能力不可或缺。

### 关键创新点二：概率调度器（Probabilistic Scheduler）

**Baseline 做法**：GRPO 采用平衡调度（Balanced Scheduling），即在整个训练过程中以均匀概率 $1/K$ 从所有 $K$ 个难度等级中随机采样任务。传统课程学习（Traditional CL）则采用硬切换策略：在预设的时间阈值 $\tau_k$ 处从难度 $k$ 完全切换到难度 $k+1$。

**E2H 的改变**：E2H 提出两种**概率调度器**，在训练过程中以连续变化的方式调整不同难度任务的采样概率，实现从易到难的平滑过渡：

- **余弦调度器（E2H-C）**：非参数化策略，利用余弦函数插值采样权重，训练初期侧重简单任务，后期逐步转向困难任务。定义为 $\mathbf{S}_{\mathrm{cosine}}(t, k) = \alpha_t \cdot (K - k - 1) + (1 - \alpha_t) \cdot k$，其中 $\alpha_t = \frac{1}{2}(1 + \cos(\frac{t}{T}\pi))$。

- **高斯调度器（E2H-G）**：参数化策略，通过高斯核函数控制每个难度等级的采样概率。定义为 $\mathbf{S}_{\mathrm{Gaussian}}(t, k) = \exp\left(-\frac{(x_t - \mu_k)^2}{2\sigma^2}\right)$，其中 $x_t = (\frac{t}{T})^\beta (K-1)$ 是时间变量，$\mu_k$ 是第 $k$ 级任务的中心位置。超参数 $\beta$ 控制难度转移速度，$\sigma$ 控制采样集中度（Figure 4）。

**调度器的因果机制**：与平衡调度相比，E2H 的概率调度器通过**控制训练过程中不同难度任务的采样比例**，使模型在早期获得足够的简单任务训练信号以建立基础能力，同时避免在简单任务上过拟合（E2H-G 通过高斯衰减快速降低简单任务的采样概率）。与硬切换的传统课程学习相比，概率调度器允许**不同难度任务的持续混合**，防止灾难性遗忘。消融实验（Table 2）表明，E2H-G（$\sigma=0.25, \beta=0.75$）在 Blocksworld Hard 上达到 32.9%，显著优于平衡调度（21.1%）和传统课程学习（24.5%）。

### 创新点三：理论保证与样本效率

E2H 的理论分析（Section 3.3）在近似策略迭代（API）框架下，将最终策略的性能差距 $\mathcal{E}_K$ 分解为四项之和：收敛偏差、策略评估误差、策略更新误差和**课程近似误差** $\|Q_K^* - Q_k^*\|_{d_K}$（Theorem 3.1）。这一分解揭示了课程学习的双重优势：
- **样本效率提升**：简单任务具有更小的评估误差 $\delta_k$ 和策略更新误差 $\epsilon_k$，使早期阶段能以更少样本达到收敛。
- **平滑分布插值**：通过降低课程近似误差，确保从源分布到目标分布的平滑过渡。

Theorem 3.2 进一步给出了课程学习所需总样本数 $M_{CRL}$ 少于直接学习 $M_{Direct}$ 的充分条件：$\frac{(e \cdot l)^{2(1-K)} - 1}{1 - (e \cdot l)^2} < m - 1$，其中 $e$ 和 $l$ 分别刻画评估误差和 $L_k$ 的几何衰减率。实验（Table 8）实证验证了这一理论优势：E2H-G 仅使用 3,200 个 hard 样本即达到 32.9% 的 Blocksworld Hard 准确率，而直接训练基线使用 12,800 个 hard 样本仅达到 21.1%。

### 与 DAPO 的互补性

E2H 的课程学习策略与 DAPO（Yu et al., 2025）的算法改进是**正交且互补**的。DAPO 通过动态采样和优势裁剪解决了 GRPO 中零优势批次（advantage-zero batches）的问题，而 E2H 通过课程调度降低了训练初期的探索难度。两者结合时（Table 5），DAPO+E2H-G 在 Countdown Hard 上达到 43.7%，显著优于单独使用 DAPO（36.0%）或 GRPO+E2H-G（28.1%）。Figure 7 进一步显示，E2H 的课程调度能有效减少 DAPO 训练过程中的零优势批次占比，表明课程学习通过提供更易学习的初始任务，间接改善了策略优化的稳定性。



E2H Reasoner 的核心 pipeline 由三个模块串联构成，形成“分解—调度—优化”的闭环。

**1. 任务难度分解模块**  
输入为原始训练数据集，输出为按难度分级的四个子集：Trivial、Easy、Medium、Hard。对于具有人工标注的数据集（如 Blocksworld 按规划步数、Countdown 按操作数数量、MATH 按题目等级），直接依据标注划分；对于无标注的数据集（如 GSM8K、AQuA），则先使用基础模型在 CoT 提示下进行推理，根据错误率自动估计难度并分档（见 Figure 5、Figure 6）。这一分解的核心目的是降低训练过程中的分布偏移，使模型能够在低难度任务上先建立稳定的推理基础。

**2. 概率调度器**  
调度器决定在每个训练步 $t$ 从四个难度子集中采样的概率分布。E2H 提供两种调度策略：
- **余弦调度（E2H-C）**：非参数化策略，通过余弦函数控制概率从易到难的平滑过渡，在训练初期集中采样 Trivial 和 Easy 任务，后期逐步增加 Medium 和 Hard 的权重。
- **高斯调度（E2H-G）**：参数化策略，以高斯核定义采样概率 $\mathbf{S}_{\mathrm{Gaussian}}(t, k) = \exp\left(-\frac{(x_t - \mu_k)^2}{2\sigma^2}\right)$，其中 $x_t = \left(\frac{t}{T}\right)^\beta (K-1)$。通过调节 $\mu_k$、$\sigma$ 和 $\beta$ 可控制各难度任务的峰值位置与衰减速度，使 Trivial/Easy 任务的采样概率快速衰减，避免过拟合简单模式。

调度器的输出为每步采样的任务批次，送入下游的强化学习训练。

**3. GRPO/DAPO 强化学习训练**  
以调度器采样的任务为输入，使用策略优化算法（默认 GRPO，可替换为 DAPO）结合 LoRA 微调进行后训练。整个推理过程被建模为折扣 MDP：状态空间为所有合法 token 前缀，动作空间为词表，奖励函数为稀疏奖励——仅在模型输出完整的 `<answer>...</answer>` 并给出正确答案时给予非零奖励。训练过程中，模型从易到难逐步接触不同难度的推理任务，在稀疏奖励和分布偏移的双重挑战下建立从核心原理到复杂推理的能力递进。

**数据流总结**：  
`原始训练集 → [难度分解] → {Trivial, Easy, Medium, Hard} → [概率调度器] → 每步采样批次 → [GRPO/DAPO + LoRA] → 更新后策略`

这一框架的理论基础在于：课程学习通过构造中间难度的插值分布，缩小了从预训练源分布到目标困难分布的迁移差距，从而在理论上保证了更优的样本复杂度和收敛上界（Theorem 3.1, Theorem 3.2）。实验表明，E2H-G 在多个基准的困难子集和 OOD 任务上显著优于无课程的 GRPO 基线，且所需困难样本数大幅减少（Table 8），验证了框架设计的有效性。



### 3.1 任务难度分解模块

E2H Reasoner 的第一个核心模块是**任务难度分解**，其目标是将原始训练集划分为难度递增的子集，以降低强化学习过程中的分布偏移和奖励稀疏性。具体划分策略分为两种情况：

- **有人工难度标注的数据集**（如 Blocksworld、Countdown、MATH）：直接依据任务固有属性划分。例如，Blocksworld 按规划步长、Countdown 按操作数数量、MATH 按题目等级进行分档（Table 9）。
- **无人工标注的数据集**（如 GSM8K、AQuA）：通过基础模型在 CoT 提示下的**错误率**自动估计难度，并按四分位数将样本归入 trivial、easy、medium、hard 四个等级（Figure 5, Figure 6）。

该模块的消融实验（Table 1）表明，仅使用 hard 数据训练会导致模型在困难任务上表现极差（如 Blocksworld Hard 仅 2.6），而加入 trivial 和 easy 数据后，hard 准确率跃升至 21.1，验证了简单任务对学习核心推理原理的关键作用。

### 3.2 概率调度器

概率调度器是 E2H 的核心创新，负责在训练过程中动态调整不同难度任务的采样比例。论文提出了两种调度策略，并与基线策略进行了对比。

#### 基线调度策略

- **平衡调度（Balanced Scheduling）**：均匀混合所有难度数据，采样概率恒定：
  $$S_{\text{balanced}}(t, k) = \frac{1}{K}$$
  其中 $K$ 为难度等级数，$k \in \{0, \dots, K-1\}$ 表示难度索引。

- **传统课程学习（Traditional CL）**：按固定时间阈值 $\tau_k$ 顺序切换难度：
  $$S_{\text{trad}}(t, k) = \begin{cases} 1, & \tau_k \leq t < \tau_{k+1} \\ 0, & \text{否则} \end{cases}$$

#### 余弦调度器（E2H-C）

余弦调度器是一种非参数策略，通过余弦函数平滑插值各难度任务的采样权重：
$$S_{\text{cosine}}(t, k) = \alpha_t \cdot (K - k - 1) + (1 - \alpha_t) \cdot k$$
$$\alpha_t = \frac{1}{2} \left(1 + \cos\left(\frac{t}{T} \pi\right)\right)$$

其中 $t$ 为当前训练步，$T$ 为总训练步数。训练初期 $\alpha_t \approx 1$，采样偏向低难度任务；随着训练推进，$\alpha_t$ 逐渐衰减至 0，采样重心向高难度转移。该调度器旨在缓解奖励稀疏和灾难性遗忘（Section 3.2）。

#### 高斯调度器（E2H-G）

高斯调度器引入参数化控制，通过高斯核定义采样概率：
$$S_{\text{Gaussian}}(t, k) = \exp\left(-\frac{(x_t - \mu_k)^2}{2\sigma^2}\right)$$
$$x_t = \left(\frac{t}{T}\right)^\beta (K - 1)$$

其中 $\mu_k$ 为第 $k$ 级难度的中心位置，$\sigma$ 控制采样宽度，$\beta$ 控制时间变量的非线性增长速率。Figure 4 展示了不同超参数组合下采样概率随训练步的变化：$\beta$ 越大，早期越集中于简单任务；$\sigma$ 越小，各阶段采样越集中。

**关键区别**：E2H-C 后期仍保留对简单任务的少量采样（防止遗忘），而 E2H-G 可通过调整 $\sigma$ 快速衰减简单任务的采样概率，使模型更早聚焦困难任务。Table 2 的消融显示，E2H-G (0.25, 0.75) 在 Blocksworld Hard 上达 32.9，E2H-G (0.5, 0.5) 在 Countdown Hard 上达 41.0，均显著优于平衡调度和传统 CL。

### 3.3 强化学习训练模块

E2H 的强化学习训练基于策略优化框架，将 LLM 推理过程建模为折扣马尔可夫决策过程（MDP）：
$$\mathcal{M} = (\mathcal{S}, \mathcal{A}, P, r, \gamma)$$

- **状态空间 $\mathcal{S}$**：所有有效 token 前缀序列 $s_t = (x_0, x_1, \dots, x_t)$。
- **动作空间 $\mathcal{A}$**：词汇表 $\Sigma$。
- **策略 $\pi_\theta$**：预训练 LLM 的条件分布 $\pi_\theta(x_{t+1} | s_t) = p_\theta(x_{t+1} | x_0, \dots, x_t)$。
- **奖励函数 $r$**：稀疏奖励——所有中间状态 $r(s, a, s') = 0$，仅在模型生成最终答案 $y$（由 `<answer></answer>` 包裹）时给予非零奖励 $r(y)$。

论文主要使用 **GRPO**（Guo et al., 2025）作为基础 RL 算法，并在消融中结合 **DAPO**（Yu et al., 2025）验证互补性。训练采用 LoRA 微调，超参数统一配置（Table 10）。

### 3.4 理论保证：性能界与样本复杂度

E2H 的理论分析基于**近似策略迭代（API）**框架，在以下假设下展开（Section 3.3.1）：
- 近似策略评估误差有界：$\| \hat{Q}_k^{\pi_k} - Q_k^{\pi_k} \|_\infty \leq \delta_k$
- 近似贪婪策略改进误差有界：$\mathbb{E}_{s \sim \mu_k}[Q^{\pi_{k+1}}(s, \pi_{k+1}(s))] \geq \mathbb{E}_{s \sim \mu_k}[\max_a \hat{Q}_k(s, a)] - \epsilon_k$
- 分布偏移受控（concentrability）
- 课程漂移有界

**定理 3.1（性能差距上界）**：经过 $K$ 阶段课程学习后，最终策略 $\pi_K$ 与最优策略 $\pi_K^*$ 的性能差距满足：
$$\mathcal{E}_K \leq \sum_{k=1}^K \left( \gamma^T \eta_k + \frac{2\gamma(1-\gamma^T)}{(1-\gamma)^2} \delta_k + \frac{2\gamma}{\beta(1-\gamma)^2} \right) + \sum_{k=1}^{K-1} \| Q_K^* - Q_k^* \|_{d_K}$$

该界由四部分组成：收敛偏差（$\gamma^T \eta_k$）、评估误差项（含 $\delta_k$）、策略更新误差项、以及**课程近似误差** $\| Q_K^* - Q_k^* \|_{d_K}$。课程学习的核心优势在于：简单任务上 $\delta_k$ 和 $\epsilon_k$ 更小（样本效率更高），且课程近似误差可通过合理设计调度器控制。

**定理 3.2（样本效率条件）**：在几何误差分配假设下，课程学习所需总样本数 $M_{CRL}$ 少于直接学习 $M_{Direct}$ 的条件为：
$$M_{CRL} < M_{Direct} \iff \frac{(e \cdot l)^{2(1-K)} - 1}{1 - (e \cdot l)^2} < m - 1$$

其中 $e$ 为误差衰减因子，$l$ 为每阶段样本分配比例，$m$ 为直接学习的样本倍数。该条件表明，当课程阶段数 $K$ 足够且误差衰减合理时，课程学习具有严格的样本效率优势。Table 8 的实验结果与此一致：E2H-G 仅需 2,400 个 hard 样本即达到 32.9 的 Blocksworld Hard 准确率，而 GRPO（All）使用 8,000 个 hard 样本仅达 21.1。



## 实验与关键发现

### 核心瓶颈与实验动机

大语言模型在困难推理任务上直接使用强化学习（如GRPO）时，面临两个根本性挑战：**严重稀疏奖励**和**分布偏移**。由于奖励仅在最终答案正确时给出，模型从零开始探索困难任务时几乎收不到有效反馈，导致训练不稳定且容易过拟合。E2H Reasoner通过从易到难的课程学习，逐步建立推理能力，从机制上缓解了这一问题。

### 主实验结果

**Table 3** 展示了E2H Reasoner在三个模型（Qwen 1.5B、Qwen 3B、LLaMA 3.2 3B）上的核心结果。在Blocksworld的Hard子集上，E2H-G将Qwen 1.5B的准确率从GRPO的21.1%提升至32.9%（+11.8），在OOD任务上从2.6%提升至7.3%。Countdown上同样显著：Hard准确率从18.1%提升至28.1%（+10.0）。MATH数据集上，E2H-G在Hard子集达到48.7%，相比GRPO的46.3%有稳定提升。


![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KJvHnl3kUv/figures/012_Table_3.jpg]]
*Table 3: Results of E2H Reasoner across three models on Blocksworld (Valmeekam et al., 2023), Countdown (Gandhi et al., 2024) and MATH Hendrycks et al. (2021). Our method consistently improves performance especially on HARD and OOD tasks, demonstrating effective reasoning, results on more models are in Appendix G.1. Best numbers are in bold and second-best are underlined. Figure 5: GSM8K difficulty distribution based on error rates. Difficulty groups used for training are derived from quartiles of this distribution*

**Table 4** 报告了GSM8K和AQuA上的结果。由于这两个数据集缺乏人工难度标注，难度分档基于模型在CoT提示下的错误率自动划分（见**Figure 5**）。E2H-G在GSM8K上平均准确率达到78.7%，显著优于GRPO的67.7%（+11.0）；在AQuA上平均准确率为66.1%，优于GRPO的63.3%。


![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KJvHnl3kUv/figures/013_Table_4.jpg]]
*Table 4: Performance of E2H Reasoner on GSM8K and AQuA, where difficulty splits are derived from error rates due to the absence of human labels. Fig. 5 shows these splits, and Table 15 confirms robustness to the number of splits*

**Table 7** 评估了在MATH上训练的模型向AIME24和OlympiadBench的泛化能力。E2H-G在AIME24上Pass@1为6.7%，是GRPO（3.3%）的两倍以上，验证了课程学习对分布外泛化的促进作用。

### 消融实验

#### 任务分解的必要性

**Table 1** 消融了不同难度数据组合的影响。仅使用Hard数据训练时，模型在Blocksworld Hard上仅达7.6%；加入Medium数据后提升至17.0%；进一步加入Easy和Trivial数据后达到21.1%。这一趋势在Countdown和MATH上一致，证明简单任务帮助模型学习核心推理原理，从而赋能困难任务。


![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KJvHnl3kUv/figures/010_Table_1.jpg]]
*Table 1: Impact of task decomposition for LLM post-training. Trivial and easy examples help the model learn core principles that enable success on harder tasks*

#### 调度策略的对比

**Table 2** 系统对比了四种调度策略：平衡调度、传统课程学习（CL）、余弦调度（E2H-C）和高斯调度（E2H-G）。E2H-G在Countdown Hard上达到41.0%，远超平衡调度的18.1%和CL的28.3%；在MATH Hard上E2H-G达到48.7%，同样最优。E2H-C在Blocksworld上表现较好（Hard 32.9%），但在Countdown上因简单任务过拟合导致Hard性能下降。高斯调度通过快速衰减简单任务的采样概率，有效避免了这一问题。


![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KJvHnl3kUv/figures/011_Table_2.jpg]]
*Table 2: Effect of scheduling strategies in LLM post-training. We compare balanced scheduling, traditional curriculum learning (CL), and our proposed E2H Reasoner variants, namely, E2H-G and E2H-C. CoT is reported as a reference*

#### 与DAPO的互补性

**Table 5** 和**Table 6** 展示了E2H与DAPO的结合效果。DAPO+E2H-G在Blocksworld Hard上达到35.1%，优于单独DAPO的26.2%和单独E2H-G的32.9%。**Figure 7** 进一步显示，E2H-G和E2H-C均能显著减少训练过程中零优势批次（advantage-zero batches）的占比，表明课程学习通过提供更稳定的梯度信号与DAPO形成互补。


![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KJvHnl3kUv/figures/015_Table_5.jpg]]
*Table 5: Ablation of E2H on GRPO vs DAPO. E2H improves overall performance over both baselines and yields consistent gains when combined with DAPO, indicating that the two approaches are complementary*

#### 样本效率验证

**Table 8** 直接验证了理论上的样本效率优势。所有方法的总训练样本数固定为12,800。GRPO（HARD）将所有样本投入困难任务，但E2H-G仅使用3,580个困难样本就实现了更优性能。E2H-C使用3,200个困难样本同样优于非课程基线。这证实了课程学习在样本复杂度上的优势：通过从易到难的渐进训练，模型用更少的困难样本学到更强的推理能力。


![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_KJvHnl3kUv/figures/018_Table_8.jpg]]
*Table 8: Consistent with our theoretical guarantees, CRL methods (E2H-C, E2H-G) attain strong performance while requiring substantially fewer hard samples than non-curriculum baselines. For example, E2H-G uses 3580 hard samples versus 12800 for GRPO (HARD). Training exclusively on OOD (GRPO-OOD) trained on 12800 OOD samples performs poorly (see Table 3)*

### 失败模式与局限

1. **非自适应调度**：高斯和余弦调度器均为预定义的静态策略，不会根据训练过程中的模型能力动态调整。在Countdown上，E2H-C因简单任务采样时间过长导致过拟合，Hard性能反而下降（Table 2），暴露了固定调度的脆弱性。

2. **超参数敏感性**：高斯调度器的参数（μ, σ, β）和难度分档数需要人工调整。**Table 15** 显示方法对分档数（3/4/5）具有一定鲁棒性，但最优参数仍依赖任务特性。

3. **调度器选择的权衡**：**Table 16** 定性总结了各调度策略的优缺点。余弦调度无参数但容易过拟合简单任务；高斯调度灵活但引入了额外超参数；自适应方法（如Self-Evolve）理论上更优，但在本实验中性能不如E2H-G，可能因其动态调整机制在稀疏奖励下不够稳定。

### 关键图表结论

- **Figure 1(a,b)**：E2H在Pass@k评估中不仅在低k值下提升准确率，在高k值下同样优于基座模型，表明课程学习使模型真正掌握了可泛化的推理能力。
- **Figure 2**：任务分解示意——训练集被划分为trivial、easy、medium、hard四个难度级别，模型从易到难逐步学习。
- **Figure 4**：高斯采样过程可视化，展示了不同超参数下各难度任务的采样概率随训练步数的变化曲线。
- **Figure 7**：DAPO+E2H组合显著降低零优势批次比例，提供了课程学习稳定训练动态的直接证据。



## 定位与知识库关联

### 方法关系与谱系定位

E2H Reasoner 处于大语言模型强化学习后训练与课程学习两条线的交汇点。其核心训练算法直接建立在 **GRPO**（Guo et al., 2025）之上，并与 **DAPO**（Yu et al., 2025）形成互补关系。在课程学习维度，E2H 与两类基线形成对比：一类是**传统课程学习（Traditional CL）**，采用固定顺序的阶段式调度；另一类是**自适应课程方法 Self-Evolve**（Chen et al., 2025），通过维持 50% 解决率动态调整采样难度。

与 GRPO 的默认平衡采样策略不同，E2H 将训练数据按难度分解为 trivial、easy、medium、hard 四级，并通过概率调度器（余弦调度 E2H-C 或高斯调度 E2H-G）控制各难度任务的采样比例。消融实验（Table 5）表明，E2H 在 GRPO 和 DAPO 上均带来一致提升，且结合 DAPO 后训练过程中零优势批次的占比显著下降（Figure 7），说明课程学习与 DAPO 的改进策略是互补的而非替代关系。

与 Self-Evolve 的自适应机制相比，E2H 的调度器是非自适应的——高斯和余弦调度在训练开始前即已确定，不会根据训练过程中的模型能力动态调整。Table 2 的结果显示，在困难任务上 E2H-G 和 E2H-C 均优于 Self-Evolve，但这并不意味着非自适应调度本质更优，而是表明精心设计的静态调度在样本效率和最终性能上可以超越简单的自适应策略。

### 适用边界与局限

E2H 的有效性建立在两个前提之上：一是训练数据能够被合理地按难度分解，二是难度分档与调度器超参数被恰当设置。对于具备人工难度标注的任务（如 Blocksworld 按规划步数、Countdown 按操作数数量、MATH 按题目等级），分解是直接的。对于无标注任务（如 GSM8K、AQuA），论文采用模型在 CoT 提示下的错误率自动估计难度，并按分位数划分。Table 15 的鲁棒性消融显示方法对分档数不敏感，但这一结论仅在 GSM8K 上验证，在其他任务类型上的推广性需要手动确认。

方法的另一关键局限在于调度器的非自适应性。高斯调度器的形状由参数 ω 和 ε 控制（分别决定简单任务概率衰减速度和困难任务峰值位置），余弦调度器则完全无参数。这些超参数需要人工调优，且最优配置因任务而异：例如在 Blocksworld 上 E2H-G(0.25, 0.75) 最优，而在 Countdown 和 MATH 上 E2H-G(0.5, 0.5) 最优（Table 2）。论文明确指出，与最大化可学习性的自适应课程方法结合可能进一步提升性能，但这一方向尚未被探索。

### 开放问题

1. **自适应调度**：能否设计基于训练过程信号（如优势值、模型能力估计、任务解决率变化）的自适应调度器，在保持 E2H 样本效率优势的同时减少超参数调优负担？

2. **与可学习性课程结合**：E2H 的调度基于难度排序，而最大化可学习性的课程方法基于模型当前能力选择最优挑战级别。两者的结合机制和理论性质尚不明确。

3. **大规模扩展性**：当前实验主要在 Qwen 1.5B/3B 和 LLaMA 3.2 3B 规模上验证，E2H 在更大模型（如 7B+）和更多样化任务上的表现及调度器参数迁移规律需要进一步研究。

4. **理论条件的实际验证**：Theorem 3.2 给出了课程学习样本复杂度优于直接学习的条件 $M_{CRL} < M_{Direct} \iff \frac{(e*l)^{2(1-K)}-1}{1-(e*l)^2} < m-1$，其中涉及几何误差分配假设。在实际大规模训练中该条件是否成立，以及如何根据该条件指导超参数选择，仍是开放问题。



## 原文 PDF

![[paperPDFs/ICLR_2026/Curriculum_Reinforcement_Learning_from_Easy_to_Hard_Tasks_Improves_LLM_Reasoning.pdf]]
