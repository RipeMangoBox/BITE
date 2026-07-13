---
title: "WMPO: World Model-based Policy Optimization for Vision-Language-Action Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/WMPO_World_Model_based_Policy_Optimization_for_Vision_Language_Action_Models.pdf
project_link: https://wm-po.github.io/
code_link: null
openreview_forum_id: qE2FyvRvuF
aliases:
- WWMBPO
- WMPO
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/deep_rl
core_operator: "通过学得的像素空间视频生成世界模型替代真实环境，实现完全在想象中进行的高效在线策略优化，消除了对物理交互的依赖。"
primary_logic: "利用大量机器人轨迹预训练的像素级视频生成世界模型，通过策略行为对齐、噪声帧条件和帧级动作控制确保长时域忠实模拟，并结合稀疏奖励模型与组相对策略优化（GRPO），首次验证了基于世界模型的VLA RL可行性，显著提升样本效率并涌现自我纠错行为。"
claims:
- "WMPO在Mimicgen仿真四个操作任务中，以128条真实轨迹预算，平均成功率47.1%，显著优于所有基线（DPO 37.3%，GRPO 38.0%），展现出超强样本效率。"
- "WMPO训练的策略展现出演示数据中不存在的自我纠错行为，且成功轨迹更短、更流畅。"
- "WMPO在多种分布外扰动下保持强大泛化能力，平均成功率显著高于离线RL方法。"
- "WMPO支持终身学习，通过交替更新策略和世界模型实现稳定且显著的持续性能提升，而DPO无法迭代改善。"
---

# WMPO: World Model-based Policy Optimization for Vision-Language-Action Models

