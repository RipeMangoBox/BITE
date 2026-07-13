---
title: "Buffer Matters: Unleashing the Power of Off-Policy Reinforcement Learning in Large Language Model Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Buffer_Matters_Unleashing_the_Power_of_Off_Policy_Reinforcement_Learning_in_Large_Language_Model_Reasoning.pdf
project_link: null
code_link: null
openreview_forum_id: RduOiisl1S
aliases:
- BBAPO
- BMUPOPRLLLMR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过引入离策略经验重放缓冲区，并设计自适应批次构建机制——动态过滤在线零方差样本（X₁）、周期性重新评估历史困难样本并选取有提升者（X₂），以及从近三步骤的高质量缓冲区中随机采样以填补批次容量（X₃）——打破奖励同质化，同时提高数据复用效率，在保证理论下界的情况下稳定提升策略。"
primary_logic: "维持训练批次中足够的奖励方差和适当的难度分布是RLVR成功的关键，而单纯依赖在线采样难以满足。BAPO通过难度感知的历史缓冲区选择性复用，将高方差的历史样本重新注入训练，既不引入过多旧策略偏差（通过FIFO和TV约束），又显著提升了模型对困难问题的解决能力，并且该方法的结构逻辑优于具体超参数调参。"
claims:
- "BAPO在数学、规划和视觉推理任务上平均比GRPO提升12.5%。"
- "BAPO成功解决了基模型完全无法解答的问题的40.7%。"
- "BAPO的性能提升主要源于离线组件的结构逻辑，而非特定的超参数设置。"
- "即使在参数自由的“迷你测试”中，BAPO仍明显优于GRPO。"
---

# Buffer Matters: Unleashing the Power of Off-Policy Reinforcement Learning in Large Language Model Reasoning

> [!tip] 核心洞察
> 维持训练批次中足够的奖励方差和适当的难度分布是RLVR成功的关键，而单纯依赖在线采样难以满足。BAPO通过难度感知的历史缓冲区选择性复用，将高方差的历史样本重新注入训练，既不引入过多旧策略偏差（通过FIFO和TV约束），又显著提升了模型对困难问题的解决能力，并且该方法的结构逻辑优于具体超参数调参。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 缓冲区至关重要：释放大语言模型推理中离线策略强化学习的潜力 |
| 英文题名 | Buffer Matters: Unleashing the Power of Off-Policy Reinforcement Learning in Large Language Model Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=RduOiisl1S) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | BAPO (Batch Adaptation Policy Optimization) |
| Dataset | 多任务平均提升, AIME24 (数学), MATH500 (数学), Countdown-3to4 (规划) |

> [!tip] 效果简介
> - 多任务平均提升 上，相对GRPO的准确率提升 为 +12.5%，对比 GRPO，变化 +12.5%。
> - AIME24 (数学) 上，Accuracy (%) 为 38.54，对比 30.73 (GRPO)，变化 +7.81。
> - MATH500 (数学) 上，Accuracy (%) 为 89.18，对比 85.40 (GRPO)，变化 +3.78。

## 概要

### 问题瓶颈

在大语言模型的推理能力训练中，以GRPO为代表的在线策略强化学习微调范式已成为主流。然而，该范式存在两个根本性的效率瓶颈：

1. **奖励同质化导致梯度消失**：当组内所有样本的奖励完全一致（全对或全错）时，优势估计归零，模型无法获得有效的学习信号。
2. **经验严重浪费**：在线策略遵循“一次使用即丢弃”的原则，高方差或困难样本仅被使用一次即被抛弃，导致训练数据利用率极低，尤其对困难样本几乎无提升。

### 核心方法：BAPO

本文提出**BAPO（Batch Adaptation Policy Optimization）**，一种离策略强化学习微调框架，通过难度感知的经验重放机制解决上述瓶颈。其核心思路是：维持训练批次中足够的奖励方差和适当的难度分布，而单纯依赖在线采样难以满足这一条件。

BAPO引入三个关键组件来构建自适应训练批次：
- **在线过滤（X₁）**：剔除奖励方差为零的样本组，保留具有有效学习信号的在线样本。
- **困难样本重利用（X₂）**：周期性用当前策略重新评估历史困难样本，选取出现提升的样本重新注入训练。
- **高质量样本复用（X₃）**：从近三步的高质量缓冲区中随机采样，填充批次容量，提高数据复用效率。

该方法通过FIFO机制和总变分距离约束控制旧策略偏差，在保证理论下界的情况下稳定提升策略。

### 核心结论

1. **显著性能提升**：BAPO在数学、规划和视觉推理任务上平均比GRPO提升**12.5%**，成功解决了基模型完全无法解答的问题的**40.7%**。
2. **结构优势主导**：性能提升主要源于离策略组件的结构逻辑，而非特定的超参数设置；即使在参数自由的“迷你测试”中，BAPO仍明显优于GRPO。
3. **困难样本攻克**：移除历史困难样本重利用（X₂）导致性能下降约**21%**，证明针对性攻克困难样本至关重要。
4. **计算效率可控**：BAPO的训练总时间与GRPO相当，且所需推理量远低于DAPO。
5. **算法无关性**：将BAPO的批次构建范式泛化到PPO（BA-PPO），在AIME 2024上比标准PPO高出**+5.5个点**，证明该范式是算法无关的增强。

