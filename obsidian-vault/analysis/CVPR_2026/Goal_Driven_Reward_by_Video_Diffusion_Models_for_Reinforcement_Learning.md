---
title: Goal-Driven Reward by Video Diffusion Models for Reinforcement Learning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Goal_Driven_Reward_by_Video_Diffusion_Models_for_Reinforcement_Learning.pdf
project_link: "https://qiwang067.github.io/genreward"
code_link: null
aliases:
- GDRBVDMRL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用预训练视频扩散模型生成的目标条件视频来提供内在奖励信号，无需手工奖励设计
primary_logic: 将生成目标视频的潜在表示与智能体观测的潜在表示进行余弦相似度计算作为视频级奖励，并通过学习前向-后向表示来估计从状态-动作对达到由CLIP选取的关键帧目标状态的概率作为帧级奖励，从而引导策略实现细粒度目标达成
claims:
- 在Meta-World Bin Picking任务上，GenReward将episode return从Dense Reward的398提升至822，并显著优于RoboCLIP、Diffusion Reward、TADPoLe等其他奖励模型
- 消融实验表明移除视频级奖励或前向-后向奖励均会导致性能显著下降，验证了两个奖励组件的必要性
- 在Distracting Control Suite的WalkerWalk任务上，GenReward（782±110）大幅超越Raw Reward（640±74）、RoboCLIP（695±94）和Diffusion Reward（28±2）
- Meta-World Pick Out of Hole (dense) 上 episode return = 582
---

# Goal-Driven Reward by Video Diffusion Models for Reinforcement Learning

