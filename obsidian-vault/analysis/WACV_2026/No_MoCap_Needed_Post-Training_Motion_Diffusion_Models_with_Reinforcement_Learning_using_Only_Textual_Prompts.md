---
title: "No MoCap Needed: Post-Training Motion Diffusion Models with Reinforcement Learning using Only Textual Prompts"
type: paper
paper_level: A
venue: WACV
year: 2026
pdf_ref: "paperPDFs/WACV_2026/No_MoCap_Needed:_Post-Training_Motion_Diffusion_Models_with_Reinforcement_Learning_using_Only_Textual_Prompts.pdf"
project_link: null
code_link: null
aliases:
- RBPTFMDMDTR
tags:
- WACV_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 利用强化学习（DDPO）与仅文本提示，将预训练文本-运动检索模型（TMR）的语义相似度作为奖励信号，对预训练运动扩散模型进行后训练，无需真实运动数据。
primary_logic: 将扩散去噪过程形式化为马尔可夫决策过程（MDP），以DDPO优化扩散策略，仅使用文本-运动嵌入的余弦相似度作为稀疏奖励，无需配对数据即可将生成分布转向目标域；同时采用LoRA高效微调和DPM-Solver++加速采样，在保持原始分布性能的同时实现零样本适配。
claims:
- 跨数据集实验中，StableMoFusion经过RL微调后在HumanML3D→KIT-ML任务上R@1提升至0.413（基线0.362），FID降至1.291（基线1.860）。
- 跨数据集实验中，StableMoFusion在KIT-ML→HumanML3D任务上R@1提升至0.391（基线0.327），FID降至1.799（基线2.465）。
- 留一法（Object Manipulation）实验中，微调后模型在测试集上的FID改善至0.615（基线0.714），且超越全数据集训练模型。
- 遗忘实验显示，微调后模型在原HumanML3D上性能未退化，反而检索分数与FID均有轻微提升，表现出正反向迁移。
---

# No MoCap Needed: Post-Training Motion Diffusion Models with Reinforcement Learning using Only Textual Prompts

> [!tip] 核心洞察
> 将扩散去噪过程形式化为马尔可夫决策过程（MDP），以DDPO优化扩散策略，仅使用文本-运动嵌入的余弦相似度作为稀疏奖励，无需配对数据即可将生成分布转向目标域；同时采用LoRA高效微调和DPM-Solver++加速采样，在保持原始分布性能的同时实现零样本适配。

