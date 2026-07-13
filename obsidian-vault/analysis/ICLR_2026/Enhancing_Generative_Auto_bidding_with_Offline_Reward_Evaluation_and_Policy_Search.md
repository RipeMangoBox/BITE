---
title: "Enhancing Generative Auto-bidding with Offline Reward Evaluation and Policy Search"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Enhancing_Generative_Auto_bidding_with_Offline_Reward_Evaluation_and_Policy_Search.pdf
project_link: null
code_link: null
openreview_forum_id: kMuQBgPIdg
aliases:
- AP
- EGABOREPS
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入一个可学习的轨迹评估器（evaluator）为规划器提供显式的轨迹质量评分，并在KL散度和Lipschitz连续性约束下安全地最大化该评分，从而在离线数据集邻近的认证区域内实现可靠的策略改进。"
primary_logic: "将离线强化学习中的保守策略搜索思想与生成式规划相结合，利用评估器的Lipschitz连续性和同步耦合技术，使生成模型在保持对离线数据的行为克隆同时，通过评估器反馈持续提升生成轨迹的质量，并在理论上确保次优性有界。"
claims:
- "AIGB-Pearl在模拟和真实世界实验中均达到SOTA性能，相比最强基线（DiffBid）GMV提升超过3%。"
- "KL约束贡献了约1.1%的GMV提升，Lipschitz约束贡献了约1.8%的GMV提升，验证了两个约束的必要性。"
- "轨迹评估器在OOD轨迹上的排序准确率AUC达到85.5%（模拟）和75.1%（真实），表明评估器在外推时仍保持较高可靠性。"
- "理论推导（Theorem 3）给出了KL-Lipschitz约束下评分最大化与真实性能之间的次优性差距上界，为安全探索提供了保证。"
---

# Enhancing Generative Auto-bidding with Offline Reward Evaluation and Policy Search

> [!tip] 核心洞察
> 将离线强化学习中的保守策略搜索思想与生成式规划相结合，利用评估器的Lipschitz连续性和同步耦合技术，使生成模型在保持对离线数据的行为克隆同时，通过评估器反馈持续提升生成轨迹的质量，并在理论上确保次优性有界。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 利用离线奖励评估与策略搜索增强生成式自动竞价 |
| 英文题名 | Enhancing Generative Auto-bidding with Offline Reward Evaluation and Policy Search |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=kMuQBgPIdg) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AIGB-Pearl |
| Dataset | Simulated experiments (30 advertisers), Real-world A/B test (6k advertisers, 19 days), Real-world TargetROAS A/B test (300k advertisers, 22 days), Simulated first-price auction |

> [!tip] 效果简介
> - Simulated experiments (30 advertisers) 上，GMV 为 502.98 (1.5k budget)，对比 480.76 (DiffBid)，变化 +4.62%。
> - Real-world A/B test (6k advertisers, 19 days) 上，GMV 为 78,676,009，对比 76,390,174 (DiffBid)，变化 +3.00%。
> - Real-world TargetROAS A/B test (300k advertisers, 22 days) 上，GMV 为 819,550,812，对比 779,642,891 (DiffBid)，变化 +5.1%。

## 概要

自动竞价是计算广告的核心决策问题，广告主需在预算约束下动态调整出价以最大化累计价值。现有生成式自动竞价方法（AIGB）通过条件生成模型从离线轨迹数据中学习规划策略，但其核心瓶颈在于**仅依赖行为克隆而缺乏对生成轨迹质量的显式反馈**——当目标条件超出离线数据分布时，模型无法进行有导向的探索，生成轨迹的可靠性急剧下降。

针对这一瓶颈，本文提出 **AIGB-Pearl**（Planning with EvaluAtor via RL），其核心思路是将离线强化学习中的保守策略搜索思想引入生成式规划框架：**训练一个可学习的轨迹评估器为生成轨迹提供显式质量评分，并在KL散度约束与Lipschitz连续性约束下安全地最大化该评分**。该设计使规划器在保持对离线数据的行为克隆同时，通过评估器反馈持续提升生成轨迹质量，并在理论上确保次优性有界（Theorem 3）。

