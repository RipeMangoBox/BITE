---
title: "Morph: A Motion-free Physics Optimization Framework for Human Motion Generation"
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/Morph_A_Motion_free_Physics_Optimization_Framework_for_Human_Motion_Generation.pdf
project_link: "https://interestingzhuo.github.io/Morph-Page/"
code_link: null
aliases:
- Morph
tags:
- ICCV_2025
- topic/motion_animation
- topic/motion_animation/human_motion_generation
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 利用预训练生成器产生的大量含噪合成运动数据，代替真实数据训练一个运动物理精炼模块（MPR），该模块在物理仿真器中通过强化学习将噪声运动投影到物理合理空间，并引入运动VAE先验奖励以保持运动分布；精炼后的数据再用于微调生成器，从而形成无需真实数据的、生成与精炼互相促进的闭环。
primary_logic: 预训练生成器虽输出物理不合理的运动，但其多样性与规模足以替代真实数据训练一个物理精炼模块；该模块在仿真器中通过模仿学习与先验奖励约束，能在提升物理合理性的同时保留原运动分布特性；将精炼后的数据反向优化生成器，可使生成器与精炼模块在多轮迭代中持续互相增强，实现物理合理性与生成质量的同步提升。
claims:
- 仅使用生成器合成的噪声数据训练MPR模块是可行的，并且由于真实数据与生成数据之间存在域差距，使用真实数据反而导致性能衰减。
- 先验奖励对保持运动分布至关重要，移除先验奖励会导致FID剧烈恶化，说明没有先验约束的精炼运动偏离了原运动分布。
- Morph-MDM 将渗透（Penetrate）完全消除（23.152→0.000），漂浮（Float）从 17.502 降至 2.258，滑动（Skate）从 3.540 降至 0.016。
- 多轮交替训练MG与MPR可进一步改善性能，三轮优化后FID降至0.034，PFC降至0.618，达到最佳效果。
---

# Morph: A Motion-free Physics Optimization Framework for Human Motion Generation

> [!tip] 核心洞察
> 预训练生成器虽输出物理不合理的运动，但其多样性与规模足以替代真实数据训练一个物理精炼模块；该模块在仿真器中通过模仿学习与先验奖励约束，能在提升物理合理性的同时保留原运动分布特性；将精炼后的数据反向优化生成器，可使生成器与精炼模块在多轮迭代中持续互相增强，实现物理合理性与生成质量的同步提升。

