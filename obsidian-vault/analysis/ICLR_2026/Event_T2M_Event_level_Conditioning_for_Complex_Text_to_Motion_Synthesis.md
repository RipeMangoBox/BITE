---
title: "Event-T2M: Event-level Conditioning for Complex Text-to-Motion Synthesis"
type: paper
paper_level: A
venue: ICLR
year: 2026
pdf_ref: paperPDFs/ICLR_2026/Event_T2M_Event_level_Conditioning_for_Complex_Text_to_Motion_Synthesis.pdf
project_link: https://tjswodud.github.io/EventT2M
code_link: null
openreview_forum_id: mXPeXZ1KWT
aliases:
- ET
- Event-T2M
tags:
- ICLR_2026
- topic/generative_models_diffusion
- topic/generative_models_diffusion/generative_models_and_autoencoders
core_operator: "通过引入事件（event）的严格定义，将文本提示分解为独立事件序列，为每个事件生成专用的运动感知嵌入，并通过事件级交叉注意力（ECA）将这些事件标记注入扩散模型的Conformer块中，从而显式建模动作的顺序和组合关系。"
primary_logic: "将文本到动作生成的问题从单一全局嵌入扩展到事件级条件注入，使得模型能够在生成过程中专注于每个语义自包含的动作单元，同时通过全局标记保持整体连贯性，从而在复杂的多动作序列上实现顺序准确、过渡自然的运动合成。"
claims:
- "Event-T2M在HumanML3D-E基准上，当事件数增加时，表现显著优于所有基线，尤其是在≥4事件的条件下，R-Precision Top-1达到0.466（相对于最佳基线MoMask的0.441），FID为0.265（相对于0.418）。"
- "用户研究显示，Event-T2M在保真度、顺序对齐和自然度方面与真实运动无统计学显著差异，显著优于其他方法。"
- "消融实验证实，事件级交叉注意力（ECA）相比词级注意力能持续提高R-Precision，特别是在事件数较多的条件下。"
- "LLM的事件分解准确度达到93.3%，且人工标注的测试集与LLM分割的结果一致，表明方法不依赖于特定的LLM管道。"
---

# Event-T2M: Event-level Conditioning for Complex Text-to-Motion Synthesis

> [!tip] 核心洞察
> 将文本到动作生成的问题从单一全局嵌入扩展到事件级条件注入，使得模型能够在生成过程中专注于每个语义自包含的动作单元，同时通过全局标记保持整体连贯性，从而在复杂的多动作序列上实现顺序准确、过渡自然的运动合成。

