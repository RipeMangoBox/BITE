---
title: "Composition of Memory Experts for Diffusion World Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Composition_of_Memory_Experts_for_Diffusion_World_Models.pdf
openreview_forum_id: sUEdpZCHdp
aliases:
- CMEC
- CMEDWM
tags:
- ICLR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: "将过去-未来一致性需求从单一架构中解耦，采用由对比式专家乘积（PoCE）驱动的异构记忆专家组合（短时、长时、空间）是突破这一瓶颈的关键调控变量。"
primary_logic: "通过将记忆分布到专门的专家并以对比方式抑制虚假模式，扩散世界模型可在不增加平方计算成本的前提下扩展上下文长度，同时提高预测质量与导航规划能力。"
claims:
- "CoME在所有记忆配置中取得最佳重建指标（LPIPS=0.097, SSIM=0.892, PSNR=23.07）。"
- "对比式专家乘积（PoCE）相比朴素乘积显著降低LPIPS（联合专家：无对比0.192 → 有对比0.097），避免模式坍缩。"
- "上下文长度从50帧增至480帧，LPIPS持续降低，未见饱和（在Memory Maze上）。"
- "CoME在RECON导航任务上取得ATE=0.96、RPE=0.28，显著优于NWM（ATE=1.13, RPE=0.35）等基线。"
---

# Composition of Memory Experts for Diffusion World Models

> [!tip] 核心洞察
> 通过将记忆分布到专门的专家并以对比方式抑制虚假模式，扩散世界模型可在不增加平方计算成本的前提下扩展上下文长度，同时提高预测质量与导航规划能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 扩散世界模型的记忆专家组合 |
| 英文题名 | Composition of Memory Experts for Diffusion World Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=sUEdpZCHdp) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Composition of Memory Experts (CoME) |
| Dataset | Memory Maze, RECON |

> [!tip] 效果简介
> - Memory Maze 上，LPIPS↓ 为 0.097，对比 0.209 (Base)，变化 −0.112 (↓53.6%)。
> - Memory Maze 上，SSIM↑ 为 0.892，对比 0.771 (Base)，变化 +0.121 (↑15.7%)。
> - RECON 上，ATE↓ 为 0.96，对比 1.13 (NWM)，变化 −0.17 (↓15.0%)。

## 概述

**核心问题**：世界模型需要记忆过去观测以预测未来，但传统架构面临根本性的记忆权衡——Transformer 能保留局部细节，其计算代价却随上下文长度平方增长；循环模型和状态空间模型虽可线性扩展，却因压缩历史而丧失长期保真度。单一架构难以同时兼顾短时细节与长程一致性。

**核心洞察**：CoME 将记忆需求从单一架构中解耦，分布到一组专门的记忆专家中，并通过**对比式专家乘积**（Product of Contrastive Experts, PoCE）进行概率融合。这一机制的关键在于：将每个条件专家与其无条件基线做加权几何混合，使融合时能主动抑制各专家分布中的虚假模式，而非简单叠加——从而在不引入平方计算代价的前提下，同时保留局部细节与长期记忆。

**方法定位**：CoME 实例化了三个互补的记忆专家：
- **短时记忆**（STM）：基于 DiT，在 33 帧滑动窗口上直接注意力，捕获局部动态；
- **长时记忆**（LTM）：在外部扩散模型权重上进行测试时 LoRA 微调，存储情景知识；
- **空间长时记忆**（SLTM）：以相机位姿等空间先验提供定位一致性。

三者通过 PoCE 融合为统一的分数函数进行采样。

**主要结果**：
- 在 Memory Maze 上，CoME 取得 LPIPS 0.097（较 Base 模型降低 53.6%），SSIM 0.892，PSNR 23.07，全面优于所有记忆配置（Table 1）；
- 上下文长度从 50 帧扩展至 480 帧时，LPIPS 持续降低且未出现饱和（Figure 1）；
- 在 RECON 导航基准上，CoME 的 ATE 为 0.96、RPE 为 0.28，显著优于 NWM（ATE 1.13, RPE 0.35）等基线（Table 2）；
- 消融实验证实，对比式专家乘积是性能提升的核心：联合专家在无对比时 LPIPS 为 0.192，加入 PoCE 后降至 0.097，有效避免了模式坍缩（Table 4）。

**局限与开放问题**：CoME 对组成专家的质量与容量较敏感；在剧烈动态变化环境或超长序列（>1000 帧）下的鲁棒性尚未验证；对比系数 $\alpha_i$ 的自适应选择及免梯度记忆机制仍需探索。

## 背景与动机

### 世界模型中的记忆瓶颈

世界模型的核心任务是基于观测历史预测未来状态，从而为智能体提供规划与决策的基础。然而，当前世界模型面临一个根本性的**记忆权衡**：模型要么保留丰富的局部细节，要么支持长程上下文，但难以兼得。

