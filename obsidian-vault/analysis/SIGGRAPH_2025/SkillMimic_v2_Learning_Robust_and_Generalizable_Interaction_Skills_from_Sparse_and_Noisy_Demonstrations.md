---
title: "SkillMimic-V2: Learning Robust and Generalizable Interaction Skills from Sparse and Noisy Demonstrations"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2025
pdf_ref: paperPDFs/SIGGRAPH_2025/SkillMimic_v2_Learning_Robust_and_Generalizable_Interaction_Skills_from_Sparse_and_Noisy_Demonstrations.pdf
project_link: https://ingrid789.github.io/SkillMimicV2/
code_link: null
aliases:
- SV
- SkillMimic-V2
tags:
- SIGGRAPH_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过拼接轨迹图（STG）和状态转移场（STF）进行数据增强，发现潜在轨迹以扩大状态覆盖；采用自适应轨迹采样（ATS）动态调整难度权重，解决链断裂问题；并利用预训练的历史编码器（HE）学习记忆依赖行为，使策略能泛化到未见的技能过渡和恢复状态。
primary_logic: 尽管演示数据有限且噪声显著，在物理世界中存在无数可行轨迹可以自然桥接不同技能或从演示邻域涌现，形成连续的技能变化和转移空间。通过显式构造这些轨迹并指导RL训练，可以将噪声演示转化为覆盖丰富的训练信号。
claims:
- 在BallPlay-M上，完整方法（SM+Ours）平均技能成功率（SR）达到96.9%，比基线SkillMimic的53.3%提升43.6个百分点；技能转移成功率（TSR）从15.1%提升至93.8%。
- 在ParaHome上，完整方法平均成功率从基线的5.5%提升至100%，ε邻域成功率从0.1%提升至40.1%。
- 消融实验表明，STF是最关键的组件：移除STF后，SR从96.94%骤降至68.67%，TSR从93.80%降至66.54%。
- 方法使技能转移成为可能，例如从Dribble-Left到Dribble-Right的转移成功率从基线的1.4%提升至100%，而这些转移在参考数据中不存在。
---

# SkillMimic-V2: Learning Robust and Generalizable Interaction Skills from Sparse and Noisy Demonstrations

> [!tip] 核心洞察
> 尽管演示数据有限且噪声显著，在物理世界中存在无数可行轨迹可以自然桥接不同技能或从演示邻域涌现，形成连续的技能变化和转移空间。通过显式构造这些轨迹并指导RL训练，可以将噪声演示转化为覆盖丰富的训练信号。

