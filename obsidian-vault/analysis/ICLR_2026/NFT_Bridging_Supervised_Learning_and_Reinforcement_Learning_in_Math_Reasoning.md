---
title: "NFT: Bridging Supervised Learning and Reinforcement Learning in Math Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/NFT_Bridging_Supervised_Learning_and_Reinforcement_Learning_in_Math_Reasoning.pdf
openreview_forum_id: ujBrsQm6Zu
aliases:
- NAFTN
- NFT
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过构造隐式负策略（implicit negative policy），将负样本的建模参数化为正策略的函数，使得对负样本的最大似然训练直接等价于优化正策略，从而让SL也能有效利用验证信号。"
primary_logic: "正策略与负策略之间存在严格的线性耦合关系（π_old = r_q π^+ + (1-r_q) π^-），借此可以将负样本的监督学习目标转化为对正策略的梯度更新，打破了SL无法从错误中学习的传统认知。"
claims:
- "NFT 通过隐式负策略实现负样本上的策略优化，其最优解收敛于真实正分布 π^+。"
- "NFT 与 GRPO 在严格 on-policy 训练下梯度等价，尽管两者理论根基完全不同。"
- "在 7B 和 32B 数学推理基准上，NFT 性能匹配或超越 SOTA RL 算法（如 DAPO），并显著优于 RFT。"
- "负反馈的使用显著提升了模型的探索能力（熵增加），且在大模型上收益更大。"
---

# NFT: Bridging Supervised Learning and Reinforcement Learning in Math Reasoning

