---
title: "Towards Bridging the Gap between Large-Scale Pretraining and Efficient Finetuning for Humanoid Control"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Towards_Bridging_the_Gap_between_Large_Scale_Pretraining_and_Efficient_Finetuning_for_Humanoid_Control.pdf
project_link: https://lift-humanoid.github.io
code_link: null
openreview_forum_id: NEOTsyyYH7
aliases:
- LLSPEF
- TBGBLSPEFHC
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "在微调阶段执行确定性策略，将随机探索完全限制在物理信息世界模型内，并利用大规模SAC预训练为模型提供良好初始化，从而解耦安全数据收集与充分探索，同时提升样本效率与安全性。"
primary_logic: "SAC配合大批量更新和高UTD可以在GPU上实现类似PPO的快速收敛并zero-shot部署，且其随机策略兼容基于模型的学习；将SAC预训练与基于物理信息的世界模型离线预训练结合，能在微调时通过模型内探索实现数据高效且安全的适应。"
claims:
- "SAC with large-batch updates and high UTD ratio achieves fast convergence and zero-shot deployment on a physical humanoid robot."
- "LIFT finetuning converges across in-distribution and out-of-distribution target speeds, while PPO, SAC, FastTD3, and SSRL degrades or fails."
- "Removing world model pretraining slows down training; removing large-scale SAC pretraining leads to non-convergence (poor local minima)."
- "SAC policy outperforms PPO in stability and sample efficiency during preliminary model-based finetuning."
---

# Towards Bridging the Gap between Large-Scale Pretraining and Efficient Finetuning for Humanoid Control

