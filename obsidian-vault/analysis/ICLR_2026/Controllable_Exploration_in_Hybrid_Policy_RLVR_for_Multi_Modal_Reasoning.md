---
title: "Controllable Exploration in Hybrid-Policy RLVR for Multi-Modal Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Controllable_Exploration_in_Hybrid_Policy_RLVR_for_Multi_Modal_Reasoning.pdf
openreview_forum_id: 5wxyCidRsK
aliases:
- CEHPRMMR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过将专家数据视为分布基线（而非绝对目标），利用组内优势幅度|Â_i|作为稀有度权重来校准更新幅度，并结合LeakyReLU的非对称梯度门控，实现对探索强度的可控调节。"
primary_logic: "将专家监督重新定义为相对参考的分布校准基线，使得对正确但低频响应的强化和对过自信错误的抑制都能以受控方式进行，从而在保留策略熵的同时引导探索方向，解决了以往混合策略中模仿信号与探索需求之间的冲突。"
claims:
- "在极具挑战性的GeoEval基准上，CalibRL准确率达到33.44%，远超GRPO (26.15%)、SFT+GRPO (6.00%)和混合策略方法，证明可控探索在处理困难样本上的优势。"
- "移除优势加权|Â_i|导致所有基准的平均性能从50.59大幅下降至45.30，验证了组稀有度权重对维持熵和提升性能的必要性。"
- "通过调整LeakyReLU的α参数可控制探索强度，α=0.5达到最佳性能，且训练熵曲线显示α能有效调节探索行为。"
- "与LUFFY和RL-PLUS相比，CalibRL的训练后策略熵最高（1.4968 vs 0.0881 vs 0.3452），且奖励更高，表明其校准机制有效缓解了熵崩溃。"
---

# Controllable Exploration in Hybrid-Policy RLVR for Multi-Modal Reasoning