| 字段 | 内容 |
|------|------|
| 中文题名 | SkillMimic-V2：从稀疏和噪声演示中学习鲁棒且可泛化的交互技能 |
| 英文题名 | SkillMimic-V2: Learning Robust and Generalizable Interaction Skills from Sparse and Noisy Demonstrations |
| 会议/期刊 | SIGGRAPH 2025 |
| Links | [Project](https://ingrid789.github.io/SkillMimicV2/) · [paper](https://doi.org/10.1145/3721238.3730640) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | SkillMimic-V2 |
| Dataset | BallPlay-M, ParaHome |

> [!tip] 效果简介
> - BallPlay-M (5 skills) 上，Average Success Rate (SR) 96.9% vs 53.3% (+43.6%)。
> - BallPlay-M 上，Average Skill Transition Success Rate (TSR) 93.8% vs 15.1% (+78.7%)；Average ε-Neighborhood Success Rate (εNSR) 49.3% vs 18.3% (+31.0%)。
> - ParaHome (7 skills) 上，Average Success Rate (SR) 100% vs 5.5% (+94.5%)。

## 概要

物理仿真角色从人类演示中学习交互技能时，面临一个根本瓶颈：**稀疏且带噪声的演示数据无法覆盖完整的技能变化空间**。现有RLID（Reinforcement Learning from Interaction Demonstrations）方法在参考轨迹存在物理不可达状态转移时，会遭遇“链断裂”（chain break）问题——策略在错误状态处累积偏差，导致后续动作完全失效。这一困境在上篮（Layup）、投篮（Shot）等需要记忆依赖行为的复杂技能中尤为突出，基线方法SkillMimic的成功率仅为53.3%。

**SkillMimic-V2** 的核心洞察在于：尽管演示有限，物理世界中存在无数可行轨迹，它们可以自然地桥接不同技能，或从演示邻域中涌现，形成一个连续的技能变化与转移空间。通过显式构造这些潜在轨迹并引导强化学习训练，噪声演示得以转化为覆盖丰富的训练信号。

基于这一思想，方法引入四个关键组件：**拼接轨迹图（STG）** 发现不同技能演示间的潜在转移；**状态转移场（STF）** 为演示邻域内的任意状态建立唯一的目标连接，并通过掩码状态桥接远距离转移；**自适应轨迹采样（ATS）** 根据样本难度动态调整权重，解决链断裂问题；**预训练历史编码器（HE）** 将过去状态压缩为紧凑嵌入，赋予策略记忆依赖行为的能力。

在BallPlay-M（5项篮球技能）上，完整方法达到**96.9%的平均技能成功率**，较基线提升43.6个百分点；技能转移成功率从15.1%跃升至**93.8%**。在ParaHome（7项日常交互技能）上，成功率从5.5%提升至**100%**。消融实验表明，STF是最关键的组件——移除后成功率骤降至68.67%。方法还展现出对数据噪声的强鲁棒性：在物体位置叠加σ=30mm噪声时仍保持84.9%以上的成功率，而基线完全失效。

### 问题背景：物理仿真中交互技能的模仿学习

让物理仿真角色从人类演示中学习复杂的交互技能，是计算机图形学与机器人学中长期存在的挑战。与纯运动技能（如行走、奔跑）不同，交互技能涉及角色与动态物体之间的精细协调——例如运球时手与球的持续接触、倒茶时水壶与茶杯的相对位姿约束、或抓取书本时手指与物体的稳定接触。这类技能的成功执行不仅要求角色自身姿态的准确性，还要求物体状态的精确控制，因此对演示数据的质量和覆盖范围提出了更高要求。

近年来，基于强化学习的交互演示模仿方法（Reinforcement Learning from Interaction Demonstrations, RLID）取得了显著进展。其中，**SkillMimic**（Wang et al., 2024c）将交互模仿统一为单个技能的学习问题，通过乘积形式的统一奖励函数同时优化身体姿态、物体状态、相对关系和接触目标，在多个交互任务上展示了领先的性能。然而，这些方法的成功高度依赖于演示数据的质量与覆盖范围。

### 核心瓶颈：稀疏噪声演示下的“链断裂”问题

在实际应用中，获取高质量、全覆盖的交互演示数据极为困难。人类演示者通常只能提供**稀疏且带噪声的短轨迹片段**——例如，仅演示一次短暂的运球动作，或仅展示抓取书本的单一姿态。这些演示数据存在两个根本性缺陷：

1. **状态覆盖不足**：稀疏的演示片段无法覆盖完整的技能变化空间。以篮球技能为例，演示数据可能只包含独立的投篮（Shot）和运球（Dribble）片段，而从未展示从运球过渡到投篮的连续过程。对于需要记忆依赖的复杂技能（如上篮 Layup），演示数据往往在关键阶段中断，导致参考轨迹不完整。

2. **参考轨迹中的错误状态**：由于演示采集过程中的噪声或物理不可行性，参考轨迹可能包含无法在物理仿真中精确复现的状态转移。当策略试图严格跟踪这些错误状态时，会产生“**链断裂**”（chain-breaking）问题——一个状态的跟踪失败会连锁导致后续所有状态的跟踪失败，最终使整个技能执行崩溃。

这些问题在现有方法中尤为突出。如Figure 2所示，当参考轨迹包含物理不可达的状态转移时，完美的轨迹重建变得不可能；学习目标应转变为在参考轨迹的ε邻域内寻找一组既物理可行又满足重建阈值的理想轨迹。然而，现有RLID方法缺乏有效机制来探索和利用这一邻域空间。

### 现有方法的局限

以SkillMimic为代表的现有RLID方法在面对稀疏噪声演示时暴露出三个关键短板：

- **缺乏数据增强能力**：方法仅使用原始参考轨迹进行训练，无法从有限的演示中推断出更丰富的可行轨迹。当演示数据未覆盖技能间的过渡状态时，策略无法学习技能转移能力——例如，从左手运球（Dribble-Left）切换到右手运球（Dribble-Right）的成功率仅15.1%（Table 1, SM基线）。

- **缺乏自适应难度调节**：均匀采样策略对所有轨迹片段一视同仁，导致困难样本（如链断裂的起始状态）训练不足，而简单样本过度训练。这使得上篮（Layup）等记忆依赖技能的基线成功率低至0.0%（Table 1）。

- **缺乏历史信息建模**：策略网络仅基于当前状态做出决策，无法捕捉需要长程记忆的技能特征。对于需要记住早期动作序列才能完成后续步骤的技能（如投篮前的运球准备），这一缺陷尤为致命。

### 核心洞察与本文动机

尽管演示数据有限且噪声显著，本文提出一个关键洞察：**在物理世界中，存在无数可行的潜在轨迹，它们可以自然地桥接不同技能之间的空白，或从演示数据的邻域状态中涌现，形成一个连续的技能变化与转移空间**。如Figure 3所示，给定两个简短的技能演示（如Shot和Dribble），在它们之间存在无限条未被捕获但物理有效的轨迹（图中问号所示），这些轨迹既可以实现技能间的平滑过渡，也可以从邻域状态中衍生出新的执行变体。

基于这一洞察，本文提出**SkillMimic-V2**框架，核心动机是：**通过显式构造这些潜在轨迹并将其转化为RL训练信号，将稀疏噪声演示转化为覆盖丰富的训练数据，从而学习鲁棒且可泛化的交互技能**。具体而言，框架通过拼接轨迹图（STG）发现技能间的潜在转移、通过状态转移场（STF）为邻域内的任意状态建立唯一的定向连接、通过自适应轨迹采样（ATS）动态调节训练难度以解决链断裂问题，并通过预训练的历史编码器（HE）赋予策略记忆依赖行为的能力。

这一方法在BallPlay-M（5项篮球技能）和ParaHome（7项日常交互技能）两个基准上进行了验证：完整方法在BallPlay-M上达到96.9%的平均技能成功率（基线53.3%），技能转移成功率从15.1%提升至93.8%；在ParaHome上平均成功率从5.5%提升至100%。这些结果表明，通过数据增强和结构化探索，从稀疏噪声演示中学习鲁棒交互技能是可行的。

## 核心方法与创新机理

SkillMimic-V2 的核心创新在于将**稀疏且带噪声的交互演示**转化为覆盖丰富的训练信号，使物理仿真机器人能够学习鲁棒且可泛化的交互技能。相对于基线方法 SkillMimic（Wang et al., 2024c），本工作在四个关键维度上进行了系统性改进，每个改进都针对现有 RLID 方法在稀疏演示场景下的根本性缺陷。

### 从邻域探索到结构化状态转移场

基线方法（SkillMimic、DeepMimic）的状态初始化策略是从参考轨迹状态中随机采样，这一做法在演示数据稀疏时导致状态覆盖严重不足。SkillMimic-V2 的核心洞察在于：**尽管演示有限，参考轨迹的 ε 邻域内存在无数物理可行但未被捕获的轨迹**，它们可以自然桥接不同技能或从演示邻域涌现（Figure 3）。

为利用这一洞察，方法首先在参考状态的 ε 邻域内均匀采样新状态，随后通过**状态转移场（State Transition Field, STF）**为每个采样状态建立唯一的定向连接：基于运动学相似度度量 $S_k$ 寻找最近的参考状态作为目标，并在两者之间插入适当数量的掩码状态以桥接远距离转移（Sec. 4.3）。这一设计将无结构的邻域随机探索转化为显式的、物理可行的转移路径，使策略能够在训练中接触到远超原始演示的状态空间。

消融实验（Table 3）证实 STF 是**最关键的组件**：移除 STF 后，平均技能成功率（SR）从 96.94% 骤降至 68.67%，技能转移成功率（TSR）从 93.80% 降至 66.54%。值得注意的是，STF 显式结构化邻域探索在全部指标上显著超越基于熵的探索方法（IAE），后者仅将 SR 提升至 53.31%（Table 7），说明无结构的探索增强无法有效解决稀疏演示下的覆盖问题。

### 拼接轨迹图：发现潜在的技能间转移

当演示数据仅包含孤立的技能片段时，技能之间的转移路径完全缺失。SkillMimic-V2 提出**拼接轨迹图（Stitched Trajectory Graph, STG）**来解决这一问题（Sec. 4.4）：通过将不同技能的参考轨迹进行拼接，显式构造出潜在的技能间转移轨迹，并用掩码表示拼接点处的缺失数据。STG 替代原始参考轨迹用于后续的 STF 数据增强和 RLID 训练。

这一设计使技能转移成为可能。在 BallPlay-M 上，从 Dribble-Left 到 Dribble-Right 的转移（DL-DR）在参考数据中完全不存在，基线 SkillMimic 的 TSR 仅为 1.4%，而 SkillMimic-V2 达到 100%（Figure 4, Table 1）。整体上，平均 TSR 从基线的 15.1% 提升至 93.8%，验证了 STG 在发现潜在转移方面的有效性。

### 自适应轨迹采样：解决“链断裂”问题

稀疏演示中的参考轨迹往往包含物理不可达的状态转移，导致“链断裂”（chain break）问题——策略在轨迹早期失败后无法恢复，后续状态永远无法被访问。SkillMimic-V2 的**自适应轨迹采样（Adaptive Trajectory Sampling, ATS）**策略（Sec. 4.5）通过动态调整采样权重来解决这一问题：

$$ \dot{p}_i = \frac{e^{-\lambda_s \bar{r}_i}}{\sum_{j=0}^{T-1} e^{-\lambda_s \bar{r}_j}}, \quad \bar{r}_i = \frac{1}{T-i}\sum_{t=i}^{T-1} r_t $$

其中 $\bar{r}_i$ 是从时间步 $i$ 到轨迹末端 $T-1$ 的平均奖励，$\lambda_s$ 控制难度侧重。低奖励（高难度）的轨迹片段获得更高的采样概率，形成动态课程学习。消融实验（Table 3）表明，移除 ATS 会显著降低 Layup 和 Shot 等记忆依赖技能的成功率，这些技能正是“链断裂”问题最严重的场景。

### 历史编码器：赋予策略记忆依赖能力

上篮（Layup）和投篮（Shot）等技能具有强记忆依赖性——当前动作的正确性取决于过去状态的序列模式，而非仅当前状态。基线方法 SkillMimic 无显式历史编码，无法学习此类行为。SkillMimic-V2 引入**历史编码器（History Encoder, HE）**（Sec. 4.6）：通过行为克隆预训练，将过去 $k$ 个状态压缩为低维嵌入（维度仅为 3），冻结后作为策略的额外输入：

$$ \mathbf{h}_t = \theta(\mathbf{s}_{t-k}, ..., \mathbf{s}_{t-1}), \quad \mathbf{a}_t \sim \pi(\cdot | \mathbf{c}, \mathbf{s}_t, \mathbf{h}_t) $$

关键设计在于使用**预训练的紧凑嵌入**而非直接拼接历史状态。Table 7 显示，直接拼接历史状态（SM+HS）导致 PPO 训练完全崩溃（SR 为 0.0%），而预训练嵌入则稳定收敛。这是因为高维历史状态拼接会引入大量噪声维度，破坏策略梯度估计的稳定性。

### 创新之间的协同关系

上述四个组件并非孤立工作，而是形成递进式协同：STG 在技能层面发现潜在转移，STF 在状态层面建立结构化连接，ATS 在采样层面聚焦困难样本，HE 在表征层面赋予策略时序推理能力。完整的 SkillMimic-V2（SM+STG+STF+ATS+HE）在 BallPlay-M 上达到 96.94% SR 和 93.80% TSR，在 ParaHome 上达到 100% SR——而基线 SkillMimic 在相同任务上分别为 53.3% 和 5.5%（Table 1, Table 2）。

在数据噪声鲁棒性方面，当物体位置叠加 $\sigma=30$mm 噪声时，SkillMimic-V2 仍保持 84.9% 以上的 SR，而基线在相同条件下完全失效（Table 4），进一步验证了结构化数据增强策略对噪声的固有容忍度。

SkillMimic-V2 的整体框架围绕一个核心洞察构建：**尽管演示数据有限且噪声显著，物理世界中存在无数可行轨迹，可以自然桥接不同技能或从演示邻域涌现，形成连续的技能变化和转移空间**。通过显式构造这些轨迹并指导强化学习训练，可以将噪声演示转化为覆盖丰富的训练信号。

框架的输入是**稀疏的技能演示片段**（例如，仅包含投篮和运球的短轨迹），输出是一个**统一的技能策略** $\pi(\cdot | \mathbf{c}, \mathbf{s}_t, \mathbf{h}_t)$，能够执行多种交互技能并在它们之间鲁棒切换。整个 pipeline 由五个关键模块串联构成：

### 1. 拼接轨迹图（STG）

STG 负责**发现演示技能之间的潜在转移**。给定多个技能的稀疏演示轨迹，STG 将它们拼接成一张有向图，显式构造出原始数据中不存在的跨技能转移路径（例如从运球左到运球右）。这些拼接轨迹扩充了训练数据的覆盖范围，为后续的状态转移场和策略训练提供更丰富的参考信号（Sec. 4.4）。

### 2. 状态转移场（STF）

STF 是框架**最关键的组件**（消融实验中移除 STF 后成功率从 96.94% 骤降至 68.67%，Table 3）。它在 STG 的基础上进一步扩展，为演示邻域内的**任意采样状态**建立唯一的定向连接。具体而言：

- 在参考状态的 $\varepsilon$-邻域内均匀采样新状态 $\mathbf{s}_{\text{new}}$；
- 通过运动学相似度度量 $S_k$ 找到与之最匹配的参考状态 $\hat{\mathbf{s}}_j$；
- 在 $\mathbf{s}_{\text{new}}$ 和 $\hat{\mathbf{s}}_j$ 之间插入 $N$ 个掩码状态 $\mathbf{s}_{\emptyset}$，桥接远距离转移，确保物理可行性（Sec. 4.3, Appendix B.4）。

这一机制将稀疏的参考轨迹扩展为覆盖邻域的**连续转移场**，使策略能够从任意邻域状态恢复并完成技能。

### 3. 自适应轨迹采样（ATS）

ATS 解决**“链断裂”问题**——参考轨迹中的错误状态会导致后续状态连锁失败。ATS 基于滑动平均奖励 $\bar{r}_i$ 为每个轨迹片段分配采样概率：

$$\dot{p}_i = \frac{e^{-\lambda_s \bar{r}_i}}{\sum_{j=0}^{T-1} e^{-\lambda_s \bar{r}_j}}, \quad \bar{r}_i = \frac{1}{T-i}\sum_{t=i}^{T-1} r_t$$

难度越高的片段（平均奖励越低），被采样的概率越大，形成**动态课程学习**，使策略优先攻克困难状态转移（Sec. 4.5, Eq. 8）。

### 4. 历史编码器（HE）

许多交互技能（如上篮、投篮）具有**记忆依赖性**——当前最优动作依赖于过去的状态序列。HE 通过行为克隆预训练，将过去 $k$ 个状态压缩为低维嵌入 $\mathbf{h}_t = \theta(\mathbf{s}_{t-k}, ..., \mathbf{s}_{t-1})$，冻结后作为策略的额外输入。消融实验表明，直接拼接历史状态会导致 PPO 收敛崩溃（SR 为 0.0%），而预训练的小型嵌入（维度仅为 3）有效解决了这一问题（Sec. 4.6, Table 7）。

### 5. RLID 策略训练

以上模块生成的数据增强轨迹和采样策略最终输入 RLID 框架进行 PPO 训练。RLID 将交互模仿建模为学习底层的机器人-物体状态转移 $s_{t+1} \sim P(\cdot | \phi, s_t, f)$，并使用统一交互模仿奖励：

$$r_t = S(s_{t+1}, \hat{s}_{t+1}) = r_t^b \cdot r_t^o \cdot r_t^{\text{rel}} \cdot r_t^{\text{cg}}$$

该奖励由身体、物体、相对和接触四项子奖励的乘积构成，衡量生成状态与参考状态的相似度（Sec. 3, Eq. 1-2）。

### 数据流总览

稀疏演示片段 → **STG** 拼接跨技能转移路径 → **STF** 在邻域内建立状态级定向连接 → **ATS** 按难度加权采样轨迹片段 → **HE** 提供历史嵌入 → **RLID (PPO)** 训练统一技能策略。整个流程在单块 NVIDIA RTX 4090 GPU 上运行，使用 2048 个并行环境，训练约需 24 小时（>1.3B 样本）。

### 3.1 问题形式化与RLID基础

SkillMimic-V2建立在**从交互演示中强化学习（RLID）**框架之上。RLID将技能学习建模为机器人-物体状态转移的学习过程。策略被参数化为高斯分布以支持随机探索，其均值由神经网络 $\phi(s_t)$ 生成，方差固定：

$$s_{t+1} \sim P(\cdot | \phi, s_t, f)$$

其中 $f$ 为物理模拟器。统一的交互模仿奖励定义为四项归一化子奖励的乘积：

$$r_t = S(s_{t+1}, \hat{s}_{t+1}) = r_t^b \cdot r_t^o \cdot r_t^{rel} \cdot r_t^{cg}$$

四项子奖励分别衡量生成状态与参考状态在**身体姿态**、**物体位姿**、**相对位置**和**接触图**四个维度的相似度。该乘积形式确保任一维度失败都会显著压低整体奖励，从而提供细粒度的交互引导。

### 3.2 状态转移场（STF）

STF是方法最关键的组件（消融实验证实移除STF后SR从96.94%骤降至68.67%）。其核心思想是：在参考状态的 $\varepsilon$ 邻域内，为任意采样状态建立唯一的定向转移路径。

**邻域初始化与目标匹配**：从参考状态的 $\varepsilon$ 邻域内均匀采样新状态 $s_{\text{new}}$，随后在参考轨迹中寻找运动学最相似的状态作为目标：

$$\hat{s}_j = \arg \max_{s \in \mathcal{A}} S(s_{\text{new}}, s)$$

运动学相似度 $S_k(s_A, s_B) = r^b \cdot r^o \cdot r^{rel}$ 排除接触信息，仅基于身体、物体和相对位姿计算，确保匹配的是空间构型而非接触状态。

**掩码状态桥接**：当采样状态与目标状态距离较远时，直接转移在物理上不可行。STF在两者之间插入 $N$ 个掩码状态，构建平滑过渡轨迹：

$$\{ s_{\text{new}}, \underbrace{s_{\emptyset}, ..., s_{\emptyset}}_{N}, \hat{s}_j, ..., \hat{s}_T \}$$

掩码状态数量 $N$ 由相似度 $\beta$ 自适应决定：$N = \min(-\lfloor \log_{10}(\beta) \rfloor, N_{\max})$。相似度越低（距离越远），插入的掩码状态越多，保证转移的物理可行性。掩码状态在训练中不计入模仿损失，仅作为探索的中间跳板。

### 3.3 拼接轨迹图（STG）

STG解决稀疏演示中技能间转移数据缺失的问题。给定多个技能的短演示片段，STG将不同技能的轨迹端点进行拼接，发现潜在的技能转移路径。例如，将Dribble-Left的末端状态与Dribble-Right的起始状态连接，构造出原始数据中不存在的跨技能转移轨迹。拼接后的轨迹图 $\mathcal{A}^\dagger$ 替代原始参考轨迹，作为后续STF增强和RLID训练的基础。

STG的局限性在于无法处理涉及不同刚体对象的任务（如ParaHome中水壶与椅子属于不同物体），限制了跨物体技能转移的能力。

### 3.4 自适应轨迹采样（ATS）

ATS解决“链断裂”问题：参考轨迹中某一步的错误状态会导致后续所有步骤的模仿奖励崩溃，使策略难以从失败中恢复。ATS根据样本难度动态调整轨迹片段的采样权重：

$$\dot{p}_i = \frac{e^{-\lambda_s \bar{r}_i}}{\sum_{j=0}^{T-1} e^{-\lambda_s \bar{r}_j}}, \quad \bar{r}_i = \frac{1}{T-i}\sum_{t=i}^{T-1} r_t$$

其中 $\bar{r}_i$ 是从时间步 $i$ 到轨迹末尾的平均奖励，$\lambda_s$ 控制难度权重。平均奖励越低（样本越难），采样概率越高。这使得策略在训练中更多地暴露于困难状态转移，从而学会从失败中恢复。ATS对Layup和Shot等记忆依赖技能尤为关键。

### 3.5 历史编码器（HE）

记忆依赖技能（如上篮、投篮）要求策略“记住”过去的运动状态以规划未来动作。直接拼接历史状态会导致PPO在高维输入下收敛崩溃（SM+HS的SR为0.0%）。HE通过行为克隆预训练一个紧凑编码器，将过去 $k$ 个状态压缩为低维嵌入：

$$\mathbf{h}_t = \theta(\mathbf{s}_{t-k}, ..., \mathbf{s}_{t-1})$$

策略条件于技能标签、当前状态和历史嵌入：

$$\mathbf{a}_t \sim \pi(\cdot | \mathbf{c}, \mathbf{s}_t, \mathbf{h}_t)$$

编码器预训练后冻结，嵌入维度仅为3，在提供记忆能力的同时避免维度爆炸。消融实验表明HE对Layup等技能的成功率提升至关重要。

## 实验与关键发现

### 核心实验设计

实验在两个具有挑战性的交互技能基准上评估 SkillMimic-V2：**BallPlay-M**（5项篮球技能：Dribble-Left、Dribble-Right、Pickup、Layup、Shot）和 **ParaHome**（7项日常交互技能：倒茶、放茶壶、推椅子等）。对比基线包括当前最先进的 RLID 方法 **SkillMimic**（SM，Wang et al. 2024c）和经典运动模仿方法 **DeepMimic**（DM，Peng et al. 2018），两者均在统一交互奖励框架下训练以确保公平性。评估指标包括：

- **成功率（Success Rate, SR）**：从参考状态初始化时成功完成技能的比例。
- **技能转移成功率（Skill Transition Success Rate, TSR）**：从其他技能的末端状态初始化时，成功执行目标技能的比例。
- **ε邻域成功率（ε-Neighborhood Success Rate, εNSR）**：从参考状态 ε 邻域内随机采样初始化时的成功率，衡量泛化鲁棒性。
- **归一化奖励（Normalized Reward, NR）**：平均每帧奖励，反映模仿质量。

所有结果均在 10,000 次随机试验上平均，训练使用单块 NVIDIA RTX 4090 GPU、2048 并行环境，训练时长约 24 小时（>1.3B 样本）。

### 主结果：BallPlay-M 与 ParaHome

**BallPlay-M**（Table 1）：完整方法（SM+Ours）平均技能成功率达到 **96.9%**，较基线 SkillMimic 的 53.3% 提升 **43.6 个百分点**；技能转移成功率（TSR）从 15.1% 跃升至 **93.8%**（+78.7 pp）；ε 邻域成功率（εNSR）从 18.3% 提升至 **49.3%**（+31.0 pp）。尤其值得注意的是，对于 Layup 和 Shot 等长时序、记忆依赖技能，基线几乎完全失败（SR 分别为 11.4% 和 0.0%），而本方法分别达到 **98.9%** 和 **100%**。技能转移方面，从 Dribble-Left 到 Dribble-Right 的转移成功率从基线的 1.4% 提升至 **100%**（Figure 4, Figure 7），这些转移路径在参考数据中完全不存在。

**ParaHome**（Table 2）：完整方法平均 SR 从基线的 5.5% 提升至 **100%**（+94.5 pp），εNSR 从 0.1% 提升至 **40.1%**（+40.0 pp）。基线在倒茶、放茶壶等技能上几乎完全失效，而本方法实现了鲁棒的技能执行与泛化。

### 消融实验：组件贡献分析

Table 3 在 BallPlay-M 上系统消融了各组件（以 SM+ε-NSI 为基础，即 SkillMimic + ε 邻域状态初始化）：

![[assets/figures/papers/paper_list_l1806_SkillMimic_v2_Learning_Robust_and_Generalizable_Interaction_Skills_from/figures/008_Table_3.jpg]]
*Table 3: Ablation study of key components on BallPlay-M*

- **完整方法**（SM+STG+STF+ATS+HE）：SR 96.94%，TSR 93.80%，εNSR 49.26%。
- **移除 STF**（-STF）：SR 骤降至 **68.67%**（-28.27 pp），TSR 降至 **66.54%**（-27.26 pp），εNSR 降至 38.50%。STF 是**最关键组件**，其显式构建邻域状态到参考轨迹的定向连接，为策略提供了结构化的探索引导，远优于无引导的邻域随机初始化。
- **移除 HE**（-HE）：SR 降至 86.84%，TSR 降至 79.08%。历史编码器对 Layup 和 Shot 等记忆依赖技能尤为关键：移除 HE 后，Layup SR 从 98.9% 降至 68.4%，Shot SR 从 100% 降至 69.6%。
- **移除 ATS**（-ATS）：SR 降至 90.66%，TSR 降至 83.88%。ATS 通过动态提升困难样本的采样权重，解决了“链断裂”问题，对长时序技能影响显著。
- **移除 STG**（-STG）：SR 降至 89.34%，TSR 降至 84.08%。STG 通过拼接不同技能轨迹发现潜在转移，是实现技能间平滑过渡的基础。

### 进一步对比与消融

**Table 7** 提供了更多对照实验：
- 直接将历史状态拼接为策略输入（SM+HS）导致 PPO 训练崩溃（SR 0.0%），验证了预训练历史编码器（HE）将高维历史压缩为低维嵌入的必要性。
- 基于熵的探索方法（SM+IAE）仅将 SR 提升至 53.31%，远低于 STF 的 68.67%，表明 STF 的结构化邻域探索远优于无结构的熵最大化探索（Figure 8 进一步展示了 vanilla PPO 中调节探索率的有限效果）。

![[assets/figures/papers/paper_list_l1806_SkillMimic_v2_Learning_Robust_and_Generalizable_Interaction_Skills_from/figures/015_Figure_8.jpg]]
*Figure 8: Increasing and annealing the exploration rate in vanilla PPO*

**Table 6** 在纯运动技能（Locomotion）上的实验表明，本方法的数据增强策略同样有效，但提升幅度小于交互技能场景，这与方法主要针对交互技能中物体状态转移的设计目标一致。

### 鲁棒性与数据效率

**数据噪声鲁棒性**（Table 4）：在物体位置叠加不同程度高斯噪声的测试中，当噪声标准差 σ=30mm 时，本方法仍保持 **84.9%** 以上的 SR，而基线 SkillMimic 在相同条件下完全失效。这表明 STF 和 ATS 的组合有效缓解了参考数据中的噪声干扰。

**数据效率**（Table 5）：在 Ball Pickup 技能上，仅使用 **1 条**演示轨迹时，本方法 SR 达到 58.8%（基线 0.0%）；使用 3 条时达到 100%。方法能在极少演示下学习可行技能，体现了数据增强策略的有效性。

### 失败模式与局限

1. **跨物体技能转移受限**：STG 组件无法处理涉及不同刚体对象的任务（如 ParaHome 中水壶与椅子），限制了跨物体技能拼接的能力。
2. **极度损坏演示**：当演示数据严重缺失或损坏时，框架性能可能下降，可能需要引入大规模交互先验（如条件跟踪策略）来弥补。
3. **训练计算开销**：单技能训练在单 GPU 上需超过 24 小时（>1.3B 样本），训练时间较长。
4. **历史编码器依赖演示质量**：HE 的预训练依赖于演示数据的自监督学习，对原始演示质量仍有一定要求。

### 关键图表结论摘要

- **Figure 6**：训练曲线显示，本方法在 SR、TSR、εNSR 和 NR 四项指标上均显著优于基线，且收敛更稳定。
- **Figure 7**：技能转移矩阵显示，本方法在任意篮球技能间的转移成功率均接近或达到 100%，而基线在多数转移对上几乎为零。
- **Figure 4/5**：定性结果显示，本方法能执行超出参考数据长度的持续运球、实现参考数据中不存在的左右运球切换，以及鲁棒的倒茶和推椅子序列。

![[assets/figures/papers/paper_list_l1806_SkillMimic_v2_Learning_Robust_and_Generalizable_Interaction_Skills_from/figures/009_Figure_7.jpg]]
*Figure 7: Comparison of skill transition success rate (%) between five basketball skills. Our method demonstrates robust performance in achieving high success rates for transitions between arbitrary skills*

![[assets/figures/papers/paper_list_l1806_SkillMimic_v2_Learning_Robust_and_Generalizable_Interaction_Skills_from/figures/010_Figure_6.jpg]]
*Figure 6: Performance comparisons of the proposed approach against baselines across four key metrics*

![[assets/figures/papers/paper_list_l1806_SkillMimic_v2_Learning_Robust_and_Generalizable_Interaction_Skills_from/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison on BallPlay-M. Blue trajectories in (a,b) indicate executions beyond the reference Layup data length. In*

![[assets/figures/papers/paper_list_l1806_SkillMimic_v2_Learning_Robust_and_Generalizable_Interaction_Skills_from/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparison on BallPlay-M. The neighborhood range ?? for ??NSR test is consistent with training settings*

## 定位与知识库关联

### 1 问题定位：RLID范式的瓶颈

SkillMimic-V2 建立在 **Reinforcement Learning from Interaction Demonstrations (RLID)** 范式之上。RLID 将交互技能学习建模为学习底层机器人-物体状态转移的过程：策略被参数化为高斯分布，均值由神经网络 $\phi(s_t)$ 生成，下一状态取决于策略、当前状态和物理模拟器：

$$s_{t+1} \sim P(\cdot | \phi, s_t, f)$$

训练信号来自统一交互模仿奖励，由身体、物体、相对和接触四项归一化子奖励的乘积构成：

$$r_t = S(s_{t+1}, \hat{s}_{t+1}) = r_t^b \cdot r_t^o \cdot r_t^{rel} \cdot r_t^{cg}$$

在此框架下，现有RLID方法面临一个核心瓶颈：**当交互演示数据稀疏且带噪声时，演示无法覆盖完整的技能变化空间，参考轨迹中的错误状态会导致连锁失败——即“链断裂”（chain break）问题**。这在依赖记忆的复杂技能（如上篮、投篮）上尤为致命。

### 2 基线方法对比

#### 2.1 SkillMimic（Wang et al., 2024c）

SkillMimic 是当前最先进的RLID方法。其核心策略是：
- **状态初始化**：从参考轨迹状态中随机初始化
- **采样策略**：轨迹片段均匀采样
- **数据增强**：仅使用原始参考轨迹
- **历史信息**：无显式历史编码

在 BallPlay-M 上，SkillMimic 的平均技能成功率（SR）仅为53.3%，技能转移成功率（TSR）仅为15.1%（Table 1）。在 ParaHome 上，SR 更是低至5.5%（Table 2）。这表明，即使在 ε-邻域状态初始化（ε-NSI）的增强下，SkillMimic 仍无法有效利用稀疏演示中的信息来泛化到未见状态。

#### 2.2 DeepMimic（Peng et al., 2018）

DeepMimic 是经典的运动模仿学习方法，被适配到交互任务中。其策略与 SkillMimic 类似，但在交互模仿上的表现更弱。在 BallPlay-M 上，即使增强 ε-NSI，其平均 SR 仅为19.7%，TSR 为0.0%（Table 1）。这印证了运动模仿方法在交互场景中的根本局限：交互需要更细粒度的物体-机器人关系引导，而运动模仿的奖励结构难以捕捉这种耦合。

### 3 SkillMimic-V2 的改进槽位

SkillMimic-V2 在四个关键槽位上对基线进行了系统性改进：

| 槽位 | 基线值（SkillMimic） | 改进方案 | 核心机制 |
|------|---------------------|---------|---------|
| 状态初始化策略 | 从参考轨迹状态随机初始化 | ε-邻域均匀采样 + STF定向连接 | 通过状态转移场为邻域内每个状态建立唯一的目标状态和转移路径，插入掩码状态桥接远距离转移 |
| 采样策略 | 轨迹片段均匀采样 | 自适应轨迹采样（ATS） | 基于滑动平均奖励计算采样概率 $\dot{p}_i = \frac{e^{-\lambda_s \bar{r}_i}}{\sum_{j} e^{-\lambda_s \bar{r}_j}}$，难样本权重更高 |
| 多技能数据增强 | 仅使用原始参考轨迹 | 拼接轨迹图（STG） | 将不同技能的轨迹拼接以发现潜在转移，用掩码表示缺失数据 |
| 历史信息编码 | 无显式历史编码 | 预训练历史编码器（HE） | 将过去 $k$ 个状态压缩为低维嵌入 $\mathbf{h}_t = \theta(\mathbf{s}_{t-k}, ..., \mathbf{s}_{t-1})$，冻结后作为策略额外输入 |

这些改进槽位之间存在因果依赖关系：STG 扩展了可用的轨迹空间，STF 在此基础上为邻域状态建立结构化连接，ATS 自适应地聚焦于困难转移，HE 则赋予策略处理记忆依赖行为的能力。消融实验（Table 3）表明，**STF 是最关键的组件**：移除 STF 后，SR 从96.94%骤降至68.67%，TSR 从93.80%降至66.54%。

### 4 核心洞察：从噪声演示到覆盖丰富的训练信号

SkillMimic-V2 的核心洞察在于：**尽管演示数据有限且噪声显著，物理世界中存在无数可行轨迹可以自然桥接不同技能或从演示邻域涌现，形成连续的技能变化和转移空间**。通过显式构造这些轨迹并指导RL训练，可以将噪声演示转化为覆盖丰富的训练信号。

这一洞察在方法上体现为三个递进的构造步骤：
1. **STG**：通过拼接不同技能演示构建潜在转移轨迹，发现技能间的可行桥接
2. **STF**：将 STG 扩展为状态转移场，为邻域内任意状态建立唯一的定向连接，通过插入掩码状态保证物理可行转移
3. **ATS + RLID**：在构造的轨迹空间上进行自适应难度加权的强化学习训练

### 5 适用边界与局限

#### 5.1 已知局限

1. **跨物体技能转移受限**：STG 组件无法处理涉及不同刚体对象的任务（如 ParaHome 中水壶与椅子），限制了跨物体技能转移的能力。这是 STG 基于轨迹拼接的本质局限——拼接要求物体身份一致。

2. **对演示质量的依赖**：当演示数据极度损坏或缺失严重时，框架性能可能下降。历史编码器的预训练依赖于演示数据的自监督学习，对原始演示质量仍有一定要求。

3. **训练计算开销**：所有技能训练在单块 NVIDIA RTX 4090 GPU 上需要超过24小时（>1.3B 样本），使用2048个并行环境。这限制了在更大规模技能库上的快速迭代。

#### 5.2 适用场景

该方法在以下条件下表现最优：
- 演示数据稀疏但包含关键技能片段
- 技能之间存在物理上可行的转移路径
- 任务具有记忆依赖特性（需要历史状态信息）
- 物体类型在技能间保持一致

### 6 开放问题

1. **GAIL 在交互模仿中的适配**：如何在交互模仿中成功应用 GAIL？交互需要更细粒度的引导，而 GAN 奖励通常较为粗糙，这可能是现有方法未采用对抗式模仿学习的原因。

2. **严重损坏演示的处理**：当演示严重损坏或缺失时，可能需要结合大规模交互先验，例如以目标对象状态为条件的跟踪策略，来弥补数据缺陷。

3. **真实机器人数据的适配**：在实时动态变化或高噪声的真实机器人数据中，数据增强和转移场构建规则需要如何调整？当前方法依赖物理模拟器的精确状态访问，这在真实场景中难以保证。

4. **拼接轨迹的质量提升**：是否可以通过更智能的掩码策略或图结构学习进一步提高拼接轨迹的质量？当前掩码状态数量由相似度启发式决定 $N = \min(-\lfloor \log_{10}(\beta) \rfloor, N_{max})$，可能存在更优的自适应方案。

## 原文 PDF

![[paperPDFs/SIGGRAPH_2025/SkillMimic_v2_Learning_Robust_and_Generalizable_Interaction_Skills_from_Sparse_and_Noisy_Demonstrations.pdf]]
