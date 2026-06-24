---
title: Reliable Policy Transfer for Safety-Aware End-to-End Driving with Deep Reinforcement Learning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Reliable_Policy_Transfer_for_Safety_Aware_End_to_End_Driving_with_Deep_Reinforcement_Learning.pdf
project_link: null
code_link: "https://github.com/szu-ai/safe-driving-drl/"
aliases:
- USADF
- RPTSAEEDDRL
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 决策时归一化不确定性信号σ̄，通过同时驱动不确定性加权注意力、熵门控探索和因果-不确定性迁移对齐，实现对安全关键行为的统一调控。
primary_logic: 将不确定性信号作为控制层可靠性接口的核心，贯穿场景表示、奖励塑造、探索和跨域迁移，能够系统性地提升闭环驾驶的安全性与泛化性。
claims:
- 完整模型在Town02上获得DS 214.3、RC 84.1%、碰撞率0.005/km、IS 0.94，显著超越对比方法。
- 碰撞率从ST-P3的0.011降至本模型的0.006，不确定性门控探索使安全性大幅提升。
- 移除不确定性加权注意力后CTE上升0.11，证明不确定加权对稳定性至关重要。
- 因果-不确定性迁移对齐使Town02 DS从194.1（无迁移）提升至214.3，且零样本泛化明显优于对比方法。
---

# Reliable Policy Transfer for Safety-Aware End-to-End Driving with Deep Reinforcement Learning

