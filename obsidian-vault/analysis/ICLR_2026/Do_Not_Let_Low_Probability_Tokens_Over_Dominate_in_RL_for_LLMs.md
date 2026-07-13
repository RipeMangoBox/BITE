---
title: "Do Not Let Low-Probability Tokens Over-Dominate in RL for LLMs"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Do_Not_Let_Low_Probability_Tokens_Over_Dominate_in_RL_for_LLMs.pdf
project_link: null
code_link: https://github.com/zhyang2226/AR-Lopti
openreview_forum_id: FOnAdLo0tM
aliases:
- ARLPTIL
- DNLLPTODRL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "token 概率 π 通过梯度幅度 ∝ (1-π) 影响更新贡献；可通过重新加权优势（Advantage Reweighting）或分阶段隔离更新（Lopti）来控制不同概率 token 的梯度影响力。"
primary_logic: "在 LLM 的 RL 训练中，梯度范数与 token 概率负相关，使得低概率 token 过度拉偏参数更新方向，损害高概率 token 的正确调整；通过削弱低概率 token 的梯度贡献或调整更新顺序可以恢复平衡，显著提升推理和数学任务性能。"
claims:
- "低概率 token 产生更大的梯度范数，主导模型更新方向，而高概率 token 正确更新的比例不足 50%。"
- "理论推导证明：任意层的梯度范数被约束在正比于 (1-π_θ(o_{i,t})) 的上下界之间。"
- "Advantage Reweighting 和 Lopti 能够显著提高高概率 token 的正确更新方向比例，并最终在 K&K 推理任务上带来高达 46.2% 的性能提升。"
- "K&K Logic Puzzles (Qwen2.5-3B-Instruct) 上 Avg. accuracy = GRPO + Reweight + Lopti: 0.57"
---

# Do Not Let Low-Probability Tokens Over-Dominate in RL for LLMs

