---
title: "UniT: Unified Multimodal Chain-of-Thought Test-time Scaling"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/UniT_Unified_Multimodal_Chain_of_Thought_Test_time_Scaling.pdf
project_link: "https://ai.meta.com/research/publications/unit-unified-multimodal-chain-of-thought-test-time-scaling"
code_link: null
aliases:
- UniT
tags:
- CVPR_2026
- topic/other_unclear
- topic/other_unclear/general
core_operator: 引入多模态思维链推理和测试时计算预算（图像生成轮数）控制，使模型能够在推理阶段进行迭代式的生成-验证-细化，从而根据任务难度动态分配计算资源并提升输出质量。
primary_logic: 在短推理轨迹上训练的统一模型可以在测试时泛化至更长的推理链；顺序链式推理相较于并行采样能更高效地利用推断计算，以更少的资源实现更优的性能缩放，并同时惠及生成和理解任务。
claims:
- UniT 在 OneIG-Bench 上的对齐总体分数达到 0.843，相比基础 Bagel 模型（0.764）提升 10.34%。
- 顺序链式缩放仅需并行最优-N 采样约 2.5× 更少的图像生成量即可达到同等性能。
- 移除验证机制导致 OneIG Align 下降 3.1%；移除内容记忆对多轮编辑影响最大，ImgEdit 分数从 4.26 降至 2.45。
- 训练时平均轨迹长度 3.6 轮，测试时平均延长至 4.7 轮，展现出超越训练分布的推理长度泛化能力。
---

# UniT: Unified Multimodal Chain-of-Thought Test-time Scaling

> [!tip] 核心洞察
> 在短推理轨迹上训练的统一模型可以在测试时泛化至更长的推理链；顺序链式推理相较于并行采样能更高效地利用推断计算，以更少的资源实现更优的性能缩放，并同时惠及生成和理解任务。

