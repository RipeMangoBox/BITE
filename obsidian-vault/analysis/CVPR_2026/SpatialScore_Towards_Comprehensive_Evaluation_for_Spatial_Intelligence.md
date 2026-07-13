---
title: "SpatialScore: Towards Comprehensive Evaluation for Spatial Intelligence"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/SpatialScore_Towards_Comprehensive_Evaluation_for_Spatial_Intelligence.pdf
project_link: "https://haoningwu3639.github.io/SpatialScore/"
code_link: "https://github.com/haoningwu3639/SpatialScore/"
aliases:
- SBSTDSAF
- SpatialScore
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
- topic/benchmarks_datasets_evaluation
core_operator: 引入全面的多任务空间智能基准（SpatialScore）量化能力差距，并通过大规模空间推理训练数据（SpatialCorpus）进行监督微调，同时构建无需训练的智能体框架（SpatialAgent），集成了12个专业空间感知工具，以 Plan-Execute 和 ReAct 范式动态调用工具来增强推理能力。
primary_logic: 将视觉基础模型（如深度估计器、相机姿态估计器）作为工具集成到语言模型推理循环中，能够显著提升多模态大模型在复杂空间任务上的表现；全面的基准是推动该领域进步的必要条件。
claims:
- SpatialScore 上人类水平为 86.60，而最佳模型（Gemini-3-Pro）仅 60.12，差距巨大。
- 基于 SpatialCorpus 微调使 Qwen3-VL-8B 在 SpatialScore-Repurpose 上从 54.53 提升至 76.29。
- SpatialAgent-ReAct 在不进行任何微调的情况下将 Qwen3-VL-8B 在 SpatialScore-OpenSource 上的准确率从 42.97 提升至 50.01。
- SpatialAgent 成功通过调用工具（如深度估计、光流）逐步推理出正确空间属性（见图4定性结果）。
---

# SpatialScore: Towards Comprehensive Evaluation for Spatial Intelligence

> [!tip] 核心洞察
> 将视觉基础模型（如深度估计器、相机姿态估计器）作为工具集成到语言模型推理循环中，能够显著提升多模态大模型在复杂空间任务上的表现；全面的基准是推动该领域进步的必要条件。

