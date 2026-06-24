---
title: "Keep the Best, Forget the Rest: Reliable Alignment with Order-Aware Preference Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Keep_the_Best_Forget_the_Rest_Reliable_Alignment_with_Order_Aware_Preference_Optimization.pdf
aliases:
- KBFRRAOAPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/batch_offline
core_operator: "通过在每批中根据参考对齐得分和即时损失筛选掉最高损失的部分未对齐样本，控制梯度方差并收紧泛化界。"
primary_logic: "通过参考策略的对齐程度识别和暂时排除最模糊的训练对，RAPPO在不牺牲参考指导的前提下提高了训练的稳定性和泛化性能。"
claims:
- "RAPPO achieves a tighter generalization bound than standard DPO."
- "RAPPO improves reward score by 3.5%, 1.1%, and 7.1% across three SFT model sizes on IMDb, compared to DPO."
- "RAPPO reduces toxicity to as low as 2.28% compared to 6.30% for the best baseline on Real-Toxicity-Prompts."
- "RAPPO surpasses SIMPO and DPO under GPT-4 evaluation, achieving win rates of 58.8% and 74.5%, respectively."
---

# Keep the Best, Forget the Rest: Reliable Alignment with Order-Aware Preference Optimization

> [!tip] 核心洞察
> 通过参考策略的对齐程度识别和暂时排除最模糊的训练对，RAPPO在不牺牲参考指导的前提下提高了训练的稳定性和泛化性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 保留最佳，遗忘其余：基于顺序感知偏好优化的可靠对齐 |
| 英文题名 | Keep the Best, Forget the Rest: Reliable Alignment with Order-Aware Preference Optimization |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=LrHfYPFTtg); [GitHub](https://github.com/pxyWaterMoon/rappo) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/batch_offline |
| Method | RAPPO |
| Dataset | IMDB Sentiment Control, Real-Toxicity-Prompts, Text Summarization (GPT-4 evaluation), PKU-SafeRLHF |

> [!tip] 效果简介
> - IMDB Sentiment Control 上，Reward Score ↑ 为 1.6811 (RAPPO-4)，对比 1.5537 (SimPO)，变化 +0.1274 (8.2%)。
> - Real-Toxicity-Prompts 上，Toxicity % ↓ 为 2.28% (RAPPO-4)，对比 6.30% (DPO)，变化 -4.02%。
> - Text Summarization (GPT-4 evaluation) 上，Win Rate vs DPO 为 74.5%，对比 50.0% (parity)，变化 +24.5%。

## 概述

大语言模型对齐的核心挑战之一是如何利用人类偏好信号稳定地优化策略。标准直接偏好优化（DPO）虽然避免了显式奖励建模，却对参考策略的假设高度敏感：当参考策略本身与人类偏好不一致时，偏好数据集中大量“模糊”的对比对会主导梯度信号，导致训练不稳定并扩大泛化误差。这一瓶颈源于DPO隐式奖励函数对参考策略对数比值的依赖——不可靠的参考锚点使得模型难以区分真正可信的偏好样本。

针对该问题，本文提出顺序感知的偏好优化方法**RAPPO**（**R**eliable **A**lignment with **O**rder-Aware **P**reference **O**ptimization）。RAPPO在每步训练中对小批次样本进行对齐性评分，依据参考策略在选中/拒绝响应上的概率比将样本划分为对齐子集和未对齐子集，然后从未对齐样本中按即时损失排序，**暂时丢弃损失最大的少量样本**，仅用保留的对齐样本和筛选后的未对齐样本执行参数更新。该方法通过“保留最佳、遗忘其余”的策略，在维持参考指导的同时，降低了未对齐样本引入的梯度方差，从而在理论上收紧泛化界，且**不永久删除任何样本**——随着模型改善，被丢弃的样本可重新进入训练。RAPPO仅需少量代码修改即可嵌入现有DPO类算法，额外训练时间约为25%，保持实用性。

核心结论与主要结果：
- **理论保证**：RAPPO建立起比标准DPO更紧的泛化界，其顺序感知的删除机制通过减少高损失样本对梯度的干扰，提高了参数更新的稳定性。
- **广泛任务超越**：在IMDb情感控制、Real‑Toxicity‑Prompts毒性缓解、文本摘要以及PKU‑SafeRLHF安全对齐四个基准上，RAPPO一致且显著地优于DPO、SimPO、KTO、ORPO、R‑DPO等多种基线。例如，情感奖励得分提升最高达7.7%，毒性率降至2.28%（相比最佳基线6.30%），GPT‑4评估下对DPO与SimPO的胜率分别达到74.5%和58.8%，安全率与帮助性指标亦全面领先。
- **鲁棒性与效率**：超参数敏感性实验表明RAPPO对对齐阈值和丢弃数量稳健；额外的排序与筛选开销可控，适合实际部署。

综上，RAPPO为基于参考策略的偏好优化提供了一种简单而有效的顺序感知修正，缓解了参考偏差带来的泛化退化，在多个层面推进了语言模型与人类偏好的可靠对齐。

（注：该方法尚未在超大规模（>8B）模型上充分验证，理论分析依赖于光滑性与Lipschitz假设，未来可扩展自适应丢弃策略并探索与其他对齐范式的结合。）

## 背景与动机

大规模语言模型对齐的主流范式之一是通过人类偏好数据进行微调。直接偏好优化（DPO）作为RLHF的高效替代，通过最大化偏好响应与拒绝响应之间的隐式奖励差距来直接优化策略，避免了显式奖励建模和策略梯度估计。然而，DPO的核心机制——隐式奖励函数 

$$r_{\theta}(x,y) = \beta \log \frac{\pi_{\theta}(y|x)}{\pi_{\mathrm{ref}}(y|x)}$$

高度依赖于参考策略$\pi_{\mathrm{ref}}$的质量。当参考策略本身与人类偏好发生冲突时，DPO的损失信号会受到严重污染：模糊的偏好对会在梯度计算中占据主导地位，导致训练方差增大、参数更新不稳定，最终损害泛化能力。理论分析表明，标准DPO的泛化界会因参考策略的不可靠性而扩张，这意味着模型在未见数据上的性能难以保证。

实证观察同样揭示了这一脆弱性。如图1(A)所示，即便使用更大规模的SFT模型作为参考策略，数据集中仍普遍存在与人类偏好相悖的未对齐样本。在IMDb情感控制任务上，随着参考策略由GPT2‑Small逐渐扩大至GPT2‑Large，DPO的性能反而可能出现衰退（见图1(B)）。这些现象指向了一个清晰的方法缺口：现有DPO算法缺乏对参考策略不可信程度的感知与抑制能力。

为填补这一缺口，RAPPO（Order‑Aware Preference Optimization）被提出。它的核心动机是：通过参考策略的对齐程度，主动识别并暂时移除每批中最高损失的、最不可靠的模糊训练对，使模型仅依据清晰的对齐样本和剩余可信任的未对齐样本进行更新。该设计并非简单丢弃数据，而是以顺序感知的方式控制梯度方差，从而在不牺牲参考指导的前提下，为训练过程提供更紧的泛化界。理论证明（Theorem 4.7）确认，RAPPO的稳定性递归界显著优于标准DPO，且其在多个实际任务上展现出一致且可观的改进：在IMDb上奖励得分提升3.5%–7.1%，在毒性控制上将毒性率从基线最优的6.30%降至2.28%，在GPT‑4评估下相对于DPO的胜率达74.5%。这些初步结果驱使进一步探索如何将顺序感知的样本筛选系统化为一种通用的、轻量的DPO增强机制。

## 核心创新

**根本瓶颈**。标准 DPO 隐含假设参考策略 $\pi_{\mathrm{ref}}$ 提供的偏好信号与人类偏好一致。实际上，$\pi_{\mathrm{ref}}$ 经常给出与人类偏好相悖的决策，导致大量“未对齐”偏好对混入训练（Figure 1A）。这些模糊样本的梯度贡献具有高方差，不仅主导了整体优化方向，而且放大了泛化误差，使模型在弱参考策略下性能急剧下降（Figure 1B）。现有的 DPO 变体（如 IPO、SimPO、KTO 等）通过调整损失形式或丢弃参考策略应对该问题，但未能从根本上区分并控制由参考偏差引起的噪声样本。

**核心思路：顺序感知的批量筛选**。RAPPO 的关键创新在于引入“参考对齐序”这一新的因果调控旋钮——它不是永久删除样本，而是在每个训练步上动态识别并暂时排除最可能破坏优化的未对齐对，从而控制梯度方差并收紧泛化界。

**方法级创新——两个 changed slots**：

1. **批次构成**（相对于 DPO 使用全批次样本）  
   - 在每个 mini‑batch 中，根据参考对齐分数 $\frac{\pi_{\mathrm{ref}}(y_w|x)}{\pi_{\mathrm{ref}}(y_l|x)}$ 与阈值 $\tau$ 的比较，将样本划分为 **对齐子集** $\mathcal{A}_\mathcal{B}$ 和 **未对齐子集** $\mathcal{U}_\mathcal{B}$（Algorithm 1, Step 2‑4）。  
   - 对 $\mathcal{U}_\mathcal{B}$ 中的样本按个例 DPO 损失 $\ell_i(\theta)$ 升序排列，**保留损失最小的** $b-q$ 个样本，**丢弃**损失最大的 $q$ 个（Step 5）。  
   - 此举等效于在未对齐样本集合上以顺序标准筛选，使得高损失、不可靠的模糊对在本步中被排除。

2. **优化目标**（相对于 DPO 的全批平均损失）  
   - RAPPO 的每步损失定义为保留的对齐样本和筛选后的未对齐样本的加权平均（Algorithm 1, Step 6）。当小批次中未对齐数量 $b \le q$ 时使用全批，否则只依赖对齐子集和保留的 $b-q$ 个未对齐样本（Proposition 4.8 给出了无偏梯度估计形式）。  
   - 这一目标本质上对未对齐样本施加了基于序的截断，使得每一步的梯度贡献主要来自“清晰的偏好信号”（对齐样本）与“最不有害的未对齐样本”，从而在降低方差的同时保留了参考策略的有益信息。

**管道三阶段**：  
- **评分与划分**：用 $\pi_{\mathrm{ref}}$ 计算每样本对齐分数并二值化。  
- **排序与筛选**：对未对齐子集按即时损失排序，丢弃 top‑$q$。  
- **参数更新**：在保留的子集上执行梯度更新。

**理论与经验支撑**：  
- 定理 4.7 证明，RAPPO 的保留策略能够**最小化未对齐样本的期望最大权重**，从而获得比标准 DPO 更紧的参数稳定性递归界 $\Delta_{t+1} \le (1+L\eta_t)\Delta_t + \frac{2C}{s-q}\eta_t \mathbb{E}[\max_{i\in\mathrm{Kept}_t} w(z_{t,i})]$，直接导出更优的泛化保证。  
- 实验上，RAPPO 在 IMDB 情感控制任务上使奖励评分相对 DPO 提升 3.5–7.1%（跨三个 SFT 模型规模），在毒性控制上将毒性降低至 2.28%（DPO 为 6.30%），在 GPT‑4 评估下对 DPO 的胜率达到 74.5%，在 PKU‑SafeRLHF 上安全率与有用性也全面优于基线。消融实验证实移除样本数 $q$ 的增加（1→2→4）持续提升性能，且 $\tau$ 在 $\{0.8,1.0,1.2\}$ 内具有鲁棒性，额外计算开销仅约 25%。

**与外源方法的对比**：不同于完全丢弃参考策略的 SimPO，RAPPO 保留并选择性使用参考策略；不同于在损失函数上引入偏移或正则项的 DPO‑offset、R‑DPO、ORPO 等，RAPPO 通过实时样本选择直接降低噪声梯度的方差，是一种与损失形式正交、可与现有 DPO 改进叠加的轻量级框架。

**需注意的局限**：当前方法尚未在超过 8B 参数的模型上验证，且超参数 $q$ 和 $\tau$ 的设定仍需人工经验或网格搜索；理论分析依赖光滑性假设，实际语言模型可能不完全满足。这些点可在后续工作中进一步探索自适应丢弃策略。

## 整体框架

![[assets/figures/papers/iclr26_0016_LrHfYPFTtg_Keep_the_Best_Forget_the_Rest_Reliable_Alignment/figures/004_Figure_3.jpg]]
*Figure 3: RAPPO Pipeline:(1) sample mini-batch data; (2) score each mini-batch by reference alignment, splitting samples into Aligned and Unaligned; (3)unaligned samples are ranked by persample loss; (4) temporarily remove some Largest ones for this update*

RAPPO 的整体管道围绕一个核心洞察构建：标准 DPO 在利用参考策略 π_ref 时，对 π_ref 与人类偏好不一致的模糊样本（misaligned preference pairs）高度敏感。这些样本会在梯度信号中引入高方差，干扰训练稳定性并损害泛化能力。RAPPO 在每一优化步中主动识别这类不可靠的对，并**暂时剔除一批中最混乱的若干样本**，使模型始终在相对可靠的信号上更新，从而在不牺牲参考指导的前提下收紧泛化界（Theorem 4.7）。

### 输入–输出流

- **输入**：偏好数据集 `{(x, y_w, y_l)}`，参考策略 π_ref（通常为经过监督微调的基础模型），当前策略 π_θ，以及超参数 `q`（未对齐子集中每批丢弃的样本数）和阈值 `τ`。
- **输出**：更新后的策略参数 θ，每次步骤只对挑选出的子集计算损失并反向传播。

### 管道模块

整个管道由三个高度解耦的模块串联而成，如 Algorithm 1 和 Figure 3 所示。

#### 1. 批次对齐评分（Aligned/Unligated Partitioning）

对每个从偏好数据集中采样的 mini‑batch `B`，RAPPO 首先计算每一样本的**参考对齐分数**：

$$
\frac{\pi_{\mathrm{ref}}(y_w^i \mid x^i)}{\pi_{\mathrm{ref}}(y_l^i \mid x^i)}
$$

并与预设阈值 τ 比较（通常取 τ ∈ {0.8, 1.0, 1.2}）。若比值大于 τ，则认为 π_ref 对该偏好对具有可靠的倾向性，归入对齐集 `A_B`；否则归入未对齐集 `U_B`（Algorithm 1, Step 2–4）。这种基于参考策略概率比值的设计，本质上是在诊断参考模型自身的“困惑度”：当参考策略对 `y_w` 和 `y_l` 的相对置信度过低时，该样本很可能携带误导性信号。

#### 2. 未对齐损失排序与筛选（Order‑Aware Filtering）

对未对齐子集 `U_B` 中的每一个样本，RAPPO 计算其**个体 DPO 损失**：

$$
\ell_i(\theta) = -\log\sigma\big(\beta(\Delta_\theta(z^i) - \Delta_{\mathrm{ref}}(z^i))\big)
$$

然后将所有 `ℓ_i(θ)` 按升序排列，并**只保留损失最小的 `b − q` 个样本**（`b = |U_B|`），丢弃剩余 `q` 个损失最大的样本（Algorithm 1, Step 5）。这里隐含的机制是：损失越大，意味着该偏好对在当前模型和参考策略下越模糊、梯度越不稳定，将它们暂时排除能直接降低条件方差（见 Section 4.2 中的方差不等式及 Proof of part (ii)）。Remark 4.1 强调，样本不会被永久删除；随着模型改善，原本模糊的未对齐样本可能重新获得清晰的梯度信号，从而在后续步骤中重新进入训练。

#### 3. 参数更新（Gradient Aggregation and Update）

保留的样本由两部分组成：所有对齐样本 `A_B` 加上筛选后的 `b − q` 个低损失未对齐样本。RAPPO 在这部分联合子集上计算 **每步平均损失**（如果 `b ≤ q` 则使用全批样本，不丢弃）：

$$
\hat{\mathcal{L}}_{\text{step}}^{\text{RAPPO}} =
\begin{cases}
\displaystyle\frac{1}{s}\sum_{i\in\mathcal{B}} \ell_i(\theta), & \text{if } b \le q,\\[10pt]
\displaystyle\frac{1}{s-q}\!\left(\sum_{i\in\mathcal{A}_\mathcal{B}}\ell_i(\theta) + \sum_{j=1}^{b-q}\ell_{(j)}(\theta)\right), & \text{if } b > q.
\end{cases}
$$

然后对该损失反向传播，更新模型参数 θ（Algorithm 1, Step 6–7）。这一设计在数学上等价于通过**非均匀权重**组合数据集样本，其无偏梯度估计由 Proposition 4.8 保证，并直接对应于更紧的泛化递归界（Theorem 4.7 (iii)）。

### 设计思想总结

RAPPO 并未引入新的奖励模型或复杂的对抗训练，而是通过**对现有 DPO 批次构成的轻量化改造**实现可靠对齐：先以参考对齐分数区分信度，再以单样本损失排序剔除最不可靠者。两个改变槽位（批次构成与优化目标）使其能在几乎不增加显存负担的情况下（约 25% 额外训练时间，Section D.4），将模糊样本引起的梯度方差控制在更窄范围内，从而显著提升训练稳定性与最终性能。此管道与 DPO 类方法（如 IPO、KTO、R‑DPO 等）保持兼容，可视为一种即插即用的**顺序感知偏好优化范式**。

## 核心模块与公式推导

RAPPO 的设计核心在于**批次内顺序感知的偏好筛选**。面对标准 DPO 对参考策略偏差高度敏感、模糊偏好对主导梯度信号从而损害泛化的瓶颈，该方法通过因果调节——在每步更新中依据参考对齐得分识别并暂时剔除损失最高的未对齐样本——来降低梯度方差、收紧泛化界。下面依次梳理三个关键模块，并给出驱动方法的公式及其变量含义。

### 1. 关键模块

**（1）批次划分与对齐评分**  
对于小批次 $\mathcal{B}$ 中的每个偏好对 $z^i = (x^i, y_w^i, y_l^i)$，计算**参考对齐得分** $s^i = \frac{\pi_{\mathrm{ref}}(y_w^i|x^i)}{\pi_{\mathrm{ref}}(y_l^i|x^i)}$，并与阈值 $\tau$ 比较：若 $s^i > \tau$，将该样本划入**对齐子集** $\mathcal{A}_{\mathcal{B}}$；否则归入**未对齐子集** $\mathcal{U}_{\mathcal{B}}$（算法1，步骤2‑4）。这一划分直接暴露参考策略是否与人类偏好一致——对齐子集中的样本提供可靠指导，而未对齐子集则可能引入冲突信号。

**（2）未对齐损失排序与筛选**  
对 $\mathcal{U}_{\mathcal{B}}$ 中的每个样本计算 DPO 个例损失 $\ell_i(\theta) = -\log\sigma\big(\beta(\Delta_\theta(z^i) - \Delta_{\mathrm{ref}}(z^i))\big)$，按升序排列（算法1，步骤5）。设 $b = |\mathcal{U}_{\mathcal{B}}|$：若 $b > q$（$q$ 为预先指定的丢弃数量），只保留损失最小的 $b-q$ 个样本，丢弃 $q$ 个损失最大的样本；若 $b \le q$，则原封不动保留整个批次（算法1，步骤6）。这种“去高损、留低损”的选择准则等价于优先保留参考偏差较小的未对齐样本，从而压低它们对梯度的过度干扰——核心引理（第4节）表明，保留最小损失的样本能够最小化未对齐子集贡献的条件方差。

**（3）参数更新**  
利用上述保留的对齐样本与筛选后的未对齐样本的梯度均值，执行一步随机梯度下降（或 Adam）更新模型参数（算法1，步骤7）。被丢弃的样本并未从数据集中永久移除，仅在当前步骤被暂时忽略；随着训练推进，原本未对齐的样本可能因模型改善而重新通过阈值检验，自然回流训练（注解4.1）。

### 2. 核心公式

**（A）DPO 基础损失与隐式奖励**  
RAPPO 建立在 DPO 框架之上，其核心桥梁是将策略的对数比映射为隐式奖励：

$$
r_\theta(x,y) = \beta \log \frac{\pi_\theta(y|x)}{\pi_{\mathrm{ref}}(y|x)}.
$$

进而，标准 DPO 优化目标为最大化偏好回答与拒绝回答之间的隐式奖励差：

$$
\mathcal{L}_{\mathrm{DPO}}(\pi_\theta;\pi_{\mathrm{ref}}) = -\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{P}}\left[\log\sigma\left(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_{\mathrm{ref}}(y_w|x)} - \beta\log\frac{\pi_\theta(y_l|x)}{\pi_{\mathrm{ref}}(y_l|x)}\right)\right].
$$

