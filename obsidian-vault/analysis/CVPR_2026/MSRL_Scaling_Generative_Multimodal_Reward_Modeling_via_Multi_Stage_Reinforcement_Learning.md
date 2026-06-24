---
title: "MSRL: Scaling Generative Multimodal Reward Modeling via Multi-Stage Reinforcement Learning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MSRL_Scaling_Generative_Multimodal_Reward_Modeling_via_Multi_Stage_Reinforcement_Learning.pdf
project_link: null
code_link: "https://github.com/wangclnlp/MSRL"
aliases:
- MMSRL
- MSRL
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 利用大规模文本偏好数据中的丰富监督信号来学习通用的奖励推理能力，并通过“文本RL→基于描述的RL→全多模态RL”的课程式迁移机制，在几乎没有额外多模态标注的情况下大幅提升多模态奖励建模的效果。
primary_logic: 偏好建模所需的核心推理能力可以从大量易于获取的纯文本数据中习得，并通过精心设计的多阶段训练以及跨模态知识蒸馏（CMKD）有效地迁移到多模态任务上。
claims:
- MSRL在仅使用与基线相同的多模态偏好数据下，将InternVL3.5-8B的VL-RewardBench平均准确率从生成式MRM基线的66.6%大幅提升至75.9%。
- 移除第一阶段（纯文本RL）会导致VL-RewardBench平均性能骤降6.9个百分点，证实大规模文本RL是多模态奖励建模的关键增益来源。
- 在图像生成基准GenAI-Bench上，MSRL将准确率从基线的70.2%提升至75.7%，且模型在多尺寸下均表现出持续的规模化特性。
- 引入的跨模态知识蒸馏（CMKD）和基于描述的RL有效弥合了任务与模态差异，消融实验显示移除第二阶段的描述-Based RL会导致1.6%~2.6%的性能下降。
---

# MSRL: Scaling Generative Multimodal Reward Modeling via Multi-Stage Reinforcement Learning

> [!tip] 核心洞察
> 偏好建模所需的核心推理能力可以从大量易于获取的纯文本数据中习得，并通过精心设计的多阶段训练以及跨模态知识蒸馏（CMKD）有效地迁移到多模态任务上。

