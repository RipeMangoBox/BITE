---
title: "Can Large Vision-Language Models Correct Semantic Grounding Errors By Themselves?"
type: paper
paper_level: A
venue: CVPR
year: 2025
pdf_ref: paperPDFs/CVPR_2025/Can_Large_Vision_Language_Models_Correct_Semantic_Grounding_Errors_By_Themselves.pdf
code_link: null
project_link: https://andrewliao11.github.io/vlms_feedback/
aliases:
- ISCVBV
- CLVLMCSGEBT
tags:
- CVPR_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: "将语义基础问题分解为更容易的二元验证任务，并利用同一VLM作为验证器（Verifier）生成二元反馈，通过迭代对话循环，结合文本提示（零样本CoT）和视觉提示（视觉标记、RoI裁剪）来引导模型修正预测，是提升性能的核心操作变量。"
primary_logic: "VLMs可以通过自身生成的二元反馈进行迭代自校正，显著提升语义基础准确性，无需外部工具或先知。关键在于将复杂的生成式修正简化为简单的二元验证，并采用针对性的提示策略，使模型能够有效接收和利用反馈。"
claims:
- "在COCO数据集上，GPT-4o使用VLM验证自校正框架提升准确性8.43点，达到47.92%，相对基础预测39.49%增益显著。"
- "VLM二元验证生成的反馈质量（F1分数）相较内在自校正平均高出10点以上，LLaVA-1.5从51.12提升至61.71，证实了分解任务的有效性。"
- "神谕二元反馈结合零样本CoT和视觉标记可使开源自校正模型相对基础预测平均提升7.45点，表明VLM能够接收并利用反馈。"
- "内在自校正导致多数VLM性能下降，例如GPT-4V在ADE20k上从40.36骤降至22.95（-17.41），凸显了所提出二元反馈验证框架的必要性。"
---

# Can Large Vision-Language Models Correct Semantic Grounding Errors By Themselves?

