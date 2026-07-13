---
title: Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Boosting_Vision_Language_Action_Finetuning_with_Feasible_Action_Neighborhood_Prior.pdf
project_link: null
code_link: null
aliases:
- FGRFSFP
- BVLAFFANP
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在 SFT 和 RFT 损失中引入 FAN 引导的 KL 散度正则项，强制策略分布朝着以最优动作为中心的高斯形状靠拢，从而扩大有效的可行动作邻域。
primary_logic: 将策略输出分布塑造成高斯形状，能够捕捉物理动作空间的局部平滑容错性，使模型不再仅仅追求单一正确动作，而是学习一个允许一定偏差的动作邻域，从而显著提升微调的泛化能力和样本效率。
claims:
- SFT 暖启动后策略分布极窄（成功率 48.4%），PPO 使其变宽（93.8%），FAN-PPO 明确塑造高斯形状并达到最高成功率（97.4%）。
- FAN-SFT 在 ManiSkill 基准上相比 OpenVLA+SFT 基线，分布内成功率提升 11.7%，OOD 平均提升 5.2%。
- FAN-PPO 在 ManiSkill 基准上相比 PPO 基线，OOD 平均成功率提升 6.2%（OpenVLA）和 7.9%（OpenVLA-OFT）。
- 真机实验中，FAN-SFT 在多个空间扰动任务上的成功率大幅领先标准 SFT（例如 Task-3 中 17/30 vs 7/30）。
---

# Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior

> [!tip] 核心洞察
> 将策略输出分布塑造成高斯形状，能够捕捉物理动作空间的局部平滑容错性，使模型不再仅仅追求单一正确动作，而是学习一个允许一定偏差的动作邻域，从而显著提升微调的泛化能力和样本效率。

| 字段 | 内容 |
|------|------|
| 中文题名 | 利用可行动作邻域先验增强视觉-语言-动作微调 |
| 英文题名 | Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.01570) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | FAN-guided Regularization (FAN-SFT / FAN-PPO) |
| Dataset | ManiSkill, ManiSkill OOD, ManiSkill (RFT) OOD average, Real-world Pick-and-Place |

> [!tip] 效果简介
> - ManiSkill (PutOnPlateInScene25Main) 上，In-Distribution Success Rate (%) 89.8 ± 0.8 (FAN-SFT) vs 78.1 ± 3.1 (OpenVLA+SFT) (+11.7)。
> - ManiSkill OOD (Vision, Semantic, Execution average) 上，OOD Success Rate (%) 63.3 (FAN-SFT) vs 58.1 (OpenVLA+SFT) (+5.2)。
> - ManiSkill (RFT) 上，In-Distribution Success Rate (%) 97.4 ± 0.7 (OpenVLA+FAN-PPO) vs 95.9 ± 3.2 (OpenVLA+PPO) (+1.5)。

## 概要

视觉-语言-动作（VLA）模型的微调通常直接继承大语言模型的训练范式——使用 one-hot 交叉熵（SFT）或 PPO 进行策略优化。然而，这种范式忽略了物理动作空间的一个关键特性：**可行动作邻域（Feasible Action Neighborhood, FAN）**——在最优动作附近存在一个连通的、允许一定偏差的动作集合，其 Q 值几乎等价。忽视这一容错性会导致策略过度拟合单一演示动作，产生极窄的分布，泛化能力差且样本效率低。

本文的核心洞察是：**将策略输出分布塑造成以最优动作为中心的高斯形状，能够有效捕捉物理动作空间的局部平滑容错性**。基于此，作者提出 **FAN 引导的正则化方法（FAN-SFT / FAN-PPO）**，在 SFT 和 RFT 损失中引入 KL 散度正则项，强制策略分布向目标高斯分布靠拢，从而扩大可行动作邻域，使模型不再仅仅追求单一正确动作，而是学习一个允许合理偏差的鲁棒策略。

决定性的证据来自 **Figure 1**：SFT 暖启动后策略分布极窄（成功率仅 48.4%），PPO 使其变宽（93.8%），而 FAN-PPO 明确塑造出高斯形状并达到最高成功率（97.4%）。在 ManiSkill 基准上，FAN-SFT 相比标准 SFT 分布内成功率提升 **11.7%**，OOD 平均提升 **5.2%**（Table 1）；FAN-PPO 相比标准 PPO 的 OOD 平均提升 **6.2%–7.9%**（Table 2）。真机实验中，FAN-SFT 在空间扰动任务上成功率大幅领先（如 17/30 vs 7/30，Table 3），验证了方法的实际鲁棒性。

**方法定位**：FAN 正则化是一种轻量、即插即用的微调增强技术，可与现有 VLA 骨干（如 OpenVLA、OpenVLA-OFT）及 SFT / PPO 训练流程无缝集成。相比标签平滑等传统正则化，FAN 显式建模了动作空间的几何结构，在泛化能力和样本效率上均展现出显著优势。

### 视觉-语言-动作模型的微调范式

视觉-语言-动作（VLA）模型将机器人操控建模为指令条件化的马尔可夫决策过程，通过大规模预训练获得视觉感知与语言理解能力，再在下游任务上进行微调以适应特定场景。当前主流的微调范式分为两个阶段：

- **监督微调（SFT）**：在专家演示数据上最大化动作的对数似然，损失函数为负对数似然：

  $$\mathcal { L } _ { \mathrm { S F T } } ( \theta ) = - \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \sum _ { t = 0 } ^ { K ^ { i } - 1 } \log \pi _ { \theta } ( a _ { t } ^ { i } | s _ { t } ^ { i } , l ^ { i } )$$

  该范式直接继承自语言模型的训练方式，将动作离散化为 token 序列进行逐 token 的交叉熵优化。

- **强化微调（RFT）**：在 SFT 暖启动后，通过在线交互收集经验，使用 PPO 等策略梯度方法优化奖励信号。典型流程以 **RL4VLA** 为代表，利用截断的重要性采样比率和广义优势估计（GAE）来更新策略。

### 核心瓶颈：忽视物理动作的容错结构

