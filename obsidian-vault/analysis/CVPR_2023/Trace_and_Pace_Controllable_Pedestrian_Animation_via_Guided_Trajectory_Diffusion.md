---
title: "Trace and Pace: Controllable Pedestrian Animation via Guided Trajectory Diffusion"
type: paper
paper_level: A
venue: CVPR
year: 2023
pdf_ref: paperPDFs/CVPR_2023/Trace_and_Pace_Controllable_Pedestrian_Animation_via_Guided_Trajectory_Diffusion.pdf
project_link: https://research.nvidia.com/labs/toronto-ai/trace-pace/
aliases:
- TP
- TPCPAGTD
tags:
- CVPR_2023
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "将轨迹生成建模为条件扩散过程，并利用测试时的分类器无关引导与重构引导，在去噪过程中施加任意用户目标，无需训练时指定任务。"
primary_logic: "在扩散去噪过程中，通过引导函数扰动干净轨迹预测实现灵活控制，保持轨迹真实性的同时，能与基于对抗运动先验的物理控制器无缝闭环，并进一步利用RL值函数引导提升场景适应能力。"
claims:
- "在 ORCA-Maps 数据集上，TRACE 结合障碍物与行人避碰引导实现了零碰撞率，且真实性（EMD）优于 VAE 基线。"
- "混合训练与负分类器无关采样权重（w<0）使得模型在 nuScenes 闭路环境下达到分布外目标控制（扰动航点误差 0.802）。"
- "闭环动画系统中，组合引导（障碍避碰+航点）进一步降低失败率，且额外添加 PACER 感知引导后效果更佳。"
- "采用特征图网格局部查询地图信息，相比全局编码或栅格化，在无引导时显著降低障碍物碰撞率。"
---

# Trace and Pace: Controllable Pedestrian Animation via Guided Trajectory Diffusion

