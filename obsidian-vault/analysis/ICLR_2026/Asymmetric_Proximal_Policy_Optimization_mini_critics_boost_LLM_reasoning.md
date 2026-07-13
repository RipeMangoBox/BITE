---
title: "Asymmetric Proximal Policy Optimization: mini-critics boost LLM reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Asymmetric_Proximal_Policy_Optimization_mini_critics_boost_LLM_reasoning.pdf
project_link: null
code_link: null
openreview_forum_id: 0vgzrcv4Dr
aliases:
- APPOA
- APPOMCBLR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过引入轻量级非对称集成评论家（mini-critics）和基于价值估计不确定性的策略损失重构，实现了高效、鲁棒的价值估计和更有效的策略更新。"
primary_logic: "预训练模型的初始表征能力使得非对称actor-critic架构可行；通过无重叠数据分块训练的集成迷你评论家能够产生多样化且校准良好的价值估计；利用评论家间价值估计的标准差可衡量状态的信息量和探索效用，以此指导优势掩码和熵过滤，提升策略学习效率。"
claims:
- "AsyPPO 使用一组轻量级 mini-critics，每个在无重叠的提示分片上训练。"
- "AsyPPO 利用评论家间不确定性来细化策略更新：(i) 掩码评论家一致区域的梯度，(ii) 从熵正则化中过滤高分歧状态。"
- "非重叠数据分区技术增强了集成评论家的多样性，并带来了稳定的性能提升。"
- "Multiple benchmarks (MATH-500, OlympiadBench, MinervaMath, AMC 2023, etc.) 上 Accuracy = AsyPPO (two 4B critics, 14B actor) avg +3 points vs GRPO (F..."
---

# Asymmetric Proximal Policy Optimization: mini-critics boost LLM reasoning

> [!tip] 核心洞察
> 预训练模型的初始表征能力使得非对称actor-critic架构可行；通过无重叠数据分块训练的集成迷你评论家能够产生多样化且校准良好的价值估计；利用评论家间价值估计的标准差可衡量状态的信息量和探索效用，以此指导优势掩码和熵过滤，提升策略学习效率。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 非对称近端策略优化：微型评论家提升大语言模型推理 |
| 英文题名 | Asymmetric Proximal Policy Optimization: mini-critics boost LLM reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=0vgzrcv4Dr) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Asymmetric Proximal Policy Optimization (AsyPPO) |
| Dataset | Multiple benchmarks (MATH-500, OlympiadBench, MinervaMath, AMC 2023, etc.), Qwen3-4B-Base performance improvement (6 benchmark average), Qwen3-8B-Base and 14B-Base, LiveCodeBench (Code Generation) |

> [!tip] 效果简介
> - Multiple benchmarks (MATH-500, OlympiadBench, MinervaMath, AMC 2023, etc.) 上，Accuracy 为 AsyPPO (two 4B critics, 14B actor) avg +3 points vs GRPO (Figure 8); vs VAPO: 61.3 vs 54.8; vs PPO (dense reward): 84.9 vs 81.5 (Table 2)，对比 GRPO, VAPO, Q-RM+PPO, Classic PPO，变化 In Figure 8, +3 points over GRPO; In Table 1, +6.5 over VAPO; In Table 2, +2.4 (dense reward)。
> - Qwen3-4B-Base performance improvement (6 benchmark average) 上，Improvement over initial policy 为 AsyPPO: > 6% improvement，对比 Classic PPO (symmetric)，变化 > 6%。
> - Qwen3-8B-Base and 14B-Base 上，Improvement over initial policy 为 AsyPPO: about 3% improvement，对比 Classic PPO，变化 about 3%。

## 概要

### 问题背景与瓶颈

将强化学习应用于大语言模型（LLM）推理训练时，主流的近端策略优化（PPO）算法依赖对称的 actor-critic 架构——价值函数（评论家）的规模需与策略模型（演员）相当。这在计算上极为昂贵，且在稀疏奖励和长推理链场景下，单一大型评论家的价值估计往往不够准确。近期方法（如 **GRPO**，He et al., 2025）索性放弃价值函数，转而采用组采样和平均优势基线，虽降低了开销，却牺牲了状态价值估计带来的训练鲁棒性。

### 核心方法：非对称近端策略优化（AsyPPO）

AsyPPO 的**核心洞察**在于：预训练 LLM 已具备强表征能力，使得小型评论家同样能有效指导大型策略模型。基于此，AsyPPO 提出三项关键设计：

1. **非对称集成评论家**：用两个轻量级迷你评论家（如 Qwen3-1.7B）替代与策略模型等大的对称评论家（如 Qwen3-14B），将峰值 GPU 内存降低约 20%，每步训练加速约 20 秒。
2. **无重叠数据分区**：在提示级别将训练数据均匀划分为不相交子集，每个迷你评论家仅在其专属数据上训练，从而增强集成多样性，避免认知同步。
3. **不确定性感知的策略更新**：利用评论家间价值估计的标准差衡量状态信息量——对低标准差（高共识）状态掩蔽优势梯度以避免过拟合，对高标准差（高分歧）状态过滤熵正则化以抑制无效探索。

