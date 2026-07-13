---
title: "SPG: Sandwiched Policy Gradient for Masked Diffusion Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SPG_Sandwiched_Policy_Gradient_for_Masked_Diffusion_Language_Models.pdf
project_link: https://chenyuwang-monica.github.io/spg/
code_link: https://github.com/facebookresearch/SPG
openreview_forum_id: 18j5Q49GwN
aliases:
- SSPG
- SPG
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "使用上下界联合估计（夹层策略梯度）来替代不可算的对数似然，并通过块状掩码策略对齐训练与推断分布，从而减少策略梯度偏差并提升训练稳定性。"
primary_logic: "将组相对优势加权的对数似然目标替换为夹层目标：对正向优势最大化ELBO（下界），对负向优势最小化EUBO（上界），构建一个有效的下界代理目标。结合块状掩码生成扰动样本，使估计更贴近实际推理解码分布，实现更稳健的策略优化。"
claims:
- "SPG在四个推理基准上显著超越先前最优方法，在序列长度256下，GSM8K准确率提升3.6%，MATH500提升2.6%，Countdown提升18.4%，Sudoku提升27.0%。"
- "块状掩码策略在所有任务上一致优于随机掩码，验证了对齐训练-推断分布的重要性。"
- "混合似然估计（SPG w/ Mixture）比单独使用ELBO或EUBO效果更好，梯度范数更低、训练更稳定。"
- "SPG训练奖励上升更快且收敛水平更高，同时有效生成长度更短、更简洁的解。"
---

# SPG: Sandwiched Policy Gradient for Masked Diffusion Language Models