> [!tip] 核心洞察
> 将专家监督重新定义为相对参考的分布校准基线，使得对正确但低频响应的强化和对过自信错误的抑制都能以受控方式进行，从而在保留策略熵的同时引导探索方向，解决了以往混合策略中模仿信号与探索需求之间的冲突。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向多模态推理的混合策略RLVR可控探索 |
| 英文题名 | Controllable Exploration in Hybrid-Policy RLVR for Multi-Modal Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5wxyCidRsK); [GitHub](https://github.com/zhh6425/CalibRL) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | CalibRL |
| Dataset | In-domain geometry (平均), Out-of-domain (7个基准平均), GeoEval (个别困难集), MMMU (OOD) |

> [!tip] 效果简介
> - In-domain geometry (平均) 上，准确率 (%) 为 44.93，对比 39.48 (GRPO)，变化 +5.45。
> - Out-of-domain (7个基准平均) 上，准确率 (%) 为 59.36，对比 57.24 (GRPO)，变化 +2.12。
> - GeoEval (个别困难集) 上，准确率 (%) 为 33.44，对比 26.15 (GRPO)，变化 +7.29。

## 概述

在多模态大语言模型（MLLM）的强化学习可验证推理（RLVR）训练中，存在一个关键瓶颈：直接模仿专家轨迹会导致策略熵快速下降（熵崩溃），使模型丧失探索更优推理路径的能力。现有的混合策略方法试图通过引入专家数据来引导学习，但始终无法实现稳定、可控的探索——策略要么过度确定性，要么进行无引导的随机探索，两者均导致性能下降。

针对这一问题，本文提出了 **CalibRL**，一种支持可控探索的混合策略 RLVR 框架。其核心思想是**将专家数据重新定义为分布校准基线，而非绝对模仿目标**。通过引入两个互补机制——分布感知的优势加权与非对称激活函数（LeakyReLU）——CalibRL 能够以受控方式强化正确但低频的响应，同时抑制过自信的错误更新，从而在保留策略熵的同时引导探索方向。

在方法定位上，CalibRL 属于混合策略优化范式，但其对专家数据的利用方式与现有方法有本质区别：**LUFFY**（Yan et al., 2025）将专家信号作为离策略指导，**RL-PLUS**（Dong et al., 2025）通过多重要性采样塑造探索优势，而 CalibRL 则将专家响应作为相对参考的分布基线，通过组内优势幅度 $|\hat{A}_i|$ 作为稀有度权重来校准更新幅度，并结合 LeakyReLU 的非对称梯度门控实现对探索强度的可控调节。

实验结果表明，CalibRL 在多个基准上取得了显著且一致的提升。在极具挑战性的 GeoEval 基准上，准确率达到 33.44%，远超 GRPO（26.15%）、SFT+GRPO（6.00%）及其他混合策略方法。在 7 个域外基准上，平均准确率提升 2.12 个百分点。消融实验验证了各组件的必要性：移除优势加权导致平均性能从 50.59 大幅下降至 45.30；LeakyReLU 参数 α 可有效控制探索强度，α=0.5 达到最佳平衡。与 LUFFY 和 RL-PLUS 相比，CalibRL 的训练后策略熵最高（1.4968 vs 0.0881 vs 0.3452），且奖励更高，证实其校准机制有效缓解了熵崩溃问题。

## 背景与动机

### 多模态推理中的强化学习瓶颈

多模态大语言模型（MLLMs）在几何、数学等复杂推理任务上的能力提升，近期得益于可验证奖励的强化学习（RLVR）范式。该范式通过稀疏的二元奖励信号——正确响应为1，否则为0——引导模型自主探索有效的推理路径。GRPO（Shao et al., 2024）作为代表性方法，通过组内归一化优势 $\hat{A}_{i,t}$ 消除对价值网络的依赖，在推理任务上展现了显著效果。

然而，RLVR训练存在一个关键的结构性矛盾：**策略熵的快速崩溃**。在稀疏奖励环境下，模型一旦发现某条能获得奖励的推理路径，便会迅速收敛到该路径上，导致策略分布过于集中，丧失探索更优解的能力。这一问题在多模态推理中尤为突出，因为视觉-语言联合空间中的推理路径远比纯文本场景复杂，早期收敛往往意味着模型被困在次优解附近。

### 混合策略方法的困境

为缓解熵崩溃并注入先验知识，研究者提出了混合策略（hybrid-policy）方法，在RL训练中引入专家轨迹作为辅助信号。然而，现有方法陷入两难境地：

- **直接模仿专家**：如SFT+GRPO的序列范式，先通过负对数似然 $\mathcal{L}_{\mathrm{expert}} = -\mathbb{E}[\log \pi_{\theta}(\tau_i^{\mathrm{expert}}|q_i)]$ 最大化专家轨迹概率，再进行RL训练。这导致策略被过度约束在专家行为的邻域内，熵虽高但探索缺乏方向性，性能反而低于纯GRPO——在GeoEval上SFT+GRPO仅取得6.00%的准确率，远低于GRPO的26.15%（Table 1）。

- **无引导的随机探索**：纯GRPO虽然保持了一定的探索性，但缺乏有效的方向引导，在面对困难样本时探索效率低下。而LUFFY（Yan et al., 2025）和RL-PLUS（Dong et al., 2025）等混合策略方法，虽然试图平衡专家知识与策略探索，但训练后策略熵极低（分别为0.0881和0.3452），表明它们实质上仍陷入了确定性模式（Table 15, Appendix F）。

### 核心洞察：从绝对模仿到分布校准

上述困境的根源在于：**现有方法将专家数据视为绝对目标，而非相对参考**。当专家响应被当作“正确答案”来直接最大化其似然时，优化过程会单调地推高专家路径的概率（$\nabla_{\theta}\mathcal{L}_{\mathrm{expert}} = -\mathbb{E}[\nabla_{\theta}\log \pi_{\theta}(\tau_i^{\mathrm{expert}}|q_i)]$），无论该路径在当前策略分布下是否已被充分覆盖。这导致两个后果：

1. **过自信抑制**：对模型已能正确推理但方式不同于专家的响应，施加不必要的惩罚。
2. **稀有响应忽视**：对正确但低频的推理路径，缺乏针对性的强化信号。

本文的核心洞察在于：**将专家监督重新定义为分布校准基线**。具体而言，通过计算策略响应与专家响应的对数概率差 $\Delta\ell_i = \log \pi_{\theta}(\tau_i^{\mathrm{policy}}|q_i) - \log \pi_{\theta}(\tau_i^{\mathrm{expert}}|q_i)$，将专家知识转化为相对偏好信号；再利用组内绝对优势 $|\hat{A}_i|$ 作为稀有度权重，对低频的正确响应给予更强更新，对过自信的错误响应进行受控抑制。这种**非对称校准机制**使得模仿信号与探索需求不再冲突，而是在保留策略熵的同时引导探索方向。

基于此洞察，本文提出**CalibRL**——一个支持可控探索的混合策略RLVR框架，通过分布感知的优势加权和LeakyReLU非对称激活，实现对探索强度的精确调节。

## 核心创新

CalibRL的核心创新在于重新定义了混合策略RLVR中专家数据的角色，将其从“绝对模仿目标”转变为“分布校准基线”，并通过两个互补机制——**分布感知的优势加权**和**LeakyReLU非对称门控**——实现对探索强度的可控调节，从根本上解决了现有方法面临的熵崩溃与探索失控困境。

### 专家数据的角色重构：从绝对目标到分布基线

传统混合策略方法（如LUFFY、RL-PLUS）将专家轨迹视为直接模仿或离策略奖励的目标，导致策略概率分布单向收敛于专家行为，策略熵快速下降（熵崩溃）。CalibRL的核心洞察在于：**专家监督应作为相对参考的分布校准基线，而非绝对优化目标**。

具体而言，CalibRL引入对数概率差距 $\Delta \ell_i$ 来衡量模型对自身响应与专家响应的相对偏好：

$$\Delta \ell_i = \log \pi_{\theta}(\tau_i^{\mathrm{policy}}|q_i) - \log \pi_{\theta}(\tau_i^{\mathrm{expert}}|q_i)$$

这一设计的关键在于：它不强制策略向专家分布靠拢，而是将专家响应作为校准的“锚点”。当策略对正确响应的概率低于专家基线时，系统进行强化；当策略对错误响应表现出过自信时，系统进行抑制。这种**双向校准**使得对正确但低频响应的强化和对过自信错误的抑制都能以受控方式进行，在保留策略熵的同时引导探索方向。

### 分布感知的优势加权：以稀有度校准更新幅度

标准GRPO中的组归一化优势 $\hat{A}_i$ 仅用于指示策略梯度方向。CalibRL的创新在于**额外利用绝对优势 $|\hat{A}_i|$ 作为“组稀有度权重”**，调制探索更新的幅度。

其因果机制如下：在组内采样中，正确响应越稀有，其归一化优势的绝对值越大（见Figure 4）。$|\hat{A}_i|$ 因此天然反映了响应的“稀有度”——稀有但正确的响应获得更大的更新权重，从而被更积极地强化；常见的正确响应则获得较小的更新权重，避免过度优化。这一机制使得探索资源向尚未被充分发现的正确推理路径倾斜，而非均匀分散。

消融实验提供了决定性证据：移除优势加权 $|\hat{A}_i|$ 后，所有基准的平均性能从50.59大幅下降至45.30（Table 4），验证了组稀有度权重对维持熵和提升性能的必要性。

### LeakyReLU非对称门控：可控的探索强度调节

CalibRL采用LeakyReLU作为激活函数，构成可控探索损失的核心：

$$\mathcal{L}_{\mathrm{exploration}} = |\hat{A}_i| \cdot \mathrm{LeakyReLU}(-s_i \cdot \Delta \ell_i, \alpha)$$

其中 $s_i$ 为正确性信号（正确为+1，错误为-1），$\alpha$ 为LeakyReLU的负斜率参数。该设计的创新在于**非对称梯度门控**：

- 当输入为正（策略表现优于基线）时，梯度为1，正常更新；
- 当输入为负（策略表现不如基线）时，梯度被缩放至 $\alpha < 1$，**抑制更新强度**，防止对过自信错误的过度惩罚或对已充分学习的正确响应的过度强化。

参数 $\alpha$ 因此成为控制探索强度的“旋钮”：$\alpha$ 越大，对负输入的抑制越弱，探索越激进；$\alpha$ 越小，抑制越强，探索越保守。实验表明，$\alpha=0.5$ 达到最佳性能平衡（平均50.59），且训练熵曲线（Figure 3）直观展示了 $\alpha$ 对探索行为的有效调节——过高或过低的 $\alpha$ 均导致性能下降（Table 4）。

与其他激活函数（ReLU、Sigmoid等）的消融对比进一步验证了**非对称性**的关键贡献：LeakyReLU凭借其可调节的负斜率，构建了可控的熵塑形机制，而对称激活函数无法实现这种精细的探索调控（Table 7）。

### 与现有方法的本质区别

与简单熵正则化或KL-Cov等传统熵控制方法相比，CalibRL的创新在于**引导式而非无引导的熵控制**。传统方法通过增加熵奖励项鼓励随机探索，但无法区分有意义的推理多样性与无意义的随机性。CalibRL通过专家基线校准和优势加权，将探索引导至“被专家认可但尚未被策略充分发现”的方向，在GeoQA等困难基准上取得显著提升（Table 6）。

与LUFFY和RL-PLUS等混合策略方法相比，CalibRL的训练后策略熵最高（1.4968 vs 0.0881 vs 0.3452），且奖励更高（Table 15），表明其校准机制有效缓解了熵崩溃，实现了稳定、可控的探索。

## 整体框架

CalibRL 的整体框架围绕一个核心矛盾展开：在 RLVR 训练中，如何利用专家数据引导探索，同时避免策略熵的快速崩溃。传统混合策略方法要么将专家轨迹作为绝对模仿目标，导致策略过度确定性；要么进行无引导的随机探索，难以收敛到更优的推理路径。CalibRL 的关键设计在于**将专家数据重新定义为分布校准基线**，而非严格的模仿目标，从而在保留策略熵的同时，以受控方式引导探索方向。

### 框架总览

CalibRL 建立在 GRPO 的组归一化优势框架之上，通过三个协同模块实现可控探索：

| 模块 | 功能 | 核心机制 |
|------|------|----------|
| 对数概率差距计算 | 衡量策略与专家的相对偏好 | $ \Delta \ell_i = \log \pi_{\theta}(\tau_i^{\mathrm{policy}}|q_i) - \log \pi_{\theta}(\tau_i^{\mathrm{expert}}|q_i) $ |
| 优势加权校准 | 利用组内稀有度动态调整更新幅度 | $ |\hat{A}_i| $ 作为稀有度权重 |
| LeakyReLU 非对称门控 | 选择性强化或抑制，控制探索强度 | 负斜率 $ \alpha $ 控制抑制程度 |

这三个模块集成为一个可控探索损失项，叠加在标准 GRPO 目标上：

$$ \mathcal{L}_{\mathrm{exploration}} = |\hat{A}_i| \cdot \mathrm{LeakyReLU}(-s_i \cdot \Delta \ell_i, \alpha) $$

$$ \mathcal{J}(\theta) = \mathbb{E}_{q \sim \mathcal{D}, \tau \sim \pi_{\theta}(\cdot|q)} \sum_{t=1}^{|\tau|} \min(r_{i,t}(\theta) \hat{A}_{i,t}, \mathrm{clip}(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_{i,t}) - \lambda \mathcal{L}_{\mathrm{exploration}} $$

其中 $ s_i \in \{-1, +1\} $ 表示响应的正确性信号，$ \lambda $ 平衡标准策略优化与探索校准。

### 输入输出流

**输入**：
- 问题 $ q_i $ 从数据集 $ \mathcal{D} $ 采样
- 策略模型 $ \pi_{\theta} $ 对每个问题生成 $ G $ 个响应 $ \{\tau_i^{\mathrm{policy}}\} $
- 对应的专家响应 $ \tau_i^{\mathrm{expert}} $（作为分布基线）
- 可验证奖励 $ R(\tau) \in \{0, 1\} $（正确为 1，否则为 0）

**处理流程**：
1. 计算组归一化优势 $ \hat{A}_i $（基于 $ G $ 个响应的奖励分布）
2. 计算对数概率差距 $ \Delta \ell_i $（策略响应 vs 专家响应的对数似然差）
3. 将 $ |\hat{A}_i| $ 作为稀有度权重，$ \mathrm{LeakyReLU}(-s_i \cdot \Delta \ell_i, \alpha) $ 作为非对称门控
4. 组合为 $ \mathcal{L}_{\mathrm{exploration}} $，以权重 $ \lambda $ 集成到 GRPO 损失中

**输出**：
- 更新后的策略参数 $ \theta $，在保持较高熵的同时提升奖励和准确率

### 关键设计逻辑

**为什么需要优势加权**：$ |\hat{A}_i| $ 反映了某个响应在组内的稀有程度——正确但低频的响应获得更大的优势幅度，从而被更强地强化；常见响应（无论正误）的更新幅度被压缩。消融实验证实，移除 $ |\hat{A}_i| $ 导致所有基准平均性能从 50.59 降至 45.30（Table 4），验证了组稀有度权重对维持熵和性能的必要性。

**为什么需要 LeakyReLU 非对称门控**：当 $ -s_i \cdot \Delta \ell_i < 0 $（即模型对正确响应的概率低于专家，或对错误响应的概率高于专家）时，LeakyReLU 以斜率 $ \alpha < 1 $ 缩放梯度，避免过度修正。$ \alpha $ 直接控制探索强度：$ \alpha=0.5 $ 达到最佳性能平衡（Table 4），且训练熵曲线显示 $ \alpha $ 能有效调节探索行为（Figure 3）。

**与现有混合策略方法的本质区别**：LUFFY 和 RL-PLUS 等方法的专家信号直接参与策略更新，导致训练后策略熵极低（LUFFY: 0.0881, RL-PLUS: 0.3452），而 CalibRL 保持熵为 1.4968 且奖励更高（Table 15），表明其校准机制有效缓解了熵崩溃。

## 核心模块与公式推导

### 3.1 熵崩溃问题与专家监督的局限性

在RLVR训练中，一个直接的混合策略思路是将专家轨迹的负对数似然损失 $\mathcal{L}_{\mathrm{expert}}$ 与GRPO目标联合优化：

$$\mathcal{L}_{\mathrm{expert}} = -\mathbb{E}_{(q_i,\tau_i^{\mathrm{expert}})\sim\mathcal{D}}\left[\log\pi_{\theta}(\tau_i^{\mathrm{expert}}|q_i)\right]$$

其梯度 $\nabla_{\theta}\mathcal{L}_{\mathrm{expert}} = -\mathbb{E}_{(q_i,\tau_i^{\mathrm{expert}})}\left[\nabla_{\theta}\log\pi_{\theta}(\tau_i^{\mathrm{expert}}|q_i)\right]$ 单调地增加专家响应的生成概率。然而，这种单向优化会导致策略熵 $\mathcal{H}(\pi_{\theta}(\cdot|q)) = -\sum_{\tau} \pi_{\theta}(\tau|q) \log \pi_{\theta}(\tau|q)$ 快速下降，即**熵崩溃**——模型被锁定在专家轨迹的邻域内，丧失了探索更优推理路径的能力。Figure 1的训练动态曲线证实了这一现象：SFT+GRPO的熵值虽高但奖励停滞，而纯GRPO的熵则过早收敛。

### 3.2 可控探索的核心机制

CalibRL的核心设计是将专家数据重新定义为**分布校准基线**而非绝对模仿目标，通过三个相互配合的模块实现对探索强度的精细调控。

**对数概率差距。** 对于每个问题 $q_i$，计算策略自身响应 $\tau_i^{\mathrm{policy}}$ 与专家响应 $\tau_i^{\mathrm{expert}}$ 的对数似然差：

$$\Delta \ell_i = \log \pi_{\theta}(\tau_i^{\mathrm{policy}}|q_i) - \log \pi_{\theta}(\tau_i^{\mathrm{expert}}|q_i)$$

$\Delta \ell_i$ 捕捉了模型对两类响应的相对偏好：正值表示模型更倾向于自身采样结果，负值表示模型更认可专家轨迹。这一差距为后续的校准提供了方向性信号。

**优势加权校准。** 利用GRPO的组归一化优势 $\hat{A}_i$，取绝对值 $|\hat{A}_i|$ 作为**组稀有度权重**。Figure 4揭示了其物理含义：在一个采样组内，正确响应的频率越低，其对应的 $|\hat{A}_i|$ 越大。因此，$|\hat{A}_i|$ 天然地放大了对低频正确响应的强化力度，同时抑制了对高频错误响应的过度关注。

**LeakyReLU非对称门控。** 可控探索损失的核心形式为：

$$\mathcal{L}_{\mathrm{exploration}} = |\hat{A}_i| \cdot \mathrm{LeakyReLU}(-s_i \cdot \Delta \ell_i, \alpha)$$

其中 $s_i \in \{+1, -1\}$ 为响应正确性信号（正确为+1，错误为-1）。LeakyReLU的负斜率参数 $\alpha \in (0, 1)$ 实现了非对称梯度门控：
- 当模型对**正确响应**的偏好不足（$s_i=+1$ 且 $\Delta \ell_i < 0$）时，输入为正，LeakyReLU输出完整梯度，强化该响应；
- 当模型对**错误响应**过度自信（$s_i=-1$ 且 $\Delta \ell_i > 0$）时，输入为负，梯度被 $\alpha$ 缩放，以受控方式抑制该响应。

$\alpha$ 因此成为调节探索强度的关键旋钮：$\alpha$ 越小，对过自信错误的抑制越温和，策略保持更高熵；$\alpha$ 越大，抑制越激进，策略趋于确定性。

### 3.3 最终训练目标

将可控探索损失集成到GRPO的PPO式裁剪目标中，得到CalibRL的完整优化目标：

$$\mathcal{J}(\theta) = \mathbb{E}_{q \sim \mathcal{D}, \tau \sim \pi_{\theta}(\cdot|q)} \sum_{t=1}^{|\tau|} \min(r_{i,t}(\theta) \hat{A}_{i,t}, \mathrm{clip}(r_{i,t}(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_{i,t}) - \lambda \mathcal{L}_{\mathrm{exploration}}$$

其中 $r_{i,t}(\theta) = \frac{\pi_{\theta}(\tau_{i,t}|s_{i,t})}{\pi_{\theta_{old}}(\tau_{i,t}|s_{i,t})}$ 为重要性采样比率，$\lambda$ 平衡标准策略优化与专家引导探索。消融实验（Table 5）表明 $\lambda=0.1$ 达到最佳折衷——过大的 $\lambda$（$\geq 0.3$）会导致性能急剧下降，因为探索信号压倒了策略优化的梯度方向。

## 实验与分析

### 核心瓶颈验证：熵崩溃与探索困境

在多模态大语言模型的RLVR训练中，直接模仿专家轨迹会导致策略熵快速下降。Figure 1的训练动态曲线清晰地揭示了这一现象：GRPO基线在训练后期熵值持续衰减，策略逐渐丧失多样性；而SFT+GRPO虽维持较高熵值，但其奖励曲线几乎停滞，准确率显著低于纯GRPO，表明无引导的高熵状态并不能转化为有效的探索。CalibRL通过将专家数据视为分布基线而非绝对目标，在保持较高策略熵（1.4968）的同时实现了奖励和准确率的持续提升，验证了“可控探索”这一核心设计理念的有效性（Table 15）。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_5wxyCidRsK/figures/004_Figure_1.jpg]]
*Figure 1: Entropy, reward, and accuracy curves of different methods. We split the entropy comparison into two panels for clarity*

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_5wxyCidRsK/figures/022_Table_15.jpg]]
*Table 15: Statistical data points from our trained checkpoints*

