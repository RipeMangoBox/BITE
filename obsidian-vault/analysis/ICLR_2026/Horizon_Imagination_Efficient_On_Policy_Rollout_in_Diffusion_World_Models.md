---
title: "Horizon Imagination: Efficient On-Policy Rollout in Diffusion World Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Horizon_Imagination_Efficient_On_Policy_Rollout_in_Diffusion_World_Models.pdf
project_link: null
code_link: https://github.com/leor-c/horizon-imagination
openreview_forum_id: Obefq4k8iG
aliases:
- HIH
- HIEPRDWM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过并行去噪与稳定动作采样解耦去噪预算和衰减周期，实现在降低计算预算的同时维持控制性能。"
primary_logic: "通过同时去噪多个未来观测并引入基于逆变换采样的稳定动作选择机制，Horizon Imagination 能够在子步预算（每帧少于一次去噪步）下保持控制性能，并在低到中等预算下取得优于序列生成的生成质量。"
claims:
- "Horizon Imagination denoises multiple future observations simultaneously, reducing sequential burden."
- "Stable action sampling mechanism reduces unnecessary action changes and stabilizes denoising process."
- "Novel Horizon schedule disentangles denoising budget from decay horizon, supporting fractional steps-per-frame budgets."
- "Replacing stable action sampling with naive sampling leads to substantial drop in control performance."
---

# Horizon Imagination: Efficient On-Policy Rollout in Diffusion World Models