上述微调范式存在一个根本性问题：它们机械地照搬了语言模型的训练逻辑，却忽略了物理动作与语言 token 之间的本质差异。

在语言模型中，一个 token 的预测错误（如将“猫”预测为“狗”）通常意味着语义的完全偏离，因此 one-hot 交叉熵的“精确匹配”导向是合理的。然而，在机器人操控中，**动作空间具有内在的局部平滑性和容错性**——抓取位置偏离最优解几毫米、关节角度偏差几度，往往仍然能够成功完成任务。也就是说，物理动作存在一个**可行动作邻域（Feasible Action Neighborhood, FAN）**，在此邻域内的动作虽然与专家演示不完全一致，但同样是有效的。

标准的 SFT 损失强制模型将概率质量集中在单一专家动作上，导致策略分布极度尖锐、窄峰化。如 **Figure 1(a)** 所示，SFT 暖启动后的策略分布呈现极窄的单峰形状，FAN 覆盖范围极小。这种过拟合于演示动作的策略在面对视觉扰动、语义变化或执行误差时泛化能力严重不足——分布内成功率仅为 48.4%。

随后的 PPO 微调虽然通过探索机制在一定程度上拓宽了策略分布（**Figure 1(b)**，成功率提升至 93.8%），但这种拓宽是隐式的、无结构的，缺乏对 FAN 几何形状的显式建模引导，导致样本效率低下且最终策略的分布形态并非最优。

### 本文动机：显式建模可行动作邻域先验

基于以上分析，本文的核心动机是：**将物理动作空间的局部容错性显式地编码为微调过程中的结构化先验**，引导策略分布朝着以最优动作为中心、具有一定宽度的平滑形状演化，而非追求对单一演示动作的精确复现。

具体而言，本文提出将 FAN 建模为以策略模式为中心的局部单峰平滑区域——即高斯分布，并通过 KL 散度正则化项强制策略输出分布向该目标形状靠拢。这一设计的直觉在于：

- 高斯形状天然捕捉了“中心最优、偏差容忍”的物理动作特性；
- 显式的分布形状引导比隐式的探索更高效，能同时提升微调的泛化能力和样本效率；
- 该正则化项可无缝集成到 SFT 和 PPO 两种微调范式中，形成 **FAN-SFT** 和 **FAN-PPO** 两种算法变体。

### 方法谱系与知识库定位

本工作处于 VLA 微调与策略正则化的交叉点，与以下基线方法形成对比：

| 方法 | 核心机制 | 与 FAN 的关系 |
|------|----------|---------------|
| **OpenVLA + SFT** | 标准负对数似然微调 | 无正则化，策略分布极窄 |
| **RL4VLA / OpenVLA + PPO** | 在线强化微调，隐式拓宽分布 | 无显式 FAN 引导 |
| **OpenVLA-OFT + PPO** | 动作分块模型的强化微调 | 无显式 FAN 引导 |
| **Label Smoothing** | 软化 one-hot 目标标签 | 均匀平滑，未建模空间结构 |
| **FAN-SFT / FAN-PPO（本文）** | KL 散度引导策略分布向高斯形状靠拢 | 显式建模 FAN 几何先验 |

与标签平滑等通用正则化手段不同，FAN 正则化利用了物理动作空间的几何结构——高斯分布的中心位于策略模式、协方差反映局部容错范围，从而提供了一种**领域感知的、结构化的**正则化信号。理论分析（Proposition 1）进一步表明，带有 FAN 先验的最优策略更新可分解为旧策略、高斯先验和 Q 值三者的几何插值，揭示了该正则化在信任域约束下的合理性与可解释性。

## 核心方法与创新机理

### 问题根因：VLA 微调中的分布崩溃与泛化瓶颈

当前视觉-语言-动作（VLA）模型的微调范式直接继承了大语言模型的训练目标——SFT 阶段使用 one-hot 交叉熵最大化专家动作的似然，RFT 阶段使用 PPO 优化稀疏奖励。然而，这种范式忽略了一个关键事实：**物理动作空间具有天然的局部容错性**。在给定状态下，存在一个以最优动作为中心的连通邻域，其中的动作虽然与专家演示不完全一致，但都能成功完成任务。本文将这一邻域形式化定义为**可行动作邻域**（Feasible Action Neighborhood, FAN）。

SFT 暖启动后的策略分布呈现出极度尖锐的单峰形态（Figure 1a），模型几乎将所有概率质量集中在离散化动作空间中的单个 bin 上，导致 FAN 极小。此时分布内成功率仅为 **48.4%**，模型对视觉扰动、语义变化和执行偏差极为敏感。虽然随后的 PPO 微调通过探索奖励信号使分布变宽，将成功率提升至 **93.8%**（Figure 1b），但这一过程是**隐式且低效**的——PPO 需要大量在线交互才能逐步“发现”动作空间的容错结构。

### 核心洞察：用高斯先验显式塑造可行动作邻域

本文的核心洞察是：**将策略输出分布塑造成以当前策略模式为中心的高斯形状，可以直接捕捉物理动作空间的局部平滑容错性**。这一设计背后的因果关系链条如下：

1. **FAN 的几何代理**：在离散化动作空间中，策略分布的形状反映了模型对 FAN 的隐式认知。一个宽而平滑的分布对应一个大的 FAN，意味着模型允许在最优动作附近的一定偏差。
2. **高斯先验的归纳偏置**：高斯分布天然满足“局部单峰、平滑衰减”的性质，恰好匹配物理动作空间的容错结构——越接近最优动作，成功概率越高；越远离，成功概率越低。
3. **显式正则化 vs 隐式探索**：与其让 PPO 通过大量试错隐式地拓宽分布，不如直接在损失函数中注入 FAN 先验，引导策略分布主动向目标高斯靠拢。

### 方法创新：FAN 引导的正则化框架

基于上述洞察，本文提出 **FAN 引导的正则化**（FAN-guided Regularization），将可行动作邻域先验显式注入 VLA 微调的 SFT 和 RFT 两个阶段。其核心是一个统一的 KL 散度正则项：

