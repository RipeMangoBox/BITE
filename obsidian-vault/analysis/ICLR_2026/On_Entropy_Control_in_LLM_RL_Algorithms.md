---
title: "On Entropy Control in LLM-RL Algorithms"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/On_Entropy_Control_in_LLM_RL_Algorithms.pdf
project_link: null
code_link: null
openreview_forum_id: LqazVN5epT
aliases:
- ECLRA
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将熵计算限制在基于当前策略top-p概率的缩减令牌空间（夹持），并重新归一化策略分布，从而在保留探索能力的同时大幅降低偏差；同时根据夹持熵值自适应调整系数，动态平衡探索与利用。"
primary_logic: "在LLM的极大动作空间中，传统熵最大化会均等提升大量无关令牌的概率，产生巨大的偏差。通过只对高概率令牌（即可能包含正确输出的紧凑子集）计算熵并正则化，可以更精准地鼓励有效探索，维持熵水平稳定，从而持续提升策略性能。"
claims:
- "AEnt在两种实验设置、六个基准中的五个上取得最优性能，显著优于GRPO和EntReg。"
- "AEnt成功防止了GRPO的熵塌陷，并在塌陷时间点后继续提升测试分数，而GRPO和EntReg则趋于平台。"
- "自适应系数相比固定系数能更好地控制熵和响应长度，避免训练中熵爆发及重复推理模式。"
- "MATH-Hard (Setting a) 上 准确率 = 0.552"
---

# On Entropy Control in LLM-RL Algorithms

> [!tip] 核心洞察
> 在LLM的极大动作空间中，传统熵最大化会均等提升大量无关令牌的概率，产生巨大的偏差。通过只对高概率令牌（即可能包含正确输出的紧凑子集）计算熵并正则化，可以更精准地鼓励有效探索，维持熵水平稳定，从而持续提升策略性能。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | LLM-RL算法中的熵控制：自适应夹持熵正则化方法 |
| 英文题名 | On Entropy Control in LLM-RL Algorithms |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=LqazVN5epT) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AEnt |
| Dataset | MATH-Hard (Setting a), MATH-Hard (Setting b), AIME24 (Setting a), AIME24 (Setting b) |

> [!tip] 效果简介
> - MATH-Hard (Setting a) 上，准确率 为 0.552，对比 GRPO 0.524，变化 +0.028。
> - MATH-Hard (Setting b) 上，准确率 为 0.813，对比 GRPO 0.773，变化 +0.040。
> - AIME24 (Setting a) 上，准确率 为 0.217，对比 GRPO 0.192，变化 +0.025。

## 概要

大语言模型强化学习（LLM-RL）中，熵正则化长期被视为维持探索、防止策略过早收敛的重要手段。然而，该工作指出，在LLM的极大动作空间（词汇量可达数万）且最优输出高度稀疏的场景下，传统熵正则化会均等提升大量无关令牌的概率，引入严重的偏差，导致增益微弱甚至无效。同时，固定熵系数无法适应训练过程中熵的剧烈波动，常使策略过早停滞或失控。

针对上述瓶颈，本文提出**自适应夹持熵正则化方法 AEnt**。其核心操控变量有二：其一，将熵的计算限制在基于当前策略 top-p 概率的缩减令牌空间（夹持），并重新归一化策略分布，从而在保留探索能力的同时大幅降低偏差；其二，根据夹持熵值与预设区间的偏离程度自适应调整熵系数，动态平衡探索与利用。

实验证据表明，AEnt 在两种训练设置、六个数学推理基准中的五个上取得最优性能（Table 1），显著优于 GRPO 与 EntReg。AEnt 成功防止了 GRPO 的熵塌陷，并在塌陷时间点后继续提升测试分数，而 GRPO 和 EntReg 则趋于平台（Figure 3a, Figure 4a）。消融实验进一步证实，自适应系数相比固定系数能更好地控制熵和响应长度，避免训练中熵爆发及重复推理模式（Figure 5）。

在方法谱系上，AEnt 属于基于策略梯度的 LLM-RL 正则化方法，其基础策略优化模块采用 **GRPO**（Shao et al., 2024）的 PPO-clip 目标，对比基线包括不使用熵正则化的 GRPO 以及使用传统全动作空间熵正则化的 **EntReg**（Mnih et al., 2016; Schulman et al., 2017）。AEnt 的独特贡献在于将熵正则化从全动作空间迁移至动态缩减的夹持空间，并引入自适应系数机制，为LLM-RL中的探索-利用平衡提供了新的控制维度。

