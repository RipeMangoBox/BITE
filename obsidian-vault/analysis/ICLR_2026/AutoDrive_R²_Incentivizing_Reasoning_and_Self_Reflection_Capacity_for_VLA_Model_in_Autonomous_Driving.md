---
title: "AutoDrive-R²: Incentivizing Reasoning and Self-Reflection Capacity for VLA Model in Autonomous Driving"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: "paperPDFs/ICLR_2026/AutoDrive_R²_Incentivizing_Reasoning_and_Self_Reflection_Capacity_for_VLA_Model_in_Autonomous_Driving.pdf"
project_link: null
code_link: null
openreview_forum_id: KVWaCzJrrq
aliases:
- AR
- ARIRSRCVMAD
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "引入四步思维链（观察→计算→逻辑→自反思）与基于物理的多维度奖励（空间对齐、车辆动力学、时间平滑性），使模型在推理质量和物理约束之间取得平衡。"
primary_logic: "有效的自动驾驶需要能够自验证的结构化推理过程，并通过物理约束进行优化，以生成安全、可行且舒适的轨迹。"
claims:
- "去除自反思（w/o Self.）使平均L2误差增加21.1%"
- "去除时间平滑奖励（r_tem）导致平均L2误差增加26.3%"
- "在nuScenes上相比EMMA+，平均L2误差降低34.5%"
- "在Waymo零样本上相比Qwen2.5-VL-7B，平均L2误差降低90.7%"
---

# AutoDrive-R²: Incentivizing Reasoning and Self-Reflection Capacity for VLA Model in Autonomous Driving

> [!tip] 核心洞察
> 有效的自动驾驶需要能够自验证的结构化推理过程，并通过物理约束进行优化，以生成安全、可行且舒适的轨迹。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AutoDrive-R²：激励自动驾驶VLA模型的推理与自反思能力 |
| 英文题名 | AutoDrive-R²: Incentivizing Reasoning and Self-Reflection Capacity for VLA Model in Autonomous Driving |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=KVWaCzJrrq) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | AutoDrive-R² |
| Dataset | nuScenes, Waymo, NAVSIM (Closed-loop) |

> [!tip] 效果简介
> - nuScenes 上，L2 Error (m) Avg. 为 0.19，对比 0.29 (EMMA+)，变化 -34.5%。
> - Waymo 上，L2 Error (m) Avg. 为 0.19，对比 0.30 (EMMA+)，变化 -33.3%。
> - NAVSIM (Closed-loop) 上，PDMS↑ 为 90.3，对比 84.0 (Para-Drive)，变化 +6.3。

## 概要

### 1. 问题与瓶颈

现有视觉-语言-动作（VLA）模型在自动驾驶轨迹规划中面临一个核心瓶颈：**缺乏结构化的推理过程与物理可行性约束**。无论是通用视觉语言模型（如 **Qwen2.5-VL-7B**，Bai et al., 2025）还是专用驾驶模型（如 **EMMA+**，Hwang et al., 2024），在复杂场景下往往直接输出轨迹坐标，跳过了对场景的深度理解、物理规律的应用以及推理结果的自验证，导致生成的轨迹预测不准确且物理不可行。

### 2. 核心方法：AutoDrive-R²

针对上述瓶颈，**AutoDrive-R²** 提出了一个两阶段的 VLA 训练框架，通过**结构化思维链**与**物理接地奖励**的协同作用来提升模型的推理质量与物理可行性。

- **第一阶段（SFT）**：构建名为 **nuScenesR²-6K** 的思维链数据集，对基础 VLM 进行监督微调。该数据集采用四步推理链——**观察（Observation）→ 计算（Calculation）→ 逻辑（Logic）→ 自反思（Reflection）**，使模型在输出轨迹前先进行场景分析、运动学计算、交通规则推理与自我验证。
- **第二阶段（RL）**：采用**组相对策略优化（GRPO）**，并设计了一个**物理接地奖励框架**，综合考量空间对齐误差、转向角偏差、速度偏差以及时间平滑性，引导模型生成既准确又物理可行的轨迹。

### 3. 核心结论

实验证据表明，AutoDrive-R² 在多个基准上实现了显著提升：

- **nuScenes 开环评估**：相比 EMMA+，平均 L2 误差降低 **34.5%**（0.19m vs. 0.29m，Table 1）。
- **Waymo 零样本评估**：相比 Qwen2.5-VL-7B，平均 L2 误差降低 **90.7%**（Table 2）。
- **NAVSIM 闭环评估**：PDMS 指标达到 **90.3**，优于 Para-Drive 的 84.0（Table 3）。

消融实验进一步揭示了关键组件的因果作用：去除自反思步骤使平均 L2 误差增加 **21.1%**；去除时间平滑奖励导致误差增加 **26.3%**；仅进行 RL 训练而不经 SFT 冷启动，误差升高 **22.2%**（Table 4）。这些结果验证了结构化推理与物理约束在自动驾驶 VLA 模型中的决定性作用。

