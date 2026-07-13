---
title: "Interactive Character Control with Auto-Regressive Motion Diffusion Models"
type: paper
paper_level: A
venue: SIGGRAPH
year: 2024
pdf_ref: paperPDFs/SIGGRAPH_2024/Interactive_Character_Control_with_Auto_Regressive_Motion_Diffusion_Models.pdf
code_link: null
project_link: https://yi-shi94.github.io/amdm_page/
aliases:
- MARMDM
- ICCARMDM
tags:
- SIGGRAPH_2024
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "将扩散模型改造为自回归形式并采用极少量去噪步骤（40步）和轻量级MLP网络，使其在实时性下生成高质量、多样化的运动。"
primary_logic: "将扩散模型的自回归设计与任务导向采样、修补和分层强化学习相结合，可构建一个轻量、高保真的实时运动生成框架，无需针对每个下游任务重新训练即可生成多样化、符合控制目标的运动。"
claims:
- "A-MDM逐帧生成下一帧，仅需少于50个去噪步数，实现实时交互。"
- "网络为轻量MLP（10层，1024维），足以生成多样化运动。"
- "A-MDM在HumanML3D和AMASS上的FID、ADE及多样性指标优于VAE-based自回归模型MVAE和HuMoR。"
- "A-MDM可通过修补和分层强化学习进行控制，无需微调。"
---

# Interactive Character Control with Auto-Regressive Motion Diffusion Models

