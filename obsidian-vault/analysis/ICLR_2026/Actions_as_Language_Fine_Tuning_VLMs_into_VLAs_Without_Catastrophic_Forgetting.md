---
title: "Actions as Language: Fine-Tuning VLMs into VLAs Without Catastrophic Forgetting"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Actions_as_Language_Fine_Tuning_VLMs_into_VLAs_Without_Catastrophic_Forgetting.pdf
aliases:
- AALFTVIVWCF
- VLM2VLA
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/robotics
core_operator: "通过在数据层面将底层动作重新表示为自然语言描述（例如“向前移动 4.2 厘米”），使 VLA 的微调数据与 VLM 的预训练表示空间对齐，从而仅用低秩适配（LoRA）即可高效学习机器人策略，避免大幅修改预训练权重，从根本上阻断遗忘。"
primary_logic: "“动作即语言”的数据重标注流程将机器人控制转化为标准的有监督文本生成任务，无需任何架构改动或昂贵的大规模共训练，就能在学会控制的同时完整保留 VLM 的感知、推理和多语言能力，并赋予其对全新任务和指令的零样本泛化。"
claims:
- "语言化的动作表示在基座模型 Gemma‑3‑12B‑IT 下获得的对数概率远高于基于离散 token 的表示，直观证明了数据分布对齐。"
- "VLM2VLA 在 12 项多模态理解基准上保持了基座模型 85% 以上的性能（如 MMB‑en 70.9），而 OpenVLA、ECoT 等 VLA 几乎完全丧失这些能力（多数指标为 0）。"
- "在分布外（OOD）真实机器人操作任务中，VLM2VLA 取得显著高于 ECoT、OpenVLA 的成功率（如‘Pick Up the Item Above Ash Ketchum’任务 60% vs. 30%），并展现零样本多语言指令跟随。"
- "消融实验（VLM2VLA‑NR 移除层次化推理，VLM2VLA‑AT 采用离散 token 动作）均导致 OOD 成功率大幅下降，证实语言表示和分层推理两者缺一不可。"
---

# Actions as Language: Fine-Tuning VLMs into VLAs Without Catastrophic Forgetting

> [!tip] 核心洞察
> “动作即语言”的数据重标注流程将机器人控制转化为标准的有监督文本生成任务，无需任何架构改动或昂贵的大规模共训练，就能在学会控制的同时完整保留 VLM 的感知、推理和多语言能力，并赋予其对全新任务和指令的零样本泛化。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | 行动即语言：微调视觉语言模型为视觉语言行动模型而不发生灾难性遗忘 |
| 英文题名 | Actions as Language: Fine-Tuning VLMs into VLAs Without Catastrophic Forgetting |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=sFO9d6XSlf) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/robotics |
| Method | VLM2VLA |
| Dataset | MMB-en (多模态理解), MMMU (多模态理解), Pick Up the Item Above Ash Ketchum (OOD 机器人操作) |

> [!tip] 效果简介
> - MMB-en (多模态理解) 上，准确率 为 70.9，对比 55.1 (MolmoAct)，变化 +15.8。
> - MMMU (多模态理解) 上，准确率 为 45.9，对比 46.0 (Gemma-3-12B-IT, 原始 VLM)，变化 -0.1。
> - Pick Up the Item Above Ash Ketchum (OOD 机器人操作) 上，任务成功率 为 60%，对比 30% (ECoT)，变化 +30%。

## 概述

将视觉语言模型微调为视觉语言行动模型时，现有方法面临一个根本性的分布不匹配：机器人遥操作数据中的低层动作表示与视觉语言模型的预训练文本-图像分布存在显著差异。这一不匹配导致全参数微调或架构改造时发生灾难性遗忘，使模型丧失通用视觉理解和推理能力。VLM2VLA通过从数据层面将底层动作重新表示为自然语言描述，使微调数据与视觉语言模型的预训练表示空间对齐，从而仅用低秩适配即可高效学习机器人策略，从根本上阻断遗忘。

该方法将动作预测转化为一个基于视觉问答的分层推理过程，高层子任务预测、中层运动规划和低层动作生成均以自然语言形式输出。数据重标注管线借助Gemini 2.5 Pro自动将原始机器人轨迹分解为包含子任务、运动计划和动作块的语言描述，在无需任何架构改动或大规模共训练的前提下，使模型在学会控制的同时完整保留了视觉语言模型的感知、推理和多语言能力。

核心实验证据表明：VLM2VLA在12项多模态理解基准上保持了基座模型85%以上的性能，而OpenVLA、ECoT等视觉语言行动模型几乎完全丧失这些能力；在分布外真实机器人操作任务中取得显著更高的成功率，在“Pick Up the Item Above Ash Ketchum”任务上达到60%的成功率，远超ECoT的30%；消融实验进一步证实，用离散token替代语言动作或移除分层推理均导致分布外泛化能力大幅下降，其中移除分层推理使长流程任务性能严重退化，而离散token表示使依赖世界知识的任务成功率仅为语言表示的一半。

