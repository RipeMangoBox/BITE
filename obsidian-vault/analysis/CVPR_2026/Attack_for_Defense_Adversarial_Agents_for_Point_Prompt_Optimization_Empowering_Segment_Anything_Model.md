---
title: "Attack for Defense: Adversarial Agents for Point Prompt Optimization Empowering Segment Anything Model"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Attack_for_Defense_Adversarial_Agents_for_Point_Prompt_Optimization_Empowering_Segment_Anything_Model.pdf
project_link: null
code_link: null
aliases:
- PPDP
- ADAAPPOESAM
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过对抗式强化学习框架，攻击智能体学习激活破坏性提示以降低SAM性能，防御智能体学习抑制这些有害提示并恢复精度；两个智能体在双空间图环境中交互训练，以分割质量变化为奖励，从而实现动态提示优化。
primary_logic: 构建一个任务无关的双空间图环境（融合DINOv2特征距离和物理距离），并利用对抗式DQN智能体基于分割反馈选择激活/去激活提示，防御智能体能够自主学习识别并抑制有害提示，从而在推理时无需重新训练即可即插即用地提升SAM的分割质量。
claims:
- PPD攻击智能体可将理想提示的性能从mIoU 69.4降至21.5（PASCAL VOC），而防御智能体可恢复至63.5。
- PPD-FM在PASCAL VOC上mIoU达到60.3，对比FM-PPO的53.7，提升6.6个百分点；在ISIC上mIoU达到64.2，对比FM-PPO的62.4，提升1.8个百分点；在Kvasir上mIoU达到44.9，对比FM-PPO的29.5，提升15.4个百分点。
- PPD在推理时不依赖任何下游任务，仅使用防御智能体过滤低质量提示，实现任务无关的即插即用优化。
- PPD利用DINOv2特征构建的双空间图环境，使智能体能够基于特征和物理距离联合推理提示配置，从而有效学习攻击与防御策略。
---

# Attack for Defense: Adversarial Agents for Point Prompt Optimization Empowering Segment Anything Model

> [!tip] 核心洞察
> 构建一个任务无关的双空间图环境（融合DINOv2特征距离和物理距离），并利用对抗式DQN智能体基于分割反馈选择激活/去激活提示，防御智能体能够自主学习识别并抑制有害提示，从而在推理时无需重新训练即可即插即用地提升SAM的分割质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 以攻为守：对抗式智能体驱动的点提示优化方法用于增强Segment Anything模型 |
| 英文题名 | Attack for Defense: Adversarial Agents for Point Prompt Optimization Empowering Segment Anything Model |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2509.18891) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | Point Prompt Defender (PPD) |
| Dataset | PASCAL VOC, ISIC, Kvasir |

> [!tip] 效果简介
> - PASCAL VOC 上，mDSC (%) 69.1 (FM-PPD) vs 62.1 (FM-PPO) (+7.0)；mIoU (%) 60.3 (FM-PPD) vs 53.7 (FM-PPO) (+6.6)。
> - ISIC 上，mDSC (%) 76.3 (FM-PPD) vs 72.3 (FM-PPO) (+4.0)；mIoU (%) 64.2 (FM-PPD) vs 62.4 (FM-PPO) (+1.8)。
> - Kvasir 上，mDSC (%) 54.8 (FM-PPD) vs 38.9 (FM-PPO) (+15.9)。

## 概要

Segment Anything Model（SAM）凭借其强大的零样本泛化能力，已成为视觉分割领域的基础模型。然而，SAM的分割质量高度依赖于点提示的精确性——一个关键瓶颈在于，现有方法通常依赖手工启发式或静态特征匹配生成提示，缺乏对分割反馈的动态适应，导致提示质量在不同场景下波动剧烈，泛化性和鲁棒性不足。

针对这一瓶颈，本文提出了一种“以攻为守”的对抗式强化学习框架——**Point Prompt Defender (PPD)**。其核心思想是：通过构建一个攻击智能体（Attack Agent）来主动探索并激活破坏性提示，迫使SAM分割性能下降；同时训练一个防御智能体（Defense Agent）学习识别并抑制这些有害提示，从而恢复分割精度。两个智能体在基于DINOv2特征距离与物理距离联合构建的双空间图环境中交替训练，以Dice系数的变化作为奖励信号，无需任务特定标签即可自主学习提示优化策略。