当前方法仍存在若干局限：夹持空间的选择缺乏理论指导，依赖经验调参；实验仅在 1.5B 和 7B 规模模型上进行；缺少对夹持熵正则化的理论收敛性分析；自适应系数的超参数仍需手动设定，跨任务迁移性未经验证。



### 大语言模型强化学习中的熵正则化困境

将强化学习（RL）应用于大语言模型（LLM）的微调已成为提升模型推理能力的主流范式，典型代表如 **GRPO**（Shao et al., 2024）。在此类方法中，策略优化通常以最大化期望累积奖励为目标。然而，LLM的动作空间——即词汇表大小——极为庞大（通常达$10^4$–$10^5$量级），且每个状态下真正“正确”或“有用”的令牌仅占极小比例，即最优动作具有高度稀疏性。这一结构性特征使得传统RL中的探索机制面临根本性挑战。

熵正则化是RL中经典的探索促进手段，其核心思想是在策略优化目标中附加一个熵奖励项：

$$V_{\lambda}^{\pi_{\theta}}(\mathcal{D}) := V^{\pi_{\theta}}(\mathcal{D}) + \lambda \mathcal{H}(\pi_{\theta})$$

其中 $\mathcal{H}(\pi_{\theta})$ 为策略在完整动作空间上的熵，$\lambda$ 为熵系数。理论直觉上，最大化熵可以鼓励策略保持随机性，避免过早收敛到次优解。然而，在LLM-RL场景下，这一直觉遭遇了严重的现实背离。

### 传统熵正则化的双重失效机制

**偏差问题**：在极大动作空间中，标准策略熵 $\mathcal{H}(\pi_{\theta})$ 的计算涉及对所有可能令牌的概率求和。由于最优令牌极为稀疏，熵最大化会均等地提升大量无关令牌的概率——这些令牌对任务毫无贡献，却因数量庞大而主导了熵的值。其结果是：熵正则化引入的偏差远大于其带来的探索收益，导致增益微弱甚至无效。本文的合成MDP实验（Figure 1）直接验证了这一点：在动作空间大小为$10^5$且最优动作日益稀疏的受控环境中，传统熵正则化的性能随稀疏度增加而急剧下降，而本文提出的夹持熵正则化则始终保持稳定。

**熵波动与固定系数的矛盾**：即使采用熵正则化，训练过程中策略熵本身会发生剧烈波动。如 Figure 2 所示，GRPO配合恒定熵系数时，熵值在训练早期可能爆发式增长，随后又迅速塌陷。固定的 $\lambda$ 完全无法适应这种动态变化：当熵过高时，固定的奖励会进一步放大探索偏差；当熵过低时，固定的奖励又不足以阻止策略的确定性塌陷。这种“一刀切”的系数设计使得熵正则化在LLM-RL中形同虚设——本文实验表明，熵正则化的GRPO（EntReg，参考Mnih et al., 2016; Schulman et al., 2017）相比基础GRPO仅带来微不足道的增益。

### 核心洞察与本文动机

上述困境的根源在于：**传统熵正则化将探索压力均匀分布在全部动作空间上，而LLM的有效探索仅需在一个紧凑的、由高概率令牌构成的子空间中进行**。换言之，策略本身已经通过其概率分布隐含地标识了哪些令牌是“值得考虑的”——那些概率极低的令牌几乎不可能被采样，对其施加熵奖励只会徒增偏差。

基于此洞察，本文提出 **AEnt（Adaptive Entropy）**方法，其动机可归结为两个关键设计：

1. **夹持熵（Clamped Entropy）**：将熵的计算限制在基于当前策略 top-$(1-p)$ 概率的缩减令牌空间上，并在该子空间内重新归一化策略分布后再计算熵。这从根本上切断了无关令牌对熵奖励的贡献，大幅降低偏差的同时保留了有效探索能力。

2. **自适应熵系数**：根据夹持熵的实时水平动态调整 $\lambda$——当熵低于预设下界时增大系数以鼓励探索，当熵高于预设上界时减小系数以抑制偏差。这使得探索-利用的平衡能够随训练进程自动校准。

通过这两项机制，AEnt旨在解决LLM-RL中熵正则化“有理论却无实效”的根本矛盾，为策略优化提供持续、稳定的探索信号。



## 核心方法与创新机理

本工作提出的 **AEnt**（Adaptive Clamped Entropy Regularization）方法，针对 LLM-RL 中传统熵正则化失效的两个关键瓶颈，引入了两项紧密耦合的创新机制。

### 瓶颈一：全动作空间熵正则化的巨大偏差

