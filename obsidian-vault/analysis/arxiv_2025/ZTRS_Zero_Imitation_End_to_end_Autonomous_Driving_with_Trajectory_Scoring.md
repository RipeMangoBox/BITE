---
title: "ZTRS: Zero-Imitation End-to-end Autonomous Driving with Trajectory Scoring"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/ZTRS_Zero_Imitation_End_to_end_Autonomous_Driving_with_Trajectory_Scoring.pdf
aliases:
- ZZITSEPO
- ZTRS
tags:
- arxiv_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: Exhaustive Policy Optimization（EPO）：将轨迹规划转化为离散动作集上的评分问题，在离线数据上对所有可枚举动作计算优势函数（EPDMS得分减去时序一致性修正），通过穷举策略梯度提供密集监督，使高维传感器端到端规划器无需人类示范即可从零训练。
primary_logic: 通过将连续轨迹空间离散化为可枚举动作集，并结合离线强化学习与穷举策略优化（EPO），可利用开环规则奖励（EPDMS）替代人类示范，在保留高维视觉输入的条件下从零训练出鲁棒的端到端规划器，彻底消除对模仿学习的依赖。
claims:
- ZTRS在Navhard基准上达到最先进水平（EPDMS 45.5%），超越所有基于IL的传感器方法。
- 在HUGSIM闭环驾驶基准上，ZTRS的路线完成率（RC）超越IL基线GTRS-Dense 4.6个百分点。
- 消融实验表明，使用完整动作空间上的似然优化（EPO）相比仅对采样动作计算对数似然，性能显著提升；加入时序一致性修正项b后EC指标提升23.4%。
- ZTRS是首个完全消除模仿学习、仅通过奖励从高维真实世界图像中学习端到端规划的框架。
---

# ZTRS: Zero-Imitation End-to-end Autonomous Driving with Trajectory Scoring

> [!tip] 核心洞察
> 通过将连续轨迹空间离散化为可枚举动作集，并结合离线强化学习与穷举策略优化（EPO），可利用开环规则奖励（EPDMS）替代人类示范，在保留高维视觉输入的条件下从零训练出鲁棒的端到端规划器，彻底消除对模仿学习的依赖。

