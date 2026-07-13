---
title: Recovering Physically Plausible Human-Object Interactions from Monocular Videos
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Recovering_Physically_Plausible_Human_Object_Interactions_from_Monocular_Videos.pdf
project_link: null
code_link: null
aliases:
- PGHRRASDP
- RPPHOIFMV
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 基于回滚长度的自适应采样以识别可靠帧，并结合双重（前向/后向）传播与运动学更新机制，逐步将局部物理合理状态扩散至全序列。
primary_logic: 尽管整体运动学估计噪声大，但序列中存在接触清晰、运动缓慢的可靠帧；从这些帧初始化并在仿真中回滚，通过自适应采样和迭代传播，可使策略克服噪声并学习稳定的物理交互。
claims:
- 自适应采样和双重传播机制能够从严重噪声的视觉重建中逐渐恢复整个HOI序列
- 相比运动学基线VisTracker，我们的方法在BEHAVE和InterCap上大幅提升了接触率和物理合理性指标
- 消融实验证明双重传播和运动学更新至关重要：完整方法的成功率(SR-B 51.4)远超朴素训练的11.4
- BEHAVE 上 ContRate-h ↑ = 0.89
---

# Recovering Physically Plausible Human-Object Interactions from Monocular Videos

> [!tip] 核心洞察
> 尽管整体运动学估计噪声大，但序列中存在接触清晰、运动缓慢的可靠帧；从这些帧初始化并在仿真中回滚，通过自适应采样和迭代传播，可使策略克服噪声并学习稳定的物理交互。

| 字段 | 内容 |
|------|------|
| 中文题名 | 从单目视频中恢复物理上合理的人-物交互 |
| 英文题名 | Recovering Physically Plausible Human-Object Interactions from Monocular Videos |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Huang_Recovering_Physically_Plausible_Human-Object_Interactions_from_Monocular_Videos_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Physics-Guided HOI Refinement via RL with Adaptive Sampling and Dual Propagation |
| Dataset | BEHAVE, InterCap |

> [!tip] 效果简介
> - BEHAVE 上，ContRate-h ↑ 0.89 vs 0.52 (VisTracker) (+0.37)；ObjFloat ↓ 0.10 vs 0.30 (VisTracker) (-0.20)；ObjJerk ↓ 188.5 vs 524.9 (VisTracker) (-336.4)。
> - InterCap 上，SR-B ↑ / SR-F ↑ 52.6 / 57.1 vs InterMimic (finetuned) 较低 (显著提升)。

## 概要

从单目视频中恢复人与物体交互（HOI）是理解人类行为的关键技术，但现有运动学重建方法（如 **VisTracker**，Xie et al., CVPR 2023）产生的估计往往包含严重噪声——人体漂浮、物体穿模、关节抖动等物理不合理现象普遍存在。直接将这些噪声运动学作为强化学习（RL）的模仿目标，会导致策略训练不稳定甚至完全失败：朴素RL训练在BEHAVE数据集上的成功率（SR-B）仅为11.4（Table 3）。

本文的核心洞察在于：尽管整体运动学估计质量差，但序列中仍存在接触清晰、运动缓慢的“可靠帧”。若能识别这些帧作为锚点，在物理仿真器中回滚并逐步将物理合理状态扩散至全序列，就能从噪声中恢复出物理上可信的交互。基于这一认识，作者提出了一套**物理引导的HOI精炼框架**，其核心是**基于回滚长度的自适应采样**与**双重传播-运动学更新**机制的协同工作。

具体而言，该方法采用两阶段流水线：首先利用VisTracker从单目视频重建含噪声的人-物运动学；随后在物理仿真器中训练前向与反向两个RL跟踪策略，通过自适应采样提高可靠帧的初始化概率，并利用前向/后向回滚的成功片段持续更新运动学目标，形成“传播-更新”的迭代闭环（Figure 3）。这一机制使策略能够克服视觉输入的噪声，逐步恢复完整的物理合理HOI序列。

实验结果表明，该方法在两个标准基准（BEHAVE和InterCap）上相较运动学基线VisTracker大幅提升了物理合理性指标：接触率（ContRate-h）从0.52提升至0.89，物体浮动（ObjFloat）从0.30降至0.10，物体抖动（ObjJerk）从524.9降至188.5（Table 1）。与物理基线**InterMimic**（Xu et al., CVPR 2025）相比，本方法在BEHAVE上达到SR-B 51.4 / SR-F 60.0，在InterCap上达到SR-B 52.6 / SR-F 57.1，均显著优于InterMimic的微调版本（Table 2）。消融实验进一步证实，完整的双重传播与运动学更新设计是成功的关键：去除这些组件后，成功率从51.4骤降至11.4（Table 3）。

