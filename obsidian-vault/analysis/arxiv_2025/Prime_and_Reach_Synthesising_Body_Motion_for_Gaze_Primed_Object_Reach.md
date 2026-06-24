---
title: Prime and Reach Synthesising Body Motion for Gaze Primed Object Reach
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach.pdf
aliases:
- PRMDM
- PRSBMGPOR
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/generative_models_diffusion/diffusion_image_video
core_operator: 目标条件（目标姿势或目标位置）与基于注视-物体交集的预瞄-抓取数据集相结合，通过微调扩散模型隐式诱发预瞄行为。
primary_logic: 注视预瞄行为可以从包含全身体运动和注视标注的策划数据中，通过目标条件扩散模型隐式学习，而无需将其作为显式条件。
claims:
- 使用目标姿势条件，模型在GIMO上将预瞄成功率提升18.2%（绝对值）超过最佳基线，同时接近完美完成抓取。
- 在目标位置条件下，模型在MoGaze上的抓取成功率提升高达81.7%。
- 在MoGaze目标姿势条件下，P&R的预瞄成功率达到53.33，超越最强基线DNO（31.15）达22.18%。
- Nymeria预训练优于HumanML3D预训练，在HD-EPIC上预瞄成功率为51.00 vs. 47.10（DNO），MPJPE降低0.27。
---

# Prime and Reach Synthesising Body Motion for Gaze Primed Object Reach

> [!tip] 核心洞察
> 注视预瞄行为可以从包含全身体运动和注视标注的策划数据中，通过目标条件扩散模型隐式学习，而无需将其作为显式条件。