> [!tip] 核心洞察
> 将生成目标视频的潜在表示与智能体观测的潜在表示进行余弦相似度计算作为视频级奖励，并通过学习前向-后向表示来估计从状态-动作对达到由CLIP选取的关键帧目标状态的概率作为帧级奖励，从而引导策略实现细粒度目标达成

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于视频扩散模型的目标驱动奖励用于强化学习 |
| 英文题名 | Goal-Driven Reward by Video Diffusion Models for Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.00961) · [Project](https://qiwang067.github.io/genreward) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | GenReward |
| Dataset | Meta-World Pick Out of Hole, Meta-World Bin Picking, Meta-World Shelf Place, DCS Walker Walk |

> [!tip] 效果简介
> - Meta-World Pick Out of Hole (dense) 上，episode return 582 vs 193 (Dense Reward) (+389)。
> - Meta-World Bin Picking (dense) 上，episode return 822 vs 398 (Dense Reward) (+424)。
> - Meta-World Shelf Place (dense) 上，episode return 814 vs 154 (Dense Reward) (+660)。

## 概述

### 问题瓶颈

强化学习在复杂连续控制任务中的成功高度依赖奖励函数的设计。手工设计奖励函数不仅需要大量领域知识，而且泛化性差——同一套奖励逻辑难以迁移到不同任务，这严重限制了强化学习在真实场景中的可扩展性。现有的替代方案（如从演示中学习奖励、利用视觉-语言模型计算相似度奖励等）要么依赖专家示教，要么忽略了动作信息与细粒度目标达成的关联。

### 核心方法

**GenReward** 提出了一种全新的奖励框架：利用预训练视频扩散模型作为目标驱动的奖励生成器，无需手工设计奖励函数，也无需专家演示。其核心思路是将生成的目标条件视频所蕴含的“世界知识”转化为强化学习智能体的内在奖励信号，具体通过两个互补的奖励通道实现：

- **视频级奖励（Video-Level Reward）**：利用视频扩散模型的3D Causal VAE编码器，分别提取智能体历史观测与生成目标视频的潜在表示，计算二者余弦相似度，引导智能体在宏观行为层面模仿目标视频。
- **帧级奖励（Frame-Level FB Reward）**：通过CLIP从生成视频中选取与任务描述最相关的关键帧作为目标状态，再学习前向-后向表示（Forward-Backward Representation）来估计从任意状态-动作对到达该目标状态的概率，为细粒度目标达成提供逐帧引导。

最终奖励为视频级奖励、帧级FB奖励与环境原始奖励的加权组合：$r^{\mathrm{gen}} = \alpha \cdot r^{\mathrm{video}} + \beta \cdot r^{\mathrm{FB}} + r^{\mathrm{env}}$。

### 方法谱系与知识库定位

GenReward 在奖励建模领域占据了一个独特位置。与基于视觉-语言模型的奖励方法（如 **RoboCLIP**，Sontakke et al., NeurIPS 2023）相比，GenReward 不需要专家演示视频或文本描述作为参考，而是通过生成模型主动合成目标视频。与基于扩散模型的奖励方法（如 **Diffusion Reward** 使用条件熵负值、**TADPoLe** 使用去噪梯度）相比，GenReward 显式建模了状态-动作对到目标状态的到达概率，具备动作感知能力（action-aware），从而能提供更细粒度的目标达成信号（见 Table 1）。

从技术脉络看，GenReward 继承了视频扩散模型（以 CogVideoX 为骨干）的生成先验，将其适配为目标条件生成；同时吸收了前向-后向表示学习中“用内积近似长期状态占有测度”的理论框架（$F(s,a,z)^\top B(s')$ 近似 $M^{\pi_z}(s,a,s')$），将世界知识压缩为可微分的奖励信号。该方法在 DreamerV3 的世界模型-策略训练框架上运作，属于**生成式先验 + 基于模型的强化学习**的交叉范式。

### 主要结果

在 Meta-World 复杂操作任务上，GenReward 展现出显著的性能提升：
- **Pick Out of Hole**：episode return 从 Dense Reward 的 193 提升至 582；
- **Bin Picking**：从 398 提升至 822；
- **Shelf Place**：从 154 提升至 814。

在 Distracting Control Suite 的 Walker Walk 任务上，GenReward（782±110）大幅超越 Raw Reward（640±74）、RoboCLIP（695±94）和 Diffusion Reward（28±2）。在 Adroit Door 任务上，成功率从 60% 提升至 90%。

消融实验确认了两个奖励通道的必要性：移除视频级奖励或帧级FB奖励均导致性能显著下降。值得注意的是，即使生成的视频存在幻觉（如物体瞬移），GenReward 仍能提供有效的奖励引导，体现出一定的鲁棒性。

## 背景与动机

### 问题背景：强化学习的奖励设计瓶颈

强化学习（RL）在机器人操作、运动控制等复杂连续控制任务中展现出巨大潜力，但其成功高度依赖于精心设计的奖励函数。在真实世界的机器人任务中，手工设计奖励函数面临两个核心挑战：

**领域知识依赖**：工程师必须为每个新任务编写特定的奖励项，这要求对任务结构和环境动力学有深入理解。例如在Meta-World操作任务中，抓取、放置、开门等不同技能需要完全不同的奖励逻辑。

**泛化性受限**：手工奖励通常只能覆盖单一任务变体，当任务目标、物体位置或环境外观发生变化时，奖励函数往往失效，限制了RL在开放场景中的可扩展性。

虽然环境提供的密集奖励（Dense Reward）可以缓解部分问题，但其本质仍是程序化的、任务特定的，无法迁移到新任务。稀疏奖励虽然更通用，但探索效率极低，策略难以收敛。

### 现有奖励模型的局限性

近年来，研究者尝试利用视觉-语言模型（VLM）或生成模型构建通用奖励函数，以替代手工设计。这些方法各有优势，但也存在明显不足：

- **RoboCLIP**（Sontakke et al., NeurIPS 2023）通过计算智能体观测与演示视频或文本描述的CLIP嵌入相似度作为奖励，但需要专家演示视频作为参考，且无法利用动作信息进行细粒度目标达成判断。
- **Diffusion Reward** 将条件视频扩散模型的负条件熵作为奖励信号，鼓励智能体产生与生成模型分布一致的轨迹，但缺乏对具体目标状态的显式建模。
- **TADPoLe** 利用文本条件图像扩散模型的去噪梯度作为零样本密集奖励，但仅依赖单帧图像信息，忽略了时间维度的行为一致性。

这些方法的共同缺陷在于：**它们或依赖专家演示，或无法显式建模从当前状态-动作对到目标状态的到达关系**，导致奖励信号粗糙，难以引导策略实现精确的目标达成。

### 核心动机：视频生成模型中的世界知识迁移

大规模预训练视频扩散模型（如CogVideoX）在海量视频数据上学习到了丰富的物理世界先验——包括物体运动规律、交互动力学和任务完成过程。本文的核心洞察是：

> **这些预训练视频生成模型蕴含的“世界知识”可以被提取并转化为RL策略学习的内在奖励信号，从而无需手工设计奖励函数。**

具体而言，给定一个任务描述（如“捡起蓝色叉子”），视频扩散模型可以生成展示任务完成过程的目标视频。该视频不仅提供了“任务应该是什么样”的视觉参考，其潜在表示还编码了任务完成的结构化信息。通过将智能体的实际观测与生成的目标视频在潜在空间中进行对齐，可以构建一个无需专家演示、无需任务特定编程的通用奖励机制。

### 本文动机与目标

基于上述观察，本文提出 **GenReward（Generative Reward）** 框架，旨在回答以下问题：

1. **如何从生成的目标视频中提取有效的奖励信号？** 利用视频扩散模型的3D Causal VAE编码器，将生成视频与智能体观测映射到共享潜在空间，通过余弦相似度计算视频级奖励。

2. **如何实现细粒度的目标达成引导？** 在视频级奖励的基础上，引入前向-后向（Forward-Backward）表示学习，显式建模从状态-动作对到达由CLIP选取的关键帧目标状态的概率，提供帧级奖励。

3. **如何将生成先验与RL策略学习有效结合？** 将视频级奖励、帧级FB奖励与环境奖励加权组合，作为DreamerV3世界模型策略训练的总奖励信号。

这种设计使得GenReward具备三个关键特性：**基于生成模型**（无需专家演示）、**动作感知**（利用前向-后向表示建模状态-动作到目标的到达关系）、**分层奖励**（视频级粗粒度引导 + 帧级细粒度引导），从而在复杂操作任务中显著超越现有奖励模型。

## 核心创新

GenReward的核心创新在于将**预训练视频扩散模型（VDM）的世界知识**转化为强化学习的内在奖励信号，从而**完全替代手工奖励工程**。与现有奖励模型相比，GenReward在两个关键维度上实现了根本性变革：

### 创新一：从“程序化奖励”到“生成式目标驱动奖励”

传统RL奖励函数依赖领域专家手工设计（如Dense Reward）或从演示/文本中学习相似度（如**RoboCLIP**，Sontakke et al., NeurIPS 2023），而GenReward通过微调后的视频扩散模型**直接生成目标条件视频**，将“什么是好的行为”编码在生成先验中。具体而言：

- **视频级奖励**：利用3D Causal VAE编码器分别提取智能体观测序列$`\mathbf{z}^v`$与生成的目标视频$`\mathbf{z}^{\mathrm{goal}}`$的潜在表示，计算余弦相似度$`r^{\mathrm{video}} = \cos(\mathbf{z}^v, \mathbf{z}^{\mathrm{goal}})`$作为奖励。这使得智能体无需显式定义目标状态即可被引导向“看起来像完成任务”的行为。
- **关键瓶颈突破**：手工奖励函数泛化性差（如Bin Picking中Dense Reward仅获398 episode return），而GenReward通过生成式先验将return提升至822（Figure 5），证明生成模型蕴含的世界知识可有效替代人工设计。

### 创新二：动作感知的帧级细粒度目标达成

现有奖励模型（RoboCLIP、Diffusion Reward、TADPoLe）普遍**忽略动作信息**，仅基于状态相似度提供奖励（Table 1）。GenReward首次引入**前向-后向表示（Forward-Backward Representation）**，显式建模状态-动作对到目标状态的到达概率：

- **机制**：学习前向网络$`F(s,a,z)`$和后向网络$`B(s')`$，使得$`F(s,a,z)^\top B(s')`$近似从$`(s,a)`$到达目标状态$`s'`$的长期概率（Eq.7）。帧级奖励定义为$`\mathbf{r}^{\mathrm{FB}}(s,a,I^*) = \mathbf{F}(s,a,\psi(I^*))^\top \mathbf{B}(\psi(I^*))`$（Eq.9），其中$`I^*`$由CLIP从生成视频中选取与任务描述最相关的关键帧（Eq.6）。
- **因果证据**：消融实验表明，移除动作信息后DCS Walker Walk性能从782±110骤降至435±249（Table D），验证了动作感知对细粒度目标达成的必要性。这一设计使GenReward成为**首个同时利用生成先验和动作信息的奖励模型**。

### 创新三：双层奖励的协同机制

GenReward的最终奖励为$`r^{\mathrm{gen}} = \alpha \cdot r^{\mathrm{video}} + \beta \cdot r^{\mathrm{FB}} + r^{\mathrm{env}}`$（Eq.10），其中视频级奖励提供**粗粒度行为引导**（模仿目标视频的整体运动模式），帧级FB奖励提供**细粒度目标达成信号**（评估当前动作是否朝向关键帧目标）。两者形成互补：

- 移除视频级奖励导致性能显著下降（Figure 8 Left），证明粗粒度引导对探索方向的重要性；
- 移除FB奖励同样造成退化，且引入帧级目标后性能优于无帧级变体（Figure 8 Left），验证细粒度信号的增益；
- 敏感性分析显示，$`\alpha`$过小无法模仿目标视频，过大则阻碍探索；$`\beta`$过小未能利用世界知识，过大则探索困难（Figure 8 Middle/Right），揭示了两层奖励存在**最优平衡区间**。

综上，GenReward通过“生成式目标视频驱动 + 动作感知帧级到达概率”的双层奖励架构，实现了从“手工设计”到“生成式引导”的范式转变，在Meta-World和DCS等多个基准上显著超越现有方法。

## 整体框架

GenReward 的核心思路是利用预训练视频扩散模型的世界知识来驱动强化学习智能体的行为学习，从而绕过手工设计奖励函数的瓶颈。整个框架由三个层级递进的模块构成，形成从粗粒度视频模仿到细粒度目标达成的奖励信号链。

**Pipeline 总览。** 如 Figure 2 所示，GenReward 的训练流程（Algorithm 1）包含五个关键阶段：视频扩散模型微调、视频级奖励计算、CLIP 关键帧选择、前向-后向表示学习、以及奖励组合与策略训练。在在线交互过程中，系统以固定间隔触发奖励计算：首先利用微调后的视频扩散模型根据任务描述生成目标视频，然后通过 3D Causal VAE 编码器分别提取目标视频和智能体历史观测的潜在表示，计算余弦相似度作为视频级奖励；同时，CLIP 从生成视频中选取与任务描述最相关的关键帧作为帧级目标，前向-后向网络估计从当前状态-动作对到达该目标状态的概率，产生帧级奖励。最终奖励为三者的加权和：

$$r^{\mathrm{gen}} = \alpha \cdot r^{\mathrm{video}} + \beta \cdot r^{\mathrm{FB}} + r^{\mathrm{env}}$$

**模块间关系与信息流。** 视频级奖励提供全局行为模仿信号——它衡量智能体当前行为轨迹与目标视频在潜在空间中的整体相似度，引导策略向目标行为模式靠拢。帧级 FB 奖励则提供细粒度的目标达成信号——它显式建模状态-动作对到特定目标帧的到达概率，使策略能够精确执行抓取、放置等关键操作。环境奖励 $r^{\mathrm{env}}$ 作为基础信号保留，提供任务完成的基本反馈。三者互补：视频级奖励负责“做什么”，帧级奖励负责“怎么做”，环境奖励提供底线保障。

**与现有奖励模型的本质差异。** Table 1 从四个维度对比了 GenReward 与代表性基线方法。**RoboCLIP**（Sontakke et al., NeurIPS 2023）依赖 VLM 计算观测与演示视频/文本的相似度，但需要专家演示且不利用动作信息；**Diffusion Reward** 基于条件视频扩散模型的条件熵负值作为奖励，同样缺乏动作感知；**TADPoLe** 利用文本条件图像扩散模型的去噪梯度，但仅处理单帧图像。GenReward 的独特之处在于：基于生成模型而非判别模型，不需要专家演示，且通过前向-后向表示首次将动作信息引入生成式奖励框架，实现了对目标达成过程的细粒度建模。

**关键设计选择。** 视频扩散模型选用 CogVideoX 作为基座，在操作视频数据集上微调以支持目标条件生成。潜在编码器采用 3D Causal VAE，能够捕捉时序动态信息。CLIP 帧选择器使用 OpenCLIP，确保选出的关键帧与任务语义高度相关。前向-后向网络通过最小化 Bellman 残差损失训练，其低秩近似特性使得在任意策略下估计长期到达概率成为可能。这些设计选择的消融验证见后续实验分析章节。

### 补充图表

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our proposed framework. The key idea is to leverage generated goal-conditioned videos for world knowledge transfer, enabling the downstream agent to improve performance on unseen tasks*

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/003_Figure_2.jpg]]
*Figure 2: Pipeline of GenReward, which computes goal-driven rewards for behavior learning of the agent using generative prior. During online interaction with the environment, at regular intervals, we employ the correlation between the latent representations of the agent’s observations and the generated goal videos as video-level rewards. Meanwhile, we learn a forward-backward model to measure the probability of reaching the goal state that is selected using CLIP from a given state–action pair, providing frame-level reward for finegrained goal-achievement*

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/004_Figure_4.jpg]]
*Figure 4: Illustration of experimental setups in our experiments with generated videos and image observations from environments*

