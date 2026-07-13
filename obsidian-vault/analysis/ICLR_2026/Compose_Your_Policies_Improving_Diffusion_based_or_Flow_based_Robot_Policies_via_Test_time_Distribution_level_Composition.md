---
title: "Compose Your Policies! Improving Diffusion-based or Flow-based Robot Policies via Test-time Distribution-level Composition"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Compose_Your_Policies_Improving_Diffusion_based_or_Flow_based_Robot_Policies_via_Test_time_Distribution_level_Composition.pdf
project_link: https://sagecao1125.github.io/GPC-Site/
code_link: null
openreview_forum_id: TnLFRhLuZ6
aliases:
- GPCG
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "凸组合权重 w（取值 0 到 1），通过调整该权重可控制不同策略分数的贡献比例，从而影响最终策略的性能，且最优权重高度依赖于具体任务。"
primary_logic: "将多个预训练策略的分布分数进行凸组合，能够在功能层面降低分数估计误差，并通过扩散采样的稳定性保证将这一改进传播到整个动作轨迹，从而实现在无需额外训练的情况下超越任一父策略的系统性性能提升。"
claims:
- "凸组合分数可以在不训练的情况下产生优于任何单个策略的一步功能目标。"
- "在 Robomimic 和 PushT 基准上，GPC 的组合策略平均成功率相比最强的父策略提升最高达 7.55%（如 Florence-F+FP）。"
- "凸分数组合的理论优势通过稳定性分析可传播到整个采样轨迹，从而降低整体轨迹误差。"
- "Robomimic & PushT 上 Average Success Rate (%) = 86.39 (Florence-Policy-F+FP)"
---

# Compose Your Policies! Improving Diffusion-based or Flow-based Robot Policies via Test-time Distribution-level Composition

