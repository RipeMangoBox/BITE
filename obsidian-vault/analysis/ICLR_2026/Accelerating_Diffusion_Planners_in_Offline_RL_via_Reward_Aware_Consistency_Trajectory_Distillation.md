---
title: "Accelerating Diffusion Planners in Offline RL via Reward-Aware Consistency Trajectory Distillation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Accelerating_Diffusion_Planners_in_Offline_RL_via_Reward_Aware_Consistency_Trajectory_Distillation.pdf
project_link: null
code_link: null
aliases:
- RACTDR
- ADPORRACTD
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "将奖励优化直接融入一致性轨迹蒸馏过程，驱动学生模型从教师捕获的多模态分布中选择高奖励模式。"
primary_logic: "通过在噪声自由空间中使用预训练奖励模型对单步去噪学生进行奖励梯度引导，实现完全解耦训练，同时获得高回报动作轨迹与大幅推理加速。"
claims:
- "RACTD 将采样分布聚集在高奖励模式上。"
- "RACTD 在 D4RL Gym‑MuJoCo 上以 1 步采样取得最高平均分数，并比此前 SOTA 提升 9.7%。"
- "RACTD 在 hopper‑medium‑replay 上比 Diffuser 快 43 倍（0.015s vs 0.644s），NFE 从 20 降至 1。"
- "D4RL Gym‑MuJoCo (9 tasks) 上 Average Score (offline model selection) = 96.4"
---

# Accelerating Diffusion Planners in Offline RL via Reward-Aware Consistency Trajectory Distillation

> [!tip] 核心洞察
> 通过在噪声自由空间中使用预训练奖励模型对单步去噪学生进行奖励梯度引导，实现完全解耦训练，同时获得高回报动作轨迹与大幅推理加速。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于奖励感知一致性轨迹蒸馏的离线强化学习扩散规划器加速 |
| 英文题名 | Accelerating Diffusion Planners in Offline RL via Reward-Aware Consistency Trajectory Distillation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=hRuTBS07C7) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | Reward-Aware Consistency Trajectory Distillation (RACTD) |
| Dataset | D4RL Gym‑MuJoCo (9 tasks), D4RL FrankaKitchen (kitchen‑partial, kitchen‑mixed), Maze2d (Large) |

> [!tip] 效果简介
> - D4RL Gym‑MuJoCo (9 tasks) 上，Average Score (offline model selection) 为 96.4，对比 88.9 (Diffuser)，变化 +7.5 (about 8.4%)。
> - D4RL FrankaKitchen (kitchen‑partial, kitchen‑mixed) 上，Average Score (offline model selection) 为 60.0 (59.0, 60.9)，对比 51.9 (Consistency AC) for partial, 56.5 (Diffusion QL) for mixed，变化 competitive with NFE=1 vs baselines' NFE=2‑5。
> - Maze2d (Large) 上，Score 为 143.8 ±0.0，对比 123.0 (Diffuser, 256 NFE) / 149.0 (EDM teacher, 80 NFE)，变化 +20.8 over Diffuser, near teacher performance。

## 概要

扩散规划器（diffusion planners）在离线强化学习中展现出多模态行为建模能力，但其迭代采样过程导致推理速度极慢，难以满足实时决策需求。现有的加速方法面临两种困境：基于行为克隆的一致性蒸馏难以从次优数据中提取高质量策略；而演员‑评论家框架下的一致性蒸馏则需要并行训练多个网络，训练复杂且不稳定。其根本瓶颈在于，如何在保持对多模态行为分布覆盖的同时，快速引导采样集中到高回报区域。

本文提出奖励感知一致性轨迹蒸馏（Reward‑Aware Consistency Trajectory Distillation, RACTD），核心机制是在学生模型的一致性轨迹蒸馏过程中直接注入奖励信号。具体而言，方法由三个解耦模块构成：预训练的教师扩散规划器捕获离线数据中的多模态动作分布；学生一致性模型通过蒸馏学习从噪声到干净动作的任意步映射；预训练的奖励模型在干净的噪声自由空间中对学生单步去噪输出提供梯度引导。这一设计将奖励优化与分布蒸馏完全解耦，学生只需一次去噪即可生成高回报的动作轨迹。