| 字段 | 内容 |
|------|------|
| 中文题名 | MSRL：通过多阶段强化学习实现生成式多模态奖励建模的规模化扩展 |
| 英文题名 | MSRL: Scaling Generative Multimodal Reward Modeling via Multi-Stage Reinforcement Learning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.25108) · [Code](https://github.com/wangclnlp/MSRL) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | MSRL (Multi-Stage Reinforcement Learning) |
| Dataset | VL-RewardBench, Multimodal RewardBench, GenAI-Bench, Image Gen + Video Under. + Video Gen. |

> [!tip] 效果简介
> - VL-RewardBench 上，Avg. Accuracy (%) 75.9 vs 66.6 (+9.3)。
> - Multimodal RewardBench 上，Avg. Accuracy (%) 80.5 vs 76.2 (+4.3)。
> - GenAI-Bench (Image Generation) 上，Accuracy (%) 75.7 vs 70.2 (+5.5)。

## 概述

多模态奖励模型（Multimodal Reward Models, MRMs）是多模态大语言模型（MLLM）偏好对齐的关键组件，但其规模化训练长期受困于**多模态人类偏好标注数据极其稀缺且昂贵**这一核心瓶颈。现有的基于可验证奖励的强化学习（RLVR）训练范式直接依赖有限的多模态偏好数据，难以充分释放生成式MRM的潜力。

针对这一数据瓶颈，本文提出 **MSRL（Multi-Stage Reinforcement Learning）**，一种多阶段强化学习框架。其核心洞察在于：偏好建模所需的通用奖励推理能力可以从**大规模、易获取的纯文本偏好数据**中习得，并通过精心设计的课程式迁移机制有效注入多模态模型。MSRL通过“文本RL → 基于描述的RL → 全多模态RL”三阶段训练，配合跨模态知识蒸馏（CMKD），在几乎不增加多模态人工标注的前提下实现了生成式MRM性能的大幅跃升。

实验结果表明，在相同多模态标注预算下，MSRL将InternVL3.5-8B在VL-RewardBench上的平均准确率从生成式MRM基线的66.6%提升至**75.9%**，在图像生成基准GenAI-Bench上从70.2%提升至**75.7%**，并在4B和8B两个模型尺度上均表现出持续的规模化特性。消融实验进一步证实，移除纯文本RL阶段会导致6.9个百分点的性能骤降，验证了大规模文本监督是多模态奖励建模的关键增益来源。

## 背景与动机

多模态大语言模型（MLLM）的快速发展使得对齐人类偏好成为关键瓶颈。多模态奖励模型（MRM）作为偏好对齐的核心组件，负责评估模型输出的质量。然而，当前MRM的训练面临一个根本性矛盾：人类偏好标注数据——尤其是多模态场景下的成对偏好数据——极其稀缺且标注成本高昂。这一“数据瓶颈”直接制约了基于可验证奖励的强化学习（RLVR）训练范式的规模化扩展，使得生成式MRM的性能难以持续提升。

现有MRM主要分为两类：判别式MRM通过Bradley-Terry损失直接输出标量分数，生成式MRM则以自然语言形式直接预测偏好标签。尽管生成式MRM具备更强的可解释性和灵活性，但其训练范式——通常是在有限的多模态偏好数据上进行监督微调（SFT）后直接应用RLVR——并未从根本上解决数据稀缺问题。**R1-Reward**（Zhang et al., arXiv 2025）和**UnifiedReward**（Wang et al., 2025）等代表性工作虽然验证了RLVR在生成式MRM中的有效性，但它们的性能提升始终受限于多模态标注数据的规模。

MSRL的核心动机源于一个关键观察：偏好建模所需的核心推理能力——比较、分析和判断——本质上并不依赖于特定模态。大规模纯文本偏好数据中蕴含着丰富的偏好监督信号，这些信号能否被有效利用来增强多模态奖励建模？MSRL的回答是肯定的：通过“文本RL → 基于描述的RL → 全多模态RL”的课程式迁移机制，可以在几乎不增加多模态标注预算的前提下，将文本域习得的通用奖励推理能力有效迁移至多模态任务。

这一动机得到了初步实验的强力支持。如图1所示，充足的文本偏好数据能够驱动RLVR的规模化扩展（子图a），而多阶段RL设计则进一步将这种规模化收益传递至多模态生成式奖励模型（子图b）。在VL-RewardBench上，MSRL将InternVL3.5-8B的平均准确率从生成式MRM基线的66.6%大幅提升至75.9%（+9.3个百分点），并在图像生成基准GenAI-Bench上实现了70.2%到75.7%的显著提升。这些结果表明，跨模态偏好迁移不仅是可行的，而且具有极高的实际价值。

## 核心创新

MSRL的核心创新在于**将多模态奖励建模从“数据受限的单阶段训练”重构为“能力迁移的多阶段课程学习”**，从根本上改变了生成式MRM的训练范式。其关键设计可凝结为三个相互耦合的changed slots。

### 训练范式：从单阶段RLVR到三阶段课程学习

传统生成式MRM的训练范式（如**R1-Reward**，Zhang et al., arXiv 2025）是直接对有限的多模态偏好数据应用RLVR，这导致模型只能在稀缺的标注信号中挣扎，形成“数据瓶颈”。MSRL将这一范式彻底重构为三阶段课程：

1. **阶段一（纯文本RL）**：在40万条大规模文本偏好数据上进行SFT + RLVR，建立强泛化的文本奖励推理策略。此时视觉编码器和投影器被完全冻结，迫使模型专注于学习偏好推理的“元能力”。
2. **阶段二（基于描述的RL + CMKD）**：将多模态数据中的视觉输入替换为文本描述进行RL，并引入跨模态知识蒸馏（CMKD）将文本策略的推理能力迁移至多模态模型，同时增加任务识别奖励（$r_{\mathrm{task}}$）以弥合任务差异。
3. **阶段三（多模态RL）**：在约2万条原始多模态数据上进行最终的RLVR微调，使模型完全适应多模态任务。

这一课程设计的核心洞察是：**偏好建模所需的推理能力可以从廉价、丰富的文本数据中习得，并通过精心设计的迁移机制有效注入多模态模型**。消融实验提供了决定性证据——移除阶段一（纯文本RL）会导致VL-RewardBench平均性能骤降6.9个百分点（Table 4），证实大规模文本RL是多模态奖励建模的关键增益来源。

### 跨模态迁移机制：描述桥接与知识蒸馏

传统方法缺乏显式的跨模态迁移设计，模型被迫直接从多模态偏好数据中同时学习推理能力和模态理解。MSRL引入了两个互补的迁移机制：

- **基于描述的RL（Caption-Based RL）**：作为文本与多模态之间的中间步骤，将图像/视频替换为文本描述进行RL训练。这使模型能够在保留偏好推理能力的同时，逐步适应多模态任务的输入格式和输出要求。消融显示，移除阶段二会导致1.6%~2.6%的性能下降（Table 4），证实了其在桥接领域差异中的关键作用。
- **跨模态知识蒸馏（CMKD）**：从基于描述训练的教师模型中采样多条推理链（$\{o_1, o_2, \ldots, o_n\} \sim \pi_{\theta_{\mathrm{text}}}(\cdot \mid s, c)$），选择最优推理链作为学生模型的监督信号。这一设计实现了推理能力的可扩展对齐，无需额外的无标注偏好数据。

在偏好泛化阶段，caption:text混合比为4:1时取得最高准确率75.5，优于纯描述训练（74.6）和过于均衡的混合（1:1, 73.8）（Table 6），表明适度的文本数据混合有助于稳定训练。

### 奖励设计：引入任务识别信号

基线方法仅使用格式奖励与准确率奖励（$r_v(s, o) = r_{\mathrm{format}}(s, o) + r_{\mathrm{accuracy}}(s, o)$），这在多任务场景下缺乏对任务类型的显式引导。MSRL在阶段二和阶段三中额外引入任务识别奖励（$r_{\mathrm{task}}$），鼓励模型区分图像理解、图像生成、视频理解、视频生成等不同多模态任务类型。这一设计使模型能够在跨任务泛化时保持对任务上下文的敏感性，是CMKD有效发挥作用的重要辅助机制。

### 视觉模块训练策略：阶段性参数解冻

与通常所有参数全程参与训练的基线策略不同，MSRL在纯文本阶段冻结视觉编码器和投影器，仅在跨模态阶段（阶段二和阶段三）解冻。这一设计确保文本阶段学到的推理能力不会被视觉模块的随机梯度干扰，同时在后阶段允许视觉表征与推理策略进行协同适应。

## 整体框架

MSRL 提出了一种三阶段课程式训练范式，其核心思想是：**偏好建模所需的通用推理能力可以从大规模纯文本数据中习得，再通过渐进式跨模态迁移注入多模态奖励模型**，从而绕开多模态人类偏好标注稀缺且昂贵的“数据瓶颈”。

### 设计动机与瓶颈突破

传统的生成式多模态奖励模型（MRM）直接对有限的多模态偏好数据应用 RLVR（Reinforcement Learning with Verifiable Rewards）进行单阶段训练。由于多模态偏好标注成本极高，训练数据规模受限，导致 RLVR 的规模化扩展难以实现。MSRL 的关键突破在于识别出**偏好推理本身是一种跨模态可迁移的能力**——判断“哪个回答更好”所依赖的逻辑推理、标准权衡等核心技能，完全可以先在廉价且大规模存在的文本偏好数据上充分训练，再迁移至多模态场景。

### 三阶段课程架构

Figure 2 给出了 MSRL 的整体流程。训练依次经历三个阶段，每个阶段承担明确的迁移职责：

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/003_Figure_2.jpg]]
*Figure 2: An overview of the MSRL approach. We begin by applying RL to large-scale textual preference data (400k examples) to capture rich textual preferences. We then train an RL agent on caption-based data to generalize these preferences to multimodal tasks. During this stage, we also fine-tune the MRMs with CMKD to enhance the generalization. Subsequently, we perform RL with a limited amount of multimodal data to enable adaptation. Note that although the illustration uses image understanding as an example, MSRL is a general approach and can be applied to develop MRMs for arbitrary multimodal tasks*

