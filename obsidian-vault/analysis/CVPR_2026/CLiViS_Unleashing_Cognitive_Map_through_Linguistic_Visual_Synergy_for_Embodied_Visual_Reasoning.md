---
title: "CLiViS: Unleashing Cognitive Map through Linguistic-Visual Synergy for Embodied Visual Reasoning"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/CLiViS_Unleashing_Cognitive_Map_through_Linguistic_Visual_Synergy_for_Embodied_Visual_Reasoning.pdf
project_link: null
code_link: "https://github.com/Teacher-Tom/CLiViS"
aliases:
- CLiViS
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: LLM驱动的高层任务分解与VLM的开放式感知协同，通过动态认知地图迭代积累任务相关视觉证据，实现感知与推理的闭环。
primary_logic: 通过构建可演化的结构化认知地图（导航图+关系图）作为桥梁，使LLM能主动指导VLM进行针对性感知，从而结合LLM的推理与VLM的感知优势。
claims:
- CLiViS在OpenEQA、EgoTempo、EgoSchema三个基准上均取得最优性能，平均准确率显著超越各范式最强基线（Socratic-based +20.2%, 端到端VLM +2.9%, 视频推理 +14.3%）。
- 消融实验表明，将多轮迭代协同缩减为单轮导致准确率下降10.5%，将LLM替换为VLM更引致12.4%下降，验证了迭代LLM-VLM协同的必要性。
- 在不同VLM骨干（Qwen2.5-VL, InternVL3, VideoLLaMA3）上，CLiViS均实现一致且显著的性能提升（+2.0%~+4.3%），证明其模型无关的通用性。
- EgoSchema 上 Accuracy = 69.4 (CLiViS w/ InternVL3)
---

# CLiViS: Unleashing Cognitive Map through Linguistic-Visual Synergy for Embodied Visual Reasoning

> [!tip] 核心洞察
> 通过构建可演化的结构化认知地图（导航图+关系图）作为桥梁，使LLM能主动指导VLM进行针对性感知，从而结合LLM的推理与VLM的感知优势。

