---
title: "VisionReasoner: Unified Reasoning-Integrated Visual Perception via Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/VisionReasoner_Unified_Reasoning_Integrated_Visual_Perception_via_Reinforcement_Learning.pdf
openreview_forum_id: QoDOwjsbAq
aliases:
- VisionReasoner
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "统一奖励机制（格式奖励+精度奖励）结合强化学习（GRPO）和多目标认知学习策略，使单个模型能够通过推理解决多种视觉感知任务。"
primary_logic: "将多种视觉感知任务重新定义为三个基础类别（检测、分割、计数），并利用强化学习与精心设计的统一奖励机制，可以训练出具备通用多目标认知与推理能力的统一模型。"
claims:
- "VisionReasoner在COCO检测、ReasonSeg分割和CountBench计数上分别相对提升29.1%、22.1%和13.2%，显著超越基线Qwen2.5VL。"
- "批量化匈牙利匹配算法将多目标匹配速度提升4倍，且不会损失精度。"
- "非重复奖励在多个数据集上带来一致的性能提升，并显著缩短推理响应长度。"
- "人工评估显示推理轨迹具有高图像一致性（97.0%）和答案一致性（90.5%），验证了推理过程的忠实性。"
---

# VisionReasoner: Unified Reasoning-Integrated Visual Perception via Reinforcement Learning

> [!tip] 核心洞察
> 将多种视觉感知任务重新定义为三个基础类别（检测、分割、计数），并利用强化学习与精心设计的统一奖励机制，可以训练出具备通用多目标认知与推理能力的统一模型。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | VisionReasoner：基于强化学习的统一推理整合视觉感知框架 |
| 英文题名 | VisionReasoner: Unified Reasoning-Integrated Visual Perception via Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=QoDOwjsbAq); [GitHub](https://github.com/JIA-Lab-research/VisionReasoner) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | VisionReasoner |
| Dataset | COCO val, RefCOCO val, RefCOCO+ val, RefCOCOg test |

> [!tip] 效果简介
> - COCO val 上，AP 为 37.7，对比 29.2 (Qwen2.5-VL-7B)，变化 +8.5 (29.1% relative)。
> - RefCOCO val 上，bbox AP 为 88.6，对比 88.8 (Qwen2.5-VL-7B)，变化 -0.2。
> - RefCOCO+ val 上，bbox AP 为 83.6，对比 82.3 (Qwen2.5-VL-7B)，变化 +1.3。

## 概述

**问题瓶颈**：现有视觉感知任务（检测、分割、计数等）高度碎片化，依赖特定任务模型或模块，缺乏统一的框架来同时处理多种任务，且推理能力有限。

**核心方法**：VisionReasoner 将多种视觉感知任务重新定义为检测、分割、计数三个基础类别，并采用强化学习（GRPO）与统一奖励机制（格式奖励 + 精度奖励）训练单一模型，使其具备通用多目标认知与推理能力。

**关键证据**：
- 在 COCO 检测上相对基线 **Qwen2.5-VL-7B** (Yang et al., 2024) 提升 **29.1%**，ReasonSeg 分割提升 **22.1%**，CountBench 计数提升 **13.2%**。
- 批量化匈牙利匹配算法将多目标匹配速度提升 **4 倍**，且不损失精度。
- 非重复奖励在多个数据集上带来一致性能提升，并显著缩短推理响应长度。
- 人工评估显示推理轨迹具有 **97.0%** 的图像一致性和 **90.5%** 的答案一致性，验证推理过程的忠实性。

**方法定位**：VisionReasoner 属于基于强化学习的统一视觉感知框架，以 Qwen2.5-VL 为视觉-语言骨干，结合 SAM2 分割模块和 TaskRouter 任务路由器，通过 GRPO 优化多任务推理能力。相比有监督微调（交叉熵损失）和分离式任务模型，其关键差异在于统一奖励驱动的多目标认知学习策略。

## 背景与动机

视觉感知是计算机视觉的核心任务，涵盖目标检测、实例分割、目标计数等多种形式。长期以来，这些任务依赖**特定任务模型或专用模块**（如 DQ-DETR 等检测器、SAM2 等分割器），各自独立设计架构与损失函数，缺乏统一的建模框架。近年来，大型视觉语言模型（LVLMs）如 **Qwen2.5-VL-7B**（Yang et al., 2024）和 **Qwen2-VL-7B**（Wang et al., 2024）展现了跨任务泛化的潜力，但其在视觉感知任务上的表现仍受限于两个关键瓶颈：

**瓶颈一：统一框架缺失。** 现有 LVLMs 通常通过监督微调（SFT）适配下游任务，使用交叉熵损失进行逐 token 优化。然而，检测、分割、计数等任务具有截然不同的输出形式（边界框坐标、掩码、数字），SFT 范式难以在单一模型中统一处理这些异构输出，导致模型在不同任务间性能参差不齐。

**瓶颈二：推理能力有限。** 复杂视觉场景往往需要多步推理——例如，“找到穿红色衬衫且戴眼镜的人旁边的蓝色杯子”需要链式逻辑推断。现有模型缺乏结构化的推理机制，难以在生成最终答案前进行显式的认知推理过程，限制了其在复杂指令下的表现。

针对上述问题，**VisionReasoner** 提出了一条统一的解决路径：将多种视觉感知任务重新定义为三个基础类别（检测、分割、计数），并利用**强化学习（GRPO）**配合精心设计的**统一奖励机制**，训练出具备通用多目标认知与推理能力的单一模型。其核心动机在于：通过奖励信号引导模型生成推理链，而非依赖特定任务的监督标签，从而实现跨任务的统一优化。

## 核心创新

VisionReasoner 的核心创新在于通过**统一奖励机制与强化学习**，将多种视觉感知任务整合到一个共享模型中，并赋予其可解释的推理能力。其关键设计突破体现在以下四个维度。

### 1. 训练范式变革：从监督微调到强化学习

传统视觉感知模型（如 Kosmos）通常采用交叉熵损失进行监督微调，而 VisionReasoner 转而使用 **GRPO（Group Relative Policy Optimization）强化学习**，其目标函数为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{x \sim \Pi\mathrm{ain} \mathrm{Batch}, \{\sigma_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{odd}}}(O|x)} \left[ \frac{1}{G} \sum_{i=1}^G \min\left( \frac{\pi_\theta(o_i \mid x)}{\pi_{\theta_{\mathrm{odd}}}(o_i \mid x)} A_i, \operatorname{clip}\left( \frac{\pi_\theta(o_i \mid x)}{\pi_{\theta_{\mathrm{odd}}}(o_i \mid x)}, 1-\varepsilon, 1+\varepsilon \right) A_i \right) - \beta D_{\mathrm{KL}}(\pi_\theta \parallel \pi_{\mathrm{ref}}) \right]$$

