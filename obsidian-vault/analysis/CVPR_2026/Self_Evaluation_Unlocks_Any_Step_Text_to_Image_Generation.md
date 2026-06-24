---
title: Self-Evaluation Unlocks Any-Step Text-to-Image Generation
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Self_Evaluation_Unlocks_Any_Step_Text_to_Image_Generation.pdf
project_link: null
code_link: null
aliases:
- SEMSE
- SEUASTIG
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用模型自身的当前分数估计对生成样本进行自评估，构建动态自教师信号，实现局部轨迹学习与全局分布匹配的统一。
primary_logic: 通过在训练中引入自评估损失，模型利用分类器自由引导(CFG)下的自身得分作为全局匹配信号，无需预训练教师即可在任意步数推理中保持高质量。
claims:
- 在GenEval基准上，Self-E在所有推理步数（2,4,8,50）均超越现有方法，尤其在2步时超越最强基线0.12（Table 1）
- 仅使用分类器得分项的自评估损失足以有效训练，并加速收敛（Table 2）
- Self-E性能随推理步数单调提升，实现超快速少步生成与高质量多步采样的统一（Table 1, Figure 5）
- GenEval 上 Overall Score = 0.753 (2 steps)
---

# Self-Evaluation Unlocks Any-Step Text-to-Image Generation

> [!tip] 核心洞察
> 通过在训练中引入自评估损失，模型利用分类器自由引导(CFG)下的自身得分作为全局匹配信号，无需预训练教师即可在任意步数推理中保持高质量。

| 字段 | 内容 |
|------|------|
| 中文题名 | 自评估解锁任意步数文本到图像生成 |
| 英文题名 | Self-Evaluation Unlocks Any-Step Text-to-Image Generation |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.22374) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Self-Evaluating Model (Self-E) |
| Dataset | GenEval |

> [!tip] 效果简介
> - GenEval 上，Overall Score 0.753 (2 steps) vs TiM 0.634 (2 steps) (+0.119)；Overall Score 0.781 (4 steps) vs TiM 0.687 (4 steps) (+0.094)；Overall Score 0.785 (8 steps) vs FLUX 0.589 (8 steps) (+0.196)。

## 概述

扩散模型与流匹配模型已成为文本到图像生成的主流范式，然而其高质量生成通常依赖数十甚至上百步的迭代去噪推理，计算成本高昂。现有加速方案大致分为两类：基于蒸馏的方法（如 **LCM**）需要预训练教师模型，限制了从零训练的能力；从零训练的少步方法（如 **IMM**）则仅依赖局部速度或分数监督，缺乏对全局分布的有效建模，在极低步数下质量下降显著。

本文提出 **Self-Evaluating Model (Self-E)**，一种无需预训练教师即可实现任意步数推理的文本到图像生成方法。其核心洞见在于：利用模型自身的当前分数估计对生成样本进行自评估，构建动态自教师信号，从而将局部轨迹学习与全局分布匹配统一到单一训练框架中。具体而言，模型在标准流匹配损失（学习从数据中预测 $\mathbf{x}_0$）的基础上，引入自评估损失——利用分类器自由引导（CFG）下的自身得分构造伪目标，驱动生成分布向真实分布靠拢。

**主要结果**：在 GenEval 基准上，Self-E 在所有推理步数（2、4、8、50 步）均达到最优性能，且总体得分随步数单调提升（0.753 → 0.781 → 0.785 → 0.815）。在 2 步推理的极端少步设置下，Self-E 以 0.753 的总体得分显著超越同期任意步数方法 **TiM**（0.634），领先幅度达 0.119。消融实验表明，仅使用分类器得分项的自评估损失即足以有效训练并加速收敛，而能量保持归一化与后期辅助项引入进一步提升了训练稳定性和少步生成质量。

**方法定位**：Self-E 属于从零训练的任意步数生成范式，区别于依赖蒸馏的 LCM 系列和仅做局部匹配的标准流匹配方法。其通过自评估机制实现“模型即教师”，为扩散/流匹配模型的训练提供了一种新的全局监督视角。

## 背景与动机

### 扩散与流匹配模型的核心瓶颈

当前主流的文本到图像生成模型，包括扩散模型（如 **SDXL**、**SANA-1.5**）和流匹配模型（如 **FLUX.1-dev**），均依赖于沿扩散轨迹的逐步去噪过程。这些模型在训练时仅接受局部速度或分数监督——即模型学习预测当前噪声状态到干净数据的瞬时变化方向。这种局部监督机制虽然保证了训练稳定性，却导致一个根本性缺陷：**模型缺乏对生成结果全局分布质量的感知能力**。