> [!tip] 核心洞察
> SAC配合大批量更新和高UTD可以在GPU上实现类似PPO的快速收敛并zero-shot部署，且其随机策略兼容基于模型的学习；将SAC预训练与基于物理信息的世界模型离线预训练结合，能在微调时通过模型内探索实现数据高效且安全的适应。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 面向人形控制的大规模预训练与高效微调桥接方法 |
| 英文题名 | Towards Bridging the Gap between Large-Scale Pretraining and Efficient Finetuning for Humanoid Control |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=NEOTsyyYH7) · [Project](https://lift-humanoid.github.io) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | LIFT (Large-scale pretraIning and efficient FineTuning) |
| Dataset | Booster T1 sim-to-sim finetuning (target speeds: 0.6, 1.0, 1.2, 1.5 m/s), Unitree G1 sim-to-sim finetuning (target speeds: 0.6 |

> [!tip] 效果简介
> - Booster T1 sim-to-sim finetuning (target speeds: 0.6, 1.0, 1.2, 1.5 m/s) 上，收敛性与速度跟踪精度 为 LIFT在所有速度下收敛，稳定跟踪目标速度，身体振荡显著减少，对比 SAC快速发散；PPO逐渐退化并崩溃；FastTD3剧烈振荡不收敛；SSRL在高速度下失败，变化 LIFT显著优于所有基线。
> - Unitree G1 sim-to-sim finetuning (target speeds: 0.6, 1.5 m/s) 上，行走稳定性和奖励性能 为 LIFT在0.6 m/s下振荡大幅减少，在1.5 m/s下成功由站立到行走，对比 基线方法性能差或发散，变化 LIFT表现出更稳定的人类行走步态。

## 概要

人形机器人的运动控制长期面临一个两难困境：**大规模预训练**需要快速、稳定的策略学习，而**高效微调**则要求在新环境中安全、数据高效地适应。当前主流的on-policy方法（如PPO）虽能借助大规模并行仿真快速收敛，但其on-policy特性导致微调时样本效率低下，且随机探索在真实环境中存在安全隐患；off-policy方法（如SAC）虽可复用数据，但在人形机器人大规模预训练中收敛缓慢、稳定性差；基于模型的方法（如MBPO）则因世界模型预测误差累积而难以可靠微调。这三类方法之间的张力构成了**预训练到高效微调之间的核心瓶颈**。

本文提出 **LIFT（Large-scale pretraIning and efficient FineTuning）**，一个三阶段框架来桥接这一差距。其核心洞察是：**将随机探索与安全数据收集解耦**——在微调阶段，真实环境中仅执行确定性策略，而将充分探索限制在物理信息世界模型内部。这一设计的关键使能因素是：SAC配合大批量更新和高更新-数据比（UTD）可在GPU上实现与PPO相当的快速收敛，且其随机策略天然兼容基于模型的学习。

LIFT的三个阶段分别为：
1. **大规模SAC策略预训练**：利用JAX实现的高UTD SAC在数千个并行环境中快速训练，获得可zero-shot部署的基础策略，同时记录所有transition数据。
2. **物理信息世界模型离线预训练**：基于Brax可微动力学引擎，结合残差网络学习接触力、耗散力矩等未建模效应，从离线数据中训练精确的世界模型。
3. **策略与世界模型联合微调**：在目标环境中执行确定性策略收集真实数据以微调世界模型，随后在世界模型内进行随机策略探索生成合成数据，更新actor-critic。

实验表明，LIFT在Booster T1和Unitree G1人形机器人的sim-to-sim微调中，**在所有目标速度下均稳定收敛**，而SAC快速发散、PPO逐渐退化并崩溃、FastTD3剧烈振荡、SSRL在高速任务中失败。消融实验进一步揭示：去除世界模型预训练会显著拖慢收敛速度；去除大规模SAC预训练则导致策略陷入局部极差而完全无法收敛；将物理信息世界模型替换为纯神经网络集成模型（如MBPO）则使预测误差急剧升高、策略回报归零。真实世界微调实验也验证了LIFT在实地环境中的有效性。

LIFT的方法定位处于**大规模off-policy预训练**与**物理信息模型基强化学习**的交叉点：它继承了SAC的样本效率与探索能力，同时利用物理先验约束世界模型预测，从而在微调阶段实现安全且数据高效的适应。与纯on-policy预训练-微调范式（PPO）和纯黑盒世界模型方法（MBPO）相比，LIFT通过**预训练算法选择**（SAC而非PPO）、**世界模型结构设计**（物理信息而非黑盒）、**探索-执行解耦**三个关键设计，系统性地解决了从大规模预训练到安全高效微调的过渡问题。



### 人形机器人控制的规模化瓶颈

人形机器人的运动控制正经历从手工设计到数据驱动范式的深刻转变。大规模并行仿真使得强化学习（RL）能够在数小时内训练出可部署的策略，但这一成功主要集中在 **on-policy** 方法——尤其是 **PPO**（Schulman et al., 2017）——之上。PPO 借助数千个并行环境实现了快速收敛，然而其根本局限在于：**每次策略更新后必须丢弃旧数据**，导致样本效率低下。当机器人被部署到与训练环境存在物理差异的新场景时，PPO 需要在新环境中重新收集大量交互数据，且随机探索过程可能引发跌倒、硬件损伤等安全风险。

这一矛盾指向了人形机器人控制领域的核心瓶颈：**大规模预训练与高效安全微调之间存在明显断层**。预训练阶段追求速度与稳定性，微调阶段则要求样本效率与安全性，而现有方法难以同时满足这两个阶段的需求。

### 现有方法的系统性缺陷

#### On-policy 方法的微调困境

PPO 在预训练中表现优异，但在微调场景下暴露出两个致命弱点。其一，on-policy 的数据利用方式意味着每步环境交互只能支持一次梯度更新，当微调预算有限时，策略难以从稀疏的新环境数据中提取足够信息。其二，PPO 的随机探索在微调初期尤为危险——人形机器人在陌生动力学条件下执行随机动作，极易触发不稳定状态。实验表明，PPO 在微调过程中性能逐渐退化并最终崩溃（Figure 2），且其对初始动作标准差的敏感度极高（Figure 6）。

#### Off-policy 方法的稳定性挑战

Off-policy 方法理论上可通过复用历史数据提升样本效率，但将其应用于人形机器人大规模预训练时面临严峻的稳定性问题。**SAC**（Haarnoja et al., 2018b）作为代表性 off-policy 算法，在标准设置下难以匹配 PPO 的收敛速度；**FastTD3**（Seo et al., 2025）虽针对大规模并行训练做了优化，但在微调阶段出现剧烈振荡，无法稳定收敛（Figure 2）。根本原因在于：这些方法在微调时仍需在真实环境中执行随机策略以维持探索，而人形机器人的高维动作空间和接触密集型动力学使得随机探索的代价极高。

#### Model-based 方法的精度与安全鸿沟

基于模型的方法提供了另一种思路——在世界模型中生成合成数据进行策略优化，从而减少真实环境交互。**SSRL**（Levy et al., 2024）利用物理信息世界模型从零训练四足机器人，证明了混合动力学模型的潜力。然而，将该方法直接迁移到人形机器人面临两个障碍：从零开始训练世界模型和策略需要大量不安全的环境交互；人形机器人的接触模式远比四足机器人复杂，对模型精度要求更高。另一方面，纯神经网络世界模型（如 **MBPO**，Janner et al., 2019）在预测误差上显著劣于物理信息模型，导致策略微调完全失败（Figure 5）。

### 核心洞察：解耦探索与执行

上述分析揭示了一个关键的结构性矛盾：**策略优化需要充分探索，但人形机器人的真实环境探索代价高昂且不安全**。LIFT 的核心洞察在于将这一矛盾拆解为两个可独立求解的子问题：

1. **预训练阶段**：SAC 配合大批量更新和高 Update-To-Data（UTD）比率，可以在 GPU 上实现与 PPO 相当的快速收敛，同时其随机策略天然兼容基于模型的学习范式。这为世界模型提供了丰富的训练数据，也为微调提供了良好的策略初始化。

2. **微调阶段**：在真实环境中执行**确定性策略**（仅使用动作均值），将随机探索完全限制在**物理信息世界模型**内部。这一设计实现了安全与效率的双重收益——真实环境的交互数据仅用于微调世界模型，而策略的充分探索发生在模型生成的合成轨迹中，避免了不安全动作的直接执行。

这一解耦策略的可行性建立在两个关键前提之上：SAC 预训练策略提供了足够好的初始行为，使得确定性执行不会导致性能崩溃；物理信息世界模型具备足够的预测精度，使得模型内的探索能够产生有效的学习信号。消融实验证实了这两个前提的不可或缺性——去除 SAC 预训练导致策略陷入局部极差而无法收敛，去除世界模型预训练则显著拖慢训练速度（Figure 4）。



## 核心方法与创新机理

LIFT 的核心创新在于通过**预训练–微调流程中的三个关键设计变更**，系统性地桥接了大规模人形控制策略预训练与安全高效微调之间的鸿沟。这些变更并非孤立的技术点，而是围绕一个统一的因果机制展开：**将随机探索与安全数据收集解耦**。

### 关键设计变更

**1. 预训练算法：从 PPO 到高 UTD 大批量 SAC**

主流人形机器人预训练普遍采用 on-policy 的 **PPO**（Schulman et al., 2017），因其在大规模并行仿真中收敛快速。然而 PPO 的策略是确定性的（仅输出动作均值），无法直接兼容基于模型的探索需求。LIFT 转而采用 **SAC**（Haarnoja et al., 2018b），并配合两个关键实现选择：

- **高 UTD 比率（Update-To-Data ratio）**：在单步环境交互后进行多次梯度更新，显著提升样本效率。实验表明，将 UTD 从 1 提升到 10 即可大幅加速收敛（Figure 9）。
- **大批量更新**：利用 JAX 的固定张量形状和编译内核复用，在单张 GPU 上支持数千个并行环境的大批量更新，无额外数据传输开销。

这一组合使 SAC 在预训练阶段的收敛速度与 PPO 相当甚至更快——在 Booster T1 运动任务上，收敛时间从约 7 小时缩短至约 0.5 小时。更重要的是，SAC 的随机策略（输出状态依赖的均值与方差）天然兼容后续基于模型的探索，而 PPO 的确定性策略在此场景下性能高度敏感于初始动作标准差（Figure 6）。

**2. 微调探索方式：真实环境确定性执行 + 世界模型内随机探索**

传统微调方法（无论是 PPO、SAC 还是 **FastTD3**（Seo et al., 2025））在目标环境中直接执行随机策略进行探索。这在人形机器人上风险极高：随机动作可能导致跌倒、硬件损坏，且样本效率低下。

LIFT 的核心机制创新在于**将探索与执行解耦**：

- **真实环境中**：仅执行确定性策略（使用动作均值 $\mu_\theta(s)$），确保数据收集的安全性。
- **世界模型中**：使用完整的随机策略 $\pi_\theta(a|s) = \mathcal{N}(\mu_\theta(s), \Sigma_\theta(s))$ 进行 rollout，在模型内充分探索并生成合成数据用于策略更新。

这一设计直接解决了人形机器人微调中的安全–探索困境：确定性执行保证安全，模型内探索保证样本效率。消融实验证实，若移除这一解耦机制（即直接在环境中随机探索），SAC 快速发散，PPO 逐渐退化并最终崩溃（Figure 2）。

**3. 世界模型：物理信息结构 + 离线预训练**

与 **MBPO**（Janner et al., 2019）等使用纯神经网络集成世界模型的方法不同，LIFT 采用**物理信息世界模型**，将已知的拉格朗日动力学与可学习的残差网络结合：

$$M(q_t) \ddot{q}_t + C(q_t, \dot{q}_t) + G(q_t) = B\tau_t + \underbrace{J^\top F_t^e + \tau_t^d}_{\text{残差网络学习}}$$

残差网络 $\tau_\phi(s_t, a_t)$ 仅需预测接触力 $J^\top F_t^e$ 和耗散力矩 $\tau_t^d$ 等未建模效应，而非从头学习整个动力学。这一归纳偏置使世界模型预测精度远超纯神经网络方法。消融实验（Figure 5）显示，替换为 MBPO 的神经网络集成世界模型后，MSE 显著升高，策略回报接近零。

此外，LIFT 将世界模型训练与策略训练**完全解耦**：在 SAC 预训练期间将所有 transition 记录到磁盘，策略收敛后离线训练世界模型。这与 Dreamer、MBPO 等在线联合训练的方法形成对比，在大规模并行场景下显著提升了墙钟效率。消融表明，去除世界模型预训练虽仍能最终收敛，但训练速度明显减慢（Figure 4）。

### 创新间的因果依赖

三个设计变更之间存在强因果依赖，形成完整链条：

- **SAC 预训练**为世界模型提供高质量离线数据，同时为微调提供良好初始策略。去除 SAC 预训练直接导致策略陷入局部极差、完全无法收敛（Figure 4）。
- **物理信息世界模型**的准确性是模型内探索有效性的前提。模型预测误差过大会导致策略在虚假动态上优化，最终在真实环境中失败。
- **确定性执行 + 模型内探索**的解耦机制依赖于世界模型提供可靠的“想象”环境，同时依赖于 SAC 随机策略在模型内产生有意义的探索行为。

三者共同构成了一个闭环：SAC 预训练 → 高质量世界模型 → 安全的模型内探索 → 高效的策略微调。缺失任一环节，整个流程的性能都会显著退化或完全失败。



![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/001_Figure_1.jpg]]
*Figure 1: Large-scale pretraIning and efficient FineTuning (LIFT) Framework. In stage (i), we implement SAC in JAX to support large-batch update and high UTD, achieving fast, robust convergence in massively parallel simulation and zero-shot deployment to a real humanoid in outdoor experiments. In stage (ii), we pretrain a physics-informed world model on the SAC data, combining Lagrangian dynamics with a residual predictor to capture contact forces and other unmodeled effects. In stage (iii), we finetune both the policy and the world model to new environments while executing only deterministic actions in the environment. Stochastic exploration is confined to rollouts within the world model. This frame...*

### 核心瓶颈与设计动机

人形机器人控制面临一个根本性张力：大规模并行仿真中的 on-policy 强化学习（如 PPO）虽能快速收敛，但其样本效率低下，且在新环境中执行随机探索存在严重安全风险；而 off-policy 或 model-based 方法虽可复用数据，却在大规模预训练中稳定性不足、耗时长。LIFT（Large-scale pretraIning and efficient FineTuning）正是针对这一“预训练效率”与“微调安全性”之间的鸿沟而设计。

### 三阶段流水线

LIFT 将人形机器人从零训练到新环境适应的完整流程解耦为三个顺序阶段，如图 1 所示：

**阶段一：大规模 SAC 策略预训练。** 在 MuJoCo Playground 中，采用 JAX 实现的高 UTD（Update-To-Data ratio）大批量 Soft Actor-Critic，在数千个并行仿真环境中训练人形运动策略。非对称 actor-critic 架构使 actor 仅接收本体感知状态，而 critic 可访问特权信息。该阶段的关键工程决策是：将 UTD 比率从常规的 1 提升至 10–20，配合大批量更新（batch size 达 4096–8192），使 SAC 在单张 NVIDIA RTX 4090 GPU 上约半小时内即可收敛，并实现真实机器人 zero-shot 部署。预训练过程中，所有 transition 数据被记录至磁盘，供下一阶段使用。

**阶段二：物理信息世界模型离线预训练。** 基于 Brax 的可微刚体动力学引擎，构建一个混合世界模型：已知的拉格朗日动力学方程提供刚性运动先验，残差网络则学习接触力、耗散力矩等未建模效应。世界模型以端到端方式从离线数据中训练，最小化对角高斯负对数似然损失，同时输出下一特权状态的预测均值与异方差不确定性。与 MBPO、Dreamer 等在线训练范式不同，LIFT 将世界模型训练与策略训练完全解耦，从而在大规模并行场景下获得显著的墙钟效率优势。

**阶段三：策略与世界模型联合微调。** 这是 LIFT 实现安全高效适应的核心机制。在新环境（如 Brax 仿真或真实机器人）中，策略仅执行确定性动作（使用 actor 输出的均值），从而杜绝真实环境中的随机探索风险。收集到的确定性轨迹用于微调世界模型，使其适应新动力学。随后，在世界模型内部执行随机策略 rollout，利用 SAC 的熵正则化探索生成合成数据，更新 actor 与 critic 网络。安全重置条件（基于躯干高度、速度、关节限位等物理界限）在世界模型 rollout 中终止不安全轨迹，防止错误状态传播。

### 输入输出流与模块关系

三个阶段的依赖关系是单向且渐进的：阶段一的输出是收敛的 SAC 策略参数和全量 transition 数据集；阶段二消费该数据集，输出预训练的世界模型参数；阶段三同时加载预训练策略与世界模型，在目标环境中交替执行“真实环境确定性数据收集 → 世界模型微调 → 模型内随机探索与策略更新”的循环。这种设计使得随机探索的“风险”被完全隔离在世界模型之内，而真实环境中始终执行安全的确定性策略，从而在样本效率与部署安全性之间建立了因果解耦。



LIFT 框架由三个顺序模块构成：大规模 SAC 策略预训练、物理信息世界模型预训练、以及策略与世界模型联合微调。三个模块的因果链条为：SAC 预训练提供良好的策略初始化和世界模型训练数据；世界模型预训练将未建模动力学（接触力、耗散力矩）编码为残差网络，使模型具备精确的前向预测与不确定性估计能力；微调阶段则在真实环境中执行确定性策略以保证安全，同时将随机探索完全限制在世界模型内，利用 SAC 的随机策略在模型生成数据上更新 actor-critic，从而实现样本高效且安全的适应。

### 大规模 SAC 策略预训练

预训练阶段采用非对称 actor-critic 结构的 SAC 算法。Actor 仅接收本体感知状态 $s_t$，输出高斯分布的均值与方差：

$$\pi_{\theta}(a \mid s) = \mathcal{N}(\mu_{\theta}(s), \Sigma_{\theta}(s))$$

Critic 网络 $Q_{\psi_i}(s_t^p, a_t)$ 则接收特权状态 $s_t^p$（包含环境真值信息）与动作 $a_t$，最小化带熵正则的贝尔曼残差：

$$\mathbb{E}_{(s_t^p, a_t, r_{t+1}, s_{t+1}^p) \sim \mathcal{D}, a_{t+1} \sim \pi_\theta(\cdot|s_{t+1})} \left[ Q_\psi(s_t^p, a_t) - \left( r_{t+1} + \gamma \left( \min_{i=1,2} Q_{\bar{\psi}_i}(s_{t+1}^p, a_{t+1}) - \alpha \log \pi_\theta(a_{t+1}|s_{t+1}) \right) \right)^2 \right]$$

Actor 的优化目标为最大化熵增广的 Q 值：

$$\mathbb{E}_{s_t, s_t^p \sim \mathcal{D}, a_t \sim \pi_\theta(\cdot|s_t)} \left[ \alpha \log \pi_\theta(a_t|s_t) - \min_{i=1,2} Q_{\psi_i}(s_t^p, a_t) \right]$$

其中 $\alpha$ 为熵温度系数，控制探索与利用的平衡。实现上，SAC 以 JAX 编写，利用固定张量形状实现高效算子融合和编译内核复用，支持大批量更新（batch size 可达数千）和高 UTD 比率（Update-To-Data ratio），在单张 GPU 上以数千个向量化环境并行训练，无需额外数据传输开销。所有输入特征通过运行均值和方差进行归一化，确保训练过程中特征尺度均衡。

### 物理信息世界模型预训练

世界模型基于拉格朗日动力学方程构建，显式建模机器人刚体动力学，同时引入残差网络学习未建模的接触力和耗散力矩：

$$M(q_t) \ddot{q}_t + C(q_t, \dot{q}_t) + G(q_t) = B\tau_t + J^\top F_t^e + \tau_t^d$$

其中 $M$ 为质量矩阵，$C$ 为科里奥利力项，$G$ 为重力项，$B\tau_t$ 为驱动力矩，$J^\top F_t^e$ 为接触力项，$\tau_t^d$ 为耗散力矩项。残差网络 $\tau_\phi(s_t, a_t)$ 近似未知的外部力矩：

$$\tau_\phi(s_t, a_t) \approx J^\top F_t^e + \tau_t^d$$

世界模型基于 Brax 的可微分刚体物理原语实现，将残差网络预测的外部力矩注入可微分的物理步进中，实现端到端的前向预测。训练采用离线方式：在 SAC 预训练过程中将所有 transition 数据记录到磁盘，策略收敛后从这些离线数据中训练世界模型。损失函数为多步自回归对角高斯负对数似然（NLL）：

$$\mathcal{L}_{\phi} = \frac{1}{BH} \sum_{b=1}^{B} \sum_{t=0}^{H-1} \left[ \left( \widehat{s}_{b, t+1}^p - s_{b, t+1}^p \right)^2 \odot \exp\left( -\log \sigma_{b, t}^2 \right) + \log \sigma_{b, t}^2 \right]$$

其中 $B$ 为批次大小，$H$ 为自回归预测步长，$\widehat{s}_{b, t+1}^p$ 为预测的下一步特权状态，$\sigma_{b, t}^2$ 为学习的异方差预测方差。该损失同时优化状态预测精度和不确定性估计：对于已见状态，模型学习输出小方差；对于未见状态，模型输出大方差，从而为后续微调提供可靠的不确定性指示。

### 策略与世界模型联合微调

微调阶段的核心设计是将安全数据收集与充分探索解耦。在目标环境中，策略仅执行确定性动作（使用 actor 输出的均值），避免随机探索带来的安全风险。收集到的真实环境数据用于微调世界模型，使其适应新环境动力学。随后，在世界模型内部使用 SAC 的随机策略进行 rollout 生成合成数据，利用这些数据更新 actor-critic 网络。

世界模型内的 rollout 采用安全重置机制，当状态超出物理界限时自动终止：

$$\text{terminate if } \{h_t, |v|, |\omega|, |\phi|, |\theta|, q_j, \dot{q}_j\} \notin \text{Bounds}$$

其中 $h_t$ 为基座高度，$v$ 和 $\omega$ 为线速度和角速度，$\phi$ 和 $\theta$ 为躯干横滚和俯仰角，$q_j$ 和 $\dot{q}_j$ 为关节位置和速度。该机制防止模型错误累积导致的不安全状态传播，确保合成数据的质量。

模型预测的期望回报定义为：

$$J_{\phi}^{R}(\pi_{\theta}) = \mathbb{E} \left[ \sum_{t=0}^{\infty} \gamma^t r_{t+1} \middle| s_0 \sim \mu, a_t \sim \pi_{\theta}(\cdot | s_t), (s_{t+1}, r_{t+1}) \sim \mathbb{P}_{\phi}(\cdot | s_t, a_t) \right]$$

其中 $\mathbb{P}_{\phi}$ 为物理信息世界模型的转移概率。微调采用迭代流程：每收集 $T_{ep}$ 步真实数据后，在世界模型上执行多轮训练，随后进行策略更新，循环往复直至收敛。



## 实验与关键发现

### 预训练性能：SAC大规模并行收敛

LIFT的预训练阶段采用高UTD（Update-To-Data ratio）和大批量更新的SAC，在MuJoCo Playground中的六项人形机器人任务上进行了评估。如Figure 7所示，LIFT（红色）在三种机器人构型（T1LowDim、T1、G1）的粗糙地形和平面地形任务上，均取得了与PPO（橙色）和FastTD3（蓝色）相当或更高的评估回报，且在粗糙地形上达到峰值回报的速度更快。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/011_Figure_7.jpg]]
*Figure 7: Pretraining performance comparison of LIFT (red), PPO (orange), and FastTD3 (blue) across six humanoid tasks (top row: rough terrain for the three robot configurations; bottom row: flat terrain for the three robot configurations). Results show the mean over 8 random seeds*