### 主要结果

在多个数学推理基准（MATH-500、OlympiadBench、MinervaMath、AMC 2023 等）上，AsyPPO 相较主流方法取得一致提升：

- 相比 **GRPO**（无价值函数方法），平均准确率提升约 3 个百分点（Figure 8）；
- 相比 **VAPO**（Yue et al., 2025），平均准确率从 54.8 提升至 61.3（Table 1）；
- 在密集奖励设置下，相比经典对称 PPO 提升 2.4 个百分点（84.9 vs 81.5，Table 2）；
- 在 Qwen3-4B-Base 上性能提升超过 6%，在 Qwen3-8B/14B-Base 上提升约 3%（Abstract）。

在代码生成任务（LiveCodeBench）和跨模型家族迁移（Llama-3.1-8B-Base）上也展现出稳定的泛化能力。

### 方法定位

AsyPPO 在现有 RL4LLM 方法谱系中开辟了**非对称价值估计**的新路径：它既保留了价值函数带来的训练稳定性，又通过轻量集成和不确定性感知机制大幅降低了计算开销，在完全无价值函数方法（GRPO）与对称 PPO 之间找到了高效的折中方案。



### 大语言模型强化学习中的价值估计困境

将强化学习应用于大型语言模型（LLM）的推理训练时，主流的近端策略优化（**PPO**, Schulman et al., 2017）算法依赖对称的 actor-critic 架构——评论家（价值函数）与策略模型规模相当，通过广义优势估计（GAE）为策略更新提供细粒度的令牌级优势信号。然而，这一经典范式在 LLM 场景下面临两个相互纠缠的瓶颈：

**计算开销与价值估计质量的矛盾。** 训练一个与策略模型同等规模的评论家（如 Qwen3-14B 策略配 14B 评论家）会带来巨大的 GPU 内存和训练时间开销。若为降低成本而缩减评论家规模，则价值估计的准确性会显著下降，尤其在稀疏奖励和长推理链场景中，单评论家难以对复杂的状态转换给出可靠的回报预测。这迫使近期主流方法（如 **GRPO**, He et al., 2025）彻底放弃价值函数，转而采用组采样和平均优势基线——虽降低了计算成本，却牺牲了状态价值估计带来的细粒度学习信号和训练稳定性。

**价值估计的不确定性与策略更新的冲突。** 即便采用价值函数，传统方法对所有状态一视同仁地施加优势梯度和熵正则化。但在 LLM 推理中，不同状态的信息量差异巨大：评论家高度共识的状态往往对应策略已充分掌握的模式，其优势梯度贡献有限且容易导致对低质量样本的过拟合；而评论家分歧大的状态虽暗示未来动态复杂，却未必值得鼓励探索——盲目施加熵正则化可能引发无意义的策略发散甚至熵坍塌。

### 核心动机：非对称架构与不确定性感知

本文的核心假设是：**预训练 LLM 的初始表征能力使得非对称 actor-critic 架构成为可能**——轻量级评论家借助预训练表征先验，足以对更大规模的策略模型提供有效的价值引导。在此基础上，通过集成多个小型评论家并利用其价值估计的不确定性来细化策略更新，有望同时解决计算效率、估计鲁棒性和学习有效性三个问题。

具体而言，本文的动机源自以下观察：

1. **轻量评论家的可行性。** 初步实验表明，单个 Qwen3-0.6B 评论家即可跨模型规模（4B、8B、14B 策略）提供有效指导（Figure 3 左），但朴素集成因评论家同质化而增益有限（Figure 3 中），需要引入多样性机制来释放集成潜力。

2. **价值共识的信息量信号。** 当多个评论家对某状态的价值估计高度一致时，意味着该状态的下游动态已被策略充分建模，此类样本对学习增益有限且容易导致过拟合（Figure 5a）；反之，高分歧状态则暗示未来动态复杂且与最终结果的耦合较弱（Figure 7a）。

3. **价值标准差优于熵作为不确定性指标。** 实验发现，低价值标准差的状态始终维持低熵，但低熵状态可能仍有高价值标准差（Figure 6 左），表明价值标准差比策略熵更精准地刻画了状态的学习效用和探索风险。

基于以上动机，本文提出 **非对称近端策略优化（AsyPPO）**，通过无重叠数据分块训练的轻量级集成评论家和基于价值不确定性的策略损失重构，实现高效、鲁棒的价值估计和更有效的策略学习。



## 核心方法与创新机理

AsyPPO 的核心创新在于**解耦 actor-critic 的对称性约束**，通过三个相互协同的机制实现轻量级但鲁棒的价值估计，从而重构 PPO 的策略更新过程。