对应的经验损失（$N$ 条样本的均值）为：

$$
\widehat{\mathcal{L}}_{\mathrm{DPO}} = \frac{1}{N}\sum_{i=1}^N\left[-\log\sigma\big(\beta(\Delta_\theta(z^i) - \Delta_{\mathrm{ref}}(z^i))\big)\right].
$$

**（B）RAPPO 的即批损失**  
RAPPO 在上述损失中引入硬截断，实际用于每步更新的损失函数为：

$$
\hat{\mathcal{L}}_{\text{step}}^{\text{RAPPO}} =
\begin{cases}
\displaystyle\frac{1}{s}\sum_{i\in\mathcal{B}}\ell_i(\theta), & \text{if } b \le q,\\[12pt]
\displaystyle\frac{1}{s-q}\Bigg(\sum_{i\in\mathcal{A}_{\mathcal{B}}}\ell_i(\theta) + \sum_{j=1}^{b-q}\ell_{(j)}(\theta)\Bigg), & \text{if } b > q,
\end{cases}
$$

其中：
- $s = |\mathcal{B}|$ 为批次大小；
- $b = |\mathcal{U}_{\mathcal{B}}|$ 为未对齐样本数；
- $q$ 为人工设定的丢弃数量；
- $\ell_{(j)}(\theta)$ 表示 $\mathcal{U}_{\mathcal{B}}$ 中升序排列下第 $j$ 小的个例损失。

