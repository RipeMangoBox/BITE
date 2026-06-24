---
title: "Curriculum Group Policy Optimization: Adaptive Sampling for Unleashing the Potential of Text-to-Image Generation"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Curriculum_Group_Policy_Optimization_Adaptive_Sampling_for_Unleashing_the_Potential_of_Text_to_Image_Generation.pdf
project_link: null
code_link: "https://github.com/PRIS-CV/CGPO"
aliases:
- CGPOC
- CGPOASUPTIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用组奖励方差作为在线提示不一致性代理，动态识别处于模型“最近发展区”的高学习信号提示，并通过自适应概率采样优先选择这些提示。
primary_logic: 最具信息量的训练提示位于模型表现不一致（高奖励方差）的区域；通过持续优先采样这些提示，训练课程随模型能力同步演变，显著提升训练效率和最终性能。
claims:
- CGPO使用组奖励方差作为在线代理，识别模型部分掌握但尚未稳定掌握的提示。
- 消融实验证明，基于方差的概率采样组件贡献了最大的性能增益。
- GenEval 上 Overall = 0.96
- GenEval 上 Attribute Binding = 0.89
---

# Curriculum Group Policy Optimization: Adaptive Sampling for Unleashing the Potential of Text-to-Image Generation

> [!tip] 核心洞察
> 最具信息量的训练提示位于模型表现不一致（高奖励方差）的区域；通过持续优先采样这些提示，训练课程随模型能力同步演变，显著提升训练效率和最终性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | 课程群策略优化：自适应采样释放文本到图像生成潜能 |
| 英文题名 | Curriculum Group Policy Optimization: Adaptive Sampling for Unleashing the Potential of Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2605.17807) · [Code](https://github.com/PRIS-CV/CGPO) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Curriculum Group Policy Optimization (CGPO) |
| Dataset | GenEval, T2I-CompBench++, DPG Bench, Multi-Reward |

> [!tip] 效果简介
> - GenEval 上，Overall 0.96 vs 0.94 (Flow-GRPO 8 GPU) (+0.02)；Attribute Binding 0.89 vs 0.82 (Flow-GRPO) (+0.07)。
> - T2I-CompBench++ 上，Texture 0.7521 vs 0.7298 (Flow-GRPO) (+0.0223)。
> - DPG Bench 上，Overall 85.5 vs 85.4 (Flow-GRPO) (+0.1)。

## 概述

文本到图像（T2I）生成模型在强化学习微调中普遍采用均匀采样策略，忽略了不同提示对模型当前学习能力的匹配程度。大量训练批次中的提示处于模型已完全掌握或尚无法学习的区域，边际学习效用低下，导致样本效率差。**Curriculum Group Policy Optimization（CGPO）** 针对这一瓶颈，提出以**组奖励方差**作为在线代理信号，动态识别模型“部分掌握但尚未稳定”的提示——这些提示位于模型能力的最近发展区，能提供最高的学习信号。

CGPO 的核心机制是：为每个提示生成一组图像，计算组内奖励的方差；高方差表明模型对该提示的表现不一致，意味着该提示仍具有可挖掘的学习空间。基于此，CGPO 通过自适应概率采样优先选择高方差提示，并辅以探索平衡与历史平滑机制防止提示被永久忽略。同时，引入基于比例公平优化的类别校准方法，动态平衡不同类别间的采样权重，强化弱势类别。整个训练过程构成一个随模型能力同步演变的课程，训练难度逐步推进。

在 GenEval 基准上，CGPO 以 SD3.5-Medium 为基座模型、Flow-GRPO 为主要基线，取得了 **Overall 0.96** 的成绩，较 Flow-GRPO（8 GPU 复现）提升 +0.02，其中属性绑定（Attribute Binding）子指标从 0.82 提升至 0.89（+0.07）。在 T2I-CompBench++ 和 DPG Bench 上也观察到一致的增益。消融实验证实，基于方差的概率采样组件贡献了最大的性能增益（Overall 从 94.42 提升至 95.15，+0.73），验证了自适应采样策略的有效性。

**方法定位**：CGPO 属于强化学习微调框架内的**数据采样优化方法**，不改动奖励模型或策略优化算法本身，而是通过改变“训练什么”来提升“学到什么”。其核心贡献在于将课程学习的思想与在线不确定性估计相结合，为 T2I 强化学习训练提供了一种轻量、即插即用的效率提升方案。

## 背景与动机

### 文本到图像生成的强化学习瓶颈

近年来，强化学习（RL）已成为提升文本到图像（T2I）生成模型指令遵循能力的核心范式。以 **Flow-GRPO** 为代表的方法将T2I微调建模为策略优化问题：模型作为策略，根据文本提示生成图像，再由视觉-语言奖励模型对生成结果进行评分，通过组相对优势（group relative advantage）更新策略参数。这一框架在组合生成、属性绑定等任务上取得了显著进展。

然而，现有RL训练流程中存在一个被忽视的关键瓶颈：**提示采样策略的均匀性假设**。在标准训练中，每个训练步从提示池中均匀随机采样一个批次。这一设计隐含假设所有提示对模型学习的边际效用相同——但这一假设在实际情况中并不成立。

### 均匀采样的边际效用困境

训练过程中，提示对模型的学习价值呈现显著分化。对于模型已经稳定掌握的简单提示，生成图像的奖励值持续较高且波动很小，此时继续训练这些提示带来的梯度信号微弱，边际学习效用趋近于零。对于远超模型当前能力的困难提示，模型几乎无法生成符合要求的图像，奖励值持续低迷且同样缺乏变化，梯度信号同样贫瘠。

真正富含学习信号的提示处于二者之间的“中间地带”：模型对这些提示的掌握**不一致**——有时能生成符合要求的图像，有时则失败。这种不一致性表现为同一提示下生成的多张图像（图像组）之间的奖励值波动较大。高方差区域恰好对应模型能力的“最近发展区”，训练这些提示能够提供最有效的梯度更新。

### 现有方法的缺口

当前T2I强化学习方法普遍缺乏对上述学习信号差异的建模。Flow-GRPO等框架虽然在策略优化层面引入了多项改进（如组相对优势、多奖励模型集成），但在数据采样层面仍沿用朴素的均匀策略。这导致两个直接后果：

1. **样本效率低下**：大量训练计算被浪费在低边际效用的提示上，模型需要更多训练步数才能达到目标性能。
2. **课程缺失**：训练过程缺乏从易到难的课程演进机制，模型无法在适当阶段集中攻克匹配其当前能力的提示。

### 本文动机与核心思路

针对上述问题，本文提出 **Curriculum Group Policy Optimization（CGPO）**，一个自适应课程采样框架。CGPO的核心洞察是：**组奖励方差可以作为提示不一致性的在线代理**——高方差意味着模型已部分掌握但尚未稳定掌握该提示，正是当前阶段最具训练价值的样本。

基于这一洞察，CGPO构建了一个闭环的自适应采样机制：在每个训练步中，利用图像组的奖励统计动态更新每个提示的采样概率，使高方差提示获得更高的被采样概率。随着模型能力提升，原本高方差的提示逐渐被掌握（方差降低），采样概率自然下降，而更高难度的提示进入高方差区域，采样概率自动上升。这一机制使训练课程随模型能力同步演变，无需人工设计难度先验或分段课程。

此外，CGPO还引入了基于比例公平优化的类别校准方法，在类别间动态平衡采样权重，防止模型在特定类别上过拟合而忽视弱势类别。

## 核心创新

CGPO 的核心创新在于将 T2I 强化学习中的提示采样从**静态均匀策略**转变为**在线自适应课程策略**。传统 RL 微调（如 Flow-GRPO）对所有提示等概率采样，忽略了提示难度与模型当前学习能力的匹配关系，导致大量训练批次中提示的边际学习效用低下。CGPO 通过两个紧密耦合的机制解决了这一问题。

### 1. 方差驱动的自适应采样

CGPO 的核心操作变量是**组奖励方差**（Group Reward Variance）。对于每个提示 $p$，模型生成 $G$ 张图像并获取奖励 $\{R_{x_1}, \dots, R_{x_G}\}$，计算其方差：

$$V_p = \operatorname{Var}(\{R_{x_1}, R_{x_2}, \dots, R_{x_G}\}) = \frac{1}{G} \sum_{i=1}^{G} (R_{x_i} - \mu_x)^2$$

高方差意味着模型对该提示的掌握处于**“部分掌握但尚未稳定掌握”**的状态——这正是 Vygotsky 最近发展区理论在 T2I 训练中的体现。这类提示提供了最大的边际学习信号。CGPO 将批次内方差线性映射为提案概率：

$$P^{\mathrm{var}}(p) = \frac{V_p - \min(V)}{\max(V) - \min(V)}$$

随后通过泊松采样范式，以独立伯努利试验的方式决定每个提示是否进入下一训练批次，使高学习信号的提示被优先选取。

### 2. 概率更新与探索平衡

为避免采样陷入局部最优，CGPO 设计了双轨概率更新规则。对于已采样提示，使用最近三次提案概率的移动平均进行平滑，抑制单次噪声波动；对于未采样提示，每轮自动增加 $1/N$ 的概率增量，防止长期未被选中的提示被永久忽略：

$$P^{\mathrm{list'}}(p) = \begin{cases} \frac{1}{3} \sum_{t-2}^{t} P_{(t)}^{\mathrm{var}}(p), & p \in S_b \\ P^{\mathrm{list}}(p) + \frac{1}{N}, & p \notin S_b \end{cases}$$

这一机制使得训练课程能够随模型能力的提升而**自主演变**：随着模型对简单提示的掌握趋于稳定（方差降低），采样概率自然向更难、方差更高的提示转移，形成从易到难的课程推进。

### 3. 基于比例公平的类别校准

在提示采样基础上，CGPO 进一步引入了类别间平衡机制。不同语义类别（如颜色、计数、空间关系）的难度差异显著，均匀处理会导致弱势类别被边缘化。CGPO 通过比例公平优化框架，根据类别内平均奖励动态计算校准权重 $q_i$，其闭式解为：

$$q_i = \frac{1 + \lambda v_i}{c + \lambda}$$

其中 $\lambda$ 控制均衡与重点强化之间的权衡。采样时，提示的最终概率乘以所属类别的权重，强化弱势类别的采样频率。

### 消融验证

消融实验（Table 4）明确揭示了各组件的因果贡献：在 Flow-GRPO 基线（GenEval Overall 94.42%）上，**概率采样**（Probability Sampling）单独贡献了 +0.73% 的提升，是所有组件中增益最大的，直接验证了方差驱动自适应采样的有效性。加入**探索平衡**后提升至 +1.32%，加入**类别校准**后达到 +1.68% 的最终性能。这一累积增益结构说明，三个组件分别解决了“采样什么”、“如何持续探索”和“类别间如何平衡”三个互补问题。

## 整体框架

CGPO 的核心思想是将 T2I 强化学习中的提示采样从**静态均匀分布**转变为**在线自适应课程**。该方法通过四个顺序阶段构成一个闭环，使采样概率随模型能力的提升而动态演进，始终聚焦于处于“最近发展区”的高学习信号提示。

### 四阶段闭环结构

CGPO 的每次训练迭代按以下顺序执行（Figure 2）：

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/002_Figure_2.jpg]]
*Figure 2: Flowchart of Our CGPO Method. Our CGPO method operates through four sequential stages: 1) Probability Sampling: A batch of prompts that match the model’s current capability and remain actively learnable is sampled according to the current sampling probabilities. 2) Reward Calculation: Image groups are generated, and their rewards and advantages are computed for policy training. 3) Probability Computation: Group reward statistics are used to update prompt-level sampling probabilities and category-level calibration weights. 4) Probability Update: After applying exploration balancing and historical smoothing, both the sampling list and the category weight list are updated*