| 字段 | 内容 |
|------|------|
| 中文题名 | 注视预瞄引导的物体抓取全身运动合成 |
| 英文题名 | Prime and Reach Synthesising Body Motion for Gaze Primed Object Reach |
| 会议/期刊 | arXiv 2025 |
| Links | [Project](https://masashi-hatano.github.io/prime-and-reach/) · [paper](https://arxiv.org/abs/2512.16456) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/generative_models_diffusion/diffusion_image_video |
| Method | P&R Motion Diffusion Model |
| Dataset | HD-EPIC, MoGaze, GIMO |

> [!tip] 效果简介
> - HD-EPIC (Goal Pose) 上，Prime Success 53.45 vs 48.99 (DNO) (+4.46%)。
> - MoGaze (Goal Pose) 上，Prime Success 53.33 vs 31.15 (DNO) (+22.18%)；Reach Success 98.55 vs 78.68 (DNO) (+19.87%)。
> - HD-EPIC (Object Location) 上，Reach Success 100.00 vs 67.06 (DartControl fine-tuned) (+32.94%)。

## 概述

人类在伸手抓取物体之前，通常会先用目光“预瞄”目标——这种注视预瞄行为是自然交互的重要前兆。然而，现有运动生成方法依赖合成数据集或实验室录制，缺乏注视预瞄行为与全身体运动的真实配对，无法生成自然的预瞄-抓取运动。

本文提出 **P&R Motion Diffusion Model**，一种目标条件扩散模型，用于合成包含注视预瞄的全身抓取运动。核心思路是：注视预瞄行为可以从精心策划的数据中隐式学习，而无需将其作为显式条件。具体而言，作者从五个公开数据集中自动提取了 **23.7K 条** 包含注视-物体交集的预瞄-抓取序列，并以此为微调数据，在 Nymeria 大规模日常活动数据集上预训练的文本条件扩散模型基础上，引入目标姿势或目标位置作为条件，通过扩散潜变量优化在推理阶段进一步强化约束。

主要结果：
- 在 HD-EPIC 上，目标姿势条件下预瞄成功率（Prime Success）达到 **53.45%**，超越最强基线 DNO（48.99%）**+4.46%**；目标位置条件下抓取成功率（Reach Success）达 **100.00%**，较微调后的 DartControl（67.06%）提升 **+32.94%**。
- 在 MoGaze 上，目标姿势条件下预瞄成功率较 DNO 提升 **+22.18%**（53.33 vs. 31.15），抓取成功率提升 **+19.87%**（98.55 vs. 78.68）。
- Nymeria 预训练优于常用的 HumanML3D 预训练，在 HD-EPIC 上预瞄成功率提升至 51.00（vs. 47.10），MPJPE 降低 0.27。

该方法首次在全身运动合成中实现了可靠的注视预瞄行为生成，为构建更自然的具身交互系统提供了新路径。

## 背景与动机

### 问题背景：注视预瞄与物体抓取的全身运动合成

人类在抓取物体之前，通常会先用目光锁定目标物体——这一行为被称为“注视预瞄”（gaze priming）。预瞄行为不仅是人类运动意图的自然表达，也为智能体在复杂环境中的交互提供了关键的时空线索。然而，从计算角度合成包含注视预瞄行为的全身体运动，仍然是一个未被充分探索的挑战。

现有的运动生成方法主要分为两类。一类依赖大规模文本-运动数据集（如HumanML3D）进行条件生成，但这类数据通常来自合成环境或实验室录制，缺乏真实的注视行为标注。另一类方法利用目标条件（如目标位置或目标姿态）引导运动生成，但往往将注视行为视为显式条件，或者干脆忽略预瞄行为的存在。**核心瓶颈在于：现有数据集缺乏注视预瞄行为与全身体运动的真实配对，导致模型无法学习到“先看后抓”这一自然行为模式。**

### 现有方法缺口

当前运动生成领域存在三个关键缺口：

1. **数据缺口**：主流运动数据集（如HumanML3D、KIT-ML）不包含注视标注，而包含注视的数据集（如GIMO、MoGaze）又缺乏大规模、多样化的日常抓取序列。二者之间缺乏桥梁。

2. **方法缺口**：现有目标条件运动生成方法（如**WANDR**、**DNO**、**DartControl**）虽然能够生成到达目标位置的运动，但它们并未显式建模或评估注视预瞄行为。文本条件方法（如**MDM**、**GMD**）则完全无法利用目标空间信息，生成的抓取运动往往缺乏物理合理性。

3. **评估缺口**：目前尚无专门评估“预瞄-抓取”运动质量的指标。传统指标（如MPJPE、FID）只能衡量运动重建精度或分布相似性，无法捕捉“头部是否在抓取前指向了目标物体”这一关键行为特征。

### 本文动机

本文的核心动机是填补上述三个缺口。具体而言：

- **从数据角度**，我们提出自动策划流程，从五个包含注视标注的公开数据集中提取“预瞄-抓取”运动片段，构建首个大规模、多场景的Prime & Reach（P&R）数据集（23.7K序列）。
- **从方法角度**，我们设计目标条件扩散模型，通过微调隐式学习注视预瞄行为，而无需将其作为显式条件——这一洞察源于观察：当模型被要求生成“从初始状态到达目标姿态/位置”的运动时，预瞄行为会自然涌现。
- **从评估角度**，我们引入Prime Success指标，量化生成运动中的预瞄行为质量，为后续研究提供可复现的评估基准。

通过上述三个维度的贡献，本文旨在推动全身运动生成从“能生成运动”向“能生成符合人类行为规律的运动”演进。

## 核心创新

P&R的核心创新不在于提出全新的生成架构，而在于**将注视预瞄行为从显式建模问题转化为隐式学习问题**，通过三个关键层面的设计实现了这一转化。

### 1. 问题重构：从显式注视条件到隐式预瞄学习

现有运动生成方法面临的根本瓶颈是：注视预瞄行为与全身体运动的真实配对数据极度匮乏，实验室录制或合成数据集无法提供自然的预瞄-抓取序列。P&R的解决路径不是设计显式的注视生成模块，而是：

- **策划真实预瞄数据**：利用注视射线与3D物体边界框的交集检测，从五个公开数据集中自动提取包含预瞄-抓取行为的23.7K序列。预瞄时刻 $t_p$ 定义为注视射线首次与目标物体相交的最早时间戳（在抓取事件前10秒窗口内），计算公式为：

$$T_{\mathrm{int}} = \{ t | t \in [t_e - w, t_e], \mathbb{I}(\mathrm{intersect}(\hat{\mathbf{d}}_{\mathrm{gaze}}^t, o_{\mathrm{3D}})) = 1 \} \quad t_p = \min_{t \in T_{\mathrm{int}}} t$$

- **隐式诱发预瞄行为**：模型仅接收目标条件（目标姿势或目标位置）和初始状态，不接收任何注视相关条件。预瞄行为完全通过微调扩散模型从策划数据中隐式习得——模型学会了“在接近目标物体前自然地注视它”这一人类行为模式。

这一设计背后的核心洞察是：**注视预瞄是人类目标导向运动的固有组成部分，而非需要单独建模的独立行为**。

### 2. 条件注入机制：加法残差连接

P&R将初始状态（姿态与速度）和目标条件（目标姿势或物体位置）拼接后线性投影为向量 $\mathbf{p}$，通过残差加法注入文本条件token：

$$\tilde{\mathbf{z}}_{\mathbf{t}} = \mathbf{z}_{\mathbf{t}} + \mathbf{p}$$

消融实验（Table S6）证实，这种加法注入方式在8项指标中的7项上优于交叉注意力注入：

$$\delta_{\mathbf{t}} = \mathrm{Softmax}\left(\frac{(\mathbf{z}_{\mathbf{t}}\mathbf{W}_Q)(\mathbf{p}\mathbf{W}_K)^T}{\sqrt{d_k}}\right)(\mathbf{p}\mathbf{W}_V)$$

加法注入的优势在于保持条件信息与文本表征的紧密耦合，避免了交叉注意力中可能的信息稀释。

### 3. 预训练策略：Nymeria替代HumanML3D

现有文本到运动模型普遍使用HumanML3D进行预训练，但该数据集缺乏目标导向的日常活动序列。P&R改用**Nymeria**——一个大规模日常活动数据集（含叙述文本）进行预训练，在HD-EPIC上带来显著增益：

- 预瞄成功率从47.10（DNO，HumanML3D预训练）提升至51.00（Nymeria预训练）
- MPJPE降低0.27
- R-Precision提升34.0%，Multi-modal Distance降低2.68（Table S8）

这一改进说明，**预训练数据的生态效度**——即是否包含与下游任务相似的运动模式——比数据规模本身更为关键。

### 4. 推理优化：扩散潜变量噪声优化

为进一步提升生成质量，P&R在推理阶段引入扩散潜变量噪声优化：对初始噪声 $\mathbf{V}_T$ 进行 $M=400$ 次迭代优化，目标函数包含目标位置损失：

$$\bar{\mathcal{L}}_{\mathrm{goal}} = || o_{3\mathrm{D}} - x_{\mathrm{right~wrist}}^{N} ||_2^2$$

该优化使模型在仅给定目标位置的稀疏条件下，仍能生成精确到达目标的运动（HD-EPIC上抓取成功率达100.00%，较微调后的DartControl提升32.94%）。

### 与基线的根本差异

| 维度 | 现有方法（MDM/DNO/WANDR） | P&R |
|------|--------------------------|-----|
| 条件模态 | 文本或文本+初始状态 | 文本+初始状态+目标姿势/位置 |
| 预训练数据 | HumanML3D（通用文本-运动） | Nymeria（日常活动+叙述） |
| 微调数据 | 无（零样本）或文本条件 | 策划的23.7K预瞄-抓取序列 |
| 注视建模 | 不涉及 | 隐式学习（非显式条件） |
| 推理优化 | 直接采样或有限DNO | 400次潜变量噪声优化 |

综上，P&R的创新本质是**通过数据策划和条件设计，将注视预瞄这一复杂行为转化为扩散模型可隐式学习的涌现属性**，而非增加模型复杂度或显式建模新模态。

## 整体框架

P&R Motion Diffusion Model 的整体框架围绕一个核心设计展开：**通过目标条件（goal pose 或 object location）注入扩散模型，隐式地诱发注视预瞄行为，而非将其作为显式条件**。该框架由预训练、微调和推理优化三个阶段构成，其 pipeline 模块关系如下。

### 输入条件组合

模型接收三类条件信号：

1. **文本提示**：描述动作类型（如 "The person moves across and picks/puts an object"），经 Text Encoder 编码为隐空间 token $\mathbf{z}_{\mathbf{t}}$。
2. **初始身体状态**：包含初始姿态和速度，与目标条件拼接后线性投影为向量 $\mathbf{p}$。
3. **目标条件**（二选一）：
   - **目标姿态**：指定抓取时刻的全身姿态；
   - **目标位置**：仅指定 3D 物体位置 $o_{3\mathrm{D}}$，是更具挑战性的条件形式。

### 条件注入与运动生成

条件注入采用**残差加法**机制，将投影后的初始状态与目标条件 $\mathbf{p}$ 直接加到文本 token 上：

$$\tilde{\mathbf{z}}_{\mathbf{t}} = \mathbf{z}_{\mathbf{t}} + \mathbf{p}$$

消融实验证实，这种加法注入优于交叉注意力注入（Table S6），在 7/8 项指标上表现更佳。修改后的条件 $\tilde{\mathbf{z}}_{\mathbf{t}}$ 被注入 Transformer Decoder 的交叉注意力层，Decoder 从纯噪声出发，通过 $T=50$ 步扩散去噪，逐步生成 $N$ 帧的 263 维运动表示，涵盖 22 个关节的局部位置、局部旋转和局部速度。Post-Processor 随后将该表示转换为 3D 关节位置。

### 训练损失

总训练损失为两项之和：

$$\mathcal{L} + \mathcal{L}_{\mathrm{joint}}$$

其中 $\mathcal{L}$ 是 263 维运动表示的重构损失，$\mathcal{L}_{\mathrm{joint}}$ 是关节位置重构损失。消融实验表明，加入 $\mathcal{L}_{\mathrm{joint}}$ 可在 HD-EPIC 和 MoGaze 上同时降低 MPJPE 和定位误差（Table S5）。在目标位置条件下，额外引入目标位置损失：

$$\bar{\mathcal{L}}_{\mathrm{goal}} = || o_{3\mathrm{D}} - x_{\mathrm{right~wrist}}^{N} ||_2^2$$

约束预测的右手腕位置逼近 3D 物体位置。

### 推理阶段的潜在噪声优化

推理时引入 **Latent Noise Optimizer**，对初始噪声 $V_T$ 进行 $M=400$ 次迭代优化，使用与训练相同条件（初始状态 + 目标姿态或位置）的损失函数 $L_{\mathrm{opt}}$ 进行引导。这一优化步骤显著提升了生成质量，尤其是在仅给定目标位置的挑战性条件下——在 HD-EPIC 目标位置条件下，抓取成功率从微调版 DartControl 的 67.06% 提升至 100.00%（Table 3）。

### 预训练与微调策略

框架采用两阶段训练策略：
- **预训练**：在 Nymeria 大规模日常活动数据集（含叙述文本）上预训练 600K 步，学习率 $1\times10^{-4}$。相比 HumanML3D 预训练，Nymeria 预训练使 R-Precision 提升 34.0%，Multi-modal Distance 降低 2.68（Table S8），在 HD-EPIC 上 Prime Success 从 47.10 提升至 51.00（Table 4）。
- **微调**：在策划的 23.7K P&R 序列（来自 HD-EPIC、MoGaze、HOT3D、ADT、GIMO 五个数据集，按 70%/30% 划分训练/测试）上微调 250K 步，学习率 $5\times10^{-5}$。

### 架构消融关键发现

- **Decoder 优于 Encoder**：Transformer decoder 架构在 MoGaze 上 Prime Success 提升 5.57%，在 HD-EPIC 上定位误差降低 22.86（Table S4）。
- **扩散步数 $T=50$ 为最优平衡**：降至 $T=10$ 时，HD-EPIC 上 Prime Success 下降 1.55%（Table S7）。

### 数据流总览

整个 pipeline 的数据流为：**文本提示 + 初始状态 + 目标条件 → 条件编码与注入 → Transformer Decoder 扩散去噪（50 步）→ 263 维运动表示 → 关节位置后处理 → 推理时潜在噪声优化（400 次迭代）→ 最终运动序列**。该序列随后通过 Prime Success 和 Reach Success 等指标进行评估，评估时采用统一的 22 关节 HumanML3D 表示和一致的度量协议。

### 补充图表

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/004_Figure_3.jpg]]
*Figure 3: P&R motion diffusion model for goal-conditioned motion generation. We concatenate the initial state of the human body and the goal pose/goal object as conditions, along with a text condition describing the type of action the motion is expected to perform. This accumulated condition is injected into the transformer decoder layers, which then outputs an N-length motion sequence over multiple diffusion steps. At inference we perform diffusion latent noise optimisation over M iterations using the same conditioning (i.e. initial state and goal pose or location)*

