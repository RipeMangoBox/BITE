---
title: "SCoT: Teaching 3D-LLMs to Think Spatially with Million-scale CoT Annotations"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/SCoT_Teaching_3D_LLMs_to_Think_Spatially_with_Million_scale_CoT_Annotations.pdf
openreview_forum_id: 5Tph6wFMOm
aliases:
- SSCT
- SCoT
tags:
- ICLR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: "按任务复杂度分层决定是否使用CoT监督：对简单感知任务仅保留答案监督以避免过度推理幻觉，对需要推理的分析与规划任务引入详尽、场景锚定的CoT推理链，并使用<SI>标签强制引用具体场景信息。"
primary_logic: "构建一个百万级别的SCoT数据集，将3D任务分为感知、分析、规划三个层次，仅在后两个层次中使用场景锚定的思维链监督；同时提出<SI>标签确保推理步骤的每个依据都明确引用场景证据，从而在不损害感知表现的前提下，大幅提升复杂任务的可解释性、忠实性和可信度。"
claims:
- "在简单的感知任务上过度使用CoT会使模型产生幻觉，导致约4.9%的准确率下降。"
- "CoT训练在分析和规划任务上平均提升可解释性6.21%、忠实性11.74%、可信度10.02%。"
- "三级任务分类（感知、分析、规划）明确规定了何时宜用CoT，从而在基础观察和复杂推理之间取得平衡。"
- "<SI>标记强制推理过程引用场景信息，使原本模糊的断言转化为可验证的锚定声明。"
---

# SCoT: Teaching 3D-LLMs to Think Spatially with Million-scale CoT Annotations

> [!tip] 核心洞察
> 构建一个百万级别的SCoT数据集，将3D任务分为感知、分析、规划三个层次，仅在后两个层次中使用场景锚定的思维链监督；同时提出<SI>标签确保推理步骤的每个依据都明确引用场景证据，从而在不损害感知表现的前提下，大幅提升复杂任务的可解释性、忠实性和可信度。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | SCoT：以百万级思维链标注教会三维大语言模型空间思维 |
| 英文题名 | SCoT: Teaching 3D-LLMs to Think Spatially with Million-scale CoT Annotations |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=5Tph6wFMOm) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | SCoT (Spatial Chain-of-Thought) 数据集与训练框架 |
| Dataset | SCoT-Analysis (Implicit Detection), SCoT-Planning (Situated Planning), SCoT-Perception (ScanRefer) |

> [!tip] 效果简介
> - SCoT-Analysis (Implicit Detection) 上，Acc@0.25 为 32.2，对比 8.6，变化 +23.6。
> - SCoT-Planning (Situated Planning) 上，Explainability (1-10) 为 7.38，对比 6.64，变化 +0.74。
> - SCoT-Perception (ScanRefer) 上，Acc@0.25 为 56.4，对比 58.4，变化 -2.0。

## 概述

现有三维大语言模型（3D-LLMs）在场景理解与交互方面取得了显著进展，但其训练范式存在一个根本性瓶颈：主流方法仅依赖“问题-答案”对进行监督，缺乏显式、结构化的推理过程引导。这使得模型在面对需要多步空间推理的分析与规划任务时，透明性差、可靠性低，难以满足真实场景中对可解释决策的需求。然而，一个关键的因果发现是——不加区分地在所有任务上引入思维链（Chain-of-Thought, CoT）监督并非良策：在简单的空间感知任务上过度使用CoT反而会诱发幻觉，导致准确率下降约4.9%（Table 2, Fig. 2）。

针对这一矛盾，**SCoT（Spatial Chain-of-Thought）** 提出了一个原则性的解决方案：**按任务复杂度分层决定是否使用CoT监督**。具体而言，SCoT首先建立了一个三级任务分类体系——**空间感知**（回答“那里有什么”）、**空间分析**（回答“这意味着什么”）和**空间规划**（回答“我该怎么做”）。对于仅需事实性输出的感知任务，SCoT保留传统的仅答案监督，避免过度推理带来的幻觉；对于需要推理的分析与规划任务，SCoT则引入详尽的、场景锚定的思维链，并要求推理的每一步都通过专用的 `<SI>` 标签显式引用场景证据，从而将模糊的断言转化为可验证的锚定声明。