具体而言，给定正向扩散轨迹 $\mathbf{x}_t = \alpha_t \mathbf{x}_0 + \sigma_t \mathbf{\epsilon}$，传统流匹配方法通过最小化条件流匹配损失来学习速度场，该损失仅约束模型在单个时间点的预测与真实数据之间的局部一致性。由于模型从未在训练中“看到”自身生成样本的完整分布，它无法判断多步累积误差是否导致生成结果偏离真实数据分布。这一缺陷直接造成了**推理步数与生成质量之间的强耦合**：模型需要大量推理步数（通常50步以上）来保证局部近似的累积精度，否则少步推理将产生严重的语义失真和视觉伪影。

### 现有加速方案的局限性

为突破上述瓶颈，研究者提出了两类主要加速策略：

**蒸馏方法**（如基于潜空间的 **LCM**）通过将多步教师模型的生成轨迹压缩到少步学生模型中，实现了推理加速。然而，这类方法存在两个根本性限制：其一，必须依赖预训练的高质量教师模型，无法从零开始训练；其二，学生模型的上限受限于教师模型的能力，且蒸馏过程中的信息损失可能引入额外的分布偏移。

**从零训练的少步方法**（如基于矩匹配的 **IMM** 和同期提出的任意步数方法 **TiM**）试图通过设计新的训练目标来绕过对教师模型的依赖。IMM通过匹配生成分布与真实分布的矩来实现全局监督，TiM则探索了过渡模型框架下的任意步数生成。然而，这些方法在极少数步数（2-4步）下的性能仍显著落后于多步模型，且缺乏统一的框架来同时处理局部轨迹学习和全局分布匹配。

### 核心动机：从局部监督到自评估闭环

本文的核心洞察在于：**模型自身的当前分数估计本身就携带了关于生成样本质量的全局信息，无需外部教师即可构建有效的分布匹配信号**。具体而言，在分类器自由引导（CFG）框架下，模型对自身生成样本的条件得分与无条件得分之差，天然地指示了该样本在条件分布中的相对密度——这正是分类器得分的本质。

基于这一洞察，Self-E提出了一种自评估机制：在训练过程中，模型不仅从真实数据中学习局部轨迹，还利用其当前参数对自身生成的样本进行评分，并将该评分转化为伪目标信号进行回归。这形成了一个**内部反馈闭环**，使模型能够在训练中持续感知并修正其生成分布与真实分布之间的全局偏差，从而在任意推理步数下保持生成质量。该机制无需预训练教师模型，实现了局部轨迹学习与全局分布匹配的统一。

## 核心创新

### 瓶颈分析：局部监督与全局分布匹配的割裂

传统扩散模型和流匹配（Flow Matching）模型的核心训练范式存在一个结构性缺陷：它们仅依赖**局部速度/分数监督**。以条件流匹配（CFM）为例，模型学习的是从带噪样本 $\mathbf{x}_t$ 预测干净样本 $\mathbf{x}_0$ 的期望，其损失函数仅约束了单个时间步上的条件分布匹配。这种逐点监督虽然能有效学习局部轨迹，但缺乏对模型**生成分布全局结构**的感知能力。

由此带来的直接后果是：模型在少步推理时质量急剧下降，因为局部轨迹的累积误差无法被全局分布约束所纠正。为弥补这一缺陷，现有方法要么依赖多步迭代（增加推理成本），要么借助预训练教师模型进行蒸馏（如 LCM 依赖 SDXL 等教师模型），后者限制了从零训练（train from scratch）的可能性。

### 核心洞察：模型自评估实现全局分布匹配

Self-E 的核心创新在于**将模型自身的当前分数估计转化为全局监督信号**。具体而言，模型在训练过程中生成样本 $\hat{\mathbf{x}}_s$，然后利用分类器自由引导（CFG）下的自身得分构建一个**自评估伪目标** $\mathbf{x}_{\mathrm{self}}$，其梯度方向与真实分布和模型分布之间的分类器得分差一致：

$$\mathbf{x}_{\mathrm{self}} := \mathrm{sg} \big[ \hat{\mathbf{x}}_0 - [ G_{\theta}(\hat{\mathbf{x}}_s, s, s, \phi) - G_{\theta}(\hat{\mathbf{x}}_s, s, s, \mathbf{c}) ] \big]$$

其中 $\mathrm{sg}[\cdot]$ 表示停止梯度前向传播，$\phi$ 为空条件。这一构造的精妙之处在于：**无需任何外部教师模型**，仅利用模型自身在 CFG 下的条件得分差，就能生成指向全局分布匹配方向的伪目标。将这一自评估损失与数据重建损失结合，形成统一的训练目标：

$$\mathcal{L}_{s,t}(\theta) = \| \hat{\mathbf{x}}_0 - \mathbf{x}_0 \|_2^2 + \lambda_{s,t} \| \hat{\mathbf{x}}_0 - \mathbf{x}_{\mathrm{self}} \|_2^2$$

其中 $\lambda_{s,t} = \frac{\sigma_t}{\alpha_t} - \frac{\sigma_s}{\alpha_s}$ 是时间相关的自适应权重。

### 关键设计变更（Changed Slots）

相对于标准流匹配基线，Self-E 在三个维度上进行了关键修改：

