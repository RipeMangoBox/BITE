---
title: "Triple-BERT: Do We Really Need MARL for Order Dispatch on Ride-Sharing Platforms?"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Triple_BERT_Do_We_Really_Need_MARL_for_Order_Dispatch_on_Ride_Sharing_Platforms.pdf
project_link: null
code_link: https://github.com/RS2002/Triple-BERT
openreview_forum_id: symgW6FhA6
aliases:
- TB
- Triple-BERT
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将调度问题建模为集中式单智能体强化学习（SARL），通过动作分解策略将巨量联合动作空间转化为单个司机选择概率的乘积，并利用BERT自注意力机制捕获司机与订单间的全局关系，从而绕开MARL的合作难题与维度灾难。"
primary_logic: "订单调度本质上是集中决策问题，采用SARL可直接使用全局状态，避免多智能体信用分配与非稳态；配合参数高效的BERT结构和QK-attention，使集中式SARL足以应对大规模观测与行动空间，并超过精心设计的MARL方法。"
claims:
- "Triple-BERT在曼哈顿真实打车数据集上相较现有最先进方法（DeepPool等）综合提升约11.95%。"
- "多时段平均性能中，Triple-BERT在奖励（14730.48）、服务率（0.98）和取车时间（5.73分钟）上均显著优于所有基线方法。"
- "消融实验证实两阶段训练和QK-attention正归一化对模型性能至关重要；去除位置嵌入可改善泛化能力。"
- "Manhattan Yellow Taxi (多个时段，19:00‑19:30) 上 Average Reward = 14730.48"
---

# Triple-BERT: Do We Really Need MARL for Order Dispatch on Ride-Sharing Platforms?

