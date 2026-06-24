---
title: "Thinking with Drafts: Speculative Temporal Reasoning for Efficient Long Video Understanding"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/Thinking_with_Drafts_Speculative_Temporal_Reasoning_for_Efficient_Long_Video_Understanding.pdf
project_link: null
code_link: null
aliases:
- TDSTRELVU
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 将时间感知与推理解耦，引入轻量级草案MLLM专门负责密集帧探索与关键帧选择，而目标MLLM仅需处理稀疏代表帧，从而大幅减少视觉token数量与上下文长度。
primary_logic: 借鉴人脑双系统协作机制，采用双模型推测-验证协同设计：小模型快速推测信息丰富的关键帧，大模型专注于高质量时序推理与验证，在保持推理质量的同时显著加速长视频理解。
claims:
- 在Qwen2.5-VL-7B上观察到视觉token注意力呈现长尾分布，超过90%的token注意力分数低于10^-3。
- SpecTemp在13.7帧时即超越Qwen2.5-VL-7B（16帧），延迟从2.1秒降至1.8秒。
- SpecTemp在58.1帧时精度超越VideoChat-R1.5，速度提升23%。
- TempCompass 上 准确率 (%) = 75.3 (13.7帧) / 77.2 (47.6帧)
---

# Thinking with Drafts: Speculative Temporal Reasoning for Efficient Long Video Understanding

> [!tip] 核心洞察
> 借鉴人脑双系统协作机制，采用双模型推测-验证协同设计：小模型快速推测信息丰富的关键帧，大模型专注于高质量时序推理与验证，在保持推理质量的同时显著加速长视频理解。

| 字段 | 内容 |
|------|------|
| 中文题名 | 草稿思考：面向高效长视频理解的推测性时序推理 |
| 英文题名 | Thinking with Drafts: Speculative Temporal Reasoning for Efficient Long Video Understanding |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.00805) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | SpecTemp |
| Dataset | TempCompass, MVBench, Video-Holmes, LongVideoBench |

> [!tip] 效果简介
> - TempCompass 上，准确率 (%) 75.3 (13.7帧) / 77.2 (47.6帧) vs 72.2 (Qwen2.5-VL-7B 16帧) (+3.1)。
> - MVBench 上，准确率 (%) 68.7 / 69.3 vs 64.1 (Qwen2.5-VL-7B 16帧) (+4.6)。
> - Video-Holmes 上，准确率 (%) 47.0 (14.5帧) / 47.8 (58.1帧) vs 35.0 (Qwen2.5-VL-7B 16帧) (+12.0)。

## 概述

### 问题瓶颈：密集视觉上下文带来的效率困境

当前主流的长视频理解方法遵循“thinking-with-frames”范式，即大型多模态语言模型（MLLM）在生成推理轨迹的同时处理密集采样的视频帧。这一范式面临一个根本性瓶颈：不断增长的多模态上下文——包含推理轨迹和大量视觉token——导致LLM预填充阶段的计算开销急剧膨胀。观测表明，在Qwen2.5-VL-7B处理长视频时，超过90%的视觉token的注意力分数低于10⁻³（Figure 1(d)），意味着绝大多数视觉token对推理的贡献微乎其微，却占据了大量计算资源。这种长尾分布揭示了视觉冗余是效率瓶颈的核心来源。

### 核心思路：推测性时序推理

SpecTemp借鉴人脑双系统协作机制，提出了一种**推测性时序推理**框架，将时间感知与推理解耦。其核心设计是引入一个轻量级草案MLLM（3B）专门负责密集帧探索与关键帧选择，而目标MLLM（7B）仅需处理草案模型筛选出的稀疏代表帧，从而大幅减少视觉token数量与上下文长度。这一双模型推测-验证协同设计，在保持推理质量的同时显著加速长视频理解。

### 方法定位：双模型协同的强化学习框架

从方法论谱系来看，SpecTemp区别于以下范式：

- **单模型直接推理**（如Qwen2.5-VL-7B，2025）：统一采样或模型自身选择帧，单步或线性交织的思考-观察过程，缺乏对视觉冗余的主动管理。
- **thinking-with-frames范式**（如VideoChat-R1.5，Yan et al., 2025）：在推理过程中处理密集帧，视觉上下文随推理步数增长，效率受限。
- **层次压缩方法**（如VideoChat-Flash，Li et al., 2024）：通过压缩视觉表示减少token数，但可能丢失细粒度时序信息。

SpecTemp的关键创新在于将推测解码的思想从语言领域迁移到视频理解领域，通过双模型协同实现语义级近似与验证。其训练范式也从传统的监督微调或单阶段RL，升级为冷启动SFT加双模型协同GRPO强化学习的两阶段优化。

### 主要结果概览

SpecTemp在多个基准上实现了精度与效率的双重提升：