1. **概率采样 (Probability Sampling)**：根据当前维护的概率列表，对每个提示独立进行伯努利试验，生成一个批次。高方差提示被赋予更高的采样概率，而低方差（已稳定掌握或完全未掌握）的提示采样概率较低。
2. **奖励计算 (Reward Calculation)**：为采样到的每个提示生成一组图像（group），计算每张图像的奖励以及**组相对优势**（group relative advantage），用于后续的策略梯度更新。组相对优势定义为：
   $$\hat{A}_i = \frac{R(x_i, p) - \text{mean}(\{R(x_i, p)\}_{i=1}^G)}{\text{std}(\{R(x_i, p)\}_{i=1}^G)}$$
3. **概率计算 (Probability Computation)**：利用组奖励统计量更新两个关键信号——提示级的采样概率提案值 $P^{\text{var}}$ 和类别级的校准权重 $w_i$。
4. **概率更新 (Probability Update)**：对已采样提示采用历史平滑（最近三次提案值的移动平均），对未采样提示施加探索补偿（概率自增 $1/N$），最终更新概率列表和类别权重列表，供下一轮采样使用。

### 核心自适应机制

**提示级：方差驱动的概率采样。** 对于单个提示 $p$，其图像组奖励的方差 $V_p$ 被用作提示不一致性的在线代理：
$$V_p = \text{Var}(\{R_{x_1}, R_{x_2}, \dots, R_{x_G}\}) = \frac{1}{G} \sum_{i=1}^{G} (R_{x_i} - \mu_x)^2$$
高方差意味着模型已部分掌握该提示的要求，但尚未达到稳定掌握——这正是边际学习效用最高的状态。将批次内方差线性映射到 $[0,1]$ 区间得到提案概率：
$$P^{\text{var}}(p) = \frac{V_p - \min(V)}{\max(V) - \min(V)}$$