实验表明，RACTD 在 D4RL Gym‑MuJoCo 的 9 项任务上以 1 步采样（NFE=1）取得平均分 96.4，相比此前最优的 Diffuser（88.9）提升约 8.4%。在 hopper‑medium‑replay 任务上，推理时间从 Diffuser 的 0.644 秒降至 0.015 秒，实现 43 倍加速，同时分数从 93.6 提升至 109.5。消融分析确认：奖励目标在学生蒸馏阶段加入优于教师阶段加入；单步采样已接近多步采样性能；适当的奖励损失权重显式驱动分布向高奖励模式聚集。方法局限性在于需训练三个网络，且蒸馏训练存在损失波动风险。



离线强化学习的核心挑战是从静态、混合质量的交互数据中学习高回报策略。扩散规划器（diffusion planners）通过建模动作序列的联合分布，能够有效捕获离线数据中蕴含的多模态行为模式，在标准基准任务上展现出超越传统方法的表现。然而，这类方法依赖迭代去噪采样，每一步推理都需要数十次甚至数百次网络前传（NFE），导致推理速度极慢，难以满足实时决策场景的延时约束。

为缓解这一瓶颈，一致性蒸馏（Consistency Trajectory Distillation, CTD）等加速范式被引入，试图将多步扩散过程压缩为单步或极少步数的生成。CTD 由一致性轨迹模型损失（$\mathcal{L}_{\mathrm{CTM}}$）和去噪得分匹配损失（$\mathcal{L}_{\mathrm{DSM}}$）共同构成，理论上可将采样步数降为一次函数评估。然而，直接将 CTD 与离线 RL 结合时，现有方案暴露出两条关键缺陷：

- **行为克隆型蒸馏（Consistency BC）** 简单模仿教师在训练数据上的生成分布，无法有选择地滤除次优行为。当数据集中包含大量低奖励轨迹时，学生模型会同等概率地采样低回报动作，导致性能退化。
- **演员‑评论家型蒸馏（Consistency AC）** 尝试在蒸馏过程中引入价值函数引导，但需要同时维护策略网络与评论家网络，多模型并发训练增加了优化难度与超参敏感性，训练不稳定且工程负担重（相关开放问题亦指出"如何开发更有效的基于一致性的蒸馏方法以应对次优数据及演员‑评论家网络的并发训练"）。

上述缺口直接推动本文的动机：**在一致性轨迹蒸馏的框架内，以完全解耦的方式将奖励信号注入学生模型，而不依赖于多步扩散采样或噪声感知的奖励模型**。具体而言，利用预训练的扩散教师捕获多模态行为分布，同时在噪声自由的"清洁"样本空间上引入一个独立训练的可微奖励模型，直接最大化学生单步输出动作的预期累积回报。这一设计使得奖励优化与蒸馏训练相互分离：教师负责提供行为多样性，奖励损失则以端到端可微的形式驱动学生将生成分布向高奖励模式聚集，无需在线执行分类器引导或多步反向传播奖励梯度。

这一动机的合理性在后续实验中得到了直接印证——在 D4RL Gym‑MuJoCo 的 9 个任务上，所提方法（RACTD）仅需 **1 次函数评估** 即可取得 **96.4** 的平均分数，相对此前最佳结果提升 9.7%；在 hopper‑medium‑replay 任务上，推理耗时从基线 Diffuser 的 0.644 秒降至 **0.015 秒**，加速比达 43 倍（NFE 从 20 降至 1）；最高加速情形下可达 142 倍。奖励分布分析（Figure 3）进一步表明，RACTD 成功将生成样本集中于 D4RL 数据的高奖励模式，验证了"奖励感知蒸馏可实现模式选择与推理提速统一"的核心假设。



## 核心方法与创新机理

扩散规划器在离线强化学习中面临一个众所周知的瓶颈：迭代去噪采样导致单步动作生成耗时过长，难以满足实时推理需求。此前的一致性蒸馏方法尝试加速采样路径，但它们要么在行为克隆范式下无法处理次优数据，要么依赖演员-评论家框架进行多网络并发训练，训练过程复杂且不稳定。

RACTD 的核心创新在于将**奖励优化直接融入一致性轨迹蒸馏过程**，从而在不引入演员-评论家框架的前提下，驱动学生模型从教师模型捕获的多模态行为分布中自主选择高回报模式。其关键机制可概括为：

