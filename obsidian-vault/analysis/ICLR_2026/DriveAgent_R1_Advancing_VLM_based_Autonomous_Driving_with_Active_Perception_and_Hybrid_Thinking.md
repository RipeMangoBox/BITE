---
title: "DriveAgent-R1: Advancing VLM-based Autonomous Driving with Active Perception and Hybrid Thinking"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/DriveAgent_R1_Advancing_VLM_based_Autonomous_Driving_with_Active_Perception_and_Hybrid_Thinking.pdf
project_link: https://tsinghua-mars-lab.github.io/DriveAgent-R1/
code_link: null
openreview_forum_id: r2g8TV4nJy
aliases:
- DriveAgent-R1
tags:
- ICLR_2026
- topic/reinforcement_learning_planning_agents
- topic/reinforcement_learning_planning_agents/planning_control
core_operator: "通过主动调用视觉工具集（RoI放大、多视角检索、深度估计、3D目标检测）进行具身视觉推理的能力，以及根据场景复杂度在高效纯文本推理与鲁棒工具增强视觉推理之间自适应切换的混合思维机制。"
primary_logic: "提出主动感知框架，使智能体在遇到不确定性时能够主动调用视觉工具获取关键证据，将决策建立在可验证的视觉信息之上，并通过级联强化学习训练自适应模式选择，实现安全与效率的平衡。"
claims:
- "DriveAgent-R1 在 Drive-Internal 测试集上使用工具后获得+6.07%的准确率提升，优于 GPT-5 并接近人类驾驶水平。"
- "在 nuScenes 测试集上，DriveAgent-R1 的序列平均联合准确率超越 GPT-5（47.10% vs 45.14%），同时自适应模式选择准确率达到 65.30%。"
- "消融实验证实，主动感知比被动感知更依赖视觉证据（无图像时相对性能下降更大），且级联强化学习策略显著优于单阶段 RL。"
- "Drive-Internal_test 上 First-Frame Joint Acc. (%) w/ Tools = 51.34"
---

# DriveAgent-R1: Advancing VLM-based Autonomous Driving with Active Perception and Hybrid Thinking

