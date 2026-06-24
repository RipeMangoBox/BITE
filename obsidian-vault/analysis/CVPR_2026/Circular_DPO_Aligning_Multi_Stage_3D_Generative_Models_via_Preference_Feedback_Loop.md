---
title: "Circular-DPO: Aligning Multi-Stage 3D Generative Models via Preference Feedback Loop"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Circular_DPO_Aligning_Multi_Stage_3D_Generative_Models_via_Preference_Feedback_Loop.pdf
project_link: null
code_link: null
aliases:
- CD
- Circular-DPO
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 通过构建偏好反馈循环，将最终阶段优化后的资产与未优化资产构成偏好对，前馈至前置阶段，模拟梯度信号并实现联合优化。
primary_logic: 利用 DPO 微调最终阶段产生的高质量资产与未优化资产对比，形成可前馈的偏好信号；同时引入质量感知加权机制（w1 过滤噪声，w2 动态降权）以抑制偏好数据噪声，从而在不依赖可微分梯度的条件下端到端对齐多阶段模型。
claims:
- Circular-DPO 在 ImageReward 指标上超越基线 35.15%，在 Reward3D 上超越 21.44%。
- 与各阶段独立进行 DPO 相比，Circular-DPO 在 ImageReward 上额外提升 14.11%，在 Reward3D 上额外提升 6.06%。
- 用户调研中近 70% 的参与者更偏好 Circular-DPO 生成的资产。
- DreamReward (Trellis backbone) 上 ImageReward = -0.5607
---

# Circular-DPO: Aligning Multi-Stage 3D Generative Models via Preference Feedback Loop

> [!tip] 核心洞察
> 利用 DPO 微调最终阶段产生的高质量资产与未优化资产对比，形成可前馈的偏好信号；同时引入质量感知加权机制（w1 过滤噪声，w2 动态降权）以抑制偏好数据噪声，从而在不依赖可微分梯度的条件下端到端对齐多阶段模型。

| 字段 | 内容 |
|------|------|
| 中文题名 | Circular-DPO：基于偏好反馈循环的多阶段3D生成模型对齐 |
| 英文题名 | Circular-DPO: Aligning Multi-Stage 3D Generative Models via Preference Feedback Loop |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_Circular-DPO_Aligning_Multi-Stage_3D_Generative_Models_via_Preference_Feedback_Loop_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | Circular-DPO |
| Dataset | DreamReward, User Study |

> [!tip] 效果简介
> - DreamReward (Trellis backbone) 上，ImageReward -0.5607 (+35.15%)；Reward3D 0.3290 (+21.44%)；ImageReward -0.5607 (ours) vs separate DPO (+14.11% over separate DPO)。
> - User Study 上，Preference Rate ~70% vs Trellis (original) (nearly 70% preferred Circular-DPO)。

## 概述

多阶段3D生成模型（如 **Trellis** (Xiang et al., arXiv 2024)）通过将生成过程解耦为稀疏结构生成与局部潜变量生成两个阶段，实现了高质量的3D资产合成。然而，这类管道存在一个根本性瓶颈：**阶段间存在不可微分操作，导致后续阶段（如纹理与几何细化）的偏好信号无法通过梯度反向传播到前置阶段（如稀疏结构生成）**，从而引发纹理-几何不一致性问题，限制了整体对齐优化的上限。

针对这一问题，本文提出 **Circular-DPO**，核心思路是**构建偏好反馈循环（Preference Feedback Loop）**，在不依赖可微分梯度的条件下实现多阶段模型的端到端对齐。具体而言，该方法首先利用 DPO（Direct Preference Optimization）对管道最终阶段进行微调，生成优化后的高质量3D资产；随后将这些优化资产与未优化资产构成偏好对，通过 VAE 重编码反馈至前置阶段，以偏好信号模拟梯度传播，驱动第一阶段模型的联合优化。此外，Circular-DPO 引入**质量感知加权机制**（包含基于质量差距的过滤权重 $w_1$ 和基于奖励模型对数似然的动态降噪权重 $w_2$），有效抑制偏好数据中的噪声，仅对高质量偏好对计算 DPO 损失。

实验结果表明，Circular-DPO 在多个指标上取得显著提升：在 **DreamReward** 基准上，**ImageReward 指标超越基线 35.15%，Reward3D 指标超越 21.44%**；与各阶段独立进行 DPO 训练相比，ImageReward 额外提升 14.11%，Reward3D 额外提升 6.06%。用户调研中，近 **70%** 的参与者更偏好 Circular-DPO 生成的资产，验证了该方法在提升生成质量与人类偏好对齐方面的有效性。

