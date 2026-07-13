---
title: "Agentic Jigsaw Interaction Learning for Enhancing Visual Perception and Reasoning in Vision-Language Models"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Agentic_Jigsaw_Interaction_Learning_for_Enhancing_Visual_Perception_and_Reasoning_in_Vision_Language_Models.pdf
project_link: null
code_link: https://github.com/yuzeng0-0/AGILE
openreview_forum_id: 3kouij8BWi
aliases:
- AJILEVPRVLM
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将拼图求解建模为逐步代码交互过程，利用可编程合成数据提供可验证的密集训练信号，通过强化学习驱动模型在探索与反馈中迭代增强感知和推理能力。"
primary_logic: "以拼图交互作为代理任务，利用其可控难度与可验证性，为VLMs提供需要细粒度视觉辨别与空间关系推理的结构化训练信号，从而实现感知机制的底层强化，并泛化至一般视觉理解任务。"
claims:
- "即使是简单的2×2拼图任务，现有VLM准确率仅为9.5%，接近随机水平，表明基础感知推理能力缺失。"
- "AGILE通过交互式RL将2×2拼图平均准确率从9.5%提升至82.8%，Score从29.4%提升至89.0%，证明交互式训练极大增强了拼图求解能力。"
- "AGILE训练后模型在9个通用视觉基准上平均性能提升3.1%（HRBench4K +4.2%、HRBench8K +5.2%、VStarBench +4.2%），验证了感知推理能力的有效泛化。"
- "去除Crop/Zoom动作后下游任务平均性能从63.9%降至63.5%，表明细粒度交互（局部放大、裁剪观察）对于获得鲁棒感知推理至关重要。"
---

# Agentic Jigsaw Interaction Learning for Enhancing Visual Perception and Reasoning in Vision-Language Models

