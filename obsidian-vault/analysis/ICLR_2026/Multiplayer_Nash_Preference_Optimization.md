---
title: "Multiplayer Nash Preference Optimization"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Multiplayer_Nash_Preference_Optimization.pdf
project_link: null
code_link: https://github.com/smiles724/MNPO
openreview_forum_id: x7aLhLMVn1
aliases:
- MMNPO
- MNPO
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/optimization_methods
core_operator: "将偏好对齐从两人博弈扩展至多人博弈，通过引入多个历史策略或外部模型作为对手，构建时间依赖的对手混合（TD-MNPO），或使用异质偏好预言（HT-MNPO），从而稳定优化、降低梯度方差，并更准确地捕捉偏好结构。"
primary_logic: "将偏好优化建模为n人博弈，每个策略同时与一个对手群体竞争，而不是单一对手，通过乘性权重更新收敛至纳什均衡，获得更强的鲁棒性和泛化能力。"
claims:
- "TD-MNPO在AlpacaEval 2.0上达到57.27 LC Win Rate，Arena-Hard上52.26，均显著优于所有NLHF基线。"
- "消融实验表明增加玩家数n持续提升对齐质量，但n>3收益递减。"
- "HT-MNPO利用多个异质奖励模型，在AlpacaEval 2.0上达到59.64（Athene-RM-8B），超越同质设定。"
- "MNPO将DPO、INPO、SPIN等方法统一为其特例，揭示了多人框架的通用性。"
---

# Multiplayer Nash Preference Optimization