这一性能提升的关键在于超参数调优：在Booster T1低维运动任务上，将UTD从1提升至10显著改善了样本效率；最终将收敛时间从约7小时压缩至约0.5小时（单张NVIDIA RTX 4090 GPU）。Table 1列出了不同环境下的具体配置，其中并行环境数从1000到4096不等，批次大小最高达16384，梯度更新步数与环境步数之比（即UTD）在部分配置中达到20。此外，预训练得到的SAC策略可在户外环境中zero-shot部署至真实Booster T1人形机器人，验证了其策略的鲁棒性。

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/027_Table_1.jpg]]
*Table 1: LIFT Hyperparameter Configurations for MuJoCo Playground Environments*

### 微调主结果：LIFT全面优于基线

在Booster T1的sim-to-sim微调任务中，LIFT在四个目标速度（0.6、1.0、1.2、1.5 m/s）下均稳定收敛并精确跟踪目标速度，身体振荡显著减少（Figure 2）。相比之下，所有基线方法均表现出不同程度的失败：

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/002_Figure_2.jpg]]
*Figure 2: Results of finetuning Booster T1 robot with varying target speeds. The black dashed line represents the target velocity for each task. Results are averaged over 8 random seeds*

- **SAC**：不使用显式探索噪声，快速发散且无法恢复。
- **PPO**：初期表现尚可，但逐渐退化并最终崩溃。
- **FastTD3**：出现剧烈振荡，未能收敛。
- **SSRL**：在较高目标速度（1.2、1.5 m/s）下无法达到目标速度，且不收敛。