### 4. 方法定位

AutoDrive-R² 定位于**通用 VLM 的自动驾驶专用化**路径，区别于两类基线：

- **训练型驾驶专家**（如 **UniAD**，Hu et al., 2023；**VAD**，Jiang et al., 2023）：依赖大规模驾驶数据从头训练，缺乏语言推理能力。
- **通用 VLM 直接应用**（如 Qwen2.5-VL-7B）：具备语言能力但缺乏领域推理结构与物理约束。

AutoDrive-R² 通过**仅 6k 样本的轻量训练**，在通用 VLM 基础上注入领域推理能力与物理常识，实现了数据效率与性能的平衡。



### 自动驾驶决策的核心瓶颈

自动驾驶系统需要在高度动态和不确定的环境中生成安全、物理可行且舒适的轨迹。近年来，视觉-语言-动作（VLA）模型在自动驾驶领域展现出巨大潜力，它们能够将视觉感知、语言理解和动作规划统一在一个端到端框架中。然而，现有VLA模型面临一个根本性瓶颈：**缺乏结构化的推理过程与物理可行性约束**。具体而言，当前模型通常直接从感知输入映射到轨迹输出，缺少显式的中间推理步骤，导致在复杂场景下生成的轨迹预测不准确且物理不可行。这种“黑箱”式决策方式使得模型难以解释其规划依据，也无法自我验证输出是否合理。

### 现有方法的局限性

当前自动驾驶决策方法可大致分为三类：

- **基于训练的驾驶专家模型**（如UniAD、VAD、BEV-Planner、Ego-MLP）：这些模型在特定数据集上表现良好，但泛化能力有限，且缺乏对场景的语义理解能力。
- **专用驾驶VLM模型**（如DriveVLM、OmniDrive、EMMA+）：通过引入视觉语言模型来增强场景理解，但推理过程仍较为简单，通常仅依赖直接预测或基础提示词推理，未充分利用结构化思维链的优势。
- **通用视觉语言模型**（如Qwen2.5-VL-7B）：虽然具备强大的视觉理解和语言生成能力，但在自动驾驶这一专业领域中缺乏领域知识和物理约束意识，导致轨迹预测误差较大。

上述方法的共同缺陷在于：**推理质量不足且缺少物理约束的显式建模**。模型可能生成在几何上看似合理但违反车辆动力学（如超出最小转弯半径、侧向加速度过大）或时间上不连续的轨迹，这在真实驾驶场景中可能引发严重安全问题。

### 核心洞察与研究动机

本工作的核心洞察是：**有效的自动驾驶需要能够自验证的结构化推理过程，并通过物理约束进行优化，以生成安全、可行且舒适的轨迹**。这一洞察源于对人类驾驶员决策过程的观察——人类驾驶员在规划路径时会自然地经历“观察路况→计算距离速度→逻辑判断→自我检查”的认知链条，同时其操作始终受车辆物理极限的约束。

基于此，本文提出AutoDrive-R²框架，旨在通过两个关键机制弥补现有方法的缺口：

1. **结构化思维链推理**：引入四步推理流程（观察→计算→逻辑→自反思），使模型能够显式地分析场景、量化运动参数、结合交通规则进行逻辑推理，并在最后通过自反思验证推理一致性并修正潜在矛盾。
2. **物理接地奖励优化**：设计融合空间对齐、车辆动力学（转向角、速度一致性）和时间平滑性的多维度奖励函数，通过强化学习使模型在推理质量和物理约束之间取得平衡。

通过将结构化推理与物理约束优化相结合，AutoDrive-R²旨在使VLA模型在自动驾驶任务中不仅“知道该做什么”，更能“验证做得对不对”，从而在nuScenes、Waymo等标准基准上实现更准确、更安全的轨迹规划。



## 核心方法与创新机理

AutoDrive-R² 的核心创新在于为自动驾驶 VLA（Vision-Language-Action）模型引入了一种**结构化的自验证推理机制**与**物理接地奖励优化框架**，从根本上改变了模型生成轨迹的方式。其创新可归结为三个紧密耦合的 changed slots：

### 1. 四步自反思思维链（Reasoning Process）

传统 VLA 模型（如 EMMA+、Qwen2.5-VL-7B）直接从视觉输入映射到轨迹坐标，缺乏显式的中间推理过程。AutoDrive-R² 将轨迹规划分解为四个递进且相互校验的阶段：

- **Observation（图像分析）**：建立基础场景理解，识别障碍物、车道线等关键元素
- **Calculation（物理计算）**：基于运动学方程将观测转化为量化预测
- **Logic（逻辑推理）**：结合交通规则进行安全检查和上下文推理
- **Reflection（自反思验证）**：反向检查推理链条的一致性，识别并修正矛盾

这一设计的核心洞见在于：**有效的自动驾驶需要能够自验证的结构化推理过程**。消融实验提供了强因果证据——去除四步推理结构（w/o. Four.）使平均 L2 误差增加 31.5%，去除自反思阶段（w/o. Self.）使误差增加 21.1%（Table 4）。这证明推理的完整性和自验证能力并非锦上添花，而是性能的关键瓶颈。

