---
title: Leveraging Verifier-Based Reinforcement Learning in Image Editing
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Leveraging_Verifier_Based_Reinforcement_Learning_in_Image_Editing.pdf
project_link: null
code_link: null
aliases:
- LVBRLIE
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将奖励模型从简单的整体打分器转变为基于原则分解和链式思维（CoT）的推理验证器（verifier-based RRM），使其能够对编辑结果进行细粒度、可解释的评估，从而提供高质量的训练信号。
primary_logic: 编辑指令可分解为一组可独立验证的原则（如「应保持不变的元素」「需遵循修改的要求」「整体视觉质量」），对每个原则进行逐一检查并聚合为最终分数，不仅能生成结构化、可解释的奖励，还能准确对齐人类偏好。
claims:
- 经过SFT冷启动和GCPO强化学习训练的7B Edit-RRM在内部基准上准确率达到82.2%，显著超过Seed-1.5-VL（79.3%）和编辑专用模型EditScore（65.9%），证明推理验证器优于传统整体打分器。
- GCPO算法通过群体对比偏好优化，将RRM在公开基准EditReward上的准确率从73.3%（仅SFT）进一步提升至78.2%，验证了强化学习对齐人类偏好的关键作用。
- 在人类评估中，经Edit-R1优化的FLUX.Kontext模型获得了+23.2的GSB评分，显著优于基线，证明基于验证器的RLHF能切实提升编辑质量与指令遵循能力。
- Internal Reward Benchmark 上 Accuracy = 82.2% (7B RL-RRM)
---

# Leveraging Verifier-Based Reinforcement Learning in Image Editing

> [!tip] 核心洞察
> 编辑指令可分解为一组可独立验证的原则（如「应保持不变的元素」「需遵循修改的要求」「整体视觉质量」），对每个原则进行逐一检查并聚合为最终分数，不仅能生成结构化、可解释的奖励，还能准确对齐人类偏好。

| 字段 | 内容 |
|------|------|
| 中文题名 | 基于验证器强化学习的图像编辑方法 |
| 英文题名 | Leveraging Verifier-Based Reinforcement Learning in Image Editing |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.27505) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Edit-R1 |
| Dataset | Internal Reward Benchmark, EditRewardBench, GEdit-Bench-EN, Human Evaluation |

> [!tip] 效果简介
> - Internal Reward Benchmark 上，Accuracy 82.2% (7B RL-RRM) vs 79.3% (Seed-1.5-VL) (+2.9%)。
> - EditRewardBench (public) 上，Accuracy 78.2% (RL-RRM 7B) vs 65.9% (EditScore 7B) (+12.3%)。
> - GEdit-Bench-EN (FLUX.Kontext family) 上，Overall Score (O) 6.24 (RL w. RL-RRM 7B) vs 5.77 (FLUX.Kontext) (+0.47)。

## 概述

图像编辑任务要求模型精确理解并执行复杂的编辑指令，然而，现有的奖励模型（Reward Model）普遍采用整体打分范式，仅输出一个标量分数，无法解释模型在哪些具体指令要求上成功或失败。这种粗粒度反馈不仅容易产生有偏甚至幻觉性的奖励信号，也严重阻碍了基于人类反馈的强化学习（RLHF）在图像编辑领域的有效应用。

针对这一瓶颈，本文提出 **Edit-R1**，一个以**可推理验证器（Verifier-based Reasoning Reward Model, RRM）** 为核心的框架。其核心洞见在于：编辑指令可以被分解为一组可独立验证的原则——例如“应保持不变的元素”（Keep）、“需遵循的修改要求”（Follow）以及“整体视觉质量”（Quality）——奖励模型只需逐项检查编辑结果是否满足这些原则，并聚合为最终分数，即可生成结构化、可解释且与人类偏好高度对齐的细粒度奖励。

为实现这一目标，Edit-R1 构建了一个两阶段训练流程：首先通过冷启动监督微调（SFT）让模型学会基于原则分解的链式思维（CoT）推理与逐项评分；随后引入**群体对比偏好优化（Group Contrastive Preference Optimization, GCPO）** 算法，利用人类偏好对进一步强化 RRM 的推理对齐能力。训练完成的 RRM 作为一个非可微但高质量的奖励信号，通过 GRPO 算法直接优化下游编辑模型（如 FLUX.Kontext、Qwen-Edit）的流匹配过程。

核心实验结果验证了该范式的有效性：

- **奖励模型评估**：经过完整两阶段训练的 7B Edit-RRM 在内部基准上达到 **82.2%** 的准确率，显著优于闭源通用视觉语言模型 Seed-1.5-VL（79.3%）和编辑专用模型 EditScore（65.9%）；在公开基准 EditReward 上，GCPO 将准确率从仅 SFT 的 73.3% 进一步提升至 **78.2%**，证明了强化学习对齐人类偏好的关键作用。
- **下游编辑性能**：在 GEdit-Bench-EN 上，以 RL-RRM 为奖励信号优化的 FLUX.Kontext 模型获得 **6.24** 的综合评分，较基线提升 0.47；人类评估中，该模型获得 **+23.2** 的 GSB 评分，表明基于验证器的 RLHF 能切实提升编辑质量与指令遵循能力。