上述结果表明，“动作即语言”的数据表示范式通过将机器人控制转化为标准的有监督文本生成任务，有效解耦了策略学习与通用能力保持之间的矛盾，为构建不遗忘预训练能力的通用视觉语言行动模型提供了简洁而高效的路径。

## 背景与动机

将大规模预训练的视觉语言模型（VLM）转化为能够理解场景并输出底层控制指令的视觉语言行动模型（VLA），是当前机器人学习的前沿方向。此类转化的核心瓶颈在于：机器人遥操作数据中使用的低层动作表示，无论是将连续动作离散化并映射到模型词汇表中概率极低的 token（如 OpenVLA、ECoT），还是附加独立于 VLM 文本空间的连续动作头（如 MolmoAct、π0.5），**都与 VLM 预训练时所见的自然图像‑文本分布存在根本性的分布不匹配**。这种不匹配导致在微调阶段不得不大幅扰动模型参数，从而 **诱发灾难性遗忘**：VLA 在获得操纵能力的同时，几乎完全丧失 VLM 原本具备的通用视觉理解、常识推理与多语言能力（见 Figure 2 中央所示）。实验证明，现有 VLA 如 OpenVLA、ECoT 在经过机器人数据训练后，其在多项多模态理解基准（MMB‑en、MMMU 等）上的得分接近于零，无法继承基座 VLM 的世界知识（Table 1）。

一个关键的因果观察来自对基座模型概率行为的分析：在未经任何机器人微调时，Gemma‑3‑12B‑IT 对以自然语言形式表达的动作文本（例如“向前移动 4.2 厘米”）所赋予的对数概率，远高于对离散 token 映射动作的概率（Figure 3）。这说明**语言化的动作表示天然落在 VLM 预训练分布的支撑集上**；反过来，传统离散 token 表示则处于分布边缘，强制模型去记忆与文本生成无关的映射模式，从而压垮了预训练权重。

基于此，本文的核心动机是：**在数据层面将底层动作重新定义为自然语言描述**，使 VLA 的监督信号与 VLM 的预训练表示空间完全对齐。这种设计将机器人控制重构为标准的有监督文本生成任务，进而允许仅使用低秩适配（LoRA）对 VLM 进行微调，在几乎不修改预训练权重的前提下习得策略，从根源上阻断灾难性遗忘。由此，VLM2VLA 的目标是在学会灵巧操纵的同时，完整保留基座模型原有的感知、推理与多语言能力（Figure 1），并赋予其对全新任务和指令的零样本泛化。

## 核心创新

### 瓶颈：微调 VLM 为 VLA 时的分布失配与灾难性遗忘

将视觉语言模型（VLM）微调为视觉语言行动模型（VLA）的核心障碍在于**数据表示层面的根本性不匹配**。机器人遥操作数据中的底层动作——无论是被离散化为新添加的特殊 token（如 OpenVLA 的做法，将数值映射到模型词汇表中概率最低的 token），还是通过独立的连续动作头（如 MolmoAct、π0.5）输出——与 VLM 基座模型在海量文本-图像数据上建立的预训练分布完全脱节。这种分布断裂导致全参数微调或大规模架构改造时，模型迅速偏离原有的知识空间，丧失通用视觉理解、常识推理和指令跟随能力（图 2 直观对比了传统 VLA 的过拟合现象与保留世界知识的目标状态）。

VLM2VLA 的核心创新在于**识别出这层数据分布冲突并将其从源头化解**，而非在模型层面进行复杂的权衡或大规模共训练。

### 关键洞见：“动作即语言”

论文提出的解决方案具有方法论上的简洁性与根本性：**将底层动作重新表示为自然语言文本**，直接嵌入 VLM 原有的词汇空间。具体而言，连续的动作向量（如末端执行器位移 `dx, dy, dz`）被转换为形如 “Move forward 4.2 cm” 的自然语言描述。这一设计消除了动作空间与文本空间之间的模态鸿沟，使得机器人控制策略的学习退化为标准的有监督文本生成任务。

这一对齐的有效性在基座模型 Gemma‑3‑12B‑IT 上获得了先验验证：在微调前，模型对语言化动作表示赋予的对数概率显著高于基于最小概率 token 分配的离散表示（图 3），直观证明了语言动作天然落在预训练分布的高密度区域，而人为修改的 token 映射则处于概率尾部。正是这种数据层面的亲和性，使得后续的微调只需通过低秩适配（LoRA）对 VLM 基座进行极小扰动即可完成，从根本上阻断了灾难性遗忘的发生路径。

### Changed Slot：相对于基线方法的范式转换

| 维度 | 基线方法 | VLM2VLA |
|------|----------|---------|
| **动作表示** | 离散化至最小概率 token（OpenVLA、ECoT）或独立连续动作头（MolmoAct、π0.5） | 自然语言文本（如 “Move forward 4.2 cm”），嵌入 VLM 原有词汇空间 |
| **微调方式** | 全参数微调或大规模架构改造，需额外硬件对齐（如 π0.5 的共训练） | 仅对所有线性层施加 LoRA（rank=16），基座架构完全不变 |
| **任务定义** | 端到端动作映射 | 三阶段视觉问答式分层推理：子任务预测 → 运动规划 → 动作生成 |
| **数据闭环** | 依赖原始数据标注 | 利用 Gemini 2.5 自动将轨迹重标注为自然语言子轨迹（含子任务、运动计划、动作块） |

