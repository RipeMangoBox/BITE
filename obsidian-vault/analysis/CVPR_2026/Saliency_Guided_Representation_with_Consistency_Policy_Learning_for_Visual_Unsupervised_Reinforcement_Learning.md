---
title: Saliency-Guided Representation with Consistency Policy Learning for Visual Unsupervised Reinforcement Learning
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Saliency_Guided_Representation_with_Consistency_Policy_Learning_for_Visual_Unsupervised_Reinforcement_Learning.pdf
project_link: null
code_link: null
aliases:
- SSGRCPL
- SGRCPLVURL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/representation_self_supervised_transfer
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过显著性引导的动态表示学习将表示与SR目标解耦，同时引入一致性策略与URL特定的无分类器引导，是提升后继度量质量和技能可控性、从而改进泛化的关键操作柄。
primary_logic: 将表示学习与后继训练分离，利用基于后继值函数梯度的显著性图强制编码器聚焦于动态相关特征；并采用一致性扩散策略实现单步高效的多模态动作建模，通过无分类器引导在技能多样性与可控性之间取得平衡。
claims:
- Figure 2显示SR方法在视觉输入下泛化性能急剧下降，且注意力热力图集中在任务无关区域。
- Figure 3表明HILP-pixel的值-回报Spearman相关性显著低于HILP-state和HILP-SDE-pixel，说明次优表示主要损害后继度量而非基础特征。
- Table 1全面对比显示SRCP在Walker、Quadruped、Cheetah域平均性能分别超出当时最佳方法13%、33%和11%。
- Table 2消融实验证实移除显著性动态编码器或一致性策略均导致性能下降，两者结合达到最优。
---

# Saliency-Guided Representation with Consistency Policy Learning for Visual Unsupervised Reinforcement Learning

> [!tip] 核心洞察
> 将表示学习与后继训练分离，利用基于后继值函数梯度的显著性图强制编码器聚焦于动态相关特征；并采用一致性扩散策略实现单步高效的多模态动作建模，通过无分类器引导在技能多样性与可控性之间取得平衡。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于显著性引导表示与一致性策略学习的视觉无监督强化学习 |
| 英文题名 | Saliency-Guided Representation with Consistency Policy Learning for Visual Unsupervised Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.05931) |
| Topic | #topic/vision_multimodal_applications #topic/representation_self_supervised_transfer #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SRCP (Saliency-Guided Representation with Consistency Policy Learning) |
| Dataset | ExORL Walker, ExORL Quadruped, ExORL Cheetah, ExORL Jaco |

> [!tip] 效果简介
> - ExORL Walker (4 tasks average) 上，平均回报 (average return) 453 vs 238 (HILP) (+215)。
> - ExORL Quadruped (4 tasks average) 上，平均回报 355 vs 232 (HILP) (+123)。
> - ExORL Cheetah (4 tasks average) 上，平均回报 543 vs 454 (HILP) (+89)。

## 概述

视觉无监督强化学习（URL）旨在无需任务奖励的预训练阶段，让智能体习得可跨任务泛化的技能。基于后继表示（Successor Representation, SR）的方法在低维状态输入下表现出色，但在高维视觉输入下泛化性能急剧下降。**Figure 2** 显示，SR 方法在视觉 URL 中性能大幅衰减，且注意力热力图集中在任务无关区域，说明编码器未能捕获动态相关特征。

本文揭示核心瓶颈：传统 SR 方法将编码器与 SR 目标端到端联合优化，导致学习到的视觉表示偏向与动态无关的区域，进而使后继度量估计不准，并削弱技能条件策略对多模态动作分布的表达能力与技能可控性，最终限制零样本泛化性能。

针对上述问题，本文提出 **SRCP（Saliency-Guided Representation with Consistency Policy Learning）**，核心思路是将表示学习与后继训练解耦，并引入一致性扩散策略实现高效的多模态动作建模。SRCP 包含两个关键创新：

- **显著性引导的动态表示学习**：利用基于后继值函数梯度的显著性图，强制编码器聚焦于动态相关区域，将表示学习目标与 SR 目标解耦。
- **一致性策略与无分类器引导**：采用一致性模型作为技能条件策略，通过 URL 特定的无分类器引导，在技能多样性与可控性之间取得平衡，同时以单步推理实现高效动作生成。

实验验证了问题诊断与方法的有效性。**Figure 3** 表明，HILP-pixel 的值-回报 Spearman 相关性显著低于 HILP-state 和 HILP-SDE-pixel，证实次优表示主要损害后继度量而非基础特征。**Table 1** 的全面对比显示，SRCP 在 Walker、Quadruped、Cheetah 域的平均性能分别超出当时最佳方法 13%、33% 和 11%。**Table 2** 的消融实验进一步证实，移除显著性动态编码器或一致性策略均导致性能下降，两者结合达到最优。

## 背景与动机

### 视觉无监督强化学习的泛化困境

无监督强化学习（Unsupervised Reinforcement Learning, URL）的核心目标是在没有任务奖励的条件下，预训练出能够快速适应多种下游任务的通用智能体。后继表示（Successor Representation, SR）方法因其优雅的线性奖励分解结构——将价值函数表达为基础特征与技能向量的内积 $Q_r^\pi(s,a) = \psi^\pi(s,a)^\top z$——而在零样本泛化方面展现出独特优势：智能体只需从少量任务样本中通过最小二乘回归推断技能向量 $z_r := \mathbb{E}_{\rho}[\varphi\varphi^\top]^{-1}\mathbb{E}_{\rho}[\varphi r]$，即可泛化到新任务。

