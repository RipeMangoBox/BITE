---
title: "VisionDirector: Vision-Language Guided Closed-Loop Refinement for Generative Image Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VisionDirector_Vision_Language_Guided_Closed_Loop_Refinement_for_Generative_Image_Synthesis.pdf
project_link: "https://visiondirector.github.io/"
code_link: null
aliases:
- VisionDirector
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将长指令分解为结构化目标，并引入闭环的目标级验证和回滚机制，使模型能够逐步检查每个子目标的完成情况并纠正错误；同时利用GRPO强化学习优化编辑策略，在保证质量的前提下缩短编辑步数。
primary_logic: 将复杂的多目标图像生成与编辑任务建模为多步决策过程，由视觉语言模型（VLM）作为“导演”进行规划、执行和验证，能够在不修改扩散模型本身的前提下，显著提升指令遵循性和目标完成度。
claims:
- 在LGBench上，添加VisionDirector后各基础模型的目标完成率均显著提升，如Flux-Krea从66.8%提升至74.9%，Flux-Dev从40.0%提升至62.4%。
- 在GenEval基准上，VisionDirector达到0.94总体分数，超越所有对比模型（如Qwen-Image 0.87），在Counting、Position、Attribute等子项上均领先。
- GRPO微调将平均编辑轮次从4.2降至3.1（约26%减少），同时目标覆盖率从0.74提升至0.78。
- LGBench (T2I) 上 Finish (%) = 74.9 (Flux-Krea + VisionDirector)
---

# VisionDirector: Vision-Language Guided Closed-Loop Refinement for Generative Image Synthesis

> [!tip] 核心洞察
> 将复杂的多目标图像生成与编辑任务建模为多步决策过程，由视觉语言模型（VLM）作为“导演”进行规划、执行和验证，能够在不修改扩散模型本身的前提下，显著提升指令遵循性和目标完成度。