这一范式转换的深层含义在于：VLM2VLA **不引入任何新的网络架构组件**（无动作头、无新的可学习 token），也不依赖昂贵的大规模视觉-语言-行动共训练。它仅通过数据重标注和推理模板设计，就将机器人控制完全纳入 VLM 的预训练能力范畴。

### 分层推理：将控制转化为有监督文本生成

VLM2VLA 将策略分布显式分解为三个条件概率的乘积：

$$
p_{\theta}(\bar{a}_i, m_i, l_i \mid \bar{o}_i, L) = \underbrace{p_{\theta}(l_i \mid \bar{o}_i, L)}_{\text{子任务预测}} \; \underbrace{p_{\theta}(m_i \mid l_i, \bar{o}_i)}_{\text{运动规划}} \; \underbrace{p_{\theta}(\bar{a}_i \mid m_i, l_i, \bar{o}_i)}_{\text{动作生成}}
$$

其中 $l_i$ 为高层子任务（如 “grasp the pepper”），$m_i$ 为中层运动计划（如 “move left 3 cm then down 5 cm”），$\bar{a}_i$ 为底层动作块，$L$ 为语言指令，$\bar{o}_i$ 为观测历史。这一分解将复杂的控制策略拆解为由粗到细的文本推理链，每一步都产生可解释的自然语言输出。消融实验（图 8）证实，移除这一推理结构（VLM2VLA‑NR）会导致长流程分布外（OOD）任务的成功率大幅下降，证明子任务分解和运动规划对泛化至关重要——仅有语言动作表示而不具备分层推理能力，模型在需要世界知识和多步规划的场景中仍然脆弱。

### 测试时闭环验证：弥补自我评估能力的不足

尽管 VLM2VLA 能通过分层推理生成规划，但模型自身尚无法可靠判断子任务是否成功完成。为此，论文引入了一个外部的测试时闭环验证器

$$
V : \mathcal{O} \times \mathcal{O} \times \mathcal{L} \times \mathcal{L} \to \mathcal{L}
$$

利用 Gemini 2.5 Pro 比较执行前后的图像观测和当前/下一个子任务描述，输出语言判定以决定是继续当前子任务、进入下一步还是重新尝试。这一设计在模型本身的验证能力不足与系统闭环可靠性需求之间取得了实用折衷——尽管引入了外部依赖，但它确保了长流程操作的鲁棒性，同时也指出了未来的优化方向（训练 VLM 自身兼具验证功能）。

### 决定性证据要点

1. **先验概率对齐**（图 3）：Gemma‑3‑12B‑IT 在微调前对语言动作的 log-probability 远高于离散 token 表示（置信度 0.95）。
2. **多模态能力保持**（表 1）：VLM2VLA 在 MMMU 上得分 45.9，仅比原始 VLM 下降 0.1；在 MMB‑en 上达 70.9，而 OpenVLA、ECoT 等基线在多模态基准上几乎完全丧失能力（置信度 0.95）。
3. **OOD 操控泛化**（图 5）：在需要世界知识的任务（如 “Pick Up the Item Above Ash Ketchum”）上，VLM2VLA 成功率 60%，远超 ECoT 的 30%（置信度 0.9）。
4. **双消融验证**（图 8）：移除分层推理（VLM2VLA‑NR）或替换为离散 token 动作（VLM2VLA‑AT）均显著降低 OOD 成功率，后者在需世界知识的任务上表现约为完整方法的一半（置信度 0.95）。
5. **跨架构泛化**（图 8、图 9）：基于 Qwen‑2.5 的 VLM2VLA‑Q 取得与主模型接近的成功率与规划能力，证明 “动作即语言” 方法不绑定特定 VLM 架构（置信度 0.9）。

## 整体框架

![[assets/figures/papers/iclr26_0006_sFO9d6XSlf_Actions_as_Language_Fine-Tuning_VLMs_into_VLAs_W/figures/001_Figure_1.jpg]]
*Figure 1: We present VLM2VLA, a data pipeline and training methodology for fine-tuning VLMs into VLAs Out-of-Distribution After grasping, lift the pepper vertically (+dz) to clear the stove t Datawhile preserving their foundational perceptual and reasoning capabilities. Our policy retains its pretraining knobs, then move horizontally forward (+dx) and slightly right knowledge, enabling strong VQA performance and superior generalization in real robotic manipulation tasks*

![[assets/figures/papers/iclr26_0006_sFO9d6XSlf_Actions_as_Language_Fine-Tuning_VLMs_into_VLAs_W/figures/004_Figure_4.jpg]]
*Figure 4: VLM2VLA's pipeline for annotating existing robot datasets ${ \mathcal { D } } _ { \mathrm { r o b } }$ into $\mathcal { D } _ { \mathrm { l a n } }$ described via natural language. We use Gemini 2.5 (Team, 2025) to decompose each trajectory into sub-trajectories, each with an associated subtask, motion plan, and action chunk

