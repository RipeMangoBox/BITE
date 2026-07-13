---
title: "Pose-RFT: Aligning MLLMs for 3D Pose Generation via Hybrid Action Reinforcement Fine-Tuning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Pose_RFT_Aligning_MLLMs_for_3D_Pose_Generation_via_Hybrid_Action_Reinforcement_F_91500ba4f27e.pdf
project_link: null
code_link: null
aliases:
- PR
- Pose-RFT
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 将任务建模为混合动作空间（离散文本+连续姿势）的强化学习问题，并设计HyGRPO算法进行组相对优势分解优化，使模型直接根据奖励函数最大化语义和空间对齐目标。
primary_logic: 将连续姿势输出的策略建模为多变量高斯分布，并将综合优势函数分解为离散与连续两部分分别进行优势归一化和PPO风格的裁剪更新，从而使语言模型和姿势解码器能在统一的奖励信号下协同优化。
claims:
- SFT产生次优的平均输出，而RFT通过学习奖励最大化产生高奖励、语义和空间对齐的输出。
- HyGRPO在混合动作空间上稳定优化，而标准离散GRPO无法提升连续姿势质量。
- Pose-RFT在推理姿势估计（RPE）任务上建立了新的SOTA，证明了多模态推理能力。
- 3DPW 上 MPJPE (mm) ↓ = 85.9
---

# Pose-RFT: Aligning MLLMs for 3D Pose Generation via Hybrid Action Reinforcement Fine-Tuning

> [!tip] 核心洞察
> 将连续姿势输出的策略建模为多变量高斯分布，并将综合优势函数分解为离散与连续两部分分别进行优势归一化和PPO风格的裁剪更新，从而使语言模型和姿势解码器能在统一的奖励信号下协同优化。

| 字段 | 内容 |
|------|------|
| 中文题名 | Pose-RFT：通过混合动作强化微调对齐多模态大语言模型的三维姿势生成 |
| 英文题名 | Pose-RFT: Aligning MLLMs for 3D Pose Generation via Hybrid Action Reinforcement Fine-Tuning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=ea1U1MgbdT) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | Pose-RFT |
| Dataset | 3DPW, Human3.6M, RPE, PoseScript-H2 |

> [!tip] 效果简介
> - 3DPW 上，MPJPE (mm) ↓ 85.9 vs 94.7 (UniPose) (-8.8)。
> - Human3.6M 上，MPJPE (mm) ↓ 63.0 vs 69.2 (UniPose) (-6.2)。
> - RPE 上，MPJPE (mm) ↓ 198.6 vs 213.4 (UniPose) (-14.8)。

## 概要

3D人体姿态生成在多模态大语言模型（MLLM）时代面临一个根本性的对齐困境：监督微调（SFT）的确定性回归范式天然无法处理“一对多”的语义模糊性——同一段文本描述或同一张图像可以对应多种合理的三维姿态，而SFT迫使模型预测一个折衷的“平均”输出，导致语义一致性与空间准确度双双不足。**Pose-RFT** 针对这一瓶颈，将学习范式从监督模仿转向奖励驱动的强化微调（RFT），核心思路是将姿态生成建模为**混合动作空间**（离散文本 + 连续姿态）上的强化学习问题，并设计 **HyGRPO** 算法进行组相对优势分解优化，使模型直接最大化语义和空间对齐目标。

方法上，Pose-RFT 在三个关键维度上区别于先前工作（如 **ChatPose** (Feng et al., 2024)、**UniPose** (Li et al., 2025c) 等）：(1) 将连续姿态输出建模为多变量高斯分布策略，而非确定性回归；(2) 采用 HyGRPO 将综合优势函数分解为离散与连续两部分，分别进行组归一化和 PPO 风格裁剪更新；(3) 引入四种任务特定奖励函数——空间位置、语义对齐、格式正确性和文本嵌入相似度——作为统一的优化信号。

实验结果表明，Pose-RFT 在图像到姿态重建任务上大幅超越先前最优方法：在 3DPW 数据集上 MPJPE 降至 85.9 mm（较 UniPose 降低 8.8 mm），在 Human3.6M 上降至 63.0 mm（降低 6.2 mm）。在更具挑战性的推理姿态估计（RPE）基准上，Pose-RFT 建立了新的 SOTA（MPJPE 198.6 mm），验证了基于 MLLM 的推理驱动姿态估计的有效性。文本到姿态检索任务同样取得一致提升，跨检索器评估中 R^{T2P}@5 达到 55.2，较 SFT 基线提升 7.5 个百分点。消融实验进一步确认：标准离散 GRPO 无法提升连续姿态质量，而 HyGRPO 实现了稳定且显著的增益，证明了混合动作优化方法的必要性。

