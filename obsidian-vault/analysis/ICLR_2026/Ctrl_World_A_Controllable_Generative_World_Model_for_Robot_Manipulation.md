---
title: "Ctrl-World: A Controllable Generative World Model for Robot Manipulation"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Ctrl_World_A_Controllable_Generative_World_Model_for_Robot_Manipulation_d904ad23051f.pdf
project_link: "https://ctrl-world.github.io"
code_link: null
aliases:
- CW
- Ctrl-World
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 联合多视图预测（含腕部相机）、帧级动作条件化与姿态条件记忆检索的协同设计。
primary_logic: 将预训练视频扩散模型适配为可控、多视图、长时一致的世界模型，可在想象空间中准确评估策略指令遵循能力，并通过合成成功轨迹进行监督微调，显著提升策略在未见任务中的表现。
claims:
- 多视图联合预测捕获更全面的场景表示，并满足现代VLA策略的输入格式。
- 帧级动作条件化使视觉动态与高频控制信号紧密对齐。
- 姿态条件记忆检索通过引入稀疏历史帧和帧间交叉注意力，稳定了长时rollout并保持时序一致性。
- 想象空间中的评估结果与真实世界的指令遵循能力排名高度相关。
---

# Ctrl-World: A Controllable Generative World Model for Robot Manipulation

> [!tip] 核心洞察
> 将预训练视频扩散模型适配为可控、多视图、长时一致的世界模型，可在想象空间中准确评估策略指令遵循能力，并通过合成成功轨迹进行监督微调，显著提升策略在未见任务中的表现。