### 主实验结果

#### 域内几何推理任务

Table 1展示了在GeoEval、Geo3K、GeoQA三个域内几何推理基准上的性能对比。CalibRL以平均准确率44.93%显著超越所有基线方法，较GRPO（39.48%）提升5.45个百分点。在极具挑战性的GeoEval基准上，CalibRL达到33.44%，远超GRPO（26.15%）、SFT+GRPO（6.00%）以及现有混合策略方法LUFFY（38.64%）和RL-PLUS（34.68%），证明可控探索在处理困难样本上的关键优势。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_5wxyCidRsK/figures/005_Table_1.jpg]]
*Table 1: Performance comparison on in-domain geometry benchmarks*

#### 域外泛化能力

Table 2报告了七个域外基准的泛化性能。CalibRL以平均准确率59.36%领先GRPO（57.24%），在MathVista（71.90% vs 70.00%）和MMMU（56.55% vs 55.44%）等任务上均取得一致提升。Figure 2直观展示了CalibRL相对于GRPO基线的性能变化幅度，域内提升更为显著，域外任务同样保持正向增益，表明方法未牺牲泛化能力。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_5wxyCidRsK/figures/006_Table_2.jpg]]
*Table 2: Performance comparison on out-of-domain benchmarks. We present the Science benchmark as ‘Sci.’ and the Spatial Reasoning benchmark as ‘Sp.’*

