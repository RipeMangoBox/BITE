---
title: "ViBES: A Conversational Agent with Behaviorally-Intelligent 3D Virtual Body"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/ViBES_A_Conversational_Agent_with_Behaviorally_Intelligent_3D_Virtual_Body.pdf
project_link: null
code_link: "https://github.com/bosonai/higgs-audio"
aliases:
- VSLBMMME
- ViBES
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 将语音、语言和行为统一在一个模型中，利用混合模态专家（MoME）和不对称跨模态注意力（SLB-Attn）实现联合规划与生成，并在大规模时间同步的三模态数据集上训练，使模型具备对话条件化的身体动作生成能力。
primary_logic: 将非言语行为重新定义为对话智能的核心组成部分，采用参数分割的Transformer专家架构：冻结预训练语音-语言骨干，附加轻量级的侧挂运动专家（面部/身体），通过跨注意力从骨干读取信息，从而在保留语言和韵律智能的同时，赋予3D虚拟身体可控的、社交恰适的对话交互能力。
claims:
- 在对话行为基准（Converse3D测试集）上，ViBES的平衡R-Precision达到0.467，显著超过最佳先验方法LoM（0.323），同时FID降至93.9，远优于MotionGPT的262.2，证明联合建模大幅提升对话-动作对齐。
- 在语音指标评估中，ViBES的上下文相关性得分4.584、角色一致性得分4.376，接近真实值上限（4.838 / 4.893），表明模型保留了预训练语音LLM的语言与韵律智能。
- 消融实验证实，启用面部与身体之间的注意力不会带来可测量的改进，说明在条件化于语音-语言流之后，面部与身体流在很大程度上独立，从而验证了不对称注意力设计的合理性。
- Conversational Behavior (Converse3D test set) 上 R1-Balanced ↑ = 0.467
---

# ViBES: A Conversational Agent with Behaviorally-Intelligent 3D Virtual Body

> [!tip] 核心洞察
> 将非言语行为重新定义为对话智能的核心组成部分，采用参数分割的Transformer专家架构：冻结预训练语音-语言骨干，附加轻量级的侧挂运动专家（面部/身体），通过跨注意力从骨干读取信息，从而在保留语言和韵律智能的同时，赋予3D虚拟身体可控的、社交恰适的对话交互能力。