### 方法定位

在RLVR方法谱系中，BAPO位于在线策略与离策略方法的交叉地带。与纯在线方法（GRPO、DAPO、MoPPS）相比，BAPO引入了历史经验复用；与现有离策略方法（GRPO v=5、RePO、Remix-GRPO）相比，BAPO的关键区别在于**难度感知的自适应批次构建**——不是简单地混合或检索历史样本，而是根据样本的奖励方差和难度动态决定哪些历史样本值得重新注入训练。这一设计使得BAPO在保持计算效率的同时，显著提升了对困难问题的解决能力。



大语言模型（LLM）的推理能力近年来取得了显著进展，但仅靠监督微调（SFT）往往难以突破性能瓶颈。强化学习（RL）后训练，特别是基于结果奖励的强化学习与可验证奖励（RLVR），已成为提升LLM复杂推理能力的关键范式。然而，当前主流的在线策略（on-policy）RLVR框架存在两个根本性的效率瓶颈，严重制约了训练效果。

**瓶颈一：奖励同质化导致梯度消失。** 在典型的在线策略RLVR框架（如GRPO）中，模型对每个提示生成一组回复，并通过组内相对优势估计来提供学习信号。优势函数的计算依赖于组内奖励的方差：当一组回复全部正确或全部错误时，奖励方差为零，优势估计也为零，导致该批次样本无法提供任何有效的梯度更新。这种“奖励同质化”现象在训练过程中频繁出现，尤其随着模型能力提升，全对样本的比例逐渐增加，使得大量计算资源被浪费在无效的更新上。

**瓶颈二：经验浪费与困难样本的“遗忘”。** 在线策略框架遵循“一次使用即丢弃”的原则——每个训练步骤生成的样本仅用于当前步的参数更新，随后便被丢弃。这种设计造成了严重的数据浪费：高方差样本（如部分正确的困难问题）和模型暂时无法解决的极难样本，往往只被利用一次。如图1所示，在GRPO训练前后，准确率分组（0/8到8/8）的样本分布变化表明，基础模型完全无法解决（0/8准确率）的困难样本在训练后改善十分有限，大量困难样本始终停留在低准确率区间，未能得到有效的针对性学习。

上述两个瓶颈相互耦合，形成了一个恶性循环：奖励同质化使得在线采样中有效学习信号稀疏，而经验浪费则导致那些真正蕴含学习价值的困难样本无法被重复利用。尽管已有工作尝试通过离策略（off-policy）机制来缓解这一问题——例如GRPO（v=5）（Mroueh et al., 2025）通过延迟策略同步引入准离策略数据流，RePO（Li et al., 2025）利用检索策略从缓冲区采样，Remix-GRPO（Liang et al., 2025）以固定比例混合历史样本——但这些方法或缺乏对样本难度的感知，或未能系统性地解决奖励同质化和困难样本针对性训练的问题。

**本文动机。** 基于上述分析，本文的核心洞察是：维持训练批次中足够的奖励方差和适当的难度分布是RLVR成功的关键，而单纯依赖在线采样难以满足这一要求。为此，本文提出BAPO（Batch Adaptation Policy Optimization），一种离策略RLVR框架，通过难度感知的历史缓冲区选择性复用，将高方差的历史样本重新注入训练，在保证策略一致性（通过FIFO机制和总变分距离约束）的前提下，显著提升模型对困难问题的解决能力。该方法的结构逻辑——而非具体的超参数调优——是实现性能增益的根本原因。



## 核心方法与创新机理

BAPO 的核心创新在于**将离策略（off-policy）经验重放机制系统性地引入大语言模型推理的强化学习后训练**，通过三个相互协同的“changed slots”从根本上解决在线策略 RLVR 框架的两大效率瓶颈：奖励同质化导致的梯度消失，以及“一次使用即丢弃”造成的高方差/困难样本浪费。

### 1. 在线样本方差过滤（X₁）：打破奖励同质化

传统 GRPO 目标函数中，优势估计 $\hat{A}_{i,t}$ 依赖于组内奖励的标准化（Equation 2）。当组内 $G$ 条回复全部正确或全部错误时，奖励方差为零，优势估计退化为零向量，该批次对策略更新不产生任何有效梯度。

BAPO 引入**在线过滤器**，在构建训练批次前显式剔除这些零方差样本。具体地，仅保留组平均奖励满足 $\mu_{\alpha,r}(x) \in [1/G, (G-1)/G]$ 的提示-回复组，即剔除全对（$\mu=1$）和全错（$\mu=0$）的极端情况。这一操作直接切断了奖励同质化向梯度消失的因果链路，确保进入训练的每个样本都携带非零学习信号。

### 2. 历史困难样本重新评估（X₂）：攻克“无法解决”问题

GRPO 框架下，基模型完全无法解答的问题（准确率 0/8）在训练中几乎得不到改善——Figure 1 清晰展示了这一“困难样本固化”现象。BAPO 的核心应对策略是维护一个**困难样本缓冲区** $\mathcal{B}_{\text{bad}}$，并周期性地（每 $m$ 步）用当前策略 $\pi_{\theta_t}$ 对这些历史难题重新生成回复，仅选取出现可观测提升的样本（$c_1 < \mu_{\pi_{\theta_t},r}(x) < 1$）作为 X₂ 子集注入训练批次。