| 字段 | 内容 |
|------|------|
| 中文题名 | ZTRS：基于轨迹评分的零模仿端到端自动驾驶 |
| 英文题名 | ZTRS: Zero-Imitation End-to-end Autonomous Driving with Trajectory Scoring |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2510.24108) · [Code](https://github.com/woxihuanjiangguo/ZTRS) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | ZTRS (Zero-Imitation Trajectory Scoring with Exhaustive Policy Optimization) |
| Dataset | Navhard, Navtest, HUGSIM |

> [!tip] 效果简介
> - Navhard (开环规划，挑战性真实+合成场景) 上，EPDMS ↑ 45.5% (ZTRS V2-99) vs 45.3% (GTRS-Dense ViT-L, 最佳IL传感器方法) (+0.2%)。
> - Navtest (开环规划，通用真实场景) 上，EPDMS ↑ 86.2 (ZTRS ViT-L) vs 85.6 (HydraMDP++ ViT-L) (+0.6)。
> - HUGSIM (闭环驾驶，3DGS渲染场景) 上，RC ↑ / HD-Score ↑ RC 42.6 / HD-Score 28.9 (ZTRS) vs RC 38.0 / HD-Score 28.6 (GTRS-Dense) (+4.6% RC / +0.3 HD-Score)。

## 概述

端到端自动驾驶方法长期面临一个根本性两难：**模仿学习（Imitation Learning, IL）** 依赖人类专家示范，但受限于示范质量与协变量偏移（covariate shift）；**强化学习（Reinforcement Learning, RL）** 虽可通过仿真规模化训练，却仅能操作低维符号输入（如3D目标检测框与地图），无法利用高维传感器中的丰富语义信息。至今尚无方法能在保留原始传感器输入的前提下，完全通过奖励信号训练端到端规划器。

本文提出 **ZTRS（Zero-Imitation Trajectory Scoring with Exhaustive Policy Optimization）**，首次彻底消除对模仿学习的依赖。其核心思想是：将连续轨迹空间离散化为可枚举的动作集（16384条候选轨迹），利用开环规则奖励 **EPDMS** 替代人类示范作为监督信号，并通过**穷举策略优化（Exhaustive Policy Optimization, EPO）**——一种针对可枚举动作与奖励定制的策略梯度变体——在离线数据上对所有动作计算优势加权似然梯度，提供密集监督，从而在保留高维视觉输入的条件下从零训练出鲁棒的端到端规划器。

实验结果表明，ZTRS在三个基准上展现了强劲性能：
- 在 **Navhard**（挑战性开环规划基准）上达到最先进水平（EPDMS 45.5%），超越所有基于IL的传感器方法；
- 在 **HUGSIM**（3DGS渲染的闭环驾驶基准）上，路线完成率（RC）超越IL基线 GTRS-Dense 4.6个百分点；
- 消融实验证实，穷举策略优化相比仅对采样动作计算对数似然，EPDMS提升7.5%；加入时序一致性修正项后，舒适性指标EC提升23.4%。

ZTRS的成功表明，通过穷举密集优化可克服从零训练的冷启动问题，使端到端规划器无需任何人类示范即可从高维传感器数据中学习驾驶策略。

## 背景与动机

端到端自动驾驶旨在从高维传感器输入（如相机图像）直接输出规划轨迹，省去传统模块化方法中感知、预测、规划的级联流程。然而，该领域长期面临一个根本性困境：**模仿学习（Imitation Learning, IL）与强化学习（Reinforcement Learning, RL）各执一端，无法兼得**。

以**UniAD**（Hu et al., CVPR 2023）、**VAD**（Jiang et al., ICCV 2023）、**DriveSuprim**（Yao et al., arXiv 2025）等为代表的IL方法，通过拟合人类专家示范轨迹来学习驾驶策略，能够直接操作高维视觉输入。但其性能受限于两个瓶颈：（1）人类示范的质量上限——专家数据中的次优行为会直接污染学习目标；（2）协变量偏移（covariate shift）——训练分布与测试分布不匹配时，误差会沿时序累积，导致灾难性偏离。IL方法本质上在“模仿”，而非“理解”驾驶的优劣。

另一方面，RL方法可通过仿真环境中的试错交互获得规模化训练信号，不受人类示范质量约束。但现有RL驾驶工作（如**PDM-Closed**, Dauner et al., CoRL 2023）仅能操作低维符号输入（3D目标检测框、地图元素等），无法利用原始传感器中的丰富语义信息。这是因为高维视觉空间中的RL探索极其困难，奖励稀疏且方差巨大。

由此形成一个清晰的研究缺口：**尚无方法能够同时保留原始传感器输入，并完全通过奖励信号训练端到端规划器**。IL方法有视觉但受限于示范，RL方法有奖励但丢失了视觉。ZTRS的动机正是打破这一僵局——通过将连续轨迹空间离散化为可枚举动作集，并设计一种适用于该离散空间的穷举策略优化算法，使得高维视觉输入上的零模仿RL训练成为可能。

## 核心创新

### 瓶颈诊断：模仿学习与强化学习的两难困境

端到端自动驾驶的主流范式——模仿学习（Imitation Learning, IL）——面临一个根本性瓶颈：它以人类专家示范为监督信号，因而受限于示范质量与协变量偏移（covariate shift）。另一方面，强化学习（Reinforcement Learning, RL）虽可通过仿真规模化训练，但现有RL驾驶方法仅能操作低维符号输入（如3D目标检测框与高清地图），无法利用高维传感器（相机图像）中蕴含的丰富语义信息。**在ZTRS之前，尚无方法能在保留原始传感器输入的条件下，完全通过奖励信号训练端到端规划器**。

ZTRS的核心洞察在于：若能**将连续轨迹空间离散化为可枚举的动作集**，并借助离线强化学习与规则奖励（EPDMS）替代人类示范，便可在保留高维视觉输入的条件下从零训练出鲁棒的端到端规划器，彻底消除对模仿学习的依赖。

### 关键创新机制：Exhaustive Policy Optimization (EPO)

ZTRS的方法论核心是**Exhaustive Policy Optimization（EPO）**——一种针对可枚举动作与奖励量身定制的策略梯度变体。其工作原理如下：

1. **动作空间离散化**：将连续轨迹空间通过K-means聚类压缩为16384条候选轨迹，每条轨迹覆盖约4秒的驾驶行为（10Hz采样率）。这一离散化使得“对所有动作穷举计算优势函数”在计算上成为可能。

2. **穷举策略梯度**：EPO不依赖采样来估计策略梯度，而是对动作集中**每一条可能轨迹**计算其优势加权似然梯度：

$$g := \sum_{\substack{a' \in \mathcal{A} \\ s \sim \mathcal{D}}} \Psi(s, a') \nabla_{\theta} \pi_{\theta}(a' \mid s)$$

其中 $\Psi(s, a')$ 为优势函数，$\pi_{\theta}(a' \mid s)$ 为策略网络输出的动作概率。这一穷举计算为训练提供了**密集监督信号**——每个状态下所有16384个动作均参与梯度更新，而非仅依赖采样或教师动作。

3. **奖励信号设计**：优势函数定义为EPDMS规则得分减去时序一致性修正项：

$$\Psi(s_t, a_t) = \mathcal{E}(s_t, a_t) - b(s_t, a_t, a_{t-1}), \quad b = \lambda \mathbb{I}[\mathrm{EC}(a_{t-1}, a_t)]$$

其中 $\mathcal{E}(s_t, a_t)$ 为开环规划指标EPDMS（综合安全惩罚项与舒适性加权项），$b$ 为时序一致性惩罚项（检测相邻帧间的舒适性违规，$\lambda=0.2$）。最终 $\Psi$ 被归一化至零均值单位方差，以稳定训练。

### 范式转变：三个维度的系统性创新

ZTRS相对于IL基线方法（如**DriveSuprim** (Yao et al., arXiv 2025)、**GTRS-Dense** (Li et al., arXiv 2025)、**HydraMDP++** (Li et al., arXiv 2025)等）实现了三个关键维度的范式转变：

| 创新维度 | IL基线方案 | ZTRS方案 |
|---------|-----------|---------|
| **学习范式** | 模仿学习，以人类示范轨迹为监督信号 | 离线强化学习，以EPDMS规则奖励为监督信号，完全无需人类示范 |
| **策略优化方式** | 对采样/教师动作计算对数似然梯度 | EPO：对动作集中所有16384条轨迹计算优势加权似然梯度，提供密集监督 |
| **训练目标** | 人类示范轨迹 | EPDMS规则得分减去时序一致性修正项：$\Psi = \mathcal{E} - b$ |

### 创新有效性的证据链

消融实验系统性地验证了上述创新的必要性：

- **学习范式转变**：将最大EPDMS轨迹作为模仿目标（伪标签）会导致性能显著下降，证明直接使用奖励作为监督优于将其转换为伪标签。这表明EPO的密集奖励信号是核心驱动力，而非简单的标签替换。

- **穷举vs采样**：使用完整动作空间上的似然优化（EPO）相比仅对采样动作计算对数似然，EPDMS提升7.5%，充分证明穷举密集监督的有效性。采样方法无法提供足够的梯度信息覆盖整个动作空间。

- **时序一致性修正**：加入修正项 $b$ 后，EC（Ego Comfort）指标提升23.4%，有效抑制了轨迹震荡问题。这揭示了纯奖励驱动训练的一个关键失败模式——缺乏时序约束会导致规划不稳定。

### 方法定位：轨迹评分器架构

ZTRS继承了轨迹评分器（Trajectory Scorer）的架构范式（与GTRS-Dense、DriveSuprim等同属一类），但其**训练机制发生了根本性变化**。框架由五个模块组成：图像骨干网络（从三视角拼接图像中提取视觉令牌）、轨迹分词器（将K-means聚类轨迹编码为查询向量）、Transformer解码器（轨迹查询通过交叉注意力获取视觉上下文）、策略头（输出动作概率分布 $\pi(\cdot|s)$，由EPO训练）以及评分头（预测各EPDMS子指标的规则得分，以二分类损失训练）。这一架构使得ZTRS成为**首个完全消除模仿学习、仅通过奖励从高维真实世界图像中学习端到端规划的框架**。

## 整体框架

ZTRS 的整体架构围绕一个核心设计原则展开：**将连续轨迹规划问题转化为离散动作集上的评分与选择问题**，从而使得端到端规划器能够完全通过奖励信号从零训练，无需任何人类示范。如图 2 所示，框架由五个模块串联构成，形成“传感器输入 → 轨迹评分 → 策略输出”的完整推理链路。

### 输入与分词

系统接收两类输入：**前视拼接图像**（分辨率 512×2048，由三视角图像拼接而成）和**固定轨迹候选集**。图像骨干网络（默认使用 DD3D 预训练的 V2-99 或 Depth-Anything 预训练的 ViT-L）将图像编码为 $L$ 个图像令牌 $\{x_{\text{img}}^i\}_{i=1}^L$。同时，轨迹分词器将预先通过 K-means 聚类得到的 $n=16384$ 条候选轨迹（每条约 4 秒 @ 10Hz）编码为轨迹查询向量 $\{x_{\text{traj}}^i\}_{i=1}^n$。

### Transformer 解码器

轨迹查询向量作为 Transformer 解码器的查询（query），图像令牌作为键（key）和值（value）。通过交叉注意力机制，每条轨迹查询从图像令牌中提取与自身相关的视觉上下文信息，得到富含场景语义的轨迹表征。这一设计使得轨迹评估能够直接利用高维传感器中的细粒度语义（如道路边界、障碍物轮廓、交通标志），而非依赖中间符号化表征（3D 目标框 / 地图）。

### 双头输出

解码后的轨迹表征被并行送入两组头部：

- **评分头**：$m$ 个评分头分别预测每条轨迹在 EPDMS 各子指标上的规则得分 $\{S_i(\cdot|s)\}_{i=1}^m$，以二分类损失训练。这些预测得分在推理时用于计算 EPDMS 综合指标，但训练阶段仅作为辅助任务。
- **策略头**：将轨迹表征映射为动作概率分布 $\pi(\cdot|s)$，输出每条轨迹被选中的似然。该分布由 Exhaustive Policy Optimization（EPO）训练，训练目标为优势加权似然梯度：

$$g := \sum_{\substack{a' \in \mathcal{A} \\ s \sim \mathcal{D}}} \Psi(s, a') \nabla_{\theta} \pi_{\theta}(a' \mid s)$$

其中优势函数 $\Psi(s_t, a_t) = \mathcal{E}(s_t, a_t) - b(s_t, a_t, a_{t-1})$，即 EPDMS 规则得分减去时序一致性修正项 $b = \lambda \mathbb{I}[\mathrm{EC}(a_{t-1}, a_t)]$（$\lambda=0.2$），最终归一化至零均值单位方差。

### 推理流程

推理时，图像骨干提取视觉令牌，轨迹分词器编码候选轨迹集，Transformer 解码器完成交叉注意力交互后，策略头输出每条轨迹的概率分布。系统选择概率最高的轨迹作为规划结果，无需额外的后处理或轨迹优化步骤。

### 与现有范式的根本差异

图 1 对比了三种端到端自动驾驶范式。模块化方法依赖感知-预测-规划的解耦流水线；模仿学习方法以人类示范为监督信号，受限于示范质量和协变量偏移；ZTRS 则完全消除对模仿学习的依赖，在保留原始高维传感器输入的前提下，仅通过 EPDMS 规则奖励和 EPO 穷举策略梯度从零训练，实现了“零模仿”的端到端规划。

### 补充图表

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2510_24108/figures/001_Figure_1.jpg]]
*Figure 1: Comparisons between three paradigms for end-to-end autonomous driving*

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2510_24108/figures/002_Figure_2.jpg]]
*Figure 2: The Overall Framework of ZTRS. Given offline sensor data and a fixed set of trajectories, ZTRS first tokenizes these two modalities. In a Transformer Decoder, the trajectory tokens attend to image tokens to acquire the context. Finally, scoring heads and a policy head map the trajectory tokens to rule-based scores and action likelihoods*

## 核心模块与公式推导

### 2.1 整体框架：从连续回归到离散评分

ZTRS 将轨迹规划重新定义为**离散动作集上的评分问题**，而非直接回归连续轨迹参数。其核心架构由五个模块串联构成：

1. **图像骨干网络（Image Backbone）**：从三视角拼接的前视图（512×2048）中提取 $L$ 个图像令牌 $\{x_{\text{img}}^i\}_{i=1}^L$。默认采用 DD3D 预训练的 V2-99 或 Depth-Anything 预训练的 ViT-L。
2. **轨迹分词器（Trajectory Tokenizer）**：将 K-means 聚类得到的 $n=16384$ 条固定候选轨迹（每条约 4 秒 @10Hz）编码为轨迹查询向量 $\{x_{\text{traj}}^i\}_{i=1}^n$。
3. **Transformer 解码器（Transformer Decoder）**：轨迹查询通过交叉注意力机制与图像令牌交互，获取视觉上下文信息。
4. **策略头（Policy Head）**：将参与后的轨迹查询映射为动作概率分布 $\pi_\theta(\cdot \mid s)$，由 EPO 训练。
5. **评分头（Scoring Heads）**：预测每条轨迹在 EPDMS 各子指标上的规则得分，以二分类损失训练。

这一设计的关键在于：策略头和评分头共享同一组轨迹查询表示，但前者输出概率分布用于动作选择，后者输出规则得分用于奖励计算——两者解耦，使策略学习完全摆脱对人类示范的依赖。

### 2.2 策略梯度定理的穷举形式

标准策略梯度定理将梯度表达为期望形式：

$$g := \mathbb{E}\left[\Psi(s, a) \nabla_\theta \log \pi_\theta(a \mid s)\right]$$

当动作空间 $\mathcal{A}$ 可枚举时，该期望可精确展开为求和形式，这是 EPO 的理论基础：

$$g = \sum_{a' \in \mathcal{A}} \Psi(s, a') \nabla_\theta \pi_\theta(a' \mid s)$$

其中 $\Psi(s, a')$ 为动作 $a'$ 在状态 $s$ 下的优势函数。与标准策略梯度依赖蒙特卡洛采样不同，求和形式允许对**所有**可枚举动作计算梯度贡献，从而提供密集且无偏的监督信号。

### 2.3 Exhaustive Policy Optimization (EPO)

EPO 将上述求和形式直接应用于离线数据集上的端到端训练。给定离线数据集 $\mathcal{D}$ 和可枚举动作集 $\mathcal{A}$，EPO 梯度定义为：

$$g := \sum_{\substack{a' \in \mathcal{A} \\ s \sim \mathcal{D}}} \Psi(s, a') \nabla_\theta \pi_\theta(a' \mid s)$$

**优势函数构造**是 EPO 的核心。ZTRS 采用开环规则指标 EPDMS 作为基础奖励，并引入时序一致性修正项以抑制轨迹震荡：

$$\Psi(s_t, a_t) = \mathcal{E}(s_t, a_t) - b(s_t, a_t, a_{t-1})$$

其中修正项定义为：

$$b(s_t, a_t, a_{t-1}) = \lambda \cdot \mathbb{I}[\mathrm{EC}(a_{t-1}, a_t)]$$

$\mathbb{I}[\mathrm{EC}(a_{t-1}, a_t)]$ 为指示函数，检测相邻帧轨迹间是否存在舒适性违规（EC 子指标），$\lambda=0.2$ 为手工设定的惩罚权重。最终 $\Psi$ 被归一化至零均值单位方差，以确保训练稳定性。

### 2.4 评估指标：EPDMS 与 HD-Score

**开环规划指标 EPDMS** 由惩罚项集合和加权项集合组合而成：

$$\mathcal{E}(s, a) = \left(\prod_{m \in S_{\text{pen}}} m(s, a)\right) \cdot \left(\frac{\sum_{m \in S_{\text{avg}}} w_m m(s, a)}{\sum_{m \in S_{\text{avg}}} w_m}\right)$$

- **惩罚项 $S_{\text{pen}}$**：包含 NC（无碰撞）、DAC（与自车距离）、DDC（与动态障碍物距离）、TLC（交通灯合规），以乘积形式施加硬约束——任一项为 0 则整体得分为 0。
- **加权项 $S_{\text{avg}}$**：包含 TTC（碰撞时间）、EP（自车进度）、LK（车道保持）、HC（人类相似度）、EC（舒适性），以加权平均衡量综合驾驶质量。

**闭环驾驶指标 HD-Score** 整合整段驾驶过程的路线完成率与逐帧安全/舒适性：

$$\mathrm{HD\text{-}Score} = RC \cdot \sum_{t=1}^{T} \left(\prod_{m \in \{\mathrm{NC}, \mathrm{DAC}\}} m(s_t, \tilde{a}_t)\right) \cdot \left(\frac{\sum_{m \in \{\mathrm{TTC}, \mathrm{HC}\}} w_m m(s_t, \tilde{a}_t)}{\sum_{m \in \{\mathrm{TTC}, \mathrm{HC}\}} w_m}\right)$$

其中 $RC$ 为路线完成率，$\tilde{a}_t$ 为闭环执行的动作。该指标将安全（NC/DAC 乘积）与舒适性（TTC/HC 加权平均）统一为单一标量，惩罚任何时刻的安全违规。

### 2.5 关键设计决策的因果机制

**为什么 EPO 优于采样策略梯度？** 消融实验（Table 4）揭示：仅对采样动作计算对数似然导致 EPDMS 下降 7.5%。原因在于 16384 条轨迹中绝大多数是低质量动作，随机采样极易遗漏高优势动作的梯度信号。EPO 通过穷举计算所有动作的梯度贡献，确保每条高优势轨迹都获得充分的参数更新，从而提供密集且无遗漏的监督。

**为什么直接使用奖励优于伪标签模仿？** 将最大 EPDMS 轨迹作为模仿目标导致性能显著下降（Table 4）。这一反直觉现象说明：开环 EPDMS 最高分轨迹未必是闭环最优解，将其硬性作为模仿目标会引入系统性偏差。EPO 通过优势加权（而非硬选择）保留了对多条高质量轨迹的概率质量，使策略在闭环执行中更具鲁棒性。

**时序修正项的作用机制**：不加修正项时，EPO 倾向于为连续帧选择 EPDMS 高但彼此不一致的轨迹，导致严重震荡。加入 $b$ 项后 EC 指标提升 23.4%，本质是通过惩罚相邻帧间的舒适性违规来强制时序平滑性，使规划轨迹在时域上连续可执行。

## 实验与分析

### 实验设置

ZTRS在三个基准上接受评估：**Navtest**（通用真实场景开环规划）、**Navhard**（挑战性真实+合成场景开环规划）和**HUGSIM**（3DGS渲染场景闭环驾驶）。所有方法均在Navtrain划分上训练，Navhard和HUGSIM的合成数据不参与训练，确保零样本评估的公平性。

训练使用24块NVIDIA A100 GPU，共训练15个epoch，batch size为528，学习率$2\times10^{-4}$，权重衰减为0.0。对比时使用相同的图像骨干网络（V2-99或ViT-L）以控制模型容量变量。**PDM-Closed**（Dauner et al., CoRL 2023）使用真实符号输入（3D目标/地图），不直接与传感器方法比较，仅作为性能上限参考。ZTRS训练中不使用人类过滤来计算EPDMS，奖励计算比某些基线更严格。

---

### 主实验结果

#### Navhard：挑战性场景开环规划

在Navhard基准上，ZTRS以V2-99骨干网络取得**45.5%的EPDMS总分**，达到所有传感器方法中的最先进水平（Table 1）。具体而言，ZTRS超越IL基线**GTRS-Dense**（ViT-L，45.3%）0.2个百分点，超越**DriveSuprim**（44.4%）1.1个百分点。值得注意的是，ZTRS在合成场景（Stage2）上的优势更为显著——合成数据未参与训练，这表明奖励驱动的训练在分布外场景下具有更强的泛化能力。

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2510_24108/figures/003_Table_1.jpg]]
*Table 1: Performance on the Navhard Benchmark. PDM-Closed uses ground-truth symbolic inputs for planning, while other methods rely on sensor data*

在子指标层面，ZTRS在舒适性指标（Comfort）上达到**98.4%**，显著超越所有IL基线；在无碰撞（NC）指标上达到**100%**，与PDM-Closed持平。这验证了EPDMS规则奖励能够直接引导模型学习安全约束，而无需依赖人类示范中的安全行为。

#### Navtest：通用场景开环规划

在Navtest基准上，ZTRS（ViT-L骨干）取得**86.2的EPDMS**，超越**HydraMDP++**（85.6，Li et al., arXiv 2025）0.6分，但仍落后于**DriveSuprim**（87.1，Yao et al., arXiv 2025）0.9分（Table 2）。这一结果表明：在通用真实场景下，精心设计的IL方法仍具有一定优势；但ZTRS在完全摒弃人类示范的条件下，已能将差距缩小至1%以内。

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2510_24108/figures/004_Table_2.jpg]]
*Table 2: Performance on the Navtest Benchmark*

#### HUGSIM：闭环驾驶零样本评估

闭环驾驶是检验端到端规划器真实能力的金标准。在HUGSIM基准的公开场景上，ZTRS取得**42.6%的路线完成率（RC）和28.9的HD-Score**，超越IL基线**GTRS-Dense**（RC 38.0，HD-Score 28.6）**4.6个百分点的RC和0.3的HD-Score**（Table 3）。同时，ZTRS大幅领先**UniAD**（Hu et al., CVPR 2023，RC 20.2）和**VAD**（Jiang et al., ICCV 2023，RC 13.5）等经典端到端规划器。

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2510_24108/figures/005_Table_3.jpg]]
*Table 3: Zero-shot Performance on the HUGSIM Benchmark. *Official results from Zhou et al. (2024) on both public and unreleased private scenarios. The rest are based on the public scenarios*

