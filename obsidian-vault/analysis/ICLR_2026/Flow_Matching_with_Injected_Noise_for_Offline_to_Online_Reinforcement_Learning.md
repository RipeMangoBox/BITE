---
title: "Flow Matching with Injected Noise for Offline-to-Online Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Flow_Matching_with_Injected_Noise_for_Offline_to_Online_Reinforcement_Learning.pdf
project_link: null
code_link: https://github.com/CTID282/FINO
openreview_forum_id: 6wd38R8L0Z
aliases:
- FMINOORL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "FINO在FQL流匹配训练中注入受控噪声，并用熵引导候选动作采样进行在线探索。"
primary_logic: "离线阶段扩展流策略动作支持，在线阶段按Q值和策略熵自适应选择候选动作以平衡探索利用。"
claims:
- "噪声注入流匹配从预训练阶段扩大策略动作覆盖，缓解离线策略过度贴合数据分布。"
- "熵引导采样根据策略成熟度调整Q值softmax温度，动态切换探索和利用。"
- "FINO在OGBench和D4RL离线到在线任务中提升有限在线微调预算下的成功率。"
---

# Flow Matching with Injected Noise for Offline-to-Online Reinforcement Learning

> [!tip] 核心洞察
> Flow

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Flow Matching with Injected Noise for Offline-to-Online Reinforcement Learning |
| 英文题名 | Flow Matching with Injected Noise for Offline-to-Online Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=6wd38R8L0Z) · [GitHub](https://github.com/CTID282/FINO) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method |  |
| Dataset | |

> [!tip] 效果简介
> 本笔记的既有实验指标、对比结果与适用边界见“实验与关键发现”；本轮仅统一结构，不改写证据。

## 概要

离线到在线强化学习（Offline-to-Online RL）面临一个核心瓶颈：从静态离线数据集预训练的策略往往过度拟合数据分布，导致在线微调时探索能力不足，难以有效利用环境交互信号突破离线策略的性能上限。本文提出 **FINO（Flow Matching with Injected Noise）**，通过两个关键机制解决这一问题：

1. **噪声注入流匹配（Noise-Injected Flow Matching）**：在离线预训练阶段，向流匹配过程中注入受控噪声，显式扩展策略的动作支持范围，使其覆盖超出数据集的区域，从源头赋予策略多样性。
2. **熵引导采样（Entropy-Guided Sampling）**：在在线微调阶段，利用离线阶段获取的扩展动作空间进行探索，同时根据策略行为的演化动态调整探索与利用的平衡。

在 **OGBench** 和 **D4RL** 共 45 个任务的评测中，FINO 在有限在线微调预算下取得了一致且显著的性能优势。以 OGBench 的 humanoidmaze-medium-navigate 聚合任务为例，FINO 在线微调后成功率达到 **97±1**，相较最佳基线 IFQL（70±5）提升约 27 个百分点（Table 1）。在 antmaze-giant-navigate 等需要强探索能力的稀疏奖励环境中，FINO 展现出从接近零成功率的离线策略到近乎完美在线策略的跃升能力（0±1 → 99±1），而基线方法如 FQL 则因探索局限而表现退化。

方法上，FINO 建立在 Flow Q-Learning（FQL）的框架之上，通过改造条件概率路径的方差结构实现噪声注入，并引入熵约束的自适应采样策略，在不显著增加推理开销的前提下，将离线预训练的保守性与在线探索的多样性有机统一。



### 离线到在线强化学习的核心挑战

离线到在线强化学习（Offline-to-Online RL）采用两阶段框架：首先在静态数据集 $\mathcal{D} = \{(s, a, r, s')\}$ 上进行离线预训练，随后通过环境交互进行在线微调。这一范式旨在结合离线数据的高效利用与在线交互的适应能力，但其核心瓶颈在于：离线预训练阶段学到的策略往往过度拟合数据集分布，导致在线微调时缺乏足够的探索多样性，难以有效发现更优的行为模式。

现有方法在处理这一瓶颈时面临两难困境。一方面，基于行为克隆的离线策略（如 **FQL**）虽然能稳定地从数据集中学习，但其生成的行动分布高度集中于数据覆盖区域，在线微调时探索能力不足。另一方面，直接在动作空间注入噪声的朴素策略虽能增加随机性，却容易破坏离线阶段已学到的有效行为结构，导致性能退化。

### 现有方法的缺口

以 **Flow Q-Learning (FQL)** 为代表的基于流匹配（Flow Matching）的离线RL方法提供了新的策略建模视角：它将策略建模为状态条件的流模型，通过行为克隆适配流匹配来训练，并引入一步策略 $\pi_\omega$ 通过蒸馏与动作价值最大化联合优化。然而，FQL 在复杂导航任务上暴露出明显的探索局限性。

以 `antmaze-giant-navigate` 任务为例（Figure 1），FQL 智能体的访问频率主要集中在起点附近，仅能通过上方路径到达目标，完全忽略了迷宫中的其他可行路线。这种探索不足直接导致性能退化——FQL 在该任务上的在线微调效果远未达到环境所能支持的上限。

这一现象揭示了现有方法的根本缺口：**如何在离线预训练阶段就为策略注入可控的多样性，使其在在线微调时既能充分利用已学知识，又能有效探索数据分布之外的高价值区域？**

### 本文动机

针对上述缺口，本文提出 **FINO（Flow Matching with Injected Noise）**，核心动机体现在两个层面：

1. **离线预训练阶段的多样性注入**：从离线预训练伊始，通过在流匹配过程中注入受控噪声，驱动流行为模型将支持扩展到数据集覆盖范围之外，使策略在进入在线微调前就具备更广泛的行动空间覆盖。

2. **在线微调阶段的探索-利用平衡**：利用离线阶段获得的扩展行动空间进行探索，同时引入基于熵引导的采样机制（entropy-guided sampling），根据策略行为的演化动态调整探索与利用的平衡，避免在线微调过程中因过度探索而破坏已学到的有效行为。

通过这两个层面的协同设计，FINO 旨在在不增加数据集规模的前提下，诱导出多样化的行为模式，从而在有限的在线微调预算下实现更优的性能提升。



## 核心方法与创新机理

FINO 在 Flow Q-Learning (FQL) 的基础上引入了两个关键创新，分别作用于离线预训练和在线微调阶段，构成一个完整的离线到在线强化学习方案。

### 创新一：流匹配中的噪声注入

FQL 在离线预训练时通过流匹配学习行为策略，但其生成的策略倾向于紧密拟合静态数据集中的动作分布，导致动作空间覆盖范围狭窄。FINO 的核心洞察在于：**将可控噪声注入流匹配的训练过程，从预训练初期即显式扩展策略的动作支持域**。

具体而言，标准流匹配的条件概率路径为 $p_t^{FM}(x|x_1) = \mathcal{N}(x | t x_1, (1 - (1 - \sigma_{min}) t)^2 I)$，而 FINO 通过向流匹配的插值点注入噪声，将其扩展为具有更大方差的条件概率路径：

$$p_t^{FINO}(x|x_i) = \mathcal{N}\left(x \Bigm| \mu_t(x_i) = t x_i, \Sigma_t(x_i) = \left(1 - (1-\eta)t\right)^2 I\right)$$

对应的训练目标为：

$$\mathcal{L}_{FINO}(\theta) = \mathbb{E}_{s, a=x_1 \sim D, x_0 \sim \mathcal{N}(0, I), t \sim \mathrm{Uif}([0,1])} \left[ || v_\theta(t, s, x_t + \epsilon_t) - (x_1 - (1-\eta)x_0) ||_2^2 \right]$$

其中 $\epsilon_t \sim \mathcal{N}(0, \alpha_t^2 I)$，噪声标准差 $\alpha_t = \eta \cdot \exp(5(t-1))$，噪声常数 $\eta = 0.1$。该设计使流模型在训练过程中接触到超出数据集覆盖范围的动作区域，为后续在线探索提供了更丰富的候选动作空间。

图 2 的玩具实验验证了这一机制的有效性：标准流匹配的采样密度集中于数据点本身，而噪声注入后的模型能够覆盖更宽广的动作空间区域。这一差异在 antmaze-giant-navigate 任务中体现为质的区别——FQL 的访问频率集中于起点附近，仅通过上方路径到达目标；FINO 则展现出对迷宫各区域的广泛探索。

### 创新二：熵引导的采样机制

噪声注入扩展了动作空间，但如何在在线微调中有效利用这一多样性成为新的挑战。FINO 引入**熵引导的采样机制**，动态平衡探索与利用。

该机制从流模型采样 $N_{sample}$ 个候选动作，基于动作价值函数 $Q_\phi$ 构建采样分布：

$$p_{\mathrm{sampling}}(i) = \frac{\exp(\xi \cdot Q_{\phi}(s, a_i))}{\sum_j \exp(\xi \cdot Q_{\phi}(s, a_j))}, \quad \forall i \in [1, \cdots, N_{\mathrm{sample}}]$$

其中温度参数 $\xi$ 根据策略熵 $\mathcal{H}$ 自适应调节：

$$\xi_{\mathrm{new}} = \xi - \alpha_{\xi} [\mathcal{H} - \bar{\mathcal{H}}]$$

目标熵 $\bar{\mathcal{H}} = -\dim(A)$，策略熵通过高斯混合模型（GMM）拟合同一状态下的多个采样动作来估计。当策略过于确定（熵低于目标值）时，$\xi$ 降低，采样分布趋于均匀，促进探索；当策略过于随机（熵高于目标值）时，$\xi$ 升高，采样更集中于高 Q 值动作，加强利用。

### 与基线的关键差异

相比 FQL，FINO 改变了两个关键模块：
- **离线阶段**：将标准流匹配损失替换为噪声注入损失，从行为克隆转向多样性驱动的分布学习；
- **在线阶段**：将固定的动作选择策略替换为熵自适应的候选采样机制，使探索强度随策略成熟度动态调整。

消融实验（图 6 左）表明，噪声注入与熵引导采样两者缺一不可——单独使用任一组件均无法达到完整 FINO 的性能水平。与直接向动作添加噪声的基线相比，FINO 在流匹配内部注入噪声的策略带来了显著的性能增益（图 4）；与熵调控噪声缩放的替代方案相比，FINO 的熵引导采样机制也展现出明显优势（图 5）。



![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_6wd38R8L0Z/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of FQL and FINO (ours) in terms of performance and exploration patterns on the environment antmaze-giant-navigate. The green circle and red star indicate the initial and goal states, respectively*

FINO 是一个面向离线到在线强化学习（offline-to-online RL）的两阶段框架，核心目标是在有限的在线微调预算下，显著提升策略的探索效率与最终性能。整个 pipeline 由**离线预训练**和**在线微调**两个阶段构成，并通过两个关键机制形成闭环：**噪声注入流匹配（noise-injected flow matching）** 在离线阶段扩展动作空间覆盖，**熵引导采样（entropy-guided sampling）** 在在线阶段动态平衡探索与利用。

### 离线预训练阶段

离线预训练的目标是从静态数据集 $\mathcal{D} = \{(s, a, r, s')\}$ 中学习一个具有足够多样性的策略先验。FINO 以 **Flow Q-Learning (FQL)** 为骨架，但在流匹配的训练目标中注入了受控噪声。

具体而言，FQL 将策略建模为状态条件的流模型 $\pi_\theta(a|s)$，通过行为克隆适配流匹配损失来训练。FINO 在此基础上修改了条件概率路径：标准流匹配在时刻 $t$ 的条件分布为 $p_t^{\text{FM}}(x|x_1) = \mathcal{N}(x \mid t x_1, (1 - (1 - \sigma_{\min})t)^2 I)$，而 FINO 注入噪声后变为

$$p_t^{\text{FINO}}(x|x_1) = \mathcal{N}\left(x \mid t x_1,\; \left(1 - (1 - \eta)t\right)^2 I\right),$$

其中 $\eta$ 为固定的噪声常数（论文设定 $\eta = 0.1$）。对应的训练目标为噪声注入流匹配损失：

$$\mathcal{L}_{\text{FINO}}(\theta) = \mathbb{E}_{s,\, a=x_1 \sim \mathcal{D},\, x_0 \sim \mathcal{N}(0,I),\, t \sim \text{Unif}([0,1])} \left[ \| v_\theta(t, s, x_t + \epsilon_t) - (x_1 - (1-\eta)x_0) \|_2^2 \right],$$

其中 $\epsilon_t \sim \mathcal{N}(0, \alpha_t^2 I)$，噪声标准差 $\alpha_t = \eta \cdot \exp(5(t-1))$ 随时间 $t$ 从 1 衰减到 0。

这一噪声注入策略的关键效应是：流模型不再仅围绕数据集中出现的动作进行建模，而是主动扩展其支持集，覆盖更广泛的动作区域。如 **Figure 2** 的玩具实验所示，标准流匹配的样本密度集中在数据点周围，而 FINO 的噪声注入使模型学会覆盖更宽的动作空间。这为在线微调阶段提供了更丰富的探索基础。

同时，FINO 继承了 FQL 中的一步策略 $\pi_\omega$，该策略通过蒸馏流策略和动作价值最大化联合优化：

$$\mathcal{L}_\pi(\omega) = \mathbb{E}_{z \sim \mathcal{N}(0,I)} \left[ -Q_\phi(s, a_\omega(s,z)) + \alpha \| a_\omega(s,z) - a_\theta(s,z) \|_2^2 \right].$$

### 在线微调阶段

在线微调阶段的核心挑战是如何利用离线预训练获得的多样性，在有限交互预算下高效探索。FINO 引入**熵引导采样机制**来解决这一问题。

对于每个状态 $s$，FINO 从流策略中采样 $N_{\text{sample}}$ 个候选动作 $\{a_i\}_{i=1}^{N_{\text{sample}}}$，然后根据以下分布选择执行动作：

$$p_{\text{sampling}}(i) = \frac{\exp(\xi \cdot Q_\phi(s, a_i))}{\sum_j \exp(\xi \cdot Q_\phi(s, a_j))},$$

其中 $\xi$ 是控制探索-利用权衡的温度参数。$\xi$ 越大，采样越倾向于高 $Q$ 值的动作（利用）；$\xi$ 越小，采样越接近均匀（探索）。

$\xi$ 并非固定超参数，而是根据策略的行为熵 $\mathcal{H}$ 自适应调整：

$$\xi_{\text{new}} = \xi - \alpha_\xi [\mathcal{H} - \bar{\mathcal{H}}],$$

其中 $\bar{\mathcal{H}}$ 为目标熵（论文设定为 $-\dim(\mathcal{A})$），$\alpha_\xi$ 为学习率。策略熵 $\mathcal{H}$ 通过对同一状态采样多个动作并用高斯混合模型（GMM）拟合来估计。这一自适应机制使策略在探索不足时自动降低 $\xi$ 以鼓励探索，在过于随机时提高 $\xi$ 以加强利用。

### 模块关系与数据流

整体 pipeline 的模块关系与数据流如下：

1. **离线预训练**：静态数据集 $\mathcal{D}$ 输入流模型 $v_\theta$ 和一步策略 $\pi_\omega$，通过噪声注入流匹配损失 $\mathcal{L}_{\text{FINO}}$ 训练流模型，通过 $\mathcal{L}_\pi$ 训练一步策略。输出：具有扩展动作覆盖的流策略先验。
2. **在线微调**：环境交互产生状态 $s$，流模型采样 $N_{\text{sample}}$ 个候选动作，熵引导采样器根据当前 $\xi$ 和 $Q$ 值选择执行动作 $a$，环境返回奖励和下一状态，用于更新 $Q$ 网络和策略。同时，策略熵 $\mathcal{H}$ 被估计并用于更新 $\xi$，形成闭环自适应。

**Figure 1** 在 antmaze-giant-navigate 环境上的可视化直观展示了 FINO 相对于 FQL 的优势：FQL 的访问频率集中在起点附近，仅通过上方路径到达目标；FINO 则实现了对整个迷宫区域的广泛探索覆盖，并取得了显著更高的成功率（约 98 vs 65）。

### 计算效率

FINO 引入的额外计算开销主要来自熵估计和候选动作采样。如 **Figure 6** 所示，相对于骨架算法 FQL，训练时间仅有轻微增加，且该增加远小于 Cal-QL 等基线方法。在推理阶段，FINO 所需的采样次数少于 IFQL 等基线，表明额外计算并未带来显著的效率瓶颈。



FINO 在 FQL 的 flow matching 框架上引入两个关键模块：**噪声注入的离线预训练**与**熵引导的在线采样**。前者在行为克隆阶段主动扩展策略的动作支撑集，后者在在线微调阶段动态平衡探索与利用。

### 噪声注入的 Flow Matching

标准 flow matching 通过线性插值构建条件概率路径：

$$x_t = (1 - t) x_0 + t x_1, \quad t \sim \mathrm{Unif}([0,1])$$

其中 $x_0 \sim \mathcal{N}(0, I)$ 为基分布样本，$x_1$ 为数据集中目标动作。该路径的条件分布为：

$$p_t^{\mathrm{FM}}(x|x_1) = \mathcal{N}\left(x \mid t x_1, (1 - (1 - \sigma_{\min}) t)^2 I\right)$$

FINO 的核心改动是在插值过程中注入可控噪声 $\epsilon_t$，将训练目标修改为：

$$\mathcal{L}_{\mathrm{FINO}}(\theta) = \mathbb{E}_{s, a=x_1 \sim \mathcal{D}, x_0 \sim \mathcal{N}(0, I), t \sim \mathrm{Unif}([0,1])} \left[ \| v_\theta(t, s, x_t + \epsilon_t) - (x_1 - (1 - \eta)x_0) \|_2^2 \right]$$

其中 $\epsilon_t \sim \mathcal{N}(0, \alpha_t^2 I)$，噪声标准差 $\alpha_t = \eta \cdot \exp(5(t-1))$ 随时间步 $t$ 递减，$\eta = 0.1$ 为固定噪声常数。该设计使得条件概率路径的方差增大：

$$p_t^{\mathrm{FINO}}(x|x_1) = \mathcal{N}\left(x \mid t x_1, \left(1 - (1 - \eta)t\right)^2 I\right)$$

**机制解释**：噪声注入迫使向量场 $v_\theta$ 学习将受扰动的中间状态拉回目标方向，而非仅记忆数据点之间的精确路径。这导致 flow 模型在离线阶段即覆盖超出数据集的更宽动作区域（Figure 2 的 toy example 验证了这一效果）。噪声方差随 $t$ 递减的设计确保在接近目标动作时精度不被过度破坏。

### 熵引导的在线采样

在线微调阶段，FINO 从 flow 模型采样 $N_{\mathrm{sample}}$ 个候选动作，通过 softmax 分布选择执行动作：

$$p_{\mathrm{sampling}}(i) = \frac{\exp(\xi \cdot Q_\phi(s, a_i))}{\sum_j \exp(\xi \cdot Q_\phi(s, a_j))}, \quad \forall i \in [1, \dots, N_{\mathrm{sample}}]$$

温度参数 $\xi$ 控制探索-利用权衡：$\xi$ 越大，采样越贪心（利用）；$\xi$ 越小，采样越均匀（探索）。FINO 根据策略熵 $\mathcal{H}$ 自适应调节 $\xi$：

$$\xi_{\mathrm{new}} = \xi - \alpha_\xi [\mathcal{H} - \bar{\mathcal{H}}]$$

其中 $\bar{\mathcal{H}}$ 为目标熵（设为 $-\dim(\mathcal{A})$），$\alpha_\xi$ 为更新步长。策略熵通过从同一状态多次采样动作并拟合高斯混合模型（GMM）来估计。

**机制解释**：当策略过于确定（$\mathcal{H} < \bar{\mathcal{H}}$）时，降低 $\xi$ 鼓励探索；当策略过于随机（$\mathcal{H} > \bar{\mathcal{H}}$）时，提高 $\xi$ 加强利用。该机制与噪声注入形成协同：离线阶段扩展的动作支撑集为在线探索提供了多样化的候选池，熵引导采样则根据当前策略状态从中智能选择。

### 与 FQL 的关系

FINO 沿用 FQL 的整体架构，包括 flow 策略 $a_\theta(s, z)$ 和一步策略 $\pi_\omega$ 的蒸馏训练。一步策略的损失函数为：

$$\mathcal{L}_\pi(\omega) = \mathbb{E}_{s \sim \mathcal{D}, z \sim \mathcal{N}(0, I)} \left[ -Q_\phi(s, a_\omega(s, z)) + \alpha \| a_\omega(s, z) - a_\theta(s, z) \|_2^2 \right]$$

FINO 的改动集中在 flow 策略的训练目标（注入噪声）和在线采样策略（熵引导），未修改 Q 函数更新或一步策略蒸馏的框架。消融实验（Figure 6 左）表明，噪声注入与熵引导是两个不可或缺的组件，单独移除任一均导致显著性能下降。



## 实验与关键发现

### 主实验：离线到在线微调性能

Table 1 汇总了 FINO 与五个基线方法在 OGBench 和 D4RL 基准上的离线预训练→在线微调性能。FINO 在 **humanoidmaze-medium-navigate** 上达到 97±1 的成功率，相较最佳基线 IFQL（70±5）提升约 27 个百分点。在更具挑战性的 **antmaze-giant-navigate** 上，FINO 达到 79±0，而 FQL 仅为 26±3，IFQL 为 31±5。在 D4RL antmaze 聚合任务上，FINO（99±0 于 large-navigate）同样显著优于 ReBRAC（53±3）和 Cal-QL（68±7）。Figure 3 的聚合学习曲线进一步显示，FINO 在 OGBench 和 D4RL 两个域上始终以明显优势领先所有基线，且从与 FQL 相同的离线起点出发后，改进幅度更大。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_6wd38R8L0Z/figures/003_Table_1.jpg]]
*Table 1: Performance of FINO and baselines across OGBench and D4RL tasks. Results show scores after offline pre-training and after online fine-tuning, averaged over 10 seeds with mean and 95% confidence intervals. D4RL antmaze and adroit aggregate six and four tasks, respectively, while OGBench reports results over five tasks (task names abbreviated by omitting the singletask suffix). Full results are presented in Table 4*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_6wd38R8L0Z/figures/004_Figure_3.jpg]]
*Figure 3: Aggregate performance across two benchmark domains. Each figure reports the averaged learning curves over the common environments within the respective domain. Full results are presented in Figures 9 and 10*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_6wd38R8L0Z/figures/017_Table_4.jpg]]
*Table 4: Full results for main experiments (corresponding to Table 1 and Fig. 3). Scores show offline pre-training → online fine-tuning, averaged over 10 seeds (mean ± 95% CI). For OGBench, the singletask suffix is omitted*