> [!tip] 核心洞察
> 通过同时去噪多个未来观测并引入基于逆变换采样的稳定动作选择机制，Horizon Imagination 能够在子步预算（每帧少于一次去噪步）下保持控制性能，并在低到中等预算下取得优于序列生成的生成质量。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Horizon Imagination：扩散世界模型中高效的在线策略推演 |
| 英文题名 | Horizon Imagination: Efficient On-Policy Rollout in Diffusion World Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=Obefq4k8iG) · [GitHub](https://github.com/leor-c/horizon-imagination) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Horizon Imagination (HI) |
| Dataset | Atari 100K and Craftium, Craftium |

> [!tip] 效果简介
> - Atari 100K and Craftium 上，Episodic return 为 HI (ν=4, B=16)，对比 Autoregressive (ν=1, B=32)，变化 comparable performance, using half the denoising budget。
> - Craftium 上，FVD 为 HI parallel (ν=4, 8, 16) with B=2 to 128，对比 sequential (ν=1) or Pyramidal schedule，变化 parallel achieves lower (better) FVD under low to medium budgets; sub‑step budgets achieve competitive quality。

## 概要

**Horizon Imagination** 是一种面向扩散世界模型的高效在线策略推演方法，其核心动机在于解决扩散模型在强化学习想象（imagination）阶段的计算瓶颈：现有序列想象力要求逐帧串行去噪，每一步都需要完整的去噪预算，导致推理成本高昂，难以在实际控制任务中部署。

该方法通过三个关键设计突破上述瓶颈：

1. **并行去噪**：同时去噪多个未来观测，将序列生成中高度串行的计算负担转化为并行计算，大幅降低推理延迟。
2. **稳定动作采样**：基于逆变换采样的确定性动作选择机制，在去噪过程中保持动作一致性，抑制策略随机性引入的生成不稳定（见图 1）。
3. **Horizon 调度**：通过独立控制去噪预算 $B$ 和衰减周期 $\nu$，解耦了传统金字塔调度中两者相互绑定的约束，支持**子步预算**（每帧少于一次去噪步）下的高效生成（见图 2）。

在 Atari 100K 和 Craftium 基准上的实验表明，Horizon Imagination 在使用一半去噪预算（$\nu=4, B=16$）的条件下，控制性能与自回归基线（$\nu=1, B=32$）相当；在低到中等预算下，并行生成的 FVD 质量优于序列生成。消融实验进一步证实，稳定动作采样是维持控制性能的关键组件，替换为朴素采样会导致性能显著下降。

**方法定位**：Horizon Imagination 属于基于扩散世界模型的模型基强化学习（MBRL）框架，在想象力效率维度推进了扩散生成在在线控制中的应用边界。其核心贡献在于将扩散去噪的预算分配从“逐帧串行”重构为“跨帧并行+调度解耦”，为扩散世界模型的实时部署提供了可行路径。



### 扩散世界模型在强化学习中的效率瓶颈

基于模型的强化学习（MBRL）通过在想象中推演未来轨迹来训练策略，从而减少对真实环境交互的需求。近年来，扩散模型凭借其高质量的生成能力被引入世界模型构建中，用于生成未来的观测序列。然而，这一范式面临一个根本性的计算瓶颈：**扩散世界模型在生成高质量想象轨迹时计算成本高昂**。

具体而言，现有的序列想象力（sequential imagination）要求世界模型逐帧生成未来观测，每一帧都需要经历完整的去噪过程。这种逐帧串行的推理方式导致：
- 去噪步骤与生成帧数线性耦合，计算量随想象视界（horizon）增长而急剧膨胀；
- 推理过程高度串行，难以利用并行计算资源；
- 在实际控制部署中，高昂的推理延迟成为阻碍扩散世界模型落地的关键障碍。

### 现有方法的局限

当前扩散世界模型主要采用两类去噪调度策略：

**自回归基线**（ν=1, B=32）对每一帧独立执行完整的去噪过程，每帧消耗固定的去噪预算 B。这种方式虽然生成质量稳定，但计算效率最低。

**Pyramidal schedule**（Chen et al., 2024）通过在时间维度上分配递减的去噪预算来提升效率，但其衰减周期（decay horizon）与总去噪预算相互耦合。如 Figure 2 所示，当总预算增加时，Pyramidal schedule 的衰减周期会发生漂移，导致高预算下的生成质量反而严重退化（见 Figure 8）。这种耦合限制了预算调节的灵活性，使得该调度无法在保持质量的前提下自由降低计算开销。

### 核心动机与研究问题

上述分析揭示了两个关键缺口：

1. **去噪预算与衰减周期的耦合问题**：现有调度无法独立控制“花多少算力”和“看多远”，这阻碍了在子步预算（sub-step budget，即每帧平均少于一次去噪步）下的高效生成。

2. **策略诱导的生成不稳定性**：在并行去噪过程中，若从策略分布中随机采样动作，去噪步骤间的动作波动会导致生成序列出现严重的不稳定性（见 Figure 1）。这种不稳定性不仅损害生成质量，更会误导策略训练。

基于此，本文提出 **Horizon Imagination（HI）**，旨在回答以下核心问题：**能否在显著降低去噪预算的同时，维持扩散世界模型的控制性能和生成质量？** 这一问题的解决将直接推动扩散世界模型在资源受限场景中的实际部署。



## 核心方法与创新机理

Horizon Imagination 的核心创新在于将扩散世界模型的想象力过程从**串行逐帧去噪**转变为**并行多步去噪**，并通过两个关键机制——稳定动作采样和 Horizon schedule——解决了并行化带来的策略不稳定与预算-衰减耦合问题。以下从三个 changed slots 展开分析。

### 并行去噪策略：从串行到并行的范式转变

传统扩散世界模型在想象力阶段采用自回归基线（ν=1, B=32）：每生成一帧观测，需执行完整的去噪步数，生成 h 帧需要 h×B 次去噪，推理过程高度串行且计算密集。

Horizon Imagination 的核心转变在于**同时去噪多个未来观测**。在想象力过程中，去噪器 v_θ 以并行方式处理多个时间步的潜变量，即使近未来观测尚未完全去噪，远未来观测的去噪也已开始。这意味着去噪预算 B 不再与生成帧数 h 绑定，为子步预算（B < h）提供了可能。

这一转变的关键洞察是：扩散生成的质量并非严格依赖于每帧独立的完整去噪过程。通过让多个观测共享去噪步骤，可以在降低总计算量的同时维持生成质量。实验证据表明，在 ν=4, B=16 的配置下，Horizon Imagination 仅使用自回归基线一半的去噪预算，即可在 Atari 100K 和 Craftium 基准上维持相当的控制性能（Figure 4, Section 5.2.2）。

### 稳定动作采样：消除策略诱导的去噪不稳定

并行去噪引入了一个新的挑战：在去噪过程中，策略需要为每个未来时间步提供动作条件，但去噪早期的观测仍处于高噪声状态，策略输出的动作分布会随去噪进程剧烈变化。朴素的重采样策略——在每个去噪步独立采样动作——会导致动作频繁切换，破坏去噪过程的稳定性（Figure 1 展示了 Craftium/ChopTree-v0 环境下的生成崩溃现象）。

稳定动作采样的解决方案基于逆变换采样的确定性映射。给定策略分布 π 和一个固定的排列 ρ，算法通过单个均匀样本 ω 在去噪过程中一致地选择动作：

$$\mathbf{a}(\pi, \omega) = \begin{cases} \rho(i) & \text{for the smallest } i \text{ with } \omega_i < \alpha_i(\pi), \\ \rho(N) & \text{if no such } i \text{ exists} \end{cases}$$

这一机制的理论保证在于：当策略分布从 p 演变为 q 时，动作变化的期望次数被总变分距离 δ(p, q) 所下界。实证分析（Figure 3）表明，稳定采样在 16 步去噪过程中平均至多产生一次动作变化，接近理论下界，而朴素采样则在大多数步骤中改变动作，总体变化超过一半。

消融实验（Figure 5, Section 5.2.3）提供了决定性证据：将稳定动作采样替换为朴素采样导致控制性能大幅下降，在 Atari Boxing 和 Gopher 环境中尤为显著，性能曲线出现明显崩溃。这证实了动作稳定性是并行想象力成功的关键因素。

### Horizon Schedule：解耦去噪预算与衰减周期

现有并行去噪方案（如 Diffusion Forcing 的 Pyramidal schedule, Chen et al., 2024）将去噪预算 B 和衰减周期 ν 耦合在一起：当预算增加时，衰减周期会随之漂移，导致远未来观测获得过多去噪步骤，反而损害生成质量（Figure 8 显示 Pyramidal schedule 下生成质量随预算增加而急剧恶化）。

Horizon schedule 通过独立控制两个参数解决了这一问题。schedule 矩阵 K 的条目定义为：

$$K_{i,j} = \mathrm{clamp}(\kappa(j-1, i-1), 0, 1)$$

其中 $\kappa(t, b) = -t/\nu + (b/B)(1 + (h-1)/\nu)$。这一线性调度确保衰减周期 ν 在不同预算 B 下保持恒定（Figure 2 对比了两种 schedule 的行为），使得预算可以独立调节而不影响去噪质量的衰减模式。

这一解耦的实际意义在于支持**子步预算**：当 B < h 时，系统以少于每帧一步的预算运行，这在 Pyramidal schedule 中是无法实现的。实验表明（Figure 6, Section 5.3），在低到中等预算下，Horizon schedule 的并行配置（ν=4, 8, 16）在 FVD 指标上优于串行基线，且子步预算配置能达到与满预算基线相当的质量。

### 创新总结

三个 changed slots 构成了一个相互依赖的创新体系：并行去噪提供了效率提升的可能性，稳定动作采样解决了并行化引入的策略不稳定问题，Horizon schedule 则解耦了预算与衰减周期，使子步预算成为可行。消融实验证实，缺少任一机制都会导致性能退化——替换稳定采样导致控制崩溃，使用 Pyramidal schedule 替代 Horizon schedule 则使生成质量随预算增加而恶化。



![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Obefq4k8iG/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of the Pyramidal schedule (Chen et al., 2024) and the proposed Horizon schedule (transposed). Horizon fixes the decay horizon ( $\nu$ \ : = \ : 3 ) yielding consistent schedules across budgets, whereas in the Pyramidal schedule the decay horizon drifts with budget, as the two are entangled, leading to degraded generation quality at higher budgets*

Horizon Imagination (HI) 是一个面向扩散世界模型的在线策略推演框架，其核心设计目标是在显著降低去噪计算预算的同时维持控制性能。框架由五个协同模块构成：**表征模型**、**去噪器（因果 DiT）**、**奖励-终止预测器**、**稳定动作采样机制**、以及**Horizon 调度器**，整体流程围绕“并行多步想象”展开。

### 数据流与模块关系

1. **表征模型**（autoencoder）将高维观测 $o_t$ 编码为有界潜变量 $z_t^1 \in [-1,1]^{d}$，并在需要时解码回像素空间用于可视化和奖励预测。编码器与解码器的具体架构见 Table 1 和 Table 2。
2. **去噪器** $v_\theta$ 是一个因果 DiT（Diffusion Transformer），接收带噪潜变量序列 $\{z_{1}^{\tau_1}, \ldots, z_{t}^{\tau_t}\}$ 及历史动作 $a_{<t}$，预测干净潜变量与噪声潜变量之差 $z_t^1 - z_t^0$。训练时使用 $h$ 步轨迹片段，损失函数为：
   $$L(\theta) = \frac{1}{h} \sum_{t=1}^{h} \mathbb{E}_{z^0, z^1, \tau} \| v_\theta(z_1^{\tau_1}, \ldots, z_t^{\tau_t}, a_{<t}, \tau_{\leq t}) - (z_t^1 - z_t^0) \|^2$$
   其中 $z_t^{\tau_t} = \tau_t z_t^1 + (1-\tau_t) z_t^0$ 为噪声插值结果（Section 4.1, Eq. 1）。
3. **奖励-终止预测器**是一个轻量级 CNN+LSTM 网络，从潜变量轨迹中预测奖励 $r_t$ 和终止信号 $d_t$，为策略训练提供模拟反馈（Table 4）。
4. **Actor-Critic 控制器**包含独立的策略网络 $\pi$ 和价值网络 $V^\pi$，通过 REINFORCE 算法结合优势缩放和熵正则化进行训练（Section 4.3）。

### 并行想象与稳定采样

HI 的核心创新在于**并行去噪**：在推演过程中，去噪器同时处理多个未来观测，而非逐个串行生成。这带来了一个关键挑战——远未来观测在近未来观测尚未完全去噪时即被处理，导致策略在去噪过程中接收到的上下文噪声水平不断变化。

为解决这一问题，HI 在每次去噪步前查询策略，获得各时间步的动作分布，并通过**稳定动作采样**机制将策略分布映射为确定性动作：
$$\mathbf{a}(\pi, \omega) = \begin{cases} \rho(i) & \text{for the smallest } i \text{ with } \omega_i < \alpha_i(\pi), \\ \rho(N) & \text{if no such } i \text{ exists} \end{cases}$$
其中 $\omega \sim U[0,1]^N$ 为固定随机样本，$\rho$ 为固定排列，$\alpha_i(\pi)$ 为策略分布的累积概率。该机制确保在去噪过程中动作变化次数接近理论下界，实证表明平均仅约一次变化，而朴素采样则导致半数以上步骤发生动作改变（Figure 3）。

### Horizon 调度器

HI 引入的 **Horizon 调度器** $K$ 定义了每个去噪步 $i$ 对每个观测 $j$ 的去噪时间 $\tau$：
$$K_{i,j} = \mathrm{clamp}(\kappa(j-1, i-1), 0, 1), \quad \kappa(t, b) = -\frac{t}{\nu} + \frac{b}{B}\left(1 + \frac{h-1}{\nu}\right)$$
其中 $B$ 为去噪预算，$\nu$ 为衰减周期。该调度器的关键优势在于**解耦去噪预算与衰减周期**，支持子步预算（$B < h$，即每帧少于一次去噪步），而先前的 Pyramidal schedule（Chen et al., 2024）中两者相互纠缠，导致高预算下生成质量退化（Figure 2）。

### 训练与推演流程

训练阶段，世界模型（去噪器 + 奖励-终止预测器）从经验回放池中采样轨迹片段进行监督学习。推演阶段，HI 从当前观测的干净潜变量 $z_{\leq k}^1$ 出发，并行初始化 $h$ 步噪声潜变量，按 Horizon 调度器定义的 $\tau$ 序列进行 $B$ 步去噪，每一步通过稳定采样获取策略动作，最终生成想象轨迹用于 Actor-Critic 的策略更新。

整体框架的模块关系可概括为：表征模型提供潜空间接口，去噪器与 Horizon 调度器实现高效并行想象，稳定采样机制抑制策略噪声，奖励-终止预测器提供模拟反馈，Actor-Critic 控制器利用想象轨迹进行策略优化。



Horizon Imagination 的核心由三个相互协同的模块构成：并行去噪器、稳定动作采样机制以及 Horizon 调度策略。它们共同解决了扩散世界模型在想象力过程中计算串行化与策略诱导不稳定两大瓶颈。

### 并行去噪器

世界模型由一个基于因果 DiT 架构的去噪器 $v_{\theta}$ 和一个轻量级的奖励-终止预测器（CNN+LSTM）组成。去噪器的训练目标是最小化以下 1-Rectified Flow 回归损失：

$$L(\theta) = \frac{1}{h} \sum_{t=1}^{h} \mathbb{E}_{\mathbf{z}^{0},\mathbf{z}^{1},\tau} \| v_{\theta}(\mathbf{z}_{1}^{\tau_{1}}, \ldots, \mathbf{z}_{t}^{\tau_{t}}, \mathbf{a}_{<t}, \tau_{\leq t}) - (\mathbf{z}_{t}^{1} - \mathbf{z}_{t}^{0}) \|^{2}$$

其中 $\mathbf{z}_{t}^{1}$ 是由自编码器编码的干净潜变量，$\mathbf{z}_{t}^{0}$ 是从先验采样的噪声，$\mathbf{z}_{t}^{\tau_{t}} = \tau_{t}\mathbf{z}_{t}^{1} + (1-\tau_{t})\mathbf{z}_{t}^{0}$ 为两者的线性插值。去噪器以因果方式接收所有过去帧的噪声潜变量和动作序列，预测当前帧干净潜变量与噪声潜变量之差，从而学习环境动态的生成模型。

### 稳定动作采样

在并行去噪过程中，策略需要在每个去噪步为每个未来时间步提供动作。若直接对策略分布进行随机采样，去噪过程中动作频繁变化会导致生成序列崩溃（Figure 1）。稳定动作采样通过逆变换采样的思想，将随机性外移至一个固定的均匀样本 $\omega$，使动作选择成为确定性映射：

$$\mathbf{a}(\pi, \omega) = \begin{cases} \rho(i) & \text{for the smallest } i \text{ with } \omega_i < \alpha_i(\pi), \\ \rho(N) & \text{if no such } i \text{ exists} \end{cases}$$

其中 $\pi$ 为策略输出的类别分布，$\rho$ 为固定排列，$\alpha_i(\pi)$ 为累积概率。该机制的理论保证是：当策略分布从 $\mathbf{p}$ 演变为 $\mathbf{q}$ 时，动作发生变化的概率下界为总变分距离 $\delta(\mathbf{p}, \mathbf{q})$，而稳定采样实际产生的动作变化次数紧贴此下界（Figure 3a），远优于朴素采样（Figure 3b）。

### Horizon 调度

Horizon 调度通过一个去噪时间矩阵 $K$ 独立控制两个关键参数：去噪预算 $B$（总去噪步数）和衰减周期 $\nu$（未来观测噪声沿时间轴衰减的速率）。矩阵条目定义为：

$$K_{i,j} = \mathrm{clamp}(\kappa(j-1, i-1), 0, 1)$$

其中 $\kappa(t, b) = -t/\nu + (b/B)(1 + (h-1)/\nu)$ 定义了一族斜率为 $-1/\nu$ 的直线。与 Pyramidal 调度（Chen et al., 2024）的根本区别在于：Horizon 调度将衰减周期 $\nu$ 固定，使预算 $B$ 的变化仅影响去噪时间线的密度而不改变衰减模式（Figure 2）。这支持了子步预算（$B < h$，即每帧少于一次去噪步），并在不同预算下保持一致的生成质量，而 Pyramidal 调度随预算增加会因衰减周期漂移导致质量急剧退化（Figure 8）。

### 策略训练目标

Actor-Critic 控制器使用 REINFORCE 算法训练，策略目标在想象力轨迹的每个噪声水平上累积：

$$A_{k+t} \log \pi(\mathbf{a}_{k+t}^{\tau_t} | \ldots) + \eta \mathcal{H}(\pi_{k+t}^{\tau_t})$$

优势函数采用收益分位数范围进行缩放以稳定训练：

$$A_{t} = \mathrm{sg}\left( \frac{G_t - \mathrm{symexp}(\hat{V}_t^{\pi})}{\max(1, S)} \right)$$

其中 $S$ 为收益分位数范围，$\mathrm{symexp}$ 为对称指数变换。



## 实验与关键发现

### 核心瓶颈与实验动机

扩散世界模型在强化学习中面临一个关键矛盾：生成高质量的想象轨迹需要大量去噪步骤，而现有序列想象力（sequential imagination）要求每帧独立执行完整的去噪过程，导致推理高度串行且计算密集。Horizon Imagination 的核心目标是在降低计算预算的同时维持控制性能，其实验设计围绕三个因果调节变量展开：并行去噪策略、稳定动作采样机制、以及解耦去噪预算与衰减周期的 Horizon schedule。

### 控制性能：子步预算下的策略训练

**Figure 4** 展示了 Actor-Critic 训练过程中平均 episodic return 曲线。实验对比了三组配置：自回归基线（ν=1, B=32）、HI 并行配置（ν=4, B=16）和（ν=4, B=32）。在四个 Craftium 环境（SmallRoom、Room、Speleo、ChopTree）和四个 Atari 游戏（Boxing、Breakout、Gopher、Seaquest）上，ν=4 的两组配置均保持了与自回归基线相当的控制性能。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Obefq4k8iG/figures/005_Figure_4.jpg]]
*Figure 4: Actor-Critic Performance. Average episodic return curves of key baselines during training. Each baseline is evaluated over 5 seeds. Curves show the mean and standard deviation, smoothed by a moving average (window size 15). A dashed horizontal line denotes Atari human-level performance*