| 字段 | 内容 |
|------|------|
| 中文题名 | Morph：一种无需真实运动数据的人体动作生成物理优化框架 |
| 英文题名 | Morph: A Motion-free Physics Optimization Framework for Human Motion Generation |
| 会议/期刊 | ICCV 2025 |
| Links | [paper](https://arxiv.org/abs/2411.14951) · [Project](https://interestingzhuo.github.io/Morph-Page/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Morph |
| Dataset | HumanML3D, AIST++ |

> [!tip] 效果简介
> - HumanML3D 上，Penetrate↓ 0.000 vs 23.152 (-100%)；Float↓ 2.141 vs 10.660 (-79.9%)；Skate↓ 0.010 vs 5.262 (-99.8%)。
> - AIST++ 上，Penetrate↓ 0.000 vs N/A (EDGE alone) (completely eliminated)。

## 概述

现有动作生成模型普遍忽略物理约束，导致生成的动作为现漂浮、脚滑、穿透等物理伪影（Figure 1）。如何在不依赖昂贵真实运动数据的条件下训练有效的物理优化器，是该领域尚未解决的瓶颈。

Morph 提出了一种无需真实运动数据的物理优化框架。其核心思路是：利用预训练生成器产生的大规模含噪合成运动数据，替代真实数据训练一个运动物理精炼模块（Motion Physics Refinement, MPR）；该模块在物理仿真器中通过强化学习将噪声运动投影到物理合理空间，并引入运动 VAE 先验奖励以保持运动分布；精炼后的数据再用于微调生成器，从而形成生成与精炼互相促进的闭环。

实验表明，Morph 在文本到动作（HumanML3D）和音乐到舞蹈（AIST++）两个任务上均显著改善了物理合理性：渗透（Penetrate）完全消除，漂浮（Float）和滑动（Skate）降低一个数量级以上，同时生成质量指标（FID、R-Precision）保持竞争性甚至略有提升。用户研究中，Morph 在物理合理性维度以 97.5% 的胜率显著优于基线。多轮交替训练可进一步使 FID 降至 0.034，PFC 降至 0.618，验证了生成器与精炼模块相互增强的机制。

在方法谱系上，Morph 区别于 **PhysDiff**（Yu et al., 2023）等将物理优化嵌入扩散过程的方法，提出了两阶段协同训练范式：先训练 MPR 精炼噪声运动，再用精炼数据微调生成器。其先验奖励机制采用轻量运动 VAE 提供平滑稳定的分布约束，避免了对抗性奖励的不稳定性。该方法可即插即用地与多种生成器（扩散、自回归、掩码建模）结合，展现出良好的通用性。

## 背景与动机

### 物理伪影：动作生成中被忽视的瓶颈

文本到动作生成领域近年来取得了显著进展，扩散模型、自回归模型和掩码建模等方法在生成多样性和文本匹配度上不断刷新记录。然而，几乎所有现有方法都共享一个隐含假设：只要生成的动作“看起来像”真实数据分布中的样本，它就是合理的。这一假设导致了一个系统性问题——**物理伪影**的普遍存在。

Figure 1 展示了典型的问题模式：生成的人物动作出现漂浮（双脚离地悬空）、脚滑（足部在地面滑动而非稳定支撑）、身体倾斜角度违反重力约束，以及肢体穿透（身体部件相互穿插）。这些伪影并非个别方法的缺陷，而是源于一个更深层的瓶颈：**现有动作生成模型普遍忽略物理约束**，其优化目标仅关注运动学层面的数据分布匹配，而不考虑动力学可行性。

### 现有方案的困境：物理优化依赖真实数据

针对这一问题，已有工作尝试将物理约束引入生成流程。代表性方法如 **PhysDiff**（Yu et al., 2023）将物理优化嵌入扩散去噪过程，通过多步迭代将噪声运动投影到物理合理空间。然而，这类方法存在一个关键限制：**它们依赖真实运动数据来训练物理优化器**。

真实运动数据的获取成本极高——需要专业动捕设备和演员，且难以覆盖所有动作类型。更根本的是，真实数据与生成器输出的合成数据之间存在显著的**域差距**（domain gap）：物理优化器在真实数据上训练后，面对生成器产生的噪声运动时，泛化能力受限。这形成了一个“先有鸡还是先有蛋”的困境：要训练物理优化器需要真实数据，而真实数据既昂贵又与目标域不匹配。

### 核心动机：用合成数据替代真实数据

本文的核心洞察在于打破上述循环：**预训练生成器虽输出物理不合理的运动，但其多样性与规模足以替代真实数据来训练物理精炼模块**。这一思路的可行性建立在两个观察之上：

1. **数据量优势**：预训练生成器可以近乎零成本地产生大规模合成运动数据，其数量远超可获取的真实动捕数据。
2. **闭环互促潜力**：一旦物理精炼模块在合成数据上训练完成，它可以将噪声运动投影到物理合理空间；这些精炼后的数据反过来可以用于微调生成器，使生成器输出本身更接近物理合理分布，进而在下一轮为精炼模块提供更高质量的输入。

这一“生成-精炼-反哺”的闭环机制，使得系统可以在**无需任何真实运动数据**的条件下，实现物理合理性与生成质量的同步提升。这正是 Morph 框架的核心动机：构建一个运动无关（Motion-Free）的物理优化框架，让物理约束的施加不再受制于昂贵的数据获取成本。

## 核心创新

Morph 的核心创新在于构建了一个**无需真实运动数据的闭环物理优化框架**，通过三个关键机制改变了现有动作生成中物理约束的施加方式。

### 创新一：以合成噪声数据替代真实数据训练物理精炼模块

现有物理优化方法（如 **PhysDiff**，Yu et al., 2023）依赖真实运动数据嵌入物理约束，使得成本高昂且泛化受限。Morph 的核心突破在于发现并验证了一个关键事实：**预训练生成器产生的含噪合成运动数据足以替代真实数据训练物理精炼模块（MPR）**，甚至由于真实数据与生成数据之间存在域差距，使用真实数据反而导致性能衰减。

消融实验（Table 1）直接证实了这一点：仅使用合成数据训练的模型 F 在所有物理指标上优于使用真实数据的模型 G，同时保持了有竞争力的生成指标。这一发现使得整个框架摆脱了对昂贵真实运动捕捉数据的依赖，从根本上改变了物理优化的数据范式。

### 创新二：运动 VAE 先验奖励替代对抗式分布约束

在强化学习驱动的物理仿真中，如何约束仿真动作不偏离原始运动分布是一个核心难题。现有方法多采用对抗性奖励（adversarial reward），但训练不稳定且容易导致模式坍塌。Morph 提出了**轻量运动 VAE 作为先验奖励模型**，通过学习连续时间步状态差值的分布，提供平滑且稳定的分布约束信号。

消融实验表明，移除先验奖励（模型 D）会导致 FID 指标显著恶化，说明没有先验约束的精炼运动会偏离原运动分布。这一设计以较小的计算代价（轻量 VAE）换取了物理优化过程中的分布稳定性，是该框架能够有效工作的关键保障。

### 创新三：生成器与精炼模块的多轮协同优化

不同于 **PhysDiff** 将物理优化嵌入扩散过程的多步迭代，Morph 采用**两阶段协同训练策略**：第一阶段利用生成器产生的大规模噪声运动训练 MPR 模块，第二阶段将物理精炼后的数据用于微调生成器。更重要的是，这两个阶段可以多轮交替进行，形成生成与精炼互相增强的正反馈闭环。

实验证实，三轮优化后性能达到最佳（FID 降至 0.034，PFC 降至 0.618），表明生成器在精炼数据的微调下能够学会产生更物理合理的运动，而更合理的生成运动又为 MPR 提供了更好的训练数据，实现了**无需真实数据的自我提升**。

### 创新边界与局限

需要指出的是，当前框架仅适用于地面接触动作（如行走、跑步），对于涉及环境交互的动作（如坐椅子、游泳），MPR 模块无法在仿真器中复现，需借助模仿选择操作过滤。此外，框架的有效性依赖于生成器产生的合成数据质量，且物理仿真与强化学习训练需要较高计算资源（8 块 Tesla V100 GPU）。这些限制为后续研究指明了方向。

## 整体框架

Morph 框架的核心思想是**在无需真实运动数据的前提下，通过生成器与物理精炼模块的协同训练，实现物理合理性与生成质量的双向提升**。其整体架构由两个关键模块构成，并通过两阶段训练流程形成闭环。

### 模块组成

**运动生成器（Motion Generator, MG）** 可以是任意现成的动作生成模型（如扩散模型、自回归模型或掩码建模模型），其作用是根据条件信号 $c$（文本或音乐）生成运动序列：

$$\tilde{\pmb{x}}^{1:L} = f_{\xi}(c)$$

其中每帧 $\tilde{\pmb{x}}^{l} = [\pmb{\theta}^{l}, \pmb{p}^{l}]$ 包含关节旋转和位置信息。预训练生成器虽能产生语义相关的动作，但普遍存在漂浮、脚滑、穿透等物理伪影。

**运动物理精炼模块（Motion Physics Refinement, MPR）** 是整个框架的核心创新，由三个子组件构成：

- **运动模仿者（Motion Imitator）**：基于强化学习的控制策略，驱动物理仿真器中的人形角色模仿输入运动。
- **物理仿真器（Physics Simulator）**：提供真实的物理约束环境，确保输出动作满足接触力、重力等基本物理规律。
- **运动先验奖励模型（Motion Prior Reward Model）**：一个轻量的运动 VAE，用于提供平滑稳定的分布约束信号，防止精炼后的运动偏离原始运动分布。

MPR 的奖励函数由三部分组成：模仿奖励 $r_{\mathrm{m}}^{l}$ 鼓励仿真动作在关节旋转、位置、速度、角速度上逼近输入动作；能量惩罚 $r_{\mathrm{e}}^{l} = -0.0005 \cdot \|\hat{\pmb{\nu}}^{l} \hat{\pmb{\omega}}^{l}\|_{2}^{2}$ 抑制高频抖动；先验奖励 $r_{p}^{l}$ 基于运动 VAE 的状态差值重建距离，引导仿真动作保持自然性。

### 两阶段训练流程

**阶段一：MPR 模块训练。** 预训练生成器根据训练集条件信号批量生成大规模含噪合成运动数据，这些数据被送入 MPR 模块。MPR 在物理仿真器中通过强化学习将噪声运动投影到物理合理空间，同时利用运动 VAE 先验奖励约束运动分布。此阶段仅训练 MPR，生成器参数冻结。

**阶段二：生成器微调。** MPR 精炼后的物理合理运动数据被用于微调运动生成器，微调损失为均方误差：

$$\mathcal{L}_{\mathrm{MG}}(\xi) = \mathbb{E}\left[\|\pmb{x}^{1:L} - f_{\xi}(\pmb{c})\|_{2}^{2}\right]$$

在微调前，框架引入**模仿选择操作（Imitation Selection Operation）**：基于 MPJPE 阈值 $\tau$ 过滤非地面接触动作（如坐、游泳等），仅将物理优化成功的样本送入生成器微调，避免低质量精炼数据污染生成器。

### 多轮协同优化

两阶段训练可迭代进行多轮：上一轮微调后的生成器产生质量更高的合成数据，用于训练更强的 MPR；更强的 MPR 又能产生更高质量的精炼数据，进一步优化生成器。实验表明，三轮交替训练后性能达到最优（FID 降至 0.034，PFC 降至 0.618），验证了生成器与精炼模块互相增强的正反馈机制。

### 推理流程

推理时，给定条件信号 $c$，运动生成器首先生成含噪声运动序列，随后 MPR 模块将其投影为物理合理运动，最终输出兼顾语义一致性与物理真实性的动作序列。对于非地面接触的动作类型，模仿选择操作在推理阶段同样生效，将其直接交由生成器输出而不经过物理精炼。

### 补充图表

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/002_Figure_2.jpg]]
*Figure 2: An overview of the Morph framework. Morph comprises a Motion Generator and a Motion Physics Refinement module. Morph employs a two-stage training process: Motion Physics Refinement module training and Motion Generator fine-tuning. And a Imitation Selection Operation is employed to ensure the motion quality after physics refinement. The solid curved arrows on the left and right (in orange and green) represent the iterative, collaborative optimization between Stage 1 and Stage 2*

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/001_Figure_1.jpg]]
*Figure 1: Examples of physical inconsistencies in generations*

