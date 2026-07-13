---
title: "RiskPO: Risk-based Policy Optimization with Verifiable Reward for LLM Post-Training"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/RiskPO_Risk_based_Policy_Optimization_with_Verifiable_Reward_for_LLM_Post_Training.pdf
project_link: null
code_link: https://github.com/RTkenny/RiskPO
openreview_forum_id: KjHB7rebQO
aliases:
- RRBPO
- RiskPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过引入风险度量（MVaR）和问题捆绑方案，将优化目标从均值转向奖励分布尾部，增强对困难问题的梯度信号。"
primary_logic: "将风险敏感目标引入LLM后训练，可缓解熵崩塌，促进探索，从而扩展推理边界，而非仅提升采样效率。"
claims:
- "RiskPO在硬级别数学推理基准上，平均Pass@1达到46.65，比最强基线DAPO（43.87）高+2.78，比GRPO（40.41）高+6.24。"
- "RiskPO在训练过程中维持显著更高的策略熵，有效缓解熵崩塌问题。"
- "在Pass@k指标上，RiskPO相对于GRPO的差距随k增大而扩大，表明模型扩展了推理边界而非仅仅提升采样效率。"
- "理论证明MVaR优势与对数概率的协方差小于均值方法，因此每个更新步导致更高的策略熵。"
---

# RiskPO: Risk-based Policy Optimization with Verifiable Reward for LLM Post-Training

> [!tip] 核心洞察
> 将风险敏感目标引入LLM后训练，可缓解熵崩塌，促进探索，从而扩展推理边界，而非仅提升采样效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | RiskPO：基于风险策略优化与可验证奖励的大型语言模型后训练 |
| 英文题名 | RiskPO: Risk-based Policy Optimization with Verifiable Reward for LLM Post-Training |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KjHB7rebQO) · [GitHub](https://github.com/RTkenny/RiskPO) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | RiskPO (Risk-based Policy Optimization) |
| Dataset | Hard-level Average (AIME25, AIME24, AMC, MATH500, Minerva, Oly.) |

> [!tip] 效果简介
> - Hard-level Average (AIME25, AIME24, AMC, MATH500, Minerva, Oly.) 上，Avg. Pass@1 为 46.65，对比 43.87 (DAPO)，变化 +2.78。
> - AIME24 上，Pass@1 为 33.3，对比 26.6 (DAPO)，变化 +6.7。
> - AMC 上，Pass@1 为 60.8，对比 58.6 (DAPO)，变化 +2.2。

## 概要

当前基于强化学习的大语言模型后训练方法（如 GRPO、DAPO）普遍采用均值目标优化，即最大化采样响应的期望奖励。这类方法过度关注高概率输出序列，忽视稀有但富含信息的推理路径，导致训练过程中出现**熵崩塌**——策略分布迅速收窄，模型探索能力受限，推理边界难以扩展。

针对这一瓶颈，本文提出 **RiskPO（Risk-based Policy Optimization）**，将风险敏感目标引入 LLM 后训练。其核心思路是：**将优化目标从奖励分布的均值转向分布尾部**，通过混合风险价值（MVaR）度量，对低奖励区域施加额外惩罚，从而为困难问题保留更强的梯度信号。配合问题捆绑方案，RiskPO 将稀疏的二值奖励转化为丰富的反馈，缓解了均值方法中常见的零优势问题。

理论分析表明，MVaR 优势与对数概率的协方差小于均值优势的协方差，因此每个更新步导致更高的策略熵（Proposition 1, Theorem 2），从原理上解释了 RiskPO 缓解熵崩塌的机制。

在硬级别数学推理基准上，RiskPO 的平均 Pass@1 达到 **46.65**，比最强基线 DAPO（43.87）高 **+2.78**，比 GRPO（40.41）高 **+6.24**（Table 1）。在 Pass@k 指标上，RiskPO 相对于 GRPO 的优势随 k 增大而扩大，表明模型扩展了推理边界而非仅提升采样效率（Figure 4）。训练过程中，RiskPO 的策略熵持续高于 GRPO，验证了理论预测（Figure 5）。



### 可验证奖励强化学习的瓶颈

近年来，基于可验证奖励的强化学习（RLVR）已成为大型语言模型（LLM）后训练的核心范式。其基本目标是在给定问题 $x$ 下最大化期望奖励：

$$\mathcal{I}(\theta) = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_\theta(\cdot|x)} [R(y)]$$

