---
title: "PlanAgent: A Multi-modal Large Language Agent for Closed-loop Vehicle Motion Planning"
type: paper
paper_level: A
venue: arXiv
year: 2024
pdf_ref: paperPDFs/arxiv_2024/PlanAgent_A_Multi_modal_Large_Language_Agent_for_Closed_loop_Vehicle_Motion_Planning.pdf
aliases:
- PlanAgent
tags:
- arxiv_2024
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 引入多模态大语言模型（MLLM）作为认知智能体，通过分层思维链（CoT）结合环境变换与反思模块，使MLLM能够在闭环规划中进行常识推理并生成安全的规划器。
primary_logic: 利用MLLM的常识推理能力，通过BEV图像和车道图文本描述高效编码场景，设计从场景理解到运动指令再到代码生成的分层思维链，辅以模拟反思机制，显著提升闭环运动规划在常见和长尾场景下的性能与泛化能力。
claims:
- PlanAgent在nuPlan Val14和Test14-hard基准上达到SOTA，NR-CLS和R-CLS均显著优于规则基方法PDM-Closed和学习基方法PlanTF、DTPP。
- PlanAgent是首个基于MLLM的中到中闭环规划系统，通过多模态场景编码和分层CoT实现规划。
- 环境变换模块的BEV地图与车道图文本描述使场景编码token数降低至其他LLM方法的约三分之一（平均141.32 tokens）。
- 消融实验证实分层CoT中的场景理解、运动指令以及Reflection模块分别对NR-CLS贡献2.42、1.91和2.67。
---

# PlanAgent: A Multi-modal Large Language Agent for Closed-loop Vehicle Motion Planning

