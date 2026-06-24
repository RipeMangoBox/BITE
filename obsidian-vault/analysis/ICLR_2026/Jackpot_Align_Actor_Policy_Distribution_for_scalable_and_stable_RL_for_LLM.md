---
title: "Jackpot: Align Actor-Policy Distribution for scalable and stable RL for LLM"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Jackpot_Align_Actor_Policy_Distribution_for_scalable_and_stable_RL_for_LLM.pdf
openreview_forum_id: 5RATVAQGPx
aliases:
- Jackpot
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过对actor的采样分布应用具有预算约束的拒绝采样(OBRS)，根据当前策略概率与目标策略概率之比选择性保留或屏蔽token，从而直接缩小actor与策略之间的KL散度，同时通过接受率控制采样效率。"
primary_logic: "OBRS可在高接受率下将分布KL散度降低近一个数量级；通过Top-K logits联合集近似归一化常数并结合批级偏差校正，可将此修正以极低的计算开销（<3%）集成到PPO损失函数中，在保持信任区域约束的同时实现稳定且高效的off-policy训练。"
claims:
- "在极端off-policy训练中，Jackpot保持低KL散度并稳定收敛，而TIS和无对齐方法出现KL爆炸和训练崩溃。"
- "OBRS在校准实验中以≈95%的接受率将整体KL散度降低约一个数量级，证明其高效性和分布逼近能力。"
- "在128× actor-policy更新比下，Jackpot在AMC基准上提升了20%，在AIME上提升了8%（相对于off-policy基线）。"
- "消融实验表明，在BF16有延迟的训练中，完整的masking+reweighting方案相较于仅使用masking（OBRS rejection）在所有测试基准上均有显著提升，且避免了训练崩溃。"
---

# Jackpot: Align Actor-Policy Distribution for scalable and stable RL for LLM