### 非对称架构与无重叠数据分区

传统 PPO（Schulman et al., 2017）要求评论家与策略模型规模相当，在 LLM 推理场景中导致巨大的计算开销和内存压力。GRPO（He et al., 2025）等近期方法完全放弃价值函数，转而采用组采样平均优势，但牺牲了状态价值估计的细粒度指导能力。AsyPPO 提出**非对称 actor-critic 架构**：使用两个轻量级迷你评论家（如 Qwen3-1.7B）指导大型策略模型（如 Qwen3-14B），使峰值 GPU 内存降低约 20%，每步训练加速约 20 秒（Figure 1(b)）。

然而，同质化初始化的集成评论家面临认知同步风险——若所有评论家看到相同数据，其价值估计高度一致，集成退化为单评论家。AsyPPO 的解决方案是**提示级别的无重叠数据分区**：将每个提示下的响应均匀划分给不同评论家，确保每个评论家接触不重叠的轨迹子集。这一设计从数据源头注入多样性，使评论家间价值估计的标准差显著增大（Figure 3 Right），为后续不确定性感知机制提供了可靠信号。

### 不确定性感知的策略损失重构

集成评论家的核心价值在于其**价值估计的标准差 $\sigma_t$** 可作为状态信息量和探索效用的代理指标。AsyPPO 据此重构了 PPO 的策略损失函数，包含两个互补机制：

**优势掩码（Advantage Masking）**：当评论家对某个状态的价值估计高度一致（$\sigma_t$ 低）时，该状态的未来动态已被策略充分建模，其优势梯度提供的学习信号有限，且在高数据复用（UTD=4）下容易导致过拟合。AsyPPO 掩蔽价值标准差最低的 $k\%$ 状态的优势梯度，使策略专注于高信息量样本。消融实验表明，掩蔽最低 20% 价值标准差状态的优势，在高数据复用场景下带来约 6 个百分点的性能提升（Figure 5(b)），且基于价值标准差的掩蔽始终优于基于熵的掩蔽（Figure 5(c)）。

**熵过滤（Entropy Filtering）**：当评论家对状态的价值估计高度分歧（$\sigma_t$ 高）时，该状态与最终结果的耦合较弱，未来动态复杂且不确定。在此类非关键状态上施加熵正则化会鼓励无意义的探索，甚至导致策略坍塌。AsyPPO 将价值标准差最高的 $h\%$ 状态从熵正则化项中排除，仅对剩余状态施加熵鼓励。实验显示，过滤高标准差状态可防止策略熵崩溃，带来约 7 个百分点的提升（Figure 7(b)），且过滤高标准差状态比过滤高熵状态更能有效维持策略熵水平（Figure 7(c)）。

### 方法谱系与知识库定位

| 方法 | 价值函数 | 架构 | 策略损失 | 关键局限 |
|------|---------|------|---------|---------|
| **PPO** (Schulman et al., 2017) | 对称评论家 | Actor = Critic | 标准裁剪目标 | 计算开销大，价值估计在稀疏奖励下不准确 |
| **GRPO** (He et al., 2025) | 无 | Actor-only | 组平均优势 | 缺乏细粒度状态价值指导 |
| **VAPO** (Yue et al., 2025) | 价值函数 | 面向价值估计 | 标准 PPO 变体 | 仍需较大评论家 |
| **Q-RM + PPO** (Chen et al., 2025b) | 令牌级奖励 | 奖励模型引导 | 标准 PPO | 依赖额外奖励模型训练 |
| **AsyPPO** (本文) | 轻量集成评论家 | Actor ≫ Critic | 不确定性感知掩码+过滤 | 需额外评论家训练，超参数需调整 |

AsyPPO 的关键洞察在于：预训练 LLM 的初始表征能力使得**小型评论家已具备指导大型策略的潜力**，但需要数据分区的多样性注入和不确定性感知的损失重构来充分释放这一潜力。两个迷你评论家即可实现性能的阶跃式提升（Figure 9(b)），在效率和效果之间取得了显著平衡。



![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_0vgzrcv4Dr/figures/003_Figure_1.jpg]]
*Figure 1: (Left): Learnable critics naturally enhance policy stability through fine-grained value estimation and yield continuous gains as training progresses. Off-policy ratio=8, average@4 of 6 benchmarks, i.e., AIME 24, AIME 25, MATH-500, OlympiadBench, MinervaMath, and AMC 2023. (Right): AsyPPO restores the critic’s role in PPO while remaining lightweight and stable under LLM-scale training. The average clock time of training and the peak GPU memory usage of AsyPPO are significantly lower than those of the classic PPO, remain at the GRPO level*

AsyPPO 的整体 pipeline 围绕“非对称 actor-critic + 不确定性感知策略更新”这一核心思路组织，包含五个紧密衔接的模块。图 1 对比了经典对称 PPO、无价值函数的 GRPO 和本文 AsyPPO 的架构差异，直观展示了非对称设计带来的计算效率优势。

