---
title: "BAPO: Stabilizing Off-Policy Reinforcement Learning for LLMs via Balanced Policy Optimization with Adaptive Clipping"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BAPO_Stabilizing_Off_Policy_Reinforcement_Learning_for_LLMs_via_Balanced_Policy_Optimization_with_Adaptive_Clipping.pdf
project_link: null
code_link: null
aliases:
- BBPOAC
- BAPO
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/language_speech_and_dialog
core_operator: "BAPO动态调整PPO式裁剪上下界，以平衡离策略LLM强化学习中正负优势token的贡献。"
primary_logic: "训练中监控正样本损失占比，放宽上界纳入低概率正样本并收紧下界抑制低概率负样本。"
claims:
- "固定对称裁剪会排除低概率正样本，造成策略熵下降和探索能力受损。"
- "自适应非对称裁剪可稳定离策略RL并避免负优势样本主导更新。"
- "BAPO在AIME数学推理和跨领域评估中提升7B与32B模型表现。"
---

# BAPO: Stabilizing Off-Policy Reinforcement Learning for LLMs via Balanced Policy Optimization with Adaptive Clipping

> [!tip] 核心洞察
> 通过动态调整裁剪边界 c_low 和 c_high，可以重新平衡正负样本的贡献：纳入更多低概率正样本（熵增更新），过滤过多低概率负样本，从而保持策略熵、稳定训练并提升性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BAPO：通过自适应裁剪的平衡策略优化稳定大语言模型的离策略强化学习 |
| 英文题名 | BAPO: Stabilizing Off-Policy Reinforcement Learning for LLMs via Balanced Policy Optimization with Adaptive Clipping |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jIeJJqG7dz) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/language_speech_and_dialog |
| Method | BAPO (Balanced Policy Optimization with Adaptive Clipping) |
| Dataset | AIME 2024, AIME 2025 |

> [!tip] 效果简介
> - AIME 2024 上，Pass@1 为 70.8 (7B), 87.1 (32B)，对比 66.9 (7B SFT), 84.4 (32B SFT)，变化 +3.9 (7B), +2.7 (32B)。
> - AIME 2025 上，Pass@1 为 62.5 (7B), 80.0 (32B)，对比 59.0 (7B SFT), 78.1 (32B SFT)，变化 +3.5 (7B), +1.9 (32B)。
> - AIME 2024 上，Pass@1 为 87.1 (32B BAPO)，对比 81.4 (Qwen3-32B)，变化 +5.7。

## 概要

本文提出 **BAPO (Balanced Policy Optimization with Adaptive Clipping)**，一种用于稳定大语言模型（LLM）离策略强化学习训练的自适应裁剪策略优化方法。核心贡献在于：通过动态调整策略梯度目标函数中的裁剪边界（clipping bounds）$c_{\mathrm{low}}$ 和 $c_{\mathrm{high}}$，重新平衡正负优势样本对优化的贡献，从而有效抑制离策略训练中常见的策略熵急剧下降和训练崩溃问题。实验表明，BAPO 在 AIME 2024 和 AIME 2025 等数学推理基准上显著超越现有方法：7B 模型超越 SkyWork-OR1-7B 等开源模型，32B 模型不仅达到同规模最优，还超越了 o3-mini 和 Gemini-2.5-Flash-Thinking 等专有系统。

### 2.1 离策略强化学习在 LLM 中的挑战

离策略强化学习（off-policy RL）通过重用旧策略采样的数据来提升样本效率，但在 LLM 训练中面临严重的不稳定问题。如 Figure 2 所示，随着数据陈旧度（data staleness）增加，模型出现优化不稳定、熵持续下降甚至训练突然崩溃的现象。

### 2.2 根本瓶颈：正负样本贡献失衡

论文通过分析 PPO 梯度分解（Equation 5）发现，固定对称裁剪边界（如 $[0.8, 1.2]$）导致两个关键问题：