> [!tip] 核心洞察
> 在 LLM 的 RL 训练中，梯度范数与 token 概率负相关，使得低概率 token 过度拉偏参数更新方向，损害高概率 token 的正确调整；通过削弱低概率 token 的梯度贡献或调整更新顺序可以恢复平衡，显著提升推理和数学任务性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 不要让低概率 token 在 LLM 强化学习训练中过度主导 |
| 英文题名 | Do Not Let Low-Probability Tokens Over-Dominate in RL for LLMs |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=FOnAdLo0tM) · [GitHub](https://github.com/zhyang2226/AR-Lopti) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Advantage Reweighting & Low-Probability Token Isolation (Lopti) |
| Dataset | K&K Logic Puzzles (Qwen2.5-3B-Instruct), K&K Logic Puzzles (Qwen2.5-7B-Instruct-1M), Math-related (DSR Uniform, Qwen2.5-7B), Math-related (ORZ |

> [!tip] 效果简介
> - K&K Logic Puzzles (Qwen2.5-3B-Instruct) 上，Avg. accuracy 为 GRPO + Reweight + Lopti: 0.57，对比 GRPO: 0.39，变化 +46.2%。
> - K&K Logic Puzzles (Qwen2.5-7B-Instruct-1M) 上，Avg. accuracy 为 GRPO + Reweight + Lopti: 0.91，对比 GRPO: 0.77，变化 +18.2%。
> - Math-related (DSR Uniform, Qwen2.5-7B) 上，Avg. all accuracy (%) 为 GRPO + Reweight: 40.01，对比 GRPO: 38.98，变化 +1.03 pp。

## 概要

在基于强化学习的大语言模型后训练中，策略梯度优化存在一个被忽视的结构性偏差：**低概率 token 的梯度范数与 $1-\pi_\theta(o_{i,t})$ 成正比，会不成比例地主导模型参数更新方向**，压制高概率 token 的正确调整，从而降低训练效率与最终推理能力。本文首次从“梯度不均衡”视角切入该问题，理论推导证明任意层的激活梯度范数被约束在正比于 $(1-\pi_\theta(o_{i,t}))$ 的上下界之间（Proposition 4.2），并通过实验证实低概率 token 产生的梯度量级远超高概率 token，导致高概率 token 正确更新的比例不足 50%（Figure 1, Figure 3）。

针对该瓶颈，作者提出两种互补的干预策略：

- **Advantage Reweighting**：按 token 概率线性重新缩放优势权重 $\hat{A}_{i,t} = [\alpha \cdot \pi_\theta(o_{i,t}) + (1-\alpha)] \cdot \hat{A}_i$，压低低概率 token 的梯度贡献，几乎不引入额外计算开销。
- **Low-Probability Token Isolation (Lopti)**：将 token 按概率阈值 $\eta$ 分为两组，先单独更新低概率 token，再更新高概率 token，通过调整更新顺序引导梯度流向。

在 K&K 逻辑谜题基准上，两种方法分别将 GRPO 基线性能提升 35.9% 和 38.5%，联合使用带来 **46.2%** 的准确率提升（Qwen2.5-3B-Instruct，Figure 4）；在更大规模的 Qwen2.5-7B-Instruct-1M 上也获得 18.2% 的提升。方法在 REINFORCE++ 和 DAPO 等策略梯度算法上同样有效，验证了其泛化性。数学相关任务上，Advantage Reweighting 单独使用即可带来约 1 个百分点的稳定增益，但 Lopti 的叠加未产生协同效应，其机理尚待进一步分析。方法的主要代价在于 Lopti 需执行两次更新，计算时间约为原来的两倍。

### LLM 强化学习训练的梯度失衡困境

在大语言模型的后训练阶段，强化学习已成为提升推理与对齐能力的关键手段。以 **GRPO**（Shao et al., 2024; Liu et al., 2025）为代表的策略梯度方法，通过分组相对优势替代独立价值模型，在降低训练开销的同时推动了推理能力的涌现。然而，这类方法在更新机制上存在一个被长期忽视的结构性缺陷：**不同概率 token 对模型更新的贡献严重失衡**。

### 核心瓶颈：低概率 token 过度主导梯度更新

该工作的核心发现是：在 LLM 的 RL 训练中，**低概率 token 的梯度范数远大于高概率 token，从而不成比例地主宰参数更新方向**。如 Figure 1(d) 所示，当将 token 按概率四分位分组后，最低概率组（概率 < 0.25）的梯度范数显著高于最高概率组（概率 > 0.75）。这种失衡导致了一个反直觉的现象：低概率 token 的少量出现，即可在梯度层面压倒大量高概率 token 的更新信号。

Figure 1(e,f) 的选择性更新实验进一步验证了这一判断——仅更新最低概率 token 时，高概率 token 的概率变化幅度甚至超过仅更新高概率 token 时的情形。这说明低概率 token 的梯度已经渗透并扭曲了高概率 token 的更新轨迹。

### 因果机制：梯度范数与 token 概率的负相关

该工作从理论上证明了这一现象的必然性。**Proposition 4.2** 给出了任意 Transformer 层激活值梯度范数的上下界：

$$\prod_{j=\ell+1}^{L} c_j \cdot |w_{i,t}| \cdot \sqrt{\frac{N}{N-1}} \cdot (1-\pi_\theta(o_{i,t})) \le \|\delta_\ell(o_{i,t})\| \le \prod_{j=\ell+1}^{L} d_j \cdot |w_{i,t}| \cdot \sqrt{2} \cdot (1-\pi_\theta(o_{i,t}))$$

该结论表明，对于任意层的梯度范数，其大小被约束在正比于 $(1-\pi_\theta(o_{i,t}))$ 的区间内。这意味着 **token 概率越低，其产生的梯度范数越大**——这是由 softmax 输出层的数学结构决定的，而非训练超参数或数据分布的偶然产物。

### 更新方向的系统性偏差

梯度范数的失衡直接转化为更新方向的偏差。Figure 3 的统计显示，在标准 GRPO 训练中，高概率 token 被正确更新（即优势为正时概率上升、优势为负时概率下降）的比例不足 50%，几乎等同于随机猜测。相比之下，低概率 token 的正确更新比例虽高，但其巨大的梯度量级使得模型整体更新被拉向少数低概率 token 的方向，压制了高概率 token 的有效学习。

### 现有方法的缺口

在 RL for LLMs 领域，已有工作关注了奖励设计、优势估计、KL 约束等环节的改进，但**尚未有方法从梯度贡献的 token 级不平衡角度切入**。该工作首次将梯度失衡识别为制约 RL 训练效率的关键瓶颈，并据此提出了两条互补的干预路径：通过优势重新加权（Advantage Reweighting）削弱低概率 token 的更新权重，以及通过分阶段隔离更新（Lopti）调整梯度流向。

## 核心方法与创新机理

本工作首次从**梯度不均衡**的角度审视 LLM 的 RL 训练效率问题。其核心发现是：在 GRPO 等策略梯度算法中，低概率 token 的梯度范数与 $(1 - \pi_\theta)$ 成正比（见 Proposition 4.2，Equation 3），这导致它们不成比例地主导向量场更新方向，压制高概率 token 的有效学习。基于这一因果机制，作者提出两个正交且可叠加的改进插槽：

### 改进插槽一：优势重新加权（Advantage Reweighting）

**Baseline 做法**：GRPO 中所有 token 共享统一的分组相对优势 $\hat{A}_i$，不区分 token 概率高低。

**创新做法**：将每个 token 的优势按其在当前策略下的概率线性缩放：

$$\hat{A}_{i,t} = [\alpha \cdot \pi_{\theta}(o_{i,t}) + (1-\alpha)] \cdot \hat{A}_i$$

其中 $\alpha \in [0, 1]$ 控制压低低概率 token 贡献的程度。当 $\alpha=0$ 时退化为原始 GRPO；$\alpha$ 越大，低概率 token 的更新权重被削弱得越强。该方法几乎不引入额外计算开销。

### 改进插槽二：低概率 Token 隔离更新（Lopti）

**Baseline 做法**：在一个梯度步中同时更新所有 token，低概率 token 的大梯度直接干扰高概率 token 的更新方向。

**创新做法**：以阈值 $\eta$（默认 0.5）将 token 分为低概率组（$\pi \leq \eta$）和高概率组（$\pi > \eta$），**先更新低概率 token，再更新高概率 token**（Algorithm 1, lines 11–19）。这一顺序设计将低概率 token 的梯度“引流”至先导步骤，避免其对后续高概率 token 更新的干扰。代价是单步更新计算量约翻倍。

### 插槽间的协同与分工

两个插槽可独立或联合使用。在逻辑推理任务（K&K）上，二者叠加产生协同增益（+46.2%）；但在数学任务上，联合使用无额外提升，作者建议单独使用（Table 1）。消融实验（Figure 6）进一步揭示：仅允许更新高概率 token（屏蔽低概率 token）会严重损害 GRPO 基线，说明低概率 token 并非无用，而是需要**受控的梯度贡献**；反转 Lopti 更新顺序（先高后低）则导致训练崩溃，验证了“先低后高”顺序的必要性。

### 方法定位

两个改进插槽均作用于 GRPO 的**优势估计与梯度更新环节**，不改变采样、奖励计算或 KL 惩罚组件。它们同样适用于 REINFORCE++ 和 DAPO 等基于策略梯度的 RL 算法（Table 7, Figure 19），展现出良好的泛化性。

本文提出的方法围绕一个核心发现展开：在 LLM 的强化学习训练中，低概率 token 的梯度范数与 $(1-\pi)$ 成正比，会不成比例地主导模型更新方向，压制高概率 token 的有效学习。为解决这一问题，论文设计了两种可独立或联合使用的干预机制——**Advantage Reweighting** 和 **Low-Probability Token Isolation (Lopti)**，嵌入到以 GRPO 为基础 RL 算法的训练流水线中。

### Pipeline 总览

整体训练流程由五个核心模块串联构成，Advantage Reweighting 和 Lopti 分别在优势估计与策略更新阶段插入干预：

1. **采样（Sampling）**：对于每个问题 $q$，使用当前策略 $\pi_\theta$ 采样 $G$ 个回答 $\{o_i\}_{i=1}^G$。
2. **奖励计算（Reward Calculation）**：依据规则奖励函数 $r(q, o)$ 评估每个回答的得分（见 Section 5.1、Table 4）。
3. **优势估计（Advantage Estimation）**：基于分组奖励计算组相对优势 $\hat{A}_i$，作为 token 级更新信号的基础。
4. **优势重加权（Advantage Reweighting，可选）**：按 token 概率 $\pi_\theta(o_{i,t})$ 线性缩放优势权重，弱化低概率 token 的梯度贡献。
5. **低概率 token 隔离（Lopti，可选）**：将 token 按概率阈值 $\eta$ 分为低概率组（$\pi \le \eta$）和高概率组（$\pi > \eta$），先更新低概率组，再更新高概率组，引导梯度流向。
6. **策略更新（Policy Update）**：使用 GRPO 的 clipped objective 和 KL 惩罚更新策略参数 $\theta$。

### 关键干预机制

**Advantage Reweighting** 通过公式 $\hat{A}_{i,t} = [\alpha \cdot \pi_\theta(o_{i,t}) + (1-\alpha)] \cdot \hat{A}_i$ 重新计算 token 级优势。超参数 $\alpha \in [0,1]$ 控制压低低概率 token 贡献的程度：$\alpha$ 越大，低概率 token 的优势被削弱得越多，几乎不引入额外计算开销。

**Lopti** 则通过分阶段更新实现梯度流向控制：先将低概率 token 单独更新，使其梯度先于高概率 token 生效，从而减少两类 token 在同一梯度步中的相互干扰。代价是每次更新需执行两次前向-反向传播，计算时间约为原来的两倍。

两种机制可以并发使用。在 K&K 逻辑推理任务上，联合使用带来了最高的性能增益（Qwen2.5-3B-Instruct 上准确率从 0.39 提升至 0.57，相对提升 46.2%）；但在数学任务上，联合使用未带来额外增益，推荐单独使用（Table 1）。

### 输入输出流

- **输入**：训练问题集 $\mathcal{D}$，预训练参考策略 $\pi_{\text{ref}}$，初始策略 $\pi_\theta$
- **中间信号**：采样回答 $\{o_i\}$ → 规则奖励 $r(q, o_i)$ → 组相对优势 $\hat{A}_i$ →（可选）重加权优势 $\hat{A}_{i,t}$ →（可选）按 $\eta$ 分组的 token 集
- **输出**：更新后的策略参数 $\theta$，在推理和数学任务上具有更高的测试准确率

### 问题建模与 GRPO 基础

本文采用一种经过修改的 GRPO 变体作为策略优化基础。具体而言，移除了原始 GRPO 中的回答长度归一化操作，改为在同一 query-batch 内对所有 token 进行统一归一化。

GRPO 的优化目标为：

$$J_{GRPO}(\theta) = \mathbb{E}_{q \sim \mathcal{D}, \{o_i\}_{i=1}^G \sim \pi_{old}} \frac{1}{\sum_{i=1}^G |o_i|} \sum_{i=1}^G \sum_{t=1}^{|o_i|} \{ \min[ r_{i,t}(\theta) \hat{A}_{i,t}, \operatorname{clip}(r_{i,t}(\theta); 1-\epsilon_l, 1+\epsilon_h) \hat{A}_{i,t} ] - \beta \mathbb{D}_{\mathrm{KL}}[\pi_\theta | \pi_{ref}] \}$$

其中重要性采样比率 $r_{i,t}(\theta) = \frac{\pi_\theta(o_{i,t} | q, o_{i,<t})}{\pi_{old}(o_{i,t} | q, o_{i,<t})}$ 表示当前策略与旧策略在 token $t$ 上的概率比；KL 散度估计器采用无偏形式 $\mathbb{D}_{\mathrm{KL}}[\pi_\theta | \pi_{ref}] = \frac{\pi_{ref}(o_{i,t})}{\pi_\theta(o_{i,t})} - \log \frac{\pi_{ref}(o_{i,t})}{\pi_\theta(o_{i,t})} - 1$。

### 核心理论：梯度范数与 token 概率的负相关关系

对 GRPO 目标求梯度可得每个 token 的更新由 log-prob 梯度与上下文权重 $w_{i,t}$ 的乘积构成：

$$\nabla_\theta J_{GRPO}(\theta) = \mathbb{E} \frac{1}{\sum |o_i|} \sum_i \sum_t \underbrace{[\frac{\pi_\theta(o_{i,t})}{\pi_{old}(o_{i,t})} \hat{A}_{i,t} \cdot \mathbb{I}_{\mathrm{trust}} + \beta \frac{\pi_{ref}(o_{i,t})}{\pi_\theta(o_{i,t})} - \beta]}_{w_{i,t}} \cdot \nabla_\theta \log \pi_\theta(o_{i,t})$$

本文的核心理论贡献（Proposition 4.2）证明了：对于任意第 $\ell$ 层的激活值，其梯度范数被约束在与 $(1 - \pi_\theta(o_{i,t}))$ 成正比的上下界之间：

$$\prod_{j=\ell+1}^{L} c_j \cdot |w_{i,t}| \cdot \sqrt{\frac{N}{N-1}} \cdot (1-\pi_\theta(o_{i,t})) \le \|\delta_\ell(o_{i,t})\| \le \prod_{j=\ell+1}^{L} d_j \cdot |w_{i,t}| \cdot \sqrt{2} \cdot (1-\pi_\theta(o_{i,t}))$$

这一理论结果揭示了**低概率 token 产生更大梯度范数**的根本原因：当 $\pi_\theta(o_{i,t}) \to 0$ 时，梯度范数上界趋近于最大值；当 $\pi_\theta(o_{i,t}) \to 1$ 时，梯度范数趋近于零。这意味着低概率 token 会不成比例地主导模型参数更新方向，压制高概率 token 的有效学习。

### 方法一：Advantage Reweighting（优势重加权）

针对上述梯度偏差，Advantage Reweighting 通过线性缩放优势权重来压低低概率 token 的更新贡献：

$$\hat{A}_{i,t} = [\alpha \cdot \pi_{\theta}(o_{i,t}) + (1-\alpha)] \cdot \hat{A}_{i,t}$$

其中 $\alpha \in [0,1]$ 为控制压低程度的超参数。当 $\alpha = 0$ 时退化为原始 GRPO；$\alpha$ 越大，低概率 token 的优势被压缩越强。该方法几乎不引入额外计算开销。

### 方法二：Low-Probability Token Isolation (Lopti)

Lopti 采用分阶段更新策略来隔离低概率 token 的梯度干扰。具体流程为：

1. 预定义概率阈值 $\eta \in (0,1)$，将 batch 内所有 token 分为两组：低概率 token（$\pi \le \eta$）和高概率 token（$\pi > \eta$）
2. **先**对低概率 token 组执行一次策略更新
3. **再**对高概率 token 组执行一次策略更新

这一顺序至关重要——消融实验表明，反转更新顺序（先高后低）会导致训练崩溃。Lopti 的计算开销约为原始 GRPO 的两倍，因为需要执行两次更新步骤。

### 方法协同

Advantage Reweighting 与 Lopti 可并行使用。在 K&K 逻辑推理任务上，二者联合使用带来了最优性能提升（+46.2%）；但在数学任务上，联合使用未产生进一步的协同增益，推荐单独使用。

## 实验与关键发现

### 核心发现：低概率 token 主导梯度更新

论文首先通过动机实验（Figure 1）揭示了 GRPO 训练中的一个关键现象：在 Qwen2.5-7B-Instruct-1M 上对 K&K Logic Puzzles 进行 GRPO 训练时，token 的梯度范数与其概率呈显著负相关。将 token 按概率四分位分组后，最低概率组（π < 0.25）的梯度范数远高于最高概率组（π > 0.75）。当仅更新低概率 token 时，模型参数发生剧烈变化；而仅更新高概率 token 时，概率变化几乎为零。这直接证实了“低概率 token 过度主导模型更新方向”的瓶颈。

进一步分析（Figure 3）表明，在 naive GRPO 下，高概率 token 中正优势 token 被更新到正确方向的比例不足 50%——这意味着模型在调整高置信度推理步骤时近乎随机。Advantage Reweighting 和 Lopti 均能显著提升这一比例，使高概率 token 的更新更加可靠。

### K&K 逻辑推理任务主结果

Figure 4 展示了在 K&K Logic Puzzles 上的核心结果。所有评估准确率取最后三个检查点的平均值以降低随机性。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_FOnAdLo0tM/figures/011_Figure_4.jpg]]
*Figure 4: Experimental results on the K&K Logic Puzzles benchmark. For Advantage Reweight, $\alpha$ = 0 . 3 , and for Lopti, $\eta$ = 0 . 5 . . The reward curve during training (left) is truncated to exclude the first epoch and smoothed with an exponential moving average (coefficient: 0.95). The evaluation accuracy on the test set (right) are averaged over the last three checkpoints to mitigate randomness