## 核心模块与公式推导

P&R 运动扩散模型的核心思想是：将目标条件（目标姿态或目标位置）与文本提示、初始状态拼接后注入 Transformer 解码器，通过扩散去噪生成包含预瞄行为的全身运动序列。以下按模块拆解其关键设计与公式。

### 条件注入模块

模型接收三类条件：**文本提示** $c$、**初始状态**（身体姿态与速度）、**目标条件**（目标姿态或物体位置）。初始状态与目标条件被拼接后通过线性投影得到向量 $\mathbf{p}$，然后以残差加法注入文本条件的隐空间 token $\mathbf{z}_{\mathbf{t}}$：

$$\tilde{\mathbf{z}}_{\mathbf{t}} = \mathbf{z}_{\mathbf{t}} + \mathbf{p}$$

其中 $\mathbf{z}_{\mathbf{t}}$ 由文本编码器对提示 $c$ 编码得到。消融实验验证了加法注入优于交叉注意力注入（Table S6），后者在 8 项指标中的 7 项上表现更差。交叉注意力的消融形式为：

$$\delta_{\mathbf{t}} = \mathrm{Softmax}\left(\frac{(\mathbf{z}_{\mathbf{t}}\mathbf{W}_Q)(\mathbf{p}\mathbf{W}_K)^T}{\sqrt{d_k}}\right)(\mathbf{p}\mathbf{W}_V)$$