**阶段 1：纯文本强化学习（Text-Only RL）**
在大规模文本偏好数据（约 40 万条）上先进行监督微调（SFT），使模型学会生成结构化的思维链输出并遵循格式要求；随后应用 RLVR 强化奖励推理能力。此阶段**冻结视觉编码器和投影器**的所有参数，仅训练语言部分，确保模型专注于学习通用的偏好推理策略，不受视觉模态噪声干扰。

**阶段 2：基于描述的 RL + 跨模态知识蒸馏（Caption-Based RL + CMKD）**
这是弥合文本与多模态之间“任务差异”和“模态差异”的关键中间步骤。具体做法是将多模态数据中的视觉输入（图像/视频）替换为文本描述，构造“基于描述”的偏好数据，使模型在保留文本推理能力的同时逐步适应多模态任务的多样格式。同时引入两项增强机制：
- **任务识别奖励**（$r_{\text{task}}$）：鼓励模型区分不同多模态任务类型（图像理解、视频理解、图像生成等），提升任务泛化能力。
- **跨模态知识蒸馏（CMKD）**：从阶段 1 的纯文本教师模型中采样多条推理链 $\{o_1, o_2, \ldots, o_n\} \sim \pi_{\theta_{\text{text}}}(\cdot \mid s, c)$，筛选高质量推理过程用于蒸馏多模态学生模型，实现推理能力的跨模态对齐。此阶段解冻视觉模块，使其开始参与训练。

**阶段 3：全多模态强化学习（Multimodal RL）**
在少量原始多模态偏好数据（约 2 万条）上进行最终的 RLVR 微调，使模型完全适应多模态输入，完成从文本到多模态的完整迁移闭环。

### 输入输出流

