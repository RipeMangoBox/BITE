---
title: "Online Learning and Equilibrium Computation with Ranking Feedback"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Online_Learning_and_Equilibrium_Computation_with_Ranking_Feedback.pdf
project_link: null
code_link: null
openreview_forum_id: lg6H2oJPky
aliases:
- A2IRA3AR
- OLECRF
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "排序反馈的类型（瞬时效用 InstUtil Rank vs. 时间平均效用 AvgUtil Rank）、Plackett-Luce 排名模型的温度参数 τ，以及效用向量总变化的次线性假设，直接决定了能否实现次线性后悔。"
primary_logic: "将完整排序拆解为成对比较，利用逻辑函数的单调性和可逆性从比较频率中恢复底层效用估计，配合滑动窗口处理非平稳性，即可在仅含排序反馈的非随机环境中实现次线性后悔；特别地，在全信息 AvgUtil Rank 且 τ 为常数时，次线性变化假设可被移除，而在 InstUtil Rank 下则需要该假设。"
claims:
- "在 InstUtil Rank 排序反馈下，任何算法都无法实现次线性期望后悔（线性缺口定理）。"
- "本文提出算法在效用向量的总变化次线性（Assumption 4.2）时能够达成次线性后悔。"
- "在全信息 AvgUtil Rank 反馈且 τ 为常数时，上述次线性变化假设可以被移除。"
- "HH-RLHF 数据集（LLM 路由任务） 上 平均后悔 (Average Regret) = Algorithm 3（AvgUtil Rank，强盗反馈）"
---

# Online Learning and Equilibrium Computation with Ranking Feedback

> [!tip] 核心洞察
> 将完整排序拆解为成对比较，利用逻辑函数的单调性和可逆性从比较频率中恢复底层效用估计，配合滑动窗口处理非平稳性，即可在仅含排序反馈的非随机环境中实现次线性后悔；特别地，在全信息 AvgUtil Rank 且 τ 为常数时，次线性变化假设可被移除，而在 InstUtil Rank 下则需要该假设。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于排序反馈的在线学习与均衡计算 |
| 英文题名 | Online Learning and Equilibrium Computation with Ranking Feedback |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=lg6H2oJPky) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Algorithm 2 (for InstUtil Rank) and Algorithm 3 (for AvgUtil Rank) |
| Dataset | HH-RLHF 数据集（LLM 路由任务）, 合成博弈（均衡计算） |

> [!tip] 效果简介
> - HH-RLHF 数据集（LLM 路由任务） 上，平均后悔 (Average Regret) 为 Algorithm 3（AvgUtil Rank，强盗反馈），对比 始终提供事后最佳固定 LLM 模型的表现，变化 平均后悔随时间下降并快速逼近基线。
> - 合成博弈（均衡计算） 上，可剥削度 (Exploitability) 为 Algorithm 2 和 Algorithm 3（多种设置），对比 粗相关均衡 (CCE) 的理想可剥削度 0，变化 可剥削度随 t 增加而下降，表明收敛至近似 CCE。

## 概要

**问题瓶颈**：传统在线学习与均衡计算依赖精确的数值效用反馈，但在人机协同、隐私受限等真实场景中，反馈往往仅以行动排序的形式存在——用户只给出偏好顺序，不提供具体评分。如何从这种排序反馈中实现次线性后悔，是该领域的核心瓶颈。

**核心因果旋钮**：问题的可解性取决于三个关键因素：排序反馈的类型（瞬时效用排序 InstUtil Rank vs. 时间平均效用排序 AvgUtil Rank）、Plackett-Luce 排名模型的温度参数 τ，以及效用向量随时间总变化的增长速度。这三者共同决定了能否以及如何实现次线性后悔。

**核心洞见**：将完整排序拆解为成对比较，利用逻辑函数的单调可逆性从比较频率中恢复底层效用估计，配合滑动窗口处理非平稳性，即可在仅含排序反馈的非随机环境中实现次线性后悔。特别地，在全信息 AvgUtil Rank 且 τ 为常数时，对效用变化的次线性假设可被移除；而在 InstUtil Rank 下，该假设是必需的。

**决定性证据**：
- 在 InstUtil Rank 排序反馈下，任何算法都无法实现次线性期望后悔——存在线性缺口下界（置信度 0.95）。
- 本文提出算法在效用向量总变化次线性（Assumption 4.2，即 $P^{(T)} \le \mathcal{O}(T^q), q<1$）时能够达成次线性后悔（置信度 0.95）。
- 在全信息 AvgUtil Rank 反馈且 τ 为常数时，上述次线性变化假设可被移除（置信度 0.95）。

**方法定位**：本文提出两类算法——Algorithm 2 处理 InstUtil Rank，Algorithm 3 处理 AvgUtil Rank——均遵循“效用估计 + 在线学习黑盒”的模块化架构。效用估计模块（Algorithm 1）通过滑动窗口内的成对比较计数与逆 sigmoid 映射从排序置换中恢复隐藏效用；在线学习黑盒（如 FTRL）将估计效用作为输入产生新策略；在强盗设定下，额外引入探索混合机制以保证每个动作被提出的概率下界为正。该方法谱系位于“排序反馈下的在线学习”这一新兴交叉领域，区别于传统的数值反馈在线学习和纯偏好学习。

