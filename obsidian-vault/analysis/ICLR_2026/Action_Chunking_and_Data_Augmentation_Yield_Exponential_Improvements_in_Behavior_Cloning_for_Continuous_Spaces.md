---
title: "Action Chunking and Data Augmentation Yield Exponential Improvements in Behavior Cloning for Continuous Spaces"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Action_Chunking_and_Data_Augmentation_Yield_Exponential_Improvements_in_Behavior_Cloning_for_Continuous_Spaces.pdf
project_link: null
code_link: null
aliases:
- ACNIDC
- ACDAYEIBCCS
tags:
- ICLR_2026
- topic/optimization_theory_probabilistic
- topic/optimization_theory_probabilistic/reinforcement_learning_and_planning
core_operator: "核心干预措施是动作分块（预测并执行开环动作序列）与探索性数据收集（在专家动作执行时注入噪声），二者通过控制论稳定性机制规避复合误差。"
primary_logic: "控制论中的增量输入-状态稳定性（EISS）是上述干预有效性的根本原因：动作分块通过开环稳定动力学诱导闭环稳定性，噪声注入则提供了遏制复合误差所需的局部探索方向，而无需迭代式专家交互。"
claims:
- "动作分块可以复合误差指数级增长的问题，且不需要修改专家数据。"
- "在HalfCheetah环境中，足够大的白噪声注入带来显著性能提升，效果与更先进的迭代方法相当。"
- "在确定性、完全可观测的机器人操作任务（robomimic tool_hang）中，执行稍长的动作块即可显著提升成功率。"
- "在缺乏开环稳定性的MuJoCo环境中，朴素的动作分块会导致性能灾难性下降，而噪声注入则提供了可靠的局部探索。"
---

# Action Chunking and Data Augmentation Yield Exponential Improvements in Behavior Cloning for Continuous Spaces

> [!tip] 核心洞察
> 控制论中的增量输入-状态稳定性（EISS）是上述干预有效性的根本原因：动作分块通过开环稳定动力学诱导闭环稳定性，噪声注入则提供了遏制复合误差所需的局部探索方向，而无需迭代式专家交互。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 动作分块与数据增强在连续空间行为克隆中带来指数级提升 |
| 英文题名 | Action Chunking and Data Augmentation Yield Exponential Improvements in Behavior Cloning for Continuous Spaces |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jiWXDvw1Lf) |
| Topic | #topic/optimization_theory_probabilistic #topic/optimization_theory_probabilistic/reinforcement_learning_and_planning |
| Method | 动作分块与探索性噪声注入（Action-Chunking & Noise-Injected Data Collection） |
| Dataset | Synthetic EISS dynamics, HalfCheetah-v5, Humanoid-v5, robomimic tool_hang (全状态观测) |

> [!tip] 效果简介
> - Synthetic EISS dynamics 上，复合误差缓解 为 动作分块（ℓ>1）策略，对比 ℓ=1（仅反馈控制），变化 指数级改善（将指数增长转化为多项式增长）。
> - HalfCheetah-v5 上，累计奖励 为 噪声注入（σ_u=0.5或1.0），对比 Vanilla BC，变化 性能大幅提升，与DAgger/DART相当。
> - Humanoid-v5 上，累计奖励 为 朴素噪声注入（σ_u=0.25），对比 Vanilla BC / DAgger / DART，变化 噪声注入提供可靠的局部探索，性能优于或接近迭代方法。

## 概要

连续状态-动作空间中的行为克隆面临一个根本瓶颈：策略在训练分布上的微小回归误差，在闭环执行时会被环境动力学反复放大，形成**复合误差**——其随任务时长呈指数级增长，导致学到的策略在实际部署中性能急剧下降。本文从控制论稳定性角度出发，揭示并系统性地缓解了这一现象。

**核心结论**：通过两项简单、无需迭代式专家交互的实践——**动作分块**（预测并开环执行一个动作序列）和**探索性噪声注入**（在专家动作执行时注入噪声，但保留清洁动作标签）——即可将复合误差从指数灾难转化为多项式增长，甚至在开环稳定条件下给出与时长无关的有限界。其根本原因在于动力学系统的**指数增量输入-状态稳定性（EISS）**：动作分块利用开环稳定特性诱导出闭环稳定，噪声注入则覆盖可激励的误差方向，提供可靠的局部探索，而无需执行迭代式的策略 rollout 或专家在线标注。

**方法定位**：相比仅模仿未修改专家数据的原始行为克隆（Vanilla BC），以及需要多轮在线专家交互的 DAgger、DART 等方法，本文方案通过改变**策略参数化**（从单步动作预测到长度为 $\ell$ 的动作块预测）和**数据分布**（从纯专家轨迹到专家轨迹与噪声注入轨迹的混合分布），在不增加交互成本的前提下，以控制论稳定性保证显著提升了模仿学习的闭环性能。

**主要结果**：