在Unitree G1的微调任务中（Figure 15），LIFT同样展现出优势：在0.6 m/s目标速度下，身体振荡大幅减少；在1.5 m/s下，策略从初始的不稳定运动成功过渡到稳定的站立行走步态（Figure 14展示了微调前后的步态对比），而基线方法性能差或发散。

真实世界微调实验（Figure 3、Figure 8）进一步验证了LIFT的有效性：在3个随机种子下，LIFT持续提升评估回报、前向速度跟踪和角速度跟踪表现，同时降低了动作速率惩罚项。需要注意的是，速度跟踪误差可能来源于机载IMU加速度计对基座速度的噪声估计。

### 消融研究：预训练与物理信息世界模型缺一不可

**预训练消融**（Figure 4，Booster T1目标速度1.5 m/s）：

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/005_Figure_4.jpg]]
*Figure 4: Ablation of the pretraining on Booster T1 (target forward speed = 1.5 m/s). Results are averaged over 8 random seeds*

- **完整LIFT**：在$4 \times 10^4$环境步内收敛，成功跟踪目标速度。
- **去除世界模型预训练**：方法最终仍能收敛，但训练速度明显变慢，表明世界模型预训练对样本效率有显著贡献。
- **去除大规模SAC预训练**：策略陷入局部极差，完全无法收敛。这表明大规模SAC预训练提供的良好初始化是避免劣质局部最优的关键。