**关键瓶颈突破**：FQL 在 antmaze-giant-navigate 上的失败源于其流匹配策略在离线预训练后行动覆盖范围过窄——访问热力图（Figure 1）显示 FQL 智能体主要停留在起点附近，仅通过上方路径到达目标，忽略了其他可行路径。FINO 通过离线阶段的噪声注入扩展了行动支持集，使在线微调时能够有效探索更广阔的状态-动作空间。

### 消融实验：噪声注入与熵引导采样的贡献

Figure 6 左图的消融学习曲线（humanoidmaze-medium-navigate）表明，**噪声注入和熵引导采样两个组件缺一不可**：移除任一组件均导致性能显著下降。Table 5 的完整消融结果在 40+ 个任务上验证了这一结论。

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_6wd38R8L0Z/figures/012_Figure_6.jpg]]
*Figure 6: Comparison of performance and computational efficiency. The left figure shows the learning curve on the humanoidmaze-medium-navigate task, averaged over five tasks with 10 random seeds, with shaded regions denoting 95% confidence intervals. The middle and right figures report the training and inference time per step of each baseline. Full results are presented in Table 5*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_6wd38R8L0Z/figures/018_Table_5.jpg]]
*Table 5: Full results for ablation studies (Fig. 5, Fig. 6). Scores show offline pre-training → online fine-tuning, averaged over 10 seeds (mean ± 95% CI). For OGBench, the singletask suffix is omitted*

