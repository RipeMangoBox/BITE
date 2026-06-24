---
title: "Token-Importance Guided Direct Preference Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Token_Importance_Guided_Direct_Preference_Optimization.pdf
openreview_forum_id: cMEnMVvMw9
aliases:
- TD
- TIGDPO
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "通过梯度归因与高斯先验混合的令牌重要性权重分配机制，搭配结构化三元组损失，在令牌级别精确调节偏好信号。"
primary_logic: "精确识别并加权关键令牌，可以过滤非关键令牌带来的噪声；三元组损失在连续语义空间中拉近生成输出与首选响应、拉远与非首选响应的距离，从而实现更稳定、更细粒度的人类偏好对齐。"
claims:
- "TI-DPO 采用混合加权机制，结合梯度归因和高斯先验，确保令牌重要性评分的准确性和鲁棒性。"
- "TI-DPO 使用三元组损失提供结构化优化指导，显式拉近生成输出与首选响应、拉远与非首选响应的距离。"
- "高斯先验被设计用于修正 Transformer 的 U 型注意力偏差，防止优化忽略响应中段的语义核心。"
- "理论证明 TI-DPO 比 DPO 具有更紧的损失上界（定理 2），且最优策略的期望奖励严格占优（定理 3）。"
---

# Token-Importance Guided Direct Preference Optimization