> [!tip] 核心洞察
> 利用大量机器人轨迹预训练的像素级视频生成世界模型，通过策略行为对齐、噪声帧条件和帧级动作控制确保长时域忠实模拟，并结合稀疏奖励模型与组相对策略优化（GRPO），首次验证了基于世界模型的VLA RL可行性，显著提升样本效率并涌现自我纠错行为。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | WMPO：基于世界模型的视觉-语言-动作策略优化 |
| 英文题名 | WMPO: World Model-based Policy Optimization for Vision-Language-Action Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=qE2FyvRvuF) · [Project](https://wm-po.github.io/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/deep_rl |
| Method | WMPO (World Model-based Policy Optimization) |
| Dataset | Mimicgen (Coffee, StackThree, ThreePieceAssembly, Square), Disruption Scenarios (Position, Background, Texture), Real-world Square insertion (5mm clearance) |

> [!tip] 效果简介
> - Mimicgen (Coffee, StackThree, ThreePieceAssembly, Square) 上，Success rate (%) 为 47.1 (P=128 mean)，对比 37.3 (DPO), 38.0 (GRPO)，变化 +9.8 over DPO, +9.1 over GRPO。
> - Mimicgen (Coffee, StackThree, ThreePieceAssembly, Square) 上，Success rate (%) 为 57.6 (P=1280 mean)，对比 42.4 (DPO), 43.5 (GRPO)，变化 +15.2 over DPO, +14.1 over GRPO。
> - Disruption Scenarios (Position, Background, Texture) 上，Success rate (%) mean across disruption types 为 29.6 (Ours)，对比 24.2 (DPO), 26.3 (GRPO), 26.7 (Base)，变化 +5.4 over DPO, +3.3 over GRPO, +2.9 over Base。

## 概要

将强化学习应用于视觉-语言-动作（VLA）模型时，面临两大核心瓶颈：**物理交互样本效率极低**——真实机器人轨迹采集成本高昂，难以支撑在线策略优化所需的大量试错；**离策略价值估计偏差**——离线RL方法（如DPO）虽能利用已有数据，但受限于分布偏移，无法有效探索和纠错。

WMPO（World Model-based Policy Optimization）通过一个关键因果调节变量解决了上述瓶颈：**以学得的像素空间视频生成世界模型替代真实环境**，将VLA的策略优化完全置于“想象”中进行。其核心洞察在于：利用大规模机器人轨迹预训练的像素级世界模型，配合策略行为对齐、噪声帧条件与帧级动作控制三项技术，实现长时域忠实模拟；在此基础上，结合稀疏奖励模型与组相对策略优化（GRPO），首次验证了基于世界模型的VLA在线RL可行性。

**主要结论：**

- **超强样本效率**：在Mimicgen仿真四个操作任务中，仅使用128条真实轨迹预算，WMPO平均成功率达47.1%，显著优于DPO（37.3%）和GRPO（38.0%）；当预算扩展至1280条时，优势进一步扩大（57.6% vs. 42.4%/43.5%）。
- **涌现自我纠错**：WMPO训练的策略展现出演示数据中不存在的自我纠错行为，成功轨迹更短、更流畅。
- **鲁棒泛化**：在位置、背景、纹理等多种分布外扰动下，WMPO平均成功率（29.6%）显著高于离线RL方法（DPO 24.2%）。
- **终身学习能力**：通过交替更新策略与世界模型，WMPO实现稳定且持续的迭代提升，而DPO无法从迭代中获益。
- **真实世界验证**：在5mm间隙的精细插入任务中，WMPO成功率（70%）优于基策略（53%）和DPO（60%）。

WMPO为VLA模型提供了一条无需昂贵物理交互、样本高效且具备自我纠错能力的策略优化路径，其像素空间世界模型的设计使其可直接复用VLA的预训练视觉知识，避免潜在空间转换带来的信息损失。



### 问题背景：VLA策略优化的两难困境

视觉-语言-动作（VLA）模型通过在互联网规模的视觉-语言数据和大规模机器人轨迹上预训练，展现出强大的视觉理解和任务泛化能力。然而，VLA策略的优化范式长期面临一个根本性的两难选择：

**模仿学习**是当前VLA训练的主流范式——通过行为克隆从人类演示数据中学习策略。这种方法虽然训练稳定、实现简单，但存在本质局限：策略只能复现演示中的行为，无法从失败中学习，缺乏自我纠错能力。当面对演示数据未覆盖的状态时，策略容易陷入不可恢复的错误。

**真实环境强化学习（RL）**则试图通过与物理世界直接交互来优化策略。理论上，RL允许策略通过试错探索更优的行为模式。但在VLA场景下，这一路径面临两个核心瓶颈：**物理交互的样本效率极低**——每次策略更新都需要大量真实环境采样，对于精细操作任务而言，收集数千条真实轨迹的成本高得令人望而却步；**离策略价值估计偏差**——直接使用历史数据优化当前策略时，价值函数的估计偏差会严重损害训练稳定性。

### 现有方法的缺口

近期工作尝试将RL引入VLA微调，但均未根本解决上述矛盾：

- **DPO**（Direct Preference Optimization, Rafailov et al., 2023）采用离线偏好优化，完全依赖预收集的真实轨迹对，避免了在线采样，但无法主动探索新行为，策略提升受限于离线数据的覆盖范围。
- **GRPO**（Group Relative Policy Optimization, Shao et al., 2024）通过组相对优势实现在线策略优化，但仍需在真实环境中执行大量采样，样本效率问题未得到缓解。

更深层的问题在于：现有世界模型方法（如基于RSSM的潜在状态世界模型）通常在抽象潜在空间中操作，与VLA预训练获得的丰富视觉表征存在**模态错配**，无法直接利用VLA已有的视觉知识，导致模拟保真度不足。

### 核心动机：在想象中完成策略优化

WMPO的核心动机源于一个关键洞察：**如果能够构建一个足够忠实的世界模型，完全替代真实环境进行策略优化，就能同时获得RL的探索能力和模仿学习的样本效率**。

具体而言，这一思路需要解决三个层次的挑战：

1. **世界模型的保真度**：如何在像素空间而非潜在空间中生成长时域、动作条件化的视频预测，使其与VLA的视觉表征空间对齐？
2. **策略行为对齐**：如何让世界模型准确反映当前策略的行为模式，特别是其失败模式，从而避免模拟-现实鸿沟？
3. **稀疏奖励下的高效优化**：在完全想象的轨迹上，如何仅凭任务成功/失败的二元信号驱动有效的策略更新？

WMPO通过三个技术支柱回应这些挑战：基于大规模机器人轨迹预训练的**像素空间视频扩散世界模型**，在少量策略自身行为数据上微调的**策略行为对齐机制**，以及结合稀疏奖励模型与**组相对策略优化（GRPO）**的完全想象内在线策略优化框架。这一设计使VLA策略得以在零物理交互的条件下，从大规模想象的试错经验中涌现出演示数据中不存在的自我纠错行为。



## 核心方法与创新机理

WMPO 针对将强化学习应用于视觉-语言-动作（VLA）模型时面临的两大瓶颈——物理交互样本效率极低和离策略价值估计偏差——提出了一套系统性的解决方案。其核心创新并非单一技术的堆砌，而是围绕**像素空间世界模型**构建的完整在线策略优化闭环，使 VLA 的 RL 训练完全脱离真实环境交互。

### 从潜在空间到像素空间的世界模型范式转换

传统基于模型的方法（如 RSSM 体系）在抽象潜在空间中运行世界模型，与 VLA 预训练时使用的视觉特征空间存在根本性错配，导致预训练知识难以有效迁移。WMPO 的关键决策是**直接在像素空间操作**：基于 OpenSora 视频扩散主干构建世界模型，并将 3D VAE 替换为 SDXL 的 2D VAE，使世界模型的视觉表示与 VLA 策略的预训练视觉知识天然对齐。这一架构选择消除了潜在空间转换带来的信息损失，为后续的想象中策略优化奠定了保真度基础。

### 三项关键技术保障长时域模拟的忠实性

像素空间视频生成面临的核心挑战是在长时域自回归生成中维持视觉质量和动作-帧对齐。WMPO 引入了三项针对性技术：

**噪声帧条件训练**是维持生成稳定性的关键机制。传统方法使用干净帧作为条件进行自回归生成，预测误差会逐步累积导致质量崩溃。WMPO 在训练时对条件帧施加扩散早期时间步（timestep 50）的轻微噪声扰动，迫使模型学会从非完美条件中恢复，从而在实际推理时对累积误差具有鲁棒性。消融实验表明，去除该技术会导致长时域生成质量急剧下降。

**帧级动作控制**解决了全局动作条件（如交叉注意力或简单拼接）带来的动作-帧对齐问题。WMPO 扩展了 AdaLN 模块，通过 MLP 为每个 transformer 层的每一帧生成动作特定的缩放和偏移参数，实现精细的帧级调制：

$$\mathbf{x}^i = \mathbf{x}^i + (1 + \alpha_1^i) \cdot \mathrm{Block} \Big( \gamma_1^i \cdot \mathrm{LayerNorm}(\mathbf{x}^i) + \beta_1^i \Big)$$

**策略行为对齐**是弥合模拟-现实差距的核心机制。世界模型在通用机器人轨迹上预训练后，其状态-动作分布与当前策略存在偏差。WMPO 使用策略自身收集的少量真实 rollout 轨迹对世界模型进行微调，使其适应下游分布并忠实捕捉失败模式。这一过程成本可控，却是确保想象轨迹对策略优化具有指导价值的前提。

### 想象空间内的在线策略优化

在优化算法层面，WMPO 采用**组相对策略优化（GRPO）**在想象空间中执行完全的在线策略优化，并做了两项关键调整：

1. **移除 KL 散度正则化**：传统 RL 微调通常保留 KL 惩罚以防止策略偏离预训练分布过远，但这会抑制探索。WMPO 去除 KL 项，配合动态采样策略鼓励策略探索演示数据中不存在的新行为——这正是涌现自我纠错能力的算法基础。

2. **稀疏奖励模型**：WMPO 训练一个轻量级奖励模型（VideoMAE 编码器 + 线性头），在真实轨迹上以二分类交叉熵损失训练，预测完整想象轨迹的任务成功与否。该模型在四个任务上 F1 分数均超过 0.95，为 GRPO 提供了可靠的稀疏奖励信号，避免了手工设计密集奖励函数的 reward hacking 风险。

整体的优化目标是在学得世界模型下最大化想象轨迹的期望累积回报：

$$\operatorname*{max}_{\theta} \mathbb{E}_{\tau \sim \pi_{\theta}, p_{\phi}} \left[ R_{\psi}(\tau) \right]$$

其中世界模型根据过去 $c$ 帧观察和预测的动作片段生成未来 $K$ 帧：

$$I_{i:i+K} \sim p_{\phi}(I_{i-c:i}, a_{i:i+K})$$

策略更新使用 GRPO 的裁剪替代目标，以组内归一化优势替代传统价值函数：

$$r_{i,t}(\theta) = \frac{\pi_{\theta}(a_{i,t} \mid s_{i,t})}{\pi_{\theta_{\mathrm{old}}}(a_{i,t} \mid s_{i,t})}, \qquad \hat{A}_i = \frac{R_i - \mathrm{mean}(\{R_i\}_{i=1}^{G})}{\mathrm{std}(\{R_i\}_{i=1}^{G})}$$

### 创新点的协同效应

上述创新并非孤立存在，而是形成了正向反馈循环：像素空间世界模型使 VLA 的预训练知识得以保留，噪声帧条件和帧级动作控制保障了想象轨迹的视觉质量，策略行为对齐确保想象内容与当前策略相关，而去除 KL 正则的 GRPO 则充分利用这些高质量想象轨迹探索新行为。这一协同效应在实验中体现为 WMPO 策略涌现出的自我纠错能力——这是演示数据中不存在的行为，也是纯模仿学习或离线 RL 方法无法获得的。



![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_qE2FyvRvuF/figures/002_Figure_2.jpg]]
*Figure 2: WMPO starts from an initial state $s _ { 0 }$ . The overall training procedure consists of three components: (1) Imagined Trajectory Generation, where policy model $\pi _ { \theta _ { \mathrm { o l d } } }$ and world model $p _ { \phi }$ interact alternately to generate a full imagined trajectory; (2) Trajectory Sampling, where multiple trajectories are sampled and evaluated by the reward model $R _ { \psi }$ ; and (3) Policy Update, where the policy parameters θ are optimized via Eq. 4. This process is iteratively repeated throughout training