| 模型 | 方法 | 平均准确率 | 相对提升 |
|------|------|-----------|---------|
| Qwen2.5-3B-Instruct | GRPO (baseline) | 0.39 | — |
| Qwen2.5-3B-Instruct | + Reweight | 0.53 | +35.9% |
| Qwen2.5-3B-Instruct | + Lopti | 0.54 | +38.5% |
| Qwen2.5-3B-Instruct | + Reweight + Lopti | **0.57** | **+46.2%** |
| Qwen2.5-7B-Instruct-1M | GRPO (baseline) | 0.77 | — |
| Qwen2.5-7B-Instruct-1M | + Reweight | 0.88 | +14.3% |
| Qwen2.5-7B-Instruct-1M | + Lopti | 0.89 | +15.6% |
| Qwen2.5-7B-Instruct-1M | + Reweight + Lopti | **0.91** | **+18.2%** |

两种方法在 3B 模型上的联合增益（46.2%）显著高于 7B 模型（18.2%），暗示小模型对低概率 token 主导问题更敏感。训练奖励曲线（EMA 平滑，系数 0.95）显示，Reweight 和 Lopti 均能加速收敛并提升最终奖励水平。

### 数学推理任务主结果

Table 1 汇总了数学相关数据集上的结果。此处 Advantage Reweighting 的 α 设为 0.1，Lopti 的 η 固定为 0.5。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_FOnAdLo0tM/figures/022_Table_1.jpg]]
*Table 1: Experimental results on math-related datasets (DSR for DeepScaleR and ORZ for Open-Reasoner-Zero). For Advantage Reweight, α is set to 0.1, and for Lopti, η is set to 0.5. The evaluation accuracy(%) are averaged over the last three checkpoints to mitigate randomness*

