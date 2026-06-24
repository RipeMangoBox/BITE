---
title: "Q-RAG: Long Context Multi‑Step Retrieval via Value‑Based Embedder Training"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Q_RAG_Long_Context_MultiStep_Retrieval_via_ValueBased_Embedder_Training.pdf
aliases:
- QR
- Q-RAG
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将多步检索视为有限时域MDP，对嵌入器进行最大熵强化学习训练，通过状态与动作嵌入的内积估计Q值，并引入基于已检索事实的相对位置编码以支持时间推理。"
primary_logic: "仅微调轻量级嵌入器即可实现与微调LLM相当的多步检索性能，同时保持O(N)的时间/空间复杂度和极快的训练收敛，从而以极低资源成本在超长上下文中达到最先进的常识推理与寻针（NIAH）性能。"
claims:
- "Q‑RAG在BabiLong QA3（最难的子任务）上几乎无性能退化，与所有基线相比优势最大，尤其在10M token上下文下精度保持~0.95。"
- "在RULER基准的所有NIAH子任务上达到接近完美的准确率（4K‑1M均为100或99.7），且未观察到长度退化。"
- "在HotPotQA上事实检索F1持平Beam‑Retriever（SOTA），在分布外Musique上大幅超越所有基线。"
- "消融实验表明，移除软Q函数（熵正则化）或目标网络会显著降低长上下文检索F1（32K时从97.1降至94.5/75.9）。"
---

# Q-RAG: Long Context Multi‑Step Retrieval via Value‑Based Embedder Training

