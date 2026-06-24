---
title: "BFM-Zero: A Promptable Behavioral Foundation Model for Humanoid Control Using Unsupervised Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/BFM_Zero_A_Promptable_Behavioral_Foundation_Model_for_Humanoid_Control_Using_Unsupervised_Reinforcement_Learning.pdf
openreview_forum_id: jkhl2oI0g5
aliases:
- BZ
- BFM-Zero
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "采用Forward-Backward（FB）表示学习与GAN风格判别器，在无奖励交互与运动捕捉数据上训练统一的潜任务空间Z，策略仅需条件化于潜向量z即可泛化至多种下游任务。"
primary_logic: "BFM-Zero利用离线策略无监督RL预训练形成平滑可解释的潜行为空间，通过FB分解实现零样本的运动跟踪、目标到达和奖励优化，并支持少量样本的潜空间优化以适应新任务。"
claims:
- "BFM-Zero基于FB-CPR框架，结合了Forward-Backward方法用于零样本RL、在线训练和基于运动捕捉数据的策略正则化。"
- "BFM-Zero能够在真实Unitree G1人形机器人上零样本完成多种任务，包括运动跟踪、目标到达和奖励优化。"
- "在运动跟踪测试中，BFM-Zero以仅200M样本显著优于SOTA方法GMT（6800M样本），LAFAN1上E_mpjpe仅为1.0789 vs 2.2425，AMASS上1.0342 vs 1.9064。"
- "领域随机化、非对称历史依赖训练和辅助奖励正则化是实现Sim-to-Real成功迁移的关键设计。"
---

# BFM-Zero: A Promptable Behavioral Foundation Model for Humanoid Control Using Unsupervised Reinforcement Learning

> [!tip] 核心洞察
> BFM-Zero利用离线策略无监督RL预训练形成平滑可解释的潜行为空间，通过FB分解实现零样本的运动跟踪、目标到达和奖励优化，并支持少量样本的潜空间优化以适应新任务。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | BFM-Zero：面向人形机器人控制的提示式行为基础模型，基于无监督强化学习 |
| 英文题名 | BFM-Zero: A Promptable Behavioral Foundation Model for Humanoid Control Using Unsupervised Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=jkhl2oI0g5) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | BFM-Zero |
| Dataset | LAFAN1 (tracking), AMASS (tracking), 真实世界6种运动 (tracking), 零样本通用性（跨任务） |

> [!tip] 效果简介
> - LAFAN1 (tracking) 上，E_mpjpe (↓) 为 1.0789，对比 GMT: 2.2425，变化 -51.9%。
> - AMASS (tracking) 上，E_mpjpe (↓) 为 1.0342，对比 GMT: 1.9064，变化 -45.8%。
> - 真实世界6种运动 (tracking) 上，E_mpjpe (↓) 为 1.1408 (real)，对比 0.8041 (sim-dr)，变化 +41.8%。

## 概述

人形机器人的全身控制长期依赖**在线策略PPO**与**明确的任务跟踪奖励**，导致策略高度专用、难以跨任务泛化，且缺乏统一的提示接口。无监督离线策略强化学习在真实机器人上的Sim-to-Real迁移与鲁棒性亦未得到系统验证。

BFM-Zero提出了一种**提示式行为基础模型**，核心思路是：利用**Forward-Backward（FB）表示学习**与**GAN风格判别器**，在无奖励交互与运动捕捉数据上训练统一的潜任务空间$\mathcal{Z}$，策略仅需条件化于潜向量$z$即可泛化至多种下游任务。该方法基于**FB-CPR**（Tirinzoni et al., 2025）构建，将零样本RL的FB分解与在线训练、运动捕捉策略正则化相结合，形成平滑可解释的潜行为空间。

**关键结论**：
- **零样本多任务能力**：BFM-Zero在真实Unitree G1人形机器人上零样本完成运动跟踪、目标到达和奖励优化三类任务，无需任何再训练。
- **显著样本效率优势**：在运动跟踪基准上，BFM-Zero仅用**200M样本**即超越SOTA方法**GMT**（Chen et al., 2025，需6800M样本），LAFAN1上E_mpjpe为**1.0789**（GMT: 2.2425），AMASS上**1.0342**（GMT: 1.9064），误差分别降低51.9%和45.8%。
- **Sim-to-Real成功迁移**：非对称历史依赖训练、领域随机化与辅助奖励正则化三者协同，将真实世界跟踪性能损失控制在可接受范围（约2.47%），并展现出对踢打、推搡等外部扰动的自然恢复能力。
- **可操作的潜空间**：学习到的$\mathcal{Z}$具备平滑语义结构，支持球形线性插值实现自然行为过渡，并通过CEM实现少量样本的潜空间优化以适应新任务。