该设计的逻辑在于：当未对齐样本极少时，直接只用全批梯度；当未对齐样本充足时，强制丢弃 $q$ 个最模糊的偏好对，仅保留对齐集与 $(b-q)$ 个相对可靠的未对齐样本。

**（C）RAPPO 完整目标函数**  
考虑到批次中未对齐样本数 $b$ 的随机性，RAPPO 的总体优化目标可表述为按 $b$ 的概率加权求和（命题4.8）：

$$
\hat{\mathcal{L}}^{\text{RAPPO}} = \sum_{b=0}^{\min(q,\hat{\mu}N)} P(|\mathcal{U}_B|=b)\frac{m_g+m_b}{s} \;+\; \sum_{b=q+1}^{\min(s,\hat{\mu}N)} P(|\mathcal{U}_B|=b)\frac{m_g+\sum_{j=1}^{\hat{\mu}N} \alpha_j \ell_{(j)}}{s-q},
$$

式中：
- $N$ 为数据集总规模，$\hat{\mu}$ 为未对齐样本在数据集中的比例估计；
- $m_g$ 为对齐集中的损失之和；
- $m_b$ 为当 $b\le q$ 时未对齐集的损失之和；
- $\alpha_j$ 为第 $j$ 个未对齐样本在丢弃后被保留的概率，由超几何分布给出。

