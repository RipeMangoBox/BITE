---
title: "PixelCraft: A Multi-Agent system for High-Fidelity Visual Reasoning on Structured Images"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/PixelCraft_A_Multi_Agent_system_for_High_Fidelity_Visual_Reasoning_on_Structured_Images.pdf
project_link: null
code_link: https://github.com/microsoft/PixelCraft
openreview_forum_id: HtpjSCs3g5
aliases:
- PixelCraft
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "将微调后的高精度像素级定位模型与传统计算机视觉算法相结合，并引入具有图像记忆的非线性多智能体讨论机制，可以显著提升结构化图像的推理准确性和灵活性。"
primary_logic: "将紧凑型多模态大模型微调为精准的定位模型，用于驱动工具智能体中的经典CV算子，并采用由规划器管理的图像记忆来支持分支和回溯，从而在保持上下文紧凑的同时，实现结构化图像的高保真、非线性的多智能体推理。"
claims:
- "PixelCraft在三个图表推理基准（CharXiv、ChartQAPro、EvoChart）上显著优于所有基线，在GPT-4o上分别达到55.2、58.83、70.24，相比直接回答基线提升+5.6、+6.32、+7.60。"
- "微调后的定位模型将结构化元素的整体IoU从0.26大幅提升至0.93，为下游高精度工具操作奠定了基础。"
- "消融研究表明，工具智能体（TA）的引入带来了最大的平均性能增益，视觉批评（VC）和规划批评（PC）的叠加进一步将CharXiv准确率从63.8%提升至68.1%。"
- "与线性视觉CoT相比，具备图像记忆和选择机制的PixelCraft在CharXiv上获得了3.1%的额外增益，验证了非线性推理架构的优势。"
---

# PixelCraft: A Multi-Agent system for High-Fidelity Visual Reasoning on Structured Images