关键结论是：**HI 在子步预算 B=16（每帧平均 0.5 步去噪）下即可维持完整性能**，仅需自回归基线一半的去噪计算量。这一结果直接验证了并行去噪策略的有效性——同时去噪多个未来观测并未损害策略学习所需的轨迹质量。

### 稳定动作采样的决定性作用

**Figure 5** 的消融实验揭示了稳定动作采样机制的因果重要性。将稳定采样替换为朴素采样（每次去噪步独立从策略分布中采样动作）后，控制性能出现显著下降。在 Atari Boxing 和 Gopher 上，朴素采样的性能几乎完全崩溃；在 Craftium 的 ChopTree 和 Speleo 环境中，return 曲线也明显低于稳定采样配置。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Obefq4k8iG/figures/006_Figure_5.jpg]]
*Figure 5: Actor–critic performance comparison between the proposed stable action sampling method and the naive baseline. Each baseline is evaluated over 5 seeds. Curves show the mean and standard deviation, smoothed by a moving average (window size 15). A dashed horizontal line denotes Atari human-level performance*

这一现象的根本原因在于：去噪过程中策略分布随观测逐步清晰化而演变，朴素采样在每个去噪步引入独立的随机扰动，导致动作序列频繁波动（**Figure 3b** 显示朴素采样在 16 步中平均改变超过半数动作），进而破坏去噪过程的稳定性。相比之下，稳定采样通过逆变换采样将动作选择与固定的均匀样本 ω 绑定，确保仅在策略分布发生实质性偏移时才改变动作——实证结果显示平均最多一次动作变化（**Figure 3a**），接近全变差下界 δ(p, q)。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Obefq4k8iG/figures/003_Figure_3.jpg]]
*Figure 3: (a) Distributions of the average number of action changes, in $\delta ( \pmb { p } , \pmb { q }$ ) units, for various N values. Minimum, mean, and maximum are indicated

