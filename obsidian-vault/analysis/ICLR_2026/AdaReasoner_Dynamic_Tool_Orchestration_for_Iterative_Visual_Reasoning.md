---
title: "AdaReasoner: Dynamic Tool Orchestration for Iterative Visual Reasoning"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/AdaReasoner_Dynamic_Tool_Orchestration_for_Iterative_Visual_Reasoning.pdf
aliases:
- ADTOIVR
acceptance: accepted
openreview_forum_id: nUGPEmQ2ut
tags:
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/vision_models_multimodal
core_operator: 引入多轮动态工具编排机制：将工具增强推理形式化为状态-动作-观察序列决策过程，并辅以专门设计的数据管线（包含反思与工具失败案例）和适配多轮工具调用的工具GRPO强化学习算法，使模型能够自适应地选择、组合、弃用工具。
primary_logic: 通过冷启动阶段向模型植入正确的工具使用模式，再利用强化学习中的多轮奖励和自适应激励机制优化工具调用策略，模型能够自主发展出根据任务需求调整工具种类和使用频率的涌现行为，从而突破模型规模的限制，使小模型获得与大型专有模型匹敌甚至更优的性能。
claims:
- AdaReasoner 为 7B 模型带来平均 +38.7% 的性能提升，在 VSP 上达到 97.6% 准确率，远超基线。
- 工具冷启动 (TC) 与工具 GRPO (TG) 的组合训练显著优于单独使用直接 SFT 或直接 GRPO，例如 7B 模型在 VSP 上提升 68.00 个百分点。
- 在冷启动数据中加入反思和回溯机制能大幅提升鲁棒性：当路径规划工具 A* 不可用时，含反思训练的模型性能为 91.36，而无反思训练仅为 67.27。
- 训练期间未见过的工具（A*）可在推理时被模型零样本采纳并正确调用（成功率 94.53%），且通过 RL 训练模型能掌握工具的应用场景，在导航任务上达到 96.33% 准确率。
paradigm: 通过冷启动阶段向模型植入正确的工具使用模式，再利用强化学习中的多轮奖励和自适应激励机制优化工具调用策略，模型能够自主发展出根据任务需求调整工具种类和使用频率的涌现行为，从而突破模型规模的限制，使小模型获得与大型专有模型匹敌甚至更优的性能。
---

# AdaReasoner: Dynamic Tool Orchestration for Iterative Visual Reasoning

> [!tip] 核心洞察
> 通过冷启动阶段向模型植入正确的工具使用模式，再利用强化学习中的多轮奖励和自适应激励机制优化工具调用策略，模型能够自主发展出根据任务需求调整工具种类和使用频率的涌现行为，从而突破模型规模的限制，使小模型获得与大型专有模型匹敌甚至更优的性能。

