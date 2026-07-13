---
title: "MIBURI: Towards Expressive Interactive Gesture Synthesis"
type: paper
paper_level: A
venue: CVPR
year: 2026
pdf_ref: paperPDFs/CVPR_2026/MIBURI_Towards_Expressive_Interactive_Gesture_Synthesis.pdf
project_link: "https://vcai.mpi-inf.mpg.de/projects/MIBURI"
code_link: null
aliases:
- MIBURI
tags:
- CVPR_2026
- topic/vision_multimodal_applications
- topic/vision_multimodal_applications/3d_rendering_reconstruction
core_operator: 直接利用语音-文本基础模型Moshi内部对齐的令牌流作为条件，构建时间维度与运动学维度的双重自回归Transformer结构，结合残差矢量量化（RVQ）分体素编码，实现低时延因果生成。
primary_logic: 通过体素感知的残差矢量量化（RVQ）编码层次化运动细节，解耦时间与运动学维度并分别由因果Transformer建模；引入对比InfoNCE损失和语音激活损失以防止自回归模型坍塌至静态姿势，从而在因果约束下仍能生成多样化、与语音对齐的富有表现力的手势。
claims:
- MIBURI在BEAT2多说话人评估中以FGD 0.480和BeatAlign 0.461超越了包括EMAGE、GestureLSM等离线基线
- 在用户感知研究中，MIBURI在自然度和语音匹配度上显著优于EMAGE和GestureLSM（p<0.001）
- MIBURI实现每帧仅36ms的低延迟，是现有方法中延迟最低的实时方案
- 消融实验证明双重Transformer结构、对比损失和Moshi特征对提升手势生成质量至关重要
---

# MIBURI: Towards Expressive Interactive Gesture Synthesis

> [!tip] 核心洞察
> 通过体素感知的残差矢量量化（RVQ）编码层次化运动细节，解耦时间与运动学维度并分别由因果Transformer建模；引入对比InfoNCE损失和语音激活损失以防止自回归模型坍塌至静态姿势，从而在因果约束下仍能生成多样化、与语音对齐的富有表现力的手势。