> [!tip] 核心洞察
> 将多个预训练策略的分布分数进行凸组合，能够在功能层面降低分数估计误差，并通过扩散采样的稳定性保证将这一改进传播到整个动作轨迹，从而实现在无需额外训练的情况下超越任一父策略的系统性性能提升。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 组合你的策略：通过测试时分布级组合改进基于扩散或流式的机器人策略 |
| 英文题名 | Compose Your Policies! Improving Diffusion-based or Flow-based Robot Policies via Test-time Distribution-level Composition |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=TnLFRhLuZ6) · [Project](https://sagecao1125.github.io/GPC-Site/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | General Policy Composition (GPC) |
| Dataset | Robomimic & PushT, RoboTwin 2.0, Real-world Clean Table |

> [!tip] 效果简介
> - Robomimic & PushT 上，Average Success Rate (%) 为 86.39 (Florence-Policy-F+FP)，对比 78.84 (Florence-Policy-F)，变化 +7.55%。
> - RoboTwin 2.0 上，Average Success Rate 为 0.72 (RDT+DPpcd)，对比 0.65 (DPpcd)，变化 +7%。
> - Real-world Clean Table 上，Successes / 20 trials 为 14/20，对比 12/20 (DPimg) and 7/20 (DPpcd)，变化 +2 and +7。

## 概要

机器人策略学习面临一个根本性瓶颈：单个扩散或流式策略受限于有限的训练数据和模型容量，难以在所有任务上表现优异。不同预训练策略往往具有互补的失败模式——一个策略在视觉模态上表现良好，另一个则在点云输入上更鲁棒——但直接收集大规模交互数据或进行在线微调的成本过高，使得单一策略无法充分利用所有可用的预训练知识。

针对这一问题，本文提出 **General Policy Composition (GPC)**，一种训练无关（training-free）的测试时组合框架。GPC 的核心思想是将多个预训练策略的分布分数进行凸组合，在功能层面降低分数估计误差，并借助扩散采样的稳定性保证将这一改进传播到整个动作轨迹。具体而言，给定 $n$ 个预训练策略的分数函数 $s_{\theta}(\tau_t, t, c_i)$，GPC 的凸组合分数为：

$$\hat{s}_{\mathrm{comp}}(\tau_t, t, c) = \sum_{i=1}^{n} w_i s_{\theta}(\tau_t, t, c_i),\quad \sum_{i=1}^{n} w_i = 1$$

组合权重 $w$ 通过测试时搜索确定，无需任何额外训练或数据。理论分析表明，凸组合分数估计器的均方误差 $Q(w)$ 是关于 $w$ 的凸二次函数，存在最优权重 $w^*$ 使得组合误差不超过任一单独估计器（Proposition 4.1）；进一步地，分数误差的降低通过采样稳定性界线性地转化为终端轨迹精度的提升（Proposition 4.2, Corollary 4.1）。

**主要结果**：在 Robomimic 和 PushT 基准上，GPC 的组合策略平均成功率相比最强父策略提升最高达 **+7.55%**（Florence-F+FP 组合：86.39 vs. 78.84）；在 RoboTwin 2.0 双手操作任务上，RDT+DPpcd 组合平均成功率达 0.72，相比 DPpcd 的 0.65 提升 7%；真实世界实验中，GPC 在 Clean Table 任务上取得 14/20 的成功率，优于图像基线（12/20）和点云基线（7/20）。

**方法定位**：GPC 属于测试时组合方法，可与多种主流扩散或流式策略（DP、MP、FP、Florence-Policy、π0、DP3、RDT 等）兼容。相比需要训练或微调的集成方法，GPC 仅引入约 0.04 秒的推理延迟增量（每动作块从 0.09 秒增至 0.13 秒），且权重搜索的模拟时间开销（约 2.5 小时）远低于训练成本。该方法在处理异构动作块长度和推理步数方面也展现出兼容性。

机器人操作策略的学习在过去几年取得了显著进展，特别是基于扩散模型和流匹配模型的生成式策略，如 **Diffusion Policy**（Chi et al., 2023）、**Florence Policy**（Reuss et al., 2024）和 **π0**（Black et al., 2024）等，在多样化的操作任务上展现了令人瞩目的性能。这些策略将动作生成立为一个条件分布建模问题，通过迭代去噪或流匹配从噪声中逐步恢复出高质量的动作轨迹。然而，尽管单个策略在其擅长领域表现优异，它们在面对不同任务、不同感知模态或不同架构选择时，往往呈现出**互补的失败模式**：一个策略在某个任务上成功，在另一个任务上却可能失败；基于图像的策略和基于点云的策略各有其感知盲区；不同网络架构的策略也各有其归纳偏置的优劣。

这一现象暴露了当前机器人策略学习领域的核心瓶颈：**单个扩散或流式机器人策略受限于有限的训练数据和模型容量，无法在所有任务上表现优异**。要获得一个全能型策略，最直接的思路是收集更大规模的交互数据集或对策略进行在线微调，但这些方式的成本极为高昂——无论是数据采集的人力与时间成本，还是训练所需的计算资源，都使得这一路径在实践中难以规模化。

与此同时，社区中已经积累了大量的预训练策略模型，它们在不同条件（如视觉模态、网络骨干、任务设定）下训练，蕴含着互补的知识。然而，现有方法缺乏一种机制，能够在**不引入额外训练**的前提下，将这些预训练策略的能力进行有机整合。传统的集成方法（如动作空间的平均）往往忽略了扩散策略的核心在于其分布分数（score），而非最终的动作输出，因此难以从分布层面实现真正的能力融合。

本文的核心动机正是源于这一观察：**不同策略往往具有互补的失败模式，单独使用任何单一策略都无法充分利用所有可用的预训练知识**。如果能够在测试时，通过某种方式将多个预训练策略的分布分数进行组合，就有可能在不增加训练成本的情况下，构建出一个超越任一父策略的更强大策略。这一思路将策略改进的焦点从“训练更好的单一模型”转移到了“测试时组合现有模型”，为机器人策略的性能提升开辟了一条低成本、高灵活性的新路径。

## 核心方法与创新机理

### 问题瓶颈

单个扩散或流式机器人策略受限于有限的训练数据和模型容量，难以在所有任务上表现优异。收集大规模交互数据集或进行在线微调成本高昂，而不同策略往往具有互补的失败模式——单独使用任一策略都无法充分利用所有可用的预训练知识。GPC 的核心洞察在于：**无需额外训练，仅通过测试时组合多个预训练策略的分布分数，即可在功能层面降低分数估计误差，并通过扩散采样的稳定性保证将这一改进传播到整个动作轨迹**，从而系统性超越任一父策略。

### 关键创新：测试时凸分数组合

GPC 的创新集中在一个核心操作上——**策略分数获取方式从单一来源变为多源凸组合**。具体而言，GPC 将多个预训练策略（可来自不同视觉模态、网络架构或 VA/VLA 设置）的分数函数进行凸加权求和：

$$\hat{s}_{\mathrm{comp}}(\tau_t, t, c) = \sum_{i=1}^{n} w_i s_{\theta}(\tau_t, t, c_i),\quad \sum_{i=1}^{n} w_i = 1$$

这一设计的理论依据是：凸组合分数估计器的均方误差 $Q(w) = \mathbb{E} \| \varepsilon(w) - s^{*} \|^2$ 是关于权重 $w$ 的凸二次函数，存在最优 $w^*$ 使得组合误差不超过任一单独估计器（Proposition 4.1）。更重要的是，分数误差的减小能通过稳定性界线性转化为终端轨迹精度的提高——若凸组合降低了累积分数误差，则理论误差界严格收紧（$B(s_{\mathrm{comp}}) < \min_i B(s_i)$，Corollary 4.1）。

### 测试时权重搜索

最优组合权重 $w$ 高度依赖于具体任务，GPC 通过在测试时进行离散化网格搜索来确定（Algorithm 1）。搜索过程完全在模拟环境中完成，不涉及物理交互。权重搜索引入了额外的计算开销（约 2.5 小时模拟时间），但相比训练或微调成本仍可忽略。

### 与叠加原理的连接

GPC 框架自然延伸到叠加原理，支持逻辑与（Logical AND）和逻辑或（Logical OR）等更强的组合算子。逻辑与要求各策略分数在采样过程中保持一致，实验表明其带来的性能提升比凸组合更大——例如 DP+MP 的 AND 组合在 Robomimic 上平均成功率达到 64.92，远超基线的 39.19（Table 4）。

### 兼容异构策略

GPC 可与异构的动作块长度和推理步数兼容。当两个策略的动作块长度不同时（如 $H_A \geq H_B$），GPC 采样长度为 $H_A$ 的共享噪声轨迹，仅在重叠的前 $H_B$ 步进行凸分数组合，尾部保持策略 A 的分数不变。此机制使 GPC 能够灵活组合具有不同设计选择的预训练策略，无需修改其架构或训练流程。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_TnLFRhLuZ6/figures/004_Figure_2.jpg]]
*Figure 2: Overview of our proposed General Policy Composition. Combining distributional scores from pre-trained diffusion-based or flow-based policies on different conditions (e.g., visual modalities and network backbones), GPC can generate expressive and adaptable action trajectories through convex score combination without additional training*