$$\mathcal { L } _ { \mathrm { F A N } } = \mathbb { E } _ { s } \left[ D _ { \mathrm { K L } } ( \pi ( \cdot | s ) \| \mathcal { N } ( \cdot | \mu ( s ) , \Sigma ( s ) ) ) \right]$$

该正则项强制策略分布 $\pi(\cdot|s)$ 向以 $\mu(s)$ 为中心、$\Sigma(s)$ 为协方差的目标高斯分布靠拢。**$\mu(s)$ 取当前策略的模式（即 argmax 动作），而非专家动作**，这使得正则化是“分布形状引导”而非“动作目标牵引”，保留了模型对最优动作的学习自由度。

#### Changed Slot 1：SFT 阶段的自适应协方差

在标准 SFT 的负对数似然损失基础上，FAN-SFT 引入加权 KL 正则项：

$$\mathcal { L } _ { \mathrm { F A N - S F T } } ( \theta ) = - \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \sum _ { t = 0 } ^ { K ^ { i } - 1 } \Big ( \log \pi _ { \theta } ( a _ { t } ^ { i } | s _ { t } ^ { i } , l ^ { i } ) + \alpha D _ { \mathrm { K L } } \big ( \pi _ { \theta } ( \cdot | s _ { t } ^ { i } , l ^ { i } ) \| \mathcal { N } ( \cdot | \mu ( s _ { t } ^ { i } ) , \Sigma ( s _ { t } ^ { i } ) ) \big ) \Big )$$

其中协方差采用**自适应计算**：$\Sigma(s) = \operatorname{diag}\left( \sum_{a \in A} \pi(a|s,l) (a - \mu(s))^2 \right)$，即策略分布自身的方差。这一设计的优势在于：当策略尚未收敛时，分布较宽，目标高斯也相应较宽，避免过度约束；随着训练进行，分布自然收窄，正则化强度自动减弱。

#### Changed Slot 2：RFT 阶段的固定协方差

在 PPO 的截断损失中，FAN-PPO 以减法形式集成 KL 正则项：

$$\mathcal { L } _ { \mathrm { F A N - P P O } } ( \boldsymbol { \theta } ) = - \frac { 1 } { K } \sum _ { k = 0 } ^ { K - 1 } \Big [ \operatorname* { m i n } \Big ( I _ { t } ^ { k } \hat { A } ( s _ { k } , a _ { k } , l ) , \mathrm { C l i p } ( I _ { t } ^ { k } , 1 - \epsilon , 1 + \epsilon ) \hat { A } ( s _ { k } , a _ { k } , l ) \Big ) - \alpha D _ { \mathrm { K L } } ( \pi _ { \theta } ( \cdot | s _ { k } , l ) \| \mathcal { N } ( \cdot | \mu ( s _ { k } ) , \Sigma ) ) \Big ]$$

与 SFT 阶段不同，RFT 阶段使用**固定各向同性协方差** $\Sigma = \sigma^2 I$（OpenVLA 取 $\sigma=0.3$，OpenVLA-OFT 取 $\sigma=0.2$）。这是因为 RFT 阶段策略已经在 SFT 暖启动后具有一定结构，固定协方差可以提供稳定的正则化信号，避免自适应协方差在策略剧烈更新时引入不稳定性。

#### Changed Slot 3：正则化系数 $\alpha$ 的调节作用

$\alpha$ 控制 FAN 先验的强度，是连接“模仿专家”与“扩展邻域”两个目标的旋钮：
- **$\alpha=0$**：退化为标准 SFT/PPO，无 FAN 引导
- **$\alpha=1.0$**：FAN-PPO 的最佳设置，在 ManiSkill 上达到最高成功率
- **$\alpha \geq 2.0$**：训练开始不稳定
- **$\alpha \geq 5.0$**：训练崩溃

这一敏感性分析（Figure 26）表明，FAN 先验需要在“保持最优动作精度”与“扩展容错邻域”之间取得平衡。

### 理论支撑：信任域内的最优策略更新

本文进一步给出了带有 FAN 先验和信任域约束的最优策略更新形式（Proposition 1）：

$$\pi _ { t + 1 } ( a \vert s , l ) \propto \mathcal { N } ( a \vert \mu ( s ) , \Sigma ) ^ { \frac { \alpha } { \alpha + \beta ^ { * } } } \pi _ { t } ( a \vert s , l ) ^ { \frac { \beta ^ { * } } { \alpha + \beta ^ { * } } } \times \exp \left( \frac { Q ^ { \pi _ { t } } ( s , a , l ) } { \alpha + \beta ^ { * } } \right)$$

这一闭式解揭示了 FAN-PPO 的几何本质：**新策略是旧策略、高斯先验和 Q 值 Boltzmann 分布三者的几何插值**。$\alpha$ 越大，高斯先验的权重越高，策略越倾向于形成平滑的单峰形状；$\beta^*$（信任域约束的对偶变量）越大，旧策略的权重越高，更新越保守。这种插值机制确保了策略在扩展 FAN 的同时不会偏离已学到的有效行为太远。

### 与基线方法的本质区别

| 方法 | 分布形状引导 | 机制 |
|------|-------------|------|
| 标准 SFT | 无 | 仅最大化专家动作似然，分布极窄 |
| 标签平滑 | 弱 | 在 one-hot 目标上添加均匀噪声，缺乏结构先验 |
| 标准 PPO | 隐式 | 通过探索奖励信号被动拓宽分布 |
| 熵最大化 | 无结构 | 仅鼓励分布均匀化，不引导特定形状 |
| **FAN 正则化** | **显式高斯** | 主动塑造局部单峰平滑分布，匹配物理容错结构 |

消融实验证实了这些区别：FAN-SFT 在 ManiSkill OOD 平均上达到 **63.3%**，而最佳标签平滑仅为 **60.1%**（Table 12）；FAN-PPO 在样本效率上显著优于熵最大化正则化（Figure 28a），达到 90% 训练成功率所需步数从 249 降至 **98**（Table 15）。高斯核平滑的多峰目标正则化也能带来提升，但仍不及单峰高斯先验（Figure 28b），这验证了“局部单峰”假设对当前任务空间的适配性。

