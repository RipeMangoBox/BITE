---
title: "SceneCOT: Eliciting Grounded Chain-of-Thought Reasoning in 3D Scenes"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SceneCOT_Eliciting_Grounded_Chain_of_Thought_Reasoning_in_3D_Scenes.pdf
openreview_forum_id: U9meoc0Sau
aliases:
- SceneCOT
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "引入显式的 chain-of-thought 推理结构，将任务分解为阶段并嵌入区域识别、实体检测、对象属性提取等多模态专家信号，确保每个推理步骤都与场景中具体实体相关联。"
primary_logic: "通过将复杂的3D场景推理任务分解为可管理的子步骤，并在每个步骤中显式整合多模态视觉线索，可以显著提升推理的准确性、可解释性以及 grounding 与问答之间的一致性。"
claims:
- "SCENECOT 在 Beacon3D 上的 Good Coherence (GC) 指标达到34.7，远高于所有基准方法（次高20.4）。"
- "消融实验表明，去除问题类型识别、区域识别或 grounding loss 均会导致性能下降，验证了各组件的重要性。"
- "Oracle 实验表明，当提供完美的 ground-truth 掩码和标签后，Counting 任务得分从47.9提升至98.8，证实 grounding 质量是性能上限的关键。"
- "MSQA 上 Counting GPT-Score = 47.9"
---

# SceneCOT: Eliciting Grounded Chain-of-Thought Reasoning in 3D Scenes

> [!tip] 核心洞察
> 通过将复杂的3D场景推理任务分解为可管理的子步骤，并在每个步骤中显式整合多模态视觉线索，可以显著提升推理的准确性、可解释性以及 grounding 与问答之间的一致性。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SceneCOT：三维场景中的有根据思维链推理 |
| 英文题名 | SceneCOT: Eliciting Grounded Chain-of-Thought Reasoning in 3D Scenes |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=U9meoc0Sau) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SCENECOT |
| Dataset | MSQA, Beacon3D, SQA3D-G |

> [!tip] 效果简介
> - MSQA 上，Counting GPT-Score 为 47.9，对比 37.4 (Chat-Scene†)，变化 +10.5。
> - Beacon3D 上，Good Coherence (GC) 为 34.7，对比 20.4 (SceneVerse)，变化 +14.3。
> - SQA3D-G 上，Grounding F1@50 为 51.6，对比 3.4 (Chat-Scene)，变化 +48.2。

## 概述

### 1. 问题背景与瓶颈

三维场景理解正从感知走向推理，但现有3D大语言模型在回答复杂场景问题时存在一个关键瓶颈：**缺乏逐步的、与场景对象显式关联的推理过程**。模型虽然可能给出正确的最终答案，但推理过程不透明，且 grounding 与问答之间的一致性（grounding-QA coherence）很低——即模型声称的依据对象与实际答案之间的对应关系薄弱。这一问题在计数、导航、空间关系等需要精确场景参照的任务中尤为突出。

### 2. 核心方法与洞察

**SCENECOT** 的核心洞察是：将复杂的3D场景推理任务分解为可管理的子步骤，并在每个步骤中显式整合多模态视觉线索，可以显著提升推理的准确性、可解释性以及 grounding 与问答之间的一致性。

为此，SCENECOT 将推理过程重构为四个阶段：
- **任务识别**：判定问题类型（计数、存在性、属性、导航、指代、空间关系），生成 `<think_type>` 标签以指导后续模块选择；
- **区域定位**：基于方向和钟表参考系将场景划分为子区域，过滤无关对象，生成 `<think_rgn>`；
- **实体 grounding**：调用3D视觉 grounding 专家模型（PQ3D）和符号引擎，获得对象概率、位置等显式多模态线索，生成 `<think_grd>` 和 `[OBJ]` token；
- **有根据的推理**：整合视觉线索进行逐步推理，最终生成 `<answer>`。

训练目标联合优化三项损失（式1）：
$$\mathcal{L} = \mathcal{L}_{\mathrm{CoT}} + \mathcal{L}_{\mathrm{ans}} + \mathcal{L}_{\mathrm{ground}}$$
其中 $\mathcal{L}_{\mathrm{CoT}}$ 和 $\mathcal{L}_{\mathrm{ans}}$ 为因果语言建模损失，$\mathcal{L}_{\mathrm{ground}}$ 为对象 grounding 的交叉熵损失，确保模型在每个推理步骤中都与场景实体保持显式关联。

### 3. 方法定位

在方法谱系中，SCENECOT 区别于两类现有方案：
- **单步直接生成方法**（如 **LEO**、**MSR3D**、**Chat-Scene**、**SceneVerse**、**LLaVA-3D**）：这些基线直接生成答案，缺乏显式的逐步 grounding 推理过程，可解释性和 grounding 一致性不足；
- **隐式 grounding 方法**（如基于对象中心 token 的场景表示）：虽涉及对象信息，但未在每个推理步骤中显式调用多模态专家信号。