1. **奖励感知的蒸馏目标**：在标准的一致性轨迹蒸馏损失（CTM loss + DSM loss）之上，额外引入可微奖励损失 $\mathcal{L}_{\mathrm{Reward}} = -R_{\psi}(\vec{s}_n, \hat{\mathbf{a}}_n)$，使得学生模型在去噪过程中被显式引导向高累积回报的动作序列。完整训练目标为：
   $$\mathcal{L} = \alpha \mathcal{L}_{\mathrm{CTM}} + \beta \mathcal{L}_{\mathrm{DSM}} + \sigma \mathcal{L}_{\mathrm{Reward}}$$
   这一训练目标的改变（即 changed slot）是 RACTD 区别于 Consistency BC 等基线方法的关键所在——后者依赖行为克隆进行蒸馏，无法利用奖励信号区分数据质量。

2. **完全解耦的训练架构**：由于学生模型可单步去噪，奖励模型 $R_{\psi}$ 可以直接在噪声自由的干净样本空间中进行训练和梯度回传，无需为扩散模型设计噪声感知的奖励模型，也无需执行多步奖励优化。这是与基于扩散模型的分类器引导采样方法（如 Diffuser 的 reward-guided sampling）的根本差异，后者必须在每个噪声级别计算奖励梯度，计算开销极大。

3. **从多模态到单峰的模式选择机制**：教师扩散规划器从混合质量离线数据中捕获包含次优模式的多模态行为分布。RACTD 通过奖励信号对单步去噪学生施加梯度引导，使采样分布自发向高奖励模式集中——Figure 3 显示，在 hopper-medium-expert 数据集上，RACTD 的采样分布明显聚集在较高奖励的模式上，而无条件教师和无条件学生的分布则分散覆盖多种模式。这意味着 RACTD 不是简单地拟合教师分布，而是在其支撑集内部进行奖励驱动的偏好选择。

4. **极致的推理加速与性能增益**：得益于单步采样能力，RACTD 在 D4RL Gym-MuJoCo 9 个任务上以 NFE=1 取得平均分数 96.4，相比 Diffuser（NFE≥20，平均 88.9）提升约 8.4%（摘要宣称较此前 SOTA 提升 9.7%）。在 hopper-medium-replay 上，推理时间从 Diffuser 的 0.644 秒降至 0.015 秒，NFE 从 20 降为 1，实现 43 倍加速，同时分数从 93.6 提升至 109.5（Table 4）。在 Maze2d Large 长时序规划任务中，RACTD 以 1 NFE 达到 143.8，超过 Diffuser（256 NFE）的 123.0，接近教师模型（80 NFE）的 149.0 水平。

消融实验进一步验证了奖励感知蒸馏设计的有效性：在 walker-medium 上，将奖励模型加入学生训练阶段的效果（118.8±0.3）显著优于加入教师训练阶段（94.5±2.6），这表明奖励驱动模式选择应在蒸馏阶段而非教师预训练阶段执行（Table 5）。此外，奖励损失权重存在最优值（hopper-medium-replay 上最佳权重 0.7 得 108.4±1.4），过高会导致训练不稳定（Figure 4），而 DSM 损失不可或缺——去除后将导致性能崩溃至 1.5±0.0（Table 14）。



![[assets/figures/papers/iclr26_0005_hRuTBS07C7_Accelerating_Diffusion_Planners_in_Offline_RL_vi/figures/001_Figure_1.jpg]]
*Figure 1: Overview of Reward Aware Consistency Trajectory Distillation (RACTD). We incorporate reward guidance with consistency trajectory distillation to train a student model that can generate actions with high rewards with only one denoising step*

RACTD 的整体流程由三个核心模块串联构成：预训练的教师扩散规划器、可单步去噪的学生一致性模型，以及独立预训练的奖励预测网络。三者的协作方式如下（参见 Figure 1）：

1. **教师扩散规划器（Teacher Diffusion Planner）**  
   首先在混合质量的离线轨迹数据上，采用 EDM 参数化的去噪得分匹配目标（式 (4)）训练一个无条件扩散模型。该教师能够捕获数据中固有的多模态行为分布，但推理时需要多步迭代去噪，速度极慢。

2. **学生一致性模型（Student Consistency Model）**  
   学生模型通过一致性轨迹蒸馏（CTD）从教师处继承分布知识。训练时同时施加两个损失：  
   - $\mathcal{L}_{\mathrm{CTM}}$（式 (5)）强制直接预测路径与两阶段预测路径在概率流 ODE（PF‑ODE）轨迹上的预测一致；  
   - $\mathcal{L}_{\mathrm{DSM}}$（式 (7)）迫使学生从噪声样本直接预测出干净的动作轨迹，从而稳定训练并保留数据分布。  
   蒸馏完成后，学生只需一次前向传播（NFE=1）即可从噪声生成高质量动作序列。

