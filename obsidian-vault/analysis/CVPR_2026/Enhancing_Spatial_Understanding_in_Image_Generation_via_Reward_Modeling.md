---
title: Enhancing Spatial Understanding in Image Generation via Reward Modeling
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Enhancing_Spatial_Understanding_in_Image_Generation_via_Reward_Modeling.pdf
project_link: null
code_link: null
aliases:
- STKG
- ESUIGRM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 构建专门针对空间关系的对抗性偏好数据集并训练空间感知奖励模型（SpatialScore），进而利用该奖励模型为GRPO在线强化学习提供准确的空间准确性反馈，直接引导生成模型优化空间布局。
primary_logic: 通过对抗性构造的海量偏好对训练出的VLM奖励模型，能够比通用VLM和专有模型更精准地判断空间正误；将该奖励模型集成到GRPO框架中，并辅以top-k过滤缓解优势偏差，可显著提升扩散模型对复杂空间提示的遵循能力。
claims:
- SpatialScore在空间评估基准上的总体成对准确率达到0.958，超过GPT-5 (0.890) 和 Gemini-2.5 Pro (0.951)。
- 以SpatialScore为奖励的在线RL将Flux.1-dev的SpatialScore从2.18提升至7.81，并在DPG-Bench空间关系子维度上从0.871提升至0.932。
- 在DPG-Bench全维度评估中，我们的方法超越原始Flux.1-dev，整体得分接近GPT-Image-1，而GenEval训练的Flow-GRPO出现退化。
- Qwen-Image基线上应用SpatialScore RL后，SpatialScore从6.74提升到8.25，所有空间基准一致改善。
---

# Enhancing Spatial Understanding in Image Generation via Reward Modeling

> [!tip] 核心洞察
> 通过对抗性构造的海量偏好对训练出的VLM奖励模型，能够比通用VLM和专有模型更精准地判断空间正误；将该奖励模型集成到GRPO框架中，并辅以top-k过滤缓解优势偏差，可显著提升扩散模型对复杂空间提示的遵循能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | 通过奖励建模增强图像生成的空间理解 |
| 英文题名 | Enhancing Spatial Understanding in Image Generation via Reward Modeling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.24233) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SPATIALSCORE with Top-k GRPO |
| Dataset | Reward Evaluation Benchmark, SpatialScore, DPG-Bench - Relation-Spatial, DPG-Bench 全维度 |

> [!tip] 效果简介
> - Reward Evaluation Benchmark (365偏好对) 上，总体成对准确率 0.958 (SpatialScore 7B) vs 0.951 (Gemini-2.5 Pro) (+0.007)。
> - SpatialScore (in-domain) 上，奖励分数 7.81 vs 2.18 (Flux.1-dev) / 3.01 (Flow-GRPO*) (+5.63 (over Flux.1-dev))。
> - DPG-Bench - Relation-Spatial 上，准确率 0.932 vs 0.871 (Flux.1-dev) (+0.061)。

## 概要

### 问题瓶颈
文本到图像生成模型在处理多对象间的复杂空间关系时仍存在显著不足。现有奖励模型——无论是基于人类偏好的通用图像奖励模型（如**ImageReward**、**PickScore**、**HPSv3**），还是基于VQA风格的评估器（如**UnifiedReward**），均无法可靠地判断生成图像中空间布局的正确性，常常给空间错误的图像分配更高的奖励分数（Figure 1）。同时，基于规则检测的**GenEval**奖励在遮挡等视觉挑战下评估失准，且无法泛化到包含多对象复杂空间关系的长提示场景（Figure 2）。这导致在线强化学习缺乏准确的空间反馈信号，制约了生成模型空间理解能力的提升。

### 核心方法与因果机制
本文提出**SpatialScore**——一个专门评估文本到图像生成中空间关系准确性的奖励模型，并将其集成到在线强化学习框架中，直接引导生成模型优化空间布局。方法的核心链条为：

1. **对抗性偏好数据构造**：利用大语言模型生成并扰动复杂空间提示，通过多个先进生成模型产生图像对，经人工验证形成**SpatialReward-Dataset**（80k偏好对）。
2. **空间感知奖励模型训练**：以**Qwen2.5-VL-7B**为骨干，附加线性奖励头，通过Bradley-Terry偏好损失微调，使模型能精准判断空间正误。
3. **在线RL优化**：将SpatialScore作为奖励源，采用**GRPO**算法对基础生成模型（如**Flux.1-dev**）进行在线策略优化，并引入**top-k过滤**策略缓解不同难度提示导致的优势估计偏差。