- 在合成 EISS 动力学上，动作分块完全抑制了复合误差的指数增长，将其压缩为常数级比例（Theorem 1、Figure 1 左）。
- 在 MuJoCo 的 HalfCheetah‑v5 与 Humanoid‑v5 任务中，足够强度的白噪声注入使行为克隆性能大幅提升，达到或超越 DAgger、DART 等迭代方法的水平（Figure 1 中、右）。
- 在确定性、完全可观测的 robomimic tool_hang 操作任务中，仅执行稍长的动作块即可显著提升成功率；噪声注入在该稳定设定下同样起效（Figure 2）。
- 消融实验表明：记录清洁动作标签是噪声注入有效的关键，使用噪声标签反而导致性能崩溃；动作分块若无开环稳定性支撑则会引发灾难性退化，验证了理论条件的必要性（Figure 3）。

综上，本文以控制论视角为连续控制中的行为克隆提供了兼具理论深度与实用价值的方法框架，并为稳定性条件、噪声尺度和混合比例的选择提出了进一步研究的问题。

在连续状态-动作空间的模仿学习中，行为克隆（Behavior Cloning, BC）面临一个核心瓶颈：**复合误差（compounding errors）**。当学习到的策略在闭环执行时，每一步微小预测偏差会通过系统动力学不断累积，导致策略分布逐步偏离专家演示分布。这种分布偏移与误差累积形成恶性循环，使轨迹误差 $J_{\text{TRAJ},T}$ 随任务时长 $T$ 呈指数级增长 [Equation (2.3)]，远超过在专家分布上测得的演示误差 $J_{\text{DEMO},T}$。该现象解释了为什么标准 BC 在看似拟合良好的情况下，闭环执行性能却急剧退化。

现有缓解复合误差的主流方法依赖**迭代式专家交互**：DAgger 在每一轮收集专家纠正数据并更新策略，DART 则在收集阶段注入噪声后请求专家重新标注。这些方法虽有一定效果，但要求专家持续参与互动标注，成本高昂。此外，如图 1（右侧 Humanoid-v5）所示，在学得策略初始性能极差的设置下，迭代方法自身的 rollout 质量低下或噪声协方差塑造过于激进，反而可能表现次优。

本文的核心动机源于一个关键观察：**控制论中的增量输入-状态稳定性（Exponentially Incrementally Input-to-State Stability, EISS）** [Definition 2.1] 是理解和对抗复合误差的根本性分析工具。EISS 刻画了动力学系统对有界输入扰动产生有限状态偏差、且该偏差随时间收缩的性质。在此框架下，研究者识别出两种非迭代式的干预手段：

- **动作分块（Action-Chunking）** [Practice 1]：预测并执行长度为 $\ell$ 的开环动作序列。在开环稳定动力学下，充分长的动作块可将轨迹误差与演示误差的比值约束为与 $T$ 无关的常数 [Theorem 1/3]，从指数灾难降为多项式依赖。
- **探索性噪声注入（Noise-Injected Data Collection）** [Practice 2]：在数据采集阶段向专家动作叠加球形噪声，但记录清洁动作作为标签。此举使数据分布覆盖更可激励的误差方向 [Proposition 4.3]，在非开环稳定环境下将误差界由指数改善为 $O(T)$ 多项式依赖 [Theorem 2/4]。

这两种实践的吸引力在于**无需专家迭代交互**：动作分块仅改变策略参数化方式，而噪声注入仅需在采集阶段注入噪声后一次性标注——专家无需观察学得策略的 rollout 并反复纠正。如图 1（中左）所示，在合成 EISS 动力学上，频繁反馈可引发指数复合误差，而动作分块有效缓解；在 HalfCheetah-v5 上，足够大的白噪声注入带来与迭代方法相当的性能提升，同时在 Humanoid-v5 上提供更可靠的局部探索。在 robomimic tool_hang 全状态观测任务中（图 2），仅将执行块长从 $\ell=1$ 延长到 $\ell \geq 4$ 即可显著提升成功率，验证了动作分块在确定性、完全可观测设置下的有效性，排除了部分可观测性或生成式架构为主要机制的替代假说。

总之，本文从控制论稳定性视角出发，系统分析复合误差的成因，并提出动作分块与噪声注入作为理论支撑、实验验证的非迭代式解决方案。

## 核心方法与创新机理

本文针对连续状态-动作行为克隆中的**复合误差（compounding error）**瓶颈，提出了两个直接改变基本假设的 **changed slots**，而非简单的模块叠加。这两项干预从控制论稳定性机制出发，从根本上改变了误差随任务时长的传播方式。

### 关键机制 Slot 变化

**1. 策略参数化形式：从单步预测到动作分块**

- **基准**: 传统行为克隆策略输出单个动作（Markovian policy），每一步执行后接收新状态反馈，形成闭环控制。
- **创新**: 将策略输出改为长度为 $\ell$ 的动作序列（chunked policy），在一个块内部采用开环方式执行，不依赖即时状态反馈。该策略在生成动作块时仍可条件于当前状态，但块内动作以开环方式推进。

  这一改动的核心控制论洞察在于：若环境动力学具备指数增量输入-状态稳定性（EISS, Definition 2.1），即轨迹对之间具有收缩性质，那么**充分长的动作块能将闭环轨迹误差与演示误差的比例从指数依赖衰减为常数量级**，从而消除复合误差的指数增长。理论保证见 Theorem 1/Theorem 3，其中轨迹误差界形式为：

  $$
  \mathbf{J}_{\mathrm{TRAJ},T}(\tilde{\pi}) \leq O_{\star}(1) \, \mathbf{J}_{\mathrm{DEMO},T}(\tilde{\pi}; \mathbb{P}_{\pi^{\star}})
  $$

  该界证明**开环稳定动力学能够诱导闭环稳定性**，且所需块长仅与系统参数呈对数关系，对统计复杂度的影响可忽略。

