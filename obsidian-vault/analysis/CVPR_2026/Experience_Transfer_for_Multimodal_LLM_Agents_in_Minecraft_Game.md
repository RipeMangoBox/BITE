---
title: Experience Transfer for Multimodal LLM Agents in Minecraft Game
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Experience_Transfer_for_Multimodal_LLM_Agents_in_Minecraft_Game.pdf
project_link: null
code_link: null
aliases:
- ETMLAMG
tags:
- CVPR_2026
- topic/representation_self_supervised_transfer
- topic/representation_self_supervised_transfer/representation_learning
core_operator: 引入五个显式迁移维度（结构、属性、过程、功能、交互）并结合上下文内类比学习（ICAL），主动检索、适应和复用历史经验。
primary_logic: 将可复用的环境与交互知识按结构、属性、过程、功能、交互五维显式分解，并在统一的上下文状态描述符（CSD）上实施上下文内类比学习（ICAL），使模型能够通过类比推理在任务间迁移知识，实现加速学习和爆发式解锁。
claims:
- Echo 在从零学习的目标解锁任务上实现了1.3×–1.7×的加速。
- 移除属性轴导致Recipe类任务成功率显著下降约11%。
- 移除程序轴导致Crafting Chain类任务成功率下降约12%。
- ICAL 能够识别任务步骤中的模式（收集材料、使用工作台、排列材料）并加以适应，从而实现跨任务知识迁移。
---

# Experience Transfer for Multimodal LLM Agents in Minecraft Game

> [!tip] 核心洞察
> 将可复用的环境与交互知识按结构、属性、过程、功能、交互五维显式分解，并在统一的上下文状态描述符（CSD）上实施上下文内类比学习（ICAL），使模型能够通过类比推理在任务间迁移知识，实现加速学习和爆发式解锁。

| 字段 | 内容 |
|------|------|
| 中文题名 | 面向Minecraft游戏的多模态LLM代理经验迁移 |
| 英文题名 | Experience Transfer for Multimodal LLM Agents in Minecraft Game |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2604.05533) |
| Topic | #topic/representation_self_supervised_transfer #topic/representation_self_supervised_transfer/representation_learning |
| Method | Echo |
| Dataset | Recipe, Object Unlocking Progress, Continuous Learning |

> [!tip] 效果简介
> - Recipe (Bed) 上，Success@0→30 92.5 vs 87.5 (JARVIS-1) (+5.0)。
> - Recipe (Iron Pickaxe) 上，Success@0→30 87.5 vs 85.0 (JARVIS-1) (+2.5)。
> - Recipe (Shield) 上，Success@0→30 87.5 vs 80.0 (JARVIS-1) (+7.5)。

## 概要

现有基于多模态大语言模型（MLLM）的开放世界代理（如 **Voyager** (Wang et al., TMLR 2024)、**JARVIS-1** (Wang et al., IEEE TPAMI 2024)、**MP5** (Qin et al., CVPR 2024) 和 **MrSteve** (Park et al., ICLR 2025)）虽然具备一定的记忆与规划能力，但其记忆机制本质上是被动的：历史经验被存储为原始轨迹或技能库，缺乏结构化的迁移维度，导致代理在面临新任务时不得不反复从头学习，效率低下且泛化能力受限。

针对这一瓶颈，本文提出 **Echo** 框架，核心思路是将经验迁移从被动检索升级为主动类比推理。Echo 将可复用的环境与交互知识显式分解为**结构、属性、过程、功能、交互**五个迁移维度，并统一编码为**上下文状态描述符（CSD）**——一种将多模态输入压缩为可比较、可验证的语义快照的表示形式。在此基础上，Echo 实施**上下文内类比学习（ICAL）**，主动从记忆库中检索相关历史案例，通过类比推理适应并验证潜在新任务，从而实现跨任务的知识迁移。