> [!tip] 核心洞察
> 正策略与负策略之间存在严格的线性耦合关系（π_old = r_q π^+ + (1-r_q) π^-），借此可以将负样本的监督学习目标转化为对正策略的梯度更新，打破了SL无法从错误中学习的传统认知。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | NFT：在数学推理中桥接监督学习与强化学习 |
| 英文题名 | NFT: Bridging Supervised Learning and Reinforcement Learning in Math Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ujBrsQm6Zu); [Project](https://research.nvidia.com/labs/dir/Negative-aware-Fine-Tuning) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Negative-aware Fine-Tuning (NFT) |
| Dataset | Average over 6 benchmarks (Qwen2.5-Math-7B), AMC23 (Qwen2.5-Math-7B), Average over 6 benchmarks (Qwen2.5-32B) |

> [!tip] 效果简介
> - Average over 6 benchmarks (Qwen2.5-Math-7B) 上，Average Accuracy 为 51.7，对比 DAPO: 51.2, RFT: 48.3，变化 +0.5 vs DAPO, +3.4 vs RFT。
> - AMC23 (Qwen2.5-Math-7B) 上，Accuracy 为 88.5，对比 DAPO: 85.0, RFT: 79.7，变化 +3.5 vs DAPO, +8.8 vs RFT。
> - Average over 6 benchmarks (Qwen2.5-32B) 上，Average Accuracy 为 59.2，对比 DAPO: 59.9, RFT: 52.8，变化 -0.7 vs DAPO, +6.4 vs RFT。

## 概述

### 问题背景

在大语言模型（LLM）的数学推理能力训练中，强化学习（RL）方法近年来占据了主导地位，而监督学习（SL）方法在很大程度上被忽视。这一现象的核心瓶颈在于：传统的 SL 方法（如拒绝采样微调 RFT）只能利用正样本（正确答案）进行训练，必须丢弃所有负样本（错误答案），因为它们依赖参考答案且缺乏从错误中自我反思的机制。相比之下，RL 方法可以通过验证信号（奖励）有效利用负反馈，从而在在线自改进（online self-improvement）场景中持续获得性能提升。这一结构性差异使得 SL 在验证驱动的在线训练中始终落后于 RL。

### 核心方法

本文提出 **Negative-aware Fine-Tuning (NFT)**，一种在线学习算法，旨在桥接 SL 与 RL 之间的鸿沟。NFT 的核心创新在于通过构造**隐式负策略（implicit negative policy）**，将负样本的建模参数化为正策略的函数，使得对负样本的最大似然训练可以直接转化为对正策略的梯度优化。这一设计的理论基石是正策略与负策略之间的严格线性耦合关系：

$$r_{\mathbf{q}} \pi^{+}(\mathbf{a}|\mathbf{q}) + [1-r_{\mathbf{q}}] \pi^{-}(\mathbf{a}|\mathbf{q}) = \pi_{\mathrm{old}}(\mathbf{a}|\mathbf{q})$$

借助这一恒等式，NFT 无需引入额外的模型即可同时对正负样本进行监督训练，打破了“SL 无法从错误中学习”的传统认知。理论上，NFT 的最优解收敛于真实正分布 $\pi^{+}$（Theorem 3.1），且在严格 on-policy 训练下与主流 RL 算法 GRPO 梯度等价（Proposition 4.2），尽管两者的理论根基完全不同。

### 方法定位

Figure 1 将 NFT 定位为在线微调算法谱系中的桥梁：它一端连接仅使用正样本的 SL 方法（如 RFT），另一端连接使用奖励信号进行策略优化的 RL 方法（如 GRPO、DAPO）。NFT 通过监督学习的形式实现了对负反馈的有效利用，从而兼具 SL 的简洁性与 RL 的样本利用效率。

### 主要结果

在数学推理基准上的实验表明，NFT 在 7B 和 32B 模型规模上均表现出色：
- **7B 模型**：NFT 在 6 个基准上的平均准确率达到 51.7%，匹配或超越 SOTA RL 算法 DAPO（51.2%），并显著优于 RFT（48.3%）。
- **32B 模型**：NFT 平均准确率为 59.2%，与 DAPO（59.9%）基本持平，较 RFT（52.8%）提升 6.4 个百分点。

此外，分析显示负反馈的使用显著提升了模型的探索能力（熵增加），且这一收益在大模型上更为明显。消融实验验证了困难问题加权和负似然比裁剪等设计选择的有效性。

## 背景与动机

### 数学推理中的在线微调范式

大语言模型在数学推理任务上的能力提升高度依赖在线微调——模型在训练过程中持续生成答案、接收验证反馈并据此更新策略。这一范式下存在两条主流技术路线：

**监督学习路线**以**拒绝采样微调（RFT）**为代表（Yuan et al., 2023b; Dong et al., 2023），仅保留验证器判定正确的样本进行最大似然训练，直接丢弃所有错误生成。其核心操作是最大化正样本的对数似然，等价于最小化模型分布与数据分布之间的 KL 散度：

$$\max_{\theta} \mathbb{E}_{a \sim \pi(a \mid q)} \log \pi_{\theta}(a \vert q) \Leftrightarrow \min_{\theta} D_{\mathrm{KL}}\left[\pi(a \vert q) \vert\vert \pi_{\theta}(a \vert q)\right]$$

**强化学习路线**以 **GRPO**（Shao et al., 2024）及其变体 **DAPO**（Yu et al., 2025）为代表，通过组归一化优势估计和策略梯度更新模型。其梯度形式为：

$$\nabla_{\theta} J(\theta) = \mathbb{E}_{a \sim \pi_{\theta}(a \vert \mathbf{q})} \nabla_{\theta} \left[ r(\mathbf{q}, a) \log \pi_{\theta}(a \vert \mathbf{q}) \right]$$

在离线场景下，通过重要性采样将梯度重写为：

$$\nabla_{\theta} J(\theta) = \mathbb{E}_{a \sim \pi_{\mathrm{old}}(a | q)} \left[ \frac{\pi_{\theta}(a | q)}{\pi_{\mathrm{old}}(a | q)} r(q, a) \nabla_{\theta} \log \pi_{\theta}(a | q) \right]$$

### 核心瓶颈：监督学习为何落后

在验证驱动的在线自改进场景中，监督学习长期落后于强化学习，其根本原因在于两个结构性缺陷：

1. **对参考答案的刚性依赖**：SL 方法必须依赖外部提供的正确答案才能构造训练信号，无法从模型自身的探索中提取学习信息。

2. **负样本的信息浪费**：RFT 直接丢弃所有错误生成，丧失了从失败中学习的机会。这一浪费在数学推理中尤为致命——错误答案往往揭示了模型的系统性推理缺陷，而这些缺陷恰好是改进的关键杠杆点。

相比之下，RL 方法天然具备利用负反馈的能力：通过优势函数 $\hat{A}_{q,a} = [r(q,a) - \mathrm{mean}\{r^{1:K}\}] / \mathrm{std}\{r^{1:K}\}$，错误样本获得负优势，驱动策略远离低奖励区域。这使得 RL 在探索能力和最终性能上持续领先于 SL。

### 本文动机：用监督学习的方式利用负反馈

本文的核心动机在于打破上述认知壁垒：**监督学习是否也能有效利用负样本进行策略优化？**

关键洞察在于，正策略 $\pi^{+}$ 与负策略 $\pi^{-}$ 之间存在严格的线性耦合关系：

$$r_{\mathbf{q}} \pi^{+}(\mathbf{a}|\mathbf{q}) + [1-r_{\mathbf{q}}] \pi^{-}(\mathbf{a}|\mathbf{q}) = \pi_{\mathrm{old}}(\mathbf{a}|\mathbf{q})$$

其中 $\pi^{+}$ 和 $\pi^{-}$ 分别由贝叶斯规则定义：

$$\pi^{+}(\mathbf{a}|\mathbf{q}) := \frac{\pi_{\mathrm{old}}(\mathbf{a}|\mathbf{q}) p(r=1|\mathbf{q},\mathbf{a})}{\sum_{A} \pi_{\mathrm{old}}(\mathbf{a}|\mathbf{q}) p(r=1|\mathbf{q},\mathbf{a})}$$

$$\pi^{-}(a|q) := \frac{\pi_{\mathrm{old}}(a|q)[1-p(r=1|q,a)]}{\sum_{A} \pi_{\mathrm{old}}(a|q)[1-p(r=1|q,a)]}$$

这一耦合关系意味着：负策略可以被参数化为正策略的函数，无需引入额外模型。通过在负样本上构造隐式负策略并进行最大似然训练，其梯度更新可以直接等价于对正策略的优化。这使得 SL 方法首次获得了与 RL 同等的负反馈利用能力，从而在在线自改进场景中弥合了两类方法之间的性能鸿沟。

Figure 1 展示了这一方法谱系：NFT 通过监督信号利用负反馈，桥接了强化学习与监督学习两大范式。

## 核心创新

### 问题瓶颈：监督学习为何在验证驱动训练中落后

在线微调（online fine-tuning）范式中，强化学习（RL）长期占据主导地位，而监督学习（SL）被视为次优方案。其根本瓶颈在于：传统 SL（如 Rejection Fine-Tuning, RFT）**依赖参考答案，只能利用正样本进行最大似然训练，完全丢弃模型生成的错误样本**。这导致两个后果：

1. **数据利用率低下**：模型在在线采样中产生大量负样本，这些样本包含有价值的自我反思信号，但 SL 范式缺乏利用它们的机制。
2. **探索能力退化**：仅拟合正样本会持续降低模型输出的熵（Figure 8），使策略趋于保守，丧失发现更优解的能力。

相比之下，RL 方法（如 GRPO、DAPO）通过策略梯度自然地利用正负反馈信号，在在线自改进场景中持续领先。

### 核心洞见：正负策略的线性耦合

NFT 的关键突破在于发现**正策略与负策略之间存在严格的线性耦合关系**。给定旧策略 $\pi_{\mathrm{old}}$ 和问题 $q$ 的答案正确率 $r_q$，正策略 $\pi^+$（正确答案的条件分布）和负策略 $\pi^-$（错误答案的条件分布）满足：

$$r_q \pi^+(a|q) + (1-r_q) \pi^-(a|q) = \pi_{\mathrm{old}}(a|q)$$

这一恒等式（Eq. 7）揭示了：**负策略并非独立实体，而是正策略和旧策略的确定性函数**。由此，NFT 构造了隐式负策略（implicit negative policy）：

$$\pi_\theta^-(a|q) := \frac{\pi_{\mathrm{old}}(a|q) - r_q \pi_\theta^+(a|q)}{1 - r_q}$$

这意味着只需维护一个正策略模型 $\pi_\theta^+$，即可同时参数化负策略，**无需额外模型或偏好数据**。

### 方法创新：四个关键 changed slots

基于上述洞见，NFT 相对于 RFT 等 SL 基线做出了四个关键改变：

**1. 负样本利用（Negative Data Usage）**
- Baseline（RFT）：丢弃所有负样本，仅对正样本做最大似然估计。
- NFT：构造隐式负策略，同时对正负样本进行最大似然训练。负样本的优化目标通过隐式参数化转化为对正策略的梯度更新，打破了 SL 无法从错误中学习的传统认知。

**2. 损失函数重构（Loss Function）**
NFT 的序列级损失（Eq. 9）联合优化正负样本：

$$\mathcal{L}^{\mathrm{NFT}}(\theta) = r\left[-\log \frac{\pi_\theta^+(a|q)}{\pi_{\mathrm{old}}(a|q)}\right] + (1-r)\left[-\log \frac{1 - r_q \frac{\pi_\theta^+(a|q)}{\pi_{\mathrm{old}}(a|q)}}{1 - r_q}\right]$$

- 正样本项（$r=1$）：最大化新旧策略似然比的对数，等价于带基线减法的监督学习。
- 负样本项（$r=0$）：当正策略对错误答案的似然比 $R_\theta$ 增大时，该项产生惩罚梯度，驱动模型远离错误分布。

**3. 负似然比裁剪（Negative Likelihood Clipping）**
为防止对负样本的过度惩罚导致训练崩溃，NFT 对负似然比施加最小值裁剪 $\epsilon$（Eq. 10），并使用直通梯度（straight-through gradient）保持梯度流。消融实验（Figure 10）表明，$\epsilon=1.0$ 时性能最佳；$\epsilon \to 0$ 会因过度惩罚负样本而降低整体性能。

**4. 提示加权（Prompt Weighting）**
不同于 RFT 对所有问题等权重处理，NFT 根据问题难度分配权重 $\omega(q)$，使困难问题（低 $r_q$）获得更高训练权重：

$$\omega(q) = 1 - r_q \quad \text{或} \quad \omega(q) = \sqrt{(1-r_q)/r_q}$$

消融实验（Figure 9）证实，这两种加权策略均显著优于均匀加权，且二者性能相当。

### 理论地位：桥接 SL 与 RL

NFT 的理论贡献不仅在于提出新算法，更在于**揭示了 SL 与 RL 在在线微调中的内在联系**。Proposition 4.2 证明：在严格 on-policy 训练下，NFT 与 GRPO 的梯度完全等价，尽管理论根基截然不同（前者基于监督学习的策略分解，后者基于策略梯度）。这一发现将 NFT 定位为在线算法谱系中桥接 SL 与 RL 的关键节点（Figure 1）。

### 证据强度评估

| 创新点 | 证据类型 | 置信度 |
|--------|----------|--------|
| 隐式负策略的最优解收敛于真实正分布 | 定理证明（Theorem 3.1, Appendix A） | 高 |
| NFT 与 GRPO 在 on-policy 下梯度等价 | 命题证明（Proposition 4.2, Appendix A.4） | 高 |
| 性能匹配或超越 SOTA RL（DAPO） | 主实验（Table 1, 7B/32B） | 高 |
| 负反馈提升探索能力（熵增加） | 训练曲线（Figure 8） | 中高 |
| 负反馈在大模型上收益更大 | 观察性结论（Sec.5.3） | 中 |

**需注意的局限**：当前实现主要依赖二进制奖励验证器，连续奖励场景的理论扩展（Appendix B）尚未经大规模实验验证。此外，RFT 在 32B 模型中贡献了总增益的 80%，负反馈仅贡献 20%，这是否意味着负样本的作用被高估，仍需进一步研究。

## 整体框架

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_ujBrsQm6Zu/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of the NFT algorithm. Data Collection: An LLM π generates answers to a set of math questions. Generation results are split into two sub-datasets based on their answer correctness. Policy Optimization: By constructing an implicit policy for modeling negative data, NFT enables direct policy optimization on both positive and negative answers via maximum-likelihood*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_ujBrsQm6Zu/figures/001_Figure_1.jpg]]
*Figure 1: A spectrum of online algorithms for LLM fine-tuning. NFT bridges reinforcement learning and supervised learning methods through the leverage of negative feedback via supervision*

