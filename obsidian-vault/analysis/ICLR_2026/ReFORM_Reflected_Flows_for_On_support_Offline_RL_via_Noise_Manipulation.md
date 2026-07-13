---
title: "ReFORM: Reflected Flows for On-support Offline RL via Noise Manipulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/ReFORM_Reflected_Flows_for_On_support_Offline_RL_via_Noise_Manipulation.pdf
project_link: https://mit-realm.github.io/reform/
code_link: null
openreview_forum_id: YvFsyRReeN
aliases:
- ReFORM
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "ReFORM将有界源分布BC流策略与反射流噪声生成器复合，以构造性约束离线RL动作支持集。"
primary_logic: "先学习从有界噪声到行为动作的BC流，再在源空间内反射优化噪声分布以最大化Q值。"
claims:
- "支持集约束通过策略结构保证，而不是依赖KL或Wasserstein等显式保守正则。"
- "有界源分布和反射流确保优化后策略仍处于BC策略支持集内。"
- "ReFORM在OGBench和D4RL任务上以统一超参数取得强离线RL性能。"
---

# ReFORM: Reflected Flows for On-support Offline RL via Noise Manipulation

> [!tip] 核心洞察
> ReFORM

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | ReFORM: Reflected Flows for On-support Offline RL via Noise Manipulation |
| 英文题名 | ReFORM: Reflected Flows for On-support Offline RL via Noise Manipulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=YvFsyRReeN) · [Project](https://mit-realm.github.io/reform/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method |  |
| Dataset | |

> [!tip] 效果简介
> 结果与证据沿用下文“实验与关键发现”中的现有记录；本轮不新增或外推论文事实。

## 概要

离线强化学习（Offline RL）的核心瓶颈在于分布外（OOD）动作引发的价值函数过高估计——当学习策略偏离行为策略的支持集时，Q函数对未见动作的评估不可靠，导致策略崩溃。现有方法多通过统计距离正则化（如KL散度、Wasserstein距离）约束策略与行为策略的偏离，但这在抑制OOD的同时也限制了策略改进的上限。

ReFORM提出了一种**结构性支持约束**方案：将策略构造为行为克隆（BC）流策略与反射流噪声生成器的组合。BC流策略从有界源分布 $q_{\text{BC}} = \mathcal{U}(B_l^d)$ 学习到数据分布 $p_{\text{BC}}$ 的映射；噪声生成器在BC策略的源分布支持集内生成多模态噪声，通过反射流技术确保 $\operatorname{supp}(\tilde{q}_{\text{BC}}) \subseteq \operatorname{supp}(q_{\text{BC}})$。这一设计使得最终策略的支持集天然落在行为策略支持集内，**无需显式正则化即可避免OOD问题**，同时保留了策略的多模态表达能力。

在40个OG-Bench任务（覆盖antmaze导航、cube/sence操作，含CLEAN和NOISY两类数据集）上，ReFORM以恒定超参数在所有基线中取得主导性优势，性能剖面曲线全面优于IFQL、FQL（S/M/L）及DSRL等基于流模型的离线RL方法。消融实验表明，有界源分布与反射流噪声生成器是性能增益的关键组件，且方法对超参数 $l$（源分布半径）不敏感。



离线强化学习（Offline RL）的核心挑战在于分布偏移：从静态数据集中学习的策略，在部署时可能选择数据覆盖范围之外的动作（Out-of-Distribution, OOD），导致价值函数过高估计和灾难性策略崩溃。现有的主流解决方案——无论是显式约束策略与行为策略的KL散度，还是隐式地对价值函数施加悲观惩罚——本质上都在**限制策略改进的幅度**，以换取安全性。这种“保守主义”虽然降低了OOD风险，却也给策略性能设定了天花板：当行为策略本身是次优的，保守方法难以超越数据集中已观察到的动作分布。

更棘手的是**多模态行为数据**。现实离线数据往往包含多种完成任务的策略（例如绕行左侧或右侧），要求策略能够捕捉并选择性地利用这些多模态。扩散模型和流模型等生成式策略虽然擅长表达复杂多模态分布，但它们与保守约束的结合并不自然——约束过紧会抹平多模态，约束过松则OOD依然存在。现有工作（如DSRL、FQL）试图在生成式策略上施加行为正则化，但始终面临一个根本性矛盾：**OOD抑制与策略改进之间存在不可消除的张力**。

本文的动机正是打破这种张力。核心洞察是：如果能让策略**天然地**只在行为策略的支持集（support）内采样，那么OOD问题就从优化约束变成了结构保证——无需牺牲策略改进即可获得安全性。这引出了一个关键问题：能否设计一种策略架构，使其**通过构造**满足支持约束？



## 核心方法与创新机理

ReFORM 的核心创新在于**通过构造实现支持约束（support constraint by construction）**，从根本上规避离线强化学习中的分布外（OOD）动作问题，而无需引入限制策略改进强度的显式正则化项。

### 问题瓶颈与因果开关

离线 RL 的核心瓶颈在于：当学习到的策略在评估时采样到数据集中未覆盖的 OOD 动作时，Q 函数会给出不可靠的估计值，导致策略优化走向错误方向。现有方法通常通过统计距离正则化（KL 散度、Wasserstein 距离等）将学习策略拉向行为策略 $\pi_\beta$，但这在限制 OOD 的同时也约束了策略改进的上限。

ReFORM 识别的**因果开关**是：OOD 问题的根源不在于策略偏离行为策略的密度中心，而在于策略的支持集（support）超出了行为策略的支持集。只要保证 $\text{supp}(\pi_\theta(\cdot|s)) \subseteq \text{supp}(\pi_\beta(\cdot|s))$，策略就可以在支持集内自由地选择高 Q 值动作，包括行为策略密度极低的区域。

### 核心洞察：两阶段流式策略的组合构造

ReFORM 的核心洞察是将策略构造为**噪声生成器与 BC 流式策略的复合函数**：

$$\pi_\theta(a|s) = \psi_{\theta_1}\big(\psi_{\theta_2}(w; s); s\big), \quad w \sim \mathcal{U}(\mathcal{B}_l^d)$$

其中：
- **第一阶段（BC 流式策略 $\psi_{\theta_1}$）**：通过流匹配（flow matching）从有界均匀分布 $q_{\text{BC}} = \mathcal{U}(\mathcal{B}_l^d)$（$d$ 维超球内的均匀分布）变换到近似行为策略的目标分布 $p_{\text{BC}}(\cdot|s)$。选择有界支持集作为源分布是关键——它使得支持集近似成为可能。
- **第二阶段（反射流噪声生成器 $\psi_{\theta_2}$）**：学习一个反射流（reflected flow），在 BC 策略的源分布 $q_{\text{BC}}$ 的支持集内操纵噪声分布，生成最大化 Q 值的噪声 $\tilde{q}_{\text{BC}}$，同时保证 $\text{supp}(\tilde{q}_{\text{BC}}) \subseteq \text{supp}(q_{\text{BC}})$。

由于 BC 流式策略是连续映射，源分布支持集内的任意点映射后仍落在目标分布支持集内，因此整个复合策略天然满足支持约束——**这是构造性保证，而非优化约束**。

### 相对于 Baseline 的 Changed Slots

| 方法组件 | 典型离线 RL 方法（FQL、DSRL 等） | ReFORM |
|---------|-------------------------------|--------|
| **策略表示** | 隐式 Q 函数加权采样或扩散策略 | 两阶段流式策略（BC flow + reflected flow） |
| **OOD 处理机制** | 统计距离正则化（KL / Wasserstein）约束策略密度 | 支持约束通过构造保证，无需显式正则化 |
| **源分布** | 无界高斯分布或标准正态分布 | 有界均匀分布 $\mathcal{U}(\mathcal{B}_l^d)$ |
| **噪声操纵方式** | 固定源分布采样 | 反射流在支持集内优化噪声分布以最大化 Q 值 |
| **推理加速** | 需多步采样 | 蒸馏为一步策略 $\mu_{\hat{\theta}_1}(z; s)$ |

### 关键设计决策与证据

1. **有界源分布的必要性**：消融实验（Figure 4）表明，将源分布替换为无界分布（ReFORM(U)）会导致严重的 OOD 问题，模型完全无法学习。这验证了有界支持集对于支持约束构造性保证的必要性。

2. **反射流优于补偿策略**：在边界处理上，补偿出界速度（compensating outbound velocities）比反射出界速度（reflecting outbound velocities）训练更稳定（Figure 4 右侧训练曲线）。其理论解释仍是开放问题。

3. **蒸馏的边际收益**：移除蒸馏步骤（ReFORM(NoDistill)）仅导致性能轻微下降，说明蒸馏主要影响推理效率而非策略质量。

### 方法的可迁移性

反射流噪声生成器不仅适用于流式策略，理论上可与任何基于生成模型的策略（包括扩散策略）组合，具有较好的通用性。



![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_YvFsyRReeN/figures/001_Figure_1.jpg]]
*Figure 1: ReFORM algorithm. The process with gray arrows indicates the BC flow policy, learned to transform a simple source distribution $q _ { \mathrm { B C } } = \hat { \mathcal { U } } ( \mathcal { B } _ { l } ^ { d }$ ) to a target distribution $p _ { \mathrm { B C } }$ that matches the dataset . The blue arrows indicate the ReFORM process, where we learn a flow noise generator to generate a manipulated source distribution $\tilde { q } _ { \mathrm { B C } }$ for the BC policy so that the manipulated target p˜BC maximizes the $\dot { Q }$ value while staying inside the support (denoted in red) of the BC policy