| 字段 | 内容 |
|------|------|
| 中文题名 | ViBES：行为智能3D虚拟身体的对话代理 |
| 英文题名 | ViBES: A Conversational Agent with Behaviorally-Intelligent 3D Virtual Body |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2512.14234) · [Code](https://github.com/bosonai/higgs-audio) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | ViBES (Speech–Language–Behavior model with Mixture-of-Modality-Experts) |
| Dataset | Conversational Behavior |

> [!tip] 效果简介
> - Conversational Behavior (Converse3D test set) 上，R1-Balanced ↑ 0.467 vs 0.323 (LoM) (+0.144)；FID ↓ 93.9 vs 262.2 (MotionGPT) (-168.3)；Diversity → 10.73 vs 7.40 (MotionGPT) (+3.33)。

## 概要

现有对话系统将人体行为视为孤立的模态翻译任务——语音转手势、文本转表情——缺乏对“何时动、做什么、如何在多轮对话中适应”的统一智能决策，导致时机生硬、社交基础薄弱，且语音、语言与动作堆栈相互割裂。**ViBES** 的核心主张是将非言语行为重新定义为对话智能的一等公民：通过参数分割的混合模态专家（Mixture-of-Modality-Experts, MoME）架构，将语音-语言理解与面部/身体运动生成统一在单个自回归模型中，使 3D 虚拟身体具备对话条件化的、社交恰适的交互能力。

**方法定位**：ViBES 冻结预训练的语音-语言骨干（GLM-4-9B），附加轻量级侧挂运动专家（面部/身体），通过不对称跨模态注意力（SLB-Attn）使运动专家仅交叉注意力到语音-语言流，从而在保留语言与韵律智能的同时，赋予模型可控的身体行为生成能力。模型在约 1000 小时的时间对齐三模态数据集 Converse3D 上训练，并引入分数旋转位置编码（Fractional RoPE）实现精确的跨模态时序同步。

**核心结果**：在对话行为基准 Converse3D 测试集上，ViBES 的平衡 R-Precision 达到 **0.467**，显著超过最佳先验方法 LoM 的 0.323；FID 降至 **93.9**，远优于 MotionGPT 的 262.2（Table 2）。语音指标评估中，上下文相关性得分 **4.584**、角色一致性得分 **4.376**，接近真实值上限（4.838 / 4.893），表明模型完整保留了预训练语音 LLM 的语言与韵律智能（Table 3）。消融实验证实，面部与身体专家之间的注意力不带来可测量的性能提升，验证了不对称注意力设计的合理性。



### 问题背景：从对话代理到具身行为智能

赋予AI代理一个可信的3D虚拟身体，使其在对话中展现自然、恰适的非言语行为（面部表情、手势、身体姿态），是构建沉浸式人机交互系统的核心挑战之一。当前的对话系统在语音和语言层面已取得显著进展，但在行为层面仍存在根本性断裂：系统能“说”也能“听”，却难以决定**何时移动、做什么动作、以及如何在多轮对话中动态调整行为**。

这种断裂的根源在于，现有方案普遍将人体行为视为一个简单的**模态翻译任务**——例如，将语音信号直接映射为手势序列，或将文本映射为身体姿态。这类“语音转手势”或“文本转运动”的范式忽略了对话行为的本质：非言语行为是**社交智能的组成部分**，需要理解对话上下文、语用意图和社交规范，而非仅仅是声学或语言特征的函数。

### 现有方法的三大缺口

**缺口一：决策智能缺失，行为生成沦为条件映射。** 现有协同语音手势生成方法（如**SynTalker**、**EMAGE**、**LoM**）和文本到运动生成方法（如**T2M**、**MotionGPT**、**MoMask**）将行为生成建模为从单一模态到运动参数的确定性或概率性映射。这些方法缺乏对“何时该动、何时该静”的决策能力，导致生成的动作**时机生硬、社交基础薄弱**。例如，在倾听对方说话时保持静止与在表达强调时做出手势，需要截然不同的行为策略，但现有模型无法在统一的推理框架下处理这种差异。

**缺口二：模态堆栈碎片化，语音、语言与动作相互孤立。** 典型的对话管线由三个独立模型拼接而成：语音识别/合成模型处理音频，大语言模型处理文本，运动生成模型处理身体动画。这种级联架构不仅引入累积误差，更根本性地剥夺了行为模型访问语言理解和语音韵律信息的能力。当身体动作无法“听到”语调变化、无法“理解”话语语义时，生成的点头、手势和表情必然流于表面同步，而非深层语义对齐。

**缺口三：缺乏大规模时间同步的三模态训练数据。** 现有数据集（如HumanML3D、BEAT2）仅提供成对对齐——要么是文本-运动对，要么是音频-运动对，缺乏**同步的音频-文本-运动三元组**。这使得联合训练语音、语言和行为模型成为不可能。此外，不同模态采用各自的标准帧率（音频12.5/25/50Hz，运动20/30Hz），缺乏精确的跨模态时序同步机制，进一步加剧了模态对齐的困难。

### 本文动机：将非言语行为重新定义为对话智能的核心

针对上述缺口，本文提出**ViBES**（Speech–Language–Behavior model with Mixture-of-Modality-Experts），其核心动机在于**将非言语行为从辅助输出提升为对话智能的一等公民**。具体而言，ViBES追求三个目标：

1. **统一建模**：将语音、语言和行为整合在单一模型中，实现联合规划与生成，而非事后拼接。
2. **参数高效融合**：在保留预训练语音-语言骨干智能的前提下，以轻量级方式注入行为生成能力，避免灾难性遗忘。
3. **精确时序对齐**：构建大规模时间同步的三模态数据集，并设计跨模态时序编码机制，确保语音、文本和运动在毫秒级精度上对齐。

通过这一设计，ViBES旨在赋予3D虚拟身体**对话条件化的行为生成能力**——即，根据对话历史、当前话语和韵律特征，自主决定面部表情和身体动作的时机、类型与强度，从而向真正行为智能的对话代理迈出关键一步。



## 核心方法与创新机理

ViBES的根本创新在于将非言语行为从“模态翻译的后处理”重新定义为**对话智能的一等公民**，并为此构建了一个统一的语音-语言-行为（SLB）生成模型。其核心突破可归纳为三个相互耦合的架构与数据层面的changed slots。

### 1. 混合模态专家与不对称跨模态注意力

现有对话系统将语音、文本和动作视为分离的堆栈，通过级联或简单串联组合，缺乏统一的跨模态策略。ViBES采用**混合模态专家（MoME）架构**，以参数分割的方式将模型组织为三个Transformer专家：**语音-语言（TS）专家**、**面部表情专家**和**身体运动专家**。

关键设计在于**硬路由（hard routing）**——按模态将Token确定性地分配给对应专家，避免稀疏MoE中学习路由的不稳定性——以及**不对称的SLB-Attn注意力拓扑**。TS专家执行标准的自注意力以维持语言理解与语音生成能力：

$$
\mathbf{Q}_{\mathrm{ts}} = \mathrm{LN}_{\mathrm{attn}}(\mathbf{h}_{\mathrm{ts}}^{(\ell)}) W_{\mathrm{ts}}^{Q}, \quad
\mathbf{K}_{\mathrm{ts}} = \mathrm{LN}_{\mathrm{attn}}(\mathbf{h}_{\mathrm{ts}}^{(\ell)}) W_{\mathrm{ts}}^{K}, \quad
\mathbf{V}_{\mathrm{ts}} = \mathrm{LN}_{\mathrm{attn}}(\mathbf{h}_{\mathrm{ts}}^{(\ell)}) W_{\mathrm{ts}}^{V}.
$$

$$
\tilde{\mathbf{h}}_{\mathrm{ts}}^{(\ell)} = \mathbf{h}_{\mathrm{ts}}^{(\ell)} + \mathrm{Softmax}\Big(\frac{\mathbf{Q}_{\mathrm{ts}}\mathbf{K}_{\mathrm{ts}}^{\top}}{\sqrt{d_h}}\Big)\mathbf{V}_{\mathrm{ts}} W_{\mathrm{ts}}^{O}.
$$

而面部和身体专家**仅通过交叉注意力从TS流读取信息**，不执行自注意力，也不相互通信：

$$
\mathbf{Q}_{\mathrm{face}} = \mathrm{LN}_{\mathrm{attn}}(\mathbf{h}_{\mathrm{face}}^{(\ell)}) W_{\mathrm{face}}^{Q}, \quad
\mathbf{Q}_{\mathrm{body}} = \mathrm{LN}_{\mathrm{attn}}(\mathbf{h}_{\mathrm{body}}^{(\ell)}) W_{\mathrm{body}}^{Q}.
$$

$$
\tilde{\mathbf{h}}_{\mathrm{face}}^{(\ell)} = \mathbf{h}_{\mathrm{face}}^{(\ell)} + \mathrm{Softmax}\Big(\frac{\mathbf{Q}_{\mathrm{face}}\mathbf{K}_{\mathrm{ts}}^{\top}}{\sqrt{d_h}}\Big)\mathbf{V}_{\mathrm{ts}} W_{\mathrm{face}}^{O}.
$$

这一设计的因果逻辑是：**一旦面部和身体流充分条件化于语音-语言流，它们之间基本独立**。消融实验证实，启用Face↔Body注意力未带来可测量的性能提升（Section 3.2），从而验证了移除该连接的设计合理性。此外，TS骨干基于预训练的**GLM-4-9B**语音LLM并保持冻结，仅附加轻量级的侧挂运动专家，以参数高效的方式保留了语言与韵律智能。

### 2. 多模态分数旋转位置编码

不同模态使用各自的标准帧率（音频12.5/25/50Hz，运动20/30Hz等），缺乏精确的跨模态时序同步，是先前工作的一个结构性缺陷。ViBES统一采用**25fps主时钟**，并引入**分数旋转位置编码（Fractional RoPE）** 以实现精确的跨模态时间对齐。

核心机制是：以TS流令牌的整数位置索引为锚点，利用时间戳对运动令牌进行线性插值，赋予其分数索引：

$$
\alpha_t = \frac{u(t) - u(a_i)}{u(a_{i+1}) - u(a_i)} \in [0, 1), \qquad s_t = s_{a_i} + \alpha_t.
$$

对于位于第一个TS锚点之前的运动令牌，采用左尾外推。此外，可选的模态相位调整 $\hat{s}_t = \gamma_{m_t} s_t + \delta_{m_t}$ 进一步稳定训练并减少模态边界冲突。RoPE的逆频率阶梯 $\omega_j = b^{-\frac{2j}{d_{\mathrm{rot}}}}$ 则为跨模态序列提供了统一的时间感知位置嵌入。这一设计使得交错的多模态Token序列能够在单一旋转时间线上保持时序一致性，是联合建模语音节奏与身体运动节奏的基础。

### 3. 大规模时间同步三模态数据集

现有数据集（如HumanML3D、BEAT2）仅提供成对对齐（文本-运动或音频-运动），缺乏大规模的时间对齐音频-文本-运动三元组，从根本上限制了对话行为联合建模的可能性。ViBES构建了**Converse3D**数据集，约1000小时，来源包括三类互补数据：(i) 真实YouTube对话视频经单目3D重建管线处理；(ii) 高质量现有运动数据集；(iii) 受控合成数据。所有运动统一表示为SMPL-X和FLAME参数，并时间对齐到25fps主时钟。

这一数据层面的创新是前述架构设计得以成立的前提：只有在大规模三模态同步数据上训练，MoME架构中的跨模态注意力才能真正学习到语音韵律、语言语义与面部/身体运动之间的对话条件化映射关系。

**创新总结**：ViBES通过“参数分割的专家架构 + 分数时序对齐 + 大规模三模态数据”的组合，将非言语行为生成从模态翻译提升为对话上下文条件化的联合规划问题，同时以冻结骨干的方式保留了预训练语音LLM的语言智能——这一“能力保留式扩展”的设计哲学是其区别于简单端到端训练方法的核心特征。



ViBES 的整体框架围绕一个核心设计原则展开：将非言语行为（面部表情与身体动作）从附属的模态翻译任务提升为对话智能的一等公民，并与语音、语言在统一模型内进行联合规划与生成。为此，ViBES 采用端到端的自回归架构，将所有模态转换为统一的令牌空间，并通过混合模态专家（MoME）与不对称跨模态注意力（SLB-Attn）实现参数高效且可控的跨模态融合。

### 流水线总览

ViBES 由三个关键模块串联构成，形成从原始多模态信号到 3D 虚拟身体动作的完整推理链路：

1.  **多模态分词器**：将文本、语音、面部运动与身体运动分别转换为离散令牌序列，并统一到 25fps 的主时钟上，为跨模态时序对齐奠定基础。
2.  **语音-语言-行为模型主干**：基于冻结的预训练语音 LLM 骨干（GLM-4-9B）构建，引入三个模态专属的 Transformer 专家——语音-语言专家、面部专家和身体专家——通过硬路由按模态分配令牌，并利用不对称 SLB-Attn 实现跨模态信息共享。
3.  **多模态分数旋转位置编码**：为交错的多模态令牌序列提供精确的时间位置编码，以 TS 流整数索引为锚点，通过线性插值赋予运动令牌分数索引，并支持可选的模态相位偏移与缩放。

Figure 2 展示了这一架构的全貌：音频、文本和运动数据分别经各自的分词器处理后，以交错令牌流的形式送入 MoME 主干，最终自回归地生成语音响应与同步的 3D 面部及身体动画。

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/002_Figure_2.jpg]]
*Figure 2: Model overview. The model adopts an autoregressive structure that converts all modalities into a unified token space. It consists of a Speech–Language–Behavior model with a Mixture-of-Modality-Experts (MoME) architecture, which processes audio, motion, and text inputs while sharing cross-modal information through the proposed Speech–Language–Behavior Attention (SLB-Attn) mechanism*

