---
title: "Plan-R1: Safe and Feasible Trajectory Planning as Language Modeling"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Plan_R1_Safe_and_Feasible_Trajectory_Planning_as_Language_Modeling.pdf
openreview_forum_id: uusTA1rBhR
aliases:
- PR
- Plan-R1
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "解耦行为学习与规划原则对齐：先通过预训练捕捉类人驾驶行为，再使用基于规则的强化学习进行微调以显式对齐安全与合规等原则。同时，采用 VD‑GRPO 替代 GRPO 的分组归一化，通过中心化和固定缩放保留绝对奖励幅度，确保安全关键目标在训练全过程中保持主导梯度。"
primary_logic: "将轨迹规划重新定义为原则对齐的自回归预测任务：预训练阶段学习通用的多智能体运动模式，微调阶段利用无需人类偏好数据的规则化奖励和双模型 rollout 实现原则对齐，并通过移除 GRPO 中方差归一化的 VD‑GRPO 解决多目标优化中安全优先级被稀释的问题。"
claims:
- "Plan‑R1 是一个两阶段框架，将行为学习与原则对齐解耦，从而克服纯专家数据的局限性。"
- "VD‑GRPO 通过替换分组归一化为中心化与固定缩放，保留绝对奖励幅度，确保安全关键目标持续主导优化。"
- "VD‑GRPO 将碰撞避免指标从 93.87 提升至 97.32，显著优于标准 GRPO，同时反应式 CLS 达到 90.04。"
- "在最具挑战性的反应式基准上，Plan‑R1 取得了最新的 R‑CLS 成绩（Test14‑random: 90.04，比 Diffusion Planner 高 +7.11），验证了双模型设计与原则对齐的有效性。"
---

# Plan-R1: Safe and Feasible Trajectory Planning as Language Modeling