本文提出的方法围绕一个核心观察展开：当前 VLA 微调范式直接继承语言模型的训练目标（one-hot 交叉熵或 PPO），忽略了物理动作空间内在的容错性和近等价性，导致策略过度拟合单一演示动作，泛化能力差且样本效率低。为此，作者引入**可行动作邻域（Feasible Action Neighborhood, FAN）** 的概念——在给定状态下，与最优动作具有近等价 Q 值且连通的局部动作集合——并将其建模为一个以策略模式为中心的高斯分布。通过在 SFT 和 RFT 损失中注入 FAN 引导的 KL 散度正则项，强制策略输出分布朝高斯形状靠拢，从而扩大有效的可行动作邻域，使模型不再仅仅追求单一正确动作，而是学习一个允许一定偏差的平滑动作区域。

整体 pipeline 由以下模块串联构成：

1. **预训练 VLA 骨干（OpenVLA / OpenVLA-OFT）**：视觉编码器与语言模型骨干将多模态感官输入（图像、语言指令）映射为离散动作 token 序列，提供初始的策略分布 $\pi_\theta(a|s, l)$。
2. **SFT 阶段（监督微调暖启动）**：在标准负对数似然损失 $\mathcal{L}_{\mathrm{SFT}}$ 的基础上，加入 FAN 正则项 $\mathcal{L}_{\mathrm{FAN}}$，形成 **FAN-SFT** 损失。该正则项计算策略分布与以策略模式 $\mu(s)$ 为中心、方差为自适应协方差 $\Sigma(s)$ 的高斯分布之间的 KL 散度，引导策略在拟合专家动作的同时保持局部平滑。
3. **RFT 阶段（强化微调）**：在 SFT 暖启动后，引入基于 PPO 的强化微调。**FAN-PPO** 将 FAN KL 正则项集成到 PPO 截断损失中，目标高斯采用固定各向同性协方差 $\Sigma = \sigma^2 I$（OpenVLA 取 $\sigma=0.3$，OpenVLA-OFT 取 $\sigma=0.2$），以稳定训练并进一步塑造策略分布的高斯几何结构。
4. **值网络**：独立的价值网络 $V_\phi$ 估计状态值函数，为 PPO 提供 GAE 优势估计和值函数回归目标。

**输入输出流**：给定视觉观测 $s$ 和语言指令 $l$，预训练 VLA 骨干输出离散动作空间上的策略分布 $\pi_\theta(\cdot|s,l)$。在 SFT 阶段，该分布与专家动作 $a_t^i$ 计算负对数似然，同时与目标高斯计算 KL 散度，二者加权求和（系数 $\alpha$）形成最终 FAN-SFT 损失。在 RFT 阶段，策略与环境交互收集轨迹，PPO 损失基于截断重要性采样比率和优势函数更新策略，FAN 正则项作为附加项引导分布形状。最终，策略分布被塑造成以最优动作为中心的高斯形状，其宽度由 $\alpha$ 和 $\sigma$ 控制，对应物理动作空间的容错邻域。

**关键设计选择**：
- SFT 阶段使用**自适应协方差** $\Sigma(s) = \operatorname{diag}\left(\sum_{a \in A} \pi(a|s,l)(a-\mu(s))^2\right)$，使目标高斯宽度随策略当前的不确定性动态调整。
- RFT 阶段切换为**固定协方差**，避免在线交互中协方差估计不稳定导致训练崩溃。
- 正则化系数 $\alpha$ 控制 FAN 先验的强度：SFT 中通常取较小值（如 0.01），RFT 中 $\alpha=1.0$ 表现最佳，但 $\alpha \geq 2.0$ 会导致训练不稳定，$\alpha \geq 5.0$ 则直接崩溃（见 Figure 26 敏感性分析）。

**与基线方法的本质区别**：标准 SFT 和 PPO 均不包含任何分布形状的正则化，策略分布由数据或奖励信号自由驱动；标签平滑（Label Smoothing）虽能缓解过拟合，但仅对目标标签施加均匀噪声，缺乏对动作空间局部结构的建模。FAN 正则化通过显式的高斯先验，直接编码了“动作空间中靠近最优动作的区域同样可行”这一物理先验，从而在根本上改变了策略分布的几何结构（Figure 1 直观展示了 SFT 暖启动的极窄分布、PPO 的宽分布与 FAN-PPO 的高斯形状之间的差异）。

### 问题形式化：可行动作邻域（FAN）

本文的核心概念是**可行动作邻域**（Feasible Action Neighborhood, FAN）。其形式化定义为：对于给定状态 $s$，令最优动作为 $a^{*}(s) = \arg\max_{a \in A} Q(s, a)$，则对于容忍度 $\delta > 0$，FAN 是包含 $a^{*}(s)$ 的最大连通动作集合，该集合内的所有动作 $a$ 满足 $Q(s, a^{*}) - Q(s, a) \leq \delta$。

FAN 捕捉了物理动作空间的一个关键性质：**局部容错性和近等价性**。在真实机器人操作中，偏离专家演示动作一定范围内的动作往往也能完成任务。然而，当前 VLA 微调范式直接继承语言模型的标准训练目标（如 one-hot 交叉熵或 PPO），忽略了这一性质，导致策略过度拟合单一演示动作，泛化能力差且样本效率低。

本文的核心洞察是：**策略输出分布的形状可以作为 FAN 的实用代理**。通过将策略分布塑造成以最优动作为中心的高斯形状，模型能够隐式地学习并利用动作空间的局部平滑容错性。

### 核心正则化项：FAN Regularizer

FAN 引导正则化的核心是将策略分布 $\pi(\cdot|s)$ 与一个目标高斯分布 $\mathcal{N}(\cdot|\mu(s), \Sigma(s))$ 之间的 KL 散度作为附加损失项：

$$ \mathcal{L}_{\mathrm{FAN}} = \mathbb{E}_{s} \left[ D_{\mathrm{KL}} \left( \pi(\cdot|s) \| \mathcal{N}(\cdot|\mu(s), \Sigma(s)) \right) \right] $$