> [!tip] 核心洞察
> OBRS可在高接受率下将分布KL散度降低近一个数量级；通过Top-K logits联合集近似归一化常数并结合批级偏差校正，可将此修正以极低的计算开销（<3%）集成到PPO损失函数中，在保持信任区域约束的同时实现稳定且高效的off-policy训练。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Jackpot：对齐Actor-Policy分布以实现可扩展且稳定的LLM强化学习 |
| 英文题名 | Jackpot: Align Actor-Policy Distribution for scalable and stable RL for LLM |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5RATVAQGPx); [Project](https://infini-ai-lab.github.io/jpt_website/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | JACKPOT |
| Dataset | GSM8K, MATH-500, AMC22 & AMC23 |

> [!tip] 效果简介
> - GSM8K 上，Mean@4 为 92.24，对比 88.04，变化 +4.20。
> - MATH-500 上，Mean@4 为 80.05，对比 71.15，变化 +8.90。
> - AMC22 & AMC23 上，Mean@4 为 53.916，对比 39.15，变化 +14.766。

## 概述

### 问题瓶颈

在大语言模型（LLM）的强化学习（RL）训练中，rollout阶段是主要的计算瓶颈。为提升训练吞吐量，常见的工程方案是增大actor与policy的更新比（即让生成轨迹的推理模型与正在优化的策略模型不同步），但这会引入严重的**分布不匹配**问题：actor的采样分布$P_{\mathrm{inf}}$与policy的目标分布$P_{\mathrm{ref}}$（或最新策略$P_{\mathrm{new}}$）之间的KL散度急剧增大，导致训练不稳定甚至崩溃。传统的截断重要性采样（TIS）方法在稳定性和性能之间存在固有权衡，无法有效缓解极端的分布偏移——Figure 1显示，在极端off-policy设置下，TIS的KL散度仍剧烈上升并伴随训练崩溃。

### 核心方法定位

**Jackpot** 提出了一套完整的分布对齐方案，核心思路是**先对齐、再修正**：

1. **最优预算拒绝采样（OBRS）掩码**：在rollout阶段，根据当前策略概率与目标策略概率之比，以概率$\min\left(1, \frac{p_{\mathrm{target}}(a)}{\lambda \cdot p_{\mathrm{inf}}(a)}\right)$选择性地保留或屏蔽token，从而直接缩小actor与policy之间的KL散度。OBRS是满足给定接受率预算下唯一最小化KL散度的拒绝规则，校准实验表明其在约95%的高接受率下可将整体KL散度降低近一个数量级（Figure 2）。

2. **高效概率估计与偏差校正**：通过取$p_{\mathrm{inf}}$和$p_{\mathrm{new}}$的Top-K logits并集近似计算OBRS的归一化常数$Z_{\mathrm{approx}}$，并利用批级经验接受率计算校正因子$\kappa$以消除系统性低估偏差，将额外计算开销控制在3%以内。

3. **稳定化的Jackpot-PPO损失**：将上述修正集成到PPO损失函数中，形成$\min(Z \cdot \max(\lambda, p_{\mathrm{ref}}/p_{\mathrm{inf}}), C_1) \cdot \min(p_{\mathrm{ref}}/p_{\mathrm{new}}, C_2) \cdot \mathcal{L}^{\mathrm{PPO}}$的重加权形式，并对整体权重应用stop-gradient，在保持信任区域约束的同时实现稳定的off-policy训练。

### 核心结论

- **稳定收敛**：在极端off-policy训练（如用Qwen3-1.7B做rollout训练Qwen3-8B）中，Jackpot维持低KL散度并稳定收敛，而无对齐方法和TIS均出现KL爆炸和训练崩溃（Figure 1）。

- **显著性能提升**：在128× actor-policy更新比下，Jackpot在AMC基准上提升20%，在AIME上提升8%（相对于off-policy基线）；在64×更新比下，GSM8K提升4.2分，MATH-500提升8.9分，AMC22&23提升14.8分（Table 3）。

- **组件有效性**：消融实验证实，完整的masking+reweighting方案显著优于仅使用OBRS masking，且在BF16有更新延迟的设置下避免了训练崩溃（Table 6）；OBRS masking单独应用即可纠正因FP8量化不稳定性导致的训练崩溃（Table 5）。

- **超参数鲁棒性**：拒绝阈值$\lambda=1.0$为稳健默认值，在0.8-1.2范围内性能变化不大；$C_1$在2-10范围内均表现稳定；Top-K=20可在极小开销下提供准确的归一化常数估计。

## 背景与动机

### 大语言模型强化学习的效率瓶颈

将强化学习（RL）应用于大语言模型（LLM）的推理能力训练已成为提升模型数学、编程等复杂任务表现的重要范式。典型的RL训练流程交替执行两个阶段：**rollout阶段**由actor模型采样生成完整响应序列，**训练阶段**则利用这些序列计算策略梯度并更新模型参数。然而，这一范式面临严峻的效率挑战——rollout阶段的自回归生成过程消耗大量计算资源，其开销通常远超参数更新本身。

为提升训练吞吐，一种自然的工程策略是**增大actor与policy的更新比**：让actor执行多轮rollout后才进行一次策略更新，或采用异步架构让rollout与训练解耦。但这一优化引入了一个根本性问题：**actor的采样分布与当前策略分布之间出现显著偏差**。当使用过时的actor分布采样的数据来更新当前策略时，标准的重要性采样（Importance Sampling）权重会因分布不匹配而产生高方差梯度估计，导致训练不稳定乃至完全崩溃。

### 现有方法的局限性：截断重要性采样的固有权衡

针对off-policy训练中的分布偏移问题，**截断重要性采样（Truncated Importance Sampling, TIS）** 是应用最广泛的修正手段（源自Impala, Espeholt et al., ICML 2018）。其核心思想是将重要性权重 $p_{\text{ref}}(x) / p_{\text{inf}}(x)$ 截断至一个预设上限 $C$，以抑制极端权重值：

$$\mathcal{L}^{\mathrm{PPO}}(\theta) = \mathbb{E}_{x \sim P_{\mathrm{inf}}} \Big[ \min\big( \frac{p_{\mathrm{ref}}(x)}{p_{\mathrm{inf}}(x)}, C \big) \min\big( r_{\theta}(x) \hat{A}(x), \mathrm{clip}(r_{\theta}(x), 1-\epsilon, 1+\epsilon) \hat{A}(x) \big) \Big]$$

然而，TIS方法在**稳定性与性能之间存在固有权衡**：较小的截断阈值 $C$ 可以有效抑制方差但会引入系统性偏差，损害策略优化的准确性；较大的 $C$ 保留更多有效信息但难以控制极端权重带来的梯度爆炸风险。当分布偏移严重时——例如actor与策略模型架构不同、或更新比高达128×——TIS无法有效遏制KL散度的持续增长，训练仍会走向崩溃（见Figure 1中TIS的KL曲线和性能塌陷）。

### 核心挑战：从被动修正到主动对齐

上述困境揭示了一个更深层的问题：**现有方法仅在损失函数层面被动修正分布不匹配，而未在数据生成源头主动缩小分布差距**。当actor的采样分布 $P_{\text{inf}}$ 与目标策略分布 $P_{\text{target}}$ 之间的KL散度过大时，任何基于重要性采样的后验修正都将面临方差-偏差的不可调和矛盾。

Jackpot的动机正是打破这一僵局：**能否在rollout阶段以极低的额外开销主动调整actor的采样分布，使其逼近目标策略分布，从而从根源上缓解off-policy训练的稳定性问题？** 这一思路要求设计一种轻量级的分布对齐机制，既能有效缩小KL散度，又不显著牺牲采样效率（接受率），同时还需将修正无缝集成到标准PPO优化框架中。

## 核心创新

### 问题瓶颈：Actor-Policy分布偏移导致的训练崩溃

在LLM的强化学习训练中，rollout阶段（actor采样轨迹）通常消耗大量计算资源。为提高效率，实践中常允许actor与待更新的策略（policy）使用不同的分布——例如actor更新滞后、或使用更小的模型进行推理。然而，这种分布不匹配会引入严重的训练不稳定：当actor的采样分布 $P_{\mathrm{inf}}$ 与目标策略分布显著偏离时，PPO的信任区域约束被破坏，训练可能直接崩溃。

传统的截断重要性采样（TIS, **Impala** (Espeholt et al., ICML 2018)）通过权重 $\min(p_{\mathrm{ref}}/p_{\mathrm{inf}}, C)$ 来修正分布不匹配，但其在稳定性和性能之间存在固有权衡——截断阈值 $C$ 过小会限制有效样本的利用，过大则无法抑制高方差梯度。当分布偏移严重时（如用Qwen3-1.7B的rollout训练Qwen3-8B），TIS的KL散度仍会剧烈增长并最终崩溃（Figure 1）。

### 核心因果机制：最优预算拒绝采样（OBRS）

Jackpot的核心创新在于**在采样阶段直接修正actor的分布**，而非仅在损失函数中事后补偿。具体而言，采用最优预算拒绝采样（Optimal Budgeted Rejection Sampling, OBRS）：对actor采样出的每个token $a$，以概率

$$\alpha_C(a) = \min\left(1, \frac{p_{\mathrm{target}}(a)}{\lambda \cdot p_{\mathrm{inf}}(a)}\right)$$

决定是否保留该token。被拒绝的token不参与后续的损失计算和梯度回传。

这一机制的因果效应体现在两个层面：

1. **分布KL散度的直接压缩**：OBRS是满足给定接受率预算下唯一最小化KL散度的拒绝规则。校准实验（Figure 2）表明，在以约95%的高接受率运行时，OBRS可将actor与目标策略之间的整体KL散度降低近一个数量级。

2. **信任区域约束的隐式维护**：通过拒绝那些在目标策略下概率远低于actor采样概率的token，OBRS使实际参与更新的样本分布 $P_{\mathrm{OBRS}}$ 在KL意义上严格逼近目标策略，从而在PPO的信任区域内运作。

### 方法谱系与知识库定位

| 方法 | 分布修正策略 | 修正阶段 | 核心局限 |
|------|-------------|---------|---------|
| **On-policy PPO/GRPO** | 无（actor与策略同步） | — | 计算开销大，无法利用异步/异构rollout |
| **Off-policy (no correction)** | 无 | — | 分布偏移导致训练崩溃 |
| **TIS** (Espeholt et al., ICML 2018) | 损失重加权：$\min(p_{\mathrm{ref}}/p_{\mathrm{inf}}, C)$ | 损失计算 | 稳定性-性能权衡，严重偏移时失效 |
| **TIS with Adjustment** | 用detached新策略logits替代 $p_{\mathrm{ref}}$ 作为重要性比分母 | 损失计算 | 仍仅事后修正，不改变采样分布 |
| **Jackpot (本文)** | OBRS拒绝采样 + 损失重加权 | 采样阶段 + 损失计算 | 需额外top-k logits收集（<3%开销） |

### 三个关键Changed Slots

**Changed Slot 1：rollout采样分布调整**

- **Baseline**：直接使用actor原始分布 $P_{\mathrm{inf}}$ 生成轨迹，不做任何干预。
- **Jackpot**：在rollout过程中应用OBRS掩码——每个token以 $\min(1, p_{\mathrm{target}}(a)/(\lambda \cdot p_{\mathrm{inf}}(a)))$ 的概率被接受，被拒绝的token屏蔽出损失和梯度计算。$\lambda$ 为缩放因子，控制接受率与KL压缩程度的权衡（$\lambda=1.0$ 为稳健默认值，消融实验表明在0.8–1.2范围内性能平坦）。

**Changed Slot 2：归一化常数估计**

- **Baseline**：计算整个词表（通常>100k tokens）的归一化常数 $Z$，内存和计算开销极大，实际不可行。
- **Jackpot**：取 $P_{\mathrm{inf}}$ 和 $P_{\mathrm{new}}$ 的top-k token（$k=20$）的并集 $\mathcal{V}_k$ 近似计算 $Z_{\mathrm{approx}}$，并利用批级经验接受率 $\hat{\bar{\alpha}}$ 计算校准因子 $\kappa = \frac{\hat{\bar{\alpha}}}{\frac{1}{B}\sum_{i=1}^{B} Z_{\mathrm{approx}}^{(i)}}$ 以消除top-k近似的系统性低估偏差。此方案仅增加不到3%的计算开销。

**Changed Slot 3：PPO损失重加权**

- **Baseline**：标准PPO-clip损失，或TIS权重 $\min(p_{\mathrm{ref}}/p_{\mathrm{inf}}, C) \cdot \mathcal{L}^{\mathrm{PPO}}$。
- **Jackpot**：稳定化的Jackpot-PPO损失，针对不同场景有两种形式：
  - **低延迟场景**（目标为 $p_{\mathrm{ref}}$）：$\min(Z \cdot \max(\lambda, p_{\mathrm{ref}}/p_{\mathrm{inf}}), C) \cdot f(x)$
  - **高延迟场景**（目标为最新策略 $p_{\mathrm{new}}$）：$\min(Z \cdot \max(\lambda, p_{\mathrm{new}}/p_{\mathrm{inf}}), C_1) \cdot \min(p_{\mathrm{ref}}/p_{\mathrm{new}}, C_2) \cdot f(x)$

其中 $f(x) = \min(r_\theta(x)\hat{A}(x), \mathrm{clip}(r_\theta(x), 1-\epsilon, 1+\epsilon)\hat{A}(x))$ 为标准PPO截断项。整体权重应用stop-gradient，避免梯度通过重要性权重传播导致的不稳定。$C_1 \in [2, 10]$ 范围内性能不敏感。

### 决定性证据

1. **极端off-policy稳定性**（Figure 1）：用Qwen3-1.7B的rollout训练Qwen3-8B，Jackpot（黄色）维持低KL散度并稳定收敛至接近on-policy性能；无对齐方法（粉色）在约4000-6000步KL爆炸并崩溃；TIS（绿色）KL散度持续增长且性能显著落后。

2. **OBRS校准实验**（Figure 2）：在初始KL散度较大的情况下，OBRS仍保持约95%的接受率，并将整体KL散度降低约一个数量级，验证了其高效性和分布逼近能力。

3. **大规模off-policy收益**（Table 3-4）：在128× actor-policy更新比下，Jackpot在AMC基准上提升约20%，在AIME上提升约8%（相对于off-policy基线）；在64×设置下，GSM8K从88.04提升至92.24，MATH-500从71.15提升至80.05。

4. **消融实验**（Table 6）：在BF16有更新延迟的训练中，完整的masking+reweighting方案（完整Jackpot）相比仅使用masking（OBRS rejection alone）在所有测试基准上均有显著提升，且避免了训练崩溃——例如AIME24从19.167提升至25.625，AMC从49.699提升至63.855。

## 整体框架

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/006_Figure_3.jpg]]
*Figure 3: Illustration of JACKPOT Pipeline focusing on Optimal Budgeted Rejection Sampling (OBRS) and Reweighting Procedures*