PPD的关键优势在于其**任务无关的即插即用特性**：防御智能体一旦训练完成，在推理时可直接对任意初始提示集进行过滤优化，无需针对下游任务重新训练或域适配。这使得PPD能够作为一种通用的提示增强模块，灵活嵌入各类基于SAM的分割流程中。

实验结果表明，PPD在自然图像和医学图像分割任务上均展现出显著的性能提升。在单样本SAM分割设定下，PPD-FM在PASCAL VOC上mIoU达到60.3%，相较基线FM-PPO（53.7%）提升6.6个百分点；在医学数据集ISIC上mIoU达到64.2%，提升1.8个百分点；在更具挑战性的Kvasir内窥镜数据集上，mIoU从29.5%跃升至44.9%，提升幅度高达15.4个百分点。消融实验进一步验证了攻击-防御机制的有效性：攻击智能体可将理想提示的mIoU从69.4骤降至21.5，而防御智能体可恢复至63.5，证明了对抗式训练框架在探索提示空间和抑制有害提示方面的核心价值。



**Segment Anything Model (SAM) 的提示依赖瓶颈。** SAM 作为视觉基础模型，在图像分割任务中展现出强大的零样本泛化能力。然而，其分割质量高度依赖于用户提供的点提示质量。在实际部署中，用户通常难以给出精确的提示点，导致分割结果出现边界模糊、区域缺失或误分割等问题。这一“提示敏感性”构成了 SAM 从通用模型走向可靠下游应用的核心瓶颈。

**现有提示优化方法的局限。** 当前针对 SAM 的提示工程方法大致分为两类：一类依赖手工设计的启发式规则生成提示，缺乏对分割反馈的动态适应；另一类采用单智能体强化学习进行提示优化，如 **FM-PPO**（Liu et al., CVPR 2025）通过特征匹配初始化并迭代优化点提示。然而，这些方法存在两个关键缺口：(1) 优化策略依赖任务特定的先验或微调，难以在不同场景间泛化；(2) 缺乏对“有害提示”的主动识别与抑制机制，导致在低质量初始提示下鲁棒性不足。

**“以攻为守”的核心动机。** 本文提出一个关键洞察：要提升 SAM 对提示扰动的鲁棒性，最有效的方式是主动暴露于破坏性提示并学习防御。基于这一思想，PPD（Point Prompt Defender）构建了一个对抗式强化学习框架——攻击智能体学习激活破坏性提示以降低 SAM 性能，防御智能体则学习识别并抑制这些有害提示以恢复分割精度。通过这种“攻击-防御”的博弈训练，防御智能体能够在推理时即插即用地过滤任意初始提示中的噪声，实现任务无关的鲁棒增强。



## 核心方法与创新机理

PPD的核心创新在于将点提示优化重新定义为一个**对抗式强化学习问题**，通过“以攻为守”的双智能体博弈机制，动态探索并抑制对SAM分割有害的提示。其关键创新点可归纳为以下四个维度：

### 1. 对抗式双智能体优化范式

现有方法（如**FM-PPO**（Liu et al., CVPR 2025））采用单智能体强化学习，直接从特征匹配初始化点提示并迭代优化，缺乏对提示间复杂交互和潜在破坏性影响的显式建模。PPD引入**攻击智能体**与**防御智能体**的竞争性博弈框架：攻击智能体主动学习激活能够最大化SAM分割性能下降的破坏性提示，防御智能体则学习去激活这些有害提示以恢复分割精度。两个智能体均基于DQN实现，以SAM输出的Dice系数变化作为奖励信号进行训练（公式见Section III.B，Equation 4和6）。这种对抗训练机制迫使防御智能体在多样化的提示扰动下学习鲁棒的过滤策略，而非简单地向最优方向微调。

### 2. 双空间图环境的结构化推理

传统方法通常直接使用点坐标或简单的特征距离来表征提示关系。PPD构建了一个**任务无关的双空间异质图环境**，将每个点提示建模为图节点，节点间的边同时编码两种距离信息：
- **特征距离矩阵** $M_f(i,j) = \| f_i - f_j \|$，基于DINOv2提取的图像补丁特征向量计算；
- **物理距离矩阵** $M_p(i,j) = \| x_i - x_j \|$，基于补丁几何中心的欧氏距离。