SCENECOT 通过引入显式的 chain-of-thought 推理结构，将多模态专家（3D视觉 grounding、符号引擎、区域过滤规则）嵌入到推理链的每个阶段，属于**逐步有根据推理**范式。

### 4. 主要结果与证据强度

**Table 1**（MSQA 基准）显示，SCENECOT 在 Counting 任务上达到 **47.9** GPT-Score，较最佳基线 Chat-Scene†（37.4）提升 **+10.5**，在所有子任务中取得最优或次优结果。

**Table 2**（Beacon3D 基准）的 Grounding-QA 连贯性评估中，SCENECOT 的 Good Coherence（GC）达到 **34.7**，远超所有基线（次高 SceneVerse 为 20.4），同时双失败率（DF）最低（16.8%），表明其 grounding 与问答之间具有强一致性。

**消融实验**（Figure 5）证实，去除问题类型识别、区域识别或 grounding loss 均导致性能下降，验证了各组件的必要性。**Oracle 实验**（Table 3）表明，当提供完美的 ground-truth 掩码和标签后，Counting 得分从 47.9 跃升至 **98.8**，证实 grounding 质量是性能上限的关键约束。

**零样本泛化**（Table 11）：在 SQA3D-G 上，SCENECOT 的 Grounding F1@50 达到 **51.6**，远高于 Chat-Scene 的 3.4，证明即便在未见的场景问答数据上，其 grounding 能力仍具显著优势。

### 5. 局限与开放问题

当前框架受限于预定义的任务类型，尚未覆盖长期具身任务规划；SCENECOT-185K 数据集仅基于 ScanNet 构建，场景多样性有限；推理延迟约 **10.4 秒**，主要瓶颈在 LLM 序列生成，制约实时应用。此外，空间关系等子任务的 CoT 设计仍不完善，性能上限较低。如何改进思维链设计、扩展至更复杂场景、降低推理延迟，是后续研究的关键方向。

## 背景与动机

三维场景理解正从单纯的对象识别走向复杂的、情境化的场景推理。用户不再满足于“场景里有什么”，而是期望模型能够回答诸如“我左边的第三个物体是什么颜色？”或“面向北边时，12点钟方向有几把椅子？”这类需要多步推理的问题。这要求模型同时具备两种能力：一是对三维空间关系的精确建模，二是将推理步骤与场景中具体实体显式关联的**grounding**能力。

近年来，多模态大语言模型（MLLM）在三维场景问答上取得了显著进展。然而，现有方法存在一个核心瓶颈：**它们在回答复杂场景问题时，缺乏逐步的、与场景对象显式关联的推理过程**。大多数模型采用“端到端”的单步生成策略——直接接收场景表示和问题，然后输出答案。这种黑箱式推理虽然在某些情况下答案可能正确，但带来了两个严重问题：

1. **可解释性缺失**：用户无法理解模型是如何得出结论的，这在具身智能、人机协作等高风险场景中是不可接受的。
2. **Grounding-QA 一致性低**：模型的回答与它所依据的场景实体之间缺乏可验证的关联。即使答案正确，也无法确认模型是否真的“看”对了物体，还是仅凭语言先验进行了猜测。

从方法谱系来看，现有基线方法均未有效解决这一瓶颈。**LEO** 和 **Chat-Scene** 等方法通过对象令牌或场景令牌隐式地编码场景信息，但缺少显式的 grounding 步骤；**MSR3D** 直接生成回答，没有中间推理过程；**SceneVerse** 和 **LLaVA-3D** 虽然利用了多模态场景表示，但同样未引入结构化的逐步推理。即便是使用真实标签作为输入的 Oracle 基线 **GPT-4o***，其推理过程也不包含与场景实体的显式关联。

这一缺口在需要精确空间定位和计数的任务上尤为突出。例如，在 Beacon3D 基准的 Grounding-QA 连贯性评估中，现有方法的 Good Coherence（GC）指标普遍较低，表明模型常常“答对但指错”或“指对但答错”，双失败率也居高不下。

本文的动机正是源于这一关键缺口：**如何让三维大语言模型像人类一样，在回答复杂场景问题时进行有步骤、可追溯、与场景实体紧密关联的推理？** 受大语言模型中思维链（Chain-of-Thought）推理的启发，本文提出将 CoT 范式引入三维场景理解，但进一步要求每个推理步骤都显式地 grounding 到场景中的具体实体上——这不仅是生成一段推理文字，而是要在推理的每一步中调用多模态专家信号，将“思考”与“观察”紧密结合。