| 字段 | 内容 |
| ------ | ------ |
| 中文题名 | Event-T2M：面向复杂文本到动作合成的事件级条件生成 |
| 英文题名 | Event-T2M: Event-level Conditioning for Complex Text-to-Motion Synthesis |
| 会议/期刊 | ICLR 2026 |
| Links | [paper](https://openreview.net/forum?id=mXPeXZ1KWT) · [Project](https://tjswodud.github.io/EventT2M) |
| Topic | #topic/generative_models_diffusion #topic/generative_models_diffusion/generative_models_and_autoencoders |
| Method | Event-T2M |
| Dataset | HumanML3D, HumanML3D-E (Condition 4), KIT-ML |

> [!tip] 效果简介
> - HumanML3D 上，R-Precision Top-1 为 0.562±.002，对比 0.529±.003 (MoGenTS)，变化 +0.033。
> - HumanML3D-E (Condition 4) 上，R-Precision Top-1 为 0.466±.008，对比 0.441±.013 (MoMask)，变化 +0.025。
> - HumanML3D-E (Condition 4) 上，FID 为 0.265±.007，对比 0.418±.030 (MoMask)，变化 降低0.153。

## 概要

文本到动作（Text-to-Motion）生成的核心瓶颈在于：现有系统将包含多个动作的复杂提示压缩为单一的全局文本嵌入（如CLIP的[EOS]标记），这一操作抹去了动作的时间顺序与独立语义，导致生成结果中出现动作遗漏、顺序重排和不自然的过渡。

Event-T2M针对这一瓶颈提出了因果性解法：**将文本到动作的生成从单点全局条件扩展为事件级序列条件**。具体而言，该方法将输入提示分解为独立的事件子句，为每个事件生成专用的运动感知嵌入，并通过事件级交叉注意力（ECA）将这些事件标记注入扩散模型的Conformer块中，使模型在生成过程中能够聚焦于每个语义自包含的动作单元，同时借助全局标记维持整体连贯性。

实验证据支撑了这一设计的有效性：
- 在标准基准HumanML3D上，Event-T2M的R-Precision Top-1达到0.562，优于最佳基线MoGenTS的0.529（Table 1）。
- 在按事件数分层的HumanML3D-E基准上，当事件数≥4时，R-Precision Top-1为0.466，较最佳基线MoMask的0.441提升显著；FID从0.418降至0.265，降幅达0.153（Table 3）。
- 用户研究表明，Event-T2M在保真度、顺序对齐和自然度三个维度上与真实运动无统计学显著差异，且显著优于所有对比方法（Figure 3）。
- 消融实验确认，事件级交叉注意力相比词级注意力能持续提升R-Precision，且LIMM和ATII模块对复杂事件生成至关重要（Table 4, Table 16）。

方法的局限性在于：当前未考虑长时间运动的物理合理性及人物与物体的交互，LLM事件分解环节引入了约1.43秒的额外延迟。



文本到动作生成（Text-to-Motion）旨在根据自然语言描述合成三维人体运动序列，其应用涵盖动画制作、虚拟现实和具身智能等领域。近年来，基于扩散模型和自回归架构的方法在这一任务上取得了显著进展，代表性工作包括 **MDM**（Tevet et al., 2022）、**MotionDiffuse**（Zhang et al., 2024a）、**T2M-GPT**（Zhang et al., 2023a）和 **MoMask**（Guo et al., 2024）等。然而，这些方法在应对包含多个独立动作的复杂提示时，暴露出一个根本性瓶颈。

### 全局嵌入的语义压缩瓶颈

现有系统普遍采用单一全局文本嵌入作为生成条件。具体而言，它们将整个文本提示（例如“一个人向前走，然后蹲下，再跳起来挥手”）通过 CLIP 或 TMR 等文本编码器压缩为一个固定维度的向量——通常取 CLIP 的 `[EOS]` 标记或 TMR 的全局输出。这一全局嵌入随后通过交叉注意力机制注入扩散去噪器或自回归解码器的每一层。

这种设计的核心缺陷在于：**单一向量无法保留多动作序列的时间顺序和独立语义**。当提示包含多个动作时，全局嵌入将“走”、“蹲”、“跳”、“挥手”等信息混叠在一起，模型在生成过程中失去了对动作单元边界的感知。这导致三类典型失败模式：

1. **动作遗漏**：部分事件在生成的运动序列中完全消失。
2. **顺序重排**：动作的执行顺序与文本描述不一致。
3. **过渡不自然**：动作之间的衔接缺乏连贯性，出现生硬的突变。

### 现有尝试的局限

部分工作试图缓解这一问题。例如，**AttT2M**（Zhong et al., 2023）和 **GraphMotion**（Jin et al., 2023）引入了词级或动词级的细粒度条件，但这些方法仍将文本视为扁平的标记序列，缺乏对“事件”这一语义自包含单元的结构化建模。它们可以关注到单个词汇（如“跳”），却无法区分“先走再跳”与“先跳再走”之间的顺序差异。实验证据表明，当提示中的事件数量增加时，这些基线的 FID 急剧上升、R-Precision 显著下降（见 Table 3, Figure 2a），说明词级条件并不能从根本上解决顺序组合泛化问题。

### 核心动机与研究问题

上述分析指向一个明确的研究动机：**如何将文本到动作生成的条件表示从单一全局嵌入扩展到事件级的结构化注入**，使得模型能够在生成过程中显式地感知每个独立动作单元及其先后关系？

为此，Event-T2M 提出了一套系统性的解决方案：首先通过大语言模型（LLM）将复杂提示分解为事件子句序列，然后为每个事件生成专用的运动感知嵌入，最后通过事件级交叉注意力（ECA）将这些事件标记注入扩散模型的 Conformer 块中。这一设计将生成问题从“给定一个全局描述生成整个运动”重新定义为“给定一个事件序列，按序合成并平滑连接各个动作单元”，从而在保持整体连贯性的同时，实现对复杂多动作序列的精确建模。



## 核心方法与创新机理

Event-T2M 的核心创新在于将文本到动作生成的条件表示从**单一全局文本嵌入**重构为**事件序列的条件注入**，从而解决复杂多动作提示中动作遗漏、顺序错乱和过渡不自然的问题。这一重构通过三个关键槽位的改变实现：

### 1. 文本条件表示：从全局嵌入到事件序列嵌入

现有方法（如 T2M、MDM、MoMask 等）将整个文本提示压缩为单个 CLIP 的 [EOS] 标记或等效的全局嵌入，无法保留动作的时间顺序和独立语义。Event-T2M 将文本提示通过 LLM 分解为独立的事件子句序列 $\{C_k\}_{k=1}^K$，然后为每个事件子句生成专用的运动感知嵌入：

$$E_k = f_{\mathrm{TMR}}(C_k), \qquad E_k \in \mathbb{R}^{D_y}$$

同时保留一个全局文本标记 $G = f_{\mathrm{TMR}}(W)$ 以维持整体语义连贯性。所有事件嵌入堆叠为矩阵 $\boldsymbol{E} \in \mathbb{R}^{K \times D_y}$，作为后续条件注入的基础。

### 2. 条件注入机制：事件级交叉注意力（ECA）

这是 Event-T2M 最关键的架构创新。现有方法使用标准交叉注意力将全局文本注入扩散去噪网络，无法细粒度地控制每个动作单元的生成时序。Event-T2M 在 Conformer 块中引入**事件级交叉注意力（ECA）**，以运动标记作为查询、事件标记作为键和值进行多头交叉注意力：

$$A^{(h)} = \mathrm{softmax}\bigg( \frac{Q_m^{(h)} (K_e^{(h)})^{\top}}{\sqrt{d_h}} \bigg), \quad Z^{(h)} = A^{(h)} V_e^{(h)}$$

$$ECA(x_t, E) = \gamma \cdot \mathrm{Dropout}(Z)$$

其中 $\gamma$ 是可学习的缩放因子，初始化为接近零以稳定训练。ECA 使得扩散模型能够在生成过程中**显式地关注每个语义自包含的动作单元**，从而在复杂多动作序列上实现顺序准确、过渡自然的运动合成。

消融实验（Table 4）证实，事件级交叉注意力相比词级注意力能持续提高 R-Precision，尤其在事件数较多的条件下（Condition 4 下 Top-1 从 0.441 提升至 0.466）。

### 3. 文本预处理：LLM 事件分解

现有方法直接使用全文作为输入，缺乏对动作结构的显式建模。Event-T2M 引入 LLM 作为前置分解器，将输入提示分割为事件子句序列。LLM 的事件分解准确度达到 93.3%，且人工标注的测试集与 LLM 分割的结果一致（Table 14），表明方法不依赖于特定的 LLM 管道。

### 配套架构创新

除上述三个核心槽位改变外，Event-T2M 还引入了两个辅助模块以增强事件级生成的能力：

- **LIMM（局部信息建模模块）**：通过深度可分离 1D 卷积在时间维度上强制局部平滑，为事件级条件提供更好的运动表示基础。
- **ATII（自适应文本信息注入器）**：通过门控机制根据运动上下文自适应注入全局文本语义，确保整体连贯性不被事件级条件破坏。

消融实验（Table 16）表明，移除 LIMM 或 ATII 均导致 FID 和 R-Precision 下降，验证了这些模块对事件级生成的必要性。



![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/001_Figure_1.jpg]]
*Figure 1: Main Architecture of Event-T2M. An input prompt is split into clauses by an LLM, encoded as event tokens with a TMR encoder, and fused with a global token. Tokens guide the diffusion process through an event-level module, enabling generation of sequentially complex motions*

