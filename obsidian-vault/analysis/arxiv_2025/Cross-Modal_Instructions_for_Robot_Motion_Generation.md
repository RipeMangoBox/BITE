---
title: Cross-Modal Instructions for Robot Motion Generation
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Cross-Modal_Instructions_for_Robot_Motion_Generation.pdf
project_link: null
code_link: null
aliases:
- CMIRMG
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 通过层次化精度耦合，将大型视觉语言模型的高层推理与小型微调视觉语言模型的像素级精确定位相结合，形成从指令到3D轨迹的端到端管道。
primary_logic: 将跨模态指令视为上下文学习示例，利用推理模型生成关键点描述，再由微调模型精确定位，并通过多视图射线投影将2D轨迹提升为3D运动轨迹，从而实现无需物理演示的机器人行为生成。
claims:
- 在RLBench篮球投篮任务上，CrossInstruct达到0.90成功率，而纯RL方法SAC/TD3均无法从零开始获得非零回报。
- 由CrossInstruct初始化的策略在Jenga任务上收敛到约90%成功率，而从零训练的方法无法获得非零回报。
- 在8项RLBench任务中，CrossInstruct大幅优于无精度耦合的VLM推理基线和从零训练的RL方法。
- RLBench Basketball in Hoop 上 Success rate = 0.90
---

# Cross-Modal Instructions for Robot Motion Generation

> [!tip] 核心洞察
> 将跨模态指令视为上下文学习示例，利用推理模型生成关键点描述，再由微调模型精确定位，并通过多视图射线投影将2D轨迹提升为3D运动轨迹，从而实现无需物理演示的机器人行为生成。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于跨模态指令的机器人运动生成 |
| 英文题名 | Cross-Modal Instructions for Robot Motion Generation |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2509.21107) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | CrossInstruct |
| Dataset | RLBench Basketball in Hoop, RLBench Jenga, RL Jenga, RL Peg insertion |

> [!tip] 效果简介
> - RLBench Basketball in Hoop 上，Success rate 0.90 vs 0 (SAC/TD3 from scratch) (+0.90)。
> - RLBench Jenga (policy execution) 上，Success rate 0.55 vs 0 (SAC/TD3 from scratch) (+0.55)。
> - RL Jenga (RL fine-tuning) 上，Success rate ~90% vs 0 (training from scratch) (+90%)。

## 概述

机器人从人类指令中生成可执行运动，传统上依赖大量物理演示，成本高昂且难以泛化。跨模态指令（草图、文本标签等）提供了一种更自然的交互方式，但现有方法面临一个关键瓶颈：大型视觉语言模型（VLM）擅长高层语义推理，却缺乏精确的空间定位能力，导致生成的轨迹无法可靠地作用于目标物体。

**CrossInstruct** 针对这一瓶颈提出了层次化精度耦合方案。其核心思路是将跨模态指令视为上下文学习示例，由大型推理VLM生成语义关键点描述，再委托小型微调VLM进行像素级精确定位；随后在多视图图像上生成2D轨迹，并通过射线投影将其提升为3D末端执行器轨迹分布。这一管道实现了从指令到可执行运动的端到端转换，无需任何物理演示。

实验表明，在RLBench的篮球投篮任务上，CrossInstruct达到**0.90成功率**，而纯强化学习方法（SAC、TD3）从零训练无法获得非零回报（Table I）。在Jenga任务上，CrossInstruct初始化的策略经RL微调后收敛至约**90%成功率**，同样远超从零训练的基线（Fig. 12）。消融实验进一步验证，移除精度耦合模块会导致VLM在相似颜色物体上频繁定位错误（Fig. 9, Fig. 10），证实了层次化耦合对空间准确性的关键作用。

## 背景与动机

### 问题背景：从物理演示到跨模态指令

机器人操作策略的传统范式依赖于大量物理演示数据。模仿学习（Imitation Learning）需要人类操作员反复执行任务以收集状态-动作对，而强化学习（Reinforcement Learning）则要求智能体在环境中进行数百万步的试错交互。这两种范式都面临一个根本瓶颈：**物理演示的获取成本极高**，且难以泛化到新的任务场景和视觉环境。

