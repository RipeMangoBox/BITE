---
title: "LongPerceptualThoughts: Distilling System-2 Reasoning for System-1 Perception"
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/LongPerceptualThoughts_Distilling_System_2_Reasoning_for_System_1_Perception.pdf
project_link: https://qwenlm.github.io/blog/qwq-32b-preview/
code_link: null
aliases:
- LongPerceptualThoughts
tags:
- arxiv_2025
- topic/other_unclear
- topic/other_unclear/general
core_operator: 通过三阶段数据合成框架（从密集描述生成可验证多选题，提取简单CoT，再用推理模型扩展为长思维链）生成包含丰富认知行为的数据，并结合直接偏好优化（DPO）训练，可以显著提升VLM的感知推理性能。
primary_logic: 将前沿推理大模型（DeepSeek-R1）的复杂推理能力蒸馏到指令微调VLM中，同时让生成数据保持与目标模型输出分布接近，不仅提升了视觉中心任务的性能，还能泛化到文本推理任务。
claims:
- 所提出的三阶段框架能合成包含验证、回溯等行为的长思维链数据。
- 在5个视觉中心基准上平均提升+3.4个点，V* Bench提升+11.8个点。
- DPO训练比纯SFT更有效，且能缓解错误token的影响。
- 现有蒸馏数据集（Virgo, VLAA-thinking）反而导致性能下降，说明保持输出分布的重要性。
---

# LongPerceptualThoughts: Distilling System-2 Reasoning for System-1 Perception