> [!tip] 核心洞察
> 将偏好优化建模为n人博弈，每个策略同时与一个对手群体竞争，而不是单一对手，通过乘性权重更新收敛至纳什均衡，获得更强的鲁棒性和泛化能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 多人纳什偏好优化 |
| 英文题名 | Multiplayer Nash Preference Optimization |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=x7aLhLMVn1) · [GitHub](https://github.com/smiles724/MNPO) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/optimization_methods |
| Method | MNPO (Multiplayer Nash Preference Optimization) |
| Dataset | Arena-Hard, AlpacaEval 2.0 (Llama-3-8B-it) |

> [!tip] 效果简介
> - Arena-Hard 上，Win Rate (WR, %) 为 52.26 (TD-MNPO)，对比 48.03 (INPO)，变化 +4.23。
> - AlpacaEval 2.0 (Llama-3-8B-it) 上，Length-Controlled Win Rate (LC, %) 为 42.94 (TD-MNPO)，对比 41.48 (INPO)，变化 +1.46。

## 概要

现有基于纳什均衡的偏好优化方法（NLHF）将对齐建模为两人零和博弈，每轮仅在当前策略与单一对手之间进行偏好比较。然而，现实世界中的人类偏好天然具有**多源、异质和非传递性**——不同人群的价值排序可能相互冲突，单一对手的反馈不足以刻画完整的偏好结构。这导致现有方法在优化过程中出现梯度振荡、探索不足，策略难以覆盖多样化的偏好群体。

本文提出**多人纳什偏好优化**（Multiplayer Nash Preference Optimization, MNPO），将偏好对齐从两人博弈范式扩展至n人博弈。核心思路是：每个策略不再仅与一个对手竞争，而是同时面对一个**对手群体**，通过乘性权重更新收敛至多人博弈的纳什均衡。这一框架从根本上改变了偏好信号的采集方式——策略需要在对多个对手的“一对多”比较中胜出，从而获得更稳定、信息量更丰富的训练信号。

MNPO包含两种实例化方案：**时间依赖MNPO**（TD-MNPO）将历史策略的加权混合作为动态对手集合，利用训练过程中的策略演化轨迹构建对手群体；**异质MNPO**（HT-MNPO）则引入多个使用不同奖励模型的策略作为对手，直接捕捉偏好的异质性。理论分析表明，MNPO统一了DPO、INPO、SPIN等现有方法——它们均可视为MNPO在不同玩家数量和对手配置下的特例（Table 1）。

实验验证了多人框架的有效性：TD-MNPO在AlpacaEval 2.0上达到57.27的LC Win Rate，Arena-Hard上达到52.26，均显著优于所有NLHF基线（Table 2）。消融实验揭示，增加玩家数n持续提升对齐质量，但n>3后收益递减（Table 5）。HT-MNPO利用多个异质奖励模型，在AlpacaEval 2.0上达到59.64（Athene-RM-8B），进一步超越同质设定（Table 2, Table 8）。在不同LLM法官下的多次运行中，MNPO表现出最高的均值且标准差最小，验证了其优化稳定性（Table 7）。

**方法定位**：MNPO属于在线偏好优化方法，其核心创新在于将博弈论中的多人博弈框架引入对齐训练。与依赖单一奖励模型的RLHF不同，MNPO直接利用偏好预言（可为LLM法官或奖励模型）进行策略间的比较优化，无需显式奖励建模。其优势在于多人博弈带来的梯度方差降低和偏好覆盖增强，代价是计算开销随玩家数量线性增长。当前局限包括：偏好预言在高性能策略上的区分能力下降、二进制偏好信号在高质量区域的收益递减，以及异质扩展缺乏正式收敛保证。



### 从奖励模型到偏好博弈：RLHF 的基本框架

大语言模型的对齐通常依赖基于人类反馈的强化学习（RLHF），其核心是在最大化奖励信号的同时，防止策略偏离参考模型过远。标准目标函数为带 KL 正则项的最大奖励优化：

$$J(\pi) = \mathbb{E}_{x \sim d_0} [ \mathbb{E}_{y \sim \pi(\cdot|x)} [R(x,y)] - \tau \operatorname{KL}(\pi(\cdot|x) \| \pi_{\mathrm{ref}}(\cdot|x)) ]$$

这一框架将人类偏好压缩为标量奖励函数 $R(x,y)$，再通过强化学习微调策略。然而，奖励模型的训练与使用存在根本性张力：人类偏好本质上具有多源、异质和非传递性，单一标量奖励难以忠实地刻画这种复杂性。

### 从奖励到偏好预言：纳什学习范式的兴起

为绕过显式奖励建模，纳什学习从人类反馈（NLHF）将偏好对齐重新建模为两人零和博弈。给定一个偏好预言 $\mathbb{P}(y_1 \succ y_2 \mid x)$，两玩家博弈目标为：

$$J(\pi_1, \pi_2) = \mathbb{E}_{x \sim d_0} [ \mathbb{E}_{y_1 \sim \pi_1, y_2 \sim \pi_2} [\mathbb{P}(y_1 \succ y_2 \mid x)] - \tau \operatorname{KL}(\pi_1 \| \pi_{\mathrm{ref}}) + \tau \operatorname{KL}(\pi_2 \| \pi_{\mathrm{ref}}) ]$$

在该博弈中，玩家 1 最大化对玩家 2 的胜率，玩家 2 最小化玩家 1 的胜率。纳什均衡策略 $\pi_1^*, \pi_2^*$ 满足：

$$\pi_1^*, \pi_2^* := \operatorname{argmax}_{\pi_1 \in \Pi} \operatorname{argmin}_{\pi_2 \in \Pi} J(\pi_1, \pi_2)$$

实践中，通过最小化对偶间隙（duality gap）来逼近纳什策略：

$$\operatorname{DualGap}(\pi) := \operatorname{max}_{\pi_1} J(\pi_1, \pi) - \operatorname{min}_{\pi_2} J(\pi, \pi_2)$$

现有方法如 **INPO**（在线两人纳什偏好优化）和 **SPIN**（自博弈迭代优化）均在此两人框架下运作，分别使用当前策略-参考策略对或历史策略作为对手进行优化。

### 两人博弈的瓶颈：为什么需要多人？

尽管两人纳什学习取得了显著进展，但其核心假设——偏好可被单一对手分布充分捕获——在实际中面临三重挑战：

1. **偏好多源性**：人类偏好的多样性意味着不存在单一的“最优对手”；策略在某一对手上优化可能导致在其他偏好群体上表现退化。
2. **优化振荡**：两人博弈中，策略围绕单一对手分布迭代更新时，梯度方差大，收敛路径不稳定。
3. **探索不足**：固定对手集合限制了策略探索的空间，难以覆盖多样化的偏好群体。

这些瓶颈的深层原因是：**实际偏好结构是一个多人博弈，而非两人博弈**。每个策略需要同时与一个对手群体竞争，而非单一对手。

### MNPO 的核心动机与设计方向

本文提出**多人纳什偏好优化（MNPO）**，将偏好对齐从两人博弈系统性地扩展至 $n$ 人博弈。其核心动机在于：

- **稳定优化**：通过引入多个历史策略或外部模型作为对手，构建时间依赖的对手混合（TD-MNPO），降低梯度方差，稳定收敛路径。
- **覆盖多样性**：异质偏好预言（HT-MNPO）允许每个玩家关联不同的奖励模型，从多维度捕捉偏好信号，获得更全面的对齐。
- **统一框架**：MNPO 将 DPO、INPO、SPIN 等方法统一为其特例（见 Table 1），揭示了多人框架的通用性。

在 MNPO 中，每个玩家 $i$ 的目标函数扩展为：

$$J(\pi_i, \{\pi_j\}_{j \neq i}) = \mathbb{E}_{x \sim d_0} [ \mathbb{E}_{y^i \sim \pi_i, \{y^j \mid y^j \sim \pi_j\}_{j \neq i}} [\mathbb{P}(y^i \succ \{y^j\}_{j \neq i} \mid x)] - \tau \operatorname{KL}(\pi_i(\cdot|x) \| \pi_{\mathrm{ref}}(\cdot|x)) ]$$

通过乘性权重更新，策略迭代收敛至多人博弈的纳什均衡，从而获得更强的鲁棒性和泛化能力。



## 核心方法与创新机理

MNPO的核心创新在于将偏好优化从**两人零和/一般和博弈**扩展为**多人博弈**，由此引入两个关键的结构性改变，直接回应了现有方法的瓶颈。

### 从两人到多人：博弈结构的根本转变

现有纳什偏好优化方法（如**INPO**）将对齐建模为当前策略与单一对手（参考策略或上一轮策略）之间的两人博弈。这一设定隐含假设偏好信号来自同质群体，但实际人类偏好具有多源、异质和非传递性，导致策略在单一对手分布上优化时出现振荡、探索不足，难以充分覆盖多样化的偏好群体。

MNPO将博弈扩展为$n$人：每个玩家策略$\pi_i$同时与一个对手群体$\{\pi_j\}_{j \neq i}$竞争，目标函数为：

$$J(\pi_i, \{\pi_j\}_{j \neq i}) = \mathbb{E}_{x \sim d_0} \left[ \mathbb{E}_{y^i \sim \pi_i, \{y^j\}_{j \neq i}} [\mathbb{P}(y^i \succ \{y^j\}_{j \neq i} \mid x)] - \tau \operatorname{KL}(\pi_i \| \pi_{\mathrm{ref}}) \right]$$

这一转变的因果机制在于：**对手多样性直接降低了梯度估计的方差**。当策略面对多个不同对手时，偏好信号来自更广泛分布，单次采样的噪声被平均化，优化轨迹更平滑。消融实验（Table 5）证实了这一点——将玩家数$n$从1增至3，AlpacaEval 2.0 LC Win Rate从53.32持续提升至57.42；$n=4$时收益递减，表明3个对手已能捕获主要偏好多样性。

### 对手集合的构造：时间依赖与异质预言

如何构造对手群体是多人博弈的核心设计空间。MNPO提出两种互补方案：

**时间依赖MNPO（TD-MNPO）**：对手集合由前$n-1$个历史策略的加权混合构成。损失函数为：

$$\mathcal{L}_{\mathrm{TD}}^{t,\mathrm{D}}(\pi \mid \beta, \{\lambda_j\}, \eta) = \mathbb{E}_{y,y' \sim \pi, y_w,y_l \sim \lambda_{\widetilde{\pi}}(y,y')} \mathbb{D}\left[ \log\frac{\pi(y_w|x)}{\pi(y_l|x)} - \sum_{j=0}^{n-2} \lambda_j \log\frac{\pi_{t-j}(y_w|x)}{\pi_{t-j}(y_l|x)} \mid \eta \delta^\star \right]$$