| 字段 | 内容 |
|------|------|
| 中文题名 | Ctrl-World：一种用于机器人操作的可控生成世界模型 |
| 英文题名 | Ctrl-World: A Controllable Generative World Model for Robot Manipulation |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=748bHL2BAv) · [Project](https://ctrl-world.github.io) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | Ctrl-World |
| Dataset | DROID validation set, 10-second interactive trajectories, Downstream tasks |

> [!tip] 效果简介
> - DROID validation set, 10-second interactive trajectories (256 clips) 上，PSNR (第三视角相机) 23.56 vs 21.36 (IRASim-Single-View) (+2.20)。
> - DROID validation set, 10-second interactive trajectories 上，FVD (第三视角相机) 97.4 vs 138.1 (IRASim-Single-View) (-40.7)。
> - Downstream tasks (spatial/shape/novel instructions) 上，Success rate 83.4% (after post-training) vs 38.7% (pretrained π0.5) (+44.7%)。

## 概述

通用机器人策略的评估与迭代改进长期受困于真实世界试验的高成本与低扩展性。现有动作条件世界模型（如 **WPE** (Quevedo et al., 2025) 与 **IRASim** (Zhu et al., 2024)）仅支持单视图预测，缺乏精细的帧级控制，且长时一致性不足，无法与现代多视图 VLA（Vision-Language-Action）策略进行闭环交互。这构成了一个关键瓶颈：**策略评估与改进无法在“想象空间”中可靠完成**。

**Ctrl-World** 针对上述瓶颈，将预训练视频扩散模型适配为一个可控、多视图、长时一致的生成式世界模型。其核心设计围绕三个协同的因果调节维度展开：

1. **联合多视图预测**：同时预测两个第三视角与一个腕部视角，捕获更全面的场景表示，并天然匹配现代 VLA 策略的输入格式。
2. **帧级动作条件化**：将 Cartesian 空间动作块通过帧间交叉注意力注入每一帧，使视觉动态与高频控制信号紧密对齐。
3. **姿态条件记忆检索**：从历史中采样稀疏关键帧，利用帧间交叉注意力嵌入对应机器人姿态，重锚预测至相似历史状态，从而稳定长时 rollout 并保持时序一致性。

在想象空间中，Ctrl-World 对策略指令遵循能力的评估结果与真实世界排名高度相关。进一步地，通过在世界模型中合成成功轨迹并进行监督微调，策略在空间理解、形状理解、新指令等未见任务上的成功率平均提升 **44.7%**（从预训练 π₀.₅ 的 38.7% 提升至 83.4%）。

在方法谱系上，Ctrl-World 属于**基于预训练视频扩散模型的动作条件世界模型**，其关键区别于既有工作在于：从单视图预测扩展到多视图联合生成，从粗粒度条件化升级为帧级动作注入，并引入显式的姿态记忆机制以解决长时遗忘问题。该工作为“在想象中评估与改进通用机器人策略”提供了可扩展的范式，同时揭示了当前方法在精细交互、低层执行精度提升及自动化成功判定等方面的开放问题。

## 背景与动机

### 机器人策略评估的“真实世界瓶颈”

通用机器人操作策略（特别是基于视觉-语言-动作的 VLA 策略）的迭代开发面临一个根本性困境：评估与改进策略需要大量真实世界试验，而每一次物理部署都意味着高昂的时间成本、硬件磨损与安全风险。这一“真实世界瓶颈”严重制约了策略的规模化迭代——开发者难以快速判断一个策略变体是否比上一个更好，更难以低成本地发现策略在未见任务上的失败模式。

### 现有世界模型的三个缺口

一种自然的替代方案是构建**动作条件世界模型**（action-conditioned world model），让策略在“想象空间”中执行 rollout，从而将评估从物理世界迁移到仿真器中。然而，现有的动作条件视频预测方法存在三个关键缺口，使其无法与现代 VLA 策略进行有效的闭环交互：

**缺口一：单视图预测导致部分可观测性。** 现有方法如 **IRASim**（Zhu et al., 2024）和 **WPE**（Quevedo et al., 2025）仅从单一第三视角相机预测未来帧。这种单视图设置不仅丢失了场景的关键视觉信息（如遮挡区域），更与主流 VLA 策略的多视图输入格式不兼容——现代策略通常同时依赖第三视角和腕部相机观测来做出精确控制决策。

**缺口二：缺乏帧级精细控制。** 预训练视频扩散模型（如 Stable Video Diffusion）仅支持文本或图像条件，无法将高频动作信号精确注入每一帧的生成过程。这导致生成的世界动态与控制信号之间出现因果断裂——模型可能“看到”机械臂在移动，但移动的方向、幅度与给定动作指令并不一致。

**缺口三：长时一致性崩溃。** 在自回归 rollout 过程中，预测误差会逐步累积，导致数秒后的生成帧出现严重的视觉漂移和幻觉——物体凭空消失、机械臂姿态突变、场景布局扭曲。这使得现有方法难以支撑超过数秒的策略闭环评估。

### 本文动机：构建可控、多视图、长时一致的世界模型

针对上述缺口，本文提出 **Ctrl-World**——一个从预训练视频扩散模型适配而来的可控生成世界模型。其核心设计目标是将视频生成基础模型的强大先验转化为机器人策略的“想象引擎”，具体通过三项协同设计实现：

1. **联合多视图预测**：同时预测两个第三视角和一个腕部视角的未来帧，既捕获更全面的场景表示，又满足现代 VLA 策略的输入格式。
2. **帧级动作条件化**：将 Cartesian 空间动作块通过帧间交叉注意力注入每一帧，使视觉动态与控制信号紧密对齐。
3. **姿态条件记忆检索**：从历史帧中采样与当前机器人姿态相似的帧，通过交叉注意力重锚预测，稳定长时 rollout 并保持时序一致性。

凭借这三项设计，Ctrl-World 旨在实现两个关键能力：（1）在想象空间中准确评估策略的指令遵循行为，使其与真实世界表现高度相关；（2）通过合成成功轨迹对策略进行监督微调，显著提升策略在未见任务上的表现。

## 核心创新

Ctrl-World 的核心创新在于将预训练视频扩散模型系统性地改造为**可控、多视图、长时一致**的机器人世界模型，使其能够与现代 VLA（Vision-Language-Action）策略进行闭环交互。相较于现有动作条件世界模型（如 **WPE**（Quevedo et al., 2025）、**IRASim**（Zhu et al., 2024））仅支持单第三视角预测、缺乏精细帧级控制、长时一致性差的局限，Ctrl-World 通过以下三个关键设计实现突破：

### 1. 联合多视图预测

现有方法仅从单一第三视角相机预测未来帧，导致部分可观测性和幻觉问题（Figure 3）。Ctrl-World 将两个第三视角相机和一个腕部相机的输入 token 沿 token 维度拼接，**联合预测所有视图**。这一设计不仅捕获更全面的场景表示，还直接匹配现代 VLA 策略（如 π0.5）的多视图输入格式，使世界模型与策略之间能够实现无缝的闭环交互。

### 2. 帧级动作条件化

预训练视频扩散模型通常仅支持文本或图像条件，缺乏对高频控制信号的精细响应能力。Ctrl-World 引入了**帧级动作条件化机制**：将策略输出的未来动作块转换为 Cartesian 空间末端执行器姿态，通过帧间交叉注意力（frame-wise cross-attention）注入到空间 Transformer 的每一帧中。这使得视觉动态与控制信号紧密对齐，生成 rollout 能够准确反映每个动作的因果效应。消融实验表明，移除此机制会导致 PSNR 从 23.56 大幅下降至 21.20，FVD 从 97.4 升至 122.7（Table 2），验证了其对控制精度的关键作用。

### 3. 姿态条件记忆检索

长时 rollout 面临误差累积和时序一致性退化的问题。Ctrl-World 设计了**姿态条件记忆检索**：从历史帧中以固定间隔采样 k 帧（间隔 1-2 秒），将对应的机器人 Cartesian 姿态通过帧间交叉注意力嵌入到每帧预测中。这一机制使模型能够检索并重锚到相似的历史状态，稳定长时生成。Figure 4 左侧的注意力可视化显示，在预测 t=4s 帧时，模型对 t=0s 帧（具有相似姿态）表现出强注意力。消融实验中，移除记忆机制导致 PSNR 从 23.56 降至 23.06，FVD 从 97.4 升至 105.5（Table 2）。

### 高效适配策略

Ctrl-World 采用**参数高效微调**策略：仅新增一个 3 层 MLP（将 7 维 Cartesian 空间动作投影为 1024 维潜变量），冻结预训练 SVD 骨干网络的其他参数，在扩散损失上微调。这种轻量适配使得模型能够在 2×8 H100 GPU 上约 2-3 天完成训练，同时保留了预训练模型的泛化能力，使其能够零样本迁移到新的 DROID 场景和相机布局（Figure 6）。

三个创新组件的协同作用使得 Ctrl-World 能够生成超过 20 秒的连贯 rollout，并在想象空间中准确评估策略的指令遵循能力，为后续的策略改进（通过合成成功轨迹进行监督微调，成功率提升 44.7%）奠定了基础。

## 整体框架

Ctrl-World 是一个面向通用机器人策略的可控生成世界模型，其整体设计围绕“策略闭环 rollout”这一核心目标展开。如图1所示，系统接收多视图观测与语言指令，由策略产生动作块，世界模型根据当前观测与动作块预测未来多视图观测，从而在想象空间中完成策略评估与数据合成。

### 输入输出流

系统的输入由三部分组成：
- **多视图观测** $o_t$：包含两个第三视角相机与一个腕部相机的 RGB 图像，满足现代 VLA 策略的输入格式。
- **语言指令** $l$：描述任务目标（如“将绿色毛巾向左折叠”）。
- **初始机器人状态**：用于将策略输出的关节速度转换为 Cartesian 空间末端执行器姿态。

策略 $\pi$ 接收当前观测与指令，输出 $H$ 步动作块：
$$a_{t+1}, a_{t+2}, ..., a_{t+H} \sim \pi(\cdot | o_t, l)$$
世界模型 $W$ 以当前观测 $o_t$ 和动作块 $A_t$ 为条件，生成未来 $H$ 步的多视图预测：
$$o_{t+1}, ..., o_{t+H} \sim W(\cdot | o_t, A_t)$$
随后，将预测的最后一帧作为新的观测 $o_{t+H}$，策略再次采样动作，形成自回归闭环。在实验中，每次交互使用 15 步动作块（约 1 秒），自回归进行 10 轮，共生成 10 秒的交互轨迹。

### 模块关系与数据流

Ctrl-World 以预训练视频扩散模型（Stable Video Diffusion, SVD）为骨干，通过三个关键适配模块将其转化为可控、多视图、长时一致的世界模型（图2）：

1. **多视图联合预测**：将 $N$ 个视图的图像经 VAE 编码后沿 token 维度拼接，联合预测所有视图的未来帧。这使模型能够捕获跨视图的场景表示，避免单视图方法因部分可观测性产生的幻觉。

2. **帧级动作条件化**：策略输出的动作块经 Adapter 转换为 Cartesian 空间末端执行器姿态，再通过正向运动学得到关节位置。这些姿态信息通过帧间交叉注意力注入每一帧的生成过程，使视觉动态与高频控制信号紧密对齐。

3. **姿态条件记忆检索**：从历史帧中以间隔 $m$ 采样 $k$ 帧（共 7 帧，间隔 1–2 秒），将对应机器人姿态嵌入后，通过帧间交叉注意力作用于当前预测。该机制将预测重锚定到相似历史状态，稳定长时 rollout 并保持时序一致性。

### 训练与推理流程

**训练阶段**：仅新增一个 3 层 MLP（将 7 维 Cartesian 动作投影为 1024 维潜变量），冻结 SVD 骨干的其他参数，在 DROID 数据集（95,599 条轨迹）上以扩散损失进行微调：
$$\mathcal{L} = \mathbb{E}_{x_0, \epsilon, t'} \Vert \hat{x}_0(x_{t'}, t', c) - x_0 \Vert^2$$
其中 $c$ 为条件信息（历史帧、动作姿态），$x_0$ 为真实未来帧。训练在 2×8 H100 GPU 上约需 2–3 天，总 batch size 为 64。

**推理与策略改进**（Algorithm 1）：世界模型推理时，对给定指令 $l$ 和初始观测 $o_t$，自回归生成完整轨迹。合成轨迹由人工标注成功/失败，成功的轨迹构成 $D_s$。随后在 $D_s$ 上对策略进行监督微调：
$$\mathcal{L}_{\theta} = \mathbb{E}_{o_t, a_{t:t+H} \sim D_s} \Vert \pi_{\theta}(o_t, l) - a_{t:t+H} \Vert^2$$
这一闭环使策略能够从世界模型合成的成功经验中学习，在未见任务上平均提升 44.7% 的成功率（从 38.7% 到 83.4%，图9）。

### 与基线方法的架构差异

| 设计维度 | 基线方法 (WPE / IRASim) | Ctrl-World |
|---------|------------------------|------------|
| 视觉输入与预测 | 单第三视角相机 | 联合多视图（2 第三视角 + 1 腕部） |
| 动作条件化 | 无精细帧级条件 | 帧级交叉注意力注入 Cartesian 姿态 |
| 长时记忆 | 无显式记忆或有限历史帧 | 姿态条件记忆检索，采样 7 帧历史 |
| 基础模型适配 | 直接使用或全模型微调 | 仅训练动作投影 MLP，冻结骨干 |

这些设计使 Ctrl-World 在长时交互轨迹生成中显著优于基线：在 DROID 验证集上，PSNR 达到 23.56（IRASim 为 21.36），FVD 降至 97.4（IRASim 为 138.1）（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/001_Figure_1.jpg]]
*Figure 1: Ctrl-World is designed for policy-in-the-loop rollouts with generalist robot policies. It generates joint multi-view predictions (including wrist views), enforces fine-grained action control via frame-level conditioning, and sustains coherent long-horizon dynamics through pose-conditioned memory retrieval. These components enable (1) accurate policy evaluation in imagination, with alignment to real-world rollouts, and (2) targeted policy improvement through synthetic trajectories*