在这一框架下，GRPO（Shao et al., 2024）及其变体（DAPO、GPG、GMPO、Dr.GRPO）通过组标准化奖励和重要性采样裁剪，在数学推理等任务上取得了显著进展。然而，这些方法共享一个根本性的设计选择：**优化目标均基于奖励分布的均值**。

这一选择带来了一个被长期忽视的瓶颈：均值目标天然倾向于高概率输出序列，使得模型在训练中过度聚焦已有能力范围内的“安全”推理路径，而忽视那些稀有但富含信息的低概率探索路径。其直接后果是**熵崩塌**——策略的多样性随训练急剧下降，推理边界被锁定在一个狭窄的局部最优区域内。当所有组内响应都获得零奖励时，标准化优势退化为零，梯度信号完全消失，模型陷入停滞。

### 从均值到分布尾部：风险敏感视角

风险敏感强化学习在金融工程和决策控制领域已有悠久传统，其核心思想是：决策者不仅关心期望收益，还关心收益分布的尾部行为。将这一视角引入LLM后训练，意味着我们不应仅问“平均能答对多少题”，而应问“在最困难的题目上，模型的表现如何”。

在数学推理场景中，奖励信号通常是二元的（正确/错误），且困难问题天然稀疏。基于均值的优化会将大部分梯度信号分配给模型已经擅长的中等难度问题，而对真正需要突破的困难问题——那些处于奖励分布下尾的样本——几乎不产生有效梯度。这解释了为何GRPO类方法在简单基准上表现良好，但在AIME等硬级别基准上提升缓慢。

### 本文动机

本文提出RiskPO（Risk-based Policy Optimization），其核心动机是：**将优化目标从奖励分布的均值转向尾部，以缓解熵崩塌并扩展推理边界**。具体而言，RiskPO引入混合风险价值（Mixed Value-at-Risk, MVaR）目标，该目标显式地对奖励分布的下尾区域施加额外权重，同时排除已经表现良好的高奖励区域。通过这种风险厌恶的设计，模型被迫关注那些尚未掌握的困难推理模式，从而维持更高的策略熵，促进持续探索。

此外，为解决二元奖励在单问题粒度上的稀疏性问题，RiskPO设计了问题捆绑方案：将多个问题随机组合成捆绑，将稀疏的0/1奖励转化为丰富的0到B的捆绑得分，为风险敏感优化提供足够的统计信号。这一设计使得MVaR的分位数估计和优势计算在实践上可行。

理论层面，本文证明了MVaR优势与对数概率的协方差小于均值优势的协方差（Theorem 2），从而每个更新步导致更高的策略熵（Proposition 1），为RiskPO缓解熵崩塌提供了严格的数学基础。



## 核心方法与创新机理

RiskPO 的核心创新在于将**风险敏感目标**引入大语言模型后训练，从根本上改变了策略优化的信号来源与梯度分配方式。与以 **GRPO** (Shao et al., 2024) 为代表的均值目标方法相比，RiskPO 在三个关键维度上实现了系统性改进。

### 从均值到尾部：优化目标的范式转换

GRPO 及其变体（**DAPO**、**GPG**、**GMPO**、**Dr.GRPO**）均以期望奖励最大化为目标，其标准化优势函数 $A_i = \frac{R(y_i) - \mu}{\sigma}$ 本质上是围绕组内均值分配正负信号。这一设计存在结构性缺陷：当大部分采样序列产生相同奖励时（如全部正确或全部错误），优势信号趋于零，导致梯度消失。更关键的是，均值目标过度关注高概率输出序列，忽视了稀有但富含信息的推理路径，最终引发**熵崩塌**——策略过早收敛到有限几个输出模式，推理边界受限。

RiskPO 通过引入**混合风险价值**（Mixed Value-at-Risk, MVaR）目标，将优化重心从均值转向奖励分布的**下尾和中间段**：