在 Minecraft 的从零学习设定下，Echo 在物品解锁进度上实现了 **1.3×–1.7×** 的加速，并展现出爆发式的连锁解锁现象——在中期阶段短时间内快速解锁多个相似物品。消融实验进一步验证了各迁移维度的因果贡献：移除属性轴导致 Recipe 类任务成功率下降约 11%，移除程序轴使 Crafting Chain 类任务下降约 12%，移除功能轴几乎使 Functional Equivalence 任务失效。这些结果表明，显式的多维知识分解是跨任务迁移的关键使能因素，而非简单的记忆容量扩展。



### 多模态LLM代理的泛化困境

基于多模态大语言模型（MLLM）的具身代理在开放世界任务中展现出强大的感知与规划能力，但其跨任务泛化能力仍面临根本性瓶颈。传统MLLM代理将记忆视为被动存储仓库——仅保存原始轨迹或技能片段，在遇到新任务时缺乏结构化的经验迁移机制。这导致代理在每个新任务上几乎从零开始学习，效率低下且难以形成累积的知识增长。

问题的核心在于：复杂环境中的状态转移和因果关系在不同任务间差异显著，简单地复用历史轨迹无法捕捉可迁移的底层模式。现有方法如 **Voyager**（Wang et al., TMLR 2024）依赖技能库与课程学习，**JARVIS-1**（Wang et al., IEEE TPAMI 2024）使用多模态记忆支持规划，**MP5**（Qin et al., CVPR 2024）结合主动感知进行探索，**MrSteve**（Park et al., ICLR 2025）引入事件记忆机制——但这些方法均未将经验迁移作为显式的结构化过程来设计。其上下文内学习（In-Context Learning, ICL）主要用于被动检索少量历史样本以辅助当前子任务序列的生成，而非主动发现和适应可迁移的知识模式（Figure 1）。

### 核心瓶颈：记忆的结构化与主动迁移缺失

现有工作的根本缺陷可归结为两个层面。其一，**记忆表示缺乏显式的迁移维度**：环境中的可复用知识——物体的结构属性、材料特性、制作流程、功能等价性、交互方式——被混杂在非结构化的轨迹或技能描述中，模型无法按维度对齐和比较不同任务间的相似性。其二，**学习范式是被动而非主动的**：代理仅在需要时检索历史片段，而非主动从记忆库中发现潜在可迁移的新任务并进行验证执行。

这两重缺陷共同造成了一个关键现象：代理在解锁一系列功能相似物品时，无法利用已学经验实现“爆发式”迁移，而是以近似线性的速度逐个攻克，学习效率受到严重制约。

### 本文动机：显式迁移维度与上下文内类比学习

针对上述瓶颈，本文提出 **Echo** 框架，其核心动机是将经验迁移从隐式、被动的副产品转变为一个显式、主动的结构化过程。具体而言，Echo 引入两个相互协同的机制：

1. **五维显式迁移表示**：将可复用的环境与交互知识按结构（Structural）、属性（Attribute）、过程（Procedural）、功能（Functional）、交互（Interaction）五个维度显式分解，形成统一的上下文状态描述符（Contextual State Descriptor, CSD），使多模态输入被压缩为可比较、可验证的语义快照。

2. **上下文内类比学习（In-Context Analogy Learning, ICAL）**：将ICL从被动检索升级为主动的类比推理过程——代理主动从CSD记忆库中检索相关经验，通过多维语义相似度匹配识别可迁移模式，归纳生成潜在新任务的假设，并在执行后验证其有效性。

通过这一设计，Echo 使代理能够在任务间实现类比推理驱动的知识迁移，从而加速学习并产生爆发式的物品解锁现象（Figure 2）。后续章节将详细阐述CSD的构建方式、ICAL的工作流程，以及两者如何协同实现结构化经验迁移。



## 核心方法与创新机理

### 瓶颈定位：从被动记忆到主动经验迁移

现有 MLLM 代理（如 **Voyager** (Wang et al., TMLR 2024)、**JARVIS-1** (Wang et al., IEEE TPAMI 2024)）在 Minecraft 等开放世界中面临一个共同瓶颈：**记忆被视为被动存储**，仅用于检索历史样本以辅助当前子任务序列生成，缺乏结构化的经验迁移能力。这导致代理在跨任务时不断重新学习，效率低下且难以泛化——因为不同任务的状态转移和因果关系各异，传统方法无法识别和复用可迁移的知识模式（参见 Figure 3）。

