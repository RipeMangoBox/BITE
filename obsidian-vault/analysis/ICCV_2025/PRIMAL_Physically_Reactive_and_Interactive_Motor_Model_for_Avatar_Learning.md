---
title: PRIMAL Physically Reactive and Interactive Motor Model for Avatar Learning
type: paper
paper_level: A
venue: ICCV
year: 2025
pdf_ref: paperPDFs/ICCV_2025/PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learning.pdf
project_link: https://yz-cnsdqz.github.io/eigenmotion/PRIMAL
aliases:
- PPRIMMAL
tags:
- ICCV_2025
- topic/motion_animation/character_control_physics
- topic/pose_trajectory_control
- topic/motion_animation
core_operator: 采用单帧初始状态（关节位置与速度）作为条件的自回归扩散模型，在短时间尺度（0.5秒）上学习运动的物理特性，摆脱对历史语义依赖，从而支持流式实时交互与冲量扰动。
primary_logic: 人类运动在短时间尺度（约0.5秒）内由物理主导而非高层语义，因此利用大量无标签短运动片段训练的条件扩散模型能够隐式学习物理约束，无需物理模拟即可生成逼真且可交互的运动。
claims:
- 在仅给定单帧初始状态的条件下，模型能生成任意长度运动，并在冲量扰动下保持高物理真实度（ASR 0.088, ANCR 1.0）。
- 预训练模型通过无监督学习短时运动片段，即能掌握足部接触等物理现象，ASR低至0.024。
- 通过简单修改初始速度即可实现对角色行为的实时冲量控制，无需额外训练。
- 使用Classifier-Based Guidance可精准控制运动速度和方向，且推导解析梯度实现实时性能。
---

# PRIMAL Physically Reactive and Interactive Motor Model for Avatar Learning

> [!tip] 核心洞察
> 人类运动在短时间尺度（约0.5秒）内由物理主导而非高层语义，因此利用大量无标签短运动片段训练的条件扩散模型能够隐式学习物理约束，无需物理模拟即可生成逼真且可交互的运动。

