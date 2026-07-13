---
title: "E3AD: An Emotion-Aware Vision-Language-Action Model for Human-Centric End-to-End Autonomous Driving"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/E3AD_An_Emotion_Aware_Vision_Language_Action_Model_for_Human_Centric_End_to_End_Autonomous_Driving.pdf
project_link: null
code_link: null
aliases:
- E3AD
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将连续 VAD 情绪空间建模、双通路空间推理（自我中心+环境中心）以及一致性导向的三阶段训练（模态预训练、联合微调、情绪-动作对齐）融入统一的 VLA 框架，使模型能够根据指令中的情绪色彩调整视觉定位与规划行为。
primary_logic: 注入情绪认知的 VLA 模型能更准确地解析驾驶指令中的隐含意图与紧迫程度，通过连续 VAD 向量指导指称消歧与轨迹生成，并由双通路空间表征增强 3D 理解及地图一致性，最终产出更符合人类期望的安全、共情驾驶行为。
claims:
- 在端到端轨迹规划上，E3AD 全面超越包括 PTPC 在内的所有基线，ADE/FDE/SSPD 等指标最高相对提升 20%。
- 在视觉定位任务中，E3AD 在 Talk2Car、MoCAD、DrivePilot 及多种挑战性子集上均大幅领先现有 SOTA，绝对增益最高 +11.63%。
- 情绪感知模块使模型在歧义指令和长文本指令上的定位准确率获得最大提升（分别 +4.5%/+4.8%），消融实验证实其不可或缺。
- 双通路空间推理中，去除自我中心通路导致视觉定位 IoU 下降 7.0%，去除环境中心通路则使轨迹规划 ADE/FDE 恶化约 10%，说明两者互补且对下游任务至关重要。
---

# E3AD: An Emotion-Aware Vision-Language-Action Model for Human-Centric End-to-End Autonomous Driving

> [!tip] 核心洞察
> 注入情绪认知的 VLA 模型能更准确地解析驾驶指令中的隐含意图与紧迫程度，通过连续 VAD 向量指导指称消歧与轨迹生成，并由双通路空间表征增强 3D 理解及地图一致性，最终产出更符合人类期望的安全、共情驾驶行为。

| 字段 | 内容 |
|------|------|
| 中文题名 | E3AD：面向人本端到端自动驾驶的情绪感知视觉-语言-动作模型 |
| 英文题名 | E3AD: An Emotion-Aware Vision-Language-Action Model for Human-Centric End-to-End Autonomous Driving |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.04733) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | E3AD |
| Dataset | Talk2Car-Trajectory, Talk2Car |

> [!tip] 效果简介
> - Talk2Car-Trajectory 上，ADE↓ 3.88 vs 4.54 (PTPC) (降低 17.01%)；FDE↓ 6.64 vs 7.75 (PTPC) (降低 20.00%)。
> - Talk2Car (test) 上，视觉定位 IoU (accuracy)↑ 80.12 vs 74.62 (CAVG) (绝对提升 +6.86%)。
> - Talk2Car (emotion) 上，Valence Spearman ρ↑ 0.95 vs — (达到 SOTA) (领先已有方法)。

## 概要

### 问题与瓶颈

现有端到端自动驾驶系统在设计上聚焦于理性控制与空间推理，却普遍忽视了乘客的情感状态——如焦虑、紧迫感或信任度。这种“情感盲区”导致系统行为与人类期望之间存在显著的**情感鸿沟**，不仅削弱了人机交互的自然性，更从根本上限制了公众对自动驾驶的接受度。当乘客发出带有情绪色彩的指令时，情感无关的视觉-语言-动作模型无法解析其中的隐含意图与紧迫程度，从而产生生硬、不匹配的驾驶行为。

### 核心方法

本文提出 **E3AD**，首个将连续情绪建模与双通路空间推理统一于端到端框架的**情感感知视觉-语言-动作模型**。其核心设计包括三个关键创新：

1. **连续 VAD 情绪空间建模**：将自然语言指令映射到 Valence-Arousal-Dominance 三维连续空间，精准捕捉语气、紧迫度等情感信息，并以此引导指称消歧与轨迹生成。
2. **双通路空间推理**：融合自我中心通路（相对方向、距离、图像坐标）与环境中心通路（BEV 坐标与粗轨迹），分别提供短视距动作线索与全局地图拓扑理解，实现互补的空间认知。
3. **三阶段一致性训练**：从模态预训练（情绪+空间）到联合指令微调，再到基于直接偏好优化的情绪-动作对齐，逐步赋予模型情感感知、空间推理与行为一致性的能力。

### 主要结果

在多个真实驾驶数据集上的系统评估表明，E3AD 在端到端轨迹规划、视觉定位与情绪估计三项核心任务上均取得领先性能：

