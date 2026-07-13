---
title: "VisMem: Latent Vision Memory Unlocks Potential of Vision-Language Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/VisMem_Latent_Vision_Memory_Unlocks_Potential_of_Vision_Language_Models.pdf
project_link: null
code_link: "https://github.com/YU-deep/VisMem.git"
aliases:
- VisMem
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/generative_models_diffusion
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 在VLM的潜在空间中引入动态的、认知对齐的双重记忆系统（视觉主导的短期记忆和语义主导的长期记忆），通过可训练的调用机制在需要时插入细粒度感知或抽象语义标记。
primary_logic: 模仿人类记忆理论，将短期视觉记忆和长期语义记忆内化为轻量级潜在记忆标记，无需修改核心VLM参数，即可在生成过程中同时保持感知保真度和语义一致性，从而突破视觉处理瓶颈。
claims:
- VisMem 在12个综合视觉基准上相比 vanilla 模型平均提升11.0%，且在所有15个基线中排名第一。
- 在 MuirBench 的细粒度子任务（如计数、视觉检索、grounding）上分别提升 +7.0%、+9.4% 和 13.1%。
- 跨域泛化实验中，仅用两个数据集训练，VisMem 在四个未见基准上仍保持显著领先，与全量训练数据差距仅约2%。
- 四阶段连续学习后，VisMem 在 MMVet 上保留 72.1% 的性能，灾难性遗忘最轻微。
---

# VisMem: Latent Vision Memory Unlocks Potential of Vision-Language Models

> [!tip] 核心洞察
> 模仿人类记忆理论，将短期视觉记忆和长期语义记忆内化为轻量级潜在记忆标记，无需修改核心VLM参数，即可在生成过程中同时保持感知保真度和语义一致性，从而突破视觉处理瓶颈。