ReFORM 是一个两阶段流式策略（two-stage flow policy），其核心设计目标是通过构造方式（by construction）实现支持集约束，从而在不限制策略改进能力的前提下规避离线强化学习中的分布外（OOD）动作问题。整体 pipeline 由三个关键模块串联构成：**BC 流式策略**、**反射流噪声生成器** 和**一步蒸馏策略**。

**第一阶段：BC 流式策略学习。** 首先从离线数据集中学习一个行为克隆（BC）流式策略 $\psi_{\theta_1}$。该策略以有界均匀分布 $q_{\text{BC}} = \mathcal{U}(\mathbf{B}_l^d)$（$d$ 维半径为 $l$ 的超球面上的均匀分布）为源分布，通过条件流匹配（conditional flow matching）将其变换为目标分布 $p_{\text{BC}}(\cdot|s)$，以逼近行为策略 $\pi_\beta(\cdot|s)$。这一阶段仅依赖数据集中的状态-动作对，不涉及 Q 函数优化。

**第二阶段：反射流噪声生成器。** 在 BC 流式策略的基础上，引入一个噪声生成器 $\psi_{\theta_2}$，其作用是在源分布 $q_{\text{BC}}$ 的支持集内部对噪声进行重分布。该生成器采用反射流（reflected flow），通过反射 ODE 确保生成样本始终不超出 $q_{\text{BC}}$ 的有界支持集。优化目标为最大化组合策略 $\mu_\theta = \mu_{\theta_1} \circ \psi_{\theta_2}$ 的期望 Q 值，从而在支持集约束内实现策略改进。由于噪声生成器的输出始终满足 $\text{supp}(\tilde{q}_{\text{BC}}) \subseteq \text{supp}(q_{\text{BC}})$，经 BC 流式策略推送后，最终动作分布 $\tilde{p}_{\text{BC}}$ 也必然满足 $\text{supp}(\tilde{p}_{\text{BC}}) \subseteq \text{supp}(p_{\text{BC}})$，即整个组合策略天然满足支持集约束。