- **轨迹规划**：在 Talk2Car-Trajectory 基准上，E3AD 的 ADE 与 FDE 分别较最强基线 **PTPC**（Grujicic et al., AAAI 2022）降低 17.01% 与 20.00%，实现了全面超越。
- **视觉定位**：在 Talk2Car 测试集上，E3AD 的 IoU 准确率达到 80.12%，较此前最优方法 **CAVG**（Liao et al., CTR 2024）绝对提升 6.86%；在 MoCAD、DrivePilot 及多种挑战性子集上同样大幅领先。
- **情绪估计**：VAD 三维度 Spearman 相关系数均达到 0.95 以上，显著优于已有方法，验证了连续情绪建模的有效性。
- **消融实验**：去除情绪建模使歧义指令与长文本指令的定位准确率分别下降 4.5% 与 4.8%；去除自我中心通路导致定位 IoU 下降 7.0%，去除环境中心通路则使轨迹规划 ADE/FDE 恶化约 10%，证实各组件的独立价值与互补性。
- **用户研究**：217 人主观评估中，E3AD 在合规性、情绪同步、安全感与偏好等维度均获最高分，表明其行为更符合人类期望。

### 方法谱系与知识库定位

E3AD 以通用视觉-语言模型 **Qwen2.5-VL-7B**（Bai et al., arXiv 2025）为推理主干，通过低秩适配器注入情感与空间先验，在保持参数效率的同时实现任务特化。相较于以 **FSDrive-Finetuned**（Zeng et al., arXiv 2025）为代表的现有 VLA 范式，E3AD 首次将连续 VAD 情绪空间显式纳入决策闭环，并从自我中心与环境中心双视角构建空间理解，突破了单一视角推理的局限。其训练策略融合了监督微调与偏好对齐，为情感感知自动驾驶提供了一条可复现的技术路径。



### 端到端自动驾驶的“情感鸿沟”

近年来，视觉-语言-动作（VLA）模型在端到端自动驾驶领域取得了显著进展，使车辆能够根据自然语言指令完成视觉定位与轨迹规划。然而，现有系统在设计上存在一个根本性盲区：它们将驾驶建模为一个纯粹理性、去情感化的优化问题，完全忽视乘客的情感状态——如焦虑、紧迫感或信任感。这种“情感无关”（emotion-agnostic）范式导致系统行为与人类期望之间出现深刻的**情感鸿沟**，严重影响了公众对自动驾驶技术的信任与接受度。

具体而言，当乘客以不同语气发出“靠边停车”的指令时，现有系统无法区分“从容地靠边”与“紧急靠边”之间的行为差异，只能输出一条中性的、最优化的轨迹。这种缺乏共情能力的驾驶行为，在真实人机交互中往往显得僵硬、不可预测，甚至引发乘客的不安全感。

### 现有方法的局限

当前主流的端到端自动驾驶方法可归纳为两类缺陷：

1. **情感建模的缺失或粗糙化**：绝大多数方法完全未引入情感认知模块。少数尝试情感感知的工作仅使用离散情绪标签（如“happy”、“angry”），无法刻画情绪的连续性与强度变化，更无法将情绪信号与驾驶决策建立因果关联。

2. **空间推理的单通路偏置**：现有 VLA 模型通常仅依赖自我中心（egocentric）前视图进行空间理解，缺乏对全局道路拓扑、遮挡关系及多智能体布局的结构化表征。这种短视距的空间认知在复杂城市场景中容易产生指称歧义与轨迹规划偏差。

### E3AD 的核心动机

针对上述缺口，E3AD 提出将**连续 VAD 情绪空间建模**、**双通路空间推理**以及**一致性导向的三阶段训练**融入统一的 VLA 框架。其核心动机在于：注入情绪认知的 VLA 模型能够更准确地解析驾驶指令中的隐含意图与紧迫程度，通过连续 VAD 向量指导指称消歧与轨迹生成，并由双通路空间表征增强 3D 理解及地图一致性，最终产出更符合人类期望的安全、共情驾驶行为。

### 任务定义

E3AD 将开放域端到端自动驾驶形式化为如下映射：

$$f_{\theta} : (I, C) \to \hat{\mathcal{V}} = \{\hat{b}, \hat{\tau}\}$$

其中 $I$ 为多视角观测，$C$ 为自然语言指令，$\hat{b}$ 为指称目标定位，$\hat{\tau}$ 为未来轨迹航点序列。这一统一框架将情绪理解、视觉定位与路径规划纳入同一个自回归推理链条，为实现人本自动驾驶提供了形式化基础。



## 核心方法与创新机理

E3AD 的核心贡献在于将**连续情绪建模**与**双通路空间推理**统一注入 VLA 框架，并辅以**三阶段一致性训练**，从而弥合现有端到端自动驾驶系统中的“情感鸿沟”。以下从三个关键维度展开其相对于现有范式的创新。

### 从离散情绪到连续 VAD 空间的情感注入

现有 VLA 系统（如 **FSDrive-Finetuned**，Zeng et al., arXiv 2025；**CAVG**，Liao et al., CTR 2024）要么完全无视乘客情绪，要么仅使用离散情绪标签（如 happy/angry），无法捕捉驾驶指令中细微的语气差异与紧迫程度。E3AD 首次将连续 **Valence-Arousal-Dominance (VAD)** 三维情绪空间引入端到端驾驶决策（Section 3.3）：