> [!tip] 核心洞察
> 仅微调轻量级嵌入器即可实现与微调LLM相当的多步检索性能，同时保持O(N)的时间/空间复杂度和极快的训练收敛，从而以极低资源成本在超长上下文中达到最先进的常识推理与寻针（NIAH）性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Q-RAG：基于价值学习的嵌入器训练实现长上下文多步检索 |
| 英文题名 | Q-RAG: Long Context Multi‑Step Retrieval via Value‑Based Embedder Training |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=MS9nWFY7LG); [GitHub](https://github.com/griver/Q-RAG) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Q‑RAG |
| Dataset | BabiLong QA3 (10M tokens), RULER NIAH Avg (4K‑1M), HotPotQA, Musique (out‑of‑distribution) |

> [!tip] 效果简介
> - BabiLong QA3 (10M tokens) 上，Answer Accuracy 为 ~0.95，对比 ~0.37 (ARMT)，变化 ~+0.58。
> - RULER NIAH Avg (4K‑1M) 上，Accuracy (%) 为 100 (4K) / 99.7 (1M)，对比 99.7 (LongRoPE2‑8B at 4K) / not reported at 1M，变化 +0.3 / only Q‑RAG reports near‑perfect at 1M。
> - HotPotQA 上，Fact F1 为 0.93，对比 0.97 (Beam‑Retriever)，变化 -0.04。

## 概述

现有长上下文多步检索方法（如基于 Transformer 的 Beam‑Retriever、微调 LLM 的 Search‑R1、或构建知识图谱的 GraphReader）普遍依赖昂贵的 LLM 微调或慢节奏的图构建，难以高效扩展到超长文本（>1M token），且无法充分挖掘嵌入空间的紧凑性以实现快速推理。**Q‑RAG** 提出一种全新的训练范式：冻结 LLM，仅微调轻量级嵌入器，将多步检索建模为有限时域马尔可夫决策过程（MDP），并通过最大熵强化学习进行训练。其核心组件包括状态嵌入器 $E_s$ 与动作嵌入器 $E_a$，利用二者内积直接估计每个文本片段的 $Q$ 值；同时引入基于已检索事实区间的相对位置编码，赋予代理对文档时序关系的内生感知。训练采用并行 Q 网络（PQN）与 $\lambda$‑回报，无需经验回放即可在单张 A100‑80GB GPU 上于 12 小时内完成收敛，推理时的时间和空间复杂度均保持 $\mathcal{O}(N)$，天然适应超长上下文。

在超长上下文检索基准上的实验结果表明，**仅微调嵌入器便可在多项任务上匹敌甚至超越微调 LLM 的方法**。具体而言，在 BabiLong 最难的 QA3 子任务上，Q‑RAG 在高达 10M token 的上下文下仍保持约 0.95 的答案准确率（ARMT 在相同长度下降至 ∼0.37），几乎无性能退化。在 RULER 基准的“大海捞针”（NIAH）所有子任务上，Q‑RAG 在 4K 和 1M token 上下文中分别取得 100% 和 99.7% 的近乎完美准确率，未见长度退化。在开放域多步检索任务 HotPotQA 上，Q‑RAG 的事实检索 F1 达到 0.93，与当前 SOTA 方法 Beam‑Retriever 持平；而在分布外测试集 Musique 上，Q‑RAG 以 0.71 的 Fact F1 大幅超越其他基线（Beam‑Retriever 仅 0.61），亦与需要全量 LLM 微调的 Search‑R1 持平。消融实验进一步揭示，移除软 Q 函数（熵正则化）或目标网络将分别导致长上下文检索 F1 从 97.1 降至 94.5 和 75.9，证实了最大熵框架与目标网络对稳定学习的关键作用。训练效率方面，Q‑RAG 在消费级 GPU 上耗时不到 12 小时即达到峰值性能，相比需 8×A100 的大规模 LLM 微调方案具有显著资源公平优势，为低成本、高效率的超长上下文推理提供了可复现的新范式。

## 背景与动机

长上下文理解正成为大语言模型走向复杂推理的关键能力：用户需要在长达数百万tokens的文档、对话或知识库中定位多条分散的证据，并基于这些证据完成问答、事实核查或叙事推理。然而，将推理建立在超长文本之上远非简单的检索增强生成（RAG）可及，因为真实任务往往要求**多步检索**——智能体必须在多轮中迭代选择新片段，直至收集到所有支持事实。随着上下文长度向百万级（1M tokens）扩展，这一多步决策过程面临三大核心挑战：**检索精度不退化**、**训练与推理代价可控**，以及**对时间顺序与组合关系的敏感建模**。

---

### 现有方法及其瓶颈

当前处理长上下文多步推理的方法大致分为三类，各自在成本、效率或泛化能力上存在明显缺口。

**微调LLM的范式**（如Search‑R1、Re‑Plug）让语言模型学习生成中间搜索查询或直接输出答案。这类方法虽然利用了LLM的推理先验，但需要在海量长文本上微调数十亿参数的模型，训练资源需求巨大（通常需8×A100 GPU），推理延迟高，且很难在远超训练长度的上下文中保持性能。

**检索器重排序范式**的代表是Beam‑Retriever，它使用一个额外的Transformer对候选轨迹进行评分并进行搜索。该方法在分布内数据集（如HotPotQA）上达到了当前最佳的事实F1（0.97），但其监督训练依赖大量人工标注的黄金检索轨迹，向分布外任务（如Musique OOD）泛化时Fact F1骤降至0.61，且推理过程中复杂的搜索机制拖慢了整体速度。

**零样本图构建方法**（如GraphReader）通过LLM将长文档转化为知识图谱再逐步探查。这类方法不依赖训练，但图谱构建本身的成本随上下文长度急剧上升，在超长上下文中几乎不可行。此外，**循环记忆Transformer**（Titans, Atlas, ARMT, RMT）通过压缩历史或分段循环将上下文窗口扩展到百万tokens，但在需要精确时序匹配和多跳组合的困难任务上表现极不稳定。以BabiLong最难子任务QA3为例，ARMT在10M tokens下回答准确率衰减至约0.37（Figure 2b），显示出单纯依赖隐式记忆无法可靠地保持多步推理链。

---

### 为什么需要新的路径

上述方法的一个共同特征是：**核心决策（下一步检索什么）仍依赖语言模型本身或其代理组件**，而嵌入空间仅被当作静态的相似度度量。然而，嵌入器天然擅长将文本映射到紧凑的低维向量，且内积计算效率极高（O(N)复杂度）。如果能让嵌入器直接学会多步检索的策略——即每一步根据已收集的证据状态，为所有候选片段计算一个“选择价值”，并按此价值行动——就有可能在保持嵌入检索的速度和可扩展性的同时，获得接近甚至超越LLM微调的决策质量。

这正是本文的动机。Q‑RAG将多步检索形式化为有限时域的马尔可夫决策过程（MDP），并通过**最大熵强化学习**直接训练一对轻量级的状态嵌入器与动作嵌入器。其中，状态嵌入器编码当前查询与已选片段，动作嵌入器编码候选片段及其相对于已检索事实的时间位置；二者内积直接给出该候选片段在当前状态下的**软Q值**。策略按Boltzmann分布采样下一动作，而价值函数通过带目标网络的时序差分学习（TD）和λ‑回报稳定更新。整个训练只需12小时在单张A100‑80GB GPU上完成，且仅微调嵌入器，LLM完全保持冻结。

这种设计带来三个根本性变化：

1. **训练与推理效率的质变**：训练成本从多卡LLM微调压缩到单张消费级GPU的12小时内，推理时间复杂度保持O(N)，在百万tokens上下文中仍可实时运行。
2. **长度泛化的鲁棒性**：在RULER基准的全部NIAH子任务上，Q‑RAG在4K至1M tokens的上下文长度下均取得近乎完美的准确率（100% 至 99.7%，Table 1），未出现任何长度退化。
3. **困难任务上的显著提升**：在BabiLong的QA3（需要最长时间推理链且涉及时间意识）上，Q‑RAG在10M tokens下精度维持约0.95，远超所有基线（Figure 2b）。在分布外Musique数据集上，Q‑RAG的Fact F1达到0.71，与全量微调LLM的Search‑R1持平，且大幅超越Beam‑Retriever（0.61，Table 2）。

这些证据共同表明，**将多步检索中的“何时查什么”决策落实为嵌入空间中的值函数学习，既能突破LLM微调的效率瓶颈，又能弥补静态嵌入在组合与时间推理上的不足**，为超长上下文推理提供了一条成本与性能兼顾的实用路径。

## 核心创新

现有长上下文多步检索方法普遍存在两个制约瓶颈：一是依赖对大型语言模型（LLM）的监督微调或策略梯度微调（如 Search‑R1 通过微调 LLM 生成中间检索查询；Beam‑Retriever 通过轨迹克隆训练重排序器），训练成本高昂且难以扩展到千万级 token 的超长上下文；二是基于图构建或循环记忆的零样本方法（如 GraphReader）推理速度慢，无法充分利用预训练嵌入空间的紧凑性进行快速检索。Q‑RAG 的核心创新在于以**轻量级嵌入器为轴心**，将多步检索转化为有限时域马尔可夫决策过程（MDP），并通过**最大熵强化学习**直接优化嵌入空间中的检索策略。这一范式转变从三个关键层面打破了上述瓶颈，仅微调嵌入器即获得了与微调 LLM 相当甚至更优的多步检索性能，同时保持 O(N) 时间/空间复杂度与极快的训练收敛。

**训练对象切换：从微调 LLM 到仅微调嵌入器。**  
无论是 Search‑R1 的查询生成、Beam‑Retriever 的重排序，还是其他基于 PPO/GRPO 的策略微调，baseline 方法均在生成模型一侧施加训练开销，而嵌入器则被冻结。Q‑RAG 反向而行：**冻结 LLM 与环境奖励信号，仅对状态嵌入器 (E_s) 和动作嵌入器 (E_a) 进行端到端强化学习微调**。状态嵌入器将当前的查询与已选取的文本片段编码为高维向量，动作嵌入器则将候选片段及其位置信息映射到同一空间，两者通过内积直接估计每个候选动作的 Q 值：$Q_\theta(s, a^i) = \langle E_s(s), E_a(a^i, i) \rangle$。这种设计使检索策略的学习完全在紧凑的嵌入空间内完成，无需协调 LLM 的参数更新，从而将训练资源从 8×A100 的 LLM 微调降至单张 A100‑80GB 的约 12 小时完成收敛（Figure 6），资源公平性优势显著。

**学习范式切换：从监督复制/PPO 到最大熵时序差分学习。**  
多步检索本质上是一个序列决策问题，但现有方法或依赖带标注轨迹的克隆（Beam‑Retriever），或使用高方差的策略梯度（如 GRPO）微调 LLM。Q‑RAG 采用**带最大熵框架的值函数学习**，引入软 Q 函数与 Boltzmann 策略：  
$$Q^\pi(s,a) = r(s,a) + \gamma V^\pi(s'), \quad V^\pi(s) = \mathbb{E}_{a\sim\pi}[Q^\pi(s,a) - \alpha\log\pi(a|s)], \quad \pi(a|s) \propto \exp(Q_\theta(s,a)/\alpha)$$  
其中温度 $\alpha$ 控制探索与利用的平衡。训练时，Parallel Q‑Network（PQN）借助缓慢更新的目标网络 $\theta'$ 计算 $\lambda$‑return（$G_t^\lambda$），以 MSE 损失 $ \ell_Q = \mathbb{E}[(Q_\theta(s_t, a_t) - G_t^\lambda)^2] $ 驱动在线策略学习，无需经验回放。消融实验（Table 3）直接证明了这一范式的必要性：移除目标网络使 BabiLong QA3 32K 上下文中支持事实 F1 从 97.1 骤降至 75.9；取消熵正则化（Soft‑Q）亦导致 F1 下降至 94.5，且方差增大，说明目标网络对稳定价值估计以及熵正则化对保持充分探索均不可或缺。

**位置编码切换：从绝对位置到基于已检索事实的相对位置。**  
长程叙事与时间推理任务（如 BabiLong QA3）要求模型理解事件发生的先后顺序。Baseline 方法通常仅使用绝对位置编码或完全缺乏时间信息。Q‑RAG 提出**基于已检索事实分区的相对位置编码**，根据当前轨迹中已选取的片段将原始文档索引映射为实数位置 $\rho_t(i)$：  
$$\rho_t(i) = j\delta + \ell\frac{i - b_j}{b_{j+1} - b_j}$$  
其中 $b_j$ 为第 $j$ 个已选片段的起始位置，$\delta$ 为区间宽度。动作嵌入器进而以 $\rho_t(i)$ 替换绝对位置，使代理能够感知候选片段与已提取证据的空间‑时间关系。这一设计是 Q‑RAG 在 BabiLong QA3（超长上下文、多跳时间推理）上几乎无性能退化（Figure 2b, 10M token 仍保持 ~0.95 准确率，远优于最强基线 ARMT 的 ~0.37）的关键推手，也是该方法在 RULER 所有 NIAH 子任务上实现接近完美精度（4K‑1M 均为 100 或 99.7，Table 1）的重要支撑。

综上，Q‑RAG 通过**值函数驱动的嵌入器训练**，将多步检索的决策能力压缩进轻量级嵌入器，在开放性多跳 QA（HotPotQA 事实 F1 持平 Beam‑Retriever 0.93 vs 0.97，Musique OOD 超越至 0.71 vs 0.61，Table 2）和极长上下文寻证（RULER MH QA 1M 达 61，Table 1）等场景均取得顶尖表现；同时具备快速推理（O(N) 内积运算）与训练高效的双重优势，开辟了一条以低资源成本解决超长上下文检索问题的新路径。

## 整体框架

![[assets/figures/papers/iclr26_0016_MS9nWFY7LG_Q-RAG_Long_Context_MultiStep_Retrieval_via_Value/figures/001_Figure_1.jpg]]
*Figure 1: Q-RAG agent interacts with multi-step retrieval environment. The starting state $s _ { 0 }$ contains the initial query q. At the start of the episode, the agent embeds all chunks of the long context $\mathbb { C }$ . At each step t, the agent computes a vector embedding of the current state $s _ { t }$ , , which includes q and all previously selected chunks. For every chunk $c ^ { i } \in \mathbb { A } _ { t }$ , the utility of retrieving it is evaluated by the Q-function $Q _ { \theta } ( s _ { t }$ , a = $c ^ { i }$ ) . The policy $\pi _ { \theta }$ selects the next chunk from $\mathbb { A } _ { t }$ with probability proportional to its $Q _ { \theta } ( s _ { t } , c ^ { i }$ ) value

Q‑RAG 将多步检索形式化为**有限时域马尔可夫决策过程 (MDP)**，并将检索行为完全置于文本片段（chunk）的嵌入空间中进行：仅对轻量级嵌入器进行**最大熵强化学习**训练，而下游 LLM 保持冻结。这一设计使得代理（agent）能够通过向量内积直接估计每个候选片段的“效用”，从而在 O(N) 的时间与空间复杂度下完成多步推理与检索，避免了现有方法中昂贵的 LLM 微调或慢速图构建。

**核心模块与数据流**（参见 Figure 1）：

- **状态嵌入器 $E_s$**：以当前查询 $q$ 及已选择的所有片段作为输入，输出当前状态 $s_t$ 的向量表示。该模块将逐步积累的证据压缩为一个紧凑的搜索状态。
- **动作嵌入器 $E_a$**：将上下文中的每个候选片段 $a^i$ 及其（相对于已提取事实的）**位置编码**映射为动作向量。通过相对位置编码（式 (6)–(7)），代理能够感知不同片段与已有证据之间的时序关系，这是支撑长程叙事任务的关键。
- **Q 值函数 $Q_\theta$**：采用最简洁的形式——直接计算状态向量与动作向量的内积，即 $Q_\theta(s_t, a^i) = \langle E_s(s_t), E_a(a^i, i) \rangle$。该设计将检索价值估计压缩到单一嵌入空间中，使推理成本仅为一次点积。
- **Boltzmann 策略 $\pi_\theta$**：依据 Q 值和温度参数 $\alpha$ 定义的选择分布（式 (3)），代理以软最大化（softmax）概率决定下一步要检索的片段，熵正则化项鼓励探索。
- **时序差分学习**：训练使用 **Parallel Q-Network (PQN)** 骨干，在线计算 $\lambda$-回报 $G_t^\lambda$ 作为目标值，并通过最小化与当前 Q 值的均方误差进行更新（式 (4)–(5)）。此过程无需经验回放缓冲区，收敛极快。
- **目标网络 $\theta'$**：通过指数移动平均缓慢更新，提供稳定的价值估计，消融实验（Table 3）表明移除目标网络会导致长上下文下 F1 从 97.1 骤降至 75.9，证明其对学习稳定性的必要性。

**端到端流程**：输入长文本上下文 $C$ 与用户查询 $q$。初始状态 $s_0$ 仅含 $q$。代理预先嵌入所有片段，然后在每一步 t 计算状态嵌入、所有可用动作的 Q 值，依据 Boltzmann 策略选择下一个片段，并把该片段加入状态形成 $s_{t+1}$。达到预设最大步数 T 或触发基于 Q 阈值的早期停止后，代理将收集到的支持事实传输给生成器 LLM，生成最终答案。训练时，以是否检索到金标支持事实的集合作为终端奖励，利用最大熵强化学习优化嵌入器参数；推理时仅需一次前向嵌入和 T 次内积计算。

**因果机制与瓶颈突破**：现有长上下文多步检索方法通常需要通过 LLM 生成中间查询或构建全图，导致超长上下文（>1M token）下效率急剧下降或无法泛化。Q‑RAG 将“检索决策”完全压缩到嵌入器的内积中，结合最大熵 RL 所引入的探索性 Boltzmann 策略与 TD 学习中的 $\lambda$-回报，使轻量级嵌入器能够学到隐式的多步规划和长程依赖。相对位置编码进一步强化了时间推理能力，使得 Q‑RAG 即便在 4K 长度文档上训练，也能直接泛化至 1M 甚至 10M token 的上下文中并保持接近完美的针检索寻精度（Table 1）与常识推理性能（Figure 2b），而无需对 LLM 做任何微调。

## 核心模块与公式推导

Q‑RAG 将长上下文多步检索形式化为有限时域马尔可夫决策过程（MDP）$\langle \mathcal{S}, \mathcal{A}, p, r, \gamma \rangle$，并在嵌入空间中对轻量级嵌入器进行最大熵强化学习。整个系统由六个核心模块构成：**状态嵌入器**、**动作嵌入器**、**Q 值函数**、**玻尔兹曼策略**、**时序差分学习单元**（含目标网络）以及**相对位置编码**。各模块的协同工作使得代理无需微调大语言模型即可在超长上下文中高效检索。

### 最大熵状态‑动作价值函数

为鼓励探索并防止策略过早收敛到次优轨迹，Q‑RAG 采用软（最大熵）价值函数。给定策略 $\pi$，软 Q 函数定义为

$$
Q^{\pi}(s,a) = r(s,a) + \gamma V^{\pi}\bigl(s' = p(s,a)\bigr), \tag{1}
$$

其中 $s\in\mathcal{S}$ 为当前状态（包含原始查询与已选片段），$a\in\mathcal{A}$ 为动作（选取下一个文本片段），$r$ 为从支持事实获得的终端奖励，$\gamma$ 为折扣因子，$p$ 为确定性转移函数。相应的软状态价值函数为

$$
V^{\pi}(s) = \mathbb{E}_{a\sim\pi(\cdot\mid s)}\Bigl[Q^{\pi}(s,a) - \alpha\log\pi(a\mid s)\Bigr], \tag{2}
$$

其中熵正则项 $-\alpha\log\pi$ 由温度系数 $\alpha$ 控制，显式地鼓励策略保持足够的随机性。

### 状态与动作嵌入器

状态嵌入器 $E_{s}(\cdot;\theta_{1})$ 将当前状态 $s_{t}$ 编码为向量 $\mathbf{h}_{s}\in\mathbb{R}^{d}$；动作嵌入器 $E_{a}(\cdot;\theta_{2})$ 则将候选文本片段 $a^{i}$ 连同其位置信息编码为动作表示 $\mathbf{h}_{a^{i}}\in\mathbb{R}^{d}$。Q 值通过两个嵌入向量的内积高效近似：

$$
Q_{\theta}(s, a^{i}) = \bigl\langle E_{s}(s;\theta_{1}),\; E_{a}(a^{i}, \cdot;\theta_{2}) \bigr\rangle. \tag{3}
$$

该分解使得在每一步只需计算一次状态嵌入，而对所有候选动作仅需矩阵乘法，从而保持推理复杂度为 $O(N)$，支持百万级上下文。

### 玻尔兹曼策略

基于 Q 函数，代理按玻尔兹曼分布选择动作：

$$
\pi_{\theta}(a_{t}\mid s_{t}) = \frac{\exp\!\bigl[\frac{1}{\alpha}(Q_{\theta}(s_{t},a_{t}) - q)\bigr]}{\sum_{a\in\mathcal{A}_{t}}\!\exp\!\bigl[\frac{1}{\alpha}(Q_{\theta}(s_{t},a) - q)\bigr]}, \qquad q = \max_{a\in\mathcal{A}_{t}} Q_{\theta}(s_{t},a). \tag{4}
$$

减去当前最大 Q 值 $q$ 保证了数值稳定性，温度 $\alpha$ 调节探索与利用的权衡：$\alpha\to0$ 时策略退化为贪婪选择，$\alpha$ 较大时倾向于均匀探索。

### 时序差分学习与目标网络

训练采用并行 Q 网络（PQN，Parallel Q‑Network），结合指数移动平均更新的目标网络 $\theta'$ 和 $\lambda$‑回报以实现稳定、低方差的值估计。从目标网络计算状态价值使用 LogSumExp 形式：

$$
V_{\theta'}(s_{t}) = \alpha \log\sum_{a\in\mathcal{A}_{t}}\!\exp\!\Bigl(\frac{Q_{\theta'}(s_{t},a)}{\alpha}\Bigr). \tag{5}
$$

在线策略生成轨迹后，Q 网络通过最小化当前估计与 $\lambda$‑回报 $G_{t}^{\lambda}$ 的均方误差进行优化：

$$
\mathcal{L}_{Q} = \mathbb{E}\Bigl[\bigl(Q_{\theta}(s_{t},a_{t}) - G_{t}^{\lambda}\bigr)^{2}\Bigr]. \tag{6}
$$

$\lambda$‑回报混合了多步经验，减少了偏差–方差权衡的压力，而目标网络的慢速更新（指数移动平均）进一步防止了值函数的震荡。消融实验证实，移除目标网络会使 32K 上下文下的支持事实检索 F1 从 97.1 骤降至 75.9，而移除熵正则化（软 Q）也会导致显著退化，说明这两个模块对稳定学习不可或缺。

### 相对位置编码

为让检索代理具备时间推理能力，Q‑RAG 引入基于已检索事实区间的相对位置编码。对于原始文档中索引为 $i$ 的片段，其相对位置通过以下映射计算：

$$
\rho_{t}(i) = j\,\delta + \ell\,\frac{i - b_{j}}{\,b_{j+1} - b_{j}\,}, \tag{7}
$$

其中 $b_{j}$ 表示第 $j$ 个已选片段的原始起始/结束边界，$\delta$ 和 $\ell$ 为可学习参数（或预设超参）。该映射将全局位置压缩到多个区间内，并保留区间内的相对顺序。最后，动作嵌入器中的绝对位置参数被替换为相对位置：

$$
E_{a}(a^{i},\,i;\theta_{2}) \;\Rightarrow\; E_{a}\!\bigl(a^{i},\,\rho_{t}(i);\theta_{2}\bigr). \tag{8}
$$

这一设计使得代理能够感知候选片段与已有证据之间的先后、邻近关系，从而在需要长程因果或时序推理的超长文档任务（如 BabiLong QA3）中实现几乎无退化的性能。

## 实验与分析

### 主实验结果

**超长上下文多步推理（BabiLong）**  
Q‑RAG 在 BabiLong 的 QA3 子任务上展现出几无退化的性能：当上下文从 1K token 扩展至 10M token 时，答案准确率始终保持在约 0.95，而最强的微调基线 ARMT 在相同条件下骤降至 ~0.37（Figure 2b）。在所有任务（QA1–QA5）的平均表现上，Q‑RAG 同样显著优于其他微调方法，且随着上下文增长优势持续扩大（Figure 2a）。这一结果表明，通过嵌入器的价值学习进行多步检索能够有效处理对时序感知和长推理链要求最高的场景，避免循环记忆型 Transformer 在超长序列上的灾难性遗忘。

![[assets/figures/papers/iclr26_0016_MS9nWFY7LG_Q-RAG_Long_Context_MultiStep_Retrieval_via_Value/figures/003_Figure_2.jpg]]
*Figure 2: Comparison of answer accuracy on the long-context benchmark BabiLong. Solid lines denote methods fine-tuned on the BabiLong, while dashed lines denote zero-shot methods. a) Average performance across tasks Q1–QA5. b) Performance on the hardest task, QA3, which requires the longest reasoning chain and temporal awareness*