需要指出的是，该方法在定量指标上尚未超越此前基于 Score Distillation 的方法，且性能依赖偏好数据集质量——尽管有权重机制缓解噪声，极端噪声仍可能导致次优结果。该偏好反馈循环机制能否推广至 Score Distillation 类方法，仍是待探索的开放问题。

## 背景与动机

### 3D 生成的多阶段范式与不可微分瓶颈

近年来，3D 资产生成经历了从单阶段端到端模型向多阶段解耦架构的演进。以 **Trellis**（Xiang et al., arXiv 2024）为代表的两阶段框架，将异质 3D 表示的生成显式解耦为：**第一阶段**生成稀疏体素结构 $x_{\text{sparse}}$，**第二阶段**以该稀疏结构为条件生成局部潜变量 $x_{\text{slat}}$，编码精细几何与纹理信息。这种解耦设计有效降低了单次生成的复杂度，但也引入了一个关键瓶颈：两个阶段之间存在不可微分操作（如离散体素化），导致第二阶段的梯度信号无法反向传播至第一阶段。

这一不可微分阻隔的直接后果是**纹理-几何不一致性**（texture-geometry inconsistency）。如图 2 所示，当第二阶段生成的精细纹理与第一阶段确定的全局结构发生冲突时，前期阶段无法接收来自后期阶段的纠偏信号，使得整体生成质量受限于各阶段的独立优化能力。

### 现有对齐方法的局限

在文本到 3D 生成领域，主流的质量对齐方法可分为两类：

1. **基于 Score Distillation 的方法**：通过预训练的 2D 扩散模型提供蒸馏信号来优化 3D 表示，但其优化过程计算开销大，且对多阶段架构的适配性有限。
2. **直接偏好优化（DPO）方法**：如 **DreamDPO**（Zhou et al., arXiv 2025）将 DPO 引入 3D 生成，但仅针对单阶段模型设计，无法处理多阶段管道中的梯度阻断问题。

若简单地将 DPO 分别应用于各阶段（即各阶段独立 DPO），偏好信号仍被局限在各自阶段内，前期阶段无法利用后期优化产生的质量提升信息。这正是本文要解决的核心问题：**如何在不可微分的多阶段管道中，将最终阶段的偏好信号有效传递至前期关键阶段，实现端到端的联合对齐？**

### 核心动机：偏好反馈循环

本文的核心洞察是：虽然梯度无法直接跨越不可微分操作反向传播，但**偏好信号可以通过数据循环的方式前馈传递**。具体而言，当最终阶段经过 DPO 微调后，其生成的 3D 资产质量显著提升；将这些优化后的资产与未优化资产构成偏好对，经过 VAE 重编码回稀疏表示空间后，即可作为第一阶段的训练信号。这一“优化-对比-反馈”的循环机制，本质上模拟了梯度反向传播的功能，使得前期阶段能够间接学习到后期优化的结果。

此外，偏好数据的噪声问题不容忽视。无论是人工标注的偏好对，还是通过模型自动构造的反馈对，都存在质量参差不齐的情况。因此，设计鲁棒的质量感知加权机制，在利用偏好信号的同时抑制噪声干扰，是实现稳定对齐的必要条件。

## 核心创新

Circular-DPO 的核心创新在于**构建了一个偏好反馈循环（Preference Feedback Loop）**，将多阶段 3D 生成管道中不可微分阻隔所阻断的偏好信号，以前馈偏好对的形式重新注入前置阶段，从而实现端到端的全管道对齐优化。

### 动机：纹理-几何不一致性的根源

在 **Trellis**（Xiang et al., arXiv 2024）等典型两阶段 3D 生成框架中，第一阶段生成稀疏体素结构 $x_{\text{sparse}}$，第二阶段以该结构为条件生成局部潜变量 $x_{\text{slat}}$ 以编码精细几何与纹理。然而，**纹理和几何之间的不一致性**（如 Figure 2 所示）源于一个关键瓶颈：第二阶段到第一阶段之间存在不可微分操作，导致与纹理质量相关的梯度信号无法反向传播至第一阶段。这意味着即使第二阶段能够生成高质量纹理，第一阶段生成的几何结构也无法随之优化，形成结构性错配。

### 关键机制：偏好反馈循环

Circular-DPO 通过三个步骤突破上述瓶颈，形成闭环优化：

1. **最终阶段 DPO 微调**：首先在结构化潜变量生成器 $G_L$（第二阶段）上，使用人类偏好数据集 $\mathcal{D}_{\text{slat}}$ 进行 Flow-DPO 微调，目标为 $\min_{G_L} \mathcal{L}_{\text{DPO}}(\mathcal{D}_{\text{slat}}, G_L)$。该步骤使 $G_L$ 能够生成与人类偏好对齐的高质量资产。