- **连续建模**：将情绪表征为 $e \in \mathbb{R}^3$，相比离散类别能更精细地刻画从“轻松巡航”到“紧急避让”的情绪梯度。
- **情绪感知命令增强**：利用 Qwen2.5-VL 为每条原始指令生成 $K$ 个保持驾驶目标但改变态度/强度的改写版本，构造增强命令-情绪对 $\mathcal{C}^*$，并通过监督微调损失 $\mathcal{L}_{\mathrm{emo}}$ 使 VLM 获得连续 VAD 预测能力。
- **因果作用机制**：预测的 VAD 向量在推理时作为隐式先验，引导模型在歧义指令消歧和长文本指令理解中做出更符合情绪意图的指称定位与轨迹规划。

消融实验证实这一创新的不可或缺性：去除情绪建模后，模型在**歧义指令**和**长文本指令**子集上的视觉定位准确率分别下降 4.5% 和 4.8%（Table 5），说明连续情绪信号是消解语义模糊与长距离依赖的关键杠杆。

### 双通路空间推理：自我中心与环境的互补融合

传统 VLA（如 **Qwen2.5-VL-7B**，Bai et al., arXiv 2025）通常仅依赖单一自我中心前视图进行空间理解，缺乏对道路拓扑、遮挡关系和多智能体布局的全局感知。E3AD 提出**双通路空间推理**（Section 3.4），将两类互补的空间先验融合：

| 通路 | 表征空间 | 预测目标 | 功能角色 |
|------|----------|----------|----------|
| **自我中心通路 (Egocentric)** | 相对方向、距离、图像坐标 | 即时动作导向的空间线索 | 短视距精细定位 |
| **环境中心通路 (Allocentric)** | BEV 世界坐标、粗轨迹 | 全局道路结构与多智能体布局 | 长时域路径规划 |

两条通路在功能上高度互补：消融实验中，移除自我中心通路导致 Talk2Car 视觉定位 IoU 下降 7.0%（Table 5），而移除环境中心通路则使轨迹规划 ADE/FDE 分别恶化约 10.0%/10.1%（Table 6）。这一结果揭示了一个关键洞察：**精细指称定位依赖自我中心的局部空间线索，而安全、连贯的路径规划离不开环境中心的全局拓扑理解**。

### 三阶段一致性训练：从模态预训练到情绪-动作对齐

现有方法通常采用单一阶段的指令微调（SFT），缺乏对情绪与驾驶行为之间一致性的显式约束。E3AD 设计了三阶段渐进式训练策略（Section 3.6）：

1. **模态预训练**：分别训练情绪预测和空间推理能力，使 VLM 获得领域特化的感知技能。
2. **联合指令微调**：通过自回归损失 $\mathcal{L}_{\mathrm{Joint}}$ 统一优化完整输出序列 $T = (\hat{e}, \hat{b}, \hat{\tau})$，驱动情感、定位与规划的一体化推理。
3. **情绪-动作对齐（DPO）**：构造伪偏好对——选取 VAD 嵌入偏离最大的增强指令作为负样本并生成对应的情绪扰动轨迹，通过 DPO 损失 $\mathcal{L}_{\mathrm{dpo}}$ 鼓励模型偏好真实轨迹而抑制情绪扭曲的轨迹，实现行为与情感的一致性对齐。

DPO 阶段的收益在 Figure 4 中得到验证：训练后情绪-轨迹的 Spearman 相关系数显著提高。这一创新确保了模型不会因情绪注入而产生不安全的驾驶行为，而是将情绪作为**调节因子**而非**决定因子**融入决策。

### 创新总结

上述三项创新构成了 E3AD 相对于现有 VLA 范式的核心突破：连续 VAD 情绪空间为模型提供了理解人类意图的“情感维度”，双通路空间推理弥补了单一视角的感知盲区，而三阶段一致性训练则将情绪认知与驾驶行为牢固绑定。三者协同作用，使 E3AD 在轨迹规划（Table 1，ADE 相对 PTPC 降低 17.01%）和视觉定位（Table 2，Talk2Car 绝对提升 +6.86%）上均取得显著增益，同时保持了情绪估计的 SOTA 水平（Table 3，Valence Spearman ρ 达 0.95）。



E3AD 的核心设计动机在于弥合现有端到端自动驾驶系统与人类乘客之间的**情感鸿沟**。传统 VLA 模型仅将多视图图像直接映射为规划输出，完全忽视指令中蕴含的情绪色彩与行为紧迫度（Figure 1a），导致系统行为机械化、缺乏共情。E3AD 通过将**连续 VAD 情绪空间建模**、**双通路空间推理**以及**一致性导向的三阶段训练**统一于一个 VLA 框架中（Figure 1b），使模型能够根据指令中的情感信息调整视觉定位与轨迹规划，最终产出更符合人类期望的安全、共情驾驶行为。

### 任务定义与输入输出流

E3AD 将任务形式化为一个开放域端到端自动驾驶映射：

$$f_{\theta} : (I, C) \to \hat{\mathcal{V}} = \{\hat{b}, \hat{\tau}\}$$

给定多视角观测 $I$（包含自我中心前视图与 BEV 环境中心视图）和自然语言指令 $C$，模型需要联合推理并输出指称目标 $\hat{b}$ 与未来轨迹航点序列 $\hat{\tau}$。这一统一策略将视觉定位与路径规划整合为单一自回归生成过程，避免了传统级联式方法中的误差累积。

### 核心模块与信息流