> [!tip] 核心洞察
> 将紧凑型多模态大模型微调为精准的定位模型，用于驱动工具智能体中的经典CV算子，并采用由规划器管理的图像记忆来支持分支和回溯，从而在保持上下文紧凑的同时，实现结构化图像的高保真、非线性的多智能体推理。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | PixelCraft：一种面向结构化图像的高保真视觉推理多智能体系统 |
| 英文题名 | PixelCraft: A Multi-Agent system for High-Fidelity Visual Reasoning on Structured Images |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=HtpjSCs3g5) · [GitHub](https://github.com/microsoft/PixelCraft) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | PixelCraft |
| Dataset | CharXiv (GPT-4o), ChartQAPro (GPT-4o), EvoChart (GPT-4.1-mini), Geometry3K auxiliary-line subset (GPT-4.1-mini) |

> [!tip] 效果简介
> - CharXiv (GPT-4o) 上，Accuracy 为 55.2，对比 52.4 (Reconcile)，变化 +2.8。
> - ChartQAPro (GPT-4o) 上，Accuracy 为 58.83，对比 56.52 (CoT)，变化 +2.31。
> - EvoChart (GPT-4.1-mini) 上，Accuracy 为 79.44，对比 76.64 (CoT)，变化 +2.80。

## 概要

结构化图像（如科学图表、几何图形、信息图）的视觉推理面临一个关键瓶颈：现有方法依赖低精度图像处理与线性推理模式，感知错误在推理链中逐步累积，最终导致错误结论。PixelCraft 针对这一瓶颈，提出了一套多模态多智能体系统，其核心思路是将紧凑型多模态大模型（MLLM）微调为高精度像素级定位模型，用以驱动工具智能体中的经典计算机视觉（CV）算子，并引入由规划器管理的图像记忆来支持分支与回溯，从而在保持上下文紧凑的同时实现高保真、非线性的视觉推理。

在方法定位上，PixelCraft 区别于传统的思维链（CoT）和视觉 CoT 范式：前者仅进行文本推理，后者虽引入图像但采用线性历史全量保留的方式；PixelCraft 则通过规划器选择性调用历史视觉状态，实现了显式的推理分支与回溯能力（Figure 1）。系统由调度器、规划器、推理器、工具智能体以及双层批评机制（视觉批评与规划批评）构成，形成“智能体选择—讨论—迭代修正”三阶段工作流（Figure 2）。

实验结果表明，PixelCraft 在三个图表推理基准上均显著优于现有基线：在 GPT-4o 骨干下，CharXiv 准确率达 55.2%（+5.6），ChartQAPro 达 58.83%（+6.32），EvoChart 达 70.24%（+7.60）（Table 1）。消融研究进一步揭示，工具智能体的引入带来了最大的平均性能增益，而视觉批评与规划批评的叠加将 CharXiv 准确率从 63.8% 推升至 68.1%（Table 4）。微调后的定位模型将结构化元素的整体 IoU 从 0.26 提升至 0.93，为高精度工具操作奠定了感知基础（Table 6）。与线性视觉 CoT 相比，具备图像记忆和选择机制的 PixelCraft 在 CharXiv 上获得了 3.1% 的额外增益，验证了非线性推理架构的优势（Table 3）。

综上，PixelCraft 通过高保真感知与灵活推理架构的协同，在结构化图像推理任务上取得了一致且显著的性能提升。



结构化图像（如科学图表、信息图、几何示意图）是科学交流与数据分析的核心载体。从这类图像中提取精确的定量信息、进行跨子图比较或空间关系推理，要求系统同时具备高精度的感知能力与灵活的推理能力。然而，当前主流方法在这一任务上存在两个根本性瓶颈。

**瓶颈一：低精度图像处理导致感知错误累积。** 现有视觉推理方法对图像的“操作”大多停留在粗粒度层面。以视觉思维链（Visual CoT）为代表的范式，依赖多模态大模型直接生成带标注的中间图像，但其定位精度严重不足——实验表明，未经专门微调的模型在结构化图表元素上的整体IoU仅为0.26（Table 6）。低质量的中间输出在推理链中逐级传递，感知错误被不断放大，最终污染结论。Refocus等方法尝试引入视觉基元（visual primitives）作为工具，但其手工设计的有限工具集和基于基元的定位方式，同样无法达到像素级精度。

**瓶颈二：线性推理模式缺乏灵活性与纠错能力。** 现有推理框架——无论是纯文本的思维链（CoT）、多智能体辩论（Debate/Reconcile），还是视觉CoT——本质上都遵循线性推进逻辑。它们将全部历史图像顺序拼接，无法显式地执行分支探索或回溯修正。这意味着，一旦推理在某个中间步骤出现偏差，系统缺乏结构化的机制来识别错误并回到分叉点重新推理。多智能体辩论虽然引入了讨论环节，但在图表推理基准上“几乎没有带来增益”（Table 1），说明简单的文本讨论不足以弥补感知层面的缺陷。

**本文动机。** 上述分析揭示了一个清晰的因果杠杆：将高精度像素级定位能力与支持分支回溯的非线性推理架构相结合，有望同时解决感知精度和推理灵活性两大问题。PixelCraft由此提出——通过微调紧凑型多模态大模型获得高保真定位能力，并将其嵌入到由规划器（Planner）管理图像记忆的多智能体讨论框架中，使工具智能体能够调用经典计算机视觉算法执行精确的图像操作，同时双层批评机制（视觉批评与规划批评）提供实时验证与事后纠错。这一设计实现了从“粗粒度线性推理”到“高保真非线性推理”的范式转变（Figure 1）。



## 核心方法与创新机理

结构化图像的视觉推理长期受困于一个关键瓶颈：现有方法依赖低精度图像处理与线性推理模式，导致感知错误在推理链中逐步累积，最终影响结论的可靠性。PixelCraft 针对这一瓶颈，在两个核心维度上实现了根本性的创新突破。

### 从低精度定位到高保真像素级感知

传统方法（如 **Refocus**）采用基于视觉基元的粗粒度定位，难以精确捕捉图表中微小元素的边界，导致下游操作（如裁剪、掩码）产生累积误差。PixelCraft 的核心创新在于将**微调后的紧凑型多模态大模型**与**经典计算机视觉算法**深度融合，构建了高精度的像素级感知能力。

具体而言，PixelCraft 构建了一个高质量的合成数据集，包含图表与几何图形，用于微调 Qwen2.5-VL-3B 模型，使其成为专用的定位模型。该模型以自回归方式生成序列 $Y = ( y _ { 1 } , \dots , y _ { T } )$，同时编码文本答案与对应的边界框坐标。实验证据（Table 6, Section D.3）表明，这一微调将结构化元素的整体 IoU 从 0.26 大幅提升至 0.93，子图区域的 IoU 更是从 0.52 跃升至 0.99。这一高精度定位能力被注入到**工具智能体（Tool Agents）**中，驱动裁剪、放大、添加辅助线、按图例掩码等经典 CV 算子，从而在图像处理层面消除了感知误差的根源。

### 从线性推理到非线性多智能体协作

现有方法（如视觉 Chain-of-Thought）采用线性推理范式，顺序生成中间图像并全量保留历史状态，缺乏对错误分支的回溯能力。PixelCraft 引入了**由规划器管理的图像记忆（Planner-managed Image Memory）**，实现了非线性推理架构。

该架构的核心机制是：规划器将所有中间视觉输出存入图像记忆，并可根据需要**选择性召回**任意历史状态，从而支持显式的推理分支与回溯。与线性视觉 CoT 相比，这一设计在 CharXiv 上带来了 3.1% 的额外增益（Table 3, Section 5.3），验证了非线性推理在结构化图像任务中的优势。

在此基础上，PixelCraft 构建了**双层批评机制**以进一步强化推理质量：

- **视觉批评（Visual Critic）**：在推理循环内实时验证工具智能体的输出是否满足目标，以及当前图像是否足以回答问题，形成即时纠错闭环。
- **规划批评（Planning Critic）**：在推理完成后进行事后审查，评估整个推理过程的逻辑正确性与效率，并提供工具列表调整建议，触发重新推理。

消融研究（Table 4, Section 5.3）揭示了各组件的贡献层级：工具智能体的引入带来了最大的平均性能增益，将 CharXiv 准确率从 63.8% 提升至 65.0%；视觉批评的叠加进一步推高至 66.0%；规划批评的加入最终使完整系统达到 68.1%。这一递进式增益结构表明，高保真感知与非线性推理并非孤立创新，而是通过多智能体协作形成了相互增强的有机整体。

### 工具生成的半自动化范式

与手工设计有限工具集的传统做法不同，PixelCraft 采用**半自动化的工具生成流程**（Section 3.1, Appendix B）：由 LLM 生成候选工具，经专家验证与微调后集成经典 CV 算法。聚类分析（Table 5）显示，生成的工具自然收敛为五类核心操作——添加辅助线、子图裁剪、按图例掩码、区域放大、数据点定位——覆盖了结构化图像推理的主要需求。这一范式在保持工具可靠性的同时，显著扩展了工具集的覆盖范围与灵活性。



![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_HtpjSCs3g5/figures/002_Figure_2.jpg]]
*Figure 2: An illustration of the PixelCraft workflow. The process begins with Agent Selection, where the dispatcher chooses the appropriate tools. Next, during Agent Discussion, the planner coordinates tool agents to process the image (e.g., cropping and masking) and the reasoner to perform analysis, with the visual critic providing real-time validation. Finally, the planning critic performs a post-hoc review of the entire process, confirming its correctness*