3. **奖励感知引导（Reward‑Aware Guidance）**  
   与传统扩散策略在噪声空间中优化奖励不同，RACTD 利用学生模型的单步去噪能力，直接在干净的状态‑动作空间引入一个预训练的可微回报预测网络 $R_{\psi}$。训练学生时，额外加入奖励损失 $\mathcal{L}_{\mathrm{Reward}} = -R_{\psi}(\vec{s}_n, \hat{\mathbf{a}}_n)$（式 (8)），通过最大化预测累积回报，将学生模型的生成分布从教师的多模态分布中拉向高奖励模式（Figure 3 证实了这种模式集中效应）。最终训练目标为  
   
$$
\mathcal{L} = \alpha\mathcal{L}_{\mathrm{CTM}} + \beta\mathcal{L}_{\mathrm{DSM}} + \sigma\mathcal{L}_{\mathrm{Reward}} \quad (\text{式 (9)}).
$$

**输入输出流**  
- **输入**：当前及历史的状态序列 $\vec{s}_n$（固定长度的过去观测）与随机噪声 $\mathbf{x}_T$。  
- **处理**：学生模型 $G_{\theta}(\mathbf{x}_T, T, 0)$ 一次性从噪声映射到干净的动作序列 $\hat{\mathbf{a}}_n$；奖励网络 $R_{\psi}$ 评估该轨迹的期望回报。  
- **输出**：高回报的固定长度未来动作序列；实际部署时仅执行第一个动作，形成闭环控制。

这种设计实现了**完全解耦的训练**：教师只负责建模行为分布，奖励模型只负责提供偏好信号，学生蒸馏阶段将二者统一。相比需要多网络并发训练的演员‑评论家方法，RACTD 的训练过程更简单；同时由于学生仅需单步采样，推理速度获得数量级提升（如在 hopper‑medium‑replay 上相比 Diffuser 的 20 NFE 降至 1 NFE，加速 43 倍，见表 4）。



RACTD 的架构由三个解耦模块构成，并通过将奖励优化直接嵌入一致性轨迹蒸馏，实现单步去噪生成高回报动作序列。

### 模块构成
- **教师扩散规划器（Teacher Diffusion Planner, EDM）**：预训练的无条件扩散模型，基于混合质量离线数据捕获多模态动作分布，为蒸馏提供丰富的轨迹先验。其训练目标采用 EDM 参数化的去噪得分匹配损失（公式 4）。
- **学生一致性模型（Student Consistency Model）**：通过一致性轨迹蒸馏（CTD）从教师路径学习，支持任意步去噪，尤其是单步生成。网络架构采用 1D 时序 CNN 与 FiLM 条件层，输入为固定长度的历史观测序列并输出未来动作序列。
- **预训练奖励模型（Reward Model, R_ψ）**：可微的回报预测网络，在干净（无噪声）的状态‑动作空间上给出期望累积折扣回报的估计，为学生蒸馏提供奖励信号。

图表引用：Figure 1 为总览，展示了如何将奖励引导结合 CTD 训练单步学生；Figure 2 可视化了 CTM 损失、DSM 损失和奖励损失在 PF‑ODE 轨迹上的作用。

### 关键公式

**问题建模（MDP 目标）**  
在离线数据约束下，策略需最大化累积折扣回报：

$$
\pi^{*} = \arg \max_{\pi} \mathbb{E}_{\tau \sim \pi} \left[ \sum_{n=0}^{H} \gamma^{n} R(\mathbf{s}_n,\mathbf{a}_n) \right] \tag{1}
$$

**教师训练损失**  
教师模型 $D_{\phi}$ 学习从带噪轨迹 $\mathbf{x}_t$ 预测原始干净轨迹 $\mathbf{x}_0$：

$$
\mathcal{L}_{\mathrm{EDM}} = \mathbb{E}_{t,\mathbf{x}_{0},\mathbf{x}_{t}\mid\mathbf{x}_{0}}\left[ d(\mathbf{x}_{0}, D_{\phi}(\mathbf{x}_{t}, t)) \right] \tag{4}
$$

