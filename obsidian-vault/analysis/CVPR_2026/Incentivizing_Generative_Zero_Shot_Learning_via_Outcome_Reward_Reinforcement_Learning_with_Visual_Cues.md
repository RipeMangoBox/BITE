---
title: Incentivizing Generative Zero-Shot Learning via Outcome-Reward Reinforcement Learning with Visual Cues
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Incentivizing_Generative_Zero_Shot_Learning_via_Outcome_Reward_Reinforcement_Learning_with_Visual_Cues.pdf
project_link: null
code_link: null
aliases:
- IGZSLORRLVC
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过结果奖励强化学习（RL）将生成器的优化目标直接与下游分类正确率对齐，同时引入类级视觉原型约束来稳定训练并增强类内紧凑性。
primary_logic: 将生成器视为策略模型，用分类器作为奖励模型，引导生成器自我进化以合成更具判别力和任务相关性的视觉特征；利用微调视觉特征挖掘类级视觉原型，并通过原型蒸馏损失对齐合成特征与视觉原型，提升类内紧凑性和训练稳定性。
claims:
- 在CUB、SUN和AWA2三个基准上，RLVC在CZSL和GZSL设置下均取得最优准确率与调和均值（如CUB Acc 90.1%，H 81.2）。
- 消融实验表明，移除RL和视觉线索后性能显著下降（CUB Acc 88.6%→90.1%，H 75.1→81.2）。
- 原型蒸馏损失优于KL散度和L1损失，证实其设计有效性。
- CUB 上 Acc (CZSL) = 90.1%
---

# Incentivizing Generative Zero-Shot Learning via Outcome-Reward Reinforcement Learning with Visual Cues

> [!tip] 核心洞察
> 将生成器视为策略模型，用分类器作为奖励模型，引导生成器自我进化以合成更具判别力和任务相关性的视觉特征；利用微调视觉特征挖掘类级视觉原型，并通过原型蒸馏损失对齐合成特征与视觉原型，提升类内紧凑性和训练稳定性。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过结果奖励强化学习与视觉线索激励生成式零样本学习 |
| 英文题名 | Incentivizing Generative Zero-Shot Learning via Outcome-Reward Reinforcement Learning with Visual Cues |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.21138) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | RLVC |
| Dataset | CUB, SUN, AWA2, Overall |

> [!tip] 效果简介
> - CUB 上，Acc (CZSL) 90.1%。
> - SUN 上，Acc (CZSL) 77.7%。
> - AWA2 上，Acc (CZSL) 84.0%。

## 概要

生成式零样本学习（Generative Zero-Shot Learning, GZSL）通过合成未见类别的视觉特征来弥合语义与视觉模态之间的鸿沟。然而，现有方法面临两个关键瓶颈：**合成特征与下游分类任务脱节（任务无关）**，以及**仅依赖语义原型导致视觉相似但语义相近的类别特征重叠严重**。其根本原因在于，传统生成器仅以对抗损失为优化目标，缺乏来自分类任务的直接反馈信号。

针对上述问题，本文提出 **RLVC**（Outcome-Reward Reinforcement Learning with Visual Cues），核心思路是将生成器视为强化学习中的策略模型，用预训练分类器作为奖励模型，以分类正确类的对数概率作为结果奖励，直接引导生成器合成更具判别力和任务相关性的视觉特征。同时，RLVC从微调视觉特征中挖掘类级视觉原型，通过原型蒸馏损失将合成特征拉向对应原型，增强类内紧凑性与训练稳定性。

在 CUB、SUN 和 AWA2 三个标准基准上，RLVC 在 CZSL 和 GZSL 两种设置下均取得最优结果，平均准确率提升约 **4.7%**（Table 1）。消融实验证实，强化学习奖励与视觉线索两个组件对性能提升均有显著贡献（Table 3）。



### 零样本学习的生成式范式