### 2. 物理接地的多维度奖励函数（Reward Function）

现有方法通常仅使用简单的 L2 位置误差作为优化目标，忽略了轨迹的物理可行性和驾驶舒适性。AutoDrive-R² 提出了一种物理接地奖励框架，将奖励信号分解为四个维度：

- **空间对齐奖励** $r_{pos}$：预测坐标与真值的均方欧氏距离（Eq. 4）
- **转向动力学奖励** $r_{ste}$：预测转向角与真值的偏差平方（Eq. 5）
- **速度一致性奖励** $r_{vel}$：预测速度与真值的偏差平方（Eq. 6）
- **时间平滑性奖励** $r_{tem}$：连续控制信号变化的惩罚项（Eq. 7）

四个奖励通过加权求和集成：$r_{acc} = \lambda_{pos} r_{pos} + \lambda_{ste} r_{ste} + \lambda_{vel} r_{vel} + \lambda_{tem} r_{tem}$（Eq. 8）。消融实验揭示了各维度的因果重要性：去除空间对齐奖励（w/o. $r_{pos}$）导致误差从 0.19m 剧增至 0.53m；去除时间平滑奖励（w/o. $r_{tem}$）使误差增加 26.3%（Table 4）。这表明物理约束不仅是锦上添花的正则项，而是模型学习可行轨迹的必要条件。

### 3. 两阶段训练策略（Training Strategy）

AutoDrive-R² 采用 SFT → RL 的两阶段训练范式，而非单阶段微调：

- **阶段一**：在 nuScenesR²-6K 数据集上进行监督微调（SFT），该数据集通过 “生成-验证” 流水线（Qwen2.5-VL-72B 生成，Qwen-VL-Max 验证）构建，包含四步 CoT 推理序列
- **阶段二**：使用 GRPO（Group Relative Policy Optimization）进行强化学习优化，采用上述物理接地奖励

这一策略的必要性得到了强因果验证：仅进行 RL 训练而不经过 SFT（7B + RL）比 SFT 基线（7B + SFT）的平均 L2 误差高出 22.2%（Table 4）。SFT 阶段提供的结构化推理先验是 RL 阶段有效优化的前提——没有 “冷启动” 的推理能力，物理奖励无法有效引导模型学习。

### 创新间的因果耦合

三个 changed slots 之间存在深层依赖关系。四步 CoT 为物理奖励提供了可优化的推理结构——模型需要先学会 “观察-计算-逻辑-反思” 的思维模式，物理奖励才能针对性地优化各阶段的输出质量。GRPO 的组内相对比较机制（Eq. 1-3）则使模型能够从多个候选轨迹中学习偏好，而非仅拟合单一真值。这种 “结构化推理 + 物理约束 + 相对优化” 的组合，使得 AutoDrive-R² 仅用 6k 训练样本（远少于 EMMA+ 的约 103k 样本）即在 nuScenes 上实现 34.5% 的误差降低（0.19m vs. 0.29m），并在 Waymo 零样本场景下相比 Qwen2.5-VL-7B 降低 90.7% 的误差。



![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_KVWaCzJrrq/figures/002_Figure_1.jpg]]
*Figure 1: Pipeline of our method. We adopt a two-stage training process. The first stage introduces an innovative CoT dataset named nuScenesR²-6K for SFT. The nuScenesR²-6K adopts a four-step logical chain with self-reflection to generate valuable chain-of-thought data. The second stage proposes an novel physics-grounded reward framework for RL optimization, which incorporates spatial alignment, vehicle dynamic, and temporal smoothness for reliable trajectory planning*

AutoDrive-R² 采用**两阶段训练框架**，将结构化推理能力与物理可行性约束注入 VLA 模型。其核心 pipeline 由两个顺序阶段构成，如图 1 所示。

**阶段一：监督微调（SFT）—— 冷启动推理能力**

首先构建名为 **nuScenesR²-6K** 的思维链数据集，该数据集通过 “生成-验证” 流水线创建：利用 Qwen2.5-VL-72B 合成初始 CoT 推理序列，再由 Qwen-VL-Max 作为验证器进行筛选。每条数据包含一个**四步逻辑链**：

1. **图像分析**：建立基础场景理解，包括障碍物检测与车道识别
2. **物理计算**：基于运动学方程将观测转化为量化预测
3. **逻辑推理**：结合交通规则进行安全检查与推理
4. **自反思验证**：反向检查推理一致性并修正矛盾

模型在此阶段学习结构化的 “观察→计算→逻辑→反思” 推理范式，为后续强化学习提供冷启动。

**阶段二：强化学习（RL）—— 物理接地优化**

采用**组相对策略优化**对模型进行强化学习训练。与标准 RLHF 不同，GRPO 通过组内候选响应之间的相对比较来估计优势，避免了对独立 Critic 网络的需求。其核心目标函数为：