### 主要结果
- **奖励评估准确率**：SpatialScore（7B）在空间评估基准上总体成对准确率达**0.958**，超越**GPT-5**（0.890）和**Gemini-2.5 Pro**（0.951）（Table 1）。
- **空间生成能力提升**：以SpatialScore为奖励的在线RL将Flux.1-dev的SpatialScore从**2.18**提升至**7.81**，在DPG-Bench空间关系子维度上从**0.871**提升至**0.932**（Table 2）。
- **全维度泛化**：在DPG-Bench全维度评估中，该方法超越原始Flux.1-dev，整体得分接近**GPT-Image-1**；而使用GenEval训练的Flow-GRPO则出现退化（Table 3）。
- **跨模型泛化**：在**Qwen-Image**基线上应用SpatialScore RL后，SpatialScore从**6.74**提升至**8.25**，所有空间基准一致改善（Table 7）。

### 方法定位
SpatialScore填补了现有奖励模型在空间评估上的空白，将VLM的视觉推理能力转化为可微的奖励信号。其与GRPO在线RL的结合，为提升扩散模型对复杂空间提示的遵循能力提供了一条有效路径。该方法属于“奖励建模引导的生成模型对齐”范式，区别于基于规则的评估和通用偏好模型，专注于空间关系的细粒度反馈。



文本到图像（T2I）生成模型近年来取得了显著进展，但在准确遵循涉及多对象复杂空间关系的提示方面仍面临根本性挑战。用户提示中常包含诸如“A在B的左侧”、“C在D的上方”等空间约束，而现有模型生成的图像往往无法精确满足这些要求，这严重制约了生成内容在广告设计、产品展示等实际场景中的可用性。

### 现有奖励模型的空间评估缺陷

强化学习（RL）微调已被证明是提升生成模型指令遵循能力的有效途径，但其成功高度依赖奖励信号的质量。当前主流的奖励模型在空间理解方面存在严重不足。如图1所示，现有奖励模型——包括基于人类偏好的通用图像奖励模型（如**ImageReward**、**PickScore**、**HPSv3**）和基于VLM的奖励模型（如**UnifiedReward**）——经常对空间关系错误的图像赋予比正确图像更高的奖励分数。这一现象揭示了它们缺乏可靠的空间推理能力，无法为在线RL训练提供准确的反馈信号。

### 基于规则奖励的局限性

**GenEval**作为一种基于规则的空间评估方法，通过目标检测器验证对象间的空间关系，曾被用于Flow-GRPO等在线RL框架。然而，该方法存在两个关键缺陷：

1. **泛化性不足**：如图2(a)所示，使用GenEval奖励训练的模型无法泛化到包含多对象复杂空间关系的长提示，训练过程中奖励信号的提升并未转化为实际生成质量的改善。
2. **视觉感知脆弱**：如图2(b)所示，基于目标检测器的规则奖励在遮挡等视觉挑战下容易产生错误评估——当对象被部分遮挡时，检测器可能完全失效，而现代VLM能够准确推断正确的空间响应。这使得GenEval奖励在真实场景中的可靠性大打折扣。

### 核心瓶颈与本文动机

上述分析揭示了当前T2I生成领域的核心瓶颈：**缺乏专门针对空间关系评估的高质量奖励模型**。通用人类偏好奖励模型无法捕捉细粒度的空间准确性，而基于规则的GenEval奖励则因依赖检测器而缺乏鲁棒性和泛化能力。这一缺口导致在线RL训练缺乏可靠的空间反馈信号，使生成模型难以通过优化过程习得精确的空间布局能力。

为此，本文提出构建专门针对空间关系的对抗性偏好数据集，并训练空间感知的VLM奖励模型**SpatialScore**，进而将其集成到GRPO在线强化学习框架中，为扩散模型提供精准的空间准确性反馈，直接引导其优化空间布局。



## 核心方法与创新机理

本工作的核心创新在于构建了一个**专门针对空间关系的奖励模型（SpatialScore）**，并将其集成到**在线强化学习框架（GRPO）**中，从而系统性地解决了文本到图像生成中长期存在的空间理解难题。相比于现有方案，该方法在三个关键环节上实现了突破性改进。

### 1. 从通用奖励到空间专用奖励：SpatialScore

现有奖励模型（如 ImageReward、PickScore、HPSv3、UnifiedReward）主要针对整体图像质量或人类偏好进行训练，**缺乏对复杂多对象空间关系的细粒度判断能力**。如图 Figure 1 所示，这些模型常常给空间关系错误的图像打出比正确图像更高的分数，暴露出其空间推理的根本缺陷。即便是基于规则的 GenEval 奖励，也因依赖对象检测器而在遮挡等视觉挑战下产生错误评估，且无法泛化到包含多个空间关系约束的长提示（Figure 2）。

SpatialScore 的核心变革在于**将奖励模型从通用偏好评估器重构为空间准确性专家**。它以 Qwen2.5-VL-7B 作为视觉-语言骨干 $H_\phi$，将其原始语言建模头替换为一个线性奖励头 $R_\phi$，输出一个标量奖励分数：

$$s = R_{\phi}( H_{\phi}(c, y) )$$

