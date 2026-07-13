---
title: "TextOp: Real-time Interactive Text-Driven Humanoid Robot Motion Generation and Control"
type: paper
paper_level: A
venue: arXiv
year: 2026
pdf_ref: paperPDFs/arxiv_2026/TextOp_Real_time_Interactive_Text_Driven_Humanoid_Robot_Motion_Generation_and_Control.pdf
project_link: https://text-op.github.io/
code_link: https://github.com/microsoft/onnxruntime
aliases:
- TextOp
tags:
- arxiv_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 采用自回归短时域运动扩散模型生成运动参考，并由基于强化学习的全身运动跟踪策略执行，同时通过机器人骨架运动表示和生成数据增强弥合分布差距。
primary_logic: 将交互式文本驱动运动生成视为一种流式条件预测问题，并通过机器人特定运动表示和域自适应训练，实现从虚拟角色到真实人形机器人的实时部署。
claims:
- TextOp在真实机器人上连续执行了多种技能，能够在实时文本命令变化时平滑地切换动作。
- 在30秒的真实机器人运行中，TextOp在随机和循环指令下均保持高成功率和跟踪精度。
- 端到端用户交互延迟平均为0.73秒，满足实时交互需求。
- 在BABEL验证集上，TextOp的运动生成在段级和过渡级指标上均达到最优，FID显著低于DART+Retarget。
---

# TextOp: Real-time Interactive Text-Driven Humanoid Robot Motion Generation and Control

> [!tip] 核心洞察
> 将交互式文本驱动运动生成视为一种流式条件预测问题，并通过机器人特定运动表示和域自适应训练，实现从虚拟角色到真实人形机器人的实时部署。