### 世界模型生成质量：并行 vs 序列

**Figure 6** 以 FVD 和 MSE 为指标，系统评估了不同去噪预算 B（2 至 128）下世界模型的生成质量。在低到中等预算区间（B ≤ 32），并行配置（ν=4, 8, 16）的 FVD 明显优于序列基线（ν=1）。这表明**并行去噪在计算受限场景下具有生成质量优势**——同时为多个未来帧分配去噪步骤，比逐帧集中去噪更能有效利用有限预算。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Obefq4k8iG/figures/007_Figure_6.jpg]]
*Figure 6: World model generation quality versus denoising steps budget. Each point shows the average FVD/MSE over 512 sampled 33-frame segments, where the first frame was given as context and the last 32 were generated conditioned on the recorded actions. A dashed vertical line indicates the transition out of sub-step budgets*

值得注意的是，当预算增至 B=128 时，MSE 出现上升趋势，尽管 FVD 持续改善。这揭示了扩散模型生成中的一个微妙现象：更高的去噪预算可能使生成序列在感知质量上更优（FVD 更低），但同时也可能偏离真实轨迹更远（MSE 更高）。这一漂移效应在 Atari 游戏上同样存在（**Figure 7**），但 FVD/MSE 的绝对值更低，表明 Atari 环境的视觉动态相对简单。