> [!tip] 核心洞察
> 将前沿推理大模型（DeepSeek-R1）的复杂推理能力蒸馏到指令微调VLM中，同时让生成数据保持与目标模型输出分布接近，不仅提升了视觉中心任务的性能，还能泛化到文本推理任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | LongPerceptualThoughts：将系统2推理蒸馏到系统1感知 |
| 英文题名 | LongPerceptualThoughts: Distilling System-2 Reasoning for System-1 Perception |
| 会议/期刊 | arXiv 2025 |
| Links | [paper](https://arxiv.org/abs/2504.15362) · [paper](https://arxiv.org/abs/2502.13923) · [Project](https://qwenlm.github.io/blog/qwq-32b-preview/) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | LongPerceptualThoughts 三阶段数据合成与偏好优化框架 |
| Dataset | CV-Bench, V* Bench, MMVP, MMStar-V |

> [!tip] 效果简介
> - CV-Bench 上，Accuracy 76.61 vs 74.74 (+1.87)。
> - V* Bench 上，Accuracy 60.31 vs 48.51 (+11.80)。
> - MMVP 上，Accuracy 75.00 vs 73.67 (+1.33)。

## 概要

当前开源视觉语言模型（VLMs）在感知任务上的推理能力存在明显瓶颈：其思维链（Chain-of-Thought, CoT）通常浅层、线性且僵化，缺乏验证、回溯、子目标设定等系统2认知行为，难以应对需要深度视觉推理的复杂场景。本文提出 **LongPerceptualThoughts**，一个三阶段数据合成与偏好优化框架，旨在将前沿推理大模型的复杂推理能力蒸馏到指令微调VLM中，从而提升其系统1感知效率下的系统2推理质量。

核心方法分为三步：（1）利用LLM从密集图像描述生成可验证的多选题；（2）由目标VLM提取简单CoT；（3）通过推理大模型（DeepSeek-R1-Distill-Qwen-32B）将简单CoT扩展为包含丰富认知行为的长思维链。在此基础上，构造正确性与简洁性偏好对，先进行监督微调（SFT），再通过直接偏好优化（DPO）训练。

实验表明，在5个视觉中心基准上，该方法平均提升**+3.4个点**，其中在极具挑战性的 V* Bench 上提升高达**+11.8个点**。消融实验证实，DPO训练相比纯SFT将平均增益从+1.5点提升至+3.4点，且构造的偏好数据有效缓解了长思维链中错误token的负面影响。值得注意的是，直接使用现有蒸馏数据集（如Virgo、VLAA-thinking）反而导致视觉基准性能下降，凸显了保持输出分布与目标模型一致的重要性。此外，该方法在文本推理基准MMLU-Pro上也展现出良好的泛化能力。

本工作的核心洞察是：通过精心设计的合成框架，将推理大模型的复杂认知行为蒸馏到指令微调VLM中，不仅能显著提升视觉中心任务的性能，还能实现跨模态的推理能力迁移。

视觉语言模型（VLMs）在图像理解、描述和问答等任务上取得了显著进展，但其推理过程往往表现出“系统1”式的浅层、线性特征——模型倾向于直接给出答案，缺乏验证、回溯、子目标设定等“系统2”式的深度认知行为。这一局限在需要精细视觉感知和逻辑推理的复杂任务中尤为突出：开源VLMs生成的思维链（Chain-of-Thought, CoT）通常结构僵化，难以对中间步骤进行自我纠错或重新审视，导致在精细感知基准上的表现受限。

近年来，前沿推理大模型（如DeepSeek-R1）通过大规模强化学习展现出丰富的推理行为，但其推理能力主要集中于文本领域，且通常以闭源API或极大参数量模型的形式存在，难以直接部署到视觉感知任务中。一个自然的思路是将这些推理模型的“系统2”能力蒸馏到指令微调的VLM中，然而现有尝试面临两个关键障碍：

**第一，现有蒸馏数据集存在严重的领域偏移和可学习性差距。** 如**Virgo**（Du et al., 2025）和**VLAA-thinking**（Chen et al., 2025）等数据集虽然尝试从大模型蒸馏多模态推理数据，但实验表明，在这些数据集上微调反而导致视觉基准性能下降（如VLAA-thinking在5个视觉基准上的平均准确率仅为42.32%，远低于基座模型的58.47%）。其根本原因在于：这些数据由远超目标模型规模的推理模型生成，其输出分布与目标VLM存在显著不匹配，导致模型难以有效学习。

**第二，直接使用密集描述数据进行监督微调会破坏模型的指令遵循能力。** 在**DOCCI**（Onoe et al., 2024）等密集描述数据集上微调虽然看似提供了丰富的视觉信息，但实验表明这会急剧降低模型在视觉问答基准上的表现，因为纯描述任务与问答任务的输出分布差异过大。

针对上述瓶颈，本文提出**LongPerceptualThoughts**框架，核心动机是：**能否在保持输出分布与目标VLM接近的前提下，将前沿推理模型的复杂认知行为有效蒸馏到视觉感知任务中？** 为此，本文设计了三阶段数据合成管线，以密集图像描述为起点，通过“目标VLM生成简单CoT → 推理模型扩展为长思维链”的递进式策略，生成既包含验证、回溯等丰富认知行为、又与目标模型输出分布接近的训练数据，并结合直接偏好优化（DPO）训练，实现对VLM感知推理能力的系统性提升。

## 核心方法与创新机理

### 问题瓶颈：VLM 感知推理的“浅层思维”困境

当前开源视觉语言模型（VLMs）在视觉感知任务上的思维链（CoT）普遍呈现**线性、僵化的结构**，缺乏验证、回溯、子目标设定等系统2认知行为。这一瓶颈导致模型在面对需要精细视觉定位或复杂空间推理的任务时表现受限。如 **Figure 1** 所示，开源 VLM 生成的 CoT 往往是单向推演，而前沿推理模型（如 Gemini 2.0 Flash Thinking）则展现出丰富的认知行为模式。LongPerceptualThoughts 的核心创新正是围绕**如何将系统2推理能力蒸馏到系统1感知模型**这一因果调控点展开。

### 关键创新一：三阶段数据合成框架（Ask, Think, and Think Harder）

现有的多模态推理数据集（如 **Virgo** (Du et al., 2025)、**VLAA-thinking** (Chen et al., 2025)）直接从大模型蒸馏推理轨迹，但存在严重的领域偏移（domain mismatch）和可学习性差距（learnability gap），导致微调后视觉基准性能反而下降（见 Table 1）。LongPerceptualThoughts 提出了截然不同的数据生成策略，其核心在于**保持生成数据与目标模型输出分布接近**：

- **Stage 1（Ask）**：使用 LLM（gpt-4o-mini）从密集图像描述（DOCCI 数据集，Onoe et al., 2024）生成可验证的多选题。这一步将纯文本描述转化为具有明确答案的视觉推理问题，为后续 CoT 生成提供可验证的监督信号。
- **Stage 2（Think）**：使用**目标 VLM 本身**（Qwen2.5-VL-7B-Instruct）对图像和多选题生成简单思维链。这一步确保初始 CoT 的风格和分布与最终要微调的模型一致，避免了直接使用外部模型带来的分布偏移。
- **Stage 3（Think Harder）**：使用推理 LLM（DeepSeek-R1-Distill-Qwen-32B）将简单思维链扩展为包含验证、回溯、子目标设定等复杂认知行为的长思维链。关键设计是**以简单 CoT 为前缀**并附加提示词（如“Wait,”），引导推理模型在已有推理基础上进行深化和反思，而非从零生成。

这一“Ask → Think → Think Harder”的三阶段设计（见 **Figure 2**）形成了一个闭环：从描述到问题，从问题到初步推理，再从初步推理到深度思考，每一步都保证与目标模型的输出空间保持兼容。

### 关键创新二：基于正确性与简洁性的偏好优化（DPO）

传统方法仅使用监督微调（SFT）训练长 CoT 数据，但合成数据中不可避免地包含错误 token 和冗余推理。LongPerceptualThoughts 在 SFT 基础上引入**直接偏好优化（DPO）**，并构造了两类偏好对：

- **正确性偏好对**：$(z_1^+, a_1^+) \succ (z_1^-, a_1^-)$ 和 $(z_1^- \oplus z_2^+, a_2^+) \succ (z_1^-, a_1^-)$。前者确保正确推理优于错误推理；后者鼓励模型在初始错误后通过反思纠正——即使第一步错了，经过推理模型修正的完整轨迹仍然优于未纠正的错误轨迹。这一设计显式地**增加了模型在负上下文条件下生成正响应的概率**，从而缓解错误 token 的级联影响。
- **简洁性偏好对**：$(z_1^+, a_1^+) \succ (z_1^+ \oplus z_2^+, a_2^+)$。在保持正确性的前提下，简洁推理优于冗长推理，鼓励模型减少不必要的冗余 token。

实验证据表明，仅 SFT 训练带来平均 +1.5 点的提升，而加入 DPO 后将增益扩大到 **+3.4 点**（Table 1），且一致性更好。这表明偏好优化不仅提升了性能，还使得模型在测试时更有效地分配计算资源。

### 关键创新三：输出分布对齐的蒸馏策略

与直接使用 Virgo 或 VLAA-thinking 等数据集进行蒸馏不同，LongPerceptualThoughts 的**每个数据点都经过目标 VLM 的“校准”**——Stage 2 提取的简单 CoT 来自目标模型本身，Stage 3 的扩展以这些 CoT 为前缀。这一设计使得合成数据与目标模型的输出分布保持接近，从而避免了领域偏移。实验证实，在 Virgo 或 VLAA-thinking 上微调反而导致视觉基准性能下降（Table 1, Table 4），而 LongPerceptualThoughts 不仅在视觉任务上提升显著，还能**泛化到纯文本推理任务 MMLU-Pro**，获得 +2 点的提升（Table 2），说明引入的复杂推理结构具有跨模态迁移能力。

### 创新总结

| 创新维度 | 基线方法 | LongPerceptualThoughts |
|---------|---------|----------------------|
| 数据生成 | 直接从大模型蒸馏推理轨迹 | 三阶段合成：目标模型生成简单CoT → 推理模型扩展为长CoT |
| 输出分布 | 外部模型分布，存在领域偏移 | 以目标模型CoT为前缀，保持分布接近 |
| 训练策略 | 纯SFT | SFT预训练 + DPO偏好优化（正确性+简洁性） |
| 认知行为 | 浅层线性推理 | 验证、回溯、子目标设定等系统2行为 |
| 泛化能力 | 视觉任务可能倒退 | 视觉+3.4点，文本+2点 |

LongPerceptualThoughts 提出了一套三阶段的数据合成与偏好优化框架，旨在将前沿推理大模型的系统2推理能力蒸馏到指令微调的视觉语言模型（VLM）中。该框架的核心瓶颈在于：当前开源 VLM 的思维链（CoT）通常浅层且僵化，缺乏验证、回溯、子目标设定等复杂认知行为，限制了其在复杂视觉感知任务上的表现。

### 三阶段数据合成流水线

整个数据合成流程遵循“提问—思考—深度思考”（Ask, Think, and Think Harder）的递进逻辑（图2），三个阶段依次衔接：

**阶段1：密集描述到多选题生成。** 以现成的密集图像描述数据集（DOCCI，Onoe et al., 2024）为起点，使用 LLM（gpt-4o-mini）将每张图像的密集描述自动转换为可验证的多选题（MCQ）。这一步骤将非结构化的描述文本转化为具有明确正确答案的评估形式，为后续的思维链提取和扩展提供了可验证的监督信号。

**阶段2：简单思维链提取。** 将图像和阶段1生成的多选题输入目标 VLM（Qwen2.5-VL-7B-Instruct），让其生成推理过程与最终答案。此时提取到的思维链通常呈现浅层、线性的推理结构，缺乏深度认知行为——这正是本工作试图解决的核心问题。

**阶段3：思维扩展。** 将阶段2得到的简单思维链作为前置条件，拼接一个微妙的提示词（如“Wait,”），输入推理大模型（DeepSeek-R1-Distill-Qwen-32B），使其继续生成长思维链。该阶段的提示结构为：

$$\text{User: } c \oplus q \quad \text{Assistant: } \langle\text{think}\rangle \oplus z_1 \oplus m$$

其中 $c$ 为密集描述，$q$ 为问题，$z_1$ 为阶段2的简单思维链，$m$ 为触发深度推理的标记词。推理模型在此基础上扩展出包含验证、回溯、子目标设定等丰富认知行为的长思维链。

### 数据集构建与训练策略

三阶段合成完成后，框架根据正确性和简洁性两个维度构造训练数据：

**SFT 数据集**（30,295 条样本）：收集所有最终导向正确答案的思维链序列，包括阶段2直接正确的推理 $(z_1^+, a_1^+)$、阶段3扩展后正确的推理 $(z_1^+ \oplus z_2^+, a_2^+)$，以及初始错误但经反思纠正的推理 $(z_1^- \oplus z_2^+, a_2^+)$。

**偏好数据集**（17,208 对）：构造两类偏好对——
- **正确性偏好**：正确推理优于错误推理 $(z_1^+, a_1^+) \succ (z_1^-, a_1^-)$；经过反思纠正的错误推理优于未纠正的错误推理 $(z_1^- \oplus z_2^+, a_2^+) \succ (z_1^-, a_1^-)$。
- **简洁性偏好**：简洁的正确推理优于冗长的正确推理 $(z_1^+, a_1^+) \succ (z_1^+ \oplus z_2^+, a_2^+)$，鼓励模型在保持正确性的前提下减少冗余输出。

训练采用两阶段策略：首先在 SFT 数据集上进行全参数监督微调，随后在偏好数据集上进行直接偏好优化（DPO）。所有实验均基于 Qwen2.5-VL-7B-Instruct 基座模型，使用 LLaMA-Factory 进行全参数微调，超参数通过验证集早停机制统一调优。

### 框架设计的核心洞察

该框架的有效性源于两个关键设计选择：（1）通过推理大模型扩展简单思维链，引入了复杂的推理结构，提升了基座模型的通用推理能力；（2）数据生成过程中使用目标 VLM 自身的输出作为思维扩展的起点，使得合成数据与目标模型的原始输出分布保持接近，避免了现有蒸馏数据集（如 Virgo、VLAA-thinking）因领域偏移和可学习性差距导致的性能倒退。

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2504_15362/figures/002_Figure_2.jpg]]
*Figure 2: Ask, Think, and Think Harder: The three stages to synthesize long CoT data for vision-centric tasks. Assuming the access to an image and its associated dense caption, we first ask an LLM to convert dense captions to multiple-choice questions. In Stage 2, we extract simple CoT from VLM. These simple CoTs typically exhibits shallow and rigid reasoning, especially in vision-centric tasks. Therefore, in Stage 3, we precondition a reasoning LLM with these simple CoTs and append a subtle cue, e.g., “Wait,”, to elicit more diverse long CoTs*