| 字段 | 内容 |
|------|------|
| 中文题名 | UniT：统一多模态思维链测试时扩展 |
| 英文题名 | UniT: Unified Multimodal Chain-of-Thought Test-time Scaling |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2602.12279) · [Project](https://ai.meta.com/research/publications/unit-unified-multimodal-chain-of-thought-test-time-scaling) |
| Topic | #topic/other_unclear #topic/other_unclear/general |
| Method | UniT |
| Dataset | OneIG-Bench, CompBench, ImgEdit, MIRA |

> [!tip] 效果简介
> - OneIG-Bench 上，Overall Alignment 0.843 vs 0.764 (Bagel) (+10.34%)。
> - CompBench (multi-object editing) 上，Overall Score 0.988 vs 0.936 (Bagel) (+5.56%)。
> - ImgEdit (multi-turn editing) 上，Human Eval Score (0-10) 4.26 vs 1.31 (Bagel) (+225.19%)。

## 概述

当前统一多模态模型普遍采用单次前向传播生成输出，缺乏对生成结果进行自我验证、反思与迭代修正的能力。这一瓶颈在需要多步推理的组合生成、多轮编辑和复杂视觉推理任务中尤为突出——模型无法在生成后识别约束违反、无法将复杂指令分解为可执行的子目标，也无法在多轮交互中保持内容记忆。

针对这一问题，UniT 提出将**多模态思维链推理**与**测试时计算预算控制**相结合，使单一统一模型能够在推理阶段执行“生成-验证-细化”的迭代循环。其核心洞察在于：在短推理轨迹上训练的统一模型，可以在测试时泛化至更长的推理链；且**顺序链式推理**相较于并行最优-N采样，能以更少的计算资源实现更优的性能缩放，同时惠及生成和理解两类任务。

方法层面，UniT 通过三个关键模块实现上述目标：(1) **Agentic 数据合成流水线**，利用 VLM 验证与图像编辑模型自动生成约 12K 条多轮思维链轨迹，诱导验证、子目标分解和内容记忆三种认知行为；(2) **统一模型训练**，在合成轨迹上对 Bagel 基座模型进行监督微调；(3) **测试时缩放推理**，通过预算强制控制图像生成轮数，并采用嵌套分类器自由引导以提升文本遵循性与视觉一致性。

实验结果表明，UniT 在组合生成（OneIG-Bench 对齐分数 0.843，较 Bagel 提升 10.34%）、多轮编辑（ImgEdit 人类评分 4.26，提升 225%）和视觉推理（MIRA 准确率 11.5，提升 53.33%）等任务上均取得显著增益。顺序链式缩放仅需并行最优-N 采样约 2.5 倍更少的图像生成量即可达到同等性能。消融实验进一步验证了验证机制、内容记忆和数据质量过滤的关键作用。

## 背景与动机

### 统一多模态模型的生成瓶颈

近年来，统一多模态模型（unified multimodal models）在同时处理文本理解与图像生成任务上取得了显著进展。这类模型将视觉理解与视觉生成能力整合于单一架构中，使得模型能够“看懂”图像并“画出”图像。然而，现有统一模型——如 **Bagel**（Deng et al., 2025b）——的工作方式存在一个根本性局限：它们仅通过单次前向传播生成输出，缺乏对生成结果进行自我验证、反思与迭代修正的能力。

这一局限在面对以下三类任务时尤为突出：

1. **组合生成（Compositional Generation）**：当用户指令包含多个约束条件（如“画一只戴着红色帽子的白猫坐在蓝色椅子上”），单次生成往往遗漏或违背部分约束，模型却无法自行发现并修复这些错误。
2. **多轮编辑（Multi-turn Editing）**：在连续编辑场景中，模型需要记住前几轮的图像内容和用户意图，单次前向机制无法维持跨轮次的内容记忆与一致性。
3. **复杂视觉推理（Visual Reasoning）**：涉及多步逻辑推断的视觉问题（如拼图推理、因果推断）需要分解子目标并逐步验证假设，单次“看一眼就回答”的模式难以胜任。

### 测试时扩展的文本经验与多模态空白

在大语言模型（LLM）领域，测试时扩展（Test-Time Scaling, TTS）已被证明是提升推理能力的有效范式——通过思维链（Chain-of-Thought）在推理阶段分配更多计算资源，模型可以显著提高复杂问题的解决能力。然而，这一范式在多模态生成领域几乎处于空白状态。核心挑战在于：

- **生成任务缺乏自然的结构化反馈信号**：文本推理可以依赖逻辑自洽性进行验证，而图像生成的质量评估本身就是一个开放问题。
- **多模态思维链需要交织文本推理与图像操作**：模型不仅需要“思考”，还需要将思考结果转化为具体的图像编辑动作，这要求模型同时具备理解、规划和生成能力。
- **缺乏训练数据**：自然存在的多模态思维链轨迹极为稀缺，人工标注成本高昂且难以规模化。

### 核心动机与研究问题

基于上述缺口，本文的核心动机是：**能否将测试时扩展范式引入统一多模态模型，使模型在推理阶段通过多轮“生成-验证-细化”的思维链过程，根据任务难度动态分配计算资源，从而提升生成质量与推理能力？**

具体而言，本文试图回答以下问题：

- 如何自动合成高质量的多模态思维链训练数据，以诱导模型产生验证、子目标分解和内容记忆等认知行为？
- 统一模型在经过思维链微调后，能否在测试时泛化至比训练时更长的推理链？
- 顺序链式推理（sequential chain-of-thought）与并行采样（best-of-N parallel sampling）相比，哪种策略能更高效地利用推断计算资源？
- 这种测试时扩展机制是否能同时惠及生成任务（组合生成、多轮编辑）和理解任务（视觉推理）？

### 方法概览

为回答上述问题，本文提出 **UniT（Unified Multimodal Chain-of-Thought Test-Time Scaling）** 框架，其核心思路包含三个环节：

1. **Agentic 数据合成**：构建自动化流水线，利用视觉语言模型（VLM）进行迭代验证与规划，利用图像编辑模型执行细化操作，生成约 12K 条多轮思维链轨迹（如 Figure 2 所示）。
2. **统一模型训练**：在合成轨迹上对 Bagel 模型进行监督微调（700 H100 GPU 小时），使模型内化多模态推理模式。
3. **测试时缩放推理**：通过预算强制（Budget Forcing）机制控制图像生成轮数，实现顺序链式缩放，并配合嵌套分类器自由引导（CFG）以提升生成质量。

实验表明，UniT 在组合生成基准 OneIG-Bench 上相较 Bagel 提升 10.34%（0.764 → 0.843），在多轮编辑基准 ImgEdit 上人类评估分数提升 225%（1.31 → 4.26），同时顺序链式缩放仅需并行最优-N 采样约 2.5× 更少的图像生成量即可达到同等性能，展现出显著的推理效率优势。

## 核心创新

UniT 的核心创新在于将**多模态思维链推理**与**测试时计算预算控制**引入统一多模态模型，使单一模型能够在推理阶段进行迭代式的“生成—验证—细化”循环，从而根据任务难度动态分配计算资源并提升输出质量。这一框架的关键突破体现在以下四个维度的 changed slots 上。

### 从单次生成到多轮自校正的推理范式转变

现有统一多模态模型（如基础 **Bagel**，Deng et al., 2025b）仅通过单次前向传播生成输出，缺乏对生成结果进行自我验证、反思与迭代修正的能力。这一局限在面对需要多步推理的组合生成、多轮编辑和复杂视觉推理时尤为突出。UniT 通过引入多轮思维链推理机制，使模型在推理时能够执行显式的验证、子目标分解和内容记忆行为，实现了从“一次性输出”到“迭代式精化”的范式跃迁。

具体而言，推理时通过**预算强制**（Budget Forcing）机制控制图像生成轮数 $C$，模型在每轮生成后自动进行自我验证，识别约束违反并规划下一步修正策略。这一机制使得模型在测试时能够泛化至比训练时更长的推理链——训练时平均轨迹长度为 3.6 轮，测试时平均延长至 4.7 轮（Figure 5），展现出超越训练分布的推理长度泛化能力。

### Agentic 数据合成：自动引出认知行为

传统方法缺乏显式的多轮思维链训练数据。UniT 构建了 **Agentic 数据合成流水线**（Figure 2），利用 VLM 和图像编辑模型迭代生成约 12K 条多轮思维链轨迹。该流水线通过以下循环自动引出三类关键认知行为：

- **验证**：VLM 评估生成图像是否满足提示约束，识别缺失或错误的元素；
- **子目标分解**：当验证不通过时，VLM 通过 `<think>` 标记进行显式推理，将复杂指令分解为可执行的子任务序列；
- **内容记忆**：模型显式引用和比较历史图像，追踪累积修改进度，避免重复错误或丢失已完成的部分。

这一数据合成策略是 UniT 能够内化多模态推理模式的基础。消融实验（Table 5）表明，移除验证机制导致 OneIG-Bench 对齐分数下降 3.1 个百分点；移除内容记忆对多轮编辑打击最大，ImgEdit 分数从 4.26 骤降至 2.45（相对下降 42.5%）。

### 嵌套 CFG 设计：解耦文本遵循与视觉一致性

在图像生成的分类器自由引导（CFG）设计上，UniT 提出了**嵌套的文本 CFG 与图像 CFG** 机制，独立控制文本跟随性和视觉一致性，这是对常规 CFG 设计的结构化改进：

$$v_{\text{text}} = v_{t,\text{unc}} + s_t (v_t - v_{t,\text{unc}})$$

$$v_{\text{final}} = v_{i,\text{unc}} + s_i (v_{\text{text}} - v_{i,\text{unc}})$$

第一层文本 CFG（$s_t=4.0$）增强指令遵循能力；第二层图像 CFG（$s_i=2.0$）在文本引导结果基础上施加图像条件化引导，以保持跨轮编辑的结构一致性。这种嵌套设计使得模型在迭代精化过程中既能忠实响应新指令，又能保留已生成内容的主体特征。

### 顺序链式缩放：更高效的测试时计算利用

在测试时缩放策略上，UniT 揭示了**顺序链式推理相较于并行采样**的关键效率优势。核心洞察在于：在短推理轨迹上训练的统一模型可以在测试时泛化至更长的推理链；顺序链式推理通过逐轮积累改进，能够以更少的资源实现更优的性能缩放。实验表明，顺序链式缩放仅需并行最优-N 采样约 2.5× 更少的图像生成量即可达到同等性能（Section 5.1; Figure 1），且在更多轮次下仍保持收益，而并行缩放较早进入平台期。这一优势同时惠及生成和理解任务——在 MIRA 视觉推理基准上，UniT 从 $C=1$ 到 $C=10$ 实现了 53.33% 的准确率提升（Table 4），证明思维链推理行为可从生成任务迁移至理解任务。

## 整体框架

UniT 构建了一套完整的多模态思维链测试时扩展框架，其核心思路是将迭代式的“生成-验证-细化”循环内化到统一多模态模型中，从而突破传统单次前向生成在组合生成、多轮编辑和复杂视觉推理上的瓶颈。该框架由三个紧密协作的模块构成：**Agentic 数据合成模块**、**统一模型训练模块**和**测试时缩放推理模块**，三者共同支撑起验证、子目标分解与内容记忆等认知行为的涌现。

### 数据合成：Agentic 流水线

训练数据的获取是整个框架的基石。UniT 设计了一套自动化的 Agentic 流水线（图 2），利用三个角色模型协同生成约 12K 条多轮思维链轨迹：

- **图像生成模型**根据用户提示生成初始图像；
- **视觉语言模型**对生成结果进行验证，判断输出是否满足提示要求；
- 当验证不通过时，VLM 通过显式的思考标记进行子目标分解，规划具体改进步骤，并重写编辑指令；
- **图像编辑模型**执行细化操作，生成新图像后再次进入验证循环。

这一迭代过程持续至验证通过，所产生的交错文本-图像推理轨迹直接教会统一模型如何在测试时通过计算来细化输出。流水线中还嵌入了数据相关性过滤和最小视觉变化过滤等质量筛选机制，确保合成轨迹的有效性。

### 统一模型训练

训练阶段以 **Bagel**（Deng et al., 2025b）为基础统一多模态模型，在合成轨迹上进行监督微调，耗时约 700 H100 GPU 小时。训练过程中，模型不仅学习多轮推理的文本模式，还内化了嵌套的分类器自由引导策略：

$$v_{\mathrm{text}} = v_{t,\mathrm{unc}} + s_t (v_t - v_{t,\mathrm{unc}})$$

$$v_{\mathrm{final}} = v_{i,\mathrm{unc}} + s_i (v_{\mathrm{text}} - v_{i,\mathrm{unc}})$$

其中文本 CFG 尺度 $s_t=4.0$ 增强指令遵循，图像 CFG 尺度 $s_i=2.0$ 在文本引导基础上进一步保持跨轮编辑的结构一致性。这种嵌套设计使模型在迭代细化中能同时兼顾语义忠实度和视觉连贯性。

值得注意的是，训练时轨迹的平均长度为 3.6 轮（图 5），但模型在测试时展现出超越训练分布的长度泛化能力，平均推理轮次延长至 4.7 轮——这是有效测试时扩展的关键特性。

### 测试时推理：预算强制与顺序缩放

推理阶段的核心机制是**预算强制**，将文本领域的推理 token 控制适配到多模态场景：计算预算 $C$ 定义为图像生成轮数。模型在每轮推理中自主决定是否继续细化，当达到预算上限时强制终止。

这一设计催生了两种截然不同的测试时扩展策略：

- **顺序链式缩放**：模型沿单条推理链迭代细化，每轮基于前一轮的输出进行验证和修正；
- **并行最优-N 采样**：独立生成 $N$ 张图像，通过 HPSv3 评分选择最佳结果。

顺序缩放的关键优势在于每轮都能利用前序信息进行针对性改进，而非从零开始重新生成。实验表明，顺序链式缩放仅需并行最优-N 采样约 2.5× 更少的图像生成量即可达到同等性能，且在更多轮次下仍保持收益增长，而并行缩放较早进入平台期。

### 认知行为涌现

贯穿整个框架的是三种认知行为的自然涌现：

1. **验证**：模型主动评估当前输出是否满足约束，识别遗漏或错误；
2. **子目标分解**：将复杂指令拆解为可逐步执行的子任务；
3. **内容记忆**：跨轮次追踪已完成的修改和保持不变的属性。

这些行为并非显式编程，而是从 Agentic 流水线的“生成-验证-规划”交互中自然产生，并通过训练内化到统一模型中。消融实验（表 5）定量证实了各自贡献：移除验证导致 OneIG Align 下降 3.1 个百分点，移除内容记忆使 ImgEdit 多轮编辑分数从 4.26 骤降至 2.45，相对下降 42.5%。

### 输入输出流

整体框架的端到端流程如下：

- **输入**：用户自然语言提示（可包含多轮编辑指令序列）
- **数据合成阶段**：提示 → 初始生成 → VLM 验证与规划 → 编辑模型细化 → 循环 → 多轮轨迹
- **训练阶段**：合成轨迹 → Bagel 模型监督微调 → UniT 模型
- **推理阶段**：用户提示 + 预算 $C$ → UniT 多轮推理（生成-验证-细化循环）→ 最终图像输出

这一框架的优雅之处在于：训练时仅需短推理链数据，测试时即可泛化至更长链；顺序推理的计算效率天然优于并行采样；且认知行为同时惠及生成任务和理解任务，展现出统一多模态模型的独特潜力。

### 补充图表

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/001_Figure.jpg]]