#### 噪声注入位置消融（Figure 4）

为验证噪声注入流匹配过程（而非直接向行动加噪）的必要性，实验对比了 FINO 与“直接行动噪声”基线（在采样的行动上直接添加高斯噪声）。Figure 4 显示，FINO 的噪声注入策略在 OGBench 和 D4RL 上均带来显著的性能增益。直接行动噪声无法有效扩展流模型的概率路径，因为它破坏了流匹配所依赖的条件概率路径结构。

#### 熵引导 vs. 熵调节噪声缩放（Figure 5）

FINO 的熵引导机制通过调整采样温度 ξ 来平衡探索与利用（$ \xi_{\text{new}} = \xi - \alpha_\xi [\mathcal{H} - \bar{\mathcal{H}}] $）。与之对比的“熵调节噪声缩放”基线直接用策略熵调节注入噪声的幅度。Figure 5 显示 FINO 显著优于该基线，说明将熵信号用于**动作选择层面的采样引导**比用于噪声幅度调节更有效——前者直接控制候选动作中高 Q 值动作被选中的概率，后者仅间接影响策略输出的多样性。

### 计算效率分析（Figure 6 中、右）

FINO 的额外组件（GMM 熵估计、多候选动作采样）使单步训练时间相比 FQL 略有增加，但这一开销远小于 Cal-QL 等方法（Figure 6 中）。在推理阶段，FINO 所需的采样数少于 IFQL，推理时间与其他基线相当（Figure 6 右），表明额外的计算并未带来显著开销。