**第三阶段：一步蒸馏。** 为提升推理效率，将两阶段组合策略蒸馏为一步策略 $\mu_{\hat{\theta}_1}$，通过最小化与原始 BC 流式策略输出的均方误差实现。蒸馏后的策略直接以从 $q_{\text{BC}}$ 采样的潜变量 $z$ 和状态 $s$ 为输入，输出动作 $a$，无需在推理时执行 ODE 求解。

**输入输出流总结：** 状态 $s$ 与从有界均匀分布采样的潜变量 $z$ 作为输入，经蒸馏后的一步策略直接输出动作 $a$。训练阶段，BC 流式策略学习从 $z$ 到 $a$ 的映射，噪声生成器在 $z$ 空间内进行有界扰动以最大化 Q 值，两个模块协同优化，最终通过蒸馏合并为单一前向网络。



ReFORM 的核心架构由两个级联的流模型构成：BC 流策略（BC flow policy）与反射流噪声生成器（reflected flow noise generator）。前者从离线数据集中学习行为克隆，将简单源分布映射到匹配行为策略的复杂动作分布；后者在 BC 策略的源分布支撑集内生成受约束的多模态噪声，通过改变 BC 策略的输入来间接改变其输出动作分布，从而在不引入 OOD 动作的前提下实现策略改进。