$$ \mathcal{L}_{GRPO}(\theta) = -\mathbb{E}\left[ \frac{1}{G} \sum_{i=1}^G \left( \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)} \cdot A_i, \text{clip}\left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)}, 1-\epsilon, 1+\epsilon \right) \cdot A_i \right) - \beta \mathbb{D}_{KL}(\pi_\theta || \pi_{ref}) \right) \right] $$

其中组内优势 $A_i$ 经标准化处理：

$$ A_i = \frac{r_i - \mathrm{mean}(\{r_i\}_{i=1}^G)}{\mathrm{std}(\{r_i\}_{i=1}^G)} $$

KL 散度项采用无偏估计器：

$$ \mathbb{D}_{KL}(\pi_\theta || \pi_{ref}) = \frac{\pi_{ref}(o_i|q)}{\pi_\theta(o_i|q)} - \log \frac{\pi_{ref}(o_i|q)}{\pi_\theta(o_i|q)} - 1 $$

**物理接地奖励框架**

RL 阶段的关键创新在于设计了多维度物理接地奖励，替代传统单一的位置误差：

- **空间对齐奖励**：$r_{pos} = \frac{1}{N} \sum_{i=1}^{N} \left( (x^i - x_{gt}^i)^2 + (y^i - y_{gt}^i)^2 \right)$
- **转向角奖励**：$r_{ste} = \frac{1}{N} \sum_{j=1}^{N} \left( \theta^j - \theta_{gt}^j \right)^2$
- **速度奖励**：$r_{vel} = \frac{1}{N} \sum_{k=1}^{N} \left( v^k - v_{gt}^k \right)^2$
- **时间平滑奖励**：$r_{tem} = \frac{1}{N} \sum_{j=1}^{N} \left( \theta^{j} - \theta^{j-1} \right)^{2} + \frac{1}{N} \sum_{k=1}^{N} \left( v^{k} - v^{k-1} \right)^{2}$

综合准确度奖励为加权求和：

$$ r_{acc} = \lambda_{pos} \cdot r_{pos} + \lambda_{ste} \cdot r_{ste} + \lambda_{vel} \cdot r_{vel} + \lambda_{tem} \cdot r_{tem} $$

实验中所有权重均设为 1（消融实验证实均匀权重优于递减权重）。总奖励 $r_i = r_{acc}^i + r_{format}^i$，其中格式奖励确保模型输出符合预期结构。

**输入输出流**

模型输入为单帧前视图图像 $F$ 和历史车辆状态 $H$，输出为预测的 BEV 轨迹坐标 $\dot{T}$：

$$ \dot{T} = M(H, F) $$

轨迹规划被显式分解为四步推理过程，最终生成包含自验证的完整思维链，在推理质量与物理约束之间取得平衡。



### 两阶段训练流水线

AutoDrive-R² 采用“冷启动SFT + 物理接地RL”的两阶段训练框架，其核心模块如 **Figure 1** 所示：

1. **阶段一：监督微调（SFT）** — 使用自建的 nuScenesR²-6K 思维链数据集对基础 VLA 模型进行冷启动训练，使其习得结构化的四步推理能力与自反思验证机制。
2. **阶段二：强化学习（RL）** — 采用基于物理接地的多维度奖励函数，通过组相对策略优化（GRPO）对模型进行进一步优化，在保持推理质量的同时强制物理可行性约束。

---

### 四步思维链推理模块

模型将轨迹规划任务分解为四个递进式推理阶段，形成完整的自验证逻辑闭环：

| 步骤 | 模块名称 | 核心功能 |
|:---:|:---|:---|
| 1 | **图像分析（Image-Driven Analysis）** | 建立基础场景理解，包括障碍物检测、车道识别与交通参与者定位 |
| 2 | **物理计算（Physics-based Calculation）** | 利用运动学方程将视觉观测转化为量化的运动预测 |
| 3 | **逻辑推理（Contextual Logic Synthesis）** | 结合交通规则与领域知识进行安全检查与决策推理 |
| 4 | **自反思验证（Self-Reflection Validation）** | 反向检查推理链的一致性，识别并修正潜在的逻辑矛盾 |

该四步链的因果机制在于：前三个推理阶段（观察→计算→逻辑）提供了从感知到决策的完整前向推理路径，而第四阶段的自反思则充当了“内省式验证器”，使模型能够在输出最终轨迹前自主发现并纠正推理错误。消融实验（Table 4）表明，去除四步推理结构（w/o. Four.）使平均 L2 误差增加 31.5%，去除自反思（w/o. Self.）使误差增加 21.1%，证实了两者对于推理质量的关键作用。

---

### 物理接地奖励模块

RL 阶段的奖励函数由四个物理维度组成，共同构成对轨迹质量的多目标评估：

**空间对齐奖励（Spatial Alignment Reward）** — 衡量预测轨迹坐标与真值之间的欧氏距离：