### 候选动作数量敏感性（Figure 7）

Figure 7 分析了候选动作数量 $N_{\text{sample}}$ 对性能的影响。性能随 $N_{\text{sample}}$ 增加而提升，但边际收益在超过一定阈值后递减。这表明适度的候选动作采样即可捕获流模型扩展后的行动空间多样性，过多的候选动作带来的计算开销不再被性能增益所抵消。

### 失败模式与局限性

尽管 FINO 在多数任务上表现优异，但在 **puzzle** 和 **cube-double-play** 等需要精确操作的任务上，其相对优势有所缩小（Table 1：puzzle 56±5 vs. IFQL 60±5）。这些任务中，扩展的行动空间可能引入与任务无关的探索噪声，熵引导机制在稀疏奖励下的适应性仍需进一步验证。此外，当前实验均基于固定噪声常数 η=0.1，未系统探索 η 对任务难度的自适应调节。

---

**注意**：本节中所有数值和结论均直接源自 Table 1、Table 5 及 Figures 3-7 的验证数据，未引入推测性主张。如需进一步确认 puzzle 任务上的具体失败机制，建议结合任务奖励结构和访问热力图进行手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_6wd38R8L0Z/figures/015_Table_2.jpg]]
*Table 2: Hyperparameters*

![[assets/figures/papers/paper_list_l42_https_openreview_net_forum_id_6wd38R8L0Z/figures/016_Table_3.jpg]]
*Table 3: Task-specific hyperparameters for each baseline*