> [!tip] 核心洞察
> 提出主动感知框架，使智能体在遇到不确定性时能够主动调用视觉工具获取关键证据，将决策建立在可验证的视觉信息之上，并通过级联强化学习训练自适应模式选择，实现安全与效率的平衡。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | DriveAgent-R1：基于主动感知与混合思维的视觉语言模型自动驾驶智能体 |
| 英文题名 | DriveAgent-R1: Advancing VLM-based Autonomous Driving with Active Perception and Hybrid Thinking |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=r2g8TV4nJy) · [Project](https://tsinghua-mars-lab.github.io/DriveAgent-R1/) |
| Topic | #topic/reinforcement_learning_planning_agents #topic/reinforcement_learning_planning_agents/planning_control |
| Method | DriveAgent-R1 |
| Dataset | Drive-Internal_test, nuScenes_test, DriveBench, nuScenes Validation (Open-Loop Planning) |

> [!tip] 效果简介
> - Drive-Internal_test 上，First-Frame Joint Acc. (%) w/ Tools 为 51.34，对比 GPT-5 56.48; DriveAgent-R1 without tools 45.27，变化 +6.07 (over without tools)。
> - nuScenes_test 上，Seq. Avg. Joint Acc. (%) w/ Tools 为 47.10，对比 GPT-5 45.14，变化 +1.96。
> - DriveBench 上，Perception Score 为 34.07，对比 DriveLM 16.85，变化 +17.22。

## 概要

现有基于视觉语言模型（VLM）的自动驾驶规划方法普遍采用**被动感知范式**——智能体仅依赖初始前视图和文本描述进行推理，缺乏在不确定性下主动寻求额外视觉证据的能力。这种范式带来两个核心瓶颈：其一，当场景存在歧义或遮挡时，模型无法调用更精细的视觉信息来消除不确定性，推理质量受限于初始输入的完备性；其二，冗余的多视图信息持续输入会增加计算开销并分散注意力，反而损害简单场景下的决策效率。

针对上述瓶颈，本文提出 **DriveAgent-R1**，一个具备主动感知与混合思维能力的自动驾驶智能体。其核心洞察在于：**赋予智能体在遇到不确定性时主动调用视觉工具获取关键证据的能力，并通过级联强化学习训练自适应模式选择，实现安全与效率的平衡。**

**方法定位。** DriveAgent-R1 在感知范式、推理模式和训练策略三个维度上对现有方法进行了系统性改进：

- **感知范式**：从被动文本推理升级为主动感知，智能体可按需调用视觉工具集（包括 RoI 放大、多视角检索、深度估计、3D 目标检测），将决策建立在可验证的视觉信息之上。
- **推理模式**：从单一文本链式推理升级为混合思维框架，智能体根据场景复杂度在高效文本推理（`<think_text>`）与鲁棒工具增强视觉推理（`<think_tool>`）之间自适应切换。
- **训练策略**：从标准监督微调或单阶段强化学习升级为三阶段渐进训练——领域对齐（DriveAlign-3B）→ 双模式 SFT → 级联 RL（强制对比模式 RL + 自适应模式选择 RL）。

**核心结果。** 在仅 3B 参数规模下，DriveAgent-R1 在 Drive-Internal 测试集上通过主动使用工具获得 **+6.07% 的准确率提升**，性能优于 GPT-5 并接近人类驾驶水平；在 nuScenes 测试集上，序列平均联合准确率达到 **47.10%**，超越 GPT-5（45.14%），同时自适应模式选择准确率达到 **65.30%**。消融实验证实，主动感知相比被动感知显著加深了对视觉证据的依赖（无图像时相对性能下降更大），且级联 RL 策略在模式选择准确率和规划精度上均显著优于单阶段 RL 变体。

### 自动驾驶感知范式的演进瓶颈

自动驾驶系统的决策能力高度依赖于对复杂驾驶场景的准确感知与理解。近年来，视觉语言模型（VLM）凭借其强大的多模态理解和推理能力，在自动驾驶规划任务中展现出巨大潜力。然而，现有基于VLM的驾驶智能体普遍采用**被动感知范式**：系统仅接收固定的前视图图像和文本描述，随后通过纯文本链式推理生成驾驶决策。这种范式存在两个根本性缺陷。

**第一，被动感知无法在不确定性下主动寻求额外视觉证据。** 当面对遮挡、远距离目标、复杂路口等场景时，人类驾驶员会主动调整注意力——侧头观察、注视后视镜、聚焦特定区域——以消除认知不确定性。而现有VLM智能体缺乏这种“主动看”的能力，仅能基于有限的初始视觉输入进行推理，导致在面对需要多视角验证或精细区域辨别的场景时，推理质量严重受限。例如，在复杂路口右转时，仅凭前视图可能无法确认侧向来车或行人信号灯状态，而被动推理系统只能依赖不完整信息做出决策。

**第二，冗余多视图信息增加计算开销并分散注意力。** 部分方法试图通过向VLM输入全部多视图图像（如前、后、左、右、广角等）来弥补信息不足，但这种策略带来了新的问题：大量冗余视觉token显著增加了推理延迟和计算成本，同时分散了模型对关键区域的注意力，反而降低了决策效率。

### 现有方法的推理模式局限

当前主流的VLM驾驶智能体，如**DriveLM**（Sima et al., 2024）和**Dolphins**（Ma et al., 2024），其推理过程本质上是单一模式的文本链式推理。这种推理方式在简单场景下效率尚可，但在复杂场景中缺乏与视觉世界的交互验证能力。相比之下，人类驾驶员的认知过程具有显著的**混合思维特征**：在熟悉的直行道路上，驾驶员可以依赖快速、直觉性的判断；而在复杂路口或突发状况下，则会主动调用视觉注意力进行深度观察和验证，再做出审慎决策。现有系统未能模拟这种根据场景复杂度自适应切换推理模式的能力。

### 核心动机与研究目标

基于上述分析，本文的核心动机在于：

1. **赋予VLM智能体主动感知能力**：设计一套视觉工具集（包括RoI放大、多视角检索、深度估计、3D目标检测），使智能体在遇到不确定性时能够主动调用这些工具获取关键视觉证据，将决策建立在可验证的视觉信息之上，而非仅依赖初始输入和文本推理。

2. **建立混合思维框架**：模拟人类驾驶员的认知模式，使智能体能够根据场景复杂度在高效纯文本推理与鲁棒工具增强视觉推理之间自适应切换，在安全性与计算效率之间取得平衡。

3. **通过渐进训练培养工具使用与模式选择能力**：工具的有效使用和自适应模式选择并非VLM的固有能力——实验表明，未经专门训练的模型（如Qwen2.5-VL-3B/7B）在使用工具时反而会出现性能下降。因此，需要设计专门的训练策略，通过级联强化学习逐步培养智能体的工具调用和模式选择能力。

最终目标是构建一个仅3B参数规模、但能够通过主动感知和混合思维达到与顶级闭源模型（如GPT-5）可比甚至更优性能的自动驾驶智能体，同时接近人类驾驶水平。

## 核心方法与创新机理

DriveAgent-R1 的核心创新在于将自动驾驶智能体的感知范式从**被动文本推理**转变为**主动具身视觉推理**，并通过**混合思维机制**实现安全与效率的平衡。相对现有 VLM-based 驾驶智能体，该方法在三个关键维度上实现了突破。

### 1. 感知范式：从被动文本推理到主动视觉工具调用

现有方法（如 **DriveLM** (Sima et al., 2024)、**Dolphins** (Ma et al., 2024)）采用被动感知范式，智能体仅基于初始前视图和文本描述进行链式推理，在遇到视觉不确定性时无法主动寻求额外证据。DriveAgent-R1 引入了一套**视觉工具集（Vision Toolkit）**，使智能体能够根据推理需求主动调用：

- **Retrieve View**：检索其他视角的图像以获取被遮挡或视野外的信息
- **RoI Inspection**：对感兴趣区域进行放大观察，捕捉细节（如远处交通标志、车辆碰撞）
- **Depth Estimation**：获取场景深度信息，辅助距离判断
- **3D Object Detection**：获取三维目标检测结果，增强空间理解

工具调用的核心机制在于**上下文历史更新**：每次工具调用后，新的文本思维 $T_k$ 与工具返回的编码视觉证据 $I_k$ 被拼接到历史中，形成迭代增强的推理链：

$$H_k = H_{k-1} \oplus T_k \oplus I_k, \quad \mathrm{for~} k < K$$

这一机制使智能体的决策建立在可验证的视觉信息之上，而非仅依赖初始文本推理。消融实验（Table 7）证实了主动感知的因果作用：完整工具集在无图像时相对性能下降 -15.8%，远高于被动前视图模式的 -7.2%，表明主动感知**显著加深了模型对视觉证据的依赖**，有效缓解了视觉忽视问题。

### 2. 推理模式：混合思维框架的自适应切换

现有方法采用单一的文本链式推理路径，无法根据场景复杂度调整推理策略。DriveAgent-R1 提出**混合思维框架（Hybrid-Thinking）**，允许智能体在两类推理模式间自适应选择：

- **文本推理（$\mathcal{M}_{\text{text}}$）**：适用于简单场景，直接基于初始视觉和文本信息进行高效推理
- **工具增强视觉推理（$\mathcal{M}_{\text{tool}}$）**：适用于复杂场景，通过迭代调用视觉工具获取关键证据

模式选择由智能体自主决策，通过生成 `<think_text>` 或 `<think_tool>` 标记触发不同推理路径。这一设计的核心优势在于效率与鲁棒性的平衡：Table 8 显示，自适应模式（$\mathcal{M}_{\text{adaptive}}$）相比纯工具模式将推理延迟从 7.91s 降至 6.74s，输出 tokens 从 314.45 降至 265.57，同时保持了较高的规划准确率。

### 3. 训练策略：三阶段渐进训练与级联强化学习

为培养上述能力，DriveAgent-R1 设计了**三阶段渐进训练策略**，其核心是**级联强化学习（Cascaded RL）**：

- **Stage 1 — 双模式监督微调（DM-SFT）**：使用 4K 高质量 CoT 数据（工具必要/非必要各 2K），赋予模型对两种推理模式的格式和语义基础理解
- **Stage 2 — 强制对比模式 RL（FCM-RL）**：通过 **MP-GRPO** 变体，强制生成等量的文本模式和工具模式响应，构成统一响应组进行奖励归一化：

$$\mathcal{O}(q) = \{o_i^{\text{text}}\}_{i=1}^{G/2} \cup \{o_j^{\text{tool}}\}_{j=1}^{G/2}$$

这一阶段的核心机制是**对比学习**：通过在同一问题下比较两种模式的准确率差异，模型学会识别何时需要工具辅助。奖励函数为 $R = R_{\text{acc}} + R_{\text{fmt}}$。

- **Stage 3 — 自适应模式选择 RL（AMS-RL）**：引入**条件工具使用奖励**，鼓励有效工具调用并惩罚冗余调用：

$$R = R_{\text{acc}} + R_{\text{fmt}} + \mathbb{I}(\text{mode} = \mathcal{M}_{\text{tool}}) \cdot R_{\text{tool}}$$

其中 $R_{\text{tool}} = (R_{\text{acc}, i} - \bar{R}_{\text{acc}}^{\text{text}}) - N_i \cdot C_{\text{tool}}$，通过对比文本模式基线准确率来量化工具调用的净收益，每次工具调用成本 $C_{\text{tool}} = 0.125$。

消融实验（Table 6）证实了级联策略的必要性：完整三阶段训练的 MSA（模式选择准确率）达到 65.30%，显著优于仅 SFT（47.10%）或单阶段 RL 变体。Figure 4 进一步揭示了各阶段的渐进增益——$\mathcal{M}_{\text{adaptive}}$ 模式的准确率和 MSA 随训练阶段逐步提升，验证了级联设计对培养自适应能力的因果作用。

### 局限与待解决问题

尽管创新显著，该方法仍存在已知瓶颈：
- **工具过度依赖**：在复杂路口中，智能体可能因误解侧视图中的行人红绿灯而推翻正确的初始判断（Figure 16），暴露出对最新感知证据的盲目接受倾向
- **基础理解不足**：面对多交通信号冲突场景时，推理可能忽略上下文语义而机械采纳感知结果
- **工具使用的双刃剑效应**：小模型（Qwen2.5-VL-3B/7B）在无专门训练时使用工具反而导致性能下降（Table 1），表明该能力需要模型基础能力或针对性训练的支撑

这些局限指向未来的研究方向：如何通过对抗性场景训练增强辩证推理能力，以及如何动态调整工具调用阈值以在计算开销和安全性之间取得更优平衡。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_r2g8TV4nJy/figures/002_Figure_2.jpg]]
*Figure 2: The Hybrid-Thinking architecture of DriveAgent-R1. For simple scenarios (Top), the agent uses direct text-based reasoning ( T _ { 1 } A ) . For complex scenarios (Bottom), it iteratively interleaves thoughts ( T _ { k } ) with tool calls to a Vision Toolkit, acquiring new visual evidence ( I _ { k } ) to refine its decision-making. The detailed visulization of this case is shown in Fig. 10, Appendix A.10*