其中：
- $\mu(s)$：目标高斯的均值，取为当前策略分布的**模式**（即概率最大的动作 bin），使高斯中心始终锚定在模型认为的最优动作上。
- $\Sigma(s)$：目标高斯的协方差矩阵，控制容许邻域的宽度，在不同训练阶段采用不同策略（见下文）。

### 监督微调：FAN-SFT

在 SFT 阶段，标准损失为负对数似然（NLL）：

$$ \mathcal{L}_{\mathrm{SFT}}(\theta) = -\frac{1}{n} \sum_{i=1}^{n} \sum_{t=0}^{K^{i}-1} \log \pi_{\theta}(a_{t}^{i} | s_{t}^{i}, l^{i}) $$

FAN-SFT 将 FAN 正则项直接加到 SFT 损失上：

$$ \mathcal{L}_{\mathrm{FAN-SFT}}(\theta) = -\frac{1}{n} \sum_{i=1}^{n} \sum_{t=0}^{K^{i}-1} \Big( \log \pi_{\theta}(a_{t}^{i} | s_{t}^{i}, l^{i}) + \alpha \, D_{\mathrm{KL}} \big( \pi_{\theta}(\cdot|s_{t}^{i}, l^{i}) \| \mathcal{N}(\cdot|\mu(s_{t}^{i}), \Sigma(s_{t}^{i})) \big) \Big) $$

其中超参数 $\alpha > 0$ 控制正则化强度。

在 SFT 阶段，协方差矩阵采用**自适应**形式，基于当前策略分布的加权方差：

$$ \Sigma(s) = \operatorname{diag}\left( \sum_{a \in A} \pi(a|s, l) \, (a - \mu(s))^{2} \right) $$

这种自适应协方差的优势在于：训练初期策略分布较宽时，目标高斯也相应较宽，避免过度约束；随着训练收敛，分布收窄，高斯也自动收紧，保持合理的邻域范围。

### 强化微调：FAN-PPO

在 RFT 阶段，标准 PPO 的截断损失为：

$$ \mathcal{L}_{\mathrm{PPO}}(\theta) = -\frac{1}{K} \sum_{k=0}^{K-1} \min\Big( I_{t}^{k} \hat{A}(s_{k}, a_{k}, l), \, \operatorname{Clip}(I_{t}^{k}, 1-\epsilon, 1+\epsilon) \hat{A}(s_{k}, a_{k}, l) \Big) $$

其中 $I_{t}^{k} = \pi_{\theta}(a_{k}|s_{k}, l) / \pi_{\theta_{\mathrm{old}}}(a_{k}|s_{k}, l)$ 为重要性采样比率，$\hat{A}$ 为 GAE 优势估计。

FAN-PPO 将 FAN 正则项集成到 PPO 损失中：

$$ \mathcal{L}_{\mathrm{FAN-PPO}}(\theta) = -\frac{1}{K} \sum_{k=0}^{K-1} \Big[ \min\Big( I_{t}^{k} \hat{A}(s_{k}, a_{k}, l), \, \operatorname{Clip}(I_{t}^{k}, 1-\epsilon, 1+\epsilon) \hat{A}(s_{k}, a_{k}, l) \Big) - \alpha \, D_{\mathrm{KL}} \big( \pi_{\theta}(\cdot|s_{k}, l) \| \mathcal{N}(\cdot|\mu(s_{k}), \Sigma) \big) \Big] $$

与 SFT 阶段不同，RFT 阶段采用**固定各向同性协方差** $\Sigma = \sigma^{2} I$，以保持训练稳定性。对于 OpenVLA 骨干，默认 $\sigma = 0.3$；对于 OpenVLA-OFT 骨干，默认 $\sigma = 0.2$。

### 理论支撑：带 FAN 先验的最优策略更新

论文从信任域约束优化的角度给出了理论分析。在 KL 散度信任域约束下，加入 FAN 先验后的最优策略更新具有如下闭式形式：

$$ \pi_{t+1}(a|s, l) \propto \mathcal{N}(a|\mu(s), \Sigma)^{\frac{\alpha}{\alpha + \beta^{*}}} \; \pi_{t}(a|s, l)^{\frac{\beta^{*}}{\alpha + \beta^{*}}} \times \exp\left( \frac{Q^{\pi_{t}}(s, a, l)}{\alpha + \beta^{*}} \right) $$

这一更新形式揭示了 FAN 正则化的几何本质：新策略是**旧策略、高斯先验与 Q 值指数项三者的几何插值**。$\alpha$ 控制高斯先验的权重，$\beta^{*}$ 为对偶变量，由信任域约束决定。当 $\alpha \to 0$ 时，退化为标准信任域策略更新；当 $\alpha > 0$ 时，高斯先验持续将策略分布拉向以当前最优动作为中心的平滑形状，从而扩大有效的可行动作邻域。

### 关键模块总结

| 模块 | 角色 | 关键公式 |
|------|------|----------|
| VLA 骨干（OpenVLA / OpenVLA-OFT） | 视觉编码 + 语言模型，将感官输入映射为离散动作 token | — |
| SFT Head | 标准监督微调，负对数似然拟合专家动作 | Equation (1) |
| PPO Policy Head | 强化微调策略更新，截断重要性采样优化优势函数 | Equation (3) |
| **FAN Regularizer** | **核心创新**：KL 散度引导策略分布朝高斯形状演化 | Equation (5) |
| Value Network | 估计状态值函数，用于 GAE 优势估计 | Equation (4) |

### 超参数敏感性（需手动验证的要点）

消融实验揭示了 FAN 正则化对关键超参数的敏感性：

- **正则化系数 $\alpha$**：在 FAN-PPO 中，$\alpha = 1.0$ 表现最佳；$\alpha \geq 2.0$ 导致训练不稳定；$\alpha \geq 5.0$ 导致训练崩溃（Figure 26）。
- **目标高斯标准差 $\sigma$**：过小（如 0.05）损害性能；$\sigma \in [0.1, 2.0]$ 范围内结果稳定，默认值 $\sigma = 0.3$（Figure 27）。
- 与**标签平滑**和**熵最大化**等替代正则化方法的对比表明，FAN 的高斯形状先验是性能增益的关键来源，而非简单的分布展宽（Table 12, Figure 28）。

