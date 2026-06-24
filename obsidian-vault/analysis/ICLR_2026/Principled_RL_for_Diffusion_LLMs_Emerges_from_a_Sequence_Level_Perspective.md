---
title: "Principled RL for Diffusion LLMs Emerges from a Sequence-Level Perspective"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Principled_RL_for_Diffusion_LLMs_Emerges_from_a_Sequence_Level_Perspective.pdf
openreview_forum_id: S5YeC9llIL
aliases:
- EEBSLPO
- PRDLEFSLP
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将整个序列生成视为单一动作，采用序列级策略优化目标，以证据下界（ELBO）作为不可处理的对数似然的代理，同时引入长度归一化的重要性比率和稳定的k2 KL散度估计器，从根本上消除了动作空间与模型生成机制之间的错配。"
primary_logic: "将动作空间从token级提升到序列级，并借助ELBO代理与稳定性技术，使强化学习自然适配dLLM的全局生成特性，避免了token级分解带来的启发式误差；该方法在需要整体一致性的规划任务上效果尤为显著。"
claims:
- "序列级+ELBO（ESPO）在Sudoku消融实验中唯一实现稳定收敛至高回报，而所有token级变体均失败（图1）。"
- "ESPO在Countdown和Sudoku上分别相较基础LLaDA模型平均提升62.3和70.3个百分点，远超token级基线（表1）。"
- "仅将k2估计器施加于token级基线（d1+k2）不能带来实质提升，证明序列级框架是关键（表5）。"
- "k2 KL估计器在整个训练中表现出稳定的梯度范数，而k1和k3分别导致崩溃和急剧尖峰（图6）。"
---

# Principled RL for Diffusion LLMs Emerges from a Sequence-Level Perspective