闭环结果的核心意义在于：ZTRS是**首个完全消除模仿学习、仅通过奖励从高维真实世界图像中学习端到端规划**的框架，且在闭环驾驶中超越了所有IL传感器基线。这证明了“零模仿”范式在闭环交互场景下的可行性。

---

### 消融实验

消融实验（Table 4）系统验证了ZTRS三个核心设计选择的有效性：

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2510_24108/figures/006_Table_4.jpg]]
*Table 4: Ablation study on different learning paradigms and targets*

**1. 学习范式：IL → RL。** IL基线（以人类轨迹为模仿目标）在Navtest上取得EC 80.5、EPDMS 86.2。若直接以最大EPDMS轨迹作为伪标签进行模仿学习，性能显著下降——这证明将奖励转换为伪标签会丢失奖励信号中的分布信息，直接使用奖励作为监督（即RL范式）是更优选择。

**2. 穷举策略优化（EPO）。** 使用完整动作空间（16384条轨迹）上的似然优化，相比仅对采样动作计算对数似然，**EPDMS提升7.5%**。这验证了穷举密集监督的有效性：当动作空间可枚举时，对每个动作计算优势加权梯度能提供比采样估计更丰富的学习信号。

**3. 时序一致性修正项b。** 加入修正项$b$（$\lambda=0.2$）后，**EC指标提升23.4%**（从59.2升至77.2），有效抑制了轨迹震荡。这揭示了纯奖励驱动训练的一个关键缺陷——逐帧独立优化会忽略帧间一致性，而简单的时序惩罚即可大幅缓解该问题。