WMPO 的核心思路是将 VLA 策略的在线强化学习完全迁移到学得的像素空间世界模型中，从而摆脱对真实物理交互的依赖。整个训练流程由三个交替执行的模块构成：**想象轨迹生成**、**轨迹采样**和**策略更新**。

### 问题形式化

WMPO 将 VLA 操作任务建模为一个马尔可夫决策过程（MDP）$\mathcal{M} = (\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R})$。其中状态空间 $\mathcal{S} = \mathcal{I} \times \mathcal{G}$ 由图像观测空间 $\mathcal{I}$ 和语言指令空间 $\mathcal{G}$ 的笛卡尔积构成；动作空间 $\mathcal{A}$ 为 VLA 模型输出的动作分箱空间；转移函数 $\mathcal{P}$ 和奖励函数 $\mathcal{R}$ 在 WMPO 中分别由学得的世界模型 $p_\phi$ 和奖励模型 $R_\psi$ 近似替代。

在此设定下，策略优化的目标被重新表述为在世界模型内部最大化想象轨迹的期望累积回报：

$$\max_{\theta} \mathbb{E}_{\tau \sim \pi_{\theta}, p_{\phi}} \left[ R_{\psi}(\tau) \right]$$

其中 $\pi_\theta$ 为待优化的 VLA 策略，$p_\phi$ 为世界模型，$R_\psi$ 为奖励模型，$\tau$ 为一条完整的想象轨迹。