## 核心创新

SCENECOT 的核心创新在于将 3D 场景推理从单步“黑箱”答案生成转变为**显式、逐步、有根据的思维链推理**。这一转变通过以下四个关键机制实现：

### 1. 四阶段逐步推理策略

现有 3D 大语言模型（如 **LEO**、**MSR3D**、**Chat-Scene**）通常采用单步直接生成答案的策略，缺乏中间推理过程。SCENECOT 将复杂场景问答分解为四个有序阶段（Figure 2）：

1. **任务识别**：生成 `<think_type>` 标签，判断问题属于计数、存在性、指代、导航、空间关系、属性等类别，指导后续模块选择。
2. **区域定位**：基于方向和钟表参考系将场景划分为子区域，过滤无关对象，生成 `<think_rgn>` 以缩小搜索空间。
3. **实体 grounding**：调用多模态专家模型（3D 视觉 grounding 模型 PQ3D、符号引擎）获取对象概率、3D 位置等显式线索，生成 `<think_grd>` 和 `[OBJ]` token。
4. **有根据的推理**：整合视觉线索，进行总结并生成最终 `<answer>`。

这一分解策略的因果效应在消融实验中得到了直接验证：去除问题类型识别或区域识别均导致性能显著下降（Figure 5），证实了逐步推理结构对性能的因果贡献。

### 2. 显式多模态 grounding 机制

现有方法或者完全缺乏 grounding 步骤，或者仅通过对象 token 进行隐式 grounding（如 Chat-Scene 的对象中心表示），导致推理过程与场景实体之间的关联性弱。SCENECOT 在每个推理步骤中**显式调用多模态专家**（Algorithm 1），构造 `<obj_prob>`、`<obj_loc_prob>`、`<highlight_obj>` 等视觉线索，确保每个推理步骤都与场景中具体实体相关联。

这一机制的因果效应体现在两个层面：
- **grounding-QA 连贯性**：SCENECOT 在 Beacon3D 上的 Good Coherence (GC) 指标达到 34.7，远超次优方法 SceneVerse 的 20.4（Table 2），表明 grounding 与问答之间的显式关联显著提升了一致性。
- **grounding 质量作为性能上限**：Oracle 实验（Table 3）表明，当消除语义错误和 grounding 错误后，计数任务得分从 47.9 跃升至 98.8，导航任务从当前水平提升至 87.2，直接证实 grounding 质量是制约整体性能的关键瓶颈。

### 3. 联合训练目标

现有方法通常仅优化语言建模损失。SCENECOT 引入联合训练目标（Eq. 1）：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CoT}} + \mathcal{L}_{\mathrm{ans}} + \mathcal{L}_{\mathrm{ground}}$$

其中 $\mathcal{L}_{\mathrm{CoT}}$ 和 $\mathcal{L}_{\mathrm{ans}}$ 为因果语言建模损失，分别优化推理链和最终答案的生成；$\mathcal{L}_{\mathrm{ground}}$ 为交叉熵 grounding 损失，鼓励模型准确识别目标对象。消融实验表明，去除 grounding loss 导致计数、指代和导航任务性能下降（Figure 5），验证了该损失项对 grounding 密集型任务的必要性。

### 4. 规则驱动的区域过滤

现有方法通常考虑场景中所有对象，导致搜索空间过大。SCENECOT 通过规则引擎基于方向信息过滤相关子区域的对象（Sec 3.1, Sec A.2），将注意力集中在任务相关实体上。内部评估显示，问题类型识别准确率达 99.4%，区域识别达 100%（Table 14），表明这些基于规则的初始阶段高度可靠，为后续推理提供了稳定的基础。

### 创新总结

SCENECOT 的创新本质在于**将 grounding 从隐式副产品提升为显式推理步骤**，通过“任务分解 + 多模态专家调用 + 联合优化”的组合机制，解决了 3D 场景问答中推理可解释性和 grounding 一致性的瓶颈。这一设计使模型不仅在答案准确性上提升（MSQA 计数任务 +10.5，Table 1），更在 grounding-QA 连贯性上建立了显著优势（GC 提升 +14.3，Table 2）。

## 整体框架

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_U9meoc0Sau/figures/002_Figure_2.jpg]]
*Figure 2: SCENECOT framework. The model decomposes 3D scene reasoning into four steps: task recognition, spatial region recognition, entity grounding, and grounded reasoning. Each stage introduces explicit grounding signals (e.g., objects, attributes, spatial positions), ensuring step-by-step reasoning and improved grounding-QA coherence*