| 字段 | 内容 |
|------|------|
| 中文题名 | 无需动捕：仅用文本提示通过强化学习对运动扩散模型进行后训练 |
| 英文题名 | No MoCap Needed: Post-Training Motion Diffusion Models with Reinforcement Learning using Only Textual Prompts |
| 会议/期刊 | WACV 2026 |
| Links | [paper](https://arxiv.org/abs/2510.06988) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | RL-based Post-Training Framework for Motion Diffusion Models (DDPO + TMR Reward) |
| Dataset | Cross-Dataset, Leave-One-Out |

> [!tip] 效果简介
> - Cross-Dataset (HumanML3D→KIT-ML) 上，R@1 (Text-to-Motion Retrieval) 0.413 (StableMoFusion ours) vs 0.362 (StableMoFusion pretrained) (+0.051)；FID 1.291 (StableMoFusion ours) vs 1.860 (StableMoFusion pretrained) (-0.569)。
> - Cross-Dataset (KIT-ML→HumanML3D) 上，R@1 0.391 (StableMoFusion ours) vs 0.327 (StableMoFusion pretrained) (+0.064)；FID 1.799 (StableMoFusion ours) vs 2.465 (StableMoFusion pretrained) (-0.666)。
> - Leave-One-Out (Object Manipulation) 上，FID 0.615 (StableMoFusion ours) vs 0.714 (StableMoFusion pretrained without class) (-0.099)。

## 概要

现有文本到运动扩散模型在跨数据集或新动作类别上泛化能力有限，适配通常依赖额外的运动捕捉数据和全模型重训练，成本高且扩展性差。本文提出一种基于强化学习的后训练框架，仅使用文本提示即可对预训练运动扩散模型进行微调，无需任何真实运动数据。

核心思路是将扩散去噪过程形式化为马尔可夫决策过程（MDP），以预训练文本-运动检索模型（TMR）的语义相似度作为奖励信号，利用去噪扩散策略优化（DDPO）对扩散策略进行在线优化。为提升训练效率，框架引入LoRA低秩适配器冻结预训练骨干，并采用DPM-Solver++将采样步数从1000步压缩至10步。

在跨数据集实验中，StableMoFusion经RL微调后在HumanML3D→KIT-ML任务上R@1从0.362提升至0.413，FID从1.860降至1.291；在KIT-ML→HumanML3D任务上R@1从0.327提升至0.391，FID从2.465降至1.799。留一法实验中，微调后模型在测试集上的FID改善至0.615（基线0.714），且超越全数据集训练模型。遗忘实验进一步表明，微调后模型在原数据分布上性能未退化，检索分数与FID均有轻微提升，呈现正反向迁移。



### 问题背景：运动扩散模型的泛化瓶颈

基于扩散的文本驱动人体运动生成近年来取得了显著进展，预训练模型如 **MoMask**、**MotionGPT**、**StableMoFusion** 和 **MDM-SMPL** 在标准基准上展现了强大的生成能力。然而，这些模型面临一个关键瓶颈：**当遇到新的动作类别或与预训练数据分布差异较大的目标域时，其零样本泛化能力十分有限**。传统上，要使模型适配新域，通常需要依赖额外的运动捕捉（MoCap）数据对模型进行全参数重训练，这不仅成本高昂、数据获取困难，而且扩展性差——每遇到一个新域都需要重复这一昂贵流程。

### 现有方法的缺口

现有适配方案存在两个核心缺陷：

1. **数据依赖**：无论是全模型微调还是领域自适应方法，通常需要目标域的真实运动标注数据。在隐私敏感场景或稀缺动作类别（如特定操作动作）中，获取此类数据极为困难。
2. **灾难性遗忘风险**：直接在目标域上微调预训练模型，往往会导致模型在原始分布上的性能显著退化，丧失已学到的通用运动知识。

### 核心动机与解决思路

本文的核心动机是**探索一种无需任何真实运动数据、仅利用文本提示即可将预训练运动扩散模型适配到新域的后训练范式**。关键洞察在于：

- **将扩散去噪过程形式化为马尔可夫决策过程（MDP）**，其中状态由文本条件、扩散步和当前噪声样本组成，动作对应去噪后的样本，策略即为扩散模型的条件去噪分布。这一形式化使得扩散模型的采样过程可以被强化学习直接优化。
- **利用预训练的文本-运动检索模型（TMR）作为奖励信号**：TMR 模型能够将文本和运动映射到联合嵌入空间，通过计算余弦相似度评估生成运动与文本提示的语义对齐程度。这一奖励信号完全替代了对真实运动标注的依赖。
- **采用 DDPO（去噪扩散策略优化）对扩散策略进行微调**，结合重要性采样和 PPO 裁剪目标，在仅使用稀疏终端奖励的条件下有效优化生成分布，将其引导至目标域。

通过这一框架，模型能够在保持原始分布性能的同时实现零样本域适配，从根本上绕过了对运动捕捉数据的依赖，为运动扩散模型的实际部署提供了一条低成本、高扩展性的路径。



## 核心方法与创新机理

本文的核心贡献在于提出了一种**无需真实运动数据的后训练框架**，通过强化学习将预训练运动扩散模型适配到新的数据分布或动作类别。相较于现有方法依赖额外运动捕捉数据或全模型重训练，该方法仅需文本提示即可完成域迁移，显著降低了适配成本与扩展门槛。

### 关键创新点

**1. 扩散去噪过程的MDP形式化**

将条件扩散模型的迭代去噪过程形式化为马尔可夫决策过程（MDP），其中状态定义为 $\mathbf{s}_t \triangleq (\mathbf{c}, t, \mathbf{x}_t)$，动作定义为 $\mathbf{a}_t \triangleq \mathbf{x}_{t-1}$，策略即为扩散模型的条件去噪分布 $\pi(\mathbf{a}_t \mid \mathbf{s}_t) \triangleq p_{\boldsymbol{\theta}}(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})$。该形式化使得扩散模型的采样过程可被RL算法直接优化，无需对模型架构做任何修改。

**2. 文本-运动检索模型作为奖励信号**