> [!tip] 核心洞察
> 将动作空间从token级提升到序列级，并借助ELBO代理与稳定性技术，使强化学习自然适配dLLM的全局生成特性，避免了token级分解带来的启发式误差；该方法在需要整体一致性的规划任务上效果尤为显著。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 从序列级视角看扩散大语言模型的原则性强化学习 |
| 英文题名 | Principled RL for Diffusion LLMs Emerges from a Sequence-Level Perspective |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=S5YeC9llIL); [GitHub](https://github.com/ML-GSAI/ESPO) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | ESPO (ELBO-based Sequence-level Policy Optimization) |
| Dataset | GSM8K, MATH, Countdown, Sudoku |

> [!tip] 效果简介
> - GSM8K 上，平均准确率（128/256/512长度） 为 82.0 (ESPO)，对比 75.9 (LLaDA)，变化 +6.1。
> - MATH 上，平均准确率（128/256/512长度） 为 39.5 (ESPO)，对比 37.0 (LLaDA)，变化 +2.5。
> - Countdown 上，平均成功率（128/256/512长度） 为 81.0 (ESPO)，对比 18.7 (LLaDA)，变化 +62.3。

## 概述

扩散大语言模型（dLLM）通过非自回归的迭代去噪过程生成序列，在推理灵活性和可控性上展现出独特优势。然而，将现有强化学习方法（如 GRPO）直接应用于 dLLM 时面临根本性障碍：这些方法依赖自回归模型提供的逐 token 条件概率来计算重要性比率，而 dLLM 的生成机制无法自然提供此类 token 级分解。现有工作采用平均场近似或 token 级 ELBO 分解等启发式代理，但这些方案存在根本性不一致，导致训练不稳定甚至学习失败。

本文的核心洞察在于：**问题的根源并非寻找更优的 token 级代理，而是 token 级分解本身与 dLLM 的全局生成特性存在结构性错配**。为此，本文提出 **ESPO（ELBO-based Sequence-level Policy Optimization）**，将整个序列生成视为单一动作，采用序列级策略优化目标。ESPO 以证据下界（ELBO）作为不可处理的对数似然的代理，同时引入长度归一化的重要性比率和稳定的 k2 KL 散度估计器，从根本上消除了动作空间与模型生成机制之间的不匹配。

在方法定位上，ESPO 属于序列级强化学习框架，其关键设计包括：将 GRPO 的动作空间从 token 级提升到序列级；利用 ELBO 替代真实对数似然；通过除以序列长度 L 进行重要性比率归一化以防止指数爆炸；采用 MSE 形式的 k2 KL 估计器替代含指数项的不稳定 k3 估计器。

实验结果表明，ESPO 在规划密集型任务上效果尤为显著：在 Countdown 和 Sudoku 上分别相较基础模型 **LLaDA-8B-Instruct**（Nie et al., 2025）平均提升 62.3 和 70.3 个百分点，远超 token 级基线方法。消融实验证实，仅将 k2 估计器施加于 token 级基线无法带来实质提升，序列级框架本身才是性能增益的关键来源。在数学推理（GSM8K、MATH）和代码生成（HumanEval、MBPP）任务上，ESPO 同样取得一致提升，尽管幅度受预训练模型能力天花板制约。

## 背景与动机

### 扩散大语言模型的生成范式

扩散大语言模型（dLLM）采用非自回归迭代去噪的方式生成序列。与自回归模型逐token预测不同，dLLM的生成过程从完全掩码的状态开始，通过多步去噪逐步揭示整个序列。其前向扩散过程以概率 $t$ 将token替换为掩码 $\mathbf{M}$：

$$q_t(y_t|y,x) = \prod_{i=1}^{L} q_t(y_t^i|y^i,x) \quad \mathrm{and} \quad q_t(y_t^i|y^i,x) = \begin{cases} 1-t, & y_t^i = y^i, \\ t, & y_t^i = \mathbf{M} \end{cases}$$

训练时，模型通过证据下界（ELBO）优化参数，该下界作为不可处理的对数似然 $\log \pi_{\theta}(y|x)$ 的代理：

$$\mathcal{L}_{\theta}(y|x) \triangleq \mathbb{E}_{t \sim \mathcal{U}[0,1]} \mathbb{E}_{y_t \sim q_t(y_t|y,x)} \left[ \frac{1}{t} \sum_{i=1}^{L} \mathbf{1}[y_t^i = \mathbf{M}] \log p_{\theta}(y^i|y_t, x) \right] \leq \log \pi_{\theta}(y|x)$$

这一生成范式的核心特征是**全局性**：模型在去噪的每一步同时考虑所有位置，序列的各个token并非独立生成，而是通过迭代过程协同涌现。

### 现有强化学习方法的根本错配

主流强化学习方法（如GRPO）专为自回归模型设计，其核心操作依赖**逐token的条件概率分解**。以GRPO为例，其重要性比率建立在token级策略比率之上：

$$\rho^{k,(i)} = \frac{\pi_{\theta}(y^{k,(i)} \vert x, y^{<k,(i)})}{\pi_{\theta_{\mathrm{old}}}(y^{k,(i)} \vert x, y^{<k,(i)})}$$

然而，dLLM无法自然提供这种逐token的条件概率。为将现有RL方法强行适配到dLLM，研究者采用了两种启发式代理：

- **平均场近似**：假设各token独立，将联合分布分解为边缘分布的乘积。这一假设与dLLM的全局耦合生成机制根本矛盾。
- **token级ELBO分解**：将序列ELBO按token位置拆解，以单个token对ELBO的贡献作为其条件似然的代理：

$$\mathcal{L}_{\theta}^{k}(y | x) \triangleq \mathbb{E}_{t \sim \mathcal{U}[0,1]} \mathbb{E}_{y_t \sim q_t(y_t | y, x)} \left[ \frac{1}{t} \mathbf{1}[y_t^{k} = \mathbf{M}] \log p_{\theta}(y^{k} | y_t, x) \right]$$

这两种方案均存在**根本性不一致**：它们试图将序列级生成过程强行拆解为独立的token级决策，导致动作空间与模型生成机制之间的结构性错配。实验证据表明，这种错配直接导致训练不稳定或学习失败——在Sudoku消融实验中，所有token级变体均无法收敛至高回报，而序列级方案则稳定收敛（Figure 1）。

### 本文动机：从序列级视角重构RL框架

上述分析揭示了一个关键洞察：**问题不在于寻找更好的token级代理，而在于token级分解本身就不适用于dLLM**。dLLM的生成本质上是将整个序列视为一个整体动作，而非一系列独立子动作的组合。

基于这一认识，本文提出**ESPO（ELBO-based Sequence-level Policy Optimization）**，其核心设计原则包括：

1. **动作空间提升**：将整个序列生成视为单一动作，从根本上消除动作空间与模型生成机制之间的错配。
2. **序列级似然代理**：直接使用序列级ELBO作为不可处理的对数似然的代理，避免任何token级分解带来的启发式误差。
3. **稳定性保障**：引入长度归一化的重要性比率和稳定的k2 KL散度估计器，解决序列级框架在大规模训练中面临的数值稳定性挑战。

该方法在需要整体一致性的规划任务上效果尤为显著——Countdown和Sudoku任务上分别相较基础模型平均提升62.3和70.3个百分点，远超所有token级基线（Table 1）。

## 核心创新

ESPO的核心贡献在于将扩散大语言模型（dLLM）的强化学习从token级动作空间提升至序列级动作空间，从根本上消除了现有方法中动作分解与模型生成机制之间的结构性错配。这一转变由四个相互耦合的**changed slots**构成，每个slot都针对dLLM的非自回归、全局去噪特性进行了专门设计。

### 1. 动作空间：从token级到序列级

自回归模型的强化学习（如GRPO）天然依赖逐token的条件概率分解，但dLLM通过迭代去噪生成整个序列，无法提供这种token级分解。现有工作（如**diffu-GRPO** (Zhao et al., 2025)和**wd1** (Tang et al., 2025)）试图用平均场近似或token级ELBO分解来构造代理概率，但这些启发式方法存在根本性不一致——token级分解强行将一个全局生成过程割裂为独立步骤，导致训练不稳定甚至完全失败。

ESPO将整个序列的生成视为**单一原子动作**，直接优化序列级策略目标。这一设计的因果机制在于：dLLM的去噪过程本质上是全局的——每一步去噪都同时影响所有token的分布，因此将动作空间提升到序列级，使策略优化目标与模型的实际生成机制在结构上完全对齐。图1的消融实验提供了决定性证据：在Sudoku任务上，所有token级变体（无论使用平均场还是ELBO代理）均无法有效学习，而序列级+ELBO的组合是唯一实现稳定收敛并达到最高回报的方案。

### 2. 似然代理：序列级ELBO

由于dLLM的序列对数似然$\log \pi_\theta(y|x)$不可处理，ESPO采用序列级证据下界（ELBO）作为代理。与先前工作中将ELBO按token拆解的做法不同，ESPO直接使用完整序列的ELBO（Eq. 2或Eq. 3），不对其进行任何token级分解：

$$\mathcal{L}_{\theta}(y|x) \triangleq \mathbb{E}_{t \sim \mathcal{U}[0,1]} \mathbb{E}_{y_t \sim q_t(y_t|y,x)} \left[ \frac{1}{t} \sum_{i=1}^{L} \mathbf{1}[y_t^i = \mathbf{M}] \log p_{\theta}(y^i|y_t, x) \right] \leq \log \pi_{\theta}(y|x)$$

这一选择的关键洞察是：ELBO作为整体保留了序列生成过程的全局结构信息，而token级分解会破坏这种结构，引入难以控制的近似误差。当与序列级动作空间结合时，ELBO代理使重要性比率能够自然地反映新旧策略在整个序列上的相对优劣。

### 3. 重要性比率：长度归一化

原始的序列级重要性比率$\rho_{\mathrm{seq}}^{(i)} = \exp(\mathcal{L}_{\theta}(y^{(i)}|x) - \mathcal{L}_{\theta_{\mathrm{old}}}(y^{(i)}|x))$直接对ELBO差取指数，由于ELBO值随序列长度线性增长，该比率容易出现指数爆炸，导致梯度不稳定。

ESPO引入**长度归一化**来稳定训练：

$$\rho_{\mathrm{seq}}^{(i)} = \exp\left(\frac{1}{L}(\mathcal{L}_{\theta}(y^{(i)}|x) - \mathcal{L}_{\theta_{\mathrm{old}}}(y^{(i)}|x))\right)$$

通过除以序列长度$L$，重要性比率被归一化到每个token的平均ELBO差异，有效防止了长序列下的数值溢出。这一归一化是序列级框架得以在大规模训练中稳定运行的关键工程支撑。

### 4. KL散度估计器：k2估计器

KL正则化是防止策略更新偏离参考模型过远的关键约束。ESPO摒弃了传统GRPO中使用的k3估计器（包含指数项），转而采用**k2估计器**：

$$\widehat{\mathbb{K}\mathbb{L}}_{\mathtt{k}2} = \frac{1}{2} \bigl( \mathcal{L}_{\theta}(y^{(i)}|x) - \mathcal{L}_{\mathrm{ref}}(y^{(i)}|x) \bigr)^{2}$$

k2估计器采用MSE形式，不含指数项，其梯度无偏且稳定。图2和图6提供了强有力的消融证据：k1估计器（无有效约束）导致模型崩溃；k3估计器因指数项引入严重不稳定性，回报停滞且梯度出现急剧尖峰；仅k2估计器在整个训练过程中保持稳定的梯度范数，并收敛至最高回报。

值得注意的是，表5的消融实验揭示了一个关键事实：将k2估计器简单替换到token级基线（d1+k2）上，性能与原始基线相当，无法带来实质提升。这证明ESPO的巨大增益**并非来自k2估计器本身，而是来自序列级框架与k2估计器的协同作用**——只有将动作空间提升到序列级，k2的稳定性优势才能充分释放。

### 创新耦合逻辑

上述四个changed slots并非独立改进，而是形成了一条完整的因果链：**序列级动作空间**消除了根本性的结构错配，使RL目标与dLLM生成机制对齐；**序列级ELBO**为这一框架提供了可处理的似然代理；**长度归一化**和**k2估计器**则分别解决了序列级框架引入的数值稳定性和KL约束稳定性问题。这四个组件缺一不可，共同构成了ESPO区别于所有token级基线的方法论壁垒。

## 整体框架

ESPO（ELBO-based Sequence-level Policy Optimization）是一个针对扩散大语言模型（dLLM）设计的序列级强化学习框架。其核心设计理念源于一个根本性观察：扩散模型通过迭代去噪生成整个序列，无法像自回归模型那样提供逐token的条件概率分解。因此，ESPO将**整个序列的生成视为单一原子动作**，从根本上消除了传统token级强化学习方法（如GRPO）与dLLM生成机制之间的结构性错配。

### 框架总览

ESPO的整体pipeline由以下几个关键模块串联而成，形成从采样到策略更新的闭环：

```
输入提示 x
    │
    ▼
┌─────────────────────────────────┐
│  1. 序列采样（旧策略 π_θold）      │
│  - 生成 G 个完整序列 y^(1..G)    │
│  - 计算每个序列的奖励 R(x,y)     │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  2. 组相对优势计算               │
│  Â^(i) = R(x,y^(i)) - mean(R)   │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  3. ELBO代理计算（新旧策略）      │
│  - L_θ(y|x) 与 L_θold(y|x)      │
│  - 使用抗差采样降低方差           │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  4. 长度归一化重要性比率          │
│  ρ_seq = exp((L_θ - L_θold)/L)  │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  5. 序列级GRPO目标 + k2 KL正则   │
│  - 剪切优势 + 重要性比率加权     │
│  - k2估计器约束策略偏离           │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  6. 策略更新（μ次迭代）           │
│  - LoRA微调（r=128, α=64）      │
│  - 更新 π_θ → π_θold            │
└─────────────────────────────────┘
```

### 模块职责与输入输出

**模块1：序列采样。** 给定输入提示 $x$，旧策略 $\pi_{\theta_{\text{old}}}$ 通过迭代去噪生成 $G$ 个完整序列 $\{y^{(1)}, \dots, y^{(G)}\}$。每个序列经过奖励函数 $R(x, y)$ 评估，获得标量奖励值。该模块的输出是序列-奖励对，为后续优势计算提供基础。

**模块2：组相对优势计算。** 在每个采样组内，计算每个序列相对于组均值的优势 $\hat{A}^{(i)} = R(x, y^{(i)}) - \frac{1}{G}\sum_{j=1}^{G} R(x, y^{(j)})$。这种组内归一化消除了奖励尺度的影响，使优化信号仅依赖于序列间的相对排序。

**模块3：ELBO代理计算。** 这是ESPO的核心创新之一。由于dLLM的序列对数似然 $\log \pi_\theta(y|x)$ 不可直接计算，ESPO采用证据下界（ELBO）作为可处理的代理。对于每个序列，分别计算当前策略和旧策略下的ELBO值 $\mathcal{L}_\theta(y|x)$ 与 $\mathcal{L}_{\theta_{\text{old}}}(y|x)$。为降低ELBO差异估计的方差，该模块引入**抗差采样**（共享噪声水平和掩码位置）和**耦合采样**（构建互补掩码，确保每个token均获得学习信号）。

**模块4：长度归一化重要性比率。** 将ELBO差值除以序列长度 $L$ 进行归一化，得到稳定的重要性比率：
$$\rho_{\text{seq}}^{(i)} = \exp\left(\frac{1}{L}\left(\mathcal{L}_\theta(y^{(i)}|x) - \mathcal{L}_{\theta_{\text{old}}}(y^{(i)}|x)\right)\right)$$
未经归一化的原始比率（Eq. 6）在序列较长时会导致指数爆炸，使训练崩溃。长度归一化是保证大规模训练稳定性的关键技术。

**模块5：序列级GRPO目标与k2 KL正则。** 将归一化重要性比率代入GRPO的剪切目标函数，形成序列级策略优化目标。同时，引入k2 KL散度估计器约束当前策略不偏离参考策略过远：
$$\widehat{\mathbb{KL}}_{\text{k2}} = \frac{1}{2}\left(\mathcal{L}_\theta(y^{(i)}|x) - \mathcal{L}_{\text{ref}}(y^{(i)}|x)\right)^2$$
k2估计器采用MSE形式，不含指数项，梯度无偏且稳定。消融实验（Figure 2, Figure 6）表明，k1估计器导致模型崩溃，k3估计器因含指数项而梯度剧烈震荡，唯有k2在整个训练过程中保持稳定的梯度范数。

**模块6：策略更新。** 在每组采样数据上执行 $\mu$ 次策略更新（默认 $\mu=8$），使用LoRA进行参数高效微调。更新后的策略成为下一轮迭代的旧策略，形成闭环。

### 关键设计决策的因果链路

框架设计的因果链路清晰：**动作空间从token级提升到序列级** → 消除了token级分解与dLLM生成机制的根本性不一致 → 需要序列级似然代理 → 引入ELBO作为可处理代理 → ELBO的指数形式导致数值不稳定 → 引入长度归一化重要性比率和k2 KL估计器 → 实现稳定训练。

消融实验（Figure 1）直接验证了这一因果链：在Sudoku任务上，仅序列级+ELBO的组合（蓝色曲线）实现了稳定收敛至高回报，而所有token级变体（包括token级ELBO和平均场近似）均失败。进一步地，Table 5显示将k2估计器简单替换到token级基线（d1+k2）并不能带来实质提升，证明性能增益的核心来源是**序列级框架本身**，而非孤立的稳定性技术。

## 核心模块与公式推导

ESPO 的核心设计围绕一个根本性转变展开：将强化学习的动作空间从 token 级提升到序列级。这一转变解决了扩散大语言模型（dLLM）与现有 RL 方法之间的结构性错配——dLLM 通过迭代去噪生成整个序列，无法像自回归模型那样提供逐 token 的条件概率分解。以下逐一拆解构成 ESPO 的关键模块及其数学基础。

### 扩散模型的证据下界（ELBO）

ESPO 将序列级 ELBO 作为不可处理的对数似然 $\log \pi_{\theta}(y|x)$ 的代理。对于掩码离散扩散模型，其前向过程以概率 $t$ 将 token 替换为掩码 $\mathbf{M}$（Eq. 1）。基于连续掩码比率 $t \sim \mathcal{U}[0,1]$ 的 ELBO 定义为：

$$\mathcal{L}_{\theta}(y|x) \triangleq \mathbb{E}_{t \sim \mathcal{U}[0,1]} \mathbb{E}_{y_t \sim q_t(y_t|y,x)} \left[ \frac{1}{t} \sum_{i=1}^{L} \mathbf{1}[y_t^i = \mathbf{M}] \log p_{\theta}(y^i|y_t, x) \right] \leq \log \pi_{\theta}(y|x)$$

其中 $L$ 为序列长度，$p_{\theta}$ 为模型预测分布。该公式对每个被掩码的 token 计算对数概率并求和，再用 $1/t$ 加权以校正掩码比率。实践中采用低方差变体（Eq. 3），使用离散掩码数 $l \sim \mathcal{U}(\{1,2,\dots,L\})$ 替代连续 $t$，并将权重调整为 $L/l$。

### 序列级策略优化目标

ESPO 将整个序列 $y$ 的生成视为单一原子动作。基于 GRPO 框架，序列级重要性比率直接使用 ELBO 构造：

$$\rho_{\mathrm{seq}}^{(i)} = \exp \bigl( \mathcal{L}_{\theta}(y^{(i)}|x) - \mathcal{L}_{\theta_{\mathrm{old}}}(y^{(i)}|x) \bigr)$$

其中 $\mathcal{L}_{\theta}$ 和 $\mathcal{L}_{\theta_{\mathrm{old}}}$ 分别为当前策略和旧策略下序列 $y^{(i)}$ 的 ELBO。该比率与组相对优势 $\hat{A}^{(i)}$ 结合，经剪切后构成策略优化目标 $\mathcal{I}_{\mathrm{seq}}(\pi_{\theta})$（Eq. 7）。

### 长度归一化的重要性比率

上述原始比率包含指数项，在序列较长时极易引发数值爆炸。ESPO 引入长度归一化以稳定训练：

$$\rho_{\mathrm{seq}}^{(i)} = \exp\left(\frac{1}{L}\bigl(\mathcal{L}_{\theta}(y^{(i)}|x) - \mathcal{L}_{\theta_{\mathrm{old}}}(y^{(i)}|x)\bigr)\right)$$

除以序列长度 $L$ 等价于对每个 token 的 ELBO 贡献取均值，有效抑制了指数增长，使梯度范数在整个训练过程中保持稳定。

### k2 KL 散度估计器

KL 正则化项用于约束策略更新幅度，防止策略偏离参考模型过远。常见的 k3 估计器包含指数项：

$$\widehat{\mathbb{K}\mathbb{L}}_{\mathtt{k}3} = \exp \bigl( \mathcal{L}_{\mathrm{ref}} - \mathcal{L}_{\theta} \bigr) - 1 - \bigl( \mathcal{L}_{\mathrm{ref}} - \mathcal{L}_{\theta} \bigr)$$

当使用 ELBO 近似对数似然时，该指数项重新引入了与原始重要性比率相同的不稳定问题。ESPO 转而采用 k2 估计器——MSE 形式的二次损失：

$$\widehat{\mathbb{K}\mathbb{L}}_{\mathtt{k}2} = \frac{1}{2} \bigl( \mathcal{L}_{\theta}(y^{(i)}|x) - \mathcal{L}_{\mathrm{ref}}(y^{(i)}|x) \bigr)^{2}$$

k2 估计器不含指数项，梯度无偏且稳定。消融实验（Figure 2, Figure 6）表明：k1 估计器因缺乏有效约束导致模型崩溃，k3 估计器出现剧烈的梯度尖峰并停滞在低回报，而 k2 在整个训练中保持稳定的梯度范数并收敛至最高回报。关键的是，仅将 k2 施加于 token 级基线（d1+k2）并不能带来实质提升（Table 5），证明性能增益源于序列级框架本身，而非估计器选择。

### 方差降低技术

ELBO 差异估计的方差直接影响策略梯度质量。ESPO 采用两项互补技术：

- **抗差采样（共享掩码）**：对当前策略和旧策略的 ELBO 估计使用相同的噪声水平和掩码位置，消除因随机掩码不同引入的额外方差。
- **耦合采样**：构建互补掩码对，使每个 token 在两次前向传播中恰好被掩码一次，保证所有 token 均获得学习信号，同时进一步降低估计方差。

结合耦合采样的每样本总 FLOPs 为 $F_{\mathrm{total}} = 2 N D (K + 6 \mu M)$，其中 $N$ 为参数量，$D$ 为序列长度，$K$ 为去噪步数，$\mu$ 为策略更新次数，$M$ 为蒙特卡洛样本数。

### 训练配置

所有实验采用 2 个蒙特卡洛样本和策略更新值 $\mu = 8$，通过 LoRA（$r=128, \alpha=64$）进行参数高效微调。消融实验表明，增加 MC 样本数（$M=1 \to 4$）可提升 Sudoku 上的训练稳定性并加速收敛，但总 FLOPs 增长约 47%；$\mu$ 在 $[8, 12, 24, 48, 72]$ 范围内均能收敛至相似的高回报，方法对该超参数具有鲁棒性。

## 实验与分析

### 核心发现：序列级框架的决定性作用

ESPO在规划任务上取得了压倒性优势。在Countdown任务上，ESPO相较基础LLaDA模型平均提升**62.3个百分点**（18.7%→81.0%）；在Sudoku任务上提升更为显著，达到**70.3个百分点**（15.7%→86.0%）（Table 1）。相比之下，所有token级RL基线（diffu-GRPO、wd1）在这两项任务上的提升微乎其微，甚至出现性能倒退。这一对比揭示了问题的本质：token级分解与dLLM生成机制之间存在根本性错配，而非仅仅是代理精度不足。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_S5YeC9llIL/figures/003_Table_1.jpg]]
*Table 1: Model performance on mathematics and planning benchmarks. For each task, we train a separate model. Countdown results with † for LLaDA, diffu-GRPO, and wd1 are from Zhao et al. (2025); Tang et al. (2025), while other results are reproduced as detailed in Section 5.1. ∆ denotes the improvement of ESPO over LLaDA or Dream model without reinforcement post-training*