VLM2VLA 的总体流水线围绕一个核心设计：将低层机器人动作表示为自然语言文本，使策略学习与视觉语言模型（VLM）的预训练表示空间完全对齐。这一设计使得只需对 VLM 施加轻量的低秩适配（LoRA）即可完成机器人控制训练，从而在根源上阻断灾难性遗忘。整个框架可划为三个紧密协作的阶段：**数据重标注**，将原始遥操作轨迹转化为语言化的策略监督；**分层视觉推理**，在推理时将决策过程分解为子任务规划、运动描述与动作生成三步问答；以及**闭环验证**，通过外部验证器实现基于子任务完成状态的可靠执行控制（图1）。

### 数据重标注：将动作转化为语言

框架的起点是对机器人数据集 $D_{\text{rob}}$ 中的原始轨迹 $\boldsymbol{\tau} = \{(o_t, a_t)\}_{t=0}^{T}$ 进行自动化重标注。利用 Gemini 2.5，每条轨迹被分解为若干子轨迹，每个子轨迹由一张视觉观测和一段自然语言描述组成，其描述包含三个层次：**子任务**（如“抓起胡萝卜”）、**运动计划**（如“向前平移接近物体”）以及一个**动作块**。动作块直接以自然语言指定末端执行器的平移量，例如“向前移动 4.2 厘米”，从而将原本连续或离散化的动作信号彻底转化为 VLM 原生支持的文本预测形式（图4）。

这一标注流程的本质是改变监督信号的模态：控制输出不再是独立于语言空间的特殊 token，而是嵌入在 VLM 原有词汇分布中的自然语言。实验证据表明，在未经微调的 Gemma‑3‑12B‑IT 模型下，语言化动作的对数概率远高于基于离散 token 的表示（图3），直观验证了数据分布对齐的有效性。

### 分层推理：三阶段视觉问答式动作生成

在推理时，VLM2VLA 将策略判决显式分解为一个三阶段的分层推理过程，整体概率模型为：

$$
p_{\theta}(\bar{a}_i, m_i, l_i \mid \bar{o}_i, L) = \underbrace{p_{\theta}(l_i \mid \bar{o}_i, L)}_{\text{1) 子任务预测}} \ \underbrace{p_{\theta}(m_i \mid l_i, \bar{o}_i)}_{\text{2) 运动规划}} \ \underbrace{p_{\theta}(\bar{a}_i \mid m_i, l_i, \bar{o}_i)}_{\text{3) 动作生成}}
$$

其中 $L$ 为高层次语言指令，$\bar{o}_i$ 为当前视觉观测，三个条件概率分别对应：
1. **子任务预测**：模型先根据完整指令和当前观测，输出当前应执行的子任务 $l_i$；
2. **运动规划**：结合子任务 $l_i$ 与观测，生成一个更高层的运动描述 $m_i$（如“向右平移至锅上方”）；
3. **动作生成**：在运动规划 $m_i$ 的引导下，直接输出语言化的低层动作序列 $\bar{a}_i$（如“向右移动 1.2 厘米，向前移动 3.5 厘米”）。

三步均以自然语言形式输出，使得整个推理链条能够最大限度地复用 VLM 的预训练视觉理解和常识推理能力。消融实验中，移除这一分层推理结构（VLM2VLA‑NR）会导致长时序任务成功率大幅下降，证实子任务分解与运动规划对策略泛化至关重要。

### 微调策略：LoRA 下的最小架构改动

微调阶段直接在 Gemma‑3‑12B‑IT 基座模型上进行，**不修改任何 VLM 架构**。所有线性模块（q‑proj, k‑proj, v‑proj, o‑proj, up‑proj, down‑proj, gate_proj）上仅施加低秩适配（LoRA），秩 $r=16$，缩放因子 $\alpha=32$，训练时仅优化新增的低秩矩阵，大幅减少对原本预训练权重的扰动。正因动作本身已嵌入语言空间，LoRA 就足以学习机器人策略拟合，而无需全参数微调或引入独立的动作头，从而有效避免了灾难性遗忘，使模型在多模态理解基准上仍保留超过 85% 的原始性能。

### 闭环验证：任务完成的外驱判定

VLM2VLA 在测试时以闭环方式运行，引入一个外部验证器 $V : \mathcal{O} \times \mathcal{O} \times \mathcal{L} \times \mathcal{L} \to \mathcal{L}$，利用 Gemini 2.5 Pro 对比动作执行前后的视觉观测与子任务文本，判定当前子任务是否已成功完成。验证器的输出直接决定下一周期是继续执行同一子任务（重试），还是切换到下一子任务。该机制将执行可靠性与策略推理解耦，弥补了 VLM 自身尚不具备可靠子任务验证能力的不足，同时为更高成功率的长时间操作任务提供保障。

## 核心模块与公式推导

**动作即语言**是 VLM2VLA 的核心设计。它将机器人低层动作直接表示为自然语言文本（例如“向前移动 4.2 厘米”），嵌入预训练 VLM 原有的词汇空间。这一数据级对齐使机器人行为学习与 VLM 的文本‑图像条件分布高度相容，进而仅用低秩适配（LoRA）即可微调基座模型，大幅减少对重参数的扰动，从根本上阻断灾难性遗忘。