**方法定位**：Pose-RFT 属于强化微调范式在具身多模态生成任务上的迁移应用，其 HyGRPO 算法为混合动作空间的策略优化提供了可复用的技术方案。该方法在图像到姿态、文本到姿态及推理姿态估计三个任务维度上均验证了有效性，但奖励函数质量依赖和组归一化的计算开销仍是当前局限。



三维人体姿势生成是计算机视觉与多模态学习的交叉前沿，其核心任务是从图像或自然语言描述中恢复精确的三维人体姿态。近年来，多模态大语言模型（MLLM）的兴起为这一任务带来了新的范式——通过统一的语言接口同时处理视觉理解与姿势推理。然而，现有方法普遍采用监督微调（SFT）的确定性回归范式，这构成了一个根本性的瓶颈。

**核心瓶颈：确定性回归无法处理“一对多”映射**。在三维姿势生成中，同一文本描述（如“一个人正在奔跑”）或同一单目图像可以对应多种物理上合理的三维姿态——这是一个典型的“一对多”模糊性问题。SFT通过最小化预测值与真实值之间的L2距离来训练模型，这迫使模型学习所有可能解的平均值，产生一个“折衷但次优”的输出。如图1所示，SFT输出虽然在数学意义上接近平均真值，但在语义一致性和空间准确度上严重不足——这被称为“对齐差距”（alignment gap）。这一现象在推理姿势估计（RPE）等需要复杂多模态推理的场景中尤为突出，模型需要同时理解视觉线索、语言指令并推理出合理的空间配置，而SFT的平均化策略在此彻底失效。

**现有方法的局限**。此前的工作如**ChatPose**（Feng et al., 2024）、**UniPose**（Li et al., 2025c）和**ChatHuman**（Lin et al., 2024）虽然探索了MLLM在姿势生成中的应用，但均未突破SFT范式的限制。这些方法将姿势输出建模为确定性回归问题，直接预测SMPL参数或关节坐标，缺乏对输出不确定性的显式建模，也无法根据任务目标灵活调整生成策略。更关键的是，这些方法无法利用强化学习中的奖励信号直接优化语义对齐和空间精度等高层目标。

**本文动机：从监督模仿到奖励驱动的强化微调**。受大语言模型强化微调（RFT）成功的启发，本文提出将三维姿势生成重新建模为混合动作空间下的强化学习问题。核心思想是：让模型直接最大化语义和空间对齐的奖励函数，而非模仿固定的真值标签。这一范式转变的关键在于：（1）将连续姿势输出建模为多变量高斯分布，使策略能够表达输出的不确定性；（2）设计HyGRPO算法，实现离散语言头和连续姿势头在统一奖励信号下的协同优化。通过这种方式，模型不再被迫预测“平均”输出，而是学习生成高奖励、语义和空间双重对齐的高质量姿态。



## 核心方法与创新机理

Pose-RFT 的核心创新在于将 3D 姿势生成从确定性监督模仿范式彻底转向**奖励驱动的强化微调（RFT）**，并为此设计了一套完整的混合动作强化学习框架。以下从三个层面剖析其关键创新与 changed slots。

### 1. 训练范式转换：从 SFT 到 RFT

传统姿势特定 MLLM（如 **ChatPose**（Feng et al., 2024）、**UniPose**（Li et al., 2025c））依赖监督微调（SFT），通过 L2 回归等确定性损失直接预测 SMPL 参数。这种范式存在根本性缺陷：3D 姿势生成天然具有“一对多”的模糊性——同一文本描述或图像可对应多种合理的 3D 姿势，而 SFT 强制模型收敛到单一“平均”输出，导致**语义一致性与空间准确度的严重对齐差距**（alignment gap）。

Pose-RFT 将问题重新建模为强化学习问题：模型不再模仿 ground-truth，而是通过**最大化任务奖励**来学习生成高奖励输出。这一范式转换的因果机制在于：奖励函数可以灵活编码多维度目标（空间精度、语义对齐、格式规范），使模型在探索中自主发现符合多目标的最优生成策略，而非被迫折衷。

### 2. 混合动作空间建模：离散文本 + 连续姿势

这是方法层面最关键的 changed slot。现有姿势 MLLM 将姿势输出视为确定性回归问题，直接预测单一参数向量。Pose-RFT 则引入**混合动作空间**，将整体策略分解为两项的乘积（Eq. 1）：

$$\pi_{\theta}(a, p | q) = \pi_{\theta}(a | q) \cdot \pi_{\theta}(p | q, a)$$

其中，离散子策略 $\pi_{\theta}(a | q)$ 由 LLaVA 语言模型头生成文本响应 $a$；连续子策略 $\pi_{\theta}(p | q, a)$ 被建模为**多变量高斯分布**（Eq. 2）：