## 核心模块与公式推导

Morph 框架由两个核心模块构成：**运动生成器（Motion Generator, MG）** 与 **运动物理精炼模块（Motion Physics Refinement, MPR）**。二者通过两阶段训练形成闭环，无需真实运动数据即可实现物理合理性的持续提升。

### 运动生成器（MG）

MG 可以是任意预训练的文本到动作或音乐到舞蹈生成模型。给定条件信号 $c$（如文本描述或音乐特征），MG 输出 $L$ 帧的合成运动序列：

$$\tilde{\pmb{x}}^{1:L} = f_{\xi}(c), \quad \text{where} \quad \tilde{\pmb{x}}^{1:L} = \left\{ \tilde{\pmb{x}}^{l} = [\pmb{\theta}^{l}, \pmb{p}^{l}] \right\}_{l=1}^{L}$$

其中 $f_{\xi}$ 为参数 $\xi$ 下的生成器，每帧 $\tilde{\pmb{x}}^{l}$ 包含关节旋转 $\pmb{\theta}^{l}$ 和关节位置 $\pmb{p}^{l}$。这些合成运动虽具有多样性，但普遍存在漂浮、脚滑、穿透等物理伪影，这正是 MPR 模块要解决的问题。

### 运动物理精炼模块（MPR）