Jackpot 的核心设计思路是通过在 rollout 阶段主动调整 actor 的采样分布，从源头缩小其与目标策略（policy）之间的概率分布差距，从而在保持高采样效率的前提下实现稳定且可扩展的 off-policy 训练。整个 pipeline 由三个关键模块串联构成，如图 Figure 3 所示。

### 模块关系与数据流

**Phase 1：OBRS Token 掩码（Rollout 阶段）**

在标准 RL 训练中，actor 模型 $P_{\mathrm{inf}}$ 生成响应序列时，每个 token 的采样完全由其原始输出分布决定。Jackpot 在此阶段引入最优预算拒绝采样（Optimal Budgeted Rejection Sampling, OBRS）：对 actor 采样出的每个 token $a$，以概率

$$\alpha_C(a) = \min\Bigl( 1, \frac{p_{\mathrm{target}}(a)}{\lambda \cdot p_{\mathrm{inf}}(a)} \Bigr)$$

决定接受或屏蔽该 token。其中 $p_{\mathrm{target}}$ 为目标策略分布（通常为参考策略 $p_{\mathrm{ref}}$ 或最新策略 $p_{\mathrm{new}}$），$\lambda$ 为控制接受率与 KL 散度权衡的缩放因子。被拒绝的 token 不参与后续损失计算和梯度回传。这一操作将 actor 的有效采样分布从 $P_{\mathrm{inf}}$ 调整为 $P_{OBRS}$：