## 核心模块与公式推导

Ctrl-World 的架构建立在一个预训练视频扩散模型之上，通过三个关键适配模块将其转化为可控、长时一致的世界模型。图 Figure 2 展示了整体架构。

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/002_Figure_2.jpg]]
*Figure 2: Ctrl-World is initialized from a pretrained video diffusion model and adapted into a controllable, temporally consistent world model with: (1) Multi-view input and joint prediction for unified information understanding. (2) Memory retrieval mechanism, which adds sparse history frames in context and project pose information into each frame via frame-level cross-attention, re-anchoring predictions to similar past states. (3) Frame-level action conditioning to better align high-frequency action with visual dynamics*

### 多视图联合预测

为满足现代 VLA 策略的多视图输入格式并捕获更全面的场景表示，Ctrl-World 将多个相机视角的图像在 token 维度上拼接后进行联合预测。给定 N 个输入图像，每个包含 H×W 个 token，模型将它们沿 token 维度拼接，并联合预测所有视角的未来帧 $O_{t:t+H}$。这一设计使模型能够跨视角共享信息，避免单视图方法中因部分可观测性导致的幻觉问题。消融实验表明，取消多视图联合预测（仅预测单视图）会导致腕部相机 PSNR 从 19.18 降至 15.94，并增加生成幻觉（Table 2, Figure 3）。