| 字段 | 内容 |
|------|------|
| 中文题名 | CLiViS：通过语言-视觉协同释放认知地图用于具身视觉推理 |
| 英文题名 | CLiViS: Unleashing Cognitive Map through Linguistic-Visual Synergy for Embodied Visual Reasoning |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2506.17629) · [Code](https://github.com/Teacher-Tom/CLiViS) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | CLiViS |
| Dataset | EgoSchema, EgoTempo, OpenEQA |

> [!tip] 效果简介
> - EgoSchema 上，Accuracy 69.4 (CLiViS w/ InternVL3) vs 60.0 (VideoTree, 估计值) (+9.4)。
> - EgoTempo 上，Accuracy 36.8 (CLiViS w/ GPT-4.1) vs 34.2 (GPT-4.1) (+2.6)。
> - OpenEQA 上，Accuracy (Likert score ≥4) 57.3 (CLiViS w/ VideoLLaMA3) vs — (—)。

## 概述

具身视觉推理（Embodied Visual Reasoning, EVR）要求模型从长时第一人称视频中提取细粒度视觉线索并进行高层语义推理，以回答关于场景、动作和事件的复杂问题。现有方法面临一个核心瓶颈：基于视频描述的方法将视频压缩为文本后丢失关键视觉细节，而端到端视觉语言模型（VLM）虽能保留视觉信息，却缺乏步骤化的组合推理能力。此外，长时视频的时空动态复杂性进一步加剧了这一感知与推理之间的张力。

CLiViS 提出了一种训练无关（training-free）的框架，通过语言-视觉协同来释放认知地图的潜力，从而桥接感知与推理。其核心洞察在于：构建一个可演化的结构化认知地图作为桥梁，使大语言模型（LLM）能够主动指导 VLM 进行针对性感知，从而结合 LLM 的推理优势与 VLM 的感知优势。具体而言，LLM 负责高层任务分解与子指令生成，VLM 在指定视频片段上执行定向感知，二者的输出被整合为动态更新的认知地图与证据记忆，最终支撑 LLM 的综合推理与答案生成。

实验结果表明，CLiViS 在 OpenEQA、EgoTempo 和 EgoSchema 三个基准上均取得最优性能，平均准确率显著超越各范式最强基线——相比 Socratic-based 方法提升 20.2%，相比端到端 VLM 提升 2.9%，相比视频推理方法提升 14.3%。消融实验进一步验证了多轮迭代协同的必要性：将推理过程压缩为单轮导致准确率下降 10.5%，用 VLM 替换 LLM 作为规划者更引致 12.4% 的下降。此外，CLiViS 在 Qwen2.5-VL、InternVL3、VideoLLaMA3 等不同 VLM 骨干上均实现一致且显著的性能提升（+2.0%～+4.3%），证明了其模型无关的通用性。

## 背景与动机

### 具身视觉推理的双重挑战

具身视觉推理（Embodied Visual Reasoning, EVR）要求模型从第一人称长视频中理解复杂场景并回答用户指令。该任务可形式化为 $R = f_{\theta}(V, I)$，即给定输入视频 $V$ 和指令 $I$，生成响应 $R$。其核心难点在于同时处理两个高度耦合的子问题：**细粒度视觉感知**与**高层语义推理**。

具体而言，模型必须从长时间跨度的视频流中精准捕捉与任务相关的视觉细节——例如物体的属性变化、空间位置转移、人物交互动作——同时将这些碎片化的感知证据组织成连贯的逻辑链条，最终推导出符合指令意图的答案。这两个需求天然存在张力：感知要求对视觉信号保持高保真度，而推理则需要在语义空间中进行抽象与组合。

### 现有范式的结构性缺陷

当前 EVR 方法可归纳为三类范式，但各自存在难以逾越的瓶颈：

**基于视频描述的方法（Socratic-based）** 先将视频转化为文本描述，再由 LLM 进行推理，即 $R = \text{LLM}(\text{Capt}(V), I)$。该类方法严重依赖描述质量，而文本化过程不可避免地丢失关键视觉细节——空间位置、物体外观、动作时序等精细信息在转译中衰减，导致 LLM 在推理时缺少必要的感知锚点。

**端到端 VLM 方法** 直接对视频进行编码并输出答案。虽然保留了更丰富的视觉表征，但这类模型缺乏显式的步骤化组合推理能力：它们难以将复杂指令分解为可逐一验证的子任务，也无法在长视频中主动搜索与任务相关的视觉证据。面对需要多跳推理的场景，端到端 VLM 往往退化为对整体视觉印象的模糊匹配。

**视频推理方法（Video Reasoning）** 引入多步推理机制，但通常依赖固定的感知策略，无法根据推理进程动态调整感知焦点。当 LLM 在推理中产生新的假设或信息需求时，这些方法缺乏将高层语义意图反馈至感知层的闭环通道。

### 核心瓶颈与本文动机

上述范式的共同症结在于**感知与推理的割裂**：感知模块被动提供固定表征，推理模块在封闭的语义空间内运作，两者之间缺少双向交互的桥梁。这使得现有方法无法实现“带着问题去看，看着结果去推”的认知闭环。

CLiViS 的提出正是为了打破这一僵局。其核心洞察是：若能构建一个可演化的结构化场景表示作为感知与推理的共享中介，LLM 便能主动指导 VLM 进行针对性感知，而 VLM 的感知结果又能即时更新 LLM 的推理状态。这种 **LLM-VLM 协同**机制使模型兼具 LLM 的任务分解与逻辑推理能力，以及 VLM 的开放式视觉感知能力，从而在具身视觉推理中实现感知与推理的真正融合。

## 核心创新

CLiViS 的核心创新在于突破现有具身视觉推理（EVR）方法中感知与推理割裂的瓶颈，提出了一种**LLM 规划、VLM 感知的迭代协同框架**。该框架通过动态演化的结构化认知地图作为桥梁，使 LLM 能够主动指导 VLM 进行任务导向的定向感知，从而将高层语义推理与细粒度视觉感知闭合为统一循环。

### 关键设计转变：从被动描述到主动感知引导

现有 EVR 范式存在三个相互对立的困境（Figure 1）：基于视频描述的方法（Socratic-based）依赖文本中介，丢失关键视觉细节；端到端 VLM 缺乏步骤化组合推理能力；视频推理方法虽有多步推理，但感知仍停留于被动特征提取。CLiViS 从根本上改变了这一格局——**将 LLM 从被动的文本消费者转变为主动的感知规划者**，使其能够根据当前推理状态动态生成子任务，引导 VLM 在特定视频片段上执行定向感知。

这一转变体现在以下三个 changed slots 上：

1. **推理流程**：从单步 VLM 推理或两阶段“描述-推理”范式，转变为**迭代式 LLM 规划—VLM 感知的协同推理**（Eq. 2-4）。LLM 基于当前认知状态分解子任务 $T_i$，VLM 在对应片段 $V_{T_i}$ 上执行感知，输出结果反馈至 LLM 以更新认知并生成下一轮子任务，形成“假设-验证”闭环。

2. **场景表示**：从静态文本描述或稠密特征编码，转变为**动态演化的结构化认知地图** $\mathcal{M} = \{\mathcal{G}_{nav}, \mathcal{G}_{rel}\}$（Eq. 5）。导航图 $\mathcal{G}_{nav}$ 捕获时间片段及其关联实体，关系图 $\mathcal{G}_{rel}$ 记录实体间的细粒度语义关系。这一图结构表示随推理迭代持续更新（Eq. 7），使场景理解从一次性快照变为增量积累过程。

3. **任务依赖记忆**：从无记忆或简单对话历史，转变为**证据记忆模块** $\mathcal{E} = (r, \tau, O)$（Eq. 6），每条证据原子包含语言论据 $r$、时间跨度 $\tau$ 和涉及的对象集合 $O$。该模块在每轮迭代中追加推理相关依据（Eq. 8），为 LLM 的最终决策提供可追溯的证据链。

### 协同机制的本质：因果杠杆

CLiViS 的因果杠杆在于**LLM 驱动的高层任务分解与 VLM 的开放式感知协同，通过认知地图实现感知与推理的闭环**。这一机制解决了 EVR 的核心瓶颈——长时视频中时空动态复杂，单一模型难以同时兼顾全局推理与局部细节。LLM 负责“知道该看什么”，VLM 负责“看清楚是什么”，认知地图则作为两者的共享工作记忆，持续积累任务相关的视觉证据。

消融实验直接验证了这一协同机制的必要性（Table 3）：将多轮迭代压缩为单轮导致准确率下降 **10.5%**，而将 LLM 规划者替换为 VLM 更引致 **12.4%** 的下降——这表明 LLM 的高层规划能力与 VLM 的感知能力不可相互替代，二者的迭代协同是性能提升的根本来源。

## 整体框架

CLiViS 将具身视觉推理（EVR）重新定义为 LLM–VLM 协同构建动态认知地图的过程，而非传统的单步推理或视频描述后推理范式。其核心公式为：

$$R = \mathrm{LLM}\left( \mathcal{M}, I \mid \mathcal{M} = \bigcup_{T_i \in \mathrm{LLM}(I, \mathcal{M})} \mathrm{VLM}(V, T_i) \right)$$

其中，LLM 基于动态演化的认知地图 $\mathcal{M}$ 进行推理，而 $\mathcal{M}$ 则由 VLM 在 LLM 分解的子任务 $T_i$ 引导下从视频 $V$ 中逐步构建。这一闭环机制使 LLM 能够主动指导 VLM 进行针对性感知，而非被动接受静态描述。

### 推理三阶段

CLiViS 的推理流程分为三个核心阶段（Figure 2）：

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/002_Figure_2.jpg]]
*Figure 2: Overall Framework. The inference of CLiViS consists of three steps: (1) initialize the cognitive map and evidence memory from segmented scene descriptions; (2) iteratively update task-relevant visual cues via LLM–VLM interaction; and (3) integrate context for final answer generation*