## 实验与关键发现

### 核心实验设计

为系统验证 FAN 引导正则化的有效性，实验覆盖两个主流 VLA 骨干网络——**OpenVLA** 与 **OpenVLA-OFT**，在 **ManiSkill**（PutOnPlateInScene25Main）和 **LIBERO-Spatial** 两个仿真基准上进行 SFT 和 RFT 两阶段评估。所有训练在 NVIDIA A100 80GB GPU 上完成。评估维度包括：分布内成功率、三类 OOD 泛化（视觉扰动 Vision、语义扰动 Semantic、执行扰动 Execution）、样本效率、收敛速度，以及真机空间鲁棒性。

### 监督微调（SFT）主结果

Table 1 给出了 ManiSkill 基准上 SFT 方法的对比。FAN-SFT 在分布内任务上达到 **89.8%**，相比 OpenVLA+SFT 基线的 78.1% 提升 **+11.7 个百分点**；在三类 OOD 任务上的平均成功率为 **63.3%**，领先基线 5.2 个百分点。Figure 2 进一步按 OOD 子任务拆解，显示 FAN-SFT 在视觉、语义和执行扰动下均取得一致增益，验证了高斯形状先验对泛化能力的系统性提升。

![[assets/figures/papers/paper_list_l2377_https_arxiv_org_abs_2604_01570/figures/002_Table_1.jpg]]
*Table 1: Comparison of SFT results on the ManiSkill benchmark. Values denote success rates (%)*

![[assets/figures/papers/paper_list_l2377_https_arxiv_org_abs_2604_01570/figures/003_Figure_2.jpg]]
*Figure 2: SFT performance on OpenVLA with and without FAN-guided regularization across different OOD tasks on ManiSkill*

Figure 3 展示了不同训练数据量下的性能曲线。FAN-SFT 在各数据规模下均优于标准 SFT，且在数据量较小时优势更为明显——说明 FAN 正则化通过扩大可行动作邻域，有效缓解了少样本条件下的过拟合。

![[assets/figures/papers/paper_list_l2377_https_arxiv_org_abs_2604_01570/figures/004_Figure_3.jpg]]
*Figure 3: SFT performance on OpenVLA with and without FAN-guided regularization across different data sizes on in-distribution and three OOD tasks (Vision, Semantic, Execution)*

在 LIBERO-Spatial 基准上，OpenVLA-OFT 配合 FAN-SFT 达到 **98.8%** 成功率，领先 SFT 基线 3.6 个百分点（Section 6.1）。Figure 4 以等高线图可视化空间扰动下的鲁棒性：FAN-SFT 的高成功率区域（红色虚线）显著宽于基线（黑色虚线），直观展示了 FAN 先验对空间扰动的容错能力。

![[assets/figures/papers/paper_list_l2377_https_arxiv_org_abs_2604_01570/figures/006_Figure_4.jpg]]
*Figure 4: Spatial robustness on LIBERO-Spatial, comparing OpenVLA finetuned with SFT (left) versus our FAN-SFT (right). Color indicates success rate; the black and red dashed lines are the equal-success-rate contours for each method, respectively*

### 强化微调（RFT）主结果

Table 2 对比了 RFT 方法在 ManiSkill 上的表现。OpenVLA+FAN-PPO 在分布内达到 **97.4%**，OOD 平均 **88.1%**，分别领先 PPO 基线 1.5 和 6.2 个百分点。OpenVLA-OFT+FAN-PPO 同样展现出一致增益，OOD 平均提升 7.9 个百分点（从 63.3% 到 71.2%）。Figure 6 按 OOD 子任务细分，显示 FAN-PPO 在两类骨干网络上均实现全面超越。

![[assets/figures/papers/paper_list_l2377_https_arxiv_org_abs_2604_01570/figures/007_Table_2.jpg]]
*Table 2: Comparison of RFT results on the ManiSkill benchmark. Values denote success rates (%)*

![[assets/figures/papers/paper_list_l2377_https_arxiv_org_abs_2604_01570/figures/008_Figure_6.jpg]]
*Figure 6: Performance comparison of OpenVLA and OpenVLA-OFT trained with PPO and FAN-PPO across various OOD tasks*

Figure 7 和 Figure 8 的训练曲线揭示了 FAN-PPO 的样本效率优势：OpenVLA 达到 90% 训练成功率所需步数从 249 降至 **98**（Table 15），OpenVLA-OFT 也观察到类似的加速收敛现象。这归因于 FAN 正则化引导策略分布直接朝高斯形状演化，避免了 PPO 从极窄 SFT 分布缓慢展宽的探索过程。

### 真机验证

Table 3 报告了 JAKA 机械臂在物体入盒任务上的真机评估（Figure 9）。在分布内任务（Task-1）上，FAN-SFT 与 SFT 基线均成功（10/10 vs 10/10）。但在引入空间扰动后，差距急剧拉大：Task-3（机械臂位姿扰动）中 FAN-SFT 成功 **17/30**，而基线仅 7/30；Task-4（物体初始位姿扰动）中 FAN-SFT 成功 15/30，基线仅 8/30。Figure 30 的定性 rollout 显示，FAN-SFT 在扰动下仍能平稳完成抓取-放置序列，而基线则出现抓取失败或放置偏移。

### 消融研究

**与标签平滑对比**。Table 12 将 FAN-SFT 与多种标签平滑策略对比。最佳标签平滑配置在 ManiSkill OOD 平均上仅达 60.1%，而 FAN-SFT 达到 63.3%，证明高斯形状引导比简单的概率质量重分配更有效。

**与熵最大化及高斯核平滑对比**。Figure 28 比较了 FAN-PPO 与熵最大化正则化（EM）和高斯核平滑正则化。FAN-PPO 在样本效率和最终性能上均优于 EM（Figure 28a）；高斯核平滑的多峰目标正则化虽带来提升，但仍不及单峰高斯先验的 FAN 正则化（Figure 28b），验证了局部单峰假设在实验任务上的适用性。