消融实验（Table 5）进一步证实了这一判断。将k2 KL估计器简单替换到token级基线（d1+k2）中，Sudoku性能仅与原始d1持平（26.3/23.1/18.8 vs. 26.7/24.1/15.9），远未触及ESPO的水平（92.7/84.7/80.7）。这表明**k2估计器的稳定梯度是必要条件，但序列级动作空间才是性能跃升的充分条件**。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_S5YeC9llIL/figures/025_Table_5.jpg]]
*Table 5: Performance comparison on Sudoku (LLaDA-8B-Instruct). We compare the original d1 (using k3), d1 adapted with the k _ { 2 } estimator, and our ESPO method*

Figure 1的消融实验直观展示了这一因果链：在Sudoku训练中，序列级+ELBO组合（蓝色）是唯一实现稳定收敛至高回报的配置，而token级+ELBO（绿色）经历严重不稳定后崩溃，平均场近似变体（橙色、红色）则完全无法学习。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_S5YeC9llIL/figures/002_Figure_1.jpg]]
*Figure 1: Training performance on the Sudoku task under different action space (Token-level vs. Sequence-level) and likelihood approximations (Mean-field vs. ELBO). Our method (blue) combines a sequence-level action space with an ELBO approximation, yielding the most stable and highest performance. Figure 2: Training performance on the Sudoku task with different KL-divergence estimators. The k _ { 2 } estimator (blue) achieves stable and superior performance. The k _ { 1 } estimator (orange) is highly unstable and collapses, while the k _ { 3 } estimator (green) stagnates*