**核心结论：**
- 在仿真实验中，AIGB-Pearl相比最强基线DiffBid的GMV提升**4.62%**（Table 1）；在真实世界A/B测试中（6k广告主，19天），GMV提升**3.00%**（Table 2）；在TargetROAS场景下（300k广告主，22天），GMV提升**5.1%**（Table 8）。
- 消融实验表明，KL约束单独贡献约**+1.1%** GMV，Lipschitz约束单独贡献约**+1.8%** GMV，验证了两个约束的必要性（Table 4）。
- 轨迹评估器在分布外轨迹上的排序准确率AUC达到**85.5%**（仿真）和**75.1%**（真实），为安全探索提供了可靠基础（Table 5）。

**方法定位：** AIGB-Pearl位于生成式自动竞价与离线强化学习的交叉点。与DiffBid等纯生成式方法相比，它引入了评估器驱动的策略搜索机制；与CQL、IQL等离线RL方法相比，它保留了生成式规划的条件采样能力，并通过同步耦合技术实现更紧的Lipschitz约束估计。

### 自动竞价与生成式规划

在线广告自动竞价的核心是在预算约束下最大化广告主的累计价值。该问题可形式化为一个马尔可夫决策过程（MDP）：

$$
\operatorname* { m a x } _ { a _ { 1 } , a _ { 2 } , \cdots , a _ { T } } \mathbb { E } _ { s _ { t + 1 } \sim \mathcal { P } ( \cdot | s _ { t } , a _ { t } ) } \bigg [ \sum _ { t = 1 } ^ { T } r _ { t } \bigg ] , \mathrm { s . t . } \sum _ { t = 1 } ^ { T } c _ { t } \leq B
$$

其中 $r_t$ 为时刻 $t$ 的即时回报（如 GMV），$c_t$ 为花费，$B$ 为总预算。传统方法依赖在线强化学习，但在真实竞价环境中进行在线探索成本极高且风险不可控。

近年来，生成式自动竞价（AIGB）方法通过条件生成模型直接从离线数据集中学习轨迹分布，避免了在线交互。其核心目标为最大化轨迹的条件似然：

$$
\operatorname* { m a x } _ { \theta } \mathbb { E } _ { ( \tau , y ( \tau ) ) \sim \mathcal { D } } [ \log p _ { \theta } ( \tau | y ( \tau ) ) ]
$$

其中 $\tau$ 为出价轨迹，$y(\tau)$ 为轨迹质量条件（如目标 ROI）。AIGB 的推理过程为：给定期望的质量条件 $y^*$，从生成模型中采样轨迹，再通过逆动力学控制器将规划的状态序列转化为具体出价动作。

### 现有方法的瓶颈

尽管 AIGB 在离线场景下展现了良好的轨迹生成能力，其本质缺陷在于**缺乏对生成轨迹质量的显式反馈机制**。具体而言：

1. **纯模仿学习的局限**：AIGB 仅通过最大化离线数据集中的轨迹似然进行训练，生成模型没有接收到关于“所生成轨迹是否真正优质”的信号。当目标条件 $y^*$ 超出离线数据分布时，模型只能依赖外推，生成质量无法保证。

2. **无导向探索**：AIGB 缺乏在离线数据分布外进行有导向探索的能力。它无法判断哪些偏离数据分布的方向是安全的、可能带来性能提升的，哪些方向会导致严重的性能退化甚至预算浪费。

3. **理论保证缺失**：现有方法未提供关于外推时生成轨迹质量的理论保证，使得在实际部署中难以评估风险边界。

### 本文动机

针对上述瓶颈，本文的动机在于：**能否在保持生成式规划框架优势的同时，引入离线强化学习中的保守策略搜索思想，为生成模型提供显式的轨迹质量反馈，并在理论上保证探索的安全性？**

具体而言，本文试图回答三个关键问题：

- **评估问题**：如何构建一个可靠的轨迹质量评估器，使其不仅在离线数据分布内准确，在分布外仍保持较高的排序可靠性？
- **优化问题**：如何在评估器的引导下，使生成模型持续提升轨迹质量，同时避免因过度追求评分而生成不可靠的轨迹？
- **理论问题**：能否为上述“评估-优化”循环提供次优性上界，从理论上认证安全探索的范围？

这些问题的解决，将使得生成式自动竞价方法从“被动模仿”走向“主动改进”，在保持离线学习安全性的同时获得持续的性能提升。

## 核心方法与创新机理

现有生成式自动竞价方法（AIGB）的核心瓶颈在于：规划器仅通过最大化离线数据集中轨迹的条件似然进行训练（Eq.3），缺乏对生成轨迹质量的显式反馈机制。这意味着模型只能在离线数据分布内进行模仿，无法在条件外推时有导向地探索更优策略——当目标条件 $y^*$ 超出数据集覆盖范围时，生成轨迹的可靠性急剧下降，甚至产生高风险行为。