传统熵正则化在标准 RL 中通过鼓励探索来提升策略性能，但在 LLM 场景下面临根本性挑战：**词汇量级（通常数万）的动作空间与极度稀疏的最优输出之间存在尖锐矛盾**。理论分析（Proposition 1）表明，熵正则化虽然能收紧策略梯度与最优策略之间的次优性界（将 $\epsilon$ 的依赖从线性改善为平方），但同时引入了一个与动作空间大小 $|\mathcal{A}|$ 正相关的偏差项 $\lambda H \log \frac{|\mathcal{A}|}{|\mathcal{A}_H^*(s_0)|^{1/H}}$。在 LLM 的巨型动作空间中，这一偏差项会均等地提升大量无关令牌的概率，使得正则化带来的增益被严重稀释甚至抵消——如 Figure 1 的合成 MDP 实验所示，当最优动作数量降至 5 以下时，传统熵正则化几乎不产生任何性能增益。

### 创新一：夹持熵（Clamped Entropy）

AEnt 的核心操作是将熵的计算从完整动作空间 $\mathcal{A}$ **压缩**到每个状态 $s$ 上基于当前策略 $\pi_\theta$ 的 top-$(1-p)$ 高概率令牌构成的缩减空间 $\mathcal{A}(s)$，并在该空间上重新归一化策略分布后计算熵：

$$\tilde{\mathcal{H}}(\pi_{\theta}) := - \sum_{t=0}^{H-1} \mathbb{E}_{s_{t} \sim \pi_{b}} \bigg[ \sum_{a \in \mathcal{A}(s_{t})} \tilde{\pi}_{\theta}(a|s_{t}) \log \tilde{\pi}_{\theta}(a|s_{t}) \bigg]$$

其中 $\tilde{\pi}_{\theta}(a|s) = \frac{\exp(\theta_{s,a})}{\sum_{a \in \mathcal{A}(s)} \exp(\theta_{s,a})}$，$\mathcal{A}(s) = \{ \text{top } (1-p) \text{ percent tokens in } \pi_{\theta}(\cdot|s) \}$。

这一设计的**因果逻辑**在于：正确输出通常仅分布在少数高概率令牌的紧凑子集中，而低概率令牌几乎不可能构成正确答案。通过将熵正则化限制在“可能包含正确答案”的令牌集合上，夹持熵在保留探索能力的同时，**大幅削减了传统熵正则化因均等提升无关令牌概率而引入的偏差**。Figure 1 的受控实验直接验证了这一机制——在最优动作极度稀疏（≤5）的场景下，夹持熵正则化仍能持续提供性能增益，而传统熵正则化已完全失效。

### 瓶颈二：固定熵系数无法适应训练中的熵剧烈波动

即使采用夹持熵，若使用固定熵系数 $\lambda$，LLM-RL 训练仍会遭遇严重不稳定。如 Figure 2 所示，GRPO 配合恒定熵系数时，策略熵在训练中后期出现剧烈波动。这是因为 LLM 策略在强化学习微调过程中，其输出分布的集中度会发生显著变化，固定的正则化强度无法动态匹配这种变化——熵过低时探索不足导致策略停滞，熵过高时则引发推理模式崩塌（如响应长度失控、重复生成）。

### 创新二：自适应熵系数（Adaptive Entropy Coefficient）

AEnt 在每个全局步结束时，根据当前夹持熵 $\tilde{\mathcal{H}}(\pi_{\theta})$ 与预设目标区间 $[\tilde{\mathcal{H}}_{\text{low}}, \tilde{\mathcal{H}}_{\text{high}}]$ 的偏离程度，自动调整熵系数：

$$\lambda' \leftarrow \mathrm{Proj}_{[\lambda_{\mathrm{low}}, \lambda_{\mathrm{high}}]} \left[ \lambda - \beta \min(\tilde{\mathcal{H}}(\pi_{\theta}) - \tilde{\mathcal{H}}_{\mathrm{low}}, 0) + \beta \min(\tilde{\mathcal{H}}_{\mathrm{high}} - \tilde{\mathcal{H}}(\pi_{\theta}), 0) \right]$$

该更新规则的**控制逻辑**清晰：当夹持熵低于下限时增大 $\lambda$ 以加强探索，高于上限时减小 $\lambda$ 以降低偏差，始终将策略熵维持在有利于持续学习的区间内。Figure 5 的消融实验证实，自适应系数相比固定系数能有效防止训练中的熵爆发和响应长度失控，而测试分数保持相当。

### 整体优化目标

将两项创新统一，AEnt 的优化目标为：