具体而言，基于 **Transformer** 的世界模型通过全局注意力机制直接访问历史帧，能够保留精细的时空细节，但其计算代价随上下文长度呈**平方增长**，使得扩展到长序列（如数百帧）在计算上不可行。作为替代，**循环模型**和**状态空间模型**（如 Mamba, Gu & Dao, 2024）通过压缩历史信息实现线性复杂度扩展，但这种压缩不可避免地**丢失了长期保真度**，导致在需要精确回忆远距离事件的场景中表现退化。

这一瓶颈在需要长期一致性的任务中尤为突出：例如导航任务要求智能体记住数百步之前的空间布局，或视频生成任务要求模型在镜头反转后准确召回初始场景。单一架构难以同时满足“保留细节”与“扩展上下文”这两个相互冲突的需求。

### 现有方法的局限性

现有工作试图通过不同策略缓解上述权衡，但各存在不足：

- **滑动窗口注意力**：将上下文限制在固定长度的近期窗口内，虽可控制计算成本，但完全丢弃了窗口之外的长期信息，无法支持跨越远距离的因果推理。
- **状态空间模型（SSM）**：通过隐状态压缩实现线性扩展，但压缩过程本身是信息有损的，导致长期重建质量随序列增长而衰减。
- **全注意力 Transformer**：作为理想上限，可在长上下文中保持高质量预测，但其平方级计算代价使其在实际部署中不可行。

这些方法的共同缺陷在于：它们将**过去-未来一致性需求**完全寄托于单一架构，迫使模型在“局部精度”与“全局覆盖”之间做出零和取舍。

### 本文动机

本文提出一种**解耦式记忆架构**，将记忆能力分布到多个**专门化的专家模型**中，而非依赖于单一模型。核心洞察在于：

> 通过将记忆分布到专门的专家并以对比方式抑制虚假模式，扩散世界模型可在不增加平方计算成本的前提下扩展上下文长度，同时提高预测质量与导航规划能力。

具体而言，本文引入 **Composition of Memory Experts (CoME)**，将记忆系统分解为三个互补的专家：

1. **短时记忆专家（STM）**：负责捕获局部动态与细节，基于近期上下文窗口（如33帧）操作。
2. **长时记忆专家（LTM）**：通过测试时微调将情景知识直接存储在外部扩散模型的权重中，支持数百帧乃至更长范围的回忆。
3. **空间长时记忆专家（SLTM）**：利用相机位姿等空间先验提供定位与空间一致性。

为将这些异构专家有效融合，本文提出**对比式专家乘积（Product of Contrastive Experts, PoCE）**策略。与朴素的专家乘积（PoE）不同，PoCE 通过引入对比基线抑制各专家产生的虚假模式，避免融合过程中的模式坍缩，从而在保持计算可控的前提下实现一致且高质量的长期预测。

## 核心创新

### 根本瓶颈：世界模型的记忆权衡

传统视频世界模型面临一个根本性的结构矛盾：**局部保真度与长期一致性不可兼得**。Transformer 架构通过全局注意力保留每一帧的细节，但其计算代价随上下文长度平方增长，难以扩展到长序列；循环模型（RNN）和状态空间模型（SSM，如 **Mamba**（Gu & Dao, 2024））虽可实现线性扩展，却因将历史压缩为固定维度的隐状态而丧失长期保真度。这一瓶颈迫使现有方法在“记住细节”和“看得够远”之间做出妥协。

### 核心调控变量：记忆的解耦与对比式融合

CoME 的关键创新在于将过去-未来一致性需求**从单一架构中解耦**，转而引入两个相互配合的调控变量：

1. **分布式记忆专家系统**：将记忆职责分配给多个专门化的专家模型，而非由单一模型承担全部记忆压力。
2. **对比式专家乘积（PoCE）融合**：在采样时以概率乘积方式融合异构专家，并通过对比机制抑制虚假模式。

这两个变量共同作用，使得世界模型能够在**不增加平方计算成本**的前提下扩展有效上下文长度，同时提升预测质量。

### 相对基线的关键变更（Changed Slots）

| 设计维度 | 基线方案 | CoME 方案 | 证据锚点 |
|---------|---------|----------|---------|
| **记忆架构** | 单一 Transformer，固定 3 帧上下文 | 分布式多专家系统：短时记忆（STM，33 帧滑动窗口）、长时记忆（LTM，100–1000 帧，测试时微调）、空间长时记忆（SLTM，相机位姿） | Sec 3.3 |
| **融合策略** | 无组合，仅靠单一模型预测 | 基于对比式专家乘积（PoCE）的概率融合，每个专家与其无条件基线对比后相乘，抑制虚假模式 | Eq (3), Sec 3.2 |
| **长时记忆实现** | 无长时记忆机制，只能通过增大上下文窗口扩展 | 在外部扩散模型权值上进行测试时 LoRA 微调，将情景知识存储于模型参数中 | Sec 3.3 |