| 字段 | 内容 |
|------|------|
| 中文题名 | MIBURI: 面向富有表现力的交互式手势合成 |
| 英文题名 | MIBURI: Towards Expressive Interactive Gesture Synthesis |
| 会议/期刊 | CVPR 2026 |
| Links | [paper](https://arxiv.org/abs/2603.03282) · [Project](https://vcai.mpi-inf.mpg.de/projects/MIBURI) |
| Topic | #topic/vision_multimodal_applications #topic/vision_multimodal_applications/3d_rendering_reconstruction |
| Method | MIBURI |
| Dataset | BEAT2, Embody3D |

> [!tip] 效果简介
> - BEAT2 (多说话人, 23 speakers) 上，FGD ↓ 0.480 (MIBURI+Face) vs 0.850 (EMAGE*) (↓0.370)；BeatAlign → 0.461 (MIBURI+Face) vs 0.236 (EMAGE*) (↑0.225)；L1-Div → 10.44 (MIBURI+Face) vs 6.58 (EMAGE*) (↑3.86)。
> - BEAT2 (单说话人 - Scott) 上，BeatAlign → 0.790 (MIBURI) vs 0.795 (EMAGE) [最接近] (基本持平)。
> - 延迟分析 (RTX 3090) 上，每帧时间 (s) 0.0349 ± 0.0017 vs 0.1680 (GestureLSM) / 1.269 (MambaTalk) (最低延迟)。

## 概要

**核心问题**：现有生成式协同语音手势合成方法普遍依赖未来语音上下文，推理延迟高，难以满足具身对话代理（ECA）所需的**在线、因果、实时交互**要求，导致手势表现力与交互流畅性无法兼得。

**核心方案**：MIBURI 直接利用语音-文本基础模型 **Moshi** 内部对齐的语音/文本令牌流作为条件，构建**时间维度与运动学维度的双重自回归 Transformer** 结构，结合**分体素残差矢量量化（RVQ）** 编码，实现低时延因果生成。通过引入**对比 InfoNCE 损失**和**语音激活损失**，有效防止自回归模型坍塌至静态姿势，在因果约束下仍能生成多样化、与语音对齐的富有表现力的手势。

**方法定位**：MIBURI 属于**在线因果手势生成**范式，区别于 **EMAGE**、**CaMN** 等非因果离线方法，以及 **GestureLSM**、**MambaTalk** 等实时基线。其核心创新在于：（1）绕过传统 ECA 复杂的多组件管线，直接从语音-文本基础模型的内嵌令牌生成手势；（2）通过体素感知的 RVQ 编码层次化运动细节，并以时间-运动学解耦的 Transformer 分别建模时间动态与体素层次结构。

**关键结果**：
- 在多说话人 BEAT2 评估中，MIBURI 以 **FGD 0.480** 和 **BeatAlign 0.461** 超越包括 EMAGE、GestureLSM 在内的所有基线（Table 2）。
- 用户感知研究中，MIBURI 在自然度和语音匹配度上显著优于 EMAGE 和 GestureLSM（p<0.001，Figure 4）。
- 推理延迟仅 **36 ms/帧**，为现有方案中最低的实时系统（Table 4）。
- 消融实验证实：双重 Transformer 结构、对比损失和 Moshi 特征对生成质量均至关重要（Table 5–7）。

**局限与开放问题**：因果建模导致语义性手势（如隐喻手势）有限，节拍手势占主导；当前框架尚未利用对话对方的肢体动态信息，无法实现完整双向交互；对域外说话人和极端风格的泛化能力有待验证。未来方向包括从 LLM 中间特征解耦对话意图以提升因果手势的语义性，以及将多模态对话线索融入生成过程。



### 具身对话代理中的手势生成困境

具身对话代理（Embodied Conversational Agent, ECA）需要实时生成与语音同步的全身手势和面部表情，以支撑自然的人机交互。协同语音手势（co-speech gesture）不仅传递语义信息，还承担着调节对话节奏、表达情感与态度的关键功能。然而，现有手势生成方法普遍面临一个根本性矛盾：**生成质量与交互实时性难以兼得**。

一方面，以 **EMAGE**、**CaMN**、**RAG-Gesture** 为代表的离线手势合成方法在生成质量上取得了显著进展。这些方法依赖完整的未来语音上下文进行非因果建模，能够提前规划语义性手势（如隐喻手势），在BEAT2等基准上展现出良好的语音-手势对齐能力。但它们的推理延迟高、无法满足在线交互需求，本质上不适合ECA场景。

另一方面，面向实时交互的因果生成方法（如 **GestureLSM** 的流匹配变体、**MambaTalk** 的状态空间模型变体）虽然满足了因果性约束，却在手势表现力和多样性上大打折扣。因果注意力掩码使得模型无法预知即将到来的语音内容，生成的手势往往退化为重复、僵硬的节拍性运动，缺乏与语义内容匹配的丰富表达。

### 现有管线的结构性缺陷

传统ECA系统的工程管线进一步加剧了这一问题。如图Fig. 2所示，现有方案通常需要串联多个独立组件：自动语音识别（ASR）→ 大语言模型（LLM）→ 文本到语音合成（TTS）→ 手势生成。这种级联架构不仅引入累积延迟，更致命的是**各模块之间的信息传递存在语义损耗**——LLM生成的文本令牌丢失了语音的韵律、重音、情感等副语言信息，而TTS输出的声学特征又难以回溯对话的深层语义意图。手势生成器最终只能基于贫瘠的中间表征进行条件建模，难以产出与语音自然耦合的富有表现力的手势。

### 核心瓶颈与本文动机

上述问题的本质瓶颈可归结为：**现有生成式协同语音手势合成方法依赖未来语音上下文，推理延迟高，无法满足ECA所需的在线、因果、实时交互要求，导致难以同时保障手势表现力与交互流畅性**。

本文提出的 **MIBURI**（Multimodal Interactive Body and Utterance Rendering Interface）直接针对这一瓶颈。核心思路是**绕过传统级联管线的信息瓶颈，直接利用语音-文本基础模型Moshi内部对齐的令牌流作为条件**，在因果约束下实现低延迟、富有表现力的手势生成。Moshi作为全双工口语对话模型，其内部令牌流天然融合了语义、韵律与声学信息，且以流式方式逐帧产出，为构建真正的在线因果手势生成系统提供了理想的条件信号。

通过体素感知的残差矢量量化（RVQ）编码层次化运动细节，并设计时间-运动学双重自回归Transformer结构，MIBURI在保持每帧仅36ms低延迟的前提下，首次在因果生成框架中实现了超越离线基线的生成质量——在多说话人BEAT2评估中，FGD达到0.480，BeatAlign达到0.461，均显著优于EMAGE等非因果方法。这标志着实时手势生成从“牺牲质量换速度”走向“质量与速度兼得”的重要一步。



## 核心方法与创新机理

MIBURI的核心创新在于**以因果、实时的方式解决了富有表现力的协同语音手势生成问题**，打破了现有方法依赖未来语音上下文、推理延迟高的瓶颈。其创新体系可从以下四个维度理解：

### 1. 语音条件来源的根本转变：从声学特征到语音-文本基础模型内部令牌流

传统协同语音手势合成方法（如CaMN、EMAGE、RAG-Gesture）普遍使用wav2vec或外部TTS提取的声学特征作为条件输入。这些特征虽然包含了韵律信息，但语义表达能力有限，且往往需要访问未来帧才能获得稳定表示，天然违背因果性要求。

MIBURI直接利用**Moshi语音-文本基础模型内部对齐的令牌流**作为条件。Moshi在生成全双工口语对话时，内部维护着多层级的语音令牌$\mathbf{f}^{\mathrm{speech}} \in \mathbb{R}^{T \times \bar{K}^{\mathrm{speech}} \times \bar{d}}$和文本令牌$\mathbf{f}^{\mathrm{text}} \in \mathbb{R}^{T \times K^{\mathrm{text}} \times d}$，这些令牌天然具备因果性（仅依赖当前及历史信息），且同时编码了语义内容和韵律细节。这一转变的实质是将手势生成“嫁接”到语音生成模型的内部表征上，使得手势模型无需自行从音频中解耦语义与韵律，也无需等待未来上下文即可获得丰富的条件信息。

消融实验（Table 5）为这一创新提供了决定性证据：将Moshi令牌替换为wav2vec特征后，FGD从0.480急剧恶化至1.103，BeatAlign从0.461下降至0.405，证明了Moshi内部语义-韵律对齐令牌的不可替代性。

### 2. 运动标记化的层次化解耦：分体素残差矢量量化

基线方法通常使用单一的VQ-VAE对全身运动进行编码，或根本未使用分体素编码策略。MIBURI提出了**分体素（Body-part aware）的残差矢量量化（RVQ）**方案：将每个姿态解耦为上身（含手部）$\mathbf{g}^u$、下身（含全局位移与脚部接触）$\mathbf{g}^l$和面部表情$\mathbf{g}^f$三个独立部分，各自训练独立的RVQ-VAE编解码器，最终沿运动学级别轴拼接为完整令牌序列$\mathbf{g} = \mathrm{Concat}(\mathbf{g}^u, \mathbf{g}^l, \mathbf{g}^f)$。

这一设计的核心洞察在于：不同身体部位的运动具有不同的动态特性和与语音的关联模式。面部表情与语音的语义/情感高度耦合，上身手势承载主要的语义表达功能，而下身运动更多反映姿态稳定与空间位移。分体素编码使得每个部位的码书可以专注于其特有的运动模式，残差结构则通过多级码书（$K=8$时MPJPE降至0.016m，Table 8）层次化地捕捉从粗粒度到细粒度的运动细节。

### 3. 生成架构的维度解耦：时间Transformer与运动学Transformer的双重自回归结构

现有生成架构通常采用单一的自回归Transformer（如CaMN）或非因果的扩散/流匹配模型（如EMAGE、GestureLSM）。MIBURI提出了**时间维度与运动学维度的双重解耦自回归结构**：

- **时间Transformer** $\mathcal{T}_{\mathrm{temporal}}$沿时间轴自回归工作，根据过去的手势令牌和当前及历史的语音/文本令牌预测隐藏状态$\mathbf{h}_t$，并输出第一运动学级别的令牌$\mathbf{g}_{(t,1)}$。这捕获了手势的跨时间动态演化。
- **运动学Transformer** $\mathcal{T}_{\mathrm{kinematic}}$在固定时间步$t$内沿运动学级别轴自回归工作，以$\mathbf{h}_t$和已生成的较低级别令牌$\mathbf{g}_{(t,<k)}$为条件，逐级预测更高级别的令牌$\mathbf{g}_{(t,k)}$。这建模了体素内部的层次化结构。

这种解耦设计的优势在于：时间Transformer可以专注于跨帧的动态连贯性，而运动学Transformer则专注于单帧内从粗到细的运动细节生成。消融实验（Table 6）表明，将双Transformer结构替换为单一Transformer后，FGD从0.480恶化至1.256，同时延迟并未显著改善，验证了维度解耦的必要性。

### 4. 训练目标的多元化：防止自回归坍塌的对比损失与语音激活损失

自回归模型在条件生成任务中容易坍塌至静态平均姿态，这是一个被广泛认知的失效模式。MIBURI通过两项创新损失函数系统性地解决了这一问题：

- **对比InfoNCE损失** $\mathcal{L}_{\mathrm{con}}$：通过Gumbel-Softmax重参数化获得可微潜变量$\mathbf{z}$，在潜空间中对匹配的GT-预测对施加吸引力，对错配对施加排斥力。这迫使生成分布保持足够的熵，防止模式坍塌。消融实验（Table 7）显示，单独使用交叉熵损失时FGD为0.704，加入$\mathcal{L}_{\mathrm{con}}$后改善至0.480，运动多样性指标L1-Div从8.56提升至10.44。
- **语音激活损失** $\mathcal{L}_{\mathrm{va}}$：一个二分类头部，强制模型区分倾听与说话状态，抑制倾听时产生“幻影手势”并强化说话时的表达性手势。这解决了对话场景中手势生成的语境敏感性问题。

完整训练目标为$\mathcal{L} = \mathcal{L}_{\mathrm{CE}} + \alpha \mathcal{L}_{\mathrm{con}} + \beta \mathcal{L}_{\mathrm{va}}$（$\alpha=0.1, \beta=0.01$），三项损失的协同作用使得模型在因果约束下仍能生成多样化、与语音对齐的富有表现力的手势。

### 创新体系的内在逻辑

上述四项创新并非孤立存在，而是构成了一个**因果生成能力栈**：Moshi令牌流提供了因果条件的语义-韵律基础（第1层），分体素RVQ提供了层次化运动表示（第2层），双重Transformer提供了匹配该表示的生成架构（第3层），而对比损失与语音激活损失则确保了在该架构下生成质量不退化（第4层）。这一能力栈使得MIBURI实现了每帧仅36ms的低延迟（Table 4），在BEAT2多说话人评估中以FGD 0.480和BeatAlign 0.461超越了包括EMAGE、GestureLSM等离线基线（Table 2），并在用户感知研究中显著优于对比方法（Figure 4，$p<0.001$）。



MIBURI 提出一种**在线、完全因果**的协同语音手势生成框架，其核心设计目标是在极低延迟下同时输出富有表现力的全身手势与面部表情，以支撑实时具身对话代理（ECA）。与传统 ECA 管线（Figure 2）依赖级联的语音识别、文本理解、手势合成等多组件不同，MIBURI 直接从语音-文本基础模型 **Moshi** 的内部令牌流中提取条件信息，从而消除因等待未来语音上下文而产生的推理延迟。

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/002_Figure_2.jpg]]
*Figure 2: Overview. Existing solutions [9, 39] to animate ECAs involve a complex pipeline (above) of multiple components to generate gestures with speech. MIBURI (below) generates full body co-speech gestures directly by utilizing internal semantic/acoustic tokens of speech-text foundation model [12]*