其中 $c$ 为文本指令，$y$ 为生成图像。该奖励模型通过 Bradley-Terry 偏好损失在专门构建的 **SPATIALREWARD-DATASET**（80k 对抗性偏好对）上进行微调：

$$\mathcal{L}_{\mathrm{Reward}}(\theta) = \mathbb{E}_{c, y_w, y_l}\big[ -\log P(y_w \succ y_l \mid c) \big]$$

$$P(y_w \succ y_l \mid c) = \sigma\big( R_{\phi}(H_{\phi}(y_w, c)) - R_{\phi}(H_{\phi}(y_l, c)) \big)$$

这一设计使得 SpatialScore 能够精准捕捉“A 在 B 的左边”、“C 在 D 的上方且被部分遮挡”等细微空间差异。实验表明，SpatialScore 在空间评估基准上的总体成对准确率达到 **0.958**，超越了 GPT-5（0.890）和 Gemini-2.5 Pro（0.951）等专有大规模 VLM（Table 1）。

### 2. 从规则式奖励到 VLM 驱动的在线 RL 反馈

在生成模型优化层面，现有工作（如 Flow-GRPO）使用基于规则的 GenEval 奖励进行在线强化学习，但该方法存在两个致命缺陷：**（a）无法泛化到长提示中的复杂空间关系**（Figure 2a）；**（b）在遮挡等视觉挑战下产生错误评估**（Figure 2b）。这导致 Flow-GRPO 训练后的模型在 DPG-Bench 全维度上出现严重退化（从 82.91 降至 57.02，Table 3）。

本工作将 SpatialScore 作为 GRPO 的奖励信号源，为生成模型提供**细粒度、语义级别的空间准确性反馈**。训练管线（Figure 4）首先从策略模型采样一组图像，用 SpatialScore 对其空间准确性进行评分排序，然后选取 top-k 最准确和 bottom-k 最不准确的样本，将分数转换为优势信号：

$$A^{i} = \frac{ R(x_{i}^{0}, c) - \mathrm{mean}\big(\{R(x_{0}^{i}, c)\}_{i=1}^{G}\big) }{ \mathrm{std}\big(\{R(x_{0}^{i}, c)\}_{i=1}^{G}\big) }$$

策略模型通过策略梯度优化直接奖励正确的空间布局并惩罚错误，从而增强基座模型的空间理解能力。为支持 RL 探索，模型将流匹配的确定性 ODE 转化为 SDE，采用 Euler-Maruyama 离散化：

$$x_{t+\Delta t} = x_t + \left[ v_{\theta}(x_t, t) + \frac{\sigma_t^2}{2t}\big( x_t + (1-t) v_{\theta}(x_t, t) \big) \right]\Delta t + \sigma_t \sqrt{\Delta t}\,\epsilon$$

### 3. Top-k 过滤：缓解 GRPO 中的优势估计偏差

标准 GRPO 在组内对所有样本进行标准化计算优势时，存在一个被忽视的**优势偏差问题**：对于简单提示，组内大部分样本都能获得高奖励，导致一些高质量样本因高于组内均值而获得负优势（Figure 5）。这会误导策略更新，削弱对简单提示的优化效果。

本工作提出 **top-k 过滤策略**：仅选取组内奖励最高和最低的 $2k$ 个样本构建平衡子集 $S$，在该子集上计算优势并优化 GRPO 目标：

$$\mathcal{L}_{\mathrm{GRPO}}(\boldsymbol{\theta}) = \frac{1}{|\boldsymbol{S}|}\sum_{i\in S}\frac{1}{T}\sum_{t=0}^{T-1} \operatorname*{min}\big( r_{t}^{i}(\boldsymbol{\theta}) A_{t}^{i},\, \dots \big)$$

该策略不仅缓解了优势偏差，还**显著降低了训练的计算开销**——将每次策略更新的 NFE（函数评估次数）从 144 降至 72（Table 4）。消融实验确认 $k=6$ 在 DPG-Bench、UnigenBench++ 等多个基准上取得最优表现（Table 4, Figure 7）。

### 创新总结

上述三个 changed slots——**空间专用奖励模型、VLM 驱动的在线 RL 反馈、top-k 优势过滤**——构成了一个完整的闭环：对抗性构造的空间偏好数据训练出高精度空间评估器，该评估器为 GRPO 提供可靠的奖励信号，top-k 过滤则确保训练过程稳定高效。这一组合使得 Flux.1-dev 的 SpatialScore 从 2.18 跃升至 7.81，DPG-Bench 空间关系子维度从 0.871 提升至 0.932（Table 2），并在 Qwen-Image 基线上验证了方法的跨模型泛化能力（SpatialScore 从 6.74 提升至 8.25，Table 7）。



本文提出的方法围绕一个核心闭环：**构造空间偏好数据 → 训练空间感知奖励模型 → 以该奖励模型驱动在线强化学习优化生成模型**。整个管线包含三个紧密耦合的模块，形成从数据到评估再到策略优化的完整反馈回路。

