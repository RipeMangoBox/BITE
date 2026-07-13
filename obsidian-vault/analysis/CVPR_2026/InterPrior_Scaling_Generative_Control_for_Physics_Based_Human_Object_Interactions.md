---
title: "InterPrior: Scaling Generative Control for Physics-Based Human-Object Interactions"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/InterPrior_Scaling_Generative_Control_for_Physics_Based_Human_Object_Interactions.pdf
project_link: null
code_link: null
aliases:
- InterPrior
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在蒸馏得到的变分策略基础上进行强化学习微调，利用随机初始化与稀疏目标作为局部优化器，提升策略鲁棒性。
primary_logic: 蒸馏为策略提供了自然的行为先验初始化，而强化学习微调作为一种局部优化器，在保持行为自然性的同时扩展了策略的泛化边界，使其能够处理未见目标和失败恢复。
claims:
- 蒸馏得到的变分策略能够从多模态观测和高层意图中重建运动，但其在大规模HOI配置空间上不泛化。
- 强化学习微调通过数据增强和扰动，提升策略在未见目标和初始化上的能力，并保持预训练知识。
- InterAct/OMOMO (Snapshot goals) 上 Success Rate (Succ↑) % = 90.0
- OMOMO select (full-reference, thin objects) 上 Success Rate (SR↑) % = 83.2 (InterPrior)
---

# InterPrior: Scaling Generative Control for Physics-Based Human-Object Interactions

> [!tip] 核心洞察
> 蒸馏为策略提供了自然的行为先验初始化，而强化学习微调作为一种局部优化器，在保持行为自然性的同时扩展了策略的泛化边界，使其能够处理未见目标和失败恢复。

| 字段 | 内容 |
|------|------|
| 中文题名 | InterPrior：面向物理人-物交互的可扩展生成控制 |
| 英文题名 | InterPrior: Scaling Generative Control for Physics-Based Human-Object Interactions |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.06035) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | InterPrior |
| Dataset | InterAct/OMOMO, OMOMO select, HODome |

> [!tip] 效果简介
> - InterAct/OMOMO (Snapshot goals) 上，Success Rate (Succ↑) % 90.0。
> - OMOMO select (full-reference, thin objects) 上，Success Rate (SR↑) % 83.2 (InterPrior) vs 63.9 (InterMimic) (+19.3)。
> - HODome (novel interactions, finetuned) 上，Success Rate (SR↑) % 72.4 (InterPrior + finetune)。

## 概要

物理仿真中的人-物交互（Human-Object Interaction, HOI）生成控制面临一个根本瓶颈：大规模演示数据无法覆盖所有可能的构型空间，导致纯蒸馏策略在未见目标及初始化条件下泛化能力严重不足。InterPrior 针对这一问题提出了一条“蒸馏初始化 + 强化学习局部优化”的技术路线——首先将全参考模仿专家蒸馏为变分策略，获得自然的行为先验；随后通过强化学习微调，在不破坏预训练知识的前提下扩展策略的泛化边界，使其能够处理未见目标和失败恢复。

方法上，InterPrior 构建了一个三阶段训练范式：（I）在大规模 HOI 数据上训练带形状奖励与扰动的全参考模仿专家 **InterMimic+**；（II）将该专家蒸馏为掩码条件变分策略，学习多模态潜技能空间；（III）对蒸馏策略进行强化学习后训练，利用随机初始化与稀疏目标帧的 in-betweening 任务提升鲁棒性。关键改进槽位包括引入无参考手部奖励 $r_h$、将潜变量投影到单位超球面以提高鲁棒性，以及在后训练中保留蒸馏正则化以防止遗忘。

实验表明，InterPrior 在 InterAct/OMOMO 的 Snapshot goals 任务上达到 90.0% 成功率；在 OMOMO 薄物体全参照跟踪上，成功率从 **InterMimic** 的 63.9% 提升至 83.2%（+19.3%）；在 HODome 新交互上微调后达到 72.4%。消融研究进一步证实，RL 微调将 Contact 任务失败率从 5.4 降至 2.9，并在多目标链任务上大幅提升成功率。

当前方法的局限在于：策略仍受训练数据覆盖率和质量的约束，高度损坏或未见的交互模式无法可靠恢复；长序列 rollout 中可能出现物体穿透、脚部滑动等物理伪影；接触与手部表示尚不支持精细手指灵巧操作；三阶段流程增加了训练复杂度与超参数负担。