### 核心因果杠杆：五维显式迁移 + 上下文内类比学习

Echo 的核心创新可归结为两个相互耦合的因果杠杆：

**杠杆一：五维显式迁移空间（changed slot: 记忆表示）**

Echo 将可复用的环境与交互知识按五个维度显式分解：
- **结构轴（Structural）**：物体间的空间与组合关系
- **属性轴（Attribute）**：材料的物理与语义属性
- **过程轴（Procedural）**：任务执行的步骤序列
- **功能轴（Functional）**：物品的功能等价性
- **交互轴（Interaction）**：代理与环境之间的操作模式

这一设计将传统方法中“被动仓库、无结构化迁移维度、仅存储原始轨迹或技能”的记忆表示（baseline value），替换为“五个显式迁移维度统一描述世界状态与交互”的主动表示（proposed value）。其关键载体是**上下文状态描述符（CSD）**（changed slot: 多模态统一表示），将视觉、文本、交互等多模态输入压缩为可比较、可验证的语义快照，解决了传统方法异构信息难以跨任务对齐的问题（参见 Figure 4）。

**杠杆二：上下文内类比学习（ICAL）（changed slot: 学习范式）**

Echo 将 ICL 从被动检索升级为主动过程：代理从 CSD 记忆库中基于多维语义相似度检索 top-K 最相关经验，通过类比推理识别任务步骤中的模式（如“收集材料→使用工作台→排列材料”），将其适应到新任务并生成分层计划与自验证断言。这一范式转变使模型能够**主动检索、适应并验证潜在新任务**，而非仅被动辅助子任务生成（参见 Figure 1 与 Figure 5）。

### 核心洞察

> 将可复用的环境与交互知识按结构、属性、过程、功能、交互五维显式分解，并在统一的上下文状态描述符（CSD）上实施上下文内类比学习（ICAL），使模型能够通过类比推理在任务间迁移知识，实现加速学习和爆发式解锁。

### 与 Baseline 的关键差异总结

| 维度 | 传统方法（Voyager, JARVIS-1 等） | Echo |
|------|----------------------------------|------|
| 记忆表示 | 被动仓库，无结构化迁移维度 | 五维显式迁移轴 + CSD 统一表示 |
| 学习范式 | 被动检索历史样本辅助子任务生成 | 主动 ICAL：检索→适应→验证→执行 |
| 多模态对齐 | 异构信息未统一编码，难以跨任务对齐 | CSD 将多模态输入压缩为可比较语义快照 |
| 验证机制 | 无或简单 | 一致性自检查验计划内部逻辑与外部可行性 |

### 证据支撑

- **加速学习**：Echo 在物品解锁任务上达到 1.3×–1.7× 的加速（Figure 2），并在中期表现出“爆发式解锁”现象——相似物品在短时间内被批量解锁。
- **消融验证**：移除属性轴导致 Recipe 类任务成功率下降约 11%；移除过程轴导致 Crafting Chain 任务下降约 12%；移除功能轴几乎使 Functional Eq. 任务失效（下降约 9%），证明各维度对特定任务类型具有不可替代的贡献（Figure 7）。
- **类比推理**：个案研究（Figure 9）展示了 ICAL 如何通过功能相似性将制作木镐的经验迁移到制作石镐，验证了“识别模式并适应”的核心机制。



Echo 的整体框架遵循经典的感知—记忆—规划—验证—执行循环，其核心创新在于将传统被动式上下文学习（ICL）转变为主动的上下文内类比学习（ICAL），并引入五个显式的迁移维度来结构化记忆与跨任务泛化。图 6 展示了该迭代框架的全貌：系统采用三层架构（感知层、决策层、执行层），与短期和长期记忆系统交互，支撑结构化的 ICAL 和基于案例的知识迁移。

### 核心循环与模块关系

框架的推理过程可形式化为以下步骤：