**主要结果**：在 HH-RLHF 数据集（LLM 路由任务）上，Algorithm 3 在 AvgUtil Rank 强盗反馈下的平均后悔随时间下降并快速逼近事后最佳固定模型的基线（Figure 2）。在合成博弈的均衡计算中，Algorithm 2 和 Algorithm 3 的可剥削度随迭代轮次增加而下降，表明策略收敛至近似粗相关均衡（Figure 3, 7–9）。温度 τ 和提议动作数量 K 的影响已通过实验系统评估。

**局限与开放问题**：当前工作尚未闭合 AvgUtil Rank 在强盗反馈下的下界与上界间隙——τ 为常数时是否困难未知。理论结果主要基于合成对抗环境，尚未在实际骑乘共享或在线约会等真实排序反馈场景中验证。能否在非平稳偏好环境下保持次线性后悔，以及高维真实数据上的效用估计质量是否需要进一步调整，均有待探索。



### 核心瓶颈：从数值反馈到排序反馈

在线学习与均衡计算的经典理论建立在**数值效用反馈**之上——学习者每轮能直接观测到所选行动的精确效用值，或至少获得一个无偏估计（强盗反馈）。但在大量人机协同或隐私受限的真实应用中，这一前提并不成立。平台推荐餐厅、约会应用匹配对象、LLM 路由选择模型时，用户往往只能以**行动排序**的形式表达偏好，而无法提供精确的数值评分。例如，顾客可能将推荐的菜品从最喜欢到最不喜欢进行排列，却不会给出每道菜的具体评分。这种排序反馈缺失了效用值的绝对尺度信息，使得传统依赖数值比较的后悔最小化框架面临根本性挑战。

本文正是针对这一落差展开研究：**当反馈仅以排序形式存在时，能否以及如何实现次线性后悔？**

### 排序反馈的两种范式

为系统刻画排序反馈的多样性，本文区分了两种生成机制，其核心差异在于排序所依据的评分向量 $r^{(t)}$ 的选择：

- **瞬时效用排序（InstUtil Rank）**：每轮排序基于当前时刻的瞬时效用向量 $\pmb{u}^{(t)}$ 生成，反映用户即时的偏好状态。
- **时间平均效用排序（AvgUtil Rank）**：排序基于截至当前时刻的累积平均效用 $\pmb{u}_{\mathrm{avg}}^{(t)} := \frac{1}{t} \sum_{s=1}^{t} \pmb{u}^{(s)}$，反映用户长期积累的满意度。

两种范式对应不同的现实场景：InstUtil Rank 适用于偏好快速变化的推荐系统，而 AvgUtil Rank 更贴近用户对服务质量的整体评价（如对司机或约会对象的长期印象）。排序的随机性由 Plackett-Luce 模型刻画，其温度参数 $\tau$ 控制排序的确定性程度——$\tau \to 0^+$ 时排序几乎完全由效用决定，$\tau$ 较大时则引入更多随机噪声。

### 理论挑战：线性缺口与可行性边界

本文首先揭示了排序反馈带来的根本性困难：

- **InstUtil Rank 下的不可能性**：在瞬时效用排序反馈下，任何算法都无法实现次线性期望后悔。这一线性缺口定理表明，仅凭排序信息无法在非平稳环境中有效追踪效用变化。
- **AvgUtil Rank 的条件可行性**：当温度参数 $\tau$ 足够小（即排序过于确定）时，AvgUtil Rank 同样面临次线性后悔的不可达性（至多对数因子的间隙）。这意味着排序反馈的信息损失并非在任何情况下都能被补偿。

这些下界结果（总结于 Table 1）划定了排序反馈下在线学习的理论可行性边界，也构成了本文算法设计的出发点：**在何种附加条件下，可以突破这些不可能性？**

### 核心洞察与本文路径

本文的关键洞察在于：**将完整排序拆解为成对比较，利用逻辑函数的单调性和可逆性从比较频率中恢复底层效用估计，配合滑动窗口处理非平稳性，即可在仅含排序反馈的非随机环境中实现次线性后悔。** 具体而言：

1. **效用估计**：通过滑动窗口内的成对比较计数与逆 sigmoid 映射，从 Plackett-Luce 排序中恢复隐藏的效用向量（Algorithm 1），将排序反馈转化为带噪的数值信号。
2. **非平稳性控制**：引入效用向量的次线性变化假设 $P^{(T)} := \sum_{t=2}^{T} \| \pmb{u}^{(t)} - \pmb{u}^{(t-1)} \| \le \mathcal{O}(T^q)$（$q < 1$），确保滑动窗口内的效用漂移可控。
3. **范式差异**：在 InstUtil Rank 下，次线性变化假设是必需的，算法可达成 $\mathcal{O}(T^{2/3})$ 等次线性后悔界；而在全信息 AvgUtil Rank 且 $\tau$ 为常数时，该假设可被完全移除——因为时间平均天然平滑了效用波动。

本文随后将这一框架扩展至均衡计算：在多智能体博弈中，每个玩家仅接收排序反馈，中介平台通过在线无悔学习使联合策略收敛至近似粗相关均衡（$\epsilon$-CCE）。实验部分在合成博弈和 HH-RLHF 数据集上的 LLM 路由任务中验证了理论发现（Figures 2–9），并揭示了温度 $\tau$ 和提议动作数 $K$ 对后悔及可剥削度的系统影响。

### 遗留问题