### 模块一：SPATIALREWARD-DATASET 构造

该模块负责生成大规模、高质量的空间关系偏好数据，为后续奖励模型训练提供监督信号。其流程可概括为：

1. **提示生成与扰动**：利用大语言模型生成涵盖多对象复杂空间关系的文本提示，并通过规则化扰动（如交换对象位置、替换空间介词）构造“正确-错误”提示对。
2. **图像生成**：使用多个先进文本到图像生成模型，分别为正确提示和扰动提示生成对应图像，形成候选图像对。
3. **人工验证**：对生成的偏好对进行人工校验，确保“胜者”图像确实在空间关系上优于“败者”图像，最终形成超过 80k 的高质量偏好对数据集（见 Figure 3）。

这一对抗性构造策略是关键——它刻意制造空间关系上的正误对比，迫使奖励模型学习细粒度的空间判别能力，而非依赖表面图像质量。

### 模块二：SpatialScore 奖励模型训练

以 Qwen2.5-VL-7B 作为视觉-语言骨干网络 $H_{\phi}$，替换其原有的语言建模头为一个线性奖励头 $R_{\phi}$。给定指令 $c$ 和生成图像 $y$，奖励分数通过下式计算：

$$s = R_{\phi}( H_{\phi}(c, y) )$$

对于偏好对中的胜者图像 $y_w$ 和败者图像 $y_l$，偏好概率由分数差经 sigmoid 函数给出：

$$P(y_w \succ y_l \mid c) = \sigma\big( R_{\phi}(H_{\phi}(y_w, c)) - R_{\phi}(H_{\phi}(y_l, c)) \big)$$

训练采用 Bradley-Terry 偏好损失：

$$\mathcal{L}_{\mathrm{Reward}}(\theta) = \mathbb{E}_{c, y_w, y_l}\big[ -\log P(y_w \succ y_l \mid c) \big]$$

该模块的输出是一个专门评估空间关系准确性的奖励模型，其在空间评估基准上的成对准确率达到 0.958，超越了 GPT-5 (0.890) 和 Gemini-2.5 Pro (0.951)（Table 1）。

### 模块三：在线 RL 训练（GRPO + top-k 过滤）

将训练好的 SpatialScore 作为奖励信号源，对基础生成模型（Flux.1-dev）进行在线强化学习优化。该模块的核心设计包括：

1. **SDE 采样探索**：将流匹配的确定性 ODE 转化为随机微分方程（SDE），引入随机性以支持 RL 探索。离散化采用 Euler-Maruyama 格式（Eq. 4）。
2. **GRPO 策略优化**：从当前策略模型采样一组图像，用 SpatialScore 评分后进行组内优势归一化（Eq. 5），再通过策略梯度更新模型参数（Eq. 6）。
3. **top-k 过滤**：仅选取奖励最高和最低的各 $k$ 个样本参与优势计算和策略更新，缓解不同难度提示导致的优势偏差（Figure 5），同时将每次更新的 NFE 从 144 降至 72。

整个管线的信息流如 Figure 4 所示：**策略模型采样 → SpatialScore 评分 → top-k 筛选 → 优势估计 → 策略梯度更新**，形成闭环迭代，直接引导生成模型优化空间布局的准确性。

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/004_Figure_4.jpg]]
*Figure 4: GRPO training pipeline for enhancing spatial unserstanding. We first samples a group of images from the policy model and uses our specialized SpatialScore to rate their spatial accuracy. After ranking based on these scores, we select the top-k most accurate and bottom-k least accurate examples and convert these scores into advantage signals. The policy model is updated via policy gradient optimization to directly reward correct spatial layouts and penalize errors, thereby enhancing the base model’s spatial understanding*

### 输入输出流总结

- **数据流**：LLM 生成的提示对 → 生成模型产出的图像对 → 人工验证 → 偏好数据集（模块一输入）
- **训练流**：偏好数据集 → SpatialScore 奖励模型（模块二输出，模块三输入）
- **优化流**：SpatialScore 奖励信号 → GRPO 优势估计 → 生成模型参数更新（模块三闭环）

这一框架的核心优势在于：奖励模型专门针对空间关系进行训练，能够提供比通用 VLM 和规则式奖励（如 GenEval）更精准的空间反馈；而 top-k 过滤策略则有效缓解了在线 RL 中因提示难度差异导致的优势估计偏差，使训练更加稳定高效。



### 空间感知奖励模型（SpatialScore）

SpatialScore 的核心架构以 **Qwen2.5-VL-7B**（Bai et al., 2025）作为视觉-语言骨干网络 $H_{\phi}$，用于提取给定指令 $c$ 与生成图像 $y$ 的联合特征。原始的语言建模头被替换为一个全新的线性奖励头 $R_{\phi}$，将特征投影为标量奖励分数：