### 数学与编程任务上的稳健提升

在数学推理任务上，ESPO同样带来一致但相对温和的提升：GSM8K平均准确率从75.9%提升至82.0%（+6.1pp），MATH从37.0%提升至39.5%（+2.5pp）。编程任务上，HumanEval Pass@1从37.8%提升至40.1%（+2.3pp），MBPP从37.8%提升至45.4%（+7.6pp）（Table 2）。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_S5YeC9llIL/figures/004_Table_2.jpg]]
*Table 2: Model performance on coding benchmarks. We train a single model and evaluate it across multiple coding benchmarks (HumanEval and MBPP) at different sequence lengths. ∆ denotes the improvement of ESPO over LLaDA model without reinforcement post-training. ESPO consistently enhances the performance while even achieving competitive results compared with LLaDA-1.5, which was trained on a privately collected dataset at a significantly larger scale*

数学和编程任务上的增益幅度远小于规划任务，这反映了RL微调的一个基本约束：**预训练模型的知识边界构成了性能天花板**。规划任务（Countdown、Sudoku）要求模型在约束空间内进行探索性搜索，预训练阶段未充分暴露此类结构化推理模式，因此RL后训练有巨大的改进空间。而数学和编程能力已在预训练语料中被大量覆盖，RL只能做边际优化。