> **实证验证**: 在确定性、完全可观测的 robomimic `tool_hang` 任务中，将评价块长 $\ell$ 从 1 增至 4 即可带来成功率的**显著跃升**（Figure 2），而预测视界的额外作用次要，从而排除了"部分可观测性"或"生成式架构"为机制的替代假说。

**注意**：动作分块不等同于多步预测。Theorem 1 明确指出，若仅进行多步预测但仍以滚动时域方式执行（$\ell=1$），则无法规避复合误差，**开环执行才是关键**。

---

**2. 数据收集分布：从纯专家轨迹到探索性噪声注入**

- **基准**: 训练数据仅来自专家策略的马尔可夫链轨迹 $\mathbb{P}_{\pi^{\star}}$。
- **创新**: 在数据收集阶段，对专家动作**注入球形噪声**（$\sigma_{\mathbf{u}}$ 参数控制噪声幅度），但**记录的标签仍为清洁的专家动作**。训练分布采用混合形式：
  
  $$
  \mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}},\alpha} \triangleq \alpha \mathbb{P}_{\pi^{\star}} + (1-\alpha) \mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}}}
  $$
  
  其中 $\alpha \in [0,1]$ 为清洁轨迹的混合比例。

  这一改动的核心洞察在于：当环境动力学**不具有开环稳定性**时，纯粹的动作分块会导致性能灾难性崩溃（Figure 3 右）。噪声注入通过在**可激励子空间（excitable subspace）**上提供必要的局部探索数据，使得策略在未见过的误差方向上也能学到恢复行为，从而遏制复合误差。理论分析（Theorem 2/Theorem 4）表明，在光滑但非开环稳定的动力学下，噪声注入将轨迹误差与演示误差的关系**从指数灾难转为多项式依赖**（与 $T$ 线性相关，而非指数）：
  
  $$
  \mathbf{J}_{\mathrm{TRAJ},T}(\hat{\pi}) \lesssim O_{\star}(T) \, \sigma_{\mathbf{u}}^{-2} \, \mathbf{J}_{\mathrm{DEMO},T}(\hat{\pi}; \mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}},0.5})
  $$

  该机制的关键性质是**噪声注入主要沿更容易激励的方向发生**（Proposition 4.3 / Figure 7），仅需对可激励子空间进行监督，而无需强化学习意义上对全空间的覆盖或控制论意义上的持续激励条件。

> **实证验证**: 在 HalfCheetah-v5 环境（Figure 1 中图）中，$\sigma_{\mathbf{u}} \in \{0.5, 1.0\}$ 的噪声注入使性能**与 DAgger、DART 等迭代式强基线相当**，而无需任何迭代式专家交互。在 Humanoid-v5 环境（Figure 1 右）中，朴素噪声注入的性能甚至**优于** DAgger/DART，因为后两者的劣质滚动策略或激进的噪声协方差塑造可能适得其反。

---

### 消融分析的核心发现

从实验消融（Figure 3）中可以提炼出几项**直接支撑创新有效性的因果证据**：

- **清洁标签是关键瓶颈**：若在噪声注入时记录噪声化的动作标签（而非清洁标签），性能将发生灾难性崩溃。这说明该方法并非简单的数据覆盖增强，而是通过清洁标签保留了"从噪声中恢复"的回归目标。
- **混合比例 $\alpha$ 的边际效应递减**：只要有足够数量（数量级无需极大）的噪声注入轨迹，性能对清洁轨迹比例不敏感，这降低了该实践的工程调参难度。
- **动作分块在无开环稳定性时失效**：在 MuJoCo 的 HalfCheetah 等非开环稳定环境中，单纯增加块长无法提升性能，反而导致灾难性下降，这从负面验证了 Theorem 1 中"假定开环稳定性"的必要条件。

### 与迭代式方法的关系

本文提出的噪声注入可被视作 David Laskey 等人 DART 算法的一个**去迭代化版本**（如文中所述）：DART 需要在多轮次中收集数据并不断请求专家标签，而本文的 Practice 2 仅需**一轮**扰动式数据收集，在统计效率上具有明显优势，同时避免了迭代方法中因劣质中间策略滚动而导致的数据分布退化问题。

---

### 边界与开放问题

上述创新虽有效，但存在理论上的**未闭合环节**，需手动评估对具体任务的风险：