跨模态指令（Cross-Modal Instructions）提供了一种更自然、更低成本的替代方案。人类可以通过草图、文本标签甚至口头描述来传达操作意图，而无需实际执行物理动作。这种指令形式利用了人类的空间推理能力，将高层语义意图压缩为简洁的视觉-语言符号。然而，如何让机器人从这种稀疏、模糊的指令中生成精确的3D运动轨迹，仍然是一个开放问题。

### 现有方法缺口：语义推理与空间精度的断层

当前利用视觉语言模型（VLM）进行机器人操作的方法存在一个关键断层：**高层语义推理与像素级空间定位之间缺乏有效耦合**。

一方面，大型VLM（如GPT-4V、Gemini等）展现出强大的语义理解和任务规划能力，能够在上下文中解析跨模态指令的意图。但当它们被直接要求输出像素坐标或连续轨迹时，往往产生空间定位错误——尤其是在存在相似颜色物体、遮挡或小目标物体的场景中。如**Fig. 9**所示，无精度耦合时，VLM推理常常无法使机器人充分触及按钮、篮球或Jenga块等目标物体；**Fig. 10**进一步揭示了颜色混淆导致的轨迹错误：当场景中存在多个蓝色物体时，推理模型会错误地将轨迹锚定到相似颜色的干扰物上。

另一方面，纯强化学习方法（如**SAC**（Haarnoja et al., ICML 2018）和**TD3**（Fujimoto et al., ICML 2018））虽然能够通过环境交互学习闭环策略，但在稀疏奖励的复杂操作任务上从零训练时往往无法获得非零回报。**Table I**显示，在RLBench的篮球投篮和Jenga任务上，SAC和TD3的成功率均为0。

### 本文动机：层次化精度耦合

本文的核心动机是弥合上述断层。作者提出**CrossInstruct**框架，其核心洞见是：**将跨模态指令视为上下文学习示例，利用大型推理VLM的高层语义理解能力生成关键点描述，再将像素级精确定位委托给小型微调VLM，最后通过多视图射线投影将2D轨迹提升为3D运动轨迹**。

这种层次化精度耦合（Hierarchical Precision Coupling）的设计逻辑是：大型VLM擅长“知道要做什么”（what to do），而小型微调VLM擅长“知道在哪里做”（where to do it）。通过将这两个能力解耦并协同，CrossInstruct能够在无需任何物理演示的条件下，仅凭草图、文本等跨模态指令生成可执行的机器人运动轨迹，并泛化到新的视觉场景和任务配置中。

## 核心创新

CrossInstruct 的核心创新在于构建了一个**层次化精度耦合（Hierarchical Precision Coupling）** 的跨模态指令理解与运动生成框架，解决了传统 VLM 推理方法“高层语义理解强、低层空间定位弱”的根本矛盾。这一创新通过三个紧密耦合的 changed slots 实现。

### 从直接像素预测到语义-精度解耦的关键点定位

基线方法（如 **VLM-Reasoning / HAMSTER**，Li et al., 2025）直接让大型 VLM 输出像素坐标，导致在遮挡、小物体或颜色相似场景下频繁出现定位错误（Fig. 9, Fig. 10）。CrossInstruct 将这一过程解耦为两个阶段：

1. **推理 VLM $\mathcal{R}$ 生成语义关键点描述符**：$\mathcal{K} = \{ k_i \}_{i=1}^N$，其中 $k_i = (\ell_i, \alpha_i)$，$\ell_i$ 为自然语言标签（如“篮球中心”），$\alpha_i$ 为辅助元数据。这使大型模型专注于其擅长的高层语义推理。
2. **微调指向 VLM $\mathcal{G}$ 进行像素级精确定位**：针对每个关键点标签 $\ell_i$，在多视图图像 $I_m$ 上预测像素坐标 $\{ u_{i,m}^{(t)}, v_{i,m}^{(t)} \} = \mathcal{G}(\ell_i \mid I_m)$。小型模型经过专门微调，具备精确的 2D 指向能力。

这一解耦的核心洞察在于：**将跨模态指令视为上下文学习示例**，利用推理模型生成关键点描述，再由微调模型完成精确定位，使系统同时获得高层语义理解与低层几何精度。