在方法谱系上，本工作位于**单目HOI重建**与**物理仿真引导的人体运动生成**的交叉点。与纯运动学方法（如VisTracker）相比，它引入了物理约束以消除穿透与浮动；与通用物理模仿方法（如InterMimic）相比，它通过自适应采样和双重传播机制专门解决了噪声运动学下的策略学习难题。该框架目前仍受限于初始运动学重建质量，且仅支持单物体、接触动态相对简单的场景，向多物体、多人及场景感知交互的扩展是未来的重要方向。



### 单目视频人-物交互重建的物理合理性鸿沟

从单目视频中恢复人与物体的三维交互（HOI）是计算机视觉与具身智能交叉领域的核心挑战。近年来，基于运动学的方法（kinematic reconstruction）在从单目视频估计人体姿态、物体位姿以及二者联合运动方面取得了显著进展，例如 **VisTracker**（Xie et al., CVPR 2023）能够在全局坐标系中重建人-物交互序列。然而，这些运动学重建结果普遍存在严重的物理不合理性：物体漂浮（floating）、穿模（penetration）、接触抖动（jittering）等问题几乎不可避免。如 Figure 1 所示，从视频输入得到的运动学估计往往包含错误的接触配置，物体悬浮在空中或嵌入人体内部，与真实物理世界的行为严重偏离。

这种物理不合理性的根源在于，纯运动学方法仅从像素或几何约束出发进行优化，缺乏对质量、力、接触动力学等物理先验的建模。当视频中的运动模糊、遮挡或深度歧义加剧时，运动学估计的噪声会进一步放大，导致重建结果在物理仿真器中无法复现——人形机器人会摔倒、物体会飞走、接触会瞬间断裂。

### 物理仿真与强化学习结合的机遇与瓶颈

为了弥补上述鸿沟，研究者开始探索在物理仿真器中使用强化学习（RL）训练跟踪策略，使虚拟人形机器人模仿运动学参考运动，同时自动满足物理约束。这类方法（如 **InterMimic**，Xu et al., CVPR 2025）在单人运动生成和简单交互中展现了潜力：策略接收当前物理状态和未来运动学目标，输出关节力矩，仿真器根据动力学方程推进状态，从而产出物理上合理的运动序列。

然而，当将这一范式直接应用于从单目视频获得的噪声运动学重建时，一个关键瓶颈浮现：**噪声的运动学参考会直接毒化RL训练过程**。具体而言，如果策略试图模仿包含漂浮、穿模、抖动的运动学目标，它将学习到错误的行为模式，导致回滚（rollout）迅速失败——人形机器人可能在几帧内就失去平衡或失去与物体的接触。如 Table 3 所示，当使用朴素RL训练（naive RL）直接将VisTracker输出作为跟踪目标时，在BEHAVE数据集上的向后成功率（SR-B）仅为11.4，向前成功率（SR-F）仅为24.5。这意味着绝大多数序列无法被物理上合理地复现。

### 核心洞察：噪声序列中存在可靠帧

本文的核心洞察在于：尽管整体运动学估计充满噪声，但序列中并非所有帧都同样不可靠。**存在一些“可靠帧”（reliable frames）**——这些帧通常对应接触清晰、运动缓慢、遮挡较少的时刻，其运动学估计相对准确。如果策略从这些可靠帧初始化并在仿真器中回滚，它能够成功地在较长的时间窗口内维持物理合理性。相反，从噪声严重的帧（如接触模糊、快速运动、物体被遮挡的帧）初始化，回滚往往会迅速崩溃。

这一观察揭示了问题的本质不是“整个序列都无法用物理策略跟踪”，而是“噪声帧破坏了回滚的连续性”。因此，核心问题转化为：**如何自动识别可靠帧，并从这些帧出发，将物理上合理的状态逐步扩散到整个序列？**

### 本文动机与方法概览

基于上述洞察，本文提出了一种**基于自适应采样与双重传播的物理引导HOI优化框架**。该方法不假设运动学重建是准确的，也不试图在全局范围内一次性修正所有帧。相反，它采用一种迭代的“传播-更新”机制：

1. **自适应采样**：根据回滚长度自动评估每帧的可靠性，提高可靠帧被选为初始化起点的概率，使策略优先从“容易学”的状态开始训练。
2. **双重传播**：同时训练前向（forward）和反向（backward）两个策略。前向策略沿时间正序回滚，反向策略沿时间逆序回滚。二者相互补充——前向回滚的成功部分可以更新后续帧的运动学目标，反向回滚的成功部分可以修正前序帧的初始状态。
3. **运动学更新**：将仿真器产生的物理合理状态用于更新对应帧的运动学参考，使后续回滚的跟踪目标逐步从“噪声运动学”转变为“物理合理运动学”，从而打破噪声对策略训练的负反馈循环。