然而，这一优势在视觉输入下急剧衰减。Figure 2(a) 清晰地揭示了这一断层：**HILP** 和 **FB** 等代表性 SR 方法在低维物理状态输入下泛化性能优异，但在高维视觉输入下性能断崖式下降。这一现象指向一个深层问题：视觉 URL 中，SR 方法的瓶颈不在后继度量本身，而在其所依赖的视觉表示。

### 瓶颈诊断：联合优化导致表示偏差

传统 SR 方法将编码器与后继目标端到端联合优化——编码器仅通过 SR 目标的梯度获得监督信号。这种设计在低维状态下可行，但在高维视觉空间中产生了严重的表示偏差。

Figure 2(b) 的注意力热力图直接暴露了这一缺陷：现有方法的注意力大量集中在与任务动态无关的背景区域（如地面纹理、天空），而非智能体自身的关节或运动关键部位。这种偏差的因果后果在 Figure 3 中得到定量验证：HILP-pixel 的值-回报 Spearman 相关性显著低于 HILP-state 和 HILP-SDE-pixel，说明**次优表示主要损害的是后继度量的质量，而非基础特征本身**。换言之，编码器学到的是“看热闹”而非“看门道”的表示。

理论分析进一步支撑了这一诊断。论文导出的零样本策略次优性界表明，泛化误差受后继特征逼近误差的直接控制：

$$\|\hat{V}^{\pi_{z_r}} - V^\star\|_\infty \leq \frac{3\|z_r\|_*}{1-\gamma} \sup_{s,a} \|\hat{\psi}^{z_r}(s,a) - \psi^{\pi_{z_r}}(s,a)\|$$

当编码器聚焦于动态无关区域时，后继特征 $\psi$ 的估计偏差被放大，进而通过技能推断 $z_r$ 传导至策略，最终侵蚀泛化性能。

### 策略建模的双重挑战

除表示偏差外，现有 SR 方法在策略层面同样存在短板。标准技能条件策略（如高斯策略）难以捕捉无监督预训练中自然涌现的多模态行为分布——同一技能 $z$ 可能对应多种有效动作模式（如“行走”技能既可以是小步快走也可以是大步慢走）。单模态策略强行将多模态分布压缩为单峰，导致技能表达力不足和可控性下降。同时，扩散策略虽能建模多模态，但其多步采样过程在推理效率上构成瓶颈。

### 本文动机

上述分析揭示了视觉 URL 的两个核心缺口：(1) 表示学习与 SR 目标的耦合导致动态无关的视觉偏差；(2) 策略建模缺乏对多模态行为分布的表达能力和高效推理机制。SRCP 的提出正是为了填补这两个缺口——通过显著性引导的动态表示学习将编码器从 SR 目标中解耦，同时引入一致性策略与 URL 特定的无分类器引导，在技能多样性与可控性之间取得平衡。

## 核心创新

### 问题根源：视觉后继表示中的表示-目标耦合

现有基于后继表示（SR）的无监督强化学习方法（如 **HILP** 和 **FB**）在低维状态输入下表现出优异的零样本泛化能力，但在高维视觉输入下性能急剧下降（见 Figure 2(a)）。SRCP 的诊断实验揭示了这一现象的深层原因：

- **注意力偏差**：SR 方法联合优化编码器与后继度量目标，导致编码器学到的视觉表示偏向任务无关的视觉区域（如背景纹理、静态物体），而非与动力学相关的特征（见 Figure 2(b) 注意力热力图对比）。
- **后继度量失真**：次优表示直接损害了后继特征的估计质量。HILP-pixel（视觉输入下的 HILP）的值-回报 Spearman 相关性显著低于 HILP-state（状态输入）和 HILP-SDE-pixel（使用物理真值监督编码器的视觉输入），表明问题根源在于表示学习而非后继度量本身（见 Figure 3）。
- **策略建模受限**：不准确的表示导致技能条件策略难以表达多模态动作分布，削弱了技能的可控性和多样性（见 Figure 4 中不同技能下的轨迹对比）。

上述发现指向一个核心瓶颈：**表示学习与后继目标端到端耦合，使编码器缺乏独立于 SR 目标的动态感知能力，进而形成“表示偏差 → 度量不准 → 策略退化 → 泛化失败”的级联失效**。

### 关键操作柄：解耦表示与策略的双重革新

SRCP 通过两个核心操作柄打破上述级联失效：

1. **显著性引导的动态表示解耦**：将编码器训练从 SR 目标中分离，引入基于后继值函数梯度的显著性图作为监督信号，强制编码器聚焦于动态相关区域，学习与任务无关的动力学特征。
2. **一致性策略与 URL 特定无分类器引导**：采用一致性扩散模型作为技能条件策略，实现单步高效的多模态动作建模，并通过无分类器引导在技能多样性与可控性之间取得平衡。