$$\mathcal{L}_{\mathrm{AEnt}}(\theta; \lambda) = \mathcal{L}_{\mathrm{PO}}(\theta) + \lambda \tilde{\mathcal{H}}(\pi_{\theta})$$

其中 $\mathcal{L}_{\mathrm{PO}}$ 为基础策略优化损失（本工作采用 GRPO 的 PPO-clip 目标），$\lambda$ 按上述自适应规则动态调整。这一设计实现了**探索偏差控制**（通过夹持空间）与**探索强度调节**（通过自适应系数）的解耦与协同，使 LLM-RL 训练能够在极大动作空间中持续、稳定地提升推理能力。



AEnt 的整体 pipeline 围绕“策略采样—GRPO 策略优化—夹持熵计算—自适应系数调整”四个模块构建，形成一个闭环的在线强化学习流程。

**输入**：一个预训练的 LLM 策略 $\pi_\theta$，以及一个数学推理任务数据集 $\mathcal{D}$（如 MATH 或 OpenR1-math 子集），其中每个样本 $s_0 \sim \mathcal{D}$ 是一个问题提示。

**核心流程**（参见 Algorithm 1）：

1. **策略采样**：在每个全局步开始，使用上一个全局步的策略 $\pi_b$ 进行 rollout，从当前策略分布中采样生成批量轨迹（即推理链与最终答案）。这些轨迹随后通过任务奖励函数（如答案正确性判断）获得奖励信号。

2. **基于 GRPO 的策略优化**：将收集到的轨迹和奖励输入 GRPO 的 PPO-clip 目标 $\mathcal{L}_{\mathrm{PO}}(\theta)$，作为基础策略优化损失。GRPO 通过组内相对优势估计来更新策略参数 $\theta$。

3. **夹持熵计算**：在策略更新的同时，对每个状态 $s_t$ 执行夹持操作——选取当前策略 $\pi_\theta(\cdot|s_t)$ 下概率最高的 top-$(1-p)$ 百分比的令牌构成缩减动作空间 $\mathcal{A}(s_t)$，在该空间上重新归一化策略分布 $\tilde{\pi}_\theta$，并计算夹持熵 $\tilde{\mathcal{H}}(\pi_\theta)$。

4. **自适应系数调整**：每个全局步结束时，根据夹持熵 $\tilde{\mathcal{H}}(\pi_\theta)$ 与预设区间 $[\tilde{\mathcal{H}}_{\mathrm{low}}, \tilde{\mathcal{H}}_{\mathrm{high}}]$ 的偏离程度，按公式 (4.1) 自动调整熵系数 $\lambda$，并将其投影到 $[\lambda_{\mathrm{low}}, \lambda_{\mathrm{high}}]$ 区间。更新后的 $\lambda$ 用于下一全局步的优化目标。

**输出**：经过多轮迭代后的优化策略 $\pi_\theta$，该策略在保持适度探索熵水平的同时，在数学推理基准上取得更高的测试准确率。

**模块间的因果链路**：
- 夹持熵计算模块通过将熵估计限制在高概率令牌的紧凑子集上，大幅降低了传统全空间熵正则化引入的偏差，这是 AEnt 优于 EntReg 的根本原因。
- 自适应系数调整模块解决了固定熵系数在 LLM-RL 训练中无法应对熵剧烈波动的问题——当熵过低时增大 $\lambda$ 鼓励探索，过高时减小 $\lambda$ 抑制偏差，从而防止 GRPO 中常见的熵塌陷现象。
- 最终优化目标整合为 $\mathcal{L}_{\mathrm{AEnt}}(\theta; \lambda) = \mathcal{L}_{\mathrm{PO}}(\theta) + \lambda \tilde{\mathcal{H}}(\pi_\theta)$，使策略在提升任务奖励的同时维持健康的探索水平。

**证据支撑**：该框架的有效性由 Table 1 中 AEnt 在 6 个基准中的 5 个上取得最优成绩，以及 Figure 3a/4a 中 AEnt 在 GRPO 熵塌陷后继续提升测试分数的现象所证实。消融实验（Figure 5, Figure 6）进一步验证了自适应系数和夹持操作各自的贡献。



### 3.1 瓶颈洞察：全动作空间熵正则化的偏差

在LLM-RL中，策略的动作空间为整个词汇表 $\mathcal{A}$（通常 $>10^5$），而数学推理等任务的最优输出极为稀疏。传统熵正则化目标为：
$$V^{\pi_\theta}(\mathcal{D}) + \lambda \mathcal{H}(\pi_\theta)$$
其中策略熵定义为：
$$\mathcal{H}(\pi_\theta) = - \sum_{t=0}^{H-1} \mathbb{E}_{s_t \sim \pi_\theta} \left[ \sum_{a \in \mathcal{A}} \pi_\theta(a|s_t) \log \pi_\theta(a|s_t) \right]$$