### 4.1 BC 流策略

BC 流策略 $\psi_{\theta_1}$ 学习一个时间相关的速度场 $v_{\theta_1}$，将源分布 $q_{\mathrm{BC}}$ 变换为目标分布 $p_{\mathrm{BC}}(\cdot|s)$，后者近似行为策略 $\pi_\beta(\cdot|s)$。源分布选择为 $d$ 维超球内的均匀分布：

$$q_{\mathrm{BC}} = \mathcal{U}(\mathcal{B}_l^d)$$

其中 $\mathcal{B}_l^d = \{x \in \mathbb{R}^d : \|x\| \leq l\}$ 是半径为 $l$ 的超球。选择有界支撑的源分布是实现支撑约束的关键——它使得 BC 策略的支撑集天然有界，为后续噪声生成器在支撑集内操作提供了几何基础。

速度场的学习采用简单线性流（simple linear flow），其条件概率路径为 $x_t = t a + (1 - t) z$，其中 $a$ 为数据集中的动作，$z \sim q_{\mathrm{BC}}$。BC 流策略的损失函数为：

$$\mathcal{L}_{\mathrm{BC}}(\theta_1) = \mathbb{E}_{(s,a)\sim\mathcal{D},\; z\sim\mathcal{U}(\mathcal{B}_l^d),\; t\sim\mathcal{U}[0,1]} \left[\|v_{\theta_1}(t, t a + (1-t)z; s) - (a - z)\|^2\right]$$

该损失直接回归速度场的目标值 $a - z$，使流模型学会将 $z$ 沿直线路径推向 $a$。训练完成后，BC 流策略的均值动作由 ODE 终点给出：$\mu_{\theta_1}(z; s) = \psi_{\theta_1}(1, z; s)$。

### 4.2 反射流噪声生成器

噪声生成器 $\psi_{\theta_2}$ 的目标是学习一个从 $q_{\mathrm{BC}}$ 到自身支撑集内某个优化后分布 $\tilde{q}_{\mathrm{BC}}$ 的映射，使得组合策略 $\mu_\theta = \mu_{\theta_1} \circ \psi_{\theta_2}$ 的期望 Q 值最大化。其核心约束是：

$$\mathrm{supp}(\tilde{q}_{\mathrm{BC}}) \subseteq \mathrm{supp}(q_{\mathrm{BC}})$$

为满足该约束，噪声生成器采用反射流（reflected flow）机制，通过反射 ODE 确保生成样本始终停留在超球 $\mathcal{B}_l^d$ 内：