这两个操作柄协同作用：解耦后的高质量表示为后继度量提供准确的动态特征，而一致性策略充分利用准确的度量信息生成可控的多模态行为，共同提升零样本泛化性能。

### 与基线方法的 Changed Slots 对比

| 设计维度 | 基线方法（HILP / FB 等） | SRCP 创新 |
|---------|----------------------|----------|
| **表示学习目标** | 与 SR 目标端到端联合优化，编码器仅依赖 SR 梯度 | 显著性引导的前向/逆向动力学预测任务，与 SR 目标完全解耦 |
| **编码器监督信号** | 仅依赖 SR 目标的间接梯度 | 额外使用基于 SR 值函数梯度的显著性图作为动力学预测的监督掩码 |
| **策略学习范式** | 标准技能条件前馈策略（如高斯策略） | 一致性策略 + URL 特定无分类器引导 + 双重行为一致性损失 |

**Slot 1: 表示学习目标解耦**。基线方法将编码器 $f$ 与后继特征 $\psi$ 联合优化，使得表示学习完全受 SR 目标驱动。SRCP 引入独立的动力学预测任务——前向动力学 $\mathcal{L}_{D1} = \|D(f(o), a) - s'\|^2$ 和逆向动力学 $\mathcal{L}_{I1} = \|I(f(o), s') - a\|^2$——使编码器学习与后继度量无关的动态特征。这一解耦设计在理论上由泛化界支撑：零样本策略的次优性 $\|\hat{V}^{\pi_{z_r}} - V^{\star}\|_{\infty} \leq \frac{3\|z_r\|_*}{1-\gamma} \sup_{s,a} \|\hat{\psi}^{z_r}(s,a) - \psi^{\pi_{z_r}}(s,a)\|$ 表明，后继特征的逼近误差直接控制泛化性能，而解耦表示学习是降低该误差的关键。

**Slot 2: 显著性图监督**。基线方法的编码器缺乏显式的注意力引导。SRCP 从后继值函数 $Q$ 对输入观测 $o$ 的梯度中构建显著性图 $O_\alpha$——保留梯度幅值排名靠前的像素，屏蔽信息量低的区域——并将其作为额外的动力学预测目标：$\mathcal{L}_{D2} = \|D(f(o_\alpha), a) - s'\|^2$。总表示损失 $\mathcal{L}_{\mathrm{rep}} = \mathcal{L}_{D1} + \mathcal{L}_{I1} + \beta(\mathcal{L}_{D2} + \mathcal{L}_{I2})$ 中的 $\beta$ 控制显著性引导的强度，使得编码器被迫关注对动态预测真正重要的视觉区域。

**Slot 3: 一致性策略与无分类器引导**。基线方法使用单模态高斯策略，难以捕捉技能条件动作的多模态分布。SRCP 采用一致性模型 $g_\theta(s, a_t, z) \approx a_0$，可从任意噪声水平直接恢复干净动作，实现单步高效推理。同时引入 URL 特定的无分类器引导：$a = g_\theta(s, a_t, \emptyset) + \omega \cdot (g_\theta(s, a_t, z) - g_\theta(s, a_t, \emptyset))$，通过引导权重 $\omega$ 调节技能对动作生成的约束强度。策略训练目标 $\mathcal{L}_{\pi} = \mathcal{L}_Q^{\pi} + \lambda_1 \mathcal{L}_{bc1}^{\pi} + \lambda_2 \mathcal{L}_{bc2}^{\pi}$ 融合了技能条件值损失和双重行为一致性损失，确保策略既忠于数据集行为又具备技能可控性。

### 创新点的协同机制

三个 changed slots 形成闭环协同（见 Figure 5 框架总览）：(1) 显著性图从当前后继度量中提取动态注意力区域；(2) 显著性引导的动力学任务利用该图训练编码器，更新后的编码器反过来改进后继度量的输入质量；(3) 一致性策略基于高质量的后继度量学习多模态技能行为，其生成的动作又为下一轮显著性图计算提供新的数据。这种迭代优化的设计使得表示质量、度量精度和策略表达力相互促进，最终在 Walker、Quadruped、Cheetah 域分别以 13%、33%、11% 的优势超越当时最佳方法（见 Table 1）。

## 整体框架

SRCP 的整体预训练框架由五个核心模块构成，它们在一个迭代训练循环中协同工作，如图 Figure 5 所示。这五个模块分别是：无监督数据集、显著性图生成、显著性动态表示学习、后继度量训练以及一致性策略学习。框架的核心设计理念是将视觉表示学习与后继表示（SR）目标解耦，同时引入高效的多模态策略建模，从而解决现有 SR 方法在视觉无监督强化学习（URL）中泛化性能急剧下降的问题。

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/005_Figure_5.jpg]]
*Figure 5: SRCP pretraining framework. SRCP first leverages unsupervised data to generate saliency maps that guide the learning of saliency-aware dynamic representations. The resulting encoder is shared between successor measure training and consistent policy learning, enabling effective successor measure and expressive policy behaviors, thereby enhancing generalization*

### 模块关系与数据流

框架的输入是无奖励的多任务交互轨迹，这些轨迹来自无监督数据集。整个流程按以下顺序迭代执行：