| 数据集 | 方法 | 平均准确率 (%) |
|--------|------|---------------|
| DSR Uniform | GRPO | 38.98 |
| DSR Uniform | + Reweight | **40.01** |
| DSR Uniform | + Lopti | 39.75 |
| DSR Uniform | + Reweight + Lopti | 39.83 |
| ORZ | GRPO | 39.83 |
| ORZ | + Reweight | **41.09** |
| ORZ | + Lopti | 40.57 |
| ORZ | + Reweight + Lopti | 40.81 |

在数学任务上，Advantage Reweighting 单独使用效果最佳（DSR +1.03 pp，ORZ +1.26 pp），而 Lopti 的增益较小。**关键失败模式**：Reweight 与 Lopti 联合使用时并未产生协同增益，甚至略低于 Reweight 单独使用。论文建议在数学任务中单独使用 Reweight。这一现象需要手动验证——可能与数学数据中低概率 token 比例较低有关，使得 Lopti 的分组隔离策略收益有限。

### 方法泛化性验证

Table 7 将方法迁移到 REINFORCE++ 算法上，在 K&K 任务中验证泛化性：

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_FOnAdLo0tM/figures/037_Table_7.jpg]]
*Table 7: Experimental results of REINFORCE++ on the K&K Logic Puzzles dataset. For Advantage Reweight, α = 0.1, and for Lopti, $\eta$ = 0 . 5 . The evaluation accuracy on the test set are averaged over the last three checkpoints to mitigate randomness*