这一机制的关键因果效应在于：困难样本不再被单次采样后丢弃，而是获得了“二次机会”。当策略能力逐步提升后，原本无法解决的题目可能产生部分正确回复，这些**从“全错”过渡到“部分正确”的样本恰恰携带最高的奖励方差**（Proposition A.3 证明 $\mu=1/2$ 时方差最大化），为策略改进提供了最强的单步学习信号。消融实验证实，移除 X₂ 导致性能下降约 21%（Figure 6），验证了针对性攻克困难样本的决定性作用。

### 3. 高质量历史样本复用（X₃）：提升数据效率与训练稳定性

在线过滤剔除零方差样本后，实际可用样本数往往低于配置的批次容量，造成训练效率损失。BAPO 通过维护一个 **FIFO 高质量缓冲区** $\mathcal{B}_{\text{high}}$ 来解决这一问题：仅保留近三个训练步内的高质量轨迹（$c_2 \leq \mu \leq c_3$），从中随机采样以填充批次剩余容量。

该设计的精妙之处在于**双重约束机制**：
- **时效性约束**（FIFO + 三步窗口）：确保复用样本的生成策略与当前策略的总变分距离有界，避免引入过大的离策略偏差。
- **质量阈值动态映射**（Equation 8）：随着全局平均性能 $r_{\text{tot}}$ 的提升，高质量阈值 $c_2, c_3$ 通过线性映射从“较易”区间向“较难”区间滑动，使缓冲区始终提供具有适当难度的样本，避免训练后期因样本过于简单而失去学习价值。

准确率迁移矩阵（Figure 15）为 X₃ 的安全性提供了强证据：初始达到 8/8 准确率的样本在整个训练过程中极少退化到低分段，证明高质量历史样本的复用不会引入噪声或导致性能倒退。

### 4. 推理策略延迟同步（$v=5$）：准离策略数据流

BAPO 将推理策略 $\alpha$ 与训练策略 $\pi_\theta$ 的同步延迟 $v$ 步（默认 $v=5$）。这一设计将完全在线（$v=1$）的数据流转变为**准离策略**模式：推理策略的更新频率降低，减少了同步开销，同时增加了样本来源的策略多样性。理论分析（Section 3.3）通过总变分距离约束 $\text{TV}(\pi_{\theta_t}, \pi_{\theta_{t-v}}) \leq \delta_1$ 保证了该延迟不会破坏训练稳定性。消融实验表明，在合理范围内（$v=5, m=5$）性能保持稳定，仅当延迟极端增大导致策略偏差过大时才会出现性能下降。

### 5. 结构逻辑优于超参数调参

BAPO 的创新本质在于**批次构建的结构逻辑**，而非特定超参数设置。论文通过“迷你测试”（Mini-test）验证了这一点：在完全剥离超参数（仅使用标准零优势过滤、重放历史全错样本、复用 $\mu=0.5$ 样本）的条件下，BAPO 仍显著优于 GRPO（Figure 5）。此外，将该批次构建范式泛化到 PPO（BA-PPO）在 AIME 2024 上比标准 PPO 高出 +5.5 个点（Figure 16），证明这是一种算法无关的增强策略。



![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_RduOiisl1S/figures/003_Figure_2.jpg]]
*Figure 2: The overview of the (a) on-policy and (b) offpolicy RL Post-training framework*

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_RduOiisl1S/figures/004_Figure_3.jpg]]
*Figure 3: The workflow of (a) off-policy rollout and (b) off-policy training in our RLVR framework*

BAPO（Batch Adaptation Policy Optimization）是一个以**离线策略推断 + 自适应批次构建**为核心的RLVR后训练框架。其设计直指在线策略RLVR（如GRPO）的两大效率瓶颈：**奖励同质化**导致的梯度消失，以及**经验严重浪费**导致的困难样本难以改善。BAPO通过将训练流程拆解为离线策略推断阶段和自适应批次构建阶段，在不引入过多旧策略偏差的前提下，系统性提升训练信号的多样性和数据复用效率。

### 离线策略推断阶段

BAPO采用**延迟同步的推理策略**进行样本生成。具体而言，训练策略 $\pi_{\theta_t}$ 每步更新，而用于生成在线样本的推理策略 $\alpha$ 则延迟 $v$ 步同步（$v=5$），形成准离策略数据流。对于每个提示 $x$，推理策略 $\alpha$ 生成 $G$ 条回复（$G=8$），并计算每条回复的对数概率和奖励。这一设计降低了同步开销，同时增加了在线样本的多样性。为了控制策略偏差，BAPO在理论上约束了当前策略与延迟推理策略之间的总变分距离：$TV(\pi_{\theta_t}(\cdot|x), \pi_{\theta_{t-v}}(\cdot|x)) \leq \delta_1$（对所有 $x \in \mathcal{X}_1$ 成立），从而为后续离策略训练提供稳定性保证。

### 缓冲区体系

BAPO维护两类历史经验缓冲区，以存储离线策略推断阶段产生的轨迹：