**类别级：比例公平校准。** 不同语义类别的学习难度差异可能导致弱势类别被系统性忽略。CGPO 通过比例公平优化，根据类别内平均奖励动态调整采样权重，其闭式解为：
$$q_i = \frac{1 + \lambda v_i}{c + \lambda}$$
其中 $\lambda$ 控制均衡与重点强化之间的权衡。采样时，类别校准权重与提示级概率相乘，得到最终采样概率。

**探索与平滑。** 为防止长期未采样提示被永久忽略，CGPO 对未采样提示施加 $1/N$ 的概率增量；同时，已采样提示的概率通过最近三次提案值的平均进行平滑，抑制单次采样的噪声波动：
$$P^{\text{list'}}(p) = \begin{cases} \frac{1}{3} \sum_{t-2}^{t} P_{(t)}^{\text{var}}(p), & p \in S_b \\ P^{\text{list}}(p) + \frac{1}{N}, & p \notin S_b \end{cases}$$

### 输入输出流

- **输入**：完整的提示集 $\{p_1, p_2, \dots, p_N\}$，初始化为均匀概率列表。
- **每轮迭代**：概率列表 → 泊松采样 → 图像组生成 → 奖励计算与策略更新 → 方差统计与类别校准 → 概率列表更新。
- **输出**：经过强化学习微调的 T2I 模型，以及随训练演进的概率列表（反映课程难度的动态变化）。

消融实验（Table 4）证实了这一闭环设计的有效性：在 Flow-GRPO 基线（Overall 94.42）上，依次加入概率采样（+0.73）、探索平衡（+1.32）和类别校准（+1.68），各组件均带来累积增益，其中概率采样贡献了最大的性能提升，验证了方差驱动自适应采样策略的核心作用。

## 核心模块与公式推导

### 3.1 方法总览：四阶段闭环

CGPO 方法由四个顺序阶段构成一个闭环（见 Figure 2），每个训练轮次依次执行：

1. **概率采样（Probability Sampling）**：根据当前概率列表，通过泊松采样范式为每个提示独立做出伯努利决策，生成训练批次 $S_b$。
2. **奖励计算（Reward Calculation）**：为批次中的每个提示生成图像组，计算组内奖励及组相对优势，用于策略训练。
3. **概率计算（Probability Computation）**：利用组奖励统计量更新提示级采样概率和类别级校准权重。
4. **概率更新（Probability Update）**：应用探索平衡与历史平滑后，更新概率列表与类别权重列表。

该闭环的核心机制在于阶段 3 和阶段 4：模型根据当前能力下的奖励信号动态调整下一轮的采样分布，使训练课程随模型能力同步演进。

### 3.2 组奖励方差：提示不一致性的在线代理

CGPO 的核心洞察是：**最具信息量的训练提示位于模型表现不一致的区域**。当模型对某个提示已稳定掌握（奖励高且方差低）或完全无法处理（奖励低且方差低）时，该提示的边际学习效用有限；而当模型部分掌握但尚未稳定时（奖励波动大），该提示恰好处于“最近发展区”，能提供高价值的学习信号。

为量化这种不一致性，CGPO 使用图像组内的奖励方差作为在线代理指标。对于提示 $p$，生成一组 $G$ 张图像 $\{x_1, x_2, \dots, x_G\}$，其组奖励方差定义为：

$$V_p = \operatorname{Var}(\{R_{x_1}, R_{x_2}, \dots, R_{x_G}\}) = \frac{1}{G} \sum_{i=1}^{G} (R_{x_i} - \mu_x)^2$$

其中 $R_{x_i}$ 为第 $i$ 张图像的奖励分数，$\mu_x$ 为组内平均奖励。高 $V_p$ 值表明模型对该提示的掌握程度不稳定，是优先采样的候选对象。

### 3.3 自适应采样概率计算

在概率计算阶段，CGPO 将批次内各提示的方差线性映射到 $[0, 1]$ 区间，得到提案概率 $P^{\mathrm{var}}$：

$$P^{\mathrm{var}}(p) = \frac{V_p - \min(V)}{\max(V) - \min(V)}$$

其中 $\min(V)$ 和 $\max(V)$ 分别为当前批次中所有提示组奖励方差的最小值和最大值。该映射确保高方差提示获得更高的采样提案概率，低方差提示获得较低提案概率。

### 3.4 概率更新：历史平滑与探索平衡

为避免采样概率的剧烈波动和长期忽略部分提示，CGPO 设计了双轨概率更新规则：

$$P^{\mathrm{list'}}(p) = \begin{cases} \frac{1}{3} \sum_{t-2}^{t} P_{(t)}^{\mathrm{var}}(p), & p \in S_b \\ P^{\mathrm{list}}(p) + \frac{1}{N}, & p \notin S_b \end{cases}$$

- **已采样提示**：取最近三次提案概率的均值作为新概率，利用历史平滑抑制单次采样的噪声波动。
- **未采样提示**：概率自增 $1/N$（$N$ 为提示总数），防止某些提示因早期方差低而被永久忽略——随着模型能力提升，这些提示可能在后期重新进入高方差区域，成为有价值的学习信号。

### 3.5 类别校准：比例公平优化

除提示级自适应采样外，CGPO 还引入类别级校准机制，解决不同类别间难度差异导致的训练不均衡问题。该机制基于比例公平优化框架，通过最大化以下目标函数求解类别校准系数：

$$\underset{q}{\operatorname{max}} \sum_{i=1}^{c} \log(q_i) - \lambda \cdot \mathrm{KL}(v \| q), \quad \mathrm{s.t.} \forall i, q_i \geq 0, \sum_{i=1}^{c} q_i = 1$$

其中 $c$ 为类别数，$v_i$ 为类别 $i$ 的参考权重（基于该类内平均奖励），$q_i$ 为待求解的校准系数。KL 散度项 $\mathrm{KL}(v \| q)$ 以超参数 $\lambda$ 控制校准强度：$\lambda$ 越大，$q$ 越接近 $v$，即越倾向于强化弱势类别；$\lambda$ 越小，越倾向于均匀探索。

该优化问题存在闭式解：

$$q_i = \frac{1 + \lambda v_i}{c + \lambda}$$

采样时，将提示级概率乘以对应类别的校准权重 $w_i = q_i$，得到最终采样概率 $\tilde{P}_i^{\mathrm{sampling}} = w_i \times P_i^{\mathrm{list}}$，用于伯努利试验。

### 3.6 关键公式汇总

| 公式 | 变量含义 | 功能 |
|------|----------|------|
| $V_p = \frac{1}{G}\sum_{i=1}^{G}(R_{x_i} - \mu_x)^2$ | $G$：组大小；$R_{x_i}$：单图奖励；$\mu_x$：组均值 | 量化提示掌握不一致性 |
| $P^{\mathrm{var}}(p) = \frac{V_p - \min(V)}{\max(V) - \min(V)}$ | $\min(V),\max(V)$：批次内方差极值 | 方差到采样概率的线性映射 |
| $P^{\mathrm{list'}}(p)$ 分段更新规则 | $S_b$：当前批次；$N$：提示总数 | 历史平滑 + 探索平衡 |
| $q_i = \frac{1 + \lambda v_i}{c + \lambda}$ | $v_i$：类别参考权重；$\lambda$：校准强度 | 类别校准系数闭式解 |

## 实验与分析

### 主要结果

CGPO 在多个基准上以更少的训练步数取得领先性能。所有实验均基于 SD3.5-Medium 作为基础生成模型，在相同的 8 卡 H100 硬件条件下复现 Flow-GRPO，并使用相同的数据集、奖励模型和评估协议。除 CGPO 和 8 GPU 版 Flow-GRPO 外，其他方法的数据来自原始 Flow-GRPO 论文，保证了对比的公平性。

**GenEval 基准**（Table 1）：CGPO 在总体指标上达到 0.96，超越 Flow-GRPO 的 0.94（+0.02）。在关键子指标上，属性绑定（Attribute Binding）从 0.82 提升至 0.89（+0.07），显示出方差驱动采样对复合概念理解的显著增强。在颜色、空间关系和计数等维度上同样取得一致提升。

**T2I-CompBench++ 基准**（Table 2）：使用与 Table 1 相同的模型（仅在 GenEval 生成数据集上训练），CGPO 在纹理（Texture）指标上达到 0.7521，相比 Flow-GRPO 的 0.7298 提升 +0.0223，验证了课程采样策略的跨基准泛化能力。

**DPG Bench 基准**（Table 3）：CGPO 在总体指标上达到 85.5，略优于 Flow-GRPO 的 85.4（+0.1），在密集提示生成任务上保持竞争力。

**多奖励模型实验**（Table 5）：在同时使用 GenEval、OCR 和 PickScore 三个奖励模型的设置下，CGPO 分别达到 0.96 / 0.95 / 23.43，全面超越 Flow-GRPO 的 0.94 / 0.92 / 23.31，证明自适应采样策略在不同奖励信号下均有效。

**训练效率**（Figure 3）：CGPO 仅需 160 GPU 小时即达到 Flow-GRPO 的峰值性能（0.944），训练速度提升一倍，验证了优先采样高边际学习效用提示的效率优势。

### 消融实验

Table 4 以 Flow-GRPO 为基线（Overall 94.42%），逐步累加各组件，揭示了每个设计的独立贡献：

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/007_Table_4.jpg]]
*Table 4: Ablation Studies. Effectiveness analysis of individual components on GenEval. The baseline method is Flow-GRPO. Components are added incrementally. The reported improvements represent the difference from the baseline performance*

- **+Probability Sampling**：Overall 提升至 95.15%（+0.73），贡献了最大的单组件增益。这直接证明了基于组奖励方差的概率采样策略能有效识别并优先选择与模型当前训练阶段匹配的提示。
- **+Exploring Balance**：Overall 进一步提升至 95.74%（+1.32）。该机制为长期未被采样的提示提供概率补偿（每轮自增 $1/N$），防止模型过早收敛到局部最优的提示子集，使后续阶段可能变得有用的提示保持被探索的机会。
- **+Category Calibration**：Overall 达到 96.10%（+1.68）。基于比例公平优化的类别校准方法根据类别内平均奖励动态调整采样权重，有效平衡了类别间的难度差异，强化了弱势类别。

**代理指标对比**（Table 6）：在多个候选代理指标中，奖励方差在 GenEval 上取得最佳 Overall（0.83），优于优势幅度和多准则混合指标，验证了方差作为提示不一致性代理的有效性。

**超参数 λ 研究**（Table 7）：类别校准中的 λ 控制均衡与重点强化之间的平衡。实验表明 λ 需要针对数据集调参，其自适应确定方法值得进一步研究。

### 定性分析

Figure 4 展示了 CGPO 与 SD3.5-Medium 和 Flow-GRPO 在属性绑定、颜色、空间关系和计数等关键维度上的定性对比。CGPO 生成的图像在物体属性正确关联、颜色准确性和空间布局合理性方面均有明显提升，与定量指标一致。

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative Comparison on the GenEval Benchmark. Our method outperforms SD3.5-M and Flow-GRPO in key areas including Attribute Binding, Color, Spatial, and Counting*

Figure 5 通过难度分层追踪了高概率提示（$P^{\mathrm{list}} > 0.7$）在训练过程中的分布演变：难度从 Level 1 逐步推进至 Level 3，直观验证了课程难度随模型能力同步提升的自适应机制。

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/009_Figure_5.jpg]]
*Figure 5: Sampling Probability Difficulty Distribution. We perform difficulty stratification using a single category and then track the number of high-probability prompts (P > 0.7) in the probability list across training steps. The difficulty progressively increases from Level 1 to Level 3*

Figure 6 的训练曲线显示，平均奖励（reward avg）持续上升而奖励标准差均值（reward std mean）先升后降，与“高方差区域逐渐向更难提示转移”的预期一致。

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/012_Figure_6.jpg]]
*Figure 6: Model Training Curves on Weights & Biases. This figure displays the changes in rewards during our model’s training process. Here, reward avg represents the average reward, while reward std mean indicates the mean standard deviation of rewards*