**极致上下文寻针（RULER NIAH）**  
在 RULER 基准的全部 “大海捞针”（needle‑in‑a‑haystack, NIAH）子任务上，Q‑RAG 取得了接近完美的准确率：4K 上下文下平均准确率 100%，1M 上下文下为 99.7%，且未观察到随长度增加的性能退化（Table 1）。这得益于嵌入器仅在 4K 文档上训练却可无缝泛化至 1M token 的推理长度，无需位置编码外推或额外微调。

![[assets/figures/papers/iclr26_0016_MS9nWFY7LG_Q-RAG_Long_Context_MultiStep_Retrieval_via_Value/figures/004_Table_1.jpg]]
*Table 1: Results on the RULER benchmark, evaluating long-context retrieval performance across various context lengths. S (Single-needle): Find one value for one key. MK (Multi-keys): Find one value for one key among many. MV (Multi-values): Find all values for one key. MQ (Multi-query): Answer multiple questions over the context. MH QA: open domain multi-hop question answering. SH QA: single-hop question answering*

**开放域多跳问答（HotPotQA / Musique）**  
在 HotPotQA 上，Q‑RAG 的事实检索 F1 达到 0.93，与当前最优的 Beam‑Retriever（0.97）差距微小，且大幅超过其他基线（Table 2）。更重要的是，在分布外（OOD）数据集 Musique 上，Q‑RAG 的事实检索 F1（0.71）与需要完整微调 LLM 的 Search‑R1 并列最优，超过 Beam‑Retriever 近 10 个百分点，展现出极强的泛化能力。需要注意的是，Beam‑Retriever 在评估时被明确告知金标跳数，而 Q‑RAG 仅使用固定的最大步数 $T$，因此 Q‑RAG 在更严格的条件下仍取得了有竞争力的结果。