Event-T2M 的整体设计围绕一个核心问题展开：现有文本到动作生成系统将复杂多动作提示压缩为单一全局文本嵌入（如 CLIP 的 `[EOS]` 标记），导致动作的时间顺序和独立语义丢失，生成结果中出现遗漏、重排和不自然过渡。Event-T2M 通过引入严格的事件定义，将生成问题从全局嵌入扩展到事件级条件注入，其 pipeline 由三个关键阶段构成：**事件分解与编码**、**事件级条件注入架构**、以及**扩散生成**。

### 输入输出流

系统输入为自然语言动作描述文本 $W$，输出为对应的 3D 人体运动序列。整体流程如下：

1. **LLM 事件分解**：输入文本 $W$ 首先通过大语言模型（LLM，具体使用 Gemini 2.5 Flash）分解为事件子句序列 $\{C_k\}_{k=1}^K$。LLM 的分解遵循严格的事件定义（Table 8），将“事件”界定为特定时间点上的同时性动作单元。该分解准确度达到 93.3%，且经人工标注验证与 LLM 分割结果一致（Table 14），表明 pipeline 不依赖于特定 LLM 管道。

2. **双路径文本编码**：
   - **事件嵌入**：每个事件子句 $C_k$ 通过运动感知的 TMR 编码器 $f_{\mathrm{TMR}}$ 映射为事件嵌入 $E_k \in \mathbb{R}^{D_y}$，所有事件嵌入堆叠为矩阵 $\boldsymbol{E} \in \mathbb{R}^{K \times D_y}$，作为后续事件交叉注意力的键和值。
   - **全局标记**：同时，完整提示 $W$ 通过同一 TMR 编码器生成全局语义嵌入 $G = f_{\mathrm{TMR}}(W)$，保留整体语义连贯性。

3. **事件级条件注入与扩散生成**：噪声运动样本 $x_t$ 进入由 $N$ 个相同 Event-T2M 块堆叠的 Conformer 架构，每个块按序执行以下操作：局部信息建模（LIMM）、自适应文本注入（ATII）、前馈网络、Conformer 自注意力、以及事件交叉注意力（ECA）。全局标记 $G$ 通过 ATII 的门控机制根据运动上下文自适应注入；事件标记 $\boldsymbol{E}$ 通过 ECA 以运动标记为查询、事件标记为键值进行多头交叉注意力，输出经可学习的缩放因子 $\gamma$（初始化为接近零）和 Dropout 调控后注入运动表示。去噪器 $\varphi_{\theta}$ 在时间步 $t$、全局标记 $G$ 和事件标记 $\boldsymbol{E}$ 的条件下，从 $x_t$ 预测原始运动 $x_0$。