尽管本文在排序反馈的在线学习理论中取得了突破性进展，仍有若干关键问题悬而未决：AvgUtil Rank 在强盗反馈下当 $\tau$ 为常数时的下界与上界间隙尚未闭合；所提算法尚未在真实排序反馈场景（如拼车匹配、在线约会）中部署验证；非平稳偏好随时间变化的拓展也值得进一步探索。这些开放问题指向排序反馈学习理论的下一个重要前沿。



## 核心方法与创新机理

本文的核心创新在于将在线学习与均衡计算从对**数值效用反馈**的依赖中解放出来，构建了一套仅需**排序反馈**即可实现次线性后悔与近似均衡收敛的算法框架。其关键创新点可归纳为以下三个相互耦合的维度。

### 1. 反馈机制的范式转换：从数值效用到排序置换

传统在线学习（无论是全信息还是强盗反馈）均假设学习者能获取行动的精确效用值或至少一个带噪的数值信号。本文首次系统性地将反馈机制替换为**基于 Plackett-Luce 模型的排序置换**，并区分了两种具有本质不同的排序反馈类型：

- **瞬时效用排序（InstUtil Rank）**：排序依据当前时刻的效用向量 $\mathbf{u}^{(t)}$ 生成。该设定下，反馈仅反映瞬时偏好，与历史无关。
- **时间平均效用排序（AvgUtil Rank）**：排序依据截至当前时刻的累积平均效用 $\mathbf{u}_{\mathrm{avg}}^{(t)}$ 生成。该设定更贴近用户基于长期体验给出评价的真实场景，但引入了时间耦合性。

这一转换直接回应了人机协同、推荐系统、隐私保护等应用中“用户只愿给出相对偏好排序而不愿提供精确评分”的现实瓶颈。反馈类型的区分并非简单的设定枚举，而是揭示了排序反馈的**时间语义**对学习难度的根本性影响：InstUtil Rank 下，即使效用向量的总变化次线性，任何算法都无法实现次线性期望后悔（线性缺口定理）；而 AvgUtil Rank 在温度参数 $\tau$ 为常数时，则可移除对效用变化次线性的依赖。

### 2. 效用估计的因果机制：从成对比较到逆 S 形映射

在无法直接观测效用值的情况下，本文的核心技术洞察是：**完整排序可被解构为成对比较，而 Plackett-Luce 模型中任意两动作的胜率与它们的隐藏效用差之间存在由逻辑函数（sigmoid）刻画的单调可逆关系**。基于此，Algorithm 1 通过以下步骤实现从排序置换到效用估计的因果链：

1. **滑动窗口计数**：在最近 $m$ 轮排序中，统计每对动作的胜率。
2. **逆 S 形映射**：利用逻辑函数的可逆性，从胜率反推隐藏效用差。
3. **效用漂移控制**：滑动窗口的长度 $m$ 决定了统计误差与效用漂移之间的权衡——窗口越长，方差越小，但在非平稳环境中引入的偏差越大。