> [!tip] 核心洞察
> 将扩散模型的自回归设计与任务导向采样、修补和分层强化学习相结合，可构建一个轻量、高保真的实时运动生成框架，无需针对每个下游任务重新训练即可生成多样化、符合控制目标的运动。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 基于自回归运动扩散模型的交互式角色控制 |
| 英文题名 | Interactive Character Control with Auto-Regressive Motion Diffusion Models |
| 会议/期刊 | SIGGRAPH 2024 |
| Links | [paper](https://arxiv.org/abs/2306.00416) · [Project](https://yi-shi94.github.io/amdm_page/) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | A-MDM (Auto-Regressive Motion Diffusion Model) |
| Dataset | HumanML3D, LaFAN1 |

> [!tip] 效果简介
> - HumanML3D 上，FID (↓) 为 1.7435 ± 0.0813，对比 MVAE: 11.2393 ± 0.1607，变化 减少9.4958（更低更好）。
> - LaFAN1 上，Foot Skating (FS↓) 为 1.99，对比 NSM: 2.25，变化 降低0.26。

## 概要

实时交互式角色控制面临一个核心瓶颈：现有的运动扩散模型（如MDM、GMD）采用时空模型一次性生成整个运动序列，无法满足实时交互对逐帧响应的需求；而传统的自回归模型（如基于VAE的MVAE和HuMoR）在生成长序列时容易产生漂移和运动质量下降。本文提出的**A-MDM（Auto-Regressive Motion Diffusion Model）**将扩散模型改造为自回归形式，仅需极少量去噪步骤（40步）和轻量级MLP网络（10层，1024维），即可在实时条件下生成高质量、多样化的运动序列。

核心思路在于：将扩散模型的自回归设计与任务导向采样、空间/时间修补以及分层强化学习相结合，构建一个轻量、高保真的实时运动生成框架。该框架无需针对每个下游任务重新训练或微调基础模型，即可通过不同的控制策略生成符合多样化控制目标的运动。

主要结果方面，A-MDM在HumanML3D数据集上的FID达到1.74，相比MVAE的11.24有显著提升（Table 5）；在LaFAN1上的足部滑动指标（FS）为1.99，优于NSM的2.25（Table 6）。消融实验表明，40个扩散步骤在运动质量和多样性之间达到了最佳平衡，推理时间约为20.96ms，满足实时交互需求。



角色动画的实时交互控制是计算机图形学中的核心挑战，其目标是根据用户输入或任务目标，实时生成高质量、多样化的角色运动序列。这一任务面临双重约束：一方面需要运动具有自然性和物理合理性，另一方面必须满足毫秒级的实时推理延迟，以支持游戏、虚拟现实等交互式应用。

现有方法可大致分为两类。第一类是**时空扩散模型**，如 **MDM** (Tevet et al., ICLR 2023) 和 **GMD** (Karunratanakul et al., ICCV 2023)，它们将整个运动序列视为一个时空单元，通过扩散模型一次性生成完整序列。这类模型在运动质量和多样性上表现优异，但其“全序列一次性生成”的范式从根本上无法满足实时交互需求——用户无法在序列生成过程中动态插入新的控制信号。第二类是**基于VAE的自回归模型**，如 **MVAE** (Ling et al., ACM Trans. Graph. 2020) 和 **HuMoR** (Rempe et al., ICCV 2021)，它们逐帧预测下一帧运动，天然适合交互场景。然而，这类模型在生成长序列时存在严重的**漂移问题**：误差逐帧累积，导致运动质量迅速退化，且生成的运动多样性不足。

**核心瓶颈**在于：时空扩散模型提供了高质量生成能力但缺乏实时交互性，而自回归VAE模型支持逐帧交互但牺牲了生成质量。是否存在一种范式，能够同时继承扩散模型的高保真生成能力和自回归框架的实时交互优势？

本文的动机正是弥合这一缺口。作者提出 **A-MDM（Auto-Regressive Motion Diffusion Model）**，将扩散模型改造为自回归形式：以极少量去噪步骤（仅40步）和轻量级MLP网络，在实时性约束下逐帧生成高质量、多样化的运动。其核心洞察是：将扩散模型的自回归设计与任务导向采样、空间/时间修补、分层强化学习等控制策略相结合，可以构建一个轻量、高保真的实时运动生成框架，且无需针对每个下游任务重新训练模型。



## 核心方法与创新机理

A-MDM 的核心创新在于将扩散模型改造为**自回归生成范式**，使其能够在极低延迟下实时生成高质量运动，同时通过多种免训练的控制策略适配不同交互任务。相比于现有方案，其关键突破体现在以下四个维度的范式转变：

### 1. 生成范式：从时空一次性生成到自回归逐帧预测

现有运动扩散模型（如 **MDM** (Tevet et al., ICLR 2023) 和 **GMD** (Karunratanakul et al., ICCV 2023)）采用时空模型一次性生成整个运动序列，这从根本上无法满足实时交互对逐帧响应的需求。而传统的自回归模型（如 **MVAE** (Ling et al., ACM Trans. Graph. 2020) 和 **HuMoR** (Rempe et al., ICCV 2021)）基于 VAE 架构，在生成长序列时容易出现漂移和运动质量退化。

A-MDM 将扩散模型重新设计为自回归形式：给定前一帧的角色状态 $x_{f-1}$，模型对当前帧 $x_f$ 的条件分布进行建模，逐帧生成后续运动。这一设计使得模型天然适配交互式控制场景——每生成一帧即可根据用户输入实时调整下一帧的生成方向。

### 2. 模型架构：从 Transformer/VAE 到轻量 MLP

与 MDM 使用的 Transformer 架构或 MVAE/HuMoR 的 VAE 架构不同，A-MDM 采用了极为精简的网络设计：**10 层全连接网络，每层 1024 个隐藏单元，使用 SiLU 激活函数和层归一化**。这一轻量 MLP 架构是 A-MDM 实现实时性能的关键——它证明了在自回归扩散框架下，无需复杂网络即可生成多样化的高质量运动。

### 3. 扩散步数：从 1000 步到 40 步

标准 DDPM 需要约 1000 个去噪步骤才能生成高质量样本，这完全无法满足实时交互的延迟要求。A-MDM 将去噪步数压缩至 **仅 40 步**，在运动质量和推理速度之间取得了关键平衡。消融实验表明（Table 3, Table 4），在 100STYLE 和 LaFAN1 数据集上，40 步配置在 APD（运动多样性）和 ADE（距离误差）上均达到最优，同时推理时间仅约 20.96ms，满足实时交互需求。

### 4. 控制方式：从无控制/任务特定训练到免训练多策略控制

现有方法通常要么缺乏控制能力，要么需要为每个下游任务单独训练特定策略。A-MDM 提出了**三种免训练的通用控制策略**，可在不修改基础模型的情况下适配不同任务：

- **任务导向采样**：生成多个候选轨迹，根据用户定义的评分函数选择最优者，适用于目标到达等简单任务。
- **空间与时间修补**：通过在每个去噪步后直接替换用户指定的关节特征（空间修补），或通过调整关键帧附近帧的去噪初始化步数（时间修补），实现精确的关节轨迹控制和关键帧间插值。
- **分层强化学习控制器**：训练一个高层策略来预测去噪过程中的残差向量，引导基础 A-MDM 完成需要精确控制的复杂任务（如摇杆控制和路径跟随），弥补了任务导向采样在精度导向任务中的不足。

这四种范式转变共同构成了 A-MDM 的核心创新：**一个轻量、实时、通用可控的自回归运动扩散框架**，无需为每个新任务重新训练即可生成多样化且符合控制目标的高保真运动。



A-MDM 的整体设计围绕一个核心矛盾展开：**如何在保持扩散模型生成质量与多样性的同时，实现满足实时交互需求的逐帧推理速度**。为此，该框架将去噪扩散概率模型（DDPM）改造为自回归生成范式，并围绕这一基础模型构建了多层控制策略，形成一个“生成-控制”解耦的模块化 pipeline。

### 基础生成模型：自回归运动扩散

基础模块是一个条件扩散模型，其输入为前一帧的角色状态 $x_{f-1}$，输出为当前帧状态 $x_f$ 的条件分布。训练遵循标准 DDPM 流程：前向过程逐步向真实运动帧 $x_f^0$ 注入高斯噪声，反向过程则训练一个去噪网络 $\mathfrak{p}_\theta$ 从噪声中恢复原始信号。其单步前向加噪过程为：

$$q(x_f^t | x_f^{t-1}) = \mathcal{N}(x_f^t; \sqrt{1 - \beta^t} x_f^{t-1}, \beta^t I)$$

训练损失采用简化后的 MSE 形式：

$$L_t^{\text{simple}}(x) = \mathbb{E}_{t \sim [1:T], x_f^0, \epsilon_f^t} \left\| \epsilon_f^t - \mathfrak{p}_\theta(x_{f-1}, x_f^t, e^t) \right\|_2$$

其中 $\epsilon_f^t$ 为真实噪声，$e^t$ 为扩散步数嵌入。该损失驱使网络学会从噪声观测中预测噪声分量，从而在推理时通过迭代去噪生成下一帧。

推理时，模型以自回归方式运行：给定初始姿态，生成第一帧；随后将生成的帧作为下一时刻的条件输入，逐帧滚动生成任意长度的运动序列。这一设计的关键瓶颈在于：**自回归模型在长序列生成中易产生误差累积导致的漂移**。为缓解该问题，A-MDM 在训练中采用了**调度采样**策略——以一定概率使用模型自身的预测结果而非真实数据作为下一帧的条件输入，使模型在训练阶段即暴露于自回归推理时的误差分布，从而提升长序列生成的稳定性。

### 轻量化架构设计

为实现实时推理，A-MDM 在网络架构上做出了显著简化。去噪网络 $\mathfrak{p}_\theta$ 采用一个**仅含 10 层全连接层的轻量 MLP**，每层包含 1024 个隐藏单元，使用 SiLU 激活函数后接 Layer Normalization。这与时空扩散模型（如 **MDM**，Tevet et al., ICLR 2023）使用的 Transformer 架构形成鲜明对比，也与 VAE-based 自回归模型（如 **MVAE**，Ling et al., ACM Trans. Graph. 2020；**HuMoR**，Rempe et al., ICCV 2021）的编解码结构不同。

更关键的是，A-MDM 将扩散步数从 DDPM 默认的 1000 步大幅压缩至 **仅 40 步**。消融实验表明，40 步在运动质量与多样性之间取得了最优平衡——在 100STYLE 数据集上，40 步的 APD 为 102.52，ADE 为 10.36 cm；在 LaFAN1 上，40 步获得最佳 ADE 和 APD，且单帧推理时间约为 20.96 ms。步数过少会导致生成质量下降，过多则损害实时性，40 步恰好落在这个帕累托前沿的拐点。

### 控制策略层：模块化任务适配

基础生成模型训练完成后，A-MDM 无需针对下游任务重新训练或微调，而是通过三种互补的控制策略实现任务适配，形成“一次训练、多策略复用”的 pipeline：

1. **任务导向采样**：在推理时生成 $N$ 条候选轨迹，根据用户定义的评分函数（如距目标点的距离）进行排序，选择最优轨迹执行。该方法适用于目标到达等简单运动任务，但在需要精确跟踪的操纵杆控制或路径跟随任务中存在短视性问题。

2. **空间与时间修补**：空间修补通过在每一步去噪后使用二值掩码 $m_f$ 将用户指定特征替换为目标值——$\hat{x}_f^t = (1 - m_f) \odot x_f^t + m_f \odot \tilde{x}_f^t$——实现关节轨迹的精确控制。时间修补则用于关键帧插值，通过调整各帧的去噪初始化步数 $t_0 = (1 - \frac{f}{N}) t_{\max}$，使越靠近目标关键帧的生成帧越接近于目标姿态，从而产生平滑过渡。

3. **分层强化学习控制器**：针对需要精确、持续控制的任务（如路径跟踪），A-MDM 引入一个高层 RL 策略，该策略在每个去噪步预测残差向量 $a_f^t$ 来引导基础模型的去噪过程。策略的优化目标为期望回报：

$$J_{RL}(\pi) = \mathbb{E}_{\tau \sim p(\tau|\pi)} \left[ \sum_{f=0}^{\infty} \gamma^f r(s_f, a_f) \right]$$

这种分层设计将运动先验（基础模型）与任务策略（RL 控制器）解耦，使同一基础模型可服务于不同任务目标。

### 输入输出流

整个 pipeline 的数据流可概括为：**初始姿态 → 自回归扩散生成 → 控制策略介入 → 角色状态序列**。具体而言，用户提供初始角色姿态作为条件，基础 A-MDM 在 40 步去噪后生成下一帧；控制策略根据任务需求对生成过程进行干预（评分选择、特征替换或残差引导）；生成的帧作为新的条件反馈至下一轮生成，循环往复直至输出完整运动序列。该流程的模块化设计确保了各组件可独立替换或升级，例如未来可将基础模型替换为一致性模型以进一步降低推理延迟。

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2306_00416/figures/001_Figure_1.jpg]]
*Figure 1: We present Auto-Regressive Motion Diffusion Model (A-MDM), a framework for generating high-fidelity kinematic motion sequences. Once trained, A-MDM can be reused to perform new tasks through different control strategies, such as inpainting (upper right, and lower left), and hierarchical control via reinforcement learning (lower right)*



