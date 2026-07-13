---
title: "TRM-VLA: Temporal-Aware Chain-of-Thought Reasoning and Memorization for Vision-Language-Action Models"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/TRM_VLA_Temporal_Aware_Chain_of_Thought_Reasoning_and_Memorization_for_Vision_Language_Action_Models.pdf
project_link: null
code_link: null
aliases:
- TV
- TRM-VLA
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/image_and_video_generation
core_operator: 仅在关键决策点触发分层链式推理（KTR），并利用动态上下文记忆（GCM）维持时间一致性，从而消除冗余并提升长期规划。
primary_logic: 机器人操作推理应根据任务进展自适应启动，而非固定频率；同时必须保持历史推理记忆以确保行动的时序连贯性。
claims:
- TRM-VLA在SIMPLER上达到72.9%成功率，并将CoT token生成量减少4倍。
- 移除KTR使SIMPLER平均成功率从0.73降至0.65。
- 移除GCM使SIMPLER平均成功率从0.73降至0.54。
- LIBERO-90 上 成功率 = 94.8
---

# TRM-VLA: Temporal-Aware Chain-of-Thought Reasoning and Memorization for Vision-Language-Action Models

> [!tip] 核心洞察
> 机器人操作推理应根据任务进展自适应启动，而非固定频率；同时必须保持历史推理记忆以确保行动的时序连贯性。

| 字段 | 内容 |
|------|------|
| 中文题名 | TRM-VLA：面向视觉-语言-动作模型的时序感知链式推理与记忆框架 |
| 英文题名 | TRM-VLA: Temporal-Aware Chain-of-Thought Reasoning and Memorization for Vision-Language-Action Models |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://openaccess.thecvf.com/content/CVPR2026/html/Li_TRM-VLA_Temporal-Aware_Chain-of-Thought_Reasoning_and_Memorization_for_Vision-Language-Action_Models_CVPR_2026_paper.html) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/image_and_video_generation |
| Method | TRM-VLA |
| Dataset | LIBERO-90, SIMPLER |

> [!tip] 效果简介
> - LIBERO-90 上，成功率 94.8 vs 88.4 (CogACT) (+6.4)。
> - SIMPLER 上，平均成功率 0.73 vs 0.65 (无KTR) (+0.08)；平均成功率 0.73 vs 0.54 (无GCM) (+0.19)。
> - 真实世界任务 上，平均成功率 0.69 vs 0.50 (CogACT-ECoT) (+0.19)。

## 概要

现有视觉-语言-动作（VLA）模型在机器人操作中引入链式推理（CoT）以增强决策能力，但普遍采用**逐帧生成完整CoT**的策略。这一范式暴露了两个关键瓶颈：其一，每个时间步独立生成推理导致**大量冗余计算**，推理token开销与任务时长线性增长；其二，帧间推理**缺乏时序一致性**，历史决策信息无法有效传递，制约长期任务执行。

针对上述问题，本文提出**TRM-VLA**（Temporal-Aware Chain-of-Thought Reasoning and Memorization for Vision-Language-Action Models），核心调控机制包含两个联动组件：

- **键帧触发推理（KTR）**：仅在关键决策点（如抓取、放置等状态切换时刻）触发分层CoT推理，其余时间步不生成推理，从根本上消除冗余。
- **粒度自适应上下文记忆（GCM）**：维护动态多粒度记忆缓冲区，通过交叉注意力选择性检索历史推理特征，确保跨帧推理的时序连贯性。

该方法的核心洞见在于：机器人操作推理应**自适应于任务进展**而非固定频率触发，同时必须**保持历史推理记忆**以保障行动序列的因果一致性。

**主要结果**：TRM-VLA在SIMPLER基准上达到**72.9%**成功率，在LIBERO-90上达到**94.8%**成功率，均取得最优性能；同时将CoT token生成量**降低4倍**（真实世界任务中从每步26.8 tokens降至4.3 tokens）。消融实验表明，移除KTR使SIMPLER平均成功率从0.73降至0.65，移除GCM进一步降至0.54，验证了时序推理与记忆机制各自的关键贡献。



### 机器人操作中的视觉-语言-动作模型

视觉-语言-动作模型（Vision-Language-Action Model, VLA）将视觉感知、语言理解与动作生成统一于单一框架，已成为机器人操作任务的核心范式。标准VLA模型直接根据当前观测 $o_t$ 和语言指令 $l_t$ 预测动作 $a_t$：