> [!tip] 核心洞察
> 在扩散去噪过程中，通过引导函数扰动干净轨迹预测实现灵活控制，保持轨迹真实性的同时，能与基于对抗运动先验的物理控制器无缝闭环，并进一步利用RL值函数引导提升场景适应能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Trace and Pace：基于引导轨迹扩散的可控行人动画 |
| 英文题名 | Trace and Pace: Controllable Pedestrian Animation via Guided Trajectory Diffusion |
| 会议/期刊 | CVPR 2023 |
| Links | [paper](https://arxiv.org/abs/2304.01893); [Project](https://nv-tlabs.github.io/trace-pace); [Project](https://research.nvidia.com/labs/toronto-ai/trace-pace/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | TRACE and PACER |
| Dataset | ORCA-Maps (合成), nuScenes (真实数据), Flat (Crowd) 地形, 多样地形（障碍物 + 斜坡等） |

> [!tip] 效果简介
> - ORCA-Maps (合成) 上，障碍物碰撞率 / 代理人碰撞率 / EMD 横向加速度 为 TRACE (Combined Guidance): 0.014 / 0.009 / 0.009，对比 VAE (Combined Guidance): 0.018 / 0.015 / 0.032，变化 显著降低碰撞率并提升真实统计。
> - nuScenes (真实数据) 上，扰动航点误差 (m) 为 TRACE Mixed w=-0.5: 0.802，对比 VAE: 0.962，变化 误差降低约 0.16m。
> - Flat (Crowd) 地形 上，失败率 / 轨迹跟随误差 为 PACER Agent Aware + Agt Avoid 引导: 0.013 / 0.071，对比 PACER Agent Unaware 无引导: 0.252 / 0.102，变化 失败率降低 94.8%。

## 概述

**问题瓶颈**：数据驱动的行人轨迹模型在测试时难以灵活满足用户自定义控制目标（如航点、避碰、社会分组），而规则方法虽可控却缺乏真实感；同时，物理动画控制器通常针对特定任务重训练，缺乏通用性。

**核心思路**：将行人轨迹生成建模为条件扩散过程，在去噪阶段通过**重构引导（Reconstruction Guidance）** 扰动干净轨迹预测，实现对任意可微目标的测试时控制，无需训练时指定任务。该轨迹规划器（TRACE）与基于对抗运动先验的物理控制器（PACER）形成闭环动画系统，并进一步利用强化学习值函数引导提升场景适应能力。

**方法定位**：TRACE 作为高层轨迹扩散模型，通过 2D 卷积特征网格局部查询地图信息，结合分类器无关采样与混合训练策略，在保持轨迹真实性的同时支持多目标组合引导；PACER 作为底层物理动画控制器，具备地形、社交与体型感知能力，驱动模拟人形跟随目标轨迹。

**主要结果**：
- 在 ORCA-Maps 合成数据集上，TRACE 结合障碍物与行人避碰引导实现接近零碰撞率，且轨迹真实度（EMD）显著优于 VAE 基线（Table 1）。
- 在 nuScenes 真实数据上，混合训练配合负分类器无关采样权重（w=−0.5）使分布外航点控制误差降至 0.802 m（Table 2）。
- 闭环动画系统中，组合引导（障碍避碰+航点）大幅降低失败率，额外添加 PACER 感知引导后效果更佳（Table 3）；值函数引导进一步提升复杂地形下的轨迹跟随鲁棒性（Table 4）。
- 消融实验证实：特征图网格地图编码优于全局编码或栅格化（Table 5）；混合训练与条件随机丢弃增强引导灵活性（Table 6）；代理感知与体型感知对降低失败率至关重要（Table 9）。

**局限性**：扩散采样效率较低（单角色 1–3 秒），难以实时；多目标引导权重平衡困难，轨迹可能偏离数据流形；PACER 面对大型障碍物且无绕行路径时表现不佳，低速步态多样性不足。

## 背景与动机

行人动画是计算机视觉与图形学交叉领域的核心问题，其目标是在复杂场景中生成真实、可控的行人运动。该问题的上游是轨迹预测与规划，下游是物理仿真与动作合成，两者之间的鸿沟构成了当前方法的主要瓶颈。

### 现有方法的双重困境

数据驱动的行人轨迹模型（如基于 CVAE 或扩散模型的方法）能够从大规模数据中学习逼真的运动模式，但面临一个根本性矛盾：**训练时的数据分布无法覆盖测试时用户多样化的控制需求**。当用户希望指定航点、避碰特定障碍物、或引导人群保持社交分组时，这些模型缺乏在推理阶段灵活响应任意目标的机制。相反，基于规则的规划器（如 **ORCA**）天然支持精确控制，但其生成的轨迹缺乏真实行人运动的统计特征，表现为过度的路径平滑与不自然的加减速模式。

在底层动画控制层面，现有的物理仿真控制器通常针对特定任务进行端到端训练——例如在平坦地形上行走、或在固定障碍物布局中导航。这种**任务特化的训练范式**导致控制器缺乏通用性：一旦场景地形、障碍物分布或交互代理数量发生变化，就需要重新训练。同时，这些控制器往往将轨迹跟踪作为唯一目标，忽略了步态自然性、体型差异、以及社交环境中的感知能力。

### 核心洞察：轨迹扩散与测试时引导的融合

本文的核心洞察在于将上述两个层面的问题统一到一个闭环框架中解决。其因果机制可以概括为：

1. **将轨迹生成建模为条件扩散过程**，使得模型能够从数据中学习丰富的运动先验；
2. **在扩散去噪过程中引入测试时引导（test-time guidance）**，通过可微损失函数扰动干净轨迹预测，实现对任意用户目标的灵活响应，而无需在训练阶段预先指定控制任务；
3. **将引导后的轨迹传递给基于对抗运动先验的物理控制器**，形成高层规划与低层执行的闭环反馈，并进一步利用强化学习中的值函数作为额外引导信号，提升场景适应能力。

这一设计使得系统在保持轨迹真实性的同时，获得了规则方法般的可控性——用户只需在测试时定义一个可微的目标函数（如“远离障碍物”或“接近目标航点”），即可驱动扩散模型生成符合该目标的轨迹。

### 关键挑战与设计选择

实现上述框架需要解决几个关键技术挑战：

- **地图条件的有效编码**：轨迹生成需要感知场景中的障碍物布局。简单的全局编码或栅格化方式难以提供精确的局部空间信息，而本文提出的特征图网格（feature grid）方法允许在去噪过程中按轨迹位置插值查询局部地图特征，显著降低了无引导条件下的障碍物碰撞率（Table 5）。

- **引导公式的稳定性**：传统的噪声均值引导（noisy guidance）直接在噪声空间施加梯度扰动，容易导致轨迹偏离数据流形。本文提出的重构引导（reconstruction guidance）改为扰动干净轨迹预测，再将梯度反传至噪声输入，支持任意可微损失函数，在引导效果和真实性上均优于噪声均值方法（Table 1）。

- **分布外目标的适应性**：当用户指定的控制目标（如扰动航点）超出训练分布时，标准分类器无关采样（classifier-free sampling）的权重 $w > 0$ 会抑制多样性，反而降低可控性。本文发现采用**负权重（$w < 0$）** 可以显著提升模型对引导的敏感性，使轨迹能够灵活适应分布外目标（Table 2, Table 8）。

### 系统闭环与局限

TRACE-PACER 系统将轨迹扩散模型（TRACE）与物理动画控制器（PACER）连接为闭环：TRACE 每 2 秒根据 PACER 的当前状态重新规划轨迹，PACER 则负责在物理仿真中执行轨迹并处理地形、障碍物及其他代理的实时交互。这一闭环设计使得系统能够在多样地形（障碍物、斜坡、楼梯等）和拥挤人群场景中稳定运行。

然而，当前框架仍存在明显局限：扩散采样的计算开销较大（单角色 1–3 秒），难以满足实时应用需求；多目标引导时不同损失项的权重 $\alpha$ 难以平衡，过大的总梯度可能导致轨迹偏离数据流形；PACER 在面对大型障碍物且无绕行路径时表现不佳，且低速行走动作缺乏多样性。这些问题为后续研究指明了方向，包括扩散模型的轻量化、引导过程的动态裁剪、以及更丰富的社交行为建模。

## 核心创新

本工作提出 **TRACE**（可控轨迹扩散模型）与 **PACER**（物理动画控制器）构成的闭环行人动画系统，其核心创新在于将轨迹生成建模为条件扩散过程，并通过**测试时重构引导**实现灵活的用户控制，同时与基于物理的底层控制器无缝集成。以下从四个关键维度阐述相对于基线方法的根本性改进。

### 1. 地图条件编码：从全局向量到局部特征网格查询

传统方法通常将场景地图编码为单一全局特征向量或栅格化表示，这导致空间信息的粗粒度丢失，尤其在无引导采样时，轨迹难以感知局部障碍物分布。TRACE 采用**2D 卷积特征网格**编码地图，在去噪过程中按轨迹的每个空间位置进行**插值查询**（Figure 2）。这一设计使得模型能够捕获细粒度的局部环境信息，消融实验（Table 5）表明，仅此一项改进，在无引导条件下即可将障碍物碰撞率从全局编码的 0.056 降至 0.046，降幅约 18%。定性对比（Figure 12）也显示，网格特征使轨迹在障碍物附近表现出更细腻的避让行为。

### 2. 引导公式：从噪声均值扰动到干净轨迹重构引导

现有扩散引导方法（如 Diffuser 方式）通常在预测的**噪声均值**上直接施加梯度扰动（Eq. 5），这限制了可用的引导损失形式。TRACE 提出**重构引导**（Reconstruction Guidance）：首先从网络获取干净轨迹预测 $\hat{\tau}^0$，然后用任意可微损失函数 $\mathcal{I}$ 的梯度对其进行扰动，并将梯度**反传至噪声输入** $\tau^k$（Eq. 6）：

$$\tilde{\tau}^{0} = \hat{\tau}^{0} - \alpha \Sigma_{k} \nabla_{\tau^{k}} \mathcal{I}(\hat{\tau}^{0})$$

这一公式的关键优势在于：引导损失直接作用于**物理可解释的干净轨迹空间**，而非抽象的噪声空间。这使得系统可以无缝集成任意可微目标，包括解析的避碰损失、航点跟随损失，乃至从 PACER 强化学习训练中获得的**值函数**（Value Function）。消融实验（Table 4）证实，值函数引导可额外降低失败率约 2.4%（从 0.202 降至 0.178），并改善轨迹跟随误差。

### 3. 训练策略：混合数据集与分类器无关采样

传统条件扩散模型往往在单一数据集上以固定条件训练，限制了测试时的控制灵活性。TRACE 采用两项关键策略：

- **多数据集混合训练**：将 ORCA-Maps（合成）与 ORCA-Interact（交互）数据混合，并配合**10% 的条件独立随机丢弃**。消融（Table 6）表明，丢弃率超过 5% 后对性能影响甚微，但显著增强了模型对分类器无关采样的兼容性。
- **负分类器无关采样权重**（$w < 0$）：在测试时组合条件与无条件噪声预测时，采用负权重可**放大**引导信号的影响。Table 7–8 显示，$w = -0.5$ 使 nuScenes 上扰动航点误差从 1.129 降至 0.546，降幅超过 50%；但 $w < -0.5$ 会损害轨迹真实性，揭示了控制强度与自然度之间的权衡边界。

### 4. 控制器运动监督：从标准 AMP 到对称性约束

PACER 在标准对抗运动先验（AMP）判别器基础上，额外引入**运动对称损失**（Mirror Symmetry Loss，Eq. 7）：

$$L_{\mathrm{sym}}(\theta) = \| \pi_{\mathrm{PACER}}(h_t, o_t, \beta, \tau_s) - \Phi_a(\pi_{\mathrm{PACER}}(\Phi_s(h_t, o_t, \beta, \tau_s))) \|^2$$

该损失通过比较原始状态与镜像状态下的策略输出差异，显式鼓励对称步态，有效抑制跛行等不对称运动伪影。配合代理感知（Agent Aware）与体型感知（Body Aware）设计，PACER 在拥挤场景中将失败率从 0.252 降至 0.087（Table 9），降幅达 65%。

### 创新总结

上述四个 changed slots 形成了一条清晰的因果链：**局部特征网格**提供精细的空间感知基础，**重构引导**赋予测试时任意目标的可控性，**混合训练与负采样权重**使模型适应分布外控制，而**对称运动损失**确保底层动画的自然度。这些创新共同解决了“数据驱动方法缺乏可控性，规则方法缺乏真实感”的核心瓶颈，使得系统能够在零碰撞率下实现用户指定的航点导航、障碍避碰与人群交互（Table 1, Table 3）。

## 整体框架

Trace and Pace 系统由两个核心模块构成闭环流水线：**TRACE**（高层轨迹扩散规划器）与 **PACER**（底层物理动画控制器）。TRACE 以场景历史轨迹和语义地图为条件，通过条件扩散过程生成未来轨迹；生成轨迹随后传递给 PACER，驱动物理模拟人形在三维地形中行走。PACER 的执行结果（当前状态）每隔 2 秒反馈回 TRACE 进行重规划，形成闭环控制（Sec. 3.3）。

**输入流**：对于场景中每个目标行人，TRACE 接收三类信息——该行人自身的历史轨迹、所有邻近行人的历史轨迹、以及环境的语义地图（Figure 2）。地图通过 2D 卷积网络编码为特征网格，在去噪过程中按当前轨迹位置进行局部插值查询，而非使用全局编码向量（Sec. 3.1.1）。

**扩散规划**：TRACE 将未来轨迹视为待去噪的信号。前向过程逐步向干净轨迹 $ \tau^0 $ 添加高斯噪声得到 $ \tau^k $（Eq. 1）；逆向过程通过 1D 时序 U-Net（Figure 7）预测干净轨迹 $ \hat{\tau}^0 $，并以过去运动特征、邻居特征和地图特征网格为条件（Sec. 3.1.1）。训练损失为预测干净轨迹与真实轨迹的均方误差（Eq. 3）。

**测试时引导**：用户控制通过**重构引导**（Reconstruction Guidance）实现。在每个去噪步，先由网络预测干净轨迹 $ \hat{\tau}^0 $，再用任意可微损失函数 $ \mathcal{I} $ 的梯度扰动该预测，并将梯度反传至噪声输入 $ \tau^k $（Eq. 6）。这允许在测试时灵活施加障碍物避碰、行人避碰、航点跟随等控制目标，而无需在训练阶段指定这些任务（Sec. 3.1.2）。配合分类器无关采样（Eq. 4）和混合训练策略（多数据集联合训练 + 条件随机丢弃），TRACE 可适应分布外的控制目标（Sec. 4.2）。

**物理执行**：PACER 是一个基于对抗运动先验（AMP）的物理控制器，接收 TRACE 输出的目标轨迹 $ \tau_s $、环境观测 $ o_t $ 和体型参数 $ \beta $，输出关节力矩驱动物理人形（Figure 3, Figure 9）。除标准 AMP 判别器外，PACER 额外引入**运动对称损失** $ L_{\mathrm{sym}} $（Eq. 7），鼓励对称步态以减少跛行等不自然动作（Sec. 3.2）。控制器具备地形感知、社交感知（感知其他代理）和体型感知能力，使其能在多样地形和人群场景中鲁棒执行（Table 9）。

**闭环反馈**：TRACE 每 2 秒重新规划一次，接受 PACER 反馈的当前人形状态，使高层规划与底层执行形成动态闭环。此外，PACER 在强化学习训练中习得的**值函数**可直接作为 TRACE 的引导目标，鼓励生成更易于物理执行、更适应当前地形的轨迹（Table 4, Sec. 3.2）。

整个系统的关键设计在于：扩散模型提供轨迹的真实性与多样性，重构引导提供测试时的灵活可控性，物理控制器提供运动物理合理性，三者通过闭环机制耦合为统一的 pedestrian animation 系统（Figure 1, Figure 6）。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2304_01893/figures/003_Figure_3.jpg]]
*Figure 3: Pipeline: Pedestrian Animation Controller (PACER)*