NFT（Negative-aware Fine-Tuning）是一种在线微调算法，其核心 pipeline 由两个交替执行的阶段构成：**数据收集**与**策略优化**（Figure 2）。

### 数据收集阶段

对于每个数学问题 $q$，当前策略模型 $\pi_\theta$ 采样 $K$ 个候选答案 $\{a_1, a_2, \dots, a_K\}$。每个答案通过验证器（binary reward verifier）标注正确性 $r(q, a) \in \{0, 1\}$，据此将生成结果划分为正样本集 $\mathcal{D}^+$ 和负样本集 $\mathcal{D}^-$。同时，记录旧策略（采样时的模型）下每个答案的对数似然 $\log \pi_{\text{old}}(a|q)$，并计算该问题的经验正确率 $\hat{r}_q = \frac{1}{K} \sum_{a|q} r(q, a)$。

关键过滤规则：仅保留 $0 < \hat{r}_q < 1$ 的问题参与训练，即排除全对或全错的极端情况，确保正负样本同时存在以驱动有效学习。

### 策略优化阶段

NFT 的核心创新在于通过**隐式负策略**（implicit negative policy）同时利用正负样本进行监督学习（Figure 2 右半部分）。具体流程如下：

1. **正分支**：对正样本 $(r=1)$，计算 token 级新旧策略似然比 $R_\theta^t(q, a) = \frac{\pi_\theta^+(a_t|q, a_{<t})}{\pi_{\text{old}}(a_t|q, a_{<t})}$，最大化 $\log R_\theta^t$，即标准的监督微调形式。