> [!tip] 核心洞察
> 以拼图交互作为代理任务，利用其可控难度与可验证性，为VLMs提供需要细粒度视觉辨别与空间关系推理的结构化训练信号，从而实现感知机制的底层强化，并泛化至一般视觉理解任务。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | AGILE：交互式拼图学习增强视觉感知与推理 |
| 英文题名 | Agentic Jigsaw Interaction Learning for Enhancing Visual Perception and Reasoning in Vision-Language Models |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=3kouij8BWi) · [GitHub](https://github.com/yuzeng0-0/AGILE) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | AGILE |
| Dataset | 2×2 Jigsaw, 3×3 Jigsaw, HRBench4K, HRBench8K |

> [!tip] 效果简介
> - 2×2 Jigsaw 上，Accuracy (%) 为 82.8，对比 9.5 (Cold-Start SFT)，变化 +73.3。
> - 3×3 Jigsaw 上，Accuracy (%) 为 20.8，对比 0.4 (Cold-Start SFT)，变化 +20.4。
> - HRBench4K 上，Accuracy (%) 为 73.0，对比 68.8 (Qwen2.5-VL-7B)，变化 +4.2。

## 概要

现有大视觉-语言模型（VLMs）在需要全面视觉理解和结构化推理的任务上表现近乎随机——即便是最简单的2×2拼图任务，Qwen2.5-VL-7B的准确率也仅为9.5%，接近随机猜测水平。这一瓶颈的根源在于高质量多模态强化学习（RL）数据稀缺且难以扩展，导致模型缺乏细粒度视觉辨别与空间关系推理的底层能力。

AGILE将拼图求解建模为逐步代码交互过程：模型在每个步骤生成Python代码调用预定义的Swap、Observe、Crop、Zoom动作，环境返回细粒度视觉反馈，形成多轮观察-行动循环。这一设计利用可编程合成数据提供可验证的密集训练信号，通过组相对策略优化（GRPO）驱动模型在探索与反馈中迭代增强感知和推理能力。其核心洞察在于：拼图交互作为代理任务，具备可控难度与可验证性，能够为VLM提供结构化训练信号，实现感知机制的底层强化，并泛化至一般视觉理解任务。

实验结果表明，AGILE将2×2拼图平均准确率从9.5%提升至82.8%，Score从29.4%提升至89.0%。更重要的是，训练后模型在9个通用视觉基准上平均性能提升3.1%，其中HRBench4K提升4.2%、HRBench8K提升5.2%、VStarBench提升4.2%，验证了感知推理能力的有效泛化。消融实验进一步确认，去除Crop/Zoom操作后下游任务平均性能从63.9%降至63.5%，表明细粒度局部观察行为对获得鲁棒感知推理至关重要。



### 大视觉-语言模型的感知推理瓶颈

大视觉-语言模型（VLMs）在图像描述、视觉问答等任务上取得了显著进展，然而当任务需要**全面的视觉理解**和**结构化的空间推理**时，现有模型的表现却大幅退化。一个令人警醒的发现是：即便是简单的2×2拼图任务，当前先进VLM的准确率仅为9.5%，几乎等同于随机猜测水平（Table 1, Qwen2.5VL-7B Cold-Start）。这一结果揭示了一个深层问题——现有VLM虽然能够识别物体和场景，但在需要细粒度视觉辨别、空间关系建模和多步推理整合的任务上，其底层感知机制存在根本性缺失。

这一瓶颈并非偶然。当前VLM的训练范式主要依赖大规模图文对进行预训练，再通过人工标注或闭源模型生成的视觉问答数据进行监督微调。这种范式存在两个结构性缺陷：

1. **训练信号粗糙**：传统的视觉问答数据通常只提供“图像-问题-答案”三元组，缺乏中间推理步骤的密集反馈。模型仅从最终答案的正确性中学习，无法获得关于“如何观察”、“从何处观察”、“如何逐步推理”的过程性指导。

2. **高质量多模态RL数据稀缺**：强化学习（RL）在语言模型的后训练中已展现出强大的推理能力提升效果，但将其迁移到视觉-语言领域面临根本性困难——需要大量可验证、可交互的多模态训练样本，而这类数据的获取和标注成本极高，难以规模化扩展。

### 现有方法的局限

现有尝试提升VLM感知推理能力的方法大致可分为两类，但各自存在明显局限：

- **基于监督微调的方法**（如Qwen2.5-VL、InternVL系列）：依赖大规模人工标注或模型蒸馏数据，但数据质量受限于标注者的专业水平或教师模型的能力上限，且无法提供交互式反馈。在需要多步空间推理的任务中，这类方法难以教会模型“主动观察”和“逐步验证”。

- **基于RL的VLM训练方法**（如MiMo-VL-7B-RL）：尝试将语言模型的RL后训练范式引入视觉领域，但受限于可验证奖励信号的设计困难。现有工作多依赖最终答案的正确性作为奖励，无法为中间推理步骤提供细粒度指导，导致训练效率低下。

### 核心动机：以拼图交互作为代理任务

AGILE的核心动机源于一个关键洞察：**拼图求解天然是一个需要细粒度视觉辨别、空间关系推理和多步决策的代理任务，且其难度可控、答案可自动验证**。如果将拼图求解建模为模型与环境的逐步交互过程——模型生成代码执行观察或操作动作，环境返回视觉反馈——那么这一过程恰好能为VLM提供密集的、结构化的训练信号。

具体而言，拼图交互学习具有以下独特优势：

- **可编程合成**：拼图数据可通过从高分辨率、OCR、真实场景等多源图像中分割网格并随机打乱来自动生成，无需人工标注，理论上可无限扩展（Section 3.2）。
- **难度可控**：通过调整网格尺寸（2×2、3×3）和初始打乱程度（L0至L6难度等级），可以系统性地控制任务复杂度，实现课程学习。
- **密集可验证反馈**：每一步操作（交换、裁剪观察、缩放）后环境都会返回新的视觉状态，最终拼图是否完全正确可自动判定，这为RL提供了逐步骤的丰富训练信号。
- **感知机制的底层强化**：为了正确求解拼图，模型必须学会辨别拼图块边缘的纹理、颜色、形状等细粒度视觉线索，并推理它们之间的空间邻接关系。这种底层感知能力的强化有望泛化至更广泛的视觉理解任务。

正是基于上述动机，AGILE将拼图求解重新定义为**逐步代码交互过程**：模型在每一步生成Python代码调用预定义API（Swap、Observe、Crop、Zoom），环境执行代码并返回更新后的视觉观察。通过冷启动监督微调使模型掌握基本交互能力，再通过组相对策略优化（GRPO）驱动模型在探索与反馈中迭代增强感知与推理效率。最终目标不仅是让模型学会解拼图，更是通过这一结构化交互训练，从底层强化VLM的视觉感知机制，使其在一般视觉理解任务上获得可泛化的性能提升。



## 核心方法与创新机理

AGILE的核心创新在于将**拼图求解**建模为一个**逐步代码交互的代理任务**，并通过**可编程合成数据**与**强化学习**的协同，从根本上改变了视觉-语言模型（VLM）感知与推理能力的获取方式。相较于现有VLM依赖静态多模态QA数据或单轮推理的范式，AGILE在四个关键维度上实现了系统性突破。

### 1. 训练范式：从静态推理到多轮交互式强化学习

现有VLM通常采用监督微调（SFT）或直接推理，模型仅基于单次输入产生输出，缺乏与外部环境的动态交互。AGILE引入**冷启动SFT + 多轮交互式强化学习（GRPO）**的双阶段范式。模型在每一步基于当前拼图状态生成Python代码，调用预定义的Swap、Observe、Crop、Zoom等API，环境执行代码后返回细粒度的视觉反馈（更新后的拼图图像或局部放大视图），形成**观察-行动-反馈**的闭环。这一范式使模型能够在主动探索中迭代优化感知策略，而非被动拟合静态答案。

### 2. 训练数据：从人工标注到可编程无限扩展

高质量多模态RL数据的稀缺是制约VLM发展的核心瓶颈。AGILE通过**可编程规则合成拼图数据**，从根本上解决了这一问题。从高分辨率、OCR、真实场景等多源图像中自动分割为m×m网格并随机打乱，即可生成大规模、难度可控（通过初始正确块数L0–L7调节）的训练样本。消融实验表明，增加拼图RL数据量可显著提升拼图准确率和下游任务表现（Figure 3），且在同等20K样本预算下，拼图数据训练效果优于通用QA数据（Figure 4），验证了可编程合成数据的独特训练价值。

### 3. 环境交互机制：从无交互到代码驱动的细粒度感知

AGILE定义了一套**Python API驱动的动作空间**，使模型能够执行传统VLM无法实现的细粒度视觉操作：**Swap**交换拼图块并观察更新状态；**Observe**获取当前完整拼图视图；**Crop**裁剪特定区域进行近距离检查；**Zoom**放大选定区域以辨别细节纹理。消融实验揭示，去除Crop/Zoom操作后下游任务平均性能从63.9%降至63.5%（Table 8），表明局部放大与裁剪观察行为对于获得鲁棒的感知推理能力至关重要。这一机制使模型从“整体看图”进化为“主动观察”。

### 4. 奖励函数：从单一正确性到复合效率导向

传统VLM训练仅依赖最终答案正确性作为奖励信号。AGILE设计了**组合准确性、格式和步数惩罚的复合奖励函数**：

$$R = \alpha \cdot R_{\mathrm{acc}} + \beta \cdot R_{\mathrm{format}} + \gamma \cdot R_{\mathrm{step}}$$

其中步数奖励 $R_{\mathrm{step}}$ 在正确完成时按实际步数惩罚（$\lambda=-0.05$），错误时赋予最大步数惩罚，鼓励模型用最少有效步骤完成拼图。消融实验证实，移除步数奖励（$\gamma=0$）会导致VStarBench和MMVP性能明显下降（Table 6），验证了效率导向奖励对于培养高效交互策略的必要性。



![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/002_Figure_2.jpg]]
*Figure 2: Overview of the AGILE framework. (a) depicts the interaction process between the model and the external environment, together with the implementation of the GRPO algorithm; (b) shows the collection of high-quality jigsaw trajectory data; and (c) illustrates the model–environment interaction during the jigsaw rollout process*