## 核心模块与公式推导

### 3.1 TRACE 轨迹扩散模型

TRACE 将行人未来轨迹生成建模为条件去噪扩散概率模型。给定目标行人的历史轨迹、周围邻居的历史轨迹以及语义地图，模型输出一条未来轨迹计划。其核心由三个模块构成：**条件扩散骨架**、**测试时引导机制** 和**地图特征网格编码**。

**前向扩散过程** 将干净轨迹 $\tau^0$ 逐步加噪为纯噪声 $\tau^K$：

$$q(\tau^{1:K} \mid \tau^0) := \prod_{k=1}^K q(\tau^k \mid \tau^{k-1})$$

单步转移核为高斯分布：

$$q(\tau^k \mid \tau^{k-1}) := \mathcal{N}(\tau^k; \sqrt{1-\beta_k} \tau^{k-1}, \beta_k \mathbf{I})$$

其中 $\beta_k$ 为噪声调度参数，控制每步添加的噪声量。

**逆向去噪过程** 学习从噪声恢复干净轨迹：

$$p_\phi(\tau^{k-1} \mid \tau^k, C) := \mathcal{N}(\tau^{k-1}; \mu_\phi(\tau^k, k, C), \Sigma_k)$$

其中 $C$ 为条件信息（历史轨迹、邻居特征、地图），$\mu_\phi$ 为网络预测的去噪均值，$\Sigma_k$ 为固定方差。训练损失为对干净轨迹预测的均方误差：