### 物理人-物交互控制的规模化困境

在物理仿真器中生成自然且鲁棒的人-物交互（Human-Object Interaction, HOI）运动，是具身智能与角色动画领域的核心挑战。现有工作主要沿两条路径展开：基于全参考的运动模仿（motion imitation）和基于目标条件（goal-conditioned）的生成控制。全参考模仿策略（如 **InterMimic**）通过密集跟踪参考运动轨迹，能够在训练分布内产生高质量的交互行为，但其本质是“回放”而非“生成”——策略缺乏对高层意图的理解，无法在未见目标构型或随机初始化下自主决策。目标条件策略则试图直接从高层意图（如目标物体位姿、接触点）生成运动，但其训练依赖于大规模、多样化的演示数据，而HOI的构型空间随物体种类、交互类型和人体自由度的组合呈指数级膨胀，数据覆盖的稀疏性成为根本瓶颈。

### 蒸馏-微调范式的缺失

近期工作探索了将全参考专家策略蒸馏为目标条件策略的思路（如 **MaskedMimic**），试图将专家的运动知识压缩到一个可接受高层目标输入的变分策略中。这一范式为策略提供了自然的行为先验，使生成的运动保持类人特征。然而，纯蒸馏策略在构型空间的大规模外推上存在固有局限：蒸馏过程本质是对专家分布的拟合，当测试时的目标与初始化偏离训练分布时，策略缺乏主动探索和纠错的能力，表现为抓取失败后无法恢复、对细薄物体的接触不稳定、以及长序列多目标链中的累积误差。

### 核心洞察与本文动机

本文的核心洞察在于重新定位蒸馏与强化学习的关系：**蒸馏提供行为先验，强化学习微调作为局部优化器扩展泛化边界**。具体而言，蒸馏得到的变分策略已经编码了丰富的多模态技能潜空间，使其成为强化学习微调的理想初始化——微调无需从零开始探索，而是在已有行为结构的基础上，通过数据增强（物理扰动、随机初始化）和稀疏目标奖励，将策略的能力边界推向训练分布之外。这一范式在保持行为自然性的同时，使策略能够处理未见目标构型、不完美初始化和失败恢复等实际部署场景。

基于上述动机，本文提出 **InterPrior**——一个三阶段的可扩展生成控制框架：(I) 在大规模HOI数据上训练增强的全参考专家策略（InterMimic+）；(II) 将专家蒸馏为掩码条件变分策略，学习结构化的潜技能空间；(III) 对蒸馏策略进行强化学习后训练，以in-betweening任务形式提升泛化性。该框架的核心设计原则是：**蒸馏与微调的协同**——蒸馏阶段通过ELBO、尺度正则化和时间一致性损失构建紧凑的潜空间，微调阶段在保留蒸馏正则化的前提下引入稀疏目标奖励，使策略在“记住”自然行为的同时“学会”应对更广泛的构型。



## 核心方法与创新机理

InterPrior 的核心创新在于将“蒸馏+强化学习微调”的两阶段范式引入物理人-物交互（HOI）控制，并围绕**多模态目标条件化**与**策略鲁棒性**设计了三个关键的 changed slots，使其区别于现有的模仿学习基线。

### 1. 从全参考模仿到多模态目标条件化

传统全参考模仿策略（如 **InterMimic**）要求提供完整的参考运动轨迹，在未见目标或初始化扰动下泛化能力有限。InterPrior 通过**掩码条件变分蒸馏**，将全参考专家策略压缩为一个仅依赖稀疏目标（快照、轨迹、接触）的生成式策略，从而摆脱了对完整参考的依赖。

在此过程中，方法引入了两个关键设计：

- **无参考手部奖励（$r_h$）**：基线专家仅使用跟踪奖励，无法在没有参考的情况下激励正确的抓握行为。InterPrior 在专家训练阶段即引入基于当前模拟状态的包裹式手部奖励 $r_h$，使蒸馏后的策略即使在没有完整手指参考时也能产生合理的接触行为。
- **潜变量单位球投影（$z_t := z_t / \|z_t\|$）**：标准 VAE 的潜空间缺乏边界约束，导致采样时可能落入低密度区域。InterPrior 在采样后将潜变量投影到单位超球面，增强了推理时的鲁棒性和行为自然性。

### 2. 强化学习微调作为局部优化器