AGILE 将拼图求解建模为**逐步代码交互过程**，其核心 pipeline 由三个紧密耦合的模块构成：可编程数据合成、冷启动监督微调（SFT）和交互式强化学习（RL），整体架构如 Figure 2 所示。

### 数据流与模块关系

**输入**为一张高分辨率、OCR 或真实场景图像，经可编程规则分割为 $m \times m$ 网格并随机打乱，生成难度可控的拼图状态 $I_{Shuffle}$。**输出**为模型通过多步交互逐步恢复的正确排列 $I_{GT}$。

三个核心模块的协作流程如下：

1. **Programmatic Data Synthesis（可编程数据合成）**：从多源图像中自动生成大规模拼图训练数据，支持无限扩展且难度可控（通过初始正确块数 $N$ 调节）。该模块为后续 SFT 和 RL 阶段提供结构化训练信号。

2. **Cold-Start SFT Stage（冷启动监督微调）**：利用 Gemini 2.5 Pro 生成的 1.6K 专家交互轨迹进行监督微调，使基座模型（Qwen2.5-VL-7B）掌握基本的指令遵循和 Python 代码生成能力，确保模型能够与环境进行初始交互。训练在 llama-factory 上以全参数微调完成。

3. **Interactive RL with GRPO（交互式强化学习）**：采用组相对策略优化（GRPO），模型在每一步生成 Python 代码调用预定义 API（Swap、Observe、Crop、Zoom），环境执行代码后返回**细粒度视觉反馈**（当前观察图像和错误信息），形成多步观察-行动循环。奖励函数由准确性、格式和步数惩罚三部分加权组合（$\alpha=0.8, \beta=0.2, \gamma=1.0$），鼓励以最少有效步骤完成拼图。RL 训练在 verl 上以全参数微调完成。