该表达明确展示了 RAPPO 的动态加权本质：高损失未对齐样本的等效权重被降至零，但数据本身并未被永久删除。

**（D）理论保证：稳定性递归不等式**  
RAPPO 不仅经验性能显著，其泛化优势亦可在温和假设下严格证明。在光滑性与 Lipschitz 连续条件下，参数更新的稳定性递归为：

$$
\Delta_{t+1} \le (1+L\eta_t)\Delta_t + \frac{2C}{s-q}\eta_t \mathbb{E}\Big[\max_{i\in\mathrm{Kept}_t} w(z_{t,i})\Big],
$$

其中：
- $\Delta_t$ 衡量参数在不同 shuffle 下的偏差；
- $L$ 为梯度函数的 Lipschitz 常数；
- $\eta_t$ 为学习率；
- $C$ 为常数；
- $w(z_{t,i})$ 是样本 $z_{t,i}$ 的梯度权重，与损失高度负相关。

RAPPO 通过“保留损失最小的 $(b-q)$ 个未对齐样本”显式最小化了 $\mathbb{E}[\max_{i\in\mathrm{Kept}_t} w(z_{t,i})]$，从而直接压缩递归不等式的右端项，最终导出比标准 DPO 更紧的泛化上界（定理4.7）。这一理论结果从根本上解释了顺序感知丢弃机制为何能同时提升训练的**稳定性**与**泛化性能**。