> [!tip] 核心洞察
> 精确识别并加权关键令牌，可以过滤非关键令牌带来的噪声；三元组损失在连续语义空间中拉近生成输出与首选响应、拉远与非首选响应的距离，从而实现更稳定、更细粒度的人类偏好对齐。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于令牌重要性引导的直接偏好优化 |
| 英文题名 | Token-Importance Guided Direct Preference Optimization |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=cMEnMVvMw9); [GitHub](https://github.com/gracefulning/TIDPO) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | TI-DPO |
| Dataset | MMLU, GSM8K, GPQA, HumanEval |

> [!tip] 效果简介
> - MMLU 上，Accuracy 为 69.3，对比 65.3 (DPO avg)，变化 +4.0。
> - GSM8K 上，Accuracy 为 72.3，对比 69.3 (DPO avg)，变化 +3.0。
> - GPQA 上，Accuracy 为 25.3，对比 24.0 (DPO avg)，变化 +1.3。

## 概述

大语言模型的对齐训练普遍依赖从人类偏好数据中学习，但主流方法如 **DPO**（Rafailov et al., 2023）在序列级别进行优化，隐式地将每个令牌视为同等重要。这一简化带来了两个连锁瓶颈：**关键令牌的信号被非关键令牌的噪声淹没**，导致训练不稳定且对标注噪声敏感；同时，现有令牌级方法（如 **TDPO**、**TIS-DPO**）依赖有偏的概率代理或简化的加权方案，无法精细刻画人类偏好的令牌级结构。

TI-DPO 的核心思路是：**精确识别并加权关键令牌，可以过滤非关键令牌带来的噪声，从而实现更稳定、更细粒度的人类偏好对齐**。为此，方法引入了一个**令牌重要性引导的直接偏好优化**框架，其因果调节旋钮包含两个协同组件：

1. **混合加权机制**：将梯度归因分数与高斯先验进行凸组合（Eq. 8），梯度归因通过反向传播捕获每个令牌对模型最终预测的因果贡献，而高斯先验则显式对抗 Transformer 的“U型注意力偏差”（Lost-in-the-Middle），防止优化忽略响应中段的语义核心。
2. **结构化三元组损失**：以策略模型动态生成的输出为锚点，在连续语义空间中拉近与首选响应的距离、拉远与非首选响应的距离，提供令牌级 DPO 损失之外的显式结构化指导。

理论层面，TI-DPO 被证明具有比 DPO 更紧的损失上界（定理 2），且最优策略的期望奖励严格占优（定理 3）。

实验在三个基座模型（LLaMA-3.2-3B、LLaMA-3.1-8B、Mistral-7B-v0.3）上，与 SFT、DPO、IPO、KTO、SimPO、TDPO、CPO、TPO、GRPO 等 10 个基线方法进行了对比。TI-DPO 在六个评估维度上取得领先：

- **HumanEval**：67.0（DPO 平均 61.0，+6.0）
- **TruthfulQA**：62.0（DPO 平均 56.7，+5.3）
- **IFEval**：75.7（DPO 平均 70.0，+5.7）
- **MMLU**：69.3（DPO 平均 65.3，+4.0）
- **GSM8K**：72.3（DPO 平均 69.3，+3.0）
- **GPQA**：25.3（DPO 平均 24.0，+1.3）

消融实验（Table 2）证实：移除三元组损失导致数学和代码分数显著下降；移除高斯先验则明显损害可靠性分数。此外，TI-DPO 在标签噪声下的鲁棒性（Table B8）和生成多样性（Table B9）均优于 DPO 和 TPO。

方法的主要代价在于训练阶段：混合权重需要一次额外的反向传播计算梯度归因，导致单轮训练时间约为标准 DPO 的两倍，但不影响推理速度。在知识密集型推理任务（MMLU、GSM8K）上，TI-DPO 可能不及 GRPO/TPO 等序列级优化方法；但在对细粒度语义控制要求高的指令跟随、真实性和代码生成任务上表现突出。

## 背景与动机

### 大语言模型对齐与偏好优化

将大语言模型（LLM）的行为与人类偏好对齐，是构建安全、有用 AI 系统的核心挑战。当前主流范式遵循“从人类反馈中强化学习”（RLHF）框架，通常分为两个阶段：首先训练一个奖励模型来近似人类偏好，然后使用强化学习（如 PPO）优化策略模型以最大化该奖励。然而，RLHF 流程复杂、训练不稳定，且奖励模型本身可能遭受“奖励黑客”问题。

**直接偏好优化**（DPO，Rafailov et al., 2023）通过将奖励函数重新参数化为策略模型与参考模型的对数比，跳过了显式奖励建模步骤，直接在人类偏好数据上优化策略。其核心损失函数为：

$$
\mathcal{L}_{\mathrm{DPO}} = -\mathbb{E}_{(x,y_{\mathrm{w}},y_{\mathrm{l}})\sim\mathcal{D}}\left[\log\sigma\left(\beta\left(\log\frac{\pi_{\theta}(y_{\mathrm{w}}|x)}{\pi_{\mathrm{ref}}(y_{\mathrm{w}}|x)}-\log\frac{\pi_{\theta}(y_{\mathrm{l}}|x)}{\pi_{\mathrm{ref}}(y_{\mathrm{l}}|x)}\right)\right)\right]
$$

该公式通过对比首选响应 $y_{\mathrm{w}}$ 与非首选响应 $y_{\mathrm{l}}$ 的对数概率比来优化策略，极大简化了训练流程。

### 序列级优化的根本瓶颈

尽管 DPO 取得了显著成功，但其优化机制存在一个根本性缺陷：**它在序列级别进行优化，隐式地将响应中所有令牌视为同等重要**。这一假设与人类偏好的实际形成机制严重不符——人类在评估一段回复时，通常仅由少数关键令牌（如事实性陈述、逻辑转折词、代码中的关键变量名）决定整体偏好判断，而大量功能性或冗余令牌对偏好信号几乎没有贡献。

这种令牌级重要性的缺失导致两个直接后果：

1. **训练不稳定**：非关键令牌上的梯度噪声干扰优化方向，使模型在训练过程中出现性能波动甚至退化。
2. **数据噪声敏感**：当偏好数据中存在标注噪声时，序列级优化无法区分噪声来源，导致模型学习到错误的偏好模式。

### 现有令牌级方法的不足

为缓解上述问题，近期研究开始探索令牌级别的偏好优化方法，如 **TDPO**（Zeng et al., 2024）和 **TIS-DPO**（Liu et al., 2024a）。但这些方法存在明显的局限性：

- **依赖有偏的概率代理**：部分方法使用策略模型自身输出的概率作为令牌重要性指标，但这在训练初期极不可靠，形成“用有偏模型指导自身优化”的循环。
- **简化加权方案**：另一些方法采用固定的位置加权（如线性衰减），无法适应不同任务和上下文中令牌重要性的动态变化。
- **忽视架构偏置**：Transformer 架构存在固有的“U 型注意力偏置”（Lost-in-the-Middle 现象），即模型天然倾向于关注序列首尾而忽略中段。现有令牌级方法未对此进行显式修正，导致响应中段的语义核心被系统性忽视。

### 结构化优化的缺失

此外，现有 DPO 变体（包括令牌级方法）的优化目标本质上是一个二分类对比任务——仅要求模型区分首选与非首选响应。这种目标缺乏对生成输出本身的直接结构化约束：它没有显式地要求模型生成的输出在语义空间中靠近首选响应、远离非首选响应。在连续偏好空间中，这种“拉近-推远”的结构化信号对于细粒度对齐至关重要。

### 本文动机

针对上述缺口，本文提出 **TI-DPO**（Token-Importance Guided Direct Preference Optimization），核心动机在于：

- **精确令牌加权**：设计一种不依赖模型自身概率的、客观的令牌重要性估计机制，使优化聚焦于真正影响人类偏好的关键令牌。
- **架构偏置修正**：显式对抗 Transformer 的 U 型注意力偏置，确保响应中段的语义核心不被忽略。
- **结构化优化信号**：引入三元组损失，在连续语义空间中提供“拉近-推远”的结构化约束，超越简单的二分类对比。

通过这三个维度的改进，TI-DPO 旨在实现更稳定、更细粒度、对噪声更鲁棒的人类偏好对齐。

## 核心创新

TI-DPO 的核心创新在于将传统 DPO 的序列级优化解构为**令牌级加权对比**与**结构化三元组约束**的双重机制，通过两个关键改变槽（changed slots）实现更精细的人类偏好对齐。

### 改变槽一：令牌重要性加权（Token Importance Weighting）

基线 DPO 及其多数变体对响应序列中的所有令牌赋予隐式均匀权重（均为 1），导致非关键令牌（如功能词、标点）与语义核心令牌在损失函数中获得相同的优化信号。这种粗粒度处理不仅引入噪声，还使得模型在训练中对数据扰动敏感。

TI-DPO 将这一均匀加权替换为**梯度归因分数与高斯先验的凸组合**：

$$
W = \lambda \cdot \mathcal{T}_{\mathrm{norm}} + (1 - \lambda) \cdot \mathcal{P}_{\mathrm{prior}} \quad \text{(Eq. 8)}
$$

该混合权重由两个互补组件构成：

1. **梯度归因（Gradient Attribution）**：以最终位置的最大 logit 为目标（$\mathcal{L}_{\mathrm{target}} = \max(L_{T-1})$，Eq. 5），计算其对每个令牌嵌入的梯度，取 L1 范数作为原始重要性得分（$I_i = \|\nabla_{e_i} \mathcal{L}_{\mathrm{target}}\|_1$，Eq. 6）。这一机制从因果角度捕捉每个令牌对模型最终预测的贡献程度。

2. **高斯先验（Gaussian Prior）**：$\mathcal{P}_{\mathrm{prior}}(t) = \exp\left(-\frac{1}{2}\left(\frac{t - \mu}{\sigma}\right)^2\right)$（Eq. 7），其中 $\mu = (T-1)/2$，$\sigma = T/4$。该先验在序列中心达到峰值、两端衰减，专门用于对抗 LLM 架构固有的“Lost-in-the-Middle”注意力偏置——即 Transformer 对序列首尾令牌过度关注、对中间语义核心关注不足的 U 型注意力模式。

两者的凸组合由超参数 $\lambda \in [0, 1]$ 控制。梯度归因提供数据驱动的精确性，高斯先验提供结构化的鲁棒性，二者协同确保关键令牌获得高权重，同时避免梯度归因在噪声样本上的不稳定。

### 改变槽二：优化目标（Optimization Objective）

基线 DPO 的优化目标为序列级的二分类对比损失（Eq. 3），仅比较完整首选响应与非首选响应的对数概率比。TI-DPO 将其扩展为**加权令牌级 DPO 损失与结构化三元组损失的联合优化**：

$$
\mathcal{L}_{\mathrm{TI-DPO}} = \mathcal{L}_{\mathrm{DPO-w}} + \gamma \, \mathcal{L}_{\mathrm{triplet}} \quad \text{(Eq. 14)}
$$

其中：

- **加权令牌级 DPO 损失**（$\mathcal{L}_{\mathrm{DPO-w}}$，Eq. 12）：将令牌重要性权重 $w_t^{\mathrm{w}}$ 和 $w_t^{\mathrm{l}}$ 嵌入到 DPO 的对数比求和过程中，使优化信号集中在关键令牌上，过滤非关键令牌的噪声。

- **三元组损失**（$\mathcal{L}_{\mathrm{triplet}}$，Eq. 13）：以当前策略模型动态生成的输出作为锚点（anchor），在连续语义空间中显式拉近锚点与首选响应（正例）的距离，同时推远与非首选响应（负例）的距离，并以预设 margin $\alpha$ 约束。这一结构化约束弥补了 DPO 损失仅做二分类对比的不足，为模型提供更细粒度的方向性指导。

### 理论支撑

TI-DPO 的创新不仅体现在工程层面，还获得了严格的理论保证：

- **更紧的损失上界**（Theorem 2）：$\mathcal{L}_{\mathrm{TI-DPO}} \leq \mathcal{L}_{\mathrm{DPO}} - \frac{1}{2} \kappa \Delta_{\sigma^2}$，TI-DPO 的期望损失被 DPO 损失严格上界，差值正比于方差减少量。其根源在于令牌加权抑制了非关键令牌的梯度方差（Lemma 1：$\sigma_{TI-DPO}^2 < \sigma_{DPO}^2$）。

- **最优策略的奖励占优**（Theorem 3）：在固定总 KL 散度约束下，TI-DPO 最优策略的期望真实奖励严格高于 DPO 策略，即 $\mathbb{E}_{\boldsymbol{y}\sim\pi_{\mathrm{TI-DPO}}}[r^*(\boldsymbol{x},\boldsymbol{y})] \ge \mathbb{E}_{\boldsymbol{y}\sim\pi_{\mathrm{DPO}}}[r^*(\boldsymbol{x},\boldsymbol{y})] + \delta$。这是因为 TI-DPO 将 KL 预算集中于关键令牌，避免在非关键令牌上浪费优化容量。

### 与传统令牌级方法的区别

相较于已有的令牌级方法（如 **TDPO**（Zeng et al., 2024）依赖有偏的概率代理、**TIS-DPO**（Liu et al., 2024a）采用简化的启发式加权），TI-DPO 的混合权重机制首次将因果梯度归因与架构感知先验相结合，同时引入三元组损失提供结构化优化信号，实现了从“令牌级加权”到“令牌级结构化对齐”的跨越。

## 整体框架

TI-DPO 的核心思想是将序列级的偏好优化细化为令牌级的结构化对齐，其整体架构由三个关键设计串联而成：**令牌重要性加权机制**、**加权 DPO 损失**和**结构化三元组损失**。整个框架遵循“识别关键令牌 → 加权偏好优化 → 结构化语义拉近/推远”的级联逻辑。

### 输入与数据流

对于每个训练样本，系统接收一个三元组 $(x, y_w, y_l)$，其中 $x$ 为输入提示，$y_w$ 为人类偏好的首选响应，$y_l$ 为非首选响应。数据流依次经过以下模块：

1. **令牌重要性评分**：对 $y_w$ 和 $y_l$ 中的每个令牌，分别计算其重要性权重。该模块由两个子组件协同工作：
   - **梯度归因**：以最终步的最大 logit 为目标 $\mathcal{L}_{\mathrm{target}} = \max(L_{T-1})$，计算该目标对每个令牌嵌入的梯度，并取 L1 范数作为原始重要性得分 $I_i = \|\nabla_{e_i} \mathcal{L}_{\mathrm{target}}\|_1$。这捕捉了每个令牌对模型预测的因果贡献。
   - **高斯先验**：为对抗 Transformer 架构固有的 “Lost-in-the-Middle” 偏置（即模型倾向于关注序列首尾而忽略中间语义核心），引入中心峰值的高斯先验分布 $\mathcal{P}_{\mathrm{prior}}(t) = \exp\left(-\frac{1}{2}\left(\frac{t-\mu}{\sigma}\right)^2\right)$，确保响应中段的令牌获得非零基线权重。
   - **混合加权**：将归一化后的梯度得分 $\mathcal{T}_{\mathrm{norm}}$ 与高斯先验 $\mathcal{P}_{\mathrm{prior}}$ 进行凸组合，得到最终令牌权重 $W = \lambda \cdot \mathcal{T}_{\mathrm{norm}} + (1-\lambda) \cdot \mathcal{P}_{\mathrm{prior}}$，超参数 $\lambda \in [0,1]$ 控制两者的平衡。

2. **加权 DPO 损失**：利用上述令牌权重，对策略模型 $\pi_\theta$ 与参考模型 $\pi_{\mathrm{ref}}$ 的对数比进行令牌级加权求和，得到加权奖励差 $\Delta r_{\mathrm{token}}$，进而构建加权 DPO 损失 $\mathcal{L}_{\mathrm{DPO-w}}$。关键令牌的偏好信号被放大，而非关键令牌的噪声被抑制。

3. **三元组损失**：以当前策略模型动态生成的输出为锚点 $y$，在连续语义空间中计算锚点与 $y_w$（正例）和 $y_l$（负例）的嵌入距离，施加经典三元组约束：锚点与正例的距离必须比与负例的距离至少小一个预设 margin $\alpha$。该损失显式拉近生成输出与首选响应的语义距离，同时推远与非首选响应的距离。

4. **联合优化**：最终目标函数为上述两个损失的线性组合：
   $$\mathcal{L}_{\mathrm{TI-DPO}} = \mathcal{L}_{\mathrm{DPO-w}} + \gamma \mathcal{L}_{\mathrm{triplet}}$$
   其中 $\gamma$ 控制三元组损失的相对权重。

### 模块关系与设计意图

三个核心模块形成互补的分工：

- **混合加权模块**解决“哪些令牌重要”的问题。梯度归因提供细粒度的因果信号，但单独使用可能受 Transformer U 型注意力偏置的影响；高斯先验作为结构正则项，确保响应中段的语义核心不被忽略。两者的凸组合在准确性与鲁棒性之间取得平衡。
- **加权 DPO 损失**解决“如何利用重要性信号进行偏好优化”的问题。它将传统 DPO 的序列级对比细化为令牌级加权对比，使得优化聚焦于关键令牌的选择，降低无关令牌带来的方差。理论证明（定理 2）表明，该设计使 TI-DPO 的期望损失严格小于标准 DPO，差值正比于方差减少量。
- **三元组损失**解决“如何结构化地引导生成方向”的问题。它不依赖显式奖励模型，而是直接在策略模型自身的嵌入空间中施加距离约束，提供更精细的优化指导。消融实验证实，移除三元组损失会导致数学和代码任务分数显著下降。

### 训练与推理的分离

值得注意的是，梯度归因计算仅在训练阶段引入额外开销（约 2 倍于标准 DPO 的单轮训练时间），推理阶段不涉及任何梯度计算或令牌权重估计，因此 TI-DPO 的推理速度与标准 DPO 对齐的模型完全一致。

## 核心模块与公式推导

TI-DPO 的核心由两个相互配合的机制构成：**令牌重要性加权**与**结构化三元组损失**。前者解决“哪些令牌对偏好信号更关键”的问题，后者在连续语义空间中提供细粒度的优化引导。

### 令牌重要性加权机制

传统 DPO 在序列级别优化，隐含地假设所有令牌对偏好信号的贡献均等。TI-DPO 通过在令牌级马尔可夫决策过程（Token-Level MDP）框架下引入显式的重要性权重，打破了这一假设。权重计算分为三步：

**第一步：梯度归因（Gradient Attribution）。** 对于首选响应 $y_w$ 中的每个令牌 $i$，计算模型最终位置的最大 logit 对该令牌嵌入 $e_i$ 的梯度，并取 L1 范数作为原始重要性得分：

$$I_i = \|\nabla_{e_i} \mathcal{L}_{\mathrm{target}}\|_1 = \sum_k |(\nabla_{e_i} \mathcal{L}_{\mathrm{target}})[k]| \quad \text{(Eq. 6)}$$

其中 $\mathcal{L}_{\mathrm{target}} = \max(L_{T-1})$ 为最终步 logit 的最大值（Eq. 5）。直觉上，若某令牌的微小扰动会引起模型最终预测的剧烈变化，则该令牌对输出语义贡献更大。

**第二步：高斯先验修正（Gaussian Prior）。** 大语言模型存在“Lost-in-the-Middle”偏置——对序列中段信息的关注度天然低于两端。为对抗这一架构偏置，引入中心峰值的高斯先验分布：

$$\mathcal{P}_{\mathrm{prior}}(t) = \exp\left(-\frac{1}{2}\left(\frac{t - \mu}{\sigma}\right)^2\right) \quad \text{(Eq. 7)}$$

其中 $\mu = (T-1)/2$，$\sigma = T/4$。该先验赋予序列中部令牌更高的基线权重，确保优化不会忽略响应的语义核心。

**第三步：凸组合（Hybrid Weighting）。** 最终令牌权重 $W$ 是归一化梯度得分 $\mathcal{T}_{\mathrm{norm}}$ 与高斯先验 $\mathcal{P}_{\mathrm{prior}}$ 的凸组合：

$$W = \lambda \cdot \mathcal{T}_{\mathrm{norm}} + (1 - \lambda) \cdot \mathcal{P}_{\mathrm{prior}} \quad \text{(Eq. 8)}$$

超参数 $\lambda \in [0, 1]$ 控制两者的平衡。这一混合设计使得权重既保留了梯度对语义关键性的敏锐感知，又具备高斯先验的结构稳定性，避免梯度噪声导致的权重估计偏差。

### 加权令牌级 DPO 损失

获得令牌权重后，将其注入 DPO 的对数比计算中。定义加权令牌级奖励差：

$$\Delta r_{\mathrm{token}} = \sum_{t=1}^{T_w} w_t^w \log \frac{\pi_\theta(y_w^t | x, y_w^{<t})}{\pi_{\mathrm{ref}}(y_w^t | x, y_w^{<t})} - \sum_{t=1}^{T_l} w_t^l \log \frac{\pi_\theta(y_l^t | x, y_l^{<t})}{\pi_{\mathrm{ref}}(y_l^t | x, y_l^{<t})}$$

其中 $w_t^w$、$w_t^l$ 分别为首选和非首选响应中第 $t$ 个令牌的混合权重。加权 DPO 损失为：

$$\mathcal{L}_{\mathrm{DPO-w}} = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( \beta \Delta r_{\mathrm{token}} \right) \right] \quad \text{(Eq. 12)}$$