$$\pi_{\theta}(p | q, a) = \mathcal{N}(p; \mu_{\theta}(q, a), \Sigma_{\theta}(q, a))$$

该分布的均值 $\mu_{\theta}$ 和协方差 $\Sigma_{\theta}$ 由专用连续姿势头预测。这一设计的核心洞察是：将姿势输出从点估计升级为分布估计，使策略能够表达输出不确定性，并在强化学习框架下通过采样探索更优的姿势空间——这正是 SFT 确定性回归无法做到的。

### 3. HyGRPO 算法：混合动作空间的稳定优化

策略建模的改变需要配套的优化算法。标准离散动作 RL 算法（如 GRPO）直接应用于混合动作空间时，**无法提升连续姿势质量**（Figure 4 提供了决定性证据：离散 GRPO 的姿势生成奖励无改善，而 HyGRPO 持续稳定提升）。

HyGRPO 的核心机制是**组相对优势分解**：对每组采样的 $G$ 个候选输出，分别计算离散文本的优势 $\hat{F}_i$ 和连续姿势的优势 $\hat{\Delta}_i$，对两者独立进行组归一化，再分别应用 PPO 风格的裁剪更新，并加入 KL 散度惩罚项 $\beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}})$ 防止策略崩溃（Eq. 6/21）：

$$\mathcal{J}_{\mathrm{HyGRPO}} = \mathbb{E}_{q \sim \mathcal{D}, \{a_i, p_i\}_{i=1}^G \sim \pi_{\theta}(\cdot | q)} \Bigg[ \frac{1}{G} \sum_{i=1}^G \min(r_d \hat{F}_i, \mathrm{clip}(r_d, 1-\epsilon, 1+\epsilon) \hat{F}_i) + \frac{1}{V} \sum_{i=1}^V \min(r_c \hat{\Delta}_i, \mathrm{clip}(r_c, 1-\epsilon, 1+\epsilon) \hat{\Delta}_i) - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \Bigg]$$

这一设计的必要性在于：离散语言 token 和连续姿势参数的梯度特性、数值尺度截然不同。统一归一化会掩盖连续部分的微弱但关键的优化信号；分解归一化使两个策略头在各自空间中接收到针对性的学习信号，从而实现协同优化。

### 4. 多维奖励信号设计

Pose-RFT 定义了四种任务奖励，替代 SFT 的单一回归损失：

- **空间位置奖励** $\mathcal{R}_{\mathrm{joint}} = \frac{1}{||J_{\mathrm{pred}} - J_{\mathrm{gt}}||_2}$：直接优化 3D 关节精度（Eq. 7）
- **语义对齐奖励** $\mathcal{R}_{\mathrm{semantic}} = \cos(\phi_t(q), \phi_p(p))$：确保文本-姿势语义一致性（Eq. 8）
- **格式奖励** $\mathcal{R}_{\mathrm{format}}$：二元奖励约束输出模板（Eq. 9）
- **文本相似度奖励** $\mathcal{R}_{\mathrm{text}} = \cos(E(a_{\mathrm{pred}}), E(a_{\mathrm{gt}}))$：使用 BGE-M3 编码器评估文本回答质量（Eq. 10）

消融实验（Table 5）揭示了奖励间的强耦合关系：移除格式奖励导致跨模态任务**灾难性失败**（MPJPE 飙升至 131.9mm），说明格式约束是有效优化的前提条件；移除联合位置奖励使 PA-MPJPE 上升 21.9mm，严重损害几何精度。这表明多维奖励并非简单叠加，而是构成了一个相互制约的优化约束系统。

### 5. 创新总结

| 维度 | 基线方法（ChatPose/UniPose） | Pose-RFT | 因果机制 |
|------|------------------------------|----------|----------|
| 训练范式 | 监督微调（SFT） | 强化微调（RFT）+ HyGRPO | 从模仿平均输出转向最大化多维奖励 |
| 姿势建模 | 确定性回归（点估计） | 多变量高斯分布（分布估计） | 表达输出不确定性，支持探索 |
| 优化算法 | 标准监督损失 | HyGRPO（分解优势 + PPO 裁剪） | 离散/连续独立归一化，稳定协同优化 |
| 训练信号 | 单一回归损失 | 四种任务奖励 | 多目标约束下的策略搜索 |

这些创新形成了完整的因果链条：**分布建模**使策略能够表达“一对多”的姿势空间 → **HyGRPO** 提供稳定优化混合动作的算法基础 → **多维奖励**引导策略同时追求空间精度和语义对齐 → 最终弥合 SFT 的对齐差距。



Pose-RFT 将 3D 人体姿势生成从监督模仿范式转向奖励驱动的强化微调范式，其核心架构围绕一个混合动作空间的多模态大语言模型（MLLM）展开。整体 pipeline 由四个关键模块串联构成：**Pose-Aware Encoder**、**Discrete Policy Head**、**Continuous Policy Head** 和 **Reward Functions**，并通过 **HyGRPO** 算法实现端到端的联合优化。