Figure 2 完整展示了 E3AD 的训练与推理管线，其信息流可概括为以下关键环节：

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/002_Figure_2.jpg]]
*Figure 2: Overview of E3AD and its training/inference pipeline. Given egocentric and allocentric views with a natural-language command (a), E3AD outputs emotion, grounding, and waypoint tokens via two core modules: Emotion Modeling (b) encodes commands in continuous VAD space (c), and Spatial Reasoning fuses egocentric and allocentric pathway cues. Training proceeds from Modality Pretraining for emotion/spatial skills (d) to Joint Fine-Tuning that predicts (eˆ, ˆb, τˆ) in a single autoregressive chain (e), followed by Emotion-Action Alignment (f). During inference (g), E3AD runs end-to-end to estimate (eˆ), ground (ˆb), and plan (τˆ), producing human-centric feedback*

1. **多模态感知输入**：系统接收自我中心视图和环境中心视图，配合自然语言驾驶指令（Figure 2a），形成视觉-语言联合输入。

2. **情绪建模模块**：指令首先进入情绪建模模块（Figure 2b），被映射到连续的 Valence-Arousal-Dominance 三维情绪空间 $e \in \mathbb{R}^3$（Figure 2c）。该模块解析指令中的语气、紧迫度等情感信息，为下游决策提供情绪先验。情绪建模采用命令增强策略：对每条原始指令生成多个保持驾驶目标但改变态度/强度的改写版本，并通过监督微调使 VLM 具备连续 VAD 情绪预测能力。

3. **双通路空间推理**：两个互补的空间通路并行处理视觉信息——
   - **自我中心通路**：从前视图预测目标的相对方向、距离及图像坐标，提供即时、短视距的动作导向空间线索；
   - **环境中心通路**：从 BEV 视角预测目标的世界坐标位置并生成粗轨迹，编码道路拓扑、遮挡和多智能体布局等全局结构。
   两条通路的输出被融合，形成兼具局部精度与全局一致性的空间表征。

4. **VLA 主干推理**：以 **Qwen2.5-VL-7B** 为核心多模态推理引擎，融合图像与语言语义，自回归地输出完整序列 $T = (\hat{e}, \hat{b}, \hat{\tau})$，即情绪估计、指称目标和初始轨迹。

5. **动作解码与口头反馈**：VLA 的高层输出经过动作解码器转化为精确、物理可行的最终航点序列；同时，口头反馈生成器根据预测的情感状态、指称目标及规划轨迹，生成带有适当语气与详略程度的口头回应 $\hat{r}$，降低乘客的“黑箱”焦虑。

### 三阶段一致性训练

E3AD 采用渐进式训练策略，逐步赋予模型情绪感知、空间推理和一致决策能力：

- **阶段一：模态预训练**——分别训练情绪预测和空间推理能力，使 VLM 掌握连续 VAD 情绪估计和双通路空间表征；
- **阶段二：联合指令微调**——最小化完整输出序列 $T$ 的自回归负对数似然：

$$\mathcal{L}_{\mathrm{Joint}} = - \mathbb{E}_{(I, C, T)} \sum_{t=1}^{|T|} \log p_{\theta}(T_t \mid T_{<t}, I, C)$$

驱动情绪、定位与规划的一体化推理；

- **阶段三：情绪-动作对齐**——通过构造伪偏好对并采用 DPO 损失进行对齐：

$$\mathcal{L}_{\mathrm{dpo}} = - \mathbb{E}_i \left[ \log \sigma \left( \beta \left( \log p_{\theta}(\tau^{(i)} \mid \mathcal{C}^{(i)}) - \log p_{\theta}(\widetilde{\tau}_{k^{-}}^{(i)} \mid \mathcal{C}^{(i)}) \right) \right) \right]$$

其中负样本轨迹 $\widetilde{\tau}_{k^{-}}^{(i)}$ 来自 VAD 嵌入偏离最大的增强指令，鼓励模型偏好真实轨迹而抑制情绪扭曲的轨迹，实现行为与情感的一致性对齐。

整个框架在推理时端到端运行，从多视图图像和自然语言指令出发，依次完成情绪估计、指称定位和轨迹规划，并生成人本化的口头反馈，形成完整的感知-推理-执行闭环。

### 补充图表

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/001_Figure_1.jpg]]
*Figure 1: Overview of our E3AD. (a) Existing VLAs behave as emotion-agnostic systems, mapping multi-view images directly to a planning output without human-in-the-loop interaction or emotion understanding. (b) Our model adds explicit emotion modeling and closed-loop feedback, allowing the agent to infer intent intensity, ground referents more reliably, and adapt its plan accordingly. (c) This yields the Open-Domain E2E AD task, where the agent jointly reasons over language, emotion, perception, and navigation to enable human-centered and context-aware autonomy*



E3AD 的核心架构围绕三个关键设计展开：连续情绪建模、双通路空间推理，以及三阶段一致性训练。以下逐一剖析各模块的机理与关键公式。

### 连续情绪建模

传统方法或完全忽略情绪，或仅使用离散类别标签（如“愤怒”“开心”），难以刻画驾驶指令中细微的语气变化与紧迫程度。E3AD 引入连续的 **Valence-Arousal-Dominance (VAD)** 三维情绪空间，将任意自然语言指令映射为 $e \in \mathbb{R}^3$，分别编码愉悦度、唤醒度和支配度。

