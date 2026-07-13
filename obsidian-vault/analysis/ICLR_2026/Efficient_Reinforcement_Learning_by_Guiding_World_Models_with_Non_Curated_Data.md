---
title: "Efficient Reinforcement Learning by Guiding World Models with Non-Curated Data"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Efficient_Reinforcement_Learning_by_Guiding_World_Models_with_Non_Curated_Data.pdf
project_link: null
code_link: https://github.com/zhaoyi11/ncrl
openreview_forum_id: oBXfPyi47m
aliases:
- NNCODER
- ERLBGWMNCD
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "在微调过程中重用非整理离线数据：通过检索任务相关轨迹进行经验重演，减轻分布偏移与灾难性遗忘；同时训练行为克隆先验策略，引导在线数据收集靠近世界模型高置信区域，从而显著提升样本效率。"
primary_logic: "无奖励、混合质量、多形态的非整理离线数据可以在预训练与微调两个阶段被有效利用。预训练学习一个任务无关的多形态世界模型，微调时通过基于特征相似度的轨迹检索实现经验重演，并利用行为克隆先验策略切换执行引导，使强化学习在有限交互预算下大幅超越从零训练及现有离线数据利用方法。"
claims:
- "NCRL achieves nearly twice the aggregate score of learning-from-scratch baselines across 72 visuomotor tasks spanning 6 embodiments."
- "NCRL consistently outperforms all compared methods that leverage offline data (R3M, UDS-RLPD, ExPLORe, JSRL-BC) by a large margin on challenging locomotion and manipulation tasks."
- "Ablation study demonstrates that world model pre-training alone is insufficient for hard tasks; combining with retrieval-based experience rehearsal and execution guidance is cruci..."
- "NCRL at 150k online steps achieves higher mean success rate on Meta-World (0.748) and higher mean episodic return on DMControl (617.73) compared to DreamerV3 and DrQ-v2 at the sam..."
---

# Efficient Reinforcement Learning by Guiding World Models with Non-Curated Data