> [!tip] 核心洞察
> 将轨迹规划重新定义为原则对齐的自回归预测任务：预训练阶段学习通用的多智能体运动模式，微调阶段利用无需人类偏好数据的规则化奖励和双模型 rollout 实现原则对齐，并通过移除 GRPO 中方差归一化的 VD‑GRPO 解决多目标优化中安全优先级被稀释的问题。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Plan-R1：基于语言建模的安全可行轨迹规划 |
| 英文题名 | Plan-R1: Safe and Feasible Trajectory Planning as Language Modeling |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=uusTA1rBhR); [GitHub](https://github.com/XiaolongTang23/Plan-R1) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | Plan‑R1 |
| Dataset | nuPlan Val14 (Reactive), nuPlan Test14‑hard (Reactive), nuPlan Test14‑random (Reactive) |

> [!tip] 效果简介
> - nuPlan Val14 (Reactive) 上，R‑CLS 为 87.69 (Plan‑R1)，对比 82.80 (Diffusion Planner)，变化 +4.89。
> - nuPlan Test14‑hard (Reactive) 上，R‑CLS 为 77.20 (Plan‑R1)，对比 69.22 (Diffusion Planner)，变化 +7.98。
> - nuPlan Test14‑random (Reactive) 上，R‑CLS 为 90.04 (Plan‑R1)，对比 82.93 (Diffusion Planner)，变化 +7.11。

## 概述

### 问题与瓶颈

轨迹规划是自动驾驶的核心环节，要求同时满足安全、舒适与交通规则合规等多重目标。现有学习型规划器普遍依赖专家演示进行模仿学习，虽然能够捕捉类人驾驶行为，却缺乏明确的安全意识——它们可能无差别地继承专家数据中的超速、压线等不良行为，在闭环仿真中引发碰撞或违规。另一方面，将强化学习直接应用于多目标规划时，常用的分组相对策略优化（GRPO）存在一个关键缺陷：其分组归一化操作会消除不同组之间的奖励尺度差异，导致稀有的高方差安全违规组的优势被压缩至与大量低方差安全组相似的水平，从而稀释安全关键信号，抑制对安全目标的优化。

### 核心思路

Plan‑R1 将轨迹规划重新定义为**原则对齐的自回归预测任务**，通过**解耦行为学习与原则对齐**来解决上述瓶颈。方法采用两阶段框架：

1. **预训练阶段**：在专家数据上训练一个通用的自回归运动预测器，捕捉多样化的多智能体交互行为，不涉及任何安全或合规约束。
2. **微调阶段**：将预训练模型初始化为自车规划器，利用无需人类偏好数据的**规则化奖励**进行强化学习微调，显式对齐安全、舒适、合规等规划原则。同时引入**双模型设计**——可训练的自车规划器与冻结的预训练世界模型交互，实现反应式闭环仿真，使自车能够感知周围智能体对其决策的响应。

为克服 GRPO 在安全关键场景中的梯度稀释问题，Plan‑R1 提出了**方差解耦 GRPO（VD‑GRPO）**：用中心化和固定全局缩放替代分组方差归一化，保留绝对奖励幅度，确保安全关键目标在训练全过程中保持主导梯度。

### 方法定位

Plan‑R1 属于**学习型规划器**，但与纯模仿学习方法（如 PlanTF、Diffusion Planner）不同，它引入了基于规则的强化学习微调，使模型在保留类人驾驶行为的同时显式对齐安全原则。与规则型规划器（如 PDM‑Closed、Gameformer）相比，Plan‑R1 不依赖手工设计的后处理规则，而是通过端到端学习实现原则对齐。在方法谱系中，Plan‑R1 桥接了行为学习与原则约束，可视为一种**原则引导的生成式规划范式**。

### 主要结果

在 nuPlan 基准测试上，Plan‑R1 取得了领先性能：

- **Val14 反应式模式**：R‑CLS 达到 87.69，较此前最优的 Diffusion Planner（82.80）提升 **+4.89**。
- **Test14‑hard 反应式模式**：R‑CLS 达到 77.20，较 Diffusion Planner（69.22）提升 **+7.98**。
- **Test14‑random 反应式模式**：R‑CLS 达到 90.04，较 Diffusion Planner（82.93）提升 **+7.11**，创下该基准的最新记录。

消融实验进一步验证了各设计的有效性：VD‑GRPO 将碰撞避免指标从 93.87 提升至 97.32，显著优于标准 GRPO；反应式世界模型使 R‑CLS 达到 90.04，优于回放真实轨迹（87.44）和仅预训练基线（82.81）；移除碰撞奖励组件则导致 NR‑CLS 骤降至 73.10，证实了安全约束的核心作用。

## 背景与动机

轨迹规划是自动驾驶系统的核心模块，其目标是在动态、多智能体环境中生成安全、可行且合规的未来运动序列。近年来，基于学习的规划器取得了显著进展，但它们普遍存在一个根本性瓶颈：**高度依赖专家演示数据，缺乏明确的安全意识**。纯模仿学习范式使模型倾向于复现人类驾驶行为，却无法区分安全操作与不良习惯——当专家数据中包含超速、激进变道等行为时，模型会不加甄别地继承这些模式，从而在闭环运行中产生安全隐患。

这一问题的深层原因在于，现有方法将行为学习与安全原则对齐耦合在单一训练阶段中。无论是纯模仿学习，还是联合模仿学习与强化学习的方法，其优化目标均未显式编码安全约束，导致模型在面临分布外场景时缺乏可靠的决策边界。与此同时，将通用强化学习算法直接应用于多目标轨迹规划时，会引入新的优化偏差。具体而言，**GRPO（Group Relative Policy Optimization）的分组归一化机制会消除跨组奖励的尺度差异**：在安全关键场景中，少数包含碰撞等严重违规的高方差组与大量安全组的归一化优势值趋于相似，使得安全违规信号被稀释，模型难以将优化资源集中于安全目标的提升。

上述缺口催生了一个核心动机：**能否将行为学习与原则对齐解耦，使规划器既能捕捉类人驾驶的多样性和流畅性，又能通过显式的规则化反馈强制满足安全与合规约束？** 这要求重新审视轨迹规划的范式——不再将其视为单纯的模仿问题，而是定义为一个原则对齐的自回归预测任务：预训练阶段学习通用的多智能体运动模式，微调阶段利用无需人类偏好数据的规则化奖励实现安全对齐。

此外，解决 GRPO 在多目标优化中的信号稀释问题同样关键。这需要一种保留绝对奖励幅度的策略优化方法，确保安全关键目标在训练全过程中保持主导梯度，而非被大量低风险样本的平均效应淹没。Plan-R1 正是在这两个维度上提出了系统性解决方案：通过两阶段框架实现行为与原则的解耦，并通过方差解耦的 VD-GRPO 算法保障安全优化的优先级。

## 核心创新

Plan‑R1 的核心创新在于将轨迹规划重新定义为**原则对齐的自回归预测任务**，并通过两阶段框架与方差解耦的强化学习目标，系统性解决了现有学习型规划器的两大瓶颈：对专家演示的过度依赖导致的安全意识缺失，以及多目标强化学习中安全信号被稀释的问题。

### 瓶颈一：纯模仿学习继承不良行为

现有学习型规划器（如 PLUTO、Diffusion Planner）高度依赖专家演示进行模仿学习，缺乏明确的安全意识。如图 2 所示，专家轨迹本身存在超速行为，而纯学习型方法会忠实地复现这些不良模式。这一现象的根源在于**行为学习与安全原则的耦合**——模型仅被训练为“像专家一样驾驶”，而非“安全地驾驶”。

### 创新一：两阶段解耦框架

Plan‑R1 将行为学习与原则对齐解耦为两个独立阶段（图 1）：

- **第一阶段（预训练）**：在专家数据上通过 next‑motion‑token 预测的自回归目标，训练一个通用的多智能体运动预测器 $p_a$，捕捉类人驾驶行为的多样性。该阶段不涉及任何安全约束，仅建立强行为先验。
- **第二阶段（RL 微调）**：将预训练模型初始化为自车规划器 $\pi_e$，使用基于规则的奖励函数进行强化学习微调，显式对齐安全、舒适、合规等规划原则。奖励函数采用乘性安全指标与加性代价项的混合设计：
  $$R(y_t) = \prod_{k\in\mathcal{T}_{safe}} \mathbf{1}_{k,t} \cdot \sum_{j\in\mathcal{T}_{cost}} w_j \cdot r_j(y_t)$$
  其中安全指标（碰撞、可行驶区域等）以乘积形式确保任何安全违规都将奖励归零，从而赋予安全约束绝对优先级。

该框架的关键优势在于**无需人类偏好数据**：规则化奖励直接编码了可验证的物理约束，避免了 RLHF 中昂贵且可能存在偏好的标注过程。

### 瓶颈二：GRPO 分组归一化稀释安全信号

在将 GRPO 直接应用于多目标规划时，其分组归一化（per‑group normalization）会消除跨组奖励尺度差异。由于安全违规组（低奖励、高方差）在训练中较为稀有，而安全组（高奖励、低方差）大量存在，归一化后两者的优势值分布趋于相似（图 4），导致安全关键目标的梯度被稀释，模型难以有效优化安全行为。

### 创新二：VD‑GRPO 保留绝对奖励幅度

Plan‑R1 提出 **Variance‑Decoupled GRPO (VD‑GRPO)**，通过移除方差归一化来保留绝对奖励幅度：

$$\tilde{R}^{VD}(y_t^g) = \frac{R(y_t^g) - \mu_R}{c}$$

其中 $\mu_R$ 为全局奖励均值，$c$ 为固定缩放常数。与标准 GRPO 的分组均值/标准差归一化相比，VD‑GRPO 仅进行中心化和固定缩放，**不消除组间方差差异**。这使得安全违规组的优势值天然大于安全组，确保安全关键目标在训练全过程中保持主导梯度。

图 5 的训练动态验证了这一机制的有效性：VD‑GRPO 持续降低不安全组比例，而标准 GRPO 在训练后期出现不安全行为反弹。消融实验（表 2）进一步量化了 VD‑GRPO 的贡献：碰撞避免指标从 GRPO 的 93.87 提升至 97.32（+3.45），反应式 CLS 从 88.35 提升至 90.04。

### 创新三：双模型反应式仿真

RL 微调阶段采用**双模型设计**：可训练的自车规划器 $\pi_e$ 与冻结的预训练模型 $p_a$（作为反应式世界模型）交互。在 rollout 过程中，$\pi_e$ 探索新策略，$p_a$ 预测周围智能体对自车决策的反应，实现交互感知的闭环仿真。这一设计解决了传统 RL 规划中环境交互不真实的问题——消融实验（表 3）表明，反应式世界模型的 R‑CLS 达到 90.04，显著优于回放真实轨迹（87.44）和仅预训练基线（82.81）。

### 方法谱系与知识库定位

Plan‑R1 在以下维度上区别于现有方法：

| 维度 | 现有方法 | Plan‑R1 |
|------|---------|---------|
| **训练范式** | 仅模仿学习（PlanTF, Diffusion Planner）或联合 IL+RL | 两阶段：自回归预训练 → 规则化 RL 微调 |
| **RL 奖励归一化** | GRPO 分组均值/标准差归一化 | VD‑GRPO：中心化 + 全局固定缩放 |
| **多智能体交互建模** | 回放真实轨迹或非反应式仿真 | 双模型：可训练规划器 + 冻结反应式世界模型 |

在 nuPlan 最具挑战性的反应式基准上，Plan‑R1 取得了最新的 R‑CLS 成绩（Test14‑random: 90.04，比 **Diffusion Planner**（Zheng et al., 2025）高 +7.11），验证了上述创新的综合有效性。

## 整体框架

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_uusTA1rBhR/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of our Plan-R1: Stage (a) pre-trains a motion predictor on expert data; Stage (b) fine-tunes it with VD-GRPO using rule-based rewards to align with planning principles*

Plan‑R1 将轨迹规划重新定义为**原则对齐的自回归预测任务**，并通过两阶段框架将行为学习与规划原则对齐解耦，从而克服纯专家演示方法继承不良行为（如超速）的瓶颈。其整体 pipeline 由五个核心模块串联构成，形成从数据表征到策略优化的完整闭环。

### 运动分词（Motion Tokenization）

连续轨迹首先通过 K‑disk 聚类算法离散化为运动 token，构建一个有限的动作词汇表。这一分词操作将连续规划空间转换为离散序列，使自回归 Transformer 能够以 next‑motion‑token 预测的方式处理多智能体运动生成问题。

### Transformer 解码器与因子化注意力

模型主体采用**因子化注意力 Transformer 解码器**，通过三种注意力机制建模多智能体时空交互：
- **时序自注意力**：捕捉同一智能体沿时间维度的运动连贯性；
- **地图‑智能体交叉注意力**：将车道几何与交通规则等上下文信息注入智能体表征；
- **智能体间交叉注意力**：建模周围智能体之间的空间交互。

该架构同时服务于预训练阶段的全智能体运动预测和微调阶段的自车规划器。

### 自回归预训练

在第一阶段，模型在专家驾驶数据上以 **next‑motion‑token 负对数似然**为目标进行自回归预训练，学习通用的类人多智能体运动模式。预训练损失为：

$$\mathcal{L}_{\text{pretrain}} = -\sum_{t=1}^{F}\sum_{n=0}^{N} \log p_a(y_{t,n} \mid y_{<t,0:N}, C)$$

其中 $p_a$ 为智能体预测器，$C$ 为上下文信息，$F$ 为未来帧数，$N$ 为周围智能体数量。此阶段不引入任何显式安全约束，仅捕捉数据中的行为分布。

### 双模型 Rollout 与规则化奖励

第二阶段微调时，Plan‑R1 采用**双模型设计**实现交互感知的闭环仿真：
- **可训练的自车规划器** $\pi_e$：以原则 $P$ 为条件，探索新的决策策略；
- **冻结的预训练世界模型** $p_a$：预测周围智能体对自车行为的反应式响应。

每次 rollout 中，$\pi_e$ 生成自车运动 token，$p_a$ 同步预测其他智能体的反应，形成交互式轨迹。随后通过**规则化奖励函数**评估轨迹质量：

$$R(y_t) = \prod_{k\in\mathcal{T}_{\text{safe}}} \mathbf{1}_{k,t} \cdot \sum_{j\in\mathcal{T}_{\text{cost}}} w_j \cdot r_j(y_t)$$

该奖励采用**乘性安全指标**（碰撞、可行驶区域合规等）与**加性软代价项**（舒适性、TTC、速度合规、进展）的乘积结构：一旦安全约束被违反，对应指示函数归零，整个奖励直接归零，从而在结构上赋予安全绝对优先级。

### VD‑GRPO 策略优化

标准 GRPO 在微调时对每组轨迹独立进行均值‑标准差归一化，这会**消除跨组奖励尺度差异**，导致稀有的高方差安全违规组与大量低方差安全组获得相近的归一化优势，稀释安全关键信号的梯度主导地位。

Plan‑R1 提出 **VD‑GRPO**（Variance‑Decoupled GRPO），将分组归一化替换为**中心化与固定全局缩放**：

$$\tilde{R}^{\text{VD}}(y_t^g) = \frac{R(y_t^g) - \mu_R}{c}$$

其中 $\mu_R$ 为全局奖励均值，$c$ 为固定缩放常数。通过移除方差项，VD‑GRPO 保留了不同组之间的绝对奖励幅度差异，确保安全关键目标在训练全过程中保持优势梯度。微调损失在 GRPO 框架下结合重要性采样比率、累积优势与 KL 散度惩罚，约束策略不偏离参考策略过远。

### 数据流与模块关系

整体信息流为：场景上下文 $C$ 与历史运动序列 → 运动分词 → Transformer 解码器（因子化注意力）→ 自回归运动 token 序列 → 规则化奖励评估 → VD‑GRPO 优势计算与策略更新。预训练阶段仅使用专家数据优化 $p_a$；微调阶段冻结 $p_a$ 作为世界模型，仅更新 $\pi_e$，实现行为学习与原则对齐的结构化解耦。

## 核心模块与公式推导

### 问题形式化：原则对齐的自回归序列预测

Plan‑R1 将轨迹规划重新定义为**原则对齐的自回归预测任务**。给定高精地图 $M$、历史轨迹 $X$ 和规划原则 $P$（安全、舒适、合规等），模型需预测所有智能体在未来 $F$ 个时间步的联合运动 $Y = \{y_{1,0:N}, \dots, y_{F,0:N}\}$。核心分解如 **Equation (1)** 所示：

$$p(Y \mid C, P) \approx \prod_{t=1}^{F} \pi_e(y_{t,0} \mid y_{<t,0:N}, C, P) \prod_{n=1}^{N} p_a(y_{t,n} \mid y_{<t,0:N}, C)$$

其中：
- $C = \{M, X\}$ 为场景上下文；
- $\pi_e$ 为**可训练的自车规划器**，显式条件于原则 $P$；
- $p_a$ 为**冻结的智能体预测器**（世界模型），仅条件于历史与上下文；
- 该分解假设周围智能体运动独立于自车规划原则，从而将行为学习与原则对齐解耦。

### 运动分词与模型架构

连续轨迹通过 **K‑disk 聚类算法** 离散化为运动 token 词汇表，使规划问题转化为离散 token 的自回归生成。模型采用 **Transformer Decoder with Factorized Attention**，包含三层注意力机制：
- **时序自注意**：建模单智能体的时间依赖；
- **地图‑智能体交叉注意**：融合道路拓扑与交通规则；
- **智能体间交叉注意**：捕获多智能体交互。

### 预训练：行为先验建立

预训练阶段使用专家数据，对所有智能体的 next‑motion‑token 进行负对数似然优化，如 **Equation (2)**：

$$\mathcal{L}_{\text{pretrain}} = -\sum_{t=1}^{F}\sum_{n=0}^{N} \log p_a(y_{t,n} \mid y_{<t,0:N}, C)$$

该阶段不涉及原则 $P$，仅学习通用的类人多智能体运动模式，为后续微调提供强行为先验。

### 双模型 Rollout：反应式闭环仿真

RL 微调阶段采用**双模型设计**：可训练的自车规划器 $\pi_e$ 与冻结的预训练世界模型 $p_a$ 交互。在 rollout 中，$\pi_e$ 探索新策略，$p_a$ 预测周围智能体的反应，实现交互感知的闭环仿真。这是 Plan‑R1 在反应式基准上取得显著提升的关键——仅回放真实轨迹（non‑reactive）无法模拟自车决策变化引发的他车响应。

### 规则化奖励设计

奖励函数 **Equation (3)** 采用乘性安全指标与软性代价项的加权和之积：

$$R(y_t) = \prod_{k \in \mathcal{T}_{\text{safe}}} \mathbf{1}_{k,t} \cdot \sum_{j \in \mathcal{T}_{\text{cost}}} w_j \cdot r_j(y_t)$$

- $\mathcal{T}_{\text{safe}}$ 包含碰撞、可行驶区域合规等**硬性安全约束**，不满足时通过指示函数 $\mathbf{1}_{k,t}$ 将奖励归零；
- $\mathcal{T}_{\text{cost}}$ 包含舒适性、TTC、速度合规、进展等**软性代价项**，通过权重 $w_j$ 调节优先级；
- 该设计确保安全约束具有绝对优先权，而非与舒适性等目标简单加权。

### VD‑GRPO：解耦方差的策略优化

标准 GRPO 的分组归一化会消除跨组奖励尺度差异，导致稀有的高方差安全违规组与大量低方差安全组的归一化优势相似，稀释安全关键信号。**VD‑GRPO** 通过 **Equation (5)** 解决此问题：

$$\tilde{R}^{\text{VD}}(y_t^g) = \frac{R(y_t^g) - \mu_R}{c}$$

- $\mu_R$ 为全局奖励均值，$c$ 为**固定缩放常数**（超参数研究 Figure 9 表明 VD‑GRPO 对 $c$ 不敏感）；
- 该设计移除了方差归一化，保留不同组间的绝对奖励幅度差异，确保安全关键目标在训练全过程中保持主导梯度（Figure 4 提供了安全组与不安全组绝对优势分布的对比证据）。

微调损失 **Equation (4)** 在 VD‑GRPO 奖励归一化基础上，结合重要性采样比率、累积优势 $\hat{A}_t^g$ 以及 KL 散度惩罚项 $\beta D_{KL}[\pi_e \| \pi_{\text{ref}}]$，控制策略不偏离预训练参考模型过远。

## 实验与分析

### 主要结果

我们在 nuPlan 基准的三个测试子集上对 Plan‑R1 进行了全面评估，区分非反应式（NR）与反应式（R）模式，并与专家回放、规则型/混合型规划器和纯学习型规划器进行对比。表 1 汇总了核心指标 CLS（综合闭环得分）。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_uusTA1rBhR/figures/002_Table_1.jpg]]
*Table 1: Comparison with SOTAs on nuplan benchmark. The best result is in bold and the second best result is underlined. *: with rule-based post-processing. NR/R: non-reactive/reactive mode*