> [!tip] 核心洞察
> VLMs可以通过自身生成的二元反馈进行迭代自校正，显著提升语义基础准确性，无需外部工具或先知。关键在于将复杂的生成式修正简化为简单的二元验证，并采用针对性的提示策略，使模型能够有效接收和利用反馈。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 大型视觉语言模型能否自行纠正语义基础错误？ |
| 英文题名 | Can Large Vision-Language Models Correct Semantic Grounding Errors By Themselves? |
| 会议/期刊 | CVPR 2025 |
| Links | [paper](https://arxiv.org/abs/2404.06510) · [Project](https://andrewliao11.github.io/vlms_feedback/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | Iterative Self-Correction with VLM Binary Verification |
| Dataset | ADE20k (semantic grounding accuracy), COCO (semantic grounding accuracy) |

> [!tip] 效果简介
> - ADE20k (semantic grounding accuracy) 上，Accuracy (%) 为 40.29，对比 35.86，变化 +4.43。
> - ADE20k (semantic grounding accuracy) 上，Accuracy (%) 为 41.18，对比 33.81，变化 +7.36。
> - COCO (semantic grounding accuracy) 上，Accuracy (%) 为 47.92，对比 39.49，变化 +8.43。

## 概要

### 1. 问题背景与核心瓶颈

大型视觉语言模型（VLMs）在语义基础（semantic grounding）任务中——即将图像区域映射为文本描述——仍存在显著错误。一个关键且未被充分探索的问题是：**VLM能否通过自我纠正（self-correction）来修正这些错误？**

当前VLMs在自我纠正方面的核心瓶颈在于**无法有效利用反馈**。具体表现为两个层面：

- **反馈生成质量低下**：当缺乏外部工具或先知反馈时，模型通过内在自校正（Intrinsic Self-Correction）生成的反馈极不可靠，甚至导致性能严重退化。例如，GPT-4V在ADE20k数据集上经过三轮内在自校正后，准确率从40.36骤降至22.95（-17.41点）。
- **反馈遵循能力不足**：即使提供显式的正确反馈（神谕反馈），开源VLM仍有约25%的案例无法遵循指令修正预测，揭示了模型在指令遵循方面的根本性缺陷。

### 2. 核心思路与方法定位

本文的核心洞察是：**将复杂的生成式修正任务分解为更简单的二元验证任务**，从而获得更可靠的反馈信号。基于此，作者提出了一种**基于VLM二元验证的迭代自校正框架**，无需领域内数据、微调或架构改动。

该方法的核心操作变量包括三个关键设计：

1. **验证方式转换**：由同一VLM充当验证器（Verifier），将“生成正确类别”的复杂任务简化为“判断预测是否正确”的二元验证任务，生成正确/错误的二元反馈。
2. **反馈集成策略**：结合零样本思维链（Zero-shot CoT）文本提示和视觉提示（视觉标记、RoI裁剪），引导模型有效接收并利用反馈进行修正。
3. **迭代对话循环**：预测器与验证器之间进行多轮交互，每轮利用验证反馈修正预测，直至收敛或达到最大轮次。

### 3. 方法谱系与知识库定位

本工作定位于**VLM自校正与多模态理解**的交叉领域。与LLM自校正研究（关注文本推理）不同，本文聚焦于连接语言与视觉概念的语义基础任务，这是目前研究较少的领域。

在方法谱系上，本文的对比基准包括：
- **内在自校正（Intrinsic Self-Correction）**：基于提示的自我反思方法，要求模型自行审查并修正答案，但不引入外部验证信号。
- **神谕验证（Oracle Verification）**：使用真实二元反馈作为性能上界，用于衡量VLM利用反馈的潜力上限。

本文提出的VLM二元验证框架在两者之间建立了桥梁——不依赖外部工具，但通过任务分解获得了远超内在自校正的反馈质量。

### 4. 主要结果概览

实验在两个全景分割数据集（ADE20k和COCO）上，对多个开源和专有VLM进行了评估。核心发现如下：

**自校正有效性**：
- GPT-4o在COCO上通过VLM验证自校正提升准确率8.43点（39.49→47.92），在ADE20k上提升7.36点（33.81→41.18）。
- LLaVA-1.5在ADE20k上提升4.43点（35.86→40.29）。

**反馈质量对比**：
- VLM二元验证生成的反馈F1分数相较内在自校正平均高出10点以上（LLaVA-1.5：51.12→61.71），证实了任务分解的有效性。

**反馈利用潜力**：
- 神谕二元反馈结合零样本CoT和视觉标记可使开源自校正模型相对基础预测平均提升7.45点，表明VLM具备接收并利用反馈的能力。

**内在自校正的危害**：
- 内在自校正导致多数VLM性能下降，凸显了所提出二元验证框架的必要性。

### 5. 局限性与开放问题

尽管取得显著提升，该方法仍存在若干局限：
- 自校正增益与神谕上界之间仍有较大差距，VLM生成的反馈存在噪声，可能误导预测器。
- 强专有模型（GPT-4V、GPT-4o）在多轮神谕反馈后仍保持40%以上的错误率，其利用真实信息的能力受限。
- 评估仅限于语义基础任务，泛化性有待验证。

开放问题包括：如何提升VLM遵循显式反馈的能力？如何设计更可靠的反馈生成机制？自校正能否扩展到更复杂的视觉推理任务？

### 问题背景：大型视觉语言模型的语义基础能力

大型视觉语言模型（VLMs）在图像描述、视觉问答等任务中展现了强大的多模态理解能力，但其在**语义基础**（semantic grounding）——即将图像中的特定区域准确映射为对应的语义类别文本——这一基础任务上的表现仍远未达到可靠水平。语义基础要求模型在给定图像 $\mathbf{x}$、感兴趣区域 $\mathbf{r}_i$ 和文本提示 $\mathbf{q}$ 的条件下，输出描述该区域语义类别的文本 $\mathbf{\sigma}_{0_i} = \mathbf{VLM}(\mathbf{x}, \mathbf{r}_i, \mathbf{q})$（Section 3.1）。这一能力是视觉推理、具身智能等下游应用的关键前提，但现有VLMs在此任务上错误率居高不下，成为实际部署的核心瓶颈。

### 现有方法缺口：自校正的缺失与内在反思的失败

在大语言模型（LLMs）领域，自我校正（self-correction）已被探索作为提升推理准确性的有效手段，但其在VLMs的多模态理解任务中几乎未被研究。一个关键挑战在于：**生成高质量的反馈本身极为困难**。现有尝试依赖模型的“内在自校正”（Intrinsic Self-Correction），即要求模型自行审查并修正其预测，但这一方法在语义基础任务上表现出**灾难性的性能退化**。例如，GPT-4V在ADE20k数据集上经过三轮内在自校正后，准确率从40.36骤降至22.95（-17.41点），表明模型不仅无法有效识别自身错误，反而在反思过程中引入了更多错误预测（Table 4）。

### 核心动机：将复杂修正简化为二元验证

面对上述困境，本文提出一个关键洞察：**语义基础任务可以被分解为更简单的二元验证任务**。与其要求模型直接生成修正后的正确类别（这需要复杂的生成和推理能力），不如让模型仅判断一个已有预测是否正确——这是一个二分类问题，难度显著降低。通过将同一VLM实例化为“验证器”（Verifier），生成二元反馈（正确/错误），再通过迭代对话循环将反馈集成回预测过程，模型可以在无需外部工具、领域数据微调或架构修改的前提下，实现可靠的自我纠正。

### 研究目标与核心问题

本文系统性地探索以下核心问题：
1. **VLMs能否接收并理解基础反馈？** 即当提供显式反馈时，模型是否具备遵循指令修正预测的能力？
2. **VLMs能否为自身生成高质量的反馈？** 通过二元验证分解策略，模型生成的反馈是否比内在反思更可靠？
3. **迭代自校正能否稳定提升语义基础准确性？** 在无神谕（oracle）反馈的真实场景下，自校正框架是否有效且不会造成性能倒退？

这些问题的回答将为VLMs的自我改进能力提供基础性理解，并为无需额外训练即可提升多模态理解性能开辟新路径。

## 核心方法与创新机理

本工作的核心创新在于提出了一种**基于VLM二元验证的迭代自校正框架**，使得大型视觉语言模型能够在不依赖外部工具、领域数据微调或架构修改的前提下，通过自我生成的反馈显著提升语义基础（Semantic Grounding）的准确性。

### 创新1：将语义基础任务分解为二元验证任务

现有自校正方法面临的核心瓶颈在于生成可靠反馈的难度极高。本工作识别出一个关键的简化策略：**语义基础任务可以被分解为更容易的二元验证任务**（判断预测是否正确），从而获得更可靠的反馈信号。这一洞察直接催生了VLM Verifier的设计——使用同一VLM作为验证器，仅需回答“是/否”问题，而非生成完整的修正文本，大幅降低了反馈生成的难度。

### 创新2：VLM二元验证替代内在自校正

与依赖模型自我反思的**内在自校正**（Intrinsic Self-Correction）基线方法相比，本方法的核心变化体现在以下三个操作槽位：

| 操作槽位       | 基线方法（内在自校正）  | 本方法（VLM二元验证）                            | 证据锚点                   |
| ---------- | ------------ | --------------------------------------- | ---------------------- |
| **验证方式**   | 无显式反馈或模型自我审查 | 由同一VLM作为验证器生成二元反馈（正确/错误），输入为裁剪区域或视觉标记图像 | Section 3.2.2, Table 3 |
| **反馈集成方式** | 仅文本提示或无显式反馈  | 结合零样本CoT文本提示与视觉提示（红圈标记、RoI裁剪、SoM）引导模型修正 | Table 2                |
| **迭代机制**   | 单次预测或有限轮次    | 多轮迭代对话循环，每轮利用验证反馈修正预测，直至收敛或达到最大轮次       | Section 5.1, Table 4   |

实验证据表明，内在自校正对多数VLM产生**负面增益**——例如GPT-4V在ADE20k上从40.36骤降至22.95（-17.41，Table 4），而VLM二元验证生成的反馈质量（F1分数）相较内在自校正平均高出**10点以上**（LLaVA-1.5从51.12提升至61.71，Table 3），证实了将复杂修正任务简化为二元验证这一设计的有效性。

### 创新3：提示策略的针对性设计

框架的另一个关键创新在于**反馈接收的提示策略设计**。研究发现，结合零样本CoT文本提示与视觉标记（visual marks）是引导模型利用二元反馈的最有效策略，平均带来**7.45个准确性点**的提升（Table 2）。视觉提示技术的选择需针对特定VLM定制——例如ViP-LLaVA偏好视觉标记，而LLaVA-1.5在RoI裁剪条件下表现更优（Table 3）。这种“文本+视觉”双重提示策略确保了模型能够有效接收并利用二元反馈信号进行迭代修正。

### 创新4：无需外部工具的闭环自校正

整个框架形成了一个**闭环的自校正系统**：Base Predictor生成初始预测 → VLM Verifier生成二元反馈 → Feedback Integrator将反馈集成到下一轮预测 → 迭代循环直至收敛。这一设计使得VLM仅依靠自身能力即可实现语义基础准确性的持续提升，无需任何外部工具或先知反馈。在COCO数据集上，GPT-4o使用该框架将准确性从39.49%提升至47.92%（+8.43，Table 5），LLaVA-1.5在ADE20k上从35.86%提升至40.29%（+4.43，Table 4），验证了闭环自校正的可行性。

本文提出的语义基础自校正框架围绕一个核心操作变量展开：**将复杂的生成式修正任务分解为更简单的二元验证任务**，并利用同一VLM作为验证器生成反馈，通过迭代对话循环引导模型修正预测，全程无需外部工具、领域内数据或模型微调。

### 框架总览

整个pipeline由四个核心模块构成，形成“预测—验证—集成—迭代”的闭环（Figure 2）：

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2404_06510/figures/002_Figure_2.jpg]]
*Figure 2: Semantic grounding and self-correction framework. Left (Semantic Grounding): Given an image and a text prompt that specifies a region of interest, a VLM is tasked to identify the semantic class best describing the image region. Center (Feedback Generation): For completeness, we explore both oracle and automated feedback generated from VLMs themselves. Oracle Binary Feedback: An oracle provides feedback only on the correctness of the predictions. Oracle Class Label Feedback: An oracle provides explicit feedback on the correct class labels. Automated Binary Feedback: A VLM acts as a ‘Verifier’, confirms or rejects the previous predictions. Right (Feedback Integration): VLMs correct their own...*