$$L = \mathbb{E}_{\epsilon, k, \tau^0, C} \left[ ||\tau^0 - \hat{\tau}^0||^2 \right]$$

网络实际预测干净轨迹 $\hat{\tau}^0$，再通过闭式解恢复去噪均值：

$$\pmb{\mu}(\pmb{\tau}^0, \pmb{\tau}^k) := \frac{\sqrt{\bar{\alpha}_{k-1}}\beta_k}{1-\bar{\alpha}_k} \pmb{\tau}^0 + \frac{\sqrt{\alpha_k}(1-\bar{\alpha}_{k-1})}{1-\bar{\alpha}_k} \pmb{\tau}^k$$

其中 $\alpha_k = 1 - \beta_k$，$\bar{\alpha}_k = \prod_{i=1}^k \alpha_i$。

**地图特征网格编码** 是 TRACE 的关键设计选择。地图 $M$ 通过 2D 卷积网络编码为特征网格，在去噪的每一步，按当前噪声轨迹的 2D 位置进行双线性插值查询，将局部地图特征注入 U-Net 的中间层。消融实验（Table 5）证实，这种网格查询方式在无引导时障碍物碰撞率（0.046）显著低于全局编码（0.056）或栅格化编码（0.052），说明局部空间查询能更精细地捕捉障碍物边界信息。