通过这一机制，物理合理的状态如同“涟漪”一般从可靠帧向两侧扩散，最终覆盖整个序列（Figure 3）。实验表明，该方法在BEHAVE和InterCap两个标准HOI基准上，相比运动学基线VisTracker在接触率、物体漂浮、物体抖动等物理合理性指标上取得了显著提升（Table 1），同时大幅超越了物理基线InterMimic的成功率（Table 2）。消融实验进一步验证了自适应采样、双重传播和运动学更新每个组件的关键作用（Table 3, Figure 6）。



## 核心方法与创新机理

本文提出 **Physics-Guided HOI Refinement via RL with Adaptive Sampling and Dual Propagation**，核心创新围绕一个关键瓶颈展开：单目视频的运动学重建（如 **VisTracker**，Xie et al., CVPR 2023）包含严重噪声与物理不合理性（浮动、穿模、抖动），直接用于强化学习训练会导致策略不稳定或失败。针对此，方法在三个维度上引入创新机制。

### 1. 基于回滚长度的自适应采样

传统方法采用均匀随机初始化或标准参考状态初始化（RSI），从噪声运动学帧中随机采样起始帧进行策略回滚。然而，噪声严重的帧会导致回滚快速失败，策略难以学习有效行为。

本文的创新在于**基于回滚长度的自适应采样**（Section 3.4）：策略在训练过程中记录每帧作为起点时的回滚成功长度，并据此动态调整采样概率——回滚成功越长的帧，被选为起始帧的概率越高。这等价于自动识别序列中接触清晰、运动缓慢的“可靠帧”，使策略优先从这些帧初始化并在仿真中回滚，逐步积累成功经验。该机制是后续双重传播能够有效扩散物理合理状态的基础。

### 2. 双重传播机制

传统物理跟踪方法仅训练单一前向策略，沿时间正序回滚。当序列中早期帧噪声严重时，前向策略缺乏可靠的起始点，导致整体重建失败。

本文提出**双重传播**（Section 3.5, Figure 3）：同时训练前向策略和反向策略，分别沿时间正序和逆序执行回滚。前向策略从早期可靠帧向后传播物理合理状态，反向策略从晚期可靠帧向前传播。二者相互增强——前向回滚成功段的状态为反向策略提供更好的初始化，反之亦然。通过多轮迭代，物理合理状态从稀疏的可靠帧逐渐扩散至全序列，最终实现完整的人-物交互重建。

消融实验（Table 3）证实：采用双策略实现的双重传播，其成功率远高于用单一策略实现的双向传播。

### 3. 运动学目标更新

传统RL跟踪方法始终以初始噪声运动学作为跟踪目标，策略被迫模仿不合理的参考（如无接触的抓取阶段），难以学习正确的交互行为。

本文提出**运动学目标更新**（Section 3.5）：在双重传播的每轮迭代中，用仿真生成的成功回滚段状态替换对应帧的噪声运动学估计，并将更新后的运动学同时作为后续回滚的**初始化状态**和**跟踪目标**。这意味着策略不再盲目追随原始噪声参考，而是逐步向物理上已验证的合理状态靠拢。

消融实验（Figure 6）揭示了该设计的因果作用：若仅将运动学更新用于初始化而不作为跟踪目标，策略仍需模仿噪声运动学，在物体抓取阶段因参考中缺乏接触而无法学会拾取动作；反之，当反向回滚产生的运动学更新作为跟踪目标时，策略成功学会抓取盒子并完成后续动作。完整方法（双重传播 + 运动学更新）在BEHAVE上达到 SR-B 51.4，而朴素RL训练仅获得 11.4（Table 3），差距达4.5倍。

### 创新点总结

| 创新维度 | 基线做法 | 本文做法 | 因果作用 |
|---------|---------|---------|---------|
| 采样策略 | 均匀/RSI随机初始化 | 基于回滚长度的自适应采样 | 提高可靠帧采样概率，降低噪声帧对策略的干扰 |
| 策略架构 | 单一前向策略 | 前向+反向双策略双重传播 | 从序列两端同时扩散物理合理状态，相互增强 |
| 跟踪目标 | 始终使用初始噪声运动学 | 用仿真状态持续更新运动学参考 | 策略目标从噪声逐步迁移至物理合理状态 |

三者形成闭环：自适应采样识别可靠帧 → 双重传播从可靠帧向全序列扩散 → 运动学更新将扩散结果固化为新的跟踪目标，使策略在噪声严重的视觉重建中逐步“自举”出完整的物理合理交互序列。



本文提出一种两阶段流水线，目标是从单目视频中恢复物理上合理的人-物交互（HOI）序列。核心思想是：将现成的运动学重建作为含噪声的初始化，然后在物理仿真器中通过强化学习（RL）训练跟踪策略，利用自适应采样与双重传播机制逐步纠正噪声，最终输出物理一致的交互序列。

### 两阶段流水线概览