> [!tip] 核心洞察
> 无奖励、混合质量、多形态的非整理离线数据可以在预训练与微调两个阶段被有效利用。预训练学习一个任务无关的多形态世界模型，微调时通过基于特征相似度的轨迹检索实现经验重演，并利用行为克隆先验策略切换执行引导，使强化学习在有限交互预算下大幅超越从零训练及现有离线数据利用方法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 利用非整理离线数据引导世界模型的高效强化学习 |
| 英文题名 | Efficient Reinforcement Learning by Guiding World Models with Non-Curated Data |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=oBXfPyi47m) · [GitHub](https://github.com/zhaoyi11/ncrl) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | NCRL (Non-curated offline data for efficient RL) |
| Dataset | Meta-World (50任务), DMControl (22任务), Quadruped Walk (DMControl), Shelf Place (Meta-World) |

> [!tip] 效果简介
> - Meta-World (50任务) 上，平均成功率 为 0.748，对比 DreamerV3 @150k: 0.360; DrQ-v2 @150k: 0.430，变化 +0.388。
> - DMControl (22任务) 上，平均回合回报 为 617.73，对比 DreamerV3 @150k: 320.86; DrQ-v2 @150k: 226.49，变化 +296.87。
> - Quadruped Walk (DMControl) 上，回合回报 为 855.6，对比 DreamerV3 @150k: 145.2，变化 +710.4。

## 概要

在微调阶段，离线预训练数据与在线强化学习数据之间存在严重的分布偏移，导致朴素的世界模型微调失效，尤其阻碍困难探索任务上的策略学习。NCRL（Non-curated offline data for efficient RL）提出了一种两阶段框架来解决这一问题：首先从无奖励、混合质量、多形态的非整理离线数据中预训练一个任务无关的世界模型；随后在微调阶段，通过基于特征相似度的轨迹检索实现经验重演以缓解分布偏移，并训练行为克隆先验策略进行执行引导，使在线数据收集靠近世界模型的高置信区域。

在72个视觉运动任务（涵盖6种形态的Meta-World和DMControl基准）上，NCRL在15万在线交互步数下取得了近乎两倍于从零训练基线（DreamerV3、DrQ-v2）的聚合得分，并以显著优势超越所有对比的离线数据利用方法（R3M、UDS-RLPD、ExPLORe、JSRL-BC）。消融实验证实，世界模型预训练单独不足以在困难任务上工作，必须结合检索式经验重演和执行引导才能实现高性能。NCRL在更困难的数据条件下（直接使用非整理数据，而基线方法需预处理保留任务相关轨迹）仍取得大幅领先，且未使用奖励塑形、专家回放预填充等额外技巧。



### 视觉运动控制中的样本效率困境

从高维像素输入中学习复杂的视觉运动控制策略是深度强化学习的核心挑战之一。无模型方法如 **DrQ-v2** 虽然取得了显著进展，但通常需要数百万甚至上千万的环境交互步数才能收敛，这在真实机器人场景中成本高昂且不切实际。基于模型的方法如 **DreamerV3**（Hafner et al., 2023）通过在世界模型的潜在空间中学习，显著提升了样本效率，但其从零开始训练时仍需大量在线交互来构建对任务动态的准确理解。

### 离线数据的利用现状与缺口

近年来，研究者开始探索利用离线数据来加速强化学习。现有方法大致可分为三类：

- **视觉表征预训练**：如 **R3M**（Nair et al., 2022），通过在大规模离线视频数据上预训练视觉编码器，为下游策略提供通用表征。然而，这类方法仅利用了静态的视觉特征，忽略了环境动态和动作信息。
- **离线到在线强化学习**：如 **UDS-RLPD**（Yu et al., 2022; Ball et al., 2023）和 **JSRL-BC**（Uchendu et al., 2023），试图从离线数据中学习初始策略，再通过在线交互进行微调。但这些方法通常要求离线数据带有奖励标签，或假设数据质量较高。
- **不确定性驱动的探索**：如 **ExPLORe**（Li et al., 2023），通过为无奖励的离线数据标注不确定性奖励来引导探索，但这类方法在面对困难探索任务时效果有限。

这些方法的共同局限在于：它们对离线数据施加了严格的整理要求——需要任务相关、带奖励标签、质量可控。然而，现实世界中更常见的是**非整理离线数据**（non-curated offline data）：无奖励、混合质量、跨多种机器人形态。如何有效利用这类“野生”数据来加速强化学习，仍是一个开放问题。

### 世界模型预训练的潜力与瓶颈

一个更具前景的方向是将世界模型预训练与离线数据相结合。通过在离线数据上预训练一个任务无关的世界模型，智能体可以在微调前就获得对环境动态的先验理解。然而，这一范式面临一个关键瓶颈：**离线预训练数据与在线RL微调数据之间存在严重的分布偏移**。如图2（左）所示，在微调初期，在线交互产生的观测分布与预训练所用的离线数据分布差异显著，导致朴素的世界模型微调失效，尤其在需要深度探索的困难任务上表现糟糕——例如在Meta-World的Shelf Place任务上，仅使用预训练世界模型的DreamerV3在150k步后成功率仍为0。

### 本文动机

基于上述分析，本文的核心动机是回答以下问题：**能否在预训练和微调两个阶段都充分利用非整理离线数据，从而在极低在线交互预算下实现高效的视觉运动控制？**

具体而言，需要解决两个子问题：
1. **如何减轻分布偏移？** 在微调时，如何让世界模型记住与当前任务相关的离线知识，而非被在线数据完全覆盖？
2. **如何引导高效探索？** 在奖励稀疏的困难任务中，如何利用离线数据中的行为先验，引导智能体在有限交互步数内访问高奖励区域？

本文提出的 **NCRL**（Non-curated offline data for efficient RL）正是围绕这两个问题展开，通过经验重演（experience rehearsal）和执行引导（execution guidance）两种机制，在非整理离线数据上构建了一套完整的预训练-微调框架。



## 核心方法与创新机理

NCRL 的核心创新并非提出全新的算法范式，而是通过**重新定义离线数据在模型基强化学习中的使用方式**，系统性地解决了从预训练到在线微调的分布偏移瓶颈。具体体现在以下四个关键维度：

### 1. 数据范式的根本转变：从整理数据到非整理数据

传统方法依赖**任务特定、带奖励标签的整理数据**进行世界模型预训练，而 NCRL 首次证明**无奖励、混合质量、多形态的非整理离线数据**可以在预训练与微调两个阶段被有效利用。这一转变使得方法无需昂贵的数据筛选与标注，直接使用来自多种机器人形态、不同策略质量、不含奖励信号的原始轨迹数据。与基线方法（如 R3M、UDS-RLPD、ExPLORe、JSRL-BC）需要预处理离线数据、仅保留任务相关轨迹不同，NCRL 直接使用包含大量无关数据的非整理数据集，在更困难的数据条件下仍取得大幅领先（Figure 3）。

### 2. 微调阶段的离线数据重利用：经验重演

现有方法通常在预训练后丢弃离线数据，仅用在线交互数据微调世界模型。然而，离线预训练数据与在线 RL 数据之间存在严重的分布偏移，导致朴素微调在困难探索任务上失效。NCRL 提出**经验重演**机制：在微调过程中，基于预训练编码器提取的特征计算在线观测与离线轨迹初始观测的 L2 距离，通过 Faiss 高效检索前 k 条最相似的任务相关轨迹，将其与在线数据混合重放以更新世界模型和奖励函数。这一机制同时缓解了分布偏移与灾难性遗忘问题——消融实验表明，经验重演将在线数据与离线/专家数据之间的 Wasserstein 距离显著降低（Figure 2 右），且仅靠世界模型预训练（P）在困难任务上几乎失效，必须结合经验重演（ER）和执行引导（G）才能显著提升表现（Figure 6）。

### 3. 探索机制创新：执行引导替代不确定性奖励

传统基于模型的探索方法通常依赖世界模型的不确定性估计来生成内在奖励（如 ExPLORe），但这类方法在困难探索任务上效果有限。NCRL 提出**执行引导**：在检索到的任务相关数据上通过行为克隆训练一个先验策略 $\pi_{bc}$，在线数据收集时按照线性退火调度概率性地在 RL 策略 $\pi_{\phi}$ 与 $\pi_{bc}$ 之间切换。其核心直觉是引导智能体向世界模型高置信区域探索，而非盲目追求不确定性。消融实验表明，在 Assembly 和 Stick Pull 等困难探索任务上，执行引导远超基于不确定性奖励标记的替代方案（OTS）（Figure 7），且对退火调度不敏感，表现出良好的鲁棒性（Figure 12）。

### 4. 统一的多形态世界模型架构

NCRL 对标准 RSSM 架构进行了三项关键修改以适应非整理多形态数据：移除任务相关损失以支持任务无关预训练；对动作维度进行零填充以统一不同形态的动作空间；将模型扩展至 280M 参数以提升表征能力。与为每个任务独立训练 RSSM 的基线不同，NCRL 在每个 benchmark 上仅训练一个共享的世界模型，实现了跨形态的知识迁移。微调实验进一步表明，完整微调世界模型优于冻结编码器或仅微调解码器（Figure 8），验证了端到端自适应的必要性。

**总结**：NCRL 的创新本质是通过“非整理数据预训练 + 检索式经验重演 + 行为克隆执行引导”的三位一体设计，将分布偏移从阻碍变为可调控的杠杆，使强化学习在 150k 在线交互预算下达到从零训练方法 3.3–6.7 倍样本量才能获得的性能（Table 4, Table 5）。



![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_oBXfPyi47m/figures/001_Figure_1.jpg]]
*Figure 1: Overview of NCRL (Non-curated offline data for efficient RL). NCRL leverages noncurated offline data—reward-free, mixed-quality, and multi-embodiment—to enable efficient RL. It uses this data to pretrain a task-agnostic world model, and then, during fine-tuning, to reduce distributional shift and guide exploration through experience rehearsal and execution guidance*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_oBXfPyi47m/figures/002_Table_1.jpg]]
*Table 1: Comparison with different policy learning methods that leverage offline data*