#### 跨模型架构验证

Table 3显示，CalibRL在Qwen2.5VL-3B和InternVL3-8B两种不同架构的基础模型上均一致优于GRPO、LUFFY和RL-PLUS：Qwen2.5VL-3B上平均提升2.65个百分点（37.09% vs 34.44%），InternVL3-8B上提升2.05个百分点（47.42% vs 45.37%）。在更大规模的Qwen2.5-VL-32B模型上（Table 11），CalibRL同样保持3.17个百分点的平均提升，验证了方法的可扩展性。

### 消融实验：可控探索机制解构

#### 优势加权|Â_i|的必要性

Table 4的消融实验表明，移除优势加权项|Â_i|会导致所有基准的平均性能从50.59大幅下降至45.30，降幅达5.29个百分点。Figure 4揭示了|Â_i|的物理含义：在每组10个样本中，|Â_i|与奖励频率呈反向关系——低频（稀有）响应的|Â_i|值更大，从而获得更强的更新幅度，实现对分布尾部的校准强化。这一机制是维持策略熵和提升性能的核心驱动力。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_5wxyCidRsK/figures/009_Table_4.jpg]]
*Table 4: Ablation studies on the controllable exploration objective. We present the Science benchmark as ‘Sci.’ and the Spatial Reasoning benchmark as $\mathrm { \cdot } \mathrm { s p . }$ ’. The highlighted row represents our optimal results. Bold and underlined values denote the best and second-best results, respectively