| 设计维度 | 基线方法 | Self-E 方法 | 证据锚点 |
|:---|:---|:---|:---|
| **网络输入** | 仅接受时间 $t$ 和条件 $\mathbf{c}$ | 额外接受辅助时间 $s$，网络为 $V_\theta(\mathbf{x}_t, t, s, \mathbf{c})$ | Eq. (6) |
| **训练损失** | 仅 $\mathcal{L}_{\text{CFM}}$（数据重建） | $\mathcal{L}_{\text{data}} + \lambda \mathcal{L}_{\text{self-evaluate}}$，并采用能量保持归一化 | Eq. (16), Eq. (20) |
| **全局监督** | 无，仅局部速度匹配 | 通过自评估损失利用模型自身分类器得分进行全局分布匹配 | Sec. 3.2, Eq. (15) |

**网络输入的扩展**（$s$ 的引入）是支撑自评估机制的结构性前提——模型需要同时感知当前噪声水平 $t$ 和评估目标时间 $s$，才能在训练中统一处理数据学习和自评估两种模式。当 $s = t$ 时，模型退化为标准流匹配预测；当 $s < t$ 时，模型执行自评估，利用当前参数下的得分估计构建全局监督。

**能量保持归一化**（Energy-Preserving Normalization）是另一个关键设计。由于自评估伪目标 $\mathbf{x}_{\mathrm{self}}$ 与数据目标 $\mathbf{x}_0$ 的组合可能导致训练目标能量偏移，Self-E 引入归一化操作：

$$\mathbf{x}_{\mathrm{renorm}} = \frac{\mathbf{x}_0 + \lambda_{s,t} \mathbf{x}_{\mathrm{self}}}{\| \mathbf{x}_0 + \lambda_{s,t} \mathbf{x}_{\mathrm{self}} \|_2} \| \mathbf{x}_0 \|_2$$

该操作保持组合目标的 L2 范数与原始数据一致，改善了训练稳定性。消融实验（Table 2）证实，能量保持归一化在大多数推理步数下均带来性能提升，仅在极端 2 步设置下略有下降。

### 与现有方法的本质区别

Self-E 与现有少步生成方法的根本差异在于**去除了对预训练教师模型的依赖**。LCM 等蒸馏方法需要先训练一个多步教师模型，再将其知识蒸馏到少步学生模型中，这种两阶段范式限制了训练效率和可扩展性。IMM（矩匹配）方法虽支持从零训练，但仅通过分布矩进行约束，缺乏对生成分布精细结构的建模能力。TiM 作为同期任意步数方法，同样未引入自评估机制。

Self-E 通过**动态自教师信号**实现了局部轨迹学习与全局分布匹配的统一：模型既是学生（从数据学习局部速度），也是自身的教师（通过自评估提供全局分布监督）。这种设计使得模型在训练全过程中始终优于标准 Flow Matching 和 IMM（Figure 5），且在任意推理步数下均保持高质量生成。

## 整体框架

Self-E 的整体设计遵循一个核心原则：**让模型在从数据中学习局部轨迹的同时，利用自身当前能力对生成样本进行自评估，从而获得全局分布匹配的监督信号**。该框架无需预训练教师模型，即可实现从零开始的任意步数文本到图像生成训练。

### 双目标协同训练范式

模型训练由两个互补的目标驱动，形成“数据学习 + 自评估”的闭环结构（Figure 2）：

![[assets/figures/papers/paper_list_l2213_https_arxiv_org_abs_2512_22374/figures/002_Figure_2.jpg]]
*Figure 2: Self-Evaluating Model. (a) Overview. The model is trained with two complementary objectives: learning from data (b) and self-evaluation (c). (b) Learning from data. Given a real sample x0, we add noise to obtain xt and train*

1. **数据学习模块 (Learning from Data)**：遵循条件流匹配 (Conditional Flow Matching, CFM) 范式，将真实样本 $\mathbf{x}_0$ 加噪得到 $\mathbf{x}_t$，训练网络 $G_\theta(\mathbf{x}_t, t, s, \mathbf{c})$ 预测原始样本 $\mathbf{x}_0$。该模块提供**局部速度/轨迹监督**，损失函数为：
   $$\mathcal{L}_{\text{data}}(\theta) = \mathbb{E}_{s,t,\mathbf{x}_0,\epsilon} \left[ \| G_{\theta}(\mathbf{x}_t, t, s, \mathbf{c}) - \mathbf{x}_0 \|^2 \right]$$