> [!tip] 核心洞察
> 将组相对优势加权的对数似然目标替换为夹层目标：对正向优势最大化ELBO（下界），对负向优势最小化EUBO（上界），构建一个有效的下界代理目标。结合块状掩码生成扰动样本，使估计更贴近实际推理解码分布，实现更稳健的策略优化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SPG：用于掩码扩散语言模型的夹层策略梯度 |
| 英文题名 | SPG: Sandwiched Policy Gradient for Masked Diffusion Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=18j5Q49GwN) · [GitHub](https://github.com/facebookresearch/SPG) · [Project](https://chenyuwang-monica.github.io/spg/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | SPG (Sandwiched Policy Gradient) |
| Dataset | GSM8K (0-shot, length 256), MATH500 (0-shot, Countdown (0-shot, Sudoku (3-shot |

> [!tip] 效果简介
> - GSM8K (0-shot, length 256) 上，准确率 为 86.1 (SPG w/ Mixture)，对比 82.5 (UniGRPO)，变化 +3.6。
> - MATH500 (0-shot, length 256) 上，准确率 为 40.0 (SPG w/ Mixture)，对比 37.4 (UniGRPO)，变化 +2.6。
> - Countdown (0-shot, length 256) 上，准确率 为 70.7 (SPG w/ Mixture)，对比 52.3 (WD1)，变化 +18.4。

## 概要

扩散语言模型（dLLM）在推理与对齐任务中展现出潜力，但其对数似然不可计算，导致标准策略梯度方法无法直接应用。现有强化学习（RL）方法普遍使用证据下界（ELBO）作为代用似然，然而ELBO仅为下界，无法有效利用负奖励对不良生成进行惩罚，引入显著偏差，限制了对齐效果的上限。

针对这一瓶颈，本文提出**夹层策略梯度（Sandwiched Policy Gradient, SPG）**。核心思路是用一个可计算的上下界联合估计来“夹住”不可算的真实对数似然：对正优势轨迹最大化ELBO（下界），对负优势轨迹最小化证据上界（EUBO），从而构建原策略优化目标的一个有效下界代理。同时，引入**块状掩码（block-wise masking）策略**替代传统的随机掩码，使蒙特卡洛估计中的扰动样本分布更贴近实际推理解码过程，进一步减少偏差并提升训练稳定性。

在四个数学与逻辑推理基准（GSM8K、MATH500、Countdown、Sudoku）上，SPG显著超越先前最优方法：在序列长度256设定下，GSM8K准确率提升3.6%，MATH500提升2.6%，Countdown提升18.4%，Sudoku提升27.0%。在编码任务HumanEval和MBPP上，SPG亦分别取得1.9%和4.7%的Pass@1增益。消融实验证实，混合似然估计（ELBO+EUBO）与块状掩码策略是性能提升的关键因素，且SPG在多种解码策略下均表现出强泛化性。



掩码扩散语言模型（Masked Diffusion Language Model, MDLM）通过逐步去噪生成文本，其训练依赖于最大化证据下界（ELBO）。然而，当将这类模型应用于强化学习（RL）后训练时，一个根本性瓶颈浮现：**扩散语言模型（dLLM）的真实对数似然 $\log \pi_\theta(x|c)$ 不可计算**，因为其生成过程涉及对大量潜在变量路径的积分。

标准的策略梯度方法（如 REINFORCE）要求计算 $\nabla_\theta \log \pi_\theta(x|c)$，但这在 dLLM 中无法直接获得。现有 RL 方法（如 **D1**（Zhao et al., 2025）、**WD1**（Tang et al., 2025））转而使用 ELBO 作为代用似然。ELBO 是真实对数似然的下界，这意味着：

- **对正奖励（优势）轨迹**：最大化 ELBO 等价于最大化真实对数似然的一个下界，方向正确但可能保守。
- **对负奖励（优势）轨迹**：ELBO 无法有效利用负奖励进行惩罚——因为 ELBO 仅是下界，最小化 ELBO 并不能保证真实对数似然被充分压低。这引入了显著的**估计偏差**，导致模型无法有效区分好样本与坏样本，限制了 RL 对齐的效果。

此外，现有方法在蒙特卡洛估计中普遍采用**随机掩码**策略来生成扰动样本。然而，dLLM 在实际推理时通常采用块状解码（block-wise decoding）或半自回归解码，随机掩码生成的训练分布与推理分布之间存在**分布不匹配**，进一步降低了策略梯度估计的准确性。

上述两个问题构成了当前 dLLM 强化学习后训练的核心瓶颈：**似然估计偏差**与**训练-推理分布错位**。本文的动机正是针对这两个缺口，提出一种能够有效利用负奖励信号、同时对齐训练与推理分布的策略梯度方法。



## 核心方法与创新机理

SPG 的核心创新在于解决了一个根本瓶颈：**扩散语言模型（dLLM）的真实对数似然 $\log\pi_\theta(x|c)$ 不可计算**，导致标准策略梯度方法无法直接应用。现有 RL 方法（如 D1、WD1）使用 ELBO 作为代用似然，但 ELBO 仅为下界，无法有效利用负奖励进行惩罚，引入显著偏差。SPG 通过两个关键的 **changed slots** 系统性地解决了这一问题。

### 1. 夹层似然估计：从单一 ELBO 到上下界联合

**基线做法：** 现有方法仅使用 ELBO（下界）作为似然估计，或直接忽略负优势轨迹。由于 $\mathcal{L}_{\mathrm{ELBO}} \leq \log\pi_\theta$，仅最大化下界意味着无法对负奖励样本施加有效惩罚——因为下界的最小化并不能保证真实似然的最小化。

**SPG 方案：** 构建“夹层目标”，对正负优势分别使用不同的界：
- **正优势轨迹**（$A^j \geq 0$）：最大化 ELBO（下界），这与传统做法一致；
- **负优势轨迹**（$A^j < 0$）：最小化 EUBO（证据上界），确保真实似然被有效压低。

具体而言，SPG 将组相对优势加权的对数似然目标替换为：

$$
\mathcal{I}_{\mathrm{SPG}}(\theta) = \mathbb{E}\left[\frac{1}{g}\sum_{j=1}^{g}\left(\mathbb{1}_{A^j\ge0}\cdot A^j\mathcal{L}_{\mathrm{ELBO}} + \mathbb{1}_{A^j<0}\cdot A^j\mathcal{L}_{\mathrm{EUBO}}\right)\right]
$$

由于 $\mathcal{L}_{\mathrm{ELBO}} \leq \log\pi_\theta \leq \mathcal{L}_{\mathrm{EUBO}}$，该目标构成原策略优化目标的一个**可计算下界**（Section 3.1），且允许任意优势值（包括负值），突破了基线方法对非负奖励的依赖。

**混合损失（Mixture）的进一步改进：** 在实践中，SPG 引入 ELBO 与 EUBO 的线性混合 $\tilde{\mathcal{L}}_{\mathrm{Mix}} = \omega\cdot\tilde{\mathcal{L}}_{\mathrm{EUBO}} + (1-\omega)\cdot\mathcal{L}_{\mathrm{ELBO}}$ 用于负优势估计。其梯度具有**置信度感知权重**：

$$
g_{\omega,k} = ((1-\omega)w(t,z_t) + \omega\rho_{\beta}) \partial_{\theta_k}\log\pi_{\theta}(x|z_t,c)
$$

对不确定 token 自动赋予小权重，防止梯度消失（Proposition 1）。消融实验（Table 3）表明，SPG w/ Mixture 在所有推理基准上一致优于单独使用 ELBO 或 EUBO，且梯度范数更低、训练更稳定（Figure 7）。

### 2. 块状掩码策略：对齐训练与推断分布

**基线做法：** 蒙特卡洛估计中采用随机掩码生成扰动样本，与推理解码时的半自回归生成分布存在显著差异。

**SPG 方案：** 采用**块状掩码（block-wise masking）**策略：将序列划分为若干块，随机选择一个块，其前部保持干净、后部全部掩码。这一设计模拟了半自回归解码中“逐块生成”的模式，使训练过程中的蒙特卡洛采样分布更贴近实际推理分布。

消融实验（Table 4, Table 11）表明，块状掩码在所有任务上一致优于随机掩码——在 Countdown 上为 SPG w/ EUBO 带来 +23.9 的准确率提升，在 Sudoku 上亦有大幅增益。更重要的是，使用块状掩码训练的模型对多种解码策略（不同块大小、随机/置信解码、全序列解码）均展现出强泛化性（Figure 6, Table 17），验证了对齐训练-推断分布的关键作用。

### 3. EUBO 的紧致性设计

SPG 的 EUBO 基于 Rényi 变分界推导，在连续时间极限下形式为：

$$
\tilde{\mathcal{L}}_{\mathrm{EUBO}}(x_{1:n};\theta) = \frac{1}{\beta}\sum_{i=1}^{n}\log\mathbb{E}_{t,z_t}\left[w(t)\cdot\mathbb{1}(z_{t,i}=m)\cdot\pi_{\theta}^{\beta}(x_i|z_t)\right]
$$

其中 $\beta \geq 1$ 控制上界的紧致程度。实验表明，使用更紧的有偏上界（EUBO）优于基于 $\log x \leq x-1$ 的宽松无偏上界（Table 14），说明**估计紧致性比无偏性对策略优化更重要**。

综上，SPG 通过**夹层似然估计**和**块状掩码**这两个 changed slots，在不增加计算开销的前提下（每次梯度更新约 0.49–0.51 分钟，8×A100），系统性解决了 dLLM 中似然不可算导致的策略梯度偏差问题，在数学推理（GSM8K +3.6%、MATH500 +2.6%、Countdown +18.4%、Sudoku +27.0%）和代码生成（HumanEval +1.9%、MBPP +4.7%）任务上均取得显著提升（Table 1, Table 2）。



![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_18j5Q49GwN/figures/005_Figure_2.jpg]]
*Figure 2: The training process of SPG for MDLM. Left: From a prompt c, we generate responses $\{ \bar { \pmb { x } ^ { j } } \} _ { j = 1 } ^ { g }$ . We then maximize a lower bound on the likelihood $\pi _ { \pmb { \theta } } ( \bar { \pmb x } ^ { j } \mid \bar { \pmb c }$ ) for high-reward responses while minimizing an upper bound for low-reward ones. Right: The upper/lower bound of likelihood is estimated via Monte Carlo using a block-wise masking strategy, where a random block is selected for masking, with earlier blocks kept clean and later blocks fully masked. The example shows a sequence of length 9 with a block size of 3, where the current generation block is highlighted in yellow

SPG（Sandwiched Policy Gradient）是一种面向掩码扩散语言模型（MDLM）的强化学习后训练方法。其核心挑战在于：扩散语言模型的对数似然 $\log \pi_\theta(x|c)$ 不可直接计算，导致标准策略梯度估计器无法直接应用。现有方法（如 D1）使用 ELBO 作为代用似然，但 ELBO 仅为下界，无法有效利用负奖励信号进行惩罚，引入显著偏差。

SPG 的整体 pipeline 由四个模块串联构成，形成“采样→扰动→估计→更新”的闭环：

### 模块一：组采样与奖励计算

对于每个输入提示 $c$，从当前策略 $\pi_{\text{sg}[\theta]}$（停止梯度）采样 $g$ 个完整响应序列 $\{x^j\}$。随后计算每个响应的**组相对优势**：

$$A^j(c, x^j) = R(c, x^j) - \frac{1}{g}\sum_{\jmath=1}^{g} R(c, \tilde{x}^{\jmath})$$

该优势值以组内平均奖励为基线，正优势表示该响应优于组内平均，负优势反之。这一设计使得 SPG 需要同时处理正、负两类优势信号，而 ELBO 仅能在最大化方向提供有效梯度——这正是后续夹层目标设计的直接动因。

### 模块二：块状掩码生成

对每个完成序列 $x^j$，采用**块状掩码策略**生成 $m$ 个扰动样本用于蒙特卡洛估计。具体而言，将序列划分为若干连续块，随机选择一个块边界，将该块之前的所有 token 保持干净，该块及之后的所有 token 全部替换为 `[MASK]`。这一策略旨在对齐训练阶段的掩码分布与实际推理时的半自回归解码分布，从而减少分布偏移带来的估计偏差。

### 模块三：夹层目标构建与梯度计算

这是 SPG 的核心创新。对于正优势轨迹（$A^j \geq 0$），最大化 ELBO（证据下界）；对于负优势轨迹（$A^j < 0$），最小化 EUBO（证据上界）或其与 ELBO 的混合。目标函数为：

$$\mathcal{I}_{\mathrm{SPG}}(\theta) = \mathbb{E}\left[\frac{1}{g}\sum_{j=1}^{g}\left(\mathbb{1}_{A^j\ge0}\cdot A^j\mathcal{L}_{\mathrm{ELBO}}(x^j|c;\theta) + \mathbb{1}_{A^j<0}\cdot A^j\tilde{\mathcal{L}}(x^j|c;\theta)\right)\right]$$

其中 $\tilde{\mathcal{L}}$ 可为纯 EUBO（SPG w/ EUBO）或 ELBO 与 EUBO 的混合（SPG w/ Mixture）：

$$\tilde{\mathcal{L}}_{\mathrm{Mix}}(x|c;\theta) = \omega\cdot\tilde{\mathcal{L}}_{\mathrm{EUBO}}(x|c;\theta) + (1-\omega)\cdot\mathcal{L}_{\mathrm{ELBO}}(x|c;\theta)$$

由于 $\mathcal{L}_{\mathrm{ELBO}} \leq \log \pi_\theta \leq \tilde{\mathcal{L}}_{\mathrm{EUBO}}$，该夹层目标构成了原组策略优化目标的一个**可计算下界**，从而保证优化方向的合理性。混合梯度的一个关键性质是**置信度感知加权**：对模型预测置信度低的 token 自动赋予较小权重，有效缓解梯度消失问题。

### 模块四：策略更新

使用模块三计算得到的梯度直接更新策略参数 $\theta$。SPG 未引入重要性采样、策略裁剪或 KL 正则化等额外稳定技术，保持了方法的简洁性。

### 输入输出流总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| 组采样 | 提示 $c$，策略 $\pi_{\text{sg}[\theta]}$ | $g$ 个响应序列及组相对优势 |
| 块状掩码 | 完整序列 $x^j$ | $m$ 个块状掩码的扰动样本 |
| 夹层目标 | 扰动样本，优势值 $A^j$ | SPG 目标梯度 |
| 策略更新 | 梯度 | 更新后的策略参数 $\theta$ |

该方法的关键设计决策——夹层估计与块状掩码——共同解决了扩散语言模型 RL 训练中的两个核心瓶颈：不可算似然下的有效梯度估计，以及训练-推断分布失配。



### 问题形式化：组相对优势目标

SPG的出发点是将扩散语言模型的策略优化表述为**组相对优势加权的对数似然最大化**。给定提示 $c$，从当前策略 $\pi_{\theta}$ 中采样 $g$ 个完成序列 $\{x^j\}_{j=1}^g$，计算每个序列的组相对优势：

$$A^j(c, x^j) := R(c, x^j) - \frac{1}{g}\sum_{\jmath=1}^{g} R(c, \tilde{x}^{\jmath})$$

其中 $R(c, x)$ 为奖励函数（如答案正确性）。策略梯度目标可重写为优势加权形式：

$$\mathcal{I}^{\mathrm{group}}(\theta) = \mathbb{E}_{c,\{x^j\}\sim\pi_{\mathrm{sg}[\theta]}}\left[\frac{1}{g}\sum_{j=1}^{g}A^j(x^j,c)\log\pi_{\theta}(x^j|c)\right]$$

**核心瓶颈**：扩散语言模型的对数似然 $\log\pi_{\theta}(x|c)$ 不可直接计算，标准策略梯度无法直接应用。

---

### 核心模块一：夹层目标（Sandwiched Objective）

SPG的核心创新是用**可计算的上下界替代不可算的对数似然**，构建一个原目标的有效下界。

**正优势轨迹**（$A^j \geq 0$）：最大化 ELBO（证据下界），该下界来自掩码扩散模型的预训练目标：

$$\mathcal{L}_{\mathrm{ELBO}}(x;\theta) = \mathbb{E}_{t,z_t}\left[\sum_{i=1}^{n} w(t)\cdot\mathbb{1}(z_{t,i}=m)\cdot\log\pi_{\theta}(x_i|z_t)\right]$$

其中 $w(t)$ 为时间步权重，$z_t$ 为时刻 $t$ 的掩码序列，$m$ 表示 [MASK] token。

**负优势轨迹**（$A^j < 0$）：最小化 EUBO（证据上界），迫使模型降低不利序列的生成概率。EUBO 基于 Rényi 变分界推导，其连续时间形式为：

$$\tilde{\mathcal{L}}_{\mathrm{EUBO}}(x_{1:n};\theta) = \frac{1}{\beta}\sum_{i=1}^{n}\log\mathbb{E}_{t,z_t}\left[w(t)\cdot\mathbb{1}(z_{t,i}=m)\cdot\pi_{\theta}^{\beta}(x_i|z_t)\right]$$

其中 $\beta$ 控制上界的紧度（$\beta$ 越大，界越紧）。

**夹层目标**将两者统一：

$$\mathcal{I}_{\mathrm{SPG}}(\theta) = \mathbb{E}\left[\frac{1}{g}\sum_{j=1}^{g}\left(\mathbb{1}_{A^j\ge0}\cdot A^j\mathcal{L}_{\mathrm{ELBO}}(x^j|c;\theta) + \mathbb{1}_{A^j<0}\cdot A^j\mathcal{L}_{\mathrm{EUBO}}(x^j|c;\theta)\right)\right]$$

由于 $\mathcal{L}_{\mathrm{ELBO}} \leq \log\pi_{\theta} \leq \mathcal{L}_{\mathrm{EUBO}}$，有 $\mathcal{I}_{\mathrm{SPG}}(\theta) \leq \mathcal{I}^{\mathrm{group}}(\theta)$，即 SPG 目标是原目标的一个**可计算下界**，最大化该下界构成有效的代理优化。

---

### 核心模块二：混合似然估计（Mixture Likelihood）

实践中，单独使用 EUBO 处理负优势轨迹存在估计偏差（因对数置于期望之外）。SPG 进一步引入 **ELBO 与 EUBO 的线性混合**作为更稳定的似然近似：

$$\tilde{\mathcal{L}}_{\mathrm{Mix}}(x|c;\theta) := \omega\cdot\tilde{\mathcal{L}}_{\mathrm{EUBO}}(x|c;\theta) + (1-\omega)\cdot\mathcal{L}_{\mathrm{ELBO}}(x|c;\theta)$$

其中 $\omega \in [0,1]$ 为混合系数（实验中固定为 0.5）。

该混合损失的梯度具有**置信度感知权重**特性：

$$g_{\omega,k} = ((1-\omega)w(t,z_t) + \omega\rho_{\beta}) \partial_{\theta_k}\log\pi_{\theta}(x|z_t,c)$$

其中 $\rho_{\beta}$ 为由 $\pi_{\theta}^{\beta}$ 导出的权重项。**关键性质**：对模型预测置信度低的 token，$\pi_{\theta}^{\beta}(x_i|z_t)$ 较小，对应权重自动降低，避免梯度消失；对高置信度 token 则赋予更大权重。这一自适应机制提升了训练稳定性（见 Figure 7，SPG w/ Mixture 梯度范数更低）。

---

### 核心模块三：块状掩码策略（Block-wise Masking）

蒙特卡洛估计 ELBO/EUBO 时需对序列施加掩码。现有方法使用**随机掩码**，与推理时的自回归式解码分布不匹配。

SPG 采用**块状掩码**：将序列划分为若干块，随机选择一个块边界，保留该块之前的所有 token 为干净状态，将该块之后的所有 token 全部替换为 [MASK]。这一策略模拟了半自回归解码的生成过程，使训练时的掩码分布与推理时的解码分布对齐。

实验证据（Table 4, Table 11）：块状掩码在所有推理基准上一致优于随机掩码，在 Countdown 上对 SPG w/ EUBO 带来 +23.9 的绝对准确率提升，验证了分布对齐的关键作用。

---

### 训练流程总览

SPG 的完整训练迭代（Algorithm 1）包含四个步骤：

1. **组采样与奖励计算**：对每个提示生成 $g$ 个完成序列，计算组相对优势。
2. **块状掩码生成**：对每个完成序列，采用块状掩码策略生成 $m$ 个扰动样本用于蒙特卡洛估计。
3. **夹层目标构建与梯度计算**：根据优势正负分别选择 ELBO 或混合损失（EUBO+ELBO）构建 SPG 目标，计算梯度。
4. **策略更新**：使用计算得到的梯度更新策略参数 $\theta$。



## 实验与关键发现

### 核心瓶颈与评估逻辑

扩散语言模型（dLLM）的对数似然无法解析计算，使得标准策略梯度方法无法直接应用。已有RL方法（如D1、WD1）使用ELBO作为代用似然，但ELBO仅为下界，当优势为负时无法有效惩罚不良轨迹——最大化下界等价于最大化一个比真实似然更小的量，这导致负奖励信号被严重削弱，策略优化引入显著偏差。SPG的核心设计正是针对这一瓶颈：通过引入EUBO（证据上界），为负优势轨迹构建一个可计算的上界，使策略梯度能够有效区分正负反馈。实验评估围绕三个关键问题展开：

1. **夹层目标是否比单一ELBO更有效？** ——验证混合似然估计（SPG w/ Mixture）能否减少策略梯度偏差。
2. **块状掩码是否优于随机掩码？** ——验证训练-推断分布对齐是否影响最终性能。
3. **SPG在不同任务和解码策略下是否具有鲁棒性？** ——验证方法的泛化能力。

所有评估均使用LLaDA-8B-Instruct作为基础模型，在半自回归置信解码（块大小32，温度0.0，去噪步数为序列长度一半）下进行。RL方法均采用基于验证集准确率的最优检查点选择，D1和WD1使用官方代码复现且排除额外SFT阶段以确保公平比较。

---

### 主实验结果

**Table 1** 展示了SPG与基线方法在四个数学和逻辑推理基准上的测试准确率。SPG w/ Mixture在所有任务和生成长度下均取得最优结果：

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_18j5Q49GwN/figures/006_Table_1.jpg]]
*Table 1: Model performance on four reasoning benchmarks. The best results are bolded and the second best are underlined. SPG consistently outperforms all other methods. We denote the absolute gain of test accuracy to the previous state-of-the-art in green*

| 基准 | 最优基线方法 | 基线准确率 | SPG w/ Mixture | 绝对提升 |
|------|-------------|-----------|----------------|---------|
| GSM8K (256) | UniGRPO | 82.5 | **86.1** | +3.6 |
| MATH500 (256) | UniGRPO | 37.4 | **40.0** | +2.6 |
| Countdown (256) | WD1 | 52.3 | **70.7** | +18.4 |
| Sudoku (256) | UniGRPO | 67.0 | **94.0** | +27.0 |

在Countdown和Sudoku上的巨大增益（+18.4和+27.0个百分点）表明，当任务具有明确的结构化约束和可验证性时，SPG的上下界联合估计能够更有效地利用负奖励信号进行策略修正。相比之下，MATH500上的增益相对有限（+2.6），这暗示基础模型能力与任务难度本身可能是主要瓶颈，单纯优化RL目标难以突破预训练能力的上限。

在编码任务上（**Table 2**），SPG w/ Mixture同样取得最优：HumanEval Pass@1达到41.5（+1.9 over WD1），MBPP Pass@1达到50.6（+4.7 over UniGRPO）。编码任务的增益幅度小于逻辑推理任务，这与编码任务对生成长度和格式的敏感度更高有关。

**Figure 3** 的训练奖励曲线进一步验证了SPG的优化效率：SPG w/ Mixture的奖励上升速度显著快于D1、WD1和UniGRPO，且收敛水平更高。这表明夹层目标不仅提升了最终性能，也加速了策略优化的收敛过程。

---

### 消融实验

#### 混合似然估计的有效性

**Table 3** 对比了四种负优势轨迹似然估计方法：仅用ELBO、仅用EUBO、SPG w/ Mixture（混合ELBO和EUBO）、以及忽略负优势轨迹。SPG w/ Mixture在所有四个推理基准上一致最优，相比仅用ELBO的版本，GSM8K提升2.2个百分点，Countdown提升2.4个百分点，Sudoku提升3.0个百分点。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_18j5Q49GwN/figures/009_Table_3.jpg]]
*Table 3: Ablations on log-likelihood estimation methods for negative advantage traces. The best results are bolded and the second best underlined. We denote the absolute gain of test accuracy to SPG w/ ELBO in green. SPG w/ Mixture consistently outperforms other likelihood estimation methods. Table 4: Ablations on the masking strategies in Monte Carlo estimation. We denote the absolute gain of test accuracy to random masking for each model in green. Our block-wise masking strategy leads to consistent improvement to random masking on both benchmarks*