## 核心模块与公式推导

UniT 框架由三个核心模块构成：**Agentic 数据合成模块**、**统一模型训练模块**和**测试时缩放推理模块**。三者协同工作，使单一统一多模态模型能够在推理阶段进行多轮迭代式的生成-验证-细化。

### 数据合成模块

该模块仅在训练阶段使用，通过自动化的 Agentic 流水线合成多模态思维链轨迹。流水线包含三个角色：图像生成模型负责生成初始图像，视觉语言模型（VLM）负责验证生成结果是否满足提示要求，图像编辑模型负责执行细化操作。当 VLM 判定输出不满足约束时，会通过显式的思维 token 进行子目标分解，规划具体改进方案，并重写编辑指令。这一迭代循环持续至验证通过，从而产生交错文本与图像的多轮推理轨迹（Fig. 2）。最终收集约 12K 条轨迹，训练时平均轨迹长度为 3.6 轮。

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/002_Figure_2.jpg]]
*Figure 2: Agentic framework for synthesizing chain-of-thought training data. Starting from a user prompt, an image generation model generates an initial image. A vision-language model then performs verification - evaluating whether the output satisfies the prompt. When unsatisfactory, the VLM engages in explicit subgoal decomposition through thinking tokens, planning concrete improvements, and rewriting editing instructions. This iterative loop continues until verification succeeds, generating multi-turn reasoning trajectories that teach unified models to refine outputs through test-time computation. The explicit reasoning traces of the three models capture how cognitive behaviors emerge from the int...*