**阶段一：认知与记忆初始化。** 首先将视频切分为固定时长片段（如 30 秒），由 VLM 为每个片段生成粗粒度视觉描述。LLM 随后解析这些描述，提取实体、动作和时空关系，构建初始认知地图 $\mathcal{M}^{(0)}$ 与证据记忆 $\mathcal{E}^{(0)}$。

**阶段二：迭代式语言-视觉协同。** 这是 CLiViS 的核心循环。在每一轮迭代中，LLM 基于当前认知状态 $\mathcal{M}^{(i-1)}$ 和原始指令 $I$，生成针对特定视频片段的子任务查询 $T_i$。VLM 在指定片段上执行该子任务，提取任务相关的视觉证据。LLM 随后整合 VLM 输出，识别新实体或关系、解决冲突，更新认知地图：

$$\mathcal{M}^{(i)} = Update\left( \mathcal{M}^{(i-1)}, \mathrm{VLM}(V_{T_i}, T_i) \right)$$

同时，将推理相关的依据（包含语言论据、时间跨度和涉及的对象集合）追加到证据记忆：

$$\mathcal{E}^{(i)} = Update\left( \mathcal{E}^{(i-1)}, \mathrm{VLM}(V_{T_i}, T_i) \right)$$

**阶段三：集成推理与答案生成。** LLM 综合当前认知地图 $\mathcal{M}^{(i)}$ 与证据记忆 $\mathcal{E}^{(i)}$，判断信息充分性：