### Transformer 解码器

模型采用 Transformer **解码器**架构进行迭代去噪。消融表明解码器优于编码器：在 MoGaze 上将 Prime Success 提升 5.57%，在 HD-EPIC 上将 Loc Err 降低 22.86（Table S4）。解码器通过交叉注意力与修改后的条件 $\tilde{\mathbf{z}}_{\mathbf{t}}$ 交互，输出 $N$ 帧的 263 维运动表示 $\{v^n\}_{n=1}^{N}$，其中 $v^n \in \mathbb{R}^{263}$ 编码了 22 个身体关节的局部位置、局部旋转和局部速度。

### 训练损失

总训练损失由两部分组成：

$$\mathcal{L} + \mathcal{L}_{\mathrm{joint}}$$

- $\mathcal{L}$：263 维运动表示的重构损失。
- $\mathcal{L}_{\mathrm{joint}}$：关节位置重构损失。消融（Table S5）表明加入 $\mathcal{L}_{\mathrm{joint}}$ 可改善 HD-EPIC 和 MoGaze 上的 MPJPE 与 Loc Err。

在目标位置条件下，额外引入目标位置损失：

$$\bar{\mathcal{L}}_{\mathrm{goal}} = || o_{3\mathrm{D}} - x_{\mathrm{right~wrist}}^{N} ||_2^2$$

