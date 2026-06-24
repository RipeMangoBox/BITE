---
title: "PP-Motion: Physical-Perceptual Fidelity Evaluation for Human Motion Generation"
type: paper
paper_level: A
venue: ACM MM
year: 2025
pdf_ref: paperPDFs/ACM_MM_2025/PP-Motion_Physical-Perceptual_Fidelity_Evaluation_for_Human_Motion_Generation.pdf
project_link: null
code_link: "https://github.com/Sarah816/PP-Motion"
aliases:
- PM
- PP-Motion
tags:
- ACM_MM_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过强化学习驱动的物理模拟器生成“最近物理可行修正运动”，将其与原始运动的L2距离定义为连续、细粒度的物理保真度标签，并结合Pearson相关损失与人类感知损失联合训练评分网络。
primary_logic: 利用物理模拟器提供客观的连续物理对齐信号，并通过Pearson相关损失让网络学习物理标签的内在趋势，而非绝对数值，从而在无需依赖主观阈值的情况下，使评估指标同时对齐物理规律与人类感知，且二者可相互增强。
claims:
- PP-Motion 在物理相关性指标上大幅超越所有先前指标（例如 MDM 子集上 PLCC 从 MotionCritic 的 0.329 提升至 0.727）。
- PP-Motion 在人类感知对齐准确率上同样略优于专门优化感知的 MotionCritic（85.18% vs 85.07%），证明物理标注可辅助感知对齐。
- 连续物理标注的有效性：与以往粗糙二元标注（如 IFR）相比，细粒度标注提供了更丰富的监督信息。
- Pearson 相关损失相较于 MSE 损失能更好地捕获物理先验，消融实验表明替换为 MSE 导致物理和感知指标均下降。
---

# PP-Motion: Physical-Perceptual Fidelity Evaluation for Human Motion Generation

> [!tip] 核心洞察
> 利用物理模拟器提供客观的连续物理对齐信号，并通过Pearson相关损失让网络学习物理标签的内在趋势，而非绝对数值，从而在无需依赖主观阈值的情况下，使评估指标同时对齐物理规律与人类感知，且二者可相互增强。

