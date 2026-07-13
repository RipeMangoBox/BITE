---
title: "On the Design of KL-Regularized Policy Gradient Algorithms for LLM Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/On_the_Design_of_KL_Regularized_Policy_Gradient_Algorithms_for_LLM_Reasoning.pdf
project_link: null
code_link: https://github.com/complex-reasoning/RPG
openreview_forum_id: qe060gmfm7
aliases:
- RPGRIRSVRR
- DKRPGALR
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "精确的非策略重要性加权和KL正则化形式的系统性推导。"
primary_logic: "通过统一的Regularized Policy Gradient（RPG）推导，揭示了k3估计器与非归一化KL的等价性，纠正了GRPO在非策略采样下KL项的重要性权重缺失，并设计了RPG-Style Clip裁剪重要性采样机制，从而在保证梯度一致性的同时提升训练的稳定性和可扩展性。"
claims:
- "GRPO中的KL惩罚项在非策略采样下缺少重要性权重，导致梯度不一致。"
- "k3估计器等价于非归一化KL散度（UKL），为统一推导提供基础。"
- "RPG-REINFORCE配合RPG-Style Clip在AIME24/25上比DAPO提升高达6个绝对百分点。"
- "RPG-REINFORCE在8K上下文长度下AIME25达52%准确率，超过官方Qwen3-4B-Instruct。"
---

# On the Design of KL-Regularized Policy Gradient Algorithms for LLM Reasoning