### 统一模型训练模块

在合成轨迹上对 **Bagel** 统一多模态模型进行监督微调，耗时 700 H100 GPU 小时。Bagel 本身具备理解和生成能力，但未包含多轮思维链或迭代细化机制。训练使模型内化三种关键的认知行为：

- **验证**：评估当前生成结果是否满足提示约束
- **子目标分解**：将复杂组合指令拆解为可顺序执行的子任务
- **内容记忆**：显式引用和比较历史图像，跟踪累积进展

### 测试时缩放推理模块

推理阶段引入**预算强制**机制，将文本领域的预算强制策略适配至多模态场景。核心差异在于：文本方法控制推理 token 数量，而 UniT 控制图像生成轮数 $C$，因为图像扩散采样占主导推理延迟。在指定预算 $C$ 下，模型进行 $C$ 轮顺序链式推理，每轮可生成一幅图像。训练时平均轨迹长度 3.6 轮，测试时平均延长至 4.7 轮，展现出超越训练分布的推理长度泛化能力（Fig. 5）。

### 嵌套分类器自由引导

训练与推理阶段均采用嵌套的分类器自由引导设计，独立控制文本跟随性和视觉一致性：

**文本 CFG**：将文本条件化预测与无条件化预测进行线性组合，引导尺度 $s_t = 4.0$，以增强文本指令遵循：