| 字段 | 内容 |
|------|------|
| 中文题名 | VisMem：潜在视觉记忆释放视觉语言模型潜力 |
| 英文题名 | VisMem: Latent Vision Memory Unlocks Potential of Vision-Language Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2511.11007) · [Code](https://github.com/YU-deep/VisMem.git) |
| Topic | #topic/vision_multimodal_applications #topic/generative_models_diffusion #topic/vision_multimodal_applications/image_and_video_generation |
| Method | VisMem |
| Dataset | MMStar, MMVet, MuirBench, MMMU |

> [!tip] 效果简介
> - MMStar 上，准确率 68.9 vs 62.6 (Vanilla) (+6.3)。
> - MMVet 上，准确率 75.1 vs 66.0 (Vanilla) (+9.1)。
> - MuirBench 上，准确率 69.8 vs 57.4 (Vanilla) (+12.4)。

## 概要

当前视觉语言模型（VLM）在自回归解码过程中面临一个系统性的**视觉处理瓶颈**：模型倾向于优先累积文本上下文，逐渐丢失对初始视觉证据的 grounding，同时缺乏上下文化的视觉语义经验，导致在细粒度理解、多步推理和长序列生成任务上性能显著下降。

针对这一问题，**VisMem** 提出了一种全新的**潜在空间范式**（Figure 1），其核心思想是模仿人类记忆理论中的双重记忆系统——将短期视觉记忆与长期语义记忆内化为轻量级的潜在记忆标记，在不修改核心 VLM 参数的前提下，于生成过程中按需插入细粒度感知或抽象语义信息。

该方法在 12 个综合视觉基准上的实验表明，VisMem 相较 vanilla 模型平均提升 **11.0%**，在所有 15 个基线方法中排名第一。尤其在 MuirBench 的细粒度子任务上，计数、视觉检索和 grounding 分别提升 **+7.0%**、**+9.4%** 和 **+13.1%**；在 MV-Math 上更是取得了 **+22.5%** 的显著增益。此外，VisMem 展现出优异的跨域泛化能力（与全量训练数据差距仅约 2%）和灾难性遗忘抵抗能力（四阶段连续学习后 MMVet 性能保留 **72.1%**），并兼容多种基座模型（Qwen2.5-VL、LLaVA-OV-1.5、InternVL-3.5 等），在推理效率与性能之间取得了良好的平衡。

### 视觉语言模型的“视觉处理瓶颈”

视觉语言模型（VLM）近年来在视觉问答、图像描述等任务上取得了显著进展，但在需要细粒度视觉理解、多步推理和长序列生成的高阶场景中，其性能仍远落后于文本端的能力。这一差距的根源并非视觉编码器提取特征的能力不足，而是自回归解码过程中存在一个系统性的**视觉处理瓶颈**：随着生成序列的增长，VLM 倾向于优先累积文本上下文，逐渐丢失对初始视觉证据的 grounding，同时缺乏上下文化的视觉语义经验来支撑复杂的推理链。简而言之，模型“看到”了图像，却无法在生成过程中持续“记住”并有效利用视觉信息。

### 现有方法的四种范式及其局限

为缓解上述瓶颈，已有方法可大致归为四种范式（如 Figure 1 所示），但各有其根本性缺陷：

1. **直接训练范式**：通过监督微调（SFT）或强化学习（如 **Visual-RFT**、**VLM-R1**、**Vision-R1**、**PAPO**）直接优化 VLM 的参数。这类方法虽然通用，但完全依赖模型自身从数据中隐式学习视觉 grounding，缺乏对视觉记忆的显式建模，在细粒度任务上提升有限。

2. **图像级范式**：在推理时引入额外的视觉处理模块（如 **Sketchpad**、**GRIT**、**PixelReasoner**、**DeepEyes**、**OpenThinkImg**），对图像进行再编码或生成辅助视觉标记。然而，这些方法通常需要额外的视觉编码器或生成器，计算开销大，且与原始 VLM 的集成是非侵入式的，难以在自回归循环中灵活调用。

3. **Token 级范式**：在文本序列中插入额外的视觉 token（如 **Scaffold**、**ICoT**、**MINT-CoT**、**VPT**），试图在 token 空间保持视觉信息。但这类方法将视觉信息硬编码为离散 token，损失了视觉特征的连续性和丰富性，且容易与文本 token 产生干扰。

4. **潜在空间范式**：在 VLM 的潜在空间中操作视觉信息（如 **Mirage**），避免 token 化损失。但现有方法缺乏对视觉记忆的结构化建模——没有区分短期感知与长期语义，也没有动态的调用机制，导致记忆的利用效率低下。

### VisMem 的核心动机：从人类记忆理论到潜在视觉记忆

VisMem 的核心动机源于一个认知科学洞见：人类在视觉推理时，并非一次性编码所有细节，而是依赖**双重记忆系统**——**短期视觉记忆**保持当前场景的感知细节（如物体的颜色、位置、纹理），**长期语义记忆**存储抽象的概念知识（如“这是一只猫”的类别信息）。两种记忆在需要时被灵活调用，共同支撑复杂的视觉推理。

受此启发，VisMem 提出了一种全新的潜在视觉记忆框架，其设计原则包括：

- **非侵入式集成**：通过扩展 VLM 词汇表引入特殊记忆操作标记，而非修改核心 VLM 参数，实现即插即用的记忆增强。
- **双重记忆形成**：分别设计**短期记忆形成器**（编码细粒度感知证据）和**长期记忆形成器**（编码抽象语义知识），在潜在空间中生成轻量级记忆标记。
- **动态按需调用**：引入可训练的查询构建器，基于当前解码上下文自适应地决定何时调用何种记忆，避免无效调用对生成质量的负面影响。

这一设计使得 VisMem 能够在自回归生成过程中同时保持感知保真度和语义一致性，从根本上突破视觉处理瓶颈，而非仅仅在特定任务上“打补丁”。

## 核心方法与创新机理

VisMem 的核心创新在于将认知心理学中的双重记忆理论内化为 VLM 潜在空间中的轻量级记忆系统，通过**非侵入式的词汇表扩展**和**基于强化学习的动态调用机制**，在不修改核心 VLM 参数的前提下，从根本上缓解了自回归解码过程中的“视觉处理瓶颈”。其关键创新点体现在以下三个 changed slots 上：

### 1. 记忆操作原语：非侵入式词汇表扩展

VisMem 在标准 VLM 词汇表 $V$ 上增加了四个不可分割的特殊记忆操作标记——`<m_I^s>`、`<m_E^s>`、`<m_I^l>`、`<m_E^l>`，分别对应短期/长期记忆的调用起始与结束。这些标记被注册到 tokenizer 中，并将嵌入矩阵从 $\mathbb{R}^{|V| \times d}$ 扩展至 $\mathbb{R}^{(|V|+4) \times d}$。在自回归生成过程中，当模型输出调用标记时，立即触发记忆形成流程，生成的潜在记忆标记与结束标记被无缝插入到 token 序列中，随后模型在其上下文中继续解码。这一设计使得记忆调用完全融入 VLM 原有的生成范式，无需改变模型架构或推理管线。

### 2. 认知对齐的双重记忆形成器

VisMem 引入两个轻量级 LoRA 适配器作为记忆形成器，分别附加在视觉编码器和语言模型上：
- **短期记忆形成器 $F_s$**：生成 $N_s$ 个细粒度、视觉主导的潜在记忆标记，编码当前视觉输入的丰富感知证据；
- **长期记忆形成器 $F_l$**：生成 $N_l$ 个语义主导的潜在记忆标记，编码抽象的高层视觉语义知识。

记忆形成过程由一个轻量级 Transformer 编码器 $B$（查询构建器）驱动：$B$ 读取当前多模态隐藏状态 $H$ 和可学习的初始查询 $Q_{init}$，生成上下文感知的记忆查询 $Q = B([H, Q_{init}])[-K:]$。随后，记忆形成器基于目标序列 $X$、查询 $Q$ 和可学习的记忆标记初始值，生成潜在记忆标记 $M_{s/l} = F_{s/l}([X, Q, M_{init}])[-N_{s/l}:]$。这种双重记忆设计模仿了人类记忆中“感知暂存”与“语义固化”的分工，使模型在生成过程中同时保持感知保真度和语义一致性。

### 3. 基于 GRPO 的两阶段强化学习训练

VisMem 采用基于 GRPO 的两阶段训练范式，分别优化记忆形成质量和记忆调用策略：
- **阶段一（记忆形成优化）**：冻结策略模型 $P$，最大化引入记忆后的性能增量 $\Delta S(\tau)$，更新查询构建器 $B$ 和记忆形成器 $F_{s/l}$，确保生成的潜在记忆标记对任务有正向贡献；
- **阶段二（记忆调用优化）**：冻结记忆组件，更新策略模型 $P$ 的部分参数 $\theta$，在最大化性能增量的同时引入两项惩罚——错误记忆类型惩罚 $p_{type}$ 和负回报调用惩罚 $p_{neg}$，引导模型学会在合适的时机调用合适的记忆类型。

这种解耦训练策略使得记忆系统的形成能力和调用能力分别得到充分优化，避免了端到端训练中可能出现的耦合退化问题。消融实验表明，随机调用概率在 75% 时性能达到峰值，100% 全量调用反而导致性能下降，验证了动态调用机制的必要性和有效性。

VisMem 的整体设计遵循“按需调用、双记忆协同”的原则，在不修改核心 VLM 参数的前提下，通过潜在空间中的轻量级记忆模块增强视觉处理能力。其 pipeline 由四个关键模块串联而成：**词汇表扩展** → **查询构建器** → **记忆形成器** → **记忆调用与插入**，最终无缝嵌入自回归解码流程。

**1. 词汇表扩展与调用触发**

VisMem 首先在 VLM 的标准词汇表 $\mathcal{V}$ 中注册四个不可分割的特殊记忆操作 token：`<m_I^s>`、`<m_E^s>`、`<m_I^l>`、`<m_E^l>`，分别表示短期记忆的调用/结束和长期记忆的调用/结束。对应的嵌入矩阵从 $\mathbb{R}^{|\mathcal{V}| \times d}$ 扩展至 $\mathbb{R}^{(|\mathcal{V}|+4) \times d}$。在自回归生成过程中，当策略模型 $\mathcal{P}$ 采样出调用 token 时，记忆形成流程被立即触发：

$$x_{t,i} \to \begin{cases} \text{invocation}, & x_{t,i} \in \{<m_I^s>, <m_I^l>\} \\ \text{continue}, & \text{otherwise} \end{cases}$$

这一设计使得记忆调用完全由模型自主决策，无需外部干预。

**2. 查询构建器（Query Builder）**

记忆调用的前置模块是一个轻量级 Transformer 编码器 $\mathcal{B}$。它接收当前多模态隐藏状态 $\mathbf{H}$ 与可学习的初始查询 $\mathbf{Q}_{init}$ 的拼接，输出上下文感知的记忆查询：

$$\mathbf{Q} = \mathcal{B}([\mathbf{H}, \mathbf{Q}_{init}])[-K:]$$

其中 $K$ 为查询长度，默认设为 8。查询 $\mathbf{Q}$ 编码了当前视觉输入和文本上下文的联合信息，用于引导后续记忆内容的检索与生成。

**3. 双重记忆形成器（Memory Formers）**

两个轻量级 LoRA 适配器分别承担短期与长期记忆的生成任务：

- **短期记忆形成器 $\mathcal{F}_s$**：附加在视觉编码器上，生成细粒度、视觉主导的潜在记忆标记，编码当前输入的丰富感知证据（如物体位置、纹理、数量等）。
- **长期记忆形成器 $\mathcal{F}_l$**：附加在语言模型上，生成语义主导的潜在记忆标记，编码抽象的高层视觉语义知识（如类别概念、场景语义等）。

两者的生成过程统一为：

$$\mathbf{M}_{s/l} = \mathcal{F}_{s/l}([\mathbf{X}, \mathbf{Q}, \mathbf{M}_{init}])[-N_{s/l}:]$$

其中 $\mathbf{X}$ 为目标序列，$\mathbf{M}_{init}$ 为可学习的记忆标记初始值，$N_s$ 和 $N_l$ 分别为短期和长期记忆标记的长度（默认 $N_s=8$，$N_l=16$）。

**4. 记忆插入与解码恢复**

生成的潜在记忆标记 $\mathbf{M}_{s/l}$ 被插入到已输出的调用 token 之后，紧接着自动追加对应的结束 token（`<m_E^s>` 或 `<m_E^l>`）。此后，VLM 在包含记忆标记的扩展上下文中继续自回归生成：

$$x_{t,i} \sim \mathcal{P}(\cdot \mid s_t, x_{t,<i}, \{m_I, m_1, \dots, m_N, m_E\})$$

整个插入过程对原始解码流程无侵入性——记忆标记作为特殊的潜在向量直接参与后续的注意力计算，但不会改变 VLM 自身的参数结构。

**5. 两阶段训练范式**

VisMem 采用基于 GRPO 的两阶段强化学习策略：

- **阶段一（记忆形成优化）**：冻结策略模型 $\mathcal{P}$，仅更新查询构建器 $\mathcal{B}$ 和记忆形成器 $\mathcal{F}_{s/l}$，最大化引入记忆后的性能增量 $\Delta S(\tau)$。
- **阶段二（记忆调用优化）**：冻结记忆组件，更新策略模型的部分参数 $\theta$，在最大化性能增量的同时引入记忆类型惩罚 $p_{type}$ 和负回报惩罚 $p_{neg}$，引导模型学会何时调用何种记忆。

总体优化目标为联合最大化策略模型与记忆系统的期望性能：

$$\max_{\mathcal{P},\mathcal{M}} \mathbb{E}_{(I,V)\sim\mathcal{D},\tau\sim(\mathcal{P},\mathcal{M})}[S(\tau)]$$

这一设计使得 VisMem 能够以 **8.2%–43.8%** 的额外推理延迟为代价，在 12 个视觉基准上实现平均 **11.0%** 的性能提升，且兼容 Qwen2.5-VL、LLaVA-OV-1.5、InternVL-3.5 等多种基座模型。

![[assets/figures/papers/paper_list_l2358_https_arxiv_org_abs_2511_11007/figures/002_Figure_2.jpg]]
*Figure 2: The overview of our proposed VisMem*

### 问题形式化与自回归生成瓶颈

给定视觉输入 $I$ 和文本指令 $V$，VLM 在环境状态 $s_t$ 下以自回归方式逐 token 生成输出序列。标准解码过程为：

$$x_{t,i} \sim \mathcal{P}(\cdot \mid s_t, x_{<i})$$

其中 $x_{t,i}$ 表示时间步 $t$ 的第 $i$ 个输出 token，$\mathcal{P}$ 为策略模型（即 VLM 本身）。然而，随着文本序列的累积，模型逐渐丧失对初始视觉证据的 grounding，形成“视觉处理瓶颈”。VisMem 的核心思路是在此生成过程中引入潜在视觉记忆，将优化目标扩展为：

$$\max_{\mathcal{P},\mathcal{M}} \mathbb{E}_{(I,V)\sim\mathcal{D},\tau\sim(\mathcal{P},\mathcal{M})}[S(\tau)]$$

其中 $\mathcal{M}$ 表示记忆系统，$S(\tau)$ 为轨迹 $\tau$ 的性能评分，$\mathcal{D}$ 为任务分布。该目标要求策略模型与记忆系统联合优化，使模型在需要时主动调用视觉记忆以增强生成质量。

### 记忆调用机制：词汇表扩展与触发逻辑

VisMem 通过非侵入式地扩展 VLM 词汇表来实现记忆调用。具体而言，在原始词汇表 $\mathcal{V}$ 上增加四个特殊记忆操作 token：

$$\tilde{\mathcal{V}} = \mathcal{V} \cup \{ <m_I^s>, <m_E^s>, <m_I^l>, <m_E^l> \}$$

其中 $<m_I^s>$ 和 $<m_I^l>$ 分别为短期和长期记忆的调用触发 token，$<m_E^s>$ 和 $<m_E^l>$ 为对应的结束 token。这些 token 被注册为不可分割的特殊 token，嵌入矩阵从 $\mathbb{R}^{|\mathcal{V}|\times d}$ 扩展至 $\mathbb{R}^{(|\mathcal{V}|+4)\times d}$。

在自回归解码过程中，触发逻辑由以下条件分支决定：

$$x_{t,i} \to \begin{cases} \text{invocation}, & x_{t,i}\in\{<m_I^s>, <m_I^l>\} \\ \text{continue}, & \text{otherwise} \end{cases}$$

当模型生成调用 token 时，记忆系统立即启动记忆形成过程，生成 $N$ 个潜在记忆标记 $\{m_1, \dots, m_N\}$，随后自动追加结束 token，恢复正常的逐 token 解码：

$$x_{t,i} \sim \mathcal{P}(\cdot \mid s_t, x_{t,<i}, \{m_I, m_1,\dots,m_N, m_E\})$$

这种设计使记忆标记无缝嵌入生成流，不破坏 VLM 原有的自回归架构。

### 记忆形成：查询构建器与双重记忆形成器

记忆形成过程依赖两个核心组件：查询构建器 $\mathcal{B}$ 和记忆形成器 $\mathcal{F}_{s/l}$。

**查询构建器** $\mathcal{B}$ 是一个轻量级 Transformer 编码器。它读取当前多模态隐藏状态 $\mathbf{H}$ 和可学习的初始查询 $\mathbf{Q}_{init}$，生成上下文感知的记忆查询：

$$\mathbf{Q} = \mathcal{B}([\mathbf{H}, \mathbf{Q}_{init}])[-K:]$$

即取编码器输出的最后 $K$ 个向量作为记忆查询，用于检索相应的潜在记忆内容。默认配置中 $K=8$。

**短期记忆形成器** $\mathcal{F}_s$ 和**长期记忆形成器** $\mathcal{F}_l$ 分别为附加在视觉编码器和语言模型上的轻量级 LoRA 适配器。给定目标序列 $\mathbf{X}$、记忆查询 $\mathbf{Q}$ 和可学习记忆初始值 $\mathbf{M}_{init}$，记忆标记的生成过程为：

$$\mathbf{M}_{s/l} = \mathcal{F}_{s/l}([\mathbf{X}, \mathbf{Q}, \mathbf{M}_{init}])[-N_{s/l}:]$$

其中 $N_s$ 和 $N_l$ 分别为短期和长期记忆标记的预设长度，默认取 $N_s=8$、$N_l=16$，可从 $\{2, 4, 8, 16, 32\}$ 中选择。短期记忆形成器编码细粒度的视觉感知证据，长期记忆形成器则合成抽象的高层语义知识，二者在功能上互补。

### 两阶段强化学习训练目标

VisMem 采用基于 GRPO 的两阶段训练范式，分别优化记忆形成和记忆调用。

**阶段一：记忆形成优化。** 冻结策略模型 $\mathcal{P}$，优化查询构建器 $\mathcal{B}$ 和记忆形成器 $\mathcal{F}_{s/l}$，目标是最大化引入记忆后的性能增量：

$$\max_{\mathcal{F}_{s/l},\mathcal{B}} \mathbb{E}_{\tau\sim\mathcal{P}(\cdot|x,\mathbf{M}_{s/l}), \mathbf{M}_{s/l}\sim\mathcal{F}_{s/l}(\mathbf{Q}), \mathbf{Q}\sim\mathcal{B}(\mathbf{H})}[\Delta S(\tau)]$$

其中 $\Delta S(\tau)$ 表示相对于无记忆集成的轨迹的性能提升。

**阶段二：记忆调用优化。** 冻结记忆组件，优化策略模型 $\mathcal{P}$ 的部分参数 $\theta$，使其学会在恰当的时机调用正确的记忆类型。目标函数在最大化性能增量的同时，引入两项惩罚：

$$\max_{\theta} \mathbb{E}_{\tau\sim\mathcal{P}(\cdot|x,\mathbf{M}_{s/l})}[\Delta S(\tau) - \alpha(p_{type}+p_{neg})]$$

其中 $p_{type}$ 惩罚调用错误类型的记忆（如需要细粒度感知时却调用了长期语义记忆），$p_{neg}$ 惩罚产生负回报的调用（即调用记忆后性能反而下降），$\alpha$ 为平衡系数。这种设计促使模型形成稀疏而精准的记忆调用策略——实验表明，随机调用概率在 75% 时性能达到峰值，100% 全量调用反而导致性能下降。

## 实验与关键发现

### 主实验结果：12 基准上的全面领先

VisMem 在覆盖视觉理解、推理和生成三大能力的 12 个基准上，与 15 个基线方法进行了系统对比。实验结果表明，VisMem 在所有基准上均取得最优或次优成绩，整体平均得分达到 **65.5**，相比 vanilla 模型（54.5）提升 **11.0%**，相比第二名方法亦有显著领先（Table 1）。

![[assets/figures/papers/paper_list_l2358_https_arxiv_org_abs_2511_11007/figures/003_Table_1.jpg]]
*Table 1: Results on 12 benchmarks to evaluate visual understanding, reasoning and generation abilities. The best and second best values are emphasized, and the average values are calculated for both specific capabilities and overall results*

在理解能力维度，VisMem 在 MMStar、MMVet、MuirBench 等 6 个基准上平均得分 **68.2**，其中 MuirBench 提升最为显著（+12.4），验证了记忆系统对细粒度视觉证据保持的核心价值。在推理能力维度，VisMem 在 MathVista 和 MV-Math 上分别取得 **79.8** 和 **41.4**，较 vanilla 模型分别提升 +12.0 和 +22.5，后者尤为突出——该基准要求从多模态输入中提取数学关系，对视觉上下文的持续 grounding 要求极高，VisMem 的双重记忆机制恰好弥补了 VLM 在此类任务上的视觉遗忘缺陷。

在生成能力维度，VisMem 同样保持领先，表明潜在记忆标记不仅增强了感知与推理，也未损害语言生成的流畅性。

### 细粒度能力分析：记忆系统的差异化贡献

在 MuirBench 的 9 个子任务上（Table 5），VisMem 在计数（+7.0%）、视觉检索（+9.4%）和 grounding（+13.1%）等依赖细粒度视觉证据的任务上大幅领先第二名方法。值得注意的是，**仅使用短期记忆**在这些子任务上表现更优，而**仅使用长期记忆**在 MV-Math 上表现更佳——这直接验证了两种记忆的互补性：短期记忆编码丰富的感知细节，服务于定位与计数；长期记忆编码抽象语义，服务于数学推理中的概念关联。

在 LogicVista 的 10 个子集上（Table 6），VisMem 同样在推理技能和能力维度均保持领先，进一步证实记忆系统对逻辑推理的普适增益。

### 消融实验：记忆组件与调用策略的因果验证

消融实验（Table 3/Table 9）揭示了几个关键因果机制：

![[assets/figures/papers/paper_list_l2358_https_arxiv_org_abs_2511_11007/figures/009_Table_3.jpg]]
*Table 3: Ablations of latent vision memory invocation and dual latent vision memory formation*

1. **双重记忆的必要性**：完整 VisMem（双记忆+动态调用）在所有基准上性能最优。仅保留短期记忆在 MuirBench 和多信任度上更佳，仅保留长期记忆在 MV-Math 上更佳，二者单独使用均无法覆盖全部任务类型，验证了认知对齐的双记忆设计的合理性。

2. **调用概率的非单调效应**：随机调用概率在 **75%** 时性能达到峰值，100% 全量调用反而导致性能下降（如 Mimics 基准从 73.6 降至 73.4）。这表明并非所有生成步骤都需要视觉记忆增强——过度调用可能引入与当前上下文无关的视觉信息，干扰语言模型的生成连贯性。当前动态调用机制虽已有效，但仍有优化空间。

3. **记忆长度与性能的权衡**：增大记忆查询长度 K 和记忆标记长度 N_s、N_l 从 2 到 32 可进一步提升性能，但计算成本随之增加（Table 10, 11）。这表明记忆容量是性能的“可调节旋钮”，但需在精度与效率间取舍。

### 跨域泛化与灾难性遗忘缓解

跨域泛化实验（Figure 3, Table 7）中，模型仅在 Visual CoT 和 Mulberry 两个数据集上训练，随后在四个未见基准上评估。VisMem 在所有未见基准上仍保持显著领先，与使用全量训练数据的性能差距仅约 2%。这得益于记忆模块的轻量化设计——LoRA 适配器仅学习如何从冻结的 VLM 中提取和注入视觉记忆，而非改变核心视觉-语言映射，因此对训练数据分布的过拟合风险更低。

![[assets/figures/papers/paper_list_l2358_https_arxiv_org_abs_2511_11007/figures/013_Table_7.jpg]]
*Table 7: Results of various models with full training datasets and partial datasets (Visual CoT [42] and Mulberry [71]), and evaluated across four benchmarks*

四阶段连续学习实验（Figure 4, Table 8）进一步验证了 VisMem 对灾难性遗忘的抵抗力。经过四个阶段的序贯训练后，VisMem 在 MMVet 上保留 **72.1%** 的性能，优于 DeepEyes（68.4%）和 Mirage（67.0%）。原因在于记忆形成器 F_s/F_l 与策略模型 P 在两阶段训练中被解耦优化（Eq. 7-8），新任务训练主要更新记忆组件，对原有视觉理解能力的干扰较小。

### 效率分析：性能-延迟的最优平衡

推理效率分析（Figure 6, Table 12）显示，VisMem 引入的额外推理延迟仅为 vanilla 模型的 **8.2%–43.8%**，远优于大多数图像级方法（如 Sketchpad、GRIT 等需要额外视觉编码步骤的方法），也优于部分 token 级方法。在性能-延迟散点图（Figure 6）上，VisMem 位于 Pareto 前沿，表明其在同等延迟下实现了最高的性能增益。

![[assets/figures/papers/paper_list_l2358_https_arxiv_org_abs_2511_11007/figures/008_Figure_6.jpg]]
*Figure 6: Results of average inference time and performance across four benchmarks. The size is proportional to its y-value*

![[assets/figures/papers/paper_list_l2358_https_arxiv_org_abs_2511_11007/figures/022_Table_12.jpg]]
*Table 12: Average inference time per sample (seconds), average inference speed (samples / seconds), and task performances across four benchmarks on various methods. Perf. indicates Performance*

### 基座模型兼容性

VisMem 在 9 个不同规模和来源的基座模型上均带来一致的性能提升（Table 2），包括 Qwen2.5-VL（3B/7B/32B）、LLaVA-OV-1.5（4B/8B）和 InternVL-3.5（4B/8B/14B/38B）。这验证了方法的模型无关性——记忆模块仅通过扩展词汇表和附加 LoRA 适配器实现，不依赖特定 VLM 架构。

### 失败模式与局限

尽管整体性能领先，VisMem 仍存在以下不足：

- **全量调用的性能退化**：当调用概率设为 100% 时性能反而下降，说明当前动态调用机制无法完全避免无效记忆插入对生成质量的负面影响。如何更精确地判断何时需要记忆增强，是后续优化的关键方向。
- **计算成本**：引入的记忆模块带来 8.2%–43.8% 的额外延迟，在实时性要求极高的场景下可能成为瓶颈。记忆长度增大时成本进一步上升。
- **训练资源需求**：两阶段 GRPO 训练需要 8 块 H200 GPU，对小型研究团队不够友好。
- **任务覆盖**：论文未验证 VisMem 在视频理解或多模态交互任务上的效果，其通用性有待进一步检验。

## 定位与知识库关联

### 1. 范式分类与 VisMem 的定位

当前缓解 VLM “视觉处理瓶颈” 的方法可归纳为四种范式（Figure 1）：

- **直接训练范式 (Direct Training)**：通过监督微调或强化学习直接优化 VLM，不引入额外视觉处理模块。代表方法包括 **SFT**、基于 RL 的 **Visual-RFT** 、**VLM-R1** 、**Vision-R1** 以及 **PAPO**。这类方法实现简单，但缺乏结构化的视觉记忆机制，在细粒度理解和多步推理任务上提升有限。
- **图像级范式 (Image-level)**：在生成过程中引入辅助视觉工具或中间图像表示。典型工作包括 **Sketchpad** （生成草图辅助推理）、**GRIT** （利用图像上下文）、**PixelReasoner** （像素级推理）、**DeepEyes** （多步视觉搜索）和 **OpenThinkImg**。这类方法能保留丰富的视觉信息，但引入的图像生成或检索步骤带来显著的计算开销。
- **Token 级范式 (Token-level)**：在文本序列中显式插入视觉 token。代表方法有 **Scaffold** （结构化视觉提示）、**ICoT** （视觉思维链）、**MINT-CoT** （多模态思维链）、**VPT** （视觉提示调优）。这类方法将视觉信息直接文本化，但 token 序列长度膨胀严重，且离散化可能丢失细粒度视觉细节。
- **潜在空间范式 (Latent Space)**：在 VLM 的连续潜在空间中操作，不改变文本 token 序列的表面形式。**Mirage** 是此范式的代表，在潜在空间中插入视觉 token。**VisMem 属于此范式**，通过可训练的记忆形成器在潜在空间中动态生成视觉记忆标记，兼具感知保真度和计算效率。

VisMem 与上述方法的核心差异在于：它引入了**认知对齐的双重记忆系统**——短期记忆负责细粒度感知证据的保留，长期记忆负责抽象语义知识的巩固——并通过**可学习的调用机制**在需要时按需插入，而非固定模式或全量注入。

### 2. 与关键基线的方法论对比

| 维度 | Mirage （潜在空间基线） | VisMem（本文） |
|------|---------------------------|---------------|
| 记忆类型 | 单一潜在视觉 token | 双重记忆：短期（感知）+ 长期（语义） |
| 记忆触发 | 固定或规则触发 | 可学习的动态调用（GRPO 优化） |
| 记忆形成 | 基于编码器输出 | 上下文感知查询构建器 + LoRA 形成器 |
| 训练策略 | 监督微调 | 两阶段 GRPO 强化学习（先优化记忆形成，再优化调用策略） |

与 Token 级方法（如 **Scaffold** 、**ICoT** ）相比，VisMem 的潜在记忆标记不占据文本 token 空间，避免了序列长度的线性膨胀，同时保留了连续表示的表达能力。与图像级方法（如 **DeepEyes** 、**PixelReasoner** ）相比，VisMem 无需额外的图像生成或检索步骤，推理延迟仅比 vanilla 模型高 8.2%–43.8%，显著优于大多数图像级方法（Table 12, Figure 6）。

### 3. 适用边界与条件

VisMem 的设计使其在以下场景中尤为有效：

- **细粒度视觉理解任务**：MuirBench 上的计数 (+7.0%)、视觉检索 (+9.4%) 和 grounding (+13.1%) 子任务均大幅领先基线，表明短期记忆有效保留了感知证据。
- **多步视觉推理**：MathVista (+12.0%) 和 MV-Math (+22.5%) 上的显著提升，验证了记忆系统在长链推理中持续提供视觉 grounding 的能力。
- **多模型兼容性**：在 Qwen2.5-VL（3B/7B/32B）、LLaVA-OV-1.5（4B/8B）、InternVL-3.5（4B/8B/14B/38B）共 9 个基座模型上均获得一致提升（Table 2），证明方法的模型无关性。
- **连续学习场景**：四阶段连续训练后，VisMem 在 MMVet 上保留 72.1% 的性能，优于 DeepEyes 的 68.4% 和 Mirage 的 67.0%（Figure 4），显示对灾难性遗忘的强抵抗力。

**适用边界**：VisMem 假设 VLM 具备基本的视觉编码和语言生成能力，其增益依赖于基座模型的初始性能。对于极低性能的基座模型，记忆系统可能无法有效补偿基础能力的不足。此外，方法目前仅在静态图像任务上验证，视频或多模态交互场景的适用性待检验。

### 4. 局限性与开放问题

**已知局限**：

1. **推理延迟**：尽管优于图像级方法，VisMem 仍引入 8.2%–43.8% 的额外推理时间（Table 12），在实时性要求极高的场景下可能成为瓶颈。
2. **调用机制的非最优性**：消融实验显示，100% 全量调用反而导致性能下降（如 Mimics 基准从 73.6 降至 73.4），表明当前动态调用策略尚未达到最优，无效调用可能损害生成质量（Table 3）。
3. **训练资源需求**：两阶段 GRPO 训练需要 8 块 H200 GPU，对小型研究团队不够友好。
4. **模态限制**：仅验证了静态图像理解，未拓展至视频、音频等连续多模态输入。

**开放问题**：

- **可解释性**：潜在记忆标记的具体语义内容尚不透明，如何使记忆编码的信息具备可解释性，让用户理解不同任务中记忆调用的具体作用？
- **自适应记忆长度**：记忆长度 $N_s$、$N_l$ 的最优值是否与任务复杂度存在显式定量关系？能否实现基于任务难度的自适应选择？
- **跨模态拓展**：VisMem 框架能否拓展到时序多模态输入，以支持视频理解中的时序记忆与因果推理？
- **效率优化**：除 LoRA 外，是否存在其他参数高效方法（如量化、蒸馏）可进一步降低训练和推理成本，同时保持性能？

**公平性说明**：论文未专门讨论公平性或社会偏见评估，主要聚焦于视觉能力的提升。在实际部署中，基座 VLM 的固有偏见可能通过记忆系统被保留或放大，需人工验证。

## 原文 PDF

![[paperPDFs/CVPR_2026/VisMem_Latent_Vision_Memory_Unlocks_Potential_of_Vision_Language_Models.pdf]]