**超参数敏感性**。Figure 26 分析了正则化系数 α 的影响：α=1.0 表现最佳，α≥2.0 导致训练不稳定，α≥5.0 导致策略崩溃。Figure 27 分析了目标高斯标准差 σ 的影响：σ 过小（如 0.05）损害性能，σ 在 [0.1, 2.0] 范围内结果稳定，默认值 σ=0.3（OpenVLA）和 σ=0.2（OpenVLA-OFT）为合理选择。

### 失败模式与局限性

FAN 正则化基于动作空间局部单峰平滑的高斯先验假设。当任务存在多个离散的可行区域（如需要截然不同的抓取策略）时，单峰高斯可能无法覆盖所有可行模式，导致性能受限。这一局限性在高斯核平滑消融（Figure 28b）中已有初步体现——多峰目标虽不及单峰高斯，但仍有提升，暗示更灵活的先验形式值得探索。

此外，FAN-PPO 对 α 和 σ 敏感，需仔细调参以避免训练崩溃（Figure 26）。当前实验集中在 ManiSkill 和 LIBERO 仿真环境及单一真机任务，在更广泛的机器人平台和任务类型上的泛化性有待进一步验证。FAN 正则化依赖动作空间的离散化（bin 划分），向连续动作空间的扩展尚未在本文探讨。

## 定位与知识库关联

### 问题定位：VLA 微调中的分布坍缩与泛化瓶颈

当前视觉-语言-动作（VLA）模型的微调范式直接继承自语言模型的训练方法——监督微调（SFT）使用 one-hot 交叉熵损失，强化微调（RFT）则采用 PPO 等策略优化算法。这一继承忽略了一个关键差异：**物理动作具有内在的容错性和近等价性**，即最优动作周围存在一个“可行动作邻域”（Feasible Action Neighborhood, FAN），其中的动作虽然与专家演示不完全一致，但同样能成功完成任务。

在标准 SFT 下，模型被强制拟合单一的专家动作序列，导致策略分布极度尖锐、熵极小。如 Figure 1(a) 所示，SFT 暖启动后的策略分布呈现窄峰状，FAN 几乎为零，成功率仅 48.4%。这种过拟合使得模型在分布外（OOD）场景下泛化能力极差。随后的 PPO 微调通过试错探索在一定程度上拓宽了分布（Figure 1(b)），将成功率提升至 93.8%，但这一拓宽过程是无结构的，样本效率低下。

本文的核心洞察是：**将策略输出分布塑造成以最优动作为中心的高斯形状，能够显式建模物理动作空间的局部平滑容错性**，使模型学习一个允许合理偏差的动作邻域，从而在微调阶段同时提升泛化能力和样本效率。

### 方法谱系：FAN 正则化在 VLA 微调生态中的位置

#### 与监督微调基线的关系

FAN-SFT 在标准 SFT 的负对数似然损失基础上引入 KL 散度正则项：

$$
\mathcal { L } _ { \mathrm { F A N - S F T } } ( \theta ) = - \frac { 1 } { n } \sum _ { i = 1 } ^ { n } \sum _ { t = 0 } ^ { K ^ { i } - 1 } \Big ( \log \pi _ { \theta } ( a _ { t } ^ { i } | s _ { t } ^ { i } , l ^ { i } ) + \alpha D _ { \mathrm { K L } } \big ( \pi _ { \theta } ( \cdot | s _ { t } ^ { i } , l ^ { i } ) \| \mathcal { N } ( \cdot | \mu ( s _ { t } ^ { i } ) , \Sigma ( s _ { t } ^ { i } ) ) \big ) \Big )
$$

其中目标高斯以策略当前模式 $\mu(s)$ 为中心，协方差 $\Sigma(s)$ 采用自适应计算：$\Sigma(s) = \operatorname{diag}(\sum_{a \in A} \pi(a|s,l)(a-\mu(s))^2)$。这一设计与 **Label Smoothing**（标签平滑）有本质区别：标签平滑将概率质量均匀扩散到所有动作，缺乏对动作空间几何结构的建模；而 FAN 正则化通过高斯形状先验，将概率质量集中在最优动作的局部邻域内，保留了动作空间的拓扑信息。消融实验（Table 12）证实，FAN-SFT 在 ManiSkill OOD 平均上达到 63.3%，而最佳标签平滑配置仅 60.1%，验证了结构化先验的优势。

#### 与强化微调基线的关系

FAN-PPO 将 FAN 正则项集成到 PPO 的截断损失中：

$$
\mathcal { L } _ { \mathrm { F A N - P P O } } ( \boldsymbol { \theta } ) = - \frac { 1 } { K } \sum _ { k = 0 } ^ { K - 1 } \Big [ \operatorname* { m i n } \Big ( I _ { t } ^ { k } \hat { A } ( s _ { k } , a _ { k } , l ) , \mathrm { C l i p } ( I _ { t } ^ { k } , 1 - \epsilon , 1 + \epsilon ) \hat { A } ( s _ { k } , a _ { k } , l ) \Big ) - \alpha D _ { \mathrm { K L } } ( \pi _ { \theta } ( \cdot | s _ { k } , l ) | | \mathcal { N } ( \cdot | \mu ( s _ { k } ) , \Sigma ) ) \Big ]
$$

与标准 PPO 相比，FAN-PPO 的关键差异在于目标分布的设计：RFT 阶段采用固定各向同性协方差 $\Sigma = \sigma^2 I$（OpenVLA 使用 $\sigma=0.3$，OpenVLA-OFT 使用 $\sigma=0.2$），以保证训练稳定性。这一选择基于以下观察：RFT 阶段策略已在 SFT 暖启动后具有一定结构，固定的高斯先验足以引导分布向鲁棒形状演化。

从理论角度看，Proposition 1 给出了带有信任域约束和 FAN 先验的最优策略更新形式：