1. **基础预测器**：给定图像 $\mathbf{x}$、指定区域 $\mathbf{r}_i$ 和文本提示 $\mathbf{q}$，VLM输出描述该区域的语义类别文本 $\mathbf{\sigma}_{0_i} = \mathbf{VLM}(\mathbf{x}, \mathbf{r}_i, \mathbf{q})$。这是自校正的起点。

2. **VLM验证器**：同一VLM被实例化为验证器，对基础预测器的输出进行二元判断（正确/错误）。验证器接收经过视觉提示处理的输入（如RoI裁剪或视觉标记图像），生成二元反馈信号 $f^{\mathrm{VLM}}$。这一设计的关键洞察是：判断预测是否正确比生成正确预测本身更容易，因此二元验证能产生更可靠的反馈（Table 3证实VLM二元验证的F1分数相较内在自校正平均高出10点以上）。

3. **反馈集成器**：将二元反馈整合到下一轮预测中。采用两种互补的提示策略——文本层面的零样本CoT和视觉层面的标记提示（红圈、SoM等），引导模型关注被判定为错误的区域并进行修正。实验表明，零样本CoT与视觉标记的组合是最有效的反馈集成方式，平均提升7.45个准确率点（Table 2）。

4. **迭代对话循环**：协调预测器与验证器之间的多轮交互。在第 $t=0$ 轮获得基础预测后，验证器生成反馈，预测器据此修正，循环进行直至达到预设最大轮次 $K$ 或收敛。实验设置中，开源模型最多运行5轮，专有模型（GPT-4V、GPT-4o）运行3轮即可观察到稳定趋势（Table 4, Table 5）。