| 字段 | 内容 |
|------|------|
| 中文题名 | PP-Motion：面向人体动作生成的物理-感知保真度评估 |
| 英文题名 | PP-Motion: Physical-Perceptual Fidelity Evaluation for Human Motion Generation |
| 会议/期刊 | ACM MM 2025 |
| Links | [paper](https://arxiv.org/abs/2508.08179) · [Code](https://github.com/Sarah816/PP-Motion) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | PP-Motion |
| Dataset | MotionPercept-MDM, MotionPercept-FLAME |

> [!tip] 效果简介
> - MotionPercept-MDM 上，Accuracy (%) 85.18 vs 85.07 (MotionCritic) (+0.11%)；PLCC 0.727 vs 0.329 (MotionCritic) (+0.398)；SROCC 0.622 vs 0.316 (MotionCritic) (+0.306)。
> - MotionPercept-FLAME 上，Accuracy (%) 68.82 vs 67.66 (MotionCritic) (+1.16%)；PLCC 0.657 vs 0.152 (MotionCritic) (+0.505)；SROCC 0.660 vs 0.280 (MotionCritic) (+0.380)。

## 概述

人体动作生成模型近年来取得了显著进展，然而，如何全面评估生成动作的质量仍是一个开放难题。现有评估指标面临一个核心瓶颈：**物理可行性与人类感知无法被单一指标同时兼顾**。一方面，人类标注虽能反映感知质量，但通常仅提供粗糙的二元判断（“更好/更差”），缺乏细粒度的物理对齐真值；另一方面，基于启发式规则的物理指标（如足部滑动、漂浮、穿透等）仅捕捉局部物理违规，无法提供连续、整体的物理保真度信号。更关键的是，人类感知与物理规律之间存在不一致性——一个在人眼看来自然流畅的动作，在物理模拟器中可能因足部漂浮或动量失衡而跌倒，反之亦然（图1）。这种“感知-物理”鸿沟使得单纯依赖感知标注或物理规则的数据驱动指标难以学习有效的物理先验。

针对上述瓶颈，本文提出 **PP-Motion**，一个同时对齐人类感知与物理规律的细粒度动作保真度评估指标。其核心思路是：利用强化学习驱动的物理模拟器，为每个动作序列生成其“最近物理可行修正运动”，并将原始运动与修正运动之间的 L2 距离作为连续、细粒度的物理保真度标签。在此基础上，PP-Motion 联合优化两个损失函数——基于“更好/更差”动作对的感知损失，以及最大化预测分数与物理标签之间 Pearson 相关系数的相关损失——使网络既能捕获人类偏好，又能学习物理保真度的内在趋势，而无需依赖主观阈值。这种设计使得物理标注信号与感知监督信号相互增强，而非彼此竞争。

实验结果表明，PP-Motion 在物理相关性指标上大幅超越所有先前方法：在 MotionPercept-MDM 子集上，PLCC 从 MotionCritic 的 0.329 提升至 0.727，SROCC 从 0.316 提升至 0.622。同时，在人类感知对齐准确率上，PP-Motion 也略优于专门优化感知的 MotionCritic（85.18% vs 85.07%），验证了物理标注可辅助感知对齐的核心假设。消融实验进一步证实，Pearson 相关损失相较于常规 MSE 损失能更有效地捕获物理先验，且按动作类别分批计算相关损失优于跨类别计算。此外，将 PP-Motion 作为奖励信号微调 MDM 生成模型，可使平均 MPJPE 从 76.06 降至 63.33，展示了该指标在下游任务中的应用潜力。

## 背景与动机

### 人体动作生成评估的核心瓶颈

近年来，基于扩散模型等生成范式的人体动作生成取得了显著进展，然而如何可靠地评估生成动作的质量仍是一个悬而未决的问题。理想的评估指标应同时满足两个维度的要求：**人类感知保真度**——动作在视觉上是否自然、语义是否合理；**物理可行性**——动作是否遵循物理定律，例如不发生滑步、漂浮或地面穿透。

现有评估方案在这两个维度上存在结构性缺陷：

- **人类感知评估的粗糙性**：现有数据驱动的感知评估方法（如 **MotionCritic** (Wang et al., ICLR 2025)）依赖人类标注的“更好/更差”二元比较对进行训练。这类标注虽然直观，但本质上粗糙且主观——标注者只能给出离散的偏好判断，无法提供关于物理可行性的细粒度、客观的连续监督信号。
- **物理评估的启发式局限**：传统物理评估指标（如 **Floating**、**Skating**、**Penetration** (Ugrinovic et al., CVPR 2024) 以及 **PFC** (Wang et al., ICLR 2025)）基于人工设计的启发式规则来检测特定物理异常。这些规则覆盖面有限，难以捕捉复杂的物理违规模式，且无法与人类感知形成有效互补。

### 感知与物理的错位

一个更具根本性的发现是：**人类感知判断与物理可行性之间并非总是一致**。如 Figure 1 所示，一段在视觉上看似自然、语义合理的动作，在物理模拟器中执行时可能因关节力矩不合理而摔倒；反之，一段在人类看来不自然的动作，却可能在模拟器中成功执行。这种错位揭示了单独依赖任一维度进行评估的固有风险，也表明一个理想的评估指标必须能够**同时对齐物理规律与人类感知**。

### 核心动机与解决思路

本文的核心动机在于：**利用物理模拟器提供客观、连续的物理对齐信号，并将其与人类感知二元标注联合训练，使评估网络在无需依赖主观阈值的情况下，同时学习物理规律与人类感知偏好**。

具体而言，本文提出 **PP-Motion** 框架，其关键设计包括：

1. **细粒度物理标注生成**：通过强化学习驱动的物理模拟器，为每一段动作生成“最近物理可行修正运动”，并以原始运动与修正运动之间的 L2 距离作为连续、细粒度的物理保真度标签。这克服了以往二元物理判断（如 IFR）监督信息不足的问题。
2. **Pearson 相关损失**：训练时最大化模型预测与物理标签之间的 Pearson 相关系数，使网络学习物理标签的内在趋势而非绝对数值，从而更稳健地捕获物理先验。
3. **联合训练策略**：将物理相关损失与人类感知损失加权联合优化，使物理标注能够辅助感知对齐，二者相互增强而非彼此冲突。

这一设计使得 PP-Motion 在物理相关性指标上大幅超越所有先前指标（例如 MDM 子集上 PLCC 从 MotionCritic 的 0.329 提升至 0.727），同时在人类感知对齐准确率上亦略优于专门优化感知的 MotionCritic（85.18% vs 85.07%），证明了物理标注可有效辅助感知对齐。

## 核心创新

PP-Motion 的核心创新在于**首次将连续的物理保真度信号与人类感知二元标注统一进同一个评估指标训练框架**，使二者相互增强而非彼此妥协。这解决了此前动作评估领域的一个根本瓶颈：现有指标要么仅依赖启发式物理规则（如滑步、漂浮检测），要么仅拟合粗糙的人类偏好标签，无法同时兼顾物理可行性与感知合理性。

### 瓶颈与因果调控

**真实瓶颈**：人类标注天然粗粒度（通常为“更好/更差”的二元比较），缺乏细粒度、客观的物理对齐真值，导致数据驱动的评估网络难以有效学习物理先验。物理启发式指标虽然客观，但仅覆盖少数物理违规模式，与人类感知的相关性极弱。

**因果调控**：PP-Motion 通过强化学习驱动的物理模拟器，为每一条动作序列生成其“最近物理可行修正运动”，并将原始运动与修正运动之间的 L2 距离定义为**连续、细粒度的物理保真度标签** $e_p = \|\boldsymbol{x} - \boldsymbol{x}'\|_2$（见 Eq. 6）。这一标签不依赖任何主观阈值，而是由物理仿真器客观给出，从而为网络提供了丰富的物理监督信号。

在此基础上，PP-Motion 采用 **Pearson 相关损失**（Eq. 4）而非常规的 MSE 回归损失来学习物理标签。核心洞察在于：物理标签的绝对数值受动作类型、序列长度等因素影响，跨类别直接回归绝对误差会引入噪声；而 Pearson 相关损失仅约束模型预测与物理标签之间的**趋势一致性**，使网络能够跨类别捕捉物理保真度的内在排序关系，大幅提升泛化能力。

### 四个关键 Changed Slots

相较于以 **MotionCritic**（Wang et al., ICLR 2025）为代表的纯感知基线，PP-Motion 在以下四个维度上做出了根本性改变：

| 设计维度 | 基线方案 | PP-Motion 方案 | 作用机制 |
|---------|---------|---------------|---------|
| **物理监督损失函数** | 无物理损失，或使用常规 MSE 回归 | Pearson 相关损失 $\mathcal{L}_{\mathrm{corr}}$ | 学习物理标签的内在趋势而非绝对数值，避免跨类别数值尺度不一致导致的噪声 |
| **物理标注粒度** | 无连续物理标注，或仅使用启发式规则与二元判断 | 基于物理仿真差异的连续 L2 距离标注 | 提供细粒度、客观的物理监督信号，替代粗糙的启发式规则 |
| **训练监督源** | 仅使用人类感知二元标签 | 联合使用人类感知二元标签与物理连续标签 | 物理标注为感知对齐提供额外正则，二者联合训练可相互增强 |
| **物理修正运动获取策略** | 不进行修正，或仅在全数据集进行一次预训练 | 全数据集预训练 + 单序列强化学习微调 | 显著降低修正运动与原始运动的模仿误差，提升物理标签质量（Table 2） |

### 联合训练如何实现“物理-感知互增强”

PP-Motion 的总损失函数为感知损失与相关损失的加权和（Eq. 5）：

$$\mathcal{L} = \mathcal{L}_{\mathrm{percept}} + \lambda \mathcal{L}_{\mathrm{corr}}$$

其中感知损失 $\mathcal{L}_{\mathrm{percept}}$（Eq. 3）采用二元交叉熵形式，鼓励模型对“更好”动作给出更高分数；物理相关损失 $\mathcal{L}_{\mathrm{corr}}$（Eq. 4）最大化预测分数与物理标签的 Pearson 相关系数。

这种联合设计的深层机制在于：物理标签提供了感知标签**缺失的连续排序信息**，帮助网络在感知标注模糊或矛盾的区域建立更稳定的评分曲面；而感知标签则为物理标签提供了**人类视觉偏好的语义锚点**，防止网络过度拟合物理仿真中与视觉质量无关的细微差异。消融实验（Table 7）证实，将 Pearson 相关损失替换为 MSE 损失后，物理相关性指标（MDM 上 SROCC 从 0.622 降至 0.413）和人类感知准确率均显著下降，验证了相关损失对物理先验学习的关键作用。

### 物理标注生成：两阶段策略

物理修正运动的质量直接决定物理标签的可靠性。PP-Motion 采用两阶段策略（详见 Table 2 的定量对比）：

1. **全数据集预训练**：在 MotionPercept 全部子集上训练一个基于 PHC 的物理修正网络 $F_p$，使其学会将任意动作映射为物理可行的运动。
2. **单序列强化学习微调**：对每一条待标注序列，在预训练模型基础上进行独立的强化学习微调，奖励函数（Eq. 8）鼓励修正运动在平移、旋转、线速度和角速度上尽可能贴近原始运动，同时满足物理约束。

Table 2 显示，单序列微调后，MDM-Train、MDM-Val 和 FLAME 三个子集上的重建误差分别从 55.72 mm、55.49 mm、69.20 mm 降至 49.65 mm、50.90 mm、53.76 mm，表明微调显著提升了修正运动与原始运动的贴近程度，从而保证了物理标签的细粒度和准确性。

## 整体框架

PP-Motion 的评估框架围绕一个核心矛盾展开：人类感知与物理可行性并不总是一致（Figure 1）。一个视觉上自然、语义合理的动作可能在物理模拟器中跌倒，反之亦然。因此，框架的设计目标不是偏袒某一方，而是让两类信号在训练中相互增强。

### 训练流水线

整体训练流水线如 Figure 2 所示，由三个关键阶段串联而成：

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_08179/figures/002_Figure_2.jpg]]
*Figure 2: Our metric design and training pipeline. The network takes a human motion sequence as input, which is processed by a motion encoder to extract spatiotemporal features. These features are then decoded into a fidelity score by a fidelity decoder. The network is trained in a supervised fashion using fine-grained physical annotations alongside human perceptual labels*