关键区别在于：标准 DPO 对所有令牌的对数比求和后取均值（隐式均匀权重），而 $\mathcal{L}_{\mathrm{DPO-w}}$ 通过 $w_t^w$、$w_t^l$ 放大了关键令牌的优化信号，抑制了非关键令牌的噪声。

### 结构化三元组损失

仅靠加权 DPO 损失无法显式控制生成输出在语义空间中的相对位置。TI-DPO 引入三元组损失，以策略模型自身生成的响应为锚点：

$$\mathcal{L}_{\mathrm{triplet}} = \max\left(0, \|f(y) - f(y_w)\|_2^2 - \|f(y) - f(y_l)\|_2^2 + \alpha\right) \quad \text{(Eq. 13)}$$

其中 $y \sim \pi_\theta(\cdot | x, y_w)$ 是以首选响应为上下文、由当前策略动态生成的锚点响应；$f(\cdot)$ 为语义嵌入函数；$\alpha$ 为间隔超参数。该损失惩罚锚点与首选响应的距离大于与非首选响应距离的情况，显式地将生成输出拉向偏好方向、推离非偏好方向。

### 完整优化目标

TI-DPO 总损失为两者的联合优化：

$$\mathcal{L}_{\mathrm{TI-DPO}} = \mathcal{L}_{\mathrm{DPO-w}} + \gamma \mathcal{L}_{\mathrm{triplet}} \quad \text{(Eq. 14)}$$