> [!tip] 核心洞察
> 通过统一的Regularized Policy Gradient（RPG）推导，揭示了k3估计器与非归一化KL的等价性，纠正了GRPO在非策略采样下KL项的重要性权重缺失，并设计了RPG-Style Clip裁剪重要性采样机制，从而在保证梯度一致性的同时提升训练的稳定性和可扩展性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 论KL正则化策略梯度算法在大语言模型推理中的设计 |
| 英文题名 | On the Design of KL-Regularized Policy Gradient Algorithms for LLM Reasoning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qe060gmfm7) · [GitHub](https://github.com/complex-reasoning/RPG) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Regularized Policy Gradient (RPG) and its REINFORCE-style variant (RPG-REINFORCE) |
| Dataset | AIME24, AIME25 (mathematical reasoning benchmarks), AIME25 (8K context length), AIME24 (4K context length), AIME25 (4K context length) |

> [!tip] 效果简介
> - AIME24, AIME25 (mathematical reasoning benchmarks) 上，accuracy (absolute improvement) 为 RPG-REINFORCE with RPG-Style Clip，对比 DAPO，变化 +6 percentage points。
> - AIME25 (8K context length) 上，accuracy 为 RPG-REINFORCE with RPG-Style Clip (52%)，对比 Qwen3-4B-Instruct (47%)，变化 +5 percentage points。
> - AIME24 (4K context length) 上，Best score 为 RPG-REINFORCE-URKL (0.4531)，对比 DAPO (0.4479, second best)，变化 +0.0052。

## 概要

当前基于KL正则化的策略梯度方法（如GRPO、DAPO、REINFORCE++）在LLM推理训练中缺乏统一的理论框架：正向/反向KL、归一化/非归一化KL以及估计器选择之间的关系模糊不清，且多数方法在使用非策略采样时忽略正确的重要性加权，导致梯度估计偏差和训练不稳定。

本文提出**Regularized Policy Gradient (RPG)** 统一推导框架，核心贡献包括：

- **揭示k3估计器与非归一化KL散度（UKL）的等价性**，为不同KL形式提供统一的数学基础。
- **纠正GRPO的非策略梯度缺失**：指出GRPO中KL惩罚项在非策略采样下缺少重要性权重 $w(x)=\pi_\theta(x)/\pi_{\text{old}}(x)$，导致目标函数梯度与实际优化方向不一致。
- **设计RPG-Style Clip双裁剪机制**：针对正则化优势项的重要性比率进行非对称裁剪，在保证梯度一致性的同时提升训练稳定性。
- **建立完全可微损失与REINFORCE式损失之间的梯度等价条件**，通过停止梯度算子（SG）实现灵活实现。

实验表明，RPG-REINFORCE配合RPG-Style Clip在数学推理基准上显著优于现有方法：在AIME24/25上比DAPO提升最高**6个绝对百分点**；在8K上下文长度下AIME25准确率达**52%**，超越官方Qwen3-4B-Instruct模型（47%）。框架在Qwen-3-4B和Qwen-2.5-7B-Instruct模型上均表现出稳定的可扩展性。

### 核心瓶颈：KL正则化策略梯度中的梯度不一致与设计碎片化

在大语言模型（LLM）的强化学习微调中，KL正则化策略梯度方法已成为稳定训练、防止策略崩溃的标准范式。然而，当前方法存在一个根本性问题：**正向/反向KL、归一化/非归一化KL以及估计器选择之间缺乏统一的理论理解**。更严重的是，以GRPO（Shao et al., 2024）为代表的非策略采样方法在实践中常常忽略正确的重要性加权，导致梯度估计出现系统性偏差，直接威胁训练的稳定性和收敛性。

具体而言，GRPO在非策略采样下直接使用k3估计器进行KL惩罚，缺少重要性权重$w(x) = \pi_\theta(x) / \pi_{\text{old}}(x)$的修正。如论文Section 2.2所揭示的：“The direct subtraction without this weight means the gradient derived from GRPO's objective does not, in general, correspond to the gradient of the intended off-policy objective”——这种目标与梯度的不一致是当前方法训练不稳定的深层原因。

### 现有方法缺口：从碎片化设计到缺乏统一框架

当前主流的KL正则化策略梯度方法呈现出明显的碎片化特征：

- **GRPO**（Shao et al., 2024）采用分组相对奖励估计优势，配合k3估计器进行KL正则化，但缺少非策略重要性加权，梯度与目标脱节。
- **DAPO** 作为无价值函数基线的方法，结合了更高的clip-higher策略，但同样未解决KL项的重要性权重缺失问题。
- **REINFORCE++**（Hu, 2025）对REINFORCE进行了增强，加入token级KL惩罚（使用k2估计器）和归一化，但其KL正则化形式的选择缺乏系统性论证。

这些方法各自选择了不同的KL方向、归一化方式和估计器，却缺少一个统一的框架来解释这些设计选择之间的内在联系和等价关系。特别是，广泛使用的k3估计器与非归一化KL散度之间的等价性尚未被明确揭示，导致方法设计停留在经验层面。

### 本文动机：建立统一的RPG框架

针对上述瓶颈，本文的核心动机是通过系统性的理论推导，建立一个统一的**Regularized Policy Gradient（RPG）**框架。该框架旨在：

1. **统一KL正则化形式**：将归一化/非归一化KL变体纳入同一推导体系，并证明k3估计器与非归一化KL散度（UKL）的等价性（Remark 3.5），为方法选择提供理论依据。

2. **纠正梯度不一致**：精确推导非策略重要性加权机制，补全GRPO等方法的KL项缺失权重，确保梯度估计与优化目标的一致性。

3. **设计稳定训练机制**：提出RPG-Style Clip双裁剪机制，在保证梯度一致性的前提下控制重要性比率的方差，实现训练稳定性与可扩展性的统一。

通过这一框架，本文不仅解释了现有方法的设计选择，更提供了可操作的损失函数构造方案（完全可微损失与REINFORCE式损失），以及配套的参考策略更新策略和裁剪机制，形成了一套完整的LLM推理能力增强方案。

## 核心方法与创新机理

本文的核心创新在于通过**统一的Regularized Policy Gradient (RPG)推导框架**，系统性地纠正了当前KL正则化策略梯度方法中的若干关键缺陷，并引入了配套的稳定化机制。具体而言，创新体现在以下四个紧密耦合的方面：

### 1. 非策略重要性加权的精确化：纠正GRPO的梯度偏差

GRPO（Shao et al., 2024）在目标函数中直接加入KL惩罚项，但忽略了非策略采样（off-policy sampling）所需的**重要性权重（importance weight）**。这一遗漏导致其替代损失的梯度与实际目标函数的梯度**不一致**（Section 2.2）。RPG框架从统一的KL正则化目标出发，通过严格的梯度推导（Proposition 3.2, 3.6），为所有KL变体（正向/反向、归一化/非归一化）给出了**精确的重要性加权形式**。例如，非归一化正向KL（UFKL）的策略梯度为：

$$\nabla_{\theta} J_{\mathrm{UFKL}}(\theta) = Z_{\mathrm{old}} \mathbb{E}_{x \sim \widetilde{\pi}_{\mathrm{old}}} \left[ \left( w(x) R(x) - \beta (w(x) - 1) \right) \nabla_{\theta} \log \pi_{\theta}(x) \right]$$

其中 $w(x) = \pi_{\theta}(x) / \pi_{\mathrm{old}}(x)$ 是缺失的重要性权重。这一修正保证了梯度估计的无偏性，是后续所有设计的基础。

### 2. KL正则化形式的统一：揭示k3估计器与非归一化KL的等价性

不同方法（GRPO、REINFORCE++等）使用不同的KL方向或估计器，缺乏统一理解。RPG框架的关键洞察是：**广泛使用的k3估计器等价于非归一化KL散度（UKL）**（Remark 3.5）。具体地：

$$\mathbb{E}_{x \sim \pi_{\theta}} \left[ k_3\left( \frac{\pi_{\mathrm{old}}(x)}{\pi_{\theta}(x)} \right) \right] = \mathrm{UKL}(\pi_{\theta} \| \pi_{\mathrm{old}})$$

其中 $k_3(y) := y - 1 - \log y$。这一等价性将看似独立的k3惩罚纳入统一的RPG推导，使得框架同时支持**正向/反向KL**和**归一化/非归一化KL**四种组合，并为每种组合提供了对应的完全可微损失（Table 1）和REINFORCE式损失（Table 2）。

### 3. 损失估计器的梯度等价性：桥接完全可微与REINFORCE式实现

RPG框架严格证明了：在正确的非策略加权下，**带停止梯度（stop-gradient）的REINFORCE式损失与完全可微损失在梯度上等价**（Proposition 4.1）。这意味着实践者可以自由选择实现方式——完全可微损失便于端到端优化，而REINFORCE式损失通过 $\mathrm{SG}(\cdot)$ 算子将优势项与策略参数的梯度解耦，降低了内存和计算开销——而不牺牲梯度一致性。这一设计选择（Figure 1中的design choice i）为不同工程约束下的部署提供了灵活性。

### 4. RPG-Style Clip：面向正则化优势的双裁剪机制

PPO的对称裁剪 $[1-\varepsilon, 1+\varepsilon]$ 不适用于包含KL惩罚项的**正则化优势（regularized advantage）**，因为KL项会改变优势的符号和幅度分布。RPG-Style Clip（Algorithm 1）引入**双裁剪机制**：

$$\mathcal{L}^{\mathrm{RPG-Clip}}(x,\theta) = \begin{cases} \max\big(-w(x)\widehat{A}(x;\theta), -\mathrm{clip}(w(x), 1-\epsilon_1, 1+\epsilon_2)\widehat{A}(x;\theta)\big), & \widehat{A}(x;\theta) \ge 0 \\ \min\big(\max(\ldots), -c\widehat{A}(x;\theta)\big), & \widehat{A}(x;\theta) < 0 \end{cases}$$

其核心特征为：
- **非对称裁剪区间** $[1-\varepsilon_1, 1+\varepsilon_2]$：允许对正负优势方向采用不同的裁剪力度（实验中UFKL使用 $(0.2, 0.28)$，而GRPO使用 $(0.1, 0.1)$）。
- **负优势下界** $c$：防止当 $\widehat{A} < 0$ 时损失函数过度惩罚高概率样本，维持探索能力。

这一机制直接作用于重要性权重 $w(x)$，在控制方差的同时引入可控的偏差-方差权衡，是RPG-REINFORCE在AIME24/25上相较DAPO提升高达**6个绝对百分点**的关键使能技术。

### 创新间的因果链

上述四个创新并非孤立存在。精确的重要性加权（创新1）是统一推导的前提；k3-UKL等价性（创新2）将GRPO的实践经验纳入理论框架；梯度等价性（创新3）保证了不同实现路径的正确性；而RPG-Style Clip（创新4）则是在前三个创新构建的正确梯度骨架上的**稳定化增强**。四者共同构成了从理论推导到工程实践的完整创新链条。


### 核心引擎与迭代闭环

本文提出的迭代式正则化策略梯度（RPG）框架围绕一个中心化的 **RPG Core Engine** 构建，该引擎在每个迭代步 $t$ 接收三类输入：当前策略 $\pi_\theta^{(t)}$、参考策略 $\pi_{\text{old}}^{(t)}$ 以及奖励信号 $R(x)$。引擎内部执行四个有序步骤（Figure 1）：

1. **构建KL正则化目标**：将期望奖励与KL散度惩罚项组合为统一目标 $J(\theta^{(t)}) = \mathbb{E}[R] - \beta \cdot \text{Divergence}$。
2. **推导非策略梯度**：基于广义策略梯度定理（Proposition 2.1），对目标求导得到精确的非策略梯度表达式，其中重要性权重 $w(x) = \pi_\theta(x) / \pi_{\text{old}}(x)$ 是保证梯度一致性的关键。
3. **构造替代损失函数**：将梯度表达式封装为可优化的损失函数 $\mathcal{L}(\theta^{(t)})$。
4. **优化策略参数**：通过梯度下降更新策略，输出 $\pi_\theta^{(t+1)}$。

框架以迭代闭环运行：更新后的策略 $\pi_\theta^{(t+1)}$ 进入下一轮迭代，参考策略 $\pi_{\text{old}}^{(t+1)}$ 也随之更新（周期性同步或当token级KL偏移超过阈值时触发），实现持续的推理能力提升。

### 三项设计选择

RPG Core Engine 的具体行为由三个正交的设计选择配置（Figure 1）：

- **设计选择 (i)：损失估计器类型**——完全可微损失（Fully Differentiable）或带停止梯度的REINFORCE式损失。两者在特定条件下梯度等价（Proposition 4.1），但实现复杂度与训练动态有所不同。
- **设计选择 (ii)：KL形式**——归一化KL或非归一化KL（如UKL/$k_3$估计器）。本文证明了广泛使用的 $k_3$ 估计器与非归一化KL散度等价（Remark 3.5），为统一推导提供了理论基础。
- **设计选择 (iii)：KL方向**——正向KL $\text{KL}(\pi_{\text{old}} \| \pi_\theta)$ 或反向KL $\text{KL}(\pi_\theta \| \pi_{\text{old}})$，分别对应零强迫和模式搜索行为。

### 关键模块与数据流

| 模块 | 功能 | 关键输出 |
|------|------|---------|
| **KL Form Selector** | 选择归一化/非归一化KL形式 | 目标函数 $J(\theta)$ 的具体表达式 |
| **KL Direction Selector** | 选择正向/反向KL | 正则化项的符号与梯度结构 |
| **Loss Estimator Selector** | 选择完全可微或REINFORCE式损失 | 替代损失 $\mathcal{L}(\theta)$ |
| **RPG-Style Clip (Dual-Clip)** | 裁剪重要性权重以稳定训练 | 截断后的损失项，控制方差 |
| **Reference Policy Updater** | 周期性更新参考策略 | 更新后的 $\pi_{\text{old}}$ |

**RPG-Style Clip** 是框架中关键的稳定化模块。它将重要性权重 $w(x)$ 裁剪到 $[1-\epsilon_1, 1+\epsilon_2]$ 区间，并对负优势情况施加额外下界 $-c \cdot \widehat{A}(x;\theta)$，形成双裁剪机制（Algorithm 1）。该模块引入可控的偏差-方差权衡，但裁剪参数 $(\epsilon_1, \epsilon_2)$ 目前依赖经验选择。

**Reference Policy Updater** 通过迭代式参考更新方案控制KL偏移：每 $K$ 步优化器更新后将当前策略设为 $\pi_{\text{old}}$，或在token级KL移动平均超过阈值 $\kappa$ 时触发更新。该机制使训练过程中仅需在GPU内存中保留一个模型（上一迭代的概率可预计算并存储）。

### 输入输出流总结

```
输入：当前策略 π_θ^(t)、参考策略 π_old^(t)、奖励 R(x)
  ↓
[KL Form Selector] → 确定目标函数形式（UFKL/URKL/NKL等）
  ↓
[KL Direction Selector] → 确定KL方向（正向/反向）
  ↓
[Loss Estimator Selector] → 构造替代损失（完全可微或REINFORCE式）
  ↓
[RPG-Style Clip] → 裁剪重要性权重，稳定梯度
  ↓
[优化器更新] → π_θ^(t+1)
  ↓
[Reference Policy Updater] → 条件性更新 π_old^(t+1)
  ↓
输出：更新后的策略 π_θ^(t+1)、更新后的参考策略 π_old^(t+1)
```

归一化KL形式的完全可微替代损失总结于 **Table 4**，其非归一化对应版本见 **Table 1**（完全可微）和 **Table 2**（REINFORCE式）。两类损失在梯度等价性上的理论保证由 Proposition 4.1 提供。

### 3.1 迭代RPG框架总览

RPG框架的核心是一个迭代式的KL正则化策略梯度引擎，其结构如Figure 1所示。每次迭代包含四个步骤：

1. **构建KL正则化目标**：将期望奖励与KL散度惩罚项组合成目标函数 $J(\theta) = \mathbb{E}[R] - \beta \cdot \text{KL}$。
2. **推导非策略梯度**：基于广义策略梯度定理（Proposition 2.1），在非策略采样下精确推导 $\nabla_\theta J(\theta)$。
3. **构造替代损失函数**：设计一个替代损失 $\mathcal{L}(\theta)$，使其梯度等价于 $-\nabla_\theta J(\theta)$。
4. **优化策略参数**：通过梯度下降更新策略参数。

引擎的行为由三个关键设计选择决定：
- **损失估计器类型**（设计选择i）：完全可微损失 vs. 带停止梯度的REINFORCE式损失。
- **KL形式**（设计选择ii）：归一化KL vs. 非归一化KL（如UKL/k₃估计器）。
- **KL方向**（设计选择iii）：正向KL $(\pi_{\text{old}} \| \pi_\theta)$ vs. 反向KL $(\pi_\theta \| \pi_{\text{old}})$。

### 3.2 广义策略梯度定理

RPG框架的推导基础是Proposition 2.1给出的广义策略梯度定理（Generalized Policy Gradient Theorem）：

$$\nabla_{\theta} \mathbb{E}_{x \sim \pi_{\theta}} [f(x, \theta)] = \mathbb{E}_{x \sim \pi_{\theta}} \left[ f(x, \theta) \nabla_{\theta} \log \pi_{\theta}(x) + \nabla_{\theta} f(x, \theta) \right]$$

其中 $f(x, \theta)$ 是同时依赖采样变量 $x$ 和参数 $\theta$ 的任意函数。该定理为后续推导非归一化KL正则化目标的策略梯度提供了统一工具。

### 3.3 非归一化KL散度与k₃估计器的等价性

RPG框架的关键洞察在于揭示了非归一化KL散度（UKL）与广泛使用的k₃估计器之间的等价关系。

**定义3.1**（非归一化正向KL）：
$$\mathrm{UKL}(\pi_{\mathrm{old}} \| \pi_{\theta}) = \int_x \pi_{\mathrm{old}}(x) \log \frac{\pi_{\mathrm{old}}(x)}{\pi_{\theta}(x)} dx + \int_x (\pi_{\theta}(x) - \pi_{\mathrm{old}}(x)) dx$$

该散度由两部分组成：广义KL散度（第一项）和质量修正项（第二项），后者保证了当 $\pi_\theta$ 未归一化时散度仍具有良好的数学性质。

**Remark 3.5**（k₃估计器的等价性）：
$$k_3(y) := y - 1 - \log y$$

k₃估计器与非归一化KL散度之间存在精确等价关系：
$$\mathbb{E}_{x \sim \pi_{\theta}} \left[ k_3\left( \frac{\pi_{\mathrm{old}}(x)}{\pi_{\theta}(x)} \right) \right] = \mathrm{UKL}(\pi_{\theta} \| \pi_{\mathrm{old}})$$

这一等价性揭示了GRPO中使用的k₃惩罚项本质上就是非归一化反向KL散度，为统一理解各类KL正则化方法提供了理论基础。

### 3.4 非归一化KL正则化目标的策略梯度

基于广义策略梯度定理，可以推导出非归一化正向KL（UFKL）和反向KL（URKL）正则化目标的精确非策略梯度。

**UFKL目标**：
$$J_{\mathrm{UFKL}}(\theta) = \mathbb{E}_{x \sim \pi_{\theta}} [R(x)] - \beta \, \mathrm{UKL}(\pi_{\mathrm{old}} \| \pi_{\theta})$$

**Proposition 3.2**（UFKL策略梯度）：
$$\nabla_{\theta} J_{\mathrm{UFKL}}(\theta) = Z_{\mathrm{old}} \mathbb{E}_{x \sim \widetilde{\pi}_{\mathrm{old}}} \left[ \left( w(x) R(x) - \beta (w(x) - 1) \right) \nabla_{\theta} \log \pi_{\theta}(x) \right]$$

其中：
- $w(x) = \pi_\theta(x) / \pi_{\mathrm{old}}(x)$ 为重要性权重
- $Z_{\mathrm{old}} = \int \pi_{\mathrm{old}}(x) dx$ 为参考策略的归一化常数
- $\widetilde{\pi}_{\mathrm{old}} = \pi_{\mathrm{old}} / Z_{\mathrm{old}}$ 为归一化后的采样分布

**URKL目标**：
$$J_{\mathrm{URKL}}(\theta) = \mathbb{E}_{x \sim \pi_{\theta}}[R(x)] - \beta \, \mathrm{UKL}(\pi_{\theta} \| \pi_{\mathrm{old}})$$

**Proposition 3.6**（URKL策略梯度）：
$$\nabla_{\theta} J_{\mathrm{URKL}}(\theta) = Z_{\mathrm{old}} \mathbb{E}_{x \sim \widetilde{\pi}_{\mathrm{old}}} \left[ w(x) \Big( R(x) - \beta \log w(x) \Big) \nabla_{\theta} \log \pi_{\theta}(x) \right]$$

两个梯度公式均显式包含重要性权重 $w(x)$，这是RPG框架区别于GRPO的核心：GRPO在非策略采样下直接使用k₃估计器而未加重要性权重，导致梯度估计与真实目标梯度不一致（Section 2.2）。

### 3.5 替代损失函数

RPG框架提供两类替代损失函数，其梯度等价于负的策略梯度。

**完全可微损失**（Table 1）：直接对目标函数求导得到。以UFKL为例：
$$\mathcal{L}_{\mathrm{UFKL}}(\theta) = -Z_{\mathrm{old}} \mathbb{E}_{x \sim \widetilde{\pi}_{\mathrm{old}}} \left[ w(x) R(x) - \beta (w(x) - 1) \right]$$

**REINFORCE式损失**（Table 2）：使用停止梯度算子 $\mathrm{SG}(\cdot)$，损失系数在自动微分时不产生额外梯度。以UFKL为例：
$$\mathcal{L}^{\mathrm{REINFORCE\text{-}style}}_{\mathrm{UFKL}}(\theta) = -\mathbb{E}_{x \sim \widetilde{\pi}_{\mathrm{old}}} \left[ \mathrm{SG}\left( Z_{\mathrm{old}} (w(x)R(x) - \beta (w(x)-1)) \right) \log \pi_{\theta}(x) \right]$$

**Proposition 4.1**（梯度等价性）：在标准正则条件下，两类损失满足 $\nabla_\theta \mathcal{L}(\theta) = -\nabla_\theta J(\theta)$，保证优化方向一致。

### 3.6 RPG-Style Clip（双裁剪机制）

为解决非策略训练中重要性权重 $w(x)$ 过大导致的高方差问题，RPG引入双裁剪机制（Algorithm 1）：

$$\mathcal{L}^{\mathrm{RPG\text{-}Clip}}(x,\theta) = \begin{cases} \max\big(-w(x)\widehat{A}(x;\theta), -\mathrm{clip}(w(x), 1-\epsilon_1, 1+\epsilon_2)\widehat{A}(x;\theta)\big), & \widehat{A}(x;\theta) \ge 0 \\ \min\big(\max(\ldots), -c\widehat{A}(x;\theta)\big), & \widehat{A}(x;\theta) < 0 \end{cases}$$

其中 $\widehat{A}(x;\theta)$ 为KL正则化后的优势项。该机制的核心设计：
- **正向优势时**：裁剪 $w(x)$ 至 $[1-\epsilon_1, 1+\epsilon_2]$，防止过大权重导致更新不稳定。
- **负向优势时**：额外引入下界 $-c\widehat{A}$，避免过度惩罚已被压制的采样路径。

与PPO的对称裁剪 $[1-\epsilon, 1+\epsilon]$ 不同，RPG-Style Clip支持非对称裁剪区间，且裁剪对象是重要性权重而非概率比率，更适配KL正则化场景。Figure 2展示了该损失函数在正/负优势下随 $w(x)$ 变化的梯度流动特性。

## 实验与关键发现

### 主要结果

RPG框架在数学推理基准上展现出显著且一致的性能优势，尤其在结合RPG-Style Clip后，RPG-REINFORCE变体成为最强的配置。

在8K上下文长度设定下，**RPG-REINFORCE** 配合RPG-Style Clip在AIME25上达到**52%的准确率**，超越了官方Qwen3-4B-Instruct模型的47%（见Table 3）。与强基线DAPO相比，RPG-REINFORCE在数学推理基准上的绝对准确率提升高达**+6个百分点**。具体到各基准的最后一步（Last）得分：RPG-REINFORCE-UFKL在AIME24上取得0.5906，RPG-REINFORCE-URKL在AIME25上取得0.5073，RPG-URKL在AMC23上取得0.9492——均为各自基准上的最优Last分数。

在4K上下文长度下（Table 5），RPG-REINFORCE-URKL在AIME24上取得最佳分数0.4531，以微弱优势超越DAPO的0.4479；在AIME25上同样以正边际领先。2K上下文长度下（Table 6），RPG-REINFORCE-UFKL在AIME24上取得最佳整体分数0.3625，RPG-UFKL在AIME25上取得最佳Last分数0.2563。在Minerva-Math和Olympiad-Bench上（Table 7），RPG-REINFORCE变体同样展现出领先优势。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_qe060gmfm7/figures/022_Table_5.jpg]]
*Table 5: Combined performance metrics with 4k context length on the AIME24, AIME25 and AMC23 mathematical reasoning benchmarks, showing “Last” and “Best” scores. The “Last” score is from the 400th training step, assuming the training process remained stable to that point. The highest score in each column is bolded, and the second highest is underlined. RPG and RPG-REINFORCE methods are highlighted with light cyan and light green backgrounds, respectively*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_qe060gmfm7/figures/029_Table_6.jpg]]
*Table 6: Combined performance metrics with 2K context length on the AIME24, and AIME25 mathematical reasoning benchmarks, showing “Last” and “Best” scores. The “Last” score is from the 400th training step, assuming the training process remained stable to that point. The highest score in each column is bolded, and the second highest is underlined. RPG and RPG-REINFORCE methods are highlighted with light cyan and light green backgrounds, respectively*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_qe060gmfm7/figures/030_Table_7.jpg]]
*Table 7: Combined performance metrics with 4k context length on the Minerva-Math and Olympiad-Bench mathematical reasoning benchmarks, showing “Last” and “Best” scores. The “Last” score is from the 400th training step, assuming the training process remained stable to that point. The highest score in each column is bolded, and the second highest is underlined. RPG and RPG-REINFORCE methods are highlighted with light cyan and light green backgrounds, respectively*