零样本学习（Zero-Shot Learning, ZSL）旨在识别训练阶段未曾出现的未见类（unseen classes），其核心挑战在于弥合可见类（seen classes）与未见类之间的语义鸿沟。传统嵌入方法（embedding-based methods）试图将视觉特征与语义原型（如属性向量或词嵌入）映射到共享空间，但常因枢纽化问题（hubness problem）和跨模态对齐偏差而受限。

生成式ZSL方法（generative ZSL）另辟蹊径：利用语义原型作为条件，训练生成模型合成未见类的视觉特征，从而将ZSL转化为标准的监督分类问题。这类方法近年来取得了显著进展，代表性工作包括 **f-VAEGAN-D2**（Xian et al., CVPR 2019）、**TFVAEGAN**（Narayan et al., ECCV 2020）以及近期的 **ZeroDiff**（Ye et al., ICLR 2025）等。

### 现有方法的关键瓶颈

尽管生成式ZSL取得了可观进展，现有方法存在两个深层缺陷：

**瓶颈一：任务无关的生成目标。** 现有生成式ZSL方法通常仅依赖对抗损失（adversarial loss）训练生成器，优化目标是“合成看起来像真实特征的样本”，而非“合成对下游分类任务有用的特征”。这导致生成器可能产出视觉上逼真但判别力不足的特征——生成目标与分类任务之间存在根本性脱节。

**瓶颈二：语义原型驱动的类间重叠。** 生成器仅以语义原型（如属性向量）为条件，然而视觉相似但语义相近的类别（如不同种类的鸟类）在语义空间中高度邻近，导致合成特征在特征空间中严重重叠，类间边界模糊，直接损害分类精度。

Figure 1(a) 直观展示了这一困境：现有方法合成的特征分布散乱、类间交叠，而理想情况应是类内紧凑、类间分离。

### 本文动机：从“生成逼真特征”到“生成有用特征”

本文提出 **RLVC（Outcome-Reward Reinforcement Learning with Visual Cues）**，核心动机是将生成器的优化目标从“分布匹配”转向“任务对齐”。具体而言，RLVC 将生成器视为强化学习中的策略模型（policy model），以预训练的分类器作为奖励模型（reward model），用分类正确类的对数概率作为结果奖励信号，引导生成器自我进化，合成更具判别力的视觉特征。

同时，为缓解纯语义条件导致的类间重叠，RLVC 引入类级视觉原型（class-level visual prototypes）作为额外的条件线索：利用微调后的视觉编码器，按类别对可见类真实特征求均值，得到紧凑的视觉原型，并通过原型蒸馏损失将合成特征拉向对应原型，增强类内紧凑性和训练稳定性。

Figure 1(b) 展示了 RLVC 的预期效果：合成特征在奖励信号的引导下趋向任务相关，在视觉原型的约束下呈现清晰的类内聚集和类间分离。



## 核心方法与创新机理

RLVC的核心创新在于将生成式零样本学习（ZSL）重新置于强化学习（RL）视角下，通过两个关键“changed slots”解决了现有方法的根本瓶颈：**合成特征与下游分类任务脱节**以及**语义原型导致的类间特征重叠**。

### 1. 训练目标：从任务无关对抗到结果奖励驱动的自我进化

现有生成式ZSL方法（如**TFVAEGAN** (Narayan et al., ECCV 2020)、**f-VAEGAN-D2** (Xian et al., CVPR 2019)）仅依赖对抗损失 $\mathcal{L}_G^{\mathrm{adv}}$ 训练生成器，其优化目标与最终分类正确率无直接关联，导致合成特征虽在分布上接近真实特征，却未必具备判别力。

RLVC的根本性转变在于引入**结果奖励强化学习**，将生成器 $G_\theta$ 视为策略模型，将冻结的分类器 $R$ 作为奖励模型。奖励信号直接取自分类器对合成特征 $\tilde{\mathbf{x}}_0$ 预测正确类的对数概率：

$$r = \log p(y \mid \tilde{\mathbf{x}}_0)$$