**一致性轨迹模型损失（CTM loss）**  
强制学生模型 $G_{\theta}$ 的"直接预测路径"与"两步预测路径"一致性（$\mathrm{sg}(\theta)$ 表示停止梯度）：

$$
\mathcal{L}_{\mathrm{CTM}} = \mathbb{E}\left[ d\left( G_{\mathrm{sg}(\theta)}(\hat{\mathbf{x}}_{k}^{(t)}, k, 0),\; G_{\mathrm{sg}(\theta)}(\mathbf{x}_{k}^{(t,u)}, k, 0) \right) \right] \tag{5}
$$

其中：

- 直接预测：$\hat{\mathbf{x}}_{k}^{(t)} = G_{\theta}(\mathbf{x}_{t}, t, k)$，
- 两步预测：$\mathbf{x}_{k}^{(t,u)} = G_{\mathrm{sg}(\theta)}(\mathrm{Solver}(\mathbf{x}_{t}, t, u;\phi), u, k)$。

**去噪得分匹配损失（DSM loss）**  
直接约束学生从噪声到干净样本的一步映射，防止模式偏离：

$$
\mathcal{L}_{\mathrm{DSM}} = \mathbb{E}_{t,\mathbf{x}_{0},\mathbf{x}_{t}\mid\mathbf{x}_{0}}\left[ d(\mathbf{x}_{0}, G_{\theta}(\mathbf{x}_{t}, t, 0)) \right] \tag{7}
$$

**奖励损失（Reward loss）**  
利用奖励模型驱动学生生成高回报动作序列，负号表示最大化奖励：

$$
\mathcal{L}_{\mathrm{Reward}} = -R_{\psi}(\vec{s}_n, \hat{\mathbf{a}}_n) \tag{8}
$$

其中 $\vec{s}_n$ 为历史观测序列，$\hat{\mathbf{a}}_n$ 为学生单步去噪预测的动作序列。

**RACTD 总损失**  
将上述三种损失加权组合，实现端到端蒸馏：

$$
\mathcal{L} = \alpha \mathcal{L}_{\mathrm{CTM}} + \beta \mathcal{L}_{\mathrm{DSM}} + \sigma \mathcal{L}_{\mathrm{Reward}} \tag{9}
$$

- CTM 损失和 DSM 损失共同构成一致性轨迹蒸馏（CTD）。
- 奖励损失仅在学生训练阶段加入，使整个过程完全解耦：教师无需感知奖励，奖励模型也未涉及噪声空间。

文献指出，这种奖励感知蒸馏可视为离策略确定性策略梯度的一种近似：学生单步生成的动作相当于确定性策略输出，奖励损失提供梯度方向，将采样分布聚集到高奖励模式（Figure 3 验证了这一模式选择效果）。需注意不同任务对损失权重敏感（附录 Table 9、Table 14–15），尤其是奖励权重过大可能引起训练不稳定。



## 实验与关键发现

本节围绕 RACTD（Reward‑Aware Consistency Trajectory Distillation）在标准离线 RL 基准上的主结果、消融实验与吞吐效率展开分析，同时指出核心瓶颈与失败模式。所有实验均在 D4RL Gym‑MuJoCo、FrankaKitchen 和 Maze2d 三个环境中进行，对比基线涵盖行为克隆、模型‑free 离线 RL（CQL、IQL）、序列决策模型（DT、TT）、基于模型的方法（MOPO、MOReL、MBOP）以及扩散类方法（Diffusion QL、Consistency AC、Consistency BC、Diffuser）。

### 主任务性能与加速效果

**Gym‑MuJoCo 离线 RL（Table 1）**。在 9 个任务的离线模型选择标准下，RACTD 以 **仅 1 个函数评估次数（NFE=1）** 取得平均分 **96.4**，优于 Diffuser 的 88.9 和此前所有对比方法，相对先前 SOTA 提升约 **9.7%**。在 8/9 任务上 RACTD 位列前二，尤其在半猎豹‑中‑回放（halfcheetah‑medium‑replay）和 walker2d‑中‑专家（walker2d‑medium‑expert）等次优数据占比高的场景中，单步采样即展现出显著增益。该结果由教师扩散模型捕获的多模态分布与学生阶段嵌入的奖励梯度引导共同支撑：$ \mathcal{L} = \alpha \mathcal{L}_{\mathrm{CTM}} + \beta \mathcal{L}_{\mathrm{DSM}} + \sigma \mathcal{L}_{\mathrm{Reward}} $ 在保持行为覆盖的同时将采样质量推向高回报模式。