### 创新一：分布式记忆专家系统

CoME 将记忆分解为三个互补的专家，各司其职：

- **短时记忆专家（STM）**：基于 DiT 架构，直接关注最近 33 帧的滑动窗口上下文 $c_{\mathrm{ST}}$，负责捕获局部动态与运动细节。
- **长时记忆专家（LTM）**：一个独立的扩散模型，通过测试时微调将长期历史 $\mathcal{C}_{\mathrm{LT}}$ 的情景知识存储在其权值 $\psi$ 中。使用 LoRA 适配器进行参数高效微调，既保留了预训练先验，又防止灾难性遗忘。
- **空间长时记忆专家（SLTM）**：基于空间先验 $S$（如相机位姿）提供定位与空间一致性约束，确保生成帧在全局空间中的连贯性。

这一设计的关键洞见在于：**不同类型的记忆需要不同的归纳偏置和存储机制**，强行用单一架构统一处理必然导致效率与保真度的折衷。

### 创新二：对比式专家乘积（PoCE）

朴素专家乘积（PoE）直接将各专家分布相乘：

$$p(\mathbf{x} \mid \mathcal{M}) \propto \prod_{i=1}^{K} p_i(\mathbf{x})$$

然而，当专家预测存在分歧时，PoE 会指数级放大不一致的模式，导致模式坍缩。CoME 引入对比式专家乘积（PoCE），将每个条件专家与其无条件基线 $\bar{p}_i$ 进行加权几何混合：

$$\tilde{p}_i(\mathbf{x}) \propto p_i(\mathbf{x})^{\alpha_i} \, \bar{p}_i(\mathbf{x})^{1-\alpha_i}$$

其中 $\alpha_i \ge 1$ 控制条件信息的强度。这一设计的核心机理是：**对比操作抑制了各专家分布中的虚假模式，同时保留了被多个专家共同支持的真实模式**。消融实验（Table 4）证实，加入对比机制后，联合专家的 LPIPS 从 0.192 降至 0.097，降幅达 49.5%。

### 完整融合形式

最终，CoME 将预训练先验 $p_\theta$、STM $p_\phi$、LTM $p_\psi$ 和 SLTM $p_\lambda$ 四个对比专家按统一分布融合（Eq 4），各专家权重由系数 $\alpha_0, \alpha_1, \alpha_2, \alpha_3$ 调节。这一框架具有良好的可扩展性——新增记忆类型只需添加对应的对比专家项，无需修改现有组件。

## 整体框架

![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_sUEdpZCHdp/figures/011_Figure_4.jpg]]
*Figure 4: Illustration of Mixture of Contrastive Experts. (a) Individual experts, modeled as Gaussian mixtures, modes are decreasing geometrically (from left to right). (b) Individual contrastive experts, with uniform modes. (c) Product of Experts, Exponentially scales PoE, Product of Contrastive Experts.PoCE suppresses inconsistent modes (e.g., the four rightmost peaks) while preserving the dominant left kernel. The vertical line indicates the center of probability mass for the PoE and PoCE*

CoME 将视频世界模型的记忆系统从单一架构中解耦，构建为一个**异构记忆专家的组合系统**。其核心思想是：不同的记忆需求（局部细节、长期一致性、空间定位）由专门的专家分别承担，并在采样时通过**对比式专家乘积（Product of Contrastive Experts, PoCE）** 进行概率融合，从而在不增加平方计算成本的前提下扩展有效上下文长度。

### 系统架构

CoME 的整体 pipeline 由四个核心模块组成，它们共享一个统一的扩散去噪框架，但在条件输入和参数更新策略上相互独立：

| 模块 | 角色 | 条件输入 | 参数策略 |
|------|------|----------|----------|
| **预训练先验** $p_\theta$ | 提供通用视频生成能力 | 短上下文 $c$（3帧） | 冻结 |
| **短时记忆（STM）** $p_\phi$ | 捕获局部动态与细节 | 滑动窗口 $c_{\text{ST}}$（33帧） | 独立训练 |
| **长时记忆（LTM）** $p_\psi$ | 存储情景知识 | 长时历史 $c_{\text{LT}}$（100-1000帧） | 测试时LoRA微调 |
| **空间长时记忆（SLTM）** $p_\lambda$ | 提供空间先验与定位 | 相机位姿 $S$ | 独立训练 |

### 信息流与融合机制

系统的输入输出流遵循以下流程：