**第一阶段：运动学重建。** 给定单目视频，使用现成的运动学重建方法 **VisTracker**（Xie et al., CVPR 2023）在全局坐标系中重建人与物体的运动。输出为 $T$ 帧的运动序列 $M = \{ \mathbf{q}_t^h, \mathbf{q}_t^o \}_{t=1}^T$，其中人体状态 $\mathbf{q}_t^h$ 包含 SMPL-H 参数（全局朝向 $\Phi_t^h$、身体姿态 $\Theta_t^h$、体型 $\beta^h$、根位移 $\Gamma_t^h$），物体状态 $\mathbf{q}_t^o$ 包含 6-DoF 位姿。然而，由于单目重建的固有歧义性，该阶段产生的运动学估计通常包含严重噪声，表现为接触不正确、物体浮动、穿透和关节抖动等问题（Figure 1, Figure 2）。

**第二阶段：物理引导的跟踪策略。** 将噪声运动学参考输入物理仿真器，训练一个基于 RL 的跟踪策略，使其在模仿参考运动的同时维持物理合理性。该阶段是本文的核心贡献所在，其关键挑战在于：直接以噪声运动学为目标进行 RL 训练会导致策略不稳定甚至完全失败（消融实验中朴素 RL 的成功率仅为 11.4）。为解决这一问题，本文引入了自适应采样与双重传播机制。

### 模块关系与数据流

流水线包含三个关键模块，其数据流与协同关系如 Figure 2 和 Figure 3 所示：

![[assets/figures/papers/paper_list_l1078_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Recovering_Physi/figures/002_Figure_2.jpg]]
*Figure 2: Overview of our two-stage pipeline. In the first stage, we use off-the-shelf kinematic reconstruction method VisTracker [44] to reconstruct human-object interactions in global coordinates from the input video, producing kinematic estimates that are often noisy. In the second stage, we train a physics-based tracking policy to imitate these reference kinematics within a simulator using reinforcement learning. At each timestep t, the policy receives the current physical state*

1. **VisTracker 运动学重建**（上游模块）：从视频生成含噪声的初始人与物体运动序列，作为后续物理跟踪的参考目标。该模块的输出质量直接影响整个流水线的上限。

2. **MDP 物理跟踪策略**（核心执行模块）：将 HOI 跟踪建模为马尔可夫决策过程。在每个时间步 $t$，策略接收当前物理状态 $s_t^s$ 和一组未来运动学参考状态编码 $s_t^g = \{ \hat{s}_{t,t+k} \}_{k \in \mathbf{K}}$（编码了人体姿态差异、物体位姿差异、距离差异及接触差异），输出关节动作 $a_t$ 驱动仿真器中的人形机器人向运动学目标靠近。奖励函数为五项子奖励的乘积：
   $$\mathbf{r}_t = \mathbf{r}_t^{\mathrm{h}} \cdot \mathbf{r}_t^{\mathrm{o}} \cdot \mathbf{r}_t^{\mathrm{c}} \cdot \mathbf{r}_t^{\mathrm{d}} \cdot \mathbf{r}_t^{\mathrm{e}}$$
   分别对应人体姿态、物体位姿、接触状态、人-物距离和能量消耗，每项均采用指数形式 $\exp(-\lambda E)$ 以鼓励精确跟踪。

3. **自适应采样与双重传播系统**（迭代优化模块）：这是克服噪声运动学的核心机制。其工作流程为：
   - **自适应采样**：基于回滚长度识别序列中的可靠帧（如接触清晰、运动缓慢的帧），提高这些帧被选为初始化起点的概率，而非均匀随机采样。
   - **双重传播**：同时训练前向策略和反向策略。前向策略从可靠帧向前回滚，反向策略从可靠帧向后回滚，两者相互增强，将物理合理状态逐步扩散到整个序列。
   - **运动学更新**：将成功回滚片段生成的物理状态用于更新对应帧的运动学参考。后续迭代的回滚从更新后的更优质状态初始化，并以此为跟踪目标，使策略逐渐摆脱原始噪声的影响。

通过多轮“传播-更新”循环，物理合理状态从可靠帧向全序列扩散，最终恢复整个 HOI 序列（Figure 3）。这一设计使策略能够从极度噪声的视觉重建中学习，并在整个序列上输出物理上合理的人-物交互。

### 补充图表

![[assets/figures/papers/paper_list_l1078_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Recovering_Physi/figures/001_Figure_1.jpg]]
*Figure 1: Physically plausible reconstruction of human-object interactions from monocular video. Given an input video, we start from a noisy kinematic reconstruction (e.g., incorrect contact, floating objects, etc). Then, we optimize a policy for this sequence that can rollout a physically plausible version of the observed interaction*



### 两阶段流水线概览

本方法采用两阶段流水线（Figure 2）：第一阶段利用现成的运动学重建方法 **VisTracker**（Xie et al., CVPR 2023）从单目视频中恢复全局坐标系下的人-物运动序列；第二阶段在物理仿真器中训练基于强化学习的物理跟踪策略，以模仿这些参考运动学，同时维持物理合理性。