$$v_{\mathrm{text}} = v_{t,\mathrm{unc}} + s_t (v_t - v_{t,\mathrm{unc}})$$

**图像 CFG**：在文本引导结果 $v_{\mathrm{text}}$ 基础上，进一步施加图像条件化引导，尺度 $s_i = 2.0$，以保持跨轮编辑的结构一致性：

$$v_{\mathrm{final}} = v_{i,\mathrm{unc}} + s_i (v_{\mathrm{text}} - v_{i,\mathrm{unc}})$$

其中 $v_t$ 为文本条件化预测，$v_{t,\mathrm{unc}}$ 为文本无条件化预测，$v_{i,\mathrm{unc}}$ 为图像无条件化预测。两层嵌套设计使模型在遵循编辑指令的同时，维持与输入图像的结构连贯性。

### 认知行为诱导机制

上述模块在训练与推理过程中自然诱导出三种认知行为。消融实验定量验证了各自的贡献：移除验证行为导致 OneIG-Bench 对齐分数从 84.3 降至 81.2（下降 3.1 个百分点）；移除内容记忆对多轮编辑打击最大，ImgEdit 人工评分从 4.26 骤降至 2.45（相对下降 42.5%）。子目标分解对组合生成任务尤为关键，使模型能顺序处理复杂指令中的多个约束。

### 补充图表

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/014_Figure_7.jpg]]
*Figure 7: Data synthesis pipeline architecture. Three model roles coordinate via information flows: Image Gen Model produces initial images, Vision-language model verifies image and performs planning/prompt rewriting with content memory, Image Editing Model applies refinements. Trajectories loop until satisfied, producing interleaved text-image chain-of-thought data*

## 实验与分析

### 主结果：组合生成