消融实验进一步揭示：SFT 阶段同时保留“思考”（Think）与“验证”（Verify）模块可获得最优性能；GCPO 在仅使用约 1 万人类偏好对（不到 SFT 数据的 1%）的情况下，仍能稳定提升约 4.9 个百分点，说明增益主要来源于人类对齐质量而非数据量；模型从 3B 扩展至 7B 时呈现出良好的可扩展趋势。此外，RL-RRM 作为奖励信号比仅 SFT 的 RRM 更为严格和鲁棒，能有效纠正编辑模型在微调中产生的幻觉问题（如错误修改未指定的属性）。

## 背景与动机

图像编辑任务要求模型在保留源图像无关区域的同时，精确执行用户指令所描述的局部修改。近年来，随着扩散模型和流匹配模型的快速发展，图像编辑的生成质量取得了显著进步。然而，**编辑结果与人类意图之间的精确对齐**仍然是一个核心挑战——模型常常出现属性泄露（如修改衬衫颜色时意外改变帽子颜色）、指令遵循不完整，或生成不符合物理规律的视觉伪影。

### 现有奖励模型的根本缺陷

将强化学习从人类反馈（RLHF）引入图像编辑，理论上可以弥合这一对齐鸿沟。但该路径面临一个关键瓶颈：**缺乏可解释的细粒度奖励模型**。现有的奖励模型几乎全部采用“整体打分器”范式——它们接收一张编辑图像和一条指令，直接输出一个标量分数，而不解释该分数如何得出、也不区分指令中不同约束的满足程度。

这种黑箱评分机制带来了三个严重问题：

1. **有偏反馈**：整体打分器可能过度关注图像的视觉质量，而忽略指令中某些细粒度要求（如“只改变颜色，保持纹理不变”），导致奖励信号与真实编辑质量之间出现系统性偏差。
2. **幻觉风险**：模型可能对未实际发生的修改给出高分，或对正确执行的编辑给出低分，因为缺乏逐项核验的机制。
3. **训练信号粗糙**：单一标量无法为编辑模型的策略优化提供结构化指导——模型不知道自己在哪条原则上失分，也就难以针对性改进。

这一缺陷在现有方法的性能对比中得到了印证：编辑专用评分模型 **EditScore**（7B）在公开基准 EditReward 上的准确率仅为 65.9%，甚至低于通用视觉语言模型 **Seed-1.5-VL** 的 79.3%，说明简单的微调策略并未解决奖励建模的核心问题。

### 本文的核心动机

Edit-R1 的提出源于一个关键洞察：**编辑指令天然可分解为一组可独立验证的原则**。例如，“将红色衬衫改为蓝色，保持其他元素不变”这条指令，可以拆解为三个原则：（1）衬衫颜色应变为蓝色（遵循修改要求）；（2）除衬衫外的所有元素应保持不变（保持约束）；（3）编辑结果应保持整体视觉质量（质量约束）。

基于这一洞察，Edit-R1 将奖励模型从“整体打分器”重构为“推理验证器”：它首先将编辑指令分解为可验证的原则集合，然后对每条原则逐一进行链式思维推理和核验，最终聚合为结构化、可解释的细粒度奖励。这一范式转变使得奖励信号不仅更准确地对齐人类偏好，还能为下游编辑模型的优化提供可操作的反馈。

## 核心创新

Edit-R1 的核心创新在于对图像编辑奖励模型进行了**范式级重构**，将奖励信号从不可解释的整体打分器升级为可推理、可验证的细粒度评估器，并以此为基础构建了完整的编辑模型强化学习优化闭环。具体而言，该方法在以下三个关键维度上实现了突破。

### 从整体打分到推理验证的范式转变

现有图像编辑奖励模型（如 **Seed-1.5-VL**、**EditScore**）普遍采用整体打分范式——直接为编辑结果输出一个标量分数。这种“黑箱”评分方式存在根本性缺陷：它无法区分编辑指令中不同子要求的满足程度，容易产生有偏甚至幻觉反馈，严重阻碍了 RLHF 在图像编辑任务中的有效应用。

Edit-R1 提出了一种**基于验证器的推理奖励模型（Verifier-based RRM）**，其核心机制是将编辑指令分解为一组可独立验证的原则（遵循“应保持不变的元素”、“需执行的修改要求”、“整体视觉质量”三类），然后对每个原则逐一进行链式思维（CoT）检查，最终聚合为结构化、可解释的细粒度奖励。这一转变使得奖励模型从“打分器”进化为“验证器”，从根本上解决了传统方法的可解释性缺失问题。

