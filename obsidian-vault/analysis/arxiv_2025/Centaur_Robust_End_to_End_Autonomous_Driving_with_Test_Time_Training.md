---
title: "Centaur: Robust End-to-End Autonomous Driving with Test-Time Training"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Centaur_Robust_End_to_End_Autonomous_Driving_with_Test_Time_Training.pdf
project_link: null
code_link: https://github.com/OpenDriveLab/OpenScene
aliases:
- Centaur
tags:
- arxiv_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过测试时训练（TTT）在线最小化规划器决策的不确定性。具体而言，引入一种名为集群熵（Cluster Entropy）的新型不确定性度量，基于驾驶方向对候选轨迹进行聚类，计算5路分类熵，并利用历史帧的梯度异步更新规划器的评分解码器，从而在不损害进度的情况下提高安全性。
primary_logic: 集群熵提供了一种简单、可解释且无监督的不确定性估计，适用于轨迹评分的端到端规划器。TTT仅使用单步梯度更新，配合梯度缓冲区实现异步并行，能够有效抑制异常高评分，使模型偏向更安全的方向，从而显著提升安全关键指标（如TTC）并接近人类表现。
claims:
- Centaur在navtest基准上达到92.6% PDMS，大幅超越回退层策略（65.3%）并接近人类上限（94.8%），证明TTT的有效性。
- 在navtest官方排行榜上，Centaur以92.10%平均PDMS排名第一，显著优于Hydra-MDP（91.26%）等基线，且无需模型集成。
- 在更具挑战性的navsafe安全基准上，Centaur取得74.14总体PDMS，远超Hydra-MDP（56.47）和Hydra-SE（62.84），展示了在边缘场景中的泛化能力。
- 集群熵在故障识别任务中达到62.8% TPR和73.6%准确率，优于其他不确定性度量，适用于预警系统。
---

# Centaur: Robust End-to-End Autonomous Driving with Test-Time Training

> [!tip] 核心洞察
> 集群熵提供了一种简单、可解释且无监督的不确定性估计，适用于轨迹评分的端到端规划器。TTT仅使用单步梯度更新，配合梯度缓冲区实现异步并行，能够有效抑制异常高评分，使模型偏向更安全的方向，从而显著提升安全关键指标（如TTC）并接近人类表现。