### 输入输出流

系统接收多模态输入 $q$（图像或文本描述），经过视觉编码和语言理解后，模型在混合动作空间中同时生成离散的文本响应 $a$ 和连续的 3D 姿势参数 $p$。整体策略被显式分解为两部分（Eq. 1）：

$$\pi_{\theta}(a, p | q) = \pi_{\theta}(a | q) \cdot \pi_{\theta}(p | q, a)$$

其中，离散子策略 $\pi_{\theta}(a | q)$ 由 LLaVA 语言模型头负责，生成自然语言响应；连续子策略 $\pi_{\theta}(p | q, a)$ 则建模为多变量高斯分布（Eq. 2）：

$$\pi_{\theta}(p | q, a) = \mathcal{N}(p; \mu_{\theta}(q, a), \Sigma_{\theta}(q, a))$$

该分布的均值和协方差由一个专用的连续姿势头预测，使得模型能够表达姿势生成中固有的“一对多”模糊性，而非像 SFT 那样被迫输出确定性折衷解。

### 模块关系与数据流

**Pose-Aware Encoder** 作为视觉前端，弥补了通用 CLIP 编码器在细粒度姿态信息捕捉上的不足。该模块采用在人体姿势估计任务上预训练的专用 Vision Transformer，与语言模型的视觉编码器并行工作，为后续策略头提供更丰富的空间特征。消融实验证实，该模块在 3DPW 数据集上带来了显著更高的空间位置奖励得分（Figure 3）。

**Discrete Policy Head** 和 **Continuous Policy Head** 共享骨干网络，但各自独立输出。给定输入 $q$，模型首先生成 $G$ 组候选响应 $\{a_i, p_i\}_{i=1}^G$，每组包含一个文本回答和一个 3D 姿势。这种组采样策略是 HyGRPO 算法进行组相对优势归一化的基础。

**Reward Functions** 模块包含四种任务特定的奖励函数，为策略优化提供多维度的训练信号：
- **空间位置奖励** $\mathcal{R}_{\mathrm{joint}}$：图像到姿势任务中，采用预测与真实关节位置欧氏距离的倒数（Eq. 7）；
- **语义对齐奖励** $\mathcal{R}_{\mathrm{semantic}}$：文本到姿势任务中，采用文本与姿势嵌入的余弦相似度（Eq. 8）；
- **格式奖励** $\mathcal{R}_{\mathrm{format}}$：二元奖励，鼓励输出符合指定模板（Eq. 9）；
- **文本相似度奖励** $\mathcal{R}_{\mathrm{text}}$：使用 BGE-M3 编码器计算生成回答与真实回答的余弦相似度（Eq. 10）。

### 优化机制

HyGRPO 算法接收这 $G$ 组候选及其奖励后，对离散和连续动作分别计算优势函数并进行组归一化，随后对两个策略头分别施加 PPO 风格的裁剪更新，并加入 KL 散度惩罚项以防止策略偏离参考模型过远。最终的目标函数为（Eq. 6）：

$$\mathcal{J}_{\mathrm{HyGRPO}} = \mathbb{E}_{q \sim \mathcal{D}, \{a_i, p_i\}_{i=1}^G \sim \pi_{\theta}(\cdot | q)} \Bigg[ \frac{1}{G} \sum_{i=1}^G \Big( \min(r_d \hat{F}_i, \mathrm{clip}(r_d, 1-\epsilon, 1+\epsilon) \hat{F}_i) \Big) + \frac{1}{V} \sum_{i=1}^V \Big( \min(r_c \hat{\Delta}_i, \mathrm{clip}(r_c, 1-\epsilon, 1+\epsilon) \hat{\Delta}_i) \Big) - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \Bigg]$$

这种分解式的优势信号设计是 Pose-RFT 成功的关键——标准离散 GRPO 无法提升连续姿势质量，而 HyGRPO 通过分别提供针对性的梯度信号，实现了离散语言和连续姿势的协同优化（Figure 4）。

整个框架的训练分为两个阶段：首先在姿势特定数据上进行监督预训练以获得合理的初始化策略，然后通过强化微调在奖励信号的引导下最大化语义和空间对齐目标，从而弥合 SFT 范式下的对齐差距。

### 补充图表

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/002_Figure_2.jpg]]
*Figure 2: Overview of Pose-RFT Framework. Our reinforcement fine-tuning framework for posespecific MLLMs. Given a multimodal input, the model generates multiple hybrid responses (text + pose). These candidates are evaluated using task-specific rewards, and our HyGRPO algorithm updates the policy to promote the generation of higher-reward outputs*

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/001_Figure_1.jpg]]
*Figure 1: Examples and Motivation. Left: An overview of our Pose-RFT framework for multimodal 3D pose generation. Right: Illustrating the alignment gap. While SFT yields a suboptimal averaged output, RFT produces a high-reward output for superior semantic and spatial alignment*