这一结果验证了核心洞察：**正优势最大化下界、负优势最小化上界**的组合策略优于任何单一估计。仅用ELBO无法有效惩罚负轨迹（因为ELBO ≤ log π，惩罚效果被低估），仅用EUBO则在正优势侧引入不必要的上界松弛。混合估计在两者之间取得平衡。

**Figure 7** 的梯度范数动态提供了训练稳定性层面的解释：SPG w/ Mixture的梯度范数显著低于仅用ELBO或EUBO的版本，表明混合估计减少了梯度震荡，使优化更加平稳。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_18j5Q49GwN/figures/021_Figure_7.jpg]]
*Figure 7: Dynamics of the gradient norm of models trained with different log-likelihood estimation methods. SPG w/ Mixture achieves lower gradient norm and more stable optimization. We report mean and standard deviation over a rolling window of 50 steps*

#### 块状掩码策略

**Table 4** 展示了掩码策略的消融结果。块状掩码在所有任务上一致优于随机掩码，其中在Countdown上的增益最为显著：SPG w/ EUBO从45.4跃升至69.3（+23.9），SPG w/ Mixture从62.0提升至69.9（+7.9）。

这一结果的因果机制在于：训练时使用块状掩码生成扰动样本，其分布更贴近半自回归解码的实际推理过程（推理时模型逐块去噪）。随机掩码产生的样本分布与推理分布存在系统性偏差，导致策略梯度估计的方差增大。块状掩码通过对齐训练-推断分布，减少了这种偏差，使策略优化更加有效。