SCENECOT 的核心设计理念是将复杂的3D场景推理任务分解为可管理的子步骤，并在每个步骤中显式整合多模态视觉线索，从而提升推理的准确性与 grounding-QA 一致性。该框架建立在一个多模态大语言模型（MLLM）之上，以 LLaVA-1.5（基于 Vicuna-7B）作为主推理引擎，并通过四个顺序执行的模块完成从问题输入到有根据答案输出的完整流程（Figure 2）。

### 四阶段推理流水线

**阶段一：任务识别（Task Recognition）**。模型首先分析输入问题，识别其所属的任务类型（如计数、存在性判断、属性查询、空间关系、导航等），并生成 `<think_type>` 标签。该标签将指导后续模块选择相应的处理策略。实验表明，该模块的识别准确率达到 99.4%（Table 14），为下游处理提供了高度可靠的基础。

**阶段二：区域识别（Region Recognition）**。基于代理的位置和朝向信息，模型通过规则引擎将场景划分为子区域，并利用方向信息（包括基本方向与钟表参考系）过滤与问题无关的对象。该模块生成 `<think_rgn>` 标签，明确指定任务相关的空间范围。区域识别的准确率达到 100%（Table 14），有效缩减了后续 grounding 阶段的搜索空间。

**阶段三：实体 grounding（Entity Grounding）**。在筛选后的区域范围内，模型调用专门的3D视觉 grounding 专家模型（基于 PQ3D 微调）对问题所指的目标实体进行定位。该模块生成 `<think_grd>` 标签和 `[OBJ]` token，同时由符号引擎提取多模态视觉线索，包括对象概率 `<obj_prob>`、3D位置 `<obj_loc_prob>` 以及高亮对象 `<highlight_obj>` 等（Algorithm 1）。对于属性和描述类子任务，还会通过2D视觉编码器获取目标对象的图像特征。

**阶段四：有根据的推理（Grounded Reasoning）**。模型整合前三个阶段产生的所有视觉线索与结构化信息，进行总结并生成最终答案 `<answer>`。这一阶段确保每个推理步骤都与场景中的具体实体显式关联，从而实现 grounding-QA 的连贯性。

### 训练目标

SCENECOT 采用联合优化策略，总损失函数为三项损失之和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CoT}} + \mathcal{L}_{\mathrm{ans}} + \mathcal{L}_{\mathrm{ground}}$$

其中，$\mathcal{L}_{\mathrm{CoT}}$ 和 $\mathcal{L}_{\mathrm{ans}}$ 分别为推理链文本和最终答案的因果语言建模损失，$\mathcal{L}_{\mathrm{ground}}$ 为基于 PQ3D 专家模型的对象 grounding 交叉熵损失（Eq. 1）。消融实验证实，去除 grounding loss 会导致计数、指代和导航等子任务性能显著下降（Figure 5），验证了显式 grounding 监督的必要性。

### 与基线方法的关键差异

相较于 LEO、Chat-Scene、MSR3D 等现有方法，SCENECOT 的核心差异体现在两个维度：其一，推理策略从单步直接生成答案转变为四阶段逐步推理；其二，grounding 机制从无显式步骤或仅通过对象 token 隐式关联，升级为在每个推理步骤中显式调用多模态专家获取对象概率、位置等线索。Table 1 的对比结果表明，SCENECOT 是唯一被标注为“Grounded”的方法，在 MSQA 的计数子任务上以 47.9 的 GPT-Score 显著优于次优基线 Chat-Scene†（37.4），在 Beacon3D 的 Good Coherence 指标上以 34.7 远超 SceneVerse（20.4）（Table 2）。

## 核心模块与公式推导

SCENECOT 将复杂的三维场景推理分解为四个顺序执行的阶段，每个阶段引入显式的 grounding 信号，确保推理步骤与场景实体之间建立可追溯的关联。

**任务识别模块 (Task Recognition Module)** 首先分析输入问题，生成 `<think_type>` 标签以确定问题类型。该模块将问题归类为计数、存在性、属性、指代、导航或空间关系等预定义类别，为后续模块的选择和推理路径提供依据。消融实验表明，去除该模块后导航和空间关系任务性能显著下降（Figure 5），但模块自身的分类准确率达到 99.4%（Table 14），高度可靠。

**区域识别模块 (Region Recognition Module)** 基于智能体的位置与朝向，利用方向信息将三维场景划分为子区域。具体而言，系统通过正则表达式匹配解析问题中的方向描述——包括基本方向（左、右、前、后）和钟表方向（如“1点钟方向”），随后根据规则引擎过滤出相关子区域内的候选对象，生成 `<think_rgn>` 标签。该模块有效缩小了后续 grounding 的搜索空间：消融实验中移除区域识别后，计数、指代和属性任务性能均出现明显下降（Figure 5），而模块本身识别准确率达到 100%（Table 14）。