### 输入输出流

整个管线的输入为实时语音，输出为与语音同步的 SMPL-X 全身姿态参数，涵盖上身（含手部）、下身（含全局位移与脚部接触）以及面部表情（FLAME 参数）。其信息流转路径如下：

1. **语音-文本令牌提取**（Sec. 3.1）：Moshi 在生成全双工语音对话时，内部会同时产生对齐的语音令牌 $\mathbf{f}^{\mathrm{speech}} \in \mathbb{R}^{T \times \bar{K}^{\mathrm{speech}} \times \bar{d}}$ 和文本令牌 $\mathbf{f}^{\mathrm{text}} \in \mathbb{R}^{T \times K^{\mathrm{text}} \times d}$，这些令牌编码了从语义到韵律的多层上下文信息，作为手势生成的条件输入。

2. **分体素手势编解码**（Sec. 3.2）：将全身运动解耦为**上身** $\mathbf{g}^u$、**下身** $\mathbf{g}^l$ 和**面部** $\mathbf{g}^f$ 三个体素区域，各自独立训练残差矢量量化（RVQ）编解码器，将连续姿态序列压缩为离散运动令牌。最终手势令牌沿运动学级别轴拼接为 $\mathbf{g} = \mathrm{Concat}(\mathbf{g}^u, \mathbf{g}^l, \mathbf{g}^f)$。