第一阶段输出的重建运动表示为：

$$M = \{ \mathbf{q}_t^h, \mathbf{q}_t^o \}_{t=1}^T$$

其中人体状态参数 $\mathbf{q}_t^h = \{ \Phi_t^h, \Theta_t^h, \beta^h, \Gamma_t^h \}$ 包含SMPL-H模型的全局朝向、身体姿态、形状参数和根平移；$\mathbf{q}_t^o$ 为物体6D位姿。该运动学估计通常包含严重噪声——浮动、穿模、抖动等现象普遍存在（Section 3.1）。

### 物理跟踪MDP

第二阶段将HOI跟踪形式化为马尔可夫决策过程（MDP），包含状态空间、动作空间、仿真器驱动的转移动力学和奖励函数（Section 3.3）。策略在每一时间步 $t$ 观察状态 $\mathbf{s}_t = \{ s_t^s, s_t^g \}$，其中 $s_t^s$ 为当前物理状态，$s_t^g$ 为未来运动学参考相对于当前状态的编码：

$$s_t^g = \big\{ \hat{s}_{t,t+k} \big\}_{k \in \mathbf{K}}$$

该编码包含人体关节旋转差异 $\hat{\theta}_{t+k}^h \ominus \theta_t^h$、人体位置差异 $\hat{p}_{t+k}^h - p_t^h$、物体旋转与位置差异、人-物距离差异以及参考接触状态等（Eq. 1）。策略据此输出动作 $a_t$，驱动人体模型向运动学目标靠近。

### 奖励函数设计

总奖励定义为五项子奖励的乘积形式（Eq. 2）：

$$\mathbf{r}_t = \mathbf{r}_t^{\mathrm{h}} * \mathbf{r}_t^{\mathrm{o}} * \mathbf{r}_t^{\mathrm{c}} * \mathbf{r}_t^{\mathrm{d}} * \mathbf{r}_t^{\mathrm{e}}$$

每项均为指数形式 $\exp(-\lambda E)$，分别对应：
- **人体项** $\mathbf{r}_t^{\mathrm{h}}$：惩罚关节旋转、位置和速度与参考的偏差；
- **物体项** $\mathbf{r}_t^{\mathrm{o}}$：惩罚物体旋转、位置和速度偏差；
- **接触项** $\mathbf{r}_t^{\mathrm{c}}$：对齐实际接触状态 $c_t$ 与参考 $\hat{c}_t$，并惩罚物体接触点与其配对手部关节之间的距离；
- **距离项** $\mathbf{r}_t^{\mathrm{d}}$：最小化人-物接近度偏差 $\lVert d_t - \hat{d}_t \rVert$；
- **能量项** $\mathbf{r}_t^{\mathrm{e}}$：惩罚关节力矩，鼓励节能运动。

乘积形式的奖励结构意味着任何一项严重偏离都会导致整体奖励急剧下降，从而强制策略在所有维度上同时满足约束（Section 3.3）。

### 自适应采样与双重传播机制

这是本方法的核心创新模块（Figure 3, Section 3.4-3.5）。运动学估计整体噪声大，但序列中存在接触清晰、运动缓慢的**可靠帧**。核心思路是：从这些可靠帧初始化回滚，利用仿真中的物理合理性逐步扩散到全序列。

![[assets/figures/papers/paper_list_l1078_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Recovering_Physi/figures/003_Figure_3.jpg]]
*Figure 3: Overview of our dual propagation with kinematics update mechanism. Kinematic estimates from monocular videos are often highly noisy. Rollouts initialized from these noisy states typically fail quickly, whereas rollouts that start from frames with accurate contact configurations succeed for much longer. To propagate these physically plausible states across the sequence, we train two HOI tracking policies simultaneously: a forward policy that performs forward rollouts and a backward policy that performs backward rollouts. States from the successful portions of previous rollouts are used to update the corresponding noisy kinematic frames, and subsequent rollouts initialize from these improved...*

**自适应采样**：不同于均匀随机初始化，本方法基于回滚长度动态调整各帧的采样概率——回滚成功距离越远的帧，其被选中作为下一轮初始化的概率越高。这使策略训练集中于能够产生有效信号的帧。

**双重传播**：同时训练前向策略和反向策略，分别执行前向和反向回滚。前轮回滚中成功部分生成的物理合理状态，用于**更新**对应帧的噪声运动学估计；后续回滚则从这些改进后的状态初始化。通过多轮迭代的“传播-更新”循环，物理合理状态逐渐覆盖整个序列，最终两条策略均能重建完整的物理一致HOI序列。

**运动学更新**的关键在于：更新后的运动学不仅用作下一轮回滚的初始化，还**同时作为跟踪目标**。消融实验证实，若仅用于初始化而不更新跟踪目标，策略仍试图模仿原始噪声运动学，性能显著下降（Table 3, Figure 6）。