其中 $\gamma$ 控制三元组损失的相对强度。理论分析表明，该目标具有比标准 DPO 更紧的损失上界（Theorem 2），且最优策略的期望奖励严格占优（Theorem 3）。

## 实验与分析

### 主要结果

TI-DPO 在三个基座模型（LLaMA-3.2-3B、LLaMA-3.1-8B、Mistral-7B-v0.3）上进行了系统评估，覆盖通用知识（MMLU）、数学推理（GSM8K）、专家推理（GPQA）、代码生成（HumanEval）、真实性（TruthfulQA）和指令跟随（IFEval）六个维度。Table 1 报告了各方法在三个基座模型上的平均得分。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/001_Table_1.jpg]]
*Table 1: Average scores of each fine-tuning method across three base models*

TI-DPO 取得 **62.3** 的平均总分，领先所有对比方法。具体而言，相较于标准 DPO（Rafailov et al., 2023），TI-DPO 在 HumanEval 上提升 **+6.0**（67.0 vs. 61.0），在 TruthfulQA 上提升 **+5.3**（62.0 vs. 56.7），在 IFEval 上提升 **+5.7**（75.7 vs. 70.0）。在 MMLU 和 GSM8K 上分别取得 **+4.0** 和 **+3.0** 的增益。GPQA 上的提升相对温和（+1.3），这与该任务高度依赖序列级逻辑一致性的特点一致。