A-MDM 将标准扩散模型改造为自回归形式，逐帧预测下一帧运动，并辅以调度采样、修补、任务导向采样和分层强化学习等控制模块。以下逐一说明各模块的设计逻辑与核心公式。

### 3.1 自回归运动扩散模型（基础生成器）

A-MDM 的基础模块是一个条件扩散模型：给定第 $f-1$ 帧的角色状态 $x_{f-1}$，模型对第 $f$ 帧的状态 $x_f$ 建模分布 $p(x_f \mid x_{f-1})$。训练遵循 DDPM 范式，包含前向加噪和反向去噪两个过程。

**前向扩散。** 从真实数据 $x_f^0$ 开始，逐步注入高斯噪声，共 $T$ 步。单步加噪过程为：

$$q(x_f^t \mid x_f^{t-1}) = \mathcal{N}\big(x_f^t; \sqrt{1 - \beta^t}\, x_f^{t-1}, \beta^t I\big)$$

其中 $\beta^t$ 为噪声调度参数，$t \in [1, T]$。完整的马尔可夫链为 $q(x_f^{1:T} \mid x_f^0) = \prod_{t=1}^T q(x_f^t \mid x_f^{t-1})$。

**反向去噪。** 模型学习一个去噪网络 $\mathfrak{p}_\theta$，以 $x_{f-1}$ 为条件，从纯噪声 $x_f^T \sim \mathcal{N}(0, I)$ 逐步恢复 $x_f^0$。训练目标为简化后的 MSE 损失：