- Theorem 2 的界仍含有与 $T$ 线性的因子，**并非完全与任务时长无关**（horizon‑free），在极长时间上下文中仍可能累积误差（尽管比指数因子已有质变）。
- 理论分析依赖**局部线性化、光滑性以及专家闭环绕路具有 EISS 的假设**，这些条件在高度非线性或不稳定的实际系统中可能不完全满足。
- 当前理论假定了**专家策略为确定性**，对随机专家策略的扩展尚未纳入界定。
- 块长 $\ell$ 与统计复杂性之间的精确关系、以及噪声尺度 $\sigma_{\mathbf{u}}$ 与混合比例 $\alpha$ 的鲁棒选择配方，仍待进一步工作予以刻画（这些属于本文列出的开放问题）。

![[assets/figures/papers/iclr26_0006_jiWXDvw1Lf_Action_Chunking_and_Data_Augmentation_Yield_Expo/figures/011_Figure_4.jpg]]
*Figure 4: A comparison of open-loop control, where the policy generates actions without accessing the system state, and closed-loop control, where the policy's generated actions condition on the system state. While actionchunks are generated closed-loop, the actions within a chunk are executed "open-loop."*

![[assets/figures/papers/iclr26_0006_jiWXDvw1Lf_Action_Chunking_and_Data_Augmentation_Yield_Expo/figures/012_Figure_5.jpg]]
*Figure 5: A visualization of EISS (Definition 2.1), which guarantees pairwise contraction of trajectories. Figure 6: We visualize the stabilizing effect of using multiple action chunks (shown in different colors) when evaluating a "chunked" policy (with corresponding trajectory shown in black). As the open-loop dynamics on each chunk is stabilizing, this ensures closed-loop-EISS of the resulting learned policy over multiple chunks*

该方法针对连续状态‑动作空间中行为克隆的复合误差瓶颈，引入两个非迭代式的干预模块——**动作分块策略**与**探索性噪声注入**。整体流程在数据采集阶段与执行阶段分别作用，形成一条无需修改专家交互方式的轻量级改进管线。

**输入与输出**。系统接受专家演示数据集 $S_n=\{(\mathbf{x}_{1:T}^{(i)},\mathbf{u}_{1:T}^{(i)})\}_{i=1}^n$ 作为训练输入，其中 $\mathbf{x}_t$ 为状态，$\mathbf{u}_t$ 为专家动作。训练目标是学习一个策略 $\hat{\pi}$，在闭环执行时最小化轨迹误差 $\mathbf{J}_{\mathrm{TRAJ},T}$。

**两个核心干预模块**：

1.  **动作块生成器**。在策略参数化层面，将标准马尔可夫策略（单步预测 $\mathbf{u}_t=\pi(\mathbf{x}_t)$）替换为**块策略**（chunked policy），以当前状态 $\mathbf{x}$ 为输入，输出一个长度为 $\ell$ 的开环动作序列：
    $$\mathsf{chunk}[\widetilde{\pi}](\mathbf{x}) = \big( \pi(\mathbf{x}), \pi(g^{\pi}(\mathbf{x})), \pi((g^{\pi})^{2}(\mathbf{x})), \dots, \pi((g^{\pi})^{\ell-1}(\mathbf{x})) \big)$$
    其中 $g^{\pi}(\mathbf{x})$ 表示在开环动力学下执行一步动作后的后继状态。在**执行时**，块内所有动作均以开环方式依次下达，而不接受中间状态的反馈（Figure 4）。其作用机制是：在满足指数增量输入‑状态稳定性（EISS）的开环动力学下，充分长的动作块使闭环策略继承稳定性，将轨迹误差从指数增长压缩为与 $T$ 无关的常数级（Theorem 1）。

2.  **探索性噪声注入**。在**数据采集阶段**，执行专家动作时叠加球形噪声 $\sigma_{\mathbf{u}} \mathbf{z}_t$（$\mathbf{z}_t\sim\mathrm{Uniform}(\mathbb{S}^{d_{\mathbf{u}}})$），同时**保留清洁动作标签**作为监督信号。训练分布为混合形式：
    $$\mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}},\alpha} \triangleq \alpha\,\mathbb{P}_{\pi^{\star}} + (1-\alpha)\,\mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}}}$$
    其中 $\alpha\in[0,1]$ 控制清洁轨迹的比例。噪声注入的关键作用是为策略提供**可激励的局部探索方向**——尤其是可控子空间中的误差分量——使得在无开环稳定性的环境中，轨迹误差由指数灾难降为多项式依赖（Theorem 2）。与迭代交互方法（DAgger、DART）相比，该方法将扰动数据生成前置到首次数据采集阶段，无需多轮专家纠正。

**模块关系**。两个模块在机理上互补：动作分块通过开环稳定动力学诱导闭环稳定性，在稳定系统中独立解决复合误差（Figure 2）；噪声注入则利用局部探索遏制不稳定系统中的发散行为，弥补动作分块在不稳定环境中的失效（Figure 3右侧）。二者可在相同环境中**叠加使用**以发挥协同效果。

值得注意的是，该方法不依赖部分可观测性或生成式架构，即使在确定性、马尔可夫、全状态可观测的设置下依然有效。