该损失约束预测的右手腕末端位置 $x_{\mathrm{right~wrist}}^{N}$ 接近 3D 物体位置 $o_{3\mathrm{D}}$。

### 扩散采样与推理优化

扩散过程设 $T=50$ 步，从纯噪声开始逐步去噪。消融显示 $T=50$ 为最佳平衡点，降至 $T=10$ 会使 HD-EPIC 上 Prime Success 下降 1.55%（Table S7）。

推理时引入**扩散隐空间噪声优化**：对初始噪声 $V_T$ 在 $M=400$ 次迭代中通过损失函数 $L_{\mathrm{opt}}$ 进行优化，以进一步对齐目标条件。该模块是 P&R 在目标位置条件下实现 100% Reach Success（HD-EPIC）的关键因素之一。

### 后处理模块

解码器输出的 263 维表示经后处理转换为 3D 关节位置，供评估指标（如 Prime Success、MPJPE）使用。当前模型生成全身运动但不包含手部细节，这是方法的一个已知局限。

## 实验与分析

### 核心实验设置

实验在五个策划数据集（HD-EPIC、MoGaze、HOT3D、ADT、GIMO）上评估P&R模型。所有方法统一使用HumanML3D的22关节运动表示，按70%/30%划分训练/测试集，采用一致的文本提示（"The person moves across and picks/puts an object"）。对于依赖文本条件的基线，零样本评估直接使用预训练权重；微调版本则在与P&R相同的策划数据上重新训练，确保公平比较。模型先在Nymeria数据集上预训练600K步（学习率1e-4），再在策划的P&R序列上微调250K步（学习率5e-5）。

### 主要结果

#### 目标姿势条件下的预瞄与抓取性能

P&R在目标姿势条件下显著超越所有基线方法。在HD-EPIC上，P&R的Prime Success达到53.45%，比最强基线DNO（48.99%）提升4.46个百分点（Table S3）。在MoGaze上优势更为突出：Prime Success达到53.33%，超越DNO（31.15%）达22.18个百分点；Reach Success达到98.55%，比DNO（78.68%）提升19.87个百分点。在GIMO上，P&R的预瞄成功率比此前最佳方法绝对提升18.2%，同时接近完美完成抓取任务（Section 5.4）。值得注意的是，DNO作为基于扩散噪声优化的强基线，在零样本条件下表现有限，而P&R通过目标条件微调实现了质的飞跃。

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/014_Table.jpg]]
*Table: S3: Per-Dataset Training - Comparison of motion generation baselines. Here, we train an independent model per dataset (HD-EPIC, MoGaze, HOT3D, ADT, and GIMO), and report results for each. The baselines are grouped by the type of conditioning used for generation. † denotes the zero-shot inference. For MDM, we evaluate two pre-trained models: (1) trained on HumanML3D, and (2) trained on Nymeria., denoted as ‡ and ∗, respectively. Entries without a marker correspond to models fine-tuned on our per-dataset P&R sequences*