### 模块关系与数据流

整个训练流程以**数据生成与分区**为起点。在每个训练步，策略模型（actor）对一批提示采样生成响应序列，形成 `(状态, 动作, 奖励)` 轨迹。随后，这些轨迹在**提示级别**按均匀无重叠的方式划分给各个迷你评论家——每个评论家获得每个提示下不重叠的响应子集。这一分区策略是确保集成评论家多样性的关键操作，其形式化表达为：

$$\mathcal{L}_{\mathrm{critic}}(\phi) = \sum_{m=1}^{M} \mathbb{E}_{(s_t, R_t) \sim \mathcal{D}_m} \left[ \left( V(s_t; \phi_m) - R_t \right)^2 \right]$$

其中 $\mathcal{D}_m$ 表示第 $m$ 个迷你评论家分配到的无重叠数据子集。

**迷你评论家训练**模块在每个子集上独立最小化价值预测的均方误差（MSE），使各评论家形成差异化的价值估计视角。训练完成后，进入**集成价值估计与优势计算**模块：取所有迷你评论家价值输出的平均值作为集成价值函数 $\bar{V}(s_t) = \frac{1}{M} \sum_{m=1}^{M} V_m(s_t; \phi_m)$，并基于此计算广义优势估计（GAE），得到校正后的优势 $\bar{A}_t$。

校正优势随后进入**不确定性感知掩码与过滤**模块。该模块计算各状态上迷你评论家价值估计的标准差 $\sigma_t$，并据此生成两个二值向量：

- **优势掩码** $\mathbb{I}_t^{\mathcal{A}}$：对价值标准差最低的 $k\%$ 状态（评论家高度一致的状态）置零，抹去其优势梯度，避免对低信息量样本的过拟合。
- **熵过滤向量** $\mathbb{I}_t^{\mathcal{H}}$：对价值标准差最高的 $h\%$ 状态（评论家高度分歧的状态）置零，将其从熵正则化项中排除，抑制无意义的探索行为。

最终，**重构 PPO 目标优化**模块将上述掩码和过滤向量嵌入标准 PPO 裁剪目标，形成完整的策略损失函数：

$$\mathcal{J}_{\mathrm{PPO}}(\theta) = \mathbb{E} \frac{1}{|o|} \sum_{t=1}^{|o|} \left[ \mathbb{I}_t^{\mathrm{A}} \cdot \min\left( \frac{\pi_\theta}{\pi_{\theta_{\mathrm{old}}}} \bar{A}_t, \operatorname{clip}\left( \frac{\pi_\theta}{\pi_{\theta_{\mathrm{old}}}}, 1-\epsilon, 1+\epsilon \right) \bar{A}_t \right) + \beta \cdot \mathbb{I}_t^{\mathcal{H}} \cdot \mathcal{H}[\pi_\theta(\cdot|s_t)] \right]$$

策略参数 $\theta$ 通过最小化该损失进行更新，完成一轮迭代。

### 输入输出规范

- **输入**：提示集 $Q \sim P(Q)$，预训练策略模型 $\pi_{\theta}$，$M$ 个轻量级迷你评论家 $\{V_{\phi_m}\}_{m=1}^M$。
- **中间产物**：采样响应轨迹、分区数据子集 $\{\mathcal{D}_m\}$、集成价值估计 $\bar{V}(s_t)$、校正优势 $\bar{A}_t$、价值标准差 $\sigma_t$、掩码向量 $\mathbb{I}^{\mathcal{A}}$ 和过滤向量 $\mathbb{I}^{\mathcal{H}}$。
- **输出**：更新后的策略参数 $\theta$，以及更新后的评论家参数 $\{\phi_m\}$。

### 与基线方法的关键差异

| 组件 | 经典 PPO (Schulman et al., 2017) | GRPO (He et al., 2025) | AsyPPO (本文) |
|------|------|------|------|
| 价值函数 | 对称评论家（与 actor 同规模） | 无价值函数，组平均优势 | 轻量级集成迷你评论家 |
| 评论家训练数据 | 共享全部轨迹 | 不适用 | 无重叠提示级分区 |
| 优势计算 | 单评论家 GAE | 组内相对奖励 | 集成平均价值 GAE |
| 策略损失 | 标准 PPO 裁剪 | 组归一化优势裁剪 | 不确定性感知掩码 + 熵过滤 |

这一非对称设计使 AsyPPO 在保持价值估计鲁棒性的同时，将峰值 GPU 内存降低约 20%，每步训练时间缩短约 20 秒（见 Figure 1(b)），实现了效率与性能的有效平衡。



### 4.1 非对称集成评论家架构