本文方法建立在两个互为补充的实践模块之上：**动作分块策略（Practice 1）** 与 **探索性噪声注入数据收集（Practice 2）**。二者通过控制论中的增量输入‑状态稳定性（EISS）机制，分别应对开环稳定与开环不稳定的动力学场景，将行为克隆中原本指数增长（compounding error）的轨迹误差压至常数阶或多项式阶。

### 模块一：动作分块策略（Action‑Chunking）

动作分块策略在每一个闭合控制周期内输出一个长度为 ℓ 的**开环动作序列**，且在块内执行时不从环境中获取新的状态反馈（图4）。其核心公式为该策略的显式定义：

$$
\mathsf{chunk}[\widetilde{\pi}](\mathbf{x}) = \big( \pi(\mathbf{x}),\; \pi(g^{\pi}(\mathbf{x})),\; \pi((g^{\pi})^{2}(\mathbf{x})),\; \dots,\; \pi((g^{\pi})^{\ell-1}(\mathbf{x})) \big)
$$

- $\mathbf{x}$：当前块起始状态。
- $\pi$：基础的马尔可夫策略（状态到动作的单步映射）。
- $g^{\pi}$：专家策略 $\pi^{\star}$ 诱导的闭环动力学映射，即 $g^{\pi}(\mathbf{x}) = f(\mathbf{x}, \pi^{\star}(\mathbf{x}))$，其中 $f$ 为环境状态转移函数。
- $\ell$：分块长度（动作块的步数）。

这一参数化方式将策略类的输出维度从 1 变为 ℓ，但其统计复杂度增加有限，却能在开环稳定动力学下**彻底消除复合误差的指数增长**。Theorem 1（正文 Theorem 3）给出的上界具有形式：

$$
\mathbf{J}_{\mathrm{TRAJ},T}(\tilde{\pi}) \leq O_{\star}(1)\; \mathbf{J}_{\mathrm{DEMO},T}(\tilde{\pi}; \mathbb{P}_{\pi^{\star}})
$$

- $\mathbf{J}_{\mathrm{TRAJ},T}$：学得策略与专家策略在 $T$ 步内的累积轨迹误差（状态‑动作平方误差之和，截断到1）。
- $\mathbf{J}_{\mathrm{DEMO},T}$：在纯粹专家轨迹分布 $\mathbb{P}_{\pi^{\star}}$ 上的演示回归误差。
- $O_{\star}(1)$：与时间 $T$ 无关的系统常数（依赖于 EISS 参数 $C_{\mathrm{ISS}}$, $\rho$ 等）。

该界的意义在于：只要动力学满足**指数增量输入‑状态稳定性**（EISS）——

$$
\| \mathbf{x}_t - \mathbf{x}_t' \| \leq C_{\mathrm{ISS}} \rho^{t-1} \| \mathbf{x}_1 - \mathbf{x}_1' \| + C_{\mathrm{ISS}} \sum_{k=1}^{t-1} \rho^{t-1-k} \| \mathbf{u}_k - \mathbf{u}_k' \|
$$

（其中 $\rho \in (0,1)$ 保证扰动呈指数衰减）——充分长的动作块即可将闭环策略诱导为闭环 EISS，从而将轨迹误差限制为演示误差的固定倍数，不随 $T$ 爆炸。对块长度 $\ell$ 的要求为对数级而非巨大长程预测。

实验上，这一机制在确定性的、全状态可观测的机器人操作任务（robomimic `tool_hang`）中表现显著：一旦执行稍长的块，成功率急剧提升（Figure 2 左），而纯粹的预测视界变化影响甚微，证实开环执行而非多步预测才是消除复合误差的关键。

### 模块二：探索性噪声注入（Noise Injection）

当环境动力学不具有开环稳定性时，单纯的动作分块会因不稳定传播而导致策略崩溃（Figure 3 右），此时必须在**数据收集阶段**注入探索噪声来覆盖策略误差可能激发的方向。具体实践为：

1. **噪声执行，清洁标签**：在专家回放过程中，实际执行的动作是 $\mathbf{u}_t = \pi^{\star}(\mathbf{x}_t) + \sigma_{\mathbf{u}} \mathbf{z}_t$，其中 $\mathbf{z}_t \sim \mathrm{Unif}(\mathbb{S}^{d_{\mathbf{u}}-1})$（$d_{\mathbf{u}}$ 维单位球面上的均匀噪声），但记录给策略学习的标签仍为清洁动作 $\pi^{\star}(\mathbf{x}_t)$。
2. **混合分布训练**：将清洁专家轨迹与噪声注入轨迹按比例 $\alpha$ 混合，构造训练分布

$$
\mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}},\alpha} \triangleq \alpha\, \mathbb{P}_{\pi^{\star}} + (1-\alpha)\, \mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}}}
$$

并在该分布上最小化回归误差 $\mathbf{J}_{\mathrm{DEMO},T}(\hat{\pi}; \mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}},\alpha})$。

理论保证（Theorem 2，正文 Theorem 4）给出以下上界：

$$
\mathbf{J}_{\mathrm{TRAJ},T}(\hat{\pi}) \lesssim O_{\star}(T)\; \sigma_{\mathbf{u}}^{-2}\; \mathbf{J}_{\mathrm{DEMO},T}(\hat{\pi}; \mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}},0.5})
$$