1. **物理标注生成**：对数据集中每一条动作序列，利用物理修正网络 $F_p$ 在物理模拟器中生成其“最近物理可行修正运动” $\boldsymbol{x}'$，并以原始运动与修正运动之间的 L2 距离 $e_p = \|\boldsymbol{x} - \boldsymbol{x}'\|_2$ 作为连续、细粒度的物理保真度标签（Eq. 6–7）。这一标注是框架的因果旋钮——它将原本粗糙的二元物理判断（如是否漂浮、是否滑步）转化为可微分的连续信号。

2. **特征提取与评分**：动作序列 $\boldsymbol{x}$ 经过一个基于双流注意力结构的 Motion Encoder 提取时空特征，再由 Fidelity Decoder（MLP）解码为保真度分数 $\hat{s} = F(\boldsymbol{x}; \theta)$（Eq. 1）。

3. **联合监督训练**：网络同时接受两类监督——来自人类标注的“更好/更差”二元感知标签，以及上述物理模拟器生成的连续物理标签。总损失函数为感知损失与物理相关损失的加权和（Eq. 5）：
   $$ \mathcal{L} = \mathcal{L}_{\mathrm{percept}} + \lambda \mathcal{L}_{\mathrm{corr}} $$
   其中感知损失 $\mathcal{L}_{\mathrm{percept}}$ 采用二元交叉熵形式，鼓励模型对“更好”动作给出更高分数（Eq. 3）；物理损失 $\mathcal{L}_{\mathrm{corr}}$ 则直接最大化预测分数与物理标签之间的 Pearson 相关系数（Eq. 4），使模型学习物理标注的内在趋势而非绝对数值。