2. **负分支**：对负样本 $(r=0)$，NFT 不直接建模负策略，而是利用策略耦合恒等式 $r_q \pi^+ + (1-r_q) \pi^- = \pi_{\text{old}}$，将负策略参数化为正策略的函数：
   $$\pi_\theta^{-}(a|q) = \frac{\pi_{\text{old}}(a|q) - r_q \pi_\theta^+(a|q)}{1 - r_q}$$
   由此，负样本的最大似然目标被转化为对正策略 $\pi_\theta^+$ 的梯度更新。负似然比 $\frac{1 - \hat{r}_q R_\theta^t}{1 - \hat{r}_q}$ 被最大化，同时施加最小值裁剪 $\epsilon$ 以防止过度惩罚（默认 $\epsilon=1.0$），并使用直通梯度（straight-through gradient）保持梯度流。

3. **提示加权**：每个问题的损失按 $\omega(q)$ 加权，困难问题（低 $\hat{r}_q$）获得更高权重。可选方案包括 $\omega(q)=1-\hat{r}_q$ 或 $\omega(q)=\sqrt{(1-\hat{r}_q)/\hat{r}_q}$，后者在形式上与 GRPO 对齐。

### 输入输出流

- **输入**：数学问题集、验证器（binary reward function）、预训练 LLM 作为初始策略 $\pi_0$。
- **每轮迭代**：当前策略 $\pi_\theta$ 采样答案 → 验证器标注 → 计算 $\hat{r}_q$ 和旧策略似然 → 过滤有效问题 → 计算 token 级 NFT 损失（Eq. 10）→ 梯度更新 $\theta$。
- **输出**：经过多轮在线自改进的优化策略 $\pi_\theta^+$，在数学推理基准上匹配或超越主流 RL 算法。