通过指数移动平均（EMA）对奖励进行平滑处理并计算优势 $\widehat{A}_i$，RL损失直接驱动生成器朝“合成特征更容易被正确分类”的方向更新：

$$\mathcal{L}_{\mathrm{RL}} = -\frac{1}{B}\sum_i \widehat{A}_i \log p(y_i \mid \tilde{\mathbf{x}}_{0,i})$$

这一机制使生成器从“模仿真实特征分布”跃迁为“合成对分类任务有用的特征”，实现了生成目标与下游任务的因果对齐。消融实验（Table 3）证实：移除RL组件后，CUB数据集上的CZSL准确率从90.1%降至88.6%，GZSL调和均值从81.2骤降至75.1，验证了RL驱动的任务相关性是性能提升的核心杠杆。

### 2. 条件信息：从纯语义原型到语义-视觉双重约束

传统方法仅以语义原型 $\mathbf{z}^c$（属性向量或词嵌入）作为生成条件，但语义空间与视觉空间存在天然鸿沟——语义相近的类别在视觉上可能高度重叠，导致生成器难以区分细粒度差异。

RLVC引入**类级视觉原型**作为补充条件信号。通过对可见类微调视觉特征按类别求均值，得到视觉原型：

$$\mathbf{v}^c = \frac{1}{|\mathcal{T}_c|}\sum_{i\in\mathcal{T}_c} \mathbf{x}_i^s$$

在此基础上，设计**原型蒸馏损失**，以余弦距离度量合成特征与对应视觉原型的相似度：

$$\mathcal{L}_{\mathrm{PD}} = \frac{1}{B}\sum_i \left(1 - \frac{\tilde{\mathbf{x}}_{0,i}^\top \mathbf{v}^{c_i}}{\|\tilde{\mathbf{x}}_{0,i}\|_2\|\mathbf{v}^{c_i}\|_2}\right)$$

该损失将合成特征拉向类级视觉中心，增强类内紧凑性，同时为RL训练提供稳定锚点。Table 3的消融显示，仅移除视觉线索（保留RL）同样导致精度下降；Table 4进一步表明，该余弦距离形式在CUB、SUN、AWA2三个数据集上均优于KL散度和L1损失，验证了其设计有效性。

### 3. 训练策略：冷启动与交替优化

RL训练对奖励模型质量高度敏感。RLVC采用**冷启动**策略：先进行若干epoch的纯对抗训练（$\mathcal{L}_G^{\mathrm{adv}}$），待生成器具备基础合成能力后再激活RL损失，交替更新对抗损失和RL损失（Algorithm 1）。Figure 3的训练趋势图显示，奖励值在冷启动后逐步上升并趋于稳定，ZSL准确率随之平稳增长，证实该策略有效避免了RL初期的优化不稳定问题。

综上，RLVC通过“结果奖励对齐任务目标 + 视觉原型增强类内紧凑性 + 冷启动保障训练稳定”三个changed slots的协同作用，在CUB、SUN、AWA2三个基准上取得平均4.7%的CZSL准确率提升，实现了生成式ZSL从“分布模仿”到“任务驱动”的范式跃迁。



RLVC 将生成式零样本学习重新表述为一个结果奖励驱动的强化学习问题，其整体架构由四个核心模块构成闭环，如图 2 所示。

**顶层：奖励模型与视觉编码器。** 一个视觉编码器在可见类数据上进行微调，产出两类关键信息：一是微调后的视觉特征 $\mathbf{x}^s$，用于后续的视觉原型挖掘；二是冻结的分类器 $R$，它对任意输入特征输出类别预测概率，从而作为奖励模型提供任务相关的奖励信号 $r = \log p(y \mid \tilde{\mathbf{x}}_0)$（Eq. 7）。该奖励信号直接衡量合成特征被正确分类的可能性，是连接生成器与下游分类任务的因果纽带。