2. **自评估模块 (Self-Evaluation)**：模型利用自身当前的分数估计，对生成样本 $\hat{\mathbf{x}}_s$ 进行自评估。核心机制是借助分类器自由引导 (CFG) 下的分类器得分项，构造一个伪目标 $\mathbf{x}_{\text{self}}$，其梯度方向与全局分布匹配的得分方向一致：
   $$\mathbf{x}_{\text{self}} := \text{sg} \big[ \hat{\mathbf{x}}_0 - [ G_{\theta}(\hat{\mathbf{x}}_s, s, s, \phi) - G_{\theta}(\hat{\mathbf{x}}_s, s, s, \mathbf{c}) ] \big]$$
   其中 $\text{sg}$ 为停止梯度算子，$\phi$ 为 CFG 的空文本条件。自评估损失最小化模型预测与该伪目标的均方误差：
   $$\mathcal{L}_{\text{self-evaluate}}(\theta) = \mathbb{E}_{t,s,\mathbf{x}_0,\epsilon} \left[ \| G_{\theta}(\mathbf{x}_t, t, s, \mathbf{c}) - \mathbf{x}_{\text{self}} \|^2 \right]$$
   该模块提供**全局分布匹配监督**，使模型在没有教师模型的情况下也能学习生成样本的整体分布特性。

### 关键设计：辅助时间输入

与传统流匹配模型仅接受时间 $t$ 和条件 $\mathbf{c}$ 不同，Self-E 的网络额外接受一个辅助时间 $s$，形式为 $V_\theta(\mathbf{x}_t, t, s, \mathbf{c})$。这一设计是自评估机制得以实现的基础：当 $s < t$ 时，模型被训练为不仅从当前噪声状态恢复原始样本，还要使其生成结果在更早的时间步 $s$ 处符合全局分布。

### 训练目标组合与归一化

最终逐样本训练目标为数据损失与自评估损失的加权组合：
$$\mathcal{L}_{s,t}(\theta) = \| \hat{\mathbf{x}}_0 - \mathbf{x}_0 \|_2^2 + \lambda_{s,t} \| \hat{\mathbf{x}}_0 - \mathbf{x}_{\text{self}} \|_2^2$$
其中自评估权重 $\lambda_{s,t} = \frac{\sigma_t}{\alpha_t} - \frac{\sigma_s}{\alpha_s}$ 由时间步动态决定。

为进一步提升训练稳定性和视觉质量，框架引入**能量保持归一化 (Energy-Preserving Normalization)**，对组合目标进行归一化处理，保持数据能量不变。

### 推理调度

训练完成后，模型支持任意步数推理。单步去噪更新规则为：
$$\mathbf{x}_{t_{k+1}} = \mathbf{x}_{t_k} - (t_k - t_{k+1}) V_\theta(\mathbf{x}_{t_k}, t_k, s_k, \mathbf{c})$$
其中辅助时间 $s_k$ 可在 $[t_{k+1}, t_k]$ 区间内灵活调节，以优化不同步数下的生成效果。

### 模块间关系总结

| 模块 | 输入 | 输出 | 监督类型 |
|------|------|------|----------|
| 数据学习 | $\mathbf{x}_t, t, s, \mathbf{c}$ | $\hat{\mathbf{x}}_0$ | 局部轨迹（真实 $\mathbf{x}_0$） |
| 自评估 | $\hat{\mathbf{x}}_s, s, \mathbf{c}, \phi$ | $\mathbf{x}_{\text{self}}$ | 全局分布（分类器得分） |
| 能量归一化 | $\mathbf{x}_0, \mathbf{x}_{\text{self}}$ | $\mathbf{x}_{\text{renorm}}$ | 稳定性正则 |
| 推理调度 | $\mathbf{x}_{t_k}, t_k, s_k, \mathbf{c}$ | $\mathbf{x}_{t_{k+1}}$ | 无（推理阶段） |

整个框架的核心创新在于**将局部轨迹学习与全局分布匹配统一在单一模型的训练过程中**，通过自评估机制动态构造教师信号，避免了传统蒸馏方法对预训练教师模型的依赖，实现了从零训练的任意步数高质量生成。

## 核心模块与公式推导

Self-E的核心架构由两个互补的训练模块构成：**数据学习模块**提供局部轨迹监督，**自评估模块**提供全局分布匹配信号。两个模块共享同一个速度场网络 $V_\theta(\mathbf{x}_t, t, s, \mathbf{c})$，该网络在标准流匹配输入（当前样本 $\mathbf{x}_t$、时间 $t$、条件 $\mathbf{c}$）的基础上，额外接受一个辅助时间 $s$，使其能够同时处理来自真实数据和模型自生成样本的监督。

### 数据学习模块

该模块遵循条件流匹配（Conditional Flow Matching, CFM）范式。给定真实数据 $\mathbf{x}_0$，通过正向扩散轨迹合成带噪样本：

$$\mathbf{x}_t = \alpha_t \mathbf{x}_0 + \sigma_t \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(0, \mathbf{I})$$

其中 $\alpha_t, \sigma_t$ 为噪声调度参数。模型学习预测原始数据 $\mathbf{x}_0$，损失函数为：

$$\mathcal{L}_{\mathrm{data}}(\theta) = \mathbb{E}_{s,t,\mathbf{x}_0,\boldsymbol{\epsilon}} \left[ \| G_{\theta}(\mathbf{x}_t, t, s, \mathbf{c}) - \mathbf{x}_0 \|^2 \right]$$