PixelCraft 是一个面向结构化图像的多模态多智能体系统，其核心目标是通过高保真图像处理与灵活的非线性推理，解决现有方法中因低精度感知与线性推理链导致的错误累积问题。系统围绕一个由规划器（Planner）管理的**图像记忆（Image Memory）** 构建，将推理过程组织为三个协同阶段：查询感知的智能体选择、角色驱动的智能体讨论，以及迭代修正与自我纠正。

### 系统架构与模块关系

PixelCraft 由以下功能模块构成，各模块均由多模态大模型（MLLM）实例化，并与专门化的工具智能体协作：

- **调度器（Dispatcher）**：根据输入查询的语义需求，从工具库中动态选择一个相关工具智能体子集，避免无关工具引入噪声。
- **规划器（Planner）**：作为推理流程的核心协调者，负责将主查询分解为可管理的子查询，编排智能体的激活顺序，管理所有智能体间的通信，并维护图像记忆以支持非线性推理。
- **推理器（Reasoner）**：对当前图像状态和子问题进行逻辑分析，给出中间结论或最终答案。
- **工具智能体（Tool Agents）**：执行高精度图像处理操作（如裁剪子图、放大区域、按图例屏蔽元素、添加辅助线等），由微调后的紧凑型定位模型驱动经典计算机视觉（CV）算子，实现像素级精准编辑。
- **视觉批评（Visual Critic）**：在推理循环内实时验证工具智能体的输出是否满足当前目标，并判断当前图像状态是否足以回答问题。
- **规划批评（Planning Critic）**：在推理过程结束后进行事后审查，评估整个推理链的逻辑正确性与效率，提出工具列表修正建议（如增删工具）以触发重新推理。