训练动态曲线（Figure 1）进一步揭示了 TI-DPO 的收敛特性：在 TruthfulQA 上，TI-DPO 随训练步数持续稳定提升，最终超越所有基线；在 IFEval 上，TI-DPO 展现出显著的性能优势，且训练曲线波动小于多数对比方法，表明令牌级加权有效抑制了噪声令牌对优化的干扰。

多维能力雷达图（Figure 2）显示，TI-DPO 在指令跟随和真实性两个维度的归一化得分明显优于其他指令模型，而在数学推理维度与 TPO、GRPO 等方法互有高低。这一模式与方法的理论定位一致：令牌级精细加权天然适合对局部语义控制要求高的任务，而序列级优化方法在依赖全局逻辑一致性的推理任务上仍具竞争力。

### 消融实验

Table 2 以 LLaMA-3.2-3B-Instruct 为基座，系统拆解了 TI-DPO 各组件的贡献。全量 TI-DPO 在所有六个评估维度上均取得最高分，验证了各模块的协同必要性。

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/005_Table_2.jpg]]
*Table 2: Ablation study scores: the full TI-DPO vs. base instruction model (Llama-3.2-3B-Instruct) with other weight and triplet conditions*

**三元组损失的贡献**：移除三元组损失（w/o Triplet Loss）导致数学和代码分数显著下降——数学从 80.7 降至 79.0，代码从 33.0 降至 31.0。这表明三元组损失在连续语义空间中拉近生成输出与首选响应、拉远与非首选响应距离的结构化约束，对需要精确语义对齐的数学推理和代码生成任务尤为重要。