$$R_i = \mathrm{LLM}\left( \mathcal{M}^{(i)}, \mathcal{E}^{(i)}, I \right)$$

若信息充分，则生成最终答案；否则返回阶段二，发起新一轮子任务查询。这一自适应机制使推理深度与视频复杂度相匹配（Figure 5）。

### 认知地图与证据记忆

认知地图是 CLiViS 的核心表示结构，由两个互补的子图构成：

$$\mathcal{M} = \left\{ \mathcal{G}_{nav}, \mathcal{G}_{rel} \right\} = \left\{ (V_{nav}, E_{nav}), (V_{rel}, E_{rel}) \right\}$$

- **导航图** $\mathcal{G}_{nav}$：以视频时间片段为节点，记录各片段包含的实体，支撑 LLM 定位到需要进一步感知的时空区域。
- **关系图** $\mathcal{G}_{rel}$：以实体为节点，记录实体间的细粒度关系（如空间位置、交互动作），为推理提供结构化语义支撑。

证据记忆 $\mathcal{E}$ 则由一系列证据原子组成：

$$\mathcal{E} = (r, \tau, O)$$

每个证据原子包含语言论据 $r$、时间跨度 $\tau$ 以及涉及的对象/区域/动作集合 $O$，确保推理过程的可追溯性。

### 与现有范式的区别

相比三类主流方法，CLiViS 的框架设计具有本质差异：
- **Socratic-based 方法**（如 Qwen2.5-VL + Qwen2.5-Max）将视频描述与 LLM 推理解耦为两阶段，丢失关键视觉细节；
- **端到端 VLM**（如 InternVL3、VideoLLaMA3）直接输入视频进行推理，缺乏步骤化组合推理能力；
- **视频推理方法**（如 VideoAgent、VideoTree）虽引入多步推理，但缺乏结构化的动态记忆机制。

CLiViS 通过 LLM 规划–VLM 感知的迭代闭环，将三者的优势融合：LLM 的高层任务分解能力、VLM 的开放词汇感知能力、以及认知地图提供的结构化多步推理支撑。消融实验证实了这一设计的必要性——将多轮迭代压缩为单轮导致准确率下降 10.5%，将 LLM 规划者替换为 VLM 则引致 12.4% 的退化（Table 3）。

### 补充图表

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/001_Figure_1.jpg]]
*Figure 1: Comparison of our proposed CLiViS with previous methods. CLiViS bridges perception and reasoning by combining the strengths of LLMs and VLMs*

## 核心模块与公式推导

CLiViS 将具身视觉推理（EVR）重新定义为 LLM 与 VLM 协同构建动态认知地图的过程，其核心形式化表述为：

$$R = \mathrm{LLM}\left(\mathcal{M}, I \mid \mathcal{M} = \bigcup_{T_i \in \mathrm{LLM}(I, \mathcal{M})} \mathrm{VLM}(V, T_i)\right)$$

其中 $R$ 为最终响应，$V$ 为输入视频，$I$ 为任务指令，$\mathcal{M}$ 为动态认知地图，$T_i$ 为 LLM 分解出的子任务。该公式揭示了方法的因果机制：LLM 并非直接对视觉内容推理，而是通过主动生成子任务 $T_i$ 来驱动 VLM 进行定向感知，VLM 的感知结果再反向更新 $\mathcal{M}$，形成感知与推理的闭环。

### 认知地图