在更大规模的Qwen-2.5-7B-Instruct模型上（Table 8），RPG-FKL在AMC23上取得最佳分数0.8836，RPG-REINFORCE-FKL在AIME24上取得最佳分数0.2906，进一步验证了框架的可扩展性。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_qe060gmfm7/figures/046_Table_8.jpg]]
*Table 8: Combined performance metrics on the AMC23, AIME24, and AIME25 mathematical reasoning benchmarks with Qwen-2.5-7B-Instruct model, showing “Last” and “Best” scores. The “Last” score is from the 400th training step, assuming the training process remained stable to that point. The highest score in each column is bolded, and the second highest is underlined. RPG and RPG-REINFORCE methods are highlighted with light cyan and light green backgrounds, respectively*

训练动态方面（Figure 4、Figure 5、Figure 6），RPG和RPG-REINFORCE方法在奖励（critic score）和策略熵上展现出比GRPO和DAPO更稳定的训练进程。RPG-REINFORCE变体通常产生更长的响应长度，且策略熵维持在较高水平，表明模型保持了更好的探索能力。

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_qe060gmfm7/figures/013_Figure_4.jpg]]
*Figure 4: Training dynamics and benchmark performance for fully differentiable Regularized Policy Gradient (RPG) and REINFORCE-Style RPG (RPG-REINFORCE) compared to baselines (GRPO and DAPO) with 8k context length*