其中每个 rollout 的相对优势通过组内标准化计算：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \ldots, r_G\})}{\operatorname{std}(\{r_1, r_2, \ldots, r_G\})}$$

这一范式转换的因果机制在于：RL 奖励信号直接对预测-真值匹配质量进行优化，而非仅拟合 token 分布。消融实验证实，GRPO 和 DAPO 两种 RL 算法均在 ReasonSeg-val 上带来显著提升（基线 56.9 → GRPO 61.9 → DAPO 61.7），验证了 RL 范式本身的关键作用（Table 5）。

### 2. 任务架构统一：从多模型分立到单一模型覆盖

现有方案需为检测、分割、计数等任务分别设计专用模型或模块，VisionReasoner 将这些任务重新定义为三种基础类别，并通过统一的函数形式表达：

$$( \{ \mathbf { B } _ { i } , \mathbf { M } _ { i } \} ) _ { i = 1 } ^ { N } = \mathcal { F } ( \mathbf { I } , \mathbf { T } )$$

模型根据任务类型自动路由输出：

$$\mathrm { O u t p u t } = \left\{ \begin{array} { l l } { \{ \mathbf { B } _ { i } \} _ { i = 1 } ^ { N } , } & { \mathrm { i f } \mathbf { C } \mathrm { ~ i s ~ d e t e c t i o n } , } \\ { \{ \mathbf { M } _ { i } \} _ { i = 1 } ^ { N } , } & { \mathrm { i f } \mathbf { C } \mathrm { ~ i s ~ s e g m e n t a t i o n } , } \\ { N , } & { \mathrm { i f } \mathbf { C } \mathrm { ~ i s ~ c o u n t i n g } . } \end{array} \right.$$

其中任务分类由 TaskRouter 完成：$\mathbf { C } = { \mathcal { F } } _ { \mathrm { r o u t e r } } ( \mathbf { T } )$。分割任务采用 **detect-then-segment** 范式，计数任务采用 **detect-then-count** 范式，生成的检测框 $\{B_i\}$ 和中心点 $\{P_i\}$ 作为连接分割模块（SAM2）的桥梁。这种架构使单个 7B 模型在检测、分割、计数三大类任务上均取得领先，相对基线 Qwen2.5-VL-7B 分别提升 29.1%（COCO）、22.1%（ReasonSeg）和 13.2%（CountBench）。

### 3. 多目标匹配加速：批量化匈牙利算法

RL 训练要求对每个 rollout 进行预测-真值匹配以计算奖励，朴素匹配在 30 个目标场景下需 $2 \times 10^{-3}$ 秒。VisionReasoner 将匈牙利算法与批处理结合，实现 **4 倍加速**，仅需 $5 \times 10^{-4}$ 秒完成匹配，且不损失匹配精度（Table 3）。这是支撑 RL 训练可扩展性的关键工程创新。

### 4. 奖励设计精细化：格式奖励 + 精度奖励

奖励函数从简单的精度奖励扩展为四部分统一结构：
- **思考格式奖励**：促进结构化推理链生成
- **非重复格式奖励**：抑制冗余推理模式
- **多目标 IoU 奖励**：对 IoU > 0.5 的匹配框递增 $\frac{1}{\max\{N, K\}}$
- **L1 距离奖励**：对 L1 距离低于阈值（框 10 像素，点 30 像素）的匹配递增 $\frac{1}{\max\{N, K\}}$

消融实验（Figure 4）表明，非重复奖励在多个数据集上带来一致的性能增益，同时显著缩短推理响应长度——去除该奖励后模型倾向于生成更长且重复的推理过程。这揭示了奖励设计对推理效率与质量的双重调控作用。

## 整体框架

![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_QoDOwjsbAq/figures/006_Figure_3.jpg]]
*Figure 3: Illustration of VisionReasoner. (a) For a given image I and text instruction T, our model generates the expected output corresponding to the instruction. (b) For each observation o _ { i } . , we calculate the rewards (Section 3.4) and attain the optimal match of multi-objects (Section 3.5)*