关键设计在于**加权混合权重$\lambda_j$**，它决定了近期与远期历史策略的影响比例。这一机制使得TD-MNPO天然统一了多种现有方法（Table 1）：当$n=2$、对手为参考策略时退化为**DPO**；当对手为上一轮策略时恢复**INPO**；当对手为历史策略的等权混合时对应**SPIN**。这种统一性并非简单的形式化重述，而是揭示了这些方法本质上都是多人博弈在不同对手构造下的特例。

**异质MNPO（HT-MNPO）**：每个玩家关联一个独立的奖励模型作为偏好预言，对手策略由不同奖励模型引导。这直接回应了偏好异质性的现实——不同用户群体或评估维度可能对“好”响应有不同甚至冲突的定义。HT-MNPO在AlpacaEval 2.0上达到59.64（Athene-RM-8B），显著超越同质设定，验证了异质对手带来的增益。但需注意，HT-MNPO缺乏正式收敛保证（见局限性），其实效性目前仅来自经验验证。

### 优化算法：乘性权重更新的多人推广

MNPO将两人博弈中的乘性权重更新推广至多人场景，策略迭代规则为：

$$\pi_i^{(t+1)}(\boldsymbol{y} \mid \boldsymbol{x}) \propto \left( \prod_{j \neq i} \pi_j^{(t)}(\boldsymbol{y} \mid \boldsymbol{x}) \right)^{\frac{1}{n-1}} \exp\left( \frac{\eta}{n-1} \sum_{j \neq i} \mathbb{P}\left( \boldsymbol{y} \succ \pi_j^{(t)} \mid \boldsymbol{x} \right) \right)$$