## 核心模块与公式推导

GenReward 的奖励生成管线由五个核心模块串联构成，从生成式先验提取到策略训练形成闭环。

**视频扩散模型微调（Video Diffusion Model Adaptation）**：在操作视频数据集上微调预训练 CogVideoX，使其支持目标条件的视频生成。微调沿用标准扩散去噪范式，前向过程逐步向潜变量注入高斯噪声：

$$\mathbf{x}_t = \alpha_t \mathbf{x}_0 + \sigma_t \epsilon, \quad \epsilon \sim \mathcal{N}(0, \mathbf{I}) \tag{1}$$

去噪模型 $\hat{\epsilon}_\theta$ 的优化目标为：

$$\min_\theta \mathbb{E}_{\epsilon \sim \mathcal{N}(0, \mathbf{I})} \left\| \hat{\epsilon}_\theta(\mathbf{x}_t, t, c_{\mathrm{text}}, c_{\mathrm{image}}) - \epsilon \right\|_2^2 \tag{2}$$

其中 $c_{\mathrm{text}}$ 为文本条件，$c_{\mathrm{image}}$ 为图像条件。微调后模型可根据任务描述生成目标视频，作为下游奖励计算的生成式先验。

**视频级奖励计算（Video-Level Goal as Reward）**：在智能体与环境交互过程中，以固定间隔利用 3D Causal VAE 编码器分别提取智能体历史观测 $\mathbf{o}_{0:T}$ 和生成目标视频 $\mathbf{o}_{0:K}$ 的潜在表示：