AIGB-Pearl 的核心创新在于**将离线强化学习中的保守策略搜索思想与生成式规划深度融合**，通过三个关键机制实现了从“被动模仿”到“安全探索”的范式转变：

### 1. 可学习轨迹评估器：为生成质量提供显式反馈

AIGB-Pearl 引入一个独立的轨迹评估器（Trajectory Evaluator），通过监督学习为任意生成轨迹 $\tau$ 输出质量评分 $\hat{y}_\phi(\tau)$。评估器的训练损失（Eq.11）包含三个组件：
- **点式损失**：拟合真实轨迹质量标签 $y(\tau)$；
- **成对损失**：增强轨迹间相对排序能力；
- **Lipschitz 惩罚**：约束评估器对轨迹变化的敏感度，确保其在分布外区域仍保持合理预测。

该评估器使规划器首次获得显式的轨迹质量信号，为后续的策略搜索提供了优化方向。实验表明，评估器在 OOD 轨迹上的排序准确率 AUC 达到 85.5%（模拟）和 75.1%（真实），验证了其在外推时的可靠性（Table 5）。

### 2. KL-Lipschitz 约束评分最大化：理论保证的安全探索

单纯最大化评估器评分会导致规划器利用评估器缺陷生成不可靠的高分轨迹。AIGB-Pearl 提出带双重约束的评分最大化目标（Eq.8）：

$$\max_\theta L(\theta) \quad \text{s.t.} \quad \mathbb{E}_{y}[D_{\mathrm{KL}}(p_D(\tau|y) \| p_\theta(\tau|y))] \leq \delta_K, \quad \mathrm{Lip}_{W_1}(p_\theta(\tau|y)) \leq L_p$$

- **KL 散度约束**：限制规划器对离线数据条件分布的偏离，防止灾难性遗忘；
- **Lipschitz 约束**：限制生成分布对条件变化的敏感度，确保条件外推时的平滑性。

理论推导（Theorem 3）证明，在该约束下评分最大化与真实性能之间的次优性差距有界：

$$J(\theta^*) - J(\hat{\theta}) \leq 2\delta_D + (1+2k)\sqrt{T}R_m\left[\sqrt{\delta_M} + \sqrt{\delta_K} + (1+\epsilon)y_m L_p\right]$$

这为安全探索提供了理论保证：规划器在离线数据集邻近的“认证区域”内进行策略改进，该区域内评估器保持高准确度（Figure 1）。

### 3. 同步耦合 Wasserstein 估计：实现 Lipschitz 约束的实用算法

Lipschitz 约束中的 Wasserstein 距离 $W_1(p_\theta(\tau|y_1), p_\theta(\tau|y_2))$ 难以直接计算。AIGB-Pearl 提出**同步耦合技术**：对两个不同条件 $y_1, y_2$ 下的生成过程使用相同的随机噪声，从而消除随机性引入的虚假差异，得到更紧的 Wasserstein 上界。当规划器方差固定为常数时，该上界简化为生成均值差异的范数和：

$$\hat{W}_1(y_1, y_2; \theta) = \sum_t \|\mu_\theta(s_{1:t}^1, y_1, t) - \mu_\theta(s_{1:t}^2, y_2, t)\|$$

该方法被嵌入规划器训练损失（Eq.12）的 Lipschitz 惩罚项中，使理论约束可实际优化。

### 方法对比：关键变化槽位

| 变化维度 | AIGB 基线（如 DiffBid） | AIGB-Pearl |
|---------|----------------------|------------|
| **探索机制** | 无评估器，仅通过固定条件 $y^*$ 从生成模型采样 | 训练轨迹评估器提供质量评分，在约束下最大化该评分实现安全探索 |
| **规划器训练目标** | 最大化离线轨迹的条件似然（Eq.3） | 复合损失：评分最大化 + 条件行为克隆 + Lipschitz 惩罚（Eq.12） |
| **探索安全性** | 无显式约束 | KL 约束限制行为偏差，Lipschitz 约束限制条件敏感度 |
| **Wasserstein 估计** | 不涉及 | 同步耦合技术对齐生成噪声，得到更紧上界（Eq.13） |