MPR 模块由三个组件构成：**运动模仿者（Motion Imitator）**、**物理仿真器（Physics Simulator）** 和 **运动先验奖励模型（Motion Prior Reward Model）**。其核心机制是在物理仿真器中将 MG 输出的含噪运动投影到物理合理空间，通过强化学习进行精炼。

#### 模仿奖励

模仿奖励鼓励仿真动作在多个运动学维度上逼近输入动作，是 MPR 训练的基础信号：

$$r_{\mathrm{m}}^{l} = w_{\theta} \exp\left[ -\alpha_{\theta} |\tilde{\theta}^{l} - \hat{\theta}^{l}| \right] + w_{p} \exp\left[ -\alpha_{p} |\tilde{p}^{l} - \hat{p}^{l}| \right] + w_{v} \exp\left[ -\alpha_{v} |\tilde{\pmb{v}}^{l} - \hat{\pmb{v}}^{l}| \right] + w_{\omega} \exp\left[ -\alpha_{\omega} |\tilde{\pmb{\omega}}^{l} - \hat{\pmb{\omega}}^{l}| \right]$$

其中 $\tilde{\cdot}$ 表示输入运动（MG 输出），$\hat{\cdot}$ 表示仿真器产生的运动，四项分别对关节旋转、位置、线速度和角速度进行指数衰减型奖励，$w$ 和 $\alpha$ 为各类别的权重与敏感度系数。