### 模块关系

Event-T2M 的架构由以下核心模块协同构成（Figure 1）：

| 模块 | 角色 | 关键设计 |
|------|------|----------|
| **LLM 事件分解器** | 将输入文本分解为事件子句序列 | 使用事件感知提示模板，准确度 93.3% |
| **TMR 事件编码器** | 为每个事件子句生成运动感知嵌入 | 运动检索预训练，捕捉动作语义 |
| **全局标记提取** | 为完整提示生成全局语义嵌入 | 保持整体连贯性 |
| **LIMM** | 促进运动序列的局部时间平滑 | 深度可分离 1D 卷积 + GroupNorm + ReLU |
| **ATII** | 根据运动上下文自适应注入全局文本语义 | Sigmoid 门控机制，逐通道调控 |
| **Conformer 块** | 长期与短期时间建模 | 自注意力 + 卷积的结合 |
| **ECA** | 将事件嵌入通过交叉注意力注入运动表示 | 运动查询 × 事件键值，可学习缩放因子 |
| **扩散去噪器** | 从噪声样本恢复干净运动 | 10 步 DDPM，条件为 $t, G, \boldsymbol{E}$ |

### 关键设计决策

- **事件级 vs 词级条件**：消融实验（Table 4）证实，事件级交叉注意力（ECA）相比词级注意力能持续提高 R-Precision，尤其在事件数较多时（Condition 4 下 Top-1 从 0.441 提升至 0.466）。这是因为词级注意力将语义分散到单个词上，无法保留有序依赖关系，而 ECA 直接以语义自包含的事件单元为基础进行条件注入。

- **Conformer vs Transformer**：消融实验（Table 7）显示，Conformer 架构在相同事件条件下提供更优的 FID 和 R-Precision，原因在于其结合了自注意力的长期建模能力和卷积的局部平滑特性，更适合运动序列的时间结构。

- **ATII 与 LIMM 的必要性**：移除 LIMM 或 ATII 均导致 FID 和 R-Precision 下降（Table 16），尤其在复杂事件条件下，表明局部平滑和自适应全局语义注入对于事件级生成至关重要。

整体而言，Event-T2M 的 pipeline 通过将文本到动作生成问题从单一全局嵌入扩展到事件级条件注入，使模型能够在生成过程中专注于每个语义自包含的动作单元，同时通过全局标记保持整体连贯性，从而在复杂的多动作序列上实现顺序准确、过渡自然的运动合成。



Event-T2M 的生成框架围绕一个核心设计展开：将文本到动作的条件建模从单一全局嵌入扩展为**事件序列的显式注入**。其关键模块链路由 LLM 事件分解器、TMR 事件编码器、全局标记提取、以及扩散去噪器中的 Conformer 块与事件交叉注意力（ECA）组成。以下聚焦于决定模型行为的关键公式及其变量含义。

### 事件嵌入与堆叠

给定输入文本提示 $W$，LLM 将其分解为事件子句序列 $\{C_k\}_{k=1}^{K}$。每个子句 $C_k$ 通过运动感知的 TMR 编码器 $f_{\mathrm{TMR}}$ 映射为事件嵌入：

$$E_k = f_{\mathrm{TMR}}(C_k), \qquad E_k \in \mathbb{R}^{D_y}$$

其中 $D_y$ 为嵌入维度。所有事件嵌入被堆叠为矩阵，供后续交叉注意力使用：

$$\boldsymbol{E} = \left[ \begin{array}{l} \boldsymbol{E}_{1}^{\top} \\ \vdots \\ \boldsymbol{E}_{K}^{\top} \end{array} \right] \in \mathbb{R}^{K \times D_{y}}$$

同时，整个提示 $W$ 也被编码为全局文本标记 $G = f_{\mathrm{TMR}}(W)$，用于提供整体语义连贯性。

### 局部信息建模模块（LIMM）

在每个 Event-T2M 块内部，首先通过 LIMM 在时间维度上强制局部平滑，防止生成动作出现帧间不连续：

$$\mathrm{LIMM}(x_t) = \mathrm{ReLU}(\mathrm{GN}(\mathrm{PW}(\mathrm{DW}(x_t))))$$

其中 $\mathrm{DW}$ 为深度可分离 1D 卷积，$\mathrm{PW}$ 为逐点卷积，$\mathrm{GN}$ 为 GroupNorm。该模块作用于运动表示 $x_t$ 与时间步 $t$ 的拼接结果。

### 自适应文本注入器（ATII）

全局文本标记 $G$ 通过门控机制自适应地注入运动特征。对于下采样的运动特征 $m_j'$，门控向量由 Sigmoid 生成并与 $G$ 逐通道相乘：