最大化该熵项会均等提升**所有**令牌的概率，包括大量与正确推理无关的令牌。这引入了严重的偏差，导致熵正则化增益微弱甚至无效。受控MDP实验（Figure 1）证实：当最优动作数 $>10$ 时熵正则化有效，但当最优动作极度稀疏（$\leq 5$）时完全失效。

### 3.2 夹持熵（Clamped Entropy）：缩减动作空间

AEnt的核心创新是将熵计算限制在**基于当前策略top-p概率的缩减令牌空间**上。具体定义：

$$\tilde{\mathcal{H}}(\pi_{\theta}) := - \sum_{t=0}^{H-1} \mathbb{E}_{s_{t} \sim \pi_{b}} \left[ \sum_{a \in \mathcal{A}(s_{t})} \tilde{\pi}_{\theta}(a|s_{t}) \log \tilde{\pi}_{\theta}(a|s_{t}) \right]$$

其中：
- $\mathcal{A}(s) = \{ \text{top } (1-p) \text{ percent tokens in } \pi_{\theta}(\cdot|s) \}$：仅保留当前状态下概率最高的 $(1-p)$ 百分比的令牌
- $\tilde{\pi}_{\theta}(a|s) = \frac{\exp(\theta_{s,a})}{\sum_{a \in \mathcal{A}(s)} \exp(\theta_{s,a})}$：在缩减空间上重新归一化的策略分布

**机制解释**：夹持操作将熵计算限定在可能包含正确输出的紧凑令牌子集上，避免了对大量无关令牌的均等概率提升，从而在保留探索能力的同时大幅降低了偏差。Figure 1 显示，即使在最优动作极度稀疏（$\leq 5$）的场景下，夹持熵正则化仍能带来显著的性能增益。

### 3.3 自适应熵系数：动态平衡探索与利用

固定熵系数无法适应LLM-RL训练中熵的剧烈波动（Figure 2显示熵在第200步后开始剧烈震荡）。AEnt根据夹持熵的实时水平自动调整系数 $\lambda$：

$$\lambda' \leftarrow \mathrm{Proj}_{[\lambda_{\mathrm{low}}, \lambda_{\mathrm{high}}]} \left[ \lambda - \beta \min(\tilde{\mathcal{H}}(\pi_{\theta}) - \tilde{\mathcal{H}}_{\mathrm{low}}, 0) + \beta \min(\tilde{\mathcal{H}}_{\mathrm{high}} - \tilde{\mathcal{H}}(\pi_{\theta}), 0) \right]$$

**变量含义**：
- $\tilde{\mathcal{H}}_{\mathrm{low}}, \tilde{\mathcal{H}}_{\mathrm{high}}$：预设的夹持熵目标区间下界和上界
- $\beta$：系数调整步长
- $\lambda_{\mathrm{low}}, \lambda_{\mathrm{high}}$：熵系数的允许范围

**调节逻辑**：当夹持熵低于 $\tilde{\mathcal{H}}_{\mathrm{low}}$ 时增大 $\lambda$ 以鼓励探索，防止策略过早停滞；当夹持熵高于 $\tilde{\mathcal{H}}_{\mathrm{high}}$ 时减小 $\lambda$ 以降低偏差，防止策略失控。每次调整后将 $\lambda$ 投影到 $[\lambda_{\mathrm{low}}, \lambda_{\mathrm{high}}]$ 区间内。

### 3.4 AEnt整体优化目标

将上述组件整合，AEnt的完整优化目标为：

$$\mathcal{L}_{\mathrm{AEnt}}(\theta; \lambda) = \mathcal{L}_{\mathrm{PO}}(\theta) + \lambda \tilde{\mathcal{H}}(\pi_{\theta})$$

其中 $\mathcal{L}_{\mathrm{PO}}(\theta)$ 为基础策略优化损失（本文采用GRPO的PPO-clip目标）。在每个全局步结束时，按公式3.3更新 $\lambda$，实现自适应熵控制。

### 3.5 算法流程

AEnt的训练循环包含四个关键模块：