- **短视频基准**：仅使用13.7帧即超越Qwen2.5-VL-7B的16帧性能，TempCompass准确率从72.2%提升至75.3%，同时推理延迟从2.1秒降至1.8秒（Table 1）。
- **长视频基准**：在Video-Holmes上以14.5帧取得47.0%准确率，较Qwen2.5-VL-7B的35.0%提升12个百分点；在58.1帧配置下，精度超越VideoChat-R1.5，速度提升23%（Table 2）。
- **极端长程检索**：在V-NIAH（2000帧）测试中保持超过80%的准确率，验证了框架对超长视频的记忆与检索能力（Figure 8）。

这些结果表明，通过将密集感知卸载到轻量级草案模型，SpecTemp在保持甚至提升推理质量的前提下，有效缓解了长视频理解中的效率瓶颈。

## 背景与动机

### 长视频理解的效率困境

多模态大语言模型（MLLM）在视频理解任务中取得了显著进展，但其处理长视频的能力仍受制于一个根本性瓶颈：**不断增长的多模态上下文长度**。当前主流范式——可称为“thinking-with-frames”——要求模型在推理过程中同时承载视频帧的密集视觉token和逐步展开的推理轨迹。随着视频时长增加，预填充阶段的计算开销急剧膨胀，直接拖慢推理速度并推高显存占用。

这一瓶颈并非源于所有视觉token的等量贡献。对**Qwen2.5-VL-7B**（Qwen2.5-VL, 2025）的注意力分析揭示了一个关键现象：超过90%的视觉token注意力分数低于10⁻³，呈现显著的长尾分布（Figure 1(d)）。这意味着绝大多数视频帧对最终推理的贡献微乎其微，却依然消耗着等量的计算资源。换言之，现有范式将时间感知与推理过程紧密耦合，迫使模型在大量冗余信息中“大海捞针”。

### 现有方法的局限

为缓解上述问题，学界提出了多种策略，但均存在固有缺陷：

- **统一采样**：以固定间隔选取帧，虽简单高效，但无法区分关键帧与冗余帧，在长视频中容易遗漏时序上分散的细粒度线索。
- **层次压缩**：如**VideoChat-Flash**（Li et al., 2024）通过token压缩减少上下文长度，但压缩过程本身可能丢失对时序推理至关重要的视觉细节。
- **单模型强化学习推理**：如**Video-R1**（Feng et al., 2025）和**VideoChat-R1.5**（Yan et al., 2025），虽通过强化学习增强了模型的时序推理能力，但未从根本上解耦感知与推理——模型仍需在长上下文中同时完成帧筛选和逻辑推演，效率提升有限。实验表明，VideoChat-R1.5虽精度领先，但推理延迟高达5.8秒（Table 1），难以满足实时或大规模应用需求。

### 核心洞察：推测性时序推理

本文的出发点源于一个认知科学类比：**人脑在处理复杂时序任务时，并非由单一系统包揽全局，而是依赖快速直觉系统（System 1）与慢速分析系统（System 2）的协同**。前者快速扫描环境、提出候选信息；后者专注验证与深度推理。这一双系统协作机制天然地实现了感知与推理的解耦。

受此启发，本文提出**SpecTemp**（Speculative Temporal Reasoning）框架，核心思想是：**将时间感知与推理解耦，引入轻量级草案MLLM专门负责密集帧探索与关键帧选择，而目标MLLM仅需处理稀疏代表帧**。这一“推测-验证”协同设计从根源上削减了目标模型的视觉token数量与上下文长度，在保持推理质量的同时显著加速长视频理解。

### 本文动机与贡献定位

SpecTemp的提出旨在回答一个核心问题：**能否在不牺牲推理精度的前提下，大幅降低长视频理解的推理延迟？** 为此，本文做出以下贡献：

1. **双模型推测-验证架构**：设计了一个7B目标MLLM与3B草案MLLM协同工作的框架，草案模型负责在密集采样的时间区域内快速探索并选取信息量最大的关键帧，目标模型则专注于基于稀疏帧的高质量时序推理。
2. **迭代式时序推理机制**：通过最多3轮迭代，目标模型预测需要进一步探索的时间区域（Clue Tokens），草案模型据此进行定向密集采样与帧选择，形成闭环验证。
3. **双模型协同强化学习训练**：提出冷启动监督微调（SFT）与分组相对策略优化（GRPO）相结合的训练范式，并设计IoU奖励与视觉信息增益奖励，分别引导目标模型的时序定位能力和草案模型的帧选择质量。

后续章节将详细展开SpecTemp的技术方案、实验验证及其在短视频与长视频基准上的性能表现。

## 核心创新

SpecTemp的核心创新在于将传统“思考-观察”范式中紧密耦合的时间感知与推理解耦，构建了一个**双模型推测-验证协同架构**。这一设计直接回应了长视频理解中的根本效率瓶颈：在传统范式中，大型多模态大模型（MLLM）需同时承担密集视觉感知与复杂时序推理，导致预填充阶段上下文长度急剧膨胀，其中超过90%的视觉token注意力分数低于10⁻³（Figure 1(d)），却仍需付出高昂的计算代价。