### 关键交互机制

模型与环境的交互通过预定义的 Python API 实现，动作空间包含四类操作（Figure 1）：
- **Swap**：交换两块拼图并观察更新后的拼图状态
- **Observe**：获取当前完整拼图排列的视觉反馈
- **Crop**：裁剪特定区域进行局部细节观察
- **Zoom**：放大选定区域以检查细粒度纹理和边缘连续性

这种代码驱动的交互设计使得环境能够返回精确的视觉反馈信号，为 GRPO 提供密集的训练奖励，驱动模型在探索与反馈中迭代增强感知和推理能力。消融实验表明，去除 Crop/Zoom 动作会导致下游任务平均性能下降约 0.4%（Table 8），验证了细粒度局部观察行为对鲁棒感知推理学习的关键作用。



### 3.1 交互环境与动作空间

AGILE将拼图求解建模为模型与外部环境之间的逐步交互过程。给定输入图像，环境将其分割为 $m \times m$ 的网格块，并维护三种状态表示：

- **打乱状态**：$I_{Shuffle} = \{ I_{1}, I_{2}, \dots, I_{m^{2}} \}$，表示随机排列后的拼图块集合。
- **真值布局**：$I_{GT} = \{ I_{\pi(1)}, I_{\pi(2)}, \ldots, I_{\pi(m^{2})} \}$，其中 $\pi$ 为正确的置换映射。
- **当前状态**：$I_{State} = \{ I_{\pi^{*}(1)}, I_{\pi^{*}(2)}, \dots, I_{\pi^{*}(m^{2})} \}$，其中 $\pi^{*}$ 为模型当前维护的排列。

环境预定义Python API，模型通过生成可执行代码调用以下四类动作（图1）：

1. **Swap**：交换任意两块拼图的位置，环境返回更新后的全局视图。
2. **Observe**：获取当前完整拼图状态的视觉快照。
3. **Crop**：裁剪指定区域进行局部细致观察，返回高分辨率裁剪图像。
4. **Zoom**：对选定区域进行放大，以检查细粒度视觉细节。

每次动作执行后，环境返回对应的视觉反馈（当前观察图像及可能的错误信息），形成多步“观察—代码生成—执行—反馈”循环。

### 3.2 冷启动监督微调

为使模型具备基本的指令遵循和Python代码交互能力，AGILE首先利用Gemini 2.5 Pro生成的1.6K高质量拼图求解轨迹进行监督微调（SFT）。这些轨迹包含完整的多步交互序列，涵盖从初始观察到逐步推理、代码生成直至拼图完成的全过程。冷启动阶段使用全参数微调，在llama-factory框架上完成。

### 3.3 交互式强化学习

强化学习阶段采用**组相对策略优化**（Group Relative Policy Optimization, GRPO），其核心目标函数为：

$$
\mathcal { I } _ { \mathrm { G R P O } } ( \theta ) = \mathbb { E } _ { x \sim \mathcal { D } , \{ y _ { i } \} _ { i = 1 } ^ { G } \sim \pi _ { \mathrm { o d d } } ( \cdot | x ; \mathcal { V } ) } \left[ \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \frac { 1 } { \sum _ { t = 1 } ^ { | y _ { i } | } I ( y _ { i , t } ) } \sum _ { t = 1 : I ( y _ { i , t } ) = 1 } ^ { | y _ { i } | } \operatorname* { m i n } \left( \frac { \pi _ { \theta } ( y _ { i , t } \mid x , y _ { i , < t } ; \mathcal { V } ) } { \pi _ { \mathrm { o d d } } ( y _ { i , t } \mid x , y _ { i , < t } ; \mathcal { V } ) } \hat { A } _ { i , t } , \mathrm { c l i p } \left( \frac { \pi _ { \theta } ( y _ { i , t } \mid x , y _ { i , < t } ; \mathcal { V } ) } { \pi _ { \mathrm { o d d } } ( y _ { i , t } \mid x , y _ { i , < t } ; \mathcal { V } ) } , 1 - \epsilon , 1 + \epsilon \right) \hat { A } _ { i , t } \right) \right] - \beta \mathbb { D } _ { \mathrm { K L } } ( \pi _ { \theta } \| \pi _ { \mathrm { r e f } } )
$$