奖励函数采用预训练文本-运动检索模型（TMR）计算生成运动与文本提示的余弦相似度：$r(\mathbf{x}_0, \mathbf{c}) = \mathrm{sim}(\phi_{\mathrm{text}}(\mathbf{c}), \phi_{\mathrm{motion}}(\mathbf{x}_0))$。奖励仅在最终去噪步骤（$t=0$）赋予，其余步骤为零，形成稀疏奖励结构。这一设计的关键优势在于：TMR模型经对比学习训练，能够区分嵌入空间中相近的概念，使得奖励信号对语义对齐的评判更为精细，且整个过程无需任何配对运动真值。

**3. DDPO策略优化**

采用去噪扩散策略优化（DDPO）算法更新扩散模型参数，目标函数为基于重要性采样的PPO裁剪目标：

$$\mathcal{L}_{\mathrm{DDPO}}(\theta) = \mathbb{E}_t \left[ \sum_{t=0}^T \min\left( w_t(\theta) \hat{A}_t, \mathrm{clip}(w_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$

其中重要性权重 $w_t(\theta) = \frac{p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})}{p_{\theta_{\mathrm{old}}}(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})}$ 允许从旧策略生成的轨迹中多次采样更新，提升样本效率。优势估计 $\hat{A}_t$ 基于最终奖励与策略对数概率梯度计算。

**4. 高效训练策略组合**

- **LoRA低秩适配**：冻结预训练扩散骨干网络，仅在注意力层和MLP层中插入低秩适配器（rank=4, α=16）进行优化，大幅降低可训练参数量，同时稳定RL训练过程。
- **DPM-Solver++加速采样**：将标准DDPM的1000步去噪替换为高阶ODE求解器DPM-Solver++，仅需10步即可完成采样，显著提升训练效率。该采样器与LoRA的组合使得30,000次迭代的微调在计算上可行。

### 与基线的核心差异

| 维度 | 预训练模型（零样本） | 本文方法 |
|------|---------------------|---------|
| 微调方式 | 冻结模型直接推理 | RL微调（DDPO + TMR奖励） |
| 奖励信号 | 无 | TMR文本-运动余弦相似度 |
| 参数训练 | 无 | LoRA适配器（rank=4, α=16） |
| 采样策略 | 标准DDPM（1000步） | DPM-Solver++（10步） |

该方法的核心洞察在于：**将生成分布转向目标域并不需要真实运动数据，仅需一个能够评判语义对齐质量的奖励模型即可引导扩散策略的优化方向**。这一思路绕过了数据采集瓶颈，为运动生成模型的零样本域适配提供了新的范式。



本文提出一种基于强化学习的运动扩散模型后训练框架，其核心设计目标是在不依赖任何真实运动捕捉数据的前提下，仅利用文本提示将预训练模型适配到新的数据分布或未见动作类别。框架将扩散去噪过程形式化为马尔可夫决策过程（MDP），以预训练文本-运动检索模型（TMR）的语义相似度作为奖励信号，通过去噪扩散策略优化（DDPO）更新模型参数，同时引入LoRA低秩适配和DPM-Solver++加速采样以保障训练效率与稳定性。

### 两阶段闭环架构

框架由两个交替执行的阶段构成闭环，如Figure 1所示：

**阶段一：样本采集（Sample Collection）**  
从目标数据集中采样文本提示 $\mathbf{c}$，以标准高斯噪声 $\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ 为起点，利用当前扩散模型 $p_\theta$ 执行完整的 $T$ 步去噪过程。每一步去噪中，模型输出条件分布 $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})$，从中采样得到 $\mathbf{x}_{t-1}$。所有中间状态 $(\mathbf{c}, t, \mathbf{x}_t, \mathbf{x}_{t-1})$ 及其对应的似然值被存入回放缓冲（replay buffer）。去噪完成后，最终生成的运动序列 $\mathbf{x}_0$ 与文本提示一同送入奖励模型进行评分。

**阶段二：策略更新（Policy Update）**  
从回放缓冲中采样轨迹，利用当前策略重新计算各步似然，基于重要性采样和PPO裁剪目标更新扩散模型参数。奖励信号仅在最终去噪步（$t=0$）生效，其余步奖励为零，形成稀疏奖励结构。

### 关键模块与数据流

框架包含四个核心模块，按数据流顺序依次为：