1. **负优势样本主导优化**：如 Figure 4 所示，正样本在数量和损失贡献上均占少数，负样本的梯度主导了更新方向。
2. **熵增更新被系统性排除**：固定裁剪阻止了低概率正样本参与优化，而这些样本正是熵增更新的来源。

> "in standard algorithms with symmetric clipping bounds (e.g., [0.8,1.2]), a majority of positive, low-probability tokens are prevented from contributing to the optimization. This systematic exclusion of entropy-increasing updates causes a continuous decline in entropy, ultimately crippling the model's exploratory capacity and resulting in a performance bottleneck."

### 2.3 熵-裁剪规则（Entropy-Clip Rule）

论文推导了熵-裁剪规则（Equation 6），揭示了裁剪机制与熵变化之间的定量关系：

$$\Delta \mathcal{H}(\pi_\theta) \approx -\eta \cdot \mathrm{Cov}_{y \sim \pi_\theta(\cdot|x)} \left[ \log \pi_\theta(y_t | x, y_{<t}), A_t \cdot \mathcal{X}(y_t) + C \right]$$

其中 $\mathcal{X}(y_t)$ 是裁剪指示函数（Equation 7），表示 token 是否未被裁剪并参与梯度计算。该规则表明：只有未被裁剪的 token 才影响熵变化，且熵的变化方向由对数概率与优势之间的协方差决定。

## 核心方法与创新机理

### 3.1 关键洞察

通过非对称裁剪实验（Figure 7），论文验证了两个关键发现：

- **增大上界 $c_{\mathrm{high}}$**（引入更多低概率正样本）提升性能并抑制熵下降
- **放松下界 $c_{\mathrm{low}}$**（引入更多低概率负样本）降低性能并加速熵崩溃

> "increasing the upper bound c_high (which introduces more low-probability positive tokens to policy updates) improves performance while counteracting the downward trend of entropy... relaxing the lower bound c_low (which introduces more low-probability negative tokens to policy updates) not only degrades performance but also accelerates entropy collapse."

### 3.2 BAPO 自适应裁剪机制

BAPO 的核心创新在于动态调整裁剪边界 $c_{\mathrm{low}}$ 和 $c_{\mathrm{high}}$，以维持正样本损失贡献占比不低于阈值 $\rho_0$。具体而言：

- **纳入更多低概率正样本**（熵增更新）
- **过滤过多低概率负样本**（防止熵崩溃）
- **防止正样本过度主导**（避免尾部退化）

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_jIeJJqG7dz_BAPO_Stabiliz/figures/001_Figure_1.jpg]]
*Figure 1: Performance of BAlanced Policy Optimization with Adaptive Clipping (BAPO).*

BAPO 的训练流程包含三个主要模块：

1. **采样与奖励计算**：从行为策略 $\pi_{\theta_{\mathrm{rollout}}}$ 采样响应，计算奖励和优势
2. **自适应裁剪边界调整**：根据正样本损失贡献比例 $\rho$ 动态调整 $c_{\mathrm{low}}$ 和 $c_{\mathrm{high}}$
3. **策略更新**：使用调整后的裁剪边界最大化 BAPO 目标函数

### 5.1 BAPO 目标函数

BAPO 采用与 PPO 相同形式的目标函数，但使用自适应裁剪边界：

$$J^{\mathrm{BAPO}}(\theta) = \mathbb{E}_{y \sim \pi_{\theta_{\mathrm{rollout}}}(\cdot|x)} \sum_{t=1}^T \left[ \min( r_t \cdot A_t, \mathrm{clip}(r_t, c_{\mathrm{low}}, c_{\mathrm{high}}) \cdot A_t ) \right]$$

### 5.2 自适应裁剪条件

BAPO 通过以下条件确保正样本贡献占比不低于阈值 $\rho_0$：