#### 上界紧度与混合系数

**Table 14** 对比了紧上界（EUBO，基于Rényi变分界）与松上界（基于log x ≤ x-1的无偏上界）。紧上界在MATH500和Countdown上均优于松上界（如β=1.0时平均35.7 vs 34.7），验证了**有偏紧界优于无偏松界**的实践原则——偏差的代价小于方差增大的代价。

**Figure 5** 展示了超参数β和ω的敏感性分析。β=1.0在多数任务中效果最优，β过大（>2.0）会导致上界过松而性能下降。混合系数ω在0.5附近表现稳健，表明ELBO和EUBO的等权重混合是一个安全且有效的默认选择。

#### 推理策略鲁棒性

**Figure 6** 和 **Table 17** 展示了SPG在不同推理策略下的泛化能力。无论采用何种解码顺序（半自回归不同块大小、全序列解码）和去掩码策略（置信解码、随机解码），SPG均大幅超越所有基线方法。这验证了块状掩码训练策略的有效性：模型在训练期间已接触到多种掩码分布，因此对推理策略的变化具有天然的鲁棒性。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_18j5Q49GwN/figures/018_Figure_6.jpg]]
*Figure 6: Ablations on inference strategies, including different combinations of decoding orders ( $\mathrm { i . e . }$ semi-autoregressive (semi-AR) decoding with varying block sizes and full sequence decoding) and unmasking approaches (i.e., confidence-based and random unmasking). We set generation length to 256 and report the average accuracy across four benchmarks. SPG consistently outperforms all baselines by a large margin across different inference strategies*