该更新具有$\mathcal{O}(1/\sqrt{T})$的遗憾界，保证平均策略收敛至$\epsilon$-近似纳什均衡。与两人博弈相比，多人更新的核心差异在于：优势估计变为对所有对手的平均，而非对单一对手；正则项变为所有对手策略的几何平均。这使得更新方向更稳健——单个对手的噪声被群体平均稀释。

### 与基线的结构性差异总结

| 设计维度 | 基线（INPO/DPO） | MNPO |
|---------|-----------------|------|
| 玩家数量 | 2 | $n$（可配置） |
| 对手集合 | 单一策略（参考或上轮） | 历史策略加权混合（TD）或异质奖励模型策略（HT） |
| 偏好预言 | 单一通用预言 | 同质（共享）或异质（每玩家独立） |
| 损失函数 | 两玩家平方损失 | 多人扩展平方损失，含对手加权项 |
| 收敛保证 | 两人纳什均衡 | 多人纳什均衡（同质），异质无正式保证 |

这些改变的共同效果是：**策略不再针对单一对手过拟合，而是在多样化对手压力下学习更具泛化性的偏好表征**。稳定性实验（Table 7）佐证了这一点——在不同LLM法官下，MNPO的均值最高且标准差较小，表明其对评估方差的鲁棒性优于SFT、DPO和INPO。