$$\mathbf{z}^v = 3\mathrm{D\ Causal\ VAE}(\mathbf{o}_{0:T}) \tag{3}$$

$$\mathbf{z}^{\mathrm{goal}} = 3\mathrm{D\ Causal\ VAE}(\mathbf{o}_{0:K}) \tag{4}$$

视频级奖励定义为两个潜向量之间的余弦相似度：

$$r^{\mathrm{video}} = \cos(\mathbf{z}^v, \mathbf{z}^{\mathrm{goal}}) = \frac{\mathbf{z}^v \cdot \mathbf{z}^{\mathrm{goal}}}{\|\mathbf{z}^v\| \|\mathbf{z}^{\mathrm{goal}}\|} \tag{5}$$

该模块的瓶颈在于：余弦相似度仅提供粗粒度的视频级对齐信号，无法区分视频内部哪些帧对任务成功更关键。

**关键帧选择（CLIP Frame Selector）**：为获取帧级目标，利用 OpenCLIP 从生成视频中选择与任务描述 $G$ 最相关的帧：

$$I^* = \arg\max_i \frac{\mathbf{CLIP}_L(G) \cdot \mathbf{CLIP}_I(I_i)}{\|\mathbf{CLIP}_L(G)\| \|\mathbf{CLIP}_I(I_i)\|} \tag{6}$$