#### LeakyReLU的探索强度调节

Table 4同时展示了LeakyReLU负斜率α的调节效果。α=0.5达到最佳平均性能50.59，α=0.3时性能降至50.02，α=0.8时进一步降至49.30。Figure 3的熵演化曲线直观验证了这一机制：较大的α值导致更高的训练熵，表明LeakyReLU的非对称梯度门控能够有效控制探索强度——当输入为负时，梯度被缩放为α倍，抑制过自信更新；α越大，抑制越弱，探索越强。

![[assets/figures/papers/paper_list_l2_https_openreview_net_forum_id_5wxyCidRsK/figures/011_Figure_3.jpg]]
*Figure 3: Entropy evolution during training for different α values in our framework. We split the comparison into two panels for clarity. The curves demonstrate how α controls exploration strength*

#### 平衡权重λ的敏感性

Table 5显示，λ=0.1在标准策略优化与专家引导探索之间达到最佳折衷。λ过小（0.01）时探索信号不足，平均性能降至49.64；λ过大（≥0.3）时专家引导过强，性能急剧下降至47.53。这一结果表明可控探索需要精细的权重平衡。

#### 与通用熵控制方法的对比

Table 6将CalibRL与熵正则化、KL-Cov、Clip-Cov等通用熵控制方法进行对比。直接添加熵系数（0.01）反而损害性能（36.79% vs GRPO的39.48%），KL-Cov略有改善（40.55%），而CalibRL以44.93%显著领先。这证明CalibRL并非简单地维持高熵，而是通过专家基线引导探索方向，避免了无引导随机探索的效率损失。