其中：$G$ 为每组采样的轨迹数，$\hat{A}_{i,t}$ 为组内相对优势估计，$\epsilon$ 为裁剪阈值，$\beta$ 控制KL散度惩罚强度以防止策略偏离参考模型过远。GRPO的核心优势在于无需单独训练价值网络，通过组内比较即可获得稳定的优势信号。

**奖励函数**由三个分量加权组合而成：

1. **准确性奖励** $R_{\mathrm{acc}}$：拼图完全正确时为1，否则为0。
2. **格式奖励** $R_{\mathrm{format}}$：模型输出符合预期代码格式时为1，否则为0。
3. **步数奖励** $R_{\mathrm{step}}$：

$$
R _ { \mathrm { s t e p } } = \lambda \cdot \Big ( \mathbb { I } _ { \{ R _ { \mathrm { a c c } } = 1 \} } \cdot s t e p _ { \mathrm { n u m } } + \mathbb { I } _ { \{ R _ { \mathrm { a c c } } = 0 \} } \cdot s t e p _ { \mathrm { m a x } } \Big )
$$

其中 $\lambda = -0.05$ 为步数惩罚系数。当拼图正确完成时，按实际步数 $step_{\mathrm{num}}$ 施加惩罚；当拼图错误时，赋予最大步数惩罚 $step_{\mathrm{max}}$，以防止模型在早期RL训练中通过随机动作“刷”步数奖励。

总奖励为三者的加权和：

$$
R = \alpha \cdot R _ { \mathrm { a c c } } + \beta \cdot R _ { \mathrm { f o r m a t } } + \gamma \cdot R _ { \mathrm { s t e p } }
$$

权重设定为 $\alpha = 0.8$，$\beta = 0.2$，$\gamma = 1.0$。该设计使准确性奖励占据主导地位，格式奖励确保代码输出的可执行性，步数奖励则鼓励模型以最少的有效步骤完成拼图，从而学习高效的感知与推理策略。

### 3.4 可编程数据合成

RL训练数据通过可编程规则自动生成：从高分辨率自然图像、OCR文档图像、真实场景图像等多源数据中，将图像分割为 $m \times m$ 网格并随机打乱，自动生成大规模、难度可控的拼图实例。难度由初始正确块数 $N$ 控制（$N$ 越小，打乱程度越高，难度越大）。这种合成方式无需人工标注，理论上可无限扩展训练数据规模。



## 实验与关键发现

### 拼图任务性能：从随机猜测到高精度求解

AGILE 将拼图求解从近乎随机猜测的水平提升至高精度完成，验证了交互式强化学习对感知与推理能力的根本性强化。Table 1 展示了 2×2 和 3×3 拼图设置下的准确率结果。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/003_Table_1.jpg]]
*Table 1: Jigsaw Acc result. LN indicates the difficulty level, where N denotes the initial number of correct pieces. A smaller N corresponds to a more scrambled jigsaw and higher difficulty. The best results are highlighted in bold, and the second-best results are underlined*

在 2×2 拼图上，基座模型 Qwen2.5-VL-7B 经冷启动 SFT 后平均准确率仅为 **9.5%**，接近随机水平（25%），表明现有 VLM 缺乏基础的细粒度视觉辨别与空间关系推理能力。经 AGILE 交互式 RL 训练后，平均准确率跃升至 **82.8%**（+73.3 个百分点），在所有难度级别（L0–L7）上均大幅超越冷启动基线和 GPT-4o、Gemini-2.5-Pro 等闭源模型。Table 2 的 Score 指标同样印证这一趋势：平均 Score 从 29.4% 提升至 89.0%，说明模型不仅完成拼图，而且以更少的有效步骤完成。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/004_Table_2.jpg]]
*Table 2: Jigsaw Score result. LN indicates the difficulty level, where N denotes the initial number of correct pieces. A smaller N corresponds to a more scrambled jigsaw and higher difficulty. The best results are highlighted in bold, and the second-best results are underlined*