1. **策略采样**：使用上一个全局步的策略 $\pi_b$ 进行rollout，收集批量轨迹
2. **基于GRPO的策略优化**：以GRPO的PPO-clip目标作为基础损失 $\mathcal{L}_{\mathrm{PO}}$
3. **夹持熵计算**：在每个状态上选取top-$(1-p)$概率的令牌构成 $\mathcal{A}(s)$，计算重新归一化策略的熵 $\tilde{\mathcal{H}}(\pi_\theta)$
4. **自适应系数调整**：每个全局步结束，按公式3.3调整 $\lambda$ 并投影到 $[\lambda_{\mathrm{low}}, \lambda_{\mathrm{high}}]$

> **注意**：夹持百分比 $p$ 的选择对算法效果有显著影响（Figure 6消融实验证实），但目前缺乏理论指导，依赖经验调参。自适应系数的超参数（$\tilde{\mathcal{H}}_{\mathrm{low}}, \tilde{\mathcal{H}}_{\mathrm{high}}, \beta$）仍需手动设定，可能在不同任务间需要重新调整。



## 实验与关键发现

### 核心瓶颈的实证验证

传统熵正则化在LLM-RL中失效的根源，在于LLM巨大的动作空间（词汇量通常为$10^5$级）与数学推理任务中极稀疏的最优输出之间的结构性矛盾。论文通过一个受控合成MDP实验（**Figure 1**）清晰揭示了这一机制：在$|\mathcal{A}|=10^5$的动作空间下，当最优动作数量为10或15时，熵正则化（Entropy Regularized）相比无正则化确实能带来性能增益；但当最优动作稀疏至5个以下时，熵正则化的增益完全消失。**核心因果链**是：熵最大化会均等提升大量无关令牌的概率，引入的偏差（bias）随最优动作稀疏度增加而急剧放大，最终抵消甚至超过探索带来的收益。相比之下，夹持熵正则化（Clamped Entropy Regularization）在所有稀疏度下均保持增益，且对稀疏度变化更加鲁棒。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_LqazVN5epT/figures/004_Figure_1.jpg]]
*Figure 1: Test in a controlled MDP with a large action space of size | ${ \mathcal { A } }$ | = 1 $0 ^ { 5 }$ and increasingly sparse optimal actions*

在真实LLM-RL训练中，这一偏差问题进一步与**熵的剧烈波动**耦合。如**Figure 2**所示，GRPO配合恒定熵系数训练时，策略熵在约200步后开始剧烈震荡。固定系数无法响应这种动态变化：熵塌陷时系数不足以维持探索，熵爆发时系数又过度放大偏差，导致策略过早停滞或失控。

### 主要结果

**Table 1**汇总了在两种实验设置（Setting a和Setting b）、六个数学推理基准上的测试分数。AEnt在五个基准上取得最优，具体增益如下：

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_LqazVN5epT/figures/010_Table_1.jpg]]
*Table 1: Test scores by benchmark, where we evaluate the model with the highest average test score trained by each algorithm. Here (a), (b) indicates the two settings described in 5.1. Bold numbers indicate the best performance one on the benchmark*

| 基准 | Setting | GRPO | AEnt | Δ |
|------|---------|------|------|---|
| MATH-Hard | a | 0.524 | **0.552** | +0.028 |
| MATH-Hard | b | 0.773 | **0.813** | +0.040 |
| AIME24 | a | 0.192 | **0.217** | +0.025 |
| AIME24 | b | 0.367 | **0.392** | +0.025 |
| MATH-500 | b | 0.865 | **0.882** | +0.017 |

值得注意的是，EntReg（使用传统全动作空间熵正则化的GRPO变体）相比GRPO的提升极为有限，甚至在某些基准上几乎持平，直接验证了“传统熵正则化在LLM-RL中增益微弱”的核心论断。

**Table 3**进一步在Qwen2.5-Math-7B模型上验证了方法的可扩展性：AEnt在六个基准中的五个上取得最优，MATH-Hard分数从GRPO的0.628提升至0.657（+0.029）。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_LqazVN5epT/figures/025_Table_3.jpg]]
*Table 3: Benchmark scores of training Qwen2.5-Math-7B on 6k samples from the DeepMath dataset. Bold numbers indicate the best result on the benchmark*

### 训练动态分析

**Figure 3a**和**Figure 4a**联合揭示了AEnt的关键行为模式。在GRPO训练中，策略熵在约175步后发生塌陷（entropy collapse），此后测试分数趋于平台，不再提升。AEnt在相同时间点后不仅维持了稳定的策略熵水平，测试分数继续攀升并最终超越所有基线。这表明AEnt成功打破了“熵塌陷—性能停滞”的因果链条。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_LqazVN5epT/figures/003_Figure_3.jpg]]

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_LqazVN5epT/figures/014_Figure_4.jpg]]
*Figure 4: (b) Training DeepSeek-R1-distilled-Qwen-1.5b on a subset of OpenR1-math dataset. Figure 4: Entropy and response length trend (see also Figure 3 for test score comparison)*