1. **记忆编码阶段**：给定观测序列，STM 通过滑动窗口注意力直接编码最近 33 帧的视觉上下文；LTM 通过测试时微调将长时历史（可达数百帧）的情景知识存储到外部扩散模型的 LoRA 权重中；SLTM 则基于相机位姿等空间信息提供定位先验。

2. **组合采样阶段**：在生成未来帧时，各专家分别输出其条件分数函数。CoME 采用 **PoCE 融合策略**（式 4），将每个条件专家与其无条件基线进行对比式混合，然后通过乘积形式组合为统一分布：

$$
p_{\mathrm{CoME}}(\mathbf{x} \mid c, c_{\mathrm{ST}}, c_{\mathrm{LT}}, S) \propto 
\underbrace{\left[p_{\theta}(\mathbf{x} \mid \mathcal{Q})^{1-\alpha_0} p_{\theta}(\mathbf{x} \mid c)^{\alpha_0}\right]}_{\text{预训练先验}}
\underbrace{\left[p_{\phi}(\mathbf{x} \mid \mathcal{Q})^{1-\alpha_1} p_{\phi}(\mathbf{x} \mid c_{\mathrm{ST}})^{\alpha_1}\right]}_{\text{短时记忆}}
\times
\underbrace{\left[p_{\psi(\mathcal{Q})}(\mathbf{x} \mid c)^{1-\alpha_2} p_{\psi(c_{\mathrm{LT}})}(\mathbf{x} \mid c)^{\alpha_2}\right]}_{\text{长时记忆}}
\underbrace{\left[p_{\lambda}(\mathbf{x} \mid \mathcal{Q})^{1-\alpha_3} p_{\lambda}(\mathbf{x} \mid S)^{\alpha_3}\right]}_{\text{空间记忆}}
$$

其中 $\alpha_i \geq 1$ 控制各专家对最终预测的贡献强度，$\mathcal{Q}$ 表示空条件（无条件基线）。

3. **模式抑制机制**：PoCE 的关键创新在于，每个对比专家 $\tilde{p}_i(\mathbf{x}) \propto p_i(\mathbf{x})^{\alpha_i} \overline{p}_i(\mathbf{x})^{1-\alpha_i}$ 将条件分布与无条件基线进行加权几何混合。当 $\alpha_i > 1$ 时，该操作会抑制那些在无条件基线中已经存在的虚假模式，而保留条件信号特有的模式——这有效避免了传统专家乘积（PoE）中常见的模式坍缩问题（Figure 4 通过高斯混合示例直观展示了这一效果）。

### 关键设计决策

- **解耦记忆粒度**：STM 负责高保真局部细节（33 帧滑动窗口），LTM 负责长程一致性（测试时微调存储情景记忆），SLTM 负责空间定位——三者各司其职，避免了单一模型在记忆容量与计算效率之间的根本性权衡。

- **测试时微调作为记忆写入**：LTM 不通过增大上下文窗口来扩展记忆，而是在测试时对预训练扩散模型进行 LoRA 微调，将长时历史直接编码到模型权重中。这一设计使得记忆容量与推理时的计算开销解耦：记忆写入发生在微调阶段，采样时仅需标准的前向传播。

- **对比融合而非简单乘积**：消融实验（Table 4）表明，直接使用朴素专家乘积会导致性能退化（联合专家 LPIPS 从 0.097 升至 0.192），而 PoCE 通过对比基线抑制虚假模式，是实现稳定融合的关键。

## 核心模块与公式推导

### 3.1 扩散世界模型基础

CoME 建立在视频扩散世界模型之上。给定过去观测 $c$，模型学习预测未来帧 $\mathbf{x}$ 的条件分布。扩散过程定义为前向高斯加噪：

$$q(\mathbf{x}_t | \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1 - \beta_t} \mathbf{x}_{t-1}, \beta_t \mathbf{I})$$

训练目标采用简化去噪损失（预测噪声而非图像）：

$$\mathcal{L}(\theta) = \mathbb{E}_{\mathbf{x}_0, t, \epsilon \sim \mathcal{N}(0, \mathbf{I})} \left[ \lVert \epsilon - \epsilon_\theta(\mathbf{x}_t, t) \rVert^2 \right] \quad \text{(Eq 1)}$$

采样时通过反向 Langevin 动力学逐步去噪：

$$\mathbf{x}_{t-1} = \frac{1}{\sqrt{\alpha_t}} \left( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \epsilon_\theta(\mathbf{x}_t, t) \right) + \sigma_t \eta, \quad \eta \sim \mathcal{N}(0, \mathbf{I}) \quad \text{(Eq 2)}$$

该框架的核心瓶颈在于：单一扩散 Transformer（DiT）受限于固定短上下文窗口（如 3 帧），无法有效利用长程历史；而直接扩展上下文窗口会导致注意力计算代价平方增长。