蒸馏获得的变分策略虽然提供了自然的行为先验，但在大规模 HOI 配置空间上无法可靠泛化——这是该工作的核心瓶颈。InterPrior 将强化学习微调定位为一种**局部优化器**：在保持预训练知识的前提下，通过数据增强和物理扰动，扩展策略的泛化边界。

具体而言，微调被形式化为一个 **in-betweening 任务**：策略从随机初始配置出发，向数据集中随机抽取的单帧目标进行跟踪。奖励设计由能量奖励、手部奖励、稀疏目标成功奖励和终止惩罚组成：

$$r_t^{\mathrm{PT}} = (r_{\mathrm{energy}} \times r_{\mathrm{h}}) + r_{\mathrm{goal}} + r_{\mathrm{ter}}$$

其中目标奖励 $r_{\mathrm{goal}}$ 仅在当前状态与目标的掩码特征距离低于阈值 $\tau$ 时激活，提供稀疏的成功信号。同时，通过蒸馏正则化项保留预训练知识，防止灾难性遗忘。

### 3. 与基线的本质差异

| 设计维度 | InterMimic / MaskedMimic | InterPrior |
|---------|------------------------|------------|
| 手部奖励 | 无（仅跟踪参考） | 引入无参考包裹奖励 $r_h$ |
| 潜变量正则化 | 无（标准 VAE） | 单位超球面投影 |
| 训练策略 | 仅蒸馏 | 蒸馏 + RL 微调（in-betweening + 蒸馏正则化） |

消融实验验证了这些 changed slots 的有效性：使用改进的 InterMimic+ 专家替换原专家后，成功率和泛化性均有提升；增加潜变量尺度损失和时间一致性损失进一步提高了目标跟随精度；RL 微调则将 Contact 任务的失败率从 5.4 降至 2.9，并在多目标链任务上大幅提升成功率（Table 1）。

> **注意**：关于 InterMimic 和 MaskedMimic 的具体发表信息（作者/年份/会议），当前证据中未提供完整引用元数据，需手动核实。



InterPrior 采用三阶段训练范式，将大规模人-物交互（HOI）数据中的全参考模仿专家逐步转化为一个可泛化的目标条件生成控制器。图2给出了框架总览。

**阶段一：全参考专家训练（InterMimic+）**
首先在HOI运动捕捉数据上训练一个全参考模仿策略作为教师。该专家以当前人-物状态和完整未来参考轨迹为输入，通过PPO最大化复合奖励进行训练。奖励由跟踪奖励 $r_{\mathrm{track}}$、能量效率奖励 $r_{\mathrm{energy}}$、无参考手部奖励 $r_{\mathrm{h}}$ 和终止惩罚 $r_{\mathrm{ter}}$ 组成：
$$r_t = (r_{\mathrm{track}} \times r_{\mathrm{energy}} \times r_{\mathrm{h}}) + r_{\mathrm{ter}}$$
其中手部奖励 $r_{\mathrm{h}}$ 是 InterPrior 的关键设计——它不依赖参考轨迹中的手指动作，而是根据模拟状态中手指与物体的接触程度直接给予奖励，激励策略学会主动包裹物体。此外，训练中引入随机化、扰动和数据增强以扩展参考范围，使专家对初始化扰动具有更强的鲁棒性。

**阶段二：变分蒸馏**
将阶段一训练好的专家策略蒸馏为一个掩码条件变分策略。该策略的核心是一个潜变量模型，由三个网络组成：
- 先验网络 $p_{\psi}(z_t | \mathbf{x}_{t-\ell:t}, \mathcal{G}_t)$：仅根据历史状态和稀疏目标推断潜技能变量
- 编码器 $q_{\phi}(z_t | \mathbf{x}_t, \mathcal{G}_t, \mathbf{y}_{t:t+H}, \mathbf{y}_{t+L})$：训练时使用全参考未来信息引导潜变量学习
- 解码器 $f_{\theta}(\mathbf{a}_t | \mathbf{x}_{t-\ell:t}, z_t)$：根据历史状态和采样的潜变量输出动作

蒸馏总损失为：
$$\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ELBO}} + \lambda_{\mathrm{scale}} \mathcal{L}_{\mathrm{scale}} + \lambda_{\mathrm{tc}} \mathcal{L}_{\mathrm{tc}}$$
其中 $\mathcal{L}_{\mathrm{ELBO}}$ 为标准变分证据下界，$\mathcal{L}_{\mathrm{scale}}$ 强制先验均值位于单位球面上，$\mathcal{L}_{\mathrm{tc}}$ 为时间一致性损失。蒸馏后，采样得到的潜变量被投影到单位超球面（$z_t := z_t / \|z_t\|$），以提高推理时的鲁棒性。