#### 能量惩罚

为抑制仿真过程中产生的高频抖动，引入能量惩罚项：

$$r_{\mathrm{e}}^{l} = -0.0005 \cdot \left\| \hat{\pmb{\nu}}^{l} \hat{\pmb{\omega}}^{l} \right\|_{2}^{2}$$

该惩罚对关节力矩 $\hat{\pmb{\nu}}^{l}$ 与角速度 $\hat{\pmb{\omega}}^{l}$ 的 L2 范数施加负奖励，使仿真动作更加平滑自然。消融实验表明，去除能量奖励会导致生成指标下降，验证了其对抑制抖动的有效性。

#### 运动先验奖励

仅靠模仿奖励容易使仿真动作偏离原运动分布。为此，Morph 引入一个轻量运动 VAE 作为先验奖励模型。该 VAE 学习连续时间步状态差值 $\Delta\mathbf{s}$ 的分布：

$$\mathcal{L}(\boldsymbol{\theta}, \boldsymbol{\phi}; \mathbf{s}) = \mathbb{E}_{q_{\phi}(\mathbf{z}|\Delta\mathbf{s})} \left[ \log p_{\theta}(\Delta\mathbf{s}|\mathbf{z}) \right] - D_{\mathrm{KL}} \left( q_{\phi}(\mathbf{z}|\Delta\mathbf{s}) \parallel p(\mathbf{z}) \right)$$

基于训练好的 VAE，先验奖励定义为仿真动作状态差值与 VAE 重建状态差值之间的 L1 距离的 Sigmoid 变换：

$$r_{p}^{l} = 1 - \frac{1}{1 + e^{-||\Delta\overline{s} - \Delta s||}}$$

其中 $\Delta\overline{s}$ 为 VAE 重建的状态差值，$\Delta s$ 为仿真器产生的状态差值。该奖励引导仿真动作保持在自然运动分布内，消融实验中移除先验奖励导致 FID 剧烈恶化，证实了其对分布约束的关键作用。

### 生成器微调

MPR 精炼后的物理合理运动被用于微调生成器，采用均方误差损失：

$$\mathcal{L}_{\mathrm{MG}}(\boldsymbol{\xi}) = \mathbb{E}\left[ \left\| \boldsymbol{x}^{1:L} - f_{\boldsymbol{\xi}}(\boldsymbol{c}) \right\|_{2}^{2} \right]$$

其中 $\boldsymbol{x}^{1:L}$ 为 MPR 输出的精炼运动序列。通过该损失，生成器学会直接输出物理合理性更高的动作，从而在推理时无需再经过仿真器，大幅降低部署成本。

### 模仿选择操作

对于坐、游泳、爬楼梯等非地面接触动作，当前物理仿真器无法正确模拟。Morph 通过**模仿选择操作（Imitation Selection Operation）** 过滤此类动作：基于 MPJPE（平均关节位置误差）阈值 $\tau$ 判断物理精炼是否成功，仅将精炼成功的样本送入生成器微调。超参数分析表明 $\tau=0.5$ 可在生成质量与物理合理性之间取得最佳平衡。

### 补充图表

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/008_Figure_4.jpg]]
*Figure 4: A flowchart illustrating the data preprocessing process. The parameters are calculated from the first frame and then applied to all generated motion sequences before they are fed into the MPR module*

## 实验与分析

### 主结果：物理指标的跨越式改善

Morph 在 HumanML3D 文本到动作任务上展现出对物理伪影的根本性消除。以 MoMask 为基线的 Morph-MoMask（Model H）将渗透（Penetrate）从 23.152 降至 **0.000**，完全消除了身体部件相互穿透的问题；漂浮（Float）从 10.660 降至 2.141，降幅达 79.9%；滑动（Skate）从 5.262 降至 0.010，降幅达 99.8%。综合物理度量 PFC 从 1.058 降至 0.647，降幅 38.8%（Table 1）。

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/003_Table_1.jpg]]
*Table 1: Ablation study on Morph-MoMask (combined with MoMask [6] generator) for text-to-motion task on HumanML3D dataset. IS: imitation selection operation; Prior: using prior reward training MPR module; Adv: using adversarial reward training MPR module; Energy: using energy reward training MPR module; Real Data: using real motion data training MPR module; FT: fine-tuning Motion Generator with physics-refined motions. The arrows (↑ / ↓) indicate that higher/smaller values are better*