DriveAgent-R1 的整体架构围绕**主动感知**与**混合思维**两个核心机制构建，形成一条从视觉输入到规划决策的端到端推理管线。

### 管线总览

系统以多视图图像和文本导航指令作为输入，经过三个关键阶段的处理：

1. **领域对齐基础模型（DriveAlign-3B）**：以 Qwen2.5-VL-3B 为基础，在 530K 驾驶场景 VQA 数据上进行全参数微调，增强模型对驾驶场景中视觉细节的敏感性，为后续的主动感知提供视觉基础。该模型作为整个管线的统一初始化点。

2. **混合思维推理引擎**：在推理时，智能体首先进行**模式选择**——根据场景复杂度自适应决定走哪条推理路径：
   - **纯文本推理（Text-based M-CoT，记为 M_text）**：适用于简单场景，直接基于初始前视图和文本描述进行链式推理，生成元动作序列。
   - **工具增强视觉推理（Tool-based M-CoT，记为 M_tool）**：适用于复杂或不确定场景。智能体通过迭代地“思考—调用工具—获取视觉证据”的循环，逐步澄清不确定性。当智能体判断需要额外视觉信息时，会主动调用**视觉工具集（Vision Toolkit）**中的工具，获取高分辨率 RoI 放大、多视角检索、深度估计或 3D 目标检测结果，并将工具返回的编码视觉证据拼接到上下文历史中，作为后续推理的依据。上下文历史的更新遵循公式：
     $$H_k = H_{k-1} \oplus T_k \oplus I_k, \quad \mathrm{for~} k < K$$
     其中 $H_{k-1}$ 为前一历史，$T_k$ 为新的文本思维，$I_k$ 为工具返回的视觉证据。