NCRL 采用**两阶段流水线**，核心思想是将同一份非整理离线数据在预训练与微调两个阶段中分别复用，以解决从零训练样本效率低、以及朴素世界模型微调因分布偏移而失效的问题。

### 阶段一：多形态世界模型预训练

输入为**无奖励标签、混合质量、跨多形态**的非整理离线数据集 $\mathcal{D}_{\mathrm{off}}$。该阶段训练一个**任务无关的共享世界模型**，其架构基于 RSSM（Recurrent State-Space Model），但做了三项关键修改：

1. **移除任务相关损失**，使模型不依赖任务标签；
2. **对动作维度进行零填充**，统一跨形态的动作空间；
3. **将模型扩展至 280M 参数**，以容纳多形态的观测与动力学信息。

预训练目标由三项损失加权组合构成：

$$\mathcal{L}(\theta) = \mathbb{E}_{(o_{t-1}, a_{t-1}, o_t) \sim \mathcal{D}_{\mathrm{off}}} \Big[ \frac{1}{T} \sum_{t=1}^T \big( \beta_1 \mathcal{L}_{\mathrm{pred}}(\theta) + \beta_2 \mathcal{L}_{\mathrm{dyn}}(\theta) + \beta_3 \mathcal{L}_{\mathrm{rep}}(\theta) \big) \Big]$$