$$L_t^{\text{simple}}(x) = \mathbb{E}_{t \sim [1:T],\, x_f^0,\, \epsilon_f^t}\Big[ \|\epsilon_f^t - \mathfrak{p}_\theta(x_{f-1}, x_f^t, e^t)\|_2 \Big]$$

其中 $\epsilon_f^t$ 是第 $t$ 步注入的真实噪声，$e^t$ 为扩散步数的嵌入编码。网络直接预测噪声而非数据本身。

### 3.2 调度采样（Scheduled Sampling）

自回归模型在推理时以自身生成的前一帧作为输入，训练时若始终使用真实帧（Teacher Forcing），会导致训练-推理分布不匹配，产生漂移。A-MDM 采用调度采样中的 Student Forcing 策略：训练时以一定概率 $p$ 使用模型上一帧的重建结果 $\hat{x}_{f-1}^t$ 替代真实帧 $x_{f-1}$，概率 $p$ 随训练进程递增。损失函数形式上与公式 (3) 相同，但条件帧的来源在真实帧与重建帧之间切换。

### 3.2.1 轻量网络架构

去噪网络 $\mathfrak{p}_\theta$ 采用极轻量的 MLP 设计：10 层全连接层，每层 1024 个隐藏单元，激活函数为 SiLU，每层后接 Layer Normalization。这一设计使得单帧去噪仅需 40 步即可完成，推理延迟约 20.96 ms（LaFAN1 数据集），满足实时交互需求。