### 3.2 对比式专家乘积（PoCE）

CoME 将记忆集成建模为**专家乘积（Product of Experts, PoE）**问题。给定完整记忆 $\mathcal{M}$ 被划分为 $K$ 个互补子集 $c_1, \ldots, c_K$，条件分布近似为各专家分布的乘积：

$$p(\mathbf{x} \mid \mathcal{M}) = p(\mathbf{x} \mid c_1, \ldots, c_K) \propto \prod_{i=1}^{K} p_i(\mathbf{x})$$

其中每个专家 $p_i$ 仅条件于其对应的上下文字集。然而，朴素 PoE 存在严重缺陷：当各专家分布的模式不完全一致时，乘积操作会**指数级放大虚假模式**，导致模式坍缩。

为解决此问题，CoME 引入**对比式专家乘积（Product of Contrastive Experts, PoCE）**。核心思想是将每个条件专家 $p_i$ 与其无条件基线 $\bar{p}_i$ 进行加权几何混合，形成对比专家 $\tilde{p}_i$：

$$\tilde{p}_i(\mathbf{x}) \propto p_i(\mathbf{x})^{\alpha_i} \bar{p}_i(\mathbf{x})^{1 - \alpha_i} \quad \text{(Eq 3)}$$

其中 $\alpha_i \geq 1$ 为对比系数。该形式的关键性质（**命题 1**）：在核密度估计框架下，若各核支持集互不相交，对比专家分布可写为：

$$\tilde{p}_i(\mathbf{x}) \propto \sum_{k=1}^{M} (\pi_k^i)^{\alpha_i} (\omega_k^i)^{1 - \alpha_i} h_k(\mathbf{x})$$

其中 $\pi_k^i$ 为条件专家下第 $k$ 个核的权重，$\omega_k^i$ 为基线下的对应权重。这表明 PoCE **仅重加权核的幅值而不改变其形状**，从而在抑制虚假模式的同时保留局部结构——这与简单温度调节（会同时收缩方差）有本质区别。当基线权重均匀时，进一步简化为 $\tilde{p}_i(\mathbf{x}) \propto \sum_k (\pi_k^i)^{\alpha_i} h_k(\mathbf{x})$。

最终，完整条件分布为所有对比专家的乘积：

$$p(\mathbf{x} \mid \mathcal{M}) \propto \prod_{i=1}^{K} \tilde{p}_i(\mathbf{x})$$

### 3.3 记忆专家实例化

CoME 实例化三个互补的记忆专家，每个对应不同的记忆角色：

**短时记忆专家（Short-Term Memory, STM）**：基于 DiT 架构，直接对近期上下文窗口 $c_{\text{ST}}$（33 帧滑动窗口）进行交叉注意力条件化。STM 负责捕获局部动态与细节纹理，但无法感知窗口外的历史信息。

**长时记忆专家（Long-Term Memory, LTM）**：一个独立的外部扩散模型，通过两条通道条件化：(1) 标准上下文条件 $c$（与预训练先验对齐）；(2) 在长程历史 $\mathcal{C}_{\text{LT}}$ 上进行**测试时 LoRA 微调**，将情景知识直接存储于权值 $\psi$ 中。LoRA 适配器提供隐式正则化，防止灾难性遗忘并保留通用先验。

**空间长时记忆专家（Spatial Long-Term Memory, SLTM）**：基于空间先验 $S$（如相机位姿序列）进行条件化，提供定位与空间一致性约束。其对比基线通过丢弃空间先验获得。

### 3.4 CoME 完整组合形式

将预训练先验 $p_\theta$、STM $p_\phi$、LTM $p_\psi$、SLTM $p_\lambda$ 代入 Eq (3) 的 PoCE 框架，得到 CoME 的完整分布：

$$p_{\text{CoME}}(\mathbf{x} \mid c, c_{\text{ST}}, c_{\text{LT}}, S) \propto \left[ p_\theta(\mathbf{x} \mid \mathcal{Q})^{1-\alpha_0} p_\theta(\mathbf{x} \mid c)^{\alpha_0} \right] \cdot \left[ p_\phi(\mathbf{x} \mid \mathcal{Q})^{1-\alpha_1} p_\phi(\mathbf{x} \mid c_{\text{ST}})^{\alpha_1} \right] \cdot \left[ p_{\psi(\mathcal{Q})}(\mathbf{x} \mid c)^{1-\alpha_2} p_{\psi(c_{\text{LT}})}(\mathbf{x} \mid c)^{\alpha_2} \right] \cdot \left[ p_\lambda(\mathbf{x} \mid \mathcal{Q})^{1-\alpha_3} p_\lambda(\mathbf{x} \mid S)^{\alpha_3} \right] \quad \text{(Eq 4)}$$