**阶段三：强化学习后训练**
蒸馏策略虽然能重建自然运动，但在大规模HOI配置空间上泛化能力不足——这是本工作的核心瓶颈。为此，InterPrior 将后训练形式化为一个 in-betweening 任务：从随机采样的初始配置出发，追踪从数据集中随机抽取的单帧目标。后训练奖励为：
$$r_t^{\mathrm{PT}} = (r_{\mathrm{energy}} \times r_{\mathrm{h}}) + r_{\mathrm{goal}} + r_{\mathrm{ter}}$$
其中 $r_{\mathrm{goal}}$ 是稀疏成功信号，当当前状态与目标帧的掩码特征距离低于阈值 $\tau$ 时激活。同时，通过蒸馏正则化保留预训练知识，防止灾难性遗忘。

**输入输出流**
最终策略以观测向量 $\mathbf{x}_t$ 为输入，该向量聚合了人体运动学（根位置/朝向/速度）、物体运动学（位置/朝向/速度）以及交互状态（符号距离 $D_t$、二值接触 $C_t$）：
$$\mathbf{x}_t = \Big[ \underbrace{r_t^h, \theta_t^h, \dot{r}_t^h, \dot{\theta}_t^h}_{\mathrm{human}}, \underbrace{r_t^o, \theta_t^o, \dot{r}_t^o, \dot{\theta}_t^o}_{\mathrm{object}}, \underbrace{D_t, C_t}_{\mathrm{interaction}} \Big]$$
目标通过掩码残差编码 $\tilde{\mathbf{y}}_{t+k} = \mathbf{m}_{t+k} \odot \Delta(\mathbf{y}_{t+k}, \mathbf{x}_t)$ 注入策略，支持快照目标、轨迹目标和接触目标三种控制模式。策略输出为驱动物理仿真人体模型的关节动作。

**模块关系总结**
三个阶段形成递进关系：专家训练提供行为参考上限，变分蒸馏将全参考知识压缩为条件生成先验，RL后训练作为局部优化器扩展泛化边界。蒸馏为RL提供了自然行为初始化，而RL微调在保持行为自然性的同时使策略能够处理未见目标和失败恢复场景。

### 补充图表

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the proposed InterPrior framework. It consists of: (I) full-reference imitation expert training on large-scale human-object interaction data; (II) distillation of the expert into a variational policy with a structured latent space for skill embeddings; and (III) post-training of the variational policy to enhance generalization. Blue modules denote the final policy used at inference; green and red modules are training-only components, and red arrows denote supervision signals (rewards/losses)*

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/001_Figure_1.jpg]]
*Figure 1: InterPrior is a versatile generative controller instantiated as a goal-conditioned policy that controls a simulated humanoid to follow goal guidance and interact with objects in a physics-based simulator. Three core, composable capabilities enable pursuing (I) longhorizon snapshot goals, (II) trajectory goals, and (III) contact goals (Top). Yellow, blue, and red dots respectively denote human, object, and contact goals. It demonstrates failure recovery (Bottom Left) from unsuccessful grasps. InterPrior enables steering control from a human operator and can be applied to humanoid robot embodiments (Bottom Right). More demo videos are provided in the webpage*



### 3.1 观测与目标表示

策略的观测向量聚合了人、物及交互状态，构成多模态条件输入的基础：

$$
\mathbf{x}_t = \Big[ \underbrace{r_t^h, \theta_t^h, \dot{r}_t^h, \dot{\theta}_t^h}_{\mathrm{human}},  \underbrace{r_t^o, \theta_t^o, \dot{r}_t^o, \dot{\theta}_t^o}_{\mathrm{object}},  \underbrace{D_t, C_t}_{\mathrm{interaction}} \Big]
$$

其中 $r$ 表示位置、$\theta$ 表示姿态（旋转）、$\dot{r}$ 和 $\dot{\theta}$ 为对应速度；$D_t$ 为人-物表面的有符号距离，$C_t$ 为二元接触指示。目标通过掩码残差编码转化为策略可处理的形式：

$$
\tilde{\mathbf{y}}_{t+k} = \mathbf{m}_{t+k} \odot \Delta(\mathbf{y}_{t+k}, \mathbf{x}_t)
$$