$$\hat{g}_j = \mathrm{Sigmoid}(W_c[m_j' \oplus G]) \odot G$$

这里 $\oplus$ 表示拼接，$W_c$ 为可学习权重。门控机制使模型能够根据当前运动上下文动态调节全局语义的注入强度。

### 事件交叉注意力（ECA）

ECA 是 Event-T2M 的核心条件注入机制。在多头交叉注意力中，运动标记作为查询 $Q_m^{(h)}$，事件标记作为键 $K_e^{(h)}$ 和值 $V_e^{(h)}$：

$$A^{(h)} = \mathrm{softmax}\bigg( \frac{Q_m^{(h)} (K_e^{(h)})^{\top}}{\sqrt{d_h}} \bigg), \quad Z^{(h)} = A^{(h)} V_e^{(h)}$$

所有注意力头的输出拼接后，经过可学习的缩放因子 $\gamma$ 和 Dropout：

$$ECA(x_t, E) = \gamma \cdot \mathrm{Dropout}(Z)$$

$\gamma$ 初始化为接近零的值，以保证训练初期的稳定性。ECA 使扩散过程中的每一步都能直接关注到每个独立事件，从而显式建模动作的顺序和组合关系。

### 扩散训练目标

运动生成被形式化为条件去噪扩散过程。前向过程从真实运动 $x_0$ 生成带噪样本：

$$x_t = \sqrt{\bar{\alpha}_t} x_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

去噪器 $\varphi_{\boldsymbol{\theta}}$ 以时间步 $t$、全局标记 $G$ 和事件标记 $E$ 为条件，预测原始运动 $x_0$：

$$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\boldsymbol{x}_0, t, \epsilon} \Big[ \| \boldsymbol{x}_0 - \varphi_{\boldsymbol{\theta}}(\boldsymbol{x}_t, t, G, E) \|_2^2 \Big]$$

该损失函数驱动模型从噪声中恢复出与事件序列一致的干净运动。推理时采用 10 步 DDPM 采样（Table 5 消融证实该设置在效率与质量间取得平衡）。



## 实验与关键发现

### 核心瓶颈与因果机制

现有文本到动作生成系统（如 **T2M** (Guo et al., 2022)、**MDM** (Tevet et al., 2022)、**MotionDiffuse** (Zhang et al., 2024a) 等）普遍将整个复杂多动作提示压缩为单一全局文本嵌入（如 CLIP 的 `[EOS]` 标记）。这种设计无法保留动作的时间顺序和独立语义，导致生成结果中出现动作遗漏、顺序重排和不自然的过渡——这是制约复杂多动作合成的根本瓶颈。

Event-T2M 的因果调节变量在于：将文本提示显式分解为独立事件序列，为每个事件生成专用的运动感知嵌入，并通过**事件级交叉注意力（ECA）**将这些事件标记注入扩散模型的 Conformer 块中。这使得模型能够在生成过程中专注于每个语义自包含的动作单元，同时通过全局标记保持整体连贯性。这一设计将文本到动作生成的问题从单一全局嵌入扩展到事件级条件注入，从而在复杂的多动作序列上实现顺序准确、过渡自然的运动合成。

### 主实验结果

#### 标准基准上的性能

在 HumanML3D、KIT-ML 和 Motion-X 三个标准测试集上，Event-T2M 与 14 个现有最先进方法进行了全面比较（Table 1 和 Table 2）。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/002_Table_1.jpg]]
*Table 1: Comparison on the HumanML3D, KIT-ML, and Motion-X test sets with existing state-ofthe-art approaches. For each metric, “↑” denotes that larger values are better, while “↓” denotes that smaller values are better. The best score is marked in bold and the second-best is underlined*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/003_Table_2.jpg]]
*Table 2: Comparison on the HumanML3D, KIT-ML, and Motion-X test sets with MARDM approaches. For each metric, “↑” denotes that larger values are better, while “↓” denotes that smaller values are better*

**HumanML3D 数据集**上，Event-T2M 在多项关键指标上达到最优：
- **R-Precision Top-1** 达到 0.562±.002，显著优于次优方法 **MoGenTS** (Yuan et al., 2024) 的 0.529±.003，提升 +0.033。
- **MM-Dist** 为 2.804±.014，**MModality** 为 0.432±.013，均达到最优水平。
- **FID** 为 0.056±.002，虽非最优（**MoMask** (Guo et al., 2024) 为 0.045±.002），但仍处于极具竞争力的水平。

与 **MARDM** 系列方法（Meng et al., 2024）的比较（Table 2）进一步验证了优势：Event-T2M 在 HumanML3D 上的 R-Precision Top-1 为 0.549±.002，显著高于 **MARDM-SiT** 的 0.500±.004。