### 3.1 混合动作空间的强化学习建模

Pose-RFT 将多模态 3D 姿势生成重新形式化为一个**混合动作空间**（hybrid action space）的强化学习问题。模型同时输出两类动作：**离散的文本标记** $a$（自然语言响应）和**连续的 3D 姿势参数** $p$（SMPL 身体姿态）。

整体策略被分解为离散子策略与连续子策略的乘积：

$$\pi_{\theta}(a, p | q) = \pi_{\theta}(a | q) \cdot \pi_{\theta}(p | q, a)$$

其中 $q$ 为多模态输入（图像或文本），$\pi_{\theta}(a | q)$ 由 LLaVA 语言模型头建模，负责生成离散文本响应；$\pi_{\theta}(p | q, a)$ 为连续姿势子策略，**以文本响应为条件**进行姿势生成，体现了“先理解、后生成”的因果链条。

连续姿势策略被建模为**多变量高斯分布**：

$$\pi_{\theta}(p | q, a) = \mathcal{N}(p; \mu_{\theta}(q, a), \Sigma_{\theta}(q, a))$$

其中均值 $\mu_{\theta}$ 和协方差 $\Sigma_{\theta}$ 均由专用的连续姿态头（pose head）预测。这一分布建模是 Pose-RFT 区别于确定性回归 SFT 的核心——它赋予了模型在“一对多”模糊性下进行探索的能力，而非被迫输出一个折衷的“平均”姿势。

### 3.2 HyGRPO 算法：混合动作空间的组相对策略优化

HyGRPO 是 Pose-RFT 的核心优化算法，其关键创新在于**将综合优势函数分解为离散与连续两部分**，分别进行组归一化和 PPO 风格的裁剪更新，从而在统一的奖励信号下协同优化语言头和姿势头。

对于每个输入 $q$，模型采样 $G$ 个候选输出 $\{a_i, p_i\}_{i=1}^G$，并通过任务奖励函数获得标量奖励 $R_i$。HyGRPO 的目标函数为：

$$\mathcal{J}_{\mathrm{HyGRPO}} = \mathbb{E}_{q \sim \mathcal{D}, \{a_i, p_i\}_{i=1}^G \sim \pi_{\theta}(\cdot | q)} \Bigg[ \frac{1}{G} \sum_{i=1}^G \Big( \min(r_d \hat{F}_i, \mathrm{clip}(r_d, 1-\epsilon, 1+\epsilon) \hat{F}_i) \Big) + \frac{1}{V} \sum_{i=1}^V \Big( \min(r_c \hat{\Delta}_i, \mathrm{clip}(r_c, 1-\epsilon, 1+\epsilon) \hat{\Delta}_i) \Big) - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}}) \Bigg]$$

其中：
- $\hat{F}_i$ 为**离散优势**（discrete advantage），由文本响应的组相对奖励归一化得到，$r_d$ 为离散策略的概率比；
- $\hat{\Delta}_i$ 为**连续优势**（continuous advantage），由姿势输出的组相对奖励归一化得到，$r_c$ 为连续策略的概率比；
- $V$ 为连续动作的维度；
- 两个 $\min(\cdot, \text{clip}(\cdot))$ 项分别对离散和连续策略施加 PPO 风格的裁剪，防止策略更新过大；
- $\beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\mathrm{ref}})$ 为 KL 散度惩罚项，约束当前策略 $\pi_{\theta}$ 不过度偏离参考策略 $\pi_{\mathrm{ref}}$（通常为 SFT 初始化权重），防止语言能力退化。

**与标准 GRPO 的本质区别**：标准 GRPO 仅针对离散动作空间设计，其优势归一化和策略更新无法直接适用于连续姿势输出。实验证实（Figure 4），离散 GRPO 无法提升连续姿势质量，而 HyGRPO 通过分解优势信号实现了稳定且一致的性能增益。

### 3.3 任务奖励函数设计

Pose-RFT 设计了四类任务奖励函数，作为策略优化的唯一训练信号，替代 SFT 中的监督回归损失：

**空间位置奖励（Spatial Location Reward）**，用于图像到姿势任务：

$$\mathcal{R}_{\mathrm{joint}} = \frac{1}{\|J_{\mathrm{pred}} - J_{\mathrm{gt}}\|_2}$$

其中 $J_{\mathrm{pred}}$ 和 $J_{\mathrm{gt}}$ 分别为预测和真实的 3D 关节点位置。该奖励直接最大化空间对齐精度，是驱动姿势重建质量提升的核心信号。消融实验表明，移除该奖励导致 PA-MPJPE 上升 21.9mm（Table 5）。