这种双空间表示使智能体能够联合推理提示的语义相似性和空间邻近性，从而更精准地判断哪些提示组合可能产生冲突或干扰。该图环境是任务无关的，不依赖任何下游任务标签或域特定信息，为后续的即插即用部署奠定了基础。

### 3. 分割反馈驱动的自监督训练信号

与需要任务特定标签或分割原型的基线方法不同，PPD的训练信号完全来自**SAM自身输出的分割质量变化**。攻击奖励 $r_t^{\mathrm{atk}} = -(\mathrm{Dice}(\hat{M}_t, M) - \mathrm{Dice}(\hat{M}_{t-1}, M))$ 鼓励降低Dice系数，防御奖励 $r_t^{\mathrm{def}} = \mathrm{Dice}(\hat{M}_t, M) - \mathrm{Dice}(\hat{M}_{t-1}, M)$ 鼓励提升Dice系数。这种设计使得PPD无需针对不同下游任务重新设计损失函数或标注数据，仅通过SAM的通用分割反馈即可学习提示优化的通用策略。

### 4. 任务无关的即插即用推理

PPD在推理阶段仅部署训练好的**防御智能体**，对任意来源的初始提示集（如特征匹配、手工标注等）进行过滤优化，无需针对下游任务微调或域适配。消融实验表明（Table I），在PASCAL VOC上，攻击智能体可将理想提示的mIoU从69.4降至21.5，而防御智能体可恢复至63.5；在ISIC上，对特征匹配提示施加PPD防御后，mIoU从55.0提升至64.2。这验证了防御智能体在任务无关设置下对低质量提示的有效过滤能力。

### 创新点总结

| 创新维度 | 基线方法 | PPD方法 |
|---------|---------|---------|
| 优化策略 | 启发式或单智能体RL | 对抗式双智能体RL（攻击-防御博弈） |
| 提示表示 | 点坐标或简单特征距离 | 双空间图（DINOv2特征距离+物理距离） |
| 训练信号 | 任务特定标签或原型 | SAM输出的Dice系数变化（自监督） |
| 推理适应 | 需微调或域适配 | 任务无关部署，仅用防御智能体过滤 |



PPD (Point Prompt Defender) 采用“以攻为守”的对抗式强化学习框架，其核心由三个关键组件构成：**双空间图环境**、**攻击智能体**与**防御智能体**。整体流程如图2所示：首先利用参考图像构建融合DINOv2特征距离与物理距离的双空间异质图，并基于真实掩码初始化一组理想提示作为交互起点；随后，攻击智能体与防御智能体在SAM分割反馈的驱动下交替博弈——攻击者学习激活破坏性提示以降低分割质量，防御者学习去激活这些有害提示以恢复精度；训练完成后，仅需部署防御智能体即可在推理时对任意初始提示集进行过滤优化，实现任务无关的即插即用增强。

### 双空间图环境构建

PPD将提示优化问题建模为图上的序贯决策过程。对于给定图像，首先将其划分为规则补丁网格，利用预训练的DINOv2模型提取每个补丁的特征向量 $f_i$，并计算特征距离矩阵 $M_f(i,j) = \| f_i - f_j \|$ 与物理距离矩阵 $M_p(i,j) = \| x_i - x_j \|$（其中 $x_i$ 为补丁几何中心坐标）。该异质图环境使智能体能够同时基于语义相似性和空间邻近性进行结构化推理，而非孤立地评估单个提示点。

### 理想提示初始化

为构建对抗训练的起点，PPD在训练图像的ground-truth掩码内部和外部均匀采样正负点提示，形成“理想提示集”。这些高质量初始提示为攻击智能体提供了明确的优化基准——攻击者的目标是偏离这一理想状态，而防御者则需从中识别并抑制被注入的有害提示。

### 对抗式双智能体训练

训练过程采用交替回合制：每一轮中，攻击智能体（DQN）从当前非活跃提示集合 $\mathcal{A}_t^{\mathrm{atk}} = \{ p_i \in \mathcal{P} \mid \mathrm{status}_i = \mathrm{inactive} \}$ 中选择一个提示激活，以最大化SAM分割性能的下降，其奖励函数为 $r_t^{\mathrm{atk}} = -\left( \mathrm{Dice}(\hat{M}_t, M) - \mathrm{Dice}(\hat{M}_{t-1}, M) \right)$；随后防御智能体（DQN）从活跃提示集合 $\mathcal{A}_t^{\mathrm{def}} = \{ p_i \in \mathcal{P} \mid \mathrm{status}_i = \mathrm{active} \}$ 中选择一个提示去激活，以恢复分割精度，奖励函数为 $r_t^{\mathrm{def}} = \mathrm{Dice}(\hat{M}_t, M) - \mathrm{Dice}(\hat{M}_{t-1}, M)$。两个Q网络均通过时序差分损失 $\mathcal{L}_t = \left( r_t + \gamma \max_{a'} Q_{\theta^-}(s_{t+1}, a') - Q_\theta(s_t, a_t) \right)^2$ 进行优化。这一对抗机制迫使防御智能体在攻击者制造的多样化破坏场景中学习鲁棒的提示过滤策略。