### 三阶段数据合成框架

LongPerceptualThoughts 的核心是一个三阶段数据合成流水线，它从密集图像描述出发，逐步生成包含复杂认知行为的长思维链数据。该框架的三个阶段分别为：

**Stage 1：密集描述到多选题生成模块。** 该模块使用一个纯文本大语言模型（gpt-4o-mini），将 DOCCI 数据集（Onoe et al., 2024）中的密集图像描述转换为可验证的多选题。其关键设计在于：多选题的答案可以直接从描述文本中推断，从而为后续思维链的正确性提供自动验证信号。

**Stage 2：简单 CoT 提取模块。** 该模块使用目标视觉语言模型 Qwen2.5-VL-7B-Instruct，输入图像和 Stage 1 生成的多选题，要求模型生成推理过程和最终答案。这一阶段产生的思维链通常呈现浅层、线性的推理结构，缺乏验证、回溯等高级认知行为。

**Stage 3：思维扩展模块。** 这是框架的核心创新所在。该模块使用推理大语言模型 DeepSeek-R1-Distill-Qwen-32B，将 Stage 2 的简单思维链扩展为包含丰富认知行为的长思维链。具体做法是：将密集描述 $c$、问题 $q$、简单 CoT $z_1$ 以及一个微妙的提示词（如“Wait,”）拼接后，让推理模型继续生成。其提示结构可形式化为：