该估计器的误差界（Theorem 5.1）由两项构成：统计误差项 $\mathcal{O}(\tau \sqrt{\log(|\mathcal{A}|/\delta) / m'})$ 和窗口内效用漂移项 $\sum \|\mathbf{u}^{(s+1)} - \mathbf{u}^{(s)}\|_\infty$。这一分解直接揭示了排序反馈下学习的核心调节旋钮：温度参数 $\tau$ 控制排序的随机性（$\tau$ 越小，排序越确定，但估计越困难），效用向量的总变化 $P^{(T)}$ 则决定非平稳性带来的漂移代价。

### 3. 算法设计的模块化架构与反馈类型自适应

本文的算法设计采用高度模块化的流水线架构，将排序反馈下的学习问题分解为四个可替换模块：

| 模块 | 功能 | 全信息设定 | 强盗设定 |
|------|------|-----------|----------|
| 动作提议 | 确定本轮参与排序的动作集 | 全部动作 | 从当前策略 $\pi^{(t)}$ 独立有放回采样 $K$ 个动作 |
| 效用估计 (Algorithm 1) | 从排序置换恢复隐藏效用 | 直接估计 $\mathbf{u}^{(t)}$ | 估计 $\mathbf{u}^{(t)}$ 或 $\mathbf{u}_{\mathrm{avg}}^{(t)}$ |
| 在线学习黑盒 (如 FTRL) | 从估计效用产生新策略 | 标准全信息算法 | 标准全信息算法 |
| 探索混合 | 保证每个动作被提出的概率下界 | 无需 | $\pi^{(t+1)} = (1-\gamma) \cdot \text{Alg} + \gamma \cdot \text{Uniform}$ |

这一架构的核心优势在于**反馈类型与学习算法的解耦**：效用估计模块负责处理排序反馈的特殊性，而在线学习黑盒可以是任意标准的全信息无悔算法（如 FTRL、OGD）。对于 InstUtil Rank，Algorithm 2 直接估计当前效用并输入黑盒；对于 AvgUtil Rank，Algorithm 3 则利用平均效用向量的变化上界独立于累积变化这一关键性质，在 $\tau$ 为常数时移除了对 $P^{(T)}$ 次线性的依赖。在强盗设定下，Algorithm 3 进一步引入分块估计策略，将时间步划分为大小为 $M$ 的块，通过块内效用平均来平衡估计的偏差与方差。

### 创新边界与未闭合问题

尽管本文在排序反馈下的在线学习理论上取得了系统性突破，但仍存在两个关键缺口：**AvgUtil Rank 在强盗反馈下的下界与上界之间尚未闭合**——当 $\tau$ 为常数时，该设定的固有难度未知；以及所有理论结果尚未在真实排序反馈场景（如乘车共享匹配、在线约会）中得到验证。



本文提出了一套从排序反馈中实现在线学习与均衡计算的通用算法框架。该框架的核心思路是：将仅含排序信息的反馈转化为可被标准在线学习算法消费的数值效用估计，从而复用成熟的后悔最小化技术。整体流程由四个关键模块串联构成，根据反馈类型（InstUtil Rank / AvgUtil Rank）和信息结构（全信息 / 强盗反馈）的不同，模块内部的实现细节有所差异。

### 模块一：动作提议

在每个时间步，学习器需要决定向环境（或用户）提议哪些动作，以获取相应的排序反馈。

- **全信息设定**：提议动作集 $o^{(t)}$ 直接包含全部动作，即 $o^{(t)} = \mathcal{A}$。
- **强盗设定**：从当前策略 $\pi^{(t)}$ 中独立有放回地采样 $K$ 个动作构成 $o^{(t)}$，$|o^{(t)}| = K$。这一采样方式确保了每个动作被提议的概率与当前策略成比例，为后续的效用估计提供了概率基础。

### 模块二：效用估计（Algorithm 1）

这是框架的核心创新模块。由于环境只返回提议动作的排序 $\sigma^{(t)}$ 而非数值效用，需要从排序中恢复底层效用向量的估计 $\widetilde{\boldsymbol{u}}^{(t)}$。

**估计机制**：利用 Plackett-Luce 排名模型中成对比较概率与效用差异之间的单调关系。具体而言，在最近 $m$ 轮的滑动窗口内，统计任意两个动作 $a, a'$ 的胜率（即 $a$ 排在 $a'$ 之前的频率），然后通过逆 sigmoid 映射将该胜率转换为效用差的估计。这一过程将完整的排序置换拆解为成对比较，从而将排序反馈问题规约为二值比较的聚合问题。

**滑动窗口的作用**：窗口长度 $m$ 控制着估计的偏差-方差权衡。较大的 $m$ 降低统计方差，但会引入更多历史数据，在非平稳环境下可能增加偏差（因为较早的效用与当前效用差异更大）。这一权衡在 InstUtil Rank 下尤为关键，因为效用向量本身随时间变化；而在 AvgUtil Rank 下，由于排序基于时间平均效用，效用向量的变化幅度天然较小（每步变化不超过 $\mathcal{O}(1/t)$），估计难度显著降低。

### 模块三：在线学习黑盒

将估计得到的效用向量 $\widetilde{\boldsymbol{u}}^{(t)}$ 输入一个标准的全信息在线学习算法（如 Follow-The-Regularized-Leader, FTRL），该算法作为一个确定性的黑盒预言机，输出更新后的策略 $\pi^{(t+1)}$。框架对此模块无特殊约束，任何具有次线性后悔保证的全信息算法均可直接嵌入。

**AvgUtil Rank 的特殊要求**：在 AvgUtil Rank 下，由于反馈本身基于累积平均效用，要求所嵌入的在线学习算法具有“稳定性”——即对累积效用的小幅扰动不敏感。FTRL 是满足这一性质的典型选择。

### 模块四：探索混合（仅强盗设定）

在强盗反馈设定下，动作提议依赖于当前策略的采样。为确保每个动作都有被提议的正概率下界（从而保证效用估计的覆盖性），将黑盒算法输出的策略与均匀分布进行混合：

$$\pi^{(t+1)} = (1 - \gamma) \cdot \text{Alg}\left((\widetilde{\boldsymbol{u}}^{(s)})_{s=1}^{t}\right) + \gamma \cdot \frac{\mathbf{1}(\mathcal{A})}{|\mathcal{A}|}$$

其中 $\gamma \in (0, 1)$ 为探索系数。这一混合保证了 $\min_a \pi^{(t+1)}(a) \geq \gamma / |\mathcal{A}|$，为效用估计中的成对比较提供了足够的样本量。

### 两种反馈类型下的算法实例化

框架针对两类排序反馈分别实例化为 Algorithm 2（InstUtil Rank）和 Algorithm 3（AvgUtil Rank），其流程差异可通过 Figure 10 和 Figure 11 直观理解：

- **Algorithm 2（InstUtil Rank）**：效用估计模块直接估计当前时刻的瞬时效用 $\boldsymbol{u}^{(t)}$，估计误差受滑动窗口内效用漂移的累积影响。因此，需要效用向量的总变化 $P^{(T)}$ 为次线性（Assumption 4.2）才能保证整体后悔的次线性。
- **Algorithm 3（AvgUtil Rank）**：效用估计模块估计的是截至当前时刻的时间平均效用 $\boldsymbol{u}_{\text{avg}}^{(t)}$。由于平均效用的逐步变化自动以 $\mathcal{O}(1/t)$ 衰减，在全信息且温度参数 $\tau$ 为常数时，不再需要额外的次线性变化假设即可实现次线性后悔。在强盗设定下，则需引入分块估计策略来处理采样偏差，此时 $P^{(T)}$ 的次线性假设仍然必要。

### 输入输出流总结

| 阶段 | 输入 | 输出 |
|------|------|------|
| 动作提议 | 当前策略 $\pi^{(t)}$ | 提议动作集 $o^{(t)}$ |
| 排序反馈 | $o^{(t)}$、环境效用 | 排序 $\sigma^{(t)} \sim \text{PL}(r^{(t)}, \tau)$ |
| 效用估计 | 最近 $m$ 轮的 $(\sigma, o)$ 历史 | 效用估计 $\widetilde{\boldsymbol{u}}^{(t)}$ |
| 策略更新 | $\widetilde{\boldsymbol{u}}^{(1:t)}$ | 新策略 $\pi^{(t+1)}$（强盗设定下经探索混合） |

这一模块化设计使得框架具有高度的灵活性：效用估计模块可独立优化，在线学习黑盒可替换为任意前沿算法，而探索混合机制则为强盗设定提供了必要的统计保障。



### 问题形式化与反馈模型

本文研究一个 $T$ 轮在线学习问题，其中智能体在每轮 $t$ 选择一个策略 $\pi^{(t)} \in \Delta^A$，环境生成效用向量 $\pmb{u}^{(t)} \in [0,1]^{|A|}$。智能体无法直接观测 $\pmb{u}^{(t)}$，而是收到一个基于 Plackett-Luce (PL) 模型的排序反馈。具体而言，给定提议动作集 $o^{(t)}$ 和评分向量 $\pmb{r}^{(t)}$，观察到完整排序 $\sigma^{(t)}$ 的概率为：

$$
\mathbb{P}\left( \sigma^{(t)} \mid o^{(t)} \right) = \prod_{k_1=1}^{K} \frac{\exp\left( \frac{1}{\tau} r^{(t)}\left( \sigma^{(t)}(k_1) \right) \right)}{\sum_{k_2=k_1}^{K} \exp\left( \frac{1}{\tau} r^{(t)}\left( \sigma^{(t)}(k_2) \right) \right)}
$$

其中 $\tau > 0$ 为温度参数，控制排序的随机性：$\tau \to 0$ 时排序趋于确定性（按效用严格降序），$\tau \to \infty$ 时趋于均匀随机。

本文考虑两种排序反馈类型，取决于 $\pmb{r}^{(t)}$ 的选取方式：

- **InstUtil Rank**（瞬时效用排序）：$\pmb{r}^{(t)} = \pmb{u}^{(t)}$，即按当前时刻的瞬时效用排序。
- **AvgUtil Rank**（时间平均效用排序）：在全信息设定下 $\pmb{r}^{(t)} = \frac{1}{t} \sum_{s=1}^{t} \pmb{u}^{(s)}$；在强盗设定下 $\pmb{r}^{(t)} = \pmb{u}_{\text{empirical}}^{(t)}$，其中经验效用定义为：

$$
u_{\text{empirical}}^{(t)}(a) := \frac{\sum_{s=1}^{t} u^{(s)}(a) \sum_{a' \in o^{(s)}} \mathbb{1}(a = a')}{\sum_{s=1}^{t} \sum_{a' \in o^{(s)}} \mathbb{1}(a = a')}
$$

智能体的目标是最小化外部后悔：

$$
R^{(T), \mathrm{external}} := \max_{\widehat{\pi} \in \Delta^{A}} \sum_{t=1}^{T} \langle \pmb{u}^{(t)}, \widehat{\pi} - \pi^{(t)} \rangle
$$

### 核心模块：效用估计 (Algorithm 1)

从排序反馈中学习的核心挑战在于恢复隐藏的数值效用。本文的核心设计是将完整排序拆解为成对比较，利用逻辑函数的单调可逆性从比较频率中估计底层效用。

Algorithm 1 使用一个长度为 $m$ 的滑动窗口，基于最近 $m$ 轮的排序观测来估计当前效用向量 $\widetilde{\pmb{u}}^{(t)}$。具体步骤为：

1. **成对比较计数**：在窗口内统计任意两个动作 $a, a'$ 的相对排序频率——即 $a$ 排在 $a'$ 之前的比例。
2. **逆 sigmoid 映射**：利用 PL 模型中成对比较概率与效用差的逻辑函数关系，对频率应用逆 sigmoid 变换，得到效用差的估计。
3. **效用重建**：从成对效用差中恢复出绝对效用值。

该模块的估计误差由两部分组成（以 InstUtil Rank 为例）：

$$
\left\| \widetilde{\pmb{u}}^{(t)} - \pmb{u}^{(t)} \right\|_{\infty} \leq \underbrace{\frac{\tau \left( e^{\frac{1}{\tau}} + 1 \right)^{2}}{p} \sqrt{\frac{\log\left( \frac{4 |\mathcal{A}|}{\delta} \right)}{m'}}}_{\text{统计误差}} + \underbrace{\sum_{s=t-m'+1}^{t-1} \left\| \pmb{u}^{(s+1)} - \pmb{u}^{(s)} \right\|_{\infty}}_{\text{窗口内效用漂移}}
$$

其中 $p$ 是任意两个动作同时被提议的概率下界（全信息下 $p=1$，强盗下 $p$ 由探索混合保证），$m'$ 是实际使用的窗口大小。这一分解揭示了算法设计的核心权衡：增大窗口 $m$ 可降低统计误差，但会累积更多的效用漂移。

### 核心模块：在线学习黑盒与探索混合

Algorithm 1 输出的估计效用 $\widetilde{\pmb{u}}^{(t)}$ 被直接送入标准全信息在线学习算法（如 Follow-The-Regularized-Leader, FTRL），作为确定性黑盒使用。该黑盒负责从估计效用中更新策略。

在强盗设定下，为保证每个动作被提议的概率有正下界（从而保证效用估计的覆盖性），算法额外引入**探索混合**模块：将黑盒输出的策略与均匀分布混合：

$$
\pi^{(t+1)} = (1 - \gamma) \cdot \text{Alg}\left( (\widetilde{\pmb{u}}^{(s)})_{s=1}^{t} \right) + \gamma \cdot \frac{\mathbf{1}(A)}{|A|}
$$

其中 $\gamma \in (0,1)$ 为探索系数，提议动作集 $o^{(t)}$ 通过从 $\pi^{(t)}$ 中独立有放回采样 $K$ 个动作生成。

### 关键公式：后悔界

**InstUtil Rank 全信息后悔界**：当效用向量的总变化满足次线性假设 $P^{(T)} := \sum_{t=2}^{T} \| \pmb{u}^{(t)} - \pmb{u}^{(t-1)} \| \le \mathcal{O}(T^q), \; q < 1$ 时，Algorithm 2 的后悔界为：

$$
R^{(T), \mathrm{external}} \le R^{(T), \mathrm{external}}\left( \mathrm{Alg}, \left( \widetilde{\pmb{u}}^{(t)} \right)_{t=1}^{T} \right) + \mathcal{O}\left( \left( P^{(T)} \right)^{\frac{1}{3}} T^{\frac{2}{3}} \left( \log\left( \frac{T}{\delta} \right) \right)^{\frac{1}{3}} \right)
$$

第一项是基础算法在估计效用序列上的后悔，第二项是效用估计误差的累积惩罚。当 $P^{(T)}$ 次线性时，整体后悔为次线性。

**AvgUtil Rank 全信息后悔界**：由于时间平均效用的变化量天然有界（每轮变化不超过 $1/t$），当基础算法（如 FTRL）具有稳定性时，Algorithm 3 的后悔界独立于 $P^{(T)}$：

$$
R^{(T), \mathrm{external}} \le R^{(T), \mathrm{external}}\left( \mathrm{Alg}, \left( \pmb{u}^{(t)} \right)_{t=1}^{T} \right) + \mathcal{O}\left( L T^{\frac{5}{3}} \log\left( \frac{T}{\delta} \right) \right)
$$

其中 $L$ 为基础算法的稳定性参数。这表明在 AvgUtil Rank 且 $\tau$ 为常数时，次线性变化假设可以被移除。

### 算法流程

Algorithm 2（InstUtil Rank）和 Algorithm 3（AvgUtil Rank）的整体流程分别由图 Figure 10 和 Figure 11 给出，其核心流水线为：

**动作提议** → **排序观测** → **效用估计 (Algorithm 1)** → **在线学习黑盒 (FTRL 等)** → **探索混合（仅强盗设定）** → **策略更新**

两种算法在全信息和强盗设定下的差异主要在于：提议动作集的生成方式（全信息下提议全部动作，强盗下采样 $K$ 个）以及是否引入探索混合。



## 实验与关键发现

### 主实验结果

本文在两类任务上验证了所提算法的有效性：在线学习（后悔最小化）与均衡计算（可剥削度最小化）。

**在线学习任务（HH‑RLHF 数据集）**  
在 LLM 路由任务上，Algorithm 3（AvgUtil Rank，强盗反馈）的平均后悔随时间持续下降并快速逼近事后最佳固定 LLM 模型的表现（Figure 2）。该结果表明，即使仅能观察到排序反馈且无法获取精确效用值，算法仍能有效识别高质量动作。

**均衡计算任务（合成博弈）**  
在多种设置下，Algorithm 2 和 Algorithm 3 的可剥削度均随轮次增加而下降，表明策略序列收敛至近似粗相关均衡（CCE，理想可剥削度为 0）。该趋势在全信息反馈（Figure 3, Figure 7）与强盗反馈（Figure 8, Figure 9）下均成立。


![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_lg6H2oJPky/figures/004_Figure_3.jpg]]
*Figure 3: The exploitability for the full-information feedback setting under both InstUtil Rank and AvgUtil Rank. Performance is evaluated across different temperatures τ and cumulative utility variations P ^ { ( T ) } = T ^ { q } . Each parameter combination is tested 10 times with different random seeds*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_lg6H2oJPky/figures/008_Figure_7.jpg]]
*Figure 7: The exploitability for the full-information setting under both InstUtil Rank and AvgUtil Rank feedback in the game-play setting. The performance is tested under different temperatures τ . Each parameter combination is tested 10 times with different random seeds*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_lg6H2oJPky/figures/009_Figure_8.jpg]]
*Figure 8: The exploitability for the bandit feedback setting under InstUtil Rank feedback in the game-play setting. Performance is evaluated across different temperatures τ and numbers of proposed actions K. Each parameter combination is tested 10 times with different random seeds*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_lg6H2oJPky/figures/010_Figure_9.jpg]]
*Figure 9: The exploitability for the bandit feedback setting under AvgUtil Rank feedback in the game-play setting. Performance is evaluated across different temperatures τ and numbers of proposed actions K. Each parameter combination is tested 10 times with different random seeds*