这里 $G_\theta$ 是网络的 $\mathbf{x}_0$ 预测输出。该损失等价于学习条件期望 $\mathbb{E}[\mathbf{x}_0|\mathbf{x}_t, \mathbf{c}]$，为模型提供沿扩散轨迹的局部速度监督。值得注意的是，辅助时间 $s$ 在此模块中与 $t$ 相同，仅作为网络输入的一致性接口。

### 自评估模块

自评估模块是Self-E的核心创新，它使模型能够**利用自身的当前分数估计对生成样本进行全局分布匹配**，无需依赖预训练教师模型。其推导逻辑如下：

**动机**：当 $s < t$ 时，模型从 $\mathbf{x}_t$ 预测的 $\hat{\mathbf{x}}_0$ 可进一步加噪得到 $\hat{\mathbf{x}}_s$。理想情况下，模型分布 $p_\theta(\mathbf{x}_s|\mathbf{c})$ 应匹配真实数据分布 $q(\mathbf{x}_s|\mathbf{c})$。这一全局匹配可通过最小化反向KL散度实现，其梯度涉及得分差：

$$\delta(\hat{\mathbf{x}}_s) = \nabla_{\hat{\mathbf{x}}_s} \log p_\theta(\hat{\mathbf{x}}_s|\mathbf{c}) - \nabla_{\hat{\mathbf{x}}_s} \log q(\hat{\mathbf{x}}_s|\mathbf{c})$$

**得分分解**：利用分类器自由引导（CFG）技术，上述得分差可分解为两项：

$$\delta(\hat{\mathbf{x}}_s) = (\omega - 1) \underbrace{\left( \nabla_{\hat{\mathbf{x}}_s} \log q(\hat{\mathbf{x}}_s | \phi) - \nabla_{\hat{\mathbf{x}}_s} \log q(\hat{\mathbf{x}}_s | \mathbf{c}) \right)}_{\text{分类器得分项}} + \underbrace{\left( \nabla_{\hat{\mathbf{x}}_s} \log p_{\theta}(\hat{\mathbf{x}}_s | \mathbf{c}) - \nabla_{\hat{\mathbf{x}}_s} \log q(\hat{\mathbf{x}}_s | \mathbf{c}) \right)}_{\text{辅助项}}$$

其中 $\phi$ 为空文本条件，$\omega$ 为引导强度。**分类器得分项**仅依赖真实数据分布的得分差，可通过模型自身在条件 $\mathbf{c}$ 和 $\phi$ 下的预测近似；**辅助项**则涉及模型分布与真实分布的得分差。

**伪目标构造**：为将得分差转化为可优化的回归目标，Self-E通过停止梯度（stop-gradient, $\mathrm{sg}$）构造伪目标：

$$\mathbf{x}_{\mathrm{self}} := \mathrm{sg} \big[ \hat{\mathbf{x}}_0 - [ G_{\theta}(\hat{\mathbf{x}}_s, s, s, \phi) - G_{\theta}(\hat{\mathbf{x}}_s, s, s, \mathbf{c}) ] \big]$$

该伪目标的梯度方向与分类器得分项一致。自评估损失即最小化模型预测与伪目标的均方误差：

$$\mathcal{L}_{\mathrm{self-evaluate}}(\theta) = \mathbb{E}_{t,s,\mathbf{x}_0,\boldsymbol{\epsilon}} \left[ \| G_{\theta}(\mathbf{x}_t, t, s, \mathbf{c}) - \mathbf{x}_{\mathrm{self}} \|^2 \right]$$

**关键实证发现**：仅使用分类器得分项（即省略辅助项）已足够有效，甚至能加速收敛（见Table 2）。辅助项若从头引入会显著降低性能，但在训练后期引入可减轻极少数步生成中的棋盘格伪影（见Figure 6）。

### 组合目标与归一化

最终逐样本训练目标为数据损失与自评估损失的加权组合：

$$\mathcal{L}_{s,t}(\theta) = \| \hat{\mathbf{x}}_0 - \mathbf{x}_0 \|_2^2 + \lambda_{s,t} \| \hat{\mathbf{x}}_0 - \mathbf{x}_{\mathrm{self}} \|_2^2$$

其中自评估权重 $\lambda_{s,t} = \frac{\sigma_t}{\alpha_t} - \frac{\sigma_s}{\alpha_s}$ 控制全局匹配信号的强度，随噪声水平自适应调节。为进一步改善训练稳定性和视觉质量，Self-E引入**能量保持归一化**，对组合目标进行范数保持缩放：

$$\mathbf{x}_{\mathrm{renorm}} = \frac{\mathbf{x}_0 + \lambda_{s,t} \mathbf{x}_{\mathrm{self}}}{\| \mathbf{x}_0 + \lambda_{s,t} \mathbf{x}_{\mathrm{self}} \|_2} \| \mathbf{x}_0 \|_2$$

