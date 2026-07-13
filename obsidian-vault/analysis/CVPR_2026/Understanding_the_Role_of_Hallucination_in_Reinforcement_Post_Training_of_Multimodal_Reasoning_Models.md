---
title: Understanding the Role of Hallucination in Reinforcement Post-Training of Multimodal Reasoning Models
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Understanding_the_Role_of_Hallucination_in_Reinforcement_Post_Training_of_Multimodal_Reasoning_Models.pdf
project_link: null
code_link: "https://github.com/hiyouga/EasyR1"
aliases:
- HACF
- URHRPTMRM
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/benchmarks_datasets_evaluation
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 通过控制训练时视觉与文本信息的完整性（如使用空白图像、随机图像替换或移除文本），创造幻觉诱导条件，从而诊断RL训练是否真正依赖视觉信号。
primary_logic: 即使在训练数据视觉信息被严重破坏或完全移除的情况下，RL后训练依然能够提升多模态推理性能，有时甚至超过标准训练，揭示出现有方法主要强化了文本推理，而非教会模型从视觉信息中学习。
claims:
- 在完全幻觉诱导的设置下，RL后训练仍能显著提升模型的推理性能，在某些情况下甚至优于标准训练。
- 对于7B模型，随机图像替换（RI）训练在平均基准上超过了标准GRPO训练（54.23 vs 53.52）。
- 在3B模型上，移除文本信息（TR）训练并未比移除图像（BI/RI）训练带来更明显的性能提升，表明模型尚未有效利用视觉信息。
- Geometry3K (BI corruption) 上 Accuracy = 14.1% (GRPO-BI, 7B)
---

# Understanding the Role of Hallucination in Reinforcement Post-Training of Multimodal Reasoning Models

> [!tip] 核心洞察
> 即使在训练数据视觉信息被严重破坏或完全移除的情况下，RL后训练依然能够提升多模态推理性能，有时甚至超过标准训练，揭示出现有方法主要强化了文本推理，而非教会模型从视觉信息中学习。

