---
title: "TraPO: A Semi-Supervised Reinforcement Learning Framework for Boosting LLM Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/TraPO_A_Semi_Supervised_Reinforcement_Learning_Framework_for_Boosting_LLM_Reasoning.pdf
openreview_forum_id: 3K1y4KbWAx
aliases:
- TTBPO
- TraPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "无标签样本的通过率轨迹（pass rate trajectory）与有标签样本的通过率轨迹的余弦相似度（trajectory alignment）。"
primary_logic: "少量的有标签样本可以作为‘锚点’来稳定基于一致性的无监督训练：只有当无标签样本的学习动态（通过率轨迹）与有标签样本的轨迹高度一致时，其推理模式才被视为可靠，并纳入强化学习训练，从而避免错误共识的强化。"
claims:
- "仅使用1K有标签+3K无标签样本，TRAPO的域内平均准确率达到42.6%，超过在45K无标签样本上训练的最佳无监督方法（Self-certainty，38.3%）。"
- "使用4K有标签+12K无标签样本时，TRAPO在所有基准上超越在全量45K有标签样本上训练的完全监督模型（ID Avg. 45.6 vs 45.5，OOD Avg. 59.7 vs 57.3）。"
- "无标签样本的通过率轨迹与有标签数据库平均轨迹的余弦相似度（TCS）能够有效区分可靠与不可靠样本，高相似度样本的性能显著优于低相似度样本（top 10% vs bottom 10% 差距超过40%）。"
- "TRAPO的轨迹选择策略即插即用，与多种无监督基线（Sentence-level Entropy, Token-level Entropy, TTRL）结合后，性能均优于简单的半监督组合。"
---

# TraPO: A Semi-Supervised Reinforcement Learning Framework for Boosting LLM Reasoning