**实体 Grounding 模块 (Entity Grounding Module)** 是框架的核心组件，负责在筛选后的候选区域内定位目标对象。该模块以微调版的 PQ3D 作为三维视觉 grounding 专家模型，结合文本嵌入计算对象与问题描述之间的语义匹配概率。模块输出 `<think_grd>` 标签和 `[OBJ]` 标记，显式标注被 grounding 到的场景实体。在训练过程中，该模块受到额外的 grounding 损失监督（见下文的训练目标公式），强制模型学习准确的实体定位。消融实验证实，去除 grounding 损失会导致计数、指代和导航任务性能下降，而存在性任务受此影响较小（Figure 5）。

**符号引擎 / 视觉线索构造器 (Symbolic Engine / Visual Clue Constructor)** 从 grounding 模块的输出中提取结构化信息，构造三类关键视觉线索：`<obj_prob>` 表示对象 grounding 的置信度概率，`<obj_loc_prob>` 编码对象的三维空间位置信息，`<highlight_obj>` 提供被选中对象的图像 token。这些线索以统一格式注入后续的推理阶段，确保大语言模型能够直接利用多模态感知信号进行决策。

**有根据的推理模块 (Grounded Reasoning Module)** 整合前述阶段产生的所有视觉线索和结构化信息，执行最终的逐步推理并生成 `<answer>` 标签。该模块以 LLaVA-1.5（基于 Vicuna-7B）作为多模态大语言模型推理引擎，在推理过程中可调用二维视觉编码器处理属性描述等需要图像理解的任务。

---

**训练目标公式**

SCENECOT 采用联合优化策略，总损失函数为三项损失的加权和：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CoT}} + \mathcal{L}_{\mathrm{ans}} + \mathcal{L}_{\mathrm{ground}}$$

其中各分量含义如下：
- $\mathcal{L}_{\mathrm{CoT}}$：思维链文本生成的因果语言建模损失，监督模型逐步生成包含 `<think_type>`、`<think_rgn>`、`<think_grd>` 等标签的推理轨迹。
- $\mathcal{L}_{\mathrm{ans}}$：最终答案生成的因果语言建模损失，监督模型在推理链末尾输出正确的 `<answer>`。
- $\mathcal{L}_{\mathrm{ground}}$：对象 grounding 的交叉熵损失，由 PQ3D 专家模型提供监督信号，强制模型在 `[OBJ]` 标记位置准确预测目标实体的语义标签。

该联合训练目标使模型在学会逐步推理的同时，获得显式的实体定位能力，从而提升 grounding 与问答之间的一致性。消融实验中移除 $\mathcal{L}_{\mathrm{ground}}$ 后，MSQA 上计数、指代和导航任务的性能均出现可测量的下降（Figure 5），验证了该损失项的必要性。

---

**钟表方向计算**

在导航任务中，系统需要将三维空间中的相对角度转换为人类可理解的钟表方向描述。其计算方式为：

$$\text{clockwise\_direction} = \text{round}(\text{angle} / 30) \% 12$$

其中 angle 表示目标对象相对于智能体朝向的偏转角（以度为单位）。该公式将 360 度圆周等分为 12 个扇区，每个扇区对应 30 度，取整后通过模 12 运算映射到 1 至 12 点钟的标准钟面表示。这一方向计算规则被集成在区域识别模块中，用于生成方向相关的 `<think_rgn>` 标签和后续的空间推理。

## 实验与分析

### 主要结果

SCENECOT 在 MSQA 和 Beacon3D 两个基准上均展现出相对于现有方法的显著优势。Table 1 汇总了主要对比结果。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_U9meoc0Sau/figures/005_Table_1.jpg]]
*Table 1: Experimental Results on MSQA and Beacon3D. *: GPT-4o’s input contains ground-truth object labels, locations, and attributes. ‡: The result of MSQA is not based on Version-2.1 data. MSR3D, Chat-Scene, and LEO are trained on SCENECOT-185K-QA(no grounded COT). :: The models are trained on our dataset. The best and second-best performances are highlighted across the entire table. In the third column, ‘Grounded’ indicates whether the reasoning results can be explicitly linked to specific entities*

在 MSQA 基准上，SCENECOT 在 Counting 子任务上取得 47.9 GPT-Score，较次优方法 Chat-Scene†（37.4）提升 +10.5。值得注意的是，SCENECOT 是唯一具备显式 grounding 能力的方法（Table 1 中标记为 ✓），其整体表现均衡，在 Exist、Attribute、Spatial、Navigation 等多个子任务上均达到最优或次优水平。