其中 $\mathcal{L}_{\mathrm{pred}}$ 为观测重建的对数似然，$\mathcal{L}_{\mathrm{dyn}}$ 与 $\mathcal{L}_{\mathrm{rep}}$ 分别用 stop-gradient KL 散度约束动力学预测与表征学习。每个 benchmark 仅训练一个世界模型，而非逐任务独立训练。

### 阶段二：RL 微调与离线数据复用

微调阶段同时使用在线交互数据 $\mathcal{D}_{\mathrm{on}}$ 和非整理离线数据 $\mathcal{D}_{\mathrm{off}}$，通过两个核心机制解决分布偏移与探索困难。

**经验重演（Experience Rehearsal）**：利用预训练阶段学到的编码器 $e_\theta$，计算在线观测与每条离线轨迹初始观测之间的 L2 特征距离：

$$\mathbf{D} = \| \mathbf{e}_{\theta}(o_{\mathrm{on}}) - \mathbf{e}_{\theta}(o_{\mathrm{off}}) \|_2$$

借助 Faiss 高效检索前 $k$ 条最相似轨迹，构成任务相关的离线子集 $\mathcal{D}_{\mathrm{retrieved}}$。该子集与在线数据混合后用于世界模型微调（沿用式 (1)）和 Dreamer 风格的演员-评论家训练，从而**减轻分布偏移与灾难性遗忘**。定量证据表明，经验重演显著降低了在线数据与离线/专家数据之间的 Wasserstein 距离（Figure 2）。

**执行引导（Execution Guidance）**：在检索到的 $\mathcal{D}_{\mathrm{retrieved}}$ 上通过行为克隆训练一个先验策略 $\pi_{bc}$。在线数据收集时，按预定义的线性退火调度概率性地切换至 $\pi_{bc}$，引导智能体向世界模型高置信区域探索。消融实验（Figure 6）表明，世界模型预训练（P）单独不足以解决困难任务，必须与经验重演（ER）和执行引导（G）协同工作才能显著提升性能。

### 整体输入输出流

- **预训练输入**：非整理离线数据（无奖励、混合质量、多形态观测与动作序列）。
- **预训练输出**：一个 280M 参数的任务无关 RSSM 世界模型及其编码器。
- **微调输入**：在线交互数据 + 经检索得到的任务相关离线轨迹子集。
- **微调输出**：针对目标任务优化的世界模型、奖励函数、演员策略与评论家；数据收集时交替执行 RL 策略与行为克隆先验策略。

整个流程无需奖励塑形、无需专家回放预填充，即可在 150k 在线步数下使 Meta-World 平均成功率达到 0.748、DMControl 平均回合回报达到 617.73，分别匹配 DreamerV3 与 DrQ-v2 在 3.3–6.7 倍样本下的表现（Table 4, Table 5）。



NCRL 的核心由四个协同模块构成：**多形态世界模型预训练**、**经验检索**、**行为克隆先验策略训练**、以及**RL 微调与经验重演/执行引导**。这些模块围绕一个中心思想展开——在预训练和微调两个阶段充分利用无奖励、混合质量、多形态的非整理离线数据，以缓解分布偏移并引导高效探索。

### 多形态世界模型预训练

NCRL 采用一个共享的循环状态空间模型（Recurrent State Space Model, RSSM），在非整理离线数据 $\mathcal{D}_{\mathrm{off}}$ 上进行任务无关的预训练。与标准 Dreamer 框架不同，该模型做了三处关键修改：(i) 移除任务相关损失，使模型专注于通用的环境动力学建模；(ii) 对动作进行零填充，以统一不同形态间的动作维度；(iii) 将模型扩展至 280M 参数以提升表征容量。

RSSM 的核心组件定义如下：

$$h_t = f_\theta(h_{t-1}, z_{t-1}, a_{t-1}) \qquad z_t \sim q_\theta(z_t \mid h_t, o_t) \qquad \hat{z}_t \sim p_\theta(\hat{z}_t \mid h_t) \qquad \hat{o}_t \sim d_\theta(\hat{o}_t \mid h_t, z_t)$$

其中 $f_\theta$ 为确定性序列模型，$q_\theta$ 为编码器，$p_\theta$ 为动力学预测器，$d_\theta$ 为观测解码器。预训练总目标为：