3. **双重自回归生成**（Sec. 3.3）：手势生成由**时间 Transformer** 和**运动学 Transformer** 解耦完成。时间 Transformer 以因果注意力机制自回归预测每个时间步的第一级运动学令牌 $\mathbf{g}_{(t,1)}$，条件于过去的手势令牌、当前及历史的语音/文本令牌和说话人身份嵌入；运动学 Transformer 则在固定时间步内自回归预测更高运动学级别的令牌 $\mathbf{g}_{(t,k)}$，建模体素内部的层次结构。

4. **可微采样与损失约束**（Sec. 3.4–3.5）：训练时通过 Gumbel-Softmax 重参数化使离散采样可微，联合优化交叉熵损失、对比 InfoNCE 损失（防止模式坍塌至平均姿态）和语音激活损失（区分倾听/说话状态）。推理时采用核采样（top‑p=0.8/0.95）与分类器自由引导（CFG）以增强多样性和语音对齐质量。

### 模块关系

Figure 3 展示了各模块的拓扑关系：Moshi 的语音/文本令牌流并行馈入时间 Transformer 和运动学 Transformer；时间 Transformer 输出的隐藏状态 $\mathbf{h}_t$ 作为运动学 Transformer 的条件输入，后者在时间维度的每个“列”内完成运动学维度的自回归递推。三个体素的编解码器独立训练，但在生成时通过统一的令牌序列进行联合建模。这种**时间-运动学二维解耦**的设计使得模型在保持因果性的同时，能够捕获跨时间的动态变化与跨体素的层次化运动细节。

### 实时部署架构

Figure 5 展示了实时演示系统的部署方案：主推理进程以连续循环运行 Moshi 与 MIBURI，两个并行进程分别负责语音/文本可视化与运动渲染，进程间通过 WebSocket 在每个时间步流式传输数据，实现低延迟的全双工交互。消融实验（Table 4）表明，该架构在 NVIDIA RTX 3090 上达到每帧仅 **36 ms** 的推理延迟，是现有方法中延迟最低的实时方案。