---

### 失败模式与局限

1. **MATH500增益有限**：尽管SPG在MATH500上取得2.6个百分点的提升，但绝对准确率仍仅为40.0%。这表明对于高难度数学推理任务，RL后训练的增益受限于基础模型的推理能力。SPG无法弥补预训练阶段的能力缺口。

2. **EUBO的蒙特卡洛偏差**：由于对数置于期望之外（Jensen不等式），EUBO的蒙特卡洛估计存在理论偏差。虽然实验表明有偏紧界优于无偏松界，但偏差对梯度方向的影响尚未量化分析，可能在极端情况下导致错误更新。

3. **超参数固定**：混合系数ω和紧度参数β作为固定超参数，未采用自适应调节。在训练动态变化时（如奖励分布漂移），固定参数可能无法持续保持最优。

4. **计算开销未减少**：尽管SPG在性能上显著提升，但每次梯度更新的计算时间与基线方法相近（约0.49-0.51分钟/步，8×A100 GPU），块状掩码未引入额外开销但也未减少开销。增加蒙特卡洛样本数（m=4）可进一步提升性能（**Table 20**），但相应地增加计算负担。

5. **任务覆盖范围有限**：当前实验仅覆盖推理和编码任务，在对话、安全对齐等更复杂的开放式任务上的有效性有待验证。SPG使用的简单策略梯度公式未引入重要性采样、裁剪或KL正则化等常用RL稳定技术，可能在更复杂环境中面临训练不稳定问题。