### 失败模式与局限

论文未系统报告失败案例。从方法机理推断，潜在局限包括：方差代理指标在奖励模型噪声较大时的鲁棒性未经验证；类别校准系数 λ 需针对不同数据集手动调整；方法在更大规模、更多样化的训练数据和类别上的扩展性有待检验。上述推断需人工核实原文补充材料。

### 补充图表

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/003_Table_1.jpg]]
*Table 1: GenEval Result. Best results are indicated in bold. Results for all methods, with the exception of our approach and the Flow-GRPO model trained on 8 GPUs, are obtained from the original Flow-GRPO paper*

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/004_Figure_3.jpg]]
*Figure 3: Training Efficiency Comparison. Performancetraining time curves*

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/005_Table_2.jpg]]
*Table 2: T2I-CompBench++ Result. This evaluation uses the same model presented in Table 1, which was trained on the GenEvalgenerated dataset. Best results are indicated in bold*

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/006_Table_3.jpg]]
*Table 3: DPG Bench Result. This evaluation uses the same model presented in Table 1, which was trained on the GenEval-generated dataset. Best results are indicated in bold*

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/010_Table_5.jpg]]
*Table 5: Comparison Experiments with Multiple Rewards*

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/011_Table_6.jpg]]
*Table 6: Comparison of Multiple Proxy Indicators*