整个流程的输入输出定义统一遵循生成式 MRM 的范式（Table 1）：输入为拼接后的字符串 $s$，包含任务提示 $p$、多模态上下文 $x$ 以及候选回答 $y_a$、$y_b$；模型直接生成偏好判断（选择 A 或 B），并输出推理过程。训练信号来自可验证奖励 $r_v(s, o) = r_{\text{format}}(s, o) + r_{\text{accuracy}}(s, o)$，即格式奖励与准确率奖励之和，通过 GRPO 算法优化 RLVR 目标：

$$\mathcal{L}_{\mathrm{RLVR}} = -\mathbb{E}_{(p, x, y_a, y_b, l) \sim D_r, o \sim \pi_{\theta}} [r_v(s, o)] - \beta D_{\mathrm{KL}}(\pi_{\theta} || \pi_{\theta_{\text{old}}})$$

### 关键设计决策

消融实验验证了各阶段的不可替代性：移除阶段 1 会导致 VL-RewardBench 平均准确率骤降 6.9 个百分点，证实大规模文本 RL 是多模态奖励建模的核心增益来源；移除阶段 2 的基于描述的 RL 和 CMKD 会造成 1.6%–2.6% 的性能下降，说明该中间阶段在桥接文本与多模态领域差异中扮演关键角色。此外，在阶段 2 的偏好泛化训练中，caption:text 混合比为 4:1 时取得最优准确率（75.5），优于纯描述训练（74.6）和过于均衡的混合（1:1, 73.8），表明以描述数据为主、辅以少量文本数据的混合策略最有利于跨模态迁移。

### 补充图表

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/002_Figure_1.jpg]]
*Figure 1: Illustration of our multi-stage RL approach. SubfiguFigure 1. Illustration of our multi-stage RL approach. Subfigure Figure 1. Illustration of our multi-stage RL approach. SubfiguFigure 1. Illustration of our multi-stage RL approach. Subfigure(a) shows that abundant textual preference data can facilitate sca(a) shows that abundant textual preference data can facilitate scal-(a) shows that abundant textual preference data can facilitate sc(a) shows that abundant textual preference data can facilitate scal-able RL. Subfigure (b) demonstrates that we can effectively scaable RL. Subfigure (b) demonstrates that we can effectively scale able RL. Subfigure (b) demonstrates that we can effectivelyR...*

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/001_Figure.jpg]]
*Figure: (a) Learning Curves across Modalities*

## 核心模块与公式推导

MSRL 的核心设计围绕一个因果性调控旋钮展开：**偏好建模所需的推理能力可以从大规模纯文本数据中习得，并通过三阶段课程式迁移注入多模态奖励模型**。该方法将训练流程拆解为三个递进的模块，每个模块解决一个特定的瓶颈。

### 模块一：纯文本强化学习（Stage 1）

**目标**：利用大规模文本偏好数据（约40万条）建立强泛化的奖励推理策略，突破多模态人类偏好标注稀缺的“数据瓶颈”。

**流程**：首先对基础 MLLM 进行监督微调（SFT），使其学会生成结构化的思维链输出并遵循格式要求（如正确放置 `<think>` 和 `<answer>` 标签）。随后，在文本偏好数据上应用基于可验证奖励的强化学习（RLVR），其核心优化目标为：

$$\mathcal{L}_{\mathrm{RLVR}} = -\mathbb{E}_{(p, x, y_a, y_b, l) \sim D_r, o \sim \pi_{\theta}} \big[ r_v(s, o) \big] - \beta D_{\mathrm{KL}}(\pi_{\theta} \| \pi_{\theta_{\mathrm{old}}})$$

其中，可验证奖励 $r_v(s, o)$ 由两部分组成：

$$r_v(s, o) = r_{\mathrm{format}}(s, o) + r_{\mathrm{accuracy}}(s, o)$$

- **$r_{\mathrm{format}}$**：格式奖励，检查输出结构是否符合预定义模板（如是否包含正确的标签对）。
- **$r_{\mathrm{accuracy}}$**：准确率奖励，判断模型预测的偏好标签 $l$ 是否与真实偏好一致。
- **$\beta D_{\mathrm{KL}}$ 项**：KL 散度惩罚，防止策略 $\pi_{\theta}$ 偏离旧策略 $\pi_{\theta_{\mathrm{old}}}$ 过远，实践中使用 GRPO 算法进行优化。

**关键设计**：在此阶段，视觉编码器和投影器的所有参数被冻结，确保模型专注于文本推理能力的构建，避免视觉模块的干扰。

### 模块二：基于描述的强化学习与跨模态知识蒸馏（Stage 2）

**目标**：弥合“任务差异”（文本偏好 vs. 多模态偏好）和“模态差异”（纯文本 vs. 图文混合），将阶段一习得的推理能力迁移到多模态场景。

**子模块 2.1：基于描述的偏好泛化**