VisionReasoner 将多种视觉感知任务统一到一个端到端框架中，其核心思路是将任务重新定义为三个基础类别——检测、分割和计数——并通过强化学习训练单一模型同时具备推理与多任务执行能力。

### 统一推理-感知流水线

模型以图像 $\mathbf{I}$ 和文本指令 $\mathbf{T}$ 作为输入，输出与指令对应的结果：

$$( \{ \mathbf { B } _ { i } , \mathbf { M } _ { i } \} ) _ { i = 1 } ^ { N } = \mathcal { F } ( \mathbf { I } , \mathbf { T } )$$

其中 $\mathbf{B}_i$ 为检测框，$\mathbf{M}_i$ 为分割掩码，$N$ 为目标数量。根据任务类型 $\mathbf{C}$，最终输出形式不同：

$$\mathrm { O u t p u t } = \left\{ \begin{array} { l l } { \{ \mathbf { B } _ { i } \} _ { i = 1 } ^ { N } , } & { \mathrm { i f } \mathbf { C } \mathrm { ~ i s ~ d e t e c t i o n } , } \\ { \{ \mathbf { M } _ { i } \} _ { i = 1 } ^ { N } , } & { \mathrm { i f } \mathbf { C } \mathrm { ~ i s ~ s e g m e n t a t i o n } , } \\ { N , } & { \mathrm { i f } \mathbf { C } \mathrm { ~ i s ~ c o u n t i n g } . } \end{array} \right.$$

任务类别由 TaskRouter 自动判定：

$$\mathbf { C } = { \mathcal { F } } _ { \mathrm { r o u t e r } } ( \mathbf { T } )$$

### 模块组成与数据流

流水线由五个关键模块串联构成（Figure 3）：

1. **Vision-Language Backbone（Qwen2.5-VL）**：处理图像和文本，生成结构化推理链，并从中提取目标检测框 $\mathbf{B}_i$ 和中心点 $\mathbf{P}_i$。这是整个框架的认知核心，承担“理解-推理-定位”的完整过程。

2. **Reasoning Module**：内嵌于 Backbone 中，负责生成可解释的推理轨迹（reasoning trace），使模型不仅输出结果，还显式展示其多步推理过程。推理链的忠实性经人工评估验证，图像一致性（IC）达 97.0%，答案一致性（AC）达 90.5%。

3. **Segmentation Module（SAM2）**：以检测框和中心点为桥梁，生成二值分割掩码 $\mathbf{M}_i$。框架采用“先检测后分割”（detect-then-segment）范式处理分割任务，采用“先检测后计数”（detect-then-count）范式处理计数任务，从而将三类任务统一到同一检测驱动的流程中。

4. **Multi-object Matching（批量化匈牙利算法）**：计算预测结果与真值之间的最优一对一匹配，用于奖励计算。该模块通过批量化计算将匹配速度提升 4 倍——在 30 个目标场景下，匹配耗时仅 $5 \times 10^{-4}$ 秒（Table 3），且不损失匹配精度。

5. **TaskRouter**：对输入指令进行任务分类并自动路由，使同一模型无需外部任务标识即可自适应切换输出格式。

### 训练范式与奖励设计

与以往使用交叉熵损失的监督微调方法（如 Kosmos）不同，VisionReasoner 采用 GRPO 强化学习框架进行训练。其核心创新在于统一奖励机制（unified reward），包含两类奖励：

- **格式奖励**：思考格式奖励（thinking reward）促进结构化推理，非重复奖励（non-repeat reward）抑制冗余推理模式。消融实验表明，非重复奖励在多个数据集上带来一致的性能提升，并显著缩短推理响应长度（Figure 4）。
- **精度奖励**：多目标 IoU 奖励和 L1 距离奖励，基于匈牙利匹配结果计算。检测框 IoU 超过 0.5 或 L1 距离低于 10 像素时给予正向激励，中心点 L1 距离阈值为 30 像素。

GRPO 通过组内奖励归一化计算相对优势：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \ldots, r_G\})}{\operatorname{std}(\{r_1, r_2, \ldots, r_G\})}$$