$$\frac{ \sum_{A_t > 0} \pi_{\theta_{\mathrm{rollout}}}(y_t) \cdot | \min( r_t \cdot A_t, \mathrm{clip}(r_t, 0, c_{\mathrm{high}}) \cdot A_t ) | }{ \sum_{A_t} \pi_{\theta_{\mathrm{rollout}}}(y_t) \cdot | \min( r_t \cdot A_t, \mathrm{clip}(r_t, c_{\mathrm{low}}, c_{\mathrm{high}}) \cdot A_t ) | } \geq \rho_0$$

算法逐步增大 $c_{\mathrm{high}}$ 和 $c_{\mathrm{low}}$（步长分别为 $\delta_1$ 和 $\delta_2$），直至满足上述条件。

### 5.3 理论分析

论文在附录 G 中提供了完整的理论推导，证明在 tabular softmax 策略假设下：

- **Proposition 1**：PPO 更新后 logit 参数的变化为 $\eta \cdot \pi_\theta(y_t) \cdot [A(y_t) \cdot \mathcal{X}(y_t) + C]$
- **Proposition 2 (Equation 6)**：熵变化近似为对数概率与优势的负协方差
- **Table 9** 总结了不同 token 特征对熵变化的影响：高概率高优势或低概率低优势的 token 降低熵；高概率低优势或低概率高优势的 token 增加熵

## 实验与关键发现

### 6.1 主要结果

**Table 1: Main evaluation results.**

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_jIeJJqG7dz_BAPO_Stabiliz/figures/020_Table_1.jpg]]
*Table 1: Main evaluation results.*

| 模型 | AIME 2024 | AIME 2025 |
|------|-----------|-----------|
| BP-Math-7B SFT | 66.9 | 59.0 |
| BP-Math-7B BAPO | **70.8** | **62.5** |
| BP-Math-32B SFT | 84.4 | 78.1 |
| BP-Math-32B BAPO | **87.1** | **80.0** |
| Qwen3-32B | 81.4 | 72.9 |
| DeepSeek-R1 | 79.8 | 70.0 |

BAPO 在 7B 和 32B 规模上均显著超越 SFT 基线，32B 模型超越 Qwen3-32B（+5.7/+7.1）和 DeepSeek-R1（+7.3/+10.0）。

### 6.2 跨领域泛化

**Table 3: Comparison of performance across different domains.**

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_jIeJJqG7dz_BAPO_Stabiliz/figures/023_Table_3.jpg]]
*Table 3: Comparison of performance across different domains. Results includes AMC 2023 and OlympiadBench He et al. (2024) for advanced mathematical reasoning, ARC-AGI Chollet (2019) for logical reasoning, and GPQA-Diamond Rein et al. (2024) for scientific question answering.*

| 方法 | AMC 2023 | OlympiadBench | ARC-AGI | GPQA-Diamond |
|------|----------|---------------|---------|--------------|
| Original | 82.5 | 54.2 | 1.4 | 45.7 |
| BAPO | **92.5** | **58.4** | **3.2** | **51.3** |

BAPO 在数学推理（AMC 2023, OlympiadBench）、逻辑推理（ARC-AGI）和科学问答（GPQA-Diamond）等多个领域均取得一致提升。

### 6.3 消融实验

**Table 5: Ablation studies on positive token contribution threshold $\rho_0$**

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_jIeJJqG7dz_BAPO_Stabiliz/figures/029_Table_5.jpg]]
*Table 5: Ablation studies on positive token contribution threshold $\rho _ { 0 }$*

| $\rho_0$ | AIME 2024 | AIME 2025 | Average |
|----------|-----------|-----------|---------|
| 0.40 | 70.8 | 62.5 | 66.7 |
| 0.45 | 69.6 | 63.8 | 66.7 |
| 0.50 | 71.3 | 60.8 | 66.1 |

正样本贡献阈值 $\rho_0$ 在 0.4-0.5 范围内性能波动很小（平均 66.1-66.7），表明 BAPO 对超参数不敏感。