**分类器无关引导** 通过训练时随机丢弃条件信息（10% 概率）实现。测试时组合条件与无条件噪声预测：

$$\tilde{\epsilon}_\phi = \epsilon_\phi(\tau^k, k, C) + w \left( \epsilon_\phi(\tau^k, k, C) - \epsilon_\phi(\tau^k, k) \right)$$

其中 $w$ 为引导权重。当 $w > 0$ 时增强条件影响，$w < 0$ 时则推动采样远离条件分布。消融实验（Table 7, Table 8）表明，$w = -0.5$ 时模型对引导损失最敏感，能在 nuScenes 扰动航点任务中将误差从 1.129 降至 0.546，但 $w < -0.5$ 会损害轨迹真实性。

### 3.2 重构引导机制

区别于直接在噪声均值上施加梯度扰动的标准做法：

$$\tilde{\pmb{\mu}} = \pmb{\mu} - \alpha \pmb{\Sigma}_{k} \nabla_{\pmb{\mu}} \mathcal{I}(\pmb{\mu})$$

TRACE 采用**重构引导**，扰动网络预测的干净轨迹 $\hat{\tau}^0$：

$$\tilde{\tau}^{0} = \hat{\tau}^{0} - \alpha \Sigma_{k} \nabla_{\tau^{k}} \mathcal{I}(\hat{\tau}^{0})$$

关键区别在于：梯度是对噪声输入 $\tau^k$ 求导，需通过去噪网络反向传播，而非对均值直接求导。这使得引导损失 $\mathcal{I}$ 可以是任意可微函数（如障碍物距离、航点偏差、RL 值函数），无需训练时指定控制目标。扰动后的干净轨迹再通过式 (9) 恢复去噪均值，进入下一步采样。这一设计是 TRACE 实现测试时灵活控制的因果杠杆。

### 3.3 PACER 物理动画控制器

PACER 是底层物理控制器，以目标轨迹 $\tau_s$、本体感受历史 $h_t$、环境观测 $o_t$ 和体型参数 $\beta$ 为输入，输出关节力矩驱动模拟人形。其策略网络 $\pi_{\mathrm{PACER}}$ 由任务特征提取器 $E_{\mathrm{PACER}}$ 和动作策略网络 $\pi_{\mathrm{PACER}}^{\mathrm{A}}$ 组成（Figure 9），基于对抗运动先验（AMP）训练。

除标准 AMP 判别器外，PACER 额外引入**运动对称损失**以抑制跛行等不对称步态：

$$L_{\mathrm{sym}}(\theta) = \| \pi_{\mathrm{PACER}}(h_t, o_t, \beta, \tau_s) - \Phi_a(\pi_{\mathrm{PACER}}(\Phi_s(h_t, o_t, \beta, \tau_s))) \|^2$$

其中 $\Phi_s$ 将状态沿 sagittal 平面镜像，$\Phi_a$ 将动作进行对应镜像变换。该损失鼓励策略输出左右对称的运动模式。

### 3.4 闭环重规划

系统以 2 秒为周期进行闭环重规划：TRACE 根据当前状态生成新轨迹，PACER 执行并反馈实际状态。轨迹规划时间随场景复杂度变化（Figure 14），单角色约 1–3 秒，是系统实时性的主要瓶颈。

## 实验与分析

### 核心实验结果

#### 轨迹生成的可控性与真实性（ORCA-Maps）

在 ORCA-Maps 合成数据集上，TRACE 通过重构引导实现了对用户控制目标的高效满足，同时保持轨迹的真实感。Table 1 展示了不同引导组合下的定量对比：

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2304_01893/figures/007_Table_1.jpg]]
*Table 1: Guidance evaluation on ORCA-Maps dataset. TRACE using full diffusion guidance improves upon VAE latent optimization and selective sampling (TRACE-Filter) in terms of meeting objectives, while maintaining strong realism. Table 2. Guidance evaluation on nuScenes. Training on mixed data and using w\<0 for classifier-free sampling are important to achieve controllability for out-of-distribution objectives*

- **单目标引导**：在仅使用障碍物避碰引导时，TRACE 将碰撞率降至 **0.014**，显著优于 VAE 基线的 0.018；在行人避碰引导下，TRACE 实现 **零碰撞率**（0.000），而 VAE 为 0.010。
- **组合引导**：同时施加障碍物与行人避碰引导时，TRACE 的障碍物碰撞率保持 0.014，行人碰撞率仅 0.009，且轨迹真实度（EMD 横向加速度）为 **0.009**，远优于 VAE 的 0.032。这表明 TRACE 在满足多重控制目标时不会牺牲轨迹的自然性。
- **与滤波基线的对比**：TRACE-Filter（无引导扩散采样后滤波）在组合引导下的行人碰撞率高达 0.147，说明测试时引导是必要的——仅靠采样后筛选难以有效满足约束。