在更具挑战性的 3×3 拼图上，冷启动 SFT 准确率降至 0.4%，而 AGILE 训练后达到 **20.8%**（+20.4 个百分点）。尽管绝对数值仍较低，但这一提升幅度表明交互式学习范式具备向更复杂空间推理任务扩展的潜力。当前 3×3 训练受限于上下文窗口长度，是性能进一步提升的主要瓶颈。

### 下游任务泛化：感知推理能力迁移至通用视觉基准

AGILE 训练后的模型在 9 个通用视觉基准上平均性能提升 **3.1%**（Table 3），证明拼图交互学习获得的感知推理能力可有效泛化至一般视觉理解任务。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/005_Table_3.jpg]]
*Table 3: Main results. Performance comparison of different models on the 9 benchmarks. Abbreviations: MME-RW (MME-RealWorld-Lite), RWQA (RealWorldQA), HRB4K (HRBench4K), HRB8K (HRBench8K), HalBench (HallusionBench), MMMU (MMMU VAL), Avg. denotes the average performance across all 9 benchmarks. ∆ represents the relative performance gain achieved by RL compared to the base model Qwen2.5-VL-7B. The best results are highlighted in bold, and the second-best results are underlined*

具体而言，在需要细粒度视觉辨别的基准上提升尤为显著：**HRBench4K** 提升 4.2%（68.8% → 73.0%），**HRBench8K** 提升 5.2%（65.3% → 70.5%），**VStarBench** 提升 4.2%（76.4% → 80.6%）。这些基准要求模型在复杂场景中定位细微视觉差异，与拼图任务中对局部细节的反复观察和比对高度一致。在 RealWorldQA 上提升 2.6%，HallusionBench 上提升 3.9%，进一步表明感知能力的底层强化具有跨任务迁移性。

值得注意的是，AGILE 训练的 7B 模型在多个基准上超越更大规模的 Qwen2.5-VL-72B（如 HRBench4K 上 73.0% vs 72.0%），且显著优于同等规模的 InternVL3-8B 和 MiMo-VL-7B-RL，验证了交互式拼图训练相对于传统 RL 方法的效率优势。

### 消融实验：交互机制与奖励设计的关键作用

#### 动作空间消融：Crop/Zoom 的不可替代性

Table 8 显示，移除 Crop/Zoom 操作后，下游任务平均性能从 63.9% 降至 63.5%（下降约 0.4%）。这一消融结果揭示了细粒度交互行为的关键因果机制：Crop 和 Zoom 操作使模型能够对拼图局部区域进行放大观察，迫使模型学习精确的视觉特征对比和空间位置验证。缺乏这些操作时，模型仅能依赖全局 Swap 和 Observe，训练信号的粒度不足以充分强化底层视觉编码器。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/020_Table_8.jpg]]
*Table 8: Performance of RL without Gemini 2.5 Pro expert trajectories and with ablated action spaces. Furthermore, removing the Crop/Zoom operations leads to a clear decline in performance, underscoring the importance of AGILE’s interaction design in enabling effective fine-grained perceptual reasoning*

#### 奖励函数消融：步数惩罚的必要性

Table 6 的奖励系数消融表明，移除步数奖励（γ=0）导致 VStarBench 和 MMVP 性能明显下降。步数惩罚（R_step）的设计机制是：正确完成时按实际步数惩罚（λ=−0.05），错误时赋予最大步数惩罚。这一设计鼓励模型以最少有效步骤完成拼图，抑制无意义的随机尝试行为，从而在 RL 过程中形成高效的观察-行动策略。值得注意的是，为防止模型在 RL 早期“破解”步数奖励，该惩罚仅在拼图正确完成时生效。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/018_Table_6.jpg]]
*Table 6: Ablation on Reward Coefficients. Sensitivity analysis of the weighting coefficients $\alpha , \beta$ , and γ in the total reward

#### 冷启动数据规模消融：RL 是性能提升主因

Table 10 显示，将冷启动 SFT 数据集从 1.6K 扩展至 2.4K 和 3.2K 仅带来微弱差异。同时，Table 8 表明完全去除专家轨迹、仅靠交互式 RL 训练仍可实现 +1.8% 的平均性能提升。这两项消融共同证明：主要性能增益源自 RL 过程中的交互探索与反馈，而非对闭源模型 Gemini 2.5 Pro 的蒸馏。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/022_Table_10.jpg]]
*Table 10: Effect of scaling the cold-start (SFT) dataset size. Increasing SFT data provides only marginal differences, indicating that most performance gains come from the RL stage*