> [!tip] 核心洞察
> 利用MLLM的常识推理能力，通过BEV图像和车道图文本描述高效编码场景，设计从场景理解到运动指令再到代码生成的分层思维链，辅以模拟反思机制，显著提升闭环运动规划在常见和长尾场景下的性能与泛化能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | PlanAgent：面向闭环车辆运动规划的多模态大语言模型智能体 |
| 英文题名 | PlanAgent: A Multi-modal Large Language Agent for Closed-loop Vehicle Motion Planning |
| 会议/期刊 | arXiv 2024 |
| Links | [paper](https://arxiv.org/abs/2406.01587) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | PlanAgent |
| Dataset | nuPlan Val14, nuPlan Test14-hard, Token Efficiency |

> [!tip] 效果简介
> - nuPlan Val14 (non-reactive closed-loop) 上，NR-CLS 93.26 vs 92.51 (PDM-Closed) (+0.75)。
> - nuPlan Val14 (reactive closed-loop) 上，R-CLS 92.75 vs 91.79 (PDM-Closed) (+0.96)。
> - nuPlan Test14-hard (non-reactive closed-loop) 上，NR-CLS 72.51 vs 65.07 (PDM-Closed) (+7.44)。

## 概述

现有车辆运动规划方法在闭环长尾场景下面临瓶颈：规则基方法（如 **PDM-Closed**，Dauner et al., CoRL 2023）依赖人工定义参数与搜索策略，泛化能力有限；学习基方法（如 **PlanTF**，Cheng et al., ICRA 2024；**DTPP**，Huang et al., ICRA 2024）直接从数据预测轨迹或代价，但在分布外场景中鲁棒性不足；近期基于大语言模型（LLM）的规划器（如 **GPT-Driver**、**Agent-Driver**、**DiLu**）虽引入常识推理，却普遍采用文本化场景描述，导致 token 消耗高、空间理解弱，且缺乏闭环安全验证机制。如何高效编码场景并利用常识推理实现安全、可泛化的闭环规划，是该领域的核心瓶颈。

PlanAgent 的核心洞察在于：将多模态大语言模型（MLLM）作为认知智能体，通过 BEV 图像与车道图文本描述高效编码场景，并设计从场景理解到运动指令再到代码生成的分层思维链（Hierarchical Chain-of-Thought），辅以仿真反思模块进行安全验证，从而在闭环规划中兼顾常识推理与泛化能力。具体而言，PlanAgent 包含三个核心模块——Environment Transformation 将感知数据转化为 BEV 地图与基于车道图的文本描述，使场景编码 token 数降至其他 LLM 方法的约三分之一（平均 141.32 tokens）；Reasoning Engine 利用 MLLM 执行分层思维链，逐步完成场景理解、纵/横向运动指令生成与 IDM 规划器代码输出；Reflection Module 对生成的规划器进行仿真评估，评分低于阈值则触发重新思考，以降低 MLLM 不确定性带来的安全风险。

在 nuPlan Val14 和 Test14-hard 基准上，PlanAgent 取得闭环运动规划 SOTA：Val14 上 NR-CLS 达 93.26（较 PDM-Closed 提升 +0.75），R-CLS 达 92.75（+0.96）；在更具挑战性的 Test14-hard 上，NR-CLS 达 72.51（较 PDM-Closed 提升 +7.44），R-CLS 达 76.82（+1.64）。消融实验证实，分层思维链中的场景理解、运动指令以及 Reflection 模块分别对 NR-CLS 贡献 2.42、1.91 和 2.67，验证了各模块设计的有效性。该方法首次将 MLLM 引入中到中闭环规划系统，为自动驾驶中常识驱动的高效场景编码与安全规划提供了新范式。

## 背景与动机

自动驾驶运动规划的核心挑战在于，车辆必须在动态、交互且充满长尾场景的开放环境中生成安全、合理的行驶轨迹。现有的规划方法大致可分为三类，但各自存在明显的能力边界。

**规则基方法**，如 **PDM-Closed**（Dauner et al., CoRL 2023），依赖人工设计的智能驾驶员模型（IDM）参数搜索与代价评估，在常见场景下表现稳健，但在长尾场景中泛化能力严重不足——其性能高度受限于人工规则的完备性，无法应对规则未覆盖的复杂交互。

**学习基方法**，如 **PlanTF**（Cheng et al., ICRA 2024）和 **DTPP**（Huang et al., ICRA 2024），通过模仿学习或联合预测-规划从数据中学习驾驶策略，试图突破规则的天花板。然而，这类方法在闭环泛化上存在瓶颈：它们在常见场景中往往不如精心调优的规则基方法，而在更具挑战性的长尾场景中，由于训练数据覆盖不足，性能同样急剧下降。这种“两头不靠”的困境，根源于纯数据驱动方法缺乏对场景语义和物理常识的真正理解。

**大语言模型（LLM）基方法**为上述困局提供了新的可能。LLM具备强大的常识推理能力，能够在缺乏专门训练数据的情况下理解场景语义并做出合理决策。然而，现有LLM基规划方法仍面临三个关键缺口：

1. **闭环规划能力缺失**：如 **GPT-Driver**（Mao et al., arXiv 2023）和 **Agent-Driver**（Mao et al., arXiv 2023）仅在开环设定下生成航点，无法应对闭环仿真中的误差累积与动态交互；**DiLu**（Wen et al., ICLR 2024）虽在简化环境（highway-env）中实现了闭环，但未在真实级自动驾驶基准上验证。

2. **场景编码效率低下**：现有LLM方法通常将所有智能体的数值坐标或全量信息转换为文本描述，导致token消耗巨大——**GPT-Driver**平均每个场景需709.34 tokens，**LLM-ASSIST**（Sharan et al., arXiv 2023）需441.41 tokens。这不仅增加了推理成本，更因上下文窗口限制而难以处理复杂场景。

3. **安全验证机制薄弱**：LLM的生成具有固有的不确定性，直接将其输出用于车辆控制存在安全隐患。现有方法或缺乏安全验证，或仅依赖简单的后优化，无法在闭环中有效降低MLLM不确定性带来的风险。

综上，核心瓶颈在于：**缺乏一个能够将MLLM的常识推理能力高效注入闭环运动规划的系统框架，该框架需同时解决场景表示效率、推理层次化以及安全验证三大问题。** PlanAgent正是针对这一瓶颈，首次提出了基于MLLM的中到中闭环规划智能体系统。

## 核心创新

PlanAgent 的核心创新在于将多模态大语言模型（MLLM）引入中到中闭环运动规划，通过**场景表示-分层推理-安全验证**三位一体的设计，系统性解决了现有方法在长尾场景泛化和常识推理上的瓶颈。相对于规则基、学习基和已有的 LLM 基方法，PlanAgent 在以下四个关键维度上实现了根本性改变。

### 1. 场景编码：从冗余文本到多模态高效表示

现有 LLM 基方法（如 **GPT-Driver**，Mao et al., arXiv 2023；**LLM-ASSIST**，Sharan et al., arXiv 2023）普遍采用全量智能体信息的文本描述作为场景输入，导致 token 消耗巨大（GPT-Driver 平均 709.34 tokens，LLM-ASSIST 平均 441.41 tokens），且丢失了空间拓扑结构。PlanAgent 的**环境变换模块**将场景编码重构为双通道表示：**BEV 地图**提供全局语义信息（以不同颜色可视化八种道路元素，红色箭头标注智能体运动方向和速度），**车道图文本描述**则仅保留自车周围 8 个节点的拓扑连接与智能体状态信息。这一设计使平均 token 数降至 141.32，约为 GPT-Driver 的三分之一（Table III），同时保留了关键的空间结构信息。消融实验证实，同时使用 BEV 地图与车道图文本描述可获得最高的 NR-CLS 和 R-CLS（Table IV），验证了多模态编码的互补性。

### 2. 推理机制：从直接输出到分层思维链

已有 LLM 方法通常采用单一提示直接生成航点或控制器参数，缺乏对场景的深层理解。PlanAgent 设计了**分层思维链**，将推理过程分解为三个递进阶段：**场景理解**（通过全局与局部提问引导 MLLM 分析交通态势）→ **运动指令生成**（给出纵向与横向的驾驶建议及理由）→ **规划器代码生成**（输出基于 IDM 的具体规划器代码）。这一分层设计使 MLLM 能够在每个阶段聚焦特定子任务，而非一次性处理全部复杂度。消融实验表明，去除场景理解导致 NR-CLS 下降 2.42，去除中层级运动指令导致下降 1.91（Table V），证实了分层推理每一步的独立贡献。

### 3. 安全机制：从无验证到反思闭环

大多数 LLM 基规划方法缺乏对生成结果的安全验证，MLLM 输出的不确定性可能直接导致危险行为。PlanAgent 引入**反思模块**，对生成的规划器进行仿真评估：若评分 $s \geq \lambda$（阈值），则接受并执行；否则触发重新思考，重新生成规划器，最多执行 $\text{max\_exe}$ 次。这一机制将开环的文本生成转变为闭环的安全验证，有效降低了 MLLM 幻觉带来的风险。去除反思模块会导致 NR-CLS 下降 2.67（Table V），是三个模块中贡献最大的单一组件，凸显了安全验证在 MLLM 规划中的关键作用。

### 4. 规划范式：从规则/学习到常识驱动的代码生成

规则基方法（如 **PDM-Closed**，Dauner et al., CoRL 2023）依赖人工定义的 IDM 参数搜索，在长尾场景中泛化能力受限；学习基方法（如 **PlanTF**，Cheng et al., ICRA 2024；**DTPP**，Huang et al., ICRA 2024）则受限于训练数据分布。PlanAgent 通过 MLLM 的常识推理能力，在理解场景语义后动态生成 IDM 规划器代码，而非直接输出数值轨迹。这一范式转换使系统在 Test14-hard 长尾基准上的 NR-CLS 达到 72.51，较 PDM-Closed 提升 7.44 个百分点（Table II），证明了常识推理在复杂场景中的独特价值。

### 创新总结

PlanAgent 的四项 changed slots 构成了一个完整的创新闭环：**高效场景编码**降低了 MLLM 的输入负担，**分层思维链**引导了结构化的常识推理，**反思模块**提供了安全兜底，**代码生成范式**则赋予了规划器在长尾场景中的适应能力。这一设计使 PlanAgent 成为首个在闭环中到中规划中同时实现 SOTA 性能和强泛化能力的 MLLM 智能体系统。

## 整体框架

PlanAgent 是首个基于多模态大语言模型（MLLM）的中到中闭环运动规划系统，其整体架构由三个核心模块串联而成：**环境变换模块（Environment Transformation）**、**推理引擎模块（Reasoning Engine）** 和 **反思模块（Reflection Module）**。三个模块形成闭环反馈流：环境变换模块将感知数据转化为多模态场景提示，推理引擎据此通过分层思维链生成规划器代码，反思模块对生成的规划器进行仿真验证并决定是否触发重新推理。

**输入输出流。** 系统输入为自动驾驶环境中的感知信息，包括道路元素（车道线、交叉口等）和周围智能体状态。输出为可直接执行的 IDM 规划器代码，该规划器实时计算自车的纵向加速度与横向控制指令，驱动车辆完成闭环运动规划。

**模块间关系。** 环境变换模块从原始感知数据中提取关键信息，构建 BEV 地图作为全局语义表示，同时基于车道图生成文本描述作为局部场景提示。这两类多模态提示共同输入推理引擎。推理引擎在预定义的系统提示（任务定义提示、常识提示、思维链引导提示）指导下，利用 MLLM 进行多轮分层推理，依次完成场景理解、运动指令生成和规划器代码生成。生成的规划器进入反思模块，在仿真器中运行并计算评分——若评分不低于预设阈值 λ，则接受并执行该规划器；否则触发重新思考，最多执行 max_exe 次迭代，以降低 MLLM 输出不确定性带来的安全风险。

**核心设计动机。** 现有规则基方法（如 **PDM-Closed**，Dauner et al., CoRL 2023）在长尾场景中泛化能力不足，学习基方法（如 **PlanTF**，Cheng et al., ICRA 2024）缺乏常识推理能力，而早期 LLM 基方法（如 **GPT-Driver**、**Agent-Driver**，Mao et al., arXiv 2023）仅适用于开环设定且场景编码 token 开销巨大。PlanAgent 通过上述三模块设计，首次将 MLLM 的常识推理能力引入闭环规划，同时以 BEV 地图与车道图文本描述的组合将场景编码 token 数降至其他 LLM 方法的约三分之一（平均 141.32 tokens），在 nuPlan Val14 和 Test14-hard 基准上均取得 SOTA 性能。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2406_01587/figures/003_Figure_2.jpg]]
*Figure 2: Based on a MLLM, we propose a novel planning agent pipeline comprising three modules: Environment Transformation, Reasoning Engine, and Reflection Module. In the Environment Transformation module, key information about the environment is extracted to form a BEV map and construct a lane-graph representation. Subsequently, the lane graph is translated into textual descriptions and used as scenario prompts along with the BEV map. In the Reasoning Engine module, an MLLM generates planner codes based on the IDM [16] planner through hierarchical chain-of-thought reasoning with scenario prompts and pre-defined system prompts (including task definition prompts, common sense prompts, and chain-of-th...*

## 核心模块与公式推导

PlanAgent 的整体架构由三个核心模块串联构成：**环境变换**、**推理引擎**与**反思模块**（Fig. 2）。三个模块协同完成“多模态场景编码→分层常识推理→安全闭环验证”的闭环规划流程。

### 环境变换模块

该模块负责将原始感知数据高效压缩为 MLLM 可理解的多模态场景提示，核心设计目标是**在保留关键语义的前提下最小化 token 开销**。

**BEV 地图构建**：将八类道路元素（车道线、人行横道、路沿等）以不同颜色渲染为俯视语义图，同时用红色箭头标注周围智能体的运动方向与速度（箭头长度编码速度大小）。BEV 地图作为全局语义信息直接以图像形式输入 MLLM。

**车道图文本描述**：基于车道中心线构建有向图，每个节点代表一段中心线片段。仅保留自车所在节点及其周围 8 个邻接节点的拓扑关系与智能体占用状态，将其转换为结构化文本（Fig. 3）。这一设计使场景文本描述的平均 token 数降至 **141.32**，仅为 GPT-Driver（709.34 tokens）的约五分之一、LLM-ASSIST（441.41 tokens）的约三分之一（Table III），大幅降低了 MLLM 推理的上下文长度负担。

### 推理引擎模块

推理引擎接收环境变换模块输出的场景提示（BEV 图像 + 车道图文本）和预定义的系统提示，驱动 MLLM 通过**分层思维链**进行多轮推理，最终生成可执行的规划器代码。

**系统提示构成**（Fig. 4）：
- **任务定义提示**：明确 MLLM 的角色与规划目标。
- **常识提示**：注入驾驶常识（如安全跟车距离、路口减速原则），弥补 MLLM 在自动驾驶特定领域知识的不足。
- **思维链引导提示**：规定分层推理的结构与输出格式。

**分层思维链推理流程**（三级递进）：
1. **场景理解**：MLLM 首先回答全局性问题（如“当前处于何种道路类型？”）和局部性问题（如“前方最近车辆的相对位置与速度？”），建立对驾驶情境的语义认知。
2. **运动指令生成**：基于场景理解，MLLM 分别输出纵向运动指令（期望速度、跟车策略）和横向运动指令（目标车道选择），每条指令均附带推理理由。
3. **规划器代码生成**：MLLM 根据运动指令调用预定义的 `Generate_IDM_Planner` 函数接口，生成实例化 IDM 规划器的 Python 代码。

消融实验（Table V）表明：去除场景理解环节导致 NR-CLS 下降 **2.42**；去除中层级运动指令导致 NR-CLS 下降 **1.91**，验证了分层推理中每一级的独立贡献。

### 反思模块

为降低 MLLM 输出不确定性带来的安全风险，反思模块对生成的规划器进行**闭环仿真验证**。

**决策规则**（式 4）：设仿真驾驶评分（综合舒适性、安全性、进度等指标）为 $s$，预设阈值为 $\lambda$，则：

$$\mathrm{Decision} = \begin{cases} \mathrm{Planning}, & s \geq \lambda \\ \mathrm{Rethinking}, & s < \lambda \end{cases}$$

若评分不低于阈值，接受当前规划器并执行；否则触发“重新思考”，将仿真反馈信息传回推理引擎重新生成规划器，最多执行 $\mathrm{max\_exe}$ 次迭代。消融实验（Table V）显示，移除反思模块将导致 NR-CLS 下降 **2.67**，是其贡献最大的单一模块。

### 关键公式：IDM 规划器

PlanAgent 生成的规划器基于智能驾驶员模型，其纵向加速度由式 (1) 给出：

$$a = \Bigg( 1 - \left( \frac{v}{v_0} \right)^\delta - \left( \frac{s^*}{s} \right)^2 \Bigg)$$

其中 $v$ 为当前速度，$v_0$ 为期望速度（由 MLLM 根据场景设定），$s$ 为当前跟车间隙，$s^*$ 为期望安全间隙，$\delta$ 为加速度指数。计算得到的加速度 $a$ 需经式 (2) 裁剪至允许的加减速极限 $[dec, acc]$ 内：

$$\frac{dv}{dt} = \min(acc, \max(a, dec))$$

MLLM 最终输出的规划器调用形式为式 (3)：

$$Generate\_IDM\_Planner(c, la, v_0, acc, dec)$$

其中 $c$ 为目标中心线，$la$ 为前导车辆信息，$v_0, acc, dec$ 为 MLLM 根据场景推理确定的规划器参数。这些参数的选择直接体现了 MLLM 对驾驶情境的常识推理结果——例如在拥堵场景下降低 $v_0$、在湿滑路面增大 $dec$ 的绝对值。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2406_01587/figures/004_Figure_3.jpg]]
*Figure 3: The top of the picture shows the process of constructing a lane map (top right) based on the environment (top left). The white square on the left represents the ego vehicle. The red node on the right indicates the centerline segment where the ego vehicle is located, while nodes of other colors correspond to lane segments of the same color on the left. The bottom of the picture displays the converted text description of the scenario based on the lane-graph, including node relationships and motion states*