### 消融分析

实验系统性地考察了两个关键超参数的影响：

- **温度参数 τ**：控制 Plackett‑Luce 排名模型的随机性。τ 越小，排序越确定性地反映效用差异；τ 越大，排序噪声越强。在 InstUtil Rank 全信息设置下，较小 τ 通常导致更快的收敛，但极端小的 τ 可能加剧估计方差（Figure 3, Figure 4）。在 AvgUtil Rank 下，τ 的影响相对温和，算法在较宽范围内保持稳定（Figure 5, Figure 6）。


![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_lg6H2oJPky/figures/005_Figure_4.jpg]]
*Figure 4: The regret for bandit feedback setting under InstUtil Rank feedback in the online learning setting. The performance is evaluated across different temperatures τ , cumulative utility variations P ^ { ( T ) } = T ^ { q } , and numbers of proposed actions K. Each parameter combination is tested 10 times with different random seeds*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_lg6H2oJPky/figures/006_Figure_5.jpg]]
*Figure 5: The regret for bandit feedback setting under AvgUtil Rank feedback in the online learning setting. The performance is evaluated across different temperatures τ , cumulative utility variations P ^ { ( T ) } = T ^ { q } , and numbers of proposed actions K. Each parameter combination is tested 10 times with different random seeds*

- **提议动作数 K**：在强盗设置中，K 决定了每轮观察到的动作数量。增大 K 提供更丰富的比较信息，从而加速效用估计的收敛，但也会增加每轮的决策成本。实验显示，后悔和可剥削度均随 K 增大而单调改善，且边际收益递减（Figure 4, Figure 5, Figure 8, Figure 9）。