$$\text{User: } c \oplus q \quad \text{Assistant: } \langle\text{think}\rangle \oplus z_1 \oplus m$$

其中 $m$ 是触发深度反思的提示词，推理模型在此基础上生成扩展后的长思维链。

### 数据集构建与偏好优化模块

生成长思维链数据后，框架进一步构造监督微调（SFT）数据集和偏好数据集，以支持两阶段训练。

**长思维链的形式化定义。** 一条长思维链被定义为多个中间思考单元的串联：

$$\Psi_Z := z_1 \oplus z_2 \oplus \dots$$

其中每个 $z_i$ 是一个中间推理步骤，$\oplus$ 表示拼接操作。最终答案记为 $a$，整个数据格式为 `<think> thought </think> <answer> answer </answer>`。

**偏好数据对定义。** 给定图像 $v$、问题 $q$、思维链序列 $Z$ 和答案 $a$，偏好关系定义为：

$$(v, q, Z^+, a^+) \succ (v, q, Z^-, a^-)$$

即正确的推理轨迹和答案优于错误的轨迹。

**SFT 数据集构造。** SFT 数据集收集所有导致最终正确答案的思维链，包括三种情况：

$$(z_1^+, a_1^+), (z_1^+ \oplus z_2^+, a_2^+), (z_1^- \oplus z_2^+, a_2^+)$$