$$d\psi_{\theta_2}(t, w; s) = v_{\theta_2}(t, \psi_{\theta_2}(t, w; s); s)\,dt + dL_t, \quad \psi_{\theta_2}(0, w; s) = w$$

其中 $L_t$ 是局部时（local time）项，当样本触及超球边界时产生反射效应，将其推回支撑集内部。噪声生成器的优化目标为最大化组合策略的 Q 值：

$$\mathcal{L}_{\mathrm{NG}}(\theta_2) = \mathbb{E}_{s\sim\mathcal{D},\; w\sim\mathcal{U}(\mathcal{B}_l^d)} \left[-Q_{\phi}^{\mu_\theta}\left(s,\; \mu_{\theta_1}(\psi_{\theta_2}(1, w; s); s)\right)\right]$$

该损失通过 BPTT（backpropagation through time）沿整个流轨迹反向传播梯度，同时优化速度场 $v_{\theta_2}$。反射机制保证了 $\tilde{q}_{\mathrm{BC}}$ 的支撑集始终是 $q_{\mathrm{BC}}$ 支撑集的子集，从而在构造层面避免了 OOD 问题。

### 4.3 蒸馏为一阶策略

为降低推理时的计算开销，ReFORM 将两阶段流策略蒸馏为单步映射。蒸馏损失直接最小化蒸馏模型 $\mu_{\hat{\theta}_1}$ 与原始 BC 流策略 $\mu_{\theta_1}$ 在随机噪声输入下的输出差异：

$$\mathcal{L}_{\mathrm{Distill}}(\hat{\theta}_1) = \mathbb{E}_{s\sim\mathcal{D},\; z\sim\mathcal{U}(\mathcal{B}_l^d)} \left[\|\mu_{\hat{\theta}_1}(z; s) - \mu_{\theta_1}(z; s)\|^2\right]$$

蒸馏后的策略 $\mu_{\hat{\theta}_1}$ 直接接受噪声生成器的输出 $z = \psi_{\theta_2}(1, w; s)$ 作为输入，单步前向即可产生动作，无需再求解 ODE。

### 理论保证

两个定理形式化了 ReFORM 的支撑约束性质：

- **定理 1**：反射流噪声生成器产生的分布 $\tilde{q}_{\mathrm{BC}}$ 满足 $\mathrm{supp}(\tilde{q}_{\mathrm{BC}}) \subseteq \mathrm{supp}(q_{\mathrm{BC}})$。
- **定理 2**：组合策略 $\pi_\theta$ 的支撑集满足 $\mathrm{supp}(\pi_\theta(\cdot|s)) \subseteq \mathrm{supp}(\pi_{\mathrm{BC}}(\cdot|s))$，即始终处于 BC 策略的支撑集内。

这两个定理共同保证了 ReFORM 在构造层面避免了 OOD 动作的产生，同时不对策略改进施加额外的分布距离正则化约束，允许策略在支撑集内自由探索高 Q 值区域。



## 实验与关键发现

### 主实验结果

ReFORM 在 OG-Bench 的 40 个任务（CLEAN 和 NOISY 数据集）上，使用**同一套超参数**取得了最优整体性能。性能曲线（Figure 2）显示，ReFORM 在归一化得分接近 1 的区间内占据最高比例，表明其在高性能区域的概率密度显著优于所有对比方法。对比的基线包括 IFQL、FQL（L/M/S 三种规模变体）和 DSRL，这些方法均使用了各自手工调优的超参数（Table 3），而 ReFORM 无需针对不同任务进行超参数调整。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_YvFsyRReeN/figures/004_Figure_2.jpg]]
*Figure 2: Performance profile over CLEAN and NOISY datasets. For a given normalized score τ (x-axis), the performance profile shows the probability that a given method achieves a score ≥ τ (see Agarwal et al. (2021) for details). On the CLEAN dataset, ReFORM achieves greater scores with higher probabilities than all other baselines. The same is true on the NOISY dataset except for a small set of normalized scores around 0.9 where ReFORM and FQL(S) have similar probabilities within the statistical margins. (a) BC. (b) DSRL. (c) IFQL. (d) FQL(S). (e) FQL(M). (f) FQL(L). (g) ReFORM3. Figure 3: Learned policy distributions with the toy example. The Q-value reaches the maximum at the lower left and upper...*