**General Policy Composition（GPC）** 是一种训练无关（training‑free）的测试时策略组合框架，其核心思想是将多个预训练扩散或流式策略的分布分数进行凸组合，从而在不进行额外训练或微调的前提下，获得比任一父策略更强的动作生成能力。整体流程由三个串联模块构成：

### 1. 多源分数估计

给定当前观测条件 $c$ 和噪声化动作轨迹 $\tau_t$，GPC 同时调用 $n$ 个预训练策略模型，每个策略在各自的输入模态或架构条件下独立预测分数（或等价地，噪声估计）：

- 策略可以来自不同的视觉模态（如 RGB 图像策略与点云策略）
- 策略可以基于不同的网络架构（如 **Diffusion Policy** (Chi et al., 2023)、**Flow Policy**、**Florence Policy** (Reuss et al., 2024)、**RDT** (Liu et al., 2024a) 等）
- 各策略的条件 $c_i$ 可以不同，但共享同一噪声轨迹 $\tau_t$

这一步的输出是 $n$ 个独立的分数估计 $s_\theta(\tau_t, t, c_i)$，它们各自携带了对应策略从训练数据中习得的分布知识。

### 2. 凸分数组合

GPC 将多个策略的分数通过凸组合（convex combination）融合为单一的复合分数估计：

$$\hat{s}_{\mathrm{comp}}(\tau_t, t, c) = \sum_{i=1}^{n} w_i \, s_\theta(\tau_t, t, c_i), \quad \sum_{i=1}^{n} w_i = 1$$

其中组合权重 $w_i \in [0,1]$ 是框架的核心可调参数。这些权重**不在训练阶段学习**，而是通过**测试时搜索**（test‑time search）在验证任务上以离散网格方式确定最优值。权重搜索引入的计算开销约为 2.5 小时模拟时间（9 个候选权重 × 若干 rollout），但相比训练或微调成本仍可忽略。

理论上，凸组合能够降低单步分数估计的均方误差：当两个估计器的误差项不完全相关时，存在最优权重 $w^*$ 使得组合估计器的误差不超过任一单独估计器（Proposition 4.1）。这一功能层面的改进通过扩散采样的稳定性保证传播到整个轨迹：若组合分数降低了累积分数误差，则终端轨迹误差的理论上界严格降低（Corollary 4.1）。

### 3. 迭代去噪采样