### 两阶段训练策略：冷启动 SFT + GCPO 强化学习

Edit-R1 为推理奖励模型设计了独特的两阶段训练流程，以同时获得推理能力和人类偏好对齐能力：

- **冷启动 SFT**：利用大规模自动生成的四元组数据（参考图、指令、原则分解、编辑候选），通过外部 VLM 质量验证筛选出最高准确率的 CoT 推理轨迹，对基座模型进行监督微调。这一阶段赋予模型初步的原则分解与逐项验证能力。
- **GCPO（Group Contrastive Preference Optimization）**：提出一种基于组间对比的偏好优化算法。对于每个人类标注的偏好对，RRM 为偏好图像和非偏好图像各生成 N 个评分候选，通过组间成对比较计算赢/输比率作为奖励信号，再在组内进行优势归一化。该算法在仅使用约 1 万人类标注对（不到 SFT 数据的 1%）的情况下，将 RRM 准确率稳定提升约 4.9 个百分点，证明增益源于人类对齐质量而非数据量。

### 非可微奖励驱动的编辑模型优化

由于 RRM 在推理过程中需要生成离散的 CoT 文本，其奖励信号不可微，无法直接用于基于梯度的策略优化。Edit-R1 通过将训练好的 RL-RRM 作为非可微奖励信号，与标准 **GRPO 算法**结合，优化下游编辑模型的流匹配过程。实验表明，使用经 GCPO 训练的 RL-RRM 作为奖励信号，比仅用 SFT-RRM 能获得更高且更稳定的评价奖励，表明 RL-RRM 是更严格、更鲁棒的评估器。这一设计使得基于验证器的推理奖励能够切实反哺编辑模型的生成质量提升，形成完整的“推理验证→偏好对齐→策略优化”闭环。

### 方法谱系与知识库定位

从奖励模型的设计谱系来看，Edit-R1 的 RRM 是目前唯一同时具备以下三项推理增强特性的图像编辑奖励模型：**显式使用可验证原则（as verifier）**、**链式思维推理（thinks）**、**强化学习对齐（RL）**。相较于仅依赖 VLM 整体评分的 Seed-1.5-VL、Seed-1.6-VL，以及编辑专用的 EditScore，Edit-RRM 在建模范式上实现了从“评分”到“验证”的跨越。在训练策略上，相较于传统的单一阶段 SFT，Edit-R1 引入的 GCPO 算法通过组间对比机制有效利用了人类偏好数据，为奖励模型的 RL 训练提供了新的范式参考。

## 整体框架

Edit-R1 的整体框架围绕一个核心组件——**基于验证器的推理奖励模型（Verifier-based Reasoning Reward Model, RRM）**——构建，并将其作为下游图像编辑模型强化学习的训练信号。该框架包含三个逻辑阶段：（1）将编辑指令分解为可独立验证的原则集合；（2）通过冷启动监督微调（SFT）与群体对比偏好优化（GCPO）两阶段训练，得到一个能生成可解释、细粒度奖励的 RRM；（3）利用训练好的 RRM 作为非可微奖励信号，通过 GRPO 算法优化下游编辑模型。

### 原则分解与输入四元组

框架的起点是将一条自由形式的编辑指令转化为一组结构化的、可验证的原则。具体而言，对于每张参考图像及其对应的编辑指令，系统首先利用外部 VLM（如 Seed-1.5-VL）将任务分解为三类原则：

- **Keep（应保持不变的元素）**：编辑后图像中必须保留的源图像属性；
- **Follow（需遵循的修改要求）**：指令明确要求的编辑操作；
- **Quality（整体视觉质量）**：图像的自然度、一致性等感知质量指标。

分解后的原则集合 $\mathcal{P}$ 与源图像、编辑指令、编辑后的图像共同构成一个**四元组（quadruple）**，作为 RRM 的输入。该四元组的生成采用多模型策略：使用多个编辑模型为同一（源图像，指令）对生成多个编辑候选，形成大规模训练数据池。

### 奖励模型训练流水线

RRM 的训练是一个两阶段过程，如 Figure 2 所示。

**阶段一：冷启动 SFT（Cold-Start SFT）**
此阶段的目标是赋予 RRM 基本的链式思维（Chain-of-Thought, CoT）推理与逐原则验证能力。具体流程为：
1. 利用 VLM 池对每个四元组生成多条推理轨迹，每条轨迹包含“思考（Think）”过程和“验证（Verify）”评分；
2. 使用外部 VLM 作为“质量控制裁判”，重新评估每条推理轨迹中每个原则判断的正确性，计算验证准确率；
3. 选择准确率最高的 CoT 轨迹构建 SFT 数据集，对基础模型进行监督微调，得到 **SFT-RRM**。