**方法定位**：BFM-Zero属于**无监督离线策略RL + 潜空间条件化**范式，区别于传统基于PPO的任务专用跟踪器（如GMT），其训练无需任务特定奖励，推理阶段通过将奖励函数、目标姿态或运动序列嵌入潜空间直接执行，实现了从“单任务专用”到“通用提示式”的范式转变。

## 背景与动机

人形机器人的全身控制是实现通用物理智能的关键瓶颈。当前主流方法几乎全部采用在线策略的PPO（Proximal Policy Optimization）范式，配合明确的任务特定跟踪奖励函数进行训练。这种范式存在三个根本性局限：

**任务专用性**：每个新任务（如特定步态行走、特定姿态到达、特定奖励优化）都需要从头训练一个独立的控制器，策略无法跨任务泛化。现有方法缺乏统一的提示接口，无法像语言模型那样通过简单的输入变换来切换行为模式。

**数据与样本效率低下**：以当前SOTA通用运动跟踪方法 **GMT**（Chen et al., 2025）为例，其训练需要高达6800M环境交互样本，且仅能执行运动跟踪单一任务。这种样本效率在真实机器人上几乎不可行，严重制约了方法的可扩展性。

**Sim-to-Real迁移缺乏系统验证**：虽然部分工作在仿真中展示了全身控制能力，但无监督离线策略RL在真实人形机器人上的Sim-to-Real迁移和鲁棒性始终未经验证。领域随机化、观测噪声、执行器非线性等因素在真实部署中会造成显著的性能退化，现有方法对此缺乏有效的系统性解决方案。

**核心动机**：BFM-Zero旨在突破上述局限，构建一个统一的**提示式行为基础模型**（promptable behavioral foundation model）。其核心思路是：通过无监督强化学习预训练，学习一个平滑、可解释的潜行为空间$Z$，使得策略仅需条件化于潜向量$z$即可泛化至多种下游任务——包括运动跟踪、目标姿态到达和奖励函数优化——无需任何再训练。同时，通过非对称历史依赖训练、领域随机化和辅助奖励正则化等设计，确保模型能够从仿真稳健迁移至真实Unitree G1人形机器人。

## 核心创新

BFM-Zero的核心创新在于将**无监督强化学习**范式引入人形机器人全身控制，构建了一个**统一的、可提示的行为基础模型**。相对于现有方法，其关键突破体现在以下四个维度：

### 1. 训练范式：从任务专用在线策略到通用离线策略无监督学习

现有SOTA人形控制方法（如**GMT**，Chen et al., 2025）普遍采用基于PPO的在线策略训练，依赖针对特定任务手工设计的模仿奖励函数——每新增一个任务就需要重新训练。BFM-Zero转而采用基于**FB-CPR**（Tirinzoni et al., 2025）的离线策略无监督RL框架，在训练阶段**完全不需要任务特定奖励**：策略仅通过条件化于一个潜向量 $z$ 即可被“提示”执行不同行为。这一范式转换使单一模型能够覆盖多种下游任务，无需重新训练。

### 2. 任务定义：从固定奖励到零样本潜空间提示

传统方法将任务定义为固定的奖励函数或动作序列跟踪目标，缺乏灵活性。BFM-Zero通过Forward-Backward（FB）表示学习构建了一个**平滑、可解释的潜任务空间** $Z$，将任意下游任务（奖励函数、目标姿态、运动序列）统一嵌入为潜向量 $z$：

- **奖励推理**：通过样本估计 $z_r = \frac{1}{N} \sum_i r(s_i) B(s_i)$，将任意奖励函数映射为潜提示；
- **目标到达**：直接使用后继特征 $z_g = B(s_g)$ 作为目标姿态的潜表示；
- **运动跟踪**：通过向前看 $H$ 帧的后继特征之和 $z_t = \sum_{t'=t}^{t+H} B(s_{t'})$ 定义跟踪序列的潜提示。

这种统一接口使BFM-Zero成为首个支持**零样本跨任务泛化**的人形控制模型——从运动跟踪到目标到达再到奖励优化，均通过同一策略执行。

### 3. Sim-to-Real迁移：超越单纯领域随机化的三层鲁棒性设计

现有Sim-to-Real方案多仅依赖领域随机化。BFM-Zero引入了一个**三层鲁棒性训练体系**：

| 组件 | 作用 |
|------|------|
| **非对称历史依赖训练** | Actor仅使用观测历史 $o_{t,H}$，Critic访问特权状态 $s_t$，桥接部分可观测性与真实环境的不确定性 |
| **领域随机化** | 随机化质量、摩擦、关节偏移、躯干质心等物理参数，并施加扰动与传感器噪声 |
| **辅助奖励正则化** | 通过辅助评论家 $Q_R$ 惩罚大动作、不精确脚步等不安全行为，确保策略在真实硬件上的安全运行 |