**KIT-ML 数据集**上，Event-T2M 在语义对齐方面表现突出：
- **MM-Dist** 为 2.742±.016（最优），**MModality** 为 0.762±.026（最优），相比次优方法 **Light-T2M** (Zeng et al., 2025) 的 1.005±.036 降低了 0.243，表明生成多样性更好。

**Motion-X 数据集**上，Event-T2M 同样表现优异：
- **R-Precision Top-1** 为 0.519±.005，显著优于 **Light-T2M** 的 0.473±.006，提升 +0.046。
- **FID** 为 0.115±.004，优于 **MARDM-SiT** 的 0.134±.006。

#### 复杂多事件基准上的优势

HumanML3D-E 基准按事件数量分层评估，是验证事件级条件设计有效性的核心实验（Table 3）。随着事件数量增加，Event-T2M 的优势愈发显著：

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/004_Table_3.jpg]]
*Table 3: Comparative results on HumanML3D-E against state-of-the-art baselines. “Condition 2/3/4” denotes prompts with at least 2, 3, and 4 events, respectively*

**Condition 2（≥2 事件）**：
- R-Precision Top-1 为 0.536，FID 为 0.079，两项指标均优于所有基线。

**Condition 3（≥3 事件）**：
- R-Precision Top-1 为 0.487，FID 为 0.137，优势持续扩大。

**Condition 4（≥4 事件）**——最具挑战性的条件：
- **R-Precision Top-1** 达到 0.466±.008，显著优于最佳基线 **MoMask** 的 0.441±.013（+0.025）。
- **FID** 为 0.265±.007，远低于 **MoMask** 的 0.418±.030（降低 0.153），表明生成质量在复杂条件下具有压倒性优势。
- **MM-Dist** 为 3.063，同样优于所有比较方法。

Figure 2(a) 直观展示了这一趋势：随着事件数从 ≥1 增加到 ≥4，所有基线的 FID 急剧上升、R-Precision 快速下降，而 Event-T2M 保持了最低的 FID 和最高的 R-Precision，退化幅度远小于其他方法。Figure 2(b) 的效率分析显示，在 ≥4 事件条件下，Event-T2M 以较小的模型参数量实现了最高的准确度，展现了紧凑性与可扩展性。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/007_Figure_2.jpg]]
*Figure 2: Overall comparison of Event-T2M: (a) As event counts increase ( $\geq$ 1 , $\geq$ 2 , $\geq$ 3 , $\geq$ 4 ) , Event-T2M consistently achieves the lowest FID and the highest R-Precision, while baselines degrade sharply under compositional complexity. (b) Efficiency analysis at ≥4 events shows that Event-T2M achieves high accuracy with low model size, demonstrating its compactness and scalability

在 KIT-ML-E 和 Motion-X-E 上的扩展实验（Table 10、Table 11）进一步验证了跨数据集的一致性优势。

### 消融实验

#### 事件级条件 vs. 词级条件

Table 4 对比了 TMR 和 CLIP 编码器在词级（Token-level）和事件级（Event-level）条件下的性能。核心发现：
- 在 TMR 编码器设置下，事件级条件在 Condition 2 的 R-Precision Top-1 为 0.536，优于词级条件的 0.521；在 Condition 4 下，事件级的 FID 为 0.265，显著优于词级的 0.329。
- 事件级交叉注意力（ECA）相比词级注意力能持续提高 R-Precision 并降低 MM-Dist，尤其在事件数较多的条件下，验证了事件级语义单元对于保持动作顺序和独立性的关键作用。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/008_Table_4.jpg]]
*Table 4: Ablation study on text encoders and conditioning methods on HumanML3D-E*

#### 架构组件消融

**LIMM 与 ATII 的必要性**（Table 16）：移除 LIMM（局部信息建模模块）或 ATII（自适应文本注入器）均导致 FID 上升和 R-Precision 下降，特别是在复杂事件条件下。例如，在 Condition 4 下，完整模型的 FID 为 0.265，而移除 LIMM 后升至 0.303，移除 ATII 后升至 0.296，证实这些组件对于事件级生成至关重要。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/027_Table_16.jpg]]
*Table 16: Ablations for LIMM and ATII. “Condition 2/3/4” denotes prompts with at least 2, 3, and 4 events, respectively*

**Conformer vs. Transformer**（Table 7）：在相同事件条件下，Conformer 架构相比 Transformer 在 FID 和 R-Precision 上均提供更优性能。例如，Condition 4 下 Conformer 的 FID 为 0.265、R-Precision Top-1 为 0.466，而 Transformer 为 0.313 和 0.451。Conformer 中卷积与自注意力的结合有效增强了局部时序建模能力。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/015_Table_7.jpg]]
*Table 7: Ablation study on the architecture design (Transformer vs. Conformer)*

**CFG Scale 与采样步数**（Table 5、Table 6）：CFG Scale=4 在各项指标上达到最佳平衡；采样步数为 10 时综合性能最优，验证了扩散过程配置的合理性。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/013_Table_5.jpg]]
*Table 5: Sampling Step ablation. R represents R-Precision*

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/014_Table_6.jpg]]
*Table 6: CFG Scale ablation*