**非反应式模式**下，Plan‑R1*（带规则后处理）在 Val14 上取得 94.72 NR‑CLS，在所有方法中排名第一；在 Test14‑hard 上，Plan‑R1（无后处理）达到 77.45 NR‑CLS，超越所有纯学习型基线。**反应式模式**是更具挑战性的设置，要求规划器在交互式仿真中实时响应周围智能体的动态变化。在此设置下，Plan‑R1 在 Test14‑random 上取得 90.04 R‑CLS，比此前最优的纯学习型方法 Diffusion Planner（82.93）高出 **+7.11**；在 Test14‑hard 上达到 77.20 R‑CLS，领先 Diffusion Planner **+7.98**。带后处理的 Plan‑R1* 在反应式模式下同样表现出色，Test14‑random 达到 93.71 R‑CLS，为所有方法中的最高值。

这些结果表明，Plan‑R1 的两阶段设计——先通过预训练捕捉类人多智能体运动模式，再通过基于规则的强化学习微调显式对齐安全与合规原则——在安全性和可行性两个维度上都取得了显著提升。

### 消融实验

#### 基于规则的 RL 微调与 VD‑GRPO 的作用

表 2 系统消融了 RL 微调和 VD‑GRPO 的贡献。仅预训练的基线在反应式模式下仅取得 82.81 R‑CLS。引入标准 GRPO 微调后，NR‑CLS 提升 3.04，可行驶区域合规性（Drivable）从 88.25 提升至 95.03，但关键的碰撞避免指标（Collision）却从 94.83 **下降**至 93.87。这一反常现象揭示了 GRPO 的核心缺陷：其分组归一化消除了跨组奖励尺度差异，导致稀有的高方差安全违规组与大量低方差安全组获得相似的优势估计，从而稀释了安全关键信号的优化梯度。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_uusTA1rBhR/figures/007_Table_2.jpg]]
*Table 2: Ablation study on the importance of ruled-based RL fine-tuning and VD-GRPO*