消融实验表明，该归一化策略在除2步极端情况外的所有推理步数下均能提升性能（Table 2）。

### 任意步数推理

训练完成后，Self-E支持任意步数的去噪推理。给定时间网格 $\{t_k\}_{k=0}^{K}$，单步更新规则为：

$$\mathbf{x}_{t_{k+1}} = \mathbf{x}_{t_k} - (t_k - t_{k+1}) V_\theta(\mathbf{x}_{t_k}, t_k, s_k, \mathbf{c})$$

其中 $V_\theta$ 为速度场预测，辅助时间 $s_k$ 可在区间 $[t_{k+1}, t_k]$ 内调节以优化生成效果。这一灵活的推理调度使同一模型能够在2步到50步的广泛范围内保持高质量生成，实现少步效率与多步精度的统一。

## 实验与分析

### 核心定量结果：GenEval 基准上的任意步数性能

Self-E 在 GenEval 基准上实现了任意推理步数下的全面领先，且性能随步数单调递增。Table 1 报告了完整的定量对比：

![[assets/figures/papers/paper_list_l2213_https_arxiv_org_abs_2512_22374/figures/004_Table_1.jpg]]
*Table 1: Quantitative Comparison on GenEval [16]. Our method is consistently SOTA across all step counts and improves monotonically with more steps on GenEval Overall (2→4→8→50: 0.753→0.781→0.785→0.815). Notably, we achieve large margins in the few-step regime (e.g., +0.12 at 2-step over the best prior methods), while remaining the top performer at 8 and 50 Steps*

| 推理步数 | Self-E Overall Score | 最强基线及其分数 | 领先幅度 |
|---------|---------------------|-----------------|---------|
| 2 步 | 0.753 | TiM 0.634 | +0.119 |
| 4 步 | 0.781 | TiM 0.687 | +0.094 |
| 8 步 | 0.785 | FLUX 0.589 | +0.196 |
| 50 步 | 0.815 | 与 FLUX 等最强流匹配方法持平或超越 | — |

**关键结论**：
1. **少步优势显著**：在 2 步和 4 步的极端少步设定下，Self-E 对次优方法 TiM 的领先幅度分别达到 0.119 和 0.094，表明自评估机制在少步推理中提供了关键的全局分布约束。
2. **多步仍具竞争力**：在 50 步推理时，Self-E 与 FLUX 等参数量可能更大的模型持平或超越，说明自评估训练并未损害模型的多步推理能力上限。
3. **单调递增特性**：从 2 步到 50 步，Overall Score 从 0.753 单调上升至 0.815，验证了“超快速少步生成与高质量多步采样的统一”这一核心主张。

> **公平性说明**：所有对比方法在 GenEval 上使用统一评估协议，但部分基线模型规模不同（如 FLUX 参数量更大），Self-E 采用 2B 参数模型。

### 消融研究：自评估机制各组件的作用

Table 2 和 Figure 4–6 系统验证了 Self-E 各设计选择的贡献：

![[assets/figures/papers/paper_list_l2213_https_arxiv_org_abs_2512_22374/figures/006_Figure_4.jpg]]
*Figure 4: Controlled Ablation Study. We compare our method to alternative pretraining methods - Flow Matching and IMM. Full prompts appear in supplementary. Our method produces favorable results across all step budgets*

![[assets/figures/papers/paper_list_l2213_https_arxiv_org_abs_2512_22374/figures/008_Table_2.jpg]]
*Table 2: Controlled Ablation Study. We report overall scores on GenEval [16]. The upper block compares our method with two alternative design choices of omitting the target normalization or incorporating the auxiliary term throughout all training steps. Reported after 100K iterations. The bottom block compares our method with alternative pretraining methods - Flow Matching and IMM. Reported after 300K iterations*

#### 1. 自评估损失的核心地位

与两类替代预训练方案——标准 **Flow Matching (CFM)** 和基于矩匹配的 **IMM**——相比，Self-E 在训练全过程中始终显著优于二者（Table 2 底部区块，Figure 5）。Figure 5 进一步显示，Self-E 的 GenEval 分数随训练迭代快速攀升，且在所有推理步数（2/4/8/50）上均保持对 Flow Matching 的稳定优势，证实自评估损失不仅提升最终性能，还加速收敛。

![[assets/figures/papers/paper_list_l2213_https_arxiv_org_abs_2512_22374/figures/005_Figure_5.jpg]]
*Figure 5: Training Progress Comparison. GenEval scores across different inference steps (2, 4, 8, and 50) for our method and Flow Matching over training iterations (from 50k to 300k). Our approach consistently outperforms Flow Matching at all inference steps, indicating its superior effectiveness and robustness*

#### 2. 分类器得分项的充分性