**阶段二：GCPO 强化学习（Reasoning-Reinforced Reward Learning）**
此阶段利用人类标注的偏好对（约 10k 对，不足 SFT 数据的 1%）进一步对齐人类偏好。GCPO 的核心机制是**组间对比、组内优势**：
- 对于每个偏好对（胜者图像 $x^w$，败者图像 $x^l$），RRM 为每张图像生成 $N$ 条思维链评分候选；
- 计算**赢/输比率奖励**：胜者候选的赢比率等于其分数高于败者组所有候选分数的比例，败者候选的输比率等于其分数低于胜者组所有候选分数的比例；
- 在胜者组和败者组内部分别计算优势函数 $A^w$ 和 $A^l$，并应用 PPO 风格的裁剪替代损失进行策略优化，得到 **RL-RRM**。

GCPO 的损失函数（省略 KL 散度项）为：

$$\mathcal{L}_{\mathrm{GCPO}}(\phi) = \mathbb{E} \left[ \frac{1}{2N} \sum_{j=1}^N \frac{1}{T} \sum_{t=0}^{T-1} \left( \min(r_{t,j}^w A_j^w, \mathrm{clip}) + \min(r_{t,j}^l A_j^l, \mathrm{clip}) \right) \right]$$

### 下游编辑模型优化

训练完成的 RL-RRM 作为一个**不可微的奖励信号**，被集成到标准的 GRPO 算法中以优化下游编辑模型。具体而言，在流匹配（flow matching）的推理过程中，编辑模型为同一输入生成 $G$ 个编辑候选（组大小 $G=24$），RRM 对每个候选进行逐原则验证并提取标量分数 $\tau_i$，然后计算组内标准化优势：

$$A_i = \frac{\tau_i - \mathrm{mean}(\{\tau_i\})}{\mathrm{std}(\{\tau_i\}) + \epsilon_{\mathrm{std}}}$$

编辑模型通过最大化期望优势进行策略更新，同时采用裁剪目标函数和 KL 散度惩罚项（系数 $\beta=0.04$）来保证训练稳定性。

### 模块关系与数据流

整个框架的数据流可概括为：
1. **指令 → 原则分解**：外部 VLM 将编辑指令转化为结构化原则集合；
2. **图像生成 → 四元组构建**：多编辑模型生成候选，形成（源图，指令，原则，编辑图）四元组；
3. **CoT 推理 → 评分**：RRM 对四元组进行逐原则验证，生成结构化评分；
4. **SFT → GCPO**：先通过高质量 CoT 数据冷启动，再通过人类偏好对强化对齐；
5. **RRM → GRPO**：RL-RRM 作为奖励信号，驱动下游编辑模型的流匹配过程优化。

该设计的核心优势在于：奖励模型不再是黑盒的整体打分器，而是一个可解释的推理验证器，其输出的逐原则评分不仅为编辑模型提供了细粒度的训练信号，也使得整个优化过程具有可审计的透明度。

### 补充图表

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/001_Figure_1.jpg]]
*Figure 1: Our framework: from verifier-based reasoning reward model (RRM) to downstream. (a) Verifier as a reasoning reward model. The RRM decomposes an instruction into verifiable principles and scores an edited image against them in a single pass. (b) Reward benchmark performance. Our final 7B model, trained with SFT and GCPO (RL-RRM), reaches 82.22% accuracy, surpassing the Seed-VLM baseline. Each training component contributes to the performance gain. (c) Downstream application. Using our 7B RL-RRM as a reward signal significantly improves the performance of FLUX.Kontext [5] across multiple editing categories during post-training*

## 核心模块与公式推导

### 两阶段奖励模型训练管线

Edit-R1 的核心是构建一个基于验证器的推理奖励模型（RRM），其训练分为两个阶段：**冷启动监督微调（Cold-Start SFT）** 与 **群体对比偏好优化（GCPO）**。

**阶段一：冷启动 SFT。** 该阶段的目标是赋予 RRM 初始的链式思维（CoT）推理与逐项验证能力。具体流程为：
1. **原则分解**：利用 Seed-1.5-VL 将编辑指令分解为一组可独立验证的原则集合 $\mathcal{P}$，涵盖「应保持不变的元素」「需遵循修改的要求」「整体视觉质量」等维度。
2. **四元组数据生成**：为每个（参考图，指令）对，使用多个编辑模型生成多个编辑候选，形成大规模四元组数据（指令、源图、原则、编辑图）。
3. **CoT 推理与评分**：由 VLM 池对每个四元组生成多条思维链推理和评分轨迹。
4. **外部验证与数据筛选**：使用外部 VLM 作为「质量控制裁判」，逐条验证推理轨迹的正确性，选择准确率最高的 CoT 轨迹构建 SFT 数据。

**阶段二：GCPO 强化学习。** 在冷启动 SFT 之后，GCPO 利用人类标注的偏好对（约 10k 对，不足 SFT 数据的 1%）进一步将 RRM 与人类偏好对齐。GCPO 的核心机制是「组间奖励对比、组内优势计算」：对于每个偏好对，RRM 为偏好图像和非偏好图像各生成 $N$ 个候选评分，通过组间成对比较计算赢/输比率作为奖励信号，再在组内计算优势函数进行策略优化。