$\mathbf{m}_{t+k}$ 为元素级掩码，$\Delta(\cdot,\cdot)$ 对旋转分量使用 log‑map 差异、对位置分量使用减法。这一设计使得同一策略可统一处理快照目标、轨迹目标和接触目标。

### 3.2 InterMimic+ 专家训练

第一阶段的专家策略通过 PPO 最大化复合奖励来学习稳健的全参考模仿：

$$
r_t = (r_{\mathrm{track}} \times r_{\mathrm{energy}} \times r_{\mathrm{h}}) + r_{\mathrm{ter}}
$$

核心改进在于引入无参考的**手部奖励** $r_{\mathrm{h}}$，激励手指基于当前模拟状态包裹物体，而非单纯跟踪参考手指姿态。终止惩罚 $r_{\mathrm{ter}}$ 在人体跌倒或状态偏差过大时触发。配合随机化、扰动和数据增强，InterMimic+ 相比原 InterMimic 在薄物体抓取等精细交互上显著提升了鲁棒性（见图 3）。

### 3.3 变分蒸馏：潜技能空间建模

第二阶段将专家策略蒸馏为掩码条件变分策略，核心是学习一个结构化的潜技能空间，使策略在稀疏目标条件下仍能生成多样且自然的运动。变分模型由三个组件构成：

$$
p_{\psi}(z_t | \mathbf{x}_{t-\ell : t}, \mathcal{G}_t) \quad q_{\phi}(z_t | \mathbf{x}_t, \mathcal{G}_t, \mathbf{y}_{t:t+H}, \mathbf{y}_{t+L}) \quad f_{\theta}(\mathbf{a}_t | \mathbf{x}_{t-\ell : t}, z_t)
$$

- **先验网络** $p_{\psi}$：仅基于历史观测和稀疏目标 $\mathcal{G}_t$ 推断潜变量分布，是推理时的唯一编码路径。
- **编码器** $q_{\phi}$：训练时额外引入全参考未来帧 $\mathbf{y}_{t:t+H}$ 和远帧 $\mathbf{y}_{t+L}$，提供更丰富的后验信息。
- **解码器** $f_{\theta}$：从潜变量 $z_t$ 和历史状态解码动作 $\mathbf{a}_t$。

蒸馏总损失为：

$$
\mathcal{L}_{\mathrm{total}} = \mathcal{L}_{\mathrm{ELBO}} + \lambda_{\mathrm{scale}} \mathcal{L}_{\mathrm{scale}} + \lambda_{\mathrm{tc}} \mathcal{L}_{\mathrm{tc}}
$$

$\mathcal{L}_{\mathrm{ELBO}}$ 为标准证据下界；$\mathcal{L}_{\mathrm{scale}}$ 为**尺度正则**，强制先验均值落在单位超球面上（采样后执行 $z_t := z_t / \|z_t\|$），提升潜空间鲁棒性；$\mathcal{L}_{\mathrm{tc}}$ 为**时间一致性损失**，约束相邻帧潜变量平滑过渡。消融实验表明，加入尺度损失和时间一致性损失后目标跟随准确度进一步提升（Table 1）。

### 3.4 强化学习后训练：泛化边界扩展

蒸馏策略在大规模 HOI 配置空间上泛化能力不足，第三阶段通过 RL 微调将其扩展为局部优化器。微调被形式化为 **in‑betweening 任务**：从随机初始构型出发，朝向从数据集中随机抽取的单帧目标运动。微调奖励为：

$$
r_t^{\mathrm{PT}} = (r_{\mathrm{energy}} \times r_{\mathrm{h}}) + r_{\mathrm{goal}} + r_{\mathrm{ter}}
$$

其中 $r_{\mathrm{goal}}$ 为稀疏成功信号，仅在当前状态与目标帧的掩码特征距离低于阈值 $\tau$ 时激活：

$$
r_{\mathrm{goal}} = \begin{cases} r_{\mathrm{succ}}, & \mathrm{if } \left\| m_{t+L} \odot \Delta(\tilde{y}_{t+L}, \mathbf{x}_t) \right\|_1 < \tau \\ 0, & \mathrm{otherwise} \end{cases}
$$