$$
\pi _ { t + 1 } ( a \vert s , l ) \propto \mathcal { N } ( a \vert \mu ( s ) , \Sigma ) ^ { \frac { \alpha } { \alpha + \beta ^ { * } } } \pi _ { t } ( a \vert s , l ) ^ { \frac { \beta ^ { * } } { \alpha + \beta ^ { * } } } \times \exp \left( \frac { Q ^ { \pi _ { t } } ( s , a , l ) } { \alpha + \beta ^ { * } } \right)
$$

该更新可解释为旧策略、高斯先验和 Q 值三者的几何插值，其中 $\alpha$ 控制高斯先验的强度，$\beta^*$ 为信任域约束的拉格朗日乘子。这一形式揭示了 FAN-PPO 与 **RL4VLA**（基于 PPO 的 VLA 强化微调基线）的本质区别：RL4VLA 仅依赖 Q 值引导策略更新，而 FAN-PPO 显式注入了动作空间的几何先验，使策略更新具有了结构化的方向性。

#### 与其他正则化技术的对比

FAN 正则化与两类常见正则化方法形成对比：

1. **熵最大化（Entropy Maximization）**：鼓励策略分布均匀化，但忽略了动作空间的几何结构。Figure 28a 显示，FAN-PPO 在样本效率和最终性能上均优于熵最大化正则化，因为后者将概率质量无差别地扩散到整个动作空间，包括那些明显不可行的区域。

2. **高斯核平滑（Gaussian-Kernel Smoothing）**：对多峰目标分布进行平滑处理也能带来一定提升（Figure 28b），但仍不及 FAN 正则化的高斯先验。这表明，**显式塑造单峰高斯形状比简单平滑多峰分布更有效**，因为前者直接编码了“动作空间局部单峰平滑”这一归纳偏置。

### 适用边界与关键假设

FAN 正则化的有效性建立在以下假设之上，这些假设同时划定了方法的适用边界：

1. **动作空间局部单峰假设**：FAN 先验假设每个状态下的可行动作邻域是连通的、单峰的，可以用以最优动作为中心的高斯分布近似。这一假设在抓取、放置等操作任务中成立，但在存在多个离散可行区域的任务（如需要绕过障碍物的复杂运动规划）中可能失效。此时，高斯先验可能将概率质量错误地集中在不可行的中间区域。

2. **动作空间离散化依赖**：当前 FAN 正则化依赖于动作空间的 bin 划分（离散动作 tokens），KL 散度在离散分布上计算。对于连续动作空间的直接扩展（如与扩散策略结合）尚未在本文中探讨，这限制了方法在连续控制场景下的直接应用。

3. **超参数敏感性**：FAN-PPO 对正则化系数 $\alpha$ 和目标标准差 $\sigma$ 较为敏感。Figure 26 显示，$\alpha=1.0$ 表现最佳，$\alpha \geq 2.0$ 导致训练不稳定，$\alpha \geq 5.0$ 直接导致训练崩溃。Figure 27 表明，$\sigma$ 过小（如 0.05）会损害性能，$\sigma$ 在 [0.1, 2.0] 范围内结果相对稳定。这种敏感性意味着在不同任务和模型规模上部署时需要仔细调参，增加了实际应用的工程负担。

4. **验证范围有限**：实验主要在模拟环境（ManiSkill, LIBERO-Spatial）和单一真机抓取任务上进行，尚未在更广泛的机器人平台、任务类型和动态环境中验证。特别是，在真实人机交互或非结构化动态环境下的鲁棒性仍属未知。

### 局限与开放问题

#### 已识别的局限

1. **高斯先验的表达能力上限**：单峰高斯分布可能无法捕捉某些任务中多模态的可行动作结构。当最优动作邻域呈现多峰或非对称形状时，强制拟合高斯分布可能引入系统性偏差。

2. **训练稳定性与超参数耦合**：FAN-PPO 的稳定性依赖于 $\alpha$ 和 $\sigma$ 的精细协调。过大的 $\alpha$ 导致高斯先验主导更新，压制了 Q 值的信息；过小的 $\sigma$ 则退化为近似点估计，丧失邻域建模能力。当前缺乏自适应的超参数调节机制。

3. **与预训练阶段的割裂**：FAN 正则化仅在微调阶段应用，未探索在 VLA 大规模预训练阶段引入类似先验的可能性。预训练阶段学习到的表征可能已经隐含了动作空间的几何结构，如何利用这一结构来设计更有效的预训练目标仍是一个开放问题。

#### 值得探索的开放问题

1. **超越高斯先验的正则化形式**：探索多峰目标分布（如高斯混合模型）或非参数密度估计作为 FAN 先验，以应对复杂动作空间中的多模态可行动作邻域。Figure 28b 的高斯核平滑实验已初步验证了这一方向的可能性，但性能仍不及单峰高斯先验，提示需要更精细的多峰建模策略。

2. **连续动作空间的扩展**：将 FAN 先验与连续动作表示（如扩散策略、动作分块预测）结合，可能带来更细粒度的动作邻域建模。扩散模型的去噪过程天然具有将分布引导向目标形状的能力，与 FAN 先验的分布塑造目标高度契合。

3. **大规模预训练中的 FAN 先验**：将 FAN 正则化扩展到多任务 VLA 预训练阶段，可能从源头塑造模型的策略分布结构，使微调阶段获得更好的初始化。这需要解决大规模数据下目标高斯参数估计的效率和稳定性问题。

4. **动态环境与交互场景下的鲁棒性**：在真实人机交互或动态障碍物环境中，可行动作邻域可能随时间演化。FAN 先验在此类非稳态场景下的适应性尚未评估，需要设计时变的目标分布或在线自适应机制。

5. **理论性质的深入刻画**：当前 Proposition 1 给出了 FAN 先验下的最优策略更新形式，但对收敛速率、泛化误差界等理论性质的分析尚不充分。建立 FAN 正则化与策略泛化能力之间的定量关系，将有助于指导超参数选择和先验设计。

## 原文 PDF

![[paperPDFs/CVPR_2026/Boosting_Vision_Language_Action_Finetuning_with_Feasible_Action_Neighborhood_Prior.pdf]]