### 三阶段工作流程

系统的工作流按以下三个阶段展开（参见 Figure 2）：

**阶段一：查询感知的智能体选择。** 调度器分析用户查询，从预定义的工具库中筛选出与任务相关的工具智能体，与推理器一同构成当前推理会话的参与智能体集合。

**阶段二：角色驱动的智能体讨论。** 规划器将主查询分解为子查询序列，并协调工具智能体与推理器的交替执行。工具智能体接收规划器的指令，调用微调定位模型输出精确坐标，再由经典CV算法完成图像编辑；推理器则基于更新后的图像状态进行分析。视觉批评在此阶段持续介入，对每一步工具输出进行目标满足度与可回答性验证，形成闭环反馈。规划器通过图像记忆存储所有中间视觉输出，并可选择性地回溯任意历史图像状态，从而支持显式的推理分支与回溯，保持上下文紧凑的同时实现非线性推理。

**阶段三：迭代修正与自我纠正。** 规划批评对整个推理过程进行事后审查，识别逻辑漏洞或低效步骤，并向规划器提供改进建议。规划器据此调整工具选择或推理路径，触发新一轮的智能体讨论，直至规划批评确认推理正确或达到预设迭代上限。

### 输入输出流

系统的输入为一张结构化图像（如科学图表、几何图形、信息图）和一个自然语言查询。输出为最终答案文本。内部数据流的关键特征在于：图像状态在工具智能体处理后被更新并存入图像记忆，规划器在每一步决策时从记忆中选取最相关的历史图像作为推理器的输入，而非简单地将所有中间图像线性拼接。这种设计使得系统能够在需要时“回退”到先前的视觉状态，探索替代推理路径，从而突破线性视觉思维链（Visual CoT）的固有局限。



### 系统架构概览

PixelCraft 是一个面向结构化图像的多模态多智能体系统，其核心由六个功能模块构成：**Dispatcher（调度器）**、**Planner（规划器）**、**Reasoner（推理器）**、**Tool Agents（工具智能体）**、**Visual Critic（视觉批评）** 和 **Planning Critic（规划批评）**。这些模块通过一个三阶段工作流协同运作：查询感知的智能体选择、角色驱动的智能体讨论、以及迭代修正与自我纠正。

### 关键模块功能

**Planner 与图像记忆** 是系统非线性推理能力的核心载体。Planner 负责将主查询分解为可管理的子查询，编排智能体的激活顺序，并协调所有智能体间的通信。其关键创新在于维护一个**图像记忆（image memory）**，存储所有中间视觉输出。这使得 Planner 能够自适应地回溯任意历史图像状态，支持显式的推理分支与回溯，同时保持上下文紧凑——这与线性视觉 CoT 将全部图像顺序流式传输的方式形成根本区别。

**Tool Agents** 是实现高保真图像处理的关键执行单元。每个工具智能体内部集成了一个**微调后的定位模型**（基于 Qwen2.5-VL-3B）和**经典计算机视觉算法**。定位模型提供像素级精度的结构化元素坐标，驱动 CV 算子执行裁剪、放大、添加辅助线、按图例遮罩等操作。消融实验表明，工具智能体的引入带来了最大的平均性能增益（Table 4），而定位模型的微调将整体 IoU 从 0.26 提升至 0.93（Table 6），为下游操作奠定了基础。

**双层批评机制** 提供闭环验证能力。Visual Critic 在循环内实时验证工具智能体的输出是否满足目标，以及当前图像是否足以回答问题；Planning Critic 则在事后审查整个推理过程的逻辑正确性与效率，提出工具列表的修正建议（如增删工具）并触发重新推理。消融实验显示，移除 Visual Critic 后 CharXiv 准确率从 68.1% 降至 66.0%，移除 Planning Critic 后进一步降至 67.5%（Table 4），验证了双层批评的叠加贡献。