为获取丰富的情绪监督信号，论文采用 **情绪感知命令增强**：对每条原始指令 $C^{(i)}$，利用 Qwen2.5-VL 生成 $K$ 条保持驾驶目标但改变态度/强度的改写指令 $C_{aug}^{(i)} = \{C_1^{(i)}, \dots, C_K^{(i)}\}$，并通过预训练情绪模型为每条改写指令标注 VAD 真值 $e_k^{(i)}$。在模态预训练阶段，模型通过最小化负对数似然学习从指令到 VAD 向量的映射：

$$\mathcal{L}_{\mathrm{emo}} = - \mathbb{E}_{(C_k^{(i)}, e_k^{(i)}) \sim \mathcal{C}^*} \big[ \log p_{\theta}(e_k^{(i)} \mid C_k^{(i)}) \big]$$

该损失使 VLM 主干获得连续情绪预测能力，为后续的指称消歧与轨迹生成提供情绪先验。

### 双通路空间推理

人类的空间认知同时依赖自我中心（egocentric）与环境中心（allocentric）两种参照系。E3AD 据此设计双通路空间推理模块：

- **自我中心通路** 从前视图像预测目标的相对方向、距离及图像坐标，提供即时、短视距的动作导向空间线索。
- **环境中心通路** 从 BEV 视角预测目标的世界坐标位置并生成粗轨迹，编码道路拓扑、遮挡和多智能体布局等全局结构。

两条通路的输出在 VLA 主干中融合，互补地增强 3D 理解与地图一致性。

### 三阶段一致性训练

E3AD 采用渐进式训练策略，逐步赋予模型情绪感知、空间推理与行为对齐能力：

**阶段一：模态预训练。** 分别训练情绪预测（$\mathcal{L}_{\mathrm{emo}}$）和空间推理任务，使主干网络获得领域特化的多模态表征。

**阶段二：联合指令微调。** 将情绪 $e$、指称目标 $b$ 和轨迹航点 $\tau$ 统一为自回归输出序列 $T = (e, b, \tau)$，通过最大化条件概率实现一体化推理：

$$\mathcal{L}_{\mathrm{Joint}} = - \mathbb{E}_{(I, C, T)} \sum_{t=1}^{|T|} \log p_{\theta}(T_t \mid T_{<t}, I, C)$$

**阶段三：情绪-动作对齐。** 为使驾驶行为与情绪表达保持一致，论文引入基于直接偏好优化（DPO）的对齐训练。首先构造伪偏好对：选取 VAD 嵌入偏离最大的增强指令作为负样本，并生成对应的情绪扰动轨迹：

$$C_{k^{-}}^{(i)} = \arg \max_k \| e_k^{(i)} - e^{(i)} \|_2, \quad \widetilde{\tau}_{k^{-}}^{(i)} \sim p_{\theta}(\tau \mid C_{k^{-}}^{(i)}, I^{(i)})$$

随后通过 DPO 损失鼓励模型偏好真实轨迹 $\tau^{(i)}$ 而抑制情绪扭曲的轨迹 $\widetilde{\tau}_{k^{-}}^{(i)}$：

$$\mathcal{L}_{\mathrm{dpo}} = - \mathbb{E}_i \left[ \log \sigma \left( \beta \left( \log p_{\theta}(\tau^{(i)} \mid \mathcal{C}^{(i)}) - \log p_{\theta}(\widetilde{\tau}_{k^{-}}^{(i)} \mid \mathcal{C}^{(i)}) \right) \right) \right]$$

其中 $\sigma$ 为 sigmoid 函数，$\beta$ 控制偏好强度。该阶段有效提升了情绪-轨迹一致性（Figure 4 中 Spearman 相关系数提高）。

### 动作解码与口头反馈

VLA 主干输出的高层语义（目标位置、粗轨迹）经 **Action Decoder** 转化为精确、物理可行的最终航点序列。同时，**Verbal Feedback Generator** 根据预测的情绪状态、指称目标及规划轨迹，生成带有适当语气与详略程度的口头回应，降低乘客的“黑箱”焦虑。

### 补充图表

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/003_Figure_3.jpg]]
*Figure 3: Visualization of emotion distributions before and after augmentation. (a) Proportions of GoEmotion categories across Talk2Car splits. (b) VAD distribution of GoEmotion. (c) Incorporating driving commands enriches emotional diversity. (d) Emotion-aware augmentation expands and smooths the VAD distribution, providing broader and continuous emotion supervision*



## 实验与关键发现

### 端到端轨迹规划主结果

E3AD 在 Talk2Car-Trajectory 基准上全面超越所有现有方法，印证了情绪感知与双通路空间推理对驾驶行为建模的实质性增益。如 Table 1 所示，相较于此前最强的基线 **PTPC**（Grujicic et al., AAAI 2022），E3AD 在平均位移误差（ADE）上降低 17.01%（3.88 vs. 4.54），终点位移误差（FDE）降低 20.00%（6.64 vs. 7.75），Frechet 距离降低 18.26%。在 SSPD 与 PA 指标上同样取得最优，表明模型不仅能更精确地逼近人类驾驶轨迹，还能更可靠地抵达目标区域。

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/004_Table_1.jpg]]
*Table 1: End-to-end performance of E3AD vs. state-of-the-art (SOTA) baselines. Best results are bold; second-best are underlined*