1. **无监督数据集**：提供多样化的、与任务无关的交互轨迹 $(s, a, s')$，作为预训练的数据源。这些数据不包含任何任务奖励信号，仅反映智能体在环境中的原始交互行为。

2. **显著性图生成**：在每次迭代中，系统基于当前后继值函数 $Q$ 对输入观测 $o$ 的梯度计算显著性图 $O_\alpha$。具体而言，通过计算梯度幅值并仅保留排名靠前的像素，将动态无关区域掩码掉，从而高亮对后继度量影响最大的动态相关区域。这一步骤为后续的表示学习提供了关键的监督信号。

3. **显著性动态表示学习**：编码器 $f$ 通过一个显著性引导的动力学预测任务进行更新。该任务同时利用原始观测 $o$ 和显著性掩码后的观测 $o_\alpha$，训练前向动力学模型 $D$ 和逆向动力学模型 $I$。前向损失 $\mathcal{L}_{D1}$ 和 $\mathcal{L}_{D2}$ 分别基于原始观测和显著性观测预测下一状态表示 $s'$；逆向损失 $\mathcal{L}_{I1}$ 和 $\mathcal{L}_{I2}$ 则从当前和下一状态表示预测动作 $a$。总表示学习损失为：
   $$\mathcal{L}_{\mathrm{rep}} = \mathcal{L}_{D1} + \mathcal{L}_{I1} + \beta \cdot (\mathcal{L}_{D2} + \mathcal{L}_{I2})$$
   这一设计强制编码器聚焦于与动力学相关的视觉特征，而非被 SR 目标间接引导至任务无关区域。

4. **后继度量训练**：基于解耦后的编码器，基础特征 $\varphi(s)$ 和后继特征 $\psi(s, a, z)$ 被联合优化，以满足贝尔曼一致性：
   $$L_{\psi} = \|\psi(s, a, z) - \varphi(s') - \gamma \bar{\psi}(s', a', z)\|^2$$
   由于编码器已通过动力学任务捕获了动态相关特征，后继度量的估计质量得到显著提升，这直接关系到零样本泛化的理论界（Equation 1）。

5. **一致性策略学习**：策略部分采用一致性模型 $g_\theta(s, a_t, z)$ 作为技能条件策略，能够从任意噪声水平 $t$ 直接恢复干净动作 $a_0$。训练目标由三部分组成：
   $$\mathcal{L}_{\pi} = \mathcal{L}_Q^{\pi} + \lambda_1 \mathcal{L}_{bc1}^{\pi} + \lambda_2 \mathcal{L}_{bc2}^{\pi}$$
   其中 $\mathcal{L}_Q^{\pi}$ 是技能条件值损失，$\mathcal{L}_{bc1}^{\pi}$ 和 $\mathcal{L}_{bc2}^{\pi}$ 是双重行为一致性损失。推理时，通过无分类器引导机制融合无条件和有条件输出：
   $$a = g_\theta(s, a_t, \emptyset) + \omega \cdot (g_\theta(s, a_t, z) - g_\theta(s, a_t, \emptyset))$$
   这使得策略能够在技能多样性与可控性之间取得平衡，并有效建模多模态动作分布。

### 关键设计选择

框架的两个关键操作柄——表示学习与 SR 目标的解耦、一致性策略与无分类器引导的引入——直接回应了视觉 URL 中观察到的瓶颈。Figure 2 显示，传统 SR 方法（如 HILP、FB）在视觉输入下泛化性能急剧下降，且注意力热力图集中在任务无关区域；Figure 3 进一步揭示，HILP-pixel 的值-回报 Spearman 相关性显著低于 HILP-state，说明次优表示主要损害后继度量而非基础特征。SRCP 通过显著性引导的动力学任务强制编码器关注动态相关区域，并利用一致性策略实现单步高效的多模态动作生成，从而在 Walker、Quadruped、Cheetah 等域上取得了显著优于现有方法的零样本泛化性能（Table 1）。

### 补充图表

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/001_Figure_1.jpg]]
*Figure 1: Illustration of traditional RL and SR methods: (a) Traditional RL trains with task-specific rewards. (b) Traditional RL generalizes poorly to tasks with different rewards. (c) SR methods learn skill-conditioned skills without reward. (d) SR agents infer skills from minimal task information and generalize across tasks*

## 核心模块与公式推导

### 5.1 总体框架与模块划分

SRCP 预训练框架由五个模块构成，按迭代循环交替优化（Figure 5）：

1. **无监督数据集**：提供无奖励的多任务交互轨迹，作为预训练的数据源。
2. **显著性图生成**：基于后继值函数对输入观测的梯度，计算显著性图以高亮动态相关区域。
3. **显著性动态表示学习**：利用原始观测和显著性图，通过前向/逆向动力学预测任务训练编码器，强制其聚焦于动态特征。
4. **后继度量训练**：基于解耦后的编码器，联合优化基础特征 $\varphi$ 和后继特征 $\psi$，保持贝尔曼一致性。
5. **一致性策略学习**：以一致性模型作为技能条件策略，引入无分类器引导和多重行为一致性损失，实现多模态行为建模与技能可控性。

---

### 5.2 显著性图生成

显著性图 $O_\alpha$ 的构造基于后继值函数对输入观测的梯度。给定观测 $o$ 和技能 $z$，值函数由后继特征与技能向量的内积给出：