认知地图是 CLiViS 的核心结构化表示，由导航图和关系图两个子图构成：

$$\mathcal{M} = \{\mathcal{G}_{nav}, \mathcal{G}_{rel}\} = \{(V_{nav}, E_{nav}), (V_{rel}, E_{rel})\}$$

- **导航图** $\mathcal{G}_{nav}$：以视频时间片段为节点 $V_{nav}$，记录各片段内出现的实体；边 $E_{nav}$ 捕获片段间的时序关联。它为 LLM 提供了“何时去感知”的时空锚点。
- **关系图** $\mathcal{G}_{rel}$：以实体为节点 $V_{rel}$，边 $E_{rel}$ 编码实体间的细粒度语义关系（如空间位置、交互动作）。它使 LLM 能够理解“谁对谁做了什么”。

认知地图在第 $i$ 轮迭代中通过 VLM 对子任务 $T_i$ 的感知输出进行增量更新：

$$\mathcal{M}^{(i)} = \mathrm{Update}\left(\mathcal{M}^{(i-1)}, \mathrm{VLM}(V_{T_i}, T_i)\right)$$

更新过程包括识别新实体与关系、解决与既有地图的冲突，从而让认知地图随推理深入而持续演化。

### 证据记忆

为支撑多步推理中的证据追溯与信息充分性判断，CLiViS 维护一个证据记忆模块。每个证据原子定义为三元组：

$$\mathcal{E} = (r, \tau, O)$$

其中 $r$ 为自然语言论据，$\tau$ 为相关时间跨度，$O$ 为涉及的对象、区域或动作集合。证据记忆的更新遵循：

$$\mathcal{E}^{(i)} = \mathrm{Update}\left(\mathcal{E}^{(i-1)}, \mathrm{VLM}(V_{T_i}, T_i)\right)$$

在第 $i$ 轮，LLM 综合当前认知地图与证据记忆生成响应或下一轮子任务：

$$R_i = \mathrm{LLM}\left(\mathcal{M}^{(i)}, \mathcal{E}^{(i)}, I\right)$$

### 推理管线模块

CLiViS 的推理流程由七个功能模块串联而成：

1. **视频分段与描述**：将视频切分为固定时长片段（如 30 秒），由 VLM 生成粗粒度场景描述，作为认知地图初始化的原料。
2. **认知与记忆初始化**：LLM 解析片段描述，提取实体、动作和关系，构建初始 $\mathcal{M}^{(0)}$ 与 $\mathcal{E}^{(0)}$。
3. **子指令生成**：LLM 基于当前认知状态与原始指令 $I$，生成针对特定片段的定向子任务 $T_i$（如“检查第 2 段中人物是否拿起杯子”）。
4. **VLM 感知执行**：VLM 在指定片段 $V_{T_i}$ 上执行 $T_i$，提取任务相关的细粒度视觉证据。
5. **认知地图更新**：LLM 整合 VLM 输出，执行 $\mathcal{M}^{(i)}$ 的增量更新。
6. **证据记忆更新**：将本轮推理依据追加到 $\mathcal{E}^{(i)}$。
7. **集成推理与答案生成**：LLM 判断信息充分性，若充分则输出最终答案 $R$，否则进入下一轮迭代。

该管线通过迭代式 LLM-VLM 协同，使高层任务分解与开放式视觉感知相互增强，避免了纯描述方法的信息丢失和端到端 VLM 缺乏步骤化推理的局限。

### 补充图表

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/003_Figure_3.jpg]]
*Figure 3: Cognitive Map consists of a navigation graph and a relation graph. The former captures temporal regions and associated entities. The latter records fine-grained relations between entities*

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/004_Figure_4.jpg]]
*Figure 4: Prompt for LLM-VLM Synergy. For brevity, the prompt here is abbreviated. Please refer to appendix for the complete version*

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/013_Figure_7.jpg]]
*Figure 7: Qualitative results of Cognitive Map and Sub-Instrction Generation*

## 实验与分析

### 主实验结果

CLiViS在三个代表性具身视觉推理基准上均取得了最优性能，平均准确率达到49.4%，显著超越三类主流范式的各自最强基线。Table 1汇总了统一配置下的公平比较结果。