消融实验表明，去除辅助奖励会导致真实机器人**严重不稳定**，而仿真指标几乎不变——这揭示了辅助奖励对Sim-to-Real迁移的关键作用。在Unitree G1真实机器人上，BFM-Zero的跟踪性能仅比无领域随机化的特权变体下降2.47%，验证了该设计的有效性。

### 4. 策略架构：从前馈MLP到带观测历史的残差网络

BFM-Zero的策略网络采用了**带观测历史的残差架构**（类Transformer块），而非传统的前馈MLP。这一设计使策略能够利用历史观测序列中的时序信息，更好地应对部分可观测性和环境动态变化。消融研究表明，增加模型容量和采用残差架构普遍提升运动跟踪性能。

### 5. GAN风格行为正则化：将策略锚定于人类运动先验

BFM-Zero通过一个**潜条件判别器** $D$ 引入GAN目标，使策略生成的行为分布与运动捕捉数据难以区分：

$$\mathcal{L}(D) = - \mathbb{E}_{\tau \sim \mathcal{M}, (o, s) \sim \tau} [\log(D(o, s, z_\tau))] - \mathbb{E}_{(o, s, z) \sim \mathcal{D}} [\log(1 - D(o, s, z))]$$

这一机制将无监督探索自然地约束在类人行为流形上，是BFM-Zero能够生成自然、鲁棒运动的关键设计。

### 创新总结

BFM-Zero的核心贡献在于**将零样本RL的FB框架首次成功应用于人形机器人全身控制的Sim-to-Real场景**，通过潜空间统一提示、三层鲁棒性训练和GAN行为正则化，实现了从“每任务一模型”到“单一通用模型”的范式跃迁。

## 整体框架

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_jkhl2oI0g5/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the BFM-Zero framework. After the pre-training stage, BFM-Zero forms a latent space that can be used for zero-shot reward optimization, single-frame goal reaching, and tracking. It can also be adapted in a few-shot fashion to reach more challenging poses*

BFM-Zero 的整体流程分为三个阶段：**无监督预训练**、**零样本推理**与**少量样本适应**（图2）。其核心目标是在无奖励交互中学习一个统一的潜行为空间 $Z \subseteq \mathbb{R}^d$，使策略仅需条件化于潜向量 $z$ 即可泛化至多种下游任务。

### 预训练阶段

预训练阶段同时使用两类数据源：仿真器中的在线无奖励交互，以及离线无标签行为数据集（运动捕捉数据）。训练目标是在统一的潜空间 $Z$ 中嵌入任务表征，并学习一个以 $z$ 为条件的可提示策略。该阶段由以下模块协同完成：

- **Forward-Backward 表示学习**：基于 FB-CPR 算法（Tirinzoni et al., 2025），通过前向映射 $F$ 和后向映射 $B$ 对长期状态转移动态进行有限秩分解，$B$ 捕捉状态间的低频长程时序依赖，形成平滑可解释的潜空间。
- **潜条件判别器**：采用 GAN 风格目标，迫使策略的观测-状态分布与运动捕捉数据难以区分，从而将行为正则化至人类运动流形。
- **辅助奖励评论家**：学习一组惩罚不安全或非期望行为（如过大幅度动作、不精确脚步）的评论家 $Q_R$，为 Sim-to-Real 安全迁移提供约束。
- **非对称 Actor-Critic 与观测历史**：策略仅以观测历史 $o_{t,H}$ 为输入，而评论家（$F, Q_D, Q_R$）可访问特权状态 $s_t$。这种非对称设计使策略能在部分可观测的真实世界中运行，同时利用仿真中的完整状态信息进行高效训练。
- **领域随机化**：对物理参数（连杆质量、摩擦系数、关节偏移、躯干质心等）、外部扰动和传感器噪声进行大范围随机化，桥接 Sim-to-Real 差距。

Actor 的最终损失整合了三项信号：FB 项驱动任务相关行为，风格评论家 $Q_D$ 保证人形自然度，辅助评论家 $Q_R$ 施加安全约束：

$$\mathcal{L}(\pi) = - \mathbb{E} \Big[ F(o_{t,H}, s_t, a_t, z)^\top z + \lambda_D Q_D(o_{t,H}, s_t, a_t, z) + \lambda_R Q_R(o_{t,H}, s_t, a_t, z) \Big]$$

### 推理与适应阶段

预训练完成后，下游任务通过以下方式嵌入潜空间 $Z$ 并直接执行，无需再训练：

- **奖励优化**：对任意奖励函数 $r$，通过样本估计潜向量 $z_r = \frac{1}{N} \sum_i r(s_i) B(s_i)$，零样本 Q 函数可直接由后继特征计算：$Q_r^{\pi_z}(s, a) = F(s, a, z)^\top \mathbb{E}_{s' \sim \rho}[B(s') r(s')]$。
- **目标到达**：单帧目标姿态的潜向量即其后向特征 $z_g = B(s_g)$。
- **运动跟踪**：通过向前看 $H$ 帧的后向特征之和定义跟踪序列的潜提示 $z_t = \sum_{t'=t}^{t+H} B(s_{t'})$。