### 核心公式

定位模型采用自回归生成范式，其输出序列联合编码了文本答案与对应的边界框坐标：

$$Y = (y_1, \dots, y_T)$$

其中 $Y$ 表示模型生成的自回归序列，$T$ 为序列长度，每个 $y_t$ 为离散 token。该序列同时包含自然语言推理文本和结构化的坐标信息，使得单一模型能够端到端地完成“理解问题—定位元素—输出坐标”的完整流程。微调后的模型在结构化图表元素上的定位精度达到 0.93 IoU，远优于通用大模型的 0.26 IoU（Table 6），为工具智能体中的 CV 算子提供了可靠的坐标输入。



## 实验与关键发现

### 主要结果

PixelCraft在三个结构化图像推理基准上均取得了一致的领先性能，验证了高保真图像处理与非线性多智能体推理的有效性。在**CharXiv**基准上，基于GPT-4o的PixelCraft达到55.2%准确率，相比最强基线Reconcile（52.4%）提升2.8个百分点；在**ChartQAPro**上达到58.83%，超越CoT基线（56.52%）2.31个百分点；在**EvoChart**上达到70.24%，相比直接回答基线提升7.60个百分点（Table 1）。值得注意的是，单纯的多智能体辩论方法（Debate、Reconcile）在图表推理任务上收益极为有限，这表明缺乏高保真感知能力的讨论机制难以纠正底层的感知错误。


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_HtpjSCs3g5/figures/003_Table_1.jpg]]
*Table 1: Performance comparison across different models and evaluation methods*

在几何推理任务上，PixelCraft的优势更为突出。在**Geometry3K辅助线子集**上，基于GPT-4.1-mini的PixelCraft达到34.38%，相比直接回答基线（24.22%）提升超过10个百分点（Table 2）。该子集要求模型精确捕捉点线关系并添加辅助线，正是PixelCraft像素级定位与经典CV算子（如线条交点检测）的核心优势场景。

泛化能力方面，在真实信息图**InfographicVQA**的结构化推理子集上，PixelCraft分别以GPT-4.1-mini（79.8%）和GPT-4o（71.6%）均超越所有基线（Table 9），证明该方法不仅适用于合成图表，也能有效处理真实世界的复杂信息图。


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_HtpjSCs3g5/figures/048_Table_9.jpg]]
*Table 9: Performance comparison on the structured reasoning subset of InfographicVQA. PixelCraft consistently outperforms baselines, demonstrating strong generalization to real-world infographics*

### 消融实验

#### 视觉CoT vs. PixelCraft框架

为验证非线性推理架构的独立贡献，论文将PixelCraft与线性视觉CoT范式进行了直接对比（Table 3）。在CharXiv上，具备图像记忆和选择机制的PixelCraft达到68.1%，相比视觉CoT的65.0%获得3.1个百分点的额外增益；在ChartQAPro上，差距为4.52个百分点（65.56% vs. 61.04%）。这一结果表明，图像记忆支持的分支与回溯能力是实现灵活视觉推理的关键，而非仅仅是视觉工具的叠加。


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_HtpjSCs3g5/figures/005_Table_3.jpg]]

#### 组件逐层消融

Table 4展示了以GPT-4.1-mini为骨干模型时，各组件逐步叠加的性能变化：

- **基础推理器**（无工具）：CharXiv 63.8%，ChartQAPro 62.21%
- **+工具智能体（TA）**：CharXiv提升至65.0%（+1.2），ChartQAPro提升至62.72%（+0.51）。TA的引入带来了最大的平均性能增益，证实高保真图像处理是瓶颈突破的核心。
- **+调度器（Disp）**：CharXiv进一步升至66.9%（+1.9），说明查询感知的工具选择有效减少了无关工具的干扰。
- **+视觉批评（VC）**：CharXiv升至68.0%（+1.1），循环内实时验证机制带来了正向贡献。
- **+规划批评（PC）**：最终CharXiv达到68.1%，ChartQAPro达到65.56%。PC的叠加增益虽相对较小（CharXiv +0.1），但其价值体现在事后逻辑审查和触发重新推理的能力上。