#### 编码器公平性验证

为排除 TMR 编码器本身带来的优势，作者在 Table 15 中将所有基线统一替换为 TMR 编码器后重新评估。结果表明，仅替换编码器并不能弥补基线的不足，Event-T2M 的优势源于事件级条件设计与架构的协同，而非编码器选择。

#### 事件分解可靠性

LLM 的事件分解准确度达到 93.3%。为进一步验证方法不依赖于特定 LLM 管道，作者在人工标注的 LLM-free 测试集上重新评估（Table 14），在 ≥4 事件条件下，Event-T2M 的 R-Precision Top-1 为 0.460、FID 为 0.268，仍显著优于所有基线，证实了事件级条件设计本身的鲁棒性。

### 用户研究

Figure 3 展示了基于 7 分 Likert 量表的用户研究结果，评估维度包括保真度（Fidelity）、顺序对齐（Order alignment）和自然度（Naturalness）。Event-T2M 在所有三个维度上均显著优于其他方法（p < 0.01），且与真实运动（GT）之间无统计学显著差异。这表明 Event-T2M 生成的复杂多动作序列不仅在自动指标上表现优异，在人类感知层面也达到了接近真实的水平。

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/011_Figure_3.jpg]]
*Figure 3: Results of the user study (7-point Likert scale). Error bars denote standard errors. (a) Fidelity, (b) Order alignment, and (c) Naturalness. Event-T2M achieves significant gains over all competing methods and performs on par with ground-truth (GT)*

### 定性分析

Figure 4 展示了一个包含 7 个事件的复杂提示的定性比较。Event-T2M 是唯一能够按正确顺序执行所有动作的方法，而基线方法普遍出现动作遗漏或顺序错误。这直观验证了事件级分解和条件注入在保持长序列动作完整性方面的核心作用。

### 推理效率

Table 17 显示，Event-T2M 包含 LLM 预处理的总推理时间为 1.6 秒，其中模型本身仅需 0.17 秒。虽然 LLM 事件分解引入了约 1.43 秒的额外延迟，但考虑到复杂多动作场景下生成质量的显著提升，这一开销是可接受的。

### 局限与失败模式

尽管 Event-T2M 在复杂多动作合成上取得了显著进展，仍存在以下局限：
1. **物理合理性不足**：当前模型未考虑长时间运动的物理约束，可能导致生成的运动在物理上不自然。
2. **人物-物体交互缺失**：未建模人物与物体的自然交互，限制了在具身智能等场景的应用。
3. **下游集成尚未实现**：方法尚未无缝集成到动画管线、具身智能体和视频制作等实际应用中。
4. **LLM 延迟开销**：事件分解步骤引入了不可忽略的预处理延迟，对实时应用构成挑战。

### 开放问题

基于上述局限，作者提出了四个值得进一步探索的方向：
- 如何将物理感知目标纳入事件条件生成，以提升长时间运动的合理性？
- 如何实现生成运动中的细粒度事件编辑，支持交互式创作？
- 如何将事件条件扩展到涉及视觉和音频的多模态环境？
- 如何进一步提高事件分解的效率和准确性，降低预处理延迟？

### 补充图表

![[assets/figures/papers/paper_list_l14_https_openreview_net_forum_id_mXPeXZ1KWT/figures/020_Table_8.jpg]]
*Table 8: Event-aware prompt: Incorporates our proposed definition of event to guide segmentation*



## 定位与知识库关联

### 问题定位与核心瓶颈

现有文本到动作生成系统（Text-to-Motion）普遍采用单一全局文本嵌入（如CLIP的[EOS]标记）来条件化整个运动生成过程。这种设计在处理复杂多动作提示时暴露出根本性缺陷：全局嵌入将多个独立动作的语义压缩为单一向量，无法保留动作的时间顺序和独立语义，导致生成结果中出现动作遗漏、顺序重排、以及不自然的过渡动作。该瓶颈在提示包含三个及以上独立事件时尤为突出——基线方法的FID和R-Precision随事件数增加而急剧恶化，而Event-T2M的提出正是为了系统性地解决这一“组合复杂性”下的语义保真度问题。

### 方法谱系与关键分叉

Event-T2M位于扩散式文本到动作生成的方法谱系中，其架构演化可从三个关键设计维度溯源：

**扩散生成范式**。Event-T2M继承了**MDM**（Tevet et al., 2022）和**MotionDiffuse**（Zhang et al., 2024a）的扩散框架，采用10步DDPM进行高效采样。与这些将全局文本嵌入作为唯一条件源的方法不同，Event-T2M将条件空间从单一全局向量扩展为“全局语义标记 + 事件序列标记”的双层级结构。