2. **偏好对构造与前馈**：利用优化后的 $G_L$ 与未优化的 $G_L^{\text{ref}}$ 分别生成资产，构成“优化/未优化”资产对。这些资产对经 VAE 编码器重编码，获得对应的稀疏表示 $x_{\text{sparse}}$，从而构造出可直接用于第一阶段 $G_S$ 训练的偏好对数据集。

3. **前置阶段引导**：使用构造的偏好对训练第一阶段稀疏结构生成器 $G_S$，目标为 $\min_{G_S} \mathcal{L}_{\text{DPO}}(\{(x^{\text{op}}, x^{\text{un-op}})\}, G_S)$。由此，来自最终阶段的偏好信号以前馈方式传递至前置阶段，模拟了梯度信号的功能。

这一机制的核心洞察在于：**利用 DPO 微调产生的优化资产与未优化资产之间的质量差异，将不可微分的梯度信号转化为可前馈的偏好对**，从而在不依赖可微分梯度的条件下实现联合优化。

### 质量感知加权机制

偏好数据（尤其是前馈构造的偏好对）存在噪声，直接使用可能损害训练稳定性。Circular-DPO 引入双层质量感知加权：

- **质量差距权重 $w_1$**：定义 $w_1 = G_{\text{op}} - G_{\text{un-op}}$，即优化资产与未优化资产的偏好得分之差。仅当 $w_1 > \tau$（阈值 $\tau$ 设为零）时，该偏好对才被纳入训练，过滤掉质量差距不显著的噪声对。

- **动态可靠性权重 $w_2$**：基于奖励模型 $r$ 的对数似然计算 $w_2(c, x^w, x^l) = \frac{\exp(h)}{\mathbb{E}_{\mathcal{D}}[\exp(h)]}$，其中 $h = \log \sigma(r(c, x^w) - r(c, x^l))$。该权重为更可靠的偏好对分配更高权重，动态抑制噪声。

最终损失函数为条件触发式：
$$
\mathcal{L}_{\text{Circular-DPO}} = \begin{cases} \mathcal{L}_{\text{DPO}} & \text{if } w_1 > \tau \\ 0 & \text{if } w_1 \le \tau \end{cases}
$$
其中 $\mathcal{L}_{\text{DPO}}$ 为带 $w_2$ 加权的通用 Flow-DPO 损失。

### 与 Baseline 的关键差异

| 维度 | Baseline（Trellis） | Circular-DPO |
|------|---------------------|--------------|
| 第二阶段训练 | 标准条件流匹配（CFM） | CFM + Flow-DPO 微调 |
| 第一阶段优化信号 | 无（梯度阻隔） | 前馈偏好对，模拟梯度信号 |
| 偏好对权重 | 均匀权重 | $w_1$ 过滤 + $w_2$ 动态降噪 |
| 优化范式 | 各阶段独立训练 | 偏好反馈循环联合优化 |

消融实验证实：与各阶段独立进行 DPO（separate DPO）相比，引入反馈循环后在 ImageReward 上额外提升 14.11%，在 Reward3D 上额外提升 6.06%，验证了反馈循环是性能增益的核心来源。同时，移除 $w_1$ 或 $w_2$ 均导致生成质量下降，出现纹理几何不一致，证实了质量感知加权机制的必要性。

## 整体框架

Circular-DPO 提出了一套面向多阶段 3D 生成管线的偏好反馈循环框架，其核心设计目标是**绕过不可微分操作造成的梯度阻隔**，将最终阶段的偏好信号前馈至前置阶段，实现端到端的联合对齐。

### 管线总览

框架建立在 **Trellis**（Xiang et al., arXiv 2024）的两阶段生成架构之上，并保持其模块结构不变：

1. **稀疏结构生成器 G_S**（第一阶段）：基于 Rectified Flow Transformer，从文本条件生成连续的稀疏体素特征网格 $x_{\text{sparse}}$，经解码后转化为离散稀疏结构。
2. **结构潜变量生成器 G_L**（第二阶段）：以稀疏结构为条件，通过稀疏卷积 Transformer 生成本地潜变量 $x_{\text{slat}}$，编码精细几何与纹理信息。
3. **VAE 编码器/解码器**：实现 3D 资产与潜在表示之间的双向转换——VAE 解码器将 $x_{\text{slat}}$ 解码为最终 3D 资产，VAE 编码器则将资产重编码回稀疏表示，用于构造前馈偏好对。

### 偏好反馈循环的三步机制

Circular-DPO 的核心创新在于构建了一个**闭环的偏好信号传导路径**，由三个步骤构成：