值得注意的是，ESPO在编程任务上训练单一模型即可在多个benchmark上获得一致提升，而基线wd1在全参数微调下高度敏感，需仔细调整超参数以避免训练崩溃——这从侧面印证了ESPO框架的鲁棒性。

### KL估计器的稳定性机制

Figure 2和Figure 6揭示了不同KL估计器的训练动力学差异。k1估计器（无有效约束）导致模型迅速崩溃；k3估计器（含指数项）产生剧烈的梯度尖峰，回报停滞；唯有k2估计器（MSE形式）在整个训练过程中保持稳定的梯度范数，使策略平滑收敛。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_S5YeC9llIL/figures/017_Figure_6.jpg]]
*Figure 6: Comparison of training dynamics with different KL divergence estimators. The top row illustrates the KL estimates, while the bottom row displays the gradient norms for the k _ { 1 } , k _ { 2 } and k _ { 3 } estimators. The k _ { 1 } estimator (left) lacks effective constraints, leading to model collapse. The k _ { 3 } estimator (right) suffers from severe instability and gradient spikes. In contrast, the k _ { 2 } estimator (middle) demonstrates superior stability and consistent gradient norms throughout training*

k3的不稳定性源于其指数项：当用ELBO近似对数似然时，$ \exp(\mathcal{L}_{\mathrm{ref}} - \mathcal{L}_{\theta}) $ 重新引入了与未归一化重要性比率（Eq. 6）相同的数值爆炸问题。k2通过二次形式 $ \frac{1}{2}(\mathcal{L}_{\theta} - \mathcal{L}_{\mathrm{ref}})^2 $ 绕过了指数操作，同时保持了梯度无偏性——这是ESPO能够在长序列训练中维持稳定的关键设计。