**语义对齐奖励（Semantic Alignment Reward）**，用于文本到姿势任务：

$$\mathcal{R}_{\mathrm{semantic}} = \cos(\phi_t(q), \phi_p(p))$$

其中 $\phi_t$ 和 $\phi_p$ 分别为文本编码器和姿势编码器，计算文本-姿势嵌入的余弦相似度，直接优化跨模态语义对齐。

**格式奖励（Format Reward）**：

$$\mathcal{R}_{\mathrm{format}} = \begin{cases} 1, & \text{if output matches expected format} \\ 0, & \text{otherwise} \end{cases}$$

这是一个二元奖励，鼓励模型输出符合指定模板的结构化响应。消融实验（Table 5）表明，移除格式奖励会导致跨模态任务的灾难性失败（MPJPE 升至 131.9），说明格式约束是有效优化的必要前提。

**文本嵌入相似度奖励（Text Embedding Similarity Reward）**：

$$\mathcal{R}_{\mathrm{text}} = \cos(E(a_{\mathrm{pred}}), E(a_{\mathrm{gt}}))$$

使用 BGE-M3 编码器 $E(\cdot)$ 计算生成回答 $a_{\mathrm{pred}}$ 与真实回答 $a_{\mathrm{gt}}$ 的余弦相似度，确保语言输出的语义质量不因 RL 优化而退化。

### 3.4 Pose-Aware Encoder

为弥补通用 CLIP 视觉编码器在细粒度姿态信息捕获上的不足，Pose-RFT 在视觉管线中引入了一个**姿态感知视觉编码器**（Pose-Aware Encoder）。该模块基于在人体姿态估计任务上预训练的 ViT（Goel et al., 2023），专门提取与人体姿态相关的空间特征。消融实验（Figure 3）表明，相比仅使用 CLIP 编码器，该模块在 3DPW 数据集上显著提升了空间位置奖励分数，验证了专用视觉编码器对于精确空间对齐的必要性。

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/005_Figure_3.jpg]]
*Figure 3: Ablation Study of Pose-RFT’s Core Components. Both the Pose-Aware Encoder and Reinforcement Fine-tuning (RFT) contribute positively, with RFT providing the most significant gains across both semantic and spatial rewards*

### 补充图表

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/007_Figure_4.jpg]]
*Figure 4: Comparison between GRPO and HyGRPO. Training reward curves for pose generation. The discrete-only GRPO fails to yield improvements, whereas our proposed HyGRPO achieves consistent gains, demonstrating that a hybrid-action approach is essential for optimizing continuous pose outputs*



## 实验与关键发现

### 主实验结果：图像到姿势生成

Pose-RFT 在标准人体姿势估计基准上全面超越现有 MLLM 方法。**Table 1** 展示了在 3DPW 和 Human3.6M 数据集上的重建误差对比。在 3DPW 上，Pose-RFT 将 MPJPE 降至 **85.9 mm**，相比先前最优的 **UniPose**（Li et al., 2025c）的 94.7 mm 降低了 8.8 mm（相对提升 9.3%）；在 Human3.6M 上，MPJPE 从 69.2 mm 降至 **63.0 mm**，降幅 6.2 mm。值得注意的是，在更具挑战性的推理姿势估计（RPE）基准上，Pose-RFT 以 **198.6 mm** 的 MPJPE 建立了新的 SOTA，相比 UniPose 的 213.4 mm 降低了 14.8 mm，验证了基于 MLLM 的推理驱动姿势估计方法的有效性。

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/003_Table_1.jpg]]
*Table 1: Comparison on Human Pose Estimation task. Reconstruction errors are reported on the 3DPW and Human3.6M datasets*

### 主实验结果：文本到姿势生成

在文本到姿势生成任务上，**Table 2** 报告了 PoseScript 数据集上两种评估协议下的检索召回率。在全量检索协议下，Pose-RFT 在大多数指标上取得最优性能：R^{T2P}@5 达到 42.2，R^{P2T}@5 达到 **45.3**（相比 UniPose 的 42.1 提升 3.2 个百分点）。跨检索器评估（**Table 6**）进一步验证了泛化能力：使用 PoseEmbroider 作为检索模型时，Pose-RFT 的 R^{T2P}@5 达到 **55.2**，远超 SFT 基线的 47.7（提升 7.5 个百分点）。作者将这一成功归因于强化微调中的语义对齐奖励，有效增强了模型捕捉细粒度文本-姿势对应关系的能力。

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/004_Table_2.jpg]]
*Table 2: Comparison on Text-to-Pose Generation Task. Retrieval metrics (Recall@K, K=5, 10, 20) are reported on the PoseScript dataset under two evaluation protocols*