**Step 1 — 最终阶段优化**：在人类偏好数据集 $\mathcal{D}_{\text{slat}}$ 上对第二阶段生成器 $G_L$ 执行 DPO 微调，使用 Flow-DPO 目标：

$$\min_{G_L} \mathcal{L}_{\text{DPO}}(\mathcal{D}_{\text{slat}}, G_L)$$

优化后的 $G_L^{\text{opt}}$ 能够生成更符合人类偏好的 3D 资产。

**Step 2 — 偏好对构造**：利用优化后的模型采样生成“优化资产”，与原始模型生成的“未优化资产”配对。这些资产经体素化和 VAE 编码器重编码后，获得对应的稀疏表示 $x_{\text{sparse}}^{\text{op}}$ 与 $x_{\text{sparse}}^{\text{un-op}}$，形成可直接用于第一阶段训练的前馈偏好对。

**Step 3 — 前置阶段引导**：将构造的偏好对用于训练第一阶段生成器 $G_S$：

$$\min_{G_S} \mathcal{L}_{\text{DPO}}(\{(x^{\text{op}}, x^{\text{un-op}})\}, G_S)$$

至此，来自最终阶段的偏好信号以**隐式梯度**的形式传递至前置阶段，绕过了原本不可微分的操作阻隔。

### 质量感知加权机制

由于偏好数据（无论是人工标注还是自动构造）不可避免地存在噪声，Circular-DPO 引入双层加权策略：

- **质量差距权重 $w_1$**：$w_1 = G_{\text{op}} - G_{\text{un-op}}$，衡量优化资产与未优化资产的偏好得分差距，用于过滤低质量偏好对。
- **动态可靠性权重 $w_2$**：基于奖励模型 $r$ 的对数似然计算，为更可靠的偏好对分配更高权重：

$$w_2(c, x^w, x^l) = \frac{\exp(h)}{\mathbb{E}_{\mathcal{D}}[\exp(h)]}, \quad h = \log \sigma(r(c, x^w) - r(c, x^l))$$

最终损失仅对满足 $w_1 > \tau$ 的偏好对计算 DPO 损失：

$$\mathcal{L}_{\text{Circular-DPO}} = \begin{cases} \mathcal{L}_{\text{DPO}} & \text{if } w_1 > \tau \\ 0 & \text{if } w_1 \le \tau \end{cases}$$

该过滤机制有效抑制了低质量偏好对带来的噪声干扰，消融实验证实移除 $w_1$ 或 $w_2$ 均会导致纹理-几何不一致性加剧、生成质量下降。

### 关键设计洞察

框架的本质创新在于：**将不可微分的“解码-渲染-评分”链路替换为“采样-配对-前馈”的偏好循环**。传统多阶段管线中，第二阶段产生的纹理几何不一致性无法通过梯度反向传播修正第一阶段的结构生成；Circular-DPO 通过 DPO 将最终资产的质量差异编码为偏好对，使其成为第一阶段可优化的监督信号，从而在不依赖可微分梯度的条件下实现了跨阶段联合对齐。

### 补充图表

![[assets/figures/papers/paper_list_l2451_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Circular_DPO_Aligni/figures/003_Figure_3.jpg]]
*Figure 3: The overall framework of our Circular-DPO. In the first line, we review the generation process of Trellis. Our method is in the dashed box. We train the final 3D stage via DPO to generate optimized samples for constructing weighted preference pairs, which are subsequently utilized to optimize the preceding sparse structure model, thereby propagating preference signals to the preceding stage*

![[assets/figures/papers/paper_list_l2451_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Circular_DPO_Aligni/figures/001_Figure_1.jpg]]
*Figure 1: Overview of the Circular-DPO*

## 核心模块与公式推导

### 3.1 条件流匹配与 DPO 基础

**条件流匹配（Conditional Flow Matching, CFM）** 是 Trellis 多阶段生成模型的训练基础。给定噪声样本 $x_0 \sim p_0$ 和目标数据 $x_1 \sim p_1$，CFM 通过最小化预测速度场与线性插值方向之间的 L2 距离来训练生成器：

$$\mathcal { L } _ { \mathrm { CFM } } ( \theta ) = \mathbb { E } _ { t , x _ { 0 } \sim p _ { 0 } , x _ { 1 } \sim p _ { 1 } } \| v _ { \theta } ( x ( t ) , t ) - ( x _ { 1 } - x _ { 0 } ) \| _ { 2 } ^ { 2 }$$

其中 $v_\theta$ 为参数化的速度场，$x(t) = t x_1 + (1-t) x_0$ 为线性插值路径。该目标直接回归从噪声到数据的直线方向，避免了扩散模型中复杂的 score 估计。