UniT 在组合生成基准 OneIG-Bench 上展现了显著的性能提升。如 Table 1 所示，UniT 在 C=10 轮推理预算下取得 **0.843 的总体对齐分数**，相比基础 Bagel 模型（0.764）提升 **10.34%**，相比引入纯文本思维链的 Bagel+CoT（0.790）亦有 6.71% 的优势。这一增益在不同提示长度（Short/Medium/Long）和提示类型（NP/T&P）的子类上均保持一致，表明多模态思维链推理对组合指令遵循具有普适的增强作用。

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/006_Table_1.jpg]]
*Table 1: Compositional generation, OneIG-Bench. NP denotes the natural language prompt. T&P denotes the tag-based and phrase-based prompt. Short, Medium and Long represent the length of the prompts, where Short denotes the number of words is less than 30, Medium denotes the number between 30 and 60, and Long denotes the number exceeding 60. Bagel+CoT indicates Bagel with text-only chain-of-thought*

在 **CompBench 多对象编辑**任务上（Table 3），UniT 取得 **0.988 的总体分数**，较 Bagel（0.936）提升 5.56%，在所有子指标上均达到最优。这验证了迭代验证与细化机制对精确对象属性控制的贡献。

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/009_Table_3.jpg]]
*Table 3: Multi-object editing, CompBench. LC-T denotes local CLIP scores between the edited foreground and the local description. LC-I refers to the CLIP image similarity between the foreground edited result and ground truth (GT) image. Overall scores are computed using min-max normalization for each metric*

### 主结果：多轮编辑

多轮编辑是单次生成模型最薄弱的环节。在 **ImgEdit 基准**上（Table 2），Bagel 仅获得 1.31 的人类评估分数（0-10 分制），而 UniT 在 C=4 时达到 **4.26 分，相对提升 225.19%**。从 C=1 到 C=4，UniT 的分数从 1.31 持续攀升至 4.26，展现出清晰的测试时缩放趋势。值得注意的是，UniT 在“内容记忆”和“指令理解”两个维度上提升尤为突出——这正是单次生成模型完全缺失的能力。三位专家独立评分的一致性达到 Krippendorff’s α = 0.82，评估可靠性高。

### 主结果：视觉推理

在 **MIRA 多模态推理基准**上（Table 4），UniT 从 C=1 时的 7.5 分提升至 C=10 时的 **11.5 分，相对提升 53.33%**。这一结果表明，在生成任务中诱导出的认知行为（子目标分解、逐步验证）可以**迁移至理解任务**，使模型能够将复杂推理问题分解为可管理的子步骤。然而，UniT 的绝对分数仍明显低于 GPT-5（OpenAI, 2025）和 Qwen2.5-VL (72B)（Bai et al., 2025）等大规模模型，揭示了基础模型能力上限对推理性能的根本制约。

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/011_Table_4.jpg]]
*Table 4: Multimodal reasoning, MIRA, with direct input. We report results across four reasoning categories: EG (Geometry), PBR (Physics), ASLP (Puzzles), and CT (Causal), along with the overall average score*

### 消融实验：认知行为

Table 5 系统消融了三种核心认知行为的贡献：

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/012_Table_5.jpg]]
*Table 5: Cognitive behavior ablation. Impact of removing verification, subgoal decomposition, or content memory from our agentic framework*

- **移除验证机制**：OneIG Align 从 84.3 降至 81.2（-3.1 个百分点），MIRA 准确率下降 1.9 个百分点。验证是确保生成结果与指令一致的第一道防线。
- **移除子目标分解**：对组合生成影响最大，OneIG Align 下降 2.4 个百分点。这表明将复杂指令拆解为有序子任务是处理多约束场景的关键。
- **移除内容记忆**：对多轮编辑造成**灾难性影响**——ImgEdit 分数从 4.26 骤降至 2.45，相对下降 42.5%。内容记忆是跨轮次保持对象身份和编辑一致性的核心机制，其缺失导致模型在后续轮次中“遗忘”先前编辑内容。

### 消融实验：数据质量

Table 6 验证了数据合成流水线中各项过滤策略的必要性：

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/013_Table_6.jpg]]
*Table 6: Data quality ablation. Impact of removing individual curation filters (Sec. 3.1) from the training data pipeline*

- **移除数据相关性过滤**（即保留与原始指令无关的合成轨迹）：OneIG Align 下降 3.1 个百分点，说明噪声轨迹会稀释模型对指令-生成对应关系的学习。
- **移除最小视觉变化过滤**（即保留编辑前后差异过小的轨迹）：显著损害多轮编辑性能，因为模型无法从“无变化”的伪轨迹中学习有效的细化策略。