并最大化带裁剪的重要性采样目标（Equation 2），同时施加 KL 惩罚以防止策略偏离参考模型过远。

### 关键设计决策

框架将视觉感知任务压缩为检测、分割、计数三个基础类别的洞察，源于对现有任务共性的分析。这一简化使得单一模型无需任务特定模块即可覆盖多种下游应用。训练数据仅约 7k 样本（来自 LVIS、RefCOCOg、gRefCOCO 和 LISA++），模型以 Qwen2.5-VL 和 SAM2 初始化，batch size 16，学习率 $1 \times 10^{-6}$。有限的训练数据规模既是效率优势，也可能限制某些任务上的覆盖度，这一点在论文局限性中被明确指出。

## 核心模块与公式推导

### 3.1 强化学习目标：GRPO

VisionReasoner 采用 Group Relative Policy Optimization（GRPO）作为训练范式，替代传统的交叉熵监督微调。GRPO 的核心在于通过组内奖励的相对比较来估计优势函数，从而避免训练一个独立的价值网络。

对于每个输入 $x$，从旧策略 $\pi_{\theta_{\text{old}}}$ 中采样 $G$ 个 rollout $\{o_i\}_{i=1}^G$，每个 rollout 的奖励为 $r_i$。第 $i$ 个 rollout 的相对优势通过组内均值与标准差归一化得到：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \ldots, r_G\})}{\operatorname{std}(\{r_1, r_2, \ldots, r_G\})}$$

GRPO 的最大化目标为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{x \sim \mathrm{Train\ Batch},\ \{\sigma_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}(O|x)} \left[ \frac{1}{G} \sum_{i=1}^G \min\left( \frac{\pi_\theta(o_i \mid x)}{\pi_{\theta_{\mathrm{old}}}(o_i \mid x)} A_i,\ \operatorname{clip}\left( \frac{\pi_\theta(o_i \mid x)}{\pi_{\theta_{\mathrm{old}}}(o_i \mid x)}, 1-\varepsilon, 1+\varepsilon \right) A_i \right) - \beta D_{\mathrm{KL}}(\pi_\theta \parallel \pi_{\mathrm{ref}}) \right]$$