![[assets/figures/papers/iclr26_0005_hRuTBS07C7_Accelerating_Diffusion_Planners_in_Offline_RL_vi/figures/004_Table_1.jpg]]
*Table 1: (Offline RL: Gym-MuJoCo) Performance and sampling efficiency (NFE: Number of Function Evaluations) of RACTD and a variety of baselines on the D4RL Gym-MuJoCo benchmark. Results As shown in Table 1, RACTD achieves the highest average score by a substantial margin and best or second-best performance on 8 / 9 tasks in Gym-MuJoCo, with the only exception being a medium-expert dataset where reward guidance is less beneficial. RACTD is also the only planningbased method that achieves single-step sampling compared to consistency model based actor-critic methods (which require double sampling steps) and other diffusion-based planners (which require 20× more sampling steps)*

**FrankaKitchen 长时序操作（Table 2）**。在 kitchen‑partial 与 kitchen‑mixed 两个子任务上，RACTD（NFE=1）平均得分 **60.0**，与采用 2‑5 步采样的 Diffusion QL、Consistency AC 等持平，且推理步骤数仅为后者的 $1/5$。这表明奖励感知蒸馏可以有效蒸馏复杂操作空间中的多步规划能力。

**Maze2d 长时序规划（Table 3）**。RACTD 在 Large 迷宫中取得 **143.8** 分（NFE=1），远超 Diffuser 的 123.0（NFE=256）并逼近无奖励引导的教师模型（EDM，NFE=80，149.0）。全局平均分 133.4 亦在所有开环规划方法中最高，验证了蒸馏过程对长跨步状态空间的高保真传递。

![[assets/figures/papers/iclr26_0005_hRuTBS07C7_Accelerating_Diffusion_Planners_in_Offline_RL_vi/figures/006_Table_3.jpg]]
*Table 3: (Long-horizon planning) The performance of RACTD, Diffuser, Flow Q-learning and prior model-free algorithms in the Maze2D environment. Flow Q-learning is close loop planning and Diffuser, RACTD are open loop planning*

**推理效率（Table 4）**。以 hopper‑medium‑replay 为例，RACTD 的单次动作生成仅需 **0.015 s**，相较 Diffuser（0.644 s，20 NFE）实现 **43× 加速**；相比同环境下基于 DDIM 或 DDPM 的方法也有 20‑30 倍提升。这一加速根源在于学生模型 $G_\theta$ 经损失 $\mathcal{L}_{\mathrm{CTM}}$ 直接学习从噪声到干净轨迹的任意步跳转，使得推理退化为一次前向传播。

![[assets/figures/papers/iclr26_0005_hRuTBS07C7_Accelerating_Diffusion_Planners_in_Offline_RL_vi/figures/007_Table_4.jpg]]
*Table 4: Wall clock time and NFEs per action for different samplers and Diffuser on MuJoCo hopper-medium-replay*

### 消融实验

**奖励引导的注入阶段（Table 5）**。将奖励目标加入学生蒸馏阶段（RACTD）的性能（118.8±0.3）显著优于将其加入教师训练阶段（94.5±2.6）。噪声‑free 空间中的单步去噪使可微奖励模型 $R_\psi$ 能够直接评估生成动作的期望回报，避免多步扩散中所需的噪声感知奖励建模，是解耦训练的关键。

![[assets/figures/papers/iclr26_0005_hRuTBS07C7_Accelerating_Diffusion_Planners_in_Offline_RL_vi/figures/008_Table_5.jpg]]
*Table 5: We compare incorporating the reward model in different stages of training on MuJoCo hopper-medium-replay. Results are presented as the mean and standard error across 100 seeds*

**损失权重敏感性**。在 hopper‑medium‑replay 上，奖励权重 $\sigma$ 的最优值约为 **0.7**（得分 108.4±1.4），过高（如 1.5）会导致训练不稳定（Table 15）。DSM 权重 $\beta$ 的最佳值为 **1.0**，去除该项会使性能崩溃至 1.5±0.0（Table 14），说明纯 CTM 损失无法覆盖行为探索所需的分布对齐，DSM 与 CTM 的联合对维持生成多样性不可或缺。