**Flow-DPO 损失** 将 DPO 思想迁移到流匹配框架。给定偏好对 $(x_0^w, x_1^w)$（获胜样本）和 $(x_0^l, x_1^l)$（失败样本），通过比较参考模型 $\theta_{\mathrm{ref}}$ 与优化模型 $\theta_{\mathrm{opt}}$ 在两者上的 MSE 差异来建模偏好：

$$\mathcal { L } _ { \mathrm { DPO } } = - \mathbb { E } _ { x _ { 0 , 1 } ^ { w } , x _ { 0 , 1 } ^ { l } , t } \log \sigma \Bigg ( \beta \Big [ \big ( \mathrm { MSE } _ { t } ( x _ { 0 } ^ { w } , x _ { 1 } ^ { w } ; \theta _ { \mathrm { ref } } ) - \mathrm { MSE } _ { t } ( x _ { 0 } ^ { w } , x _ { 1 } ^ { w } ; \theta _ { \mathrm { opt } } ) \big ) - \big ( \mathrm { MSE } _ { t } ( x _ { 0 } ^ { l } , x _ { 1 } ^ { l } ; \theta _ { \mathrm { ref } } ) - \mathrm { MSE } _ { t } ( x _ { 0 } ^ { l } , x _ { 1 } ^ { l } ; \theta _ { \mathrm { opt } } ) \big ) \Big ] \Bigg )$$

其中 $\beta$ 控制偏好强度，$\sigma$ 为 sigmoid 函数。核心直觉是：优化模型应在获胜样本上比参考模型产生更小的 MSE（即更好的重建），而在失败样本上差距应更小或反向。

### 3.2 多阶段生成管道与不可微分瓶颈

**Trellis 两阶段架构**（Xiang et al., arXiv 2024）显式解耦了异质 3D 表示的生成：

- **Stage 1 — 稀疏结构生成器 $G_S$**：基于 Rectified Flow Transformer，从文本条件生成连续特征网格，经解码转换为离散稀疏体素结构 $x_{\mathrm{sparse}}$，定义全局拓扑和粗略形状。
- **Stage 2 — 结构潜变量生成器 $G_L$**：采用稀疏卷积 Transformer，以 $x_{\mathrm{sparse}}$ 为条件生成局部潜变量 $x_{\mathrm{slat}}$，编码精细几何与纹理信息。

两个阶段之间存在 **不可微分操作**（如体素化、离散化），导致 Stage 2 的损失梯度无法反向传播至 Stage 1。这意味着即使 Stage 2 生成质量不佳（如纹理与几何不一致），也无法通过梯度信号指导 Stage 1 调整稀疏结构。Figure 2 展示了这种纹理-几何不一致性的典型表现。

![[assets/figures/papers/paper_list_l2451_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Circular_DPO_Aligni/figures/002_Figure_2.jpg]]
*Figure 2: Demonstration of texture and geometry inconsistency*

### 3.3 偏好反馈循环的核心模块

Circular-DPO 的核心创新在于通过偏好对的构建与前馈，绕过不可微分瓶颈，实现端到端的多阶段对齐。整体框架如 Figure 3 所示，包含三个关键步骤：

**Step 1：最终阶段 DPO 优化。** 使用预处理的人类偏好数据集 $\mathcal{D}_{\mathrm{slat}}$，对 Stage 2 的 $G_L$ 进行 DPO 微调：

$$\min_{G_L} \mathcal{L}_{\mathrm{DPO}}(\mathcal{D}_{\mathrm{slat}}, G_L)$$

此步骤使 $G_L$ 学会生成更符合人类偏好的结构潜变量，从而产生更高质量的 3D 资产。

**Step 2：构建前馈偏好对。** 利用优化后的 $G_L^{\mathrm{opt}}$ 与未优化的 $G_L^{\mathrm{un\text{-}opt}}$ 分别生成 3D 资产，经 VAE 编码器重编码回稀疏表示 $x_{\mathrm{sparse}}$，构造偏好对 $(x_{\mathrm{sparse}}^{\mathrm{op}}, x_{\mathrm{sparse}}^{\mathrm{un\text{-}op}})$。这些偏好对将 Stage 2 的优化效果“编码”为可前馈的信号。

**Step 3：前置阶段引导。** 使用构造的偏好对训练 Stage 1 的 $G_S$：

$$\min_{G_S} \mathcal{L}_{\mathrm{DPO}}(\{ (x^{\mathrm{op}}, x^{\mathrm{un\text{-}op}}) \}, G_S)$$

由此，Stage 2 的偏好信号被闭环传递至 Stage 1，形成 **偏好反馈循环**（Figure 4）。