**4. 动作空间规模。** Table 5分析了训练/推理时轨迹数量对性能的影响。在合成场景上，缩小动作空间提升性能（EPDMS2达60.7）；但在真实场景上，缩小动作空间反而损害性能（EPDMS1下降）。这一域差异的根本原因尚待探究，可能源于合成场景的轨迹分布更集中、真实场景需要更丰富的候选集来覆盖多样性。

---

### 定性分析

Figure 3展示了ZTRS在Navtest开环规划中的轨迹可视化（蓝色）与人类轨迹（绿色）的对比。在路径跟随场景中，ZTRS的规划轨迹与人类轨迹高度重合；在交互变道场景中，ZTRS能够生成合理的变道轨迹；在谨慎驾驶场景中，ZTRS表现出适当的减速行为。Figure 4展示了HUGSIM闭环驾驶中的规划轨迹（橙色点），ZTRS在挑战性闭环场景中展现出稳定的驾驶行为。

---

### 失败模式与局限性

尽管ZTRS取得了显著的实验结果，仍存在以下局限：

1. **开环通用场景仍落后于最强IL方法**：在Navtest上落后DriveSuprim 0.9 EPDMS，表明奖励驱动的训练在通用场景下可能尚未完全匹敌精心设计的IL方法。

2. **动作空间覆盖有限**：轨迹候选集受限于K-means聚类得到的16384条固定轨迹，无法覆盖所有驾驶可能性，且轨迹集质量依赖nuPlan数据集的代表性。