### 模块关系与信息流

框架中各模块的职责与数据流向可概括为：

| 模块 | 输入 | 输出 | 核心作用 |
|------|------|------|----------|
| Physical Correction Network ($F_p$) | 原始动作 $\boldsymbol{x}$ | 物理可行修正动作 $\boldsymbol{x}'$ | 生成物理对齐的参考运动 |
| Physical Annotation Generator | $\boldsymbol{x}, \boldsymbol{x}'$ | 物理保真度标签 $e_p$ | 将物理差异量化为连续监督信号 |
| Motion Encoder | 动作序列 $\boldsymbol{x}$ | 时空特征 | 提取关节级时空表示 |
| Fidelity Decoder | 时空特征 | 保真度分数 $\hat{s}$ | 将特征映射为标量评分 |
| Correlation Loss Module | $\hat{s}, e_p$ | $\mathcal{L}_{\mathrm{corr}}$ | 最大化预测与物理标签的相关性 |

### 关键设计决策

框架中有两个关键设计值得注意：

- **连续物理标注替代启发式规则**：与以往基于启发式规则的二元物理指标（如 Floating、Skating、Penetration）不同，PP-Motion 的物理标签来自模拟器中的 L2 距离，天然连续且细粒度。这为网络提供了更丰富的监督信息，使其能够捕捉肉眼难以分辨的物理差异（如 Figure 4 所示）。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_08179/figures/012_Figure_4.jpg]]
*Figure 4: (a) A MotionPercept better/worse data pair: the motion on the left, annotated as ‘better’ and visually superior, exhibits physics issues (e.g. floating, skating). The motion on the right, annotated as ‘worse’ and visually inferior, shows greater physical plausibility. (b) Three MotionPercept samples in a group, all annotated as ‘worse’ by humans, reveal different physical characteristics in the simulator. Our PP-Motion scores (higher means better) successfully capture these physical distinctions*

- **Pearson 相关损失替代 MSE**：物理标签的绝对数值受模拟器精度、运动类型等因素影响，直接回归数值（MSE）容易过拟合到噪声。Pearson 相关损失只关心预测与标签之间的单调趋势，使网络学到更鲁棒的物理先验。消融实验证实，将 $\mathcal{L}_{\mathrm{corr}}$ 替换为 MSE 会导致物理相关性指标和人类感知准确率双双下降。

整个框架的核心洞察在于：物理模拟器提供客观的连续对齐信号，Pearson 相关损失让网络学习其内在趋势而非绝对数值，从而在无需依赖主观阈值的情况下，使评估指标同时对齐物理规律与人类感知，且二者可相互增强。

## 核心模块与公式推导

PP-Motion 的训练管线由三个核心模块构成：**运动编码器（Motion Encoder）**、**保真度解码器（Fidelity Decoder）** 以及 **物理标注生成器（Physical Annotation Generator）**。其中前两者构成可学习的评分网络 $F(x; \theta)$，后者在训练前离线生成细粒度物理标签，不参与梯度更新。

### 运动编码器与保真度解码器