消融实验（Table 4）量化了各创新的贡献：KL 约束单独贡献约 +1.1% GMV，Lipschitz 约束贡献约 +1.8% GMV，二者联合使用使 AIGB-Pearl 在真实世界 A/B 测试中相比最强基线 DiffBid 实现 +3.00% GMV 提升（Table 2）。

AIGB-Pearl 的整体 pipeline 围绕“生成式规划器 + 轨迹评估器”的双模块交互架构展开，核心思想是将离线强化学习中的保守策略搜索思想注入生成式自动竞价框架，使规划器在离线数据集邻近的认证区域内安全地提升生成轨迹的质量。

### 模块组成与交互关系

系统包含三个主要模块，其中前两个为本文核心贡献：

1. **轨迹评估器（Trajectory Evaluator）**：通过监督学习训练，为任意给定轨迹 $\tau$ 输出质量评分 $\hat{y}_\phi(\tau)$。训练损失由三部分组成：点式拟合损失（最小化与真实回报 $y(\tau)$ 的均方误差）、成对排序损失，以及 Lipschitz 惩罚项，确保评估器在数据分布外推时仍保持较高的排序准确率（详见 Eq.11）。评估器的输入表示进一步通过预训练大语言模型生成的语义嵌入增强，以加速收敛并提升绝对准确率。

2. **生成式规划器（Generative Planner）**：采用 Causal Transformer 架构，以目标条件 $y^*$ 为输入，自回归地生成轨迹状态序列。规划器的训练目标是一个复合损失函数（Eq.12），包含三项：
   - **评分最大化项**：最大化评估器对生成轨迹的打分，驱动策略向高质量方向探索；
   - **条件行为克隆项**：最大化离线数据集中轨迹的条件似然，保持对离线数据分布的拟合；
   - **Lipschitz 惩罚项**：利用同步耦合技术（synchronous coupling）对齐不同条件下的生成噪声，估计 Wasserstein 距离上界，限制规划器对条件变化的敏感度。

3. **逆动力学控制器（Inverse Dynamics Controller）**：从规划器生成的状态序列推断具体的出价动作。该模块与 AIGB 基线共享，非本文贡献，因此性能增益完全归因于规划器部分的改进。

### 输入输出流

- **离线训练阶段**：从离线数据集 $\mathcal{D}$ 中采样轨迹 $\tau$ 及其对应的回报条件 $y(\tau)$。评估器以轨迹为输入，以真实回报为监督信号进行训练；规划器则以目标条件 $y^*$ 为输入生成轨迹，由评估器给出评分，再结合行为克隆信号和 Lipschitz 惩罚联合优化。
- **在线推理阶段**：给定目标条件 $y^*$，规划器生成轨迹状态序列，逆动力学控制器据此输出出价动作，应用于实时竞价环境。

### 核心约束机制

整个框架的安全探索能力建立在两个关键约束之上（Eq.8）：

- **KL 散度约束**：限制规划器生成分布与离线数据条件分布之间的 KL 散度，防止行为克隆偏差过大；
- **Lipschitz 连续性约束**：限制规划器条件分布对输入条件 $y$ 变化的 Wasserstein 距离敏感度，由超参数 $L_p$ 控制。

这两个约束共同定义了离线数据集附近的一个“认证邻域”（certified neighborhood），在此区域内评估器保持高准确度，规划器可以安全地进行评分最大化探索，且理论上有次优性差距上界保证（Theorem 3, Eq.9）。图 1 给出了该约束评分最大化机制的原理示意，图 2 展示了评估器与规划器的完整交互架构。

### 3.1 问题形式化：从行为克隆到评分最大化

现有生成式自动竞价方法（AIGB）的核心训练目标是在离线数据集 $\mathcal{D}$ 上最大化轨迹的条件似然：

$$
\operatorname*{max}_{\theta} \mathbb{E}_{(\tau, y(\tau)) \sim \mathcal{D}} [\log p_{\theta}(\tau | y(\tau))] \tag{Eq.3}
$$

其中 $\tau$ 为轨迹，$y(\tau)$ 为轨迹质量标签（如累计GMV）。此目标本质是行为克隆，缺乏对生成轨迹质量的显式反馈，导致规划器在外推条件 $y^*$ 下生成不可靠。

AIGB-Pearl 的核心洞察是引入一个可学习的**轨迹评估器**（Trajectory Evaluator）$\hat{y}_{\phi}(\tau)$，为规划器提供显式的轨迹质量评分，并将规划器目标转化为在约束下最大化该评分：