> [!tip] 核心洞察
> 少量的有标签样本可以作为‘锚点’来稳定基于一致性的无监督训练：只有当无标签样本的学习动态（通过率轨迹）与有标签样本的轨迹高度一致时，其推理模式才被视为可靠，并纳入强化学习训练，从而避免错误共识的强化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | TraPO：一种用于提升大语言模型推理的半监督强化学习框架 |
| 英文题名 | TraPO: A Semi-Supervised Reinforcement Learning Framework for Boosting LLM Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3K1y4KbWAx); [GitHub](https://github.com/ShenzhiYang2000/TRAPO) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | TRAPO (Trajectory-based Policy Optimization) |
| Dataset | In-Distribution (AIME, AMC, MATH-500, Minerva, Olympiad) average, Out-of-Distribution (ARC-c, GPQA*, MMLU-Pro) average, In-Distribution average, Cross-domain OOD (non‑math unlabeled) – ID average |

> [!tip] 效果简介
> - In-Distribution (AIME, AMC, MATH-500, Minerva, Olympiad) average 上，Accuracy (%) 为 42.6 (1K labeled + 3K unlabeled)，对比 38.3 (Self-certainty, 45K unlabeled)，变化 +4.3%。
> - Out-of-Distribution (ARC-c, GPQA*, MMLU-Pro) average 上，Accuracy (%) 为 56.1 (1K labeled + 3K unlabeled)，对比 48.4 (Self-certainty, 45K unlabeled)，变化 +7.7%。
> - In-Distribution average 上，Accuracy (%) 为 45.6 (4K labeled + 12K unlabeled)，对比 45.5 (Fully Supervised, 45K labeled)，变化 +0.1%。

## 概述

**问题瓶颈**：现有的大语言模型推理强化学习（RLVR）主要依赖两类范式——完全有监督（需大量标注）和完全无监督（基于自洽性奖励）。无监督RLVR在训练后期因缺乏外部监督信号，倾向于强化错误的推理模式，导致性能坍塌；而简单的半监督组合（将两类数据直接混合训练）忽视了有标签与无标签数据之间的内在联系，仅带来约0.6%的边际提升，未能有效利用无标签数据。

**核心思想**：TRAPO 提出以**通过率轨迹（pass rate trajectory）** 为桥梁，连接有标签与无标签数据的学习动态。其核心假设是：少量有标签样本可以作为“锚点”来稳定基于一致性的无监督训练——仅当无标签样本的通过率变化轨迹与有标签样本的平均轨迹高度一致时，其推理模式才被视为可靠，并被纳入强化学习训练。这一机制通过**轨迹余弦相似度（TCS）** 量化对齐程度，从而避免错误共识的强化。

**方法定位**：TRAPO 属于**半监督RLVR**范式，在标准GRPO框架上引入三个关键模块：(1) 混合奖励函数——有标签数据使用真实答案奖励，无标签数据使用多数投票伪标签奖励；(2) 动态样本选择——基于TCS筛选可靠无标签样本参与训练；(3) 预热机制——训练初期仅用有标签数据更新策略，同时累积无标签轨迹，确保选择稳定性。该方法即插即用，可与多种无监督基线（如Sentence-level Entropy、Token-level Entropy、TTRL）结合。

**主要结果**：
- **高效标注利用**：仅使用1K有标签+3K无标签样本，TRAPO的域内平均准确率达到42.6%，超越在45K无标签样本上训练的最佳无监督方法Self-certainty（38.3%），提升4.3个百分点（Table 1）。
- **超越全量监督**：使用4K有标签+12K无标签样本（仅10%标注率），TRAPO在所有基准上超越使用全量45K有标签样本训练的完全监督模型（域内平均45.6 vs 45.5，域外平均59.7 vs 57.3）（Figure 1左）。
- **轨迹选择有效性**：TCS能够有效区分可靠与不可靠样本——高相似度样本（top 10%）的性能显著优于低相似度样本（bottom 10%），差距超过40%（Figure 4）。
- **即插即用性**：TRAPO的轨迹选择策略与多种无监督基线结合后，性能均优于简单的半监督组合（Figure 7）。
- **Scaling特性**：随着数据规模增加，TRAPO在25%标注率下即可接近或达到完全监督性能（Figure 1右）。

## 背景与动机

### 大语言模型推理能力的强化学习训练

大语言模型（LLM）的推理能力近年来取得了显著进展，其中基于可验证奖励的强化学习（RLVR）已成为核心训练范式。RLVR通过定义可自动验证的奖励函数（如数学题答案匹配），使模型能够在无需人工标注的情况下，通过自我探索与反馈优化推理策略。GRPO（Shao et al., 2024）等代表性方法已成功将RLVR应用于数学推理等任务，取得了令人瞩目的性能提升。

### 有监督与无监督RLVR的困境

当前的RLVR训练主要存在两种范式，但各自面临根本性瓶颈：

**有监督RLVR**依赖于大量人工标注的正确答案。当标注数据充足时，模型能够稳定地从真实奖励信号中学习，性能随数据规模持续提升。然而，高质量标注的成本极高，尤其在数学竞赛、科学推理等专业领域，标注者本身需要具备相应的专业能力。这一成本约束严重限制了有监督RLVR的规模化应用。

**无监督RLVR**试图摆脱对标注的依赖，通过自洽性奖励（如多数投票一致性）提供伪监督信号。然而，这一范式面临一个关键问题：**模型在训练后期会强化错误的推理模式，导致性能坍塌**。其根本原因在于，当模型对某些问题形成错误但一致的推理路径时，多数投票机制会将这种“错误共识”误判为正确，进而通过奖励信号不断强化，形成自我欺骗的恶性循环。实验表明，即使在45K无标签样本上训练的最佳无监督方法（Self-certainty, Zhao et al., 2025），其域内平均准确率仅为38.3%，远低于全量有监督训练的45.5%。

### 简单半监督组合的不足

一个自然的思路是将有监督与无监督方法进行半监督组合——对少量有标签数据使用真实奖励，对大量无标签数据使用自洽性奖励。然而，这种简单的组合策略忽视了有标签数据与无标签数据之间的内在联系：并非所有无标签样本的推理模式都同样可靠，直接将全部无标签样本纳入训练会将不可靠样本的噪声引入优化过程，损害模型性能。

### 核心动机：从“学什么”转向“怎么学”

本文的核心动机源自一个关键观察：**少量有标签样本可以作为“锚点”，通过监控模型在这些锚点上的学习动态，来评估无标签样本推理模式的可靠性**。具体而言，模型在训练过程中对每个样本的通过率（pass rate）会随训练轮次演化，形成一条通过率轨迹。有标签样本的轨迹反映了在真实奖励引导下的可靠学习动态，而无标签样本的轨迹则可能因伪标签噪声而偏离。通过度量无标签样本轨迹与有标签样本轨迹的相似度，可以识别出那些学习动态与可靠模式一致的无标签样本，从而在利用大规模无标签数据的同时，避免错误共识的强化。

这一视角将关注点从“模型学到了什么”（输出层面的正确性）转向“模型是怎么学的”（训练动态层面的轨迹一致性），为半监督RLVR提供了新的理论框架。

## 核心创新

### 问题瓶颈：无监督RLVR的性能坍塌

当前基于强化学习的大语言模型推理训练（RLVR）面临一个根本性困境：**完全有监督的RLVR**（如**Fully Supervised GRPO**，Shao et al., 2024）依赖大量人工标注的真实答案，成本高昂；而**完全无监督的RLVR**（如基于多数投票伪标签的**TTRL**、最大化自确定性的**Self-certainty**、最小化token级熵的**Token-level Entropy**等）虽摆脱了对标签的依赖，却在训练后期因缺乏外部监督而**持续强化错误的推理模式**，导致模型性能不升反降——即“性能坍塌”。简单的半监督组合（将有标签与无标签数据的损失直接相加）忽视了二者之间的内在联系，无法有效利用无标签数据来稳定训练过程，性能提升微乎其微。

### 核心洞察：以有标签样本为“锚点”稳定无监督训练

TRAPO的核心洞察在于：**少量的有标签样本可以作为“锚点”来校准无监督训练的方向**。具体而言，TRAPO并不直接信任所有无标签样本的自洽性奖励，而是转而观察模型在训练过程中对每个样本的**学习动态**——即“通过率轨迹”（pass rate trajectory，各训练epoch中生成回答满足期望答案的比例序列）。其关键假设是：**只有当无标签样本的学习动态与有标签样本的学习动态高度一致时，该无标签样本的推理模式才被视为可靠**，其伪标签才值得信赖并纳入强化学习训练。这一机制从根本上避免了模型在无监督训练中形成并强化错误共识。

### 关键创新点（Changed Slots）

**1. 训练范式：从“完全有/无监督”到“动态半监督”**

| 维度 | 基线方法 | TRAPO |
|------|---------|-------|
| 有标签数据 | 使用ground‑truth奖励（`R(τ, y) = I(a = y)`） | 同基线 |
| 无标签数据 | 全部直接使用自洽性奖励（如多数投票） | 仅纳入经轨迹筛选的**可靠子集**，使用自洽性奖励 |
| 训练目标 | 有监督与无监督损失简单相加 | 有标签GRPO损失 + 经掩码筛选的无标签GRPO损失（Eq. 8） |

混合奖励函数（Eq. 3）形式上与简单半监督方法相同，但TRAPO的关键区别在于**对无标签样本施加了动态选择掩码**（Eq. 7），仅允许通过轨迹一致性检验的样本参与梯度更新。

**2. 无标签数据利用方式：从“全量使用”到“轨迹对齐筛选”**

TRAPO引入**轨迹余弦相似度（Trajectory Cosine Similarity, TCS）**作为无标签样本可靠性的核心度量（Eq. 6）。具体流程为：

- 维护一个**可靠轨迹数据库**，初始化为所有有标签样本的通过率轨迹，后续将筛选出的可靠无标签轨迹动态加入；
- 计算每个无标签样本的通过率轨迹与数据库**平均可靠轨迹**的余弦相似度；
- 通过**top‑p比例 + 阈值Γ**双重标准筛选高相似度样本（Eq. 7），仅将这些样本纳入训练。

这一设计将“学什么”的问题转化为“怎么学”的问题——通过观察学习过程的动态一致性来间接判断伪标签的质量，而非依赖单点的输出置信度。

**3. 训练稳定性机制：从“无保护”到“预热+渐进纳入”**

为防止训练初期模型尚未形成稳定推理模式时错误纳入噪声样本，TRAPO设计了**预热阶段**：在初始若干epoch内仅使用有标签数据进行GRPO更新，同时计算并记录所有无标签样本的伪通过率轨迹，但不将其纳入损失函数。预热结束后，再应用选择掩码逐步纳入可靠无标签样本。这一机制有效避免了训练早期的错误信号污染。

### 理论支撑

TRAPO提供了**泛化误差界**（Theorem 3.1，非正式版本见Eq. 10），将目标域风险分解为三项：

1. 源域（有标签数据）经验风险；
2. **轨迹不一致性惩罚项**（`1 - TCS`的期望），约束无标签样本的学习动态偏离；
3. 投票置信度项，反映伪标签的统计可靠性。

该理论界为“轨迹对齐能提升泛化性能”提供了形式化依据，解释了为何筛选高TCS样本能够稳定训练并提升最终性能。

### 创新点的实验验证

- **轨迹相似度的区分能力**：Figure 4显示，TCS得分前10%的无标签样本性能比后10%高出**超过40个百分点**，证明轨迹对齐能有效识别可靠样本。
- **即插即用性**：Figure 7和附录E.3表明，将TRAPO的轨迹选择策略与多种无监督基线（Sentence-level Entropy、Token-level Entropy、TTRL）结合后，性能均优于简单的半监督组合，验证了该策略的通用性。
- **消融实验**：与随机选择、基于句子熵的选择及基于自确定性的选择相比，TRAPO在相同选择比例下性能显著更优（Table 13），确认了轨迹对齐信号优于单点置信度指标。

## 整体框架

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_3K1y4KbWAx/figures/004_Figure_3.jpg]]
*Figure 3: TRAPO is a semi-supervised RLVR training framework to dynamically select reliable unlabeled samples throughout the training process based on pass rate trajectory matching*