组合分数 $\hat{s}_{\mathrm{comp}}$ 被直接嵌入标准的扩散/流式采样循环中，通过 Langevin 动力学等更新规则从噪声逐步生成动作轨迹：

$$\tau_{t-1} = \alpha_t \tau_t + \beta_t \hat{s}_{\mathrm{comp}}(\tau_t, t, c) + \gamma_t \eta, \quad \eta \sim \mathcal{N}(0, \sigma_t^2 I)$$

整个采样过程与单策略扩散推理完全兼容，仅将原本的单一分数替换为组合分数。由于需要并行运行多个策略模型的前向传播，推理延迟从约 0.09 秒略微增加至 0.13 秒每动作块，仍在可接受范围内。

### 框架的输入输出流

| 阶段 | 输入 | 输出 |
|------|------|------|
| 分数估计 | 观测条件 $c$、噪声轨迹 $\tau_t$、时间步 $t$ | $n$ 个策略的独立分数估计 |
| 凸组合 | $n$ 个分数估计 + 搜索得到的最优权重 $w_i$ | 单一复合分数 $\hat{s}_{\mathrm{comp}}$ |
| 去噪采样 | 复合分数 + 采样超参数 | 最终动作轨迹 $\tau_0$ |

GPC 还支持**叠加组合算子**的扩展：除凸组合外，框架可自然衔接逻辑 OR（按 softmax 加权）和逻辑 AND（强制策略间分数梯度一致）等更强的组合方式。实验表明，逻辑 AND 组合在 Robomimic 上可带来比凸组合更显著的性能提升（如 DP+MP 的 AND 组合平均成功率达 64.92，远超基线的 39.19，见 Table 4）。此外，GPC 兼容异构的动作块长度和推理步数：当两个策略的动作块长度不同时，在重叠部分进行凸组合，非重叠部分保留较长策略的原始分数，即可实现无缝融合。

### 核心模块

GPC 框架由三个顺序执行的模块构成，全程无需训练，仅在测试时组合已有预训练策略。

**多源分数估计 (Score Estimation)**：给定当前带噪动作轨迹 $\tau_t$ 和时间步 $t$，从 $n$ 个预训练策略分别获取条件分数预测 $s_\theta(\tau_t, t, c_i)$，其中条件 $c_i$ 可对应不同的视觉模态（图像、点云）或网络架构（扩散策略、流式策略、VLA 模型）。该模块的输出是 $n$ 个独立的分数估计，承载了不同策略对当前状态下最优动作方向的判断。

**凸分数组合 (Convex Score Composition)**：将各策略的分数进行加权求和，得到组合分数：

$$\hat{s}_{\mathrm{comp}}(\tau_t, t, c) = \sum_{i=1}^{n} w_i s_\theta(\tau_t, t, c_i), \quad \sum_{i=1}^{n} w_i = 1$$

其中 $w_i \in [0,1]$ 为组合权重，通过测试时离散搜索确定最优值。该模块的核心机制在于：当各策略的分数估计误差具有互补性时，凸组合可以在均方误差意义上产生优于任一单独估计器的分数（Proposition 4.1），从而在功能层面降低分数估计误差。

**迭代去噪采样 (Iterative Denoising)**：基于组合分数执行 Langevin 动力学更新，逐步从噪声中恢复动作轨迹：

$$\tau_{t-1} = \alpha_t \tau_t + \beta_t \hat{s}_{\mathrm{comp}}(\tau_t, t, c) + \gamma_t \eta,\quad \eta \sim \mathcal{N}(0, \sigma_t^2 I)$$

其中 $\alpha_t, \beta_t, \gamma_t$ 为扩散调度参数，$\eta$ 为高斯噪声。该模块将组合分数的优势传播到整个采样轨迹：若凸组合降低了累积分数误差，则理论误差界严格缩小（$B(s_{\mathrm{comp}}) < \min_i B(s_i)$，Corollary 4.1），终端轨迹精度因此得到系统性提升。

### 关键公式与理论保证

**凸组合误差函数**：令 $\varepsilon(w) = w\varepsilon_1 + (1-w)\varepsilon_2$ 为两个分数估计器的凸组合误差，则均方误差

$$Q(w) = \mathbb{E} \| \varepsilon(w) - s^{*} \|^2$$

是关于 $w$ 的凸二次函数，存在最优权重 $w^*$ 使得 $Q(w^*) \leq \min(Q(0), Q(1))$，即组合估计器的误差不超过任一单独估计器（Proposition 4.1）。这是 GPC 功能层面改进的理论基础。