**物理信息世界模型消融**（Figure 5，Booster T1目标速度1.5 m/s）：

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/009_Figure_5.jpg]]
*Figure 5: Ablation of Physics informed World Model on Booster T1 (target speed = 1.5 m/s). Results are averaged over 8 random seeds*

- 将LIFT的物理信息世界模型替换为**MBPO**（Janner et al., 2019）的纯神经网络集成世界模型后，世界模型的MSE显著升高，策略的episode return始终接近零，完全无法收敛。这一结果直接证明了物理先验（拉格朗日动力学与残差网络）对世界模型预测精度的决定性作用。

**超参数敏感性分析**：

- **UTD与批次大小**（Figure 9）：增大UTD比例和批次大小可加速预训练收敛；增大缓冲区大小可提升学习速度，但会消耗更多GPU内存。
- **熵系数$\alpha$与自回归损失步长**（Figure 10）：较大的$\alpha$值会降低微调稳定性并导致最终前向速度下降，使用预训练阶段的$\alpha$值或更小的$\alpha$可获得更稳定的学习。自回归预测步长方面，horizon=1有时无法达到目标速度，而horizon=2和4可确保稳定收敛，表明多步自回归预测对世界模型训练和策略微调的稳定性至关重要。

### 失败模式与局限

1. **世界模型依赖**：微调流程依赖物理信息世界模型的准确性，在高度动态或接触密集的新环境中，模型偏差可能影响性能。MBPO消融实验已证实，世界模型预测误差的显著升高直接导致策略崩溃。