**高斯先验的贡献**：移除高斯先验（w/o Gaussian Prior）后，可靠性（Reliability）得分从 86.8 明显下降至 82.5。这直接验证了高斯先验对抗 Transformer “Lost-in-the-Middle”偏置的设计动机——若不显式增强响应中段的令牌权重，模型倾向于忽略语义核心，导致可靠性下降。

**权重策略对比**：均匀权重（Uniform Weight）和随机权重（Random Weight）变体均显著低于全量方法，证明令牌重要性分配必须是有信息量的，而非任意加权。Softmax 先验变体（w/ Softmax Prior）也不及高斯先验，说明中心峰值的高斯分布形状对对抗 U 型注意力偏置具有不可替代的作用。

### 令牌重要性权重的分布与可解释性

Figure 4 展示了六个基准任务中基于梯度归因的令牌重要性权重的分布模式。不同任务呈现出差异化的权重集中特征：代码生成（HumanEval）和指令跟随（IFEval）任务中，权重高度集中于少数关键令牌（如函数名、约束关键词），而非关键令牌的权重被有效抑制；知识密集型任务（MMLU、GPQA）中权重分布相对均匀，反映这些任务对全局信息的依赖。

Table B1 进一步量化了令牌重要性权重分布、性能提升幅度与样本级 Pearson 相关系数之间的关系。高权重令牌的集中度与任务性能提升呈正相关，表明 TI-DPO 的权重分配机制能够有效识别对偏好对齐贡献最大的令牌。