$$
\operatorname*{max}_{\theta} L(\theta) \triangleq \mathbb{E}_{\tau \sim p_{\theta}(\tau \mid y^{*})} [\hat{y}_{\phi}(\tau)] \tag{Eq.4}
$$

**瓶颈分析**：直接最大化 Eq.4 会导致规划器利用评估器误差生成高评分但低真实质量的对抗性轨迹。根本原因在于评估器在离线数据分布外（OOD）的预测偏差 $|J(\theta) - L(\theta)|$ 不可控，其中 $J(\theta) = \mathbb{E}_{\tau \sim p_{\theta}(\tau|y^*)}[y(\tau)]$ 为真实性能。

**理论保证**（Theorem 2）：该偏差的上界由三项构成：
- $\delta_D$：评估器在数据集上的拟合误差；
- $(1+k)\sqrt{T}R_m \cdot \mathbb{E}_y[W_1(p_{\theta}(\tau|y^*), p_{\theta}(\tau|y))]$：规划器对条件变化的敏感度（Wasserstein距离）；
- $(1+k)\sqrt{T}R_m \cdot \mathbb{E}_y[W_1(p_{\theta}(\tau|y), p_{\mathcal{D}}(\tau|y))]$：规划器与离线数据分布的模仿误差。

### 3.2 约束评分最大化目标

为控制上述偏差，AIGB-Pearl 引入两类约束，形成核心优化目标：

$$
\operatorname*{max}_{\theta} L(\theta) \quad \mathrm{s.t.} \quad 
\mathbb{E}_{y \sim p_{\mathcal{D}}(y)} [D_{\mathrm{KL}}(p_{\mathcal{D}}(\tau|y) || p_{\theta}(\tau|y))] \leq \delta_K, \quad 
\mathrm{Lip}_{W_1}(p_{\theta}(\tau|y)) \leq L_p \tag{Eq.8}
$$

**KL散度约束**（$\delta_K$）：限制规划器对离线数据条件分布的行为克隆偏差，将第二个Wasserstein项上界压缩为 $\sqrt{\delta_K}$，防止生成分布偏离数据支撑集。

**Lipschitz约束**（$L_p$）：限制规划器对条件 $y$ 变化的敏感度，将第一个Wasserstein项上界压缩为 $(1+\epsilon)y_m L_p$，确保在条件外推时轨迹变化平滑可控。

**次优性界**（Theorem 3）：在 Eq.8 约束下，规划器真实性能的次优性差距有上界：

$$
J(\theta^{*}) - J(\hat{\theta}) \leq 2\delta_D + (1+2k)\sqrt{T}R_m \left[\sqrt{\delta_M} + \sqrt{\delta_K} + (1+\epsilon)y_m L_p\right] \tag{Eq.9}
$$

其中 $\delta_M$ 为离线数据集的行为策略次优性。该界保证了在认证邻域内的安全策略改进。

### 3.3 评估器训练

评估器通过监督学习训练，损失函数包含拟合项与Lipschitz惩罚项：

$$
l_e(\phi) = \underbrace{\mathbb{E}_{\tau \sim \mathcal{D}} [(\hat{y}_{\phi}(\tau) - y(\tau))^2]}_{\text{拟合真实标签}} + 
\beta_1 \underbrace{\mathbb{E}_{\tau_1, \tau_2} \left[|\hat{y}_{\phi}(\tau_1) - \hat{y}_{\phi}(\tau_2)| - \sqrt{T}R_m \|\tau_1 - \tau_2\|_F\right]_+}_{\text{Lipschitz惩罚}} \tag{Eq.11}
$$

**Lipschitz惩罚的作用**：强制评估器满足 $\mathrm{Lip}(\hat{y}_{\phi}) \leq \sqrt{T}R_m$，即预测值对轨迹变化的敏感度有界，从而在OOD区域保持预测稳定性。实际训练中额外引入成对损失（pair-wise loss）和LLM语义嵌入增强（Figure 8），以提升绝对准确率和排序能力。

### 3.4 规划器训练

规划器（Causal Transformer）的损失函数将 Eq.8 转化为无约束优化：