AsyPPO 的核心架构由两个轻量级迷你评论家（mini-critics）构成，每个评论家的参数量远小于策略网络（如 Qwen3-1.7B 评论家指导 Qwen3-14B 策略）。这一非对称设计的关键在于**预训练模型的初始表征能力**：即使评论家规模较小，其从预训练中继承的丰富表征仍能有效估计状态价值，从而打破传统对称 actor-critic 架构中评论家必须与策略等规模的限制。

**无重叠数据分区**是确保集成评论家多样性的核心机制。在提示级别上，响应数据被均匀划分为不重叠的子集，每个迷你评论家仅在其分配的子集上训练：

$$ \mathcal { L } _ { \mathrm { c r i t i c } } ( \phi ) = \sum _ { m = 1 } ^ { M } \mathcal { L } _ { \mathrm { c r i t i c } } ^ { ( m ) } ( \phi _ { m } ) = \sum _ { m = 1 } ^ { M } \mathbb { E } _ { ( s _ { t } , R _ { t } ) \sim \mathcal { D } _ { m } } \left[ \left( V ( s _ { t } ; \phi _ { m } ) - R _ { t } \right) ^ { 2 } \right] $$

其中 $M$ 为迷你评论家数量（默认 $M=2$），$\mathcal{D}_m$ 为第 $m$ 个评论家分配的数据子集，$V(s_t; \phi_m)$ 为评论家对状态 $s_t$ 的价值预测，$R_t$ 为蒙特卡洛回报。该设计通过数据层面的隔离，迫使各评论家发展出差异化的价值估计视角，为后续的不确定性感知机制奠定基础。

### 4.2 集成价值估计与校正优势

策略更新所需的优势估计基于集成平均价值函数计算。对于每个状态 $s_t$，集成价值为各迷你评论家输出的均值：

$$ \bar { V } ( s _ { t } ) = \frac { 1 } { M } \sum _ { m = 1 } ^ { M } V _ { m } ( s _ { t } ; \phi _ { m } ) $$

基于此均值价值函数，校正后的广义优势估计（GAE）为：

$$ \bar { A } _ { t } ( \gamma , \lambda ) = \sum _ { l = 0 } ^ { T - t - 1 } ( \gamma \lambda ) ^ { l } \delta _ { t + l } , \quad \delta _ { t } = r _ { t } + \gamma \bar { V } ( s _ { t + 1 } ) - \bar { V } ( s _ { t } ) $$

其中 $\gamma$ 为折扣因子，$\lambda$ 为 GAE 的指数衰减参数，$\delta_t$ 为时序差分误差。通过集成平均，校正后的优势估计能够平滑单个评论家的估计偏差，提升价值信号的鲁棒性。

### 4.3 不确定性感知的策略损失重构

AsyPPO 对标准 PPO 裁剪目标进行了两处关键重构，均以评论家间的价值估计标准差 $\sigma_t$ 作为不确定性的量化指标。

**优势掩码**：当评论家对某状态的价值估计高度一致（$\sigma_t$ 低）时，表明该状态的后续动态已被策略充分建模，其优势梯度提供的学习信号有限，且可能导致对低质量样本的过拟合。因此，对价值标准差最低的 $k$ 比例状态掩蔽其优势梯度：

$$ \mathbb { I } _ { t } ^ { \mathrm { A } } = \begin{cases} 0, & \text{if } \sigma_t \in \text{Low}_k(\boldsymbol{\sigma}) \\ 1, & \text{otherwise} \end{cases} $$

**熵过滤**：当评论家分歧较大（$\sigma_t$ 高）时，该状态与最终结果的耦合较弱，未来动态复杂且难以预测。在此类非关键状态上进行熵正则化会诱导无意义的探索，甚至导致策略坍塌。因此，对价值标准差最高的 $h$ 比例状态排除熵正则化项：

$$ \mathbb { I } _ { t } ^ { \mathcal { H } } = \begin{cases} 0, & \text{if } \sigma_t \in \text{Top}_h(\boldsymbol{\sigma}) \\ 1, & \text{otherwise} \end{cases} $$

完整的策略损失函数为：

$$ \mathcal { J } _ { \mathrm { P P O } } ( \theta ) = \mathbb { E } _ { [ q \sim P ( Q ) , o \sim \pi _ { \theta _ { \mathrm { o l d } } } ( O \mid q ) ] } \frac { 1 } { | o | } \sum _ { t = 1 } ^ { | o | } \left[ \mathbb { I } _ { t } ^ { \mathrm { A } } \cdot \min \left( \frac { \pi _ { \theta } ( o _ { t } | q , o _ { < t } ) } { \pi _ { \theta _ { \mathrm { o l d } } } ( o _ { t } | q , o _ { < t } ) } \bar { A } _ { t } , \text{clip} \left( \frac { \pi _ { \theta } ( o _ { t } | q , o _ { < t } ) } { \pi _ { \theta _ { \mathrm { o l d } } } ( o _ { t } | q , o _ { < t } ) } , 1 - \epsilon , 1 + \epsilon \right) \bar { A } _ { t } \right) + \beta \cdot \mathbb { I } _ { t } ^ { \mathcal { H } } \cdot \mathcal { H } [ \pi _ { \theta } ( \cdot | s _ { t } ) ] \right] $$