$$\mathcal{L}(\theta) = \mathbb{E}_{(o_{t-1}, a_{t-1}, o_t) \sim \mathcal{D}_{\mathrm{off}}, z_t \sim q_\theta(\cdot \mid h_t, o_t)} \Big[ \frac{1}{T} \sum_{t=1}^T \big( \beta_1 \mathcal{L}_{\mathrm{pred}}(\theta) + \beta_2 \mathcal{L}_{\mathrm{dyn}}(\theta) + \beta_3 \mathcal{L}_{\mathrm{rep}}(\theta) \big) \Big]$$

三项损失的具体形式为：

$$\mathcal{L}_{\mathrm{pred}}(\theta) = -\ln d_\theta(o_t | z_t, h_t) \qquad \mathcal{L}_{\mathrm{dyn}}(\theta) = \max(1, \mathrm{KL}(\mathrm{sg}(q_\theta(z_t | h_t, o_t) \| p_\theta(\hat{z}_t | h_t)))) \qquad \mathcal{L}_{\mathrm{rep}}(\theta) = \max(1, \mathrm{KL}(q_\theta(z_t | h_t, o_t) \| \mathrm{sg}(p_\theta(\hat{z}_t | h_t))))$$

其中 $\mathrm{sg}(\cdot)$ 表示 stop-gradient 操作。$\mathcal{L}_{\mathrm{pred}}$ 最大化观测重建的对数似然；$\mathcal{L}_{\mathrm{dyn}}$ 约束动力学预测器 $p_\theta$ 向编码器后验 $q_\theta$ 靠拢；$\mathcal{L}_{\mathrm{rep}}$ 则约束编码器表征向动力学先验靠拢。这种对称的 KL 散度设计使得模型在无奖励信号的条件下，仍能学习到紧致且可预测的隐空间表征。

### 经验检索

在微调阶段，NCRL 通过经验检索从非整理离线数据中动态获取任务相关轨迹。检索基于预训练编码器 $e_\theta$ 提取的特征，计算在线观测 $o_{\mathrm{on}}$ 与每条离线轨迹初始观测 $o_{\mathrm{off}}$ 之间的 L2 距离：

$$\mathbf{D} = \| \mathbf{e}_{\theta}(o_{\mathrm{on}}) - \mathbf{e}_{\theta}(o_{\mathrm{off}}) \|_2$$

利用 Faiss 向量检索库，该方法可在数秒内从大规模离线数据集中检索出前 $k$ 条距离最近的轨迹，构成任务相关的离线子集 $\mathcal{D}_{\mathrm{retrieved}}$。这一机制的核心在于：预训练编码器已将不同形态的观测映射到语义一致的隐空间，使得基于特征距离的检索能够有效识别与当前任务动力学相近的历史经验。

### 行为克隆先验策略训练

在检索到的任务相关数据 $\mathcal{D}_{\mathrm{retrieved}}$ 上，NCRL 通过行为克隆训练一个先验策略 $\pi_{\mathrm{bc}}$。该策略捕捉了离线数据中的行为先验，为后续的执行引导提供基础。值得注意的是，由于离线数据质量混合，$\pi_{\mathrm{bc}}$ 并非最优策略，但其行为分布位于世界模型的高置信区域，能有效引导在线探索远离模型认知盲区。

### RL 微调中的经验重演与执行引导

微调阶段同时使用在线数据 $\mathcal{D}_{\mathrm{on}}$ 和检索的离线数据 $\mathcal{D}_{\mathrm{retrieved}}$ 更新世界模型与奖励函数，并执行 Dreamer 风格的演员-评论家训练。评论家训练使用 λ-回报作为目标：