**关键机制**：重构引导（Eq. 6）直接扰动干净轨迹预测 $\hat{\tau}^0$，将任意可微损失函数的梯度反传至噪声输入 $\tau^k$，使得去噪过程逐步趋向用户目标。相比 VAE 的潜变量优化，扩散模型的多步去噪提供了更细粒度的控制空间。

#### 分布外目标控制（nuScenes）

在真实驾驶场景数据集 nuScenes 上，TRACE 展现了强大的分布外目标控制能力。Table 2 显示，在扰动航点引导任务中：

- 混合训练（ORCA-Maps + ORCA-Interact）配合负分类器无关采样权重 $w = -0.5$ 时，TRACE 的航点误差仅为 **0.802 m**，优于 VAE 的 0.962 m。
- 当 $w = 0$（标准条件采样）时，误差为 1.129 m；$w = -0.5$ 将误差降低约 **29%**，证明负权重能显著增强模型对引导的敏感性，使采样分布向满足控制目标的方向偏移。

**因果机制**：混合训练使模型学习了更丰富的轨迹分布，而 $w < 0$ 的采样策略（Eq. 4）将分类器无关引导反向作用——放大无条件与条件预测的差异，使输出更易被外部引导函数“推动”出原始分布，从而适应训练时未见过的控制目标。

#### 闭环动画系统性能

将 TRACE 与 PACER 物理控制器组成闭环系统后，在多样地形和人群场景中评估了端到端动画质量（Table 3）：

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2304_01893/figures/009_Table_3.jpg]]
*Table 3: Closed-loop animation results. Our system successfully follows waypoints and avoids collisions in a variety of terrains, and additional guidance improves performance*

- **人群平面场景**：代理感知（Agent Aware）的 PACER 配合行人避碰引导，将失败率从无感知无引导的 **0.252 降至 0.013**（降低 94.8%），轨迹跟随误差从 0.102 降至 0.071。
- **障碍物地形**：组合引导（航点 + 障碍避碰）使失败率降至 0.178，额外添加 PACER 值函数引导后进一步降至 **0.178 → 0.178**（原文 Table 4 显示值函数引导额外降低失败率约 2.4%，从 0.202 降至 0.178）。
- **值函数引导的作用**（Table 4）：利用 PACER 强化学习训练中学习到的值函数作为 TRACE 的引导目标，鼓励生成更易被控制器跟随的轨迹。在障碍物地形中，值函数引导将失败率从 0.202 降至 0.178，轨迹跟随误差从 0.118 降至 0.113。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2304_01893/figures/010_Table_4.jpg]]
*Table 4: Using the value function learned in RL training as guidance improves quality of trajectory following and robustness to varying terrains, obstacles, and other agents*

**闭环反馈机制**：TRACE 每 2 秒重新规划，接受 PACER 的当前状态作为输入，形成感知-规划-执行的闭环。值函数引导的独特优势在于它直接编码了控制器在当前地形和状态下的“可达性”知识，使高层规划与低层执行能力对齐。

### 消融实验

#### 地图编码方式

Table 5 对比了三种地图条件编码策略在无引导下的表现：

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2304_01893/figures/016_Table_5.jpg]]
*Table 5: No guidance evaluation on ORCA-Maps dataset. Ablation on architecture design choices*

- **特征图网格（Grid）**：障碍物碰撞率 **0.046**，行人碰撞率 0.020，EMD 0.009。
- **全局编码（Global）**：障碍物碰撞率 0.056，行人碰撞率 0.023，EMD 0.008。
- **栅格化编码（Raster）**：障碍物碰撞率 0.052，行人碰撞率 0.024，EMD 0.009。

特征图网格在障碍物碰撞率上分别比全局编码和栅格化低 **17.9%** 和 **11.5%**。其优势在于：在去噪过程中，按轨迹点位置在 2D 卷积特征图上进行局部插值查询，保留了空间局部性，使模型能感知轨迹附近的精确障碍物布局，而非依赖压缩后的全局摘要。

#### 训练策略

Table 6 的消融表明：

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2304_01893/figures/017_Table_6.jpg]]
*Table 6: No guidance evaluation on ORCA-Maps dataset. Ablation on training routine*

- 混合 ORCA-Maps 与 ORCA-Interact 数据集训练，相比仅用 ORCA-Maps，障碍物碰撞率从 0.046 小幅变化至 0.048，行人碰撞率从 0.020 降至 0.017，EMD 保持 0.009——**几乎无性能损失**。
- 条件随机丢弃概率在 5%–20% 范围内对无引导性能影响甚微（碰撞率波动 < 0.003），10% 丢弃率在引导灵活性与基础性能间取得平衡。

**设计意图**：混合训练扩展了轨迹分布覆盖，而条件丢弃使模型同时学习条件与无条件去噪，为测试时的分类器无关采样（Eq. 4）提供基础。

#### 分类器无关采样权重

Table 7（ORCA-Maps 无引导）和 Table 8（nuScenes 扰动航点引导）系统分析了权重 $w$ 的影响：

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2304_01893/figures/018_Table_7.jpg]]
*Table 7: Classifier-free sampling analysis on ORCA-Maps dataset with no guidance. Table 8. Classifier-free sampling analysis on nuScenes dataset using perturbed waypoint guidance. w= 2.0*