### 三大核心模块

**模块一：想象轨迹生成。** 该模块实现策略与世界模型的交替自回归交互。给定初始状态 $s_0$（包括初始 $m$ 帧图像观测和语言指令），当前策略 $\pi_{\theta_{\text{old}}}$ 预测一个长度为 $K$ 的动作片段；随后，世界模型 $p_\phi$ 以最近 $c$ 帧观测和该动作片段为条件，生成接下来的 $K$ 帧图像：

$$I_{i:i+K} \sim p_{\phi}(I_{i-c:i}, a_{i:i+K})$$

生成的新帧被拼接到观测序列中，作为下一步策略预测的输入。这一过程重复执行，直至生成一条完整的想象轨迹。

**模块二：轨迹采样。** 对每个初始状态，从当前策略和世界模型中采样一组共 $G$ 条想象轨迹。每条轨迹被送入奖励模型 $R_\psi$ 进行评估——该模型基于 VideoMAE 编码器加线性头实现，以二元交叉熵损失在真实轨迹上训练，输出轨迹成功与否的稀疏二元信号。随后，采用动态采样策略保证组内轨迹多样性，并计算组归一化优势函数：

$$\hat{A}_i = \frac{R_i - \text{mean}(\{R_i\}_{i=1}^{G})}{\text{std}(\{R_i\}_{i=1}^{G})}$$

**模块三：策略更新。** 基于采样的想象轨迹和归一化优势，使用 GRPO（Group Relative Policy Optimization）的裁剪替代目标更新策略参数 $\theta$。与标准 GRPO 不同，WMPO 移除了 KL 散度正则化项，以鼓励策略探索演示数据中不存在的新行为。更新目标为：

$$\mathcal{L}(\theta) = \mathbb{E}_{s_0 \sim \mathcal{D}, \{\tau_i\}_{i=1}^{G} \sim \pi_{\theta_{\text{old}}}} \left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{T} \sum_{t=0}^{T} \min \left( r_{i,t}(\theta) \hat{A}_i, \; \text{clip} \left( r_{i,t}(\theta), 1-\epsilon_{\text{low}}, 1+\epsilon_{\text{high}} \right) \hat{A}_i \right) \right]$$

其中概率比 $r_{i,t}(\theta) = \frac{\pi_{\theta}(a_{i,t} \mid s_{i,t})}{\pi_{\theta_{\text{old}}}(a_{i,t} \mid s_{i,t})}$，参考对数概率由旧策略预先计算并缓存。

### 策略行为对齐

为缓解世界模型与当前策略之间的状态-动作分布漂移，WMPO 引入策略行为对齐机制：定期使用当前策略在真实环境中收集少量轨迹，对世界模型进行微调。这一步骤使世界模型能够适应下游分布并忠实捕捉策略的失败模式，是维持想象轨迹可信度的关键环节。

整个训练流程（Figure 2）以迭代方式执行：策略在想象中更新后，其行为数据被用于微调世界模型，更新后的世界模型再为下一轮策略优化提供更准确的想象环境，形成闭环。



### 问题形式化

WMPO将VLA操作任务建模为马尔可夫决策过程 $M = (\mathcal{S}, \mathcal{A}, P, R)$。状态空间 $\mathcal{S} = \mathcal{I} \times \mathcal{G}$，其中 $\mathcal{I}$ 为图像观测空间，$\mathcal{G}$ 为语言指令空间；动作空间 $\mathcal{A}$ 为动作分箱后的离散空间（分箱为256 bins）。优化目标为最大化在学得世界模型 $p_\phi$ 下想象轨迹的期望累积回报：

$$\operatorname*{max}_{\theta} \mathbb{E}_{\tau \sim \pi_{\theta}, p_{\phi}} \left[ R_{\psi}(\tau) \right] \tag{1}$$