### Horizon schedule 与 Pyramidal schedule 的对比

**Figure 8** 展示了使用 Pyramidal schedule（Chen et al., 2024）时的生成质量。与 Horizon schedule 形成鲜明对比的是，Pyramidal schedule 下生成质量随预算增加而急剧恶化——因为其衰减周期与去噪预算耦合，高预算导致衰减周期异常延长，破坏了去噪调度的一致性。Horizon schedule 通过固定衰减周期 ν 并独立控制预算 B（**Eq. 3**），在所有预算水平下保持稳定的调度结构（**Figure 2**），这是其在高预算下仍能维持生成质量的关键设计。

![[assets/figures/papers/paper_list_l15_https_openreview_net_forum_id_Obefq4k8iG/figures/019_Figure_8.jpg]]
*Figure 8: World model generation quality versus denoising steps budget when using the Pyramidal schedule of Chen et al. (2024). Each point shows the average FVD/MSE over 512 sampled 33-frame segments, where the first frame was given as context and the last 32 were generated conditioned on the recorded actions. A dashed vertical line indicates the transition out of sub-step budgets*

### 失败模式与已知局限

1. **Breakout 环境的性能不足**：在 Atari Breakout 上，原始 HI 方法的性能欠佳，需要引入解耦 Actor 变体。该变体尚未在完整基准上评估，其泛化性有待验证。