TRAPO 是一个半监督强化学习推理框架，其核心目标是在仅有少量有标签样本的条件下，通过动态筛选可靠的无标签样本，稳定且高效地提升大语言模型的推理能力。该框架的底层瓶颈在于：纯无监督 RLVR 在训练后期会强化错误的推理模式，导致性能坍塌；而简单的半监督组合（直接混合有标签与无标签数据）忽视了二者之间的内在联系，无法有效利用无标签数据。TRAPO 的关键因果调节变量是**无标签样本的通过率轨迹与有标签样本平均轨迹的余弦相似度**（Trajectory Cosine Similarity, TCS），其核心洞察是：少量有标签样本可以作为“锚点”来稳定基于一致性的无监督训练——只有当无标签样本的学习动态与有标签样本高度一致时，其推理模式才被视为可靠，并纳入强化学习。

整个 pipeline 由六个顺序耦合的模块构成，其输入输出流如 Figure 3 所示。

### 1. 预热训练 (Warm-up)

训练开始时，TRAPO 进入预热阶段。在此阶段，**仅使用有标签数据** $\mathcal{D}_l$ 进行 GRPO 更新，同时计算并记录所有无标签样本 $\mathcal{D}_u$ 的伪通过率轨迹。这一设计的目的是为轨迹相似度计算积累足够长的历史序列，避免在模型初期表现不稳定时引入噪声选择。预热轮数（warmup epochs）是一个可调超参数，默认设为 5，消融实验表明设为 8 可进一步提升域内性能（Table 11）。

### 2. 通过率计算 (Pass Rate Computation)

对每个样本，在每个训练 epoch $t$，计算其通过率 $P_q^{(t)}$。对于有标签数据，通过率定义为生成回答与真实答案 $y$ 一致的比例；对于无标签数据，则使用当前 epoch 的多数投票伪标签 $\tilde{y}^{(t)}$ 作为替代标准：