![[assets/figures/papers/paper_list_l20_https_openreview_net_forum_id_qe060gmfm7/figures/028_Figure_6.jpg]]
*Figure 6: Training dynamics and benchmark performance for fully differentiable Regularized Policy Gradient (RPG) and REINFORCE-Style RPG (RPG-REINFORCE) compared to baselines (GRPO and DAPO) with 2k context length*

### 消融实验

**KL系数的影响**（Figure 9）：在4K上下文长度下，KL系数β=1e-4时模型性能优于β=1e-3。较小的KL惩罚强度允许策略在优化奖励时有更大的灵活性，同时仍能防止过度偏离参考策略。

**裁剪比率的影响**（Figure 8）：不同的clip比率设置在REINFORCE-style RPG中对critic score和响应长度的影响相似，但特定配置下性能更优。采用更高且clip-higher的DAPO-like策略（如(0.2, 0.28)）可以增加actor熵并提升整体性能，这表明适当的裁剪松弛度有助于维持策略多样性。

**迭代参考更新的影响**（Figure 9）：移除迭代参考模型更新机制会导致响应长度持续增长和actor熵下降，但模型性能在后期有所恢复。这表明迭代参考更新主要起到稳定训练、控制KL漂移的作用，而非直接决定最终性能的上限。

### 关键图表结论