$$P_{OBRS}(x) = \frac{\min(p_{\mathrm{inf}}(x), \frac{p_{\mathrm{target}}(x)}{\lambda})}{\sum_{x'} \min(p_{\mathrm{inf}}(x'), \frac{p_{\mathrm{target}}(x')}{\lambda})}$$

OBRS 在理论上被证明是给定接受预算下唯一最小化与目标分布 KL 散度的拒绝规则，且经 OBRS 修正后的分布 $P_{OBRS}$ 在 KL 散度意义上严格更接近目标分布。校准实验（Figure 2）表明，即使初始 KL 散度很大，接受率仍可维持在约 95%，而整体 KL 散度降低约一个数量级。

**Phase 2：Top-K Logit 收集与偏差校正**

为计算 OBRS 所需的归一化常数 $Z$，Jackpot 不遍历整个词表（计算和内存开销极大），而是利用 actor 前向传播时自然产生的 logits，收集 $P_{\mathrm{inf}}$ 和 $P_{\theta_{\mathrm{new}}}$ 各自的 top-k token，取其并集构成近似词表：

$$\mathcal{V}_k = \mathrm{top\text{-}k}(p_{\mathrm{inf}}) \cup \mathrm{top\text{-}k}(p_{\theta_{\mathrm{new}}})$$

基于 $\mathcal{V}_k$ 计算近似归一化常数 $Z_{\mathrm{approx}}$。由于 top-k 近似会系统性低估真实 $Z$ 值，Jackpot 进一步在训练 batch 内计算批级偏差校正因子 $\kappa$：

$$\kappa = \frac{\hat{\bar{\alpha}}}{\frac{1}{B} \sum_{i=1}^{B} Z_{\mathrm{approx}}^{(i)}}$$

其中 $\hat{\bar{\alpha}}$ 为 batch 内的经验接受率，$B$ 为 batch 大小。最终使用的校正归一化常数为 $\kappa \cdot Z_{\mathrm{approx}}$。消融实验表明，取 $k=20$ 即可在仅增加不到 3% 计算开销的前提下提供足够准确的 $Z$ 估计。

**Phase 3：Jackpot 权重计算与 PPO 损失重加权**

在 PPO 更新阶段，Jackpot 利用校正后的归一化常数和策略概率比计算最终的 Jackpot 重要性权重，并将其（经 stop-gradient 处理）乘到标准 PPO 截断损失上。针对不同程度的分布偏移，Jackpot 提供两种损失变体：

- **标准变体**（以 $p_{\mathrm{ref}}$ 为目标策略）：

$$\mathcal{L}_{ours}^{\mathrm{PPO}}(\theta) = \mathbb{E}_{x \sim P_{\mathrm{inf}}} \Big[ \min( Z \cdot \max(\lambda, \frac{p_{\mathrm{ref}}(x)}{p_{\mathrm{inf}}(x)}), C ) \cdot f(x) \Big]$$

- **高陈旧度变体**（以 $p_{\mathrm{new}}$ 为目标策略，适用于 rollout 与训练策略严重不同步的场景）：

$$\mathcal{L}_{ours}^{\mathrm{PPO}}(\theta) = \Big[ \min( Z \cdot \max(\lambda, \frac{p_{\mathrm{new}}(x)}{p_{\mathrm{inf}}(x)}), C_1) \cdot \min(\frac{p_{\mathrm{ref}}}{p_{\mathrm{new}}}, C_2) \cdot f(x) \Big]$$

其中 $f(x)$ 为标准 PPO 截断项，$C$、$C_1$、$C_2$ 为截断阈值。该设计同时兼顾了重要性采样比的修正和 PPO 信任区域约束，使得训练在高度 off-policy 的条件下仍能保持稳定。

### 关键设计优势

整个 pipeline 无需额外采样轨迹，无需额外的 log-probability 计算，也无需修改 vLLM 等推理引擎。OBRS 掩码操作在 rollout 阶段以极低成本完成，top-k 收集和偏差校正均复用已有前向计算结果，额外计算开销控制在总计算量的 3% 以内。

## 核心模块与公式推导

### 3.1 最优预算拒绝采样 (OBRS)

Jackpot 的核心机制是在 roll-out 阶段对 actor 的采样分布施加**最优预算拒绝采样 (Optimal Budgeted Rejection Sampling, OBRS)**，以直接缩小 actor 分布 $P_{\mathrm{inf}}$ 与目标策略分布之间的 KL 散度。

给定从推理分布 $p_{\mathrm{inf}}$ 中采样得到的 token $a$，其被接受的概率为：

$$\alpha_C(a) = \min\left(1, \frac{p_{\mathrm{target}}(a)}{\lambda \cdot p_{\mathrm{inf}}(a)}\right)$$

其中 $\lambda$ 是缩放因子，用于控制接受率与分布对齐程度之间的权衡。被拒绝的 token 不参与后续的损失计算和梯度回传。在所有满足给定接受预算的拒绝规则中，该缩放接受规则是唯一能使被保留分布与目标分布之间 KL 散度最小化的规则（Verine et al., 2024）。

经过 OBRS 掩码后，token 的实际采样分布变为：

$$P_{\mathrm{OBRS}} = \frac{\min\left(p_{\mathrm{inf}}(x), \frac{p_{\mathrm{target}}(x)}{\lambda}\right)}{\sum_{x'} \min\left(p_{\mathrm{inf}}(x'), \frac{p_{\mathrm{target}}(x')}{\lambda}\right)}$$

其中分母 $Z = \sum_{x'} \min(p_{\mathrm{inf}}(x'), p_{\mathrm{target}}(x')/\lambda)$ 为归一化常数。理论保证：对于任意 $C > 0$，$P_{\mathrm{OBRS}}$ 与目标分布之间的 KL 散度严格小于原始 $p_{\mathrm{inf}}$ 与目标分布之间的 KL 散度。

校准实验（Figure 2）验证了 OBRS 的实际效果：即使初始 KL 散度很大，接受率仍保持在约 95%，整体 KL 散度降低约一个数量级。

### 3.2 Jackpot-PPO 损失函数

#### 3.2.1 基础形式：对齐至参考策略 $p_{\mathrm{ref}}$

在标准 off-policy 设置中，目标是将推理分布对齐至参考策略 $p_{\mathrm{ref}}$。Jackpot 在标准 PPO 截断目标 $f(x) = \min(r_{\theta}(x) \hat{A}(x), \mathrm{clip}(r_{\theta}(x), 1-\epsilon, 1+\epsilon) \hat{A}(x))$ 的基础上，引入基于 OBRS 的重要性权重：

$$\mathcal{L}_{\mathrm{ours}}^{\mathrm{PPO}}(\theta) = \mathbb{E}_{x \sim P_{\mathrm{inf}}} \Big[ \min\left( Z \cdot \max\left(\lambda, \frac{p_{\mathrm{ref}}(x)}{p_{\mathrm{inf}}(x)}\right), C \right) \cdot f(x) \Big]$$

其中：
- $Z$ 为 OBRS 的归一化常数，将经验分布校正为目标分布；
- $\max(\lambda, p_{\mathrm{ref}}/p_{\mathrm{inf}})$ 确保权重下界为 $\lambda$，避免因 $p_{\mathrm{ref}} \ll p_{\mathrm{inf}}$ 导致权重过小而浪费样本；
- $C$ 为截断阈值，控制单一样本对更新的最大影响，维持信任区域约束。

#### 3.2.2 高延迟变体：对齐至最新策略 $p_{\mathrm{new}}$

当 roll-out 模型与训练模型之间的更新延迟极高时，将目标策略替换为最新更新后的策略 $p_{\mathrm{new}}$ 更为有效。此时损失函数引入双层截断：

$$\mathcal{L}_{\mathrm{ours}}^{\mathrm{PPO}}(\theta) = \Big[ \min\left( Z \cdot \max\left(\lambda, \frac{p_{\mathrm{new}}(x)}{p_{\mathrm{inf}}(x)}\right), C_1 \right) \cdot \min\left(\frac{p_{\mathrm{ref}}}{p_{\mathrm{new}}}, C_2 \right) \cdot f(x) \Big]$$

- 第一层权重 $Z \cdot \max(\lambda, p_{\mathrm{new}}/p_{\mathrm{inf}})$ 将推理分布 $p_{\mathrm{inf}}$ 校正至最新策略 $p_{\mathrm{new}}$；
- 第二层权重 $\min(p_{\mathrm{ref}}/p_{\mathrm{new}}, C_2)$ 为标准 PPO 似然比，约束更新不偏离参考策略过远；
- 整体权重施加 stop-gradient，防止权重计算本身引入梯度偏差。

### 3.3 高效归一化常数估计

直接计算归一化常数 $Z$ 需遍历整个词表（通常 > 150k tokens），内存和计算开销极大。Jackpot 采用两阶段近似策略，将额外计算开销控制在 3% 以内。

#### 3.3.1 Top-K 并集近似

取推理分布 $p_{\mathrm{inf}}$ 和当前策略 $p_{\theta_{\mathrm{new}}}$ 的 top-k token 的并集构建近似词表：

$$\mathcal{V}_k = \mathrm{top\text{-}k}(p_{\mathrm{inf}}) \cup \mathrm{top\text{-}k}(p_{\theta_{\mathrm{new}}})$$

在该并集上计算近似归一化常数：

$$Z_{\mathrm{approx}} = \sum_{x \in \mathcal{V}_k} \min\left(p_{\mathrm{inf}}(x), \frac{p_{\mathrm{new}}(x)}{\lambda}\right)$$

消融实验（Table 9）表明，$k=20$ 即可提供足够准确的 $Z$ 估计，更大的 $k$（如 40）无进一步明显收益。

#### 3.3.2 批级偏差校正

Top-k 近似会系统性地低估真实的 $Z$。Jackpot 利用训练 batch 内的经验接受率 $\hat{\bar{\alpha}}$ 计算校正因子 $\kappa$：

$$\kappa = \frac{\hat{\bar{\alpha}}}{\frac{1}{B} \sum_{i=1}^{B} Z_{\mathrm{approx}}^{(i)}}$$

其中 $\hat{\bar{\alpha}}$ 为 batch 内 token 的实际接受比例，$B$ 为 batch 大小。最终使用的校正归一化常数为 $Z = \kappa \cdot Z_{\mathrm{approx}}$。该校正无需额外前向传播，仅利用 OBRS 阶段已产生的接受/拒绝信号即可完成。

### 3.4 算法流程

完整的 Jackpot 算法（Algorithm 1）分为两个阶段：

**阶段一（Roll-out 与 OBRS 掩码）**：actor 使用推理分布 $p_{\mathrm{inf}}$ 逐 token 生成响应；对每个 token 计算接受概率 $\alpha_C(a)$ 并执行拒绝采样；同时从 actor 的前向传播中收集 top-k log-probabilities，用于后续 $Z_{\mathrm{approx}}$ 的计算。

**阶段二（PPO 更新与重加权）**：在训练 batch 上计算 $Z_{\mathrm{approx}}$ 和校正因子 $\kappa$；对每个 token 计算 Jackpot 重要性权重 $w_{\mathrm{OBRS}} = Z \cdot \max(\lambda, p_{\mathrm{new}}/p_{\mathrm{inf}})$；将 stop-gradient 后的权重乘以标准 PPO 截断损失，完成梯度更新。

## 实验与分析

### 核心瓶颈与因果验证

LLM强化学习训练中，rollout阶段的计算开销使得提高actor-policy更新比（即多次策略更新对应一次rollout）成为提升效率的关键手段。然而，当actor的采样分布与当前策略分布出现偏离时，传统的截断重要性采样（TIS）方法面临稳定性与性能的固有权衡——截断阈值过小会引入偏差，过大则无法有效抑制分布偏移带来的方差爆炸。**JACKPOT**通过最优预算拒绝采样（OBRS）直接调整actor的采样分布，从根源上缩小分布KL散度，而非仅在损失函数层面进行事后修正。

**Figure 1** 展示了这一因果机制的决定性证据：在极端off-policy场景下（Qwen3-1.7B-Base rollout训练Qwen3-8B-Base），无对齐方法（pink）的KL散度剧烈飙升并迅速崩溃；TIS方法（green）虽然延迟了崩溃，但KL散度仍持续增长且性能远逊于on-policy基线（purple）；而JACKPOT（yellow）将KL散度维持在低位，并稳定收敛至接近on-policy的性能水平。这直接验证了分布对齐是稳定训练的必要条件，而OBRS是实现这一对齐的有效因果杠杆。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/002_Figure_1.jpg]]
*Figure 1: RL training requires actor-policy maintaining strong probability distribution alignment. When actor and policy aren’t aligned, they will result in training collapse. Here we show training setting use a Qwen3-1.7B-Base model training rollout to train a Qwen3-8B-Base model policy. Without any alignment procedures, training collapses (pink). Prior method TIS (green) also show significant gap towards Qwen3-8B-Base on-policy baseline (purple), while collapsing, using TIS sees KL divergence also violently increasing. Our proposed method, Jackpot (yellow) maintains small KL divergence between actor and policy model probability distribution, while showing stable and competitive training convergence...*

### 主实验结果

**Table 1** 和 **Table 3** 汇总了JACKPOT在多个数学推理基准上的主实验结果。在Qwen3-4B-Base模型上，当rollout:train batch ratio为2048:32（即64×更新比）时，JACKPOT相较于Off Policy基线在GSM8K上提升**+4.20**（92.24 vs 88.04），在MATH-500上提升**+8.90**（80.05 vs 71.15），在AMC22&23上提升**+14.77**（53.92 vs 39.15）。当更新比进一步提升至128×（4096:32）时，性能优势进一步扩大：GSM8K提升**+12.30**（92.00 vs 79.70），MATH-500提升**+19.80**（80.00 vs 60.20），AMC22&23提升**+18.20**（51.20 vs 33.00）。在更具挑战性的竞赛级基准上（**Table 4**），JACKPOT在AMC12 2024上取得**+20.56**的提升（50.00 vs 29.44），在AIME24上取得**+6.67**的提升（20.625 vs 13.958）。这些结果表明JACKPOT在多种更新比和模型规模下均能稳定地大幅超越off-policy基线。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/012_Table_3.jpg]]
*Table 3: Evaluation scores across benchmarks (GSM8K, MATH-500, AMC22 & AMC23)*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/013_Table_4.jpg]]
*Table 4: Evaluation scores across benchmarks (AMC12 2024, AIME24, AIME25)*

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/007_Table_1.jpg]]
*Table 1: Evaluation scores across benchmarks. TIS + Adjustment is explained in Section B.1*