关键的是，这种物理改善并未以牺牲生成质量为代价。Morph-MoMask 的 FID 从 0.045 进一步优化至 0.041，RTOP-3 从 0.807 提升至 0.816，证明物理精炼后的数据反向微调生成器能够同时提升物理合理性与语义对齐度。

在 AIST++ 音乐到舞蹈任务上，Morph-EDGE 同样将渗透降至 0.000，漂浮降至 3.519，滑动降至 0.009，验证了框架的跨任务泛化能力。

### 消融实验：核心组件的因果链路

Table 1 的系统消融揭示了各组件的作用机制：

**先验奖励是不可或缺的分布约束。** 移除先验奖励的 Model D 在 FID 上出现显著恶化，表明缺乏先验约束的仿真运动会偏离原始运动分布，产生虽物理合理但语义扭曲的动作。这验证了运动 VAE 先验模型在保持生成多样性中的关键作用。

**合成数据优于真实数据。** Model F（仅用生成器合成数据训练 MPR）在所有物理指标上优于 Model A（原始 MoMask），而使用真实运动数据训练 MPR 的 Model G 性能反而下降。这一反直觉结果揭示了真实数据与生成数据之间存在显著的域差距——MPR 在推理时面对的是生成器输出的含噪运动，用同源数据训练才能获得最佳的域内精炼能力。

**能量奖励抑制高频抖动。** 移除能量惩罚的 Model E 在生成指标上弱于完整版 Model F，说明对关节力矩和角速度的 L2 惩罚（公式 $r_{\mathrm{e}}^{l} = -0.0005 \cdot \| \hat{\pmb{\nu}}^{l} \hat{\pmb{\omega}}^{l} \|_{2}^{2}$）有效抑制了仿真中的高频抖动，使精炼后的运动更自然。

**生成器微调是性能提升的放大器。** 对比 Model F（仅 MPR 精炼，不微调生成器）与 Model H（MPR 精炼 + 生成器微调），后者在物理指标和生成指标上均有进一步提升。这说明用精炼数据微调生成器使生成器学会了产生物理更合理的动作，而不仅仅是依赖后处理修复。

### 多轮优化：生成器与精炼器的协同进化

Table 7 展示了 MPR 与生成器交替训练的效果。单轮优化已显著改善性能，而三轮优化后达到最佳：FID 降至 0.034，PFC 降至 0.618。这一结果验证了框架的核心洞察——生成器与物理精炼模块可以在多轮迭代中相互增强，形成正向反馈循环。每一轮中，经过上轮微调的生成器产生质量更高的合成数据，进而训练出更强的 MPR 模块，后者再为下一轮生成器微调提供更优质的精炼数据。

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/013_Table_7.jpg]]
*Table 7: Comparison of text-to-motion with multi-round optimization of the MPR module and motion generator based on Morph-MoMask. We set τ as 0.5 and use the total number of generated noisy motion data to train*

### 合成数据规模与数据增强效应

Table 6 显示，增大 MPR 训练所用的合成噪声运动数据量可同时改善生成指标和物理合理性指标。这一发现进一步证实了合成数据的“数据增强”作用——预训练生成器虽输出物理不合理的运动，但其多样性与规模足以替代真实数据训练物理精炼模块，且更大的数据量带来更好的精炼效果。

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/012_Table_6.jpg]]
*Table 6: Comparison of text-to-motion with different amounts of noisy motion data training for Morph-MoMask† (combined with MoMask [6] motion generator, without fine-tuning motion generator). N refers to the total number of generated noisy motion data samples, which is three times the amount of the original real training data. D refers to the number of generated motion data used to train the MPR module. We set τ as 0.5 for testing*

### 模仿选择阈值的权衡

Table 5 对模仿选择阈值 τ 的分析表明，τ = 0.5 在生成质量与物理合理性之间取得了最佳平衡。较低的阈值会过度过滤精炼样本，减少用于微调生成器的有效数据量；较高的阈值则可能引入物理优化不完全的样本，损害整体物理指标。这一操作本质上是一个质量-数量权衡机制。

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/011_Table_5.jpg]]
*Table 5: Hyper-parameter analysis of τ in Imitation Selection operation. Comparison with different values of τ based on Morph-MoMask† (combined with MoMask [6] motion generator, without fine-tuning motion generator) for text-to-motion task on HumanML3D dataset. The arrows (↑ / ↓) indicate that higher/smaller values are better*