$$r_{pos} = \frac{1}{N} \sum_{i=1}^{N} \left( (x^i - x_{gt}^i)^2 + (y^i - y_{gt}^i)^2 \right)$$

其中 $(x^i, y^i)$ 为第 $i$ 个预测航点的 BEV 坐标，$(x_{gt}^i, y_{gt}^i)$ 为对应真值坐标，$N$ 为预测航点数量。

**转向角奖励（Steering Angle Reward）** — 约束预测转向角与真值的一致性：

$$r_{ste} = \frac{1}{N} \sum_{j=1}^{N} \left( \theta^j - \theta_{gt}^j \right)^2$$

其中 $\theta^j$ 为第 $j$ 帧的预测转向角，$\theta_{gt}^j$ 为真值转向角。

**速度奖励（Velocity Reward）** — 约束预测速度与真值的偏差：

$$r_{vel} = \frac{1}{N} \sum_{k=1}^{N} \left( v^k - v_{gt}^k \right)^2$$

其中 $v^k$ 为第 $k$ 帧的预测速度，$v_{gt}^k$ 为真值速度。

**时间平滑奖励（Temporal Smoothness Reward）** — 惩罚连续控制信号的剧烈变化，确保轨迹的物理可行性与乘坐舒适性：

$$r_{tem} = \frac{1}{N} \sum_{j=1}^{N} \left( \theta^{j} - \theta^{j-1} \right)^{2} + \frac{1}{N} \sum_{k=1}^{N} \left( v^{k} - v^{k-1} \right)^{2}$$

该奖励的因果机制在于：通过惩罚相邻帧间转向角和速度的平方差，强制模型生成平滑的控制序列，避免物理上不可行的突变。消融实验（Table 4）显示，去除 $r_{tem}$ 导致平均 L2 误差增加 26.3%，而去除 $r_{pos}$ 则使误差剧增至 0.53m，表明空间对齐是奖励框架中最关键的组件。

**集成精度奖励（Integrated Accuracy Reward）** — 将上述四个维度加权求和：

$$r_{acc} = \lambda_{pos} \cdot r_{pos} + \lambda_{ste} \cdot r_{ste} + \lambda_{vel} \cdot r_{vel} + \lambda_{tem} \cdot r_{tem}$$

实验中所有权重系数 $\lambda$ 均设为 1。超参数消融（Table 5）证实，均匀权重 $(1,1,1,1)$ 优于递减权重 $(0.4, 0.3, 0.2, 0.1)$，后者使平均 L2 误差从 0.19m 升至 0.22m。

---

### GRPO 优化模块

RL 阶段采用组相对策略优化（GRPO），其核心优势在于通过组内候选响应的相对比较机制避免了传统 PPO 中价值网络（critic network）的引入。关键公式如下：

**优势归一化** — 对组内 $G$ 个候选响应的奖励进行标准化，获得相对优势：

$$A_i = \frac{r_i - \mathrm{mean}(\{r_i\}_{i=1}^G)}{\mathrm{std}(\{r_i\}_{i=1}^G)}$$

其中 $r_i = r_{acc}^i + r_{format}^i$ 为第 $i$ 个响应的总奖励（精度奖励 + 格式奖励）。

**GRPO 损失函数** — 带裁剪重要性采样与 KL 惩罚的策略优化目标：

$$\mathcal{L}_{GRPO}(\theta) = -\mathbb{E}[q \sim P(Q), \{o_i\}_{i=1}^G \pi_{\theta_{old}}(O|q)] \frac{1}{G} \sum_{i=1}^G \left( \min\left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)} \cdot A_i, \text{clip}\left( \frac{\pi_\theta(o_i|q)}{\pi_{\theta_{old}}(o_i|q)}, 1-\epsilon, 1+\epsilon \right) \cdot A_i \right) - \beta \mathbb{D}_{KL}(\pi_\theta || \pi_{ref}) \right)$$

其中 $\pi_\theta$ 和 $\pi_{\theta_{old}}$ 分别为当前策略与旧策略，$\epsilon$ 为裁剪范围，$\beta$ 为 KL 惩罚系数。

**KL 散度估计器** — 用于正则化的无偏估计：

$$\mathbb{D}_{KL}(\pi_\theta || \pi_{ref}) = \frac{\pi_{ref}(o_i|q)}{\pi_\theta(o_i|q)} - \log \frac{\pi_{ref}(o_i|q)}{\pi_\theta(o_i|q)} - 1$$

超参数消融（Table 5）确定最优配置为：生成数量 $G=6$（增至 8 无额外收益），KL 系数 $\beta=0.04$（相比 0.02 和 0.06 取得最低平均 L2 误差 0.19m）。

---

### 物理约束公式（附录参考）

论文在附录中提供了车辆动力学约束的物理基础公式，用于支撑奖励设计的合理性：

**最小转弯半径**：

$$R_{min} = \frac{L}{\sin(\delta_{max})}$$

其中 $L$ 为车辆轴距，$\delta_{max}$ 为最大转向角。