![[assets/figures/papers/iclr26_0016_MS9nWFY7LG_Q-RAG_Long_Context_MultiStep_Retrieval_via_Value/figures/005_Table_2.jpg]]
*Table 2: Comparison of methods on HotPotQA and Musique benchmarks. Bold text and underline denote the best and second best scores respectively*

**RULER 多跳与单跳问答**  
对于 RULER 中的多跳问答（MH QA），Q‑RAG 在 1M token 上下文时将准确率维持在 61%，显著高于 LongRoPE2‑8B 在 128K 时的 56% 以及其他记忆型基线（Table 1）。然而，单跳问答（SH QA）性能从 4K 时的 62% 随长度逐渐下降至 1M 时的 52%，表明模型在超长上下文中定位单个证据仍存在困难，这可由其训练信号主要依赖多跳支持事实组合的特点所解释。

**训练效率与收敛**  
在单张 A100‑80GB GPU 上，Q‑RAG 的训练约需 12 小时即可收敛（Figure 6），且学习曲线呈现快速上升后平稳，相比需要 8×A100 进行 LLM 微调的方法（如 Search‑R1）在资源公平性上具有数量级优势。

![[assets/figures/papers/iclr26_0016_MS9nWFY7LG_Q-RAG_Long_Context_MultiStep_Retrieval_via_Value/figures/022_Figure_6.jpg]]
*Figure 6: Learning curves for HotPotQA and BabiLong QA3 runs. Both graphs the average episodic return with respect to training time*