| 模型 | 方法 | 平均准确率 | 相对提升 |
|------|------|-----------|---------|
| Qwen2.5-3B-Instruct | REINFORCE++ | 0.23 | — |
| Qwen2.5-3B-Instruct | + Reweight + Lopti | **0.41** | **+76.5%** |
| Qwen2.5-7B-Instruct-1M | REINFORCE++ | 0.62 | — |
| Qwen2.5-7B-Instruct-1M | + Reweight + Lopti | **0.88** | **+41.9%** |

REINFORCE++ 的 baseline 远低于 GRPO，但 Reweight + Lopti 带来的相对提升更为显著（3B 上 +76.5%），表明低概率 token 主导问题在不同策略梯度算法中普遍存在，且该方法对此类算法具有广泛适用性。DAPO 实验（Table 8）和 LLaMA 系列模型实验（Table 9）也验证了跨模型的一致性增益。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_FOnAdLo0tM/figures/040_Table_8.jpg]]
*Table 8: Experimental results of DAPO on the K&K Logic Puzzles dataset*

### 消融研究

**仅更新高概率 token 的后果**（Figure 6a）：屏蔽低概率 token 仅允许高概率 token 更新会严重损害 GRPO baseline 性能。这说明低概率 token 虽然“过度主导”，但完全排除它们同样有害——它们仍携带必要的探索信号。