对于零样本难以完成的挑战性任务，框架支持两种少量样本适应方式：

- **单姿态适应**：以零样本潜向量 $z_0$ 为初始点，使用 CEM 在潜空间内优化目标 $J(z) = \sum_{t=0}^{T-1} (r_{\mathrm{task}}(s_t) - \alpha_R \sum_{k=1}^{N_{\mathrm{aux}}} r_k(o_t, s_t, a_t))$，平衡任务奖励与辅助惩罚。
- **轨迹适应**：采用双退火轨迹优化，基于显式跟踪奖励在潜空间内优化整条轨迹的潜序列。

### 输入输出流

整个系统的输入为机器人本体感知观测历史 $o_{t,H}$（包含 $H$ 步的观测与动作序列），输出为 29 自由度 PD 控制器目标 $a \in \mathbb{R}^{29}$。任务通过潜向量 $z$ 提示，策略网络采用带残差连接的类 Transformer 架构（表3），评论家与判别器则使用更大容量的嵌入残差块以充分捕获特权状态信息。

## 核心模块与公式推导

BFM-Zero的核心架构围绕**Forward-Backward（FB）表示学习**构建统一的潜任务空间，并通过离线策略无监督RL预训练形成可提示的行为基础模型。其关键模块如下：

### Forward-Backward表示学习（F, B）

BFM-Zero建立在**FB-CPR**算法（Tirinzoni et al., 2025）之上，该算法结合了Forward-Backward方法用于零样本RL。FB的核心思想是对策略$\pi_z$诱导的长期状态转移动态进行有限秩近似：