值得注意的是，TIS with Adjustment基线（使用detached新策略logits作为重要性比分母）本身已是一个强基线，但JACKPOT在此基础上仍有显著提升，说明OBRS分布调整提供了独立于损失重加权的增益。

### 关键消融分析

**Masking与Reweighting的协同效应。** **Table 6** 展示了在BF16有更新延迟的设置下，仅使用OBRS masking（即拒绝采样）与完整JACKPOT（masking + reweighting）的对比。Masking-only方案在训练后期出现崩溃（best before crash），而完整方案不仅避免了崩溃，还在所有基准上取得大幅领先：AIME24从19.167提升至**25.625**，AMC从49.699提升至**63.855**，MATH500从78.750提升至**83.800**。这表明损失重加权对于在高方差off-policy场景下维持训练稳定性至关重要。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/015_Table_6.jpg]]
*Table 6: BF16 training with rollout staleness (64/2048). Best scores before crash for masking-only*

**拒绝阈值λ的鲁棒性。** **Table 8** 显示，拒绝阈值λ（文中记为c）在0.8–1.2范围内对最终性能影响不大，尤其在MATH500和GSM8K上表现几乎平坦。λ=1.0被验证为稳健的默认值，无需针对不同任务进行精细调参。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/017_Table_8.jpg]]
*Table 8: Effect of rejection threshold c on benchmark performance. Experiment Setup: Model: Qwen3-4B-Base (target) / Qwen3-1.7B-Base (rollout); Generation length limit: 8K; Training examples: 9K. Numbers are pass@1 accuracy*