### 4.2 任务导向采样（Task-Oriented Sampling）

对于目标到达等简单任务，A-MDM 无需额外训练。模块从当前状态出发，并行生成 $K$ 条候选轨迹，每条轨迹自回归生成若干帧。随后按用户定义的评分函数（如到目标点的距离）对候选轨迹排序，选择最优者执行。该模块的短视性使其在需要精确控制的路径跟随任务上表现受限。

### 4.3 空间修补与时间修补

**空间修补（Spatial Inpainting）。** 用户指定部分关节轨迹（如头部和根关节位置），模型在去噪的每一步将指定分量强制替换为用户目标值，其余维度由扩散模型自由生成。更新规则为：

$$\hat{x}_f^t = (1 - m_f) \odot x_f^t + m_f \odot \tilde{x}_f^t$$

其中 $m_f$ 为二值掩码，$\tilde{x}_f^t$ 为用户指定的目标特征，$\odot$ 表示逐元素乘积。该操作在每个去噪步后执行，无需微调模型。

**时间修补（Temporal Inpainting / 关键帧插值）。** 给定起始帧和目标关键帧，模型生成中间过渡帧。为使生成帧平滑趋近目标帧，第 $f$ 帧的去噪过程从不同的扩散步数初始化：

$$t_0 = \left(1 - \frac{f}{N}\right) t_{\max}$$

其中 $N$ 为过渡总帧数，$t_{\max}$ 为最大扩散步数。越靠近目标关键帧的帧，去噪起始步数越小，从而更紧密地贴合目标帧。

### 5.1 分层强化学习控制器

对于修补和任务导向采样难以处理的复杂控制任务（如精确路径跟随），A-MDM 引入分层强化学习策略。高层控制器 $\pi$ 在每个去噪步 $t$ 预测一个残差向量 $a_f^t$，叠加到当前去噪结果 $\hat{x}_f^t$ 上，以引导去噪过程朝向任务目标。策略优化目标为期望回报：

$$J_{RL}(\pi) = \mathbb{E}_{\tau \sim p(\tau \mid \pi)} \left[ \sum_{f=0}^{\infty} \gamma^f r(s_f, a_f) \right]$$

其中 $\tau$ 为轨迹，$\gamma$ 为折扣因子，$r(s_f, a_f)$ 为任务相关的即时奖励。低层基础扩散模型保持冻结，仅高层控制器被训练，从而在新任务上复用已学到的运动先验。



## 实验与关键发现

### 生成质量与多样性主结果

A-MDM 在多个基准数据集上对运动生成质量、多样性和泛化能力进行了系统评估，并与现有的自回归运动模型进行了对比。

**Table 1** 展示了在 AMASS、100STYLE 和 LaFAN1 三个数据集上的定量比较结果。A-MDM 在平均距离误差（ADE）和平均成对距离（APD）两个核心指标上均优于基于 VAE 的自回归模型 **MVAE** (Ling et al., ACM Trans. Graph. 2020) 和 **HuMoR** (Rempe et al., ICCV 2021)。具体而言，在 100STYLE 数据集上，A-MDM 的 ADE 为 10.36 cm，显著低于 MVAE 和 HuMoR；APD 达到 102.52，表明其生成的运动具有更高的多样性。在 LaFAN1 数据集上，A-MDM 同样在 ADE 和 APD 上取得最优结果。值得注意的是，A-MDM 仅使用 40 个扩散步骤即可实现上述性能，而传统 DDPM 通常需要 1000 步，这为其实现实时交互奠定了基础。