**横向加速度限制**（防侧滑约束）：

$$a_c = \frac{v^2}{R} \leq \mu g$$

其中 $v$ 为车速，$R$ 为转弯半径，$\mu$ 为路面摩擦系数，$g$ 为重力加速度。

**加加速度定义**（舒适性约束）：

$$j(t) = \frac{d a(t)}{d t}$$

**悬架动力学模型**：

$$m \ddot{x} + c \dot{x} + k x = F(t)$$

其中 $m$ 为质量，$c$ 为阻尼系数，$k$ 为弹簧刚度，$F(t)$ 为外部激励力。

> **注意**：上述物理约束公式来自论文附录，主要用于论证奖励函数设计的物理合理性，并非直接参与模型训练或推理的计算模块。



## 实验与关键发现

### 主实验结果

#### nuScenes 开环轨迹预测

Table 1 报告了 nuScenes 数据集上的轨迹 L2 误差与碰撞率对比。AutoDrive‑R² 7B 在平均 L2 误差上达到 **0.19 m**，相比此前最强的专用驾驶模型 **EMMA+**（Hwang et al., 2024）的 0.29 m 降低了 **34.5%**。在 1 s、2 s、3 s 三个预测时域上，L2 误差分别为 0.11 m、0.24 m、0.30 m，均显著优于所有对比方法。碰撞率方面，AutoDrive‑R² 7B 的平均碰撞率仅为 0.19%，比 EMMA+ 的 0.27% 低约 30%。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_KVWaCzJrrq/figures/003_Table_1.jpg]]
*Table 1: Trajectory L2 errors and collision rates on the nuScenes dataset*

值得注意的是，这一性能优势是在**极小的训练数据规模**下取得的——AutoDrive‑R² 仅使用 6k 样本进行 SFT，而 EMMA+ 使用了约 103k 样本的内部数据集。通用 VLM 基线 **Qwen2.5‑VL‑7B**（Bai et al., 2025）的平均 L2 误差高达 1.45 m，进一步凸显了结构化推理与物理奖励训练的有效性。

#### Waymo 零样本泛化

Table 2 展示了在 Waymo 数据集上的零样本评估结果。AutoDrive‑R² 7B 在未接触任何 Waymo 训练数据的情况下，取得平均 L2 误差 **0.19 m**，相比 EMMA+ 的 0.30 m 降低 **36.7%**，相比 Qwen2.5‑VL‑7B 的 2.05 m 降低 **90.7%**。这一结果验证了四步思维链推理结构与物理奖励框架的跨域泛化能力——模型习得的是可迁移的推理范式，而非对特定数据分布的过拟合。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_KVWaCzJrrq/figures/004_Table_2.jpg]]
*Table 2: Trajectory L2 errors on Waymo*

#### NAVSIM 闭环评估

Table 3 报告了 NAVSIM 闭环基准上的性能。AutoDrive‑R² 7B 在综合指标 PDMS 上达到 **90.3**，超过此前最优的 **Para‑Drive**（84.0）**+6.3 分**。在导航完成率（NC 98.5）、驾驶准确性（DAC 95.9）、时间违规（TTC 95.4）、舒适度（Comfort 100）和 ego‑progress（EP 82.7）等子指标上均取得最优或接近最优的结果。闭环评估中的高舒适度得分（100）直接验证了物理奖励中时间平滑项 $r_{tem}$ 的有效性。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_KVWaCzJrrq/figures/006_Table_3.jpg]]
*Table 3: Performance on the Closed-loop NAVSIM*

#### 定性分析

Figure 2 和 Figure 3 展示了 nuScenes 上 12 个场景的轨迹规划定性对比。AutoDrive‑R² 的预测轨迹（蓝线）与真值（绿线）高度重合，尤其在弯道和交叉口场景下，相比 Qwen2.5‑VL‑7B 和 EMMA+ 的偏差显著更小。Figure 4 和 Figure 5 展示了“Aha Moment”自反思案例：模型在推理过程中主动识别并修正了初始预测中的物理矛盾，例如检测到预测轨迹超出最小转弯半径约束后进行了重新规划。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_KVWaCzJrrq/figures/005_Figure_2.jpg]]
*Figure 2: Qualitative comparison of trajectory planning performance across Qwen2.5-VL-7B, EMMA+, and our AutoDrive-R² on the nuScenes dataset. Note that blue lines denote predicted trajectories while green lines represent ground truth trajectories*

### 消融实验

Table 4 通过系统性地移除各组件，量化了每个设计选择的贡献。

![[assets/figures/papers/paper_list_l30_https_openreview_net_forum_id_KVWaCzJrrq/figures/007_Table_4.jpg]]
*Table 4: Ablation studies of trajectory L2 errors on nuScenes dataset for validation*

#### 两阶段训练的必要性