**文本条件表示**。在编码器选择上，Event-T2M采用TMR（Text-to-Motion Retrieval）编码器替代主流使用的CLIP。TMR编码器经过运动-文本对比预训练，生成的嵌入对运动语义更为敏感。消融实验（Table 4）表明，即便在相同的事件级条件下，TMR编码器相比CLIP能持续提升R-Precision，尤其在事件数≥3时优势更显著。

**条件注入机制**。这是Event-T2M与基线方法最本质的分叉点。**T2M-GPT**（Zhang et al., 2023a）和**MoMask**（Guo et al., 2024）等基于VQ-VAE的方法将文本条件注入离散的码本空间，但条件本身仍为全局表示。**AttT2M**（Zhong et al., 2023）和**GraphMotion**（Jin et al., 2023）尝试通过注意力机制或图结构建模动作间关系，但未将条件表示本身拆解为事件级语义单元。Event-T2M的核心创新在于将条件注入从“词级交叉注意力”升级为“事件级交叉注意力（ECA）”：运动标记作为查询（Query），事件标记作为键和值（Key/Value），使模型在生成每个时间步的运动时能够显式关注到独立的语义事件单元。消融实验（Table 4）证实，事件级条件相比词级条件在HumanML3D-E的所有事件数条件下均提升R-Precision并降低MM-Dist。

**Conformer架构**。Event-T2M选择Conformer（Gulati et al., 2020）而非标准Transformer作为骨干网络。Conformer将自注意力与卷积结合，在保持长程依赖建模能力的同时通过卷积核引入局部时间平滑。消融实验（Table 7）显示，在相同事件条件下，Conformer相比Transformer在FID和R-Precision上均有稳定提升，表明局部平滑对事件级运动生成的连贯性具有正向贡献。

### 关键组件与因果机制

Event-T2M的架构由以下核心模块构成，其因果作用已通过消融实验验证：

- **LLM事件分解器**：使用Gemini 2.5 Flash将输入提示分解为事件子句序列。该模块的准确度达到93.3%，且人工标注测试集的结果与LLM分割结果一致（Table 14），表明方法不依赖于特定的LLM管道。
- **TMR事件编码器**：为每个事件子句生成运动感知的事件嵌入$E_k = f_{\mathrm{TMR}}(C_k)$，同时为整个提示生成全局语义嵌入$G$。
- **LIMM（局部信息建模模块）**：$\mathrm{LIMM}(x_t) = \mathrm{ReLU}(\mathrm{GN}(\mathrm{PW}(\mathrm{DW}(x_t))))$，通过深度可分离1D卷积在时间维度上强制局部平滑。
- **ATII（自适应文本信息注入器）**：$\hat{g}_j = \mathrm{Sigmoid}(W_c[m_j' \oplus G]) \odot G$，根据当前运动上下文自适应地门控全局文本语义的注入。
- **ECA（事件交叉注意力）**：$A^{(h)} = \mathrm{softmax}\big( \frac{Q_m^{(h)} (K_e^{(h)})^{\top}}{\sqrt{d_h}} \big), \quad Z^{(h)} = A^{(h)} V_e^{(h)}$，使用运动标记查询事件标记，输出经过可学习缩放因子$\gamma$和Dropout调节。
- **扩散去噪器**：训练目标为$\mathcal{L}(\boldsymbol{\theta}) = \mathbb{E}_{\boldsymbol{x}_0, t, \epsilon} \big[ \| \boldsymbol{x}_0 - \varphi_{\boldsymbol{\theta}}(\boldsymbol{x}_t, t, G, E) \|_2^2 \big]$，从带噪样本直接预测原始运动。

消融实验（Table 16）表明，移除LIMM或ATII均导致FID上升和R-Precision下降，尤其在复杂事件条件下（≥4事件），证实了这些组件对于事件级生成的必要性。

### 适用边界与局限

1. **物理合理性**：当前模型未考虑长时间运动的物理约束（如平衡、关节限制），生成结果可能在极长序列上出现物理不合理的情况。
2. **人物-物体交互**：模型未建模人物与物体的自然交互，无法处理“拿起杯子”等涉及外部物体的动作。
3. **推理延迟**：LLM事件分解引入了约1.43秒的额外延迟，总推理时间为1.6秒（模型本身仅需0.17秒），对实时应用构成一定开销。
4. **下游集成**：尚未无缝集成到动画管线、具身智能体或视频制作等下游应用中。

### 开放问题

- 如何将物理感知目标纳入事件条件生成，以保障长时间运动的物理合理性？
- 如何实现生成运动中的细粒度事件编辑（如替换、插入或删除单个事件）？
- 如何将事件条件扩展到涉及视觉和音频的多模态环境？
- 如何进一步提高事件分解的效率和准确性，降低LLM调用的延迟开销？



## 原文 PDF

![[paperPDFs/ICLR_2026/Event_T2M_Event_level_Conditioning_for_Complex_Text_to_Motion_Synthesis.pdf]]