基于这一核心洞察，SCoT构建了一个**百万级别（约110万样本）的思维链标注数据集**，覆盖感知（240K）、分析（460K）和规划（390K）三个层次，并配套提出了SCoT-Reasoner模型与两阶段训练策略：第一阶段在感知样本上建立基础空间理解能力，第二阶段在分析与规划样本上微调生成显式CoT。实验结果表明，CoT训练在分析与规划任务上平均提升可解释性6.21%、忠实性11.74%、可信度10.02%（Table 3, Table 4），而感知任务则因避免了CoT的过度使用而保持了原有性能。这一“分层监督”范式在不牺牲基础感知能力的前提下，显著增强了3D-LLMs在复杂空间推理任务上的可解释性与可信度。

**方法谱系与知识库定位**：SCoT处于3D视觉-语言模型与思维链推理的交叉地带。相较于仅提供问答对的早期3D对话基线（如**Chat3D V2**、**Chat Scene**、**LL3DA**等）以及将3D场景视为动态视频的**Video 3D LLM**，SCoT首次系统性地将任务复杂度作为CoT使用的决策依据，并通过 `<SI>` 锚定机制确保推理链条的场景忠实性。与通用视觉思维链方法不同，SCoT的贡献在于揭示了“何时不应使用CoT”与“如何使CoT可验证”这两个同等重要的维度，为3D空间智能的可靠推理提供了新的研究范式。

## 背景与动机

三维场景理解正从单纯的物体识别走向复杂的空间推理与规划。当前，3D大语言模型（3D-LLMs）已在场景对话、视觉定位等任务上展现出一定能力，但其训练范式存在一个根本性瓶颈：模型主要通过“问题—答案”对进行监督，缺乏显式的、结构化的推理过程引导。这种仅答案的监督方式，使得模型在面对需要多步空间分析或情景化规划的任务时，推理过程不透明、结论难以验证，进而导致可解释性差、可信度低。

引入思维链（Chain-of-Thought, CoT）似乎是解决这一问题的自然路径。然而，本文揭示了一个关键的反直觉发现：**不加区分地在所有任务上使用CoT监督，反而会损害简单感知任务的性能**。实验表明，在空间感知任务（如ScanRefer目标定位）上过度使用CoT，会引发幻觉、遗漏和错误推理，导致准确率下降约4.9%（见Table 2与Figure 2）。这一现象揭示了现有方法的一个深层缺口：缺乏一个原则性的框架来界定“何时需要CoT”以及“如何让CoT忠实于场景”。

与此同时，现有3D-LLM训练数据集（如ScanRefer、3D-LLM、SceneVerse等）普遍存在两个结构性局限：其一，数据规模有限，且仅提供问答对，不包含推理过程标注；其二，任务类型单一，无法覆盖从基础感知到高层规划的完整认知谱系。如Table 1所示，此前尚无数据集能在百万级规模上同时提供感知、分析与规划三个层次的场景锚定推理链。

上述缺口共同指向一个核心问题：**如何在不损害基础感知能力的前提下，赋予3D-LLMs可解释、可验证的空间推理能力？** 本文的动机正是构建一个按任务复杂度分层、场景锚定的思维链监督体系，使模型在简单观察任务上保持高效准确，而在复杂分析与规划任务上生成透明、可信的逐步推理。

## 核心创新

SCoT的核心创新在于针对3D-LLM训练中“何时以及如何引入思维链（CoT）”这一被忽视的关键问题，提出了系统性的解决方案。具体体现在三个紧密耦合的层面：

### 1. 任务复杂度分层的CoT使用策略

现有3D-LLM的训练数据几乎全部采用简单的（问题，答案）对（Table 1），缺乏对推理过程的显式监督。SCoT首次引入了一个原则性的三层任务分类体系——**空间感知**、**空间分析**、**空间规划**——并以此明确规定CoT的适用范围（Sec. 3.1）。

这一策略的核心洞察是：**不加区分地引入CoT监督并非无害**。实验表明，在简单的感知任务（如ScanRefer、SQA3D）上强制使用CoT，会导致模型产生幻觉、遗漏和错误，准确率平均下降约4.9%（Table 2, Fig. 2）。因此，SCoT仅在需要推理的分析与规划任务中引入CoT监督，而在感知任务上维持仅答案的监督格式。这种“按需推理”的策略在不损害基础感知能力的前提下，大幅提升了复杂任务的可解释性、忠实性和可信度。

