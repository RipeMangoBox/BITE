---
title: "Revisual-R1: Advancing Multimodal Reasoning From Optimized Cold Start to Staged Reinforcement Learning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Revisual_R1_Advancing_Multimodal_Reasoning_From_Optimized_Cold_Start_to_Staged_Reinforcement_Learning.pdf
openreview_forum_id: NTo6f6GENJ
aliases:
- RR
- Revisual-R1
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "采用纯文本的高难度冷启动数据预先构建推理引擎，然后通过配备优先级优势蒸馏（PAD）的多模态 RL 将推理能力与实际视觉基础对齐，最后通过文本 RL 微调巩固和锐化综合推理技能。"
primary_logic: "1) 有效的冷启动初始化对 MLLM 推理至关重要，仅使用精选文本数据即可使模型在多模态推理上优于许多现有方法；2) 标准 GRPO 在多模态 RL 中存在梯度停滞，而提出的 PAD 通过过滤零优势样本并重加权有效轨迹来稳定训练、提升效果；3) 在多模态 RL 之后进行文本 RL 微调，可以进一步打磨语言表达和逻辑一致性，从而增强多模态推理能力。"
claims:
- "有效冷启动：纯文本数据训练即可显著提升多模态推理性能，超越多种多模态冷启动方法。"
- "PAD解决梯度停滞：通过选择性过滤零优势样本并进行温度控制的优先采样，PAD 显著稳定了训练并提升了样本效率。"
- "分阶段 RL 优于单阶段或混合训练：先多模态 RL (MRL) 再文本 RL (TRL) 的顺序在消融实验中达到最佳平均性能 (49.6)，明显优于反向顺序 (45.5) 或混合训练 (47.6)。"
- "多模态与文本推理基准平均 (Multimodal & Textual Benchmarks Average) 上 Pass@1 平均准确率 (Average Accuracy) = 53.1"
---

# Revisual-R1: Advancing Multimodal Reasoning From Optimized Cold Start to Staged Reinforcement Learning