### 消融实验：核心组件贡献

**Figure 3** 展示了 Pose-RFT 核心组件的消融奖励曲线。Pose-Aware Encoder 的引入使 3DPW 上的空间位置奖励显著提升，证明专用姿态视觉编码器相比通用 CLIP 编码器能捕获更精细的姿态信息。强化微调（RFT）在所有奖励维度上贡献最大，验证了从监督模仿到奖励驱动优化的范式转变是性能提升的核心驱动力。

**Table 3** 的分布建模消融进一步揭示了关键设计选择。在 3DPW 上，基线模型（确定性回归）的 MPJPE 为 94.7 mm；引入多变量高斯分布建模（Dist.）后降至 89.2 mm；叠加 RFT 后进一步降至 **85.9 mm**。在 PoseScript-H2 上，完整配置（Baseline + Dist. + RFT）的 mRecall^{T2P} 达到 **57.6**，为最优结果。这表明分布建模与强化微调之间存在协同效应：分布建模为策略优化提供了必要的探索空间，而 RFT 通过奖励信号引导该空间向高质量区域收敛。

### 消融实验：HyGRPO 算法有效性

**Figure 4** 直接对比了标准 GRPO 与 HyGRPO 在姿势生成上的训练奖励曲线。仅优化离散文本动作的标准 GRPO 无法提升连续姿势质量，奖励曲线停滞不前；而 HyGRPO 通过分解离散/连续优势信号并分别进行 PPO 风格裁剪更新，实现了持续且显著的提升。这证明了在混合动作空间中，为连续策略提供独立、针对性的优势信号是稳定优化的必要条件。

### 消融实验：奖励函数组件分析

**Table 5** 的奖励组件消融揭示了各奖励函数的因果作用：

- **移除联合位置奖励**（Spatial Location Reward）：PA-MPJPE 上升 **21.9 mm**，严重损害几何精度，证明空间监督是姿势重建的核心驱动信号。
- **移除格式奖励**（Format Reward）：导致跨模态任务**灾难性失败**，MPJPE 飙升至 131.9 mm。这表明格式约束是有效优化的前提条件——若输出不符合预期模板，其他奖励函数无法正确计算，策略梯度将受到严重噪声干扰。
- **移除语义对齐奖励或文本相似度奖励**：分别在文本到姿势和图像到姿势任务上造成性能退化，验证了多模态奖励信号对维持跨任务能力的必要性。

### 训练过程定性分析

**Figure 5** 展示了文本到姿势生成的训练过程演化。随着强化微调的推进（从左至右），固定文本提示生成的 3D 姿势在语义一致性和结构合理性上逐步改善，直观验证了 RFT 的优化效果。**Figure 6** 的图像到姿势定性对比显示，Pose-RFT 在捕捉挑战性肢体方向和整体动态方面显著优于基线方法，尤其在复杂姿态下展现出更高的空间准确度和真实感。

### 失败模式与局限性

尽管 Pose-RFT 取得了显著性能提升，其有效性受限于奖励函数质量。当前奖励主要依赖几何距离和嵌入相似度，难以捕捉姿势自然度、上下文关联性等细微人类偏好，不准确的奖励信号可能误导策略优化方向。此外，HyGRPO 的组相对优势归一化要求为每个输入生成多个候选输出（组采样），引入了显著的计算开销，限制了向更大模型或数据集的扩展。在混合动作空间优化中，如何平衡离散语言和连续姿势的优化以避免语言理解能力退化，仍是开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/006_Table_3.jpg]]
*Table 3: Ablation study on distributional modeling (denoted as “Dist.”) for 3D pose generation. Reconstruction and retrieval metrics are reported on the 3DPW and PoseScript-H2 datasets*

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/013_Table_5.jpg]]
*Table 5: Ablation study on reward components. We report the performance impact of removing individual rewards during RL fine-tuning*

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/009_Figure_6.jpg]]
*Figure 6: Qualitative comparison on image-topose generation. Our Pose-RFT (bottom row) exhibits superior spatial accuracy and realism over baselines, especially in capturing challenging limb orientations and overall dynamics*

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/008_Figure_5.jpg]]
*Figure 5: Training progression of text-to-pose generation. As reinforcement fine-tuning progresses (left to right), 3D poses generated from fixed text prompts exhibit increasingly improved semantic consistency and structural plausibility*

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/011_Figure_7.jpg]]
*Figure 7: Pose-RFT results on human-written prompts from PoseScript (Delmas et al., 2022)*

![[assets/figures/papers/paper_list_l75_https_openreview_net_forum_id_ea1U1MgbdT/figures/012_Figure_8.jpg]]
*Figure 8: Pose-RFT results on in-the-wild videos*



## 定位与知识库关联

### 1. 与先前方法的对比定位