#### 目标位置条件下的抓取性能

当仅给定物体3D位置作为条件时，P&R展现出更强的鲁棒性。在HD-EPIC上，P&R的Reach Success达到100.00%，比微调后的DartControl（67.06%）提升32.94个百分点（Table 3）。在MoGaze上，抓取成功率提升高达81.7%（Section 5.5）。这一结果表明，即使没有完整的姿态信息，模型也能从目标位置隐式推断出合理的全身运动轨迹。

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/008_Table_3.jpg]]
*Table 3: Impact of condition: We show how each of our modified conditions and optimisation impacts P&R model’s performance (last row)*

#### 跨数据集泛化能力

Table 2展示了单模型在所有数据集上联合训练的结果。P&R在HD-EPIC和MoGaze上保持领先，但在HOT3D和ADT上部分指标略低于DNO。这主要因为HOT3D和ADT的序列数较少（分别为1,482和1,814条，Table 1），且ADT的全身姿态依赖EgoAllo估计引入噪声。Table S1的消融表明，使用EgoAllo估计姿态相比真实Mocap数据，性能下降有限，验证了方法的实用性。

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/002_Table_1.jpg]]
*Table 1: Curated Dataset Statistics. We report statistics on curated P&R sequences across five publicly available datasets, ordering them by the size of curated sequences. We report the number of P&R sequences, duration between prime time and reach time i.e*

### 消融实验

#### 条件组件与推理优化的贡献

Table 3逐层拆解了各组件的贡献。基础模型（仅文本条件）几乎无法完成预瞄行为。加入初始状态条件后，Prime Success开始出现。进一步加入目标姿势条件使性能大幅跃升。最终加入扩散潜在噪声优化（M=400次迭代）后，模型在HD-EPIC上Prime Success达到53.45%，Reach Success达到100.00%。推理优化对目标位置条件尤为关键——它使模型在仅知物体位置的情况下，通过优化初始噪声隐式搜索合理的全身运动。

#### 架构选择

Transformer解码器优于编码器架构（Table S4）。在MoGaze上，解码器将Prime Success提升5.57%；在HD-EPIC上，定位误差降低22.86。解码器的自回归生成特性更适合运动序列建模。

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/015_Table.jpg]]
*Table: S4: Encoder $\mathbf { v } / \mathbf { s }$ Decoder. We compare encoder and decoder architecture for P&R motion generation. Table S5: Loss Ablation*

条件注入方式上，加法（$\tilde{\mathbf{z}}_{\mathbf{t}} = \mathbf{z}_{\mathbf{t}} + \mathbf{p}$）优于交叉注意力（Table S6），在8项指标中的7项取得更好结果。交叉注意力引入额外参数但未带来增益，表明简单的残差连接足以融合多模态条件。

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/016_Table.jpg]]
*Table: S6: Condition Injection. We verify different methods for injecting our initial state and goal conditions*

#### 损失函数与扩散步数

加入关节位置重建损失$\mathcal{L}_{\mathrm{joint}}$可改善MPJPE和定位误差（Table S5），因为它直接监督3D空间中的关节位置，弥补了263维表示空间中误差的不足。

扩散步数T=50在质量与效率间取得最佳平衡（Table S7）。降至T=10时，HD-EPIC上Prime Success下降1.55%；增至T=100提升有限但计算成本翻倍。

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/017_Table.jpg]]
*Table: S7: Impact of diffusion steps T . We compare the performance of P&R motion generation for multiple diffusion steps*

#### 预训练数据集的战略意义

Table 4揭示了预训练数据的关键作用。Nymeria预训练相比HumanML3D预训练，在HD-EPIC上将Prime Success从47.10%提升至51.00%（DNO基线），MPJPE降低0.27。Table S8进一步显示，Nymeria预训练使R-Precision提升34.0%，多模态距离降低2.68。Nymeria包含大规模日常活动数据与自然语言叙述，其运动分布更接近真实的人-物交互场景，为下游的预瞄-抓取任务提供了更好的初始化。

### 定性分析

Figure 5展示了三个数据集上的生成结果。在目标姿势条件下（半透明黄色），生成的运动在预瞄时刻的头部朝向与真值（浅绿色）高度一致，箭头方向准确指向目标物体。在目标位置条件下（棕色），模型虽无完整姿态参考，仍能生成合理的抓取轨迹。Figure 1从HD-EPIC展示了典型的预瞄行为：注视点（绿色十字）在接近物体前持续与目标（青色球体）相交，随后手部完成抓取。