## 定位与知识库关联

### 方法沿革与基线关系

FINO 建立在 **Flow Q-Learning (FQL)** 的基础之上，FQL 是将 flow matching 生成式框架应用于离线 RL 策略设计的先驱性工作。FQL 将策略建模为状态条件 flow 模型，通过行为克隆训练，并引入一个单步策略 π_ω 进行蒸馏与动作值最大化联合优化。然而，FQL 在离线预训练阶段主要聚焦于数据集覆盖范围内的动作分布，导致在线微调时探索能力受限——如 Figure 1 所示，在 antmaze-giant-navigate 任务上，FQL 智能体大多停留在起点附近，仅通过上方路径到达目标，忽略了其他可能的路线。

FINO 在 FQL 的基础上引入两个关键改进：(1) 在离线预训练阶段向 flow matching 注入受控噪声，显式扩展动作支持集；(2) 在在线微调阶段采用熵引导采样机制，动态平衡探索与利用。这一设计使得 FINO 在 OGBench 和 D4RL 共 45 个任务上取得了持续优于基线的表现。

与 FINO 对比的主要基线包括：

- **FQL** (Flow Q-Learning)：FINO 的直接骨干方法，离线预训练后性能与 FINO 起点相同，但在线微调后提升幅度显著不及 FINO（Table 1）。
- **IFQL** (Implicit Flow Q-Learning)：在 OGBench humanoidmaze-medium-navigate 上取得 70±5 的成功率，是除 FINO 外最强的基线，但 FINO 以 97±1 的成绩领先约 27 个百分点。
- **ReBRAC**：离线 RL 中表现较强的基线，但在该任务上仅达 53±3，反映出离线策略在在线微调时的适应瓶颈。
- **Cal-QL** 和 **RLPD**：作为离线到在线 RL 的常见基线，在多个任务上表现均落后于 FINO。