- **Figure 4（8K训练动态）**：RPG-REINFORCE变体在响应长度和策略熵上均高于GRPO和DAPO，且训练曲线更平滑，验证了RPG-Style Clip和重要性加权对训练稳定性的贡献。
- **Table 3（8K综合性能）**：RPG-REINFORCE方法在AIME24和AIME25的Last和Best分数上全面领先，证明了REINFORCE式损失与RPG-Style Clip组合的有效性。
- **Figure 5（4K训练动态）**：RPG-REINFORCE变体达到最高的响应长度（约2800），而REINFORCE++及其变体处于中等水平，GRPO和DAPO相对较低，表明RPG框架鼓励更充分的推理链展开。
- **Table 5（4K综合性能）**：RPG-REINFORCE-URKL在AIME24和AIME25上均取得最优Best分数，证实了非归一化反向KL配合REINFORCE式损失的优势。
- **Figure 8（clip比率消融）**：不同clip比率下训练曲线高度重合，说明RPG-REINFORCE对clip参数的选择具有一定鲁棒性，但精细调优仍能带来性能增益。
- **Figure 9（KL系数与参考更新消融）**：β=1e-4显著优于β=1e-3；移除迭代参考更新后熵下降但性能可恢复，提示KL正则化的核心作用在于约束更新幅度而非严格锚定参考分布。