> [!tip] 核心洞察
> 订单调度本质上是集中决策问题，采用SARL可直接使用全局状态，避免多智能体信用分配与非稳态；配合参数高效的BERT结构和QK-attention，使集中式SARL足以应对大规模观测与行动空间，并超过精心设计的MARL方法。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Triple-BERT：网约车订单调度是否真正需要多智能体强化学习？ |
| 英文题名 | Triple-BERT: Do We Really Need MARL for Order Dispatch on Ride-Sharing Platforms? |
| 会议/期刊 | ICLR 2026 (Oral) |
| Links | [paper](https://openreview.net/forum?id=symgW6FhA6) · [GitHub](https://github.com/RS2002/Triple-BERT) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Triple-BERT |
| Dataset | Manhattan Yellow Taxi (多个时段，19:00‑19:30), Manhattan Yellow Taxi (多个时段), Manhattan FHV Data |

> [!tip] 效果简介
> - Manhattan Yellow Taxi (多个时段，19:00‑19:30) 上，Average Reward 为 14730.48，对比 DeepPool: 14570，变化 +160.48 (1.1%)，但与BMG‑Q等差距更大。
> - Manhattan Yellow Taxi (多个时段) 上，Service Rate 为 0.98 (98%)，对比 DeepPool: 0.96，变化 +0.02 (2.1%)。
> - Manhattan Yellow Taxi (多个时段) 上，Pickup Time (minutes) 为 5.73，对比 DeepPool: 7.58，变化 -1.85 (24.4%)。

## 概要

网约车订单调度面临一个根本性瓶颈：**维度灾难（Curse of Dimensionality, CoD）**。现有方法多采用多智能体强化学习（MARL），其中独立MARL因缺乏全局协调而合作性差，集中训练分散执行（CTDE）MARL则因集中式评价器遭遇维度爆炸，导致收敛缓慢、性能次优。

Triple-BERT 的核心洞察在于：**订单调度本质上是集中决策问题**，采用集中式单智能体强化学习（SARL）可直接使用全局状态，从根本上绕开多智能体的信用分配与非稳态难题。为应对SARL面临的巨量观测与动作空间，该方法引入三项关键设计：

- **动作分解策略**：将联合动作概率建模为每个司机独立选择订单概率的乘积，配合二分图整数线性规划（ILP）求解，将指数级动作空间转化为可处理的线性规模。
- **BERT自注意力架构**：利用参数共享的自注意力机制捕获司机与订单间的全局交互关系，避免参数随规模线性膨胀。
- **QK-Attention正归一化**：以两个小型网络近似大型网络，并通过非负归一化稳定训练，将乘法复杂度转为加法复杂度。

在曼哈顿真实打车数据集上，Triple-BERT 相较现有最优方法综合提升约 **11.95%**。多时段平均性能中，服务率达到 **0.98**，取车时间降至 **5.73分钟**（较DeepPool降低24.4%），奖励达 **14730.48**，在所有核心指标上均显著超越独立MARL和CTDE MARL基线。消融实验进一步证实，两阶段训练（IDDQN预训练 + 集中式TD3微调）和QK-Attention正归一化对模型收敛与性能至关重要，而去除位置嵌入则增强了模型在不同订单规模下的泛化能力。

**方法定位**：Triple-BERT 属于集中式SARL调度框架，通过动作分解与BERT架构解决大规模观测与动作空间问题，在方法谱系上区别于独立MARL（如DeepPool、BMG-Q）、CTDE MARL（如HIVES、Enders et al.）以及值分解MARL（如CEVD）等路线。



### 网约车订单调度的核心挑战

网约车平台需要在每个决策时刻将空闲司机与待服务订单进行实时匹配，这一调度问题本质上是一个大规模序列决策问题。其核心难点在于**维度灾难（Curse of Dimensionality, CoD）**：随着司机和订单数量的增长，联合动作空间呈指数级膨胀。具体而言，当存在 $n$ 个司机和 $m_t$ 个订单时，动作空间的下界为：

$$|A_t| \geq (n - m_t + 2)^{m_t} \geq 2^{m_t}$$

这意味着即使在中等地规模场景下，枚举所有可能的司机-订单分配方案也是不可行的。

### 现有MARL方法的困境

近年来，多智能体强化学习（Multi-Agent Reinforcement Learning, MARL）被广泛用于解决订单调度问题，但现有方法普遍受困于维度灾难：

- **独立MARL方法**（如 **DeepPool**、**BMG-Q**）：每个司机作为独立智能体学习各自的Q值函数，虽然避免了联合动作空间的组合爆炸，但由于缺乏全局协调机制，智能体之间合作性差，容易导致次优分配。
- **集中训练分散执行（CTDE）方法**（如 **HIVES**、**Enders et al.** 的MASAC框架）：通过集中式评论家（Critic）网络获取全局信息来指导训练，但集中式评论家本身需要处理所有智能体的联合状态-动作空间，导致网络参数随智能体数量急剧膨胀，遭遇维度爆炸，收敛缓慢且性能难以达到最优。
- **值分解方法**（如 **CEVD**）：尝试将全局值函数分解为个体值函数的组合，但在复杂调度场景下，分解假设往往不成立，限制了合作效果。

### 关键洞察：调度本质是集中决策问题

本文的核心洞察在于：**订单调度本质上是一个集中式决策问题**。平台拥有全局状态信息（所有司机位置、订单分布、交通状况等），且最终分配决策是集中做出的。采用多智能体框架人为引入了智能体之间的信用分配（credit assignment）难题和非稳态（non-stationarity）问题，而这些问题在集中式单智能体强化学习（Single-Agent RL, SARL）框架下天然不存在。

然而，直接将SARL应用于大规模调度面临两个关键障碍：
1. **巨量观测空间**：集中式智能体需要同时处理所有司机和订单的状态信息，输入维度极高。
2. **巨量动作空间**：联合动作空间随司机-订单对数量呈组合爆炸，传统SARL无法直接输出有效的联合动作。

### 本文动机与解决思路

针对上述困境，本文提出 **Triple-BERT**，一个专为大规模订单调度设计的集中式SARL框架。其核心思路是通过三项关键技术绕开MARL的合作难题与维度灾难：

- **动作分解策略**：将联合动作概率分解为每个司机独立选择订单概率的乘积，将组合优化问题转化为可求解的二分图匹配问题，从根本上规避了动作空间的指数爆炸。
- **BERT自注意力架构**：利用Transformer的全局自注意力机制捕获司机与订单之间的复杂交互关系，同时通过参数复用（parameter reuse）控制网络规模随司机/订单数量的增长。
- **QK-Attention高效计算**：设计轻量级的QK-Attention模块替代传统的大矩阵乘法，将计算复杂度从乘法级降至加法级，使集中式SARL在实际规模下可训练、可部署。



## 核心方法与创新机理

### 从多智能体到集中式单智能体的范式转换

Triple-BERT 的核心创新在于对网约车订单调度问题的根本性重新建模。现有方法普遍将调度视为多智能体强化学习（MARL）问题，每个司机作为一个独立智能体进行决策。然而，这一范式面临两个结构性困境：

- **独立 MARL**（如 DeepPool、BMG-Q）中，各智能体仅基于局部观测独立决策，缺乏全局协调机制，导致合作性差、整体效率低下。
- **集中训练分散执行（CTDE）MARL**（如 HIVES、Enders et al.、CEVD）虽引入集中式评价器以促进合作，但评价器需处理所有智能体的联合状态与动作，其输入维度随司机数量呈指数增长，遭遇维度灾难（Curse of Dimensionality），导致收敛缓慢且性能次优。

Triple-BERT 的核心洞察是：**订单调度本质上是一个集中决策问题**——平台拥有全局状态信息，且所有司机的调度决策天然应由中心统一协调。基于此，该方法将问题重新建模为**集中式单智能体强化学习（SARL）**，以单一策略直接输出所有司机的联合调度方案。这一范式转换从根本上绕开了 MARL 中的信用分配与非稳态难题，使策略能够直接利用全局状态进行优化。

### 动作分解：化解指数级联合动作空间

集中式 SARL 面临的首要挑战是动作空间的维度爆炸。当 $n$ 个司机面对 $m$ 个订单时，联合动作空间的下界为 $(n - m + 2)^m$（见 Appendix A），随订单数呈指数增长，传统的直接枚举或联合动作采样策略在此规模下完全不可行。

Triple-BERT 提出的**动作分解策略**是解决这一瓶颈的关键。其核心思想是将联合动作概率 $\pi_{\Theta}^T(A_t | S_t)$ 分解为各司机独立选择订单概率的乘积形式：

$$\pi_{\Theta}^T(A_t | S_t) = \mathsf{z}\left(\prod_{i,j \in \mathrm{h}(A_t)} \mathcal{P}_{i,j,t}\right)$$

其中 $\mathcal{P}_{i,j,t}$ 表示司机 $i$ 选择订单 $j$ 的概率。基于这一分解，贪心动作选择等价于最大化所选司机-订单对的 log 概率之和：

$$\arg\max_{A_t \in \psi(S_t)} \sum_{i,j \in \mathsf{h}(A_t)} \log \mathcal{P}_{i,j,t}$$

该优化问题可高效地通过二分图整数线性规划（ILP）求解，将指数级动作空间的探索转化为对概率矩阵 $\mathcal{P}_t$ 的学习与约束优化。这一设计使集中式 SARL 在大规模场景下的决策成为计算上可行的。

### BERT 架构与 QK-Attention：高效捕获全局交互

为处理包含大量司机与订单的高维观测空间，Triple-BERT 引入了基于 BERT 的网络架构，其设计围绕两个关键原则：

**参数效率**：传统全连接网络或 GNN 在处理可变规模的司机-订单集合时，参数量随数量线性甚至超线性增长。BERT 的自注意力机制通过参数共享，使网络参数量与输入规模解耦，有效控制了模型复杂度。

**全局关系建模**：Actor-BERT 将所有司机和订单的编码特征拼接为一个序列，通过多头自注意力机制一次性捕获所有司机之间、订单之间以及司机-订单之间的全局交互关系。值得注意的是，由于输入序列具有置换不变性，该方法**省略了位置嵌入**，消融实验证实这一设计不仅未损害性能，反而提升了模型在不同订单数量下的泛化能力（Table 9）。

在生成司机-订单效用矩阵时，Triple-BERT 采用了**QK-Attention-Norm** 模块替代传统的全连接评分网络：

$$\mathrm{QK\text{-}Attention\text{-}Norm}(\overline{w}_{i,t}, \overline{o}_{j,t}) := \mathbf{f}(\overline{w}_{i,t}; \theta_f) \cdot \frac{\mathrm{Softplus}(\mathbf{g}(\overline{o}_{j,t}; \theta_g))^T}{||\mathrm{Softplus}(\mathbf{g}(\overline{o}_{j,t}; \theta_g))||_2}$$

该设计具有双重优势：首先，通过两个小型网络 $\mathbf{f}$ 和 $\mathbf{g}$ 近似大型评分网络，将乘法复杂度转化为加法复杂度，显著降低计算开销；其次，对 $\mathbf{g}$ 的输出施加 Softplus 非负化与 L2 归一化，确保效用矩阵元素非负且范数稳定，缓解了参数冗余问题并大幅提升训练稳定性。消融实验表明，去除该归一化会导致模型性能劣于所有基线方法，验证了其对稳定训练的关键作用。

### 两阶段训练：突破样本稀缺瓶颈

集中式 SARL 在训练初期面临严重的样本稀缺问题：随机策略下，巨大的动作空间中极难采样到有效调度方案，导致学习信号稀疏。Triple-BERT 提出的**两阶段训练策略**有效应对了这一挑战：

- **第一阶段（预训练）**：采用独立 DQN（IDDQN）以分布式方式训练特征提取器（Worker Encoder 与 Order Encoder）。IDDQN 基于司机独立决策的简化假设，虽非最优策略，但能快速收敛并为特征提取器提供有效的初始化。
- **第二阶段（微调）**：冻结预训练的特征提取器，基于集中式 TD3 框架微调 Actor-BERT 与 Critic-BERT。此时特征提取器已具备基本的订单-司机匹配判别能力，使集中式策略能够在有意义的特征空间中进行探索与优化。

消融实验（Figure 3）提供了决定性证据：仅使用第二阶段训练（无 IDDQN 预训练）时，模型完全无法收敛，奖励持续下降并伴随剧烈震荡。这证实了两阶段训练并非可选的工程技巧，而是使集中式 SARL 训练成为可能的必要条件。值得注意的是，独立性假设仅在第一阶段预训练中使用，微调后的集中式框架不再依赖该假设。

### 与基线方法的创新差异总结

| 创新维度 | 基线方法 | Triple-BERT |
|---------|---------|-------------|
| **强化学习框架** | 多智能体（独立或 CTDE） | 集中式单智能体 SARL |
| **动作空间处理** | 直接评估司机-订单对或联合动作采样 | 动作分解为概率乘积 + ILP 求解 |
| **网络架构** | GNN / Q-网络 / MLP | BERT 自注意力 + QK-Attention-Norm |
| **训练策略** | 单阶段端到端训练 | IDDQN 预训练 + 集中式 TD3 微调 |

这些创新并非孤立的技术改进，而是围绕“集中式 SARL 能否替代 MARL”这一核心问题形成的系统性方案：范式转换提供了理论可行性，动作分解与 BERT 架构解决了计算可行性，两阶段训练保障了优化可行性。三者的协同使 Triple-BERT 在曼哈顿真实打车数据集上相较现有最先进方法综合提升约 11.95%，并在服务率、取车时间等关键运营指标上全面超越所有 MARL 基线。



![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_symgW6FhA6/figures/002_Figure_2.jpg]]
*Figure 2: Network Architecture: The network consists of three main components: the feature extractor, the actor sub-network, and the critic sub-network. First, a worker encoder and an order encoder are used to extract features from individual worker and order information, respectively. Then an Actor BERT model captures the relationships between them and a QK-Attention module calculates the selection probabilities for each worker-order pair. Finally, the fused features of the selected worker-order pairs are input into two separate Critic BERT models for further information extraction, and two Critic MLPs compute the Q-values, as TD3 requires two critics. (In this figure, the fused sequence (input to C...*

Triple‑BERT 是一个集中式单智能体强化学习（SARL）框架，专为大规模网约车订单调度设计。其核心思路是将调度问题建模为集中决策任务，通过动作分解策略将指数级联合动作空间转化为单个司机选择概率的乘积，并利用参数高效的 BERT 架构捕获司机与订单间的全局交互关系，从而绕开多智能体强化学习（MARL）面临的维度灾难与合作难题。

### 系统工作流

整体调度流程如 **Figure 1** 所示。在每个时间步，系统首先根据上一时间步的分配结果更新司机池和订单池的状态：订单池加入新到达的订单并移除超时订单。随后，Triple‑BERT 对当前状态进行全局评估，输出每个司机‑订单对的效用矩阵，并通过整数线性规划（ILP）求解最大化全局分配概率的匹配方案。

### 网络架构总览

Triple‑BERT 的网络结构由三大组件构成（**Figure 2**），形成一条端到端的信息处理管线：

1. **特征提取器（Feature Extractor）**  
   包括司机编码器（Worker Encoder）和订单编码器（Order Encoder），分别将单个司机的状态信息和单个订单的信息编码为统一维度的特征向量。编码器内嵌自适应重加权层（Adaptive Re‑weighting Layer, ARL）和归一化层，以增强特征表达并促进收敛。

2. **Actor 子网络**  
   由 Actor‑BERT 和 QK‑Attention‑Norm 模块组成。Actor‑BERT 对所有司机和订单的编码特征进行自注意力计算，捕获全局交互关系；QK‑Attention‑Norm 在此基础上生成司机‑订单效用矩阵，并通过正归一化保证训练稳定性。该子网络的核心作用是执行动作分解：将联合动作概率建模为各司机选择订单概率的乘积。

3. **Critic 子网络**  
   包括两个独立的 Critic‑BERT 和两个 Critic‑MLP。Critic‑BERT 对已选动作对应的司机‑订单融合特征进行二次全局信息提取，Critic‑MLP 将 BERT 输出映射为 Q 值。双评论家结构遵循 TD3 算法设计，用于缓解 Q 值高估问题。

### 两阶段训练管线

Triple‑BERT 采用两阶段训练策略以解决样本稀缺和收敛困难：

- **第一阶段（IDDQN 预训练）**：在独立 MARL 假设下，使用 IDDQN 方法对司机编码器和订单编码器进行预训练，使其获得基本的特征提取能力。该阶段为后续集中式训练提供了良好的参数初始化。
- **第二阶段（集中式 TD3 微调）**：移除独立假设，将预训练的编码器接入完整的 Actor‑Critic 架构，基于 TD3 算法进行端到端集中式训练。Actor 通过近似策略梯度（式 7）优化，Critic 通过双 Q 网络损失（式 8）更新。探索通过向概率矩阵添加噪声实现，噪声越大策略越随机，噪声为零时退化为贪心策略。

消融实验表明，仅使用第二阶段训练（无预训练）会导致模型无法收敛、奖励持续下降（**Figure 3**），验证了两阶段训练的必要性。



### 特征提取器：司机编码器与订单编码器

Triple‑BERT 的特征提取器由两个独立的编码器构成，分别处理司机状态与订单信息，将异构原始输入映射为统一维度的特征向量。

**司机编码器（Worker Encoder）** 采用 LSTM + MLP 结构，将司机当前在途订单序列（含行程进度、目的地等时序信息）编码为固定长度的隐状态，再与其他非序列特征（如当前位置、空闲时长）拼接后通过 MLP 输出司机特征向量 $\overline{w}_{i,t}$。编码器内部集成了自适应重加权层（Adaptive Re‑weighting Layer, ARL），其形式为：

$$y = x \circ \Omega$$

其中 $x$ 为输入特征，$\Omega = \text{MLP}(x)$ 为通过小型网络学到的权重向量，$\circ$ 表示逐元素乘积。ARL 使网络能自适应地增强或抑制不同特征维度，提升特征提取质量。

**订单编码器（Order Encoder）** 为纯 MLP 结构，将订单的起点/终点坐标、已等待时间等属性映射为订单特征向量 $\overline{o}_{j,t}$，同样配备 ARL 层。

最终，所有司机和订单的特征被拼接为一个序列，作为后续 BERT 模块的输入：

$$\tilde{S}_t = [\tilde{w}_{1,t}, \tilde{w}_{2,t}, \ldots, \tilde{w}_{n,t}, \tilde{o}_{1,t}, \tilde{o}_{2,t}, \ldots, \tilde{o}_{m_t,t}]$$

其中 $n$ 为司机数量，$m_t$ 为 $t$ 时刻的待分配订单数量。

---

### Actor 子网络：Actor‑BERT 与 QK‑Attention‑Norm

Actor 子网络负责从全局特征序列中提取司机与订单间的交互关系，并生成每对司机‑订单的选择概率。

**Actor‑BERT** 是一个标准的 Transformer 编码器，对输入序列 $\tilde{S}_t$ 执行多头自注意力，使每个司机和订单的特征都能感知全局上下文。关键设计决策是**省略位置嵌入**——由于输入序列中的司机和订单天然具有排列不变性（permutation invariance），加入位置嵌入反而会引入虚假的顺序偏置。消融实验证实，去除位置嵌入后 Triple‑BERT 在不同订单数量下均获得更高奖励，且在未见过的订单规模上仍保持良好泛化。

**QK‑Attention** 模块将 Actor‑BERT 输出的司机特征 $\overline{w}_{i,t}$ 和订单特征 $\overline{o}_{j,t}$ 映射为标量效用值，其基础形式为：

$$\text{QK-Attention}(\overline{w}_{i,t}, \overline{o}_{j,t}) := \mathbf{f}(\overline{w}_{i,t}; \theta_f) \cdot \mathbf{g}(\overline{o}_{j,t}; \theta_g)^T$$

其中 $\mathbf{f}$ 和 $\mathbf{g}$ 是两个小型网络。这一设计的核心动机是**计算效率**：若直接用一个大型网络 $\mathbf{F}(\overline{w}_{i,t}, \overline{o}_{j,t}; \theta_F)$ 评估所有司机‑订单对，计算复杂度为 $\mathcal{O}(n \times m_t)$ 次完整前向传播；而 QK‑Attention 将 $\mathbf{f}$ 和 $\mathbf{g}$ 的输出预先计算并缓存，将乘法复杂度转化为加法复杂度，显著降低大规模场景下的推理开销。

**QK‑Attention‑Norm** 在此基础上引入正归一化以提升训练稳定性：

$$\text{QK-Attention-Norm}(\overline{w}_{i,t}, \overline{o}_{j,t}) := \mathbf{f}(\overline{w}_{i,t}; \theta_f) \cdot \frac{\text{Softplus}(\mathbf{g}(\overline{o}_{j,t}; \theta_g))^T}{\|\text{Softplus}(\mathbf{g}(\overline{o}_{j,t}; \theta_g))\|_2}$$

其中 $\text{Softplus}$ 确保 $\mathbf{g}$ 的输出非负，$\ell_2$ 归一化将其约束为单位范数。这一归一化缓解了 $\mathbf{f}$ 和 $\mathbf{g}$ 之间的参数冗余问题——若不加以约束，两个网络可能学到任意缩放互补的参数组合，导致梯度信号不稳定。消融实验证实，去除 QK‑Attention‑Norm 会使模型表现劣于所有基线方法。

---

### Critic 子网络：Critic‑BERT 与双 Critic‑MLP

Critic 子网络遵循 TD3 的双评论家架构，用于评估 Actor 所选动作的质量。其输入为动作函数 $\mathcal{A}$ 定义的序列：

$$\mathcal{A}(w_{i,t}) = \begin{cases} (\overline{w}_{i,t}, \overline{o}_{j,t}) & \text{若订单 } j \text{ 被分配给司机 } i \\ \emptyset & \text{否则} \end{cases}$$

即对于每个被分配的司机，将其特征与对应订单特征拼接；未分配订单的司机以空向量填充。该序列通过两个独立的 Critic‑BERT 进一步提取全局信息，再分别经 Critic‑MLP 映射为标量 Q 值 $\Omega_{\pi_\Theta^T,1}^{TD3}$ 和 $\Omega_{\pi_\Theta^T,2}^{TD3}$。

Critic 的损失函数为标准 TD3 形式：

$$L_C = \sum_{i=1,2} \mathbb{E}_{\pi_\Theta^T} \left[ \mathcal{Q}_{\pi_\Theta^T}^{TD3}(S_{t+1}, R_{t+1}; \Theta^-) - \Omega_{\pi_\Theta^T,i}^{TD3}(S_t, A_t; \Theta) \right]$$

其中 $\Theta^-$ 为目标网络参数，$\mathcal{Q}_{\pi_\Theta^T}^{TD3}$ 为双 Q 网络中较小者经目标策略平滑后的目标值。

---

### 动作分解与策略梯度

Triple‑BERT 的核心创新在于将联合动作空间分解为独立概率之积。令 $\mathcal{P}_{i,j,t}$ 表示司机 $i$ 选择订单 $j$ 的概率（由 QK‑Attention‑Norm 输出经 softmax 得到），则聚合策略定义为：

$$\pi_\Theta^T(A_t | S_t) = \mathsf{z}\left(\prod_{i,j \in \mathrm{h}(A_t)} \mathcal{P}_{i,j,t}\right)$$

其中 $\mathrm{h}(A_t)$ 为联合动作 $A_t$ 中所有被分配的司机‑订单对，$\mathsf{z}$ 为单调增函数。这一分解将原本随订单数指数增长的动作空间（下界为 $2^{m_t}$）压缩为 $\mathcal{O}(n \times m_t)$ 个独立概率的计算。

贪心动作选择等价于最大化对数概率之和，可通过二分图匹配的整数线性规划（ILP）高效求解：

$$\arg\max_{A_t \in \psi(S_t)} \pi_\Theta^T(A_t | S_t) = \arg\max_{A_t \in \psi(S_t)} \sum_{i,j \in \mathsf{h}(A_t)} \log \mathcal{P}_{i,j,t}$$

策略梯度采用基于优势函数的近似形式：

$$\nabla_\Theta \mathrm{J}(\Theta) \propto \mathbb{E}_{\pi_\Theta^T} \left[ (\mathbf{Q}_{\pi_\Theta^T}^{TD3}(S_t, A_t) - B) \nabla_\Theta \sum_{i,j \in \mathrm{h}(A_t)} \log \mathcal{P}_{i,j,t} \right]$$

其中 $B$ 为基线函数，$\mathbf{Q}_{\pi_\Theta^T}^{TD3}$ 为双 Critic 中较小者的 Q 值。该梯度形式将全局动作的信用分配自然地分解到各司机‑订单对的 log 概率上，绕开了多智能体强化学习中棘手的信用分配问题。



## 实验与关键发现

### 核心性能对比

Triple-BERT在曼哈顿真实打车数据集上展现了显著的性能优势。在多个时段（19:00–19:30）的平均性能评估中，Triple-BERT在所有关键指标上均超越现有最先进方法：

- **平均奖励**：Triple-BERT达到14730.48，相较DeepPool的14570提升约1.1%，但与BMG-Q等其他MARL基线的差距更为显著。
- **服务率**：Triple-BERT实现0.98（98%）的服务率，较DeepPool的0.96提升2.1%。
- **取车时间**：Triple-BERT将平均取车时间压缩至5.73分钟，较DeepPool的7.58分钟减少24.4%，这是用户体验改善最突出的指标。

在曼哈顿FHV数据集上，Triple-BERT的奖励达到14329.74，相较BMG-Q的12249.24提升17.0%，验证了集中式SARL架构在复杂城市环境中的优势。综合来看，Triple-BERT相较现有最先进方法实现约11.95%的综合提升，服务订单数增加4.26%，取车时间减少22.25%。

### 训练过程与收敛性分析

两阶段训练策略是Triple-BERT成功的关键。训练曲线（Figure 3）揭示了以下因果机制：

- **预训练的必要性**：仅使用第二阶段集中式TD3训练（无IDDQN预训练）时，模型完全无法收敛，奖励持续下降并伴随剧烈波动。这表明随机初始化的特征提取器无法为集中式策略优化提供有效的状态表征，预训练阶段通过独立DQN学习为后续全局优化奠定了表征基础。
- **QK-Attention正归一化的稳定性作用**：去除QK-Attention中的Softplus正归一化后，模型表现劣于所有基线方法。该归一化通过确保g网络输出非负且L2范数为1，缓解了参数冗余问题，防止训练过程中梯度不稳定导致的性能退化。
- **位置嵌入的泛化影响**：去除Actor-BERT中的位置嵌入后，Triple-BERT在不同订单数量下均获得更高奖励，且在未见过的订单规模上仍保持良好的泛化能力。这是因为司机-订单序列本质上是置换不变的，位置嵌入引入了虚假的顺序先验，干扰了自注意力机制对全局交互关系的捕获。

### 消融实验与架构分析

**编码器选择的影响**（Table 10）：基于ARL（自适应重加权层）的编码器显著提升了Triple-BERT及独立MARL方法的性能，但对CTDE（集中训练分散执行）MARL方法效果甚微。这一对比揭示了CTDE方法的瓶颈在于集中式评论家网络的维度灾难——即使改进了特征提取，评论家仍需面对指数级增长的联合动作空间，导致价值估计质量低下。


![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_symgW6FhA6/figures/015_Table_10.jpg]]
*Table 10: Reward of Different Methods Under Different Encoder*

**探索策略的鲁棒性**（Figure 4）：在概率矩阵上施加不同类型噪声（高斯噪声、均匀噪声、BSC噪声）均使Triple-BERT优于传统MARL方法，验证了动作分解策略对探索机制的鲁棒性。当噪声足够大时策略退化为完全随机策略，噪声为零时收敛至贪心策略，这种连续可调的探索机制为实践部署提供了灵活性。

### 跨场景泛化与效率分析

**不同城区的迁移能力**（Table 8）：在纽约皇后区数据集上，Triple-BERT的奖励为5577.83，相较BMG-Q的5362.00提升4.0%。与曼哈顿相比提升幅度较小，这是因为皇后区订单分布更为分散，各调度策略间的奖励差异本身较小，限制了探索效率。这暴露了集中式SARL在极度分散需求场景下的边际收益递减问题。


![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_symgW6FhA6/figures/013_Table_8.jpg]]
*Table 8: Performance of Different Methods in Queens, New York City*