### 关键机制创新：推测性时序推理

SpecTemp引入了一种**层次化的测试时扩展框架**，其核心改变体现在以下四个维度：

**1. 双模型非对称协同**

将单一大型MLLM替换为一个7B参数的目标MLLM与一个3B参数的草案MLLM（均基于Qwen2.5-VL初始化）。目标模型专注于全局时序推理与答案生成，草案模型则专门负责密集帧探索与关键帧选择。这种计算非对称性（|π_draft| ≪ |π_target|）使得密集感知任务被卸载到轻量级模型，大幅降低了目标模型需处理的视觉token数量。

**2. 迭代推测-验证循环**

推理流程从单步或线性交织的思考-观察过程，转变为**最多3次迭代的推测-验证循环**（Algorithm 1, Figure 2）：
- **初始化**：目标模型基于均匀采样的10帧生成初始推理轨迹，并预测需要进一步探索的时间区域（Clue Tokens）。
- **推测**：草案模型在目标模型预测的时间区域内以1fps进行密集采样，依据当前推理轨迹选出2个最具代表性且去冗余的关键帧。
- **验证**：目标模型利用草案选择的稀疏帧和累积推理轨迹，生成新的推理轨迹或最终答案，必要时指示下一轮探索区域。

这一循环使得模型能够动态聚焦于信息丰富的视频片段，而非被动接受固定采样。

**3. 双模型协同强化学习**

训练范式从监督微调或单阶段RL，升级为**冷启动SFT + 双模型协同GRPO强化学习**。关键设计在于奖励函数的差异化构造：
- **目标模型奖励**（公式7）：由格式正确性、答案准确性和预测证据段与真实区域的时间IoU三部分组成，引导目标模型精确定位关键时序区域。
- **草案模型奖励**（公式8-9）：引入视觉信息增益奖励 $R_{\mathrm{visual}} = \mathrm{Sim}_{\mathrm{CLIP}}(q, f_i) - \max_{f_j \in \mathcal{F}_{\mathrm{prev}}} \mathrm{Sim}_{\mathrm{CLIP}}(f_i, f_j)$，鼓励选择与问题高度相关且与已选帧冗余度低的帧。

消融实验证实，同时使用IoU奖励和视觉信息增益奖励的组合达到了最佳性能（Table 7）。

**4. 帧选择策略的根本转变**

帧选择从统一采样或模型自身隐式选择，转变为**草案模型依据目标模型预测的时间线索进行密集采样并显式选择**。在16帧预算下，默认分配策略10+2×3（初始10帧 + 每次迭代2帧 × 最多3次迭代）实现了准确率与效率的最佳平衡（Table 8）。

### 与基线方法的本质区别

相较于**VideoChat-R1.5**（Yan et al., 2025）代表的thinking-with-frames范式——其中单个大型MLLM需在持续增长的多模态上下文中同时进行感知与推理——SpecTemp通过推测性解耦，在仅使用14.5帧时即超越Qwen2.5-VL-7B的16帧性能（Video-Holmes +12.0%），同时将推理延迟从4.1秒降至3.7秒。当扩展至58.1帧时，精度超越VideoChat-R1.5，速度提升23%（Table 2）。

## 整体框架

SpecTemp 提出了一种**双模型协同的推测性时序推理框架**，其核心思想是将传统“思考-帧”范式中耦合的密集视觉感知与高层时序推理解耦，分别交由一个轻量级草案 MLLM 和一个强大的目标 MLLM 完成。这种设计直接回应了 Figure 1(d) 揭示的效率瓶颈：在 Qwen2.5-VL-7B 上，超过 90% 的视觉 token 注意力分数低于 10⁻³，大量计算被浪费在信息量极低的帧上。

### 框架总览与模块关系

框架由五个关键模块构成，形成一条**迭代推测-验证**的处理链路：

1. **目标 MLLM（7B）**：作为推理核心，负责全局时序推理、生成需要进一步探索的时间线索，并最终验证草案模型的帧选择、产出答案。其输入为问题文本和稀疏代表帧，输出包括推理轨迹、密集采样区域指示和最终答案。

2. **草案 MLLM（3B）**：作为感知前端，负责在目标模型预测的时间区域内进行密集帧探索，并从中选出最具信息量的稀疏代表帧。其计算规模显著小于目标模型（|π_draft| ≪ |π_target|），从而以较低开销完成密集感知任务。

3. **密集采样模块**：根据目标模型输出的时间线索，在指定区域内以 1 fps 的密度进行帧采样，为草案模型提供候选帧池。

4. **稀疏帧选择模块**：草案模型基于视觉信息增益奖励（公式 8）从密集帧中选出与问题高度相关且彼此去冗余的关键帧，作为下一轮目标模型的输入。