- $\sigma_{\mathbf{u}}$：注入噪声的尺度。
- $O_{\star}(T)$：线性依赖于 $T$ 的量（相比原始指数增长的 $C^T$ 因子是质的改善）。
- $\mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}},0.5}$：等比例混合清洁与噪声轨迹的分布（$\alpha=0.5$）。

该界揭示：在光滑的、非开环稳定的动力学下，通过噪声注入，轨迹误差与噪声增强演示误差之间仅呈多项式关系，且增大噪声尺度 $\sigma_{\mathbf{u}}$ 能进一步压低上界（反比于 $\sigma_{\mathbf{u}}^2$）。其控制论直觉在于，噪声注入主要发生在更加"可激励"的方向（Figure 7），从而使一阶策略误差在可控子空间上变得可被训练损失检测。

实验消融表明，清洁标签至关重要（噪声标签会带来灾难性崩溃），而混合比例 $\alpha$ 在提供足够多的噪声注入轨迹后影响边际递减（Figure 3 左、中）。在 HalfCheetah‑v5 等不满足开环稳定的基准上，以噪声注入训练的行为克隆可达到与迭代式交互方法（DAgger、DART）相当甚至更优的性能，却避免了迭代过程中不良策略回滚的风险（Figure 1 中）；在 Humanoid‑v5 上朴素的噪声注入同样提供了可靠的局部探索，优于部分迭代方法（Figure 1 右）。

## 实验与关键发现

### 主结果：动作分块与噪声注入突破复合误差瓶颈

实验围绕连续控制中行为克隆的**复合误差**瓶颈展开，验证了动作分块（Practice 1）和探索性数据收集中的噪声注入（Practice 2）的独立与协同效果。核心证据来源于典型MuJoCo基准和模拟动力学系统，关键指标为累计奖励（HalfCheetah、Humanoid）与任务成功率（robomimic tool_hang），并与 Vanilla BC、DAgger、DART 等基线与迭代基线对比。

在合成 EISS 动力学上（Figure 1 左），高频反馈导致标准的 Markov 策略引发指数级复合误差增长，而将策略参数化从单个动作预测切换为**长度ℓ>1的动作块**后，该增长被抑制为多项式级别，直接印证了 Theorem 1 的理论界（$\mathbf{J}_{\mathrm{TRAJ},T}(\tilde{\pi}) \leq O_{\star}(1)\,\mathbf{J}_{\mathrm{DEMO},T}(\tilde{\pi}; \mathbb{P}_{\pi^{\star}})$）。在 HalfCheetah-v5 环境（Figure 1 中、Figure 3），引入**足够大的白噪声注入**（$\sigma_{\mathbf{u}} = 0.5$ 或 $1.0$）收集清洁动作标签的数据，使得 Vanilla BC 的性能得到大幅提升，其累计奖励与需要迭代专家交互的 DAgger 和 DART 处于同一水平。类似地，在 Humanoid-v5 上，朴素的噪声注入（$\sigma_{\mathbf{u}}=0.25$）提供了可靠的局部探索方向，效果优于或匹敌迭代方法（Figure 1 右），而后者可能因不良的策略回滚或激进的噪声协方差整形而次优。

![[assets/figures/papers/iclr26_0006_jiWXDvw1Lf_Action_Chunking_and_Data_Augmentation_Yield_Expo/figures/003_Figure_1.jpg]]
*Figure 1: Visualization of the benefits of action-chunking (Practice 1) and noise-injection (Practice 2). Left: even on synthetic globally EISS (Definition 2.1) dynamics f, frequent feedback can cause exponential compounding error, which action-chunking mitigates. Center: HalfCheetah-v5 environment. We see sufficiently large white noise injection yields significant performance improvement, on par with more advanced iterative methods. Right: Humanoid-v5 environment. Iterative methods like DAGGER and DART can be suboptimal due to poor learned policy rollouts or aggressive noise-covariance shaping, while naive noise-injection reliably provides the necessary local exploration; error bars omitted for clar...*