### 关键公式

**分数提取。** 奖励模型 $\mathbb{R}_\phi$ 接收编辑图像 $x$、指令 $c$ 和原则集 $\mathcal{P}$，生成文本形式的推理与评分，再通过解析函数 $\Phi$ 提取标量分数：

$$\tau_j^w = \Phi(\mathbb{R}_\phi(x_j^w, c, \mathcal{P}))$$

其中 $x_j^w$ 为偏好组中的第 $j$ 个图像，$\tau_j^w$ 为其对应分数。

**赢/输比率奖励。** 在 GCPO 中，偏好组候选的赢比率定义为该候选分数高于所有非偏好组候选的比例；非偏好组候选的输比率同理：

$$r_j^w = \frac{1}{N} \sum_{k=1}^{N} \mathbb{1}\{\tau_j^w > \tau_k^l\}, \quad r_j^l = \frac{1}{N} \sum_{k=1}^{N} \mathbb{1}\{\tau_j^l < \tau_k^w\}$$

其中 $N$ 为每组生成的候选数量，$\tau_k^l$ 为非偏好组候选分数。

**GCPO 损失（简化形式，省略 KL 散度项）。** GCPO 采用裁剪替代损失，对每个候选的每个推理 token 位置计算策略梯度：

$$\mathcal{L}_{\mathrm{GCPO}}(\phi) = \mathbb{E} \left[ \frac{1}{2N} \sum_{j=1}^N \frac{1}{T} \sum_{t=0}^{T-1} \left( \min(r_{t,j}^w A_j^w, \mathrm{clip}) + \min(r_{t,j}^l A_j^l, \mathrm{clip}) \right) \right]$$

其中 $T$ 为推理 token 长度，$A_j^w$ 和 $A_j^l$ 分别为偏好组和非偏好组内的优势函数，$\mathrm{clip}$ 为裁剪操作。

**编辑模型 GRPO 优势函数。** 在下游编辑模型优化中，RRM 作为非可微奖励信号，通过 GRPO 算法提供反馈。组内标准化优势定义为：

$$A_i = \frac{\tau_i - \mathrm{mean}(\{\tau_i\})}{\mathrm{std}(\{\tau_i\}) + \epsilon_{\mathrm{std}}}$$

其中 $\tau_i = \Phi(\mathbb{R}_\phi(x_0^i, c, \mathcal{P}))$ 为组内第 $i$ 个编辑结果的 RRM 评分，$\epsilon_{\mathrm{std}}$ 为防止除零的小常数。GRPO 训练目标为最大化期望优势，同时引入裁剪目标和 KL 散度惩罚项（$\beta=0.04$，组大小 $G=24$）以稳定策略更新。

### 模块间的因果链路

原则分解模块将模糊的编辑指令转化为可验证的检查清单，为 CoT 推理提供了结构化锚点；外部验证模块通过筛选高质量推理轨迹，确保 SFT 冷启动数据的可靠性；GCPO 模块则利用人类偏好对中的对比信号，使 RRM 的评分分布更精准地对齐人类判断。这三个模块形成递进依赖：原则分解质量决定 CoT 推理的上限，外部验证过滤低质轨迹保障 SFT 基础能力，GCPO 在此基础上注入人类对齐信号，最终使 7B RL-RRM 在内部基准上达到 82.2% 的准确率，显著超越 Seed-1.5-VL（79.3%）和编辑专用模型 EditScore（65.9%）。

### 补充图表

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/004_Figure_2.jpg]]
*Figure 2: The Training pipeline of Verifier-based Reasoning Reward Model (RRM). Top (Cold-Start SFT): Given an edit instruction and a source image, we generate large-scale quadruple data (instruction, source image, principles, edited image) and employ VLM pools to generate numerous reasoning traces and use another VLM to select the thinking COT with the highest accuracy to build SFT data and cold-start the Reasoning Reward Model (RRM). Bottom (GCPO): For each human-labeled preference pair, the reward model generates N thinking-score candidates per image. We compute a win/loss ratio reward by pairwise comparing every candidate in the preferred group against all candidates in the non-preferred group. T...*

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/010_Figure_5.jpg]]
*Figure 5: Illustration of the Verifier-based Reasoning Reward Model (RRM) inference process. (a) shows the input quadruple, which includes the source image, the edit instruction, and the decomposed principles for evaluation. (b) shows the final summary output from the RRM, containing the score for each principle and the final comprehensive score for the edited image*

## 实验与分析

### 奖励模型评估