$$\mathcal{T}_{\mathrm{MVaR}_{\alpha:\beta}^{\omega}}(\theta) = \left\{ (1+\omega)\int_{F_{\theta}^{-1}(0)}^{F_{\theta}^{-1}(\alpha)} + \int_{F_{\theta}^{-1}(\alpha)}^{F_{\theta}^{-1}(\beta)} \right\} r dF_{\theta}(r)$$

该目标显式排除了高奖励区域（$\beta$ 分位数以上），通过权重参数 $\omega \geq 0$ 强化对低分位（困难问题）的关注。这一设计直接针对均值目标的瓶颈：困难问题在均值框架下因采样概率低而缺乏梯度信号，而 MVaR 通过集中参数化尾部区域，确保这些富含信息的问题获得充分优化。

### 从单题到捆绑：奖励信号的重构

传统 RLVR 方法对每个问题独立采样并计算二进制奖励（正确/错误），这导致奖励空间极度稀疏。RiskPO 引入**问题捆绑方案**：将 $B$ 个问题随机排列后组合成 $G$ 个无重叠的捆绑，使用捆绑内各题得分之和（取值范围 $0$ 到 $B$）作为奖励信号。这一设计将稀疏的二进制反馈转化为丰富的多级信号，使得 MVaR 的分位数估计和优势计算成为可能。

捆绑方案的梯度估计器通过随机排列无放回采样构造 $G$ 个互斥捆绑，保证每个采样序列恰好被使用一次，从而得到无偏梯度估计。最终损失函数采用序列级重要性采样和信任域裁剪：

$$\mathcal{I}_{\mathrm{MVaR}}^{\mathrm{clip}}(\theta) = \mathbb{E}\left[ \frac{1}{G}\sum_{j=1}^G \frac{1}{B}\sum_{i=1}^B \min\left( s_j^i(\theta) A^{(j)}, \mathrm{clip}(s_j^i(\theta), 1-\epsilon, 1+\epsilon) A^{(j)} \right) \right]$$

其中 $s_j^i(\theta)$ 是经序列长度归一化的重要性权重，$A^{(j)}$ 是基于 MVaR 分位数的捆绑级优势。

### 熵崩塌的理论缓解

RiskPO 提供了对熵维持机制的严格理论分析。在表格 softmax 策略和单调 log 概率假设下，**命题 1** 表明策略熵的变化近似为优势与 log 概率的负协方差乘以学习率：

$$\Delta \mathcal{H} \approx -\eta \, \mathrm{Cov}(\log \pi_\theta(y|x), A_\theta(x,y))$$

基于此，**定理 2** 证明 MVaR 优势与 log 概率的协方差不超过均值优势的协方差：

$$\mathrm{Cov}(\log \pi_\theta, A_{\mathrm{MVaR}}) \leq \mathrm{Cov}(\log \pi_\theta, A_{\mathrm{Mean}})$$

这意味着 RiskPO 的每个更新步导致更小的熵下降，从机制层面缓解了熵崩塌。实验验证了这一理论：RiskPO 在整个训练过程中维持显著高于 GRPO 的策略熵（Figure 5），且 Pass@k 性能差距随 $k$ 增大而扩大（Figure 4），表明模型扩展了推理边界而非仅提升采样效率。

### 关键超参数与敏感性

RiskPO 引入了三个核心超参数：分位数水平 $\alpha, \beta$、捆绑大小 $B$ 和混合参数 $\omega$。消融实验表明，默认配置（$\alpha=0.2, \beta=0.8, B=5, \omega=0.5$）在数学推理基准上取得最优平均性能，但方法对这些参数较为敏感，过大或过小的取值都会导致性能下降。此外，分位数在线跟踪使用随机近似更新，可能引入额外估计方差，影响训练稳定性。



![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KjHB7rebQO/figures/002_Figure_2.jpg]]
*Figure 2: The framework of RiskPO*