$$a _ { t } \sim P _ { \theta } ( a _ { t } \mid o _ { t } , l _ { t } )$$

这一公式简洁地刻画了从感知到动作的端到端映射，但其隐式推理过程缺乏可解释性，且在需要多步规划的复杂任务中表现受限。

### 推理增强VLA的兴起与瓶颈

为提升模型的规划能力，近期工作引入链式推理（Chain-of-Thought, CoT），使模型在生成动作前先产生显式的中间推理轨迹 $r_t$：

$$a _ { t } \sim P _ { \theta } ( a _ { t } \mid r _ { t } , o _ { t } , l _ { t } ) , \quad r _ { t } \sim P _ { \theta } ( r _ { t } \mid o _ { t } , l _ { t } )$$

代表性工作如 **ECoT**（Zawalski et al., CoRL 2025）在每个时间步生成完整的独立CoT，显著提升了动作预测的合理性。然而，这一设计暴露出两个根本性缺陷：

1. **推理冗余**：机器人操作任务的多数时间步处于平滑执行阶段（如物体移动、机械臂过渡），并不需要高层次的规划推理。在每个时间步生成完整CoT导致大量冗余计算，不仅浪费推理资源，还拖慢了实时响应速度。
2. **时序断裂**：现有方法的帧间推理相互独立，缺乏跨帧记忆机制。当任务需要多步协调（如“拿起杯子→走到水壶旁→接水”）时，模型无法利用历史推理信息维持行动的时序连贯性，导致长期任务执行失败。

### 本文动机与核心思路

针对上述瓶颈，本文提出 **TRM-VLA**（Temporal-Aware Chain-of-Thought Reasoning and Memorization for Vision-Language-Action Models），核心洞察是：**机器人操作推理应根据任务进展自适应启动，而非固定频率；同时必须保持历史推理记忆以确保行动的时序连贯性。**

具体而言，TRM-VLA 引入两个相互协同的创新模块：

- **键帧触发推理（Keyframe-Triggered Reasoning, KTR）**：仅在关键决策点（如抓取物体、切换子任务）触发分层链式推理，其他时间步不生成推理，从根本上消除冗余。
- **粒度自适应上下文记忆（Granularity-adaptable Context Memory, GCM）**：维护动态多粒度记忆缓冲区，通过交叉注意力检索历史推理特征，为当前决策提供时序上下文。

如 Figure 1 所示，与每帧生成完整CoT或固定间隔生成CoT的现有模式相比，TRM-VLA 仅在关键帧触发层次化推理，并维持动态记忆缓冲区，在减少冗余推理token的同时提升成功率。实验表明，TRM-VLA 在 SIMPLER 基准上达到 72.9% 的成功率，同时将 CoT token 生成量减少 4 倍，验证了时序感知推理与记忆机制的有效性。



## 核心方法与创新机理

TRM-VLA 的核心创新在于将机器人操作中的链式推理（CoT）从“逐帧全量生成”转变为“关键帧触发、时序记忆增强”的模式，解决了现有VLA模型的两大瓶颈：**推理冗余**与**时序不一致**。具体而言，TRM-VLA 通过两个紧密协作的模块——**键帧触发推理（KTR）** 与 **粒度自适应上下文记忆（GCM）**——实现了这一转变。

### 推理触发策略：从逐帧全量到关键帧分层触发

现有推理增强型VLA模型（如 **ECoT**，Zawalski et al., CoRL 2025）在每个时间步均生成完整的链式推理轨迹，导致大量冗余计算，且推理内容缺乏对任务进展的感知。TRM-VLA 的 KTR 模块改变了这一范式：它将任务执行过程划分为三个时序阶段（早期高层规划、中期感知锚定子任务分解、后期低层移动执行），并仅在推理标签发生变化的“关键帧”触发分层 CoT 生成。其核心机制通过关键帧指示器实现：