- **高质量缓冲区 $\mathcal{B}_{\mathrm{high}}$**：采用FIFO机制，仅保留近三步的高质量轨迹。缓冲区中每个条目存储提示、回复、奖励以及生成时的策略概率 $\alpha_B(y|x)$，以便后续计算重要性采样比 $\rho_{\alpha_B}(\theta) = \frac{\pi_\theta(y|x)}{\alpha_B(y|x)}$，修正历史样本与当前策略之间的分布差异。
- **困难样本缓冲区 $\mathcal{B}_{\mathrm{bad}}$**：存储历史上表现极差（组平均奖励 $\mu_{\alpha,r}(x) \leq c_1$）的提示，用于周期性重新评估和针对性攻克。

### 自适应批次构建阶段

这是BAPO的核心创新。训练批次由三个子集动态合并而成，通过一个统一的指示函数 $I(x)$ 进行样本选择：

$$
I(x) = \underbrace{\mathbf{1}_{\{\frac{1}{G} \leq \mu_{\alpha,r}(x) \leq \frac{G-1}{G}\}}}_{\text{过滤的新鲜样本 } \mathcal{X}_1} + \underbrace{\mathbf{1}_{\{\mu_{\alpha_B,r}(x) \leq c_1 \wedge \mu_{\pi_{\theta_t},r}(x) > c_1\}}}_{\text{改善的历史困难样本 } \mathcal{X}_2} + \underbrace{\mathbf{1}_{\{c_2 \leq \mu_{\alpha_B,r}(x) \leq c_3\}}}_{\text{历史高质量样本 } \mathcal{X}_3}
$$

**子集 $\mathcal{X}_1$（过滤的新鲜样本）**：从在线推断批次中剔除奖励方差为零的样本——即组内全部正确（$\mu=1$）或全部错误（$\mu=0$）的提示。这些零方差样本会导致优势估计 $\hat{A}_{i,t}$ 为零，无法提供有效梯度。保留组平均奖励满足 $\mu_{\alpha,r}(x) \in [1/G, (G-1)/G]$ 的样本，确保训练信号中始终存在足够的奖励方差。

**子集 $\mathcal{X}_2$（改善的历史困难样本）**：每 $m$ 步（$m=5$），从困难缓冲区 $\mathcal{B}_{\mathrm{bad}}$ 中取出提示，用当前策略 $\pi_{\theta_t}$ 重新生成回复，并仅保留在当前策略下组平均奖励提升到 $c_1$ 以上且未达到满分（$\mu < 1$）的样本：