![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_x7aLhLMVn1/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the two-player baseline and our multiplayer MNPO training paradigm*

MNPO 将偏好对齐从传统的两人博弈扩展为 **n 人博弈**，核心思路是让每个策略同时与一个对手群体竞争，而非仅针对单一对手优化。这一扩展的关键动机在于：真实人类偏好具有多源、异质和非传递性，两人博弈下的策略优化容易在单一对手分布上出现振荡，探索不足，难以充分覆盖多样化的偏好群体。

### 训练范式概览

Figure 1 对比了两人基线方法与 MNPO 的训练范式。在传统两人博弈中，策略 $\pi_t$ 仅与一个对手（如参考策略 $\pi_{\text{ref}}$ 或当前策略的镜像）交互；而 MNPO 将这一结构扩展为多人博弈，$\pi_t$ 同时与多个对手 $\{\pi_{t-1}, \pi_{t-2}, \dots\}$ 竞争，每个对手都通过偏好预言提供比较信号。

### Pipeline 模块与数据流

MNPO 的训练流程由四个核心模块串联构成：

1. **Opponent Pool Construction（对手池构建）**  
   从历史策略或外部模型中选择对手并进行加权混合，构成当前玩家的对手集合。在时间依赖变体（TD-MNPO）中，对手为前 $n-1$ 个历史策略的加权组合；在异质变体（HT-MNPO）中，对手为不同奖励模型对应的策略。

2. **Preference Comparison（偏好比较）**  
   对每个玩家，查询偏好预言获得其与对手群体比较的偏好信号。在同质设定下，所有玩家共享同一个偏好预言；在异质设定下，每个玩家关联不同的奖励模型，构造独立的训练数据对。

3. **Multiplayer Loss Computation（多人损失计算）**  
   根据当前策略、对手策略和偏好信号计算多人博弈损失。TD-MNPO 损失（式 17）将历史策略混合作为对手，HT-MNPO 损失（式 18）则为每个玩家引入其专属的奖励差距信号 $\delta_i^\star$。

4. **Policy Update（策略更新）**  
   使用优化器最小化多人损失，通过乘性权重更新规则（式 10）迭代更新策略参数。理论保证表明，平均策略 $\bar{\pi}^{(T)}$ 以 $O(1/\sqrt{T})$ 的遗憾界收敛至 $\epsilon$-近似纳什均衡。

### 输入输出流

- **输入**：基座模型 $\pi_{\text{ref}}$、偏好预言（单一或异质）、历史策略缓存、奖励模型（HT-MNPO 下可选）
- **中间状态**：对手池的加权混合策略、偏好比较信号、奖励差距估计
- **输出**：优化后的策略 $\pi_t$，该策略在多人博弈中最小化对偶间隙（Duality Gap），逼近纳什均衡

### 统一框架特性

MNPO 的一个重要性质是其统一性：通过调整玩家数量 $n$、对手集合 $O_\pi$ 和混合权重 $\lambda_j$，可将 DPO、INPO、SPIN 等现有方法恢复为其特例（Table 1）。例如，DPO 对应 $n=2$、$O_\pi=\pi_{\text{ref}}$、$\lambda_j=1$ 的配置，而 INPO 则对应 $n=2$、在线对手的配置。这种统一性揭示了多人框架的通用性，也为理解不同偏好优化方法之间的关系提供了统一视角。



### 3.1 同质多人偏好优化

MNPO 将偏好对齐从两人博弈推广至 $n$ 人博弈。每个玩家策略 $\pi_i$ 同时与对手群体 $\{\pi_j\}_{j \neq i}$ 竞争，目标函数为：

$$J(\pi_i, \{\pi_j\}_{j \neq i}) = \mathbb{E}_{x \sim d_0} \left[ \mathbb{E}_{y^i \sim \pi_i, \{y^j \mid y^j \sim \pi_j\}_{j \neq i}} [\mathbb{P}(y^i \succ \{y^j\}_{j \neq i} \mid x)] - \tau \operatorname{KL}(\pi_i(\cdot|x) \| \pi_{\mathrm{ref}}(\cdot|x)) \right]$$

其中 $\mathbb{P}(y^i \succ \{y^j\}_{j \neq i} \mid x)$ 为 Plackett-Luce 模型下 $y^i$ 胜出所有对手的概率，$\tau$ 控制与参考策略 $\pi_{\mathrm{ref}}$ 的 KL 散度正则化强度。

**乘性权重更新** 是该框架的核心迭代机制：

$$\pi_i^{(t+1)}(\boldsymbol{y} \mid \boldsymbol{x}) \propto \left( \prod_{j \neq i} \pi_j^{(t)}(\boldsymbol{y} \mid \boldsymbol{x}) \right)^{\frac{1}{n-1}} \exp\left( \frac{\eta}{n-1} \sum_{j \neq i} \mathbb{P}\left( \boldsymbol{y} \succ \pi_j^{(t)} \mid \boldsymbol{x} \right) \right)$$

该更新以对手策略的几何平均为基底，按平均胜率优势指数放大响应概率。理论保证：平均策略 $\bar{\pi}^{(T)} = \frac{1}{T}\sum_{t=1}^T \pi^{(t)}$ 以 $\epsilon = O(1/\sqrt{T})$ 的 regret 界收敛至 $\epsilon$-近似纳什均衡。

为绕过偏好预言查询的复杂性，论文推导了等价的可计算平方损失：

$$L'_t(\pi) = \mathbb{E}_{y,y' \sim \pi_t, y_w,y_l \sim \lambda_{\mathbb{P}}(y,y')} \left[ \left( h_t(\pi, y_w, y_l) - \frac{1}{2\eta} \right)^2 \right]$$

其中 $\lambda_{\mathbb{P}}(y,y')$ 是从当前策略 $\pi_t$ 采样的响应对经偏好预言标记后的胜-负对分布，$h_t$ 编码了策略与对手间的对数概率比差异。

### 3.2 时间依赖多人扩展（TD-MNPO）

为利用训练历史中积累的策略多样性，TD-MNPO 以加权历史策略混合构建对手集合：

$$\mathcal{L}_{\mathrm{TD}}^{t,\mathrm{D}}(\pi \mid \beta, \{\lambda_j\}, \eta) = \mathbb{E}_{y,y' \sim \pi, y_w,y_l \sim \lambda_{\widetilde{\pi}}(y,y')} \mathbb{D}\left[ \log\frac{\pi(y_w|x)}{\pi(y_l|x)} - \sum_{j=0}^{n-2} \lambda_j \log\frac{\pi_{t-j}(y_w|x)}{\pi_{t-j}(y_l|x)} \mid \eta \delta^\star \right]$$

这里 $\widetilde{\pi}$ 是前 $n-1$ 个历史策略 $\{\pi_{t-j}\}_{j=0}^{n-2}$ 按权重 $\lambda_j$ 构成的混合分布，$\mathbb{D}$ 为平方距离或后向 Bernoulli KL 散度，$\delta^\star$ 为奖励差距目标。

**统一性**：TD-MNPO 将多种现有方法纳入其特例（Table 1）。例如，取 $n=2$、对手为 $\pi_{\mathrm{ref}}$、$\lambda_j=1$ 时退化为 DPO；取对手为当前策略自身时恢复 INPO 等在线方法。这一统一性源于框架对玩家数量、对手构成和权重分配的灵活配置。

### 3.3 异质多人扩展（HT-MNPO）

当不同玩家关联不同的奖励模型（偏好预言）时，每个玩家 $i$ 的损失函数为：

$$\mathcal{L}_{\mathrm{HT}}^{i,\mathrm{D}}(\pi_i \mid \beta, \{\lambda_j\}, \eta) = \mathbb{E}_{y,y' \sim \pi_i, y_w,y_l \sim \lambda_{\mathbb{P}_i}(y,y')} \mathbb{D}\left[ \log\frac{\pi_i(y_w|x)}{\pi_i(y_l|x)} - \sum_{j \neq i} \lambda_j \log\frac{\pi_j(y_w|x)}{\pi_j(y_l|x)} \mid \eta \delta_i^\star \right]$$

关键差异在于 $\delta_i^\star$ 是玩家 $i$ 专属奖励模型下的奖励差距，$\mathbb{P}_i$ 为其专属偏好预言。这使得 MNPO 能同时对齐异质甚至冲突的评估维度，趋向一种平衡多维度质量的人口均衡。需要注意的是，异质设定下乘性权重更新的收敛性缺乏形式化保证（见局限性讨论）。



## 实验与关键发现

### 主实验结果

MNPO 在三个主流指令遵循与偏好对齐基准上均取得了最优结果。Table 2 报告了以 GPT-5-mini 作为评估法官的全面对比。在 AlpacaEval 2.0 上，TD-MNPO 达到 **57.27** Length-Controlled Win Rate，HT-MNPO（Athene-RM-8B）进一步达到 **59.64**，显著超越所有 NLHF 基线。在难度更高的 Arena-Hard 上，TD-MNPO 的 Win Rate 为 **52.26**，较次优方法 INPO（48.03）提升 **+4.23** 个百分点，表明多人博弈框架在复杂对抗场景下的优势更为突出。MT-Bench 上 MNPO 同样保持领先。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_x7aLhLMVn1/figures/003_Table_2.jpg]]
*Table 2: Performance of various models on instruction-following and preference-alignment benchmarks (AlpacaEval 2.0, Arena-Hard, and MT-Bench), evaluated using GPT-5-mini as the judge*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_x7aLhLMVn1/figures/009_Table_8.jpg]]
*Table 8: Ablation of 2-player vs. 3-player HT-MNPO on AlpacaEval 2.0. 2-player scores are averaged over all pairwise judge configurations for each reward model (e.g., Armo (Skywork) and Armo (Athene) for ArmoRM-Llama3), while 3-player results are copied from the full HT-MNPO setting in Tab. 2*