$$M^{\pi_z}(\mathrm{d}s' | s, a) \simeq F(s, a, z)^\top B(s') \rho(\mathrm{d}s')$$

其中，$F(s, a, z)$为前向映射，将状态-动作对与潜任务向量$z$映射到低维空间；$B(s')$为后向映射，捕捉状态间长程时间依赖的低频特征；$\rho(\mathrm{d}s')$为状态分布权重。这一分解使得后继特征的线性运算即可近似任意奖励函数下的Q值。

FB的训练通过时序差分损失实现，近似后继度量的Bellman方程：

$$\mathcal{L}(F, B) = \mathbb{E} \Big[ \big( F(o_{t,H}, s_t, a_t, z)^\top B(o^+, s^+) - \gamma \overline{F}(o_{t+1,H}, s_{t+1}, a_{t+1}, z)^\top \overline{B}(o^+, s^+) \big)^2 \Big] - 2 \mathbb{E} \big[ F(o_{t,H}, s_t, a_t, z)^\top B(o_{t+1}, s_{t+1}) \big]$$

其中$o_{t,H}$为观测历史，$o^+$和$s^+$为从回放缓存中采样的独立观测与状态，$\overline{F}$和$\overline{B}$为目标网络（target networks）。

### 潜在条件判别器（D）

为将策略行为约束在人类运动捕捉数据的分布内，BFM-Zero引入GAN风格的判别器，其损失为：

$$\mathcal{L}(D) = - \mathbb{E}_{\tau \sim \mathcal{M}, (o, s) \sim \tau} \left[ \log(D(o, s, z_\tau)) \right] - \mathbb{E}_{(o, s, z) \sim \mathcal{D}} \left[ \log(1 - D(o, s, z)) \right]$$

其中$\mathcal{M}$为运动捕捉数据集（如LAFAN1），$z_\tau$为运动片段$\tau$对应的潜向量，$\mathcal{D}$为策略在线交互数据。判别器以观测、特权状态和潜向量为条件，迫使策略生成与人类行为难以区分的动作。

### 辅助奖励评论家（Q_R）

为保证Sim-to-Real迁移的安全性，BFM-Zero引入辅助奖励评论家，通过标准Bellman残差损失学习惩罚不安全行为的价值函数：

$$\mathcal{L}(Q_R) = \mathbb{E} \left[ \Big( Q_R(o_{t,H}, s_t, a_t, z) - \sum_{k=1}^{N_{\max}} r_k(s_t) - \gamma \overline{Q_R}(o_{t+1,H}, s_{t+1}, a_{t+1}, z) \Big)^2 \right]$$

辅助奖励$r_k$涵盖大动作幅度、不精确脚步等惩罚项，在仿真中指标几乎不变但对真实机器人稳定性至关重要。

### Actor损失函数

最终策略（Actor）的损失函数整合FB项、风格判别器信号和辅助评论家：

$$\mathcal{L}(\pi) = - \mathbb{E} \Big[ F(o_{t,H}, s_t, a_t, z)^\top z + \lambda_D Q_D(o_{t,H}, s_t, a_t, z) + \lambda_R Q_R(o_{t,H}, s_t, a_t, z) \Big]$$

其中$Q_D$为判别器提供的风格奖励，$Q_R$为辅助评论家，$\lambda_D$和$\lambda_R$为权重系数。Actor仅以观测历史$o_{t,H}$为输入，而Critic（F、B、D、Q_R）可访问特权状态$s_t$，形成非对称训练架构。

### 零样本推理的核心公式

预训练完成后，下游任务通过将任务嵌入潜空间$Z$实现零样本执行：

- **奖励推理**：给定任意奖励函数$r$，其潜向量通过采样估计：
  $$z_r = \frac{1}{N} \sum_i r(s_i) B(s_i)$$
  对应策略的Q值可直接由后继特征计算：
  $$Q_r^{\pi_z}(s, a) = F(s, a, z)^\top \mathbb{E}_{s' \sim \rho} [B(s') r(s')]$$

- **目标到达**：单帧目标姿态的潜向量即其后向特征：
  $$z_g = B(s_g)$$

- **运动跟踪**：通过向前看$H$帧的后向特征之和定义跟踪序列的潜提示：
  $$z_t = \sum_{t'=t}^{t+H} B(s_{t'})$$

### 少量样本适应目标

对于需要在线微调的场景，BFM-Zero在潜空间内优化潜向量$z$，目标函数平衡任务奖励与辅助惩罚：

$$J(z) = \sum_{t=0}^{T-1} \Big( r_{\mathrm{task}}(s_t) - \alpha_R \sum_{k=1}^{N_{\mathrm{aux}}} r_k(o_t, s_t, a_t) \Big)$$

优化可采用CEM（Cross-Entropy Method）或双退火轨迹优化等方法，无需修改网络参数即可适应新任务。

## 实验与分析

### 核心性能：零样本运动跟踪的样本效率与精度优势

BFM‑Zero 在零样本运动跟踪任务上展现出显著的样本效率优势。在 LAFAN1 基准上，BFM‑Zero 仅使用 **200M** 环境交互样本，即达到 $E_{\text{mpjpe}} = 1.0789$，相比 SOTA 通用跟踪方法 **GMT**（Chen et al., 2025）的 $2.2425$（使用 6800M 样本），误差降低 **51.9%**。在 AMASS 数据集上，BFM‑Zero 同样以 $1.0342$ 的误差大幅优于 GMT 的 $1.9064$（降低 45.8%）（Table 9）。这一结果的核心驱动力在于：Forward‑Backward 表示学习将长期转移动态压缩为低秩分解 $M^{\pi_z}(\mathrm{d}s' | s, a) \simeq F(s, a, z)^\top B(s') \rho(\mathrm{d}s')$，使得策略无需为每个跟踪目标重新训练，仅需通过潜向量 $z_t = \sum_{t'=t}^{t+H} B(s_{t'})$ 提示即可泛化。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_jkhl2oI0g5/figures/045_Table_9.jpg]]
*Table 9: Comparison of general tracking methods and BFM-Zero*

需注意，该对比仅针对通用跟踪方法；BFM‑Zero 作为行为基础模型的零样本能力，与任务专用跟踪器的直接对比存在任务设定差异。

### 仿真性能分层：领域随机化与非对称训练的影响

Table 1（Section 3）揭示了 BFM‑Zero 在不同仿真配置下的性能分层：

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_jkhl2oI0g5/figures/003_Table_1.jpg]]

| 模型变体 | 仿真环境 | 跟踪误差 ($E_{\text{mpjpe}}$ ↓) | 奖励推理得分 ↑ | 姿态到达误差 ↓ |
|----------|----------|-------------------------------|----------------|----------------|
| BFM‑Zero‑priv | Isaac (无 DR) | 1.0749 | 299.3 | 1.0291 |
| BFM‑Zero | Isaac (DR) | 1.1015 | 221.9 | 1.1387 |
| BFM‑Zero | MuJoCo (DR) | 1.0789 | 207.3 | 1.1041 |

从特权变体 BFM‑Zero‑priv 到领域随机化版本，跟踪性能下降仅 **2.47%**，姿态到达下降 **10.65%**，但奖励推理性能下降 **25.86%**。这一不对称退化说明：领域随机化对需要精确奖励推理的任务影响最大——随机化引入的动力学扰动使得基于后继特征 $Q_r^{\pi_z}(s, a) = F(s, a, z)^\top \mathbb{E}_{s' \sim \rho}[B(s') r(s')]$ 的零样本 Q 值估计产生偏差。相比之下，Sim‑to‑Sim 迁移（Isaac → MuJoCo）的性能变异小于 7%，表明框架本身对仿真器差异具有鲁棒性。

### 真实世界验证：Sim‑to‑Real 迁移的关键设计

在 Unitree G1 人形机器人上，BFM‑Zero 零样本完成了六种运动跟踪任务，真实世界 $E_{\text{mpjpe}} = 1.1408$，相比仿真（DR）的 $0.8041$ 上升 41.8%（Table 8）。这一性能损失在可接受范围内，归功于三项关键设计：

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_jkhl2oI0g5/figures/044_Table_8.jpg]]
*Table 8: Comparison of real-world and simulation performance*