自评估得分可分解为分类器得分项与辅助项两部分（Eq. 13）。实验表明，**仅使用分类器得分项已足够有效，甚至加速收敛**（Table 2）。这构成了方法的核心简洁性：模型利用 CFG 下的自身得分估计即可构建有效的全局匹配信号，无需额外的辅助监督。

#### 3. 辅助项的双刃剑效应

- **从头引入辅助项**：显著降低性能（Table 2 上部区块），表明训练初期引入辅助项会干扰分类器得分项的主导学习过程。
- **后期引入辅助项**：可减轻 2 步生成中的棋盘格伪影（Figure 6），但需在训练后期阶段引入以规避负面影响。这揭示了辅助项在极端少步伪影抑制中的实用价值，但其引入时机至关重要。

![[assets/figures/papers/paper_list_l2213_https_arxiv_org_abs_2512_22374/figures/007_Figure_6.jpg]]
*Figure 6: (Left) Models trained only with the classifier score component from Eq. (13) have clear checkerboard artifacts in extreme few-step regime, 2 steps in this example. (Right) Incorporating the auxiliary term from Eq. (13) in later stages of training helps mitigating these artifacts. Results are from our 2B model*

#### 4. 能量保持归一化的作用

能量保持归一化（Eq. 19–20）对组合训练目标进行归一化以保持数据能量。Table 2 显示，该策略**普遍提升性能**（除 2 步极端情况外），且改善了训练稳定性和视觉质量。论文在所有实验中均采用此策略。

### 定性结果：任意步数下的生成质量一致性

Figure 3 提供了 Self-E 与 FLUX、SDXL、SANA、LCM、TiM 等方法在不同推理步数下的定性对比。Self-E 在所有步数下均产出细节丰富、语义准确、与文本提示对齐的视觉结果，尤其在少步设定下，其他方法常出现语义丢失或伪影，而 Self-E 保持了良好的文本-图像一致性。

### 失败模式与局限性

1. **极端少步细节损失**：在 1–2 步推理时，图像细节清晰度不及 50 步推理，这是当前方法的固有局限。
2. **设计空间未充分探索**：损失权重方案 λ_{s,t} 和推理调度策略 s_k 的选择尚未充分优化，存在进一步提升空间。
3. **CFG 依赖**：当前方法依赖条件引导（CFG）推导分类器得分，难以直接扩展到无条件生成场景。
4. **下游任务未验证**：尚未在视频生成等任务中检验方法的迁移有效性。

### 补充图表

![[assets/figures/papers/paper_list_l2213_https_arxiv_org_abs_2512_22374/figures/001_Figure_1.jpg]]
*Figure 1: Qualitative Any-Step Generation. We showcase diverse text-to-image results from our model at different inference step counts, demonstrating coherent semantics, strong text alignment. Text prompts are provided in the supplementary material*

## 方法谱系与知识库定位

### 1. 与基线方法的关系

**Self-E** 的核心定位是**从零训练（training from scratch）的任意步数文本到图像生成模型**，其方法谱系可沿两条轴线展开：训练范式（蒸馏 vs. 从零训练）与生成框架（扩散 vs. 流匹配）。

#### 1.1 相对于蒸馏方法的突破

基于蒸馏的少步生成方法（如 **LCM**，即 Latent Consistency Models）依赖预训练教师模型提供蒸馏信号，这带来了两个根本性限制：(1) 需要先训练高质量教师模型，增加了总体计算开销；(2) 蒸馏过程受教师模型容量和质量的约束，难以超越教师。Self-E 通过**自评估机制**完全绕过了这一依赖——模型利用自身在分类器自由引导（CFG）下的当前分数估计作为全局匹配信号，实现了“自教师”（self-teaching）效果。这一设计使得从零训练任意步数模型成为可能，无需任何外部教师。

#### 1.2 相对于流匹配方法的改进

标准流匹配（**Flow Matching / CFM**）仅通过局部速度/分数监督进行训练，损失函数为 $\mathcal{L}_{\text{data}}$（Eq. 7），缺乏对生成分布全局结构的显式约束。这导致模型在少步推理时出现严重的分布偏移——局部轨迹的累积误差无法被全局信号纠正。Self-E 在数据学习损失之上引入**自评估损失** $\mathcal{L}_{\text{self-evaluate}}$（Eq. 15），将模型自身的分类器得分转化为全局分布匹配信号。这一设计的理论依据在于：自评估得分 $\delta(\hat{\mathbf{x}}_s)$ 中的分类器得分项（Eq. 13）直接指向真实条件分布 $q(\hat{\mathbf{x}}_s|\mathbf{c})$ 与无条件分布 $q(\hat{\mathbf{x}}_s|\phi)$ 之间的差异方向，从而提供了超越局部轨迹的全局监督。

与 **IMM**（矩匹配方法）相比，Self-E 不依赖显式的矩匹配约束，而是通过得分函数的梯度方向隐式地实现分布对齐。Table 2 的消融实验表明，Self-E 在训练全过程中始终显著优于 Flow Matching 和 IMM，验证了自评估机制的有效性。