在OpenEQA上，CLiViS（搭配VideoLLaMA3骨干）以57.3的Likert评分（≥4）取得第一，较Socratic式基线提升20.2个百分点，较端到端VLM提升2.9个百分点。在EgoTempo上，CLiViS（搭配InternVL3）以23.0的准确率领先视频推理方法14.3个百分点。在EgoSchema上，CLiViS（搭配InternVL3）达到69.4%，较视频推理最强基线VideoTree（约60.0%）高出约9.4个百分点。这一跨基准的全面领先表明，CLiViS通过整合LLM的语言推理、VLM的开放词汇感知以及多步推理的动态认知地图，有效弥补了单一范式的结构性短板。

### 消融实验

Table 3在EgoTempo上系统拆解了CLiViS各组件的贡献，所有实验统一使用InternVL3与Qwen2.5-Max组合。

**多轮迭代协同**是性能的核心支柱。将推理过程压缩为单轮（即仅执行一次LLM分解与VLM感知）导致准确率骤降10.5%，验证了迭代式假设-验证循环对于逐步积累任务相关视觉证据的不可替代性。

**LLM作为规划者**的角色不可由VLM替代。将LLM替换为VLM作为任务分解与认知地图更新的规划者，准确率下降12.4%。这说明高层任务分解、子指令生成与冲突消解需要LLM的强推理能力，VLM的视觉感知优势无法弥补其在结构化规划上的不足。

**证据记忆模块**的移除同样导致性能退化（具体退化幅度需核实原文Table 3数据，当前证据置信度0.8）。证据原子通过记录论据、时间跨度与对象集合，为LLM的最终集成推理提供了可追溯的推理依据，缺失该模块将削弱多轮推理的信息积累效率。

### 模型无关性验证

Table 2展示了CLiViS在不同VLM骨干上的性能增益。在Qwen2.5-VL、InternVL3和VideoLLaMA3三种VLM上，CLiViS分别带来+2.0%、+4.3%和+2.6%的一致提升（均搭配Qwen2.5-Max作为LLM）。这一结果证明CLiViS的协同框架对底层VLM选择不敏感，其性能增益源于LLM-VLM协同机制本身，而非特定模型的偏置。

### 推理延迟与效率分析

Table 4在EgoSchema上对比了CLiViS与各基线的延迟-准确率权衡。CLiViS以约195秒的推理延迟取得69.4%的准确率，在训练无关方法中具有竞争力的效率，但相比端到端VLM（通常数秒级延迟）仍存在显著差距。Figure 5进一步揭示了推理轮次与视频时长的正相关关系，表明CLiViS能够根据任务复杂度自适应分配推理深度，而非固定轮次。

### 细分问题类别分析

Table 5在EgoTempo的问题类别维度上展开对比。CLiViS在推理密集型类别（如因果推理、时序关系判断）上优势尤为突出，这得益于认知地图对时空实体关系的显式建模与证据记忆对推理链的可追溯支持。相比之下，在简单事实检索类别上，端到端VLM的差距较小，说明CLiViS的增益主要来自复杂推理场景。

### 与前沿海量模型的对比

Table 6将CLiViS与GPT-4.1、Gemini-2.5-flash等前沿多模态模型在EgoTempo上进行对比。CLiViS（搭配GPT-4.1）以36.8%的准确率超越GPT-4.1原生的34.2%，表明即使在强基线模型上，LLM-VLM协同框架仍能通过结构化认知地图与迭代感知带来额外增益。

### 失败模式与局限性

尽管CLiViS在多个基准上取得最优，其性能仍受限于以下因素：

1. **离线被动场景限制**：当前工作仅聚焦于被动视频问答（EM-EQA），尚未扩展到交互式主动导航（A-EQA），受限于主动场景数据的可用性。
2. **基础模型能力瓶颈**：作为训练无关框架，CLiViS的性能上限由预训练LLM和VLM的能力决定，未针对具体任务进行微调。
3. **实时性不足**：约195秒的推理延迟使其难以满足机器人实时交互需求，尽管在同等方法中已具竞争力。
4. **感知粒度依赖**：VLM的开放式感知虽灵活，但在细粒度物体识别与精确定位上仍可能出错，错误会在认知地图更新中累积传播。