## 实验与分析

### 主要结果

RAPPO 在四个基准任务上均取得了优于现有偏好优化方法的性能，验证了顺序感知样本筛选策略对训练稳定性和泛化能力的提升作用。

**情感控制（IMDb）。** 在标准情感奖励评分上，RAPPO‑4 达到 **1.6811**，比最强基线 SimPO 高出 8.2%（表 1、表 7）。针对不同规模的 SFT 模型（GPT2‑Small、Medium、Large），RAPPO 相对 DPO 分别将奖励分数提升 3.5%、1.1% 和 7.1%（图 1(B)）。注意，参考策略越弱，RAPPO 的增益幅度越大，这直接印证了其核心机制——有效抑制了由未对齐参考策略引入的模糊偏好的干扰。

![[assets/figures/papers/iclr26_0016_LrHfYPFTtg_Keep_the_Best_Forget_the_Rest_Reliable_Alignment/figures/005_Table_1.jpg]]
*Table 1: Comparison of reward scores and toxicity percentages across various preference optimization methods, evaluated on the IMDB and Real-Toxicity-Prompts Gehman et al. (2020) test set. Higher reward scores and lower toxicity indicate better performance. The whole experiments of SIMPO are defered in Table 7*

![[assets/figures/papers/iclr26_0016_LrHfYPFTtg_Keep_the_Best_Forget_the_Rest_Reliable_Alignment/figures/002_Figure_1.jpg]]
*Figure 1: (A) Reference model performance across three SFT models (GPT2-Small, Medium, and Large). Correct: the reference policy aligns with human preference. Wrong: the reference policy conflicts with human preference. (A) shows that misaligned data are frequent regardless of model size, though the proportion decreases as model size increases. (B) Reward scores on the IMDb experiment (Section 5.1) using DPO and RAPPO under different reference policy scales. Performance declines as the reference policy weakens. Nonetheless, with a simple modification to DPO, our method RAPPO improves performance by 3.5%, 1.1%, and 7.1% across the three models*