5. **迭代控制模块**：按照预设的最大迭代次数 T_max = 3 控制推测-验证循环的终止，在准确率与延迟之间取得平衡。

### 输入输出流与迭代流程

整个推理过程遵循 Algorithm 1 定义的迭代推测-验证循环，Figure 2 给出了可视化示意：

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/002_Figure_2.jpg]]
*Figure 2: Illustration of SpecTemp’s iterative speculation-verification process. Target MLLM predicts temporal regions (Clue Tokens); Draft MLLM proposes frames; Target MLLM verifies with History Tokens across iterative rounds*

**初始化阶段**（公式 3）：目标模型接收问题文本 W^q 和初始均匀采样的 10 帧 V_0^s，生成初始推理轨迹 T_0、需要密集探索的时间区域 V_0^d 和候选答案 W^a。

**迭代推测-验证循环**（t = 1, 2, ..., T_max）：
- **草案推测**（公式 4）：草案模型接收当前迭代的密集帧 V_t^d 和上一轮的推理轨迹 T_{t-1}，从中选出稀疏代表帧 V_t^s。
- **目标验证**（公式 5）：目标模型基于草案选择的稀疏帧 V_t^s 和累积的历史推理轨迹 T_{<t}，生成新的推理轨迹 T_t、下一轮需要探索的密集区域 V_t^d，或直接输出最终答案 W^a。

**终止条件**：当目标模型判定已掌握足够信息时，直接输出答案；否则继续迭代，直至达到 T_max = 3。

### 训练范式

SpecTemp 采用**两阶段优化**策略（第 3.3 节）：
- **冷启动 SFT**：在 SpecTemp-80K 数据集上进行监督微调，使双模型初步学会协同工作。
- **双模型协同 GRPO 强化学习**：采用分组优势函数和 KL 惩罚项（β = 0.04）联合优化目标模型和草案模型（公式 6）。目标模型的奖励由格式正确性、答案准确性和预测证据段与真实区域的时间 IoU 组成（公式 7）；草案模型的奖励由格式正确性和视觉信息增益组成（公式 8-9），后者鼓励选择与问题相关且与已选帧冗余度低的帧。

这种推测-验证的协同设计，使得目标模型始终仅需处理稀疏的关键帧，从而在保持推理质量的同时将视觉 token 数量和上下文长度控制在较低水平，从根本上缓解了传统范式的效率瓶颈。

### 补充图表

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/003_Figure_3.jpg]]
*Figure 3: Overview of data generation pipeline and composition*

## 核心模块与公式推导

### 3.1 双模型推测-验证框架

SpecTemp 的核心设计是将传统“思考-观察”范式中耦合的时序感知与推理解耦，引入**非对称双模型协同架构**：一个 7B 参数的目标 MLLM（π_target）负责全局时序推理与草案验证，一个 3B 参数的草案 MLLM（π_draft）负责密集帧探索与关键帧选择，满足计算非对称性 |π_draft| ≪ |π_target|。

传统 MLLM 直接基于统一采样帧生成答案的条件似然为：

$$ \pi \left( \mathbf { W } ^ { \mathrm { a } } \mid \mathbf { W } ^ { \mathrm { q } } , \mathbf { V } \right) = \prod _ { i = 1 } ^ { n } \pi \left( \mathbf { W } _ { i } ^ { \mathrm { a } } \mid \mathbf { W } _ { < i } ^ { \mathrm { a } } , \mathbf { W } ^ { \mathrm { q } } , \mathbf { V } \right) $$

其中 **W^q** 为问题文本，**V** 为视频帧序列，**W^a** 为逐 token 生成的答案序列。

SpecTemp 将其重构为迭代推测-验证过程，在最多 T_max 次迭代内的联合似然为：

$$ \prod _ { \mathbf { \mu } \leq T _ { \mathrm { m a x } } } \pi _ { \mathrm { t a r g e t } } \big ( \mathbf { W } ^ { \mathrm { a } } , \mathbf { V } ^ { \mathrm { d } } \mid \mathbf { W } ^ { \mathrm { q } } , \mathbf { V } ^ { \mathrm { s } } \big ) \cdot \pi _ { \mathrm { d r a f t } } \big ( \mathbf { V } ^ { \mathrm { s } } \mid \mathbf { V } ^ { \mathrm { d } } \big ) $$

其中 **V^s** 为草案模型选择的稀疏代表帧，**V^d** 为目标模型预测的需要密集探索的时间区域。

### 3.2 迭代推测-验证流程

每次迭代包含三个步骤，形成“预测-探索-验证”闭环：

**步骤一：初始化（目标模型预测）**

$$ { \bf T } _ { 0 } , { \bf V } _ { 0 } ^ { \mathrm { d } } , { \bf W } ^ { \mathrm { a } } = \pi _ { \mathrm { t a r g e t } } ( { \bf W } ^ { \mathrm { q } } , { \bf V } _ { 0 } ^ { \mathrm { s } } ) $$