### 反馈类型与信息流

框架研究了两种反馈来源：

- **神谕反馈**：作为理论上界，包括二元反馈（仅告知正确/错误）和类别标签反馈（直接给出正确答案）。神谕二元反馈使开源模型平均提升约9个准确率点，但类别标签反馈未能达到100%准确率——LLaVA-1.5从35.86提升至94.8，仍有约5%的案例未能遵循显式正确指令（Table 1），揭示了模型遵循反馈的能力瓶颈。

- **VLM自生成反馈**：无需外部先知，由同一VLM作为验证器生成二元反馈。这是框架的核心贡献——将自校正从“模型自我反思”转变为“模型自我验证”，避免了内在自校正中反馈质量低下的问题。

### 与基准方法的本质区别

该框架与两类基准形成鲜明对比：

- **内在自校正**：要求模型自行审查并修正答案，不提供显式外部反馈。实验表明这一方法对多数VLM有害——GPT-4V在ADE20k上从40.36骤降至22.95（Table 4），因为模型无法可靠地区分自身预测的正确性。

- **神谕验证**：作为性能上界，证明VLM具备接收和利用反馈的能力，但实际增益受限于反馈集成效率和模型遵循指令的能力。

本框架在两者之间开辟了新路径：用VLM自身生成可靠的二元反馈替代不可靠的内在反思，同时避免依赖外部先知，实现了无需监督的自校正闭环。

### 语义基础的形式化定义

语义基础（Semantic Grounding）任务被定义为将图像区域映射为文本描述。给定输入图像 $\mathbf{x}$、目标区域 $\mathbf{r}_i$ 和文本提示 $\mathbf{q}$，VLM 输出描述该区域语义类别的文本序列：

$$
\mathbf{\sigma}_{0_i} = \mathbf{VLM}(\mathbf{x}, \mathbf{r}_i, \mathbf{q})
$$