### 超参数鲁棒性与计算成本

ESPO对关键超参数表现出良好的鲁棒性。蒙特卡洛样本数从1增加到4时，Sudoku训练稳定性持续改善且收敛加速，但Countdown上影响较小（Figure 4）——这可能因为Sudoku的奖励信号更稀疏，需要更多样本降低梯度方差。策略更新值μ在[8, 12, 24, 48, 72]范围内均能收敛到相似的高回报，较小μ在Sudoku上初始收敛更快（Figure 5）。

![[assets/figures/papers/paper_list_l49_https_openreview_net_forum_id_S5YeC9llIL/figures/009_Figure_4.jpg]]
*Figure 4: Ablation study on the number of Monte Carlo samples for Countdown and Sudoku. We evaluate training performance with different MC sample counts (1, 2, 4), showing the effect of increased sampling on reward optimization*

计算成本方面，采样阶段占据主导。以编程任务100步训练为例，MC样本数从1增加到4时，wall-clock时间从5.61小时增至9.06小时（+61%），而理论FLOPs从608ND增至896ND（+47%）（Table 3）。总FLOPs公式为 $ F_{\mathrm{total}} = 2ND(K + 6\mu M) $，其中去噪步数K和策略更新次数μ是主要乘数因子。

### 失败模式与边界条件