其中 $\pi_\theta$ 为待优化的VLA策略，$R_\psi$ 为学得的奖励模型。

### 想象轨迹生成

WMPO的核心创新在于将策略优化完全置于像素空间视频生成世界模型内。给定初始状态 $s_0$，旧策略 $\pi_{\theta_{\text{old}}}$ 与世界模型 $p_\phi$ 交替交互生成完整轨迹。具体而言，策略接收最近 $m$ 帧图像和语言指令，预测动作片段 $a_{i:i+K}$；世界模型则以最近 $c$ 帧观测和预测的动作片段为条件，生成接下来 $K$ 帧图像：

$$I_{i:i+K} \sim p_{\phi}(I_{i-c:i}, a_{i:i+K}) \tag{2}$$

这一自回归过程持续进行，直至生成完整的想象轨迹。

### 世界模型架构与关键设计

世界模型基于OpenSora视频扩散骨干，并进行了三项关键改造以适配VLA策略优化：

**像素空间操作**。与基于RSSM的潜空间世界模型不同，WMPO直接操作像素空间，采用SDXL的2D VAE替代OpenSora的3D VAE，从而能直接利用VLA预训练的视觉知识，消除潜空间与视觉特征空间的失配。

**噪声帧条件训练**。为缓解长时域自回归生成中的误差累积，WMPO在训练时对条件帧施加轻微扩散噪声（对应早期timestep 50），而非使用干净帧。这提升了世界模型对不完美条件输入的鲁棒性，是实现稳定长时域生成的关键。

**帧级动作控制**。WMPO扩展了AdaLN模块，在每帧对transformer层注入动作特定的缩放和偏移参数。对于第 $i$ 帧的特征表示，更新规则为：

$$\mathbf{x}^i = \mathbf{x}^i + (1 + \alpha_1^i) \cdot \mathrm{Block} \Big( \gamma_1^i \cdot \mathrm{LayerNorm}(\mathbf{x}^i) + \beta_1^i \Big)$$

其中 $\alpha_1^i, \gamma_1^i, \beta_1^i$ 由MLP根据动作信号和扩散时间步嵌入生成。该设计确保动作信号与对应帧精确对齐，避免全局动作条件导致的动作-帧失配。

### 策略行为对齐

为缓解世界模型与目标策略之间的状态-动作分布偏移，WMPO引入策略行为对齐：在每轮策略优化前，使用当前策略采集的少量真实轨迹对世界模型进行微调，使其适应下游分布并更忠实地捕捉失败模式。

### 奖励模型

奖励模型采用VideoMAE编码器加线性头，在真实轨迹上以二元交叉熵损失训练，用于预测想象轨迹的二元成功/失败。若轨迹中任一片段的预测分数超过阈值 $\tau_{\text{thr}}$，则整条轨迹被判定为成功。该模型在所有任务上F1分数均高于0.95，为策略优化提供可靠的稀疏奖励信号。

### 轨迹采样与策略更新

对每个初始状态，从当前策略和世界模型采样一组 $G$ 条想象轨迹，由奖励模型评估成功与否。采用动态采样策略确保组内多样性，并计算组归一化优势：

$$r_{i,t}(\theta) = \frac{\pi_{\theta}(a_{i,t} \mid s_{i,t})}{\pi_{\theta_{\text{old}}}(a_{i,t} \mid s_{i,t})}, \qquad \hat{A}_i = \frac{R_i - \mathrm{mean}(\{R_i\}_{i=1}^{G})}{\mathrm{std}(\{R_i\}_{i=1}^{G})}$$

其中 $r_{i,t}(\theta)$ 为新旧策略的概率比，$\hat{A}_i$ 为组内归一化优势。旧策略下动作片段的对数概率作为GRPO更新的参考基线：

$$\log \pi_{\theta_{\text{old}}} (a_t \mid s_t) = \sum_{i=1}^{K} \sum_{j=1}^{D} \log \pi_{\theta_{\text{old}}} \left( a_t^{i,j} \mid s_t \right) \tag{3}$$

策略更新采用去除KL散度正则化的GRPO裁剪替代目标，鼓励策略探索新行为：

$$\mathcal{L}(\theta) = \mathbb{E}_{s_0 \sim \mathcal{D}, \{\tau_i\}_{i=1}^{G} \sim \pi_{\theta_{\text{old}}}} \left[ \frac{1}{G} \sum_{i=1}^{G} \frac{1}{T} \sum_{t=0}^{T} \min \left( r_{i,t}(\theta) \hat{A}_i, \; \mathrm{clip} \left( r_{i,t}(\theta), 1-\epsilon_{\text{low}}, 1+\epsilon_{\text{high}} \right) \hat{A}_i \right) \right] \tag{4}$$

去除KL正则化并采用动态采样策略，既降低了内存消耗，又使GRPO训练保持稳定。整个训练流程在想象轨迹生成、轨迹采样和策略更新三个模块间迭代循环。