其中 $\epsilon$ 为裁剪范围，$\beta$ 为熵正则化系数，$\mathcal{H}[\cdot]$ 为策略熵。该损失函数通过双重不确定性感知机制，在保留有效学习信号的同时抑制过拟合和无意义探索。消融实验表明，掩蔽 20% 的低标准差状态带来约 6 个百分点的提升（Figure 5b），排除高标准差状态的熵过滤带来约 7 个百分点的提升（Figure 7b），且基于价值标准差的掩蔽始终优于基于熵的掩蔽（Figure 5c）。



## 实验与关键发现

### 主实验结果

AsyPPO 在数学推理基准上展现出显著且一致的性能优势。在 Qwen3-4B-Base 上，AsyPPO 相较经典对称 PPO 实现了超过 6% 的性能提升；在 Qwen3-8B-Base 和 Qwen3-14B-Base 上，提升幅度约为 3%。这一增益伴随着显著的计算效率改善：非对称架构使峰值 GPU 内存降低约 20%，每步训练时间缩短约 20 秒（Figure 1(b)）。

在更大规模模型的泛化实验中（Figure 8），AsyPPO（使用两个 4B 评论家指导 14B 策略模型）在多基准上的平均准确率比 GRPO 高出约 3 个百分点，同时比对称 PPO 轻量 20% 以上。值得注意的是，朴素的非对称 PPO 在 1.7B 评论家设置下无法有效指导 14B 策略，而 AsyPPO 通过集成评论家和不确定性感知机制解锁了这一能力。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_0vgzrcv4Dr/figures/021_Figure_8.jpg]]
*Figure 8: AsyPPO improves accuracy by an average of about 3 + points compared to GRPO, and achieves more than 20% lighter weight than symmetrical PPO. Our naive asymmetric PPO still works on the 14b policy, but fails under the 1.7b critic setting. However, AsyPPO unlocks the 1.7b critic’s ability to guide the 14b actor*

与面向价值函数的基线方法对比（Table 1），AsyPPO 取得 61.3 的平均准确率，显著优于 VAPO（54.8）和 Q-RM + PPO（56.2），提升幅度达 6.5 个百分点。在密集奖励与稀疏奖励场景下（Table 2），AsyPPO 分别达到 84.9 和 83.6，较经典 PPO 的 81.5 和 78.3 提升 2.4 和 5.3 个百分点，表明其在稀疏奖励长推理链场景下的鲁棒性更强。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_0vgzrcv4Dr/figures/030_Table_1.jpg]]
*Table 1: Performance comparison*

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_0vgzrcv4Dr/figures/031_Table_2.jpg]]
*Table 2: Performance comparison*

跨领域迁移方面，在代码生成任务 LiveCodeBench 上（Table 3），AsyPPO 将基础模型得分从 45.6 提升至 55.2，而经典 PPO 仅达到 49.7（提升 5.5 个百分点）。跨模型家族的泛化实验（Table 4）显示，AsyPPO 在 Llama-3.1-8B-Base 上将平均准确率从 4.6 提升至 23.8，优于经典 PPO 的 19.2（提升 4.6 个百分点），验证了方法的模型架构无关性。

### 消融实验

**非重叠数据分区的必要性。** Figure 3 系统对比了三种评论家配置：单迷你评论家（左）虽能跨模型规模提供有效指导，但朴素集成两个评论家（中）由于缺乏多样性，性能提升有限；本文提出的非重叠数据分区方法（右）显著增强了评论家间的认知差异，带来稳定的性能跃升。

**优势掩码的关键作用。** Figure 5(b) 显示，在高数据复用设置（UTD=4）下，掩蔽价值标准差最低的 20% 状态的优势梯度，使 AsyPPO 获得约 6 个百分点的性能提升，有效防止了对低信息量样本的过拟合。Figure 5(c) 进一步表明，基于价值标准差的掩蔽机制始终优于基于熵的掩蔽，提供了更强的学习效率增益。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_0vgzrcv4Dr/figures/012_Figure_5.jpg]]
*Figure 5: (a): Agreement among critics implies the state’s downstream dynamics are well modeled by the policy, making these samples low-value for learning and best avoided for overfitting. (b): In the high data-reuse setting (UTD=4), masking the bottom 20% (by value-std) boosts AsyPPO’s learning efficiency, yields an improvement of about 6 points. The accuracy records of the six benchmarks follow Figure 1 (b). (c): We evaluated two 5% masking mechanisms on vanilla AsyPPO (baseline), i.e., entropy vs. value-std. The value-std masking produced the strongest learning efficiency benefit. Actors use Qwen3-4B-Base, while critics use Qwen3-0.6B-Base*