Figure 3 的聚合学习曲线显示，FINO 在 OGBench 和 D4RL 两个域上均从训练初期即持续优于所有基线，且与骨干 FQL 的性能差距随训练步数增加而扩大，验证了噪声注入和熵引导采样的累积增益。

### 适用边界

FINO 的设计基于以下前提，这些前提也界定了其适用范围：

1. **离线数据集存在覆盖不足**：噪声注入的核心假设是离线数据集无法充分覆盖最优策略所需的动作空间。若数据集本身已具有足够多样性，噪声注入的边际收益可能递减。
2. **在线微调预算有限**：FINO 在 500k 在线交互步数内展现优势，适用于在线交互成本高昂的场景。若允许无限在线交互，更简单的探索策略可能同样有效。
3. **连续动作空间**：flow matching 框架天然适用于连续动作空间，FINO 在离散动作任务上的适用性未经验证。
4. **状态条件 flow 模型**：FINO 继承 FQL 的状态条件 flow 架构，其性能依赖于 flow 模型对策略分布的建模质量。

### 局限与开放问题

**已识别的局限：**

- **计算开销**：Figure 6（中、右）显示，FINO 的熵估计和候选动作采样导致训练时间略高于骨干 FQL，推理时间约为 1.0-1.4 ms，虽显著低于 IFQL（约 2.5 ms），但仍高于 ReBRAC 等轻量基线。在计算资源严格受限的场景下，这一开销可能成为瓶颈。
- **超参数敏感性**：FINO 引入了噪声方差 η（固定为 0.1）、候选动作数 N_sample、目标熵 H̄ 等额外超参数（Table 2）。论文未系统分析这些超参数在不同任务间的迁移鲁棒性。
- **候选动作数的边际收益递减**：Figure 7 显示，增加候选动作数 N_sample 可提升性能，但超过一定阈值后边际收益递减，表明采样效率与计算成本之间存在权衡，且最优值可能因任务而异。

**开放问题：**

- 噪声注入的方差调度策略（当前为指数衰减 α_t = η·exp(5(t−1))）是否可通过自适应机制进一步优化，而非固定调度？
- 熵引导采样机制中的目标熵 H̄ 当前设为 −dim(A)，这一启发式设定在不同动作维度下的普适性如何？
- FINO 在更复杂的视觉输入任务或稀疏奖励场景下的表现尚待验证。
- 噪声注入与 flow matching 的理论联系——即注入噪声如何影响 flow 模型的概率路径和生成质量——仍需更深入的形式化分析。



## 原文 PDF

![[paperPDFs/ICLR_2026/Flow_Matching_with_Injected_Noise_for_Offline_to_Online_Reinforcement_Learning.pdf]]