**内部基准与公开基准的双重验证**。Edit-RRM在内部构建的奖励基准上达到82.2%的准确率（7B RL-RRM），显著超越闭源基线Seed-1.5-VL（79.3%）和编辑专用模型EditScore（65.9%）。在公开基准EditRewardBench上，两阶段训练策略展现出清晰的递进增益：冷启动SFT阶段将RRM准确率推至73.3%，已大幅领先EditScore-7B（65.9%）；GCPO强化学习阶段进一步将RL-RRM提升至78.2%（+4.9个百分点），验证了人类偏好对齐的关键作用。值得注意的是，GCPO仅使用了约1万对人工标注数据——不到SFT数据量的1%——却贡献了显著的性能跃升，说明增益主要来自人类对齐质量的提升，而非数据规模的简单堆砌（Table 4）。

**推理能力对比**。Table 1系统对比了现有奖励模型的能力维度。Edit-RRM是首个在图像编辑任务中同时集成“作为验证器（as verifier）”“链式思维推理（thinks）”和“强化学习（RL）”三项推理增强特性的生成式逐点评分模型。传统方法如Seed-VLM系列仅提供整体标量评分，缺乏可解释的验证机制；EditScore虽为编辑专用，但未引入原则分解与CoT推理。Edit-RRM的独特定位使其能够对编辑结果进行细粒度、可解释的评估，为下游编辑模型提供高质量训练信号。

### 下游编辑模型优化

**GEdit-Bench-EN全量评估**。Table 3展示了在GEdit-Bench-EN全量数据集上的详细性能对比。以FLUX.Kontext为基座，使用RL-RRM（7B）作为奖励信号进行GRPO优化后，Overall Score（O）从基线的5.77提升至6.24（+0.47），在文本编辑、颜色/材质变更、运动修改、主体操作等多个编辑类别上均取得一致提升。值得注意的是，使用SFT-RRM（7B）作为奖励信号时，训练奖励的稳定性与Seed-1.5-VL相当；而经GCPO强化后的RL-RRM则表现出更强的可扩展性和更严格的评估标准，在训练过程中产生持续更高的评估奖励（Figure 4），表明RL-RRM是更鲁棒的奖励提供者。

**人类评估**。Table 5报告了GSB（Good-Same-Bad）人类评估结果。FLUX.Kontext经Edit-R1优化后获得+23.2的GSB分数，表明人类评估者在绝大多数情况下偏好经过验证器强化学习优化的编辑结果。这一主观评估与自动指标（GPT-4.1评分的SC和PQ）高度一致，验证了奖励模型与人类感知的对齐质量。

**定性分析**。Figure 6展示了FLUX.Kontext在多样化编辑指令下的定性对比。Edit-R1优化后的模型在文本编辑、颜色/材质变更、运动修改和主体操作（添加与移除）等类别上均表现出更强的指令遵循能力，同时保持高感知质量。Figure 9进一步展示了在Qwen-Edit上的定性改进，尤其在运动相关编辑和细粒度属性修改方面效果显著，表明Edit-R1框架对不同编辑架构具有良好的适配性。

### 消融实验

**SFT阶段的模块贡献**。Table 2系统消融了SFT阶段的关键组件。完整的“Think+Verify”（T+V）配置在GCPO之前始终取得最高准确率。单独移除“Think”（仅保留Verify）或“Verify”（仅保留Think）均导致显著性能下降，证明原则分解后的逐项推理（Think）与外部验证筛选（Verify）是两个互补的关键环节。

**GCPO阶段的数据效率**。GCPO在仅使用约1万对人工偏好数据（不到SFT数据的1%）的情况下，将RRM准确率稳定提升约4.9个百分点。这一结果表明，GCPO的增益机制在于通过组间对比偏好优化实现更好的人类对齐，而非依赖大规模数据扩展。

**模型规模的可扩展性**。从3B到7B的参数扩展实验显示，SFT和GCPO阶段的准确率均持续提高，展现出清晰的缩放趋势（Figure 3b、3d）。7B模型在内部基准上达到82.2%的最高准确率，表明更大规模的验证器有望带来进一步的性能提升。

**编辑优化中的奖励模型选择**。Figure 4对比了SFT-RRM与RL-RRM作为奖励信号时的训练动态。使用GCPO训练后的RL-RRM在编辑模型优化过程中产生持续更高的评估奖励，且训练过程更稳定。这表明经强化学习对齐的RRM是更严格、更鲁棒的评估器，能够为下游编辑任务提供更可靠的监督信号。

### 失败模式与局限性

**幻觉修复案例**。Figure 10展示了一个典型的RL纠正SFT幻觉的案例：指令要求将衬衫改为红色同时保留其他特征，SFT模型的“失败”输出错误地将帽子颜色也改为红色。RRM通过逐项原则验证准确识别了这一属性泄露问题并给予惩罚，RL优化后的模型则正确保留了蓝色帽子。这表明基于验证器的奖励机制能够有效识别并纠正SFT阶段遗留的细粒度编辑失败。