将多模态偏好数据中的图像/视频输入替换为其文本描述（caption），构造“基于描述的数据”，在此数据上进行 RL。这一设计使得模型可以在不接触原始视觉信号的情况下，先学会处理多模态任务的偏好判断逻辑。同时，引入**任务识别奖励 $r_{\mathrm{task}}$**，鼓励模型区分不同的多模态任务类型（如图像理解、视频生成等），增强任务间泛化能力。

**子模块 2.2：跨模态知识蒸馏（CMKD）**

为解决模态差异，CMKD 从阶段一训练出的纯文本教师模型 $\pi_{\theta_{\mathrm{text}}}$ 中采样多条推理链：

$$\{o_1, o_2, \ldots, o_n\} \sim \pi_{\theta_{\mathrm{text}}}(\cdot \mid s, c)$$

其中 $s$ 为偏好样本的文本部分，$c$ 为对应的视觉描述。随后，从采样结果中选择高质量的推理链，将其作为监督信号对多模态学生模型进行微调。这一蒸馏过程将纯文本策略的推理能力对齐到多模态表示空间中，且无需额外的无标注偏好数据。

**关键设计**：此阶段解冻视觉编码器和投影器，使其开始参与训练。同时，caption 与 text 数据的混合比被证明是一个敏感超参数——消融实验显示 4:1 的比例取得最优准确率 75.5，优于纯描述训练（74.6）和 1:1 混合（73.8）。

### 模块三：多模态强化学习（Stage 3）

**目标**：在有限的多模态偏好数据（约2万条）上进行最终的 RLVR，使模型完全适应原始多模态输入。

**流程**：此阶段直接使用原始多模态数据（包含图像/视频输入），沿用与阶段一相同的 RLVR 目标函数（含格式奖励与准确率奖励），对模型进行微调。由于前两个阶段已构建了强泛化的推理基座，此阶段仅需少量数据即可实现高效适应。

### 模块间因果链条

三个模块的递进关系构成了完整的因果链路：**阶段一**提供来自大规模文本数据的丰富监督信号，建立通用奖励推理能力（消融实验中移除阶段一导致 VL-RewardBench 性能骤降 6.9 个百分点）；**阶段二**通过描述替换和知识蒸馏将文本能力桥接到多模态领域（移除阶段二导致 1.6%~2.6% 的性能下降）；**阶段三**在真实多模态数据上完成最终适配。这一设计使得 MSRL 在与基线使用**完全相同**的多模态标注预算下，将 InternVL3.5-8B 在 VL-RewardBench 上的平均准确率从 66.6% 提升至 75.9%。

### 补充图表

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/004_Table_1.jpg]]
*Table 1: Description of different multimodal tasks for generative MRMs. Templates for each task are provided in Appendix A*

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/007_Figure.jpg]]
*Figure: (b) In Stage 3, we train the model using 20k multimodal preference examples*

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/011_Figure_4.jpg]]
*Figure 4: Template used for the image understanding task*

## 实验与分析

### 核心瓶颈与实验动机

多模态人类偏好标注数据极其稀缺且昂贵，导致基于可验证奖励的强化学习（RLVR）训练难以规模化，形成了“数据瓶颈”，阻碍了生成式多模态奖励模型（MRM）的性能提升。MSRL的核心假设是：偏好建模所需的核心推理能力可以从大量易于获取的纯文本数据中习得，并通过精心设计的多阶段课程式迁移机制有效地迁移到多模态任务上。实验部分围绕这一假设展开，从主结果、消融分析、规模化特性三个维度进行验证。

### 主实验结果

#### VL-RewardBench 与 Multimodal RewardBench

**Table 2** 展示了 MSRL 与各类基线在 VL-RewardBench 和 Multimodal RewardBench 上的准确率对比。以 InternVL3.5-8B 为骨干模型，MSRL 在 VL-RewardBench 上取得了 75.9% 的平均准确率，相比使用相同多模态偏好数据训练的生成式 MRM 基线（66.6%）提升了 **9.3 个百分点**；在 Multimodal RewardBench 上，MSRL 达到 80.5%，较同一基线（76.2%）提升了 4.3 个百分点。

在 4B 尺度上，MSRL 同样展现出显著优势：VL-RewardBench 平均准确率达到 69.7%，较生成式 MRM 4B 基线（60.5%）提升了 9.2 个百分点。这表明 MSRL 的收益在不同模型规模下具有一致性。

值得注意的是，MSRL 在保持与基线完全相同的多模态标注预算的前提下，仅额外引入了不涉及多模态人工标注的纯文本偏好数据和基于描述的构造数据，即实现了上述提升。

#### 图像生成、视频理解与视频生成任务

**Table 3** 进一步验证了 MSRL 在视觉生成任务上的泛化能力。在图像生成基准 GenAI-Bench 上，MSRL 8B 将准确率从基线的 70.2% 提升至 75.7%（+5.5%）。在图像生成、视频理解、视频生成三类任务的平均准确率上，MSRL 达到 80.7%，较判别式 MRM 8B 基线的 73.7% 提升了 **7.0 个百分点**。这表明通过文本 RL 习得的奖励推理能力能够有效泛化到超出训练分布的生成类任务。