**分数到采样的稳定性界**：

$$\mathbb{E} \| x_{\hat{s}}(T) - x^{*}(T) \| \leqslant \left( \int_0^T e^{2\int_t^T \tilde{L}(\tau)d\tau} L_s(t)^2 dt \right)^{1/2} \left( \int_0^T \kappa(t)^2 dt \right)^{1/2}$$

该不等式（Proposition 4.2）将终端轨迹误差上界表示为累积分数误差的单调递增函数，其中 $\tilde{L}(\tau)$ 为 Lipschitz 常数，$\kappa(t)$ 为分数误差项。这意味着分数估计精度的提升会线性地转化为轨迹精度的提高，从而将一步功能优势传播到完整动作序列。

**叠加组合扩展**：在凸组合的基础上，GPC 还支持逻辑 OR 和逻辑 AND 两种叠加算子。逻辑 OR 通过 softmax 函数动态分配权重 $w_i^{1-t} = \text{softmax}(T \log \hat{p}_t(\tau|c_i) + \ell)$，实现从多个分布中采样；逻辑 AND 则要求各策略分数一致（$d\log p_t(\tau|c_i) = d\log p_t(\tau|c_j)$），使采样收敛到所有策略的共识区域。实验表明，AND 组合在父策略互补性强的场景下可带来比凸组合更大的提升（如 DP+MP 的 AND 组合在 Robomimic 上平均达到 64.92，远超基线的 39.19，Table 4）。

> **注意**：以上公式均来自原文 Section 3-5 的推导，变量含义严格以原文定义为准。关于最优权重的解析求解、组合算子的进一步设计等仍为开放问题，文中未提供闭式解。

## 实验与关键发现

### 核心实验设定

GPC 在三个不同规模的基准上进行了验证：**Robomimic**（单臂操作，含 Can/Lift/Square 三个任务）、**PushT**（平面推块任务）、**RoboTwin 2.0**（六项双手操作任务），以及四项真实世界任务（Place Bottles、Hang Mug、Clean Table、Punch Holes）。所有实验均为训练无关（training-free）设定：GPC 仅在测试时对已有的预训练策略进行分数组合，无需任何额外数据、微调或在线交互。

权重搜索采用离散网格扫描，在模拟环境中约需 2.5 小时（Table 6），对于真实世界实验则通过模拟器上的权重搜索结果直接迁移。推理延迟从单策略的 0.09 秒/动作块增加到 GPC 的 0.13 秒/动作块（Table 7），增长幅度在可接受范围内，且完全为计算开销，不涉及物理交互。

*Table 4: Results of GPC with superposition, highlighting performance increase by strong compositional operators. Table 6: Comparison of training/finetuning time vs. GPC weight search. $T _ { \mathrm { e v a l } } = N _ { \mathrm { r o l l o u t } } \times T _ { \mathrm { I } }$ per rollout. For RoboMimic, T RoboMimiceval $\approx$ 2 0 0 * 5 $\mathrm { s }$ = 0 . 2 7 hr. For realworld, $T _ { \mathrm { e v a l } } ^ { \mathrm { R e a l } } { \approx } \mathrm { \dot { 2 } 0 } * \mathrm { 3 0 s }$ = 0 . 1 7 hr

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_TnLFRhLuZ6/figures/014_Table_7.jpg]]
*Table 7: Per–action-chunk inference latency in RoboMimic. The overhead of GPC is modest and purely computational*

### 主要结果

**Table 1** 展示了 Robomimic 和 PushT 上的核心结果。GPC 在所有组合配置上均超越了其最强的父策略：

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_TnLFRhLuZ6/figures/006_Table_1.jpg]]
*Table 1: Experiment results on Robomimic and PushT. The table shows the success rate Ò. Our GPC yields a noticeable average improvement compared with the base policies*

- **Florence-Policy-F + FP** 组合平均成功率达到 86.39%，相比最强父策略 Florence-Policy-F（78.84%）提升 **+7.55%**，是单任务提升最大的组合。
- **π0 + FP** 组合在 Square 任务上达到 94%，在 PushT 上达到 62.25%，平均成功率为 88.94%，为所有组合中最高。
- 跨架构组合（如 DP + MP、Florence-Policy-D + DP）同样获得一致提升，表明 GPC 不依赖特定架构。