3. **训练计算开销高**：EPO需对每个状态计算所有16384个动作的前向传播和EPDMS评分，训练计算开销显著高于传统IL方法。

4. **时序修正超参数手工设定**：$\lambda=0.2$为手工设定，缺乏自适应机制或理论保证。

5. **仅支持离线训练**：无法与环境交互进行在线探索和持续改进，开环EPDMS奖励指标可能无法完全捕捉闭环驾驶中的多智能体交互和长时域规划需求。

6. **仿真-真实域差异**：Table 5揭示的动作空间规模在合成与真实数据上的相反效应，表明仿真与真实域间存在未弥合的差异，可能限制从仿真到真实的迁移能力。

### 补充图表

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2510_24108/figures/007_Table_5.jpg]]
*Table 5: The relationship between the size of the action space and evaluation data. EPDMS1 measures the real-world portion of Navhard, while EPDMS2 measures the simulated portion*

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2510_24108/figures/008_Figure_3.jpg]]
*Figure 3: Visualizations of planned trajectories (blue curves) and the human trajectory (green curves) on the open-loop planning benchmark Navtest*

![[assets/figures/papers/paper_list_l73_https_arxiv_org_abs_2510_24108/figures/009_Figure_4.jpg]]
*Figure 4: Visualizations of planned trajectories (orange dots) on the challenging closed-loop driving benchmark HUGSIM*