### 从 2D 直接推理到多视图 3D 轨迹融合

基线方法仅使用 2D 推理，缺乏将 2D 轨迹提升为可执行 3D 运动的能力。CrossInstruct 引入**多视图射线投影（Multi-View Lifting via Ray Casting）** 机制：

1. 推理模型 $\mathcal{R}$ 结合关键点坐标，生成两个视图上的 2D 轨迹 $\xi_1, \xi_2$。
2. 每个 2D 路点被建模为图像空间中的高斯分布：$p(u_m, v_m \mid t) = \mathcal{N}((u_m, v_m) \mid \xi_m(t), \Sigma_m)$。
3. 通过标定相机参数，将像素坐标沿射线投影到 3D 空间：$f_r(u_m, v_m, d) = \mathbf{o}^m + \omega(u_m, v_m) d$。
4. 多视图射线交叉采样，将 2D 轨迹分布融合为 3D 路点高斯分布：$p(x_t \mid t) = \mathcal{N}(x_t \mid \mu_t, \Sigma_t)$，最终形成完整 3D 轨迹分布 $p(\tau \mid \xi_1, \xi_2, \mathcal{P}) = \prod_{t=1}^{H} p(x_t \mid t)$。

这一管线使 CrossInstruct 能够从多视图 2D 草图直接生成可执行的 3D 末端执行器轨迹，无需任何物理演示数据。

### 从开环轨迹到闭环策略的强化学习精炼

CrossInstruct 生成的轨迹分布不仅可直接执行，还可作为强化学习的初始化策略。通过 **TD3+BC** 损失函数：

$$\mathcal{L}_{\mathrm{actor}} = \lambda \mathbb{E}_{(s,a) \sim \mathcal{D}} [\| \pi(s) - a \|^2] - (1 - \lambda) \mathbb{E}_s [Q(s, \pi(s))]$$

该损失在行为克隆项（保持接近合成轨迹）和 Critic 最大化项（通过交互改进策略）之间取得平衡，使策略收敛到对扰动、感知噪声和分布偏移具有鲁棒性的闭环策略 $\pi^*$。

### 创新效果验证

消融实验表明，精度耦合模块在小物体或遮挡场景下价值最为显著——无精度耦合时，VLM 推理常常错误定位相似颜色的物体（Fig. 10）。在 RLBench 篮球投篮任务上，CrossInstruct 达到 0.90 成功率，而纯 RL 方法（SAC/TD3）从零训练无法获得非零回报（Table I）。在 Jenga 任务上，由 CrossInstruct 初始化的策略收敛到约 90% 成功率，而从零训练的 RL 方法完全失败（Fig. 12）。

## 整体框架

CrossInstruct 的完整管道将跨模态指令（草图、文本等）转化为机器人可执行的 3D 运动轨迹，其核心设计围绕一个关键瓶颈展开：**高层语义推理与像素级空间精确定位之间的鸿沟**。传统方法要么依赖大型 VLM 直接输出坐标（缺乏空间精度），要么需要大量物理演示来训练策略（泛化能力差）。CrossInstruct 通过**层次化精度耦合**（Hierarchical Precision Coupling）将这两个能力解耦并重新组合，形成端到端的指令到轨迹生成管道。

### 输入：跨模态指令元组

系统的输入被形式化为一个元组：

$$\mathcal{T} = \{ I, S, T \}$$

其中 $I$ 为场景图像，$S$ 为自由形式的草图（如箭头、圆圈），$T$ 为可选的文本信息。这些指令以**上下文学习示例**（in-context learning examples）的方式提供给大型推理 VLM，使其在无需参数更新的情况下理解任务意图。

### 管道四阶段

整个框架由四个顺序模块组成，数据流严格单向：

**1. 跨模态指令编码**  
将人类提供的草图、图像和文本组合为标准化元组 $\mathcal{T}$，作为后续推理的上下文输入。