**Table 2** 报告了 RoboTwin 双手操作任务的结果。**RDT + DP_pcd** 组合平均成功率达到 0.72，相比 DP_pcd（0.65）提升 **+7%**；**DP_img + DP_pcd** 跨模态组合也获得约 +5% 的平均提升。这验证了 GPC 能够有效融合不同视觉模态（图像与点云）和不同架构（如 RDT 与 DP）的互补信息。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_TnLFRhLuZ6/figures/007_Table_2.jpg]]
*Table 2: Experiment results on RoboTwin with 6 diverse bimanual manipulation tasks. GPC achieves an obvious increase with up to 7% improvement on the success rate*

**Table 5** 展示了真实世界实验结果。在 Clean Table 任务上，GPC 取得 14/20 的成功率，优于 DP_img（12/20）和 DP_pcd（7/20）；在 Place Bottles 任务上，GPC 取得 13/20，优于 DP_img（7/20）和 DP_pcd（11/20）。Figure 8 的轨迹可视化进一步显示 GPC 产生的动作轨迹比单一策略更连贯、更接近目标。

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_TnLFRhLuZ6/figures/012_Table_5.jpg]]
*Table 5: Real-world experiment results, demonstrating the effectiveness of GPC*

### 权重消融与失败模式分析

**Table 3** 系统性地考察了组合权重对 GPC 性能的影响，揭示了三个关键发现：

![[assets/figures/papers/paper_list_l16_https_openreview_net_forum_id_TnLFRhLuZ6/figures/008_Table_3.jpg]]
*Table 3: Experiment results of our method under different composition configurations. These results highlight GPC’s versatility and the importance of weight tuning across policies*

1. **最优权重高度依赖任务**：同一对父策略在不同任务上的最优权重 w 可能完全不同。例如在 Empty Cup Place 任务上，最优权重 w₁=0.4 带来 **+24%** 的巨大提升（从 DP_img 的 0.42 和 DP_pcd 的 0.62 提升至 0.86），而在其他任务上最优权重则偏向于更强的父策略。

2. **父策略性能差距过大时提升有限**：当两个父策略中一个表现极差时，组合难以带来显著增益。这是因为凸组合的分数估计被限制在父策略分数构成的凸包内，无法超越表现更好的父策略太多。提升最大的场景是**两个父策略均具有中等准确度且失败模式互补**的情况（如 Empty Cup Place）。

3. **更强父策略通常应获得更大权重**：文中建议将更强策略的权重偏向 >0.5，这一启发式规则在大多数任务上有效，但并非绝对——Empty Cup Place 的反例（最优权重 0.4，偏向较弱策略）说明互补性有时比绝对强度更重要。

### 叠加组合的进一步增益

**Table 4** 探索了超越凸组合的叠加算子。**逻辑与（Logical AND）** 组合在多个配置上带来了比凸组合更大的提升：

- **Florence-Policy-D + DP** 的 AND 组合在 Robomimic 上平均达到 90.50%（Can）、100%（Lift）、100%（Square），远超基线的 39.19%。
- **DP + MP** 的 AND 组合平均达到 64.92，同样远超单策略基线。

逻辑与组合要求各策略在采样过程中达成一致，本质上是取各策略分布的“交集”，从而产生更保守但更可靠的预测。这一结果揭示了组合算子设计的重要性——更强大的组合方式可能带来远超简单凸平均的性能。

### 定性可视化分析

**Figure 3** 通过三组对比案例展示了 GPC 的定性优势：
- 第一行：DP_img 失败（红色叉号），DP_pcd 成功，GPC 成功——GPC 继承了成功策略的行为。
- 第二行：DP_img 成功，DP_pcd 失败，GPC 成功——GPC 同样能过滤掉失败策略的噪声。
- 第三行：两者均成功，但 GPC 产生更优轨迹——组合分数引导采样进入两个分布的重叠高密度区域。

**Figure 4** 从分布层面分析了不同模态和架构组合下的样本分布。适当的权重配置使 GPC 产生的样本分布更接近真实动作分布，且具有比单个策略更高的成功率。

**Figure 5** 展示了完整执行时间内的样本分布演化。GPC 产生的分布在时间维度上比基线更连贯，说明分数层面的改进通过扩散采样的稳定性传播到了整个动作轨迹，与 Proposition 4.2 的理论预测一致。

### 异构配置与多策略扩展

GPC 支持**异构动作块长度**和**不同推理步数**的组合。**Table 8** 显示，当 DP（块长 8，执行 5 步）与 Florence-Policy-D（块长 16，执行 10 步）组合时，GPC 通过在重叠部分进行分数组合，将成功率从 0.50/0.53 提升至 0.66。这表明 GPC 不需要父策略具有统一的输出格式。