$$P_q^{(t)} = \begin{cases} \frac{1}{G}\sum_{i=1}^G \mathbb{I}(a_i^{(t)} = \tilde{y}^{(t)}), & q \in \mathcal{D}_u \\ \frac{1}{G}\sum_{i=1}^G \mathbb{I}(a_i^{(t)} = y), & q \in \mathcal{D}_l \end{cases}$$

其中 $G$ 为每个问题生成的回答数量，$a_i^{(t)}$ 为第 $i$ 条回答中提取的答案。

### 3. 轨迹数据库维护 (Trajectory Database)

TRAPO 维护一个可靠轨迹数据库 $\mathcal{D}_{\text{reliable}}$。该数据库在训练开始时初始化为所有有标签样本的通过率轨迹。在预热阶段结束后，每个 epoch 会将经过筛选的可靠无标签样本轨迹加入数据库，并计算平均可靠轨迹 $\bar{\mathbf{T}}_{\text{reliable}}^{(t)}$：

$$\mathbf{T}_q^{(t)} = [P_q^{(1)}, P_q^{(2)}, \ldots, P_q^{(t)}]$$

平均可靠轨迹作为衡量无标签样本“可靠性”的基准参考。

### 4. 轨迹余弦相似度 (Trajectory Cosine Similarity, TCS)

对于每个无标签样本 $u$，计算其当前轨迹 $\mathbf{T}_u^{(t)}$ 与平均可靠轨迹 $\bar{\mathbf{T}}_{\text{reliable}}^{(t)}$ 的余弦相似度：

$$\mathrm{TCS}(\mathbf{T}_u^{(t)}, \bar{\mathbf{T}}_{\text{reliable}}^{(t)}) = \hat{\mathbf{T}}_u^{(t)} \cdot \hat{\bar{\mathbf{T}}}_{\text{reliable}}^{(t)}$$

其中 $\hat{\cdot}$ 表示 L2 归一化。TCS 度量了无标签样本与有标签样本在学习动态上的一致性——高相似度意味着该无标签样本的推理模式受到有标签锚点的“外部验证”。

### 5. 可靠样本选择 (Reliable Sample Selection)

TRAPO 采用双重筛选机制确定哪些无标签样本可以参与训练。选择掩码 $\mathbf{M}(u)$ 的定义为：

$$\mathbf{M}(u) = \mathbb{I}(u \in \text{top-p}(\mathrm{TCS})) \vee \mathbb{I}(\mathrm{TCS} \geq \Gamma)$$

即同时满足两个条件之一：TCS 位于所有无标签样本的前 $p$ 比例，或 TCS 超过绝对阈值 $\Gamma$。消融实验表明，$\text{top-p}=0.3$ 和 $\Gamma=0.5$ 时取得最佳综合性能（Table 9, Table 10）。被选中的无标签样本轨迹随后被加入可靠轨迹数据库，用于下一轮的平均轨迹计算。

### 6. 掩码 GRPO 损失 (Masked GRPO Loss)

最终，TRAPO 的总损失函数为有标签 GRPO 损失与经掩码筛选的无标签 GRPO 损失的加权组合：

$$\mathcal{L}(\theta) = \mathcal{I}_{\mathrm{GRPO}}^{\mathrm{labeled}}(\theta) + \mathbf{M} \odot \mathcal{I}_{\mathrm{GRPO}}^{\mathrm{unlabeled}}(\theta)$$

其中 GRPO 目标 $\mathcal{I}_{\mathrm{GRPO}}(\theta)$ 采用标准的带裁剪的重要性采样伪损失与 KL 惩罚项（Eq. 9）。有标签数据的奖励来自真实答案匹配，无标签数据的奖励来自多数投票自洽性。通过掩码 $\mathbf{M}$，只有学习动态与有标签锚点高度一致的无标签样本才会贡献梯度，从而避免了错误共识的强化。

### 输入输出流总结

- **输入**：少量有标签数据集 $\mathcal{D}_l$（含问题-答案对）和大量无标签数据集 $\mathcal{D}_u$（仅含问题）。
- **内部状态**：可靠轨迹数据库 $\mathcal{D}_{\text{reliable}}$ 及其平均轨迹 $\bar{\mathbf{T}}_{\text{reliable}}$，每个样本的通过率轨迹 $\mathbf{T}_q$。
- **输出**：经过半监督 RLVR 优化的策略模型 $\pi_\theta$，其在域内和域外推理基准上的准确率显著提升。

该框架的关键设计选择——以通过率轨迹而非单点指标（如熵或自确定性）作为可靠性判据——源于一个核心发现：无标签样本的通过率轨迹与有标签数据库平均轨迹的余弦相似度能够有效区分可靠与不可靠样本，高相似度样本（top 10%）的性能显著优于低相似度样本（bottom 10%），差距超过 40%（Figure 4）。此外，该轨迹选择策略具有即插即用特性，与多种无监督基线（Sentence-level Entropy、Token-level Entropy、TTRL）结合后，性能均优于简单的半监督组合（Figure 7）。

## 核心模块与公式推导

### 半监督混合奖励函数

TRAPO 的核心训练范式是半监督RLVR，其奖励函数根据数据来源分情况处理。对于有标签数据，使用与真实答案匹配的二元奖励；对于无标签数据，使用多数投票生成的自洽性伪奖励：

$$R_{\mathrm{semi}}(\tau_i^j) = \begin{cases} R(\tau_i^j, y_i), & (q_i, y_i) \in \mathcal{D}_l \\ R_u(\tau_i^j), & q_i \in \mathcal{D}_u \end{cases}$$

