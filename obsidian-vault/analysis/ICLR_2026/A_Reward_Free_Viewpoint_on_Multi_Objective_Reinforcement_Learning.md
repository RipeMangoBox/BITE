---
title: "A Reward-Free Viewpoint on Multi-Objective Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/A_Reward_Free_Viewpoint_on_Multi_Objective_Reinforcement_Learning.pdf
project_link: https://rl-bandits-lab.github.io/MORL-FB/
code_link: null
aliases:
- MFFBMORL
- RFVMORL
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过引入无奖励强化学习的训练目标作为辅助任务，具体包括偏好引导的潜在向量探索（PG-Explore）、基于小批量采样的辅助任务构建，以及基于观测奖励向量的辅助 Q 损失。"
primary_logic: "RFRL 自然地学习了一组比 MORL 所需更广的策略，这可以作为结构化辅助任务来提升泛化性和样本效率，但需要偏好引导的探索才能在实践中发挥效用。"
claims:
- "在 MO-Gymnasium 的 6 个连续控制任务上，MORL-FB 的 Utility (UT) 和 Hypervolume (HV) 指标均达到最优或接近最优，且 Episodic Dominance (ED) 始终低于 0.5，表明其在大多数偏好下优于所有基准方法。"
- "MORL-FB 在聚合指标 IQM、中位数和均值上以较大优势优于现有方法，证实了其性能提升。"
- "移除辅助 Q 损失导致 Ant3d 和 Humanoid2d 上 UT 变为负值，证实该损失对表示学习至关重要。"
- "移除偏好引导探索导致性能大幅下降，在 Ant3d 上 UT 从 3.43 降至 1.23。"
---

# A Reward-Free Viewpoint on Multi-Objective Reinforcement Learning