### 模块间关系与数据流

三个模块之间的协作关系体现了 ViBES “冻结骨干 + 侧挂专家” 的核心设计哲学：

- **分词器 → 主干**：分词器输出的交错令牌序列是主干的唯一输入。文本令牌携带语义信息与词级时间戳，语音令牌携带韵律与副语言线索，面部和身体令牌则编码了 SMPL-X/FLAME 参数空间的运动先验。所有令牌在进入主干前已通过分数 RoPE 注入了统一的时间位置信息。
- **主干内部的信息流**：MoME 架构采用硬路由策略——每个令牌根据其模态类型被确定性分配给对应的 FFN 专家和 LayerNorm，无需学习路由。跨模态交互完全通过 SLB-Attn 实现：TS 专家执行自注意力以维护语言理解与语音生成的上下文；面部和身体专家则仅通过交叉注意力从 TS 专家的键/值对中读取信息，彼此之间不直接交互。消融实验证实，启用面部与身体之间的注意力无法带来可测量的性能提升，表明在条件化于 TS 流之后，面部与身体流在很大程度上是独立的（Section 3.2）。
- **主干 → 输出**：主干自回归生成的令牌序列经解码头还原为语音波形、面部 FLAME 参数和身体 SMPL-X 参数，驱动 3D 虚拟身体在对话中做出社交恰适的非言语行为。