## 方法谱系与知识库定位

### 1. 核心范式定位：从模仿学习到零模仿强化学习

端到端自动驾驶的规划模块长期面临一个根本性两难：**模仿学习（IL）** 以人类专家轨迹为监督信号，受限于示范质量与协变量偏移（covariate shift），在分布外场景下泛化能力脆弱；**强化学习（RL）** 虽可通过仿真规模化探索，但现有RL规划方法仅能操作低维符号输入（3D目标检测框、矢量化地图），无法利用高维传感器中的丰富语义信息。ZTRS的核心贡献在于**首次打破这一僵局**——在保留原始视觉传感器输入的条件下，完全通过奖励信号从零训练端到端规划器，彻底消除了对模仿学习的依赖。

这一范式跃迁的技术杠杆是**Exhaustive Policy Optimization（EPO）**：将连续轨迹规划转化为离散动作集上的评分问题，在离线数据上对所有可枚举动作计算优势函数，通过穷举策略梯度提供密集监督。如Figure 1所示，ZTRS区别于模块化方法（依赖感知-预测-规划流水线）和IL方法（依赖人类示范），开创了“零模仿端到端RL”的第三条路径。

### 2. 与基线方法的关系图谱

#### 2.1 轨迹评分器（Trajectory Scorer）谱系