**底层：策略模型（生成器）与判别器。** 生成器 $G_\theta$ 被视作强化学习中的策略模型。它以噪声 $\epsilon$、语义原型 $\mathbf{z}^c$、扩散状态 $\mathbf{x}_t$ 和时间步 $t$ 为条件，输出合成的干净视觉特征 $\tilde{\mathbf{x}}_0$（Eq. 1）。两个判别器 $D_{x_0}$ 和 $D_{x_t}$ 分别区分真实与合成的干净特征以及状态转移对，构成标准的对抗训练框架，为生成器提供基础的分布对齐约束。

**中层：视觉原型挖掘与蒸馏。** 该模块从微调后的可见类视觉特征中，按类别计算均值得到类级视觉原型 $\mathbf{v}^c$（Eq. 12）。这些原型作为视觉线索，通过原型蒸馏损失 $\mathcal{L}_{\mathrm{PD}}$（Eq. 13）将合成特征拉向对应类的视觉中心，增强类内紧凑性并稳定训练。

**数据流与训练闭环。** 一次完整的训练迭代沿以下路径流动：语义原型 $\mathbf{z}^c$ 和噪声输入生成器，产出合成特征 $\tilde{\mathbf{x}}_0$；该特征同时送入判别器（计算对抗损失 $\mathcal{L}_G^{\mathrm{adv}}$）和冻结的奖励模型 $R$（计算奖励 $r$）；奖励经 EMA 平滑和停止梯度处理后转化为优势 $\widehat{A}$，驱动策略梯度损失 $\mathcal{L}_{\mathrm{RL}}$（Eq. 11）；同时，合成特征与对应的视觉原型 $\mathbf{v}^c$ 计算原型蒸馏损失。三者加权求和构成总生成器损失 $\mathcal{L}_G^{\mathrm{total}} = \mathcal{L}_G^{\mathrm{adv}} + \lambda_{\mathrm{PD}} \mathcal{L}_{\mathrm{PD}}$（Eq. 14），其中 RL 损失在满足冷启动阈值后交替加入更新。这一设计使得生成器在保持分布真实性的同时，被显式激励朝向更易被正确分类的方向自我进化。

### 补充图表

![[assets/figures/papers/paper_list_l2687_https_arxiv_org_abs_2603_21138/figures/002_Figure_2.jpg]]
*Figure 2: Model architecture and training of RLVC. The top panel shows how we train the reward model with a visual encoder to produce fine-tuned visual features and reward signals. The bottom panel depicts how we update the policy model*



### 3.1 扩散生成基座

RLVC 将生成器构建在扩散生成框架之上。给定类级语义原型 $\mathbf{z}^c$（如属性向量或词嵌入）和标准高斯噪声 $\epsilon$，生成器 $G_\theta$ 在扩散状态 $\mathbf{x}_t$ 和时间步 $t$ 的条件下合成视觉特征：

$$\tilde{\mathbf{x}}_0 = G_\theta(\epsilon, \mathbf{z}^c, \mathbf{x}_t, t) \in \mathbb{R}^d$$

框架包含两个判别器：$D_{x_0}$ 负责区分真实干净特征与合成干净特征，$D_{x_t}$ 负责区分真实状态转移与合成状态转移。生成器的对抗损失为：

$$\mathcal{L}_G^{\mathrm{adv}} = -\mathbb{E}[D_{x_0}(\tilde{\mathbf{x}}_0, \mathbf{z}^c)] - \mathbb{E}[D_{x_t}(\tilde{\mathbf{x}}_t, \mathbf{x}_{t+1}, \mathbf{z}^c, t)]$$

判别器总损失为两者之和：$\mathcal{L}_D = \mathcal{L}_{D_{x_0}} + \mathcal{L}_{D_{x_t}}$。这一基座沿用了生成式 ZSL 的经典对抗训练范式，但仅依赖语义原型约束，合成特征与下游分类任务之间存在脱节。

### 3.2 结果奖励强化学习模块