**Table 2** 进一步评估了模型的泛化能力——从数据集中运动片段的最后一帧出发，生成延续运动。A-MDM 在所有三个数据集上的 APD 均显著高于 MVAE 和 HuMoR，同时保持较低的足部滑动（Foot Skating）和骨骼长度误差（Bone Length Error），说明其生成的运动不仅多样，而且物理合理性更好。

在更大规模的 **HumanML3D** 数据集上（**Table 5**），A-MDM 与生成式自回归模型和时空扩散模型进行了全面比较。A-MDM 的 FID 达到 **1.7435 ± 0.0813**，远低于 MVAE 的 11.2393 ± 0.1607，降幅高达 **9.4958**。在多样性指标（Diversity）上，A-MDM 为 11.0967 ± 0.1088，同样优于 MVAE 的 8.0373 ± 0.0708。与时空扩散模型 **MDM** (Tevet et al., ICLR 2023) 相比，A-MDM 的 FID 略高（1.7435 vs. 0.5440），但需注意 MDM 一次性生成整个序列，不适合实时交互场景；A-MDM 以轻量级架构和极低推理延迟实现了可竞争的质量。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2306_00416/figures/020_Table_5.jpg]]
*Table 5: Comparison between generative auto-regressive models and spacetime models on HumanML3D [Guo et al. 2022]*

**Table 6** 将 A-MDM 与非生成式自回归模型 **NSM** (Starke et al., ACM Trans. Graph. 2019) 在 LaFAN1 上进行了对比。A-MDM 的足部滑动（FS）为 **1.99 cm**，低于 NSM 的 2.25 cm（降低 0.26 cm）；穿透指标（Penetration）为 0.07 cm，也优于 NSM 的 0.13 cm。

### 扩散步数消融实验

扩散步数是平衡生成质量与推理速度的关键超参数。**Table 3** 和 **Table 4** 分别展示了在 100STYLE 和 LaFAN1 数据集上不同扩散步数的消融结果。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2306_00416/figures/011_Table_3.jpg]]
*Table 3: Comparison of A-MDM with different number of diffusion steps on 100STYLE. (unit:cm)*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2306_00416/figures/013_Table_4.jpg]]
*Table 4: Comparison of A-MDM with different numbers of diffusion steps on the full LaFAN1, excluding environment interaction motions. Distance error units are measured in cm*

在 100STYLE 上（**Table 3**），随着扩散步数从 20 增加到 80，ADE 从 14.35 cm 先降至 10.36 cm（40 步），随后在 80 步时略微回升至 10.89 cm；APD 则从 94.08 持续上升至 104.60。**40 个扩散步骤实现了运动质量和多样性的最佳平衡**（APD 102.52, ADE 10.36 cm），同时推理时间仅约 20.96 ms，满足实时交互需求。

在 LaFAN1 上（**Table 4**），40 步同样获得最佳 ADE 和 APD。进一步增加步数并未带来显著的质量提升，反而增加了推理延迟。这一消融实验充分验证了 A-MDM 在极低扩散步数下即可收敛到高质量生成结果的设计优势。

### 控制策略的定性分析

A-MDM 通过任务导向采样、空间修补和时间修补三种策略，在不进行任何微调的情况下实现了多样化的运动控制。

**任务导向采样**（Section 4.2, **Fig. 10**）通过生成候选轨迹池并根据用户定义的目标函数评分，选择最优轨迹。与 HuMoR 相比，A-MDM 生成的轨迹更直接、步数更少，能够高效完成目标到达任务。然而，该方法存在短视性（myopic）局限——在需要精确控制的操纵杆跟随和路径跟随任务中表现不佳，难以紧密贴合用户指定的指令。

**空间修补**（Section 4.3, **Fig. 7**）允许用户指定特定关节（如头部和根关节）的期望轨迹，A-MDM 在每个去噪步骤后通过二元掩码替换对应特征分量，生成符合约束的全身运动。该方法能精确匹配用户指定的轨迹，但在约束不自然时容易产生足部滑动和抖动。

**时间修补/关键帧插值**（Section 4.3, **Fig. 5, Fig. 6, Fig. 9**）通过在关键帧之间动态调整去噪初始化步数——靠近关键帧的帧从更晚的去噪步数开始——生成自然流畅的过渡运动。A-MDM 能够在实时条件下为不同目标帧生成自然过渡，无需额外训练。