其中：
- $R(\tau_i^j, y_i) = \mathbb{I}(a_i^j = y_i)$：有监督奖励，提取的回答与真实答案一致时为1，否则为0（Eq. 1）。
- $R_u(\tau_i^j) = \mathbb{I}(a_i^j = \mathbf{MAJ}(a_i^1,\dots,a_i^G))$：无监督奖励，回答与$G$次采样中的多数投票结果一致时为1（Eq. 2）。

这一混合奖励是TRAPO的基础损失信号来源，但有标签与无标签数据的简单混合并不能有效利用无标签数据（简单半监督组合仅带来约0.6%的微弱提升）。TRAPO的关键创新在于如何筛选可靠的无标签样本参与训练。

### 通过率轨迹与轨迹数据库

TRAPO不依赖单次推理结果，而是追踪每个样本在整个训练过程中的**通过率轨迹**来刻画其学习动态。对每个训练轮次$t$，样本$q$的通过率定义为：

$$P_q^{(t)} = \begin{cases} \frac{1}{G}\sum_{i=1}^G \mathbb{I}(a_i^{(t)} = \tilde{y}^{(t)}), & q \in \mathcal{D}_u \\ \frac{1}{G}\sum_{i=1}^G \mathbb{I}(a_i^{(t)} = y), & q \in \mathcal{D}_l \end{cases}$$

其中无标签样本使用当前轮次的多数投票伪标签$\tilde{y}^{(t)}$，有标签样本使用真实标签$y$。累积$t$个轮次的通过率即构成通过率轨迹：

$$\mathbf{T}_q^{(t)} = [P_q^{(1)}, P_q^{(2)}, \ldots, P_q^{(t)}]$$

TRAPO维护一个**可靠轨迹数据库**$\mathcal{D}_{\text{reliable}}$：初始化为所有有标签样本的轨迹，后续将经筛选的可靠无标签轨迹加入，并计算平均可靠轨迹$\bar{\mathbf{T}}_{\text{reliable}}^{(t)}$作为对齐基准。

### 轨迹余弦相似度（TCS）与可靠样本选择

TRAPO通过计算无标签样本轨迹与平均可靠轨迹的余弦相似度来衡量其推理模式的可靠性：

$$\mathrm{TCS}(\mathbf{T}_u^{(t)}, \bar{\mathbf{T}}_{\mathrm{reliable}}^{(t)}) = \hat{\mathbf{T}}_u^{(t)} \cdot \hat{\bar{\mathbf{T}}}_{\mathrm{reliable}}^{(t)}$$

其中$\hat{\cdot}$表示L2归一化后的向量。TCS越高，说明该无标签样本的学习动态与有标签样本越一致，其推理模式越可能被外部监督验证。

基于TCS，TRAPO通过**top-p比例**和**阈值$\Gamma$**双重条件筛选可靠无标签样本：

$$\mathbf{M}(u) = \mathbb{I}(u \in \mathrm{top\text{-}p}(\mathrm{TCS})) \vee \mathbb{I}(\mathrm{TCS} \geq \Gamma)$$

即选取TCS位于前$p$比例或超过阈值$\Gamma$的无标签样本参与训练。消融实验表明，top-p=0.3和$\Gamma=0.5$时取得最优综合性能（ID Avg. 41.7/42.6，OOD Avg. 53.6/56.1），过高或过低均导致性能下降。

### 掩码GRPO损失

TRAPO的最终优化目标是将有标签GRPO损失与经掩码筛选的无标签GRPO损失结合：

$$\mathcal{L}(\theta) = \mathcal{I}_{\mathrm{GRPO}}^{\mathrm{labeled}}(\theta) + \mathbf{M} \odot \mathcal{I}_{\mathrm{GRPO}}^{\mathrm{unlabeled}}(\theta)$$

其中GRPO目标函数为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \frac{1}{\sum_{i=1}^G |\tau_i|} \sum_{i=1}^G \sum_{l=1}^{|\tau_i|} \mathrm{CLIP}(\gamma_{i,l}(\theta), A_i, \epsilon) - \beta \cdot \mathbb{D}_{\mathbf{KL}}[\pi_\theta || \pi_{\mathrm{ref}}]$$

其中$\gamma_{i,l}(\theta) = \frac{\pi_\theta(o_{i,l}|q, o_{i,<l})}{\pi_{\theta_{\text{old}}}(o_{i,l}|q, o_{i,<l})}$为重要性采样比率，$A_i$为组内标准化优势函数，$\mathrm{CLIP}$为裁剪操作，$\mathbb{D}_{\mathbf{KL}}$为与参考策略的KL散度惩罚项。

### 预热机制

为保证训练初期轨迹的稳定性，TRAPO采用**预热阶段**：前若干轮次仅使用有标签数据更新策略模型，同时计算并记录无标签样本的通过率轨迹，但不纳入损失计算。预热结束后，再应用选择掩码纳入可靠无标签样本。消融实验显示，预热轮数设为8时域内平均分数最高（43.1），比默认5轮略有提升。

### 理论泛化界（Theorem 3.1）

TRAPO给出了一个非正式的理论泛化界，将目标域泛化误差上界分解为三项：