### 2. 场景锚定的思维链生成与<SI>标签机制

传统CoT在文本空间中自由推理，缺乏对3D场景信息的显式引用，导致推理过程难以验证。SCoT通过两个关键设计解决了这一问题：

- **场景上下文构建**：在生成CoT之前，先为每个3D场景构建详细的场景上下文（包括场景图、文本描述和BEV图像），作为VLM生成推理链的输入（Fig. 3）。
- **<SI>标签强制锚定**：在CoT生成过程中，VLM被严格提示在推理链的每一步中，凡是使用场景信息（如对象属性、空间关系、场景布局）时，必须显式插入`<SI>`标签进行引用（Sec. 3.2）。未正确使用`<SI>`标签的样本将被直接丢弃。

这一机制将原本模糊的断言转化为可验证的锚定声明，使推理过程的每一步依据都可以追溯到具体的场景证据。

### 3. 两阶段训练策略与ORS空间建模

SCoT-Reasoner采用**两阶段训练策略**（Sec. 4）：第一阶段在240K空间感知样本上建立基础感知能力；第二阶段在460K分析+390K规划样本上微调，使模型学会生成包含`<SI>`锚点的显式CoT。这种渐进式训练避免了直接学习复杂推理链时可能出现的感知能力退化。

在模型架构层面，SCoT-Reasoner引入了**ORS（对象-关系-场景）细化模块**（Appendix A.2），通过空间图+Graph-Transformer融合绝对位置和相对关系信息。该模块以对象为节点、偏移嵌入为边构建空间图，通过带可学习空间偏差的Graph-Transformer提炼对象-关系-场景特征，生成增强表示$\bar{F}_i^{ORS} \in \mathbb{R}^{1 \times 2048}$（Fig. 8）。相比多数基线仅使用原始点云或多视图特征的做法，ORS模块提供了更丰富的结构化空间上下文，为后续的CoT推理提供了更可靠的信息基础。

### 核心创新总结

| 创新维度 | 基线做法 | SCoT做法 | 关键证据 |
|---------|---------|---------|---------|
| 训练监督信号 | 仅（问题，答案）对 | 感知任务维持仅答案；分析/规划任务使用（问题，含<SI>锚点的CoT，答案） | Table 2, Sec. 3.2 |
| CoT使用策略 | 无或全量使用 | 按任务复杂度分层决定 | Sec. 3.1, Table 2 |
| 推理锚定机制 | 无 | <SI>标签强制引用场景证据 | Sec. 3.2 |
| 训练阶段 | 单阶段端到端 | 两阶段渐进式（感知→推理） | Sec. 4 |
| 空间关系建模 | 原始点云/多视图特征 | ORS模块（空间图+Graph-Transformer） | Appendix A.2, Fig. 8 |

这三个创新点形成了完整的因果链条：**分层策略决定了“何时用CoT”，<SI>机制和场景锚定决定了“如何用CoT”，两阶段训练和ORS模块则提供了支撑CoT推理的感知和空间基础**。消融实验验证了这一链条的有效性：完整的CoT+<SI>设置带来最高的综合评分，但移除对象级推理或场景级推理均会导致可解释性、忠实性和可信度的显著下降（Table 9）。

## 整体框架

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_5Tph6wFMOm/figures/021_Figure_8.jpg]]
*Figure 8: Model architecture of SCoT-Reasoner. SCoT-Reasoner receives language instruction, object proposals segmented from 3D scene and video frames as input, then performs step-by-step reasoning and analysis based on the object-grounded or scene-grounded facts, and ultimately generates reliable accurate and verifiable answers*

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_5Tph6wFMOm/figures/003_Table_1.jpg]]
*Table 1: Comparison of SCoT dataset and the existing 3D large language model train sets. “M.3D.” means the Matterport3D dataset, “3RS.” means the 3RScan dataset, “M.S.” means the MultiScan dataset, “S.3D.” means the Structured3D dataset, “P.T.” means the ProcTHOR dataset, “Obj.” means the Objaverse dataset, “ARK.” means the ARKitScenes dataset, “3D.F.” means the 3D-Front dataset. “Reasoning” refers to the reasoning process besides the final answer*