2. **极高预算下的 MSE 漂移**：当 B ≥ 128 时，生成序列与真实轨迹的像素级偏差增大。虽然感知质量（FVD）仍在改善，但这对需要精确状态重建的下游任务可能构成风险。

3. **连续动作空间的未验证性**：稳定动作采样机制基于离散动作空间的逆变换采样设计，其在连续动作空间的扩展方案和性能表现尚未经实验检验。

### 待验证的开放问题

- 解耦 Actor 变体在更多环境（尤其是需要长程信用分配的任务）中是否能保持优势？
- 稳定动作采样在连续控制任务（如 MuJoCo、DMControl）中的可行替代方案是什么？
- Horizon Imagination 在更大规模的视频扩散世界模型（如基于 3D VAE 的潜空间模型）中，并行去噪的效率优势是否依然成立？



## 定位与知识库关联

### 问题域定位

Horizon Imagination 处于**扩散世界模型 × 在线策略强化学习**的交叉地带。其核心瓶颈是：扩散模型在生成高质量想象轨迹时，传统的序列去噪范式导致推理过程高度串行且计算密集，使得在真实控制环境中部署时成本不可接受。该工作并非提出新的扩散架构或 RL 算法，而是通过**推理过程的系统重构**——并行去噪、稳定动作采样、解耦调度——在计算预算与控制性能之间建立新的帕累托前沿。