![[assets/figures/papers/paper_list_l2165_https_arxiv_org_abs_2605_17807/figures/013_Table_7.jpg]]
*Table 7: Hyperparameter Study. Effect of the hyperparameter λ in Category Calibration*

## 方法谱系与知识库定位

### 1. 基线关系与差异化定位

CGPO 的核心基线是 **Flow-GRPO**，本文将其作为强化学习训练框架的直接对比对象。Flow-GRPO 采用均匀采样策略，所有提示以等概率被选入训练批次。CGPO 在此基础上替换了采样机制，其余训练组件（LoRA 微调、组相对优势计算、奖励模型等）保持一致，消融实验的基线即为 Flow-GRPO 的完整复现（Table 4，8 卡 H100，相同数据集与评估协议）。

CGPO 与 Flow-GRPO 的本质差异在于对“训练信号质量”的建模方式：
- **Flow-GRPO**：隐式假设所有提示对模型学习的边际效用相等，均匀采样。
- **CGPO**：引入组奖励方差作为提示不一致性的在线代理，动态识别模型“部分掌握但尚未稳定”的提示，并提高其采样概率。这一设计使得训练课程随模型能力同步演变，而非静态预设。

从方法谱系看，CGPO 属于**在线课程学习**与**强化微调**的交叉点。其自适应采样思想与以下方向存在关联：
- **课程学习**：传统课程学习依赖预定义的难度度量（如提示长度、语义复杂度），CGPO 则利用模型自身的奖励反馈在线构建课程，避免了人工定义难度指标的局限性。
- **优先级经验回放**：在深度强化学习中，基于 TD-error 优先采样高学习价值的经验。CGPO 将类似逻辑迁移至 T2I 的提示采样，但以组奖励方差替代时序差分误差。
- **主动学习 / 不确定性采样**：高方差提示可视为模型“不确定”的样本，CGPO 的采样策略与不确定性采样原则一致，但操作于图像组而非单样本。