**采样步数上限（Table 16）**。将 NFE 从 1 提升至 2 或 4 几乎不带来分数的额外提升（109.5 → 109.8 → 107.9），且推理时间成倍增加。这表明 RACTD 训练时 learn 的 "anytime‑to‑anytime" 跳转能力使得单步生成已逼近质量上限。

**规划视界与历史长度（Table 17 等）**。在 walker‑medium‑replay 上，将历史观测窗口扩展到 4 步、动作规划视界延长至 16 步，可以将分数提升至 108.0±1.4，说明更长上下文对部分部分可观察环境有帮助，但相对于单步采样的核心增益而言为次要因素。

### 模式选择与奖励分布（Figure 3）

在 hopper‑medium‑expert 数据集上，无条件教师与无条件学生的采样奖励分布均呈双峰，包含低奖励模式；RACTD 则将分布几乎完全集中到高奖励模式上，证实了奖励损失 $\mathcal{L}_{\mathrm{Reward}} = -R_\psi(\vec{s}_n, \hat{\mathbf{a}}_n)$ 通过梯度引导提供了有效模式过滤，而非简单复现数据集中的高奖励片段。

### 失败模式与限制

1. **训练成本**：需要分别预训练教师扩散模型、奖励模型以及学生蒸馏，三条管线独立部署，总体计算开销较高。  
2. **教师步骤依赖**：教师要达到强泛化通常需要 $>20$ 步去噪，这一耗时瓶颈限制了整体的训练吞吐。  
3. **蒸馏稳定性**：CTM 损失自身存在波动，加入奖励目标后权重稍高即会引起训练扰动的放大（Table 15），需针对每个任务调整 $\sigma$。  
4. **离线评估偏差**：在部分 D4RL 环境中，离线模型选择与在线选择存在小幅度不一致，但对 RACTD 的相对优势影响有限（Table 2 离线/在线均显示竞争力）。

本实验未涉及安全性、公平性或分布外泛化的专门评估，且仅适用于具备可微奖励模型的离线任务，直接将不可微反馈（如规则评估器）纳入蒸馏仍需进一步研究。

### 补充图表

![[assets/figures/papers/iclr26_0005_hRuTBS07C7_Accelerating_Diffusion_Planners_in_Offline_RL_vi/figures/003_Figure_3.jpg]]
*Figure 3: The reward distribution of the D4RL hopper-medium-expert dataset and 100 rollouts from an unconditioned teacher, an unconditioned student, and RACTD*



## 定位与知识库关联

RACTD 的核心定位是**奖励感知的一致性轨迹蒸馏**，它直接回应了扩散规划器在离线强化学习中的两大瓶颈：迭代采样导致的推理速度慢，以及现有一致性蒸馏方法无法在行为克隆下有效处理次优数据的问题。该方法通过将独立的奖励模型引入学生蒸馏阶段，在保持训练完全解耦的同时，引导单步去噪学生从教师的多模态分布中主动选择高奖励模式。

### 与基线及后续方法的关系

RACTD 的方法脉络建立在以下几条技术路线之上：

- **相对于扩散规划器（如 Diffuser）**：Diffuser 通过在扩散采样过程中注入奖励引导来实现高回报规划，但必须进行多次反向去噪（通常在 20 步以上），推理延迟极高。RACTD 保留了教师扩散模型捕获多模态行为的能力，却将生成过程压缩为一次函数评估，在 MuJoCo hopper‑medium‑replay 任务上将推理时间从 0.644 s 降至 0.015 s，同时将分数从 93.6 提升至 109.5（Table 4）。这意味着 RACTD 不是简单地用速度换质量，而是在显著加速的同时获得了更好的性能。

- **相对于一致性蒸馏基线（Consistency BC / Consistency AC）**：一致性行为克隆（Consistency BC）虽然能一步生成动作，但在面对混杂着次优行为的数据时，学生会无差别地模仿所有模式，导致平均回报受限。一致性演员‑评论家（Consistency AC）尝试通过评论家网络进行模式筛选，却引入了多网络并发训练的复杂性和不稳定性。RACTD 绕开了这一权衡：它采用**无条件教师**（仅负责覆盖分布）与**独立奖励模型**的组合，训练过程完全解耦，并通过奖励损失 $ \mathcal{L}_{\mathrm{Reward}} = -R_{\psi}(\vec{s}_n, \hat{\mathbf{a}}_n) $ 直接驱动学生模型收敛到高奖励区域。Figure 3 直观地展示了这一模式选择效应——RACTD 的采样分布明显集中在高奖励模式上，而普通学生则沿习了教师的全部模式。