**2. 层次化精度耦合模块（核心创新）**  
该模块包含两个 VLM 的分工协作：
- **推理 VLM $\mathcal{R}$**（大型模型）：承担高层任务推理。它首先生成 $N$ 个语义关键点描述符 $\mathcal{K} = \{ k_i \}_{i=1}^N$，其中 $k_i = (\ell_i, \alpha_i)$，$\ell_i$ 为自然语言标签（如“篮球中心”），$\alpha_i$ 为辅助文本元数据。随后，$\mathcal{R}$ 结合这些关键点信息生成两个视图上的 2D 轨迹。
- **指向 VLM $\mathcal{G}$**（小型微调模型）：接收 $\mathcal{R}$ 生成的关键点标签 $\ell_i$，在每个视图图像 $I_m$ 上预测精确的像素坐标 $\{ u_{i,m}^{(t)}, v_{i,m}^{(t)} \}$。

这一耦合机制的本质是**将空间精度任务从推理模型中剥离**，委托给专门微调的轻量模型，从而避免了大型 VLM 在像素级定位上的系统性偏差。

**3. 多视图射线投影器**  
将 2D 像素轨迹提升为 3D 末端执行器轨迹分布。具体步骤：
- 将每个时间步的 2D 路点建模为图像空间中的高斯分布：$p(u_m, v_m \mid t) = \mathcal{N}((u_m, v_m) \mid \xi_m(t), \Sigma_m)$
- 通过标定的多视图几何，将像素坐标沿相机射线投影到 3D 空间：$f_r(u_m, v_m, d) = \mathbf{o}^m + \omega(u_m, v_m) d$
- 对两个视图的射线进行交叉采样，融合得到 3D 路点的高斯分布：$p(x_t \mid t) = \mathcal{N}(x_t \mid \mu_t, \Sigma_t)$
- 最终输出完整的 3D 轨迹分布：$p(\tau \mid \xi_1, \xi_2, \mathcal{P}) = \prod_{t=1}^{H} p(x_t \mid t)$

**4. 策略执行与 RL 精炼**  
生成的 3D 轨迹可以直接开环执行，也可以作为离线演示数据初始化强化学习策略。CrossInstruct 采用 TD3+BC 方法，通过如下损失函数进行微调：

$$\mathcal{L}_{\mathrm{actor}} = \lambda \mathbb{E}_{(s,a) \sim \mathcal{D}} [\| \pi(s) - a \|^2] - (1 - \lambda) \mathbb{E}_s [Q(s, \pi(s))]$$

该损失使学习到的策略既保持在合成轨迹附近，又能通过 critic 引导的更新超越原始轨迹质量，最终收敛到对扰动和分布偏移鲁棒的闭环策略 $\pi^*$。

### 关键设计决策

整个管道的信息流体现了“推理-定位-融合-执行”的层次化分解：推理 VLM 负责理解任务语义并生成关键点描述，指向 VLM 负责像素级精确定位，射线投影器负责 2D 到 3D 的几何提升，RL 精炼阶段则赋予策略闭环鲁棒性。这种设计使得 CrossInstruct **无需任何物理演示**即可生成可泛化的机器人行为，从根本上区别于传统模仿学习范式。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/003_Figure_3.jpg]]
*Figure 3: An overview of CrossInstruct (left) with an example of precise pointing of keypoints (right). The hierarchical precision model coupling module enables the reasoning model to leverage a smaller fine-tuned VLM to precisely identify relevant keypoints, which then guide robot end-effector motion*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/001_Figure_1.jpg]]
*Figure 1: We enable robots to interpret cross-modal instructions, in the form of rough sketches and textual labels (shown on the left). Subsequent motion can be generated and generalized to novel setups and environments (shown on the right)*

## 核心模块与公式推导

CrossInstruct 将跨模态指令转化为可执行机器人运动轨迹，其核心由三个紧密耦合的模块构成：跨模态指令编码、层次化精度耦合模块，以及多视图射线投影器。整个管道的形式化起点是将人类提供的指令定义为一个元组：

$$\mathcal{T} = \{ I, S, T \}$$

其中 $I$ 为场景图像，$S$ 为自由形式草图集合，$T$ 为可选的文本信息。系统的目标是学习一个条件分布：