#### 激活函数与参考基线的选择

Table 7验证了LeakyReLU的非对称性对性能的关键贡献：其表现优于ReLU、Sigmoid等对称或单侧激活函数。Table 8表明，使用专家轨迹作为参考基线显著优于使用参考策略基线，专家知识提供的校准信号更有价值。

### 失败模式与局限性

1. **专家数据质量依赖**：当使用能力较弱的Qwen2.5-VL-72B替代GPT-4o作为专家时，性能提升幅度明显减小（Table 13），表明方法效果与专家能力正相关。
2. **长度偏好风险**：Δℓ_i的对数概率计算可能引入轻微的长度偏好，尽管长度归一化消融实验（Table 12）表明该影响较小且未损害正确性学习。
3. **任务领域局限**：当前实验主要集中在几何和数学推理任务，在其他多模态推理领域的有效性有待进一步验证。

## 方法谱系与知识库定位

### 问题定位：RLVR中的探索-模仿困境

在多模态大语言模型的RLVR（基于可验证奖励的强化学习）训练中，存在一个核心瓶颈：**熵崩溃**。当训练目标直接或间接地模仿专家轨迹时，策略的熵会快速下降，模型过早收敛到确定性行为模式，丧失了探索更优推理路径的能力。这一问题在现有的混合策略方法中尤为突出——这些方法试图在RL训练中融入专家监督，但往往导致策略要么过于确定性（模仿过强），要么进行无引导的随机探索（探索失控），两者均导致性能下降。