2. **真实世界部署的安全边界**：真实世界微调需人工安全干预和重置，缺乏自主故障恢复机制。LIFT通过安全重置条件（基于物理界限的终止判断）在世界模型内过滤不安全状态，但这一机制尚未延伸至真实环境的自动故障处理。

3. **感知模态限制**：当前系统仅使用本体感知状态，未扩展到视觉等复杂感知输入，限制了其在需要环境感知的任务上的适用性。

4. **流水线复杂度**：异步数据收集与训练、对象交互等高级任务尚未集成，当前流水线复杂度有限。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/010_Figure_6.jpg]]
*Figure 6: Comparison of PPO and SAC in a preliminary fine-tuning experiment with the BoosterT1 robot, run for 48 hours on a single Brax simulation. The left figure shows the evaluation episode return, and the right figure shows the body’s linear velocity along the x-axis. Curves represent the average over 8 random seeds, with evaluation performed in 128 parallel environments. PPO performance is highly sensitive to the initial action standard deviation (std). Replacing the PPO actor with a SAC-style actor that outputs both the mean and standard deviation improves stability, although SAC still requires fewer samples to achieve the same performance*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/028_Table_2.jpg]]
*Table 2: Finetune Hyperparameter of LIFT*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/029_Table_3.jpg]]
*Table 3: Reward Function Components and Weights*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/030_Table_4.jpg]]
*Table 4: Default reward terms (Note: U [ a , b ] denotes uniform distribution over [a, b])*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/031_Table_5.jpg]]
*Table 5: Domain randomization parameters (Note: U [ a , b ] denotes uniform distribution over [a, b], $\pm$ U ( c ) denotes uniform distribution over [ - c , c ] )*