**Table 9** 进一步展示了三策略组合的可行性：**FP + FP-F + π0** 在 Can 和 Lift 任务上均达到 100% 成功率，Square 任务达到 94%。然而，随着策略数量增加，权重搜索空间呈指数增长，计算成本问题凸显。

### 失败模式与局限

尽管 GPC 在大多数场景下表现优异，但仍存在明确的失败边界：

1. **父策略均失败时无法挽救**：当两个父策略在某个任务上均表现极差时，凸组合无法凭空产生有效行为，因为组合分数仍在父策略分数的凸包内。
2. **权重搜索引入额外计算开销**：离散网格搜索在模拟环境中约需 2.5 小时，虽然远低于训练或微调成本，但对于需要快速部署的场景仍是不小的负担。
3. **推理延迟增加**：从 0.09 秒增至 0.13 秒/动作块，对实时性要求极高的场景需注意。
4. **多策略扩展的维度灾难**：目前实验集中在双策略或三策略组合，扩展到更多策略时权重搜索空间呈指数增长，需要更高效的搜索策略。

## 定位与知识库关联

### 与现有方法的关系

#### 基策略谱系

GPC 构建于一系列扩散策略和流式策略之上，这些策略构成了组合的“父策略”池。主要基策略包括：

- **扩散策略（Diffusion Policy, DP）**（Chi et al., 2023）：将机器人动作生成建模为条件扩散过程，通过迭代去噪从高斯噪声中恢复动作轨迹。
- **Mamba Policy (MP)**（Cao et al., 2025b）：基于状态空间模型的扩散策略变体，提供不同于 Transformer 架构的分数估计。
- **Flow Policy (FP)**：基于流匹配的策略，通过学习常微分方程定义的向量场来生成动作。
- **Florence Policy-D / Florence Policy-F**（Reuss et al., 2024）：分别基于扩散和流式架构的视觉-语言-动作策略，利用 Florence 视觉编码器。
- **π0**（Black et al., 2024）：流匹配策略。
- **DP3**（Ze et al., 2024b）：基于点云的 3D 扩散策略。
- **RDT**（Liu et al., 2024a）：基于扩散 Transformer 的机器人策略。

这些策略在架构（Transformer、状态空间模型）、输入模态（RGB 图像、点云、文本）和生成机制（扩散、流匹配）上存在差异，从而产生互补的失败模式，这正是 GPC 组合增益的来源。

#### 与模型组合方法的关系

GPC 属于测试时模型组合（test-time model composition）范式，与以下方法形成对比：

- **集成方法（Ensemble）**：传统集成通过平均多个模型的输出预测来降低方差，但通常要求模型输出在同一空间（如离散动作分布）。GPC 在分数空间而非动作空间进行组合，保留了扩散采样的生成能力。
- **叠加原理（Superposition）**（Skreta et al., 2024）：通过逻辑 OR（混合分布采样）或逻辑 AND（分数一致性约束）组合多个概念条件。GPC 将凸组合作为基础算子，并自然扩展至 OR/AND 操作——逻辑 OR 通过 softmax 加权实现，逻辑 AND 通过强制分数一致性实现。实验表明，AND 组合在特定场景下可带来更大幅度的提升（如 DP+MP 的 AND 组合在 Robomimic 上平均达到 64.92，远超基线的 39.19，见 Table 4）。
- **分类器引导（Classifier Guidance）**：通过在扩散采样中引入额外梯度项来施加条件控制。GPC 不依赖分类器，直接组合预训练策略的分数函数，避免了训练分类器的开销。

#### 与训练范式的关系

GPC 的核心定位是**训练无关（training-free）**的测试时增强框架。与以下范式形成互补而非替代：

- **微调（Fine-tuning）**：需要额外交互数据或演示数据，成本高昂。GPC 无需任何训练或数据收集，仅利用现有预训练模型。
- **联合训练（Joint Training）**：从零开始训练多模态策略需要大规模多模态数据集。GPC 允许独立训练的单模态策略在测试时组合，降低了对联合数据的需求。
- **在线适应（Online Adaptation）**：需要物理交互和试错。GPC 的权重搜索在模拟环境中完成（约 2.5 小时），不涉及物理交互。

### 适用边界

#### 有效场景