## 实验与关键发现

### 核心瓶颈与解决路径

VLA模型的RL训练面临两个核心瓶颈：**物理交互样本效率极低**——真实环境中的试错成本高昂，且难以实现严格的在策略（on-policy）优化；**离策略价值估计偏差**——离线RL方法（如DPO）受限于静态偏好数据，无法有效探索新行为。WMPO通过一条因果路径解决这两个问题：**用学得的像素空间视频生成世界模型替代真实环境，实现完全在想象中进行的在线策略优化**，从而消除对物理交互的依赖。

这一路径的关键技术支撑包括：（1）基于OpenSora的视频扩散世界模型，直接操作像素空间以利用VLA的预训练视觉知识；（2）策略行为对齐（Policy Behavior Alignment），用少量策略自身采集的真实轨迹微调世界模型，缓解模拟-现实分布偏移；（3）噪声帧条件与帧级动作控制，确保长时域生成的稳定性；（4）稀疏奖励模型与去KL正则的GRPO优化，鼓励策略探索新行为。

### 主实验结果

**表1**展示了WMPO与两个RL基线（GRPO、DPO）在Mimicgen仿真基准四个精细操作任务上的对比结果。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_qE2FyvRvuF/figures/004_Table_1.jpg]]
*Table 1: Comparison of policy optimization methods across four manipulation tasks in the Mimicgen simulation benchmark. P denotes the rollout budget, i.e., the number of full real trajectories available for policy optimization. Results show that WMPO consistently outperforms both GRPO and DPO baselines under different budgets. As the rollout budget increases from 128 to 1280, WMPO continues to exhibit substantial improvements, highlighting both its data efficiency and scalability. Performance is reported as the task success rate (%)*

| 方法 | P=128 平均成功率 | P=1280 平均成功率 |
|------|-----------------|-------------------|
| DPO (Rafailov et al., 2023) | 37.3% | 42.4% |
| GRPO (Shao et al., 2024) | 38.0% | 43.5% |
| **WMPO (Ours)** | **47.1%** | **57.6%** |

在最低真实轨迹预算（P=128）下，WMPO以平均47.1%的成功率显著超越DPO（+9.8个百分点）和GRPO（+9.1个百分点），展现出超强样本效率。当预算扩大至P=1280时，WMPO的优势进一步扩大至+15.2（vs. DPO）和+14.1（vs. GRPO）个百分点，说明方法具有良好的可扩展性。在所有四个任务（Coffee、StackThree、ThreePieceAssembly、Square）上，WMPO在两个预算级别均保持最优，无任务反转。

### 涌现行为：自我纠错

**图3**展示了WMPO策略在Square任务上的行为分析。与基策略（模仿学习）相比，WMPO训练的策略展现出**演示数据中不存在的自我纠错能力**：当方块未能对准插入位置时，策略会主动调整末端执行器姿态，而非继续执行失败动作直至超时。这一涌现行为源于世界模型生成的大规模想象轨迹——策略在想象中经历失败并学会从中恢复，而纯模仿学习无法获得此类经验。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_qE2FyvRvuF/figures/003_Figure_3.jpg]]
*Figure 3: Behavior analysis of the Square task (inserting the square into the stick) shows that, compared with the base policy, WMPO demonstrates the ability to self-correct*

**图5**的效率分析进一步证实：WMPO成功轨迹的相对平均长度显著短于基策略（以基策略为100%基准），表明WMPO不仅成功率更高，而且**抑制了卡顿行为（stuck behaviors），使策略执行更快、更流畅**。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_qE2FyvRvuF/figures/009_Figure_5.jpg]]
*Figure 5: Relative average trajectory length of successful trials across different policies (Base Policy = 100%)*

### 泛化能力

**表2**评估了各方法在三种分布外扰动下的鲁棒性：位置扰动（改变目标物初始位置）、背景扰动（替换桌面纹理）、纹理扰动（替换物体表面纹理）。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_qE2FyvRvuF/figures/008_Table_2.jpg]]
*Table 2: We evaluate each policy in its corresponding disruption scenario and report the success rate (%)*

| 方法 | 位置扰动 | 背景扰动 | 纹理扰动 | 平均 |
|------|---------|---------|---------|------|
| Base Policy | 18.8 | 46.3 | 14.9 | 26.7 |
| GRPO | 18.3 | 46.4 | 14.3 | 26.3 |
| DPO | 17.2 | 42.1 | 13.3 | 24.2 |
| **WMPO (Ours)** | **22.3** | **50.0** | **16.4** | **29.6** |

WMPO在所有扰动类型上均取得最优，平均成功率29.6%，比DPO高出5.4个百分点。值得注意的是，DPO在泛化场景下甚至弱于基策略（24.2% vs. 26.7%），说明离线RL可能过度拟合训练分布；而WMPO完全在世界模型中进行策略优化，捕获了更泛化的策略表征。