#### 与外部开源模型的对比

在 VL-RewardBench 上，MSRL 8B（75.9%）显著优于已有的开源生成式 MRM，包括 **R1-Reward**（Zhang et al., arXiv 2025）和 **UnifiedReward**（Wang et al., 2025）。在 Multimodal RewardBench 上，MSRL 同样保持领先。此外，采用多数投票（voting@16）能够进一步带来 1.0~1.5 个百分点的平均增益。

### 消融实验：各训练阶段的贡献

**Table 4** 通过逐步移除各训练阶段，量化了每个阶段对最终性能的贡献。

**移除第一阶段（纯文本 RL）** 导致 VL-RewardBench 平均准确率骤降 **6.9 个百分点**，这是所有消融项中降幅最大的。该结果直接证实：大规模文本偏好数据中蕴含的丰富监督信号是多模态奖励建模的关键增益来源。值得注意的是，移除第一阶段的同时也移除了 SFT 冷启动步骤，因此该降幅反映了文本 RL 与 SFT 初始化共同缺失的代价。

**移除第二阶段（基于描述的 RL + CMKD）** 导致性能下降 1.6% 至 2.6%。虽然降幅小于第一阶段，但该阶段在桥接文本与多模态领域差异中扮演着不可替代的角色——它通过将视觉输入替换为文本描述来弥合模态鸿沟，同时利用跨模态知识蒸馏（CMKD）将纯文本策略的推理能力迁移到多模态模型。若直接跳过第二阶段、从文本 RL 跳转到全多模态 RL，模型将面临任务格式与模态分布的双重偏移，性能损失在所难免。

**移除第三阶段（多模态 RL）** 同样会导致性能下降，因为模型缺乏对真实多模态输入的最终适应。但降幅相对较小，说明前两个阶段已经习得了大部分可迁移的奖励推理能力。

### 偏好泛化阶段的混合比消融

**Table 6** 展示了第二阶段中 caption 数据与 text 数据不同混合比例的影响。当 caption:text 混合比为 **4:1** 时，取得最高准确率 75.5，优于纯描述训练（1:0，74.6）和过于均衡的混合（1:1，73.8）。这一结果表明：基于描述的 RL 是偏好泛化的主体驱动力，但保留少量文本数据有助于维持文本推理能力的稳定性，防止灾难性遗忘。过高的文本比例（如 1:1）则会稀释描述训练的跨模态桥接效果。

### 规模化特性

**Figure 3** 展示了在 VL-RewardBench 上，MSRL 性能随文本偏好数据量增加而持续提升的规模化曲线。这一趋势验证了论文的核心洞察：通过大规模文本 RL 习得的奖励推理能力可以有效地转化为多模态奖励建模的增益，且该增益随文本数据规模单调递增。结合 Figure 1 中不同模型尺度的学习曲线，MSRL 在 1B 到 14B 骨干上均表现出持续的规模化特性，且更大模型从文本 RL 中获益更为显著。

### 公平性说明

所有自训基线（判别式 MRM、生成式 MRM）均使用与 MSRL 完全相同的一组多模态偏好数据进行训练。外部开源模型（如 R1-Reward、UnifiedReward、LLaVA-Critic）的结果优先采用原论文报告的数字或直接使用其公开模型进行评测。不同尺度的 InternVL3.5 骨干模型均进行了公平对比，并报告了参数量、训练设置等信息。

### 失败模式与局限性

尽管 MSRL 取得了显著提升，但仍存在以下局限：

1. **多模态数据依赖未完全消除**：MSRL 仍然需要一定数量的多模态偏好数据（实验中约 2 万条，见 **Table 5**），无法完全脱离多模态标注。对于标注成本极高的任务场景，这一需求仍可能构成瓶颈。

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/009_Table_5.jpg]]
*Table 5: Dataset statistics used in Stage 2 and Stage 3*

2. **描述质量敏感性**：跨模态知识蒸馏的性能依赖于描述质量（实验中由 GPT-5 生成）以及教师模型的推理质量。若描述不准确或遗漏关键视觉细节，可能引入噪声并损害蒸馏效果。

3. **骨干模型验证范围有限**：目前主要在 InternVL3.5 骨干上进行了验证，尚未在大规模 MLLM（如超过 14B 的模型）或更多样的架构上进行充分测试，跨架构泛化性有待进一步确认。

4. **训练流程复杂度**：三阶段训练流程引入了额外的超参数（如混合比、任务奖励权重等），调参成本较高，且多阶段训练的端到端可微融合仍是一个开放问题。