---

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|---------|
| Table 1 | SPG w/ Mixture在四个推理基准上全面超越先前最优方法，Countdown和Sudoku增益尤为显著 |
| Table 2 | SPG在编码任务上同样取得最优，但增益幅度小于推理任务 |
| Table 3 | 混合似然估计（ELBO+EUBO）一致优于单一估计，验证夹层目标的必要性 |
| Table 4 | 块状掩码一致优于随机掩码，Countdown上增益达+23.9，验证训练-推断分布对齐的重要性 |
| Figure 3 | SPG收敛更快、奖励更高，验证夹层目标的优化效率 |
| Figure 7 | SPG w/ Mixture梯度范数更低，训练更稳定 |
| Figure 6 | SPG在多种推理策略下均大幅超越基线，展示强泛化性 |
| Table 14 | 有偏紧上界优于无偏松上界，偏差代价小于方差代价 |

### 补充图表

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_18j5Q49GwN/figures/032_Table_11.jpg]]
*Table 11: Ablations on the masking strategies in Monte Carlo estimation. Our block-wise masking strategy leads to consistent improvement to random masking on both benchmarks*



## 定位与知识库关联

### 问题定位：扩散语言模型的策略梯度困境

扩散语言模型（dLLM）的核心瓶颈在于其对数似然 $\log \pi_\theta(x|c)$ 不可直接计算——这是由离散扩散过程中多次掩码-去掩码迭代导致的边缘化难题。对于自回归语言模型，标准策略梯度（REINFORCE）可直接利用对数似然进行优势加权更新；但在dLLM中，这一路径被阻断。