### 消融实验

**软 Q 函数与目标网络**  
移除最大熵框架（即 soft‑Q 中的熵正则化）导致 BabiLong QA3 在 32K 上下文上的支持事实检索 F1 从 97.1 降至 94.5，且方差明显增大（Table 3）。更严重的是，去掉目标网络（target network）后，F1 骤降为 75.9 且标准差高达 1.83，说明基于指数移动平均的稳定化机制对价值学习至关重要。

![[assets/figures/papers/iclr26_0016_MS9nWFY7LG_Q-RAG_Long_Context_MultiStep_Retrieval_via_Value/figures/009_Table_3.jpg]]
*Table 3: Ablation results on BabiLong QA3. Table shows F1 score for support facts retrieval. All values are averaged over 3 runs with different seeds*

**检索步数敏感性**  
在 HotPotQA 上将最大检索步数从 2 增至 3 时，Facts EM 从 0.832 跃升至 0.935，验证了多步检索对召回完整支持事实的必要性；进一步增加步数主要改善召回，但可能轻微牺牲 F1（Table 4）。这一趋势在不同规模的生成器（Qwen3‑4B 至 32B）上均一致，表明多步检索策略本身是性能提升的主因。

**超参数 α 与 λ 的鲁棒性**  
熵系数 α 与 λ‑回报参数 λ 在较宽区间内对最终性能影响平滑，不存在尖锐的最优点（Figure 3a, b），这有利于实际部署时的超参数选择。推理时间随上下文长度线性增长，符合 $O(N)$ 的理论复杂度（Figure 3c）。