### 帧级动作条件化

为实现精细的动作控制，Ctrl-World 将策略输出的动作块逐帧注入到视频扩散过程中。具体而言，策略输出的关节速度动作序列 $a_{t+1:t+H}^{\mathrm{jv}}$ 首先通过一个适配器转换为 Cartesian 空间末端执行器姿态序列 $q_{t+1:t+H}^{\mathrm{cartesian}}$，转换过程依赖正向运动学（Forward Kinematics）：

$$
q_{t+1:t+H}^{\mathrm{joint}} = \mathrm{Adapter}(q_t^{\mathrm{joint}}, a_{t+1:t+H}^{\mathrm{jv}}), \quad q_{t+1:t+H}^{\mathrm{cartesian}} = FK(q_{t+1:t+H}^{\mathrm{joint}})
$$

随后，这些 Cartesian 姿态通过一个仅含 3 层的 MLP（从 7 维投影至 1024 维潜在嵌入）进行编码，并经由空间 Transformer 中的帧间交叉注意力（frame-wise cross-attention）作用于每一帧。这种设计确保视觉动态与高频控制信号紧密对齐，使生成的 rollout 能够反映每个动作的因果效应。消融实验证实，移除帧级动作条件化会导致 PSNR 从 23.56 大幅下降至 21.20，FVD 从 97.4 升至 122.7（Table 2）。