**CalibRL** 的提出正是为了解决这一困境。其核心洞察在于：将专家监督的角色从“绝对目标”重新定义为“分布校准基线”，使得对正确但低频响应的强化和对过自信错误的抑制都能以受控方式进行，从而在保留策略熵的同时引导探索方向。

### 方法谱系中的定位

CalibRL 位于**混合策略RLVR**这一方法分支，其前身和同期工作构成了清晰的方法演进脉络：

**纯RL基线**：
- **GRPO**（Shao et al., 2024）：采用组归一化优势进行策略优化，是当前RLVR训练的标准范式。GRPO不利用任何专家数据，完全依赖模型自身采样进行探索，在困难样本上探索效率受限。

**顺序范式**：
- **SFT+GRPO**：先通过监督微调让模型模仿专家行为，再进行GRPO训练。这一范式的问题在于：SFT阶段已经将策略推向高置信度的确定性区域，后续RL训练难以有效探索（Figure 1显示其熵异常偏高但奖励停滞，准确率极低）。

**混合策略方法**：
- **LUFFY**（Yan et al., 2025）：采用离策略指导的混合优化方法，利用专家数据进行直接最大似然或作为离策略奖励信号。
- **RL-PLUS**（Dong et al., 2025）：通过多重要性采样与探索优势塑造来融合专家信息。
- **DAPO**：采用更高裁剪阈值的RL方法。