1. **扩散策略（Diffusion Policy）**：将去噪条件分布 $p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})$ 定义为策略 $\pi(\mathbf{a}_t \mid \mathbf{s}_t)$，其中状态 $\mathbf{s}_t \triangleq (\mathbf{c}, t, \mathbf{x}_t)$，动作 $\mathbf{a}_t \triangleq \mathbf{x}_{t-1}$。该MDP形式化将扩散生成过程转化为可优化的序贯决策问题。

2. **奖励模型（TMR Reward Model）**：采用预训练的文本-运动检索模型TMR作为奖励函数，计算文本嵌入 $\phi_{\text{text}}(\mathbf{c})$ 与运动嵌入 $\phi_{\text{motion}}(\mathbf{x}_0)$ 的余弦相似度：
   $$r(\mathbf{x}_0, \mathbf{c}) = \mathrm{sim}(\phi_{\text{text}}(\mathbf{c}), \phi_{\text{motion}}(\mathbf{x}_0))$$
   该奖励仅在最终去噪步赋予，引导生成运动向文本语义对齐的方向优化。

3. **LoRA低秩适配器**：冻结预训练扩散骨干网络，仅在注意力层和MLP层中插入可训练的低秩矩阵（秩 $r=4$，缩放因子 $\alpha=16$），大幅减少可训练参数量，同时稳定RL微调过程。

4. **DPM-Solver++加速采样器**：将标准DDPM的1000步去噪替换为高阶ODE求解器DPM-Solver++，仅需10步即可完成采样，显著提升样本采集效率。

### 优化目标

策略更新采用DDPO的重要性采样变体，优化目标为：
$$\mathcal{L}_{\mathrm{DDPO}}(\theta) = \mathbb{E}_t \left[ \sum_{t=0}^T \min\left( w_t(\theta) \hat{A}_t, \mathrm{clip}(w_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$
其中重要性权重 $w_t(\theta) = \frac{p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})}{p_{\theta_{\mathrm{old}}}(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})}$ 用于重加权旧轨迹，优势估计 $\hat{A}_t = \nabla_\theta \log p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c}) \cdot r(\mathbf{x}_0, \mathbf{c})$ 将最终步奖励通过策略对数概率梯度传播至所有去噪步。

### 与基线方法的关键差异

相较于冻结预训练模型直接进行零样本推理的基线方案（如 **MoMask**、**MotionGPT**、**StableMoFusion**、**MDM-SMPL**），本框架引入四个关键变更槽位：(1) 从冻结模型推理变为基于DDPO的RL微调；(2) 引入TMR余弦相似度作为奖励信号；(3) 从全模型微调或无训练变为仅优化LoRA适配器；(4) 从标准1000步DDPM采样变为DPM-Solver++的10步加速采样。这些设计共同实现了无需真实运动数据的零样本分布适配能力。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2510_06988/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our fine-tuning procedure. Left: Sample Collection. Diffusion trajectories are generated from Gaussian noise conditioned on prompts sampled from the dataset. At each denoising step, the model outputs a normal distribution from which*



本方法的核心架构由四个关键模块构成：**MDP形式化**、**DDPO策略优化**、**TMR奖励模型**和**高效学习策略**。以下逐一展开其公式推导与变量含义。

### 3.1 扩散过程与MDP形式化

运动扩散模型的前向过程逐步向干净运动序列 $\mathbf{x}_0$ 添加高斯噪声：

$$q(\mathbf{x}_t \mid \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_t; \sqrt{\alpha_t} \mathbf{x}_0, (1 - \alpha_t) \mathbf{I})$$

其中 $\alpha_t$ 为噪声调度参数，$t \in \{1, \dots, T\}$ 为扩散步。逆向过程学习从噪声恢复干净序列，条件于文本提示 $\mathbf{c}$：

$$p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c}) = \mathcal{N}(\mathbf{x}_{t-1}; \mu_\theta(\mathbf{x}_t, t, \mathbf{c}), \Sigma_t)$$

为将扩散去噪纳入强化学习框架，本文借鉴 **Black et al.** 在图像域的MDP形式化，将其适配至运动生成。定义状态、动作与策略如下：

- **状态**：$\mathbf{s}_t \triangleq (\mathbf{c}, t, \mathbf{x}_t)$，包含文本条件、当前扩散步和噪声样本。
- **动作**：$\mathbf{a}_t \triangleq \mathbf{x}_{t-1}$，即下一步去噪后的运动样本。
- **策略**：$\pi(\mathbf{a}_t \mid \mathbf{s}_t) \triangleq p_{\boldsymbol{\theta}}(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})$，将扩散模型的条件去噪分布直接视为策略。