$$s = R_{\phi}( H_{\phi}(c, y) ) \tag{1}$$

该设计使模型能够输出服从高斯分布的连续奖励值，专门用于评估生成图像中多对象空间关系的准确性。

### 偏好建模与训练损失

给定指令 $c$，对于赢家图像 $y_w$ 与输家图像 $y_l$ 的偏好对，SpatialScore 通过 sigmoid 函数将两者分数差转化为偏好概率：

$$P(y_w \succ y_l \mid c) = \sigma\big( R_{\phi}(H_{\phi}(y_w, c)) - R_{\phi}(H_{\phi}(y_l, c)) \big) \tag{2}$$

模型训练采用 Bradley-Terry 偏好损失，最小化负对数似然：

$$\mathcal{L}_{\mathrm{Reward}}(\theta) = \mathbb{E}_{c, y_w, y_l}\big[ -\log P(y_w \succ y_l \mid c) \big] \tag{3}$$

该损失驱动奖励模型为空间关系正确的图像分配更高分数，为空间关系错误的图像分配更低分数。

### 在线强化学习的随机探索机制

在 GRPO 在线强化学习阶段，为引入足够的探索随机性，将流匹配（Flow Matching）的确定性 ODE 转化为随机微分方程（SDE），采用 Euler-Maruyama 离散化：

$$x_{t+\Delta t} = x_t + \left[ v_{\theta}(x_t, t) + \frac{\sigma_t^2}{2t}\big( x_t + (1-t) v_{\theta}(x_t, t) \big) \right]\Delta t + \sigma_t \sqrt{\Delta t}\,\epsilon \tag{4}$$

其中 $v_{\theta}$ 为速度场预测网络，$\sigma_t$ 控制噪声强度，$\epsilon \sim \mathcal{N}(0, I)$ 为标准高斯噪声。SDE 采样使策略模型在去噪过程中产生多样化候选图像，为后续奖励评估与策略优化提供探索空间。

### 优势估计与 Top-k 过滤

标准 GRPO 对组内所有样本进行奖励标准化计算优势：

$$A^{i} = \frac{ R(x_{i}^{0}, c) - \mathrm{mean}\big(\{R(x_{0}^{i}, c)\}_{i=1}^{G}\big) }{ \mathrm{std}\big(\{R(x_{0}^{i}, c)\}_{i=1}^{G}\big) } \tag{5}$$

然而，对于简单提示（多数样本均获高奖励），组均值偏高会导致部分高质量样本获得负优势，产生**优势估计偏差**（Figure 5）。为解决此问题，本文引入 **top-k 过滤策略**：仅选取组内 SpatialScore 奖励最高和最低的各 $k$ 个样本构成子集 $\boldsymbol{S}$，在该子集上执行优势归一化与策略更新。GRPO 目标函数修正为：

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/005_Figure_5.jpg]]
*Figure 5: Advantage bias. For easy prompts with many highreward samples, some high-quality samples often obtain negative advantages due to the high group mean*

$$\mathcal{L}_{\mathrm{GRPO}}(\boldsymbol{\theta}) = \frac{1}{|\boldsymbol{S}|}\sum_{i\in S}\frac{1}{T}\sum_{t=0}^{T-1} \operatorname*{min}\big( r_{t}^{i}(\boldsymbol{\theta}) A_{t}^{i},\, \dots \big) \tag{6}$$

其中 $r_{t}^{i}(\boldsymbol{\theta})$ 为重要性采样比率，$\dots$ 表示裁剪项（与标准 PPO 一致）。默认配置采用 $k=6$，在保证样本多样性的同时将每步训练的函数评估次数（NFE）从 144 降至 72（Table 4）。

### 补充图表

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/001_Figure_1.jpg]]
*Figure 1: Failure of Reward Models on Spatial Understanding. Existing reward models [17, 23, 29, 53] often assign higher reward values to spatially incorrect images than to spatially correct ones, thereby exposing their limited spatial reasoning capabilities*

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/002_Figure_2.jpg]]
*Figure 2: Limitations of GenEval [9] as the reward model. (a) GenEval-based RL training fails to generalize to long prompts involving complex spatial relationships across multiple objects. (b) The rule-based GenEval rewards, which rely on object detectors, often produce incorrect evaluations under visual challenges like occlusion, while modern VLMs can accurately infer the correct response*



## 实验与关键发现

### 核心瓶颈与实验动机

现有奖励模型（包括人类偏好奖励模型如 **ImageReward**、**PickScore**、**HPSv3** 和 VQA 风格模型如 **UnifiedReward**）无法准确评估文本到图像生成中复杂的多对象空间关系。Figure 1 展示了这一失效模式：这些模型经常为空间关系错误的图像分配比正确图像更高的奖励值。同时，基于规则的 **GenEval** 奖励在遮挡等视觉挑战下产生错误评估，且在长提示场景下无法泛化（Figure 2）。这导致在线强化学习缺乏可靠的奖励信号，直接限制了生成模型的空间理解能力提升。