$$
l_p(\theta) = -\underbrace{\mathbb{E}_{\tau \sim p_{\theta}(\tau \mid y^{*})} [\hat{y}_{\phi}(\tau)]}_{\text{评分最大化}} - 
\beta_2 \underbrace{\mathbb{E}_{(\tau, y) \sim p_{\mathcal{D}}} [\log p_{\theta}(\tau \mid y)]}_{\text{条件行为克隆}} + 
\beta_3 \underbrace{\mathbb{E}_{y_1, y_2} \left[\hat{W}_1(y_1, y_2; \theta) - L_p |y_1 - y_2|\right]_+}_{\text{Lipschitz惩罚}} \tag{Eq.12}
$$

三项分别对应：评估器反馈驱动的策略改进、KL约束的近似实现（通过加权行为克隆）、Lipschitz约束的近似实现。

**同步耦合技术**（Synchronous Coupling）：为估计Lipschitz惩罚中的Wasserstein距离 $\hat{W}_1$，AIGB-Pearl 采用同步耦合——对两个条件 $y_1, y_2$ 下的轨迹生成使用相同的噪声序列，消除随机性差异，得到更紧的上界。当规划器方差固定为常数时，上界简化为：

$$
\hat{W}_1(y_1, y_2; \theta) = \sum_t \|\mu_{\theta}(s_{1:t}^1, y_1, t) - \mu_{\theta}(s_{1:t}^2, y_2, t)\|
$$

即仅需计算两条件下生成均值序列的逐步差异之和。该技术是满足Lipschitz约束的关键工程实现，代价是限制了模型方差的灵活性。

## 实验与关键发现

### 核心实验结论

AIGB-Pearl在模拟与真实世界实验中一致地取得了SOTA性能。在模拟实验（30个广告主）中，AIGB-Pearl的GMV达到502.98（1.5k预算），相比最强基线DiffBid（480.76）提升**+4.62%**（Table 1）。在真实世界A/B测试（6k广告主，19天）中，GMV从76,390,174提升至78,676,009，相对DiffBid提升**+3.00%**，同时购买数量（BuyCnt）提升+2.20%，ROI提升+1.89%（Table 2）。在更大规模的TargetROAS出价场景（300k广告主，22天）中，GMV提升幅度达到**+5.1%**（Table 8）。此外，在一价拍卖的模拟实验中，AIGB-Pearl同样保持优势，GMV提升+4.2%（Table 13）。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_kMuQBgPIdg/figures/003_Table_1.jpg]]
*Table 1: Overall performance (GMV) in simulated experiments with 30 advertisers. ∆ indicates the relative improvement of AIGB-Pearl against the most competitive baseline (which is underlined). Note that the absolute values are normalized without specific meanings; only ∆ matters*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_kMuQBgPIdg/figures/004_Table_2.jpg]]
*Table 2: Overall performance in real-world A/B tests, involving 6k advertisers over 19 days*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_kMuQBgPIdg/figures/019_Table_8.jpg]]
*Table 8: Overall performance of TargetROAS in real-world A/B test, involving 300k advertisers over 22 days*

由于AIGB-Pearl与DiffBid共享相同的逆动力学控制器，上述性能增益完全归因于规划器的改进。这提供了强有力的实证证据：**保守式RL驱动的评分最大化**能够有效提升生成轨迹的质量。

### 泛化能力验证

在离线数据集**未覆盖的广告主**（4k个）上的A/B测试中，AIGB-Pearl相比DiffBid仍取得+3.32%的GMV提升，相比Decision Transformer（DT）提升+3.08%（Table 3）。这表明KL-Lipschitz约束有效控制了外推风险，使模型在OOD条件下仍能生成可靠轨迹。

### 消融研究：约束机制的有效性

消融实验直接验证了两个核心约束的独立贡献（Table 4，6k广告主，8天A/B测试）：

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_kMuQBgPIdg/figures/006_Table_4.jpg]]
*Table 4: Ablation Study. The effectiveness of the KL constraint and the Lipschitz constraint in Realworld A/B tests, involving 6k advertisers over 8 days*

- **KL约束**单独贡献约**+1.1%** GMV提升。移除KL约束后，规划器生成轨迹偏离行为克隆分布，评估器评分与真实性能之间的偏差增大。
- **Lipschitz约束**单独贡献约**+1.8%** GMV提升。移除Lipschitz约束后，规划器对条件变化过度敏感，在条件外推时生成质量不稳定。

两个约束的联合使用带来了超过各自贡献之和的整体增益，说明二者之间存在协同效应：KL约束限制探索范围，Lipschitz约束保证探索方向的安全性。

### 评估器可靠性分析