仅进行 RL 训练而不进行 SFT 冷启动（7B + RL），平均 L2 误差为 0.33 m，相比完整两阶段训练的 0.19 m 升高 **22.2%**。这表明 nuScenesR²‑6K 数据集提供的结构化推理先验对后续 RL 优化至关重要——RL 阶段主要负责在物理约束下精调推理质量，而非从零学习推理模式。

#### 四步推理结构与自反思

移除四步推理结构（w/o. Four.）后，平均 L2 误差从 0.19 m 升至 0.25 m，**退化 31.5%**。去除自反思阶段（w/o. Self.）导致误差升至 0.23 m，**退化 21.1%**。两个结果共同说明：分阶段的推理链（观察→计算→逻辑→反思）为模型提供了可验证的认知结构，其中自反思步骤充当了推理质量的“内部验证器”。

#### 物理奖励各分量的贡献

- 移除空间对齐奖励 $r_{pos}$ 后，误差剧增至 **0.53 m**，表明位置精度是物理奖励的基石。
- 移除转向角奖励 $r_{ste}$ 后，误差升至 0.24 m（**+26.3%**）。
- 移除速度一致性奖励 $r_{vel}$ 后，误差升至 0.23 m（**+21.1%**）。
- 移除时间平滑奖励 $r_{tem}$ 后，误差升至 0.24 m（**+26.3%**），且附录 C 的定性结果显示轨迹出现明显抖动。

四个分量的独立移除均导致显著性能下降，验证了多维度物理约束的互补性——空间对齐保证精度，动力学约束保证物理可行性，时间平滑保证舒适性。

### 超参数分析

Table 5 对三个关键超参数进行了消融：

- **奖励权重**：均匀权重 $\lambda = (1,1,1,1)$ 的平均 L2 误差为 0.19 m，优于递减权重 $(0.4,0.3,0.2,0.1)$ 的 0.22 m。这表明四个物理约束维度同等重要，不应人为区分优先级。
- **KL 散度系数**：$\beta = 0.04$ 取得最优结果。$\beta = 0.02$ 时误差升至 0.21 m（策略更新过于激进），$\beta = 0.06$ 时误差为 0.20 m（约束过强限制优化）。
- **生成候选数**：$G = 6$ 和 $G = 8$ 均达到 0.19 m，显著优于 $G = 4$ 的 0.23 m。选择 $G = 6$ 以平衡性能与计算开销。

### 局限与失败模式

尽管性能优异，AutoDrive‑R² 存在以下已知局限：

1. **单帧前视输入**：模型仅使用单帧前视图图像，未利用多视角和时序信息，在遮挡场景或需要长时推理的情况下可能失效。
2. **训练数据覆盖不足**：nuScenesR²‑6K 仅包含 6k 样本，难以覆盖全部边缘场景（如极端天气、罕见交通参与者行为）。
3. **物理奖励的经验性**：奖励权重和超参数基于经验设定，未经过系统化的跨平台验证，可能不适用于不同动力学特性的车辆。
4. **闭环评估限于仿真**：未在真实车辆上部署测试，NAVSIM 闭环结果虽好，但仿真到现实的迁移差距尚未量化。

### 关键图表结论摘要

| 图表 | 核心结论 |
|------|---------|
| Table 1 | AutoDrive‑R² 7B 在 nuScenes 上平均 L2 误差 0.19 m，比 EMMA+ 低 34.5% |
| Table 2 | Waymo 零样本平均 L2 误差 0.19 m，比 Qwen2.5‑VL‑7B 低 90.7% |
| Table 3 | NAVSIM 闭环 PDMS 90.3，超过 Para‑Drive 6.3 分 |
| Table 4 | 去除自反思 +21.1%，去除 $r_{tem}$ +26.3%，去除 $r_{pos}$ 导致误差暴涨 |
| Table 5 | 均匀奖励权重和 $\beta = 0.04$ 为最优配置 |
| Figure 2/3 | 定性轨迹在弯道和交叉口场景显著优于基线 |
| Figure 4/5 | 自反思机制触发“Aha Moment”，主动修正物理不可行预测 |



## 定位与知识库关联

### 1. 技术路线定位

AutoDrive-R² 处于**视觉-语言-行动（VLA）大模型**与**自动驾驶轨迹规划**的交叉地带，其核心贡献在于首次将**结构化自反思推理**与**物理接地奖励**系统性地引入 VLA 驾驶模型的两阶段训练流程中。

从方法谱系看，现有自动驾驶模型可大致分为三类：

- **训练驱动的驾驶专家模型**：如 **UniAD** (Hu et al., 2023)、**VAD** (Jiang et al., 2023)、**BEV-Planner** (Li et al., 2024)、**Ego-MLP** (Zhai et al., 2023)。这类方法依赖大规模标注数据进行端到端训练，在特定场景下表现优异，但缺乏可解释的推理过程，且泛化能力受限于训练数据分布。

- **专用驾驶大模型**：如 **DriveVLM** (Tian et al., 2024)、**OmniDrive** (Wang et al., 2024)、**EMMA+** (Hwang et al., 2024)。这类方法将视觉语言模型引入驾驶决策，尝试利用预训练知识进行场景理解，但推理过程通常为直接预测或简单提示引导，缺乏结构化的自验证机制和物理可行性约束。