RiskPO的整体流程围绕一个核心洞察展开：传统基于均值的目标（如GRPO）过度关注高概率输出序列，忽视稀有但富含信息的推理路径，导致熵崩塌和推理边界受限。为缓解这一问题，RiskPO引入**风险敏感优化**范式，将优化目标从均值转向奖励分布的尾部，并辅以**问题捆绑方案**将稀疏奖励转化为丰富反馈信号。

框架由两大阶段级联构成，如图2所示：

**阶段一：奖励信号富集（Reward Signal Enrichment）**。在标准RLVR流程中，单个问题的二元奖励（正确/错误）高度稀疏，当组内所有回答均错误时，标准化优势退化为零，梯度消失。RiskPO的解决方案是将B个问题随机排列后组合成G个无重叠的捆绑（bundle），以捆绑内各问题得分的总和作为新的奖励信号。这一操作将原本取值为0或1的稀疏信号转化为0到B的丰富反馈，从根本上缓解了零优势问题。具体而言，从数据分布中采样B个问题构成X，对每个问题生成G个回答，再通过随机排列将回答分配到G个捆绑中，确保每个回答恰好属于一个捆绑且无重复使用。

**阶段二：风险敏感策略优化（Risk-sensitive Policy Optimization）**。在获得捆绑级奖励后，RiskPO采用混合风险价值（Mixed Value-at-Risk, MVaR）作为优化目标。MVaR将奖励分布划分为下尾和中间段两个区域：下尾（分位数0到α）以权重(1+ω)进行加权，中间段（分位数α到β）以权重1进行加权，而高奖励区域（分位数β到1）被完全排除。这一设计使优化过程聚焦于困难问题和中等难度问题，对已掌握的高奖励样本停止梯度更新。MVaR的梯度形式为：

$$\nabla_\theta \mathcal{T}_{\mathrm{MVaR}_{\alpha:\beta}^\omega}(\theta) = \frac{1}{\beta-\alpha} \mathbb{E}\left[ g(R(y), F_\theta^{-1}(\alpha), F_\theta^{-1}(\beta)) \nabla_\theta \ln \pi_\theta(y|x) \right]$$

其中 $g(z,a,b) = (1+\omega)(z-a)^+ - (z-b)^+ + a - b$，该函数对低于α分位数的样本施加额外梯度信号，对高于β分位数的样本进行裁剪。

**算法实现**采用双时间尺度随机近似（Algorithm 1）。在每个训练步，算法执行以下模块化流程：
1. **问题捆绑**：采样B个问题，每个问题生成G个回答，随机排列后形成G个捆绑。
2. **在线分位数跟踪**：使用随机近似更新分位数 $Q^\alpha$ 和 $Q^\beta$，以跟踪奖励分布的动态变化。
3. **MVaR优势计算**：根据捆绑得分和当前分位数，为每个捆绑计算风险敏感优势 $A^{(j)}$。
4. **裁剪MVaR目标**：应用序列级重要性采样和信任域裁剪，计算最终损失函数：

$$\mathcal{I}_{\mathrm{MVaR}}^{\mathrm{clip}}(\theta) = \mathbb{E}\left[ \frac{1}{G}\sum_{j=1}^G \frac{1}{B}\sum_{i=1}^B \min\left( s_j^i(\theta) A^{(j)}, \mathrm{clip}(s_j^i(\theta), 1-\epsilon, 1+\epsilon) A^{(j)} \right) \right]$$

其中 $s_j^i(\theta)$ 为序列级重要性权重，$\epsilon$ 为裁剪阈值。
5. **策略更新**：使用梯度下降更新策略参数θ。

**熵机制的理论支撑**。RiskPO维持更高策略熵的能力源于其优势函数与对数概率之间更小的协方差。Proposition 1表明，每个自然梯度步后，策略熵的变化近似为 $\Delta\mathcal{H} \approx -\eta \cdot \mathrm{Cov}(\log\pi_\theta, A_\theta)$。Theorem 2进一步证明，MVaR优势与log概率的协方差始终小于或等于均值优势的协方差，因此RiskPO在每个更新步导致更小的熵下降，有效缓解了熵崩塌问题。这一理论预测在实验中得到了实证验证（Figure 9）。