$$p(\tau \mid \mathcal{T}, \mathcal{V}, \mathcal{P}), \quad \tau = \{ (x_t, R_t, g_t) \}_{t=1}^{H}$$

其中 $\mathcal{V}$ 为多视图图像，$\mathcal{P}$ 为相机位姿，$\tau$ 为长度为 $H$ 的运动轨迹，每个时间步包含末端执行器位置 $x_t$、朝向 $R_t$ 和夹爪状态 $g_t$。

### 层次化精度耦合模块

该模块是解决“高层语义与精确空间定位脱节”这一瓶颈的关键。它通过双模型分工实现精度耦合：

1. **语义关键点生成**：大型推理 VLM $\mathcal{R}$ 首先分析跨模态指令 $\mathcal{T}$，生成 $N$ 个语义关键点描述符集合：

   $$\mathcal{K} = \{ k_i \}_{i=1}^N, \qquad k_i = (\ell_i, \alpha_i)$$

   其中 $\ell_i$ 为自然语言标签（如“篮球中心”），$\alpha_i$ 为辅助文本元数据。这一步将高层推理转化为可定位的语义锚点。

2. **像素级精确定位**：小型微调指向模型 $\mathcal{G}$ 接收每个关键点标签 $\ell_i$，在每张视图图像 $I_m$ 上预测像素坐标：

   $$\{ u_{i,m}^{(t)}, v_{i,m}^{(t)} \} = \mathcal{G}(\ell_i \mid I_m), \quad m \in \{1, 2\}$$

   这一步将语义锚点转化为精确的 2D 空间坐标，弥补了大型 VLM 在像素级定位上的不足。

3. **2D 轨迹生成**：推理模型 $\mathcal{R}$ 结合指令 $\mathcal{T}$、多视图 $\mathcal{V}$、关键点描述符 $\mathcal{K}$ 及其像素坐标，生成两个视图上的 2D 轨迹 $\xi_1, \xi_2$。

该模块的证据强度较高（confidence 0.95），其有效性在消融实验中得到验证：无精度耦合时，VLM 推理常因颜色混淆而错误定位物体（Fig. 10），在小物体或遮挡场景下尤为明显。

### 多视图射线投影器

2D 轨迹需提升为 3D 末端执行器轨迹。该模块通过标定的多视图几何完成这一转换：

1. **2D 路点概率建模**：将每个时间步 $t$ 在视图 $m$ 上的轨迹点建模为高斯分布：

   $$p(u_m, v_m \mid t) = \mathcal{N}((u_m, v_m) \mid \xi_m(t), \Sigma_m)$$

2. **射线投影**：利用相机内参，将像素坐标 $(u_m, v_m)$ 和深度参数 $d$ 映射为 3D 射线：

   $$f_r(u_m, v_m, d) = \mathbf{o}^m + \omega(u_m, v_m) d, \quad d \in [d_{\text{near}}, d_{\text{far}}]$$

   其中 $\mathbf{o}^m$ 为相机光心，$\omega(\cdot)$ 为像素到射线方向的映射函数。

3. **多视图交叉融合**：对两个视图的射线进行交叉采样，估计每个时间步的 3D 路点高斯分布：

   $$p(x_t \mid t) = \mathcal{N}(x_t \mid \mu_t, \Sigma_t)$$

   完整轨迹分布由各时间步分布连乘得到：

   $$p(\tau \mid \xi_1, \xi_2, \mathcal{P}) = \prod_{t=1}^{H} p(x_t \mid t)$$

该模块的证据强度较高（confidence 0.95），其几何原理在 Fig. 5 中有直观展示。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/007_Figure_5.jpg]]
*Figure 5: Intersecting rays from different poses*

### 策略执行与 RL 精炼

生成的轨迹分布可直接执行，也可作为强化学习的初始化。当采用 RL 精炼时，使用 TD3+BC 的演员损失函数：

$$\mathcal{L}_{\mathrm{actor}} = \lambda \mathbb{E}_{(s,a) \sim \mathcal{D}} [\| \pi(s) - a \|^2] - (1 - \lambda) \mathbb{E}_s [Q(s, \pi(s))]$$