其中 $\mathbf{\sigma}_{0_i}$ 表示在初始时间步 $t=0$ 时对第 $i$ 个区域的预测输出（Section 3.1）。该公式是整个自校正框架的起点，后续所有反馈生成与修正操作均围绕此基础预测展开。

### 核心模块划分

论文提出的**迭代自校正框架**由四个关键模块构成，形成“预测—验证—集成—迭代”的闭环：

**1. Base Predictor（基础预测器）**

基础预测器即 VLM 本身，负责在每一轮对话中根据当前图像、区域框和提示生成语义类别预测。初始轮次 $t=0$ 使用原始图像和标准提示，后续轮次则接收经过反馈增强的提示和视觉输入（Figure 2 左）。

**2. VLM Verifier（VLM 验证器）**

验证器是整个框架的核心创新。与需要模型自省的内在自校正（Intrinsic Self-Correction）不同，验证器将语义基础任务**分解为更简单的二元验证任务**——仅需判断“预测是否正确”而非生成正确的类别标签。验证器由同一 VLM 实例化，输入为经过视觉提示处理的图像（RoI 裁剪或视觉标记），输出二元反馈信号 $f^{\mathrm{VLM}}$（正确/错误）。

这一分解策略的关键证据来自 Table 3：LLaVA-1.5 使用 VLM 二元验证（RoI crop）的反馈 F1 分数达到 61.71，相较内在自校正的 51.12 提升超过 10 点，证实了降低任务难度对反馈质量的显著增益。

**3. Feedback Integrator（反馈集成器）**

反馈集成器负责将二元反馈信号转化为下一轮预测可用的提示。论文探索了两种互补的提示策略（Figure 3）：

- **文本提示**：零样本思维链（Zero-shot CoT），在 VLM 输出前添加引导性句子，促使模型在推理过程中显式考虑反馈信息。
- **视觉提示**：包括视觉标记（Visual Marks，如红圈标注目标区域）、RoI 裁剪（仅保留目标区域）、以及 Set-of-Mark（SoM）标注。视觉提示通过修改输入图像来引导模型的注意力聚焦。

Table 2 的消融实验表明，零样本 CoT 与视觉标记的组合是最有效的反馈集成策略，平均提升 7.45 个准确率点。

**4. Iterative Dialogue Loop（迭代对话循环）**

迭代循环协调预测器与验证器之间的多轮交互。在每一轮 $t$，预测器生成当前预测，验证器产生二元反馈，反馈集成器将反馈注入下一轮预测的提示中。循环持续进行直至达到预设最大轮次 $K$ 或验证器确认所有预测正确（Section 5.1）。

### 反馈类型的形式化区分

论文系统性地研究了三种反馈来源：

- **神谕二元反馈 $f^*$**：由真实标注提供的正确/错误信号，作为理论上界。
- **神谕类别标签反馈**：由真实标注提供的显式正确类别名称。
- **VLM 自生成反馈 $f^{\mathrm{VLM}}$**：由同一 VLM 作为验证器生成的二元反馈。

三者构成递进的研究层次：神谕类别标签反馈揭示模型遵循显式指令的能力上限（Table 1 显示 LLaVA-1.5 提升至 94.8 但未达 100%，暴露约 25% 的指令遵循失败率）；神谕二元反馈验证二元信号本身的有效性；VLM 自生成反馈则检验框架在无外部工具条件下的实际可行性。

## 实验与关键发现

### 核心实验设计

本研究的实验体系围绕三个递进问题展开：（1）VLM能否接收并利用外部反馈提升语义基础准确性？（2）VLM能否为自身生成高质量的二元反馈？（3）在迭代自校正框架下，VLM能否通过自身生成的反馈持续提升性能？实验在ADE20k和COCO两个全景分割数据集上进行，评估指标为语义基础准确率（Accuracy），反馈质量以F1分数衡量。

**基础模型选择**：实验覆盖四类代表性VLM——开源通用模型LLaVA-1.5、视觉提示增强模型ViP-LLaVA、开源强模型CogVLM，以及专有模型GPT-4V和GPT-4o，以验证方法的跨模型泛化性。

**反馈类型设定**：研究设计了三种反馈来源作为对照：（1）**Oracle Binary Feedback**（神谕二元反馈）：仅告知预测正确与否，作为理论上界；（2）**Oracle Class Label Feedback**（神谕类别标签反馈）：直接提供真实类别名，作为最强上界；（3）**VLM Binary Verification**（VLM二元验证）：由同一VLM实例化的验证器生成二元反馈，是本文的核心方法。

### 主实验结果