### 2. 适用边界与假设条件

CGPO 的有效性建立在以下假设之上，这些假设同时界定了其适用边界：

1. **奖励模型的可靠性**：组奖励方差作为提示不一致性的代理，其有效性取决于奖励模型能否捕捉到模型对提示要求的掌握程度。当奖励模型噪声较大或与真实生成质量的相关性较弱时，方差信号可能失真。论文未对此进行鲁棒性分析，这是一个需要手动验证的开放问题。

2. **图像组内独立性**：组奖励方差的计算假设同一提示下生成的 G 张图像相互独立。若生成过程存在强条件依赖（如使用固定种子或低温度采样），方差可能无法反映模型的不确定性。

3. **提示空间的覆盖性**：探索平衡机制（未采样提示概率自增 1/N）保证了所有提示最终都有机会被采样，但在极端规模（N 极大）时，低方差提示的采样频率可能极低，类别校准的均衡效果需要进一步验证。

4. **架构与奖励模型的可迁移性**：当前实验基于 **SD3.5-Medium** 作为基础生成模型，并使用 GenEval 生成的提示数据集。该方法在不同 T2I 架构（如自回归模型、基于流的模型）和不同奖励模型组合下的泛化性尚未验证。

### 3. 局限与开放问题

**方法层面**：
- **代理指标的局限性**：Table 6 显示，奖励方差在 GenEval 上取得最佳 Overall（0.83），优于优势幅度和多准则混合指标，但其在噪声环境下的鲁棒性未被探讨。当奖励模型本身存在系统性偏差时，方差可能放大错误信号。
- **超参数敏感性**：类别校准中的 λ 控制均衡与重点强化之间的平衡，Table 7 表明需要针对数据集调参。如何自适应确定 λ 是一个待解决问题。
- **计算开销**：CGPO 需要维护概率列表并对每个提示进行独立采样决策，在大规模提示集上的扩展性有待验证。