VD‑GRPO 通过移除方差归一化、仅保留中心化和固定缩放，解决了上述问题。相比标准 GRPO，VD‑GRPO 将碰撞避免指标从 93.87 提升至 **97.32**（+3.45），可行驶区域合规性达到 97.32，TTC 指标达到 95.02，最终 R‑CLS 达到 90.04。图 4 进一步从机制层面验证了这一解释：标准 GRPO 下安全组与不安全组的绝对优势分布高度重叠，而 VD‑GRPO 使不安全组产生显著更大的优势值，确保安全目标在训练全过程中保持主导梯度。图 5 显示，VD‑GRPO 在训练过程中持续降低不安全组的比例，而 GRPO 则表现出波动甚至回升。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_uusTA1rBhR/figures/009_Figure_4.jpg]]
*Figure 4: Distributions of |Aˆ| for safe vs. unsafe groups*

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_uusTA1rBhR/figures/011_Figure_5.jpg]]
*Figure 5: Proportion of unsafe groups during training. Table 3: Ablation on model capacity and world model (WM) choices*

#### 世界模型与交互感知仿真

表 3 消融了世界模型（WM）选择对反应式规划性能的影响。回放真实轨迹（GT Replay）作为世界模型时，R‑CLS 为 87.44，优于仅预训练基线（82.81），但显著低于使用冻结预训练模型作为反应式世界模型的方案（**90.04**）。这一差距验证了双模型设计的必要性：冻结的世界模型能够根据自车规划器的探索性决策实时预测周围智能体的反应，从而在 RL 微调过程中提供交互感知的仿真环境，使规划器学会在动态多智能体场景中做出安全决策。