目标模型基于问题文本和初始均匀采样帧 **V_0^s**，同时生成推理轨迹 **T_0**（包含时间线索）、需要密集采样的时间区域 **V_0^d**，以及可能的答案 **W^a**。

**步骤二：草案推测（草案模型选帧）**

$$ \mathbf { V } _ { t } ^ { \mathrm { s } } = \pi _ { \mathrm { d r a f t } } \left( \mathbf { V } _ { t } ^ { \mathrm { d } } ; \mathrm { T } _ { t - 1 } \right) , \quad t \in [ 1 , T _ { \mathrm { m a x } } ] $$

草案模型根据上一轮推理轨迹 **T_{t-1}** 提供的时间线索，从密集采样帧 **V_t^d**（以 1fps 采样）中选出信息量最大且去冗余的稀疏代表帧 **V_t^s**。

**步骤三：目标验证（目标模型推理）**

$$ \left( \mathbf { T } _ { t } , \mathbf { V } _ { t } ^ { \mathrm { d } } , \mathbf { W } ^ { \mathrm { a } } \right) = \pi _ { \mathrm { t a r g e t } } ( \mathbf { V } _ { t } ^ { \mathrm { s } } ; \mathbf { T } _ { < t } ) $$

目标模型利用草案选择的稀疏帧和累积推理轨迹 **T_{<t}**，生成新的推理轨迹、进一步探索的密集区域，或最终答案。当模型判断信息充分时输出答案并终止循环，否则进入下一轮迭代。

### 3.3 双模型强化学习优化

SpecTemp 采用两阶段训练：冷启动监督微调（SFT）后接 GRPO 强化学习。联合优化目标模型和草案模型的损失函数为：

$$ \mathcal { I } = \mathbb { E } \left[ { \bf W } ^ { \mathrm { q } } , { \bf V } , \{ { \bf W } ^ { \mathrm { a } } , { \bf V } ^ { \mathrm { d } } \} \sim \pi _ { \mathrm { t a r g e t _ { \mathrm { o l d } } } } , { \bf V } ^ { \mathrm { s } } \sim \pi _ { \mathrm { d r a f t _ { \mathrm { o l d } } } } \right] \frac { 1 } { G } \sum _ { i = 1 } ^ { G } \frac { \pi _ { \mathrm { t a r g e t } } \left( { \bf W } _ { i } ^ { \mathrm { a } } , { \bf V } ^ { \mathrm { d } } \mid { \bf W } ^ { \mathrm { q } } , { \bf V } ^ { \mathrm { s } } \right) \cdot \pi _ { \mathrm { d r a f t } } \left( { \bf V } ^ { \mathrm { s } } \mid { \bf V } ^ { \mathrm { d } } \right) } { \pi _ { \mathrm { t a r g e t _ { \mathrm { o l d } } } } \left( { \bf W } _ { i } ^ { \mathrm { a } } , { \bf V } ^ { \mathrm { d } } \mid { \bf W } ^ { \mathrm { q } } , { \bf V } ^ { \mathrm { s } } \right) \cdot \pi _ { \mathrm { d r a f t _ { \mathrm { o l d } } } } \left( { \bf V } ^ { \mathrm { s } } \mid { \bf V } ^ { \mathrm { d } } \right) } A _ { i } - \beta \cdot \mathbb { D } _ { K L } \left( \pi _ { \mathrm { t a r g e t } } \cdot \pi _ { \mathrm { d r a f t } } \Vert \pi _ { \mathrm { t a r g e t } } \cdot \pi _ { \mathrm { d r a f t _ { \mathrm { r e f } } } } \right) $$

其中 G 为采样组数，**A_i** 为分组优势函数，β=0.04 为 KL 惩罚系数，防止新策略过度偏离参考策略。

### 3.4 奖励设计

**目标模型奖励**由三部分组成：

$$ R _ { \mathrm { t a r g e t } } = R _ { \mathrm { f o r m a t } } ^ { \mathrm { t a r g e t } } + R _ { \mathrm { a n s w e r } } + R _ { \mathrm { I o U } } $$

- **R_format**：格式正确性奖励，确保输出符合预定义模板
- **R_answer**：答案准确性奖励，基于标准答案匹配
- **R_IoU**：时间定位奖励，计算预测证据段时间区间与真实区间的时间 IoU

**草案模型奖励**由两部分组成：

$$ R _ { \mathrm { d r a f t } } = R _ { \mathrm { f o r m a t } } ^ { \mathrm { d r a f t } } + R _ { \mathrm { v i s u a l } } $$

其中视觉信息增益奖励 **R_visual** 的设计为：

$$ R _ { \mathrm { v i s u a l } } = \mathrm { S i m } _ { \mathrm { C L I P } } ( q , f _ { i } ) - \operatorname* { m a x } _ { f _ { j } \in \mathcal { F } _ { \mathrm { p r e v } } } \mathrm { S i m } _ { \mathrm { C L I P } } ( f _ { i } , f _ { j } ) $$