## 实验与分析

### 主实验结果

PlanAgent在nuPlan闭环规划挑战赛的Val14和Test14-hard基准上均取得最优性能，验证了其在常见场景与长尾场景下的规划能力与泛化性。

在Val14基准上，PlanAgent的非反应式闭环评分（NR-CLS）达到**93.26**，反应式闭环评分（R-CLS）达到**92.75**，分别以+0.75和+0.96的幅度超越此前最强的规则基方法**PDM-Closed**（Dauner et al., CoRL 2023）。在学习基方法中，**PlanTF**（Cheng et al., ICRA 2024）和**DTPP**（Huang et al., ICRA 2024）的NR-CLS分别为86.05和72.61，与PlanAgent差距明显。这表明PlanAgent在常见场景下已具备与精心调优的规则基方法相当甚至更优的闭环驾驶能力。

更具说服力的证据来自Test14-hard长尾基准。在该基准上，PlanAgent的NR-CLS达到**72.51**，较PDM-Closed的65.07提升**+7.44**；R-CLS达到**76.82**，较PDM-Closed的75.18提升**+1.64**。学习基方法PlanTF和DTPP在Test14-hard上的NR-CLS分别为38.31和48.36，远低于PlanAgent。这一结果直接支撑了论文的核心论断：基于MLLM的常识推理能力使PlanAgent在长尾场景中展现出显著优于规则基和学习基方法的泛化性能（见Table II）。