### 分层强化学习控制

对于需要长期规划和精确执行的任务，A-MDM 引入了分层强化学习控制器（Section 5, **Fig. 8**）。高层策略预测残差向量引导基础扩散模型的去噪过程，使其生成符合任务目标的运动。**Fig. 11** 的学习曲线显示，A-MDM 在目标到达任务上的回报显著高于其他分层模型。**Fig. 12** 展示了分层控制器从相同初始状态出发到达固定目标时生成多样化轨迹的能力。与修补法相比（**Fig. 13**），分层控制器在轨迹跟踪时可以适当偏离目标轨迹以产生更自然的运动，而修补法则精确匹配用户轨迹但可能牺牲自然度。

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2306_00416/figures/015_Figure_13.jpg]]
*Figure 13: (c) Hierarchical Control Fig. 13. Character trajectory (in white) from inpainting (b) and hierarchical control(c) when following a user-specified circular trajectory (in red). The trajectory of inpainting matches user’s target trajectory exactly, while the hierarchical controller can deviate from the target trajectory as needed in order to produce more natural motions*

### 失败模式与局限性

尽管 A-MDM 在生成质量和控制灵活性上表现优异，论文明确指出了以下失败模式：

1. **非自然控制下的伪影**：当用户指定的控制约束不自然或物理不可行时，A-MDM 容易产生足部滑动和抖动，这是自回归模型在强约束条件下的共性挑战。
2. **极端情况下的不稳定**：自回归扩散模型在极端条件下偶尔会出现不稳定行为和生成失败，可能与误差累积有关。
3. **单帧预测的局限**：当前模型仅基于前一帧预测下一帧，可能牺牲部分时间一致性。扩展为多帧预测可能有益于处理更复杂的运动模式。
4. **任务导向采样的短视性**：基于候选评分的任务导向采样缺乏长期规划能力，在需要精确控制的操纵杆跟随等任务中表现不足，分层强化学习虽能缓解此问题，但需要针对每个任务单独训练高层策略。

### 关键图表结论汇总

| 图表 | 核心结论 |
|------|----------|
| **Table 1** | A-MDM 在 AMASS/100STYLE/LaFAN1 上的 ADE 和 APD 均优于 VAE-based 自回归模型 MVAE 和 HuMoR |
| **Table 2** | A-MDM 在泛化能力上显著优于基线，生成运动更多样且物理合理性更好 |
| **Table 3/4** | 40 个扩散步骤是质量与速度的最佳平衡点，推理时间约 20.96 ms |
| **Table 5** | 在 HumanML3D 上 FID 达 1.74，远超 MVAE（11.24），接近时空模型 MDM（0.54）但满足实时性 |
| **Table 6** | 足部滑动（1.99 cm）和穿透（0.07 cm）均优于非生成式模型 NSM |
| **Fig. 10** | 任务导向采样生成的轨迹比 HuMoR 更直接高效 |
| **Fig. 11** | 分层强化学习控制器在目标到达任务上学习效率更高，回报显著优于其他分层模型 |
| **Fig. 13** | 修补法精确匹配轨迹，分层控制器可适当偏离以产生更自然运动 |

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2306_00416/figures/014_Figure_10.jpg]]
*Figure 10: (b) A-MDM Fig. 10. Task-oriented sampling using HuMoR (Left) vs. A-MDM (Right). The trajectories of A-MDM are more direct and take fewer steps. Results are generated using models trained on 100STYLE*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2306_00416/figures/009_Table_1.jpg]]
*Table 1: Comparisons on AMASS, 100STYLE and LaFAN1. 50 motion sequences are generated starting at fixed initial states. Each motion is 60 frames long when evaluating ADE and 150 frames long for calculating APD. (unit: cm)*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2306_00416/figures/010_Table_2.jpg]]
*Table 2: To evaluate the models’ generalization capabilities when generating new motions not in the dataset, we use the models to generate continuation motions starting at the last frame of motion clips in the dataset. We compare the models on the AMASS, 100STYLE, and LaFAN1 datasets. (unit: cm)*

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2306_00416/figures/019_Table_6.jpg]]
*Table 6: Comparison between NSM and A-MDM. (unit: cm)*