### 与已有方法的关系

**自回归基线**（ν=1, B=32）是该文设定的序列去噪参照系。在此配置下，每帧观测分配固定的去噪步数，未来观测必须等待近邻观测先完成去噪，形成严格的时序依赖链。Horizon Imagination 直接挑战了这一范式，证明通过并行去噪可以在仅一半预算（B=16）下维持控制性能。

**Diffusion Forcing 的 Pyramidal schedule**（Chen et al., 2024）是该文在调度策略上的直接前驱与对比对象。Pyramidal schedule 的核心缺陷在于去噪预算 B 与衰减周期 ν 相互耦合：预算增大时，衰减周期会漂移，导致远未来观测获得过多的去噪预算，反而使生成质量恶化（见 Figure 8）。Horizon schedule 通过独立的线性调度函数 κ(t, b) = -t/ν + (b/B)(1 + (h-1)/ν) 将两者解耦，使得 ν 在任意预算下保持恒定，这是该方法在低到中等预算下优于 Pyramidal schedule 的结构性原因。

在**扩散世界模型**的更大谱系中，该工作继承了将扩散模型作为环境动力学生成器的思路，但区别于那些关注扩散架构本身（如 DiT 缩放、视频扩散先验）的工作。其贡献集中在推理效率层面，因此在方法上可与更强大的扩散骨干网络正交组合。