1. **非对称历史依赖训练**：策略仅使用观测历史 $o_{t,H}$，而评论家（Critic）访问特权状态 $(o_{t,H}, s_t)$，使策略学会从部分可观测信息中推断动力学状态，桥接仿真与现实的感知差距。
2. **领域随机化**：对质量、摩擦系数、关节偏移、躯干质心等物理参数进行均匀分布随机化（Table 4），迫使策略学习对参数变化鲁棒的控制策略。
3. **辅助奖励正则化**：通过辅助评论家 $Q_R$ 惩罚大动作、不精确脚步等不安全行为，其损失函数为 $\mathcal{L}(Q_R) = \mathbb{E} [ ( Q_R(o_{t,H}, s_t, a_t, z) - \sum_k r_k(s_t) - \gamma \overline{Q_R}(\dots) )^2 ]$。

真实世界实验中，BFM‑Zero 展示了多样化的运动跟踪能力（Figure 4：动态舞蹈、行走中频繁转向、从跌倒中自然恢复），连续目标到达（Figure 5：在多个目标姿态间平滑过渡，无需显式插值），以及奖励优化行为（Figure 6：坐姿、蹲伏、低速移动、举臂等命令的忠实执行）。

### 扰动鲁棒性：离线策略训练与 GAN 正则化的协同效应

BFM‑Zero 展现出超越显式扰动训练的鲁棒性（Figure 7）：被踢腿部时保持稳定、受到强力推搡时后退一步吸收冲击、被拉倒后自然站起并返回 T 姿态。该鲁棒性并非主要源于扰动训练，而是源于 **TD 式离线策略训练**与 **GAN 风格判别器**的协同作用。判别器损失 $\mathcal{L}(D) = -\mathbb{E}_{\tau \sim \mathcal{M}} [\log D(o, s, z_\tau)] - \mathbb{E}_{(o, s, z) \sim \mathcal{D}} [\log(1 - D(o, s, z))]$ 使策略行为与人类运动捕捉数据难以区分，从而隐式地将策略吸引到稳定、自然的运动模式流形上，当遭遇外界扰动时，策略自然回归到该流形。

### 少量样本适应：潜空间优化的有效性

在少量样本适应场景中，BFM‑Zero 展示了两种模式：

- **单姿态适应**：以零样本潜向量 $z_0 = B(s_g, o_g)$ 为初始点，使用 CEM 优化目标 $J(z) = \sum_t (r_{\text{task}}(s_t) - \alpha_R \sum_k r_k(o_t, s_t, a_t))$，其中 $r_{\text{task}} = \mathbf{1}_{\{h_{\text{rightfoot}} > 0.15 \text{m} \land \text{no‑contact}\}}$。在 4 kg 额外负载下，单腿站立时间超过 15 秒（Figure 8a）。
- **轨迹适应**：采用双退火轨迹优化，以显式跟踪奖励为目标，使跟踪误差降低约 **29.1%**（Figure 8b）。

这些结果表明，BFM‑Zero 的潜空间 $Z$ 具有良好的优化景观，少量在线交互即可显著提升特定任务性能。

### 消融实验：辅助奖励对 Sim‑to‑Real 的决定性作用

去除辅助奖励的消融实验揭示了一个关键不对称性：**仿真指标几乎不变，但真实机器人出现严重不稳定**（Figure 15）。这说明辅助奖励 $Q_R$ 的作用并非提升仿真性能上限，而是约束策略远离仿真中不存在、现实中却会导致失败的“捷径行为”（如过大的关节力矩、不精确的足部着地）。这一发现对 Sim‑to‑Real 迁移具有普遍指导意义：仅依赖领域随机化不足以消除仿真与现实的分布偏移，显式的安全约束正则化是必要的补充。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_jkhl2oI0g5/figures/032_Figure_15.jpg]]
*Figure 15: Examples of training losses as a function of the number of environment steps when training with and without auxiliary rewards (top). Bottom table shows the evaluation score of the models on tracking, goal reaching and reward inference. The model is the ResNet model with 6 blocks and 2048 hidden dimension*

### 数据源与模型规模消融

- **数据源选择**：使用运动数据集（尤其是 LAFAN1）进行奖励推理，性能显著优于使用在线回放缓存（Figure 13, 14）。原因在于运动数据集覆盖的状态分布更接近人类行为流形，使得后继特征 $B(s)$ 的估计在该流形上更精确。
- **模型架构**：增加模型容量并采用残差架构（ResNet 风格）普遍提升运动跟踪性能，但对奖励推理的收益温和（Figure 12）。这表明跟踪任务对表示容量更敏感，而奖励推理更依赖于数据质量。
- **潜空间维度**：$d_z \geq 256$ 时零样本性能相似，但 $d_z = 1024$ 时奖励推理下降；经 CEM 适应后，高维模型可达到相近性能（Figure 17, Table 7）。这暗示过大的潜空间可能引入虚假自由度，需少量在线样本“校准”。