### 防御专用推理

推理阶段仅使用训练好的防御智能体，无需攻击智能体参与。给定任意初始提示集（如特征匹配方法生成的提示），防御智能体基于双空间图环境逐轮评估并去激活有害提示，直至收敛。此过程不依赖任何下游任务标签或微调，实现了真正的即插即用部署。

图3的定性结果表明，攻击智能体能有效引入破坏性提示导致分割退化，而防御智能体可显著恢复分割质量，验证了对抗训练框架的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2761_https_arxiv_org_abs_2509_18891/figures/002_Figure_2.jpg]]
*Figure 2: Overview of PPD: A dual-space graph and ideal prompts form the environment. Guided by SAM segmentation feedback, the attack agent activates poor prompts to degrade performance, while the defense agent suppresses them to recover accuracy. Solid and dashed lines denote agent training and testing phases, respectively*



PPD 的核心架构由三个紧密耦合的模块构成：**双空间图环境**、**对抗式双智能体训练**以及**防御智能体推理**。以下逐一展开其设计逻辑与关键公式。

### 1. 双空间图环境构建

PPD 将提示优化问题建模为一个异质图上的序列决策过程。给定一张图像，首先利用 DINOv2 提取图像补丁特征，构建一个融合语义与空间信息的双空间图。

**特征距离矩阵**衡量图像补丁间的语义相似性：

$$M_f(i,j) = \| f_i - f_j \|$$

其中 $f_i$、$f_j$ 分别为第 $i$ 和第 $j$ 个图像补丁的 DINOv2 特征向量，$\|\cdot\|$ 为欧氏距离。该矩阵编码了不同图像区域在语义空间中的远近关系。

**物理距离矩阵**捕捉补丁间的空间邻近性：

$$M_p(i,j) = \| x_i - x_j \|$$

其中 $x_i$、$x_j$ 为补丁几何中心的二维坐标。联合这两种距离信息，图节点能够同时感知语义关联和空间约束，为后续智能体的结构化推理提供基础。

在此基础上，PPD 通过**理想提示初始化**为对抗训练提供高质量起点：在训练图像的真实掩码内部均匀采样正点提示，在掩码外部均匀采样负点提示，构成初始提示集 $\mathcal{P}$。

### 2. 对抗式双智能体训练

PPD 采用两个独立的 DQN 智能体进行交替对抗训练，以 SAM 输出的 Dice 系数变化作为奖励信号。

**攻击智能体**的目标是最大化分割性能的下降。其动作空间为当前所有非活跃提示：

$$\mathcal{A}_t^{\mathrm{atk}} = \{ p_i \in \mathcal{P} \mid \mathrm{status}_i = \mathrm{inactive} \}$$

攻击智能体从中选择一个提示 $p_i$ 激活，将其加入提示集并送入 SAM 生成新的分割预测 $\hat{M}_t$。奖励函数定义为 Dice 系数的负向变化：

$$r_t^{\mathrm{atk}} = -\left( \mathrm{Dice}(\hat{M}_t, M) - \mathrm{Dice}(\hat{M}_{t-1}, M) \right)$$

其中 $M$ 为真实掩码。当攻击动作导致分割质量下降时，奖励为正，鼓励智能体发现破坏性提示。

**防御智能体**的目标是抑制有害提示以恢复分割精度。其动作空间为当前所有活跃提示：

$$\mathcal{A}_t^{\mathrm{def}} = \{ p_i \in \mathcal{P} \mid \mathrm{status}_i = \mathrm{active} \}$$

防御智能体从中选择一个提示去激活。奖励函数直接定义为 Dice 系数的正向变化：

$$r_t^{\mathrm{def}} = \mathrm{Dice}(\hat{M}_t, M) - \mathrm{Dice}(\hat{M}_{t-1}, M)$$