1.  **感知模块**：处理来自 Minecraft 环境的多模态输入，包括视觉观测、文本信息和交互反馈。
2.  **记忆检索模块**：基于上下文状态描述符（CSD）的向量表示，在记忆库中计算多维语义相似度，检索出与当前状态最相关的 Top-K 历史经验 $S_K$。
3.  **规划模块（含 ICAL）**：指令微调的多模态大语言模型 $f_\theta$ 接收当前观测 $x_t$、检索到的范例 $S_K$ 和协议 protocol，生成层次化规划 $\pi_t$ 与自验证断言 $\mathcal{A}ss_t$，其形式化表达为：
    $$[ \pi _ { t } , { \mathcal A } s s _ { t } ] = f _ { \theta } ( x _ { t } , S _ { K } , \mathrm { p r o t o c o l } )$$
    在此过程中，模型并非被动地使用检索样本来辅助当前子任务序列生成，而是主动从记忆库中检索潜在的新任务，通过类比推理进行验证和执行——这正是 ICAL 与经典 ICL（如 **DEPS** 和 **JARVIS-1** (Wang et al., IEEE TPAMI 2024) 中的被动检索范式）的本质区别（见图 1 的概念对比）。
4.  **验证模块**：一致性自检查验计划的内部逻辑一致性与外部任务可行性。
5.  **执行模块**：执行动作序列并收集轨迹反馈，随后将新的经验更新回记忆库。

### 输入输出流

系统的输入是环境的多模态观测 $x_t$（视觉、文本、交互信号），经 CSD 压缩为可比较的语义快照后，进入记忆检索与 ICAL 规划流程。输出为层次化的动作计划 $\pi_t$，交由执行器在环境中执行。整个循环持续迭代，使代理能够在从零开始的设定下，通过主动检索、适应和复用结构化经验，实现跨任务的加速学习与爆发式解锁。

### 补充图表

![[assets/figures/papers/paper_list_l2388_https_arxiv_org_abs_2604_05533/figures/006_Figure_6.jpg]]
*Figure 6: Overview of our iterative framework. The system performs perception, memory retrieval, planning, verification, and execution in a loop. A three-layer architecture (perception, decision, execution) interacts with short- and long-term memory to support structured ICAL and case-based transfer*



### 上下文状态描述符（CSD）与五维迁移轴

Echo 的核心创新在于将多模态环境表示与历史经验显式分解为五个可解释的迁移维度，形成统一的**上下文状态描述符（Contextual State Descriptor, CSD）**。单个指令微调的 MLLM 作为中心机制，沿五个轴对跨模态对应关系进行表示、对齐和评估：

- **结构轴（Structural）**：描述物体或场景的空间布局与组成关系。
- **属性轴（Attribute）**：刻画物体的材质、颜色、状态等内在属性。
- **过程轴（Procedural）**：记录任务执行的步骤序列与操作流程。
- **功能轴（Functional）**：抽象物体或工具的功能语义与使用目的。
- **交互轴（Interaction）**：编码代理与环境之间的交互模式与动作-反馈关系。

CSD 将视觉、文本和交互信号压缩为紧凑、可比较的语义快照，使得不同任务间的经验能够在统一的向量空间中进行多维语义相似度计算。如 Figure 4 所示，每个 CSD 包含元数据及上述五个语义维度的结构化编码。

![[assets/figures/papers/paper_list_l2388_https_arxiv_org_abs_2604_05533/figures/004_Figure_4.jpg]]
*Figure 4: Overview of the CSD schema*

### 结构化上下文内类比学习（ICAL）

传统方法（如 DEPS、JARVIS-1）将上下文内学习（ICL）视为被动过程——从记忆库中检索少量样本以辅助当前目标的子任务序列生成。Echo 则将 ICL 重新定义为**主动的上下文内类比学习（In-Context Analogy Learning, ICAL）**过程（见 Figure 5 的工作流程）：

![[assets/figures/papers/paper_list_l2388_https_arxiv_org_abs_2604_05533/figures/005_Figure_5.jpg]]
*Figure 5: ICL-based analogical learning workflow using the CSD memory bank*