为解决任务脱节问题，RLVC 将生成器视为策略模型，引入冻结的分类器 $R$ 作为奖励模型。对于合成特征 $\tilde{\mathbf{x}}_0$，奖励信号定义为分类器对正确类 $y$ 的对数概率：

$$r = \log p(y \mid \tilde{\mathbf{x}}_0)$$

该结果奖励直接衡量合成特征在下游分类任务中的正确性，从而将生成器的优化目标与分类准确率对齐。为稳定训练，对奖励序列进行指数移动平均（EMA）平滑后减去基线，得到优势估计 $\widehat{A}_i$，并通过停止梯度操作防止奖励模型被生成器反向影响。最终的策略梯度损失为：

$$\mathcal{L}_{\mathrm{RL}} = -\frac{1}{B}\sum_i \widehat{A}_i \log p(y_i \mid \tilde{\mathbf{x}}_{0,i})$$

该损失推动生成器朝向更易被正确分类的方向合成特征，形成自我进化的闭环。

### 3.3 视觉线索与原型蒸馏模块

仅依赖语义原型容易导致视觉相似但语义相近的类别特征重叠。RLVC 从微调后的视觉特征中挖掘类级视觉原型，对第 $c$ 类所有可见类特征求均值：

$$\mathbf{v}^c = \frac{1}{|\mathcal{T}_c|}\sum_{i\in\mathcal{T}_c} \mathbf{x}_i^s$$

其中 $\mathcal{T}_c$ 为第 $c$ 类在微调视觉特征中的样本集合。随后通过原型蒸馏损失将合成特征拉向对应视觉原型，以余弦距离度量：

$$\mathcal{L}_{\mathrm{PD}} = \frac{1}{B}\sum_i \left(1 - \frac{\tilde{\mathbf{x}}_{0,i}^\top \mathbf{v}^{c_i}}{\|\tilde{\mathbf{x}}_{0,i}\|_2\|\mathbf{v}^{c_i}\|_2}\right)$$

该损失增强类内紧凑性，并为 RL 训练提供稳定的几何约束。最终生成器总损失为对抗损失与原型蒸馏损失的加权和：

$$\mathcal{L}_G^{\mathrm{total}} = \mathcal{L}_G^{\mathrm{adv}} + \lambda_{\mathrm{PD}} \mathcal{L}_{\mathrm{PD}}$$

### 3.4 冷启动训练策略

直接引入 RL 损失可能导致早期训练不稳定。RLVC 采用冷启动策略：先进行若干 epoch 的纯对抗训练（$\mathcal{L}_G^{\mathrm{adv}}$），待生成器具备基本合成能力且奖励达到预设阈值后，再交替更新对抗损失和 RL 损失（Algorithm 1）。RL 更新的学习率（$5\times10^{-5}$）低于对抗损失的学习率（$5\times10^{-4}$），以保证训练平稳过渡。训练趋势（Figure 3）表明，奖励值随训练逐步上升并趋于稳定，优势估计仅小幅波动，ZSL 准确率持续增益，验证了该策略的有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2687_https_arxiv_org_abs_2603_21138/figures/001_Figure_1.jpg]]
*Figure 1: Motivating illustration. (a) Existing generative ZSL methods train with adversarial losses conditioned only on semantic prototypes. This often leads to task-agnostic synthesized features and inter-class overlap. (b) Our RLVC incentivizes the generative model updating via RL reward and visual cues, enabling synthesized features that remain task-relevant and faithfully represent the data distribution*



## 实验与关键发现

### 实验设置

RLVC 在三个标准零样本学习基准上进行评估：**CUB**（细粒度鸟类分类，200 类）、**SUN**（场景识别，717 类）和 **AWA2**（动物属性分类，50 类）。实验覆盖两种设定：**CZSL**（常规零样本学习，仅未见类分类）和 **GZSL**（广义零样本学习，见/未见类联合分类），评价指标分别为 Top-1 准确率（Acc）与调和均值 H = (2 × S × U) / (S + U)。