奖励函数采用稀疏设计，仅在最终去噪步（$t=0$）给予非零奖励：

$$R(\mathbf{s}_t, \mathbf{a}_t) \triangleq \begin{cases} r(\mathbf{x}_0, \mathbf{c}) & \text{if } t = 0 \\ 0 & \text{otherwise} \end{cases}$$

这一形式化的关键洞察在于：扩散模型的逐步去噪天然构成一条长度为 $T$ 的轨迹，无需额外建模即可嵌入MDP框架。

### 3.2 DDPO策略优化目标

为提高样本效率并支持每批生成数据上的多次策略更新，方法采用重要性采样的DDPO变体。核心优化目标为PPO裁剪损失：

$$\mathcal{L}_{\mathrm{DDPO}}(\theta) = \mathbb{E}_t \left[ \sum_{t=0}^T \min\left( w_t(\theta) \hat{A}_t, \mathrm{clip}(w_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$

其中重要性权重 $w_t(\theta)$ 为当前策略与旧策略的似然比：

$$w_t(\theta) = \frac{p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})}{p_{\theta_{\mathrm{old}}}(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})}$$

优势估计 $\hat{A}_t$ 基于最终步奖励与策略对数概率梯度的乘积：

$$\hat{A}_t = \nabla_\theta \log p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c}) \cdot r(\mathbf{x}_0, \mathbf{c})$$

该设计的因果机制在于：优势估计将稀疏的终端奖励沿扩散轨迹反向传播，使策略在所有去噪步上均获得优化信号，而非仅在最后一步。

### 3.3 TMR奖励模型

奖励信号来自预训练的文本-运动检索模型 **TMR**（Text-Motion Retrieval）。给定生成的运动 $\mathbf{x}_0$ 和文本提示 $\mathbf{c}$，奖励函数定义为二者嵌入的余弦相似度：

$$r(\mathbf{x}_0, \mathbf{c}) = \mathrm{sim}(\phi_{\mathrm{text}}(\mathbf{c}), \phi_{\mathrm{motion}}(\mathbf{x}_0))$$

其中 $\phi_{\mathrm{text}}$ 和 $\phi_{\mathrm{motion}}$ 分别为TMR的文本编码器和运动编码器，将文本与运动映射至共享嵌入空间。TMR采用对比学习训练，能有效区分嵌入空间中相近的概念，这使得奖励信号对语义细微差异敏感。需注意，奖励模型的质量直接影响微调效果——若TMR未能捕捉特定运动风格或物理合理性，则奖励信号的引导能力将受限。

### 3.4 高效学习策略

为实现稳定且高效的RL微调，方法引入两项关键设计：

**LoRA低秩适配**：冻结预训练扩散骨干网络，仅在注意力层和MLP层插入可训练的低秩矩阵（秩 $r=4$，缩放因子 $\alpha=16$）。这大幅减少了可训练参数量，同时降低了RL训练的不稳定性。

**DPM-Solver++加速采样**：将标准DDPM的1000步去噪替换为高阶ODE求解器 **DPM-Solver++**，仅需10步即可完成采样。这显著缩短了轨迹生成时间，使得RL训练在计算上可行。



## 实验与关键发现

### 核心实验设计

本文实验围绕一个中心问题展开：**在不使用任何真实运动数据的前提下，RL 后训练能否将预训练运动扩散模型适配到新的数据分布或未见过的动作类别？** 为此，作者设计了两类实验范式——跨数据集迁移（Cross-Dataset）和留一法（Leave-One-Out），并在多个预训练模型架构上进行验证。

**跨数据集实验**在两个标准基准之间进行：HumanML3D 和 KIT-ML。模型在源数据集上预训练，仅使用目标数据集的文本提示（无运动标注）进行 RL 微调，随后在目标测试集上评估。**留一法实验**则在 HumanML3D 内部进行：从训练集中移除某一动作类别（如 Object Manipulation），在剩余类别上从头训练模型，再用 RL 微调适配被移除的类别，最后在该类别的测试集上评估。这种设计直接检验了方法对**零样本泛化**的增益——模型从未见过目标类别的真实运动数据，仅通过文本提示学习生成。