其中 $\mathbf{CLIP}_L$ 为文本编码器，$\mathbf{CLIP}_I$ 为图像编码器。该模块存在已知失效模式：CLIP 相似度最高帧未必对应任务成功状态（如抓取动作未完成但语义高度匹配），详见 Figure B 的失败案例。

**前向-后向表示学习（Forward-Backward Representation）**：为显式建模从状态-动作对到达目标状态的细粒度概率，学习前向网络 $F(s,a,z)$ 和后向网络 $B(s')$。核心理论依据是长期转移测度的低秩近似：

$$M(s,a,s',\pi_z) \approx F^\top(s,a,z) B(s') \rho(\mathrm{d}s') \tag{7}$$

其中 $\rho$ 为状态分布，$\pi_z$ 为以潜变量 $z$ 为条件的策略。训练通过最小化 Bellman 残差损失实现：

$$\begin{aligned} \|F_z^\top B\rho - (P + \gamma P_{\pi_z} \bar{F}_z^\top \bar{B}\rho)\| = &\mathbb{E}_{(s_t,a_t,s_{t+1})\sim\rho}[(F(s_t,a_t,z)^\top B(\psi(I^*)) - \gamma \bar{F}(s_{t+1},\pi_z(s_{t+1}),z)^\top \bar{B}(\psi(I^*)))^2] \\ &- 2\mathbb{E}_{(s_t,a_t,s_{t+1})\sim\rho}[F(s_t,a_t,z)^\top B(\psi(I^*))] + \mathrm{Const.} \tag{8}\end{aligned}$$

其中 $\psi(I^*)$ 为关键帧 $I^*$ 的语义编码，$\bar{F}$ 和 $\bar{B}$ 为目标网络（target network）。为防止表示退化，额外施加正交归一化正则：

$$\mathcal{L}_{\mathrm{norm}} = \left\| \mathbb{E}_{\rho} [B B^\top] - I_d \right\|_{\mathrm{F}}^2$$

帧级奖励定义为从 $(s,a)$ 到达目标帧 $I^*$ 的似然：

$$\mathbf{r}^{\mathrm{FB}}(s,a,I^*) = \mathbf{F}(s,a,\psi(I^*))^\top \mathbf{B}(\psi(I^*)) \tag{9}$$

该模块的关键因果机制在于：前向-后向表示将动作信息显式纳入奖励计算，使智能体能够进行目标驱动的动作选择——选择使 $F(s,a,z)$ 与 $B(s_{\mathrm{goal}})$ 内积最大的动作（Figure 3）。消融实验证实，从 FB 奖励中移除动作信息会导致 DCS Walker Walk 上性能从 $782\pm110$ 骤降至 $435\pm249$（Table D），验证了动作感知设计的必要性。

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/005_Figure_3.jpg]]
*Figure 3: Goal-driven action selection. Learned representation space enables goal-directed control by selecting the action whose forward representation of the current state–action pair most closely aligns with the backward representation of goal state*

**奖励组合与策略训练（Reward Combination）**：最终奖励为三个分量的加权和：

$$r^{\mathrm{gen}} = \alpha \cdot r^{\mathrm{video}} + \beta \cdot r^{\mathrm{FB}} + r^{\mathrm{env}} \tag{10}$$