### 语音-文本条件令牌流提取

MIBURI 直接利用语音-文本基础模型 **Moshi** 内部对齐的令牌流作为手势生成的条件输入，避免了传统 ECA 管线中 ASR→NLU→TTS 的多级串联延迟。Moshi 在每个时间步输出两类令牌：

- **语音令牌**：$$\mathbf{f}^{\mathrm{speech}} \in \mathbb{R}^{T \times \bar{K}^{\mathrm{speech}} \times \bar{d}}$$，包含多层残差矢量量化后的声学-韵律信息；
- **文本令牌**：$$\mathbf{f}^{\mathrm{text}} \in \mathbb{R}^{T \times K^{\mathrm{text}} \times d}$$，编码语义内容。

其中 $T$ 为时间帧数，$\bar{K}^{\mathrm{speech}}$ 和 $K^{\mathrm{text}}$ 分别为语音和文本的量化级别数，$\bar{d}$ 与 $d$ 为嵌入维度。该令牌流天然具备因果性（仅依赖当前及历史上下文），为下游手势生成提供了语义与韵律对齐的实时条件信号。

### 分体素残差矢量量化编解码器

手势序列被解耦为三个身体区域独立编码：上身（含手部）$\mathbf{g}^u$、下身（含全局位移与脚部接触）$\mathbf{g}^l$、面部表情 $\mathbf{g}^f$。每个区域分别训练一个残差矢量量化变分自编码器（RVQ-VAE），通过 $K$ 层残差码书将连续运动参数压缩为离散令牌序列。最终手势令牌沿运动学级别轴拼接：

$$\mathbf{g} = \mathrm{Concat}(\mathbf{g}^u, \mathbf{g}^l, \mathbf{g}^f)$$

其中 $K = K^u + K^l + K^f$ 为总运动学级别数。分体素设计的核心优势在于：各区域运动模式差异显著（如面部高频微表情 vs. 下身低频位移），独立码书能更高效地分配编码容量，消融实验表明增加码书数量 $K$ 可有效降低重建误差（$K=8$ 时 MPJPE 降至 0.016m）。

### 时间-运动学双重自回归 Transformer

生成架构由两个因果 Transformer 组成，分别在时间维度和运动学维度进行自回归建模：

**时间 Transformer** 捕获跨帧手势动态，根据过去手势令牌与当前及历史语音/文本令牌预测隐藏状态：

$$\mathbf{h}_t = \mathcal{T}_{\mathrm{temporal}}(\mathbf{g}_{(<t)}, \mathbf{f}_{(\leq t)}^{\mathrm{speech}}, \mathbf{f}_{(\leq t)}^{\mathrm{text}}, \mathbf{f}^{\mathrm{id}})$$

其中 $\mathbf{f}^{\mathrm{id}}$ 为说话人身份嵌入。该隐藏状态随后用于预测当前帧的第一级运动学令牌：

$$\mathbf{g}_{(t,1)} = \mathrm{Softmax}(\mathrm{Linear}(\mathbf{h}_t))$$

**运动学 Transformer** 在固定时间步 $t$ 内自回归预测更高运动学级别的令牌，条件于已生成的较低级别令牌及当前帧的语音/文本特征：

$$\mathbf{g}_{(t,k)} = \mathcal{T}_{\mathrm{kinematic}}(\mathbf{h}_t, \mathbf{g}_{(t,<k)}, \mathbf{f}_t^{\mathrm{speech}}, \mathbf{f}_t^{\mathrm{text}}, \mathbf{f}^{\mathrm{id}})$$

这种二维解耦设计的因果机制在于：时间 Transformer 仅依赖过去帧，保证因果性；运动学 Transformer 在帧内并行预测各级令牌，维持低延迟。消融实验证实双重 Transformer 结构显著优于单一 Transformer 架构（FGD 从 1.256 降至 0.480）。

### 对比 InfoNCE 损失与语音激活损失

为防止自回归模型坍塌至静态平均姿态，引入两类辅助损失：

**Gumbel-Softmax 重参数化**使离散令牌采样可微，获得潜变量：

$$\mathbf{z} = \sum_{k=1}^{K} \mathrm{GumbelSoftmax}(\tilde{\mathbf{o}}_k) \mathbf{C}_k \in \mathbb{R}^{T \times d}$$

其中 $\tilde{\mathbf{o}}_k$ 为第 $k$ 级 logits，$\mathbf{C}_k$ 为对应码书。基于此构建**对比 InfoNCE 损失**：