这些提升的因果机制在于：环境中心通路提供的 BEV 全局拓扑信息使模型能够提前感知道路结构与遮挡关系，从而生成更平滑、更符合地图约束的航点序列。消融实验（Table 6）证实，移除环境中心通路后 ADE/FDE 分别恶化约 10.0%/10.1%，验证了该通路对规划质量的不可替代性。

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/009_Table_6.jpg]]
*Table 6: Ablation of core designs in E3AD on waypoint planning*

### 视觉定位主结果

在视觉定位任务上，E3AD 在多个数据集及其挑战性子集上均达到最优性能（Table 2）。在 Talk2Car 测试集上，E3AD 以 80.12% 的准确率超越此前最优方法 **CAVG**（Liao et al., CTR 2024）达 +6.86 个百分点；在 MoCAD 测试集和 DrivePilot 测试集上分别取得 79.64% 和 82.56% 的准确率，绝对增益最高达 +11.63%。

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/005_Table_2.jpg]]
*Table 2: Comparison of E3AD and state-of-the-art baselines on visual grounding tasks. Best results are bold; second-best are underlined*

特别值得关注的是，E3AD 在视觉约束子集（+6.6%）、歧义指令子集（+4.5%）和长文本指令子集（+4.8%）上的提升幅度最为显著。这揭示了情绪建模的核心价值：连续 VAD 向量能够解析指令中的隐含紧迫度与情感色彩，从而在语义模糊或信息密度高的场景中引导模型做出更符合人类意图的指称消歧。消融实验（Table 5）进一步证实，移除情绪建模后，歧义和长文本子集的准确率分别下降 4.5% 和 4.8%，降幅远大于其他子集，说明情绪信号在消解语义不确定性和长距离依赖中扮演不可替代的角色。

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/007_Table_5.jpg]]
*Table 5: Ablation study of E3AD’s core components on visual grounding performance on the Talk2Car (T2C) benchmark, vision constraint (Constr.), ambiguous (Ambg.), and long-context command (Long) test sets. Components: Egocentric pathway (Ego.), Allocentric pathway (Allo.), DPO, and Emotion Modeling (Emo.)*

### 双通路空间推理的互补性

消融实验揭示了自我中心通路与环境中心通路的分工与互补关系。Table 5 显示，移除自我中心通路导致 Talk2Car 视觉定位 IoU 显著下降 7.0%，在视觉约束子集上也下降 6.6%。这是因为自我中心通路提供的相对方向、距离及图像坐标等精细空间线索，直接服务于近距离目标的精确指称。

与之相对，Table 6 表明移除环境中心通路对轨迹规划指标造成约 10% 的性能退化，但对视觉定位的影响相对较小。环境中心通路从 BEV 视角编码道路拓扑、多智能体布局等全局结构信息，这些信息对长时域路径规划至关重要，但对单帧指称定位的边际贡献有限。两条通路的互补性证明，类人的空间认知需要同时具备“以我为中心”的即时感知和“以环境为中心”的结构化理解。

### 情绪-动作对齐的有效性

DPO 训练阶段通过构造伪偏好对，将情绪表达与驾驶行为进行显式对齐。Figure 4 展示了 DPO 训练前后情感-轨迹一致性的变化：Spearman 相关系数在 Valence 和 Arousal 维度上均有提升，表明模型学会了根据指令中的情绪色彩调整轨迹风格。

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/010_Figure_4.jpg]]
*Figure 4: DPO’s effect on emotion-trajectory consistency*

定性案例（Figure 6）进一步佐证了这一效果：当指令带有“谨慎”情绪色彩时，E3AD 会生成更保守的轨迹（更低的规划速度、更大的安全距离），而中性指令下则保持正常驾驶行为。这种情绪-行为的一致性在 217 人用户研究（Figure 7）中得到主观验证——E3AD 在合规性、情绪同步、安全感和偏好等维度均获得最高 Likert 评分。

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/013_Figure_7.jpg]]
*Figure 7: User study on perceived compliance, emotion, safety, and preference. (Left) E3AD consistently achieves high Likert scores across all age groups. (Right) Comparison of Rank-1 votes, E3AD dominates in most dimensions, outperforming all baselines*

### 连续情绪估计性能

Table 3 报告了 E3AD 在 Valence-Arousal-Dominance 三维连续情绪空间上的估计精度。模型在三个维度上均达到最高的 Spearman ρ 和 Kendall τ 相关系数，其中 Valence 维度的 Spearman ρ 高达 0.95，表明模型能够高度一致地捕捉指令中的愉悦-不悦程度。这一能力源于情绪感知命令增强策略（Figure 3）：通过生成保持驾驶目标但变化语气的改写指令，显著扩展和平滑了训练数据的 VAD 分布，使模型获得更丰富的情绪监督信号。

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/006_Table_3.jpg]]
*Table 3: Emotion prediction across valence, arousal, and dominance. Reported metrics are Spearman’s ρ and Kendall’s τ correlations with ground-truth VAD (↑: a higher value is better)*