在学术基准的综合评估中（Table 3），MNPO 在指令遵循、知识问答和常识推理三个维度上取得平均分 **71.08**，为所有方法中最高。在数学与代码基准上（Table 4），MNPO 的表现亦保持竞争力，说明多人博弈对齐并未损害模型的通用推理能力。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_x7aLhLMVn1/figures/004_Table_3.jpg]]
*Table 3: Model performance on instruction, knowledge, and commonsense benchmarks*

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_x7aLhLMVn1/figures/005_Table_4.jpg]]
*Table 4: Model performance on math and coding benchmarks*

### 消融实验

**玩家数量的影响。** Table 5 展示了 TD-MNPO 中玩家数 $n$ 从 1 到 4 的消融结果。AlpacaEval 2.0 LC Win Rate 从 $n=1$ 时的 53.32 持续提升至 $n=3$ 时的 57.42，验证了多人博弈框架的核心假设：增加对手多样性能够稳定优化过程并提升对齐质量。$n=4$ 时收益递减（57.42→57.27），表明三玩家配置已接近收益饱和点。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_x7aLhLMVn1/figures/006_Table_5.jpg]]
*Table 5: Ablation on the number of players (n) in TD-MNPO, where we report AlpacaEval 2.0 (lengthcontrolled win rate, %). Increasing n consistently improves alignment quality, with diminishing returns beyond n=3*

**异质偏好的增益。** Table 8 对比了 HT-MNPO 在两玩家与三玩家配置下的表现。以 ArmoRM-Llama3 为例，三玩家配置（57.63）显著优于两玩家配置的平均值（55.43），在所有奖励模型上均观察到一致趋势。这说明引入异质偏好预言能够捕捉更丰富的偏好结构，而多人框架是释放这一潜力的必要条件。