$$\mathcal{R}_{\mathcal{D}_l}(\pi_\theta^{(t)}) + \lambda' + \alpha \cdot \mathbb{E}_{q'\sim\mathcal{D}_u}[1 - \mathrm{TCS}(\mathbf{T}_{q'}^{(t)}, \bar{\mathbf{T}}_{\mathrm{reliable}}^{(t)})] + L_{\mathcal{Y}}(1 - \bar{C}^{(t)} + \sqrt{\frac{\ln(2n/\delta)}{2G}})$$

其中第一项为源域经验风险，第二项为轨迹不一致性惩罚（无标签轨迹与可靠轨迹的偏离程度），第三项为多数投票置信度项。该界从理论上解释了为何轨迹对齐能够控制泛化误差：无标签样本的轨迹与有标签样本越一致，其引入的泛化风险越低。

## 实验与分析

### 核心瓶颈与动机验证

TRAPO 解决的核心问题是**无监督 RLVR 的性能坍塌**。在缺乏外部监督的情况下，模型会在训练后期不断强化自身的错误推理模式，形成“错误共识”（wrong consensus），导致准确率不升反降。简单的半监督组合——将有标签 GRPO 损失与无标签 GRPO 损失直接相加——忽视了有标签与无标签数据之间的内在联系，仅带来边际提升（约 0.6%），远未释放无标签数据的潜力。

TRAPO 的核心洞察在于：**少量有标签样本可以作为“锚点”来稳定基于一致性的无监督训练**。只有当无标签样本的学习动态（通过率轨迹）与有标签样本的轨迹高度一致时，其推理模式才被视为可靠，并被纳入强化学习训练。这一机制通过轨迹余弦相似度（TCS）实现——即无标签样本的通过率轨迹与有标签数据库平均轨迹的余弦相似度——从而避免错误共识的强化。

### 主实验结果

**Table 1** 展示了 Qwen2.5-Math-7B 在三种训练范式下的综合性能。核心发现如下：

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_3K1y4KbWAx/figures/005_Table_1.jpg]]
*Table 1: Overall performance based on Qwen2.5-Math-7B under three different training paradigms. Bold and underline indicate the best and second-best results, respectively*

**极低标注率下的突破**：仅使用 1K 有标签 + 3K 无标签样本，TRAPO 的域内平均准确率达到 **42.6%**，超过在 45K 无标签样本上训练的最佳无监督方法 **Self-certainty**（38.3%，Zhao et al., 2025），提升 **+4.3%**；同时超越最佳简单半监督组合 2.6%，以及使用相同 1K 标签的完全监督模型（39.4%）3.2%。在分布外基准上，TRAPO 达到 **56.1%**，比 Self-certainty（48.4%）高出 **+7.7%**。

**以 10% 标注成本超越全量监督**：当使用 4K 有标签 + 12K 无标签样本时（仅占全量 45K 标签的约 10%），TRAPO 在所有基准上超越在全量 45K 有标签样本上训练的完全监督模型——域内平均 **45.6 vs 45.5**，分布外平均 **59.7 vs 57.3**。这一结果表明，TRAPO 的轨迹选择策略能够有效甄别高质量无标签样本，使其贡献接近甚至超越真实标签的价值。

**跨域泛化能力**：Table 2 展示了更具挑战性的跨域场景——使用 1K 数学（域内）有标签样本和 1K 非数学（分布外）无标签样本。TRAPO 的域内平均达到 **41.0%**，超过 Self-certainty（39.2%）1.8%，并接近完全监督的 41.9%；分布外平均达到 **56.9%**，显著超过所有无监督和简单半监督基线。这表明轨迹相似度信号在跨域场景下仍然有效。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_3K1y4KbWAx/figures/006_Table_2.jpg]]
*Table 2: Performance of different training paradigms with 1K labeled math (ID) samples and 1K unlabeled non-math (OOD) samples. Bold and underline indicate the best and second-best results, respectively*

### 轨迹匹配有效性分析

**Figure 4** 直接验证了轨迹相似度与无标签样本质量之间的因果关系。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_3K1y4KbWAx/figures/009_Figure_4.jpg]]
*Figure 4: Left: Average performance changes on labeled and unlabeled data. Center: Unlabeled data performance vs. trajectory matching score using true training dynamics on unlabeled data. Right: Unlabeled data performance vs. trajectory matching score using pseudo training dynamics on unlabeled data*

左子图展示了有标签和无标签数据在训练过程中的平均性能变化：有标签数据性能稳步上升，而无标签数据由于缺乏真实监督，其伪通过率轨迹波动较大。这为轨迹匹配提供了信号基础。

中间子图使用**真实训练动态**（即使用无标签样本的真实答案计算通过率轨迹）进行分析：轨迹相似度高的样本（top 10%）与相似度低的样本（bottom 10%）之间的性能差距超过 **40%**，证明了通过率轨迹本身蕴含了丰富的样本质量信息。

右子图使用**伪训练动态**（即实际训练中可获取的伪标签通过率轨迹）进行分析：尽管存在伪标签噪声，高 TCS 样本的性能仍然显著优于低 TCS 样本，差距同样超过 40%。这验证了 TRAPO 在实际可操作条件下的有效性——即使无法获取真实答案，伪标签轨迹也能有效区分可靠与不可靠样本。

### 消融实验

**选择策略对比**（Table 13）：在 30% 选择比例下，TRAPO 的轨迹选择策略（ID Avg. 41.8）显著优于随机选择（40.5）、基于句子熵的选择（40.0）和基于自确定性的选择（39.8）。这表明“怎么学”比“学什么”提供了更强的样本质量信号——静态的置信度或熵指标无法捕捉模型在训练过程中的动态行为模式。