运动编码器接收人体动作序列 $\boldsymbol{x} \in \mathbb{R}^{T \times J \times D}$（$T$ 帧，$J$ 关节，$D$ 特征维度），通过双流注意力融合模块提取时空特征。每个融合模块包含空间自注意力分支与时间自注意力分支，分别沿关节维度和时间维度建模依赖关系，随后经 MLP 进行跨流融合。该设计沿用了 MotionCritic（Wang et al., ICLR 2025）中的感知评分骨干，但在训练目标上做了根本性扩展。

保真度解码器为一个轻量 MLP，将编码器输出的时空特征映射为标量保真度分数 $\hat{s}$：

$$\hat{s} = F(\boldsymbol{x}; \theta) \tag{1}$$

### 物理标注生成：从仿真差异到连续标签

物理标签的核心思想是：**用物理模拟器生成“最近物理可行修正运动”$\boldsymbol{x}'$，将原始运动 $\boldsymbol{x}$ 与 $\boldsymbol{x}'$ 的 L2 距离定义为连续物理保真度标签**。这一过程分两步：

**Step 1 — 全数据集预训练**：在 MotionPercept 全部三个子集（MDM-Train、MDM-Val、FLAME）上预训练物理修正网络 $\boldsymbol{F}_p$，使其学会将任意运动映射为模拟器可执行的版本：

$$\boldsymbol{x}' = \boldsymbol{F}_p(\boldsymbol{x}) \tag{7}$$

$\boldsymbol{F}_p$ 基于 PHC（Perpetual Humanoid Control）框架，通过强化学习训练，逐帧奖励函数鼓励修正运动在平移、旋转、线速度和角速度上贴近原始运动，同时满足物理约束：

$$r_t = w_{jp} e^{-100 \|\boldsymbol{p}_t' - \boldsymbol{p}_t\|} + w_{jr} e^{-10 \|\boldsymbol{q}_t' \ominus \boldsymbol{q}_t\|} + w_{jv} e^{-0.1 \|\boldsymbol{v}_t' - \boldsymbol{v}_t\|} + w_{j\omega} e^{-0.1 \|\boldsymbol{\omega}_t' - \boldsymbol{\omega}_t\|} \tag{8}$$

**Step 2 — 单序列强化学习微调**：对每个动作序列单独微调修正网络，使 $\boldsymbol{x}'$ 尽可能贴近原始运动的同时保持物理可行性。Table 2 显示，单序列微调后的重建误差（Recon. Err.）在 MDM-Train 上从 55.72 mm 降至 49.65 mm，FLAME 上从 69.20 mm 降至 53.76 mm，证明微调显著提升了修正运动的模仿精度。

最终物理保真度标签定义为：

$$e_p = \|\boldsymbol{x} - \boldsymbol{x}'\|_2 \tag{6}$$

$e_p$ 越大，表示原始运动越偏离物理可行域，物理保真度越低。与 MotionCritic 中粗糙的二元感知标签（“更好/更差”）不同，$e_p$ 是连续值，提供了细粒度的监督信号（Table 1 对比了两种标注的统计分布差异）。

### 联合训练损失

PP-Motion 的训练目标是最小化感知损失与物理相关损失的加权和：

$$\min_{\theta} \mathcal{L}_{\text{percept}}(F(\boldsymbol{x}; \theta), y_{\text{prec}}) + \lambda \mathcal{L}_{\text{corr}}(F(\boldsymbol{x}; \theta), y_{\text{phy}}) \tag{2}$$

**感知损失** 沿用 MotionCritic 的成对比较范式。对于“更好-更差”动作对 $(\boldsymbol{x}^{(h)}, \boldsymbol{x}^{(l)})$，损失鼓励模型给更好动作分配更高分数：

$$\mathcal{L}_{\text{percept}} = -\mathbb{E}_{(\boldsymbol{x}^{(h)}, \boldsymbol{x}^{(l)})} \left[ \log \sigma \Big( F(\boldsymbol{x}^{(h)}) - F(\boldsymbol{x}^{(l)}) \Big) \right] \tag{3}$$

**物理相关损失** 是 PP-Motion 的关键创新。不同于常规回归任务中使用 MSE 损失直接拟合 $e_p$ 的绝对值，PP-Motion 采用 **Pearson 相关系数损失**，最大化模型预测分数与物理标签之间的线性相关性：

$$\mathcal{L}_{\text{corr}} = -\frac{\sum_{i=1}^{n} (\hat{s}_i - \bar{\hat{s}})(e_{p,i} - \bar{e}_p)}{\sqrt{\sum_{i=1}^{n} (\hat{s}_i - \bar{\hat{s}})^2} \sqrt{\sum_{i=1}^{n} (e_{p,i} - \bar{e}_p)^2}} \tag{4}$$

总损失为：

$$\mathcal{L} = \mathcal{L}_{\text{percept}} + \lambda \mathcal{L}_{\text{corr}} \tag{5}$$

### 设计动机：为什么用相关损失而非 MSE？