在 D4RL 基准的 12 个环境上（Table 5），ReFORM 同样表现出竞争力，在多数 AntMaze 和 Adroit 任务上达到或超过最佳性能的 95% 阈值。在视觉操控任务上（Table 6），ReFORM 在两个任务（CLEAN 和 NOISY visual-cube）上均取得最佳结果。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_YvFsyRReeN/figures/022_Table_5.jpg]]
*Table 5: D4RL results. We present the following results on environments in the D4RL Fu et al. (2020) benchmark. The results are averaged over 3 seeds and 32 runs per seed. The results are bolded if the algorithm achieves at or above 95% of the best performance following Park et al. (2025a)*

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_YvFsyRReeN/figures/023_Table_6.jpg]]
*Table 6: Visual manipulation results. We present the following results on visual manipulation environments in OGBench Park et al. (2025a). The results are averaged over 3 seeds and 32 runs per seed. The results are bolded if the algorithm achieves at or above 95% of the best performance following Park et al. (2025a). To save space, the -singletask tags are omitted from task names*

ReFORM 的训练时间约为每百万步 80 分钟（Table 7），是 FQL（40 分钟）和 IFQL（35 分钟）的约两倍，比 DSRL（55 分钟）慢约 45%。这一额外开销主要来自噪声生成器的反向传播通过时间（BPTT）计算。

### 支持约束的有效性：Toy Example 分析

Figure 3 通过一个二维 toy example 直观展示了支持约束的机制。在该示例中，Q 函数的最大值位于左下角和右上角两个角落，而行为策略的分布集中在中心区域。BC 策略仅覆盖了行为策略的支持范围，无法触及高 Q 值区域。DSRL 通过向行为策略添加噪声来扩展覆盖，但受限于固定的噪声尺度。FQL 的三个变体（S/M/L）随着正则化强度的减弱，逐渐偏离支持范围，其中 FQL(L) 完全脱离支持区域，产生了严重的 OOD 外推。**ReFORM 则成功将策略分布引导至两个高 Q 值角落，同时严格保持在 BC 策略的支持边界（红色边界）之内**，实现了在不违反支持约束的前提下最大化性能。

### 消融实验

**源分布的有界性是关键设计。** Figure 4（左）对比了 ReFORM 与使用无界源分布变体 ReFORM(U) 的性能。ReFORM(U) 无法学到任何有效策略（归一化得分接近零），证实了有界源分布对于满足支持约束和避免 OOD 问题至关重要。

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_YvFsyRReeN/figures/005_Figure_4.jpg]]
*Figure 4: Ablations. Left: normalized scores of ReFORM and its variants with different source distributions. Right: training curves of ReFORM and its variants by changing its components*

**BC 流策略蒸馏的影响。** 去除蒸馏步骤的变体 ReFORM(NoDistill) 性能略有下降（Figure 4 右），表明一步策略蒸馏虽然对最终性能有一定贡献，但并非决定性因素。

**速度场边界处理策略。** 在反射流噪声生成器中，处理超出支持边界速度的策略有两种：反射（reflecting）和补偿（compensating）。实验发现，**补偿出界速度比反射出界速度使训练过程更稳定**（Figure 4 右），但作者指出这一现象目前缺乏理论解释，是值得进一步研究的问题。

### 失败模式与局限