其中 $\mathcal{Q}$ 表示空条件（无条件基线），$\alpha_i \geq 1$ 控制各专家对比强度。采样时，该分布通过各专家分数函数的加权和实现：

$$\nabla_{\mathbf{x}_t} \log p_{\text{CoM}} = \sum_k \alpha_k \nabla \log p_k + (1 - \alpha_k) \nabla \log \bar{p}_k$$

该公式将四个异构专家的预测统一为单一去噪方向，在采样时完成融合，无需修改训练流程。

---

**关键机制总结**：CoME 通过 PoCE 将过去-未来一致性需求从单一架构中解耦，分布到专门的记忆专家。对比机制抑制虚假模式，使得联合分布集中在各专家一致的区域，从而在不增加平方计算代价的前提下扩展有效上下文长度。消融实验证实，移除对比机制（即朴素 PoE）会导致 LPIPS 从 0.097 退化至 0.192（Table 4），验证了 PoCE 是避免模式坍缩的关键设计。

## 实验与分析

### 核心瓶颈验证：上下文长度与重建质量

传统世界模型面临根本性的记忆权衡：Transformer 可保留局部细节，但计算代价随上下文长度平方增长；循环或状态空间模型虽可线性扩展，却因压缩历史而丧失长期保真度。CoME 通过将记忆分布到专门的专家并以对比方式抑制虚假模式，试图在不增加平方计算成本的前提下扩展上下文长度。

**Figure 1** 展示了在 Memory Maze 数据集上，上下文长度从 50 帧增至 480 帧时 LPIPS 持续降低，未见饱和。这一趋势表明，CoME 的记忆架构确实突破了单一 Transformer 模型面临的上下文扩展瓶颈——传统全注意力 Transformer 在此长度下计算代价已不可接受，而 CoME 通过异构专家组合实现了有效扩展。


![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_sUEdpZCHdp/figures/002_Figure_1.jpg]]
*Figure 1: (LPIPS ↓) as a function of context length on the Memory Maze dataset. Longer contexts lead to more faithful reconstructions, with no saturation observed up to 480 frames*

### 主实验结果

#### Memory Maze 重建质量

**Table 1** 汇总了不同记忆配置在 Memory Maze 上的重建指标。CoME 在所有配置中取得最优结果：LPIPS=0.097，SSIM=0.892，PSNR=23.07。相较于仅使用 3 帧上下文的 Base 模型（LPIPS=0.209），CoME 将 LPIPS 降低了 53.6%。单独使用短时记忆（STM）或长时记忆（LTM）均能带来增益，但完整组合（STM+LTM+SLTM）的效果显著优于任何单一专家，验证了异构记忆分布的必要性。


![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_sUEdpZCHdp/figures/001_Table_1.jpg]]
*Table 1: Comparison of different memory configurations on reconstruction metrics with two steps per frame. Best values are highlighted*

值得注意的是，全注意力 Transformer（200 帧上下文）作为理想上限，其 LPIPS 为 0.086，CoME 以 0.097 接近这一上限，却避免了平方级计算代价。Mamba 基线（SSM）的 LPIPS 为 0.131，虽优于 Base 但明显弱于 CoME，说明单纯的线性状态空间压缩仍不足以保留长程细节。

#### RECON 导航规划精度

**Table 2** 给出了 RECON 基准上的导航规划精度对比。CoME 取得 ATE=0.96、RPE=0.28，显著优于 NWM（ATE=1.13, RPE=0.35），以及 GNM（Shah et al., 2022）和 NOMAD（Sridhar et al., 2023）等专用导航方法。这一结果表明，高质量的世界状态预测直接转化为更优的规划能力——CoME 通过保持长程场景一致性，使导航策略能够基于更可靠的未来想象做出决策。


![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_sUEdpZCHdp/figures/003_Table_2.jpg]]
*Table 2: Planning accuracy on the RECON benchmark (100 sampled trajectories). We report Absolute Trajectory Error (ATE) and Relative Pose Error (RPE). Comparison of CoME with GNM Shah et al. (2022), NOMAD Sridhar et al. (2023) and NWM Bar et al. (2024)*

#### 语义记忆与场景召回

在 RealEstate10K 上（**Table 3**），CoME 的 LPIPS=0.359、PSNR=21.3、SSIM=0.83，全面优于 Base 模型（LPIPS=0.405）和 HG-t 基线。**Figure 3** 的定性结果进一步揭示了 CoME 的场景召回能力：在生成六帧前向轨迹后反转相机轨迹，CoME 能正确回忆初始帧的场景结构，而无长时记忆的 Base 模型则产生明显偏离。这说明 LTM 专家通过测试时微调确实将情景知识编码进了模型权重。