SCoT提出了一套完整的**从数据构建到模型训练的闭环框架**，旨在赋予3D大语言模型显式的空间推理能力。该框架由两个核心组件构成：一个百万级别的空间思维链数据集（SCoT Dataset）和一个专为空间推理设计的模型架构（SCoT-Reasoner）。

### 数据-训练-推理的宏观流程

整个pipeline遵循“分层数据生成→两阶段训练→锚定推理”的逻辑链路：

1. **数据生成阶段**：首先为每个3D场景构建详细的场景上下文（包括场景图、文本描述、BEV图像），然后根据三级任务分类（感知、分析、规划）生成对应的监督样本。感知任务沿用公开基准的Q-A对，分析与规划任务则由VLM基于场景上下文生成包含`<SI>`锚定标签的Query–CoT–Answer三元组。
2. **训练阶段**：采用两阶段策略——第一阶段在240K空间感知样本上建立基础感知能力，第二阶段在460K分析+390K规划样本上微调生成显式CoT，避免CoT对简单感知任务的干扰。
3. **推理阶段**：SCoT-Reasoner接收语言指令、对象提议与多模态特征，通过ORS模块提炼空间关系后，由LLM骨干生成逐步推理文本，最终输出包含CoT和答案的响应。

### SCoT数据集的核心设计

SCoT数据集包含约**110万样本**，其与现有3D-LLM训练集的根本差异在于引入了**显式的、场景锚定的推理链**。如Table 1所示，此前数据集（如ScanRefer、3D-LLM、SceneVerse、3D-GRAND等）仅提供Q-A对，而SCoT在分析与规划任务中额外提供了结构化的CoT推理过程。

数据生成的关键机制是**`<SI>`标签强制锚定**：VLM被严格提示在推理链的每一步中，当使用场景信息（如对象属性、空间关系、场景布局）时，必须显式插入`<SI>`标签。这使得原本模糊的断言转化为可验证的锚定声明。质量控制环节会丢弃`<SI>`标签使用不足或不正确的样本，确保推理链忠实于场景。

### SCoT-Reasoner模型架构

SCoT-Reasoner的架构如Figure 8所示，由以下模块串联构成：

| 模块 | 功能 | 输入 | 输出 |
|------|------|------|------|
| **多模态编码器（2D/3D）** | 提取对象中心的多模态特征 | 3D场景与视频帧 | $F_i^{2D} \in \mathbb{R}^{1 \times 1024}$（DINOv2）、$F_i^{3D} \in \mathbb{R}^{1 \times 1024}$（Uni3D）、$B_i \in \mathbb{R}^{1 \times 6}$（3D边界盒） |
| **ORS细化模块** | 通过空间图+Graph-Transformer融合绝对位置与相对关系 | 对象特征与边界盒 | $\bar{F}_i^{ORS} \in \mathbb{R}^{1 \times 2048}$（拼接2D/3D特征与精炼后的空间特征） |
| **模态投影层** | 将ORS增强特征投影到LLM嵌入空间 | $\bar{F}_i^{ORS}$ | LLM可接受的嵌入表示 |
| **LLM骨干（Vicuna-7B + LoRA）** | 执行逐步推理，生成CoT与最终答案 | 语言指令、对象标识符、投影特征 | 包含`<SI>`锚定推理链和答案的完整响应 |

ORS模块是空间推理能力的核心：它以对象为节点、偏移嵌入为边构建空间图，通过带可学习空间偏差的Graph-Transformer精炼对象-关系-场景特征，使模型能显式建模空间关系而非隐式记忆。

### 训练策略的分层控制

框架通过**两级控制**确保CoT仅在需要推理的任务上生效：

- **任务级控制**：三级分类（感知/分析/规划）明确规定感知任务仅使用答案监督，分析与规划任务使用完整CoT监督。
- **训练级控制**：两阶段训练确保第一阶段建立的基础感知能力不被第二阶段的CoT训练破坏——这解释了为何SCoT-Reasoner在感知任务上仍能达到或超越仅答案训练的模型（Table 8），同时在分析与规划任务上大幅领先。