$$
\mathcal{X}_2 = \left\{ (x, y') \mid (x, y) \in \mathcal{B}_{\mathrm{bad}}, y' \sim \pi_{\theta_t}(\cdot \mid x), c_1 < \mu_{\pi_{\theta_t}, r}(x) < 1 \right\}
$$

这一机制将曾被放弃的困难样本重新注入训练，且仅在模型确实取得进步时才纳入批次，避免无效噪声。

**子集 $\mathcal{X}_3$（历史高质量样本）**：当 $\mathcal{X}_1$ 和 $\mathcal{X}_2$ 不足以填满配置的批次容量 $B$ 时，从高质量缓冲区 $\mathcal{B}_{\mathrm{high}}$ 中随机采样以填补剩余容量：

$$
\mathcal{X}_3 = \mathcal{S}\left(\mathcal{B}_{\mathrm{high}}, \min\left(|\mathcal{B}_{\mathrm{high}}|, B - |\mathcal{X}_1| - |\mathcal{X}_2|\right)\right)
$$

高质量阈值的定义采用**自适应线性映射**：$c_i = r_{\mathrm{tot}} \cdot (c_i^{\mathrm{high}} - c_i^{\mathrm{low}}) + c_i^{\mathrm{low}}$（$i \in \{2,3\}$），其中 $r_{\mathrm{tot}}$ 为全局平均性能。随着模型整体能力提升，高质量阈值从较易区间向较难区间滑动，确保复用的样本始终具有适当的难度。

### 策略更新

最终训练批次 $\mathcal{X}_1 \cup \mathcal{X}_2 \cup \mathcal{X}_3$ 被送入策略更新阶段。BAPO的联合训练目标为：

$$
\mathcal{L}_{\alpha}(\pi_\theta) = \underbrace{\mathbb{E}_{(x,y) \sim \alpha}\left[\rho_{\alpha}(\theta) \cdot \hat{A}(x,y)\right]}_{\text{在线样本贡献}} + \underbrace{\mathbb{E}_{(x,y) \sim \mathcal{B}}\left[\rho_{\alpha_B}(\theta) \cdot \hat{A}(x,y)\right]}_{\text{历史样本贡献}} - \beta \cdot \mathbb{D}_{\mathsf{KL}}(\pi_\theta \| \alpha)
$$

其中优势估计 $\hat{A}_{i,t} = \frac{r_i - \mathrm{mean}(\{r_\ell\})}{\sqrt{\mathrm{std}^2(\{r_\ell\}) + \varepsilon}}$ 沿用组内标准化方式。历史样本通过重要性采样比 $\rho_{\alpha_B}(\theta)$ 修正分布偏移，KL惩罚项约束策略不会偏离推理策略 $\alpha$ 过远。

### 模块关系与数据流

整个pipeline的模块关系可概括为：**离线策略推断** → **在线过滤（$\mathcal{X}_1$）** → **困难样本周期性重评估（$\mathcal{X}_2$）** → **高质量样本回放（$\mathcal{X}_3$）** → **自适应批次合并** → **策略更新**。三个子集相互补充：$\mathcal{X}_1$ 提供当前策略下的高方差学习信号，$\mathcal{X}_2$ 针对性攻克历史遗留的困难问题，$\mathcal{X}_3$ 作为稳定填充防止批次欠采样。实验表明，实际训练中约40-60%的批次样本来自在线过滤（$\mathcal{X}_1$），剩余部分由 $\mathcal{X}_2$ 和 $\mathcal{X}_3$ 动态补充（Figure 14），且总批次大小在训练过程中频繁低于最大配置容量（Figure 8），印证了自适应构建机制的必要性。



### 问题根源：奖励同质化与经验浪费

在线策略RLVR框架（以GRPO为代表）的核心训练信号来自组内相对优势估计。给定一个提示 $x$ 的 $G$ 条回复，其优势函数为：

$$\hat{A}_{i,t} = \frac{r_i - \text{mean}(\{r_\ell\})}{\sqrt{\text{std}^2(\{r_\ell\}) + \varepsilon}}$$

当组内所有回复的奖励完全相同（全对 $r_i=1$ 或全错 $r_i=0$）时，标准差为零，导致优势估计为零，梯度消失，该批次无法提供有效学习信号。同时，在线策略的"一次使用即丢弃"原则使得高方差或困难样本仅被利用一次，造成严重的数据浪费——实验表明，GRPO训练后，大量初始无法解决的困难样本（0/8准确率）几乎没有改善。

### 核心机制：自适应批次构建

BAPO通过**难度感知的历史缓冲区选择性复用**打破奖励同质化，其训练批次由三个子集动态合并构成，由批次选择函数 $I(x)$ 统一描述：

$$I(x) = \underbrace{\mathbf{1}_{\{\frac{1}{G} \leq \mu_{\alpha,r}(x) \leq \frac{G-1}{G}\}}}_{\text{Filtered Fresh}} + \underbrace{\mathbf{1}_{\{\mu_{\alpha_B,r}(x) \leq c_1 \wedge \mu_{\pi_{\theta_t},r}(x) > c_1\}}}_{\text{Improved Historical Difficult}} + \underbrace{\mathbf{1}_{\{c_2 \leq \mu_{\alpha_B,r}(x) \leq c_3\}}}_{\text{Historical High-quality}}$$

其中 $\mu_{\alpha,r}(x)$ 表示在策略 $\alpha$ 下提示 $x$ 的组平均奖励，$c_1, c_2, c_3$ 为难度阈值。

#### 子集一：在线过滤样本（X₁）

从在线采样批次中**剔除零方差样本**，仅保留组平均奖励 $\mu_{\alpha,r}(x) \in [1/G, (G-1)/G]$ 的提示。这确保进入训练的在线样本始终具有非零优势，提供有效的梯度信号。消融实验表明，若将范围过滤替换为均匀过滤，训练极度不稳定，梯度范数爆炸，150步后性能完全崩溃。

#### 子集二：改善的历史困难样本（X₂）

维护一个困难样本缓冲区 $\mathcal{B}_{\text{bad}}$，存储历史上表现极差的提示。每 $m$ 步，用当前策略 $\pi_{\theta_t}$ 重新生成回复，仅选取出现可观测提升的样本：

$$\mathcal{X}_2 = \left\{(x, y') \mid (x, y) \in \mathcal{B}_{\text{bad}}, y' \sim \pi_{\theta_t}(\cdot \mid x), c_1 < \mu_{\pi_{\theta_t},r}(x) < 1\right\}$$

这一机制的核心价值在于：将历史高方差样本重新注入训练，针对性攻克困难问题。消融实验显示，移除X₂导致性能下降约21%，证明该组件至关重要。

#### 子集三：高质量历史复用（X₃）

维护一个FIFO高质量缓冲区 $\mathcal{B}_{\text{high}}$，仅保留近三步的高质量轨迹。当在线过滤后的样本不足满批时，随机采样以填补剩余容量：

$$\mathcal{X}_3 = S\left(\mathcal{B}_{\text{high}}, \min\left(|\mathcal{B}_{\text{high}}|, B - |\mathcal{X}_1| - |\mathcal{X}_2|\right)\right)$$

高质量阈值通过线性映射动态调整，随全局平均性能 $r_{\text{tot}}$ 从易到难偏移：

$$c_i = r_{\text{tot}} \cdot (c_i^{\text{high}} - c_i^{\text{low}}) + c_i^{\text{low}}, \quad i \in \{2,3\}$$

准确率迁移矩阵分析证实，初始8/8准确率的样本在训练过程中极少退化到低分段，确保X₃数据源的可靠性。

### 缓冲区实体结构

缓冲区中每个条目存储完整信息以支持重要性采样修正：

$$\mathcal{B} = \{(u_i, \{x_{i,j}\}_{j=1}^{G}, \{y_{i,j}\}_{j=1}^{G}, \{r_{i,j}\}_{j=1}^{G}, \{\alpha_B(y_{i,j} \mid x_i)\}_{j=1}^{G})\}_{i=1}^{|\mathcal{B}|}$$

包含：唯一标识符 $u_i$、提示组、回复组、奖励组、以及**生成时的策略概率**，后者用于计算重要性采样比 $\rho_{\alpha}(\theta)$，修正历史样本与当前策略的分布差异。

### 合并训练目标

最终训练目标融合在线样本和历史缓冲区样本，并施加KL正则约束策略偏移：

$$\mathcal{L}_{\alpha}(\pi_{\theta}) = \underbrace{\mathbb{E}_{(x,y) \sim \alpha}\left[\rho_{\alpha}(\theta) \cdot \hat{A}(x,y)\right]}_{\text{Contribution from fresh samples}} + \underbrace{\mathbb{E}_{(x,y) \sim \mathcal{B}}\left[\rho_{\alpha_B}(\theta) \cdot \hat{A}(x,y)\right]}_{\text{Contribution from historical samples}} - \beta \cdot \mathbb{D}_{\text{KL}}(\pi_{\theta} \| \alpha)$$

### 离策略推理与稳定性保证

BAPO采用延迟同步机制：推理策略 $\alpha$ 每 $v$ 步才与训练策略 $\pi_{\theta}$ 同步一次（默认 $v=5$），形成准离策略数据流。理论分析假设总变分距离有界：

$$\text{TV}(\pi_{\theta_t}(\cdot \mid x), \pi_{\theta_{t-v}}(\cdot \mid x)) \leq \delta_1 \quad \forall x \in \mathcal{X}_1$$

FIFO机制和近期策略缓冲区共同约束历史样本的策略偏差，确保训练稳定性。消融显示，在合理范围内（$v=5, m=5$）性能保持稳定，仅极端延迟才会因策略偏差过大而损害性能。



## 实验与关键发现

### 核心瓶颈与动机验证

BAPO的设计动机源于对GRPO训练动态的实证观察。**Figure 1** 追踪了数学数据集在GRPO训练前后不同准确率分组（0/8到8/8）的样本数量变化：低准确率组（0/8，即模型完全无法解决的问题）的样本数量几乎未减少，揭示了在线策略RLVR框架对困难样本的改善能力极为有限。这一现象的根本原因在于GRPO的两大效率瓶颈：（1）**奖励同质化**——当组内G条回复全部正确或全部错误时，优势估计为零，梯度消失，训练批次失去有效学习信号；（2）**经验浪费**——每个在线采样批次仅使用一次即丢弃，困难样本的高方差信息未被充分利用。

### 主实验结果

**Table 1** 展示了BAPO与多个基线方法在数学推理基准上的综合对比。以DeepSeek R1 Distill Qwen 1.5B为基模型，BAPO在AIME24上达到**38.54%**的准确率，比GRPO（30.73%）提升**+7.81**个百分点；在MATH500上达到89.18%（GRPO为85.40%）；在AMC23上达到89.18%。BAPO的平均准确率为**56.01%**，显著优于GRPO（43.51%）和DAPO（49.67%），实现了约**12.5%**的平均相对提升。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_RduOiisl1S/figures/008_Table_1.jpg]]
*Table 1: Comprehensive Evaluation Results. $\because$ indicates fine-tuning via the corresponding method. Accuracy is averaged over 32 runs. The bold value denotes the top result, and the underlined value denotes the second-top result*