> [!tip] 核心洞察
> RFRL 自然地学习了一组比 MORL 所需更广的策略，这可以作为结构化辅助任务来提升泛化性和样本效率，但需要偏好引导的探索才能在实践中发挥效用。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 多目标强化学习的无奖励视角 |
| 英文题名 | A Reward-Free Viewpoint on Multi-Objective Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=IwiwmY3Mzz) · [Project](https://rl-bandits-lab.github.io/MORL-FB/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | MORL-FB (Forward-Backward Multi-Objective Reinforcement Learning) |
| Dataset | HalfCheetah2d, Hopper3d, Ant3d, Humanoid2d |

> [!tip] 效果简介
> - HalfCheetah2d 上，UT (×10^3) 为 7.69 ± 0.08，对比 6.85 ± 0.01 (Q-Pensieve)，变化 +0.84。
> - Hopper3d 上，UT (×10^3) 为 2.36 ± 0.01，对比 1.82 ± 0.02 (Q-Pensieve)，变化 +0.54。
> - Ant3d 上，UT (×10^3) 为 3.43 ± 0.22，对比 1.81 ± 0.08 (Q-Pensieve)，变化 +1.62。

## 概要

多目标强化学习（MORL）的核心挑战在于，测试时所需的用户偏好往往未知且多样，而传统基于偏好条件化的方法难以在维持样本效率的同时有效泛化到未见的偏好组合。与此同时，标准无奖励探索策略（如从标准正态分布采样潜在向量 $z$）并未针对多目标奖励结构进行对齐，导致探索集中于无关区域，无法为 MORL 提供有效的行为多样性。本文从无奖励强化学习（RFRL）的视角切入，提出一种名为 MORL‑FB（Forward‑Backward Multi‑Objective Reinforcement Learning）的方法，其核心思路是将 RFRL 的训练目标作为辅助任务嵌入 MORL 框架，借助偏好引导的潜在向量探索（PG‑Explore）与直接利用观测奖励向量的辅助 Q 损失，促使模型在训练中自然地学得更广泛且更具相关性的策略表示，从而在不额外增加环境交互的前提下同步提升泛化性和样本效率。

在 MO‑Gymnasium 的 6 个连续控制任务上，MORL‑FB 在 Utility（UT）、Hypervolume（HV）和 Episodic Dominance（ED）三项关键指标上均达到最优或接近最优：UT 和 HV 以显著优势超越 PD‑MORL、Q‑Pensieve、CAPQL 等十余种基准方法，且 ED 始终低于 0.5，表明在绝大部分偏好下其表现优于所有基准。聚合性能（中位数、均值、IQM）同样呈现一致的大幅领先。即使训练时仅暴露少数基础偏好向量（标准基向量与均匀分布偏好），MORL‑FB 仍能保持强大的泛化能力，而 PD‑MORL 和 Q‑Pensieve 的性能则明显退化。消融实验进一步揭示，移除辅助 Q 损失会使部分任务的 UT 跌至负值，偏好引导探索的移除则导致关键任务上 UT 下降超过 50%，证实了这两个组件的不可或缺性。此外，MORL‑FB 仅需 3M 总环境步数即可达到或超越单目标 SAC 在 21 个偏好向量上总计 63M 步数所获得的帕累托前沿，样本效率提升约一个数量级；在 Hopper 系列环境上的零样本跨目标迁移实验也验证了其表示的可迁移性。这些结果共同表明，将 RFRL 的结构化探索与多目标奖励信息有机结合的辅助任务设计，能够有效突破传统 MORL 在偏好泛化与样本利用上的根本瓶颈。



多目标强化学习（Multi-Objective Reinforcement Learning, MORL）的核心是训练能够同时优化多个可能冲突目标的策略。在实际应用中，不同用户或场景下目标的相对重要性（即**偏好向量** $\lambda$）往往在训练时未知，且测试时可能覆盖整个偏好空间。一个典型的做法是依靠**线性标量化** $f_{\lambda}(\mathbf{r}) = \lambda^{\top} \mathbf{r}$ 将多维奖励压缩为标量，然后学习一个偏好条件化的策略，最大化期望折扣回报向量 $\mathbf{V}^{\pi} := \mathbb{E}_{\pi, s_0 \sim \mu}[\sum_{t=0}^{\infty} \gamma^t \mathbf{R}(s_t, a_t)]$。挑战在于：当训练资源有限时，策略必须在大量未知偏好上同时保持高回报（**泛化能力**）和高样本效率。

现有方法可大致分为两类。**单策略条件化方法**（如 PD‑MORL、Q‑Pensieve、CAPQL、Envelope Q‑Learning）直接在训练偏好分布上优化标量化目标，但在偏好集合缩小或测试偏好显著偏离训练分布时，泛化能力急剧下降（Figure 4, Table 24）。**多策略方法**（如 PG‑MORL、MORL/D、GPI‑LS）通过显式维护多个策略来覆盖帕累托前沿，虽然解集更完整，但计算与样本开销随目标数量增长，难以扩展到高维连续控制。一个被忽视的缺口是**无奖励强化学习（Reward‑Free RL, RFRL）**与 MORL 之间的深层联系：RFRL 方法（如 Forward‑Backward 分解，FB）训练时不依赖具体奖励函数，学到的策略集天然比 MORL 所需的更宽泛，理论上可作为结构化辅助任务提升 MORL 的泛化与样本效率。然而，直接将原始 FB 框架（例如从标准正态分布 $\mathcal{N}(0,I)$ 采样潜在向量 $z$）应用于 MORL 会导致**探索与奖励结构脱节**——采样的 $z$ 大多远离实际多目标标量奖励所对应的低维子空间，使得训练信号稀疏，策略无法高效覆盖有效偏好区域（Vanilla FB 在所有连续控制任务上性能极差，Table 26；动机实验图1 中标准正态采样对应的回报向量分布单一且与偏好无关）。

上述瓶颈的根源在于 RFRL 的探索机制并未考虑 MORL 中的偏好-奖励结构：标量化后的奖励仅由偏好向量的 $d$ 维线性组合决定，对应的潜在向量 $z_{\lambda} = \mathbf{H}\lambda$ 被约束在一个 $d$ 维子空间内（Eq. 4），这使得无引导的随机 $z$ 采样大量浪费在无关区域，导致样本效率低下。消融实验明确指出：若去掉偏好引导探索，Ant3d 任务的效用指标（UT）从 3.43 骤降至 1.23；彻底移除辅助 Q 损失则使 UT 变为负值（Table 25, Table 17），证实这两项设计对表示学习至关重要。

本文的核心动机正源于此：**从无奖励 RL 的视角重新审视 MORL**，将 RFRL 的前向‑后向（FB）训练目标作为辅助任务，同时引入**偏好引导的潜在向量探索（PG‑Explore）**与**基于观测奖励向量的辅助 Q 损失**，迫使学到的表示和探索行为聚焦于与多目标标量奖励相关的状态‑动作区域。该方法旨在突破现有单策略方法泛化差、多策略方法成本高的困境，在显著提升样本效率（仅需 3M 总步数即可达到单目标 SAC 在 21 个偏好上训练 63M 步的帕累托前沿水平，Figure 20）的同时，实现对未见偏好的鲁棒泛化。



## 核心方法与创新机理

传统的多目标强化学习（MORL）方法（如 PD-MORL、Q-Pensieve）的通用范式是：策略以用户偏好 $\lambda$ 为条件，直接优化标量化奖励 $\lambda^\top \mathbf{r}$。这一范式在训练偏好覆盖不足时泛化能力受限，且未能利用无奖励强化学习（RFRL）天然蕴含的结构化辅助任务。MORL-FB 从 RFRL 视角出发，对训练范式引入了三项关键改变，构成本工作相对于所有基线（包括原始 FB）的核心创新：

| 创新维度 | 基线做法 | MORL-FB 的改变 | 因果机制 | 决定性证据 |
|:---|:---|:---|:---|:---|
| **训练范式** | 策略以 $\lambda$ 为条件直接优化标量化回报 | 将 RFRL 的 FB 后继测度学习作为辅助任务，学习一组比单一 MORL 更广的策略（Section 3） | 利用 RFRL 对任意奖励函数的零样本泛化能力，为 MORL 提供结构化知识共享 | 原始 FB（$z\sim\mathcal{N}(0,I)$）在所有任务上表现极差（Table 26），证明仅靠无监督 RFRL 不足，必须与后两项创新结合 |
| **潜在向量 $z$ 采样** | 从标准正态分布 $\mathcal{N}(0,I)$ 采样（FB）或直接采用线性映射 $z_\lambda = \mathbf{H}\lambda$ | 在小批量数据上构造 $\hat{z}_\lambda = \sum \mathbf{B}_\omega(s,a)\mathbf{r}^\top\lambda/n_s$ 并归一化（Algorithm 1, Section 3.1） | 突破 $z_\lambda$ 仅位于 $d$ 维子空间的限制，将探索导向多目标相关区域；产生多模态度量分布，增加策略多样性 | 移除 PG‑Explore（改用 $\mathcal{N}(0,I)$）使 Ant3d 的 Utility 从 **3.43** 降至 **1.23**（Table 25）；t‑SNE 显示学到的 $z$ 呈多模态而非单模态（Figure 5） |
| **Q 学习损失** | 仅使用标量化奖励（或 FB 伪奖励）的 TD 误差 | 增加辅助 Q 损失 $\mathcal{L}_Q$，以观测奖励向量 $\mathbf{r}$ 和 $\lambda$ 监督 $\mathbf{F}_\theta(s,a,z_\lambda)^\top z_\lambda$（Equation 6） | 利用原始多目标信号直接监督前向表示，强化了状态‑动作表征的有效性 | 移除辅助 Q 损失导致 Ant3d 的 Utility 变为负值（‑1.53），Hypervolume 几乎归零（Table 25, Table 17）；Humanoid2d 的 Utility 亦降为负值 |

### 1. 范式转变：以 RFRL 辅助任务替代直接偏好条件化

基线单策略方法（如 PD-MORL、Q-Pensieve）仅在训练时对已知偏好进行优化，其策略 π(s, λ) 的泛化完全依赖神经网络的外推，缺乏对未知偏好的结构化适应性。MORL-FB 则引入 Forward-Backward（FB）分解（Equation 1–3），将后继测度学习作为辅助任务：前向网络 $\mathbf{F}_\theta(s,a,z)$ 与后向网络 $\mathbf{B}_\omega(s,a)$ 共同逼近一族最优策略，覆盖比任何单一 MORL 目标更广的标量奖励函数（Section 3.1）。这一范式的核心优势在于，RFRL 框架天然具备对新奖励函数的零样本泛化能力，但前提是需要偏好相关的探索来激活与多目标相关的策略区域——这正是后续两项创新的动机。

### 2. 偏好引导的潜在向量探索（PG‑Explore）

基线方法（包括原始 FB）从标准正态分布采样 $z$，无法将探索集中在多目标回报相关的状态区域。MORL-FB 的关键改变是：在算法循环中，对每个采样到的偏好 $\lambda$，利用当前回放缓存的 $n_s$ 个转移样本构造 $\hat{z}_\lambda = \sum \mathbf{B}_\omega(s,a)\mathbf{r}^\top\lambda/n_s$，并归一化作为策略执行用的潜在向量（Algorithm 1）。这一设计使得 $z$ 的分布与偏好方向和当前经验分布相适应，同时打破了 $z_\lambda = \mathbf{H}\lambda$ 被限制在 $d$ 维子空间的局限（Equation 4 及分析）。消融实验证实，移除此机制后性能大幅衰退（Table 25），t-SNE 可视化更直接表明学到的 $z$ 分布呈丰富多模态（Figure 5），证明 PG‑Explore 是使 RFRL 在 MORL 中生效的必要纽带。

### 3. 基于观测奖励向量的辅助 Q 损失

基线方法仅对标量化奖励（或 FB 伪奖励）计算 TD 误差，没有显式利用观测到的向量奖励来约束表示学习。MORL-FB 在标准 Measure Loss（Equation 5）之上，增加了辅助 Q 损失 $\mathcal{L}_Q$，以真实奖励向量 $\mathbf{r}$ 和偏好 $\lambda$ 计算 TD 目标，直接监督前向网络预测值 $\mathbf{F}_\theta(s,a,z_\lambda)^\top z_\lambda$（Equation 6）。该损失促使表示网络不仅学习后继测度的几何结构，还学习与多目标奖励一致的值函数结构。消融实验表明，移除该损失后 Ant3d 和 Humanoid2d 的 Utility 均跌至负值（Table 25），证实该组件对表示学习至关重要；同时系数 $\alpha_Q$ 在 0.25–2 范围内性能稳健（Table 18），说明其易于调优。

上述三项创新共同构成 **MORL‑FB** 的核心技术贡献。在 MO‑Gymnasium 的 6 个连续控制任务上，MORL‑FB 在所有指标（UT, HV, ED）上均达到最优或接近最优（Figure 2），聚合指标 IQM 和 CVaR@0.1 同样领先（Figure 3, Table 21）；在仅训练少量偏好时仍保持优越的泛化能力（Figure 4）；仅需 3M 步即可实现单目标 SAC 在 21 个偏好下总计 63M 步的帕累托前沿（Figure 20）。这些结果充分验证了 RFRL 视角下三项改变的有效性，且所有证据均来自贝叶斯超参数优化下的公平对比，结论可靠。



![[assets/figures/papers/repair_max_IwiwmY3Mzz_Reward_Free_MORL/figures/001_Figure_1.jpg]]
*Figure 1: A motivating experiment on Deep Sea Treasure. (a)(b) Training performance (UT and HV defined in the sequel) of MORL-FB under different batch sizes for $\hat { z } _ { \lambda }$ . (c) KDE contour of return vector distributions of $\pi ( \cdot$ , z ) induced by $\hat { z } _ { \lambda }$ (with various batch sizes b) and $\hat { z } \sim \mathcal { N }$ ( 0 , $\mathbb { T } ^ { d _ { z } }$ ) This shows that $\hat { z } _ { \lambda }$ corresponds to learning for more diverse and relevant behavior in MORL than $z _ { \lambda }$ and the z sampling strategy of the original FB. The detailed configuration is provided in Appendix C

MORL-FB 在范式层面将多目标强化学习重新定位为**无奖励强化学习（RFRL）的一个特例**，并通过逐模块改造使原始 FB 框架适配于多目标场景。其核心思路是：将 RFRL 中“学习一组覆盖不同奖励函数的策略”这一能力作为**辅助任务**，注入到面向用户偏好的 MORL 训练中，从而在不牺牲样本效率的前提下提升跨偏好泛化。

### 模块组成与连接关系

整个 pipeline 由以下关键模块构成，其关系与数据流见 Figure 1 及相关训练算法：

1. **前向表示网络 $\mathbf{F}_{\theta}(s, a, z)$**  
   接受状态 $s$、动作 $a$ 与潜在向量 $z$，输出 $d_z$ 维向量，用于近似后继测度。通过该表示，任意由 $z$ 编码的标量化奖励函数对应的最优 Q 值可分解为内积：
   
$$
Q(s, a, z) = \mathbf{F}_{\theta}(s, a, z)^{\top} z .
   \tag{1}
$$

2. **后向表示网络 $\mathbf{B}_{\omega}(s, a)$（或仅依赖状态）**  
   编码奖励函数的表征。对任意奖励函数 $R$，其对应的潜在向量 $z_R$ 定义为
   
$$
z_R = \mathbb{E}_{(s,a) \sim \mathcal{D}} \left[ \mathbf{B}_{\omega}(s,a) \, R(s,a) \right],
   \tag{2}
$$

   从而将奖励函数映射为低维向量。在多目标设定下，偏好向量 $\lambda$ 的线性标量化奖励对应的 $z_{\lambda}$ 落在 $d$ 维子空间内，导致探索不足（式 (4)）。

3. **偏好引导探索（PG-Explore）**  
   针对 $z_{\lambda}$ 分布局限的问题，MORL-FB 采用**小批量采样**构造探索性潜在向量：
   
$$
\hat{z}_{\lambda} = \sum_{(s,a,\mathbf{r},s') \in \mathcal{D}} \frac{\mathbf{B}_{\omega}(s,a) \, \mathbf{r}^{\top} \lambda}{n_s}.
   \tag{5}
$$

   该向量通过对回放缓存中随机采样的转移元组使用观测奖励向量 $\mathbf{r}$ 加权求和得到，并经归一化后作为条件输入。相比于标准正态采样，$\hat{z}_{\lambda}$ 将探索引导至与多目标奖励相关的状态区域，从而产生更具多样性和相关性的策略行为（Figure 1, 5）。  

4. **策略网络 $\pi(s, z)$**  
   根据状态 $s$ 和潜在向量 $z$ 输出动作分布。训练时，策略由 $\mathbf{F}_{\theta}$ 与 $z$ 的内积引导：
   
$$
\pi(s, z) = \arg\max_a \mathbf{F}_{\theta}(s,a,z)^{\top} z .
   \tag{3}
$$

5. **度量损失 $\mathcal{L}_{\mathrm{M}}$**  
   基于后继测度的贝尔曼残差训练前向与后向网络：
   
$$
\mathcal{L}_{\mathrm{M}}(\mathbf{F}_{\theta}, \mathbf{B}_{\omega}; z) = \mathbb{E} \big[ (\mathbf{F}_{\theta}(s,a,z)^{\top}\mathbf{B}_{\omega}(s',a') - \gamma \mathbf{F}_{\bar{\theta}}(s',\pi(s',z),z)^{\top}\mathbf{B}_{\bar{\omega}}(s',a'))^2 \big] - 2\mathbb{E} \big[ \mathbf{F}_{\theta}(s,a,z)^{\top}\mathbf{B}_{\omega}(s',a') \big],
   \tag{6}
$$

   该损失强制 $\mathbf{F}$ 与 $\mathbf{B}$ 的乘积近似后继测度。

6. **辅助 Q 损失 $\mathcal{L}_{Q}$**  
   直接利用**观测奖励向量** $\mathbf{r}$ 与偏好 $\lambda$ 计算 TD 误差，为表示学习提供额外监督：
   
$$
\mathcal{L}_{Q}(\mathbf{F}_{\theta}; z) = \mathbb{E} \big[ (\mathbf{F}_{\theta}(s,a,z)^{\top}z - (\lambda^{\top}\mathbf{r} + \gamma \mathbf{F}_{\bar{\theta}}(s',\pi(s',z),z)^{\top}z))^2 \big].
   \tag{7}
$$

   消融实验表明，移除该损失会导致严重性能退化（表 17、25），证实其对表示学习不可或缺。

### 训练与推理的数据流

- **训练阶段**  
  1. 从均匀分布或偏好超曲面采样偏好向量 $\lambda$；  
  2. 从经验回放缓存 $\mathcal{D}$ 中抽取小批量数据；  
  3. 利用 PG-Explore 构建潜在向量 $\hat{z}_{\lambda}$（同时可混合标准 $z_{\lambda}$ 以保证稳定性）；  
  4. 以 $\hat{z}_{\lambda}$ 为输入，计算度量损失 $\mathcal{L}_{\mathrm{M}}$ 与辅助 Q 损失 $\mathcal{L}_{Q}$，更新 $\mathbf{F}_{\theta}$、$\mathbf{B}_{\omega}$ 和策略 $\pi$；  
  5. 策略与环境交互，将转移 $(s, a, \mathbf{r}, s')$ 存入回放缓存。  

- **测试阶段**  
  给定用户偏好 $\lambda$，可直接通过式 (2) 计算 $z_{\lambda}$ 或使用训练时学到的映射 $\mathbf{B}_{\omega}$ 构造，再通过策略 $\pi(\cdot, z_{\lambda})$ 输出动作，无需额外训练。

### 关键机制与证据

该框架的成功依赖于三个因果耦合：
- **偏好引导探索**将 $z$ 的分布从退化子空间扩展为多模态结构，为策略提供多样的辅助任务（Figure 5）；  
- **辅助 Q 损失**使表示学习能够直接利用奖励向量的监督信号，弥补纯度量损失的不足；  
- **FB 分解**本身提供了零样本泛化能力，而上述两项改进使其在多目标任务上充分释放（图 4 显示即使在极有限偏好训练集下泛化依然稳健）。

需要注意的是，原始 FB（即不加偏好引导、无辅助损失的 Vanilla RFRL）在所有连续控制任务上表现极为低迷，进一步佐证了上述改进的必要性（表 26，FB 行）。



MORL‑FB 将多目标 RL 视作 RFRL 的一个特例，并通过前向‑后向（FB）框架同时学习一组面向不同标量化奖励的最优策略。其核心模块包含两个表示网络、一个偏好引导的潜在向量探索机制以及两个彼此协同的损失函数。

### 前向与后向表示
FB 框架将后继测度分解为前向表示 $\mathbf{F}_{\theta}(s,a,z)$ 与后向表示 $\mathbf{B}_{\omega}(s,a)$ 的内积。给定偏好的潜在编码 $z_R$，最优 Q 函数可表示为

$$
Q(s,a,z_R)=\mathbf{F}_{\theta}(s,a,z_R)^{\top}z_R \tag{1}
$$

其中 $z_R$ 由奖励函数 $R$ 经由后向表示在经验分布 $\mathcal{D}$ 上的期望定义：

$$
z_R=\mathbb{E}_{(s,a)\sim\mathcal{D}}\big[\mathbf{B}_{\omega}(s,a)\,R(s,a)\big] \tag{2}
$$

策略 $\pi$ 则通过最大化该内积选取动作：

$$
\pi(s,z_R)=\arg\max_a \mathbf{F}_{\theta}(s,a,z_R)^{\top}z_R \tag{3}
$$

在多目标场景下，标量化奖励为 $\lambda^{\top}\mathbf{r}$，对应的 $z_{\lambda}$ 事实上位于一个 $d$ 维线性子空间中：

$$
z_{\lambda}=\mathbf{H}\lambda,\qquad \mathbf{H}=\mathbb{E}\big[\mathbf{B}_{\omega}(s,a)\,\mathbf{R}(s,a)^{\top}\big] \tag{4}
$$

该线性结构导致 $z_{\lambda}$ 被束缚在偏好无关的列向量张成的空间内，严重限制了探索范围。

### 偏好引导探索 (PG‑Explore)
为突破上述线性约束，MORL‑FB 引入基于小批量采样的偏好引导探索。对每个训练步骤采样的偏好 $\lambda$，从回放缓存 $\mathcal{D}$ 中抽取一批经验，按下式构造 $\hat{z}_{\lambda}$：

$$
\hat{z}_{\lambda}= \frac{1}{n_s}\sum_{(s,a,\mathbf{r},s')\in\mathcal{D}} \mathbf{B}_{\omega}(s,a)\,\mathbf{r}^{\top}\lambda
$$

该构造中的 $\mathbf{r}^{\top}\lambda$ 项通过逐样本乘积而非期望方式引入随机性，使 $\hat{z}_{\lambda}$ 偏离严格的线性子空间，从而在训练中诱发出比原始 FB 更丰富、多模态的潜在向量的分布。消融实验表明，移除该机制后，Ant3d 上的效用 (UT) 从 3.43 跌落至 1.23，证实了偏好引导探索的有效性。

### 测度损失与辅助 Q 损失
FB 框架的训练依赖两类损失。**测度损失** $\mathcal{L}_{\mathrm{M}}$ 最小化后继测度上的贝尔曼残差，驱动 $\mathbf{F}_{\theta}$ 与 $\mathbf{B}_{\omega}$ 学习奖励‑策略无关的动力学表征：

$$
\begin{aligned}
\mathcal{L}_{\mathrm{M}}(\mathbf{F}_{\theta},\mathbf{B}_{\omega};z_{\lambda})
&=\mathbb{E}_{(s_t,a_t,s_{t+1})\sim\mathcal{D}}\Big[\big(\mathbf{F}_{\theta}(s_t,a_t,z_{\lambda})^{\top}\mathbf{B}_{\omega}(s',a')\\
&\quad - \gamma\mathbf{F}_{\bar{\theta}}(s_{t+1},\pi(s_{t+1},z_{\lambda}),z_{\lambda})^{\top}\mathbf{B}_{\bar{\omega}}(s',a')\big)^2\Big] \\
&\quad -2\mathbb{E}_{(s_t,a_t,s_{t+1})\sim\mathcal{D}}\Big[\mathbf{F}_{\theta}(s_t,a_t,z_{\lambda})^{\top}\mathbf{B}_{\omega}(s_{t+1},a_{t+1})\Big]
\end{aligned} \tag{5}
$$

其中 $\bar{\theta},\bar{\omega}$ 为目标网络参数，$(s',a')$ 为从 $\mathcal{D}$ 中独立采样的状态‑动作对。

**辅助 Q 损失** $\mathcal{L}_{Q}$ 则直接利用观测到的奖励向量 $\mathbf{r}$，构造标量化 TD 误差：

$$
\mathcal{L}_{Q}(\mathbf{F}_{\theta};z_{\lambda}) = \mathbb{E}_{(s,a,\mathbf{r},s')\sim\mathcal{D}}\Big[\big(\mathbf{F}_{\theta}(s,a,z_{\lambda})^{\top}z_{\lambda} - (\lambda^{\top}\mathbf{r} + \gamma\mathbf{F}_{\bar{\theta}}(s',\pi(s',z_{\lambda}),z_{\lambda})^{\top}z_{\lambda})\big)^2\Big] \tag{6}
$$

该损失将 $z_{\lambda}$ 作为键值，迫使 $\mathbf{F}_{\theta}$ 主动编码与多目标标量回报相关的信息。消融实验证实，移除 $\mathcal{L}_{Q}$ 后，Ant3d 和 Humanoid2d 上的效用变为负值，超体积近乎为零，说明辅助 Q 损失对表示学习不可或缺。$\mathcal{L}_{Q}$ 的系数 $\alpha_{Q}$ 在 0.25 至 2 之间敏感性低，进一步表明其易于调参。

### 策略网络
最终策略 $\pi$ 接收当前状态 $s$ 与潜在向量 $z$，输出动作分布，如式 (3) 所示。不同于传统 MORL 直接条件化于偏好向量 $\lambda$，MORL‑FB 的策略条件于由整个奖励函数 $R$ 编码的 $z$，从而实现了跨偏好和跨任务目标的泛化与零样本迁移。

通过上述模块的组合，MORL‑FB 将 RFRL 的辅助任务原则注入多目标 RL，以偏好引导探索破除线性约束，并借助辅助 Q 损失强化表征学习，最终在样本效率与泛化能力上取得显著提升。



## 实验与关键发现

本节基于 MO-Gymnasium 中的 6 个连续控制任务（HalfCheetah2d、Hopper3d、Ant3d、Humanoid2d、Humanoid5d 等）对 MORL-FB 进行系统评估。所有算法均经贝叶斯超参数优化，在 3M 环境步数、5 个随机种子的统一协议下训练与评估（Table 26）。评估指标包括 Utility（UT，偏好平均标量化回报）、Hypervolume（HV）与 Episodic Dominance（ED），并采用与 Agarwal et al. (2021) 和 Fu et al. (2020) 一致的归一化方式。

![[assets/figures/papers/repair_max_IwiwmY3Mzz_Reward_Free_MORL/figures/047_Table_26.jpg]]

### 综合性能对比

MORL-FB 在所有任务上均取得最优或接近最优的 **UT** 和 **HV**，且 **ED** 始终低于 0.5，表明其在绝大多数偏好下优于 12 个基线方法（Figure 2，Table 26）。具体而言，在 HalfCheetah2d 上，UT 达到 $7.69 \times 10^3$，比第二名 Q‑Pensieve 高出 $0.84 \times 10^3$；在更具挑战的 Humanoid5d 上，UT 比 GPI‑LS 高 $3.51 \times 10^3$。聚合指标进一步强化了这一优势：中位数、均值和四分位数均值（IQM）均显著领先于所有基准，说明性能增益具有跨任务一致性（Figure 3）。

![[assets/figures/papers/repair_max_IwiwmY3Mzz_Reward_Free_MORL/figures/002_Figure_2.jpg]]
*Figure 2: Evaluation of MORL-FB and several MORL benchmark algorithms on diverse continuous control tasks within the MO-Gymnasium suite, assessing performance using key metrics. These results demonstrate the clear advantage of MORL-FB across all tested benchmarks*

![[assets/figures/papers/repair_max_IwiwmY3Mzz_Reward_Free_MORL/figures/003_Figure_3.jpg]]
*Figure 3: Evaluation of MORL-FB and several MORL benchmark algorithms using aggregate metrics, including median, mean, and interquartile mean (IQM). These results show the superior performance of MORL-FB across all metrics*

**样本效率** 方面，MORL-FB 仅需 3M 总步数即可获得与单目标 SAC 在 21 个偏好向量上总计 63M 步数相当甚至更优的帕累托前沿（Figure 20，Section D.10）。这一结果直接源于 RFRL 框架提供的辅助任务与偏好引导探索：潜在向量 $z$ 不再被限制在 $d$ 个线性子空间，而是通过小批量采样构造 $\hat{z}_\lambda$（Equation (4)），使策略学习能够覆盖比标准 MORL 更广泛的回报分布，从而同时提升泛化性与数据效率。

![[assets/figures/papers/repair_max_IwiwmY3Mzz_Reward_Free_MORL/figures/041_Figure_20.jpg]]
*Figure 20: Return vectors (Moving Speed vs. Energy Cost) achieved under 21 different preference vectors [0, 1], [0.05, 0.95], . . . , [0.95, 0.05], [1, 0] across different methods. Each scatter cloud corresponds to the learned policies under a specific preference, illustrating how MORL methods adapt to diverse trade-offs between objectives*

**泛化能力** ：当训练偏好仅保留基向量与少量均匀采样时，PD‑MORL 和 Q‑Pensieve 的性能大幅衰退，而 MORL-FB 的 UT 和 HV 几乎保持稳定，证明其学到的策略集在偏好空间内具有更强的插值与外推能力（Figure 4，Table 24）。

**鲁棒性** ：在最坏情况偏好（CVaR@0.1）下，MORL-FB 在 HalfCheetah2d 和 Walker2d 上均取得最高得分，说明它不仅能适应平均偏好，对尾部风险也更具抵抗力（Table 21）。

### 消融实验

为量化各设计模块的因果贡献，我们对三个关键组件进行了消融（Table 25，Figure 6）：

![[assets/figures/papers/repair_max_IwiwmY3Mzz_Reward_Free_MORL/figures/046_Table_25.jpg]]
*Table 25: Performance comparison of MORL-FB and its ablated versions across environments. This table evaluates MORL-FB against variants lacking preference-guided exploration or the Q-loss component, showing their performance across different environments*

- **辅助 Q 损失** ：移除该损失 $\mathcal{L}_Q$（Equation (6)）后，在 Ant3d 上 UT 从 3.43 骤降至 $-1.53$，HV 几乎归零；在 Humanoid2d 上也出现 UT 转负的现象。这证实 $\mathcal{L}_Q$ 对前向/后向表示的学习至关重要——它直接利用观测奖励向量构建 TD 目标，迫使 $F_\theta(s,a,z)^\top z$ 与真实标量回报对齐，否则表示会严重退化。
- **偏好引导探索（PG‑Explore）** ：用标准正态分布采样 $z$ 替代 PG‑Explore 后，Ant3d 的 UT 从 3.43 跌至 1.23，性能与原始 FB（RFRL）相当。可视化分析（Figure 5）显示，PG‑Explore 使学习到的 $z$ 分布呈现多模态，覆盖与多目标奖励相关的多样区域；而原始 FB 的 $z$ 分布呈单峰，无法有效探索除随机区域外的策略空间，导致样本效率极低（Table 26 中 FB 行）。
- **Q 损失系数 $\alpha_Q$** ：在 0.25 至 2 范围内，性能波动很小，表明该方法对辅助损失权重具有低敏感性（Table 18）。

综上，PG‑Explore 与辅助 Q 损失是 MORL-FB 获得优越性能的**双重必要条件**：前者提供结构化的任务多样性，后者将这些多样性任务转化为可靠的表示学习信号。

### 失败模式与局限

尽管 MORL-FB 在主流基准上表现突出，但仍存在可识别的不足：

1. **稀疏/复杂奖励环境** ：目前的偏好引导探索依赖于小批量采样构造 $z$，当环境奖励极其稀疏或动态复杂时，该采样策略可能仍无法有效覆盖关键状态区域，探索效率会显著下降。这暗示需结合更专门的探索机制（如内在奖励或计数式探索）。
2. **线性标量化假设** ：当前框架基于偏好向量的线性加权，虽已展示向非线性扩展的可能性（Equation (4) 的推广），但尚未在需要非线性偏好聚合（如凸包或排序型偏好）的任务上验证。迁移至此类场景可能导致表示萎缩或策略退化。
3. **计算开销** ：MORL-FB 的训练成本介于轻量级单策略方法与重量级多策略方法之间，在大规模环境（如高维连续控制或长序列规划）中仍有优化空间，尤其是批量采样与 $z$ 归一化步骤引入的额外算力消耗。

这些局限同时也是未来工作的方向，例如将其他 RFRL 技术（如基于距离保持的状态表示）整合至 MORL 中，以进一步释放无奖励视角的潜力。



## 定位与知识库关联

### 方法谱系：从 RFRL 到 MORL 的首次系统性嫁接

MORL-FB 首次将无奖励强化学习（Reward-Free RL, RFRL）的目标函数作为辅助任务引入多目标强化学习（MORL），建立了两个长期独立发展领域的直接联系。其核心洞察在于：RFRL 方法天然地学习了一组比单一线性标量奖励更宽广的最优策略集合，该集合恰好可以作为 MORL 的结构化辅助任务，从而提升策略在未知偏好下的泛化与样本效率。与传统 MORL 策略不同，MORL-FB 并非直接优化偏好条件化的标量奖励，而是借由 Forward-Backward (FB) 分解学习后继测度（successor measure）的压缩表示 $F_\theta(s,a,z)$ 与 $B_\omega(s,a)$（见公式 (1)~(3)）。这一表示一旦习得，即可零样本获得任意线性标量化偏好下的最优 Q 函数 $Q(s,a,z_\lambda)=F_\theta(s,a,z_\lambda)^\top z_\lambda$，从而绕开了为每个偏好重新训练的困境。该方法处于**单策略偏好条件化方法**与**表示驱动的多策略方法**的交界点：它仅维护单一策略网络 $\pi(s,z)$，却因 $z$ 可编码多样化的奖励函数而具备类似多策略方法的覆盖能力。

### 与基准方法的关键差异及优势来源

本文与 12 种代表性基准方法进行了系统比较，覆盖了单策略偏好条件化、多策略分解、广义策略改进等不同设计路线。MORL‑FB 的实质改进集中在三个“因果旋钮”上，这些组件在消融实验中被证实为性能提升的必要条件。

**1. 训练范式：从直接标量化转向 RFRL 辅助目标。**  
传统单策略方法（PD‑MORL、Q‑Pensieve、CAPQL、EQL、PCN）直接以 $\lambda^\top r$ 或伪奖励作为优化目标，其策略在训练时仅暴露于有限偏好，测试时对未见偏好泛化差。MORL‑FB 将 FB 框架的测度损失（公式 (5)）作为主目标，额外增加基于观测奖励向量的辅助 Q 损失（公式 (6)）。测度损失强制表示 $F$ 与 $B$ 遵守后继测度的贝尔曼方程，从而使 $z$ 空间能够编码任意线性奖励，而非仅训练时见过的 $\lambda$ 集合。移除辅助 Q 损失后，Ant3d 上的 Utility (UT) 从 3.43 降为负值，超体积 (HV) 几乎归零（Table 25, Table 17），证实该损失对表示学习不可或缺。

**2. 潜在向量 $z$ 的采样：从无结构噪声到偏好引导探索。**  
原始 FB 从标准正态分布采样 $z$，在 MORL 场景下完全无法优先探索与多目标奖励相关的状态区域（Table 26 中 FB 行性能极差）。PD‑MORL 等使用 $z_\lambda = \mathbf{H}\lambda$（公式 (4)），其位于 $d$ 维线性子空间内，多样性严重不足。MORL‑FB 提出的 PG‑Explore 通过小批量采样构造 $\hat{z}_\lambda = \sum \mathbf{B}_\omega(s,a) \mathbf{r}^\top \lambda / n_s$（Algorithm 1），使 $z$ 脱离 $\mathbf{H}$ 的列空间，产生与偏好相关的多模态分布（Figure 5 的 t‑SNE 可视化证实了多模态 vs. 单模态的差异）。在 Ant3d 上，仅将 PG‑Explore 替换为标准正态采样便使 UT 从 3.43 暴跌至 1.23（Table 25），反映出引导探索是释放 RFRL 辅助任务效用的关键机制。

**3. Q 损失的结构：从单纯依赖 FB 内积到纳入实际奖励向量。**  
多数基准方法不直接使用观测奖励向量 $\mathbf{r}$（Q‑Pensieve 仅用其标量化值）。MORL‑FB 辅助 Q 损失强制 $F_\theta(s,a,z_\lambda)^\top z_\lambda$ 匹配 $\lambda^\top \mathbf{r} + \gamma V(s')$，从而将真实奖励信号注入表示学习，缓解了 FB 框架的预测误差累积。该损失系数在 $[0.25, 2]$ 范围内性能稳定（Table 18），说明模块设计具有良好的鲁棒性。

### 适用边界：在何时、何处 MORL‑FB 有效

MORL‑FB 在 MO‑Gymnasium 的 6 个连续控制基准上展现了显著优势（UT、HV 最优或接近最优，Episodic Dominance 始终低于 0.5，Figure 2/Table 26），但其有效性受以下假设与条件约束：

1. **线性标量化偏好假设。**  
   方法的核心数学建立在线性标量化之上（$f_\lambda(\mathbf{r}) = \lambda^\top \mathbf{r}$），因为 $z_\lambda$ 的线性结构（$\mathbf{z}_\lambda = \mathbf{H}\lambda$）以及策略贪婪化直接依赖该内积。当用户真实偏好为非线性（如切比雪夫或超体积标量化）时，习得的 $z$ 空间不再保证覆盖最优策略，论文仅定性讨论了向非线性扩展的可能性，尚未在复杂非线性任务上验证。

2. **环境奖励向量可观测。**  
   PG‑Explore 和辅助 Q 损失均直接要求从环境中获得完整的奖励向量 $\mathbf{r}$（见 Algorithm 1 及公式 (6)）。若环境仅提供标量化奖励或稀疏终局奖励，该方法无法直接部署。这点限制了其在许多传统 RL 基准（如 OpenAI Gym 中的标量奖励环境）上的零样本迁移。

3. **探索在稀疏奖励环境下可能不足。**  
   偏好引导探索虽较标准正态采样大幅改善，但在奖励稀疏或目标间冲突剧烈的环境中，小批量采样构建的 $\hat{z}_\lambda$ 可能仍无法覆盖关键区域。论文明确指出“需要更专门化的探索策略”，且未在如 Maze、Hybrid Reward 等极端稀疏任务上测试。

4. **计算开销介于轻量与重量方法之间。**  
   MORL‑FB 需同步训练 Forward/Backward 网络、策略网络及温度参数，并在每步插入 $z$ 构造与双重损失计算。虽然总环境步数仅 3M 即可达到单目标 SAC 在 21 个偏好上总计 63M 步的帕累托前沿（Figure 20, 附录 D.10），其墙上时钟时间仍高于 EQL 等轻量方法，在大规模（如高维状态、更多目标）场景下的扩展性尚未评估。

### 局限与开放问题

论文明确列出了当前方法的局限，并指出了几个值得深入探索的方向：

**已知局限：**
- 当前探索策略在复杂/稀疏奖励环境中可能不足，更专门的探索机制（如基于好奇心或信息增益）有必要整合。
- 尚未在非线性标量化任务上进行系统性实验，无法断言 FB 框架可直接迁移。
- 训练流程的计算开销虽然在可接受范围，但在超大规模环境中仍有优化空间。

**开放问题：**
- **非线性标量化扩展。** 如何在不牺牲表示线性结构的前提下，使 $z$ 空间能够覆盖非线性标量化的最优策略？一种可能的路径是学习 $z$ 的非线性组合函数，或引入条件变分推断。
- **集成其他 RFRL 方法。** 除 FB 外，后继测度学习、距保持状态表示（distance-preserving state representations）等 RFRL 技术能否提供更丰富的辅助任务？MORL‑FB 的成功范式为这类移植提供了路线图。
- **跨设置泛化。** 在部分可观测（POMDP）、多智能体或多目标环境中，偏好引导的 $z$ 表示能否维持其泛化能力？初步的零样本跨目标数量迁移实验（Hopper2d → Hopper3d/4d，Figure 7）已展现了潜力，但更广泛的设置仍有待检验。
- **自适应偏好探索。** 当前 PG‑Explore 使用固定的均匀 $ \lambda$ 采样分布，面对动态变化的用户偏好或主动学习场景，设计能在线调整采样分布的元策略将是一重要方向。

总体而言，MORL-FB 在方法谱系中开辟了“以 RFRL 作为 MORL 辅助任务”的新路径，通过偏好引导探索和辅助 Q 损失破解了原始 RFRL 方法在 MORL 下的失效问题，但其当前边界清晰——线性、全观测、相对稠密奖励的连续控制任务。上述局限与开放问题构成了未来沿该路线深化 RFRL-for-MORL 图谱的核心议题。



## 原文 PDF

![[paperPDFs/ICLR_2026/A_Reward_Free_Viewpoint_on_Multi_Objective_Reinforcement_Learning.pdf]]