这种分层设计直接回应了核心瓶颈：不加区分地使用CoT会使简单感知任务产生约4.9%的准确率下降（Table 2），而仅在分析/规划任务上使用CoT则带来可解释性+6.21%、忠实性+11.74%、可信度+10.02%的全面提升（Table 3、Table 4）。

## 核心模块与公式推导

### 多模态编码器：2D/3D特征提取

SCoT-Reasoner 首先对场景中每个目标对象提取多模态特征。给定第 $i$ 个对象，其3D特征由 Uni3D 从点云中提取，2D特征由 DINOv2 从多视图图像中提取，同时保留其3D边界盒信息：

$$F_i^{3D} \in \mathbb{R}^{1 \times 1024}$$

$$F_i^{2D} \in \mathbb{R}^{1 \times 1024}$$

$$B_i \in \mathbb{R}^{1 \times 6}$$

其中 $B_i$ 编码了对象的尺寸（长、宽、高）与空间位置（中心坐标）。这三类信息共同构成对象的基础表示，为后续的空间关系建模提供输入。

### ORS细化模块：空间图与Graph-Transformer

ORS（Object-Relation-Scene）细化模块是SCoT-Reasoner的核心空间建模组件（见附录A.2及Figure 8）。该模块将场景显式构造为空间图：以对象为节点，以节点间的空间偏移嵌入为边。随后，Graph-Transformer利用可学习的空间偏差对节点特征进行消息传递与精炼，融合绝对位置与相对关系信息，最终生成增强的对象-关系-场景表示：

$$\bar{F}_i^{ORS} \in \mathbb{R}^{1 \times 2048}$$

该表示由Graph-Transformer精炼后的空间特征与原始2D或3D特征拼接而成，维度为2048。$\bar{F}_i^{ORS}$ 同时编码了对象自身属性、对象间空间关系以及全局场景上下文，为LLM的逐步推理提供了结构化、场景锚定的感知基础。

### 模态投影与LLM骨干

ORS增强特征 $\bar{F}_i^{ORS}$ 经模态特定的投影层映射至LLM（Vicuna-7B）的嵌入空间。LLM接收语言指令、对象标识符与投影特征后，通过LoRA微调生成逐步推理文本，最终输出包含CoT和答案的完整响应。整个推理过程由 `<SI>` 标签强制锚定场景证据，确保每个推理步骤的依据可追溯至具体的场景信息。

### 两阶段训练策略

SCoT-Reasoner采用两阶段训练（Section 4）：第一阶段在约240K空间感知样本上建立基础感知能力，仅使用答案监督；第二阶段在约460K分析样本与390K规划样本上微调，引入包含 `<SI>` 锚点的显式CoT监督。这种分层训练策略与三级任务分类（感知、分析、规划）相对应，从机制上避免了在简单感知任务上过度使用CoT所引发的幻觉问题（Table 2显示约4.9%的准确率下降）。

## 实验与分析

### 核心发现：CoT监督的任务依赖性

SCoT的核心实验结论具有明确的二分性：**思维链（CoT）监督在简单感知任务上是有害的，而在需要推理的分析与规划任务上则带来显著增益**。这一发现直接验证了论文提出的“按任务复杂度分层使用CoT”的核心策略。

在感知任务上，为SCoT-Reasoner添加CoT监督导致五项基准测试的性能全面下降（Table 2）。典型退化包括：ScanRefer的Acc@0.25从58.4降至56.4，Multi3DRefer的F1@0.25从60.1降至53.5，SQA3D的精确匹配率（EM）从55.8降至47.4。论文将这一现象归因于**过度推理幻觉**：在仅需识别“有什么”的简单任务中，模型被强制生成推理步骤后，倾向于编造不存在的关系或遗漏关键对象（Fig. 2），导致平均约4.9%的准确率损失。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_5Tph6wFMOm/figures/005_Table_2.jpg]]
*Table 2: Results on SCoT-Perception tasks with or without perception CoT supervision. “CoT” means using CoT annotations in the perception tasks. The model is SCoT-Reasoner*