**决策效率**（Table 7）：尽管BERT架构引入了额外计算，但QK-Attention通过将乘法复杂度转化为加法复杂度，使Triple-BERT在不同司机-订单规模下保持了可接受的决策时间，验证了架构设计对大规模部署的支撑能力。


![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_symgW6FhA6/figures/012_Table_7.jpg]]
*Table 7: Decision Time of Different Driver and Order Amounts (unit: seconds)*

### 失败模式与局限

1. **单点故障风险**：集中式SARL依赖全局状态信息，一旦通信中断或中心节点失效，整个调度系统将瘫痪。这是集中式架构固有的鲁棒性缺陷。
2. **两阶段训练复杂度**：预训练阶段需收集大量独立MARL样本，增加了训练时间和系统工程复杂度，限制了快速部署能力。
3. **极端分散场景的收益递减**：在订单密度低的区域，集中式全局优化的边际优势缩小，简单的独立策略可能已接近性能上限。
4. **优化目标单一**：当前框架仅优化订单调度，未考虑动态定价、车辆重定位等联合优化任务，限制了平台整体收益的提升空间。

### 补充图表

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_symgW6FhA6/figures/003_Table_1.jpg]]
*Table 1: Comparison of Different Ride Sharing Methods: Bold entries represent the best results*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_symgW6FhA6/figures/005_Table_2.jpg]]
*Table 2: Performance of Different Methods in Manhattan FHV Data*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_symgW6FhA6/figures/008_Table_3.jpg]]
*Table 3: Model Configurations*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_symgW6FhA6/figures/009_Table_4.jpg]]
*Table 4: Average Performance under Multiple Periods: Bold entries represent the best results*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_symgW6FhA6/figures/010_Table_5.jpg]]
*Table 5: Reward of Different Methods Under Different Days*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_symgW6FhA6/figures/011_Table_6.jpg]]
*Table 6: Reward of Different Methods During High Concurrency Period among Different Driver Amounts*

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_symgW6FhA6/figures/014_Table_9.jpg]]
*Table 9: Reward of Tripe-BERT w/ and w/o Positional Embedding (PE)*