其中 $z_1^+$ 表示 Stage 2 中 VLM 给出的正确思维链，$z_1^-$ 表示错误思维链，$z_2^+$ 表示 Stage 3 中推理模型给出的纠正性思维链。第三种情况尤为关键：它保留了“初始错误—经反思纠正”的完整推理轨迹，使模型能够学习从错误中恢复的能力。

**正确性偏好对。** 基于正确性构造的偏好对有两类：

$$(z_1^+, a_1^+) \succ (z_1^-, a_1^-)$$

$$(z_1^- \oplus z_2^+, a_2^+) \succ (z_1^-, a_1^-)$$

第一类表示正确推理优于错误推理；第二类表示经过反思纠正的错误推理轨迹优于未纠正的错误推理。第二类偏好对的设计意图是：在给定错误上下文 $z_1^-$ 的条件下，模型应自然提高生成纠正性响应 $z_2^+$ 的概率，即 $P(z_2^+, a_2^+ | z_1^-)$。

**简洁性偏好对。** 为鼓励高效推理，框架还引入了简洁性偏好：

$$(z_1^+, a_1^+) \succ (z_1^+ \oplus z_2^+, a_2^+)$$

即简洁的正确推理优于冗长的正确推理，促使模型在保持正确性的前提下减少冗余 token。

### 训练模块

训练分为两个阶段。首先在 LongPerceptualThoughts SFT 数据集（共 30,295 个样本）上进行全参数微调，基座模型为 Qwen2.5-VL-7B-Instruct，使用 LLaMA-Factory 框架。随后在构造的偏好数据集（共 17,208 对）上进行直接偏好优化（DPO），通过正确性偏好缓解长思维链中不可避免的错误 token 的影响，同时通过简洁性偏好抑制过度思考。

## 实验与关键发现

### 主实验结果

本节报告 LongPerceptualThoughts 在五个视觉中心基准上的性能，并与免训练方法、现有多模态推理数据集进行对比。所有实验均基于相同的基座模型 **Qwen2.5-VL-7B-Instruct**，采用全参数微调框架 LLaMA-Factory，评估时统一使用 greedy decoding 并将图像缩放至最长边 512 像素。

**Table 1** 汇总了核心结果。我们将方法分为三组：(1) 免训练方法（包括基座模型的零样本 CoT 基线 Internal Thinking CoT）；(2) 现有多模态推理数据集（DOCCI、Virgo、VLAA-thinking）；(3) 本文提出的 LongPerceptualThoughts。

关键发现如下：

- **LongPerceptualThoughts SFT+DPO 在五个基准上平均准确率达到 61.87%，相较基座模型提升 +3.4 个百分点。** 其中，在具有挑战性的 **V\* Bench** 上提升最为显著，达 **+11.80 个百分点**（从 48.51 到 60.31），表明长思维链中的验证、回溯等认知行为对需要精细视觉定位的任务尤为有效。
- **仅使用 SFT 的平均提升为 +1.5 个百分点**，而加入 DPO 后将增益扩大至 +3.4 个百分点，说明偏好优化在纠正错误 token 和鼓励高效推理方面发挥了关键作用。
- **直接微调 DOCCI 密集描述数据导致性能急剧下降**（平均 52.67，低于基座模型的 58.47），证实纯描述数据会破坏模型的指令遵循能力。
- **使用 Virgo 或 VLAA-thinking 等现有蒸馏数据集反而造成性能倒退**：Virgo 平均 56.31，VLAA-thinking 平均 56.60，均低于基座模型。这归因于领域偏移（domain mismatch）和可学习性差距（learnability gap）——这些数据集由远大于目标模型的推理模型生成，其输出分布与 Qwen2.5-VL-7B-Instruct 差异过大，导致直接微调时模型难以有效吸收其中的推理模式。