其中 $r^{\mathrm{env}}$ 为环境原生奖励，$\alpha$ 和 $\beta$ 为权重系数。该组合作为总奖励信号输入 DreamerV3 进行策略训练。敏感性分析（Figure 8 Middle/Right）表明：$\alpha$ 过小无法有效模仿目标视频，过大则抑制探索；$\beta$ 过小未能充分利用世界知识，过大则导致探索困难。

### 补充图表

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/008_Figure_7.jpg]]
*Figure 7: Showcase of selecting the goal image from the video generated with the prompt pick up the blue fork using CLIP. The highlighted area represents the video frames that are more relevant to the task. The frame with the highest similarity reflects the frame-level goal*

## 实验与分析

### 主要结果：GenReward 在复杂操作任务上显著超越现有奖励模型

GenReward 在 Meta-World 基准的三个复杂操作任务上均大幅超越环境原生密集奖励（Dense Reward，DreamerV3 backbone）。如 Figure 5 所示，在 **Pick Out of Hole** 任务上，GenReward 将 episode return 从 193 提升至 582（+389）；在 **Bin Picking** 任务上，从 398 提升至 822（+424）；在 **Shelf Place** 任务上，从 154 提升至 814（+660）。这一提升幅度表明，视频扩散模型提供的内在奖励信号能够有效弥补手工设计奖励函数在复杂操作任务中的信息不足。

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/007_Figure_5.jpg]]
*Figure 5: Performance on Meta-World complex manipulation tasks in terms of episode return under dense reward setting*

与同类奖励模型相比，GenReward 同样展现出明显优势。在 Bin Picking 任务上，**RoboCLIP**（Sontakke et al., NeurIPS 2023）虽能利用演示视频的视觉相似度提供奖励，但其 episode return 仅为约 450，远低于 GenReward 的 822；**Diffusion Reward** 和 **TADPoLe** 的表现则更弱，分别约为 300 和 250。Table 1 揭示了这一差距的结构性原因：RoboCLIP 和 Diffusion Reward 均不显式利用动作信息，TADPoLe 则依赖文本条件图像扩散模型，而 GenReward 通过前向-后向表示显式建模状态-动作对到目标状态的到达概率，从而提供更细粒度的目标达成信号。

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/002_Table_1.jpg]]
*Table 1: Compared to other competitive reward models, the proposed reward framework is based on generative models, does not require expert demonstrations, and incorporates action information for fine-grained goal-achievement*

定性分析进一步印证了定量结果。Figure 6 展示了 Bin Picking 任务上的策略行为对比：TADPoLe 甚至未能接触冰球（puck），Diffusion Reward 则将抓取的冰球移离目标位置，而 GenReward 使策略能够以更少步数完成抓取，并优于 Dense Reward 和 RoboCLIP。

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/006_Figure_6.jpg]]
*Figure 6: Policy evaluation on the Meta-World Bin Picking task. TADPoLe fails to contact the puck, while Diffusion Reward moves the grasped puck away from the target position. In contrast, GenReward enables the policy to complete the grasp in fewer steps and outperforms both Dense Reward and RoboCLIP*

### 跨基准泛化：从操作到运动控制

GenReward 的泛化能力在 **Distracting Control Suite (DCS)** 和 **Adroit** 基准上得到验证。如 Table A（Supplementary Material）所示，在 DCS 的 **Walker Walk** 任务上，GenReward 取得 782±110 的 episode return，显著超越 Raw Reward（640±74）、RoboCLIP（695±94）和 Diffusion Reward（28±2）。Diffusion Reward 在此任务上的极低表现（28±2）表明，仅依赖条件熵作为奖励信号在视觉干扰环境下几乎失效。在 Adroit **Door** 任务上，GenReward 的成功率达到 90±10%，而 Raw Reward 仅为 60±20%。

### 消融实验：视频级奖励与帧级奖励的双重必要性

Figure 8（Left）展示了在 Meta-World Pick Place 任务上的消融结果。移除视频级奖励（`GenReward w/o video-level reward`）导致性能显著下降，证明生成目标视频的潜在表示相似度是引导策略的关键信号。移除帧级 FB 奖励（`GenReward w/o FB reward`）同样造成性能损失，且 GenReward 引入帧级目标奖励后的完整版本优于无帧级目标的变体，验证了从状态-动作对估计目标到达概率的细粒度奖励是不可或缺的。

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/009_Figure_8.jpg]]
*Figure 8: These figures display the ablation studies and sensitivity analyses of GenReward on Meta-World Pick Place. Left: Comparison with GenReward without video-level reward or FB reward. Middle: The sensitivity analyses of video-level reward weight. Right: The performance of GenReward with different FB reward scale*