当去激活动作提升分割质量时，防御智能体获得正奖励。

两个智能体的 Q 网络均通过时序差分损失进行优化：

$$\mathcal{L}_t = \left( r_t + \gamma \max_{a'} Q_{\theta^-}(s_{t+1}, a') - Q_\theta(s_t, a_t) \right)^2$$

其中 $\gamma$ 为折扣因子，$\theta$ 和 $\theta^-$ 分别为当前 Q 网络和目标 Q 网络的参数。

**训练流程**：每个 episode 中，攻击智能体先执行若干步激活操作以降低 SAM 性能，随后防御智能体执行去激活操作以恢复精度。两个智能体交替更新，共享同一双空间图环境，但各自维护独立的 Q 网络。训练共进行 1000 个 episode，每个 episode 的环境步数在 50 到 300 之间随机采样。Q 网络使用 Adam 优化器训练，学习率为 $1 \times 10^{-4}$，批大小为 128。

### 3. 防御智能体推理

推理阶段仅部署训练好的防御智能体，攻击智能体不参与。给定任意初始提示集（可来自特征匹配、人工标注等），防御智能体基于双空间图环境对活跃提示进行去激活决策，过滤低质量或破坏性提示。这一过程不依赖任何下游任务标签，无需对 SAM 或智能体进行重训练，实现了任务无关的即插即用优化。

> **注意**：PPD 目前仅支持点提示的优化，尚未扩展至框提示或掩码提示。训练过程需构建双空间图并交替更新两个 DQN 网络，计算开销较大，且防御效果在一定程度上依赖初始提示的质量——当初始提示在空间或语义上完全偏离目标区域时，优化空间有限。

### 补充图表

![[assets/figures/papers/paper_list_l2761_https_arxiv_org_abs_2509_18891/figures/001_Figure_1.jpg]]
*Figure 1: Adversarial training in PPD: The attack agent activates prompts to worsen SAM segmentation, while the defense agent deactivates harmful prompts to improve it. A judge evaluates the segmentation quality based on the ground truth*



## 实验与关键发现

### 对抗攻击与防御的因果验证

PPD的核心机制——攻击智能体降低分割质量、防御智能体恢复精度——在消融实验中得到了直接验证。在PASCAL VOC数据集上，使用理想点提示（基于真实掩码均匀采样）的SAM分割基线mIoU为69.4。当攻击智能体介入并激活破坏性提示后，mIoU骤降至21.5，降幅高达47.9个百分点，证明攻击智能体能够有效探索提示空间的脆弱区域并施加强破坏性干扰。随后，防御智能体对活跃提示集进行过滤去激活，mIoU恢复至63.5，回升42.0个百分点，表明防御智能体学会了识别并抑制有害提示，在保留有效提示的同时大幅修复分割质量（Table I Top）。

在医学图像数据集ISIC上，PPD同样展现出稳定的优化能力。仅使用特征匹配生成的初始提示，mIoU为55.0；经PPD防御智能体优化后，mIoU提升至64.2，增益9.2个百分点（Table I Bottom）。这一结果表明，防御智能体不仅能够对抗自身攻击智能体产生的破坏，还能泛化至其他来源的低质量提示（如特征匹配），实现任务无关的即插即用优化。

### 单样本SAM分割主实验

在单样本SAM分割设定下，PPD与特征匹配初始化方法FM-PPO结合（记为FM-PPD），在自然图像和医学图像基准上与多个现有方法进行了对比（Table II）。主要结果如下：

**PASCAL VOC（自然图像）。** FM-PPD取得mDSC 69.1、mIoU 60.3，相较FM-PPO（mDSC 62.1、mIoU 53.7）分别提升7.0和6.6个百分点。与PerSAM（Zhang et al., ICLR 2024）、Matcher（Liu et al., ICLR 2024）、VRP-SAM（Sun et al., CVPR 2024）等方法相比，FM-PPD在所有指标上均取得最优或次优结果。

**ISIC（皮肤病变）。** FM-PPD取得mDSC 76.3、mIoU 64.2，相较FM-PPO（mDSC 72.3、mIoU 62.4）提升4.0和1.8个百分点。