1. **预训练能力瓶颈**：数学和编程任务上的提升幅度受限于预训练模型原有能力，RL无法注入新知识。
2. **ELBO代理偏差**：ELBO作为序列对数似然的代理与真实值存在偏差，在特定条件下可能误导优化方向。
3. **模型架构限制**：当前验证仅针对掩码离散扩散模型（MDM），连续扩散或流匹配模型的适用性未知。
4. **奖励设计依赖**：规划任务上的显著效果可能依赖于明确的规则奖励信号，向模糊奖励的真实任务推广需进一步验证。
5. **Dream设置下的退化**：在Sudoku的Dream设置（24 token短答案生成）中，diffu-GRPO反而导致性能下降（98.1%→96.0%），ESPO恢复至98.0%但未超越原始模型（Table 4），说明极短序列下序列级框架的优势被压缩。

### 关键图表速查

| 图表 | 核心结论 |
|------|----------|
| Figure 1 | 序列级+ELBO是唯一稳定收敛的配置，token级变体均失败 |
| Figure 2 | k2估计器是实现稳定训练的必要条件，k1崩溃、k3停滞 |
| Table 1 | ESPO在规划任务上提升60-70pp，远超token级基线 |
| Table 5 | 仅替换k2到token级框架无效，序列级动作空间是关键 |
| Figure 6 | k2提供稳定的梯度范数，k3产生剧烈尖峰 |
| Figure 4 | 增加MC样本改善Sudoku稳定性，对Countdown影响较小 |

## 方法谱系与知识库定位

### 核心瓶颈：自回归RL范式与扩散模型的根本性错配

扩散大语言模型（dLLM）通过迭代去噪生成完整序列，其生成过程天然是全局性的，无法像自回归模型那样提供逐token的条件概率分解。然而，主流强化学习方法（如GRPO）的核心机制——重要性比率和策略梯度——恰恰依赖这种token级概率。这一矛盾构成了dLLM强化学习训练的根本性障碍。

现有工作试图通过启发式代理来弥合这一鸿沟，但均存在结构性缺陷：

- **diffu-GRPO (d1)**（Zhao et al., 2025）采用平均场近似，将联合分布粗暴分解为各token边际分布的乘积，完全忽略了token间的条件依赖关系，导致似然估计存在系统性偏差。
- **wd1**（Tang et al., 2025）使用加权似然重标定，本质上仍是对token级ELBO的重新组合，未能跳出token级分解的框架约束。
- 部分方法尝试对ELBO进行token级分解（$\mathcal{L}_{\theta}^{k}(y|x)$），但该分解在数学上并不严格等于条件对数似然，引入了额外的近似误差。

论文通过Sudoku消融实验（图1）给出了决定性证据：**所有token级变体（无论使用平均场近似还是ELBO分解）均无法稳定学习，而序列级+ELBO的组合是唯一收敛到高回报的方案**。这揭示了一个关键洞察：问题不在于寻找更好的token级代理，而在于token级分解本身与dLLM的生成机制根本不相容。

### ESPO的解决方案：序列级视角的三重创新

ESPO（ELBO-based Sequence-level Policy Optimization）的核心策略是将动作空间从token级提升到序列级，使强化学习目标与dLLM的全局生成特性对齐。具体而言，该方法在三个关键维度上实现了突破：