**Lopti 更新顺序的敏感性**（Figure 6b）：反转 Lopti 的更新顺序（先高概率后低概率）会导致训练崩溃、准确率显著下降。这验证了“先让低概率 token 释放梯度张力，再让高概率 token 在稳定梯度方向上调整”这一顺序设计的必要性。

**α 超参数调节**（Figure 6c）：在 K&K 推理任务中，α 取 0.2–0.3 时效果最优；过低（α=0）等价于 naive GRPO，过高（α=1）则完全按概率缩放优势，过度压制低概率 token。数学任务中 α=0.1 更优（Table 3），说明不同任务对低概率 token 的依赖程度不同。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_FOnAdLo0tM/figures/027_Table_3.jpg]]
*Table 3: Hyperparameter settings for Advantage Reweighting and Lopti*

**η 阈值调节**（Figure 6d）：Lopti 的阈值 η 在 0.3–0.7 范围内表现稳定，η=0.5 是通用选择。

**80/20 规则与 batch shard 数交互**（Figure 19）：当 GRPO/DAPO 的更新 batch shard 数 n ≤ 8 时，流行的 80/20 规则（Wang et al., 2025）反而降低性能；仅当 n = 16 时才有效。这表明低概率 token 主导问题的严重程度与 on-policy 采样程度相关——更大的 shard 数使策略更 on-policy，低概率 token 的梯度偏差更突出。