| 字段 | 内容 |
|------|------|
| 中文题名 | 空间评分：迈向空间智能的全面评估 |
| 英文题名 | SpatialScore: Towards Comprehensive Evaluation for Spatial Intelligence |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2505.17012) · [Project](https://haoningwu3639.github.io/SpatialScore/) · [Code](https://github.com/haoningwu3639/SpatialScore/) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion #topic/benchmarks_datasets_evaluation |
| Method | SpatialScore (Benchmark), SpatialCorpus (Training Data), and SpatialAgent (Agent Framework) |
| Dataset | SpatialScore-OpenSource, SpatialScore-Repurpose |

> [!tip] 效果简介
> - SpatialScore-OpenSource 上，Overall accuracy 48.72 (Qwen3-VL-8B + SpatialCorpus) vs 42.97 (Qwen3-VL-8B zero-shot) (+5.75)；Overall accuracy 50.01 (Qwen3-VL-8B + SpatialAgent-ReAct) vs 42.97 (Qwen3-VL-8B zero-shot) (+7.04)。
> - SpatialScore-Repurpose 上，Overall accuracy 76.29 (Qwen3-VL-8B + SpatialCorpus) vs 54.53 (Qwen3-VL-8B zero-shot) (+21.76)；Overall accuracy 67.51 (Qwen3-VL-8B + SpatialAgent-ReAct) vs 54.53 (Qwen3-VL-8B zero-shot) (+12.98)。

## 概要

多模态大语言模型（MLLM）在通用视觉理解上取得了长足进步，但在严格的空间智能——如相机姿态估计、深度感知、运动追踪和视角推理——方面仍存在显著不足。现有评估基准存在两个关键瓶颈：**任务碎片化**，各基准仅覆盖少数空间维度，无法形成全面画像；**难度过低且范围狭窄**，难以区分模型真实能力与表面统计关联。这导致当前最佳模型与人类水平之间存在巨大的认知鸿沟。

针对上述问题，本文提出了一套系统性的解决方案，包含三个协同组件：

1.  **SpatialScore 基准**：首个面向多模态空间智能的全面评估基准，覆盖 10 个空间能力维度和 30 个具体任务，包含约 5K 经人工验证的高质量样本。该基准整合了来自 23 个公开数据集的空间相关样本，并首次利用 3D 标注数据重新构造了多样化的问答对（判断、多选、开放式），以严格测试模型的几何空间感知能力。

2.  **SpatialCorpus 训练语料**：一个包含 331K 多模态问答对的大规模空间推理训练集，用于监督微调，使模型内化空间关系与几何概念。

3.  **SpatialAgent 智能体框架**：一种无需训练的推理增强方法，将 12 个专业空间感知工具（如深度估计器、相机姿态估计器、光流/运动估计器）集成到 MLLM 的推理循环中，通过 Plan-Execute 和 ReAct 两种范式动态调用工具，逐步推理出复杂空间属性。

**核心发现**：在 SpatialScore 上，人类水平为 86.60，而当前最佳模型 Gemini-2.5-Pro 仅达到 60.12，差距显著（Table 2）。基于 SpatialCorpus 的微调使 Qwen3-VL-8B 在 SpatialScore-Repurpose 子集上从 54.53 提升至 76.29（Table 8）；而 SpatialAgent-ReAct 在不修改模型参数的情况下，将同模型在 SpatialScore-OpenSource 上的准确率从 42.97 提升至 50.01（Table 7）。这表明：**将视觉基础模型作为工具集成到语言模型推理中，能够显著增强空间智能；而全面的基准是推动该领域进步的必要条件。**

### 空间智能：多模态大模型的“阿喀琉斯之踵”

空间智能（Spatial Intelligence）是指智能体感知、推理并与三维世界交互的能力，涵盖深度估计、相机姿态理解、物体运动追踪、视角推理等核心技能。对于旨在实现通用人工智能的多模态大语言模型（MLLM）而言，空间智能是其理解物理世界、执行具身任务的关键基础。然而，当前最先进的 MLLM 在空间推理任务上的表现远逊于人类——SpatialScore 基准测试显示，人类水平为 **86.60**，而表现最好的专有模型 Gemini-3-Pro 仅达到 **60.12**，存在超过 26 个百分点的巨大认知鸿沟（Table 2 Overall）。

### 现有评估体系的三重缺陷

这一鸿沟的暴露，根源于现有空间智能评估基准存在三个系统性缺陷：

**碎片化与范围狭窄**。现有基准如 CV-Bench、SpatialSense、MMIU 等多聚焦于单一或少数几个空间子任务（如仅评估深度或仅评估空间关系），缺乏对空间智能全貌的覆盖。SpatialScore 的系统性对比（Table 1）表明，此前没有任何基准同时涵盖真实世界数据、AIGC 生成数据、单图/多图序列/视频等多种输入模态，以及判断、多选、开放式问答等多样化的问答格式。

**任务过于简单**。许多现有基准中的问题仅需浅层视觉特征即可回答，未能真正考验模型的几何空间推理能力。例如，部分数据集存在标注错误或歧义（Figure 5），使得模型可以通过表面模式匹配而非真正的空间理解来获得高分。

**缺乏规模化训练支撑**。即使有了更好的评估基准，MLLM 在空间推理上的训练数据仍然匮乏。通用多模态预训练数据以自然图像描述和常识问答为主，极少涉及严格的度量空间推理（如“物体 A 距离相机 2.3 米，物体 B 在 A 后方 1.5 米处”这类精确几何关系）。

### 本文的动机与核心回应

针对上述缺口，本文提出了一套“评估-数据-推理”三位一体的空间智能增强体系：

1. **SpatialScore**：构建迄今最全面的多模态空间智能基准，包含约 5K 人工验证样本，覆盖 30 个空间任务、10 个能力维度，首次系统量化了 49 个 MLLM 与人类之间的空间智能差距。

2. **SpatialCorpus**：构建大规模空间推理训练语料（331K QA 对），通过监督微调直接注入空间知识，弥补预训练阶段的空间推理数据不足。

3. **SpatialAgent**：提出无需训练的智能体框架，集成 12 个专业空间感知工具（深度估计器、相机姿态估计器、光流/运动估计器等），通过 Plan-Execute 和 ReAct 两种推理范式动态调用工具，以工具增强的方式弥补 MLLM 内生空间能力的不足。

这一体系的核心洞察在于：**将视觉基础模型作为工具集成到语言模型推理循环中，能够显著提升 MLLM 在复杂空间任务上的表现；而全面的基准是推动该领域进步的必要条件**。

## 核心方法与创新机理

SpatialScore 工作的核心创新并非提出一种全新的模型架构，而是围绕**评估基准、训练数据与推理范式**三个维度，系统性地弥补了现有多模态大模型（MLLM）在空间智能评估与增强上的关键缺口。其创新逻辑根植于一个明确的因果机制：**现有基准的碎片化与简单化掩盖了模型在严格几何空间感知（如相机姿态估计、深度推理、运动追踪）上的真实缺陷**，而通过构建全面基准量化这一差距，并分别从数据驱动与智能体驱动两条路径施加干预，能够显著提升模型的空间推理能力。

具体而言，相较于基线方法（如 Qwen3-VL、InternVL3 等通用 MLLM 的零样本直接推理），本工作在以下两个关键维度上实现了根本性的改变：

**1. 训练数据与优化目标的转变：从通用预训练到空间推理专项微调**
基线方法依赖于在大规模通用多模态数据上的预训练，直接进行零样本推理，缺乏对空间几何属性的显式建模。SpatialScore 通过构建 **SpatialCorpus**（包含 331K 高质量空间问答对的大规模训练资源），将优化目标从通用的图文对齐转向专门的空间推理能力。这一转变的因果效应在实验中得到了强有力的验证：基于 SpatialCorpus 对 Qwen3-VL-8B 进行监督微调后，模型在 SpatialScore-Repurpose 子集上的准确率从 54.53 跃升至 76.29（+21.76），在 SpatialScore-OpenSource 子集上亦提升 5.75 个百分点（Table 7, Table 8）。这表明，**注入大规模、多样化的空间推理监督信号是突破模型空间认知瓶颈的有效因果杠杆**，尽管其增益高度依赖于训练数据与评估任务的分布对齐程度。

**2. 推理机制的革新：从端到端黑箱生成到多工具协同的智能体推理**
基线方法采用单一 MLLM 端到端直接生成回答的范式，在面对需要精确几何计算或动态空间关系推理的复杂任务时往往力不从心。SpatialScore 提出了 **SpatialAgent** 这一无需训练的智能体框架，其核心创新在于将 12 个专业空间感知工具（如深度估计器、相机姿态估计器、光流/运动估计器等）动态集成到语言模型的推理循环中，并支持 **Plan-Execute**（任务分解与逐步执行）与 **ReAct**（迭代观察与策略优化）两种推理范式。
这一机制创新的优势在于：它将空间推理从模型内部的隐式知识检索，转化为对外部精确感知工具的显式调用与整合。在不进行任何微调的情况下，SpatialAgent-ReAct 将 Qwen3-VL-8B 在 SpatialScore-OpenSource 上的准确率从 42.97 提升至 50.01（+7.04），且 ReAct 范式的迭代推理特性使其在多数基准上优于 Plan-Execute 范式（Table 7）。定性结果（Figure 4）进一步展示了智能体通过逐步调用深度估计、光流等工具，成功推理出正确空间属性的过程，而其他模型则直接给出错误回答。

综上，SpatialScore 的创新本质在于**识别并利用了“全面评估—数据增强—工具协同”这一增强空间智能的因果链条**：全面基准暴露能力缺陷，专项数据提供知识补充，智能体框架实现工具协同，三者共同推动 MLLM 向人类水平的空间智能迈进。

SpatialScore 工作围绕空间智能评估与增强构建了一个“评估基准—训练语料—推理智能体”三位一体的整体框架，其核心逻辑为：首先通过全面的基准诊断当前多模态大语言模型（MLLM）的空间认知瓶颈，然后分别从数据驱动和智能体驱动两条互补路径提升模型的空间推理能力。

### 框架总览与模块关系

整个系统由三个核心模块构成，彼此之间存在递进与互补关系：

1.  **SpatialScore（评估基准）**：作为诊断工具，覆盖 30 个空间任务、约 5K 人工验证样本，系统量化 MLLM 在 10 个空间能力维度上的表现，揭示模型与人类水平（86.60）之间的巨大差距（最佳模型 Gemini-3-Pro 仅 60.12）。该基准为后续改进提供了明确的能力短板定位。

2.  **SpatialCorpus（训练语料）**：作为数据驱动改进路径的基础资源，包含 331K 多模态空间推理问答对，源自 3D 标注数据的重新利用与合成。其作用是为监督微调提供大规模、多样化的空间推理训练信号。

3.  **SpatialAgent（推理智能体）**：作为训练无关的智能体增强路径，在推理时动态调用 12 个专业空间感知工具（深度估计器、相机姿态估计器、光流/运动估计器、目标定位/计数/分割工具等），通过 Plan-Execute 或 ReAct 范式进行多步推理，无需微调即可提升现成 MLLM 的空间理解能力。

三者关系可概括为：**SpatialScore 发现问题，SpatialCorpus 和 SpatialAgent 从不同角度解决问题**。前者通过注入空间推理知识增强模型内在能力，后者通过外部工具调用补偿模型感知缺陷。

### 输入输出流

#### 基本 MLLM 问答流（基线）

给定问题 $\mathbf{q}$ 和视觉输入 $\mathbf{v}$，MLLM $\Phi$ 直接生成响应：

$$\mathbf{r} = \Phi(\mathbf{q}, \mathbf{v})$$

这是所有基线模型（Qwen3-VL、InternVL3、LLaVA-OneVision 等）的默认推理方式，也是衡量改进的起点。

#### 数据驱动路径：SpatialCorpus 监督微调

该路径不改变推理时的架构，而是在训练阶段将 MLLM 在 SpatialCorpus 上进行监督微调，使模型内化空间推理知识。微调后的模型仍使用上述基本问答流进行推理，但参数已针对空间任务优化。这一路径的核心优势在于**推理时零额外开销**，但提升幅度受训练数据分布与评估任务对齐程度的影响——在分布接近的 SpatialScore-Repurpose 子集上提升 21.76 个百分点，而在分布差异较大的 OpenSource 子集上仅提升 5.75 个百分点。

#### 智能体路径：SpatialAgent 工具增强推理

该路径保持 MLLM 参数不变，通过智能体框架 $\mathcal{A}$ 在推理时动态编排工具箱 $\mathcal{T}$ 中的工具：

$$\mathbf{r} = \mathcal{A}(\mathbf{q}, \mathbf{v}; \Phi; \mathcal{T})$$

SpatialAgent 内部由四个角色模块组成，支持两种推理范式：

**Plan-Execute 范式**（图 3b）：
- **Planner（规划器）**：将复杂空间问题分解为有序的工具调用计划 $\mathbf{p}$：
  $$\mathbf{p} = \Phi_{\mathrm{plan}}(\mathbf{q}, \mathbf{v}; \mathcal{T}) = \{(\mathbf{t}_1, \mathrm{args}_1), \dots, (\mathbf{t}_k, \mathrm{args}_k)\}$$
- **Executor（执行器）**：按计划逐步调用工具箱中的工具，获取结构化感知结果。
- **Summarizer（总结器）**：整合所有工具输出，生成最终答案及推理链。

**ReAct 范式**（图 3c）：
- **Observer（观察者）**：基于历史记忆 $\mathcal{M}_i$ 逐步推理，决定下一步是调用工具还是输出最终答案：
  $$\mathcal{M}_i = \{\mathbf{m}_1, \dots, \mathbf{m}_{i-1}\} = \{(\mathbf{o}_1, \mathbf{y}_1), \dots, (\mathbf{o}_{i-1}, \mathbf{y}_{i-1})\}, \quad \mathcal{M}_1 = \emptyset$$
  其中 $\mathbf{o}_j$ 为第 $j$ 步的观察，$\mathbf{y}_j$ 为工具执行结果。
- **Executor 与 Summarizer**：与 Plan-Execute 范式共享，负责工具调用执行与最终答案整合。

两种范式的关键区别在于：Plan-Execute 一次性生成完整计划后顺序执行，效率较高（约 5.4 秒/样本）但缺乏中间纠错能力；ReAct 每步根据观察动态决策，迭代推理能力更强（在 OpenSource 子集上 50.01 vs. Plan-Execute 的 49.58），但延迟更高（约 9.3 秒/样本）。当 Plan-Execute 推理失败时（4B 模型失败率 2.25%，8B 模型 8.24%），系统自动降级为直接回答。

### 数据构造管线支撑

上述三个核心模块均依赖统一的数据构造管线（图 2a）：从 3D 标注数据出发，通过 QA 对生成管线产生判断、多选和开放式问题，经 LLM 预过滤和人工筛选确保质量与视觉依赖性。SpatialScore 整合了新增的 3D 标注重利用数据（SpatialScore-Repurpose，1,091 样本）与来自 23 个公开数据集的空间相关样本，总计 5,025 样本；SpatialCorpus 则基于模拟器和 3D 元数据扩展至 331K 样本，为监督微调提供大规模训练信号。

![[assets/figures/papers/paper_list_l827_https_arxiv_org_abs_2505_17012/figures/001_Figure_1.jpg]]
*Figure 1: | Overview. (a) Representative examples from distinct categories in SpatialScore, which thoroughly assesses spatial intelligence capabilities via question-answering (judgment, multi-choice, and open-ended QA); (b) Performance of state-of-the-art models compared to humans on SpatialScore*

### 3.1 问题形式化

SpatialScore 将空间智能评估统一为多模态问答框架。给定视觉输入 $\mathbf{v}$（单图、多图序列或视频）和自然语言问题 $\mathbf{q}$，模型需生成回答 $\mathbf{r}$。论文定义了两种推理路径：

**基础 MLLM 直接推理**：端到端模型 $\Phi$ 直接以视觉和问题为条件生成回答：

$$\mathbf{r} = \Phi(\mathbf{q}, \mathbf{v})$$

**空间智能体增强推理**：引入工具箱 $\mathcal{T}$（包含 12 个专业空间感知工具），智能体 $\mathcal{A}$ 以核心模型 $\Phi$ 为推理引擎，动态编排工具调用，生成回答：

$$\mathbf{r} = \mathcal{A}(\mathbf{q}, \mathbf{v}; \Phi; \mathcal{T})$$

这两种形式化路径对应了论文的两条技术路线：数据驱动的监督微调（优化 $\Phi$ 本身）与训练无关的智能体增强（保持 $\Phi$ 冻结，通过 $\mathcal{A}$ 和 $\mathcal{T}$ 弥补能力短板）。

### 3.2 SpatialAgent 双范式推理

SpatialAgent 提供了两种互补的推理范式，分别对应不同的空间任务特性。

**Plan-Execute 范式**：适用于可预先分解的结构化空间问题。规划器 $\Phi_{\mathrm{plan}}$ 将复杂问题分解为有序的工具调用计划 $\mathbf{p}$：

$$\mathbf{p} = \Phi_{\mathrm{plan}}(\mathbf{q}, \mathbf{v}; \mathcal{T}) = \{(\mathbf{t}_1, \mathrm{args}_1), \dots, (\mathbf{t}_k, \mathrm{args}_k)\}$$

其中 $\mathbf{t}_i$ 为第 $i$ 步调用的工具，$\mathrm{args}_i$ 为该工具的参数。执行器按序调用工具，汇总器整合所有工具输出生成最终回答。该范式的优势在于规划与执行解耦，推理过程可解释性强，但对复杂动态场景的适应性有限——当规划错误时，执行器无法中途修正，导致一定失败率（Qwen3-VL-4B 为 2.25%，8B 为 8.24%），此时系统降级为直接回答。

**ReAct 范式**：适用于需要逐步观察与调整的迭代推理场景。观察器维护记忆状态 $\mathcal{M}_i$，存储历史观察与执行结果：

$$\mathcal{M}_i = \{\mathbf{m}_1, \dots, \mathbf{m}_{i-1}\} = \{(\mathbf{o}_1, \mathbf{y}_1), \dots, (\mathbf{o}_{i-1}, \mathbf{y}_{i-1})\}, \quad \mathcal{M}_1 = \emptyset$$

在第 $i$ 步，观察器基于当前视觉输入、问题、可用工具和历史记忆，决定下一步动作：调用特定工具（生成 $\mathbf{t}_i$ 和 $\mathrm{args}_i$）或输出最终回答。该范式通过迭代交互实现策略精炼，在多数基准上优于 Plan-Execute（如 8B 在 SpatialScore-OpenSource 上 50.01 vs 49.58），但推理延迟更高（约 9.3 秒/样本 vs 5.4 秒/样本）。

### 3.3 空间工具箱设计

工具箱 $\mathcal{T}$ 是 SpatialAgent 的核心能力来源，包含 12 个专业空间感知工具，覆盖以下类别：

- **深度估计**：从单目或双目图像推断场景深度图，支撑对象距离、相对位置等判断。
- **相机姿态估计**：估计相机内参和外参，支撑视角推理和相机运动分析。
- **光流与运动估计**：捕捉帧间像素级运动，支撑对象运动和时序推理。
- **目标定位、计数与分割**：检测并定位场景中的对象实例，支撑计数、空间关系判断。

这些工具本身是独立的视觉基础模型，SpatialAgent 通过结构化提示引导核心 MLLM 选择合适的工具并解析其输出。工具的输出以结构化文本形式返回（如深度值范围、目标边界框坐标），而非原始视觉特征图，从而与语言模型的推理循环无缝衔接。工具的精度直接影响最终答案的可靠性——当工具输出存在误差时，该误差可能传播至汇总器，导致错误回答（见图 4 定性结果中的工具执行错误案例）。

### 3.4 数据构造管线

SpatialScore 和 SpatialCorpus 共享一套数据构造管线，核心模块包括：

1. **3D 标注数据复用**：利用现有 3D 数据集中的精确空间标注（深度图、相机姿态、目标边界框等），通过规则模板生成多样化的问答对，涵盖判断题、多选题和开放式问题三种格式。
2. **干扰项生成策略**：多选题采用三种策略生成具有挑战性的干扰项——（i）从同类别标注中随机采样；（ii）在正确答案上施加小扰动；（iii）基于常见空间错觉构造语义混淆项。
3. **LLM 预过滤与人工筛选**：通过 LLM 初步过滤低质量样本（如答案可从文本线索推断而无需视觉输入），再经人工核查确保视觉依赖性和标注准确性，最终从 23 个公开数据集中筛选出 5,025 个高质量样本构成 SpatialScore。

SpatialCorpus 在此基础上进一步扩展，利用模拟器生成大规模训练数据，最终包含 331K 个空间推理问答对，覆盖多种视觉数据类型和输入模态。

![[assets/figures/papers/paper_list_l827_https_arxiv_org_abs_2505_17012/figures/005_Figure_3.jpg]]
*Figure 3: | Architecture and Workflow of SpatialAgent. (a) Specialized spatial perception tools within SpatialAgent; (b) The Plan-Execute paradigm for task decomposition and stepwise execution; (c) The ReAct paradigm for iterative interaction and strategy refinement*

## 实验与关键发现

### 基准评估：SpatialScore 上的模型表现

为量化当前多模态大模型的空间智能水平，作者在 SpatialScore 上对 49 个代表性 MLLM 进行了大规模评估，涵盖开源模型（如 Qwen3-VL、InternVL3、LLaVA-OneVision）与商业模型（如 Gemini-3-Pro、GPT-5）。评估覆盖 10 个空间能力维度：心理旋转、计数、深度估计、物体距离、物体运动、相机姿态与运动、时序推理、视角推理、物体尺寸和物体定位。

**核心发现：模型与人类之间存在巨大鸿沟。** 人类在 SpatialScore 上的总体准确率达到 86.60，而表现最佳的商业模型 Gemini-3-Pro 仅取得 60.12（Table 2）。在开源模型中，Qwen3-VL-235B-A22B 以 56.63 的总体得分领先，中规模模型（7B–14B）中 VST-7B-RL 取得 52.47，Qwen3-VL-8B 仅 45.48。这一差距表明现有 MLLM 在严格的几何空间感知任务上仍面临根本性困难，尤其是在需要精确度量推理的深度估计、相机姿态和物体运动等维度上表现尤为薄弱。

### 数据驱动路径：SpatialCorpus 监督微调

为验证空间推理训练数据的价值，作者构建了包含 331K 多模态问答对的 SpatialCorpus，并基于此对 Qwen3-VL 系列模型进行监督微调。表 7 和表 8 分别展示了在 SpatialScore-OpenSource 和 SpatialScore-Repurpose 两个子集上的量化对比。

在 **SpatialScore-OpenSource** 子集上，Qwen3-VL-8B 经 SpatialCorpus 微调后，总体准确率从零样本的 42.97 提升至 48.72（+5.75）。在 **SpatialScore-Repurpose** 子集上，提升幅度更为显著：同模型从 54.53 跃升至 76.29（+21.76）。这一差异值得关注：SpatialCorpus 的构建数据源自特定的 3D 标注数据集和模拟器，与 SpatialScore-Repurpose 子集的分布更为接近，因此在该子集上的增益远高于 OpenSource 子集。这提示训练数据分布与评估任务的对齐程度对微调增益有决定性影响。

### 智能体路径：SpatialAgent 的训练无关增强

SpatialAgent 提供了一条无需微调即可提升空间推理能力的替代路径。该框架以 Qwen3-VL 为核心推理引擎，集成 12 个专业空间感知工具（包括深度估计器、相机姿态估计器、光流/运动估计器、目标定位与分割工具等），支持 Plan-Execute 和 ReAct 两种推理范式。

在 **SpatialScore-OpenSource** 子集上，SpatialAgent-ReAct 将 Qwen3-VL-8B 的准确率从零样本的 42.97 提升至 50.01（+7.04），Plan-Execute 范式则提升至 49.58（+6.61）。在 **SpatialScore-Repurpose** 子集上，SpatialAgent-ReAct 取得 67.51（+12.98），Plan-Execute 取得 66.97（+12.44）。ReAct 范式在两个子集上均略优于 Plan-Execute，验证了迭代推理和动态策略调整在复杂空间任务中的优势。

值得注意的是，SpatialAgent 的提升完全来自推理阶段的工具编排，无需任何模型参数更新。图 4 的定性结果展示了 SpatialAgent 通过调用深度估计、光流等工具逐步推理出正确空间属性的过程，而其他基线模型则直接给出错误回答。

### 消融分析：提示策略与推理范式

作者通过消融实验考察了提示策略的影响。One-shot 提示相比 zero-shot 仅带来小幅提升（Qwen3-VL-4B: +1.51, 8B: +0.78），表明仅靠上下文示例难以根本解决 MLLM 的空间推理缺陷。这一发现从侧面印证了 SpatialCorpus 微调和 SpatialAgent 工具增强的必要性。

在推理范式对比中，ReAct 在多数基准上优于 Plan-Execute（如 8B 在 OpenSource 上 50.01 vs 49.58），但 Plan-Execute 在部分任务上具有更低的推理失败率。Plan-Execute 模式下，Qwen3-VL-4B 的推理失败率为 2.25%，8B 为 8.24%；失败时系统降级为直接回答，可能无法充分体现工具调用的优势。

### 计算开销与效率权衡

SpatialAgent 的推理延迟显著高于直接推理。Table 6 报告了各工具的计算开销：以 Qwen3-VL-8B 为智能体核心执行 Plan-Execute 范式时，平均推理延迟约 5.4 秒/样本，ReAct 范式则约 9.3 秒/样本，比直接推理慢数倍。工具调用频率最高的模块包括深度估计器和目标定位工具，其 GPU 内存占用和单次调用延迟构成了系统的主要计算瓶颈。这一开销限制了 SpatialAgent 在实时应用场景中的部署可行性。

![[assets/figures/papers/paper_list_l827_https_arxiv_org_abs_2505_17012/figures/014_Table_6.jpg]]
*Table 6: | Analysis of Computational Overhead for the SpatialAgent Toolbox. Here, we evaluate SpatialAgent (with Qwen3-VL-8B serving as the agent core and executing the Plan-Execute reasoning paradigm) on SpatialScore, reporting the average GPU memory usage, single-invocation latency, and invocation frequency of each tool in the toolbox*

### 失败模式与局限性

SpatialAgent 的推理质量受限于底层工具模型的精度。工具的错误输出（如深度估计偏差、目标漏检）可能传播至最终答案，导致推理链断裂。此外，Plan-Execute 范式在复杂场景下存在一定的规划失败率，此时系统回退至直接回答，无法发挥工具增强的优势。基于 SpatialCorpus 的微调方法则面临训练-测试分布偏移问题：在分布内任务上增益显著，但在分布外任务上提升有限，表明当前训练语料的覆盖范围仍需扩展。

![[assets/figures/papers/paper_list_l827_https_arxiv_org_abs_2505_17012/figures/006_Table_3.jpg]]
*Table 3: | Comparisons of our Data-driven and Agent-based Approaches on SpatialScore. Qwen3-VL is adopted in two ways: (i) supervised fine-tuned on our SpatialCorpus; and (ii) as the agent core to conduct reasoning using the Plan-Execute (PE) and ReAct paradigms in SpatialAgent*

![[assets/figures/papers/paper_list_l827_https_arxiv_org_abs_2505_17012/figures/015_Table_7.jpg]]
*Table 7: | Quantitative Comparisons on SpatialScore-OpenSource Subset. Qwen3-VL is adopted in two ways: (i) supervised fine-tuned on our SpatialCorpus; and (ii) as the agent core to conduct reasoning using the Plan-Execute (PE) and ReAct paradigms in SpatialAgent*

![[assets/figures/papers/paper_list_l827_https_arxiv_org_abs_2505_17012/figures/007_Figure_4.jpg]]
*Figure 4: | Qualitative Results. We present the reasoning process of SpatialAgent against the direct responses of other models. While occasional errors occur due to tool execution or interpretation mistakes, these limitations are expected to diminish as MLLMs advance*

## 定位与知识库关联

### 空间智能评估的演进与SpatialScore的定位

SpatialScore的提出根植于一个明确的瓶颈：现有的空间智能评估基准过于碎片化，任务简单且范围狭窄，无法全面衡量多模态大语言模型（MLLM）在严格几何空间感知上的真实能力。作者通过系统梳理现有基准（Table 1）发现，此前的评估体系在数据类型（真实图像 vs. AIGC）、输入模态（单图、多图序列、视频）和问答格式（判断、多选、开放式）上均存在覆盖缺口。SpatialScore以约5K人工验证样本、30个任务、10个空间能力维度的规模，成为当前覆盖面最广的空间智能基准。

在基线对比层面，论文评估了49个代表性MLLM（Table 2），涵盖开源模型（如**Qwen3-VL**、**Qwen2.5-VL**、**InternVL3**、**LLaVA-OneVision**）和闭源模型（如**Gemini-2.5-Pro**、**GPT-5**），以及专门的空间推理模型**VST-3B-RL**。关键发现是：人类水平为86.60，而最佳闭源模型Gemini-3-Pro仅60.12，最佳开源模型Qwen3-VL-235B-A22B为56.63，揭示了巨大的认知鸿沟。这一结果直接验证了核心洞察：全面的基准是推动该领域进步的必要条件。

### 方法论谱系：数据驱动与智能体驱动的双路径

SpatialScore的方法论贡献并非单一模型，而是一个包含三条技术路线的评估与改进框架：

**1. 数据驱动路径（SpatialCorpus微调）**

该方法将通用MLLM的训练范式从“预训练通用多模态数据，零样本直接推理”转变为“在SpatialCorpus（331K空间QA对）上监督微调，针对空间推理进行专门优化”。SpatialCorpus的构建利用了3D标注数据（如深度图、相机姿态、目标边界框）和模拟器，通过QA对生成管线、LLM预过滤和人工筛选确保质量。这一路线与传统的任务特定微调（如VST系列）形成互补：VST-3B-RL虽在SpatialScore上取得48.04的领先成绩，但其训练数据和范式与SpatialCorpus的覆盖范围不同。

**2. 智能体驱动路径（SpatialAgent）**

SpatialAgent代表了从“单一MLLM端到端直接生成回答”到“多智能体系统动态调用专业工具”的范式转变。其架构包含四个核心模块：Planner（Plan-Execute模式下将复杂空间问题分解为有序工具调用计划）、Observer（ReAct模式下根据观察和记忆逐步推理）、Executor（执行工具调用并返回结构化结果）、Summarizer（整合工具输出生成最终答案）。这一设计直接回应了因果机制：将视觉基础模型（如深度估计器、相机姿态估计器）作为工具集成到语言模型推理循环中，能显著提升复杂空间任务表现。

**3. 工具增强的推理范式**

SpatialAgent集成了12个专业空间感知工具，包括深度估计器、相机姿态估计器、光流/运动估计器、目标定位/计数/分割工具等。这一定位使其区别于纯端到端模型和简单的提示工程方法。消融实验表明，One-shot提示相比zero-shot仅带来小幅提升（Qwen3-VL-4B: +1.51, 8B: +0.78），说明仅靠提示难以根本解决空间推理缺陷，进一步验证了工具增强的必要性。

### 适用边界与关键约束

SpatialScore及其配套方法的适用边界受以下因素制约：

**数据分布偏差**：SpatialCorpus源自特定3D数据集和模拟器，与SpatialScore-Repurpose子集分布更接近。这导致微调增益在不同子集上差异显著——在Repurpose子集上提升21.76%，而在OpenSource子集仅提升5.75%。这意味着SpatialCorpus微调的效果高度依赖于训练数据与评估任务的对齐程度，在分布外场景的泛化性需要谨慎评估。

**工具链依赖与误差传播**：SpatialAgent依赖外部空间感知工具的精度，工具的错误输出可能传播至最终答案。Plan-Execute模式在复杂场景下存在推理失败率（Qwen3-VL-4B: 2.25%, 8B: 8.24%），此时系统降级为直接回答，无法体现工具优势。这一机制虽然保证了系统鲁棒性，但也意味着工具增强的实际收益受限于核心MLLM的基础能力。

**计算开销约束**：SpatialAgent引入显著的推理延迟——Plan-Execute约5.4秒/样本，ReAct约9.3秒/样本（Table 6），比直接推理慢数倍。工具箱中各工具的GPU内存占用和调用频率差异明显，限制了实时应用场景的部署。

### 范式对比与互补性

ReAct范式在多数基准上优于Plan-Execute（如8B在OpenSource上50.01 vs. 49.58），体现了迭代推理在空间任务中的优势。但两种范式并非互斥：Plan-Execute适合任务结构清晰的场景，ReAct更适合需要动态调整策略的复杂推理。当前工作将微调路径与智能体路径作为独立方案评估，二者的互补结合（如微调后的模型作为SpatialAgent核心）仍是开放问题。

### 局限与开放问题

**计算效率优化**：如何降低SpatialAgent的计算开销是实用化的关键。可能的方向包括工具模型的轻量化（如使用蒸馏后的视觉基础模型）、推理缓存（复用相同场景的工具输出）、以及工具调用的并行化执行。

**训练与推理的融合**：当前SpatialAgent以训练无关的方式增强推理，而SpatialCorpus微调独立运作。能否将Plan-Execute和ReAct的推理轨迹用于训练，或使微调模型更好地适配工具调用范式，以获得互补增益，尚待探索。

**工具覆盖的完备性**：12个工具是否覆盖了全部空间感知需求？未来扩展方向可能包括3D场景图构建、动态时空推理、以及多智能体协同感知等更复杂的空间认知能力。

**训练语料的平衡性**：构建分布更广泛、更平衡的训练语料，以缓解微调在不同子集上的差分提升问题，是提升方法泛化性的必要条件。这需要探索跨模拟器、跨数据源的数据混合策略和分布对齐技术。

## 原文 PDF

![[paperPDFs/CVPR_2026/SpatialScore_Towards_Comprehensive_Evaluation_for_Spatial_Intelligence.pdf]]