在规划和视觉几何任务上（**Table 2**），BAPO同样表现突出。以Qwen2.5 Math 1.5B为基模型，BAPO在Countdown-3to4（CD-34）上达到**73.00%**（GRPO为62.94%），提升**+10.06**个百分点；在Geometry3K测试集上达到46.33%（GRPO为43.12%）。值得注意的是，DAPO在相同任务上需要约**1921k**次推理，而BAPO仅需**733k**次，推理量节省约62%。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_RduOiisl1S/figures/009_Table_2.jpg]]
*Table 2: (b) Planning and Visual Geometry Benchmarks*

**Figure 4** 的训练奖励曲线显示，BAPO在数学、规划和视觉几何三个任务上均实现了比GRPO和DAPO更平滑的收敛过程，且奖励下界更高，表明离策略缓冲区机制有效稳定了训练动态。

### 困难样本攻克能力

BAPO对困难样本的针对性改善是其核心优势。**Figure 7** 追踪了DeepScalerR训练子集上不同准确率分组的变化：经过3个epoch训练后，BAPO成功改善了**31%**的初始无法解决问题（0/8准确率），而GRPO仅改善了**19%**。这一**+12%**的差距直接验证了历史困难样本重利用机制（X₂）的有效性——通过周期性重新评估并选取有提升的困难样本，BAPO将高方差的学习信号重新注入训练，显著提升了对困难问题的解决能力。

### 消融实验

**Figure 6** 系统性地消融了BAPO的核心组件和超参数敏感性：

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_RduOiisl1S/figures/018_Figure_6.jpg]]
*Figure 6: Ablation Studies for BAPO. The first column presents ablations on frequency-related hyperparameters (m, v). The second column shows ablations on buffer subsets ( $\mathcal { X } _ { 2 } , \bar { \mathcal { X } } _ { 3 }$ ) . The third column compares fixed vs. adaptive difficulty thresholds