### 姿态条件记忆检索

为稳定长时 rollout 并保持时序一致性，Ctrl-World 引入了姿态条件记忆检索机制。模型从历史帧中采样 k 帧（间隔为 m 步），将其作为上下文输入，并通过帧间交叉注意力将对应帧的机器人姿态信息嵌入到每个预测帧中。模型输入形式为拼接后的历史 token 与加噪未来帧：

$$
[o_{t-km}, ..., o_{t-m}, o_t, x_{t'}]
$$

这一机制使模型能够检索到与当前状态相似的历史帧，从而重新锚定预测。Figure 4 左侧的注意力可视化显示，在预测 t=4s 帧时，模型对 t=0s 帧（具有相似姿态）表现出强烈注意力，验证了记忆检索的有效性。消融实验中，移除记忆机制导致 PSNR 从 23.56 降至 23.06，FVD 从 97.4 升至 105.5（Table 2）。

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/006_Figure_4.jpg]]
*Figure 4: Controllability of Ctrl-World and ablations. Different action sequences can produce distinct rollouts in Ctrl-World with centimeter-level precision. Removing memory leads to blurry predictions (blue), while removing frame-level pose conditioning reduces control precision (purple). Attention visualization (left) when predicting the t = 4 s frame shows strong attention to the t = 0 s frame with the same pose, illustrating the effectiveness of memory retrieval. For clarity, each action chunk is expressed in natural language (e.g., “Z-axis -6 cm”). Due to space constraints, only the wrist-view is visualized for intermediate frames*

### 训练目标

Ctrl-World 的训练遵循扩散模型范式，仅新初始化动作投影 MLP 而冻结其他预训练参数。训练目标为最小化模型预测的干净数据 $\hat{x}_0$ 与真实未来帧 $x_0$ 之间的均方误差：

$$
\mathcal{L} = \mathbb{E}_{x_0, \epsilon, t'} \Vert \hat{x}_0(x_{t'}, t', c) - x_0 \Vert^2
$$

其中 $c$ 代表条件信息（包括历史帧、动作序列和记忆姿态），$t'$ 为扩散时间步。模型在 DROID 数据集（95,599 条轨迹）上训练，约需 2-3 天（2×8 H100 GPU，总 batch size 64）。

### 策略动作采样与交互闭环

在策略闭环交互中，给定多视图观测 $o_t$ 和语言指令 $l$，通用策略 $\pi$ 输出未来 H 步的动作序列：

$$
a_{t+1}, a_{t+2}, ..., a_{t+H} \sim \pi(\cdot | o_t, l)
$$

世界模型 $W$ 随后根据当前观测 $o_t$ 和动作块 $A_t$ 预测未来多视图观测：