### 跨生成器泛化

Table 2 将 Morph 与多种类型生成器结合——扩散模型（MotionDiffuse、MDM）、自回归模型（T2M-GPT）、掩码建模（MoMask）——均取得一致的物理指标改善。这表明 MPR 模块作为即插即用的物理精炼组件，对生成器的具体架构不敏感，具有广泛的适用性。

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/004_Table_2.jpg]]
*Table 2: Comparison results for text-to-motion task on HumanML3D dataset. Morph is combined with different types of motion generators. MG: Motion Generator; MPR: Motion Physics Refinement module; FT: fine-tuning motion generator with the physics-refined motion data. † denotes Morph without fine-tuning the motion generator (only Stage 1 training)*

### 用户研究

Table 8 的用户研究提供了感知层面的验证：Morph-MoMask 在物理合理性维度以 **97.5%** 的胜率显著优于 MoMask 基线。这一极端高的胜率与客观物理指标中渗透降至零、滑动降至近零的结果相互印证，说明物理指标的改善确实转化为人类可感知的质量提升。

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/010_Table_8.jpg]]
*Table 8: The win rate of Morph over baselines*

### 失败模式与局限

尽管物理指标改善显著，Morph 仍存在明确的应用边界。当前的物理仿真器无法复现非地面接触动作（如坐椅子、游泳、爬楼梯），因此方法依赖模仿选择操作过滤此类动作。这意味着对于涉及环境交互的动作类型，Morph 无法提供物理优化，限制了其在更广泛动作生成场景中的应用。

此外，物理仿真和强化学习训练需要较高计算资源（8 块 Tesla V100 GPU），且框架的有效性依赖于生成器产生的合成数据质量——若生成器本身偏差过大，可能影响 MPR 的训练效果。这些局限指向了未来的改进方向：扩展仿真器以支持环境交互、探索更轻量的物理仿真方案、以及研究多轮优化的自动收敛判定策略。

### 补充图表

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/005_Table_3.jpg]]
*Table 3: Comparison results on common generation metrics for text-to-motion on HumanML3D dataset*

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/006_Table_4.jpg]]
*Table 4: Comparison results for music-to-dance on AIST++ dataset. † denotes Morph without fine-tuning motion generator*

![[assets/figures/papers/arxiv_2024_morph_2411_14951/figures/015_Table_9.jpg]]
*Table 9: Cross-Task generalization results on Music2Dance and Text2Motion*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

Morph 的核心贡献在于提出了一种**无需真实运动数据的物理优化范式**，这使其在方法谱系中占据了一个独特的位置。现有工作可沿两个维度进行定位：物理约束的施加方式，以及对真实运动数据的依赖程度。

**与物理感知运动生成方法的关系。** 早期工作如 **PhysDiff**（Yu et al., 2023）将物理约束嵌入扩散模型的去噪过程，通过多步迭代投影来修正生成动作中的物理伪影。**Reindiffuse** 采用了类似的扩散过程内嵌物理优化的思路。这些方法的核心瓶颈在于：物理优化步骤必须与扩散采样的时间步耦合，且优化过程本身依赖于在真实运动数据上训练的物理先验。Morph 则将物理优化从生成过程中解耦，构建了独立的 Motion Physics Refinement（MPR）模块——该模块在物理仿真器中通过强化学习将噪声运动投影到物理合理空间。这种解耦设计使得物理优化可以独立于生成器的具体架构（扩散、自回归、掩码建模）运行，赋予了 Morph 即插即用的模型无关特性。

**与物理仿真模仿学习的关系。** MPR 模块中的运动模仿者借鉴了物理角色控制（Physics-based Character Control）领域的方法，如 **PHC** 等工作的模仿学习框架。但关键区别在于：传统物理模仿方法需要真实运动捕捉数据作为模仿目标，而 Morph 的 MPR 模块**仅使用生成器合成的含噪运动数据**进行训练。消融实验（Table 1, Model G vs. Model F）证实了这一设计的必要性：当使用真实运动数据训练 MPR 时，由于真实数据与生成数据之间存在显著的域差距（domain gap），物理指标反而出现性能衰减。这一发现构成了 Morph 方法论的核心洞见——预训练生成器的输出虽然包含物理伪影，但其多样性与规模足以替代真实数据训练物理精炼模块。