**Figure 4a**还显示，AEnt的响应长度（response length）在训练全程保持紧凑且稳定，而EntReg和GRPO的响应长度则出现不同程度的膨胀或波动。结合**Figure 5**的消融结果，自适应熵系数是这一稳定性的关键：固定系数无法阻止训练中期的熵爆发，导致响应长度失控和重复推理模式；自适应系数通过将夹持熵约束在预设区间$[\tilde{\mathcal{H}}_{\text{low}}, \tilde{\mathcal{H}}_{\text{high}}]$内，动态平衡探索与利用，从而在维持准确率的同时显著提升推理效率。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_LqazVN5epT/figures/017_Figure_5.jpg]]
*Figure 5: AEnt with adaptive entropy coefficient vs with a constant coefficient. The score in this test is similar. Adaptive coefficient better controls the response length and the policy entropy*

### 消融研究

**夹持百分比$p$的敏感性**（**Figure 6**）：$p$控制夹持空间$\mathcal{A}(s)$的大小——$p$越大，保留的令牌越少，夹持越激进。实验表明，所有$p$取值下AEnt均优于GRPO基线，且较大的$p$（更激进的夹持）通常带来更好的性能。这暗示进一步压缩动作空间可能是收益递增的方向，但当前缺乏理论指导，$p$的选择仍依赖经验调参。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_LqazVN5epT/figures/020_Figure_6.jpg]]
*Figure 6: Comparison of different clamping percentage p*

**自适应系数 vs 固定系数**（**Figure 5**）：在测试分数相近的情况下，自适应系数显著更好地控制了策略熵和响应长度。固定系数在训练中期无法阻止熵的剧烈波动，导致响应长度膨胀。自适应系数通过公式
$$\lambda' \leftarrow \mathrm{Proj}_{[\lambda_{\mathrm{low}}, \lambda_{\mathrm{high}}]} \left[ \lambda - \beta \min(\tilde{\mathcal{H}}(\pi_{\theta}) - \tilde{\mathcal{H}}_{\mathrm{low}}, 0) + \beta \min(\tilde{\mathcal{H}}_{\mathrm{high}} - \tilde{\mathcal{H}}(\pi_{\theta}), 0) \right]$$
自动响应夹持熵的变化：熵过低时增大$\lambda$鼓励探索，熵过高时减小$\lambda$降低偏差。

### 时间复杂度

**Table 2**对比了各算法的计算开销。AEnt每步更新的GPU小时略高于GRPO（如Setting a: 0.256h vs 0.234h），增量主要来自夹持熵计算和系数更新。然而，由于AEnt收敛更快，达到GRPO最高分数所需的总GPU时间显著更少（Setting a: 35h vs 57h；Setting b: 186h vs 237h），实际训练效率反而更高。

![[assets/figures/papers/paper_list_l25_https_openreview_net_forum_id_LqazVN5epT/figures/021_Table_2.jpg]]
*Table 2: Time complexity comparison under different settings. “Update per step” indicates the GPU hours of forward/backward process per step; “to GRPO/highest score” indicates the total GPU hours to reach the highest score achieved by GRPO/the algorithm itself. The first and second column respectively reports the results for setting (a) and (b) described in Section 5.1*

### 失败模式与局限

1. **夹持空间选择的经验依赖性**：$\mathcal{A}(s)$的构造完全依赖top-p概率裁剪，缺乏理论指导。消融显示$p$的选择对性能有显著影响，但目前无法先验地确定最优$p$值。

2. **自适应系数的超参数敏感性**：$\tilde{\mathcal{H}}_{\text{low}}$、$\tilde{\mathcal{H}}_{\text{high}}$和$\beta$仍需手动设定，这些超参数可能难以在不同任务或模型规模间直接迁移。

3. **模型规模验证不足**：当前实验仅覆盖1.5B和7B参数规模，在更大规模模型（如70B+）上的有效性尚未验证。

4. **理论收敛性缺失**：夹持熵正则化缺乏类似于传统熵正则化的理论收敛性分析，其优化性质尚未完全阐明。



## 定位与知识库关联

### 核心瓶颈与设计动机

LLM-RL 中，策略优化通常发生在词汇量级达 $10^4$–$10^5$ 的极大离散动作空间上。传统熵正则化（如 **EntReg**，Mnih et al., 2016; Schulman et al., 2017）在该场景下面临双重失效：