**对比冻结嵌入器基线**  
使用预训练嵌入器直接进行多步检索（不进行 RL 微调）的基线在 BabiLong QA3 上的 F1 极低（Table 3 中未列出数值但被标注为性能最差），证实基于价值学习的嵌入器训练是 Q‑RAG 性能的核心驱动力，而非简单的检索框架选择。

### 早期停止机制的有效性分析

Q‑RAG 利用 Q 值的幅度实现自发的早期停止：当所有候选动作的 Q 值均低于某个阈值时，代理认为已收集足够证据并终止检索。在 HotPotQA 与 BabiLong QA2 上，通过调节阈值可在早停错误和晚停错误之间取得良好的折衷（Figure 4）。ROC 曲线显示，简单的 Q 值阈值规则在 HotPotQA 上能取得 0.95+ 的 TPR 和低于 0.05 的 FPR，在 BabiLong QA2 上完美停止率可超过 99%（Figure 5 / Table 5 6）。不过，最优阈值因任务而异，尚缺乏免标定的自适应机制。

### 失败模式与局限性

尽管 Q‑RAG 在多数长上下文基准上表现突出，其局限性同样值得关注：

1. **单跳检索在极端长度下衰退**：如前所述，RULER SH QA 在 1M token 时准确率降至 52%。推测原因在于单跳问题仅需一个证据片段，而 Q‑RAG 的训练奖励完全基于支持事实的组合信号，导致模型在“多步才是必要”的设定下被过度偏向。
2. **对金标支持事实的依赖**：当前训练仅依赖终端奖励（检索到的支持事实是否与金标一致），未引入 LLM 反馈或直接优化下游答案质量。这限制了在缺乏精确证据标注的数据集上的直接应用，且可能使模型对边缘检索错误不够鲁棒。
3. **早期停止的阈值需人工标定**：Q 值阈值的选择需要针对任务特性进行网格搜索或使用少量验证数据，缺乏自适应的停止决策模块。高阈值可能导致过早起停，低阈值则浪费计算，两者都会损害最终答案精度。
4. **跨语言与跨模态泛化未验证**：所有实验均基于英文数据集（BabiLong、HotPotQA、Musique、RULER），且仅使用中等规模嵌入器（如 multilingual‑e5‑large、contriever）；在更大或最新嵌入器、非英语语言以及非文本模态上的行为尚不明确。
5. **生成器能力依赖**：尽管 Q‑RAG 显著提升了事实证据的召回，最终答案生成仍由外部 LLM 完成（QwQ‑32B 或 Qwen3‑4B）。检索与生成的分离限制了整体误差的联合优化，在开放式问答中可能留下潜在的性能天花板。