$$V_t^{\lambda} = \hat{r}_t + \gamma \left\{ \begin{array}{ll} (1-\lambda) v_{t+1}^{\lambda} + \lambda V_{t+1}^{\lambda} & t < H \\[4pt] v_H^{\lambda} & t = H \end{array} \right.$$

评论家损失最大化 λ-回报的对数似然，演员损失最大化 λ-回报并添加熵正则项促进探索：

$$\mathcal{L}(v_{\phi}) = \mathbb{E}_{p_{\theta}, \pi_{\phi}} \left[ - \sum_{t=1}^{H-1} \ln v_{\phi}(V_t^{\lambda} | s_t) \right], \quad \mathcal{L}(\pi_{\phi}) = \mathbb{E}_{p_{\theta}, \pi_{\phi}} \left[ \sum_{t=1}^{H-1} \left( - V_t^{\lambda} - \eta \cdot \mathbf{H}[a_t | s_t] \right) \right]$$

在在线数据收集阶段，NCRL 按照预定义的线性退火调度，概率性地在 RL 策略 $\pi_{\phi}$ 与行为克隆先验策略 $\pi_{\mathrm{bc}}$ 之间切换。消融实验表明，该调度对具体参数不敏感，NCRL 在多种调度下均表现鲁棒。

### 模块协同机制

上述四个模块形成了一条完整的因果链路：世界模型预训练提供了跨形态共享的隐空间表征，使经验检索能够有效识别任务相关轨迹；检索到的数据通过经验重演缓解了微调阶段的分布偏移（定量证据显示，经验重演将在线数据与离线/专家数据之间的 Wasserstein 距离显著降低）；行为克隆先验策略则利用检索数据引导在线数据收集靠近世界模型的高置信区域，解决了困难探索任务上的探索瓶颈。消融实验证实，世界模型预训练单独不足以在困难任务上工作，必须结合检索式经验重演和执行引导才能显著提升表现。



## 实验与关键发现

### 核心发现：跨72个视觉运动任务的样本效率跃升

NCRL在Meta-World（50个操作任务）和DMControl（22个运动控制任务）共计72个视觉运动任务上，以150k在线交互步的统一预算进行评估。与从零训练的基线方法相比，NCRL取得了近乎翻倍的聚合得分。具体而言，在Meta-World上，NCRL的平均成功率达到**0.748**，而DreamerV3和DrQ-v2在相同150k预算下分别仅为0.360和0.430；在DMControl上，NCRL的平均回合回报为**617.73**，远高于DreamerV3的320.86和DrQ-v2的226.49（Table 4、Table 5）。这意味着NCRL仅用150k步就达到了基线方法需要3.3–6.7倍样本量才能获得的性能水平。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_oBXfPyi47m/figures/048_Table_4.jpg]]
*Table 4: Success rate of Meta-World benchmark with pixel inputs (Cont.)*

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_oBXfPyi47m/figures/051_Table_5.jpg]]
*Table 5: Episodic return of DMControl benchmark with pixel inputs*

在困难探索任务上，NCRL的优势尤为突出。以DMControl的Quadruped Walk为例，NCRL获得**855.6**的回合回报，而DreamerV3在相同预算下仅为145.2（Table 5）；在Meta-World的Shelf Place任务上，NCRL成功率达到**0.80**，DreamerV3则为0.0（Table 4）。这些结果表明，仅靠世界模型预训练远不足以应对困难探索场景，NCRL的经验重演与执行引导机制在其中起到了决定性作用。

### 与离线数据利用方法的对比：在更严苛条件下大幅领先

为公平对比，论文对无法处理多形态数据的基线方法（R3M、UDS-RLPD、ExPLORe、JSRL-BC）进行了预处理，仅向其提供任务相关的离线轨迹子集；而NCRL直接使用包含大量任务无关数据的非整理离线数据。即便在数据条件更严苛的情况下，NCRL仍在具有代表性的困难运动和操作任务上**一致且大幅超越所有对比基线**（Figure 3右）。这一结果说明，NCRL对非整理离线数据的有效利用并非来自数据筛选的便利，而是其检索式经验重演机制的核心能力。

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_oBXfPyi47m/figures/011_Figure_3.jpg]]
*Figure 3: Left: Quantitative comparison across 72 diverse tasks from Meta-World (Yu et al., 2020) and DMControl (Tassa et al., 2018) with the same sample budget (150k). See Sec. I for full results. Right: Learning curves on representative challenging locomotion and robotic manipulation tasks. NCRL consistently outperforms state-of-the-art methods that leverage offline data by a decent margin. We plot the mean and corresponding 95% confidence interval*

与世界模型预训练方法iVideoGPT的对比进一步验证了NCRL的设计优势。iVideoGPT使用了奖励塑形（reward shaping）和专家演示回放预填充等技术，而NCRL**未使用任何此类技巧**，却取得了更优的性能（Figure 4）。这排除了正交工程优化对性能增益的干扰，表明NCRL的优势根植于经验重演和执行引导对分布偏移的缓解。

### 关键组件消融：预训练、经验重演与执行引导缺一不可