- 第一项 Sim_CLIP(q, f_i)：鼓励选择与问题文本 q 高度相关的帧 f_i
- 第二项 max Sim_CLIP(f_i, f_j)：惩罚与已选帧集合 F_prev 中冗余度高的帧，确保所选帧的多样性

该奖励机制引导草案模型在密集帧中选出既与问题相关又彼此互补的关键帧，使目标模型能以最少视觉 token 获得最充分的时序证据。

## 实验与分析

### 1. 主实验结果

SpecTemp 在两个维度的基准测试上均展现出显著的性能与效率优势：在短视频时序推理基准上以更少帧数超越强基线，在长视频理解基准上以更低延迟达到或超越代表方法。

#### 短视频时序推理

Table 1 汇总了 TempCompass 与 MVBench 上的对比结果。SpecTemp 以平均 13.7 帧的稀疏输入，在 TempCompass 上达到 75.3% 准确率，较 Qwen2.5-VL-7B（16 帧）提升 3.1 个百分点，同时推理延迟从 2.1 秒降至 1.8 秒。当帧预算放宽至 47.6 帧时，准确率进一步提升至 77.2%，延迟为 4.7 秒，仍低于 VideoChat-R1.5（64 帧，5.8 秒）。在 MVBench 上，SpecTemp 以 68.7% 的准确率领先 Qwen2.5-VL-7B 达 4.6 个百分点。这一结果表明，**草案模型筛选出的稀疏关键帧比均匀采样帧包含更丰富的时序判别信息**，使得目标模型在更少视觉 token 的条件下实现更强的推理能力。

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/004_Table_1.jpg]]
*Table 1: Performance of different models on short-form video benchmarks*

#### 长视频理解

Table 2 展示了在五个长视频基准上的表现。SpecTemp 在 14.5 帧配置下，于 Video-Holmes 上取得 47.0% 准确率，较 Qwen2.5-VL-7B（16 帧，35.0%）提升 12.0 个百分点；在 MLVU 上提升 8.0 个百分点（48.6% vs 40.6%）。当帧数增至 58.1 帧时，SpecTemp 在 LongVideoBench 上达到 61.4%，超越 VideoChat-R1.5 的精度水平，同时推理速度提升 23%。在 Video-MME（无字幕）上，SpecTemp 以 62.4%（14.5 帧）超越 Qwen2.5-VL-7B 达 6.4 个百分点。值得关注的是，**SpecTemp 的延迟优势随帧数增加而扩大**：58.1 帧时延迟为 4.7 秒，而 VideoChat-R1.5 在 64 帧下需 5.8 秒，这验证了双模型推测-验证架构在长上下文场景下的可扩展性。

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/005_Table_2.jpg]]
*Table 2: Performance of different models on long-form video benchmarks*

#### 极端长程检索

Figure 8 展示了 V-NIAH（Visual Needle-In-A-Haystack）评测结果。在 2000 帧视频中插入单帧视觉问题，SpecTemp 在所有深度位置均保持超过 80% 的检索准确率，证明其迭代推测机制能够有效定位远距离关键帧，而非受限于固定的均匀采样窗口。

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/016_Figure_8.jpg]]
*Figure 8: V-NIAH performance across frame counts and needle depths*

### 2. 消融实验

#### 帧选择策略

Table 3 对比了三种帧选择策略：统一采样、CLIP-based 选择、以及 SpecTemp 的目标+草案协同选择。在 Video-Holmes 上，协同选择（平均 14.1 帧）达到 47.0%，而统一采样仅 39.5%，CLIP-based 为 42.3%。这揭示了一个关键因果机制：**纯视觉相似度（CLIP）无法替代基于推理轨迹的语义引导**，草案模型通过接收目标模型预测的时间线索，能够选择更直接支撑答案的关键帧。

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/007_Table_3.jpg]]
*Table 3: Ablation study on frame selection strategies*

#### 双模型协同

Table 4 在 LongVideoBench 上消融了模型协同方案。仅使用大模型（Target-only）准确率为 55.2%，效率分数为 22.1；仅使用小模型（Draft-only）准确率 52.8%，效率分数 23.0。而 Large+Small 协同配置达到最高准确率 57.5% 和最高效率分数 25.0。这证实了推测-验证分工的有效性：**大模型专注于高质量时序推理，小模型承担密集感知的计算负载，二者互补而非替代**。

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/009_Table_4.jpg]]
*Table 4: Ablation study on model collaboration evaluated on LongVideoBench. Efficiency = Accuracy / Latency*

#### 训练策略

Table 5 表明，冷启动 SFT 后接双模型协同 GRPO 强化学习，在 LongVideoBench 上取得 57.5% 准确率，优于仅 SFT（54.1%）或仅 RL（55.8%）。SFT 阶段为模型提供了基本的推测-验证行为模式，RL 阶段则通过奖励信号精细化帧选择质量和推理精度。

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/010_Table_5.jpg]]
*Table 5: Ablation study on training strategies for dual-model collaboration on LongVideoBench*

