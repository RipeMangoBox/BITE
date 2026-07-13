---
title: GenHSI Controllable Generation of Human Scene Interaction Videos
type: paper
paper_level: A
venue: arXiv
year: 2025
pdf_ref: paperPDFs/arxiv_2025/GenHSI_Controllable_Generation_of_Human_Scene_Interaction_Videos.pdf
project_link: null
code_link: https://github.com/
aliases:
- GCGHSIV
tags:
- arxiv_2025
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
- topic/generative_models_diffusion
core_operator: 因果关键是将复杂的HSI视频生成任务模仿真实电影制作流程分化为三个可控阶段：剧本编写阶段用VLM将复杂文本分解为原子动作；预可视化阶段在对象正则视角下利用2D修复扩散模型生成交互，并通过接触引导的3D优化提升为3D关键帧；动画阶段用3D高斯渲染和现成视频扩散模型插值关键帧。这种分解使得无训练的、身份一致的、物理合理的视频生成成为可能。
primary_logic: 核心洞察：通过将对象正则化视角和3D关键帧作为插入点，可以将显式的3D可供性与接触约束注入生成流程，从而大幅减少视频扩散模型中的空间幻觉，并在不进行任何训练的情况下维持人物身份。
claims:
- GenHSI的三阶段分解生成方法在Long-VBench评估中全面超越商业定制方案Kling AI，在主体一致性（0.985 vs 0.961）、背景一致性（0.977 vs 0.965）、运动平滑度（0.989 vs 0.986）和图像质量（0.784 vs 0.771）上均取得更优结果。
- "在对象正则视角下进行人像修复的成功率高达93.33%，而偏航角增大到(0,π/4]时降至54.67%，到(π/4,π/2]时仅剩20%，充分证明正则视角假设的有效性。"
- GenHSI的单视图修复+3D优化方案在3D人-场景交互姿态生成中，语义对齐（Semantic Clip 0.2578 vs 0.2521）和接触指标（Contact 0.984 vs 0.971）均优于多视图修复的GenZI。
- 通过消融双关键帧（DKF）与多关键帧，证明多关键帧策略能避免幻觉过渡动态，并更好地保持人物身份。
---

# GenHSI Controllable Generation of Human Scene Interaction Videos

> [!tip] 核心洞察
> 核心洞察：通过将对象正则化视角和3D关键帧作为插入点，可以将显式的3D可供性与接触约束注入生成流程，从而大幅减少视频扩散模型中的空间幻觉，并在不进行任何训练的情况下维持人物身份。