**实验层面**：
- 论文未报告 CGPO 在训练过程中的奖励方差变化与模型性能提升之间的因果性统计检验，仅通过 Figure 5 和 Figure 6 进行了趋势展示。
- 多奖励模型实验（Table 5）仅覆盖 GenEval、OCR 和 PickScore 三种奖励组合，更广泛的奖励模型组合下的表现未知。

**开放问题**（来自 verified_analysis）：
1. 该方法在不同奖励模型和不同 T2I 架构（如扩散模型、自回归模型）上的泛化性如何？
2. 方差代理指标在奖励模型噪声较大时的鲁棒性尚未探讨。
3. 类别校准系数 λ 的选取需要针对不同数据集调参，自适应确定方法值得进一步研究。
4. 在更大规模、更多样化的训练数据和类别上的扩展性有待验证。

### 4. 与相关工作的谱系关系

在 T2I 强化微调领域，CGPO 可定位于以下坐标：
- **上游**：**Flow-GRPO** 提供了组相对优势计算的训练框架；**DPO / RLHF** 系列工作提供了从人类偏好到奖励模型的范式基础。
- **平行**：基于提示难度预分类的课程学习方法（如按语义复杂度分层），CGPO 以在线自适应方式替代了静态预分类。
- **下游潜力**：CGPO 的概率采样与类别校准机制可作为插件嵌入其他基于强化学习的 T2I 微调框架，其核心思想——利用模型自身反馈动态调整数据分布——具有跨任务迁移的潜力。

## 原文 PDF

![[paperPDFs/CVPR_2026/Curriculum_Group_Policy_Optimization_Adaptive_Sampling_for_Unleashing_the_Potential_of_Text_to_Image_Generation.pdf]]