#### 奖励组件的重要性

表 5 消融了各奖励组件对性能的贡献。完整奖励函数（包含碰撞、可行驶区域、速度合规、舒适性和进展五项）在非反应式模式下达到 91.23 NR‑CLS。移除碰撞奖励（乘性安全约束）导致 NR‑CLS 骤降至 73.10，降幅达 18.13，验证了乘性安全指标在奖励设计中的绝对优先地位。移除可行驶区域奖励同样造成显著退化。速度合规、舒适性和进展等软性代价项的移除影响相对温和，表明安全约束是性能的核心支柱。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_uusTA1rBhR/figures/017_Table_5.jpg]]
*Table 5: Ablation study on the reward components*

#### 超参数敏感性

表 4 展示了组大小 G 的影响。G=4 在准确率（NR‑CLS 91.23，R‑CLS 90.04）与计算效率（24 GB 显存）之间取得最佳平衡。更大的 G 值增加显存开销但未带来性能增益。图 9 显示 VD‑GRPO 对固定缩放常数 c 不敏感，在较宽范围内性能保持稳定，验证了该设计的鲁棒性。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_uusTA1rBhR/figures/014_Table_4.jpg]]
*Table 4: Ablation on Group Size G*

### 定性分析

图 2 对比了闭环仿真中自车轨迹的速度合规性。专家演示（a）和纯学习型方法 PLUTO（b）、Diffusion Planner（c）均继承了超速行为（橙色段），而 Plan‑R1（d）全程保持合规速度。图 3 进一步展示了预训练基线存在的典型失败模式——偏离道路、超速、与静态障碍物碰撞——而 Plan‑R1 成功避免了这些问题。这些定性结果直观地验证了基于规则的 RL 微调能够有效纠正从专家数据中继承的不良行为。