消融实验（Figure 6）系统拆解了NCRL的三个核心组件：世界模型预训练（P）、检索式经验重演（ER）和执行引导（G）。结果表明，**单独的世界模型预训练在离线数据分布较窄时完全失效**；只有当三个组件协同工作时，RL性能才能在多样化任务上获得显著提升。具体而言：

![[assets/figures/papers/paper_list_l47_https_openreview_net_forum_id_oBXfPyi47m/figures/021_Figure_6.jpg]]
*Figure 6: Ablation study on key components. “P” represents world model pre-training, “ER” means experience rehearsal, and “G” represents execution guidance. The combination of a pre-trained taskagnostic world model with retrieval-based experience rehearsal and execution guidance boosts RL performance across diverse tasks*

- **预训练（P）的作用**：预训练世界模型为RL提供了良好的初始表征，但当离线数据分布与目标任务存在偏移时，单纯微调世界模型无法克服分布失配。
- **经验重演（ER）的量化效果**：Figure 2（右）显示，经验重演将在线数据与离线数据之间的Wasserstein距离从随机检索的约0.31降至约0.12，与专家数据的距离也显著缩小。这为经验重演缓解分布偏移提供了定量证据。
- **执行引导（G）的不可替代性**：在Assembly和Stick Pull等困难探索任务上，NCRL使用的执行引导远超基于不确定性奖励标记的替代方案（OTS）（Figure 7），表明将智能体引导至世界模型高置信区域比单纯基于不确定性探索更为有效。

进一步的组件角色消融（Figure 13）和世界模型微调策略分析（Figure 8）表明：微调完整世界模型（而非冻结编码器）可获得最佳性能；冻结编码器或仅微调解码器均会导致性能显著下降。

### 鲁棒性验证：对调度与数据质量不敏感

NCRL对执行引导的退火调度表现出高度鲁棒性——在多种调度方案下性能均保持稳定（Figure 12）。更为关键的是，即使向检索数据中注入大量任务无关轨迹（最高达50%），NCRL的性能退化仍然缓慢（Figure 14），验证了检索机制在低质量非整理数据下的容错能力。检索精度实验（Table 2）显示，在多数任务上检索精度达到100%，仅在Door Open等部分任务上出现下降，但整体仍维持可用水平。

### 持续任务适应与模型规模分析

在持续任务适应场景中，NCRL显著优于广泛使用的PackNet方法——PackNet仅能达到NCRL回合回报的20–60%（Figure 5）。此外，模型规模对比（Figure 15）表明，NCRL一致优于不同规模配置下的DreamerV3变体，且随着训练预算增加，性能持续提升（Figure 16），未出现明显的收益递减。

### 失败模式与待验证边界

尽管NCRL在仿真环境中表现强劲，以下边界需注意：

1. **仿真到现实的迁移**：当前所有实验均在仿真环境中完成，向真实机器人平台的迁移仍待验证。
2. **对完全野生数据的泛化**：NCRL依赖领域相关的非整理离线数据，尚未验证其在大规模异构互联网视频等“完全野生”数据上的有效性。
3. **架构限制**：当前世界模型架构固定为RSSM，与Transformer等新架构的结合潜力未被探索。
4. **全新形态泛化**：对未见过的全新形态或任务配置，NCRL的泛化能力尚不明确。

这些边界为后续研究指明了方向，也为评估NCRL的实际部署价值提供了必要的审慎视角。



## 定位与知识库关联

### 1. 与现有离线数据利用方法的区别

NCRL 处于**基于模型的离线到在线强化学习**的交叉点，其核心差异在于对非整理离线数据的全生命周期利用。Table 1 系统对比了 NCRL 与代表性方法的能力边界：

| 方法 | 无奖励数据 | 非专家数据 | 跨形态数据 | 持续提升 | 训练稳定性 |
|------|-----------|-----------|-----------|---------|-----------|
| **R3M** (Nair et al., 2022) | ✓ | ✓ | ✓ | ✗ | ✗ |
| **UDS-RLPD** (Yu et al., 2022; Ball et al., 2023) | ✓ | ✓ | ✗ | ✗ | ✗ |
| **ExPLORe** (Li et al., 2023) | ✓ | ✗ | ✗ | ✗ | ✗ |
| **JSRL-BC** (Uchendu et al., 2023) | ✗ | ✗ | ✗ | ✗ | ✗ |
| **NCRL** (本文) | ✓ | ✓ | ✓ | ✓ | ✓ |

**关键差异点**：