### 与基线的公平性说明

为便于对照，本文对部分无法亲自复现的基线分数（如 Search‑R1、RAG‑RL）直接用原始论文数据标识（“◦”），并保持生成器一致。然而，Beam‑Retriever 被提供金标跳数，而 Q‑RAG 使用固定最大步数，这种信息不对等可能使 Beam‑Retriever 在 HotPotQA 上的优势被轻微高估。此外，Q‑RAG 在消费级 GPU 上的训练成本（≤12 h / A100‑80GB）与需要大规模并行训练的 LLM 微调方法形成鲜明对比，在资源受限环境下具有极强的实用性优势。总体而言，以上因素不会削弱 Q‑RAG 在长上下文多步检索领域建立的新效能基线。

## 方法谱系与知识库定位

### 与现有基线的关系

Q‑RAG 将多步检索形式化为有限时域马尔可夫决策过程（MDP），其核心差异在于**仅微调嵌入器而非微调大型语言模型（LLM）**：状态嵌入器 $E_s$ 与动作嵌入器 $E_a$ 通过最大熵强化学习在线更新，而 LLM 完全冻结。这直接区别于两类代表性基线——基于 LLM 微调的搜索范式（Search‑R1 通过 GRPO 微调 LLM 生成中间搜索查询；Beam‑Retriever 通过 Transformer 重排序器进行轨迹评分）与基于图构建或循环记忆的长上下文方法（GraphReader、Titans、Atlas、ARMT）。

在**训练对象**上，Q‑RAG 的对立面是以 Search‑R1 和 Re‑Plug 为代表的方法：后者冻结嵌入器、微调 LLM，而 Q‑RAG 冻结 LLM、只训练嵌入器（Section 1）。这使其训练成本大幅下降（约 12 小时 / 单张 A100‑80GB），对比 LLM 微调通常需要 8×A100 的资源，具有显著的资源公平性优势。