### 失败模式与局限性

1. **手部细节缺失**：当前模型生成全身运动但不包含手部关节细节，无法直接评估抓取质量。这是向完整物体操纵扩展的主要障碍。
2. **数据噪声影响**：ADT和HOT3D等数据集的全身姿态依赖EgoAllo估计，引入一定噪声。Table S1显示这在ADT上导致轻微性能下降，但整体影响可控。
3. **场景泛化受限**：策划数据主要来自厨房场景（HD-EPIC占18,134条，占总数的76.4%），模型在其他环境中的表现有待验证。
4. **指标参数敏感性**：Prime Success依赖固定的时间窗口σ（1.0 s）、持续时长τ（0.1 s）和距离阈值δ（25 cm）。Figure S3的敏感性分析表明，放宽σ至1.5 s或收紧δ至15 cm会显著改变成功率数值，需针对不同数据集调整。

### 补充图表

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/005_Table_2.jpg]]
*Table 2: Comparison of motion generation baselines on our curated P&R sequences using different metrics. While we train a single model for all datasets, we separate results per dataset. We show results for test splits of HD-EPIC, MoGaze, HOT3D, ADT, and GIMO separately. The baselines are grouped by the type of conditioning used for generation. † denotes the zero-shot inference. For MDM, we evaluate two pretrained models: (1) trained on HumanML3D [24], and (2) trained on Nymeria. [57], denoted as ‡ and ∗, respectively. Entries without a marker correspond to models finetuned on our P&R sequences*

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/009_Table_4.jpg]]
*Table 4: Impact of pre-training. To validate our pre-training on Nymeria, we show the P&R model’s performance without pre-training and pre-trained on HumanML3D*

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/007_Figure_5.jpg]]
*Figure 5: Qualitative results on 3 datasets: Ground truth sequence in light green, goalpose conditioned prediction in translucent yellow, and target location conditioned generation in brown. We show the pose at the initial, prime, and reach timesteps. Prime direction for both ground truth and predictions is shown using arrows, and target object location is shown in sphere*

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/019_Table.jpg]]
*Table: S8: Pretraining results*

![[assets/figures/papers/paper_list_l1693_Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach/figures/018_Figure.jpg]]
*Figure: HD-EPIC . MoGaze Fig. S3: Varying time window σ and proximity threshold δ for Prime Success calculation on HD-EPIC and MoGaze*

## 方法谱系与知识库定位

### 1. 问题定位与核心瓶颈

现有运动生成方法主要面向文本到运动（text-to-motion）或语音到手势等任务，依赖合成数据集或实验室录制数据。这些方法存在一个根本性缺口：**缺乏注视预瞄行为与全身体运动的真实配对数据**。注视预瞄（gaze priming）——即人在接近目标物体时，头部和视线先于手部指向目标——是自然抓取行为的关键前兆，但现有数据集要么缺少注视标注，要么缺少全身体姿态，导致模型无法生成自然的预瞄-抓取运动序列。

P&R 方法的核心洞察在于：注视预瞄行为**不需要作为显式条件输入模型**，而是可以从包含全身体运动和注视标注的策划数据中，通过目标条件扩散模型隐式学习。这一发现改变了问题的建模方式——从“显式建模注视行为”转向“提供正确的数据与条件组合，让模型自发涌现预瞄能力”。

### 2. 与 Baseline 的关系与差异化

P&R 与以下基线方法形成对比，差异体现在条件模态、预训练策略、微调数据和推理优化四个维度：

**MDM**（text-to-motion diffusion）：仅使用文本条件生成运动，缺乏目标空间信息，无法引导手部或头部朝向特定物体。P&R 在其扩散架构基础上，增加了初始状态与目标条件的注入机制。

**GMD**（guidance-based motion diffusion）：在采样过程中引入引导信号，但未针对预瞄-抓取任务设计专门的条件表示。P&R 采用更直接的条件注入方式（残差加法），并通过策划数据微调获得任务特异性。

**DNO**（diffusion noise optimization）：通过优化扩散初始噪声来满足约束，是 P&R 最直接的对比基线。P&R 同样采用噪声优化（M=400 次迭代），但关键差异在于：(1) P&R 使用 Nymeria 大规模日常活动数据集预训练，而非 HumanML3D；(2) P&R 在策划的 23.7K 预瞄-抓取序列上微调。在 MoGaze 目标姿势条件下，P&R 的预瞄成功率（53.33）超越 DNO（31.15）达 22.18%（绝对值），抓取成功率从 78.68 提升至 98.55（Table S3）。