这一设计源于对物理标签本质的洞察。$e_p$ 的绝对数值受模拟器参数、动作尺度等因素影响，其绝对值本身并不具备跨序列的可比性——模型真正需要学习的是 **“物理保真度的相对排序”** 这一内在趋势。Pearson 相关损失对标签的线性缩放不敏感，只关注预测与标签之间的单调关系，因此比 MSE 更适合从噪声物理标签中提取有效先验。

消融实验（Table 7）证实了这一设计选择：将 $\mathcal{L}_{\text{corr}}$ 替换为 MSE 损失后，MDM 子集上的 SROCC 从 0.622 降至 0.413，人类感知准确率也同步下降，表明相关损失不仅更好地捕获了物理规律，还通过联合训练反哺了感知对齐能力。此外，按动作提示类别分批计算 PLCC 损失（同类内计算）优于跨类别计算，进一步提升了物理相关性指标。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_08179/figures/001_Figure_1.jpg]]
*Figure 1: A motion that looks realistic does not necessarily mean it is physically feasible. Top-left: Motion appears realistic and semantically meaningful to the human eye, yet fails in physics simulation, resulting in a fall (bottom-left). Top-right: Unnatural motion in human perception executes successfully in simulation (bottom-right). This reveals a discrepancy between human perception and physical laws*

## 实验与分析

PP-Motion 的核心实验围绕两个维度展开：**人类感知对齐**（二元偏好判断准确率）和**物理保真度对齐**（预测分数与物理标注之间的排序相关性 PLCC / SROCC / KROCC）。所有实验均在 MotionPercept 数据集上进行，PP-Motion 仅在 MDM 训练子集上训练，在 MDM 验证子集和 FLAME 子集上直接测试，未对 FLAME 进行微调。

### 主实验结果

Table 3 汇总了 PP-Motion 与现有指标的全面对比。在人类感知准确率上，PP-Motion 在 MotionPercept-MDM 上达到 85.18%，略优于专门优化感知的 **MotionCritic**（Wang et al., ICLR 2025）的 85.07%；在 MotionPercept-FLAME 上，PP-Motion 以 68.82% 领先 MotionCritic 的 67.66%，优势扩大至 +1.16%。这表明**物理标注的引入不仅未损害感知对齐，反而带来了轻微增益**。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_08179/figures/006_Table_3.jpg]]
*Table 3: Quantitative comparison of our metric with previous metrics. We report human perceptual accuracy [72] and physical correlation PLCC [51], SROCC [62], and KROCC [41] on 2 datasets, MotionPercept-MDM and MotionPercept-FLAME. Bold numbers indicate the best results*

物理相关性指标上的差距更为显著。在 MotionPercept-MDM 上，PP-Motion 的 PLCC 达到 0.727，而 MotionCritic 仅为 0.329，提升幅度高达 +0.398；SROCC 从 0.316 提升至 0.622（+0.306），KROCC 从 0.220 提升至 0.461（+0.241）。在 MotionPercept-FLAME 上趋势一致：PLCC 从 0.152 跃升至 0.657（+0.505），SROCC 从 0.280 提升至 0.660（+0.380），KROCC 从 0.188 提升至 0.487（+0.299）。这些结果说明，PP-Motion 成功捕获了生成动作的物理可行性差异，而此前指标对此几乎不具备判别力。

其他基线方法的物理相关性普遍较弱。基于物理启发式规则的指标——**Floating**、**Skating**、**Penetration**（Ugrinovic et al., CVPR 2024）——仅反映单一物理缺陷维度，无法形成综合评估；**PFC**（Wang et al., ICLR 2025）聚焦足部接触，覆盖范围有限；**Joint AE** 仅度量重建误差，与物理保真度的关联微弱。这些方法的 PLCC 和 SROCC 在两张表上均远低于 PP-Motion，进一步验证了连续物理标注与相关损失设计的有效性。

按动作提示类别细分的 PLCC / SROCC / KROCC 结果（Table 4–6）显示，PP-Motion 在 HumanAct12 的 12 个提示类别和 UESTC 的 40 个提示类别上，绝大多数情况下取得最优或次优，表明其物理评估能力在不同动作类型间具有较好的稳定性。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_08179/figures/007_Table_4.jpg]]
*Table 4: Pearson’s Correlation Coefficients (PLCC) results on 12 different prompts on HumanAct12 and on the total 40 prompts of UESTC. HumanAct12 and UESTC are 2 subsets of MotionPercept-MDM. Bold numbers indicate the best results, and underline numbers indicate the second best results*

### 消融实验

Table 7 的消融实验揭示了两个关键设计选择的作用机制。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_08179/figures/010_Table_7.jpg]]
*Table 7: Ablation studies on different loss functions and training strategies*