### 失败模式与局限性

RPG-Style Clip虽然有效降低了非策略更新的方差，但其双裁剪参数(ε₁, ε₂)目前依赖经验选择，缺乏原则性的调度策略。论文明确指出"developing principled schedules for clipping would be valuable"，这意味着在不同训练阶段或不同任务上，固定的裁剪区间可能不是最优的。此外，所有实验均在数学推理基准上进行，框架在其他NLP任务（如指令跟随、安全对齐）上的泛化性尚未验证。尽管在4B和7B模型上展示了可扩展性，但在更大规模模型（如70B、405B）上的行为仍待探索。

## 定位与知识库关联

### 方法定位与统一视角

本文提出的 **Regularized Policy Gradient (RPG)** 框架及其 REINFORCE 式变体 **RPG-REINFORCE**，本质上是对现有 KL 正则化策略梯度方法的一次系统性梳理与纠偏。RPG 不引入全新的优化范式，而是通过严格的非策略梯度推导，揭示了几种主流方法之间的隐含联系和关键缺陷。

框架的核心贡献在于统一了以下三个维度的设计选择：
- **KL 形式**：归一化 KL 与非归一化 KL（UKL）；
- **KL 方向**：正向 KL（$\mathrm{KL}(\pi_{\mathrm{old}} \| \pi_{\theta})$，零强迫）与反向 KL（$\mathrm{KL}(\pi_{\theta} \| \pi_{\mathrm{old}})$，模式搜索）；
- **损失估计器**：完全可微损失与带停止梯度的 REINFORCE 式损失（两者在梯度上等价，见 Proposition 4.1）。