3. **运动规划头（Motion Planning MLP Head）**：一个轻量 MLP，接收混合思维引擎输出的高层元动作序列（one-hot 编码）、视觉 token 以及自车状态信息，将其转换为低层的未来轨迹点（预测 3 秒内以 2Hz 采样的路径点），完成从语义决策到可执行轨迹的桥接。

### 视觉工具集设计

视觉工具集是主动感知能力的执行载体，包含四个可被智能体按需调用的工具：

- **Retrieve View（多视角检索）**：获取其他相机视角的图像，弥补单视角盲区。
- **RoI Inspection（感兴趣区域放大）**：对特定区域进行高分辨率裁剪和放大，用于确认远处或模糊目标。
- **Depth Estimation（深度估计）**：提供场景深度信息，辅助距离判断。
- **3D Object Detection（3D 目标检测）**：获取目标的空间位置和尺寸，增强对三维场景结构的理解。

### 训练管线

上述推理能力的获得依赖于**三阶段渐进训练策略**：

- **阶段一：双模式监督微调（Dual-Mode SFT）**：使用 4K 高质量思维链数据（工具必要和工具不必要各 2K），让模型同时学习文本推理和工具增强推理的格式与语义边界。
- **阶段二：强制对比模式强化学习（MP-GRPO）**：在 15K 探索集上，强制模型对每个问题同时生成文本模式和工具模式的响应，通过统一的奖励归一化让模型直接对比两种模式的优劣，建立模式选择的初步能力。
- **阶段三：自适应模式选择强化学习**：在阶段二的基础上，引入条件工具使用奖励 $R_{\mathrm{tool}}$，鼓励模型在工具确实能带来准确率增益时选择工具模式，同时惩罚不必要的工具调用，最终实现安全与效率的平衡。

图 2 展示了混合思维架构中两种推理路径的示意：简单场景下直接文本推理，复杂场景下迭代交织思维与工具调用。图 3 则概括了整个三阶段渐进训练流程。