**Pearson 相关损失 vs. MSE 损失**：将物理损失从 PLCC 相关损失替换为常规 MSE 回归损失后，MotionPercept-MDM 上 SROCC 从 0.622 骤降至 0.413，人类感知准确率也从 85.18% 下降。这表明物理标注的**绝对数值本身噪声较大**（受模拟器初始状态、随机种子等因素影响），直接回归数值会引入误导信号；而 Pearson 相关损失仅约束预测分数与物理标签的**排序趋势一致**，使网络学习到鲁棒的物理先验，且这种先验对感知对齐具有正向迁移效应。

**按提示类别分批计算相关损失**：在训练时按动作提示类别分组计算 PLCC 损失（同类内计算），优于跨类别全局计算。直觉上，不同动作类别（如“走路”与“跳跃”）的物理误差分布差异较大，跨类别混合计算会掩盖类内物理差异的细粒度信号，分批策略则使相关损失更聚焦于同类动作的相对排序。

### 应用验证：以 PP-Motion 为奖励信号微调生成模型

Table 8 展示了将 PP-Motion 作为评估指标嵌入生成模型训练的初步应用。以 MDM 为基础生成模型，使用 PP-Motion 分数作为奖励信号进行微调后，生成动作在物理模拟器中的表现显著改善：平均 MPJPE（模拟运动与真值运动之间的逐关节位置误差）从 76.06 mm 降至 63.33 mm，PP-Motion 预测分数也相应提升。这验证了 PP-Motion 不仅是一个评估工具，也可作为**可微的物理感知反馈信号**指导生成模型向物理可行方向优化。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_08179/figures/011_Table_8.jpg]]
*Table 8: Comparison of MDM model performance before and after finetuning with our metric. PP-Motion is the average predicted score of our metric. Mean MPJPE is the mean perjoint position error between simulated motion and ground truth motion*

### 物理标注质量分析

物理标注的可靠性是 PP-Motion 有效性的前提。Table 2 对比了仅使用全数据集预训练模型与对每条序列进行强化学习微调后的模仿误差。在 MDM-Train、MDM-Val、FLAME 三个子集上，逐序列微调均显著降低了重建误差（如 FLAME 上从 69.20 mm 降至 53.76 mm），MPJPE 和 PA-MPJPE 也有相应改善。这说明“全数据集预训练 + 单序列微调”的两阶段策略能够为每条动作生成更贴近原始运动且物理可行的修正版本，从而提供高质量的连续物理标注。

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_08179/figures/004_Table_2.jpg]]
*Table 2: Quantitative results on imitating motion sequences of MotionPercept, which has three subsets: MDM-Train, MDM-Val, and FLAME. We use pose-based metrics to compare the imitation performance between using only the pretrained model and applying per-sequence fine-tuning. Recon. Err., MPJPE, and PA-MPJPE are measured in millimeters (mm)*

Figure 4 的案例分析进一步佐证了 PP-Motion 的判别能力：(a) 在人类标注为“更好/更差”的动作对中，视觉上更优的动作反而存在漂浮、滑步等物理缺陷，而视觉较差的动作物理可行性更高，PP-Motion 分数正确捕捉了这一反转；(b) 在三个人类均标注为“更差”的动作样本中，PP-Motion 分数仍能区分其物理可行性的细微差异，体现了连续标注相较于二元标注的信息优势。

### 补充图表

![[assets/figures/papers/paper_list_l7_https_arxiv_org_abs_2508_08179/figures/003_Table_1.jpg]]
*Table 1: Annotation statistics on MotionPercept dataset*

## 方法谱系与知识库定位

### 1. 与现有评估范式的继承与分叉

PP-Motion 的核心定位是**弥合人类感知评估与物理可行性评估之间的断裂**。在 PP-Motion 之前，这两类评估方法各自独立发展，且存在显著局限：

**人类感知评估线**：以 **MotionCritic**（Wang et al., ICLR 2025）为代表，通过收集“更好/更差”动作对的人类二元标注，训练一个数据驱动的评分网络。PP-Motion 直接继承了 MotionCritic 的感知损失设计——即公式 $ \mathcal{L}_{\mathrm{percept}} $ 中的二元交叉熵式损失，鼓励模型对标注为“更好”的动作给出更高分数。然而，这一范式的瓶颈在于：人类标注天然是粗粒度的二元标签，无法提供连续的物理对齐真值，导致指标难以有效学习物理先验。

**物理启发式评估线**：以 **PFC**（Wang et al., ICLR 2025）的足部接触指标、以及 **Floating / Skating / Penetration**（Ugrinovic et al., CVPR 2024）等启发式规则为代表。这些方法通过预定义的物理违规检测规则（如漂浮、滑步、穿透）来评估动作质量，但存在两个根本问题：一是规则覆盖不全，无法捕获所有物理违规类型；二是这些规则与人类感知之间缺乏显式对齐机制。