### 顺序缩放 vs. 并行缩放

Figure 1 的核心发现是：**顺序链式缩放在所有任务上均优于并行最优-N 采样**。具体而言：

- 在 OneIG-Bench 上，C=10 的顺序缩放比并行采样高出约 4.85%。
- 顺序缩放仅需并行采样约 **2.5 倍更少的图像生成量**即可达到同等性能水平。
- 并行缩放在较早轮次即进入平台期，而顺序缩放持续受益于更多推理轮次。

这一结果的根本原因在于：顺序链式推理允许模型基于前一轮的生成结果进行**针对性修正**，而并行采样只是独立重复尝试，缺乏信息累积与反馈闭环。为公平比较，实验排除了并行采样中用于选择最优结果的 HPSv3 评分开销，仅以生成图像数量作为计算度量——因为图像扩散采样占据主导延迟，文本 tokens 开销可忽略。

### 训练-推理分布泛化

Figure 5 展示了 UniT 的一项重要涌现属性：训练时平均轨迹长度为 **3.6 轮**，而测试时平均延长至 **4.7 轮**。这一分布偏移证明模型具备**超越训练分布的推理长度泛化能力**——在短链上训练，在长链上推理。这是有效测试时缩放的关键前提：模型不是简单记忆训练时的推理模式，而是真正内化了“验证-规划-细化”的元认知循环。

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/008_Figure_5.jpg]]
*Figure 5: Training vs. inference round distribution demonstrates beyond-training generalization. The model is trained on trajectories averaging 3.6 refinement rounds, but effectively generalizes to longer inference chains averaging 4.7 rounds at test time. This distribution shift reveals the model’s emergent ability to extend inference beyond its training distribution, a key property of effective test-time scaling*

### 代表性失败模式

Figure 9 揭示了 UniT 在以下场景中仍会失败，需要手动验证：

- **精确目标计数**：如指定数量的餐巾纸排列，模型难以精确控制对象数量。
- **复杂空间关系**：如“叉子环绕盘子”的几何约束，模型缺乏精确的空间推理能力。
- **中间图像布局漂移**：在迭代细化过程中，人物数量等属性可能发生意外变化。

这些失败模式指向基础模型在细粒度约束推理和精确空间感知上的固有限制，而非思维链框架本身的问题。

### 计算开销与局限性

评估受 GPU 内存限制，最大仅探索至 C=10 轮。训练成本为 700 H100 GPU 小时，训练数据仅约 12K 条合成轨迹。超出 C=10 后，图像质量可能因累积自回归噪声而退化——这是当前框架的一个已知瓶颈。论文提出了感知阈值、重置轮次和自适应噪声调度等缓解措施作为开放问题，但尚未实验验证。

### 补充图表

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/003_Figure_3.jpg]]
*Figure 3: UniT enables iterative refinement for compositional instructions through multimodal chain-of-thought reasoning. UniT exhibits: (i) error verification and correction—identifying and fixing constraint violations that Bagel misses (top: correcting leash placement and dog action); (ii) subgoal decomposition with subject consistency—sequentially addressing instructions while maintaining subject identity across rounds (middle: preserving bear features through style transformation, bottom: skateboard consistency); (iii) quality preservation—maintaining visual fidelity through iterative refinement rather than degradation (top: reduced artifacts and haloing)*

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/005_Figure_4.jpg]]
*Figure 4: Qualitative examples of chain-of-thought test-time scaling. Representative trajectories showing progressive refinement across different tasks and computational budgets. Examples demonstrate how explicit chain-of-thought reasoning enables the model to iteratively improve compositional generation*

![[assets/figures/papers/paper_list_l2355_https_arxiv_org_abs_2602_12279/figures/010_Figure_6.jpg]]
*Figure 6: Chain-of-thought visual reasoning on MIRA. The model decomposes the puzzle into subgoals (zoom in, identify patterns) before selecting the matching piece, demonstrating cognitive behaviors transferring from generation to understanding tasks*

## 方法谱系与知识库定位

### 统一多模态模型谱系中的位置

UniT 建立在 **Bagel**（Deng et al., 2025b）这一统一多模态架构之上，该架构同时具备理解与生成能力。Bagel 本身代表了将文本生成、图像生成和视觉理解整合于单一模型的趋势，但其核心缺陷在于仅通过单次前向传播生成输出，缺乏对生成结果进行自我验证、反思与迭代修正的能力。UniT 正是在这一瓶颈处切入：它不改变底层架构，而是通过引入多模态思维链推理机制，使同一统一模型能够在测试时进行多轮“生成-验证-细化”循环。