$$\mathcal{L}_{\mathrm{con}} = -\mathbb{E}_i\left[\log\frac{\exp(\mathrm{sim}(\mathbf{z}_{i}^{\mathrm{GT}},\mathbf{z}_{i}^{\mathrm{pred}})/\tau)}{\sum_{j=1}^{B}\exp(\mathrm{sim}(\mathbf{z}_{i}^{\mathrm{GT}},\mathbf{z}_{j}^{\mathrm{pred}})/\tau)}\right]$$

该损失强制匹配的 GT-预测潜变量对相似、推开错配对，有效提升生成手势的多样性（L1-Div 从 8.56 提升至 10.44）。

**语音激活损失** $\mathcal{L}_{\mathrm{va}}$ 为二分类头，强制模型区分倾听/说话状态，抑制倾听时的幻影手势并强化说话时的表达性。

完整训练目标为三者的加权联合：

$$\mathcal{L} = \mathcal{L}_{\mathrm{CE}} + \alpha \mathcal{L}_{\mathrm{con}} + \beta \mathcal{L}_{\mathrm{va}}$$

其中 $\alpha=0.1$，$\beta=0.01$，$\mathcal{L}_{\mathrm{CE}}$ 为标准的交叉熵损失。消融实验表明，移除对比损失后 FGD 从 0.480 退化至 0.704，验证了其在维持生成质量中的关键作用。

### 补充图表

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/004_Figure_3.jpg]]
*Figure 3: MIBURI Architecture. Given Moshi’s speech/text tokens(Sec. 3.1), our approach generates a sequence of gesture tokens, which are obtained through Body-part aware Gesture Codecs(Sec. 3.2). This online framework takes in Moshi’s text/speech token as input and predict gesture tokens through autoregressive temporal and kinematic transformers(Sec. 3.3)*

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/015_Figure_6.jpg]]
*Figure 6: Kinematic Dependency Analysis. Here, “→” means “attends to”*



## 实验与关键发现

### 核心性能：多说话人量化评估

Table 2 报告了在BEAT2数据集23个说话人上的多说话人评估结果。MIBURI在生成质量与语音对齐度上全面超越所有离线与在线基线。

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/006_Table_2.jpg]]
*Table 2: Multi-speaker evaluation. Facial-MSE scaled by*

- **FGD（Fréchet Gesture Distance）**：MIBURI+Face 达到 **0.480**，相比 EMAGE* 的 0.850 降低 0.370，降幅达 43.5%。GestureLSM 为 0.517，MambaTalk* 为 0.656，RAG-Gesture 为 0.772。该指标衡量生成手势分布与真实分布的差异，数值越低表示分布越接近真实。
- **BeatAlign**：MIBURI+Face 达到 **0.461**，显著高于 EMAGE* 的 0.236（↑0.225）和 GestureLSM 的 0.414。该指标衡量手势与语音节拍的一致性，数值越高表示节拍对齐越好。
- **L1-Div**：MIBURI+Face 达到 **10.44**，远超 EMAGE* 的 6.58，表明生成手势的运动多样性显著更高。

值得注意的是，EMAGE 和 MambaTalk 均按23说话人配置重新训练，并创建了因果变体（施加因果注意力掩码）以保证公平对比。FGD 网络亦按 EMAGE 的方式重新训练，BeatAlign 中的平均速度按基准重新计算。

### 单说话人评估

Table 3 展示了单说话人（Scott）上的评估结果。MIBURI 的 BeatAlign 达到 **0.790**，与最强离线基线 EMAGE 的 0.795 基本持平，同时 FGD 为 0.491，优于 EMAGE 的 0.508。这表明 MIBURI 在因果约束下仍能达到与离线方法相当的手势-语音对齐质量。

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/007_Table_3.jpg]]
*Table 3: Single-speaker evaluation. Facial-MSE scaled by*

### 延迟与实时性分析

Table 4 对比了各方法的推理延迟与因果性。所有测量在同一 NVIDIA RTX 3090 GPU 上进行，排除渲染时间，仅统计模型前向到输出 SMPL-X 参数的时间。

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/008_Table_4.jpg]]
*Table 4: Latency and Causality Comparison. Wall-clock time is measured from the beginning of the forward pass to the conversion of outputs into SMPL-X parameters. Render times are excluded here. #Frames / Step indicates the number of frames generated per forward pass*

- MIBURI 每帧仅需 **34.9 ± 1.7 ms**，是现有方法中延迟最低的实时方案。
- GestureLSM 每帧 168.0 ms，MambaTalk 每帧高达 1269 ms。
- MIBURI 每步生成 1 帧，保证严格的因果性；GestureLSM 和 MambaTalk 每步生成 5 帧，存在未来信息泄露。

这一低延迟特性源于时间-运动学双 Transformer 的解耦设计：时间 Transformer 仅处理单帧的时间上下文，运动学 Transformer 在固定时间步内自回归生成令牌，避免了全序列建模的计算负担。

### 跨域泛化评估