- **父策略具有互补失败模式**：当两个父策略在不同任务或不同操作阶段表现出互补的优势时，GPC 的组合效果最为显著。例如，在 Empty Cup Place 任务中，DP_img 成功率为 0.42，DP_pcd 为 0.62，而 GPC 在最优权重下达到 0.86（+24%），表明两者在不同阶段提供了互补信息。
- **父策略均具有中等准确度**：当两个父策略都具备一定能力但均不完美时，凸组合可以通过抵消各自的估计误差来获得更优的分数估计。这是 Proposition 4.1 的直接推论——凸组合分数估计的均方误差 $Q(w) = \mathbb{E} \| \varepsilon(w) - s^{*} \|^2$ 是关于 $w$ 的凸二次函数，存在最优 $w^*$ 使得误差不超过任一单独估计器。
- **跨模态组合**：不同视觉模态（图像 vs. 点云）的策略组合能捕获互补的几何和语义信息，在 RoboTwin 2.0 上平均提升 5-7%。
- **跨架构组合**：不同网络架构（如 Transformer vs. 状态空间模型）的策略组合能融合不同的归纳偏置，在 Robomimic 上平均提升 2-7%。

#### 受限场景

- **父策略性能差距过大**：当某一父策略的成功率极低时，凸组合难以获得显著提升。因为凸组合的分数位于两个父策略分数的凸包内，若一个策略的分数估计严重偏离真实分数，组合也难以修正。
- **父策略均失败**：如果两个父策略在某个任务上均接近随机水平，GPC 无法凭空产生有效行为——组合只能利用已有知识，不能创造新知识。
- **实时性要求极高的场景**：GPC 增加了推理延迟（从 0.09 秒到 0.13 秒每动作块），虽然增量不大，但在需要亚毫秒级响应的场景中需谨慎评估。

### 局限与开放问题

#### 方法局限

1. **测试时权重搜索开销**：GPC 需要离散化搜索最优组合权重，在模拟环境中约需 2.5 小时（$T_{\text{search}} = N_{\text{search}} \times T_{\text{eval}}$，$N_{\text{search}}=9$ 个权重候选）。虽然远低于训练或微调成本，但限制了快速部署。
2. **离散搜索精度损失**：权重搜索采用离散化方式（步长 0.1），可能无法精确找到最优连续权重 $w^*$，引入性能损失。
3. **推理延迟增加**：每动作块的推理时间从 0.09 秒增加到 0.13 秒，因为需要运行多个策略的分数估计。
4. **策略数量扩展困难**：当前实验主要集中在双策略组合，扩展到三策略（如 FP+FP-F+π0）虽可行但会带来组合爆炸——$n$ 个策略需要搜索 $n-1$ 维权值空间。
5. **组合算子有限**：目前主要使用凸组合及少量逻辑组合（OR/AND），更强大的组合方式（如基于置信度的自适应加权、非线性组合）尚待探索。

#### 开放问题

1. **高效权重搜索策略**：能否开发基于梯度的自适应权重搜索，或利用少量验证样本快速估计最优权重，以替代固定的离散网格搜索？例如利用 Proposition 4.1 的凸性，通过少量采样点拟合二次函数来推断最优权重。

2. **多策略高效组合**：如何将 GPC 从双策略组合高效扩展到多策略（$n > 3$）组合？可能的路径包括：共享特征编码器以减少重复计算；在紧凑的隐空间中进行组合；或采用层次化组合策略。

3. **组合算子的理论拓展**：凸组合保证了分数在凸包内，但最优分数可能位于凸包之外。能否设计更灵活的组合算子（如基于不确定性的自适应加权、稀疏组合）以突破凸包限制？

4. **非扩散策略的泛化**：GPC 框架能否泛化到非扩散策略？自回归 Transformer 策略、能量基模型等具有不同的采样机制，如何定义和组合其“分数”是一个开放挑战。

5. **在线动态权重适应**：当前权重在测试前一次性搜索确定。能否在真实在线环境中根据任务进展动态调整权重？例如，在操作的不同阶段（接近、抓取、放置）自动切换主导策略。

6. **组合泛化性的理论理解**：组合策略的泛化能力与各父策略训练数据分布之间的关系尚不明确。能否通过组合来提升对未见场景的泛化性？这需要理解分数组合在分布外样本上的行为。

7. **异构动作空间的组合**：当前 GPC 通过重叠部分组合分数来处理异构动作块长度，但更根本的挑战在于不同策略可能输出不同维度的动作空间（如位置控制 vs. 速度控制）。如何在这些异构空间中进行组合仍是一个开放问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Compose_Your_Policies_Improving_Diffusion_based_or_Flow_based_Robot_Policies_via_Test_time_Distribution_level_Composition.pdf]]