该损失由两项加权组成：第一项为行为克隆项，使策略靠近合成轨迹；第二项为 critic 引导的优化项，使策略在保持初始行为的基础上进一步提升。通过这一机制，智能体收敛到闭环策略 $\pi^*$，对扰动、感知噪声和分布偏移具有鲁棒性。

> 注：关于 $\lambda$ 的具体取值和调参策略，原文未在分析材料中明确给出，需查阅原文进行手动验证。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/004_Figure_4.jpg]]
*Figure 4: CrossInstruct generates 2D trajectories over multi-view images (in red), which are subsequently fused into a coherent 3D trajectory (waypoints in blue-red color gradient shown). This can then be rolled out to slide the block to the target*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/005_Figure_6.jpg]]
*Figure 6: CrossInstruct uses the accurately pointed keypoints to enable accurate reasoning of orientation. Here we see an example of the robot pulling a Jenga block, which requires an accurate movement direction*

## 实验与分析

### 核心定量结果：RLBench基准任务

CrossInstruct在RLBench基准的8项任务上与VLM推理基线（**HAMSTER**，Li et al., 2025）和纯强化学习方法（**SAC**、**TD3**）进行了对比。Table I汇总了各任务的成功率。

**关键发现：**

- **篮球投篮任务**：CrossInstruct达到**0.90**成功率，而SAC和TD3从零开始训练均无法获得非零回报（成功率0）。VLM推理基线同样无法完成该任务。这一差距的根源在于篮球投篮需要将球精确放入篮筐，纯RL方法面临极度稀疏的奖励信号，而VLM推理基线缺乏像素级精确定位能力，无法准确抓取和放置篮球。

- **Jenga抽积木任务**：CrossInstruct直接执行轨迹的成功率为**0.55**，而纯RL方法从零训练的成功率为0。该任务要求机器人以精确方向拉出积木块，任何方向偏差都会导致失败。CrossInstruct通过层次化精度耦合模块生成的关键点方向信息（见Fig. 6）使轨迹具备正确的运动方向，从而获得非零成功率。

- **Peg插入任务**：CrossInstruct直接执行的成功率为**0.25**。该任务涉及小物体操作，对空间精度要求极高。虽然0.25的绝对值不高，但纯RL方法在该任务上同样无法从零开始获得有效回报，表明CrossInstruct提供的初始轨迹分布已包含可用的结构信息。

- **整体趋势**：CrossInstruct在几乎所有RLBench任务上一致优于VLM推理基线和纯RL方法。优势最显著的任务集中于需要精确空间定位的场景（篮球投篮、Jenga、Peg插入），而在空间要求相对宽松的任务上，VLM推理基线也能获得一定成功率。

### 强化学习初始化实验

Fig. 12展示了将CrossInstruct生成的轨迹作为离线数据初始化RL策略的效果：

- **Jenga任务**：从CrossInstruct采样轨迹初始化TD3+BC策略后，策略在训练过程中收敛至**约90%成功率**。该任务使用稀疏二值奖励，从零训练的SAC/TD3在整个训练过程中始终无法获得非零回报。这验证了CrossInstruct作为生成式模型为RL提供有效初始化的能力——即使直接执行成功率仅为0.55，其轨迹分布仍覆盖了足够的成功模式供RL精炼。

- **Peg插入任务**：CrossInstruct初始化的策略显著加速了学习过程。基线RL方法在400k步内未能收敛，而CrossInstruct初始化使策略快速获得正回报。这表明即使直接执行成功率有限，轨迹分布中的结构信息足以引导策略向高奖励区域探索。

### 消融分析：层次化精度耦合的关键作用

**精度耦合模块的贡献**通过对比VLM推理基线（无精度耦合）进行了验证：

- **小物体与遮挡场景**（Fig. 9）：无精度耦合时，VLM推理模型直接输出的轨迹常常无法精确到达需要交互的物体，如按钮、篮球和Jenga积木块。这是因为大型VLM的像素级定位能力有限，尤其当目标物体在图像中占据较小区域或被部分遮挡时。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/008_Figure_9.jpg]]
*Figure 9: Without hierarchical precision coupling, directly seeking the VLM reasoning model to provide trajectories often leads to the robot not adequately reaching the object that we need to interact with, such as the button, basketball and Jenga block*