#### 反馈接收能力验证（Table 1）

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2404_06510/figures/005_Table_1.jpg]]
*Table 1: Findings of different feedback types. VLMs can receive different types of oracle feedback to improve grounding accuracy with no additional prompting techniques (i.e. zero-shot CoT or visual prompts). Among the evaluated VLMs, LLaVA-1.5 has the largest gains, improving 5.18 and 61.06 when provided with oracle binary and class label feedback, respectively. Table 2. Findings of ways to prompt binary feedback to VLMs. We find that combining zero-shot and visual marks leads to an average of 7.45 gains w.r.t. the base predictions*

LLaVA-1.5在仅获得神谕二元反馈（无额外提示技术）的条件下，准确率从35.86%提升至41.04%（+5.18），而获得神谕类别标签反馈时飙升至94.8%（+61.06）。这一巨大差距揭示了两个关键洞察：

- **二元反馈本身即可带来显著增益**：即使仅告知“对/错”，模型已能自主修正部分错误。
- **显式正确答案并未达到100%准确率**：即使直接告知真实类别，仍有约5.2%的案例无法修正，表明模型存在**指令遵循缺陷**——部分情况下VLM无法将显式反馈映射为正确的输出修正。这一现象在开源模型中更为突出，约25%的案例未能遵循显式反馈指令。

#### 反馈提示策略消融（Table 2）

在如何向VLM呈现二元反馈的消融实验中，零样本思维链（Zero-shot CoT）文本提示与视觉标记（Visual Marks）的组合策略效果最优，相对基础预测平均提升7.45个准确率点。单独使用零样本CoT或视觉标记的增益均低于组合策略，表明**文本引导与视觉注意力引导具有互补效应**——前者帮助模型理解反馈语义并规划修正步骤，后者将模型注意力聚焦于待修正区域。

#### 反馈质量对比（Table 3）

VLM二元验证生成的反馈质量（F1分数）相较内在自校正（Intrinsic Self-Correction）平均高出10个点以上。以LLaVA-1.5为例，内在自校正的反馈F1仅为51.12，而采用RoI裁剪的VLM二元验证将F1提升至61.71（+10.59）。这一结果验证了本文的核心设计理念：**将复杂的生成式修正分解为简单的二元验证任务，显著提升了反馈的可靠性**。

值得注意的是，不同VLM对视觉提示技术的偏好存在差异：LLaVA-1.5在RoI裁剪下表现最佳，而ViP-LLaVA则更偏好视觉标记。这提示在实际部署中需针对具体模型定制验证器的输入格式。

#### 迭代自校正性能（Table 4 & Table 5）

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2404_06510/figures/008_Table_4.jpg]]
*Table 4: Performances of self-correction on ADE20k up to 5 rounds. Oracle binary feedback (oracle verification) consistently improves all evaluated VLMs. Without oracle, VLM verification still consistently improve the grounding performances. On the other hand, intrinsic self-correction demonstrates negative gains in almost every VLM except for GPT-4o. We, therefore, stop intrinsic self-correction in the third round. For GPT-4V and $\mathrm { G P T - 4 o , }$ we find that running for three rounds is enough to identify the consistent trend. Red-colored font indicates the performances is lower than performances when t = 0. Numbers in the subscript indicate the performance changed w.r.t. to the performanc...*

在ADE20k数据集上，LLaVA-1.5通过VLM验证自校正（t=5轮）将准确率从35.86%提升至40.29%（+4.43），GPT-4o在t=3轮时从33.81%提升至41.18%（+7.36）。在COCO数据集上，GPT-4o的增益更为显著，从39.49%提升至47.92%（+8.43），ViP-LLaVA也从37.26%提升至40.44%（+3.18）。

**与神谕上界的差距分析**：LLaVA-1.5在神谕验证下可达53.2%（+17.34），而VLM验证仅达40.29%，二者间约13个点的差距揭示了当前自校正框架的两大瓶颈：（1）VLM验证器生成的反馈存在噪声，部分错误反馈误导预测器；（2）即使反馈正确，模型仍有约25%的概率无法有效利用反馈进行修正。

#### 内在自校正的失败模式（Table 4 & Table 5）

内在自校正在绝大多数VLM上导致性能退化，这一负面结果构成了本文方法必要性的关键证据。GPT-4V在ADE20k上从40.36%骤降至22.95%（-17.41），LLaVA-1.5和ViP-LLaVA也出现不同程度的下降。仅有GPT-4o在部分设置下从内在自校正中微弱受益，但其增益远低于VLM验证框架。