完整消融表明，TA是性能提升的最大驱动力，VC和PC的叠加进一步巩固了推理的可靠性，三者的协同构成了PixelCraft的核心优势。

#### 定位精度消融

定位模型的精度是工具智能体高保真操作的前提。Table 6的量化对比显示，微调后的3B模型在结构化图表元素定位上实现了质的飞跃：


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_HtpjSCs3g5/figures/033_Table_6.jpg]]
*Table 6: Grounding accuracy on structured chart elements. IoU columns evaluate bounding-box overlap for subplots, legend regions, and textual labels (titles and axis labels). PCK@0.01 measures point localization accuracy for axis tick marks using a threshold of 0.01 × max(height, width)*

- **整体IoU**：从Qwen2.5-VL-7B的0.26飙升至0.93
- **子图区域IoU**：达到0.99（基线最佳为0.78）
- **图例区域IoU**：0.83（基线最佳为0.24）
- **文本标签IoU**：0.95（基线最佳为0.52）
- **刻度标记定位PCK@0.01**：0.99（基线最佳为0.36）

这一结果表明，通用MLLM的定位能力在结构化图像上严重不足，而针对性的微调是解锁高精度工具操作的关键。

### 工具使用分析

Figure 4统计了各工具在CharXiv和Geometry3K上的使用频率与性能增益。高频使用的工具包括子图裁剪、区域放大和图例掩码，这些工具激活的查询子集上均观察到显著的正向性能增益。Figure 6右侧展示了经典CV算法检测图表线条交点的典型案例，验证了将传统CV算子集成到工具智能体中的可行性。


![[assets/figures/papers/paper_list_l13_https_openreview_net_forum_id_HtpjSCs3g5/figures/012_Figure_4.jpg]]
*Figure 4: Effectiveness and prevalence of tool usage with GPT-4.1-mini on CharXiv (Wang et al., 2024) and Geometry3K (Lu et al., 2021). The performance gain is calculated specifically on the subset of queries where each tool was activated*

### 批评机制有效性

Figure 5分析了视觉批评和规划批评的错误识别能力。批评机制能够有效标记出包含感知错误或逻辑缺陷的推理案例（真阳性），并通过迭代修正显著提升这些案例的最终准确率。同时，也存在少量误报（假阳性），表明批评机制仍有优化空间。

### 计算成本与公平性

Table 7的计算成本分析表明，PixelCraft相比视觉工具和多智能体基线有更高的延迟和API调用次数，但Table 8的同等计算量对比显示，PixelCraft在匹配Self-Refine基线的测试时计算量下仍保持性能优势，验证了性能增益源于架构设计而非单纯的计算量增加。

### 失败模式与局限

尽管整体性能显著提升，PixelCraft仍存在以下局限：

1. **骨干模型依赖性**：系统性能高度依赖强大的骨干MLLM进行任务分解与工具编排。当使用较弱模型时，规划错误或工具调用失败可能导致推理链断裂。
2. **工具生成的半自动化**：当前工具创建仍需人工验证和精细化，LLM生成的候选工具并非完全可靠，限制了系统的全自动化部署能力。
3. **批评机制的误判**：Figure 5显示批评机制存在一定比例的假阳性，可能触发不必要的重新推理，增加计算开销。
4. **领域泛化边界**：虽然InfographicVQA上的结果展现了泛化潜力，但工具集的设计仍主要面向图表和几何图形，向更广泛结构化图像类型的迁移需要额外验证。


## 定位与知识库关联

### 1. 与基线方法的关系

PixelCraft 在结构化图像推理领域与多类基线方法形成对比，其核心差异体现在图像处理精度、推理范式和错误纠正机制三个维度。

**直接回答与思维链基线**：最朴素的 **Direct answer** 和 **Chain of Thought (CoT)** 基线仅依赖文本推理，缺乏对图像像素级信息的精确操作能力。实证表明，在 CharXiv 基准上，CoT 在 GPT-4o 下仅达 49.6%，而 PixelCraft 达到 55.2%（Table 1），差距源于前者无法对图表元素进行高保真裁剪、放大和辅助线标注等操作。