### 训练数据规模与质量分析

Figure 3 揭示了训练数据规模的缩放效应：随着拼图 RL 数据从 5K 增至 20K，拼图任务准确率从 22.0% 单调上升至 82.8%，HRBench4K 和 RealWorldQA 分别提升 2.0% 和 1.8%。这一趋势验证了可编程数据合成的核心优势——难度可控、规模可无限扩展，为 RL 提供持续的性能增长动力。

Figure 4 和 Table 9 的对比实验进一步凸显拼图任务的独特训练价值：在同等 20K 样本总量下，纯拼图 RL 训练效果优于纯通用 QA RL 训练，且拼图+QA 混合训练（各 10K）优于纯 QA 训练。这表明拼图任务提供的结构化感知推理信号具有通用 QA 数据无法替代的训练价值。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/021_Table_9.jpg]]
*Table 9: Comparison between General QA and Jigsaw-based RL under equal training budgets (20K)*

### 课程学习与扩展性

Table 7 展示了课程学习的有效性：在 2×2 拼图 RL 之后引入 3×3 拼图课程 RL 训练，所有 9 个下游基准均获得进一步提升。这表明通过渐进式难度递增，模型可将从简单拼图学到的感知推理策略迁移至更复杂的空间配置任务。然而，当前 3×3 训练受限于上下文窗口长度，更大尺寸（4×4 及以上）的课程扩展需要先解决交互轨迹的上下文压缩问题。

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/019_Table_7.jpg]]
*Table 7: Results of 3 $\times$ 3 Jigsaw RL Training*

### 注意力图可视化证据

Figure 12 的注意力图对比为感知机制强化提供了直观证据：AGILE 训练后，模型在图像关键区域（如物体边界、纹理细节）的注意力显著增强，热力分布更加集中和精确。这一可视化结果与下游细粒度基准的性能提升相互印证，表明交互式拼图训练确实在底层视觉编码器层面强化了特征提取能力。

### 失败模式与局限性

尽管 AGILE 在 2×2 拼图上取得显著成功，3×3 拼图准确率仍仅 20.8%，暴露出当前方法的两个核心局限：其一，多轮交互导致上下文长度急剧膨胀，在 3×3 设置下常超出模型最大窗口限制；其二，随着网格增大，动作空间组合爆炸使得 RL 探索效率下降。这些失败模式指向未来工作的关键方向——设计更高效的交互机制（如外部记忆模块、分层动作空间）以支持更大规模拼图的 RL 训练。

### 补充图表

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/016_Figure_11.jpg]]
*Figure 11: Visualization of Wandb curves in jigsaw RL optimization*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/014_Table_4.jpg]]
*Table 4: Key hyperparameters for SFT*

![[assets/figures/papers/paper_list_l3_https_openreview_net_forum_id_3kouij8BWi/figures/015_Table_5.jpg]]
*Table 5: Key hyperparameters for RL*



## 定位与知识库关联

### 核心范式定位

AGILE 属于**交互式强化学习驱动视觉感知增强**这一新兴范式，其核心特征是以可编程合成的结构化代理任务为训练媒介，通过多轮代码交互与可验证奖励信号，驱动视觉-语言模型（VLM）在底层感知机制上获得可泛化的增强。与传统VLM训练范式相比，AGILE 在三个维度上构成关键偏离：

- **训练信号来源**：从依赖人工标注或闭源模型蒸馏的静态QA对，转向可编程规则自动生成的拼图数据，难度可控、规模可无限扩展。
- **学习机制**：从单轮监督微调或直接推理，转向“冷启动SFT + 多轮交互式GRPO强化学习”的两阶段范式，模型在探索与反馈的闭环中迭代优化。
- **交互粒度**：从无环境交互，转向模型生成Python代码调用Swap/Observe/Crop/Zoom动作、环境返回细粒度视觉反馈的多步观察-行动循环。

这一范式区别于两类相关工作：

1. **VLM的强化学习微调**：如 **MiMo-VL-7B-RL** 等工作同样采用RL优化VLM，但其训练信号通常来自通用QA任务或偏好数据，缺乏结构化交互环境提供的密集、可验证的感知反馈。AGILE 表明，拼图交互提供的细粒度视觉辨别与空间推理信号，在等量训练预算下优于通用QA数据（Table 9）。