- **R3M** 仅做视觉表征预训练，冻结编码器后从零训练 RL，无法利用离线数据中的动力学知识，且在困难任务上训练不稳定。
- **UDS-RLPD** 用零奖励标记离线数据，但依赖单一形态假设，无法处理跨形态数据；其 RLPD 微调框架在分布偏移严重时性能退化。
- **ExPLORe** 基于不确定性为离线数据自动标记奖励，但假设离线数据质量较高（含专家轨迹），在混合质量数据上奖励标记不可靠。
- **JSRL-BC** 用行为克隆初始化策略，但需要专家演示数据，无法利用次优轨迹。

**公平性说明**：在与上述基线对比时，论文为它们预处理了离线数据，仅保留任务相关轨迹；而 NCRL 直接使用包含大量无关数据的非整理离线数据，在更困难的数据条件下仍取得大幅领先（Fig. 3右）。

### 2. 与世界模型预训练方法的关系

NCRL 的世界模型预训练与微调范式建立在 **DreamerV3** (Hafner et al., 2023) 的 RSSM 架构之上，但做了三项关键修改：

1. **去除任务相关损失**：DreamerV3 包含奖励预测和继续预测头，NCRL 将其移除，使世界模型完全任务无关。
2. **动作零填充统一维度**：跨形态的动作空间维度不同，NCRL 通过零填充统一到最大维度，使单个 RSSM 能处理多种形态。
3. **模型缩放至 280M 参数**：相比 DreamerV3 的默认配置显著增大，以吸收多形态数据的多样性。

与 **iVideoGPT** (Wu et al., 2025) 的对比尤为关键。iVideoGPT 同样预训练世界模型，但依赖**奖励塑形**和**专家回放缓冲区预填充**来启动在线 RL。NCRL 不使用这些技巧，仅通过经验重演和执行引导即取得更优性能（Fig. 4），说明离线数据的有效重用比工程技巧更具决定性。

**与冻结编码器方法的区别**：消融实验（Fig. 8）表明，微调完整世界模型优于仅冻结编码器或仅微调解码器。冻结编码器（类似 R3M 范式）丢失了通过在线数据持续修正表征的机会，在分布偏移下性能显著下降。

### 3. 适用边界与局限

**已验证的有效范围**：
- **环境类型**：仿真环境中的视觉运动控制任务，涵盖 72 个任务、6 种形态（Meta-World 机械臂、DMControl 运动体）。
- **数据规模**：离线数据包含数万条轨迹，在线交互预算 150k 步。
- **数据特性**：无奖励、混合质量（含随机策略和专家策略数据）、多形态。

**已知局限**：

1. **仿真到现实的鸿沟**：所有实验均在仿真环境中完成，尚未在真实机器人上验证。仿真中的分布偏移与真实环境中的动力学差异可能叠加，需要额外的域适应机制。

2. **对领域相关离线数据的依赖**：经验检索依赖离线数据中存在与目标任务相关的轨迹。若离线数据完全不包含任务相关信息（如互联网视频中的野生数据），检索将退化，方法可能失效。论文明确指出无法利用 "in-the-wild" 数据。

3. **架构限制**：世界模型限定为 RSSM，未探索与 Transformer 等新架构的结合。RSSM 的循环结构可能限制对长程依赖的建模能力。

4. **泛化边界未充分测试**：对未见过的全新形态或任务配置，泛化能力仍有待验证。当前实验中的形态均在离线数据中出现过。

### 4. 开放问题

**数据扩展方向**：
- 如何将经验检索机制扩展到大规模野生视觉数据（如互联网视频），使其能在完全无任务先验的情况下自动发现相关子集？这可能需要引入语言引导或视觉-语言对齐的检索机制。

**架构演进方向**：
- 能否将执行引导与经验重演思想与 Transformer-based world models 结合？Transformer 的并行推理能力可能提升检索效率，其注意力机制可能自然支持跨形态的动力学共享。

**安全性与实际部署**：
- 在真实多形态机器人平台上，执行引导中的行为克隆先验策略可能产生不安全动作。需要研究如何在保持探索效率的同时引入安全约束。

**跨形态迁移的理论理解**：
- 当前方法依赖动作零填充的简单统一策略，缺乏对形态间动力学相似性的显式建模。是否能通过离线数据中的动作先验和动力学知识实现更高效的跨形态迁移学习，是一个值得深入的理论问题。



## 原文 PDF

![[paperPDFs/ICLR_2026/Efficient_Reinforcement_Learning_by_Guiding_World_Models_with_Non_Curated_Data.pdf]]