## 实验与关键发现

### 主结果：与运动学基线的定量比较

我们在 BEHAVE 和 InterCap 两个标准 HOI 数据集上，与运动学重建方法 **VisTracker**（Xie et al., CVPR 2023）进行了全面比较。VisTracker 同时也是本方法第一阶段的初始化来源。结果如 Table 1 所示，核心发现如下：

![[assets/figures/papers/paper_list_l1078_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Recovering_Physi/figures/004_Table_1.jpg]]
*Table 1: Quantitative comparison with kinematics-based approaches on the BEHAVE and InterCap datasets. We compare against the state-of-the-art VisTracker [44], which also serves as the initialization for our method. While our approach introduces a slight degradation in the 3D accuracy metrics (CD), it consistently achieves substantial improvements on all interaction-related and physics-aware metrics. All results are reported using the sequences of frames that our physical tracker successfully rolls out. Please refer to the SuppleMat for these successful frames of the sequences*

**物理合理性指标的显著提升。** 在 BEHAVE 数据集上，我们的方法将人手接触率（ContRate-h）从 0.52 提升至 **0.89**（+0.37），物体漂浮程度（ObjFloat）从 0.30 降至 **0.10**（-0.20），物体抖动（ObjJerk）从 524.9 降至 **188.5**（-336.4）。InterCap 数据集上同样观察到一致且大幅的改善趋势。

**3D 精度指标的轻微退化。** 作为物理合理性提升的代价，Chamfer Distance（CD）指标出现了约 1.4 cm 的轻微退化。这一权衡在预期之内：运动学方法可以自由优化 3D 位置精度，而物理仿真器施加的接触约束与动力学一致性要求必然限制姿态空间，导致纯几何精度的小幅下降。但考虑到接触率、漂浮、穿透等交互质量指标的巨幅提升，这一代价是可接受的。

**定性对比。** Figure 4 展示了典型场景的可视化对比。VisTracker 的重建结果中，人手与物体之间存在明显的悬空间隙（接触漂浮），或人手穿透物体内部（穿透）。我们的方法通过物理仿真约束，成功消除了这些物理不合理现象，使人与物体的接触关系符合真实物理规律。

> **注意：** Table 1 中的所有指标均在物理跟踪器成功回滚的帧序列上报告，未成功回滚的帧不计入统计。这确保了比较的公平性，但也意味着指标反映的是方法在“可物理实现”帧上的表现，而非全序列覆盖率的绝对指标。

### 主结果：与物理基线的定量比较

我们将本方法与物理仿真基线 **InterMimic**（Xu et al., CVPR 2025）在两种使用模式下进行比较：(1) 直接推理模式（预训练策略直接应用于目标序列）；(2) 微调模式（在目标序列上进一步训练）。所有方法均以 VisTracker 的运动学估计作为初始化。结果如 Table 2 所示。

![[assets/figures/papers/paper_list_l1078_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Recovering_Physi/figures/006_Table_2.jpg]]
*Table 2: Quantitative comparison with physics-based approaches on the BEHAVE and InterCap datasets. We compare with the state-of-the-art InterMimic [48] approach, when it is used for direct inference, as well as when it is finetuned. All approaches are initialized using the VisTracker [44] estimate. Given the low success rate for the direct inference version of InterMimic, we do not report 3D metrics (i.e., CD and Contact metrics) for it. Also, these 3D metrics are evaluated on the intersection of successful frames of InterMimic (finetune) and our method. Interestingly, our approach outperforms both baselines in the large majority of metrics. Please refer to the SuppMat for the intersection of succe...*

**成功率指标。** 在 BEHAVE 数据集上，我们的方法取得了 SR-B **51.4** / SR-F **60.0** 的成功率；在 InterCap 上为 SR-B **52.6** / SR-F **57.1**。相比之下，InterMimic（微调）在两个数据集上的成功率均显著低于我们的方法。InterMimic（直接推理）的成功率过低，以至于无法报告有意义的 3D 指标。

**3D 精度指标。** 在二者成功帧的交集上评估 CD 和接触指标时，我们的方法在大多数指标上同样优于 InterMimic（微调）。这表明我们的方法不仅在“能否完成”上更优，在“完成质量”上也更具竞争力。

**定性对比。** Figure 5 揭示了 InterMimic 的典型失败模式：(1) 序列早期阶段缺乏接触，导致策略无法恢复正确的接触配置；(2) 策略陷入一种不自然的接触姿态，虽然能部分完成序列，但与视频中的真实交互不匹配。我们的方法通过自适应采样和双重传播机制，能够从噪声视觉输入中逐步恢复完整的物理合理接触序列。

> **公平性说明：** 与 InterMimic 的 3D 指标（CD、Contact）在二者成功帧的交集上计算，避免了因覆盖率差异导致的偏差。