### 方法定位

NFT 在在线微调算法谱系中占据独特位置（Figure 1）：它使用监督学习（最大似然）的形式，却通过隐式负策略的构造实现了对负样本的策略优化，从而桥接了监督学习（如 RFT）与强化学习（如 GRPO）之间的鸿沟。Theorem 3.1 证明，仅使用负样本进行 NFT 训练，其最优解收敛于真实正分布 $\pi^+$；Proposition 4.2 进一步揭示，在严格 on-policy 条件下，NFT 与 GRPO 的梯度等价，尽管理论根基完全不同。

## 核心模块与公式推导

### 3.1 策略分裂：从生成策略到正/负策略

NFT 的核心起点是将模型的生成策略 $\pi_{\mathrm{old}}$ 按答案正确性分裂为正策略 $\pi^+$ 和负策略 $\pi^-$。利用贝叶斯规则，正策略定义为给定问题 $\mathbf{q}$ 下正确答案的条件分布：

$$\pi^{+}(\mathbf{a}|\mathbf{q}) := \frac{\pi_{\mathrm{old}}(\mathbf{a}|\mathbf{q})\,p(r=1|\mathbf{q},\mathbf{a})}{\sum_{A}\pi_{\mathrm{old}}(\mathbf{a}|\mathbf{q})\,p(r=1|\mathbf{q},\mathbf{a})} \quad \text{(Eq. 5)}$$

负策略对称地定义为错误答案的条件分布：

$$\pi^{-}(a|q) := \frac{\pi_{\mathrm{old}}(a|q)\,[1-p(r=1|q,a)]}{\sum_{A}\pi_{\mathrm{old}}(a|q)\,[1-p(r=1|q,a)]} \quad \text{(Eq. 6)}$$

这两个策略之间存在严格的线性耦合关系，通过旧策略和问题级正确率 $r_{\mathbf{q}}$ 相连：

$$r_{\mathbf{q}}\,\pi^{+}(\mathbf{a}|\mathbf{q}) + [1-r_{\mathbf{q}}]\,\pi^{-}(\mathbf{a}|\mathbf{q}) = \pi_{\mathrm{old}}(\mathbf{a}|\mathbf{q}) \quad \text{(Eq. 7)}$$

这一恒等式是 NFT 的关键——它意味着一旦确定了正策略，负策略就被唯一确定，无需额外建模。

### 3.2 隐式负策略与 NFT 损失

传统监督学习只能对正样本做最大似然训练，因为负样本的真实分布 $\pi^-$ 未知。NFT 利用 Eq. 7 的耦合关系，将负策略参数化为正策略的函数，构造**隐式负策略**：

$$\pi_{\theta}^{-}(\mathbf{a}|\mathbf{q}) := \frac{\pi_{\mathrm{old}}(\mathbf{a}|\mathbf{q}) - r_{\mathbf{q}}\,\pi_{\theta}^{+}(\mathbf{a}|\mathbf{q})}{1 - r_{\mathbf{q}}} \quad \text{(Sec. 3.2)}$$

这使得对负样本的最大似然训练可以直接转化为对正策略 $\pi_{\theta}^{+}$ 的梯度更新。联合正负样本，NFT 的序列级损失为：

$$\mathcal{L}_{(a,q,r)\sim\mathcal{D}}^{\mathrm{NFT}}(\theta) = r\left[-\log\frac{\pi_{\theta}^{+}(a|q)}{\pi_{\mathrm{old}}(a|q)}\right] + (1-r)\left[-\log\frac{1 - r_q\frac{\pi_{\theta}^{+}(a|q)}{\pi_{\mathrm{old}}(a|q)}}{1 - r_q}\right] \quad \text{(Eq. 9)}$$

其中 $r\in\{0,1\}$ 为二元验证信号，$r_q$ 为问题 $q$ 的采样正确率。正样本项（$r=1$）是标准的似然比最大化；负样本项（$r=0$）通过隐式负策略将错误答案的监督信号反向传播到正策略，迫使模型降低错误路径的概率。