**价值标准差与熵的关系。** Figure 6 揭示了关键洞察：低价值标准差状态始终维持低熵，但低熵状态可能具有高价值标准差。这意味着仅依赖熵进行状态筛选会遗漏重要信息——低熵但高标准差的状态仍需探索，而高标准差的低价值状态则应被过滤。

**熵过滤的有效性。** Figure 7(b) 表明，将高价值标准差状态从熵正则化中排除，可防止朴素熵正则化导致的策略坍塌，并带来约 7 个百分点的显著提升。Figure 7(c) 的对比实验显示，过滤价值标准差最高的 40% 状态能够维持策略熵在健康水平，而过滤相同比例的最高熵状态则导致策略坍塌，进一步验证了以价值标准差而非熵作为过滤依据的合理性。

![[assets/figures/papers/paper_list_l43_https_openreview_net_forum_id_0vgzrcv4Dr/figures/007_Figure_7.jpg]]

**评论家规模与数量的影响。** Figure 9(a) 显示，增大评论家尺寸会稳步提升策略的峰值分数，呈现参数规模带来的边际收益。Figure 9(b) 表明，使用两个迷你评论家即可实现性能的质变跃升，更多评论家的边际增益有限。Figure 9(c) 确定合适的组大小为 32，Figure 9(d) 证实使用平均值进行价值聚合优于使用最小值。

**掩码与过滤百分比的灵敏度。** Figure 10 的灵敏度分析表明，掩蔽 20% 的低价值标准差状态带来最强劲的增益；过滤百分比在合理范围内表现稳定，且训练过程中的策略熵曲线保持健康，未出现坍塌迹象。

### 关键图表结论

- **Figure 1**：非对称架构在保持接近 GRPO 的内存效率的同时，实现了持续的准确率增长。
- **Figure 4**：集成评论家能够有效估计涉及关键推理模式（如验证、回溯、反向链式推理、子目标设定）的状态价值，校正后的价值估计普遍高于原始估计。
- **Figure 11**：价值标准差与梯度大小呈正相关，高标准差状态对应更大的策略梯度，验证了不确定性感知掩码机制的合理性。
- **Table 5**（MATH-500 上 16 次运行的平均结果）：AsyPPO 在统计上显著优于基线方法，方差可控，表明训练稳定性良好。

### 失败模式与局限性

尽管 AsyPPO 在数学推理和代码生成任务上表现优异，但仍存在以下局限：

1. **模型架构依赖性**：实验主要基于 Qwen3 模型家族，尚未在其他架构（如 DeepSeek、Mistral）上充分验证，跨架构泛化性需进一步确认。
2. **任务领域限制**：评估集中在数学推理和代码生成，在长链推理、多跳问答等复杂推理领域的有效性未知。
3. **超参数敏感性**：优势掩码和熵过滤的百分比超参数需针对不同任务调整，缺乏自适应机制。
4. **资源开销权衡**：虽然计算开销显著低于对称 PPO，但相较于完全无价值函数的 GRPO 等方法，仍需额外的评论家训练资源。



## 定位与知识库关联

### 1. 与主流RL4LLM方法的关系

AsyPPO 处于 RL4LLM 方法谱系中“价值函数回归”与“无价值函数”两条路线的交汇点，通过非对称架构重新确立了评论家在 LLM 推理训练中的地位。

**经典对称 Actor-Critic 路线。** 标准 PPO（Schulman et al., 2017）在 LLM 场景中需训练与策略模型规模相当的价值函数，计算开销极大。在稀疏奖励和长推理链场景下，单评论家的价值估计往往不准确，导致训练不稳定。AsyPPO 通过将对称评论家替换为两个轻量级迷你评论家（如 Qwen3-1.7B 指导 Qwen3-14B 策略），在保留价值估计能力的同时将峰值 GPU 内存降低约 20%（Figure 1(b)）。

**无价值函数路线。** GRPO（He et al., 2025）完全放弃价值函数，转而采用组采样和平均优势基线，成为当前 RL4LLM 的主流选择。然而，组平均优势本质上是粗粒度的基线减法，牺牲了对每个状态价值的细粒度估计。AsyPPO 在保持轻量级的前提下恢复了价值函数，在 14B 策略规模上相比 GRPO 平均提升约 3 个百分点（Figure 8），证明了价值估计在推理训练中的不可替代性。

**面向价值函数的 RLVR 方法。** VAPO（Yue et al., 2025）和 Q-RM + PPO（Chen et al., 2025b）均保留了价值函数，但前者侧重于价值函数优化的具体技术，后者引入令牌级奖励。AsyPPO 与这些工作的核心差异在于架构层面的非对称设计：用集成迷你评论家替代单一大型评论家，并通过评论家间不确定性驱动策略更新。

### 2. 核心创新与机制定位