ZTRS在架构上继承轨迹评分器范式——对离散轨迹候选集打分而非直接回归连续轨迹——但彻底改变了其训练机制：

- **GTRS-Dense**（Li et al., arXiv 2025）：IL-based轨迹评分器，以人类轨迹为监督目标。ZTRS在HUGSIM闭环基准上超越GTRS-Dense **4.6个百分点RC**（42.6 vs 38.0），在Navhard开环基准上以EPDMS 45.5%超越其45.3%，证明奖励驱动训练在闭环安全性上具有实质优势。
- **HydraMDP++**（Li et al., arXiv 2025）：IL-based轨迹评分器，Navtest上EPDMS达85.6。ZTRS以86.2超越，但差距较小（+0.6），提示在通用真实场景下奖励信号的优化空间仍存。
- **DriveSuprim**（Yao et al., arXiv 2025）：IL-based轨迹评分器，Navtest上EPDMS达87.1，仍领先ZTRS（86.2）。这表明精心设计的IL方法在开环通用场景下可能仍具有微弱优势，奖励驱动的训练尚未完全匹敌。

**关键区分点**：上述IL方法均依赖人类示范轨迹作为监督信号，ZTRS则以EPDMS规则奖励替代人类示范，训练目标从“模仿人类行为”转变为“最大化安全与舒适性指标”。这一转变在闭环驾驶中尤为关键——人类示范未必是最优策略，而规则奖励直接编码了安全约束。

#### 2.2 端到端规划器谱系

- **UniAD**（Hu et al., CVPR 2023）与**VAD**（Jiang et al., ICCV 2023）：IL-based端到端规划器，在HUGSIM闭环基准上RC分别为26.8和28.8，显著低于ZTRS的42.6。ZTRS的优势源于两方面：（1）EPO的密集监督避免了IL中的协变量偏移；（2）EPDMS奖励直接优化闭环安全性指标，而非模仿可能次优的人类行为。
- **Transfuser** 与**LTF**：IL-based规划器，在Navtest上EPDMS分别为72.5和82.8，远低于ZTRS的86.2。ZTRS的穷举策略优化在开环场景下同样展现出显著的性能优势。

#### 2.3 特权规划器（Privileged Planner）参考

- **PDM-Closed**（Dauner et al., CoRL 2023）：使用真实符号输入（3D目标/地图）的规划器，在Navhard上EPDMS达64.8%，作为传感器方法的性能上限参考。ZTRS（45.5%）与PDM-Closed的差距（19.3个百分点）反映了从高维传感器端到端学习规划的本质难度，也指明了未来改进方向——缩小传感器方法与特权方法之间的感知-规划鸿沟。