生成器与判别器采用 Adam 优化器（betas = (0.5, 0.999)），对抗损失学习率为 5×10⁻⁴，RL 损失学习率为 5×10⁻⁵。推理阶段冻结生成器 G_θ，通过 Eq. (1) 合成未见类视觉特征；CZSL 下仅用合成特征训练 softmax 分类器，GZSL 下则将微调后的可见类真实特征与合成未见类特征联合训练分类器。

### 主实验结果

**Table 1** 报告了 RLVC 与 SOTA 方法在三个基准上的全面对比。在 CZSL 设定下，RLVC 在所有数据集上取得最优准确率：CUB 90.1%，SUN 77.7%，AWA2 84.0%。在更具挑战性的 GZSL 设定下，RLVC 同样在所有数据集上取得最高调和均值 H：CUB 81.2，SUN 57.6，AWA2 80.4。相较此前 SOTA，平均准确率增益达 4.7%（见摘要声明）。

值得关注的是，RLVC 在细粒度数据集 CUB 上的提升尤为显著——CZSL 准确率突破 90%，GZSL 调和均值超过 81%，表明结果奖励 RL 机制能有效引导生成器合成更具判别力的细粒度视觉特征。在类别数最多的 SUN（717 类）上，RLVC 依然保持优势，验证了方法的可扩展性。

**Table 2** 进一步验证了 RLVC 在不同语义原型下的鲁棒性：无论是类别名称的词嵌入还是专家标注的属性向量，RLVC 均能取得一致的性能提升（括号内为增益百分比），说明该方法不依赖于特定语义表示形式。

### 消融实验

**Table 3** 揭示了 RLVC 各组件的独立贡献。移除 RL 和视觉线索后（即仅保留对抗训练），CUB 准确率从 90.1% 降至 88.6%，调和均值从 81.2 骤降至 75.1，降幅超过 6 个百分点。仅移除视觉线索（保留 RL）同样导致性能下降，证实视觉原型对稳定 RL 训练和增强类内紧凑性具有不可替代的互补作用。

**Table 4** 对比了不同原型蒸馏损失的替换效果。本文提出的余弦距离损失 L_PD 在所有数据集上均优于 KL 散度损失和 L1 损失，验证了其设计合理性——余弦距离直接度量合成特征与视觉原型的方向一致性，比概率分布匹配或逐元素回归更适合高维视觉特征的对齐。

### 训练动态分析

**Figure 3** 展示了 CUB 上的训练趋势：原始奖励随训练推进逐步上升并趋于稳定，EMA 调整后的优势仅呈现小幅波动，ZSL 准确率持续稳步增长。这一动态表明，冷启动策略有效避免了 RL 训练初期的不稳定，而 EMA 平滑机制抑制了奖励方差，使策略梯度更新更加平稳。

### 定性可视化

**Figure 4** 的 t-SNE 可视化直观对比了三种变体的特征分布：(a) 无 RL 且无视觉线索时，未见类合成特征与可见类真实特征混杂，类间重叠严重；(b) 仅移除视觉线索时，类内散布有所改善但仍存在模糊边界；(c) 完整 RLVC 下，未见类合成特征形成紧凑且边界清晰的簇，与可见类真实特征的分布结构高度一致。这从几何角度印证了 RL 奖励信号与视觉原型蒸馏损失的协同效应。

### 局限性与失败模式

尽管 RLVC 在标准基准上表现优异，但仍存在以下局限：

1. **对监督视觉特征的依赖**：视觉原型的计算需要已标注的可见类微调特征，在极端少样本或无监督场景下该前提不成立。
2. **超参数敏感性**：冷启动阈值和视觉损失系数需针对不同数据集分别调整（见 **Figure 5** 超参数分析），可能增加实际部署的调参负担。
3. **奖励模型质量依赖**：RL 训练对奖励模型的预训练质量敏感——若分类器在可见类上未充分收敛，策略优化可能出现不稳定或次优收敛。这一失败模式在细粒度类别差异微小的场景下尤为突出，需在实际应用中手动验证奖励模型的可靠性。