1. **任务选择**：从 CSD 记忆库中主动检索潜在的新任务。
2. **示例检索**：基于五维 CSD 组件计算多维语义相似度，检索 top-K 最相关历史经验。
3. **上下文构建**：将检索案例组织为类比推理的上下文。
4. **新任务归纳**：模型从上下文中泛化，输出潜在新任务的动作序列。
5. **执行验证**：执行规划并通过自验证模块检查一致性。

ICAL 的核心机制在于：模型能够识别任务步骤中的模式（如收集材料、使用工作台、排列材料）并加以适应，从而将知识从一个任务迁移到另一个任务。Figure 9 的案例研究展示了如何通过功能相似性将制作木镐的经验迁移到制作石镐。

### 迭代推理框架与核心公式

系统遵循经典的代理模型，通过结合 ICAL 与显式迁移轴，实现内部知识的高效利用以支持开放世界任务迁移。Figure 6 展示了完整的感知-记忆-规划-验证-执行循环，三层架构（感知层、决策层、执行层）与短期和长期记忆系统交互。

迭代推理过程的形式化定义如下：

**公式（1）——结构化上下文内学习**：

$$
[ \pi _ { t } , { \cal A } s s _ { t } ] = f _ { \theta } ( x _ { t } , S _ { K } , \mathrm { p r o t o c o l } )
$$

**变量含义**：
- $f_{\theta}$：指令微调的多模态大语言模型（MLLM）
- $x_t$：当前时刻 $t$ 的多模态观测（视觉、文本、交互信号）
- $S_K$：从 CSD 记忆库中基于五维语义相似度检索到的 $K$ 个范例
- $\mathrm{protocol}$：任务协议与约束规范
- $\pi_t$：生成的层次化规划（分层子任务序列）
- $\mathcal{Ass}_t$：自验证断言，用于后续一致性检查

**系统组件形式化**：
- **记忆（Memory）**：$\mathcal{M} = \{ (c_i, \tau_i) \}$，其中 $c_i$ 为 CSD 向量表示，$\tau_i$ 为对应的成功轨迹。
- **迁移空间（Transfer Space）**：五轴语义空间 $\mathcal{T} = \{ \text{Struct}, \text{Attr}, \text{Proc}, \text{Func}, \text{Inter} \}$。
- **检索算子（Retrieval Operator）**：$\mathcal{R}(x_t, \mathcal{M}, \mathcal{T}) \rightarrow S_K$，在多维语义空间中检索最相似的 $K$ 个范例。
- **验证器（Verifier）**：检查规划的内部逻辑一致性与外部任务可行性。
- **执行器（Executor）**：执行规划并收集轨迹反馈。
- **记忆更新（Memory Update）**：将成功轨迹及其 CSD 表示写入记忆库。

### 模块间的因果机制

五个迁移维度并非独立运作，而是通过多维语义相似度计算协同作用。消融实验（Figure 7）揭示了各轴与任务类型之间的因果关联：

- **属性轴**对 Recipe 类任务至关重要（移除导致成功率下降约 11%），因为合成配方高度依赖材料属性的精确匹配。
- **过程轴**对 Crafting Chain 类任务影响最大（移除导致下降约 12%），长链合成依赖步骤序列的结构化迁移。
- **结构轴**对 Functional Eq. 和 Crafting Chain 均有贡献（移除分别导致下降约 7% 和 9%）。
- **功能轴**几乎决定了 Functional Eq. 任务的成败（移除导致下降约 9%），功能等价推理直接依赖功能语义的抽象与对齐。
- **交互轴**对 Utility Blocks 任务影响显著（移除导致下降约 7%），工具使用类任务依赖交互模式的迁移。

这种轴-任务特异性表明，五维分解并非冗余设计，而是针对不同任务类型提供了互补的迁移信号。

### 补充图表

![[assets/figures/papers/paper_list_l2388_https_arxiv_org_abs_2604_05533/figures/001_Figure_1.jpg]]
*Figure 1: Conceptual illustration of Echo. The agent learns from experience and discovers transferable patterns, enabling interpretable analogy-based reasoning and cross-task generalization. In some classical methods, such as DEPS [44] and JARVIS-1 [45], ICL is mainly used to retrieve few-shots from the memory bank to assist in generating sub-task sequences for the current goal. Echo, on the other hand, treats ICL learning as an active process — it proactively retrieves potentially new tasks from the memory bank for validation and execution*