![[assets/figures/papers/iclr26_0006_jiWXDvw1Lf_Action_Chunking_and_Data_Augmentation_Yield_Expo/figures/009_Figure_3.jpg]]
*Figure 3: Features of Practice 2 exhibited on HalfCheetah-v5. Left: we compare collecting clean action labels as in Practice 2, versus the noised ones as in a coverage-based approach. We note $\sigma _ { \mathbf { u } }$ = 1 corresponds to sizable entry-wise input perturbations $\approx$ 0 . 4 on an action space of [ - 1 , 1 ]$^ { 6 }$ . Imitating with noisy labels is therefore catastrophic, yet using clean labels achieves improved performance. Center: Fixing $\sigma _ { \mathbf { u } }$ = 0 . 5 . , we vary the proportion of clean expert trajectories $\alpha \in$ [ 0 , 1 ] The performance difference is marginal past a sufficient number of noised trajectories; see Eq. (4.1). Right: naively action-chunking (Pra...

在确定性、全状态可观测的机器人操作任务 robomimic tool_hang 中（Figure 2），**动作分块的效果极为显著**：评价块长 $\geq 4$ 时成功率出现阶梯式跃升，而预测视界的影响远小于执行块长。这排除了部分可观测或生成式架构为主要机制的替代假说——即使环境是 Markov 且状态完全可观测的，执行开环动作块本身即能够稳定闭环行为。进一步地，在此开环稳定设置下注入噪声（Figure 2 右）也能带来额外增益，显示两种干预可以协同。

![[assets/figures/papers/iclr26_0006_jiWXDvw1Lf_Action_Chunking_and_Data_Augmentation_Yield_Expo/figures/006_Figure_2.jpg]]
*Figure 2: Success rates as a function of evaluated action-chunk lengths on the challenging robomimic "too$l_$hang" environment with full-state observations. Left: Each line corresponds to a model trained for a given prediction horizon on 100 expert trajectories. Each point corresponds to the model evaluating a given chunk length ranging from receding-horizon ( $\ell$ = 1 ) to the full chunk. While prediction horizon has some (transient) effect, evaluating slightly longer chunks improves success drastically. Right: We repeat a similar set-up with 50 expert training trajectories. We see that noise-injection (Practice 2) can also synergize in this open-loop stable setting (see Appendix F), though requires m...*

### 消融：清洁标签、混合比例与环境稳定性的关键角色

围绕噪声注入策略（Practice 2）的消融实验揭示了几个决定成败的实践细节（Figure 3）：

- **标签选择**：若在注入噪声时直接使用**被噪声污染的动作作为训练标签**（覆盖式学习的典型做法），策略将发生灾难性崩溃；而按照 Practice 2 记录清洁专家动作标签时性能稳定提升（Figure 3 左）。这与理论机制一致：噪声的使命是让策略在数据分布中"看到"可激励方向上的误差模式，但回归目标必须保持为专家动作，否则将引入系统性偏差。

- **混合比例 $\alpha$**：将清洁专家轨迹 $\mathbb{P}_{\pi^{\star}}$ 与噪声注入轨迹 $\mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}}}$ 以比例 $\alpha$ 混合时，性能对 $\alpha$ 的变化不敏感，只要存在足够数量的噪声注入轨迹即可（Figure 3 中）。这降低了实际部署时的超参数敏感性。

- **环境开环稳定性的必要性**：当把单纯的动作分块（Practice 1）直接应用到 HalfCheetah-v5 这种**非开环稳定**的环境时，性能出现灾难性下降（Figure 3 右），与 tool_hang 的成功形成尖锐对比。这强有力地证明了理论分析中开环稳定性假设的必要性——若动力学本身在开环下发散，分块策略无法诱导出闭环的增量输入-状态稳定性（EISS），此时必须依赖噪声注入在数据层面提供对可激励子空间的探测（Theorem 2 的界：$\mathbf{J}_{\mathrm{TRAJ},T}(\hat{\pi}) \lesssim O_{\star}(T)\,\sigma_{\mathbf{u}}^{-2}\,\mathbf{J}_{\mathrm{DEMO},T}(\hat{\pi}; \mathbb{P}_{\pi^{\star},\sigma_{\mathbf{u}},\alpha})$，将指数灾难降为多项式依赖）。

### 失败模式与边界条件

上述结果映射出清晰的失败边界：

1. **非开环稳定动力学下的朴素动作分块**：没有噪声注入时，执行块内的动作序列会快速偏离专家轨迹并放大误差，验证了"仅靠算法干预而不改变数据分布"在处理不稳定系统时的无力（Theorem A 的下界）。
2. **噪声标签的覆盖式模仿**：将探索性噪声直接嵌入标签，等价于回归到一个次优的噪声策略，消融证实此举导致奖励崩溃，否定了仅通过扩大状态动作覆盖就足以解决问题的假设。
3. **噪声注入的界并非完全 horizon‑free**：Theorem 2 中保留了 $O_{\star}(T)$ 的线性依赖，这意味着在极长任务时长下误差仍可能累积，但相比于原始 BC 的指数灾难已是质的改善。

### 图表结论精粹

- **Figure 1**：宏观视角——动作分块在合成 EISS 系统上消除指数复合误差；大噪声注入让 HalfCheetah 上的 BC 追平迭代方法；朴素噪声注入在 Humanoid 上稳健胜过迭代方法。
- **Figure 2**：确定性全状态任务中，**较长执行块长（≥4）** 是成功率突增的主因，预测视距影响次要；噪声注入在此也能锦上添花。
- **Figure 3**：实践要害——（左）必须用清洁标签；（中）$\alpha$ 影响微小；（右）开环不稳定时单纯分块致命。

综上，实验证据一致支撑了控制论因果机制：**动作分块通过开环稳定动力学抑制复合误差，噪声注入通过覆盖可激励方向提供必要的局部探索，二者在不依赖迭代专家交互的前提下，将行为克隆的性能从指数灾难提升到稳定可用**。