从场景类型细分来看，Figure 5展示了PlanAgent与PDM-Closed在Test14-hard的14种场景类型上的NR-CLS对比。PlanAgent在多数场景类型上取得领先，尤其在需要复杂交互推理的长尾场景中优势更为突出，进一步佐证了分层思维链引入的常识推理对长尾泛化的关键作用。

### Token效率

场景编码效率是PlanAgent的另一关键优势。Table III显示，PlanAgent的场景文本描述平均仅需**141.32 tokens**，而**GPT-Driver**（Mao et al., arXiv 2023）和**LLM-ASSIST**（Sharan et al., arXiv 2023）分别需要709.34和441.41 tokens。PlanAgent的token消耗约为GPT-Driver的**五分之一**，这得益于环境变换模块中BEV地图提供全局语义信息与车道图文本描述仅保留周围8个节点智能体信息的设计。更低的token消耗不仅降低了MLLM推理成本，也减少了长上下文带来的注意力分散风险。

### 消融实验

消融实验系统性地验证了PlanAgent各核心模块的贡献，所有实验均在Test14-hard基准上进行。

**环境变换模块消融**（Table IV）：对比三种场景编码方式——仅文本描述、仅BEV地图、BEV地图+车道图文本描述（完整方案）。完整方案取得最高的NR-CLS（72.51）和R-CLS（76.82），证明BEV地图的全局语义与车道图文本的局部精确信息形成互补。仅使用文本描述时性能下降最为明显，说明BEV地图提供的空间布局信息对MLLM的场景理解不可或缺。