AsyPPO 的方法论贡献可分解为三个相互耦合的机制，每个机制针对 RL4LLM 场景的特定瓶颈：

**非重叠数据分区（§4.1）。** 传统集成方法中，多个评论家使用相同轨迹训练，同质化初始化下难以产生多样性。AsyPPO 在提示级别进行无重叠均匀划分，每个迷你评论家看到不重叠的响应子集。这一设计增强了评论家间的认知差异（Figure 3 Right），为后续的不确定性驱动机制提供了基础。

**优势掩码（§4.2）。** 当评论家对某状态的价值估计高度一致（低标准差）时，该状态的下游动态已被策略充分建模，继续在这些状态上施加梯度更新会导致对低信息量样本的过拟合。AsyPPO 掩蔽价值标准差最低的 20% 状态的优势梯度，在高数据复用（UTD=4）下带来约 6 个百分点的提升（Figure 5(b)）。消融实验表明，基于价值标准差的掩蔽始终优于基于熵的掩蔽（Figure 5(c)）。

**熵过滤（§4.2）。** 当评论家对某状态的价值估计高度分歧（高标准差）时，该状态与最终结果的耦合弱、未来动态复杂，在此类非关键状态上进行探索无意义甚至有害。AsyPPO 将价值标准差最高的 20% 状态从熵正则化中排除，防止策略坍塌，带来约 7 个百分点的提升（Figure 7(b)）。值得注意的是，高标准差状态与高熵状态的重叠极小（Figure 7(c)），过滤高标准差状态比过滤高熵状态能更好地维持策略熵。

### 3. 适用边界与能力范围

**已验证的适用场景。** 实验证据覆盖了数学推理（MATH-500、OlympiadBench、MinervaMath、AMC 2023、AIME 24/25）和代码生成（LiveCodeBench）两大领域。在 Qwen3 模型家族（4B、8B、14B）上均展现出相对于经典 PPO 的稳定增益，在 4B 规模上提升超过 6%，在 8B 和 14B 规模上提升约 3%（Abstract）。跨模型家族实验（Llama-3.1-8B-Base）显示 AsyPPO 相比 PPO 提升 4.6 个百分点（Table 4），初步验证了泛化性。

**推理链长度与奖励密度。** 方法在稀疏奖励（仅最终答案正确性）和密集奖励（过程奖励）两种设置下均有效。在密集奖励场景下，AsyPPO 相比 PPO 提升 2.4 个百分点（Table 2），表明价值估计的改进对两种奖励结构均有增益。

**关键超参数依赖性。** 优势掩码和熵过滤的百分比是方法的关键调节旋钮。消融实验表明掩蔽 20% 的低价值标准差状态带来最强劲的增益（Figure 10 Left），过滤 20% 的高价值标准差状态效果最优（Figure 10 Middle）。不同任务和模型规模下，这些百分比可能需要调整。分组大小（group size）建议为 32（Figure 9(c)），价值聚合使用均值优于最小值（Figure 9(d)）。

### 4. 局限性与开放问题

**模型架构覆盖不足。** 实验主要基于 Qwen3 模型家族，尚未在 DeepSeek、Mistral、LLaMA-3 等主流架构上充分验证。跨模型家族的初步实验（Llama-3.1-8B）虽为正面，但仅覆盖单一规模。

**任务领域局限。** 评估集中在数学推理和代码生成，这些任务具有明确的正确性判断和相对结构化的推理过程。在长链推理、多跳问答、开放域生成等更复杂的推理领域，方法的有效性尚未验证。

**资源开销的折衷。** 尽管 AsyPPO 相比对称 PPO 显著降低了计算开销，但仍需训练额外的评论家网络。相比完全无价值函数的 GRPO 等方法，仍有一定资源消耗。在极端资源受限的场景下，这一开销可能成为限制因素。

**集成评论家的初始化敏感性。** 方法依赖预训练模型的初始表征能力来实现非对称架构。当基础模型的预训练质量不足或领域差异较大时，迷你评论家的指导能力可能下降。论文提出了“在同质化初始化下集成评论家能否保持效力”的开放问题，暗示这一依赖性是方法的内在约束。

**超参数的自适应调节。** 优势掩码和熵过滤的百分比目前是固定超参数。能否根据训练动态自适应调节这些阈值，是提升方法鲁棒性的潜在方向。此外，评论家超参数设置（如学习率、更新频率）对校准和不确定性估计的影响尚未系统研究。

**集成评论家的异质性潜力。** 论文提出了“由不同模型家族和尺寸组成的集成评论家系统是否表现出性能差异”的开放问题。当前实现使用同构迷你评论家，引入异构评论家可能进一步增强多样性，但也可能引入新的校准挑战。



## 原文 PDF

![[paperPDFs/ICLR_2026/Asymmetric_Proximal_Policy_Optimization_mini_critics_boost_LLM_reasoning.pdf]]