### 输入输出规范

| 模态 | 输入形式 | 输出形式 | 帧率/频率 |
|------|----------|----------|-----------|
| 文本 | 子词令牌序列（Tiktoken），附带词级时间戳 | 生成的文本响应令牌 | 与语音对齐 |
| 语音 | 12.5Hz 残差量化令牌 | 生成的语音令牌 → 波形 | 12.5Hz（令牌），25fps（时钟） |
| 面部 | FLAME 参数令牌（表情、下颌姿态） | 生成的面部运动令牌 → FLAME 参数 | 25fps |
| 身体 | SMPL-X 参数令牌（身体姿态、手部姿态） | 生成的身体运动令牌 → SMPL-X 参数 | 25fps（上采样自 6.25fps） |

所有运动流在融合前均重采样至统一的 25fps 主时钟，确保跨模态时序一致性。这一标准化是分数 RoPE 能够精确对齐不同模态时间索引的前提。

### 补充图表

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/001_Figure_1.jpg]]
*Figure 1: We present a novel speech–language–behavior (SLB) model with a mixture–of–modality–experts (MoME) architecture that ingests audio, motion, or text and shares cross-modal information via speech–language–behavior Attention (SLB-Attn). Along with a 1,000-hour conversational behavior corpus that we curate, the model advances toward endowing AI agents with a unified 3D virtual body*



ViBES 由三个核心模块构成：**多模态分词器**、**语音-语言-行为模型主干（SLB Model with MoME）**和**多模态分数旋转位置编码（Fractional RoPE）**。以下逐一展开其设计机理与关键公式。

### 多模态分词器（Multimodal Tokenizer）

该模块将异质的语音、文本、面部和身体运动统一转换为离散令牌序列，并映射到 **25 fps 的统一主时钟**上，以消除模态间的帧率差异。

- **文本**：使用 Tiktoken 进行子词分词，每个令牌附带词级时间戳。
- **语音**：以 12.5 fps 的残差量化（RQ）令牌表示，通过令牌-帧映射与 25 fps 时钟对齐。
- **面部运动**：采用 FLAME 参数模型，以 25 fps 原生帧率表示，无需重采样。
- **身体运动**：采用 SMPL-X 参数模型，原始帧率为 6.25 fps 或 25 fps，统一重采样至 25 fps。

这一标准化时钟是整个架构跨模态时序对齐的基础，确保后续位置编码与注意力计算的精确性。

### 语音-语言-行为模型主干（SLB Model with MoME）

模型基于 GLM-4-9B 骨干构建，采用**混合模态专家（Mixture-of-Modality-Experts, MoME）**架构，包含三个模态专属的前馈网络专家与层归一化：

- **TS 专家**：处理文本和语音令牌，负责语言理解与语音生成。
- **面部专家**：处理面部运动令牌。
- **身体专家**：处理身体运动令牌。