RiskPO 的核心由两个关键模块构成：**奖励信号富集（Reward Signal Enrichment）** 与 **风险敏感策略优化（Risk-sensitive Policy Optimization）**。前者通过问题捆绑将稀疏的二元奖励转化为丰富的梯度信号，后者引入混合风险价值（MVaR）目标替代传统均值目标，将优化焦点从奖励分布中心转向尾部。

### 范围风险价值（RVaR）与混合风险价值（MVaR）

传统 RLVR 方法（如 GRPO）最大化期望奖励 $\mathbb{E}[R(y)]$，等价于在整个奖励分布上取均值。RiskPO 转而关注分布的特定分位数区间。

**范围风险价值（RVaR）** 定义为奖励在分位数 $\alpha$ 到 $\beta$ 之间的条件期望：

$$\mathcal{I}_{\mathrm{RVaR}_{\alpha:\beta}}(\theta) = \frac{1}{\beta-\alpha} \int_{F_{\theta}^{-1}(\alpha)}^{F_{\theta}^{-1}(\beta)} r \, dF_{\theta}(r)$$

其中 $F_{\theta}$ 是奖励的累积分布函数，$F_{\theta}^{-1}(\alpha)$ 是 $\alpha$-分位数。RVaR 的梯度具有简洁形式：

$$\nabla_{\theta} \mathcal{I}_{\mathrm{RVaR}_{\alpha:\beta}}(\theta) = \frac{1}{\beta-\alpha} \mathbb{E}\big[ g(R(y), F_{\theta}^{-1}(\alpha), F_{\theta}^{-1}(\beta)) \, \nabla_{\theta} \ln \pi_{\theta}(y|x) \big]$$

其中 $g(z, a, b) = (z-a)^+ - (z-b)^+ + a - b$，$(z-a)^+ = \max(z-a, 0)$。该梯度仅在奖励落入 $[a, b]$ 区间时提供非零信号，天然过滤了已掌握的高奖励样本。

**混合风险价值（MVaR）** 进一步组合下尾和中间段，排除高奖励区域：

$$\mathcal{T}_{\mathrm{MVaR}_{\alpha:\beta}^{\omega}}(\theta) = \left\{ (1+\omega)\int_{F_{\theta}^{-1}(0)}^{F_{\theta}^{-1}(\alpha)} + \int_{F_{\theta}^{-1}(\alpha)}^{F_{\theta}^{-1}(\beta)} \right\} r \, dF_{\theta}(r)$$

其中 $\omega \geq 0$ 控制对下尾（最困难样本）的额外加权。当 $\omega=0$ 时 MVaR 退化为 RVaR；当 $\omega>0$ 时，模型对低奖励区域施加更强梯度，迫使策略在困难问题上投入更多探索。

### 问题捆绑方案

单问题的二元奖励（0/1）导致组内标准化优势在全部正确或全部错误时退化为零，梯度消失。RiskPO 将 $B$ 个问题随机捆绑为一组 $X = \{x_i\}_{i=1}^B$，以捆绑内各问题得分之和作为奖励信号（取值 $0$ 到 $B$），显著丰富反馈粒度。

具体实现中，对每个问题采样 $G$ 条回答 $\{y_j^i\}_{j=1}^G$，通过 $G$ 个独立随机排列 $\xi_i \sim \mathrm{Unif}(\mathfrak{S}_G)$ 构造 $G$ 个无重叠捆绑。第 $j$ 个捆绑使用 $\{y_{\xi_{i,j}}^i\}_{i=1}^B$，确保每条回答恰好使用一次。捆绑级优势 $A^{(j)}$ 基于 MVaR 分位数计算：

$$A^{(j)} = -(1+\omega)(\hat{Q}^{\alpha} - R_{B_j})^+ + g(R_{B_j}, \hat{Q}^{\alpha}, \hat{Q}^{\beta})$$

其中 $R_{B_j} = \sum_{i=1}^B R(y_{\xi_{i,j}}^i)$ 为捆绑总得分，$\hat{Q}^{\alpha}$、$\hat{Q}^{\beta}$ 为在线跟踪的分位数估计。该优势函数对低于 $\alpha$-分位数的捆绑施加 $(1+\omega)$ 倍惩罚，对中间段给予标准梯度，对高于 $\beta$-分位数的捆绑截断信号。