$$
o_{t+1}, ..., o_{t+H} \sim W(\cdot | o_t, A_t)
$$

这一交互过程可自回归地重复多轮，生成长达数十秒的想象 rollout。

### 补充图表

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/007_Figure_5.jpg]]
*Figure 5: Consistency of Ctrl-World. Since the wrist camera’s field of view changes dramatically within a single trajectory, leveraging multi-view information and memory retrieval is essential for generating consistent wrist-view predictions. Prediction highlighted in the green box are inferred from other camera views, while those in the red box are retrieved from memory*

## 实验与分析

### 世界模型质量评估

为验证Ctrl-World作为交互式世界模型的生成质量，作者在DROID验证集上进行了10秒长时轨迹生成评估。评估协议为：随机采样初始帧，模型每次接收15步动作块（约1秒跨度），自回归生成10轮，最终在256个片段上平均。对比基线包括**WPE**（Quevedo et al., 2025）和**IRASim**（Zhu et al., 2024），两者均为单视图动作条件视频预测方法。

**表1**展示了第三视角相机下的定量结果。Ctrl-World在PSNR上达到23.56，较IRASim-Single-View的21.36提升+2.20；FVD降至97.4，较IRASim的138.1降低40.7。这一显著提升的核心原因在于多视图联合预测捕获了更全面的场景表示，帧级动作条件化使视觉动态与高频控制信号紧密对齐，而姿态条件记忆检索则稳定了长时rollout的时序一致性。

**图3**的定性对比进一步揭示了单视图方法的固有缺陷。由于仅依赖单一第三视角，WPE和IRASim在面对遮挡或需精细交互的场景时出现明显的幻觉——例如无法正确移动绿色毛巾或抓取红色碗。Ctrl-World通过联合预测第三视角与腕部视角，有效缓解了部分可观测性问题，生成的未来轨迹与真实值高度吻合。

### 可控性与一致性分析

**图4**展示了Ctrl-World的精细可控性。即使动作序列仅相差数厘米（如Z轴-6 cm），模型仍能生成明显不同的rollout。消融实验表明：移除记忆机制导致预测模糊，而移除帧级姿态条件化则显著降低控制精度。左侧注意力可视化显示，在预测t=4s帧时，模型对t=0s帧中具有相似机器人姿态的区域展现出强注意力，验证了姿态条件记忆检索的有效性——它将预测重新锚定到相似历史状态。

**图5**针对腕部相机的一致性分析表明，由于腕部相机视野在单条轨迹内剧烈变化，单视图方法难以维持一致性。Ctrl-World通过跨视图信息融合与记忆检索的双重机制，能够从其他相机视角推断被遮挡区域（绿色框），或从历史帧中检索相关信息（红色框），从而生成连贯的腕部预测。

### 消融实验

**表2**系统消融了Ctrl-World的三个核心组件，所有实验均在相同条件下进行以确保公平比较：

- **移除记忆机制**：PSNR从23.56降至23.06，FVD从97.4升至105.5。记忆检索通过引入稀疏历史帧并利用帧间交叉注意力嵌入姿态信息，对维持长时生成质量至关重要。
- **移除帧级动作条件化**：PSNR大幅降至21.20，FVD升至122.7。这表明将Cartesian空间动作块通过帧间交叉注意力注入每一帧，是实现精细视觉控制的关键机制。
- **取消多视图联合预测**（仅预测单视图）：腕部相机PSNR从19.18骤降至15.94，且幻觉现象增多。多视图联合预测不仅提升了各视图的预测精度，更通过跨视图信息互补增强了整体一致性。

### 想象空间中的策略评估

为验证Ctrl-World能否在想象空间中忠实反映策略的真实世界表现，作者将通用策略π0.5与Ctrl-World进行闭环交互（**图6**）。每条轨迹包含20次交互，值得注意的是，π0.5和Ctrl-World均能零样本泛化到新的DROID设置。

**图7**的定量相关性分析表明，世界模型中的指令遵循行为排名与真实世界高度相关。然而，模型倾向于低估执行成功率——这是一个需要关注的系统性偏差。

**表3**进一步细化了各方法在不同任务上的指令遵循率与成功率对比，为策略评估的可靠性提供了更全面的证据。

### 策略改进