在 Beacon3D 基准上，SCENECOT 的 Case-level GPT-Score 达到 58.9，Object-level GPT-Score 达到 23.2，均显著领先于其他方法。该基准使用 ground-truth object masks 进行评估，确保了推理能力比较的公平性——所有方法在相同的感知输入条件下被测试，差异仅源于推理策略本身。

### Grounding-QA 连贯性

Table 2 展示了 grounding 与问答之间连贯性的深度分析。SCENECOT 在 Good Coherence（GC，即 grounding 和 QA 同时正确）指标上达到 34.7，远超次优方法 SceneVerse 的 20.4（+14.3）。同时，SCENECOT 的双重失败率（DF，两者皆错）仅为 16.8%，在所有方法中最低。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_U9meoc0Sau/figures/006_Table_2.jpg]]
*Table 2: Grounding-QA Coherence comparison across methods. Main metrics: GC: good coherence (both grounding and QA correct); QA (Obj.): per-object QA performance. Additional reference metrics: Type 1: grounding correct but QA wrong; Type 2: QA correct but grounding wrong; DF: double failure (both wrong); R _ { 1 } “ Type1 / (Type1 + DF); R2 “ Type2 / (Type2 + GC)*

这一结果揭示了现有 3D LLM 的核心瓶颈：即使答案正确，grounding 与 QA 之间也缺乏一致性。其他方法虽然在 Object-level QA 上可能表现尚可，但其 grounding 正确但 QA 错误（Type 1）或 QA 正确但 grounding 错误（Type 2）的比例较高，表明它们的回答缺乏与场景实体的可靠关联。SCENECOT 通过在每个推理步骤中显式嵌入 grounding 信号，从根本上缓解了这一问题。

### 消融实验

Figure 5 展示了针对三个关键组件的消融实验结果，验证了各模块的必要性：

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_U9meoc0Sau/figures/007_Figure_5.jpg]]
*Figure 5: Ablation study. We ablate three key factors: (1) question type recognition, (2) region recognition, and (3) grounding loss. Results show that removing any of these components degrades performance, highlighting their importance for robust step-by-step reasoning*

1. **去除问题类型识别**：将所有问题视为同一类型处理，导致 Navigation 和 Spatial Relationship 任务性能明显下降。这是因为不同任务类型需要不同的推理策略和专家模块调度，统一处理会引入不恰当的推理路径。

2. **去除区域识别**：将场景中所有对象作为输入而不进行空间过滤，显著降低了 Counting、Refer 和 Attribute 任务的性能。区域识别模块通过方向信息过滤无关对象，有效减少了干扰实体对推理过程的噪声影响。

3. **去除 grounding loss（式 (1) 中的 $\mathcal{L}_{\mathrm{ground}}$）**：使 Counting、Refer 和 Navigation 性能下降，但 Existence 任务受影响较小。这表明显式的 grounding 监督信号对于需要精确对象定位和属性提取的任务尤为关键，而对于仅需判断对象是否存在的简单任务，其边际贡献相对有限。

Table 14 显示，问题类型识别准确率达 99.4%，区域识别准确率达 100%，表明这些初始阶段高度可靠，为后续推理提供了稳固基础。

### Oracle 上界分析

Table 3 通过逐步消除错误源，揭示了 SCENECOT 的性能上限。在主实验中，SCENECOT 使用 Mask3D 提供的预测对象掩码和语义标签。Oracle 实验分两个层次：

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_U9meoc0Sau/figures/008_Table_3.jpg]]
*Table 3: Experimental results on oracle data. In our main results, we utilize Mask3D to provide object masks and semantic labels. In this table, we explore the upper boundary in two aspects: 1) perfect object masks and semantic labels, but still based on the predicted object probabilities. 2) Oracle ground-truth text-based thought. In the table, “SE” indicates semantic error, “GE” indicates grounding error*

- **消除语义错误（SE）和 grounding 错误（GE）**：当提供完美的 ground-truth 掩码和语义标签后，Counting 得分从 47.9 跃升至 98.8，Navigation 从当前水平提升至 87.2。这表明 grounding 质量是限制性能上限的关键因素。

- **仅消除 grounding 错误（GE）**：即使语义标签仍由模型预测，仅修正 grounding 错误也能带来显著提升，进一步证实了 grounding 准确性的核心作用。

值得注意的是，Spatial Relationship 任务即使在 Oracle 条件下仍是最困难的子任务，提示当前 CoT 设计在该任务类型上仍不完善，需要针对性的推理链改进。

### 失败模式与定性分析

Figure 6 展示了 SCENECOT 的定性推理示例，揭示了典型的成功与失败模式：

- **成功案例（左）**：在 Counting 任务中，SCENECOT 正确构造了视觉线索（visual clue），识别出目标对象并基于 grounding 结果进行计数，最终得出正确答案。推理链清晰展示了从任务识别到实体 grounding 再到答案生成的完整流程。