同时保留蒸馏正则化项以防止遗忘预训练知识。实验表明，RL 微调将 Contact 任务的失败率从 5.4 降至 2.9，并在多目标链任务上大幅提升成功率（Table 1），验证了“蒸馏提供行为先验初始化 + RL 作为局部优化器”这一核心洞察的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative comparison of same reference imitation between InterMimic [87] (top) and our InterMimic+ (bottom). InterMimic strictly follows the reference humanoid motion but fails to grasp the thin cloth stand when initialized with perturbations*



## 实验与关键发现

### 核心瓶颈与因果机制

InterPrior 面临的核心瓶颈在于：大规模人-物交互（HOI）演示数据无法覆盖所有可能的构型空间，导致纯蒸馏策略在未见目标及初始化上泛化能力不足。其因果调节机制为：在蒸馏得到的变分策略基础上进行强化学习微调，利用随机初始化与稀疏目标作为局部优化器，提升策略鲁棒性。核心洞见在于，蒸馏为策略提供了自然的行为先验初始化，而强化学习微调作为一种局部优化器，在保持行为自然性的同时扩展了策略的泛化边界，使其能够处理未见目标和失败恢复。

### 主实验结果

**目标条件任务评估。** Table 1 报告了在分布内目标条件任务上的量化结果。InterPrior 在 InterAct/OMOMO 数据集上的快照目标（Snapshot goals）任务中达到 **90.0%** 的成功率。该表格同时涵盖了轨迹目标（trajectory goals）和接触目标（contact goals）的评估，验证了策略对三类核心控制能力的支持（Figure 1）。

**全参照跟踪与泛化。** Table 2 展示了在 OMOMO 数据集上针对薄物体（thin objects）的全参照模仿任务结果。InterPrior 达到 **83.2%** 的成功率，相比基线 **InterMimic** 的 63.9% 提升了 **+19.3 个百分点**。在 HODome 数据集的新交互场景上，经过微调后的 InterPrior 达到 **72.4%** 的成功率，证明了方法对新对象和新交互技能的适应能力。

**零样本泛化定性结果。** Figure 5 展示了在 OMOMO 上训练的单一 InterPrior 模型，零样本泛化到 BEHAVE 和 HODome 数据集中未见对象和交互的定性结果。Figure 7 进一步对比了 InterMimic（全参照）、MaskedMimic 和 InterPrior 在 BEHAVE 数据集上对未见且不完美交互的处理能力——InterPrior 能够从不完美的数据中恢复并继续 rollout。

### 消融研究

Table 1 的消融研究揭示了以下关键结论：

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/008_Table_1.jpg]]
*Table 1: Quantitative evaluation and ablation study on in-distribution goal-conditioned tasks, including snapshot, trajectory, contact (Figure 1), plus out-of-distribution stress tests on challenging scenerio, such as long-horizon multi-goal chains and object lifting under random human initialization. For the random initialization, only the object is assigned a goal, thus the human error is omitted*

1. **专家质量的影响**：将原 InterMimic 专家替换为 InterMimic+ 专家后，成功率和泛化性均得到提升。Figure 3 的定性对比显示，InterMimic 严格跟随参照运动但在扰动初始化下无法抓取薄布架，而 InterMimic+ 通过引入形状奖励和扰动训练，显著改善了鲁棒性。

2. **潜变量正则化的贡献**：增加潜变量塑造损失（latent shaping loss）和时间一致性损失（tc loss）进一步提升了目标跟随的准确度。这些正则化项强制先验均值位于单位超球面上，并鼓励潜变量在时间上的平滑过渡。

3. **RL 微调的关键作用**：RL 微调将 Contact 任务的失败率从 5.4 降至 2.9，并在多目标链（Multi-Goal Chain）任务上大幅提升成功率。微调采用随机初始化和目标帧的 in-betweening 任务，同时通过蒸馏正则化保留预训练知识，有效扩展了策略的泛化边界。

### 失败模式与局限性

尽管 InterPrior 展现出强大的泛化能力，论文明确指出了以下失败模式和局限性：

- **数据覆盖依赖**：策略受限于训练数据的覆盖率和质量，高度损坏或未见的交互模式无法可靠恢复。
- **物理伪影**：在长序列 rollout 中可能出现物体穿透、脚部滑动或物体掉落等现象。这些伪影源于仿真器的物理近似和策略对精细接触动力学的建模不足。
- **灵巧操作缺失**：当前的接触和手部表示不支持精细的手指灵巧性或手持操作，限制了策略在需要精确手指控制场景中的表现。
- **训练流程复杂度**：三阶段训练流程（专家训练→变分蒸馏→RL 微调）增加了训练复杂度和超参数数量，增加了工程部署的难度。