**推理引擎与反射模块消融**（Table V）：分别移除分层思维链中的场景理解环节、中层级运动指令环节以及Reflection模块。结果显示：
- 移除**场景理解**（高维全局/局部问答）导致NR-CLS下降**2.42**；
- 移除**中层级运动指令**（纵向/横向推理）导致NR-CLS下降**1.91**；
- 移除**Reflection模块**导致NR-CLS下降**2.67**。

三个模块的贡献幅度表明，Reflection模块的安全验证机制对性能影响最大，场景理解次之，运动指令再次。这揭示了MLLM在闭环规划中的核心瓶颈在于输出不确定性，而Reflection模块通过仿真评估与重新思考机制有效缓解了这一问题。

**MLLM调用间隔消融**（Table VI）：考察不同MLLM调用间隔（0.5s、1s、2s、3s、4s、5s）对性能的影响。调用间隔为**2秒**时PlanAgent取得最优NR-CLS（72.51）和R-CLS（76.82）。间隔过短（0.5s）或过长（5s）均导致性能下降：过短的间隔可能引入冗余推理噪声，过长的间隔则使规划器无法及时响应环境变化。

**MLLM模型选型消融**（Table VII）：对比GPT-4V、GPT-4o、Gemini-1.5-Pro等不同多模态大语言模型在PlanAgent框架下的表现。**GPT-4V**取得最高的NR-CLS（72.51）和R-CLS（76.82），验证了其在多模态场景理解和分层推理上的优势。其他MLLM的性能均有不同程度下降，说明当前框架的性能与底层MLLM的能力密切相关。