Table 9 展示了在 Embody3D 数据集上的跨域评估结果。MIBURI 的 FGD 为 **1.642**，显著优于 GestureLSM 的 3.744（↓2.102），证明该方法对不同说话人和对话场景具有较好的泛化能力。

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/014_Table_9.jpg]]
*Table 9: Quantitative evaluation on the Embody3D dataset*

### 消融实验

#### 语音特征选择

Table 5 对比了使用 Moshi 内部令牌与 wav2vec 特征的生成效果。使用 Moshi 令牌时 FGD 从 1.103 降至 **0.480**，BeatAlign 从 0.405 提升至 **0.461**。Moshi 内部对齐的语音/文本令牌流提供了更丰富的语义与韵律信息，是高质量手势生成的关键条件输入。

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/009_Table_5.jpg]]
*Table 5: Wav2vec ablation against moshi features*

#### 模型架构变体

Table 6 对比了单一 Transformer 与时间-运动学双 Transformer 架构。双 Transformer 设计使 FGD 从 1.256 降至 **0.480**，同时保持低延迟（每帧 34.9 ms vs. 33.5 ms），证明了时间维度与运动学维度解耦建模的有效性。

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/012_Table_6.jpg]]
*Table 6: Comparison of Model Variants on Gesture Generation and Runtime*

#### 损失函数组合

Table 7 系统消融了不同损失函数的作用：

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/010_Table_7.jpg]]
*Table 7: Quantitative Effect of Losses on Generation*

- 仅使用交叉熵损失（CE）时，FGD 为 0.704，L1-Div 为 8.56。
- 加入对比 InfoNCE 损失（CE + L_con）后，FGD 降至 **0.480**，L1-Div 提升至 **10.44**。对比损失通过在潜空间增强匹配 GT-预测对的相似性、推开错配对，有效防止自回归模型坍塌至平均姿态。
- 语音激活损失（L_va）进一步抑制倾听时的幻影手势并强化说话时的表达。

#### 码书数量

Table 8 展示了残差码书数量 K 对运动重建精度的影响。K=8 时 MPJPE 降至 **0.016 m**，继续增加码书数量收益递减。论文采用 K=8 的配置以平衡重建精度与计算开销。

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/011_Table_8.jpg]]
*Table 8: Effect of Number of Codebooks K on Motion Reconstruction. MPJPE is represented in meters*

### 用户感知评估

Figure 4 展示了用户感知研究结果。在自然度（Naturalness）和语音匹配度（Speech Matching）两个维度上，MIBURI 均显著优于 EMAGE 和 GestureLSM（p < 0.001）。然而，MIBURI 在两项指标上仍低于真实数据（GT），表明生成手势在整体交互质量上存在改进空间。

![[assets/figures/papers/paper_list_l995_https_arxiv_org_abs_2603_03282/figures/005_Figure_4.jpg]]
*Figure 4: User Study for Perceptual Evaluation. Here, the red line indicates chance level (50%), * stands for*

### 运动学依赖分析

Figure 6 分析了运动学 Transformer 中自注意力在各体素之间的分布。结果表明，面部令牌的自注意力集中在自身（Face→Face），模型隐式学习到忽略无关的下身令牌，验证了分体素建模的有效性。

### 失败模式与局限性

1. **语义手势受限**：因果建模导致手势无法提前于言语产生，生成的节拍手势占主导，隐喻等语义性手势仍然有限。
2. **感知质量差距**：用户评估显示生成手势的自然度和语音匹配度仍低于真实数据。
3. **缺乏双向交互**：当前框架尚未利用对话对方的肢体动态信息，无法实现完整的双向交互手势建模。
4. **域外泛化**：模型性能受限于 BEAT2 训练数据，对域外说话人及极端风格的泛化能力有待验证。
5. **资源受限设备**：尽管在 RTX 3090 上延迟很低，但在资源受限设备上的实时性能尚需进一步优化。



## 定位与知识库关联

### 1. 技术路线与基线关系

**MIBURI** 的核心定位是在线、因果、实时的协同语音手势生成框架，其技术路线与现有工作形成以下关系：

**离线手势合成基线。** 主流协同语音手势合成方法（如 **CaMN**、**EMAGE**、**RAG-Gesture**）普遍采用非因果架构，依赖未来语音上下文进行高质量手势生成。这些方法在离线评估中表现优异，但推理延迟高，无法满足具身对话代理（ECA）的实时交互需求。MIBURI 在 BEAT2 多说话人评估中以 FGD 0.480 和 BeatAlign 0.461 超越了包括 **EMAGE**（FGD 0.850, BeatAlign 0.236）在内的离线基线（Table 2），同时在用户感知研究中显著优于 EMAGE（p<0.001, Figure 4），表明因果约束下仍可取得竞争力甚至更优的生成质量。