### 空间推理能力

Table 4 对比了 E3AD 与通用 VLM 基线在空间推理任务上的表现。相较于 **Qwen2.5-VL-7B**（Bai et al., arXiv 2025）等通用模型，E3AD 在目标定位精度和深度估计上均有大幅提升。这得益于双通路空间推理模块引入的显式空间监督：自我中心通路预测相对方向与距离，环境中心通路预测 BEV 坐标与粗轨迹，两者共同将通用 VLM 的语义理解能力锚定到精确的 3D 空间表征中。

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/008_Table_4.jpg]]
*Table 4: Spatial reasoning results on Talk2Car vs. VLM baselines*

### 失败模式与局限性

尽管 E3AD 在离线基准上表现优异，但存在以下已知局限：

1. **情绪信号来源单一**：当前仅利用自然语言文本中的情绪信息，尚未融合面部表情、语音语调等多模态情绪线索。在真实驾驶场景中，乘客的非语言情感表达可能携带重要的补充信息，遗漏这些信号可能导致情绪估计偏差。

2. **缺乏闭环验证**：所有评估均在离线数据集上进行，未在高保真仿真器中测试动态交互场景下的安全性与鲁棒性。语言反馈与实时控制的频率、延迟及计算开销亦未讨论，实际部署可行性需进一步工程验证。

3. **伪偏好对质量依赖**：DPO 对齐阶段依赖命令改写生成负样本，若部分增强指令的情绪偏移与驾驶行为变化并不一致，可能引入训练噪声，削弱对齐效果。这一风险在极端情绪表达场景下尤为突出。

4. **安全边界的模糊性**：当指令带有强烈的紧迫情绪时，模型如何在响应情绪需求与维持安全边界之间取得平衡，尚未建立明确机制。这是情绪感知自动驾驶走向实际应用前必须解决的关键问题。

### 补充图表

![[assets/figures/papers/paper_list_l2386_https_arxiv_org_abs_2512_04733/figures/011_Figure_5.jpg]]
*Figure 5: Qualitative comparison between E3AD and FSDrive-FT in emotion-rich (a), multi-agent (b), and ambiguous (c) scenes*



## 定位与知识库关联

### 1. 任务定义与范式演进

E3AD 将端到端自动驾驶的任务空间从传统的“视觉-语言-动作”三元组扩展为“视觉-语言-情绪-动作”四元组，其核心映射形式化为：

$$f_{\theta} : (I, C) \to \hat{\mathcal{V}} = \{\hat{b}, \hat{\tau}\}$$

其中 $I$ 为多视角观测，$C$ 为自然语言指令，输出包括指称目标 $\hat{b}$ 与未来轨迹航点 $\hat{\tau}$（Eq.1）。这一范式在以下三个维度上区别于现有工作：

- **情绪维度**：传统 VLA 系统（如 **FSDrive-Finetuned** (Zeng et al., arXiv 2025)、**CAVG** (Liao et al., CTR 2024)）将驾驶建模为纯理性决策，完全忽略指令中的情感色彩与紧迫程度。E3AD 首次将连续 Valence-Arousal-Dominance (VAD) 情绪空间引入端到端驾驶，使模型能够从“快点开”与“慢慢开”等语义相近但情绪迥异的指令中解析出不同的行为意图。
- **空间维度**：现有方法多依赖单一自我中心视角，缺乏对环境全局结构的显式建模。E3AD 提出双通路空间推理——自我中心通路提供相对方向/距离/图像坐标的即时线索，环境中心通路从 BEV 视角编码道路拓扑与多智能体布局，两者互补形成类人的空间认知。
- **训练维度**：不同于标准指令微调 (SFT) 或直接微调的单阶段范式，E3AD 采用三阶段一致性训练——模态预训练（情绪+空间）→ 联合微调（统一自回归预测 $e, b, \tau$）→ 情绪-动作对齐（DPO with pseudo-preference pairs），逐层注入情感感知与行为一致性。

### 2. 与关键基线的方法论差异

#### 2.1 对比 PTPC（Grujicic et al., AAAI 2022）

**PTPC** 是基于目标预测的轨迹规划方法，在 E3AD 的轨迹规划评测中作为最强基线出现（Table 1）。其核心思路是通过预测目标位置来引导轨迹生成，但完全不具备语言理解与情绪感知能力。E3AD 在 PTPC 的基础上实现了三重跨越：
- 引入自然语言指令作为驾驶意图的输入源，替代隐式的目标预测；
- 通过 VAD 情绪建模解析指令中的紧迫度与态度，使轨迹规划从“目标驱动”升级为“意图+情绪驱动”；
- 利用 VLA 主干（Qwen2.5-VL-7B, Bai et al., arXiv 2025）的多模态推理能力，实现视觉定位与轨迹规划的统一自回归生成。

实验表明，E3AD 在 ADE 上较 PTPC 降低 17.01%，FDE 降低 20.00%（Table 1），证明情绪感知与语言理解对轨迹规划的增益远超纯视觉目标预测范式。

#### 2.2 对比 CAVG（Liao et al., CTR 2024）