- **相对于其他离线 RL 基线**：与基于 Q‑learning 的方法（CQL、IQL）不同，RACTD 不依赖价值函数外推，而是通过扩散建模直接生成动作序列，天然适合处理多模态行为。与序列决策模型（Decision Transformer、Trajectory Transformer）相比，RACTD 利用一致性模型将生成过程压缩为单步去噪，在推理效率上具备数量级优势。在 D4RL Gym‑MuJoCo 的 9 个任务上，RACTD 以 1 NFE 取得平均 96.4 的分数，较 Diffuser（88.9）提升约 8.4%（Table 1），并在 8/9 任务上位列最优或次优。

- **技术贡献的"可控旋钮"**：RACTD 的关键创新在于将奖励信号直接嵌入蒸馏目标。这一改变完成了两个层面的价值提升：在训练层面，学生模型在噪声自由空间中受到回报最大化驱动的梯度更新，回避了以往方案中需要对噪声状态进行奖励估计的难题；在推理层面，学生既能单步生成高回报动作，又可天然支持任意步数的去噪（无需额外训练），为部署提供了灵活性。

### 适用边界

RACTD 的优势在以下条件下最为突出，超出这些边界则需要谨慎评估：

- **任务与数据特性**：适用于连续控制、具有明显多模态行为和足够次优样本多样性的离线 RL 场景，如 MuJoCo 步态控制、Fean厨房操作和迷宫导航。当策略分布为单峰或高奖励模式和低奖励模式在数据中没有显著分离时，模式选择机制的额外收益会减弱。
- **模型依赖**：必须预先训练一个足够强大的扩散教师（在 Maze2d 上教师需使用 80 NFE 才能达到高规划质量）和一个可微的回报预测网络。若教师无法充分覆盖高奖励区域，学生蒸馏将无法弥补这一缺陷；若奖励模型不可微（如基于规则的评估器），RACTD 当前框架无法直接适用。
- **训练负担**：三个网络（教师、学生、奖励模型）的串行或并行训练虽然相互解耦，但整体计算开销仍高于端到端的单阶段方法。在算力受限的场景下，这一成本需要纳入权衡。
- **超参数敏感性**：损失权重 $\alpha$（CTM）、$\beta$（DSM）和 $\sigma$（Reward）对最终性能影响显著。消融实验显示，去除 DSM 损失会导致性能崩溃（Table 14），而奖励权重过高则可能引发训练剧烈震荡（Figure 4），需要针对不同任务进行调参。

### 局限与开放问题

**已知局限**

1.  **训练成本与复杂度**：需要训练教师扩散模型、学生一致性模型和奖励模型三个独立网络，训练准备时间高于单阶段方法。
2.  **损失稳定性**：一致性轨迹蒸馏本身的训练过程就存在波动（CTM 损失中两条路径的对齐要求严格），额外加入的奖励梯度可能进一步放大不稳定性，尤其是在奖励权重较大的情况下。
3.  **教师质量的依赖**：RACTD 继承自教师模型的多模态分布能力，若教师在特定环境下表现不佳，学生的性能也会随之受限。

**开放问题**

-   能否开发更稳定的蒸馏训练算法，以降低波动并减轻对超参数的敏感性？例如，探索自适应损失平衡策略或正则化技术。
-   如何将 RACTD 框架扩展到不可微奖励函数的场景（如基于稀疏规则的评估器），从而使方法能够服务于更广泛的离线决策任务？
-   能否利用一个通用的无条件教师模型，针对不同下游任务仅重新训练或切换奖励模型，快速蒸馏出任务专属的单步规划器？这将大幅提升 RACTD 在多变任务环境下的迁移效率。
-   当前实验显示，在多步采样下性能未见明显提升（NFE = 2 相比 NFE = 1 几乎持平），这是否意味着单步蒸馏已经逼近教师模型的能力上限？是否存在进一步突破该上限的蒸馏策略？



## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Accelerating_Diffusion_Planners_in_Offline_RL_via_Reward_Aware_Consistency_Trajectory_Distillation.pdf

![[paperPDFs/ICLR_2026/Accelerating_Diffusion_Planners_in_Offline_RL_via_Reward_Aware_Consistency_Trajectory_Distillation.pdf]]