与稀疏 MoE 中可学习的路由器不同，ViBES 采用**硬路由**——按令牌的模态类型确定性分配至对应专家，无需额外路由参数。

**不对称跨模态注意力（SLB-Attn）** 是融合机制的核心。TS 令牌执行标准的自注意力，而面部和身体令牌仅通过交叉注意力从 TS 令牌中读取信息，彼此之间不进行注意力交互。具体而言：

**TS 注意力投影与自注意力更新：**

$$\mathbf{Q}_{\mathrm{ts}} = \mathrm{LN}_{\mathrm{attn}}(\mathbf{h}_{\mathrm{ts}}^{(\ell)}) W_{\mathrm{ts}}^{Q}, \quad \mathbf{K}_{\mathrm{ts}} = \mathrm{LN}_{\mathrm{attn}}(\mathbf{h}_{\mathrm{ts}}^{(\ell)}) W_{\mathrm{ts}}^{K}, \quad \mathbf{V}_{\mathrm{ts}} = \mathrm{LN}_{\mathrm{attn}}(\mathbf{h}_{\mathrm{ts}}^{(\ell)}) W_{\mathrm{ts}}^{V}.$$

$$\tilde{\mathbf{h}}_{\mathrm{ts}}^{(\ell)} = \mathbf{h}_{\mathrm{ts}}^{(\ell)} + \mathrm{Softmax}\Big(\frac{\mathbf{Q}_{\mathrm{ts}}\mathbf{K}_{\mathrm{ts}}^{\top}}{\sqrt{d_h}}\Big)\mathbf{V}_{\mathrm{ts}} W_{\mathrm{ts}}^{O}.$$

其中 $\mathbf{h}_{\mathrm{ts}}^{(\ell)}$ 为第 $\ell$ 层 TS 令牌的隐藏状态，$W_{\mathrm{ts}}^{Q}, W_{\mathrm{ts}}^{K}, W_{\mathrm{ts}}^{V}, W_{\mathrm{ts}}^{O}$ 为 TS 专属的投影矩阵，$d_h$ 为每个注意力头的维度。

**TS 专家前馈：**

$$\mathbf{h}_{t}^{(\ell+1)} = \tilde{\mathbf{h}}_{t}^{(\ell)} + \mathrm{FFN}_{\mathrm{ts}}\big(\mathrm{LN}_{\mathrm{ts}}(\tilde{\mathbf{h}}_{t}^{(\ell)})\big), \quad \text{for } m_{t} \in \mathcal{M}_{\mathrm{ts}}.$$

**面部/身体查询投影与交叉注意力更新：**

$$\mathbf{Q}_{\mathrm{face}} = \mathrm{LN}_{\mathrm{attn}}(\mathbf{h}_{\mathrm{face}}^{(\ell)}) W_{\mathrm{face}}^{Q}, \quad \mathbf{Q}_{\mathrm{body}} = \mathrm{LN}_{\mathrm{attn}}(\mathbf{h}_{\mathrm{body}}^{(\ell)}) W_{\mathrm{body}}^{Q}.$$

$$\tilde{\mathbf{h}}_{\mathrm{face}}^{(\ell)} = \mathbf{h}_{\mathrm{face}}^{(\ell)} + \mathrm{Softmax}\Big(\frac{\mathbf{Q}_{\mathrm{face}}\mathbf{K}_{\mathrm{ts}}^{\top}}{\sqrt{d_h}}\Big)\mathbf{V}_{\mathrm{ts}} W_{\mathrm{face}}^{O},$$

$$\tilde{\mathbf{h}}_{\mathrm{body}}^{(\ell)} = \mathbf{h}_{\mathrm{body}}^{(\ell)} + \mathrm{Softmax}\Big(\frac{\mathbf{Q}_{\mathrm{body}}\mathbf{K}_{\mathrm{ts}}^{\top}}{\sqrt{d_h}}\Big)\mathbf{V}_{\mathrm{ts}} W_{\mathrm{body}}^{O}.$$

这里的关键设计是：面部和身体令牌的查询来自自身隐藏状态，但键和值复用 TS 流的 $\mathbf{K}_{\mathrm{ts}}$ 和 $\mathbf{V}_{\mathrm{ts}}$，输出投影 $W_{\mathrm{face}}^{O}$ 和 $W_{\mathrm{body}}^{O}$ 则各自独立。这意味着运动专家仅通过“读取”语音-语言骨干的表示来获取对话上下文，而不反向影响语言理解。

**消融实验证实**，启用面部与身体专家之间的注意力无法带来可测量的性能提升——一旦条件化于 TS 流，面部与身体流在很大程度上独立。这一发现直接支撑了不对称注意力拓扑的设计合理性。

### 多模态分数旋转位置编码（Fractional RoPE）

由于不同模态的令牌以不同帧率交错排列，标准整数位置索引无法精确表达跨模态时序关系。ViBES 引入分数 RoPE，在统一的旋转时间线上为每个令牌赋予标量索引 $s_t$（可为非整数）。

以 TS 令牌的整数索引为锚点，对运动令牌进行线性插值：

$$\alpha_t = \frac{u(t) - u(a_i)}{u(a_{i+1}) - u(a_i)} \in [0, 1), \qquad s_t = s_{a_i} + \alpha_t.$$