相反，在空间分析任务上，CoT监督带来了跨模型的系统性提升（Table 3）。SCoT-Reasoner（CoT）在对象分析、关系分析和场景分析三个子任务上均取得最高的METEOR分数（分别为16.17、16.60和19.73），相比其仅答案版本（Answer-Only）分别提升0.83、2.27和1.06。更关键的是，LLM评估的三个主观维度——可解释性（Explainability）、忠实性（Faithfulness）和可信度（Trustworthiness）——在CoT设置下平均提升6.21%、11.74%和10.02%。这表明CoT不仅改善了文本质量，更从根本上增强了模型输出的可验证性。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_5Tph6wFMOm/figures/006_Table_3.jpg]]
*Table 3: Overall performance comparison on SCoT-Analysis tasks requiring text output. "R.", "M.", "Exp.", "Fai." and "Tru." are abbreviations for "ROUGE-L", "METEOR", "Explainability", "Faithfulness" and "Trustworthiness", respectively. Note that the score range for "Explainability", "Faithfulness", and "Trustworthiness" metrics is from 1 to 10. “(CoT)” means the method trained with “Full SCoT Setting”, and the counterpart without it is trained with “Answer-Only Setting”*

空间规划任务呈现出相似的模式（Table 4）。在情景化规划（Situated Planning）中，SCoT-Reasoner（CoT）的可解释性达到7.38（满分10），忠实性6.94，可信度7.14，均显著优于仅答案版本（6.64/6.09/6.30）和所有基线方法。值得注意的是，在非情景化规划（Un-situated Planning）中，CoT的增益相对收敛，这暗示**<SI>标签的场景锚定机制在需要紧密耦合场景信息的任务中发挥更关键的作用**。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_5Tph6wFMOm/figures/007_Table_4.jpg]]
*Table 4: Overall performance comparison on SCoT-Planning. "R.", "M.", "Exp.", "Fai." and "Tru." are abbreviations for "ROUGE-L", "METEOR", "Explainability", "Faithfulness" and "Trustworthiness", respectively. Note that the score range for "Explainability", "Faithfulness", and "Trustworthiness" metrics is from 1 to 10. “(CoT)” means the method trained with “Full SCoT Setting”, and the counterpart without it is trained with “Answer-Only Setting”*

### 隐式检测任务的突破性提升

隐式检测（Implicit Detection）是SCoT分析任务中最具挑战性的子任务，要求模型从场景中推断未明确陈述的信息。在该任务上，CoT监督带来的增益最为显著（Table 5）：SCoT-Reasoner（CoT）的Acc@0.25达到32.2%，Acc@0.50达到28.4%，分别比仅答案版本（8.6%/5.6%）提升23.6和22.8个百分点。这一巨大差距揭示了**结构化推理对于需要多步推断的任务是不可或缺的**——仅答案监督无法教会模型如何从场景证据中逐步推导出隐含结论。

### 消融实验：CoT粒度与<SI>标签的作用

Table 9的消融实验系统拆解了CoT监督的关键组件。移除对象级推理（w.o. Obj. in CoT）导致对象分析任务的METEOR从16.17降至15.34，可解释性从7.04降至6.43，忠实性从6.15降至5.37。移除场景级推理（w.o. Sce. in CoT）则主要损害情景化规划任务的可信度（从7.14降至6.55）。这些结果证实了**CoT的粒度需要与任务类型匹配**：对象分析依赖细粒度的对象属性推理，而情景规划则需要全局的场景上下文理解。

![[assets/figures/papers/paper_list_l51_https_openreview_net_forum_id_5Tph6wFMOm/figures/028_Table_9.jpg]]
*Table 9: Ablation experiments on different CoT settings and \<SI> levels. "R.", "M.", "Exp.", "Fai." and "Tru." are abbreviations for "ROUGE-L", "METEOR", "Explainability", "Faithfulness" and "Trustworthiness", respectively. “CoT.Len.” means the average token length of CoT, and “\<SI>” means average number of \<SI> identifier in CoT. Relationship analysis is excluded from this comparison because its CoT mainly consists of numerical computation process*

<SI>标签的消融揭示了其双重作用。完全移除<SI>标签（w.o. <SI>）导致忠实性显著下降（对象分析从6.15降至5.42），但推理速度有所提升。完整CoT+<SI>设置虽然带来最高综合评分，但推理时间增加2.0–3.2倍（例如场景分析从5.08秒增至13.30秒）。这一效率代价是当前方法的主要局限，限制了其在实时应用中的部署。