进一步地，Table D（Supplementary Material）在 DCS Walker Walk 任务上的消融揭示了动作信息的关键作用：从 FB 奖励中移除动作信息后，性能从 782±110 骤降至 435±249。这一结果表明，前向-后向表示中显式建模动作是 GenReward 区别于其他奖励模型的核心优势之一。

### 奖励权重敏感性分析

Figure 8（Middle 和 Right）展示了视频级奖励权重 α 和 FB 奖励权重 β 的敏感性分析。视频级奖励权重 α 过小会导致智能体无法有效模仿目标视频的行为模式，过大则会因过度约束而阻碍探索。FB 奖励权重 β 过小则未能充分利用世界知识，过大则使探索变得困难。实验表明存在一个适中的权重区间，使两种奖励信号协同工作。

### 关键帧选择与视觉编码器的影响

Table C（Supplementary Material）分析了关键帧选择策略和视觉编码器的影响。使用 CLIP 选择目标帧比随机选择效果更好，验证了语义相关性筛选的有效性。然而，将视觉编码器从 DINOv3 替换为 SigLIP2 会导致性能下降，表明 3D Causal VAE 与特定视觉编码器的兼容性对奖励质量有直接影响。

值得注意的是，CLIP 帧选择并非完美无缺。Figure B（Supplementary Material）展示了一个失败案例：在生成的 RT-1 Pick Apple 视频中，CLIP 选择的"最相关帧"并未完全抓取苹果，而第二相关帧实际上包含了成功的抓取动作。尽管如此，实验表明即使使用次优帧，GenReward 仍能获得性能增益，这归因于视频级奖励对整体行为模式的引导作用。

### 生成视频域的影响

Figure 9 展示了使用不同域生成视频对 GenReward 性能的影响。实验通过替换微调视频扩散模型所用的操作视频数据集来改变生成视频的域分布。结果表明，生成视频与任务域的相关性越强，奖励信号的质量越高，策略性能越好。这提示在实际部署中需谨慎选择微调数据集。

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/010_Figure_9.jpg]]
*Figure 9: Performance of GenReward on Meta-World Pick Place with different generated videos*

### 幻觉视频的鲁棒性

Table B（Supplementary Material）报告了 GenReward 在含有幻觉的生成视频下的性能。幻觉表现为生成视频中物体的瞬移或不一致运动。实验表明，即使使用含有幻觉的视频，GenReward 的奖励机制仍能提升策略性能，这得益于视频级奖励在潜在空间中捕捉的是整体行为模式而非精确的逐帧对应关系。然而，幻觉的系统性影响尚未被完全解决，这构成了当前方法的一个重要局限性。

### 训练效率

Table E（Supplementary Material）对比了各方法在 Meta-World Pick Place 任务上的训练时间。GenReward 的额外计算开销主要来自视频扩散模型的微调（约 7 天 / 16 块 A100 GPU）和前向-后向网络的学习。一旦微调完成，在线交互阶段的奖励计算开销相对可控。

### 补充图表

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/015_Table.jpg]]
*Table: A. Performance comparison across various environments*

![[assets/figures/papers/paper_list_l2681_https_arxiv_org_abs_2512_00961/figures/014_Table.jpg]]
*Table: D. Performance of GenReward variants on DCS Walker Walk*

## 方法谱系与知识库定位

### 与现有奖励模型的关系

GenReward 处于“生成模型驱动的强化学习奖励设计”这一交叉方向，其核心定位可通过 **Table 1** 清晰界定：与现有竞争性奖励模型相比，GenReward 基于生成模型、无需专家演示、且显式利用动作信息实现细粒度目标达成。以下从三个维度展开谱系分析。

**生成先验 vs. 视觉-语言对齐。** 以 **RoboCLIP**（Sontakke et al., NeurIPS 2023）为代表的 VLM 奖励模型通过计算智能体观测与演示视频或文本描述的 CLIP 相似度来定义奖励。这类方法依赖预训练的视觉-语言对齐能力，但本质上是一种“被动匹配”——它衡量当前状态与目标的语义相似性，却无法编码“如何到达目标”的动力学信息。GenReward 的视频级奖励在形式上与 RoboCLIP 的相似度计算有表面相似性，但关键区别在于：GenReward 使用视频扩散模型的 3D Causal VAE 潜在空间而非 CLIP 空间，该潜在空间经过操作视频微调，蕴含了丰富的时序-动作先验。

**条件熵 vs. 目标条件生成。** **Diffusion Reward** 将条件视频扩散模型的条件熵负值作为奖励，其直觉是“模型越不确定当前行为，说明行为越偏离训练分布”。但条件熵是一个标量信号，缺乏目标导向性——它只能告诉智能体“做得不对”，无法指明“该往哪个方向改进”。GenReward 则通过显式生成目标视频，将奖励信号锚定在具体的视觉目标上，使奖励具有方向性。实验证据充分支持这一优势：在 Meta-World Bin Picking 任务上，Diffusion Reward 甚至将抓取的冰球移离目标位置（Figure 6），而 GenReward 则引导策略以更少步数完成抓取。