#### 迭代次数

Table 6 显示，最大迭代次数 T_max=3 在准确率（57.5%）和延迟（2.3 秒）之间达到最佳平衡。T_max=1 时准确率降至 54.8%，说明单轮推测不足以充分探索长视频时序结构；T_max=5 时准确率仅微增至 57.8%，但延迟升至 3.1 秒，边际收益递减。

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/011_Table_6.jpg]]
*Table 6: Ablation study on maximum iteration number*

#### 奖励组件

Table 7 评估了奖励函数各组件的作用。同时使用 IoU 奖励和视觉信息增益奖励的组合达到最佳性能。移除 IoU 奖励（仅使用答案正确性和格式奖励）导致目标模型预测的证据段时间区域精度下降，进而影响草案模型的帧选择质量。移除视觉信息增益奖励则使草案模型倾向于选择冗余帧，降低关键帧的判别力。

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/013_Table_7.jpg]]
*Table 7: Ablation study on reward components. We evaluate the contribution of IoU reward*

#### 帧分配策略

Table 8 在 16 帧和 64 帧固定预算下探索了初始化帧数与每轮迭代帧数的分配方案。默认配置 10+2×3 在 16 帧预算下实现 57.5% LongVideoBench 准确率和 47.0% Video-Holmes 准确率。过度倾斜初始化帧（如 14+1×2）会压缩迭代探索空间，降低长程定位能力；过度倾斜迭代帧（如 6+3×3）则因初始上下文不足而损害推理起点质量。

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/014_Table_8.jpg]]
*Table 8: Ablation study on frame allocation strategies (Initial+Per-Iter×Max-Iter) under fixed budgets of 16 and 64 frames. We report accuracy (%) and inference latency*

### 3. 效率分析

Figure 4 分解了推理延迟的组成。传统 thinking-with-frames 范式中，LLM 预填充阶段需处理全部视觉 token 和推理轨迹，构成主要延迟瓶颈。SpecTemp 将密集采样（1fps）委托给 3B 草案模型，目标 7B 模型仅需处理稀疏代表帧，预填充 token 数量大幅减少，总延迟降至 2.3 秒。这一架构决策的深层逻辑在于：**90% 以上视觉 token 的注意力分数低于 10^-3（Figure 1d），对推理贡献极小，却线性推高预填充成本**。

![[assets/figures/papers/paper_list_l2112_https_arxiv_org_abs_2512_00805/figures/006_Figure_4.jpg]]
*Figure 4: Inference latency breakdown. SpecTemp achieves the lowest latency (2.3s) by delegating dense sampling to the draft model*

### 4. 失败模式与局限性

尽管 SpecTemp 在多数场景下表现优异，仍存在以下不足：

- **固定迭代上限**：T_max=3 对需要多步时序推理的复杂问题可能不足。Figure 13 的定性案例显示，三步迭代可完成时序排序推理，但对于更长的事件链，可能需要自适应迭代终止机制。
- **草案选择的语义盲区**：草案模型的视觉奖励基于 CLIP 相似度（公式 8），可能忽略需要细粒度语义理解的帧（如文本密集的场景文字），导致关键信息遗漏。
- **训练成本**：两阶段 SFT+RL 在 16 块 H100 GPU 上完成，论文未探索参数高效微调方案以降低 RL 阶段的计算开销。
- **极端长度未验证**：V-NIAH 仅测试至 2000 帧，对于小时级或更长视频的推理能力尚需进一步验证。

## 方法谱系与知识库定位

### 与现有范式的对比与继承

SpecTemp 的核心贡献在于将长视频理解中的**时间感知（temporal perception）与推理解耦**，并引入**双模型推测-验证协同**机制。这一设计直接回应了现有“thinking-with-frames”范式的效率瓶颈：传统的单模型方案（如 **Qwen2.5-VL-7B**（Qwen2.5-VL, 2025）、**VideoChat-R1.5**（Yan et al., 2025））将推理轨迹和密集视觉 token 一同塞入 LLM 的预填充阶段，导致多模态上下文不断膨胀。SpecTemp 的观察表明，超过 90% 的视觉 token 注意力分数低于 $10^{-3}$（Figure 1(d)），这意味着大量视觉信息在推理中贡献极小，却造成了显著的计算浪费。

从方法谱系看，SpecTemp 处于以下几条线的交汇处：

1. **视频推理 MLLM 线**：继承自 **VideoChat-R1.5** 和 **Video-R1**（Feng et al., 2025）的“thinking-with-frames”范式，但通过解耦时间感知任务，避免了单模型在预填充阶段处理全量密集 token 的开销。

2. **层次化/压缩视频理解线**：与 **VideoChat-Flash**（Li et al., 2024）等层次压缩方法共享“减少冗余视觉信息”的目标，但 SpecTemp 不是通过压缩 token 本身，而是通过草案模型主动选择信息量最大的代表帧来实现稀疏化。