PP-Motion 的分叉点在于：**首次将物理模拟器作为客观的连续监督信号源引入评估指标训练**，而非依赖人工设计的启发式规则。具体而言，它通过强化学习驱动的物理修正网络 $F_p$ 生成“最近物理可行修正运动” $x'$，将原始运动 $x$ 与 $x'$ 之间的 L2 距离定义为连续物理保真度标签 $e_p = \|x - x'\|_2$。这一设计将物理评估从离散的规则判断转化为连续的回归信号，使得物理监督的粒度与信息量大幅提升。

### 2. 关键技术决策的谱系定位

PP-Motion 在以下四个关键槽位上做出了区别于现有工作的选择：

| 设计槽位 | 现有基线做法 | PP-Motion 做法 | 谱系意义 |
|---------|-------------|---------------|---------|
| **物理监督损失函数** | 无物理损失，或使用 MSE 回归损失 | Pearson 相关损失 $\mathcal{L}_{\mathrm{corr}}$ | 从“学习绝对数值”转向“学习内在趋势”，避免了对主观阈值的依赖 |
| **物理标注粒度** | 二元判断（如 IFR）或启发式规则 | 基于物理仿真差异的连续 L2 距离 | 首次将物理评估从分类问题转化为回归问题 |
| **训练监督源** | 仅使用人类感知二元标签 | 联合使用感知二元标签 + 物理连续标签 | 开创了多粒度监督联合训练的范式 |
| **物理修正策略** | 不修正，或仅全数据集预训练一次 | 全数据集预训练 + 单序列 RL 微调 | 在修正精度与计算成本间取得平衡 |

其中，**Pearson 相关损失的选择是最关键的因果旋钮**。消融实验（Table 7）表明，将 $\mathcal{L}_{\mathrm{corr}}$ 替换为 MSE 损失后，物理相关性指标大幅下降（MDM 上 SROCC 从 0.622 降至 0.413），同时人类感知准确率也同步下降。这验证了核心洞察：物理标签的**相对趋势**比**绝对数值**更可靠，因为物理修正本身存在不可避免的残余误差，但不同动作之间“谁更物理可行”的排序关系是稳定的。

### 3. 适用边界与泛化限制

PP-Motion 当前存在以下已验证或待验证的边界：

**训练数据依赖**：PP-Motion 仅在 MotionPercept 的 MDM 子集上训练，在 MDM-Val 和 FLAME 子集上直接测试（未进行 FLAME 微调）。虽然跨子集的物理相关性指标仍大幅领先（FLAME 上 PLCC 达 0.657，远超 MotionCritic 的 0.152），但 FLAME 上的感知准确率绝对水平较低（68.82%），表明**不同生成模型产生的动作分布差异仍会影响指标的感知对齐能力**。其在真实运动捕捉数据上的泛化表现尚未验证。

**物理标注的计算开销**：物理标注生成需要两阶段流程——先在整个数据集上预训练物理修正网络，再对每个序列单独进行强化学习微调。Table 2 显示，单序列微调比仅使用预训练模型显著降低重建误差（FLAME 上从 69.20mm 降至 53.76mm），但这种逐序列优化的计算成本限制了标注向更大规模数据集的扩展。

**损失融合的简单性**：当前联合训练仅使用加权和 $\mathcal{L} = \mathcal{L}_{\mathrm{percept}} + \lambda \mathcal{L}_{\mathrm{corr}}$，未探索物理监督与感知监督之间更深层的交互机制（如对比学习或知识蒸馏）。这是否限制了物理先验向感知对齐的传递效率，尚需进一步研究。

### 4. 开放问题与后续工作方向

1. **跨域泛化验证**：PP-Motion 主要基于 MDM 生成的动作进行训练和评估，其在其他生成模型（如 FLAME、MDM 的不同版本）以及真实运动捕捉数据上的泛化能力尚待系统验证。这是该指标能否成为通用评估标准的关键。

2. **标注成本压缩**：物理标注生成的计算开销（全数据集预训练 + 单序列 RL 微调）限制了向大规模数据集的扩展。可能的改进方向包括：利用更高效的物理修正策略（如蒸馏预训练模型）、或通过主动学习仅对关键样本进行精细标注。

3. **物理-感知交互深化**：当前联合训练仅简单加权两个损失，是否存在更巧妙的交互方式进一步强化物理与感知的对齐？例如，利用物理标签作为对比学习中的排序信号，或通过知识蒸馏让感知分支从物理分支中提取结构先验。

4. **物理标注的因果性**：PP-Motion 的物理标签本质上是“物理修正距离”，而非“物理违规程度”。两者在多数情况下正相关，但可能存在反例（如动作本身物理可行但修正网络引入了额外偏差）。如何解耦修正网络的自身误差与真实物理违规信号，是提高标注质量的潜在方向。

## 原文 PDF

![[paperPDFs/ACM_MM_2025/PP-Motion_Physical-Perceptual_Fidelity_Evaluation_for_Human_Motion_Generation.pdf]]