![[assets/figures/papers/iclr26_0006_jiWXDvw1Lf_Action_Chunking_and_Data_Augmentation_Yield_Expo/figures/013_Figure_7.jpg]]
*Figure 7: The effect of noise injection for controllable versus uncontrollable subspaces. We illustrate the key advantage of Proposition 4.3, namely, that noise injection occurs primarily in more excitable directions. By leveraging this mechanism, we are able to derive better error rates (Suboptimal Proposition 4.2 vs Proposition 4.3)*

## 定位与知识库关联

本文的方法处于模仿学习中行为克隆路线的核心位置，聚焦于连续状态-动作空间下复合误差的缓解。与依赖迭代式专家交互的 DAgger 和 DART 不同，本文仅通过对策略参数化和数据收集分布进行两个关键"槽位"的修改，便在不引入迭代重标注的前提下实现了指数级到多项式级的误差率跃迁。具体而言：

- **相对于 Vanilla BC**：该基线仅模仿未修改的专家马尔可夫链，策略预测单步动作（Markovian policy）。本文指出，这种闭环滚动的频繁反馈是复合误差指数增长的根源（Theorem 1 的直观动机，Figure 1 Left 的合成动力学验证）。相比之下，本文的策略预测长度为 ℓ 的动作块（chunked policy），并在块执行期断开状态反馈，从而借助环境的增量输入-状态稳定性将误差的时域依赖从指数压至常数。
- **相对于 DAgger 与 DART**：这两种迭代方法分别通过收集在线滚动的专家纠正标签或向动作注入噪声并请求专家重标签来构建更强的训练分布。本文的 **Noise-Injection** 可以视作 DART 的"非迭代、萃取版"：在数据采集时，**仅向专家动作添加球形噪声并记录清洁标签**，通过混合分布 ℙ_π⋆,σ_u,α 覆盖可激励误差方向，而无需反复推演低质量策略或风险协方差设计。实验表明，在 HalfCheetah-v5 上，白噪声注入即可达到与 DAgger/DART 相当的性能（Figure 1 center），在非开环稳定的 Humanoid-v5 上甚至优于迭代方法（Figure 1 right），验证了其局部探索的充分性与鲁棒性。

### 适用边界
本文的干预有效性绑定了严格的动力学假设和任务特征：
- **动作分块**的指数收益（Theorem 1）仅在环境具有 **开环稳定性**（即动力学自身满足 EISS）时成立。在确定性、完全可观测的 robomimic tool_hang 任务中，执行 ≥4 步的动作块显著提升成功率，且预测视界的边际效应较低（Figure 2 left）；噪声注入在此类稳定环境下也能协同生效（Figure 2 right）。然而，一旦开环稳定性缺失（如 HalfCheetah-v5），朴素分块会导致灾难性崩溃（Figure 3 right），此时必须依赖噪声注入提供的局部可激励探索。
- **噪声注入**的成功依赖于两条关键实践细节：（1）必须 **记录清洁动作标签**而非噪声标签——使用噪声标签会直接导致性能崩溃（Figure 3 left）；（2）混合比例 α 的边际影响很小，只要噪声注入轨迹数量足够（Figure 3 center）。理论保证建立在局部线性化、光滑动力学和专家闭环的 EISS 特性之上，且要求专家策略为确定性；这些条件在实践中可能不完全满足，过于离轨的探索仍可能超出线性化有效区域。

### 局限与开放问题
尽管本文在理论和实验上建立了强因果机制，其结论仍存以下显式边界：
- **线性时间因子残留**：噪声注入下的轨迹误差界含与步长 T 线性的因子（Theorem 2，约 $O_{\star}(T) \sigma_{\mathbf{u}}^{-2} J_{DEMO}$），虽较指数灾难已大幅改善，但在极长时窗场景下累积误差可能仍不可忽略。能否通过超收缩或 max-norm 分析彻底消除对 T 的依赖是未解决的问题。
- **误差界紧度与参数选择**：当前论述未给出分块长度 ℓ 的精确下限（仅对数级依赖）及其对统计复杂度的定量影响；噪声尺度 σ_u 和混合比 α 的选择缺乏自动化指导，设计鲁棒的实用数据采集配方是明确的工程前沿。
- **与迭代交互的本质优势比较**：噪声注入被证明可与迭代方法匹敌甚至超越，但文中并未回答"迭代式交互在统计上是否拥有噪声注入无法企及的根本优势"这一理论问题，需进一步分离交互与探索的增益机制。
- **策略类表达力与方差**：动作分块实际上定义了更小假设空间的策略类 Π_chunk,ℓ，其相较于直接多步预测是否真的降低了渐近方差，仍属未探索领域。
- **光滑度和控制论量的精确角色**：本文的分析大量依赖 EISS、局部光滑和可激励性子空间刻画，如何将这些量的作用精确化（如给出依赖于系统矩阵 A, B 的更紧界）仍是开放的理论方向。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Action_Chunking_and_Data_Augmentation_Yield_Exponential_Improvements_in_Behavior_Cloning_for_Continuous_Spaces.pdf

![[paperPDFs/ICLR_2026/Action_Chunking_and_Data_Augmentation_Yield_Exponential_Improvements_in_Behavior_Cloning_for_Continuous_Spaces.pdf]]