2. **工具使用与代码生成VLM**：AGILE 的代码交互机制在形式上与工具调用VLM相似，但其本质差异在于：代码执行的目的不是完成外部任务，而是获取环境返回的视觉观察，形成感知-行动的闭环学习。消融实验表明，移除Crop/Zoom等细粒度观察动作会导致下游任务性能下降（Table 8），说明交互粒度对感知学习至关重要。

### 基座模型与基线关系

AGILE 以 **Qwen2.5-VL-7B**（Bai et al., 2025）为基座模型进行全参数微调，并与以下基线进行系统比较：

- **同架构基座**：Qwen2.5-VL-7B 的零样本性能作为核心对比基准，AGILE 在9个通用视觉基准上平均提升3.1%（Table 3）。
- **更大规模VLM**：Qwen2.5-VL-72B（Bai et al., 2025）作为规模扩展的参照，AGILE训练的7B模型在HRBench4K（73.0% vs 72.7%）和VStarBench（80.6% vs 80.1%）上超越了72B基座，表明交互式RL可部分弥补参数规模差距。
- **闭源前沿模型**：GPT-4o 和 Gemini-2.5-Pro 作为性能上界参照，AGILE在多个基准上接近甚至超越这些闭源模型（Table 3）。
- **开源VLM**：包括 InternVL3-8B/78B、InternVL2.5-8B、LLaVA-OV-7B 等，AGILE在大多数基准上取得最优或次优结果。

### 方法适用边界

基于论文提供的实验证据，AGILE 的适用边界可初步界定如下：

**已验证的适用场景**：
- 需要细粒度视觉辨别的任务（HRBench4K +4.2%、HRBench8K +5.2%），表明拼图训练强化了模型对图像局部细节的感知能力。
- 需要结构化空间推理的任务（VStarBench +4.2%），拼图求解中的位置关系推理可泛化至一般视觉推理场景。
- 可受益于交互式探索的视觉理解任务，Crop/Zoom动作的消融实验证实了主动局部观察行为的价值。

**已知局限**：
- **上下文长度瓶颈**：多轮拼图交互导致上下文长度急剧增加，在3×3设置下常超出模型最大窗口长度，限制了复杂拼图的RL训练。这是当前方法的核心工程约束，而非理论限制。
- **网格规模限制**：当前RL训练仅基于2×2拼图设定，3×3拼图准确率仅20.8%（Table 1），表明方法尚未有效扩展到更大规模拼图。
- **冷启动依赖**：冷启动阶段依赖闭源模型 Gemini 2.5 Pro 生成专家轨迹，可能引入成本和稳定性问题。但消融实验表明，完全移除专家轨迹后仅靠交互式RL仍可实现+1.8%的平均性能提升（Table 8），说明该依赖非性能提升主因。

**待验证的迁移边界**：
- 论文未提供拼图训练对视频理解、三维场景理解等时序/空间推理任务的迁移证据。
- 拼图数据分布以自然场景图像为主（Figure 6），对文档、图表、医学图像等特殊域的泛化能力尚不明确。

### 开放问题

1. **交互效率与规模扩展**：如何设计更高效的交互机制（如外部记忆模块、分层动作空间）以支持3×3甚至4×4拼图的RL训练而不超出上下文窗口？这是方法从概念验证走向更大规模应用的关键工程挑战。

2. **最优难度与课程设计**：随着拼图网格增大，下游视觉任务的性能增益曲线如何变化？2×2+3×3课程RL已展示进一步增益（Table 7），但最优难度比和课程策略仍需系统探索。

3. **代理任务空间扩展**：拼图交互学习范式是否可以扩展到其他结构化代理任务？论文暗示了视频帧排列、三维场景重组等潜在方向，但尚未提供实验证据。

4. **零样本迁移能力**：AGILE训练的模型是否能零样本迁移到需要结构化感知的其他任务（如图像修复、目标检索）？当前实验仅覆盖标准视觉理解基准，更广泛的迁移能力有待验证。

5. **感知机制的可解释性**：注意力图可视化（Figure 12）提供了初步的定性证据，但拼图训练究竟改变了VLM视觉编码器的哪些表征特性，仍需更系统的机制分析。



## 原文 PDF

![[paperPDFs/ICLR_2026/Agentic_Jigsaw_Interaction_Learning_for_Enhancing_Visual_Perception_and_Reasoning_in_Vision_Language_Models.pdf]]