各基准的详细提升如下：

| 基准 | 基座模型 | LongPerceptualThoughts (SFT+DPO) | 提升 |
|------|---------|--------------------------------|------|
| CV-Bench | 74.74 | 76.61 | +1.87 |
| V\* Bench | 48.51 | 60.31 | +11.80 |
| MMVP | 73.67 | 75.00 | +1.33 |
| MMStar-V | 63.73 | 64.00 | +0.27 |
| MME-RealWorld-V | 31.68 | 33.45 | +1.77 |
| **平均** | **58.47** | **61.87** | **+3.40** |

### 文本推理的分布外泛化

**Table 2** 展示了在纯文本推理基准 MMLU-Pro 上的分布外（OOD）评估结果。尽管 LongPerceptualThoughts 完全基于视觉任务合成，微调后的模型在 MMLU-Pro 上仍获得约 **+2 个百分点**的提升。这一跨模态泛化能力支持了本文的核心假设：长思维链引入的复杂推理结构（验证、回溯、子目标设定等）提升的是模型的通用推理能力，而非仅针对视觉任务的表层模式。

### 消融实验与失败模式分析

#### DPO 的作用机制

仅 SFT 带来 +1.5 点的平均提升，而 SFT+DPO 将增益推至 +3.4 点。DPO 的有效性源于两个精心设计的偏好对类型：

- **正确性偏好对**：$(z_1^+, a_1^+) \succ (z_1^-, a_1^-)$ 和 $(z_1^- \oplus z_2^+, a_2^+) \succ (z_1^-, a_1^-)$，使模型学习偏好正确答案及经过反思纠正的推理轨迹，从而自然提升在负面对上文条件下生成正面响应的概率 $P(z_2^+, a_2^+ | z_1^-)$。
- **简洁性偏好对**：$(z_1^+, a_1^+) \succ (z_1^+ \oplus z_2^+, a_2^+)$，鼓励模型在保持正确性的前提下减少冗余推理。**Table 1** 中 DPO 模型在响应长度与性能之间取得了更好的平衡（见 **Fig. 3c**），而 Virgo 和 VLAA-thinking 微调模型则表现出“过度思考”（over-thinking）——生成长文本但性能反而下降。

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2504_15362/figures/004_Table_1.jpg]]
*Table 1: Main results on five vision-centric benchmarks. We group the approaches into three categories: training-free methods, existing multimodal reasoning datasets, and our proposed LongPerceptualThoughts. On vision-centric tasks, fine-tuning on other multimodal reasoning datasets often leads to poorer performance, likely due to reduced instructionfollowing ability, domain mismatch, or an inability to capture the complex reasoning learned by larger models. In contrast, fine-tuning on LongPerceptualThoughts yields an average improvement of +1.5 points, and this gain increases to +3.4 points when using preference pairs. Notably, it achieves a 12-point improvement on the challenging V∗ Bench*

#### 现有数据集的失败原因

**Table 4** 报告了在 Virgo 和 VLAA-thinking 基础上尝试改进的结果，包括：(1) 增加 DOCCI 描述数据混合训练；(2) 仅使用其 CoT 部分进行训练。然而，这些尝试均未能恢复性能，甚至进一步恶化。这表明问题的根源在于这些数据集的**输出分布与目标 VLM 不匹配**——由大模型（如 DeepSeek-R1）生成的推理轨迹包含目标模型无法有效学习的模式和 token 分布，强行蒸馏反而引入噪声。

#### 直接微调 DOCCI 的失败

在 DOCCI 描述上直接微调导致平均性能下降约 5.8 点（从 58.47 到 52.67），且在所有五个基准上全面倒退。这说明单纯的图像描述数据缺乏问答结构和推理过程，破坏了模型在指令微调阶段获得的指令遵循能力。

### 响应长度与问题难度的自适应分配

**Fig. 4** 分析了 DPO 微调后模型在不同难度问题上的响应长度分布。有趣的是，模型自然地**为困难问题分配更多的测试时计算量**（更长的响应），而为简单问题生成更简洁的回答。这种自适应行为并非显式训练目标，而是长思维链数据中蕴含的推理模式使模型习得了根据问题复杂度调节推理深度的能力。问题难度通过基座模型的多次 rollout 结果确定（遵循 Lightman et al., 2024 的方法）。

### 认知行为分析