### 实验设置公平性说明

所有基线方法在相同的目标规格下评估，包括相同的掩码采样策略和评估环境。仿真超参数（附表 A）和策略训练超参数（附表 B）沿用了先前工作的设置，确保了比较的公平性。

### 补充图表

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/009_Table_2.jpg]]
*Table 2: Quantitative evaluation of full-reference imitation on OMOMO with thin objects and initialization perturbations, and adaptation to novel object and interaction skills, evaluated before and after finetuning on new data. For novel interactions*

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/004_Figure_5.jpg]]
*Figure 5: Zero-shot qualitative results. A single InterPrior model trained from OMOMO [28] demonstrates generalization to unseen objects and interactions from BEHAVE [3] and HODome [95]*

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/005_Figure_6.jpg]]
*Figure 6: Qualitative results on sim-to-sim from IsaacGym [41] to MuJoCo [62] with object trajectory as condition, showing a sustained interaction involving box pickup, pushing, and kicking*

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/006_Figure_4.jpg]]
*Figure 4: Qualitative results on a multi-object task. The model input is shifted to the second object once the first object is released*

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/007_Figure_7.jpg]]
*Figure 7: Qualitative comparison between InterMimic [87] (left, full reference), MaskedMimic [58] (middle), and our InterPrior (right) on unseen and imperfect interactions from the BEHAVE [3] dataset. InterPrior can recover from data imperfection and continue the rollout*

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/013_Figure.jpg]]
*Figure: A. Additional qualitative comparisons with baseline method [58, 59] (Top). Our InterPrior shows higher success rate under the same task goal*

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/014_Figure.jpg]]
*Figure: C. Qualitative results of InterPrior following the targets generated by InterDiff (yellow and red dots). InterPrior adaptively completes the task without strictly adhering to the targets, using only sparse inputs of wrist, feet, and object target*

![[assets/figures/papers/paper_list_l992_https_arxiv_org_abs_2602_06035/figures/016_Figure.jpg]]
*Figure: B. Qualitative results given the same goal. Our framework produces multiple valid yet distinct interaction trajectories*



## 定位与知识库关联

### 前置工作与基线关系

InterPrior 建立在物理仿真人-物交互（HOI）策略学习的两条主线之上：**全参考模仿学习**与**蒸馏式目标条件策略**。

**全参考模仿基线。** 最直接的参照系是 **InterMimic**，该方法通过 PPO 强化学习训练一个专家策略，使其在 IsaacGym 物理仿真器中精确跟踪参考运动序列。InterMimic 的核心机制是乘积式奖励函数 $r = r_{\text{track}} \times r_{\text{energy}}$，将逐关节跟踪奖励与能量效率奖励相乘，迫使策略在保持运动自然性的同时精确复现参考动作。这一设计在标准 HOI 场景下表现良好，但其根本局限在于：策略对参考轨迹的依赖性过强，当面对薄物体（如布料架）或初始化扰动时，严格的运动跟踪反而导致抓取失败（见 Figure 3 定性对比）。InterPrior 将 InterMimic 作为教师策略，并在此基础上引入**无参考手部奖励** $r_h$ 和物理扰动增强，构建了更强的专家 **InterMimic+**。

**蒸馏式目标条件基线。** **MaskedMimic** 代表了另一条技术路线——将全参考专家蒸馏为仅依赖稀疏目标的条件策略。其核心思想是通过掩码机制，使策略学会从部分观测中重建完整运动。然而，MaskedMimic 的蒸馏过程本质上是在做行为克隆，缺少对策略泛化边界的主动扩展。在 BEHAVE 数据集上的未见交互测试中（Figure 7），MaskedMimic 在数据不完美时会出现运动退化，而 InterPrior 能够从退化中恢复并继续 rollout。

### 核心改进与差异机制

InterPrior 在蒸馏-微调范式上做出了三个关键改进，使其区别于前述基线：

**1. 结构化潜变量空间。** 与标准 VAE 蒸馏不同，InterPrior 在变分策略中引入了两项正则化设计：采样后将潜变量投影到单位超球面（$z_t := z_t / \|z_t\|$），以及通过尺度损失 $\mathcal{L}_{\text{scale}}$ 强制先验均值保持在单位球上。这解决了标准 VAE 在稀疏目标条件下潜变量漂移的问题，使潜空间成为更稳定的技能嵌入流形。消融实验（Table 1）表明，加入潜变量塑造损失和时间一致性损失 $\mathcal{L}_{\text{tc}}$ 后，目标跟随准确度进一步提升。