### 领域对齐基础模型：DriveAlign-3B

DriveAgent-R1 以 Qwen2.5-VL-3B 为基础，首先通过 530K 驾驶场景 VQA 数据进行全参数微调，获得领域对齐模型 **DriveAlign-3B**。该阶段的核心目标是增强基础 VLM 对驾驶场景的视觉敏感性，为后续主动感知和混合思维训练提供统一的初始化基础。消融实验表明，领域对齐使规划序列平均联合准确率提升 +1.86%，且对齐后的模型在移除图像时性能相对下降更大（-15.8% vs -11.0%），说明其决策更深度地依赖视觉证据，有效缓解了视觉忽视问题。

### 混合思维框架

DriveAgent-R1 的核心推理架构采用混合思维机制，根据场景复杂度在两条推理路径间自适应切换：

- **文本推理模式（M_text）**：适用于简单场景，智能体直接基于初始前视图和文本描述进行链式思维推理，生成元动作序列。
- **工具增强推理模式（M_tool）**：适用于复杂或不确定场景，智能体迭代调用视觉工具集获取额外证据，将决策建立在可验证的视觉信息之上。

模式选择通过生成 `<think_text>` 或 `<think_tool>` 标记实现，该标记决定后续推理路径。在工具模式下，上下文历史按以下公式更新：

$$H_k = H_{k-1} \oplus T_k \oplus I_k, \quad \mathrm{for~} k < K$$

其中 $H_{k-1}$ 为前一步历史，$T_k$ 为第 $k$ 步生成的文本思维，$I_k$ 为工具调用返回的编码视觉证据，$\oplus$ 表示拼接操作。该迭代过程允许智能体在最多 $K$ 步内逐步收集关键视觉信息，最终输出元动作序列。

### 视觉工具集

Vision Toolkit 包含四个可主动调用的视觉工具：

1. **Retrieve View（多视角检索）**：从多摄像头阵列中检索目标视角图像，补充前视图之外的场景信息。
2. **RoI Inspection（感兴趣区域放大）**：对指定区域进行高分辨率裁剪和放大，用于细粒度目标识别。
3. **Depth Estimation（深度估计）**：估计场景中物体的距离信息，辅助空间推理。
4. **3D Object Detection（3D 目标检测）**：提供三维空间中目标的位置和尺寸信息。

工具调用由智能体自主决定，每次调用消耗计算资源。消融实验证实，完整工具集相比被动感知（仅前视图）在保留图像时准确率更高（45.42% vs 42.70%），且移除图像时相对下降更大（-15.8% vs -7.2%），表明主动感知显著加深了模型对视觉证据的依赖。

### 级联强化学习目标函数

训练采用三阶段渐进策略：领域对齐 → 双模式 SFT → 级联 RL。级联 RL 阶段使用 GRPO（Group Relative Policy Optimization）目标函数：

$$\mathcal{I}_{GRPO}(\theta) = \mathbb{E}_{q \sim P(Q), \{o_i\} \sim \pi_{\theta_{old}}} \left[ \frac{1}{G} \sum_{i=1}^{G} \left( \min \left( w_i A_i, \mathrm{clip}(w_i, 1 \pm \epsilon) A_i \right) - \beta \mathbb{D}_{KL}(\pi_{\theta} || \pi_{ref}) \right) \right]$$

其中重要性采样比率为：

$$w_i = \frac{\pi_{\theta}(o_i | q)}{\pi_{\theta_{old}}(o_i | q)}$$

GRPO 通过组内输出估计基线，无需额外 critic 模型。级联 RL 分为两个子阶段：

**Stage 2：强制对比模式 RL（FCM-RL）**。采用 MP-GRPO 策略，强制生成 $G/2$ 个文本模式响应和 $G/2$ 个工具模式响应，构成统一响应组：

$$\mathcal{O}(q) = \{o_i^{\mathrm{text}}\}_{i=1}^{G/2} \cup \{o_j^{\mathrm{tool}}\}_{j=1}^{G/2}$$

奖励函数为准确率奖励与格式一致性奖励之和：

$$R = R_{acc} + R_{fmt}$$

该阶段使模型在两种模式下分别获得独立强化，同时通过共享基线建立模式间的对比认知。

**Stage 3：自适应模式选择 RL（AMS-RL）**。在 Stage 2 奖励基础上引入条件工具使用奖励：

$$R = R_{acc} + R_{fmt} + \mathbb{I}(\mathrm{mode} = \mathcal{M}_{\mathrm{tool}}) \cdot R_{\mathrm{tool}}$$

工具使用奖励采用对比机制设计：

$$R_{\mathrm{tool}} = (R_{acc, i} - \bar{R}_{acc}^{\mathrm{text}}) - N_i \cdot C_{\mathrm{tool}}$$