### 鲁棒性与泛化分析

**标签噪声鲁棒性**：Table B8 报告了不同标签噪声水平下的准确率。TI-DPO 在各噪声水平下均优于 DPO，且性能衰减斜率更平缓。令牌级加权机制天然具备噪声过滤能力——噪声令牌通常获得较低的重要性权重，从而减轻其对损失函数的污染。

**生成多样性**：Table B9 的 Self-BLEU 和 Distinct-n 指标显示，TI-DPO 在提升对齐质量的同时，未牺牲生成多样性。相较于部分基线方法（如 SimPO）出现的多样性塌缩，TI-DPO 的令牌级精细调控保持了输出的丰富性。

**收敛性**：Table B10 的训练损失曲线对比表明，TI-DPO 的损失下降更平滑且最终收敛值更低，与 Theorem 2 的理论上界一致——令牌加权降低了梯度估计方差，使优化过程更稳定。

### 超参数敏感性

Table B11 和 B12 分别分析了混合权重系数 λ 和三元组损失 margin α 的敏感性。λ 在 0.3–0.7 范围内性能稳定，极端值（λ=0 仅高斯先验，λ=1 仅梯度归因）均导致性能下降，验证了凸组合设计的必要性。α 在 0.1–0.5 范围内表现鲁棒，过大 margin 会使优化困难，过小则三元组约束失效。

### 失败模式与局限

尽管 TI-DPO 在多数任务上表现优异，但存在以下值得注意的边界：

1. **推理任务上的相对劣势**：在 GSM8K 和 GPQA 上，TI-DPO 不敌 GRPO（Shao et al., 2024）和 TPO（Saeidi et al., 2024）等序列级优化方法。令牌级加权可能割裂了推理链中令牌间的长程依赖关系，而 GRPO 的群体相对优化天然保留了序列的全局一致性。

2. **训练开销**：TI-DPO 的混合权重计算需要一次额外的反向传播用于梯度归因，导致单轮训练时间约为标准 DPO 的两倍。该开销仅存在于训练阶段，不影响推理速度，但在大模型和长序列场景下可能成为实际部署的瓶颈。

3. **偏见放大风险**：若训练偏好数据本身含有刻板印象，TI-DPO 的令牌权重机制可能将高权重分配给偏见令牌（如特定代词、形容词），从而强化而非缓解偏见。不过，这一权重的可解释性也为偏见检测提供了入口——高权重令牌可直接指向潜在的偏见来源，这是序列级方法难以做到的。

### 补充图表

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/009_Table_3.jpg]]
*Table 3: Table B1: Distribution of Token Importance Weight, Performance Improvement, and Sample-level Pearson Correlation Coefficient in Each Task*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/010_Table_4.jpg]]
*Table 4: Table B2: Token Importance Assignment of A*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/011_Table_5.jpg]]
*Table 5: Table B3: Token Importance Assignment of B*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/012_Table_6.jpg]]
*Table 6: Table B4: Token Importance Assignment of C*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/013_Table_7.jpg]]
*Table 7: Table B5: LLaMA-3.2-3B evaluation*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/014_Table_8.jpg]]
*Table 8: Table B6: LLaMA-3.1-8B evaluation*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/015_Table_9.jpg]]
*Table 9: Table B7: Mistral-7B-v0.3 evaluation*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/016_Table_10.jpg]]
*Table 10: Table B8: Accuracy under varying noise levels*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/017_Table_11.jpg]]
*Table 11: Table B9: Text generation diversity metrics*

![[assets/figures/papers/paper_list_l31_https_openreview_net_forum_id_cMEnMVvMw9/figures/018_Table_12.jpg]]
*Table 12: Table B10: Training loss comparison between DPO and TI-DPO over epochs*

## 方法谱系与知识库定位

### 1. 方法脉络与 TI-DPO 的定位

TI-DPO 的提出源于对现有偏好优化方法两个核心瓶颈的回应：**序列级优化的粒度不足**与**令牌级方法的权重偏差**。

**序列级基线**——以 **DPO**（Rafailov et al., 2023）为代表——将整个生成响应视为单一偏好单元进行对比优化，隐含假设所有令牌对偏好的贡献均等。这一简化导致两个后果：（1）非关键令牌（如功能词、标点）引入的噪声稀释了偏好信号的精度，使训练不稳定且对数据噪声敏感；（2）模型无法区分响应中不同语义单元的差异化重要性，难以实现细粒度的人类偏好对齐。后续改进如 **IPO**（Azar et al., 2024）和 **KTO**（Ethayarajh et al., 2024）分别在损失函数形式和偏好建模方式上做了调整，但本质上仍停留在序列级粒度。**SimPO**（Meng et al., 2024）引入了长度归一化，但未触及令牌重要性的差异化分配问题。**CPO**（Feng et al., 2025）和 **TPO**（Saeidi et al., 2024）分别从对比学习和令牌级概率比角度做了探索，但其令牌权重机制仍相对简化。