![[assets/figures/papers/paper_list_l2451_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Circular_DPO_Aligni/figures/004_Figure_4.jpg]]
*Figure 4: Cyclic Feedback in Multi-Stage Generation Processes*

### 3.4 质量感知加权机制

偏好数据中存在噪声（人类标注不一致、自动构造对不可靠），Circular-DPO 引入双层加权策略：

**质量差距权重 $w_1$：** 基于优化资产与未优化资产的偏好得分之差衡量偏好对质量：

$$w _ { 1 } = G _ { \mathrm { op } } - G _ { \mathrm { un-op } }$$

其中 $G$ 为基于人类排序的偏好概率转换得分。$w_1$ 越大，表示优化带来的质量提升越显著，偏好对越可靠。

**动态可靠性权重 $w_2$：** 基于奖励模型 $r$ 的对数似然为每个偏好对分配动态权重：

$$w _ { 2 } ( c , x ^ { w } , x ^ { l } ) = \frac { \exp ( h ) } { \mathbb { E } _ { \mathcal { D } } [ \exp ( h ) ] } , \quad h = \log \sigma ( r ( c , x ^ { w } ) - r ( c , x ^ { l } ) )$$

$w_2$ 对奖励模型置信度高的偏好对赋予更大权重，抑制低置信度噪声。

**最终损失函数：** 带加权的通用 DPO 损失为：

$$\mathcal{L}_{\mathrm{DPO}}(\mathcal{D}'; \mathrm{G}) = -\mathbb{E}_{(x_0^w, x_1^w), (x_0^l, x_1^l) \sim \mathcal{D}', t} \log \sigma \bigg( \beta T w_2 \Big[ \big( \mathrm{MSE}_t(x_0^w, x_1^w; \mathrm{G}^{\mathrm{ref}}) - \mathrm{MSE}_t(x_0^w, x_1^w; \mathrm{G}^{\mathrm{opt}}) \big) - \big( \mathrm{MSE}_t(x_0^l, x_1^l; \mathrm{G}^{\mathrm{ref}}) - \mathrm{MSE}_t(x_0^l, x_1^l; \mathrm{G}^{\mathrm{opt}}) \big) \Big] \bigg)$$

Circular-DPO 的最终损失仅对 $w_1 > \tau$ 的高质量偏好对计算 DPO 损失：