其中 $u(t)$ 为运动令牌 $t$ 的时间戳，$a_i$ 和 $a_{i+1}$ 为相邻 TS 锚点，$s_{a_i}$ 为锚点的整数索引。对于第一个 TS 锚点之前的运动令牌，采用左尾外推：

$$s_t = s_{a_0} - \frac{u(a_0) - u(t)}{\bar{\Delta}},$$

其中 $\bar{\Delta}$ 为平均锚点间隔。

为进一步稳定训练并减少边界冲突，引入可选的模态相位调整：

$$\hat{s}_t = \gamma_{m_t} s_t + \delta_{m_t},$$

其中 $\gamma_{m_t}$ 和 $\delta_{m_t}$ 为模态 $m_t$ 的缩放因子与相位偏移。

RoPE 的频率通道定义为逆频率阶梯：

$$\omega_j = b^{-\frac{2j}{d_{\mathrm{rot}}}}, \quad j = 0, \ldots, L-1,$$

其中 $d_{\mathrm{rot}}$ 为旋转维度，$b$ 为基数。该设计使位置编码能够感知不同模态的时序粒度，在交错令牌序列中维持精确的跨模态时序一致性。

### 补充图表

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/011_Figure_6.jpg]]
*Figure 6: Overview of our YouTube data processing pipeline. The raw videos are processed to obtain high-quality 3D poses using automatic algorithms*



## 实验与关键发现

### 核心性能：对话行为基准

ViBES在Converse3D测试集上对对话行为生成质量进行了系统性评估，结果汇总于**Table 2**。模型在平衡R-Precision（R1-Balanced）上达到**0.467**，显著优于最佳先验方法LoM的0.323（+0.144），证明联合建模语音-语言-行为能够大幅提升对话与动作之间的语义对齐。在分布质量指标FID上，ViBES取得**93.9**，远优于MotionGPT的262.2（-168.3），同时多样性（Diversity）达到10.73，接近真实数据的分布宽度。MMDist降至3.178，优于LoM的3.435，进一步验证生成动作与真实分布的距离更小。

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/004_Table_2.jpg]]
*Table 2: Benchmarking conversational behavior. “↑” indicates that higher values are better. The best results are in bold*

这些指标的同步提升揭示了一个关键机制：**SLB-Attn的非对称跨模态注意力**使面部和身体运动能够直接条件化于语音-语言流（TS），从而在保留语言理解与韵律智能的同时，生成社交恰适的3D身体行为。相比之下，MotionGPT等文本到运动基线缺乏对话上下文建模能力，而LoM等协同语音手势方法未将行为视为对话智能的核心组成部分，导致R-Precision和FID均出现显著退化。

### 语音智能保留验证

为验证模型在引入运动生成后是否损害了语音LLM的语言能力，ViBES在语音指标上进行了评估（**Table 3**）。上下文相关性得分**4.584**，角色一致性得分**4.376**，均接近真实值上限（4.838 / 4.893）。这一结果表明，**冻结预训练语音-语言骨干并附加侧挂运动专家的设计**成功保留了基础模型的语言与韵律智能，未因多模态训练而出现灾难性遗忘。

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/005_Table_3.jpg]]
*Table 3: Quantitative results on speech metrics. “↑” indicates higher-is-better; best values are in bold*

### 消融实验：注意力拓扑的合理性

在架构设计中，ViBES有意禁用了面部专家与身体专家之间的直接注意力，仅保留它们各自到TS专家的交叉注意力。消融实验证实，**启用面部与身体注意力无法带来可测量的性能改进**（Section 3.2）。这一发现具有重要的因果解释：一旦面部和身体流充分条件化于语音-语言流，它们之间的直接交互便成为冗余，两个运动流在很大程度上呈现条件独立。该消融直接验证了SLB-Attn非对称设计的合理性——以TS流为信息瓶颈，既降低了计算开销，又避免了跨运动模态的噪声耦合。

### 说话人头部合成与协同语音手势

在说话人头部合成任务上（**Table 4**），ViBES与MultiTalk、ScanTalk、DiffPoseTalk、ARTalk等专用头部合成方法进行了对比。在协同语音手势生成方面（**Table 5**），ViBES在BEATv2基准上报告了FGD和BC指标。这些结果共同表明，**统一的SLB模型在子任务上同样具有竞争力**，尽管其设计目标是更广泛的对话行为生成，而非针对单一模态或任务进行优化。

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/006_Table_4.jpg]]
*Table 4: Results on talking-head synthesis. We use colors to denote the first and second places respectively. * indicates that the method was not trained on TFHP [105]*

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/009_Table_5.jpg]]
*Table 5: Co-speech gesture generation results on BEATv2 benchmark. We report FGD ×10−1, BC ×10−1*

### 数据集与评估的局限

需要明确指出的是，当前评估体系存在若干结构性局限：