其中：$\pi_\theta$ 为当前策略，$\pi_{\theta_{\mathrm{old}}}$ 为旧策略，$\pi_{\mathrm{ref}}$ 为参考策略；$\varepsilon$ 控制裁剪范围；$\beta$ 为 KL 散度惩罚系数。该目标通过裁剪的重要性采样比率与 KL 正则化，在稳定训练的同时鼓励策略向高奖励方向优化。

### 3.2 统一模型架构与任务重定义

VisionReasoner 将多种视觉感知任务重新定义为三个基础类别——检测（Detection）、分割（Segmentation）、计数（Counting），并通过统一的模型架构 $\mathcal{F}$ 处理：

$$( \{\mathbf{B}_i, \mathbf{M}_i\} )_{i=1}^N = \mathcal{F}(\mathbf{I}, \mathbf{T})$$

其中 $\mathbf{I}$ 为输入图像，$\mathbf{T}$ 为文本指令，$N$ 为目标数量，$\mathbf{B}_i$ 为第 $i$ 个目标的检测框，$\mathbf{M}_i$ 为对应的分割掩码。

根据任务类别 $\mathbf{C}$，模型输出相应结果：

$$\mathrm{Output} = \begin{cases} \{\mathbf{B}_i\}_{i=1}^N, & \text{if } \mathbf{C} \text{ is detection}, \\ \{\mathbf{M}_i\}_{i=1}^N, & \text{if } \mathbf{C} \text{ is segmentation}, \\ N, & \text{if } \mathbf{C} \text{ is counting}. \end{cases}$$

任务分类由 TaskRouter 完成：

$$\mathbf{C} = \mathcal{F}_{\mathrm{router}}(\mathbf{T})$$

该模块将文本指令 $\mathbf{T}$ 映射到任务类别 $\mathbf{C}$，实现自动路由。

### 3.3 核心模块功能

模型由以下关键模块组成，形成“推理—检测—分割/计数”的级联流水线：

1. **Vision-Language Backbone（Qwen2.5-VL）**：处理图像和文本输入，生成可解释的推理链，并在推理过程中提取目标的检测框 $\mathbf{B}_i$ 和中心点 $\mathbf{P}_i$。
2. **Reasoning Module**：负责生成结构化的推理轨迹，定位用户指令指定的目标对象。推理链既作为可解释性的载体，也为后续模块提供精确的空间锚点。
3. **Segmentation Module（SAM2）**：采用“先检测后分割”（detect-then-segment）范式。检测框 $\mathbf{B}_i$ 和中心点 $\mathbf{P}_i$ 作为桥梁输入 SAM2，生成对应的二值分割掩码 $\mathbf{M}_i$。
4. **Multi-object Matching（Hungarian）**：在奖励计算阶段，通过批量化匈牙利算法求解预测结果与真值之间的最优一对一匹配。该模块将匹配速度提升 4 倍（30 个目标场景下耗时仅 $5 \times 10^{-4}$ 秒），且不损失匹配精度。
5. **TaskRouter**：对输入指令进行任务分类，将请求路由至对应的输出分支（检测框、掩码或数量）。

### 3.4 统一奖励机制

奖励函数由格式奖励和精度奖励两部分构成，统一适用于所有任务类型：

- **格式奖励**：包括思考格式奖励（thinking reward，鼓励结构化推理）和非重复奖励（non-repeat reward，抑制冗余推理模式）。消融实验表明，非重复奖励在多个数据集上带来一致的性能提升，并显著缩短推理响应长度（Figure 4）。
- **精度奖励**：包括多目标 IoU 奖励和 L1 距离奖励。对于检测框，IoU 超过 0.5 即获得奖励增量 $\frac{1}{\max\{N, K\}}$；L1 距离低于 10 像素阈值同样获得等量奖励增量。对于中心点，L1 距离阈值放宽至 30 像素。这些奖励通过匈牙利匹配建立预测-真值对应关系后计算，确保多目标场景下的公平评估。

### 3.5 关键设计要点