$$Q(s, a, z) = \psi(s, a)^\top z$$

计算 $Q$ 对观测 $o$ 的梯度，按梯度幅值对像素进行排序，仅保留排名靠前的像素，其余区域被掩码，从而得到显著性图 $O_\alpha$。该图显式标记了与动态预测最相关的视觉区域。

---

### 5.3 显著性动态表示学习

表示学习的目标是将编码器 $f$ 从后继度量训练中解耦，使其专注于提取与动态相关的特征。具体通过四组动力学预测损失实现：

**原始观测的动力学损失**：

- 前向动力学损失 $\mathcal{L}_{D1}$：从当前表示 $f(o)$ 和动作 $a$ 预测下一状态表示 $s'$：
  $$\mathcal{L}_{D1} = \| D(f(o), a) - s' \|^2$$

- 逆向动力学损失 $\mathcal{L}_{I1}$：从当前表示 $f(o)$ 和下一状态表示 $s'$ 预测动作 $a$：
  $$\mathcal{L}_{I1} = \| I(f(o), s') - a \|^2$$

**显著性引导的动力学损失**：

- 显著性前向动力学损失 $\mathcal{L}_{D2}$：使用显著性掩码观测 $o_\alpha$ 预测下一状态表示：
  $$\mathcal{L}_{D2} = \| D(f(o_\alpha), a) - s' \|^2$$

- 显著性逆向动力学损失 $\mathcal{L}_{I2}$：基于显著性观测的表示预测动作：
  $$\mathcal{L}_{I2} = \| I(f(o_\alpha), s') - a \|^2$$

**总表示学习损失**为原始损失与显著性损失的加权组合：

$$\mathcal{L}_{\mathrm{rep}} = \mathcal{L}_{D1} + \mathcal{L}_{I1} + \beta \cdot (\mathcal{L}_{D2} + \mathcal{L}_{I2})$$

其中 $\beta$ 控制显著性引导的强度（最优值 $\beta=0.5$，见 Table 11）。

---

### 5.4 后继度量训练

后继特征 $\psi(s, a, z)$ 定义为在技能 $z$ 对应的策略 $\pi_z$ 下，未来基础特征 $\varphi$ 的折扣期望和：

$$\psi(s_0, a_0, z) = \mathbb{E}\left[\sum_{t=0}^{\infty} \gamma^t \varphi(s_{t+1}) \mid (s_0, a_0), \pi_z\right]$$

后继度量训练通过时序差分学习保持贝尔曼一致性：

$$L_{\psi} = \| \psi(s, a, z) - \varphi(s') - \gamma \bar{\psi}(s', a', z) \|^2$$

其中 $\bar{\psi}$ 为目标网络输出的后继特征。基础特征 $\varphi$ 与后继特征 $\psi$ 共享编码器 $f$，但编码器参数仅由表示学习损失 $\mathcal{L}_{\mathrm{rep}}$ 更新，与 $L_\psi$ 梯度解耦。

**零样本技能推理**：给定下游任务的奖励函数 $r$，通过最小二乘回归从少量样本中推断最优技能向量：

$$z_r := \mathbb{E}_{\rho}[\varphi \varphi^\top]^{-1} \mathbb{E}_{\rho}[\varphi r]$$

其中 $\rho$ 为离线数据分布。随后，零样本策略的动作由 $\pi_{z_r}$ 生成，其 Q 函数可表达为后继特征与技能向量的内积：$Q_r^\pi(s, a) = \psi^\pi(s, a)^\top z_r$。

---

### 5.5 一致性策略学习

为建模技能条件策略的多模态动作分布，SRCP 采用一致性模型作为策略主干。一致性模型 $g_\theta$ 从任意噪声水平 $t$ 的噪声动作 $a_t$ 直接映射回干净动作 $a_0$：

$$g_\theta(s, a_t, z) \approx a_0, \quad \forall t$$

**无分类器引导**：在推理时，结合无条件和有条件输出来调节技能指导强度：

$$a = g_\theta(s, a_t, \emptyset) + \omega \cdot (g_\theta(s, a_t, z) - g_\theta(s, a_t, \emptyset))$$

其中 $\omega$ 为引导权重（Walker 域最优 $\omega=3$，见 Table 10），$\emptyset$ 表示无条件分支（使用随机技能策略的数据训练）。

**策略训练目标**由三项损失加权组合：

$$\mathcal{L}_{\pi} = \mathcal{L}_Q^{\pi} + \lambda_1 \mathcal{L}_{bc1}^{\pi} + \lambda_2 \mathcal{L}_{bc2}^{\pi}$$

- $\mathcal{L}_Q^\pi$：技能条件 Q 值最大化损失，鼓励策略生成高回报动作。
- $\mathcal{L}_{bc1}^\pi$：技能条件行为一致性损失，约束同一技能下的动作输出一致性。
- $\mathcal{L}_{bc2}^\pi$：无条件行为一致性损失，约束随机技能策略下的一致性，增强无条件分支的稳定性。

该设计使 SRCP 在单步推理中即可生成高质量动作，避免了扩散策略的多步采样开销（Table 15：SRCP 单步推理即达到扩散策略 40 步采样的性能，训练时间从 64.8h 降至 25.4h）。

---

### 5.6 零样本泛化的理论保证

零样本策略的次优性由后继特征的逼近误差控制（Section 4）：

$$\|\hat{V}^{\pi_{z_r}} - V^{\star}\|_{\infty} \leq \frac{3 \|z_r\|_*}{1 - \gamma} \sup_{s,a} \|\hat{\psi}^{z_r}(s,a) - \psi^{\pi_{z_r}}(s,a)\|$$

该界表明：后继特征估计越精确，零样本泛化性能越接近最优。这从理论上解释了 SRCP 通过显著性动态表示解耦来提升后继度量质量、进而改善泛化的内在机制。

### 补充图表

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/002_Figure_2.jpg]]
*Figure 2: Generalization performance and attention analysis of prior methods and SCPL. (a) Task generalization performance of previous SR methods (HILP and FB) under low-dimensional state and high-dimensional visual inputs. (b) Comparison of saliency mask maps and attention heatmaps of prior methods and SRCP in the DMC Walker and Quadruped domains*

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/003_Figure_3.jpg]]
*Figure 3: Value and performance analysis of methods in Walker Stand task. (a) Implicit reward and value estimations of methods across trajectories with varying returns; (b) Spearman correlations of reward and value with return, and performance across methods*

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/004_Figure_4.jpg]]
*Figure 4: Trajectory comparison of methods with random and walking skills in the walker domain*