### 实验设置概要

实验分为两个核心阶段：**奖励模型评估**与**在线 RL 训练**。奖励模型以 **Qwen2.5-VL-7B** 为骨干网络，附加线性奖励头，在 **SPATIALREWARD-DATASET**（80k 对抗性偏好对）上通过 Bradley-Terry 偏好损失微调。在线 RL 阶段采用 **GRPO** 算法，以 **SpatialScore** 为奖励源对 **Flux.1-dev** 进行优化，并引入 **top-k 过滤策略**（默认 k=6）缓解优势估计偏差。训练采用 SDE 采样引入随机性以支持策略探索。

### 奖励模型评估结果

Table 1 展示了 SpatialScore 与多个基线在奖励评估基准（365 偏好对）上的成对准确率对比。

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/006_Table_1.jpg]]
*Table 1: Pairwise-accuracy comparisons on the reward evaluation benchmark. “1 Pert.” and “2–3 Pert.” denote subsets with one or two–three spatial perturbations applied to the perfect prompts when constructing the perturbed prompts*

**核心发现：SpatialScore 7B 以 0.958 的总体成对准确率超越所有对比模型**，包括专有 VLM **GPT-5**（0.890）和 **Gemini-2.5 Pro**（0.951）。在仅含单一空间扰动的子集上，SpatialScore 达到 0.957；在含 2-3 个扰动的更困难子集上，准确率进一步提升至 0.958，表明模型对复杂空间错误具有稳健的判别能力。

相比之下，现有图像奖励模型 **ImageReward**（0.589）、**HPSv3**（0.562）和 **PickScore**（0.575）的准确率仅略高于随机猜测，验证了通用奖励模型在空间评估上的根本性缺陷。开源 VLM **Qwen2.5-VL-72B** 的零样本准确率为 0.875，低于经过专门微调的 SpatialScore 7B，凸显了构建专门空间偏好数据集和微调策略的必要性。

Table 6 的骨干网络规模消融显示，SpatialScore 的准确率随骨干规模单调提升：3B 版本为 0.891，7B 版本为 0.958，32B 版本达到 0.973。值得注意的是，7B 版本即已超越 Gemini-2.5 Pro，在性能与效率间取得了良好平衡。

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/016_Table_6.jpg]]
*Table 6: Ablation study of SpatialScore backbone sizes on the reward evaluation benchmark. “1 Pert.” and “2–3 Pert.” denote subsets constructed by applying one or two–three spatial perturbations, respectively, to perfect prompts for perturbed prompts*

### 在线 RL 训练结果

#### 空间基准评估

Table 2 展示了以 SpatialScore 为奖励的在线 RL 训练在多个空间基准上的详细对比。

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/007_Table_2.jpg]]
*Table 2: Detailed comparisons on SpatialScore, DPG-Bench, TIIF-Bench (short/long), and UnigenBench++ (short/long). * denotes training with Geneval as the reward model. BR, AR, and RR denote basic relation, attribute+relation, and relation+reasoning. Lay-2D/3D refer to layout-2D/3D. Unibench denotes UniGenBench++*

**核心结果：经过 GRPO 训练后，Flux.1-dev 的 SpatialScore 从 2.18 跃升至 7.81（提升 +5.63）**，而使用 GenEval 奖励训练的 **Flow-GRPO** 仅达到 3.01。在 **DPG-Bench** 的 Relation-Spatial 子维度上，我们的方法将准确率从 0.871 提升至 0.932（+0.061）。

在 **TIIF-Bench** 和 **UnigenBench++** 的短提示和长提示场景下，训练后的模型在基础关系（BR）、属性+关系（AR）、关系+推理（RR）以及 2D/3D 布局等所有子维度上均取得一致提升。这验证了 SpatialScore 奖励信号对空间理解的定向优化效果。

#### DPG-Bench 全维度评估

Table 3 展示了 DPG-Bench 五个主要维度的完整对比。我们的方法在所有维度上均超越原始 Flux.1-dev，整体得分从 82.91 提升至 85.03（+2.12），接近 **GPT-Image-1** 的水平。相比之下，使用 GenEval 训练的 Flow-GRPO 出现严重退化，整体得分降至 57.02，进一步证实了规则式奖励在在线 RL 中的局限性。

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/011_Table_3.jpg]]
*Table 3: Full-dimensional comparison on DPG-Bench. The best Flux variants are in bold, and * denotes training with GenEval*

#### Geneval 零样本泛化

Table 5 显示，在 Geneval 基准上，我们的模型将总体分数从 0.65 提升至 0.78（+0.13），证明了 SpatialScore 驱动的 RL 训练不仅提升了分布内性能，还带来了可观的零样本泛化能力。

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/015_Table_5.jpg]]
*Table 5: Quantitative evaluations on the Geneval benchmark. Our model is trained using SpatialScore as the reward model*