### 3.3 实用化设计：Token 级损失、裁剪与加权

为降低序列长度带来的方差并提升训练稳定性，NFT 将 Eq. 9 分解为 token 级损失。定义每个 token 的似然比：

$$R_{\theta}^{t}(q,a) = \frac{\pi_{\theta}^{+}(a_t|q,a_{<t})}{\pi_{\mathrm{old}}(a_t|q,a_{<t})}$$

实际采用的 NFT 损失为：

$$\mathcal{L}_{\mathcal{D}}^{\mathrm{NFT}}(\theta) = -\sum_{q,a,r} \omega(q) \sum_{t} \left[ r \log R_{\theta}^{t}(q,a) + (1-r) \log \max\nolimits_{-v}\!\left(\frac{1 - \hat{r}_q R_{\theta}^{t}(q,a)}{1 - \hat{r}_q},\,\epsilon\right) \right] \quad \text{(Eq. 10)}$$

其中：
- **$\hat{r}_q = \frac{1}{K}\sum_{a|q} r(q,a)$**：对问题 $q$ 采样的 $K$ 个答案的经验正确率，用于参数化隐式负策略。
- **$\epsilon > 0$**：负似然比的最小裁剪值，防止对错误答案的过度惩罚导致训练崩溃。消融实验表明 $\epsilon=1.0$ 时性能最优（见 Figure 10），过小的 $\epsilon$ 会因激进惩罚而损害整体表现。裁剪后使用直通梯度（straight-through gradient）保持梯度流。
- **$\omega(q)$**：问题难度加权函数。困难问题（$\hat{r}_q$ 低）被赋予更高权重，可选方案包括 $\omega(q)=1-\hat{r}_q$ 或 $\omega(q)=\sqrt{(1-\hat{r}_q)/\hat{r}_q}$，两者性能相近且均优于均匀加权（见 Figure 9）。

### 3.4 数据收集与训练流程

NFT 的在线训练循环（Algorithm 1）包含以下关键步骤：
1. **采样**：对每个问题 $q$，从当前策略 $\pi_{\theta}$ 采样 $K$ 个答案。
2. **标注**：使用验证器标注每个答案的正确性 $r(q,a)\in\{0,1\}$，计算 $\hat{r}_q$ 和旧策略似然。
3. **过滤**：仅保留 $0<\hat{r}_q<1$ 的问题（排除全对或全错的提示），确保正负样本同时存在。
4. **优化**：在过滤后的数据上按 Eq. 10 更新策略参数 $\theta$。

整个流程不依赖奖励模型的标量输出，仅需二元验证信号，且无需维护额外的价值网络或负策略模型，保持了监督学习的简洁性。

## 实验与分析

### 主实验结果

NFT 在 7B 和 32B 规模的数学推理基准上进行了系统评估，与监督学习基线 RFT、偏好对齐方法 Iterative DPO，以及主流 RL 算法 GRPO、Dr. GRPO 和 DAPO 进行了全面对比。所有算法基于相同的数据集（DAPO-Math-17k）、基础设施和通用超参数实现，确保了算法维度的公平比较。

**7B 模型表现。** 在 Qwen2.5-Math-7B 上，NFT 在六个数学基准上的平均准确率达到 51.7，略优于 SOTA RL 算法 DAPO（51.2），并显著超越 SL 基线 RFT（48.3），相对提升 3.4 个百分点。在 AMC23 基准上，NFT 的优势尤为突出，达到 88.5，分别比 DAPO 和 RFT 高出 3.5 和 8.8 个百分点（Table 1）。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_ujBrsQm6Zu/figures/007_Table_1.jpg]]
*Table 1: NFT performs competitively compared with other algorithms. We report avg@32 for AIME24, AIME25, and AMC23 and avg@1 for others. Numbers within 1 % of the max are bolded*

**32B 模型表现。** 在 Qwen2.5-32B 上，NFT 平均准确率为 59.2，与 DAPO（59.9）基本持平（差距在 1% 以内），同时大幅领先 RFT（52.8），相对提升 6.4 个百分点。这表明 NFT 在更大规模模型上仍保持竞争力，且负反馈的利用在更大模型中收益更为显著。

**训练动态。** 训练曲线（Figure 6, 7）揭示了各算法的收敛特性：RFT 的验证准确率较早趋于平台期，而 NFT 和 DAPO 则持续攀升至更高水平。值得注意的是，RFT 在训练过程中生成熵持续下降，而 NFT 和 DAPO 则鼓励熵的增加（Figure 8），表明负样本的引入显著提升了模型的探索能力。这种探索能力的提升在大模型上更为明显——32B 实验中 NFT 和 DAPO 的熵增长幅度远大于 7B 实验。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_ujBrsQm6Zu/figures/009_Figure_6.jpg]]
*Figure 6: Training and validation accuracy curves for 7B experiments. We conducted 3-4 random and independent experiments for each algorithm and report their mean ± std results. Figure 7: Average accuracy across 6 benchmarks for 32B experiments. More curves in Appendix D. ure 6 and 11 present training curves across multiple runs. NFT exhibits convergence speed and final performance on par with DAPO, further supporting its stability*

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_ujBrsQm6Zu/figures/010_Figure_8.jpg]]
*Figure 8: Entropy curves for 7B and 32B runs*