基于Ctrl-World的策略改进流程如**算法1**所示：对指令和初始状态施加结构化扰动，在世界模型中执行rollout，通过人工偏好标注筛选成功轨迹构建合成数据集$D_s$，最后对策略进行监督微调。

**图8**展示了后训练任务示例及其对应的合成轨迹。世界模型能够生成成功与失败两种rollout，仅保留成功轨迹用于策略微调。训练目标为最小化动作预测的均方误差：

$$\mathcal{L}_{\theta} = \mathbb{E}_{o_t, a_{t:t+H} \sim D_s} \| \pi_{\theta}(o_t, l) - a_{t:t+H} \|^2$$

**图9**和**表4-7**展示了策略改进的核心结果。在预训练π0.5的基础上，利用合成成功轨迹进行监督微调后，策略在空间理解、形状理解、方向折叠毛巾和新物体等未见任务上的平均成功率从38.7%提升至83.4%，提升幅度达44.7%。这一结果有力地证明了Ctrl-World作为“想象训练场”的有效性——通过在世界模型中低成本地探索成功轨迹，策略能够习得在真实世界中难以通过试错获得的行为。

### 失败模式与局限性

尽管Ctrl-World展现出强大的能力，作者坦诚指出了若干失败模式：

1. **精细交互与长时推理**：模型在涉及精确物理交互或需要多步逻辑推理的任务上仍可能失败。
2. **初始观测敏感性**：模型性能对初始帧的质量和视角较为敏感，不同起始条件可能导致生成质量波动。
3. **已见指令的低级成功率**：当前世界模型的物理动态保真度尚不足以提升已见指令的低级执行精度，这暗示需要收集更多域内策略rollout数据以改进物理动态建模。
4. **合成轨迹评估依赖人工**：成功/失败判断仍需人工偏好标注，自动化的奖励模型设计仍是未来工作方向。

### 补充图表

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/003_Table_1.jpg]]
*Table 1: Quantitative results for interactive long-trajectory generation on the validation set. We evaluate our world model’s quality by generating 10-second trajectories. Given a randomly sampled initial frame, the model receives a 15-step action chunk (spanning over 1 second) in each interaction and generates for 10 rounds auto-regressively. The results are averaged over 256 clips*

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/005_Figure_3.jpg]]
*Figure 3: Qualitative results on long-horizon rollouts from the validation set. Prior models rely on single-view prediction, suffering from partial observability and hallucinations (e.g., failing to move the green towel or grasp the red bowl). In contrast, Ctrl-World jointly predicts from third-view and wrist-view cameras, yielding precise future trajectories aligned with the ground truth*

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/008_Figure_6.jpg]]
*Figure 6: Comparisons between*

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/009_Figure_7.jpg]]
*Figure 7: Quantitative correlations between real-world and world-model rollouts. The world model reliably captures instruction-following behavior but tends to underestimate the execution success rate*

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/010_Figure_8.jpg]]
*Figure 8: The top row illustrates examples of post-training tasks, while the bottom row presents synthetic trajectories generated within the world model. The world model can produce both successful and failed rollouts; we keep the successful trajectories and use them for policy fine-tuning*

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/011_Figure_9.jpg]]
*Figure 9: Policy improvement. Posttraining on synthetic data improves policy instruction-following by 44.7% on average*

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/012_Table_3.jpg]]
*Table 3: Comparison of instruction-following and success rate across methods and tasks*

![[assets/figures/papers/paper_list_l67_https_openreview_net_forum_id_748bHL2BAv/figures/013_Table_4.jpg]]
*Table 4: Policy improvement (Spatial Understanding)*

## 方法谱系与知识库定位

### 与现有方法的继承与差异

Ctrl-World 的架构根基是**预训练视频扩散模型**（Stable Video Diffusion, SVD），它继承了 SVD 在时空建模上的强大先验，但并非直接将其用作黑箱预测器。与两类最相关的现有方法相比，Ctrl-World 的核心差异体现在三个维度：