![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_sUEdpZCHdp/figures/005_Table_3.jpg]]
*Table 3: Comparison of evaluation metrics across different methods and rollout lengths on RealEstate10K. PSNR and SSIM (↑) indicate higher is better; LPIPS (↓) lower is better. Highlighting marks the best results*

在 Minecraft Marsh 数据集上（**Table 6**），CoME 同样一致改善感知与重建指标（LPIPS 从 0.408 降至 0.369），验证了方法在不同域上的泛化性。

### 消融实验：对比式专家乘积的关键作用

**Table 4** 直接检验了对比式专家乘积（PoCE）的有效性。在联合专家（STM+LTM）配置下，无对比的朴素乘积 LPIPS 为 0.192，加入对比机制后降至 0.114；完整 CoME（All）从 0.192 降至 0.097。这一消融揭示了朴素乘积的失效模式：当多个专家分布存在不一致的模式时，直接相乘会导致模式坍缩或相互抵消。PoCE 通过将每个条件专家与其无条件基线进行对比混合，抑制了虚假模式，同时保留了各专家捕获的有效信号。


![[assets/figures/papers/paper_list_l35_https_openreview_net_forum_id_sUEdpZCHdp/figures/007_Table_4.jpg]]
*Table 4: LPIPS results with and without the addition of the contrastive experts*

**Figure 4** 以高斯混合模型示意了这一机制：朴素乘积（PoE）会指数级放大主导模式，而对比式乘积（PoCE）能抑制不一致的右侧峰值，同时保留左侧主导核。

### 长时记忆适配能力分析

**Table 5** 探索了 LTM 的适配容量与上下文长度对 LPIPS 的影响。增大 LoRA 秩和上下文帧数可继续提升 LPIPS：在 450 帧上下文中，rank 256 的 LPIPS 为 0.118，而 rank 8 仅 50 帧时 LPIPS 为 0.193。然而，全量微调（Full）在相同条件下的 LPIPS 为 0.187，反而劣于 rank 256 的 LoRA 适配。这一反直觉结果说明 LoRA 提供了有益的正则化——全量微调在有限上下文上容易过拟合，而 LoRA 的低秩约束保留了预训练先验中的通用知识，仅在必要时进行适配。

### 计算开销与扩展性

CoME 的计算开销主要来自 LTM 的测试时微调。根据 **Table 9** 和 **Table 10**，使用 LoRA rank 64 时，记忆阶段引入约 4× 的计算开销；rank 16 时降至约 2×。考虑到 CoME 在 LPIPS 上相对 Base 模型 53.6% 的提升，这一开销在需要高保真长程预测的场景下是可接受的。论文未在超过 1000 帧的序列上评估计算扩展性，这需要进一步验证。

### 失败模式与局限

1. **专家质量敏感性**：CoME 假设所有专家均能提供合理且校准良好的预测。若某个专家表达能力严重受限（例如参数大幅缩减），融合结果可能退化。Table 4 中单独 SLTM 的 LPIPS 为 0.193，虽优于 Base 但明显弱于 STM 和 LTM，说明空间专家的贡献依赖于场景中空间先验的信息量。

2. **Langevin 修正无效**：论文在附录 D.3 中报告，Langevin 修正步骤在记忆增强扩散中并未带来生成质量增益。这表明在已通过 PoCE 融合多专家的条件下，额外的随机动力学步骤可能是冗余的。

3. **动态场景鲁棒性未充分验证**：论文未在剧烈动态变化的环境或更长序列（>1000 帧）上评估 SLTM 的鲁棒性。在 Memory Maze 和 RealEstate10K 等相对静态的场景中，空间先验的作用可能被高估。

4. **对比系数 α_i 的敏感性**：论文未系统探索 α_i 的选择策略。当前所有实验使用固定值，但在不同场景下，各专家的可靠性可能动态变化，固定系数可能导致次优融合。

## 方法谱系与知识库定位

### 核心瓶颈与设计动机

传统世界模型面临一个根本性的记忆权衡：**Transformer** 类架构通过全局注意力保留局部细节，但其计算代价随上下文长度平方增长，难以扩展到长序列；**循环模型**和**状态空间模型**（如 **Mamba**（Gu & Dao, 2024））虽可实现线性计算扩展，却因将历史压缩为固定维度的隐状态而丧失长期保真度。CoME 的核心洞察在于：**将过去-未来一致性需求从单一架构中解耦，转而采用由对比式专家乘积（PoCE）驱动的异构记忆专家组合**，从而在不增加平方计算成本的前提下扩展上下文长度，同时提高预测质量与导航规划能力。

### 方法谱系定位

CoME 处于**扩散世界模型**、**组合式生成**与**测试时自适应**三条技术路线的交汇点。