**实时流式基线。** 现有实时方法如 **GestureLSM**（流匹配模型）和 **MambaTalk**（状态空间模型）通过不同架构实现低延迟生成。MIBURI 与两者的核心差异在于：（1）语音条件来源——MIBURI 直接利用 Moshi 内部对齐的语义/韵律令牌流，而非外部 TTS 提取的声学特征；（2）运动表示——采用分体素残差矢量量化（RVQ）编码层次化运动细节，而非单一体素 VQ-VAE；（3）生成架构——时间-运动学双重自回归 Transformer 解耦时间动态与体素层次建模。延迟对比（Table 4）显示 MIBURI 每帧仅需 34.9ms，显著低于 GestureLSM（168ms）和 MambaTalk（1269ms），是现有方法中延迟最低的实时方案。

**语音-文本基础模型利用。** MIBURI 构建于 **Moshi** 之上，直接利用其内部令牌流作为条件输入。这一设计与传统 ECA 管线（Figure 2）形成鲜明对比：传统方案需串联 ASR→NLU→对话管理→NLG→TTS→手势生成等多个模块，存在误差累积和延迟叠加问题；MIBURI 将语音生成与手势生成统一于同一令牌流，实现了全双工对话与手势的同步输出。

### 2. 核心机制创新与适用边界

**因果瓶颈的突破路径。** 现有生成式方法依赖未来语音上下文的核心原因在于：语义性手势（如隐喻手势）往往需要预知话语意图才能提前产生。MIBURI 通过 Moshi 的内部令牌流间接获取了语义与韵律的对齐信息，结合对比 InfoNCE 损失防止模式坍塌，使得在严格因果约束下仍能生成多样化手势。然而，这一设计也决定了其适用边界：因果建模导致手势无法提前于言语产生，因此语义性手势仍然有限，生成的节拍手势占主导（论文明确指出的局限）。

**分体素编码与双重 Transformer 的适用范围。** 分体素 RVQ 编解码器（脸、上身、下身）和双重 Transformer 架构的设计假设运动学层次结构可解耦建模。运动学依赖分析（Figure 6）显示面部令牌的自注意力集中在自身（Face→Face），模型隐式学习到忽略无关的下身令牌，验证了该假设的合理性。但这一设计依赖于 SMPL-X 参数化人体的体素划分，对非人形角色或不同骨骼拓扑的泛化需要重新设计编解码器。

**训练目标的互补性。** 交叉熵损失提供逐令牌的监督信号，对比 InfoNCE 损失在潜空间增强多样性（消融实验 Table 7：加入 L_con 后 FGD 从 0.704 改善至 0.480，L1-Div 从 8.56 提升至 10.44），语音激活损失强制区分倾听/说话状态以抑制幻影手势。三者联合优化（α=0.1, β=0.01）构成了互补的训练策略，但超参数对不同数据分布的敏感性有待验证。

### 3. 局限与开放问题

**语义性手势的固有局限。** 因果建模框架下，手势无法预知未来话语内容，导致隐喻性、指示性等语义手势生成能力受限。论文将此列为明确局限，并指出感知评估中生成手势的自然度和语音匹配度仍低于真实数据（GT）。

**双向交互的缺失。** 当前框架仅利用说话者的语音/文本令牌，尚未融入对话对方的肢体动态信息，无法实现完整的双向交互手势建模。这是从单工手势生成迈向全双工交互代理的关键缺口。

**域外泛化风险。** 模型训练于 BEAT2 数据集（23 说话人），对域外说话人及极端风格的泛化能力有待验证。尽管在 Embody3D 跨域评估中 FGD 从 GestureLSM 的 3.744 降至 1.642（Table 9），但该评估仅覆盖有限域外数据。

**开放研究问题包括：**
- 能否从 LLM 的中间特征中解耦出对话意图，在生成语音和手势之前共享受意图信息，以提高因果手势的语义性？
- 如何将用户的外观、肢体动作等多模态线索融入手势生成，实现完整的双向交互？
- 在保持因果性的前提下，能否引入对未来对话计划的隐式建模，以平衡表现力与因果性？
- 如何在更广泛的说话人分布和对话场景中验证该框架的鲁棒性和通用性？

### 4. 知识库定位

MIBURI 在协同语音手势生成领域的知识库中占据以下位置：

- **问题域：** 在线因果手势生成 × 语音-文本基础模型利用 × 实时具身对话代理
- **方法族：** 自回归 Transformer + 残差矢量量化（RVQ）+ 对比学习 + 分类器自由引导（CFG）
- **关键区分点：** 首个直接利用语音-文本基础模型内部令牌流进行因果手势生成的框架；时间-运动学双重自回归架构；分体素 RVQ 编码
- **性能定位：** 在 BEAT2 多说话人评估中达到 SOTA 级别的 FGD 和 BeatAlign，同时保持最低的推理延迟（34.9ms/帧）
- **未解决挑战：** 语义性手势生成、双向交互建模、域外泛化



## 原文 PDF

![[paperPDFs/CVPR_2026/MIBURI_Towards_Expressive_Interactive_Gesture_Synthesis.pdf]]