- **非重复奖励的因果机制**：RL 训练中模型倾向于生成冗长、重复的推理链以获取更高奖励。非重复奖励通过惩罚重复模式，迫使模型学习更简洁有效的推理策略，同时提升推理忠实度。人工评估显示推理轨迹的图像一致性（IC）达 97.0%，答案一致性（AC）达 90.5%。
- **批量化匈牙利匹配**：将匹配计算从逐样本串行改为批量并行处理，在保持最优匹配质量的前提下实现 4 倍加速，使 RL 训练中的奖励计算不再成为瓶颈。

## 实验与分析

### 主实验结果

VisionReasoner在检测、分割和计数三大类视觉感知任务上均取得显著提升，验证了统一框架与强化学习训练范式的有效性。

**检测性能**（Table 1）。在COCO val上，VisionReasoner-7B的AP达到37.7，相较于Qwen2.5-VL-7B基线的29.2，绝对提升+8.5，相对提升29.1%。在RefCOCO/RefCOCO+/RefCOCOg三个指代表达检测基准上，模型分别取得88.6/83.6/87.5的AP，其中RefCOCO val略低于基线（-0.2），但RefCOCO+和RefCOCOg分别提升+1.3和+1.8。四项检测任务平均AP为80.3，超越基线1.7个点，在LVLM方法中达到最优。值得注意的是，与传统特定任务检测模型（如DQ-DETR）相比，VisionReasoner在COCO上的绝对性能仍有差距，但其优势在于无需任务特定架构即可处理多种检测任务。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_QoDOwjsbAq/figures/007_Table_1.jpg]]
*Table 1: Performance comparison on detection tasks*

**分割性能**（Table 2）。在ReasonSeg val上，VisionReasoner取得66.3 gIoU，相较Qwen2.5-VL-7B基线的56.9提升+9.4（相对提升22.1%），超越Seg-Zero-7B（Liu et al., 2025a）等专门的分割RL基线。在RefCOCO/+/g系列分割任务上，模型也保持稳定优势，分割平均gIoU达到71.0（基线67.7，+3.3）。所有LVLM方法在分割任务中均使用了SAM2作为掩码生成模块，VisionReasoner通过检测框/中心点作为桥梁连接SAM2，其性能增益主要来自更准确的定位推理。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_QoDOwjsbAq/figures/008_Table_2.jpg]]
*Table 2: Performance comparison on segmentation tasks and counting tasks. We use SAM2 for vision-language models if necessary in segmentation tasks. Table 4: Comparison on the reasoning length. Table 5: Comparison on different RL algorithm*

**计数性能**（Table 2）。在PixMo和CountBench两个计数基准上，VisionReasoner的平均准确率达到76.7%，相较基线63.6%提升+13.1个百分点（相对提升13.2%）。该结果验证了“先检测后计数”范式的有效性——模型通过推理定位目标后再统计数量，而非直接输出数字。

**VQA能力保持**（Table 7）。在OCRBench、RealworldQA、MMMUPro、MMBench、ChartQA等六个VQA基准上，VisionReasoner-7B在所有任务上均保持或超越Qwen2.5-VL-7B的性能，表明强化学习训练并未损害模型的通用视觉理解能力。

### 消融实验

**非重复奖励**（Figure 4）。非重复格式奖励在多个数据集上带来一致的性能增益，同时显著缩短推理响应长度。移除该奖励后，模型倾向于生成更长的重复推理模式，既降低效率又影响精度。这一发现表明，在RL训练中显式惩罚重复输出有助于引导模型学习更简洁有效的推理链。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_QoDOwjsbAq/figures/013_Figure_4.jpg]]
*Figure 4: Ablation on non-repeat reward. (a) Consistent performance gain across different datasets using non-repeated reward. (b) Non-repeat rewards lead to shorter response lengths*

**多目标匹配效率**（Table 3）。结合批处理与匈牙利算法的多目标匹配实现4倍加速。在30个目标的场景下，非批处理匹配需2×10⁻³秒，而优化后的批处理匈牙利匹配仅需5×10⁻⁴秒，且不损失匹配精度。这一优化对于训练效率至关重要，因为每次rollout都需要计算预测与真值的最优匹配以确定奖励。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_QoDOwjsbAq/figures/009_Table_3.jpg]]
*Table 3: Comparison of multiobject matching. Our code achieves a 4× speedup*