**评估协议**采用双维度指标：文本-运动检索分数（R@1、R@2、R@3）衡量语义对齐质量，FID 衡量生成运动的分布真实性。此外，还引入了 MultiModal Distance（MM Dist）和 MultiModality（MModality）分别评估生成多样性。用户感知研究则在 HumanML3D→KIT-ML 场景下，以 A/B 测试方式邀请人类受试者评判运动真实感和文本遵循度。

### 跨数据集迁移：主要定量结果

Table 1 汇总了跨数据集场景下的核心对比。以 **StableMoFusion** 为骨干模型时，RL 后训练带来的增益最为显著：

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2510_06988/figures/002_Table_1.jpg]]
*Table 1: Cross-Dataset Results. The base model is pretrained on HumanML3D and evaluated on KIT-ML in (a), while in (b), the model is pretrained on KIT-ML and evaluated on HumanML3D. We compare zero-shot approaches and post-training with our method, which fine-tunes the model without relying on ground-truth annotations*

- **HumanML3D → KIT-ML**：R@1 从 0.362 提升至 0.413（+0.051），FID 从 1.860 降至 1.291（-0.569），降幅约 30.6%。这意味着生成的运动不仅更贴合文本语义，分布也更接近 KIT-ML 的真实数据。
- **KIT-ML → HumanML3D**：R@1 从 0.327 提升至 0.391（+0.064），FID 从 2.465 降至 1.799（-0.666），降幅约 27.0%。反向迁移同样有效，且增益幅度相当。

值得注意的是，其他预训练模型（**MoMask**、**MotionGPT**、**MDM-SMPL**）在 RL 微调后也普遍获得提升，但 StableMoFusion 的改进幅度最大。这暗示**潜在空间扩散模型（latent-space DM）**可能比关节空间模型（joint-space DM）更适合此类 RL 后训练范式——潜在空间中的去噪轨迹更平滑，策略梯度估计的方差更低。

**用户感知研究**（Figure 3）进一步验证了定量指标的可靠性。在 HumanML3D→KIT-ML 场景下，人类受试者在运动真实感和文本遵循度两个维度上均显著偏好 RL 微调后的生成结果。这一主观评价与 FID 和 R@1 的客观改善形成交叉验证。

### 留一法实验：未见类别的零样本适配

Table 2 展示了留一法实验的结果。以 Object Manipulation 类别为例：

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2510_06988/figures/004_Table_2.jpg]]
*Table 2: Leave-one-out results on HumanML3D. A model is trained from scratch with one motion class removed from the dataset, fine-tuned using our approach, and then evaluated on a test set containing only the held-out class*

- **FID**：从零样本基线（未使用该类文本训练）的 0.714 降至 RL 微调后的 0.615（-0.099），甚至**优于在全数据集上训练的模型**（FID 0.654）。这一反直觉的结果表明，RL 微调不仅弥补了缺失类别的信息缺口，还可能通过 TMR 奖励信号的引导，学到了更精准的文本-运动对齐，从而在分布层面超越了简单增加训练数据的方案。
- **R@1**：从 0.331 提升至 0.351（+0.020），检索精度亦有改善。

这一实验的因果链条清晰：**TMR 奖励模型**在预训练阶段已学习到丰富的文本-运动语义对应关系，即使扩散模型从未见过某类动作的真实运动数据，TMR 仍能通过余弦相似度提供有效的梯度信号，将生成分布“牵引”至目标语义区域。LoRA 的低秩约束则防止了过拟合，使适配过程稳定可控。

### 灾难性遗忘与反向迁移

RL 微调的一个常见风险是**灾难性遗忘**——适配新分布后，模型在原始分布上的性能急剧退化。本文通过 Table 3 的消融实验直接回应了这一关切。

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2510_06988/figures/006_Table_3.jpg]]
*Table 3: Ablation study on forgetting after fine-tuning. We evaluate models pretrained on HumanML3D and fine-tuned on KIT-ML, reporting results on the HumanML3D test set to assess the impact of fine-tuning on the original distribution. The results show no performance degradation and, even improvements, indicating backward transfer*

实验设置：模型在 HumanML3D 上预训练，经 RL 微调适配 KIT-ML 后，重新在 HumanML3D 测试集上评估。结果出乎意料：