Pose-RFT 的核心突破在于将 3D 姿势生成的训练范式从**确定性监督模仿**转向**奖励驱动的强化学习**。在 Pose-RFT 之前，姿势特定的多模态大语言模型（MLLM）——如 **ChatPose** (Feng et al., 2024)、**UniPose** (Li et al., 2025c) 和 **ChatHuman** (Lin et al., 2024)——均采用监督微调（SFT）范式，通过最小化预测 SMPL 参数与真实值之间的 L2 回归损失来训练模型。这一范式存在根本性局限：

- **一对多模糊性无法处理**：同一文本描述（如“一个人在大步向前走”）或同一图像可对应多种合理的 3D 姿势。SFT 的确定性回归迫使模型预测所有合理解的平均值，产生“折衷”输出，在语义一致性和空间准确度上均表现不佳——这正是论文所指的**对齐差距**。
- **优化目标与评估指标脱节**：SFT 优化逐参数回归损失，而下游评估关注关节位置误差（MPJPE）或跨模态检索召回率，两者之间存在目标不一致。

Pose-RFT 通过以下四个关键改造位点（changed slots）系统性地解决了上述问题：

| 改造位点 | 基线方法（SFT范式） | Pose-RFT 方案 | 改造逻辑 |
|---------|-------------------|--------------|---------|
| **训练范式** | 监督微调（确定性回归） | 强化微调（RFT）+ HyGRPO 算法 | 从模仿“平均”输出转向最大化奖励信号，直接优化最终目标 |
| **姿势输出建模** | 确定性预测 SMPL 参数 | 多变量高斯分布策略（预测均值 μ 与协方差 Σ） | 赋予模型表达“一对多”不确定性的能力，从分布中采样而非预测单点 |
| **优化算法** | 标准监督损失（L2 回归） | HyGRPO（分解离散/连续优势，组归一化，PPO 裁剪） | 在混合动作空间上实现稳定策略优化，标准 GRPO 无法处理连续姿势 |
| **训练信号** | 单一姿态回归损失 | 四种任务奖励（空间位置、语义对齐、格式正确性、文本嵌入相似度） | 多维度奖励引导模型同时优化空间精度和语义一致性 |

### 2. 方法适用边界与局限

Pose-RFT 的有效性建立在以下前提之上，超出这些边界时方法可能失效或需要额外适配：

**奖励函数依赖性**：方法的性能上限直接受限于奖励函数的质量。当前设计的四种奖励（空间位置、语义对齐、格式正确性、文本嵌入相似度）覆盖了可自动计算的目标，但无法捕捉细微的人类偏好，如姿势的自然度、合理性或上下文关联性。消融实验证实了这一脆弱性——移除联合位置奖励导致 PA-MPJPE 上升 21.9 mm，而移除格式奖励则引发跨模态任务的灾难性失败（MPJPE 达 131.9），说明不准确的奖励信号可能严重误导策略优化方向。

**计算开销**：HyGRPO 的组相对优势归一化要求为每个输入生成多个候选输出（组大小 G），这引入了显著的计算开销。这一特性限制了该方法向更大模型（如 13B 或更大参数量的 MLLM）或更大规模数据集的直接扩展。论文未给出具体的计算开销量化数据，这一点需要读者根据实际部署场景评估。

**混合动作空间平衡**：离散语言和连续姿势的联合优化虽由 HyGRPO 统一处理，但如何在训练过程中保持两者的平衡仍是一个开放问题。过度优化姿势生成可能导致语言理解能力的退化，这一多任务能力衰减风险在当前实验中未得到充分探讨。

### 3. 开放问题与未来方向

基于 Pose-RFT 的设计逻辑和实验发现，以下问题值得后续工作关注：

1. **更丰富的奖励信号设计**：如何构建能够捕捉姿势自然度、上下文关联性等细微人类偏好的奖励函数？可能的路径包括引入人类反馈（RLHF）或训练可微分的姿势质量评估模型作为奖励模型。

2. **降低组归一化开销**：能否通过更高效的采样策略（如重要性采样）或离线优势估计来减少对每组 G 个候选的依赖，使得方法能扩展到更大模型或实时应用场景？

3. **多任务能力保持**：在混合动作空间 RL 中，如何显式约束语言能力的退化？引入语言相关的正则化项或阶段性训练策略可能是可行的缓解方案。

4. **跨领域泛化**：当前验证限于人体姿势生成，但混合动作空间 RL 的框架（离散文本 + 连续参数输出）理论上可泛化至其他多模态生成任务（如手部姿势、物体位姿估计），其实证验证有待开展。



## 原文 PDF

![[paperPDFs/ICLR_2026/Pose_RFT_Aligning_MLLMs_for_3D_Pose_Generation_via_Hybrid_Action_Reinforcement_F_91500ba4f27e.pdf]]