### 适用边界与局限

1. **离散动作空间的限制**：稳定动作采样机制（Eq. 2）基于逆变换采样，依赖离散动作的概率质量函数排序。其理论性质（动作变化次数接近全变差下界 δ(p, q)）仅在离散域内得到证明。连续动作空间的扩展方案尚未给出，能否保持相近的稳定性与生成质量需要实验验证。

2. **高预算下的 MSE 漂移**：在极高去噪预算（≥128）下，世界模型的 MSE 可能上升，生成序列与真实轨迹的偏差加大。这意味着该方法在追求极高感知质量时可能牺牲状态空间精度，对需要精确状态追踪的下游任务构成风险。

3. **环境特异性退化**：在 Atari Breakout 环境中，原始方法性能欠佳，需引入解耦 Actor 变体。该变体尚未在完整基准上评估，其泛化性存疑。

### 未解决的开放问题

- 稳定动作采样在连续动作空间中是否能保持相近的稳定性与生成质量？若不能，是否存在替代的平滑机制？
- 解耦 Actor 变体在更多环境及更大规模世界模型中的泛化表现如何？其引入是否暗示当前策略训练目标与并行去噪过程之间存在未建模的冲突？
- Horizon Imagination 在更大规模扩散世界模型（如视频扩散模型）中的效率和性能是否依然成立？当前实验限于相对紧凑的 Transformer 去噪器，向数十亿参数模型迁移时，并行去噪的显存与通信开销可能成为新的瓶颈。

### 证据强度评估

核心主张（并行去噪降低计算成本、稳定采样防止性能崩塌、Horizon schedule 解耦预算与衰减周期）均有**高强度证据**支撑（置信度 ≥0.95），来自受控消融实验和多环境验证。但关于该方法在更广泛条件下的适用性（连续动作、更大模型、更多环境）的证据**目前缺失**，相关结论需标注为推测性判断。



## 原文 PDF

![[paperPDFs/ICLR_2026/Horizon_Imagination_Efficient_On_Policy_Rollout_in_Diffusion_World_Models.pdf]]