![[assets/figures/papers/paper_list_l2388_https_arxiv_org_abs_2604_05533/figures/003_Figure_3.jpg]]
*Figure 3: Overview of motivation and Problem Framework. (a) Traditional MLLM-based agents struggle to generalize across complex real-world environments due to different state transitions and causal relations (hard to transfer) and may exhibit unstable control arising from hallucinations. (b) The proposed Structured In-Context Learning framework introduces a unified CSD that decomposes environmental knowledge into five explicit transfer dimensions*



## 实验与关键发现

### 主要结果

Echo 在 Minecraft 从零学习的设定下，于多类任务上展现出对现有记忆增强代理的显著优势。Table 1 报告了不同方法在 Recipe、Functional Eq.、Crafting Chain 和 Utility Blocks 四类任务上的 Success@0→10 与 Success@0→30 指标。在 Recipe 类任务中，Echo 的 8-shot 变体在 Bed 任务上达到 92.5% 成功率，较 **JARVIS-1**（Wang et al., IEEE TPAMI 2024）的 87.5% 提升 5.0 个百分点；在 Shield 任务上达到 87.5%，较 JARVIS-1 的 80.0% 提升 7.5 个百分点。即便在 2-shot 的极低示例设定下，Echo 仍保持竞争力（Bed 任务 92.5%），表明其类比推理机制在样本稀疏时依然有效。

![[assets/figures/papers/paper_list_l2388_https_arxiv_org_abs_2604_05533/figures/007_Table_1.jpg]]
*Table 1: From-scratch learning in Minecraft (Success@0→10 / Success@0→30). Higher is better. Results are averaged over worlds, map variants, and resource configurations. v denotes full model; u denotes component disabled*

Figure 2 从物品解锁进度的角度揭示了 Echo 的核心行为特征——**爆发式解锁**（burst-like chain-unlocking）。在迭代步数达到中期阶段时，Echo 的独特物品解锁数急剧攀升，解锁速度较 **MP5**（Qin et al., CVPR 2024）、**Voyager**（Wang et al., TMLR 2024）、**JARVIS-1** 和 **MrSteve**（Park et al., ICLR 2025）等基线方法快 1.3×–1.7×。这一现象源于 ICAL 在识别到任务间的模式相似性后，能够将已掌握的知识快速泛化到相邻任务，形成连锁解锁效应。

![[assets/figures/papers/paper_list_l2388_https_arxiv_org_abs_2604_05533/figures/002_Figure_2.jpg]]
*Figure 2: Comparison of item unlocking progress across different agents. The x-axis represents the iteration steps, and the y-axis indicates the number of unique items unlocked. Our method shows a significantly faster progression, exhibiting a “rapid unlocking” phenomenon in the mid-stage, where similar items are unlocked in an explosive manner. Compared to previous methods (MP5 [38], Voyager [42], JARVIS-1 [45], and MrSteve [36]), our approach achieves equivalent milestones about 1.3×–1.7× faster*

Figure 8 的持续学习曲线进一步验证了上述机制。在 30 个训练回合的跨度内，Echo 在第 5–15 回合的快速学习阶段（图中阴影区域）成功率攀升速度明显快于所有基线，最终在第 30 回合达到约 45% 的成功率，较 JARVIS-1（约 35%）高出约 10 个百分点，较 MP5（约 43%）亦有 2 个百分点的优势。

![[assets/figures/papers/paper_list_l2388_https_arxiv_org_abs_2604_05533/figures/009_Figure_8.jpg]]
*Figure 8: Continuous learning performance comparison. The figure shows the success rate (%) over 31 training episodes (0–30) across five agents: Ours, JARVIS-1, MP5, MrSteve, and Voyager. The shaded region (episodes 5–15) highlights the fast learning phase of our method. Compared to all baselines, our method demonstrates a faster learning rate in the mid-phase*