### 数据重标注管线
原始机器人遥操作轨迹 $\boldsymbol{\tau} = \{ (o_t, a_t) \}_{t=0}^{T}$（$o_t$ 为观测，$a_t$ 为动作）需转换为自然语言描述的监督样本。管线利用外部视觉‑语言模型（Gemini 2.5）将每条轨迹分解为若干子轨迹，每条子轨迹附带：
- 高层**子任务** $l_i$（如“将胡萝卜移至碗中”）；
- 中层**运动计划** $m_i$（空间走向与预接触描述）；
- 低层**动作块** $\bar{a}_i$（以语言表述的末端平移量，如“向右移动 3.5 厘米”）。

分解后还经过后处理（沿单维设置 2.5 cm 阈值合并微小动作），形成的数据集 $\mathcal{D}_{\mathrm{lan}}$ 直接作为下一步微调的语料。

### 分层推理模块
策略将动作预测构造为三阶段视觉问答（VQA）式生成过程，其联合分布分解为

$$
p_{\theta}(\bar{a}_i, m_i, l_i \mid \bar{o}_i, \mathcal{L})
= \underbrace{p_{\theta}(l_i \mid \bar{o}_i, \mathcal{L})}_{\text{1) 子任务预测}}
\; \underbrace{p_{\theta}(m_i \mid l_i, \bar{o}_i)}_{\text{2) 运动规划}}
\; \underbrace{p_{\theta}(\bar{a}_i \mid m_i, l_i, \bar{o}_i)}_{\text{3) 动作生成}}
$$

变量含义：
- $\mathcal{L}$：顶层语言指令；
- $\bar{o}_i$：当前子轨迹对应的图像观测（可能为多帧）；
- $l_i, m_i, \bar{a}_i$：分别表示第 $i$ 个子任务、运动计划与自然语言动作块。

该分解将复杂控制解耦为可解释的、可逐项优化的高、中、低层推理步骤，每一层均使用语言作为输出媒介，确保整个过程完全处于 VLM 的自回归文本生成能力之内。

### LoRA 微调模块
得益于动作语言表示与预训练分布的对齐，微调只需对 Gemma‑3‑12B‑IT 的所有线性模块（`q‑proj`, `k‑proj`, `v‑proj`, `o‑proj`, `up‑proj`, `down‑proj`, `gate_proj`）施加低秩适配（rank=16, alpha=32），无需引入任何独立动作头或架构改造。训练仅使用交叉熵损失，持续一个 epoch（约 300 GPU 小时，有效全局批量大小 8）。这种方式最大程度保留了 VLM 原有的多模态理解与推理能力。

### 测试时闭环验证器
执行阶段引入验证器 $V : \mathcal{O} \times \mathcal{O} \times \mathcal{L} \times \mathcal{L} \to \mathcal{L}$，其输入为动作执行前后的图像观测和当前/下一子任务文本，输出为语言形式的完成判定（“成功”或“未完成”）。若判定未完成，则重试当前子任务；成功后切换至下一子任务。论文使用 Gemini 2.5 Pro 实现该验证器，构成外循环的闭环控制。

**关键证据提示**：动作语言表示使基座模型（微调前）对语言化动作赋予的对数概率显著高于离散 token 表示（Figure 3），直接验证了分布对齐。消融实验（Figure 8、Figure 9）表明，若移除层次化推理（VLM2VLA‑NR）或改用离散 token（VLM2VLA‑AT），分布外任务成功率均大幅下降，特别在多语言指令和需要常识知识的情景中差距尤为明显。这证实了语言表示与分层推理两者缺一不可。

## 实验与分析

### 主结果：视觉-语言能力留存与机器人操作泛化
VLM2VLA 的核心主张是：通过将低层动作表示为自然语言，可以在不改变视觉-语言模型（VLM）架构、仅用低秩适配（LoRA）的条件下，将 VLM 微调为视觉-语言行动模型（VLA），并**根除灾难性遗忘**。实验从多模态理解保持和真实机器人操作两个层面验证这一主张。

**多模态理解留存。** 在 12 项多模态理解基准上（Table 1），VLM2VLA（基于 Gemma-3-12B-IT）几乎完整保留了基座模型的能力。例如，最艰难的跨学科推理任务 MMMU 上，VLM2VLA 仅下降 0.1 个点（45.9 vs. 基座 46.0），远优于任何现有 VLA——OpenVLA、ECoT 在同一基准上几乎丧失所有能力（多数指标为 0）。在综合理解任务 MMB-en 上，VLM2VLA 拿到 70.9，较同样引入机器人训练的 MolmoAct 高出 15.8 分。这表明，**“动作即语言”从根本上规避了低层动作头或离散动作 token 带来的分布失配**，从而保护了预训练权重中储存的感知与推理知识。