## 定位与知识库关联

### 1. 问题瓶颈：多智能体强化学习的维度灾难与合作困境

订单调度在网约车平台中天然具有集中决策属性——平台需要同时考虑所有司机与订单的全局匹配，以最大化整体服务效率。然而，现有研究长期将这一问题建模为多智能体强化学习（MARL），由此引入了两个深层瓶颈：

- **独立MARL的合作性缺失**：如 **DeepPool**（独立DQN）和 **BMG-Q**（独立DQN + GAT邻居信息）将每个司机视为独立智能体，策略优化时仅考虑局部奖励。这导致司机间缺乏协调，在供需密集区域产生恶性竞争，整体服务率与收益受损。
- **CTDE MARL的维度爆炸**：集中训练分散执行（CTDE）范式（如基于QMIX的 **HIVES**、基于MASAC的 **Enders et al.**、基于值分解的 **CEVD**）试图通过集中式评价器引入全局信息。然而，集中式Critic的输入维度随司机和订单数量呈指数增长——动作空间下界为 $(n - m_t + 2)^{m_t} \geq 2^{m_t}$（见附录A），导致Critic网络遭遇维度灾难，收敛缓慢且性能次优。

消融实验（Table 10）进一步证实了这一瓶颈：当使用ARL-based编码器替代简单MLP时，独立MARL方法（IDDQN、BMG-Q）的奖励显著提升，但CTDE方法（HIVES、Enders et al.、CEVD）几乎无改善。这说明CTDE的性能瓶颈不在特征提取，而在Critic网络的维度爆炸——即使提供更强的编码器，Critic也无法有效处理膨胀的联合状态-动作空间。