### 补充图表

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/005_Table_1.jpg]]
*Table 1: Performance comparison with other methods across different benchmarks. All results are reproduced under unified settings with the same model configurations (e.g., FPS, temperature). Best results are marked in bold, and the second-best is underlined*

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/008_Table_3.jpg]]
*Table 3: Ablation studies on EgoTempo. We evaluate each component of CLiViS using the combination of InternVL3 and Qwen2.5-Max*

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/006_Table_2.jpg]]
*Table 2: Model-agnostic effectiveness. CLiViS achieves consistent improvements across different VLMs, showing strong model-agnostic effectiveness. All experiments use Qwen2.5-Max as the LLM*

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/007_Table_4.jpg]]
*Table 4: Latency and Accuracy on EgoSchema*

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/009_Table_5.jpg]]
*Table 5: Performance Comparison on Various Question Categories of the EgoTempo benchmark. Best results are marked in bold, and the second-best is underlined*

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/010_Table_6.jpg]]
*Table 6: Comparison with Frontier Multimodal Models on EgoTempo*

![[assets/figures/papers/paper_list_l2379_https_arxiv_org_abs_2506_17629/figures/011_Figure_5.jpg]]
*Figure 5: Correlation between reasoning rounds and video duration*

## 方法谱系与知识库定位

### 1. 范式定位：三种主流路线的交汇点

CLiViS 并非凭空产生，而是站在三类既有范式的交叉点上，试图取长补短：

| 范式 | 代表基线 | 核心思路 | 瓶颈 |
|------|----------|----------|------|
| **Socratic-based** | Qwen2.5-VL + Qwen2.5-Max、InternVL3 + Qwen2.5-Max | 先对视频进行整体描述（Caption），再将文本描述送入 LLM 进行推理 | 视频描述环节不可避免地丢失细粒度视觉细节，导致感知瓶颈传递至推理阶段 |
| **端到端 VLM** | Qwen2.5-VL、InternVL3、VideoLLaMA3 | 将视频与指令直接输入 VLM，由单一模型完成感知与推理 | 缺乏步骤化的组合推理能力，面对长时视频的复杂时空动态时容易产生幻觉或遗漏关键线索 |
| **视频推理方法** | VideoAgent、VideoTree、Video-R1 | 通过多步调用 VLM 或引入推理链来增强时序理解 | 感知与推理的耦合仍较松散，VLM 的感知过程缺乏高层任务规划的主动引导 |

CLiViS 的核心贡献在于**将这三种范式的优势系统性地融合**：它继承了 Socratic-based 范式中 LLM 的语言推理能力，保留了端到端 VLM 的开放词汇感知能力，同时吸收了视频推理方法的多步推理机制。但 CLiViS 的关键突破在于，它改变了三者之间“各自为政”的松散关系——通过**动态认知地图**作为桥梁，使 LLM 能够主动指导 VLM 进行针对性感知，形成“假设-验证”的闭环迭代。

### 2. 技术谱系中的“因果旋钮”：从被动描述到主动协同

理解 CLiViS 在方法谱系中的位置，需要抓住一个核心的“因果旋钮”：**LLM 与 VLM 之间的信息流向与控制关系**。

- **Socratic-based 范式**中，信息流是单向的：VLM → LLM。VLM 先生成描述，LLM 再被动接收并推理。LLM 无法向 VLM 提出“请帮我确认某处是否发生了某事”的请求。
- **端到端 VLM 范式**中，信息流是隐式的：感知与推理在同一个黑箱模型中完成，无法解耦，也无法显式控制。
- **CLiViS** 将信息流重构为**双向闭环**：LLM 根据当前认知状态分解子任务，VLM 在指定视频片段上执行定向感知，感知结果反馈回 LLM 以更新认知地图，进而生成下一轮子任务。这一“LLM 规划—VLM 感知—认知更新”的循环，是 CLiViS 区别于所有基线方法的结构性创新。

从公式层面看，这一转变清晰可见。传统范式可概括为：

$$R = \operatorname{LLM}(\mathbf{Cap}(V), I) \quad \text{或} \quad R = \operatorname{VLM}(V, I)$$

而 CLiViS 将其重构为：

$$R = \operatorname{LLM}\left(\mathcal{M}, I \mid \mathcal{M} = \bigcup_{T_i \in \operatorname{LLM}(I, \mathcal{M})} \operatorname{VLM}(V, T_i)\right)$$