**相对于动作条件世界模型**：**WPE**（Quevedo et al., 2025）和 **IRASim**（Zhu et al., 2024）代表了将视频生成模型用于策略评估的早期尝试，但它们均以单第三视角相机为输入和预测目标。这一设计缺陷导致两个关键问题：其一，单视图无法覆盖完整场景状态，尤其当操作目标被遮挡或处于视野边缘时，生成质量急剧退化（Figure 3 中 IRASim 无法移动绿色毛巾即为典型失败模式）；其二，单视图格式与现代 VLA 策略（如 π0.5）的多视图输入要求不兼容，使得策略无法直接“在回路中”与这些世界模型交互。Ctrl-World 通过**联合多视图预测**（两个第三视角 + 一个腕部视角）从根本上解决了这一格式鸿沟，同时利用多视图间的信息互补抑制了单视图幻觉。

**相对于通用视频生成模型**：直接使用预训练 SVD 进行动作条件预测面临两个瓶颈——缺乏精细控制信号注入机制，以及长时自回归生成中的误差累积与一致性崩溃。Ctrl-World 的**帧级动作条件化**和**姿态条件记忆检索**正是针对这两个瓶颈的定向设计。帧级条件化将 Cartesian 空间动作块通过帧间交叉注意力作用于每一帧，使视觉动态与高频控制信号紧密对齐（消融实验中移除该机制导致 PSNR 从 23.56 骤降至 21.20，FVD 从 97.4 升至 122.7）。记忆检索则通过采样稀疏历史帧并将对应机器人姿态嵌入交叉注意力，为重锚预测提供“相似状态锚点”，从而稳定长时 rollout。

### 适用边界

Ctrl-World 的有效性建立在以下前提之上，超出这些边界时性能可能显著下降：

1. **训练数据覆盖**：模型在 DROID 数据集（95,599 条轨迹）上训练，其可控性受益于该数据集密集的动作空间覆盖。对于 DROID 分布之外的机器人形态、操作空间或动作模式，模型的泛化能力未经验证。

2. **任务类型**：当前验证集中在高层指令遵循行为（如空间理解、形状理解、方向折叠毛巾、新物体操作），而非低层执行精度。论文明确指出，Ctrl-World“不足以提升已见指令的低级成功率”，这意味着它更适合作为策略的指令理解能力评估器，而非执行精度优化器。

3. **初始观测敏感性**：模型性能对初始观测较为敏感，这暗示在分布外初始状态或极端视角下，生成质量可能不稳定。

4. **精细交互与长时推理**：涉及精细物理交互（如精密插入）或需要长时因果推理的任务是明确的失败模式。

### 局限与开放问题

**已确认的局限**：

- **物理动态保真度不足**：当前世界模型在模拟真实物理交互的精度上仍有欠缺，论文指出需要“收集更多域内策略 rollout 数据”以提升物理动态保真度。这暗示当前模型可能对接触力学、摩擦力等细粒度物理现象建模不足。
- **合成轨迹评估依赖人工标注**：在策略改进流程中，成功/失败轨迹的筛选仍依赖人工偏好判断，缺乏自动化的奖励模型。这限制了大规模迭代改进的可扩展性。
- **策略评估的保守偏差**：Figure 7 显示，世界模型中的策略成功率倾向于低估真实世界的执行成功率，这可能源于生成轨迹中的伪影或物理建模偏差。

**开放问题**：

1. **迭代协同改进**：论文提出了一个“鸡与蛋”问题——更好的世界模型需要更多策略 rollout 数据，而更好的策略又能产生更高质量的数据。如何设计迭代式的策略 rollout 与微调循环，使世界模型和策略同步提升，是一个核心开放问题。

2. **技能学习的扩展性**：当前验证集中在指令遵循这一高层技能维度。生成式世界模型能否扩展至其他技能学习目标，如低层执行精度提升、接触丰富操作、或力控任务，仍有待探索。

3. **自动化评估闭环**：结合大型视觉-语言模型（VLM）实现自动化的成功/失败判断，是消除人工标注瓶颈的关键方向。这一闭环的实现将使得从“想象空间评估”到“想象空间训练”的流水线完全自动化成为可能。

4. **跨形态泛化**：当前方法针对固定三相机配置设计，对于不同数量的相机、不同的安装位置、或单目移动操作场景的适配能力未经验证。多视图联合预测架构能否灵活适配可变视图配置，是一个有待回答的工程与理论问题。

## 原文 PDF

![[paperPDFs/ICLR_2026/Ctrl_World_A_Controllable_Generative_World_Model_for_Robot_Manipulation_d904ad23051f.pdf]]