- **颜色混淆导致的轨迹错误**（Fig. 10）：当场景中存在颜色相似的物体时，无精度耦合的VLM推理容易将目标错误地空间定位到相似颜色的物体上。例如，当蓝色Peg和蓝色方块同时存在时，推理模型生成的轨迹指向了错误的蓝色物体。而引入精度耦合后，小型微调VLM通过关键点语义描述进行精确定位，避免了此类混淆。

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/013_Figure_10.jpg]]
*Figure 10: Trajectories inferred with VLM-reasoning, without precision coupling can often mistakenly spatially-ground the objects in similar colored objects. On the right, both the peg and the square are blue, causing an erroneous trajectory (red). This does not happen in the left figure where blue pegs are not present*

- **采样随机性的作用**：CrossInstruct通过从轨迹分布中采样增加了演示的多样性。实验表明，这种随机性提高了后续RL策略的鲁棒性，因为策略在训练中接触到更丰富的状态-动作分布。

### 失败模式与局限性

CrossInstruct的主要失败模式可归纳为：

1. **直接执行精度不足**：在Peg插入等精细操作任务上，直接执行成功率仅为0.25，说明单次采样的轨迹可能因累积误差或深度估计不准确而偏离目标。RL精炼可部分弥补这一不足，但需要额外的环境交互。

2. **多视图依赖**：3D轨迹估计依赖校准的多视图相机位姿。若相机标定不准确或视图间重叠不足，射线投影的交叉点估计质量会下降，影响3D路点的精度。

3. **VLM推理的固有局限**：虽然精度耦合缓解了像素定位问题，但推理模型生成的关键点描述和2D轨迹仍可能因场景理解错误而失效，尤其在语义模糊或超出训练分布的指令下。

### 实机泛化验证

Fig. 11展示了CrossInstruct在真实机器人上的泛化能力。在Place Cups和Saw Block任务中，跨模态指令在视觉上与执行场景不同的设置上定义，机器人仍能成功执行任务。Saw Block任务还展示了指令的语义泛化——"repeat 3x"使锯切动作重复三次，表明推理模型能够理解时序语义并将其映射为重复的运动模式。

### 补充图表

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/009_Table.jpg]]
*Table: I: Comparison of CrossInstruct with a VLM reasoning baseline and pure RL approaches (SAC, TD3) on RLBench tasks. Numbers denote success rates (higher is better)*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/012_Figure_12.jpg]]
*Figure 12: We sample trajectories from CrossInstruct to initialize policies for RL training. Returns against the number of steps shown (left: Jenga; right: Peg). As the Jenga task uses a sparse binary reward, training from scratch gives no nonzero returns. For the Peg task, we illustrate the performance of baseline RL methods trained from scratch against our TD3+BC approach. We observe that CrossInstruct provides an effective generative model to initialize RL training*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/010_Figure_8.jpg]]
*Figure 8: CrossInstruct, through hierarchical precision coupling, can generate spatially-accurate motions, enabling the robot to precisely pick up and place the basketball into the hoop*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/011_Figure_11.jpg]]
*Figure 11: Generalizing Cross-modal instructions to new setups, with the Place Cups task shown in the left and the Saw Block task on the right. An image with an instruction is overlaid, and we observe that the setups that the instructions are defined over are visually different from the execution setup, highlighting the generalization exhibited. We can also provide instructions such as “repeat 3x” which specifies the sawing motion to be repeated three times*

![[assets/figures/papers/paper_list_l8_https_arxiv_org_abs_2509_21107/figures/006_Figure_7.jpg]]
*Figure 7: Representative tasks from the RLBench [27] benchmark used in our evaluations*

## 方法谱系与知识库定位

### 核心问题与因果机制

传统机器人模仿学习依赖大量物理演示，成本高昂且难以泛化。现有跨模态指令方法虽然试图利用视觉语言模型（VLM）将高层语义指令转化为机器人行为，但缺乏将语义推理与精确空间定位相结合的能力——VLM直接输出像素坐标或2D轨迹时，常因相似颜色物体混淆、小物体遮挡等原因产生空间定位错误（Fig. 9, Fig. 10），导致难以泛化到新环境。