尽管 ReFORM 在支持约束方面表现优异，其性能仍依赖于 BC 流策略的质量。如果 BC 模型本身存在 OOD 误差，噪声生成器在 BC 策略支持范围内的优化也会受到影响。此外，噪声生成器的训练需要反向传播通过整个 BC 流策略的积分过程，计算开销较大，限制了在更大规模任务上的扩展性。

### 补充图表

![[assets/figures/papers/paper_list_l44_https_openreview_net_forum_id_YvFsyRReeN/figures/015_Table_4.jpg]]
*Table 4: Full results. We present full results (normalized score) on 40 OGBench tasks. The results are averaged over 3 seeds and 32 runs per seed. The results are bolded if the algorithm achieves at or above 95% of the best performance following Park et al. (2025a). To save space, the -singletask tags are omitted from task names*



## 定位与知识库关联

### 1. 与基线方法的关系

ReFORM 处于离线强化学习中**基于生成式模型的策略优化**与**支持集约束**两条技术路线的交汇点。其核心贡献在于将这两条路线通过“构造性支持约束”（support constraint by construction）统一起来，而非像先前工作那样依赖显式的统计距离正则化。

**相对于行为克隆（BC）与简单策略约束方法：**
传统的 BC 方法直接拟合数据集中的动作分布，但缺乏利用 Q 函数进行策略改进的能力，在面对多模态行为策略时尤其受限。许多后续方法通过引入 KL 散度或 Wasserstein 距离等统计距离正则化项来约束学习策略与行为策略之间的偏离（如 IFQL 等）。然而，这些正则化方法存在一个根本性的权衡：正则化过强会限制策略改进的上限，正则化过弱则无法有效防止 OOD 动作的外推误差。ReFORM 避开了这一权衡——它通过构造使策略的支持集始终保持在 BC 策略的支持集内，因此无需任何限制策略改进的正则化项，理论上允许策略在支持集内任意优化。

**相对于扩散/流匹配策略方法：**
近年来，扩散策略和流匹配策略因其强大的多模态分布建模能力被引入离线 RL。DSRL 等方法使用扩散模型作为策略，但仍需显式正则化来约束策略与行为策略的距离。ReFORM 同样采用流匹配作为策略骨干，但其创新在于**两阶段架构**：第一阶段学习一个从有界均匀分布到行为策略的 BC 流策略；第二阶段学习一个反射流（reflected flow）噪声生成器，在 BC 策略的源分布支持集内操纵噪声，从而间接操纵 BC 策略的输出分布。这种“噪声操纵”范式使得策略改进完全发生在 BC 策略的潜空间中，从根本上杜绝了 OOD 动作的产生。

**相对于 FQL 系列方法：**
FQL（Flow Q-Learning）系列方法（包括 FQL(S)、FQL(M)、FQL(L)）同样使用流匹配策略，但通过调节缩放参数 α 来控制策略与行为策略的接近程度。这一做法本质上仍是统计距离正则化的变体，需要针对不同任务手动调整 α 值。实验表明，ReFORM 在所有 40 个 OGBench 任务上使用**同一组超参数**即可超越 FQL 系列中经过手工调参的最佳表现，验证了构造性支持约束在泛化性和调参效率上的优势。

### 2. 方法谱系定位

ReFORM 的方法论谱系可梳理如下：

| 技术要素 | 来源/相关方法 | 在 ReFORM 中的角色 |
|---------|-------------|------------------|
| 流匹配策略 | Flow matching (Lipman et al., 2023)、FQL | BC 策略的建模骨干 |
| 有界源分布 | — | 使支持集约束可构造化（均匀分布于 d 维超球体） |
| 反射流 | Reflected flow (Xie et al., 2024) | 噪声生成器保持支持集约束的核心机制 |
| 支持集约束优化 | 离线 RL 支持约束理论 | 策略改进的理论基础 |
| 策略蒸馏 | 策略蒸馏技术 | 将多步流推理压缩为一步策略以加速部署 |