### 裁剪 MVaR 目标与在线分位数跟踪

最终损失函数采用序列级重要性采样和信任域裁剪：

$$\mathcal{I}_{\mathrm{MVaR}}^{\mathrm{clip}}(\theta) = \mathbb{E}\left[ \frac{1}{G}\sum_{j=1}^G \frac{1}{B}\sum_{i=1}^B \min\left( s_j^i(\theta) A^{(j)}, \mathrm{clip}(s_j^i(\theta), 1-\epsilon, 1+\epsilon) A^{(j)} \right) \right]$$

其中 $s_j^i(\theta) = \left( \frac{\pi_\theta(y_{\xi_{i,j}}^i|x_i)}{\pi_{\theta'}(y_{\xi_{i,j}}^i|x_i)} \right)^{1/|y|}$ 为序列级重要性权重，$\epsilon$ 为裁剪阈值。分位数 $\hat{Q}^{\alpha}$、$\hat{Q}^{\beta}$ 通过随机近似在线更新，无需存储历史奖励分布。

### 熵保持机制

RiskPO 缓解熵崩塌的理论基础由两个命题支撑。**命题 1** 表明，在自然梯度步下，策略熵的变化近似为优势与对数概率的负协方差乘以学习率：

$$\Delta \mathcal{H} \approx -\eta \, \mathrm{Cov}(\log \pi_\theta(y|x), A_\theta(x,y))$$

**定理 2** 证明，MVaR 优势与对数概率的协方差不大于均值优势的协方差：

$$\mathrm{Cov}(\log \pi_\theta, A_{\mathrm{MVaR}}) \leq \mathrm{Cov}(\log \pi_\theta, A_{\mathrm{Mean}})$$

因此 RiskPO 每步更新导致的熵下降更小，在训练过程中维持更高的策略熵，从而保留探索能力、扩展推理边界。该理论在表格 softmax 策略和单调对数概率假设下成立，实验部分通过实际模型验证了假设的合理性。



## 实验与关键发现

### 主结果：硬级别数学推理

RiskPO在6个硬级别数学推理基准上进行了系统评估，所有方法均基于1.5B参数模型（DeepSeek-R1-Distill-Qwen-1.5B），在相同训练数据和评估设置下公平比较。Table 1展示了Pass@1的核心结果：


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KjHB7rebQO/figures/004_Table_1.jpg]]
*Table 1: Pass@1 performance on hard-level mathematical reasoning benchmarks*

- RiskPO在硬级别平均Pass@1上达到**46.65**，比最强基线DAPO（43.87）高出**+2.78**，比GRPO（40.41）高出**+6.24**，比GMPO（41.37）高出**+5.28**。
- 在AIME24上，RiskPO取得**33.3**，远超DAPO的**26.6**（+6.7），在AIME25上同样领先（33.3 vs 29.0，+4.3）。
- 在AMC上，RiskPO达到**60.8**，超过DAPO的**58.6**（+2.2）。

这些结果表明，MVaR风险敏感目标在最具挑战性的推理任务上带来了显著且一致的性能提升。

### 主结果：易级别与跨领域泛化

Table 2展示了RiskPO在易级别数学推理、多模态推理和代码生成基准上的表现：


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KjHB7rebQO/figures/005_Table_2.jpg]]
*Table 2: Pass@1 results on easy-level math benchmarks and multi-modal/coding benchmarks*

- 在易级别数学平均Pass@1上，RiskPO达到**68.25**（MATH 56.2，GSM8K 80.3），超过GRPO（66.55）和DAPO（67.55）。
- 在代码生成（LiveCodeBench）和多模态推理（Geometry3K）上，RiskPO分别取得**26.8**和**54.5**，均优于GRPO和DAPO，表明方法的跨领域泛化能力。

### 推理边界扩展的证据