$$\mathcal { L } _ { \mathrm { Circular-DPO } } = \left\{ \begin{array} { l l } { \mathcal { L } _ { \mathrm { DPO } } } & { \mathrm { if ~ } w _ { 1 } > \tau } \\ { 0 } & { \mathrm { if ~ } w _ { 1 } \le \tau } \end{array} \right.$$

阈值 $\tau$ 在实验中设为零，即仅保留 $G_{\mathrm{op}} > G_{\mathrm{un\text{-}op}}$ 的有效偏好对。该机制从两个层面抑制噪声：$w_1$ 过滤低质量对，$w_2$ 在有效对内动态降权。消融实验（Table 2）证实，移除任一权重均导致生成质量下降和纹理-几何不一致性增加。

## 实验与分析

### 核心实验设置

实验基于 **Trellis**（Xiang et al., arXiv 2024）和 **MVDream**（Shi et al., arXiv 2023）两种多阶段 3D 生成 Backbone 进行评估。评估体系同时覆盖 2D 感知质量与 3D 结构质量：2D 指标包括 Aesthetic Score、HPSv2 和 ImageReward；3D 指标采用 Reward3D。此外，通过用户调研从文本一致性、3D 合理性、纹理细节、几何细节及纹理-几何一致性五个维度进行五分制主观评分，并统计参与者的二元偏好选择。

### 主实验结果

**Table 1** 报告了 Circular-DPO 与多种基线方法的定量对比。在 Trellis Backbone 上，Circular-DPO 在所有 2D 指标和 3D Reward 上均超越原始基线，其中 **ImageReward 指标提升 35.15%，Reward3D 指标提升 21.44%**。这一结果直接验证了偏好反馈循环机制的有效性——通过将最终阶段优化信号前馈至前置稀疏结构生成器，模型在纹理质量和几何一致性上获得了联合提升。

与各阶段独立进行 DPO 训练（DPO separately）的消融对比进一步揭示了反馈循环的核心贡献：Circular-DPO 在 ImageReward 上额外提升 14.11%，在 Reward3D 上额外提升 6.06%。这表明单纯的最终阶段 DPO 微调无法解决多阶段管道中的不可微分阻隔问题，只有通过构建“优化-未优化”偏好对并将信号前馈至第一阶段，才能实现跨阶段联合对齐。

在 MVDream Backbone 上的迁移实验同样取得了正向收益，证明了该方法对不同类型的多阶段 3D 生成架构具有一定的泛化能力。

**用户调研**（Figure 7）提供了最强的主观证据：近 70% 的参与者更偏好 Circular-DPO 生成的 3D 资产。在五分制评分中，Circular-DPO 在纹理-几何一致性维度上的优势尤为突出，这与方法设计目标——解决多阶段生成中的纹理几何不一致问题——高度吻合。

### 消融实验

**Table 2** 和 **Figure 6** 系统消融了 Circular-DPO 的关键组件：

- **移除质量权重 w1**（即不使用基于质量差距的偏好对过滤）：生成质量显著下降，出现明显的纹理-几何不一致现象。这证实了 w1 阈值过滤机制对于抑制低质量偏好对噪声的必要性——当优化资产与未优化资产的质量差距过小时，该偏好对缺乏有效的学习信号，强行使用反而会引入噪声。
- **移除偏好权重 w2**（即取消基于奖励模型对数似然的动态降权）：模型对偏好数据噪声的鲁棒性降低，性能同样变差。w2 的作用在于为更可靠的偏好对分配更高权重，其消融结果表明偏好数据本身存在不可忽略的噪声，动态加权是维持训练稳定性的关键设计。
- **仅对第二阶段进行 DPO 而不反馈至第一阶段（即独立 DPO）**：如主实验所述，提升幅度有限，进一步确认了反馈循环是不可替代的核心机制。
- **DPO 训练 vs. 传统后训练**：Figure 6 的定性对比显示，DPO 训练生成的资产纹理更丰富、整体质量更高，验证了在流匹配模型上使用 Flow-DPO 目标进行偏好优化的有效性。

![[assets/figures/papers/paper_list_l2451_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Circular_DPO_Aligni/figures/007_Figure_6.jpg]]
*Figure 6: Visual results of the ablation study*

### 失败模式与局限性

尽管 Circular-DPO 在相对提升幅度上表现突出，但论文明确指出其在定量指标上**尚未超越此前基于 Score Distillation 的方法**。这一局限可能源于该方法目前仅在流匹配模型（Flow Matching）上验证，而 Score Distillation 方法在优化目标和生成范式上存在本质差异。偏好反馈循环机制能否迁移到 Score Distillation 管道仍是一个开放问题。

此外，方法性能对偏好数据集质量存在依赖。尽管 w1 过滤和 w2 动态加权机制能有效缓解噪声影响，但在极端噪声场景下仍可能导致次优结果。这提示在实际部署中需要关注偏好标注的质量控制。

### 补充图表

![[assets/figures/papers/paper_list_l2451_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Circular_DPO_Aligni/figures/006_Table_1.jpg]]
*Table 1: Quantitative comparisons*

![[assets/figures/papers/paper_list_l2451_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Circular_DPO_Aligni/figures/008_Table_2.jpg]]
*Table 2: Ablation Study*

![[assets/figures/papers/paper_list_l2451_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Circular_DPO_Aligni/figures/005_Figure_5.jpg]]
*Figure 5: Qualitative Visual Results*

![[assets/figures/papers/paper_list_l2451_https_openaccess_thecvf_com_content_CVPR2026_html_Li_Circular_DPO_Aligni/figures/009_Figure_7.jpg]]
*Figure 7: User study results. Left: The generation effect that users prefer more. Right: The five-point scale score results for text consistency, 3D plausibility, texture details, geometric details, and texture-geometric consistency*

## 方法谱系与知识库定位

### 1. 核心瓶颈与因果机制

多阶段3D生成管道（如 **Trellis** (Xiang et al., arXiv 2024)）将稀疏结构生成与精细几何纹理生成解耦为两个阶段，但这一架构引入了一个根本性瓶颈：第二阶段生成的精细资产（纹理、几何）与第一阶段生成的稀疏结构之间存在**不可微分操作**（如离散化、体素化转换），导致第二阶段的偏好信号无法通过梯度反向传播到第一阶段，从而产生纹理-几何不一致性问题（见 Figure 2）。Circular-DPO 的因果调节杠杆在于：**绕过不可微分梯度阻隔，将偏好信号编码为可前馈的偏好对**——先对最终阶段进行 DPO 微调，生成优化后的资产与未优化资产构成偏好对，再将这些偏好对前馈至前置阶段进行 DPO 训练，形成闭合的偏好反馈循环。

### 2. 在方法谱系中的定位

#### 2.1 与多阶段3D生成基线的继承关系

Circular-DPO 以 **Trellis** 为默认 Backbone，完整保留了其两阶段架构：
- **第一阶段**：基于 Rectified Flow Transformer 的稀疏结构生成器 $G_S$，生成连续特征网格并转换为离散稀疏体素结构 $x_{sparse}$。
- **第二阶段**：以稀疏结构为条件的稀疏卷积 Transformer $G_L$，生成局部潜变量 $x_{slat}$，编码精细几何与纹理信息。

论文同时验证了该方法在 **MVDream** (Shi et al., arXiv 2023) 上的可迁移性——MVDream 是基于多视图扩散的3D生成方法，Circular-DPO 在其上同样取得了显著的性能提升（见 Table 1 中 OURS-MVDream 结果），表明偏好反馈循环机制不依赖于特定的生成架构。

#### 2.2 与 DPO 类方法的对比

- **DreamDPO** (Zhou et al., arXiv 2025)：对单阶段3D生成模型进行 DPO 对齐，但无法处理多阶段管道中的跨阶段信号传播问题。Circular-DPO 的核心超越在于将 DPO 从单阶段扩展到多阶段联合优化。
- **DPO separately（独立 DPO）**：对两个阶段分别进行 DPO 训练但不建立反馈循环，是本文的关键消融基线。实验表明，独立 DPO 的提升有限，而加入反馈循环后 ImageReward 额外提升 14.11%，Reward3D 额外提升 6.06%（置信度 0.95），直接验证了反馈循环的必要性。
- **Flow-DPO**：本文将 DPO 目标适配到 Flow Matching 框架，使用参考模型与优化模型在获胜/失败样本上的 MSE 差来区分偏好（见公式 Flow-DPO Loss），并进一步引入质量感知加权机制（$w_1$ 过滤低质量对，$w_2$ 动态降噪），这是对标准 DPO 在3D生成场景下的重要改进。

#### 2.3 与 Score Distillation 类方法的关系

论文在公平性说明中明确指出，Circular-DPO 在定量指标上尚未超越此前基于 Score Distillation 的方法。这一局限的根本原因可能在于：Score Distillation 方法利用预训练2D扩散模型提供逐像素梯度信号，而 Circular-DPO 依赖人类偏好数据集的偏好对质量。两者在信号粒度和优化机制上存在本质差异，目前 Circular-DPO 仅在 Flow Matching 模型上验证，能否推广到 Score Distillation 范式仍是开放问题。

### 3. 方法论贡献的适用边界

#### 3.1 适用条件
- **多阶段生成管道**：方法的核心假设是存在不可微分操作阻隔的阶段间梯度传播，因此适用于任何具有类似解耦架构的生成系统。
- **偏好数据可用性**：需要构建或获取人类偏好数据集（本文基于 DreamReward 的人类排序标注构建了3D偏好数据集），偏好数据的质量直接影响最终性能。
- **Flow Matching 框架**：当前的 DPO 目标公式基于 Flow Matching 的 MSE 近似，直接迁移到其他生成范式（如 DDPM、Score-based 模型）需要重新推导 DPO 目标。

#### 3.2 关键局限
1. **偏好数据噪声依赖性**：尽管引入了 $w_1$ 质量差距过滤和 $w_2$ 动态可靠性加权，极端噪声仍可能导致次优结果。消融实验（Table 2）显示，移除任一权重机制均导致生成质量下降，出现纹理几何不一致。
2. **两阶段架构验证**：当前仅在两级联管道上验证，对于三级以上级联的复杂架构，反馈循环的构建策略（如反馈路径选择、权重分配）需要重新设计。
3. **定量指标天花板**：在 ImageReward 和 Reward3D 上虽大幅超越基线（分别提升 35.15% 和 21.44%），但未超越 Score Distillation 方法的性能上限，表明偏好反馈循环可能无法完全替代基于梯度的精细优化。

### 4. 开放问题

1. **跨范式推广**：该偏好反馈循环机制能否推广到基于 Score Distillation 的3D生成任务？如果可以，DPO 目标应如何适配不同的生成范式？
2. **更深级联架构**：在多阶段生成架构更加复杂（如三级以上级联）的情况下，反馈循环的构建策略应如何调整？是否需要分层反馈或多跳传播机制？
3. **偏好数据效率**：当前需要构建完整的偏好对数据集，能否通过主动学习或在线偏好采样减少对大规模人类标注的依赖？
4. **与梯度信号的融合**：是否存在将偏好反馈循环与可微分梯度信号（如 Score Distillation）融合的可能性，以结合两者的优势？

## 原文 PDF

![[paperPDFs/CVPR_2026/Circular_DPO_Aligning_Multi_Stage_3D_Generative_Models_via_Preference_Feedback_Loop.pdf]]