其中 $\bar{R}_{acc}^{\mathrm{text}}$ 为文本模式平均准确率基线，$N_i$ 为工具调用次数，$C_{\mathrm{tool}} = 0.125$ 为单次工具调用成本。该设计鼓励智能体仅在工具能带来足够准确率增益时调用工具，实现效率与安全的平衡。

### 模式选择准确率评估指标

为量化自适应模式选择的质量，定义模式选择准确率（MSA）：

$$MSA = \frac{1}{N} \sum_{i=1}^{N} \mathbb{I}(m_{\mathrm{adaptive}}(q_i) = m_i^*)$$

其中 $m_{\mathrm{adaptive}}(q_i)$ 为智能体对样本 $q_i$ 的自适应模式选择，$m_i^*$ 为该样本上准确率更高的最优模式。MSA 衡量智能体能否准确判断场景复杂度并选择合适推理路径。实验表明，DriveAgent-R1 的 MSA 达到 65.30%，且随训练阶段逐步提升。

## 实验与关键发现

### 核心实验结果

**DriveAgent-R1 在主动感知与混合思维框架下，以 3B 参数量在多个基准上达到或超越顶级闭源模型 GPT-5 的水平。**

在 Drive-Internal 测试集上，DriveAgent-R1 使用视觉工具集后首帧联合准确率达到 51.34%，相比不使用工具的版本（45.27%）获得 **+6.07% 的绝对提升**，且超越 GPT-5 的 56.48%（Table 1）。在 nuScenes 跨数据集测试中，序列平均联合准确率为 **47.10%，超越 GPT-5 的 45.14%**，验证了框架的泛化能力。值得注意的是，小规模开源 VLM（Qwen2.5-VL-3B/7B）在未经专门训练的情况下使用工具反而导致性能下降（分别 -0.42% 和 -3.57%），表明有效工具使用是一项非平凡技能，需要针对性训练。


在 DriveBench 基准上，DriveAgent-R1 的感知得分达到 34.07，是 DriveLM（16.85）的两倍以上（Table 2）；行为得分 43.69 同样领先。在 nuScenes 验证集的开环规划任务中，平均位移误差（ADE）为 **0.28m**，优于 DriveVLM-Dual（0.31m）和 EMMA（0.32m）（Table 3）。配合轻量 MLP 运动规划头，模型将高层元动作序列转换为低层轨迹点，实现了端到端的可执行规划。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_r2g8TV4nJy/figures/005_Table_2.jpg]]
*Table 2: Performance Comparison on DriveBench. We compare DriveAgent-R1 with representative VLM-based driving agents*

---

### 消融分析

#### 领域对齐的因果作用

领域对齐阶段（DriveAlign-3B）通过 530K VQA 数据微调，使模型在驾驶场景视觉理解上获得 **+11.7 分的显著提升**（Table 4）。更重要的是，对齐后的模型在规划任务上表现出更强的视觉依赖性：当移除图像输入时，性能相对下降 **-15.8%**，而未对齐模型仅下降 -11.0%（Table 5）。这表明领域对齐有效缓解了 VLM 常见的“视觉忽视”问题，使模型真正将决策建立在视觉证据之上，而非依赖文本先验。

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_r2g8TV4nJy/figures/007_Table_4.jpg]]
*Table 4: Analysis of Foundational Capabilities. Overall scores on domain-specific and 8 general VLM benchmarks. Numbers in blue denote the improvement over Qwen2.5-VL-3B. Detail results are in Appendix A.9.1. Table 5: Impact of Domain Alignment on High-Level Behavioral Planning Task. We report sequence accuracy on Drive-Internaltest. The relative performance drop (%) upon removing images is shown in parentheses*

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_r2g8TV4nJy/figures/008_Table_5.jpg]]

#### 级联强化学习策略的有效性

三阶段渐进训练策略是 DriveAgent-R1 成功的关键。消融实验（Table 6）表明：

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_r2g8TV4nJy/figures/010_Table_6.jpg]]
*Table 6: Ablation on the progressive training strategy on the $\mathbf { D r i v e - I n t e r n a l _ { t e s t } }$ . We evaluate different combinations of our three training stages. To ensure fair comparison, we also test variants where a single RL stage is trained for two epochs, matching the total RL epochs of DriveAgent-R1. Figure 4: Progressive training gains on Drive-Internaltest. Accuracy in $\mathcal { M } _ { \mathrm { a d a p t i v e } }$ mode and MSA improve with each training stage

- 仅使用双模式 SFT（DM-SFT）的模型自适应准确率为 40.15%，模式选择准确率（MSA）为 56.70%。
- 加入强制对比模式 RL（FCM-RL）后，自适应准确率提升至 43.40%，MSA 提升至 60.35%。
- 完整的级联 RL（FCM-RL + AMS-RL）进一步将自适应准确率推至 **45.42%，MSA 达到 64.02%**。