Figure 4展示了AMC和MATH500上Pass@k随k变化的曲线。关键发现是：**RiskPO相对于GRPO的Pass@k优势随k增大而扩大**。这意味着RiskPO并非仅仅提升了采样效率（即在高概率输出上更准确），而是真正扩展了模型的推理边界——在更大的采样预算下，模型能够探索到GRPO无法触及的正确推理路径。


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KjHB7rebQO/figures/011_Figure_4.jpg]]
*Figure 4: Pass@k learning curves on the AMC and MATH500 datasets*

### 熵崩塌缓解机制

Figure 5展示了DAPOMATH-17K上的训练动态对比，直接验证了RiskPO缓解熵崩塌的核心主张：


![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KjHB7rebQO/figures/015_Figure_5.jpg]]
*Figure 5: Learning curves on DAPOMATH-17K, the RiskPO mitigates the entropy collapse and shows better performance on difficult problems, which is indicated by risk measures*

- GRPO的策略熵在训练过程中持续下降，呈现典型的熵崩塌模式。
- RiskPO在整个训练过程中维持**显著更高**的策略熵水平，同时取得了更好的困难问题表现（以风险度量衡量）。
- 这一现象的理论基础由Theorem 2和Proposition 1给出：MVaR优势与对数概率的协方差小于均值优势的协方差，因此每个更新步导致的熵减少更小，从而在长期训练中保持更高的探索能力。

### 消融研究

#### 风险态度选择（Figure 6）

将MVaR（风险厌恶）与对应的风险寻求目标进行对比：
- 风险厌恶目标将MATH上的Pass@1从52%提升至**56%**。
- 风险寻求目标仅提升至54%，且训练曲线波动更大。
- 均值目标（GRPO）表现最差。这证实了**关注奖励分布左尾（困难样本）而非右尾（简单样本）是提升推理能力的关键**。

#### 分位数水平 (α, β)（Table 3）

在易级别数学推理上系统消融分位数参数：

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KjHB7rebQO/figures/020_Table_3.jpg]]
*Table 3: Ablation of different quantile levels ( $\alpha , \beta$ ) on easy-level mathematical reasoning

- 默认配置(α=0.2, β=0.8)取得最佳平均性能**68.25**。
- α过小（0.1）或过大（0.3, 0.4）均导致性能下降，表明需要合理平衡下尾关注范围。
- β=0.8时性能最优，过大的β（0.9）会包含过多高奖励区域，削弱风险厌恶效果。

#### Bundle大小B（Table 4）

问题捆绑方案的消融显示：

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KjHB7rebQO/figures/021_Table_4.jpg]]
*Table 4: Ablation of different bundle size B on easy-level mathematical reasoning*

- B=5时平均性能最优（68.25）。
- B=1（无捆绑）性能显著下降，验证了捆绑对于将稀疏二元奖励转化为丰富梯度信号的**必要性**。
- B过大（8, 10）同样导致性能退化，可能因为过大的捆绑模糊了单个问题的学习信号。

#### 混合参数ω（Table 5）

ω控制MVaR中对下尾区域的额外加权：

![[assets/figures/papers/paper_list_l23_https_openreview_net_forum_id_KjHB7rebQO/figures/022_Table_5.jpg]]
*Table 5: Ablation of the mixing parameter*

- ω=0.5取得最佳平均性能（68.25），表明适度强调困难样本最为有效。
- ω=0（仅关注中间段）和ω=1（最大下尾加权）均导致性能下降，说明需要在下尾关注和中间段学习之间取得平衡。

### 局限性

1. **超参数敏感性**：分位数水平(α, β)、bundle大小B和混合参数ω均需仔细调优，不同任务可能需要不同的最优配置。
2. **理论假设差距**：Theorem 2的证明依赖于表格softmax策略和单调log概率条件（Assumption 1），虽经Figure 3实证验证，但与大规模LLM的实际行为仍存在差距。
3. **分位数估计方差**：在线分位数跟踪使用随机近似，可能引入额外估计方差，影响训练稳定性，尤其在训练初期分位数估计不准确时。


## 定位与知识库关联

### 1. 方法定位