这一统一视角的关键洞察是 **Remark 3.5**：广泛使用的 $k_3$ 估计器 $k_3(y) := y - 1 - \log y$ 与非归一化 KL 散度等价。具体而言，$\mathbb{E}_{x \sim \pi_{\theta}}[k_3(\pi_{\mathrm{old}}(x)/\pi_{\theta}(x))] = \mathrm{UKL}(\pi_{\theta} \| \pi_{\mathrm{old}})$，这为理解 GRPO 等方法的 KL 惩罚项提供了理论基础。

### 与基线方法的关系

#### GRPO（Shao et al., 2024）
GRPO 使用分组相对奖励估计优势，并采用 $k_3$ 估计器进行 KL 正则化。RPG 框架指出 GRPO 的一个**关键缺陷**：在非策略采样下，GRPO 的 KL 惩罚项缺少重要性权重 $w(x) = \pi_{\theta}(x)/\pi_{\mathrm{old}}(x)$，导致其目标函数的梯度与真实非策略目标的梯度不一致（Section 2.2）。RPG 通过精确的重要性加权修正了这一问题，使得 $k_3$ 估计器在非策略设定下能够正确对应 UKL 的梯度。

#### DAPO
DAPO 是一种无价值函数基线的方法，结合了更高的 clip-higher 策略。在 RPG 的实验中，DAPO 是表现最强的基线之一——在 AIME24（4K 上下文）上以 0.4479 的最佳分数位列第二，仅次于 RPG-REINFORCE-URKL 的 0.4531（Table 5）。RPG-REINFORCE 配合 RPG-Style Clip 在 AIME24/25 上相比 DAPO 提升高达 6 个绝对百分点（Abstract），表明精确的 KL 正则化推导和双裁剪机制能够带来实质性的性能增益。