**已知局限**。（1）RRM的CoT推理过程需要离散文本生成，导致奖励信号不可微，无法直接用于基于梯度的策略优化，当前仅能通过GRPO等非梯度方法间接利用。（2）GCPO依赖人工标注偏好对（约10k），数据采集成本较高；虽性能提升显著，但更低数据量下的极限性能尚不明确。（3）当前实验仅在FLUX.Kontext和Qwen-Edit两款编辑模型上验证了有效性，在其他架构（如GAN-based编辑器或视频编辑任务）上的泛化性有待进一步探索。（4）奖励模型对原则分解的初始质量敏感——若Seed-VLM生成的原则集合不准确，可能影响后续评分的可靠性。

### 补充图表

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/002_Table_1.jpg]]
*Table 1: Comparison of reward models, highlighting reasoning capabilities. We categorize methods by their foundational characteristics (Task, Modeling Paradigm, etc.) and their support for advanced Reasoning Ability components: explicit use of principles(“as verifier”), Chain-of-Thought (“thinks”), and reinforcement learning. A checkmark (✓) denotes support. Edit-RRM (Ours) is unique in integrating all three reasoning-enhancing features within a generative, point-wise framework for visual tasks*

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/005_Figure_3.jpg]]
*Figure 3: Training dynamics of RRMs. a, SFT Loss, showing model convergence and scalability. b, SFT evaluation accuracy for the RRMs, showing steady improvement. c, Weighted advantage during GCPO training. The weighted advantage is defined as*

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/006_Figure_4.jpg]]
*Figure 4: Training dynamics of editing model optimization with different RRMs. The first row shows the training reward, and the second row shows the evaluation reward. Here, SFT-RRM denotes a reward model trained without GCPO, while RL-RRM denotes its counterpart trained with GCPO. First column: our SFT-RRM (7B) produces a reward signal that is as stable and effective as the Seed-1.5-VL. Second column: the SFT-RRM 7B exhibits stronger scalability, providing more reliable supervision and yielding better performance than the SFT-RRM 3B. Third and fourth columns: refining the RRM with GCPO results in consistently higher evaluation rewards, indicating that the RRM trained with GCPO acts as a stricter and...*

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/007_Table_2.jpg]]
*Table 2: Accuracy on our internal benchmark. T, V, and T+V denote Think, Verify, and Think+Verify, respectively*

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/008_Table_3.jpg]]
*Table 3: Detailed performance comparison on the GEdit-Bench-EN (Full set). Higher scores are better. Bold scores highlight the best result within each model family. Columns 1–11 report SC scores for different editing categories (see Appendix for details)*

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/009_Table_4.jpg]]
*Table 4: Comparison of our RRM against the baseline on the EditReward benchmark. All results are for 7B models*

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/011_Table_5.jpg]]
*Table 5: Human evaluation using the GSB protocol. Higher is better*

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/012_Figure.jpg]]
*Figure: [Text Change] Remove the text 'FREE'. [Material Alter] Turn the puppy into clay*

![[assets/figures/papers/paper_list_l2690_https_arxiv_org_abs_2604_27505/figures/016_Figure.jpg]]
*Figure: Source Winner Loser*

## 方法谱系与知识库定位

### 1. 与奖励模型基线的对比定位

Edit-R1 的核心贡献在于将图像编辑的奖励模型从**整体打分器（holistic scorer）**范式转变为**基于验证器的推理模型（verifier-based RRM）**。这一转变在 Table 1 中通过与现有方法的系统对比得到清晰定位：

- **整体打分器**：如 **Seed-1.5-VL**（闭源通用VLM）和 **EditScore**（编辑专用评分模型，7B）直接对编辑结果输出单一标量分数，缺乏对指令各维度的细粒度检查。在公开基准 EditRewardBench 上，EditScore 仅达 65.9% 准确率（Table 4），而本文仅经 SFT 的 SFT-RRM 即达 73.3%，经 GCPO 强化后的 RL-RRM 进一步提升至 78.2%，领先 EditScore 达 +12.3 个百分点。

- **通用 VLM 评分器**：Seed-1.5-VL 和其升级版 **Seed-1.6-VL** 虽具备一定视觉推理能力，但并非为编辑任务专门设计，缺乏结构化的原则分解和链式思维（CoT）验证机制。在内部基准上，本文 7B RL-RRM 以 82.2% 准确率超越 Seed-1.5-VL 的 79.3%（+2.9 个百分点），验证了专用推理验证器优于通用 VLM 直接评分。

- **Table 1 的系统定位**：该表从任务类型、建模范式、是否显式使用原则（“as verifier”）、是否具备 CoT（“thinks”）、是否使用强化学习等维度，将 Edit-RRM 与现有奖励模型进行全面对比。Edit-RRM 是唯一一个在视觉编辑任务中同时集成**原则分解验证、链式思维推理和强化学习对齐**三项核心能力的生成式点式（pointwise）模型，填补了可解释、细粒度编辑奖励模型的空白。