**RL算法对比**（Table 5）。在ReasonSeg val上，GRPO将基线gIoU从56.9提升至61.9，DAPO提升至61.7，两种RL算法均带来显著增益，GRPO略优。这验证了强化学习范式本身（而非特定算法选择）是性能提升的核心驱动。

**训练数据扩展**（Table 6）。依次添加RefCOCOg、gRefCOCO、LVIS和LISA++训练数据，模型平均性能（检测+分割）从73.0持续提升至76.2。每增加一个数据源都带来正向收益，表明多源数据混合训练有助于提升模型的泛化能力。训练数据总量仅约7k样本，这一数据效率值得关注。


![[assets/figures/papers/paper_list_l33_https_openreview_net_forum_id_QoDOwjsbAq/figures/014_Table_6.jpg]]
*Table 6: Performance comparison on different training data*

**采样数影响**（Figure 5）。不同采样数（rollout数量）会影响性能。适度增加采样数可提升探索效率，但过量采样可能导致过拟合并损害泛化能力。这一发现对RL训练的超参数选择具有指导意义。

**推理过程的作用**（Figure 6）。有无推理过程的对比表明，显式的推理链生成对复杂感知任务（特别是ReasonSeg）有显著帮助，而对简单检测任务的影响相对较小。

### 推理忠实性验证

人工评估（Table 8）显示，VisionReasoner的推理轨迹在所有IoU范围内均表现出高图像一致性（IC 97.0%）和答案一致性（AC 90.5%），验证了推理过程的忠实性——模型生成的推理链确实反映了其对图像内容的理解，而非产生与视觉输入无关的“幻觉推理”。

### 局限性

当前训练数据仅约7k样本，可能限制模型在某些长尾任务上的覆盖度。过度采样可能导致过拟合（Figure 5），需要在训练中谨慎控制采样数。此外，当前评估覆盖了10个代表性任务，更全面的任务类型评估留待未来工作（Tables 14-15）。

## 方法谱系与知识库定位

### 1. 方法脉络与基线关系

VisionReasoner 的核心定位是将多种视觉感知任务统一到单一推理框架中，其方法谱系可从训练范式、任务架构和奖励设计三个维度梳理。

**训练范式的迁移**：主流大视觉语言模型（LVLM）通常采用监督微调（SFT）配合交叉熵损失，例如 **Kosmos**（Peng et al., 2024）。VisionReasoner 则转向强化学习范式，采用 GRPO（Group Relative Policy Optimization）进行训练，其目标函数为：

$$\mathcal{I}_{\mathrm{GRPO}}(\theta) = \mathbb{E}_{x \sim \mathrm{TrainBatch}, \{o_i\}_{i=1}^G \sim \pi_{\theta_{\mathrm{old}}}(O|x)} \left[ \frac{1}{G} \sum_{i=1}^G \min\left( \frac{\pi_\theta(o_i \mid x)}{\pi_{\theta_{\mathrm{old}}}(o_i \mid x)} A_i, \operatorname{clip}\left( \frac{\pi_\theta(o_i \mid x)}{\pi_{\theta_{\mathrm{old}}}(o_i \mid x)}, 1-\varepsilon, 1+\varepsilon \right) A_i \right) - \beta D_{\mathrm{KL}}(\pi_\theta \parallel \pi_{\mathrm{ref}}) \right]$$

其中优势函数 $A_i$ 通过组内奖励的均值与标准差归一化计算：

$$A_i = \frac{r_i - \operatorname{mean}(\{r_1, r_2, \ldots, r_G\})}{\operatorname{std}(\{r_1, r_2, \ldots, r_G\})}$$

这一转变的关键瓶颈在于：RL 训练要求预测与真值之间进行最优匹配，而 SFT 的逐 token 交叉熵损失天然避免了这个需求。VisionReasoner 通过批量化匈牙利算法解决了多目标匹配的效率问题，在 30 个目标的场景下将匹配时间从 $2\times10^{-3}$ 秒压缩至 $5\times10^{-4}$ 秒，实现 4 倍加速且不损失精度（Table 3）。