### 泛化性能：MSQA基准测试

在MSQA基准上的零样本评估（Table 6）验证了SCoT训练的跨场景泛化能力。在ScanNet环境下，SCoT-Reasoner取得54.4的整体分，与域内监督模型相当，且超越GPT-4o零样本2.1分。在ARKitScenes环境下，SCoT-Reasoner取得41.2的整体分，同样优于GPT-4o和Qwen-VL的零样本表现。特别值得关注的是导航（Navigation）子任务：SCoT-Reasoner在ScanNet零样本设置下比3D-R1高出14.6分，这归因于SCoT训练中包含了大量空间规划样本，使模型习得了有效的空间推理策略。

### 失败模式与局限性

尽管整体表现强劲，实验揭示了几个值得关注的失败模式：

1. **感知任务的CoT幻觉**：如Table 2和Fig. 2所示，在简单感知任务中强制使用CoT会导致模型编造不存在的空间关系或遗漏关键对象。这一问题在Multi3DRefer（多对象指代）任务上尤为严重（F1@0.25下降6.6），可能是因为多对象场景增加了幻觉的触发机会。

2. **推理效率瓶颈**：CoT生成显著增加了推理延迟（2.0–3.2倍），这在Table 9的推理时间列中有明确记录。对于需要实时响应的机器人导航等应用，当前的推理速度尚不可接受。

3. **室内场景的局限性**：所有实验均在ScanNet、3RScan、MultiScan等室内数据集上进行，SCoT在室外大规模或动态3D环境中的有效性尚未验证。

4. **评估的主观性依赖**：虽然LLM评估采用了ChatGPT-4.1、Qwen和DeepSeek三者的平均分以减少偏差（Fig. 9显示三者间存在中等程度的相关性），但主观评分本质上仍受评估者偏好的影响。

## 方法谱系与知识库定位

### 1. 与现有3D-LLM训练范式的关系

SCoT的核心贡献不在于提出全新的模型架构，而在于重新定义了3D-LLM的训练监督信号格式与任务组织方式。现有3D-LLM训练集——如ScanRefer、3D-LLM、SceneVerse、3D-GRAND等——普遍仅提供（问题，答案）的简单Q-A对（见Table 1），缺乏显式的推理过程标注。这一设计选择直接导致了两个后果：（1）模型在需要多步空间推理的分析与规划任务上透明性差、可信度低；（2）模型无法向用户展示其得出结论的依据，限制了实际部署中的可审计性。

SCoT通过引入**按任务复杂度分层的思维链（CoT）监督**改变了这一格局。具体而言，SCoT将3D任务划分为三个层次：
- **空间感知（Spatial Perception，240K样本）**：回答“那里有什么”，仅使用答案监督；
- **空间分析（Spatial Analysis，460K样本）**：回答“这意味着什么”，使用包含`<SI>`标签锚定的逐步推理链；
- **空间规划（Spatial Planning，390K样本）**：回答“我该怎么做”，同样使用场景锚定的CoT监督。

这一分层策略的关键洞见在于：**并非所有任务都适合CoT监督**。实验证据表明，在简单感知任务上不加区分地使用CoT会导致约4.9%的准确率下降（Table 2），原因是模型在不需要推理时被强制生成推理步骤，反而引入了幻觉和错误（Figure 2）。因此，SCoT的“选择性CoT”策略本质上是一种**任务复杂度自适应的监督信号分配机制**，在基础感知能力与复杂推理能力之间取得了平衡。

### 2. 与代表性基线方法的技术对比

SCoT-Reasoner在实验中被置于多个3D-LLM基线的对比框架下，这些基线代表了不同的技术路线：

- **Chat3D V2**：基于属性感知和关系感知令牌的3D场景对话基线，其核心是通过显式的属性/关系令牌增强场景理解，但缺乏结构化的推理链监督。
- **Video 3D LLM**：将3D场景视为动态视频并结合位置编码，利用视频理解范式处理3D数据，但同样未引入CoT推理机制。
- **Chat Scene**：集成多模态输入（图像、点云）的场景级对话基线，在Chat3D V2基础上增加了类似ORC的表示，但训练监督仍限于Q-A对。
- **LL3DA**：基于大语言模型的3D助手，直接输入点云，代表了端到端点云理解的路线。
- **Scene-LLM**：用于具身智能推理的混合特征3D视觉语言基线，关注场景理解与任务执行的结合。