![[assets/figures/papers/paper_list_l6_https_openreview_net_forum_id_jkhl2oI0g5/figures/027_Figure_13.jpg]]
*Figure 13: Reward inference performance when using the experience generated by the agent (i.e., online replay buffer) or the motion dataset used for training. We get better reward performance when using the motion dataset, in particular when using LAFAN1 (see Fig. 12)*

### 失败模式与局限性

1. **稀疏奖励任务**：零样本奖励推理在稀疏奖励场景下易出现失败案例，因 $z_r = \frac{1}{N} \sum_i r(s_i) B(s_i)$ 的样本估计方差随奖励稀疏度增加而增大。
2. **模型规模与实时性**：BFM‑Zero 参数量达 440.5M，虽训练样本效率优于 GMT，但实时推理的计算负担可能限制部署频率。
3. **适应能力边界**：对于更复杂的非典型运动表达，当前 CEM/轨迹优化在潜空间内的在线自适应能力仍有不足，未探索梯度微调机制。
4. **硬件泛化**：仅在 Unitree G1 单一平台上验证，泛化至其他人形机器人构型需要进一步实验。
5. **规模律未明**：运动数据集大小、模拟数据采样策略与模型架构之间的缩放规律尚未系统研究。

## 方法谱系与知识库定位

### 1. 方法谱系：从任务专用RL到统一行为基础模型

BFM-Zero的方法论根基深植于两条技术路线的交汇：**无监督强化学习（Unsupervised RL）** 与**Forward-Backward（FB）表示学习**。其直接算法基础是**FB-CPR**（Tirinzoni et al., 2025），该方法将FB框架（Touati & Ollivier, 2021）的零样本RL能力与在线训练、基于运动捕捉数据的策略正则化相结合。BFM-Zero在此基础上的核心扩展在于：将FB-CPR从通用RL设定迁移至人形机器人全身控制的POMDP场景，并引入面向Sim-to-Real迁移的系统性工程化设计。

在人形机器人运动控制领域，现有SOTA方法（如**GMT**，Chen et al., 2025）普遍采用在线策略PPO配合显式跟踪奖励的范式。这类方法的根本局限在于**任务专用性**：每个新任务（如不同风格的运动跟踪、目标到达、奖励优化）都需要独立的奖励工程和重新训练，缺乏统一的控制接口。BFM-Zero通过单一预训练模型实现了范式转换——策略仅需条件化于潜向量 $z$ 即可泛化至多种下游任务，将“训练一个策略解决一个任务”转变为“训练一个策略，通过提示解决多个任务”。