其中认知地图 $\mathcal{M}$ 不再是一次性生成的静态文本，而是在 LLM 与 VLM 的多轮交互中**动态演化**的结构化表示。

### 3. 适用边界与局限

CLiViS 的设计假设和实验范围定义了其当前适用边界：

**任务边界**：当前工作聚焦于**离线被动视频问答**（EM-EQA），即给定一段已录制的第一人称视频和一条自然语言指令，系统需要基于视频内容给出答案。论文明确指出，尚未扩展到**交互式主动导航场景**（A-EQA），后者要求智能体在环境中实时移动并主动采集视觉信息以完成目标。作者将此归因于数据可用性的限制，但本质上，A-EQA 对推理延迟和实时决策能力提出了更高要求，而这恰恰是 CLiViS 当前架构的薄弱环节。

**模型依赖**：CLiViS 是一个**训练无关**（training-free）框架，完全依赖预训练的 LLM 和 VLM，未对任何组件进行任务特定的微调。这意味着其性能上限受基础模型能力的硬约束。Table 2 的实验表明，当 VLM 骨干从 InternVL3 切换到 VideoLLaMA3 时，CLiViS 的绝对性能也随之变化——框架本身提供的是相对提升（+2.0%~+4.3%），而非对弱模型的“起死回生”。

**推理延迟**：尽管在训练无关方法中 CLiViS 的推理延迟具有竞争力，但相比端到端模型仍显著偏高。在 EgoSchema 上，CLiViS 的推理时间约为 195 秒（Table 4），而端到端 VLM 通常可在数秒内完成。这一延迟来源于多轮 VLM 调用和 LLM 推理的累积成本，使其难以满足实时应用（如机器人交互）的需求。

### 4. 证据强度评估

支撑 CLiViS 核心主张的证据链条较为完整，但存在不同置信度层次：

- **高置信度（≥0.95）**：CLiViS 在三个基准（OpenEQA、EgoTempo、EgoSchema）上均取得最优性能，且相对各范式最强基线的提升幅度显著（Socratic-based +20.2%，端到端 VLM +2.9%，视频推理 +14.3%）。消融实验证实了多轮迭代协同（单轮退化 10.5%）和 LLM 规划不可替代性（替换为 VLM 退化 12.4%）的关键作用。模型无关性验证（Table 2）进一步排除了“仅对特定 VLM 有效”的替代解释。

- **中等置信度（~0.8）**：证据记忆模块的消融实验声称移除后性能退化，但具体退化幅度在可用分析中标注为“超过 X%”，需查阅原论文 Table 3 确认精确数值。

- **待验证**：CLiViS 与 VideoAgent、VideoTree、Video-R1 等视频推理基线的比较结果在分析中仅以汇总形式呈现（+14.3% 平均提升），各基准上的逐项对比需对照原论文 Table 1 进行交叉验证。

### 5. 开放问题与未来方向

基于 CLiViS 的当前局限和方法设计，以下方向值得关注：

1. **向主动具身推理的扩展**：能否将 CLiViS 的认知地图机制与导航策略结合，使 LLM 不仅能分析已有视频，还能规划“下一步应该看向哪里”？这需要解决认知地图的实时更新与动作决策的耦合问题。

2. **推理延迟的优化**：195 秒的推理时间限制了实际部署。可能的优化路径包括：并行化多个子任务的 VLM 调用（当前为串行迭代）、引入缓存机制避免重复感知相同片段、或通过知识蒸馏将多轮协同压缩为更高效的单模型推理。

3. **认知地图的学习优化**：当前认知地图的构建与更新完全依赖 LLM 的提示工程，未经过任务特定的优化。是否可以引入强化学习或参数高效微调（如 LoRA），使认知地图的更新策略在保持训练无关优势的同时获得任务适应性提升？

4. **外部知识的融合**：认知地图的图结构表示天然适合与外部知识图谱对接。在零样本场景下，引入常识知识库或场景图谱是否能增强 CLiViS 对未见实体和关系的泛化能力？

## 原文 PDF

![[paperPDFs/CVPR_2026/CLiViS_Unleashing_Cognitive_Map_through_Linguistic_Visual_Synergy_for_Embodied_Visual_Reasoning.pdf]]