## 实验与分析

### 核心瓶颈验证：视觉后继表示为何失效？

SRCP 首先对现有后继表示（SR）方法在视觉无监督强化学习（URL）中的退化现象进行了系统诊断。**Figure 2(a)** 显示，HILP 和 FB 在低维状态输入下表现出强泛化能力，但在高维视觉输入下性能急剧下降。注意力可视化进一步揭示，SR 方法的编码器倾向于关注与任务动态无关的背景区域（**Figure 2(b)**），而非智能体关节或地面接触等动态关键区。

为量化表示质量对后继度量的影响，SRCP 在 Walker Stand 任务上进行了值估计分析。**Figure 3** 表明：
- HILP-pixel 的值-回报趋势曲线明显弱于 HILP-state 和 HILP-SDE-pixel（**Figure 3(a)**），说明视觉编码器学习到的表示未能有效支撑值函数估计。
- Spearman 相关性对比中，HILP-pixel 的值-回报相关性显著低于其他变体，且累积回报也更低（**Figure 3(b)**）。

这些证据共同指向一个核心瓶颈：**联合优化编码器与 SR 目标会导致表示偏向动态无关区域，进而损害后继度量的准确性，最终限制零样本泛化能力。** 这一发现为 SRCP 将表示学习与 SR 目标解耦的设计提供了直接动机。

### 主要结果：零样本泛化性能

SRCP 在 ExORL 基准的 4 个域、16 个任务上进行了全面评估，每个任务使用 4 个无监督数据集（RND、PROTO、APS、APT）和 4 个随机种子，共 16 次运行取平均。**Table 1** 汇总了主要结果：

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/006_Table_1.jpg]]
*Table 1: Zero-shot generalization results across 16 tasks. Each score is averaged over 4 datasets and 4 seeds (i.e. 16 runs)*

| 域 | SRCP 平均回报 | 最佳基线 (HILP) | 提升幅度 |
|---|---|---|---|
| Walker (4 任务) | 453 | 238 | +90% |
| Quadruped (4 任务) | 355 | 232 | +53% |
| Cheetah (4 任务) | 543 | 454 | +20% |
| Jaco (4 任务) | 41 | 32 | +28% |

SRCP 在所有域上均一致超越此前最优方法，尤其在 Walker 和 Quadruped 域分别实现了 90% 和 53% 的大幅提升。在更具挑战性的视觉泛化场景 DMC-GB Walker Color Easy 上，SRCP 平均回报达到 400，远超 HILP（157）和 FB（103）（**Table 13**）。在 Point Mass Maze 导航任务中，SRCP 以 220 的平均回报同样显著优于 HILP（155）和 FB（5）（**Table 14**）。这些结果表明，SRCP 的解耦设计与一致性策略在不同任务形态和视觉复杂度下均具有鲁棒的泛化优势。

### 消融实验：组件贡献分析

为验证各组件的独立贡献，SRCP 在 RND 数据集上进行了系统消融（**Table 2**）：

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/008_Table_2.jpg]]
*Table 2: Ablation study of SRCP on the RND dataset across 4 domains. Each score is the averaged return over 4 tasks per domain, with 4 random seeds per task (i.e., 16 runs)*

- **移除显著性动态编码器（SRCP w/o SE）**：Walker 域平均得分从 439 降至 345，Quadruped 域从 485 降至 455。这表明解耦的显著性引导表示学习是泛化性能的关键支撑，尤其在需要精细动态感知的 Walker 域。
- **移除一致性策略（SRCP w/o CP）**：Walker 域平均得分降至 396，Quadruped 域降至 470。验证了多模态策略建模对技能可控性的重要性。
- **完整 SRCP**：在 Walker（439）、Quadruped（485）、Cheetah（602）、Jaco（50）四个域上均取得最高平均分，证明表示学习与策略学习的协同作用。

进一步的关键参数消融包括：