### 计算开销分析

Table 6 对比了 Lopti 的计算开销。由于 Lopti 需要将 token 分成两组并执行两次前向-反向传播，更新计算时间约为原来的两倍。例如，Qwen2.5-7B-Instruct-1M 上每步从约 120 秒增加到约 240 秒。Advantage Reweighting 几乎不引入额外计算开销，是轻量级首选。

![[assets/figures/papers/paper_list_l17_https_openreview_net_forum_id_FOnAdLo0tM/figures/034_Table_6.jpg]]
*Table 6: Computational cost comparison of Lopti operation over the first 50 training steps on K&K Logic Puzzle Dataset*

### 推理行为分析

Figure 5 分析了推理相关词频与奖励的关系。在 naive GRPO 训练中，Analysis、Statement、Causal 类词汇的频率与样本奖励呈正相关（Pearson r > 0），而 Assumption 和 Assertion 类词汇呈负相关。Advantage Reweighting 和 Lopti 训练出的模型在正相关词汇上的使用频率更高，在负相关词汇上更低，说明这两种方法不仅提升了准确率，也实质性地改善了模型的推理行为模式。

## 定位与知识库关联

### 问题定位：RL 训练中的梯度失衡

本文揭示的核心瓶颈在于 LLM 强化学习训练中一个此前未被明确指出的梯度失衡现象：**低概率 token 的梯度范数与 $1-\pi_\theta(o_{i,t})$ 成正比，不成比例地主导演化更新方向，压制高概率 token 的有效学习**。这一发现将 LLM 的 RL 训练优化从奖励设计、优势估计等传统视角，转向了 token 级别的梯度贡献分布问题。