### 失败模式与局限性

1. **InstUtil Rank 的线性缺口**：理论分析已证明，在 InstUtil Rank 反馈下，任何算法均无法实现次线性期望后悔（线性下界）。实验中间接验证了这一点：当效用向量变化剧烈（$P^{(T)}$ 增长接近线性，即 $q$ 接近 1）时，InstUtil Rank 下的后悔和可剥削度下降显著放缓，甚至趋于停滞（Figure 3, Figure 4）。

2. **小 τ 下的不稳定性**：当 τ 极小（如 τ = 0.1）时，排序近乎确定性地反映微小效用差异，导致效用估计对个别比较的依赖过强，方差增大。这在 InstUtil Rank 强盗设置下尤为明显，表现为后悔曲线波动加剧（Figure 4）。

3. **AvgUtil Rank 强盗反馈的理论间隙**：当前工作尚未闭合 AvgUtil Rank 在强盗反馈下的下界与上界间隙。当 τ 为常数时，是否仍存在线性下界，或能否在不依赖次线性变化假设（Assumption 4.2）的情况下实现次线性后悔，仍为开放问题。实验仅提供了经验证据，尚缺乏理论保证。

4. **真实场景验证缺失**：所有实验均基于合成对抗环境或 LLM 路由仿真（HH‑RLHF 数据集）。在真实排序反馈场景（如骑乘共享匹配、在线约会）中的表现尚未评估，效用估计质量和探索策略是否需要调整仍有待研究。