3. **推测解码与大-小模型协同线**：借鉴了人脑双系统协作机制，将推测性推理引入视频感知。草案模型（3B）负责密集帧探索和关键帧选择，目标模型（7B）专注于高质量时序推理与验证，两者通过迭代的推测-验证循环协同工作。

4. **强化学习驱动推理线**：采用冷启动 SFT + 双模型协同 GRPO 强化学习的训练范式，与 **Video-R1** 的单一 RL 阶段形成对比。SpecTemp 的奖励设计同时覆盖目标模型（格式正确性 + 答案准确性 + 时间 IoU）和草案模型（格式正确性 + 视觉信息增益），实现了联合优化。

### 适用边界

SpecTemp 在以下条件下表现出色：

- **长视频时序推理任务**：在 Video-Holmes（+12.0%）、MLVU（+8.0%）、Video-MME（+6.4%）等长视频基准上，SpecTemp 以更少的平均帧数（14.5 帧）超越了 Qwen2.5-VL-7B（16 帧）的精度，同时将推理延迟从 4.1 秒降至 3.7 秒（Table 2）。
- **需要多步证据检索的场景**：迭代推测-验证机制允许模型在最多 3 轮循环中逐步定位关键时间区域，在 V-NIAH（2000 帧）测试中准确率超过 80%（Figure 8）。
- **对推理延迟敏感的部署场景**：SpecTemp 在 13.7 帧时即超越 Qwen2.5-VL-7B（16 帧），延迟从 2.1 秒降至 1.8 秒（Table 1）；在 58.1 帧时精度超越 VideoChat-R1.5，速度提升 23%（Table 2）。

适用边界主要体现在：

- **最大迭代次数固定为 3**：虽然消融实验（Table 6）表明 $T_{\text{max}}=3$ 在准确率和延迟（2.3 秒）之间取得最佳平衡，但对于需要多步推理的复杂任务，这一固定上限可能限制性能。
- **草案模型的帧选择基于 CLIP 相似度**：公式 $R_{\text{visual}} = \text{Sim}_{\text{CLIP}}(q, f_i) - \max_{f_j \in \mathcal{F}_{\text{prev}}} \text{Sim}_{\text{CLIP}}(f_i, f_j)$ 仅考虑问题-帧相似度和帧间冗余度，可能忽略更复杂的语义关联或因果依赖。
- **极端长视频未验证**：V-NIAH 测试仅覆盖到 2000 帧，未对小时级或更长视频进行极端长程推理验证。

### 局限与开放问题

论文明确指出的局限包括：

1. **训练成本较高**：两阶段 SFT+RL 训练使用 16 块 H100 GPU，论文未探讨通过参数高效微调（如 LoRA）降低 RL 阶段计算开销的途径。
2. **固定迭代预算**：最大迭代次数固定为 3，缺乏自适应机制来根据问题复杂度动态调整推测-验证轮次。
3. **帧选择策略的语义深度不足**：草案模型仅基于 CLIP 相似度选择帧，可能无法捕捉需要更深层次语义理解的视觉线索。

论文未明确讨论但值得关注的开放问题：

- **超长视频扩展**：如何将 SpecTemp 推广到超过 2-3 小时的视频？可能的方向包括引入层次化推理（先定位大段时间段，再在段内精细搜索）或外部记忆机制来缓存已探索的时间区域。
- **自适应迭代预算**：是否可以通过在线学习或置信度估计来动态调整推测-验证轮次？例如，当目标模型的推理轨迹置信度较高时提前终止，或在不确定性较高时增加迭代。
- **草案模型的策略升级**：能否采用基于信息瓶颈或强化学习的帧选择策略来替代当前的 CLIP 相似度奖励？这可能需要更复杂的训练方案，但有望提升关键帧的代表性和多样性。
- **跨模型泛化性**：SpecTemp 的目标和草案模型均基于 Qwen2.5-VL 初始化，其在其他 MLLM 架构（如 InternVL 系列）上的迁移效果尚待验证。

### 知识库定位总结

SpecTemp 在“高效长视频推理”这一细分方向上占据了一个独特位置：它既不同于纯压缩方法（牺牲信息保真度换取速度），也不同于纯推理增强方法（增加推理链长度但忽略视觉 token 冗余）。其核心创新在于**用计算不对称性换取效率**——让轻量级草案模型承担密集感知的计算开销，让目标模型专注于高质量推理。这一设计在当前“thinking-with-frames”范式遭遇效率瓶颈的背景下，提供了一个可验证的解决方案，并在多个基准上同时实现了精度提升和延迟降低。

## 原文 PDF

![[paperPDFs/CVPR_2026/Thinking_with_Drafts_Speculative_Temporal_Reasoning_for_Efficient_Long_Video_Understanding.pdf]]