#### 跨模型泛化：Qwen-Image 基线

Table 7 展示了 SpatialScore RL 在 **Qwen-Image** 基线上的迁移效果。应用相同训练流程后，Qwen-Image 的 SpatialScore 从 6.74 提升至 8.25（+1.51），在 DPG-Bench、TIIF-Bench 和 UnigenBench++ 的所有子维度上均取得一致改善，验证了该方法的模型无关性和泛化潜力。

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/017_Table_7.jpg]]
*Table 7: Detailed comparisons for the Qwen-Image family on SpatialScore, DPG-Bench, TIIF-Bench (short/long), and UnigenBench++ (short/long). * denotes RL-training with our SpatialScore as the reward model. BR, AR, and RR denote basic relation, attribute+relation, and relation+reasoning. Lay-2D/3D refer to layout-2D/3D. Unibench denotes UnigenBench++*

### 消融实验：Top-k 过滤策略

Table 4 和 Figure 7 展示了 top-k 过滤策略的消融结果。

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/010_Table_4.jpg]]
*Table 4: Ablations on top-k filtering. NFE per prompt for each training step is reported under a denoising step count of 6*

**核心发现：k=6 的配置在多个基准上取得最佳性能**。无过滤（k=12，即标准 GRPO）时，由于简单提示的高奖励样本在组内标准化后获得负优势（Figure 5 所示的优势偏差问题），训练效果受限。k=4 的过滤过于激进，限制了样本多样性。k=6 在保持足够多样性的同时有效缓解了优势偏差。

此外，top-k 过滤显著降低了计算开销：每个训练步骤的 NFE（函数评估次数）从无过滤时的 144 降至 k=6 时的 72（去噪步数为 6 时），训练效率提升一倍。

### 定性分析

Figure 6 和 Figure 11 展示了复杂多对象空间关系提示的生成图像对比。经过 SpatialScore RL 训练的模型能够更准确地处理“左边/右边”、“上方/下方”、“前面/后面”等空间关系，在遮挡和多对象布局场景下表现尤为突出。相比之下，原始 Flux.1-dev 经常出现对象位置错误或关系混淆。

![[assets/figures/papers/paper_list_l2203_https_arxiv_org_abs_2602_24233/figures/008_Figure_6.jpg]]
*Figure 6: Qualitative comparison on prompts with complex spatial relationships across multiple objects*

### 失败模式与局限性

尽管取得了显著提升，当前方法仍存在以下局限：

1. **静态空间理解**：当前工作仅关注静态图像中的空间关系，尚未扩展到视频生成环境，无法处理随时间动态变化的空间关系（如物体移动、位置互换）。
2. **极端复杂场景**：对于高度组合性或极端复杂的空间场景，奖励模型和生成模型的性能可能仍有瓶颈，需进一步验证。
3. **计算开销**：虽然 top-k 过滤降低了 NFE，VLM 奖励模型的在线评估仍构成训练效率的主要瓶颈，如何进一步降低计算开销以支持更大规模训练是待解决问题。

### 关键图表索引

- **Table 1**：奖励模型成对准确率对比（SpatialScore 0.958 vs Gemini-2.5 Pro 0.951）
- **Table 2**：Flux.1-dev 在线 RL 训练后的空间基准详细对比（SpatialScore 2.18→7.81）
- **Table 3**：DPG-Bench 全维度对比（整体 82.91→85.03）
- **Table 4**：Top-k 过滤消融（k=6 最佳，NFE 144→72）
- **Table 5**：Geneval 零样本评估（0.65→0.78）
- **Table 6**：SpatialScore 骨干规模消融（3B: 0.891, 7B: 0.958, 32B: 0.973）
- **Table 7**：Qwen-Image 基线的跨模型泛化结果（SpatialScore 6.74→8.25）
- **Figure 6**：复杂空间关系提示的定性对比
- **Figure 7**：Top-k 过滤消融的训练曲线



## 定位与知识库关联

### 问题定位：空间理解为何成为图像生成的瓶颈

文本到图像（T2I）生成模型在图像质量和语义对齐方面取得了显著进展，但在**多对象复杂空间关系**的理解上仍存在系统性缺陷。现有奖励模型——包括基于人类偏好的通用图像奖励模型（如 **ImageReward**、**PickScore**、**HPSv3**）和基于VLM的统一奖励模型（如 **UnifiedReward**）——往往对空间错误的图像赋予比空间正确的图像更高的奖励分数（Figure 1），暴露了其空间推理能力的不足。另一方面，基于规则的 **GenEval** 奖励虽然能提供空间相关的反馈，但依赖对象检测器的刚性规则，在遮挡等视觉挑战下容易产生错误评估，且无法泛化到包含多对象复杂空间关系的长提示（Figure 2）。