相比之下，单阶段 RL 变体（仅 FCM-RL 或仅 AMS-RL 训练两轮）均无法达到级联策略的性能，验证了先强制对比后自适应选择的渐进训练逻辑的必要性。图 4 直观展示了各训练阶段在 M_adaptive 模式和 MSA 上的累积增益。

#### 主动感知 vs 被动感知

主动感知框架的核心优势在消融实验中得到了清晰验证（Table 7）：

![[assets/figures/papers/paper_list_l22_https_openreview_net_forum_id_r2g8TV4nJy/figures/011_Table_7.jpg]]
*Table 7: Ablation on Active vs. Passive Perception. We compare DriveAgent-R1 with passive baselines on Drive-Internaltest. Relative drop (%) without images in parentheses. Table 8: Performance and Efficiency Analysis. We compare inference latency and average output tokens for different perception and reasoning strategies*

- **完整工具集**（Retrieve View + RoI Inspection + Depth Estimation + 3D Object Detection）在有图像时达到 45.42% 准确率，无图像时降至 38.24%，相对下降 **-15.8%**。
- **被动前视图**（Passive-FV）有图像时 42.70%，无图像时 39.64%，相对下降仅 -7.2%。
- **被动多视图**（Passive-SV）有图像时 43.10%，无图像时 39.01%，相对下降 -9.5%。

主动感知框架下更大的“有图像 vs 无图像”性能差距，证实了模型确实在主动利用工具获取的额外视觉证据进行推理，而非仅仅依赖初始输入。同时，完整工具集的绝对性能最优，说明四种工具的协同作用超越了任何单一工具或被动多视图方案。

---

### 效率与模式选择分析

混合思维机制在效率与准确率之间实现了有效平衡（Table 8）。在自适应模式（M_adaptive）下，模型根据场景复杂度动态选择推理路径：

- 推理延迟从纯工具模式的 **7.91s 降至 6.74s**（降低约 15%）。
- 输出 token 数从 314.45 降至 265.57（降低约 16%）。

这意味着在简单场景中，模型自动切换至高效的纯文本推理，避免了不必要的工具调用开销；而在复杂场景中，则启用工具增强推理以获取关键视觉证据。模式选择准确率（MSA）达到 65.30%（Table 10），表明模型在大部分情况下能正确判断是否需要工具辅助。

---

### 失败模式与局限性

尽管 DriveAgent-R1 整体表现优异，但定性分析揭示了若干典型失败模式：

1. **对新视觉证据的过度依赖**：在复杂路口场景中，智能体可能因误解侧视图中的行人红绿灯而推翻最初正确的绿灯判断，导致不必要的刹车（Figure 16）。这表明模型在面对多源信息冲突时，缺乏辩证推理能力，倾向于机械采纳最新感知结果。

2. **复杂道路拓扑理解不足**：在需要辨析多交通信号冲突的场景中，推理可能忽略上下文语义而简单地信任工具返回的感知结果。这反映出模型对交通规则和场景语义的基础理解仍有提升空间。

3. **工具使用的双刃剑效应**：小模型（如 Qwen2.5-VL-3B/7B）在无专门训练时使用工具反而导致性能下降，说明工具的有效利用需要模型具备一定的基础视觉推理能力，否则额外的视觉信息反而成为噪声。

4. **验证范围有限**：当前仅在 nuScenes 和 Drive-Internal 两个数据集上验证，在更复杂的真实环境中（如极端天气、非结构化道路）的泛化能力仍需进一步测试。


## 定位与知识库关联

### 核心创新与范式演进

DriveAgent-R1 的核心创新在于将自动驾驶规划从**被动文本推理**推进到**主动具身视觉推理**。传统 VLM 驾驶智能体（如 **DriveLM** (Sima et al., 2024)、**Dolphins** (Ma et al., 2024)）采用被动感知范式：模型仅接收初始前视图和文本描述，通过纯文本链式思维（Text-based M-CoT）进行推理。这种范式在面对复杂场景时存在根本性瓶颈——当初始视觉信息不足以消除不确定性时，模型无法主动寻求额外证据，只能依赖不可靠的文本推断。

DriveAgent-R1 通过两项机制突破这一瓶颈：

1. **主动感知框架**：智能体在推理过程中可主动调用视觉工具集（Retrieve View、RoI Inspection、Depth Estimation、3D Object Detection），获取多视角、高分辨率、深度和 3D 检测等关键视觉证据，将决策建立在可验证的视觉信息之上。这一设计使感知从一次性输入转变为交互式、需求驱动的过程。

2. **混合思维机制**：受人类驾驶员认知模式启发，智能体根据场景复杂度自适应切换推理路径——简单场景使用高效纯文本推理（`<think_text>`），复杂场景启用工具增强视觉推理（`<think_tool>`），在安全性与计算效率之间取得平衡。