**多智能体协作基线**：**Debate** 和 **Reconcile** 两类多智能体讨论方法在图表推理上收益有限（Table 1）。这类方法虽然引入了多视角讨论，但本质上仍停留在文本推理层面，缺乏对图像本身的精确操控能力。PixelCraft 通过引入工具智能体（TA）将讨论从纯文本空间拓展到视觉操作空间，消融实验显示 TA 的引入带来了最大的平均性能增益，CharXiv 准确率从 63.8% 提升至 65.0%（Table 4）。

**视觉工具使用方法**：**Refocus** 代表了基于视觉基元的图表工具使用范式，但其定位精度受限于视觉基元方法，结构化元素的整体 IoU 仅为 0.26（Table 6）。PixelCraft 通过微调 Qwen2.5-VL-3B 构建高精度定位模型，将 IoU 大幅提升至 0.93，为下游 CV 算子提供了可靠的坐标基础。这一改进是工具智能体能够执行精确裁剪、放大等操作的前提。

**视觉 CoT 范式**：线性视觉 CoT 将历史图像全量保留在上下文中，不支持推理分支和回溯。PixelCraft 引入规划器管理的图像记忆，支持选择性召回历史视觉状态，在 CharXiv 上相比视觉 CoT 获得 3.1% 的额外增益（68.1% vs 65.0%，Table 3），验证了非线性推理架构在结构化图像任务上的优势。

### 2. 适用边界

PixelCraft 的设计假设与适用场景具有明确的边界条件：

**强依赖结构化图像场景**：系统的工具集（裁剪子图、区域放大、按图例屏蔽、添加辅助线）和定位模型均针对图表和几何图形设计。在 CharXiv、ChartQAPro、EvoChart 三个图表推理基准以及 Geometry3K 辅助线子集上取得了显著增益，在 InfographicVQA 结构化推理子集上也展现出泛化能力（79.8% vs CoT 的 77.3%，Table 9）。但该方法在自然图像场景下的有效性尚未得到验证。

**强骨干模型依赖**：PixelCraft 的性能高度依赖底层 MLLM 的任务分解与工具编排能力。实验在 GPT-4o、GPT-4.1-mini 和 Claude-3.7-sonnet 三个强模型上展开（Table 1），但论文明确指出较弱模型可能导致规划错误或工具调用失败。这一依赖限制了系统在资源受限场景下的部署可行性。

**工具集半自动化限制**：当前工具创建流程为“LLM 生成候选 + 专家验证与微调”，尚未实现完全自动化。工具聚类分析显示共生成 5 个主要工具簇（Table 5），但这些工具仍需人工精细化验证，限制了系统在新领域快速部署的能力。

### 3. 局限与开放问题

**工具生成的自动化瓶颈**：当前多模态大模型无法自主生成可靠的高保真视觉工具。工具创建需要人工验证和精细化，这是限制 PixelCraft 全自动化部署的核心障碍。如何实现完全自动化的高保真视觉工具生成与验证，是首要开放问题。

**骨干模型鲁棒性不足**：系统性能对特定强大骨干模型存在强依赖。消融实验中的性能增益均建立在 GPT-4.1-mini 基础上（Table 4），论文未验证在较弱模型上的表现。设计更鲁棒的智能体通信协议或轻量化专用模型以降低依赖，是重要的工程方向。

**推理范式的泛化边界**：图像记忆与非线性推理架构在结构化图像上展现了优势，但其能否推广到更通用的多模态推理任务（如机器人视觉、交互式环境理解）仍待探索。当前实验覆盖的任务类型（图表、几何、信息图）均属于静态结构化视觉场景，动态场景下的适用性缺乏证据。

**计算成本与效率权衡**：PixelCraft 的多智能体讨论和迭代修正机制增加了计算开销（Table 7 提供了延迟与 API 调用次数分析）。虽然与 Self-Refine 基线在同等计算量下的对比表明性能增益源于架构设计而非简单增加测试时计算（Table 8），但在实际部署中仍需权衡精度提升与推理成本。



## 原文 PDF

![[paperPDFs/ICLR_2026/PixelCraft_A_Multi_Agent_system_for_High_Fidelity_Visual_Reasoning_on_Structured_Images.pdf]]