### 补充图表

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_lg6H2oJPky/figures/011_Figure_10.jpg]]
*Figure 10: The diagram of Algorithm 2 with InstUtil Rank under full-information feedback (top) and bandit feedback (bottom). ⃝+ represents the addition of (1 − γ) times the output the Alg and γ times a uniform distribution over A*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_lg6H2oJPky/figures/012_Figure_11.jpg]]
*Figure 11: The diagram of Algorithm 3 with AvgUtil Rank under full-information feedback (top) and bandit feedback (bottom). represents copying the estimated utility vector for t times. ⃝+ represents the addition of ( 1 - $\gamma$ ) times the output the Alg and γ times a uniform distribution over A*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_lg6H2oJPky/figures/002_Table_1.jpg]]
*Table 1: Summary of our contributions, including the negative results (top) and the positive results (bottom). The bottom table lists the minimal assumptions required to achieve sublinear regret in each setting (✓indicates that no additional assumptions are needed). Here, $\tau$ > 0 denotes the temperature parameter of the ranking model in (PL)*




## 定位与知识库关联

### 1. 反馈范式的根本性位移

本文的核心贡献在于将在线学习与均衡计算的反馈机制从“数值效用”位移至“排序反馈”。传统在线学习框架——无论是全信息反馈（如 Follow-The-Regularized-Leader, FTRL）还是强盗反馈——均假设学习者能够直接观测到精确的效用数值。然而，在人机协同（如推荐系统、在线约会匹配）或隐私受限的真实场景中，用户往往只能提供对候选集的偏好排序，而无法给出精确的效用值。本文正是针对这一“数值反馈不可得”的瓶颈，系统性地建立了基于 Plackett-Luce 模型的排序反馈理论框架。

这一位移并非简单的反馈降级，而是引入了全新的信息结构：排序反馈将效用信息编码为成对比较的概率关系，学习者必须通过逆推理从排序置换中恢复底层效用。这种“从序到值”的推断过程构成了本文方法区别于所有传统在线学习工作的根本分界线。

### 2. 方法谱系中的定位

本文的方法设计遵循“效用估计 + 黑盒在线学习”的模块化架构，这一思路在排序反馈文献中具有自然性，但其理论分析的完备性和对多种反馈类型的统一处理构成了独特贡献。