### 2. 核心转向：集中式SARL与动作分解策略

Triple-BERT的根本洞察在于：订单调度本质上是集中决策问题，采用单智能体强化学习（SARL）可直接使用全局状态，从根本上绕开多智能体信用分配与非稳态难题。这一转向通过两个关键设计实现：

- **动作分解**：将联合动作概率 $\pi_{\Theta}^T(A_t | S_t)$ 建模为每个司机选择订单概率的增函数之积 $\mathsf{z}\left(\prod_{i,j \in \mathrm{h}(A_t)} \mathcal{P}_{i,j,t}\right)$（公式5）。这使得原本指数级的联合动作空间被分解为独立概率的乘积，贪心动作选择等价于最大化log概率之和，可通过二分图整数线性规划（ILP）高效求解（公式6）。
- **BERT自注意力架构**：Actor-BERT对所有司机和订单特征进行自注意力计算，捕获全局交互关系；QK-Attention-Norm模块生成司机-订单效用矩阵，通过两个小型网络 $\mathbf{f}$ 和 $\mathbf{g}$ 近似大型配对评估网络，将乘法复杂度转为加法复杂度（公式2-3），并采用Softplus非负归一化稳定训练。

### 3. 方法谱系定位

| 维度 | 独立MARL（DeepPool等） | CTDE MARL（HIVES等） | Triple-BERT（本文） |
|------|----------------------|---------------------|-------------------|
| 决策范式 | 多智能体分散决策 | 集中训练、分散执行 | 集中式单智能体 |
| 动作空间处理 | 独立Q值 + ILP | 联合动作采样/值分解 | 动作分解为概率乘积 + ILP |
| 网络架构 | DQN/GAT + MLP | QMIX/MASAC + MLP | BERT自注意力 + QK-Attention |
| 训练策略 | 端到端独立训练 | 端到端CTDE训练 | 两阶段：IDDQN预训练 + TD3微调 |
| 核心瓶颈 | 合作性差 | Critic维度爆炸 | 单点故障风险（集中式固有） |