1. **偏差问题**：熵最大化会均等提升大量无关令牌的概率，而数学推理等任务的最优输出极为稀疏（通常仅有少数几个令牌序列构成正确答案）。这种“均匀鼓励”引入的偏差远超其带来的探索收益，导致增益微弱甚至无效（Figure 1 的合成 MDP 实验直接验证了这一点：当最优动作数 ≤5 时，熵正则化完全失效）。
2. **系数僵化**：训练过程中策略熵会发生剧烈波动（Figure 2 显示 GRPO 在约 200 步后熵值开始大幅震荡），固定熵系数无法适应这种动态变化，导致策略过早停滞或失控。

AEnt 针对上述瓶颈，在两个维度上进行了改造：**熵计算空间**和**熵系数调节机制**。

### 方法改造点与基线对比

| 改造维度 | 基线方法 (GRPO / EntReg) | AEnt 方案 | 证据锚点 |
|---------|------------------------|----------|---------|
| **熵计算空间** | 完整词汇表 $\mathcal{A}$ 上的标准策略熵 $\mathcal{H}(\pi_\theta)$ | 基于当前策略 top-$(1-p)$ 概率令牌的缩减空间 $\mathcal{A}(s)$，重新归一化后计算的夹持熵 $\tilde{\mathcal{H}}(\pi_\theta)$ | Section 4.1, 公式 4.1 |
| **熵系数** | 固定常数 $\lambda$（如 0.002） | 根据 $\tilde{\mathcal{H}}(\pi_\theta)$ 与预设区间 $[\tilde{\mathcal{H}}_{\text{low}}, \tilde{\mathcal{H}}_{\text{high}}]$ 的偏离自动调整，并按公式 4.1 投影至 $[\lambda_{\text{low}}, \lambda_{\text{high}}]$ | Section 4.2, 公式 4.1 |
| **基础优化目标** | GRPO 的 PPO-clip 损失 $\mathcal{L}_{\text{PO}}$ | 同 GRPO，不变 | Section 4.3, 公式 4.2 |

**夹持熵的核心直觉**：在 LLM 的极大动作空间中，正确输出通常集中在概率较高的紧凑令牌子集内。通过仅对高概率令牌计算熵并正则化，AEnt 在保留有效探索能力的同时大幅降低了无关令牌的偏差干扰。自适应系数则进一步确保训练过程中熵水平维持在合理区间，避免熵塌陷（GRPO 的典型失败模式）或熵爆发。

### 适用边界与局限

**已验证的有效范围**：
- 模型规模：1.5B 和 7B 参数（Qwen2.5-Math 系列、DeepSeek-R1-Distilled-Qwen 系列）
- 任务领域：数学推理（MATH-Hard、MATH-500、AIME24、Minerva、Olympiad、AMC）
- 训练设置：两种不同的数据/超参配置（Setting a 和 Setting b），均使用 GRPO 作为基础优化器

**已知局限**（需手动验证）：
1. **夹持空间选择的经验性**：$\mathcal{A}(s)$ 的构建依赖 top-p 百分比参数，目前缺乏理论指导，效果对 $p$ 敏感（Figure 6 显示较大 $p$ 值更优，表明更激进的压缩有益，但最优选择需逐任务调参）。
2. **大规模模型未验证**：实验仅覆盖至 7B 规模，在 70B+ 模型上的有效性尚不明确。
3. **理论收敛性缺失**：夹持熵正则化的优化性质尚未完全阐明，缺少类似于传统熵正则化的理论保证。
4. **自适应系数超参数敏感**：$\tilde{\mathcal{H}}_{\text{low}}$、$\tilde{\mathcal{H}}_{\text{high}}$、$\beta$ 仍需手动设定，跨任务迁移的鲁棒性未经验证。

### 开放问题

1. **更智能的夹持空间设计**：当前仅按概率 top-p 裁剪，能否基于语义相似性对令牌聚类（如 Baram et al., 2021; Zhong et al., 2024 的冗余动作去除思路），或在状态/动作表示空间而非原始令牌空间上定义熵（Tennenholtz & Mannor, 2019; Tavakoli et al., 2018），以进一步提升效率？
2. **跨领域泛化**：夹持熵正则化在代码生成、对话系统等不同领域的 LLM 上是否依然有效？
3. **理论完善**：能否为夹持熵正则化建立类似于传统熵正则化的性能界或收敛性保证？
4. **大规模验证**：在更大参数规模（70B+）和更多计算资源下的表现有待检验。



## 原文 PDF

![[paperPDFs/ICLR_2026/On_Entropy_Control_in_LLM_RL_Algorithms.pdf]]