### 消融实验

为验证五个显式迁移维度各自的贡献，作者进行了“仅保留单轴”与“移除单轴”的消融实验，Figure 7 以柱状图和相关性热力图的形式呈现了结果。各维度的失效模式与任务高度相关：

![[assets/figures/papers/paper_list_l2388_https_arxiv_org_abs_2604_05533/figures/008_Figure_7.jpg]]
*Figure 7: Comparison of task performance when keeping or removing individual design axes. Left: bar charts for each task showing median performance change under “Keep Only” and “Remove” scenarios. Right: correlation heatmap between task outcomes and design axes (thicker borders indicate stronger correlations)*

- **属性轴**（Attribute）对 Recipe 类任务至关重要，移除后成功率下降约 11%。Recipe 任务（如合成床、盾牌）要求代理精确匹配材料的颜色、纹理等属性特征，属性轴的缺失直接削弱了跨物品的材料类比能力。
- **程序轴**（Procedural）在 Crafting Chain 类任务中影响最大，移除后成功率下降约 12%。此类任务涉及多步合成链条，程序轴编码了“收集材料→使用工作台→排列材料”的步骤模式，其缺失导致代理无法有效复用已掌握的操作序列。
- **结构轴**（Structural）的移除对 Functional Eq. 和 Crafting Chain 任务分别造成约 7% 和 9% 的性能下降。结构轴描述物品的空间布局与组件关系，在需要理解物品构造或合成网格排布的场景中发挥关键作用。
- **功能轴**（Functional）几乎使 Functional Eq. 任务失效，移除后成功率下降约 9%。功能等价任务（如用不同材料制作功能相同的工具）本质上依赖功能维度的类比推理，该轴的缺失切断了“木镐→石镐”这类迁移路径。
- **交互轴**（Interaction）的移除导致 Utility Blocks 任务成功率下降约 7%。交互轴编码代理与环境中功能性方块（如工作台、熔炉）的交互方式，其缺失直接影响工具使用类任务的表现。

相关性热力图（Figure 7 右侧）进一步量化了任务结果与设计轴之间的关联强度，边界越厚表示相关性越强，与上述消融结论一致。

### 失败模式分析

尽管 Echo 在多数场景下表现优异，实验仍暴露了若干结构性局限：

1. **长链条任务中的累积误差**：在 Crafting Chain 类任务中，即便程序轴显著提升了性能，多步合成链条中的单步规划错误仍可能级联放大，导致最终合成失败。自验证模块（Verifier）虽能进行一致性自检查，但无法完全消除幻觉引起的不可靠推理。
2. **信息稀疏场景的泛化边界**：当前实验均在 Minecraft 的相对信息密集环境中进行。在需要主动探索的稀疏信息场景（如 **MP5** 所研究的设定），代理是否仍能有效构建 CSD 并进行类比推理，尚缺乏实证支持。
3. **功能等价迁移的粒度限制**：Figure 9 的个案研究展示了从木镐到石镐的成功迁移，但这种迁移依赖于功能轴的显式编码。当任务间的功能相似性较弱或需要跨域类比时（如从工具制作迁移到建筑建造），当前框架的迁移能力可能受限。
4. **持续学习中的记忆管理**：Figure 8 显示 Echo 在后期回合的成功率增长趋于平缓。随着 CSD 记忆库的持续膨胀，检索相关范例的计算开销和噪声引入风险可能增加，如何在长期运行中高效维护记忆库以避免灾难性遗忘仍是开放问题。

![[assets/figures/papers/paper_list_l2388_https_arxiv_org_abs_2604_05533/figures/010_Figure_9.jpg]]
*Figure 9: Transferring from a wooden pickaxe to a stone pickaxe*



## 定位与知识库关联

### 与现有工作的关系

Echo 在 Minecraft 开放世界代理这一研究脉络中，直接与三类代表性工作形成对比与继承关系：