- **成功案例（中）**：在 Navigation 任务中，模型基于准确的相对位置信息（时钟方向计算，见式 A.3）正确回答了方向性问题。

- **失败案例（右）**：即使视觉线索精确匹配了正确实体，模型在最终总结阶段仍可能给出错误答案。这表明当前基础 LLM（Vicuna-7B）的推理能力本身构成了另一瓶颈——grounding 可以准确定位对象，但将 grounding 结果转化为正确答案的推理步骤仍可能出错，这与 Table 3 中 Navigation 上限仅达 87.2 的发现一致。

### 零样本泛化与 Grounding 评估

Table 11 展示了 SCENECOT 在 SQA3D 和 ScanQA 上的零样本性能。SCENECOT 在 SQA3D 上取得 39.7 EM-R，SQA3D-G 上取得 51.6 F1@50，ScanQA-G 上取得 40.8 F1@50，均显著优于 Chat-Scene 和 LEO。这表明 SCENECOT 的逐步 grounding 推理策略具有良好的泛化能力，即使在未见过的数据集上也能保持 grounding 与 QA 的一致性。

![[assets/figures/papers/paper_list_l36_https_openreview_net_forum_id_U9meoc0Sau/figures/027_Table_11.jpg]]
*Table 11: Zero-shot QA and grounding performance on SQA3D and ScanQA*

Table 4 进一步汇总了跨五个 grounding 基准的结果。SCENECOT 在 MSQA、SQA3D 和 ScanQA 的 grounding 指标上均取得最优，在 Nr3D 和 Beacon3D 上也保持竞争力。值得注意的是，专门的 3D 视觉 grounding 模型 PQ3D 在 Nr3D Top-1 上表现更好，但 SCENECOT 作为统一的推理框架，在多个基准上实现了更均衡的 grounding 性能。

### 推理成本

SCENECOT 的逐步推理策略引入了额外的计算开销。Table 13 显示，SCENECOT 的推理延迟约为 10.4 秒，其中大部分时间消耗在 LLM 序列生成上。这一延迟水平限制了其在实时交互场景中的直接应用，是当前方法的一个重要实际约束。

## 方法谱系与知识库定位

### 任务定位与核心瓶颈

SCENECOT 瞄准的是**三维场景中的情境化推理**（situated 3D reasoning）——给定一个三维场景和一条自然语言问题，模型不仅需要给出答案，还需要将推理过程显式地与场景中的具体实体关联起来。这一任务介于传统的 3D 视觉定位（3D visual grounding）和 3D 问答（3D QA）之间，其核心瓶颈在于：现有 3D 大语言模型在回答复杂场景问题时，缺乏逐步的、与场景对象显式关联的推理过程，导致答案虽然可能正确，但缺乏可解释性和 grounding-QA 连贯性。

具体而言，当前方法面临的困境可以分解为三个层面：
1. **推理黑箱**：模型直接生成答案，中间推理步骤不可见，无法验证其是否基于正确的场景理解；
2. **grounding 缺失**：即使答案正确，也无法追溯答案与场景中哪个实体相关，导致 grounding-QA coherence 低；
3. **复杂场景退化**：当场景包含大量对象时，模型难以有效筛选相关信息，性能显著下降。

### 方法谱系与基线对比

SCENECOT 位于以下几条研究线的交汇处：

**3D 多模态大语言模型**：以 LEO、Chat-Scene、LLaVA-3D 为代表的方法将 3D 场景编码为对象中心或体素特征，并与 LLM 对齐以执行问答任务。这些方法的共同特点是**单步直接生成答案**，不包含显式的逐步推理过程。Chat-Scene 通过对象 token 隐式地关联场景实体，但缺乏可追溯的 grounding 链。SCENECOT 在此基础上引入了四阶段推理结构，将隐式关联转化为显式的、可审计的 grounding 信号。

**3D 视觉定位专家模型**：PQ3D 等模型专门优化对象定位精度，在 Nr3D 等纯定位基准上表现优异（Top-1 达 57.7），但它们不执行复杂的语义推理。SCENECOT 将 PQ3D 作为多模态专家模块嵌入推理管道，在需要对象定位的步骤中调用其能力，同时通过联合训练使定位信号服务于下游推理。

**思维链推理**：在 2D 视觉语言任务中，chain-of-thought 已被证明能提升复杂推理的准确性和可解释性。SCENECOT 将这一范式迁移到 3D 场景，但面临独特的挑战：3D 场景中的推理步骤需要与三维空间中的具体实体关联，而非仅依赖抽象的语义推理。为此，SCENECOT 在每个推理阶段嵌入了多模态专家信号（3D 视觉 grounding、符号引擎），确保思维链的每一步都有场景依据。