**Top-K近似的效率-精度权衡。** **Table 9** 表明，k=20可在仅增加<3%计算开销的情况下提供足够准确的归一化常数Z估计。将k增大至40并未带来进一步性能提升，验证了Top-K并集近似的高效性。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/018_Table_9.jpg]]
*Table 9: Effect of top-k on benchmark performance. Numbers are pass@1 accuracy*

**C₁超参数的不敏感性。** **Table 7** 显示，C₁在2–10范围内均表现稳定，对最终性能不敏感，进一步降低了方法的使用门槛。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/016_Table_7.jpg]]
*Table 7: Effect of $C _ { 1 }$ on benchmark performance. Experiment Setup: Model: Qwen3-4B-Base, ${ \bf$ C } 2 = { } 3.0, threshold c { = } 1 . 0 , response limit: 8k, mini-batch/train-batch: 64/2048, PPO clip: 0.4/0.7, 100k examples. Numbers are pass@1 accuracy*

### 极端场景下的鲁棒性

**FP8量化不稳定性恢复。** **Table 5** 和 **Figure 4(b)** 展示了JACKPOT在FP8 on-policy训练中的独特价值：由于KV缓存的FP8量化引入数值不稳定性，vanilla基线出现训练崩溃；而仅应用OBRS masking（无损失重加权）即可恢复正常训练，证明OBRS对分布对齐的独立贡献——即便在名义上的on-policy设置中，量化误差引入的分布偏移也足以破坏训练。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/014_Table_5.jpg]]
*Table 5: FP8 on-policy training (no staleness). Best scores before crash for the vanilla baseline*