上述混合策略方法的共同问题是：它们将专家数据视为需要逼近的目标，而非校准参考。这导致模仿信号与探索需求之间存在根本性冲突——强化专家行为的同时不可避免地压缩策略熵。

**CalibRL的差异化设计**：
CalibRL通过三个关键机制实现了可控探索，从根本上区别于上述方法：

1. **分布基线而非绝对目标**：专家数据用于计算相对偏好 $\Delta \ell_i = \log \pi_{\theta}(\tau_i^{\text{policy}}|q_i) - \log \pi_{\theta}(\tau_i^{\text{expert}}|q_i)$，衡量模型对自身响应与专家响应的相对偏好，而非直接最大化专家似然。

2. **优势加权校准**：利用组内绝对优势 $|\hat{A}_i|$ 作为稀有度权重。在组采样中，正确但罕见的响应具有更高的 $|\hat{A}_i|$ 值（Figure 4验证了这一关系），从而获得更大的更新幅度，实现对分布尾部的有效校准。

3. **LeakyReLU非对称门控**：通过可调节的负斜率 $\alpha$ 控制对过自信错误的抑制强度。当 $s_i \cdot \Delta \ell_i < 0$ 时（即模型对错误响应过于自信），梯度被 $\alpha$ 缩放，避免过度惩罚导致的熵崩溃。

消融实验（Table 4）提供了决定性证据：移除优势加权 $|\hat{A}_i|$ 导致所有基准的平均性能从50.59大幅下降至45.30，验证了组稀有度权重对维持熵和提升性能的必要性。训练后统计（Table 15, Appendix F）进一步显示，CalibRL的策略熵为1.4968，远高于LUFFY（0.0881）和RL-PLUS（0.3452），且奖励更高，直接证实了其校准机制有效缓解了熵崩溃。

### 适用边界与局限

**专家数据依赖性**：
CalibRL的性能提升幅度与专家数据质量正相关。当使用能力较弱的专家模型（如Qwen2.5-VL-72B替代GPT-4o）时，性能提升幅度减小（Table 13）。这意味着该方法在专家知识不可靠的场景下，校准信号本身可能引入偏差。

**任务领域限制**：
现有实验主要集中在几何推理（GeoEval、Geo3K、GeoQA）和数学/科学推理（MathVista、MMMU、ScienceQA等）任务上。尽管在域外基准上展现了良好的泛化能力（平均提升+2.12个百分点，Table 2），但在其他多模态推理领域（如视觉常识推理、跨模态对齐等）的有效性有待进一步验证。

**潜在的长度偏好**：
$\Delta \ell_i$ 的计算基于序列级别的对数概率比较，可能引入微弱的长度偏好。消融实验（Table 12）表明这一影响较小且未损害正确性学习，但在对长度极其敏感的任务中仍需注意。

**超参数敏感性**：
$\alpha$ 和 $\lambda$ 的选择对性能有显著影响。$\alpha=0.5$ 和 $\lambda=0.1$ 为实验确定的最优值，过高或过低均导致性能下降（Table 4, Table 5）。在实际部署中可能需要针对不同任务进行调参。

### 开放问题

1. **专家质量的自适应校准**：当专家能力参差不齐时，如何自动调整校准强度，而非依赖固定的 $\alpha$ 和 $\lambda$？这可能需要引入不确定性感知的权重机制。

2. **多模态推理的通用性**：CalibRL在几何和数学推理上验证有效，但其核心机制（对数概率差距、优势加权）是否能推广到需要开放式生成或主观评价的任务，尚待探索。

3. **与更先进RL算法的结合**：CalibRL的探索校准模块是作为GRPO的附加损失项设计的。该设计范式是否能与更先进的策略优化算法（如PPO的变体）无缝集成，值得进一步研究。

4. **理论收敛性分析**：虽然实验表明CalibRL有效缓解了熵崩溃，但缺乏对混合目标 $\mathcal{J}(\theta) = \mathcal{J}_{\text{GRPO}} - \lambda \mathcal{L}_{\text{exploration}}$ 收敛性质的理论分析，特别是非对称门控如何影响策略的平稳分布。

## 原文 PDF

![[paperPDFs/ICLR_2026/Controllable_Exploration_in_Hybrid_Policy_RLVR_for_Multi_Modal_Reasoning.pdf]]