| 字段 | 内容 |
|------|------|
| 中文题名 | TextOp：实时交互式文本驱动人形机器人运动生成与控制 |
| 英文题名 | TextOp: Real-time Interactive Text-Driven Humanoid Robot Motion Generation and Control |
| 会议/期刊 | arXiv 2026 |
| Links | [paper](https://arxiv.org/abs/2602.07439v1) · [Project](https://text-op.github.io/) · [paper](https://arxiv.org/abs/2505.08712) · [Code](https://github.com/microsoft/onnxruntime) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TextOp |
| Dataset | BABEL validation set, Generator-produced motion sequences |

> [!tip] 效果简介
> - BABEL validation set (interactive motion generation) 上，Segment FID ↓ 3.072 (TextOp) vs 4.837 (DART+Retarget) (-1.765)；R@1 ↑ 0.300 vs 0.230 (DART+Retarget) (+0.070)。
> - Generator-produced motion sequences (simulation) 上，Success Rate (Succ) ↑ 0.814 (TextOp-M+G) vs 0.614 (TWIST2) (+0.200)；Root-relative MPJPE (mm) ↓ 34.665 (TextOp-M+G) vs 1019.826 (TWIST2) (-985.161)。

## 概要

**目标问题**：如何让通用人形机器人根据流式自然语言指令，实时、交互式地生成并执行物理可行的全向运动？现有方法或依赖预定义轨迹，或需要连续人工遥操作，无法支持用户在运行中随时修改文本命令并即时看到机器人的行为变化。

**核心方法**：TextOp 将任务分解为两层架构——高层**交互式运动生成器**（自回归潜扩散模型）根据历史运动帧和当前文本指令，以 6.25 Hz 频率自回归地生成短时域（8 帧）参考运动；低层**动态运动跟踪策略**（基于 PPO 训练的 MLP 网络）以 50 Hz 频率将参考运动转换为 29 自由度关节指令，在 Unitree G1 机器人上实时执行。关键设计包括：面向机器人骨架的自由度级局部增量运动表示（含 roll/pitch 三角编码），以及在跟踪器训练中混合动作捕捉数据与生成器产出运动以弥合分布差距。

**方法谱系与知识库定位**：TextOp 的运动生成模块沿袭 **DART** 的 VAE+潜扩散架构，但将其改造为自回归流式条件预测范式；运动表示方面，相比 **HumanML3D 风格表示**（Guo et al., CVPR 2022）、**RobotMDM**（Li et al., 2024）和 **BeyondMimic 扩散状态**（Chen et al., 2024），TextOp 的机器人骨架局部增量特征在段级和过渡级指标上均取得最优；跟踪策略方面，与 **TWIST2**（Luo et al., 2024）、**GMT**（Zhang et al., 2024）、**Any2Track**（Xu et al., 2024）等预训练跟踪器相比，TextOp 在生成运动上的跟踪成功率（0.814 vs. 0.614）和根相对 MPJPE（34.7 mm vs. 1019.8 mm）均大幅领先。

**主要结果**：
- **真实机器人**：在 30 秒连续运行中，面对随机和循环文本指令流，TextOp 保持高跟踪精度和成功率（Table I），端到端用户交互延迟平均仅 0.73 秒（Table II），并能在外部扰动下实时恢复稳定（Fig. 5）。
- **运动生成质量**：在 BABEL 验证集上，TextOp 的段级 FID 为 3.072，显著优于 DART+Retarget 的 4.837（Table III）。
- **消融验证**：自回滚训练提升过渡平滑度和分布匹配（Table XIII）；跟踪器训练中加入生成数据是提升生成运动上跟踪性能的关键（Table IV）。

**局限性**：TextOp 目前缺乏环境感知与物理推理能力，无法应对障碍物或动态场景；长期运动生成的一致性和命令歧义性在复杂指令流下仍可能退化。

### 问题背景

人形机器人因其类人的形态结构，理论上具备执行人类全部运动技能的潜力。然而，如何以自然、灵活且交互式的方式驱动通用人形机器人控制器，使其能够实时响应人类意图并生成物理可执行的全向运动，仍然是一个开放挑战。传统的人形机器人控制方法通常依赖预定义轨迹或连续的人类遥操作，这些方式要么缺乏对动态变化指令的适应能力，要么对操作者提出了极高的技能要求。

文本作为人类最自然的交互模态之一，为机器人运动控制提供了直观的接口。但将流式文本命令转化为物理机器人的连续全身运动，面临三个核心难题：

1. **生成与执行的语义鸿沟**：文本描述的是高层语义意图，而机器人需要的是关节级别的精确控制信号。现有文本驱动运动生成方法（如基于SMPL人体模型的扩散模型）虽然能产生视觉上合理的运动序列，但这些运动表示与真实机器人的关节约束、动力学特性之间存在显著的分布差距，直接重定向往往导致跟踪失败或运动失真。

2. **实时交互与运动连续性的冲突**：交互式控制要求系统能够在用户随时修改指令时立即响应，同时保持运动的物理连贯性。离线生成完整序列的方法无法满足这种流式交互需求，而简单的指令切换又会导致运动突变和失稳。

3. **从虚拟角色到物理机器人的迁移鸿沟**：在仿真中训练的运动生成器和跟踪器，部署到真实机器人时需要应对传感器噪声、执行器延迟、地面反作用力差异等现实因素，这对系统的鲁棒性提出了极高要求。

### 现有方法缺口

当前文本驱动人形机器人运动的研究可大致分为两类，但均存在明显局限：

- **基于人体运动先验的方法**：这类工作先利用大规模人体运动捕捉数据训练文本条件生成模型（如MDM、MLD等扩散模型），再将生成的SMPL运动通过重定向映射到机器人关节空间。代表方法包括**DART+Retarget**等。其根本问题在于，SMPL模型假设球面关节和自由浮动根节点，而真实人形机器人（如Unitree G1）的关节多为单自由度铰链，且受限于关节限位和动力学约束。这种表示层面的不匹配导致重定向后的运动在物理上不可执行，或需要额外的优化步骤。

- **基于强化学习的跟踪方法**：如**TWIST2**、**GMT**、**Any2Track**等，通过训练仿真中的全身跟踪策略来执行参考运动。但这些方法通常依赖动作捕捉数据作为参考，缺乏对文本指令的直接响应能力；当面对生成器产生的新运动时，由于训练分布不匹配，跟踪成功率急剧下降（例如TWIST2在生成运动上的成功率仅为0.614，根相对MPJPE高达1019.826 mm，见Table IV）。

更关键的是，上述两类方法缺乏有效的协同设计：运动生成器不了解机器人的物理约束，跟踪器也未针对生成运动的分布特性进行适配，导致整个管线在真实部署时性能大幅衰减。

### 本文动机

针对上述缺口，TextOp提出了一种端到端的文本驱动人形机器人运动生成与控制框架，其核心动机在于：

1. **统一生成与执行的表示空间**：直接在机器人骨架的运动表示上训练文本条件生成模型，从根本上消除从人体模型到机器人模型的重定向误差。该表示采用基于自由度的局部增量特征，并引入三角函数编码处理根节点的滚转和俯仰，以适配人形机器人的单自由度关节结构。

2. **实现流式交互式运动生成**：将交互式文本驱动运动生成建模为一种自回归条件预测问题——高层运动扩散模型根据历史运动帧和当前文本命令，增量式地生成短时域（8帧）参考运动，使用户能够随时修改指令并立即观察到运动变化。

3. **构建域自适应的跟踪策略**：在跟踪器的强化学习训练中，不仅使用动作捕捉数据，还大量引入生成器产生的运动片段（共计5,368个片段，31.48小时），使策略学会跟踪生成运动的分布特性，从而在部署时实现从虚拟角色到真实机器人的无缝迁移。

通过上述设计，TextOp在真实Unitree G1机器人上实现了端到端平均0.73秒的交互延迟，能够在30秒连续运行中保持高成功率和跟踪精度，并支持舞蹈、跳跃、乐器演奏、表达性手势等多种技能的实时文本驱动切换。

## 核心方法与创新机理

TextOp 的核心创新在于将**流式文本驱动的交互式运动生成**与**基于强化学习的全身运动跟踪**无缝结合，并通过**机器人骨架运动表示**和**生成数据增强**弥合虚拟角色与真实人形机器人之间的分布差距。其关键创新点体现在以下几个维度：

### 1. 流式文本驱动的自回归运动生成范式

传统方法将运动生成视为离线全序列生成任务，从静态文本提示一次性生成完整运动序列，无法响应实时变化的用户指令。TextOp 将问题重新定义为**自回归短时域条件预测**：高层运动生成器 $\mathbf{G}$ 根据历史运动帧 $\boldsymbol{x}_{t-T_{\mathrm{history}}:t-1}^{\mathrm{ref}}$ 和当前语言命令 $\boldsymbol{l}_t$，增量式地生成未来 8 帧参考运动 $\boldsymbol{x}_{t:t+T_{\mathrm{future}}-1}^{\mathrm{ref}}$（生成频率 6.25 Hz）。这一设计使得机器人能够在用户实时修改文本命令时平滑切换动作，端到端交互延迟仅为 0.73 秒（Table II），满足实时交互需求。

生成器采用 **VAE + 潜扩散模型（LDM）** 的 DART 架构，并在训练中引入**自回滚策略**（self-rollout）：连续处理 $N$ 个重叠运动片段，每个片段的历史帧随机替换为前一片段的预测未来帧。这一策略有效缩小了训练时使用真实历史与推理时使用生成历史之间的分布差距，消融实验表明自回滚训练显著提升了过渡平滑度和分布匹配质量（Table XIII）。

### 2. 机器人骨架运动表示

现有运动生成方法通常采用 HumanML3D 风格或基于 SMPL 的全局位置/速度特征，这些表示假设球形关节和连续自由度，与人形机器人受限的单自由度关节结构存在本质差异。TextOp 提出**基于自由度的局部增量机器人骨架特征**：

$$f_t = \big[{\phi}(\boldsymbol{r}_t), \Delta{\psi}_t, c_t, \Delta p_t^{\mathrm{local}}, h_t, q_t, \Delta q_t\big]$$

其中 $\phi(\boldsymbol{r}_t) = [\sin(\mathrm{roll}_t), \cos(\mathrm{roll}_t)-1, \sin(\mathrm{pitch}_t), \cos(\mathrm{pitch}_t)-1]$ 为根关节横滚和俯仰角的连续三角函数编码，其余分量为偏航角增量、脚部接触状态、局部位置增量、根高度、关节位置及增量。该表示直接编码机器人骨架的物理约束，避免了从 SMPL 到机器人骨架的重定向误差。

Table III 的对比实验显示，该表示在 BABEL 验证集上的段级 FID 达到 3.072，显著优于 DART+Retarget（4.837）和 RobotMDM 等替代方案，验证了机器人特定表示对生成质量的关键作用。

### 3. 生成数据增强的跟踪策略训练

传统运动跟踪策略仅使用动作捕捉数据训练，当部署到生成器产生的运动上时面临严重的分布偏移。TextOp 将**生成器产生的运动数据纳入跟踪器训练**：在 PPO 训练中混合使用动作捕捉数据和生成器产生的 5,368 个运动片段（总计 31.48 小时）。Table IV 显示，这一策略（TextOp-M+G）相比仅用动捕数据训练（TextOp-M），在生成运动上的跟踪成功率从 0.614 提升至 0.814，根相对 MPJPE 从 1019.826 mm 大幅降至 34.665 mm，同时语义对齐指标也显著改善。

值得注意的是，Table V 进一步揭示了泛化性能的权衡：仅在生成数据上训练会降低对未见动捕数据的泛化能力，而混合训练在部署性能和泛化能力之间取得了更优的平衡。

### 4. 从仿真到真机的端到端部署管线

TextOp 构建了完整的实时部署管线：用户文本经 CLIP 编码后通过网络发送至运动生成器，生成器以 6.25 Hz 输出参考运动，跟踪策略在机器人机载计算机上以 50 Hz 执行关节指令。Table I 显示，在 30 秒真机运行中，TextOp 在随机指令流下达到 80% 成功率（16/20），在循环指令下达到 100% 成功率，并在外部扰动下展现出实时恢复能力（Fig. 5）。

**创新局限性**：TextOp 目前缺乏显式环境感知和物理推理能力，无法适应障碍物或动态环境；长期运动生成的一致性和命令歧义性在复杂指令流下仍可能导致性能下降。

TextOp 将“实时文本驱动人形机器人运动生成与控制”分解为两个紧密协同的层级：**交互式运动生成**（Interactive Motion Generation）与**动态运动跟踪**（Dynamic Motion Tracking），并通过一个**运行时部署管线**将二者桥接，实现从流式文本输入到物理机器人关节指令的端到端闭环（Fig. 2）。

![[assets/figures/papers/paper_list_l64_https_arxiv_org_abs_2602_07439v1/figures/002_Figure_2.jpg]]
*Figure 2: Overview of TextOp’s framework. The framework consists of three main parts: (a) Interactive Motion Generation, including VAE training and LDM training, which together model future reference motion sequences conditioned on history motion and text prompt in an autoregressive style; (b) Dynamic Motion Tracking, where the MLP-based policy π takes reference motions and robot states to generate joint actions, trained in the simulation for stable execution; (c) Deployment, where the real-time user text prompt is converted into motions by the generator, translated into actions by the tracking policy based on the robot state, and executed on the physical robot*

### 系统总览与数据流

系统的核心逻辑可概括为两条公式化描述：

高层运动生成器 $\mathbf{G}$ 根据历史运动帧与当前语言命令，自回归地预测未来短时域参考运动序列：

$$
\boldsymbol{x}_{t:t+T_{\mathrm{future}}-1}^{\mathrm{ref}} = \mathbf{G}\big(\boldsymbol{x}_{t-T_{\mathrm{history}}:t-1}^{\mathrm{ref}}, \boldsymbol{l}_t\big)
$$

低层跟踪策略 $\pi$ 将参考运动转化为可执行的关节级控制信号：

$$
a_t = \pi\big(x_{t-1}^{\mathrm{robot}}, a_{t-1}, x_{t:t+T_{\mathrm{ref}}-1}^{\mathrm{ref}}\big)
$$

在运行时，用户输入的文本命令经 CLIP 编码后送入运动生成器，生成器以 6.25 Hz 的频率产出 8 帧参考运动；跟踪策略在机器人板载计算机上以 50 Hz 运行，根据当前机器人状态与参考运动实时计算关节动作，驱动 Unitree G1（29 自由度）执行。

### 模块职责与协同机制

**交互式运动生成器**采用 VAE + 潜扩散模型（LDM）的架构，遵循 DART 设计范式。它将运动生成建模为自回归的条件预测问题：每个生成步以过去 $T_{\mathrm{history}}=2$ 帧的历史运动与当前文本提示为条件，预测未来 $T_{\mathrm{future}}=8$ 帧的机器人运动。推理时应用无分类器引导（$\sigma_{\mathrm{CFG}}=5$）以增强语义对齐。训练阶段引入自回滚（self-rollout）策略——在连续运动片段之间随机替换历史帧为前一段的预测结果——以缩小训练与推理间的分布差距。

**动态运动跟踪策略**是一个基于 MLP 的全身跟踪控制器，在 IsaacLab 仿真环境中使用 PPO 训练。其关键设计在于训练数据的构成：除动作捕捉数据外，还纳入了生成器产生的运动片段（共 5,368 个片段，31.48 小时），使策略在部署时对生成运动的分布具有更强的适应性。

**运行时部署管线**负责流式文本编码、网络通信、运动缓冲同步与执行调度。端到端用户交互延迟平均为 0.73 秒（Table II），其中文本编码仅需约 7.6 ms，满足实时交互需求。

### 关键设计决策

整个框架围绕一个核心洞察展开：**将交互式文本驱动运动生成视为流式条件预测问题，并通过机器人特定运动表示和域自适应训练，实现从虚拟角色到真实人形机器人的实时部署**。这体现在两个相互配合的设计选择上：

1. **机器人骨架运动表示**：摒弃基于 SMPL 或 HumanML3D 风格的全局位置/速度特征，转而采用基于自由度（DoF）的局部增量特征，包含三角函数编码的 roll 与 pitch、局部位置增量、关节角度与角速度等，直接匹配人形机器人受约束的单自由度关节结构。

2. **生成数据增强训练**：在跟踪器训练中混合动作捕捉数据与生成器产出，弥合参考运动分布与策略训练分布之间的差距，使策略在生成运动上仍能保持高跟踪精度与语义一致性。

这两个设计相互支撑：机器人骨架表示使生成器能够产出物理上更可行的参考运动，而生成数据增强则确保跟踪器能够可靠地执行这些运动，二者共同构成了从文本意图到物理执行的完整闭环。

TextOp 将交互式文本驱动人形机器人运动生成与控制分解为两个核心模块：**交互式运动生成器**（Interactive Motion Generator）和**动态运动跟踪策略**（Dynamic Motion Tracking Policy），并通过一个运行时部署管线将二者串联为实时系统（Fig. 2）。

### 高层：交互式运动生成器

高层运动生成器 $\mathbf{G}$ 的任务是：给定历史运动帧 $\boldsymbol{x}_{t-T_{\mathrm{history}}:t-1}^{\mathrm{ref}}$ 和当前语言命令 $\boldsymbol{l}_t$，自回归地预测未来短时域参考运动序列：

$$
\boldsymbol{x}_{t:t+T_{\mathrm{future}}-1}^{\mathrm{ref}} = \mathbf{G}\big(\boldsymbol{x}_{t-T_{\mathrm{history}}:t-1}^{\mathrm{ref}}, \boldsymbol{l}_t\big)
$$

生成器采用 **DART** 架构（VAE + 潜扩散模型 LDM），两者均为 Transformer 网络。其关键创新在于**机器人骨架运动表示**——不同于 HumanML3D 或 SMPL 风格的特征，TextOp 使用基于自由度（DoF）的局部增量特征。每帧运动特征 $f_t$ 定义为：

$$
f_t = \big[{\phi}(\boldsymbol{r}_t), \Delta{\psi}_t, c_t, \Delta p_t^{\mathrm{local}}, h_t, q_t, \Delta q_t\big]
$$

其中各分量含义如下：
- $\boldsymbol{r}_t$：根部姿态的 roll 和 pitch，通过三角函数编码 $\phi(\boldsymbol{r}_t) = [\sin(\mathrm{roll}_t), \cos(\mathrm{roll}_t)-1, \sin(\mathrm{pitch}_t), \cos(\mathrm{pitch}_t)-1]$ 实现连续表示；
- $\Delta\psi_t$：根部偏航角的增量；
- $c_t$：脚部接触标签；
- $\Delta p_t^{\mathrm{local}}$：局部坐标系下的根部位置增量；
- $h_t$：根部高度；
- $q_t$：关节位置；
- $\Delta q_t$：关节位置增量。

该表示直接反映人形机器人受约束的单自由度关节结构，避免了从 SMPL 到机器人骨架的重定向误差（Table III, Table XII）。

LDM 训练采用标准 DDPM 前向加噪过程：

$$
q(z_{1:K}|z_0) = \prod_{k=1}^K \mathcal{N}(z_k; \sqrt{1-\beta_k}z_{k-1}, \beta_k I)
$$

推理时应用无分类器引导（classifier-free guidance），引导强度 $\sigma_{\mathrm{CFG}}=5$，以增强生成运动与文本语义的对齐：

$$
\hat{z}_0 = F_\theta(z_k, k, f_{t-T_{\mathrm{history}}:t-1}, \mathcal{O}) + \sigma_{\mathrm{CFG}} \cdot \big(F_\theta(z_k, k, f_{t-T_{\mathrm{history}}:t-1}, e_t) - F_\theta(z_k, k, f_{t-T_{\mathrm{history}}:t-1}, \mathcal{O})\big)
$$

为缩小训练与推理的分布差距，LDM 训练采用**自回滚策略**（self-rollout）：连续 $N$ 个重叠运动片段顺序处理，每个片段的历史随机替换为前一片段的预测未来（Table XIII 消融验证了回滚训练的有效性）。生成器以 6.25 Hz 输出 8 帧参考运动（$T_{\mathrm{future}}=8$），历史窗口 $T_{\mathrm{history}}=2$。

### 低层：动态运动跟踪策略

低层跟踪策略 $\pi$ 是一个 MLP 网络，在 IsaacLab 仿真中使用 PPO 训练，以 50 Hz 在机器人机载计算机上执行。其输入为前一帧机器人状态 $x_{t-1}^{\mathrm{robot}}$、前一动作 $a_{t-1}$ 和参考运动序列 $x_{t:t+T_{\mathrm{ref}}-1}^{\mathrm{ref}}$，输出关节指令：

$$
a_t = \pi\big(x_{t-1}^{\mathrm{robot}}, a_{t-1}, x_{t:t+T_{\mathrm{ref}}-1}^{\mathrm{ref}}\big)
$$

跟踪奖励采用基于跟踪误差的负指数形式：

$$
r_i = \exp(-\|e\|^2 / \sigma^2)
$$

训练数据的关键改进在于**混合使用动作捕捉数据和生成器产生的运动数据**（共 5,368 个片段，31.48 小时）。消融实验（Table IV）表明，仅用动作捕捉数据训练的跟踪器（TextOp-M）在生成运动上的成功率仅为 0.614，而加入生成数据的 TextOp-M+G 将成功率提升至 0.814，同时根相对 MPJPE 从 1019.8 mm 降至 34.7 mm，验证了域自适应训练的必要性。

### 运行时部署管线

部署管线（Fig. 2c）将上述模块串联：用户输入文本经 CLIP 编码后通过网络发送至运动生成器，生成器以自回归方式持续产生参考运动并存入运动缓冲区；跟踪策略从缓冲区读取参考运动，结合机器人当前状态实时计算关节指令。端到端用户交互延迟平均为 0.73 秒（Table II），其中文本编码仅需 7.64 ms，满足实时交互需求。

![[assets/figures/papers/paper_list_l64_https_arxiv_org_abs_2602_07439v1/figures/016_Table.jpg]]
*Table: XII: Comparison of motion representation components used by different methods. ✓ indicates the representation is used, × indicates it is not used. Components are reported based on the actual feature vectors used by each method, regardless of semantic overlap between each other. For the following tables, in the Unitree G1 skeleton, the term “Body” refers to 29 body links, excluding the root link, whereas in the SMPL skeleton it corresponds to 22 spherical joints. The “Base Frame” denotes the coordinate frame attached to the root link. In contrast, the “Character Frame” is a local frame aligned with the root’s yaw: its origin coincides with the root position, its yaw matches the root yaw, and...*

## 实验与关键发现

### 真实机器人部署：交互式连续技能执行

TextOp 在 Unitree G1（29 DoF）人形机器人上进行了真实世界部署验证。系统接收流式文本命令，在 30 秒的连续运行中执行了多种技能序列，包括舞蹈风格、跳跃行为、乐器演奏动作和表达性手势（Fig. 4, Fig. 7）。定量评估（Table I）表明，TextOp 在随机指令流和循环指令流下均保持了高成功率和跟踪精度：随机模式下 16/20 次试验成功，循环模式下“punch”和“play violin”均达到 10/10 成功。系统在外部扰动下展现出实时恢复能力——机器人根据受扰状态动态调整动作以保持稳定并完成文本驱动指令（Fig. 5）。

![[assets/figures/papers/paper_list_l64_https_arxiv_org_abs_2602_07439v1/figures/006_Figure_5.jpg]]
*Figure 5: Real-time recovery under external perturbations. The robot dynamically adjusts its actions based on perturbed states to preserve stability and fulfill text-driven commands*

![[assets/figures/papers/paper_list_l64_https_arxiv_org_abs_2602_07439v1/figures/004_Figure_4.jpg]]
*Figure 4: Continuous diverse skill execution in the real robot. The robot seamlessly performs a wide range of tasks, including multiple dance styles, dynamic jumping behaviors, instrument-playing motions, and expressive gestures. For complex longhorizon motions in the private dataset, the entire motion is assigned a unique label wrapped with*

端到端用户交互延迟平均为 **0.73±0.10 秒**（Table II），满足实时交互需求。延迟分解显示：文本编码仅需 7.64 ms，运动生成和策略推理为主要耗时环节，但整体流水线仍保持在可交互范围内。

### 运动生成质量评估

在 BABEL 验证集上，TextOp 的运动生成在段级（segment-level）和过渡级（transition-level）指标上均达到最优（Table III）。与 **DART+Retarget**（基于 SMPL 的 DART 生成器加运动重定向）相比，TextOp 的 **Segment FID** 从 4.837 降至 **3.072**（↓1.765），**R@1** 从 0.230 提升至 **0.300**（+0.070），表明生成运动与真实运动分布更接近且语义对齐更好。

运动表示消融（Table III, Table XIII）验证了机器人骨架运动表示的有效性：TextOp 的 DoF 级局部增量特征（含 roll/pitch 的三角函数编码）在段级 FID 和过渡级指标上均优于 HumanML3D-style 表示、BeyondMimic Diffusion State 和 RobotMDM 等替代方案。此外，自回滚训练（self-rollout）进一步提升了生成运动的过渡平滑度和分布匹配质量（Table XIII）。

### 运动跟踪策略评估

在生成器产生的运动序列上，仿真评估（Table IV）显示：在跟踪器训练中加入生成器产生的运动数据（**TextOp-M+G**）相比仅用动作捕捉数据训练（**TextOp-M**），跟踪成功率从 0.614 提升至 **0.814**（+0.200），根相对 MPJPE 从 1019.826 mm 降至 **34.665 mm**（↓985.161）。与预训练跟踪策略 **TWIST2**、**GMT**、**Any2Track** 相比，TextOp-M+G 在所有跟踪和语义指标上均取得最优或次优结果。

值得注意的是，仅在生成运动上训练的跟踪器（TextOp-G）在未见过的动作捕捉数据（SnapMoGen）上泛化能力下降（Table V），而混合训练（TextOp-M+G）在部署性能和泛化能力之间取得了更好的权衡。这一发现揭示了训练数据构成对 sim-to-real 迁移的关键影响。

### 消融与关键设计选择

- **历史与未来帧长度**：历史长度 $T_{\text{history}}=2$ 和未来长度 $T_{\text{future}}=8$ 在段级和过渡级指标间取得了最佳平衡（Table XIII）。
- **自回滚训练**：在 LDM 训练中采用自回滚策略（rollout probability），显著降低了生成器自回归推理时的分布偏移，提升了过渡平滑度（Table XIII）。
- **运动表示组件**：Table XII 系统比较了各方法的运动表示组件使用情况，TextOp 的表示涵盖全局位置、局部增量、三角函数编码的 roll/pitch、关节角度和角速度，在表征能力和机器人物理约束之间取得了平衡。

### 公平性说明与局限

- 与预训练跟踪策略（TWIST2、GMT、Any2Track）的比较使用了官方发布的检查点，但训练数据、仿真平台和域随机化设置可能不完全一致，定量提升主要来自仿真研究。
- 运动生成评估在 BABEL 验证集上进行，该集的文本注释偏向于动作类别，与其他生成模型的比较可能受数据分割影响。
- TextOp 目前缺乏显式的环境感知和交互式物理推理能力，无法适应障碍物、物体或动态环境。长期运动生成的一致性和命令歧义性可能在复杂指令流下导致性能下降，这些是未来工作需要解决的关键问题。

![[assets/figures/papers/paper_list_l64_https_arxiv_org_abs_2602_07439v1/figures/008_Table.jpg]]
*Table: III: Comparison of motion generation with different motion representations. Our method achieves the best overall performance across most segment- and transition-level metrics. Rightarrow “→” denotes that closer alignment with the dataset reference is better. Bold and underlined values indicate the best and second-best results, respectively, excluding the dataset. All results are reported as mean ± standard deviation over three generator rollout seeds*

![[assets/figures/papers/paper_list_l64_https_arxiv_org_abs_2602_07439v1/figures/017_Table.jpg]]
*Table: XIII: Ablation study on key hyperparameters for Motion Generation. All results are reported as mean ± standard deviation over three generator rollout seeds*

## 定位与知识库关联

### 1. 方法谱系：从离线生成到实时交互式部署

TextOp的技术路线可被理解为将**文本驱动的人体运动生成**与**基于强化学习的运动跟踪**两大技术流进行深度耦合，并针对人形机器人的实时交互场景进行了系统性改造。其核心贡献在于填补了“流式文本意图”与“物理可执行的全向运动”之间的鸿沟，而非在单一模块上提出全新的生成或控制范式。

**运动生成模块**直接继承了**DART**的VAE+潜扩散模型（LDM）架构，但对其进行了关键的交互式改造。传统的DART等离线生成方法从静态文本提示生成完整序列，而TextOp将其重构为**自回归短时域预测器**：以2帧历史运动为条件，预测未来8帧参考运动（6.25 Hz）。这一设计将运动生成从“一次性生成”转变为“流式条件预测”，使得生成器能够响应实时变化的文本命令。此外，TextOp引入了**自回滚训练策略**（self-rollout training），在LDM训练过程中随机用上一段的预测未来替换当前段的历史条件，从而缩小了训练时的“教师强制”与推理时的自回归执行之间的分布差距。消融实验（Table XIII）证实，自回滚训练显著提升了生成运动的过渡平滑度和分布匹配质量。

**运动表示**的选择是TextOp区别于现有工作的另一关键设计。现有方法普遍采用**HumanML3D风格的表示**（Guo et al., CVPR 2022 ）或基于SMPL的全局位置/速度特征，这些表示针对人体骨骼设计，包含大量球面关节的冗余自由度。TextOp则采用了**机器人骨架的局部增量运动表示**（Table XII），仅包含单自由度关节的位置、速度、增量变化，以及根节点的局部增量位移和滚转/俯仰的三角函数编码。这一表示不仅与Unitree G1的29自由度关节结构精确对齐，还避免了从SMPL到机器人骨架的显式重定向步骤及其引入的误差。Table III的对比实验表明，该表示在BABEL验证集上的段级FID（3.072）显著优于**DART+Retarget**（4.837）和**RobotMDM**等替代方案。

**运动跟踪模块**基于PPO训练的MLP策略，在IsaacLab仿真环境中学习将参考运动转化为关节指令。与现有跟踪方法（如**TWIST2** 、**GMT** 、**Any2Track** ）的关键区别在于训练数据的构成。传统跟踪策略通常仅在动作捕捉数据上训练，而TextOp的跟踪器训练数据中**混合了生成器产生的运动片段**（5,368个片段，31.48小时）。Table IV的消融实验表明，这一域自适应训练策略（TextOp-M+G）在生成运动上的跟踪成功率从纯动作捕捉训练（TextOp-M）的0.614提升至0.814，根相对MPJPE从1019.83 mm降至34.67 mm。这一结果揭示了生成运动与动作捕捉运动之间存在显著的分布差异，而通过将生成数据纳入训练可以有效地弥合这一差距。

### 2. 适用边界与局限

TextOp的适用边界由其设计假设和实验覆盖范围共同界定：

**适用场景**：TextOp适用于需要**实时、交互式文本驱动**的人形机器人运动生成与控制任务，特别是那些涉及多种技能序列（舞蹈、跳跃、手势、乐器演奏等）且允许用户在线修改指令的场景。其端到端交互延迟平均为0.73秒（Table II），满足实时交互需求。在30秒的真实机器人连续运行中，TextOp在随机和循环指令流下均保持了较高的跟踪成功率和精度（Table I）。

**核心局限**：

1. **缺乏环境感知与物理推理**：TextOp目前不具备显式的环境感知能力，无法对障碍物、物体或动态环境做出反应。这意味着它无法处理需要与环境进行物理交互的任务（如抓取、避障），其“交互式”仅限于文本命令层面，而非物理环境层面。

2. **长期一致性与命令歧义**：尽管自回滚训练改善了过渡平滑度，但在复杂指令流下，长期运动生成的一致性和命令歧义性仍可能导致性能下降。这一局限在BABEL数据集的文本注释偏向于动作类别标签的背景下尤为突出——生成器在语义模糊或组合指令上的表现可能弱于简单动作指令。

3. **泛化与部署鲁棒性的权衡**：Table V的结果揭示了训练数据构成的微妙权衡。仅在生成数据上训练的跟踪器（TextOp-G）在未见过的动作捕捉数据（SnapMoGen）上表现出泛化能力下降，而混合训练（TextOp-M+G）则在部署性能和泛化能力之间取得了更好的平衡。如何系统地调整动作捕捉数据与生成数据的比例以实现最优权衡，仍是一个开放问题。

4. **基线比较的局限性**：与预训练跟踪策略（TWIST2、GMT、Any2Track）的比较使用了官方发布的检查点，但训练数据、仿真平台和域随机化设置可能不完全一致。此外，在真实机器人评估中，基线方法未直接部署比较，因此定量提升主要来自仿真研究。

### 3. 开放问题

基于上述分析，TextOp留下的开放问题可归纳为三个方向：

1. **环境感知与物理推理的整合**：如何将视觉感知、物体交互和物理推理能力整合进文本驱动的运动生成框架，使机器人能够在动态环境中执行更通用的交互式任务？这可能需要将当前的“文本到运动”管线扩展为“文本+感知到运动+交互”的多模态框架。

2. **生成数据与真实数据的域自适应**：TextOp-G在未见过的动作捕捉数据上的具体失败模式是什么？这些失败是否源于生成运动的物理不可行性、分布偏移，还是跟踪策略的过拟合？如何通过改进运动表示、数据增强或域随机化来缓解这些问题？

3. **交互式控制的更细粒度评估**：当前的评估主要关注段级和过渡级指标，但实时交互式控制的核心价值在于命令切换的响应速度和语义保真度。如何设计更细粒度的评估协议，量化“命令切换延迟”“语义过渡自然度”和“用户意图对齐度”等交互式指标，是推动该方向发展的关键。

## 原文 PDF

![[paperPDFs/arxiv_2026/TextOp_Real_time_Interactive_Text_Driven_Humanoid_Robot_Motion_Generation_and_Control.pdf]]