上述基线在SCoT-Analysis和SCoT-Planning任务上的对比结果（Table 3、Table 4）揭示了一个一致的模式：**所有基线在加入CoT训练后，其可解释性（Explainability）、忠实性（Faithfulness）和可信度（Trustworthiness）均获得显著提升**——平均提升幅度分别为6.21%、11.74%和10.02%。这表明CoT监督的收益具有跨架构的通用性，而非特定模型设计的产物。

值得注意的是，SCoT-Reasoner在模型架构上引入了**ORS（Object-Relation-Scene）细化模块**，通过空间图+Graph-Transformer融合绝对位置和相对关系信息，生成对象-关系-场景增强表示。这一设计与Chat Scene的ORC-like表示有相似之处，但SCoT-Reasoner将其与CoT训练策略深度耦合，使得模型能够在推理步骤中显式引用ORS模块提取的空间关系——这正是`<SI>`标签机制发挥作用的基础。

### 3. 与推理增强型3D数据集的定位差异

Table 1将SCoT与近期出现的推理增强型3D数据集进行了对比，其中**3D-R1**是一个重要的参照点。在MSQA-ScanNet的零样本泛化测试中（Table 6），SCoT-Reasoner在导航（Navigation）子任务上比3D-R1高出14.6个百分点，总体得分达到54.4，不仅超越了GPT-4o的零样本表现（+2.1分），还达到了与域内监督模型相当的水平。这一结果表明，SCoT的场景锚定CoT（通过`<SI>`标签强制引用场景证据）比3D-R1的推理标注方式在跨场景泛化中更具优势。

### 4. 适用边界与局限

当前SCoT框架的适用边界受以下因素制约：

1. **场景域限制**：SCoT数据集基于Matterport3D、3RScan、MultiScan、Structured3D、ProcTHOR等室内数据集构建，模型在真实开放3D环境（如城市场景、动态室外环境）中的性能尚未验证。论文明确指出未来的工作将扩展到更多样化和动态的城市级场景。

2. **推理效率瓶颈**：完整的CoT+`<SI>`设置虽然带来最高综合评分，但推理时间增加2.0–3.2倍（例如场景分析从5.08秒增至13.30秒，见Table 9）。这一延迟使得当前框架难以直接应用于实时机器人等时间敏感型应用。

3. **推理步骤间的一致性问题**：论文坦承CoT推理步骤之间可能存在潜在的不一致性，但未提供系统性的检测或缓解机制。这为后续研究留下了空间——例如引入自洽性验证（self-consistency）或结构因果图来约束推理链条。

4. **感知任务中的CoT幻觉**：尽管SCoT选择在感知任务中不使用CoT以避免性能下降，但如何从根本上减少CoT引发的幻觉（而非简单回避）仍是一个开放问题。自动决定何时生成CoT的自适应机制可能是未来的解决方向。

### 5. 开放问题

基于上述分析，SCoT范式引出了以下值得后续探索的问题：

- **自适应CoT触发**：能否训练一个轻量级门控模块，根据输入问题的复杂度自动决定是否生成CoT，从而在感知任务中避免幻觉、在分析/规划任务中充分利用推理能力？
- **推理效率优化**：如何通过推理步骤压缩、提前终止或并行化来降低CoT推理的延迟，使其适用于实时应用场景？
- **室外大规模场景迁移**：SCoT的场景锚定生成范式能否有效迁移到室外城市级3D场景？在更大空间尺度下，`<SI>`标签的引用精度和场景上下文的完备性是否仍能保证？
- **更强的忠实性保障机制**：除了`<SI>`标签，是否可以通过自洽性验证、反事实推理或结构化因果图来进一步确保推理链条的真实性和忠实度？这些机制能否与现有的LLM评估框架（如ChatGPT-4.1、Qwen、DeepSeek的独立打分）形成互补？

## 原文 PDF

![[paperPDFs/ICLR_2026/SCoT_Teaching_3D_LLMs_to_Think_Spatially_with_Million_scale_CoT_Annotations.pdf]]