1. **分布度量与社交得体性的差距**：FID、R-Precision等指标主要衡量生成分布与真实分布的相似性以及运动-文本检索精度，无法全面捕捉对话行为的**社交得体性**和**时机恰当性**。一个低FID的动作序列仍可能在对话上下文中显得不合时宜。
2. **单目重建伪影的传导**：Converse3D数据集依赖SPECTRE、4D-Humans、HaMeR等自动3D重建管线，在遮挡或低分辨率场景下可能引入运动伪影，这些噪声会通过训练传递给生成模型，影响输出质量。
3. **语言与文化的代表性偏差**：数据集主要来源于英语YouTube对话，模型在多语言和跨文化场景下的泛化能力尚未验证。

### 失败模式与开放问题

从实验设计和结果中可识别出以下失败模式与待解决问题：

- **LLM推理能力的未充分利用**：当前模型冻结了语音-语言骨干，仅训练运动专家和注意力投影层。这意味着现代LLM的常识推理和社交规划能力尚未被充分释放到行为生成中。如何实现全参数端到端训练，使LLM的推理能力直接参与运动规划，是下一步的关键挑战。
- **数据集规模与多样性的瓶颈**：尽管Converse3D已达到约1000小时规模，但作者明确指出仍需进一步扩大数据集以支持全参数微调。当前数据规模可能限制了模型对细粒度社交线索（如讽刺、犹豫、情感转折）的建模精度。
- **评估体系的缺失维度**：缺乏与人类偏好对齐的评估模型，无法自动衡量生成行为的整体对话质量。这一缺失使得模型迭代缺乏闭环反馈，需要依赖昂贵的人工评估。

### 补充图表

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/003_Table_1.jpg]]
*Table 1: Comparison of Converse3D with existing datasets. We report the duration of Converse3D as N/A, since it is constructed by combining web YouTube videos and other datasets, making a direct comparison in hours less meaningful*

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/007_Figure_3.jpg]]
*Figure 3: Qualitative examples of conversational behavior. We show one example for text-based interaction (top) and one example for audio-based interaction (bottom)*

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/010_Figure_5.jpg]]
*Figure 5: Qualitative comparison for text-to-motion. While ViBES targets conversational behavior, its autoregressive design also supports text-to-motion generation for fair comparison with existing methods*

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/012_Figure_7.jpg]]
*Figure 7: Application: driving video generation with ViBES. We use our generated 3D head motion as a behavioral condition to control an off-the-shelf video generation model (Runway AI [100]), producing realistic talking avatars*

![[assets/figures/papers/paper_list_l2651_https_arxiv_org_abs_2512_14234/figures/015_Figure_10.jpg]]
*Figure 10: Additional qualitative examples for text-to-motion generation. Given a text caption, we compare the 3D motion generated by our method with those generated by state-of-the-art methods, including MotionGPT [45], LoM [11], and MoMask [37]. Our model produces smooth, natural, and sometimes better motion in comparison with existing methods, which do not model the conversaion behavior*



## 定位与知识库关联

### 1. 问题定位：从模态翻译到对话智能

现有对话系统普遍将非言语行为建模为孤立的模态翻译任务——语音转手势、文本转表情——缺乏对“何时移动、做什么、如何在多轮对话中适应”的智能决策。这导致三个结构性缺陷：

- **时序生硬**：语音、文本和动作堆栈各自采用不同帧率（音频12.5/25/50Hz，运动20/30Hz），缺乏精确的跨模态同步，动作与语义/韵律的耦合松散。
- **社交基础薄弱**：模型仅学习表面映射，未将身体行为纳入对话上下文推理，难以产生社交恰适的点头、手势和表情。
- **架构碎片化**：分离的语音、文本和动作模型通过简单级联组合，模态间缺乏统一的生成策略与信息共享机制。

ViBES的核心洞察在于：**将非言语行为重新定义为对话智能的一等公民**，而非附属输出。这要求模型在统一的架构内同时理解语言内容、语音韵律和社交上下文，并据此生成可控的3D身体行为。

### 2. 方法谱系：与现有路线的对比

ViBES位于三条研究路线的交汇处，但以独特的架构选择与每条路线形成差异。

#### 2.1 协同语音手势生成

该路线以音频驱动为主，代表性工作包括 **SynTalker**、**EMAGE** 和 **LoM**。这些方法将身体运动视为语音的伴随产物，通过编码器-解码器或扩散模型学习音频到运动的映射。其根本局限在于：仅建模“怎么说”到“怎么动”的浅层关联，无法捕捉“说什么”和“对话上下文”对行为的约束。

ViBES的突破在于引入文本作为第三模态，将语音-语言-行为统一在自回归框架中。在Converse3D测试集上，ViBES的平衡R-Precision达到**0.467**，显著超过最佳先验方法LoM的**0.323**（Table 2），FID降至**93.9**，远优于MotionGPT的**262.2**。这表明联合建模语言内容大幅提升了对话-动作对齐精度。

#### 2.2 文本到运动生成

**T2M**、**MotionGPT** 和 **MoMask** 等文本到运动方法虽能生成多样化的动作序列，但其设计目标为通用动作合成，缺乏对对话场景的专门优化。这些模型通常在HumanML3D等通用运动数据集上训练，动作分布与对话行为存在显著差异。

ViBES虽以对话行为为核心目标，但其自回归设计天然支持文本到运动生成。定性比较显示（Figure 5），ViBES在对话相关场景中产生的动作更平滑自然，这得益于Converse3D数据集提供的对话上下文先验。