**Fig. 3a** 量化了不同模型思维链中的认知行为分布。开源 VLM（如 Qwen2.5-VL）的 CoT 呈现僵化的线性结构，缺乏验证、回溯、子目标设定等行为。相比之下，前沿推理模型（如 Gemini 2.0 Flash Thinking）和 LongPerceptualThoughts 数据集展现出丰富多样的认知行为谱系。**Fig. 3b** 显示 LongPerceptualThoughts 的 CoT 长度显著长于开源 VLM 的生成结果。

### 实验公平性说明

为确保对比的公平性，本研究采取了以下措施：
- 所有微调实验使用相同的基座模型 Qwen2.5-VL-7B-Instruct 和全参数微调框架。
- 超参数（学习率、训练轮次）均通过相同的验证集早停机制调优。
- 对比数据集在样本数量或训练配置上进行了公平控制：DOCCI 使用相同的 500 张图像，VLAA-thinking 抽样至 25k 样本。
- 评估统一使用 greedy decoding，图像预处理一致。

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2504_15362/figures/005_Table_2.jpg]]
*Table 2: Evaluation on out-ofdistribution tasks text-only reasoning benchmark MMLU-Pro*

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2504_15362/figures/007_Table_4.jpg]]
*Table 4: Attempted improvements on top of VLAA-Thinking and Virgo baselines*

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2504_15362/figures/010_Figure_4.jpg]]
*Figure 4: Response lengths vs. question difficulties. We analyze the responses of the VLM fine-tuned on LongPerceptualThoughts via DPO. Interestingly, we find that the model finetuned in our data naturally allocates more test-time compute for hard questions. We follow Lightman et al. (2024); Snell et al. (2025) and determine question complexity using rollouts on the base model*

![[assets/figures/papers/paper_list_l78_https_arxiv_org_abs_2504_15362/figures/001_Figure_1.jpg]]
*Figure 1: LongPerceptualThoughts is a new synthetic dataset with 30K long-thought traces for vision-centric tasks. Each trace contains diverse cognitive behaviors (e.g., verification, subgoal setting, and backtracking), akin to system-2 reasoning. CoTs generated by open-source VLMs often produce linear, rigid reasoning traces (top). In contrast, our novel data synthesis framework effectively expands these simple thoughts using frontier reasoning models, equipping VLMs with complex reasoning structures and rich cognitive behaviors—effectively distilling system-2 reasoning into instruction-tuned VLMs*

## 定位与知识库关联

### 1. 与基线方法的关系

#### 1.1 训练数据构成：从浅层链到长思维链的范式跨越

本方法的核心创新在于训练数据的构成方式，与现有基线形成鲜明对比：

- **DOCCI** (Onoe et al., 2024)：作为密集描述数据集，DOCCI 提供了高质量的图像文本描述。然而，实验表明直接在其上进行监督微调（SFT）会导致模型性能急剧下降——这是因为纯描述数据破坏了模型的指令遵循能力（见 Table 1）。本工作将 DOCCI 仅作为数据生成的起点，而非训练目标，从而规避了这一陷阱。

- **Virgo** (Du et al., 2025) 与 **VLAA-thinking** (Chen et al., 2025)：这两个数据集代表了从大模型蒸馏多模态推理数据的现有尝试。然而，Table 1 显示，在视觉中心基准上使用这些数据集进行微调反而造成性能倒退。作者将其归因于两个关键因素：**领域偏移**（domain mismatch）和**可学习性差距**（learnability gap）——即从远大于目标模型的推理模型蒸馏时，目标模型无法有效吸收复杂的推理模式。

- **Internal Thinking CoT**：基于提示的零样本链式思考基线，其生成的思维链呈现浅层、线性的僵化结构，缺乏验证、回溯、子目标设定等系统2认知行为。

本方法通过三阶段合成框架（密集描述→多选题→简单CoT→长思维链）生成的 LongPerceptualThoughts 数据集，在保持与目标模型输出分布接近的前提下，引入了丰富的认知行为模式（见 Figure 3a）。

#### 1.2 训练策略：从纯 SFT 到 SFT+DPO 的偏好优化

现有基线普遍采用纯监督微调（SFT），而本方法引入了直接偏好优化（DPO）作为第二阶段训练：

- **SFT 阶段**：在 LongPerceptualThoughts 的 30,295 条样本上进行全参数微调，使模型初步掌握长思维链的生成模式。
- **DPO 阶段**：在构造的 17,208 对偏好数据上进行优化。偏好对的构造遵循两个原则：
  - **正确性偏好**：$(z_1^+, a_1^+) \succ (z_1^-, a_1^-)$，即正确推理优于错误推理；$(z_1^- \oplus z_2^+, a_2^+) \succ (z_1^-, a_1^-)$，即经过反思纠正的错误推理优于未纠正的错误推理。
  - **简洁性偏好**：$(z_1^+, a_1^+) \succ (z_1^+ \oplus z_2^+, a_2^+)$，即简洁的正确推理优于冗长的正确推理。