- **技能引导权重 ω**：ω=0（即关闭无分类器引导）时性能大幅下降；在 Walker 域 ω=3 时平均得分最优（439），Quadruped 域 ω=3 同样表现最佳（**Table 10、Table 3**）。这表明无分类器引导在技能多样性与可控性之间起到了关键的平衡作用。
- **显著性权重 β**：β=0.5 时 Walker 域平均得分最高（439）。β 过小会削弱动态线索的捕获，过大则可能引入噪声（**Table 11**）。

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/009_Table_3.jpg]]
*Table 3: Ablation study of parameter ω in SRCP on Quadruped domain in RND dataset, with 4 random seeds per task*

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/021_Table_10.jpg]]
*Table 10: Ablation study of parameter ω in SRCP on Walker domain in RND dataset, with 4 random seeds per task*

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/022_Table_11.jpg]]
*Table 11: Ablation study of parameter*

### 策略建模对比：一致性策略 vs. 扩散策略

为验证一致性策略的效率优势，SRCP 在 Proto Quadruped 任务上与扩散策略进行了直接对比（**Table 15**）：

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/026_Table_15.jpg]]
*Table 15: Comparison between diffusion models and SRCP*

| 方法 | 推理步数 | 平均回报 | 训练时间 |
|---|---|---|---|
| 扩散策略 | 40 步 | 492 | 64.8h |
| SRCP（一致性策略） | **1 步** | **485** | **25.4h** |

SRCP 以单步推理达到了接近 40 步扩散策略的性能（485 vs 492），同时训练时间减少约 60%。这一性能-计算权衡表明，一致性策略在保持多模态表达能力的同时，显著降低了推理延迟和训练开销，更适用于实际部署场景。

### 框架兼容性与鲁棒性

SRCP 的设计具有方法级兼容性。将 SRCP 的表示学习与策略学习组件集成到 FB 方法中形成 SRCP(FB)，在 Walker 和 Quadruped 域上 SRCP(FB) 均一致优于原始 FB（**Figure 8**），验证了该框架可作为通用增强模块适用于不同的 SR 基方法。

![[assets/figures/papers/paper_list_l2722_https_arxiv_org_abs_2604_05931/figures/010_Figure_8.jpg]]
*Figure 8: Generalization performance of FB and SRCP(FB)*

在推理数据量敏感性方面，SRCP 在 500 至 20k 条任务转移样本下性能保持稳定（**Table 16**），表明其对少量下游数据的适应能力，适合低样本零样本迁移场景。

### 失败模式与局限性

尽管 SRCP 在主要基准上表现优异，仍存在以下局限：

1. **高度随机环境的挑战**：在视觉干扰极强的场景下，基于梯度的显著性图质量可能下降，进而影响表示学习的稳定性。当前框架未针对动态视频背景等复杂干扰进行专门验证。
2. **离线设定限制**：SRCP 针对离线无监督预训练设计，尚未扩展到在线交互式学习场景，无法在交互中持续改进表示。
3. **额外计算开销**：虽然通过解耦设计控制了整体计算量，但显著性图生成与一致性训练仍引入额外耗时（**Table 12** 提供了 A800 GPU 上的计算资源对比）。

### 关键图表索引

- **Figure 2**：SR 方法泛化性能退化与注意力偏差可视化
- **Figure 3**：值估计质量与回报相关性分析
- **Table 1**：16 任务零样本泛化主结果
- **Table 2**：RND 数据集组件消融
- **Table 15**：扩散策略与一致性策略效率对比

## 方法谱系与知识库定位

### 1. 问题定位：视觉无监督RL中后继表示方法的退化

SRCP 瞄准的是视觉无监督强化学习（URL）中后继表示（Successor Representation, SR）方法的系统性退化问题。SR 方法（如 **HILP** 、**FB** ）在低维状态输入下展现出强大的零样本泛化能力——它们通过无奖励交互学习技能条件后继特征，在测试时仅需少量任务奖励样本即可推断最优技能向量并泛化至新任务。然而，当输入从低维状态切换为高维视觉观测时，这些方法的泛化性能急剧下降（Figure 2a），注意力热力图显示编码器聚焦于任务无关的背景区域（Figure 2b），导致后继度量估计失真，技能条件策略的多模态行为表达能力与可控性随之恶化。

SRCP 的核心诊断是：**次优表示主要损害后继度量，而非基础特征本身**。Figure 3 的证据链支撑了这一判断——HILP-pixel 的值-回报 Spearman 相关性显著低于 HILP-state 和 HILP-SDE-pixel，说明问题根源在于联合优化编码器与 SR 目标时，梯度信号使编码器偏向与动态无关的视觉特征，进而污染后继值函数估计。

### 2. 方法谱系中的位置

SRCP 处于**视觉 URL 后继表示方法**与**扩散/一致性策略学习**的交叉点。其基线谱系可分为三类：

| 类别 | 代表方法 | 核心机制 | 在视觉URL中的局限 |
|------|---------|---------|-----------------|
| 后继特征方法 | **HILP** 、**FB** 、**FDM** | 在 Hilbert 空间或前向-后向表示中学习后继特征 | 编码器与 SR 目标联合优化导致表示退化 |
| 低秩/谱方法 | **LRA-SR** 、**LAP** | 低秩近似或 Laplacian 特征函数 | 同样受限于端到端优化的表示质量 |
| 通用表示方法 | **CL** （对比学习）、**AE** （自编码器） | 任务无关的表示预训练 | 缺乏动态针对性，无法为 SR 提供有效特征 |