RiskPO 直接回应 GRPO 族方法的一个核心瓶颈：**基于均值的优化目标过度关注高概率输出序列，忽视稀有但富含信息的推理路径，导致熵崩塌与推理边界受限**。GRPO（Shao et al., 2024）通过组标准化奖励计算优势，本质上是最大化期望奖励；其后续变体 DAPO（Yu et al., 2025）、GPG（Chu et al., 2025）、GMPO（Zhao et al., 2025b）、Dr.GRPO（Liu et al., 2025b）主要围绕训练稳定性、归一化因子设计等工程层面改进，未触及优化目标的风险结构。

RiskPO 的差异化在于将**风险敏感目标**引入 LLM 后训练，通过三个关键设计改变优化方向：

- **优化目标替换**：从均值目标（期望奖励最大化）转向 MVaR（混合风险价值）目标，对奖励分布的下尾（困难问题）和中间段加权，排除高奖励区域。
- **奖励信号重构**：引入问题捆绑方案，将 B 个问题组合成捆绑，使用捆绑得分（0 到 B）替代单问题二元奖励，将稀疏反馈转化为丰富梯度信号。
- **优势函数重塑**：基于 MVaR 分位数的优势函数 $A_j = -(1+\omega)(F^{-1}(\alpha) - R_{B_j})^+ + g(R_{B_j}, \alpha, \beta)$，替代标准化奖励 $A_i = (R(y_i) - \mu) / \sigma$。

理论层面，RiskPO 建立了**熵崩塌的因果机制**：Proposition 1 表明策略熵变化近似为 $\Delta \mathcal{H} \approx -\eta \, \mathrm{Cov}(\log \pi_\theta(y|x), A_\theta(x,y))$；Theorem 2 证明 MVaR 优势与 log 概率的协方差 ≤ 均值优势的协方差，因此 RiskPO 每个更新步维持更高策略熵。该理论在表格 softmax 策略和单调 log 概率假设下成立，实际验证显示 DeepSeek-R1-Distill-Qwen-1.5B 在训练集上满足单调性条件（Figure 3）。

### 2. 适用边界与局限

**适用场景**：RiskPO 在硬级别数学推理基准上表现突出——AIME24 Pass@1 达 33.3，比 DAPO 高 +6.7；AMC Pass@1 达 60.8，比 DAPO 高 +2.2（Table 1）。在 Pass@k 指标上，RiskPO 相对于 GRPO 的差距随 k 增大而扩大（Figure 4），表明方法扩展了推理边界而非仅提升采样效率。多模态推理（Geometry3K）和代码生成（LiveCodeBench）上同样有效（Table 2）。

**已知局限**：

1. **超参数敏感性**：分位数水平 $(\alpha, \beta)$、bundle 大小 $B$、混合参数 $\omega$ 需要仔细调优。消融实验显示 $\alpha=0.2, \beta=0.8$ 时平均性能最优（68.25），$B=5$ 时最优，过大或过小均导致性能下降（Table 3, 4, 5）。
2. **理论假设与实际差距**：理论分析基于表格 softmax 策略和单调 log 概率条件，实际大语言模型的高维离散空间与假设存在偏差。
3. **分位数估计方差**：在线分位数跟踪使用随机近似，可能引入额外估计方差，影响训练稳定性。

### 3. 开放问题

1. **规模扩展性**：当前实验基于 1.5B 参数模型（DeepSeek-R1-Distill-Qwen-1.5B / Qwen2.5-Math-1.5B），RiskPO 能否扩展到 7B、32B 及更大规模模型尚待验证。
2. **任务泛化性**：方法在数学推理、多模态推理和代码生成上有效，但在长文本生成、对话等非结构化任务上的表现未知。
3. **与正则化技术结合**：MVaR 目标与 KL 散度约束、动态采样等正则化技术结合是否能进一步提升性能，是值得探索的方向。
4. **奖励形式扩展**：当前框架依赖二元可验证奖励（答案对/错），是否适用于连续评分或偏好数据场景需要进一步研究。
5. **分位数估计改进**：随机近似分位数跟踪是否导致有偏估计，以及如何改进估计精度和训练稳定性，是工程层面的开放问题。



## 原文 PDF

![[paperPDFs/ICLR_2026/RiskPO_Risk_based_Policy_Optimization_with_Verifiable_Reward_for_LLM_Post_Training.pdf]]