**去噪梯度 vs. 前向-后向到达概率。** **TADPoLe** 利用文本条件图像扩散模型的去噪梯度作为零样本密集奖励，其原理是去噪方向隐含了“向数据分布靠拢”的信息。但去噪梯度是单步信号，缺乏对长期目标达成概率的建模。GenReward 的帧级奖励通过前向-后向（FB）表示学习 $F(s,a,z)^\top B(s')$ 来近似从状态-动作对到达目标状态的长期概率，这是一种根本不同的奖励构造方式。更重要的是，FB 表示显式编码动作信息——消融实验表明，从 FB 奖励中移除动作信息会导致 DCS Walker Walk 性能从 782±110 骤降至 435±249（Table D），验证了动作感知设计的必要性。

### 方法适用边界

**任务类型边界。** GenReward 的设计假设任务目标可以通过视觉视频表达，因此适用于操作任务（Meta-World）和运动控制任务（Distracting Control Suite、Adroit）。对于目标难以可视化的任务（如纯状态空间优化、抽象策略游戏），该方法不直接适用。此外，帧级 FB 奖励依赖从生成视频中选取关键帧作为目标状态，这要求任务具有明确的“关键状态”概念——例如抓取任务中“手接触物体”或“物体到达目标位置”的瞬间。

**数据与计算边界。** 视频扩散模型微调需要操作视频数据集，且计算开销巨大：论文报告使用 16 块 A100 GPU 训练 7 天（Table E）。这意味着 GenReward 的部署门槛显著高于 RoboCLIP 等仅需推理的 VLM 方法。不过，一旦微调完成，奖励计算在智能体在线交互期间是高效的，因为视频生成是离线进行的。

**泛化边界。** 实验覆盖了 Meta-World 的三个操作任务、DCS Walker Walk 和 Adroit Door，证明了跨环境和跨具身的一定泛化能力。但帧级奖励依赖目标帧的语义特征编码（通过 CLIP 选择关键帧，再通过 DINOv3 或 SigLIP2 编码），对未见过的物体类别或场景的泛化性尚未充分验证。Table C 显示替换 DINOv3 为 SigLIP2 会导致性能下降，表明视觉编码器的选择对性能有显著影响，也暗示跨域泛化可能受限于编码器的预训练分布。

### 局限与开放问题

**生成视频的幻觉问题。** 视频扩散模型可能生成包含物理不一致性的视频（如物体瞬移）。Table B 显示，即使使用含有幻觉的视频，GenReward 仍能提升性能，但幻觉的影响尚未系统解决。这一现象的可能解释是：视频级奖励的余弦相似度对局部幻觉具有一定鲁棒性，而 CLIP 关键帧选择可能避开明显不合理的帧。但 Figure B 展示了一个 CLIP 选择失败案例——在生成 RT-1 Pick Apple 视频中，CLIP 最高相似度帧并未展示成功抓取，而次高帧实际包含成功抓取。这揭示了 CLIP 相似度与任务成功之间的不一致性，是当前方法的脆弱环节。

**关键帧选择的鲁棒性。** 上述 CLIP 失败案例引出一个核心开放问题：如何更鲁棒地选择目标帧？当前方法将 CLIP 相似度作为唯一选择标准，但语义相似度与“任务完成状态”并非完全对齐。可能的改进方向包括：引入时间一致性约束（优先选择视频中稳定出现的状态）、利用扩散模型自身的去噪轨迹信息、或训练专门的关键帧选择器。

**零样本迁移的可能性。** 当前 GenReward 需要针对目标域微调视频扩散模型。一个自然的开放问题是：能否利用文本直接生成目标视频而不需要微调，实现零样本跨任务迁移？这依赖于基础视频生成模型的泛化能力和对操作动作的理解程度。CogVideoX 等大规模预训练模型提供了潜在基础，但操作动作的精确生成仍是挑战。

**前向-后向表示的扩展性。** FB 表示当前建模的是从 $(s,a)$ 到单个目标帧的到达概率。能否扩展到多步目标状态序列——即学习到达一系列子目标的概率——是一个值得探索的方向。这将使 GenReward 能够处理需要多步规划的长程任务。

**Sim-to-Real 的域差距。** 所有实验均在模拟器中进行。生成视频与真实机器人观测之间的域差距如何处理，是该方法走向实际应用必须面对的问题。可能的思路包括：在真实机器人数据上微调视频扩散模型、使用域随机化生成视频、或在奖励计算中引入域自适应模块。

## 原文 PDF

![[paperPDFs/CVPR_2026/Goal_Driven_Reward_by_Video_Diffusion_Models_for_Reinforcement_Learning.pdf]]