**双模型架构不匹配。** **Figure 4(c)** 和 **Table 2** 展示了最极端的off-policy场景：使用Qwen2.5-1.5B-MATH进行rollout，训练Qwen2.5-3B-Base。在这种架构和规模均不匹配的设置下，Vanilla GRPO和TIS均出现性能崩溃，而JACKPOT不仅保持了稳定训练，还在MATH-500上提升了12%的准确率。这验证了OBRS从“完全异质的输出响应中过滤有用token”的假设——即使rollout模型与训练模型差异巨大，OBRS仍能识别并保留对策略学习有价值的token。

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/008_Table_2.jpg]]
*Table 2: AMC22&23 results of two model training using various methods across the training steps. Mean@k/Pass@k*

### 失败模式与局限性

尽管JACKPOT在多种off-policy场景下展现了显著的稳定性和性能优势，但需注意以下几点：（1）在极端架构不匹配的双模型训练中，JACKPOT虽能“击败基线并展现早期希望”，但距离on-policy性能仍有差距，表明分布对齐并非万能解药；（2）当前实验均在数学推理领域进行，方法在其他任务类型（如对话、代码生成）上的泛化性尚待验证；（3）OBRS的接受率虽在高初始KL下仍保持≈95%，但接受率与分布对齐程度之间的精确理论关系及其对最终策略质量的影响机制仍需进一步研究。

### 补充图表

![[assets/figures/papers/paper_list_l4_https_openreview_net_forum_id_5RATVAQGPx/figures/005_Figure_2.jpg]]
*Figure 2: OBRS calibration results across three views: (a) per-token probability-ratio clipping pulls the model distribution toward the target, (b) acceptance remains high (≈ 95%) even at large initial $\mathrm { K L }$ , , and (c) overall KL is reduced by roughly an order of magnitude*

## 方法谱系与知识库定位

### 问题定位：LLM强化学习的分布偏移瓶颈

在大语言模型（LLM）的强化学习（RL）训练中，rollout阶段是主要的计算瓶颈。为提升训练吞吐量，工程实践中常采用异步训练、大batch推理或分离式rollout-训练架构，但这些策略不可避免地导致actor（用于采样的模型）与policy（被更新的模型）之间的概率分布出现偏移。当这种分布不匹配得不到有效纠正时，PPO训练会面临严重的稳定性问题，甚至出现KL散度爆炸和训练崩溃。

传统上，截断重要性采样（Truncated Importance Sampling, TIS）是处理off-policy数据分布校正的标准方法，源自Impala框架（**Espeholt et al., ICML 2018**）。其核心思想是将PPO损失乘以截断的重要性权重 $\min(p_{\mathrm{ref}}/p_{\mathrm{inf}}, C)$，以降低来自过时分布样本的贡献。然而，TIS在稳定性和性能之间存在固有权衡：较小的截断阈值 $C$ 能增强稳定性，但会丢弃大量有效信息；较大的 $C$ 保留了更多信息，但无法有效抑制分布偏移带来的方差，在高偏移场景下仍会导致训练崩溃。如Figure 1所示，在极端off-policy设置（Qwen3-1.7B rollout训练Qwen3-8B）中，TIS（绿色曲线）的KL散度持续上升，最终仍出现训练崩溃，与on-policy基线（紫色曲线）之间存在显著差距。

### Jackpot的方法论创新

Jackpot的核心洞察是：与其在损失函数层面被动地修正分布不匹配（如TIS），不如在采样阶段主动调整actor的输出分布，使其逼近目标策略分布，从而从根源上缩小分布间隙。该方法包含三个紧密耦合的组件：

**1. 最优预算拒绝采样（OBRS）掩码机制**

Jackpot在rollout阶段对actor的采样分布应用OBRS：对于每个生成的token $a$，以概率 $\alpha_C(a) = \min(1, p_{\mathrm{target}}(a)/(\lambda \cdot p_{\mathrm{inf}}(a)))$ 接受该token，被拒绝的token不参与后续的损失计算和梯度回传。这里的 $\lambda$ 是控制接受率与KL散度权衡的缩放因子。OBRS的理论保证是：在所有满足给定接受预算的拒绝规则中，该规则是唯一最小化接受后分布与目标分布之间KL散度的方案。校准实验（Figure 2）证实，即使初始KL散度很大，OBRS仍能维持约95%的高接受率，并将整体KL散度降低约一个数量级。