**DartControl**（autoregressive latent diffusion）：采用自回归潜在扩散架构。在 HD-EPIC 目标位置条件下，DartControl 微调版的抓取成功率为 67.06，而 P&R 达到 100.00（Table 3），差距达 32.94%。这表明 P&R 的联合条件注入与噪声优化策略在仅给定物体位置（无目标姿势）时具有显著优势。

**WANDR**（goal-conditioned c-VAE）：使用条件 VAE 架构进行目标条件运动生成。P&R 的扩散框架在运动质量和多样性上通常优于 VAE 类方法，且 P&R 的 Transformer 解码器架构（消融实验证实优于编码器架构，Table S4）提供了更强的序列建模能力。

**Static**：作为朴素基线（平均姿态），用于标定各指标的下界。

### 3. 方法适用边界

P&R 的适用性受以下因素约束：

- **场景域限制**：策划数据主要来自厨房场景（HD-EPIC、HOT3D 等以厨房活动为主），模型在非厨房环境（如户外、工业场景）中的泛化能力未经验证。
- **手部细节缺失**：模型生成 22 关节的全身体运动（263 维表示），但不包含手指关节。这意味着生成的序列可用于分析预瞄行为和身体逼近轨迹，但无法直接用于精细抓取评估或机器人操作控制。
- **姿态估计噪声**：部分数据集（如 HD-EPIC）的全身体姿态依赖 EgoAllo 估计，引入一定噪声。消融实验表明，使用估计姿态训练对性能的影响有限，但在极端遮挡或快速运动场景下，噪声可能放大。
- **Prime Success 指标的参数敏感性**：该指标依赖时间窗口 σ（1.0 s）、持续时长 τ（0.1 s）和距离阈值 δ（25 cm）三个固定参数。敏感性分析（Figure S3）表明，放宽 σ 和 δ 会提高所有方法的成功率，但 P&R 的相对优势保持稳定。实际应用中需根据场景调整这些阈值。

### 4. 局限与开放问题

**已知局限**：

1. **无手部生成**：当前模型输出不包含手指运动，无法端到端支持物体操纵。将手部运动生成整合到预瞄-抓取流程中，是实现完整交互的关键缺失环节。
2. **场景泛化不足**：策划数据集中于室内桌面操作场景，模型在开放环境中的行为尚未评估。
3. **注视行为隐式学习**：注视预瞄完全从数据中隐式涌现，模型没有显式的注视生成模块。这既是创新点也是局限——在数据稀缺或分布外场景中，预瞄行为可能退化。
4. **单物体、单人假设**：当前框架假设单个目标物体和单人操作，未涉及多物体选择或多人协作场景。

**开放问题**：

1. **联合注视-身体生成**：设计能够同时显式生成注视方向和身体运动的统一模型，而非仅依赖隐式学习，可能提升预瞄行为的可控性和可解释性。
2. **语义级目标条件**：当前使用目标姿势或 3D 位置作为条件。探索仅使用物体类别或自然语言描述（如“拿起桌上的蓝色杯子”）作为条件，将大幅降低条件获取成本。
3. **复杂交互扩展**：将预瞄-抓取合成扩展到多步骤操作序列（如拿起杯子→倒水→放回）和多人协同场景。
4. **真实机器人验证**：在真实机器人平台上验证生成的预瞄-抓取运动，评估从仿真到现实的迁移差距。

### 5. 知识库定位

P&R 处于**目标条件人体运动生成**与**注视行为建模**的交叉点。其贡献在于：

- **数据层面**：首次大规模策划并公开了注视预瞄与全身体运动的配对数据集（23.7K 序列，覆盖 5 个数据集），为该方向提供了基准。
- **方法层面**：证明了扩散模型可以通过目标条件隐式学习注视预瞄行为，而不需要显式的注视监督信号。这一发现简化了模型设计，并启发了“行为涌现”而非“行为监督”的研究思路。
- **评估层面**：引入 Prime Success 指标，量化评估生成运动中的预瞄行为质量，填补了现有指标（如 FID、MPJPE）无法捕捉任务特异性行为的空白。

在更广的运动生成领域，P&R 的方法论（大规模预训练 + 任务特异性数据微调 + 目标条件注入）与 NLP/CV 中的 foundation model 范式一致，暗示未来可能通过扩展数据规模和条件类型，构建更通用的目标导向运动生成基础模型。

## 原文 PDF

![[paperPDFs/arxiv_2025/Prime_and_Reach_Synthesising_Body_Motion_for_Gaze_Primed_Object_Reach.pdf]]