这一瓶颈的因果链条清晰：缺乏专门的空间感知奖励模型 → 在线强化学习无法获得可靠的空间准确性反馈 → 生成模型在空间布局上缺乏有效优化信号 → 复杂空间提示的遵循能力停滞不前。

### 方法谱系：从通用奖励到空间专项奖励

本文提出的 **SpatialScore with Top-k GRPO** 在以下关键维度上对现有方法进行了系统性改进：

**奖励模型专项化**：此前的奖励模型要么面向通用图像质量（ImageReward、PickScore、HPSv3），要么依赖规则引擎（GenEval），均未针对空间关系进行专门设计。SpatialScore 以 **Qwen2.5-VL-7B**（Bai et al., 2025）为骨干网络，替换其语言建模头为线性奖励头，在精心构造的 **SPATIALREWARD-DATASET**（80k对抗性偏好对）上通过 Bradley-Terry 偏好损失进行微调，首次构建了专门评估空间关系准确性的VLM奖励模型。

**奖励信号源的范式转换**：Flow-GRPO 等方法使用 GenEval 的规则式奖励进行在线RL，受限于检测器的刚性逻辑。本工作将奖励信号源从规则引擎切换为VLM，使模型能获得细粒度的空间反馈。实验表明，GenEval训练的 Flow-GRPO 在 DPG-Bench 上出现严重退化（总分从82.91降至57.02），而 SpatialScore 引导的训练则带来一致提升。

**优势估计的偏差校正**：标准 GRPO 在组内对所有样本进行标准化计算优势时，对于简单提示（组内高分样本密集），部分高质量样本会因组均值过高而获得负优势（Figure 5），导致策略更新方向错误。本工作引入 **top-k过滤策略**：仅选取奖励最高和最低的 $2k$ 个样本参与组归一化（默认 $k=6$），有效缓解了不同难度提示导致的优势偏差，同时将每步训练的 NFE 从144降至72。

### 与专有模型的竞争定位

在奖励评估基准上，SpatialScore 7B 的总体成对准确率达到 **0.958**，超越 **GPT-5**（OpenAI, 2025）的 0.890 和 **Gemini-2.5 Pro** 的 0.951（Table 1）。值得注意的是，SpatialScore 的性能随骨干规模单调提升（3B: 0.891 → 7B: 0.958 → 32B: 0.973），7B版本已足以超越参数量远超自身的专有模型，表明专项微调比通用规模扩展在空间评估任务上更具效率。

在生成端，以 SpatialScore 为奖励的在线RL将 **Flux.1-dev**（Black Forest Labs, 2024）的 SpatialScore 从2.18提升至7.81，DPG-Bench 空间关系子维度从0.871提升至0.932（Table 2）。全维度评估中，本方法超越原始 Flux.1-dev，整体得分接近 GPT-Image-1（Table 3）。在 Qwen-Image 基线上的泛化实验进一步验证了方法的迁移性：应用 SpatialScore RL 后，SpatialScore 从6.74提升至8.25，所有空间基准一致改善（Table 7）。

### 适用边界与局限

本方法当前存在以下适用边界：

1. **静态空间理解的聚焦**：工作仅关注单帧图像中的静态空间关系，尚未扩展到视频生成环境，无法处理随时间动态变化的空间关系（如物体移动、位置互换）。这是空间理解从“空间布局”走向“时空一致性”的自然延伸方向。

2. **极端组合性场景的瓶颈**：对于高度组合性或极端复杂的空间场景，奖励模型和生成模型可能仍存在性能瓶颈。虽然 SpatialScore 在现有基准上表现优异，但其评估能力的上限尚未在更具挑战性的组合泛化测试中被充分验证。

3. **计算开销与在线RL效率**：VLM奖励模型的前向推理开销远高于规则式奖励，尽管 top-k 过滤降低了策略更新的 NFE，但奖励评估本身的计算成本仍是规模化的潜在障碍。

### 开放问题

1. **时空一致性的奖励建模**：如何将空间奖励建模有效拓展至视频生成，使模型能够理解和生成符合时序动态变化的空间一致序列？这需要构建包含时间维度的偏好数据集，并设计能评估帧间空间关系连贯性的奖励模型。

2. **奖励模型效率优化**：如何进一步降低空间奖励模型的计算开销，以满足更大规模在线RL训练的效率需求？可能的路径包括模型蒸馏、推理缓存或混合奖励策略（规则式粗筛+VLM精评）。

3. **组合泛化的深度验证**：当前基准中的空间扰动类型有限，如何构建更系统的组合泛化测试集，以揭示奖励模型和生成模型在未见空间关系组合上的真实能力边界？



## 原文 PDF

![[paperPDFs/CVPR_2026/Enhancing_Spatial_Understanding_in_Image_Generation_via_Reward_Modeling.pdf]]