### 定性分析

Figure 6展示了PlanAgent与PDM-Closed在具体场景中的定性对比，以及PlanAgent的分层推理过程示例。在需要常识推理的复杂交互场景（如无保护左转、拥挤环岛）中，PDM-Closed倾向于保守或产生不自然的轨迹，而PlanAgent通过场景理解—运动指令—代码生成的分层推理，能够产出更符合人类驾驶直觉的决策。推理过程示例显示，MLLM首先分析全局场景（“当前处于三车道道路，前方有慢速车辆”），然后给出纵向和横向运动指令及理由（“建议向左变道以超越前车，因为左侧车道空闲且速度限制允许”），最终生成对应的IDM规划器代码。这一可视化证据直观支持了分层思维链设计的有效性。

### 失败模式与局限

尽管PlanAgent在基准上表现优异，分析揭示了若干值得关注的局限：

1. **MLLM未在自动驾驶数据上微调**：当前GPT-4V等MLLM仅依赖通用预训练知识进行推理，在高度专业化的场景（如施工区特殊标志识别）中可能出现理解偏差。Table VII中不同MLLM的性能差异也暗示，模型的选择对最终性能有显著影响。

2. **固定调用间隔策略的次优性**：Table VI表明2秒间隔最优，但该策略未考虑场景紧急程度。在需要快速反应的突发场景中，固定间隔可能导致响应延迟；在稳定巡航场景中则造成不必要的计算开销。

3. **反思模块的评分函数依赖**：Reflection模块的决策依赖于预定义的仿真评分阈值λ（见公式(4)），该评分函数可能无法完全覆盖所有安全维度（如社会合规性、乘客舒适度），存在漏检不安全规划器的风险。

4. **规划器模板限制**：当前MLLM输出的是IDM规划器的参数化代码（见公式(3)），这限制了高层行为多样性。在需要非IDM行为（如紧急避让、协同让行）的场景中，模板约束可能成为性能上限。

### 与LLM基方法的属性对比

Table I系统比较了PlanAgent与近期LLM基规划方法的属性差异。PlanAgent是首个同时具备**闭环规划**、**多模态输入**（BEV图像+文本）、**中到中规划范式**、**安全验证机制**的MLLM基系统。相比之下，**GPT-Driver**和**Agent-Driver**（Mao et al., arXiv 2023）仅支持开环规划，**DiLu**（Wen et al., ICLR 2024）虽支持闭环但仅适用于highway-env简化环境，**LLM-ASSIST**仅生成控制器参数而缺乏完整的场景理解与推理链。这一属性对比凸显了PlanAgent在系统完整性和实用性上的领先。