### 补充图表

![[assets/figures/papers/paper_list_l11_https_arxiv_org_abs_2306_00416/figures/016_Figure.jpg]]
*Figure: (a) LaFAN1 (b) 100STYLE*



## 定位与知识库关联

### 1. 关键基线关系

A-MDM 的方法设计源于对两类现有范式的不足的回应：**时空扩散模型**和**传统自回归模型**。

*   **vs. 时空扩散模型**：**MDM** (Tevet et al., ICLR 2023) 和 **GMD** (Karunratanakul et al., ICCV 2023) 等模型将运动序列视为一个时空块，一次性生成整个序列。这类方法虽然生成质量高，但无法满足实时交互应用对逐帧生成和无限长序列的需求。A-MDM 的核心改变是将生成范式从“一次性生成整个序列”转变为“自回归逐帧生成”（Section 3），从而天然地适应了交互式控制场景。

*   **vs. VAE-based 自回归模型**：**MVAE** (Ling et al., ACM Trans. Graph. 2020) 和 **HuMoR** (Rempe et al., ICCV 2021) 等基于 VAE 的自回归模型是 A-MDM 最直接的比较对象。这类模型同样采用逐帧生成，但在生成长序列时容易产生漂移和低质量运动。A-MDM 的因果性改进在于将生成模型从“VAE”替换为“扩散模型”，并配合极少量去噪步骤（40步）和轻量级 MLP 网络（10层，1024维），在保持实时性的同时，显著提升了生成运动的质量和多样性。定量证据表明，在 HumanML3D 数据集上，A-MDM 的 FID 指标为 $1.7435 \pm 0.0813$，远优于 MVAE 的 $11.2393 \pm 0.1607$（Table 5）。

*   **vs. 非生成式自回归模型**：与 **NSM** (Starke et al., ACM Trans. Graph. 2019) 这类非生成式模型相比，A-MDM 作为生成式模型，能够产生更多样化的运动。在 LaFAN1 数据集上，A-MDM 的足部滑动指标（FS↓）为 1.99，优于 NSM 的 2.25（Table 6），证明了其在物理合理性上的优势。

### 2. 适用边界与局限

A-MDM 的设计目标是为实时交互式角色控制提供一个通用、轻量且高质量的运动生成基座，其适用边界和局限性如下：

*   **适用场景**：A-MDM 擅长需要**实时响应**和**多样化输出**的任务，如目标到达、关键帧插值、用户指定关节轨迹的全身运动合成等。其核心优势在于，通过任务导向采样、空间/时间修补和分层强化学习等控制策略，**无需针对每个下游任务重新训练或微调**基座模型，即可完成新任务（Sections 4 & 5）。

*   **已知局限**：
    1.  **非自然控制下的质量退化**：当用户指定的控制信号（如关节轨迹）不自然或超出训练分布时，A-MDM 生成的运动会表现出明显的足部滑动和抖动。
    2.  **极端情况下的不稳定性**：作为自回归扩散模型，在极端情况下偶尔会产生不稳定行为或生成失败。
    3.  **时间一致性权衡**：目前仅预测单帧的设计可能牺牲了部分长程时间一致性，论文指出，探索多帧预测模型可能有益。
    4.  **任务导向采样的短视性**：该方法在需要精确、持续控制的路径跟随任务中表现不佳，难以紧密贴合用户指令。

### 3. 开放问题与后续方向

论文提出了若干值得探索的方向，这些构成了该知识库的开放前沿：

1.  **鲁棒性增强**：如何系统性地减轻在非自然用户控制下的足部滑动和抖动问题，是提升交互体验的关键。
2.  **模型架构演进**：探索多帧自回归扩散模型，是否能从根本上提升时间一致性，并使其能处理更复杂的控制任务。
3.  **推理速度优化**：能否将一致性模型等扩散模型加速技术集成到 A-MDM 框架中，以进一步降低推理延迟，为更复杂的实时应用提供算力余量。
4.  **控制策略深化**：如何克服任务导向采样的短视性，使其能适用于需要精确、持续控制的任务，是拓展其应用范围的重要问题。



## 原文 PDF

![[paperPDFs/SIGGRAPH_2024/Interactive_Character_Control_with_Auto_Regressive_Motion_Diffusion_Models.pdf]]