> [!tip] 核心洞察
> 将不确定性信号作为控制层可靠性接口的核心，贯穿场景表示、奖励塑造、探索和跨域迁移，能够系统性地提升闭环驾驶的安全性与泛化性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向安全感知端到端驾驶的深度强化学习可靠策略迁移 |
| 英文题名 | Reliable Policy Transfer for Safety-Aware End-to-End Driving with Deep Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Borhan_Reliable_Policy_Transfer_for_Safety-Aware_End-to-End_Driving_with_Deep_Reinforcement_CVPR_2026_paper.html) · [Code](https://github.com/szu-ai/safe-driving-drl/) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Unified Safety-Aware DRL Framework |
| Dataset | Town10HD |

> [!tip] 效果简介
> - Town10HD 上，Collision rate (per km) 0.006 vs ST-P3 (0.011) (−45.5%)；CTE (Cross-Track Error) 0.65 vs ST-P3 (≈0.91) (−28.6%)。

## 概述

安全、可靠且可泛化的端到端驾驶控制是自动驾驶长期面临的挑战。现有方法在感知编码、奖励设计、探索策略和跨域迁移等环节各自为政，缺乏统一的因果与不确定性接口，导致在分布偏移下安全性差、泛化能力弱。本文提出一个**统一安全感知深度强化学习框架**，以归一化不确定性信号 $\bar{\sigma}$ 作为控制层的可靠性接口，贯穿场景表示、奖励塑造、探索和策略迁移，实现安全关键行为的统一调控。

核心贡献包括：（1）以自车为中心的关系图编码器，结合**不确定性加权注意力**（Eq. 7–8）构建因果状态表示；（2）含不确定性项的**可微多目标奖励**（Eq. 9–13），提供安全、进度、舒适和不确定性的稠密训练信号；（3）**联合偶然‑认知不确定性估计**与**熵门控探索**（Eq. 14–15），利用 $\bar{\sigma}$ 动态调节策略熵，实现风险感知探索；（4）**因果‑不确定性迁移对齐**（Eq. 16）与**MAML元初始化**（Eq. 17），通过对齐动作分布、注意力和不确定性统计量实现跨域快速适应。

在CARLA仿真环境中，该方法在Town10HD上取得碰撞率0.006/km、CTE 0.65，相比ST-P3（碰撞率0.011/km、CTE≈0.91）分别降低45.5%和28.6%；在Town02上获得驾驶评分214.3、路线完成率84.1%，显著超越TransFuser、ThinkTwice、RaSc等基线方法。消融实验证实，移除不确定性加权注意力使CTE升高0.11，移除熵门控使碰撞率增加0.002/km，去除迁移对齐使Town02评分降至194.1，验证了各模块的必要性与互补贡献。

## 背景与动机

端到端自动驾驶旨在直接从传感器输入映射到控制指令，近年来基于模仿学习（IL）和深度强化学习（DRL）的方法在仿真环境中取得了显著进展。然而，安全关键场景下的可靠决策仍然是一个核心瓶颈。当前方法面临三个深层困境：

**感知与控制的割裂。** 主流端到端架构通常将感知编码和策略优化视为两个独立阶段——感知模块输出全局张量融合特征，控制模块在此基础上进行决策。这种设计缺乏对感知不确定性的显式建模：当检测噪声增大或交互对象处于感知边缘时，策略无法区分“高置信度关键障碍物”与“低置信度背景杂波”，导致在密集交通或恶劣天气下出现过度反应或欠反应。**ST-P3**（Hu et al., ECCV 2022）和**TransFuser**（Chitta et al., TPAMI 2023）等代表性方法虽然在特征融合机制上做了改进，但均未将不确定性信号作为控制层的结构化输入。

**奖励塑造与探索的粗糙性。** 现有DRL驾驶方法多采用稀疏事件奖励（如碰撞惩罚、到达奖励）或固定阈值惩罚，这类奖励函数不可微且缺乏对中间安全状态的平滑反馈，使策略优化面临高方差和收敛困难。同时，策略熵通常采用全局衰减调度，与当前场景的风险水平脱钩——在高不确定性场景下，无差别的探索可能直接导致危险动作；在低不确定性场景下，过度保守的熵约束又限制了策略的精细化。

**跨域迁移缺乏因果对齐。** 从源域（如训练城镇）到目标域（如未见城镇）的迁移通常仅依赖感知层面的域适应，忽略了控制策略本身的因果结构差异。当目标域的交通规则、道路拓扑或交互密度发生变化时，源域策略的注意力分布和不确定性统计量可能与目标域的真实需求失配，导致“看似正确感知、实则错误决策”的迁移失效。**ThinkTwice**（Jia et al., CVPR 2023）和**RaSc**（Fan et al., ECCV 2024）在感知端引入了可解释性机制，但未将因果一致性和不确定性对齐纳入迁移目标。

上述问题的共同根源在于：**控制层缺乏统一的因果与不确定性接口**，使得感知编码、奖励塑造、探索和策略迁移各自为政，在分布偏移下安全性差、泛化能力弱。本文的核心动机正是构建这样一个统一接口——将不确定性信号作为控制层可靠性接口的核心，贯穿场景表示、奖励塑造、探索和跨域迁移，从而系统性地提升闭环驾驶的安全性与泛化性。

## 核心创新

本工作的核心贡献在于构建了一个以**归一化不确定性信号 $\\bar{\\sigma}$ 为统一控制接口**的安全感知端到端驾驶强化学习框架。该信号贯穿场景表示、奖励塑造、探索策略和跨域迁移四个关键环节，系统性地解决了现有方法中感知编码、奖励设计、探索与策略迁移各自为政、在分布偏移下安全性差和泛化能力弱的瓶颈问题。

### 创新一：不确定性加权因果注意力场景表示

传统端到端驾驶方法（如 **ST-P3** (Hu et al., ECCV 2022)、**TransFuser** (Chitta et al., TPAMI 2023)）采用全局张量融合，缺乏对感知不确定性的显式建模。本工作提出以自车为中心的关系图编码器，为每个场景实体构建包含相对运动学、车道几何、语义类别和aleatoric方差的紧凑边特征向量：

$$\mathbf{e}_i^t = [\Delta p_i, \Delta v_i, c_i, \kappa_i, \sigma_i^2]$$

在此基础上，引入**不确定性加权因果注意力**机制（Eq. 7），使注意力权重同时依赖于实体距离和其估计不确定性：

$$\alpha_i = \mathrm{softmax}_i\left(-\frac{\|\Delta p_i\|^2}{\sigma_i^2 + \varepsilon}\right), \quad z_t = \sum_i \alpha_i W_e e_i^t$$

聚合后的交互嵌入 $z_t$ 与自车动态、路径进度、车道特征和aleatoric不确定性拼接，形成紧凑的决策状态 $s_t$（Eq. 8）。这一设计的因果逻辑在于：高不确定性实体（如远处被遮挡的行人）获得较低注意力权重，从而抑制噪声感知对决策的干扰。消融实验（Table 2）证实，移除不确定性加权注意力后，CTE升高0.11、航向误差升高0.07，验证了该机制对控制稳定性的关键作用。

### 创新二：含不确定性项的可微多目标奖励塑造

现有方法普遍采用稀疏事件惩罚或阈值触发奖励，梯度信号不连续，优化困难。本工作提出**可微多目标奖励函数**（Eq. 9–13），将安全、进度、舒适和不确定性四个维度统一为平滑代理奖励：

$$r_t = w_s r_s + w_p r_p + w_c r_c + w_u r_u$$

其中安全项 $r_s$ 使用平滑代理函数 $\\psi_L, \\psi_P$ 替代硬阈值，对横向偏离、接近碰撞和信号违规进行连续惩罚（Eq. 10）；不确定性项 $r_u$ 直接引入归一化不确定性 $\\bar{\\sigma}$ 作为负奖励，驱动策略主动规避高不确定状态。消融实验（Table 2）表明，用事件奖励替代可微奖励（EventReward）导致DS下降18.4点、CTE升高0.09，证实可微奖励对优化稳定性的决定性贡献。

### 创新三：联合Aleatoric-Epistemic不确定性估计与熵门控探索

区别于将aleatoric和epistemic不确定性分离处理或无统一估计的基线，本工作提出**联合不确定性估计**，并计算归一化信号 $\\bar{\\sigma}$ 作为决策时置信度的统一度量。该信号直接驱动**熵门控探索**机制（Eq. 15）：

$$\mathcal{L}_{ent} = -\beta(\bar{\sigma}) H(\pi_\theta); \quad \beta(\bar{\sigma}) = \beta_0(1 - \bar{\sigma})$$

其因果机制在于：当 $\\bar{\\sigma}$ 较高（低置信度）时，熵系数 $\\beta$ 被抑制，策略倾向于保守利用而非冒险探索；当 $\\bar{\\sigma}$ 较低（高置信度）时，允许更充分的探索。这一耦合使探索行为天然具备风险感知能力。消融实验（Sec. 4.6, Table 2）显示，移除熵门控后策略方差增加21%、碰撞率增加0.002/km，且碰撞率从ST-P3的0.011降至本模型的0.006（Figure 6），验证了 $\\bar{\\sigma}$-熵耦合对安全性的显著提升。

### 创新四：因果-不确定性迁移对齐与MAML元初始化

现有策略迁移方法（如仅感知层面适配）缺乏对决策因果结构和对齐信号一致性的保障。本工作提出**因果-不确定性迁移对齐**损失（Eq. 16）：

$$\mathcal{L}_{trans} = \mathcal{L}_{KL} + \lambda_\alpha \mathrm{MMD}(\alpha_s, \alpha_t) + \lambda_u \|u_s - u_t\|^2$$

该损失同时对齐源域和目标域的动作分布（KL散度）、因果注意力权重（MMD）和不确定性统计量（L2距离），确保迁移过程中因果推理逻辑和可靠性接口的一致性。在此基础上，引入**MAML元初始化**（Eq. 17），通过跨域元学习获取小样本快速适应的初始参数。消融实验（Table 2）表明，去除迁移目标使Town02 DS从214.3降至194.1，去除MAML降至200.8，证明二者对跨域泛化的互补贡献。完整模型在Town02上获得DS 214.3、RC 84.1%、碰撞率0.005/km、IS 0.94，显著超越对比方法（Table 1）。

### 创新总结

上述四个创新并非孤立改进，而是通过**$\\bar{\\sigma}$ 作为统一控制层可靠性接口**形成闭环：不确定性加权注意力利用 $\\bar{\\sigma}$ 抑制噪声感知；不确定性奖励项驱动策略规避高风险状态；熵门控利用 $\\bar{\\sigma}$ 调节探索-利用平衡；迁移对齐确保 $\\bar{\\sigma}$ 统计量在域间一致。这一系统化设计使安全性、稳定性和泛化性得到协同提升，构成了本工作的核心方法论贡献。

## 整体框架

本文提出一个**统一安全感知深度强化学习框架**，其核心设计理念是将不确定性信号作为控制层的可靠性接口，贯穿场景表示、奖励塑造、探索策略和跨域迁移四个关键环节。框架由四个协同模块构成（Figure 1）：

![[assets/figures/papers/paper_list_l2719_https_openaccess_thecvf_com_content_CVPR2026_html_Borhan_Reliable_Policy/figures/001_Figure_1.jpg]]
*Figure 1: Unified framework: (a) relational state with uncertainty-weighted attention; (b) multi-objective reward shaping; (c) joint aleatoric–epistemic uncertainty gating of policy entropy; (d) causal-semantic transfer via KL, MMD, uncertainty matching, and MAML*

**模块一：以自车为中心的关系图编码器（Ego-Centric Relational Graph Encoder）**  
该模块将驾驶场景建模为有向关系图，其中每条边从场景实体指向自车节点。边的特征向量 $\mathbf{e}_i^t = [\Delta p_i, \Delta v_i, c_i, \kappa_i, \sigma_i^2]$ 紧凑编码了相对运动学、语义类别、车道几何和每实体的aleatoric方差。随后，通过**不确定性加权注意力**机制（Eq. 7）聚合所有交互特征：
$$\alpha_i = \mathrm{softmax}_i\big(-\frac{\|\Delta p_i\|^2}{\sigma_i^2+\varepsilon}\big), \quad z_t = \sum_i \alpha_i W_e e_i^t$$
注意力权重同时考虑空间距离和感知不确定性——高不确定性实体的影响被抑制，避免策略对噪声检测过度反应。聚合后的交互嵌入 $z_t$ 与自车速度、历史动作、路径进度、车道特征和aleatoric不确定性拼接，形成紧凑的决策状态 $s_t$（Eq. 8）。

**模块二：可微多目标奖励塑造（Differentiable Multi-Objective Reward Shaping）**  
替代传统的事件驱动或阈值惩罚，该模块设计了四组平滑可微的奖励项（Eq. 9-13）：安全项 $r_s$ 用连续代理函数惩罚横向偏离、接近碰撞和信号违规；进度项 $r_p$ 鼓励沿路线推进；舒适项 $r_c$ 抑制急加速和急转向；不确定性项 $r_u$ 惩罚高不确定性状态下的激进决策。所有项均保持有界范围，确保优化稳定性和跨域迁移的一致性。

**模块三：联合不确定性估计与熵门控探索（Joint Aleatoric-Epistemic Uncertainty Estimation & Entropy-Gated Exploration）**  
框架同时估计aleatoric（数据固有）和epistemic（模型知识不足）两类不确定性，并计算归一化信号 $\bar{\sigma} \in [0,1]$。该信号通过**熵门控机制**动态调节策略熵（Eq. 15）：
$$\mathcal{L}_{ent} = -\beta(\bar{\sigma}) H(\pi_\theta); \quad \beta(\bar{\sigma}) = \beta_0(1-\bar{\sigma})$$
当 $\bar{\sigma}$ 较高（模型不确定）时，熵系数降低，抑制探索以避免危险行为；当 $\bar{\sigma}$ 较低时，允许更充分的探索。这一机制建立了风险感知与探索之间的因果耦合。

**模块四：因果-不确定性迁移对齐与MAML初始化（Causal-Uncertainty Transfer Alignment & MAML Initialization）**  
跨域迁移时，除了标准的KL散度对齐动作分布外，还引入MMD距离对齐源域和目标域的注意力分布 $\alpha_s, \alpha_t$，以及L2距离匹配不确定性统计量 $u_s, u_t$（Eq. 16）。这确保了迁移过程中因果注意模式和可靠性感知的一致性。此外，通过MAML元学习（Eq. 17）获取跨多域的共享初始化 $\theta^*$，使模型能在目标域以小样本快速适应。

**输入输出流**：原始传感器数据经感知模块提取实体特征后，输入关系图编码器生成决策状态 $s_t$；策略网络基于 $s_t$ 输出控制动作；奖励函数根据状态-动作对计算多目标奖励信号；不确定性估计模块持续更新 $\bar{\sigma}$，同时驱动注意力权重、熵门控和迁移对齐三个下游环节。整个pipeline形成闭环，$\bar{\sigma}$ 作为统一的可靠性接口贯穿始终。

## 核心模块与公式推导

本方法将闭环驾驶策略分解为四个协同模块，以归一化不确定性信号 $\bar{\sigma}$ 作为贯穿全链路的可靠性接口，实现从场景表示到跨域迁移的统一调控。

### 3.1 以自车为中心的关系图编码器

传统端到端方法将多模态传感器数据展平为全局张量，缺乏对交互实体不确定性的显式建模。本模块将场景建模为以自车为根节点的有向关系图，每个场景实体 $e_i^t$ 通过一条有向边连接到自车节点，边的特征向量为：

$$\mathbf{e}_i^t = [\Delta p_i, \Delta v_i, c_i, \kappa_i, \sigma_i^2] \quad \text{(Eq. 6)}$$

其中 $\Delta p_i$ 为相对位置，$\Delta v_i$ 为相对速度，$c_i$ 为语义类别编码，$\kappa_i$ 为车道几何曲率，$\sigma_i^2$ 为每实体的 aleatoric 方差（由感知模块估计）。

**不确定性加权因果注意力**是此模块的核心创新。传统注意力仅基于距离或语义相似度分配权重，在感知噪声或遮挡场景下容易过度关注不可靠实体或忽略高风险目标。本方法将每实体的不确定性 $\sigma_i^2$ 嵌入注意力核：

$$\alpha_i = \mathrm{softmax}_i\left(-\frac{\|\Delta p_i\|_2^2}{\sigma_i^2 + \varepsilon}\right), \quad z_t = \sum_{i=1}^{M} \alpha_i W_e \mathbf{e}_i^t \quad \text{(Eq. 7)}$$

**机制解释**：当某实体的 $\sigma_i^2$ 较大（感知不可靠）时，即使其空间距离很近，注意力权重 $\alpha_i$ 也会被抑制，避免策略对噪声检测过度反应；反之，对于低不确定性但距离较远的高风险实体，注意力权重得以保留。$\varepsilon$ 为数值稳定常数。

聚合后的交互嵌入 $z_t$ 与自车动态特征拼接，形成决策状态：

$$s_t = [z_t; v_{\text{ego}}; a_{\text{ego}}^{t-1}; d_{\text{goal}}; \phi_{\text{lane}}; \sigma_{\text{ale}}^2] \quad \text{(Eq. 8)}$$

其中 $v_{\text{ego}}$ 为自车速度，$a_{\text{ego}}^{t-1}$ 为上一时刻动作，$d_{\text{goal}}$ 为到目标点的路径进度，$\phi_{\text{lane}}$ 为车道几何特征，$\sigma_{\text{ale}}^2$ 为全局 aleatoric 方差（作为决策时的不确定性上下文）。

### 3.2 可微多目标奖励塑形

稀疏事件奖励（如碰撞时给予大负奖励）在复杂连续控制任务中梯度信号微弱，优化困难。本模块将安全、进度、舒适和不确定性四个目标统一为可微奖励函数：

$$r_t = w_s r_s + w_p r_p + w_c r_c + w_u r_u \quad \text{(Eq. 9)}$$

**安全奖励** $r_s$ 采用平滑代理惩罚替代硬阈值约束：

$$r_s = 1 - \kappa_L \psi_L(d_L, \mu_A) - \kappa_P \psi_P - \kappa_R \rho_t \quad \text{(Eq. 10)}$$

其中 $\psi_L(d_L, \mu_A)$ 为横向偏离的平滑惩罚，$d_L$ 为自车到当前车道中心线的点线距离（由 Eq. 3.2 定义），$\mu_A$ 为场景上下文隶属度，用于动态收紧可接受偏离范围；$\psi_P$ 为接近碰撞的平滑代理；$\rho_t$ 为交通信号违规指示。所有项均连续可微，避免梯度截断。

**进度奖励** $r_p$ 鼓励沿路线前进，**舒适奖励** $r_c$ 惩罚急动度 $j_t = \|a_t^{\text{veh}} - a_{t-1}^{\text{veh}}\|_2 / \Delta t$ 和转向速率 $\dot{\delta}_t$，**不确定性奖励** $r_u$ 将决策时归一化不确定性 $\bar{\sigma}$ 纳入优化目标，引导策略主动寻求低不确定性状态。

### 3.3 联合 Aleatoric-Epistemic 不确定性估计与熵门控探索

本模块同时估计两类不确定性：**aleatoric 不确定性**（数据固有噪声，由感知模块输出方差 $\sigma_{\text{ale}}^2$）和 **epistemic 不确定性**（模型知识不足，通过集成网络的预测分歧估计）。两者联合归一化得到决策时不确定性信号 $\bar{\sigma} \in [0,1]$。

**熵门控探索**是此模块的关键创新。传统 RL 使用固定或按步衰减的熵系数，忽略了不同状态的风险差异。本方法利用 $\bar{\sigma}$ 动态调节策略熵：

$$\mathcal{L}_{\text{ent}} = -\beta(\bar{\sigma}) H(\pi_\theta(\cdot|s_t)), \quad \beta(\bar{\sigma}) = \beta_0(1 - \bar{\sigma}) \quad \text{(Eq. 15)}$$

**机制解释**：当 $\bar{\sigma}$ 较高（模型对当前状态不确定）时，$\beta(\bar{\sigma})$ 减小，策略熵被抑制，促使策略选择更保守、更确定的行为，避免在不确定状态下进行高风险探索；当 $\bar{\sigma}$ 较低（模型置信度高）时，熵系数恢复，允许更充分的探索。这建立了“不确定性-探索”的直接因果耦合。

消融实验（Table 2）证实：移除熵门控（w/o Ent. Gate）导致策略方差增加 21%，碰撞率升高 0.002/km，验证了 $\bar{\sigma}$-熵耦合的必要性。

### 3.4 因果-不确定性迁移对齐与 MAML 初始化

跨域迁移的核心挑战在于源域和目标域之间存在感知分布偏移和因果结构差异。本模块通过三个对齐目标实现可靠迁移：

$$\mathcal{L}_{\text{trans}} = \mathcal{L}_{\text{KL}} + \lambda_\alpha \text{MMD}(\alpha_s, \alpha_t) + \lambda_u \|u_s - u_t\|^2 \quad \text{(Eq. 16)}$$

- **$\mathcal{L}_{\text{KL}}$**：对齐源域和目标域的动作分布，保证行为一致性；
- **$\text{MMD}(\alpha_s, \alpha_t)$**：通过最大均值差异对齐两域的注意力分布，确保模型在目标域中关注与源域因果相关的实体；
- **$\|u_s - u_t\|^2$**：对齐不确定性统计量（均值和方差），使目标域的不确定性校准与源域一致。

此外，采用 **MAML 元初始化**获取跨域快速适应的小样本起点：

$$\theta^* = \arg\min_\theta \sum_{d\in\mathcal{D}} \mathcal{L}_{\text{RL}}^{(d)}(\theta - \alpha\nabla_\theta \mathcal{L}_{\text{RL}}^{(d)}(\theta)) \quad \text{(Eq. 17)}$$

其中 $\mathcal{D}$ 为多个源域集合，内层梯度更新模拟小样本适应过程，外层优化寻找对域变化鲁棒的初始化参数。

消融实验（Table 2）表明：去除迁移目标（w/o Transfer）使 Town02 DS 从 214.3 降至 194.1，去除 MAML 降至 200.8，证明迁移对齐和元初始化的互补贡献。

### 补充图表

![[assets/figures/papers/paper_list_l2719_https_openaccess_thecvf_com_content_CVPR2026_html_Borhan_Reliable_Policy/figures/003_Figure_3.jpg]]
*Figure 3: Ego-relational state on Town10HD: CTE and heading error reduced by uncertainty-weighted attention versus baselines*

![[assets/figures/papers/paper_list_l2719_https_openaccess_thecvf_com_content_CVPR2026_html_Borhan_Reliable_Policy/figures/005_Figure_6.jpg]]
*Figure 6: Uncertainty-aware exploration and safety metrics*

![[assets/figures/papers/paper_list_l2719_https_openaccess_thecvf_com_content_CVPR2026_html_Borhan_Reliable_Policy/figures/006_Figure_5.jpg]]
*Figure 5: Reward comparison where differentiable multi-objective shaping yields higher, more stable returns than baselines*

## 实验与分析

### 闭环驾驶主结果

Table 1 汇总了所提框架与四个代表性端到端驾驶基线——**ST-P3**（Hu et al., ECCV 2022）、**ThinkTwice**（Jia et al., CVPR 2023）、**TransFuser**（Chitta et al., TPAMI 2023）和**RaSc**（Fan et al., ECCV 2024）——在三个CARLA城镇（Town02、Town05、Town10HD）上的闭环评估结果。评估指标覆盖驾驶分数（DS）、路线完成率（RC）、碰撞率、违规分数（IS）等关键安全与进度维度。

![[assets/figures/papers/paper_list_l2719_https_openaccess_thecvf_com_content_CVPR2026_html_Borhan_Reliable_Policy/figures/007_Table_1.jpg]]
*Table 1: Closed-loop results across towns. Town02 values averaged over 20 episodes; Town05 and Town10HD over 20 episodes each*

在最具挑战性的Town02场景中，完整模型取得DS 214.3、RC 84.1%、碰撞率0.005/km、IS 0.94，在所有指标上均显著超越对比方法。该结果构成因果-不确定性统一接口有效性的核心证据——通过将归一化不确定性信号 $\bar{\sigma}$ 同时注入状态表示、奖励塑造和策略迁移，模型在分布偏移显著的跨城镇场景中保持了安全性与泛化能力。

在Town10HD上，所提方法的平均CTE降至0.65，较ST-P3（≈0.91）降低28.6%，较ThinkTwice降低20.7%，较TransFuser和RaSc分别降低15.6%和11.0%；航向误差降至0.31，较ST-P3降低47.5%。这些改进直接归因于不确定性加权注意力机制对交互特征的选择性聚合——高不确定性实体被自适应降权，避免了噪声检测对控制决策的干扰。

Figure 2 提供了定性轨迹对比。在雾天交叉口场景中，所提方法（绿色轨迹）执行谨慎减速，CTE保持在0.65；RaSc（红色轨迹）则出现明显横向漂移，CTE超过0.73。在行人过街场景中，所提方法实现无碰撞通过，而RaSc发生碰撞事件。这一对比直观展示了不确定性感知控制层在安全关键场景中的决策优势。

![[assets/figures/papers/paper_list_l2719_https_openaccess_thecvf_com_content_CVPR2026_html_Borhan_Reliable_Policy/figures/002_Figure_2.jpg]]
*Figure 2: Trajectory comparison on Town10HD. Proposed method (green, left) vs. RaSc [8] (red, right). (a) Fog intersection: cautious deceleration (CTE = 0.65) vs. lateral drift (CTE > 0.73). (b) Pedestrian crossing: no collision (CTE = 0.65) vs. collision event (CTE = 0.73)*

### 组件消融分析

Table 2 报告了在Town10HD和Town02上的组件级消融结果，系统验证了每个设计选择的独立贡献。

![[assets/figures/papers/paper_list_l2719_https_openaccess_thecvf_com_content_CVPR2026_html_Borhan_Reliable_Policy/figures/008_Table_2.jpg]]
*Table 2: Component-wise ablation on Town10HD and Town02*

**不确定性加权注意力**：移除该组件（w/o Unc. Attn.）后，CTE升高0.11，航向误差升高0.07。这表明基于每实体不确定性的注意力权重（Eq. 7）对维持横向稳定性至关重要。当注意力退化为仅依赖距离的普通softmax时，模型无法有效区分高置信度感知与噪声检测，导致对高风险交互主体的响应失当。

**熵门控探索**：移除不确定性门控（w/o Ent. Gate）导致策略方差增加21%，碰撞率增加0.002/km。这证实了 $\bar{\sigma}$-熵耦合机制（Eq. 15）的必要性——高不确定性时 $\beta(\bar{\sigma})$ 趋近于零，抑制探索以防止危险动作；低不确定性时恢复探索以促进策略优化。若将熵系数设为全局常数，则丧失了风险感知探索能力。

**可微多目标奖励**：用基于事件的稀疏奖励替代可微奖励（EventReward）后，DS下降18.4点，CTE升高0.09。可微奖励通过平滑代理函数（Eq. 10-13）为策略梯度提供连续优化信号，避免了事件奖励的稀疏性和高方差问题，对优化稳定性至关重要。

**因果-不确定性迁移对齐**：去除迁移目标（w/o Transfer）使Town02 DS从214.3骤降至194.1；去除MAML初始化（w/o MAML）则降至200.8。这两个消融条件揭示了迁移机制的互补性：KL+MMD+不确定性匹配损失（Eq. 16）对齐了源域与目标域的动作分布、注意力模式和不确定性统计量，而MAML元初始化（Eq. 17）提供了快速适应的参数起点。二者协同作用，使零样本泛化性能显著优于仅依赖感知层面适配的基线方法。

### 失败模式与局限性

尽管整体性能优异，分析揭示了以下失败模式与局限：

1. **极端域差异下的迁移退化**：当目标域的道路拓扑、交通规则或传感器配置与源域差异过大时，因果-不确定性迁移对齐的效果衰减。这是因为Eq. 16中的MMD和不确定性匹配假设源域与目标域存在可对齐的统计结构，极端差异可能违反该假设。

2. **集成模型的计算开销**：联合估计aleatoric和epistemic不确定性需要维护集成预测头，推理时计算量显著高于单头策略网络。论文未报告实时性指标，实际部署可行性需手动验证。

3. **仅限仿真验证**：所有实验基于CARLA仿真器，未在真实车辆上部署测试。仿真到现实的域迁移（Sim2Real）是开放问题，不确定性接口在该场景下的有效性尚待验证。

4. **元学习预训练成本**：MAML初始化需要额外的跨域元训练阶段，增加了训练时间和数据需求。

### 公平性说明

所有方法在相同CARLA版本、地图（Town10HD、Town05、Town02）、天气条件和交通密度下评估，每场景运行20个回合取平均。超参数通过网格搜索确定，论文提供了灵敏度分析。对比基线均使用其开源实现和推荐配置，确保比较的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l2719_https_openaccess_thecvf_com_content_CVPR2026_html_Borhan_Reliable_Policy/figures/004_Figure_4.jpg]]
*Figure 4: Route completion metrics. Off-road (%) decreases and goal rate increases when the policy uses the causal state*