### 终身学习

**图6**展示了WMPO与基线的终身学习曲线。在交替更新世界模型和策略的多轮迭代中，WMPO实现了**稳定且显著的持续性能提升**，每轮迭代后成功率均有所增长。相比之下，DPO无法通过迭代改善——其性能在第一轮后趋于饱和甚至下降，因为离线RL缺乏探索新行为分布的能力。这一结果验证了WMPO框架在持续学习场景下的独特优势。

![[assets/figures/papers/paper_list_l12_https_openreview_net_forum_id_qE2FyvRvuF/figures/010_Figure_6.jpg]]
*Figure 6: Lifelong learning results of WMPO and baselines*

### 真实世界验证

在真实世界的精细操作任务“将方块插入立柱”（5mm间隙）上，基策略、DPO和WMPO的成功率分别为53%、60%和**70%**。WMPO相比基策略提升17个百分点，相比DPO提升10个百分点，验证了仿真中训练的策略能够有效迁移至真实场景。**图7**的对比显示，世界模型生成的想象轨迹与真实轨迹高度一致，进一步证实了像素空间世界模型对真实动态的精确捕捉能力。

### 消融分析

**奖励模型可靠性**：奖励模型在所有四个任务上均达到F1分数高于0.95，为策略优化提供了可靠的稀疏二元成功信号，无需复杂的手工奖励塑形。

**KL正则化移除与动态采样**：WMPO去除了标准GRPO中的KL散度正则化项，并引入动态采样策略确保组内轨迹多样性。消融结果显示，这一设计鼓励策略探索演示数据之外的新行为（如自我纠错），同时降低了显存消耗，GRPO训练保持稳定。

**噪声帧条件**：世界模型训练中引入噪声帧条件（对条件帧施加扩散时间步50的轻微噪声）是长时域生成稳定性的关键。不使用噪声条件会导致预测质量急剧下降，因为模型对条件帧的微小误差过于敏感。噪声训练使世界模型对不完美的自回归条件具有鲁棒性，支持完整轨迹的稳定生成。

### 失败模式与局限

1. **细微扰动下的预测失败**：**图10**展示了一个典型失败案例——虽然预测轨迹在最终帧之前保持准确，但世界模型未能捕捉方块因细微扰动卡在立柱上的瞬间。尽管此类失败在验证集上相对罕见，它揭示了像素空间世界模型在精确物理交互建模上的固有局限。

2. **离散动作空间限制**：当前WMPO仅支持离散动作表示（动作分箱为256 bins），尚未扩展到基于流匹配（flow matching）的连续策略空间，限制了其在更精细动作控制任务上的应用。

3. **计算资源需求**：世界模型训练和策略优化需要大量计算资源（32张H100 GPU），可能限制小型团队的复现。

4. **任务与模型泛化**：全部实验基于OpenVLA架构和Mimicgen/真实世界插入任务，推广到其他VLA模型或更复杂任务（如POMDP设定）有待验证。



## 定位与知识库关联

### 核心瓶颈与解决思路

将强化学习（RL）应用于视觉-语言-动作（VLA）模型面临两个根本性瓶颈：**物理交互样本效率极低**和**离策略价值估计偏差**。现有方案大致分为两条路线：

- **离线RL路线**：以 **DPO**（Rafailov et al., 2023）为代表，从偏好标注的真实轨迹中学习，完全避免在线交互，但受限于演示数据的覆盖范围，无法探索新行为，且对分布外状态泛化能力不足。
- **在线RL路线**：以 **GRPO**（Shao et al., 2024）为代表，直接在真实环境中进行在线策略优化，但物理交互成本高昂，难以实现真正的同策略（on-policy）学习，且面临奖励稀疏和样本效率低下的挑战。

WMPO的因果调节变量在于：**用学得的像素空间视频生成世界模型替代真实环境，实现完全在“想象”中进行的在线策略优化**，从根本上消除了对物理交互的依赖。这一设计使得策略能够以极低的真实轨迹预算（P=128）获得远超两类基线的样本效率（平均成功率47.1% vs. DPO 37.3%、GRPO 38.0%），且随着预算增加（P=1280），优势进一步扩大（57.6% vs. 42.4%、43.5%）。

### 技术路线差异与关键创新

WMPO与现有工作的本质差异体现在五个关键维度：

**1. 世界模型表征空间：像素空间 vs. 隐空间**

传统基于模型的RL方法（如Dreamer系列、TD-MPC2等）普遍采用隐状态世界模型（RSSM-based），在抽象隐空间中进行推演。然而，VLA模型的预训练视觉知识编码于像素空间，隐空间推演与VLA的视觉表征之间存在天然鸿沟。WMPO选择**直接在像素空间操作**，基于OpenSora视频扩散骨干并替换为SDXL的2D VAE，使世界模型能够直接利用VLA的预训练视觉知识，避免了跨空间迁移的信息损失。