### 消融实验

**提示加权策略。** 研究对比了三种加权方案：均匀加权 ω(q)=1、线性困难加权 ω(q)=1-ŕ_q，以及平方根加权 ω(q)=√((1-ŕ_q)/ŕ_q)。结果显示（Figure 9），两种困难加权策略性能相近，均持续优于均匀加权。这表明优先学习困难问题（正确率低的问题）对模型性能有正向贡献。平方根加权方案在理论上与 GRPO 的梯度形式对齐，提供了 NFT 与 RL 方法之间的另一层联系。

![[assets/figures/papers/paper_list_l26_https_openreview_net_forum_id_ujBrsQm6Zu/figures/012_Figure_9.jpg]]
*Figure 9: Effect of prompt weighting*

**负似然比裁剪值。** 裁剪值 ϵ 控制对负样本的惩罚上限。实验表明（Figure 10），ϵ=1.0 为最优设置。当 ϵ→0 时，算法对负样本施加过度惩罚，导致整体性能下降。这一发现揭示了负反馈利用中的关键权衡：适度惩罚错误有助于策略改进，但过度压制负样本的似然比会损害模型的学习能力。默认采用 ϵ=1.0 有效避免了这一陷阱。

### 负反馈的贡献拆解

一个值得关注的发现是：在 32B 模型中，RFT（仅使用正样本）已经能够提供总增益的约 80%，而负反馈仅贡献剩余的约 20%。这一现象提出了一个开放问题：负样本的作用是否在某些场景下被高估？当前证据表明，负反馈的价值在大模型上可能更多地体现在维持探索能力（熵不衰减）而非直接提升准确率上，但其完整机制仍需进一步研究。

### 关键图表结论

- **Table 1**：NFT 在 7B 和 32B 上匹配或超越 SOTA RL 算法，显著优于 SL 基线。
- **Figure 6/7**：NFT 的训练曲线与 DAPO 高度一致，验证准确率持续增长，而 RFT 较早停滞。
- **Figure 8**：熵曲线揭示 NFT 和 DAPO 鼓励探索，RFT 则导致熵衰减——这解释了 SL 基线在在线自改进场景中的根本劣势。
- **Figure 9/10**：困难问题加权和适度的负似然比裁剪是 NFT 有效性的关键设计选择。

## 方法谱系与知识库定位

### 1. 方法谱系：SL 与 RL 之间的第三条路径

NFT 的核心定位是桥接监督学习（SL）与强化学习（RL）两大范式，形成在线微调算法谱系中的第三条路径（Figure 1）。理解这一谱系需要从两种范式的根本差异出发：

**SL 路径的瓶颈**：以 **Rejection Fine-Tuning（RFT）**（Yuan et al., 2023b; Dong et al., 2023）为代表的监督学习基线仅使用正样本进行最大似然训练，丢弃所有负样本。其根本缺陷在于：依赖参考答案且无法利用错误样本进行自我反思，导致在在线自改进场景中探索能力持续衰减（Figure 8 中 RFT 的熵曲线单调下降），性能显著落后于 RL 方法。

**RL 路径的优势与代价**：以 **GRPO**（Shao et al., 2024）及其变体 **Dr. GRPO**（Liu et al., 2025b）、**DAPO**（Yu et al., 2025）为代表的策略梯度方法，通过组归一化优势估计和重要性采样，能够同时利用正负样本进行策略优化，展现出更强的探索能力（熵增加）。然而，RL 方法需要精心设计的奖励塑形、优势估计和裁剪机制，训练过程对超参数敏感。

**偏好对齐路径的局限**：以 **Iterative DPO / InfoNCA**（Rafailov et al., 2023; Chen et al., 2024）为代表的偏好对齐方法使用成对比较损失进行在线训练，但其需要构造偏好对，在处理 K>2 响应时需要 InfoNCA 等扩展损失，且 β 参数需要额外扫描调优。

NFT 的关键创新在于：**通过构造隐式负策略（implicit negative policy），将负样本的建模参数化为正策略的函数**，使得对负样本的最大似然训练直接等价于优化正策略。这一设计打破了"SL 无法从错误中学习"的传统认知，使监督学习也能有效利用验证信号，在保持 SL 简洁性的同时获得了 RL 级别的性能。

### 2. 核心机理：策略耦合与隐式参数化