实验表明，DPO 将平均提升从仅 SFT 的 +1.5 点提高到 +3.4 点，且一致性更好。其机制在于：DPO 偏好对的结构使模型在给定错误上下文时，自然地增加正确响应的概率 $P(z_2^+, a_2^+ | z_1^-)$，从而缓解了长思维链数据中不可避免的错误 token 的影响。

#### 1.3 思维链行为特征：认知行为的质变

Figure 3a 的量化分析揭示了关键差异：
- 开源 VLM（如 Qwen2.5-VL）的思维链遵循僵化结构，缺乏多样化的认知行为。
- 前沿推理模型（如 Gemini 2.0 Flash Thinking）展现出子目标设定、回溯、验证等丰富的认知行为。
- LongPerceptualThoughts 数据集成功复现了这些行为模式，使指令微调 VLM 获得了类似系统2推理的能力。

### 2. 适用边界与局限

#### 2.1 数据生成的依赖性

- **密集描述依赖**：数据生成流程依赖于现成的密集图像描述数据集（DOCCI），这限制了生成问题的多样性和覆盖范围。若密集描述存在偏差或遗漏，将直接传导至后续生成的多选题和思维链。
- **图像数量限制**：仅使用 500 张图片生成全部训练数据，存在过拟合特定描述风格的风险，可能无法覆盖所有视觉场景类型。

#### 2.2 模型架构的单一性

所有训练和评估均在 Qwen2.5-VL-7B-Instruct 上进行，方法对其他 VLM 架构（如 LLaVA 系列、InternVL 系列）的泛化能力未知。不同架构对长文本思维链的吸收效率可能存在显著差异。

#### 2.3 偏好优化的内在张力

- **简洁性偏好的双刃剑**：DPO 中引入的简洁性偏好虽然鼓励高效推理，但可能过分鼓励短回答，从而约束模型在困难问题上的思考深度。Figure 4 显示模型在困难问题上自然分配更多测试时计算，但简洁性偏好可能削弱这一自适应行为。
- **算法选择的局限性**：未与其他强化学习算法（如 PPO、GRPO）进行对比，无法确定偏好优化的最优形式。

#### 2.4 数据质量的残留问题

长思维链数据中不可避免地包含部分错误或冗余 token。尽管通过 SFT 数据集构造时的过滤（仅保留最终正确的轨迹）和 DPO 偏好对的缓解机制，但未能完全消除其影响。

#### 2.5 模态覆盖范围

方法目前仅面向图像和文本，尚未扩展到视频理解、3D 场景理解或其他多模态感知推理任务。

### 3. 开放问题

1. **过程验证器的构建**：如何为视觉感知任务构建可靠的过程验证器，以支持基于搜索的推理方法（如 beam search 或 MCTS）？当前方法仅依赖最终答案的正确性进行偏好标注。

2. **思维链形式的最优性**：长文本思维链是否是提升 VLM 感知推理能力的唯一或最优途径？是否存在更高效的推理表征形式（如结构化推理图、隐式推理向量）？

3. **跨模态扩展**：本框架能否扩展到视频理解、3D 场景理解等需要时序或空间推理的多模态任务？三阶段合成框架在这些场景下需要如何适配？

4. **去密集描述化**：能否在不依赖外部密集描述的情况下，直接从图像生成高质量的感知推理数据？这将消除数据生成流程中的关键瓶颈。

5. **模型规模的扩展性**：更大的基座模型（如 72B 或商业模型）在蒸馏长感知思考数据时，增益是否更加显著？可学习性差距是否会随模型规模增大而缩小？

6. **思维链质量的自动评估**：如何自动评估合成数据中长思维链的质量，特别是其中的认知行为（验证、回溯等）是否真正符合人类预期？当前缺乏针对感知推理思维链的可靠自动评估指标。

7. **推理模型能力的上限**：在保持输出分布与目标模型一致的前提下，能否引入更强的推理模型（如原版 DeepSeek-R1）进一步提升数据质量？更强的推理模型可能带来更丰富的认知行为，但也可能加剧可学习性差距。

## 原文 PDF

![[paperPDFs/arxiv_2025/LongPerceptualThoughts_Distilling_System_2_Reasoning_for_System_1_Perception.pdf]]