## 方法谱系与知识库定位

### 与现有基线的结构性差异

本工作与现有端到端驾驶方法的核心分歧在于**控制层缺乏统一的因果与不确定性接口**。主流方法在感知编码、奖励设计、探索策略和跨域迁移上各自独立设计，导致分布偏移下安全性差、泛化能力弱。

**ST-P3**（Hu et al., ECCV 2022）采用时空透视表示进行端到端规划，但其状态表示不包含显式的不确定性建模，奖励函数依赖稀疏事件信号。本文以归一化不确定性 $\bar{\sigma}$ 为统一接口，同时驱动不确定性加权注意力（Eq. 7）、熵门控探索（Eq. 15）和因果-不确定性迁移对齐（Eq. 16），在 Town10HD 上将碰撞率从 ST-P3 的 0.011/km 降至 0.006/km（−45.5%），CTE 从约 0.91 降至 0.65（−28.6%）。

**ThinkTwice**（Jia et al., CVPR 2023）和 **TransFuser**（Chitta et al., TPAMI 2023）均采用全局张量融合的多模态表示，缺乏对场景实体不确定性的细粒度建模。本文以自车为中心的关系图取代全局张量，通过基于每实体不确定性 $\sigma_i^2$ 的注意力权重 $\alpha_i = \mathrm{softmax}_i(-\|\Delta p_i\|^2/(\sigma_i^2+\varepsilon))$ 聚合交互特征，在 Town10HD 上 CTE 分别低于 ThinkTwice 20.7%、低于 TransFuser 15.6%，航向误差分别降低 32.6% 和 26.2%。