### 2. 与下游编辑模型优化的关系

Edit-R1 框架的第二阶段将训练好的 RRM 作为奖励信号，通过 **GRPO（Group Relative Policy Optimization）**算法优化下游编辑模型。这一设计解决了两个关键瓶颈：

- **不可微奖励的利用**：RRM 的 CoT 推理输出为离散文本，奖励信号不可微，无法直接用于基于梯度的策略优化。本文采用 GRPO 的组内相对优势机制（公式 $A_i = \frac{\tau_i - \mathrm{mean}(\{\tau_i\})}{\mathrm{std}(\{\tau_i\}) + \epsilon_{\mathrm{std}}}$），仅需奖励的标量值即可进行策略更新，绕开了可微性限制。

- **与现有编辑模型的兼容性**：实验在两款架构迥异的编辑模型上验证了 Edit-R1 的通用性——基于 flow matching 的 **FLUX.Kontext** 和基于 VLM 的 **Qwen-Edit**。在 GEdit-Bench-EN 全量数据集上，FLUX.Kontext 经 RL-RRM（7B）优化后总体评分从 5.77 提升至 6.24（Table 3）；人类评估 GSB 分数达 +23.2（Table 5），表明优化后的模型在指令遵循和视觉质量上均获显著偏好。

### 3. 训练策略的消融与可扩展性

两阶段训练策略的贡献通过消融实验得到严格验证（Table 2）：

- **SFT 阶段**：同时使用 Think（CoT 推理生成）和 Verify（外部验证筛选）的 T+V 配置在所有规模下均取得最高准确率，去除任一模块均导致性能显著下降，证明高质量推理数据筛选对冷启动至关重要。

- **GCPO 阶段**：仅使用约 1 万人类标注偏好对（不足 SFT 数据的 1%），GCPO 将 RRM 准确率稳定提升约 4.9 个百分点。这一增益来自人类对齐质量而非数据量，体现了强化学习在偏好对齐中的关键作用。

- **模型规模可扩展性**：从 3B 到 7B，SFT 和 GCPO 阶段的准确率均持续提升，展现出良好的缩放趋势（Figure 3b, 3d）。在编辑模型优化中，7B RL-RRM 比 3B 版本提供更稳定、更严格的评估信号（Figure 4），表明更大规模的验证器能更有效地指导下游编辑模型。

### 4. 适用边界与局限

尽管 Edit-R1 在奖励建模和编辑优化上取得了显著进展，其适用边界和局限值得明确：

- **奖励信号不可微**：RRM 的 CoT 推理依赖离散文本生成，奖励信号天然不可微，限制了其与需要梯度回传的优化方法（如可微分 REFL）的直接结合。当前 GRPO 方案虽有效，但可能不如端到端可微方法高效。

- **人类偏好数据依赖**：GCPO 依赖约 10k 人类标注偏好对，采集成本较高。虽已证明小量高质量数据即可带来显著增益，但未充分探索在更低数据量（如 1k 或 5k）下的性能极限，也未验证完全依赖自动生成偏好数据的可行性。

- **编辑模型泛化性**：当前实验仅在 FLUX.Kontext 和 Qwen-Edit 两款编辑模型上验证，未涉及 GAN-based 编辑器、视频编辑模型或其他生成范式，Edit-R1 在更广泛架构上的有效性尚需进一步验证。

- **原则分解质量敏感性**：RRM 的评分可靠性依赖于初始原则分解的质量。若 Seed-1.5-VL 生成的原则集合不准确或不完整，可能导致评分偏差。论文未量化分析原则分解错误对最终评估的影响。

### 5. 开放问题

Edit-R1 开辟了基于验证器的推理奖励模型新范式，以下开放问题值得后续探索：

- **跨任务泛化**：能否将原则分解 + CoT 验证的奖励建模思想拓展到文本到图像生成、视频编辑、3D 内容生成等多模态任务，构建通用的多模态推理奖励模型？

- **数据效率极限**：在更少的人类偏好数据（如 1k 对）或仅用自动生成的高质量偏好数据下，GCPO 能否保持相似的训练效率和提升幅度？是否可结合主动学习或在线偏好采集进一步降低标注成本？

- **推理效率与准确率的权衡**：RRM 的 CoT 推理长度与评估准确率之间存在何种量化关系？是否存在更高效的推理格式（如结构化 JSON 输出）或推理压缩策略，在保持可解释性的同时降低推理成本？

- **从验证到生成的可解释性传递**：RRM 内部已具备对编辑结果逐原则验证的能力，如何将这种结构化验证信号反馈到编辑模型的生成过程中，使编辑模型本身具备可解释、可控的编辑能力，是提升系统整体透明度的关键方向。

## 原文 PDF

![[paperPDFs/CVPR_2026/Leveraging_Verifier_Based_Reinforcement_Learning_in_Image_Editing.pdf]]