- **通用视觉语言模型**：如 **Qwen-2.5-VL-7B** (Bai et al., 2025)。这类模型具备强大的视觉理解和语言生成能力，但未针对自动驾驶的物理约束和轨迹规划进行专门优化，直接应用于驾驶任务时误差显著。

AutoDrive-R² 的创新在于填补了上述范式的关键空白：它既保留了 VLA 模型的推理灵活性，又通过**四步思维链（观察→计算→逻辑→自反思）** 赋予模型结构化推理能力，同时以**GRPO 强化学习**和**物理接地奖励**确保输出轨迹的物理可行性。

### 2. 关键改进槽位

相较于基线方法，AutoDrive-R² 在三个核心槽位上进行了实质性改进：

| 改进槽位 | 基线做法 | AutoDrive-R² 做法 | 证据锚点 |
|---------|---------|------------------|---------|
| **训练策略** | 单阶段微调或直接 RL | 两阶段：SFT（nuScenesR²-6K CoT 数据集）+ GRPO RL（物理接地奖励） | Section 2, Figure 1 |
| **推理过程** | 直接轨迹预测或简单提示推理 | 四步思维链（观察→计算→逻辑→自反思）含自验证 | Section 2.1 |
| **奖励函数** | 简单位置误差（L2）或任务特定惩罚 | 物理接地奖励：空间对齐 + 转向动力学 + 速度一致性 + 时间平滑性 | Section 2.3, Eq. 4-8 |

其中，**自反思（Self-Reflection）** 是推理质量的核心保障——消融实验表明，去除自反思使平均 L2 误差增加 21.1%（Table 4, w/o. Self.）。**时间平滑奖励（r_tem）** 是物理可行性的关键——去除该项导致误差增加 26.3%（Table 4, RL: w/o. r_tem）。

### 3. 适用边界与局限

尽管 AutoDrive-R² 在多个基准上取得了显著提升，其适用边界和局限性同样明确：

**数据与感知层面**：
- 模型仅使用**单帧前视图图像**作为输入，未充分利用多视角环视和时序信息。这意味着在遮挡严重或需要跨视角推理的场景中，模型可能缺乏足够的感知冗余。
- 训练数据规模较小（**仅 6k 样本**），而对比方法 EMMA+ 使用了约 103k 样本的内部数据集。尽管在公平性上 AutoDrive-R² 以更少数据取得了更好效果，但小样本训练可能使其无法充分覆盖长尾边缘场景。

**物理建模层面**：
- 物理奖励的权重（λ_pos, λ_ste, λ_vel, λ_tem）基于**经验设置**（实验中均设为 1），且消融显示均匀权重优于递减权重（Table 5）。但这一配置可能不适用于所有车辆平台，尤其是动力学特性差异显著的车型（如大型卡车与小型乘用车）。
- 物理约束（最小转弯半径 Eq. 9、侧向加速度限制 Eq. 10、加加速度 Eq. 11）虽在方法论中被提及，但**未在奖励函数中显式硬编码**，而是通过时间平滑奖励间接实现。对于极端动力学场景，这种软约束可能不足以防止物理不可行轨迹的生成。

**部署与验证层面**：
- 所有评估均在**离线数据集**（nuScenes、Waymo）和**模拟器**（NAVSIM）上进行，**未在真实车辆上部署和测试**。闭环评估虽能反映一定的交互能力，但模拟器与真实世界在传感器噪声、延迟、动态障碍物行为等方面仍存在差距。
- 零样本能力仅在 Waymo 上验证，对于更具挑战性的非结构化环境（如乡村土路、施工区域、极端天气），模型的泛化能力尚不明确。

### 4. 开放问题

基于当前工作的边界，以下几个方向值得关注：

1. **多智能体交互与协同决策**：当前自反思推理仅针对自车轨迹规划。如何将推理链扩展到多智能体场景，使模型能够预测他车意图并进行协同决策，是提升复杂交互场景安全性的关键。

2. **实时传感器融合与在线适应**：模型目前依赖离线训练，无法利用实时传感器数据动态调整推理。融合时序多帧信息并引入在线学习机制，有望提升模型对动态环境的适应能力。

3. **非结构化环境的泛化**：在缺乏清晰车道线和交通规则的非结构化环境中，当前依赖“逻辑推理”模块的框架可能失效。如何使模型在规则稀疏的场景中仍能生成安全轨迹，是一个重要的开放挑战。

4. **物理约束的显式集成**：将运动学/动力学约束直接嵌入推理过程或作为硬约束，而非仅通过奖励函数间接引导，可能进一步提升轨迹的物理可行性保证。



## 原文 PDF

![[paperPDFs/ICLR_2026/AutoDrive_R²_Incentivizing_Reasoning_and_Self_Reflection_Capacity_for_VLA_Model_in_Autonomous_Driving.pdf]]