**RaSc**（Fan et al., ECCV 2024）虽在感知层面引入了关系建模，但缺少不确定性门控和因果迁移机制。定性对比（Figure 2）显示，在雾天交叉口场景中，RaSc 发生横向漂移（CTE > 0.73），而本文方法实现谨慎减速（CTE = 0.65）；在行人横穿场景中，RaSc 发生碰撞，本文方法无碰撞通过。

### 方法谱系中的定位

从技术谱系看，本工作处于**不确定性感知强化学习**与**因果迁移学习**的交叉点：

- **不确定性建模线**：传统方法将 aleatoric 和 epistemic 不确定性分离估计或仅用于感知层。本文提出联合估计两类不确定性，并将归一化信号 $\bar{\sigma}$ 作为控制层的可靠性接口——既通过 $\beta(\bar{\sigma}) = \beta_0(1-\bar{\sigma})$ 动态调节策略熵（高不确定性时抑制探索），又作为奖励项 $r_u$ 的组成部分引导安全行为。

- **因果迁移线**：现有迁移方法多停留在感知层面的域适配。本文的因果-不确定性迁移目标 $\mathcal{L}_{trans} = \mathcal{L}_{KL} + \lambda_\alpha \mathrm{MMD}(\alpha_s, \alpha_t) + \lambda_u \|u_s - u_t\|^2$ 同时对齐动作分布、注意力分布和不确定性统计量，辅以 MAML 元初始化（Eq. 17）实现小样本快速适应。消融实验证实：去除迁移目标使 Town02 DS 从 214.3 降至 194.1，去除 MAML 降至 200.8，二者互补贡献显著。