从表示学习的角度看，BFM-Zero的潜空间 $Z$ 继承了FB框架的理论优势：后向映射 $B(s)$ 捕捉状态间的长程时序依赖，前向映射 $F(s,a,z)$ 编码任务条件化的动作选择，两者内积近似策略诱导的长期状态转移动态 $M^{\pi_z}(\mathrm{d}s' | s, a) \simeq F(s, a, z)^\top B(s') \rho(\mathrm{d}s')$。这种分解使得潜空间具备了**可解释的语义结构**（Figure 9）：运动跟踪轨迹在潜空间中形成连续路径，不同行为类型自然聚类，球形线性插值（Slerp）可生成平滑的行为过渡。

### 2. 与基线方法的关键差异

| 设计维度 | 基线方法（PPO + 跟踪奖励） | BFM-Zero |
|---------|--------------------------|----------|
| 训练范式 | 在线策略PPO，任务特定模仿奖励 | 离线策略无监督RL（FB-CPR），策略通过潜向量 $z$ 提示 |
| 任务定义 | 固定奖励函数或动作序列跟踪 | 通过 $z_r$（奖励）、$z_g$（目标）、$\{z_t\}$（运动序列）零样本定义 |
| Sim-to-Real迁移 | 仅领域随机化 | 非对称历史依赖训练 + 领域随机化 + 辅助奖励正则化 |
| 策略网络 | 前馈MLP | 带观测历史的残差网络（类Transformer块） |
| 数据效率 | GMT需6800M样本 | BFM-Zero仅需200M样本 |

**数据效率优势**尤为显著：在LAFAN1运动跟踪基准上，BFM-Zero以仅200M样本达到 $E_{\text{mpjpe}}=1.0789$，显著优于GMT（6800M样本，$E_{\text{mpjpe}}=2.2425$），误差降低51.9%（Table 9）。在AMASS数据集上同样保持45.8%的误差降低（$1.0342$ vs $1.9064$）。这一效率提升源于FB框架的离线策略特性——可充分利用大规模回放缓存进行高UTD（update-to-data）训练，而非在线策略方法受限于采样效率。

### 3. 适用边界与局限

**适用边界**：
- **硬件平台**：当前仅在Unitree G1（29自由度）人形机器人上验证，泛化至其他构型（如不同自由度配置、尺寸差异显著的平台）需要重新训练或迁移学习。
- **任务类型**：覆盖运动跟踪、单帧目标到达、奖励优化三类任务，但对需要精细接触推理的操作任务（如抓取、工具使用）尚未验证。
- **运动复杂度**：零样本条件下可处理LAFAN1和AMASS中的行走、舞蹈、格斗等运动，但对极端非典型姿态（如高难度体操动作）需要少量样本适应。

**已识别的关键局限**：

1. **奖励推理的鲁棒性瓶颈**：在零样本条件下，奖励推理性能受领域随机化数据分布影响较大。Figure 3右侧直方图显示，某些奖励函数（如`move-ego-0-0`）的评估分数呈双峰分布，存在明显的失败模式（分数接近0的峰值）。稀疏奖励任务尤其容易出现推理失败。

2. **模型规模与推理成本**：BFM-Zero参数量达440.5M（Table 3），虽训练样本效率优于GMT，但实时推理的计算负担可能限制其在资源受限平台上的部署。

3. **在线自适应能力有限**：尽管CEM（Cross-Entropy Method）和轨迹优化提供了少量样本适应通道，但对于更复杂的运动表达，当前方法未探索梯度微调（fine-tuning）机制。Figure 8显示轨迹适应可将跟踪误差降低约29.1%，但仍有较大优化空间。

4. **Sim-to-Real迁移的残余差距**：真实世界运动跟踪的 $E_{\text{mpjpe}}=1.1408$，相较仿真（DR）的 $0.8041$ 仍有41.8%的性能下降（Table 8），表明领域随机化未能完全弥合Sim-to-Real鸿沟。

5. **缺乏语言接口**：当前潜空间 $Z$ 的提示方式为数值向量，未与大规模语言模型或VLA（Vision-Language-Action）模型结合，无法实现自然语言任务描述。

### 4. 关键消融发现与设计原则

消融实验揭示了若干对实际部署至关重要的设计原则：

- **辅助奖励对Sim-to-Real安全至关重要**：去除辅助奖励（auxiliary rewards）后，仿真指标几乎不变，但真实机器人出现严重不稳定（Figure 15）。这表明辅助评论家 $Q_R$ 学习的惩罚信号（大动作、不精确脚步）在仿真中看似冗余，实则是物理世界安全运行的“护栏”。

- **非对称历史训练与领域随机化的协同效应**：两者共同将Sim-to-Real性能损失控制在可接受范围（跟踪2.47%，奖励25.86%），且Sim-to-Sim变异<7%。单独使用任一技术均无法达到此效果。

- **运动数据集选择影响奖励推理质量**：使用LAFAN1数据集进行奖励推理优于在线回放缓存（Figure 13, 14），说明离线人类运动数据包含了更丰富的状态-行为关联信息，有利于后继特征 $B(s)$ 的学习。

- **潜空间维度存在最优区间**：$d_z \geq 256$ 时零样本性能相似，但维度增至1024时奖励推理下降（Table 7, Figure 17）。经CEM适应后高维模型可恢复性能（Figure 18），暗示高维潜空间保留了更多信息但需要额外优化才能有效利用。

### 5. 开放问题

1. **规模律（Scaling Laws）**：运动数据集大小、模拟数据采样策略及模型架构如何影响行为基础模型的性能增长规律？当前200M样本的训练设定是否接近性能饱和点？

2. **自适应机制深化**：如何设计更有效的在线或离线自适应算法，使模型能可靠执行更复杂的非典型运动？梯度微调与潜空间优化的结合方式值得探索。

3. **数据源最优选择**：对于奖励推理任务，离线运动数据集与在线回放缓存的混合比例如何影响鲁棒性和泛化性？是否存在任务依赖的最优数据配方？

4. **语言接口集成**：能否将BFM-Zero的潜空间与大规模语言模型结合，实现基于自然语言的任务提示？这需要建立从语言描述到潜向量 $z$ 的映射机制。

5. **跨平台泛化**：当前仅在Unitree G1上验证，方法是否可泛化至其他构型的人形机器人（如不同腿臂比例、关节限位）？是否需要构型条件化的表示学习？

6. **安全保证的形式化**：辅助奖励虽在实践中有效，但其安全保障缺乏形式化分析。如何在理论上刻画辅助评论家提供的安全边界？

## 原文 PDF

![[paperPDFs/ICLR_2026/BFM_Zero_A_Promptable_Behavioral_Foundation_Model_for_Humanoid_Control_Using_Unsupervised_Reinforcement_Learning.pdf]]