| 字段 | 内容 |
|------|------|
| 中文题名 | GenHSI：可控的人-场景交互视频生成 |
| 英文题名 | GenHSI Controllable Generation of Human Scene Interaction Videos |
| 会议/期刊 | arXiv 2025 |
| Links | [Code](https://github.com/) · [paper](https://arxiv.org/abs/2506.19840) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction #topic/generative_models_diffusion |
| Method | GenHSI |
| Dataset | Long-VBench, 3D HSI Pose Generation |

> [!tip] 效果简介
> - Long-VBench 上，Subject Consistency 0.985 vs 0.961 (+0.024)；Background Consistency 0.977 vs 0.965 (+0.012)；Motion Smoothness 0.989 vs 0.986 (+0.003)。
> - 3D HSI Pose Generation 上，Semantic Clip 0.2578 vs 0.2521 (+0.0057)；Contact 0.984 vs 0.971 (+0.013)。

## 概要

**GenHSI** 提出了一种可控的人-场景交互（HSI）视频生成框架，核心目标是解决现有视频扩散模型在生成长序列交互视频时面临的三项根本性挑战：交互动力学与可供性不真实、人物身份无法保持，以及高昂的训练或微调成本。其根本瓶颈在于模型缺乏显式的3D空间理解和可供性推理能力，导致生成结果中出现空间幻觉和物理不一致。

**核心洞察**在于：将复杂的HSI视频生成任务模仿真实电影制作流程，分解为三个可控阶段——剧本编写（Script Writing）、预可视化（Pre-visualization）和动画（Animation）。通过将对象正则化视角和3D关键帧作为插入点，GenHSI能够将显式的3D可供性与接触约束注入生成流程，从而在不进行任何训练的情况下，大幅减少空间幻觉并维持人物身份一致性。

**方法定位**上，GenHSI区别于端到端的直接视频生成范式（依赖隐式动力学建模），采用三阶段分解生成策略，通过3D关键帧提示实现对交互的精确控制。在交互姿态生成方面，GenHSI在对象正则视角下进行单视图2D修复，随后通过接触引导的3D优化提升为3D关键帧，这与多视图修复融合方案（如GenZI, Li et al., CVPR 2024）形成鲜明对比。身份保持机制则通过3D高斯化身渲染和关键帧图像提示实现，将身份保持与视频生成完全解耦，避免了传统方案中通过训练将身份嵌入模型权重的需求。

**主要结果**表明，GenHSI在Long-VBench评估中全面超越商业定制方案Kling AI Elements：主体一致性（0.985 vs 0.961）、背景一致性（0.977 vs 0.965）、运动平滑度（0.989 vs 0.986）和图像质量（0.784 vs 0.771）均取得更优结果（Table 3）。在3D人-场景交互姿态生成中，GenHSI的单视图修复+3D优化方案在语义对齐（Semantic Clip 0.2578 vs 0.2521）和接触指标（Contact 0.984 vs 0.971）上均优于多视图修复的GenZI（Table 2）。关键消融实验证实，对象正则视角下的修复成功率高达93.33%，而偏航角增大至(0, π/4]时降至54.67%，至(π/4, π/2]时仅剩20%（Table 1），充分验证了正则视角假设的有效性。多关键帧策略相比双关键帧方案，能显著减少身份变化和幻觉动态（Figure 6）。

**局限性与开放问题**方面，GenHSI在非正则视角下的交互生成能力急剧下降，Avatar渲染存在塑料质感需后处理改善，人物尺度可能不合理，且视频生成环节依赖商业API（Kling AI 1.6）限制了完全可复现性。未来方向包括设计视角自适应的修复策略、在3D化身生成阶段直接融入光照一致性约束，以及将框架泛化到多人-多物体交互等复杂场景。

### 问题背景：人-场景交互视频生成的挑战

生成逼真、可控的人-场景交互（Human-Scene Interaction, HSI）视频是计算机视觉与图形学的前沿课题。这类视频不仅要求人物与场景物体发生物理上合理的接触与交互（如“坐在椅子上”、“拿起桌上的杯子”），还需要在长序列中保持人物身份一致、运动平滑，并对用户的复杂文本指令做出精确响应。

然而，现有视频扩散模型在生成长序列HSI视频时面临三项核心挑战：

1. **交互动力学与可供性不真实**：模型缺乏显式的3D空间理解和可供性（affordance）推理能力，难以将文本指令与精确的几何约束对齐，导致生成结果中出现“空间幻觉”——人物悬浮、穿透物体、或与物体产生不符合物理规律的交互姿态。
2. **人物身份无法保持**：在长视频生成过程中，人物外貌、衣着、体型等身份特征容易发生漂移或突变，这一问题的根本原因在于现有方法将身份信息隐式地嵌入模型权重，缺乏显式的身份锚定机制。
3. **需要昂贵的训练或微调**：为特定人物定制视频生成通常需要大量数据和计算资源进行微调，难以实现零样本（zero-shot）的个性化生成。

### 现有方法的不足

当前HSI视频生成方法可大致分为两类范式，但各自存在根本性缺陷：

- **端到端直接视频生成**：如商业定制方案Kling AI Elements，直接根据文本提示生成完整视频。这类方法依赖隐式动力学建模，缺乏对3D空间关系和物理接触的显式约束，导致交互姿态失真、物体可供性幻觉等问题。在Long-VBench基准上，其主体一致性仅0.961，背景一致性0.965，图像质量0.771（Table 3），均存在明显提升空间。

- **3D交互姿态生成方法**：如GenZI（Li et al., CVPR 2024）采用多视图2D修复加融合的策略生成3D人-场景交互姿态，而COINS（Zhao et al., ECCV 2022）依赖精确的3D场景几何进行穿透和接触约束。前者面临多视图修复不一致导致姿态不适的困境（如Figure 9所示，GenZI在“躺下”和“坐在桌上”场景中产生不自然姿态），后者则要求完整且精确的场景重建，在实际应用中受限。

### 根本瓶颈与因果关键

**根本瓶颈**在于：现有方法缺乏将文本指令与精确3D几何约束对齐的机制。视频扩散模型的隐空间表征天然缺乏显式的3D空间理解和可供性推理能力，导致生成结果中交互的物理合理性与文本语义之间存在鸿沟。

**因果关键**是将复杂的HSI视频生成任务模仿真实电影制作流程分化为三个可控阶段：

- **剧本编写阶段**：用视觉语言模型（VLM）将复杂文本分解为原子交互动作与状态转移，将高层语义转化为可执行的交互原语；
- **预可视化阶段**：在对象正则视角下利用2D修复扩散模型生成交互图像，并通过接触引导的3D优化提升为3D关键帧，显式注入可供性与接触约束；
- **动画阶段**：用3D高斯渲染和现成视频扩散模型插值关键帧，将身份保持与视频生成解耦。

这一分解使得**无训练的、身份一致的、物理合理的视频生成成为可能**——核心洞察在于：通过将对象正则化视角和3D关键帧作为插入点，可以将显式的3D可供性与接触约束注入生成流程，从而大幅减少视频扩散模型中的空间幻觉，并在不进行任何训练的情况下维持人物身份。

### 本文动机

基于上述分析，本文提出GenHSI——一个3D感知的可控人-场景交互视频生成框架。GenHSI的核心设计理念是：**不试图在一个端到端模型中隐式地学习所有HSI生成能力，而是将问题分解为语义理解、3D交互生成和视频合成三个相对独立的子问题，并在每个阶段引入适当的先验与约束**。这一设计既规避了昂贵训练的依赖，又为交互的物理合理性和身份一致性提供了可解释的保障。

## 核心方法与创新机理

GenHSI 的核心创新在于将人-场景交互（HSI）视频生成这一复杂任务**分解为三个可控阶段**，模仿真实电影制作流程——剧本编写、预可视化与动画——从而**在不进行任何训练或微调**的前提下，实现了身份一致、物理合理的长序列视频生成。这一范式转换的根本动机在于：现有视频扩散模型缺乏显式的 3D 空间理解与可供性推理能力，难以将文本指令与精确的几何约束对齐，导致生成结果中出现空间幻觉和物理不一致。

### 关键 changed slots

**1. 视频生成范式：从端到端隐式生成到三阶段 3D 关键帧提示控制**

现有方法（包括商业定制方案 **Kling AI Elements**）依赖端到端视频扩散模型隐式地建模交互动力学，缺乏对 3D 空间关系和接触约束的显式控制。GenHSI 将其替换为：

- **剧本编写阶段**：利用 VLM 将复杂文本指令分解为原子交互动作与状态转移，识别场景中可交互物体并推理接触部位；
- **预可视化阶段**：在对象正则视角下生成 2D 人-物交互图像，并通过接触引导的 3D 优化将其提升为 3D 关键帧；
- **动画阶段**：使用 3D 高斯场景与化身渲染关键帧，并利用现成视频扩散模型进行关键帧插值。

这一分解使得 **3D 关键帧成为显式的控制插入点**，将 3D 可供性与接触约束注入生成流程，从而大幅减少空间幻觉。

**2. 交互姿态生成视角：从多视图修复到对象正则视角下的单视图修复+3D 优化**

零样本 3D 人-场景交互方法 **GenZI**（Li et al., CVPR 2024）采用在多个随机视图下进行 2D 修复并融合的策略，但面临多视图不一致和修复质量随视角变化剧烈下降的问题。GenHSI 的关键洞察是：**2D 扩散模型修复人-物交互的性能高度依赖于视角**——在对象正则视角（偏航角 ≤0°）下修复成功率达 93.33%，而当偏航角增大到 (π/4, π/2] 时骤降至仅 20%（Table 1）。基于此，GenHSI 仅在正则视角下进行单视图修复，然后通过 3D 优化将 2D 交互提升为 3D 一致的姿态，在语义对齐（Semantic Clip 0.2578 vs 0.2521）和接触指标（Contact 0.984 vs 0.971）上均超越 GenZI 的多视图方案（Table 2）。

**3. 3D 交互约束融入方式：从依赖精确几何到 VLM 推断+稳健优化**

组合式人-场景交互合成方法 **COINS**（Zhao et al., ECCV 2022）依赖精确的 3D 场景几何进行穿透和接触约束。GenHSI 则通过 VLM 推理接触部位，联合三项损失函数优化人物位姿：

- **交互可供性损失** $\mathcal{L}_{hoi}$：约束 VLM 识别的接触区域点对之间的 Chamfer 距离，确保人体与物体在指定部位真实接触（Eq. 5）；
- **穿透损失** $\mathcal{L}_{pen}$：通过惩罚物体顶点进入人体网格（SDF 值为负）来避免穿透（Eq. 6）；
- **轮廓 IoU 损失** $\mathcal{L}_{mask}$：通过投影掩码的交并比间接约束人体尺度与位置（Eq. 7）。

该优化框架不要求精确的场景几何，在场景重建不完整时仍能生成合理的交互姿态（Figure 9），体现了更强的鲁棒性。

**4. 身份保持机制：从训练嵌入到 3D 高斯化身渲染解耦**

现有方法通常需要通过训练或微调将人物身份嵌入模型权重。GenHSI 将身份保持与视频生成完全解耦：通过 3D 高斯化身渲染生成身份一致的关键帧图像，再以关键帧图像提示的方式驱动现成视频扩散模型进行插值。消融实验表明，多关键帧策略（利用每个交互动作生成独立关键帧）相比仅用开始和结束两个关键帧（DKF），能显著减少身份变化和幻觉过渡动态（Figure 6）。在 Long-VBench 评估中，GenHSI 的主体一致性达到 0.985，超越商业定制方案 Kling AI 的 0.961（Table 3）。

### 创新本质总结

GenHSI 的核心洞察在于：**将对象正则化视角和 3D 关键帧作为显式插入点，可以将 3D 可供性与接触约束注入生成流程**。这一设计使得无训练的、身份一致的、物理合理的视频生成成为可能，其成功的关键在于正确识别了 2D 扩散模型的视角依赖性，并利用 3D 优化桥接了 2D 修复与 3D 一致性之间的鸿沟。

GenHSI 的核心设计思想是将复杂的人-场景交互（HSI）视频生成任务模仿真实电影制作流程，分化为三个可控阶段：**剧本编写（Script Writing）、预可视化（Pre-visualization）和动画（Animation）**。这一分解的因果动机源于现有视频扩散模型在生成长序列交互视频时的根本瓶颈——模型缺乏显式的3D空间理解和可供性推理，难以将文本指令与精确的几何约束对齐，导致空间幻觉和物理不一致。通过将3D关键帧作为中间表示插入生成流程，GenHSI 在不进行任何训练的前提下，将显式的3D可供性与接触约束注入扩散模型的生成过程，从而大幅减少空间幻觉并维持人物身份。

### 三阶段流水线

整体管道的输入包括场景图像、角色图像以及描述交互链的文本提示，输出为一段可扩展长度的HSI视频。三个阶段的职责与数据流如下：

1. **剧本编写阶段**：接收用户提供的高阶文本描述和场景图像，利用视觉语言模型（VLM）识别场景中可供交互的物体，并将复杂文本分解为原子交互动作（interactive actions）与状态转移（state transitions），生成结构化的动作脚本。该脚本定义了后续关键帧的语义内容与时序关系。

2. **预可视化阶段**：以动作脚本为指导，在对象正则视角（canonical view）下利用预训练的2D修复扩散模型生成人-物交互图像，随后通过接触引导的3D优化将2D交互提升为3D一致的关键帧。每个关键帧包含经过尺度、平移和全局旋转优化后的人体网格与3D场景物体的空间组合。

3. **动画阶段**：使用3D高斯场景和3D高斯化身渲染预可视化阶段生成的多个3D关键帧，然后利用现成的视频扩散模型（Kling AI）对这些关键帧进行插值，生成连续且身份一致的HSI视频。关键帧作为图像提示引导扩散模型的生成过程，将身份保持与视频生成解耦。

### 模块关系与因果机制

三个阶段的协作逻辑遵循“语义分解→空间推理→时序合成”的因果链条：

- **剧本编写**解决“做什么”的问题：VLM的链式推理将模糊的高阶指令转化为明确的原子动作序列，为后续阶段提供精确的语义锚点。
- **预可视化**解决“在哪里、怎么做”的问题：对象正则视角的选择是因果关键——实验表明，在该视角下修复成功率高达93.33%，而偏航角增大至$(0,\pi/4]$时降至54.67%，至$(\pi/4,\pi/2]$时仅剩20%（Table 1）。这证明了正则视角假设对减少扩散模型空间幻觉的决定性作用。接触引导的3D优化通过联合交互损失$\mathcal{L}_{hoi}$、穿透损失$\mathcal{L}_{pen}$和轮廓损失$\mathcal{L}_{mask}$（式8），在不依赖精确场景几何的条件下实现物理合理的3D交互姿态。
- **动画**解决“如何动”的问题：多关键帧策略（而非仅使用起始和结束的双关键帧DKF）是避免幻觉过渡动态和保持人物身份的关键——消融实验证实DKF方案会导致身份变化和不合理过渡（Figure 6）。

### 关键设计决策的因果逻辑

GenHSI 的免训练特性源于将3D推理与视频生成解耦的架构选择：3D关键帧在预可视化阶段通过优化显式建模空间关系，视频扩散模型仅负责时序插值，无需学习隐式的物理约束。这一设计使得方法可以灵活替换底层生成模型（当前使用Kling AI 1.6），但也意味着视频生成的多样性与可控性受限于API能力。此外，方法假设场景中存在可分割的交互对象，对于极简场景或复杂多对象情形，对象检测与分割的精度将成为上游瓶颈。

![[assets/figures/papers/paper_list_l1682_GenHSI_Controllable_Generation_of_Human_Scene_Interaction_Videos/figures/001_Figure_1.jpg]]
*Figure 1: GenHSI is a 3D-aware controllable human-scene interaction (HSI) video generation method. We mimic the real-world filmmaking procedure, i.e., Script Writing, Previsualization, and Animation, to generate an extendable HSI video clip with arbitrary lengths of action chains. Given images of the scene and character with the action sequence prompt, our method will render multiple 3D-aware keyframes based on the posed 3D Gaussian avatar and 3D Gaussian scene. Finally, we interpolate them into a continuous video using the pretrained video diffusion model. The frames with colored borders are selected 3D-aware keyframes that map to the color human meshes*

GenHSI 将人-场景交互（HSI）视频生成任务分解为三个核心模块：**剧本编写**（Script Writing）、**预可视化**（Pre-visualization）和**动画**（Animation）。其中，预可视化阶段是技术创新的核心，包含对象正则视角下的 2D 修复和接触引导的 3D 姿态提升两个关键子模块。

### 3.1 剧本编写模块

该模块负责将用户输入的高阶复杂文本描述转化为结构化的原子动作序列。具体流程为：首先利用 VLM 识别场景中可交互的物体并进行分割；然后在场景图像上下文中，将文本描述解析为两类原子任务——**交互动作**（描述人-物物理交互）和**状态转移**（不改变交互关系的身体运动）。这一分解为后续的 3D 关键帧生成提供了明确的时序规划。

### 3.2 对象正则视角下的 2D 修复

预可视化的第一步是在物体的**正则视角**（canonical view）下生成人-物交互的 2D 图像。GenHSI 采用预训练的 2D 修复扩散模型，通过渐进式掩膜更新策略实现这一目标。其核心公式如下：

**干净隐变量预测**（Tweedie 公式）：

$$\mathbf{z}_{0 \mid t} = \frac{\mathbf{z}_{t} - \sqrt{1 - \bar{\alpha}_{t}} \epsilon_{\Theta}(\mathbf{z}_{t}, \mathbf{z}_{0}^{*}, m_{t}, c, t)}{\sqrt{\bar{\alpha}_{t}}}$$

其中，$\mathbf{z}_{t}$ 为当前时间步 $t$ 的噪声隐变量，$\mathbf{z}_{0}^{*}$ 为原始物体图像的隐变量，$m_{t}$ 为当前修复掩码，$c$ 为文本提示，$\epsilon_{\Theta}$ 为扩散模型的噪声预测网络。该公式从噪声观测中预测干净的初始隐变量 $\mathbf{z}_{0 \mid t}$。

**人体掩码更新**：

$$m_{t-1} = \mathrm{Segment}(\mathrm{Decode}(\hat{\mathbf{z}}_{0 \mid t}))$$

将预测的干净隐变量解码为图像后，通过分割获取人体区域掩码 $m_{t-1}$，作为下一次去噪步骤的修复掩码。

**隐变量混合**：

$$\hat{\mathbf{z}}_{0 \mid t} = \left(1 - \downarrow m_{t-1}\right) \odot \mathbf{z}_{0}^{*} + \downarrow m_{t-1} \odot \mathbf{z}_{0 \mid t}$$

以更新后的掩码为权重，将原始物体隐变量与预测的干净隐变量进行混合，生成中间潜在表示 $\hat{\mathbf{z}}_{0 \mid t}$。

**去噪推进**：

$$\mathbf{z}_{t-1} = \sqrt{\bar{\alpha}_{t}} \hat{\mathbf{z}}_{0 \mid t} + \sqrt{1 - \bar{\alpha}_{t}} \epsilon$$

利用混合隐变量执行一步去噪，得到 $t-1$ 时刻的噪声隐变量，完成一次迭代。

这一渐进式修复策略的关键在于：随着去噪进行，人体掩码不断细化，使得模型能够逐步生成与物体空间关系合理的交互姿态。实验表明，在对象正则视角下修复的成功率高达 **93.33%**，而当偏航角增大到 $(0, \pi/4]$ 时降至 **54.67%**，到 $(\pi/4, \pi/2]$ 时仅剩 **20%**（Table 1），有力证明了正则视角假设的必要性。

### 3.3 接触引导的 3D 姿态提升

2D 修复结果缺乏精确的 3D 空间信息，GenHSI 通过一个优化框架将 2D 交互姿态提升为 3D 一致的关键帧。优化变量为人体的**尺度** $s_h$、**平移** $t_h$ 和**全局旋转** $r_h$，目标是最小化以下联合损失函数：

$$\mathcal{L}_{total} = \mathcal{L}_{hoi} + \mathcal{L}_{pen} + \mathcal{L}_{mask}$$

**交互可供性损失** $\mathcal{L}_{hoi}$：

$$\mathcal{L}_{hoi} = \sum_{x \in P_h^*} \min_{y \in P_o^*} \|x - y\|_2^2 + \sum_{y \in P_o^*} \min_{x \in P_h^*} \|y - x\|_2^2$$

其中 $P_h^*$ 和 $P_o^*$ 分别为 VLM 推理出的人体和物体接触区域点集。该损失通过双向倒角距离约束接触部位在 3D 空间中真实贴合。

**穿透损失** $\mathcal{L}_{pen}$：

$$\mathcal{L}_{pen} = -\mathbb{E}_{v \in \mathcal{M}_O}[\min(\Phi(v), 0)]$$

其中 $\mathcal{M}_O$ 为物体网格顶点集，$\Phi(v)$ 为顶点 $v$ 在人体网格 SDF 中的值。该损失惩罚物体顶点进入人体内部（SDF 为负）的情况，确保物理合理性。

**轮廓 IoU 掩码损失** $\mathcal{L}_{mask}$：

$$\mathcal{L}_{mask} = \frac{m_h \cap m_h^{init}}{m_h \cup m_h^{init}} + \frac{m_{hoi} \cap m_{hoi}^*}{m_{hoi} \cup m_{hoi}^*}$$

其中 $m_h$ 为投影人体掩码，$m_h^{init}$ 为初始掩码，$m_{hoi}$ 为考虑物体遮挡后的掩码，$m_{hoi}^*$ 为修复掩码。该损失通过两个交并比项间接约束人体的尺度与位置。

对于无接触交互（如“站在椅子旁”），$\mathcal{L}_{hoi}$ 退化为距离惩罚：

$$\mathcal{L}_{hoi} = \left\{ \begin{array}{ll} 0, & d_{HO} \leq \delta \\ d_{HO} - \delta, & d_{HO} > \delta \end{array} \right.$$

其中 $d_{HO}$ 为人-物距离，阈值 $\delta = 10\text{cm}$。当距离超过阈值时施加惩罚，以维持空间邻近性。

这一优化框架的核心优势在于：**不依赖精确的 3D 场景几何**，而是通过 VLM 推理的接触线索和扩散先验的语义信息联合约束姿态。实验表明，GenHSI 的单视图修复 + 3D 优化方案在语义对齐（Semantic Clip **0.2578** vs 0.2521）和接触指标（Contact **0.984** vs 0.971）上均优于多视图修复的 **GenZI**（Li et al., CVPR 2024），且避免了多视图不一致问题（Table 2）。

### 3.4 动画模块

动画阶段将优化后的 3D 关键帧作为条件输入，利用 3D 高斯场景和化身渲染多视角关键帧图像，再通过现成的视频扩散模型（Kling AI）进行关键帧插值，生成连续视频。由于关键帧本身已包含正确的 3D 交互约束和人物身份信息，视频生成过程无需任何训练或微调即可保持身份一致性和物理合理性。

![[assets/figures/papers/paper_list_l1682_GenHSI_Controllable_Generation_of_Human_Scene_Interaction_Videos/figures/002_Figure_2.jpg]]
*Figure 2: Script Writing Stage: Complex high-level text descriptions from users do not provide a detailed scene and task understanding for the desired long video generation. The script writing stage first identifies and segments objects that the human can interact with in the scene. These objects, along with the given human prompt, are used to perform text-based motion planning from a VLM [56] that provides us with interactive actions & state transitions for keyframing in the Pre-Visualization Stage*

![[assets/figures/papers/paper_list_l1682_GenHSI_Controllable_Generation_of_Human_Scene_Interaction_Videos/figures/003_Figure_3.jpg]]
*Figure 3: 3D Keyframe Generation for Pre-visualization. GenHSI synthesizes 3D human-scene interaction pose based on the pretrained 2D image inpainting diffusion model to create a 3D keyframe as an intermediate step for HSI video generation. Our method lifts the 2D human inpainting result in the canonical view of the target object based on contact cues reasoned by the VLM chain-of-though*

## 实验与关键发现

### 核心定量结果

GenHSI 在 Long‑VBench 基准上全面超越商业视频定制方案 **Kling AI Elements**，验证了三阶段分解生成范式的有效性。如 Table 3 所示，GenHSI 在主体一致性（0.985 vs 0.961）、背景一致性（0.977 vs 0.965）、运动平滑度（0.989 vs 0.986）和图像质量（0.784 vs 0.771）四项核心指标上均取得领先。这一优势的因果根源在于：3D 关键帧提示将显式的空间约束注入视频扩散模型，大幅减少了端到端生成中常见的空间幻觉与身份漂移。

![[assets/figures/papers/paper_list_l1682_GenHSI_Controllable_Generation_of_Human_Scene_Interaction_Videos/figures/007_Table_3.jpg]]
*Table 3: Long-VBench Video Quality [32] GenHSI beats commercial video customization solution across major metrics, but shows lower Dynamic Degree as the consistent background does not contribute to the optical flow used in the evaluation. GenHSI (DKF) - dual key frame improves over commercial model, but increasing keyframes in GenHSI (Ours) improves consistency, subject identity, motion smoothness, and image quality*

值得注意的是，GenHSI 在动态程度（Dynamic Degree）指标上得分偏低。这并非质量缺陷，而是评估机制的内在偏差——高度一致的静态背景不产生显著光流，而该指标恰恰依赖光流贡献进行度量。因此，该指标的落后反而从侧面印证了方法在背景一致性上的优势。

在 3D 人‑场景交互姿态生成子任务上，GenHSI 的单视图修复 + 3D 优化方案同样展现出竞争力。Table 2 显示，GenHSI 在语义对齐（Semantic Clip 0.2578 vs 0.2521）和接触精度（Contact 0.984 vs 0.971）上均优于多视图修复的 **GenZI**（Li et al., CVPR 2024）。这表明单视图正则修复配合接触引导优化，不仅能避免多视图不一致问题，还能生成更精确的物理接触。

![[assets/figures/papers/paper_list_l1682_GenHSI_Controllable_Generation_of_Human_Scene_Interaction_Videos/figures/009_Table_2.jpg]]
*Table 2: 3D HSI Pose Generation “SV” means only inpaint single view. “MV” means inpaint multiple views*

### 消融实验与关键设计验证

**正则视角的必要性。** Table 1 的视角消融实验揭示了 2D 修复扩散模型强烈的视角依赖性：在对象正则视角（偏航角 Δθ = 0）下，人像修复成功率高达 93.33%；当偏航角增大到 (0, π/4] 区间，成功率骤降至 54.67%；而在 (π/4, π/2] 区间，成功率仅剩 20%。Figure 4 的失败案例直观展示了非正则视角下的典型失效模式——幻觉可供性（Hallucinate Affordance）与不合理交互（Implausible Interaction）。这一组消融强有力地证明：正则视角假设是 GenHSI 将 2D 扩散先验可靠地转化为 3D 交互姿态的核心前提。

**多关键帧 vs 双关键帧。** Figure 6 的定性消融对比了完整 GenHSI（多关键帧）与 GenHSI (DKF)（仅使用起始和结束两个关键帧）。结果显示，双关键帧策略会导致严重的身份变化和幻觉过渡动态，而多关键帧策略——即对每个原子交互动作生成独立关键帧——能有效保持人物身份并产生物理合理的运动过渡。这验证了“密集关键帧提示”是抑制视频扩散模型动态幻觉的关键机制。

**后处理 Harmonization。** Figure 7 展示了 harmonization 后处理对生成质量的改善效果。消融表明，该步骤能显著减轻 avatar 渲染中常见的“塑料感”外观，使合成人物更好地融入场景光照环境。但需注意，这仍属于后处理补救措施，并未从根本上解决 3D 化身与场景之间的光照不一致问题。

### 失败模式与局限性

1. **视角依赖性瓶颈。** 当修复视角偏离对象正则视角时，成功率从 93% 急剧下降至 20% 以下。这限制了非正面视角交互的生成能力，是当前框架最显著的脆弱点。
2. **人物尺度不一致。** 生成视频中人物尺度偶尔出现不合理现象，根源在于 2D 修复模型未能完全对齐 3D 空间尺度，而 3D 优化环节对此的校正能力有限。
3. **Avatar 渲染质感。** 尽管 harmonization 可改善外观，avatar 仍可能呈现不自然的渲染质感，表明光照一致性约束需要更早地融入生成流程。
4. **动态程度评估偏差。** 如前述，Long‑VBench 的动态程度指标对静态背景不敏感，导致 GenHSI 在该项得分偏低，但这反映的是评估方式的局限而非方法缺陷。
5. **外部依赖与可复现性。** 视频生成环节依赖商业 API（Kling AI 1.6），其内部模型细节不可控，可能影响结果的完全可复现性。3D 场景重建采用单视图估计（MoGe、Trellis），在复杂遮挡或无纹理区域可能不够精确，但方法通过对象正则化和稳健优化缓解了这一问题。

### 方法对比与定位

在 3D 人‑场景交互生成领域，GenHSI 与两类代表性方法形成差异化：相较于依赖精确 3D 场景几何进行穿透约束的 **COINS**（Zhao et al., ECCV 2022），GenHSI 通过 VLM 推断接触部位并以联合损失（$\mathcal{L}_{total} = \mathcal{L}_{hoi} + \mathcal{L}_{pen} + \mathcal{L}_{mask}$）隐式处理几何约束，降低了对场景重建精度的要求；相较于多视图修复融合的 **GenZI**，GenHSI 的单视图正则修复策略在接触精度上更优，且避免了多视图不一致导致的姿态扭曲（如 Figure 9 所示，GenZI 在“躺下”和“坐在桌上”等场景中产生不自然的扭曲姿态）。在视频生成层面，与端到端的 Kling AI Elements 定制方案相比，GenHSI 通过 3D 关键帧提示实现了免训练的身份保持和物理一致性，但动态多样性受限于 API 能力。

![[assets/figures/papers/paper_list_l1682_GenHSI_Controllable_Generation_of_Human_Scene_Interaction_Videos/figures/012_Figure_9.jpg]]
*Figure 9: 3D Human-Object Interactions GenHSI performs improved human object interactions even when we don’t have access to accurate scene geometry. Our work also produces more plausible poses for lying, sitting, and standing. Prior works like GenZI have inconsistent multiview inpainting resulting in diverse but uncomfortable human poses as seen in lying down and sitting on table*

## 定位与知识库关联

### 1. 方法定位与因果机制

GenHSI的核心创新在于将复杂的人-场景交互（HSI）视频生成任务分解为可解释的三阶段管道——**剧本编写（Script Writing）→ 预可视化（Pre-visualization）→ 动画（Animation）**，模仿真实电影制作流程。这一分解并非简单的工程流水线，而是引入了两个关键的因果插入点：

1. **对象正则视角（Canonical View）作为2D修复的前提**：通过在对象的正则视角下进行单视图2D修复，而非在多视图下进行修复与融合，GenHSI将2D扩散先验的生成能力约束在几何最可预测的视角。实验表明，在正则视角下修复成功率达93.33%，而偏航角增大到$(0, \pi/4]$时降至54.67%，到$(\pi/4, \pi/2]$时仅剩20%（Table 1），证明视角选择是交互可供性生成的关键因果杠杆。

2. **3D关键帧作为视频扩散模型的提示**：GenHSI不直接要求视频扩散模型理解3D几何或物理约束，而是将3D关键帧渲染为图像提示输入现成的视频扩散模型进行插值。这使得身份保持与3D几何约束完全与视频生成解耦，实现了免训练的身份一致性视频生成。

### 2. 与基线方法的关系

#### 2.1 与端到端视频生成方案的对比

**Kling AI Elements**（商业视频定制解决方案）代表了端到端视频生成的范式。GenHSI在Long-VBench上全面超越Kling AI Elements：主体一致性（0.985 vs 0.961）、背景一致性（0.977 vs 0.965）、运动平滑度（0.989 vs 0.986）和图像质量（0.784 vs 0.771）（Table 3）。然而，GenHSI在动态程度（Dynamic Degree）指标上得分偏低，这不是质量缺陷，而是评估方式对静态背景不敏感的公平性偏差——高度一致的背景不产生显著光流。

GenHSI相对于端到端方案的根本优势在于**可控性与物理合理性**：端到端模型依赖隐式动力学建模，容易产生空间幻觉和物理不一致；GenHSI通过3D关键帧显式注入接触约束和空间关系，大幅减少了这类幻觉。

#### 2.2 与3D人-场景交互生成方法的对比

**GenZI**（Li et al., CVPR 2024）是零样本3D人-场景交互生成的代表性方法，采用多视图修复（MV）策略。GenHSI的单视图修复+3D优化方案（SV）在语义对齐（Semantic Clip 0.2578 vs 0.2521）和接触指标（Contact 0.984 vs 0.971）上均优于GenZI（Table 2）。根本原因在于：多视图修复容易产生视图间不一致的修复结果，导致3D融合后的姿态不舒适或不合理（如Figure 9所示的“躺下”和“坐在桌上”场景）；而单视图正则视角修复避免了多视图不一致问题，并通过接触引导的3D优化显式约束了物理合理性。

**COINS**（Zhao et al., ECCV 2022）是组合式人-场景交互合成方法，依赖精确的3D场景几何进行穿透和接触约束。GenHSI的区别在于：不要求精确的场景几何，而是使用VLM推断接触部位，联合交互损失（$\mathcal{L}_{hoi}$）、穿透损失（$\mathcal{L}_{pen}$）和轮廓损失（$\mathcal{L}_{mask}$）优化人物位姿（Eq. 8）。这使GenHSI在场景几何不完整或由单视图估计（如MoGe、Trellis）的情况下仍能生成合理的交互（Figure 9）。

#### 2.3 与2D图像修复工具的对比

**Flex**（2D图像修复工具）用于对比关键帧创建效率与质量。GenHSI的2D修复模块在对象正则视角下通过渐进式掩膜更新（Eq. 1-4）生成人-物交互图像，核心优势在于利用Tweedie公式预测干净隐变量，并通过分割更新掩膜实现迭代优化（Figure 5），而非一次性修复。

### 3. 适用边界

GenHSI的适用边界由以下假设和约束定义：

- **对象可分割假设**：方法假设场景中存在可分割的交互对象，VLM能够识别并分割这些对象。对于极简场景（无明确交互对象）或复杂多对象情形，对象检测与分割可能面临挑战。
- **正则视角可获取假设**：2D修复的成功率高度依赖对象正则视角的可获取性。当修复视角偏离正则视角超过$\pi/4$时，成功率降至20%以下（Table 1），限制了非正面视角的交互生成能力。
- **视频生成API依赖**：动画阶段依赖商业扩散模型（Kling AI 1.6），其内部模型细节不可控，动态生成的多样性与可控性受限于API能力，可能影响结果的完全可复现性。
- **3D场景重建精度**：3D场景重建采用单视图估计（MoGe、Trellis），在复杂遮挡或无纹理区域可能不够精确，但方法通过对象正则化和稳健优化缓解了这一问题。
- **光照一致性**：Avatar渲染有时呈现“塑料”质感，尽管后处理harmonization可改善（Figure 7），但仍属于后处理步骤，未从根本上解决光照不一致问题。
- **人物尺度合理性**：人物在生成视频中的尺度可能不合理，源于2D修复模型未完全对齐3D空间尺度。

### 4. 局限与开放问题

#### 4.1 已知局限

1. **视角敏感性**：当修复视角偏离对象正则视角时，成功率急剧下降（从93%降至20%以下），限制了非正面视角的交互生成能力。
2. **光照不一致**：Avatar与场景的照明不一致现象通过后处理harmonization得到改善，但未完全消除。
3. **尺度未对齐**：人物在生成视频中的尺度可能不合理，源于2D修复模型未完全对齐3D空间尺度。
4. **API依赖**：视频生成环节依赖商业扩散模型，其动态生成的多样性与可控性受限于API能力。
5. **动态程度评估偏差**：在Long-VBench动态程度指标上得分偏低，因为高度一致的背景不产生显著光流，评估衡量方式对此不敏感。
6. **对象检测挑战**：方法假设场景中存在可分割的交互对象，对于极简场景或复杂多对象情形可能面临对象检测与分割的挑战。

#### 4.2 开放问题

1. **视角自适应修复策略**：能否设计视角自适应的修复策略，使非正则视角下的交互生成成功率也能达到接近正则视角的水平？
2. **光照一致性约束**：如何在3D化身生成阶段直接融入光照一致性约束，以避免后处理harmonization步骤？
3. **多人-多物体交互扩展**：是否能将正则视角修复与3D提升的思想扩展到多人-多物体交互的复杂场景？
4. **细粒度运动控制**：在保持背景一致性的前提下，如何通过更细粒度的运动控制提升生成视频的动态程度？
5. **角色泛化**：GenHSI的框架是否可泛化到其他类型的角色（如动物、机器人）与环境的交互生成？
6. **可训练模块替换**：能否用可训练的轻量级模块替换部分启发式步骤（如视角选择、接触点推理），以进一步提升交互精度与效率？

### 5. 知识库贡献

GenHSI在以下方面为领域知识库做出贡献：

- **三阶段分解范式**：将HSI视频生成分解为剧本编写、预可视化和动画，为复杂交互视频生成提供了可解释、可控的框架。
- **对象正则视角假设**：通过实验验证了2D扩散模型在对象正则视角下修复成功率最高（93.33%），为交互生成提供了视角选择的经验依据。
- **接触引导的3D优化**：提出联合交互、穿透和轮廓损失的优化框架，在不依赖精确场景几何的情况下实现物理合理的3D交互姿态生成。
- **免训练身份保持**：通过3D关键帧提示将身份保持与视频生成解耦，为个性化视频生成提供了免训练方案。
- **Long-VBench基准结果**：在主体一致性、背景一致性、运动平滑度和图像质量上超越商业定制方案，为领域设立了新的性能参考。

## 原文 PDF

![[paperPDFs/arxiv_2025/GenHSI_Controllable_Generation_of_Human_Scene_Interaction_Videos.pdf]]