现有RL方法对此问题的处理策略可分为两条路线：

1. **ELBO替代路线**：**D1**（Zhao et al., 2025）和**UniGRPO**（Yang et al., 2025）直接使用证据下界（ELBO）作为对数似然的代用值。由于 $\mathcal{L}_{\mathrm{ELBO}} \leq \log \pi_\theta$，ELBO仅为下界，导致一个根本性缺陷：当优势为负时，最大化 $-A^j \cdot \mathcal{L}_{\mathrm{ELBO}}$ 实际上在**最大化**一个下界，而非真正惩罚负优势轨迹，引入系统性偏差。这迫使D1/UniGRPO只能处理非负奖励，或通过奖励偏移（reward shifting）将负奖励转为正奖励，但奖励偏移本身会扭曲优化信号（Table 7已验证其效果劣于SPG）。

2. **轨迹级优化路线**：**StepWise**（Huang et al., 2025）从轨迹级更新角度切入，但Table 6显示其在MATH500和Countdown上均不及SPG。

**WD1**（Tang et al., 2025）采用基于权重扩散的RL方案，在Countdown上达到52.3%的准确率，但在数学推理（GSM8K 78.5%，MATH500 35.2%）和代码任务上整体弱于SPG。

SPG的关键突破在于：不再回避负优势问题，而是通过**夹层目标**（sandwiched objective）同时利用上下界来处理正负优势轨迹。

### SPG的方法学贡献

SPG的四个核心改动槽位及其与基线的对比：

| 改动槽位 | 基线做法 | SPG做法 | 证据锚点 |
|----------|---------|---------|---------|
| 负优势似然估计 | 仅使用ELBO（下界）或忽略负优势 | 使用EUBO（上界）或ELBO-EUBO混合 | Section 3.1, Equation 5 |
| 蒙特卡洛掩码策略 | 随机掩码 | 块状掩码（block-wise masking） | Section 3.3, Table 4 |
| 似然估计权重 | 固定权重 $w(t)$ | 置信度感知权重（confidence-aware weighting） | Equation 9, Proposition 1 |
| 奖励值约束 | 要求非负奖励 | 允许任意优势值（含负数） | Section 3.1, Algorithm 1 |

**夹层目标的数学逻辑**：SPG从组相对优势目标出发

$$\mathcal{I}^{\mathrm{group}}(\theta) = \mathbb{E}_{c,\{x^j\}\sim\pi_{\mathrm{sg}[\theta]}}\left[\frac{1}{g}\sum_{j=1}^{g}A^j(x^j,c)\log\pi_{\theta}(x^j|c)\right]$$

由于 $\mathcal{L}_{\mathrm{ELBO}} \leq \log \pi_\theta \leq \mathcal{L}_{\mathrm{EUBO}}$，SPG构造了一个可计算的下界代理目标：

$$\mathcal{I}_{\mathrm{SPG}}(\theta) = \mathbb{E}\left[\frac{1}{g}\sum_{j=1}^{g}\left(\mathbb{1}_{A^j\ge0}\cdot A^j\mathcal{L}_{\mathrm{ELBO}} + \mathbb{1}_{A^j<0}\cdot A^j\mathcal{L}_{\mathrm{EUBO}}\right)\right]$$

该目标满足 $\mathcal{I}_{\mathrm{SPG}}(\theta) \leq \mathcal{I}^{\mathrm{group}}(\theta)$，因此最大化SPG目标构成对原目标的合法优化。

**EUBO的构造**：EUBO源自Rényi变分界，在连续时间极限下简化为

$$\tilde{\mathcal{L}}_{\mathrm{EUBO}}(x_{1:n};\theta) = \frac{1}{\beta}\sum_{i=1}^{n}\log\mathbb{E}_{t,z_t}\left[w(t)\cdot\mathbb{1}(z_{t,i}=m)\cdot\pi_{\theta}^{\beta}(x_i|z_t)\right]$$