### 采样效率与泛化能力

图 7 的 Pass@k 分析表明，Plan‑R1 在相同采样预算下始终优于预训练基线，且随着采样次数增加，优势进一步扩大，验证了原则对齐对采样效率的提升。在 interPlan 基准（表 6）上，Plan‑R1* 取得 72.33 分，在规则型/混合型方法中排名第一；Plan‑R1（无后处理）在学习型方法中排名第二（55.90），仅次于 PLUTO（57.74），展示了良好的跨基准泛化能力。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_uusTA1rBhR/figures/018_Table_6.jpg]]
*Table 6: Comparison with SOTAs on interPlan benchmark. The best result is in bold and the second best result is underlined. *: with rule-based post-processing*

### 世界模型鲁棒性

表 7 分析了冻结世界模型在自车状态受高斯噪声扰动时的鲁棒性。当噪声标准差 σ 从 0 增加到 10.0 m 时，ADE 仅从 1.03 m 退化至 1.26 m，FDE 从 3.01 m 退化至 3.59 m，表明世界模型对自车状态扰动具有较强容忍度，为 RL 微调过程中自车规划器的探索提供了稳定的仿真基础。

![[assets/figures/papers/paper_list_l45_https_openreview_net_forum_id_uusTA1rBhR/figures/019_Table_7.jpg]]
*Table 7: Robustness of the frozen world model under ego-state perturbations. Gaussian noise with standard deviation σ is injected into ego states*