**相对于扩散世界模型基线**：基础扩散 Transformer（Base/DiT）仅以 3 帧上下文预测未来，缺乏任何形式的长期记忆。**滑动窗口注意力**（Sliding Window Attention）通过增大上下文窗口（如 33 帧）来扩展记忆，但受限于 Transformer 的计算代价且无法存储超出窗口的历史。**全注意力 Transformer**（Full Attention，200 帧上下文）可视为理想上限，但其平方复杂度使其在实际部署中不可行。**Mamba**（状态空间模型基线）以线性复杂度处理长序列，但压缩机制导致细节丢失。CoME 通过将记忆分布到多个专门专家（短时 33 帧、长时 100–1000 帧、空间位姿），在保持线性扩展特性的同时逼近全注意力上限的重建质量（Table 1：CoME LPIPS=0.097 vs Full Attention 0.087）。

**相对于组合式生成方法**：CoME 将记忆集成形式化为**专家乘积（Product of Experts, PoE）**问题，但其关键创新在于引入**对比式专家乘积（PoCE）**。朴素 PoE 在融合异构专家时容易发生模式坍缩——联合专家 LPIPS 从 0.192（无对比）恶化至不可用水平（Table 4）。PoCE 通过将每个条件专家与其无条件基线做加权几何混合（Eq 3），在保持局部形状的前提下抑制虚假模式（Figure 4 提供了高斯混合模型下的直观说明）。这一机制与传统的分类器自由引导（CFG）共享“对比”思想，但将其推广到多专家概率融合场景。

**相对于测试时自适应方法**：长时记忆专家（LTM）的核心机制是在外部扩散模型权值上进行**测试时 LoRA 微调**，将情景知识直接编码到模型参数中。这与传统的上下文窗口扩展或外部记忆库检索形成根本区别。Table 5 的消融表明，LoRA 秩从 8 增至 256 可带来 LPIPS 从 0.193 到 0.118 的持续改善，但全量微调反而退化至 0.187，表明 LoRA 提供了有益的正则化，防止对有限情景数据的过拟合。

**相对于导航与规划方法**：在 RECON 导航基准上，CoME 与 **GNM**（Shah et al., 2022）、**NOMAD**（Sridhar et al., 2023）和 **NWM**（Bar et al., 2024）进行了对比。CoME 取得 ATE=0.96、RPE=0.28，显著优于 NWM（ATE=1.13, RPE=0.35），证明记忆增强的世界模型可直接提升下游规划精度。

### 适用边界与局限

1. **专家质量依赖性**：CoME 假设所有组成专家均能提供合理且校准良好的预测。若某个专家表达能力严重受限（例如参数大幅缩减或训练不充分），融合结果可能退化。这一假设在常规实验设置下成立，但在资源受限场景中需要验证。

2. **容量敏感性与过拟合风险**：LTM 的测试时微调对 LoRA 秩和上下文帧数敏感。Table 5 显示，在低秩（rank=8）和短上下文（50 帧）设置下 LPIPS 为 0.193，而全量微调在上下文多样性不足时会过拟合（LPIPS 退化至 0.187 vs rank 256 的 0.118）。

3. **动态场景鲁棒性未充分验证**：论文未在剧烈动态变化的环境或更长序列（>1000 帧）上评估空间长时记忆专家（SLTM）的鲁棒性。Figure 1 显示 LPIPS 在 480 帧内未饱和，但更极端的序列长度下的行为仍是未知。

4. **计算开销**：LTM 的测试时微调引入额外计算成本。使用 LoRA rank=64 时，记忆步骤带来约 4× 计算开销（Table 9）；rank=16 时可降至约 2×。在实时或资源受限应用中，这一开销可能成为瓶颈。

5. **Langevin 修正步骤无效**：消融实验（Sec D.3）表明，在记忆增强扩散中引入额外的 Langevin 动力学修正步骤并未带来生成质量增益，提示标准扩散采样步已足够。

### 开放问题

- **对比系数 α_i 的自适应选择**：当前 α_i 为固定超参数，其在采样过程中的动态调整策略尚未探索。自适应机制可能进一步提升融合质量。
- **更长序列的记忆饱和效应**：在 >1000 帧及更高动态场景下，LTM 的 LoRA 容量是否会出现饱和，以及如何扩展专家容量，需要进一步研究。
- **免梯度记忆机制**：能否通过检索增强或外部记忆库替代测试时微调，以减少计算开销，是一个值得探索的方向。
- **视频扩散中的长程一致性**：确保长程生成中的场景一致性仍是开放挑战，特别是在相机轨迹反转等需要精确回忆的场景中。

## 原文 PDF

![[paperPDFs/ICLR_2026/Composition_of_Memory_Experts_for_Diffusion_World_Models.pdf]]