![[assets/figures/papers/iclr26_0006_sFO9d6XSlf_Actions_as_Language_Fine-Tuning_VLMs_into_VLAs_W/figures/005_Table_1.jpg]]
*Table 1: Multimodal understanding evaluation. Comparison of VLMs and VLAs across multimodal understanding benchmarks. We compare against Prismatic VLM (Karamcheti et al., 2024), OpenVLA (Kim et al., 2024), ECoT (Zawalski et al., 2025), Gemma-3 (Team et al., 2025b), Molmo Deitke et al. (2024), MolmoAct (Lee et al., 2025), PaliGemma Beyer et al. (2024), and $\pi _ { 0 . 5 }$ (Intelligence et al., 2025). Our models preserve strong performance across diverse multimodal understanding tasks despite only training on robot data. The best and second best results for each benchmark are shown in bold and underlined, respectively*

**机器人操作性能。** 在分布外（OOD）真实机器人操作任务中，VLM2VLA 展现出远超对比方法的泛化能力（Figure 5）。以显著依赖世界知识的任务 `Pick Up the Item Above Ash Ketchum` 为例，VLM2VLA 取得了 60% 的成功率，而 ECoT 仅为 30%，OpenVLA 几乎无法完成。在包含多语言指令（印地语、泰卢固语等）的复杂任务中，VLM2VLA 不仅能够正确生成层次化推理，还展现出零样本跨语言物体识别与操作能力（Figure 7）。这一特性来源于语言动作与 VLM 预训练中多语言语料的对齐，使得模型能够将印地语指令“गाजर उठाओ”准确映射到物理世界的胡萝卜上，并规划出正确的抓取动作，而无需任何多语言机器人数据训练。


![[assets/figures/papers/iclr26_0006_sFO9d6XSlf_Actions_as_Language_Fine-Tuning_VLMs_into_VLAs_W/figures/006_Figure_5.jpg]]
*Figure 5: Comparative evaluation of VLA performance on in-distribution (ID) and out-of-distribution (OOD) robotic manipulation tasks. VLM2VLA maintains high success rates on OOD tasks, highlighting its superior generalization capabilities. Each bars corresponds to an average over thirty trials, except for the 'Pick Up - T' task, where each bar corresponds to an average over ninety trials*

任务分解分析（Figure 6）进一步揭示了上述泛化的来源：VLM2VLA 在 OOD 任务中正确识别目标物体和目的地的比例显著高于 OpenVLA 和 ECoT，说明保留的视觉-语言推理能力是其鲁棒执行的基础。

### 消融分析：语言表示与分层推理缺一不可
为量化两个关键设计要素——**语言动作表示**和**层次化推理**——的贡献，论文进行了系统消融（Figure 8, Figure 9）。


![[assets/figures/papers/iclr26_0006_sFO9d6XSlf_Actions_as_Language_Fine-Tuning_VLMs_into_VLAs_W/figures/009_Figure_8.jpg]]
*Figure 8: Comparative evaluation of VLM2VLA ablations on in-distribution (ID) and out-of-distribution (OOD) robotic manipulation tasks. VLM2VLA maintains high success rates on OOD tasks relative to ablated variants, highlighting the importance of reasoning and the robustness of our methodology across different model architectures. Each bar corresponds to an average over thirty trials, except for the 'Pick Up - T' task, where each bar corresponds to an average over ninety trials*

**移除层次化推理（VLM2VLA‑NR）**：该变体直接根据图像和指令生成低层动作，跳过了子任务预测和运动规划。在长周期 OOD 任务上，VLM2VLA‑NR 的成功率出现严重退化，证明将复杂指令分解为子任务、再为每个子任务生成运动计划的分层推理过程，是处理长时序、强泛化要求的必要条件，而非多余的装饰。

**替换为离散动作 token（VLM2VLA‑AT）**：该变体将所有连续动作量化为 Gemma‑3 词表中最小概率的 token（映射关系见 Table 2），从而模拟 OpenVLA 等基线方法的动作表示方式。VLM2VLA‑AT 在需要常识或语言理解的 OOD 任务中，成功率仅为完整模型的约一半（如 `Ash Ketchum` 任务 30% vs. 60%），且在多语言指令面前几乎失败。这与预训练概率分析（Figure 3）高度一致：基座 Gemma‑3‑12B‑IT 赋予语言动作的对数概率远高于最小概率 token 构成的“假词汇”，因此后者在微调时会迫使模型大幅修改预训练表示，诱发遗忘。


![[assets/figures/papers/iclr26_0006_sFO9d6XSlf_Actions_as_Language_Fine-Tuning_VLMs_into_VLAs_W/figures/003_Figure_3.jpg]]

**跨架构泛化（VLM2VLA‑Q）**：将基座模型更换为 Qwen‑2.5 并同样采用语言动作表示训练后，VLM2VLA‑Q 在大部分 OOD 任务上取得了与 VLM2VLA 相近的成功率，且在任务分解上具备几乎相当的规划能力（Figure 9）。唯一的性能差距主要来源于动作执行的精度，而非推理层面的缺陷。这证明了“动作即语言”的方法是模型无关的，可看作一种通用数据范式。

### 失败模式与关键限制
尽管在 OOD 泛化上表现突出，VLM2VLA 的能力边界仍受以下因素制约：