![[assets/figures/papers/iclr26_0016_LrHfYPFTtg_Keep_the_Best_Forget_the_Rest_Reliable_Alignment/figures/013_Table_7.jpg]]
*Table 7: Comparison of reward scores and toxicity percentages across SimPO and RAPPO with various parameters, evaluated on the IMDB and Real-Toxicity-Prompts Gehman et al. (2020) test set. Higher reward scores and lower toxicity indicate better performance. All values are averaged over three random seeds*

**毒性控制（Real‑Toxicity‑Prompts）。** RAPPO‑4 将毒性比例压低至 **2.28%**，远优于 DPO 的 6.30%（表 1、表 7）。图 2 进一步揭示了作用机理：在参考策略最“确信”的清晰样本上，RAPPO 产生的赢‑输概率差显著大于 DPO，同时在不易对齐的样本上仅牺牲极少性能。这恰好对应了“保留最佳、遗忘其余”的设计哲学：模型将容量集中于可从可靠偏好中学习的规律，而非强行拟合模棱两可的样本。

**文本摘要（GPT‑4 胜率评估）。** 当使用 GPT‑4 作为评判时，RAPPO 对 DPO 的胜率达 **74.5%**，对 SimPO 的胜率为 **58.8%**（图 4、第 1 节）。该结果不只反映在自动化指标上的优势，也表明 RAPPO 生成的摘要更符合人类偏好。值得注意的是，图 4 中 RAPPO‑1 即已显著超越两个强基线，提示即使保守地剔除少量样本也能带来实质改进。

![[assets/figures/papers/iclr26_0016_LrHfYPFTtg_Keep_the_Best_Forget_the_Rest_Reliable_Alignment/figures/006_Figure_4.jpg]]
*Figure 4: Win Rate between RAPPO-1, SIMPO, and DPO by GPT-4*

**安全对齐（PKU‑SafeRLHF）。** 在帮助性、无害性、安全率和胜率四个维度上，RAPPO 均优于 DPO、KTO、SimPO 等基线（表 12、图 5）。具体而言，RAPPO 的安全性率提升至 57.26%（DPO 为 55.89%），帮助性得分从 0.51 上升到 **0.69**，无害性得分达到 0.357，胜率高达 **65%**。这些结果表明，RAPPO 在平衡帮助性与安全性方面具有稳健表现，且该优势并非来自增大模型容量或复杂正则项，而是源于对训练批次中不可靠样本的动态甄别。

![[assets/figures/papers/iclr26_0016_LrHfYPFTtg_Keep_the_Best_Forget_the_Rest_Reliable_Alignment/figures/016_Table_12.jpg]]
*Table 12: PKU-SafeRLHF results. RAPPO compared to DPO, CPO, KTO, SIMPO, IPO, ORPO, and R-DPO under identical decoding and evaluation protocols*

### 消融与分析

**移除样本数 q 的影响。** 表 7 显示，当 q 从 1 增至 4 时，IMDb 奖励分数与毒性指标均持续改善；奖励最高达 1.6811，毒性最低至 2.28%。这与理论分析（定理 4.7）一致：增大 q 等价于进一步压低保留集合中未对齐样本的最大权重期望 ${\mathbb{E}}[\max_{i\in\mathrm{Kept}_t} w(z_{t,i})]$，从而收紧参数稳定性递归界并减小泛化间隙。据此，q 可视为控制训练方差与偏差的直观旋钮。

**阈值 τ 的鲁棒性。** 表 2 表明，参考对齐阈值 τ 在 {0.8, 1.0, 1.2} 区间内几乎不影响性能。RAPPO 对 τ 的鲁棒性源于其联合使用阈值划分与基于实时损失排序的选择：即使划分边界不精确，最终保留的仍是同一批中对当前模型梯度方差贡献最小的样本。这一特性减轻了超参数调节负担，增强了方法的实用性。