**与运动先验建模的关系。** 为在物理优化过程中保持运动分布的自然性，Morph 引入了轻量运动 VAE 作为先验奖励模型。这与使用对抗性奖励（adversarial reward）的方法形成对比。消融实验（Table 1, Model D vs. Model F）表明，移除先验奖励会导致 FID 指标剧烈恶化，证明对抗性奖励无法提供足够稳定的分布约束信号。Morph 的运动 VAE 在连续时间步的状态差值上建模，提供平滑且稳定的先验奖励，这是保持精炼后运动语义一致性的关键机制。

### 2. 适用边界

**生成器架构兼容性。** Morph 在三种主流生成范式上进行了验证：扩散模型（**MDM**，Tevet et al., 2023；**MotionDiffuse**，Zhang et al., 2022）、自回归模型（**T2M-GPT**，Zhang et al., 2023）和掩码建模（**MoMask**，Guo et al., 2024）。在 HumanML3D 文本到动作任务上，Morph 与上述生成器结合后均显著提升了物理合理性指标，同时保持了生成质量（Table 2）。在音乐到舞蹈任务上，Morph 同样成功适配了扩散模型 **EDGE**（Tseng et al., 2023）和自回归模型 **Bailando**（Siarohin et al., 2022），在 AIST++ 数据集上实现了物理伪影的大幅削减（Table 4）。这表明 Morph 的模型无关设计具有较广的适用性。

**任务域适用性。** 当前验证集中于两个主流任务：文本到动作生成（HumanML3D）和音乐到舞蹈生成（AIST++）。跨任务泛化实验（Table 9）进一步表明，在音乐到舞蹈任务上训练的 MPR 模块可直接应用于文本到动作任务，反之亦然，说明物理精炼能力具有一定的任务迁移性。

**动作类型限制。** Morph 的适用边界受限于物理仿真器的能力。当前的仿真器无法复现非地面接触动作（如坐椅子、游泳、爬楼梯），因此方法必须依赖**模仿选择操作**（Imitation Selection Operation）过滤此类动作——基于 MPJPE 阈值 $\tau$ 判断物理优化是否成功，仅将成功的样本送入生成器微调。这意味着 Morph 在涉及环境交互和物体操作的动作类型上存在明确的应用限制。

### 3. 局限与开放问题

**物理仿真器的能力瓶颈。** 当前框架的核心局限在于物理仿真器无法处理非地面接触动作。这不仅是训练阶段的约束（需要过滤交互性动作的文本标注），也是推理阶段的限制——对于涉及坐、游泳等动作的生成结果，Morph 无法提供物理优化。如何扩展框架以处理包含环境交互和物体操作的动作，是该方向最紧迫的开放问题。

**合成数据质量依赖。** MPR 模块的训练完全依赖于生成器产生的合成数据。消融实验（Table 6）表明，增大噪声运动数据量可提升 MPR 性能，这证实了合成数据的数据增强作用。但这也意味着：若生成器本身偏差过大，可能影响 MPR 的训练效果。该依赖关系需要进一步量化分析。

**计算资源需求。** 虽然 Morph 无需昂贵的真实运动捕捉数据，但物理仿真和强化学习训练仍需要较高计算资源——论文使用 8 块 Tesla V100 GPU 进行训练。能否将 MPR 模块与更轻量的物理仿真器结合以降低推理成本，是实用化部署的关键问题。

**多轮优化的收敛策略。** Morph 的多轮交替训练（MG 与 MPR 互相优化）在三轮时达到最佳性能（Table 7：FID 0.034，PFC 0.618），但论文未给出自动判断收敛的机制。多轮优化的最佳停止策略，以及生成器微调阶段是否可能引入灾难性遗忘、如何保持原有生成多样性，仍是未充分探索的问题。

**泛化到更多角色模型。** 当前验证基于单一的人体角色模型。在不同仿真器或更复杂的角色模型（如不同体型、非人形角色）上，该方法的有效性仍需验证。

## 原文 PDF

![[paperPDFs/ICCV_2025/Morph_A_Motion_free_Physics_Optimization_Framework_for_Human_Motion_Generation.pdf]]