**Kvasir（肠道息肉）。** FM-PPD取得mDSC 54.8、mIoU 44.9，相较FM-PPO（mDSC 38.9、mIoU 29.5）大幅提升15.9和15.4个百分点。该数据集上增益最为显著，说明在初始提示质量较差的场景下，PPD的防御过滤机制能发挥更大作用。

值得注意的是，PPD在推理时不依赖任何下游任务标签或微调，仅使用训练好的防御智能体对初始提示集进行去激活过滤。这种任务无关的部署方式使其能够直接嵌入现有的SAM推理流程，无需针对特定域重新训练。

### 定性分析

Figure 3展示了理想提示、攻击后及防御后的分割结果对比。攻击智能体激活的破坏性提示导致SAM产生明显的误分割和漏分割，而防御智能体通过去激活这些有害提示，使分割结果恢复到接近理想提示的水平。Figure 4进一步对比了初始特征匹配提示与PPD优化后提示的分割效果，PPD通过去除干扰性提示，有效抑制了无关区域的误激活，同时保留了目标区域的完整分割。Figure 5的多方法对比显示，FM-PPD在边界准确性和无关区域抑制方面优于PerSAM、Matcher和FM-PPO等方法。

### 训练与实现细节

PPD在FSS-1000数据集的1000张随机采样图像上进行训练，共1000个episode，每个episode的环境步数在50至300之间随机采样。两个DQN智能体的Q网络均使用Adam优化器训练，学习率为$1 \times 10^{-4}$，批量大小为128。双空间图环境的构建依赖DINOv2提取的图像补丁特征，特征距离矩阵和物理距离矩阵分别由公式$M_f(i,j) = \| f_i - f_j \|$和$M_p(i,j) = \| x_i - x_j \|$定义。

### 失败模式与局限性

尽管PPD在多个基准上表现优异，其优化效果仍受初始提示质量的制约。当初始提示在空间或语义上完全偏离目标区域时，双空间图环境中的节点特征可能无法提供足够的判别信息，导致防御智能体的过滤决策失效。此外，PPD目前仅支持点提示优化，尚未集成文本引导或多模态参考提示，在极端冷启动场景下缺乏额外的语义锚定。训练过程中的对抗交互需要交替更新两个DQN网络并反复查询SAM进行前向推理，计算开销较大，且依赖理想提示初始化环境，限制了其在无标注数据场景下的直接训练。

### 补充图表

![[assets/figures/papers/paper_list_l2761_https_arxiv_org_abs_2509_18891/figures/004_Table.jpg]]
*Table: I ABLATION RESULTS ON NATURAL AND MEDICAL DATASETS. TOP: DEGRADATION BY ATTACKS AND RECOVERY BY DEFENSE. BOTTOM: PERFORMANCE GAINS FROM PPD OPTIMIZATION OVER FEATURE MATCHING*

![[assets/figures/papers/paper_list_l2761_https_arxiv_org_abs_2509_18891/figures/006_Table.jpg]]
*Table: II ONE-SHOT SAM-BASED SEGMENTATION PERFORMANCE ON NATURAL AND MEDICAL DATASETS. BOLD AND UNDERLINED VALUES INDICATE THE BEST AND SECOND-BEST RESULTS, RESPECTIVELY*

![[assets/figures/papers/paper_list_l2761_https_arxiv_org_abs_2509_18891/figures/003_Figure_3.jpg]]
*Figure 3: Qualitative results of ideal prompts, after adversarial attack, and after defense. Our method effectively restores segmentation quality under prompt degradation*