## 方法谱系与知识库定位

### 1. 与现有方法的谱系关系

Plan‑R1 在轨迹规划的方法谱系中占据一个独特位置：它同时跨越了“学习型规划器”与“规则型规划器”的传统边界，并通过两阶段框架将二者的优势解耦融合。

**相对于纯学习型规划器**，Plan‑R1 的核心突破在于解耦“行为学习”与“原则对齐”。纯学习型方法——如 **UrbanDriver** (Scheel et al., 2022)、**PDM‑Open** (Dauner et al., 2023)、**PlanTF** (Cheng et al., 2024b)、**PLUTO** (Cheng et al., 2024a) 和 **Diffusion Planner** (Zheng et al., 2025)——完全依赖专家演示进行模仿学习。这一范式的根本局限在于：专家数据中天然存在超速、压线等不良行为，而纯模仿学习缺乏明确的安全意识，会不加区分地继承这些行为（见 Figure 2）。Plan‑R1 的预训练阶段虽然同样使用专家数据，但其目标仅是捕捉通用的多智能体运动模式作为行为先验；真正的安全对齐发生在第二阶段基于规则的强化学习微调中，此时模型通过显式的安全、合规等原则奖励来纠正从数据中继承的不良行为。

**相对于规则型规划器**，Plan‑R1 的优势在于无需手工设计复杂的后处理逻辑。规则型方法——如 **IDM** (Treiber et al., 2000)、**PDM‑Closed** 和 **PDM‑Hybrid** (Dauner et al., 2023)、**Gameformer** (Huang et al., 2023) 以及 **PlanAgent** (Zheng et al., 2024b)——依赖确定性规则或搜索算法来保证安全，但在复杂交互场景中缺乏灵活性和泛化能力。Plan‑R1 通过双模型设计（可训练的自车规划器 + 冻结的预训练世界模型）实现了反应式闭环仿真，使自车能够感知周围智能体的反应并自适应地调整策略，而非依赖静态规则。在最具挑战性的反应式基准 Test14‑random 上，Plan‑R1 的 R‑CLS 达到 90.04，比 **Diffusion Planner** 高出 +7.11 分，比带后处理的 **PDM‑Hybrid** 高出 +2.34 分（Table 1），验证了学习型反应式仿真的优势。