从方法谱系看，UniT 处于三条研究脉络的交汇点：

1. **统一多模态模型**：与 **Janus-Pro**（Chen et al., 2025b）和 **BLIP3-o**（Chen et al., 2025a）等现有统一生成模型相比，UniT 的差异化在于其推理时自校正能力，而非单纯追求单次生成质量的提升。

2. **测试时缩放**：UniT 将文本领域的预算强制（budget forcing）策略（Muennighoff et al., 2025）首次适配至多模态场景。不同于文本模型通过控制推理 token 数量进行缩放，UniT 以图像生成轮数作为计算预算的控制维度——这是因为图像扩散采样占据了推理延迟的主导地位。

3. **思维链推理**：与 **Bagel+CoT**（Deng et al., 2025a）的纯文本思维链提示不同，UniT 的思维链是真正多模态的：模型在推理过程中交替生成文本分析（验证、子目标分解）和图像输出（细化结果），形成交织的文本-图像推理轨迹。这一设计使得认知行为（验证、子目标分解、内容记忆）能够从生成任务迁移至理解任务，如 MIRA 视觉推理中展现的子目标分解能力。

### 适用边界与能力约束

UniT 的有效性受限于以下边界条件：

- **基座模型能力上限**：UniT 的推理能力受限于 Bagel 的基础模型容量。在 MIRA 视觉推理任务上，UniT 整体准确率仅为 11.5，远低于 **GPT-5**（OpenAI, 2025）和 **Qwen2.5-VL (72B)**（Bai et al., 2025）等大规模模型。这表明思维链缩放无法弥补基础模型在视觉理解上的根本性差距，其增益主要体现在对已有能力的更有效调度上。

- **推理轮次的物理极限**：受 GPU 内存限制，实验仅探索至 C=10 轮。超出此范围后，图像质量可能因累积的自回归噪声而退化。论文提出了感知阈值、重置轮次和自适应噪声调度等缓解措施，但尚未实证验证。

- **组合复杂度的天花板**：在涉及精确目标计数、复杂空间关系或细粒度属性控制的组合任务上，UniT 仍会出现失败。这些失败模式揭示了当前验证机制在约束满足推理上的不足——模型可能“知道”约束未满足，但缺乏有效的规划能力来精确修正。

### 局限性与开放问题

**已识别的局限**：

1. **训练数据规模有限**：仅约 12K 条合成轨迹用于监督微调（700 H100 GPU 小时），可能未能充分覆盖极端长链推理或高多样性编辑场景。这限制了模型在分布外推理链上的鲁棒性。

2. **验证机制的脆弱性**：消融实验显示，移除验证行为导致 OneIG Align 下降 3.1 个百分点，但当前验证依赖模型自身的判断能力，缺乏外部验证器或结构化约束检查，可能在迭代过程中出现质量退化循环。

3. **内容记忆的强依赖**：移除内容记忆对多轮编辑的打击最大，ImgEdit 分数从 4.26 骤降至 2.45（相对下降 42.5%）。这表明模型在多轮编辑中的表现高度依赖对历史生成内容的显式记忆，一旦该机制失效，性能将急剧退化。

**开放问题**：

- 如何设计更鲁棒的验证机制，以避免在迭代过程中出现质量退化循环？能否引入外部验证器或结构化约束检查来增强自校正的可靠性？

- 如何将物理感知、视角和遮挡等隐性约束融入细化策略，以处理精确的空间推理？当前框架对这类细粒度空间关系的建模能力明显不足。

- 超出 C=10 后，测试时缩放的拐点位于何处？论文提出的感知阈值、重置轮次和自适应噪声调度等缓解措施的实际效果如何？

- 测试时缩放如何与自一致性、验证器引导生成等其他推断时技术相互协同？当前仅探索了预算强制这一种缩放策略。

- 能否发展更高效的反思机制和自适应预算分配策略，在保证质量的同时大幅降低额外推理开销？顺序链式缩放虽优于并行采样，但每轮仍需生成完整图像，计算成本仍然可观。

- 如何将本框架扩展至音频、视频等其他模态？多模态思维链的核心思想——通过交替生成与验证进行迭代细化——在理论上具有模态无关性，但具体实现面临模态特定的生成与验证挑战。

## 原文 PDF

![[paperPDFs/CVPR_2026/UniT_Unified_Multimodal_Chain_of_Thought_Test_time_Scaling.pdf]]