### 补充图表

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2406_01587/figures/005_Table.jpg]]
*Table: II COMPARISON WITH COMPETITIVE METHODS ON VAL14 AND TEST14-HARD BENCHMARKS OF NUPLAN CLOSED-LOOP PLANNING CHALLENGE*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2406_01587/figures/001_Figure_1.jpg]]
*Figure 1: Quantitative results of non-reactive closed-loop motion planning on nuPlan [1] Val14 and Test14-hard benchmarks compared with the state-of-theart rule-based method PDM-Closed [2] and learning-based method PlanTF [3] and DTPP [4]. Our proposed PlanAgent achieves state-of-the-art performance in common scenarios (Val14 benchmark) and demonstrated generalization in more challenging long-tailed scenarios (Test14-hard benchmark). Other methods either perform poorly in common scenarios or find it difficult to generalize to long-tailed scenarios. Please note that PDM-Closed, PlanTF, DTPP, and PlanAgent are denoted by purple, green, yellow, and orange, respectively. The best performances are represe...*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2406_01587/figures/006_Figure_5.jpg]]
*Figure 5: The comparison of the NR-CLS metric between our proposed PlanAgent and PDM-Closed [2] across 14 scenario types based on the nuPlan Test14-hard benchmark*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2406_01587/figures/007_Table.jpg]]
*Table: III THE AVERAGE NUMBER OF TOKENS USED TO DESCRIBE THE SCENE IN THE TEXTUAL DESCRIPTION. TABLE V ABLATION STUDY OF REASON ENGINE AND REFLECTION MODULE ON TEST14-HARD BENCHMARK. TABLE VI*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2406_01587/figures/008_Table.jpg]]
*Table: IV ABLATION STUDY OF ENVIRONMENT TRANSFORMATION MODULE ON TEST14-HARD BENCHMARK*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2406_01587/figures/009_Table.jpg]]
*Table: ABLATION STUDY OF THE INTERVAL OF MLLM CALLS ON TEST14-HARD BENCHMARK*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2406_01587/figures/010_Table.jpg]]
*Table: VII PERFORMANCE OF DIFFERENT MULTI-MODAL LARGE LANGUAGE MODELS FOR PLANAGENT ON TEST14-HARD BENCHMARK*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2406_01587/figures/002_Table.jpg]]
*Table: I COMPARISON BETWEEN PLANAGENT AND RECENT LLM-BASED APPROACHES*

![[assets/figures/papers/paper_list_l17_https_arxiv_org_abs_2406_01587/figures/011_Figure_6.jpg]]
*Figure 6: Qualitative comparison between PlanAgent (ours) and PDM-Closed and qualitative example of the hierarchical reasoning of PlanAgent*

## 方法谱系与知识库定位

### 1 在自动驾驶规划方法谱系中的位置

PlanAgent 处于**规则基规划、学习基规划与LLM基规划的交叉地带**，其核心贡献在于首次将多模态大语言模型的常识推理能力引入闭环运动规划，并通过分层思维链与反思机制弥合了“常识泛化”与“安全闭环”之间的鸿沟。

从方法谱系看，现有闭环运动规划方法可大致分为三类：

**（1）规则基方法**：以 **PDM-Closed**（Dauner et al., CoRL 2023）为代表，依赖人工定义的IDM参数与搜索策略。这类方法在常见场景中表现稳健（Val14 NR-CLS 92.51），但在长尾场景中因缺乏场景自适应能力而性能骤降（Test14-hard NR-CLS仅65.07），暴露了规则基方法“泛化天花板”的根本瓶颈。

**（2）学习基方法**：包括直接预测轨迹的模仿学习器 **PlanTF**（Cheng et al., ICRA 2024）和集成预测与规划的 **DTPP**（Huang et al., ICRA 2024）。这类方法在常见场景中表现更差（Val14 NR-CLS分别仅为49.67和43.96），且同样难以泛化至长尾场景。其瓶颈在于：纯数据驱动的方式无法内化人类驾驶的常识推理（如“在拥堵路口应减速礼让而非强行插入”），导致在分布外场景中行为不合理。

**（3）LLM基方法**：早期探索如 **GPT-Driver**（Mao et al., arXiv 2023）和 **Agent-Driver**（Mao et al., arXiv 2023）仅支持开环规划；**DiLu**（Wen et al., ICLR 2024）虽实现了闭环，但仅限于highway-env简化的仿真环境；**LLM-ASSIST**（Sharan et al., arXiv 2023）则仅用LLM生成控制器参数而非完整规划器。这些方法的共同局限在于：场景表示效率低下（token消耗高达数百至上千），且缺乏结构化的安全验证机制。

PlanAgent 的定位是**首个面向真实场景闭环的中到中（mid-to-mid）MLLM规划智能体**：它不直接输出轨迹点，而是生成可执行的IDM规划器代码，在保留规则基方法安全框架的同时，通过MLLM的常识推理赋予其场景自适应的泛化能力。

### 2 核心方法边界与适用条件

PlanAgent 的设计决策划定了其方法边界：

**（1）场景编码的效率边界**：Environment Transformation模块通过BEV地图（全局语义）与车道图文本描述（局部智能体信息，仅保留周围8个节点）的混合编码，将平均token消耗压缩至141.32，约为GPT-Driver的1/3（709.34 tokens）和LLM-ASSIST的1/3（441.41 tokens）。这一设计使MLLM调用在计算上可行，但代价是丢弃了远距离智能体的细粒度信息——在高速多车交互场景中可能丢失关键上下文。