- **缓冲区子集贡献**（第二列）：移除历史困难样本重利用（X₂）导致性能下降约**21%**，证明针对性攻克困难样本是BAPO性能提升的关键来源。移除高质量样本复用（X₃）同样造成明显性能损失，表明历史高价值样本的重复利用对维持训练稳定性和批次质量至关重要。
- **频率超参数鲁棒性**（第一列）：在合理的超参数范围内（如延迟步数v=5、重评估频率m=5），BAPO性能保持稳定。仅当延迟步数过大导致策略偏差过度累积时，性能才会显著下降。这表明BAPO的结构逻辑优于具体超参数调参。
- **阈值策略对比**（第三列）：自适应难度阈值（基于全局平均性能动态调整）优于固定阈值，验证了难度感知机制的必要性。

**Figure 10** 进一步消融了在线过滤策略。使用均匀过滤（Uniform Filter）替代BAPO默认的范围过滤（Range Filter）会导致训练极度不稳定：梯度范数在约110步后出现剧烈爆炸，150步后性能完全崩溃。这一失败模式揭示了一个关键洞察：**仅保留具有中等奖励方差的样本（μ∈[1/G, (G-1)/G]）是维持训练稳定性的必要条件**，而均匀采样会引入大量零方差或低信息量样本，破坏梯度信号质量。

### 参数自由的“迷你测试”

为消除调参偏差的影响，论文设计了参数自由的“迷你测试”（**Figure 5** 中图）：仅使用标准零优势过滤（X₁）、重放历史全错样本（X₂）以及复用准确率恰好为50%的样本（X₃）。即使在完全剥离超参数调优的情况下，BAPO仍然明显优于GRPO，验证了其批次构建结构逻辑的固有优势。这一结果与理论分析一致：准确率为1/2的样本最大化奖励方差，提供单步策略改进的理论最大潜力。

![[assets/figures/papers/paper_list_l37_https_openreview_net_forum_id_RduOiisl1S/figures/012_Figure_5.jpg]]
*Figure 5: Test Curves of Group Accuracy Changes on AIME for different RLVR methods based on Qwen3 8B. Left: Standard BAPO vs. GRPO. Medium: BAPO (mini test) vs. GRPO. Right: Standard BAPO vs. DAPO*

### 批次组成动态分析

**Figure 8** 可视化了BAPO训练过程中三类样本（X₁过滤新鲜样本、X₂改善困难样本、X₃高质量复用样本）的动态分布。实际组装批次大小频繁低于最大配置容量，说明自适应构建机制根据数据质量灵活调整批次规模。在线样本（X₁）通常占批次的**40-60%**，其余由历史缓冲区样本填充，确保了训练批次中始终包含足够的奖励方差和适当的难度分布。

### 计算开销分析

**Table 2** 的计算开销对比显示，BAPO在数学任务上的总训练时间约为**1天22小时**，与GRPO（1天16小时）相当，远低于DAPO（2天15小时）。BAPO的额外开销主要来自每m步重新评估困难样本和高价值缓冲区的FIFO维护，但总体计算成本可控。消融实验表明，移除X₂或X₃组件虽可略微减少训练时间，但会导致显著的性能损失，证明这些组件的性价比合理。

### 泛化性与安全性验证

BAPO的批次构建范式具有算法无关的泛化能力。**Figure 16** 展示了将BAPO范式迁移到Actor-Critic算法（BA-PPO）的结果：在AIME 2024基准上，BA-PPO比标准PPO高出**+5.5**个点（峰值0.325 vs 约0.27），证明该范式不仅适用于GRPO风格的RLVR，也可作为通用增强模块。

**Figure 15** 的准确率迁移矩阵验证了历史高质量样本复用的安全性。追踪1000个固定提示在训练过程中的准确率分组变化显示：初始达到8/8准确率的样本在整个训练过程中极少退化到低分段（下三角区域稀疏），确保了X₃数据源的可靠性。这一实证结果支持了FIFO机制和近期策略约束（TV距离有界）的有效性。

### 失败模式与局限性

尽管BAPO在多数场景下表现优异，但仍存在以下局限：

1. **极端长训练下的稳定性未验证**：FIFO机制依赖近期策略缓冲区保证一致性，但在训练持续极多轮次时，旧高质量样本的适用性可能需要更严格的陈旧度控制。
2. **策略突变风险**：理论分析假设总变分距离有界，实际训练中如策略发生突变，该假设可能被违反，导致性能下界不再成立。
3. **困难样本重评估开销**：在困难样本比例极高的任务中，每m步重新评估的开销可能高于预期。
4. **可扩展性待验证**：实验主要基于1.5B-8B参数规模的密集模型，未在MoE架构或超大规模模型（>100B）上验证。
5. **任务泛化性有限**：当前验证集中在数学、简单规划和视觉几何推理，对开放式文本生成或其他形式推理的泛化性尚不明确。



## 定位与知识库关联

### 1. 在线策略RLVR的瓶颈与BAPO的切入点

大语言模型推理的后训练阶段，当前主流范式是在线策略强化学习（On-Policy RLVR），其核心代表为**GRPO**（Shao et al., 2024）。GRPO通过在每组G个回复内计算相对优势估计，避免了传统PPO对价值网络的依赖，显著降低了训练开销。然而，GRPO存在两个根本性效率瓶颈：

**奖励同质化导致的梯度消失**：当组内所有样本的奖励完全相同（全对或全错）时，优势估计的方差为零，梯度信号完全消失。这意味着在训练过程中，大量“已掌握”或“完全未掌握”的问题无法为策略更新提供任何有效信息。