**Table 6: Ablation studies on movable range of clipping bounds.**

裁剪边界移动范围在默认设置 $[0.6,0.9]$ 和 $[1.2,3.0]$ 附近变化时，BAPO 始终取得高分（平均 65.5-66.9）。

**Table 7: Ablation studies on step sizes $\delta_1$ and $\delta_2$**

步长 $\delta_1$ 和 $\delta_2$ 的变化对性能不敏感（平均 66.7-66.9）。

### 6.4 训练动态分析

- **Figure 8** 显示 BAPO 实现了稳定的优化过程：训练奖励快速上升、正样本贡献增加、梯度归一化稳定、策略熵保持稳定。
- **Figure 10** 确认裁剪边界在训练过程中动态波动，验证了自适应调整机制的有效性。
- **Figure 11** 显示 BAPO 在不同数据陈旧度下均优于基线和 clip-higher 方法。
- **Figure 12** 显示 BAPO 在部分 rollout 场景下保持稳定训练，而 GRPO 出现不稳定。

### 6.5 公平性说明

- 所有实验使用相同的基座模型（DeepSeek-R1-Distill-Qwen-7B/32B、OctoThinker-Llama-3B-Long-Zero）
- 基线方法（GRPO、DAPO、TOPR、DCPO）在相同设置下复现
- BAPO 的超参数通过消融实验验证，默认设置简单且鲁棒

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_jIeJJqG7dz_BAPO_Stabiliz/figures/022_Table_2.jpg]]
*Table 2: Performance of Llama-based models.*

![[assets/figures/papers/iclr26_vision_multimodal_applications__language_speech_and_dialog__b001_jIeJJqG7dz_BAPO_Stabiliz/figures/028_Table_4.jpg]]

## 定位与知识库关联

### 7.1 与现有方法的关系

BAPO 属于离策略强化学习在 LLM 推理能力训练中的应用，其方法谱系如下：

- **PPO (Schulman et al., 2017)**：基础算法，使用固定对称裁剪边界
- **GRPO (Shao et al., 2024)**：主要基线，在 DeepSeekMath 中引入的组相对策略优化
- **DAPO (Yu et al., 2025)**：提出 clip-higher 技术放大正信号，但未处理负样本
- **TOPR (Roux et al., 2025a)**：离策略 RL 变体
- **DCPO (Yang et al., 2025b)**：离策略 RL 变体
- **BAPO (本文)**：首次提出自适应裁剪边界，同时处理正负样本贡献失衡

### 7.2 局限性

1. 消融实验仅在 7B 模型上进行，更大规模模型（如 32B）上的超参数敏感性未充分验证
2. 未报告训练的计算成本（如 GPU 小时数）或收敛速度的定量比较
3. 在非数学推理任务（如代码生成、对话）上的泛化能力未充分评估
4. 自适应裁剪机制引入了额外超参数（$\rho_0, \delta_1, \delta_2$，边界范围），尽管消融显示鲁棒性
5. 理论分析基于 tabular softmax 策略假设，实际深度神经网络中的行为可能有所偏差

### 7.3 开放问题

1. BAPO 的自适应裁剪机制能否与其他 RL 变体（如 PPO、REINFORCE）结合？
2. 正样本贡献阈值 $\rho_0$ 的最优值是否与任务难度、模型规模或数据陈旧度有关？
3. BAPO 在超长序列（如 agent 决策）或在线学习场景中的表现如何？
4. 熵-裁剪规则是否适用于其他裁剪机制（如 KL 惩罚）？
5. BAPO 能否与课程学习或数据筛选策略协同，进一步提升样本效率？

## 原文 PDF

![[paperPDFs/ICLR_2026/BAPO_Stabilizing_Off_Policy_Reinforcement_Learning_for_LLMs_via_Balanced_Policy_Optimization_with_Adaptive_Clipping.pdf]]