**失败根因**：内在自校正要求模型自行审查并修正答案，但模型难以准确判断自身预测的正确性——它倾向于将正确的预测错误地“修正”为错误答案，或将错误预测误判为正确而保持不变。这本质上是一个**元认知缺陷**：VLM缺乏对自身预测可靠性的准确评估能力。

### 成本-性能权衡分析（Figure 4）

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2404_06510/figures/022_Figure.jpg]]

GPT-4o在ADE20k上的成本-性能权衡曲线显示，VLM验证自校正在t=1时即可获得大部分增益，后续轮次的边际收益递减。这一发现对实际部署具有指导意义：**单轮自校正已能捕获约70-80%的总增益**，在计算预算受限的场景下可优先采用轻量级配置。

### 失败案例与局限性

1. **反馈噪声导致的错误传播**：VLM验证器并非完美，其生成的二元反馈存在误判（将正确预测标记为错误，或反之）。在COCO数据集上，LLaVA-1.5的个别案例中，原本正确的预测在接收错误反馈后被“修正”为错误答案，导致性能退化。

2. **指令遵循的固有缺陷**：即使提供无噪声的神谕二元反馈，开源模型仍有约25%的案例无法修正。这一比例在不同模型间相对稳定，暗示当前VLM架构存在系统性的反馈整合障碍，而非特定模型的训练不足问题。

3. **专有模型的利用瓶颈**：GPT-4V和GPT-4o在获得多轮神谕二元反馈后，错误率仍维持在40%以上。考虑到神谕反馈提供的是100%准确的信息，这一高错误率表明**强模型在利用真实反馈信息方面存在根本性限制**——它们并非缺乏信息，而是无法将已知的正确/错误信号有效转化为预测修正。

4. **任务与领域泛化性未验证**：当前实验仅限于ADE20k和COCO的语义基础任务，自校正框架在其他视觉推理任务（如视觉问答、具身指令跟随）或领域（如医学影像、遥感）的有效性仍是开放问题。

### 关键图表结论汇总

- **Table 1**：VLM能够接收并利用外部反馈，但即使提供真实类别标签也无法达到100%准确率，揭示指令遵循缺陷。
- **Table 2**：零样本CoT + 视觉标记是最优反馈呈现策略，文本与视觉引导具有互补效应。
- **Table 3**：VLM二元验证的反馈质量显著优于内在自校正（F1提升10+点），验证了任务分解的有效性。
- **Table 4 & Table 5**：VLM验证自校正在所有模型上持续提升性能，而内在自校正普遍导致退化；神谕上界与VLM验证间的差距指明了反馈质量和反馈利用两大改进方向。
- **Figure 4**：单轮自校正已捕获大部分增益，为计算资源受限场景提供轻量级部署依据。

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2404_06510/figures/014_Figure_14.jpg]]
*Figure 14: ViP-LLaVA qualitative results in ADE20k. We visualize the predictions of ViP-LLaVA at time steps from 0 to 2. Intrinsic self-correction fails to identify which predictions are correct/incorrect, while VLM binary verification and Noise-free feedback provide explicit signal on each region, leading to a better chance of correction. Note that we draw multiple samples in the VLM forward pass, therefore, leading to slightly different results even when the image and query are the same (See Appendix G). For the sake of visualization, we put a bright ID on each object and highlight the incorrect predictions in red and the correct predictions in green*

![[assets/figures/papers/paper_list_l21_https_arxiv_org_abs_2404_06510/figures/017_Figure_15.jpg]]
*Figure 15: CogVLM qualitative results in COCO. We visualize the predictions of CogVLM at time steps from 0 to 2. For the sake of visualization, we put a bright ID on each object and highlight the incorrect predictions in red and the correct predictions in green*

## 定位与知识库关联

### 任务定位：语义基础中的自校正

本研究聚焦于**语义基础（Semantic Grounding）**任务——给定图像和指定区域，要求VLM输出描述该区域的语义类别文本。该任务处于多模态理解与视觉-语言对齐的交叉点，是视觉问答、具身指令跟随等更复杂任务的基石。

在自校正（Self-Correction）这一更广泛的研究脉络中，已有工作主要探索纯文本LLM的自我修正能力，而本研究首次系统性地将自校正范式迁移至多模态语义基础场景。其核心贡献在于**将复杂的生成式修正任务分解为简单的二元验证任务**，从而绕开了现有VLM在生成高质量自反馈方面的根本困难。

### 与基线方法的关系

**内在自校正（Intrinsic Self-Correction）** 是本研究直接对比的核心基线。该方法要求模型自行审查并修正答案，无需外部反馈源。实验证据表明，内在自校正在多数VLM上导致性能显著退化——GPT-4V在ADE20k上从40.36骤降至22.95（-17.41），LLaVA-1.5和ViP-LLaVA同样出现负增益（Table 4）。这一发现构成了本文方法动机的直接实证基础：**缺乏结构化反馈的自校正不仅无效，甚至有害**。