| 字段 | 内容 |
|------|------|
| 中文题名 | PRIMAL：用于虚拟角色学习的物理响应与交互运动模型 |
| 英文题名 | PRIMAL Physically Reactive and Interactive Motor Model for Avatar Learning |
| 会议/期刊 | ICCV 2025 |
| Links |  [Project](https://yz-cnsdqz.github.io/eigenmotion/PRIMAL)|
| Topic | #topic/motion_animation/character_control_physics #topic/pose_trajectory_control #topic/motion_animation |
| Method | PRIMAL |
| Dataset | Motion Realism, Reaction to Induced Impulses, Semantic Action Generation |

> [!tip] 效果简介
> - Motion Realism (unbounded generation) 上，ASR↓ 0.024；ANCR↑ 1.0；ARD x10^-3↓ 0.074。
> - Reaction to Induced Impulses 上，ASR↓ 0.088；ANCR↑ 1.0；ARD x10^-3↓ 0.511。
> - Semantic Action Generation (few-shot) 上，R-precision↑ 0.96。

## 概述

**问题瓶颈**：现有动作生成方法面临一个根本性矛盾——离线生成系统（如扩散模型或VAE）能产出高质量运动，但缺乏实时交互能力；基于物理模拟的方法虽可响应外力，却难以产生自然流畅的动作且技能覆盖有限。核心瓶颈在于，如何在**不依赖显式物理模拟**的前提下，使虚拟角色具备实时、逼真的物理反应能力。

**核心洞察**：PRIMAL 的出发点是观察到人类运动在短时间尺度（约0.5秒）内由物理规律主导，而非高层语义意图。这意味着，如果模型能在这一时间窗口内学习运动的动力学特性，就可以隐式地掌握物理约束，无需显式物理引擎。

**因果机制**：基于上述洞察，PRIMAL 采用**单帧初始状态（关节位置与速度）作为条件**的自回归扩散模型。这一设计切断了传统方法对历史多帧语义上下文的依赖，使运动生成完全由当前物理状态驱动。当外部冲量扰动来临时，只需修改初始速度即可在下一帧生成中自然引发连锁反应，实现实时交互。

**方法定位**：PRIMAL 是一个**两阶段学习框架**：
- **预训练阶段**：在大量无标签的0.5秒运动片段上训练条件扩散模型，学习短时物理动态；
- **适应阶段**：通过 ControlNet 风格的适配器高效适应下游任务（如语义动作生成、空间目标到达），冻结基础模型以保持运动能力。

**关键结果**：
- 在无界运动生成中，PRIMAL 达到极低的足部滑动率（ASR 0.024）和完美的足部接触率（ANCR 1.0），证明其隐式学习了足部接触等物理现象（Table 1）。
- 在冲量扰动场景下，模型仍保持高物理真实度（ASR 0.088, ANCR 1.0），验证了实时物理反应能力（Table 2）。
- 通过基于分类器的引导（CBG），可精准控制运动速度和方向；通过简单修改初始速度即可实现冲量控制，无需额外训练。
- 少样本语义动作生成达到 R-precision 0.96 的分类准确率（Table 3）。

**方法谱系与知识库定位**：PRIMAL 属于**自回归扩散运动生成**范式，但区别于 **AMDM**（Shi et al., TOG 2024）、**CAMDM**、**DART**（Zhao et al., ICLR 2025）等需要多帧历史条件的方法，其单帧条件设计使其天然支持流式交互。与 **InsActor**（Ren et al., NeurIPS 2023）等扩散规划+物理模拟的混合方案不同，PRIMAL 完全数据驱动，避免了物理模拟带来的不自然感。在适应机制上，借鉴了 **OmniControl-Net**（Xie et al., ICLR 2024）的 ControlNet 范式，但应用于运动生成领域。

## 背景与动机

### 问题背景

在实时交互式3D应用中，如游戏、虚拟现实和数字人，角色动画系统需要同时满足三个核心要求：**物理真实性**（对外力扰动产生自然反应）、**实时交互性**（支持用户连续控制）以及**运动多样性**（生成丰富且不重复的动作）。传统动画系统通常依赖手工制作的状态机和动作匹配，难以在保持动作质量的同时覆盖开放场景中的无限交互可能性。

近年来，基于深度学习的运动生成方法取得了显著进展，但大多数工作集中于**离线生成**——给定高层语义条件（如文本描述、动作类别）生成固定长度的运动序列。这些方法在生成质量上表现出色，却缺乏实时交互能力：它们通常需要完整的历史上下文才能预测未来，无法在运行时对用户输入或环境变化做出即时响应。

### 现有方法缺口

当前解决角色实时物理反应的主流路径是**基于物理模拟**的方法。这类方法通过强化学习训练控制策略，使角色在物理引擎中学会行走、跑步等技能。然而，物理模拟方法面临两个根本性困境：

1. **动作自然度不足**：强化学习训练的控制器往往产生僵硬、机械的运动模式，缺乏人类运动的流畅性和表现力。尽管近年来结合运动数据的模仿学习有所改善，但在复杂交互场景下仍然难以达到数据驱动方法的自然度。
2. **技能泛化有限**：物理模拟方法通常为特定技能（如行走、跳跃）训练独立的控制器，难以在单一模型中覆盖人类运动的全部多样性。

另一方面，**数据驱动的生成模型**虽然能产生高质量运动，但其设计假设与实时交互需求存在根本冲突。现有自回归扩散模型（如**AMDM**（Shi et al., TOG 2024）、**CAMDM**、**DiP**（Tevet et al., arXiv 2024））和基于VAE的方法（如**DART**（Zhao et al., ICLR 2025）、**GAMMA**（Zhang & Tang, CVPR 2022））通常将运动视为长时序语义序列，以过去多帧作为条件预测未来。这种设计隐含地假设运动由高层语义主导，导致模型在遇到训练分布外的物理扰动时无法产生合理反应，因为扰动打破了历史帧与未来之间的语义连贯性。

### 核心洞察与动机

PRIMAL的核心洞察在于重新审视人类运动的**时间尺度特性**：在极短的时间窗口内（约0.5秒），人体运动主要由**物理规律**（动量、惯性、关节约束）而非高层语义意图主导。一个正在行走的人被突然推搡时，其身体在最初半秒内的反应几乎完全由物理决定，而非“我想继续走”的语义目标。

基于这一洞察，PRIMAL提出了一种全新的范式：**将运动生成建模为短时间尺度的物理过程，而非长时间尺度的语义序列**。具体而言，模型仅以**单帧初始状态**（关节位置与速度）作为条件，预测未来0.5秒的运动。这种设计带来了三个关键优势：

- **物理响应能力**：模型在训练中隐式学习了短时运动的物理约束，当初始速度被人为修改（模拟冲量扰动）时，能够自动生成符合物理规律的后续运动，无需显式物理模拟。
- **流式实时交互**：由于条件仅依赖当前帧，模型可以在每0.5秒窗口内独立生成运动，支持任意长度的实时推理，且无需维护历史状态。
- **无监督可扩展性**：训练数据只需大量无标注的短运动片段（从AMASS数据集中任意切分），无需动作标签或物理模拟器，使方法易于扩展到大规模运动数据。

这种将“物理反应”从“语义生成”中解耦的设计，使得PRIMAL能够在保持数据驱动运动自然度的同时，获得物理模拟方法才具备的实时响应能力，填补了两类方法之间的关键空白。

## 核心创新

PRIMAL的核心创新在于**重新定义了运动生成的条件范式**：将传统依赖多帧历史语义的自回归运动模型，彻底转变为仅依赖单帧物理初始状态（关节位置与速度）的短时物理反应模型。这一范式转变使角色首次在不使用显式物理模拟的情况下，获得了实时、逼真的物理交互能力。

### 关键创新点

**1. 单帧物理条件替代多帧历史语义**

传统自回归运动模型（如 **AMDM** (Shi et al., TOG 2024)、**CAMDM**、**DART** (Zhao et al., ICLR 2025)）通常以过去多帧（M帧）作为条件来预测未来运动，这隐式地将运动建模为语义序列的延续。PRIMAL则将条件压缩为**单帧初始状态**——包含SMPL-X的完整关节位置与速度（267维），从根本上切断了模型对历史语义上下文的依赖。这一改变的理论依据是：**人类运动在约0.5秒的短时间尺度内由物理规律主导而非高层语义**。因此，模型仅需根据当前物理状态预测未来0.5秒的运动，即可隐式学习牛顿力学约束，无需显式物理模拟。

**2. 无标记化器的原生运动空间建模**

现有扩散运动模型（如 **DiP** (Tevet et al., arXiv 2024)、**GAMMA** (Zhang & Tang, CVPR 2022)）通常依赖训练运动VAE标记化器将运动压缩到潜在空间，再在潜在空间进行扩散。PRIMAL**直接在原始运动空间操作**，避免了标记化器带来的信息损失和额外训练开销。这一设计得益于其独特的训练策略：将AMASS数据集中的所有运动切分为0.5秒片段（无需标注），直接训练去噪网络从噪声中恢复干净运动。由于片段极短且条件仅为单帧状态，模型无需压缩即可高效学习。

**3. 前向运动学损失增强物理一致性**

PRIMAL在标准DDPM简单损失之外，引入了两项前向运动学（FK）辅助损失：
- **关节位置损失** $\mathcal{L}_{FK}$：通过SMPL-X模型将预测的关节旋转映射为3D关节位置，与真实位置计算L2误差；
- **关节速度损失** $\mathcal{L}_{FKV}$：对预测速度施加同样约束。

这两项损失直接监督物理空间中的运动轨迹，显著抑制了滑步等物理不真实现象。消融证据（Table 1）显示，引入FK损失后，足部滑动指标ASR降至0.024，地面穿透指标ANCR达到1.0的完美水平。

**4. 自稳定自回归生成**

与部分自回归模型需要计划采样（scheduled sampling）来缓解误差累积不同，PRIMAL**无需任何计划采样机制**。模型在训练时仅见过0.5秒片段，但在推理时通过将生成的最后一帧状态作为下一段的条件，可生成任意长度的运动序列。模型展现出自稳定特性——即使出现微小偏差，后续生成会自动修正，不会发散。这一特性源于短时物理约束的强正则化效应。

**5. 解析梯度的实时可控引导**

PRIMAL提出基于分类器的引导（Classifier-Based Guidance, CBG）来实现对运动方向和速度的实时控制。与依赖自动微分的传统方法不同，PRIMAL**推导了运动引导损失和朝向引导损失的解析梯度**，使每一步引导仅需微秒级计算开销，保证实时交互性能。用户可通过简单修改初始速度向量，实现对角色行为的冲量控制，无需额外训练。

**6. ControlNet风格的高效任务适应**

在第二阶段适应中，PRIMAL采用类似ControlNet的适配器架构（Figure 3）：在每个Transformer块旁路添加可训练的零卷积层，以控制信号为条件。这一设计**冻结基础模型全部参数**，仅训练轻量适配器，即可在少量标注数据（如少样本动作类别、空间目标位置）上高效适应新任务，同时完整保留基础运动能力。相比之下，直接微调（finetuning）或使用自适应层归一化（AdaLN）架构均无法在保持物理真实度的同时实现高效适应。

### 与基线方法的本质差异

| 设计维度 | 基线方法 | PRIMAL |
|---------|---------|--------|
| 条件帧数 | 过去多帧（M帧） | 单帧初始状态 |
| 运动表示 | 关节旋转或潜在向量标记 | SMPL-X完整状态（267维） |
| 标记化器 | 需要训练VAE标记化器 | 无标记化器，直接在运动空间操作 |
| 训练数据切分 | 固定长度序列或整个序列 | 所有0.5秒片段，无需标注 |
| 损失函数 | 仅DDPM简单损失 | DDPM简单损失 + FK位置损失 + FK速度损失 |
| 计划采样 | 部分方法使用 | 无需，模型自稳定 |

这些创新共同构成了PRIMAL的核心能力：**在不使用物理模拟的前提下，使角色具备实时、逼真的物理反应能力**——包括对外部冲量的自然响应、连续速度/方向控制、以及任意长度运动的自稳定生成。

## 整体框架

PRIMAL 采用**两阶段“预训练-适应”**学习范式，构建了一个完全数据驱动、无需物理模拟的实时角色动画系统。其核心流程如下：

**第一阶段：反应式运动基模型预训练**
- **输入**：单帧初始状态 $\mathbf{x}_0$，包含 SMPL-X 完整状态——267 维的关节位置与速度（而非仅关节旋转或潜在标记）。
- **训练数据**：从 AMASS 运动捕捉数据集中切分出的大量 **0.5 秒**短运动片段，无需任何语义标注。
- **模型**：一个基于 Transformer 的自回归扩散去噪网络 $G(t, \mathbf{X}^t, \mathbf{x}_0)$，直接在运动空间上操作，不使用运动标记化器（tokenizer），也不依赖计划采样（scheduled sampling）。
- **输出**：未来 0.5 秒（$N$ 帧）的运动序列 $\hat{\mathbf{X}}^0$。
- **推理**：以自回归方式将上一段生成的末端状态作为下一段的初始条件，实现任意长度的实时运动生成。

**第二阶段：基于 ControlNet 风格适配器的任务适应**
- 在冻结的基模型之上，为每个 Transformer 块引入一个 **ControlNet 风格的适配器**（图 3），接收通用控制信号 $y$。
- 适配器通过缩放操作调节控制信号的影响强度，对应无分类器引导（CFG）中的 $\gamma$ 参数。
- 可高效适应不同下游任务，如**语义动作生成**（少量样本）和**空间目标到达**，同时保持基础运动能力。

**实时交互与控制模块**
- **冲量扰动控制**：通过直接修改初始状态的关节速度，即可使角色对诱导冲量产生自然反应，无需额外训练。
- **基于分类器的引导（CBG）**：通过运动引导损失 $\mathcal{L}_{move}$ 和朝向引导损失 $\mathcal{L}_{facing}$，精准控制角色的运动速度和方向；使用解析梯度推导以保证实时性能。
- **后处理管线**：包括关节重投影、抓地校正和惯性化混合，用于修正滑步等伪影，提升实时渲染质量。

**关键设计决策**：
- 条件帧数从过去多帧缩减为单帧初始状态，使模型摆脱对历史语义的依赖，从而支持流式实时交互。
- 损失函数在标准 DDPM 简单损失 $\mathcal{L}_{\mathrm{simple}}$ 基础上，额外引入前向运动学关节位置损失 $\mathcal{L}_{FK}$ 和速度损失 $\mathcal{L}_{FKV}$，增强物理一致性。

整个系统部署于 Unreal Engine 中，角色可在无任何控制信号或外部扰动的情况下自主持续运动，并对实时交互指令做出即时响应。

### 补充图表

![[assets/figures/papers/paper_list_l4_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learni/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of our network*

## 核心模块与公式推导

### 3.1 问题形式化与扩散基础

PRIMAL 的核心思想是将人体运动建模为一个条件生成问题：给定单帧初始状态（包含关节位置与速度），生成未来短时间窗口（0.5 秒）内的运动序列。这一形式化摆脱了对历史多帧语义上下文的依赖，使模型能够在仅给定物理初始条件的情况下做出实时响应。

运动片段表示为 $X^0 \in \mathbb{R}^{N \times D}$，其中 $N$ 为帧数，$D = 267$ 为 SMPL-X 完整状态维度（包含关节旋转、根节点位移等位置和速度信息）。前向扩散过程遵循标准 DDPM 范式：

$$X^t = \sqrt{\bar{\alpha}_t} X^0 + \sqrt{1 - \bar{\alpha}_t} \epsilon \tag{1}$$

其中 $\bar{\alpha}_t$ 为累积噪声调度系数，$\epsilon \sim \mathcal{N}(0, \mathbf{I})$ 为标准高斯噪声。去噪网络 $G$ 以噪声样本 $X^t$、时间步 $t$ 和条件 $c$（即初始状态 $\mathbf{x}_0$）为输入，预测干净样本 $\hat{X}^0$。基础训练损失为简单 DDPM 损失：

$$\mathcal{L}_{\mathrm{simple}} = \mathbb{E}_{X^0 \sim p(X^0), t \sim U[1,T]} \left[ \| X^0 - G(t, X^t, c) \|^2 \right] \tag{2}$$

### 3.2 自回归扩散去噪网络

去噪网络 $G(t, X^t, \mathbf{x}_0)$ 采用 Transformer 架构（见 Figure 2）。输入包含三部分：噪声运动序列 $X^t$ 的逐帧 token、时间步 $t$ 的嵌入，以及初始状态 $\mathbf{x}_0$ 的条件嵌入。时间步和初始条件通过上下文条件嵌入模块注入到每个 Transformer 块中，引导去噪过程朝向符合物理约束的方向收敛。

该网络以自回归方式运行：每次生成未来 $N$ 帧后，将最后一帧的状态作为新的初始条件，送入下一轮扩散去噪，从而实现任意长度的流式运动生成。值得注意的是，PRIMAL **不使用运动标记化器**（motion tokenizer），也**不依赖计划采样**（scheduled sampling），直接在原始运动空间上操作，避免了信息压缩损失和误差累积问题。

推理阶段采用无分类器引导（Classifier-Free Guidance, CFG）：

$$\hat{X}^0 = G(t, X^t, \varnothing) + \gamma (G(t, X^t, c) - G(t, X^t, \varnothing)) \tag{3}$$

其中 $\varnothing$ 为空条件，$\gamma$ 为引导强度。

### 3.3 前向运动学辅助损失

为增强生成运动的物理一致性，PRIMAL 在简单 DDPM 损失之上引入两个基于 SMPL-X 前向运动学（Forward Kinematics, FK）的辅助损失。总训练损失为：

$$\mathcal{L} = \mathcal{L}_{\mathrm{simple}} + \gamma_1 \mathcal{L}_{FK} + \gamma_2 \mathcal{L}_{FKV} \tag{4}$$

**关节位置损失** $\mathcal{L}_{FK}$ 计算预测关节位置与真实关节位置的 L2 误差：

$$\mathcal{L}_{FK} = \frac{1}{N} \sum_{i=0}^{N-1} \| \mathcal{M}(\beta, \hat{r}_i, \hat{\varphi}_i, \hat{\theta}_i) - J_i \|_2^2 \tag{5}$$

其中 $\mathcal{M}$ 为 SMPL-X 前向运动学函数，$\beta$ 为体型参数，$\hat{r}_i, \hat{\varphi}_i, \hat{\theta}_i$ 分别为预测的根节点位移、全局朝向和关节旋转，$J_i$ 为真实关节位置。

**关节速度损失** $\mathcal{L}_{FKV}$ 进一步约束时间维度的物理合理性：

$$\mathcal{L}_{FKV} = \frac{1}{N} \sum_{i=0}^{N-1} \| \dot{\mathcal{M}}(\beta, \hat{r}_i, \hat{\varphi}_i, \hat{\theta}_i) - \dot{J}_i \|_2^2 \tag{6}$$

其中 $\dot{\mathcal{M}}$ 为速度形式的前向运动学，$\dot{J}_i$ 为真实关节速度。这两个损失直接作用于关节位置和速度的几何空间，迫使网络隐式学习足部接触、地面约束等物理现象，是 PRIMAL 在无物理模拟条件下实现低滑步率（ASR 0.024）和高地面约束率（ANCR 1.0）的关键机制。

### 3.4 基于分类器的实时引导

为实现对角色运动方向和速度的实时控制，PRIMAL 引入基于分类器的引导（Classifier-Based Guidance, CBG）。与依赖自动微分的传统方法不同，PRIMAL 推导了引导损失的解析梯度，以保障实时性能。

**运动引导损失** 约束平均关节速度接近目标速度 $v_{goal}$：

$$\mathcal{L}_{move} = \left( \frac{1}{22N} \sum_{i=0}^{N-1} \sum_{j=1}^{22} \hat{j} - v_{goal} \right)^2 \tag{7}$$

**朝向引导损失** 约束角色朝向 $\mathbf{z}$ 与目标方向 $\mathbf{r}_{goal}$ 一致：

$$\mathcal{L}_{facing} = \| \mathbf{z} - \mathbf{r}_{goal} \|^2 \tag{8}$$

在推理时，CBG 梯度被注入去噪过程的每一步，引导生成的运动满足高层控制信号，而无需额外训练。

### 3.5 基于 ControlNet 的任务适应

为在冻结基础模型的前提下高效适应下游任务（如空间目标到达、少样本语义动作生成），PRIMAL 采用 ControlNet 风格的适配器架构（见 Figure 3）。在每个 Transformer 块中引入可训练的控制信号适配器，以通用控制信号 $y$ 为条件。适配器通过缩放因子控制其对基础模型输出的影响程度，形式上与 CFG 的 $\gamma$ 机制对应。这一设计使得基础模型的物理运动能力得以完整保留，同时仅需少量标注数据即可适应新任务。

![[assets/figures/papers/paper_list_l4_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learni/figures/003_Figure_3.jpg]]
*Figure 3: Illustration of our adaptation method. Given a base model, we introduce a ControlNet-like adaptor at each individual transformer block. The control signal y is a generic notation. We adapt the base model for semantic action generation and spatial target reaching. The scale operation manipulates the impact of the control signal, corresponding to γ in Eq. (3) of CFG*

## 实验与分析

PRIMAL 的实验评估围绕三个核心能力展开：**无界运动生成的真实度**、**对外部冲量扰动的物理反应**，以及**通过适应实现的下游任务性能**。所有实验均基于 AMASS 数据集，使用 SMPL-X 表示，评估协议与先前工作保持一致，确保公平性。

### 运动真实度：无界生成

Table 1 报告了 PRIMAL（InContext 架构）与多个 SOTA 方法在运动真实度指标上的对比。关键发现如下：

![[assets/figures/papers/paper_list_l4_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learni/figures/007_Table_1.jpg]]
*Table 1: Motion Realism: Comparison with SOTA. Best results are highlighted in boldface. We only compare “InContext” with baselines for the perceptual study (BPR). See text*

- **足部滑动（ASR）**：PRIMAL 的 ASR 低至 0.024，显著优于数据驱动基线。这表明模型在无显式物理约束的情况下，隐式学习到了足部接触等物理现象。
- **地面碰撞（ANCR）**：PRIMAL 达到 1.0 的满分，意味着生成的运动完全避免了地面穿透。
- **关节位置误差（ARD）**：PRIMAL 的 ARD 为 $0.074 \times 10^{-3}$，保持了高精度的关节重建。

这些结果验证了核心假设：在 0.5 秒的短时间尺度上，运动由物理主导而非高层语义，条件扩散模型能够从大量无标签短片段中隐式学习物理约束。Figure 4 的定性结果进一步展示了从不同初始状态生成任意长度运动序列的能力，模型在实时条件下保持了高保真度。

![[assets/figures/papers/paper_list_l4_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learni/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of three random motion generations (one per row). Given different initial states, the model is able to generate high-fidelity future motions of arbitrary lengths in real time. The numbers denote the frame indices. See Supplemental Video*

### 冲量扰动下的物理反应

Table 2 展示了角色对外部诱导冲量的反应能力。在手动扰动初始速度的条件下，PRIMAL 的 ASR 为 0.088，ANCR 保持 1.0，ARD 为 $0.511 \times 10^{-3}$。与无扰动场景（Table 1）相比，ASR 有所上升但仍处于低位，表明模型能够在受到冲量后快速恢复物理合理的运动状态。

![[assets/figures/papers/paper_list_l4_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learni/figures/005_Table_2.jpg]]
*Table 2: Results of reactions to induced impulses. The evaluation metrics are the same as in Tab. 1. Best results are in boldface*

这一能力源于模型的核心设计：仅以单帧初始状态（关节位置与速度）为条件，摆脱了对历史语义的依赖。当外部冲量改变初始速度时，模型自动生成符合物理规律的反应运动，无需额外训练。Figure 5 可视化了不同冲量扰动下的运动序列，展示了扰动速度箭头与生成运动的对应关系。

![[assets/figures/papers/paper_list_l4_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learni/figures/008_Figure_5.jpg]]
*Figure 5: Avatar reactions to induced impulses. Each row shows a motion. The pale orange arrows in the initial frame denote the perturbed velocities, and bars in the future frames denote the generated joint locations and velocities. Darker color means smaller velocity norms*

### 语义动作生成与任务适应

Table 3 报告了基于 ControlNet 风格适配器的少样本语义动作生成结果。PRIMAL 在 R-precision 指标上达到 0.96，表明在仅使用少量标注数据的情况下，模型能够准确生成指定动作类别，同时保持基础运动能力。这一高效适应能力得益于冻结基础模型、仅训练轻量适配器的策略（Figure 3），避免了灾难性遗忘。

![[assets/figures/papers/paper_list_l4_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learni/figures/006_Table_3.jpg]]
*Table 3: Results of semantic action generation. R-precision indicates classification accuracy. See more results in Sup. Mat*

### 实时控制能力

基于分类器的引导（CBG）提供了对运动速度和方向的精准控制。通过推导解析梯度而非使用自动微分，CBG 实现了实时性能。运动引导损失 $\mathcal{L}_{move}$ 和朝向引导损失 $\mathcal{L}_{facing}$ 分别约束平均关节速度和角色朝向，使用户能够通过连续信号实时操控角色行为。

### 失败模式与局限

尽管 PRIMAL 在主流指标上表现优异，仍存在以下已知局限：

1. **罕见动作的稳定性**：模型对摔倒后起身等罕见动作的生成可能不够稳定，物理表现可能不合理。这源于训练数据中此类动作的稀疏性。
2. **冲量控制的手动性**：当前冲量控制需要手动指定关节速度扰动，尚未实现高层指令（如文本、语音）到冲量的自动映射。
3. **环境感知缺失**：模型未显式考虑障碍物或场景上下文，无法保证碰撞避免。这限制了其在复杂 3D 场景中的直接部署。
4. **计算开销**：尽管生成速度可达实时，Transformer 扩散模型在资源受限平台上的推理延迟仍需优化。
5. **零样本泛化能力有限**：适应阶段依赖少量标注数据，对于全新动作类别的零样本泛化能力较弱。

这些局限指向了未来的改进方向：自动发现最优冲量序列、集成环境感知模块、通过更大的基础模型实现端到端控制，以及模型轻量化以支持移动端部署。

### 补充图表

![[assets/figures/papers/paper_list_l4_PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learni/figures/001_Figure_1.jpg]]
*Figure 1: PRIMAL is a novel generative real-time 3D character animation system that works in Unreal Engine. The avatar reacts to induced impulses promptly and naturally (top). After efficient adaptation, the avatar can be pulled to chase a “magnet” (middle). We also personalize the avatar’s movements based on a tiny mocap dataset, captured by Mocapade3.0 [19] from cellphone videos (bottom). As a result, we can control the avatar with discrete commands and continuous signals. Without any control signal, or external perturbations, the avatar moves autonomously in the 3D space without end. PRIMAL is purely data driven; no physical simulation is used*

## 方法谱系与知识库定位

### 1. 与现有工作的关系

PRIMAL 的核心定位是**数据驱动的、无需物理模拟的实时交互角色动画系统**。它处于运动生成、物理角色动画和扩散模型三个领域的交叉点，其设计选择直接回应了现有方法的瓶颈。

#### 1.1 相对于自回归运动扩散模型的改进

PRIMAL 与一系列自回归扩散运动生成基线（如 **AMDM** (Shi et al., TOG 2024)、**CAMDM**、**DART** (Zhao et al., ICLR 2025)、**DiP** (Tevet et al., arXiv 2024)）共享“扩散模型+自回归生成”的骨架，但在几个关键设计上做出了根本性改变：

- **条件窗口：从多帧历史到单帧初始状态。** 上述基线通常以过去 $M$ 帧作为条件来预测未来运动，这隐式地将运动建模为语义或时序依赖的延续。PRIMAL 仅以**单帧初始状态（关节位置与速度）** 为条件，切断了模型对历史语义的依赖。这一改变是 PRIMAL 能够响应任意冲量扰动并生成无界运动的根本原因——模型学习的是“给定当前物理状态，下一步最自然的物理演化”，而非“延续之前的动作趋势”。
- **运动表示：从潜在标记到原始运动空间。** 多数基线（如 DART）依赖预训练的 VAE 标记化器将运动压缩为潜在向量，再在潜在空间进行扩散。PRIMAL 直接在 **SMPL-X 完整状态（267 维，包含位置和速度）** 上操作，无需标记化器。这避免了潜在空间的信息损失，并使得前向运动学损失可以直接施加在原始运动表示上，强化物理一致性。
- **训练数据切分：从固定序列到所有 0.5 秒片段。** 传统方法在固定长度序列或完整动作片段上训练，PRIMAL 则利用 AMASS 数据集中所有可能的 0.5 秒短片段，无需任何标注。这一策略的关键洞察在于：**人类运动在约 0.5 秒的时间尺度上由物理主导而非高层语义**，因此大量无标签的短片段足以让模型隐式学习物理约束。

#### 1.2 相对于物理模拟方法的优势

基于物理模拟的角色动画方法（如 **InsActor** (Ren et al., NeurIPS 2023)）通过扩散模型规划运动，再依赖物理模拟器执行，其产生的动作往往不够自然，且技能有限。PRIMAL 完全摒弃了显式物理模拟，却能在冲量扰动下保持极高的物理真实度（ASR 0.088, ANCR 1.0，见 Table 2）。其核心机制是：扩散模型在短时间尺度上学到的运动分布本身蕴含了物理约束，无需额外的模拟步骤即可生成符合物理规律的反应。

#### 1.3 与 ControlNet 风格适配方法的关系

PRIMAL 的第二阶段适应采用了 **ControlNet 风格的适配器**（与 **OmniControl-Net** (Xie et al., ICLR 2024) 共享设计理念），在每个 Transformer 块中插入可训练的控制信号处理分支（Figure 3）。与传统微调（finetuning）或自适应层归一化（AdaLN）相比，ControlNet 适配器在冻结基础模型参数的前提下，仅通过少量标注数据即可高效适应新任务（如空间目标到达、语义动作生成），同时完整保留基础模型的物理运动能力。这一设计使得 PRIMAL 具备“基础物理运动模型 + 即插即用任务适配器”的模块化架构。

#### 1.4 与运动基元方法的区别

**GAMMA** (Zhang & Tang, CVPR 2022) 等基于 VAE 的运动基元方法将运动分解为离散基元，再通过组合生成动作。PRIMAL 不依赖显式的基元分解，而是让扩散模型在连续运动空间中直接学习物理演化，从而避免了基元边界处的运动不连续问题，并支持更细腻的冲量响应。

### 2. 适用边界

PRIMAL 在以下条件下表现最佳：
- **短时物理反应**：模型的核心能力集中在约 0.5 秒的时间尺度内，对于需要长时间规划的任务（如复杂导航），仍需依赖 CBG 或 ControlNet 适配器提供高层引导。
- **无环境约束的场景**：当前模型未显式考虑障碍物或场景上下文，适用于开放空间中的角色控制，但在复杂环境中可能无法避免碰撞。
- **数据分布内的运动**：模型在 AMASS 数据集上训练，对于数据分布内的运动（行走、跑步、转身等）生成质量高，但对罕见动作（如摔倒后起身）的表现可能不够稳定。

### 3. 局限与开放问题

#### 3.1 已知局限

1. **罕见动作的物理合理性**：模型对训练数据中稀疏的动作（如跌倒恢复、极端姿态）生成可能不稳定，物理表现可能不合理。
2. **冲量控制的手动性**：当前冲量控制需要手动指定关节速度扰动，尚未实现从高层指令（文本、语音）到冲量的自动映射。
3. **环境感知缺失**：模型未集成场景上下文，无法感知障碍物或地面类型，限制了在复杂 3D 环境中的应用。
4. **计算开销**：尽管生成速度可达实时，但 Transformer 扩散模型的计算开销在移动设备或游戏主机上可能仍较高。
5. **零样本泛化有限**：适应阶段依赖少量标注数据，对于完全未见的新动作类别，泛化能力受限。

#### 3.2 开放问题

1. **自动冲量发现**：如何自动发现并生成用于控制角色的最优冲量序列，以实现复杂行为目标？
2. **场景感知集成**：如何将环境感知（障碍物、地形、物理约束）集成到运动模型中，实现场景感知的实时交互？
3. **端到端高层控制**：能否通过更大的基础模型（如 LLM）实现从文本、语音到连续动作的端到端控制，将 PRIMAL 作为可调用的“物理运动引擎”？
4. **模型轻量化**：如何优化模型效率，使其在资源受限平台上也能流畅运行，以支持更广泛的实时应用（如移动游戏、VR/AR）？

## 原文 PDF

![[paperPDFs/ICCV_2025/PRIMAL_Physically_Reactive_and_Interactive_Motor_Model_for_Avatar_Learning.pdf]]