**（2）推理结构的层次边界**：分层思维链（场景理解→纵向/横向运动指令→代码生成）将复杂的规划问题分解为可解释的子任务。消融实验表明，场景理解层对NR-CLS贡献2.42，运动指令层贡献1.91，反映了“先理解后决策”的认知分层是有效的。但这一结构依赖预定义的常识提示（common sense prompts），其覆盖范围决定了推理的上界——对于提示中未涵盖的罕见场景（如道路施工区的非标准标志），MLLM可能产生错误理解。

**（3）安全机制的仿真边界**：Reflection模块通过仿真评估生成规划器并触发重新思考，对NR-CLS贡献2.67（消融实验中降幅最大）。其决策规则为：若仿真评分 $s \geq \lambda$ 则执行，否则重新生成（最多max_exe次）。这一机制有效降低了MLLM输出的不确定性，但其可靠性受限于离线仿真器的保真度——仿真器无法完全复现真实世界的物理交互与传感器噪声。

**（4）规划器模板的多样性边界**：PlanAgent生成的规划器仍基于手动设定的IDM模板，MLLM仅负责选择中心线、前导车辆、速度/加减速限制等参数。这限制了高层行为多样性（如无法生成“绕行静止障碍物”的复杂轨迹），使其在需要非标准机动（如紧急避让）的场景中可能失效。

### 3 局限性分析

根据论文自述及方法边界分析，PlanAgent存在以下局限：

1. **MLLM未在自动驾驶数据上微调**：当前使用GPT-4V等通用MLLM，未针对驾驶场景进行领域适配，可能导致在特定复杂场景（如密集人流、非结构化道路）中的理解精度不足。论文明确指出这一点，并提出了微调作为未来方向。

2. **固定时间间隔的MLLM调用策略**：消融实验表明2秒调用间隔最优，但这一策略是静态的——在场景简单时造成冗余计算，在场景突变时可能响应滞后。自适应触发机制（如基于不确定性或风险度量动态调整调用频率）是明确的改进方向。

3. **反思模块依赖离线评分函数**：当前评分函数是预定义的，可能无法覆盖所有安全维度（如乘客舒适度、社会合规性）。论文未详细披露评分函数的具体构成，其完备性需要人工验证。

4. **IDM模板限制了行为空间**：规划器生成被约束在IDM参数选择的框架内，无法表达更丰富的高层行为（如变道决策、路口博弈）。这使PlanAgent在需要灵活战术决策的场景中可能不如端到端方法。

5. **长尾场景的泛化虽显著提升但仍有差距**：在Test14-hard上NR-CLS为72.51，虽远超PDM-Closed（65.07），但与Val14上的93.26相比仍有21个百分点的下降，说明长尾场景仍是开放挑战。

### 4 开放问题与未来方向

论文提出或隐含了以下开放问题：

1. **领域微调与对齐**：如何利用自动驾驶数据（如nuPlan的场景-轨迹对）对MLLM进行监督微调或RLHF，以增强其在驾驶场景中的理解准确率和规划合理性？这涉及将通用常识与领域特定知识融合的技术挑战。

2. **自适应推理触发**：如何设计基于场景复杂度或不确定性的自适应MLLM调用策略，在保证安全的前提下最小化计算开销？可能的方向包括：利用MLLM自身输出置信度、场景突变检测、或轻量级风险评估器作为触发条件。

3. **闭环仿真反馈的强化学习**：能否将Reflection模块的仿真评分作为奖励信号，通过强化学习或直接偏好优化（DPO）对MLLM的规划策略进行迭代改进，使其驾驶行为更接近人类专家？

4. **去模板化的端到端思维链**：能否将分层思维链推广至更灵活的规划输出形式（如直接生成航点序列或代价函数），减少对预定义IDM模板的依赖，从而扩展行为多样性？这需要在安全约束与灵活性之间寻找新的平衡点。

5. **多智能体交互推理**：当前车道图描述仅保留周围8个节点的智能体信息，如何扩展MLLM的注意力范围以建模更复杂的多车博弈（如路口无信号灯协商），同时不显著增加token开销？

---

**需要人工验证的点**：论文未披露Reflection模块评分函数的具体构成（如各子指标的权重），也未详细说明max_exe的取值及其对性能的影响。消融实验中各模块的贡献值（2.42/1.91/2.67）来自单一MLLM（GPT-4V）的实验，其在不同MLLM上的稳定性需要进一步验证。

## 原文 PDF

![[paperPDFs/arxiv_2024/PlanAgent_A_Multi_modal_Large_Language_Agent_for_Closed_loop_Vehicle_Motion_Planning.pdf]]