### 补充图表

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/005_Table_2.jpg]]
*Table 2: Accuracies (%) on VL-RewardBench and Multimodal RewardBench. The best result in each group is shown in bold. Results marked with † are taken from Wang et al. [42] on VL-RewardBench, while those marked with ‡ for both VL-RewardBench and Multimodal RewardBench are from Zhang et al. [54]. All remaining baseline results are obtained by their publicly available models. For Multimodal RewardBench, the “Other” column reports the average accuracy across the general and reasoning subsets*

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/006_Table_3.jpg]]
*Table 3: Accuracies (%) on image generation, video understanding, and video generation tasks. Results marked with † are taken from Wang et al. [42]. All remaining baseline results are obtained by their publicly available models*

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/008_Figure_3.jpg]]
*Figure 3: Performance scaling with different amounts of textual preference data on the VL-RewardBench*

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/010_Table_6.jpg]]
*Table 6: Performance of preference generalization under different caption-to-text mixing ratios. The ratio “1:0” indicates that Stage 2 training uses only caption-based data, with no text-only preference data mixed in*

![[assets/figures/papers/paper_list_l2696_https_arxiv_org_abs_2603_25108/figures/017_Figure_9.jpg]]
*Figure 9: A case study illustrating the rationale generated by MSRL (8B backbone) for the image generation preference task. Image B is identified as the superior output because it effectively captures the prompt’s request for a “ruined stone thoroughfare” and “epic fantasy style” with dramatic lighting. In contrast, Image A is critiqued for missing the “vibrant hues” and “otherworldly elements”, presenting a setting that is too somber and ceremonial. This highlights MSRL’s ability to evaluate semantic alignment and stylistic fidelity in text-toimage generation precisely*

## 方法谱系与知识库定位

### 1. 方法谱系：从判别式到生成式，再到规模化课程学习

MSRL 的提出根植于多模态奖励模型（MRM）从**判别式范式向生成式范式演进**的技术脉络中，并针对生成式 MRM 在规模化训练中遭遇的“数据瓶颈”给出了系统性解决方案。

**判别式 MRM** 采用 Bradley-Terry 损失直接输出标量分数，其训练目标为：

$$\mathcal{L}_{\mathrm{d}} = -\mathbb{E}_{(x, y_a, y_b) \sim D_r} [\log(\sigma(r_{\phi}(x, y_a) - r_{\phi}(x, y_b)))]$$

该类方法（如文中作为基线的 Discriminative MRM）依赖成对偏好标签学习分数差，但无法显式建模偏好推理过程，限制了其可解释性与泛化能力。

**生成式 MRM** 则将奖励建模转化为偏好标签的生成任务，通过监督微调（SFT）直接预测“A更好/B更好”的决策：

$$\mathcal{L}_{\mathrm{g}} = -\mathbb{E}_{(p, x, y_a, y_b, l) \sim D_r} [\log \pi_{\phi}(w = l | s)]$$

在此基础上，**RLVR（基于可验证奖励的强化学习）** 被引入以进一步提升生成式 MRM 的推理质量。其核心目标函数为：

$$\mathcal{L}_{\mathrm{RLVR}} = -\mathbb{E}_{(p, x, y_a, y_b, l) \sim D_r, o \sim \pi_{\theta}} [r_v(s, o)] - \beta D_{\mathrm{KL}}(\pi_{\theta} || \pi_{\theta_{\mathrm{old}}})$$

其中可验证奖励由格式奖励和准确率奖励相加构成：

$$r_v(s, o) = r_{\mathrm{format}}(s, o) + r_{\mathrm{accuracy}}(s, o)$$

这一训练范式在代表性工作 **R1-Reward**（Zhang et al., arXiv 2025）和 **UnifiedReward**（Wang et al., 2025）中已得到验证，但它们均直接对有限的多模态偏好数据应用 RLVR，受制于多模态人类偏好标注的稀缺与昂贵，规模化扩展遭遇瓶颈。

**MSRL 的核心突破**在于将训练范式从“单阶段多模态 RLVR”重构为“三阶段课程式迁移学习”：先利用大规模文本偏好数据（40万样本）习得通用奖励推理能力，再通过基于描述的 RL 和跨模态知识蒸馏（CMKD）将能力迁移至多模态任务，最终仅用少量多模态数据（约2万样本）完成适应。这一设计使得 MSRL 在**保持与基线完全相同的多模态标注预算**下，通过引入无需额外人工标注的文本数据和基于描述的构造数据，实现了显著的性能跃升。

### 2. 与现有工作的关系定位

MSRL 与以下工作的关系可明确界定：

- **相对于 R1-Reward 和 UnifiedReward**：MSRL 继承了生成式 MRM + RLVR 的技术路线，但通过多阶段课程学习和跨模态知识蒸馏，解决了这些方法在规模化扩展时面临的“数据瓶颈”。实验表明，在相同多模态数据下，MSRL 将 InternVL3.5-8B 在 VL-RewardBench 上的平均准确率从生成式 MRM 基线的 66.6% 大幅提升至 75.9%（Table 2）。