#### 1.3 与同期任意步数方法的对比

**TiM**（Transition Models）是同期提出的任意步数文生图方法。在 GenEval 基准上，Self-E 在所有推理步数下均超越 TiM：2 步时 Overall Score 领先 0.119（0.753 vs. 0.634），4 步时领先 0.094（0.781 vs. 0.687）（Table 1）。这一差距在少步场景尤为显著，表明 Self-E 的自评估机制在极端少步推理中具有更强的分布校正能力。

#### 1.4 与大规模模型的竞争力

在 50 步推理设置下，Self-E（2B 参数）与更大规模模型（如 **FLUX.1-dev**）具有竞争力甚至超越（Table 1, Sec. 4.1）。考虑到参数量的差异，这一结果进一步凸显了自评估训练范式的效率优势。同时，Self-E 在 2 步、4 步、8 步设置下均显著超越 FLUX、**SDXL** 和 **SANA-1.5** 等扩散/流匹配模型。

### 2. 适用边界与关键设计约束

#### 2.1 对 CFG 的依赖

Self-E 的自评估机制依赖于 CFG 来构造分类器得分项（Eq. 13 中的 $(\omega-1)(\nabla_{\hat{\mathbf{x}}_s}\log q(\hat{\mathbf{x}}_s|\phi) - \nabla_{\hat{\mathbf{x}}_s}\log q(\hat{\mathbf{x}}_s|\mathbf{c}))$）。这意味着该方法**难以直接扩展到无条件生成设置**——当没有条件 $\mathbf{c}$ 和空条件 $\phi$ 的区分时，分类器得分项将退化为零。这一依赖是方法设计的结构性约束，而非工程性限制。

#### 2.2 网络输入的扩展

为支持自评估，Self-E 的网络 $V_\theta(\mathbf{x}_t, t, s, \mathbf{c})$ 额外接受辅助时间 $s$ 作为输入（Eq. 6）。这与标准流匹配模型仅接受 $t$ 和 $\mathbf{c}$ 不同。辅助时间 $s$ 在训练中用于指定自评估的目标噪声水平，在推理中可通过调整 $s_k$ 优化生成效果（Eq. 22）。这一设计增加了网络的输入维度，但带来的性能提升（Table 2）证明了其必要性。

#### 2.3 能量保持归一化的适用条件

能量保持归一化（Eq. 19-20）在大多数推理步数下普遍提升性能，但在**极端 2 步推理**场景下效果有限（Table 2 上栏）。这表明当推理步数极低时，组合目标的归一化策略可能需要更精细的调整。

### 3. 已知局限与失效模式

#### 3.1 极少步数下的细节退化

在 1-2 步推理场景下，图像细节清晰度不及 50 步推理。Figure 6 进一步揭示了仅使用分类器得分项训练的模型在 2 步生成中会出现**棋盘格伪影**（checkerboard artifacts）。引入辅助项（Eq. 13 中的第二项）并在训练后期激活可缓解该问题，但从头引入辅助项会显著降低性能（Table 2）。这表明辅助项的引入时机和权重是敏感的超参数。

#### 3.2 损失权重与推理调度的未充分优化

自评估权重 $\lambda_{s,t} = \frac{\sigma_t}{\alpha_t} - \frac{\sigma_s}{\alpha_s}$（Eq. 17）和推理调度策略 $s_k$ 的选择（Sec. 3.4）被作者明确标注为尚未充分优化的设计选择。这意味着当前报告的性能可能并非方法的上限，存在通过超参数搜索进一步提升的空间。

#### 3.3 下游任务验证的缺失

当前验证仅限于文本到图像生成任务，尚未在视频生成、图像编辑等下游任务中进行验证。自评估机制能否有效迁移到这些场景仍是一个开放问题。

### 4. 开放问题

1. **训练策略与推理调度的优化空间**：如何进一步改进损失权重方案和推理调度以提升少步生成质量？能否解耦推理时辅助时间 $s_k$ 与权重因子 $\lambda_{s,t}$ 的依赖以实现独立调节？

2. **下游任务微调的有效性**：Self-E 的自评估机制能否在下游任务微调中保持优势？微调过程中是否需要调整自评估损失的权重或形式？

3. **跨模态扩展**：能否将自评估范式扩展到视频生成模型？视频生成中的时序一致性是否会对自评估机制提出新的要求？

4. **无条件生成的适配**：如何将自评估机制适配到无条件生成设置？可能需要寻找 CFG 之外的替代方案来构造全局分布匹配信号。

5. **辅助项的引入策略**：辅助项在后期训练中引入可缓解伪影，但从头引入会损害性能。是否存在更优的引入策略（如渐进式激活、自适应权重）来平衡伪影抑制与训练稳定性？

## 原文 PDF

![[paperPDFs/CVPR_2026/Self_Evaluation_Unlocks_Any_Step_Text_to_Image_Generation.pdf]]