轨迹评估器的质量是方法有效性的前提。在模拟实验中，评估器在OOD轨迹上的排序准确率AUC达到**85.5%**；在真实世界实验中，OOD数据的AUC为**75.1%**（Table 5，5折交叉验证）。这一结果表明评估器在外推条件下仍保持较高的排序一致性，但其绝对准确率（SMAPE）在无LLM嵌入时约为38%，说明**绝对评分精度仍有较大提升空间**——这是当前方法的一个瓶颈。

评估器训练的消融显示：联合使用点式损失（point-wise loss）和成对损失（pair-wise loss）可同时降低SMAPE并提高AUC（Table 9, Table 10）；引入预训练大语言模型生成的语义嵌入（LLM embedding）加速了评估器收敛并进一步降低SMAPE（Fig. 9）。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_kMuQBgPIdg/figures/026_Table_9.jpg]]
*Table 9: SMAPE results from ablation experiments on the trajectory evaluator*

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_kMuQBgPIdg/figures/027_Table_10.jpg]]
*Table 10: AUC results from ablation experiments on the trajectory evaluator*

### 超参数敏感性

KL约束强度$\delta_K$的调优结果显示存在明显的**探索-安全权衡**（Table 12）：适中的约束强度（$\beta_2=1.0$）获得最高GMV；约束过松时评估器偏差放大导致性能下降，约束过紧时探索不足无法充分利用评估器反馈。Lipschitz常数$L_p$的下界由离线数据集中轨迹质量的条件分布Lipschitz值（实测为1.62）确定（Section 4.4），实际选择需略高于该下界以允许一定程度的策略改进。

### 多模态数据分布下的鲁棒性

在多策略数据收集场景（即离线数据来自多个不同质量的竞价策略）中，AIGB-Pearl仍保持一致的性能优势（Table 11）。这表明方法能够有效处理离线数据中的多模态分布，KL约束在此场景下起到了防止模型向单一模式坍缩的作用。

### 失败模式与局限

1. **评估器绝对精度瓶颈**：在无LLM嵌入时SMAPE约38%，即使加入嵌入后仍有改进空间。评估器的绝对误差会通过评分最大化被放大，限制最终的策略改进幅度。
2. **超参数依赖**：$\delta_K$和$L_p$需离线调优，缺乏在线自适应机制。实际部署中，数据分布漂移可能导致预设超参数不再最优。
3. **同步耦合的方差假设**：同步耦合技术要求规划器使用固定方差以得到更紧的Wasserstein上界，这限制了生成模型的表达能力。
4. **理论界的紧致性**：次优性差距上界（Theorem 3）中的常数$\delta_M$在实验中难以直接观测和估计，理论保证的实际指导意义受限。

## 定位与知识库关联

### 与生成式自动竞价（AIGB）的关系

AIGB-Pearl 直接建立在 AIGB 框架之上，沿用了其核心架构组件：因果Transformer规划器与逆动力学控制器。基线方法 **DiffBid** 作为 AIGB 的代表实现，通过最大化离线数据集中轨迹的条件似然（Eq.3）训练规划器，本质上是一种条件行为克隆。AIGB-Pearl 的关键突破在于识别并解决了 AIGB 的根本瓶颈——缺乏对生成轨迹质量的显式反馈机制。通过引入可学习的轨迹评估器，AIGB-Pearl 将规划器训练从被动模仿转变为主动的、受反馈引导的策略搜索过程。实验表明，在共享相同逆动力学控制器的条件下，AIGB-Pearl 相比 DiffBid 在真实世界 A/B 测试中实现 GMV +3.00% 的提升（Table 2），验证了规划器层面的改进是性能增益的唯一来源。

### 与离线强化学习方法的联系

AIGB-Pearl 的核心洞察——在离线数据邻近区域内进行保守的策略改进——与离线强化学习（Offline RL）的保守思想高度一致。论文将 AIGB-Pearl 与多个经典离线RL基线进行了对比，包括：

- **CQL**（Conservative Q-Learning）：通过惩罚分布外动作的Q值来保证策略保守性
- **IQL**（Implicit Q-Learning）：利用期望回归避免查询分布外动作
- **BCQ**（Batch-Constrained Q-Learning）：约束策略仅在数据支持区域内生成动作
- **MOPO**（Model-based Offline Policy Optimization）：在模型不确定性惩罚下进行策略优化
- **DT**（Decision Transformer）：将离线RL建模为序列预测问题