CrossInstruct的核心因果调控变量是**层次化精度耦合**（Hierarchical Precision Coupling）：将大型推理VLM的高层语义推理能力与小型微调VLM的像素级精确定位能力解耦并协同。推理模型负责生成语义关键点描述符，指向模型负责在图像中精确定位这些关键点的像素坐标，推理模型再基于精确定位的关键点生成2D轨迹，最终通过多视图射线投影将2D轨迹分布融合为3D末端执行器轨迹分布。这一设计将“理解做什么”与“知道在哪里做”分离，解决了单一VLM在空间精度上的瓶颈。

### 与基线方法的关系

**VLM-Reasoning基线（HAMSTER）**（Li et al., 2025）代表了不包含层次化精度耦合的VLM推理方法，直接由大型VLM生成轨迹。CrossInstruct在8项RLBench任务上大幅优于该基线（Table I），差异的根源正是精度耦合模块：消融实验表明，移除精度耦合后，VLM推理常错误定位目标物体，尤其在物体边界模糊、小尺寸或遮挡场景下性能显著下降（Fig. 9, Fig. 10）。

**纯强化学习基线**方面，CrossInstruct与**SAC**（Haarnoja et al., ICML 2018）和**TD3**（Fujimoto et al., ICML 2018）形成鲜明对比。在RLBench篮球投篮任务上，SAC/TD3从零训练无法获得非零回报，而CrossInstruct达到0.90成功率（Table I）。在Jenga任务上，纯RL方法同样失败，CrossInstruct直接执行轨迹即达0.55成功率，经**TD3+BC**（Fujimoto et al. TD3 + Behavior Cloning）微调后收敛至约90%成功率（Fig. 12）。这揭示了CrossInstruct作为RL策略初始化器的价值：其生成的轨迹分布为RL提供了有效的探索起点，使稀疏奖励任务从“完全不可解”变为“可高效收敛”。

### 方法谱系定位

从方法谱系看，CrossInstruct处于三个技术脉络的交汇点：

1. **VLM驱动的机器人操控**：沿袭利用大规模预训练VLM进行任务推理的路线，但通过引入专用指向模型弥补了VLM在像素级定位上的固有不足。
2. **从演示中学习（LfD）**：CrossInstruct实质上是一种无需物理演示的LfD方法——跨模态指令（草图+文本）构成了一种新型的“弱演示”形式，由VLM系统自动转化为可执行轨迹。
3. **多视图几何与3D感知**：通过多视图射线投影将2D轨迹提升为3D轨迹分布，连接了2D视觉推理与3D机器人运动空间。

### 适用边界与局限

CrossInstruct的适用边界受以下因素约束：

- **相机标定依赖**：多视图射线投影需要已知相机位姿 $\mathcal{P}$，这要求场景中部署标定好的多相机系统，限制了在非结构化环境中的即插即用能力。
- **指向模型的泛化能力**：小型微调VLM $\mathcal{G}$ 的指向精度依赖于训练数据的覆盖范围，对于训练中未见过的物体类别或极端视角，定位精度可能下降——尽管论文未提供系统性的失败分析，这一局限需要手动验证。
- **任务的几何可表达性**：CrossInstruct依赖关键点描述和2D轨迹来表达运动意图，对于需要复杂力控或动态接触推理的任务（如灵巧操作中的滑动接触），当前框架的表示能力可能不足。

### 开放问题

论文明确提出了两个开放方向：

1. **交互式纠正**：如何使人类能够在机器人执行动作后提供跨模态信息来纠正机器人行为？这指向从单向指令生成向闭环人机协作的扩展。
2. **新视角合成与相机解耦**：能否集成大型预训练模型（如DUSt3R、VGER或VGGT）来支持从新视角生成合成相机视图，以减少物理相机定位的负担？这直接针对上述相机标定依赖的局限，若能实现，将显著提升系统的部署灵活性。

## 原文 PDF

![[paperPDFs/arxiv_2025/Cross-Modal_Instructions_for_Robot_Motion_Generation.pdf]]