SRCP 的独特定位在于**将表示学习从 SR 目标中解耦**，而非设计更强的联合优化策略。这一设计选择使 SRCP 可作为插件式框架与多种 SR 方法集成——实验表明 SRCP(FB) 在所有任务上一致优于原始 FB（Figure 8），验证了框架的兼容性。

### 3. 核心操作柄与因果机制

SRCP 通过两个关键操作柄实现性能跃升：

**操作柄一：显著性引导的动态表示学习。** 传统方法中编码器仅接收 SR 目标的梯度信号，缺乏对动态相关区域的显式引导。SRCP 利用后继值函数对输入观测的梯度构造显著性图 $O_\alpha$——保留梯度幅值排名靠前的像素，遮蔽信息量低的区域——然后将显著性图作为前向/逆向动力学预测任务的监督掩码。总表示损失为：
$$\mathcal{L}_{\mathrm{rep}} = \mathcal{L}_{D1} + \mathcal{L}_{I1} + \beta \cdot (\mathcal{L}_{D2} + \mathcal{L}_{I2})$$
其中 $\mathcal{L}_{D1}$、$\mathcal{L}_{I1}$ 基于原始观测，$\mathcal{L}_{D2}$、$\mathcal{L}_{I2}$ 基于显著性掩码观测，$\beta$ 控制显著性引导强度。这一设计强制编码器聚焦于与状态转移因果相关的视觉区域，从而为后续的后继度量训练提供高质量动态特征。

**操作柄二：一致性策略 + URL 特定无分类器引导。** 传统高斯策略难以建模技能条件多模态动作分布。SRCP 采用一致性模型作为策略主干，从任意噪声水平直接恢复干净动作 $g_\theta(s, a_t, z) \approx a_0$，实现单步高效推理。无分类器引导机制通过混合无条件和有条件输出：
$$a = g_\theta(s, a_t, \emptyset) + \omega \cdot (g_\theta(s, a_t, z) - g_\theta(s, a_t, \emptyset))$$
在技能多样性与可控性之间取得平衡——$\omega=0$ 时退化为无技能引导的随机行为，$\omega=3$ 时在 Walker 域达到最优（Table 10）。

这两个操作柄的协同作用通过理论分析得到支撑：零样本策略的次优性受后继特征逼近误差控制（Section 4 中的泛化界），而显著性引导表示学习直接压缩该误差上界。

### 4. 适用边界与局限

SRCP 在以下条件下展现出显著优势：
- **离线无监督预训练场景**：利用无奖励多任务交互轨迹即可完成全部预训练
- **视觉输入的高维观测**：在 Walker、Quadruped、Cheetah、Jaco 四域 16 任务上平均性能分别超出当时最佳方法 13%、33%、11% 和 28%（Table 1）
- **多模态行为建模需求**：一致性策略能捕获技能条件动作分布的多模态特性（Figure 4 的轨迹对比）
- **推理样本受限场景**：对推理预算不敏感，在 500 至 20k 条任务转移样本下性能稳定（Table 16）

当前框架的明确局限包括：
1. **仅支持离线设置**：尚未扩展到在线学习场景，无法在交互中持续改进表示和策略
2. **显著性图质量依赖**：在高度随机或极端视觉干扰环境中，基于值函数梯度的显著性图可能失效，影响表示学习质量——这一风险在分析中已被识别但缺乏实验验证
3. **额外计算开销**：虽然通过解耦设计控制了整体成本，但显著性图生成与一致性训练仍引入额外耗时（Table 12 提供了 A800 GPU 上的计算资源对比）
4. **与扩散策略的性能-计算权衡**：在 Proto Quadruped 上，SRCP 以单步推理达到接近 40 步扩散策略的性能（485 vs 492），且训练时间仅 25.4h（扩散策略 64.8h），但在追求极致性能的场景下扩散策略仍略有优势（Table 15）

### 5. 开放问题

1. **在线扩展**：如何将 SRCP 推广到在线视觉 URL 设置，使智能体在交互中持续改进显著性引导表示和一致性策略？这涉及在线显著性图更新机制与策略探索-利用平衡的设计。

2. **视觉鲁棒性**：在更复杂的视觉干扰（如动态视频背景、光照变化）下，基于值函数梯度的显著性机制能否保持鲁棒并提取因果特征？需要系统性的域外泛化测试。

3. **方法集成广度**：SRCP 已验证与 HILP 和 FB 的兼容性，但能否与基于谱分解的 SR 方法（如 LAP）无缝集成？显著性引导的通用性需要更多实验支撑。

4. **显著性稳定性**：显著性图生成过程中的随机性或噪声如何影响训练稳定性？是否需要引入平滑机制或贝叶斯不确定性估计？

5. **真实机器人验证**：该框架能否应用于真实机器人视觉控制任务，并验证其对领域转移（sim-to-real）的泛化能力？这涉及视觉编码器对真实纹理和光照的适应性问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/Saliency_Guided_Representation_with_Consistency_Policy_Learning_for_Visual_Unsupervised_Reinforcement_Learning.pdf]]