然而，这些方法在自动竞价场景中面临独特挑战：竞价环境的高维状态空间和长序列决策特性使得传统离线RL方法训练不稳定。Figure 10 的对比实验显示，离线RL方法在10个随机种子下的累计奖励学习曲线波动显著，而 AIGB-Pearl 表现出更稳定的训练动态。AIGB-Pearl 的创新在于将离线RL的保守探索原则与生成式规划相结合：KL散度约束扮演了类似 BCQ 的分布约束角色，Lipschitz 约束则提供了类似于 MOPO 中模型不确定性惩罚的安全保障，但通过生成模型的条件机制实现了更高效的实现。

### 理论定位与保证

AIGB-Pearl 提供了形式化的次优性差距上界（Theorem 3），这在生成式自动竞价领域是首次。该理论框架将规划器的真实性能与评估器评分之间的差距分解为三项：数据集偏差项 δ_D、由KL约束控制的模仿误差项 √δ_K、以及由Lipschitz约束控制的条件敏感度项 (1+ε)y_m L_p。这一理论定位使 AIGB-Pearl 区别于纯粹的启发式方法，为安全探索提供了可量化的保证。然而，理论界的紧致性依赖于评估器 Lipschitz 常数的精确估计，实际中常数 δ_M（模型偏差）难以直接观测，这构成了从理论到实践的一个关键缺口。

### 适用边界

**有效适用场景：**
- 存在高质量离线轨迹数据集的竞价环境，数据覆盖了主要的状态-动作空间
- 广告主数量规模较大（实验验证了 6k 到 300k 广告主），使得统计规律稳定
- 需要对外推条件（如新的预算约束或目标ROAS）生成可靠竞价策略

**受限或未验证场景：**
- 非平稳环境：当竞争对手策略持续变化时，评估器的准确性可能退化。论文未对此进行系统验证
- 多智能体博弈：实验仅在单一广告主视角下进行，未考虑广告主之间的策略相互影响
- 其他竞价机制：实验仅在阿里巴巴广告系统（第二价格拍卖变体）上进行，第一价格拍卖的模拟实验（Table 13）虽显示 +4.2% 提升，但真实世界的泛化性未经验证
- 数据极度稀疏的冷启动场景：评估器的绝对准确率在无 LLM 嵌入时 SMAPE 约 38%，在数据稀疏时可能进一步恶化

### 局限性与开放问题

**已识别的技术局限：**

1. **同步耦合的灵活性受限**：同步耦合技术要求规划器使用固定的预测方差以得到更紧的 Wasserstein 上界。这简化了计算但限制了模型对不确定性的表达能力。如何设计更灵活的耦合方法以适应可变的生成方差是一个待解问题。

2. **评估器准确性的依赖**：尽管评估器在 OOD 轨迹上的排序准确率 AUC 达到 85.5%（模拟）和 75.1%（真实）（Table 5），但其绝对准确率（SMAPE）仍有较大改进空间。评估器误差会通过评分最大化目标传播至规划器，可能限制最终的策略改进幅度。LLM 嵌入增强（Section E.1.1）在一定程度上缓解了此问题，但未能根本解决。

3. **超参数的自适应调节**：KL约束强度 δ_K 和 Lipschitz 常数 L_p 需要离线调优。Table 12 显示适中的 KL 约束强度（β₂=1.0）获得最高 GMV，过于松弛或过紧均导致性能下降。Figure 7 揭示了超参数选择中的权衡：更大的 δ_K 和 L_p 降低了理论下界但抬高了上界。能否在训练过程中在线自适应调节这些超参数，以自动平衡探索与安全，是一个重要的开放问题。

4. **理论常数估计**：Theorem 3 中的常数 δ_M（模型偏差）在实际中难以观测，论文未提供可靠的估计方法，这削弱了理论界对实践的直接指导作用。

**开放研究方向：**

- 如何在多智能体自动竞价场景中扩展 AIGB-Pearl，考虑广告主之间的策略博弈和均衡行为？
- 评估器在非平稳环境下的鲁棒性如何维持？是否需要在线更新机制？
- 能否将 AIGB-Pearl 的保守探索框架应用于其他生成式序列决策问题（如推荐系统、库存管理）？
- 是否存在更紧的理论界，能够更精确地刻画评分最大化与真实性能改进之间的关系？

## 原文 PDF

![[paperPDFs/ICLR_2026/Enhancing_Generative_Auto_bidding_with_Offline_Reward_Evaluation_and_Policy_Search.pdf]]