**神谕验证（Oracle Verification）** 作为理论上界基准，提供两类反馈：二元反馈（仅告知正确/错误）和类别标签反馈（显式给出正确答案）。神谕二元反馈使开源自校正模型平均提升7.45准确率点（结合零样本CoT和视觉标记，Table 2），但类别标签反馈并未将准确率推至100%——LLaVA-1.5在获得真实类别标签后准确率仅达94.8（Table 1），揭示了约25%的案例中模型无法遵循显式指令的根本性限制。

本研究提出的**VLM二元验证自校正（Iterative Self-Correction with VLM Binary Verification）** 填补了内在自校正（无外部反馈）与神谕验证（完美反馈）之间的空白。其关键操作变量是将同一VLM实例化为验证器，通过二元验证任务生成反馈，并利用文本提示（零样本CoT）和视觉提示（视觉标记、RoI裁剪）引导模型在多轮迭代对话中修正预测。

### 方法谱系中的位置

从方法论角度，本文方法属于**提示驱动的自校正范式**，区别于微调或架构修改方案。其核心创新不在于模型训练，而在于反馈生成机制的设计：

1. **反馈源设计**：将验证任务从生成式修正降维为二元分类，使VLM生成的反馈F1分数相较内在自校正平均高出10点以上（LLaVA-1.5从51.12提升至61.71，Table 3），显著提升了反馈质量。

2. **提示策略组合**：零样本CoT（文本引导）与视觉标记（注意力引导）的组合被证明是最有效的反馈集成方式，平均提升7.45准确率点（Table 2）。

3. **迭代对话机制**：通过多轮预测器-验证器交互，GPT-4o在COCO上从基础预测39.49提升至47.92（+8.43，t=3轮），LLaVA-1.5在ADE20k上从35.86提升至40.29（+4.43，t=5轮）（Table 4-5）。

### 适用边界与局限

**适用条件**：
- 任务需可分解为独立的二元验证子任务
- VLM需具备基本的视觉区域理解能力
- 适用于零样本场景，无需领域内数据或微调

**核心局限**：

1. **指令遵循缺陷**：即使提供显式正确反馈，开源自校正模型仍有约25%的案例未能修正预测，限制了自校正增益的上限（Table 1）。

2. **强模型利用反馈能力有限**：GPT-4V和GPT-4o在多轮神谕二元反馈后仍保持40%以上的错误率（Sec. 5.2），表明专有模型同样存在利用真实信息的内在限制。

3. **反馈噪声风险**：VLM生成的二元反馈并非完美，错误反馈可能误导预测器，导致个别案例中预测从正确变为错误（COCO上LLaVA-1.5失败案例）。

4. **提升幅度与上界差距显著**：VLM验证自校正的提升（+4.43至+8.43）远低于神谕验证上界（+17.34，LLaVA-1.5在ADE20k），反馈生成与集成机制仍有较大改善空间。

5. **任务泛化性未验证**：评估仅限于ADE20k和COCO全景分割数据集上的语义基础任务，未探索其他视觉推理任务或领域的迁移能力。

### 开放问题

1. **反馈遵循能力的提升**：能否通过训练或提示设计降低约25%的显式反馈失败率，使模型更可靠地利用反馈信号？

2. **反馈噪声的鲁棒处理**：如何设计更可靠的反馈生成机制，或使预测器对噪声反馈具有容错能力，以提高自校正的稳定性？

3. **专有模型的高错误率根源**：GPT-4V和GPT-4o在获得神谕二元反馈后仍保持高错误率，其利用真实信息的能力限制是什么？是否存在架构或训练层面的根本瓶颈？

4. **任务扩展性**：二元验证分解策略能否推广至更复杂的视觉推理任务（如视觉问答、具身指令跟随）？哪些任务特性决定了该策略的适用性？

5. **自适应收敛判断**：最优自校正轮次因模型和数据集而异（GPT-4o在3轮后趋势稳定，LLaVA-1.5需5轮），如何在没有神谕的情况下自动判断收敛？

6. **方法协同效应**：自校正与微调、架构改进或外部工具结合能否产生协同效应，进一步缩小与神谕上界的差距？

## 原文 PDF

![[paperPDFs/CVPR_2025/Can_Large_Vision_Language_Models_Correct_Semantic_Grounding_Errors_By_Themselves.pdf]]