> [!tip] 核心洞察
> 1) 有效的冷启动初始化对 MLLM 推理至关重要，仅使用精选文本数据即可使模型在多模态推理上优于许多现有方法；2) 标准 GRPO 在多模态 RL 中存在梯度停滞，而提出的 PAD 通过过滤零优势样本并重加权有效轨迹来稳定训练、提升效果；3) 在多模态 RL 之后进行文本 RL 微调，可以进一步打磨语言表达和逻辑一致性，从而增强多模态推理能力。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Revisual-R1：通过优化冷启动与分阶段强化学习推进多模态推理 |
| 英文题名 | Revisual-R1: Advancing Multimodal Reasoning From Optimized Cold Start to Staged Reinforcement Learning |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=NTo6f6GENJ); [GitHub](https://github.com/CSfufu/Revisual-R1) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | ReVisual-R1 |
| Dataset | 多模态与文本推理基准平均 (Multimodal & Textual Benchmarks Average) |

> [!tip] 效果简介
> - 多模态与文本推理基准平均 (Multimodal & Textual Benchmarks Average) 上，Pass@1 平均准确率 (Average Accuracy) 为 53.1，对比 36.3 (最佳开源 7B 基线)，变化 +16.8。

## 概述

多模态大语言模型（MLLM）的推理能力是其迈向通用人工智能的关键瓶颈。现有方法面临两个核心障碍：其一，标准 GRPO 算法在多模态强化学习中存在**梯度停滞**问题——当组内样本奖励相同时，优势值归零，模型失去有效学习信号；其二，传统的多模态冷启动数据集缺乏足够复杂性，难以充分激发模型的推理潜能。

针对上述问题，本文提出 **ReVisual-R1**，一种从优化冷启动到分阶段强化学习的多模态推理训练框架。其核心因果路径可概括为：**先用纯文本高难度数据构建推理引擎，再通过配备优先级优势蒸馏（PAD）的多模态 RL 将推理能力与视觉基础对齐，最后以文本 RL 微调巩固语言表达与逻辑一致性**。

具体而言，ReVisual-R1 包含三个关键洞察：

1. **有效冷启动**：仅使用精筛的文本推理数据对基座模型进行微调，即可在多模态推理任务上超越多种多模态冷启动方法，证明推理能力本身具有跨模态迁移性。
2. **PAD 解决梯度停滞**：通过过滤零优势样本并进行温度控制的优先采样，PAD 将训练聚焦于高信息量轨迹，显著稳定训练并提升样本效率。
3. **分阶段 RL 优于混合训练**：先多模态 RL（MRL）后文本 RL（TRL）的顺序在消融实验中达到最佳平均性能（49.6），明显优于反向顺序（45.5）或混合训练（47.6）。

在实验层面，ReVisual-R1-7B 在多个多模态与文本推理基准上取得 **53.1%** 的平均准确率，较最佳开源 7B 基线提升 **+16.8** 个百分点，并超越 GPT-4o 的平均表现（41.6%）。消融实验进一步证实了完整三阶段训练（CS + MRL + TRL）与 PAD 各组件的必要性。

本方法的局限性在于：文本中心优化策略泛化到多模态推理的深层理论解释尚不充分；可扩展性仅在 3B 和 7B 规模上验证，更大架构（如 MoE）的表现未知；数据类型与训练阶段之间的复杂交互尚未系统研究。

## 背景与动机

多模态大语言模型（MLLM）在视觉-语言任务中展现出强大的能力，但在复杂多模态推理（如数学、逻辑、科学图表理解）上仍面临显著瓶颈。现有方法主要依赖监督微调（SFT）或标准强化学习（RL）来增强推理能力，但存在两个关键缺口：

**1. 冷启动数据的选择困境。** 传统多模态推理训练通常使用多模态冷启动数据集（如 Vision-R1、R1-One-Vision 所用数据），但这些数据集往往缺乏足够的推理深度和复杂性。实验证据表明，仅使用多模态数据训练的模型在多模态和文本推理任务上的增益均十分有限（Figure 3 紫色虚线）。相比之下，高难度、长推理链的纯文本数据（如 DeepMath、OpenR1-Math，平均响应长度达 8207.76 tokens，远超多模态数据的 821.48 tokens）能构建更强的推理引擎，并意外地泛化到多模态场景（Figure 3 红色虚线）。

**2. 标准 GRPO 在多模态 RL 中的梯度停滞。** Group Relative Policy Optimization（GRPO）是当前主流的多模态 RL 算法，其核心是计算组内相对优势函数：

$$\hat{A}(x,y_i) = \frac{r(x,y_i) - \mathrm{mean}(\{r(x,y_1),\ldots,r(x,y_G)\})}{\mathrm{std}(\{r(x,y_1),\ldots,r(x,y_G)\}) + \epsilon}$$

当组内所有样本获得相同奖励时（全部答对或全部答错），优势值归零，策略梯度消失，训练陷入停滞。这一“梯度停滞”问题严重损害了训练稳定性和样本效率，而现有方法（如 DAPO）尚未有效解决。

**本文动机。** 针对上述缺口，ReVisual-R1 提出“先构建推理引擎，再对齐视觉基础，最后打磨语言表达”的分阶段策略：首先用高质量纯文本数据完成冷启动，然后通过配备优先级优势蒸馏（PAD）的多模态 RL 将推理能力与视觉感知对齐，最后用文本 RL 微调恢复语言流畅性和高阶推理能力。该框架在 7B 规模上取得了 53.1% 的平均准确率，较最佳开源基线提升 +16.8 个百分点（Table 2）。

## 核心创新

ReVisual-R1 的核心创新围绕三个关键设计展开：**纯文本冷启动构建推理引擎**、**优先级优势蒸馏（PAD）解决多模态 RL 中的梯度停滞**、以及**分阶段强化学习（先多模态后文本）实现能力对齐与锐化**。这三者形成因果链条——先通过高难度文本数据建立强推理能力，再用 PAD 稳定地将该能力与视觉感知对齐，最后通过文本 RL 打磨语言表达与逻辑一致性。

### 文本冷启动：用纯文本数据构建推理引擎

传统多模态冷启动方法直接使用图文配对数据微调模型，但 ReVisual-R1 发现这一策略存在根本性局限：多模态冷启动数据的推理链长度极短（平均仅 821.48 tokens），远不足以激发模型的深层推理能力。相比之下，纯文本高难度推理数据（如 DeepMath）的平均响应长度达 8207.76 tokens，能迫使模型生成更长的思维链，从而建立更强的推理基础。

基于这一洞察，ReVisual-R1 在冷启动阶段**完全采用文本数据**（283K 条高难度、长推理链样本），不使用任何图像输入。实验结果表明，仅靠文本冷启动，模型在多模态推理任务上的绝对性能增益（红色虚线平均值）已显著优于使用多模态冷启动的方法（紫色虚线平均值），甚至超越了部分专门设计的多模态推理系统（见 Figure 3）。这一发现直接挑战了“多模态任务必须用多模态数据初始化”的直觉，揭示出**推理能力本身具有跨模态可迁移性**——先在文本空间建立强推理引擎，再将其与视觉感知对齐，比直接在图文混合空间训练更为有效。

### 优先级优势蒸馏（PAD）：破解多模态 RL 的梯度停滞

标准 GRPO 在多模态强化学习中存在严重的梯度停滞问题。其组内优势函数定义为：

$$\hat{A}(x,y_i) = \frac{r(x,y_i) - \mathrm{mean}(\{r(x,y_1),\ldots,r(x,y_G)\})}{\mathrm{std}(\{r(x,y_1),\ldots,r(x,y_G)\}) + \epsilon}$$

当组内所有样本的奖励相同时（全部答对或全部答错），标准差接近零，所有样本的优势均为零，导致策略梯度消失，训练完全停滞。这一问题在多模态任务中尤为突出，因为视觉推理的奖励信号往往更加稀疏。

PAD 通过两个关键操作解决这一瓶颈：

1. **过滤零优势样本**：设定绝对优势阈值区间 $[T_{\mathrm{low}}, T_{\mathrm{high}}]$（其中 $T_{\mathrm{low}} > 0$），仅保留绝对优势落在此范围内的样本，直接剔除无法提供学习信号的零优势轨迹。

2. **温度控制的优先采样**：从有效样本集中，按绝对优势的 Softmax 分布进行采样：

$$\mathrm{Pr}(i \text{ is selected} \mid i \in \mathcal{E}) = \frac{\exp(\hat{A}_i / \tau)}{\sum_{j \in \mathcal{E}} \exp(\hat{A}_j / \tau)}$$

温度参数 $\tau$ 控制探索与开发的平衡，使训练聚焦于高信息量样本（既非过于简单也非完全错误的中间难度样本），同时保持一定的探索性。

消融实验（Table 4）验证了完整 PAD 的有效性：PAD 平均分 47.7，显著优于基线 GRPO 的 45.1、仅过滤策略的 46.2、以及随机采样策略的 46.5。训练动态曲线（Figure 4）进一步显示，PAD 不仅提升了最终性能，还显著稳定了训练过程，减少了奖励方差。

### 分阶段强化学习：先对齐后锐化

ReVisual-R1 将强化学习分为两个顺序阶段，而非混合训练：

- **多模态 RL（MRL）**：在 21K 多模态样本上训练，冻结视觉编码器，省略 GRPO 中的 KL 散度约束以鼓励更广泛的策略探索。此阶段的核心目标是将文本冷启动建立的抽象推理能力与视觉感知对齐。

- **文本 RL（TRL）**：在 31K 复杂文本任务上进一步训练，恢复并增强语言流畅性和高阶推理能力。此阶段针对 MRL 后可能出现的语言退化问题进行修复，同时进一步打磨逻辑一致性。

消融实验（Table 3）清晰展示了分阶段顺序的关键性：CS + MRL + TRL 序列达到 49.6 平均分，而反向顺序（CS + TRL + MRL）仅为 45.5，混合训练（Mixed-RL）为 47.6。这一结果表明，**先对齐后锐化**的顺序至关重要——在多模态对齐完成之前进行文本 RL 会干扰视觉-推理的绑定过程，而混合训练则导致两种优化目标相互干扰。

### 创新点之间的因果依赖

三个创新点并非独立设计，而是形成因果闭环：文本冷启动提供了高质量的初始推理能力（起点），PAD 确保了多模态 RL 阶段的有效学习信号（过程），分阶段顺序则决定了能力迁移的最终效果（路径）。缺少任一环节都会导致性能退化——仅冷启动为 47.1，冷启动 + MRL（无 TRL）为 48.2，冷启动 + MRL + TRL 达到最优 49.6。这一递增趋势验证了各组件间的协同效应。

## 整体框架

![[assets/figures/papers/iclr26_0010_NTo6f6GENJ_Revisual-R1_Advancing_Multimodal_Reasoning_From/figures/002_Figure_2.jpg]]
*Figure 2: (Top): the overview of our proposed ReVisual-R1 framework.After collcting and curating data, ReVisual-R1 contains cold start and staged reinforcement learning. (Bottom): the process of our proposed prioritized advantage distillation (PAD) for multimodal reinforcement learning*

ReVisual-R1 提出了一套三阶段训练流程，旨在解决多模态大语言模型（MLLM）在复杂推理任务中的两个核心瓶颈：**冷启动数据缺乏推理复杂性**，以及**标准 GRPO 在多模态强化学习中的梯度停滞问题**。

### 三阶段流水线

如图 2（上）所示，ReVisual-R1 的完整训练包含以下顺序执行的三个阶段：

1.  **文本冷启动（Cold Start）**
    仅使用高难度、长推理链的纯文本数据对基座模型进行监督微调，预先构建强大的推理引擎。论文发现，纯文本冷启动数据（如 DeepMath 数据集，平均响应长度达 8207.76 tokens）能显著激发模型的推理能力，其带来的多模态推理性能增益甚至超过了使用多模态数据冷启动的方法（如 Vision-R1、R1-One-Vision，其平均响应长度仅 821.48 tokens）。这一阶段为后续的多模态对齐奠定了推理基础。

2.  **多模态强化学习（Multimodal RL, MRL）**
    在 GRAMMAR 数据集的多模态部分上，使用配备**优先级优势蒸馏（PAD）**的 GRPO 算法进行训练。此阶段的核心目的是将第一阶段构建的抽象推理能力与实际的视觉感知进行对齐。标准 GRPO 在此阶段面临严重的梯度停滞：当组内样本奖励相同（全部答对或全部答错）时，优势函数为零，导致策略梯度消失。PAD 通过过滤零优势样本并对高信息量轨迹进行优先采样，稳定了训练过程（详见第 4.1.1 节）。此外，MRL 阶段移除了 GRPO 的 KL 散度约束，以鼓励更广泛的策略探索。

3.  **文本强化学习（Textual RL, TRL）**
    在多模态 RL 完成后，冻结视觉编码器，仅用纯文本的复杂任务进行最终的 GRPO+PAD 强化学习微调。这一阶段的作用是恢复并增强语言流畅性，同时进一步打磨高阶推理的逻辑一致性。消融实验证实，先 MRL 后 TRL 的顺序（平均分 49.6）显著优于反向顺序（45.5）或混合训练（47.6），表明分阶段训练是必要的。

### PAD 机制概览

PAD 是嵌入在 MRL 和 TRL 阶段的核心优化组件（图 2 下）。其工作流程为：对每个 GRPO 采样组，首先过滤掉绝对优势不落在 $[T_{\text{low}}, T_{\text{high}}]$ 范围内的样本（其中 $T_{\text{low}} > 0$，直接剔除零优势样本），然后在有效样本集 $\mathcal{E}$ 中，按温度控制的 Softmax 概率进行优先采样：

$$\operatorname{Pr}(i \text{ is selected} \mid i \in \mathcal{E}) = \frac{\exp(\hat{A}_i / \tau)}{\sum_{j \in \mathcal{E}} \exp(\hat{A}_j / \tau)}$$

这一设计将训练焦点集中在能提供有效学习信号的样本上，从而解决了梯度停滞问题。

### 数据流

整个流程的数据流由 GRAMMAR 数据集支撑（表 1），该数据集包含 283K 文本样本用于冷启动，以及额外的 31K 文本和 21K 多模态样本用于后续的强化学习阶段。

## 核心模块与公式推导

### 多模态推理的形式化与GRPO

ReVisual-R1将多模态推理建模为一个策略优化问题。给定输入 $x$（包含图像与文本指令），模型策略 $\pi_\theta$ 生成回答 $y$，目标是最大化期望奖励：

$$\theta^{*} = \arg\max_{\theta} \mathbb{E}_{x\sim\mathcal{D}} \mathbb{E}_{y\sim\pi_{\theta}(y|x)} [r(y,x)] \tag{1}$$

其中 $r(y,x)$ 为奖励函数，$\mathcal{D}$ 为任务分布。

为实现稳定训练，ReVisual-R1采用**组相对策略优化 (GRPO)**，其核心目标函数为：

$$\mathbb{E}_{x\sim\mathcal{G}_i} \mathbb{E}_{y\sim\pi_{\theta}(y|x)} \left[ \min\left( \frac{\pi_{\theta}(y|x)}{\pi_{\theta_{\mathrm{ref}}}(y|x)} \hat{A}(x,y), \, \mathrm{clip}\left( \frac{\pi_{\theta}(y|x)}{\pi_{\theta_{\mathrm{ref}}}(y|x)}, 1-\epsilon, 1+\epsilon \right) \hat{A}(x,y) \right) \right] \tag{2}$$

该目标通过对新旧策略比率进行裁剪来限制更新幅度，其中 $\pi_{\theta_{\mathrm{ref}}}$ 为参考策略，$\epsilon$ 为裁剪阈值。

GRPO的关键创新在于**组内相对优势**的计算。对于同一输入 $x$ 采样的 $G$ 个回答 $\{y_1,\ldots,y_G\}$，第 $i$ 个回答的优势为：

$$\hat{A}(x,y_i) = \frac{r(x,y_i) - \mathrm{mean}(\{r(x,y_1),\ldots,r(x,y_G)\})}{\mathrm{std}(\{r(x,y_1),\ldots,r(x,y_G)\}) + \epsilon} \tag{3}$$

该公式以组内均值为基线、以标准差进行归一化，有效抑制了奖励尺度波动带来的方差。然而，当组内所有回答奖励相同时（如全部答对或全部答错），分子为零，导致**梯度停滞 (gradient stagnation)**，模型无法获得有效学习信号。

### 优先级优势蒸馏 (PAD)

为针对性解决梯度停滞问题并提升样本效率，ReVisual-R1提出了**优先级优势蒸馏 (PAD)** 机制。PAD的核心操作分为两步：

**步骤一：有效集过滤。** 对原始批次 $\mathcal{B}$ 中的每个样本，计算其绝对优势 $\hat{A}_{i,abs}$，仅保留满足阈值条件的样本构成有效集 $\mathcal{E}$：

$$T_{\mathrm{low}} \leq \hat{A}_{i,abs} \leq T_{\mathrm{high}}$$

其中 $T_{\mathrm{low}} > 0$，直接排除了绝对优势为零或极低的无效样本，从根本上消除了梯度停滞的来源。

**步骤二：温度控制的优先采样。** 从有效集 $\mathcal{E}$ 中按以下概率进行不放回采样，形成最终训练批次：

$$\mathrm{Pr}(i \text{ is selected} \mid i \in \mathcal{E}) = \frac{\exp(\hat{A}_i / \tau)}{\sum_{j \in \mathcal{E}} \exp(\hat{A}_j / \tau)} \tag{4}$$

其中 $\tau$ 为温度参数，控制探索与开发的平衡：$\tau$ 较大时采样趋于均匀，$\tau$ 较小时高优势样本被更频繁地选中。通过将训练聚焦于信息量丰富的中等优势样本，PAD显著稳定了训练动态并提升了收敛效率。

### 三阶段训练管线

ReVisual-R1的完整训练管线包含三个顺序模块：

1. **冷启动 (Cold Start)**：仅使用高难度、长推理链的纯文本数据微调基座模型，构建强大的推理引擎。该阶段不涉及任何视觉输入。

2. **多模态强化学习 (MRL)**：在GRAMMAR数据集的多模态部分上，使用配备PAD的GRPO进行训练，将抽象推理能力与视觉感知对齐。此阶段省略KL散度约束以鼓励更广泛的策略探索。

3. **文本强化学习 (TRL)**：在纯文本复杂任务上进一步用GRPO+PAD训练，冻结视觉编码器，恢复并增强语言流畅性和高阶推理能力，从而间接锐化多模态推理表现。

消融实验证实，**CS + MRL + TRL** 的完整序列达到最佳平均性能 (49.6)，显著优于反向顺序 CS+TRL+MRL (45.5) 或混合训练 Mixed-RL (47.6)，验证了“先对齐视觉、再打磨语言”这一分阶段策略的有效性。

## 实验与分析

### 核心实验设置

ReVisual‑R1 的实验管线分为三个阶段：**冷启动 (Cold Start)**、**多模态强化学习 (MRL)** 和 **文本强化学习 (TRL)**。基座模型为 Qwen2.5‑VL‑7B‑Instruct。训练数据来自作者构建的 GRAMMAR 数据集，包含 283K 纯文本冷启动样本、31K 文本 RL 样本和 21K 多模态 RL 样本（Table 1）。评估覆盖 5 个多模态推理基准（MathVerse、MathVision、DynaMath、WeMath、LogicVista）和 4 个文本推理基准（AIME24、AIME25、GPQA、MATH500），统一采用 Pass@1 准确率。

### 主要结果

**Table 2** 汇总了 ReVisual‑R1 与闭源 API 及开源模型的全面对比。核心结论：

![[assets/figures/papers/iclr26_0010_NTo6f6GENJ_Revisual-R1_Advancing_Multimodal_Reasoning_From/figures/005_Table_2.jpg]]
*Table 2: Performance comparison on diverse benchmarks.The best scores are bold;the second best are underlined (among open-source models). Scores in italics indicate that they are not reported in the original work and are obtained using the VLMEvalKit (Duan et al.,2O24)for evaluation.AIME24 and AIME25 results are averaged over eight independent inference runs to reduce score variance.MathVerse-V,DynaMath-W and WeMath-S denotes the vision-only, worst,and strict setings,respectively.△ (e.g., Ours-Open 3B Best) denotes the improvement margin of the corresponding ReVisual-Ri model over the best-performing opensource baseline model in the same scale across the respective column*

- **ReVisual‑R1‑7B 在所有开源 7B 模型中达到最佳平均性能 53.1%，较最佳开源基线（VLAA‑Thinker‑7B 的 36.3%）提升 +16.8 个百分点**（置信度 0.98）。这一优势在多模态和文本基准上均保持一致。
- 在 MATH500 上，ReVisual‑R1‑7B 达到 89.2%，超过 GPT‑4o 的平均分 41.6%（Table 2），表明纯文本数学推理能力已接近闭源强模型水平。
- ReVisual‑R1‑3B 同样在所有基准上超越 VLAA‑Thinker‑3B，平均提升 16.0%，验证了该方法在不同模型规模下的有效性。

**Figure 1** 的柱状图直观展示了这一性能优势：ReVisual‑R1 在 9 个基准中的 8 个上取得开源最优，尤其在 MathVerse 和 MathVision 等多模态数学推理任务上拉开显著差距。

### 分阶段训练消融

**Table 3** 系统消融了不同训练阶段组合的效果（均以冷启动为基础）：

![[assets/figures/papers/iclr26_0010_NTo6f6GENJ_Revisual-R1_Advancing_Multimodal_Reasoning_From/figures/006_Table_3.jpg]]
*Table 3: Ablation study of diferent training stage combinations applied to the ReVisual-R1 model, building upon a Cold Start.Best results per column are bold and second-best are underlined.Mixed-RL denotes that the model is jointly optimized with both MRL and TRL objectives in a mixed training stage*

| 训练组合 | 平均准确率 | 关键发现 |
|---------|-----------|---------|
| 仅冷启动 (CS) | 47.1 | 纯文本冷启动已具备较强推理能力 |
| CS + MRL | 48.1 | 多模态 RL 带来 +1.0 增益 |
| CS + TRL | 47.9 | 文本 RL 带来 +0.8 增益 |
| CS + MRL + TRL (ReVisual‑R1) | **49.6** | 顺序分阶段训练达到最优 |
| CS + TRL + MRL | 45.5 | 反向顺序显著劣化，甚至低于仅冷启动 |
| CS + Mixed‑RL | 47.6 | 混合训练不如分阶段训练 |

**核心因果机制**：先进行多模态 RL（MRL）再进行文本 RL（TRL）的顺序至关重要。MRL 阶段将冷启动构建的抽象推理引擎与视觉感知对齐；TRL 阶段冻结视觉编码器，在纯文本复杂任务上恢复并增强语言流畅性和高阶推理能力。反向顺序（先 TRL 后 MRL）会导致视觉对齐阶段破坏已优化的语言推理结构，平均分降至 45.5，甚至低于仅冷启动的 47.1（置信度 0.98）。混合训练（Mixed‑RL）同时优化两种目标，平均分 47.6，显著低于分阶段训练的 49.6，说明两种 RL 信号直接混合会产生干扰。

### 优先级优势蒸馏（PAD）消融

**Table 4** 消融了 PAD 各组件的贡献（基于 MRL 阶段）：

![[assets/figures/papers/iclr26_0010_NTo6f6GENJ_Revisual-R1_Advancing_Multimodal_Reasoning_From/figures/007_Table_4.jpg]]
*Table 4: Ablation results demonstrating the impact of Prioritized Advantage Distilation (PAD)and its core components.Best results per column are bold and second-best are underlined*

| 方法 | 平均准确率 | 说明 |
|------|-----------|------|
| GRPO‑Baseline | 45.1 | 标准 GRPO，存在梯度停滞 |
| GRPO‑Filter | 46.3 | 仅过滤零优势样本 |
| Random‑Sampling | 46.0 | 过滤后随机采样 |
| DAPO | 46.5 | 现有改进方法 |
| **Full PAD** | **47.7** | 过滤 + 温度控制优先采样 |

**Figure 4** 展示了训练动态：标准 GRPO 在训练中后期出现明显的梯度停滞，奖励曲线趋于平坦；而 Full PAD 持续提供有效学习信号，训练稳定且收敛更快。PAD 的核心机制是两步操作：

![[assets/figures/papers/iclr26_0010_NTo6f6GENJ_Revisual-R1_Advancing_Multimodal_Reasoning_From/figures/008_Figure_4.jpg]]
*Figure 4: Ablation of training dynamics of our PAD*

1. **过滤**：剔除绝对优势 $\hat{A}_{i,abs}$ 不在 $[T_{\mathrm{low}}, T_{\mathrm{high}}]$ 范围内的样本（其中 $T_{\mathrm{low}} > 0$），直接移除零优势样本。
2. **优先采样**：从有效样本集中按温度控制的 Softmax 分布进行采样：
   $$\mathrm{Pr}(i \text{ is selected} \mid i \in \mathcal{E}) = \frac{\exp(\hat{A}_i / \tau)}{\sum_{j \in \mathcal{E}} \exp(\hat{A}_j / \tau)}$$

仅过滤（GRPO‑Filter）比基线提升 1.2 个百分点，但随机采样（Random‑Sampling）仅提升 0.9 个百分点，说明优先采样机制贡献了约 1.4 个百分点的额外增益。

### 通用基准泛化

**Table 6** 和 **Figure 5** 展示了在通用多模态和文本基准（MMMU、MMMU‑PRO、CMMMU、MMStar、MMLU‑Pro）上的性能。ReVisual‑R1‑7B 平均分 60.91，在 7B 模型组中排名第一；ReVisual‑R1‑3B 平均分 53.60，在 3B 组中同样最优。这表明该方法不仅提升数学推理，对通用多模态理解也有正向迁移。

### 失败模式与局限性

1. **理论解释不足**：文本中心的冷启动为何能泛化到多模态推理缺乏深层理论支撑，目前仅停留在经验验证层面。
2. **规模验证有限**：仅在 3B 和 7B 模型上验证，对更大规模架构（如 MoE）的可扩展性未知。
3. **阶段交互未系统研究**：数据类型与训练阶段之间的复杂交互（如 MRL 阶段的数据配比如何影响 TRL 阶段效果）尚未探索。
4. **切换点未自动化**：MRL 到 TRL 的切换时机依赖人工设定，缺乏基于指标的自动决策机制。

> **注意**：上述局限性均来自论文自身声明，其中理论解释不足和规模验证有限两点需要读者在应用该方法时手动评估风险。

### 补充图表

![[assets/figures/papers/iclr26_0010_NTo6f6GENJ_Revisual-R1_Advancing_Multimodal_Reasoning_From/figures/003_Figure_3.jpg]]
*Figure 3: Absolute performance improvement on Qwen2.5-VL-7B-Instruct across textual and multimodal reasoning tasks.The purple and red dashed lines represent the average absolute gains of VisionR1/R1- One-Vision and DeepMath/OpenR1-Math over the baseline,respectively,across four reasoning tasks*

## 方法谱系与知识库定位

### 1. 在现有方法谱系中的位置

ReVisual-R1 的提出直接回应了多模态大语言模型（MLLM）推理能力构建中的两个关键瓶颈：**冷启动数据策略的低效**与**标准 GRPO 在多模态强化学习中的梯度停滞**。

在冷启动环节，现有方法主要分为两条路线：一是以 Vision-R1、R1-One-Vision 为代表的多模态冷启动，直接使用图文配对数据微调；另一是以 DeepMath、OpenR1-Math 为代表的文本冷启动，用高难度纯文本推理数据构建初始能力。ReVisual-R1 的消融实验（Figure 3）明确表明，**文本冷启动的平均绝对增益（红色虚线）显著高于多模态冷启动（紫色虚线）**，这一发现直接支撑了论文“仅用精选文本数据即可使模型在多模态推理上优于许多现有方法”的核心判断。因此，ReVisual-R1 选择了文本冷启动路线，并在此基础上构建了后续的分阶段强化学习框架。

在强化学习环节，ReVisual-R1 直接改进了标准 GRPO。GRPO 的核心机制是通过组内相对优势 $\hat{A}(x,y_i)$ 来提供学习信号：

$$\hat{A}(x,y_i) = \frac{r(x,y_i) - \mathrm{mean}(\{r(x,y_1),\ldots,r(x,y_G)\})}{\mathrm{std}(\{r(x,y_1),\ldots,r(x,y_G)\}) + \epsilon}$$

然而，当组内所有样本的奖励相同时（全对或全错），该优势值为零，导致梯度消失——即论文所指的“梯度停滞”。ReVisual-R1 提出的**优先级优势蒸馏（PAD）**通过两步机制解决此问题：首先过滤掉绝对优势不在 $[T_{\mathrm{low}}, T_{\mathrm{high}}]$ 范围内的零优势样本，然后基于温度控制的 Softmax 分布进行优先采样：

$$\mathrm{Pr}(i \text{ is selected} \mid i \in \mathcal{E}) = \frac{\exp(\hat{A}_i / \tau)}{\sum_{j \in \mathcal{E}} \exp(\hat{A}_j / \tau)}$$

这一机制将训练焦点集中于高信息量样本，与 DAPO 等同样试图改进 GRPO 样本效率的方法形成对比。消融实验（Table 4）显示，完整 PAD 达到 47.7 平均分，而基线 GRPO 仅为 45.1，验证了其有效性。

在分阶段训练策略上，ReVisual-R1 的 **CS + MRL + TRL** 序列（先多模态 RL，再文本 RL）在消融中达到 49.6 平均分，明显优于反向顺序 CS+TRL+MRL（45.5）和混合训练 Mixed-RL（47.6）。这表明多模态 RL 阶段负责将文本冷启动建立的推理引擎与视觉感知对齐，而后续的文本 RL 阶段则修复对齐过程中可能受损的语言流畅性和逻辑一致性——这一“先对齐、后修复”的顺序是性能最优的关键。

在 7B 规模的开源模型中，ReVisual-R1 以 53.1% 的平均准确率显著超越 VLAA-Thinker-7B 和 MM-Eureka-Qwen-7B 等此前 SOTA 模型（+16.8 个百分点），确立了新的基线。

### 2. 适用边界

ReVisual-R1 的有效性已在以下条件下得到验证：

- **模型规模**：仅在 3B 和 7B 参数规模的 Qwen2.5-VL 基座模型上进行了验证。对于更大规模的架构（如 MoE、30B+），该方法能否复现相似的性能跃升仍是开放问题。
- **任务类型**：主要覆盖数学推理（MathVerse、MathVision、AIME 等）、逻辑推理（LogicVista）和部分通用多模态理解基准（MMMU、MMStar 等）。对于更依赖细粒度视觉感知的任务（如医学影像诊断、具身操作），PAD 的样本过滤机制是否会误丢弃视觉上正确但奖励较低的样本，尚缺乏分析。
- **训练数据**：GRAMMAR 数据集由特定来源的文本和多模态推理数据构成（Table 1），冷启动阶段依赖 DeepMath 和 OpenR1-Math 等长推理链文本数据（平均响应长度 8,207.76 tokens）。若替换为其他分布的数据，冷启动效果可能变化。

### 3. 局限与开放问题

论文明确指出的局限包括：

1. **缺乏深层理论解释**：为何文本中心的优化策略能有效泛化到多模态推理，论文未提供理论层面的分析，仅给出了经验证据。
2. **可扩展性未验证**：仅测试了 3B 和 7B 模型，对于更大规模架构的行为未知。
3. **数据与阶段的交互未系统研究**：文本冷启动数据的特性（难度、长度、推理模式）如何具体影响后续 MRL 和 TRL 阶段的行为，尚未被系统性地探索。

此外，从方法设计本身可引申出以下开放问题：

- **PAD 阈值的自适应性**：$T_{\mathrm{low}}$ 和 $T_{\mathrm{high}}$ 以及温度 $\tau$ 的衰减策略目前是固定设置的，能否根据任务难度或训练进程自适应调整，以进一步提升样本效率？
- **阶段切换点的自动化**：CS → MRL → TRL 的切换目前依赖预设的步数或 epoch 数。是否存在可监测的指标（如语言流畅性退化程度、视觉对齐饱和度）来自动决定最优切换时机？
- **跨架构泛化**：该方法在 Qwen2.5-VL 上的成功是否依赖于该模型特定的视觉-语言融合机制？在其他架构（如 LLaVA 系列、InternVL 系列）上的迁移效果需要验证。

> **注意**：关于“PAD 是否会在某些视觉密集任务中误丢弃有效样本”以及“文本冷启动数据的难度阈值如何量化”等具体问题，论文未提供直接证据，需通过额外实验进行手动验证。

## 原文 PDF

![[paperPDFs/ICLR_2026/Revisual_R1_Advancing_Multimodal_Reasoning_From_Optimized_Cold_Start_to_Staged_Reinforcement_Learning.pdf]]