**2. 多模态目标条件。** InterPrior 统一了三种目标类型：快照目标（单帧人体-物体状态）、轨迹目标（多帧序列）和接触目标（指定身体部位与物体的接触关系）。这种统一通过掩码残差编码 $\tilde{\mathbf{y}}_{t+k} = \mathbf{m}_{t+k} \odot \Delta(\mathbf{y}_{t+k}, \mathbf{x}_t)$ 实现，其中 $\Delta$ 运算对旋转使用 log-map、对位置使用减法。MaskedMimic 仅支持快照和轨迹目标，缺少接触条件，这限制了其在精细交互场景中的适用性。

**3. 强化学习后训练。** 这是 InterPrior 与纯蒸馏方法最本质的区别。蒸馏得到的变分策略虽然能重建运动，但面对大规模 HOI 配置空间时泛化不可靠——这是本文识别的核心瓶颈。InterPrior 将后训练形式化为一个 in-betweening 任务：从随机初始配置出发，朝向数据集中随机抽取的单帧目标进行跟踪。后训练奖励 $r_t^{\text{PT}} = (r_{\text{energy}} \times r_h) + r_{\text{goal}} + r_{\text{ter}}$ 中，$r_{\text{goal}}$ 是一个稀疏成功信号，仅在当前状态与目标的掩码特征距离低于阈值 $\tau$ 时激活。这种稀疏奖励设计避免了密集跟踪奖励对预训练知识的覆盖，同时通过蒸馏正则化防止灾难性遗忘。

### 适用边界与局限

InterPrior 的能力边界由训练数据的覆盖率和物理仿真的精度共同划定：

**数据依赖性。** 策略的泛化受限于训练数据的分布。尽管 RL 后训练扩展了策略在未见目标和初始化上的能力，但高度损坏或完全未见的交互模式无法可靠恢复。在 HODome 数据集上的微调实验（Table 2）表明，经过新数据微调后成功率可达 72.4%，但零样本泛化仍存在明显差距。

**物理仿真伪影。** 在长序列 rollout 中，策略可能出现物体穿透、脚部滑动或物体掉落等现象。这些伪影根源于 IsaacGym 仿真器的接触模型精度限制，而非策略本身的设计缺陷。Figure 6 展示了 sim-to-sim 迁移到 MuJoCo 的结果，暗示部分伪影可通过更精确的仿真器缓解。

**灵巧性缺失。** 当前的接触和手部表示不支持手指级灵巧操作或手持操作。手部奖励 $r_h$ 仅激励手指包裹物体，而非精确的手指关节协调。这意味着 InterPrior 适用于抓取、搬运、推拉等粗粒度交互，但不适用于需要精细手指控制的场景（如旋钮操作、工具使用）。

**训练流程复杂度。** 三阶段训练流程（专家训练→变分蒸馏→RL 后训练）增加了超参数调优的负担。每个阶段都有独立的奖励权重、学习率和训练步数，阶段间的衔接需要仔细的检查点选择和正则化强度调整。

### 开放问题

1. **非刚性对象扩展。** 当前方法仅处理刚体对象。扩展到布料、绳索、液体等非刚性对象需要重新设计观测表示和接触模型，且数据采集难度显著增加。

2. **物理伪影消除。** 浅层穿透和脚部滑动是物理仿真 HOI 的共性问题。可能的解决方向包括：引入更精细的接触模型（如基于惩罚力的软接触）、在后训练中增加穿透惩罚项、或采用域随机化增强对仿真误差的鲁棒性。

3. **手指级灵巧操作。** 整合手指级灵巧操作模型需要高维动作空间和更精细的奖励设计。可能的路径是将 InterPrior 的潜技能空间与灵巧操作策略（如基于教师-学生蒸馏的灵巧抓取方法）进行级联或联合训练。

4. **训练流程简化。** 能否将三阶段流程统一为端到端训练是一个开放问题。潜在方向包括：将蒸馏和 RL 后训练合并为联合优化目标，或使用离线 RL 直接在交互数据上学习目标条件策略，从而跳过专家训练阶段。



## 原文 PDF

![[paperPDFs/CVPR_2026/InterPrior_Scaling_Generative_Control_for_Physics_Based_Human_Object_Interactions.pdf]]