### 与基线工作的关系

在 VLM 驾驶智能体谱系中，DriveAgent-R1 与以下工作构成对比：

- **DriveLM** (Sima et al., 2024) 和 **Dolphins** (Ma et al., 2024)：代表被动感知范式，仅使用初始视图和文本推理。DriveAgent-R1 在 DriveBench 上的 Perception 分数（34.07）约为 DriveLM（16.85）的两倍，证实主动感知的显著优势。

- **GPT-5**、**GPT-4.1**、**Gemini-2.5-Flash**、**Doubao-Seed-1.6**：闭源顶级 VLM，具备强大通用推理能力但未针对主动感知设计。在 nuScenes 测试集上，DriveAgent-R1（47.10%）以仅 3B 参数量超越 GPT-5（45.14%），证明专用主动感知架构在驾驶场景中的有效性。

- **Qwen2.5-VL-3B/7B/72B** (Bai et al., 2025)：开源 VLM 基线。关键发现是，小模型（3B、7B）在未经专门训练的情况下使用工具会导致性能下降（3B: -0.42%，7B: -3.57%），表明有效工具使用是一项非平凡能力，需要针对性训练。

- **DriveVLM-Dual**、**UniAD**、**VAD-Base**：nuScenes 上的规划模型基线。DriveAgent-R1 在开环规划中取得最优平均 ADE（0.28m），优于 DriveVLM-Dual（0.31m）和 EMMA（0.32m）。

### 训练策略的独特性

DriveAgent-R1 的三阶段渐进训练策略（领域对齐 → 双模式 SFT → 级联 RL）与标准监督微调或单阶段 RL 形成鲜明对比：

- **领域对齐（DriveAlign-3B）**：通过 530K VQA 数据微调，增强驾驶视觉敏感性，缓解视觉忽视问题。消融实验证实，对齐后模型在移除图像时相对性能下降更大（-15.8% vs -11.0%），表明其决策更依赖视觉证据。

- **级联 RL（Cascaded RL）**：核心创新在于分两阶段——首先通过强制对比模式 RL（FCM-RL）分别强化文本和工具两种推理能力，然后通过自适应模式选择 RL（AMS-RL）训练模式选择器。消融实验表明，级联策略显著优于仅 SFT 或单阶段 RL 变体，自适应模式准确率（MSA）随训练逐步提升。

### 适用边界

1. **数据集范围**：当前仅在 nuScenes 和 Drive-Internal 两个数据集上验证，场景覆盖以城市道路为主，对乡村、高速、极端天气等环境的泛化能力尚需验证。

2. **模型规模**：基于 Qwen2.5-VL-3B 构建，小参数量的优势在于部署效率，但可能限制对复杂道路拓扑和交通规则的深层理解。工具使用能力与模型基础能力高度相关——小模型未经训练时工具使用反而有害。

3. **感知模态**：当前工具集限于视觉（多视角图像、深度、3D 检测），未整合 LiDAR、雷达等传感器，在多模态融合感知方面存在扩展空间。

### 已知局限与失败模式

1. **工具证据的过度依赖**：智能体可能因误解工具返回的新视觉证据而推翻初始正确判断。典型失败案例（Figure 16）显示，在复杂路口中，智能体错误识别侧视图中的人行红绿灯，导致不必要的刹车。这反映出模型在信息冲突时缺乏辩证推理能力，倾向于机械采纳最新感知结果。

2. **交通规则理解不足**：当多交通信号存在冲突时，模型可能忽略上下文语义而简单依赖最近感知结果，暴露出对复杂道路拓扑和交通规则的基础理解缺陷。

3. **工具使用的双刃剑效应**：工具调用在提升准确率的同时增加推理延迟。混合思维通过自适应模式选择将延迟从 7.91s 降至 6.74s，但仍需进一步优化以满足实时性要求。

### 开放问题

1. **冲突推理能力**：如何通过对抗性场景训练增强智能体在信息冲突时的辩证推理能力，避免对最新感知证据的盲目接受？

2. **多模态扩展**：能否将混合思维框架扩展到 LiDAR、雷达等传感器，实现更全面的多模态主动感知？

3. **动态阈值调整**：在大规模部署中，如何根据场景风险动态调整工具调用阈值，以平衡计算开销和安全性？

4. **跨域泛化**：领域对齐数据集是否可以扩展以覆盖全球多样的交通规则和场景（如左行/右行、不同交通标志体系），从而提升泛化能力？

5. **任务迁移**：该框架能否推广到其他具身智能任务（如机器人导航），并且是否需要任务特定的工具集设计？

## 原文 PDF

![[paperPDFs/ICLR_2026/DriveAgent_R1_Advancing_VLM_based_Autonomous_Driving_with_Active_Perception_and_Hybrid_Thinking.pdf]]