**“一次使用即丢弃”的数据浪费**：在线策略框架要求每个训练批次必须由当前策略实时生成，历史样本被直接丢弃。这导致两个后果：其一，高方差样本（如困难问题）仅被使用一次，其蕴含的丰富学习信号未能被充分利用；其二，训练数据的利用效率极低，尤其在困难样本上几乎无法积累改进。

### 2. 离策略RLVR谱系与BAPO的定位

为缓解上述瓶颈，一系列离策略或准离策略RLVR方法被提出，BAPO正是在这一谱系中做出了关键的结构性创新。

| 方法 | 离策略机制 | 核心贡献 | 局限性 |
|------|-----------|---------|--------|
| **GRPO (v=5)** (Mroueh et al., 2025) | 延迟v步更新推理策略 | 最简单的离策略适配 | 仅缓解数据浪费，未解决奖励同质化 |
| **RePO** (Li et al., 2025) | 多样化检索策略从缓冲区采样 | 引入检索增强的缓冲区机制 | 检索策略本身引入额外复杂性 |
| **Remix-GRPO** (Liang et al., 2025) | 固定比例混合缓冲区样本 | 提高数据利用率 | 未区分样本难度，混合比例需人工设定 |
| **DAPO** (Yu et al., 2025) | 动态采样和不对称裁剪 | 在线策略改进 | 需约2.5倍推理量，计算开销大 |
| **MoPPS** (Qu et al., 2025) | 难度感知的提示选择 | 融合难度信号 | 仍为在线策略，未利用历史经验 |
| **BAPO** (本文) | 难度感知的自适应批次构建 | 选择性复用历史困难和高价值样本 | 需维护缓冲区，定期重新评估引入额外开销 |

BAPO的核心区分点在于**难度感知的批次构建逻辑**：它不简单地混合或检索历史样本，而是根据每个提示的组平均奖励，将样本划分为三类并施以不同的处理策略——过滤掉零方差的同质化样本（X₁）、周期性重新评估历史困难样本并选取有提升者（X₂）、从近期高质量缓冲区中随机采样以填补批次容量（X₃）。这种结构性设计使得训练批次始终维持足够的奖励方差和适当的难度分布，从根本上打破了奖励同质化的困境。

### 3. 适用边界与泛化能力

**任务域验证**：BAPO在数学推理（AIME24、MATH500、AMC23）、规划任务（Countdown-3to4）和视觉几何推理（Geometry3K）三个领域进行了全面验证，覆盖了当前LLM推理后训练的主要任务类型。实验表明，BAPO在这些任务上平均比GRPO提升12.5%，且成功解决了基模型完全无法解答问题的40.7%。

**算法无关性**：消融实验表明，BAPO的批次构建范式可以泛化到标准PPO框架。将BAPO的自适应批次构建机制应用于PPO（称为BA-PPO），在AIME 2024基准上比标准PPO高出+5.5个点，证明该范式是算法无关的增强策略，而非特定于GRPO的改进。

**模型规模验证**：实验基于DeepSeek Distilled Qwen 1.5B、Qwen2.5 Math 1.5B、Qwen2.5 VL 3B以及Qwen3 8B等模型进行，覆盖了1.5B至8B的参数量级。但需要注意的是，论文未在MoE架构或超大规模模型（>100B）上进行验证，其在大规模分布式训练场景下的可扩展性及对计算资源调度的影响尚不明确。

### 4. 局限性与开放问题

**策略一致性的长期稳定性**：BAPO依赖FIFO机制和近期策略缓冲区来保证策略一致性，并通过总变分距离约束提供理论下界保证。然而，当训练持续极多轮次时，旧高质量样本的适用性可能需要更严格的陈旧度控制。理论分析假设总变分距离有界，在实际训练中若策略发生突变，该假设可能被违反，导致性能下界不再成立。

**额外推理开销的权衡**：重新评估历史困难样本（每m步）会引入额外推理开销。在困难样本比例极高的任务中，这部分开销可能高于预期。尽管实验表明BAPO的训练总时间与GRPO相当（约1天22小时 vs 1天16小时），且远低于DAPO（2天15小时），但在极端困难样本占比的场景下，m参数的调优变得更为关键。

**任务域的扩展性**：实验主要聚焦于数学、简单规划和视觉几何推理，这些任务具有明确的奖励函数（答案正确性）。对于开放式文本生成、多轮对话或其他形式推理任务，奖励信号的稀疏性和同质化模式可能不同，BAPO的难度感知机制能否直接迁移尚需进一步研究。

**开放问题**：
1. BAPO的难度感知批次构建范式如何适配具有MoE架构的大语言模型？
2. 能否将BAPO的经验重放机制扩展至智能体强化学习框架，用于长序列决策任务？
3. 当训练极不稳定时，总变分距离约束是否依然满足？如果否，如何自适应调整缓冲区策略？
4. 能否通过更智能的缓冲区淘汰策略（如基于重要性的优先级）进一步平衡计算开销和性能提升？
5. 降低困难样本重新评估频率到何种程度仍能保持显著的性能增益？是否存在最优的m与v的联合调度策略？



## 原文 PDF

![[paperPDFs/ICLR_2026/Buffer_Matters_Unleashing_the_Power_of_Off_Policy_Reinforcement_Learning_in_Large_Language_Model_Reasoning.pdf]]