**记忆增强代理的演进。** 早期工作如 **Voyager**（Wang et al., TMLR 2024）将记忆视为技能库，通过课程学习逐步解锁新能力；**JARVIS-1**（Wang et al., IEEE TPAMI 2024）进一步引入多模态记忆以支持工具使用与规划。然而，这两类方法均将记忆定位为**被动存储**——仅在当前目标需要时检索历史样本辅助子任务生成，缺乏跨任务的主动迁移机制。Echo 的核心突破在于将记忆从“被动仓库”升级为“主动迁移源”：通过上下文内类比学习（ICAL），代理主动从记忆库中检索潜在新任务并加以验证执行，而非等待当前目标触发检索。

**主动感知与信息稀疏场景。** **MP5**（Qin et al., CVPR 2024）关注信息稀疏环境下的主动感知问题，强调代理需要主动探索以获取必要信息。Echo 目前的设计侧重于将已有经验结构化迁移，而非主动探索未知环境——这构成了两者在适用场景上的互补关系。论文明确指出，在信息稀疏或需要主动探索的环境中，Echo 的表现仍需进一步验证，这为后续工作留下了明确的研究空间。

**事件记忆与指令跟随。** **MrSteve**（Park et al., ICLR 2025）构建了 What-Where-When 事件记忆以支持指令跟随，但其记忆结构未显式编码任务间的可迁移维度。Echo 的五维迁移框架（结构、属性、过程、功能、交互）为事件记忆提供了更高层次的语义组织原则，使得“制作木镐”的经验可以通过功能相似性迁移到“制作石镐”（见 Figure 9 案例）。

### 适用边界

Echo 的设计基于以下核心假设，这些假设同时界定了其适用边界：

1. **环境具有可分解的迁移维度。** 五维框架（结构、属性、过程、功能、交互）的有效性依赖于环境知识可沿这些轴进行有意义的分解。在 Minecraft 中，物品配方、制作链、工具功能等确实呈现出清晰的轴对齐特性；但在真实世界物理任务中，状态转移和因果关系的多样性可能使这种分解更加困难。

2. **经验可被语义快照压缩。** 上下文状态描述符（CSD）将多模态输入压缩为可比较的语义快照，这要求视觉、文本和交互信号之间存在足够的信息冗余以供压缩。当环境观测高度噪声或信息稀疏时，CSD 的表示质量可能下降。

3. **类比推理在上下文窗口内可行。** ICAL 依赖 MLLM 在上下文窗口中完成类比推理，受限于模型的上下文长度和推理能力。对于需要长程因果链的任务，单次上下文窗口可能不足以覆盖完整的迁移逻辑。

### 局限与开放问题

**模型幻觉与自验证的边界。** 尽管 Echo 引入了验证模块进行一致性自检查，论文明确指出自验证无法完全消除不可靠推理。在开放场景中，当检索到的范例与当前任务存在微妙但关键的差异时，模型可能产生看似合理但实际不可行的计划。这一局限在长周期规划中尤为突出——验证模块可以检查单步逻辑一致性，但难以发现跨多步的累积偏差。

**CSD 记忆库的长期维护。** 随着持续学习进行，CSD 记忆库规模不断增长。如何在保持检索效率的同时避免灾难性遗忘，论文未给出明确方案。在 Figure 8 的持续学习曲线中，Echo 在第 5–15 回合展现出快速学习阶段，但后续增长趋势是否可持续仍需更长时间跨度的验证。

**跨域迁移的泛化性。** 五维框架在 Minecraft 中的有效性已通过消融实验验证（Figure 7），但这些维度是否可直接应用于 Minecraft 以外的真实世界物理任务仍是开放问题。真实环境中的迁移可能涉及更复杂的物理约束、安全约束和社会规范，这些维度未必能被当前五轴框架充分覆盖。

**与主动探索的融合。** MP5 所研究的主动探索问题与 Echo 的经验迁移能力在理论上互补——前者解决“何时获取新信息”，后者解决“如何复用已有信息”。将两者融合，构建既能主动探索又能高效迁移的统一代理框架，是一个值得探索的方向。



## 原文 PDF

![[paperPDFs/CVPR_2026/Experience_Transfer_for_Multimodal_LLM_Agents_in_Minecraft_Game.pdf]]