- **相对于 MM-RLHF-Reward 和 LLaVA-Critic**：这些开源多模态奖励/评判模型通常采用判别式架构或直接在有标注数据上微调。MSRL 的生成式范式结合多阶段 RL 训练，在 VL-RewardBench 和 Multimodal RewardBench 上均取得了显著更优的结果。

- **相对于判别式 MRM 基线**：在图像生成、视频理解、视频生成任务的平均准确率上，MSRL 达到 80.7%，而判别式 MRM 8B 基线仅为 73.7%（Table 3），验证了生成式范式在多模态奖励建模中的优势。

### 3. 适用边界与关键设计约束

MSRL 的有效性依赖于以下关键设计选择，这些选择同时也界定了其适用边界：

1. **文本数据规模依赖性**：第一阶段的大规模文本 RL 是 MSRL 的核心增益来源——消融实验显示，移除该阶段会导致 VL-RewardBench 平均性能骤降 6.9 个百分点（Table 4）。这意味着 MSRL 的收益上限受限于可用文本偏好数据的规模与质量。Figure 3 的规模化曲线证实了性能随文本数据量增加而持续提升的趋势。

2. **描述质量敏感性**：第二阶段的基于描述的 RL 和 CMKD 依赖 GPT-5 生成的图像/视频文本描述。消融实验表明，移除该阶段会导致 1.6%~2.6% 的性能下降（Table 4），证实了其桥接文本与多模态领域的关键作用。然而，若描述不准确或信息缺失，可能引入噪声并损害迁移效果。

3. **混合比调参需求**：在偏好泛化阶段，caption:text 混合比为 4:1 时取得最高准确率 75.5，优于纯描述训练（74.6）和过于均衡的混合（1:1, 73.8）（Table 6）。这表明混合比是一个需要精细调参的超参数，且最优值可能因任务和数据分布而异。

4. **多模态数据仍不可完全替代**：尽管 MSRL 大幅降低了对多模态标注的依赖，但第三阶段仍需约 2 万条多模态偏好数据来完成最终适应（Table 5），无法完全脱离多模态标注。

5. **骨干模型与规模限制**：目前 MSRL 主要在 InternVL3.5 系列（4B、8B）上进行了验证，尚未在大规模 MLLM（如超过 14B 的模型）或更多样的架构上进行充分测试。尽管在 1B 到 14B 骨干上观察到了持续的规模化特性（Figures 1 和 3），但更大规模下的收益趋势仍有待验证。

### 4. 局限与开放问题

**已识别的局限**：

- **训练流程复杂度**：三阶段训练引入了额外的超参数（如混合比、任务识别奖励权重 $r_{\mathrm{task}}$、CMKD 采样数量 $n$ 等），调参成本较高。
- **跨模态蒸馏的依赖链**：CMKD 的性能依赖于教师模型（纯文本训练的策略）的推理质量，若教师模型本身能力不足，蒸馏效果将受限。
- **视觉模块训练策略**：MSRL 在纯文本阶段冻结视觉编码器和投影器，仅在跨模态阶段解冻。这一策略虽保护了预训练视觉表征，但也可能限制了文本与视觉模态的早期融合机会。

**开放问题**：

1. **模态泛化能力**：MSRL 的跨模态迁移策略（文本→基于描述→全多模态）能否推广到音频、触觉等其他模态的更通用多模态奖励建模？这需要验证 CMKD 机制在不同模态间的有效性。

2. **无标注多模态数据的利用**：当前 CMKD 依赖描述质量，能否利用大量无标注的多模态数据（如仅图文对而无偏好标签）通过自监督或对比学习进一步增强跨模态迁移效果？

3. **规模化瓶颈**：在更大的模型规模（如 70B+）和数据规模下，三阶段的收益是否依然是单调递增的？第一阶段文本 RL 的规模化曲线（Figure 3）显示持续增长趋势，但可能存在尚未观测到的收益递减点。

4. **端到端训练的可行性**：当前三阶段训练是分离的，能否将多阶段训练融合为端到端可微的流程，减少调参复杂度和训练时间？

5. **推理效率**：MSRL 采用生成式范式，推理时需自回归生成推理链和偏好决策。文中提到多数投票（voting@16）可带来 1.0~1.5 个百分点的增益（Table 2, Table 3），但推理成本也相应增长 16 倍。如何在推理效率与准确率之间取得更优的权衡，仍是实际部署中需要解决的问题。

## 原文 PDF

![[paperPDFs/CVPR_2026/MSRL_Scaling_Generative_Multimodal_Reward_Modeling_via_Multi_Stage_Reinforcement_Learning.pdf]]