$$b _ { t } ^ { \tau } = \left\{ { \begin{array} { l l } { 1 , } & { { \mathrm { i f ~ } } r _ { t } ^ { \tau } \neq r _ { t - 1 } ^ { \tau } , } \\ { 0 , } & { { \mathrm { o t h e r w i s e } } , } \end{array} } \right. \tau \in \{ { \mathrm { p e r } } , { \mathrm { s } } , \mathrm { m } \}$$

该指示器以二进制标志标记感知（per）、子任务（s）、移动（m）三类推理标签是否发生变化。当标签不变时，模型跳过推理生成，直接复用前一时刻的推理状态。这一策略将每步平均 CoT token 生成量从 ECoT 的 26.8 降至 4.3（Table 3），降幅达约 6 倍，同时将 SIMPLER 平均成功率从 0.65 提升至 0.73（Table 4，移除 KTR 的消融实验）。

### 时序记忆机制：从帧间独立到动态上下文检索

传统 VLA 模型的帧间推理相互独立，缺乏对历史决策的记忆，导致长周期任务中行动连贯性不足。TRM-VLA 的 GCM 模块维护一个字典式动态记忆缓冲区，存储过去关键帧的分层推理标记：

$$C _ { k _ { c } } = C _ { k _ { c - 1 } } \cup \{ r _ { k _ { c } } ^ { \mathrm { t a g } } \}$$

在后续推理中，GCM 通过可学习的思维查询（thought queries）对记忆缓冲区执行交叉注意力检索，提取与当前任务相关的历史推理特征，再通过 FiLM 网络与当前认知特征融合：

$$f _ { t } = \mathrm { F i L M } ( f _ { c } , f _ { \mathrm { a t t } } )$$

这一设计使模型在做出当前决策时能够显式地参考历史推理上下文，从而增强时序一致性。消融实验表明，移除 GCM 使 SIMPLER 平均成功率从 0.73 骤降至 0.54（Table 4），降幅达 19 个百分点，验证了时序记忆对长周期任务执行的关键作用。

### 创新协同：冗余消除与一致性增强的统一

KTR 与 GCM 并非孤立运作，而是形成协同效应：KTR 通过选择性触发减少了需要存储和检索的推理量，使 GCM 的记忆缓冲区更加精简高效；GCM 则为 KTR 的触发决策提供了历史上下文，使关键帧判断更具时序连贯性。两者共同将 TRM-VLA 在真实世界任务上的平均成功率从基线的 0.50 提升至 0.69（Table 5），并在 LIBERO-90 上达到 94.8% 的 SOTA 成功率（Table 2）。



TRM-VLA 的整体设计围绕一个核心矛盾展开：现有推理增强型 VLA 模型（如 **ECoT** (Zawalski et al., CoRL 2025)）在每个时间步生成完整链式推理，虽提升了决策质量，却引入了大量冗余计算，且帧间推理相互独立，缺乏时序一致性。TRM-VLA 的解决思路是**仅在关键决策点触发分层推理，并通过动态记忆维持跨帧推理的连贯性**。

### 系统架构

TRM-VLA 构建于强基线模型 **CogACT** (Li et al., arXiv 2024) 之上，沿用了其“认知—行动”双流架构，但引入了两个核心创新模块。整体 pipeline 由以下组件串联构成：

1. **视觉编码器**：由 DINOv2 和 SigLIP 两个互补的视觉 Transformer 组成。DINOv2 负责捕获空间局部特征，SigLIP 编码语义级表示，二者共同为下游推理提供多粒度的视觉信息。

2. **语言编码器**：采用 LLaMA-2 处理语言指令，并与视觉 token 融合，形成多模态感知表征。

3. **键帧触发推理模块（KTR）**：这是框架的核心决策引擎。KTR 不再在每个时间步生成完整 CoT，而是根据任务进展将整个 episode 划分为早期规划、中期子任务分解、后期精细执行三个阶段，仅在推理标签发生变化的“关键帧”触发分层推理。非关键帧则跳过推理，直接复用上一帧的认知状态。

4. **粒度自适应上下文记忆（GCM）**：维护一个字典式动态记忆缓冲区，存储历史关键帧的层次化推理特征。当前帧通过可学习的思维查询（thought queries）与记忆缓冲区进行交叉注意力检索，提取与当前任务阶段相关的历史推理信息，解决帧间推理不一致的问题。

5. **FiLM 融合网络**：将当前帧的认知特征与 GCM 检索到的历史推理特征，通过特征线性调制进行融合，形成时序增强的认知表征。

6. **扩散动作专家**：以融合后的认知特征为条件，通过 Diffusion Transformer 迭代去噪，生成未来多步的动作序列。

### 数据流与推理模式

TRM-VLA 的推理模式与标准 VLA 和现有推理增强 VLA 有本质区别。标准 VLA 直接从观测与指令预测动作：

$$a _ { t } \sim P _ { \theta } ( a _ { t } \mid o _ { t } , l _ { t } )$$

推理增强 VLA 引入中间推理轨迹 $r_t$，但每帧独立生成：

$$a _ { t } \sim P _ { \theta } ( a _ { t } \mid r _ { t } , o _ { t } , l _ { t } ) , \quad r _ { t } \sim P _ { \theta } ( r _ { t } \mid o _ { t } , l _ { t } )$$

TRM-VLA 则将推理替换为记忆增强的时序推理状态 $m_t$：

$$a _ { t } \sim P _ { \theta } ( a _ { t } \mid m _ { t } , o _ { t } , l _ { t } )$$

其中 $m_t$ 是对历史推理轨迹的动态聚合：

$$m _ { t } \sim P _ { \phi } ( m _ { t } \mid r _ { 1 } ^ { h } , \ldots , r _ { t } ^ { h } )$$

这一形式化转变的实质效果体现在推理效率上：TRM-VLA 在真实世界任务中平均每步仅生成 **4.3 个 CoT token**，而 ECoT 基线为 **26.8 个**，推理 token 生成量减少约 6 倍。

Figure 2 展示了完整的系统架构，其中 (a) 为 VLM 推理骨干与扩散执行专家的双流设计，(b) 为 KTR 的键帧触发分层推理机制，(c) 为 GCM 的动态记忆检索与融合流程。

![[assets/figures/papers/paper_list_l2426_https_openaccess_thecvf_com_content_CVPR2026_html_Li_TRM_VLA_Temporal_Aw/figures/003_Figure_2.jpg]]
*Figure 2: Overview of the proposed TRM-VLA (Sec. 3.2). (a) System design: VLM backbone for reasoning and diffusion expert for execution. (b) Keyframe-Triggered Reasoning (Sec. 3.3) performs hierarchical reasoning only at critical frames supervised by temporal reasoning data. (c) Granularity-adaptable Context Memory (Sec. 3.4) maintains a dynamic memory buffer to enhance inter-frame reasoning coherence*

### 补充图表

![[assets/figures/papers/paper_list_l2426_https_openaccess_thecvf_com_content_CVPR2026_html_Li_TRM_VLA_Temporal_Aw/figures/002_Figure_1.jpg]]
*Figure 1: Different reasoning patterns of VLAs. (a) generate full CoT at every frame. (b) generate CoT at fxed intervals without memory. (c) generate hierarchy CoT at critical frames, and maintain a dynamic memory buffer for execution, thus reducing redundant CoT reasonings tokens while improving the success rates*



### 3.1 问题形式化与推理增强VLA

TRM-VLA将机器人操作建模为时序条件动作生成问题。标准VLA模型直接从观测与指令预测动作：

$$a _ { t } \sim P _ { \theta } ( a _ { t } \mid o _ { t } , l _ { t } )$$

推理增强VLA在此基础上引入中间推理轨迹 $r_t$，先由模型生成推理，再基于推理预测动作：

$$a _ { t } \sim P _ { \theta } ( a _ { t } \mid r _ { t } , o _ { t } , l _ { t } ) , \quad r _ { t } \sim P _ { \theta } ( r _ { t } \mid o _ { t } , l _ { t } )$$

TRM-VLA进一步引入时序记忆机制，将动作预测条件扩展为记忆增强的推理状态 $m_t$：

$$a _ { t } \sim P _ { \theta } ( a _ { t } \mid m _ { t } , o _ { t } , l _ { t } )$$

其中记忆状态 $m_t$ 由历史推理轨迹动态聚合而成：

$$m _ { t } \sim P _ { \phi } ( m _ { t } \mid r _ { 1 } ^ { h } , \ldots , r _ { t } ^ { h } )$$

### 3.2 系统架构概览

TRM-VLA构建于**CogACT**（Li et al., arXiv 2024）之上，由VLM推理骨干与扩散动作专家两部分组成（Figure 2）。核心创新在于两个即插即用的模块：**键帧触发推理（KTR）** 和**粒度自适应上下文记忆（GCM）**。

**流水线模块：**
- **视觉编码器**：由DINOv2与SigLIP双支路构成，分别捕获空间局部特征与语义级表征。
- **语言编码器**：采用LLaMA-2处理语言指令，与视觉token融合。
- **KTR模块**：仅在关键决策点生成分层链式推理，消除逐帧冗余计算。
- **GCM模块**：维护动态多粒度记忆缓冲区，通过交叉注意力检索历史推理特征。
- **FiLM融合网络**：将当前认知特征与检索到的历史推理特征进行特征线性调制融合。
- **扩散动作专家（DiT）**：以融合特征为条件，通过迭代去噪生成动作序列。

### 3.3 键帧触发推理（KTR）

KTR的核心思想是将任务执行过程划分为三个时序阶段，并在各阶段仅于推理标签变化的关键帧触发分层CoT生成。

**阶段划分：**
- **早期阶段**（$t < t_e$）：生成高层规划推理，包含任务（$r_t^{\mathrm{t}}$）、计划（$r_t^{\mathrm{p}}$）、感知（$r_t^{\mathrm{per}}$）、子任务推理（$r_t^{\mathrm{sr}}$）和移动推理（$r_t^{\mathrm{mr}}$）。
- **中期阶段**（$t_e < t < t_m$）：当感知标签变化时，生成感知、子任务推理和移动推理。
- **后期阶段**（$t_m < t < t_l$）：当子任务标签变化时，生成子任务（$r_t^{\mathrm{s}}$）、移动（$r_t^{\mathrm{m}}$）和目标推理（$r_t^{\mathrm{g}}$）；当移动标签变化时，仅生成移动和目标推理。

**关键帧指示器**通过比较相邻帧的推理标签变化来定义：

$$b _ { t } ^ { \tau } = \left\{ \begin{array} { l l } { 1 , } & { \mathrm { i f ~ } r _ { t } ^ { \tau } \neq r _ { t - 1 } ^ { \tau } , } \\ { 0 , } & { \mathrm { o t h e r w i s e } , } \end{array} \right. \quad \tau \in \{ \mathrm { p e r } , \mathrm { s } , \mathrm { m } \}$$

**时序层次推理集合** $\mathcal{T}_t$ 根据当前时间阶段和关键帧类型，动态决定应生成的推理标签集合：

$$\mathcal { T } _ { t } = \left\{ \begin{array} { l l } { \{ r _ { t } ^ { \mathrm { t } } , ~ r _ { t } ^ { \mathrm { p } } , ~ r _ { t } ^ { \mathrm { p e r } } , ~ r _ { t } ^ { \mathrm { s r } } , ~ r _ { t } ^ { \mathrm { m r } } \} , } & { t < t _ { \mathrm { e } } , } \\ { \{ r _ { t } ^ { \mathrm { p e r } } , ~ r _ { t } ^ { \mathrm { s r } } , ~ r _ { t } ^ { \mathrm { m r } } \} , } & { t _ { \mathrm { e } } < t < t _ { \mathrm { m } } \mathrm { ~ a n d ~ } b _ { t } ^ { \mathrm { p e r } } = 1 , } \\ { \{ r _ { t } ^ { \mathrm { s } } , ~ r _ { t } ^ { \mathrm { m } } , ~ r _ { t } ^ { \mathrm { g } } \} , } & { t _ { \mathrm { m } } < t < t _ { \mathrm { l } } \mathrm { ~ a n d ~ } b _ { t } ^ { \mathrm { s } } = 1 , } \\ { \{ r _ { t } ^ { \mathrm { m } } , ~ r _ { t } ^ { \mathrm { g } } \} , } & { t _ { \mathrm { m } } < t < t _ { \mathrm { l } } \mathrm { ~ a n d ~ } b _ { t } ^ { \mathrm { m } } = 1 . } \end{array} \right.$$

**KTR训练目标**为基于下一token预测的负对数似然损失：

$$\mathcal { L } _ { \mathrm { K T R } } = - \sum _ { S \in \mathcal { D } } \sum _ { t } ^ { T } \log p ( \mathcal { T } _ { t } \mid o _ { t } , l _ { t } ; \theta )$$

### 3.4 粒度自适应上下文记忆（GCM）

GCM通过字典式记忆缓冲区维护跨帧推理的时序一致性。每当关键帧 $k_c$ 触发推理时，将生成的推理token按标签插入记忆：

$$C _ { k _ { c } } = C _ { k _ { c - 1 } } \cup \{ r _ { k _ { c } } ^ { \mathrm { t a g } } \}$$

相同标签的旧条目被覆盖，确保记忆的紧凑性。在推理时，使用可学习的思维查询 $q$ 通过交叉注意力从记忆特征 $f_{\mathrm{rc}}$ 中检索相关信息：

$$f _ { \mathrm { a t t } } = \mathrm { C r o s s A t t n } ( q , K = f _ { \mathrm { r c } } , V = f _ { \mathrm { r c } } )$$

检索到的历史推理特征 $f_{\mathrm{att}}$ 与当前认知特征 $f_c$ 通过FiLM网络融合：

$$f _ { t } = \mathrm { F i L M } ( f _ { c } , f _ { \mathrm { a t t } } )$$

### 3.5 动作生成与训练目标

融合后的认知特征 $f_t$ 作为条件输入扩散动作专家（DiT），通过迭代去噪生成动作块。扩散策略的训练目标为标准均方误差损失：

$$\mathcal { L } _ { \mathrm { M S E } } = \mathbb { E } _ { \epsilon \sim \mathcal { N } ( 0 , 1 ) , i } \left\| \hat { \epsilon } ^ { i } - \epsilon \right\| _ { 2 }$$

整体训练联合优化KTR的推理损失与扩散动作的MSE损失，使模型同时学习何时推理、推理什么以及如何基于推理执行动作。



## 实验与关键发现

### 评估设置概览

TRM-VLA 在三个递进的评估层次上接受检验：模拟基准 SIMPLER-Bridge（WidowX 机械臂）、LIBERO-90（Franka 机械臂），以及基于 AIRBOT Player 的真实世界操作任务。评估维度覆盖操作精度、工具使用、时序记忆和长时程规划能力（Figure 3）。

![[assets/figures/papers/paper_list_l2426_https_openaccess_thecvf_com_content_CVPR2026_html_Li_TRM_VLA_Temporal_Aw/figures/005_Figure_3.jpg]]
*Figure 3: Cross-task, cross-embodiment evaluation environments: Simpler-Env [23] with WidowX robot, LIBERO-90 [28] with Franka robot, and real-world tasks based on AIRBOT Player robot, focusing on manipulation accuracy, tool-using, temporal memory, and long-horizon*

### 主实验结果

**SIMPLER-Bridge 基准。** TRM-VLA 在 SIMPLER-Bridge 上取得了 72.9% 的平均成功率，达到当前最优水平（Table 1）。相比强基线 CogACT（88.4% 需核实具体对应任务子集），TRM-VLA 在所有任务类别上均表现出一致的性能优势。

**LIBERO-90 基准。** 在 LIBERO-90 上，TRM-VLA 达到 94.8% 的成功率，较基线 CogACT 的 88.4% 提升 **+6.4 个百分点**（Table 2）。该结果验证了时序感知推理与记忆机制在需要长期任务规划的复杂操作场景中的有效性。

**真实世界任务。** 在真实世界评估中，TRM-VLA 以 0.69 的平均成功率显著优于 CogACT-ECoT 的 0.50，提升 **+0.19**（Table 3）。更重要的是，TRM-VLA 每步平均仅生成 **4.3 个 CoT token**，而 ECoT 基线每步需生成 26.8 个 token——推理成本降低约 **6 倍**，同时成功率大幅提升。这一结果直接验证了核心主张：仅在关键帧触发推理不仅能削减冗余计算，还能通过时序一致性增强任务完成质量。

### 消融实验

为分离 KTR 与 GCM 各自的贡献，论文在 SIMPLER 和真实世界两个层次上进行了消融（Table 4、Table 5）：

![[assets/figures/papers/paper_list_l2426_https_openaccess_thecvf_com_content_CVPR2026_html_Li_TRM_VLA_Temporal_Aw/figures/010_Table_4.jpg]]
*Table 4: Ablation study of KTR and GCM on SIMPLER*

![[assets/figures/papers/paper_list_l2426_https_openaccess_thecvf_com_content_CVPR2026_html_Li_TRM_VLA_Temporal_Aw/figures/011_Table_5.jpg]]
*Table 5: Ablation study of KTR and GCM on real-world evaluation*

| 消融设置 | SIMPLER 平均 SR | 真实世界平均 SR |
|----------|----------------|----------------|
| TRM-VLA（完整） | 0.73 | 0.69 |
| 移除 KTR | 0.65（−0.08） | — |
| 移除 GCM | 0.54（−0.19） | — |
| CogACT-ECoT 基线 | — | 0.50 |

**KTR 的独立贡献。** 移除 KTR 后，SIMPLER 平均成功率从 0.73 降至 0.65，降幅为 0.08。这表明关键帧触发推理策略在减少冗余计算的同时，并未牺牲推理质量——相反，自适应触发机制通过聚焦关键决策点，避免了全帧推理引入的噪声和不一致性。

**GCM 的独立贡献。** 移除 GCM 导致 SIMPLER 平均成功率从 0.73 骤降至 0.54，降幅高达 **0.19**，是 KTR 降幅的两倍以上。这一结果揭示了一个重要发现：**时序记忆一致性对长期任务执行的贡献可能比推理触发策略本身更为关键**。没有跨帧记忆检索，模型在长时程任务中会失去对已完成子目标和历史推理上下文的追踪，导致动作序列出现语义断裂。

**真实世界联合增益。** 在真实世界任务上，同时引入 KTR 和 GCM 将平均成功率从 0.50 提升至 0.69（+0.19），进一步验证了两个模块在真实噪声和动态环境下的协同增效。

### 关键图表结论

- **Figure 4** 展示了真实世界定性结果：TRM-VLA 在抓取、放置、工具操作等关键帧处自适应触发推理，而在常规运动阶段保持静默，实现了推理效率与任务精度的平衡。
- **Table 3** 中的 “Progress” 指标表明，TRM-VLA 在任务完成进度上同样优于基线，说明时序记忆不仅影响成功率，还影响任务执行的完整度。
- **Figure 5** 的泛化评估定性结果显示，TRM-VLA 在未见过的物体和场景配置下仍能保持合理的推理触发策略和动作执行能力。

![[assets/figures/papers/paper_list_l2426_https_openaccess_thecvf_com_content_CVPR2026_html_Li_TRM_VLA_Temporal_Aw/figures/008_Table_3.jpg]]
*Table 3: Quantitative comparison with SOTA methods on real-world tasks. ‘SR’ indicates the success rates. ’Tokens’ denotes the average number of generated CoT tokens per step, and ’Progress’ is the average completion progress of the task*

![[assets/figures/papers/paper_list_l2426_https_openaccess_thecvf_com_content_CVPR2026_html_Li_TRM_VLA_Temporal_Aw/figures/007_Figure_4.jpg]]
*Figure 4: Qualitative Results on real-world evaluation. The TRM-VLA model adaptively triggers reasoning at critical frames*

![[assets/figures/papers/paper_list_l2426_https_openaccess_thecvf_com_content_CVPR2026_html_Li_TRM_VLA_Temporal_Aw/figures/009_Figure_5.jpg]]
*Figure 5: Qualitative Results on generalization evaluation*

### 失败模式与局限

论文未单独列出系统性的失败模式分析表格，但从消融实验中可推断以下关键失效路径：

1. **无 GCM 时的时序断裂**：移除 GCM 后成功率从 0.73 降至 0.54，表明模型在缺乏历史推理记忆时，无法维持跨帧的动作连贯性，尤其在需要记住“已抓取物体”或“已完成子任务”的长时程场景中容易发生重复操作或遗漏步骤。
2. **全帧推理的冗余干扰**：ECoT 基线每步生成 26.8 个 CoT token 却仅获得 0.50 的真实世界成功率，说明固定频率的全帧推理不仅浪费计算，还可能因推理内容的前后不一致而引入冲突信号，反而损害策略质量。
3. **关键帧标注依赖**：KTR 的训练需要时间关键帧标注数据，在标注稀疏或质量不足的场景下，触发策略的准确性可能下降——这是当前框架的一个已知限制，需人工验证具体退化幅度。
4. **记忆缓冲区容量限制**：GCM 采用字典式记忆缓冲区存储历史推理标记，在超长时程任务中可能出现缓冲区溢出或检索退化，该场景下的性能表现论文未提供数据，需进一步验证。

### 补充图表

![[assets/figures/papers/paper_list_l2426_https_openaccess_thecvf_com_content_CVPR2026_html_Li_TRM_VLA_Temporal_Aw/figures/006_Table_2.jpg]]
*Table 2: Comparison with SOTA methods on LIBERO-90*



## 定位与知识库关联

### 一、与基线方法的演进关系

TRM-VLA 直接构建在 **CogACT**（Li et al., arXiv 2024）之上，后者是一种将多模态基础模型与扩散动作策略相结合的强基线系统。CogACT 本身已具备认知-行动协同能力，但其推理模式遵循标准推理增强 VLA 范式，即在每个时间步独立生成完整的链式推理（CoT），再将推理结果馈入动作专家。TRM-VLA 保留了 CogACT 的视觉编码器（DINOv2 + SigLIP）、语言编码器（LLaMA-2）和扩散动作专家（DiT）这一主干架构，但在推理机制上进行了根本性改造。

与 **ECoT**（Zawalski et al., CoRL 2025）这类典型的推理增强 VLA 相比，TRM-VLA 的核心突破在于打破了“每帧必推”的固定范式。ECoT 在每个时间步生成完整 CoT，导致大量冗余计算——在真实世界任务中，ECoT 平均每步生成 26.8 个 CoT token，而 TRM-VLA 仅需 4.3 个（Table 3），推理 token 生成量减少约 6 倍。这一效率提升并非来自模型压缩，而是源于推理触发策略的根本转变：仅在关键决策点激活分层 CoT，其余时间步直接依赖历史推理记忆进行动作预测。

与 **OpenVLA**（Kim et al., CoRL 2024）等不显式引入推理轨迹的 VLA 相比，TRM-VLA 属于推理增强路线，但其独特之处在于将时序感知引入了推理过程。OpenVLA 等模型从观测和指令直接预测动作，缺乏中间推理状态，难以处理需要长期时序依赖的操作任务。

### 二、方法适用边界

**适用场景**：TRM-VLA 的设计假设任务具有可分段的时间结构，即存在明确的关键决策点（如抓取、放置、工具切换）。在 SIMPLER-Bridge（72.9%）和 LIBERO-90（94.8%）上的表现表明，该方法在物体操作、工具使用和长时序任务中具有显著优势。真实世界评估（Table 5）进一步验证了其在操作精度、时序记忆和长程规划方面的有效性。

**不适用或需谨慎使用的场景**：
- **缺乏清晰关键帧的任务**：KTR 依赖时间关键帧标注数据来监督推理触发。对于连续、平滑的操作任务（如动态抓取、力控装配），关键决策点的定义可能模糊，KTR 的分层推理优势难以发挥。
- **超长时序任务**：GCM 采用字典式记忆缓冲区存储历史推理特征，其容量有限。论文明确指出记忆缓冲区容量可能限制超长时序任务的表现，但未给出具体的容量上限或退化曲线。
- **实时性要求极高的场景**：GCM 的交叉注意力检索和 FiLM 融合引入额外计算开销。论文未报告推理延迟数据，其在动态场景下的实时性表现需要手动验证。

### 三、局限与开放问题

**已确认的局限**：
1. **数据标注依赖**：KTR 需要额外的时间关键帧标注数据来监督分层推理的触发时机和推理内容生成。这一标注成本限制了方法向新任务域的快速迁移。
2. **记忆容量瓶颈**：GCM 的记忆缓冲区容量固定，可能限制超长时序任务中的历史推理信息保留。论文未探索记忆压缩或遗忘机制。

**待探索的开放问题**：
1. **自动关键帧学习**：当前 KTR 依赖人工标注的关键帧触发策略。如何通过强化学习或自监督信号自动学习推理触发时机，以减少标注成本，是该方法走向大规模应用的关键问题。
2. **动态场景下的检索实时性**：GCM 的交叉注意力检索机制在动态、非结构化场景下的计算延迟和检索质量尚未得到充分评估。这对于部署在真实机器人系统上至关重要。
3. **多机器人协作扩展**：当前框架针对单机器人操作任务设计。GCM 的记忆机制能否有效扩展到多机器人协作场景，处理多智能体间的共享推理记忆和时序协调，仍是一个开放问题。
4. **泛化到更复杂操作**：尽管在 SIMPLER 和 LIBERO-90 上表现优异，但论文未在需要精细力控、接触推理或长程因果推理的任务上进行评估。该框架在这些场景下的有效性需要进一步验证。



## 原文 PDF

![[paperPDFs/CVPR_2026/TRM_VLA_Temporal_Aware_Chain_of_Thought_Reasoning_and_Memorization_for_Vision_Language_Action_Models.pdf]]