![[assets/figures/papers/paper_list_l8_https_openreview_net_forum_id_NEOTsyyYH7/figures/032_Table_6.jpg]]
*Table 6: Finetune reward terms (Note: many terms disabled for sim-to-sim transfer)*



## 定位与知识库关联

### 核心瓶颈与设计动机

当前人形机器人控制面临一个关键矛盾：**on-policy RL（如PPO）虽能借助大规模并行仿真快速训练，但样本效率低，且在新环境中随机探索风险高，难以安全微调**；**off-policy RL（如SAC）和model-based RL（如MBPO）虽可复用历史数据，但在人形机器人大规模预训练中稳定性差、耗时长**，导致预训练到高效微调之间存在明显差距。

LIFT的设计正是围绕这一瓶颈展开，其核心因果调节变量是：**在微调阶段将随机探索完全限制在物理信息世界模型内，真实环境仅执行确定性策略**，从而解耦安全数据收集与充分探索，同时利用大规模SAC预训练为世界模型和策略提供良好初始化。

### 与基线方法的关系

**PPO**（Schulman et al., 2017）是当前人形机器人预训练的主流on-policy算法，凭借大规模并行仿真可实现快速收敛。然而，LIFT的实验表明（Figure 2），PPO在微调阶段性能逐渐退化并最终崩溃——其on-policy特性要求每次更新后重新采集数据，在新环境中样本效率低下，且随机探索带来的动作抖动在真实机器人上存在安全隐患。附录Figure 6进一步揭示，PPO的微调性能高度依赖初始动作标准差的选择，而SAC的随机策略天然兼容模型内探索，收敛更快且更稳定。