**2. 条件注入机制：噪声帧条件与帧级动作控制**

长时域视频生成面临两个典型失败模式：一是条件帧与生成帧之间的视觉失真累积，二是动作信号与生成帧的时序错位。WMPO引入两项针对性技术：

- **噪声帧条件**（noisy-frame conditioning）：训练时对条件帧施加早期扩散时间步（timestep 50）的轻微噪声，而非保持干净帧，使模型学会从非完美条件中恢复，显著提升长时域生成的鲁棒性。消融实验表明，移除该技术会导致生成质量急剧下降。
- **帧级动作控制**（frame-level action control）：通过扩展AdaLN模块，在transformer的每一层为每个帧注入由动作信号生成的缩放和偏移参数（$\alpha_1^i, \gamma_1^i, \beta_1^i$），实现动作与帧的精确对齐，避免了全局条件注入（如交叉注意力或简单拼接）带来的错位问题。

**3. 策略优化算法：世界模型内的GRPO**

WMPO将GRPO完全迁移到世界模型内部执行，并做出关键修改：**移除KL散度正则化**以鼓励策略探索演示数据之外的新行为，同时引入**动态采样策略**确保组内轨迹的多样性。这种设计使得策略能够在想象空间中安全地探索失败模式，从而涌现出演示数据中不存在的自我纠错行为（见Figure 3），而离线RL方法（如DPO）受限于静态数据集，无法产生此类涌现。

**4. 奖励函数设计：稀疏奖励模型**

传统RL依赖复杂的手工奖励塑形（reward shaping），容易导致奖励黑客（reward hacking）问题。WMPO采用**轻量级学习奖励模型**：以VideoMAE编码器加线性头，在真实轨迹上通过二元交叉熵损失训练，预测完整想象轨迹的任务成功与否。该模型在四个任务上均达到F1分数高于0.95，为策略优化提供了可靠的稀疏奖励信号，避免了手工设计的脆弱性。

**5. 策略行为对齐：缓解仿真-现实鸿沟**

世界模型预训练数据的分布与目标策略的行为分布之间存在漂移，导致想象轨迹与真实轨迹的失配。WMPO通过**策略行为对齐**（Policy Behavior Alignment）解决此问题：在每轮优化中，用当前策略采集少量真实轨迹微调世界模型，使其适应下游的（状态，动作）分布并忠实捕捉失败模式。这一机制是实现终身学习（lifelong learning）的关键——实验表明，WMPO在交替更新策略和世界模型的多轮迭代中实现稳定且显著的持续提升，而DPO无法迭代改善（Figure 6）。

### 适用边界与局限

**当前适用边界：**

- **动作空间限制**：WMPO目前仅支持离散动作表示（动作分箱为256 bins），尚未扩展到基于流匹配（flow matching）的连续策略空间。这限制了其在需要精细连续控制的任务上的直接应用。
- **模型架构绑定**：全部实验基于OpenVLA架构，世界模型基于OpenSora视频扩散骨干，推广到其他VLA模型或世界模型架构需要额外验证。
- **任务复杂度**：验证任务集中在Mimicgen仿真的四个精细操作任务和真实世界的方形插入任务（5mm间隙），在更复杂的多阶段、长时域操作任务上的表现有待检验。
- **计算资源门槛**：训练世界模型和策略优化需要大量计算资源（32张H100 GPU），可能限制小型团队的复现。

**已知失败模式：**

世界模型在某些细微扰动下可能无法精确预测失败瞬间。如Figure 10所示，尽管预测轨迹在最终帧之前保持准确，但模型未能捕捉到方形零件因微小扰动而卡住的失败状态。原文指出此类失败在验证集上相对罕见，但在安全关键场景中仍需警惕。

### 开放问题

1. **连续动作扩展**：如何将WMPO扩展到基于流匹配的连续动作策略，并利用FlowGRPO进行优化？这需要重新设计动作编码和世界模型的条件注入机制。
2. **部分可观察性**：WMPO当前假设完全可观察的MDP，能否处理部分可观察马尔可夫决策过程（POMDP）等更复杂的决策设定，例如遮挡场景或需要记忆的任务？
3. **终身学习的稳定性-塑性权衡**：世界模型与策略交替更新的框架在更大规模、更长时间迭代下的稳定性和塑性如何？是否存在灾难性遗忘或模型崩溃的风险？
4. **更少样本的行为对齐**：能否进一步降低世界模型微调所需的真实轨迹数量，实现更少样本的策略行为对齐，从而进一步降低真实交互成本？
5. **跨形态泛化**：像素空间世界模型的应用范围能否拓展到更广泛的机器人形态（如双臂、移动操作）和传感器模态（如深度、触觉），而不仅仅是RGB视觉？



## 原文 PDF

![[paperPDFs/ICLR_2026/WMPO_World_Model_based_Policy_Optimization_for_Vision_Language_Action_Models.pdf]]