在**学习范式**上，Beam‑Retriever 使用监督式轨迹克隆，而 Q‑RAG 采用**最大熵时序差分学习（PQN + λ‑return）**，并通过玻尔兹曼策略（Eq.3）和软 Q 函数（Eq.1‑2）维持探索。这一转变在分布外数据上带来实质收益：Musique（OOD）上 Q‑RAG 的 Fact F1 达到 0.71，远超 Beam‑Retriever（0.61）并与 Search‑R1 持平，同时无需访问 LLM 生成评分（Table 2）。消融实验进一步证实软 Q 函数（熵正则化）与目标网络对稳定学习的必要性——移除软 Q 后 BabiLong QA3 的 32K 上下文 F1 从 97.1 降至 94.5，移除目标网络后更是暴跌至 75.9 且方差剧烈增大（Table 3）。

在**位置编码**上，Q‑RAG 引入基于已检索事实分区的相对位置编码（Eq.6‑7），使代理能够利用候选片段与已提取证据的空间关系进行时序推理。这使其在长叙事任务（BabiLong QA3，10M token）上几乎无性能退化（准确率 ~0.95），而对比的循环/记忆增强基线（ARMT 等）则退化至 ~0.37（Figure 2b）。

总之，Q‑RAG 站在两类方法的交叉点上：它同时克服了 LLM 微调路线的昂贵训练开销和基于图/记忆方法在超长上下文中的性能衰减，通过仅训练嵌入器实现与 SOTA 相当甚至更优的检索精度。

### 适用边界与性能缺口

Q‑RAG 的强适用场景清晰：**超长上下文中的事实检索与寻针（NIAH）任务**。在 RULER 基准的所有 NIAH 子任务上（4K–1M token），Q‑RAG 达到近乎完美的准确率（4K 时平均 100%，1M 时 99.7%），且未观察到长度退化（Table 1）。在 BabiLong 的 1–10M token 上下文中，其平均性能在所有微调方法中最高，尤其在需要最长推理链的 QA3 子任务上形成绝对优势（Figure 2）。在多步推理方面，Q‑RAG 于 1M 长度的 RULER 多跳 QA 上仍保持 61% 的准确率，超越同长度下其他架构（如 Mamba2‑Hybrid 约 48.8%@4K，LongRoPE2‑8B 56%@128K），说明其多步检索机制能有效缓解注意力分散。

性能缺口同样明确：
1. **In‑distribution 上的多步事实检索**：在 HotPotQA 上，Q‑RAG 的 Fact F1（0.93）略低于 Beam‑Retriever（0.97）（Table 2）。该差距可部分归因于公平性差异——Beam‑Retriever 评估时被告知金标跳数，而 Q‑RAG 使用固定最大步数 $T$。此外，Beam‑Retriever 在训练域内采用重排序器进行逐轨迹评分，对已知分布拟合更紧密。
2. **极端长度下的单跳 QA**：Q‑RAG 在 RULER 的单跳 QA 准确率从 4K 时的 62% 降至 1M 时的 52%（Table 1），表明当任务仅需一次检索时，多步框架的额外步骤可能引入干扰。
3. **生成质量依赖外部 LLM**：Q‑RAG 的端到端答案生成依赖 QwQ‑32B 等外部模型，检索与生成未联合优化，因此在答案语义一致性上的提升受限于生成器能力。

适用边界还体现在数据假设上：训练依赖金标支持事实作为终端奖励，因此在无结构化事实标注的开放式场景中，当前设计无法直接迁移。

### 局限

1. **奖励信号单一**：当前仅使用支持事实的匹配作为奖励，未引入 LLM 反馈（例如生成质量或答案置信度）。这限制了在缺少金标支持事实的场景（如对话式多步检索）中的应用潜力。
2. **早期停止阈值需手动标定**：基于 Q 值阈值的停止策略虽有效，但其阈值得针对不同任务/数据集单独校准（Figure 4、Table 5‑6），缺乏自适应机制。
3. **嵌入器规模探索有限**：实验主要使用中等规模嵌入器（multilingual‑e5‑large、contriever），更大或最新的嵌入器能否进一步释放性能未被验证。
4. **跨语言泛化空白**：所有训练与评估均在英文数据集上进行，其他语言的泛化性未知。
5. **长期稳定性与鲁棒性未深究**：虽然训练曲线快速收敛（Figure 6），但对噪声标签的鲁棒性和部署后的分布漂移影响未作分析。
6. **端到端联合优化缺位**：检索与生成分离，整体系统无法根据最终答案质量反向传播梯度，限制了信息瓶颈的自动发现。

### 开放问题

- **LLM 反馈奖励**：如何利用结构化 LLM 反馈（如生成合理性评分、事实一致性信号）构建奖励，使嵌入器无需金标支持事实即可进行强化学习？
- **嵌入空间中的高阶推理**：能否在嵌入计算中直接强化组合推理能力（例如通过张量分解或关系旋转），而非仅靠位置编码间接辅助时序推理？
- **亚线性时间推理**：能否引入近似 kNN 或分层索引技术，使 Q‑RAG 在保持嵌入内积效率的同时，实现与上下文长度的亚线性推理时间，从而支持万亿 token 级别文档？
- **检索‑生成紧密耦合**：如何在保持推理效率的前提下，将策略梯度从生成器回传至检索代理，实现端到端优化？
- **跨模态多步推理**：Q‑RAG 的 MDP 框架与嵌入空间值函数机制是否可迁移至图像、表格等多模态证据的迭代检索任务？

## 原文 PDF

![[paperPDFs/ICLR_2026/Q_RAG_Long_Context_MultiStep_Retrieval_via_ValueBased_Embedder_Training.pdf]]