**超参数敏感性**（Figure 5, Tables 9-11）：
- **top-p 选择比例**：top-p=0.3 取得最佳综合性能（ID Avg. 41.7, OOD Avg. 53.6），但 top-p=0.1 也能获得较高成绩，表明仅需少量最可靠的样本即可获得显著收益。
- **轨迹相似度阈值 Γ**：Γ=0.5 时性能最优（ID Avg. 42.6, OOD Avg. 56.1）。过高（Γ=1.0）或过低（Γ=0.1）均导致性能下降——过高会排除过多样本，过低则纳入不可靠样本。
- **预热长度**：预热轮数设为 8 时域内平均分数最高（43.1），比默认 5 轮略有提升，表明充分的预热有助于建立稳定的轨迹数据库。

**即插即用性**（Figure 7）：TRAPO 的轨迹选择策略与多种无监督基线（Sentence-level Entropy, Token-level Entropy, TTRL）结合后，性能均优于简单的半监督组合。这证明了轨迹选择作为一个通用模块，可以灵活嵌入不同的无监督奖励设计之上。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_3K1y4KbWAx/figures/022_Figure_7.jpg]]
*Figure 7: Different unsupervised methods combined with our trajectory-based filtering approach can improve performance, compared to a naive semi-supervised method that directly combines supervised and unsupervised approaches. The experimental setup follows Table 2*

### Scaling 行为

**Figure 1（右）** 和 **Table 12** 展示了 TRAPO 的 scaling law：随着样本总量和标注比例的增加，性能持续提升。在 16K 总样本、25% 标注率下，TRAPO 达到域内平均 **45.6%**、分布外平均 **59.7%**，接近或达到完全监督性能。这一 scaling 趋势表明，TRAPO 的数据效率优势在大规模场景下依然保持。

![[assets/figures/papers/paper_list_l46_https_openreview_net_forum_id_3K1y4KbWAx/figures/002_Figure_1.jpg]]
*Figure 1: Performance overview. (Left) TRAPO surpasses fully supervised RLVR (45K samples) using just 10% (4K) annotated data. (Right) TRAPO scaling law: performance improves consistently with increasing sample sizes and varying annotation ratios. We only show the changes with a sample size at a 25% annotation rate in the figure; for other specific results, please see Table 12*

在 **DeepMath 数据集**（Table 8）上的实验进一步验证了跨数据分布的泛化性：TRAPO 在分布外测试集上超越完全监督训练（OOD Avg. 52.1 vs 49.7），表明轨迹选择策略对数据来源具有鲁棒性。

### 训练效率

**Table 7** 对比了不同数据规模下的墙钟训练时间。TRAPO 的轨迹计算和选择步骤未引入显著的额外开销——在相同数据规模下，其训练时间与简单半监督组合基本持平。这是因为轨迹相似度计算仅涉及轻量级的余弦相似度运算，且选择掩码的应用与损失计算无缝集成。

### 失败模式与局限性

1. **模型规模限制**：实验主要在 7B 参数及以下模型上验证（Qwen2.5-Math-7B, Qwen-2.5-7B, Llama-3.1-8B, DeepSeek-R1-Distill-Qwen-1.5B），更大规模模型上的有效性尚待验证。**需要手动验证**：轨迹相似度信号是否在更大模型中保持区分度。

2. **任务域限制**：TRAPO 依赖可验证奖励（答案匹配），主要验证于数学推理任务。向开放式推理（法律、医疗、创意写作）的泛化需要设计合适的伪奖励机制，轨迹选择策略在无明确对错标准的场景中是否有效仍是开放问题。

3. **伪标签噪声**：无标签样本的伪标签通过多数投票产生（Eq. 2）。在模型初期表现不佳时，多数投票可能产生系统性错误，导致伪通过率轨迹失真。预热阶段（仅用有标签数据更新）部分缓解了这一问题，但无法完全消除。

4. **轨迹积累延迟**：轨迹相似度计算依赖充足的训练轮次以积累有意义的通过率序列。在极短训练场景下（如仅 2-3 轮），轨迹信号可能不足以有效区分样本质量。Table 11 显示预热长度 2 轮时性能明显下降，印证了这一限制。

## 方法谱系与知识库定位

### 1. 问题定位：RLVR训练范式的瓶颈

TRAPO 针对的是基于可验证奖励的强化学习（RLVR）在大语言模型推理训练中的两个核心瓶颈：

**无监督RLVR的性能坍塌**：完全无监督的RLVR方法（如**TTRL** (Zuo et al., 2025)、**Self-certainty** (Zhao et al., 2025)、**Token-level Entropy** 和 **Sentence-level Entropy** (Agarwal et al., 2025)）依赖自洽性奖励（多数投票伪标签）进行训练。这类方法在训练后期会强化错误推理模式，导致性能坍塌——因为模型生成的错误答案若在采样中占多数，自洽性奖励会将其误判为正确，形成错误共识的正反馈循环。

**简单半监督组合的低效性**：将少量有标签数据的真实奖励与大量无标签数据的自洽性奖励直接混合训练（naive semi-supervised RLVR），仅带来约0.6%的边际提升。其根本原因在于，这种方法忽视了有标签与无标签数据之间的内在学习动态联系，未能有效区分无标签数据中哪些样本的推理模式是可靠的、哪些是不可靠的。

### 2. 核心因果机制：轨迹对齐