**基座模型的泛化性。** Table 6 报告了在不同基座模型上的消融结果。以 Llama-3-8B-it 为基座时，TD-MNPO 在 AlpacaEval 2.0 上达到 42.94 LC Win Rate，较 INPO（41.48）提升 +1.46，表明多人框架对不同模型架构具有一致的增益。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_x7aLhLMVn1/figures/007_Table_6.jpg]]
*Table 6: Ablation on Different Base Models. AlpacaEval 2.0 (LC) results*

### 稳定性分析

Table 7 展示了在不同 LLM 法官（GPT-4-1106、GPT-4.1、GPT-5-mini）下三次独立运行的结果。MNPO 在所有法官下均取得最高的均值，且标准差较小，说明其优化过程对评估器的选择具有鲁棒性。相比之下，SFT 和 DPO 的跨法官波动较大，INPO 虽较前两者稳定，但仍不及 MNPO。这一结果直接验证了多人博弈框架在降低梯度方差方面的理论优势——多个对手提供的梯度信号天然具有平均效应，抑制了单一对手分布导致的振荡。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_x7aLhLMVn1/figures/008_Table_7.jpg]]
*Table 7: Mean and standard deviation of model performance across three runs under different LLM judges. This illustrates both stability and relative improvements across RLHF methods*

### 框架统一性

Table 1 展示了 TD-MNPO 如何通过调整玩家数量 $n$、对手集合 $O_\pi$ 和混合权重 $\lambda_j$ 恢复现有偏好优化算法。当 $n=2$、$O_\pi=\pi_{\text{ref}}$、$\lambda_j=1$ 时，MNPO 退化为 DPO；当对手为当前策略时恢复 INPO；当对手为历史策略时恢复 SPIN。这种统一性并非简单的特例枚举，而是揭示了多人博弈框架的本质：现有方法本质上是在不同对手配置下的两人博弈近似，而 MNPO 通过显式引入对手群体，消除了这一近似带来的信息损失。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_x7aLhLMVn1/figures/002_Table_1.jpg]]
*Table 1: Time-dependent MNPO recovers many existing offline or online preference optimization algorithms. We denote the target reward gap as $\delta _ { r ^ { \star } }$ : = $\overline { { \eta \left( r ^ { \star } \left( x , y _ { 1 } \right) - r ^ { \star } \left( x , y _ { 2 } \right) \right) } }$ . Dsq and Dbwd represent the squared distance and backward Bernoulli KL divergence, respectively

### 失败模式与局限

尽管 MNPO 在各项基准上表现优异，但分析揭示了两个值得关注的瓶颈。第一，偏好预言的保真度成为性能上限：当策略模型生成质量极高时，预言区分优劣的能力下降，导致偏好信号的信息量不足，收敛可能停滞。这在 Table 5 中 $n=3$ 到 $n=4$ 的收益递减中已有体现——增加对手无法弥补预言本身的分辨力不足。第二，HT-MNPO 缺乏正式的理论收敛保证，其一般和博弈性质使得当前乘性权重更新不能确保收敛至纳什均衡，当前仅依赖经验验证其有效性。

### 补充图表

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_x7aLhLMVn1/figures/010_Table_9.jpg]]
*Table 9: Various preference optimization objectives given preference data $\mathcal { D }$ = ( x , $y ^ { + } , y ^ { - }$ ) , where x is an input, and $y ^ { + }$ and $y ^ { - }$ are the winning and losing responses. f is a class of divergence functions. $\Gamma$ ( x , y ) is the uncertainty estimator. l is a convex decreasing loss function. $\widehat { P } \left$( y $\succ \pi _ { t } \mid$ x $\right$) is the win rate over the distribution estimated by the average win rate over all the sampled responses $y _ { 1 : K } \sim \pi _ { t } ( \cdot \mid$ x )



## 定位与知识库关联

### 从两人博弈到多人博弈：统一框架的构建

MNPO 的核心贡献在于将现有偏好优化方法统一为多人博弈的特例，揭示了纳什偏好优化家族的内在结构。Table 1 系统性地展示了这一统一关系：通过调整玩家数量 $n$、对手集合 $O_\pi$ 和混合权重 $\lambda_j$，TD-MNPO 可以精确恢复多种离线与在线偏好优化算法。