### 消融实验：双重传播与运动学更新的关键作用

Table 3 在 BEHAVE 数据集上系统消融了本方法的三个核心设计组件。完整方法（双重传播 + 运动学更新作为跟踪目标）达到 SR-B **51.4** / SR-F **60.0**。

![[assets/figures/papers/paper_list_l1078_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Recovering_Physi/figures/008_Table_3.jpg]]
*Table 3: Ablation study for key design choices of our approach. Success rates are reported on BEHAVE. (✓) for “Kinematic Updates”: kinematics are updated for initialization only, but not as tracking targets. (✓) for “Dual Propagation”: dual propagation is implemented with a single policy instead of two*

**朴素 RL 训练的严重失败。** 如果直接从 VisTracker 的噪声运动学初始化并训练（无双重传播、无运动学更新），SR-B 仅为 **11.4**，SR-F 为 **24.5**。这验证了核心瓶颈：单目视频的运动学估计包含严重的浮动、穿模和抖动噪声，直接作为 RL 模仿目标会导致策略不稳定或完全失败。

**运动学更新作为跟踪目标的关键性。** 当运动学更新仅用于初始化、但不作为跟踪目标时（即策略仍追踪原始噪声运动学），性能显著下降。Figure 6 的定性结果直观展示了这一现象：在“拿起盒子”场景中，原始运动学在拾取阶段缺乏人-物接触，若策略追踪该噪声目标，则无法学会抓取动作。而当反向传播产生的运动学更新作为跟踪目标时，策略成功学会了抓取盒子并完成后续动作。

**双重传播的双策略优势。** 若用单一策略实现双重传播（而非分别训练前向和反向策略），成功率大幅下降。这验证了前向/反向双策略设计的必要性：两个方向的回滚任务在物理动力学上具有不同的挑战，共享单一策略难以同时掌握两个方向的控制能力。

### 失败模式与局限性

尽管本方法在物理合理性上取得了显著提升，但仍存在以下局限：

1. **对初始运动学质量的依赖。** 两阶段流水线的上限受限于 VisTracker 的 4D 重建质量。当运动学估计出现严重错误（如完全错误的人-物对应关系、大范围遮挡导致的姿态崩溃）时，物理优化阶段可能无法完全纠正。此时自适应采样可能找不到足够的可靠帧作为传播锚点。

2. **交互复杂度的限制。** 当前方法仅支持每序列单一物体且接触动态相对简单的交互场景。尚未扩展到多物体、多人、复杂接触（如手指级精细操作）或场景感知的 HOI 场景。在这些复杂场景中，接触检测、奖励设计和传播策略均需要非平凡的扩展。

3. **CD 指标的轻微退化。** 如 Table 1 所示，物理合理性提升以轻微牺牲 3D 几何精度为代价。对于某些对几何精度要求极高的应用（如精确的动作捕捉复现），这一权衡可能需要进一步优化。

### 补充图表