**计算开销。** 相对于标准 DPO，RAPPO 引入约 25% 的额外训练时间（附录 D.4），主要来自未对齐样本的损失排序步骤。鉴于排序仅作用于每批的未对齐子集，且超参数 s（批大小）通常较小，该开销在整体微调成本中几乎可以忽略。这一增益‑代价比使其便于嵌入现有 DPO 管线，仅需数行代码改动。

**与参考‑自由方法的对比。** 尽管 SimPO 完全舍弃参考策略，RAPPO 却通过选择性保留参考信息实现了更优的稳定性和最终性能（表 7 中所有 RAPPO 变体均大幅领先 SimPO）。这揭示了一个重要洞见：DPO 类方法对参考策略的依赖并非需要彻底废除，而是应当有选择地利用——暂时屏蔽最具有误导性的信号即可维持梯度可靠性的同时避免退化。

### 局限性

尽管 RAPPO 在上述实验中展现出显著优势，论文也明确指出以下当前局限： (1) 尚未在超过 **8B 参数**的大规模模型上进行验证，其可扩展性未知；(2) 超参数 q 和 τ 目前依赖网格搜索或经验预设，未来可设计自适应或可学习的保留策略；(3) 理论保证建立在光滑性和 Lipschitz 假设之上，实际语言模型未必严格满足，因此泛化界仅作为定性指引；(4) 评估集中于情感控制、毒性、摘要和安全对齐四类任务，**在其他复杂场景中的表现有待进一步检验**；(5) 当参考策略本身极度不可靠时，RAPPO 能否持续有效或需额外校准仍属开放问题；(6) 尽管额外训练时间可接受，但在超大规模训练中进一步降低该开销仍是工程优化的方向。

### 关键图表结论

- **图 1**：展示了参考策略未对齐现象的广泛存在以及 RAPPO 在不同模型规模下相对于 DPO 的稳定收益，尤其是在参考策略较弱时，RAPPO 的优势更为突出。
- **图 2**：揭示了 RAPPO 在“清晰”样本上显著扩大赢‑输概率差距，而在“模糊”样本上仅付出轻微代价，从实证角度支撑了顺序感知丢弃机制。
- **图 3**：以管道图形式直观呈现了 RAPPO 的四步操作：批采样、参考对齐评分与划分、未对齐样本损失排序、暂时丢弃高损失项并更新。
- **图 4**：以 GPT‑4 胜率矩阵的形式直观肯定了 RAPPO 超越 DPO 和 SimPO 的生成质量。
- **表 1**：提供了 IMDB 和毒性控制的总体对比，RAPPO 各变体在两项指标上均压倒了所有基线。
- **表 7**：完全展开的 SimPO 与 RAPPO 详细对比，在不同参数配置下验证了 RAPPO 的稳定优越性。
- **表 12**：安全对齐实验的全指标细表，突显 RAPPO 在帮助性和安全性上的共同进步。

## 方法谱系与知识库定位

### 与基线方法的关系

RAPPO 处于直接偏好优化（DPO）的变体谱系中，其核心贡献在于 **以参考模型的对齐程度为信号，临时排除不可靠的训练样本**，从而在不完全抛弃参考正则化的前提下提升训练稳定性。与现有方法相比，RAPPO 的定位可以从以下两个维度拆解：

1. **参考模型的使用方式**  
   - **标准 DPO** 将参考模型视为默认先验，对所有样本同等加权。但当参考策略与人类偏好不一致（错误对齐）时，模糊的偏好对会主导梯度信号，并损害泛化性能（见图 1A 和定理 4.7）。RAPPO 通过比对参考输出概率比（$\pi_{\mathrm{ref}}(y_w)/\pi_{\mathrm{ref}}(y_l) > \tau$）识别未对齐样本，并将高瞬时损失的部分临时丢弃，使更新集中在可靠的对齐样本和低损失未对齐样本上（Algorithm 1, Step 2-5）。  
   - **IPO** 和 **DPO‑offset** 通过显式 KL 正则化或可学习偏移量约束策略变化，但未从根本上区分样本可靠性。RAPPO 直接针对误对齐来源，在 IMDB 奖励分数和毒性控制上显著超越这些变体（Table 1）。  
   - **SimPO** 作为无参考方法的代表，彻底移除了参考模型，在部分任务上表现出色，但也失去了参考模型的正则化引导。RAPPO 保留了参考模型，仅在必要时剪除其有害影响，因此在 GPT‑4 评估的摘要任务中赢过 SimPO 58.8%（Figure 4），并在 PKU‑SafeRLHF 的四项指标上全面领先（Figure 5, Table 12）。  
   - **KTO**、**ORPO** 和 **R‑DPO** 分别通过不对称加权、最大似然目标或长度正则化改进损失函数，但这些设计并未显式处理参考模型的误对齐风险。RAPPO 的顺序感知过滤模块本身是目标无关的，可作为插件与上述方法结合（论文讨论了一致性，但未提供组合实验）。