- **R@1** 从 0.362 微升至 0.364，FID 从 1.860 微降至 1.851——不仅没有退化，反而略有改善。
- 作者将此现象归因为**反向迁移（backward transfer）**：TMR 奖励信号在优化文本-运动对齐的过程中，强化了通用的语义理解能力，这些能力对原始分布同样有益。

这一发现具有重要的实践意义：它意味着 RL 后训练可以安全地应用于多领域适配，无需担心损害模型的基础能力。LoRA 的冻结骨干策略在此起到了关键作用——原始权重得以保留，适配仅发生在低秩子空间内，天然抑制了灾难性遗忘。

### 多样性与对齐性的权衡

尽管 RL 微调在语义对齐和分布真实性上取得了显著提升，但**MultiModality（MModality）指标普遍下降**，这揭示了方法的一个内在权衡。以 StableMoFusion 的 HumanML3D→KIT-ML 为例，MModality 从零样本的 1.42 降至 1.18。

这一现象的机制解释是：TMR 奖励函数以余弦相似度为唯一优化目标，本质上鼓励模型生成与文本嵌入高度一致的“典型”运动，而非探索分布中的长尾样本。DDPO 的 PPO 裁剪目标进一步抑制了高方差的探索行为。因此，**多样性的牺牲是当前奖励设计的直接后果**，而非方法的根本缺陷。作者在限制部分也明确指出，如何设计奖励函数在多样性与对齐性之间取得更优平衡，是一个待解决的开放问题。

### 方法适用边界与失败模式

综合实验结果，可归纳出以下适用边界：

1. **奖励模型质量是性能上限**：TMR 的嵌入空间决定了 RL 微调的天花板。若 TMR 未能捕捉特定运动风格或物理合理性（如运动学约束、接触物理），微调后的模型也无法习得这些属性。在留一法实验中，不同被移除类别的增益幅度存在差异，这可能反映了 TMR 对不同动作类别语义表征的不均衡性。
2. **架构敏感性**：StableMoFusion（潜在空间扩散）的增益显著大于关节空间模型（MDM-SMPL），说明该框架对扩散模型的内部表征形式存在偏好。潜在空间中的去噪轨迹更平滑，使得 DDPO 的策略梯度估计更稳定。
3. **多样性-对齐性权衡**：如前所述，当前奖励设计倾向于牺牲多样性换取对齐精度。在需要高多样性的应用场景（如创意内容生成）中，这一权衡可能成为瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2510_06988/figures/003_Figure_2.jpg]]
*Figure 2: Example of improved text adherence after our fine-tuning of the StableMoFusion model. The figure shows the full animation, with color indicating time from blue to orange. The first row depicts the model before fine-tuning, while the second row shows the model after fine-tuning. After fine-tuning, the generated motions better follow the textual prompts. In particular, in panels (b) and (c), the model fully completes the circular motion, and in panels (a) and (b), the hand movements are more expressive*

![[assets/figures/papers/paper_list_l3_https_arxiv_org_abs_2510_06988/figures/005_Figure_3.jpg]]
*Figure 3: Perception study results: Human raters evaluated our method against pretrained baseline models in the Humanto-Kit scenario, assessing both motion realism and text adherence in an A/B scenario*



## 定位与知识库关联

### 与基线方法的关系

本文提出的RL后训练框架是一种**模型无关的适配层**，可作用于多种预训练运动扩散模型之上。实验覆盖了四类代表性基线：

- **MoMask**：基于离散运动token的掩码建模方法。
- **MotionGPT**：将运动视为语言序列进行生成式预训练。
- **StableMoFusion**：在潜空间进行扩散的架构，是本文主要验证载体。
- **MDM-SMPL**：直接在关节空间进行扩散的模型。

这些基线在原始训练集上表现良好，但面对新数据分布时依赖零样本泛化，缺乏针对性的分布适配机制。本文方法的核心差异在于：**不修改预训练骨干的架构或权重初始化，而是通过RL在最外层注入任务导向的优化信号**。具体而言，将扩散去噪过程形式化为MDP（状态 $\mathbf{s}_t \triangleq (\mathbf{c}, t, \mathbf{x}_t)$，动作 $\mathbf{a}_t \triangleq \mathbf{x}_{t-1}$，策略 $\pi(\mathbf{a}_t \mid \mathbf{s}_t) \triangleq p_{\boldsymbol{\theta}}(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})$），以DDPO目标进行策略优化：