**效用估计模块（Algorithm 1）** 的核心技术路线是将完整排序拆解为成对比较，利用逻辑函数的单调可逆性从比较频率中恢复效用估计。具体而言，对于滑动窗口内的 $m$ 轮排序，算法统计每一对动作 $(i, j)$ 的胜率，并通过逆 sigmoid 变换 $\tau \ln(\hat{p} / (1 - \hat{p}))$ 得到效用差的估计。这一估计的质量由两项控制：统计误差项（随窗口大小 $m$ 增大而衰减）和效用漂移项（由窗口内效用向量的总变化决定）。该估计器为后续的后悔分析提供了桥梁——将排序反馈问题转化为带噪声的数值反馈问题。

**在线学习黑盒模块** 则直接复用标准全信息在线学习算法（如 FTRL、投影梯度下降、乘法权重更新），将估计的效用向量作为输入，产生更新后的策略。这种“即插即用”的设计使得本文方法能够继承现有在线学习算法的后悔保证，同时将分析的重点聚焦于效用估计误差的传播与控制。

在强盗反馈设定下，算法进一步引入**探索混合**机制：将黑盒算法的输出与均匀分布按 $(1-\gamma) : \gamma$ 的比例混合，确保每个动作被提出的概率下界为正，从而保证效用估计的覆盖性。

### 3. 两种排序反馈的机制差异与理论后果

本文区分了两种排序反馈类型，这一区分揭示了排序反馈问题中的关键因果旋钮：

- **InstUtil Rank**：排序基于当前时刻的瞬时效用 $\pmb{u}^{(t)}$。在此设定下，本文证明了一个**线性缺口定理**——任何算法都无法实现次线性期望后悔。这一不可能性结果源于瞬时效用的快速变化使得排序信息无法有效累积。为突破这一障碍，本文引入了**次线性效用变化假设**（Assumption 4.2）：$\sum_{t=2}^T \|\pmb{u}^{(t)} - \pmb{u}^{(t-1)}\| \le \mathcal{O}(T^q), q<1$。在此假设下，Algorithm 2 在全信息设定下实现 $\mathcal{O}((P^{(T)})^{1/3} T^{2/3})$ 的后悔界，在强盗设定下实现 $\mathcal{O}((P^{(T)})^{1/5} T^{4/5})$ 的后悔界。

- **AvgUtil Rank**：排序基于截至当前时刻的时间平均效用 $\pmb{u}_{\text{avg}}^{(t)} = \frac{1}{t}\sum_{s=1}^t \pmb{u}^{(s)}$。此设定具有一个关键性质：平均效用向量的逐时刻变化自然衰减（$\|\pmb{u}_{\text{avg}}^{(t)} - \pmb{u}_{\text{avg}}^{(t-1)}\|_\infty \le \mathcal{O}(1/t)$），与累积效用变化无关。这一性质使得在全信息设定下，当温度参数 $\tau$ 为常数时，次线性变化假设可以被**完全移除**——Algorithm 3 配合稳定的更新规则（如 FTRL）即可实现次线性后悔。然而，在强盗反馈下，AvgUtil Rank 的理论图景尚未闭合：$\tau$ 为常数时是否存在线性下界，或能否在不依赖 Assumption 4.2 的情况下实现次线性后悔，仍是开放问题。

### 4. 适用边界与关键假设

本文方法的适用性受以下关键条件约束：

1. **Plackett-Luce 模型假设**：排序生成必须服从 PL 模型，其温度参数 $\tau$ 控制排序的随机性程度。当 $\tau$ 过小（排序过于确定）时，AvgUtil Rank 下同样存在线性下界，因为高度确定的排序会掩盖效用差异的细微变化。

2. **次线性效用变化假设**：对于 InstUtil Rank，这是实现次线性后悔的必要条件（在 PL 模型下）。若效用向量变化过于剧烈（$q \ge 1$），则算法无法有效追踪。

3. **全信息 vs. 强盗反馈**：在全信息设定下，所有动作均被提议并排序，效用估计的覆盖性自然满足；在强盗设定下，仅从当前策略中采样 $K$ 个动作，需通过探索混合保证覆盖。

4. **稳定更新规则**：AvgUtil Rank 要求底层在线学习算法具有稳定性（如 FTRL），以容忍平均效用估计中的累积扰动。

### 5. 局限与开放问题

**理论间隙**：AvgUtil Rank 在强盗反馈下的下界与上界之间存在间隙。具体而言，当 $\tau$ 为常数时，目前既未证明线性下界的存在，也未给出不依赖 Assumption 4.2 的次线性后悔算法。这一间隙的闭合是排序反馈在线学习理论的核心开放问题。

**实证验证不足**：当前实验主要基于合成对抗环境和 LLM 路由任务（HH-RLHF 数据集）的初步仿真，尚未在真实排序反馈场景（如骑乘共享匹配、在线约会推荐）中部署验证。效用估计模块在高维、稀疏的真实排序数据上的鲁棒性，以及探索策略在非平稳偏好下的适应性，均有待进一步检验。

**非平稳环境扩展**：本文理论建立在对抗性效用序列上，但 Assumption 4.2 限制了变化的剧烈程度。算法能否推广到更一般的非平稳环境（如偏好分布随时间漂移），并仍保持有意义的后悔保证，是一个值得探索的方向。



## 原文 PDF

![[paperPDFs/ICLR_2026/Online_Learning_and_Equilibrium_Computation_with_Ranking_Feedback.pdf]]