TRAPO 的核心因果调控变量是**无标签样本的通过率轨迹与有标签样本通过率轨迹的余弦相似度**（Trajectory Cosine Similarity, TCS）。其关键洞察在于：少量的有标签样本可以作为“锚点”来稳定基于一致性的无监督训练——只有当无标签样本的学习动态（通过率轨迹）与有标签样本的轨迹高度一致时，其推理模式才被视为可靠，并纳入强化学习训练。

具体而言，TRAPO 将视角从“模型学到了什么”（输出内容）转向“模型如何学习”（学习动态），通过跟踪每个样本在各训练轮次中生成回答的通过率变化序列，构建通过率轨迹 $\mathbf{T}_q^{(t)} = [P_q^{(1)}, P_q^{(2)}, \ldots, P_q^{(t)}]$。对于无标签样本，使用多数投票产生的伪标签计算伪通过率；对于有标签样本，使用真实标签计算通过率。然后计算每个无标签样本轨迹与可靠轨迹数据库平均轨迹的余弦相似度：

$$\mathrm{TCS}(\mathbf{T}_u^{(t)}, \bar{\mathbf{T}}_{\mathrm{reliable}}^{(t)}) = \hat{\mathbf{T}}_u^{(t)} \cdot \hat{\bar{\mathbf{T}}}_{\mathrm{reliable}}^{(t)}$$

TCS 能够有效区分可靠与不可靠样本：高相似度样本（top 10%）的性能显著优于低相似度样本（bottom 10%），差距超过40%（Figure 4）。

### 3. 与基线方法的关系

**相对于无监督RLVR方法**：TRAPO 不是替代无监督RLVR，而是提供了一种即插即用的样本选择策略。实验表明（Figure 7, Appendix E.3），将 TRAPO 的轨迹选择策略与多种无监督基线（Sentence-level Entropy, Token-level Entropy, TTRL）结合后，性能均优于简单的半监督组合。这意味着 TRAPO 的选择机制可以增强现有无监督方法的训练稳定性和效果。

**相对于有监督RLVR（Fully Supervised GRPO, Shao et al., 2024）**：TRAPO 在仅使用约10%标注数据（4K有标签+12K无标签）的情况下，在所有基准上超越在全量45K有标签数据上训练的完全监督模型（ID Avg. 45.6 vs 45.5，OOD Avg. 59.7 vs 57.3），证明了半监督范式在标注效率上的显著优势。

**相对于基于置信度的选择方法**：TRAPO 的轨迹选择策略显著优于基于句子熵、自确定性或随机选择的策略。在30%选择比例下，TRAPO 的 ID Avg. 为41.8，而其他方法均不超过40.5（Table 13）。这表明，基于学习动态的轨迹相似度比基于单次推理的置信度指标更能反映无标签样本的真实可靠性。

### 4. 适用边界与局限

**模型规模限制**：当前实验主要在 Qwen2.5-Math-7B、Qwen-2.5-7B 和 Llama-3.1-8B 等7-8B参数规模的模型上验证，尚未在13B及以上规模的大语言模型上测试。更大规模模型的训练动态可能有所不同，轨迹选择策略的有效性需要进一步验证。

**任务领域限制**：TRAPO 主要用于数学推理任务，依赖可验证的二元奖励（答案匹配）。向开放式推理任务（如法律、医疗、创意写作）的泛化存在挑战，因为这类任务缺乏明确的答案匹配机制，通过率轨迹的定义需要重新设计。

**伪标签噪声**：无标签样本的伪标签通过多数投票产生。在模型训练初期，模型推理能力较弱时，多数投票可能产生大量错误伪标签，导致伪通过率轨迹不可靠，进而影响轨迹相似度计算的准确性。预热阶段（warm-up）的设计在一定程度上缓解了这一问题，但无法完全消除。

**轨迹积累的时间成本**：轨迹相似度计算依赖充足的训练轮次以积累有意义的通过率序列。在短期训练或快速迭代场景下，轨迹长度不足可能导致相似度估计不稳定。实验表明，预热轮数设为8时域内平均分数最高（43.1），比默认5轮略有提升，说明需要一定的轨迹积累周期。

### 5. 开放问题

1. **规模扩展**：半监督RLVR范式如何扩展到13B以上规模的大语言模型？更大模型的训练动态是否仍遵循类似的轨迹一致性规律？

2. **标注样本的选择策略**：何种类型的有标签样本（难度、主题分布、多样性等）最能有效引导无标签训练？当前工作使用随机采样的有标签数据，主动选择有标签样本可能进一步提升效率。

3. **跨领域泛化**：轨迹选择策略在非数学、开放式推理任务（如法律、医疗诊断、代码生成）中是否依然有效？如何定义这些领域的通过率或等价的学习动态指标？

4. **更细粒度的动态对齐**：是否可以用更细粒度的学习动态（如token级梯度对齐、注意力模式变化）替代通过率轨迹？更细粒度的信号可能提供更丰富的样本可靠性信息。

5. **理论界的实用化**：TRAPO 提供的泛化误差界（Theorem 3.1）中的常数在实际中如何估计？该理论界能否指导自动超参数选择（如top-p比例、阈值Γ、预热轮数），从而减少人工调参成本？

## 原文 PDF

![[paperPDFs/ICLR_2026/TraPO_A_Semi_Supervised_Reinforcement_Learning_Framework_for_Boosting_LLM_Reasoning.pdf]]