**CAVG** 融合 GPT-4 增强跨模态注意力，是现有情感感知驾驶的代表性工作。E3AD 与 CAVG 的关键差异在于情绪表示的空间选择：
- CAVG 使用离散情绪类别（如 happy/angry），信息粒度粗糙且难以刻画情绪的连续渐变；
- E3AD 采用连续 VAD 三维空间（$e \in \mathbb{R}^3$），能够捕捉“略微着急”与“非常焦虑”之间的细微差异，并通过情绪感知命令增强（Eq.2）扩展训练分布。

在 Talk2Car 视觉定位任务上，E3AD 达到 80.12% 准确率，较 CAVG 的 74.62% 绝对提升 +6.86%（Table 2），且在歧义指令和长文本指令子集上增益更为显著（分别 +4.5%/+4.8%，Table 5 消融实验），证实连续情绪空间在消解语义模糊和长距离依赖中的不可替代性。

#### 2.3 对比 FSDrive-Finetuned（Zeng et al., arXiv 2025）

**FSDrive-Finetuned** 代表当前基于 VLM 的端到端自动驾驶范式，经微调后用于命令驱动场景。E3AD 与其共享 VLM 主干的思想，但在以下方面形成差异化：
- FSDrive-FT 缺乏显式的情绪建模模块，将指令视为纯语义输入；
- E3AD 的情绪建模模块独立于 VLA 主干，通过模态预训练先赋予模型 VAD 预测能力，再在联合微调中与定位/规划任务融合，避免情绪信号被其他任务淹没；
- E3AD 引入 DPO 对齐阶段（Eq.4-5），利用伪偏好对约束情绪-轨迹一致性，而 FSDrive-FT 仅使用标准 SFT。

定性对比（Figure 5）显示，在情绪丰富、多智能体和歧义场景中，E3AD 的行为更符合人类期望，而 FSDrive-FT 倾向于产生情绪不敏感的“平均化”响应。

### 3. 适用边界与泛化约束

#### 3.1 情绪信号的模态局限

当前 E3AD 仅利用自然语言文本中的情绪信号进行 VAD 建模，尚未融合面部表情、语音语调等多模态情绪信息。这意味着：
- 当乘客的语言表达与真实情绪状态不一致时（如强忍焦虑说“没事，正常开”），模型无法通过视觉或语音线索进行校准；
- 在无声场景（如乘客沉默但面部表情紧张）中，情绪感知模块完全失效。

#### 3.2 数据集与场景覆盖

所有评估均在离线真实驾驶数据集（Talk2Car、MoCAD、DrivePilot）上进行，缺乏高保真仿真器中的闭环测试。这带来两个潜在风险：
- 数据集中的驾驶行为分布可能偏向“理性”轨迹，对极端情绪场景（如紧急避险时的恐慌指令）覆盖不足；
- 离线评估无法验证模型在动态交互中的累积误差与安全边界，例如连续多轮情绪反馈是否会导致轨迹发散。

#### 3.3 伪偏好对构造的噪声风险

DPO 对齐阶段依赖情绪感知命令增强构造伪偏好对（Eq.4）：选取 VAD 嵌入偏离最大的增强指令作为负样本，并生成对应的情绪扰动轨迹。如果部分增强指令的情绪偏移与驾驶行为变化并不一致（如改写后的“火速开过去”在实际场景中不应导致轨迹剧烈变化），则伪偏好对可能引入训练噪声，误导模型学习虚假的情绪-行为关联。

#### 3.4 计算开销与实时性

E3AD 以 Qwen2.5-VL-7B 为 VLA 主干，所有实验在 8×NVIDIA H200 GPU 上运行。尽管仅训练低秩适配器以控制可训练参数量，但推理时仍需完整的 7B 参数前向传播，加上双通路空间推理与自回归生成的语言反馈，实际部署时的延迟与计算开销尚未讨论。在需要毫秒级响应的实时控制场景中，这可能需要模型蒸馏或高效推理优化。

### 4. 开放问题

1. **安全-情绪的权衡机制**：如何在融入情绪理解的同时，确保安全边界不被情绪表达所突破？例如，“快开！快开！”的紧急指令不应导致违反交通规则或危险驾驶行为。这需要在 DPO 对齐或推理阶段引入硬安全约束。

2. **跨文化与个体差异泛化**：连续 VAD 情绪模型在不同文化背景、语言习惯及个体性格差异下的泛化能力如何？同一句“开快点”在不同文化中的情绪强度可能截然不同，当前基于 GoEmotion 的 VAD 标注可能偏向英语文化。

3. **多模态情绪融合**：若进一步引入多模态情绪信号（如车内摄像头捕捉的表情），如何有效对齐语言与视觉情感表征，避免模态不一致？例如，乘客笑着说“我快迟到了”时，语言与视觉的情绪信号可能冲突。

4. **法规与伦理框架**：在自动驾驶法规与伦理框架下，车辆根据乘客情绪调整驾驶行为是否可能引发责任划分问题？如果系统因响应“着急”指令而加速导致事故，责任应由乘客、制造商还是算法承担？这需要在技术方案之外进行制度设计。



## 原文 PDF

![[paperPDFs/CVPR_2026/E3AD_An_Emotion_Aware_Vision_Language_Action_Model_for_Human_Centric_End_to_End_Autonomous_Driving.pdf]]