#### REINFORCE++（Hu, 2025）
REINFORCE++ 对 REINFORCE 进行了增强，加入了 token 级 KL 惩罚（使用 $k_2$ 估计器）和归一化处理。RPG 框架在理论上覆盖了这类方法的设计空间：REINFORCE++ 的 KL 惩罚可视为 RPG 框架中特定 KL 形式和方向的一个实例，但 RPG 提供了更系统的推导和更灵活的选择（如 UKL 形式与 $k_3$ 的等价性），并在非策略设定下保证了梯度一致性。

### 适用边界与局限

1. **任务泛化性未验证**：所有实验均在数学推理基准（AIME24、AIME25、AMC23、Minerva-Math、Olympiad-Bench）上进行。RPG 框架在指令跟随、安全对齐、代码生成等其他 NLP 任务上的有效性尚未得到实证支持。

2. **模型规模限制**：实验基于 Qwen-3-4B 和 Qwen-2.5-7B-Instruct 等较小规模模型。尽管 RPG 在设计上强调可扩展性（如通过预计算参考策略概率使训练只需单模型驻留 GPU），但在数十亿参数级别（如 70B、405B）模型上的行为仍有待探索。

3. **裁剪参数依赖经验选择**：RPG-Style Clip 的双裁剪机制引入了可控的偏差-方差权衡，但裁剪参数 $(\varepsilon_1, \varepsilon_2)$ 目前依赖经验设定（如 RPG 和 DAPO 使用 $(0.2, 0.28)$，而 GRPO 使用 $(0.1, 0.1)$）。消融实验（Figure 8）表明不同裁剪比率对性能有显著影响，但缺乏原则性的动态调度策略——论文自身也承认 "developing principled schedules for clipping would be valuable"。

4. **KL 系数敏感性**：消融实验（Figure 9）显示 KL 系数 $\beta = 10^{-4}$ 时性能优于 $\beta = 10^{-3}$，表明正则化强度需要仔细调节，且最优值可能与任务和模型规模相关。

### 开放问题

1. **裁剪参数的理论调度**：如何为 RPG-Style Clip 的 $(\varepsilon_1, \varepsilon_2)$ 设计一个理论驱动的动态调度方案，使其能根据训练过程中的 KL 偏移量或重要性权重的分布自动调整？

2. **大规模模型的稳定性**：RPG 框架在更大规模模型（如 70B、405B）上是否仍然保持训练稳定性和相对于 DAPO/GRPO 的性能优势？迭代参考更新机制在大模型下的计算开销是否可接受？

3. **KL 方向的任务依赖性**：不同 KL 方向（正向/反向）与非归一化形式在非推理任务（如指令跟随、安全对齐）中的权衡如何？正向 KL 的零强迫特性是否在某些任务中更有利于保持输出多样性？

4. **在线/离线混合训练**：RPG 框架目前假设固定的非策略采样（从 $\pi_{\mathrm{old}}$ 采样）。结合在线策略采样时，如何进一步降低梯度估计的方差并提高样本效率？

5. **替代性的重要性权重修正策略**：RPG-Style Clip 的双裁剪机制是一种经验性的方差缩减手段。是否存在更优的非策略重要性权重修正策略（如基于信任域的自适应截断），能够在理论上提供更紧的偏差-方差下界？

## 原文 PDF

![[paperPDFs/ICLR_2026/On_the_Design_of_KL_Regularized_Policy_Gradient_Algorithms_for_LLM_Reasoning.pdf]]