具体而言，当设定 $n=2$、$O_\pi = \pi_{\text{ref}}$、$\lambda_j = 1$ 时，TD-MNPO 退化为 **DPO**，即直接从静态偏好对学习的离线基线。若保持 $n=2$ 但将对手设为当前策略自身，则恢复为 **INPO** 的在线二人纳什偏好优化范式。进一步地，**SPIN** 通过使用历史策略作为对手，在 MNPO 框架下表现为时间依赖对手混合的特例。这一统一性不仅为理解现有方法提供了统一的理论视角，更揭示了多人扩展的天然合理性：现有方法本质上是在不同的对手群体规模和信息利用方式之间做出的特定选择。

### 与现有在线偏好优化方法的关系

在在线偏好优化的谱系中，MNPO 与 **SPPO** 和 **ONPO** 形成互补关系。SPPO 采用自博弈机制，通过胜率估计更新策略，其核心是两玩家博弈的迭代；ONPO 则引入乐观镜像下降以加速收敛。MNPO 从正交的方向切入——不改变更新算子的乐观性，而是扩展博弈的参与者规模。这种扩展带来了两个关键优势：一是梯度方差的降低，因为策略需要同时应对多个对手的偏好信号，而非仅针对单一对手分布优化；二是对偏好结构中非传递性的更好捕捉，多人博弈天然能够建模循环偏好关系（A 优于 B、B 优于 C、C 优于 A），而两人博弈容易陷入振荡。

### 异质扩展与多奖励模型融合

HT-MNPO 将多人博弈进一步推广至异质偏好预言场景，每个玩家关联不同的奖励模型作为偏好判断依据。这一设计使得 MNPO 能够同时利用多个异质甚至相互冲突的评估器进行对齐，在 AlpacaEval 2.0 上达到 59.64（Athene-RM-8B）的性能，显著超越同质设定。这一扩展与多奖励模型集成方法（如 reward model ensembling）形成对比：后者通常通过加权平均或投票机制融合奖励信号，而 HT-MNPO 通过博弈均衡机制让各策略在竞争中自然平衡不同偏好维度，避免了简单聚合可能掩盖的偏好冲突。

### 适用边界与关键局限

尽管 MNPO 在实验上表现强劲，其适用边界受限于以下因素：

**偏好预言的保真度瓶颈**：当策略模型生成质量极高时，偏好预言区分优劣的能力下降。此时，被拒绝的响应本身质量也高，二进制偏好信号的信息量不足以驱动进一步改进，收敛可能停滞。这一局限是所有依赖偏好预言的方法共有的，但在 MNPO 的多人设定中尤为突出，因为多人博弈对偏好信号的质量要求更高——若预言无法有效区分多个高质量响应之间的细微差异，增加玩家数量带来的收益将递减。

**异质扩展的理论缺口**：HT-MNPO 缺乏正式的理论收敛保证。同质设定下的乘性权重更新可以证明收敛至纳什均衡，但异质设定本质上是一般和博弈（general-sum game），当前更新规则不能确保收敛至纳什均衡。这一理论缺口限制了 HT-MNPO 在最坏情况下的可靠性，尽管实验结果表明其在实际场景中表现良好。

**玩家数量的收益递减**：消融实验（Table 5）表明，将玩家数 $n$ 从 1 增加到 3 带来持续的 AlpacaEval 2.0 LC Win Rate 提升（从 53.32 到 57.42），但 $n=4$ 相较 $n=3$ 的收益微小。这一现象暗示多人博弈的边际信息增益存在上限，额外的历史策略可能引入冗余或噪声，而非新的偏好结构信息。

### 开放问题与未来方向

当前工作留下了若干值得探索的方向：

1. **异质博弈的理论收敛保证**：能否为 HT-MNPO 建立收敛理论，或探索粗相关均衡（coarse correlated equilibrium）等替代解概念，以弥合理论与实验之间的鸿沟？

2. **偏好预言的细粒度扩展**：当二进制偏好信号失效时，如何引入序数列表、连续评分或偏好强度等更丰富的反馈形式，以维持多人博弈的信息增益？

3. **对手混合权重的动态调整**：当前 TD-MNPO 使用固定的指数衰减权重混合历史策略，能否设计自适应权重机制，根据近期策略的改进幅度或对手的“挑战性”动态调整，以实现最优收敛速度？

4. **多目标对齐的博弈设计**：在多任务或多维度偏好对齐场景中，如何设计异质对手的配比和交互机制，使得博弈均衡能够同时优化多个相互冲突的目标，而非简单折衷？



## 原文 PDF

![[paperPDFs/ICLR_2026/Multiplayer_Nash_Preference_Optimization.pdf]]