#### 2.3 说话人头部合成

**MultiTalk**、**ScanTalk**、**DiffPoseTalk** 和 **ARTalk** 等方法专注于语音驱动的3D头部动画，通常将头部姿态固定以简化问题。这些方法在TFHP等数据集上表现优异，但面部与身体行为分离建模，无法产生全身协调的对话行为。

ViBES将面部和身体统一在MoME架构中，通过共享的TS骨干实现协同生成。在说话人头部合成任务上（Table 4），ViBES在多项指标上达到最优或次优，同时保持了全身行为的整体一致性。

### 3. 架构决策的知识贡献

ViBES的方法论贡献可归纳为三个相互依赖的设计选择，每个选择均针对现有路线的具体瓶颈。

#### 3.1 混合模态专家（MoME）与不对称注意力

传统多模态Transformer通常采用全连接自注意力或简单的跨模态串联。ViBES引入硬路由的MoME架构：三个FFN专家（TS、面部、身体）按模态确定性分配令牌，注意力拓扑设计为不对称的SLB-Attn——TS令牌执行自注意力以融合语音-语言信息，面部和身体令牌仅通过交叉注意力从TS键/值读取信息。

这一设计的关键证据来自消融实验：**启用面部与身体专家之间的注意力无法带来可测量的性能提升**（Section 3.2）。这表明一旦条件化于TS流，面部和身体流在很大程度上独立。该发现验证了不对称注意力的合理性，同时带来参数效率优势——冻结预训练语音LLM骨干，仅训练轻量级的侧挂运动专家。

#### 3.2 分数旋转位置编码（Fractional RoPE）

跨模态时序对齐是多模态序列建模的长期挑战。现有方案通常依赖独立的帧率或粗略的时间戳对齐。ViBES提出统一25fps主时钟，通过TS锚点的线性插值为运动令牌赋予分数索引：

$$\alpha_t = \frac{u(t) - u(a_i)}{u(a_{i+1}) - u(a_i)} \in [0, 1), \quad s_t = s_{a_i} + \alpha_t$$

并引入可选的模态相位偏移与缩放：

$$\hat{s}_t = \gamma_{m_t} s_t + \delta_{m_t}$$

这种设计使不同帧率的模态令牌共享同一旋转时间线，实现了精确的跨模态时序一致性，同时避免了显式时间戳编码的冗余。

#### 3.3 大规模三模态同步数据集

方法创新的有效性高度依赖训练数据。现有数据集（如HumanML3D、BEAT2）仅提供成对对齐（文本-运动或音频-运动），缺乏时间对齐的音频-文本-运动三元组。ViBES构建的Converse3D数据集约1000小时，从三个互补来源策划：YouTube对话视频、现有高质量运动数据和受控合成数据。所有运动统一表示为SMPL-X和FLAME参数，对齐到25fps时钟。

这一数据基础设施使首次大规模三模态联合训练成为可能，是ViBES性能优势的物质基础。

### 4. 适用边界与局限

#### 4.1 数据覆盖与泛化

Converse3D主要来源于英语YouTube对话，存在语言和文化的代表性偏差。模型在多语言和跨文化场景下的泛化能力尚未验证。此外，数据集规模仍需进一步扩大，以支持全参数语音LLM骨干的端到端训练，从而释放现代LLM的全部推理能力。

#### 4.2 运动质量瓶颈

单目3D重建管线（SPECTRE、4D-Humans、HaMeR）在处理遮挡或低分辨率视频时可能引入运动伪影，这些伪影会传递给生成的运动，影响视觉质量和社交真实感。面部和手部标注依赖自动算法，部分数据可能存在噪声。

#### 4.3 评估指标局限

现有评估指标（FID、R-Precision、Diversity）主要衡量分布相似性和运动-文本检索精度，尚无法全面评估对话行为的社交得体性与时机恰当性。如何构建与人类偏好对齐的评估模型，仍是开放问题。

### 5. 开放问题与未来方向

1. **全参数端到端训练**：当前ViBES冻结预训练语音LLM骨干，仅微调运动专家。扩展数据集以支持全参数训练，有望进一步释放LLM的常识推理与社交规划能力。

2. **深层推理与社交规划**：如何使模型在生成运动的同时进行更深层的对话上下文推理——例如，根据对方情绪调整自身表情、根据话题转换调整手势风格——是通向真正社交智能的关键。

3. **运动伪影缓解**：改进单目重建管线或引入多视图/深度传感器数据，从源头提升训练数据质量；或设计鲁棒的训练策略，降低对重建噪声的敏感性。

4. **人类偏好对齐的评估**：构建能够综合衡量行为自然度、社交得体性和时机恰当性的评估框架，可能借助LLM-as-judge或人类偏好学习的方法。

5. **多模态行为控制与编辑**：当前模型以自回归生成行为序列，未来可探索细粒度的行为控制（如指定特定手势、表情强度）和交互式编辑能力。



## 原文 PDF

![[paperPDFs/CVPR_2026/ViBES_A_Conversational_Agent_with_Behaviorally_Intelligent_3D_Virtual_Body.pdf]]