$$\mathcal{L}_{\mathrm{DDPO}}(\theta) = \mathbb{E}_t \left[ \sum_{t=0}^T \min\left( w_t(\theta) \hat{A}_t, \mathrm{clip}(w_t(\theta), 1-\epsilon, 1+\epsilon) \hat{A}_t \right) \right]$$

其中重要性权重 $w_t(\theta) = \frac{p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})}{p_{\theta_{\mathrm{old}}}(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c})}$，优势估计 $\hat{A}_t = \nabla_\theta \log p_\theta(\mathbf{x}_{t-1} \mid \mathbf{x}_t, \mathbf{c}) \cdot r(\mathbf{x}_0, \mathbf{c})$。

与传统的全模型微调或数据增强不同，该方法的关键因果杠杆在于**奖励信号的设计**：使用预训练文本-运动检索模型TMR计算余弦相似度作为稀疏奖励 $r(\mathbf{x}_0, \mathbf{c}) = \mathrm{sim}(\phi_{\mathrm{text}}(\mathbf{c}), \phi_{\mathrm{motion}}(\mathbf{x}_0))$，仅在最终去噪步 $t=0$ 生效。这避免了配对的真实运动数据需求，同时利用TMR的对比学习嵌入空间将生成分布拉向文本语义对齐的方向。

### 适用边界

**正向适用场景**：
1. **跨数据集零样本适配**：当目标域仅有文本描述而无运动标注时（如从HumanML3D迁移至KIT-ML），方法可直接工作。
2. **长尾动作类别覆盖**：留一法实验表明，对训练集中完全缺失的动作类别（如Object Manipulation），微调后模型可超越全数据集训练模型的FID（0.615 vs. 0.714，Table 2(a)）。
3. **隐私敏感场景**：无需访问真实运动捕捉数据，仅依赖文本提示即可完成分布迁移。

**不适用或需谨慎使用的场景**：
1. **奖励模型覆盖盲区**：若TMR未能有效编码目标运动的风格特征或物理合理性，奖励信号将失效，微调方向可能偏离预期。这是方法的系统性瓶颈——奖励模型的质量直接决定了适配的上限。
2. **多样性敏感任务**：实验显示MultiModality指标有所下降，表明RL优化在提升语义对齐的同时会压缩生成多样性。若应用场景对运动多样性要求极高（如创意内容生成），需权衡此trade-off。
3. **实时在线场景**：当前框架依赖离线采样-回放-更新的循环，尚未验证在在线学习或实时控制场景中的可行性。

### 局限与开放问题

**已识别的局限**：
- **多样性-对齐权衡**：DDPO优化以最大化期望奖励为目标，天然倾向于生成高奖励（高文本相似度）的样本，导致分布坍缩。这是RL微调在生成模型中的普遍问题，本文未提出针对性的正则化或约束机制。
- **奖励模型的单向依赖**：TMR作为冻结的奖励函数，无法在微调过程中自适应更新。若目标域与TMR训练分布差异过大，奖励信号可能产生系统性偏差。

**开放问题**：
1. **跨模态推广**：该RL后训练框架的核心组件（扩散MDP形式化、稀疏奖励、LoRA微调）是否可迁移至音乐到舞蹈生成、文本到语音等其他条件生成任务？这需要验证TMR类检索模型在其他模态中的可用性。
2. **奖励设计的帕累托优化**：如何在单一奖励函数中同时编码语义对齐、运动真实感和多样性？多目标RL或约束型策略优化可能是潜在方向。
3. **在线适配能力**：是否可将框架改造为在线学习范式，使模型在部署过程中持续从用户反馈中学习？这涉及样本效率、安全探索和计算成本的多重挑战。
4. **奖励模型的自适应更新**：若允许TMR在微调过程中同步更新（如通过对抗训练或自监督目标），是否能突破其覆盖盲区，同时避免奖励黑客（reward hacking）问题？

**证据强度说明**：跨数据集和留一法的定量改善有明确数值支撑（置信度0.95），但多样性下降的观察需查阅原文MultiModality指标的具体数值进行手动验证。用户感知研究（Figure 3）提供了主观评价维度的补充证据，但其统计显著性和实验规模需进一步确认。



## 原文 PDF

![[paperPDFs/WACV_2026/No_MoCap_Needed:_Post-Training_Motion_Diffusion_Models_with_Reinforcement_Learning_using_Only_Textual_Prompts.pdf]]