- **无引导场景**（Table 7）：$w$ 从 0 增至 2.0，障碍物碰撞率从 0.046 降至 0.024，但 EMD 从 0.009 升至 0.024——真实度下降。$w < 0$ 时碰撞率上升，轨迹更“自由”。
- **引导场景**（Table 8）：$w = -0.5$ 时航点误差最低（0.802），$w = 0$ 时为 1.129，$w = -1.0$ 时误差回升至 0.950 且加速度真实度恶化。
- **视觉证据**（Figure 13）：增大 $w$ 使采样轨迹方差降低，靠近障碍物的行人表现出更强的避碰倾向，但轨迹多样性受限。

**权衡机制**：$w > 0$ 增强条件控制，使轨迹更“安全”但更确定性；$w < 0$ 降低条件约束，使轨迹更易被外部引导重塑，但 $w < -0.5$ 后偏离数据流形，真实性受损。

#### PACER 控制器设计

Table 9 消融了 PACER 的关键设计：

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2304_01893/figures/020_Table_9.jpg]]
*Table 9: PACER ablation study while using TRACE as the trajectory planner*

- **代理感知**：使 PACER 感知其他行人，在无引导时将失败率从 0.252 降至 **0.087**（降低 65.5%）；配合引导后降至 0.013。
- **体型感知**：在无引导时将失败率从 0.125 降至 0.093；配合引导后效果相近（0.013 vs 0.013），说明引导信号在一定程度上弥补了体型感知的缺失。
- **运动对称损失**（Eq. 7）：通过惩罚原始输出与镜像输出的差异，减少跛行等不对称步态，提升动画视觉质量（定性结果，无独立定量指标）。

### 失败模式与局限性

1. **扩散采样效率**：TRACE 单角色规划耗时 1–3 秒（Figure 14），难以满足实时应用需求。这是扩散模型多步去噪的固有瓶颈。
2. **多目标引导的梯度平衡**：同时施加多个引导目标时，各损失权重 $\alpha$ 的调节缺乏自动化机制，过大的总梯度可能使轨迹偏离数据流形，产生不自然的运动。
3. **大型障碍物绕行**：PACER 面对完全阻塞路径的大型障碍物时表现不佳——控制器缺乏高层绕行决策能力，仅依赖局部避碰。
4. **步态多样性不足**：动作数据库限制导致不同体型的步态风格趋同，无法表现社交行为（如打电话、交谈）所需的丰富上半身动作。

### 图表关键结论汇总

- **Table 1**：TRACE 重构引导在 ORCA-Maps 上实现零行人碰撞率，组合引导下真实度（EMD 0.009）显著优于 VAE（0.032）。
- **Table 2**：混合训练 + $w = -0.5$ 使 nuScenes 扰动航点误差降至 0.802 m，证明分布外控制能力。
- **Table 3**：闭环系统中，代理感知 + 引导使人群场景失败率降低 94.8%。
- **Table 4**：值函数引导额外降低失败率，证明 RL 值函数与扩散引导的协同作用。
- **Table 5**：特征图网格地图编码在无引导时障碍物碰撞率最低（0.046），验证局部查询设计的有效性。
- **Table 7–8**：$w$ 控制条件强度与引导敏感性的权衡，$w = -0.5$ 为引导任务的最优折衷点。
- **Table 9**：代理感知是 PACER 在人群场景中最关键的消融因素，体型感知在无引导时贡献显著。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2304_01893/figures/006_Figure_5.jpg]]
*Figure 5: nuScenes results demonstrating flexibility of TRACE. (a) Using mixed training and w=−0.5 is best for noisy waypoints. (b) Social group guidance encourages sets of pedestrians to stay close. (c) Mixed training (ETH/UCY+nuScenes) learns a more diverse distribution as demonstrated by unconditional sampling*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2304_01893/figures/014_Figure_10.jpg]]
*Figure 10: During training, 2048 humanoids are simulated in parallel on our synthetic terrain. Figure 11. Synthetic terrains used for training PACER. From left to right: obstacles, discrete terrains, stairs (up), stairs (down), uneven terrains, and slopes*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2304_01893/figures/005_Table.jpg]]

## 方法谱系与知识库定位

### 问题域与核心瓶颈

行人动画系统长期面临一个根本性矛盾：数据驱动的轨迹模型能产生逼真的运动模式，但难以在测试时灵活满足用户自定义的控制目标；基于规则的方法（如 ORCA）虽可控，却缺乏真实感。同时，物理动画控制器通常针对单一任务从头训练，缺乏跨场景的通用性。**TRACE and PACER** 正是针对这一瓶颈，将轨迹生成建模为条件扩散过程，利用测试时的分类器无关引导与重构引导，在去噪过程中施加任意用户目标，无需在训练时指定任务类型。

### 方法谱系定位

#### 轨迹生成：从确定性预测到可控扩散

行人轨迹预测领域长期由确定性回归模型主导，随后 VAE 框架（如 **STRIVE**）引入潜变量优化，在测试时通过优化潜码实现一定程度的控制。然而，VAE 的潜空间结构限制了控制精度与轨迹真实性的平衡。TRACE 将轨迹生成推入扩散模型范式，其核心创新在于：