| 字段 | 内容 |
|------|------|
| 中文题名 | AdaReasoner: 面向迭代视觉推理的动态工具编排 |
| 英文题名 | AdaReasoner: Dynamic Tool Orchestration for Iterative Visual Reasoning |
| 会议/期刊 | ICLR 2026 (accepted) |
| Links | [paper](https://openreview.net/forum?id=nUGPEmQ2ut) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/vision_models_multimodal |
| Method | AdaReasoner |
| Dataset | VSP, Jigsaw, BLINK-J (Jigsaw from BLINK), GUIChat |

> [!tip] 效果简介
> - VSP 上，Overall Accuracy （总体准确率） 为 97.64 (Qwen2.5-VL-7B + TC+TG)，对比 31.64 (Base), 46.64 (Direct SFT), 30.18 (Direct GRPO)，变化 +66.00 (vs Base)。
> - Jigsaw 上，Accuracy （准确率） 为 96.60 (Qwen2.5-VL-7B + TC+TG)，对比 45.70 (Base), 86.40 (Direct SFT)，变化 +50.90 (vs Base), +10.20 (vs Direct SFT)。
> - BLINK-J (Jigsaw from BLINK) 上，Accuracy （准确率） 为 96.00 (Qwen2.5-VL-7B + TC+TG)，对比 52.67 (Base), 88.00 (Direct SFT)，变化 +43.33 (vs Base)。

## 概述

现有多模态大语言模型（MLLM）在复杂视觉推理任务中面临双重瓶颈。其一，模型缺乏精细的迭代感知与验证能力，往往退化为依赖语义先验的“引导式猜测”，而非基于实际视觉证据进行推理。其二，现有工具增强方法局限于单步原子工具调用或脚本化的固定流程，不具备多轮规划与动态组合不同工具的能力。

针对上述瓶颈，AdaReasoner 提出了一套动态工具编排框架，其核心思想是将工具增强的视觉推理形式化为一个状态-动作-观察的序列决策过程。在此框架下，模型被赋予访问一组预定义视觉工具的能力——包括感知工具（如 POINT、OCR）、操作工具（如 DRAWLINE、INSERTIMAGE）和计算工具（如 A* 路径规划）——并通过多轮交互自主选择、组合乃至弃用工具，形成“观察-思考-行动”的推理循环。

为实现这一目标，AdaReasoner 在方法层面引入了两个关键创新。首先，设计了一套三阶段数据管线：从抽象最优轨迹蓝图出发，程序化填入真实工具调用的输入输出，再由强模型（Gemini 2.5 Flash）生成链式推理文本。该管线刻意融入反思回溯与工具失败场景，以提升模型面对工具不可用等异常情况时的鲁棒性。其次，提出适配多轮工具调用的工具 GRPO 强化学习算法，采用多轮奖励累积与自适应激励机制：答案正确的轨迹直接获得满分以鼓励高效推理，答案错误但工具使用正确的轨迹仍可获得部分分数以保护工具使用行为不被过早淘汰。

实验结果表明，AdaReasoner 使 7B 规模的 Qwen2.5-VL 模型在六个视觉推理基准上平均提升 **+38.7%**，在视觉空间规划（VSP）任务上达到 **97.6%** 的近乎完美准确率，显著超越 GPT-5、Claude Sonnet 4 等大型专有模型。更重要的是，工具增强使 3B 和 7B 小模型突破了规模限制，在 VSP 上收敛至接近统一的性能上限，证明动态工具编排能够有效弥补模型规模的差距。

消融研究进一步揭示了方法有效性的因果机制：工具冷启动阶段为后续强化学习提供了正确的工具使用先验，若跳过冷启动直接进行工具 GRPO，7B 模型在 VSP 上的性能骤降 24.93 个百分点；冷启动数据中的反思与回溯机制大幅提升了模型在工具不可用时的鲁棒性（VSP 整体准确率从 67.27 升至 91.36）；更高的工具奖励权重（λ_tool = 2:1）能显著加速收敛并提升最终性能。值得注意的是，在开放领域的 GUIQA 任务（WebMMU）中，纯工具 GRPO 反而优于先冷启动再 GRPO 的管线，提示预定义的专家蓝图在未知最优策略的任务上可能限制探索自由。

## 背景与动机

### 视觉推理的瓶颈：从“引导式猜测”到精细感知

多模态大语言模型（MLLM）在复杂视觉推理任务中面临根本性困境。尽管这些模型在视觉问答等任务上表现优异，但当问题需要精确的空间定位、多步验证或迭代试错时，它们往往退化为依赖语义先验的“引导式猜测”——模型倾向于输出统计上合理的答案，而非通过真正的视觉感知来确认事实。

这一瓶颈在两类任务中尤为突出：

1. **精细视觉感知与验证**：例如在视觉空间规划（Visual Spatial Planning, VSP）任务中，模型需要准确识别地图上的起点、终点和障碍物，并判断给定路径是否可行。基座模型 Qwen2.5-VL-7B 在此类任务上仅能达到 31.6% 的准确率（Table 2），远低于任务要求。问题根源在于通用 MLLM 的定位能力严重不足：Qwen-VL 系列模型在起点定位任务上的准确率仅为 2.5% 到 50.0%，而专用工具 Molmo-7B-D 的 POINT 工具则可达到 100%（Table 3）。

2. **多步推理与迭代验证**：拼图推理（Jigsaw）和 GUI 问答等任务要求模型进行“观察—假设—验证—修正”的循环。但现有 MLLM 缺乏在推理过程中动态获取新信息的能力，一旦初始判断错误，便无法通过后续步骤纠正。

### 现有工具增强方法的局限：单步调用与脚本化编排

为弥补上述缺陷，研究者尝试为 MLLM 配备外部工具。然而，现有方法存在两个关键不足：

- **单步原子工具调用**：大多数方法仅允许模型在单轮交互中调用一个工具，无法支持需要多个工具协同配合的复杂任务。例如，在 VSP 验证任务中，模型可能需要先用 POINT 定位起点，再用 DRAWLINE 绘制路径，最后通过视觉比对判断路径是否与障碍物重叠——这要求多轮、多工具的组合使用。

- **脚本化固定调用**：部分方法预设了工具调用的固定流程，模型无法根据具体任务需求灵活调整工具选择和使用频率。这种僵化的编排方式限制了模型在开放场景中的适应能力。

### AdaReasoner 的动机：动态工具编排

上述分析揭示了一个核心洞察：**视觉推理的瓶颈不在于模型“知道什么”，而在于模型“能看到什么”以及“如何利用所见”。** 如果能让模型像人类专家一样，在推理过程中自主决定何时使用何种工具、何时验证结果、何时放弃错误路径，那么即使是小规模模型也有望突破规模限制，达到与大型专有模型匹敌甚至更优的性能。

基于这一动机，AdaReasoner 提出将工具增强推理形式化为**状态-动作-观察序列决策过程**，并通过专门设计的数据管线和强化学习算法，使模型发展出**动态工具编排**的涌现行为——即在训练和推理过程中自适应地获取新工具、弃用无效工具、并动态调整工具使用频率（Figure 1）。这一框架的核心目标不是简单地“给模型更多工具”，而是让模型学会“何时用、用什么、何时停”。

## 核心创新

AdaReasoner 的核心创新在于将多模态工具增强推理重新定义为**状态-动作-观察的序列决策过程**，并围绕这一形式化构建了从数据生成到策略优化的完整技术栈，从而突破了现有多模态大语言模型（MLLM）在复杂视觉推理中的两大瓶颈：缺乏精细化迭代感知验证能力，以及工具调用局限于单步或脚本化范式。

### 形式化框架：工具增强推理的序列决策建模

AdaReasoner 将工具增强推理轨迹 $\tau$ 形式化为 $T+1$ 个轮次的状态、工具调用动作与环境观察的序列：

$$\tau = \{ ( s _ { 0 } , a _ { 0 } , o _ { 0 } ) , \dots , ( s _ { T } , a _ { T } , o _ { T } ) \}$$

每次工具调用 $a_t$ 引发状态从 $s_t$ 变迁至 $s_{t+1}$，新信息来自工具输出 $o_t$：

$$s _ { 0 } \xrightarrow { a _ { 0 } } s _ { 1 } \xrightarrow { a _ { 1 } } s _ { 2 } \dots \xrightarrow { a _ { T } } s _ { T + 1 }$$

这一形式化将工具调用从孤立的原子操作提升为**多轮交互式决策链**，使模型能够在“观察—思考—行动”的闭环中动态调整策略。模型策略配备对预定义视觉工具集 $\mathcal{T} = \{t_1, \ldots, t_n\}$ 的访问权限，该工具集覆盖感知（POINT、OCR）、操作（DRAW2DPATH、INSERTIMAGE）和计算（ASTAR）三类核心功能（Table 1）。

### 关键创新一：三阶段数据管线——植入正确的工具使用模式

与直接使用少量任务数据进行监督微调（Direct SFT）不同，AdaReasoner 采用**三阶段数据管线**生成高质量多轮工具使用轨迹（Figure 2a）：

1. **抽象最优轨迹蓝图设计**：针对每个任务类型，人工设计包含反思、回溯与显式工具失败场景的推理蓝图，确保模型学习到鲁棒的工具使用模式而非机械调用。
2. **程序化工具调用填充**：通过工具服务器执行蓝图中的工具调用，填入真实的输入参数与输出结果，保证数据的物理一致性。
3. **链式推理文本生成**：调用 Gemini 2.5 Flash 基于前两阶段的骨架生成自然的链式思维文本，形成完整的训练轨迹。

这一管线的关键设计在于**主动引入反思与失败案例**：轨迹中明确包含“尝试—验证—修正”的试错过程，以及工具不可用或返回错误结果时的回退策略。消融实验证实，这一设计显著提升了模型在工具不可用时的鲁棒性——当路径规划工具 A* 被禁用时，含反思训练的模型 VSP 总体准确率为 91.36，而无反思训练仅为 67.27（Table 5）。

### 关键创新二：两阶段训练——从模式植入到策略优化

AdaReasoner 的训练分为两个互补阶段，分别解决“学会使用工具”和“学会何时使用工具”两个不同层次的问题：

**第一阶段：工具冷启动（Tool Cold Start, TC）**。对基础模型进行全参数监督微调，使用上述三阶段管线生成的数据。此阶段的核心作用是向模型植入正确的工具调用语法、工具选择模式与基本推理流程。消融实验表明，工具冷启动对后续强化学习至关重要：缺少冷启动直接进行工具 GRPO 时，7B 模型在 VSP 上性能下降 24.93 个百分点，在 Jigsaw 上下降 19.82 个百分点（Table 2）。

**第二阶段：工具 GRPO（Tool GRPO, TG）**。将冷启动后的策略送入强化学习阶段，采用专门适配多轮工具调用的奖励设计与优化算法：

- **多轮奖励累积**：总奖励 $R_{\mathrm{total}} = R_{\mathrm{format}} \cdot ( \lambda_{\mathrm{tool}} \cdot R_{\mathrm{tool}} + \lambda_{\mathrm{acc}} \cdot R_{\mathrm{acc}} )$，其中格式奖励 $R_{\mathrm{format}} = \prod_{i=1}^{n} R_{format}(\tau_i)$ 要求所有轮次格式均正确才非零，工具奖励 $R_{\mathrm{tool}}$ 按参数名正确性和内容有效性分层评分（2~4 分连续区间），准确率奖励 $R_{\mathrm{acc}}$ 评估最终答案。
- **自适应激励机制**：答案正确时直接给予满分（8 分），无论是否使用工具；答案错误但工具调用轨迹正确时仍可获得部分分数（最高 4 分），以此鼓励模型在不确定时主动使用工具而非猜测。

奖励权重消融显示，更高的工具奖励权重（$\lambda_{\mathrm{tool}} : \lambda_{\mathrm{acc}} = 2:1$）相比无工具奖励（0:1）将 VSP 总体分数从 71.45 提升至 93.27，将 VSPO 从 57.37 提升至 82.34（Table 6），证明显式的工具使用激励对策略收敛至关重要。

### 关键创新三：统一的工具服务器与涌现行为

AdaReasoner 通过**统一的工具服务器**（Figure 2b）管理所有感知、操作和计算工具，模型通过特殊标记发起多轮工具调用，服务器完成状态转移并返回观察结果。这一架构使模型在工具 GRPO 阶段能够自主发展出**涌现式的自适应工具使用行为**（Figure 4）：在 VSP 验证任务上，模型逐渐减少 POINT 调用频率而增加 DRAW2DPATH 使用；在导航任务上，则呈现相反的模式。更值得注意的是，训练期间未见过的工具（A*）可在推理时被模型零样本采纳并正确调用，成功率高达 94.53%（Table 5），体现了框架的泛化能力。

### 创新边界与局限

尽管上述创新带来了显著性能提升，但存在值得关注的边界条件：

- **冷启动可能限制开放领域探索**：在 WebMMU 基准上，纯工具 GRPO（72.97）反而优于先冷启动再加 GRPO 的管线（68.16），说明预定义蓝图在未知最优策略的任务上可能成为束缚（Table 2）。
- **反思数据的双刃剑效应**：含反思训练虽提升了鲁棒性，但也可能导致策略僵化——当推理时引入新工具 A* 时，含反思训练的模型导航性能大幅下降（Table 5），其确切机制仍需进一步探明。

## 整体框架

![[obsidian-vault/assets/figures/papers/paper_list_l5_AdaReasoner_Dynamic_Tool_Orchestration_for_Iterative_Visual_Reasoning/figures/002_Figure_2.jpg]]
*Figure 2: An overview of our AdaReasoner framework. The process consists of two stages: (a) a Cold Start phase, where the trajectory is specially designed for multi-turn reasoning, and (c) a Tool GRPO phase, where the policy is refined via reinforcement learning guided by our adaptive, multi-turn reward. The central Tool Server (b) manages a diverse suite of both lightweight and compute-heavy tools, enabling all interactions throughout the pipeline*

![[obsidian-vault/assets/figures/papers/paper_list_l5_AdaReasoner_Dynamic_Tool_Orchestration_for_Iterative_Visual_Reasoning/figures/003_Table_1.jpg]]
*Table 1: Visual tools integrated within AdaReasoner. We illustrate their arguments, outputs, and core functions description. More detailed descriptions of our tools are presented in Appendix B.1*

AdaReasoner 的核心思想是将工具增强的多模态推理形式化为一个**状态-动作-观察的序列决策过程**，并围绕这一形式化构建两阶段训练管线与统一的工具服务器，使小规模视觉语言模型能够动态编排多种工具以完成复杂视觉推理任务。

### 问题形式化

给定一个视觉推理任务，模型策略 $\pi_\theta$ 可访问一组预定义的视觉工具集合 $\mathcal{T} = \{t_1, \ldots, t_n\}$。推理过程被建模为一条包含多轮交互的轨迹：

$$\tau = \{ (s_0, a_0, o_0), (s_1, a_1, o_1), \dots, (s_T, a_T, o_T) \}$$

其中 $s_t$ 为第 $t$ 轮的状态（包含问题、图像及历史交互），$a_t$ 为模型选择的工具调用动作，$o_t$ 为工具执行后返回的观察结果。状态转移遵循：

$$s_0 \xrightarrow{a_0} s_1 \xrightarrow{a_1} s_2 \dots \xrightarrow{a_T} s_{T+1}$$

每一轮工具调用将新的感知或操作信息注入状态，模型据此进行下一步推理或给出最终答案。

### 管线总览

AdaReasoner 的完整管线由三个核心模块构成（Figure 2）：

1. **工具策划模块（Tool Curation Module）**：负责生成高质量的多轮工具使用轨迹数据。该模块采用三阶段流程——首先设计包含反思与工具失败场景的抽象最优轨迹蓝图，随后通过程序化执行填入真实的工具输入输出，最后调用 Gemini 2.5 Flash 生成连贯的链式推理文本。关键在于，数据中显式植入了**反思与回溯**（鼓励试错验证）以及**显式工具失败案例**（防止对工具的过度依赖），为后续训练提供鲁棒的监督信号。

2. **工具冷启动阶段（Tool Cold Start, TC）**：使用上述策划数据进行全参数监督微调，目标是让模型掌握正确的工具调用语法、工具选择模式与基本推理流程。这一阶段充当 RL 探索之前的“行为锚定”，使模型在进入强化学习时已具备合理的初始策略，避免从随机策略开始导致的训练崩溃。

3. **工具 GRPO 阶段（Tool GRPO, TG）**：在冷启动策略基础上进行强化学习优化。该阶段采用专门设计的**多轮奖励函数**：

$$R_{\mathrm{total}} = R_{\mathrm{format}} \cdot (\lambda_{\mathrm{tool}} \cdot R_{\mathrm{tool}} + \lambda_{\mathrm{acc}} \cdot R_{\mathrm{acc}})$$

其中 $R_{\mathrm{format}} = \prod_{i=1}^{n} R_{format}(\tau_i)$ 为格式前置条件——仅当所有轮次的工具调用格式均正确时取 1，否则整条轨迹奖励归零。$R_{\mathrm{tool}}$ 为细粒度工具调用质量评分（按参数名正确性和内容有效性分层赋分），$R_{\mathrm{acc}}$ 为最终答案准确性。此外，**自适应激励机制**规定：答案正确时直接给予满分，答案错误但工具使用正确的轨迹仍可获得部分分数（最高 4 分），从而在探索与利用之间取得平衡。

4. **工具服务器（Tool Server）**：统一管理并执行三类视觉工具——感知工具（POINT、OCR）、操作工具（DRAWLINE、INSERTIMAGE、CROP、DETECTBLACKAREA）和计算工具（ASTAR）。模型通过特殊标记发起工具调用，服务器完成状态转移后返回观察结果，形成“观察-思考-行动”的闭环。

### 关键设计决策

- **冷启动的必要性**：消融实验表明，直接进行工具 GRPO 而无冷启动会导致性能大幅下降（7B 模型在 VSP 上降低 24.93 点）。冷启动阶段植入的正确工具使用模式是 RL 高效探索的前提。
- **反思数据的双刃剑效应**：冷启动中包含反思轨迹可显著提升模型在工具不可用时的鲁棒性（VSP Overall 从 67.27 提升至 91.36），但也可能导致策略僵化——当推理时引入训练期间未见过的工具（如 A*）时，含反思训练的模型反而难以有效接纳。
- **奖励权重的关键作用**：工具奖励权重 $\lambda_{\mathrm{tool}}$ 从 0:1 提升至 2:1 时，VSP 性能从 71.45 跃升至 93.27，表明对工具调用质量的显式激励是策略收敛的核心驱动力。

## 核心模块与公式推导

### 3.1 工具增强推理的形式化建模

AdaReasoner 将多模态工具增强推理形式化为一个**序列决策过程**。模型策略 $\pi_\theta$ 被赋予访问预定义视觉工具集 $T \triangleq \{ t_1, \ldots, t_n \}$ 的能力，在每一轮中根据当前状态决定是否调用工具、调用哪个工具以及以何种参数调用。

一条完整的推理轨迹 $\tau$ 被定义为状态-动作-观察三元组的序列：

$$\tau = \{ ( s_0, a_0, o_0 ), ( s_1, a_1, o_1 ), \dots, ( s_T, a_T, o_T ) \}$$

其中 $s_t$ 为第 $t$ 轮的状态（包含问题、图像及历史交互），$a_t$ 为模型在该轮选择的工具调用动作（含工具名称与参数），$o_t$ 为工具服务器返回的观察结果。状态转移遵循：

$$s_0 \xrightarrow{a_0} s_1 \xrightarrow{a_1} s_2 \dots \xrightarrow{a_T} s_{T+1}$$

每次工具调用 $a_t$ 将状态从 $s_t$ 更新至 $s_{t+1}$，新信息来源于工具输出 $o_t$。这一形式化将传统的单步推理扩展为**“观察-思考-行动”的多轮循环**，使模型能够在推理过程中动态获取、验证和修正信息。

### 3.2 三阶段数据管线

为向模型植入正确的工具使用模式，AdaReasoner 设计了统一的三阶段数据生成流程：

1. **抽象轨迹蓝图设计**：针对每个任务，人工或程序化设计最优推理逻辑的高层蓝图，明确每轮应调用什么工具、预期获得什么信息。蓝图特别包含两类关键场景——**反思与回溯轨迹**（鼓励模型进行试错验证）和**显式工具失败案例**（防止对外部工具过度依赖）。

2. **工具调用补充**：程序化执行蓝图中指定的工具调用，将真实的输入参数与输出结果填入轨迹，确保轨迹中工具交互的真实性。

3. **思维链文本生成**：调用 Gemini 2.5 Flash 将前两步产生的结构化轨迹转换为自然语言的链式推理文本，形成完整的训练样本。

### 3.3 两阶段训练管线

#### 工具冷启动阶段

在第一阶段，模型进行**全参数监督微调**，学习数据管线生成的高质量多轮工具使用轨迹。此阶段的核心目标是让模型掌握工具调用的正确语法、工具选择的判别模式以及基本的迭代推理流程。

#### 工具 GRPO 阶段

第二阶段采用专门适配多轮工具调用的强化学习算法。总奖励函数定义为：

$$R_{\text{total}} = R_{\text{format}} \cdot ( \lambda_{\text{tool}} \cdot R_{\text{tool}} + \lambda_{\text{acc}} \cdot R_{\text{acc}} )$$

其中各分量含义如下：

- **格式奖励** $R_{\text{format}} = \prod_{i=1}^{n} R_{format}(\tau_i)$：仅当轨迹中所有轮次的工具调用格式均正确时为 1，否则为 0。这是一个**硬性前置条件**——任何格式错误将导致整条轨迹的奖励归零。

- **工具奖励** $R_{\text{tool}}$：对工具调用的细粒度评分，按参数名正确性和内容有效性分层计分。在参数名正确的基础上，按正确参数比例给予 2~3 的连续分数；在全部参数名正确后，按内容有效参数比例给予 3~4 的连续分数。该设计提供了稠密的中间反馈信号。

- **准确率奖励** $R_{\text{acc}}$：基于最终答案正确性的评分。

- **自适应激励机制**：当最终答案正确时，轨迹直接获得满分（8 分），无论是否使用了工具；当答案错误但工具调用轨迹正确时，仍可获得最高 4 分的部分奖励。这一设计在鼓励工具使用的同时，避免了对工具的盲目依赖。

GRPO 通过组内标准化计算每条轨迹的优势函数：

$$A^{i} = \frac{r_i - \operatorname{mean}(\{r_1, \dots, r_N\})}{\operatorname{std}(\{r_1, \dots, r_N\})}$$

最终优化目标采用重要性采样比的剪裁代理目标与 KL 散度正则项：

$$\mathcal{J}_{\text{GRPO}}(\theta) = \mathbb{E}_{q \sim P(Q), \{\tau^{i}\} \sim \pi_{\theta_{\text{old}}}} \left[ \sum_{i=1}^{G} \sum_{j=1}^{|\tau^{i}|} \frac{1}{G |\tau^{i}|} \min( m_j^i A_i, \operatorname{clip}(m_j^i, 1-\varepsilon, 1+\varepsilon) A_i ) - \beta \mathbb{D}_{\text{KL}}(\pi_\theta \parallel \pi_{\text{ref}}) \right]$$

### 3.4 工具服务器

工具服务器统一管理三类视觉工具（详见 Table 1）：**感知工具**（POINT 定位、OCR 文字识别）、**操作工具**（DRAWLINE 画线、INSERTIMAGE 插入图像、CROP 裁剪）和**计算工具**（A* 路径规划）。模型通过特殊标记发起工具调用，服务器执行状态转移并返回观察结果，形成闭环交互。

## 实验与分析

![[obsidian-vault/assets/figures/papers/paper_list_l5_AdaReasoner_Dynamic_Tool_Orchestration_for_Iterative_Visual_Reasoning/figures/004_Table_2.jpg]]
*Table 2: Our main results on VSPO, VSP, Jigsaw, BLINK-J, GUIChat, and WebMMU benchmarks. TC, TG means Tool Cold Start and Tool GRPO, respectively. The best performance is highlighted in bold, while the second-best performance is indicated with an underline*

![[obsidian-vault/assets/figures/papers/paper_list_l5_AdaReasoner_Dynamic_Tool_Orchestration_for_Iterative_Visual_Reasoning/figures/005_Figure_3.jpg]]
*Figure 3: Overcoming scale-based limitations with tool augmentation. On the VSP task, our tools boost the performance of both 3B and 7B models, elevating them from disparate baselines to a near-uniform high performance*

![[obsidian-vault/assets/figures/papers/paper_list_l5_AdaReasoner_Dynamic_Tool_Orchestration_for_Iterative_Visual_Reasoning/figures/008_Table_5.jpg]]
*Table 5: Adaptability study on the VSP and VSPO tasks. Stage compares our full Tool Cold Start (TC) + Tool GRPO (TG) pipeline against TC alone. Reflection indicates training with (✓) or without (✗) reflection data. \mathbf { A } ^ { * } specifies tool availability: during Reinforcement Learning (RL), at Inference (Inf), or unavailable (-). A* Statistics report calls per sample and success rate*

![[obsidian-vault/assets/figures/papers/paper_list_l5_AdaReasoner_Dynamic_Tool_Orchestration_for_Iterative_Visual_Reasoning/figures/011_Figure_4.jpg]]
*Figure 4: Evolution of tool invocation frequencies for ASTAR, POINT, and DRAW2DPATH during reinforcement learning. The model is optimized on VSP Verification (cool-colored curves) and VSP Navigation (warm-colored curves) tasks*

### 核心性能突破

AdaReasoner 在六个多模态推理基准上进行了系统评估。Table 2 的主实验结果显示，基于 Qwen2.5-VL-7B 的 AdaReasoner（TC+TG）在 VSP 上达到 **97.64%** 的总体准确率，相较于基础模型的 31.64% 提升了 **+66.00 个百分点**。在 Jigsaw 任务上，7B 模型从 45.70% 跃升至 **96.60%**（+50.90 pp），在 BLINK-J 上达到 **96.00%**（+43.33 pp）。在更具挑战性的 VSPO 基准上，AdaReasoner 同样表现强劲，7B 模型达到 **85.09%** 的总体准确率（+55.47 pp）。平均而言，AdaReasoner 为 7B 模型带来了 **+38.66%** 的性能增益。

值得关注的是，AdaReasoner 使小模型突破了规模限制。Figure 3 直观展示了这一效应：在 VSP 任务上，基础 3B 和 7B 模型的准确率分别仅为 26.7% 和 31.6%，经过工具增强后分别提升至 94.7% 和 97.6%，远超 GPT-5 的 80.1% 和 Claude Sonnet 4 的 56.3%，逼近 96.2% 的平均上界。这一结果表明，**动态工具编排机制能够有效弥补模型规模带来的能力差距**。

### 两阶段训练的关键作用

Table 2 的消融行揭示了训练管线各组件的贡献。以 7B 模型在 VSP 上的表现为例：

- **Direct SFT**（无工具）：46.64%，仅比基础模型提升 15.00 pp
- **Direct GRPO**（无工具）：30.18%，甚至低于基础模型，说明纯强化学习在没有工具支持的情况下难以有效探索
- **TG only**（仅工具 GRPO，无冷启动）：72.71%
- **TC + TG**（完整管线）：**97.64%**

工具冷启动（TC）到工具 GRPO（TG）的递进带来了 **+24.93 pp** 的额外增益。在 Jigsaw 上，TC+TG 相较于 TG only 提升了 **+19.82 pp**。这一证据表明，**冷启动阶段为模型植入正确的工具使用模式是后续强化学习有效优化的前提条件**——缺乏这一阶段，GRPO 难以在巨大的动作空间中收敛到有效策略。

### 工具精度与通用模型的鸿沟

Table 3 对比了通用 MLLM 与专用工具（Molmo-7B-D 的 POINT）在起点定位任务上的精度。Qwen-VL 系列基础模型的定位准确率普遍偏低：3B 仅有 2.47%，7B 为 47.01%，即使 72B 也仅为 50.0%。相比之下，专用 POINT 工具达到 **100.0%** 的准确率。这解释了为何 AdaReasoner 能将感知子任务委托给外部工具而非依赖模型自身能力——通用视觉模型在精确空间定位上存在根本性瓶颈。

Table 4 进一步验证了工具增强上下文对零样本推理的增益。在 VSP-Verify 任务上，为不同规模的 Qwen2.5-VL 模型添加 DRAWLINE 工具可使准确率提升 **+6.83 至 +9.23 pp**，添加 POINT 工具则带来 **+7.62 至 +9.81 pp** 的增益。这表明即使是未经专门训练的模型，工具提供的结构化视觉信息也能显著改善推理质量。

### 反思机制的双刃剑效应

Table 5 的适应性研究揭示了反思数据训练的复杂影响。当路径规划工具 A* 在推理时不可用时：

- **含反思训练**的模型在 VSP Overall 上达到 **91.36**
- **无反思训练**的模型仅为 **67.27**

反思轨迹使模型学会了在工具失败时回溯和尝试替代策略，大幅提升了鲁棒性。然而，这一机制也存在代价：当在推理时引入训练期间未见过的 A* 工具时，含反思训练的模型反而无法有效接纳。Table 5 显示，在 RL 阶段使用 A* 训练、推理时可用 A* 的配置下，VSP Navigation 达到 **96.33%**、Verify 达到 **99.20%**；但若仅在推理时零样本引入 A*，含反思训练的模型在 Navigation 上仅达到 44.83%（无反思为 62.33%），Verify 从 94.20 降至 80.00%。

这说明 **反思训练可能导致策略僵化**——模型过度依赖训练期间习得的固定工具组合，在面对新工具时缺乏探索灵活性。这是一个需要手动验证的关键发现：反思数据的具体构成（如失败案例的比例、回溯深度）如何影响策略的可塑性，论文未提供充分分析。

### 工具调用策略的涌现行为

Figure 4 展示了 RL 训练过程中不同工具调用频率的动态演化。在 VSP Verification 任务（冷色调曲线）上，POINT 和 DRAW2DPATH 的调用频率随训练逐步收敛至稳定的任务专用模式；在 VSP Navigation 任务（暖色调曲线）上，ASTAR 的调用频率逐渐上升并稳定。这一涌现行为表明，**工具 GRPO 使模型能够自主发展出与任务特性匹配的工具选择策略**，而非机械地遵循冷启动阶段的固定模式。

Table 5 的 A* 统计进一步量化了这一能力：在 RL 阶段使用 A* 训练的模型中，A* 的零样本调用成功率达到 **94.53%**，平均每个样本调用 1.36 次。即使 A* 在冷启动阶段从未出现，模型仍能通过 RL 学会何时以及如何调用这一新工具。

### 奖励权重的敏感性

Table 6 的奖励权重消融实验揭示了工具奖励在 RL 优化中的关键作用。在 VSP 任务上，当工具奖励权重 λ_tool 从 0:1（仅准确性奖励）提升至 2:1（工具奖励权重为准确性的两倍）时，总体准确率从 **71.45%** 单调上升至 **93.27%**。VSPO 任务呈现相同趋势：从 57.37% 提升至 **82.34%**。

这一结果表明，**更大的工具奖励不仅加速了 RL 训练的收敛速度，还显著提升了最终性能**。其因果机制在于：工具奖励为中间步骤提供了密集的反馈信号，缓解了仅依赖最终答案正确性的稀疏奖励问题，使模型能够更有效地探索工具调用空间。

### 失败模式与局限性

尽管 AdaReasoner 取得了显著成果，但实验揭示了若干值得关注的失败模式：

1. **冷启动的策略束缚**：在 WebMMU 基准上，纯工具 GRPO（TG only）的 7B 模型达到 **72.97%**，而 TC+TG 管线仅为 **68.16%**。这说明当任务的最优工具使用策略与冷启动蓝图的预设模式不一致时，预定义轨迹反而限制了 RL 阶段的探索自由。对于开放领域的 GUIQA 类任务，这一效应尤为明显。

2. **反思导致的探索僵化**：如前所述，含反思训练的模型在面对新工具时表现出显著的能力下降。这暗示反思数据可能使模型过度内化了“在特定失败模式下使用特定替代工具”的固定策略，而非培养通用的工具适应能力。

3. **工具分心效应**：Table 5 显示，在推理时引入 A* 工具虽然提升了 Navigation 性能（44.83 → 62.33），却同时降低了 Verify 性能（94.20 → 80.00）。这表明新增工具可能分散模型的注意力，干扰其在其他子任务上的判断。

4. **泛化边界未明**：当前实验仅测试了 A* 这一种未见工具，对于完全陌生类别的工具（如代码执行、网络搜索），模型的零样本采纳能力尚未探明。

## 方法谱系与知识库定位

### 与基线方法的本质差异

AdaReasoner 与现有方法的核心分界线在于**多轮动态工具编排**的引入。传统工具增强 MLLM 方案（如单步视觉原子工具或脚本化固定调用链）将工具视为一次性外部查询，缺乏根据中间观察调整后续工具选择的能力。AdaReasoner 将这一问题形式化为状态-动作-观察的序列决策过程（Equation 1–2），使模型能够在“观察—思考—行动”循环中自适应地组合、弃用或切换工具。

相比于 Direct SFT 和 Direct GRPO 等无工具基线，AdaReasoner 的性能跃迁并非源于模型规模的增长，而是来自工具对感知与操作瓶颈的精确补偿。以 VSP 任务为例，Qwen2.5-VL-7B Base 仅达 31.64%，而加入工具冷启动与工具 GRPO 后跃升至 97.64%（Table 2）。更关键的是，这种提升使 3B 和 7B 小模型突破了规模限制，达到与 Qwen2.5-VL-72B、InternVL3-78B 乃至 GPT-5、Claude Sonnet 4 等大型专有模型匹配或超越的性能（Figure 3）。

与单纯依赖强化学习增强推理的方案（Direct GRPO）相比，AdaReasoner 的两阶段训练管线——先工具冷启动（TC）再工具 GRPO（TG）——构成了决定性差异。直接应用 GRPO 无法教会模型正确使用工具，7B 模型在 VSP 上仅得 30.18%，甚至低于 Base 模型；而加入冷启动后，工具 GRPO 可在此基础上再提升 24.93 个百分点（Table 2 Δ 行）。这表明，**正确的工具使用模式必须通过监督信号显式植入，RL 阶段的作用是优化调用策略而非从零探索工具语法**。

### 适用边界与任务依赖性

AdaReasoner 的性能增益高度依赖于任务特性与工具集之间的匹配度。在需要精确空间定位（VSP）、几何推理（Jigsaw）或结构化 GUI 操作（GUIChat）的任务上，外部感知与操作工具（POINT、DRAWLINE、OCR）提供了 MLLM 自身不具备的高精度能力，因此提升幅度最大（+50.90 至 +66.00 个百分点）。然而，在开放领域 GUI 问答任务 WebMMU 上，工具冷启动反而限制了策略探索空间：纯工具 GRPO 达到 72.97%，而 TC+TG 管线仅得 68.16%（Table 2）。这说明当任务的最优工具使用策略与预定义蓝图不一致时，冷启动阶段的专家轨迹可能成为束缚。

工具冷启动的另一个适用边界体现在**反思数据的双刃剑效应**上。包含反思与回溯轨迹的训练显著提升了模型在工具不可用时的鲁棒性：当路径规划工具 A* 被禁用时，含反思训练的模型在 VSP 上达到 91.36，而无反思训练仅为 67.27（Table 5）。但这一鲁棒性以牺牲策略灵活性为代价——含反思训练的模型在推理时引入新工具 A* 后，导航性能大幅下降，无法有效接纳训练期间未见过的工具组合。

### 局限与开放问题

**1. 冷启动的探索-利用困境。** 工具冷启动通过专家蓝图向模型植入正确的工具使用模式，但这一机制在未知最优策略的任务上可能过度约束。WebMMU 上的退化现象表明，当前框架缺乏根据任务特性自适应调节冷启动约束强度的机制。是否存在一个与任务不确定性相关的自适应权衡策略，使模型在结构化任务上充分利用专家知识，而在开放任务上保留更多探索自由？

**2. 反思数据的策略僵化。** 反思训练虽然提升了鲁棒性，但其导致策略僵化的确切机制尚未探明。当推理时引入新工具 A* 时，含反思训练的模型无法有效整合这一新能力。理解这一现象需要回答：反思数据是否在策略空间中形成了过于狭窄的“安全区域”，使模型拒绝偏离已知的成功模式？如何设计既能保持鲁棒性又不丧失探索灵活性的反思数据？

**3. 工具泛化的边界。** 当前框架验证了对训练期间未见过的 A* 工具的零样本采纳能力（调用成功率 94.53%，Table 5），但这一泛化仅限于与训练工具功能相近的计算型工具。模型能否泛化到完全不同的工具类别（如代码执行器、网络搜索引擎、外部分析 API）仍是一个开放问题。此外，模型是否能在推理时自主生成全新的工具组合模式（如链式调用多个工具形成复合操作），而不依赖于训练轨迹中的显式示例，也有待验证。

**4. 工具选择策略的可解释性。** 虽然 Figure 4 展示了 RL 过程中工具调用频率向任务专用策略的收敛，但模型在单次推理中决定选择特定工具的内部机制仍不透明。理解这一决策过程对于构建可信的自主推理系统至关重要，尤其是在高风险应用场景中。

**5. 多代理扩展的可行性。** 当前框架聚焦于单模型与工具服务器的交互。将动态工具编排扩展到多代理场景——其中不同代理负责不同子任务并共享工具调用结果——是否能保持稳定的自适应行为，是一个值得探索的方向。

## 原文 PDF

## 相关样本

- [[obsidian-vault/analysis/ICLR_2026/A.I.R._Enabling_Adaptive_Iterative_and_Reasoning-based_Frame_Selection_For_Video_Question_Answering.md|A.I.R.]]：同属视觉推理样本，可对照工具编排与帧选择式迭代推理。
- [[obsidian-vault/analysis/ICLR_2026/In-the-Flow_Agentic_System_Optimization_for_Effective_Planning_and_Tool_Use.md|In-the-Flow]]：同属工具使用与规划优化样本，可对照多模态工具调用和通用 agent flow 优化。

![[obsidian-vault/paperPDFs/ICLR_2026/AdaReasoner_Dynamic_Tool_Orchestration_for_Iterative_Visual_Reasoning.pdf]]