### 3. 技术谱系：离线RL与策略梯度

ZTRS的EPO方法根植于策略梯度定理（Policy Gradient Theorem），但做出了关键适配：

- **从期望到穷举求和**：标准策略梯度以动作分布上的期望形式表达（需采样估计），EPO利用离散动作集的可枚举性，将梯度精确表达为所有动作上优势函数与似然梯度之积的和，即 $g = \sum_{a' \in \mathcal{A}} \Psi(s, a') \nabla_{\theta} \pi_{\theta}(a' \mid s)$，消除了采样方差。
- **从在线交互到离线数据**：EPO在离线数据集 $\mathcal{D}$ 上对所有状态-动作对穷举计算梯度，适配自动驾驶中在线交互成本高昂的现实约束。
- **从奖励到规则得分**：优势函数 $\Psi$ 由开环规则指标EPDMS减去时序一致性修正项 $b$ 构成，即 $\Psi(s_t, a_t) = \mathcal{E}(s_t, a_t) - b(s_t, a_t, a_{t-1})$，将领域知识编码为奖励信号。

这一设计与离线RL中的**优势加权回归（AWR）** 和**奖励条件策略优化**有方法论上的亲缘关系，但ZTRS的关键创新在于将动作空间离散化以支持穷举计算，从而在无需重要性采样校正的条件下实现稳定的离线策略优化。

### 4. 适用边界与局限性

#### 4.1 动作空间覆盖的刚性约束

ZTRS的动作空间受限于K-means聚类得到的16384条固定轨迹，其覆盖能力完全依赖nuPlan数据集的代表性。在长尾场景（如紧急避障、非结构化道路）中，候选集可能缺乏合适的轨迹，导致规划失败。Table 5的消融实验揭示了更深层的矛盾：缩小动作空间在合成数据上提升性能（EPDMS2达60.7），但在真实数据上损害性能——这一域差异的根本原因尚不明确，可能与合成场景的多样性不足或真实场景对轨迹精度要求更高有关。

#### 4.2 计算开销与可扩展性

EPO需对每个状态计算所有16384个动作的前向传播和EPDMS评分，训练计算开销显著高于传统IL方法（后者仅需对教师动作或少量采样动作计算损失）。这一开销限制了动作空间规模的进一步扩展，也阻碍了向连续动作空间或更大规模候选集的迁移。

#### 4.3 离线训练的固有局限

ZTRS仅支持离线训练，无法与环境交互进行在线探索。这意味着：（1）策略受限于离线数据的分布，无法主动探索数据覆盖之外的区域；（2）无法利用在线交互进行持续改进或适应新环境。将ZTRS的离线RL框架与安全仿真器中的在线微调结合，是自然的扩展方向。

#### 4.4 奖励信号的对齐问题

开环EPDMS指标（基于规则的安全/舒适性评分）与闭环驾驶安全性之间的对齐程度尚未经过严格验证。虽然HUGSIM闭环结果提供了初步证据（RC提升4.6个百分点），但EPDMS作为训练目标可能无法完全捕捉多智能体交互、长时域规划等闭环特有的挑战。时序一致性修正项 $b$ 中的 $\lambda=0.2$ 为手工设定超参数，缺乏自适应机制或理论保证。

### 5. 开放问题与未来方向

1. **动作空间的可微分学习**：轨迹候选集能否通过可微分方式端到端学习（而非固定的K-means聚类），使动作空间自适应于不同驾驶场景和地理区域？这需要解决离散采样的梯度传播问题。

2. **离线预训练+在线微调**：如何将ZTRS的EPO框架与安全仿真器中的在线RL结合，实现“离线预训练提供先验，在线微调适应新场景”的两阶段范式？关键挑战在于离线到在线的策略迁移稳定性。

3. **多模态传感器融合**：当前ZTRS仅使用前视拼接图像，能否将EPO思想推广到激光雷达+多视角相机的多模态融合框架，进一步提升感知鲁棒性？

4. **域差异的根源与弥合**：Table 5中动作空间缩小在合成/真实数据上的相反效果，提示仿真与真实域之间存在系统性差异。这是源于视觉域偏移、场景分布差异，还是EPDMS指标在两类数据上的统计特性不同？弥合这一差异可能需要域自适应技术或更真实的传感器仿真。

5. **奖励塑形的理论化**：当前时序一致性修正项 $b$ 为手工设计，能否从最优控制或逆强化学习角度导出更具理论保证的奖励塑形机制？例如，将时序平滑性作为KL散度正则项纳入优化目标。

6. **真实道路验证**：ZTRS的零样本闭环能力目前仅在HUGSIM（3DGS渲染场景）上验证，其在真实道路测试中的可迁移性仍是开放问题。开环EPDMS指标与真实驾驶安全性之间的标定关系需要进一步实证研究。

## 原文 PDF

![[paperPDFs/arxiv_2025/ZTRS_Zero_Imitation_End_to_end_Autonomous_Driving_with_Trajectory_Scoring.pdf]]