理论推导（Proposition 4.2, Equation 3）给出了严格的上下界约束：任意层激活值的梯度范数 $\|\delta_\ell(o_{i,t})\|$ 被限制在正比于 $(1-\pi_\theta(o_{i,t}))$ 的锥形区域内。动机实验（Figure 1）进一步验证，低概率 token 产生显著更大的梯度范数，而高概率 token（$\pi > 0.75$）的正确更新方向比例不足 50%（Figure 3）。

### 方法在 RL for LLM 谱系中的位置

本文提出的 **Advantage Reweighting** 和 **Low-Probability Token Isolation (Lopti)** 属于 **token 级梯度调控** 技术，位于现有 RL for LLM 方法的下游优化层。其与相关工作的关系如下：

- **相对于 GRPO**（Shao et al., 2024）：GRPO 中所有 token 共享统一的分组相对优势 $\hat{A}_i$，不区分 token 概率。Advantage Reweighting 将优势重新计算为 $\hat{A}_{i,t} = [\alpha \cdot \pi_\theta(o_{i,t}) + (1-\alpha)] \cdot \hat{A}_i$（Equation 4），按 token 概率线性缩放更新权重；Lopti 则将 token 按阈值 $\eta$ 分为两组，先更新低概率组再更新高概率组（Algorithm 1），通过调整更新顺序引导梯度流向。
- **相对于 DAPO**：消融实验（Figure 19）表明，DAPO 中流行的 80/20 过滤规则仅在更新 batch shard 数 $n=16$ 时有效，当 $n \le 8$ 时反而降低性能，说明低概率 token 的主导问题与 on-policy 程度存在交互。
- **相对于 REINFORCE++**：方法在 REINFORCE++ 上同样有效，在 K&K 推理任务上带来 76.5% 的性能提升（Table 7），证明其适用于多种基于策略梯度的 RL 算法。

### 适用边界与局限

1. **计算开销**：Lopti 需要将 token 分成两组并执行两次更新，更新计算时间约为原来的两倍。Advantage Reweighting 几乎无额外计算成本，但在数学任务上单独使用即可达到最优效果。
2. **任务依赖性**：在 K&K 逻辑推理任务上，Advantage Reweighting 和 Lopti 联合使用产生协同增益（+46.2%）；但在数学任务上，联合使用未带来进一步提升，推荐单独使用。该差异可能与数学任务中低概率 token 的比例较低有关。
3. **算法覆盖范围**：方法仅在 GRPO、REINFORCE++ 和 DAPO 等基于策略梯度的 on-policy 算法上验证，未涉及离线 RL 或 DPO 系列方法。
4. **模型规模限制**：实验主要在 Qwen2.5-3B/7B 和 LLaMA 系列上进行，缺乏对 70B+ 规模模型的评估。

### 开放问题

1. **数学任务的协同失效**：为何 Advantage Reweighting 和 Lopti 在数学数据集上无协同增益？是否与数学任务中低概率 token 的比例或分布特征有关？
2. **自适应调控**：能否设计根据训练阶段或 token 类型动态调整 $\alpha$ 和 $\eta$ 的自适应机制？
3. **组件交互**：低概率 token 的过度主导与 KL 惩罚、clip 阈值等其他 GRPO 组件之间存在多大程度的交互？
4. **层级差异**：梯度偏差问题是否在所有 transformer 层表现一致？是否可以设计针对特定层或 attention head 的隔离策略？
5. **跨模态扩展**：该方法是否适用于多模态 LLM 或基于扩散的文本生成模型的 RL 训练？

## 原文 PDF

![[paperPDFs/ICLR_2026/Do_Not_Let_Low_Probability_Tokens_Over_Dominate_in_RL_for_LLMs.pdf]]
