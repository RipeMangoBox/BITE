---
title: "FrankenMotion: Part-level Human Motion Generation and Composition"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/FrankenMotion_Part_level_Human_Motion_Generation_and_Composition.pdf
aliases:
- FrankenMotion
tags:
- CVPR_2026
- topic/motion_animation
- topic/motion_animation/human_motion_generation
core_operator: "利用大语言模型（FrankenAgent）从高层次动作描述中推断身体部位的原子动作并生成结构化、时间对齐的部件级文本提示，同时训练一个层次化条件扩散模型（FrankenMotion）以利用这些细粒度提示。"
primary_logic: "复杂运动可分解为原子运动元素；大语言模型具备从高层语义中推理身体部件行为的能力，从而通过层次化文本条件实现运动生成中的细粒度空间-时间控制。"
claims:
- "we introduce a diffusion-based part-aware motion generation framework, namely FrankenMotion, where each body part is guided by its own temporally-structured textual prompt."
- "we instantiate FrankenAgent, an LLM agent that consumes existing datasets and outputs coherent per-frame body part annotations together with high level annotations."
- "FrankenMotion, a text-to-motion model that learns to compose complex motions through hierarchical conditioning on part-, action-, and sequence-level text"
- "FrankenAgent annotations are 93.08% correct according to human experts."
---

# FrankenMotion: Part-level Human Motion Generation and Composition

> [!tip] 核心洞察
> 复杂运动可分解为原子运动元素；大语言模型具备从高层语义中推理身体部件行为的能力，从而通过层次化文本条件实现运动生成中的细粒度空间-时间控制。