![[assets/figures/papers/paper_list_l2761_https_arxiv_org_abs_2509_18891/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative results comparing initial prompts from the reference image and those optimized by PPD, which improves segmentation by removing disruptive prompts*

![[assets/figures/papers/paper_list_l2761_https_arxiv_org_abs_2509_18891/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative segmentation results of different one-shot SAM-based methods in natural and medical images*



## 定位与知识库关联

### 与现有提示优化方法的关系

PPD 的核心贡献在于将点提示优化从“单方试探”转变为“对抗博弈”，这与现有工作形成了明确的代际差异。

**提示工程与启发式方法**：早期工作如 **Matcher**（Liu et al., ICLR 2024）通过通用特征匹配为 SAM 提供初始点提示，**GBMSeg**（Liu et al., MICCAI 2024）则针对医学图像设计了免训练的提示工程策略。这些方法的共同瓶颈在于提示生成过程是静态的——一旦生成初始点集，便不再根据 SAM 的实际分割反馈进行调整。PPD 的双空间图环境虽然也利用特征距离（基于 DINOv2），但其目的不是直接生成提示，而是为后续的动态博弈提供结构化推理空间。

**单智能体强化学习优化**：**FM-PPO**（Liu et al., CVPR 2025）是 PPD 最直接的前身与对比基线。FM-PPO 采用单智能体 PPO 框架，通过特征匹配初始化点提示后迭代优化。PPD 在此基础上做出了两个关键改变：（1）将单智能体优化扩展为攻击-防御双智能体对抗框架，使提示探索空间从“正向优化”扩展为“破坏性探索+恢复性学习”；（2）将训练信号从任务特定标签替换为基于 Dice 系数变化的通用奖励，使训练过程与下游任务解耦。这一差异在实验结果中体现为：FM-PPD 在 PASCAL VOC 上 mIoU 达到 60.3，对比 FM-PPO 的 53.7 提升 6.6 个百分点（Table II）；在更具挑战性的 Kvasir 医学数据集上，mIoU 从 29.5 跃升至 44.9，提升 15.4 个百分点，表明对抗训练学到的防御策略在分布外场景下泛化性更强。

**SAM 个性化与微调方法**：**PerSAM** 和 **PerSAM-F**（Zhang et al., ICLR 2024）通过对 SAM 的提示编码器进行单样本微调来适应下游任务，**VRP-SAM**（Sun et al., CVPR 2024）则引入视觉参考提示编码器。这类方法的核心代价在于需要针对每个下游任务进行模型级适配。PPD 走的是正交路径：它保持 SAM 完全冻结，仅在推理时通过训练好的防御智能体对输入提示进行过滤。这意味着 PPD 可以即插即用地部署到任意已训练的 SAM 流水线上，无需重训练或域适配（Section III.C）。

### 适用边界与局限

尽管 PPD 在多个基准上展示了显著增益，其适用边界受以下因素约束：

1. **初始提示质量依赖**：PPD 的防御智能体学习的是“抑制有害提示”而非“从零生成提示”。当初始提示在空间或语义上完全偏离目标区域时（例如特征匹配完全失败），防御智能体缺乏有效的候选提示可供筛选，最终分割精度仍会受限。Table I 的消融实验显示，在 PASCAL VOC 上攻击可将理想提示的 mIoU 从 69.4 降至 21.5，防御后恢复至 63.5，但未能完全回到初始水平，印证了这一残余退化。

2. **提示类型限制**：当前 PPD 框架仅支持点提示的激活/去激活操作，尚未覆盖框提示（box prompt）或掩码提示（mask prompt）等其他 SAM 支持的提示模态。对于需要精确定位边界框或多模态引导的场景，PPD 无法直接复用。

3. **训练计算开销**：PPD 的训练过程需要构建双空间图（计算 DINOv2 特征距离矩阵 $M_f(i,j) = \| f_i - f_j \|$ 和物理距离矩阵 $M_p(i,j) = \| x_i - x_j \|$），并交替更新两个 DQN 网络。训练配置为 1000 个 episode，每个 episode 包含 50-300 个随机环境步数（Section IV.b），且依赖理想提示（从真实掩码均匀采样正负点）来初始化环境。这使其训练成本高于单智能体方法如 FM-PPO。

### 开放问题

1. **多模态提示融合**：PPD 目前仅利用视觉特征（DINOv2）构建图环境。如何将文本引导或其他多模态参考信息纳入双空间图表示，使防御智能体在极端冷启动条件下（如初始提示完全缺失）仍能有效运作，是一个待探索的方向。

2. **提示类型扩展**：将 PPD 的对抗博弈框架推广至框提示、掩码提示甚至混合提示类型，需要重新设计动作空间（例如框的平移/缩放、掩码的膨胀/腐蚀）和状态表示，但核心的“攻击-防御-反馈”机制理论上可迁移。

3. **训练效率优化**：当前对抗训练的交互步数较多。能否通过课程学习（curriculum learning）先训练攻击智能体再训练防御智能体，或引入模型化环境（model-based RL）减少与 SAM 的实际交互次数，从而加速收敛并保持防御泛化性，值得进一步研究。



## 原文 PDF

![[paperPDFs/CVPR_2026/Attack_for_Defense_Adversarial_Agents_for_Point_Prompt_Optimization_Empowering_Segment_Anything_Model.pdf]]