- **奖励塑造线**：从稀疏事件惩罚（如 ST-P3）到阈值惩罚再到本文的可微多目标奖励 $r_t = w_s r_s + w_p r_p + w_c r_c + w_u r_u$，其中安全项 $r_s$ 使用平滑代理函数 $\psi_L(d_L, \mu_A)$ 替代硬阈值，使优化更稳定。消融中替换为事件奖励（EventReward）后 DS 下降 18.4 点，CTE 升高 0.09。

### 适用边界与局限

1. **仿真封闭性**：所有验证基于 CARLA 仿真（Town10HD、Town05、Town02），未在真实车辆上部署。从仿真到真实的视觉域差、动力学差异和控制延迟等未经验证。

2. **集成模型的计算开销**：框架包含关系图编码、联合不确定性估计、多目标奖励计算和迁移对齐等多个模块，推理时计算量较大，未进行实时性优化。在 CARLA 嵌入式部署场景中可能面临帧率瓶颈。

3. **迁移对齐的域相似性依赖**：因果-不确定性迁移目标依赖源域和目标域在场景结构、实体类型和交互模式上的相似性。对极端域差异（如从城市场景迁移到高速公路场景），注意力分布对齐和不确定性匹配的有效性可能下降，需要额外适应阶段。

4. **元学习的前置训练成本**：MAML 初始化需要跨多个源域的元训练阶段，增加了训练流程的复杂度和计算成本。当可用的源域数量有限时，元初始化的泛化优势可能减弱。

### 开放问题

1. **Sim2Real 迁移中的不确定性接口**：如何将当前的联合 aleatoric-epistemic 不确定性估计扩展到真实驾驶场景？真实传感器噪声、感知失败和模型误差的不确定性特性与仿真存在本质差异，统一不确定性接口的标定和适配是核心挑战。

2. **介入式因果建模的潜力**：当前方法通过注意力分布对齐实现因果一致性，但属于观测性因果推断。是否可以通过介入式因果建模（如对特定实体施加 do-操作）进一步提升迁移的因果保真度？

3. **实时部署的复杂度压缩**：如何通过模型蒸馏、注意力剪枝或不确定性估计的轻量化降低集成模型的计算开销，同时保持安全性指标的退化在可接受范围内？

4. **标准化基准的泛化验证**：当前实验在自定义 CARLA 场景上进行，在 CARLA Leaderboard 和 Bench2Drive 等标准化基准上的表现尚待验证。这些基准的交通密度、路线复杂度和评估协议更具挑战性，可进一步检验框架的泛化边界。

## 原文 PDF

![[paperPDFs/CVPR_2026/Reliable_Policy_Transfer_for_Safety_Aware_End_to_End_Driving_with_Deep_Reinforcement_Learning.pdf]]