| 字段 | 内容 |
|------|------|
| 中文题名 | FrankenMotion：人体局部运动生成与组合 |
| 英文题名 | FrankenMotion: Part-level Human Motion Generation and Composition |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2601.10909) · [Project](https://coral79.github.io/frankenmotion/) |
| Topic | #topic/motion_animation #topic/motion_animation/human_motion_generation |
| Method | FrankenMotion |
| Dataset | FrankenStein (test set) |

> [!tip] 效果简介
> - FrankenStein (test set) 上，Per-seq semantic correctness (M2T) 为 0.76。
> - FrankenStein (test set) 上，Per-action realism (FID) 为 0.04。
> - FrankenStein (test set) 上，Per-seq realism (FID) 为 0.06。

## 概述

文本驱动的人体运动生成近年来取得了显著进展，但现有方法普遍受限于粗粒度的全局序列描述或动作片段标签，缺乏对身体部件级别运动的细粒度、时间对齐的控制能力。这一瓶颈导致模型难以精确指定“左手抬起的同时右手保持不动”等空间-时间约束，限制了运动生成在交互式应用中的实用性。

针对上述问题，本文提出 **FrankenMotion**，一个基于扩散模型的部件感知运动生成框架。其核心思想是：复杂运动可分解为原子运动元素，而大语言模型具备从高层语义中推理身体部件行为的能力。方法包含两个关键组件：（1）**FrankenAgent**，一个基于大语言模型的智能体，从现有运动捕捉数据的高层动作描述中自动推断并生成结构化、时间对齐的身体部件级文本标注，构建 **FrankenStein** 数据集（总时长39.1小时，词汇量4,117）；（2）**FrankenMotion**，一个层次化条件扩散模型，同时接受序列级、原子动作级和部件级文本提示，学习将原子运动元素组合为复杂运动。

实验表明，FrankenAgent的自动标注经人工专家验证准确率达93.08%，标注者间一致性系数AC1为0.91。在FrankenStein测试集上，FrankenMotion在所有设定下均优于现有基线方法，在部件运动的语义正确性（M2T 0.76）和真实感（FID 0.04–0.06）上均取得最佳性能。消融实验进一步证实，仅使用部件级文本条件即可达到有竞争力的语义正确性（M2T 0.69），而加入原子动作和序列级文本后，部件运动的正确性和真实感进一步提升。

该方法在方法谱系上定位于文本驱动运动生成与层次化条件控制的交叉点，通过引入部件级时间对齐标注和相应的扩散模型架构，填补了从全局运动控制到细粒度身体部件控制之间的空白。

## 背景与动机

文本驱动的人体运动生成旨在根据自然语言描述合成逼真的三维人体动作序列，在动画制作、虚拟现实和人机交互等领域具有广泛的应用前景。近年来，扩散模型和Transformer架构的引入显著提升了运动生成的质量与多样性，然而现有方法在控制粒度上仍存在根本性瓶颈：它们通常仅支持序列级或粗粒度动作片段的全局文本描述，缺乏对单个身体部位进行精确、时间对齐的细粒度控制能力。

这一瓶颈的根源在于训练数据的标注粒度不足。主流运动-语言数据集（如HumanML3D、KIT-ML、BABEL）仅提供覆盖整个序列或粗粒度动作片段的高层语义标签，缺少身体部位级别的原子运动标注。这使得模型难以学习“左手抬起的同时右手保持下垂”或“腿部行走而躯干前倾”等涉及多部位协调的复杂运动模式。从因果机制来看，缺乏细粒度标注直接限制了模型对运动元素进行解耦和重组的能力，导致生成的运动在空间-时间维度上难以精确遵循用户的意图。

针对上述问题，FrankenMotion提出了一种全新的范式：利用大语言模型（LLM）的推理能力，从现有的高层动作描述中自动推断身体部位的原子动作，并生成结构化、时间对齐的部件级文本提示。这一思路的核心洞察在于，复杂运动本质上可分解为原子运动元素的组合，而LLM具备从高层语义中推理身体部件行为的能力，从而通过层次化文本条件实现运动生成中的细粒度空间-时间控制。

具体而言，FrankenMotion框架包含两个关键组件：一是FrankenAgent，一个基于LLM的智能体，负责从现有数据集中自动构建带有逐帧身体部件标注的FrankenStein数据集；二是FrankenMotion模型本身，一个层次化条件扩散模型，能够同时接收部件级、动作级和序列级三个粒度的文本提示，学习将原子运动元素组合为复杂运动。通过这种层次化条件机制，用户可以在不同抽象层级上对生成过程施加控制——从单个身体部位的精细运动，到全身协调的原子动作，再到完整的多阶段运动序列，如图1所示。

这种数据与模型协同设计的策略，为解决细粒度运动生成中的标注稀缺和可控性不足两大挑战提供了系统性的方案，也为后续探索更长时间跨度、更复杂交互场景下的运动生成奠定了基础。

## 核心创新

FrankenMotion 的核心创新在于将**文本驱动的运动生成从全局序列描述推进到身体部件级别的细粒度时空控制**。这一突破通过两个紧密耦合的组件实现：一个基于大语言模型（LLM）的自动标注智能体 **FrankenAgent**，以及一个**层次化条件扩散模型** **FrankenMotion**。两者共同解决了现有方法中“缺乏时间对齐的身体部件级动作标注”这一核心瓶颈，使得模型能够学习、组合并生成具有精确部件语义的复杂运动。

### 创新一：LLM 驱动的细粒度时空标注范式

传统运动-语言数据集（如 KIT-ML、HumanML3D）仅提供序列级或粗粒度动作片段标注，无法为单个身体部件（如左臂、右腿）提供与时间窗口对齐的运动描述。FrankenMotion 提出了一种全新的数据构建范式：

- **FrankenAgent**：一个基于 LLM 的推理智能体，其核心能力是从高层动作描述（如“走路时挥手”）中推断出各身体部件在特定时间段内的原子动作，并输出结构化的、时间对齐的部件级文本提示。形式上，每个标注元素定义为 $a = (L, t_s, t_e)$，其中 $L$ 为描述文本，$t_s$ 和 $t_e$ 分别为动作的起止时间。完整的标注集合 $\mathcal{A} = \{\mathcal{A}_s, \mathcal{A}_a, \mathcal{A}_p\}$ 涵盖序列级、原子动作级和部件级三个粒度。
- **FrankenStein 数据集**：基于上述流程，在现有数据集基础上构建了包含 39.1 小时运动数据、4117 个词汇量的多粒度标注数据集。经人工专家验证，FrankenAgent 的标注准确率达到 **93.08%**，标注者间一致性系数 AC1 为 **0.91**，证实了自动标注的高质量。

这一创新的本质在于**将 LLM 的常识推理能力迁移到运动理解的标注任务中**，以极低的人工成本实现了从粗粒度到细粒度标注的跨越，为下游模型提供了前所未有的监督信号密度。

### 创新二：层次化条件扩散模型实现部件级组合生成

在获得细粒度标注后，FrankenMotion 设计了一个能够同时接收并融合三级文本条件的扩散模型架构：

- **三级条件层次**：
  - **序列级文本** $\mathbf{L}_s$：提供全局运动语义（如“一个人走向椅子然后坐下”）。
  - **动作级文本** $\mathbf{L}_a$：在时间窗口内描述原子动作（如“行走”、“转身”）。
  - **部件级文本** $\mathbf{L}_p$：为每个身体部件提供逐帧的运动描述（如“右臂前摆”、“左腿支撑”）。

- **条件融合与生成**：模型采用 Transformer 架构的扩散模型，其预测过程可表示为 $\hat{\mathbf{x}}_0^{[1...T]} = f_{\theta}(\mathbf{x}_{\sigma}^{[1...T]}, \sigma, \mathbf{L}_s, \mathbf{L}_a, \mathbf{L}_p)$。通过 CLIP 文本编码器提取多粒度文本特征，经 PCA 降维后与含噪运动特征拼接，映射到联合隐空间中进行去噪预测。

- **鲁棒训练策略**：训练期间对部件文本采用 **Beta 分布的随机掩码**，迫使模型在部分部件标注缺失时仍能依赖动作级和序列级语义进行合理推断，从而增强了模型在推理时处理不完整条件的能力。

### 创新三：从“拼接”到“组合”的运动生成范式转变

与基线方法形成鲜明对比：
- **STMC**（Petrovich et al., arXiv 2024）采用“分而治之”策略，先独立生成各部件运动再拼接，导致整体运动不协调。
- **UniMotion**（Li et al., arXiv 2024）支持序列级和帧级条件，但缺乏身体部件维度的控制。
- **DART**（Zhao et al., ICLR 2025）基于自回归方式，难以精确遵循细粒度的部件指令。

FrankenMotion 的核心洞察在于：**复杂运动可分解为原子运动元素，而 LLM 具备从高层语义中推理身体部件行为的能力**。通过层次化文本条件，模型在训练中隐式地学习了“运动元素”及其组合规则，从而在推理时能够将部件级、动作级和序列级指令协调地融合，生成既满足细粒度约束又保持整体真实感的运动。消融实验证实了这一设计的有效性：仅使用部件文本条件时，模型已能达到有竞争力的语义正确性（M2T 0.69）；加入原子动作和序列级文本后，部件运动的正确性和真实感进一步提升（完整模型 FID 0.05）。

### 方法谱系与知识库定位

FrankenMotion 处于**文本驱动的层次化运动生成**与**LLM 辅助的数据增强**的交叉点。其方法论贡献可概括为：
1. **标注维度扩展**：将运动标注从“序列-动作”二维推进到“序列-动作-部件”三维，为细粒度运动生成提供了数据基础。
2. **条件机制创新**：通过层次化条件注入，使扩散模型能够同时处理全局语义、局部动作和部件细节，实现了真正意义上的“组合式”运动生成。
3. **LLM 与运动生成的深度融合**：不同于仅用 LLM 做文本增强的现有工作，FrankenAgent 直接参与结构化时空标注的生成，开辟了 LLM 作为“运动理解推理引擎”的新角色。

**待验证问题**：当部件级与动作级或序列级指令发生冲突时，模型如何处理不一致的条件？扩散模型架构如何具体处理时间对齐的部件级提示，以实现精确的逐帧控制？这些问题需要进一步的手动验证或源码分析。

## 整体框架

FrankenMotion 是一个基于扩散模型的部件感知人体运动生成框架，其核心设计理念是将复杂运动分解为原子运动元素，并通过层次化的文本条件实现细粒度的空间-时间控制。该框架由两条协同工作的主线构成：数据侧的 **FrankenAgent** 智能体负责从高层动作描述中自动推断并生成结构化、时间对齐的身体部件级文本标注；模型侧的 **FrankenMotion** 扩散模型则以这些多粒度文本条件为输入，学习合成符合指令的逼真运动序列。

### 框架总览

FrankenMotion 支持三种递进的控制模式（Figure 1）：

![[assets/figures/papers/paper_list_l17_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition/figures/003_Figure_1.jpg]]
*Figure 1: Overview of our FrankenMotion framework. Left: Body-Part Control, where users specify fine-grained movements of individual body parts; Middle: Body-Part + Action Control, enabling coordinated whole-body actions with part-specific constraints; Right: Body-Part + Action + Sequence Control, supporting complex multi-stage motion sequences involving interactions and transitions. In all cases, FrankenAgent translates natural-language instructions into structured control signals for precise motion generation*

1. **Body-Part Control（身体部件控制）**：用户指定单个身体部位的细粒度运动，例如“左手抬起”或“右脚向前迈出”。
2. **Body-Part + Action Control（部件+动作控制）**：在部件级约束的基础上，叠加协调的全身原子动作，实现“边挥手边下蹲”等复合行为。
3. **Body-Part + Action + Sequence Control（部件+动作+序列控制）**：支持包含交互和过渡的复杂多阶段运动序列，如“先走向椅子，坐下，然后挥手告别”。

在以上所有模式下，**FrankenAgent** 负责将自然语言指令翻译为结构化的控制信号，供后续的扩散模型使用。

### 数据管线：FrankenAgent 与 FrankenStein 数据集

由于现有运动-语言数据集仅提供粗粒度的序列级或动作级标签，缺乏时间对齐的身体部件标注，FrankenMotion 首先构建了 **FrankenStein** 数据集。该数据集以 KIT-ML、BABEL 和 HumanML3D 为基础，利用大语言模型智能体 **FrankenAgent** 进行自动标注。

FrankenAgent 的标注流程（Figure 2）如下：
- 输入：运动序列及其高层动作描述。
- 推理：LLM 将动作分解为身体部件级别的描述，并将其与对应的时间窗口对齐。
- 输出：结构化的三层标注集合 $\mathcal{A} = \{ \mathcal{A}_s , \mathcal{A}_a , \mathcal{A}_p \}$，其中：
  - $\mathcal{A}_s$ 为覆盖整个序列的单一序列级描述；
  - $\mathcal{A}_a$ 为 $N$ 个不重叠的原子动作标注列表，每个原子动作定义为一个三元组 $a = ( L , t_s , t_e )$，包含描述文本 $L$、开始时间 $t_s$ 和结束时间 $t_e$；
  - $\mathcal{A}_p$ 为 $K$ 个身体部件的细粒度标注，每个部件包含其自身的原子运动描述。

经人工专家评估，FrankenAgent 的标注准确率达到 **93.08%**，标注者间一致性系数 Gwet's AC1 为 **0.91**，验证了自动标注的质量。最终构建的 FrankenStein 数据集包含约 39.1 小时的运动数据，词汇量达 4,117 个，具备序列、原子动作和身体部件三层标签（Table 1）。

### 模型管线：FrankenMotion 扩散模型

FrankenMotion 是一个基于 Transformer 的扩散模型（Figure 3），其输入-输出流如下：

**输入层——多粒度文本编码**：
- **序列级提示** $\mathbf{L}_s$：描述整个运动序列的高层语义。
- **动作级提示** $\mathbf{L}_a$：描述各原子动作片段的内容与时间边界。
- **部件级提示** $\mathbf{L}_p$：为每个身体部位提供时间对齐的细粒度运动描述。
- 所有文本提示均通过 CLIP Text Encoder 提取特征。

**运动表示**：
- 单帧姿态表示为 $\mathbf{x} = [r_z, \dot{r}_x, \dot{r}_y, \dot{\alpha}, \pmb{\theta}, \mathbf{j}]$，包含骨盆 Z 坐标、线性速度、角速度、SMPL 姿态参数和关节位置。

**联合嵌入与扩散去噪**：
- 通过 PCA 降维和拼接，将多粒度文本特征与含噪运动映射到统一的隐空间。
- Transformer 扩散模型从噪声输入和层次化文本条件中预测干净运动序列：
  $$\hat{\mathbf{x}}_0^{[1...T]} = f_{\theta}(\mathbf{x}_{\sigma}^{[1...T]}, \sigma, \mathbf{L}_s, \mathbf{L}_a, \mathbf{L}_p)$$
- 训练目标为标准扩散去噪损失，其中条件 $\mathbf{c}$ 包含层次化文本信息。

**鲁棒训练策略**：
- 训练期间对部件文本采用 Beta 分布的随机掩码，使模型在推理时能够灵活应对部分部件提示缺失的情况，同时保持生成质量。

### 模块关系总结

FrankenMotion 的整体管线可概括为：**FrankenAgent（数据标注）→ CLIP Text Encoder（文本特征提取）→ Action-Part-Motion Embedding（联合嵌入）→ Transformer Diffusion Model（运动生成）**。其中，FrankenAgent 提供的三层时间对齐标注是整个框架实现细粒度部件控制的关键瓶颈突破点；扩散模型则通过层次化条件机制，将分解后的原子运动元素重新组合为符合高层语义的连贯运动序列。

## 核心模块与公式推导

### 姿态表征

FrankenMotion 沿用 STMC 的姿态表征方式。单帧姿态 $\mathbf{x}$ 由骨盆 Z 坐标、线性速度、角速度、SMPL 姿态参数及关节位置拼接而成：

$$\mathbf{x} = [r_z, \dot{r}_x, \dot{r}_y, \dot{\alpha}, \pmb{\theta}, \mathbf{j}]$$

其中 $r_z$ 为骨盆在 Z 轴的位置，$\dot{r}_x, \dot{r}_y$ 为 X、Y 方向的线性速度，$\dot{\alpha}$ 为绕 Z 轴的角速度，$\pmb{\theta}$ 为 SMPL 姿态参数，$\mathbf{j}$ 为关节位置。该表征将运动建模为时序帧序列 $\mathbf{x}^{[1...T]}$。

### 层次化文本条件注入

模型的核心设计在于三层文本条件的并行注入。给定序列级文本 $\mathbf{L}_s$、原子动作文本 $\mathbf{L}_a$ 和身体部件文本 $\mathbf{L}_p$，扩散模型从含噪运动 $\mathbf{x}_{\sigma}^{[1...T]}$ 预测干净运动序列：

$$\hat{\mathbf{x}}_0^{[1...T]} = f_{\theta}(\mathbf{x}_{\sigma}^{[1...T]}, \sigma, \mathbf{L}_s, \mathbf{L}_a, \mathbf{L}_p)$$

其中 $\sigma$ 为噪声水平。三层文本条件分别提供不同粒度的语义约束：$\mathbf{L}_s$ 覆盖整个序列的全局语义，$\mathbf{L}_a$ 划分不重叠的原子动作时间窗，$\mathbf{L}_p$ 为各身体部件提供逐帧的细粒度描述。

### 文本编码与特征融合

所有层次的文本提示均通过 CLIP Text Encoder 提取特征。随后，多粒度文本特征与含噪运动通过 PCA 降维和拼接操作映射到联合隐空间（Action-Part-Motion Embedding），作为 Transformer 扩散模型的输入条件。

### 训练目标与掩码策略

模型采用标准的 DDPM 去噪目标进行训练：

$$\mathcal{L} = \mathbb{E}_{\mathbf{x}_0^{[1...T]}, \sigma, \epsilon} \Big[ \| f_{\theta}(\mathbf{x}_{\sigma}^{[1...T]}, \sigma, \mathbf{c}) - \mathbf{x}_0 \|_2^2 \Big]$$

其中条件 $\mathbf{c}$ 包含层次化文本 $(\mathbf{L}_s, \mathbf{L}_a, \mathbf{L}_p)$。为增强模型在不同条件组合下的鲁棒性，训练期间对部件文本采用 Beta 分布的随机掩码策略，使模型能够在推理时灵活适应部分条件缺失的场景。

### 扩散调度与优化

模型使用余弦噪声调度，共 100 步扩散步。优化器采用 AdamW，学习率 $2 \times 10^{-4}$，批大小 32。

## 实验与分析

### 数据集构建与标注质量

FrankenMotion 的细粒度控制能力建立在 **FrankenStein** 数据集之上。该数据集以 KIT-ML、BABEL 和 HumanML3D 为源数据，通过 LLM 驱动的 **FrankenAgent** 自动推断并生成了三层结构化标注：序列级描述 $\mathcal{A}_s$、原子动作 $\mathcal{A}_a$ 和身体部件级文本 $\mathcal{A}_p$。如表 1 所示，FrankenStein 总计包含 39.1 小时的运动数据，词汇量达 4,117，远超源数据集的标注粒度。

为验证自动标注的可靠性，论文进行了人工评估：FrankenAgent 的标注准确率达到 **93.08%**，标注者间一致性系数 Gwet's AC1 为 **0.91**。这一结果表明 LLM 推断的部件级标注具有与人工标注高度一致的质量，为后续模型训练提供了可信的监督信号。然而，论文未系统分析 LLM 标注中可能存在的系统性偏差或幻觉对下游任务公平性的影响，这一点需要读者注意。

### 主实验结果

论文在 FrankenStein 测试集上将 FrankenMotion 与三类基线方法进行了定量对比：**STMC**（Petrovich et al., arXiv 2024）利用身体部件标签拼接独立生成的零件运动；**UniMotion**（Li et al., arXiv 2024）支持序列级和帧级文本条件但缺乏部件控制；**DART**（Zhao et al., ICLR 2025）基于运动历史进行自回归生成。

如表 2 所示，FrankenMotion 在所有评估维度上均取得最优结果。在语义正确性方面，序列级 M2T 得分达到 **0.76**，序列级 R@3 达到 **85.62**。在运动真实感方面，部件级平均 FID 为 **0.04**，序列级 FID 为 **0.06**。定性对比（图 4）进一步揭示了基线的典型失败模式：STMC 无法将独立生成的部件合成为协调的整体运动，DART 倾向于产生重复性动作，而 UniMotion 则难以遵循“转身”等细节指令。FrankenMotion 能够忠实组合复杂部件运动，同时精确遵循细粒度身体部件提示和高层语义。

### 层次化条件消融

为验证三层文本条件各自的贡献，论文进行了消融实验（表 3）。仅使用部件级文本条件（Part only）时，模型已能达到有竞争力的语义正确性（M2T **0.69**），表明部件级细粒度提示是运动生成的核心驱动力。进一步加入原子动作条件（Part + Action）后，模型获得了时间窗口级别的高层语义引导。完整的层次化条件（Part + Action + Sequence）使部件运动的正确性和真实感进一步提升，最终完整模型的部件级平均 M2M 达到 **0.75**，R@3 达到 **58.97**，FID 降至 **0.05**。这一趋势验证了核心因果机制：序列级文本提供全局上下文，原子动作文本提供时序结构，部件级文本提供空间细粒度约束，三者协同实现了精确的时空控制。

### 失败模式与局限性

尽管 FrankenMotion 在定量和定性评估中表现优异，论文仍指出了若干局限性。首先，现有扩散模型架构难以建模长期时序结构，将运动生成能力扩展到数分钟级别的长序列是未来重要方向。其次，身体部件运动的真实感高度依赖于 FrankenAgent 推断标注的准确性——LLM 的错误标注或幻觉会直接传导至生成质量。此外，论文未讨论当部件级指令与动作级或序列级指令发生冲突时模型的决策行为，也未分析数据分布偏差（如人口学或动作类型偏差）对生成公平性的潜在影响。这些开放问题需要后续研究进一步探索。

### 补充图表

![[assets/figures/papers/paper_list_l17_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition/figures/005_Table_1.jpg]]
*Table 1: Comparison of source motion–language datasets and our extended dataset. Our dataset builds upon KIT-ML [38], BA-BEL [40], and HumanML3D [12], using LLM-based reasoning to produce multi-level, part-aware, and unseen annotations*

![[assets/figures/papers/paper_list_l17_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition/figures/007_Table_2.jpg]]
*Table 2: Evaluating text to motion generation. We report the semantic correctness and realism of parts (averaged), action and sequence level motion, with 95% confidence interval (±) after 20 repeated evaluations. Across all settings, our FrankenMotion achieves the best performance, outperforming all prior baselines in both correctness and realism*

![[assets/figures/papers/paper_list_l17_FrankenMotion_Part_level_Human_Motion_Generation_and_Composition/figures/009_Table_3.jpg]]
*Table 3: Importance of hierarchical input condition. We train models that consume input of part only, or additionally with atomic action, or all part, action and sequence level (Seq.) texts. Even with part-level inputs alone, our model attains strong performance, achieving an M2T score close to the upper-bound GT reference. Incorporating action and sequence texts introduces high-level semantics for the desired motion, which further enhances both the correctness and realism of part-level motion generation*

## 方法谱系与知识库定位

### 1. 核心定位与继承关系

FrankenMotion 的核心贡献在于将文本驱动运动生成的**控制粒度**从“序列/动作级”下推至“身体部件级”，并通过大语言模型（LLM）自动构建训练数据来绕过人工标注的瓶颈。其方法谱系可从以下三个维度展开。

#### 1.1 运动生成架构：扩散模型与层次化条件

FrankenMotion 的骨干是一个基于 Transformer 的扩散模型，直接继承了 **MDM**（Motion Diffusion Model）的去噪范式。在条件注入方式上，它与 **UniMotion**（Li et al., arXiv 2024）共享“层次化文本条件”的设计理念——UniMotion 已支持序列级和帧级（原子动作）文本条件并具备时间对齐能力，但**缺乏身体部件维度的控制**。FrankenMotion 的关键改造在于将条件空间显式扩展为三层：序列级 $\mathbf{L}_s$、原子动作级 $\mathbf{L}_a$ 和部件级 $\mathbf{L}_p$，使扩散模型能够从含噪运动 $\mathbf{x}_{\sigma}^{[1...T]}$ 中预测干净运动 $\hat{\mathbf{x}}_0^{[1...T]} = f_{\theta}(\mathbf{x}_{\sigma}^{[1...T]}, \sigma, \mathbf{L}_s, \mathbf{L}_a, \mathbf{L}_p)$。

#### 1.2 部件感知运动合成：与 STMC 的比较

**STMC**（Petrovich et al., arXiv 2024）是直接面向身体部件运动合成的基线方法。STMC 在推理时接收部件标签作为条件，分别生成各部件运动后进行拼接。然而，其训练数据并未包含细粒度的部件级文本标注，导致拼接后的整体运动缺乏协调性和真实感。FrankenMotion 的改进是根本性的：通过 FrankenAgent 构建的 FrankenStein 数据集，在训练阶段即提供**时间对齐的部件级文本-运动配对**，使模型学习到“原子运动元素”及其组合规律，而非在推理阶段进行后处理拼接。定性结果（Figure 4）表明，STMC 无法将部件组合成真实运动，而 FrankenMotion 则能忠实合成复杂的整体运动。

#### 1.3 自回归运动生成：与 DART 的差异

**DART**（Zhao et al., ICLR 2025）采用自回归范式，基于运动历史和高层次文本提示逐帧生成运动。其控制方式依赖于序列级语义，缺乏对单个身体部件的精确约束。FrankenMotion 的扩散范式与层次化部件条件使其在**空间-时间细粒度控制**上具有本质优势。定量对比（Table 2）显示，DART 存在生成重复运动的问题，而 FrankenMotion 在所有语义正确性和真实感指标上均显著优于 DART。

### 2. 适用边界

#### 2.1 有效范围

- **控制粒度**：支持从“单个身体部件运动”到“多部件协调动作”再到“多阶段序列”的连续控制谱系（Figure 1 的三种模式），是目前文本驱动运动生成中控制粒度最细的方法。
- **数据效率**：通过 LLM 自动标注，将现有运动捕捉数据（KIT-ML、BABEL、HumanML3D）扩展为包含 39.1 小时运动、4,117 词汇量的多粒度标注数据集（Table 1），避免了昂贵的人工标注。
- **鲁棒性**：训练期间对部件文本采用 Beta 分布的随机掩码策略，使模型在推理时可灵活接受不完整的部件级条件。

#### 2.2 已知局限

1. **长期时序建模不足**：论文明确指出“现有方法难以建模长期时序结构”，扩展长时运动生成能力是未来方向。这意味着当前模型在处理数分钟级别的连贯运动序列时可能面临时序一致性问题。
2. **标注质量依赖 LLM**：FrankenAgent 的标注准确率为 93.08%（人工评估），标注者间一致性系数 AC1 为 0.91。尽管这一质量较高，但约 7% 的错误标注可能在下游生成中引入系统性偏差，尤其是当 LLM 对某些动作类型存在系统性幻觉时。
3. **条件冲突处理未明确**：当部件级指令与动作级或序列级指令发生冲突时（如“左手举起”与“双手放下”），模型如何处理不一致的条件，论文未提供机制说明或实验分析。
4. **数据分布偏差**：FrankenStein 继承自现有运动捕捉数据集，可能隐含人口学或动作类型的分布偏差，论文未对此进行公平性分析。

### 3. 开放问题

1. **扩散模型如何精确处理时间对齐的部件级提示？** 论文描述了层次化条件的注入方式（通过 PCA 降维和拼接映射到联合隐空间），但未揭示模型内部如何利用时间戳 $(t_s, t_e)$ 实现逐帧的精确控制。这是理解该方法“细粒度”能力的关键机制缺口。

2. **FrankenAgent 的推断机制是什么？** 论文仅说明 FrankenAgent 是“基于 LLM 的智能体”，但未公开其提示工程策略、推理链设计或后处理规则。这一黑箱特性限制了该标注范式的可复现性和可迁移性。

3. **如何扩展到分钟级长序列？** 当前模型的时序建模能力受限于 Transformer 的上下文窗口和扩散模型的采样效率。长序列生成可能需要引入层次化时序编码、记忆机制或级联生成策略。

4. **部件级控制的真实感上限在哪里？** 身体部件运动并非独立——真实人体运动中存在大量跨部件的生物力学耦合。当前方法将各部件视为可独立控制的条件变量，可能在某些极端组合下违反物理约束。如何显式建模部件间的运动学依赖，是提升真实感的重要方向。

5. **标注错误的传播效应如何量化？** 约 7% 的 FrankenAgent 标注错误对下游生成质量的影响程度未经验证。需要错误注入实验或对抗性测试来评估该方法的标注容错能力。

## 原文 PDF

![[paperPDFs/CVPR_2026/FrankenMotion_Part_level_Human_Motion_Generation_and_Composition.pdf]]