**任务架构的统一化**：此前视觉感知任务依赖分离的模型或模块，例如 **DQ-DETR** 专用于检测，**Seg-Zero-7B**（Liu et al., 2025a）基于 RL 处理分割。VisionReasoner 将所有任务重新定义为三个基础类别——检测、分割、计数——并通过统一的“先检测后分割/计数”范式处理。模型以 **Qwen2.5-VL-7B**（Yang et al., 2024）为视觉语言骨干，以 **SAM2** 为分割模块，输出形式由 TaskRouter 根据指令类别自动路由：

$$\mathrm{Output} = \begin{cases} \{\mathbf{B}_i\}_{i=1}^N, & \text{if }\mathbf{C}\text{ is detection}, \\ \{\mathbf{M}_i\}_{i=1}^N, & \text{if }\mathbf{C}\text{ is segmentation}, \\ N, & \text{if }\mathbf{C}\text{ is counting}. \end{cases}$$

**奖励设计的精细化**：相比简单的准确率奖励，VisionReasoner 的统一奖励机制包含格式奖励（思考格式奖励、非重复格式奖励）和精度奖励（多目标 IoU 奖励、L1 奖励）。其中非重复奖励在多个数据集上带来一致的性能提升，并显著缩短推理响应长度（Figure 4），这是此前 RL 训练中未被充分探索的维度。

### 2. 适用边界与性能定位

**检测任务**：在 COCO val 上，VisionReasoner 以 37.7 AP 显著超越基线 Qwen2.5-VL-7B 的 29.2 AP（相对提升 29.1%），但在 RefCOCO val 上略低于基线（88.6 vs. 88.8）。在 RefCOCO+ val 和 RefCOCOg test 上分别取得 83.6 和 87.5，均优于基线。检测任务平均 AP 为 80.3，较基线的 78.6 提升 1.7 个点（Table 1）。

**分割任务**：在 ReasonSeg val 上，VisionReasoner 以 66.3 gIoU 大幅超越基线 Qwen2.5-VL-7B 的 56.9 gIoU（相对提升 22.1%），且优于 **Seg-Zero-7B**（61.9 gIoU，GRPO 训练）和 **DAPO** 变体（61.7 gIoU，Table 5）。分割任务平均 gIoU 为 71.0，较基线的 67.7 提升 3.3 个点（Table 2）。

**计数任务**：在 PixMo 和 CountBench 上平均准确率达 76.7，较基线 63.6 提升 13.1 个点（Table 2），相对提升 13.2%。

**VQA 能力保持**：VisionReasoner 在 MMMU、RealWorldQA、ChartQA 等 VQA 基准上保持竞争力，未因视觉感知任务的 RL 训练而退化（Table 7）。人工评估显示推理轨迹具有 97.0% 的图像一致性和 90.5% 的答案一致性（Table 8），验证了推理过程的忠实性。

### 3. 局限与开放问题

**数据覆盖度**：训练数据仅约 7k 样本，来自 LVIS、RefCOCOg、gRefCOCO 和 LISA++ 四个数据集的训练划分。尽管依次添加这些数据集使平均性能从 73.0 持续提升至 76.2（Table 6），但有限的样本量可能限制模型在更多任务类型上的覆盖度。当前仅评估了 10 个代表性任务，全面评估更多任务类型留待未来工作。

**采样过拟合风险**：消融实验显示，过量采样可能导致过拟合并损害泛化能力（Figure 5），这提示 RL 训练中的采样数量需要在性能提升与泛化保持之间谨慎平衡。

**复杂指令的边界**：虽然定性比较显示 VisionReasoner 在复杂指令下正确定位物体，而 **DINO-X** 和 **YOLO-World** 失败（Figure 2），但这一结论仅基于有限的定性样本，尚未在标准化的复杂指令基准上进行系统验证。

**开放问题**：当前框架未涉及视频理解、3D 感知等更广泛的视觉任务类型，其统一范式的可扩展性有待验证。此外，RL 训练中奖励权重的自动调优、更大规模训练数据的构建策略，以及推理链质量与任务性能之间更精细的因果关系分析，均为值得进一步探索的方向。

## 原文 PDF

![[paperPDFs/ICLR_2026/VisionReasoner_Unified_Reasoning_Integrated_Visual_Perception_via_Reinforcement_Learning.pdf]]