这一谱系表明，ReFORM 并非从零创新，而是对已有技术模块进行了巧妙的重新组合与适配。其核心洞察在于：**如果 BC 策略的源分布具有有界支持集，且噪声生成器在该有界支持集内运行，那么组合策略的支持集将天然地被约束在 BC 策略的支持集内**——这一性质由两个定理（Theorem 1 和 Theorem 2）形式化保证。

### 3. 适用边界

**有效的前提条件：**
1. **BC 策略的源分布必须具有有界支持集**。论文中的消融实验（Figure 4）表明，当将源分布替换为无界的高斯分布（ReFORM(U)）时，算法几乎无法学到任何有效策略，因为无界源分布无法满足支持集约束的构造性条件。
2. **BC 策略本身需要具备足够的行为覆盖能力**。ReFORM 的策略改进受限于 BC 策略的支持集——如果 BC 策略未能覆盖高奖励区域，ReFORM 无法通过策略改进触及这些区域。这是支持集约束方法的固有限制。
3. **反射流噪声生成器的训练依赖于 BPTT（Backpropagation Through Time）**，这带来了较高的计算开销。论文在局限性部分明确指出，BPTT 的计算密集性是一个实际问题。

**不适用或需谨慎使用的场景：**
- 当行为策略的支持集本身严重不足（例如仅覆盖了极窄的动作区域）时，ReFORM 的策略改进空间极为有限。
- 当 BC 策略本身存在 OOD 误差时，这些误差可能通过噪声生成器的操纵被放大或传播。
- 对推理速度有极高要求的实时场景中，尽管蒸馏技术可以缓解，但蒸馏本身会引入额外的近似误差。

### 4. 局限性与开放问题

**论文明确指出的局限性：**
1. **BPTT 的计算密集性**：反射流噪声生成器的训练需要通过整个流轨迹进行反向传播，计算开销较大。论文建议未来可通过捷径模型（shortcut models）或预训练 BC 模型来缓解这一问题。
2. **对 BC 模型质量的依赖**：ReFORM 的策略改进完全建立在 BC 策略的基础上，BC 策略的 OOD 误差可能影响最终策略的质量。
3. **速度补偿与反射的稳定性差异缺乏理论解释**：实验发现，对超出边界的速度进行“补偿”（compensating）比“反射”（reflecting）训练更稳定，但目前缺乏对这一现象的理论解释。

**开放问题：**
1. **反射流噪声生成器能否与其他生成式策略（如扩散策略）结合？** 论文在结论中提及了这一可能性，但未进行实验验证。
2. **支持集约束的“紧致性”与策略改进上限之间的关系**：当前的支持集约束是“硬”约束，是否存在更灵活的约束形式，在保持 OOD 安全性的同时进一步扩展策略改进空间？
3. **理论解释**：为何速度补偿比速度反射更稳定？这一现象可能涉及流轨迹的数值稳定性与梯度传播特性，值得进一步的理论分析。

### 5. 知识库定位

ReFORM 在离线 RL 知识库中的定位可概括为：

- **问题域**：离线强化学习中的 OOD 动作外推问题
- **方法类**：生成式策略 + 构造性支持集约束
- **关键技术标签**：流匹配（Flow Matching）、反射流（Reflected Flow）、支持集约束（Support Constraint）、行为克隆（Behavior Cloning）、策略蒸馏（Policy Distillation）
- **基准测试**：OGBench（40 个任务，含 CLEAN 和 NOISY 数据集）
- **对比方法**：IFQL、FQL(S/M/L)、DSRL
- **核心优势**：无需任务特定超参数调优的构造性 OOD 防护
- **核心代价**：BPTT 计算开销、对 BC 策略质量的依赖



## 原文 PDF

![[paperPDFs/ICLR_2026/ReFORM_Reflected_Flows_for_On_support_Offline_RL_via_Noise_Manipulation.pdf]]