![[assets/figures/papers/paper_list_l2687_https_arxiv_org_abs_2603_21138/figures/009_Figure_5.jpg]]
*Figure 5: Effect of hyperparameters on CUB, including the epoch of RL cold-start, the coefficient of visual loss, and the number of synthetic unseen samples*

### 补充图表

![[assets/figures/papers/paper_list_l2687_https_arxiv_org_abs_2603_21138/figures/004_Table_1.jpg]]
*Table 1: Compared our RLVC with the SOTA methods in CZSL and GZSL settings on CUB, SUN and AWA2 benchmarks. The symbol “⋆” indicates the semantic prototypes from the class name. The symbol “–” denotes that no results are provided in the original papers. The bold and underlined markings indicate the best and second-best results, respectively*

![[assets/figures/papers/paper_list_l2687_https_arxiv_org_abs_2603_21138/figures/006_Table_3.jpg]]
*Table 3: Results of RLVC variants on CUB, SUN and AWA2 datasets. We ablate specific components to assess their effectiveness. The bold marking indicates the best results*

![[assets/figures/papers/paper_list_l2687_https_arxiv_org_abs_2603_21138/figures/007_Table_4.jpg]]
*Table 4: Comparison results for different prototype-distillation losses combined with RLVC on CUB, SUN and AWA2 datasets. The bold marking indicates the best results*

![[assets/figures/papers/paper_list_l2687_https_arxiv_org_abs_2603_21138/figures/005_Table_2.jpg]]
*Table 2: Effectiveness validation of RLVC across different semantic prototypes, including word embeddings of class names and expertannotated attribute vectors. We mark the best results in bold and the accuracy gains (%) in parentheses*

![[assets/figures/papers/paper_list_l2687_https_arxiv_org_abs_2603_21138/figures/003_Figure_3.jpg]]
*Figure 3: The training trends of our RLVC on CUB, including raw reward, EMA-adjusted advantage and ZSL accuracy*

![[assets/figures/papers/paper_list_l2687_https_arxiv_org_abs_2603_21138/figures/008_Figure_4.jpg]]
*Figure 4: Qualitative t-SNE visualization of RLVC on CUB: (a) without RL and visual cues, (b) without visual cues, and (c) full RLVC. We use real features of seen classes and synthetic features of unseen classes. Zoom in for details*



## 定位与知识库关联

### 生成式零样本学习的演进

生成式ZSL的核心思想是通过语义-视觉映射合成未见类特征，将零样本分类转化为标准的全监督分类问题。早期方法以VAE和GAN为基础：**f-VAEGAN-D2**（Xian et al., CVPR 2019）率先将条件VAE与WGAN结合，通过语义原型条件生成视觉特征；**TFVAEGAN**（Narayan et al., ECCV 2020）进一步引入任务感知的反馈机制以提升特征判别力。然而，这些方法存在一个共同瓶颈：生成器的训练目标仅依赖对抗损失，缺乏与下游分类任务的有效对齐，导致合成特征虽视觉合理但任务无关（task-agnostic），且语义相近的类别间特征重叠严重。

近期工作尝试从不同角度缓解这一问题。**ViFR**、**GenZSL**、**VADS**、**DSP** 和 **TDCSS** 等方法分别通过特征精炼、解耦表示或对比学习来增强合成质量，但本质上仍将生成器优化与分类器训练解耦。**ZeroDiff**（Ye et al., ICLR 2025）作为当前SOTA，将扩散模型引入生成式ZSL，在特征质量上取得显著提升，但其训练范式仍以对抗损失为核心，未从根本上解决任务对齐问题。

### RLVC的方法定位与核心贡献

RLVC在生成式ZSL谱系中的独特位置在于：**首次将生成器显式建模为强化学习中的策略模型**，通过结果奖励信号将合成特征的优化目标直接与分类正确率对齐。这一视角转换带来了三个关键设计：