1. **有限的动作空间**：当前仅支持末端执行器的三维平移（dx, dy, dz），不包含旋转和复杂夹爪控制。这直接将模型限制在桌面级抓取-放置类任务中，无法处理需要精细姿态调整的灵巧操作。
2. **外部重型依赖**：数据重标注和测试时闭环验证均依赖外部大模型 Gemini 2.5 Pro。VLM2VLA 自身尚不能可靠判断子任务是否完成，这导致闭环控制系统引入高昂的计算与延迟开销，并产生外部依赖风险。
3. **推理延迟偏高且分布右偏**：自回归生成动作文本的过程导致单次推理中位数为 6.1 秒，但约有 10% 的试验触发重试，使得最大值可达 48.8 秒（Table 3）。这种长尾延迟严重阻碍实时控制的应用。
4. **训练数据规模受限**：本轮实验仅在 Bridge V2 数据集的一个子集（约数百条轨迹）上进行微调，数据多样性和数量均有限。更大规模的多任务、多场景训练是否能够释放更强的零样本指令跟随和跨任务泛化，仍是待验证的开放问题。

总体来看，实验证据强度较高，所有主要声明均有多项定量基准（Table 1）、多维真实机器人实验（Figure 5, 8）和概率分析（Figure 3）支持。上述失败模式也由论文明确承认并作为未来工作方向，但动作空间与延迟问题在实际部署中值得进一步手动验证。

## 方法谱系与知识库定位

### 与主流 VLA 基线的结构性对比

VLM2VLA 的提出直接回应了当前 VLA 微调范式中的核心矛盾：**如何在注入机器人控制能力的同时，阻止视觉-语言基座模型的灾难性遗忘**。这一矛盾在不同基线方法中表现为不同的折中方案，而 VLM2VLA 的选择——从数据层面将动作重铸为自然语言——源于对这些基线失效机制的诊断。

**离散 token 化动作 VLA（OpenVLA、ECoT）**：这类方法将底层动作（如末端位移量）映射到 VLM 词表中的特定 token（通常是最小概率 token），然后在机器人数据上进行全参数或大范围微调。其根本问题在于：这些新引入的 token 表示与 VLM 预训练过程中的文本-图像联合分布之间存在严重的分布不匹配。Figure 3 的实验直观揭示了这一不匹配的量化程度：在未经微调的 Gemma‑3‑12B‑IT 基座模型下，语言化动作表示（如“向前移动 4.2 厘米”）获得的对数概率远高于基于离散 token 的表示。这意味着，离散 token 方案在训练伊始就将模型推向了其预训练知识边界之外的未知空间，全参数微调进一步迫使模型覆盖掉原有的泛化能力以拟合这些“异常 token”。后果是灾难性的：Table 1 显示，OpenVLA 和 ECoT 在 MMB‑en 等多模态理解基准上的指标几乎归零（ECoT 在所有 12 项 VQA 基准上得分为 0），成为本质上只能执行预设动作的“控制专用模型”，丧失了理解复杂指令、多语言指令及常识推理的能力。

**连续动作头 VLA（MolmoAct、π0.5）**：这类方法试图通过保留 VLM 主体、外接独立动作预测头来隔离遗忘，代表了一种“架构隔离”策略。MolmoAct 在 Table 1 中的多模态理解得分（MMB‑en 55.1）确实显著优于离散 token 方法，但仍远低于原始基座模型，且低于 VLM2VLA 的 70.9。更关键的是，架构隔离并未解决表示层面的一致性问题——动作预测模块与文本生成模块仍然是两个异构的输出空间，模型在原有多模态推理与新任务之间依然存在竞争。π0.5 则通过大规模共训练（co‑training）来缓解这一问题，试图用海量数据“覆盖”遗忘，但这属于计算密集型方案，与 VLM2VLA 的轻量级 LoRA 微调（仅 300 GPU hours）形成显著成本差异。

**VLM2VLA 的差异化定位**：VLM2VLA 不采用架构隔离，也不引入新的 token 空间，而是从根本上消除表示不匹配。通过将底层动作重新表示为自然语言文本（如“向前移动 4.2 厘米”），它使 VLA 的微调数据完整地嵌入 VLM 的已有词汇与语义空间，从而将机器人策略学习转化为标准的有监督文本生成任务。这正是其“行动即语言”核心洞察力的体现：**不是让模型适应新的动作表示，而是让动作表示适应模型的已有知识**。这一选择使得 LoRA 微调（rank=16, alpha=32, 仅作用于所有线性层）足以高效学习控制策略，无需大幅修改预训练权重。

### 消融实验的因果归因

论文通过两类关键消融实验验证了方法选择的有效性：

- **VLM2VLA‑AT（使用离散 token 替代语言动作）**：该消融版本在 OOD 任务上的成功率大幅下降，在需要世界知识的任务中（如多语言指令跟随、基于常识的物体识别）成功率仅约为完整 VLM2VLA 的一半（Figure 8）。在“Pick Up the Item Above Ash Ketchum”（涉及对宝可梦角色 Ash Ketchum 的常识理解）任务中，完整方法达到 60% 成功率，而 AT 消融版本仅 30%。这表明语言对齐是 OOD 泛化的必要条件，而非充分条件。