**相对于 GRPO 及其变体**，Plan‑R1 提出的 VD‑GRPO 解决了一个此前未被充分认识的多目标优化瓶颈。标准 GRPO 通过分组归一化（减均值除标准差）来稳定训练，但当奖励由多个尺度差异巨大的目标组成时，这种归一化会消除跨组的奖励幅度差异。具体而言，安全违规组（如碰撞）出现频率低但奖励方差高，而安全组的奖励分布集中且方差低；GRPO 的归一化使得两类组的优势值变得相似，从而稀释了安全关键信号（Figure 4）。VD‑GRPO 通过仅做中心化并采用全局固定缩放常数 $c$，保留了绝对奖励幅度，确保安全关键目标在训练全过程中保持主导梯度。这一改进使碰撞避免指标从 93.87 提升至 97.32（Table 2），且 VD‑GRPO 对缩放常数 $c$ 不敏感（Figure 9），具有良好的超参数鲁棒性。

### 2. 适用边界

Plan‑R1 的有效性建立在以下前提之上：

- **专家数据质量**：预训练阶段依赖专家演示来学习通用的多智能体运动模式。虽然微调阶段可以纠正不良行为，但若预训练数据严重缺乏某些场景（如极端天气、罕见交互模式），世界模型的反应预测能力将受到限制。
- **奖励设计的完备性**：基于规则的奖励函数（Equation 3）采用乘性安全指标与加性代价项的组合，安全约束不满足时奖励直接归零。这一设计假设所有关键安全维度（碰撞、可行驶区域、速度合规等）已被正确枚举和检测；若存在未建模的安全维度，RL 微调可能产生奖励黑客行为。
- **世界模型的冻结假设**：双模型设计中，周围智能体的反应由冻结的预训练模型 $p_a$ 预测，假设其行为独立于自车的规划原则 $P$（Equation 1）。这一假设在自车行为发生显著分布偏移时可能被打破。Table 7 显示冻结世界模型对高斯噪声注入的自车状态扰动具有一定鲁棒性，但更极端的分布外行为仍需进一步验证。
- **计算资源**：VD‑GRPO 的组大小 $G=4$ 在准确率与计算效率之间取得最佳平衡（NR‑CLS 91.23，R‑CLS 90.04，24 GB 显存，Table 4），但更大的 $G$ 会显著增加显存消耗且性能反而下降。

### 3. 局限与开放问题

尽管 Plan‑R1 在 nuPlan 基准上取得了最优性能，论文中未明确讨论的局限和开放问题包括：

- **奖励函数的泛化性**：当前奖励函数（Equation 3）中的安全指标和代价项是针对 nuPlan 场景设计的，其向真实世界的迁移需要重新校准检测器（如碰撞检测、可行驶区域判定）和权重。论文未在 nuPlan 之外的数据集上验证奖励设计的泛化能力。
- **长尾安全场景**：VD‑GRPO 通过保留绝对奖励幅度来优先优化安全目标，但安全违规组的稀有性意味着模型在训练中见到这些场景的频次仍然很低。Figure 5 显示不安全组比例在训练中持续下降，但无法保证所有类型的安全违规都被充分覆盖。
- **多原则冲突的显式建模**：当前框架将安全、舒适、合规等原则统一编码为奖励函数，但未显式处理原则之间的冲突（如紧急避障时不得不违反交通规则）。模型通过奖励加权隐式地学习折中策略，缺乏可解释的原则优先级机制。
- **世界模型的主动适应性**：冻结世界模型无法根据自车策略的变化调整其行为预测，这在自车采取激进策略时可能导致仿真失真。未来工作可探索世界模型的在线适应或对抗训练。
- **interPlan 基准的验证深度**：Table 6 报告了 interPlan 基准上的对比结果，但论文未详细分析 Plan‑R1 在该基准上的失败模式或与 nuPlan 结果的行为差异原因，这一部分需要进一步手动验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Plan_R1_Safe_and_Feasible_Trajectory_Planning_as_Language_Modeling.pdf]]