2. **样本选择策略**  
   RAPPO 的独特之处在于**动态、可逆的批次级过滤**：它从不永久删除样本，未对齐样本随模型优化可能重新满足对齐条件而进入保留集（Remark 4.1）。与静态数据清洗或永久剔除硬样本的方法相比，这种“可取消信任”机制更适合在线学习场景。理论分析表明，这种保留最小 $s-q$ 个置信度最高样本的策略同时最小化了条件方差并最大化了一阶期望下降，从而得到比标准 DPO 更紧的泛化界（Theorem 4.7 中的稳定性递归 $\Delta_{t+1} \le (1+L\eta_t)\Delta_t + \frac{2C}{s-q}\eta_t \mathbb{E}[\max_{i\in\mathrm{Kept}_t} w(z_{t,i})]$）。

### 适用边界与限制

1. **适用任务与模型规模边界**  
   - **经验覆盖**：RAPPO 在情感控制（IMDb）、毒性缩减（Real‑Toxicity‑Prompts）、文本摘要和安全性对齐（PKU‑SafeRLHF）四个任务上均获得了相对于 DPO 的一致提升（Table 1; Table 7; Table 12），模型规模覆盖 GPT‑2 Small/Medium/Large（约 0.1B–0.8B）、OPT‑2.7B 和 Pythia‑6.9B。  
   - **未验证区域**：尚未在超过 8B 参数的大规模模型（如 LLaMA‑70B 等）上进行测试；在代码生成、推理等复杂指令任务上的表现未知。定理 4.7 的推导依赖光滑性和 Lipschitz 连续性假设，实际大模型可能违反这些条件，导致理论保证不再成立。

2. **方法与实现限制**  
   - **超参数工程**：丢弃数量 $q$ 和对齐阈值 $\tau$ 目前只能通过网格搜索或经验设定（Table 2）。尽管实验显示 RAPPO 对 $\tau$ 取值（0.8–1.2）鲁棒，且增大 $q$ 持续带来收益（Table 7），但缺乏自适应或可学习的保留规则。  
   - **计算开销**：每步的评分、排序与丢弃带来约 25% 的额外训练时间（Appendix D.4），在极小批量的实验中可忽略，但在千亿 tokens 级的大规模训练中可能成为瓶颈。排序步骤的时间复杂度为 $O(s\log s)$，暂未考虑更高效的 top‑k 近似。  
   - **参考模型质量依赖**：当参考策略几乎完全不可靠（即 $\hat{\mu} \approx 1$）时，对齐子集 $\mathcal{A}_{\mathcal{B}}$ 可能过小，导致 RAPPO 退化为全批量 DPO（Algorithm 1 中 $b\le q$ 分支）。此时 RAPPO 无法提供增益，且丢弃机制丧失过滤作用，性能可能降回 DPO 基线。  
   - **理论假设与实际的差距**：泛化界的成立需要梯度被权重函数 $w(z)$ 界定，这一条件在实际 NLP 任务中难以强制验证。论文未给出 $C$ 和 $w$ 的经验估计，因此理论的定量指导意义有限。

### 开放问题

RAPPO 提出了一个核心权衡：**在依赖有噪声的参考策略进行偏好优化时，如何动态决定保留多少、保留哪些样本。** 围绕这一权衡，以下问题值得进一步研究：

1. **自适应样本保留策略**：能否使用模型自身的损失动态或验证集信号在线调整 $q$ 和 $\tau$，从而免除网格搜索？例如，基于当前批次的未对齐比例和学习曲线斜率设计元控制器。  
2. **与 token‑level 及其他变体的协同**：RAPPO 的过滤模块完全与具体的偏好优化目标解耦，理论上可以和 token‑level DPO、R‑DPO、CPO 等组合。组合后是否会产生新的梯度冲突，以及如何在理论上保证组合算法的收敛性，仍需探索。  
3. **非凸过参数化场景下的理论保证**：当前分析依赖于强光滑性和有界梯度范数，但在实际 Transformer 优化中，损失曲面高度非凸且模型过参数化。能否在弱条件（如 PL 不等式）下证明 RAPPO 的收敛性及更紧的泛化界？  
4. **极端参考策略下的可靠性**：当参考模型完全反人类偏好（如反向指令微调的模型）时，RAPPO 需要外部信号介入或自动降低 $\tau$。能否将 RAPPO 与独立的奖励校准模块结合，使其在参考完全不可信时仍保持部分过滤效果？  
5. **跨范式推广**：RAPPO 的顺序感知丢弃逻辑（保留损失最小的样本）本质上是一种在线样本加权策略，是否可用于 RLHF 的 PPO 阶段，即根据即时优势信号或 TD 误差的可靠性筛选经验？这或将缓解奖励模型过度优化和策略崩溃问题。  

总体而言，RAPPO 通过一个简单但有效的选择性过滤机制，缓解了 DPO 对参考模型的脆弱依赖，在多个基准上展现了更紧的理论界和一致的实证增益。将该思想扩展到更大规模模型、更松弛的理论框架以及更广泛的对齐范式，是未来工作的重要方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/Keep_the_Best_Forget_the_Rest_Reliable_Alignment_with_Order_Aware_Preference_Optimization.pdf]]