- **重构引导（Reconstruction Guidance）**：不同于早期扩散控制方法（如 **Diffuser**）直接在噪声均值上施加梯度扰动（Eq. 5），TRACE 扰动干净轨迹预测 $\hat{\tau}^0$，并将梯度反传至噪声输入 $\tau^k$（Eq. 6）。这一设计允许使用任意可微损失函数作为引导目标，包括解析约束（避碰、航点）和从 PACER 强化学习训练中直接继承的值函数，无需额外训练。
- **特征图网格编码**：相比将地图编码为单一全局向量或栅格化图像，TRACE 使用 2D 卷积网络生成特征图网格，在去噪过程中按轨迹位置插值查询局部地图信息。消融实验（Table 5）表明，这一设计在无引导时即可显著降低障碍物碰撞率（0.046 vs 全局编码的 0.056/栅格化的 0.052）。

#### 物理动画控制：从任务特化到通用跟随

物理模拟的人形动画控制通常依赖对抗运动先验（AMP）框架，但现有工作多为特定任务（如目标导航、地形穿越）单独训练控制器。PACER 的贡献在于：

- **通用轨迹跟随**：训练时使用多样化合成地形（障碍物、楼梯、斜坡、崎岖地形等，Figure 11）和随机目标轨迹，使单一策略具备跨场景的泛化能力。
- **运动对称损失**：在标准 AMP 判别器之外，额外添加镜像对称损失 $L_{\mathrm{sym}}$（Eq. 7），鼓励对称步态，减少跛行等不对称运动伪影。
- **社交与体型感知**：策略网络输入包含邻近代理特征和自身体型参数 $\beta$，使得 PACER 能感知周围行人并适应不同体型。

#### 闭环集成：扩散规划 + 物理执行

TRACE 与 PACER 形成分层闭环系统：TRACE 每 2 秒重新规划未来轨迹，接受 PACER 的当前状态作为反馈；PACER 则执行轨迹跟随，并将实际运动结果返回给 TRACE。这一设计使得高层规划能适应底层执行的偏差，同时底层的值函数引导进一步鼓励 TRACE 生成易于执行的轨迹。

### 关键消融发现

| 消融维度 | 核心发现 | 证据锚点 |
|---------|---------|---------|
| 引导公式 | 重构引导（Eq. 6）优于噪声均值引导（Eq. 5），支持任意可微损失 | Sec. 3.1.2, Table 1 |
| 地图编码 | 特征图网格 > 全局编码 > 栅格化，无引导时碰撞率降低约 18% | Table 5 |
| 训练策略 | 混合 ORCA-Maps 与 ORCA-Interact 训练 + 10% 条件丢弃，在不损害性能的前提下增强引导灵活性 | Table 6 |
| 分类器无关采样权重 | $w < 0$ 显著提升对引导的敏感性（扰动航点误差从 1.129 降至 0.546），但 $w < -0.5$ 会削弱轨迹真实性 | Table 7, Table 8, Figure 13 |
| PACER 代理感知 | 使代理感知其他行人，拥挤场景失败率从 0.252 降至 0.087 | Table 9 |
| 值函数引导 | 使用 PACER 的 RL 值函数作为额外引导，在多样地形上进一步降低失败率约 2.4% | Table 4 |

### 适用边界与局限性

1. **采样效率**：TRACE 扩散采样需 1–3 秒/角色，难以满足实时应用需求。这是扩散模型在交互式系统中的共性瓶颈。
2. **多目标引导稳定性**：当同时施加多个引导目标时，权重 $\alpha$ 的平衡易导致整体梯度过大，轨迹可能偏离数据流形。论文未提出自动权重调节机制。
3. **极端障碍物场景**：PACER 面对大型障碍物且无绕行路径时表现不佳，这源于物理控制器缺乏高层路径规划能力。
4. **动作多样性不足**：动作数据库限制导致不同体型的步态多样性有限，难以表现社交行为（如打电话、交谈等上肢动作）。
5. **数据依赖**：TRACE 的轨迹真实性依赖于训练数据分布，在分布外场景（如极端拥挤或非结构化环境）中，无引导采样的质量可能下降。

### 开放问题

- **动态引导裁剪**：能否在轨迹扩散模型中引入类似图像的动态裁剪机制，以稳定多目标引导过程？
- **端到端扩散动画**：能否将扩散模型扩展到完整的低层人体动画控制，而不仅是轨迹层面？
- **复杂人群互动**：如何进一步提升智能体之间的互动建模，以处理复杂人群行为（如分组、排队、避让礼仪）？
- **实时采样**：是否可以通过知识蒸馏、一致性模型或更轻量架构实现轨迹扩散的实时采样？
- **跨域迁移**：TRACE 在合成数据（ORCA）和真实数据（nuScenes）上的混合训练策略能否推广到其他传感器模态或文化背景下的行人行为？

## 原文 PDF

![[paperPDFs/CVPR_2023/Trace_and_Pace_Controllable_Pedestrian_Animation_via_Guided_Trajectory_Diffusion.pdf]]