NFT 的理论根基建立在正策略与负策略之间的严格线性耦合关系上。给定旧策略 $\pi_{\mathrm{old}}$ 和问题级正确率 $r_{\mathbf{q}}$，正策略 $\pi^{+}$ 和负策略 $\pi^{-}$ 满足：

$$r_{\mathbf{q}} \pi^{+}(\mathbf{a}|\mathbf{q}) + [1-r_{\mathbf{q}}] \pi^{-}(\mathbf{a}|\mathbf{q}) = \pi_{\mathrm{old}}(\mathbf{a}|\mathbf{q})$$

这一恒等式（Eq. 7）使得负策略可以完全由正策略表示，无需额外模型：

$$\pi_{\theta}^{-}(\mathbf{a}|\mathbf{q}) := \frac{\pi_{\mathrm{old}}(\mathbf{a}|\mathbf{q}) - r_{\mathbf{q}} \pi_{\theta}^{+}(\mathbf{a}|\mathbf{q})}{1 - r_{\mathbf{q}}}$$

基于此，NFT 的序列级损失（Eq. 9）将正负样本统一为对正策略的优化目标，其最优解收敛于真实正分布 $\pi^{+}$（Theorem 3.1，证明见 Appendix A）。

### 3. 与 GRPO 的理论等价性

一个深刻的理论发现是：**NFT 与 GRPO 在严格 on-policy 训练下梯度等价**（Proposition 4.2，证明见 Appendix A.4），尽管两者的理论根基完全不同——NFT 源自监督学习的最大似然框架，GRPO 源自策略梯度定理。当 $R_{\theta}^{t}(\mathbf{q}, \mathbf{a}) = 1$（即 on-policy 状态）时，两者的梯度表达式完全一致。

然而，在 off-policy 状态下两者产生分歧（Figure 4 展示了梯度权重的差异），这解释了为何实践中 NFT 与 DAPO 的性能互有胜负（Table 1：7B 上 NFT 51.7 vs DAPO 51.2；32B 上 NFT 59.2 vs DAPO 59.9），而非完全一致。

### 4. 关键设计选择与消融证据

NFT 引入了两个对 SL 范式而言非传统的设计选择，其有效性已通过消融实验验证：

**困难问题加权**：通过 $\omega(q) = 1 - \hat{r}_q$ 或 $\omega(q) = \sqrt{(1 - \hat{r}_q)/\hat{r}_q}$ 为低正确率问题分配更高权重，两种方案性能相近且均优于均匀加权（Figure 9）。这一设计与 GRPO 中组归一化优势的隐式加权机制形成呼应。

**负似然比裁剪**：对负样本的似然比施加最小值裁剪 $\epsilon$，并使用直通梯度（straight-through gradient）保持梯度流。当 $\epsilon \to 0$ 时，算法会对负样本施加过度惩罚，导致性能下降；默认设置 $\epsilon = 1.0$ 时性能最佳（Figure 10）。

### 5. 适用边界与局限

**已验证的适用范围**：
- 数学推理任务（AIME24/25、AMC23、MATH500、Minerva、OlympiadBench）
- 7B 和 32B 规模模型（基于 Qwen2.5-Math）
- 二进制奖励验证器（答案对/错）
- 在线自生成数据场景

**已知局限**：
1. **连续奖励未经验证**：尽管理论上可扩展至连续奖励（Appendix B），但尚未在大规模连续奖励场景下进行实验验证。
2. **负反馈潜力未充分挖掘**：在 32B 模型中，RFT 提供了总增益的约 80%，负反馈仅贡献约 20%，暗示负样本的作用可能被高估或其利用方式仍有改进空间。
3. **off-policy 行为理解不足**：NFT 与 GRPO 在 off-policy 设置下性能差异的完整机制仍需进一步研究。

### 6. 开放问题

1. **负反馈的规模化利用**：如何进一步挖掘负反馈的潜力，使其在大规模模型中带来更大的性能提升？当前 32B 模型中负反馈的边际贡献有限，是否存在更有效的负样本利用策略？

2. **任务泛化能力**：NFT 的隐式负策略框架能否推广到除数学推理外的其他生成式任务（如代码生成、长文本推理）？其有效性是否依赖于答案可自动验证的任务特性？

3. **连续奖励下的实际表现**：在连续奖励或更细粒度的反馈信号（如部分正确性评分、过程奖励）下，NFT 的实际表现如何？隐式负策略的参数化是否需要调整？

4. **RFT 基线的强势表现**：为何 RFT 在 32B 模型中能够提供总增益的 80%？这是否意味着在大规模模型中，简单的正样本复用已经捕获了大部分改进空间，负样本的边际价值被高估？

## 原文 PDF

![[paperPDFs/ICLR_2026/NFT_Bridging_Supervised_Learning_and_Reinforcement_Learning_in_Math_Reasoning.pdf]]