**关键方法差异**（基于 verified_analysis 中的 changed_slots）：

| 维度 | 基线方法 | SCENECOT |
|------|---------|----------|
| 推理策略 | 单步直接生成答案 | 四阶段逐步推理（任务识别→区域定位→实体 grounding→有根据推理） |
| grounding 机制 | 无显式 grounding 或仅隐式对象 token | 每步调用多模态专家，输出对象概率、位置等显式线索 |
| 训练目标 | 仅语言建模损失 | 联合优化 CoT 损失 + 答案损失 + grounding 交叉熵损失 |
| 区域过滤 | 考虑所有场景对象 | 基于方向和钟表参考系过滤相关子区域 |

### 决定性证据与性能边界

SCENECOT 的核心贡献得到了多层次实验的验证：

**grounding-QA 连贯性**（Table 2）：在 Beacon3D 上，SCENECOT 的 Good Coherence（GC）达到 34.7，远超所有基线方法（次高为 SceneVerse 的 20.4），同时双失败率（DF）最低（16.8%）。这意味着 SCENECOT 不仅在答案正确时更可能追溯到正确的实体，而且在答案错误时也更少出现 grounding 也错误的情况——推理失败时至少 grounding 仍可能正确，为诊断和改进提供了抓手。

**消融实验**（Figure 5）：去除问题类型识别、区域识别或 grounding loss 均导致性能下降，验证了各组件的重要性。特别地，去除区域识别（将所有对象输入模型）显著降低了计数、指代和属性任务的性能，说明信息过滤是处理复杂场景的关键机制。

**Oracle 上界实验**（Table 3）：当提供完美的 ground-truth 掩码和标签后，计数任务得分从 47.9 跃升至 98.8，导航任务从基线提升至 87.2。这一结果揭示了两个关键事实：
1. grounding 质量是性能上限的核心约束——消除语义错误和 grounding 错误后，计数任务接近完美；
2. 即使 grounding 完美，空间关系等子任务仍有较大提升空间（导航仅达 87.2），说明当前的 CoT 设计在这些任务上仍不完善。

### 适用边界与局限

SCENECOT 的有效性受以下边界条件约束：

1. **任务类型受限**：当前框架仅限于 MSQA 中预定义的任务类型（计数、存在性、属性、空间关系、指代、导航），未涵盖长期具身任务规划等更复杂的场景。问题类型识别模块虽准确率达 99.4%（Table 14），但其分类体系是封闭的。

2. **场景多样性不足**：SCENECOT-185K 数据集仅基于 ScanNet 构建，场景类型以室内环境为主。模型在室外场景、动态场景或真实世界部署中的泛化能力未经验证。

3. **推理延迟高**：总推理时间约 10.4 秒（Table 13），其中大部分时间用于 LLM 序列生成。这一延迟限制了其在实时交互应用中的可行性。

4. **依赖检测质量**：实验中使用 ground-truth 掩码进行评估（Beacon3D），实际部署中依赖 Mask3D 等检测模型，其误差会沿推理链传播。Oracle 实验已证明语义错误和 grounding 错误是性能退化的主要来源。

5. **空间关系子任务瓶颈**：即使在 Oracle 条件下，空间关系相关任务的性能上限仍显著低于计数任务，表明当前 CoT 设计在该子任务上存在结构性不足。

### 开放问题

基于上述局限，以下问题值得进一步探索：

1. **思维链设计的改进空间**：如何针对空间关系等困难子任务重新设计推理链结构？是否需要在 CoT 中引入更丰富的空间推理原语（如相对坐标系变换、遮挡推理）？

2. **任务范围的扩展**：如何将逐步 grounding 推理范式扩展到具身任务规划、长期交互式推理等更开放的任务？这可能需要重新定义推理阶段和专家模块的接口。

3. **grounding 质量的上界突破**：Oracle 实验表明 grounding 质量是性能上限。除了改进检测模型，是否可以通过强化学习等方法让模型学会在 grounding 不确定时主动请求澄清或进行多轮验证？

4. **效率优化**：如何降低 10.4 秒的推理延迟？可能的路径包括：缓存区域识别结果、并行调用多模态专家、使用更轻量的推理引擎。

5. **训练动态平衡**：不同子任务对 grounding loss 的敏感度不同（Figure 5 显示存在性任务受影响较小），如何平衡多任务训练以避免性能失衡？

6. **真实场景验证**：在更多样的真实场景（如 AR/VR 环境、机器人操作场景）中验证方法的有效性和鲁棒性。

## 原文 PDF

![[paperPDFs/ICLR_2026/SceneCOT_Eliciting_Grounded_Chain_of_Thought_Reasoning_in_3D_Scenes.pdf]]