| 字段 | 内容 |
|------|------|
| 中文题名 | 理解幻觉在多模态推理模型强化后训练中的作用 |
| 英文题名 | Understanding the Role of Hallucination in Reinforcement Post-Training of Multimodal Reasoning Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.03179) · [Code](https://github.com/hiyouga/EasyR1) |
| Topic | #topic/vision_multimodal_applications #topic/benchmarks_datasets_evaluation #topic/vision_multimodal_applications/image_and_video_generation |
| Method | Hallucination-as-Cue Framework |
| Dataset | Geometry3K, Multi-benchmark average, MathVision |

> [!tip] 效果简介
> - Geometry3K (BI corruption) 上，Accuracy 14.1% (GRPO-BI, 7B) vs 9.7% (Qwen2.5-VL-7B base) (+4.4%)；Accuracy 10.4% (GRPO-BI, 3B) vs 7.6% (Qwen2.5-VL-3B base) (+2.8%)。
> - Multi-benchmark average (MathVision, MathVerse, MathVista, We-Math) 上，AVG 54.23 (GRPO-RI, 7B) vs 53.52 (Standard GRPO, 7B) (+0.71)。
> - MathVision (3B, BI inference) 上，Accuracy BI-corrupted inference accuracy vs normal inference accuracy (positive (higher))。

## 概要

**核心问题**：当前基于强化学习（RL）的多模态推理后训练，究竟是在教会模型“看”并基于视觉信息进行推理，还是主要放大了底层大语言模型（LLM）固有的文本推理能力？

**关键发现**：本研究通过系统性的幻觉诱导实验揭示，**现有的RL多模态后训练方法并未有效利用视觉信息**。即便在训练数据的视觉信息被完全移除或严重破坏的极端条件下，RL后训练依然能够显著提升模型的多模态推理性能，甚至在部分基准上超越使用完整干净数据训练的标准方法。这表明，当前RL训练主要强化了模型的文本推理链，而非教会模型从视觉信号中学习。

**方法定位**：本文提出**Hallucination-as-Cue Framework**（幻觉即线索框架），这是一个分析性框架，而非旨在提升性能的新训练方法。其核心思路是：通过三种模态特定的数据损坏策略——空白图像替换（BI）、随机图像替换（RI）和文本信息移除（TR）——人为创造幻觉诱导条件，然后在这些损坏数据上执行RL后训练，观察模型的行为变化，从而诊断RL训练对视觉信息的真实依赖程度。

**主要结果概览**：
- 在完全移除视觉信息的BI训练下，7B模型在Geometry3K-BI上的准确率从基线的9.7%提升至14.1%（+4.4%），3B模型从7.6%提升至10.4%（+2.8%）。
- 在随机配对错误图像的RI训练下，7B模型在MathVision、MathVerse、MathVista、We-Math四个基准上的平均得分达到54.23，**超过了标准GRPO训练的53.52**。
- 移除文本信息（TR）的训练并未比移除图像（BI/RI）带来更明显的性能优势，进一步印证模型尚未有效利用视觉信息。
- 更大规模的模型（7B vs 3B）从幻觉诱导训练中获益更多，暗示模型规模与文本推理能力放大之间存在关联。

这些反直觉的结果构成了对当前多模态RL后训练范式的根本性质疑，并为理解多模态推理模型的真实能力来源提供了新的分析视角。



### 多模态推理模型的后训练困境

近年来，多模态大语言模型（MLLMs）在视觉问答、数学推理等任务上取得了显著进展。然而，如何通过后训练有效提升其推理能力，仍是一个开放性问题。主流的后训练范式——基于强化学习（RL）的方法，尤其是**GRPO**（Guo et al., arXiv 2025），通过组内归一化奖励来优化策略，无需额外训练奖励模型，已成为多模态推理模型后训练的核心手段。其核心思想是通过最大化优势估计来引导模型生成更高质量的推理轨迹：

$$A _ { i } = \frac { R _ { i } - \mu _ { \mathrm { g r o u p } } } { \sigma _ { \mathrm { g r o u p } } + \epsilon }$$

$$\mathcal { L } _ { \mathrm { G R P O } } ( \theta ) = \mathbb { E } \left[ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \operatorname* { m i n } \left( r _ { i } ( \theta ) A _ { i } , \mathrm { c l i p } \left( r _ { i } ( \theta ) , 1 - \epsilon _ { \mathrm { c l i p } } , 1 + \epsilon _ { \mathrm { c l i p } } \right) A _ { i } \right) \right] - \beta D _ { \mathrm { K L } } \big ( \pi _ { \theta } ( \cdot \mid x ) \big | \big | \pi _ { \mathrm { r e f } } ( \cdot \mid x ) \big )$$

尽管这类方法在多个基准上展现了性能提升，一个根本性问题始终未被充分回答：**RL后训练究竟是在教会模型“看见”并基于视觉信息进行推理，还是仅仅放大了底层语言模型固有的文本推理模式？**

### 核心瓶颈：视觉信息的“伪利用”

现有RL后训练方法存在一个关键瓶颈：**它们未能有效利用视觉信息进行推理，而是主要放大了底层语言模型固有的文本推理能力，导致模型依赖文本先验而非视觉基础**。这一现象在模型行为中表现为：即使视觉输入被破坏或完全移除，经过RL训练的模型仍能给出看似合理的推理过程，甚至得出正确答案。这种“幻觉式推理”揭示了当前方法的一个深层缺陷——模型可能并未真正学会从视觉信号中提取和利用信息，而是通过强化语言模型内部的统计关联来弥补视觉信息的缺失。

### 研究动机：以幻觉为线索的诊断框架

为系统性地诊断上述瓶颈，本文提出**Hallucination-as-Cue Framework**，一个以模型幻觉为分析线索的研究框架。其核心思想是：通过主动创造“幻觉诱导”条件——即在训练过程中系统性地破坏或移除模态信息——来观察RL后训练是否仍能提升模型性能。如果模型在视觉信息完全缺失的情况下依然能通过RL训练获得性能增益，则有力地证明当前方法主要强化的是文本推理能力，而非视觉理解能力。

具体而言，该框架设计了三种模态特异性损坏策略：
- **空白图像替换（BI）**：将训练图像替换为空白图像，完全移除视觉信息；
- **随机图像替换（RI）**：将训练图像替换为数据集中随机选取的图像，制造图文不匹配；
- **文本信息移除（TR）**：通过规则匹配移除所有文本条件和查询，仅保留图像。

这些损坏策略创造了一个极端的实验环境：模型被迫在“幻觉”中学习推理。如果RL后训练在此环境下仍能带来性能提升，则直接证明了当前方法对视觉信息的利用不足。这一框架不仅为理解多模态RL训练的机制提供了新的视角，也为未来设计真正能够利用视觉信号的后训练方法指明了方向。



## 核心方法与创新机理

本工作的核心创新并非提出一种新的性能导向训练算法，而是构建了一个**以幻觉为探针的分析框架（Hallucination-as-Cue Framework）**，用于诊断当前主流的多模态推理模型强化后训练范式在“视觉-语言”对齐上的深层缺陷。该框架通过系统性地破坏训练数据的模态完整性，创造出强制模型依赖幻觉进行推理的极端条件，从而揭示出RL训练的真实作用机制。

### 关键发现：RL后训练主要放大文本推理，而非视觉理解

当前基于GRPO（Guo et al., arXiv 2025）的多模态RL后训练方法，其核心瓶颈在于：**训练过程并未有效地教会模型“看”与“推理”的结合，而是主要放大了底层大语言模型固有的文本推理能力**。这一发现构成了整个工作的核心洞察。

### 方法创新：模态特异性损坏（Modality-Specific Corruptions）

为验证上述瓶颈，论文设计了三种精确的“changed slots”，对标准GRPO训练的数据输入进行受控破坏：

1. **空白图像替换（Blank Image Replacement, BI）**：将训练图像全部替换为空白图像，彻底移除视觉信息。模型被迫在无任何视觉线索的情况下，仅凭文本上下文进行推理。

2. **随机图像替换（Random Image Replacement, RI）**：将每张训练图像替换为数据集中随机选取的另一张图像，创造出图文不匹配的幻觉条件。模型面对的是错误的视觉信号，但文本信息保持完整。

3. **文本信息移除（Textual Information Removal, TR）**：通过基于规则的匹配，移除所有文本条件和查询，仅保留图像。模型被迫仅从视觉信号中推理，失去了语言模型的文本先验支撑。

这三种损坏策略构成了框架的“因果旋钮”（causal knob）：通过控制视觉与文本信息的完整性，可以精确观测RL训练在何种信息条件下产生性能增益，从而推断其真正的学习来源。

### 反直觉证据：幻觉条件下的训练增益

实验揭示了极具颠覆性的现象（详见Table 1）：

- **在7B模型上，随机图像替换训练（GRPO-RI）的平均基准得分达到54.23，超越了在干净数据上训练的标准GRPO（53.52）**。这意味着，给模型喂入错误的图像，反而比给正确图像训练效果更好。

- **在完全移除视觉信息的BI设置下，RL后训练仍能显著提升推理性能**：7B模型在Geometry3K-BI上从基线的9.7%提升至14.1%（+4.4%），3B模型从7.6%提升至10.4%（+2.8%）。

- **移除文本信息（TR）的训练并未比移除图像（BI/RI）的训练表现出更明显的优势**，这表明模型在训练过程中尚未有效利用视觉信息进行推理。

这些证据共同指向一个结论：**当前RL后训练的性能增益，主要来源于语言模型内部推理模式的强化，而非多模态视觉基础的建立**。模型在训练中学会的是“如何更好地利用文本线索进行推理”，而非“如何从图像中提取关键信息进行推理”。这一发现对当前多模态RL训练范式的有效性提出了根本性质疑，也为未来如何设计真正视觉-语言对齐的强化学习算法指明了方向。



本文提出 **Hallucination-as-Cue Framework**，一个以模型幻觉为“探针”的分析框架，旨在系统诊断基于强化学习的多模态推理后训练是否真正利用了视觉信息。该框架不提出新的训练算法，而是通过受控破坏训练数据中的模态信息来诱导幻觉，从而揭示RL训练的真实驱动力。

### 框架动机与核心假设

当前主流的RL后训练范式（如GRPO）在多模态推理任务上展现了显著的性能提升，但其提升的根源尚不明确：模型究竟是从视觉信息中学会了“看与推理”，还是仅仅放大了底层语言模型固有的文本推理能力？Hallucination-as-Cue Framework正是为回答这一问题而设计——如果RL训练确实依赖视觉信号，那么当视觉信息被系统性破坏时，性能应当崩溃；反之，如果性能仍然提升，则说明训练主要强化了文本推理。

### 三大模块与数据流

框架由三个顺序模块构成，其整体流程如 **Figure 2** 所示：

![[assets/figures/papers/paper_list_l797_https_arxiv_org_abs_2604_03179/figures/002_Figure_2.jpg]]
*Figure 2: Hallucination-as-Cue Framework. (a) Modality-Specific Corruptions: We define three types of data corruptions: Blank Image Replacement, Random Image Replacement, and Textual Information Removal. (b) Hallucination-Inductive Training: We apply these types of modality-specific corruptions to the training data to obtain three models. Since the input information is corrupted, the model learns to hallucinate the corrupted information for inference. We refer to this process as hallucination-inductive training. (c) Hallucination-Inductive Inference and Analysis: We then analyze these three models under the three types of data corruptions to compare task accuracy and examine model behavior*

**模块一：模态特定损坏（Modality-Specific Corruptions）**  
在训练数据上施加三种互补的损坏策略，分别破坏视觉或文本信息：
- **空白图像替换（Blank Image Replacement, BI）**：将所有训练图像替换为空白图像，完全移除视觉信息。
- **随机图像替换（Random Image Replacement, RI）**：将每张训练图像替换为数据集中随机选取的另一张图像，制造图文不匹配的幻觉条件。
- **文本信息移除（Textual Information Removal, TR）**：通过规则匹配移除所有文本条件和查询，仅保留图像。

这三种损坏策略构成了一个“幻觉诱导梯度”：BI和RI主要破坏视觉模态，TR破坏文本模态，从而可以分别观察各模态对RL训练的贡献。

**模块二：幻觉诱导训练（Hallucination-Inductive Training）**  
在损坏后的数据上执行标准的GRPO后训练。由于输入信息被破坏，模型被迫在幻觉中推理——即“脑补”缺失的信息来完成推理任务。这一模块的输入是损坏数据，输出是三个分别对应BI、RI、TR训练条件的模型。

**模块三：幻觉诱导推理与分析（Hallucination-Inductive Inference and Analysis）**  
在正常测试集和损坏测试集上评估上述三个模型的行为，通过对比任务准确率和推理轨迹，分析不同训练策略的影响。这一模块的关键输出是：RL训练在多大程度上依赖视觉信息，以及不同损坏条件下的性能变化模式。

### 与标准GRPO的关系

框架本身不修改GRPO的核心机制。GRPO通过组内归一化计算优势函数：

$$A _ { i } = \frac { R _ { i } - \mu _ { \mathrm { g r o u p } } } { \sigma _ { \mathrm { g r o u p } } + \epsilon }$$

并优化带裁剪比率和KL散度惩罚的目标函数：

$$\mathcal { L } _ { \mathrm { G R P O } } ( \theta ) = \mathbb { E } \left[ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \operatorname* { m i n } \left( r _ { i } ( \theta ) A _ { i } , \mathrm { c l i p } \left( r _ { i } ( \theta ) , 1 - \epsilon _ { \mathrm { c l i p } } , 1 + \epsilon _ { \mathrm { c l i p } } \right) A _ { i } \right) \right] - \beta D _ { \mathrm { K L } } \big ( \pi _ { \theta } ( \cdot \mid x ) \big | \big | \pi _ { \mathrm { r e f } } ( \cdot \mid x ) \big )$$

框架的创新在于**输入端**的系统性损坏，而非优化过程本身。这使得框架可以作为“诊断层”插入任何基于RL的多模态后训练流程中。

### 关键发现预览

该框架揭示了两个核心发现：
1. **即使在完全幻觉诱导的设置下（BI、RI），RL后训练仍能显著提升模型的推理性能**，在某些情况下（如7B模型的RI训练）甚至超越标准GRPO训练（54.23 vs 53.52平均分）。
2. **移除文本信息（TR）的训练并未比移除视觉信息（BI/RI）的训练表现出明显优势**，这表明当前的RL多模态推理训练尚未有效利用视觉信息，而是主要强化了语言模型内部的文本推理模式。



### 基础RL优化器：GRPO

本文采用**GRPO**（Group Relative Policy Optimization, Guo et al., arXiv 2025）作为统一的RL后训练优化器，所有实验均基于EasyR1框架[43]实现。GRPO的核心思想是在每组采样的补全结果内部进行奖励归一化，从而消除训练独立奖励模型的需求。

**组归一化优势估计**：对于一组大小为 $G$ 的采样补全，每个样本的优势 $A_i$ 由其奖励 $R_i$ 减去组内均值 $\mu_{\mathrm{group}}$ 后，除以组内标准差 $\sigma_{\mathrm{group}}$ 得到：

$$A_{i} = \frac{R_{i} - \mu_{\mathrm{group}}}{\sigma_{\mathrm{group}} + \epsilon}$$

其中 $\epsilon$ 为防止除零的数值稳定项。

**GRPO优化目标**：在PPO风格的裁剪代理目标基础上，引入组相对优势和KL散度惩罚项：

$$\mathcal{L}_{\mathrm{GRPO}}(\theta) = \mathbb{E}\left[\frac{1}{G}\sum_{i=1}^{G}\min\left(r_i(\theta)A_i,\ \mathrm{clip}\left(r_i(\theta), 1-\epsilon_{\mathrm{clip}}, 1+\epsilon_{\mathrm{clip}}\right)A_i\right)\right] - \beta D_{\mathrm{KL}}\big(\pi_{\theta}(\cdot\mid x)\big|\big|\pi_{\mathrm{ref}}(\cdot\mid x)\big)$$

其中 $r_i(\theta) = \frac{\pi_{\theta}(y_i|x)}{\pi_{\mathrm{old}}(y_i|x)}$ 为概率比率，$\epsilon_{\mathrm{clip}}$ 控制裁剪范围，$\beta$ 为KL惩罚系数，$\pi_{\mathrm{ref}}$ 为参考策略。

**多模态扩展**：对于MLLM，策略条件从纯文本 $\pi_{\theta}(y_i|\boldsymbol{x})$ 扩展为同时包含文本和视觉token：$\pi_{\theta}(y_i|\boldsymbol{x}_t, \boldsymbol{x}_v)$，使得GRPO可以直接作用于多模态输入。

---

### 核心框架：Hallucination-as-Cue Framework

框架由三个模块化阶段构成（图2），通过主动破坏模态信息来诊断RL训练对视觉信号的依赖程度。

#### 模块一：模态特定损坏（Modality-Specific Corruptions）

该模块定义了三种数据损坏策略，分别移除或替换回答正确问题所必需的信息，从而**强制模型在幻觉中推理**：

- **空白图像替换（BI, Blank Image Replacement）**：将所有训练图像替换为空白图像，完全移除视觉信息。
- **随机图像替换（RI, Random Image Replacement）**：每张训练图像被替换为数据集中随机选取的另一张图像，制造图文不匹配对。
- **文本信息移除（TR, Textual Information Removal）**：通过基于规则的匹配，移除所有文本条件和文本查询。

#### 模块二：幻觉诱导训练（Hallucination-Inductive Training）

在损坏后的数据上分别执行GRPO后训练，得到三个对应模型（GRPO-BI、GRPO-RI、GRPO-TR）。由于输入信息已被破坏，模型被迫学习“幻觉化”被破坏的信息以完成推理——这一过程被称为**幻觉诱导训练**。

#### 模块三：幻觉诱导推理与分析（Hallucination-Inductive Inference and Analysis）

在三种损坏类型的测试数据上评估上述三个模型的行为，比较任务准确率并分析模型行为模式，从而揭示RL训练是否真正利用了视觉信息进行推理。

---

### 关键公式变量说明

| 符号 | 含义 |
|------|------|
| $G$ | 每组采样的补全数量 |
| $R_i$ | 第 $i$ 个补全的奖励值 |
| $\mu_{\mathrm{group}}$ | 组内奖励均值 |
| $\sigma_{\mathrm{group}}$ | 组内奖励标准差 |
| $\epsilon$ | 数值稳定常数 |
| $r_i(\theta)$ | 当前策略与旧策略的概率比率 |
| $\epsilon_{\mathrm{clip}}$ | PPO裁剪阈值 |
| $\beta$ | KL散度惩罚系数 |
| $\pi_{\theta}$ | 当前策略 |
| $\pi_{\mathrm{ref}}$ | 参考策略（冻结） |
| $\boldsymbol{x}_t, \boldsymbol{x}_v$ | 文本token和视觉token |

> **注意**：上述公式均来自论文第3节Preliminaries部分，为GRPO标准定义的直接引用。Hallucination-as-Cue框架本身不引入新的数学公式，其贡献在于实验设计方法论。

### 补充图表

![[assets/figures/papers/paper_list_l797_https_arxiv_org_abs_2604_03179/figures/001_Figure_1.jpg]]
*Figure 1: Case Study. An example illustrating different hallucination behaviors in multimodal reasoning models. The left side shows the model reasoning with normal visual inputs; in this case, the reinforcement-trained model (bottom-left) produces a noisier reasoning trajectory and ultimately yields an incorrect answer. In contrast, the right side demonstrates that when visual information is removed, the reinforcement-trained model focuses directly on the question itself. With only contextual cues, the model arrives at a correct prediction. Hallucinated contents are marked in red*



## 实验与关键发现

### 核心发现：RL后训练主要放大文本推理能力，而非视觉基础

本文通过系统性的幻觉诱导实验揭示了一个关键瓶颈：当前基于RL的多模态后训练方法并未有效利用视觉信息进行推理，而是主要放大了底层语言模型固有的文本推理能力。这一发现通过三个核心证据链得到支撑。

**证据一：完全幻觉诱导设置下RL训练依然有效。** 即使在训练数据的视觉信息被严重破坏或完全移除的情况下，RL后训练仍能显著提升模型的推理性能，有时甚至超过标准训练。例如，在Geometry3K基准上，Qwen2.5-VL-7B基础模型在空白图像（BI）条件下的准确率仅为9.7%，而经过BI损坏训练的GRPO-BI模型达到14.1%，提升了4.4个百分点。3B模型同样从7.6%提升至10.4%。

**证据二：随机图像替换训练超越标准GRPO。** 对于7B模型，使用随机图像替换（RI）进行训练的GRPO-RI在多个基准（MathVision、MathVerse、MathVista、We-Math）上的平均得分达到54.23，超过了标准GRPO的53.52。这一反直觉的结果表明，即使训练时图像与文本完全不匹配，模型仍能学到有效的推理能力，进一步证实了文本推理路径的主导地位。

**证据三：移除文本信息并未比移除视觉信息带来更明显的性能提升。** 在3B模型上，移除文本条件（TR）的训练并未比移除图像（BI/RI）训练表现出更明显的优势。这揭示了一个关键事实：模型尚未有效利用视觉信息进行推理，训练收益主要来自文本模态的强化。

### 多基准性能对比

Table 1展示了不同训练方式在Qwen2.5-VL基线上的全面对比。对于3B模型，标准GRPO以44.74的平均分取得最佳表现，而BI和RI训练分别获得43.80和43.32，略低于标准训练但仍显著优于基础模型的40.72。对于7B模型，GRPO-RI以54.23的平均分领先，GRPO-BI获得53.16，均接近或超过标准GRPO的53.52，远高于基础模型的50.50。

Table 2分析了不同后训练数据集（Geometry3K、MMR1-V0、CLEVR）的影响，表明幻觉诱导训练在不同数据分布上均能带来一致的性能提升，验证了该现象的普遍性。

Table 3展示了在评估数据上施加BI损坏后各模型的性能变化。值得注意的是，在MathVision基准上，Qwen2.5-VL-3B在BI损坏推理下的准确率甚至高于正常推理，进一步说明模型在视觉信息缺失时能够更专注于文本推理路径。

### 细粒度分析：文本主导 vs 视觉主导问题

Table 4通过MathVerse基准对问题类型进行了细粒度区分。结果显示，BI训练对文本主导问题的性能影响较小，而对视觉主导问题的影响更为显著。这一差异进一步证实了RL后训练主要强化了文本推理能力，而非教会模型从视觉信息中提取关键线索。

### 训练动态分析

Figure 3和Figure 4分别展示了正常和损坏训练/测试集上的准确率曲线。在正常数据上，BI训练在早期阶段即能提升训练和测试准确率，而RI训练的准确率在若干步后大幅增长。在损坏数据上，幻觉诱导训练并未展现出对标准GRPO的明显优势，说明模型在损坏数据上学到的能力具有通用性，而非对幻觉内容的过拟合。

### 规模效应

对比3B和7B模型的实验结果揭示了显著的规模效应。7B模型从幻觉诱导训练中获益更多，GRPO-RI甚至超越了标准GRPO，而3B模型上这一现象并未出现。这表明更大规模的语言模型拥有更强的文本推理先验，在视觉信息缺失时能够更有效地利用这些先验进行补偿性推理。

### 局限性与开放问题

尽管实验证据充分，本文对观察到的行为背后的机制仅进行了初步分析。其根本原因复杂且多面，需要进一步深入研究。关键开放问题包括：RL训练在多大程度上真正利用了视觉信息进行推理？为何TR训练未表现出明显优势？为何幻觉诱导训练未导致过拟合？以及更大模型如何从幻觉推理中获益的具体机制是什么？

### 补充图表

![[assets/figures/papers/paper_list_l797_https_arxiv_org_abs_2604_03179/figures/005_Table_1.jpg]]
*Table 1: Benchmark results comparing different training regimes with Qwen2.5-VL [2] baselines. All RL-based training is performed on the Geometry3K [21] dataset. For the 3B model, standard GRPO yields the best average performance. Strikingly, for the 7B model, hallucination-inductive training (GRPO-RI) achieves the highest average score, even outperforming standard GRPO trained on clean data*

![[assets/figures/papers/paper_list_l797_https_arxiv_org_abs_2604_03179/figures/006_Table_2.jpg]]
*Table 2: Benchmark results analyzing the effect of different post-training datasets. We compare the performance of the base Qwen2.5-VL model, the standard GRPO-trained model, and the BI-corrupted GRPO-trained model across three post-training datasets: Geometry3K [21], MMR1-V0 [14], and CLEVR [11]*

![[assets/figures/papers/paper_list_l797_https_arxiv_org_abs_2604_03179/figures/007_Table_3.jpg]]
*Table 3: Benchmark results of different models with BI corruption applied to the evaluation data. Performance differences relative to normal inference are indicated in the table*

![[assets/figures/papers/paper_list_l797_https_arxiv_org_abs_2604_03179/figures/008_Table_4.jpg]]
*Table 4: Fine-grained analysis of different visual reasoning problem types using the MathVerse [41] benchmark. BI corruption is applied as the study case for inference corruption*

![[assets/figures/papers/paper_list_l797_https_arxiv_org_abs_2604_03179/figures/003_Figure_3.jpg]]
*Figure 3: Accuracy of different training regimes on the normal training and test sets*

![[assets/figures/papers/paper_list_l797_https_arxiv_org_abs_2604_03179/figures/004_Figure_4.jpg]]
*Figure 4: Accuracy of different training regimes on corrupted training and test sets*



## 定位与知识库关联

### 与现有RL后训练范式的关系

本工作并非提出一种新的强化学习算法，而是构建了一个名为 **Hallucination-as-Cue Framework** 的分析框架，用于诊断当前主流的基于RL的多模态推理后训练方法。其核心被诊断对象是 **GRPO**（Group Relative Policy Optimization, Guo et al., arXiv 2025），这是当前多模态推理模型后训练中最广泛采用的强化学习范式。

GRPO的核心机制在于通过组内奖励归一化来估计优势函数，并优化一个带有裁剪比率和KL散度惩罚的PPO风格目标。具体而言，对于一组采样完成结果，其优势估计为：

$$A _ { i } = \frac { R _ { i } - \mu _ { \mathrm { g r o u p } } } { \sigma _ { \mathrm { g r o u p } } + \epsilon }$$

GRPO的优化目标为：

$$\mathcal { L } _ { \mathrm { G R P O } } ( \theta ) = \mathbb { E } \left[ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \operatorname* { m i n } \left( r _ { i } ( \theta ) A _ { i } , \mathrm { c l i p } \left( r _ { i } ( \theta ) , 1 - \epsilon _ { \mathrm { c l i p } } , 1 + \epsilon _ { \mathrm { c l i p } } \right) A _ { i } \right) \right] - \beta D _ { \mathrm { K L } } \big ( \pi _ { \theta } ( \cdot \mid x ) \big | \big | \pi _ { \mathrm { r e f } } ( \cdot \mid x ) \big )$$

本工作将GRPO的策略扩展至多模态场景，即从 $\pi _ { \boldsymbol { \theta } } ( y _ { i } | \boldsymbol { x } )$ 扩展为 $\pi _ { \boldsymbol { \theta } } ( y _ { i } | \boldsymbol { x } _ { t } , \boldsymbol { x } _ { v } )$，使其同时接收文本token和视觉token作为输入。实验实现基于 **EasyR1** 训练框架（Zheng et al., 2025）。

与标准GRPO后训练相比，本框架的关键区别在于**训练数据的构造方式**：通过在训练阶段系统性地破坏模态信息（空白图像替换BI、随机图像替换RI、文本信息移除TR），创造“幻觉诱导”条件，从而揭示RL训练是否真正依赖视觉信号进行推理。

### 与基线模型的关系

所有实验均以 **Qwen2.5-VL**（Bai et al., arXiv 2025）作为基础多模态模型，在3B和7B两个规模上进行对比。基线设置包括：
- **Qwen2.5-VL base**：未经任何RL后训练的原始模型，作为能力下界。
- **Standard GRPO**：在完整、未损坏的Geometry3K数据集上执行标准GRPO后训练，作为常规RL训练的性能参照。

### 适用边界与条件

本框架的适用性受以下条件约束：

1. **训练范式限定**：当前分析聚焦于基于GRPO的RL后训练范式。对于其他推理范式（如潜在空间推理），本框架的诊断结论是否成立尚需验证，这被作者明确列为未来工作方向。

2. **模型规模依赖**：幻觉诱导训练的效果表现出显著的规模依赖性。在7B模型上，GRPO-RI（随机图像替换训练）的平均基准得分（54.23）超越了标准GRPO（53.52）；而在3B模型上，标准GRPO（44.74）仍保持最优。这表明**更大模型从幻觉轨迹中获益更多**，但该现象的规模阈值和上限尚未被充分探索。

3. **数据集影响**：虽然消融实验表明幻觉诱导训练在Geometry3K、MMR1-V0、CLEVR三个不同数据集上均能带来性能提升，但所有实验均限于数学推理和视觉推理领域，向其他多模态任务（如视觉问答、图像描述）的泛化性有待验证。

4. **损坏类型的局限**：TR（文本移除）训练并未比BI和RI训练表现出更明显的优势，即使TR保留了更多“正常”样本。这一反直觉现象表明，当前框架对文本模态损坏的诊断能力可能受限于底层语言模型对文本信息的强依赖。

### 已识别的局限

1. **机制解释的初步性**：作者明确指出，对所观察到的行为（幻觉诱导训练反而提升性能）背后的机制仅进行了初步分析，其根本原因“复杂且多面，需要进一步深入研究”。目前尚无法从因果层面解释为何在完全破坏视觉信息的情况下，RL训练仍能提升多模态推理性能。

2. **核心瓶颈的证实而非解决**：本工作揭示了“当前RL多模态后训练主要放大底层语言模型的文本推理能力，而非教会模型利用视觉信息”这一瓶颈，但并未提出解决方案。如何设计真正依赖视觉信号的RL训练策略，仍是开放问题。

3. **评估指标的单一性**：实验主要依赖准确率（Accuracy）和平均得分（AVG）作为评估指标，缺乏对推理过程质量、幻觉内容比例、视觉信息利用程度等维度的定量分析。

### 开放性研究问题

1. **视觉信息利用的度量**：RL训练在多大程度上真正利用了视觉信息进行推理，而不是仅增强语言模型的内部推理模式？如何设计更精确的度量指标来区分这两种效应？

2. **TR训练的反常行为**：为何移除文本信息（TR）的训练并未比移除图像信息（BI/RI）的训练表现出更明显的优势？这是否意味着当前多模态模型在RL训练中对视觉信号的依赖远低于预期？

3. **泛化能力的来源**：为何幻觉诱导训练并未在训练过程中过度拟合幻觉内容，反而学到了可迁移到正常测试数据的通用推理能力？这一“有益幻觉”现象的理论基础是什么？

4. **规模效应的机制**：为何随机图像替换（RI）训练在7B模型上超越了标准GRPO，而在3B模型上并未发生？更大模型如何从幻觉诱导的推理中获益，其具体的推理能力放大机制是什么？

5. **训练范式的扩展**：本框架的发现是否适用于其他RL算法（如PPO、DPO）或其他后训练策略（如SFT）？如果底层机制是语言模型推理能力的放大，那么这一效应是否在纯文本RL训练中同样存在？



## 原文 PDF

![[paperPDFs/CVPR_2026/Understanding_the_Role_of_Hallucination_in_Reinforcement_Post_Training_of_Multimodal_Reasoning_Models.pdf]]