- **VLM2VLA‑NR（移除分层推理，直接预测动作）**：该消融版本在长流程任务上表现显著恶化（Figure 8），证明子任务分解和运动规划模块对复杂任务的执行至关重要。值得注意的是，这种退化并非来自语言表示本身的失效，而是策略结构层面的缺失，说明“语言表示”与“分层推理”是两个独立且互补的因果机制。

- **跨架构泛化（VLM2VLA‑Q，基于 Qwen‑2.5）**：该版本在大多数任务上与基于 Gemma‑3 的 VLM2VLA 表现接近，并保持了相当的规划能力（Figure 9）。这验证了“动作即语言”策略不是特定于 Gemma 架构的技巧，而是一种**模型架构无关（model-agnostic）**的数据驱动范式。

### 适用边界与局限

尽管 VLM2VLA 在防遗忘与泛化性方面表现出色，其适用边界受限于以下结构性约束：

1. **动作空间的维度约束**：当前语言动作仅覆盖末端执行器的平移自由度（dx, dy, dz），未包含旋转和复杂夹爪控制。这意味着方法目前适用于桌面级抓取与放置任务，对于需要精细力控或多自由度协调的灵巧操作任务，其有效性尚待验证。将语言动作扩展到更高维度而同时保持文本表示的紧凑性与可解析性，是一个未解决的表示工程问题。

2. **外部依赖与闭环代价**：方法在两处依赖外部大语言模型（Gemini 2.5 Pro）：一是数据重标注管线，二是测试时的闭环验证器。这意味着系统并非完全端到端，且引入了额外的 API 调用延迟和外部服务依赖。论文明确指出，模型自身尚无法可靠完成子任务完成情况的验证（Part 006, open_questions），这限制了其作为完整自主系统的部署便捷性。

3. **推理延迟的实际约束**：自回归生成动作文本导致推理延迟分布较宽：中位数为 6.1 秒，IQR 为 5.0–6.7 秒，但最大值可达 48.8 秒（Table 3），且约 10% 的运行触发重试流程。这一延迟水平对于需要实时响应的动态操作任务构成明显瓶颈，实际部署中需要更高效的解码策略。

4. **训练数据集规模与多样性**：训练数据仅源自 Bridge V2 数据集的子集（约数百条轨迹），且由 Gemini 2.5 自动标注。虽然结果展示了令人印象深刻的泛化能力，但数据规模的有限性可能使泛化边界在面对完全未见的环境、物体或任务组合时变得脆弱。当前实验的 OOD 任务仍然处于语义相邻空间（桌面操作、类别级泛化），尚未测试跨场景域迁移（如从桌面操作到工业装配）的鲁棒性。

### 开放问题与研究展望

论文的研究路线图指向以下几个值得社区持续关注的方向：

- **实时推理的加速路径**：能否针对语言动作的解码开发专门的推测解码（speculative decoding）或结构化束搜索技术，在保持生成质量的同时将延迟压缩至亚秒级？这是从实验室演示走向实际部署的关键瓶颈。

- **动作空间的维度扩展**：将“动作即语言”范式推广至包含旋转、夹爪力控等更高维度空间时，是否需要更结构化的文本描述方案（例如引入闭环反馈相关的子 token 或分块描述）来平衡表达力与生成效率，这是一个表示设计的开放问题。

- **端到端闭环的自主化**：能否通过自训练或指令微调，使 VLM 自身同时承担策略和验证器角色，从而完全移除对外部大模型的依赖？这一方向如果实现，将使系统成为真正自包含的 VLA 智能体。

- **大规模预训练的潜力验证**：当前工作的效能上限可能受限于训练数据集规模。如果结合多任务、多场景的大规模机器人数据集（例如 Open X‑Embodiment），配合“行动即语言”的自动重标注流程进行预训练，是否会解锁更强的跨任务零样本指令跟随？这将是对该范式可扩展性的关键检验。

- **跨具身迁移的可能性**：论文提示了“动作即语言”重标注方案在跨具身策略学习中的潜在应用（Part 004）。由于语言表示天然地抽象于特定的机器人运动学和动力学，该范式与其他具身（如双臂机器人、移动操作平台）结合后，可能实现策略在具身平台间的迁移。但这需要解决不同本体的动作语义对齐问题，目前仍是一个开放假设。

**需要手动验证的边界声明**：论文未明确测试 VLM2VLA 在严重与训练分布偏离的视觉域（如极低光照、严重遮挡、非操作场景）下的退化模式。当前证据支持其在分布偏移下的强保持性，但灾难性遗忘是否完全被消除，还是仅被推至更极端的分布边界之外，尚需更大规模的应力测试确认。

## 原文 PDF

PDF 文件：paperPDFs/ICLR_2026/Actions_as_Language_Fine_Tuning_VLMs_into_VLAs_Without_Catastrophic_Forgetting.pdf

![[paperPDFs/ICLR_2026/Actions_as_Language_Fine_Tuning_VLMs_into_VLAs_Without_Catastrophic_Forgetting.pdf]]