| 字段 | 内容 |
|------|------|
| 中文题名 | Centaur：基于测试时训练的鲁棒端到端自动驾驶 |
| 英文题名 | Centaur: Robust End-to-End Autonomous Driving with Test-Time Training |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2503.11650) · [Code](https://github.com/OpenDriveLab/OpenScene) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Centaur |
| Dataset | navtest, navsafe |

> [!tip] 效果简介
> - navtest (NAVSIM v1.1) 上，PDMS (%) 92.10 ± 0.33 vs 91.26 (Hydra-MDP* ensemble) (+0.84)。
> - navsafe (safety-critical subset) 上，Overall PDM Score 74.14 vs 56.47 (Hydra-MDP) (+17.67)。

## 概要

端到端自动驾驶规划器在部署时面临一个根本性瓶颈：安全性与适应性不足。现有应对策略分为两条路径——**回退层策略**利用预定义安全动作检测失败，但导致过度保守行为，严重损害自车进度（EP）；**测试时优化**依赖显式表示和手工成本函数，需要昂贵标注，阻碍端到端方法的可扩展性。两者均无法通过新数据实现自我改进。

Centaur 的核心洞察是：**通过测试时训练（Test-Time Training, TTT）在线最小化规划器决策的不确定性，可以在不牺牲进度的情况下显著提升安全性**。为此，论文提出了一种名为**集群熵（Cluster Entropy）**的新型不确定性度量——基于驾驶方向对候选轨迹进行聚类，计算5路分类熵，并利用历史帧的梯度异步更新规划器的评分解码器。这一机制本质上抑制了模型在多个方向簇中同时赋予高评分的能力，从而修正异常高评分的离群预测，使模型偏向更安全的方向。

在方法定位上，Centaur 以轨迹评分范式端到端规划器 **Hydra-MDP** 为基础，仅在线更新评分解码器而冻结感知骨干网络，通过梯度缓冲区（长度 $F=4$）实现异步并行，避免引入显著的推理延迟。

主要实验结果确立了 Centaur 的有效性：

- **navtest 基准**：Centaur 达到 92.6% PDMS，大幅超越回退层策略（65.3%）并接近人类上限（94.8%）；在官方排行榜上以 92.10% 平均 PDMS 排名第一，以单模型超越 Hydra-MDP 的 3 模型集成（91.26%）。
- **navsafe 安全基准**：在涵盖环岛、无保护左转、恶劣天气等 10 类安全关键场景的 229 帧子集上，Centaur 取得 74.14 总体 PDMS，远超 Hydra-MDP（56.47）和 Hydra-SE（62.84），展示了在边缘场景中的强泛化能力。
- **故障识别**：集群熵在故障识别任务中达到 62.8% TPR 和 73.6% 准确率，适用于预警系统。
- **消融实验**：集群熵相比语义熵提高 0.8 PDMS，相比无 TTT 的 Hydra-MDP 提高 2.3 PDMS；TTT 对轨迹回归规划器 **TransFuser** 同样带来 2.3 PDMS 的提升，验证了方法的通用性。

论文的主要局限在于仅在 NAVSIM 仿真环境中验证，尚未在真实车辆或闭环系统中测试；TTT 虽通过缓冲区异步化，仍引入额外计算开销（Hydra-MDP 推理延迟从 243.9ms 增至 312.5ms）。开放问题包括如何扩展到闭环驾驶、在资源受限平台上的部署，以及长期持续适应中的灾难性遗忘风险。

端到端自动驾驶旨在直接从传感器输入映射到规划轨迹，但现有方法在部署时面临一个核心瓶颈：**安全性与适应性的不足**。主流应对策略可归为两类，但均存在明显缺陷。

**回退层策略的保守性陷阱。** 一种常见做法是为端到端规划器配备回退层（fallback layer），当检测到规划失败时切换至预定义的安全动作。然而，这种策略导致过度保守的行为——车辆倾向于不必要的减速或停车，严重损害自车进度（Ego Progress）。在navtest基准上，回退层策略的PDMS仅为65.3%，远低于无回退的基线方法，其EP子评分甚至降至13以下（Table 1）。这揭示了一个根本矛盾：**以牺牲进度为代价换取的安全，在真实驾驶场景中并不可行**。

**测试时优化的标注依赖困境。** 另一类方法采用显式表示和手工设计的成本函数进行测试时优化（如UniAD等），通过在线调整规划器输出来提升安全性。然而，这类方法依赖昂贵的专家标注来构建成本函数，阻碍了端到端方法的核心优势——可扩展性。当面对未见过的场景时，固定的成本函数难以泛化，而重新标注的成本高昂。

**两类方法的共同盲区：无法从新数据中自我改进。** 无论是回退层还是手工成本优化，本质上都是静态策略——它们无法利用部署过程中遇到的新数据来持续改进模型行为。一旦模型训练完成，其决策逻辑便被固化，面对分布外场景时只能依赖预定义的规则，而非动态适应。

Centaur的动机正是弥合这一缺口：**通过测试时训练（Test-Time Training, TTT）实现无需标注的在线自适应**。其核心洞察在于，端到端规划器的不确定性可以通过一种简单、可解释的度量——集群熵（Cluster Entropy）来捕捉，而最小化这种不确定性能够有效抑制异常高评分，使模型偏向更安全的方向，从而在不损害进度的情况下提升安全关键指标（如TTC），并接近人类驾驶表现（94.8%）。

## 核心方法与创新机理

Centaur 的核心创新在于将**测试时训练（Test-Time Training, TTT）**引入端到端自动驾驶规划器的部署阶段，并通过一种全新的无监督不确定性度量——**集群熵（Cluster Entropy）**——来驱动这一在线适应过程。其设计直击现有方法的两个关键瓶颈：回退层策略的过度保守性，以及基于显式代价函数的测试时优化对昂贵标注的依赖。

### 创新一：集群熵——面向轨迹评分的不确定性度量

传统的不确定性度量（如全熵、语义熵、KL 散度）在端到端规划器中缺乏对驾驶决策结构的显式建模。Centaur 提出的**集群熵**（Section 2.1）利用规划器输出轨迹的**驾驶方向**作为天然聚类依据，将候选轨迹划分为 5 个方向类别（直行、轻微左转、轻微右转、左转、右转），计算评分分布在这 5 类上的分类熵：

- **因果机制**：当规划器在多个方向类别上同时给出高评分时，集群熵升高，表明模型对驾驶方向存在不确定性。TTT 通过梯度下降最小化该熵，**抑制模型在多个类别上分配高评分的能力**，从而修正那些与同类轨迹评分显著偏离的离群预测（Section 2.2）。
- **设计优势**：集群熵**无需专家标注或代价函数**，完全无监督；仅依赖规划器自身的评分输出，计算简单且可解释。与语义熵（Hydra-SE）相比，集群熵在 navtest 上将 PDMS 提升了 **0.8 个百分点**（Table 1）。

### 创新二：基于历史梯度缓冲区的异步测试时训练

Centaur 的 TTT 策略并非在每一帧都进行完整的在线学习，而是设计了一套轻量且可异步执行的更新机制（Section 2.2, Figure 2）：

- **更新范围**：仅更新**轨迹评分解码器**的参数，冻结感知骨干网络。这使得梯度计算和参数更新的计算量大幅降低，同时保持了感知特征的稳定性（Section 4.1 Implementation）。
- **梯度累积缓冲区**：维护一个长度为 $F=4$ 的历史梯度缓冲区，每次更新使用缓冲区中历史梯度的**平均值**进行单步梯度下降：
  $$\hat{\theta}_i = \theta - \eta \left\{ \frac{\partial H}{\partial\theta} \right\}_{\text{avg}}$$
  这一设计不仅平滑了梯度更新，还使得梯度计算可以**异步并行**于推理过程——当前帧的梯度来自缓冲区中已有的历史帧，无需等待当前帧的反向传播完成即可执行推理（Section 2.2）。
- **与回退层的本质区别**：回退层策略在检测到不确定性后直接替换轨迹为预定义安全动作，导致自车进度（EP）子评分大幅下降（Table 1 中 EP 降至 13 以下），严重损害整体 PDMS。TTT 则通过参数调整使模型**自主偏向更安全的决策方向**，在提升安全子评分（如 TTC）的同时保持了高进度。

### 创新三：统一的不确定性感知与自适应部署框架

Centaur 将不确定性度量和在线适应统一为闭环：集群熵既是 TTT 的优化目标，也可作为**故障预警信号**。在故障识别任务中，集群熵以 **62.8% TPR 和 73.6% 准确率**识别规划器即将失败的帧（Table 3），优于其他不确定性度量。这为选择性启用 TTT（仅在高不确定性帧触发更新）提供了依据，可进一步降低计算开销（Table 7）。

### 与基线方法的 changed slots 总结

| 维度 | 基线方法 | Centaur |
|------|---------|---------|
| **不确定性度量** | 无（回退层）或 KL 散度、全熵 | 集群熵（Cluster Entropy） |
| **部署策略** | 无在线更新，或回退层替换轨迹 | TTT 通过历史梯度缓冲区异步更新参数 |
| **更新范围** | 完整模型或无更新 | 仅更新评分解码器，冻结感知骨干 |
| **梯度组合** | 无（SVD 或直接使用） | 缓冲区历史梯度平均值 |

这些创新使 Centaur 在 navtest 基准上达到 **92.6% PDMS**，大幅超越回退层策略（65.3%）并接近人类上限（94.8%）；在更具挑战性的 navsafe 安全基准上取得 **74.14 总体 PDMS**，远超 Hydra-MDP（56.47）和 Hydra-SE（62.84），验证了 TTT 在边缘场景中的泛化能力（Table 1, Table 4）。

Centaur 的整体框架围绕“测试时训练（Test-Time Training, TTT）”展开，其核心思路是在部署阶段通过在线梯度更新来抑制规划器决策中的不确定性，从而在不牺牲行驶进度的前提下提升安全性。该方法建立在轨迹评分（trajectory scoring）范式的端到端规划器之上，其基础模型为 Hydra-MDP。整个 pipeline 由离线训练好的感知骨干网络、轨迹评分解码器，以及部署时新增的集群熵计算器、梯度累积缓冲区和参数更新步五个关键模块构成，如 Figure 2 所示。

![[assets/figures/papers/paper_list_l80_https_arxiv_org_abs_2503_11650/figures/002_Figure_2.jpg]]
*Figure 2: Test-Time Training (TTT) in Centaur. Top: A trained end-to-end planner scores trajectories from the planning vocabulary for frames observed during testing. We sample a subset of these, clustered based on their driving direction. After aggregating predicted scores over clusters, a Cluster Entropy is calculated to reflect the uncertainty. We then obtain a gradient for Cluster Entropy minimization via backpropagation. Bottom: We accumulate gradients from historical frames and update our planner to achieve improved performance*

### 推理阶段的前向流程

在每一帧推理时，系统首先执行标准的前向传播：

1. **感知骨干网络** 接收传感器输入（LiDAR 和图像）以及导航指令 $\mathbf{c}_0$，提取 BEV 特征 $\mathbf{x}_0$。该模块在 TTT 过程中保持冻结，不参与参数更新。
2. **轨迹评分解码器** $\pi_\theta$ 为规划词汇表中所有 $k$ 条候选轨迹 $\{\mathbf{t}_j\}_{j=1}^k$ 预测评分特征 $\{s_j\}_{j=1}^k$，每条轨迹的评分特征包含多个子评分维度（NC、DAC、EP、C、TTC）：
   $$\{ s_j \}_{j=1}^k = \{ \pi_\theta ( \mathbf{t}_j , \mathbf{x}_0 , \mathbf{c}_0 ) \}_{j=1}^k$$
3. **轨迹选择模块** 通过聚合函数 $\phi$ 计算每条轨迹的最终评分，并选择评分最高的轨迹作为规划输出：
   $$\hat{\mathbf{t}}_0 = \underset{ {\mathbf{t}_j} }{ \arg\max } \{ \phi( s_j ) \}_{j=1}^k$$

### 不确定性估计：集群熵

在完成轨迹评分后，Centaur 引入了一种名为**集群熵（Cluster Entropy）**的新型不确定性度量。具体而言，系统从候选轨迹中采样 $M=100$ 条，按照其驾驶方向（如直行、微左转、微右转等）聚类为 5 个类别，然后在类别层面聚合预测评分，构建一个 5 路分类分布，并计算该分布的熵。集群熵越高，表明规划器在多个驾驶方向上都分配了高评分，即决策不确定性越大。

这一设计的直觉在于：当模型对某个方向的预测高度自信时，该方向的轨迹评分应集中且显著高于其他方向，熵值较低；反之，若模型在多个方向间摇摆不定，则熵值升高，提示潜在的安全风险。

### 测试时训练：梯度累积与参数更新

一旦计算出集群熵 $H$，Centaur 通过反向传播获得梯度 $\frac{\partial H}{\partial\theta}$，并将其存入一个长度为 $F=4$ 的历史梯度缓冲区。参数更新时，使用缓冲区内历史梯度的**平均值**进行一步梯度下降，学习率 $\eta = 1 \times 10^{-4}$：

$$\hat{\theta}_i = \theta - \eta \left\{ \frac{\partial H}{\partial\theta} \right\}_{\text{avg}}$$

这一机制的效果在于抑制模型在多个簇中同时分配高评分的能力，从而修正那些与簇内其他轨迹显著偏离的异常高评分预测，使模型偏向更安全的驾驶方向。

### 异步并行与计算效率

梯度计算仅依赖缓冲区中已有的历史时间步梯度，因此可以与当前帧的前向推理异步并行执行，避免阻塞实时决策。消融实验（Table 7）表明，TTT 带来的额外推理延迟可控：Hydra-MDP 的基础推理延迟从 243.9ms 增至 312.5ms。此外，仅在高不确定性帧触发 TTT 可进一步摊销计算开销。

### 与回退层策略的本质区别

传统的回退层（fallback layer）策略在检测到不确定性时，直接替换为预定义的安全轨迹。虽然这能避免碰撞，但会导致极端保守的行为——例如自车进度（EP）子评分降至 13 以下，严重损害整体 PDMS（Table 1）。相比之下，Centaur 的 TTT 通过微调解码器参数来“修正”评分分布，在提升安全子评分（如 TTC）的同时保持了高进度，实现了安全性与行驶效率的兼顾。

### 轨迹评分与选择

Centaur 建立在端到端轨迹评分规划器之上。给定传感器输入 $\mathbf{x}_0$ 和导航指令 $\mathbf{c}_0$，规划器 $\pi_\theta$ 为规划词汇表中的 $k$ 条候选轨迹 $\{\mathbf{t}_j\}_{j=1}^k$ 分别预测评分特征：

$$
\{ s_j \}_{j=1}^k = \{ \pi_\theta ( \mathbf{t}_j , \mathbf{x}_0 , \mathbf{c}_0 ) \}_{j=1}^k
$$

每条轨迹的评分特征 $s_j$ 包含五个子评分：无责碰撞（NC）、可行驶区域合规（DAC）、自车进度（EP）、舒适度（C）和时间到碰撞（TTC）。通过聚合函数 $\phi$ 将这些子评分合并为单一标量评分，选择评分最高的轨迹作为规划输出：

$$
\hat{\mathbf{t}}_0 = \underset{ \mathbf{t}_j }{ \arg\max } \{ \phi( s_j ) \}_{j=1}^k
$$

规划器的训练目标是通过知识蒸馏，最小化模型预测评分与专家评分 $e(\mathbf{t},\mathbf{x},\mathbf{c})$ 之间的交叉熵：

$$
\arg\min_\theta \mathbb{E}_{(\mathbf{t},\mathbf{x},\mathbf{c})\sim D_{kd}} [ \mathcal{L}_{kd} ( e(\mathbf{t},\mathbf{x},\mathbf{c}), \pi_\theta(\mathbf{t},\mathbf{x},\mathbf{c}) ) ]
$$

### 集群熵（Cluster Entropy）

集群熵是 Centaur 的核心不确定性度量模块。其计算流程如下：从 $k$ 条候选轨迹中采样 $M=100$ 条，根据每条轨迹的横向终点位置将其分配到 5 个驾驶方向簇（直行、轻微左转、轻微右转、左转、右转）。对每个簇内的轨迹评分取平均，得到 5 路类别分布，进而计算该分布的熵：

$$
H = -\sum_{c=1}^{5} p_c \log p_c
$$

其中 $p_c$ 为簇 $c$ 内轨迹的平均评分经 softmax 归一化后的概率。高集群熵意味着模型在多个驾驶方向上同时给出了高评分，反映出决策不确定性；低集群熵则表明模型对某一方向有明确偏好。

### 测试时训练（TTT）与梯度缓冲

Centaur 在部署时通过最小化集群熵来在线更新规划器参数。具体而言，在第 $i$ 帧，计算集群熵 $H$ 对评分解码器参数 $\theta$ 的梯度 $\frac{\partial H}{\partial\theta}$，并将其存入长度为 $F=4$ 的历史梯度缓冲区。参数更新使用缓冲区内梯度的平均值：

$$
\hat{\theta}_i = \theta - \eta \left\{ \frac{\partial H}{\partial\theta} \right\}_{avg}
$$

其中 $\eta = 1\mathrm{e}{-4}$ 为学习率，仅执行一步梯度下降。更新范围限定于评分解码器，感知骨干网络保持冻结——消融实验表明这足以带来显著性能提升，同时控制计算开销。

梯度缓冲机制具有双重作用：一是通过平均历史梯度平滑更新方向，抑制单帧噪声；二是梯度计算仅依赖缓冲区中已有的历史时间步，使得梯度计算可以与当前帧的前向推理异步并行执行，从而缓解 TTT 引入的延迟。

### PDM 评分

实验采用 PDM 评分（Planning Driver Model Score）作为主要评估指标，其定义为：

$$
\mathrm{PDMS} = \mathrm{NC} \times \mathrm{DAC} \times \left( \frac{5 \mathrm{TTC} + 2 \mathrm{C} + 5 \mathrm{EP}}{12} \right)
$$

该指标综合了安全性（NC、TTC）、合规性（DAC）、舒适度（C）和通行效率（EP），是 NAVSIM 基准的官方评测标准。

### 补充图表

![[assets/figures/papers/paper_list_l80_https_arxiv_org_abs_2503_11650/figures/001_Figure_1.jpg]]
*Figure 1: Reducing entropy when uncertain with test-time training (TTT). The end-to-end planner Hydra-MDP [33], stateof-the-art on navtest [10], predicts a score for every trajectory in a fixed set. In the scatter plots, we plot trajectory scores based on their lateral endpoint position, clustered into five categories (colored arrows in the upper visualizations). Hydra-MDP selects one trajectory with the highest predicted score (★) as its output. Left: In this roundabout, it selects a high-scoring outlier in the cluster ‘slight left’ where the average score is low, indicating high uncertainty. Right: Such uncertainty is measured via our proposed Cluster Entropy, which we minimize via gradient descent...*

![[assets/figures/papers/paper_list_l80_https_arxiv_org_abs_2503_11650/figures/009_Table_5.jpg]]
*Table 5: The notation used in our paper, with descriptions*

## 实验与关键发现

### 核心实验设计

所有实验基于NAVSIM v1.1仿真环境，主指标为PDM评分（PDMS），其定义为：

$$
\mathrm{PDMS} = \mathrm{NC} \times \mathrm{DAC} \times \left( \frac{5 \mathrm{TTC} + 2 \mathrm{C} + 5 \mathrm{EP}}{12} \right)
$$

该指标综合了无责碰撞（NC）、可行驶区域合规（DAC）、时间到碰撞（TTC）、舒适度（C）和自车进度（EP）五个子维度，是端到端规划器安全性与有效性的统一度量。Centaur以**Hydra-MDP**作为基础模型，TTT过程中仅更新评分解码器，冻结感知骨干网络，采样M=100条候选轨迹，使用F=4帧历史梯度缓冲区，学习率η=1e-4执行单步梯度下降。

### 主结果：navtest基准

Table 1展示了TTT与回退层策略的核心消融。Hydra-MDP基线PDMS为90.3，引入回退层策略后PDMS骤降至65.3，根本原因在于回退层强制选择预定义的“安全”轨迹，导致自车进度（EP）子评分大幅跌至13以下，产生过度保守行为。相比之下，Centaur使用集群熵进行TTT后PDMS达到92.6，不仅未损害进度，反而在安全子评分上实现提升。使用语义熵（Hydra-SE）的TTT变体也取得91.4 PDMS，较集群熵低0.8分，验证了集群熵作为不确定性度量的优越性。

在navtest官方排行榜（Table 2）上，Centaur以92.10±0.33的平均PDMS排名第一，显著超越Hydra-MDP集成版（91.26）和其他竞争方法。值得注意的是，Hydra-MDP*使用了3模型集成，而Centaur仅为单模型，这一对比进一步凸显了TTT的有效性。

![[assets/figures/papers/paper_list_l80_https_arxiv_org_abs_2503_11650/figures/005_Table_2.jpg]]
*Table 2: navtest Leaderboard. We report the mean and std over 3 independent training runs, as recommended in the leaderboard rules. *The Hydra-MDP entry, which won the 2024 NAVSIM challenge, is a single evaluation of a 3-model ensemble, unlike all other rows*

![[assets/figures/papers/paper_list_l80_https_arxiv_org_abs_2503_11650/figures/010_Table_6.jpg]]
*Table 6: NAVSIM v1.0 comparison to state-of-the-art. Unlike the official leaderboard from Table 2 in the main paper, here we report results for models with a single training seed on the earlier NAVSIM version used for the 2024 NAVSIM Challenge. Transfuser-SE denotes equipping Transfuser with TTT and semantic entropy*

### 安全关键场景：navsafe基准

为评估边缘场景泛化能力，论文构建了navsafe安全基准（Table 4），从navtest的12,146帧中筛选出229帧，覆盖环岛、黄灯决策、无保护左转、匝道驶入/驶出、异常交通标志、超车变道、无车道区域、恶劣天气、让行等10类安全关键场景。Centaur取得74.14总体PDMS，远超Hydra-MDP（56.47）和Hydra-SE（62.84），在多数子类别上均保持领先，表明TTT能有效应对分布外场景的不确定性。

![[assets/figures/papers/paper_list_l80_https_arxiv_org_abs_2503_11650/figures/008_Table_4.jpg]]
*Table 4: navsafe PDM Scores. Existing planners fall short of human-level performance. RDBT: “Roundabout”. YLLT: “Yellow light, rush or wait?”. EXR: “Exit ramp”. UNPL: “Unprotected left”. ENR: “Enter ramp”. UNTS: “Uncommon traffic sign”. OTLC: “Overtaking with lane change”. NLA: “No lane area (e.g., parking lot)”. BWTH: “Bad weather”. YLD: “Yielding (e.g., to pedestrians)”*

### 故障识别能力

Table 3评估了集群熵作为故障预警信号的潜力。在识别Hydra-MDP将在哪些帧上发生失败的二元分类任务中，集群熵达到62.8%真阳性率（TPR）和73.6%准确率，优于语义熵和全熵等其他不确定性度量。这一结果表明集群熵不仅适用于测试时优化，还可作为部署阶段的安全监控指标。

### 消融分析

**梯度缓冲区长度**：Table 7显示F=4提供最佳PDMS，F=2性能最低，但整体对F不敏感，说明梯度平均策略具有较好的鲁棒性。使用SVD组合历史梯度（TTT*）的PDMS为91.7，低于简单平均的92.6，验证了平均操作的有效性。

**更新范围**：仅更新评分解码器即可带来显著改善，冻结感知骨干在减少计算开销的同时保持了性能提升，表明TTT主要作用于决策层的评分校准。

**跨范式泛化**：Table 6显示，在轨迹回归范式规划器**TransFuser**上应用TTT与语义熵可带来2.3 PDMS的提升，证明TTT框架对不同规划范式具有一定通用性。

**延迟开销**：Hydra-MDP推理延迟从243.9ms增至312.5ms（Table 7），但通过仅在高不确定性帧启用TTT可降低摊销延迟，且梯度计算可异步并行执行，为实际部署提供了优化空间。

### 定性分析

Figure 4展示了TTT前后的轨迹评分分布变化。在成功案例中，Centaur通过TTT抑制了异常高评分，使模型从“直行”与“微左转”之间的不确定状态偏向平均评分更高的方向，从而避免碰撞。失败案例则揭示当前方法的局限：当原始预测已经高度自信时，TTT无法有效纠正错误，表明集群熵对已收敛至错误极值的评分分布缺乏足够的扰动能力。

### 局限性

实验验证范围局限于NAVSIM仿真环境，尚未在真实车辆或闭环模拟器（如CARLA）中测试。TTT引入的额外计算开销在资源受限的嵌入式平台上可能构成部署瓶颈。集群熵依赖固定的5个驾驶方向锚点进行聚类，对于需要更细粒度行为表达的场景可能不够精确。此外，论文未探讨TTT在长期持续适应过程中的灾难性遗忘问题。

### 补充图表

![[assets/figures/papers/paper_list_l80_https_arxiv_org_abs_2503_11650/figures/004_Table_1.jpg]]
*Table 1: Impact of TTT on navtest. Introducing a fallback layer [54] leads to extremely conservative behaviors, in turn reducing PDMS. On the other hand, TTT yields significant improvements, in particular with our proposed Cluster Entropy uncertainty measure*

![[assets/figures/papers/paper_list_l80_https_arxiv_org_abs_2503_11650/figures/007_Table_3.jpg]]
*Table 3: Failure identification. Our proposed Cluster Entropy uncertainty with Hydra-MDP obtains promising results on identifying frames where the model will fail on navtest*

![[assets/figures/papers/paper_list_l80_https_arxiv_org_abs_2503_11650/figures/011_Table_7.jpg]]
*Table 7: Ablations on navtest. More results, in addition to Table 1 in the main paper. TTT∗ uses the SVD of history gradients to combine them, instead of averaging. Hydra-SEf refers to using f history frames. Hydra-SE4 denotes TTT being applied only on inference of selected frames where uncertainty is higher than a threshold (e.g. Main L383). We report amortized latency on navtest*

![[assets/figures/papers/paper_list_l80_https_arxiv_org_abs_2503_11650/figures/003_Figure_3.jpg]]
*Figure 3: navsafe. We leverage definitions of safety-critical cases from NHTSA (National Highway Traffic Safety Administration) material [41] and search through navtest for frames matching these. Following human checks, we construct navsafe. CLIP-based clustering [23] of our data alongside navtest shows that navsafe consists of frames from the peripheral regions of the distribution*

![[assets/figures/papers/paper_list_l80_https_arxiv_org_abs_2503_11650/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results. For each scene, we show the PDMS and a selected subscore for both Hydra-MDP (before TTT) and Centaur (after TTT), with the highest predicted score marked using a ★. The x-axis in each plot is the candidate trajectory’s lateral end-point position. Top: TTT helps Centaur which is uncertain between ‘Forward’ and ‘Slight Left’ to prefer the direction where cluster members have a higher average score, improving safety. Bottom: A failure case, where TTT cannot suppress a confident original prediction*

## 定位与知识库关联

### 1. 核心机制与因果杠杆

Centaur的核心杠杆在于**测试时训练**与**集群熵**的协同。传统端到端规划器在部署时面临安全性与适应性的两难：回退层策略通过预定义安全动作检测失败，但导致过度保守行为（如自车进度EP骤降至13以下，Table 1），严重损害驾驶进度；而基于显式表示与手工成本函数的测试时优化（如UniAD）依赖昂贵标注，牺牲了端到端方法的可扩展性。两者均无法通过新数据自我改进。

Centaur的解决方案是引入一种无监督的不确定性度量——集群熵，并在线最小化该度量以调整规划器行为。具体而言，从规划词汇表中采样M=100条候选轨迹，按5个驾驶方向（前向、微左、微右、左转、右转）聚类，计算5路分类熵作为不确定性信号；随后利用历史F=4帧的梯度平均值，对评分解码器执行一步梯度下降（学习率η=1e-4），冻结感知骨干网络。这一机制的核心直觉在于：**梯度平均抑制了模型在多个簇中同时分配高分的能力，从而纠正与簇内其他轨迹显著偏离的异常高分预测**（Section 2.2）。

### 2. 方法谱系定位

#### 2.1 与端到端规划范式的对比

Centaur建立在轨迹评分范式之上，其基础模型**Hydra-MDP**是navtest基准上的SOTA端到端规划器。与轨迹回归范式（如**TransFuser**）不同，评分范式输出每个候选轨迹的子评分（NC、DAC、EP、C、TTC），再聚合选择最优轨迹。Centaur的TTT机制天然适配评分范式：集群熵直接作用于评分分布，梯度更新仅需修改评分解码器。

实验表明，将TTT与语义熵结合应用于回归范式规划器TransFuser，仅带来2.3 PDMS的提升（Table 6），远低于在Hydra-MDP上的效果。这暗示TTT的增益与评分范式的输出结构紧密耦合——回归范式缺乏显式的候选评分分布，集群熵无法直接构建。

#### 2.2 与测试时优化方法的对比

与**UniAD**等采用专家成本函数进行测试时优化的方法相比，Centaur的关键差异在于**无需专家标注**。UniAD依赖手工设计的成本函数（如碰撞、偏离车道等），这些函数需要昂贵的标注和领域知识。Centaur的集群熵是纯无监督信号，仅利用规划器自身的评分输出，保持了端到端方法的可扩展性。

#### 2.3 与回退层策略的对比

回退层策略（Fallback Layer）是部署端到端规划器的常见安全机制：当不确定性超过阈值时，切换到预定义的保守轨迹。然而，如表1所示，回退层导致EP从Hydra-MDP的约83骤降至13以下，PDMS从90.3降至65.3。相比之下，TTT在提升安全子评分（TTC）的同时保持了高EP，PDMS达到92.6。这表明**TTT通过参数适应而非行为替换来提升安全性，避免了保守性-进度之间的零和博弈**。

#### 2.4 与其他基线的关系

在navtest排行榜上（Table 2），Centaur以单模型92.10±0.33 PDMS超越**Hydra-MDP***（3模型集成，91.26）、**DiffusionDrive**（扩散模型规划器）、**PARA-Drive**等基线。在更具挑战性的navsafe安全基准上（Table 4），Centaur取得74.14总体PDMS，远超Hydra-MDP（56.47）和Hydra-SE（62.84），证明TTT在边缘场景中的泛化优势。

### 3. 适用边界与局限

#### 3.1 仿真验证的局限性

Centaur的所有实验均在NAVSIM仿真环境中进行，尚未在真实车辆或闭环模拟器（如CARLA）中验证。NAVSIM提供开环评估，无法捕捉规划器决策对环境的反馈影响。闭环部署中，TTT的梯度更新可能因环境交互而产生分布偏移，效果需要进一步验证。

#### 3.2 计算开销与实时性

TTT引入额外推理延迟：Hydra-MDP基础延迟243.9ms，启用TTT后增至312.5ms（Table 7）。虽然通过异步并行（梯度计算与推理解耦）或仅在高不确定性帧启用TTT可降低开销，但在资源受限的嵌入式平台上仍可能构成瓶颈。论文未提供在典型车载计算平台上的延迟数据。

#### 3.3 集群熵的表达能力限制

集群熵依赖固定的5个驾驶方向锚点进行聚类。对于需要更细粒度驾驶行为（如精确的横向偏移、动态避让）的场景，5路分类可能丢失关键信息。论文未探讨自适应聚类或更丰富的行为表示。

#### 3.4 长期适应的未探索问题

论文未探讨TTT在长期持续部署中的影响：模型是否会因持续的单步更新而发生过拟合或灾难性遗忘？梯度缓冲区仅保留4帧历史，缺乏对更早经验的记忆机制。这些是TTT从仿真走向实际部署必须解决的问题。

### 4. 开放问题

1. **闭环扩展**：如何将Centaur的TTT扩展到闭环驾驶设置，并在实时推理中保持可承受的延迟？闭环环境中，TTT的梯度更新需要与规划-控制循环同步，异步缓冲策略可能需要重新设计。

2. **极端边缘案例**：集群熵在传感器严重噪声、罕见物体或对抗性场景下的有效性如何？navsafe基准虽覆盖10类安全关键场景，但样本量仅229帧，统计显著性有限。

3. **统一推理与适应**：能否进一步统一TTT与模型推理过程，通过权重共享或条件计算来完全消除推理时的梯度计算？例如，将集群熵作为网络内部状态的一部分进行在线估计。

4. **持续学习机制**：TTT在在线持续部署中是否会导致模型对近期数据的过拟合？如何结合记忆重放或弹性权重巩固等技术来平衡适应性与稳定性？

5. **集群熵作为策略信号**：集群熵是否可以直接用作驾驶策略更新的反馈信号，而不仅仅是测试时调整？例如，将熵值映射为探索-利用权衡的调节因子，指导规划器在不确定时主动收集信息。

## 原文 PDF

![[paperPDFs/arxiv_2025/Centaur_Robust_End_to_End_Autonomous_Driving_with_Test_Time_Training.pdf]]