Triple-BERT并非简单地将MARL替换为SARL，而是通过动作分解和BERT架构解决了SARL在大规模场景中的两个固有挑战：巨量观测空间（通过参数高效的BERT和QK-Attention处理）和巨量离散动作空间（通过概率分解和ILP求解）。

### 4. 适用边界与局限

**适用场景**：
- 高密度供需环境（如曼哈顿高峰时段），此时全局协调的价值最大，Triple-BERT相较基线提升显著（奖励+15%，取车时间-24.4%）。
- 订单分布相对集中的区域，BERT自注意力能有效捕获司机-订单间的复杂交互。

**已知局限**：
- **单点故障风险**：集中式SARL依赖全局状态信息，通信中断时系统可能完全失效。这是集中式架构的固有缺陷，论文未提供容错机制。
- **两阶段训练成本**：第一阶段需收集大量独立MARL样本进行IDDQN预训练，增加了部署复杂度和训练时间。消融实验表明，跳过预训练直接进行第二阶段训练会导致模型无法收敛（Figure 3）。
- **极度分散场景的收益有限**：在Queens数据集上，Triple-BERT相较BMG-Q的奖励提升仅为4.0%（+215.83），各策略间差异缩小，表明在订单分布极度分散时，全局协调的边际收益降低。
- **功能扩展性未验证**：当前框架专注于订单-司机匹配，未考虑动态定价、车辆重定位等联合优化任务。

### 5. 开放问题

1. **鲁棒性增强**：如何解决集中式SARL的单点故障问题？可能的路径包括引入分布式备份Critic或设计通信中断时的退化策略。
2. **训练效率优化**：能否用离线强化学习替代第一阶段IDDQN预训练，直接从历史数据中学习特征提取器，降低在线采样成本？
3. **样本效率提升**：重要性采样能否改进当前基于TD3的离线策略梯度优化（公式7），进一步提高样本效率？
4. **规模化通信折衷**：如何在保持全局合作的同时降低通信成本，使SARL更适用于超大规模场景（如跨城市调度）？
5. **方法泛化**：动作分解和BERT架构能否推广到其他集中式调度任务（如仓储物流、无人机编队）？这需要验证QK-Attention-Norm在不同约束条件下的稳定性。



## 原文 PDF

![[paperPDFs/ICLR_2026/Triple_BERT_Do_We_Really_Need_MARL_for_Order_Dispatch_on_Ride_Sharing_Platforms.pdf]]