![[assets/figures/papers/paper_list_l1078_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Recovering_Physi/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative comparison with the kinematics-based method [44]. Our method successfully resolves the issues of contact floating and penetration present in the baseline, producing physically plausible human-object interaction reconstructions*

![[assets/figures/papers/paper_list_l1078_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Recovering_Physi/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative comparison with InterMimic [48]. InterMimic often struggles to recover the correct contact configuration, due to lack of contact in the early phase of the sequence (left) or committing to an unnatural contact pose that allows partial completion but does not match the interaction in the video (right). In contrast, our method reconstructs the full sequence with physically plausible contact. These improvements stem from our adaptive sampling and dual propagation with kinematics update, which enable the policy to overcome noisy visual inputs and maintain realistic interaction dynamics*

![[assets/figures/papers/paper_list_l1078_https_openaccess_thecvf_com_content_CVPR2026_html_Huang_Recovering_Physi/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative results from the ablation study. Without using the kinematic update as the tracking target, the policy attempts to imitate the noisy kinematic states, making it difficult to learn how to pick up the box, since there is no human-object contact during the pickup phase (second frame). In contrast, when the kinematic update from the backward rollouts is used as the tracking target, the policy successfully learns to grasp the box and complete the subsequent actions*



## 定位与知识库关联

### 1. 与运动学重建基线的关系

本工作的直接上游是单目视频的全身人-物交互运动学重建方法，核心基线为 **VisTracker**（Xie et al., CVPR 2023）。VisTracker 从单目视频中估计人体 SMPL-H 参数与物体 6-DoF 位姿，输出全局坐标系下的运动序列 $M = \{ \mathbf{q}_t^h, \mathbf{q}_t^o \}_{t=1}^T$。然而，这类纯运动学方法缺乏物理约束，导致输出存在三类典型失效模式：**接触浮动**（手与物体之间存在间隙）、**穿模**（手或身体穿透物体）、**物体抖动**（物体轨迹高频振荡）。本文方法以 VisTracker 输出为初始化，在第二阶段引入物理仿真与强化学习策略，将运动学估计转化为物理合理的结果。

本工作与 VisTracker 构成**互补而非替代**关系：第一阶段运动学重建的质量直接影响后续物理优化的上限，当运动学估计严重错误时（如完全丢失接触或物体位姿严重偏离），物理优化可能无法完全纠正。这一依赖关系构成了方法的核心适用边界。

### 2. 与物理仿真基线的关系

在物理合理的人-物交互生成方向上，**InterMimic**（Xu et al., CVPR 2025）是当前最先进的方法。InterMimic 通过强化学习训练通用 HOI 模仿策略，能够从运动学参考中生成物理仿真结果。

本文与 InterMimic 的关键差异体现在三个维度：

- **问题设定**：InterMimic 面向通用策略训练，期望策略在推理时泛化到新序列；本文针对**单序列优化**，为每条输入视频专门微调策略，以克服噪声运动学带来的训练困难。
- **噪声鲁棒性**：InterMimic 直接推理（direct inference）时，面对 VisTracker 的噪声运动学几乎无法成功回滚；即使对目标序列微调，其成功率也显著低于本文方法。根本原因在于 InterMimic 缺乏针对噪声运动学的专门处理机制——当序列早期缺乏接触或存在错误接触配置时，策略难以恢复正确的交互模式（见 Figure 5）。
- **机制差异**：本文的自适应采样与双重传播机制使策略能够从序列中的可靠帧逐步扩展物理合理状态，而 InterMimic 的均匀初始化策略在面对全局噪声时缺乏这种渐进式恢复能力。

定量对比（Table 2）显示，本文方法在 BEHAVE 上达到 SR-B 51.4 / SR-F 60.0，在 InterCap 上达到 SR-B 52.6 / SR-F 57.1，均显著优于 InterMimic 微调版本。

### 3. 方法谱系中的定位与贡献

从方法谱系角度看，本文处于**运动学重建**与**物理仿真策略**的交汇点，核心贡献在于提出了一套**噪声运动学条件下的物理合理化机制**，而非重新设计运动学重建或通用策略架构。

具体而言，本文的创新集中在三个可插拔的设计槽位：

| 设计槽位 | 基线做法 | 本文做法 | 证据锚点 |
|---------|---------|---------|---------|
| 采样策略 | 均匀随机初始化或标准 RSI | 基于回滚长度的自适应采样，提高可靠帧的采样概率 | Section 3.4 |
| 运动学目标更新 | 始终使用初始噪声运动学作为跟踪目标 | 用仿真生成的状态持续更新运动学参考，并支持双重传播 | Section 3.5 |
| 策略架构 | 单一前向策略 | 同时训练前向和反向策略，实现相互增强的双重传播 | Section 3.5, Figure 3 |

消融实验（Table 3）验证了这些设计的必要性：完整方法（双重传播 + 运动学更新）在 BEHAVE 上达到 SR-B 51.4 / SR-F 60.0，而朴素 RL 训练仅获得 11.4 / 24.5。值得注意的是，若运动学更新仅用于初始化而不作为跟踪目标，性能显著下降——策略被迫模仿噪声状态，在接触缺失阶段无法学习正确的抓取动作（Figure 6）。

### 4. 适用边界与局限

本方法的适用边界受以下因素制约：

- **上游依赖**：两阶段流水线受限于初始 4D 重建质量。当 VisTracker 的输出存在系统性错误（如物体类别识别错误导致错误的接触先验）时，物理优化难以弥补。
- **交互复杂度**：目前仅支持每序列单一物体且接触动态较简单的交互（如拿起、放下、搬运），尚未扩展到多物体、多人、复杂接触切换或场景感知的 HOI 场景。
- **计算开销**：每序列需独立训练前向与反向策略，推理效率低于通用策略的直接推理模式。论文未报告单序列优化所需的训练时间，这一点需要手动验证。
- **评估偏差**：所有指标基于物理跟踪器成功回滚的帧序列报告（Table 1 注释），这意味着在策略完全失败的帧上方法无输出，实际端到端可用性受限于成功率。

### 5. 开放问题

论文提出了两个值得关注的开放方向：

1. **端到端视频到动力学系统**：能否直接从像素联合推断几何与物理约束，替代当前的两阶段流水线？这需要解决视觉特征与物理状态表示的对齐问题，以及端到端训练中仿真器不可微的挑战。
2. **泛化到复杂交互场景**：如何将自适应采样与双重传播机制推广到多物体、多人交互，以及更动态的接触模式（如传递、抛接）？这涉及状态空间扩展、多智能体策略协调以及接触图建模等子问题。



## 原文 PDF

![[paperPDFs/CVPR_2026/Recovering_Physically_Plausible_Human_Object_Interactions_from_Monocular_Videos.pdf]]