**2. 高效归一化常数估计**

OBRS修正后的分布需要计算归一化常数 $Z = \sum_{x'} \min(p_{\mathrm{inf}}(x'), p_{\mathrm{target}}(x')/\lambda)$，对整个词表求和的计算和内存开销极大。Jackpot采用Top-K logits联合集近似：取 $p_{\mathrm{inf}}$ 和 $p_{\mathrm{new}}$ 各自top-k token的并集 $\mathcal{V}_k$ 作为近似词表，仅在该子集上计算 $Z_{\mathrm{approx}}$。为消除top-k近似的系统性低估偏差，进一步引入批级校正因子 $\kappa = \hat{\bar{\alpha}} / (\frac{1}{B}\sum_{i=1}^{B} Z_{\mathrm{approx}}^{(i)})$，其中 $\hat{\bar{\alpha}}$ 为批次内经验接受率。实验表明，$k=20$ 即可在仅增加不到3%计算开销的情况下提供足够准确的 $Z$ 估计。

**3. 稳定化的Jackpot-PPO损失**

将OBRS修正后的分布代入PPO目标函数，得到Jackpot-PPO损失：

$$\mathcal{L}_{\mathrm{ours}}^{\mathrm{PPO}}(\theta) = \mathbb{E}_{x \sim P_{\mathrm{inf}}} \left[ \min\left( Z \cdot \max\left(\lambda, \frac{p_{\mathrm{ref}}(x)}{p_{\mathrm{inf}}(x)}\right), C_1 \right) \cdot \min\left( \frac{p_{\mathrm{ref}}}{p_{\mathrm{new}}}, C_2 \right) \cdot f(x) \right]$$

其中 $f(x)$ 为标准PPO截断项。该损失函数的设计体现了三个关键考量：(1) $Z \cdot \max(\lambda, p_{\mathrm{ref}}/p_{\mathrm{inf}})$ 同时编码了OBRS的分布调整效应和重要性采样修正；(2) 双层截断（$C_1$ 和 $C_2$）在高延迟场景下提供了额外的稳定性保障；(3) 整体权重应用stop-gradient，避免梯度通过重要性权重回传导致的不稳定。

### 与基线方法的关系

**相对于On-policy PPO/GRPO**：Jackpot并非旨在超越on-policy训练的性能上限，而是追求在off-policy条件下逼近on-policy的表现，同时大幅提升训练效率。实验表明，在64×和128×的actor-policy更新比下，Jackpot的训练曲线能稳定收敛并接近on-policy趋势。

**相对于TIS及其变体**：论文实现了一个强TIS基线（TIS with Adjustment），使用detached新策略logits替代 $p_{\mathrm{ref}}$ 作为重要性比分母，以应对高度过时的情况。Jackpot在此基础上仅额外引入OBRS分布调整，因此在可比条件下，性能提升可直接归因于OBRS的分布对齐效应。消融实验（Table 6）进一步表明，完整的masking+reweighting方案相较于仅使用masking（即OBRS rejection alone），在所有测试基准上均有显著提升，且避免了训练崩溃。

**相对于Vanilla GRPO**：在两模型训练实验（rollout模型 ≠ 训练模型）中，Vanilla GRPO在训练后期出现性能崩溃，而Jackpot能维持稳定训练并持续提升。

### 适用边界与局限

**适用场景**：Jackpot特别适用于以下高吞吐量RL训练场景：(1) 大batch异步训练，rollout与训练更新之间存在显著延迟；(2) 分离式rollout-训练架构，actor和policy使用不同模型甚至不同架构；(3) 低精度训练（如FP8）中的量化不稳定性恢复。实验表明，即使在Qwen2.5-1.5B rollout训练Qwen2.5-3B的极端架构不匹配场景下，Jackpot仍能击败基线并维持训练稳定。

**超参数鲁棒性**：消融实验显示，拒绝阈值 $\lambda$ 在0.8-1.2范围内性能变化不大，$\lambda=1.0$ 是稳健的默认值；截断阈值 $C_1$ 在2-10范围内表现稳定，对最终性能不敏感。这降低了实际部署中的调参负担。

**已知局限**：从现有证据来看，论文未明确讨论Jackpot在以下方面的局限：(1) 在更大规模模型（如70B+）上的扩展性验证；(2) 在非数学推理任务（如代码生成、对话）上的泛化表现；(3) OBRS的接受率在极端分布偏移下的下界行为。这些方面需要进一步实验验证。

### 开放问题

1. **OBRS的渐进性质**：当actor与policy的分布偏移极大时（如使用完全不同领域的模型进行rollout），OBRS的接受率是否会降至不可用的水平？理论上的接受率下界与分布偏移程度之间的定量关系尚待分析。

2. **与RLHF/DPO的结合**：Jackpot目前仅在数学推理的GRPO框架下验证，其核心的分布对齐思想是否能迁移到RLHF的奖励模型训练或DPO等offline RL方法中，是一个值得探索的方向。

3. **多轮对话中的分布漂移**：在多轮交互场景中，分布偏移不仅来自模型更新延迟，还来自对话上下文的动态变化。Jackpot的OBRS机制是否能有效处理这种复合偏移，需要进一步研究。

4. **与推测解码的协同**：推测解码（speculative decoding）同样涉及draft模型与target模型之间的分布匹配问题，Jackpot的OBRS框架是否能应用于此场景以提升推测解码的接受率，是一个有趣的技术交叉点。

## 原文 PDF

![[paperPDFs/ICLR_2026/Jackpot_Align_Actor_Policy_Distribution_for_scalable_and_stable_RL_for_LLM.pdf]]