| 字段 | 内容 |
|------|------|
| 中文题名 | VisionDirector：视觉语言引导的闭环精细化生成图像合成 |
| 英文题名 | VisionDirector: Vision-Language Guided Closed-Loop Refinement for Generative Image Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.19243) · [Project](https://visiondirector.github.io/) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VisionDirector |
| Dataset | LGBench, GenEval |

> [!tip] 效果简介
> - LGBench (T2I) 上，Finish (%) 74.9 (Flux-Krea + VisionDirector) vs 66.8 (Flux-Krea) (+8.1)；Finish (%) 62.4 (Flux-Dev + VisionDirector) vs 40.0 (Flux-Dev) (+22.4)。
> - GenEval 上，Overall 0.94 (VisionDirector) vs 0.87 (Qwen-Image) (+0.07)；Counting 0.96 vs 0.91 (Seedream 3.0) (+0.05)。

## 概要

当前文本到图像（T2I）与图像到图像（I2I）扩散模型在处理短指令时表现优异，但面对包含排版、局部物体放置、光照一致性等多目标紧密耦合的长指令时，目标完成率普遍偏低（55.9%–71.8%），经常遗漏局部编辑，且缺乏对多目标分解和闭环修正的能力。这一瓶颈源于模型缺乏将复杂指令结构化分解、逐步验证并纠正错误的机制。

**VisionDirector** 针对上述问题提出了一种无需训练、由视觉语言模型（VLM）引导的闭环控制框架。其核心思路是将复杂的多目标图像生成与编辑任务建模为多步决策过程：由 VLM 充当“导演”，将长指令分解为结构化目标，决定是一次性生成还是分阶段微编辑，并在每一步编辑后通过语义验证进行回滚修正，从而在不修改扩散模型本身的前提下，显著提升指令遵循性和目标完成度。

该框架进一步引入 **GRPO（Group Relative Policy Optimization）** 强化学习对规划器进行后训练，自动学习更优的编辑策略——何时停止、何时验证、何时编辑——在保证生成质量的同时有效缩短编辑轮次。

实验结果表明，VisionDirector 在多个基准上均带来显著提升：
- 在 **LGBench** 上，Flux-Krea 的目标完成率从 66.8% 提升至 74.9%（+8.1%），Flux-Dev 从 40.0% 提升至 62.4%（+22.4%）。
- 在 **GenEval** 基准上，VisionDirector 达到 0.94 的总体分数，超越 Qwen-Image（0.87）等对比模型，并在 Counting（0.96）、Position、Attribute 等子项上领先。
- GRPO 微调将平均编辑轮次从 4.2 降至 3.1（约 26% 减少），同时目标覆盖率从 0.74 提升至 0.78。

在方法谱系上，VisionDirector 属于**多模态智能体与扩散模型协同**的新范式，区别于直接修改生成模型架构或依赖固定规则编辑流程的传统方案。其规划器采用 Qwen3-VL-8B，编辑器使用 Qwen-Image 与 Qwen-Image-Edit，验证器基于 Qwen3-VL-32B-Instruct，整体框架以模块化闭环方式运行，可灵活适配不同的底层生成模型。

### 长指令图像生成的核心瓶颈

文本到图像（T2I）与图像到图像（I2I）的扩散模型近年来取得了显著进展，但在面对包含多个紧密耦合目标的复杂长指令时，仍暴露出系统性缺陷。现有模型通常采用一次性生成策略，将整个长提示直接编码为条件信号，缺乏对多目标进行分解、逐步执行和闭环修正的能力。这导致两个关键问题：

1. **目标遗漏与完成率低下**：在长指令场景中，模型经常遗漏局部编辑或精细约束。例如，在 **LGBench** 基准上，**Flux-Kontext** 的目标完成率仅为 55.9%，**Qwen-Image** 为 71.8%，而 **Flux-Dev** 则崩溃至 40.0%，几乎无法满足任何文本相关目标（仅 0.8% 成功率）。这表明单纯扩大模型规模或优化单步生成质量，并不能有效解决多约束指令的遵循性问题。

2. **缺乏结构化分解与验证机制**：现有方法普遍依赖文本-图像整体相似度评分或人工评价，缺少目标级别的语义验证。当指令涉及排版精度、局部物体放置、光照一致性等紧密耦合的约束时，模型无法感知每个子目标的完成状态，更无法在失败后进行针对性修正。

### 现有方法的局限性

当前主流的 T2I 与 I2I 系统可归为两类范式，均存在结构性缺口：

- **端到端生成模型**（如 **Flux-Krea**、**Flux-Dev**、**Qwen-Image**、**SD3 Medium**、**Seedream 3.0**）：将长指令一次性输入，依赖模型内部的交叉注意力机制隐式地处理多约束。这种方式缺乏显式的目标规划与分步执行，当指令长度增加、目标间存在冲突时，模型倾向于“遗忘”部分约束或产生幻觉。
- **基于编辑的迭代方法**（如 **Qwen-Edit**、**Qwen-Edit+**、**Flux-Kontext**）：虽然支持多轮编辑，但编辑策略通常由固定规则或人工设计，缺少自适应决策能力。每轮编辑后没有目标级的验证与回滚机制，错误会在迭代中累积，最终导致图像质量下降而非提升。

上述两类方法的共同盲区在于：**将复杂的多目标生成任务视为单步映射问题，而非多步决策过程**。它们缺少一个能够理解指令结构、规划执行顺序、验证中间结果并动态调整策略的“导演”角色。

### 本文的核心动机

针对上述瓶颈，**VisionDirector** 提出了一种范式转换：将长指令图像生成与编辑建模为由视觉语言模型（VLM）驱动的闭环决策过程。其核心动机可归纳为三个层面：

1. **从单步生成到多步规划**：将长指令分解为结构化的子目标序列，由 VLM 作为“规划器”决定执行顺序——是一次性生成还是分阶段微编辑——从而将复杂任务转化为可管理的子任务链。

2. **从开环执行到闭环验证**：在每一步编辑后引入目标级的语义验证，若子目标未满足则触发回滚并重试，从根本上阻断错误的累积传播。这一机制不修改扩散模型本身，而是作为外部控制器提升指令遵循性。

3. **从固定策略到强化学习优化**：利用 **GRPO（Group Relative Policy Optimization）** 对规划器进行后训练，使其自动学习更优的编辑策略——包括何时停止、何时验证、何时编辑——在保证目标覆盖率的同时缩短编辑步数，降低推理成本。

通过这些设计，VisionDirector 旨在在不改动底层扩散模型的前提下，显著提升多约束长指令场景下的目标完成率与生成质量，弥合开源模型与闭源商业系统之间的指令遵循性差距。

## 核心方法与创新机理

VisionDirector 的核心创新在于将多目标图像生成与编辑任务重新建模为一个**由视觉语言模型（VLM）驱动的闭环决策过程**，而非传统的一次性生成或固定规则编辑。其关键创新点体现在以下三个维度：

### 1. 结构化目标分解与闭环验证机制

现有扩散模型在处理包含多个紧密耦合目标的长指令时，目标完成率普遍较低（Flux-Kontex 仅 55.9%，Qwen-Image 为 71.8%），经常遗漏局部编辑要求。VisionDirector 引入了**目标级分解与语义验证**的闭环机制：

- **从直接生成到分阶段闭环编辑**：规划器 VLM（Qwen3-VL-8B）将长指令解析为结构化子目标，决定是一次性生成还是分步编辑，并通过微网格采样执行视觉更新。每一步编辑后均由验证器 VLM（Qwen3-VL-32B-Instruct）进行目标级语义验证——若子目标未满足则回滚并重试，从根本上抑制了幻觉累积。

- **从无验证到逐目标验证**：传统方法仅依赖文本-图像相似度或人工评价，缺乏对单个子目标的精确判断。VisionDirector 的验证器对每个目标进行独立评估，提供可解释的反馈，使系统能够精确定位并修正失败项。

这一创新直接带来了显著的性能提升：在 LGBench 上，Flux-Krea 的目标完成率从 66.8% 提升至 74.9%（+8.1%），Flux-Dev 更是从 40.0% 跃升至 62.4%（+22.4%）（Table 2）。

### 2. 基于 GRPO 的策略优化

VisionDirector 将编辑策略的学习形式化为强化学习问题，采用 **Group Relative Policy Optimization（GRPO）** 对规划器进行后训练，实现了从固定规则到自适应策略的跨越：

- **从固定规则到自适应策略**：传统编辑流程依赖人工设计的固定规则。GRPO 通过采样多条轨迹并利用对齐奖励进行优化，使规划器自动学习更优的决策策略——包括何时停止、何时验证、何时编辑。

- **效率与质量的双重提升**：GRPO 微调将平均编辑轮次从 4.2 降至 3.1（约 26% 减少），同时将目标覆盖率从 0.74 提升至 0.78（Table 6）。消融实验进一步表明，组合微网格采样、语义回滚和 GRPO 后，整体目标成功率达到 74.2%，高质量任务覆盖率（≥80%）达到 35.2%（Table 7）。

### 3. 训练无关的模块化架构

VisionDirector 的核心架构是**训练无关（training-free）**的：规划器和验证器均为现成的 VLM，编辑器为预训练的扩散模型，整个闭环无需对扩散模型本身进行任何修改或微调。这一设计使其能够灵活适配不同的基础模型（如 Flux-Krea、Flux-Dev、Qwen-Image），在 GenEval 基准上达到 0.94 的总体分数，超越所有对比模型（如 Qwen-Image 的 0.87），在 Counting、Position、Attribute 等子项上均取得领先（Table 4）。

> **注意**：上述 GenEval 对比模型（如 SD3 Medium、Seedream 3.0）的具体版本与发表信息未在分析数据中提供，需手动核实。

VisionDirector 构建了一个**模块化的闭环控制系统**，将复杂的多目标图像生成与编辑任务建模为多步决策过程。该框架由三个核心模块协同工作，在不修改底层扩散模型的前提下，显著提升指令遵循性和目标完成度。

### 核心模块与角色

| 模块 | 具体实现 | 核心职责 |
|------|----------|----------|
| **规划器 VLM** | Qwen3-VL-8B | 解析长指令、分解为结构化子目标、决策执行顺序（一次生成或分步编辑）、发出短指令并监督修订直至收敛 |
| **执行器** | Qwen-Image（T2I）/ Qwen-Image-Edit（I2I） | 执行文本到图像生成或图像编辑的视觉更新 |
| **验证器 VLM** | Qwen3-VL-32B-Instruct | 提供目标级语义反馈，评估每一步编辑是否满足子目标要求 |

### 闭环控制流程

框架运行在一个**训练无关（training-free）**的八阶段确定性控制流程中，其核心闭环逻辑如下：

1. **指令摄入与目标规划**：规划器接收长指令，将其分解为多个结构化子目标，并分析目标间的依赖与冲突关系。
2. **单次生成门控**：规划器判断任务复杂度——简单任务直接调用 T2I 编辑器一次生成；复杂任务则进入分阶段编辑模式。
3. **微网格采样执行**：在编辑阶段，采用微网格采样策略生成候选图像，提升排版等精细任务的成功率。
4. **语义验证与回滚**：验证器对每一步编辑结果进行目标级评估。若某个子目标未满足，系统回滚至上一步状态并重新执行，防止幻觉累积。
5. **迭代至收敛**：上述“编辑-验证-回滚”循环持续进行，直至所有子目标被满足或达到预设步数上限。

### 策略优化（GRPO 后训练）

在训练无关控制器的基础上，VisionDirector 进一步引入 **GRPO（Group Relative Policy Optimization）** 对规划器进行强化学习微调。GRPO 针对视觉编辑场景做了三项关键适配：

- **Token 级掩码**：仅对规划器生成的决策 token 计算策略梯度，避免对无关 token 的干扰。
- **对齐奖励**：基于验证器的目标覆盖率设计奖励信号，引导策略向高完成度方向优化。
- **Rollout 工作节点**：为每个采样的策略实时渲染图像，提供真实的视觉反馈用于策略评估。

GRPO 的目标函数为：

$$
\mathcal { I } _ { \mathrm { G R P O } } ( \theta ) = \mathbb { E } _ { x , \{ y ^ { ( i ) } \} } \Bigg [ \displaystyle \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \frac { 1 } { \sum _ { t } I ( y _ { t } ^ { ( i ) } ) } \sum _ { t } I ( y _ { t } ^ { ( i ) } ) \mathcal { L } _ { \mathrm { c l i p } } ( \rho _ { t } ^ { ( i ) } , \hat { A } _ { t } ^ { ( i ) } ) - \beta \mathrm { K L } ( \pi _ { \theta } \parallel \pi _ { \mathrm { r e f } } ) \Bigg ]
$$

该目标函数在 PPO 的基础上，对每个提示采样 $G$ 条轨迹，通过 token 掩码和 KL 正则化约束策略更新幅度，使规划器学会更高效的编辑策略——在保证目标覆盖率的同时，将平均编辑轮次从 4.2 降至 3.1（约 26% 减少）。

### 模块间数据流

整个框架的输入为**长文本指令**（含 15–23 个子目标），输出为**满足所有子目标的图像**。数据在各模块间的流转关系如下：规划器将长指令转化为短指令序列 → 执行器按序生成/编辑图像 → 验证器对中间结果打分 → 验证结果反馈至规划器，触发继续编辑或回滚决策。这一闭环设计使得 VisionDirector 能够像一位“导演”一样，持续监督和修正生成过程，直至达到满意的视觉效果。

![[assets/figures/papers/paper_list_l2357_https_arxiv_org_abs_2512_19243/figures/001_Figure_1.jpg]]
*Figure 1: VisionDirector is a framework that utilizes the VLM Planner to decompose tasks into multiple goals, perform planning and judgment, and progressively optimize both image-editing and image-generation tasks. It achieves performance comparable to, and in some cases even surpassing, closed-source commercial models*

### 3.1 闭环导演框架

VisionDirector 将多目标图像生成与编辑建模为多步决策过程，由 VLM 充当“导演”，在不修改扩散模型本身的前提下实现闭环控制。系统由三个模块化组件构成：

- **规划器 VLM (Planner)**：采用 **Qwen3-VL-8B**，负责解析长指令、将任务分解为结构化子目标、决定执行顺序（一次性生成或分阶段编辑），并监督每一步的修订直至收敛。
- **编辑器 (Editors)**：包括文本到图像编辑器（**Qwen-Image**）和图像到图像编辑器（**Qwen-Image-Edit**），执行具体的视觉更新操作。
- **验证器 VLM (Verifier)**：采用 **Qwen3-VL-32B-Instruct**，提供目标级别的语义反馈，评估每一次编辑是否满足对应的子目标。

这三个组件形成模块化闭环：指令输入 → 目标规划 → 一次性门控决策 → 微网格采样执行 → VLM 验证/回滚 → 决策策略调整。其核心因果机制在于：将复杂的长指令分解为可独立验证的子目标后，每一步编辑都经过语义验证，若目标不满足则回滚并重试，从而阻断错误累积。

### 3.2 训练无关的八阶段控制器

在训练无关（training-free）模式下，控制器遵循八个确定性阶段，其设计灵感来源于 DeepSeek-R1 风格的推理链，但专门针对视觉生成任务进行了适配：

1. **指令解析**：提取所有显式和隐式目标。
2. **冲突推理**：检测目标间的语义冲突并确定优先级。
3. **执行模式选择**：根据目标数量和复杂度，决定采用一次性生成（one-shot）还是分阶段编辑（staged）。
4. **微网格采样**：对关键区域（如排版文字）进行局部网格化采样，提高局部细节的可靠性。
5. **编辑执行**：调用 T2I 或 I2I 编辑器生成/修改图像。
6. **目标级验证**：验证器逐条检查子目标的完成情况。
7. **回滚决策**：若任一关键目标未通过验证，回滚到上一个检查点并重新编辑。
8. **收敛判断**：当所有目标通过验证或达到最大迭代次数时终止。

消融实验表明，移除微网格采样器会导致排版任务随机失败率增加 7%；禁用语义回滚则导致幻觉累积，目标覆盖率降至 0.74。组合所有优化策略（微网格+回滚+GRPO）后，整体目标成功率达到 74.2%，高质量任务覆盖率（≥80% 目标完成）达到 35.2%。

### 3.3 GRPO 策略优化

为进一步提升规划效率，VisionDirector 引入 **Group Relative Policy Optimization (GRPO)** 对规划器进行强化学习后训练。GRPO 是 PPO 的一种变体，针对视觉编辑场景进行了三项关键适配：

- **Token 级掩码**：仅对规划器生成的决策 token（如目标分解、执行模式选择）计算策略梯度，屏蔽图像内容 token，避免干扰扩散模型的生成质量。
- **对齐奖励**：以验证器的目标级反馈作为奖励信号，奖励函数基于每个子目标的完成与否构建，使策略直接优化目标覆盖率。
- **Rollout 工作节点**：对每个采样的策略，并行渲染图像以获取验证反馈，支持批量 rollout 训练。

GRPO 的目标函数为：

$$
\mathcal { I } _ { \mathrm { G R P O } } ( \theta ) = \mathbb { E } _ { x , \{ y ^ { ( i ) } \} } \Bigg [ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \frac { 1 } { \sum _ { t } I ( y _ { t } ^ { ( i ) } ) } \sum _ { t } I ( y _ { t } ^ { ( i ) } ) \mathcal { L } _ { \mathrm { c l i p } } ( \rho _ { t } ^ { ( i ) } , \hat { A } _ { t } ^ { ( i ) } ) - \beta \mathrm { K L } ( \pi _ { \theta } \parallel \pi _ { \mathrm { r e f } } ) \Bigg ]
$$

其中各变量含义：

- $x$：输入的长指令提示。
- $\{ y ^ { ( i ) } \}$：对同一提示 $x$ 采样的 $G$ 条轨迹（即 $G$ 个不同的编辑决策序列）。
- $I ( y _ { t } ^ { ( i ) } )$：Token 掩码指示函数，仅对决策 token 取值为 1，其余为 0。
- $\rho _ { t } ^ { ( i ) }$：第 $i$ 条轨迹在时间步 $t$ 的重要性采样比率。
- $\hat { A } _ { t } ^ { ( i ) }$：基于验证器反馈估计的优势函数。
- $\mathcal { L } _ { \mathrm { c l i p } }$：PPO 的裁剪损失函数。
- $\beta \mathrm { K L } ( \pi _ { \theta } \parallel \pi _ { \mathrm { r e f } } )$：KL 散度正则项，约束当前策略 $\pi_\theta$ 不偏离参考策略 $\pi_{\mathrm{ref}}$ 过远。

GRPO 的核心效果体现在两方面：将平均编辑轮次从 4.2 降至 3.1（约 26% 减少），同时将目标覆盖率从 0.74 提升至 0.78。这表明强化学习不仅缩短了推理开销，还通过优化决策时机（何时继续编辑、何时验证、何时停止）提升了任务完成质量。

## 实验与关键发现

### 主结果：长指令遵循能力的系统性提升

VisionDirector的核心价值在于作为一个训练无关的“导演”控制器，在不修改底层扩散模型的前提下，显著提升了各类生成模型对长指令的遵循能力。LGBench基准上的实验（Table 2）清晰地展示了这一效果：当VisionDirector介入后，Flux-Krea的目标完成率从66.8%跃升至74.9%（+8.1个百分点），而原本几乎无法处理文本相关指令的Flux-Dev更是从40.0%飙升至62.4%（+22.4个百分点）。这揭示了一个关键瓶颈：现有扩散模型并非缺乏生成能力，而是缺乏将长指令分解为可执行子目标并进行闭环验证的“规划”能力。

![[assets/figures/papers/paper_list_l2357_https_arxiv_org_abs_2512_19243/figures/005_Table_2.jpg]]
*Table 2: Performance comparison of models with and without VisionDirector*

在更通用的GenEval基准上（Table 4），VisionDirector以0.94的总分超越了所有对比模型，包括Qwen-Image（0.87）和Seedream 3.0（0.88）。值得注意的是，在Counting（计数）子任务上，VisionDirector取得了0.96的最高分，领先Seedream 3.0达5个百分点。这表明，通过显式的目标分解和逐项验证，模型能够更精确地控制生成图像中的物体数量——这是传统端到端T2I模型长期以来的薄弱环节。

在图像编辑任务上（Table 5），VisionDirector在ImgEdit基准的9个编辑原语上全面超越了先前的开源智能体方法，总分达到4.35，与闭源商业模型的表现具有竞争力。这验证了闭环验证机制在防止编辑过程中“幻觉累积”方面的关键作用。

![[assets/figures/papers/paper_list_l2357_https_arxiv_org_abs_2512_19243/figures/011_Table_5.jpg]]
*Table 5: Results on ImgEdit Bench. The scores range from 1 to 5, representing quality from low to high. The “Overall” column averages the scores across the nine tasks. Our VisionDirector significantly outperforms the open-source model and demonstrates competitive performance with the closed-source model*

### 消融实验：闭环机制的必要性

消融研究（Table 7）系统性地拆解了VisionDirector各优化策略的贡献。移除微网格采样器后，排版相关指令的随机失败率增加了7%，说明在长指令场景下，对生成空间的精细搜索是保证文本渲染质量的关键。更致命的是，禁用语义回滚机制会导致目标覆盖率骤降至0.74——这意味着每四个子目标中就有一个因错误累积而无法完成，充分证明了“编辑-验证-回滚”闭环的必要性。

![[assets/figures/papers/paper_list_l2357_https_arxiv_org_abs_2512_19243/figures/013_Table_7.jpg]]
*Table 7: Ablation study on different optimization strategies (values in %). “Goal” reports overall goal success rate, while ≥80% indicates task-level high quality coverage. Each strategy is tested independently except the final row which combines all*

将微网格采样、语义回滚与GRPO策略优化三者组合后，系统达到了最佳性能：整体目标成功率达到74.2%，高质量任务覆盖率（≥80%目标完成）达到35.2%。这一结果说明，各优化策略之间存在协同效应——微网格提供了更优的候选解，回滚机制防止了错误传播，而GRPO则在更高层次上优化了编辑策略的效率。

### GRPO策略优化：效率与效果的双赢

GRPO强化学习后训练的效果体现在两个维度（Table 6）。在效率维度上，平均编辑轮次从4.2降至3.1，减少了约26%的扩散模型调用次数，直接降低了推理成本。在效果维度上，目标覆盖率反而从0.74提升至0.78。这一“又快又好”的结果表明，原始的规划策略存在大量冗余或次优的编辑步骤，而GRPO通过探索和奖励机制，学习到了更精简、更有效的编辑策略——例如，学会了在何时进行“一次性生成”而非多步编辑，以及何时应该触发验证而非盲目迭代。

![[assets/figures/papers/paper_list_l2357_https_arxiv_org_abs_2512_19243/figures/012_Table_6.jpg]]
*Table 6: GRPO improves planning efficiency on LGBench. “Goal cov.” measures the fraction of verified goals per task; “Edits” counts diffusion executions*

### 自适应决策行为分析

Figure 6揭示了VisionDirector的规划器在不同任务复杂度下表现出的自适应行为。当指令中的子目标数量超过15个时，系统的迭代步数从1-3步跃升至5-7步，同时“一次性生成”的偏好从超过85%急剧下降至不足10%。这种阶段性切换是系统智能性的关键体现：对于简单指令，系统倾向于一次性生成以避免不必要的编辑开销；而对于复杂的长指令，系统自动切换到分阶段编辑模式，通过逐步验证和修正来保证最终质量。这一行为模式并非人工设计的规则，而是VLM规划器基于指令语义自主决策的结果，验证了将VLM作为“导演”进行高层规划的技术路线的有效性。

![[assets/figures/papers/paper_list_l2357_https_arxiv_org_abs_2512_19243/figures/009_Figure_5.jpg]]
*Figure 5: I2I result comparison with other models*

## 定位与知识库关联

### 1. 与基线工作的关系定位

VisionDirector 并非一个独立的图像生成模型，而是一个**训练无关的 VLM 引导控制器**，可叠加于现有的 T2I/I2I 扩散模型之上。其核心定位是**多目标指令遵循的闭环编排层**，而非替代底层生成器。

**与 T2I 基线的对比**

在 LGBench 基准上，直接使用现有 T2I 模型处理长指令时，目标完成率普遍偏低：**Flux-Krea** 为 66.8%，**Flux-Dev** 仅为 40.0%，**Qwen-Image** 为 71.8%。这些模型缺乏对多目标的结构化分解与逐目标验证能力，在文本排版、局部物体放置、光照一致性等紧密耦合需求上频繁遗漏局部编辑。

VisionDirector 通过将长指令分解为结构化子目标，并在每一步编辑后引入 VLM 验证与回滚机制，使各基础模型的目标完成率显著提升：Flux-Krea 从 66.8% 提升至 74.9%（+8.1%），Flux-Dev 从 40.0% 提升至 62.4%（+22.4%）。这表明**底层模型能力越弱，闭环编排带来的边际收益越大**——Flux-Dev 在文本相关目标上几乎完全失效（仅 0.8% 成功率），而 VisionDirector 的逐步验证机制有效补偿了这一缺陷。

在 GenEval 基准上，VisionDirector 以总体 0.94 的分数超越所有对比模型（如 **Qwen-Image** 0.87、**Seedream 3.0** 0.91），在 Counting（0.96）、Position、Attribute 等子项上均领先，证明了**目标级闭环验证对细粒度指令遵循的普适提升效果**。

**与 I2I 编辑基线的对比**

在 ImgEdit 基准上，VisionDirector 在所有编辑原语上均超越已有开源方案（如 **Qwen-Edit**、**Qwen-Edit+**、**Flux-Kontext**），总体评分 4.35，与闭源商业模型竞争力相当。这验证了“规划-执行-验证”循环在多步编辑任务中的有效性——传统 I2I 方法通常依赖单步编辑指令，缺乏对编辑结果的语义校验和纠错机制。

**方法谱系中的位置**

从方法论角度看，VisionDirector 属于**VLM 引导的闭环生成**这一新兴范式，与以下工作形成对比或互补：

- **端到端指令遵循模型**（如 Qwen-Image、Seedream 3.0）：通过扩大模型容量和数据规模提升指令遵循能力，但缺乏显式的目标分解与验证机制，在超长指令（>15 个目标）下性能退化明显。
- **基于规划的图像生成代理**（如先前开源的 VLM 代理）：通常采用固定规则或人工设计的编辑流程，缺乏自适应决策能力。VisionDirector 通过 GRPO 强化学习后训练，使规划器能够自动学习何时采用单次生成、何时分步编辑、何时触发验证与回滚。
- **基于反馈的生成优化**（如利用 CLIP Score 或人类偏好的方法）：仅在整体层面评估生成质量，缺乏目标粒度的语义验证。VisionDirector 的验证器 VLM（Qwen3-VL-32B-Instruct）对每个子目标进行独立的语义校验，提供可解释的逐目标反馈。

### 2. 适用边界与关键约束

**适用场景**

VisionDirector 在以下条件下表现最优：
- **多目标长指令**：指令包含 10–20 个子目标时，闭环编排的收益最大。当目标数超过 15 时，系统自动从单次生成模式切换为分阶段编辑模式（单次执行偏好从 >85% 降至 <10%），编辑轮次从 1–3 增至 5–7。
- **紧密耦合的视觉需求**：涉及排版精度、局部物体放置、多物体空间关系、光照一致性等需要精确控制的场景。
- **底层模型能力中等偏上**：VisionDirector 不修改底层生成器，因此其对弱模型的补偿效果更显著，但最终上限仍受限于编辑器能力。

**关键约束与失效模式**

1. **极端长指令退化**：当指令超过 25 个目标或存在高度冲突需求时，系统性能仍有下降空间。规划器在多目标冲突消解上的推理能力有限，可能导致部分目标被忽略或产生不一致的编辑结果。

2. **静态图像限定**：当前框架仅针对静态图像生成与编辑，尚未扩展到视频和 3D 资产。视频生成中的时序一致性、3D 生成中的多视角一致性等需求需要重新设计验证机制。

3. **验证器偏差**：验证器 VLM 的评分与人类偏好数据之间可能存在系统性偏差。论文明确指出尚未进行全面的人类偏好对齐，这意味着在某些主观性较强的任务（如艺术风格评价）上，验证器的判定可能与人类判断不一致。

4. **计算开销**：GRPO 强化学习微调需要大量 rollout（每个提示采样 G 条轨迹），计算开销较大，可能限制在大规模部署中的应用。尽管 GRPO 将平均编辑轮次从 4.2 降至 3.1（约 26% 减少），但训练阶段的成本仍然显著。

5. **编辑器依赖性**：VisionDirector 的编辑效果受限于底层 I2I 编辑器的能力边界。若编辑器在特定编辑类型（如大幅度姿态变换、复杂物体移除）上能力不足，闭环回滚可能陷入反复重试但无法收敛的状态。

### 3. 局限与开放问题

**已明确的局限**

- 评估和框架仅针对静态图像，尚未扩展到视频和 3D 资产。
- 验证器与人类偏好数据之间可能存在偏差，尚未进行全面的人类偏好对齐。
- GRPO 强化学习微调虽有效，但需进行大量 rollout，计算开销较大。
- 在极端长指令（超过 25 个目标）或高度冲突需求下，系统性能仍有下降空间。

**开放问题**

1. **跨模态扩展**：如何将“规划-执行-验证”的闭环框架高效扩展到视频和 3D 生成任务中？视频生成需要引入时序一致性验证，3D 生成需要多视角一致性检查，这些都对验证器的设计提出新挑战。

2. **奖励设计优化**：能否通过更好的奖励设计和数据增强（如引入对比性负样本、多维度奖励分解），使 GRPO 策略进一步提升？当前的对齐奖励（alignment-based reward）可能过于粗糙，无法捕捉细粒度的编辑质量差异。

3. **人机协同**：如何在多模态编辑中引入人机协同，以处理主观艺术方向上的需求？VisionDirector 的自动化验证机制在客观目标（如物体数量、位置）上表现良好，但在风格、氛围等主观维度上可能需要人类反馈的介入。

4. **验证器对齐**：验证器与人类偏好数据的对齐方法，是否需要构建更大规模的人工标注数据集？或者能否通过弱监督、偏好学习等方法降低对齐成本？

5. **规模化部署**：GRPO 训练的计算开销限制了大规模应用。是否存在更高效的策略优化方法（如离线 RL、基于模型的规划），能在保持性能的同时降低训练成本？

## 原文 PDF

![[paperPDFs/CVPR_2026/VisionDirector_Vision_Language_Guided_Closed_Loop_Refinement_for_Generative_Image_Synthesis.pdf]]