其中 $\beta \geq 1$ 控制上界的紧度。Table 12的消融显示 $\beta=1.0$ 在多数任务中效果最优。值得注意的是，EUBO因对数置于期望之外，其蒙特卡洛估计存在Jensen不等式引入的偏差；但Table 14表明，有偏的紧上界（EUBO）仍优于使用 $\log x \leq x-1$ 构造的无偏宽松上界，后者因与真实对数似然差距过大而性能下降。

**混合损失与置信度感知权重**：为兼顾估计稳定性与紧致性，SPG对负优势轨迹采用混合损失

$$\tilde{\mathcal{L}}_{\mathrm{Mix}}(x|c;\theta) = \omega\cdot\tilde{\mathcal{L}}_{\mathrm{EUBO}}(x|c;\theta) + (1-\omega)\cdot\mathcal{L}_{\mathrm{ELBO}}(x|c;\theta)$$

其梯度具有置信度感知特性：

$$g_{\omega,k} = ((1-\omega)w(t,z_t) + \omega\rho_{\beta}) \partial_{\theta_k}\log\pi_{\theta}(x|z_t,c)$$

该权重机制对不确定token赋予小权重，有效防止梯度消失。Figure 7显示SPG w/ Mixture的梯度范数更低、优化更稳定。消融实验（Table 3, Table 10）一致表明混合估计在所有推理基准上优于单独使用ELBO或EUBO。

**块状掩码策略**：SPG采用块状掩码替代随机掩码进行蒙特卡洛估计，将序列划分为若干块，随机选择一个块，其前序块保持干净、后续块全部掩码。这一设计的动机是对齐训练时的扰动分布与推断时的解码分布。Table 4和Table 11的消融显示，块状掩码在Countdown上为SPG w/ EUBO带来+23.9的绝对提升，在Sudoku上带来+13.0的提升，在所有任务上一致优于随机掩码。Figure 6进一步表明，使用块状掩码训练的模型对多种解码策略（不同块大小、半自回归/全序列解码、置信/随机解码）均展现出强泛化性（Table 17）。

### 适用边界与局限

**已验证的适用边界**：
- 模型架构：LLaDA-8B（基于掩码扩散的语言模型）
- 任务类型：数学推理（GSM8K, MATH500）、逻辑推理（Countdown, Sudoku）、代码生成（HumanEval, MBPP）
- 序列长度：128/256/512 tokens
- 解码策略：半自回归置信解码、随机解码、全序列解码（Table 17, Figure 6）
- 微调方式：LoRA（Table 18显示全参数微调结果类似）

**已知局限**：

1. **EUBO估计偏差**：EUBO的蒙特卡洛估计因对数置于期望之外而存在偏差。虽然实验证明有偏紧界优于无偏松界（Table 14），但偏差对策略优化的精确影响尚未量化。

2. **模型架构依赖**：当前SPG专为掩码扩散语言模型（MDLM）设计，对其他离散扩散模型（如吸收态扩散）的适用性待验证。论文未在非掩码扩散架构上进行实验。

3. **RL稳定技术缺失**：SPG使用简单策略梯度公式，未引入重要性采样、策略裁剪或KL散度正则化等常用RL稳定技术。这可能限制其在更复杂奖励环境中的表现。

4. **超参数固定**：混合系数 $\omega=0.5$ 和紧度参数 $\beta$（从 {1.0, 1.5, 2.0} 中选取）作为固定超参数，未采用自适应调节。Figure 5显示 $\omega \in [0,1]$ 和 $\beta \geq 1$ 的较宽范围内性能稳健，但自适应调节可能进一步释放潜力。

5. **任务增益不均衡**：在MATH500上增益（+2.6%）相对有限，远小于Countdown（+18.4%）和Sudoku（+27.0%），暗示基础模型能力与任务特性可能构成瓶颈。

6. **蒙特卡洛样本数**：默认使用 $m=1$ 个扰动样本；Table 20显示增加至 $m=4$ 可在Countdown上获得额外提升，但计算开销同步增加。当前实验未探索 $m>4$ 的扩展性。

### 开放问题

1. **RL稳定技术的整合**：如何正确地将重要性采样、策略裁剪和KL散度正则化等标准RL稳定技术整合到dLLM的SPG框架中，而不破坏夹层目标的界保证？

2. **架构推广**：SPG能否推广到连续时间扩散或全序列扩散模型，而不限于掩码扩散？EUBO的推导依赖掩码扩散的特定前向过程，推广需要重新推导上界形式。

3. **偏差进一步缩减**：能否通过RLOO（REINFORCE Leave-One-Out）等方法进一步减少策略更新目标中的偏差？SPG当前使用组相对优势，与RLOO的思路存在结合空间。

4. **自适应超参数**：自适应调整 $\beta$ 和 $\omega$ 参数（如基于训练过程中的奖励信号或梯度范数）是否能进一步提升训练效率和最终性能？

5. **长序列与大规模扩展**：在更长的序列生成（>512 tokens）或更大规模模型（>8B参数）上，SPG的扩展性与稳定性如何？块状掩码策略的块大小是否需要随序列长度动态调整？

6. **与其他对齐技术的协同**：SPG与偏好优化方法（如LLaDA-1.5使用的VRPO）是否存在互补性？两者能否在统一框架下结合？



## 原文 PDF

![[paperPDFs/ICLR_2026/SPG_Sandwiched_Policy_Gradient_for_Masked_Diffusion_Language_Models.pdf]]