**令牌级基线**的尝试更为直接地触及核心问题。**TDPO**（Zeng et al., 2024）和 **TIS-DPO**（Liu et al., 2024a）开始为不同令牌分配不同权重，但其权重来源存在结构性偏差：TDPO 依赖概率代理信号（如策略模型对令牌的预测概率），这类信号本身受模型当前状态影响，存在自我强化的循环偏差风险；TIS-DPO 则采用相对简化的加权方案，缺乏对令牌重要性的精细刻画。

TI-DPO 的关键突破在于**权重来源的根本性改变**：通过梯度归因直接度量每个令牌对模型最终预测的因果影响，而非依赖有偏的概率代理。同时，引入高斯先验对抗 Transformer 架构固有的“Lost-in-the-Middle”偏置——该偏置使模型天然倾向于关注序列首尾而忽略中段的语义核心。这两个信号的凸组合（Eq. 8）形成了一种“因果信号 + 结构先验”的双重保障机制。

此外，TI-DPO 在损失函数层面引入了**结构化三元组损失**，这在偏好优化方法中并不常见。与 **GRPO**（Shao et al., 2024）通过群体相对比较进行优化的思路不同，TI-DPO 的三元组损失以策略模型动态生成的输出为锚点，在连续语义空间中显式拉近与首选响应的距离、推远与非首选响应的距离。这种结构化指导为优化过程提供了更明确的几何约束。

### 2. 适用边界与性能特征

TI-DPO 的性能优势呈现明显的**任务依赖性**，这直接反映了其令牌级机制的作用边界：

- **强项任务**：在需要细粒度语义控制的任务上表现突出。**IFEval**（指令跟随）上较 DPO 平均提升 5.7 个百分点，**HumanEval**（代码生成）提升 6.0 个百分点，**TruthfulQA**（真实性）提升 5.3 个百分点。这些任务中，响应的质量高度依赖于关键令牌（如指令约束词、代码逻辑节点、事实性陈述）的精确生成，TI-DPO 的加权机制恰好聚焦于这些关键令牌。

- **弱项任务**：在强烈依赖序列级逻辑一致性的任务上，TI-DPO 可能不及 **GRPO** 或 **TPO** 等序列级优化方法。具体表现为 **MMLU**（通用知识，+4.0）和 **GPQA**（推理，+1.3）的提升幅度相对较小。这些任务中，推理链的整体连贯性比单个令牌的精确性更为关键，令牌级加权的优势被部分稀释。

这一适用边界揭示了 TI-DPO 的核心设计取舍：**令牌级精确性优先于序列级整体性**。当任务对“说什么”的要求高于“如何组织”时，TI-DPO 的优势最为显著。

### 3. 局限与开放问题

**训练开销**是 TI-DPO 最直接的工程局限。混合权重计算需要额外一次反向传播来获取梯度归因信号，导致单轮训练时间约为标准 DPO 的两倍。该开销仅存在于训练阶段，不影响推理速度，但在大模型和长序列场景下仍是一个需要权衡的因素。是否存在更高效的梯度近似方法（如仅对部分层或部分令牌计算梯度）是一个待探索的方向。

**偏见风险**的双面性值得关注。若训练偏好数据本身包含偏见与刻板印象，TI-DPO 仍可能学习到这些模式。但其令牌权重机制提供了一种独特的可解释性入口：高权重令牌直接指示了模型强化了哪些偏见信号（如特定代词、形容词），这比序列级方法更容易定位偏见来源。能否利用这一特性实现**自动偏见检测与缓解**，是一个有潜力的开放问题。

**与群体优化方法的融合**是另一个值得探索的方向。GRPO 等基于群体的方法在推理任务上表现优异，其核心优势在于通过多个候选响应的相对比较进行优化。TI-DPO 的令牌重要性机制若能嵌入群体优化的框架中——例如在群体内对不同令牌进行差异化加权——可能实现推理能力与细粒度控制的互补增益。

**理论层面**，TI-DPO 已证明其损失上界比 DPO 更紧（Theorem 2）且最优策略的期望奖励严格占优（Theorem 3），但这些理论结果建立在令牌级 MDP 的框架假设之上。该框架与实际自回归生成过程之间的差距，以及高斯先验的最优参数选择与任务特性之间的关系，仍有进一步理论分析的空间。

## 原文 PDF

![[paperPDFs/ICLR_2026/Token_Importance_Guided_Direct_Preference_Optimization.pdf]]