1. **任务驱动的奖励机制**：以冻结的分类器作为奖励模型，用预测正确类的对数概率 $r = \log p(y \mid \tilde{\mathbf{x}}_0)$ 作为奖励信号，通过EMA平滑和优势函数 $\widehat{A}_i$ 稳定策略梯度更新。这使生成器从“生成逼真特征”转向“生成易于被分类器正确识别的特征”。

2. **视觉原型约束**：从微调后的可见类视觉特征中提取类级视觉原型 $\mathbf{v}^c = \frac{1}{|\mathcal{T}_c|}\sum_{i\in\mathcal{T}_c} \mathbf{x}_i^s$，通过余弦距离构建原型蒸馏损失 $\mathcal{L}_{\mathrm{PD}}$，将合成特征拉向对应类的视觉中心。这既增强了类内紧凑性，又为RL训练提供了稳定的几何锚点，缓解了纯奖励驱动训练的不稳定性。

3. **冷启动与交替优化**：先进行若干epoch的对抗训练使生成器具备基本的特征合成能力，达到RL阈值后再交替更新对抗损失和RL损失。这一策略避免了RL训练初期奖励信号质量不足导致的策略崩溃。

与ZeroDiff等扩散生成方法相比，RLVC的增量在于**优化范式的转变**而非网络架构的革新——它保留了扩散生成框架（生成器 $G_\theta$、判别器 $D_{x_0}$ 和 $D_{x_t}$）作为基础，但将训练目标从单一的对抗损失 $\mathcal{L}_G^{\mathrm{adv}}$ 扩展为对抗损失 + RL损失 + 原型蒸馏损失的联合优化。

### 适用边界与局限

RLVC的设计隐含以下假设和边界条件：

- **依赖有监督视觉特征**：视觉原型的计算需要在已标注的可见类上聚合微调特征，这意味着RLVC无法直接应用于完全无标注的场景。当可见类样本稀疏时，视觉原型的估计质量可能下降。
- **奖励模型质量敏感**：RL训练的效果高度依赖奖励模型（分类器）的预训练质量。若奖励模型在可见类上欠拟合或过拟合，其提供的奖励信号将误导策略优化，导致合成特征偏离真实分布。
- **超参数调优负担**：冷启动阈值、视觉损失系数 $\lambda_{\mathrm{PD}}$、RL学习率等关键超参数需针对不同数据集分别调整（Figure 5展示了CUB上的敏感性），这增加了实际部署的调参成本。
- **未见类泛化假设**：视觉原型仅在可见类上计算，RLVC假设未见类的视觉特征分布与可见类的类内紧凑性模式相似。当可见-未见类域差异较大时，原型蒸馏的约束可能失效。

### 开放问题

1. **大规模与预训练模型适配**：当前实验基于中小规模基准（CUB、SUN、AWA2）和传统视觉特征。RLVC能否扩展到大规模数据集或与CLIP等预训练视觉特征结合，其RL训练稳定性和收益是否保持，尚待验证。

2. **RL算法的进阶选择**：当前采用简单的策略梯度（REINFORCE变体）。更先进的RL算法（如PPO、GRPO）是否能提升训练效率、降低方差或改善最终合成质量，是值得探索的方向。

3. **可学习的视觉原型**：当前视觉原型为固定均值，缺乏对未见类的适应能力。若将视觉原型设计为可学习参数或通过元学习从语义原型预测，可能进一步提升跨类泛化能力。

4. **跨任务迁移**：RLVC的“生成器-奖励模型”协同框架本质上是任务感知条件生成的一种通用范式。它能否推广到文本到图像合成、跨模态生成等其他条件生成任务，其有效性边界在哪里，是更广泛的研究问题。



## 原文 PDF

![[paperPDFs/CVPR_2026/Incentivizing_Generative_Zero_Shot_Learning_via_Outcome_Reward_Reinforcement_Learning_with_Visual_Cues.pdf]]