**FastTD3**（Seo et al., 2025）作为高效的off-policy baseline，支持大规模并行训练，但在微调中表现出剧烈振荡且无法收敛（Figure 2）。这表明单纯的off-policy算法改进不足以解决微调中的稳定性问题，必须配合世界模型内的安全探索机制。

**SAC**（Haarnoja et al., 2018b）是LIFT的基础算法组件。LIFT的关键创新在于：通过高UTD（Update-To-Data）比率和大批量更新的JAX实现，使SAC在GPU上获得类似PPO的并行收敛速度，同时保留其随机策略特性以兼容模型内探索。实验表明，去除大规模SAC预训练后策略陷入局部极差完全无法收敛（Figure 4），证明SAC预训练为后续微调提供了不可或缺的良好初始化。

**SSRL**（Levy et al., 2024）提出了物理信息世界模型的概念，将拉格朗日动力学与残差网络结合，成功应用于四足机器人从零训练。LIFT继承了这一世界模型结构，但将其从在线训练改为离线预训练，并扩展到人形机器人的预训练-微调范式。实验显示，SSRL在人类机器人高速跟踪任务上无法收敛（Figure 2），说明从零训练对人形机器人不安全且效率不足。

**MBPO**（Janner et al., 2019）是经典的基于黑盒神经网络世界模型的MBRL方法。LIFT的消融实验（Figure 5）表明，将物理信息世界模型替换为MBPO的纯神经网络集成模型后，世界模型MSE显著升高，策略回报接近零。这验证了物理先验在人形机器人高维动力学建模中的关键作用——纯黑盒模型难以准确预测接触力和耗散力矩等未建模效应。

### 方法适用边界

LIFT的微调流程依赖物理信息世界模型的预测精度。在高度动态或接触密集的新环境中，若残差网络无法充分捕捉未建模效应（如复杂地形下的足地接触），模型偏差可能影响策略优化质量。当前系统仅使用本体感知状态（关节位置、速度、IMU等），未扩展到视觉等复杂感知输入，因此不适用于需要环境感知的任务（如视觉导航、物体操作）。

真实世界微调阶段（Figure 3、Figure 8）需人工安全干预和重置，系统缺乏自主故障恢复机制。在30k环境步的真实微调中，前向速度跟踪误差可能来自机载IMU加速度计对基座速度的噪声估计，表明感知噪声是实际部署中的潜在瓶颈。

### 局限与开放问题

1. **安全自动化**：如何在真实世界微调中融入自动安全机制，例如不确定性感知探索（利用世界模型的预测方差判断状态安全性）或机器人辅助重置？当前系统依赖人工干预，限制了长时间自主适应的可行性。

2. **感知扩展**：如何将LIFT扩展到以视觉为中心的任务？这可能需要引入潜在世界模型来处理高维感知输入，但如何在潜在空间中保留物理先验仍是一个开放挑战。

3. **异步部署效率**：当前微调采用同步的数据收集-训练循环。异步数据收集与训练能否在不引入额外复杂性的前提下进一步提高实际部署效率？这涉及off-policy数据的陈旧性与世界模型更新频率之间的权衡。

4. **对象交互与复杂任务**：LIFT目前聚焦于运动控制任务。将其扩展到全身运动跟踪（Figure 16已展示初步能力）和对象交互等高级任务，需要研究世界模型对操作力学的建模能力以及安全探索机制的泛化性。



## 原文 PDF

![[paperPDFs/ICLR_2026/Towards_Bridging_the_Gap_between_Large_Scale_Pretraining_and_Efficient_Finetuning_for_Humanoid_Control.pdf]]