**1. 动作空间重构：序列作为单一原子动作。** ESPO将整个序列生成视为一个不可分割的动作，从而消除了token级分解的必要性。这一设计使得策略优化目标可以直接作用于序列级分布，从根本上避免了启发式近似带来的误差传播。

**2. 似然代理选择：ELBO作为不可处理对数似然的替代。** 由于dLLM的序列对数似然$\log \pi_{\theta}(y|x)$无法直接计算，ESPO采用证据下界（ELBO）作为其可处理的代理。ELBO天然具有序列级形式（式2、式3），无需进行任何token级分解，与序列级动作空间的设计完美契合。消融实验（图1）证实，即使同为序列级动作空间，使用ELBO的性能也远超平均场近似，说明ELBO作为似然代理的精确性至关重要。

**3. 稳定性技术：长度归一化与k2 KL估计器。** 直接将ELBO代入重要性比率会导致指数爆炸问题（式6），因为ELBO随序列长度线性增长。ESPO引入除以序列长度$L$的归一化策略（式8），有效抑制了梯度爆炸/消失。在KL正则化方面，论文系统对比了三种估计器（图2、图6）：k1估计器缺乏有效约束导致模型崩溃；k3估计器因包含指数项而重新引入不稳定性，梯度出现剧烈尖峰；**k2估计器（MSE形式，式10）在整个训练过程中保持稳定的梯度范数，是实现稳定训练的关键**。值得注意的是，仅将k2估计器施加于token级基线（d1+k2）并不能带来实质提升（表5），这进一步证明了序列级框架本身才是性能增益的根本来源。

### 适用边界与已知局限

**任务特性依赖。** ESPO在需要整体一致性的规划任务（Countdown、Sudoku）上表现尤为突出，相较基础模型分别提升62.3和70.3个百分点（表1）。然而，在数学推理（GSM8K +6.1、MATH +2.5）和代码生成（HumanEval +2.3、MBPP +7.6）等任务上，提升幅度相对有限（表1、表2）。这表明ESPO的增益与任务对全局规划的需求程度正相关，对于主要依赖局部模式匹配的任务，序列级优化的边际收益较小。

**预训练能力天花板。** RL微调无法突破预训练模型的知识边界。在数学和编程基准上，ESPO的提升幅度受限于基础模型LLaDA-8B-Instruct的原有能力，这提示在知识密集型任务上可能需要与监督微调（SFT）结合使用。

**计算开销。** 序列级采样和多次ELBO估计带来了额外的计算成本。训练总FLOPs由$F_{\mathrm{total}} = 2 N D (K + 6 \mu M)$给出（式36），其中$N$为参数量，$D$为序列长度，$K$为去噪步数，$\mu$为策略更新次数，$M$为MC样本数。当$M$从1增加到4时，总FLOPs增加约47%，实际训练时间从5.61小时增至9.06小时（表3）。采样阶段占主导地位，尤其在长序列和大去噪步数设置下。

**模型架构限制。** 当前实验仅针对掩码离散扩散模型（MDM）进行，包括LLaDA-8B-Instruct（Nie et al., 2025）和Dream-7B-Instruct（Ye et al., 2025）。该方法在连续扩散模型或基于流匹配的生成模型上的适用性尚未验证。

**ELBO偏差。** ELBO作为对数似然的下界，与真实对数似然之间可能存在系统性偏差。在特定条件下，这种偏差可能影响策略梯度的优化方向，尽管当前实验未观察到由此导致的明显问题。

### 开放问题与未来方向

1. **规模化扩展。** ESPO能否有效扩展到百亿参数以上模型及更长序列（如$L > 2048$）？序列级ELBO的计算开销随序列长度线性增长，可能需要更高效的近似策略。

2. **跨架构泛化。** 该方法的核心思想——序列级动作空间+ELBO代理——是否适用于其他非自回归生成范式（如连续扩散、流匹配、离散扩散的非掩码变体）？这需要验证ELBO在这些架构中是否仍能作为有效的似然代理。

3. **ELBO精确性改进。** 是否存在比标准ELBO更精确的序列似然代理？例如，更紧的变分下界或基于重要性采样的估计器可能进一步缩小偏差，提升优化效率。

4. **与监督信号的融合。** 在知识密集型任务上，如何将ESPO与监督微调有效结合，以突破预训练能力限制？这涉及RL目标与SFT目标之间的平衡策略设计。

5. **样本效率提升。** 当前方法使用2-4个MC样本进行策略评估，能否通过更好的信用分配策略（如对序列中不同位置赋予差异化权重）或更智能的重要性采样方案来进一步提升样本效率？

6. **复杂奖励结构下的鲁棒性。** ESPO在具有多步依赖、稀疏奖励或组合奖励结构的任务上的表现如何？当前实验使用的奖励信号相对简单（Sudoku为完全正确与否的二元奖励），更复杂的奖励设计可能需要配套的信用分配机制。

## 原文 PDF

![[paperPDFs/ICLR_2026/Principled_RL_for_Diffusion_LLMs_Emerges_from_a_Sequence_Level_Perspective.pdf]]
